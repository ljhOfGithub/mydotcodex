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
