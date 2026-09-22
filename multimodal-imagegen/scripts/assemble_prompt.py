#!/usr/bin/env python3
"""把模板视觉模块与本次输入装配成四块绘图 Prompt；只用标准库。

四块与站点三层样例的装配规则相同：角色与任务 / 基本要求 / 视觉要求 / 内容与素材，
以两个换行连接。模板正文逐字进入视觉要求（开头的「执行方式」节除外——那是给执行者的）。
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HEADINGS = ("角色与任务", "基本要求", "视觉要求", "内容与素材")
EXECUTION_HEADING = "## 执行方式"


class InputError(ValueError):
    pass


def strip_execution_section(text: str) -> str:
    """去掉正文开头给执行者的「执行方式」节；其余原样返回。

    粘贴来的正文常带 BOM、CRLF 或开头空行，先归一再判；与站点 `generation_text` 同样对
    重复的标题 fail-closed——删掉一个标题把安装说明留在视觉要求里，比报错更糟。
    """
    text = text.replace("\r\n", "\n").lstrip("﻿").lstrip("\n")
    count = text.count(EXECUTION_HEADING)
    if count == 0:
        return text
    if count != 1 or not text.startswith(EXECUTION_HEADING + "\n\n"):
        raise InputError("「执行方式」节只能有一个且必须在模板正文开头；请原样粘贴模板页的完整 Prompt")
    index = text.find("\n\n## ", len(EXECUTION_HEADING))
    if index < 0:
        raise InputError("模板正文在「执行方式」节之后没有内容")
    return text[index + 2:]


def _nonempty(value: object, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{where} 必须是非空字符串")
    return value


def _strings(value: object, where: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise InputError(f"{where} 必须是字符串数组；无要求时省略或写 []")
    return value


def assemble(inputs: dict) -> str:
    if not isinstance(inputs, dict):
        raise InputError("inputs 必须是 JSON 对象")
    template = strip_execution_section(_nonempty(inputs.get("template_text"), "template_text")).strip("\n")
    scenario, artifact = inputs.get("scenario"), inputs.get("artifact")
    if not isinstance(scenario, dict) or not isinstance(artifact, dict):
        raise InputError("scenario 与 artifact 必须是对象")
    role = "\n".join((
        f"角色：{_nonempty(scenario.get('role'), 'scenario.role')}",
        f"场景：{_nonempty(scenario.get('name'), 'scenario.name')}",
        f"任务：{_nonempty(scenario.get('goal'), 'scenario.goal')}",
        f"读者：{_nonempty(scenario.get('audience'), 'scenario.audience')}",
        f"交付物：{_nonempty(artifact.get('name'), 'artifact.name')}",
    ))
    size = inputs.get("output_size")
    if (not isinstance(size, dict) or set(size) != {"width", "height"}
            or any(type(value) is not int or value <= 0 for value in size.values())):
        raise InputError("output_size 必须包含正整数 width/height（像素）")
    width, height = size["width"], size["height"]
    divisor = math.gcd(width, height)
    basic_lines = [f"- 输出规格：PNG，{width}×{height} 像素（宽×高），宽高比 {width // divisor}:{height // divisor}。"
                   "参考图的尺寸不改变输出规格。"]
    basic_lines += [f"- {item}" for item in (
        _strings(scenario.get("requirements"), "scenario.requirements")
        + _strings(artifact.get("requirements"), "artifact.requirements")
        + _strings(inputs.get("requirements"), "requirements"))]
    visual_pieces = [template]
    boundary = inputs.get("non_copy_boundary")
    if boundary:
        visual_pieces.append(f"不可复制边界：{_nonempty(boundary, 'non_copy_boundary')}")
    reference = inputs.get("reference")
    if reference:
        if not isinstance(reference, dict):
            raise InputError("reference 必须是对象（file 可选，constraints 必填）")
        visual_pieces.append(f"如附参考图：{_nonempty(reference.get('constraints'), 'reference.constraints')}")
    visual_pieces += [f"- {item}" for item in _strings(inputs.get("visual_requirements"), "visual_requirements")]
    content = _nonempty(inputs.get("content"), "content").strip("\n")
    blocks = (role, "\n".join(basic_lines), "\n\n".join(visual_pieces), content)
    prompt = "\n\n".join(f"# {heading}\n\n{body}" for heading, body in zip(HEADINGS, blocks))
    if template not in prompt:
        raise InputError("模板正文未逐字进入 Prompt")
    return prompt + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="装配四块绘图 Prompt；标准输出或 --out 文件。")
    parser.add_argument("inputs", help="inputs.json 路径")
    parser.add_argument("--out", help="写入的 prompt.txt 路径；省略则打印到标准输出")
    args = parser.parse_args(argv)
    try:
        inputs = json.loads(Path(args.inputs).read_text(encoding="utf-8"))
        prompt = assemble(inputs)
    except (OSError, ValueError) as error:
        print(f"未装配：{error}", file=sys.stderr)
        return 1
    if args.out:
        Path(args.out).write_text(prompt, encoding="utf-8")
        print(args.out)
    else:
        sys.stdout.write(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
