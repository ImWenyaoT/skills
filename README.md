# Agent Skills

[简体中文](README.md) | [English](README.en.md)

[![validate-skills](https://github.com/ImWenyaoT/skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/ImWenyaoT/skills/actions/workflows/validate-skills.yml)

由 Tian Wenyao 维护的一组可组合 Agent Skills，适用于 Codex、Claude Code 及其他兼容
[Agent Skills](https://agentskills.io) 的工具。

这些 skills 来自真实工作流，强调可预测的过程、明确的完成标准和渐进披露。仓库采用两层设计：

- **编排 skills** 由用户显式调用，负责选择和组合下层能力。
- **能力 skills** 由模型按任务触发，提供可复用的执行纪律。

## 安装

使用官方 [`skills`](https://skills.sh) CLI 浏览并安装：

```bash
# 查看仓库中的所有 skills
npx skills add ImWenyaoT/skills --list

# 交互式选择并安装
npx skills add ImWenyaoT/skills

# 全局安装指定 skill 到 Codex
npx skills add ImWenyaoT/skills --skill writing-papers -g -a codex -y

# 安装全部 skills
npx skills add ImWenyaoT/skills --all
```

也可以从本地 checkout 验证或安装：

```bash
npx skills add . --list
npx skills add . --skill paper-workflow
```

## Skills

### Agent 工程

| Skill | 用途 |
|---|---|
| [`agent-loops`](skills/agent-loops) | 构建有界 agent loop、terminality、handoff 和 provider seam。 |
| [`agent-evals`](skills/agent-evals) | 异步评分、failure-case 生命周期和 golden regression。 |
| [`tool-policies`](skills/tool-policies) | 设计统一工具接口、风险分级和 approval gate。 |
| [`persisting-traces`](skills/persisting-traces) | 持久化 session、memory 和 trace。 |
| [`bridging-legacy`](skills/bridging-legacy) | 用兼容 adapter 包住迁移期遗留服务。 |
| [`spec-first`](skills/spec-first) | 在 docs-backed codebase 中先更新规范再修改行为。 |
| [`adversarial-review`](skills/adversarial-review) | 派独立只读 sub-agent 做对抗式终审。 |

### 学术论文

| Skill | 用途 |
|---|---|
| [`paper-workflow`](skills/paper-workflow) | 用户调用的论文流程编排入口。 |
| [`writing-papers`](skills/writing-papers) | 起草、审阅和润色技术论文。 |
| [`drawing-figures`](skills/drawing-figures) | 规划并制作出版级论文图表。 |
| [`elsevier-articles`](skills/elsevier-articles) | 维护可复现编译的 `elsarticle` 手稿。 |
| [`elsevier-submissions`](skills/elsevier-submissions) | 构建并检查 Editorial Manager 投稿包。 |

### 机器学习与写作

| Skill | 用途 |
|---|---|
| [`training-models`](skills/training-models) | 搭建、审查和诊断神经网络训练流程。 |
| [`writing-resumes`](skills/writing-resumes) | 编写成果导向的技术或产品简历。 |
| [`markdown-pdf`](skills/markdown-pdf) | 将 Markdown 转为适合打印的 PDF。 |
| [`apple-hig`](skills/apple-hig) | 审查并实现符合 Apple HIG 的交互。 |

### Skill 维护

| Skill | 用途 |
|---|---|
| [`mining-sessions`](skills/mining-sessions) | 从历史会话中发现反复出现的 skill 摩擦。 |
| [`importing-skills`](skills/importing-skills) | 审核外部 skill 的来源、许可和引入方式。 |

## 设计原则

- 一个含 `SKILL.md` 的目录就是一个可安装 skill；scripts、references 和 assets 与其共置。
- 编排 skill 设置 `disable-model-invocation: true`，只组织能力，不复制下层规则。
- 能力 skill 保留精确的 `description`、自己的完成标准和单一事实来源。
- 只有具备独立触发或跨流程复用价值的纪律才拆成 skill；局部分支放进 `references/`。

## 仓库结构

```text
skills/<name>/SKILL.md     # 可安装 skills
evals/trigger_cases.json   # 触发边界 golden cases
scripts/                   # 仓库级校验与同步工具
docs/research/             # 设计审计与研究记录
```

`skills/` 是 [`npx skills`](https://github.com/vercel-labs/skills) 官方支持的集合目录。CLI 会
发现其中每个包含 `SKILL.md` 的一级子目录。

## 维护

```bash
# 与 CI 相同的完整检查（需要 matplotlib 和 Pillow）
./scripts/ci.sh

# 核心仓库脚本 branch coverage，最低 70%
./scripts/coverage.sh

# 官方安装器 discovery
npx skills@latest add . --list
```

GitHub Actions 会在 Python 3.11 与 3.13 上运行仓库测试和每个 skill 的内置测试，在 3.13
上强制 branch coverage 门槛，并单独验证官方 `skills` CLI 能发现全部 18 个 skills。

如需继续维护本地镜像，可运行 `./scripts/sync-to-local.sh`。仓库仍是唯一源，本地安装目录只是镜像。

## License

[MIT](LICENSE)
