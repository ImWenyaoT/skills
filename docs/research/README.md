# 审计记录（2026-07）

这一目录是**当时的快照**，不是现状。六份文档针对 GitHub issue #2–#7 写成，
描述的是 19 个 skill 时期的库，行号和文件路径按当时的树。**刻意不回填。**

回填会让它们变成一份既非历史、也不可信的东西：结论是那时的，引用却指向现在的代码。
要判断某条结论今天还成不成立，读代码，不要读这里。

## 此后发生了什么

**19 → 10 个 skill。**

| 变化 | |
|---|---|
| 删除 | `offer-magic`（含 `grill-resume` / `grill-interview`）、`apple-hig`、`writing-resumes`、`spec-first` |
| `agent-loops` `tool-policies` `agent-evals` `persisting-traces` `bridging-legacy` | → `agent-runtime` |
| `mining-sessions` `importing-skills` | → `curating-skills` |
| `elsevier-articles` `elsevier-submissions`（外加两个此前不在仓库里的 IEEE skill） | → `journal-articles` `journal-submissions` |

**评估收缩了一半。** 模型在环的路由指标（precision / recall / F1、混淆矩阵、pass@k / pass^k）
与结果层 grader 已删除：那 375 行加一个 DeepSeek 路由器，在仓库全部历史里**一次都没跑过**——
把本库的 skill 描述发给外部端点这件事从未获批，`evals/writing_papers_outcome_fixtures.json`
自己记着这句话。留下的是离线契约检查与词面 smoke。

因此 `audit-trigger-eval-coverage.md` 里所有关于 `route_with_llm.py` 与 `--predictions`
的建议都已作废；`skill-rewrite-priorities.md` 的第 1 项（`elsevier-submissions` 的悬空归档依赖）
在写下之后就被修掉了，那条描述在合并前就已经过期。

## 还成立的部分

`skill-quality-rubric.md` 的判据本身与 skill 数量无关，仍然是本库的验收标准：
自洽边界、调用与描述、信息层级、完成判定的确定性。它综合自 matt pocock 的
`writing-great-skills`、Anthropic 的 skill authoring 文档，以及 OpenAI 的 Codex Skills
与 eval 博客——**没有移植任何开源 eval 实现**，`evaluate_skill_triggers.py` 是照那些散文手写的。
