# Claims

## Supported Local Claim

Persistent force-memory state improves closed-loop manipulation under hidden contact-force shifts in the local benchmark. The 2026-06-15 continuation rerun reproduced this local claim.

## Evidence

- Proposed combined-stress success: `0.664 +/- 0.006`.
- Strongest non-oracle baseline, `online_residual_system_id`: `0.504 +/- 0.008`.
- Proposed force-violation and damage are lower than the strongest baseline.
- Pairwise proposed-vs-strongest success difference: `0.160 +/- 0.010`, winning `7/7` seeds.
- Ablations removing force-event tokens, memory decay, tail-risk planning, diagnostic probing, reset gates, or force-specific memory reduce success.
- Maximum hidden-force stress remains positive for the proposed method: `0.662` success vs `0.486` for `online_residual_system_id`.

## Scope

This supports a local mechanism claim, not a deployment claim. The paper does not yet prove real-robot transfer, external benchmark superiority, or checkpoint-level performance.

## Unsupported Claims Explicitly Avoided

- No claim of ICLR-main readiness.
- No claim of state-of-the-art real robot performance.
- No claim that force memory replaces tactile sensors or online system identification.
- No claim that the benchmark is a substitute for hardware or accepted external simulators.
