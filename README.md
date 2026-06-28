# skills

[![validate-skills](https://github.com/ImWenyaoT/skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/ImWenyaoT/skills/actions/workflows/validate-skills.yml)

> 田文耀的个人 Agent Skills 仓库 —— 用 GitHub 同步、**Codex / Claude 双端可用**的一组 [Agent Skills](https://agentskills.io)。

每个 skill 是一个自包含文件夹,含一份 `SKILL.md`(元数据 + 指令)和可选的 `scripts/`、`references/`、`assets/`。Agent 按**渐进披露**(progressive disclosure)加载:启动时只读 `name` + `description`,任务匹配时才把完整 `SKILL.md` 读进上下文,执行时再按需调用脚本/引用文件。

本仓库只收录**原创**且**泛用**的 skill——所有项目专有信息(代码路径、内部架构、个人身份)都已剥离,只留通用方法论。

## 目录(14 个)

### 🤖 Agent 工程 (Agent Engineering)

> 从实际搭 agent harness 的经验里提炼的通用工程技法。

| Skill | 用途 |
|-------|------|
| [`building-bounded-agent-loops`](building-bounded-agent-loops) | 在无状态请求处理器里写**有界** agent loop:一次请求一步、terminality/handoff 状态、按意图路由(便宜意图不触发检索)。 |
| [`running-agent-eval-loops`](running-agent-eval-loops) | agent 评估/回归 loop:evaluator 走接口、请求里 fire-and-forget 异步打分、golden 导出、failure-case 生命周期与阈值。 |
| [`wiring-agent-sdk-runners`](wiring-agent-sdk-runners) | 把厂商 agent SDK(如 OpenAI Agents SDK)封在边界后:有界 turns、feature-flag 选入、多 provider 配置、SDK 输出映射到你的 step 契约。 |
| [`designing-agent-tool-policies`](designing-agent-tool-policies) | 给 agent 设计 tools/policies/playbooks 运行时词汇:统一工具接口、风险分级 policy 门控、approval 硬停、确定性 stub。 |
| [`persisting-agent-memory-and-traces`](persisting-agent-memory-and-traces) | agent 持久化:session 状态、memory 快照、trace 落库、JSON→DB 迁移期的 fallback;证据进 trace 而非长期记忆。 |
| [`bridging-legacy-services`](bridging-legacy-services) | 用兼容适配器**包住遗留服务**而非重写:走适配器边界、先 build 再 import、迁移期保留 fallback。 |
| [`making-spec-first-changes`](making-spec-first-changes) | 文档驱动代码库里的 spec-first 纪律:改行为/架构/词汇前**先改文档**,一次变更只落一个 lane。 |
| [`running-adversarial-subagent-reviews`](running-adversarial-subagent-reviews) | 收尾前派一个**独立只读子代理对抗式终审**:树形协作、只挑 blocker/弱证据/scope 漂移,不重做。 |
| [`adopting-open-source-skills`](adopting-open-source-skills) | 引入外部/开源 skill 的纪律:核对 provenance 与 license、决定原样用/改/clean-room、记录署名。 |

### 🎓 学术论文 (Academic Paper)

| Skill | 用途 |
|-------|------|
| [`drawing-paper-figures`](drawing-paper-figures) | 为 Elsevier 风格期刊论文做图:先从参考语料推导字数/图数/配色预算,再用 figkit 画架构图、Ours-vs-baseline 散点、结果拼图(600 dpi)。 |
| [`packaging-elsevier-submissions`](packaging-elsevier-submissions) | 把成稿 LaTeX 手稿打包成 Editorial Manager 投稿包:声明集顺序、硬性规格、扁平 ASCII 源码 zip、cover letter。 |

### 🧠 机器学习 (Machine Learning)

| Skill | 用途 |
|-------|------|
| [`debugging-nn-training`](debugging-nn-training) | 神经网络训练常见错误自检清单:14 条静默失败的坑(overfit 单 batch、train/eval、zero_grad、logits-vs-softmax、view-vs-permute、shuffle、warmup…),每条「症状→为什么→怎么查→怎么改」+ 可运行脚本。 |

### ✍️ 写作 (Writing)

| Skill | 用途 |
|-------|------|
| [`writing-technical-resumes`](writing-technical-resumes) | 写/改/审技术简历的内容层:把任务流水账改成量化、成果导向、强动词的 bullet,按岗位裁剪,诚实红线。排版/导出交给你的简历工具。 |

### 🛠️ 元 / 工作流 (Meta)

| Skill | 用途 |
|-------|------|
| [`creating-skills-from-sessions`](creating-skills-from-sessions) | 从历史 agent 会话挖掘反复出现的摩擦,沉淀成新/改进的 skill:讲清 Codex/Claude 的 transcript 与 skill 存放位置、过滤 guardian 噪声、skill-vs-memory 取舍。 |

## 安装 / 同步

skill 格式是 [open agent skills standard](https://agentskills.io),**Codex 和 Claude 都直接读 `SKILL.md`**。按 scope 放进对应目录即可:

| 客户端 | 用户级目录 | 项目级目录 |
|--------|-----------|-----------|
| Claude Code | `~/.claude/skills/` | `<project>/.claude/skills/` |
| Codex / 跨 runtime | `~/.agents/skills/` | `<repo>/.agents/skills/`、`$REPO_ROOT/.agents/skills/` |

```bash
# 整库
git clone https://github.com/ImWenyaoT/skills.git /tmp/skills
cp -r /tmp/skills/building-bounded-agent-loops ~/.claude/skills/    # 或 ~/.agents/skills/

# 只装一个
git clone --depth 1 https://github.com/ImWenyaoT/skills.git /tmp/skills \
  && cp -r /tmp/skills/debugging-nn-training ~/.claude/skills/
```

> Codex 与 Claude 互相读不到对方的 skill 树;要两端都用,就把 skill 文件夹各拷一份(`cp -r`)。

## 命名约定

- 全小写、连字符分隔;**动词/动名词开头**(`building-`、`running-`、`writing-`),描述「做什么动作」而非名词。
- 目录名 == `SKILL.md` 的 `name:` 字段(部分 loader 强校验)。
- `description` 第三人称、以触发条件为主(「何时用」),≤1024 字符。

## 维护

**本仓库是唯一源**(source of truth);本地的 skill 目录只是它的镜像。

```bash
# 一键同步到本地两个镜像(保留本地第三方 skill 不动)
cp .sync-local.env.example .sync-local.env   # 首次:改成你机器的镜像路径(gitignored)
./scripts/sync-to-local.sh                   # 无配置时默认 ~/.claude/skills + ~/.agents/skills

# 提交前自查(与 CI 同款)
python scripts/validate_skills.py
```

每次 push / PR,GitHub Actions([validate-skills](.github/workflows/validate-skills.yml))自动校验所有 `SKILL.md` 的 frontmatter(`name`/`description` 合规、目录名一致、正文 ≤500 行、长引用文件需 `## Contents`)并编译内置 Python 脚本。

## 许可与致谢

本仓库按 [LICENSE](LICENSE)(MIT)发布。Agent Skills 格式由 [Anthropic](https://www.anthropic.com/) 提出并开源(规范见 [agentskills.io](https://agentskills.io));Codex 的 skill scope 见 [OpenAI Codex 文档](https://developers.openai.com/codex/skills)。
