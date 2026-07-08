# Agent Skills 开发规范

> **`CLAUDE.md` 是指向本文件(`AGENTS.md`)的符号链接——两者是同一份内容,改 `AGENTS.md` 即生效,零漂移。** 不同 runtime 各读各的文件名(Codex 读 `AGENTS.md`、Claude Code 读 `CLAUDE.md`),符号链接让两端都拿到全部规则。⚠️ 符号链接在 **Windows** checkout 上可能退化成纯文本(需 `git config core.symlinks true` + Developer Mode);本库默认只在 Mac/Linux 维护。
>
> 本文件是这个 **Agent Skills 仓库**的开发规范,规则取自 Anthropic 与 OpenAI 官方文档(见末尾「参考」),并固化了本仓库的实战做法。

> 这是一个**个人 Agent Skills 库**(源 = 本仓库,本地目录只是镜像),目前 15 个 skill,Codex 与 Claude 双端可用。
> 每个 skill = 一个自包含文件夹(`SKILL.md` + 可选 `scripts/`/`references/`/`assets/`),按**渐进披露**加载:
> 启动只读 `name`+`description`,匹配任务才读完整 `SKILL.md`,执行时再按需调脚本/引用文件。

## 黄金法则(本库的不可妥协项)

1. **每个 skill 必须自洽、可单独分享。** 一个 `SKILL.md` 里**禁止引用其它 skill**(不写「use `other-skill`」),**禁止依赖外部 skill**(如 `superpowers:*`、`skill-creator`)。
   - 理由:skill 是**在 agent 层组合**的(用户各自安装多个,模型自己挑着用);把一个 skill 单独发给别人,它不该还要别的 skill 才能用。
   - 需要表达边界时,**描述行为本身,不要点名兄弟 skill**:写「不处理 X」而不是「X 用 `other-skill`」。
2. **一个 skill = 一个可被发现的能力。** 不做大而全的 catch-all。判据:能不能给它写**一个具体的两段式名字 + 一句精准的「何时用」描述**?写不出来就是范围太宽,该收窄。
3. **内聚的任务域放一个 skill,内部用文件拆分**(progressive disclosure),而不是拆成多个 skill。
4. **改任何 skill 前先想触发,改完必须验证**(见「触发测试」)。

## 命名(Anthropic best-practices + agentskills.io 规范)

硬规则(required):

- 只允许**小写字母 + 数字 + 连字符**,**≤64 字符**;不能以 `-` 开头/结尾,不能出现连续 `--`。
- 不能含 XML 标签;不能用保留词 `anthropic` / `claude`。
- **目录名 == `SKILL.md` 的 `name:` 字段**(部分 loader 强校验)。

本库 house style:

- **两段式 `x-y`(单连字符)**、简短可扫读;名字要**具体可发现**,避免 `helper`/`utils`/`data`/`tools` 这类泛名。
- 例:`training-models`、`writing-papers`、`agent-loops`、`markdown-pdf`。

## 描述 `description`(Anthropic SDO)

- **第三人称**,以**触发条件**为主——回答「**何时用**」,而非「做什么/怎么做」。
- **关键词要密**:写用户真实会打的话(中文用户场景就放中文触发词),便于发现。
- **不要在描述里复述 workflow / 步骤**——否则 agent 会照描述办事、跳过正文。
- 反向边界(anti-scope)可以写(「Do not use for …」),但**只描述边界、不点名兄弟 skill**(自洽性)。
- `≤1024` 字符(目标 `<500`)。

## 正文与结构(Anthropic)

- `SKILL.md` 正文 **≤500 行**;超了把细节挪进 `references/`。
- **引用文件只下探一层**(从 `SKILL.md` 直接链到);**>100 行的引用文件需带 `## Contents` 目录**(本库 lint 项)。
- 可放心 bundle 大资源(API 文档、数据集、脚本)——**未被读取的文件零 token 开销**。
- 脚本优先 **`uv run`**、尽量 stdlib;**函数级注释**;新增脚本前先看现有脚本能否复用。

## 触发测试(本库的验证闭环)

把测试分两层(Anthropic Claude Code 指引):

- **(A) 路由层**:该触发的触发了吗?不该的闭嘴了吗?→ 分类问题(precision / recall / F1 / 混淆矩阵 / abstain 假触发率 / pass^k)。
- **(B) 结果层**:触发后照着做产出对吗?→ grader(代码判分优先,主观项用 LLM-judge)。

工具与契约:

- `evals/trigger_cases.json`:每个 skill **≥2 条 positive + ≥2 条 forbidden** 用例;用**相邻 skill 做 hard negative**(如 writing-papers vs drawing-figures、agent-evals vs persisting-traces);路径专用 skill 的 positive 必须带路径/仓库/唯一站点信号、negative 覆盖泛化场景。
- `scripts/evaluate_skill_triggers.py`:离线契约 + 元数据 smoke test;`--predictions <jsonl>` 进入真实指标模式(per-skill / macro / micro / weighted F1、abstain 假触发率、混淆矩阵、pass@k/pass^k、baseline 对比、selection-vs-outcome)。
- `scripts/route_with_llm.py`:模型在环路由器(OpenAI 兼容,默认 DeepSeek,`DEEPSEEK_BASE_URL`/`DEEPSEEK_API_KEY`),把每条 prompt 的真实触发抓成 predictions JSONL 喂给上面打分。
- **改了任何 `description` 后,重跑路由器确认不回退**(我们多次靠它发现/修复过度触发)。

## 提交前(与 CI 同款)

```bash
python scripts/validate_skills.py          # frontmatter / 目录名一致 / 正文≤500行 / 长引用需 Contents
python scripts/evaluate_skill_triggers.py  # 触发 goldens 契约 + smoke
python -m py_compile $(find . -path ./.git -prune -o -name '*.py' -print)
diff AGENTS.md CLAUDE.md                    # CLAUDE.md 应是 AGENTS.md 的符号链接(diff 为空;非空 = 符号链接退化了)
```

要求 **0 错误 0 警告**。每次 push/PR 由 `.github/workflows/validate-skills.yml` 自动校验。

## 新增 / 修改一个 skill 的流程

1. **先写评估**(Anthropic「start with evaluation」):在 `evals/trigger_cases.json` 加该 skill 的 positive/forbidden 用例(含相邻 hard negative)。
2. 写 `SKILL.md`:两段式名字、「何时用」描述(不复述 workflow)、正文≤500 行、**自洽不引用别的 skill**。
3. 重资料/脚本进 `references/`、`scripts/`;长引用文件加 `## Contents`。
4. 跑提交前检查;需要时用 `route_with_llm.py` 实测路由,确认目标 skill 触发、相邻不串、域外 abstain。
5. **绝不"复活"被刻意删除/归档的 skill**——先与用户确认。

## 同步 / 双端

- **本仓库是唯一源**;Claude 用 `~/.claude/skills/`,Codex 用 `~/.agents/skills/`(两端互相读不到对方的树)。
- 加载方式:Claude Code 用 `Skill` 工具加载(不要手动 `Read` skill 文件);Codex 原生加载。
- 要两端都用就把整个 skill 文件夹各拷一份;`./scripts/sync-to-local.sh` 一键同步本地镜像(保留本地第三方 skill 不动)。

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues for `ImWenyaoT/skills`; external PRs are not a triage request surface. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default five-label vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repo: read root `CONTEXT.md` and root `docs/adr/` if they exist. See `docs/agents/domain.md`.

## 参考

- Anthropic — Agent Skills 创作 best practices:<https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>
- Agent Skills 开放标准(`name`/结构规范):<https://agentskills.io/specification>
- Anthropic 工程博客 — Equipping agents with Agent Skills:<https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>
- Anthropic — Demystifying evals for AI agents:<https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
- OpenAI Codex — Agent Skills(同 agentskills 标准,Codex 读 `AGENTS.md` + `SKILL.md`):<https://developers.openai.com/codex/skills>
- OpenAI — Evals / Graders:<https://developers.openai.com/api/docs/guides/evals>
