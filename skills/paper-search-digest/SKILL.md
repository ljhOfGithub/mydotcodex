---
name: paper-search-digest
description: Search computer science papers from arXiv, DBLP, OpenAlex, and similar public scholarly sources; download available PDFs; deduplicate repeated runs; deeply read papers; and write Chinese Markdown literature reports into a target reports directory. Use when the user provides keywords, fields, venues, authors, date ranges, or a research topic and asks Codex to find papers, download papers, summarize papers, compare related work, prepare a discussion note, create a beginner-friendly deep-reading explanation, prepare a presentation-style paper walkthrough, or answer introduction/background/system/experiment/evaluation/discussion questions.
---

# Paper Search Digest

Use this skill to turn a user-provided CS research topic into a reproducible, deduplicated Markdown report with up to ten newly selected papers per run. It also supports single-paper deep-reading reports that explain a paper like a lecture for beginners.

## Workflow

1. Clarify only missing essentials: topic/keywords, field, optional date range, and target report directory. If unspecified, default the report directory to `/Users/jackie/Documents/Git/Codex_Automated_Paper_Reader/paper-daily/reports`.
2. Run `scripts/search_papers.py` to query public sources, deduplicate against prior runs, download available PDFs, and write a candidate JSON file.
3. Inspect the JSON. If there are fewer than ten new papers, report the real count; do not pad with old or irrelevant papers.
4. Deep-read each selected paper. Prefer PDF text extraction when a PDF was downloaded; otherwise use abstract, DOI/publisher page, arXiv page, DBLP metadata, and official project/code pages.
5. Choose the report type:
   - For multi-paper search, digest, related-work, or ranking requests, read `references/report-framework.md`.
   - For single-paper deep reading, beginner explanation, figure/table walkthrough, or presentation requests, read `references/deep-reading-template.md`.
6. Write one Markdown report into the reports directory. Use a filename that includes the date and a short topic slug, for example `2026-05-24-edge-iot-paper-digest.md`.
7. Update nothing else unless the user asked for it. Keep downloaded PDFs and JSON sidecars under the reports directory's `_paper_search_digest/` subfolder.

## Search Command

Run from any working directory:

```bash
python3 /Users/jackie/.codex/skills/paper-search-digest/scripts/search_papers.py \
  --query "edge computing IoT LLM scheduling" \
  --field "computer science systems" \
  --limit 10 \
  --reports-dir /Users/jackie/Documents/Git/Codex_Automated_Paper_Reader/paper-daily/reports
```

Useful options:

- `--from-year 2022` and `--to-year 2026` constrain publication years.
- `--source arxiv --source dblp --source openalex` chooses sources; default is all three.
- `--no-download` skips PDF downloads when the user only wants metadata.
- `--include-seen` allows previously seen papers; normally leave it off for repeated runs.

The script prints the JSON path and PDF directory. Read the JSON before writing the report.

## Deduplication Rules

Use the script's `dedupe_key` and `seen_before` fields as the first line of defense. It stores a persistent index at:

```text
<reports-dir>/_paper_search_digest/seen_papers.json
```

Treat a paper as duplicate if any of these match an existing item:

- DOI
- arXiv ID
- normalized title

If the user asks for exactly ten papers but fewer than ten new papers are found, write the truthful count and explain that deduplication reduced the batch.

## Reading and Reporting Standards

Do not rely only on title keywords. For each selected paper, identify:

- the actual problem and boundary conditions
- the key observation or insight
- the design choice and why it differs from prior work
- experiment setup, baselines, metrics, and main limitations
- trade-offs and deployment or ethics risks when relevant

For arXiv papers, prefer the PDF. For DBLP-only hits, use linked DOI/publisher pages or search the exact title on arXiv/OpenAlex/Semantic Scholar before concluding that a PDF is unavailable.

## Beginner-Friendly Language Standards

Write reports for a smart beginner unless the user asks for a specialist-only version.

- Explain every retained English term in a glossary before using it heavily.
- On first use, write `中文译名（English term）`; later prefer the Chinese term.
- Do not leave jargon as bare English when a plain Chinese explanation is needed.
- Do not use `instrument` as an untranslated Chinese verb.
- Prefer explicit action-level explanations, for example: `传统快照算法默认所有相关进程都能接入快照协议：它们可以在收发消息时携带快照标记，并在合适时刻记录本地状态`.
- For terms such as `instrument/instrumentation`, `baseline`, `benchmark`, `marker`, `piggyback`, `workload`, and `trace`, explain what the term means in this paper, what action it performs, and what readers may misunderstand.
- Mark uncertain details as `未在论文或元数据中确认`; do not fill gaps with generic textbook claims.

## Output Contract

For multi-paper digests, the Markdown report must include:

- search metadata: query, field, sources, run date, report path, and number of new papers
- a table of selected papers with title, year, venue/source, links, PDF path if available, and duplicate status
- one subsection per paper answering the framework questions in concise Chinese
- a cross-paper synthesis: recurring assumptions, strongest ideas, weak evidence, and best follow-up reads
- the fixed Chinese answer template filled in when enough evidence exists; otherwise mark unknowns explicitly
- a 2-minute elevator pitch draft: "问题 -> 洞察 -> 设计选择 -> 代价"

For single-paper deep-reading reports, follow `references/deep-reading-template.md`. Include useful figure/table screenshots when available, store them under `<report-stem>_assets/`, and reference them with relative Markdown image links.

Do not invent missing details. Mark unavailable evidence as `未在论文或元数据中确认`.
