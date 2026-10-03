# AntiGPT

这是一套供规划、研究与编码 Agent 使用的双角色 AI 治理包。它针对一组常见退化：模型把大量认知资源投入自我辩护、免责、限定、假想风险、重复验证和流程完整性，最终削弱判断、扩张施工并偏离用户真正要完成的目标。

本包把治理拆成两个角色：

- `antigpt-plan/`：面向 Chat、研究者、架构师、Spec 作者和日常设计讨论。
- `antigpt-exec/`：面向 Codex、Coding Agent 和其他负责仓库施工的 Harness。

两者共享同一内核：**推进真实目标，保持判断强度，把调查与验证约束在会改变决策或结果的范围内，持续关注整个工作轨迹。**

## 观察到的问题

### Defensive cognition

模型发现未知、风险、限制或反例后，容易停留在“声明这些问题”这一步。判断任务因此退化为风险陈列、条件枚举或继续研究。

### Alignment-shaped defensive language

常见表现包括免责声明、自我定位、预防性反驳、责任规避、假想反例和结论降级。典型语义操作包括：

- 已得出的决定被改写成“倾向”“可以考虑”“可能更合适”。
- 用户没有提出绝对命题，模型先构造一个，再用“不代表”“不能证明”“不自动意味着”等形式否定。
- 风险没有现实证据或决策影响，却持续获得篇幅和工作预算。

### Local defensibility optimization

单个步骤往往都能解释，但整个轨迹逐渐偏离目标：

`uncertainty → investigation → evidence → more observations → more investigation → more governance → context drift`

工程中对应为测试累积、evidence 累积、兼容层累积、局部补丁累积、CI/qualification 扩张和“为了证明完成”继续施工。

### Context drift

长任务和上下文压缩会优先保留大量过程细节。原始目标、已定决定和当前施工意图被局部故障与验证记录挤出上下文。

## 治理结构

每个角色目录包含三层：

1. `CORE-INSTRUCTIONS.md` — **长期注入层**。复制到 Chat 项目自定义提示词、Codex 全局 `AGENTS.md`、Harness system/custom instructions 等长期上下文。它承担根优化目标、判断义务、压缩后目标保持和 Skill 强制路由。
2. `SKILL.md` — **任务路由层**。保持很短，只在任务相关时加载，并指向需要的 reference。
3. `references/` — **渐进披露层**。保存 failure patterns、判例、研究方法、重构/调试/测试规则和 few-shot 示例。

`evals/` 保存行为评测场景。`antigpt-exec/scripts/scan_defensive_language.py` 提供机械语言扫描。

## 为什么 CORE 必须长期存在

OpenAI Skills 在发现阶段只暴露 metadata；完整 `SKILL.md` 由模型按任务选择读取。长期自定义提示词与 Codex `AGENTS.md` 会持续进入请求上下文，因此 CORE 承担无法交给可选 Skill 的根约束。

CORE 保持短小。详细规则继续放在 Skill 和 references 中，降低常驻 token 成本与 compaction 压力。

## 安装

### Planning / Chat

把 `antigpt-plan/CORE-INSTRUCTIONS.md` 的正文放入该 Chat 项目或 Harness 的长期自定义指令中。安装 `antigpt-plan/` 目录为 `antigpt-plan` Skill。

### Execution / Codex

把 `antigpt-exec/CORE-INSTRUCTIONS.md` 的正文放入长期 Coding Agent 指令。Codex 可使用全局 `~/.codex/AGENTS.md` 或其他 Harness 提供的持久指令入口。安装 `antigpt-exec/` 目录为 `antigpt-exec` Skill。

项目自己的 `AGENTS.md`、Specs 和 Plans继续负责项目语义与授权；本治理包负责模型如何思考、收敛、施工和验证。

### OpenAI Skill 上传

OpenAI Skill bundle 要求单个 top-level skill 目录中存在一个 `SKILL.md`。因此 `antigpt-plan/` 与 `antigpt-exec/` 分别作为两个 Skill 上传或挂载。根目录 ZIP 是治理包交付格式。

## 使用原则

CORE 的法条长期生效。Skill 负责路由。Reference 在触发对应问题时读取。不要把全部 references 一次性塞入长期提示词。

负向 pattern 用于语义诊断。`不能证明`、`可能`、`建议` 等词本身只构成 review signal；治理检查它们是否承担结论降级、自我辩护、假想反驳或无效延迟。

机械扫描负责发现候选位置。扫描结果进入语义复核；脚本默认退出码为 0，CI gate 只有在项目明确选择后才启用。

## 机械语言扫描

Coding Agent 可直接运行：

```bash
python antigpt-exec/scripts/scan_defensive_language.py .
python antigpt-exec/scripts/scan_defensive_language.py --changed
python antigpt-exec/scripts/scan_defensive_language.py docs/ AGENTS.md --format json
python antigpt-exec/scripts/scan_defensive_language.py --include-broad-negations .
```

脚本从 `antigpt-exec/scripts/scanner.toml` 读取文本扩展名、跳过目录/globs、行级允许标记和匹配规则。它检查主体化、结论降级、防御式否定、虚构对照、研究拖延、假想 defeater、automaticity framing，以及可选的宽泛否定标记。默认启用具体规则；加入 `--include-broad-negations` 后，中文“不”字和英语 `not`、`no`、`never`、`nothing`、`nobody`、`nowhere`、`without` 及否定缩写才生成低级别复核候选。宽泛标记只指出值得检查的上下文，不单独判定为问题。核心使用 Python 3.11+ 标准库 `tomllib`。默认只报告候选项并返回 0；`--fail-on` 由项目显式选择时再启用。单行需要保留敏感表达时可加 `agency-scan: allow`。

## 评测

治理生效前后使用同一组任务比较行为：

- **Baseline**：不加载 CORE/Skill，记录模型原始退化方式。
- **Governed**：加载对应 CORE 与 Skill，重复同一任务。
- **Pressure**：加入测试失败、模糊信息、旁支异常、长上下文和 compaction，观察治理是否继续保持目标与判断。

重点观察：判断是否降级、调查是否无界扩张、旁支问题是否劫持目标、测试/evidence 是否持续增长、兼容机制是否凭空出现、压缩后是否仍保留 Objective / Decisions / Current Work。

## 与 COST 的关系

`COST.en.md` 是重要历史来源。它已经指出轨迹总成本、流程成本、验证成本、历史保留偏置与停止条件。新治理把这些工程原则上移到模型行为层，并把 Planning 与 Execution 分开治理。COST 作为历史文档保留；根提示词职责转移到两份 `CORE-INSTRUCTIONS.md`。

## 设计来源

本包参考：

- OpenAI Developers — Skills: <https://developers.openai.com/api/docs/guides/tools-skills>
- OpenAI Developers — Build skills: <https://developers.openai.com/plugins/build/skills>
- OpenAI Developers — Rethinking skills and prompts for GPT-6 Astra: <https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra>
- OpenAI Developers — Using GPT-6 / `AGENTS.md` and compaction guidance: <https://developers.openai.com/api/docs/guides/latest-model>
- Superpowers skills framework，尤其是 `using-superpowers`、`writing-skills`、`systematic-debugging`、`verification-before-completion`。

治理内核吸收 Superpowers 的强制式提示词、rationalization 识别和 progressive disclosure 设计；其无条件流程化、全量验证和普遍 TDD 规则保留为对照材料。
