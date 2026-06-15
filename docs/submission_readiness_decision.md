# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v4.1 continuation rerun re-executed the paper-specific, multi-seed force-memory benchmark on 2026-06-15. It includes strong baselines, ablations, uncertainty intervals, stress tests, failure cases, generated figures, and reproducible code. The local evidence still supports the mechanism: force memory improves combined-stress success and safety relative to the strongest non-oracle baseline, `online_residual_system_id`.

Reproduced local gates:

- Success gate: proposed success `0.664 +/- 0.006` vs `0.504 +/- 0.008` for `online_residual_system_id`.
- Safety gate: proposed force-limit violation `0.231` vs `0.271`, and damage `0.161` vs `0.186`.
- Pairwise gate: proposed beats `online_residual_system_id` by `0.160 +/- 0.010`, winning `7/7` seeds.
- Ablation gate: best removed-component ablation is `minus_tail_risk_planner` at `0.628`, below full at `0.660`.
- Stress gate: at maximum hidden-force stress, proposed success is `0.662` vs `0.486` for `online_residual_system_id`.

The paper is not submission-ready because the evidence remains local. It still lacks real-robot validation, an external benchmark comparison, trained transformer checkpoints, videos/rollouts, and a full manual related-work synthesis.

Honest terminal action: keep as STRONG_REVISE. Do not submit to ICLR main until external empirical validation is added.
