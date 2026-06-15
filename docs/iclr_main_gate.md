# ICLR Main Gate

Paper: 100 force_memory_transformers

Previous v3 decision: KILL_ARCHIVE

Current v4.1 gate verdict: STRONG_REVISE

## Gate Evidence

- Local benchmark: 5 tasks, 7 latent force-memory regimes, 5 splits, 9 methods.
- Seeds: 7.
- Episodes: 84 per method/task/family/split/seed group.
- Strongest non-oracle baseline: `online_residual_system_id`.
- Proposed vs strongest baseline combined-stress success margin: `+0.160`.
- Proposed vs strongest baseline force-violation delta: `-0.039`.
- Proposed vs strongest baseline damage delta: `-0.024`.
- Full method vs best removed-component ablation margin: `+0.031`.
- Maximum hidden-force stress: proposed success `0.662` vs `0.486` for `online_residual_system_id`.
- Fresh rerun status: reproduced on 2026-06-15.

## Passed Local Gates

- Success gate: passed.
- Safety gate: passed.
- Pairwise seed gate: passed.
- Ablation gate: passed.

## Failed Submission-Ready Gates

- No real robot validation.
- No accepted external benchmark validation.
- No trained checkpoint or model card.
- No hardware/benchmark rollout videos.
- Related work is improved but still not a full manual survey.

Conclusion: viable STRONG_REVISE project, not ICLR-main ready.
