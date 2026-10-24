---
name: daily-push-skill-improver
description: Review and improve daily publishing skills after trial runs or production runs, especially skills that gather papers, market signals, news, source notes, browser publishing steps, and public-account drafts. Use when Codex is asked to refine, harden, debug, or evolve a daily push/publisher skill based on generated drafts, source logs, failure cases, user feedback, or recurring automation outcomes.
---

# Daily Push Skill Improver

## Goal

Improve a daily publishing skill without drifting into broad rewrites. Use real run artifacts to tighten evidence rules, failure handling, source bookkeeping, article structure, browser-publishing boundaries, and validation checks.

Default to small, reviewable edits. Do not publish content, operate logged-in accounts, or change automations unless the user explicitly asks.

## Required inputs

Gather the smallest available set:

- Target skill path, for example `/Users/jackie/.codex/skills/wechat-daily-signal-publisher/SKILL.md`.
- Run artifacts: draft Markdown, source notes, candidate JSON, screenshots, browser notes, error logs, or final user feedback.
- Desired improvement direction: reliability, article quality, evidence rigor, market coverage, paper coverage, Chrome publishing, or automation handoff.

If the target skill path is missing, discover it with `rg --files ~/.codex/skills | rg 'SKILL.md$'` and inspect candidates before editing. Do not invent paths.

## Review workflow

1. Read the target skill completely.
2. Read the run artifacts completely when short; for long logs, search first for `error`, `failure`, `abstract-only`, `429`, `timeout`, `PermissionError`, `published`, `draft`, `preview`, `source`, `evidence`, and user feedback.
3. Classify findings:
   - `Evidence`: unsupported claims, missing source URLs, weak evidence mislabeled as strong, missing abstract-only/full-text boundaries.
   - `Retrieval`: network failures treated as empty results, missing candidate JSON inspection, API/rate-limit gaps.
   - `Market`: stale data, missing timestamp/region, personalized investment advice risk, unsupported ticker claims, or platform rejection for prohibited financial services.
   - `Writing`: unclear title, weak opening, too broad/narrow structure, no follow-up watchlist, or semantic completeness that still fails to reproduce a user-supplied reference's literal title/opening/section/count/closing skeleton.
   - `Layout`: bare Markdown conversion used as final WeChat layout, messy bullet dots, awkward list punctuation, missing figure captions, cover-only imagery, missing mobile-reading structure, blank or whitespace-only lines between a compact Xiaohongshu section heading and its items or between items in the same section, large decorative header bands or empty safe areas with no information role, unreadable full-page paper screenshots squeezed into social cards, unclear screenshot crop boundaries that include unrelated body text, Xiaohongshu/Douyin reflow drifting too far from the source article's editorial style, short-summary bodies masquerading as full compact posts, or platform content becoming a parallel rewrite instead of a compact same-content edition.
   - `Depth`: content reads like a generic AI summary, lacks source-specific figure/table reading, skips method/evaluation/limitations, uses empty signal phrases without mechanisms, or turns a paper deep-read into slogans.
   - `Publishing`: unavailable creator capability, accidental final-publish risk, credential/session exposure risk, or a blocking login/verification/account-switch prompt. When the user has declared that only one default account is logged in, do not invent an account-name matching gate.
     For 白Yu观测 browser publishing, also treat route drift between 9223, the Chrome extension, and Computer Use, plus unclosed task tabs/windows, as reusable publishing defects. Require the canonical contract at `/Users/jackie/Documents/paper daily/automation/platform-publisher/BROWSER_SESSION_CONTRACT.md`.
   - `Artifacts`: no source notes, no run log, unclear output paths, no validation checklist.
4. Decide whether to edit:
   - Patch the skill directly when the improvement is clear, small, and generalizable.
   - Produce a change proposal only when the desired behavior is ambiguous, risky, or depends on user preference.
5. Keep changes scoped to the target skill and optional `agents/openai.yaml` metadata. Avoid unrelated files.

## Patch rules

- Preserve existing useful rules; strengthen or clarify them instead of replacing the whole skill.
- Add concrete stop conditions for failures: DNS, SSL, 429, 504, timeout, login/2FA, wrong account, missing candidate records.
- Require source artifacts for every run: `draft.md`, `sources.md`, and when useful `run-log.md`.
- Require evidence labels for public claims and explicit `abstract-only` / `listing-only` labels for papers.
- Require financial disclaimers and prohibit personalized buy/sell/target-price language unless the user explicitly requests analysis.
- When a platform reports `金融行业违规服务内容`, add the matched category to the finance candidate gate. Require the scanner to run before topic selection and before upload; a hit must replace the entire article with the next eligible candidate, not trigger keyword-only rewriting.
- Require browser publishing to default to local draft, WeChat draft, or preview; final publish only with explicit current-turn authorization.
- For WeChat article skills, require a final-layout pass before draft update: avoid raw HTML bullet lists in Chinese prose, replace them with cards/numbered rows/short paragraphs, scan for old brand spelling variants, and record any body-image uploads.
- For Xiaohongshu publisher skills, require same-content lightweight reflow rather than persona rewrite: treat the WeChat/public-account article as canonical, preserve title/section order/claims/conclusion when possible, avoid over-platformized hooks/tags, and keep visual cards as a restrained reading guide carrying details that do not fit the body limit.
- When the user supplies a reference post, extract a compact structural contract before drafting: title formula, opening sentence pattern, literal section markers and order, item counts, result-line markers, and closing line. Make those observable features validation gates; matching only the topic, tone, or information density is not sufficient.
- When a research reference names source institutions and explains the background difficulty before the method, require both in the mother draft and compact platform handoff. Use paper-listed affiliations and concrete prior-approach failures; do not guess institutions or replace the difficulty with generic field context.
- For compact Xiaohongshu research sections, require exactly one blank line between top-level blocks and zero blank or whitespace-only lines inside a block. Keep the heading and all `1️⃣`/`2️⃣`/`3️⃣` or `✅` lines consecutive.
- When a user asks for a `纯文字` finance image, set the default package to exactly one image and explicitly prohibit icons, charts, arrows, photos, illustrations, data tiles, boxed modules, and carousels. Inspect the rendered image itself after generation; a compliant prompt or source file is not visual evidence.
- Treat an explicitly required discovery source such as `jin10.com` as a candidate gate. Record the current source URL, displayed timestamp, retrieval time, and original official source when available; silently substituting another discovery source or stale material is a failed run.
- If a required validator runtime such as `node` is missing from `PATH`, load the workspace dependencies and use the executable path returned by that environment. Do not skip the validator, guess a runtime path, or install into the system environment.
- If a public Xiaohongshu short link cannot be opened by the web fetcher, use the available logged-in browser only to inspect the public reference. Stop at login, QR, CAPTCHA, phone, or other verification prompts; do not bypass them.
- When the user has explicitly chosen the single default logged-in account, validate creator/editor capability rather than a visible account label or UID. Continue to stop for login, QR, CAPTCHA, 2FA, phone, identity, account-switch, or sensitive confirmation.
- For Douyin publisher skills, prohibit short abstract-only bodies when a full compact source exists: the body must include method, evaluation/score, figure/table reading, and limitations within the character limit; if an existing post edit shows `修改审核中`, record that the public listing may still show the old body.
- Do not instruct Codex to rely on WeChat's UI "one-click layout" unless the task explicitly uses Chrome editor control. API-based workflows must generate their own WeChat-ready HTML.
- Require research/technical posts to use source figures/tables as body images when available, with captions and explanations. A cover image alone is not enough for a detailed paper-reading article.
- Require all social-platform cards to carry source detail rather than slogans: each card should explain a figure, mechanism, metric, limitation, or argument from the source.
- Require social-platform source screenshots to be cropped to the relevant figure/table/diagram region with clean boundaries. Prohibit full-page thumbnails when they make labels unreadable, and require zoom/detail cards for dense figures.
- Require figure explanations to be concrete and plain: name axes, legends, arrows, colors, modules, table rows/columns, highlighted values, and the comparison the reader should make. A copied paper caption or a vague "图中展示" sentence is not enough.
- Add targeted checks for generic AI/platform language such as `一文看懂`, `干货满满`, `颠覆认知`, `建议收藏`, `打开新思路`, `赋能`, and empty phrases like `核心信号是` when not followed by source-specific detail.
- Keep `agents/openai.yaml` aligned with the skill description if the user-facing behavior changes.

## Validation

After edits:

- Run the skill validation script:
  `python3 /Users/jackie/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>`
- If `PyYAML` is missing, use an existing environment that has it or create a temporary venv under `/tmp`; do not install packages into system Python.
- Check for leftover template text with `rg -n "TODO|\\[TODO\\]" <skill-dir>`.
- Re-read the edited sections and ensure no secrets, account credentials, or private browser state were recorded.
- For layout regressions, run targeted text checks for raw HTML list tags, old brand spelling variants, malformed sentence punctuation, and awkward list punctuation when applicable.
- For depth regressions, check that technical social posts contain figure/table interpretation, method, evaluation/score, and limitation/follow-up markers before browser upload or publish.
- For visual regressions, inspect generated card dimensions and at least the cover plus every card that contains a source screenshot; verify the crop is clean and readable on mobile-sized viewing.
- For reference-style regressions, compare the actual draft's literal marker order and item counts with the extracted structural contract.
- For compact Xiaohongshu layout regressions, run a deterministic text check that rejects `\n[ \t]*\n` inside each section after trimming the separator before the next top-level marker.
- For pure-text finance-image regressions, verify `image_count=1`, the visible brand is exactly `白Yu观测`, the source and timestamp are legible and correct, and no prohibited non-text module appears.
- When a policy scanner used a fallback runtime, record the resolved executable and scanner exit code in the run/source notes without recording credentials or environment secrets.
- If the edit came from a concrete run, state which run artifact motivated each material change.

## Output format

Report:

- Target skill path.
- Files changed.
- Main improvements.
- Validation command and result.
- Remaining risks or questions.

When no direct edit is made, provide a concise patch plan with exact sections to change.
