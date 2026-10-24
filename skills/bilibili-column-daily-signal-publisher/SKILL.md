---
name: bilibili-column-daily-signal-publisher
description: Preserve the paused 白Yu观测 Bilibili publishing contract. Bilibili publication, recovery, FIFO consumption, browser work, uploads, and submission are disabled until the user explicitly restores them.
---

# Bilibili Column Daily Signal Publisher

## Permanent publication pause — highest priority

The user has permanently paused Bilibili publishing. For every new item, same-day gap, historical failure, edit, verification, or FIFO head, record `publication-paused-by-user` and stop before creating or adapting Bilibili artifacts, jobs, bundles, or triggers. Do not open Chrome, inspect management records, upload/import, save, submit, retry, or consume daily quota.

Freeze `/Users/jackie/Documents/paper daily/reports/bilibili/publish-queue.md` exactly as historical evidence. Do not append, delete, reorder, verify, recover, or backfill any FIFO item while paused. A paused Bilibili cell is a terminal non-applicable state, not an omission, failure, queued publication, draft, or successful publication.

The workflow below is dormant reference only. Do not execute any of it unless the user explicitly restores Bilibili publishing and the automation, skill, trigger preparer, worker, and adapter pause gates have first been updated together.

## Purpose

Publish the canonical 白Yu观测 article as a Bilibili column with readable figures and restrained formatting. Do not turn it into a video script or promotional feed post.

## Workflow

1. Confirm source, account, and authorization.
   - Use the WeChat article as the canonical source.
   - Run at all five daily finance times; research is included at the three core times.
   - The verified account is LV5. Bilibili currently allows LV4-6 accounts to publish at most five columns per day, so never attempt a sixth same-day submission.
   - Keep overflow articles in a FIFO queue under `reports/bilibili/publish-queue.md`; publish queued work before newer Bilibili columns on the next available day. Never drop or duplicate an article.
   - Use `chrome:control-chrome` and the logged-in Bilibili creator session.
   - Use the user's single default logged-in account. Confirm the creator manager and column capability are available; do not require a visible account-name or UID match.
   - Stop for login, QR, CAPTCHA, 2FA, phone, identity, account-switch, or sensitive confirmation.

2. Prepare the column.
   - Save under `reports/bilibili/YYYY-MM-DD-topic/bilibili-column.md`.
   - Build a DOCX import package with real heading styles and embedded images. Markdown remains a source artifact and must not be filled directly into the rich editor.
   - After DOCX selection, wait up to 90 seconds for large imports to reach the expected native heading and image counts. Do not fail on a fixed short delay, and do not lower the declared counts to make a partial import pass.
   - Validate the DOCX before import. On macOS Scheduled/LaunchAgent runs, do not invoke LibreOffice/`soffice` for visual QA: headless startup can abort in `RegisterApplication` and leave a system crash modal over later publisher windows. Use `qlmanage` Quick Look for a first-page visual check plus structural heading/image checks. If Quick Look is unavailable, record full-page visual QA as partial rather than passed; never fall back to `soffice` in that run.
   - Preserve title keywords, evidence chain, uncertainty, limitations, and conclusion from the canonical article.
   - Research columns must include paper identity, figure/table reading, method/system design, evaluation, limitations, and follow-up.
   - Finance columns must include source timestamps, evidence, counter-evidence, risks, and a platform-safe non-recommendation statement.
   - Use section headings and short paragraphs, then embed original research PDF pages in order in one native DOCX import package.
   - If the verified editor/import image limit cannot accept all pages, embed only the ordered prefix that fits and omit the tail; never create a second column for overflow pages. Record `pdf_pages`, `embedded_pages`, `omitted_pages`, and `visual-truncated`. Do not replace the pages with selected screenshots, create research summary cards, redraw figures, synthesize diagrams, or generate AI images.

3. Validate.
   - Require full text for research; do not publish `abstract-only` or `listing-only`.
   - Run `/Users/jackie/.codex/skills/financial-market-signal-draft/scripts/check_finance_policy.mjs` on every finance title, body, caption, and tag file.
   - Reject and replace the whole finance topic on a policy hit.
   - Check exact brand `白Yu观测`, no old spaced brand, raw HTML lists, duplicate bodies, unrelated tags, or hype wording.
   - Confirm the intended ordered PDF prefix is readable and locally available, appears exactly once, and any omitted tail is recorded.
   - After import, require native heading nodes, the expected image count, and no literal Markdown markers such as `##` or `**` in the editor DOM.

4. Publish in Chrome.
   - For Daily Scheduled/unattended runs, the Scheduled worker must only package and enqueue one self-contained FIFO-head trigger with `/Users/jackie/Documents/paper daily/automation/local-publisher/prepare-trigger.cjs`. The installed `com.openai.codex.baiyu-local-publisher` LaunchAgent performs all 9223 browser actions. The Scheduled worker and an interactive conversation must not operate Chrome or import a DOCX as a fallback.
   - Before any browser action, read and follow `/Users/jackie/Documents/paper daily/automation/platform-publisher/BROWSER_SESSION_CONTRACT.md`. Scheduled/unattended runs use only the verified 9223 route; do not automatically fall back to the normal Chrome extension. The extension route is allowed only when the user explicitly hands off an already-open Bilibili tab, and that run must not switch routes. Require final cleanup evidence.
   - Use `/Users/jackie/Documents/paper daily/automation/platform-publisher/run-platform-publisher.sh` with a prepared job. Run it without `--send` first, then reuse the same job with `--platform bilibili --send`; when `queueFile` is configured the runner must match the FIFO head before upload.
   - Prefer the logged-in Chrome/CDP session on `127.0.0.1:9223`.
   - Require that `9223` belongs to `/Users/jackie/Library/Application Support/Google/Chrome Codex Debug 9223`; the port is transport only and does not contain login state. If closed, use `/Users/jackie/Documents/paper daily/automation/platform-publisher/start-platform-debug-chrome.sh`. Do not substitute a fresh profile and report the resulting login page as an expired prior session.
   - Probe `/json/version` with both `curl --noproxy '*'` and the bundled Node `fetch` from the same execution context that will run the publisher. If both return HTTP 200, continue the real publish attempt and do not reuse an earlier `EPERM` as the current blocker. If Chrome is listening but this exact context still returns `EPERM`, classify it as an execution-environment permission failure, not a closed port, logout, or platform failure.
   - Use the user's single default logged-in Bilibili account. Confirm the creator manager and `专栏投稿` capability are available, but do not require account-name or UID matching.
   - Do not treat static account-setting text such as `实名认证` together with `已认证` as an active human-verification prompt. Stop only for an actual blocking login, QR, CAPTCHA, phone, 2FA, or confirmation UI.
   - Open `https://member.bilibili.com/platform/home`.
   - Enter `投稿`, choose the visible `专栏` or article entry, and keep one claimed tab.
   - The column editor lives in the `https://member.bilibili.com/york/read-editor?` iframe. Wait for that frame, import through its native `.docx,.md` file input, and verify native heading nodes and images inside the same frame before submission. Do not search only the outer creator-page DOM.
   - After clicking publish, read submission evidence inside the same editor frame. The success text `你的专栏已提交成功` may not appear in the outer creator-page DOM. Record it as submitted/reviewing until a management record or public URL appears.
   - For an existing column, first read its `rid`/article ID from the content-management record. Open `https://member.bilibili.com/platform/upload/text/new-edit?aid=<rid>&type=3&isNew=1`, confirm the editor iframe URL carries the same `aid`, then import the DOCX. The parameterless `/platform/upload/text/new-edit` route is a new-column editor and must never be used for an in-place correction.
   - Do not infer success from a pre-existing toast. After clicking `发布` on the `aid` editor, require a fresh `你的专栏已提交成功` state.
   - Publish only through the true submit control. A draft, upload completion, or click is not success evidence.

5. Verify and record.
   - Accept a submission-success page, review status, fresh matching content-management record, or public column URL as evidence.
   - Record account, title, time, column ID or URL, image count, category, tags, and status in `bilibili-column.md`.
   - Retry recoverable proxy, timeout, connection, 429, or 5xx failures with increasing delay and page-state checks.
   - Stop on explicit rejection, missing files, unavailable column capability, or human verification.
   - Keep `CDP_UNAVAILABLE`, pre-import script/runtime failure, human-verification stop, imported-not-submitted, quota deferral, and verified review/published status separate.
   - Record daily quota usage and queue position. A quota-deferred article is not a failure and must not be reported as published.
   - For an in-place update, confirm the management total did not increase, the same article ID remains, the management summary has no raw Markdown markers, and the public opus has native headings and the expected images. Record whether the update is `审核中` or `已通过`.

## Checklist

- The user's single default Bilibili account exposes the creator manager and column capability; no visible account-name or UID match is required.
- The column is one canonical research or finance article, not a mixed topic.
- Research is full-text-backed and includes figure, method, evaluation, and limitation evidence.
- Finance passed the policy scanner and contains no prohibited service or recommendation.
- Images are readable, ordered, captioned, and aligned with the column; computer-research images are direct original-paper screenshots with page/Figure/Table provenance.
- A real submit, review, or published management record is captured.
