import assert from "node:assert/strict";
import test from "node:test";

import {
  assertNoXhsAutomationRisk,
  assertXhsPublicationAvailable,
  chooseAiDisclosureCandidate,
  computeScheduledPublishAt,
  ensureAiAssistedCreation,
  ensureAiContentDisclosure,
  ensureScheduledPublish,
  openImageFileChooser,
  resolveImageUploadControl,
  selectImageTextUploadMode,
  XHS_AI_CONTENT_DISCLOSURE_LABEL,
  XHS_CONTENT_TYPE_DECLARATION_LABEL,
  uploadFilesSequentially,
  validateManualSubmitReadiness,
  validateScheduledPublishReadback,
  validateXhsPost,
} from "../scripts/publish-prepared-xhs.mjs";

test("selects image-text mode and requires one visible upload-image button", async () => {
  let selected = false;
  const tabs = [
    {
      isVisible: async () => true,
      innerText: async () => "上传视频",
      boundingBox: async () => ({ x: 10, y: 10, width: 80, height: 40 }),
    },
    {
      isVisible: async () => true,
      innerText: async () => "上传图文",
      boundingBox: async () => ({ x: 110, y: 10, width: 80, height: 40 }),
    },
  ];
  const hidden = { isVisible: async () => false, boundingBox: async () => null };
  const visible = {
    isVisible: async () => selected,
    boundingBox: async () => ({ x: 300, y: 300, width: 120, height: 40 }),
  };
  let uploadClicked = false;
  const tab = {
    playwright: {
      locator: () => ({
        count: async () => tabs.length,
        nth: (index) => tabs[index],
      }),
      getByRole: () => ({
        count: async () => 2,
        nth: (index) => [hidden, visible][index],
      }),
      waitForTimeout: async () => undefined,
    },
    cua: {
      click: async ({ x, y }) => {
        if (x === 150 && y === 30) selected = true;
        if (x === 360 && y === 320) uploadClicked = true;
      },
    },
  };
  const control = await selectImageTextUploadMode(tab);
  assert.equal(selected, true);
  await control.click();
  assert.equal(uploadClicked, true);
});

test("reuses the visible upload-image button without clicking image-text mode", async () => {
  const visible = {
    isVisible: async () => true,
    boundingBox: async () => ({ x: 300, y: 300, width: 120, height: 40 }),
  };
  let locatorCalled = false;
  let clicked = null;
  const tab = {
    playwright: {
      getByRole: () => ({
        count: async () => 1,
        nth: () => visible,
      }),
      locator: () => {
        locatorCalled = true;
        throw new Error("image-text tab must not be queried");
      },
    },
    cua: {
      click: async (point) => {
        clicked = point;
      },
    },
  };
  const control = await selectImageTextUploadMode(tab);
  assert.equal(locatorCalled, false);
  await control.click();
  assert.deepEqual(clicked, { x: 360, y: 320 });
});

test("wraps an early filechooser rejection with the image index", async () => {
  const tab = {
    playwright: {
      waitForEvent: async () => {
        throw new Error("filechooser timeout");
      },
    },
  };
  const uploadControl = {
    click: async () => {
      await Promise.resolve();
    },
  };
  await assert.rejects(
    openImageFileChooser({ tab, uploadControl, index: 4 }),
    /XHS_SEQUENTIAL_UPLOAD_CHOOSER_NOT_OPENED index=5.*filechooser timeout/,
  );
});

test("stops on visible automation or risk-control notices", () => {
  assert.doesNotThrow(() => assertNoXhsAutomationRisk("图片正在处理中"));
  assert.throws(
    () => assertNoXhsAutomationRisk("系统检测到自动化脚本，请完成验证"),
    /XHS_AUTOMATION_OR_RISK_DETECTED.*(检测到自动化|自动化脚本)/,
  );
  assert.throws(
    () => assertNoXhsAutomationRisk("操作过于频繁，请稍后再试"),
    /XHS_AUTOMATION_OR_RISK_DETECTED.*操作过于频繁/,
  );
});

test("allows manual handoff and blocks automated submission", () => {
  assert.deepEqual(assertXhsPublicationAvailable(), {
    manualSubmit: true,
    automatedSubmit: false,
  });
  assert.throws(
    () => assertXhsPublicationAvailable({ manualSubmit: false }),
    /XHS_AUTOMATED_SUBMISSION_DISABLED.*manualSubmit=true-required/,
  );
});

test("verifies the final page without treating it as submitted", () => {
  assert.equal(
    validateManualSubmitReadiness(
      {
        title: "DeepBias深挖多模态偏见",
        body: "正文内容\n#人工智能",
        counter: "3/18",
        publishText: "发布",
        publishDisabled: "false",
        publishVisible: true,
      },
      {
        title: "DeepBias深挖多模态偏见",
        body: "正文内容",
        images: 3,
      },
    ),
    true,
  );
  assert.throws(
    () =>
      validateManualSubmitReadiness(
        {
          title: "DeepBias深挖多模态偏见",
          body: "正文内容",
          counter: "3/18",
          publishText: "定时发布",
          publishDisabled: "false",
          publishVisible: true,
        },
        {
          title: "DeepBias深挖多模态偏见",
          body: "正文内容",
          images: 3,
        },
      ),
    /XHS_MANUAL_SUBMIT_CONTROL_NOT_READY/,
  );
});

test("uploads Xiaohongshu files one at a time and verifies every increment", async () => {
  const calls = [];
  const chooserIndexes = [];
  let uploadedCount = 0;
  let chooserCount = 0;
  const openChooser = async (index) => {
    chooserIndexes.push(index);
    chooserCount += 1;
    return {
      setFiles: async (files) => {
        calls.push(files);
        uploadedCount += files.length;
      },
    };
  };
  const tab = {
    playwright: {
      evaluate: async () => ({
        counter: `${uploadedCount}/18`,
        titleCount: 1,
        editorCount: 1,
      }),
      waitForTimeout: async () => undefined,
    },
  };
  const result = await uploadFilesSequentially({
    tab,
    openChooser,
    files: ["page-01.png", "page-02.png", "page-03.png"],
  });
  assert.equal(chooserCount, 3);
  assert.deepEqual(chooserIndexes, [0, 1, 2]);
  assert.deepEqual(calls, [
    ["page-01.png"],
    ["page-02.png"],
    ["page-03.png"],
  ]);
  assert.equal(result.counter, "3/18");
});

test("resumes sequential Xiaohongshu upload from an existing image count", async () => {
  const chooserIndexes = [];
  const filesSeen = [];
  let uploadedCount = 1;
  const result = await uploadFilesSequentially({
    tab: {
      playwright: {
        evaluate: async () => ({
          counter: `${uploadedCount}/18`,
          titleCount: 1,
          editorCount: 1,
        }),
        waitForTimeout: async () => undefined,
      },
    },
    startIndex: 1,
    files: ["page-01.png", "page-02.png"],
    openChooser: async (index) => {
      chooserIndexes.push(index);
      return {
        setFiles: async (files) => {
          filesSeen.push(files);
          uploadedCount += files.length;
        },
      };
    },
  });
  assert.deepEqual(chooserIndexes, [1, 2]);
  assert.deepEqual(filesSeen, [["page-01.png"], ["page-02.png"]]);
  assert.equal(result.counter, "3/18");
});

test("uses the initial button only once, then the visible image-list add tile", async () => {
  const initialUploadButton = { name: "initial" };
  const hidden = { isVisible: async () => false };
  const addTile = { isVisible: async () => true };
  const tab = {
    playwright: {
      locator: (selector) => {
        assert.equal(selector, ".img-upload-area .entry");
        return {
          count: async () => 2,
          nth: (index) => [hidden, addTile][index],
        };
      },
    },
  };

  assert.equal(
    await resolveImageUploadControl({ tab, index: 0, initialUploadButton }),
    initialUploadButton,
  );
  assert.equal(
    await resolveImageUploadControl({ tab, index: 1, initialUploadButton }),
    addTile,
  );
});

const compactResearchBody = `今天给大家带来一篇关于多模态偏见评测的新论文——《DeepBias》。
🎓 来源机构：中科院计算所、华为2012实验室
🔍 背景难点：静态图文对容易过时并泄露。单轮查询也难以暴露安全对齐后的深层偏见。

📝一句话总结
DeepBias通过模型反馈迭代测试样本，在所测模型上暴露了静态基准遗漏的偏见。

🔑关键方法
1️⃣生成候选测试分布。
2️⃣依据模型反馈进化样本。
3️⃣多轮改写继续深挖。

💡核心创新
1️⃣从静态样本转为自适应生成。
2️⃣同时适应分布和实例。
3️⃣把目标模型反馈放进闭环。

⚠️限制与边界
1️⃣结论依赖所选模型。
2️⃣偏见标签仍需人工复核。

🧭结论和关键洞察
论文结论：自适应测试在所测模型上能暴露静态基准遗漏的偏见。
关键洞察：评测需要随模型反馈更新样本，固定题库会低估动态风险。`;

test("accepts compact research sections without internal blank lines", () => {
  const result = validateXhsPost({
    title: "DeepBias深挖多模态偏见",
    body: compactResearchBody,
  });
  assert.equal(result.research, true);
  assert.equal(result.compactSections, 5);
});

test("rejects a blank line after a compact section heading", () => {
  assert.throws(
    () =>
      validateXhsPost({
        title: "DeepBias深挖多模态偏见",
        body: compactResearchBody.replace("💡核心创新\n1️⃣", "💡核心创新\n\n1️⃣"),
      }),
    /标题后不得有空行/,
  );
});

test("rejects a blank line between items in one compact section", () => {
  assert.throws(
    () =>
      validateXhsPost({
        title: "DeepBias深挖多模态偏见",
        body: compactResearchBody.replace(
          "1️⃣从静态样本转为自适应生成。\n2️⃣",
          "1️⃣从静态样本转为自适应生成。\n\t\n2️⃣",
        ),
      }),
    /章节内部不得有空行/,
  );
});

test("requires source institutions and background difficulty for research", () => {
  assert.throws(
    () =>
      validateXhsPost({
        title: "DeepBias深挖多模态偏见",
        body: compactResearchBody.replace("🎓 来源机构：", "来源："),
      }),
    /缺少来源机构/,
  );
  assert.throws(
    () =>
      validateXhsPost({
        title: "DeepBias深挖多模态偏见",
        body: compactResearchBody.replace("🔍 背景难点：", "背景："),
      }),
    /缺少背景难点/,
  );
});

test("requires the conclusion and key-insight section", () => {
  assert.throws(
    () =>
      validateXhsPost({
        title: "DeepBias深挖多模态偏见",
        body: compactResearchBody.replace(
          /\n\n🧭结论和关键洞察[\s\S]*$/,
          "",
        ),
      }),
    /缺少固定章节/,
  );
});

test("requires exactly one one-sentence-summary line", () => {
  assert.throws(
    () =>
      validateXhsPost({
        title: "DeepBias深挖多模态偏见",
        body: compactResearchBody.replace(
          /\n\n📝一句话总结[\s\S]*?(?=\n\n🔑关键方法)/,
          "",
        ),
      }),
    /缺少固定章节/,
  );
  assert.throws(
    () =>
      validateXhsPost({
        title: "DeepBias深挖多模态偏见",
        body: compactResearchBody.replace(
          "DeepBias通过模型反馈迭代测试样本，在所测模型上暴露了静态基准遗漏的偏见。",
          "第一行总结。\n第二行总结。",
        ),
      }),
    /必须且只能包含一行内容/,
  );
});

test("rejects an independent experiment-results section", () => {
  assert.throws(
    () =>
      validateXhsPost({
        title: "DeepBias深挖多模态偏见",
        body: compactResearchBody.replace(
          "\n\n⚠️限制与边界",
          "\n\n📊实验效果\n✅单独罗列结果。\n\n⚠️限制与边界",
        ),
      }),
    /不要保留独立实验效果章节/,
  );
});

test("requires both conclusion and key insight", () => {
  assert.throws(
    () =>
      validateXhsPost({
        title: "DeepBias深挖多模态偏见",
        body: compactResearchBody.replace(
          "\n关键洞察：评测需要随模型反馈更新样本，固定题库会低估动态风险。",
          "",
        ),
      }),
    /必须依次包含论文结论和关键洞察/,
  );
});

test("rejects a duplicated final paper-title line", () => {
  assert.throws(
    () =>
      validateXhsPost({
        title: "DeepBias深挖多模态偏见",
        body: `${compactResearchBody}\n\n论文：DeepBias`,
      }),
    /不要在末尾重复论文标题/,
  );
});

test("does not impose research fields on finance notes", () => {
  const result = validateXhsPost({
    title: "FOMC维持利率",
    body: "官方维持目标区间不变。\n\n后续观察通胀和就业。",
  });
  assert.equal(result.research, false);
});

test("requires one exact AI-content disclosure control", () => {
  assert.throws(
    () => chooseAiDisclosureCandidate([]),
    /XHS_AI_CONTENT_DISCLOSURE_NOT_FOUND/,
  );
  assert.throws(
    () =>
      chooseAiDisclosureCandidate([
        { rect: { x: 1, y: 1, w: 20, h: 20 }, checked: false },
        { rect: { x: 40, y: 1, w: 20, h: 20 }, checked: false },
      ]),
    /XHS_AI_CONTENT_DISCLOSURE_AMBIGUOUS/,
  );
});

test("opens content-type declaration and selects AI-synthetic-content before publish", async () => {
  const snapshots = [
    [],
    [
      {
        label: "添加内容类型声明",
        checked: false,
        rect: { x: 10, y: 20, w: 160, h: 24 },
      },
    ],
    [
      {
        label: "笔记含AI合成内容",
        checked: false,
        rect: { x: 20, y: 60, w: 180, h: 24 },
      },
    ],
    [
      {
        label: "笔记含AI合成内容",
        checked: true,
        rect: { x: 20, y: 60, w: 180, h: 24 },
      },
    ],
  ];
  const clicks = [];
  const inspectedLabels = [];
  const result = await ensureAiAssistedCreation({
    tab: {
      playwright: {
        evaluate: async (_pageFunction, label) => {
          inspectedLabels.push(label);
          return snapshots.shift();
        },
        waitForTimeout: async () => undefined,
      },
      cua: { click: async (point) => clicks.push(point) },
    },
  });
  assert.deepEqual(result, {
    label: "笔记含AI合成内容",
    checked: true,
    clicked: true,
    verification: "native-selected-state",
    candidateAttempts: 1,
    declaration: {
      label: "添加内容类型声明",
      clicked: true,
      alreadyOpen: false,
    },
  });
  assert.deepEqual(inspectedLabels, [
    XHS_AI_CONTENT_DISCLOSURE_LABEL,
    XHS_CONTENT_TYPE_DECLARATION_LABEL,
    XHS_AI_CONTENT_DISCLOSURE_LABEL,
    XHS_AI_CONTENT_DISCLOSURE_LABEL,
  ]);
  assert.deepEqual(clicks, [
    { x: 90, y: 32 },
    { x: 110, y: 72 },
  ]);
});

test("accepts the current AI-content display value without clicking it", async () => {
  let clicked = false;
  const selected = {
    label: "笔记含AI合成内容",
    checked: true,
    rect: { x: 10, y: 20, w: 180, h: 24 },
  };
  const result = await ensureAiContentDisclosure({
    tab: {
      playwright: {
        evaluate: async () => [selected],
        waitForTimeout: async () => undefined,
      },
      cua: { click: async () => { clicked = true; } },
    },
  });
  assert.equal(result.clicked, false);
  assert.equal(result.declaration.clicked, false);
  assert.equal(result.declaration.alreadyOpen, true);
  assert.equal(result.verification, "current-display-value");
  assert.equal(result.candidateAttempts, 0);
  assert.equal(result.visibleCandidates, 1);
  assert.equal(clicked, false);
});

test("accepts duplicate DOM nodes for an already displayed AI-content value", async () => {
  const first = {
    label: "笔记含AI合成内容",
    checked: false,
    rect: { x: 20, y: 60, w: 180, h: 24 },
  };
  const second = {
    label: "笔记含AI合成内容",
    checked: false,
    rect: { x: 20, y: 96, w: 180, h: 24 },
  };
  const snapshots = [[first, second]];
  const clicks = [];
  const result = await ensureAiContentDisclosure({
    tab: {
      playwright: {
        evaluate: async () => snapshots.shift(),
        waitForTimeout: async () => undefined,
      },
      cua: { click: async (point) => clicks.push(point) },
    },
  });
  assert.equal(result.checked, true);
  assert.equal(result.verification, "current-display-value");
  assert.equal(result.candidateAttempts, 0);
  assert.equal(result.visibleCandidates, 2);
  assert.deepEqual(clicks, []);
});

test("accepts the displayed AI-content value after selecting it from the declaration menu", async () => {
  const snapshots = [
    [],
    [
      {
        label: "添加内容类型声明",
        checked: false,
        rect: { x: 10, y: 20, w: 160, h: 24 },
      },
    ],
    [
      {
        label: "笔记含AI合成内容",
        checked: false,
        rect: { x: 20, y: 60, w: 180, h: 24 },
      },
    ],
    [
      {
        label: "笔记含AI合成内容",
        checked: false,
        rect: { x: 20, y: 60, w: 180, h: 24 },
      },
      {
        label: "笔记含AI合成内容",
        checked: false,
        rect: { x: 20, y: 60, w: 150, h: 20 },
      },
    ],
  ];
  const clicks = [];
  const result = await ensureAiContentDisclosure({
    tab: {
      playwright: {
        evaluate: async () => snapshots.shift(),
        waitForTimeout: async () => undefined,
      },
      cua: { click: async (point) => clicks.push(point) },
    },
  });
  assert.equal(result.checked, true);
  assert.equal(result.verification, "current-display-after-selection");
  assert.equal(result.visibleCandidates, 2);
  assert.deepEqual(clicks, [
    { x: 90, y: 32 },
    { x: 110, y: 72 },
  ]);
});

test("stops when every AI-content candidate remains unverified", async () => {
  const snapshots = [
    [],
    [
      {
        label: "添加内容类型声明",
        checked: false,
        rect: { x: 10, y: 20, w: 160, h: 24 },
      },
    ],
    [
      {
        label: "笔记含AI合成内容",
        checked: false,
        rect: { x: 20, y: 60, w: 180, h: 24 },
      },
    ],
    [],
  ];
  await assert.rejects(
    ensureAiContentDisclosure({
      tab: {
        playwright: {
          evaluate: async () => snapshots.shift(),
          waitForTimeout: async () => undefined,
        },
        cua: { click: async () => undefined },
      },
    }),
    /XHS_AI_CONTENT_DISCLOSURE_NOT_VERIFIED candidates=0 tried=1/,
  );
});

test("stops when the content-type declaration entry is missing", async () => {
  const snapshots = [[], []];
  await assert.rejects(
    ensureAiAssistedCreation({
      tab: {
        playwright: {
          evaluate: async () => snapshots.shift(),
          waitForTimeout: async () => undefined,
        },
        cua: { click: async () => undefined },
      },
    }),
    /XHS_CONTENT_TYPE_DECLARATION_NOT_FOUND/,
  );
});

test("computes a Shanghai scheduled time at least ninety minutes later", () => {
  const result = computeScheduledPublishAt("2026-08-09T10:00:30+08:00");
  assert.deepEqual(
    {
      date: result.date,
      time: result.time,
      inputValue: result.inputValue,
      displayValue: result.displayValue,
      delayMinutes: result.delayMinutes,
      timeZone: result.timeZone,
    },
    {
      date: "2026-08-09",
      time: "11:31",
      inputValue: "2026-08-09T11:31",
      displayValue: "2026-08-09 11:31",
      delayMinutes: 90,
      timeZone: "Asia/Shanghai",
    },
  );
  assert.ok(
    result.epochMs - Date.parse("2026-08-09T10:00:30+08:00") >= 90 * 60_000,
  );
});

test("computes a ninety-minute schedule across the Shanghai day boundary", () => {
  const result = computeScheduledPublishAt("2026-08-09T23:55:00+08:00");
  assert.equal(result.displayValue, "2026-08-10 01:25");
});

test("requires scheduled publish readback to contain the date and minute", () => {
  const target = computeScheduledPublishAt("2026-08-09T10:00:00+08:00");
  assert.equal(
    validateScheduledPublishReadback(["2026-08-09", "11:30"], target),
    true,
  );
  assert.throws(
    () => validateScheduledPublishReadback(["2026-08-09", "10:09"], target),
    /XHS_SCHEDULE_TIME_NOT_VERIFIED/,
  );
});

test("selects scheduled publish, writes plus ninety minutes, and verifies it", async () => {
  const snapshots = [
    { fieldCount: 0, publishText: "发布", active: false },
    [{ x: 80, y: 30, w: 40, h: 20 }],
    { fieldCount: 1, publishText: "定时发布", active: true },
    { mode: "datetime-local", keys: ["datetime"] },
    ["2026-08-09T11:30"],
    { fieldCount: 1, publishText: "定时发布", active: true },
  ];
  const clicks = [];
  const fills = [];
  const result = await ensureScheduledPublish({
    now: "2026-08-09T10:00:00+08:00",
    tab: {
      playwright: {
        evaluate: async () => snapshots.shift(),
        locator: (selector) => ({
          count: async () => 1,
          fill: async (value) => fills.push({ selector, value }),
        }),
        waitForTimeout: async () => undefined,
      },
      cua: { click: async (point) => clicks.push(point) },
    },
  });
  assert.equal(result.displayValue, "2026-08-09 11:30");
  assert.equal(result.option.checked, true);
  assert.equal(result.option.verification, "time-field-and-submit-label");
  assert.deepEqual(result.readback, ["2026-08-09T11:30"]);
  assert.deepEqual(clicks, [{ x: 100, y: 40 }]);
  assert.deepEqual(fills, [
    {
      selector: '[data-codex-xhs-schedule-field="datetime"]',
      value: "2026-08-09T11:30",
    },
  ]);
});

test("stops when the scheduled-publish switch itself cannot be located", async () => {
  const snapshots = [
    { fieldCount: 0, publishText: "发布", active: false },
    [],
  ];
  await assert.rejects(
    ensureScheduledPublish({
      now: "2026-08-09T10:00:00+08:00",
      tab: {
        playwright: {
          evaluate: async () => snapshots.shift(),
          waitForTimeout: async () => undefined,
        },
        cua: { click: async () => undefined },
      },
    }),
    /XHS_SCHEDULE_TOGGLE_NOT_FOUND/,
  );
});

test("does not toggle off an already active scheduled publication", async () => {
  const snapshots = [
    { fieldCount: 1, publishText: "定时发布", active: true },
    { mode: "combined-text", keys: ["combined"] },
    ["2026-08-09 11:30"],
    { fieldCount: 1, publishText: "定时发布", active: true },
  ];
  const clicks = [];
  const fills = [];
  const result = await ensureScheduledPublish({
    now: "2026-08-09T10:00:00+08:00",
    tab: {
      playwright: {
        evaluate: async () => snapshots.shift(),
        locator: (selector) => ({
          count: async () => 1,
          fill: async (value) => fills.push({ selector, value }),
        }),
        waitForTimeout: async () => undefined,
      },
      cua: { click: async (point) => clicks.push(point) },
    },
  });
  assert.equal(result.option.clicked, false);
  assert.equal(result.option.verification, "time-field-and-submit-label");
  assert.deepEqual(clicks, []);
  assert.deepEqual(fills, [
    {
      selector: '[data-codex-xhs-schedule-field="combined"]',
      value: "2026-08-09 11:30",
    },
  ]);
});
