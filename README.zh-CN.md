# Arsvine Skills

[English](README.md)

这个仓库存放我在研究、软件开发和日常使用 Agent 时整理的治理方法与通用技能。目前主要维护 AntiRLHF。

## AntiRLHF

AntiRLHF 是一套面向 Agent 的治理模型，源于我长期使用 Chat、Research Agent 与 Coding Agent 的经历。模型经常能够完成局部步骤，却在长任务中偏离目标，累积局部补丁、兼容层、验证流程和防御性解释。

我把这些问题整理为对判断、注意力分配和任务轨迹的约束，并用技能与检查脚本落实到研究、开发和写作中。目标是让 Agent 持续围绕实际需求工作，在正确的职责层级解决问题，减少后续理解和修改的负担。

持久 Constitution 确定方向，四个技能把原则落实到具体任务：

| 技能                                                   | 职责                                                   |
| ------------------------------------------------------ | ------------------------------------------------------ |
| [AntiRLHF Plan](AntiRLHF/skills/antirlhf-plan/SKILL.md)   | 做出判断，研究会影响决策的未知，在合适的层级设计。     |
| [AntiRLHF Exec](AntiRLHF/skills/antirlhf-exec/SKILL.md)   | 将决策落实为实现，打通完整使用链路。                   |
| [Refactoring](AntiRLHF/skills/refactoring/SKILL.md)     | 重划职责、统一数据流，消除反复产生的复杂度。           |
| [Documentation](AntiRLHF/skills/documentation/SKILL.md) | 面向读者写作，维护文档结构，检查反复出现的防御性表达。 |

AntiRLHF 作为一个整体安装。文档技能拥有语言与导航检查脚本，四个技能共同使用这项能力。

[治理思路与演变](AntiRLHF/README.md) · [研究档案](AntiRLHF/docs/README.md) · [文档导航](AntiRLHF/INDEX.zh-CN.md)

## 开始使用

使用 Python 3.11 或更新版本，无需克隆即可安装：

```bash
curl -fsSL https://raw.githubusercontent.com/ArsvineZhu/arsvine-skills/main/scripts/install-remote.py \
  | python3 - --profile codex --antirlhf
```

已有本地副本时，在仓库根目录执行：

```bash
python scripts/install.py --profile codex --antirlhf
```

两种方式都将四个技能安装到 `~/.codex/skills/`，Constitution 与简短的版本更新引用行组成管理区块，置于 `~/.codex/AGENTS.md` 最前方，原有指令保留在后面。

[安装与更新指南](INSTALL.zh-CN.md) 包含预览、独立技能、其他 Harness 与 `--ref` 指定版本的方法。

## 通用技能

`general/` 存放可独立安装的通用能力：

- [Session Handoff](general/session-handoff/SKILL.md)：把长对话中的决策、上下文和未完成状态带到下一次会话。
- [Repo Kit](general/repo-kit/SKILL.md)：仓库快捷工具箱，处理常见的仓库基线与卫生事务。

```bash
python scripts/install.py --profile codex --skill session-handoff
python scripts/install.py --profile codex --skill repo-kit
```

## 仓库结构

```text
.config/arsvine-skills/   本仓库正在生效的检查配置
AntiRLHF/
  .version                AntiRLHF 版本
  CONSTITUTION.md          持久治理原则
  README.md / README.en.md 治理思路与演变
  INDEX.md                文档导航
  skills/                 四个配套技能（默认配置在 scripts/.config/）
  docs/                   观察、机制与文献研究档案
  archive/                历史治理文本
general/                  独立技能，各自包含 .version
scripts/                  install.py、install-remote.py、validate.py
```

## 开发

```bash
python scripts/validate.py
```

格式化：

```bash
# Python — 首次：uv tool install ruff  （或：uv sync --group dev）
ruff format .
ruff check --fix .

# Markdown / YAML — 首次：npm install
npm run format
```

仓库验证涵盖技能结构、文档导航、全部维护中的文本（含本 README 与技能参考文档）、技能界面文案、检测器行为与 Python 编译。版本记录在 `AntiRLHF/.version` 和各通用技能的 `.version` 中；安装器将版本写入已安装技能，并将简短更新提示写入 AntiRLHF 指令区块或通用技能自己的 `SKILL.md`。

## Navigation / 导航

- [安装](INSTALL.zh-CN.md)
- [AntiRLHF 介绍](AntiRLHF/README.md)
- [AntiRLHF 导航](AntiRLHF/INDEX.zh-CN.md)
- [研究档案](AntiRLHF/docs/README.md)
