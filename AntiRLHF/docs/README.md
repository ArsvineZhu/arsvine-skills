# AntiRLHF 研究档案

[English overview](README.en.md)

这里保存 AntiRLHF 形成过程中的现象记录、机制假设、提示词实验思路和文献阅读。它们是持续修订的研究笔记，有论文式的问题意识，但不按论文发表或工程验收的格式组织。观点可以鲜明；资料、观察与推断需要各自有出处。

## 研究主线

从 AntiGPT 走向 AntiRLHF，核心问题逐渐清晰：模型会准确复述要求、解释自己违反了哪条原则，实际做事时却继续采用局部修补、自我证明、过度检查与防御性措辞。它甚至可能通过一篇精彩的认错文字完成眼前的对话，而未在下一次决策里作出不同选择。

我们将这一行为称作 **局部可辩护性优化（local defensibility optimization）**：把容易检查、容易解释、容易获得认可的局部代理信号当成目标。AntiRLHF 的研究重点是**原则能否改变下一项行动**，而不是模型能否在事后讲清原则。

## 阅读路径

| 研究笔记 | 主要问题 |
| --- | --- |
| [问题与现场观察](research/field-observations.md) | 编码、测试、文档、自然语言与认错中的共同失败形态 |
| [机制与可检验假设](research/behavioral-mechanisms.md) | 规则回忆、决策、事后解释为何可能脱节 |
| [推理时治理与提示词设计](research/prompt-strategy.md) | 无法微调时，怎样让规则参与真实的行动选择 |
| [文献与社区资料](research/literature-and-community.md) | 原始论文、官方复盘、工程经验，各能支持什么 |

## 材料性质

我们区分三类来源：**亲身使用观察**记录遭遇的具体情形；**公开研究**记录研究者在特定任务与实验条件下得到的结果；**机制假设**是用于指导提示词设计的解释，等待不同场景中的实际行为来检验。

目前的改进是 **inference-time governance**：使用持久指令、任务 Skill、少量行动示范与确定性语言扫描工具。我们暂不进行权重微调或重新后训练，也不通过新造的评价流程代替开发和使用。

实际使用的规则由 [Constitution](../CONSTITUTION.md) 和 [Skills](../INDEX.zh-CN.md) 定义；这里保存研究过程与解释，不向 Agent 自动添加新的项目义务。

## Navigation / 导航

- [仓库概览](../../README.zh-CN.md)
- [安装](../../INSTALL.zh-CN.md)
- [AntiRLHF 介绍](../README.md)
- [AntiRLHF 导航](../INDEX.zh-CN.md)
- [English overview](README.en.md)
- [问题与现场观察](research/field-observations.md)
- [机制与可检验假设](research/behavioral-mechanisms.md)
- [推理时治理与提示词设计](research/prompt-strategy.md)
- [文献与社区资料](research/literature-and-community.md)
