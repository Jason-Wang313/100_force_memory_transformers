# Submission Readiness Audit v4.1

Paper: 100 `force_memory_transformers`

Audit date: 2026-06-15

Decision: STRONG_REVISE

ICLR main readiness: no

## Fresh Rerun

Command sequence:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py *> C:\Users\wangz\robotics_massive_pool_paper_factory\logs\100_force_memory_transformers_continuation_rerun_20260615.log
```

The rerun completed successfully and printed `terminal_decision=STRONG_REVISE`.

## Coverage

- `metrics.csv`: 45 rows.
- `per_task_family_metrics.csv`: 1,575 rows.
- `seed_task_family_metrics.csv`: 11,025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_family_seed_metrics.csv`: 1,715 rows.
- `stress_sweep.csv`: 54 rows.
- `stress_sweep_seed_metrics.csv`: 378 rows.
- `failure_cases.csv`: 8 rows.
- Seeds: 0 through 6.
- Tasks: `cable_threading`, `cap_twisting`, `drawer_unlatching`, `peg_insertion`, `valve_turning`.
- Latent force-memory regimes: `backlash`, `clamp_slip`, `latch_preload`, `sensor_dropout`, `stiction_buildup`, `tool_flex`, `viscoelastic_relaxation`.

## Reproduced Local Evidence

- `proposed_force_memory_transformer`: success 0.664 +/- 0.006, force violation 0.231, damage 0.161, latent accuracy 0.662, false alarm 0.114, regret 0.169.
- `online_residual_system_id`: success 0.504 +/- 0.008, force violation 0.271, damage 0.186, latent accuracy 0.443, false alarm 0.226, regret 0.329.
- Paired proposed-vs-strongest success gain: 0.160 +/- 0.010, wins 7/7 seeds.
- Best removed-component ablation: `minus_tail_risk_planner`, success 0.628 vs full 0.660.
- Maximum hidden-force stress: proposed success 0.662 vs `online_residual_system_id` 0.486.

## Gate Outcome

The paper remains a strong local mechanism audit and should stay `STRONG_REVISE`. It is still not ICLR-main ready because it lacks real robot validation, accepted external benchmark validation, trained transformer checkpoints, hardware/benchmark rollout videos, and a complete manual related-work synthesis.
