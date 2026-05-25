---
name: paper-deep-presentation
description: Deep-read one research paper from a local file path, PDF, arXiv/DOI URL, or exact title; save screenshots of important figures/tables from the paper; explain technical terms for a beginner in Chinese; reconstruct the paper's experimental process in presentation style; and write a Markdown report with embedded images to /Users/jackie/Documents/Git/Codex_Automated_Paper_Reader/paper-daily/paper-reports. Use when the user asks to 精读/精度/讲解 a single paper, understand its terminology, prepare a presentation, preserve paper figures, or produce a beginner-friendly paper report.
---

# Paper Deep Presentation

Use this skill to turn one paper into a Chinese Markdown presentation report for an entry-level reader in the field. Be faithful to the paper, explain prerequisites patiently, and make the experiment section detailed enough that the user can present it.

## Output Location

Always write the final Markdown file under:

```text
/Users/jackie/Documents/Git/Codex_Automated_Paper_Reader/paper-daily/paper-reports
```

Use a filename like:

```text
YYYY-MM-DD-short-title-presentation.md
```

For screenshots, create a sibling assets directory named after the report file:

```text
/Users/jackie/Documents/Git/Codex_Automated_Paper_Reader/paper-daily/paper-reports/YYYY-MM-DD-short-title-presentation_assets
```

Create the directory only if it does not exist. Do not write reports elsewhere unless the user explicitly overrides the path.

## Workflow

1. Identify the paper source.
   - If the user gives a local file path, verify it exists before reading.
   - If the user gives a title or URL, search authoritative sources first: arXiv, OpenReview, ACL Anthology, ACM/IEEE publisher pages, DOI landing pages, official project pages, or author PDFs.
   - If multiple papers match a title, stop and ask the user to choose instead of guessing.
2. Extract and inspect the paper.
   - Prefer PDF text extraction for PDFs (`pdftotext`, `mutool`, PyMuPDF, or another available parser).
   - Read at least abstract, introduction, method, experiments, results, limitations, and appendix sections when present.
   - Check figures/tables when they carry experimental settings or results.
3. Save and review paper visuals.
   - Identify all figures/tables that are needed to explain the method, system architecture, experiment setup, main results, ablations, or limitations.
   - Render screenshots into the report assets directory. Prefer cropped figure/table screenshots when coordinates can be determined; otherwise save the full page that contains the figure/table.
   - Use stable names such as `figure-04-system-design.png`, `table-01-gpt2-tta.png`, or `page-07-main-results.png`.
   - Embed important screenshots in the Markdown report with paths relative to the Markdown file, for example `![Figure 4: system design](YYYY-MM-DD-short-title-presentation_assets/figure-04-system-design.png)`.
   - Do not use absolute local paths such as `/Users/...` in Markdown image links; VS Code Preview may render them as blank. Keep the assets directory next to the report and link it relatively.
   - After rendering, inspect the image files when possible. Do not include blank, unreadable, or irrelevant screenshots.
4. Build a beginner vocabulary map.
   - Extract domain terms, acronyms, model names, datasets, metrics, algorithm names, and evaluation protocols.
   - Explain each term as if the user is new to the area: plain definition, why it appears in this paper, and how it connects to the paper's contribution.
   - Include any English term that remains in the Chinese prose, even if it is a common systems/ML verb such as `instrument`, `benchmark`, `baseline`, `marker`, `piggyback`, `profiling`, or `workload`.
   - Do not over-explain generic English words; focus on terms that block understanding.
5. Reconstruct the paper's logic.
   - State the research problem, why it matters, what prior approaches miss, and the paper's core idea.
   - Separate what the paper claims from what the experiments actually support.
6. Explain the experiments like a formal presentation.
   - Cover datasets/tasks, train/test split or benchmark protocol, baselines, metrics, implementation details, ablations, main tables/figures, and failure cases.
   - For each experiment, answer: question being tested, setup, comparison target, result, author's interpretation, and your caveat.
   - Tie each major experiment explanation back to its screenshot or table image when available.
   - If a detail is missing in the paper, write `论文中未明确说明` rather than inventing it.
7. Write the Markdown report using `references/report-template.md`.
8. Verify the report.
   - Confirm the Markdown file exists in the required output directory.
   - Confirm the assets directory exists and contains the screenshots referenced by the Markdown report.
   - Confirm every embedded image path points to an existing file when resolved relative to the Markdown report.
   - Include source path/URL, extraction method, and any unavailable evidence in the report.
9. Hand off to Zotero when local paper management is requested.
   - Use `$zotero-paper-library` to create a reviewable import manifest for the source PDF, generated Markdown report, and useful report assets.
   - Prefer attaching the Markdown report and screenshots to the same Zotero paper item rather than creating separate paper items for generated artifacts.
   - Preserve provenance tags such as `codex`, `paper-deep-presentation`, and the paper topic.

## Reading Standards

- Do not rely only on abstract or title.
- Do not fabricate numeric results, dataset sizes, hyperparameters, baselines, or author claims.
- Quote sparingly. Prefer paraphrase and cite section/table/figure names when possible.
- Keep the tone Chinese, beginner-friendly, and presentation-ready.
- When the paper is outside the user's likely background, add a short prerequisite ladder: what to understand first, second, and third.
- If the paper has weak experiments or unsupported claims, say so clearly but fairly.

## Language and Terminology Standards

- Prefer Chinese explanations over English-heavy prose. On first use, write `中文译名（English term）`; after that, use the Chinese term unless the English abbreviation is standard in the field.
- Do not put unexplained English verbs directly into Chinese sentences. Avoid vague phrases such as `被 instrument`, `去 benchmark`, `做 profiling`, or `piggyback marker`.
- Rewrite English-heavy phrases into concrete Chinese actions. Example: replace `进程能被 instrument` with `进程能接入快照协议，也就是能在收发消息时携带快照标记，并在合适时刻记录本地状态`.
- If an English term is retained anywhere in the report, add it to the glossary with: Chinese translation, beginner explanation, why it matters in this paper, and one common misunderstanding.
- For `instrument/instrumentation`, explain it as `接入协议/加观测或协议埋点`: modifying, configuring, or wrapping a component so it participates in measurement/control, carries protocol metadata, or records state.
- Before finalizing, scan for unexplained English terms. At minimum check: `instrument`, `instrumentation`, `benchmark`, `baseline`, `marker`, `gateway`, `snapshot`, `out-group`, `in-group`, `piggyback`, `artifact`, `workload`, `profiling`, and `trace`.

## Useful Commands

Use commands only after explaining why. Examples:

```bash
pdftotext "/path/to/paper.pdf" -
```

```bash
python3 - <<'PY'
import fitz, sys
doc = fitz.open(sys.argv[1])
for i, page in enumerate(doc, 1):
    print(f"\n--- page {i} ---")
    print(page.get_text())
PY "/path/to/paper.pdf"
```

Use `rg` to inspect extracted text for sections such as `Experiment`, `Evaluation`, `Ablation`, `Dataset`, `Baseline`, `Limitation`, and `Appendix`.

Render selected PDF pages or cropped regions with the bundled helper:

```bash
python3 /Users/jackie/.codex/skills/paper-deep-presentation/scripts/render_pdf_screenshots.py \
  --pdf "/path/to/paper.pdf" \
  --out-dir "/Users/jackie/Documents/Git/Codex_Automated_Paper_Reader/paper-daily/paper-reports/YYYY-MM-DD-short-title-presentation_assets" \
  --pages "1,4,8-10" \
  --slug "paper"
```

For cropped screenshots, pass one or more region specs in PDF point coordinates:

```bash
python3 /Users/jackie/.codex/skills/paper-deep-presentation/scripts/render_pdf_screenshots.py \
  --pdf "/path/to/paper.pdf" \
  --out-dir "/path/to/report_assets" \
  --region "figure-04,5,72,110,540,430"
```

Region format is `name,page,x0,y0,x1,y1`, using 1-based page numbers. If exact crop coordinates are uncertain, render the full page first and use that screenshot in the report rather than guessing.

## Report Contract

The final report must include:

- Paper identity: title, authors, venue/year if known, source path/URL, and report date.
- One-slide executive summary.
- Visual evidence index: a table listing each saved screenshot, what it shows, and where it is explained. Use relative image paths so VS Code Preview renders the images.
- Beginner prerequisite map.
- Technical terminology glossary.
- Problem and motivation.
- Method explanation.
- Detailed experiment walkthrough.
- Results interpretation and limitations.
- Presentation script: a structured talk track the user can speak from.
- Reading notes: what to reread, what remains uncertain, and follow-up papers or keywords.

Read `references/report-template.md` before writing the report.
