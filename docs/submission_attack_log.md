# Submission Attack Log

Paper: 100 force_memory_transformers

## Attack 1: No real robot validation

Verdict: still valid. This prevents ICLR-main readiness.

Action: mark STRONG_REVISE, not ready.

## Attack 2: No external benchmark

Verdict: still valid. The local benchmark is useful but not enough.

Action: require external manipulation validation before submission.

## Attack 3: Baselines are weak

Verdict: improved locally, not eliminated. V5 includes fifteen methods: observation-only, force-history, recurrent, diffusion, ensemble MPC, adaptive impedance, HMM-MPC, particle-filter MPC, active probe, conformal filtering, online system ID, robust thresholding, prior v4 force memory, v5 force memory, and oracle.

Action: keep as STRONG_REVISE because baselines are stronger but still proxy systems.

## Attack 4: The mechanism may be unnecessary

Verdict: addressed locally. Removing force-risk calibration, diagnostic probes, memory reset, decay memory, force-event tokens, tail-risk planning, or the v5 controller reduces success, utility, or safety.

Action: preserve ablation evidence.

## Attack 5: It wins by being unsafe

Verdict: not supported locally. V5 force violation is `0.20825` and damage is `0.09010`, both better than the strongest non-oracle safety references.

Action: include hard aggregate, stress, and fixed-risk evidence.

## Attack 6: Calibration is cosmetic

Verdict: addressed locally. V5 ECE is `0.01744` and clears the frozen calibration tolerance relative to conformal filtering.

Action: keep calibration gate in the terminal audit.

## Attack 7: The oracle gap remains

Verdict: valid. Oracle success is `0.86667`, while v5 is `0.73941`.

Action: report as a limitation and motivation for trained-model and external validation.

## Attack 8: Related work is generated and still shallow

Verdict: valid. The citation scaffold is larger and navigable, but it still needs manual synthesis before a real submission.

Action: require deeper related work before submission.

## Terminal Action

STRONG_REVISE. Continue only with trained-model and external experiments; do not submit this version to ICLR main.
