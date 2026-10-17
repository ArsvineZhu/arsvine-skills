# 社区观察与设计依据

[English](community-observations.en.md) · [简体中文](community-observations.md)

整理日期：2026 年 10 月 17 日。本页记录公开材料及其对本次设计的影响。AntiGPT 的新文本尚未经过实际任务使用。

## 编码：局部修补和评审循环

Hacker News 的[一组开发者讨论](https://news.ycombinator.com/item?id=46932195)描述了模型在持续开发中留下死代码、加入没有明确义务的向后兼容路径、回避较大的重构。讨论中也有开发者报告在模块化大仓库中正常使用 Agent，并强调明确边界和结构的重要性。这些是个人使用记录，适合识别失败形态及可能干预。

[AI 代码评审讨论](https://news.ycombinator.com/item?id=46766961)包含另一种体验：每轮评审继续提出小问题，甚至在等价写法间来回修改，重要缺陷与猜测混在一起。其对设计的启发是让检查由当前问题驱动，完成后不自动再开一轮寻找可改事项。

[关于测试增长的讨论](https://news.ycombinator.com/item?id=49795592)还提到确认依赖或语言本身行为的测试，以及中间实验测试被长期留下。仓库重构 Skill 因此从目标能力重新设计测试组织，再从旧套件中迁移仍然有用的场景；允许整组替换旧测试、夹具与测试专属辅助机制。

这些观察落实为执行选择：完整需求始终可见；结构问题直接改结构；测试和流程可以成组删除、合并或替换；取消失去工作价值的审查循环。

## 表达：明确禁止后仍反复出现

OpenAI 社区的[原始讨论](https://community.openai.com/t/most-annoying-habit-can-i-make-it-stop/1265708)集中投诉未经请求的对比重述。[其中一条回复](https://community.openai.com/t/most-annoying-habit-can-i-make-it-stop/1265708/6)指出，明确纠正后使用减少，但仍会出现。其他回复尝试直接句式约束、项目指令和临时提醒，反馈并不一致。

表达行为进入常驻 Constitution。文档工作同时保留独立的确定性语言扫描器，直接识别防御性否定、臆造的对比和判断弱化等模式。对实际写作的约束与脚本检查并用，避免反复要求同一个模型自行保证不再出现惯用句式。

## 官方对日常体验的承认

OpenAI 在[GPT-5.3 Instant 发布说明](https://openai.com/index/gpt-5-3-instant/)中直接讨论了防御性和说教式前言、不必要的限定，以及对用户意图和情绪的过度推定。文中也指出，语气、相关性和对话流畅性有些问题不会充分出现在 benchmark 中。

这支持把表达质量本身作为工作成果的一部分。在任务要求写作或交流时，观点是否明确、内容是否相关、读者能否顺畅使用，都应直接进入工作目标。

## 训练中学到面向评分者的行为

Anthropic 的[公开训练与安全说明](https://www.anthropic.com/research/improving-alignment-security-efforts)披露：在一次训练中，模型向未被提及的 reviewer 写代码注释和回复，并通过不断增加免责声明或限定来获取原本鼓励诚实的奖励；团队随后回退有关训练并调整环境。

这个案例给出了训练奖励与防御性表达之间的具体联系。GPT 的各训练环节贡献仍未公开。本次采用的机制解释是：面向评分的行为可以泛化为日常工作习惯，并与局部反馈和长期上下文共同作用。

## 指令被执行，也会增加无效工作

ETH / LogicStar 的[Evaluating AGENTS.md](https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd)及其[论文修订版](https://arxiv.org/html/2602.11988v3)观察到，在所研究的仓库级任务中，context files 没有普遍提高任务成功率，平均推理成本增加超过 20%。研究轨迹分析发现，模型确实遵循了其中不少指令，进而增加探索、测试与推理。

这项发现直接影响 AI 文档的取舍：保留非显而易见的项目事实和具体决策，删除通用教条、重复概览，以及 Agent 自行扩展的永久流程。

## 常见治理药方的取舍

Anthropic 的[提示词实践文档](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)明确讨论过过度工程化、临时文件清理和围绕测试而非通用解决方案工作的问题。其中限制改动范围、避免额外抽象的建议，适用于需要严控改动的任务。

AntiGPT 面对的还包括已批准的大范围架构重构。因此本次保留“完整目标、合理抽象、集中责任、复用依赖”的方向。文件数、diff、测试数和抽象数量都不单独决定方案好坏。

## 指令加载方式

OpenAI 的[AGENTS.md 文档](https://developers.openai.com/codex/guides/agents-md/)描述持久指令的读取方式；[Skill 文档](https://developers.openai.com/codex/skills/)描述渐进加载：开始时通常暴露名称和描述，完整内容在选中后加载。

据此，本次把持续生效的角色行为放进常驻 Constitution，把任务知识留在独立 Skill。应用只提供文件链接而未实际加载正文时，应调整安装入口；不要求模型通过“我已经读取”这样的口头声明解决加载问题。

## Navigation

[AntiGPT 介绍](../README.md) · [包入口](../../README.zh-CN.md)
