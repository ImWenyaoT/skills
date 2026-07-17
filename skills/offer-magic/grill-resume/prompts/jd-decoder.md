# JD Decoder

**目标：** 把一份招聘话术 JD 翻译成“招聘经理真实需求”的结构化情报，供简历与面试准备复用。

**铁律提醒**
- 一次只问一个问题。缺信息别全列出来一次问完。
- 不要装作了解某公司内部情况。所有团队 / 文化判断都标"我从 JD 的 ___ 推断"。
- JD 链接抓不到内容 → 直接让用户粘贴 JD 文本，别瞎编。

---

## Step 1 · 收齐输入

向用户要：

1. **JD 全文**（必需）。链接给了就先尝试，抓不到就要文本。
2. **公司名 + 岗位 + Level**（必需，JD 里没明写就问用户）。
3. **目标 Level**（可选）。如果用户面的 Level 跟 JD 标的不一样，后面的 Must Have 解读会变。

**不要在缺 JD 全文的时候硬猜。** 摘要不够用——JD 的 Hidden Signal 经常藏在用词、顺序、措辞里。

---

## Step 2 · 先标准化原始 JD

当输入来自复制粘贴的 `.txt` 或 `.md` 时，先创建 `docs/offer/`，按一岗一文件保存为 `docs/offer/<岗位名称>.md`。每份文件只保留一个一级标题和三个二级区块：`职位描述`、`任职要求`、`加分项`。

- 忠于原文，只统一编号、空行和基础标点。
- 删除招聘网站导航、联系方式、地点、更新时间、隐私政策和公司介绍。
- `主要职责`、`岗位职责`归入`职位描述`。
- 没有明确加分项时写`无`；不要移动任职要求中的“优先”条款。
- 多个岗位必须拆成多个文件，不能混合后再解码。

标准化完成后，以下步骤只读取对应岗位的单份文件。

---

## Step 3 · 五图层结构化拆解

按顺序产出，**别跳层**。

### 图层 1 · 招聘经理真实需求（最值钱）

把 JD 的营销话术翻译回招聘经理的实际期望。方法：

- 对每一条 JD requirement 问自己："字面要求是 ___，但招聘经理真正想要的人是 ___。" 两者经常不一样。
- 区分**硬要求**和**话术包装**——很多 JD 写"strong experience with X"其实意思是"做过 X 一两次就行"。
- 参考 [../frameworks/decode-patterns.md](../frameworks/decode-patterns.md) 的话术翻译表。

输出格式：

```
JD 写：
> "Looking for Product Designer with strong AI experience"

实际上招聘经理在找：
✅ 做过 AI 产品（最好端到端发过 1+ 个）
✅ 能跟 PM 和工程师快速推进
✅ 能从 0-1 定义产品形态
❌ 不需要会训模型 / 写 prompt eval pipeline
```

3-5 条这种翻译就够了，挑 JD 里最关键的几条。

### 图层 2 · Must Have（不满足就 reject）

3-5 条，每条**必须可验证**（看简历能看出来 / 面试能问出来），不能是虚的 buzzword。

格式：每条一句话 + 一个"为什么是 must"的简短理由。

> 例：
> - **AI 产品经验** — JD 里反复出现 + 团队明显在做 AI 方向
> - **Stakeholder management** — 提到 "work cross-functionally with PM, ENG, Research"
> - **End-to-end design ownership** — 提到 "from concept to ship"

### 图层 3 · Nice to Have（加分项）

3-5 条。这些**没有不会被 reject，有就明显加分**。

> 例：
> - Coding 能力（HTML/CSS/JS）
> - Startup / 早期阶段经验
> - 数据分析 / 实验设计

### 图层 4 · Hidden Signals（隐藏需求 / 文化信号）

JD 措辞里藏的"招聘经理希望这个人是怎样的人"。这是最容易被忽略也最容易出彩的部分。

参考 [../frameworks/decode-patterns.md](../frameworks/decode-patterns.md) 的 Hidden Signal 词典。常见信号：

| JD 出现的词 / 句式 | 信号 |
|---|---|
| ambiguity / unstructured / no playbook | 找自驱型，不要执行型 |
| ownership / drive / accountable | 期望端到端负责，不靠领导推 |
| influence / partner / align | 跨团队协作很重，politics 不轻 |
| fast-paced / move quickly / ship | 节奏快 / 早期阶段 / 可能加班 |
| craft / pixel-perfect / high bar | 高要求文化，作品集会被细抠 |
| mission-driven / impact | 文化匹配会被问 / 愿意降薪信号 |
| "you've shipped …" 列了具体产物 | 对作品集 / Portfolio Review 期待高 |

输出格式：

```
JD 反复出现 "ambiguity" + "ownership" + "drive"
→ 信号：这家公司在找**自驱型设计师**，不是等需求文档的执行者。
→ 面试和简历都要突出"我主动定义问题 / 推动决策"的故事。
```

3-5 条最有信号的就够。

### 图层 5 · Level / 团队 / 阶段判断

从 JD 推断这个职位的"实际形状"：

- **Level**：JD 标的 Title vs 职责暗示的实际 Level（经常有差）。
- **团队规模**：单干？小团队（< 5）？大组（10+）？JD 里有没有透露。
- **团队阶段**：0-1 / 1-N / 成熟 / 转型。
- **汇报关系**：报告给谁？（Design Lead / Head of Design / PM / CEO）
- **可能的痛点**：为什么现在招？（扩张 / 补缺 / 新方向）

每条都标推断依据，不知道就写"JD 没透露"，**不要装作知道**。

---

## Step 4 · 返回可复用结果

输出五个图层、原文证据、推断标记和可能改变结论的假设。默认返回到当前任务；只有用户要求或工作区配置明确指定路径时才持久化。

---

## Step 5 · 导流下一步

解码完毕，主动问：

> “JD 解码完了。下一步你想做什么：
> - 算一下你的简历跟它的**匹配度**？
> - 交给 `grill-resume` **审查或修改简历**？
> - 看看面试**会问哪些题**？
> - 还是先评估**值不值得投**？”

让用户选，不要自动接着跑下一条流程。

---

## 常见卡点

| 症状 | 处理 |
|---|---|
| JD 太短 / 全是 buzzword | 主动告诉用户"这份 JD 信息量不够，我能解出的部分有限，建议补充：① 公司近期产品方向 ② LinkedIn 上 hiring manager 信息 ③ 团队其他成员背景" |
| JD 是中文 / 国内公司 | 套路一样，但 Hidden Signal 词典要切换（"狼性" / "拥抱变化" / "结果导向" 各有所指） |
| 用户只给链接抓不到 | 让用户粘 JD 文本，**别根据公司名瞎猜 JD 内容** |
| 用户问“我能不能投” | 解码后基于硬条件、目标契合和机会成本给出建议，不用虚构的概率代替判断。 |
