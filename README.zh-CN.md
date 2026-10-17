# Arsvine Skills

[English](README.md)

这个仓库存放我在研究、软件开发和日常使用 Agent 时整理的治理方法与通用技能。目前主要维护 AntiGPT。

## AntiGPT

AntiGPT 是一套面向 Agent 的治理模型，源于我长期使用 Chat、Research Agent 与 Coding Agent 的经历。模型经常能够完成局部步骤，却在长任务中偏离目标，累积局部补丁、兼容层、验证流程和防御性解释。

我把这些问题整理为对判断、注意力分配和任务轨迹的约束，并用技能与检查脚本落实到研究、开发和写作中。目标是让 Agent 持续围绕实际需求工作，在正确的职责层级解决问题，减少后续理解和修改的负担。

持久 Constitution 确定方向，四个技能把原则落实到具体任务：

| 技能 | 职责 |
| --- | --- |
| [AntiGPT Plan](AntiGPT/skills/antigpt-plan/SKILL.md) | 做出判断，研究会影响决策的未知，在合适的层级设计。 |
| [AntiGPT Exec](AntiGPT/skills/antigpt-exec/SKILL.md) | 将决策落实为实现，打通完整使用链路。 |
| [Refactoring](AntiGPT/skills/refactoring/SKILL.md) | 重划职责、统一数据流，消除反复产生的复杂度。 |
| [Documentation](AntiGPT/skills/documentation/SKILL.md) | 面向读者写作，维护文档结构，检查反复出现的防御性表达。 |

AntiGPT 作为一个整体安装。文档技能拥有语言与导航检查脚本，四个技能共同使用这项能力。

[治理思路与演变](AntiGPT/README.md) · [文档导航](AntiGPT/INDEX.zh-CN.md)

## 开始使用

使用 Python 3.11 或更新版本，在仓库根目录执行：

```bash
python scripts/install.py --profile codex --antigpt
```

四个技能将安装到 `~/.codex/skills/`，Constitution 与简短的版本更新引用行组成管理区块，置于 `~/.codex/AGENTS.md` 最前方，原有指令保留在后面。

[安装与更新指南](INSTALL.zh-CN.md) 包含预览、独立技能与其他 Harness 的使用方法。

## 通用技能

`general/` 存放可独立安装的通用能力：

- [Session Handoff](general/session-handoff/SKILL.md)：把长对话中的决策、上下文和未完成状态带到下一次会话。

```bash
python scripts/install.py --profile codex --skill session-handoff
```

## 仓库结构

```text
AntiGPT/
  .version                AntiGPT 版本
  CONSTITUTION.md          持久治理原则
  README.md / README.en.md 治理思路与演变
  INDEX.md                文档导航
  skills/                 四个配套技能
  docs/                   观察与背景资料
  archive/                历史治理文本
general/                  独立技能，各自包含 .version
scripts/                  仓库安装与验证脚本
  config/                 仓库工具配置
```

## 开发

```bash
python scripts/validate.py
```

仓库验证涵盖技能结构、文档导航、全部维护中的文本（含本 README 与技能参考文档）、技能界面文案、检测器行为与 Python 编译。版本记录在 `AntiGPT/.version` 和各通用技能的 `.version` 中；安装器将版本写入已安装技能，并将简短更新提示写入 AntiGPT 指令区块或通用技能自己的 `SKILL.md`。

## Navigation / 导航

- [安装](INSTALL.zh-CN.md)
- [AntiGPT 介绍](AntiGPT/README.md)
- [AntiGPT 导航](AntiGPT/INDEX.zh-CN.md)
