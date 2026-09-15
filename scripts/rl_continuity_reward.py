r"""Reference RL reward for the two-patch G0/G1/G2 curriculum.

Run with the Python environment containing pythonocc-core:
  python rl_continuity_reward.py candidate.step G2
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

from analyze_step_continuity import analyze

ORDER = {"G0_fail": -1, "unknown": -1, "G0_only": 0, "G1_only": 1, "G2": 2}


def score(candidate: Path, target: str, mode: str = "at_least") -> dict:
    result = analyze(candidate)
    if not result.get("read_ok"):
        return {"reward": 0.0, "success": False, "reason": "STEP read failed", "analysis": result}
    edges = result.get("edges", [])
    # The curriculum contract requires exactly two faces and one shared seam.
    topology = max(0.0, 1.0 - 0.25 * abs(len(edges) - 1))
    if not edges:
        return {"reward": 0.10 * topology, "success": False, "reason": "no two-face shared seam", "analysis": result}
    edge = edges[0]
    observed = edge["grade"]
    c0 = float(ORDER.get(observed, -1) >= 0)
    g1 = float(ORDER.get(observed, -1) >= 1)
    g2 = float(ORDER.get(observed, -1) >= 2)
    thresholds = result["thresholds"]
    c0_error = edge.get("max_c0_model_units")
    g1_error = edge.get("max_g1_angle_deg")
    g2_error = edge.get("max_g2_curvature_gap")
    # Dense terms give PPO/GRPO a gradient-like ordering before a hard pass.
    c0_dense = math.exp(-c0_error / thresholds["c0_model_units"]) if c0_error is not None else 0.0
    g1_dense = c0 * math.exp(-g1_error / thresholds["g1_angle_deg"]) if g1_error is not None else 0.0
    g2_dense = g1 * math.exp(-g2_error / thresholds["g2_relative_percent"]) if g2_error is not None else 0.0
    target_level = {"G0": 0, "G1": 1, "G2": 2}[target]
    observed_level = ORDER.get(observed, -1)
    if mode == "exact":
        success = observed_level == target_level
        hierarchy = {"G0": c0_dense, "G1": 0.4 * c0_dense + 0.6 * g1_dense, "G2": 0.2 * c0_dense + 0.3 * g1_dense + 0.5 * g2_dense}[target]
        exact_bonus = float(success)
        reward = 0.10 + 0.10 * topology + 0.55 * hierarchy + 0.25 * exact_bonus
    else:
        success = observed_level >= target_level
        hierarchy = {"G0": c0_dense, "G1": 0.4 * c0_dense + 0.6 * g1_dense, "G2": 0.2 * c0_dense + 0.3 * g1_dense + 0.5 * g2_dense}[target]
        reward = 0.10 + 0.10 * topology + 0.80 * hierarchy
    return {
        "reward": round(min(1.0, reward), 6),
        "success": success,
        "target": target,
        "mode": mode,
        "observed_grade": observed,
        "components": {
            "step_read": 1.0, "topology": topology,
            "G0_pass": c0, "G1_pass": g1, "G2_pass": g2,
            "G0_dense": c0_dense, "G1_dense": g1_dense, "G2_dense": g2_dense,
        },
        "edge_metrics": {k: edge.get(k) for k in ("max_c0_model_units", "max_g1_angle_deg", "max_g2_curvature_gap")},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate", type=Path)
    ap.add_argument("target", choices=["G0", "G1", "G2"])
    ap.add_argument("--mode", choices=["at_least", "exact"], default="at_least")
    args = ap.parse_args()
    print(json.dumps(score(args.candidate, args.target, args.mode), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
