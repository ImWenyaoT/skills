# 起草框架(从零写一篇技术论文)

## 来源与署名

骨架取自 **Jennifer Widom,《Tips for Writing Technical Papers》**(Stanford InfoLab,2006-01;2009 重讲时少量修订,2012 重讲未改)——原文:<https://cs.stanford.edu/people/widom/paper-writing.html>。本文件把其方法论复述、并按本库房规(顶会 CVPR/ICCV/NeurIPS/ICLR/ICML/ACL 风格、LaTeX、去 AI 味、证据约束)做了适配与补充;关键金句按原文短引。整篇原文未逐字转载,引用其方法时请保留以上署名。

## Contents

- [起草总原则](#起草总原则)
- [1. 标题 Title](#1-标题-title)
- [2. 摘要 Abstract](#2-摘要-abstract)
- [3. 引言 Introduction(五段式)](#3-引言-introduction五段式)
- [4. 相关工作 Related Work](#4-相关工作-related-work)
- [5. 正文 Body](#5-正文-body)
- [6. 性能实验 Experiments](#6-性能实验-experiments)
- [7. 结论 Conclusions](#7-结论-conclusions)
- [8. 未来工作 Future Work](#8-未来工作-future-work)
- [9. 致谢 / 引用 / 附录](#9-致谢--引用--附录)
- [10. 语法与小尺度表达](#10-语法与小尺度表达)
- [11. 排版机制 Mechanics](#11-排版机制-mechanics)
- [12. 版本与分发 Versions](#12-版本与分发-versions)
- [起草自查清单](#起草自查清单)

## 起草总原则

- **目标不是更花哨,是更像能被收的 paper**:语言自然、逻辑自洽、图表承担信息密度、结论严格基于证据。
- **铁律(与审阅一致):不编造**任何数据、实验、引用、结论或方法细节;缺什么就标 `[作者补充]`,绝不替作者杜撰。
- **一上来就去 AI 味**:别在初稿里堆 `novel`/`state-of-the-art`/`it is worth noting`;用 `improves SR by 1.8%` 这种可核验表述代替空洞自夸。
- **概念首次用「全称(缩写)」**,后文只用缩写;术语/记号像程序变量一样,用前先定义、且只定义一次。

## 1. 标题 Title

三种可选,按投稿气质选其一:

- **描述性长标题**:`Linear-Time External Multipass Sorting with Approximation Guarantees`。
- **简短型**:`Approximate External Sort`。
- **中庸 + 记忆点**(给方法起个好记的名字):`Floosh: A Linear-Time Algorithm for Approximate External Sort`。

房规:顶会偏好「记忆点方法名 + 一句话定位」;别把标题写成关键词堆砌。

## 2. 摘要 Abstract

> 原文要点:陈述「问题 / 你的方法与解决方案 / 论文主要贡献」,几乎不写背景与动机;事实但完整;**摘要里的话不要在正文里逐字重复**。

房规:摘要末尾可落一句定量主结果(如 `cuts sorting cost from O(n log n) to O(n) with bounded unsortedness`),但只能用论文真有的数。

## 3. 引言 Introduction(五段式)

引言**极其重要**:审稿人读完引言基本已经在心里决定收还是拒,后面只是找证据支撑这个判断;随性读者也靠引言决定要不要读下去。

Stanford InfoLab 的「五段式」——除非有充分理由,引言就是五段,各回答一个问题(原文逐字):

1. **What is the problem?**
2. **Why is it interesting and important?**
3. **Why is it hard? (E.g., why do naive approaches fail?)**
4. **Why hasn't it been solved before? (Or, what's wrong with previous proposed solutions? How does mine differ?)**
5. **What are the key components of my approach and results? Also include any specific limitations.**

然后加一段(或小节)**「Summary of Contributions」**:用 bullet 列主要贡献,并标明各在哪一节——这份 bullet 同时充当全文 outline,省篇幅、去冗余。

房规:第 ⑤ 点务必诚实写出局限;贡献 bullet 用 `\item`,与正文 `\section` 编号呼应。

## 4. 相关工作 Related Work

放**前**还是放**后**,看情况:

- **放前**(引言末小节或第 2 节):相关工作能写得既短又到位,或必须一开篇就对前作表明强硬的防御立场时。
- **放后**(结论前,可叫「Discussion and Related Work」):早处(引言/Preliminaries)能一句话带过,或充分对比需要先讲完本文技术内容时。

房规:对比前作只陈述事实差异,不贬低;别把 Related Work 写成文献流水账。

## 5. 正文 Body

两条适用于每篇论文的 Guideline(原文逐字):

- **Guideline #1**:`A clear new important technical contribution should have been articulated by the time the reader finishes page 3`(即全文 1/4 处之前,清晰的新技术贡献必须已经点明)。
- **Guideline #2**:`Every section of the paper should tell a story.` 故事要线性、每步都勾着读者往下读、**不出现重大打断**(打断进附录)。注意常见坑:别讲「你是怎么一路摸索得到结果的」,只讲**结果本身**的故事。

正文随内容而变,但常见组件:

- **Running Example**:尽量全程用一个贯穿示例,可放引言末小节或第 2/3 节。
- **Preliminaries**:放**非原创但必需**的记号与术语,作用是划清「哪些不是本文贡献」;务必简洁(记住 Guideline #1)。
- **Content**(算法/系统/新构造/分析):尽量 **top-down** 叙述——让读者看得到走向、能跳读也抓得住主旨。

## 6. 性能实验 Experiments

多数顶会期望有实验。容易踩两个坑:做 **hokey(空洞)实验**;以及只挑能让自己好看的设置。想清楚两件事:

- **measure 什么**:纯运行时间 / 对关键参数的敏感性 / 各维度可扩展性(数据规模、问题复杂度……)。
- **show 什么**:绝对性能(可用/可接受)/ 相对 naive 方法 / 相对前作 / 自家不同方案之间。

房规:报增益要给基线、设置一致性、必要时误差线/置信区间/显著性;别报账式罗列数字,要解释差异对主张意味着什么。

## 7. 结论 Conclusions

一般一小段收尾即可,**绝不照抄摘要或引言**。可借定量结果把当初的主张说得更具体(如用实测加速比回扣引言里的承诺)。

## 8. 未来工作 Future Work

体现论文如何开辟新方向,推荐 bullet。两点:

- 在做的后续**明说**(`We are currently extending the algorithm to…, and preliminary results are encouraging.`)——这是在**占坑**(mark your territory)。
- 有人从你的 Future Work 找选题,视为恭维,不必设防。

## 9. 致谢 / 引用 / 附录

- **致谢**:别漏,否则伤感情;讨论、读稿反馈、实现帮助等都该谢;拿不准就谢。
- **引用**:务必**完整且一致**;别从网上乱抄不一致的 BibTeX 了事,终稿逐条核对。
- **附录**:只放详细证明与算法。准则:① 附录不含理解论文贡献所必需的内容;② 把多数读者不感兴趣的细节都收进附录(超长论文尤其靠它)。

## 10. 语法与小尺度表达

强烈建议读 Strunk & White《The Elements of Style》。常见 pet peeves:

- 所有「变量」(术语/记号)用前先定义、且只定义一次(长间隔后可善意重述);全局定义归 Preliminaries,其余就近定义。
- **不要用「etc.」**,除非剩下的项完全显而易见。可:`phases 1, 3, 5, 7, etc.`;不可:`factors such as volatility, scalability, etc.`
- **不要写「for various reasons」**——把理由讲出来。
- 避免无指代的 `this/that/these/it`(Ullman pet peeve):要求显式写出 `this` 指什么,逼出清晰表达。
- 斜体用于**定义或引用,不用于强调**(Gries pet peeve);强调应由上下文自然给出。
- `that` vs `which`:`that` 限定(defining),`which` 非限定(nondefining)。`The algorithms that are easy to implement all run in linear time.` ↔ `The algorithms, which are easy to implement, all run in linear time.`

## 11. 排版机制 Mechanics

- 终稿**必跑拼写检查**,没有借口。
- 草稿/技术报告用 11pt、宽行距、1" 页边、单栏;别用会议双栏的小字挤版折磨读者。
- 图内字号约等于正文字号。
- 表/图/曲线/算法**置于页或栏顶**,除非极小可融入文流。
- 每个表/图/曲线/算法应出现在**首次引用的同页或次页**(LaTeX 允许的话)。
- 终稿提交/发表前**打印一遍**看看——纸面常与屏幕大不相同。

## 12. 版本与分发 Versions

- 常有「会议版(后正式发表)+ 网上完整版技术报告」。建议:完整版 = 会议版 + 附录;对外只保留完整版(会议论文集除外),与最终会议版同步,改完整版时覆盖所有公开旧版。
- 论文一完成就可挂网,注明日期、按技术报告引用(不必有正式编号)。**绝不**把只是投稿的论文挂上会议版权声明,**绝不**以「submitted to conference X」引用自己的论文——一两年后它发在会议 Y 上时只会自找尴尬。

## 起草自查清单

- 引言是否按五段式回答了「是什么/为何重要/为何难/为何未解决/我的方法与局限」,并有贡献 bullet 兼作 outline?
- 第 3 页前是否已点明清晰的新技术贡献(Guideline #1)?
- 每节是否讲一个线性、不被打断的 story(Guideline #2),且讲的是结果而非摸索过程?
- 摘要/引言/结论是否互不照抄?结论是否用定量结果回扣主张?
- 实验是否说清 measure 什么、show 什么,有基线与一致设置?
- 引用是否完整一致?致谢是否齐?附录是否只放非必需细节?
- 全文是否已去 AI 味、缩写规范、记号先定义后用?**是否没有编造任何数据/实验/引用/结论?**
