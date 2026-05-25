#!/usr/bin/env python3
"""Build a reviewable JSONL manifest for Zotero paper imports."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ARXIV_RE = re.compile(r"(?<!\d)(\d{4}\.\d{4,5})(?:v\d+)?(?!\d)")
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
SUPPORTED_SUFFIXES = {".pdf", ".md", ".bib", ".ris", ".json", ".jsonl", ".txt"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_sample(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return path.name
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:20000]
    except Exception:
        return path.name


def title_guess(path: Path, sample: str) -> str:
    if path.suffix.lower() == ".md":
        for line in sample.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip()
    stem = re.sub(r"[_-]+", " ", path.stem)
    stem = ARXIV_RE.sub("", stem)
    return re.sub(r"\s+", " ", stem).strip()


def inspect_file(path: Path) -> dict:
    sample = read_sample(path)
    stat = path.stat()
    arxiv = ARXIV_RE.search(str(path)) or ARXIV_RE.search(sample)
    doi = DOI_RE.search(sample)
    return {
        "path": str(path.resolve()),
        "type": path.suffix.lower().lstrip(".") or "unknown",
        "title_guess": title_guess(path, sample),
        "doi": doi.group(0) if doi else None,
        "arxiv_id": arxiv.group(1) if arxiv else None,
        "sha256": sha256(path),
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "zotero_status": "pending-review",
    }


def collect_paths(paths: list[Path], roots: list[Path]) -> list[Path]:
    found = []
    for path in paths:
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            found.append(path)
    for root in roots:
        if root.is_file() and root.suffix.lower() in SUPPORTED_SUFFIXES:
            found.append(root)
        elif root.is_dir():
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
                    found.append(path)
    return sorted(set(found), key=lambda p: str(p.resolve()))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", action="append", default=[], help="Specific artifact file to include.")
    parser.add_argument("--root", action="append", default=[], help="Directory or file tree to scan.")
    parser.add_argument("--out", help="Optional JSONL output path. Defaults to stdout.")
    args = parser.parse_args()

    files = collect_paths([Path(p).expanduser() for p in args.path], [Path(p).expanduser() for p in args.root])
    records = [inspect_file(path) for path in files]

    lines = [json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records]
    output = "\n".join(lines)
    if output:
        output += "\n"

    if args.out:
        out_path = Path(args.out).expanduser()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"Wrote {len(records)} records to {out_path}")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
