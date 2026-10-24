---
name: zhihu-daily-signal-publisher
description: Preserve the permanent 白Yu观测 Zhihu publishing pause. Zhihu adaptation, verification, publication, recovery, browser work, imports, and submission stay disabled until the user explicitly restores them.
---

# Zhihu Daily Signal Publisher

## Permanent publication pause

Zhihu is permanently paused by the user for `yu-daily-cross-platform-drafts` and every related manual, scheduled, catch-up, repair, verification, or recovery path.

- Do not generate or adapt Zhihu Markdown/DOCX artifacts, jobs, bundles, or triggers.
- Do not consume an existing Zhihu trigger, open or inspect Zhihu in a browser, import a document, edit, verify, submit, update, retry, or recover an earlier task.
- Record every applicable Zhihu cell as `publication-paused-by-user` with `actions=0`. This is not a failure, omission, or recoverable backlog.
- Preserve historical local files, results, public URLs, and state as evidence. Do not delete, rewrite, or backfill them.
- Only a later explicit user instruction to restore Zhihu can lift this pause. Restore the skill, automation prompt, trigger preparer, worker, and platform adapter/CLI gates together before any action.
- This gate overrides every workflow, retry, verification, and browser instruction below.

## Purpose

Publish the same evidence-led article used by the other 白Yu观测 platforms as a readable Zhihu article. Convert formatting, not claims.

## Workflow

1. Confirm source and authorization.
   - Use the WeChat article as the canonical source.
   - Daily automation publishes finance at five scheduled runs and research at seven five-platform runs, for 7 research + 5 finance articles per day. Xiaohongshu-only research additions do not enter Zhihu.
   - Use `chrome:control-chrome` and the logged-in Zhihu creator session.
   - Use the user's single default logged-in account. Confirm the creator and article functions are available; do not require a visible account-name match.
   - Stop for login, QR, CAPTCHA, 2FA, phone, identity, account-switch, or sensitive confirmation.

2. Prepare the article.
   - Save under `reports/zhihu/YYYY-MM-DD-topic/zhihu-article.md`.
   - Build a DOCX import package for the platform editor. Use real heading styles and embedded images; a Markdown file is only a source artifact, not a publish-ready rich-text payload.
   - Validate the DOCX before import. On macOS Scheduled/LaunchAgent runs, do not invoke LibreOffice/`soffice` for visual QA: headless startup can abort in `RegisterApplication` and leave a system crash modal over later publisher windows. Use `qlmanage` Quick Look for a first-page visual check plus structural heading/image checks. If Quick Look is unavailable, record full-page visual QA as partial rather than passed; never fall back to `soffice` in that run.
   - Preserve the canonical title keywords, section order, evidence, uncertainty, limitations, and conclusion.
   - Research articles must retain paper identity, figure/table reading, method/system design, evaluation, limitations, and follow-up.
   - Finance articles must retain source timestamps, evidence, counter-evidence, risks, and a platform-safe non-recommendation statement.
   - Use short paragraphs and descriptive headings. Do not reduce the article to card captions or a generic abstract.
   - For computer-research articles backed by a PDF, embed original pages in order in one native DOCX import package; do not replace them with selected screenshots. If the verified editor/import image limit cannot accept all pages, embed only the ordered prefix that fits, omit the tail, and do not create a second article. Record `pdf_pages`, `embedded_pages`, `omitted_pages`, and `visual-truncated`.
   - Scale or add neutral padding only when needed for readability. Do not crop paper content, alter paper data, or overlay generated summaries. Never describe a truncated image set as the full PDF, and keep the explanation in article text.

3. Validate.
   - Require full text for research. Do not publish `abstract-only` or `listing-only`.
   - For finance, run `/Users/jackie/.codex/skills/financial-market-signal-draft/scripts/check_finance_policy.mjs` on title, body, captions, and tags.
   - Reject the whole finance topic on a policy hit; do not sanitize and reuse it.
   - Check exact brand `白Yu观测`, no raw HTML lists, no old spaced brand, no duplicate body, no hype tags, and no finance disclaimer in research. Public-page verification must read the first page `<body>` through the shared duplicate-body-safe helper because browser extensions can inject a second `<body>`; validate the installed LaunchAgent runtime copy as well as the workspace source.
   - Confirm every local image exists and is readable before opening the editor. For PDF-backed research, confirm the intended ordered prefix appears exactly once and any omitted tail is recorded.
   - After import, require native heading nodes such as the editor's actual `<h2>` or `<h3>` blocks, the expected image count, and no literal Markdown markers such as `##` or `**` in the editor DOM. Do not hard-code only one heading level when the imported DOCX visibly renders native headings.
   - An editor `<img>` count is not upload evidence. Before `发布` or `更新`, require every expected image to be loaded at a nonzero natural size and resolved to a stable HTTPS Zhihu image resource (`zhimg.com`) for three consecutive probes. Treat `data:`, `blob:`, local/external source URLs, loading/progress/error wrappers, or a changing resource set as not persisted. Wait up to the configured bounded upload timeout; if the gate still fails, stop as `imported-not-submitted` and record the draft/article ID when present.

4. Publish in Chrome.
   - For Daily Scheduled/unattended runs, the Scheduled worker must only package and enqueue one self-contained platform trigger with `/Users/jackie/Documents/paper daily/automation/local-publisher/prepare-trigger.cjs`. The installed `com.openai.codex.baiyu-local-publisher` LaunchAgent performs all 9223 browser actions. The Scheduled worker and an interactive conversation must not operate Chrome or import a DOCX as a fallback.
   - Before any browser action, read and follow `/Users/jackie/Documents/paper daily/automation/platform-publisher/BROWSER_SESSION_CONTRACT.md`. Scheduled/unattended runs use only the verified 9223 route; do not automatically fall back to the normal Chrome extension. The extension route is allowed only when the user explicitly hands off an already-open Zhihu tab, and that run must not switch routes. Require final cleanup evidence.
   - Use `/Users/jackie/Documents/paper daily/automation/platform-publisher/run-platform-publisher.sh` with a prepared job. Run it without `--send` first, then reuse the same job with `--platform zhihu --send`; do not recreate the browser sequence ad hoc.
   - Prefer the logged-in Chrome/CDP session on `127.0.0.1:9223`.
   - Require that `9223` belongs to `/Users/jackie/Library/Application Support/Google/Chrome Codex Debug 9223`; login state belongs to the profile, not the port. If closed, use `/Users/jackie/Documents/paper daily/automation/platform-publisher/start-platform-debug-chrome.sh`. Do not initialize a substitute profile and infer that the account logged out.
   - Probe `/json/version` with both `curl --noproxy '*'` and the bundled Node `fetch` from the same execution context that will run the publisher. If both return HTTP 200, continue the real publish attempt and do not reuse an earlier `EPERM` as the current blocker. If Chrome is listening but this exact context still returns `EPERM`, classify it as an execution-environment permission failure, not a closed port, logout, or platform failure.
   - Open `https://www.zhihu.com/creator`.
   - Use the user's single default logged-in Zhihu account. Confirm Creator Center and `写文章` are available, but do not require a visible account-name match. The `/write` editor can be fully logged in while omitting the account name.
   - Wait briefly for a delayed promotional `Modal` to mount. If it intercepts the Creator Center, click its single visible `关闭` button once, then re-check the page before clicking `写文章`. Treat this as a recoverable UI overlay, not a platform rejection.
   - Choose `写文章`, keeping one claimed tab for the full operation.
   - Open the editor toolbar's visible `导入` menu, click the `导入文档` button, then use the import modal's native `.docx` file input. This two-step UI does not necessarily emit a browser file-chooser event. Do not paste or fill Markdown/plain text into the rich editor and assume it will render.
   - If import creates a draft article ID before final submission, record it and resume `/p/<draftId>/edit` on retry. Reuse the already imported native content when it passes integrity checks; do not open another new-article tab and create duplicate drafts.
   - When updating an existing article, focus the rich editor and clear it with native Select All and Delete before import. Do not use `fill('')`, because it can leave old image blocks behind.
   - Verify each native heading, image, and caption appears in canonical order. For an existing article or draft, stay on `/p/<id>/edit`. Prefer an initial visible `更新` control for an already published article. If only `发布` is present, one click may merely expand `发布设置`; while still on the same `/edit` URL, click the visible `发布` confirmation at most once more. If a final `更新` appears, click it; if Zhihu instead returns directly to the exact same `/p/<id>` and visibly reports `发布成功`, accept only that same-ID transition as the submit event. In every branch, the public title/headings/full unique visible image count must still pass before recording the update. A different ID is a duplicate and must fail.
   - Before any `发布` or `更新`, open the editor's `创作声明` selector and require the visible selected value `包含 AI 辅助创作（作者对内容负责）`, following Zhihu's AI-assisted-content policy. Missing, ambiguous, or unverified selection is a hard stop; do not submit and do not replace the platform declaration with free-text disclosure in the article body.
   - For repair audits, a `verifyOnly` job may open the exact existing public URL and run the same title/heading/image integrity gate without opening the editor, importing, or submitting.
   - Review title, headings, body, images, source notes, account, and finance policy status.
   - Click the true publish control only when authorized. A draft, editor state, or click is not publication evidence.

5. Verify and record.
   - Accept only a success page, a fresh matching content-management record, or a public article URL/status as evidence.
   - Verify the public article contains native heading nodes and the expected images and contains no literal `##` or `**`. An editor-only check is insufficient.
   - If public verification fails after a submit click, retain the exact article ID, public URL, expected/observed heading counts, and expected/observed image counts in the result/state. Repair only through `/p/<id>/edit`; never open a parameterless new-article page for correction.
   - If Zhihu shows `近期发布频率过高，请24小时后重试`, stop that article as `ZHIHU_PUBLISH_RATE_LIMITED`, record the exact article/draft ID and `retryAfterHours=24`, and do not click again or retry any remaining Zhihu submissions inside that 24-hour window. This is a platform hard block, not a recoverable network retry and not publication evidence.
   - Never accept a `/p/<id>/edit` URL as publication evidence. After submission, open `/p/<id>`, require the intended title, author/account, native headings, and expected article images, then record that public URL.
   - Record account, title, time, article URL or ID, image count, status, and any review state in `zhihu-article.md`.
   - Retry recoverable proxy, timeout, connection, 429, or 5xx failures with increasing delay and page-state checks.
   - Stop on explicit rejection, missing files, unavailable creator capability, or human verification.
   - Keep `CDP_UNAVAILABLE`, pre-import script/runtime failure, human-verification stop, imported-not-submitted, and verified review/published status separate.

## Checklist

- The user's single default Zhihu account is active and `写文章` is available; no visible account-name match is required.
- The article is one canonical research or finance article, not a mixed topic.
- Research is full-text-backed and includes figure, method, evaluation, and limitation evidence.
- Finance passed the policy scanner and contains no prohibited service or recommendation.
- Images are readable, ordered, captioned, and aligned with the article; computer-research images are direct original-paper screenshots with page/Figure/Table provenance.
- A real publish or review-management record is captured.
