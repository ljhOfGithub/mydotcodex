---
name: wechat-daily-signal-publisher
description: Preserve the permanent 白Yu观测 WeChat publishing pause. WeChat/135 artifact generation, draft work, recovery, browser work, API calls, and submission stay disabled until the user explicitly restores them.
---

# WeChat Daily Signal Publisher

## Permanent publication pause — highest priority

The user permanently paused WeChat/Official Account/135 work on 2026-09-30. Until the user explicitly says “恢复微信” or “恢复公众号”, every scheduled slot, same-day catch-up, historical recovery, repair, and verification must record the WeChat cell as `publication-paused-by-user` with `actions=0`.

- Do not generate, validate, or adapt WeChat HTML, covers, preview assets, jobs, bundles, or triggers.
- Do not open or control a browser, 135 Editor, or the WeChat backend; do not upload, edit, sync, save drafts, preview, group-send, publish, verify, retry, or recover.
- Do not call the legacy WeChat API or consume an existing queued/recovery trigger.
- Preserve historical files, drafts, URLs, IDs, results, and state as evidence only. Do not delete, modify, backfill, or describe them as new work.
- This gate overrides every workflow, recovery, real-publish, legacy API, and batch-completeness instruction below. The material below is retained only as dormant reference for a future explicit restoration.
- Restoration is valid only after this skill, the automation prompt, `prepare-trigger.cjs`, the LaunchAgent worker, and the platform-publisher CLI gate are updated together.

## Hard content scope

WeChat is computer-research-only for `白Yu观测`. A finance or mixed article is `not-applicable-by-user`: do not generate WeChat HTML, a cover, a `wechat135` job/trigger, a 135 browser action, draft recovery, or historical catch-up. Do not count the skipped WeChat cell as a failure or omission. This gate can change only after the user explicitly restores finance publishing to WeChat.

## Core stance

Save evidence-first research drafts for "白Yu观测". Use 135 Editor's third-tab `插件同步` route as the sole default path for creating or updating WeChat drafts; do not silently fall back to the 135 direct save-dialog sync or the direct WeChat API. By default, WeChat behavior is draft-only: prepare or update the public-account draft, but do not execute real publish/group-send/freepublish unless the user explicitly overrides this rule for the current run. For domain writing, use:

- `computer-research-signal-draft` for computer-science-only research articles.

## Workflow

1. Confirm the run context.
   - Use the user's current date/time and timezone; for "today/latest", verify live information because papers, prices, markets, and policies drift quickly.
   - Clarify whether the user wants a local draft, a WeChat draft/preview, or final publish. If unclear, stop at draft/preview.
   - When this skill is used for the `白Yu观测` daily routine, treat WeChat as draft-only unless the current user message explicitly restores real publish behavior.
   - Treat the existing 135 authorization as valid when the user has confirmed it or the 135 account selector exposes the intended linked account. Do not proactively reopen the authorization page on every run.
   - Never request or store passwords, cookies, tokens, or recovery codes.

2. Route domain writing.
   - For computer science research only, use `computer-research-signal-draft`.
   - Reject finance and mixed articles before generating WeChat artifacts.
   - Do not silently add finance content to a research article.

3. Review the prepared post.
   - Preserve source evidence, labels, disclaimer, and local artifact paths.
   - Do not upgrade evidence strength because an item sounds important.
   - Use reviewed `.html` as the sole 135 body source. Do not pass Markdown, DOCX, plain text, or a bare Markdown conversion to 135.
   - Put every presentation-critical rule inline on elements inside `<body>`. The 135 handoff extracts body content and does not reliably preserve a `<head><style>` stylesheet.

4. Draft for "白Yu观测".
   - Use a precise research title. Keep the first paragraph useful on its own: what the paper asks and why its evidence matters.
   - Suggested structure:
     - 标题
     - 论文与问题
     - 计算机科研信号
     - 图怎么读
     - 方法、实验、限制与结论
     - 后续观察
     - 科研阅读笔记说明，不加入投资建议免责声明。
   - Use a restrained mobile HTML system: warm-white background; one body wrapper no wider than 760px; title 22-24px with line-height about 1.4; body 16px with line-height 1.75-1.9; section headings around 18px with a consistent accent; captions 12-13px gray; images `width:100%;height:auto;display:block`. Prefer spacing, thin rules, and at most one subtle background tone over decorative cards.
   - Inline these styles on the body wrapper, headings, paragraphs, images, and captions. A stylesheet that exists only in `<head>` fails the layout gate even if the local browser preview looks correct.
   - Avoid exaggerated certainty, clickbait, unsupported causal claims, and confidential information.
   - Treat layout as Codex's responsibility before the 135 handoff. Do not rely on 135 AI generation or one-click layout to replace the reviewed mother draft.
   - Avoid raw `<ul>/<li>` bullet lists in Chinese public-account prose. They often render as messy dots with awkward punctuation. Use short numbered rows, compact cards, or separate paragraphs instead.
   - Avoid list items ending with repeated semicolons or mixed punctuation. Prefer complete short sentences.
   - For computer-research posts backed by a PDF, render original pages in order and keep the article as one draft. If the verified article-image/API limit cannot accept all pages, insert only the ordered prefix that fits and omit the tail; do not create a second draft for overflow pages. Record `pdf_pages`, `uploaded_pages`, `omitted_pages`, and `visual-truncated`, and never describe a truncated image set as the full PDF. Do not create summary cards, redraw figures, synthesize diagrams, or generate AI images.
   - Only scale or add neutral padding when needed for readability. Do not crop paper content, alter paper data, or overlay generated summaries. Record every page number and keep the written figure-reading explanation in the article.
   - Use the exact brand spelling `白Yu观测` in titles, body labels, source notes, and explicit `--author` overrides. If `.env` may contain an older author value, pass `--author 白Yu观测` on draft update/add commands.
   - Use a research-note/source-version note; do not add investment-advice wording.

5. Save through 135 Editor.
   - Default every new `wechat135` job to `syncMode: "plugin"` and `pluginAction: "sync"`, including jobs that omit both fields. Use `syncMode: "direct"` only when the user explicitly requests the old 135 direct save-dialog route for that run. Never infer direct mode from a missing field or a plugin failure.
   - For Daily Scheduled/unattended runs, the Scheduled worker must only package and enqueue one self-contained `wechat135` trigger with `/Users/jackie/Documents/paper daily/automation/local-publisher/prepare-trigger.cjs`. The installed `com.openai.codex.baiyu-local-publisher` LaunchAgent performs all 9223 browser actions. The Scheduled worker and an interactive conversation must not operate 135 or upload as a fallback.
   - On the editor page, if the visible overlay says `此操作会覆盖当前排版内容`, click `不再提醒` or `不再提示`, then click the overlay's `确定` before locating or writing the editor. Do not treat this known overlay as a hidden editor or browser-security failure.
   - Use the user's logged-in Chrome and open `https://www.135editor.com/beautify_editor.html`. Reuse the current editor tab when it already contains the target article.
   - Load the reviewed WeChat-ready HTML as rich text. Require a `.html` file whose body keeps inline styles. If HTML-file import is unavailable or requires a paid tier, use rich-text paste; do not degrade the article to raw HTML, Markdown, DOCX, or plain text.
   - Verify the title, exact brand `白Yu观测`, section structure, disclaimer policy, body-image count, and absence of raw markup before saving. After inserting HTML into 135, wait until every intended body `<img>` reports loaded with a non-zero natural width before opening `保存同步`; do not let the plugin capture a text-only intermediate state.
   - In explicitly requested `syncMode: "direct"` only, open `保存同步`, set the title and author, and upload a valid cover through the cover control inside the same `保存图文` dialog. Require that exact dialog to expose one unambiguous cover file input, accept exactly one file, and complete the visible cover-crop flow. If the dialog still shows an unset cover, the crop flow never opens, or 135 reports `封面图片网址错误` / error code `-1`, stop without saving or syncing; never submit an empty, local-only, `blob:`, or otherwise unverified cover URL to WeChat.
   - In explicit direct mode, after the cover is ready, find the `同步` section in that same `保存图文` dialog, select the exact linked `白Yu观测` account, verify its checkbox remains selected, and click `保存文章`. Wait for `已成功同步到微信`; do not automatically enter the separate `同步公众号` article list. That list is recovery/verification-only after an exact-title duplicate check.
   - In the default plugin route, before opening 135's third tab, ensure exactly one eligible blank WeChat article editor exists. When there is none but a logged-in `草稿箱` list page exists, use `新的创作 → 文章` to open one; draft-list/home/history tabs are not editors and must not be counted as blank editors. Stop if blank editors remain ambiguous. Before opening the 135 plugin panel, fill that exact blank editor's title field with the target title and verify it is retained; this is target disambiguation only and is not a save or draft success. On a recovery run, reuse one exact-title editor only when all visible editor bodies contain no images and no text beyond the exact target title or `从这里开始写正文`; if it contains substantive body content, stop for inspection rather than opening another same-title editor. Before plugin enumeration, close only safe stale WeChat pages that occur before the target editor and are either an `action=list_card` draft-list page or an `isNew=1&type=10` page whose visible body still says `请重新登录`, and only when they expose no visible title editor. Preserve every titled editor, any substantive body, home/history pages, the target editor, and unrelated tabs; record closed draft-list/relogin counts. Then open the third `插件同步` tab and interpret each `公众号-网页N-标题` entry as the left-to-right order of plugin-visible WeChat backend tabs, as stated by the panel itself. If a preserved plugin dialog is already open but lacks the newly primed exact title, switch its unique visible `保存同步` tab once, then return to `插件同步` once so the extension re-enumerates tabs; do not attempt to close the Bootstrap modal or use DOM click. A trusted `force:true` fallback is allowed only after normal Playwright actionability timeout while that exact tab remains visible and enabled. Resolve exactly one row whose displayed title equals the target article title. When the plugin incorrectly displays multiple rows as `暂无标题`, an ordinal fallback is allowed only after independently re-finding one exact-title, empty backend editor, calculating its current live WeChat-tab ordinal after safe cleanup, and verifying that the plugin rows are a unique contiguous sequence starting at webpage 1 and include that ordinal as `暂无标题`; record the fallback reason as `verified-live-ordinal`. If any of those checks fail, stop as ambiguous. Never infer a target ordinal from a WeChat tab that the plugin does not list. Click only that row's adjacent `一键同步` control; the title row itself is not a selection control. Clicking `一键同步` proves only transfer to that editor, not a saved WeChat draft. Verify the target backend editor received the intended title/body, then save and verify the WeChat draft separately.
   - Open `新的创作` and its `文章` item with trusted browser clicks, registering the new-page listener before the article click. If the normal trusted click times out only on Playwright actionability while that exact control remains visible and enabled, allow one bounded `force: true` Playwright click; never force a hidden/disabled control and never fall back to DOM `element.click()` for these navigation actions. Accept either a new tab or same-tab navigation. On every new-page poll, check the page before looking for an editor. When the page shows `请重新登录`, require exactly one visible `<a id="jumpUrl">登录</a>` whose destination path is `/cgi-bin/loginpage`; the user has authorized one trusted click on that exact link because their WeChat client remains logged in. Never click the non-actionable `请重新登录` heading itself. Wait up to 30 seconds for the same page to resume. If it returns to `/cgi-bin/home`, use only that page's fresh session token to navigate the same tab to the draft-list route, then repeat `新的创作 → 文章` once; reject a second relogin loop. Do not activate Chrome or use a different browser/profile for this recovery. If the click reveals QR/CAPTCHA/mobile verification, or any verification marker is visible before or after the click, classify it as `HUMAN_VERIFICATION_REQUIRED`, preserve the page, and stop. Otherwise wait up to 60 seconds for the title editor to mount. Recognize only visible input/textarea and title-labeled contenteditable variants; hidden duplicate title controls do not count. If login recovery, a navigation click, or unique blank-editor detection still fails, record its exact stage, click method, visibility/enabled state, sanitized page counts, whether a new page was observed, page/frame paths, and relevant creation controls, and use a Playwright screenshot of the actual failed WeChat page when it remains open. Do not emit an unqualified `details:null` failure or treat an unrelated desktop screenshot as platform evidence.
   - In the verified plugin route, the primed target title makes 135's `onekeTb` show a native `该公众号编辑器中存在内容，是否覆盖？` confirmation even when the body is otherwise empty. Accept only that exact confirm, and only after the unique exact-title backend editor was independently re-verified to have no substantive body or images; dismiss and stop on every other dialog. The plugin may open a second editor with the same title instead of replacing the primed placeholder. After transfer, wait up to 90 seconds for delayed imports and identify the target by content evidence: exactly one same-title editor must contain one branded body and exactly the source editor's loaded image count. Other same-title editors may be closed only when every visible body contains no images and no text beyond the exact title or `从这里开始写正文`; preserve and stop on any non-empty duplicate. On a retry, if this exact completed-transfer state already exists, skip another plugin transfer, revalidate its image count against the current 135 source, close only verified empty placeholders, and continue with cover/save. A click or title-only editor is `WECHAT135_PLUGIN_TRANSFER_NOT_COMPLETE`, not a transferred draft. If the backend cover is empty, use its `从正文选择` flow only when there is exactly one eligible body image: choose that image, click the unique `下一步`, then accept the unique final `确认` or `完成`. A background tab may keep the unique menu link CSS-hidden; after validating one empty cover area and one body image, invoking that sole attached link is allowed. Require a visible non-empty WeChat CDN cover preview before saving. Finally click only `#js_submit`'s exact `保存为草稿`; never click `发表`.
   - Do not count `快速保存`, `保存文章`, a cover upload, a selected checkbox, a transfer, or a click as a WeChat draft. For direct 135 sync require `已成功同步到微信`; for the verified plugin/backend route require a successful WeChat save response, visible `已保存`/`保存成功`, and a returned `appmsgid`/`media_id`. Otherwise require a preview link or an exact matching new record in `公众号文章 → 微信草稿`. Close the exact backend editor only after this evidence is captured; preserve it on every failure so a bounded retry can inspect state before changing anything.
   - When updating an existing WeChat draft, open it from `公众号文章 → 微信草稿`, preserve its identity when the UI supports update, and verify that no duplicate draft was created.
   - If 135 is logged out, loses the linked account, or requests QR/CAPTCHA/2FA/administrator confirmation, stop and report the exact blocker. Do not bypass verification and do not repeatedly reopen authorization after the user has already confirmed it.
   - When a visible QR/CAPTCHA/verification-code/2FA/mobile-binding/administrator-confirmation prompt requires the user, preserve the registered 135 verification page for manual takeover instead of closing it during cleanup. Record `humanVerificationRequired=true` and `preservedForHumanVerification`; do not continue automatically after the user acts unless a new authorized retry checks the current draft/editor state first.
   - Preserve the registered 135 task page on every WeChat failure, including ordinary selector, overlay, crop, save-dialog, article-selection, timeout, and final-sync verification failures. Record `pagePreservationRequested=true`, `cleanup.preservedRegistered`, and `cleanup.preserveReason=wechat-failure` (or `human-verification`). Close the registered 135 page only after a verified draft success. A later retry must inspect the preserved editor/dialog and WeChat draft records before changing or submitting anything, to avoid duplicates.
   - Before saving, verify that the visible title and author fields actually retain the intended values. In an explicitly authorized recovery-only use of the separate `同步公众号` list, select the exact target article and require the visible selection count to be at least one before clicking `同步到微信公众号`. If a 135 promotional overlay intercepts the cover crop or save controls, close that visible overlay first; do not force-click through it.
   - If 135 fails, record the local 135 article state and the hard blocker. Do not silently switch to the direct API.

### Real-publish boundary

- 135 `保存同步` creates or updates a WeChat draft; it is not publication.
- Current official 135 guidance for WeChat's non-push `发布` still requires opening the WeChat Official Account backend, finding the draft, clicking `发布`, and completing the WeChat confirmation/scan. Do not call a 135-local save or preview a published article.
- 135 also documents `定时群发`, which is a real fan-facing group send. It requires a WeChat-verified account authorized to 135 and has feature limits such as no original declaration. Never use `定时群发`, `立即群发`, or `48小时群发` in the daily draft workflow.
- A vague request to “发布” does not authorize group send. Require explicit current-turn authorization naming the intended action and account before any real publish or group send, then re-verify the current official requirements because platform behavior can change.
- Official capability references to re-check when real publication is requested:
  - `https://www.135editor.com/books/chapter/1/797`
  - `https://www.135editor.com/books/chapter/1/41`

### Legacy direct API path — explicit opt-in only

- Do not use this path in the daily automation or as an automatic 135 fallback. Use it only when the user explicitly asks to test or restore the legacy direct API route.
- For `/Users/jackie/Documents/mediePlatform`, run every real WeChat API command through `scripts/run-wechat-direct.sh`. Do not invoke `node src/cli.js ... --send` with inherited global proxy variables.
- When the user has instructed that an unavailable `9223` path should bypass Clash, call the same wrapper with `WECHAT_SKIP_CLASH=1`. In this mode the wrapper must not query or change the Clash socket; it only removes proxy variables from the child process. Continue to classify a resulting `40164` as a direct-exit-IP whitelist blocker rather than a Clash-control failure.
- Before uploading media or saving a draft, require Clash Verge `rule` mode and the active rules `DOMAIN,api.weixin.qq.com,DIRECT`, `DOMAIN,file.api.weixin.qq.com,DIRECT`, and the WeChat domain-suffix DIRECT rules. TUN may remain enabled: the verified successful path used `rule + TUN`, with only WeChat traffic routed as `DIRECT`.
- WeChat validates the public direct出口 IP, not the local interface or proxy rule name. A home/ISP public IP can change even when the DIRECT rules are correct. When strict-direct token returns `40164`, compare the rejected IP with the last confirmed whitelisted direct IP; a changed IP requires a whitelist update before retries can succeed.
- Once routing is direct, use this fixed sequence from the previously successful run:
  1. `run-wechat-direct.sh node src/cli.js token` and require a valid `expires_in`.
  2. Upload the cover/body images and record returned IDs/URLs.
  3. Run `draft:add` or `draft:update` with `--html --author 白Yu观测 --send`.
  4. Record the returned draft `media_id`; do not call `publish:submit` in draft-only mode.
- The wrapper changes only the child process environment. Never change the user's global proxy settings automatically and never print proxy values, credentials, access tokens, cookies, or secrets.
- Read `references/successful-direct-api-path.md` when diagnosing WeChat network or `40164` failures.

6. Leave an audit trail.
   - Save the final Markdown draft and source notes in the current workspace or a user-specified folder.
   - Include source URLs, retrieval errors, evidence labels, and whether the result was local draft, WeChat draft/preview, or published.
   - Report the exact local file path and browser outcome to the user.

### Batch completeness gate

- Maintain a seven-row WeChat ledger for the seven computer-research slots. The five finance rows are `not-applicable-by-user` and must have zero WeChat artifacts, jobs, triggers, browser actions, or draft retries.
- Each row must contain the article title, HTML path, cover path, 135 action (`135-sync-create` or `135-sync-update`), result, and returned `media_id`.
- An existing draft counts only when its target title and `media_id` are recorded. A local HTML file, editor save click, API command invocation, or pending status does not count as a confirmed draft.
- Do not report the daily WeChat routine complete unless all due research rows have confirmed draft evidence or each missing row names a concrete hard blocker.
- WeChat draft failure does not invalidate successful Xiaohongshu or Douyin posts, but platform totals must always be reported independently.
- A `40164 invalid ip ... not in whitelist` belongs only to the legacy direct API route. It is not a reason to abandon the default 135 workflow or ask the user to change the IP whitelist.

## Validation checklist

Before finishing, verify:

- Candidate JSON or equivalent source records were read for paper selection.
- Paper claims are based on readable PDF/HTML full text unless explicitly marked `abstract-only` or `listing-only`.
- Finance and mixed articles were rejected before WeChat artifact generation.
- Every key claim has a source or an explicit evidence label.
- Research-only content does not include investment-advice wording.
- The 135 sync target is the user's intended linked account; for this workflow it should be `白Yu观测`. Do not reopen authorization merely to re-prove a user-confirmed binding.
- No credentials, tokens, private messages, or unrelated browser state were copied into the post.
- Finished WeChat HTML contains no accidental `<ul>` or `<li>` bullet lists unless the user explicitly wants bullets.
- Finished WeChat HTML has no old brand spelling `白Yu 观测`.
- PDF-backed computer-research posts preserve original page order in one draft. Any page-limit truncation records uploaded and omitted ranges; summary/redrawn/AI-generated research images are forbidden.
- Source notes record body-image local paths and WeChat URLs.
- Finished HTML uses inline body styles; a `<head><style>` block alone is insufficient because it is not part of the extracted 135 body.
- Unless the user explicitly overrode it in the current run, the final WeChat state for `白Yu观测` is draft/preview only, not published.
- Each research row uses the default plugin/backend route unless explicitly configured `syncMode: "direct"`. Due research rows have confirmed `media_id`/`appmsgid` values or explicit per-row hard blockers; `已成功同步到微信` applies only to the explicit direct route.
