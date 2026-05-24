# Deep Reading Template

Use this template when the user asks for a single-paper deep reading, beginner-friendly explanation, presentation draft, figure/table walkthrough, or "像讲课一样讲" report. Answer in Chinese unless the user asks otherwise.

## Asset Rules

- Create an asset directory beside the report: `<YYYY-MM-DD-short-title>_assets/`.
- Put only useful paper screenshots there: method architecture, system workflow, experimental setup, main result, ablation, failure cases, or limitation figures/tables.
- Prefer screenshots from the official PDF. Keep filenames stable and descriptive, for example `figure-method.png`, `table-main-result.png`.
- In the report, use relative Markdown image links: `![方法架构图](YYYY-MM-DD-short-title_assets/figure-method.png)`.
- If screenshot extraction is not possible, keep the screenshot index table and write `未提取截图`; do not invent image paths.

## Language and Terminology Rules

- Explain the paper as if teaching a smart beginner.
- Every retained English term in the main text must appear in the terminology table first.
- First use: `中文译名（English term）`. Later prefer Chinese.
- Do not use bare jargon as a shortcut.
- Do not use `instrument` as an untranslated Chinese verb.
- Prefer action-level explanations: `传统快照算法默认所有相关进程都能接入快照协议：它们可以在收发消息时携带快照标记，并在合适时刻记录本地状态`.
- For `instrument/instrumentation`, explain it as the concrete modification or observation hook used in the paper, not as an untranslated verb.
- For `baseline`, explain it as "用来比较的新方法之前的代表性方法或对照组".
- For `benchmark`, explain the task set, environment, and scoring protocol.
- For `marker`, explain what is attached to messages or state and why.
- For `piggyback`, explain what extra information is carried alongside an existing message.
- For `workload`, explain the concrete requests, tasks, traces, or jobs used in experiments.
- For `trace`, explain whether it is a request log, execution sequence, network packet record, or model action history.

## Report Skeleton

```markdown
# 《论文标题》精读讲解

> 报告日期：
> 论文来源：
> 阅读材料：
> 证据状态：
> 图片资产目录：

## 1. 一页纸结论

- 这篇论文解决什么问题：
- 核心想法：
- 最重要的实验结论：
- 对入门读者最该记住的一句话：

## 2. 读这篇论文前需要知道什么

| 前置概念 | 小白解释 | 为什么本文需要它 |
| --- | --- | --- |

## 3. 论文图表截图索引

| 图片 | 对应论文位置 | 这张图/表说明什么 | 报告中讲解位置 |
| --- | --- | --- | --- |
| ![图名](YYYY-MM-DD-short-title_assets/figure-name.png) | Figure/Table X, Page Y |  |  |

只放对理解论文真正有帮助的图/表。优先放方法架构图、实验设置图、主结果表、消融实验图和限制/失败案例图。

## 4. 专有名词精讲

| 术语 | 小白解释 | 在论文中的具体含义 | 容易误解的点 |
| --- | --- | --- | --- |

### 4.x 英文术语使用规范

- 本报告正文中保留的英文术语，都必须已经在上表解释。
- 首次出现写成：中文译名（English term）。后文优先使用中文译名。
- 不推荐把 `instrument` 当中文动词直接使用。
- 推荐改写：`传统算法默认进程都能接入协议，也就是能在收发消息时携带额外标记，并在合适时刻记录本地状态`。

## 5. 研究问题和动机

### 5.1 背景
### 5.2 旧方法的问题
### 5.3 作者要证明的主张

## 6. 方法像讲课一样拆开

### 6.1 总体流程

在这里嵌入并讲解最重要的方法/系统架构图：

![方法架构图](YYYY-MM-DD-short-title_assets/figure-method.png)

### 6.2 关键模块
### 6.3 与已有方法的差异
### 6.4 一个直观例子

## 7. 实验过程详细复盘

### 7.1 实验总览

| 实验 | 想回答的问题 | 数据/任务 | 对比对象 | 指标 | 结论 |
| --- | --- | --- | --- | --- | --- |

### 7.2 数据集和任务设置

在这里嵌入并讲解实验设置图/表，如果论文有：

![实验设置](YYYY-MM-DD-short-title_assets/figure-experiment-setup.png)

- 数据集：
- 划分方式：
- 输入输出：
- 评价协议：
- 论文中未明确说明的内容：

### 7.3 Baseline 和对照组

| Baseline | 代表什么方法 | 为什么要比它 | 公平性注意点 |
| --- | --- | --- | --- |

### 7.4 指标解释

| 指标 | 小白解释 | 越高/越低越好 | 它能说明什么 | 它不能说明什么 |
| --- | --- | --- | --- | --- |

### 7.5 主结果

在这里嵌入并逐图/逐表解释主结果：

![主结果表或图](YYYY-MM-DD-short-title_assets/table-main-result.png)

逐表/逐图解释主要结果：实验问题 -> 设置 -> 数字结果 -> 作者解释 -> 我的解读。

### 7.6 消融实验

在这里嵌入消融实验截图：

![消融实验](YYYY-MM-DD-short-title_assets/figure-ablation.png)

说明每个模块被移除或替换后发生了什么，以及这是否真正支持作者的设计选择。

### 7.7 鲁棒性、泛化或效率实验

如果论文包含这些实验，解释它们如何证明方法在不同场景下仍然有效。

### 7.8 失败案例和限制

列出论文承认的限制，以及阅读后发现但论文没有充分讨论的风险。

## 8. 结果到底说明了什么

- 被实验支持的结论：
- 证据还不够强的结论：
- 可能的混杂因素：

## 9. 像正式 presentation 一样讲

### 9.1 3 分钟版本

问题 -> 旧方法缺口 -> 核心方法 -> 实验设计 -> 关键结果 -> 局限。

### 9.2 10 分钟版本

按 slide 组织，每页写：标题、要讲的点、可以口播的话。

## 10. 复习清单

- 我已经理解：
- 还需要补：
- 推荐继续搜索的关键词/论文：
```
