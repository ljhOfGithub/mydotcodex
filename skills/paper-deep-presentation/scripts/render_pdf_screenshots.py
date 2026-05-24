#!/usr/bin/env python3
"""Render PDF pages or regions to PNG screenshots for paper reports."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_pages(spec: str) -> list[int]:
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start > end:
                raise ValueError(f"Invalid page range: {part}")
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    return sorted(pages)


def safe_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    return value.strip("-") or "screenshot"


def parse_region(spec: str) -> tuple[str, int, tuple[float, float, float, float]]:
    parts = [p.strip() for p in spec.split(",")]
    if len(parts) != 6:
        raise ValueError("Region must be name,page,x0,y0,x1,y1")
    name = safe_name(parts[0])
    page = int(parts[1])
    coords = tuple(float(x) for x in parts[2:6])
    x0, y0, x1, y1 = coords
    if x0 >= x1 or y0 >= y1:
        raise ValueError(f"Invalid region coordinates: {spec}")
    return name, page, coords


def render() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, help="Input PDF path")
    parser.add_argument("--out-dir", required=True, help="Output assets directory")
    parser.add_argument("--pages", default="", help='Pages to render, e.g. "1,4,8-10"')
    parser.add_argument("--region", action="append", default=[], help="Crop region: name,page,x0,y0,x1,y1")
    parser.add_argument("--slug", default="paper", help="Filename prefix for full-page renders")
    parser.add_argument("--dpi", type=int, default=180, help="Render DPI")
    args = parser.parse_args()

    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("PyMuPDF is required: install/use an environment with package 'fitz'", file=sys.stderr)
        return 2

    pdf = Path(args.pdf).expanduser().resolve()
    if not pdf.exists():
        print(f"PDF not found: {pdf}", file=sys.stderr)
        return 2

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf)
    scale = args.dpi / 72.0
    matrix = fitz.Matrix(scale, scale)
    outputs: list[Path] = []

    for page_no in parse_pages(args.pages) if args.pages else []:
        if page_no < 1 or page_no > len(doc):
            raise ValueError(f"Page out of range: {page_no}; PDF has {len(doc)} pages")
        page = doc[page_no - 1]
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        path = out_dir / f"{safe_name(args.slug)}-page-{page_no:03d}.png"
        pix.save(path)
        outputs.append(path)

    for region_spec in args.region:
        name, page_no, coords = parse_region(region_spec)
        if page_no < 1 or page_no > len(doc):
            raise ValueError(f"Page out of range: {page_no}; PDF has {len(doc)} pages")
        page = doc[page_no - 1]
        clip = fitz.Rect(*coords)
        pix = page.get_pixmap(matrix=matrix, clip=clip, alpha=False)
        path = out_dir / f"{name}.png"
        pix.save(path)
        outputs.append(path)

    for path in outputs:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(render())
