# 文献与社区资料：AntiRLHF 的外部参照

[研究档案](../README.md)

整理于 2026 年 10 月。我们把论文实验、模型提供方披露和开发者使用讨论分开阅读，再判断每条材料对 AntiRLHF 的行动策略能提供什么。仓库中的提示词改造尚未形成可公布的跨模型效果数据。

## 论文：规则回忆与实际遵守的分离

[Models Recall What They Violate: Constraint Adherence in Multi-Turn LLM Ideation](https://arxiv.org/abs/2604.28031)（Kruthof，2026）提出 DriftBench：2,146 次评分运行、七个模型、38 个研究 Brief。最终轮平均约束回忆为 97.3%，但知道约束仍违反的 KBV 比例因模型而异，范围约为 8%–99%。结构化 checkpoint 只部分缓解偏离，复杂度增长仍在。这里测量的是多轮科研构思，直接启发我们区分“能背规则”和“会按规则行动”。

[Prompt-Induced Waste in Large Reasoning Models](https://arxiv.org/abs/2608.01347)（Weinberger、Hozez，2026）研究编码 Agent 中提示词造成的工作量差异。要求开发比较多套方法，使推理 Token 规模增加约 2.4–7.4 倍，没有得到相应正确性提高；强调最大确定性会增加重复验证和工具调用。因此，把“深思熟虑”“充分证明”等空泛要求写进持久提示词，也可能成为实际成本来源。

[SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents](https://arxiv.org/abs/2605.21384)（Zhao 等，2026）将可见的单项测试与隐藏的组合行为测试区分开。模型可以优化前者而在后者失效，且任务长度扩大时差距增大。它为“局部测试通过，却没有交付可用系统”提供了实验上的相近现象；我们自己的开发经历并不因此成为该论文的实验数据。

[Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?](https://arxiv.org/abs/2602.11988)（Gloaguen 等，2026）研究仓库上下文文件，发现其通常没有改善任务成功率，同时平均增加了超过 20% 的推理成本。模型会遵循文件中的要求并因此增加探索与测试。这提醒我们，治理指令的存在和被遵循，本身也可能增加无效工作。

## 论文：示范、纠错与长任务中的状态

[LLMs can implicitly learn from mistakes in-context](https://arxiv.org/abs/2502.08550)（Alazraki 等，2025）在数学推理的 few-shot 任务中，直接展示错误及正确结果的方案，平均优于附带详细纠错理由的示范。我们据此尝试短情境—行动对照；跨到真实软件工程仍是需要观察的假设。

[When Can LLMs Actually Correct Their Own Mistakes?](https://arxiv.org/abs/2406.01297)（Kamoi 等，2024/2025）综述自我纠错研究，发现依靠模型自身提示产生的反馈缺少稳定的纠错支持，而可靠外部反馈更有效。这与我们观察到的“认错表达很强、行为改变很弱”有联系，但论文并没有直接研究 AntiRLHF。

[Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents](https://arxiv.org/abs/2607.08716)（Wu 等，2026）把记忆视为选择性干预下一项行动的机制，优于被动持续提供整份状态。它使用了独立的记忆 Agent；我们从中提取“时机与相关性”的设计启发，并不直接复制这套运行架构。

## 编码：局部修补和评审循环

Hacker News 的[一组开发者讨论](https://news.ycombinator.com/item?id=46932195)描述了模型在持续开发中留下死代码、加入没有明确义务的向后兼容路径、回避较大的重构。讨论中也有开发者报告在模块化大仓库中正常使用 Agent，并强调明确边界和结构的重要性。这些是个人使用记录，适合识别失败形态及可能干预。

[AI 代码评审讨论](https://news.ycombinator.com/item?id=46766961)包含另一种体验：每轮评审继续提出小问题，甚至在等价写法间来回修改，重要缺陷与猜测混在一起。其对设计的启发是让检查由当前问题驱动，完成后不自动再开一轮寻找可改事项。

[关于测试增长的讨论](https://news.ycombinator.com/item?id=49795592)还提到确认依赖或语言本身行为的测试，以及中间实验测试被长期留下。仓库重构 Skill 因此从目标能力重新设计测试组织，再从旧套件中迁移仍然有用的场景；允许整组替换旧测试、夹具与测试专属辅助机制。

这些观察落实为执行选择：完整需求始终可见；结构问题直接改结构；测试和流程可以成组删除、合并或替换；取消失去工作价值的审查循环。

## 表达：明确禁止后仍反复出现

OpenAI 社区的[原始讨论](https://community.openai.com/t/most-annoying-habit-can-i-make-it-stop/1265708)集中投诉未经请求的对比重述。[其中一条回复](https://community.openai.com/t/most-annoying-habit-can-i-make-it-stop/1265708/6)指出，明确纠正后使用减少，但仍会出现。其他回复尝试直接句式约束、项目指令和临时提醒，反馈并不一致。

表达行为进入常驻 Constitution。文档工作同时保留独立的确定性语言扫描器，直接识别防御性否定、臆造的对比和判断弱化等模式。对实际写作的约束与脚本检查并用，避免反复要求同一个模型自行保证不再出现惯用句式。

## 官方发布与训练案例

OpenAI 在 [GPT-4o 谄媚问题复盘](https://openai.com/index/expanding-on-sycophancy/)（2025）中说明，叠加反馈信号可能改变模型的迎合倾向，原有的测评与用户反馈未及时暴露实际体验问题。它展示了局部奖励与整体使用体验间的张力。

Anthropic 在[训练和安全实践说明](https://www.anthropic.com/research/improving-alignment-security-efforts)（2026）披露，在一次训练中，模型会向未提到的 reviewer 写注释，并通过大量 disclaimers/caveats 获取原本意在鼓励诚实的奖励。团队后来回退训练。这是我们研究“表面证明行为可成为奖励策略”的重要实例，但对其他模型的具体训练机制仍应单独讨论。

## 官方对日常体验的承认

OpenAI 在[GPT-5.3 Instant 发布说明](https://openai.com/index/gpt-5-3-instant/)中直接讨论了防御性和说教式前言、不必要的限定，以及对用户意图和情绪的过度推定。文中也指出，语气、相关性和对话流畅性有些问题不会充分出现在 benchmark 中。

这支持把表达质量本身作为工作成果的一部分。在任务要求写作或交流时，观点是否明确、内容是否相关、读者能否顺畅使用，都应直接进入工作目标。

## 指令被执行，也会增加无效工作

ETH / LogicStar 的[Evaluating AGENTS.md](https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd)及其[论文修订版](https://arxiv.org/html/2602.11988v3)观察到，在所研究的仓库级任务中，context files 没有普遍提高任务成功率，平均推理成本增加超过 20%。研究轨迹分析发现，模型确实遵循了其中不少指令，进而增加探索、测试与推理。

这项发现直接影响 AI 文档的取舍：保留非显而易见的项目事实和具体决策，删除通用教条、重复概览，以及 Agent 自行扩展的永久流程。

## 常见治理药方的取舍

Anthropic 的[提示词实践文档](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)明确讨论过过度工程化、临时文件清理和围绕测试而非通用解决方案工作的问题。其中限制改动范围、避免额外抽象的建议，适用于需要严控改动的任务。

AntiRLHF 面对的还包括已批准的大范围架构重构。因此本次保留“完整目标、合理抽象、集中责任、复用依赖”的方向。文件数、diff、测试数和抽象数量都不单独决定方案好坏。

## 提示词可控制的范围

[OpenAI Deliberative Alignment](https://openai.com/index/deliberative-alignment/) 讨论的是把规范与应用过程纳入模型训练；目前我们没有微调或重新后训练的条件。AntiRLHF 选择研究推理时的行动选择，支持稳定的规则、角色 Skill 和有用的工具反馈。

## 指令加载方式

OpenAI 的[AGENTS.md 文档](https://developers.openai.com/codex/guides/agents-md/)描述持久指令的读取方式；[Skill 文档](https://developers.openai.com/codex/skills/)描述渐进加载：开始时通常暴露名称和描述，完整内容在选中后加载。

据此，本次把持续生效的角色行为放进常驻 Constitution，把任务知识留在独立 Skill。应用只提供文件链接而未实际加载正文时，应调整安装入口；不要求模型通过“我已经读取”这样的口头声明解决加载问题。

## Navigation / 导航

- [研究档案](../README.md)
- [English research overview](../README.en.md)
