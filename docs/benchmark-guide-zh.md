# 强化学习 Text-to-CAD 论文：Benchmark 与 G0/G1/G2 训练集说明

## 1. 9 类相关资源能否直接成为测试集

**不能。上一版的 9 行是“资源地图”，不是 9 个可直接使用的测试集。** 对你的论文，应按下表处理。

| 资源 | 在论文中扮演什么角色 | 能否原样测试 G0/G1/G2 | 具体用法 |
|---|---|---:|---|
| NURBGen PartABC test | baseline 的官方/准官方测试数据 | 否 | 保留原 split，比 CD/HD/JSD/MMD/IR 和输出有效性；不可拿来训练后再测试 |
| CADTestBench | 通用 Text-to-CAD prompt compliance benchmark | 否 | 原样测尺寸、拓扑、solid 等；把你的 STEP 用 CadQuery import wrapper 暴露给 CADTests |
| Text2CAD-Bench | 复杂度和 freeform prompt 来源 | 当前公开版不够 | 公开 151 条只有 prompt，缺完整 GT/evaluator；暂不作主表，等完整发布再纳入 |
| MUSE | 工程功能、制造、装配 benchmark | 否 | 原样报告 code/geometric/VLM rubric；花瓶 G1/G2 文本只能作 prompt 种子 |
| CADGenBench | STEP validity、形状、接口和拓扑 leaderboard | 否 | 若论文覆盖 drawing/editing，可直接提交；不把它当纯 Text-to-CAD 连续性测试 |
| Text2CAD/DeepCAD | 训练数据/旧方法 benchmark | 否 | 复现旧 baseline 或作简单 sketch-extrude 数据，不适合 G2 主实验 |
| ABC/BrepGen/AutoBrep/BrepGPT 数据 | exact B-Rep 数据源及 baseline | 否 | 从训练 split 构造真实 continuity 数据；这些名字不能合并算成多个独立 benchmark |
| STEP-LLM 数据 | 带 caption 的 exact STEP 数据源/baseline | 否 | 提供 text–STEP 配对，人工补 seam intent 后进入自建数据 |
| StepScore | 辅助参考评测工具 | 否 | 法向/曲率分布可放补充实验，但不能称为 seam G1/G2 指标 |

### 推荐你论文最终采用的 4 组评测

1. **NURBGen PartABC official test**：回答“相对原 baseline，整体形状和 IR 是否提高”。
2. **CADTestBench**：回答“是否满足文本中的尺寸、拓扑和实体要求”。
3. **MUSE 或 CADGenBench 二选一**：回答工程可用性；按你的输入模态选择。
4. **自建 Text2CAD-GC**：回答“生成 CAD 的指定接缝是否真正达到 G0/G1/G2”。这是你的核心贡献，不能被前三组替代。

这样主表不是“抄 9 个 benchmark”，而是 3 个现有 benchmark + 1 个专用 continuity benchmark。若计算资源有限，最低配置是 PartABC + CADTestBench + Text2CAD-GC。

## 2. 38、252、3318 到底表示什么

扫描单位是 **edge seam（接缝）**，不是模型，也不是 prompt：

- 38 条 G2 seam，来自 7/250 个模型；每条 G2 同时满足 G0 和 G1。
- 252 条 G1-only seam，满足 G0/G1，但没有通过 G2。
- 3318 条 G0-only seam，只在位置上接合，很多是本来就应该尖锐的机械棱边。
- 此外还有 68 条 G0 fail 和 15 条 unknown。

所以，“能作为 G2 正样本的候选”确实只有 38 条接缝；“整个模型所有相关接缝均为 G2”的样本数并没有由这张统计直接给出。更不能说只有这 38 条才有测试价值：G1-only 和 G0-only 是区分模型能力、检测奖励函数是否误判所必需的负例。

当前 38 条也不能直接成为论文测试集，因为：

1. 它们来自顺序抽取的 250 个便利样本；
2. 标签是按阈值计算的 observed grade；
3. 没有人工确认该边设计上是否应该 G2；
4. 多条 seam 来自同一模型，不是独立样本。

## 3. 上一轮 JSON 是不是原始数据

不是。`partabc_250_continuity.json` 是我们运行 OCCT 后产生的 **derived evaluation result**。原始数据有三部分：

- `source.step`：真实 B-Rep，包含共享 edge、face adjacency 和参数曲面；
- `nurbs.json`：NURBGen 使用的逐面 NURBS/trim 数据；
- `caption.json`：文本描述。

连续性标签不是作者随数据提供的，而是从 STEP 两侧曲面的一阶/二阶微分计算得到的。为了方便阅读，已经把大 JSON 转为逐 seam 的 [`rl_continuity_dataset/partabc_real_seam_pool.jsonl`](../data/partabc-derived/seam_metrics.jsonl)。其中每行都明确写 `design_intent_known=false` 和 `safe_for_training=false`。

## 4. 现在交付的真实代码和数据

### 4.1 有严格数学真值、可立即跑 RL 的 pilot 数据

[`rl_continuity_dataset/README.md`](../data/pilot/README.md) 中有 90 个 STEP：G0/G1/G2 各 30，训练/验证/测试为 60/15/15。它们不是图片，而是可由 CAD kernel 打开的、带共享拓扑的 STEP；manifest 保存 prompt、曲面公式、控制系数和标签。

它们的用途是：

- 校准 evaluator；
- 让模型先学习 G0→G1→G2 的分层奖励；
- 检查 PPO/GRPO reward 是否能把 G0-only、G1-only、G2 排成正确顺序；
- 做 curriculum 的第一阶段。

它们不能单独作为论文最终 benchmark，因为几何族过于简单。

### 4.2 真实零件的 PartABC seam pool

`partabc_real_seam_pool.jsonl` 有 3,691 条真实双面接缝记录。当前只用于理解数据结构和验证迁移流程。正式训练应把同一个提取脚本运行在 PartABC/ABC **training split** 上，然后人工补 design intent；不能把当前 official test 数据用于训练。

### 4.3 可直接接 RL 的奖励代码

[`scripts/rl_continuity_reward.py`](../scripts/rl_continuity_reward.py) 接收 `candidate.step + target grade`，返回 0–1 reward、是否成功、观测等级和误差分量。G2 目标下，本地验证结果为：

- G0-only candidate：reward 低，失败；
- G1-only candidate：reward 中等，失败；
- G2 candidate：reward 1.0，通过。

它已经形成分层信号，适合 PPO/GRPO。正式训练还必须叠加 shape、dimension、topology、validity 和 sharp-edge preservation，防止 reward hacking。

## 5. 模型怎样才能有效学到 G0/G1/G2

训练样本不能只有“这个 STEP 是 G2”。每条样本至少应有：

```text
prompt
reference STEP 或明确几何约束
目标 seam 的空间/语义标识
intent: sharp 或 smooth
required_grade: G0/G1/G2
位置误差、法向角、曲率差
validity / topology / dimension 约束
```

建议三阶段训练：

1. **解析 curriculum**：使用本地 90 个样本学会等级和奖励顺序。
2. **真实单接缝 curriculum**：从 ABC training split 抽取 fillet、blend、loft、airfoil、transition surface 等样本，人工标目标 seam。
3. **真实多接缝零件 RL**：prompt 指定哪些边要锐、哪些边要 G1/G2；奖励按 required seams 的最差值或 all-pass 计算，避免均值掩盖一条失败接缝。

最终测试集必须按原始 model ID 与训练集完全隔离；所有缩放、旋转、caption 改写和几何变体跟随源模型留在同一 split。

## 6. 当前交付与下一步边界

现在已经具备：可运行的数学样本生成器、90 个真值 STEP、manifest、验证结果、PartABC 真实 seam 池和 RL reward。它足以让你理解 G0/G1/G2 如何在代码和数学上进入训练。

要形成论文级 Text2CAD-GC，还需要从无污染的 ABC/PartABC train split 批量取样、人工标 design intent、构建复杂真实零件 strata，并冻结评测容差。这部分是正式数据集建设工作，不能用当前 38 条 G2 seam 直接替代。

