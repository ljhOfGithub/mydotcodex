---
name: paper-insight-feasibility
description: Use when analyzing one paper or a small related paper set to derive evidence-grounded, non-obvious insights, distinguish them from gaps and research questions, and evaluate novelty, feasibility, and minimal validation plans. Trigger for requests like "针对这篇论文提出 insight", "调研这个 insight 是否可行", "从论文里找可做的研究点", or "评估这个论文想法能不能落地".
---

# Paper Insight Feasibility

## Goal

Turn one paper or a small related set into evidence-grounded insights and feasibility judgments. Complete the chain from paper evidence to mechanism, discriminating predictions, novelty, feasibility, and a concrete validation decision. Do not relabel a literature gap or an unanswered question as an insight.

Keep these objects distinct:

- **Observation:** what a paper or experiment reports, with source and uncertainty.
- **Gap:** what the inspected literature does not adequately cover.
- **Research question:** the answerable question that defines the proposed study.
- **Insight:** a non-obvious explanatory or organizing claim connecting conditions, mechanism, and outcome.
- **Hypothesis:** a candidate proposition derived from the insight and open to rejection.
- **Prediction:** an observable implication that distinguishes the hypothesis from at least one rival.
- **Evidence:** material that bears on a claim; it is not the claim itself.

## Workflow and Gates

### 1. Scope and source gate

Identify the target paper or small paper set and the decision requested: understand, generate insights, check novelty, assess feasibility, or design a pilot.

If the user already has a deep-reading note or cross-paper candidate card, continue in that existing artifact. Reuse its verified source anchors, correct weak transitions, and add the insight analysis after the paper's claim–method–experiment–boundary chain. Do not produce a parallel summary that repeats the same papers merely to show this skill was used.

   - Accept a local PDF/path, arXiv/DOI/URL, title, or paper text.
   - If only a title is given, find the paper from scholarly or official sources before analyzing it.
   - Prefer the PDF/full text over abstracts, blogs, or secondary summaries.
   - Record whether each source is full-text, abstract-only, metadata-only, or unavailable.
   - Do not make a deep-reading claim from abstract-only evidence. Stop expansion when new papers no longer change the interpretation or the user's scope is reached.

### 2. Layered paper reading and evidence baseline

Read in layers before proposing insights:

1. Title, abstract, introduction, conclusion.
2. Method, experiments, limitations, appendix, and key tables or figures.
3. Related work and citation chains when novelty or field position matters.

For every key paper, capture:

- full citation and stable identifier/link;
- research question, target problem, known conditions, and assumptions;
- core idea and method/training/inference chain;
- datasets, metrics, baselines, sample size or runs, ablations, and proofs where applicable;
- main findings and what they do not prove;
- limitations, failure modes, threats to validity, and missing experiments;
- relevance to the user's problem.

Then build the paper-grounded baseline:

   - Do not translate the paper's gap sentence and relabel it as the problem.
   - Extract a short core problem shared with adjacent work.
   - Separate:
     - known conditions and constraints;
     - the paper's concrete, testable research question;
     - why the problem matters and what type of value it has;
     - why it remains unsolved;
     - what prior work specifically does poorly;
     - the paper's method, assumptions, datasets, metrics, results, ablations, and limitations.
   - Treat `unresolved` and `valuable` as independent judgments. Drop or downgrade ideas whose expected payoff does not justify the difficulty.
   - Label each statement as `paper claim`, `evidence-supported conclusion`, or `analyst inference`.
   - Capture useful quotes only sparingly; mostly paraphrase with page/section anchors when possible.

Create a compact evidence ledger before synthesis:

| ID | Observation/claim | Source anchor | Evidence type | Strength/uncertainty | Supports or challenges |
|---|---|---|---|---|---|

Do not pass the evidence gate if the central observation has no inspectable source, or if a claimed mechanism is inferred only from final benchmark scores.

### 3. Innovation and literature relationship check

Classify the paper's contribution as problem, method, data, evaluation, theory, or engineering innovation. Identify the closest predecessor, competing method, extension, benchmark, survey, and critique or negative result when relevant.

Answer:

- What is genuinely new relative to the closest inspected work?
- Is it a new principle, combination, measurement, or implementation detail?
- Which experiment supports each contribution?
- Which novelty claim is partial or under-supported?
- What overlap would remove the proposed insight's residual difference?

Use backward, forward, lateral, benchmark, and negative/critique searches only as needed. A bounded search can establish what was inspected, not universal novelty.

### 4. Insight synthesis gate

Generate candidates only after the evidence baseline is stable. Use fewer strong candidates rather than filling a quota.

For each candidate:

1. **Freeze the observation:** state what was actually reported before interpreting it, including source, setting, uncertainty, and whether it was exploratory or expected.
2. **Name the anomaly or tension:** identify the pattern that a simple paper-by-paper summary does not explain. A single-paper hidden assumption can substitute for a cross-paper anomaly.
3. **Propose a mechanism:** explain how stated conditions could produce the outcome.
4. **Generate rivals:** include plausible measurement artifact, confounding/selection, reverse direction, task or model difference, stochastic variation, and competing mechanism when relevant.
5. **State the insight:** one explanatory or organizing claim; do not phrase it only as “nobody has done X” or “can we do X?”.
6. **Set boundaries:** specify tasks, systems, models, feedback, time horizon, and conditions where the insight may or may not apply.
7. **Operationalize constructs:** define how each important concept becomes an observable variable or intervention; do not substitute an easy proxy without justification.
8. **Derive discriminating predictions:** name the expected pattern, uncertainty, incompatible result, and how the result differs from at least one rival.
9. **Set status:** `candidate`, `supported`, `partially supported`, `contradicted`, or `unverified`. Literature synthesis alone usually produces `candidate` or `partially supported`, not a confirmed finding.

For a cross-paper card, make the transition explicit: which paper establishes the known phenomenon; which paper supplies a competing mechanism or a strong baseline; what observation remains unexplained after those are accounted for; why the proposed mechanism predicts something different. If the later claim does not follow from earlier evidence, state the missing premise and the smallest experiment needed to test it.

Useful candidate sources include hidden assumptions, reusable components, missing ablations, contradictory findings, systems bottlenecks, evaluation flaws, dataset opportunities, boundary failures, and theory-to-practice gaps.

Do not pass the insight gate unless a candidate has: source evidence, a mechanism or organizing principle, boundary conditions, at least one rival, a discriminating prediction, and an explicit falsifier or incompatible result.

### 5. Novelty and feasibility investigation

   - For each serious insight, check at least these dimensions:
     - Novelty: what adjacent papers, baselines, or existing products already do, and the exact residual difference after overlap is removed.
     - Technical viability: required model, data, compute, infrastructure, and expected failure modes.
     - Evidence fit: why the source paper supports or weakens the insight.
     - Measurement viability: whether the proposed constructs and outcomes can be measured validly and independently of the mechanism under test.
     - Validation path:
       - conclusion to validate;
       - improvement target and primary/secondary metrics;
       - dataset/task, experimental groups, strong baselines, controls, and ablations;
       - experimental flow and whether it isolates the proposed mechanism;
       - what is more complete than prior work and what remains incomplete;
       - rationale and reference basis;
       - explicit alignment with the core problem, concrete question, unsolved cause, and prior weakness.
     - Risk: blocker, confounder, reproducibility issue, cost, ethics, or deployment constraint.
   - Prefer the cheapest decisive falsifier before a broad implementation plan.
   - Do not invent a fixed success percentage before reproducing the baseline and running a pilot. Define the initial target relative to the strongest comparable baseline, then use pilot variance and effect size to set a meaningful threshold.
   - Browse or search scholarly sources when the answer depends on current literature, code availability, benchmarks, product status, or datasets.
   - Use primary sources where possible: paper PDFs, official repos, benchmark pages, dataset docs, arXiv/OpenReview/ACL/ACM/IEEE pages, or vendor docs.

### 6. Validation design

For each candidate that survives novelty and feasibility checks, specify:

- target conclusion and claim type: descriptive, associational, predictive, causal, or mechanistic;
- experimental unit, dataset/task, intervention, comparison, outcomes, and time horizon;
- strongest comparable baselines, positive/negative controls, and mechanism-specific ablations;
- primary and secondary metrics, uncertainty reporting, seeds or repetitions, and stopping/exclusion rules;
- exploration set for discovering conditions and an independent confirmation set for testing the frozen claim;
- what result supports the candidate, favors a rival, contradicts the candidate, or remains indeterminate;
- replication or transport test across a meaningful boundary when the claim is intended to generalize.

Never rewrite a result observed during exploration as an a priori prediction. Keep exploratory and confirmatory claims separate.

### 7. Rank, decide, and update

   - Score each insight on a 1-5 scale for novelty, feasibility, evidence strength, and expected payoff.
   - Recommend one of: pursue now, pursue after prerequisite, monitor, or drop.
   - Explain the ranking with concrete evidence rather than keyword matches.
   - Record decisive missing evidence and the smallest next action that would change the decision.
   - After new experiments or sources, update candidate status and evidence ledger; do not silently preserve an insight contradicted by stronger evidence.

## Output Format

默认在现有原卡内续写一条有前后因果关系的研究论证，而不是逐项填满上面所有检查字段。用简体中文，篇幅随证据复杂度调整：

1. **现象从何而来：**论文在哪个条件下观察到什么？原文位置和证据等级是什么？
2. **为什么现有解释不够：**最近论文已经解释哪部分？最强竞争机制还能解释哪部分？剩下的反常之处是什么？
3. **候选 insight：**用条件、机制、结果写一句解释性主张。说明它比“前人没做 X”多了哪条可检验预测。
4. **怎样区分：**设计最小实验，让候选机制与竞争机制给出不同结果；写清支持、反证和无法判定三种情形。
5. **值不值得做：**按已检索范围说明新颖性边界、数据/计算/实现条件、最大阻碍和下一步研究决定。

在每一段末尾指出下一段要解决的问题。若前一段不能推出后一段，明确缺少哪项证据并停留在候选状态。篇幅较长时可用一张证据台账或实验表，但表格须承担论证功能，不重复正文。对多篇论文，先解释每篇各自增加了哪条证据或竞争解释，再提出跨论文 insight；不按论文名称堆叠摘要。

## Guardrails

- Do not invent paper contents, code availability, benchmark results, or dataset access.
- Do not present an old local result as a fresh investigation.
- If source access fails, say exactly what failed and separate partial analysis from unverified claims.
- If the paper is outside the model's reliable memory or the topic is fast-moving, verify with current sources.
- Keep recommendations falsifiable: every "可行" judgment needs a concrete experiment or evidence path.
- Do not call a gap, question, method idea, or expected benefit an insight unless the explanatory/organizing claim is explicit.
- Do not treat a plausible mechanism as established without a design that distinguishes it from rivals.
- Do not claim novelty from a quick or undocumented search; state the search boundary and residual uncertainty.
- Do not select only confirming papers or experiments. Seek contradictory evidence and preserve negative or indeterminate results.
