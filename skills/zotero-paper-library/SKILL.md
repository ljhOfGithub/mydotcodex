---
name: zotero-paper-library
description: Manage research papers with the user's local Zotero library. Use when Codex needs to import, organize, deduplicate, tag, or attach PDFs, Markdown reports, screenshots, BibTeX/RIS/CSL metadata, or papers downloaded by paper-deep-presentation, field-progress-survey, or paper-search-digest workflows.
---

# Zotero Paper Library

Use this skill to turn downloaded research artifacts into a traceable local Zotero library. Prefer safe, reviewable steps: inspect files, build an import manifest, verify metadata, then import through Zotero-supported mechanisms.

## Safety Rules

- Do not edit Zotero's SQLite database directly.
- Do not delete Zotero files, storage folders, PDFs, reports, or downloaded artifacts.
- Do not expose API keys, account tokens, private notes, or unrelated library content.
- Prefer local Zotero client features or the Zotero local API at `127.0.0.1:23119` when available.
- If Zotero is not running or the local API is unavailable, create a manifest and tell the user what can be imported manually.
- Keep provenance: preserve source URL, DOI, arXiv ID, original PDF path, report path, and the Codex skill that produced the artifact.

## Workflow

1. Identify artifacts.
   - For `paper-deep-presentation`, inspect the report under `/Users/jackie/Documents/Git/Codex_Automated_Paper_Reader/paper-daily/paper-reports` and its sibling assets directory.
   - For `field-progress-survey`, inspect cited paper links, downloaded PDFs, BibTeX/RIS/CSL files, and generated survey reports.
   - For `paper-search-digest`, inspect downloaded PDFs and search result metadata.

2. Check local Zotero safely.
   - Run `scripts/zotero_local_check.py` to report whether Zotero directories and the local API are visible.
   - Treat the result as diagnostic only; do not infer that missing API means missing Zotero.

3. Build an import manifest.
   - Run `scripts/build_import_manifest.py --root <artifact-dir> --out <manifest.jsonl>` for downloaded folders, or pass specific files with `--path`.
   - Review the manifest for guessed title, DOI, arXiv ID, file type, SHA-256, and modification time.
   - Correct weak title guesses manually before import when needed.

4. Import and organize.
   - Prefer Zotero's own metadata retrieval from DOI, arXiv ID, ISBN, or PDF metadata.
   - Create or reuse a collection named for the project/topic/date, for example `Codex Papers/Systems for AI/2026-05-25`.
   - Attach PDFs as stored Zotero attachments unless the user asks for linked files.
   - Attach generated Markdown reports and useful figure screenshots as linked attachments when they are local Codex outputs.
   - Add tags such as `codex`, `paper-deep-presentation`, `field-progress-survey`, topic keywords, and review status (`to-read`, `deep-read`, `survey-cited`).

5. Deduplicate and verify.
   - Match duplicates by DOI, arXiv ID, normalized title, and first-author/year.
   - Merge only after showing the likely duplicate pair and the evidence.
   - Verify every imported item has at least a title, year when known, source identifier or URL, and attachment path.

6. Report back.
   - Summarize imported count, skipped count, duplicate candidates, missing metadata, and any files requiring manual Zotero action.
   - Include manifest path and collection/tag decisions.

## Commands

Explain why before running commands. Useful commands:

```bash
python3 /Users/jackie/.codex/skills/zotero-paper-library/scripts/zotero_local_check.py
```

```bash
python3 /Users/jackie/.codex/skills/zotero-paper-library/scripts/build_import_manifest.py \
  --root "/path/to/downloaded/papers" \
  --out "/path/to/zotero-import-manifest.jsonl"
```

```bash
python3 /Users/jackie/.codex/skills/zotero-paper-library/scripts/build_import_manifest.py \
  --path "/path/to/paper.pdf" \
  --path "/path/to/report.md"
```

## Detailed Guidance

Read `references/zotero-workflow.md` when you need exact tagging, collection, import, duplicate-check, or report-attachment guidance.
