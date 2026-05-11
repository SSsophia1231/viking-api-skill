#!/usr/bin/env python3
"""
Generate resources/meta.json and resources/version before each release.

Usage:
    python3 scripts/build_release.py 1.2.0
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RESOURCES_DIR = REPO_ROOT / "resources"
META_PATH = RESOURCES_DIR / "meta.json"
VERSION_PATH = RESOURCES_DIR / "version"

SKIP_FILES = {"meta.json", "version"}


def md5_of_file(path: Path) -> str:
    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 scripts/build_release.py <version>", file=sys.stderr)
        print("example: python3 scripts/build_release.py 1.2.0", file=sys.stderr)
        return 1

    version = sys.argv[1].strip()
    if not version:
        print("error: version cannot be empty", file=sys.stderr)
        return 1

    files = []
    for path in sorted(RESOURCES_DIR.rglob("*")):
        if not path.is_file():
            continue
        if path.name in SKIP_FILES:
            continue
        rel = path.relative_to(RESOURCES_DIR).as_posix()
        files.append({
            "path": rel,
            "size": path.stat().st_size,
            "md5": md5_of_file(path),
        })

    META_PATH.write_text(
        json.dumps({"version": version, "files": files}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    VERSION_PATH.write_text(version + "\n", encoding="utf-8")

    print(f"generated meta.json with {len(files)} files")
    print(f"version set to {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
