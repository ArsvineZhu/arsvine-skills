# Arsvine Skills

**AI governance and focused Agent Skills for real development work.**

Arsvine Skills 是一个公开的 AI 治理与 Agent Skills 仓库，保存 Arsvine 在实际研究、架构设计和 Coding Agent 工作中持续演化的治理方法与可复用任务能力。

仓库当前以 **AntiGPT** 为核心。AntiGPT 关注 Agent 在长任务中常见的目标漂移、判断降级、防御性推理、局部补丁累积、验证膨胀和历史结构保留偏置，并分别为 Planning 与 Execution 提供角色化 Skill。

## What's inside

| Package | Purpose |
| --- | --- |
| [`AntiGPT`](AntiGPT/README.md) | Governance model, Constitution, observations, rationale, and implementation model. |
| [`antigpt-plan`](skills/antigpt-plan/) | Research, architecture, technical comparison, specification, and design judgment. |
| [`antigpt-exec`](skills/antigpt-exec/) | Repository implementation, refactoring, debugging, testing, verification, and delivery. |
| [`session-handoff`](skills/session-handoff/) | Produce a high-fidelity conversation-state handoff and stop substantive work. |
| [`archive/governance`](archive/governance/) | Historical JDD, TED, and COST documents that led to AntiGPT. |

## Quick install

AntiGPT uses the Harness's persistent user instructions for its Constitution and native Skill discovery for task-specific guidance. It does not require a session-start hook.

For Codex, from the repository root:

```bash
python scripts/install.py --profile codex
```

The installer updates only its managed AntiGPT block in `~/.codex/AGENTS.md` and installs the repository Skills into `~/.codex/skills/`. Existing user instructions outside that block are preserved.

Other Harnesses can use the same installer with explicit paths, or follow [`INSTALL.md`](INSTALL.md).

## Repository layout

```text
AntiGPT/
  CONSTITUTION.md          # persistent governance core
  README.md                # formation, observations, model, rationale

skills/
  antigpt-plan/            # planning/research role skill
  antigpt-exec/            # execution role skill and mechanical checks
  session-handoff/         # independent task skill

archive/governance/        # superseded governance documents
scripts/                   # repository installation and validation
```

A Skill owns a distinct task contract. General engineering knowledge that only specializes Planning or Execution lives in AntiGPT role references instead of becoming another workflow Skill.

## Validate

```bash
python scripts/validate_repository.py
```

This runs structural Skill validation, script tests, documentation-graph checks, and active governance-prose checks.

## Status

This repository is research-driven and intentionally evolves through direct structural replacement. Current files describe current policy; historical governance is kept only where it remains useful for understanding the lineage.

## Navigation

- [Install Arsvine Skills](INSTALL.md)
- [AntiGPT](AntiGPT/README.md)
