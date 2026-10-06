# AntiGPT

AntiGPT 是一套面向 Agent 的治理模型。它源于长期使用 Chat、Research Agent 与 Coding Agent 时反复出现的一类问题：模型能够完成局部任务，却会在长轨迹中逐渐把资源投入到自我辩护、风险陈列、流程完整性、最小修改、兼容性想象和证明堆积，最终偏离用户真正要完成的目标。

AntiGPT 将这一类退化统一视为 **local defensibility optimization**：每一步都容易解释、容易证明、容易回退，但整个轨迹开始服务于“让局部行为看起来足够稳妥”，而非服务于目标本身。

## Constitution

[`CONSTITUTION.md`](CONSTITUTION.md) 是 AntiGPT 唯一的通用治理核心。它适合放入 Agent Harness 的用户级持久自定义指令中，并长期存在于上下文。

Constitution 只规定跨角色成立的原则：保持目标和已定决定、做出判断、在语义所有者层级解决问题、限制低价值调查与验证、不给历史结构保留特权、拒绝防御性替代，并在目标完成后停止。

具体任务知识不写入 Constitution。

## 两个角色

AntiGPT 区分 Planning 与 Execution，因为它们共享治理原则，却面对不同的退化方式。

### Plan

[`antigpt-plan`](../skills/antigpt-plan/) 面向研究、架构、技术比较、Spec 和设计判断。

它重点控制：

- 研究是否仍能改变决定、模型或实验；
- 不确定性是否被用来逃避判断；
- 架构是否从 capability、semantic owner、authority、lifecycle 和发展方向出发；
- 是否在实现第一个可行方案之前识别了更高层的所有权或模型问题；
- 已经完成的判断是否在表达时被降格。

### Exec

[`antigpt-exec`](../skills/antigpt-exec/) 面向仓库实现、重构、调试、测试、验证和交付。

它重点控制：

- 是否直接实现已经决定的语义；
- 局部故障是否劫持当前目标；
- 是否在错误 owner 上继续堆 patch、adapter、fallback 或 compatibility；
- 测试与验证是否保护真实 contract，而非追求数量和证明感；
- 旧 API、旧文档、旧测试与旧流程是否被赋予了无依据的保留特权。

Refactoring、documentation work、debugging 和 verification 都是 Plan 或 Exec 中的任务知识，因此保留为按需 reference，而不各自形成一套工作流 Skill。

## 观察模型

### Defensive cognition

模型遇到未知、风险、限制或反例后，容易持续描述这些问题，而没有把信息重新压缩为判断或行动。

### Commitment erosion

推理已经得到明确结论，输出阶段却把它改写为“倾向”“可以考虑”“可能更合适”。表达层重新引入了推理阶段已经消除的不确定性。

### Stronger-claim fabrication

<!-- antigpt: allow rule=defensive-negation-en reason="Quoted examples name the failure pattern being documented" -->
模型把一个有限命题自行升级为更强命题，再用 “does not prove”、 “does not automatically mean” 等语言否定这个自造命题。文本因此变得防御且冗长。

### Status-quo privilege

修改已有结构需要不断举证，保留已有结构却被当成默认安全选项。结果通常是 alias、shim、双路径、过渡层和局部补偿不断积累。

### Process substitution

计划、矩阵、风险等级、checklist、review stage、evidence package 或固定 phase 开始代替真正的设计和施工。流程从工具变成了交付物。

### Context drift

长任务与 compaction 更容易留下日志、失败尝试和验证历史，而真正重要的 `Objective`、`Decisions` 与 `Current Work` 被稀释。

## 实现结构

AntiGPT 使用四种不同的机制，各自只承担适合机械化的责任：

```text
Constitution
  persistent governance principles

Plan / Exec Skills
  role-specific routing and task semantics

References
  progressively disclosed domain knowledge

Scripts and evals
  mechanical checks and behavioral evaluation
```

静态脚本只能判断可机械证明的事实。语言扫描可以阻止高置信度的防御性表达模式并要求显式 waiver，但无法决定一个 caveat、抽象或兼容义务在语义上是否合理。此类判断继续由行为 eval 与实际 Agent 表现验证。

## 为什么不为每类工程任务建立 Skill

一个独立 Skill 应拥有独立的任务运行契约：触发条件、任务目标、生命周期、输出形态或停止条件会发生实质变化。

重构代码、治理文档、调试和测试通常不会改变角色。设计这些工作属于 Plan，执行这些工作属于 Exec。因此 AntiGPT 把相关知识放在角色 reference 中，避免复制核心理念或再建立一套流程。

`session-handoff` 则属于真正独立的任务：触发后当前工作必须停止，任务目标切换为恢复状态的 checkpoint，输出后再次停止，因此保留为独立 Skill。

## 历史

AntiGPT 从 JDD、TED 与 COST 演化而来。它们分别强化了 justified machinery、Token 经济和软件轨迹总成本等思想，并逐渐暴露出一个更高层的问题：治理对象不能只停留在代码与工程流程，还需要直接约束 Agent 的判断、注意力分配和任务轨迹。

历史原文保存在 [`archive/governance`](../archive/governance/)；它们已被 AntiGPT supersede，不再定义当前行为。

## Navigation

- [Repository overview](../README.md)
- [Installation](../INSTALL.md)
