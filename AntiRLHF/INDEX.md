# AntiRLHF Index

[中文](INDEX.zh-CN.md)

AntiRLHF combines a persistent Constitution with four bundled Skills. Start with the [introduction](README.en.md), then [install the bundle](../INSTALL.md).

## Structure

| Entry                                          | Role                                                                                |
| ---------------------------------------------- | ----------------------------------------------------------------------------------- |
| [Constitution](CONSTITUTION.md)                | Shared principles, kept in persistent user instructions.                            |
| [Plan](skills/antirlhf-plan/SKILL.md)           | Research, judgment, architecture, and specifications.                               |
| [Exec](skills/antirlhf-exec/SKILL.md)           | Implementation, debugging, verification, and delivery.                              |
| [Refactoring](skills/refactoring/SKILL.md)     | Responsibility boundaries, data flow, structural simplification, and test redesign. |
| [Documentation](skills/documentation/SKILL.md) | Reader-facing writing, documentation structure, and language/navigation checks.     |
| [Bundle version](.version)                     | Version shared by all four bundled Skills.                                          |

Plan and Exec load their own `references/` by task. Refactoring and Documentation provide focused task methods. Documentation owns the reusable [prose scanner](skills/documentation/scripts/check/governance_prose.py), [navigation checker](skills/documentation/scripts/check/doc_graph.py), and [scanner configuration](skills/documentation/scripts/.config/scanner.toml).

## Background

- [Research archive](docs/README.en.md): field observations, behavioral hypotheses, prompt strategies, and source notes.
- [Archive](archive/README.en.md): historical JDD, TED, and COST documents.

The repository's [general Skills](../README.md#general-skills) are independently installable. Repository installation and validation are controlled by the root `scripts/` directory.

## Navigation

- [Repository overview](../README.md)
- [Installation](../INSTALL.md)
- [AntiRLHF introduction](README.en.md)
- [Research notes](docs/README.en.md)
