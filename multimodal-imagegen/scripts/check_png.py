#!/usr/bin/env python3
"""读 PNG 实际宽高并与期望尺寸比对；只用标准库。退出码 0 = 一致。"""
from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        head = handle.read(24)
    if len(head) < 24 or head[:8] != PNG_SIGNATURE or head[12:16] != b"IHDR":
        raise ValueError(f"不是 PNG 文件：{path}")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def parse_size(text: str) -> tuple[int, int]:
    try:
        width, height = (int(part) for part in text.lower().replace("×", "x").split("x"))
    except ValueError as error:
        raise ValueError("尺寸写成 宽x高，如 1536x1024") from error
    if width <= 0 or height <= 0:
        raise ValueError("尺寸必须是正整数")
    return width, height


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="核对 PNG 尺寸。")
    parser.add_argument("png")
    parser.add_argument("--expect", required=True, help="期望尺寸，如 1536x1024")
    args = parser.parse_args(argv)
    try:
        actual = png_size(Path(args.png))
        expected = parse_size(args.expect)
    except (OSError, ValueError) as error:
        print(f"无法核对：{error}", file=sys.stderr)
        return 2
    print(f"实际 {actual[0]}×{actual[1]}，期望 {expected[0]}×{expected[1]}")
    return 0 if actual == expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
