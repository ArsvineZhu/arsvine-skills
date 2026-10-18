# 安装 Arsvine Skills

[English](INSTALL.md)

使用 Python 3.11 或更新版本。远程安装无需先克隆仓库。

## 远程安装（无需克隆）

一次拉取仓库归档并执行安装。`-` 之后的参数与 `scripts/install.py` 相同：

```bash
curl -fsSL https://raw.githubusercontent.com/ArsvineZhu/arsvine-skills/main/scripts/install-remote.py \
  | python3 - --profile codex --antirlhf
```

Windows 可用 `curl.exe` 与 `python` 按同样方式调用。用 `--ref` 指定分支、标签或提交（默认 `main`）：

```bash
curl -fsSL https://raw.githubusercontent.com/ArsvineZhu/arsvine-skills/main/scripts/install-remote.py \
  | python3 - --ref main --profile codex --antirlhf --dry-run
```

引导脚本将 GitHub zip 归档下载到临时目录，运行该树中的 `scripts/install.py`，安装结束后删除临时副本（传入 `--keep-fetch` 则保留）。用 `--from PATH` 可对已有本地副本安装，跳过下载。

## 从本地副本安装

在已克隆的仓库根目录执行：

```bash
python scripts/install.py --profile codex --antirlhf
```

## 选择安装内容

AntiRLHF 将 Constitution 与四个技能一起安装：`antirlhf-plan`、`antirlhf-exec`、`refactoring`、`documentation`。

```bash
python scripts/install.py --profile codex --antirlhf
```

单独安装通用技能：

```bash
python scripts/install.py --profile codex --skill session-handoff
python scripts/install.py --profile codex --skill repo-kit
```

组合安装：

```bash
python scripts/install.py --profile codex --antirlhf --skill session-handoff --skill repo-kit
```

省略选择参数时，安装 AntiRLHF 与全部通用技能。任意命令都可追加 `--dry-run` 预览。`install-remote.py` 使用相同的选择参数。

## 安装位置

Codex 配置将技能写入 `~/.codex/skills/`，AntiRLHF 管理区块置于 `~/.codex/AGENTS.md` 最前方，原有指令紧随其后。通用技能只安装到技能目录，版本与更新提示写在自己的 `SKILL.md` 中。

各技能 `scripts/.config/` 中的默认配置会复制到 Harness/项目的命名空间目录 `.config/arsvine-skills/`（有 `AGENTS.md` 时放在其同级；否则放在 `skills/` 同级）。文件名统一不加前导点（如 `scanner.toml`、`length.toml`、`docgraph.toml`）。该目录中已有文件不会被覆盖；若仓库已有别人的 `.config/`，只创建我们的子目录，不改动其中其它内容。

其他 Harness 可指定持久指令文件和技能目录：

```bash
python scripts/install.py --antirlhf \
  --instructions-file /path/to/persistent/instructions.md \
  --skills-dir /path/to/skills
```

已安装的技能目录会被所选源文件替换。重新安装前，请把个人修改保存在源仓库中。项目侧覆盖写在 `.config/arsvine-skills/`，不要改已安装技能目录。

## 版本与更新

- `AntiRLHF/.version` 记录整个 AntiRLHF的版本。安装时，同一版本写入四个已安装技能目录的 `.version`。
- `general/` 下每个技能拥有独立的 `.version`，随技能一起复制。
- AntiRLHF 在 Constitution 管理区块内附一条简短的 `>` 版本与更新提示，不单设小节、不写本地路径。通用技能把同样的提示写在自己的 `SKILL.md` 中。提示要求 Agent 每个会话访问可用时检查一次更新，发现新版本后提醒用户，同意后再更新。

从本地副本更新时，先拉取最新内容，再执行原来的 `scripts/install.py` 命令。无需克隆时，对目标 `--ref` 重新运行远程安装器。两种路径都会刷新所选技能及其版本提示。安装 AntiRLHF 时，同时更新置于用户指令文件最前方的管理区块。

## 交给 Agent 安装

> 用远程安装器（curl 调用 `scripts/install-remote.py`）或本仓库的 `scripts/install.py` 安装完整的 AntiRLHF 四个配套技能。指定当前 Harness 的持久指令文件与技能目录，保留无关的已有指令。写入已安装版本与更新提醒指引，并向我说明安装结果。

## 验证仓库

```bash
python scripts/validate.py
```

仓库控制命令归 `scripts/` 管理；本仓库正在生效的检查策略在 `.config/arsvine-skills/`。可复用的语言和导航检查脚本由 documentation 技能拥有。验证同时扫描维护中的人类文档和 AI 文档。`AntiRLHF/archive/` 不参与语言规则检查。

## Navigation / 导航

- [仓库概览](README.zh-CN.md)
- [AntiRLHF 介绍](AntiRLHF/README.md)
- [AntiRLHF 导航](AntiRLHF/INDEX.zh-CN.md)
- [研究档案](AntiRLHF/docs/README.md)
