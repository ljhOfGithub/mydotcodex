# Report Framework

Use this framework after candidate retrieval and PDF/metadata reading. Answer in Chinese unless the user asks otherwise.

## 1. Introduction

- What is the problem? 具体科学问题是什么？
- Why does it matter? 现实世界或学术领域中为什么重要？
- What is the current status? 该领域大致现状是什么？
- What is the core contribution? 作者做了什么，解决了什么？
- Boundary conditions: 场景、数据分布、硬件、网络、实时性、隐私或成本约束是否明确？
- Root difficulty: 长期未解决的根本难点是什么？
- Timing: 为什么现在值得关注？是否有新技术、产业需求或政策驱动？
- Difference from SOTA: 与最先进方法最大不同是什么？
- Contribution type: 是修复已有缺陷，还是开辟新方向？

## 2. Background, Motivation, Related Work

- What knowledge is needed? 听众需要哪些背景？
- What are the limitations of existing works? 现有方案瓶颈是什么？
- Why a new approach? 现有方法为何不能直接解决问题？
- Confusing concepts: 哪些术语需要区分？
- Consensus or new critique: 局限性是共识还是作者首次指出？
- Key observation: 能否用小例子或预实验解释？
- Boundary of comparison: 哪些工作看似相关但不直接可比？
- Prior failed attempts: 前人类似思路失败在哪里？本文如何绕开？

## 3. System Overview

- Inputs and outputs: 输入、输出、整体流向是什么？
- Main modules: 核心模块有哪些？
- Interaction: 模块如何协作？
- Offline/online split: 是否有离线预处理和在线推理？
- Interfaces: 数据结构、调用频率、同步/异步接口是什么？
- Failure handling: 模块失败时是否降级或容错？
- Diagrams: 是否区分数据流和控制流？
- 30-second recap: 是否能在 30 秒内复述流程？

## 4. System Design

- How solved? 算法流程、公式或系统架构改进是什么？
- Design principles: 为什么这样设计？
- Technical innovation: 哪一部分原创？
- Assumptions: 是否依赖 IID、无限带宽、可信设备等假设？
- Symbols: 公式符号是否清楚，对应哪个模块？
- Key parameters: 参数直觉是什么？
- Edge cases: 异常输入或边界情况如何处理？
- Reproducibility: 随机种子、初始化、实现细节、代码和配置是否足够？

## 5. Experiment Setup

- Environment: 硬件、软件框架、网络环境是什么？
- Datasets and benchmarks: 数据集或基准是什么？
- Baselines: 与哪些经典或 SOTA 方法对比？
- Metrics: 评价指标是什么？
- Dataset traits: 大小、标注质量、类别分布、时间跨度有什么特点？
- Baseline fairness: 是否按原论文最佳配置运行？不能复现时如何处理？
- Randomness: 是否使用多随机种子、交叉验证、均值和标准差？
- Bias risks: 是否有偏向本文方法的实验设置？是否公正说明？

## 6. Evaluation

- Does it work? 是否优于对比方法？
- Ablation: 改进来自哪些模块？
- Sensitivity: 参数变化时是否稳定？
- Trade-offs: 是否用一类性能换另一类性能？
- Weak subsets: 哪些子任务或数据子集不占优？原因是什么？
- Counterintuitive ablations: 是否有去掉模块反而更好的现象？
- Parameter cliffs: 性能从什么范围开始明显下降？
- Significance: 是否做统计显著性检验？
- Deployment cost: 时间、内存、能耗或经济成本是否可接受？

## 7. Discussion

- Key takeaways: 最应该记住的结论是什么？
- Limitations: 方法在哪些场景可能失效？
- Broader implications: 对相关领域有什么启发？
- Future work: 下一步是什么？
- Condition dependence: 结论是否依赖特定实验条件？
- Negative results: 是否有意外负面结果？
- Ethics and misuse: 是否可能被滥用或有伦理风险？
- Near vs long term: 未来工作能否分成近期小改进和长期突破？
- Best follow-up reads: 最值得继续读的一两篇参考文献是什么？

## Fixed Answer Template

Fill this template when evidence supports it. Keep blanks only when the paper does not provide enough information.

```text
现有方法（如 ______）假设 ______，但实际中 ______ 导致 ______。
______ 发现根本原因不是 ______，而是 ______。
因此它没有继续 ______，而是做了一个非常规的设计：______。
代价是 ______，但换来了 ______。
```

## Before Next Discussion

Write a 2-minute elevator pitch:

```text
问题：______
洞察：______
设计选择：______
代价：______
```
