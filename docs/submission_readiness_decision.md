# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v5-expanded rerun re-executed a larger paper-specific, multi-seed force-memory benchmark on 2026-06-22. It includes strong proxy baselines, oracle comparison, ablations, uncertainty intervals, calibration checks, stress tests, fixed-risk deployment tests, failure cases, generated figures, reproducible code, and a 32-page manuscript with boxed clickable citations. The local evidence supports the mechanism: risk-calibrated force memory improves hard success, safety, regret, utility, calibration, and fixed-risk coverage under hidden contact state.

## Reproduced Local Gates

- Success gate: v5 success `0.73941` vs `0.59054` for the best non-oracle success reference.
- Force-violation gate: v5 `0.20825` vs `0.27023` for the best safety reference.
- Damage gate: v5 `0.09010` vs `0.14141` for the best safety reference.
- Regret gate: v5 `0.07661` vs v4 `0.22067`.
- Utility gate: v5 `0.32439` vs particle-filter force-belief MPC `-0.05496`.
- Diagnostic gate: passed.
- Calibration gate: v5 ECE `0.01744`, clearing the frozen tolerance.
- Ablation gate: passed.
- Stress gate: passed.
- Fixed-risk gate: passed.

## Failed Submission-Ready Gate

- Scope gate: failed because there is no real robot validation, accepted high-fidelity benchmark validation, external benchmark comparison, or trained checkpoint.

Honest terminal action: keep as STRONG_REVISE. Do not submit to ICLR main until external empirical validation is added.
