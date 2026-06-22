# Reviewer Attacks

1. The benchmark is local and may encode assumptions that favor force memory.
2. The proposed method is a policy proxy, not a trained transformer checkpoint.
3. No real robot or accepted external simulator validates the mechanism.
4. Online residual system ID, adaptive impedance, particle-filter MPC, and conformal filtering are useful references, but trained learned baselines are still missing.
5. The oracle gap remains: `0.73941` success versus oracle `0.86667`.
6. The stress families are plausible but not calibrated from hardware logs.
7. Related work is broad and navigable, but still needs a full manual synthesis before submission.
8. The fixed-risk deployment result is local and should not be treated as a safety certificate.

Response after v5-expanded: keep the paper as STRONG_REVISE because all frozen local empirical gates pass, but do not submit it without external validation.
