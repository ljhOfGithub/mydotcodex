# Zotero Workflow Reference

## Import policy

- Prefer official Zotero UI actions and local API behavior over direct file manipulation.
- Use Zotero's metadata retrieval first for DOI, arXiv, and PDF metadata.
- Keep downloaded source files in place until the user confirms Zotero has copied or linked them correctly.
- If a PDF is associated with a generated Markdown report, import the paper item first, then attach the report to that same item as a linked file.

## Collection strategy

Use a shallow hierarchy so future Codex runs can find work quickly:

```text
Codex Papers/
  <topic or project>/
    <YYYY-MM-DD batch or survey name>
```

Examples:

- `Codex Papers/Systems for AI/2026-05-25`
- `Codex Papers/Paper Daily/2026-05-25`
- `Codex Papers/Deep Reads/<paper short title>`

## Tags

Use predictable tags:

- Workflow tags: `codex`, `paper-deep-presentation`, `field-progress-survey`, `paper-search-digest`
- Status tags: `to-read`, `skimmed`, `deep-read`, `survey-cited`, `metadata-needs-review`
- Topic tags: use short normalized topic names, for example `llm-serving`, `distributed-training`, `ai-systems`

## Metadata fields to preserve

At minimum preserve:

- Title
- Authors, if known
- Year, if known
- Venue/source, if known
- DOI, arXiv ID, OpenReview URL, ACM/IEEE/ACL URL, or publisher URL
- Original PDF path
- Generated report path
- Search or reading workflow that produced the artifact

When metadata is uncertain, tag the item `metadata-needs-review` instead of inventing missing fields.

## Duplicate checks

Check in this order:

1. DOI exact match
2. arXiv ID exact match
3. Normalized title match
4. First author plus year plus title similarity

Do not merge automatically unless the user explicitly asked for automatic merging and the identifier match is exact. Otherwise, present duplicate candidates and evidence.

## Local Zotero API notes

The Zotero desktop app can expose a local API on `http://127.0.0.1:23119`. Availability depends on the user's Zotero settings and whether Zotero is running. Use it only after a successful local check. If write operations are unsupported or rejected, fall back to a manifest and manual Zotero import instructions.

Never use the online Zotero Web API unless the user explicitly provides or authorizes credentials for that session.
