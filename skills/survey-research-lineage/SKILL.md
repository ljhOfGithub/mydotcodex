---
name: survey-research-lineage
description: Use when the user provides a research keyword, field, or topic and wants to organize the research lineage of that direction from one or more survey papers. Supports a single specified survey, multiple surveys, or finding suitable surveys first. Trigger for requests like "根据 survey 整理这个方向脉络", "用这几篇综述梳理研究发展", "给定关键词找 survey 后总结研究路线", or "整理某方向从早期到最新工作的演进".
---

# Survey Research Lineage

## Goal

Use survey papers as anchors to reconstruct a field's research lineage: key stages, representative methods, technical shifts, datasets/benchmarks, unresolved problems, and current frontier. The output should be evidence-grounded rather than a keyword summary.

## Inputs

Accept any of:

- Keyword/topic only: find 2-5 relevant surveys first.
- One survey: use it as the main spine, then verify important claims with primary papers or newer sources when needed.
- Multiple surveys: compare their coverage, merge overlapping taxonomies, and note disagreements or blind spots.
- Local PDF/path, arXiv/DOI/URL/title, or pasted bibliography.

If the user does not specify a time window, cover the field's historical development plus recent progress. If the topic is fast-moving, browse or search current scholarly sources.

## Workflow

1. Scope the field.
   - Restate the keyword/topic, adjacent terms, and inclusion/exclusion boundaries.
   - If only a broad keyword is given, narrow it into 2-4 subtopics before searching.
   - Do not use a survey blindly if it is off-topic, outdated, or only loosely related.

2. Gather survey anchors.
   - Prefer recent, highly relevant surveys from arXiv, ACM, IEEE, ACL Anthology, Springer, Elsevier, OpenReview, or journal/conference pages.
   - For multiple surveys, build a small table: title, year, venue/source, scope, taxonomy, and known gaps.
   - If only abstracts/metadata are accessible, mark that part as `metadata-only` or `abstract-only`.

3. Extract the lineage.
   - Identify the survey's taxonomy, chronological stages, representative papers, datasets, metrics, and claimed open problems.
   - Trace major transitions: problem formulation, model family, data source, optimization/training regime, system architecture, evaluation protocol, deployment setting, or theoretical assumption.
   - Follow primary papers for important milestones when possible; do not present a survey's citation list as verified evidence without checking.

4. Compare and synthesize.
   - Merge taxonomies across surveys into a coherent map.
   - Mark areas where surveys disagree, omit recent work, or use different terminology for the same idea.
   - Separate established consensus from inference.

5. Update the frontier.
   - Check for newer papers, benchmarks, datasets, repos, or standards published after the survey cutoff.
   - Explain whether frontier work extends, contradicts, or bypasses the survey taxonomy.
   - Use primary sources for current claims whenever possible.

6. Produce the research map.
   - Prioritize structure over exhaustiveness.
   - Give representative papers with year and short role in the lineage.
   - End with actionable reading order and research opportunities.

## Output Format

Use concise Chinese by default unless the user asks otherwise.

```markdown
## 范围界定
- 关键词/方向:
- 纳入范围:
- 排除范围:
- 证据等级:

## Survey 锚点
| Survey | 年份 | 覆盖范围 | 分类框架 | 主要缺口 |
|---|---:|---|---|---|

## 研究脉络
### 阶段 1: ...
- 时间:
- 核心问题:
- 代表工作:
- 技术特征:
- 评价方式:
- 为什么进入下一阶段:

### 阶段 2: ...

## 方法谱系图
| 分支 | 代表工作 | 解决的问题 | 关键假设 | 局限 |
|---|---|---|---|---|

## 数据集与评测演进
| 数据/Benchmark | 用途 | 影响 | 局限 |
|---|---|---|---|

## 最新前沿
- Survey 截止后新增趋势:
- 与原 taxonomy 的关系:
- 仍未解决的问题:

## 推荐阅读路径
1. ...

## 可做研究点
| 方向 | 来自哪条脉络 | 最小验证方式 | 风险 |
|---|---|---|---|
```

## Guardrails

- Do not fabricate survey coverage, citation relationships, paper years, datasets, or benchmark results.
- Do not treat old survey conclusions as current if the field has moved on.
- If search or PDF access fails, report the exact limitation and distinguish verified evidence from partial inference.
- Prefer primary papers for milestone claims; use surveys for structure, terminology, and coverage comparison.
- When evidence is weak, label it clearly as `inference`, `abstract-only`, or `metadata-only`.
