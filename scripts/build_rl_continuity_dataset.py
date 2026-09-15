"""Build a small, exact-label curriculum dataset for G0/G1/G2 RL experiments.

This is a calibration/pilot dataset, not a paper-scale benchmark.  Each STEP has
two sewn Bezier surface patches and exactly one interior seam.  Its continuity
grade follows analytically from z(s)=A*s+B*s^2+C*s^3 on the right patch.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing
from OCC.Core.Geom import Geom_BezierSurface
from OCC.Core.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCC.Core.TColgp import TColgp_Array2OfPnt
from OCC.Core.gp import gp_Pnt

from analyze_step_continuity import analyze


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "pilot"


def polynomial_to_bezier(a: float, b: float, c: float) -> list[float]:
    """Power coefficients A,B,C -> cubic Bezier scalar control values."""
    return [0.0, a / 3.0, (b + 2.0 * a) / 3.0, a + b + c]


def patch(x: list[float], y_width: float, z: list[float]) -> Geom_BezierSurface:
    poles = TColgp_Array2OfPnt(1, 4, 1, 2)
    for i, (px, pz) in enumerate(zip(x, z), 1):
        poles.SetValue(i, 1, gp_Pnt(px, 0.0, pz))
        poles.SetValue(i, 2, gp_Pnt(px, y_width, pz))
    return Geom_BezierSurface(poles)


def make_shape(length: float, width: float, a: float, b: float, c: float):
    left = patch([0, length / 3, 2 * length / 3, length], width, [0.0] * 4)
    right = patch(
        [length, 4 * length / 3, 5 * length / 3, 2 * length],
        width,
        polynomial_to_bezier(a, b, c),
    )
    sewing = BRepBuilderAPI_Sewing(1e-9)
    sewing.Add(BRepBuilderAPI_MakeFace(left, 1e-10).Face())
    sewing.Add(BRepBuilderAPI_MakeFace(right, 1e-10).Face())
    sewing.Perform()
    return sewing.SewedShape()


def coefficients(grade: str, rng: random.Random, scale: float):
    sign = rng.choice([-1.0, 1.0])
    if grade == "G0":
        return sign * rng.uniform(.12, .40) * scale, rng.uniform(-.12, .12) * scale, rng.uniform(-.08, .08) * scale
    if grade == "G1":
        return 0.0, sign * rng.uniform(.12, .40) * scale, rng.uniform(-.08, .08) * scale
    if grade == "G2":
        return 0.0, 0.0, sign * rng.uniform(.18, .55) * scale
    raise ValueError(grade)


def split_for(index_in_grade: int) -> str:
    # 20 train + 5 validation + 5 test per grade.
    return "train" if index_in_grade < 20 else "validation" if index_in_grade < 25 else "test"


def main():
    geometry = OUT / "geometry"
    geometry.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20260916)
    manifest = []
    verification = []
    for grade in ("G0", "G1", "G2"):
        for i in range(30):
            sample_id = f"{grade.lower()}_{i:03d}"
            split = split_for(i)
            length = rng.uniform(.7, 2.0)
            width = rng.uniform(.6, 1.6)
            a, b, c = coefficients(grade, rng, length)
            step_path = geometry / f"{sample_id}.step"
            writer = STEPControl_Writer()
            writer.Transfer(make_shape(length, width, a, b, c), STEPControl_AsIs)
            writer.Write(str(step_path))
            prompt_en = (
                f"Create two adjacent cubic Bezier surface patches with one shared seam. "
                f"The seam must have exact {grade} geometric continuity. Preserve the "
                f"requested grade and output a sewn STEP B-Rep."
            )
            prompt_zh = f"生成两片相邻三次 Bezier 曲面，只有一条共享接缝；接缝须严格达到 {grade} 几何连续，并输出已缝合的 STEP B-Rep。"
            record = {
                "sample_id": sample_id,
                "split": split,
                "task_type": "two_patch_continuity_curriculum",
                "prompt_en": prompt_en,
                "prompt_zh": prompt_zh,
                "target_mode": "exact_grade",
                "target_grade": grade,
                "reference_step": f"geometry/{sample_id}.step",
                "shared_seam_count": 1,
                "surface_definition": {
                    "left": "S1(u,v)=(L*u, W*v, 0)",
                    "right": "S2(s,t)=(L*(1+s), W*t, A*s+B*s^2+C*s^3)",
                    "domain": "u,v,s,t in [0,1]",
                    "L": length, "W": width, "A": a, "B": b, "C": c,
                },
                "analytic_reason": {
                    "G0": "Both patches meet at s=0.",
                    "G1": "A=0 iff the cross-seam tangent plane agrees.",
                    "G2": "A=0 and B=0 iff first and second geometric behavior agrees at the seam.",
                },
                "provenance": "locally generated analytic ground truth",
                "seed": 20260916,
            }
            manifest.append(record)
            result = analyze(step_path)
            verification.append({
                "sample_id": sample_id,
                "expected_grade": grade,
                "observed_edge_counts": result["edge_counts"],
                "pass": result["edge_counts"][grade if grade == "G2" else grade + "_only"] == 1,
            })

    for name, rows in (("manifest.jsonl", manifest), ("verification.jsonl", verification)):
        (OUT / name).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")
    summary = {
        "total": len(manifest),
        "by_split": {s: sum(x["split"] == s for x in manifest) for s in ("train", "validation", "test")},
        "by_grade": {g: sum(x["target_grade"] == g for x in manifest) for g in ("G0", "G1", "G2")},
        "verification_pass": sum(x["pass"] for x in verification),
        "verification_fail": sum(not x["pass"] for x in verification),
        "scope": "pilot/calibration curriculum; not a paper-scale real-object benchmark",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
