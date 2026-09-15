# G0/G1/G2 强化学习数据：现在有什么、怎么用

## 先看结论

本目录包含两种性质完全不同的数据：

1. `manifest.jsonl` + `geometry/`：90 个解析构造的两曲面 STEP，G0/G1/G2 各 30 个。它们有确定数学真值，可直接用于 reward 调试、curriculum learning 和小规模 RL pilot。它们不是复杂真实零件，不能单独支撑论文效果结论。
2. `../partabc-derived/seam_metrics.jsonl`：从 250 个真实 PartABC test STEP 计算出的 3,691 条双面接缝记录。它们有 observed continuity，却没有“设计意图”标签。由于来自官方 test，文件中明确标记 `safe_for_training=false`；训练使用会污染 NURBGen 测试结果。

## 90 个解析样本的数据划分

| Split | G0 | G1 | G2 | 合计 |
|---|---:|---:|---:|---:|
| train | 20 | 20 | 20 | 60 |
| validation | 5 | 5 | 5 | 15 |
| test | 5 | 5 | 5 | 15 |

生成器固定 seed 为 `20260916`，90/90 已由 Open CASCADE 7.9 验证为预期等级。样本记录示意：

```json
{
  "sample_id": "g2_025",
  "split": "test",
  "prompt_zh": "生成两片相邻三次 Bezier 曲面……接缝须严格达到 G2……",
  "target_grade": "G2",
  "reference_step": "geometry/g2_025.step",
  "surface_definition": {
    "left": "S1(u,v)=(L*u,W*v,0)",
    "right": "S2(s,t)=(L*(1+s),W*t,A*s+B*s^2+C*s^3)"
  }
}
```

## 为什么它们有数学真值

两片曲面在 `u=1` 与 `s=0` 相接：

\[
S_1(u,v)=(Lu,Wv,0),\qquad
S_2(s,t)=(L(1+s),Wt,As+Bs^2+Cs^3).
\]

- 任意 A/B/C 都在 `s=0` 位置相同，因此至少 G0。
- `A=0` 时跨缝一阶斜率为零，切平面相同，因此至少 G1。
- `A=0 且 B=0` 时二阶项也相同，因此达到 G2。
- 数据中的 exact G0 使用 `A≠0`；exact G1 使用 `A=0,B≠0`；G2 使用 `A=B=0,C≠0`。

这套构造让标签来自公式，而不是人眼看图或语言模型判断。

## 强化学习接口

把自然语言 prompt 交给模型，模型输出 CAD token、NURBS 参数或 CAD code；环境执行并导出 candidate STEP；奖励器读取 STEP：

```bash
python scripts/rl_continuity_reward.py \
  data/pilot/geometry/g2_025.step G2 --mode at_least
```

奖励包括 STEP 可读性、共享拓扑、G0 位置、G1 法向角和 G2 曲率差。对 G2 任务，典型层级奖励是：只达到 G0 < 达到 G1 < 达到 G2。`--mode exact` 用于要求恰好保留锐边/G0 或 G1-only；`at_least` 用于“至少达到某等级”。

训练时不能只给连续性奖励，否则模型可能通过减少接缝、输出单面或改变形状作弊。正式 reward 应组合：

\[
R=R_{validity}+R_{prompt}+R_{topology}+R_{dimension}+R_{continuity}+R_{sharp\ preservation}.
\]

其中 G2 任务可以使用分层连续性奖励：

\[
R_{continuity}=0.2e^{-d/\epsilon_0}
+0.3e^{-\theta/\epsilon_1}
+0.5e^{-\Delta\kappa/\epsilon_2},
\]

后两项分别只在 G0、G1 的前置条件满足时启用。

## 如何升级为真实零件训练集

1. 从 **ABC/PartABC 的训练 split** 取 STEP，绝不从最终 test split 取训练数据。
2. 用 `analyze_step_continuity.py` 对每条双面共享边计算 observed G grade。
3. 人工给每条候选边标 `intent=sharp/smooth` 和 `required_grade=G0/G1/G2`。自动 grade 不能替代设计意图。
4. 为零件写 prompt，并明确需满足连续性的区域或 feature，例如 “blade-to-hub blend must be G2”。
5. 按原始 ABC model ID 划分 train/validation/test；同一模型的 caption、旋转、尺度和变体不得跨 split。
6. 保留解析样本作 evaluator regression tests；用真实零件作训练和最终测试。

建议论文级数据至少包括：解析校准集、真实单接缝任务、真实多接缝零件、正确锐边保护任务四个 strata。当前 90 个样本只是第一层。

## 文件说明

- `manifest.jsonl`：90 个 prompt、公式、系数、split 和标签。
- `geometry/*.step`：90 个真值 STEP。
- `verification.jsonl`：OCCT 对每个样本的复核结果。
- `summary.json`：规模和通过数。
- `../partabc-derived/seam_metrics.jsonl`：真实 PartABC 接缝派生池，供理解和后续迁移脚本使用。

相关代码：

- `../../scripts/build_rl_continuity_dataset.py`：生成 90 个解析样本。
- `../../scripts/analyze_step_continuity.py`：从 STEP 计算连续性。
- `../../scripts/rl_continuity_reward.py`：可调用的分层奖励函数。
- `../../scripts/export_partabc_seam_pool.py`：把 250 模型结果转成逐行可读记录。

