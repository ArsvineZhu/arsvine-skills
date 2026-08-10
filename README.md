# Arsvine Skills

一个用于保存和分发 Arsvine 编写的 Codex skills 与可复用提示词包的公开仓库。

An evolving public collection of Codex skills and reusable prompt packages authored by Arsvine.

## Repository layout

```text
skills/
└── governing-repository-documentation/

prompts/
└── (future prompt packages)
```

每个 skill 都应当是一个自包含目录，并至少包含 `SKILL.md`；可按需附带
`agents/openai.yaml`、`references/`、`scripts/` 和 `assets/`。提示词包放在
`prompts/` 下，并应包含足够的说明，使其可以独立复用。

Each skill should be self-contained and include a valid `SKILL.md`. Optional
resources may live in `agents/`, `references/`, `scripts/`, and `assets/`.
Reusable prompt packages belong under `prompts/`.

## Available packages

### `governing-repository-documentation`

用于审查、创建、重构、修复和维护仓库文档，重点覆盖文档架构、重要作用域、
规范与实现之间的漂移、AI-facing instructions、操作知识和验证闭环。

Use this skill when repository documentation needs evidence-based governance,
navigation repair, canonical ownership, drift correction, or operational-knowledge
management.

## Install a skill

将目标 skill 目录复制到当前用户的 Codex skill 根目录：

```powershell
$skillsRepositoryRoot = 'C:\path\to\Arsvine Skills'
$userSkillsRoot = Join-Path $env:USERPROFILE '.codex\skills'
$skillName = 'governing-repository-documentation'

Copy-Item -LiteralPath (Join-Path $skillsRepositoryRoot "skills\$skillName") `
  -Destination (Join-Path $userSkillsRoot $skillName) -Recurse
```

After installation, restart or refresh the Codex session if the skill list does
not update immediately.

## Validate locally

From the repository root:

```powershell
python skills/governing-repository-documentation/tests/validate_skill.py
python skills/governing-repository-documentation/scripts/check_internal_links.py `
  skills/governing-repository-documentation
```

The checks are intentionally scoped to the package being changed. Run any
additional project-specific checks before publishing a new package.

## Contributing packages

- Use lowercase hyphen-case names for skill directories.
- Keep `SKILL.md` concise and put detailed material in directly linked references.
- Keep UI metadata in `agents/openai.yaml` aligned with `SKILL.md`.
- Include executable validation for scripts and report any unverified behavior.

## 中文说明

本仓库的目标是集中管理个人编写的 agent skills 和提示词包。新增内容时，优先
保持包的独立性、触发描述的准确性、引用路径的可验证性，以及面向公开使用者的
最小必要说明。
