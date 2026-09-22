#!/usr/bin/env python3
"""Export a local HTML cover with Chromium's native element screenshot."""
from __future__ import annotations

import argparse
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import struct
import sys
import threading
from urllib.parse import quote

READY_JS = r"""async (selector) => {
  const ready = async () => {
    const element = document.querySelector(selector);
    if (!element) throw new Error('找不到导出元素 ' + selector);
    await document.fonts.ready;
    if (Array.from(document.fonts).some(font => font.status === 'error'))
      throw new Error('字体加载失败，停止导出');
    await Promise.all(Array.from(element.querySelectorAll('img')).map(async image => {
      if (!image.complete) await new Promise((resolve, reject) => {
        image.addEventListener('load', resolve, {once: true});
        image.addEventListener('error', () => reject(new Error('图片加载失败')), {once: true});
      });
      if (!image.naturalWidth) throw new Error('图片未加载，停止导出');
      await image.decode();
    }));
    const backgrounds = new Set();
    for (const node of [element, ...element.querySelectorAll('*')]) {
      for (const pseudo of [null, '::before', '::after']) {
        for (const match of getComputedStyle(node, pseudo).backgroundImage.matchAll(/url\(["']?([^"')]+)["']?\)/g))
          backgrounds.add(match[1]);
      }
    }
    await Promise.all([...backgrounds].map(async url => {
      const image = new Image(); image.src = url;
      try { await image.decode(); }
      catch { throw new Error('背景图片未加载，请检查素材链接'); }
    }));
    // Guizang production-workflow: allow 500–900ms for procedural backgrounds.
    if (element.matches('canvas') || element.querySelector('canvas'))
      await new Promise(resolve => setTimeout(resolve, 800));
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    const rect = element.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) throw new Error('导出元素不可见');
    return {width: rect.width, height: rect.height};
  };
  return await Promise.race([ready(), new Promise((_, reject) =>
    setTimeout(() => reject(new Error('封面渲染超过 60 秒，请检查字体或素材加载')), 60000))]);
}"""


class AssetHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def render(source: Path, output: Path, selector: str, width: int, height: int) -> tuple[int, int]:
    from playwright.sync_api import sync_playwright

    if not source.is_file():
        raise ValueError(f"HTML 文件不存在：{source}")
    if output.exists():
        raise ValueError(f"输出已存在，请使用新文件名：{output}")
    source = source.resolve()
    server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(AssetHandler, directory=str(source.parent)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
                page.goto(f"http://127.0.0.1:{server.server_port}/{quote(source.name)}", wait_until="load", timeout=30000)
                target = page.locator(selector)
                if target.count() != 1:
                    raise ValueError("导出选择器必须匹配唯一画布")
                result = page.evaluate(READY_JS, selector)
                if (result["width"], result["height"]) != (width, height):
                    raise ValueError(f"画布为 {result['width']}×{result['height']}，期望 {width}×{height}；请修正 HTML 尺寸")
                raw = target.screenshot(type="png", animations="disabled", scale="css", omit_background=False, timeout=30000)
            finally:
                browser.close()
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("浏览器没有返回 PNG")
    actual = struct.unpack(">II", raw[16:24])
    if actual != (width, height):
        raise ValueError(f"未保存图片：导出为 {actual[0]}×{actual[1]}，期望 {width}×{height}；请修正 HTML 画布尺寸")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as file:
        file.write(raw)
    return actual


def main() -> int:
    parser = argparse.ArgumentParser(description="把本次生成的 HTML 封面导出为原尺寸 PNG，不裁切或缩放补救。")
    parser.add_argument("html", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--selector", default="#cover")
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    args = parser.parse_args()
    if args.width <= 0 or args.height <= 0:
        parser.error("宽高必须为正整数")
    try:
        width, height = render(args.html, args.output, args.selector, args.width, args.height)
    except ImportError:
        print("尚未渲染：缺少 Playwright。请使用 uv run --with playwright python 运行本脚本。", file=sys.stderr)
        return 1
    except Exception as error:
        print(f"PNG 导出失败：{error}\n请检查 HTML；若缺少浏览器，运行 PLAYWRIGHT_SKIP_BROWSER_GC=1 uv run --with playwright python -m playwright install chromium。", file=sys.stderr)
        return 1
    print(f"已导出 PNG：{args.output.resolve()}（{width}×{height}）。请查看图片确认文字、布局和素材效果。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
