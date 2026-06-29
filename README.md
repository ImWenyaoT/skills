# skills

[![validate-skills](https://github.com/ImWenyaoT/skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/ImWenyaoT/skills/actions/workflows/validate-skills.yml)

> 田文耀的个人 Agent Skills 仓库 —— 用 GitHub 同步、**Codex / Claude 双端可用**的一组 [Agent Skills](https://agentskills.io)。

每个 skill 是一个自包含文件夹,含一份 `SKILL.md`(元数据 + 指令)和可选的 `scripts/`、`references/`、`assets/`。Agent 按**渐进披露**(progressive disclosure)加载:启动时只读 `name` + `description`,任务匹配时才把完整 `SKILL.md` 读进上下文,执行时再按需调用脚本/引用文件。

本仓库优先收录**原创**且**泛用**的 skill——默认剥离项目专有信息(代码路径、内部架构、个人身份),只留通用方法论。少量高频个人项目工作流也可收录,但必须在用途说明里明确目标路径和边界。

## 目录(15 个)

### 🤖 Agent 工程 (Agent Engineering)

> 从实际搭 agent harness 的经验里提炼的通用工程技法。

| Skill | 用途 |
|-------|------|
| [`agent-loops`](agent-loops) | 在无状态请求处理器里写**有界** agent loop:一次请求一步、terminality/handoff 状态、按意图路由;并把厂商 agent SDK(如 OpenAI Agents SDK)封在 loop 的 provider 边界后(单 import 点、feature-flag 选入、多 provider 配置)。 |
| [`agent-evals`](agent-evals) | agent 评估/回归 loop:evaluator 走接口、请求里 fire-and-forget 异步打分、golden 导出、failure-case 生命周期与阈值。 |
| [`tool-policies`](tool-policies) | 给 agent 设计 tools/policies/playbooks 运行时词汇:统一工具接口、风险分级 policy 门控、approval 硬停、确定性 stub。 |
| [`persisting-traces`](persisting-traces) | agent 持久化:session 状态、memory 快照、trace 落库、JSON→DB 迁移期的 fallback;证据进 trace 而非长期记忆。 |
| [`bridging-legacy`](bridging-legacy) | 用兼容适配器**包住遗留服务**而非重写:走适配器边界、先 build 再 import、迁移期保留 fallback。 |
| [`spec-first`](spec-first) | 文档驱动代码库里的 spec-first 纪律:改行为/架构/词汇前**先改文档**,一次变更只落一个 lane。 |
| [`adversarial-review`](adversarial-review) | 收尾前派一个**独立只读子代理对抗式终审**:树形协作、只挑 blocker/弱证据/scope 漂移,不重做。 |
| [`importing-skills`](importing-skills) | 引入外部/开源 skill 的纪律:核对 provenance 与 license、决定原样用/改/clean-room、记录署名。 |

### 🎓 学术论文 (Academic Paper)

| Skill | 用途 |
|-------|------|
| [`reviewing-papers`](reviewing-papers) | 按顶会顶刊标准审稿/润色/审图:去 AI 味、逻辑自洽、图文联动、证据约束的数据分析、图表推荐、架构图 prompt;6 维度 + 8 输出模式 + P0/P1/P2 标签。 |
| [`drawing-figures`](drawing-figures) | 为 Elsevier 风格期刊论文做图:先从参考语料推导字数/图数/配色预算,再用 figkit 画架构图、Ours-vs-baseline 散点、结果拼图(600 dpi)。 |
| [`elsevier-submissions`](elsevier-submissions) | 把成稿 LaTeX 手稿打包成 Editorial Manager 投稿包:声明集顺序、硬性规格、扁平 ASCII 源码 zip、cover letter。 |

### 🧠 机器学习 (Machine Learning)

| Skill | 用途 |
|-------|------|
| [`debugging-training`](debugging-training) | 神经网络训练常见错误自检清单:14 条静默失败的坑(overfit 单 batch、train/eval、zero_grad、logits-vs-softmax、view-vs-permute、shuffle、warmup…),每条「症状→为什么→怎么查→怎么改」+ 可运行脚本。 |

### ✍️ 写作 / 文档 (Writing & Docs)

| Skill | 用途 |
|-------|------|
| [`writing-resumes`](writing-resumes) | 写/改/审技术简历的内容层:把任务流水账改成量化、成果导向、强动词的 bullet,按岗位裁剪,诚实红线。排版/导出交给你的简历工具。 |
| [`markdown-pdf`](markdown-pdf) | 把 Markdown 转成可打印的精致 PDF:封面、自动目录、代码高亮、斑马纹表格、页码。 |

### 🛠️ 元 / 工作流 (Meta)

| Skill | 用途 |
|-------|------|
| [`mining-sessions`](mining-sessions) | 从历史 agent 会话挖掘反复出现的摩擦,沉淀成新/改进的 skill:讲清 Codex/Claude 的 transcript 与 skill 存放位置、过滤 guardian 噪声、skill-vs-memory 取舍。 |

## 安装 / 同步

skill 格式是 [open agent skills standard](https://agentskills.io),**Codex 和 Claude 都直接读 `SKILL.md`**。按 scope 放进对应目录即可:

| 客户端 | 用户级目录 | 项目级目录 |
|--------|-----------|-----------|
| Claude Code | `~/.claude/skills/` | `<project>/.claude/skills/` |
| Codex / 跨 runtime | `~/.agents/skills/` | `<repo>/.agents/skills/`、`$REPO_ROOT/.agents/skills/` |

```bash
# 整库
git clone https://github.com/ImWenyaoT/skills.git /tmp/skills
cp -r /tmp/skills/agent-loops ~/.claude/skills/    # 或 ~/.agents/skills/

# 只装一个
git clone --depth 1 https://github.com/ImWenyaoT/skills.git /tmp/skills \
  && cp -r /tmp/skills/debugging-training ~/.claude/skills/
```

> Codex 与 Claude 互相读不到对方的 skill 树;要两端都用,就把 skill 文件夹各拷一份(`cp -r`)。

## 命名约定

- 全小写、连字符分隔,**两段式 `x-y`**(单连字符、简短可扫读);名字要**具体可发现**,避免 `helper`/`utils`/`data` 这类泛名。
- 目录名 == `SKILL.md` 的 `name:` 字段(部分 loader 强校验)。
- `description` 第三人称、以触发条件为主(「何时用」),≤1024 字符。

## 维护

**本仓库是唯一源**(source of truth);本地的 skill 目录只是它的镜像。

```bash
# 一键同步到本地两个镜像(保留本地第三方 skill 不动)
cp .sync-local.env.example .sync-local.env   # 首次:改成你机器的镜像路径(gitignored)
./scripts/sync-to-local.sh                   # 无配置时默认 ~/.claude/skills + ~/.agents/skills

# 提交前自查(与 CI 同款核心检查)
python scripts/validate_skills.py
python scripts/evaluate_skill_triggers.py
python -m py_compile $(find . -path ./.git -prune -o -name '*.py' -print)
```

每次 push / PR,GitHub Actions([validate-skills](.github/workflows/validate-skills.yml))自动校验所有 `SKILL.md` 的 frontmatter(`name`/`description` 合规、目录名一致、正文 ≤500 行、长引用文件需 `## Contents`),检查 `evals/trigger_cases.json` 的触发边界 goldens,并编译内置 Python 脚本。

### Skill 触发健康

`description` 是 Agent 在加载完整 `SKILL.md` 前能看到的主要触发信号。新增或改动 skill 时,同步维护 `evals/trigger_cases.json`:

- 每个 skill 至少 2 条 `expected_skills` positive case。
- 每个 skill 至少 2 条 `forbidden_skills` negative case。
- 用相邻 skill 做 hard negative,例如论文审稿 vs 论文绘图、agent eval vs trace persistence。
- 路径专用 skill 必须在 positive case 里出现路径、仓库或唯一站点信号,并在 negative case 里覆盖泛化场景。

```bash
python scripts/evaluate_skill_triggers.py

# 如果有真实 agent/sub-agent trace,可用 JSONL 计算 precision/recall:
python scripts/evaluate_skill_triggers.py --predictions /path/to/predictions.jsonl
```

`predictions.jsonl` 每行对应一个 case:

```json
{"id":"reviewing-papers-positive-rebuttal","actual_skills":["reviewing-papers"]}
```

## 许可与致谢

本仓库按 [LICENSE](LICENSE)(MIT)发布。Agent Skills 格式由 [Anthropic](https://www.anthropic.com/) 提出并开源(规范见 [agentskills.io](https://agentskills.io));Codex 的 skill scope 见 [OpenAI Codex 文档](https://developers.openai.com/codex/skills)。
