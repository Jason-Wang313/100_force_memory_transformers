# Reviewer Attacks

1. The benchmark is local and may encode assumptions that favor force memory.
2. The proposed method is a policy proxy, not a trained transformer checkpoint.
3. No real robot or accepted external simulator validates the mechanism.
4. Online residual system ID is strong, but learned latent-state baselines and tactile policies should be expanded.
5. The oracle gap remains large: `0.664` success versus oracle `0.833` under combined stress.
6. The stress families are plausible but not calibrated from hardware logs.
7. Related work still needs a full manual synthesis before submission.
