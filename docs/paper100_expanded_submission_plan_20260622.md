# Paper 100 Expanded Submission Plan

Paper: 100 `force_memory_transformers`

Date: 2026-06-22

GitHub target: `https://github.com/Jason-Wang313/100_force_memory_transformers`

Canonical PDF target: `C:/Users/wangz/Downloads/100.pdf`

Desktop policy: do not copy `100.pdf` or any paper PDF to the visible Desktop.

## Starting Point

The v4.1 continuation audit is locally positive but not submission-ready:

- The proposed force-memory transformer beats `online_residual_system_id` on combined-stress success, 0.664 vs 0.504.
- It also reduces force-limit violations and damage in the local surrogate benchmark.
- The PDF is only 7 pages, so it is below the expanded 25+ page standard.
- The evidence lacks real robot validation, accepted high-fidelity benchmark evidence, trained checkpoint release, hardware/benchmark videos, and a deep manual related-work synthesis.

The v5 rebuild must not optimize for pretty results. It must stress whether force-memory state remains useful against stronger contact-belief, adaptive-impedance, system-identification, particle-filter, tactile-history, conformal-safety, and MPC baselines.

## Thesis Under Test

Contact-rich robot policies should maintain an explicit latent force-memory state across action history, tactile/force events, contact mode changes, and delayed observations. A force-memory transformer should improve planning when current observations hide preload, stiction, backlash, relaxation, tool flex, clamp slip, sensor dropout, delayed force feedback, or embodiment-dependent force limits.

## Frozen v5 Experimental Design

- Tasks: 6 contact-rich manipulation tasks.
- Latent force-memory regimes: 8 families.
- Splits: 8 train/test/stress regimes.
- Methods: 15 total, spanning weak learned policies, recurrent force history, diffusion/transformer history, uncertainty MPC, conformal safety, robust force-threshold control, online residual system ID, adaptive impedance MPC, contact-mode HMM-MPC, particle-filter force-belief MPC, tactile/force probing, v4, v5, and oracle latent-force planning.
- Seeds: 10.
- Episodes: 6 per seed/task/regime/split/method cell.
- Main rollout rows expected: 345,600.
- Ablation rollout rows expected: at least 115,200.
- Stress sweep rows expected: at least 259,200.
- Fixed-risk rows expected: at least 138,240.

All rows must be streamed or accumulated in simple lists only; no large tensors, GPU, or high-RAM jobs are allowed.

## Metrics

- Task success.
- Force-limit violation.
- Damage or irreversible contact failure.
- Latent force-mode accuracy.
- Stale-memory false positives.
- Missed-memory false negatives.
- Calibration error.
- Regret to oracle latent-force planning.
- Robust utility after success, safety, damage, latency, probing, and abstention costs.
- Intervention/probe burden.
- Fixed-risk deployment coverage under force-violation and damage budgets.

## Strong Baselines

The v5 audit must include at least:

- `observation_only_transformer`.
- `force_history_behavior_cloning`.
- `recurrent_contact_policy`.
- `diffusion_policy_force_history`.
- `ensemble_uncertainty_mpc`.
- `conformal_risk_filter`.
- `robust_force_threshold_mpc`.
- `online_residual_system_id`.
- `adaptive_impedance_mpc`.
- `contact_mode_hmm_mpc`.
- `particle_filter_force_belief_mpc`.
- `active_tactile_probe_then_plan`.
- `proposed_force_memory_transformer_v4`.
- `risk_calibrated_force_memory_transformer_v5`.
- `oracle_latent_force_planner`.

If implementation constraints require fewer than these names, the final runner must preserve the full intended threat classes and document the substitution explicitly.

## Theory Additions

The manuscript must add:

- A formal latent force-memory POMDP-style setup.
- A memory observability proposition: when delayed or aliased force signals make current observations insufficient.
- A stale-memory failure theorem: persistent memory can harm success and safety under abrupt contact-mode changes unless reset/calibration conditions hold.
- A fixed-risk deployment lemma connecting force-violation budgets to abstention/probing coverage.
- A mechanism-necessity statement: full v5 is supported only if force-event tokens, decay, reset gates, calibration, diagnostic probes, and tail-risk planning each matter under the frozen ablation gates.
- A negative identifiability boundary against adaptive impedance, particle filtering, and online system ID.

## Frozen Submission Gates

The paper may remain `STRONG_REVISE` only if all local empirical gates pass and the only major blocker is missing external validation:

- Success gate: v5 beats the strongest non-oracle hard-split baseline using paired seed/task/regime statistics.
- Force-violation gate: v5 improves over the safest strong baseline without merely abstaining.
- Damage gate: v5 improves over the safest strong baseline.
- Regret gate: v5 lowers regret to oracle against online system ID, adaptive impedance MPC, particle-filter force-belief MPC, conformal risk filtering, and v4.
- Utility gate: v5 improves robust utility after cost, violation, damage, probing, latency, and abstention penalties.
- Diagnostic gate: v5 improves latent force-mode accuracy while keeping stale-memory false positives and missed-memory false negatives below frozen thresholds.
- Calibration gate: v5 has acceptable force-risk ECE and does not overtrust stale memory.
- Ablation gate: full v5 beats each stripped variant on the intended metric family.
- Stress gate: maximum-stress curves do not reverse in favor of adaptive impedance MPC, online system ID, particle-filter force-belief MPC, conformal risk filtering, or v4.
- Fixed-risk gate: v5 has useful deployment coverage under fixed force-violation and damage budgets.
- Scope gate: ICLR-main readiness remains `no` without real robot, accepted high-fidelity benchmark, external benchmark, or trained checkpoint evidence.

If any empirical gate fails, the terminal decision becomes `KILL_ARCHIVE`. If all empirical gates pass but scope remains local-only, the terminal decision may be `STRONG_REVISE`, but ICLR-main readiness remains `no`.

## Execution Steps

1. Preserve the current v4.1 audit as history.
2. Replace or extend `src/run_experiment.py` with the frozen v5 design.
3. Compile the runner before execution.
4. Run the full CPU-only/RAM-light experiment.
5. Verify all expected CSV counts and terminal gate logic.
6. Generate a 25+ page manuscript with honest terminal decision, full gate ledger, new theory, related-work pressure, limitations, and bright boxed clickable citations.
7. Build the PDF and copy only the final numbered PDF to `C:/Users/wangz/Downloads/100.pdf`.
8. Validate page count, hash, absence of Desktop copy, and absence of repo-local `100.pdf`.
9. Render representative PDF pages for visual QA.
10. Update README, child status, claims, final audit, ICLR gate, reproducibility, hostile reviewer, attack log, novelty, version log, and v5 audit docs.
11. Commit and push the child repo, verify public GitHub visibility, and update root ledgers.

## Completion Criteria

- Paper 100 has a frozen plan document, v5 runner, final docs, 25+ page PDF, and public GitHub push.
- `C:/Users/wangz/Downloads/100.pdf` exists with recorded SHA256.
- No `100.pdf` exists inside the child repo.
- No `C:/Users/wangz/Desktop/100.pdf` exists.
- Root ledgers mark Paper 100 under the expanded standard and advance the frontier to Paper 101.
