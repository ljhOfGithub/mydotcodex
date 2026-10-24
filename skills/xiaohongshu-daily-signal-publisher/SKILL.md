---
name: xiaohongshu-daily-signal-publisher
description: Prepare evidence-first "白Yu观测" Xiaohongshu notes in the user's logged-in system Chrome, including sequential uploads, text/topics, and AI-content disclosure, then stop on the final draft page for the user to submit manually. Do not click publish or schedule publication.
---

# Xiaohongshu Daily Signal Publisher

## Manual-submit mode — highest priority

Xiaohongshu packaging and browser preparation are active again, but automated submission is disabled.

- Generate and validate Xiaohongshu artifacts, then use the verified system-Chrome route to upload images one at a time, fill title/body/topics, and select `笔记含AI合成内容`.
- Do not select `定时发布`, set a scheduled time, click `发布`/`定时发布`, or invoke any equivalent final-submit control.
- Stop only after the final page is visibly ready and the ordinary `发布` control is available. Return `ready-for-manual-submit`, `submitted=false`, and preserve that exact Creator Center page for the user.
- `ready-for-manual-submit` is not a saved platform draft, scheduled note, publication, review state, or public record. Do not relabel it.
- Every Xiaohongshu bundle and runtime job must carry `manualSubmit=true`; reject `manualSubmit=false` before browser work.
- Historical paused items remain untouched. Do not backfill or recover them unless the user separately identifies an exact item.
- The user's prior automation-detection reports remain a circuit breaker: on any automation/risk-control notice, stop immediately, preserve evidence, and do not retry automatically.

## Core stance

Publish evidence-first "白Yu观测" notes to Xiaohongshu without leaking credentials or private browser data.

This is the Xiaohongshu packaging and posting layer. For content creation, route first:

- Use `computer-research-signal-draft` for computer-science-only research notes.
- Use `financial-market-signal-draft` for finance-only market-signal notes.
- Use a user-provided finished draft when available.

Default to local artifacts followed by a manually submitted draft-page handoff. Automated final publication remains disabled even if a broader workflow says to publish.

Before handoff, open `添加内容类型声明` and select `笔记含AI合成内容`. Leave the ordinary immediate-publish mode unchanged so the user controls the last step.

## Workflow

1. Confirm scope and permission.
   - Use the user's current date/time and timezone. For "today/latest", verify live sources because papers, market prices, news, platform UI, and policy can drift.
   - Clarify only when the user wants local artifacts without browser preparation. Otherwise default to the manual-submit handoff and never automate the final submission.
   - Never request, copy, store, or print passwords, cookies, session tokens, recovery codes, or SMS/2FA codes.
   - If Chrome asks for login, CAPTCHA, phone verification, QR scan, account switch, or sensitive confirmation, stop and ask the user to complete it manually.
   - If the browser tab or Chrome process crashes mid-run, reopen Chrome and the Xiaohongshu Creator Center, then re-check account, publish mode, uploaded assets, and current draft state before continuing. If the reopened session shows login or verification prompts, stop.

2. Preserve editorial style before platform adaptation.
   - Treat the WeChat/public-account article as the canonical source when it exists. Xiaohongshu should be a same-content compact edition, not a parallel rewrite.
   - Preserve the source title by default. If Xiaohongshu title length forces shortening, keep the same keywords and order.
   - Preserve the source article's argument and evidence order. For research notes, convert the long-form sections into the fixed compact sequence `opening -> 📝一句话总结 -> 🔑关键方法 -> 💡核心创新 -> ⚠️限制与边界 -> 🧭结论和关键洞察`, without changing claims.
   - Before `🔑关键方法`, preserve or add `🎓 来源机构：<paper-listed affiliations>` and `🔍 背景难点：<source-grounded problem>` from the research mother draft. Do not infer institutions from funders, model names, repositories, or benchmark ownership.
   - Preserve source claims, terminology, uncertainty language, and evidence notes. Do not add new claims just because the platform format is different.
   - When the full article cannot fit in Xiaohongshu's body limit, compress the source paragraphs without moving omitted research analysis into generated image cards. State this as a compact edition in source notes when relevant.
   - Treat Xiaohongshu as a lightweight redistribution surface, not a different persona.
   - Preserve the WeChat/public-account draft's calm deep-reading voice, evidence labels, source framing, and explanatory order.
   - Use the reference-style functional markers `📝` `🔑` `💡` `⚠️` `🧭` and `1️⃣` `2️⃣` `3️⃣` for research-body navigation. Avoid other decorative emoji chains, clickbait, exaggerated hooks, meme wording, excessive rhetorical questions, viral tag formulas, or breathless short-line stacking.
   - Keep the title close to the source article unless a length limit forces compression.
   - Convert format, not substance: shorten paragraphs, respect the character limit, and create vertical cards, but do not turn a research note into social-media hype.
   - For technical research, keep figure explanation, method, evaluation, limitations, and follow-up tracking in the same intellectual order as the source article whenever possible.
   - Do not make the Xiaohongshu body a generic AI summary. It must still read like a serious reading note from someone who opened the paper.
   - Avoid generic AI-sounding phrases: "在当下快速发展的时代", "打开新思路", "值得每个人看看", "干货满满", "一文看懂", "颠覆认知", "建议收藏", "核心亮点如下".
   - Avoid empty signal wording by itself: "这篇论文提醒我们", "核心信号是", "不是 X 而是 Y" must be followed by concrete mechanisms, figures, metrics, or limitations from the source.
   - Prefer source-level verbs such as `构造`, `比较`, `拆分`, `测量`, `验证`, `暴露`, `限制`; avoid vague platform/AI verbs such as `赋能`, `打通`, `重塑`, `升级范式` unless quoting the paper.

3. Enforce deep-reading quality.
   - For research notes, the body and cards together must include at least:
     - one named figure/table/diagram and what the reader should inspect in it,
     - one method or system-design mechanism,
     - one evaluation metric, score dimension, benchmark, or result pattern,
     - one limitation, uncertainty, or follow-up question.
   - The body should include enough detail to stand alone if the user reads only the caption text. Cards can carry extra detail, but the body cannot be only a teaser.
   - If the body limit forces compression, keep the paper's causal chain: problem -> mechanism -> evidence -> limitation. Remove generic introduction before removing method/evaluation/limitation.
   - If a generated draft lacks figure interpretation, method, experimental evidence, limitation, one-sentence summary, or conclusion/key insight, revise it before opening Xiaohongshu.
   - For a research note, use this mandatory 800-1,000-character template under the current validator:
     - One opening paragraph beginning `今天给大家带来一篇关于...的新论文——《...》。`, followed by the task.
     - `🎓 来源机构：<paper-listed affiliations>` on one line.
     - `🔍 背景难点：<2-3 compact source-grounded sentences>` naming at least two concrete weaknesses or constraints of the prior/default approach.
     - `📝一句话总结` with exactly one non-empty line combining the task, core mechanism, and strongest scoped finding.
     - `🔑关键方法` with exactly `1️⃣` `2️⃣` `3️⃣`; explain mechanism and decision path rather than only naming components.
     - `💡核心创新` with exactly `1️⃣` `2️⃣` `3️⃣`; compare against prior/default practice.
     - Do not use an independent `📊实验效果` section. Integrate 2-4 decisive measurements into the relevant method, innovation, limitation, or key-insight sentence, retaining benchmark, baseline, metric, value/trend, and denominator caveat.
     - `⚠️限制与边界` with 2-3 numbered items; retain source-stated and inferred limits.
     - `🧭结论和关键洞察` with exactly two consecutive lines: `论文结论：<conclusion tied to the evaluated setting>` and `关键洞察：<what the evidence reveals and why it matters>`. Keep scope and external-validity caveats in `⚠️限制与边界`.
     - End with `🧭结论和关键洞察`. Do not repeat `论文：<full paper title>` because the opening already names the paper; requested topics are entered separately by the publishing workflow.
   - Reserve enough of the 1,000-character budget for the conclusion/insight/boundary block. Compress generic opening language and repeated result wording first.
   - Use exactly one blank line between top-level blocks. Within each compact section, put the heading and all items on consecutive lines: no blank line after the heading, no blank line between numbered/result items, and no whitespace-only line containing spaces or tabs.
   - Required layout example:
     ```text
     📝一句话总结
     这篇论文通过……，在……设置下揭示了……。

     🔑关键方法
     1️⃣第一项……
     2️⃣第二项……
     3️⃣第三项……
     ```
   - Reject a research body that replaces this template with uninterrupted essay paragraphs, generic WeChat headings, or a shortened abstract.
   - Do not turn the body into a teaser that tells readers to inspect the images for substance. The text must independently explain the method and evidence even when the original PDF pages are also uploaded.
   - If the hard body limit is lower than the target range, use the maximum permitted space efficiently: remove greetings, submission invitations, generic praise, and repeated conclusions before shortening source institution, background difficulty, method, experiment, or limitation content.

4. Prepare the Xiaohongshu package.
   - Save artifacts under a date/topic folder such as `reports/xiaohongshu/YYYY-MM-DD-topic/`.
   - Produce `xiaohongshu-post.md` with:
     - the source article title or a minimally shortened source-aligned title,
     - cover text and subtitle,
     - short mobile paragraphs that remain close to the source draft,
     - restrained platform tags,
     - image order,
     - source/evidence note,
     - pre-publish checklist.
   - For computer-research posts with an available PDF, do not produce summary cards, generated visuals, or substitute standalone extracted figure assets for the paper pages. Render the original PDF pages in order and use only one Xiaohongshu note for the paper. Use an official-HTML screenshot only when no PDF is available, and retain surrounding paper context so it is visibly an original-paper screenshot.
   - Cropping margins, scaling, or adding neutral padding to reach a readable 3:4 PNG such as 1242 x 1656 is allowed. Do not redraw the figure, replace labels, alter data, add decorative elements, or overlay generated summaries.
   - For finance content, reuse the finance drafting skill's shared `render_finance_text_card.py` renderer and upload exactly one pure-text 3:4 PNG by default. Use a white or warm-neutral page, small brand/time line, one red or dark factual headline, 2-4 compact text paragraphs, and a small `来源：金十数据｜时间：...` footer; do not create a separate platform-specific finance layout.
   - Prohibit icons, charts, candlesticks, diagrams, flow arrows, photos, illustrations, data tiles, separate market-transmission boxes, separate risk boxes, and multi-card finance carousels.
   - Preserve attribution such as `某机构称`, distinguish facts from interpretation, and integrate market implications and counter-evidence into the paragraphs. If the image becomes crowded, shorten it and retain detail in the body rather than generating another image.
   - Do not copy another creator's words, logo, brand, or exact visual identity.
   - Do not reserve a large flat-color header band or empty safe area above or behind the title unless it encodes real hierarchy. Prefer one continuous neutral canvas, a thin rule, and content-led spacing; decorative color fields must not consume substantial vertical space.
   - Research screenshots must not become slogan posters or summary cards. Their job is to show the original paper evidence; explanations remain in the post body.
   - Use original paper screenshots with readable source captions when available. Avoid generated cover cards and text-only cards for technical papers.
   - Render full PDF pages at a resolution that keeps text legible when opened. Scaling or neutral padding is allowed; do not crop paper content, alter labels/data, or overlay generated summaries.
   - Xiaohongshu currently accepts at most 18 images per note. If a PDF exceeds that limit, upload only pages `1..18` in the single note and omit pages `19..N`. Do not create a second part. Record `pdf_pages=N`, `uploaded_pages=1..18`, `omitted_pages=19..N`, and `visual-truncated`; never call the image set the full PDF.
   - Figure explanations must be specific and plain: name what the axes, arrows, colors, modules, rows, or columns mean; explain what comparison the reader should make; and state why that visual supports the article's argument.
   - For screenshots with small text, prefer a cropped high-resolution capture. Put any Chinese explanation in the post body, not as generated text over the screenshot.
   - For research notes, use one main paper by default, require readable PDF/HTML full text, and use source-paper figures/tables when available.
   - For finance notes, use current market data and include a brief non-advice disclaimer.
   - For research-only notes, do not add investment-advice disclaimer wording.
   - Use the exact brand spelling `白Yu观测`, with no space between `Yu` and `观测`.

5. Check the package before opening Xiaohongshu.
   - Confirm research screenshots exist, have readable dimensions, and are visually nonblank. If `N <= 18`, cover pages `1..N` exactly once; if `N > 18`, cover pages `1..18` exactly once and record the omitted tail without splitting.
   - Confirm the body does not contain old brand spelling variants, accidental WeChat-only HTML, raw HTML list tags, messy repeated semicolons, malformed sentence punctuation, or unrelated finance/research mixing.
   - Confirm the Xiaohongshu version has not drifted away from the source article's tone. If it reads like a viral hook thread instead of a calm research note, revise before uploading.
   - Confirm the body does not read like an LLM abstract: it should contain source-specific nouns, figure/table names, method mechanics, and limits.
   - Confirm research bodies contain `🎓 来源机构：` and `🔍 背景难点：` before `🔑关键方法`; the background must name at least two concrete prior-approach weaknesses or task constraints.
   - For research notes, scan the actual body for the literal marker order `opening -> 📝一句话总结 -> 🔑关键方法 -> 💡核心创新 -> ⚠️限制与边界 -> 🧭结论和关键洞察`; require exactly one non-empty summary line, exactly three numbered method items, exactly three numbered innovation items, 2-3 limitation items, and exactly one `论文结论：` and `关键洞察：` line. Reject an independent `📊实验效果` section and a trailing `论文：<full paper title>` line. Confirm decisive experimental evidence remains embedded in the surviving sections. Content completeness without this reference skeleton is a failed adaptation.
   - Run `validateXhsPost` from `scripts/publish-prepared-xhs.mjs` before opening the platform. Reject blank or whitespace-only lines inside the five compact research sections; keep exactly one blank line only between top-level blocks.
   - Confirm no old short-summary body was concatenated with the full body.
   - Confirm source notes record local paths, source URLs, evidence labels, and whether the run is local-only, draft-save, or published.
   - For finance notes, run `/Users/jackie/.codex/skills/financial-market-signal-draft/scripts/check_finance_policy.mjs` on the final title/body file and card text sources. Any hit is a hard stop: do not upload or edit around the keyword; return to candidate selection and produce the next eligible article.
   - Confirm the finance source note contains a current `jin10.com` URL, the displayed timestamp, and any verified original-source URL.
   - Visually inspect the rendered finance PNG before upload. Require exactly one image, visible brand text exactly `白Yu观测`, a legible `来源：金十数据｜时间：...` footer, and no icons, charts, arrows, photos, illustrations, data tiles, boxed modules, or additional carousel images. Do not treat the generation prompt as proof.

6. Use Chrome for Xiaohongshu Creator Center.
   - Use the verified local package and system-Chrome handoff. Do not conceal automation, patch browser fingerprints, spoof `navigator.webdriver`, generate random mouse paths, bypass CAPTCHA, or imitate a human to evade platform controls.
   - Before and after every upload, text-entry block, disclosure change, schedule change, and submission attempt, inspect visible alerts/dialogs/toasts for automation detection, abnormal access, excessive operations, access restriction, robot checks, or safety verification. On any match, return `XHS_AUTOMATION_OR_RISK_DETECTED`, preserve evidence, stop before further action, and do not retry automatically.
   - Use state-driven pacing rather than burst actions: wait for the exact expected image count or field readback, require it to remain stable, and then apply a fixed inter-step pause. Do not add randomized delays or stealth behavior as an anti-detection workaround.
   - Use `chrome:control-chrome` for browser operation because publishing depends on the user's logged-in Chrome session.
   - Navigate first to `https://www.xiaohongshu.com/explore`; do not use a `creator.xiaohongshu.com` URL as the initial account/session entry. After that session check succeeds, draft preflight, post-management return, upload preparation, and draft-save recovery must reuse the same claimed Chrome page and return to the official image-publish route `https://creator.xiaohongshu.com/publish/publish?from=menu&target=image`. Do not return through `?source=official`, which defaults to video upload.
   - On the Explore page, require no login/QR/phone prompt. If the layout exposes `创作中心`, open it and click its visible `发布`; if the logged-in sidebar exposes only a visible `发布` link, click that link directly from Explore. Support either a new tab or an existing Creator Center tab being reused.
   - A safe `reds-mask` overlay can mount after opening Creator Center and intercept the visible publish-link click. Immediately before that click, and once more only when the click reports that exact safe mask as the pointer interceptor, re-run the existing narrow safe-overlay dismissal and retry the same visible link once. If the mask remains, changes identity, contains a login/risk-control/verification prompt, or the single retry still fails, stop without force-clicking or navigating directly to the Creator Center URL. Record the last visible state and do not retry the content automatically.
   - Use that visible Explore-page route to reach image-text publishing; do not replace it with a direct Creator Center URL or a hidden `创作服务` link.
   - Use the user's single default logged-in account; do not require the visible account name to match a configured string. If the page redirects to login or shows QR/phone/CAPTCHA verification, stop and ask the user.
   - After any browser reopen, repeat the page/account check and verify whether uploaded images, title, and body still exist before resuming edits or clicking publish.
   - Choose the note/image-text publishing mode if the platform offers multiple modes. If the single visual `上传图片` control is already present, reuse it and do not click `上传图文` again. When framework duplicates expose several DOM nodes for one visible control, exclude negative/off-screen rectangles, deduplicate overlapping nodes by their visual rectangle, require one unique rectangle, wait for it to remain stable, and click its center in the claimed system-Chrome page. Do not select an arbitrary duplicate node.
   - Upload prepared images strictly one file at a time in the planned order. For image 1, click the single visible `上传图片` button. After image 1, that button is replaced by the image-list add tile; for every later image, click the single visible `.img-upload-area .entry` tile. Each click must await a fresh `filechooser`, and each chooser gets exactly one `setFiles([path])` call. Never reuse a prior chooser. Wait until the visible image counter increases to the exact expected value, wait another 1.5 seconds and verify that value is stable, then select the next file. Never pass the full image list or more than one path in a single call. Stop and preserve the registered editor after image 1 if the add tile, chooser, count, or order cannot be verified. For research posts, images must be original-paper screenshots rather than generated cards.
   - For each requested structured topic, put the caret at the end of the body, type the complete literal `#话题`, and press Enter. Enter success is sufficient. Do not require an exact suggestion/listbox item, exact text match after Enter, blue styling, a chip, or a non-editable platform token; a related platform-selected topic is acceptable.
   - Fill title, body, tags, and cover according to `xiaohongshu-post.md`.
   - Before handoff, inspect the content-type row first. If its current visible display value is already `笔记含AI合成内容`, treat the declaration as selected and do not click or reopen it; duplicate same-text DOM wrappers for that one displayed row are not separate choices. Only when the row still shows the exact entry `添加内容类型声明`, open it, select `笔记含AI合成内容`, and read the resulting current display value back. Prefer checkbox/radio/ARIA/data-state/class evidence when present. If neither the selected display value nor a verified native selected state can be obtained, stop before handoff.
   - Do not activate `定时发布` or write any schedule field. Require the visible final control to remain the ordinary enabled `发布` control, but never click it.
   - Review visible rendering: image order, title, body breaks, tags, and source note.

### Verified Chrome publishing path

- For Daily Scheduled/unattended runs, the Scheduled worker must only package and enqueue one self-contained platform trigger with `/Users/jackie/Documents/paper daily/automation/local-publisher/prepare-trigger.cjs`. The installed `com.openai.codex.baiyu-local-publisher` LaunchAgent performs all 9223 browser actions. The Scheduled worker and an interactive conversation must not operate Chrome or upload as a fallback.
- Before any browser action, read and follow `/Users/jackie/Documents/paper daily/automation/platform-publisher/BROWSER_SESSION_CONTRACT.md`. Scheduled/unattended runs use only the verified 9223 route; do not automatically fall back to the normal Chrome extension. The extension route is allowed only when the user explicitly hands off an already-open Xiaohongshu tab, and that run must not switch routes. Require final cleanup evidence.
- Use `/Users/jackie/Documents/paper daily/automation/platform-publisher/run-platform-publisher.sh` with a prepared job. Run it without `--send` first, then reuse the same job with `--platform xiaohongshu --send`; do not recreate this sequence ad hoc.
- For CDP `9223`, reuse `/Users/jackie/Library/Application Support/Google/Chrome Codex Debug 9223`. The port does not carry login state. Do not silently substitute `/Users/jackie/Library/Application Support/Google/Chrome Codex Debug` or a fresh profile and then report that prior logins expired.
- Before attaching, confirm both that `127.0.0.1:9223` is stable and that its Chrome process uses the verified profile. If the port is closed, use `/Users/jackie/Documents/paper daily/automation/platform-publisher/start-platform-debug-chrome.sh`.
- Probe `/json/version` with both `curl --noproxy '*'` and the bundled Node `fetch` from the same execution context that will run the publisher. If both return HTTP 200, continue the real publish attempt and do not reuse an earlier `EPERM` as the current blocker. If Chrome is listening but this exact context still returns `EPERM`, classify it as an execution-environment permission failure, not a closed port, logout, or platform failure.
- Import and use `scripts/publish-prepared-xhs.mjs` for repeat publishing after the first successful page connection. Do not rewrite the browser sequence ad hoc.
- Read `references/successful-publish-examples.md` when diagnosing a regression. It records known-good inputs, page states, and completion evidence.
- Keep one claimed Chrome tab for the entire upload, edit, publish, and verification sequence. Do not switch to Computer Use or a native file dialog while the Chrome file chooser path is available.
- Locate the single visual `上传图片` button for image 1 only. Treat overlapping framework duplicates at the same positive rectangle as one visual target and use a center mouse click; reject multiple distinct visible rectangles. Once the editor shows `1/18`, locate the single visible `.img-upload-area .entry` add tile for images 2..N; the initial upload button is no longer a valid control. For each image, start a new `waitForEvent('filechooser')`, click the correct current control, and use only the newly returned chooser for one `setFiles([path])` call. The 9223 bridge locator must expose `count`, `nth`, `isVisible`, `innerText`, and `boundingBox` so hidden, off-screen, and overlapping duplicates can be handled. After each file, allow up to 60 seconds for the image counter to become `i/18`, wait 1.5 seconds, verify the same count remains stable, and only then open a fresh chooser for file `i+1`. Never send the full array or multiple paths in one call. Confirm the editor is visible and the final image counter matches the intended count before filling text.
- Fill the exact title placeholder `填写标题会有更多赞哦`. Fill the first visible `[contenteditable="true"]` editor with the canonical compact body plus restrained tags.
- Reserve enough room under Xiaohongshu's body limit for every requested structured topic before entering hashtags. Append each complete literal `#话题` at the body end and press Enter. Do not require recommendation-list matching or post-Enter topic/token verification. Stop before submission only if typing/Enter fails, the editor cannot be preserved, or the body limit is exceeded.
- Confirm title length, body length, image order, active creator capability, prohibited-term scan, the opened `添加内容类型声明`, and the selected state of `笔记含AI合成内容` before handoff; do not require a visible account-name match in the user's single default session.
- Treat `添加内容类型声明 -> 笔记含AI合成内容` as a hard handoff gate for every Xiaohongshu note. A visible current row value of `笔记含AI合成内容` is verified selection evidence, even when the framework exposes duplicate same-text wrapper nodes; do not click that row again. Open `添加内容类型声明` at most once only when the selected value is absent, select the AI-content value, and require the current display value or native selected state on readback. If verification is still unavailable, return a blocker and leave the submission control untouched.
- Treat the ordinary enabled `发布` control as a readiness check only. Record its visible label and enabled state, but perform zero clicks on it or any equivalent submit control.
- For an explicitly authorized correction of an existing note, keep the exact `/publish/update?id=...&noteType=normal` URL and note ID. Reuse an already-open exact edit tab instead of opening a duplicate or navigating the loaded tab to the same URL, which may trigger an unsaved-state dialog. Before every retry, inspect the title and current preview count: resume from the verified staged state instead of blindly deleting or uploading again.
- When replacing a full 18-image set, Xiaohongshu requires at least one image to remain: delete all but one old image, upload new pages 1–17, delete the retained old image, then append page 18. The edit page may still submit through `xhs-publish-btn[submit-text="发布"]`; treat this as an update only after reopening the same note ID and verifying the saved title and all 18 previews.
- A successful automated handoff is `status=draft`, never `ready-for-manual-submit`: require the exact `暂存离开` control, visible `保存成功`, the newest exact-title draft record with non-empty `data-draft-id` and saved time, one exact `编辑` action, and reopened readback of the title, canonical body prefix, expected `N/18` image counter, `笔记含AI合成内容`, and enabled ordinary publish control. Record `draftSaved=true`, `reopened=true`, `submitted=false`, the draft ID, and saved time. Upload completion, editor fill, the visible publish button, or merely seeing/clicking `暂存离开` is not saved-draft evidence or publication.
- When the draft cards are not present after `保存成功`, open the official `target=image` route on the same authenticated claimed page, click the unique visual `草稿箱(N)` control, wait for the drawer animation to stabilize, then click the unique visual `图文笔记(N)` tab. Both controls may be inside a closed component: validate their pierced-CDP ancestry (`draft-title-box` under `header-draft`, then `tab-item` under `draft-tabs`), exclude off-screen nodes, deduplicate overlapping rectangles, and send a center mouse click only after two stable position reads. Wait for draft records to mount, find the uniquely newest exact-title record whose saved time is not earlier than the save attempt, and reopen its exact `data-draft-id`. If the exact record or persisted title/body/image count/AI declaration cannot be verified, return an `XHS_DRAFT_*` failure and preserve the page with `preserveReason=xhs-draft-save-failure`.
- Before uploading or re-saving, inspect all open Creator Center pages and, if necessary, the official image-publish draft list for an existing exact-title record. Select only the uniquely newest saved-time record; if the newest time is tied, stop. Reopen and verify it instead of creating a duplicate. Trigger fingerprints must normalize temporary bundle paths and hash the actual ordered file contents so an identical self-contained bundle remains terminal and is skipped without browser work.
- Preserve the exact registered `/publish/publish` page when returning `draft`, with `preserveReason=xhs-saved-draft`. Also preserve a Xiaohongshu editor that fails after at least one verified image with `preserveReason=xhs-partial-upload`; inspect and resume that exact page instead of closing it and creating a browser-local one-image blank draft. Preserve Explore, creator content-management, public notes, source pages, and unrelated user tabs. Ordinary failures follow the browser contract unless a human-verification page must be preserved.
- Treat the Creator Center draft box as browser-profile-local state. Before repairing an existing draft, verify the exact Chrome profile, `data-draft-id`, saved time, first-image identity, title/body state, and preview count. Do not infer that drafts visible in normal Chrome also exist in the dedicated 9223 profile.
- Classify the last verified boundary: `CDP_UNAVAILABLE` means no page operation; a script/runtime error before the file chooser means no upload; login/QR/CAPTCHA/2FA is a human-verification stop; an uploaded editor without submission evidence is `uploaded-not-submitted`. Do not call these platform rejection or publication.
- If a proxy, browser bridge, CDP, or tool call times out without a platform validation error, retry with bounded backoff while preserving the same tab. Before every retry, inspect the current page because the previous action may have succeeded. Reclaim or reopen the tab only when the session is lost, then repeat account and draft-state checks.
- Stop retrying only for login/CAPTCHA/QR/2FA/account-switch prompts, explicit platform rejection, missing files, or repeated session loss that cannot preserve or recover state. Record the exact blocker.

7. Prepare the manual handoff.
   - Stop on the filled final page for every browser run. Do not click publish even when the user uses broad words such as "发布"; the user completes the last step.
   - If the platform has no accessible draft-save button, do not invent saved-draft evidence. Preserve the prepared page, report a concrete `XHS_DRAFT_*` blocker, and do not mark the run successful.
   - If the platform rejects content, images, title length, tags, or account permissions, record the exact visible issue without guessing.

8. Leave an audit trail.
   - Record the final browser outcome in the source notes: local package only, `ready-for-manual-submit`, failed login, blocked content-type/AI-content declaration verification, automation/risk-control stop, platform validation error, or user action required.
   - Report exact local artifact paths and the browser result to the user.

## Validation checklist

Before finishing, verify:

- Domain writing skill or finished source draft was used appropriately.
- Research claims are full-text-backed unless explicitly labeled `abstract-only` or `listing-only`.
- Market claims use current data for the requested date.
- Research-only and finance-only content were not silently mixed.
- `白Yu观测` is spelled exactly.
- Xiaohongshu body is short-paragraph and mobile-readable, but still preserves the source article's calm deep-reading style.
- Xiaohongshu title, section order, claims, figures, and conclusion stay aligned with the source article.
- Computer-research images are direct original-paper screenshots, not summary cards, redraws, synthesized diagrams, or AI-generated images.
- The body includes figure/table interpretation, method, evaluation, and limitations for technical research; screenshots provide the original visual evidence rather than carrying rewritten summaries.
- Research body uses the fixed reference-style opening, emoji section markers, three method items, three innovation items, multiple contextualized results, explicit limitations, and a distinct two-line conclusion/key-insight block without a duplicated final paper-title line.
- Research body names paper-listed source institutions and explains the background difficulty before the method.
- Compact research sections have no internal blank lines; blank lines appear only once between top-level blocks.
- PDF-backed research posts use one note and preserve page order. When the PDF exceeds 18 pages, only pages `1..18` are uploaded and the omitted tail is truthfully recorded.
- Figure captions explain concrete visual elements in plain Chinese, not just "see the figure" or a copied paper caption.
- The result does not sound like a generic AI summary or platform hook thread.
- Images are present, ordered, and sized for Xiaohongshu; research screenshots retain page/Figure/Table provenance.
- Finance uses one pure-text image with no icons, charts, diagrams, photos, infographic modules, or carousel expansion.
- No credentials, tokens, private browser data, or unrelated tabs were copied into the post.
- The user's single default Xiaohongshu session exposes the intended creator and publish functions; a visible account-name label is not required.
- `添加内容类型声明` was opened and `笔记含AI合成内容` was visibly found with its selected state verified before handoff.
- `定时发布` was not selected and no schedule field was changed.
- `暂存离开` produced visible save-success evidence; the newest exact-title draft ID was reopened and title/body/image count/AI declaration were read back.
- The ordinary `发布` control was verified as visible and enabled but was not clicked; the exact saved-draft edit page remains open for the user.
