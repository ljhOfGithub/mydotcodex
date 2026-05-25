---
name: paper-search-digest
description: Search computer science papers from arXiv, DBLP, OpenAlex, and similar public scholarly sources; download available PDFs; deduplicate repeated runs; and by default orchestrate one deep presentation report for every newly found paper by invoking the paper-deep-presentation skill. Use when the user provides keywords, fields, venues, authors, date ranges, or a research topic and asks Codex to find papers, download papers, organize a paper batch, summarize search results, compare related work, or prepare deep per-paper reports.
---

# Paper Search Digest

Use this skill to turn a user-provided CS research topic into a reproducible, deduplicated paper batch. This skill is the search/download/orchestration layer. By default, every newly found paper that is not a duplicate or clearly off-topic must be processed by `/Users/jackie/.codex/skills/paper-deep-presentation/SKILL.md`; do not write rough per-paper explanations from this skill.

## Workflow

1. Clarify only missing essentials: topic/keywords, field, optional date range, and target report directory. If unspecified, default the report directory to `/Users/jackie/Documents/Git/Codex_Automated_Paper_Reader/paper-daily/reports`.
2. Run `scripts/search_papers.py` to query public sources, deduplicate against prior runs, download available PDFs, and write a candidate JSON file.
3. Inspect the JSON. If there are fewer than ten new papers, report the real count; do not pad with old or irrelevant papers.
4. Run a supplemental PDF download pass for every newly found paper whose `pdf_path` is empty. Try, in order: arXiv PDF URL if an arXiv id exists; OpenAlex `primary_location` / open access PDF when present; DOI publisher page; exact-title search on arXiv/OpenAlex/Semantic Scholar; and finally publisher-specific authenticated access such as IEEE/Chrome. Save any recovered PDF into `<reports-dir>/_paper_search_digest/pdfs/` with a non-overwriting filename, verify it with `file`, and record `supplemental_pdf_status` in the batch notes. Do not pass unverified HTML/login/access-denied files to downstream reading.
5. Build a processing list from all newly found papers in the JSON, using supplemental PDF paths when recovered. Default to processing every new paper returned by the search script. Skip only when a paper is duplicate, clearly off-topic, lacks enough source evidence to identify it, or the user explicitly requested a smaller count. Record the reason for every skip.
6. For every paper in the processing list with a local PDF path, invoke `/Users/jackie/.codex/skills/paper-deep-presentation/SKILL.md` and pass the local PDF path plus title/source URL. That skill must generate the detailed beginner-friendly presentation report with screenshots under `/Users/jackie/Documents/Git/Codex_Automated_Paper_Reader/paper-daily/paper-reports`.
7. If a paper in the processing list has no downloaded PDF, first try to find an authoritative PDF. If the authoritative page is IEEE Xplore, an IEEE DOI landing page, or otherwise resolves to `ieeexplore.ieee.org`, use the user's Chrome browser session because the user has a PolyU institutional login there. Open the IEEE page in Chrome, use the visible PDF/download controls from the logged-in session, save the PDF into `<reports-dir>/_paper_search_digest/pdfs/` with a non-overwriting filename, and verify the saved file with `file` before treating it as a PDF. If an IEEE document id / article number is known, the official full-text PDF page is usually `https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=<article-number>`; open that URL in Chrome before falling back to the article page's PDF button. Do not ask the user for credentials, do not expose cookies/tokens, and do not attempt to bypass access controls outside the logged-in browser session. If Chrome/PolyU access fails, record the exact failure reason and continue with the best authoritative URL/title.
8. If no PDF is available after the authoritative-source and IEEE/Chrome attempts, call `paper-deep-presentation` with the best authoritative URL/title and clearly mark missing PDF evidence in the batch summary.
9. Write only a lightweight batch index/summary into the reports directory using a non-overwriting filename. Include the date, topic slug, and a run timestamp or suffix, for example `2026-05-24-093012-edge-iot-paper-batch.md`. The batch index should link to each deep presentation report produced by `paper-deep-presentation` and list any skipped papers with reasons.
10. Update nothing else unless the user asked for it. Keep downloaded PDFs and JSON sidecars under the reports directory's `_paper_search_digest/` subfolder.

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

## Non-Overwrite Rules

Never overwrite previous outputs, especially when this skill runs multiple times on the same day.

- Before writing any report, scored JSON, note, asset directory, or manually downloaded PDF, check whether the target path already exists.
- If a path exists, create a new path by adding a timestamp (`HHMMSS`) or a numeric suffix (`-run2`, `-run3`).
- Prefer report names like `YYYY-MM-DD-HHMMSS-topic-paper-digest.md` for repeated runs.
- Prefer scored JSON names like `YYYY-MM-DD-HHMMSS-topic-scored.json` if writing structured scoring output.
- Prefer asset directories like `YYYY-MM-DD-HHMMSS-topic_assets/`.
- Do not rewrite `reports/YYYY-MM-DD.md` or any existing daily report unless the user explicitly asks to replace that exact file.
- Do not delete older reports, JSON files, PDFs, or asset folders while making room for a new run.
- In the final reply, include the exact new output paths and mention if a suffix or timestamp was added to avoid overwriting.

## Reading and Reporting Standards

Do not rely only on title keywords. For each newly found paper, identify enough metadata to decide whether it is valid to process or must be skipped:

- the actual problem and boundary conditions
- the key observation or insight
- the design choice and why it differs from prior work
- experiment setup, baselines, metrics, and main limitations
- trade-offs and deployment or ethics risks when relevant

Keep this identification brief in the batch index. The full explanation, terminology table, experiment walkthrough, screenshots, and presentation script must be produced by `paper-deep-presentation`, not by this skill. Default action is process, not skip.

For arXiv papers, prefer the PDF. For DBLP-only hits, use linked DOI/publisher pages or search the exact title on arXiv/OpenAlex/Semantic Scholar before concluding that a PDF is unavailable.

For IEEE papers, prefer the official IEEE PDF when access is available through the user's logged-in Chrome/PolyU session. Save only the downloaded PDF file, never browser profile data. If Chrome opens the PDF in the built-in PDF viewer or the Google Scholar Reader extension, use that viewer's visible Download button to save the PDF. After downloading, verify that the file is a real PDF rather than an HTML login page or access-denied page. If verification fails, mark it as `IEEE/PolyU 下载失败：<reason>` and do not pass the bogus file to `paper-deep-presentation`.

When the search script did not download a PDF, do not immediately mark the paper as missing evidence. Perform the supplemental pass above and write one of these statuses into the batch index: `补充下载成功`, `补充下载失败：无开放 PDF`, `补充下载失败：需要登录但 Chrome/PolyU 不可用`, `补充下载失败：下载文件不是 PDF`, or `补充下载失败：网络/页面错误 <details>`.

## Terminology Rules

When writing Chinese reports, do not leave technical English as unexplained shorthand. For `instrument/instrumentation`, `baseline`, `benchmark`, `marker`, `piggyback`, `workload`, and `trace`, explain the concrete action and role in the paper before using the term repeatedly.

- `instrument/instrumentation`: explain what code hook, protocol change, logging point, message field, or observation mechanism is added.
- `baseline`: explain which existing method or control group it represents and why it is a fair comparison.
- `benchmark`: explain the task set, environment, input/output, and scoring protocol.
- `marker`: explain what tag or signal is attached to a message/state and what it triggers.
- `piggyback`: explain what extra information is carried along with an existing message and why that avoids an extra round trip.
- `workload`: explain the concrete requests, jobs, traces, datasets, or traffic pattern used in experiments.
- `trace`: explain whether it is a request log, execution sequence, network packet record, or model/agent action history.

Do not use `instrument` as an untranslated Chinese verb. Prefer action-level explanations such as: `传统快照算法默认所有相关进程都能接入快照协议：它们可以在收发消息时携带快照标记，并在合适时刻记录本地状态`.

## Output Contract

The batch Markdown report must include:

- search metadata: query, field, sources, run date, report path, and number of new papers
- candidate JSON path and PDF directory
- a table of processed papers with title, year, venue/source, source link, local PDF path if available, duplicate status, and relevance note
- a table mapping each processed paper to the Markdown report generated by `paper-deep-presentation`
- skipped-paper notes for any candidates that were duplicate, clearly off-topic, lacked enough evidence, or were excluded by an explicit user count limit
- any failures: network/API/PDF download/rendering/deep-report generation errors
- for IEEE candidates, whether PDF access came from the Chrome/PolyU logged-in session, failed verification, or was unavailable
- supplemental PDF status for every processed or skipped paper whose original `pdf_path` was empty

Do not use this skill to generate the full per-paper technical report. If a per-paper report is needed, it must be created by `paper-deep-presentation`.

Do not invent missing details. Mark unavailable evidence as `未在论文或元数据中确认`.
