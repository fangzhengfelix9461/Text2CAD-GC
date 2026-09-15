# Analytic continuity controls

The three STEP files share the same two-patch construction and differ only in the cross-seam polynomial:

- `two_patch_G0.step`: slope jump, G0 only.
- `two_patch_G1.step`: matching tangent plane with a curvature jump, G1 only.
- `two_patch_G2.step`: matching tangent plane and second-order behavior, G2.

`continuity_analysis.json` contains the Open CASCADE verification. These controls are evaluator regression tests rather than a training corpus.
