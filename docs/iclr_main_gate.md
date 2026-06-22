# ICLR Main Gate

Paper: 100 force_memory_transformers

Previous v3 decision: KILL_ARCHIVE

Previous v4.1 verdict: STRONG_REVISE

Current v5-expanded gate verdict: STRONG_REVISE

ICLR-main readiness: NO

## Gate Evidence

- Local benchmark: 6 tasks, 8 latent force-memory regimes, 8 splits, 15 methods.
- Seeds: 10.
- Episodes: 6 per seed/task/regime/split/method cell.
- Main rollout rows: 345,600.
- Ablation rollout rows: 115,200.
- Stress rollout rows: 288,000.
- Fixed-risk rollout rows: 138,240.
- Hard success margin over best non-oracle success reference: `0.73941 - 0.59054 = 0.14887`.
- Force-violation margin over best safety reference: `0.27023 - 0.20825 = 0.06198`.
- Damage margin over best safety reference: `0.14141 - 0.09010 = 0.05131`.
- Regret margin over v4: `0.22067 - 0.07661 = 0.14406`.
- Utility margin over best non-oracle utility reference: `0.32439 - (-0.05496) = 0.37935`.
- Calibration: v5 ECE `0.01744`.
- Fresh rerun status: reproduced on 2026-06-22.

## Passed Local Gates

- Success gate: passed.
- Force-violation gate: passed.
- Damage gate: passed.
- Regret gate: passed.
- Utility gate: passed.
- Diagnostic gate: passed.
- Calibration gate: passed.
- Ablation gate: passed.
- Stress gate: passed.
- Fixed-risk gate: passed.

## Failed Submission-Ready Gate

- Scope gate: failed.

## Scope Blockers

- No real robot validation.
- No accepted high-fidelity benchmark validation.
- No external benchmark validation.
- No trained checkpoint or model card.
- No hardware or benchmark rollout videos.
- Related work still needs manual tightening before a real submission.

Conclusion: viable STRONG_REVISE project, not ICLR-main ready.
