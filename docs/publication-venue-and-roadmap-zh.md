# Text2CAD-GC：投稿选择、数据集建设与 Benchmark 论文路线图

> 版本：2026-09-16。投稿日期以各 venue 官方页面为准；尚未发布的 2027 日期均明确标为“未公布/规划估计”。

## 1. 结论先行

这个项目可以发展成论文，但当前 `v0.1.0` 仍是 **evaluator calibration pilot**，还不是可投稿的论文级 benchmark。现有 90 个解析双曲面样本、3 个控制样例和 PartABC 前 250 个模型的便利扫描，已经证明评测器能区分 G0/G1/G2，也揭示了真实 CAD 中 G2 接缝稀少；它们不足以证明 benchmark 的覆盖性、模型排名可靠性或强化学习方法有效。

最合适的主投稿目标是 **Computer-Aided Design** 的 Dataset Paper。该刊官方范围明确包括 AI in design、data-driven modeling、representation conversion，以及“significant benchmarks”；Dataset Paper 不强制算法创新，但要求数据集免费用于研究并接受与普通论文同等严格的审稿。这与“公开数据、严格几何定义、CAD kernel 评测器、系统性 baseline”最匹配。

如果论文同时给出有说服力的强化学习方法、多个可复现 Text-to-CAD baseline 和显著的跨模型提升，可以冲击 **CVPR/ICCV、SIGGRAPH/ACM TOG 或 ICLR/ICML**。其中：

- CVPR/ICCV 需要突出 3D 生成、视觉-图形、多模态和 benchmark 的广泛意义；
- SIGGRAPH/TOG 需要突出几何建模、曲面表示和算法贡献；
- ICLR/ICML 需要证明该奖励、训练方法或评测思想具有超越 CAD 单一应用的机器学习贡献。

以当前成熟度直接赶 ICLR 2027 或 CVPR 2027 主会，不建议。更合理的路线是先完成论文级数据和 baseline，再按成熟度选择 ICCV 2027（若正式截止仍在 2027 年 3 月附近）或滚动投稿 Computer-Aided Design。

## 2. 2026 至 2027 年 3 月前的投稿窗口

“博士含金量”不是学校统一换算的分数。PolyU 2026/27 RPg Handbook 要求博士论文形成原创、独立、连贯的研究，并对知识作出显著贡献；学校页面没有规定“必须发表某个级别或数量的论文”。具体认可仍取决于学院、课题组、导师、作者顺序和论文贡献。下表的评价是针对本课题的学术影响力和匹配度，不等于 PolyU 的毕业硬指标。

| Venue | 截止日期状态（截至 2026-09-16） | 对本项目的匹配 | 博士阶段价值 | 当前建议 |
|---|---|---|---|---|
| **Computer-Aided Design, Dataset Paper** | 全年滚动投稿 | **最高**：官方明确接收 CAD benchmark 和 dataset paper | 专业领域高；数据、评测器和长期引用价值强 | **首选主目标**。完成真实数据、baseline 和公开协议后投稿 |
| **CVPR 2027** | 注册 2026-11-10；全文 2026-11-16 AoE；已确认 | 中高：含 3D geometry、datasets and benchmarks、multimodal、RL、vision+graphics | 顶会，高 | 只有在 8 周内已有团队、算力、模型和大规模实验时才冲；当前 pilot 单独投稿不够 |
| **ICCV 2027** | 大会为 2027-10-02 至 10-08，香港；2027 CFP 截止尚未正式公布。2025 届全文为 3 月 7 日，故仅可把 2027 年 3 月作为规划窗口 | 中高，与 CVPR 类似 | 顶会，高 | **较合理的冲刺目标**，但等官方 CFP 后立即校正计划 |
| **SIGGRAPH 2027 / ACM TOG track** | 大会 2027-08-08 至 08-12；2027 技术论文截止尚未公布。2026 届表单/全文分别为 1 月 15/22 日，仅作估计 | 高：NURBS、B-Rep、曲面连续性和 geometric modeling 很契合 | 图形学旗舰，极高 | 必须有新的几何算法/表示或强方法；仅拼数据不够 |
| **Eurographics 2027 Full Papers / CGF** | 大会 2027-05-10 至 05-14；官方 CFP 已上线，但当前公开页未显示可核验的 deadline | 高：计算机图形学和几何处理契合 | 图形学强会/CGF 论文，较高 | 适合作为图形学方向主投或 SIGGRAPH 的稳健替代，持续查看正式 deadline |
| **ICML 2027** | 2027 CFP 尚未公布；2026 全文为 1 月 28 日，仅作规划参考 | 中低：需把 RL/评价学习做成通用 ML 贡献 | 顶会，高 | Benchmark 本身不够；需要方法与跨域泛化论证 |
| **ICLR 2027 Main** | 摘要 2026-09-18；全文 2026-09-25 AoE；已确认 | 中：明确接收 RL、geometry/topology、datasets and benchmarks | 顶会，高 | **本轮不赶**。当前距摘要仅 2 天且证据远未完整 |
| **ICLR 2027 Workshop** | 建议投稿 2027-02-01；最迟录用通知 2027-02-26；具体 workshop 自定 | 取决于是否有 3D generation / structured generation workshop | 反馈和建立合作有用；不能等同主会论文 | 可发布中期版本、收集同行意见，不应作为最终唯一成果 |
| **IEEE TVCG** | 全年滚动投稿 | 中：geometric modeling、shape analysis 属于范围，但更偏图形/可视化 | 强期刊，高 | 若 evaluator、可视分析和几何算法都很强，可考虑 |
| **Computer Aided Geometric Design** | 全年滚动投稿 | 高：曲线、曲面、NURBS、几何生成与分析高度匹配 | 专业数学/几何价值高 | 若论文侧重连续性数学、容差和曲面构造，优先级高于通用 AI 会 |
| **ASME JCISE** | 全年滚动投稿 | 高：solid/geometric modeling、computational geometry、AI/knowledge-intensive CAD | 工程设计领域较高 | 若论文强调工程产品生命周期、可制造性和 CAD 系统落地，适合 |
| **Advanced Engineering Informatics** | 全年滚动投稿 | 中高：AI 支持知识密集型工程活动 | 工程 AI 强期刊，较高 | 需要完整工程场景、知识表达和实际效益，不能只做几何小样本 |

### 推荐的投稿决策

1. **最稳且最契合：Computer-Aided Design Dataset Paper。** 以 benchmark 为主贡献，算法可以只是参考实现，但数据必须可研究使用、文档完整、评价严谨。
2. **最高风险/最高回报：ICCV 2027。** 以“Text-to-CAD 模型在局部微分几何上被现有指标误判”为问题，配套 RL 方法、公开 benchmark、强 baseline 和跨模型分析。正式 CFP 尚未发布，先按 2027 年 2 月完成全文倒排，不能把预测日期写进正式承诺。
3. **几何算法路线：SIGGRAPH/TOG 或 Eurographics/CGF。** 需要把贡献从“测 G0/G1/G2”提高到可靠的跨 kernel 连续性估计、可微/可训练的连续性目标，或新的混合 NURBS/analytic primitive 表示。
4. **中期反馈：ICLR 2027 Workshop。** 适合提交 work-in-progress；不能用它替代主论文。

## 3. “PartABC 的 G2 数据 + 其他 benchmark”是否可行

### 3.1 可行，但贡献不能定义成数据拼接

正确的论文贡献应当是：

> **一个面向 Text-to-CAD 的、设计意图感知（intent-aware）、由 CAD kernel 验证（kernel-verified）、逐接缝定位（seam-localized）的 G0/G1/G2 benchmark。**

它由多个数据源提供几何或文本种子，但采用统一的任务定义、标注规范、泄漏控制、容差协议和评价程序。数据来源本身不是创新；新的任务、可靠标签、测试协议和由此得到的科学发现才是创新。

现有数据可分工如下：

| 数据/benchmark | 可以贡献什么 | 不能直接承担什么 |
|---|---|---|
| PartABC / NURBGen | 大规模 text-CAD 对、作者 baseline 的官方可比性、真实 STEP/B-Rep 来源 | 当前 test convenience scan 不能转成训练集；自动观察到的 G2 不等于设计意图 |
| ABC | 大规模精确曲线/曲面、STEP/Parasolid、微分量和 patch 信息 | 原始模型版权和 Onshape 条款需逐项遵守；没有现成 Text-to-G2 意图标签 |
| Text2CAD-GC analytic controls | 精确公式、正负对照、评测器单元测试和 RL curriculum | 几何族单一，不能单独代表真实机械 CAD |
| CADTestBench | 可执行 prompt predicate 的评测范式 | 原版没有 seam-level G1/G2 真值，需要扩展 predicate |
| MUSE / Text2CAD-Bench / CADGenBench | 工程任务、复杂 prompt、有效性/拓扑/制造性评价设计 | 不能假定其所有原始数据可再分发；也不能把渲染/VLM 分数当连续性真值 |

### 3.2 38 条 G2 接缝可以做什么

当前扫描得到的 **38 条是 seam，不是 38 个完整模型**，并且来自 7/250 个模型。它们适合：

- 证明提取管线能在真实 CAD 上发现候选 G2；
- 设计难例和误差分析；
- 估算 G2 的稀有程度，指导定向挖掘；
- 作为人工标注规范的 pilot。

它们不适合直接作为论文最终测试集，因为样本集中在少数模型、来源是 convenience scan、设计意图未知，并且来自作者的测试数据。最终训练数据必须从不相交的训练来源构造，最终测试也必须按源模型隔离。

### 3.3 必须新增的工作

1. **数据权利矩阵。** 记录每个来源的 license、是否允许派生、是否允许重新分发原 STEP、是否要求 ShareAlike、正确引用和联系人。PartABC 是 CC BY-NC-SA 4.0；若使用其派生数据，应署名、注明改动、非商业并以相同许可发布。ABC 官方说明 CAD 模型版权归创建者，须遵守 Onshape 条款。
2. **设计意图标签。** 区分“几何上观察到 G2”与“文本要求这里必须 G2”。每条目标 seam 至少标 `intent=sharp/smooth`、`required_grade`、定位、相邻 face、尺寸/拓扑约束和允许容差。
3. **独立划分。** 按原始 CAD model ID、近重复几何族和所有 caption/旋转/缩放变体分组划分，禁止同源泄漏。
4. **容差协议。** 统一长度尺度，并公开位置、法向/切平面、曲率误差公式，采样密度和 adaptive refinement 规则。必须同时报告阈值通过率与连续误差分布。
5. **跨 kernel 校验。** 至少用 Open CASCADE 加一个独立 kernel/CAD 系统或专家检查一组分层样本；记录 STEP 导入修复行为，避免把 kernel healing 当成模型能力。
6. **防奖励投机。** 联合检查 CAD validity、prompt compliance、尺寸、拓扑、sharp-edge preservation 和 continuity；否则模型可以删除接缝、合并成单面或把应当锐利的边磨平来获得高 G2。
7. **隐藏测试。** 公开 train/validation，测试集至少保留一部分 prompt、STEP 真值或标签不公开，并提供 evaluator/server，降低针对测试集调参。
8. **多 baseline。** 至少包含 NURBGen、一个 CAD command/program baseline、一个 STEP/B-Rep 生成 baseline，以及自己的 SFT/no-RL、RL 和 oracle/analytic control。

## 4. 建议的数据规模与统计效力

Benchmark 没有“达到多少条就自动有效”的统一数字。应以**独立模型数**做功效和置信区间设计，不能把同一模型的许多 seam 当作彼此独立。

若估计一个约 50% 的通过率，在简单独立二项假设下：95% 置信区间半宽约 ±10% 需要约 96 个独立模型，±5% 需要约 384 个独立模型。真实 CAD 中 seam 聚类会降低有效样本量，因此应按模型 bootstrap，并准备更多模型。

建议版本目标：

| 阶段 | 独立 CAD 模型 | 指定目标 seam | 用途 |
|---|---:|---:|---|
| 当前 pilot | 90 个解析双面样本 | 90 | 评测器、奖励和单元测试 |
| 标注 pilot | 100–150 个真实模型 | 300–600 | 修订标注规范、测双人一致性、发现 kernel 问题 |
| 最小论文版 | 600–1,000 个真实模型 | 2,000–5,000 | 训练/验证/公开测试和分层统计 |
| 推荐完整版 | 2,000+ 个真实模型 | 8,000+ | 覆盖复杂曲面、稀有 G2、跨来源和跨 kernel 分析 |

每个核心测试层级（G0、G1-only、G2、sharp-preservation）应尽量拥有至少 100 个独立源模型；G2 不应依靠自然随机抽样，应定向挖掘 blend、fillet、loft、transition、aero surface 等几何族，再由人工确认意图。论文提交前应根据 pilot 的 baseline 差异和方差正式计算所需样本量，上述数字只是工程规划线。

## 5. Benchmark 的任务定义与指标

### 5.1 建议定义四个互补任务

1. **Continuity recognition**：给定 STEP/B-Rep 和指定 seam，判断达到的最高 G 等级。
2. **Text-to-CAD generation**：给定文本和目标 seam 要求，生成满足形状、拓扑和连续性的 CAD。
3. **Continuity repair**：给定有 G0/G1 缺陷的 CAD 和指令，修复到指定等级，同时保持其他设计约束。
4. **Preference/ranking**：比较两个候选 CAD，选择在满足意图前提下连续性更好的一个，用于 reward model 或 RL。

### 5.2 主指标必须按模型报告

- `Valid B-Rep rate`、可网格化率、闭合 solid 率；
- G0 pass rate；
- `G1 | G0` 条件通过率；
- `G2 | G1` 条件通过率；
- **all-required-seams pass rate**：一个模型所有指定接缝均通过；
- sharp-edge preservation：要求锐利的边没有被错误平滑；
- 最差值、95 分位和完整的位置/角度/曲率误差；
- prompt compliance、尺寸误差、拓扑正确率；
- CD/HD 等整体几何指标仅作辅助，不能代替逐接缝评价。

统计上用 model-level bootstrap 置信区间；模型之间用 paired comparison；人工标签报告 Cohen's kappa 或 Krippendorff's alpha；按曲面类型、接缝长度、曲率、拓扑复杂度和 kernel 分层报告，不只给总平均数。

## 6. 从现在到可投稿的逐步 TODO

### Phase 0：冻结研究问题（第 1 周）

- [ ] 写一页 `benchmark_spec_v0.1.md`：输入、输出、四个任务、评价单位、成功条件。
- [ ] 明确 `exact grade` 与 `at least grade`；例如 G2 样本同时满足 G0/G1，但分类标签可写最高等级。
- [ ] 确定论文主张：现有整体指标无法可靠反映 seam continuity；新 benchmark 能稳定区分并改变模型排名。
- [ ] 与导师确认主投路线：Dataset Paper，还是 benchmark + RL method。

**验收门槛：** 一位没有参与项目的人能根据规范独立判断一个样本的输入、真值和评分。

### Phase 1：系统性相关工作与 venue（第 1–2 周）

- [ ] 建表整理 Text2CAD、B-Rep/NURBS generation、CAD benchmark、surface continuity、RL for structured generation。
- [ ] 对每篇论文记录任务、数据、split、输出表示、指标、代码/权重、license、算力和不可复现点。
- [ ] 复核 NURBGen、STEP-LLM、Text2CAD、CAD-Llama/BrepGen 类方法是否能作为可运行 baseline。
- [ ] 每周检查 ICCV/SIGGRAPH/Eurographics/ICML 2027 官方 CFP，不引用 deadline 聚合站作为最终依据。

**验收门槛：** related-work matrix 覆盖所有将出现在主表中的 baseline，并解释遗漏方法为何无法比较。

### Phase 2：权利、来源和数据治理（第 1–2 周）

- [ ] 建 `DATA_PROVENANCE.csv`：source、original_id、URL、license、download date、allowed use、redistribution、citation。
- [ ] 对 gated 数据保留访问记录和版本 hash；不得提交 token 或私有下载链接。
- [ ] 若原始 STEP 不能重发，发布 ID、标注、hash、提取器和用户自行获取脚本。
- [ ] 为衍生数据选兼容 license；PartABC 派生部分遵守 CC BY-NC-SA 4.0。

**验收门槛：** 每一条将公开的数据都能追溯来源和许可；不清楚的条目不进入 release。

### Phase 3：改进 evaluator（第 2–4 周）

- [ ] 固定单位归一化、G0/G1/G2 数学定义和默认阈值。
- [ ] 增加 adaptive seam sampling、端点/奇异点处理、周期曲面和退化边处理。
- [ ] 区分 topology shared edge、几何近邻边和导入后 healing。
- [ ] 对解析曲面、扰动曲面、锐边、单面投机样本写测试。
- [ ] 在第二个 kernel/CAD 系统上复核分层样本，记录差异。

**验收门槛：** 解析真值 100% 符合预期；重复运行确定；阈值敏感性和跨 kernel 差异有报告。

### Phase 4：真实样本挖掘和去重（第 3–6 周）

- [ ] 只从允许的训练来源批量提取候选，不使用 NURBGen official test 训练模型。
- [ ] 按 blend/fillet/loft/transition/freeform/analytic surface、seam 长度和曲率分层。
- [ ] 使用 source ID、拓扑签名、几何 fingerprint 和近邻检索去重。
- [ ] 定向过采样 G2 和 hard negatives；保留真实分布子集用于 prevalence 分析。

**验收门槛：** 至少 100–150 个独立模型进入 annotation pilot，来源和去重记录完整。

### Phase 5：人工标注规范与一致性（第 4–7 周）

- [ ] 编写图文 annotation manual，定义 seam 定位、sharp/smooth intent、required grade 和 uncertain。
- [ ] 两名标注者独立标 100 个模型；冲突由 CAD 专家裁决。
- [ ] 计算标注一致性；若关键字段低于预设门槛，修订规范后重标。
- [ ] 自动几何 grade 与人工设计 intent 分栏保存，禁止互相替代。

**验收门槛：** 关键离散字段的一致性达到预注册标准，所有争议有 adjudication log。

### Phase 6：文本任务构造（第 5–8 周）

- [ ] 每个模型建立结构化 specification，再生成 2–3 种语言风格的 prompt。
- [ ] prompt 明确目标 seam、连续性、应保持锐利的边、尺寸和拓扑约束。
- [ ] 由人工核对 prompt 与 CAD 一致；LLM 生成只能作草稿，不能直接当真值。
- [ ] 生成 perturbation pairs：只改变一个连续性要求，用于因果对照。

**验收门槛：** 随机抽查不存在无法定位的“这里要光滑”等歧义指令。

### Phase 7：冻结 split 和隐藏测试（第 7–9 周）

- [ ] 按 source model family 分 train/validation/public-test/private-test。
- [ ] 所有 caption 改写、尺度、旋转和几何变体跟随源模型进入同一 split。
- [ ] 公开 split manifest 与 hash；冻结后只允许版本化修复。
- [ ] 私有测试通过容器或 evaluation server 评分。

**验收门槛：** 自动 leakage audit 为零；测试集在模型数、曲面族和难度上达到预定覆盖。

### Phase 8：实现完整评分协议（第 8–10 周）

- [ ] 输出 JSON schema、失败码、每条 seam 的误差与模型级总分。
- [ ] 同时报 validity、intent compliance、continuity、shape、topology、dimensions。
- [ ] 预注册主指标和 tie-breaker，不因实验结果临时改阈值。
- [ ] Docker/conda 锁版本，并做 clean-machine reproduction。

**验收门槛：** 第三方从 README 起步可在一小时内复现 analytic controls 和一个 baseline 的评分。

### Phase 9：baseline 复现（第 9–13 周）

- [ ] 为每个 baseline 固定权重版本、prompt、seed、temperature、最大 token、失败重试规则。
- [ ] 至少 3 类 baseline；报告无法运行/无权重的方法，而不是臆造结果。
- [ ] 保存原始输出、转换日志和每级失败率：文本/代码失败、B-Rep 失败、mesh 失败、solid 失败、G 连续性失败。
- [ ] 在同一硬件/服务预算下重复至少 3 个 seed 或 bootstrap。

**验收门槛：** 主表每一格均可追溯到样本级记录和运行配置。

### Phase 10：强化学习方法与消融（第 10–16 周，可与 Phase 9 并行）

- [ ] 先训练 SFT/no-RL control，再做 PPO/GRPO 或所选 RL 方法。
- [ ] 奖励由 validity、prompt、dimension、topology、sharp preservation、continuity 组成。
- [ ] 做 reward ablation、阈值敏感性、curriculum ablation 和 evaluator-overfitting 检查。
- [ ] 在 private test 和至少一个外部 benchmark 上验证泛化。

**验收门槛：** RL 对 model-level 主指标的提升具有置信区间，且没有通过删面/并面/过度平滑投机。

### Phase 11：统计、错误分析和 benchmark 审计（第 14–17 周）

- [ ] 报告置信区间、paired test、effect size，而不只报平均数。
- [ ] 按 geometry family、复杂度、prompt 类型和 source 分层。
- [ ] 人工复核所有高分但可视上失败、低分但设计合理的异常样本。
- [ ] 分析 evaluator false positive/negative、kernel sensitivity 和 missing-data bias。

**验收门槛：** 论文每个主要结论都有对应表/图、统计检验和失败案例。

### Phase 12：论文与公开发布（第 16–20 周）

- [ ] 准备 datasheet、benchmark card、license、citation、versioning、leaderboard policy。
- [ ] 主文包含：问题、相关工作、数据构建、数学定义、评测协议、baseline、RL/消融、统计、局限。
- [ ] 匿名仓库不泄露作者信息；检查 venue 的 arXiv、双投和 AI 使用政策。
- [ ] 请至少 2 位 CAD/geometry 研究者和 1 位 ML 研究者内部审稿。
- [ ] 根据目标 venue 改写论述，而不是同一篇稿子同时投稿。

**验收门槛：** 一键复现、匿名性、许可证、所有数字和图表均通过独立检查。

## 7. 实际时间判断

以 2026-09-16 为起点：

- **单人、首次做 benchmark：** 6–9 个月更现实；
- **3–5 人团队，已有可训练模型与算力：** 4–6 个月；
- **到 CVPR 2027 全文截止约两个月：** 只适合已有成熟数据和模型的团队，不适合从当前 pilot 开始补齐全部论文证据；
- **到 2027 年 2 月形成投稿稿件：** 团队并行可争取，目标是 ICCV 2027 规划窗口或期刊；
- **期刊路线：** 没有硬会期，可先保证数据质量和复现性，学术风险最低。

## 8. 现在最先做的十件事

1. 与导师确认论文定位：`benchmark paper` 还是 `benchmark + RL method paper`。
2. 把当前 38 条 G2 定义为候选 pilot，不再把它写成最终 G2 测试规模。
3. 建数据权利和 provenance 表。
4. 从无污染训练来源取 100–150 个真实模型做双人标注 pilot。
5. 冻结连续性数学定义、尺度归一化和阈值。
6. 增加第二 kernel/专家交叉验证。
7. 确定至少三个真正能运行的 baseline，并完成 10–20 样本 smoke test。
8. 用 pilot 方差和预期提升做样本量/power calculation。
9. 冻结大规模数据的 strata、split 和 hidden-test 方案。
10. 完成后再决定冲 ICCV/SIGGRAPH，或直接走 Computer-Aided Design Dataset Paper。

## 9. 官方依据

- [PolyU Research Postgraduate Student Handbook：PhD thesis requirement](https://www.polyu.edu.hk/gs/rpghandbook/section10-1/)
- [PolyU RPg Handbook：programme goals and thesis quality](https://www.polyu.edu.hk/gs/rpghandbook/section2)
- [ICLR 2027 Call for Papers](https://www.iclr.cc/Conferences/2027/CallForPapers)
- [ICLR 2027 Call for Workshops](https://www.iclr.cc/Conferences/2027/CallForWorkshops)
- [CVPR 2027 Call for Papers](https://cvpr.thecvf.com/Conferences/2027/CallForPapers)
- [CVF upcoming conferences：ICCV 2027 dates](https://www.thecvf.com/?p=137)
- [ICCV 2025 official dates（仅作往届规划参考）](https://iccv.thecvf.com/Conferences/2025/Dates)
- [ACM SIGGRAPH upcoming conferences：SIGGRAPH 2027 dates](https://www.siggraph.org/siggraph-events/conferences/)
- [SIGGRAPH 2026 Technical Papers（仅作往届规划参考）](https://s2026.siggraph.org/program/technical-papers/)
- [Eurographics 2027 official site](https://eg2027.isti.cnr.it/)
- [ICML 2026 Call for Papers（仅作往届规划参考）](https://icml.cc/Conferences/2026/CallForPapers)
- [Computer-Aided Design official journal description and Dataset Paper policy](https://shop.elsevier.com/journals/computer-aided-design/0010-4485)
- [Computer Aided Geometric Design official journal description](https://shop.elsevier.com/journals/computer-aided-geometric-design/0167-8396)
- [IEEE TVCG official scope](https://www.computer.org/digital-library/journals/tg/cfp-ieee-transactions-on-visualization-computer-graphics)
- [ASME JCISE official scope](https://www.asme.org/publications-submissions/journals/find-journal/journal-computing-information-science-engineering)
- [PartABC dataset card and CC BY-NC-SA 4.0 terms](https://huggingface.co/datasets/SadilKhan/PartABC)
- [ABC Dataset official page, formats and licensing note](https://deep-geometry.github.io/abc-dataset/)

