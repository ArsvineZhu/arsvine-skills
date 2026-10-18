# 文档导航与已有检查工具

移动文档、调整导航、将 Documentation Skill 装进其他仓库，或调查扫描器、链接检查的实际问题时使用本文。

## 在权威位置维护文档

当前有效的文档放在对应主题目录；历史评论根据内容放在档案或研究目录。接口或工作流程被替换后，更新当前使用章节和链接，删除失效的操作指导。

移动文件后修正指向它的本地 Markdown 链接，按读者的入口实际跟随重要链接。项目确实维护多语言导航时，更新对应语言。使用语义名称，而不是匿名文档编号。

有些仓库用互相链接的 Navigation 区块维护明确的导航图。新增双向导航之前先看项目是否真的采用该约定。普通引用和出处可以保持单向链接。

## 使用现有语言扫描器

在 AntiRLHF 仓库根目录运行：

```bash
python AntiRLHF/skills/documentation/scripts/check/governance_prose.py --changed
```

审核特定文章时，可指定文件：

```bash
python AntiRLHF/skills/documentation/scripts/check/governance_prose.py path/to/file.md
```

装入 Codex 后，脚本位于 `~/.codex/skills/documentation/scripts/check/governance_prose.py`。项目配置为 `.config/arsvine-skills/scanner.toml`；没有该文件时会查用户级安装配置，再查 Skill 内置配置。需要特定规则集时使用 `--config`。

`block` 为高置信度问题，`review` 需要结合语境阅读，`signal` 是较弱提示。扫描器能定位防御式表达的某些形式，但不能决定作者真正的意思。应连同段落、读者和实际命题一起审阅。

故意引用的反面例子，可在对应段落前写明具体豁免：

```html
<!-- antirlhf: allow rule=defensive-negation-en reason="Quoted wording shown as an anti-example" -->
```

豁免用于教学例子和确实必要的表达，不应用于掩盖本该改写的防御句。脚本也会报告未使用或格式不正确的豁免。

## 有配置的仓库才运行导航检查

仓库存在 `.config/arsvine-skills/docgraph.toml` 时：

```bash
python AntiRLHF/skills/documentation/scripts/check/doc_graph.py
```

检查器读取当前维护文档范围，检查 Navigation 链接、项目要求的双向链接，以及从入口文档是否可到达。链接失效时修改对应文档，或在导航责任真实改变时更新项目配置。

在其他仓库中，可从已安装的 `documentation/SKILL.md` 定位同一个脚本。使用该约定的仓库应提供自己的 docgraph 配置。

## 从读者入口检查最终结果

打开改动影响的入口，跟随新链接，按目标读者身份读最终段落。让当前文档保留现行信息；历史与编辑说明只留在它们本来就属于交付内容的位置。
