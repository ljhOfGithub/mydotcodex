export const XHS_SUBMISSION_POLICY = Object.freeze({
  manualSubmit: true,
  automatedSubmit: false,
});

export const XHS_SCHEDULE_DELAY_MINUTES = 90;
export const XHS_TIME_ZONE = "Asia/Shanghai";
export const XHS_CONTENT_TYPE_DECLARATION_LABEL = "添加内容类型声明";
export const XHS_AI_CONTENT_DISCLOSURE_LABEL = "笔记含AI合成内容";

export function assertXhsPublicationAvailable({ manualSubmit = true } = {}) {
  if (manualSubmit !== true) {
    throw new Error("XHS_AUTOMATED_SUBMISSION_DISABLED manualSubmit=true-required");
  }
  return XHS_SUBMISSION_POLICY;
}

const XHS_AUTOMATION_RISK_PATTERNS = [
  "检测到自动化",
  "自动化脚本",
  "疑似自动化",
  "异常访问",
  "异常操作",
  "操作过于频繁",
  "访问受限",
  "安全验证",
  "请完成验证",
  "机器人验证",
  "robot check",
  "automated access",
];

export function assertNoXhsAutomationRisk(text) {
  const normalized = String(text || "").toLowerCase();
  const matched = XHS_AUTOMATION_RISK_PATTERNS.find((pattern) =>
    normalized.includes(pattern.toLowerCase()),
  );
  if (matched) {
    throw new Error(`XHS_AUTOMATION_OR_RISK_DETECTED matched=${matched}`);
  }
}

async function assertNoVisibleXhsAutomationRisk(tab) {
  const noticeText = await tab.playwright.evaluate(
    () =>
      Array.from(
        document.querySelectorAll(
          '[role="alert"], [role="dialog"], .toast, .el-message, .notification, .reds-notification',
        ),
      )
        .filter((element) => {
          const rect = element.getBoundingClientRect();
          return rect.width > 0 && rect.height > 0;
        })
        .map((element) => (element.innerText || "").trim())
        .filter(Boolean)
        .join("\n"),
    undefined,
    { timeoutMs: 10000 },
  );
  assertNoXhsAutomationRisk(noticeText);
}

async function readUploadState(tab) {
  return tab.playwright.evaluate(
    () => ({
      counter:
        Array.from(document.querySelectorAll("*"))
          .map((element) => (element.innerText || "").trim())
          .find((text) => /^\d+\/18$/.test(text)) || "",
      titleCount: document.querySelectorAll(
        'input[placeholder="填写标题会有更多赞哦"]',
      ).length,
      editorCount: document.querySelectorAll('[contenteditable="true"]')
        .length,
    }),
    undefined,
    { timeoutMs: 10000 },
  );
}

export async function uploadFilesSequentially({
  tab,
  openChooser,
  files,
  startIndex = 0,
}) {
  if (!Array.isArray(files) || files.length === 0) {
    throw new Error("XHS_SEQUENTIAL_UPLOAD_FILES_REQUIRED");
  }
  if (typeof openChooser !== "function") {
    throw new Error("XHS_SEQUENTIAL_UPLOAD_CHOOSER_REQUIRED");
  }
  if (!Number.isInteger(startIndex) || startIndex < 0 || startIndex >= 18) {
    throw new Error("XHS_SEQUENTIAL_UPLOAD_START_INDEX_INVALID");
  }
  if (startIndex + files.length > 18) {
    throw new Error("XHS_SEQUENTIAL_UPLOAD_LIMIT_EXCEEDED");
  }
  let uploaded = null;
  for (let fileIndex = 0; fileIndex < files.length; fileIndex += 1) {
    const index = startIndex + fileIndex;
    const chooser = await openChooser(index);
    await chooser.setFiles([files[fileIndex]], { timeoutMs: 60000 });
    const expectedCounter = `${index + 1}/18`;
    const deadline = Date.now() + 60000;
    do {
      uploaded = await readUploadState(tab);
      if (uploaded.counter === expectedCounter) break;
      await tab.playwright.waitForTimeout(500);
    } while (Date.now() < deadline);
    if (uploaded?.counter !== expectedCounter) {
      throw new Error(
        `XHS_SEQUENTIAL_UPLOAD_COUNT_NOT_VERIFIED expected=${expectedCounter} actual=${uploaded?.counter || "none"}`,
      );
    }
    await tab.playwright.waitForTimeout(1500);
    uploaded = await readUploadState(tab);
    if (uploaded.counter !== expectedCounter) {
      throw new Error(
        `XHS_SEQUENTIAL_UPLOAD_COUNT_UNSTABLE expected=${expectedCounter} actual=${uploaded.counter || "none"}`,
      );
    }
    await assertNoVisibleXhsAutomationRisk(tab);
  }
  return uploaded;
}

export async function resolveImageUploadControl({
  tab,
  index,
  initialUploadButton,
}) {
  if (index === 0) return initialUploadButton;
  const addImageEntries = tab.playwright.locator(".img-upload-area .entry");
  const visible = [];
  for (let candidateIndex = 0; candidateIndex < (await addImageEntries.count()); candidateIndex += 1) {
    const candidate = addImageEntries.nth(candidateIndex);
    if (await candidate.isVisible()) visible.push(candidate);
  }
  if (visible.length !== 1) {
    throw new Error(
      `XHS_SEQUENTIAL_UPLOAD_ADD_ENTRY_NOT_UNIQUE index=${index + 1} visible=${visible.length}`,
    );
  }
  return visible[0];
}

export async function selectImageTextUploadMode(tab) {
  const buttons = tab.playwright.getByRole("button", {
    name: "上传图片",
    exact: true,
  });
  const uniqueVisualTargets = async (locator, expectedText = null) => {
    const targets = new Map();
    let visibleNodes = 0;
    for (let index = 0; index < (await locator.count()); index += 1) {
      const candidate = locator.nth(index);
      if (!(await candidate.isVisible())) continue;
      if (
        expectedText !== null &&
        (await candidate.innerText({ timeoutMs: 10000 })).trim() !== expectedText
      ) {
        continue;
      }
      visibleNodes += 1;
      const box = await candidate.boundingBox();
      if (!box || box.width <= 0 || box.height <= 0 || box.x < 0 || box.y < 0) {
        continue;
      }
      const key = [box.x, box.y, box.width, box.height]
        .map((value) => Math.round(value))
        .join(":");
      if (!targets.has(key)) targets.set(key, box);
    }
    return { boxes: [...targets.values()], visibleNodes };
  };
  const mouseControl = (box) => ({
    click: async () => tab.cua.click({
      x: box.x + box.width / 2,
      y: box.y + box.height / 2,
    }),
  });
  const visibleUploadButtons = async () => {
    const visual = await uniqueVisualTargets(buttons);
    return {
      ...visual,
      control: visual.boxes.length === 1 ? mouseControl(visual.boxes[0]) : null,
    };
  };
  const alreadyVisible = await visibleUploadButtons();
  if (alreadyVisible.boxes.length === 1) return alreadyVisible.control;
  if (alreadyVisible.boxes.length > 1) {
    throw new Error(
      `XHS_IMAGE_TEXT_UPLOAD_BUTTON_NOT_UNIQUE visual=${alreadyVisible.boxes.length} nodes=${alreadyVisible.visibleNodes}`,
    );
  }

  const tabs = tab.playwright.locator(".creator-tab");
  const imageTextTabs = await uniqueVisualTargets(tabs, "上传图文");
  if (imageTextTabs.boxes.length !== 1) {
    throw new Error(
      `XHS_IMAGE_TEXT_MODE_ENTRY_NOT_UNIQUE visual=${imageTextTabs.boxes.length} nodes=${imageTextTabs.visibleNodes}`,
    );
  }
  await mouseControl(imageTextTabs.boxes[0]).click();

  const deadline = Date.now() + 15000;
  while (Date.now() < deadline) {
    const visible = await visibleUploadButtons();
    if (visible.boxes.length === 1) return visible.control;
    if (visible.boxes.length > 1) {
      throw new Error(
        `XHS_IMAGE_TEXT_UPLOAD_BUTTON_NOT_UNIQUE visual=${visible.boxes.length} nodes=${visible.visibleNodes}`,
      );
    }
    await tab.playwright.waitForTimeout(250);
  }
  throw new Error("XHS_IMAGE_TEXT_UPLOAD_BUTTON_NOT_UNIQUE visible=0");
}

export async function openImageFileChooser({ tab, uploadControl, index }) {
  let chooserError = null;
  const chooserPromise = tab.playwright
    .waitForEvent("filechooser", { timeoutMs: 10000 })
    .catch((error) => {
      chooserError = error;
      return null;
    });
  try {
    await uploadControl.click({ timeoutMs: 10000 });
    const chooser = await chooserPromise;
    if (!chooser) throw chooserError || new Error("filechooser unavailable");
    return chooser;
  } catch (error) {
    await chooserPromise;
    throw new Error(
      `XHS_SEQUENTIAL_UPLOAD_CHOOSER_NOT_OPENED index=${index + 1} ${error.message || error}`,
    );
  }
}

function shanghaiParts(timestamp) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: XHS_TIME_ZONE,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
  }).formatToParts(new Date(timestamp));
  return Object.fromEntries(
    parts
      .filter((part) => part.type !== "literal")
      .map((part) => [part.type, part.value]),
  );
}

export function computeScheduledPublishAt(now = Date.now()) {
  const timestamp = new Date(now).getTime();
  if (!Number.isFinite(timestamp)) throw new Error("XHS_SCHEDULE_TIME_INVALID");
  const exactTarget = timestamp + XHS_SCHEDULE_DELAY_MINUTES * 60_000;
  const scheduledAt = Math.ceil(exactTarget / 60_000) * 60_000;
  const { year, month, day, hour, minute } = shanghaiParts(scheduledAt);
  const date = `${year}-${month}-${day}`;
  const time = `${hour}:${minute}`;
  return {
    delayMinutes: XHS_SCHEDULE_DELAY_MINUTES,
    timeZone: XHS_TIME_ZONE,
    epochMs: scheduledAt,
    date,
    time,
    inputValue: `${date}T${time}`,
    displayValue: `${date} ${time}`,
  };
}

function dedupeRects(rects) {
  const unique = [];
  for (const rect of rects) {
    const duplicate = unique.some(
      (item) =>
        item.x === rect.x &&
        item.y === rect.y &&
        item.w === rect.w &&
        item.h === rect.h,
    );
    if (!duplicate) unique.push(rect);
  }
  return unique;
}

const RESEARCH_MARKERS = [
  "📝一句话总结",
  "🔑关键方法",
  "💡核心创新",
  "⚠️限制与边界",
  "🧭结论和关键洞察",
];

function validateResearchBody(body) {
  const markerIndexes = RESEARCH_MARKERS.map((marker) => body.indexOf(marker));
  const isResearch = markerIndexes.some((index) => index >= 0);
  if (!isResearch) return { research: false, compactSections: 0 };

  if (!body.includes("🎓 来源机构：")) {
    throw new Error("科研小红书正文缺少来源机构");
  }
  if (!body.includes("🔍 背景难点：")) {
    throw new Error("科研小红书正文缺少背景难点");
  }
  if (/^论文：/m.test(body)) {
    throw new Error("科研小红书正文不要在末尾重复论文标题");
  }
  if (body.includes("📊实验效果")) {
    throw new Error("科研小红书正文不要保留独立实验效果章节");
  }
  if (markerIndexes.some((index) => index < 0)) {
    throw new Error("科研小红书正文缺少固定章节");
  }
  for (let index = 1; index < markerIndexes.length; index += 1) {
    if (markerIndexes[index] <= markerIndexes[index - 1]) {
      throw new Error("科研小红书章节顺序错误");
    }
  }

  const contextEnd = markerIndexes[0];
  if (
    body.indexOf("🎓 来源机构：") >= contextEnd ||
    body.indexOf("🔍 背景难点：") >= contextEnd
  ) {
    throw new Error("来源机构和背景难点必须位于一句话总结之前");
  }

  for (let index = 0; index < RESEARCH_MARKERS.length; index += 1) {
    const marker = RESEARCH_MARKERS[index];
    const markerIndex = markerIndexes[index];
    const prefix = body.slice(0, markerIndex);
    if (
      !/\r?\n[ \t]*\r?\n$/.test(prefix) ||
      /(?:\r?\n[ \t]*){3,}$/.test(prefix)
    ) {
      throw new Error(`${marker} 前必须且只能有一行空行`);
    }

    const sectionEnd =
      index + 1 < RESEARCH_MARKERS.length
        ? markerIndexes[index + 1]
        : body.length;
    const rawSection = body.slice(markerIndex + marker.length, sectionEnd);
    if (!/^\r?\n/.test(rawSection) || /^\r?\n[ \t]*\r?\n/.test(rawSection)) {
      throw new Error(`${marker} 标题后不得有空行`);
    }
    const sectionContent = rawSection
      .replace(/^\r?\n/, "")
      .replace(/[ \t\r\n]+$/, "");
    if (/\r?\n[ \t]*\r?\n/.test(sectionContent)) {
      throw new Error(`${marker} 章节内部不得有空行`);
    }
  }

  const summaryMarker = RESEARCH_MARKERS[0];
  const summaryLines = body
    .slice(
      markerIndexes[0] + summaryMarker.length,
      markerIndexes[1],
    )
    .trim()
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  if (summaryLines.length !== 1 || summaryLines[0].length === 0) {
    throw new Error("一句话总结必须且只能包含一行内容");
  }

  const insightMarker = RESEARCH_MARKERS[RESEARCH_MARKERS.length - 1];
  const insightIndex = markerIndexes[markerIndexes.length - 1];
  const insightLines = body
    .slice(insightIndex + insightMarker.length)
    .trim()
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  const requiredInsightPrefixes = ["论文结论：", "关键洞察："];
  if (
    insightLines.length !== requiredInsightPrefixes.length ||
    requiredInsightPrefixes.some(
      (prefix, index) =>
        !insightLines[index]?.startsWith(prefix) ||
        insightLines[index].length === prefix.length,
    )
  ) {
    throw new Error(
      "结论和关键洞察必须依次包含论文结论和关键洞察",
    );
  }

  return { research: true, compactSections: RESEARCH_MARKERS.length };
}

export function validateXhsPost({ title, body }) {
  const researchLayout = validateResearchBody(body);
  const result = {
    titleLength: Array.from(title).length,
    bodyLength: Array.from(body).length,
    prohibited: /白Yu 观测|howto|抢救|反常识|<ul>|<li>/.test(
      `${title}\n${body}`,
    ),
    ...researchLayout,
  };
  if (result.titleLength > 20) {
    throw new Error(`小红书标题超过 20 字符: ${result.titleLength}`);
  }
  if (result.bodyLength > 1000) {
    throw new Error(`小红书正文超过 1000 字符: ${result.bodyLength}`);
  }
  if (result.prohibited) throw new Error("小红书内容命中禁止项");
  return result;
}

function uniqueLabeledCandidates(candidates) {
  const unique = [];
  for (const candidate of candidates || []) {
    const rect = candidate?.rect;
    if (!rect || rect.w <= 0 || rect.h <= 0) continue;
    const duplicate = unique.some(
      (item) =>
        item.rect.x === rect.x &&
        item.rect.y === rect.y &&
        item.rect.w === rect.w &&
        item.rect.h === rect.h,
    );
    if (!duplicate) unique.push(candidate);
  }
  return unique;
}

function chooseLabeledCandidate(candidates, errorPrefix) {
  const unique = uniqueLabeledCandidates(candidates);
  if (unique.length === 0) {
    throw new Error(`${errorPrefix}_NOT_FOUND`);
  }
  if (unique.length !== 1) {
    throw new Error(`${errorPrefix}_AMBIGUOUS count=${unique.length}`);
  }
  return unique[0];
}

export function chooseAiDisclosureCandidate(candidates) {
  return chooseLabeledCandidate(candidates, "XHS_AI_CONTENT_DISCLOSURE");
}

async function inspectLabeledControl(tab, canonicalLabel) {
  return tab.playwright.evaluate(
    (targetLabel) => {
      const normalize = (value) =>
        String(value || "").replace(/\s+/g, " ").trim();
      const canonicalize = (value) =>
        normalize(value).replace(/\s+/g, "").toUpperCase();
      const isVisible = (element) => {
        const rect = element.getBoundingClientRect();
        const style = window.getComputedStyle(element);
        return (
          rect.width > 0 &&
          rect.height > 0 &&
          style.display !== "none" &&
          style.visibility !== "hidden"
        );
      };
      const stateIsChecked = (element) => {
        if (!element) return false;
        if (
          element instanceof HTMLInputElement &&
          ["checkbox", "radio"].includes(element.type)
        ) {
          return element.checked;
        }
        if (element.getAttribute("aria-checked") === "true") return true;
        if (element.getAttribute("aria-selected") === "true") return true;
        if (element.getAttribute("data-state") === "checked") return true;
        const className = String(element.className || "");
        return /(?:^|[\s_-])(?:is-)?(?:checked|selected|active)(?:$|[\s_-])/.test(
          className,
        );
      };
      const exactNodes = Array.from(
        document.querySelectorAll("label, span, p, div"),
      ).filter(
        (element) =>
          isVisible(element) &&
          canonicalize(element.innerText) === targetLabel &&
          !Array.from(element.children).some(
            (child) =>
              isVisible(child) && canonicalize(child.innerText) === targetLabel,
          ),
      );
      if (exactNodes.length === 1) {
        exactNodes[0].scrollIntoView({ block: "center", inline: "nearest" });
      }
      return exactNodes.map((textNode) => {
        const label = textNode.closest("label");
        let scope = textNode;
        let control = null;
        for (let depth = 0; scope && depth < 6; depth += 1) {
          control = scope.matches(
            'input[type="checkbox"], input[type="radio"], [role="checkbox"], [role="radio"]',
          )
            ? scope
            : scope.querySelector(
                'input[type="checkbox"], input[type="radio"], [role="checkbox"], [role="radio"]',
              );
          if (control) break;
          scope = scope.parentElement;
        }
        if (!control && label?.htmlFor) {
          control = document.getElementById(label.htmlFor);
        }
        const clickTarget =
          (label && isVisible(label) && label) ||
          (control && isVisible(control) && control) ||
          textNode;
        const rect = clickTarget.getBoundingClientRect();
        return {
          label: normalize(textNode.innerText),
          checked: [control, label, scope].some(stateIsChecked),
          rect: { x: rect.x, y: rect.y, w: rect.width, h: rect.height },
        };
      });
    },
    String(canonicalLabel || "").replace(/\s+/g, "").toUpperCase(),
    { timeoutMs: 10000 },
  );
}

async function ensureLabeledControlChecked({ tab, label, errorPrefix }) {
  const initial = chooseLabeledCandidate(
    await inspectLabeledControl(tab, label),
    errorPrefix,
  );
  if (initial.checked) {
    return { label: initial.label, checked: true, clicked: false };
  }
  await tab.cua.click({
    x: initial.rect.x + initial.rect.w / 2,
    y: initial.rect.y + initial.rect.h / 2,
  });
  await tab.playwright.waitForTimeout(500);
  const verified = chooseLabeledCandidate(
    await inspectLabeledControl(tab, label),
    errorPrefix,
  );
  if (!verified.checked) {
    throw new Error(`${errorPrefix}_NOT_CHECKED`);
  }
  return { label: verified.label, checked: true, clicked: true };
}

function candidateRectKey(candidate) {
  const rect = candidate.rect;
  return [rect.x, rect.y, rect.w, rect.h].join(":");
}

async function selectAiContentDisclosure({ tab, candidates }) {
  let current = uniqueLabeledCandidates(candidates);
  const tried = new Set();
  const attempts = [];

  for (let attempt = 0; attempt < 4; attempt += 1) {
    const selected = current.find((candidate) => candidate.checked);
    if (selected) {
      return {
        label: selected.label,
        checked: true,
        clicked: attempts.length > 0,
        verification: "native-selected-state",
        candidateAttempts: attempts.length,
      };
    }

    const candidate = current.find(
      (item) => !tried.has(candidateRectKey(item)),
    );
    if (!candidate) break;
    tried.add(candidateRectKey(candidate));
    attempts.push(candidateRectKey(candidate));
    await tab.cua.click({
      x: candidate.rect.x + candidate.rect.w / 2,
      y: candidate.rect.y + candidate.rect.h / 2,
    });
    await tab.playwright.waitForTimeout(500);

    const after = uniqueLabeledCandidates(
      await inspectLabeledControl(tab, XHS_AI_CONTENT_DISCLOSURE_LABEL),
    );
    const selectedAfter = after.find((item) => item.checked);
    if (selectedAfter) {
      return {
        label: selectedAfter.label,
        checked: true,
        clicked: true,
        verification: "native-selected-state",
        candidateAttempts: attempts.length,
      };
    }
    if (after.length > 0) {
      return {
        label: after[0].label,
        checked: true,
        clicked: true,
        verification: "current-display-after-selection",
        candidateAttempts: attempts.length,
        visibleCandidates: after.length,
      };
    }
    current = after;
  }

  throw new Error(
    `XHS_AI_CONTENT_DISCLOSURE_NOT_VERIFIED candidates=${current.length} tried=${attempts.length}`,
  );
}

export async function ensureAiAssistedCreation({ tab }) {
  const visibleDisclosure = await inspectLabeledControl(
    tab,
    XHS_AI_CONTENT_DISCLOSURE_LABEL,
  );
  if (visibleDisclosure.length > 0) {
    return {
      label: visibleDisclosure[0].label,
      checked: true,
      clicked: false,
      verification: "current-display-value",
      candidateAttempts: 0,
      visibleCandidates: uniqueLabeledCandidates(visibleDisclosure).length,
      declaration: {
        label: XHS_CONTENT_TYPE_DECLARATION_LABEL,
        clicked: false,
        alreadyOpen: true,
      },
    };
  }

  let declaration = {
    label: XHS_CONTENT_TYPE_DECLARATION_LABEL,
    clicked: false,
    alreadyOpen: false,
  };

  const entry = chooseLabeledCandidate(
    await inspectLabeledControl(tab, XHS_CONTENT_TYPE_DECLARATION_LABEL),
    "XHS_CONTENT_TYPE_DECLARATION",
  );
  await tab.cua.click({
    x: entry.rect.x + entry.rect.w / 2,
    y: entry.rect.y + entry.rect.h / 2,
  });
  await tab.playwright.waitForTimeout(500);
  declaration = {
    label: entry.label,
    clicked: true,
    alreadyOpen: false,
  };

  const disclosure = await selectAiContentDisclosure({
    tab,
    candidates: await inspectLabeledControl(
      tab,
      XHS_AI_CONTENT_DISCLOSURE_LABEL,
    ),
  });
  return { ...disclosure, declaration };
}

export const ensureAiContentDisclosure = ensureAiAssistedCreation;

async function writeScheduledPublishFields(tab, target) {
  const plan = await tab.playwright.evaluate(
    () => {
      const isVisible = (element) => {
        const rect = element.getBoundingClientRect();
        const style = window.getComputedStyle(element);
        return (
          rect.width > 0 &&
          rect.height > 0 &&
          style.display !== "none" &&
          style.visibility !== "hidden"
        );
      };
      const fields = Array.from(document.querySelectorAll("input"))
        .filter(isVisible)
        .filter(
          (element) =>
            element.type === "date" ||
            element.type === "time" ||
            element.type === "datetime-local" ||
            /^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}$/.test(
              String(element.value || "").trim(),
            ) ||
            /定时|发布.*时间|日期|时间/.test(
              `${element.placeholder || ""} ${element.getAttribute("aria-label") || ""}`,
            ),
        );
      const dateFields = fields.filter(
        (element) =>
          element.type === "date" ||
          /日期/.test(`${element.placeholder || ""} ${element.getAttribute("aria-label") || ""}`),
      );
      const timeFields = fields.filter(
        (element) =>
          element.type === "time" ||
          /时间/.test(`${element.placeholder || ""} ${element.getAttribute("aria-label") || ""}`),
      );
      const datetimeFields = fields.filter(
        (element) => element.type === "datetime-local",
      );

      for (const element of document.querySelectorAll(
        "[data-codex-xhs-schedule-field]",
      )) {
        element.removeAttribute("data-codex-xhs-schedule-field");
      }
      if (datetimeFields.length === 1) {
        datetimeFields[0].setAttribute("data-codex-xhs-schedule-field", "datetime");
        return { mode: "datetime-local", keys: ["datetime"] };
      }
      if (dateFields.length === 1 && timeFields.length === 1) {
        dateFields[0].setAttribute("data-codex-xhs-schedule-field", "date");
        timeFields[0].setAttribute("data-codex-xhs-schedule-field", "time");
        return { mode: "date-and-time", keys: ["date", "time"] };
      }
      if (fields.length === 1) {
        fields[0].setAttribute("data-codex-xhs-schedule-field", "combined");
        return { mode: "combined-text", keys: ["combined"] };
      }
      throw new Error(`XHS_SCHEDULE_FIELDS_NOT_UNIQUE count=${fields.length}`);
    },
    undefined,
    { timeoutMs: 10000 },
  );
  const values = {
    datetime: target.inputValue,
    date: target.date,
    time: target.time,
    combined: target.displayValue,
  };
  const written = [];
  for (const key of plan.keys) {
    const field = tab.playwright.locator(
      `[data-codex-xhs-schedule-field="${key}"]`,
    );
    if ((await field.count()) !== 1) {
      throw new Error(`XHS_SCHEDULE_FIELD_NOT_UNIQUE key=${key}`);
    }
    await field.fill(values[key], { timeoutMs: 10000 });
    written.push(values[key]);
  }
  return { mode: plan.mode, written };
}

async function readScheduledPublishFields(tab) {
  return tab.playwright.evaluate(
    () => {
      const isVisible = (element) => {
        const rect = element.getBoundingClientRect();
        const style = window.getComputedStyle(element);
        return (
          rect.width > 0 &&
          rect.height > 0 &&
          style.display !== "none" &&
          style.visibility !== "hidden"
        );
      };
      return Array.from(document.querySelectorAll("input"))
        .filter(isVisible)
        .filter(
          (element) =>
            element.type === "date" ||
            element.type === "time" ||
            element.type === "datetime-local" ||
            /^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}$/.test(
              String(element.value || "").trim(),
            ) ||
            /定时|发布.*时间|日期|时间/.test(
              `${element.placeholder || ""} ${element.getAttribute("aria-label") || ""}`,
            ),
        )
        .map((element) => String(element.value || "").trim());
    },
    undefined,
    { timeoutMs: 10000 },
  );
}

export function validateScheduledPublishReadback(values, target) {
  const compact = (value) => String(value || "").replace(/\D/g, "");
  const actual = compact((values || []).join(" "));
  const expectedDate = compact(target.date);
  const expectedTime = compact(target.time);
  if (!actual.includes(expectedDate) || !actual.includes(expectedTime)) {
    throw new Error(
      `XHS_SCHEDULE_TIME_NOT_VERIFIED expected=${target.displayValue} actual=${JSON.stringify(values || [])}`,
    );
  }
  return true;
}

async function inspectScheduledPublishActivation(tab) {
  return tab.playwright.evaluate(
    () => {
      const isVisible = (element) => {
        const rect = element.getBoundingClientRect();
        const style = window.getComputedStyle(element);
        return (
          rect.width > 0 &&
          rect.height > 0 &&
          style.display !== "none" &&
          style.visibility !== "hidden"
        );
      };
      const scheduleFields = Array.from(document.querySelectorAll("input"))
        .filter(isVisible)
        .filter(
          (element) =>
            element.type === "date" ||
            element.type === "time" ||
            element.type === "datetime-local" ||
            /^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}$/.test(
              String(element.value || "").trim(),
            ) ||
            /定时|发布.*时间|日期|时间/.test(
              `${element.placeholder || ""} ${element.getAttribute("aria-label") || ""}`,
            ),
        );
      const publishControl = document.querySelector("xhs-publish-btn");
      const publishText = String(
        publishControl?.getAttribute("submit-text") || "",
      ).trim();
      return {
        fieldCount: scheduleFields.length,
        publishText,
        active: scheduleFields.length > 0 && publishText === "定时发布",
      };
    },
    undefined,
    { timeoutMs: 10000 },
  );
}

async function inspectScheduledPublishToggle(tab) {
  return tab.playwright.evaluate(
    () => {
      const normalize = (value) => String(value || "").replace(/\s+/g, " ").trim();
      const isVisible = (element) => {
        const rect = element.getBoundingClientRect();
        const style = window.getComputedStyle(element);
        return (
          rect.width > 0 &&
          rect.height > 0 &&
          style.display !== "none" &&
          style.visibility !== "hidden"
        );
      };
      const exactLabels = Array.from(
        document.querySelectorAll("label, span, p, div"),
      ).filter(
        (element) =>
          isVisible(element) &&
          normalize(element.innerText) === "定时发布" &&
          !Array.from(element.children).some(
            (child) => isVisible(child) && normalize(child.innerText) === "定时发布",
          ),
      );
      if (exactLabels.length === 1) {
        exactLabels[0].scrollIntoView({ block: "center", inline: "nearest" });
      }
      const candidates = [];
      for (const label of exactLabels) {
        const labelRect = label.getBoundingClientRect();
        let scope = label.parentElement;
        for (let depth = 0; scope && depth < 6; depth += 1) {
          const scopeRect = scope.getBoundingClientRect();
          if (scopeRect.width > 700 || scopeRect.height > 120) break;
          const controls = Array.from(
            scope.querySelectorAll(
              '[role="switch"], input[type="checkbox"], button, [class*="switch" i], [class*="toggle" i]',
            ),
          )
            .filter(isVisible)
            .map((element) => {
              const rect = element.getBoundingClientRect();
              return { x: rect.x, y: rect.y, w: rect.width, h: rect.height };
            })
            .filter(
              (rect) =>
                rect.x > labelRect.right + 12 &&
                rect.w >= 28 &&
                rect.w <= 100 &&
                rect.h >= 14 &&
                rect.h <= 60,
            )
            .sort((left, right) => right.w * right.h - left.w * left.h);
          if (controls.length > 0) {
            candidates.push(controls[0]);
            break;
          }
          scope = scope.parentElement;
        }
      }
      return candidates.filter(
        (rect, index, all) =>
          !all.some(
            (other, otherIndex) =>
              otherIndex < index &&
              other.x === rect.x &&
              other.y === rect.y &&
              other.w === rect.w &&
              other.h === rect.h,
          ),
      );
    },
    undefined,
    { timeoutMs: 10000 },
  );
}

export async function ensureScheduledPublish({ tab, now }) {
  let activation = await inspectScheduledPublishActivation(tab);
  let clicked = false;
  if (!activation.active) {
    const toggles = await inspectScheduledPublishToggle(tab);
    if (toggles.length === 0) {
      throw new Error("XHS_SCHEDULE_TOGGLE_NOT_FOUND");
    }
    if (toggles.length !== 1) {
      throw new Error(`XHS_SCHEDULE_TOGGLE_AMBIGUOUS count=${toggles.length}`);
    }
    const option = toggles[0];
    await tab.cua.click({
      x: option.x + option.w / 2,
      y: option.y + option.h / 2,
    });
    clicked = true;
    await tab.playwright.waitForTimeout(500);
    activation = await inspectScheduledPublishActivation(tab);
  }
  if (!activation.active) {
    throw new Error(
      `XHS_SCHEDULE_OPTION_NOT_ACTIVE fields=${activation.fieldCount} submitText=${JSON.stringify(activation.publishText)}`,
    );
  }
  const target = computeScheduledPublishAt(now);
  const fields = await writeScheduledPublishFields(tab, target);
  await tab.playwright.waitForTimeout(500);
  const readback = await readScheduledPublishFields(tab);
  validateScheduledPublishReadback(readback, target);
  const verifiedActivation = await inspectScheduledPublishActivation(tab);
  if (!verifiedActivation.active) {
    throw new Error(
      `XHS_SCHEDULE_OPTION_LOST fields=${verifiedActivation.fieldCount} submitText=${JSON.stringify(verifiedActivation.publishText)}`,
    );
  }
  return {
    ...target,
    option: {
      label: "定时发布",
      checked: true,
      clicked,
      verification: "time-field-and-submit-label",
      activation: verifiedActivation,
    },
    fields,
    readback,
  };
}

export function validateManualSubmitReadiness(
  readiness,
  { title, body, images },
) {
  const normalize = (value) => String(value || "").replace(/\s+/g, " ").trim();
  if (readiness?.title !== title) {
    throw new Error("XHS_MANUAL_SUBMIT_TITLE_NOT_VERIFIED");
  }
  if (!normalize(readiness?.body).startsWith(normalize(body))) {
    throw new Error("XHS_MANUAL_SUBMIT_BODY_NOT_VERIFIED");
  }
  if (readiness?.counter !== `${images}/18`) {
    throw new Error(
      `XHS_MANUAL_SUBMIT_IMAGE_COUNT_NOT_VERIFIED expected=${images}/18 actual=${readiness?.counter || "none"}`,
    );
  }
  if (
    readiness?.publishText !== "发布" ||
    readiness?.publishDisabled === "true" ||
    readiness?.publishVisible !== true
  ) {
    throw new Error("XHS_MANUAL_SUBMIT_CONTROL_NOT_READY");
  }
  return true;
}

export async function prepareExistingXhsEditor({
  tab,
  title,
  body,
  images,
  manualSubmit = true,
}) {
  assertXhsPublicationAvailable({ manualSubmit });
  validateXhsPost({ title, body });
  const titleBox = tab.playwright.getByPlaceholder(
    "填写标题会有更多赞哦",
    { exact: true },
  );
  const editor = tab.playwright.locator('[contenteditable="true"]');
  await titleBox.fill(title, { timeoutMs: 10000 });
  await tab.playwright.waitForTimeout(1000);
  await assertNoVisibleXhsAutomationRisk(tab);
  await editor.fill(body, { timeoutMs: 10000 });
  await tab.playwright.waitForTimeout(1500);
  await assertNoVisibleXhsAutomationRisk(tab);

  await tab.dom_cua.scroll({ x: 0, y: 1200 });
  await tab.playwright.waitForTimeout(500);
  const aiAssistedCreation = await ensureAiAssistedCreation({ tab });
  const readiness = await tab.playwright.evaluate(
    () => {
      const titleInput = document.querySelector(
        'input[placeholder="填写标题会有更多赞哦"]',
      );
      const editor = document.querySelector('[contenteditable="true"]');
      const publish = document.querySelector("xhs-publish-btn");
      const publishRect = publish?.getBoundingClientRect();
      return {
        title: String(titleInput?.value || ""),
        body: String(editor?.innerText || editor?.textContent || ""),
        counter:
          Array.from(document.querySelectorAll("*"))
            .map((element) => (element.innerText || "").trim())
            .find((text) => /^\d+\/18$/.test(text)) || "",
        publishText: String(publish?.getAttribute("submit-text") || "").trim(),
        publishDisabled: publish?.getAttribute("submit-disabled") || "",
        publishVisible: Boolean(
          publishRect && publishRect.width > 0 && publishRect.height > 0,
        ),
      };
    },
    undefined,
    { timeoutMs: 10000 },
  );
  validateManualSubmitReadiness(readiness, { title, body, images });
  await assertNoVisibleXhsAutomationRisk(tab);
  return { aiAssistedCreation, readiness };
}

export async function publishPreparedXhs({
  tab,
  files,
  title,
  body,
  manualSubmit = true,
}) {
  assertXhsPublicationAvailable({ manualSubmit });
  validateXhsPost({ title, body });

  const uploadButton = await selectImageTextUploadMode(tab);
  await assertNoVisibleXhsAutomationRisk(tab);

  const uploaded = await uploadFilesSequentially({
    tab,
    files,
    openChooser: async (index) => {
      await assertNoVisibleXhsAutomationRisk(tab);
      const uploadControl = await resolveImageUploadControl({
        tab,
        index,
        initialUploadButton: uploadButton,
      });
      return openImageFileChooser({ tab, uploadControl, index });
    },
  });
  if (
    uploaded.counter !== `${files.length}/18` ||
    uploaded.titleCount !== 1 ||
    uploaded.editorCount !== 1
  ) {
    throw new Error(`上传后页面校验失败: ${JSON.stringify(uploaded)}`);
  }

  const prepared = await prepareExistingXhsEditor({
    tab,
    title,
    body,
    images: files.length,
    manualSubmit,
  });
  return {
    status: "ready-for-manual-submit",
    title,
    images: files.length,
    url: await tab.url(),
    aiAssistedCreation: prepared.aiAssistedCreation,
    submitted: false,
    scheduled: false,
    pagePreservationRequested: true,
    preserveReason: "manual-submit",
  };
}
