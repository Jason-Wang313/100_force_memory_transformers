# Paper 100 Terminal Audit - 2026-06-15

Paper: `100_force_memory_transformers`

Final decision: STRONG_REVISE

ICLR main ready: no

## What Was Rechecked

- A paper-specific ICLR-main readiness execution plan was written before rerunning experiments.
- `src/run_experiment.py` compiled successfully.
- The full benchmark reran successfully with seven seeds and saved a continuation log.
- CSV, table, figure, summary, and manuscript artifacts were regenerated.
- The terminal decision in `results/summary.txt` was re-audited against the predeclared gates.

## Why It Stays Alive

The local mechanism reproduced:

- Proposed combined-stress success is 0.664 vs 0.504 for `online_residual_system_id`.
- Proposed force-limit violation is 0.231 vs 0.271 for the strongest baseline.
- Proposed damage is 0.161 vs 0.186 for the strongest baseline.
- Paired success gain against `online_residual_system_id` is 0.160 +/- 0.010 with 7/7 seed wins.
- Core removed-component ablations remain below full.
- At maximum hidden-force stress, proposed success is 0.662 vs 0.486 for `online_residual_system_id`.

## Why It Is Still Not Submission Ready

- No real robot validation.
- No accepted external manipulation benchmark.
- No trained transformer checkpoint or model card.
- No hardware or benchmark rollout videos.
- Stress regimes are local/synthetic-physical and not calibrated from hardware logs.
- Related work still needs a full manual synthesis.

## Artifact Policy

- Canonical PDF: `C:/Users/wangz/Downloads/100.pdf`.
- Visible Desktop PDF copy: prohibited.
- GitHub repository: https://github.com/Jason-Wang313/100_force_memory_transformers

## Terminal Action

Keep Paper 100 as `STRONG_REVISE`, not submission-ready. The next real work would be a trained force-memory transformer plus external or real-robot validation.
