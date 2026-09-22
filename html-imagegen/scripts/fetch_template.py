#!/usr/bin/env python3
"""Fetch a selected public template. stdout is JSON; errors go to stderr."""
from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.error import URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

DEFAULT_SITE = "https://prompts.aiplanet.live"


def resolve_selection(selection: str, site: str) -> tuple[str, str]:
    for prefix in ("style:", "composition:", "template:"):
        if selection.startswith(prefix):
            selection = selection[len(prefix):]
            break
    parsed = urlsplit(selection)
    if parsed.scheme:
        if parsed.scheme not in ("http", "https") or not parsed.netloc or parsed.username or parsed.password:
            raise ValueError("模板链接必须是无凭据的 HTTP(S) 地址")
        match = re.fullmatch(r"/image/([a-z0-9-]+)/?", parsed.path)
        if not match:
            raise ValueError("请输入图片模板详情页链接 /image/<slug>/")
        return f"{parsed.scheme}://{parsed.netloc}", match[1]
    slug = selection.split(":", 1)[-1]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("模板名称须为页面 slug 或模板 ID")
    parsed_site = urlsplit(site)
    if parsed_site.scheme not in ("http", "https") or not parsed_site.netloc or parsed_site.username or parsed_site.password:
        raise ValueError("站点必须是无凭据的 HTTP(S) 地址")
    return site.rstrip("/"), slug


def fetch_template(selection: str, site: str = DEFAULT_SITE) -> dict:
    origin, slug = resolve_selection(selection, site)
    endpoint = f"{origin}/api/v1/image/templates/{slug}.json"
    request = Request(endpoint, headers={"Accept": "application/json", "User-Agent": "PromptPlanetSkill/1"})
    with urlopen(request, timeout=30) as response:
        data = json.load(response)
    if data.get("schema_version") != 1 or not isinstance(data.get("template"), dict):
        raise ValueError("站点返回的模板 API 版本不受支持")
    template = data["template"]
    if template.get("slug") != slug:
        raise ValueError("站点返回的模板与所选页面不一致")
    dependencies = template.get("model_dependencies")
    if not isinstance(dependencies, list) or not dependencies or not set(dependencies) <= {"文本模型", "多模态模型"}:
        raise ValueError("模板缺少受支持的模型依赖，不能确定生成路线")
    prompts = template.get("prompts")
    if not isinstance(prompts, list) or any(not isinstance(p.get("body"), str) for p in prompts):
        raise ValueError("模板 API 缺少完整 Prompt 正文")
    if prompts and sum(p.get("is_default") is True for p in prompts) != 1:
        raise ValueError("模板默认 Prompt 不明确，停止自动选择")
    for key in ("page_url", "api_url"):
        template[key] = urljoin(origin + "/", template[key])
    for exemplar in template.get("exemplars", []):
        for key in ("image_url", "thumbnail_url"):
            exemplar[key] = urljoin(origin + "/", exemplar[key])
    hero = template.get("hero_image")
    if isinstance(hero, dict):  # 网页主图（L3 输出），与 exemplars[] 同样给绝对地址
        for key in ("image_url", "thumbnail_url"):
            if isinstance(hero.get(key), str):
                hero[key] = urljoin(origin + "/", hero[key])
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="读取 Prompt Planet 模板；标准输出为供 agent 消费的完整 JSON。")
    parser.add_argument("template", help="模板详情页 URL、slug 或模板 ID")
    parser.add_argument("--site", default=DEFAULT_SITE, help="使用 slug 时的站点地址")
    args = parser.parse_args()
    try:
        result = fetch_template(args.template, args.site)
    except (URLError, ValueError, KeyError, TypeError) as error:
        print(f"模板读取失败，未开始生成：{error}。请核对模板链接及站点 API 是否已发布。", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
