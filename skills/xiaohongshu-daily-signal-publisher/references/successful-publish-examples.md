# Verified Xiaohongshu publish examples

Current runs follow the skill's manual-submit contract. Older publication examples below are historical diagnostics and do not authorize clicking `发布`.

## 2026-08-30 one-image blank-draft regression

- Symptom: the first image reached `1/18`; the second image never incremented the counter, so title and body were still empty when cleanup closed the editor.
- Root causes: one `filechooser` object was reused across multiple `setFiles([path])` calls; after the first fix, the script still tried to reuse the initial `上传图片` control even though Xiaohongshu replaces it after image 1.
- Verified fix: image 1 clicks the single visible `上传图片` button; images 2..N click the single visible `.img-upload-area .entry` add tile. Every image awaits a new `filechooser`, calls `setFiles([onePath])` once, and verifies the exact stable counter before continuing.
- Verified bridge contract: the 9223 locator wrapper exposes `count`, `nth`, and `isVisible`; this is covered by the platform-publisher test suite.
- Real evidence on 2026-08-30: trigger `manual-rerun-20260830-wikiskill-xhs-addtile-03` prepared `WikiSkill：经验如何变成技能` with 18/18 images, title/body/topics, and `笔记含AI合成内容`; result was `ready-for-manual-submit`, `submitted=false`, and the editor stayed open.
- Recovery rule: preserve partial-upload editor pages with `preserveReason=xhs-partial-upload`. Existing draft repair requires the exact browser profile, `data-draft-id`, saved time, first-image identity, and local source job; never guess by an empty title alone.
- Tests after the full draft-save repair: Xiaohongshu skill 28/28, platform publisher 118/118, and local worker 16/16 passed.

## 2026-08-30 saved-draft and idempotence repair

- The final `暂存离开` button is inside a closed shadow tree. The verified path uses CDP `DOM.getFlattenedDocument({pierce:true})`, requires one `BUTTON.ce-btn.white` under the enabled `XHS-PUBLISH-BTN[submit-text=发布]`, resolves its exact backend node, and invokes that button only. It does not use coordinate-ratio clicking.
- Trigger `manual-recover-draft-20260830-wikiskill-14` opened the official image-publish draft list, selected the uniquely newest exact-title record, and reopened draft `7c9e97fd-c3ff-4792-abba-3d8e3621dfeb` saved at `2026-08-30 23:41:17` Asia/Shanghai.
- Reopen evidence: exact title `WikiSkill：经验如何变成技能`, canonical body readback length 1058, `18/18` images, visible `笔记含AI合成内容`, enabled ordinary publish control, `reopened=true`, and `submitted=false`.
- The same `data-draft-id` existed before and after the recovery save; the save updated that draft instead of creating a new ID.
- Temporary bundle roots are excluded from the semantic fingerprint while the ordered post/image bytes remain hashed. Trigger `manual-idempotence-final-20260830-wikiskill-15` reused the terminal fingerprint: it completed in under one second, registered zero browser pages, and left the saved-draft state timestamp and ID unchanged.
- Recovery rule: after `保存成功`, if the current editor does not expose a draft-box entry, open `https://creator.xiaohongshu.com/publish/publish?from=menu&target=image` in the same authenticated claimed page, choose only the uniquely newest exact-title record, click its exact `编辑`, and verify all persisted fields before returning `status=draft`.

## 2026-08-31 fixed image-entry and draft-box recovery

- Root causes from the 2026-08-29/30 broken drafts: management preflight returned through `?source=official`, which defaults to video upload; framework mirrors exposed multiple or off-screen `上传图文` nodes; after `暂存离开`, the code saw `草稿箱(N)` but did not open it; the drawer then defaulted to `视频笔记(0)` instead of `图文笔记(N)`.
- Verified route: start with the Explore session check, use the fixed 9223 system-Chrome LaunchAgent route, and after preflight return to `https://creator.xiaohongshu.com/publish/publish?from=menu&target=image`. If `上传图片` is already visible, reuse it. Treat overlapping DOM mirrors as one visual rectangle, reject distinct rectangles, and click the stable center in the claimed page.
- Verified draft readback: after `保存成功`, click the pierced closed-component `DIV.draft-title-box` for `草稿箱(N)`, wait for the drawer position to stabilize, click `DIV.tab-item` for `图文笔记(N)`, wait for `[data-draft-id]`, select the uniquely newest exact-title record, and reopen its exact edit action. The default video tab is not draft absence.
- Five historical repairs returned `status=draft`, `reopened=true`, and `submitted=false`: 18-image `AI人类监督：从看见风险到能够干预` (`c7b58bc0-cc81-420d-be7d-d18c8749d58f`), 15-image `建设性冲突Agent：不只附和设计师` (`90330896-33cf-46a6-97b9-b3a1f608b8da`), 6-image `CAF因果能动性：从解释到干预` (`8376c476-936f-4ad7-a30f-9c0e39985e0c`), 7-image `AI现象学：追踪人机体验共演化` (`1ab59d4f-c62c-4700-bdd2-e6a8980a2265`), and 18-image `AlphaEval：智能体生产评估` (`b48a4d56-5d49-47c2-a195-fc36195e7d37`).
- Idempotence evidence: identical follow-up triggers kept the same terminal fingerprints and draft IDs; four returned explicit `skipped=true`, while the 08:00 trigger returned `completed`, registered zero browser pages, and retained the same 18-image draft state. No final publish or scheduled-publish control was clicked.
- Regression gates after the repair: Xiaohongshu skill tests 31/31 and platform-publisher tests 121/121 passed; the deployed adapter and tab shim were byte-identical to workspace sources.

## AgentCanary, 7 cards

- Account: `白Yu观测`
- Upload image 1: visible `上传图片` -> fresh `filechooser` -> one `setFiles` call
- Upload images 2..N: visible `.img-upload-area .entry` add tile -> fresh `filechooser` -> one `setFiles` call
- Upload evidence: `multiple=true`, then `7/18`
- Lesson: wait for the image counter before filling or publishing

## AI earnings and Fed, 6 cards

- Account: `白Yu观测`
- Upload evidence: 6 ordered cards accepted
- Publish action: one click on the visibly verified publish control
- Completion evidence: URL changed to `published=true`

## 2026-07-26 3+3 rerun

- Adaptive Adversaries: 7 cards, `Adaptive对抗评测：静态池失效`, `published=true`
- EvoSOP: 7 cards, `EvoSOP：Agent工具治理`, `published=true`
- PlanFlip: 7 cards, `PlanFlip：计划阶段注入`, `published=true`
- Crypto weekend: 6 cards, `周末加密定价的两层分化`, `published=true`
- Energy inventory: 6 cards, `油价与能源股出现分叉`, `published=true`
- The same Chrome tab was reused for all five posts.
- Duplicate image-text tab nodes at the same rectangle were deduplicated.
- Every post required account match, image count, content limits, an enabled publish control, and fresh `published=true` evidence.
