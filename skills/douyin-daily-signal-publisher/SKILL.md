---
name: douyin-daily-signal-publisher
description: Prepare and publish compliant "白Yu观测" financial-market observations to Douyin through the user's default logged-in Chrome account. Computer-research articles are excluded by user policy.
---

# Douyin Daily Signal Publisher

## Hard content scope

Douyin is finance-only for `白Yu观测`. A computer-research article is `not-applicable-by-user`: do not create a Douyin adaptation, post file, slideshow, job, trigger, browser task, upload, draft, submission, retry, or historical catch-up. Do not count this skipped cell as a failure or omission. This gate applies before dry-run and browser work and can be removed only after the user explicitly restores computer-research publishing to Douyin.

## Core stance

Publish compliant financial-market observations for "白Yu观测", not short AI-generated promos.

Douyin is a redistribution surface. Treat the WeChat/public-account article as the canonical source when it exists. Convert the format, not the argument.

## Workflow

1. Confirm scope, account, and permission.
   - Use `chrome:control-chrome`; Douyin publishing depends on the user's logged-in Chrome session.
   - Use `https://creator.douyin.com/` or `https://creator.douyin.com/creator-micro/content/upload`.
   - Use the user's single default logged-in Douyin account; do not require a visible account-name match. The content brand remains `白Yu观测`.
   - Confirm the full creator dashboard and `发布图文` function are available. If a real login/QR/CAPTCHA/phone prompt appears, stop; an avatar menu that merely lists `身份认证` or `退出账号` is not by itself a verification prompt.
   - If Chrome asks for login, CAPTCHA, QR scan, 2FA, real-name/phone confirmation, account switch, or sensitive confirmation, stop and ask the user to handle it.
   - If the browser tab or Chrome process crashes mid-run, reopen Chrome and the Douyin creator page, then re-check account, publish format, uploaded assets, and draft state before continuing. If the reopened session shows login or verification prompts, stop.
   - Default to the action the user requested. For scheduled routines where the user has already authorized real publishing, publish after validation. For trial runs without explicit publish permission, stop at draft/package.

2. Preserve the source article.
   - Use the WeChat/public-account article as the canonical source. Douyin should be a same-content compact edition, not a separate short-video script.
   - Preserve title keywords, section order, factual claims, uncertainty language, and conclusion.
   - If Douyin character limits force compression, remove ornamental transitions first. Do not remove method, evaluation, figure interpretation, or limitations before removing general framing.

3. Enforce deep-reading quality.
   - Reject any computer-research source before artifact generation.
   - Avoid generic AI-sounding phrases: "在当下快速发展的时代", "打开新思路", "值得每个人看看", "干货满满", "一文看懂", "颠覆认知", "建议收藏".
   - Prefer precise verbs: `构造`, `比较`, `拆分`, `测量`, `验证`, `暴露`, `限制`. Avoid vague verbs such as `赋能`, `打通`, `重塑`, `升级范式` unless quoting the source.

4. Prepare Douyin artifacts.
   - Save under `reports/douyin/YYYY-MM-DD-topic/`.
   - Produce `douyin-post.md` with:
     - intended Douyin account,
     - platform title,
     - full compact body, not a short abstract,
     - restrained tags,
     - image/video upload order,
     - evidence note and validation checklist,
     - publish/edit result after browser operation.
   - Prefer image-text publishing when available.
   - For finance posts, reuse the single Xiaohongshu 3:4 pure-text image: small brand/time line, factual headline, 2-4 compact paragraphs, and `来源：金十数据｜时间：...` footer.
   - Prohibit finance carousels, icons, charts, candlesticks, diagrams, flow arrows, photos, illustrations, data tiles, and separate infographic modules. Keep attribution and uncertainty; if text is crowded, shorten the image and retain detail in the body instead of adding images.
   - If the web UI only supports video upload, create a 9:16 slideshow MP4 from the same single finance card and record the fallback.

5. Validate before upload.
   - Confirm body length fits Douyin and is not silently truncated.
   - Confirm the body does not accidentally concatenate an old short summary with the full body.
   - Confirm no old brand spelling `白Yu 观测`, raw HTML list tags, finance disclaimer in research-only posts, platformized tags, or unrelated market/research mixing.
   - Confirm the source is finance and no research-PDF page set is present.
   - For finance notes, run `/Users/jackie/.codex/skills/financial-market-signal-draft/scripts/check_finance_policy.mjs` on the final title/body file and card text sources. Any hit is a hard stop: do not upload or sanitize the same topic; return to candidate selection and use the next eligible article.
   - Confirm the finance source note contains a current `jin10.com` URL, displayed timestamp, and any verified original-source URL.
   - Visually inspect the reused finance PNG before upload. Require exactly one image, visible brand text exactly `白Yu观测`, a legible `来源：金十数据｜时间：...` footer, and no icons, charts, arrows, photos, illustrations, data tiles, boxed modules, or extra carousel images. A compliant prompt or source text file is not visual proof.

6. Publish or save.
   - For Daily Scheduled/unattended runs, the Scheduled worker must only package and enqueue one self-contained platform trigger with `/Users/jackie/Documents/paper daily/automation/local-publisher/prepare-trigger.cjs`. The installed `com.openai.codex.baiyu-local-publisher` LaunchAgent performs all 9223 browser actions. The Scheduled worker and an interactive conversation must not operate Chrome or upload as a fallback.
   - Before any browser action, read and follow `/Users/jackie/Documents/paper daily/automation/platform-publisher/BROWSER_SESSION_CONTRACT.md`. Scheduled/unattended runs use only the verified 9223 route; do not automatically fall back to the normal Chrome extension. The extension route is allowed only when the user explicitly hands off an already-open Douyin tab, and that run must not switch routes. Require final cleanup evidence.
   - Use `/Users/jackie/Documents/paper daily/automation/platform-publisher/run-platform-publisher.sh` with a prepared job. Run it without `--send` first, then reuse the same job with `--platform douyin --send`; do not recreate the browser sequence ad hoc.
   - For CDP `9223`, require `/Users/jackie/Library/Application Support/Google/Chrome Codex Debug 9223`; the port alone does not preserve login state. If closed, use `/Users/jackie/Documents/paper daily/automation/platform-publisher/start-platform-debug-chrome.sh`. Do not fall back to a newly initialized profile and misreport prior logins as expired.
   - Probe `/json/version` with both `curl --noproxy '*'` and the bundled Node `fetch` from the same execution context that will run the publisher. If both return HTTP 200, continue the real publish attempt and do not reuse an earlier `EPERM` as the current blocker. If Chrome is listening but this exact context still returns `EPERM`, classify it as an execution-environment permission failure, not a closed port, logout, or platform failure.
   - In `发布图文`, use the native multiple image input whose accept list begins with `image/png,image/jpeg`; set all ordered images once. The visible button is currently named `上传图文`, not `上传图片`.
   - Fill the platform title and full compact body from `douyin-post.md`.
   - Confirm the visible preview uses content brand `白Yu观测`; do not block on a visible account-name label when the creator capability is available in the user's single default session.
   - After any browser reopen, re-verify that the current work is still the intended draft/post and that title, body, cover, and upload set have not been reset before clicking `发布`.
   - For real publish requests, click the true `发布` button, not `暂存离开`.
   - For draft/trial requests, do not publish unless the current user request clearly authorizes it.
   - After submit, verify `已发布`, `审核中`,作品管理 visibility, or another concrete platform state. If an edit shows `修改审核中`, record that public text may not have updated yet.
   - Do not accept the title remaining in the publish editor as submission evidence. Require navigation to content management plus a fresh matching title record, then record that record's `审核中` or `已发布` state.
   - If navigation reaches content management but the fresh title is not visible within the first wait, reload content management once and wait again before declaring submission unverified. Never click publish again merely because the list is delayed.
   - Record `CDP_UNAVAILABLE`, pre-upload script/runtime failure, human-verification stop, `uploaded-not-submitted`, and verified review/published status as distinct outcomes.

7. Leave an audit trail.
   - Record account name, title, body length, upload count, publish/edit state, visible time, and any platform blocker.
   - If the post was edited after publication, record both the submitted edit and whether the public listing has updated.

## Validation checklist

Before finishing, verify:

- The user's single default Douyin account is active and creator capability is available; no visible account-name match is required.
- Content brand is exactly `白Yu观测`.
- The body is a compact deep-reading note, not a short abstract.
- Computer-research content is absent and recorded as `not-applicable-by-user` before artifacts or browser work.
- No credentials, cookies, tokens, private browser data, or unrelated tab data were copied.
- Final publish only happened when authorized by the current request or the configured routine.
