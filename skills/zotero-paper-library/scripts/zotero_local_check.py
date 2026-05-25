#!/usr/bin/env python3
"""Report local Zotero visibility without modifying the library."""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


def path_info(path: Path) -> dict:
    return {
        "path": str(path),
        "exists": path.exists(),
        "is_dir": path.is_dir(),
        "is_file": path.is_file(),
    }


def check_local_api() -> dict:
    url = "http://127.0.0.1:23119/api/users/0/items?limit=1"
    try:
        with urlopen(url, timeout=2) as response:
            body = response.read(200)
            return {
                "url": url,
                "ok": 200 <= response.status < 300,
                "status": response.status,
                "sample_bytes": len(body),
            }
    except URLError as exc:
        return {"url": url, "ok": False, "error": str(exc)}
    except Exception as exc:
        return {"url": url, "ok": False, "error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    home = Path.home()
    candidates = [
        home / "Zotero",
        home / "Library" / "Application Support" / "Zotero",
        Path(os.environ.get("ZOTERO_DATA_DIR", "")) if os.environ.get("ZOTERO_DATA_DIR") else None,
    ]
    data = {
        "zotero_paths": [path_info(path) for path in candidates if path is not None],
        "local_api": check_local_api(),
        "note": "Read-only diagnostic. This script does not edit Zotero files or databases.",
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
