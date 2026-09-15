# PartABC-derived seam audit

This directory contains **derived measurements only** from a convenience scan of 250 gated PartABC/NURBGen test models. Original STEP, NURBS JSON, captions, and renders are not redistributed.

- `seam_metrics.csv` / `seam_metrics.jsonl`: 3,691 analyzable two-face seam records from 249 models.
- `summary.json`: aggregate counts and provenance.

The records contain observed geometric continuity computed with Open CASCADE 7.9. They do not contain design-intent labels. Do not train on these records and report evaluation on the same NURBGen test models; doing so would contaminate the test set.

To build training data, acquire the upstream dataset under its own terms, run the analyzer on a disjoint training split, and manually annotate whether each target seam is intended to remain sharp or smooth.
