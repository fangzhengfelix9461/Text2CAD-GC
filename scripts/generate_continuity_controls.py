"""Generate three two-patch STEP controls with known G0/G1/G2 seam order.

S1(u,v)=(u,v,0), u,v in [0,1].  The second patch is
S2(s,t)=(1+s,t,z(s)).  z(s)=a*s, a*s^2, or a*s^3 yields,
respectively, positional-only, tangent-plane, or curvature continuity at s=0.
"""
from pathlib import Path

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing
from OCC.Core.Geom import Geom_BezierSurface
from OCC.Core.STEPControl import STEPControl_AsIs, STEPControl_Writer
from OCC.Core.StlAPI import StlAPI_Writer
from OCC.Core.TColgp import TColgp_Array2OfPnt
from OCC.Core.gp import gp_Pnt


def bezier_patch(x_controls, z_controls):
    poles = TColgp_Array2OfPnt(1, 4, 1, 2)
    for i, (x, z) in enumerate(zip(x_controls, z_controls), 1):
        poles.SetValue(i, 1, gp_Pnt(x, 0.0, z))
        poles.SetValue(i, 2, gp_Pnt(x, 1.0, z))
    return Geom_BezierSurface(poles)


def make_pair(power, amplitude=0.35):
    left = bezier_patch([0.0, 1/3, 2/3, 1.0], [0.0] * 4)
    if power == 1:      # a*s
        z = [0.0, amplitude/3, 2*amplitude/3, amplitude]
    elif power == 2:    # a*s^2
        z = [0.0, 0.0, amplitude/3, amplitude]
    elif power == 3:    # a*s^3
        z = [0.0, 0.0, 0.0, amplitude]
    else:
        raise ValueError(power)
    right = bezier_patch([1.0, 4/3, 5/3, 2.0], z)
    sewing = BRepBuilderAPI_Sewing(1e-9)
    sewing.Add(BRepBuilderAPI_MakeFace(left, 1e-10).Face())
    sewing.Add(BRepBuilderAPI_MakeFace(right, 1e-10).Face())
    sewing.Perform()
    return sewing.SewedShape()


def main():
    out = Path(__file__).resolve().parents[1] / "data" / "controls"
    out.mkdir(parents=True, exist_ok=True)
    for grade, power in [("G0", 1), ("G1", 2), ("G2", 3)]:
        shape = make_pair(power)
        step = out / f"two_patch_{grade}.step"
        writer = STEPControl_Writer()
        writer.Transfer(shape, STEPControl_AsIs)
        writer.Write(str(step))
        StlAPI_Writer().Write(shape, str(out / f"two_patch_{grade}.stl"))
    (out / "ground_truth.md").write_text(
        "# Synthetic continuity controls\n\n"
        "Two patches share the seam `x=1`. The left patch is `S1(u,v)=(u,v,0)`. "
        "The right patch is `S2(s,t)=(1+s,t,a s^k)`.\n\n"
        "- `k=1`: G0 only (positions meet; tangent planes differ).\n"
        "- `k=2`: G1 only (positions and tangent planes meet; normal curvature differs).\n"
        "- `k=3`: G2 (positions, tangent planes, and second-order curvature meet).\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
