# Agent Skills 开发规范

> **`CLAUDE.md` 是指向本文件(`AGENTS.md`)的符号链接——两者是同一份内容,改 `AGENTS.md` 即生效,零漂移。** 不同 runtime 各读各的文件名(Codex 读 `AGENTS.md`、Claude Code 读 `CLAUDE.md`),符号链接让两端都拿到全部规则。⚠️ 符号链接在 **Windows** checkout 上可能退化成纯文本(需 `git config core.symlinks true` + Developer Mode);本库默认只在 Mac/Linux 维护。
>
> 本文件是这个 **Agent Skills 仓库**的开发规范,规则取自 Anthropic 与 OpenAI 官方文档(见末尾「参考」),并固化了本仓库的实战做法。

> 这是一个**个人 Agent Skills 库**(源 = 本仓库,本地目录只是镜像),Codex 与 Claude 双端可用。
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
- 例:`training-models`、`writing-papers`、`journal-submissions`、`drawing-figures`。

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

## 指令强度(degrees of freedom)

**按每段内容的脆弱性选语气,不要全篇一个调门。** Anthropic 的比喻:窄桥 vs 开阔地。

- **窄桥**——脆弱、易错、顺序不能变。给精确步骤和硬判据。例:必须按序执行的迁移命令、训练前的 sanity check。
- **开阔地**——多条路都通、选哪条依上下文。给方向、给排序、**给每个选项的理由**,让模型自己判断。

**压缩时最容易出事**:把一份带理由的阶梯压成裸序列,就把引导写成了命令。模型照做,但选不对——因为你把判断依据删了。要么保留理由,要么把这段指向 reference 并说明"那里有每个选项的理由"。

**解释 why,而不是堆 MUST。** 全大写的 `ALWAYS`/`NEVER` 是黄信号:能改写成「目标行为 + 理由」就改写。今天的模型有 theory of mind,给了理由它能外推到你没写的情形;只给禁令它只会在你写到的那一条上听话。

**ASD-STE100 的取舍**:它的**词汇纪律**(一词一义、不为文采换词、主动语态、不省略成分、名词串 ≤3 词)对 agent 完全适用,与 Anthropic 的 "consistent terminology" 同向,该守。它的**命令语气**只适用于窄桥段落——那套规范是给飞机维修手册写的,那里每一步都是窄桥。整篇套用会把开阔地也写成窄桥。

参考:[Anthropic — Set appropriate degrees of freedom](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)、[OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills)。

## 触发测试(本库的验证闭环)

本库只做**离线**的一层:**该触发的声明了吗、不该触发的划清了吗**。

不做模型在环的路由指标(precision / recall / F1 / 混淆矩阵 / pass^k),也不做结果层
grader。这两层曾经实现过 375 行 + 一个 DeepSeek 路由器,在仓库全部历史里**一次都没跑过**
(把仓库的 skill 描述发给外部端点这件事从未获批),已删除。真需要时那是一次性调研,
不该常驻仓库。

工具与契约:

- `evals/trigger_cases.json`:每个 skill **≥2 条 positive + ≥2 条 forbidden** 用例;用**相邻 skill 做 hard negative**(如 writing-papers vs drawing-figures、journal-articles vs journal-submissions);路径专用 skill 的 positive 必须带路径/仓库/唯一站点信号、negative 覆盖泛化场景。
- `scripts/evaluate_skill_triggers.py`:三件事——**契约**(标签指向真实 skill、每个 skill 两向覆盖齐)、**anti-scope**(每条描述都得声明反向边界,且该边界被某条 forbidden 用例真正踩到)、**smoke**(prompt 与「路由器读 SKILL.md 之前能看到的那半边元数据」做词面重叠)。
- **反向边界必须写,而且必须被测。** 官方文档与实测都指向同一件事:缺反例的描述路由准确率明显下降,「做不到什么」往往比「能做什么」更能防误触发。词袋无法表示否定,所以反向边界不进正面打分(否则它的词会把 skill 往它自己排除的 prompt 上拽),而是单独跟 goldens 对账——**写了没人测的边界会被判失败**——曾经有一条反例指着两轮前就删掉的 skill,没有任何检查会对它有反应,于是一直活着。
- **smoke 的边界要知道**:它没有词干还原(`rewrite` 匹配不上 `rewriting`);中文只按「连续汉字段内的二元组」切,跨标点不成词;两个 skill 分数比值高于 `TIE_RATIO`(0.80)时**不下判决**,因为词面打分在那个区间读的是噪声(该阈值由本库 73 条正确案例的分布标定:干扰项/赢家的比值 95% 在 0.75 以下)。abstain 用例的 0.25 门槛在当前数据上几乎没有分辨力(abstain 最高 0.170,正例中位 0.159)——它挡的是灾难,不是精度。**smoke 过了不等于真实路由器会这么路由。**
- **改了任何 `description` 后重跑它**,并且看的是「相邻 skill 有没有被挤下去」,不是绝对分值。
- **改描述的 commit 不要同时改已有 golden。** 新增用例随时可以;修改或删除一条已有用例,是在动判分的基准,得单独成一次改动并写清理由——否则「描述改挂了顺手把用例改绿」和「修好了」在历史里长得一模一样。

## 提交前(与 CI 同款)

```bash
./scripts/ci.sh                             # CI 跑的全部检查,以脚本为准,不在这里抄一份
diff AGENTS.md CLAUDE.md                    # 符号链接是否退化(ci.sh 查不到这条;diff 为空即正常)
```

要求 **0 错误 0 警告**。每次 push/PR 由 `.github/workflows/validate-skills.yml` 自动校验。

## 新增 / 修改一个 skill 的流程

1. **先写评估**(Anthropic「start with evaluation」):在 `evals/trigger_cases.json` 加该 skill 的 positive/forbidden 用例(含相邻 hard negative)。
2. 写 `SKILL.md`:两段式名字、「何时用」描述(不复述 workflow)、正文≤500 行、**自洽不引用别的 skill**。
3. 重资料/脚本进 `references/`、`scripts/`;长引用文件加 `## Contents`。
4. 跑提交前检查,确认目标 skill 触发、相邻不串、域外 abstain。
5. **绝不"复活"被刻意删除/归档的 skill**——先与用户确认。

## 安装 / 更新

- **本仓库是唯一源**;已安装副本由 `npx skills` 管理,不要手工复制或编辑。
- 全局安装:`npx skills add ImWenyaoT/skills --all -g`。
- 发布新提交后更新:`npx skills@latest update -g`。
- 本机 Claude 的 `~/.claude/skills` 链接到统一的 `~/.agents/skills`;Codex 与 Claude 读取同一份安装。
- 加载方式:Claude Code 用 `Skill` 工具加载(不要手动 `Read` skill 文件);Codex 原生加载。

## 参考

- Anthropic — Agent Skills 创作 best practices:<https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices>
- Agent Skills 开放标准(`name`/结构规范):<https://agentskills.io/specification>
- Anthropic 工程博客 — Equipping agents with Agent Skills:<https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills>
- Anthropic — Demystifying evals for AI agents:<https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
- OpenAI Codex — Agent Skills(同 agentskills 标准,Codex 读 `AGENTS.md` + `SKILL.md`):<https://learn.chatgpt.com/docs/build-skills>
- OpenAI — Evals / Graders:<https://developers.openai.com/api/docs/guides/evals>
