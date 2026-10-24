---
name: field-progress-survey
description: Use when the user wants to investigate a research field, topic, method family, or application area by surveying its current latest progress and historical development with real paper citations from scholarly sources. This skill is for broad but evidence-grounded literature mapping, not deep reading every paper.
---

# Field Progress Survey


## Goal

Produce a concise, evidence-grounded survey of a field's historical trajectory and current frontier. Cite real papers and venues; do not claim to have read every paper deeply unless full-text reading was actually performed.

## Source Strategy

Search multiple scholarly sources when possible:

- arXiv, Semantic Scholar, OpenAlex, DBLP, Google Scholar snippets, publisher pages, conference proceedings, ACL Anthology, PubMed, IEEE, ACM, NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV, SIGGRAPH, CHI, KDD, WWW, SIGMOD, VLDB, or domain-specific venues.
- Prefer primary paper pages, proceedings pages, DOI records, arXiv pages, and author project pages over blogs or news.
- Use recent-year filters for the frontier, and broad historical searches for foundational work.
- If web access is unavailable or a site blocks access, say so and use available sources instead.

## Workflow

1. Clarify scope only when necessary:
   - Field/topic boundaries.
   - Time range, if the user cares.
   - Output language and depth, if not obvious.

2. Build search coverage:
   - Search the exact topic phrase.
   - Search common aliases, earlier names, and adjacent method terms.
   - Search "survey", "benchmark", "review", "tutorial", and top venue names for orientation.
   - Search recent years, including the current year, for latest work.

3. Select papers:
   - Include foundational papers, turning points, representative systems, influential benchmarks/datasets, and recent frontier papers.
   - Favor papers with clear metadata: title, authors, year, venue/source, URL/DOI/arXiv ID.
   - For broad fields, 10-20 papers is usually enough unless the user asks for more.
   - Avoid padding with weakly related papers just to reach a count.

4. Verify and deduplicate:
   - Merge arXiv and published versions when they are the same work.
   - Check author/year/title consistency before citing.
   - Separate papers, surveys, datasets, benchmarks, and blog/project pages.
   - Mark uncertain metadata as uncertain instead of inventing it.

5. Read lightly but usefully:
   - Read abstracts, introductions, figures/tables, contribution lists, and experiment summaries.
   - Deep-read only pivotal or ambiguous papers when needed to avoid a wrong claim.
   - Do not overstate results from title-only evidence.

6. Synthesize:
   - Organize history into phases with approximate dates and the problem each phase solved.
   - Explain why each phase mattered technically.
   - Identify current frontier themes, open problems, and likely next directions.
   - Distinguish mature consensus from active debate.

7. Decompose research problems when the user asks what papers are trying to solve, why the problem matters, or what can be improved.
   - Do not translate an Introduction gap sentence and relabel it as the research problem.
   - Identify a short **core problem** shared by related papers, such as `长期记忆可靠性`, `时间有效性检索`, or `多轮支持策略决策`.
   - For each paper, separate:
     1. **已知条件**: facts, setting, constraints, and observed deficiencies already assumed by the paper.
     2. **具体研究问题**: under those conditions, the precise question the paper tries to answer. Phrase it as a concrete, testable question.
     3. **为什么重要**: who benefits, what failure is prevented, or what scientific/measurement capability is enabled. Classify the value as direct application, reliability/safety, evaluation infrastructure, scientific explanation, population coverage, or long-term social value when useful.
     4. **为什么尚未解决**: data, method, measurement, cost, ethics, or deployment difficulty that blocks prior work.
     5. **现有工作哪里不好**: specific observed weakness, not vague language such as `能力不完整` or `效果有限`.
     6. **怎样可以做得更好**: an implementable improvement tied to the weakness.
   - Treat `unresolved` and `important` as separate judgments. A problem may be unsolved because it is difficult, underspecified, or low value.
   - Reuse the same core-problem label across papers that study the same underlying issue; let their known conditions and specific questions distinguish them.

8. Design experiments when requested.
   - For each selected paper or research problem, state:
     - the conclusion to validate;
     - the improvement target and primary/secondary metrics;
     - datasets/tasks, experimental groups, strong baselines, controls, and ablations;
     - the experimental flow and whether each step is necessary to answer the question;
     - what makes the design more complete than prior work and what remains incomplete;
     - why the design was constructed this way and which paper, benchmark, theory, or reporting standard supports it;
     - an explicit mapping from core problem, specific question, unsolved cause, and prior weakness to experiment components.
   - Do not invent a fixed percentage improvement before reproducing baselines and running a pilot. Define the target as improvement over the strongest comparable baseline, then use pilot variance and effect size to set a meaningful threshold.
   - Label experiment plans based only on abstracts or public metadata as `方案级/待全文核对`; do not present them as reproductions of the original protocol.
   - For broad surveys, keep experiment designs to the papers the user selects or the most promising papers unless the user explicitly requests every paper.

9. Hand off downloaded papers to Zotero when local paper management is requested.
   - Use `$zotero-paper-library` to build a manifest for downloaded PDFs, metadata files, and generated survey reports.
   - Preserve source URLs, DOI/arXiv/OpenReview identifiers, topic tags, and the survey date.
   - Mark papers cited in the final survey with `field-progress-survey` and `survey-cited` tags.

## Output Shape

Default to Chinese unless the user asks otherwise. Keep it concise and cite sources inline.

Recommended structure:

```markdown
## 一句话结论

## 发展脉络
- 阶段 1（年份范围）：核心变化。代表论文：...
- 阶段 2（年份范围）：核心变化。代表论文：...

## 当前最新进展
- 方向 A：说明。代表论文：...
- 方向 B：说明。代表论文：...

## 关键论文表
| 年份 | 论文 | 作者/机构 | 来源 | 为什么重要 |
|---|---|---|---|---|

## 仍未解决的问题

## 逐篇问题拆解（用户要求时）
- 核心问题：
- 已知条件：
- 具体研究问题：
- 为什么重要：
- 为什么尚未解决：
- 现有工作哪里不好：
- 怎样可以做得更好：

## 实验设计（用户要求时）
- 要验证的结论：
- 改善目标：
- 实验组/对照组/指标/消融：
- 流程是否达到目的：
- 完善在哪里、还缺什么：
- 构建依据：
- 与核心问题、具体问题和前人不足的呼应：

## 参考来源
```

Use links in paper titles when available. For each cited paper, include at least title, year, and source link. Include venue/source when verified.

## Quality Rules

- Never fabricate papers, venues, dates, citations, DOIs, or claims.
- If the user asks for "latest", browse or otherwise verify current sources; do not rely on memory.
- State the search date for latest-progress surveys.
- Report coverage limits, such as "主要覆盖 arXiv + 顶会论文，未系统检索专利/工业白皮书".
- Do not present citation counts, SOTA rankings, or acceptance status as current unless verified from reliable sources.
- When results conflict, name the conflict and prefer primary sources.
- Keep recommendations and trend claims tied to the papers actually found.
