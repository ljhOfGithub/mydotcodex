#!/usr/bin/env python3
"""Search CS papers, deduplicate repeated runs, and download available PDFs."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


USER_AGENT = "paper-search-digest/1.0 (mailto:none)"
ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
DEFAULT_SOURCES = ("arxiv", "dblp", "openalex")


def slugify(text: str, max_len: int = 64) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return (slug or "paper-search")[:max_len].strip("-")


def normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", title.lower())).strip()


def request_text(url: str, *, accept: str = "application/json", timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def request_bytes(url: str, *, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def year_ok(year: int | None, from_year: int | None, to_year: int | None) -> bool:
    if year is None:
        return True
    if from_year is not None and year < from_year:
        return False
    if to_year is not None and year > to_year:
        return False
    return True


def arxiv_search(query: str, limit: int, from_year: int | None, to_year: int | None) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max(limit, 10),
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
    )
    xml_text = request_text(f"https://export.arxiv.org/api/query?{params}", accept="application/atom+xml")
    root = ET.fromstring(xml_text)
    papers: list[dict[str, Any]] = []
    for entry in root.findall("atom:entry", ARXIV_NS):
        title = " ".join((entry.findtext("atom:title", default="", namespaces=ARXIV_NS)).split())
        summary = " ".join((entry.findtext("atom:summary", default="", namespaces=ARXIV_NS)).split())
        published = entry.findtext("atom:published", default="", namespaces=ARXIV_NS)
        year = int(published[:4]) if published[:4].isdigit() else None
        if not year_ok(year, from_year, to_year):
            continue
        page_url = entry.findtext("atom:id", default="", namespaces=ARXIV_NS)
        arxiv_id = page_url.rsplit("/", 1)[-1] if page_url else None
        pdf_url = None
        for link in entry.findall("atom:link", ARXIV_NS):
            if link.attrib.get("title") == "pdf" or link.attrib.get("type") == "application/pdf":
                pdf_url = link.attrib.get("href")
        papers.append(
            {
                "source": "arxiv",
                "title": title,
                "authors": [a.findtext("atom:name", default="", namespaces=ARXIV_NS) for a in entry.findall("atom:author", ARXIV_NS)],
                "year": year,
                "venue": "arXiv",
                "abstract": summary,
                "url": page_url,
                "pdf_url": pdf_url,
                "doi": None,
                "arxiv_id": arxiv_id,
            }
        )
    return papers


def dblp_search(query: str, limit: int, from_year: int | None, to_year: int | None) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"q": query, "format": "json", "h": max(limit, 10)})
    data = json.loads(request_text(f"https://dblp.org/search/publ/api?{params}"))
    hits = as_list(data.get("result", {}).get("hits", {}).get("hit"))
    papers: list[dict[str, Any]] = []
    for hit in hits:
        info = hit.get("info", {})
        try:
            year = int(info.get("year")) if info.get("year") else None
        except (TypeError, ValueError):
            year = None
        if not year_ok(year, from_year, to_year):
            continue
        authors = []
        for item in as_list(info.get("authors", {}).get("author")):
            authors.append(item.get("text", item) if isinstance(item, dict) else str(item))
        papers.append(
            {
                "source": "dblp",
                "title": info.get("title", ""),
                "authors": authors,
                "year": year,
                "venue": info.get("venue"),
                "abstract": None,
                "url": info.get("url"),
                "pdf_url": None,
                "doi": info.get("doi"),
                "arxiv_id": None,
            }
        )
    return papers


def openalex_search(query: str, limit: int, from_year: int | None, to_year: int | None) -> list[dict[str, Any]]:
    filters = []
    if from_year is not None:
        filters.append(f"from_publication_date:{from_year}-01-01")
    if to_year is not None:
        filters.append(f"to_publication_date:{to_year}-12-31")
    params = {
        "search": query,
        "per-page": str(max(limit, 10)),
        "sort": "relevance_score:desc",
    }
    if filters:
        params["filter"] = ",".join(filters)
    url = f"https://api.openalex.org/works?{urllib.parse.urlencode(params)}"
    data = json.loads(request_text(url))
    papers: list[dict[str, Any]] = []
    for work in data.get("results", []):
        year = work.get("publication_year")
        if not year_ok(year, from_year, to_year):
            continue
        authors = [
            a.get("author", {}).get("display_name", "")
            for a in work.get("authorships", [])
            if a.get("author", {}).get("display_name")
        ]
        primary = work.get("primary_location") or {}
        source = primary.get("source") or {}
        best_oa = work.get("best_oa_location") or {}
        pdf_url = best_oa.get("pdf_url") or primary.get("pdf_url")
        papers.append(
            {
                "source": "openalex",
                "title": work.get("title", ""),
                "authors": authors,
                "year": year,
                "venue": source.get("display_name"),
                "abstract": None,
                "url": work.get("doi") or work.get("id"),
                "pdf_url": pdf_url,
                "doi": (work.get("doi") or "").replace("https://doi.org/", "") or None,
                "arxiv_id": None,
            }
        )
    return papers


def paper_key(paper: dict[str, Any]) -> str:
    if paper.get("doi"):
        return "doi:" + str(paper["doi"]).lower()
    if paper.get("arxiv_id"):
        return "arxiv:" + str(paper["arxiv_id"]).lower()
    return "title:" + normalize_title(paper.get("title", ""))


def merge_papers(papers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for paper in papers:
        title = paper.get("title") or ""
        if not title.strip():
            continue
        key = paper_key(paper)
        if key not in merged:
            paper["sources"] = [paper.pop("source")]
            merged[key] = paper
            continue
        existing = merged[key]
        existing["sources"].append(paper.get("source"))
        for field in ("abstract", "pdf_url", "doi", "arxiv_id", "venue", "url"):
            if not existing.get(field) and paper.get(field):
                existing[field] = paper[field]
    return list(merged.values())


def load_seen(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"papers": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_seen(path: Path, seen: dict[str, Any]) -> None:
    path.write_text(json.dumps(seen, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def download_pdf(paper: dict[str, Any], pdf_dir: Path) -> str | None:
    pdf_url = paper.get("pdf_url")
    if not pdf_url:
        return None
    try:
        data = request_bytes(pdf_url)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        paper["pdf_error"] = str(exc)
        return None
    if not data.startswith(b"%PDF"):
        paper["pdf_error"] = "downloaded content is not a PDF"
        return None
    digest = hashlib.sha1((paper_key(paper) + pdf_url).encode("utf-8")).hexdigest()[:10]
    name = f"{slugify(paper.get('title', 'paper'), 80)}-{digest}.pdf"
    out = pdf_dir / name
    out.write_bytes(data)
    return str(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--field", default="")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--reports-dir", default="/Users/jackie/Documents/Git/Codex_Automated_Paper_Reader/paper-daily/reports")
    parser.add_argument("--from-year", type=int)
    parser.add_argument("--to-year", type=int)
    parser.add_argument("--source", action="append", choices=DEFAULT_SOURCES)
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--include-seen", action="store_true")
    args = parser.parse_args()

    sources = args.source or list(DEFAULT_SOURCES)
    reports_dir = Path(args.reports_dir).expanduser().resolve()
    state_dir = reports_dir / "_paper_search_digest"
    pdf_dir = state_dir / "pdfs"
    state_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    seen_path = state_dir / "seen_papers.json"
    seen = load_seen(seen_path)

    collected: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    fetchers = {"arxiv": arxiv_search, "dblp": dblp_search, "openalex": openalex_search}
    per_source_limit = max(args.limit * 3, 20)
    for source in sources:
        try:
            collected.extend(fetchers[source](args.query, per_source_limit, args.from_year, args.to_year))
            time.sleep(1)
        except Exception as exc:  # Keep partial results from other sources.
            errors.append({"source": source, "error": repr(exc)})

    candidates = merge_papers(collected)
    selected: list[dict[str, Any]] = []
    for paper in candidates:
        key = paper_key(paper)
        paper["dedupe_key"] = key
        paper["seen_before"] = key in seen.get("papers", {})
        if paper["seen_before"] and not args.include_seen:
            continue
        if not args.no_download:
            paper["pdf_path"] = download_pdf(paper, pdf_dir)
        selected.append(paper)
        seen.setdefault("papers", {})[key] = {
            "title": paper.get("title"),
            "first_seen": seen.get("papers", {}).get(key, {}).get("first_seen") or dt.datetime.now(dt.timezone.utc).isoformat(),
            "sources": paper.get("sources", []),
            "doi": paper.get("doi"),
            "arxiv_id": paper.get("arxiv_id"),
        }
        if len(selected) >= args.limit:
            break

    save_seen(seen_path, seen)
    run_stamp = dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    out_path = state_dir / f"{run_stamp}-{slugify(args.query, 48)}.json"
    payload = {
        "query": args.query,
        "field": args.field,
        "run_time": dt.datetime.now(dt.timezone.utc).isoformat(),
        "sources": sources,
        "limit": args.limit,
        "from_year": args.from_year,
        "to_year": args.to_year,
        "reports_dir": str(reports_dir),
        "pdf_dir": str(pdf_dir),
        "seen_index": str(seen_path),
        "errors": errors,
        "new_count": sum(1 for p in selected if not p.get("seen_before")),
        "papers": selected,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"json={out_path}")
    print(f"pdf_dir={pdf_dir}")
    print(f"selected={len(selected)} new={payload['new_count']} errors={len(errors)}")
    if errors:
        print(json.dumps(errors, ensure_ascii=False), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
