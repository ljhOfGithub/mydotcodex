---
name: paper-insight-feasibility
description: Use when analyzing one specific research paper to propose non-obvious insights, research extensions, or product/system ideas, then investigate whether each insight is feasible with evidence from the paper, related literature, datasets, code, benchmarks, engineering constraints, and experiment design. Trigger for requests like "针对这篇论文提出 insight", "调研这个 insight 是否可行", "从论文里找可做的研究点", or "评估这个论文想法能不能落地".
---

# Paper Insight Feasibility

## Goal

Turn one paper into evidence-grounded insights and feasibility judgments. Do not stop at brainstorming: every promising insight must be traced back to paper evidence, checked against outside evidence when needed, and converted into a concrete validation plan.

## Workflow

1. Identify the target paper.
   - Accept a local PDF/path, arXiv/DOI/URL, title, or paper text.
   - If only a title is given, find the paper from scholarly or official sources before analyzing it.
   - Prefer the PDF/full text over abstracts, blogs, or secondary summaries.

2. Build a paper-grounded baseline.
   - Extract the problem, method, assumptions, datasets, metrics, main results, ablations, and limitations.
   - Mark which claims are directly supported by the paper and which are inference.
   - Capture useful quotes only sparingly; mostly paraphrase with page/section anchors when possible.

3. Generate candidate insights.
   - Propose 3-7 insights unless the user requests a different count.
   - Favor insights that are actionable, testable, and not just a restatement of the paper.
   - Useful categories: hidden assumption, reusable method component, missing ablation, new application domain, systems bottleneck, evaluation flaw, dataset opportunity, theory-to-practice gap, productization path.

4. Feasibility investigation.
   - For each serious insight, check at least these dimensions:
     - Novelty: what adjacent papers, baselines, or existing products already do.
     - Technical viability: required model, data, compute, infrastructure, and expected failure modes.
     - Evidence fit: why the source paper supports or weakens the insight.
     - Validation path: minimal experiment, metric, dataset, comparison baseline, and success threshold.
     - Risk: blocker, confounder, reproducibility issue, cost, ethics, or deployment constraint.
   - Browse or search scholarly sources when the answer depends on current literature, code availability, benchmarks, product status, or datasets.
   - Use primary sources where possible: paper PDFs, official repos, benchmark pages, dataset docs, arXiv/OpenReview/ACL/ACM/IEEE pages, or vendor docs.

5. Rank and decide.
   - Score each insight on a 1-5 scale for novelty, feasibility, evidence strength, and expected payoff.
   - Recommend one of: pursue now, pursue after prerequisite, monitor, or drop.
   - Explain the ranking with concrete evidence rather than keyword matches.

## Output Format

Use concise Chinese by default unless the user asks otherwise.

```markdown
## 论文基线
- 论文:
- 核心问题:
- 方法链:
- 关键证据:
- 局限/假设:

## Insight 候选
| # | Insight | 来源证据 | 新颖性 | 可行性 | 回报 | 建议 |
|---|---|---|---:|---:|---:|---|

## 重点可行性调研
### Insight N: ...
- 直觉:
- 论文内证据:
- 外部证据:
- 最小验证实验:
- 风险与反证:
- 结论:

## 下一步
1. ...
```

## Guardrails

- Do not invent paper contents, code availability, benchmark results, or dataset access.
- Do not present an old local result as a fresh investigation.
- If source access fails, say exactly what failed and separate partial analysis from unverified claims.
- If the paper is outside the model's reliable memory or the topic is fast-moving, verify with current sources.
- Keep recommendations falsifiable: every "可行" judgment needs a concrete experiment or evidence path.
