# skills

> 田文耀的个人 Agent Skills 仓库 —— 用 GitHub 同步、跨 agent 复用的一组 [Agent Skills](https://agentskills.io)。

每个 skill 是一个自包含文件夹,含一份 `SKILL.md`(元数据 + 指令)和可选的 `scripts/`、`references/`、`assets/`。Agent 按**渐进披露**(progressive disclosure)加载:启动时只读 `name` + `description`,任务匹配时才把完整 `SKILL.md` 读进上下文,执行时再按需调用脚本/引用文件。兼容 Claude Code、Codex、Gemini CLI 等所有支持 Agent Skills 格式的客户端。

## 目录

### 🎓 学术论文 (Academic Paper)

| Skill | 用途 |
|-------|------|
| [`drawing-paper-figures`](drawing-paper-figures) | 为 Elsevier 风格期刊论文做图。两段式:先从参考论文语料推导字数/图数/配色**预算**,再用 figkit 画架构图、Ours-vs-baseline 散点、结果拼图与效率图(600 dpi)。 |
| [`packaging-elsevier-submissions`](packaging-elsevier-submissions) | 把成稿的 LaTeX 手稿打包成 Editorial Manager 投稿包。声明集及其顺序(CRediT / 利益声明 / 致谢 / 数据可用性)、摘要/highlights/图形摘要硬性规格、扁平 ASCII 源码 zip、cover letter 与防御性写作要点。 |

### 🧠 机器学习 (Machine Learning)

| Skill | 用途 |
|-------|------|
| [`debugging-nn-training`](debugging-nn-training) | 神经网络训练常见错误自检清单。14 条**静默失败**的坑(overfit 单 batch、train/eval、zero_grad、logits-vs-softmax、bias+BatchNorm、view-vs-permute,以及 shuffle、loss 平均、warmup、归一化泄漏、随机种子、显存泄漏等),每条按「症状 → 为什么 → 怎么查 → 怎么改」给出,附可运行的对照脚本。 |

### 🛠️ 元 / 工作流 (Meta)

| Skill | 用途 |
|-------|------|
| [`creating-skills-from-sessions`](creating-skills-from-sessions) | 从历史 agent 会话里挖掘反复出现的摩擦与卡点,把它们沉淀成新的或改进的 skill。讲清 transcript 与自定义 skill 的实际存放位置、如何过滤 guardian 子代理噪声、以及 skill-vs-memory 的取舍。 |

## 安装 / 同步

**整库同步**(把全部 skill 拉到本地 skills 目录):

```bash
git clone https://github.com/ImWenyaoT/skills.git /tmp/skills
# Claude Code:复制(或软链)需要的 skill 到 ~/.claude/skills/
cp -r /tmp/skills/debugging-nn-training ~/.claude/skills/
# Codex / 跨 runtime:目标改为 ~/.agents/skills/
```

**只装一个 skill**(以 `debugging-nn-training` 为例):

```bash
git clone --depth 1 https://github.com/ImWenyaoT/skills.git /tmp/skills \
  && cp -r /tmp/skills/debugging-nn-training ~/.claude/skills/
```

> 若你的客户端支持 `/install-skill` 命令,也可直接:
> `/install-skill https://github.com/ImWenyaoT/skills/tree/main/debugging-nn-training`

## 命名约定

- 全小写、连字符分隔;**动词/动名词开头**,描述「做什么动作」而非「是什么名词」 —— `drawing-paper-figures` 而非 `paper-figures`,`packaging-elsevier-submissions` 而非 `elsevier-submission-packaging`。
- 目录名与 `SKILL.md` 里的 `name:` 字段保持一致。
- `description` 以触发条件为主(「什么时候用」),便于 agent 在发现阶段判断是否加载。

## 许可与致谢

本仓库代码与文档按 [LICENSE](LICENSE)(MIT)发布。Agent Skills 格式由 [Anthropic](https://www.anthropic.com/) 提出并开源,规范见 [agentskills.io](https://agentskills.io)。
