# 安装 Arsvine Skills

[English](INSTALL.md)

使用 Python 3.11 或更新版本，在本仓库的本地副本根目录执行以下命令。

## 选择安装内容

AntiGPT 将 Constitution 与四个技能一起安装：`antigpt-plan`、`antigpt-exec`、`refactoring`、`documentation`。

```bash
python scripts/install.py --profile codex --antigpt
```

单独安装通用技能：

```bash
python scripts/install.py --profile codex --skill session-handoff
```

组合安装：

```bash
python scripts/install.py --profile codex --antigpt --skill session-handoff
```

省略选择参数时，安装 AntiGPT 与全部通用技能。任意命令都可追加 `--dry-run` 预览。

## 安装位置

Codex 配置将技能写入 `~/.codex/skills/`，AntiGPT 管理区块置于 `~/.codex/AGENTS.md` 最前方，原有指令紧随其后。通用技能只安装到技能目录，版本与更新提示写在自己的 `SKILL.md` 中。

其他 Harness 可指定持久指令文件和技能目录：

```bash
python scripts/install.py --antigpt \
  --instructions-file /path/to/persistent/instructions.md \
  --skills-dir /path/to/skills
```

已安装的技能目录会被所选源文件替换。重新安装前，请把个人修改保存在源仓库中。

## 版本与更新

- `AntiGPT/.version` 记录整个 AntiGPT的版本。安装时，同一版本写入四个已安装技能目录的 `.version`。
- `general/` 下每个技能拥有独立的 `.version`，随技能一起复制。
- AntiGPT 在 Constitution 管理区块内附一条简短的 `>` 版本与更新提示，不单设小节、不写本地路径。通用技能把同样的提示写在自己的 `SKILL.md` 中。提示要求 Agent 每个会话访问可用时检查一次更新，发现新版本后提醒用户，同意后再更新。

更新时，先取得最新仓库内容，再执行原来的安装命令，刷新所选技能及其版本提示。安装 AntiGPT 时，同时更新置于用户指令文件最前方的管理区块。

## 交给 Agent 安装

> 从本仓库安装完整的 AntiGPT 四个配套技能。使用安装器，指定当前 Harness 的持久指令文件与技能目录，保留无关的已有指令。写入已安装版本与更新提醒指引，并向我说明安装结果。

## 验证仓库

```bash
python scripts/validate.py
```

仓库控制命令与配置归 `scripts/` 管理，可复用的语言和导航检查脚本由 documentation 技能拥有。验证同时扫描维护中的人类文档和 AI 文档。JDD、TED、COST 的历史原文不参与当前语言规则检查，维护中的档案介绍参与检查。

## Navigation / 导航

- [仓库概览](README.zh-CN.md)
- [AntiGPT 介绍](AntiGPT/README.md)
- [AntiGPT 导航](AntiGPT/INDEX.zh-CN.md)
