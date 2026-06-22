# Hostile Reviewer Response

## Attack: This is still not real robotics evidence.

Response: Correct. The v5-expanded result is STRONG_REVISE, not submission-ready. The local benchmark is larger, safety-aware, calibrated, ablated, and stress-tested, but it does not replace hardware or accepted external benchmark validation.

## Attack: The baselines are still proxies.

Response: Correct. The baselines model distinct decision rules: observation-only transformer, force-history cloning, recurrent contact policy, diffusion force history, ensemble MPC, adaptive impedance MPC, HMM-MPC, particle-filter force-belief MPC, active tactile probe, conformal risk filtering, online residual system ID, robust threshold MPC, prior v4 force memory, and oracle. They are stronger than the earlier toy baselines but are still local proxy systems.

## Attack: Why does this survive at all?

Response: The local mechanism is decisive enough to keep. V5 improves hard success from `0.59054` to `0.73941` over the best non-oracle success reference, reduces force violation to `0.20825`, reduces damage to `0.09010`, improves utility to `0.32439`, clears calibration, survives ablations, and passes stress and fixed-risk gates.

## Attack: It may be tuned to the benchmark.

Response: This remains a valid risk. The plan froze the local gates before the terminal decision and reports the scope failure explicitly, but external benchmarks or hardware are required before any submission-ready claim.

## Attack: What would make it submit-worthy?

Response: A trained force-memory transformer, external benchmark validation, real or accepted high-fidelity rollouts, checkpoint/model-card release, video or rollout evidence, and deeper manual related work.
