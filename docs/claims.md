# Claims

## Supported Local Claim

Risk-calibrated force memory improves closed-loop manipulation under hidden contact-force state in the local CPU-only benchmark. The 2026-06-22 v5-expanded rerun supports this mechanism claim under stronger stress, calibration, ablation, and fixed-risk tests.

## Evidence

- Hard success: `risk_calibrated_force_memory_transformer_v5` reaches `0.73941`, while the best non-oracle success reference, `proposed_force_memory_transformer_v4`, reaches `0.59054`.
- Force violation: v5 reaches `0.20825`, below the strongest safety reference `adaptive_impedance_mpc` at `0.27023`.
- Damage: v5 reaches `0.09010`, below `adaptive_impedance_mpc` at `0.14141`.
- Regret: v5 reaches `0.07661`, below v4 at `0.22067`.
- Utility: v5 reaches `0.32439`, above particle-filter force-belief MPC at `-0.05496`.
- Calibration: v5 ECE is `0.01744`, clearing the frozen conformal-risk tolerance.
- Ablations removing force-risk calibration, diagnostic probes, reset gates, decay memory, force-event tokens, or tail-risk planning reduce success, utility, or safety.
- Stress and fixed-risk tests pass the frozen local gates.

## Scope

This supports a local mechanism claim, not a deployment claim. The paper does not yet prove real-robot transfer, external benchmark superiority, accepted high-fidelity benchmark performance, or trained-checkpoint performance.

## Unsupported Claims Explicitly Avoided

- No claim of ICLR-main readiness.
- No claim of state-of-the-art real robot performance.
- No claim that force memory replaces tactile sensing or online system identification.
- No claim that the local benchmark substitutes for hardware or accepted external simulators.
- No claim that a trained deployable transformer checkpoint exists.
