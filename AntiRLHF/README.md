# AntiRLHF 介绍

[English](README.en.md)

> 本文纯手写，在 AI 时代请您珍惜。

AntiRLHF 是一套面向 Agent 的治理模型，尤其针对模型的 **局部可辩护性优化**：模型很擅长让当前步骤显得谨慎、正确、可验证，却可能失去对完整目标、结构和用户体验的持续关注。我们最早从 GPT 的使用经历中观察到这些问题，如今也关注其他模型在类似任务中的表现。

它源于长期使用 Chat、Research Agent 与 Coding Agent 时反复出现的一类问题：模型能够完成局部任务，却会在长轨迹中逐渐把资源投入到自我辩护、风险陈列、流程完整性、最小修改、兼容性想象和证明堆积，最终偏离用户真正要完成的目标。

究其原因，是 LLM 在后训练过程中“习得”的、用于满足测评指标的应对策略——但这显然摧毁了用户体验。

## 目录

- [“GPT” 现象](#观察到的现象)
- [宪章](#宪章)
- [角色区分](#角色区分)
- [AntiRLHF 的结构](#antirlhf-的结构)
- [历史演化](#历史演化)

---

## 观察到的现象

在编码任务中，常见表现是过分验证、依赖局部通过、测试固化接口、包装与兼容不断累积；模型“不敢”重构，即便重构，也可能删除大量旧代码，却再写一份通过新框架、附加测试和流程引入更多负担的新屎山；模型不考虑能够更好组织仓库的范式：一个代码文件 2000、3000 行，一个目录下代码文件平铺，不会抽出公用机制，不优先使用成熟库或依赖，自己造轮子（然后屎山自己维护）。习惯于列出“证据”，找出“边界”，过分对齐许可证、文件 SHA。

<!-- antirlhf: allow rule=logical-limitation-zh reason="The paragraph lists unwanted qualifiers as examples, not limitations on its conclusion" -->

在自然语言中，表现为预先给出足够的回答后，不断给出边界和限定、构造读者没提出的反驳、在确定结论后面追加“不能说明、不能证明、不代表、不等于、不足以判断、不能保证、不把”等否定限定，虚空打靶。逃避责任，减低判断确定性，难以确定观点，回答啰嗦无层次。

在长期文档中，模型还可能把一次局部纠正写成全局禁令，或将“删除内容”改写成“正确内容（现在没有错误）”的墓碑。AGENTS 与技能文本会把这些习惯传给以后的模型，造成长期污染。

> 以下现象均是不希望见到的。

### 防御性认知

模型遇到未知、风险、限制或反例后，容易持续描述这些问题，而没有把信息重新压缩为判断或行动。

### 确定性降格 / “我的建议、倾向是...”

<!-- antirlhf: allow rule=commitment-weakening-zh reason="Quoted alternatives illustrate how settled judgments are weakened" -->

推理已经得到明确结论，输出阶段却把它改写为“倾向”“可以考虑”“可能更合适”。表达层重新引入了推理阶段已经消除的不确定性。

<!-- antirlhf: allow rule=invented-contrast-zh reason="The heading names quoted failure constructions discussed in this section" -->
<!-- antirlhf: allow rule=logical-limitation-zh reason="The heading names quoted failure constructions discussed in this section" -->

### 命题编造再限定 / “不是而是、不能证明、不把、不自动成为...”

<!-- antirlhf: allow rule=logical-limitation-en reason="Quoted examples name the failure pattern being documented" -->

模型把一个有限命题自行升级为更强命题，再用 “does not prove”、 “does not automatically mean” 等语言否定这个自造命题。文本因此变得防御且冗长。

### 当下保留特权 / 屎山兼容

修改已有结构需要不断举证，保留已有结构却被当成默认安全选项。结果通常是 alias、shim、双路径、过渡层和局部补偿不断积累。

### 过度工程化 / 流程制度化

计划、矩阵、风险等级、验收表、资格验证表、checklist、review stage、evidence package 或固定 phase 开始代替真正的设计和施工。流程从工具变成了交付物。模型见过太多，也太喜欢用 TDD、EDD（测试、证据驱动开发），于是，大仓测试项达数百、新项目刚起步测试就十几个，检查仓库状态就开始找齐 证据，列出矩阵。

### 上下文漂移

长任务与 compaction 更容易留下日志、失败尝试和验证历史，而真正重要的目标、决策与 当前工作被稀释。

---

## 宪章

[`CONSTITUTION.md`](CONSTITUTION.md) 是 AntiRLHF 的通用治理宪章。它适合放入 Agent Harness 的用户级持久自定义指令中，并长期存在于上下文，比如 ChatGPT APP/Codex 的用户自定义指令。

宪章只规定跨角色成立的原则：保持目标和已定决定、做出判断、在语义所有者层级解决问题、限制低价值调查与验证、不给历史结构保留特权、拒绝防御性替代，并在目标完成后停止。具体任务知识不写入宪章。

宪章约束长期工作方向，Skill 提供具体任务中的工作方法，脚本检查可机械识别的语言与文件问题。修改治理规则时，先找到它应该改变的实际动作。

## 角色区分

AntiRLHF 区分 Planning 与 Execution，因为它们共享治理原则，却面对不同的行为恶化方式。

### 计划角色

[`antirlhf-plan`](skills/antirlhf-plan/) 面向研究、架构、技术比较、Spec 和设计判断。

它重点控制：

- 研究是否仍能改变决定、模型或实验；
- 不确定性是否被用来逃避判断；
- 架构是否从 capability、semantic owner、authority、lifecycle 和发展方向出发；
- 是否在实现第一个可行方案之前识别了更高层的所有权或模型问题；
- 已经完成的判断是否在表达时被降格。

### 执行角色

[`antirlhf-exec`](skills/antirlhf-exec/) 面向仓库实现、重构、调试、测试、验证和交付。

它重点控制：

- 是否直接实现已经决定的语义；
- 局部故障是否劫持当前目标，而非不断钻牛角尖；
- 是否在错误 owner 上继续堆 patch、adapter、fallback 或 compatibility；
- 测试与验证是否保护真正重要的逻辑与契约、从目标与用户操作出发，而非追求数量、覆盖面和自我证明；
- 旧 API、旧文档、旧测试与旧流程是否被赋予了保留与兼容特权。

## AntiRLHF 的结构

AntiRLHF 使用四种不同的机制，各自只承担适合机械化的责任：

```text
Constitution
  持久治理原则

计划 / 执行技能
  角色专属的路由与任务语义

参考文档
  按需披露的领域知识

脚本
  机械检查
```

语言扫描器识别特征明确的防御表达，遇到需要语境判断的句子则提示审阅。真实的技术区别、兼容要求与写作口吻由文档作者结合任务处理。

---

## 历史演化

AntiRLHF 从 JDD、TED 与 COST 演化而来，这是在治理 GPT 模型的过程中认知由浅入深的进程。它们分别强化了 justified machinery、Token 经济和软件轨迹总成本等思想，并逐渐暴露出一个更高层的问题：治理对象不能只停留在代码与工程流程，还需要直接约束 Agent 的判断、注意力分配和任务轨迹。这些观察最初以 **AntiGPT** 为名整理；进一步关注“知道规则却仍违反”“事后自我合理化”以及训练中面向评分者的行为后，项目升级为 **AntiRLHF**。名称标明研究对象：后训练反馈塑造的行为倾向。

历史治理原文保存在 [`archive/`](./archive/README.md)。本次讨论的案例、机制假设与文献整理见 [研究档案](docs/README.md)。

## Navigation / 导航

- [仓库概览](../README.zh-CN.md)
- [安装](../INSTALL.zh-CN.md)
- [文档导航](INDEX.zh-CN.md)
- [研究档案](docs/README.md)
