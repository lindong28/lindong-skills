#!/usr/bin/env python3
"""按 OPENAI_API_KEY 调用 OpenAI Images API 生成一张图；只用标准库。

无参考图走 /v1/images/generations，有参考图走 /v1/images/edits（multipart）。写出 PNG 后核对实际
宽高是否等于 --size，不一致时退出码 1 并保留文件，由调用方决定重生成——不裁切缩放。
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import tempfile
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))  # 同目录的 check_png，脚本可从任意 cwd 运行
from check_png import parse_size, png_size  # noqa: E402

API_BASE = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
DEFAULT_MODEL = "gpt-image-1.5"


def _multipart(fields: list[tuple[str, str]], files: list[tuple[str, Path]]) -> tuple[bytes, str]:
    boundary = f"----PromptPlanet{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for name, value in fields:
        chunks.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode())
    for name, path in files:
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        chunks.append((f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{path.name}\"\r\n"
                       f"Content-Type: {content_type}\r\n\r\n").encode() + path.read_bytes() + b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def request_image(prompt: str, *, size: str, model: str, quality: str | None, references: list[Path], api_key: str) -> bytes:
    if references:
        fields = [("model", model), ("prompt", prompt), ("size", size), ("n", "1")]
        if quality:
            fields.append(("quality", quality))
        body, content_type = _multipart(fields, [("image[]", path) for path in references])
        endpoint = f"{API_BASE}/images/edits"
    else:
        payload: dict = {"model": model, "prompt": prompt, "size": size, "n": 1}
        if quality:
            payload["quality"] = quality
        body, content_type = json.dumps(payload).encode(), "application/json"
        endpoint = f"{API_BASE}/images/generations"
    request = Request(endpoint, data=body, method="POST", headers={
        "Authorization": f"Bearer {api_key}", "Content-Type": content_type, "User-Agent": "PromptPlanetSkill/1",
    })
    with urlopen(request, timeout=600) as response:
        data = json.load(response)
    try:
        return base64.b64decode(data["data"][0]["b64_json"])
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise ValueError(f"响应里没有 b64_json 图片数据：{error}") from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="用 OpenAI Images API 生成一张 PNG。")
    parser.add_argument("prompt_file", help="prompt.txt")
    parser.add_argument("--out", required=True, help="输出 PNG 路径（已存在则拒绝覆盖）")
    parser.add_argument("--size", required=True, help="宽x高，如 1536x1024")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--quality", help="原样传给 API（各模型接受的取值不同，如 low / medium / high / auto）")
    parser.add_argument("--reference", action="append", default=[], help="参考图路径，可重复；有则走 edits 端点")
    args = parser.parse_args(argv)
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("缺少 OPENAI_API_KEY；未调用。请改用宿主图片工具，或设置该环境变量后重试。", file=sys.stderr)
        return 2
    out = Path(args.out)
    if out.exists():
        print(f"输出文件已存在，拒绝覆盖：{out}", file=sys.stderr)
        return 2
    try:
        width, height = parse_size(args.size)
        prompt = Path(args.prompt_file).read_text(encoding="utf-8")
        references = [Path(item) for item in args.reference]
        missing = [str(path) for path in references if not path.is_file()]
        if missing:
            raise ValueError("参考图不存在：" + ", ".join(missing))
        image = request_image(prompt, size=f"{width}x{height}", model=args.model, quality=args.quality,
                              references=references, api_key=api_key)
        # 先验明是 PNG 再落盘：返回别的格式时不留下一个挡住重试的坏文件
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as probe:
            probe.write(image)
        try:
            actual = png_size(Path(probe.name))
        finally:
            Path(probe.name).unlink(missing_ok=True)
    except HTTPError as error:
        # 自定义 OPENAI_BASE_URL 指向的代理可能把请求头回显进错误体：把 key 抹掉再打印
        detail = error.read().decode("utf-8", "replace")[:2000].replace(api_key, "***")
        print(f"API 返回 {error.code}，未生成：{detail}", file=sys.stderr)
        return 1
    except (OSError, URLError, ValueError) as error:
        print(f"未生成：{str(error).replace(api_key, '***')}", file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(image)
    result = {"path": str(out), "width": actual[0], "height": actual[1], "model": args.model,
              "endpoint": "edits" if references else "generations", "size_matches": actual == (width, height)}
    print(json.dumps(result, ensure_ascii=False))
    if actual != (width, height):
        print(f"实际尺寸 {actual[0]}×{actual[1]} 与要求 {width}×{height} 不符；文件已保留，请重新生成，不要裁切缩放。",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
