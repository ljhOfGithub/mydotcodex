---
name: research-paper-search-report
description: Search research-oriented computer science papers from arXiv, DBLP, OpenAlex, and similar scholarly sources; download available PDFs; deduplicate repeated runs; and write Chinese Markdown research discussion reports for ten papers using a fixed Introduction/Background/System/Experiment/Evaluation/Discussion question framework. Use when the user provides keywords, fields, venues, authors, or date ranges and wants a downloadable paper batch plus a detailed research-reading report under the paper-daily reports folder.
---

# Research Paper Search Report

Use this skill when the user gives keywords, a research field, venues, authors, or a date range and wants Codex to search CS research papers, download PDFs, deduplicate repeated runs, and write a Chinese Markdown report for research discussion.

Default output root:

```text
/Users/jackie/Documents/Git/Codex_Automated_Paper_Reader/paper-daily/reports
```

Default target: ten newly found, relevant papers. If fewer than ten new papers remain after deduplication and relevance filtering, report the true count; do not pad with old or weakly related papers.

## Workflow

1. Confirm only missing essentials: keywords/topic, field, optional date range, and whether the user wants one combined report or one report per keyword group. If unspecified, write one report per keyword group.
2. Read `references/report-framework.md` and apply `$paper-communication-layers` before writing the report.
3. Search with the existing local search script:

```bash
python3 /Users/jackie/.codex/skills/paper-search-digest/scripts/search_papers.py \
  --query "<keywords>" \
  --field "<field>" \
  --limit 10 \
  --reports-dir /Users/jackie/Documents/Git/Codex_Automated_Paper_Reader/paper-daily/reports
```

Useful options:

- `--from-year 2022` and `--to-year 2026` constrain publication years.
- `--source arxiv --source dblp --source openalex` chooses sources; default is all three.
- `--no-download` preserves metadata JSON if PDF download is unstable.
- Do not use `--include-seen` unless the user explicitly wants previously seen papers.
- If the proxy or network is unstable, keep the same search/download attempt alive and retry transient transport errors until success or until the failure is clearly non-transient. Do not convert proxy flaps into “empty result” conclusions.

4. Always inspect the candidate JSON printed by the script before writing. Do not treat command success as the final result.
5. Use `_paper_search_digest/seen_papers.json` under the reports directory as the persistent dedup state. Treat DOI, arXiv ID, and normalized title matches as duplicates.
6. If the default download path fails with `IncompleteRead`, source 500/503, proxy refusal, transient DNS, timeout, `Operation not permitted`, or another transient PDF/network error, retry until success first. Only rerun with `--no-download` after confirming the blocking failure is not transient or the user explicitly wants a metadata-only fallback.
7. Rank candidates by verified relevance, source quality, evidence availability, and recency when relevant. Never select or score a paper highly only because it matched the keyword.
8. For every selected paper, read enough evidence before writing:
   - Prefer full PDF text.
   - At minimum inspect abstract, introduction, method/system design, experiments/evaluation, and conclusion when available.
   - If only metadata or abstract is available, mark `abstract-only` or `未在论文或元数据中确认` and avoid unsupported claims.
9. If a selected paper has no PDF, try authoritative sources in this order: arXiv PDF, OpenAlex open-access PDF, DOI/publisher page, exact title search on scholarly sources, and user Chrome session for logged-in publisher access when needed. Verify downloaded files with `file`; do not pass HTML/login/access-denied pages as PDFs.
10. Write a non-overwriting Markdown report in the reports directory. Use names like `YYYY-MM-DD-HHMMSS-topic-research-paper-report.md`. If the user gives multiple keyword groups, write one independent Markdown file per group.

## Report Contract

Each Markdown report must include:

- search metadata: query, field, sources, run date, output path, and number of new selected papers
- candidate JSON path, PDF directory, and dedup state path
- selected-paper table: title, year, venue/source, source URL, local PDF path, duplicate status, evidence level, and relevance note
- skipped-paper notes with reasons: duplicate, off-topic, weak evidence, explicit count limit, or download/source failure
- one detailed section per selected paper using `references/report-framework.md`
- the fixed answer template for each paper when evidence supports it
- a one-sentence version and a 2-minute version for each paper, following `$paper-communication-layers`; keep longer presentation layers optional so the batch report remains readable
- cross-paper synthesis: recurring assumptions, shared limitations, strongest research opportunities, and one or two follow-up references worth reading
- failure and limitation log: network/API/PDF download issues, missing full text, `abstract-only` papers, and claims marked `未在论文或元数据中确认`

## Evidence Rules

- Default Chinese output.
- Fact first; do not invent missing paper details.
- Mark unsupported items as `未在论文或元数据中确认`.
- Mark abstract-only analysis as `abstract-only`.
- Do not reuse old papers to satisfy a requested count.
- Do not overwrite previous reports, JSON files, PDFs, or sidecar files.
- Do not delete reports, PDFs, JSON sidecars, or dedup files.
- Do not leak credentials, tokens, cookies, or publisher session data.

## Final Reply Contract

After the run, reply with:

- report path for each keyword group
- candidate JSON path
- PDF directory
- selected paper titles and count
- skipped/duplicate count
- any source, network, PDF, or evidence limitations
