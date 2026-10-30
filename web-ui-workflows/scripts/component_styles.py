#!/usr/bin/env python3
"""Resolve explicit component choices against a downloaded, current catalog.

No network or UI operations. JSON output is opt-in; saved configuration is
read back before reporting it. Catalog content remains owned by its publisher.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile


class SelectionError(ValueError):
    pass


def canonical_hash(value):
    content = {key: row for key, row in value.items() if key != "content_sha256"}
    return hashlib.sha256(json.dumps(content, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def read_json(path, *, missing=False):
    try:
        raw = Path(path).read_bytes()
    except FileNotFoundError:
        if missing:
            return {"schema_version": 1, "components": {}}, None
        raise SelectionError(f"文件不存在：{path}；先取得目录或核对显式配置路径。")
    except OSError as exc:
        raise SelectionError(f"文件无法读取：{path}（{exc.strerror}）；未取得配置结果。") from exc
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise SelectionError(f"文件不是有效 JSON：{path}；修复后重新运行。") from exc
    if not isinstance(value, dict):
        raise SelectionError(f"文件根节点必须是对象：{path}。")
    return value, raw


def load_catalog(path):
    catalog, _ = read_json(path)
    if catalog.get("schema_version") != 1 or (not isinstance(catalog.get("components"), list) or not catalog["components"]):
        raise SelectionError("组件目录需要 schema_version=1 和 components 列表；请取得匹配版本。")
    identities = set()
    for row in catalog["components"]:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
            raise SelectionError("目录含缺少身份的组件；请修复目录定义。")
        if row["id"] in identities:
            raise SelectionError(f"目录组件重复：{row['id']}。")
        identities.add(row["id"])
        variants = row.get("variants")
        if not isinstance(variants, list) or not variants:
            raise SelectionError(f"组件 {row['id']} 没有可用变体。")
        ids = [v.get("id") if isinstance(v, dict) else None for v in variants]
        if any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
            raise SelectionError(f"组件 {row['id']} 的变体身份缺失或重复。")
        if row.get("default_variant") not in ids:
            raise SelectionError(f"组件 {row['id']} 的公开默认无法解析。")
        for variant in variants:
            if "template_ref" in variant and not variant.get("inherited_rules"):
                raise SelectionError(f"组件 {row['id']} 的模板继承尚未解析；请读取构建后的完整目录 API。")
    actual = canonical_hash(catalog)
    if "content_sha256" in catalog and catalog["content_sha256"] != actual:
        raise SelectionError("目录内容与 content_sha256 不一致；重新取得完整目录，不使用本次读数。")
    catalog["content_sha256"] = actual
    return catalog


def validate_config(value, path):
    if value.get("schema_version") != 1 or not isinstance(value.get("components"), dict):
        raise SelectionError(f"选择配置格式不匹配：{path}；需要 schema_version=1 和 components 对象。")
    for component, choice in value["components"].items():
        if not isinstance(choice, dict) or not isinstance(choice.get("variant"), str) or not choice["variant"]:
            raise SelectionError(f"配置 {path} 中 {component} 缺少 variant；修正该条或明确取消覆盖。")
    return value


def load_layers(paths):
    layers = {}
    for scope in ("task", "project", "user"):
        path = paths.get(scope)
        if path is not None:
            value, _ = read_json(path)  # explicit paths must exist when reading
            layers[scope] = validate_config(value, path)
    return layers


def resolve(catalog, layers, component=None):
    by_id = {row["id"]: row for row in catalog["components"]}
    if component is not None and component not in by_id:
        raise SelectionError(f"目录中没有组件 {component}；请选择目录已有用途，或补充其定义。")
    for scope, value in layers.items():
        for identity, selection in value["components"].items():
            if identity not in by_id:
                raise SelectionError(f"{scope} 配置引用未知组件 {identity}；修正引用或取消该条覆盖。")
            if selection["variant"] not in {v["id"] for v in by_id[identity]["variants"]}:
                raise SelectionError(f"{scope} 配置的 {identity}/{selection['variant']} 已不可解析；修正引用或取消覆盖，未静默回退。")
    rows = []
    for identity, definition in by_id.items():
        if component is not None and identity != component:
            continue
        source = "public_default"
        selection = {"variant": definition["default_variant"]}
        for scope in ("task", "project", "user"):
            candidate = layers.get(scope, {}).get("components", {}).get(identity)
            if candidate is not None:
                source, selection = scope, candidate
                break
        variant = next(v for v in definition["variants"] if v["id"] == selection["variant"])
        selected_hash = selection.get("catalog_sha256")
        rows.append({"component": identity, "name": definition.get("name", identity),
                     "variant": variant["id"], "variant_name": variant.get("name", variant["id"]),
                     "source": source, "definition": variant,
                     "selection_catalog_changed": bool(selected_hash and selected_hash != catalog["content_sha256"])})
    return {"status": "resolved", "catalog_sha256": catalog["content_sha256"],
            "components": rows, "ui_verified": False}


@contextmanager
def config_lock(path):
    # Cooperating CLI writers serialize the read/modify/replace transaction.
    # The lock file remains stable; replacing/removing it would split the lock.
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_name(path.name + ".lock").open("a") as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise SelectionError(f"另一个操作正在修改 {path}；本次未写入，操作结束后重试。") from exc
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def save_config(path, value, expected):
    current = path.read_bytes() if path.exists() else None
    if current != expected:
        raise SelectionError(f"配置在读取后发生变化：{path}；本次未覆盖，请重新读取再选择。")
    payload = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    fd, temporary = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            os.fchmod(stream.fileno(), mode)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    reread, _ = read_json(path)
    if reread != value:
        raise SelectionError(f"保存后回读不一致：{path}；文件可能已被其他写入者修改，请核对当前文件。")
    return reread


def change(catalog, paths, scope, component, variant=None, clear=False):
    if scope in ("default", "public-default"):
        raise SelectionError("公开默认由模板目录维护：修改目录的 default_variant，再按该仓发布流程同步；本工具未修改本地覆盖或网站。")
    choice = {"schema_version": 1, "components": {}}
    if not clear:
        choice["components"][component] = {"variant": variant, "catalog_sha256": catalog["content_sha256"]}
    # Clearing may repair a reference whose role was removed from the catalog.
    resolved_component = component if any(row["id"] == component for row in catalog["components"]) else None
    if not clear:
        resolve(catalog, {"task": choice}, component)
    if scope == "task":
        if paths.get("task"):
            existing, _ = read_json(paths["task"])
            validate_config(existing, paths["task"])
            if clear:
                existing["components"].pop(component, None)
            else:
                existing["components"][component] = choice["components"][component]
            choice = existing
            resolve(catalog, {"task": choice})
        return {"status": "task_selection", "selection": choice, "persisted": False,
                "catalog_sha256": catalog["content_sha256"], "ui_verified": False}
    if not paths.get(scope):
        raise SelectionError(f"{scope} 范围需要显式 --{scope} 配置路径；本次未写入。")
    path = Path(paths[scope]).expanduser().resolve()
    with config_lock(path):
        config, raw = read_json(path, missing=True)
        validate_config(config, path)
        if clear:
            config["components"].pop(component, None)
        else:
            config["components"][component] = choice["components"][component]
        layers = load_layers({key: value for key, value in paths.items() if key != scope})
        layers[scope] = config
        result = resolve(catalog, layers, resolved_component)
        save_config(path, config, raw)
        # Re-read through the same resolver path consumers use.
        result = resolve(catalog, load_layers(paths), resolved_component)
        result.update(status="cleared" if clear else "saved", path=str(path), scope=scope)
        return result


def parser():
    root = argparse.ArgumentParser(description="读取组件实际选择，或保存明确范围的覆盖；不修改页面、不直接发布网站。")
    commands = root.add_subparsers(dest="command", required=True)
    for command in ("validate", "resolve", "readback", "select", "clear"):
        sub = commands.add_parser(command)
        sub.add_argument("--catalog", required=True, type=Path, help="已下载的完整组件目录 JSON")
        sub.add_argument("--project", type=Path, help="项目配置的实际路径")
        sub.add_argument("--user", type=Path, help="使用者本地覆盖的实际路径；不会上传")
        sub.add_argument("--task", type=Path, help="本次选择 JSON；只读，不改长期设置")
        sub.add_argument("--component", required=command in ("select", "clear"))
        sub.add_argument("--json", action="store_true", help="输出机器可读 JSON")
        if command in ("select", "clear"):
            sub.add_argument("--scope", required=True, choices=("task", "project", "user", "default", "public-default"))
        if command == "select":
            sub.add_argument("--variant", required=True)
    return root


def display(result):
    status = result["status"]
    if status == "task_selection":
        print("已准备本次选择；未保存长期配置，也未修改页面。")
        print(json.dumps(result["selection"], ensure_ascii=False, indent=2))
        return
    if status in ("saved", "cleared"):
        print(f"组件覆盖已{'保存' if status == 'saved' else '取消'}并回读：{result['path']}")
    else:
        print("组件配置已读取；以下是本次输入下的有效选择，页面尚未验证。")
    names = {"task": "本次选择", "project": "项目明确选择", "user": "使用者本地覆盖", "public_default": "公开默认"}
    for row in result["components"]:
        print(f"- {row['name']}：{row['variant_name']}（来源：{names[row['source']]}）")
        if row["selection_catalog_changed"]:
            print("  目录自上次选择后已变化；应用前重新核对该变体规则与页面。")
    if status in ("saved", "cleared"):
        print("仅配置已更新；由 agent 应用到目标页面并实际操作验收，才算样式应用完成。")


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        catalog = load_catalog(args.catalog)
        paths = {scope: getattr(args, scope) for scope in ("task", "project", "user")}
        if args.command in ("select", "clear"):
            result = change(catalog, paths, args.scope, args.component,
                            getattr(args, "variant", None), args.command == "clear")
        else:
            result = resolve(catalog, load_layers(paths), args.component)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            display(result)
        return 0
    except (SelectionError, OSError) as exc:
        message = str(exc) if isinstance(exc, SelectionError) else f"本地文件操作失败（{exc.strerror}）；请核对目标路径和权限。"
        if args.json:
            print(json.dumps({"status": "error", "error": message, "ui_verified": False}, ensure_ascii=False))
        else:
            print("组件选择未完成：" + message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
