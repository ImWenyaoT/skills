# Agent Skills

[简体中文](README.md) | [English](README.en.md)

[![validate-skills](https://github.com/ImWenyaoT/skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/ImWenyaoT/skills/actions/workflows/validate-skills.yml)

由 Tian Wenyao 维护的一组可组合 Agent Skills，适用于 Codex、Claude Code 及其他兼容
[Agent Skills](https://agentskills.io) 的工具。

这些 skills 来自真实工作流，强调可预测的过程、明确的完成标准和渐进披露。每个 skill 都由模型按任务触发，
边界互不重叠，也可以单独安装、单独分享。

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
npx skills add . --skill answering-reviewers
```

## Skills

### 论文主线

从结果到投出去的一条路:写 → 画 → 排版 → 打包 → 修回。

### 学术论文

| Skill | 用途 |
|---|---|
| [`writing-papers`](skills/writing-papers) | 起草、审阅和润色技术论文。 |
| [`answering-reviewers`](skills/answering-reviewers) | 把审稿意见当 spec 逐条实现,并渲染修回看板。 |
| [`drawing-figures`](skills/drawing-figures) | 规划并制作出版级论文图表。 |
| [`journal-articles`](skills/journal-articles) | 维护可复现编译的 `elsarticle` / `IEEEtran` 手稿。 |
| [`journal-submissions`](skills/journal-submissions) | 构建并检查 Elsevier / IEEE 投稿包。 |

### 实验

| Skill | 用途 |
|---|---|
| [`training-models`](skills/training-models) | 搭建、审查和诊断神经网络训练流程——论文里的数字从这里来。 |

## 设计原则

- 一个含 `SKILL.md` 的目录就是一个可安装 skill；scripts、references 和 assets 与其共置。
- 每个 skill 自洽：不引用别的 skill，单独发给别人也能用。
- 每个 skill 保留精确的 `description`、自己的完成标准和单一事实来源。
- 只有具备独立触发或跨流程复用价值的纪律才拆成 skill；局部分支放进 `references/`。

## 仓库结构

```text
skills/<name>/SKILL.md     # 可安装 skills
evals/trigger_cases.json   # 触发边界 golden cases
scripts/                   # 仓库级校验工具
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
上强制 branch coverage 门槛，并单独验证官方 `skills` CLI 能发现全部 6 个 skills。

已安装的 skills 由 `npx skills` 管理。发布新提交后，运行 `npx skills@latest update -g` 更新全局安装。

## License

[MIT](LICENSE)
