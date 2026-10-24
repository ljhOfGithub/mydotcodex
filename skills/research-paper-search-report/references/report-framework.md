# Research Paper Report Framework

Use this framework after candidate retrieval and PDF/metadata reading. Answer in Chinese unless the user asks otherwise. For every item that is not supported by the paper or metadata, write `未在论文或元数据中确认`. If only abstract or metadata is available, mark the whole paper section as `abstract-only`.

## 1. Introduction

- What is the problem? 具体科学问题是什么？
- Why does it matter? 现实世界或学术领域中为什么重要？
- What is the current status? 该领域目前大致现状是什么？
- What is the core contribution? 作者做了什么，解决了什么？
- Boundary conditions: 问题是否有明确边界条件，例如特定场景、数据分布、硬件约束、网络条件、实时性、隐私或成本？
- Root difficulty: 如果问题长期未解决，根本难点是什么，例如非凸性、缺乏标注数据、实时性要求、异构硬件或系统复杂性？
- Timing: 为什么现在值得关注？是否有最近技术突破、产业需求或政策驱动？
- Difference from SOTA: 与已有最先进方法相比，最大不同点是什么？用一句话概括。
- Contribution type: 贡献是解决原有方法的一类缺陷，还是开辟新的子方向？

## 2. Background, Motivation, Related Work

- What knowledge is needed? 听众理解这篇工作需要具备哪些基础背景？
- What are the limitations of existing works? 现有方案存在哪些瓶颈？
- Why a new approach? 为什么现有方法不能直接解决该问题？
- Confusing concepts: 听众可能混淆哪些关键概念？需要提前区分哪些术语？
- Consensus or new critique: 现有工作的局限性是同行广泛承认，还是作者首次指出？
- Key observation: 关键观察或洞察能否用小例子、预实验或反例直观展示？
- Boundary of comparison: 是否存在看似相关但实际上不可直接比较的工作？如何划清界限？
- Prior failed attempts: 前人是否尝试过类似思路但失败？失败原因是什么？本文如何绕开？

## 3. System Overview

- Inputs and outputs: 系统输入、输出和高层处理流向是什么？
- Main modules: 系统由哪些核心模块组成？
- Interaction: 模块之间如何协作？
- Offline/online split: 是否有离线预处理和在线推理划分？分别在什么阶段完成？
- Interfaces: 模块接口是什么，例如数据结构、调用频率、同步/异步关系？
- Failure handling: 如果某个模块失败，系统是否有降级或容错机制？如果没有，是否需要说明？
- Diagram clarity: 概览图是否清晰区分数据流和控制流？
- 30-second recap: 听众能否在 30 秒内复述系统流程？如果不能，概览应如何简化？

## 4. System Design

- How solved? 具体算法流程、数学公式或系统架构改进是什么？
- Design principles: 为什么这样设计？
- Technical innovation: 哪一部分是作者原创？
- Assumptions: 设计是否依赖某些假设，例如 IID 数据、无限带宽、可信设备、稳定负载或完美标注？这些假设现实中是否近似成立？
- Symbols: 如果使用数学公式，每个符号是否清楚定义，并且能对应到系统模块？
- Key parameters: 关键参数是否有直觉解释，例如正则项系数如何控制精度与鲁棒性平衡？
- Edge cases: 是否有边界情况或异常输入？作者如何处理？
- Reproducibility: 如果听众想复现方法，至少需要哪些实现细节，例如随机种子、初始化方式、训练轮数、硬件配置、代码和超参数？

## 5. Experiment Setup

- Environment: 硬件配置、软件框架、网络环境是什么？
- Datasets and benchmarks: 使用哪些标准数据集、自建数据集或 benchmark？
- Baselines: 与哪些经典或最前沿方法对比？
- Metrics: 评价指标是什么？
- Dataset traits: 每个数据集的大小、标注质量、类别分布、时间跨度等是否有显著特点？
- Baseline fairness: 基线方法是否按照原论文最佳配置运行？如果无法复现，作者如何处理？
- Randomness: 是否使用多随机种子或交叉验证来减少偶然性？
- Non-determinism: 对深度学习、随机采样等非确定性算法，是否报告均值和标准差？
- Bias risks: 实验设置是否可能偏向作者方法，例如超参数专门为本文方法调优？是否公正说明？

## 6. Evaluation

- Does it work? 方法是否优于对比方法？
- Ablation: 改进来自哪些模块？每个模块贡献多少？
- Sensitivity: 参数变化时表现是否稳定？
- Trade-offs: 是否牺牲某方面性能来换取另一方面提升？
- Weak subsets: 主要结果中，作者方法在哪些子任务或数据子集上不占优势？原因是什么？
- Counterintuitive ablations: 消融实验是否出现去掉某模块反而性能提升的反常现象？如何解释？
- Parameter cliffs: 敏感性分析中，参数在什么范围开始剧烈下降？实际应用中是否容易碰到？
- Significance: 是否做统计显著性检验，例如 t-test 或 ANOVA，证明差异不是噪声？
- Deployment cost: 运行时间、内存占用、能耗或经济成本是否在实际部署中可接受？

## 7. Discussion

- Key takeaways: 听众最应该记住的结论是什么？
- Limitations: 方法在哪些场景可能失效？
- Broader implications: 对相关领域有什么启发？
- Future work: 下一步打算怎么做？
- Condition dependence: 主要结论是否依赖特定实验条件？更宽松或更严格条件下是否仍成立？
- Negative results: 是否有意外负面结果值得分享？它们如何修正作者初始直觉？
- Ethics and misuse: 方法是否可能被滥用或产生伦理风险？是否需要提出使用建议？
- Near vs long term: 未来工作能否分为近期可做的小改进和需要突破的长期方向？
- Best follow-up reads: 如果听众对该方向感兴趣，最值得深入阅读的参考文献是哪一两篇？

## Fixed Answer Template

Fill this template when evidence supports it. Keep blanks only when the paper does not provide enough information.

```text
现有方法（如 ______）假设 ______，但实际中 ______ 导致 ______。
______ 发现根本原因不是 ______，而是 ______。
因此它没有继续 ______，而是做了一个非常规的设计：______。
代价是 ______，但换来了 ______。
```

## Before Next Discussion

Apply `$paper-communication-layers`. For every selected paper, prepare:

- one sentence: `任务 + 核心机制 + 最强且有边界的结论`
- a 2-minute elevator pitch: `问题 -> 旧方法缺口 -> 洞察 -> 设计选择 -> 关键证据 -> 代价`

Do not turn either version into a metric list. Keep the longer 3-minute and 10-minute layers optional in batch reports.

```text
问题：______
旧方法缺口：______
洞察：______
设计选择：______
关键证据：______
代价：______
```
