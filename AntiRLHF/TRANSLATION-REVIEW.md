# AntiRLHF 指令中文审阅入口

英文 `CONSTITUTION.md`、各 Skill 的 `SKILL.md` 与 `references/*.md` 是 Agent 的执行文本。对应的 `*.zh-CN.md` 和 `openai.zh-CN.yaml` 用于中文审阅，安装器仍读取英文原文。修改指令时同步修改相关译本。

## 共同宪章与四个 Skill

| 英文执行文本 | 中文审阅文本 | 主要职责 |
| --- | --- | --- |
| [Constitution](CONSTITUTION.md) | [宪章译本](CONSTITUTION.zh-CN.md) | 所有角色通用的行动原则 |
| [Plan](skills/antirlhf-plan/SKILL.md) | [Plan 译本](skills/antirlhf-plan/SKILL.zh-CN.md) | 研究与设计中的判断、交付和参考资料路由 |
| [Exec](skills/antirlhf-exec/SKILL.md) | [Exec 译本](skills/antirlhf-exec/SKILL.zh-CN.md) | 实现任务与验证中的下一步行动、专项 Skill 路由 |
| [Refactoring](skills/refactoring/SKILL.md) | [重构译本](skills/refactoring/SKILL.zh-CN.md) | 重构方法与整体测试体系重建 |
| [Documentation](skills/documentation/SKILL.md) | [文档译本](skills/documentation/SKILL.zh-CN.md) | 文档信息架构、受众和语言检查 |

## 角色参考资料

四个 Skill 都有按任务使用的参考资料：[`Plan`](skills/antirlhf-plan/references/)、[`Exec`](skills/antirlhf-exec/references/)、[`Refactoring`](skills/refactoring/references/) 和 [`Documentation`](skills/documentation/references/)。每个英文 `.md` 都有同目录下的 `.zh-CN.md` 审阅版本。Plan、Exec 的案例负责演示角色行为；重构、写作的完整操作方法由对应专项 Skill 维护。

专项方法由 `refactoring`、`documentation` 维护，角色 Skill 使用 `../refactoring/SKILL.md`、`../documentation/SKILL.md` 定位相邻 Skill。在源码仓库和安装目录中这两个相对路径具有相同结构。

语言扫描器位于 [`documentation/scripts/check/governance_prose.py`](skills/documentation/scripts/check/governance_prose.py)；规则配置保存在使用仓库的 `.config/arsvine-skills/scanner.toml`。扫描器负责可识别句式，写作视角和文档职责由编辑者根据实际内容判断。

## 导航

- [AntiRLHF 中文索引](INDEX.zh-CN.md)
