---
name: paper-communication-layers
description: Turn an evidence-grounded paper analysis into spoken summaries at one-sentence, 30-second, 2-minute, 3-minute, and 10-minute lengths, plus interview follow-up answers. Use when the user asks how to quickly explain, present, pitch, or defend a paper; this complements paper reading/search skills and does not replace full-text verification.
---

# Paper Communication Layers

Convert an already verified paper analysis into presentation-ready Chinese at the requested duration. Preserve the paper's evidence boundary and do not add claims merely to make the story smoother.

## Required Evidence

- Work from the paper, a full-text reading report, or clearly labelled metadata/abstract evidence.
- Separate paper facts, analyst interpretation, and the user's personal contribution.
- Write `论文中未明确说明` when evidence is missing.
- Use at most the few numbers needed to support the main claim. Do not turn the short versions into metric lists.

## Shared Content Spine

Build every duration from the same six elements:

1. **问题**：具体任务及其现实后果。
2. **旧方法缺口**：现有方法在哪个可观察条件下失效。
3. **洞察**：作者对根本原因或可利用结构的判断。
4. **设计选择**：作者因此采用的关键机制。
5. **关键证据**：最能支持主张的实验，不等同于挑最高数字。
6. **代价与边界**：计算、数据、假设、泛化或证据限制。

## Output Layers

### 一句话版

Exactly one Chinese sentence combining `任务 + 核心机制 + 最强且有边界的结论`. It must still make sense without the paper title. Avoid empty claims such as “提出新方法并取得最优结果”.

### 30 秒版

Cover `问题 -> 洞察 -> 方法`. Target roughly 100–150 Chinese characters, adjusted for natural speech. Omit secondary modules and most metrics.

### 2 分钟版

Cover `问题 -> 旧方法缺口 -> 洞察 -> 设计选择 -> 关键证据 -> 代价`. Target roughly 350–550 Chinese characters. Explain why the method follows from the insight; do not merely enumerate architecture components.

### 3 分钟版

Add the experimental setting, comparison basis, strongest result, and evidence boundary to the 2-minute version. Target roughly 550–800 Chinese characters.

### 10 分钟版

Organize by slides. For every slide provide `标题`, `要讲的点`, and `可直接口播的话`. The usual order is problem, prior-work gap, key observation, method, experiment setup, main evidence, ablation/failure cases, limitations, and takeaway.

### 面试追问版

Prepare concise answers to:

- 为什么这个方法可能有效？
- 哪个实验真正支持核心主张？
- 证据哪里还不够？
- 最强替代解释是什么？
- 如果重做，最先补哪个实验？
- 你个人具体做了什么？

For the final question, use only contribution evidence supplied by the user or source materials. Never infer authorship contribution from author order, acknowledgements, or the paper's method.

## Multi-paper Use

For multiple papers, produce the required layers for each paper, then add one cross-paper sentence describing their relationship. Do not collapse distinct tasks, datasets, or metrics into a single result claim.

## Routing

- With `$paper-deep-presentation`, include all six output layers in the single-paper report.
- With `$research-paper-search-report`, include the one-sentence and 2-minute layers for each selected paper by default; add longer layers only when requested so a batch report remains usable.

