---
name: paper-vocab-cet6-plus
description: Extract and explain English vocabulary from one paper or a collection of papers, focusing on words and technical terms likely harder than China's College English Test Band 6 (CET-6). Use when Codex is asked to read PDFs, Markdown, text, DOCX, paper notes, abstracts, or paper folders and produce a Chinese vocabulary table, glossary, or learning list of advanced difficult words from the given academic material.
---

# Paper CET-6+ Vocabulary

## Overview

Use this skill to turn a given paper or paper set into a Chinese vocabulary table of words likely above CET-6 level. Treat the bundled script as a candidate generator with built-in Chinese meanings, then use paper context to verify meanings, merge variants, and write a readable final glossary.

## Workflow

1. Identify inputs: local file paths, folders, URLs, paper titles, abstracts, or pasted text. If URLs or titles are given, retrieve the paper text/PDF when possible and keep source paths/links in the final report.
2. Extract text. For local `.txt`, `.md`, `.pdf`, and `.docx` files, prefer `scripts/extract_cet4_plus_vocab.py`. For unsupported formats, convert or manually extract text with the best available tool.
3. Review candidates instead of blindly trusting them. Remove:
   - author names, affiliations, venue names, references-only terms, broken OCR fragments, and pure package/model names unless pedagogically useful;
   - ordinary CET-6/basic academic words that survived the heuristic filter;
   - duplicates and simple inflection variants when one lemma is enough.
4. Always add Chinese meanings. For each selected word or phrase, include meaning in this paper, common meaning if useful, part of speech, difficulty reason, and a short source phrase or paraphrased context. Do not deliver a user-facing table with empty placeholder meanings.
5. Mark evidence level. Use `全文` when extracted from full text, `摘要/元数据` when only abstract or metadata was available, and `人工补充` when the word is inferred from user-provided notes.

## Recommended Command

Run from any working directory:

```bash
python3 /Users/jackie/.codex/skills/paper-vocab-cet6-plus/scripts/extract_cet6_plus_vocab.py \
  --input /path/to/paper-or-folder \
  --output /path/to/vocab.md \
  --top 120
```

Useful options:

- `--input`: file or folder. Folders are scanned recursively for `.txt`, `.md`, `.pdf`, and `.docx`.
- `--output`: Markdown report path. If omitted, the report prints to stdout.
- `--top`: maximum candidate words before manual polishing.
- `--min-count`: minimum frequency, default `1`.
- `--include-phrases`: also include frequent academic bigrams such as `latent representation`.
- The script fills Chinese meanings from its built-in academic glossary. If a rare item is missing, it writes `需结合上下文确认`, and Codex must fill or remove it before final delivery.

## Output Format

For user-facing results, prefer this Markdown structure:

```markdown
# CET-6+ 论文词表

来源:
- /path/to/paper.pdf

证据等级: 全文

| Word / Phrase | 词性 | 中文含义 | 论文语境 | 难度原因 | 出现次数 |
|---|---|---|---|---|---:|
| quantization | n. | 量化 | quantization-aware training | CET-6 以外的 AI/系统专门术语 | 7 |
```

Keep explanations concise and useful for learning. When the same term appears across multiple papers, mention representative source files rather than listing every occurrence.

## Difficulty Heuristics

Use these as filters, not hard truth:

- Likely above CET-6: specialist AI/system terms (`quantization`, `ablation`, `hallucination`, `orchestration`), research-method nouns (`calibration`, `provenance`, `conformance`), specialist adjectives (`stochastic`, `adversarial`, `granular`), and paper phrases (`causal inference`, `latent representation`, `systematic uncertainty`).
- Usually not worth listing: broad academic words (`performance`, `evaluation`, `information`, `background`, `conference`, `development`) unless the paper uses a narrow technical sense.
- Preserve domain terms if they help the reader understand the paper, even when they are proper nouns, but label them as `术语` rather than ordinary vocabulary.
- If only abstract text is available, say so clearly and avoid overclaiming coverage.

## Quality Checks

Before final delivery:

- Confirm every listed item appears in the supplied paper text or user-provided content.
- Avoid fabricating Chinese meanings from title keywords alone.
- Include source path/link and evidence level.
- If the script fails to read a PDF because OCR is needed, report that limitation and use another extraction path if practical.
