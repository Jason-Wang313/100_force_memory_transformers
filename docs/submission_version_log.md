# Submission Version Log

## v1

Generated draft and repository scaffold.

## v2

Initial hardening pass.

## v3

ICLR-main gate archive. Decision: KILL_ARCHIVE because evidence was synthetic/template-only and no real baselines existed.

## v4

Paper-specific force-memory evidence rebuild. Added a deterministic NumPy benchmark, strong baselines, ablations, stress sweep, pairwise seed tests, figures, LaTeX tables, failure cases, rewritten docs, and a new manuscript. Decision changed to STRONG_REVISE because the local mechanism is supported, while submission readiness remains blocked by missing external robotics validation.

## v4.1

- Added a pre-execution ICLR-main submission-readiness plan for Paper 100.
- Reran `python src/run_experiment.py` on 2026-06-15 with thread caps and saved the continuation log.
- Reconfirmed CSV coverage for the smaller v4 protocol.
- Evidence outcome unchanged: proposed method beat `online_residual_system_id` on combined-stress success, improved force-limit violation and damage, won the paired seed gate, and survived core ablations.
- Terminal decision: STRONG_REVISE, still not ICLR-main ready without external robot or benchmark validation.

## v5-expanded

- Added and executed `docs/paper100_expanded_submission_plan_20260622.md`.
- Expanded the protocol to 6 tasks, 8 latent force-memory regimes, 8 splits, 15 methods, 10 seeds, and 6 episodes per cell.
- Generated 345,600 main rollout rows, 115,200 ablation rollout rows, 288,000 stress-sweep rows, 138,240 fixed-risk rows, and 24 negative cases.
- Added calibration, diagnostic, stress, ablation, fixed-risk, utility, regret, and scope gates.
- Rebuilt the manuscript generator and validator.
- Produced a 32-page manuscript with boxed clickable citations.
- Copied only `C:/Users/wangz/Downloads/100.pdf`; no visible Desktop copy is part of the protocol.
- Validated SHA256 `ADDCA0435B496A5A8A0783ED7BBCD6B7141F65E4A1FB740DAB3A6D353AB12D40`.
- Terminal decision: STRONG_REVISE. All frozen local empirical gates pass, but ICLR-main readiness remains no because the scope gate fails.
