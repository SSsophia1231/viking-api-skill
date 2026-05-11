import argparse
import base64
import datetime as _dt
import hashlib
import hmac
import json
import os
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests


def _now_iso() -> str:
    return _dt.datetime.now(tz=_dt.timezone.utc).isoformat()


def _safe_segment(name: str) -> str:
    s = (name or "").strip()
    if not s:
        return "_"
    replacements = {
        "/": "／",
        "\\": "＼",
        ":": "：",
        "*": "＊",
        "?": "？",
        "\"": "＂",
        "<": "＜",
        ">": "＞",
        "|": "｜",
        "\0": "",
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    s = s.rstrip(". ")
    if not s:
        return "_"
    return s


def _posix_join(base: PurePosixPath, seg: str) -> PurePosixPath:
    return base / seg


def _md5_hex(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


class ArcositeClient:
    """
    https://arcosite-openapi.bytedance.net/swagger/html
    """
    def __init__(self, *, url: str, ak: str, sk: str, business_id: str, app_id: str) -> None:
        self.url = url
        self.ak = ak
        self.sk = sk
        self.business_id = business_id
        self.app_id = app_id

    def call(self, action: str, data: Dict[str, Any]) -> requests.Response:
        payload = dict(data)
        payload["business_id"] = self.business_id
        payload["app_id"] = self.app_id
        headers = self._gen_headers(self.ak, self.sk, action, payload)
        ret = requests.post(self.url, json=payload, headers=headers, timeout=60)
        ret.raise_for_status()
        return ret

    def get_bus_structure(self, *, lang: str) -> Any:
        return self.call("GetBusStructureById", {"lang": lang, "req_source": "admin"}).json()

    def get_doc(self, *, doc_id: str, content_type: str) -> Any:
        data = self.call("GetDocById", {"id": doc_id}).json()
        data = data["Result"]
        data["content"] = self._dsl_to_md(data["content"], content_type)["Result"]
        return data

    def save_doc(self, *, doc_id: str, title: str, content: str, content_type: str) -> Any:
        mapping = {
            "markdown-it": "vs-op",
            "common": "common",
        }
        return self.call("SaveDoc", {"id": doc_id, "title": title, "content": content, "content_type": mapping[content_type]}).json()

    def _dsl_to_md(self, content: str, content_type: str):
        return self.call("ConvertMd", {"content": content, "type": content_type}).json()

    def _md_to_dsl(self, content: str):
        return self.call("ConvertDoc", {"content": content, "type": "vs-op"}).json()

    @classmethod
    def _sign(cls, headers: Dict[str, Any], sk: str) -> str:
        data_new = "POST\n"
        data_new += "/api/arcosite\n"
        for key, value in sorted(headers.items()):
            if key.startswith("x-arcosite") and value:
                data_new += key.lower() + ":" + str(value) + "\n"
        hashing = hmac.new(sk.encode("utf-8"), data_new.strip("\n").encode("utf-8"), hashlib.sha1)
        return base64.b64encode(hashing.digest()).decode()

    @classmethod
    def _gen_headers(cls, ak: str, sk: str, action: str, data: Dict[str, Any]) -> Dict[str, str]:
        headers: Dict[str, str] = {"Content-Type": "application/json;charset=utf-8", "x-arcosite-action": action}
        payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        headers["x-arcosite-content"] = _md5_hex(payload)
        headers["authorization"] = "Arcosite " + ak + ":" + cls._sign(headers, sk)
        return headers


def _extract_result_list(bus_json: Any) -> List[Dict[str, Any]]:
    if isinstance(bus_json, dict):
        for k in ("Result", "result", "Data", "data"):
            v = bus_json.get(k)
            if isinstance(v, list):
                return v
        if "result" in bus_json and isinstance(bus_json["result"], dict):
            v = bus_json["result"].get("Result") or bus_json["result"].get("result")
            if isinstance(v, list):
                return v
    if isinstance(bus_json, list):
        return bus_json
    raise ValueError("无法从 GetBusStructureById 响应中提取 Result 列表")


def _find_first_string_field(obj: Any, key_name: str) -> Optional[str]:
    queue: List[Any] = [obj]
    while queue:
        cur = queue.pop(0)
        if isinstance(cur, dict):
            if key_name in cur and isinstance(cur[key_name], str):
                return cur[key_name]
            for v in cur.values():
                if isinstance(v, (dict, list)):
                    queue.append(v)
        elif isinstance(cur, list):
            for v in cur:
                if isinstance(v, (dict, list)):
                    queue.append(v)
    return None


def _extract_doc_content(doc_json: Any) -> str:
    if isinstance(doc_json, dict):
        for k in ("Result", "result", "Data", "data"):
            v = doc_json.get(k)
            if isinstance(v, dict) and isinstance(v.get("content"), str):
                return v["content"]
        if isinstance(doc_json.get("content"), str):
            return doc_json["content"]
    content = _find_first_string_field(doc_json, "content")
    return content or ""


def _extract_doc_title(doc_json: Any) -> Optional[str]:
    if isinstance(doc_json, dict):
        for k in ("Result", "result", "Data", "data"):
            v = doc_json.get(k)
            if isinstance(v, dict) and isinstance(v.get("title"), str):
                return v["title"]
        if isinstance(doc_json.get("title"), str):
            return doc_json["title"]
    return _find_first_string_field(doc_json, "title")


def _walk_tree(
    nodes: Iterable[Dict[str, Any]],
    *,
    parent: PurePosixPath,
    mapping: Dict[str, Dict[str, Any]],
    id_to_path: Dict[str, str],
) -> List[Tuple[Dict[str, Any], PurePosixPath]]:
    leaves: List[Tuple[Dict[str, Any], PurePosixPath]] = []
    for node in nodes:
        title = str(node.get("title") or "")
        node_id = str(node.get("_id") or node.get("id") or "")
        is_dir = bool(node.get("is_dir"))

        seg = _safe_segment(title)
        rel = _posix_join(parent, seg)
        rel_key: str
        if is_dir:
            rel_key = str(rel)
        else:
            rel_key = str(rel.with_suffix(".md"))
            rel = PurePosixPath(rel_key)

        mapping[rel_key] = {
            "_id": node_id,
            "title": title,
            "is_dir": is_dir,
            "updated_at": node.get("updated_at"),
            "path": node.get("path"),
        }
        if node_id:
            id_to_path[node_id] = rel_key

        subs = node.get("subs") or []
        if isinstance(subs, list) and subs:
            if is_dir:
                leaves.extend(_walk_tree(subs, parent=rel, mapping=mapping, id_to_path=id_to_path))
            else:
                leaves.append((node, rel))
        else:
            if not is_dir:
                leaves.append((node, rel))
    return leaves


def _write_meta(meta_path: Path, meta: Dict[str, Any]) -> None:
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_meta(meta_path: Path) -> Dict[str, Any]:
    return json.loads(meta_path.read_text(encoding="utf-8"))


def download_all(
    *,
    client: ArcositeClient,
    out_dir: Path,
    lang: str,
    content_type: str,
    include_paths: Optional[List[str]] = None,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)

    bus_json = client.get_bus_structure(lang=lang)

    root_nodes = _extract_result_list(bus_json)
    mapping: Dict[str, Dict[str, Any]] = {}
    id_to_path: Dict[str, str] = {}
    leaves = _walk_tree(root_nodes, parent=PurePosixPath("."), mapping=mapping, id_to_path=id_to_path)

    for rel_str, info in mapping.items():
        if info.get("is_dir"):
            (out_dir / Path(rel_str)).mkdir(parents=True, exist_ok=True)

    include_prefixes = [_to_posix_path(p) for p in (include_paths or []) if (p or "").strip()]

    for node, rel in leaves:
        if include_prefixes and not any(_is_under(rel, p) for p in include_prefixes):
            continue
        node_id = str(node.get("_id") or node.get("id") or "")
        if not node_id:
            continue
        doc_json = client.get_doc(doc_id=node_id, content_type=content_type)
        title = _extract_doc_title(doc_json)
        if title and rel.as_posix() in mapping:
            mapping[rel.as_posix()]["remote_title"] = title

        abs_path = out_dir / Path(rel.as_posix())
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        abs_path.write_text(doc_json["content"], encoding="utf-8")
        mapping[rel.as_posix()]["content_md5"] = _md5_hex(doc_json["content"].encode("utf-8"))
        print(f"download {rel.as_posix()}")

    meta_path = out_dir / ".arcosite_meta.json"
    meta = {
        "format": "arcosite.v1",
        "downloaded_at": _now_iso(),
        "url": client.url,
        "business_id": client.business_id,
        "app_id": client.app_id,
        "lang": lang,
        "path_to_node": mapping,
        "id_to_path": id_to_path,
        "content_type": content_type,
    }
    _write_meta(meta_path, meta)
    return meta_path


def _iter_local_markdown_files(root_dir: Path) -> Iterable[Path]:
    for p in root_dir.rglob("*.md"):
        rel_parts = p.relative_to(root_dir).parts
        if any(part.startswith(".") for part in rel_parts):
            continue
        yield p


def _is_under(path: PurePosixPath, prefix: PurePosixPath) -> bool:
    prefix_parts = prefix.parts
    if not prefix_parts or prefix_parts == (".",):
        return True
    return path.parts[: len(prefix_parts)] == prefix_parts


def _to_posix_path(s: str) -> PurePosixPath:
    return PurePosixPath((s or "").lstrip("./"))


def upload_all(
    *,
    client: ArcositeClient,
    root_dir: Path,
    lang: str,
    content_type: Optional[str] = None,
    dry_run: bool = False,
    force: bool = False,
    strict: bool = False,
    include_paths: Optional[List[str]] = None,
    exclude_paths: Optional[List[str]] = None,
) -> None:
    meta_path = root_dir / ".arcosite_meta.json"
    meta = _load_meta(meta_path)
    mapping: Dict[str, Dict[str, Any]] = meta.get("path_to_node") or {}

    include_prefixes = [_to_posix_path(p) for p in (include_paths or []) if (p or "").strip()]
    exclude_prefixes = [_to_posix_path(p) for p in (exclude_paths or []) if (p or "").strip()]

    for abs_path in _iter_local_markdown_files(root_dir):
        rel = abs_path.relative_to(root_dir).as_posix()
        rel_posix = PurePosixPath(rel)

        if include_prefixes and not any(_is_under(rel_posix, p) for p in include_prefixes):
            continue
        if exclude_prefixes and any(_is_under(rel_posix, p) for p in exclude_prefixes):
            continue

        info = mapping.get(rel)
        if not info or info.get("is_dir"):
            msg = f"跳过: 未在元信息中找到 _id: {rel}"
            if strict:
                raise ValueError(msg)
            print(msg)
            continue

        doc_id = str(info.get("_id") or "")
        if not doc_id:
            msg = f"跳过: 元信息缺少 _id: {rel}"
            if strict:
                raise ValueError(msg)
            print(msg)
            continue

        content = abs_path.read_text(encoding="utf-8")
        content_md5 = _md5_hex(content.encode("utf-8"))
        if not force and info.get("content_md5") == content_md5:
            continue

        title = abs_path.stem
        if dry_run:
            print(f"dry-run: SaveDoc id={doc_id} path={rel} format={content_type}")
            continue

        client.save_doc(doc_id=doc_id, title=title, content=content, content_type=content_type)
        info["content_md5"] = content_md5
        print(f"upload {rel}")

    meta["uploaded_at"] = _now_iso()
    meta["lang"] = lang
    meta["content_format"] = content_type
    _write_meta(meta_path, meta)


def _build_client_from_env(url: str, business_id: str, app_id: str) -> ArcositeClient:
    ak = os.environ.get("Arcosite_AK") or ""
    sk = os.environ.get("Arcosite_SK") or ""
    if not ak or not sk:
        raise ValueError("请设置环境变量 Arcosite_AK 与 Arcosite_SK")
    return ArcositeClient(url=url, ak=ak, sk=sk, business_id=business_id, app_id=app_id)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://arcosite-openapi.bytedance.net/api/arcosite")
    parser.add_argument("--business-id", default="661759fdfb491202fff58f9d")
    parser.add_argument("--app-id", default="1712806259465")
    parser.add_argument("--lang", default="zh")

    sub = parser.add_subparsers(dest="cmd", required=True)

    dl = sub.add_parser("download")
    dl.add_argument("--out-dir", default=str(Path(__file__).resolve().parent / "docs"))
    dl.add_argument("--format",   default="markdown-it", choices=["common", "markdown-it"], help="文档格式：common 标准markdown；markdown-it 火山markdown")
    dl.add_argument(
        "--include-path",
        action="append",
        default=[],
        help="限制下载范围：远端文档树的路径前缀，可重复指定；不传则下载全部",
    )

    ul = sub.add_parser("upload")
    ul.add_argument("--root-dir", default=str(Path(__file__).resolve().parent / "docs"))
    ul.add_argument("--format", default="markdown-it", choices=["common", "markdown-it"], help="文档格式：common 标准markdown；markdown-it 火山markdown")
    ul.add_argument("--dry-run", action="store_true")
    ul.add_argument("--force", action="store_true")
    ul.add_argument("--strict", action="store_true")
    ul.add_argument(
        "--include-path",
        action="append",
        default=[],
        help="限制上传范围：相对 root-dir 的文件/目录前缀，可重复指定；不传则上传全部",
    )
    ul.add_argument(
        "--exclude-path",
        action="append",
        default=[],
        help="排除上传范围：相对 root-dir 的文件/目录前缀，可重复指定",
    )

    args = parser.parse_args(argv)

    client = _build_client_from_env(args.url, args.business_id, args.app_id)

    if args.cmd == "download":
        out_dir = Path(args.out_dir).expanduser().resolve()
        meta_path = download_all(client=client, out_dir=out_dir, lang=args.lang, content_type=args.format, include_paths=list(args.include_path or []))
        print(f"已下载到: {out_dir}")
        print(f"元信息: {meta_path}")
        return 0

    if args.cmd == "upload":
        root_dir = Path(args.root_dir).expanduser().resolve()
        upload_all(
            client=client,
            root_dir=root_dir,
            lang=args.lang,
            content_type=args.format,
            dry_run=bool(args.dry_run),
            force=bool(args.force),
            strict=bool(args.strict),
            include_paths=list(args.include_path or []),
            exclude_paths=list(args.exclude_path or []),
        )
        print("上传完成")
        return 0

    raise ValueError(f"未知命令: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
