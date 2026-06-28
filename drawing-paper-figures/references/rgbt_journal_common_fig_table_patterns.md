# RGB-T Tracking 期刊论文共有图表模式提炼

本文档基于 `output/rgbt_journal_fig_table_captions.md` 的自动 caption 审计结果，提炼 RGB-T tracking 期刊论文中最常见、最像“标准配置”的图表类型。

统计口径：

- 原始审计范围：`references/rgbt/tracking/journals/` 下 41 篇 PDF。
- 共有模式统计优先看方法论文子集：排除综述、benchmark/revisiting 类论文后，共 35 篇方法类论文。
- 统计是 caption 关键词层面的快速归纳，用于论文规划；正式写作时仍应回 PDF 人工确认版式和上下文。

## 一、几乎所有方法论文都有的部分

这些可以理解为 RGB-T tracking journal 方法论文的“基本盘”。如果缺失，审稿人很容易觉得证据链不完整。

| 图表类型 | 方法论文覆盖 | 作用 |
| --- | ---: | --- |
| 模块/机制细节图 | 35/35 | 解释核心模块内部结构，例如 fusion、adapter、attention、prompt、gate、Mamba、template update 等 |
| 方法总框架图 | 34/35 | 给出整体 pipeline，说明 RGB/T 输入、backbone、交互模块、head、template/update 的位置 |
| 主结果曲线/结果图 | 33/35 | 展示 PR/SR/NPR 曲线、benchmark 曲线、bar/radar/bubble 等结果可视化 |
| 组件消融表 | 34/35 | 证明核心模块不是堆料，说明各组件贡献 |
| 主 SOTA 对比表 | 29/35 | 与已有 RGB-T trackers 在 GTOT/RGBT210/RGBT234/LasHeR 等 benchmark 上比较 |
| 数据集/指标/设置表 | 29/35 | 交代 benchmark、metric、dataset setting、训练/评估口径，部分论文用文字替代表格 |

归纳成一套最小公共配置就是：

1. 一张 overall framework 图。
2. 一到两张核心模块细节图。
3. 一张或多张主结果曲线/结果可视化图。
4. 一张主 SOTA 对比表。
5. 一张组件消融表。
6. 一段或一张表说明数据集、指标、实现设置。

## 二、多数方法论文会补的部分

这些不是每篇都有，但出现频率很高。它们通常用来增强说服力，尤其适合 journal 版面。

| 图表类型 | 方法论文覆盖 | 作用 |
| --- | ---: | --- |
| 定性跟踪对比图 | 30/35 | 用多序列 frame panel 展示复杂场景下的跟踪稳定性 |
| 属性/挑战分析图 | 24/35 | 展示 low illumination、thermal crossover、occlusion、fast motion 等 challenge 下的表现 |
| 属性/挑战表 | 23/35 | 用表格补充 attribute-wise PR/SR，常和属性图二选一或同时出现 |
| 失败案例/限制图 | 20/35 | 主动说明方法边界，journal 论文里越来越常见 |
| 效率/复杂度表 | 19/35 | 报 Params、FLOPs、FPS、memory、runtime，回应实用性 |
| 参数/敏感性表 | 19/35 | 解释 threshold、layer、ratio、loss weight、sampling size 等选择 |

这类图表的共同逻辑是：主表说明“有效”，消融说明“为什么有效”，属性/定性/失败/效率说明“在什么条件下有效、代价是什么、边界在哪里”。

## 三、可选但有辨识度的加分项

这些不是所有论文都必须有，但如果和方法主线强相关，会显著增强叙事。

| 图表类型 | 方法论文覆盖 | 适合什么时候放 |
| --- | ---: | --- |
| 消融/参数敏感性图 | 16/35 | 当参数存在清晰趋势、phase transition 或 operating point 时，比表更直观 |
| 特征/响应/注意力可视化 | 13/35 | 当论文强调 reliability、attention、response quality、feature discrimination 时 |
| 速度-精度权衡图 | 13/35 | 当方法想证明不是只堆性能，也关注 FPS/Params/FLOPs 时 |
| 模态缺失/单模态鲁棒表 | 3/35 | 只有当方法主题涉及 missing modality、RGB-only/TIR-only 或 modality robustness 时才必要 |

## 四、映射到 CARE-Track 当前实验章

CARE-Track 当前第四章已经覆盖了 journal 方法论文的关键公共项：

| 公共项 | CARE-Track 当前状态 |
| --- | --- |
| 主 SOTA 对比表 | 已有 `tab:sota` |
| 组件消融表 | 已有 `tab:ablation` |
| 主结果曲线/结果图 | 已有 GTOT curves、LasHeR attribute radar |
| 定性跟踪对比图 | 已有 `fig:qualitative-tracking` |
| 参数/敏感性分析 | 已有 gate sweep 表和 gate diagnostic 图 |
| 效率/复杂度 | 目前只有正文描述，未成表 |

CARE-Track 更应该优先保留的公共核心：

1. `tab:sota`：主对比表，不能删。
2. `tab:ablation`：组件消融表，不能删。
3. 方法总框架图和 RAHF/update gate 机制图：属于几乎所有方法论文都有的图。
4. `fig:qualitative-tracking`：journal 常见强证据，建议保留。
5. gate sweep/diagnostic：和 CARE-Track 的 reliability closed loop 主线高度相关，虽然不是每篇都有，但对本文很关键。

CARE-Track 当前最值得补齐的公共项：

1. 效率/复杂度小表：Params、FPS，若能补 FLOPs 或 model size 更好。
2. 如果版面允许，加一张速度-精度权衡图或 LasHeR PR/SR 对比 bar/bubble；如果版面紧，可以不加，因为主表已经覆盖主对比。
3. 如果想强化 reliability 叙事，可补一张 response/reliability/gate accept-reject 可视化；这是加分项，不是基础项。

## 五、建议形成的 CARE-Track 实验图表骨架

若按“共有配置 + CARE-Track 主线”组织，推荐第四章图表保持为：

| 优先级 | 图表 | 是否必要 |
| ---: | --- | --- |
| 1 | 主 SOTA 对比表 | 必要 |
| 2 | 组件消融表 | 必要 |
| 3 | Reliability gate sweep 表或图 | 必要，贴合本文贡献 |
| 4 | Qualitative tracking panel | 强建议 |
| 5 | Efficiency table | 强建议补齐 |
| 6 | Attribute/radar 或 benchmark curves | 可保留其一，避免结果图过多 |
| 7 | Speed-accuracy bubble/bar | 可选 |
| 8 | Feature/attention/reliability visualization | 可选，适合 revision 或强化主线 |

一句话结论：RGB-T tracking journal 方法论文的共同骨架不是“图越多越好”，而是 `framework + module detail + SOTA table + ablation table + result curves/qualitative + efficiency/attribute 补证`。CARE-Track 现在主干基本齐了，最像公共缺口的是把 efficiency 从正文升级成表；最能体现本文差异的是保留并讲透 reliability gate sweep/diagnostic。

## 六、实验图通用铁律 checklist(每张图出图前/投稿前逐条过)

不分图种,所有实验图(尤其 PR/SR 曲线、speed-accuracy 散点、attribute radar)出图前对照,违反即返工。
配合 `analysis/figkit/`(palette_base / plot_helpers)代码化落实,别靠手调。

- [ ] **矢量格式**:导出 PDF/EPS/SVG,**绝不**在终稿放位图 PNG/JPG(截图类除外,且需高 dpi)。
- [ ] **字号够大**:缩到正文栏宽后,坐标轴刻度/图例/标注 ≥ 8pt。**小画布作图**(画布开小、字自然变大),而不是大画布配小字再缩。
- [ ] **色盲安全 + 不靠纯颜色编码**:用 ColorBrewer Qualitative / Viridis 类色板;曲线/柱再叠**线型或 marker 形状**双编码,黑白打印也能区分。
- [ ] **坐标轴诚实**:不截断 y 轴制造"差距很大"的错觉;若必须非零起点,显式标注。多子图同量纲共用刻度。
- [ ] **caption 自洽**:第一句直接给**结论/发现**(不是"Fig.X shows ...");图离开正文也能看懂。
- [ ] **无 chartjunk / 无 3D**:不要 3D 柱、阴影、渐变背景、多余网格;一张图只讲一件事。
- [ ] **图种匹配数据**:时序/阈值扫描→折线;多方法对比→分组柱;精度-速度/精度-参数权衡→散点(气泡);属性维度→雷达。别用错。
- [ ] **元素具名**:轴、图例、标注用真实名字(方法名/指标名),不留 "Module A" / "X" / "Y" 占位。

> 本 checklist 改编自 [HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) 的 figure-designer 通用规则(CC BY-NC-SA 4.0,© Yuyu Luo / HKUSTDial),已聚焦 RGB-T 实验图;架构图/动机图方法论仍以本仓 `prompts/architecture_figure.md` + `figkit/` 为准(不引入 PPT/Figma 手绘范式)。
