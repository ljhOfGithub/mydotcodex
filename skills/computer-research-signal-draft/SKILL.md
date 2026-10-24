---
name: computer-research-signal-draft
description: Prepare Chinese WeChat Official Account drafts focused only on one computer science research paper at a time. Use when Codex is asked to find or select one CS paper, deep-read its PDF or HTML full text, extract research signals, write a detailed 白Yu观测 computer-research-only article, capture original paper pages or figures for article imagery, or produce source notes without financial market content.
---

# Computer Research Signal Draft

## Goal

Write a computer-science-only public-account draft with full-text evidence. Do not include stock-market, macro, trading, or investment commentary unless the user explicitly asks to merge it later.

Default language is Chinese. Treat the article as research notes for "白Yu观测": clear, evidence-labeled, and useful for follow-up research.

## Workflow

1. Confirm topic and scope.
   - If the user gives no topic, default to recent computer science signals around AI agents, systems, security, evaluation, LLM infrastructure, HCI, data/ML systems, and distributed systems.
   - Use the current date/time for "today/latest"; verify live sources.

2. Search and record candidates.
   - Prefer `paper-search-digest` when a keyword batch is needed.
   - Use arXiv, DBLP, OpenAlex, publisher pages, project pages, and official repositories when relevant.
   - If a search script is used, read candidate JSON before selecting papers; stdout is not authoritative.
   - Save candidate/source notes with title, authors, paper-listed affiliations/source institutions, URL, date, PDF path, evidence status, and skip reason.
   - Treat author affiliations as source institutions. Do not substitute funders, model providers, benchmark owners, or repository hosts, and do not infer a collaboration that the paper does not state.

3. Require full-text evidence.
   - For public-account drafts, select papers with readable PDF or HTML full text whenever possible.
   - Download PDFs when available, verify with `file`, and extract text with `pdftotext`.
   - If PDF or HTML retrieval hits transient proxy/network errors, keep retrying that retrieval path until it succeeds or a clearly non-transient blocker is confirmed. Do not treat a proxy flap as evidence that the paper lacks full text.
   - When the daily paper-assets service is used, check its existing result with `/Users/jackie/Documents/paper daily/automation/local-assets/check-result.cjs --trigger-id <id>` in short, separate calls. Do not use a long shell sleep loop. A `pending` result means check the same ID again after bounded backoff; never recreate the trigger. If a tool returns `Script running with cell ID`, explicitly wait for that cell before continuing or ending the task.
   - Read the title/author block plus at least abstract, introduction, method/system design, experiment/evaluation, limitations, and conclusion before writing paper-level claims.
   - Use the introduction and related-work/problem-formulation text to extract 2-4 concrete background difficulties: what prior systems do, where they fail, and which data, interaction, scale, safety, latency, or deployment constraint makes the task hard.
   - If only abstract is available, label `abstract-only` and normally exclude it from main recommendations unless the user permits fallback.
   - If only title/listing is available, label `listing-only` and do not write method or result claims.

4. Select one paper for deep reading.
   - Default to exactly 1 main paper per WeChat article.
   - Use other papers only as brief background or comparison, not as additional mini-sections.
   - Pick the paper by actual contribution and evidence coverage, not keyword overlap.
   - Prefer a paper with a clear problem, concrete method/system, evaluation, limitation, follow-up angle, and readable original pages/figures/tables that can be captured directly.
   - In scheduled multi-slot runs, repeat the exact-ID/title duplicate scan immediately before creating any platform trigger. Re-read the current-day ledger, run reports, source notes, and automation memory because another slot may have completed after candidate selection. Read the Bilibili queue only when Bilibili publishing is active; when Bilibili is paused or excluded by the current user contract, do not read or inspect its frozen queue. If the paper is now present in a counted or submitted item, stop all new platform triggers for this copy, mark it `duplicate-concurrent-run`, keep it uncounted, and select a different paper. A duplicate scan performed only at candidate-selection time is not sufficient.

5. Draft structure.
   - Title: combine a faithful Chinese translation of the paper title with its core mechanism.
     - Default long-form pattern: `<paper title faithfully translated into Chinese>——<core mechanism verified from the full text>`.
     - Keep the method/system name when the original title contains one. The translated part must tell the reader the research object or task and the paper's stated contribution; the mechanism part must explain the main action, module, or inference/training process that makes it work.
     - Do not replace the translated paper meaning with a suspense hook, broad editorial contrast, standalone result number, or generic field claim. A verified number may follow the mechanism when space allows, but it cannot substitute for what the paper studies.
     - Record the original title, faithful Chinese translation, mechanism phrase, final long-form title, and any platform shortening in source notes.
     - Under a verified platform title limit, shorten in this order: remove secondary qualifiers, compress the mechanism phrase, then omit a result number. Always preserve the method/system name when present plus the research object and main mechanism; never shorten to a title that no longer reveals the paper's topic.
   - Opening: one paragraph explaining the research shift of the day.
   - Include one main paper only:
     - `论文信息`
     - `来源机构`
     - `背景与难点`
     - `一句话信号`
     - `为什么这篇值得细读`
     - `图怎么读` when a paper figure is used as the cover or a key visual.
     - `方法/系统设计`
     - `实验和指标`
     - `关键结果`
     - `限制和不确定性`
     - `结论和关键洞察`
     - `我会怎么继续跟踪`
   - Use `结论和关键洞察` as the mandatory synthesis, not as a repeated abstract:
     - Start with the authors' conclusion in 1-2 sentences, tied to the evaluated setting and strongest supporting result.
     - Extract 2-3 key insights in `claim -> evidence -> implication` form. Explain what the paper reveals about the system, method, failure mode, or research direction, not merely what components it contains.
     - Distinguish `论文结论` from `白Yu观测关键洞察`. If the paper has no dedicated conclusion section, say so and synthesize only from verified results and limitations.
   - End with what remains unresolved and 2-4 future research questions in `我会怎么继续跟踪`.
   - Treat the following as a body-depth gate, not optional expansion:
     - Open with 2 short paragraphs: first identify the paper-listed source institution(s), research task, prior/default practice, and concrete pain point; then state the paper's mechanism and strongest measured result without pretending the result generalizes beyond the evaluated setting.
     - In `论文信息/来源机构`, name the authors and paper-listed affiliations with a canonical paper URL. If the PDF does not expose affiliations clearly, write `来源机构：论文公开版本未明确列出` rather than guessing.
     - Expand `背景与难点` into 2-4 source-grounded obstacles before explaining the method. State why the existing/default approach is insufficient and what makes this task non-trivial; do not use generic field-growth language as a substitute.
     - Expand `关键方法` into 3-5 numbered mechanisms. For each mechanism, explain what signal enters, what state/module processes it, what decision/output it produces, and why that choice matters. Do not reduce a method item to a component name.
     - Expand `核心创新` into 2-4 source-grounded comparisons with prior or default practice. Name the changed interface, training/deployment assumption, or system boundary; avoid unsupported novelty adjectives.
     - Expand `实验和指标` into at least 4 distinct evidence points when the paper provides them: benchmark/task, baseline, metric, measured value or trend, and the cost/quality trade-off. Explain denominators and comparison conditions for large percentages.
     - Expand `图怎么读` beyond the paper caption: identify panels, axes, legends, arrows, table rows/columns, highlighted cells, and the exact comparison that supports the argument.
     - Expand `限制和不确定性` into at least 3 concrete items drawn from the paper or clearly labeled inference: evaluation coverage, model/data dependence, deployment cost, failure modes, missing ablations, or external-validity limits.
     - Expand `结论和关键洞察` into the authors' scoped conclusion and 2-3 evidence-grounded insights with implications. Keep evaluation and generalization boundaries in `限制和不确定性`.
   - Do not allow a core section to contain only a heading plus one sentence, or a list of result numbers without experimental context. Prefer evidence-rich explanation over filler; do not pad merely to reach a word count.
   - For a full WeChat/知乎/B站 mother article, normally provide roughly 2,500-4,500 Chinese characters of substantive body text when the paper has sufficient evidence. Shorter output must be justified by the paper's actual content, not platform convenience.
   - For the Xiaohongshu compact body, do not reuse the long-form narrative layout. Generate this fixed reference-style structure:
     - Title: a platform-length-safe compression of `<faithful Chinese paper-title meaning>，<core mechanism>`. Preserve the method/system name when present, the research object, and the main mechanism. Add the strongest verified numeric result only if space remains and its experiment and denominator support it; never let the number replace the paper topic.
     - Opening: `今天给大家带来一篇关于<topic>的新论文——《<paper title>》。` Follow with 1-2 plain sentences explaining the task.
     - Add `🎓 来源机构：<paper-listed affiliations>` on one line. Use the institutions printed in the paper, not funders or model providers; if unclear, state that the public version does not specify them.
     - Add `🔍 背景难点：<2-3 compact source-grounded sentences>` before `📝一句话总结`. Name at least two concrete weaknesses or constraints of the prior/default approach so a reader understands what problem the paper is solving.
     - `📝一句话总结`: exactly one non-empty line that combines the research task, core mechanism, and strongest scoped finding so the reader immediately knows what the paper reveals.
     - `🔑关键方法`: exactly 3 numbered items using `1️⃣` `2️⃣` `3️⃣`. Each item explains the component, input signal, decision/output, and training or inference behavior in 2-3 sentences.
     - `💡核心创新`: exactly 3 numbered items using `1️⃣` `2️⃣` `3️⃣`. Compare the paper with the default/prior approach and state what interface, training assumption, or deployment boundary changed.
     - Do not create an independent `📊实验效果` section. Preserve 2-4 decisive measurements by integrating each benchmark, baseline, metric, value/trend, and denominator caveat into the relevant method, innovation, limitation, or key-insight sentence.
     - `⚠️限制与边界`: 2-3 numbered items. Separate paper-stated limitations from the author's inference and avoid turning a narrow benchmark result into a universal claim.
     - `🧭结论和关键洞察`: exactly two consecutive lines after the heading: `论文结论：<conclusion tied to the evaluated setting>` and `关键洞察：<what the evidence reveals and why it matters>`.
     - End with `🧭结论和关键洞察`; do not repeat `论文：<full paper title>` because the opening already names the paper. Do not append submission invitations, cooperation pitches, or generic engagement questions.
   - Keep the Xiaohongshu compact body around 800-1,000 Chinese characters under the current validator. Preserve institution, background context, and the conclusion/insight/boundary block before trimming repeated wording elsewhere. Use only `🎓`, `🔍`, and the five functional section markers above; do not add decorative emoji chains or viral hashtags.
   - Use exactly one blank line between top-level blocks. Inside `📝一句话总结`, `🔑关键方法`, `💡核心创新`, `⚠️限制与边界`, and `🧭结论和关键洞察`, place the heading and every content line consecutively with no empty or whitespace-only line between them.
   - Treat this structure as mandatory for Xiaohongshu research handoff. Do not replace it with uninterrupted essay paragraphs, generic `论文信息/一句话信号` headings, or a shortened abstract.
   - When the output is intended for a WeChat draft, prepare for a designed HTML handoff: short mobile paragraphs, section cards, figure captions, and no raw Markdown bullet lists.
   - Do not use `<ul>/<li>` bullet lists for Chinese prose in the final WeChat version. Convert lists into numbered rows, compact cards, or separate short paragraphs.
   - Avoid dangling punctuation in list-like text, especially repeated semicolons and final "。，" patterns.
   - Use 2-4 screenshots taken directly from the original paper PDF or full-text HTML when available: one title/page or key-figure screenshot plus body figure/table screenshots that directly support the explanation. Do not create summary cards, redraw figures, synthesize diagrams, or generate AI images for computer-research articles.
   - Preserve the original visual content. Cropping page margins, scaling, or adding neutral padding for platform dimensions is allowed, but do not alter data, replace labels, or overlay generated summaries. Record the paper page number and Figure/Table identifier for every screenshot.
   - Each body screenshot must have a separate caption and a "how to read this figure" paragraph in the article text. This visual rule does not remove the full-text deep-reading or written analysis requirements.
   - Keep full-text reading separate from platform image delivery. Always read the full PDF, but if a target platform cannot accept all rendered pages in one post, let that publisher upload only the ordered prefix that fits and omit the remaining tail pages. Never create a second post for overflow pages.
   - Do not include investment-advice disclaimer wording in a computer-research-only article. If a closing note is needed, use research-specific wording such as "计算机科研阅读笔记，基于论文公开版本整理".

6. Evidence labels.
   - `A`: PDF/HTML full text read and locally recorded.
   - `B`: abstract/metadata plus trustworthy source, but no full text.
   - `C`: listing-only, early rumor, weak inference, or incomplete source.
   - Never upgrade evidence because the story sounds plausible.

7. Artifacts.
   - Write a Markdown draft and a source-note Markdown file.
   - Record PDF paths, text paths, retrieval failures, source URLs, and evidence labels.
   - Use a direct screenshot of the selected paper's title page, figure, diagram, or table as cover material. Save the screenshot path, source page, and Figure/Table identifier in source notes.
   - For WeChat-ready output, also write a final HTML draft when the repository/tooling supports HTML draft updates. Record local body-image paths and WeChat image URLs in source notes.
   - If the user wants WeChat publishing, hand off the final draft to `wechat-daily-signal-publisher` or the repository CLI; do not publish directly from this skill.

## Validation

Before finishing:

- Confirm exactly one main paper is interpreted in detail unless the user explicitly asks for a multi-paper roundup.
- For scheduled multi-slot runs, confirm the final pre-trigger duplicate scan was performed against current-day artifacts after drafting; reject `duplicate-concurrent-run` items before any platform trigger is created.
- Confirm the main paper has readable PDF/HTML full text or is explicitly marked as fallback.
- Confirm no finance/market signal section slipped into a research-only draft.
- Confirm no investment-advice disclaimer slipped into a research-only draft.
- Confirm source notes include candidate counts, selected titles, PDF/text paths, and failures.
- Confirm source notes record authors and paper-listed affiliations/source institutions, and the article states them without guessing.
- Confirm every research image is a direct screenshot from the selected paper, with page/Figure/Table provenance, and that no summary card, redraw, synthesized diagram, or AI-generated image was created.
- Confirm platform source notes distinguish `pdf_pages`, `uploaded_pages`, and `omitted_pages` whenever a platform image limit truncates the rendered PDF.
- Confirm every important claim has a source or evidence label.
- Confirm the body passes the depth gate: 3-5 explained method mechanisms, 2-4 grounded innovations/comparisons, at least 4 contextualized experimental findings when available, a concrete figure reading, at least 3 limitations or uncertainties, and a distinct `结论和关键洞察` section.
- Confirm `结论和关键洞察` separates the authors' conclusion from 2-3 evidence-grounded editorial insights and connects each insight to supporting evidence and its implication. Keep limitations and external-validity caveats in `限制和不确定性`.
- Confirm `背景与难点` appears before the method and explains at least two source-grounded obstacles or prior-approach failures.
- Confirm the Xiaohongshu handoff uses the exact opening + `📝一句话总结` + `🔑关键方法` + `💡核心创新` + `⚠️限制与边界` + `🧭结论和关键洞察` structure rather than long-form essay prose.
- Confirm the long-form title follows `<faithful Chinese translation>——<verified core mechanism>`, source notes record the title mapping, and every shortened platform title still exposes the method/system name when present, research object, and main mechanism.
- Treat this as a literal structure regression gate, not a semantic checklist: require the markers in that order; exactly one non-empty line under `📝一句话总结`; exactly three `1️⃣`/`2️⃣`/`3️⃣` items under both `🔑关键方法` and `💡核心创新`; 2-3 limitation items; and exactly one `论文结论：` and `关键洞察：` line under `🧭结论和关键洞察`. Reject an independent `📊实验效果` section and a trailing `论文：<full paper title>` line. Confirm decisive experimental evidence remains embedded in the surviving sections. Regenerate if the article is informative but the observable skeleton differs.
- Confirm the Xiaohongshu body contains `🎓 来源机构：` and `🔍 背景难点：` before `🔑关键方法`; allow one blank line between blocks but reject blank or whitespace-only lines inside any compact section.
- Confirm WeChat-ready drafts avoid raw bullet-list rendering and include enough body imagery for the explanation, not just a cover.
- Confirm exact brand spelling is `白Yu观测`, with no space between `Yu` and `观测`.
