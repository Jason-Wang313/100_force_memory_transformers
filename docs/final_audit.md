# Final Audit

Paper 100 v4.1 was rebuilt and rerun as a force-memory evidence audit.

## Evidence Audit

The benchmark evaluates hidden contact-force state across task, family, split, seed, and method axes. The 2026-06-15 continuation rerun reproduced the positive local result: the proposed force-memory transformer proxy beats the strongest non-oracle baseline, `online_residual_system_id`, on combined-stress success (0.664 vs 0.504) while also reducing force-limit violations and damage.

## Terminal Decision

STRONG_REVISE.

The result is promising enough to keep alive as an ICLR-main-target research project, but not ready for submission. The manuscript must not claim real robot readiness, external benchmark superiority, or deployed transformer performance.

## Verification Targets

- Re-run: `python src\run_experiment.py`.
- Main table: `results/combined_stress_table.tex`.
- Ablation table: `results/ablation_table.tex`.
- Pairwise table: `results/pairwise_decision_table.tex`.
- PDF target: `C:/Users/wangz/Downloads/100.pdf`.
- Continuation log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/100_force_memory_transformers_continuation_rerun_20260615.log`.
