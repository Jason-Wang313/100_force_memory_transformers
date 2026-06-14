# Hostile Reviewer Response

## Attack: This is still not real robotics evidence.

Response: Correct. The v4 result is STRONG_REVISE, not submission-ready. The benchmark is stronger than the v3 template because it is mechanism-specific, multi-seed, safety-aware, and ablated, but it does not replace hardware or external benchmark validation.

## Attack: The baselines are still proxies.

Response: Also correct. The baselines model distinct decision rules: observation-only transformer, force-history cloning, recurrent contact policy, ensemble MPC, conformal risk filtering, online residual system ID, and robust threshold MPC. They are stronger than the v3 toy baselines, but they are not trained competing systems.

## Attack: Why does this survive at all?

Response: The local mechanism is decisive enough to keep. The proposed method beats the strongest non-oracle baseline by `0.160 +/- 0.010` success under combined stress, wins all seeds, improves force violation and damage, and survives ablations.

## Attack: What would make it submit-worthy?

Response: A trained force-memory transformer, external benchmark validation, real or high-fidelity rollouts, checkpoint/model-card release, video evidence, and deeper manual related work.
