# Submission Attack Log

Paper: 100 force_memory_transformers

## Attack 1: No real robot validation

Verdict: still valid. This prevents ICLR-main readiness.

Action: mark STRONG_REVISE, not ready.

## Attack 2: No external benchmark

Verdict: still valid. The local benchmark is useful but not enough.

Action: require external manipulation validation before submission.

## Attack 3: Baselines are weak

Verdict: partly addressed. v4.1 retains recurrent, ensemble uncertainty, conformal risk, online residual system-ID, robust threshold MPC, and oracle baselines.

Action: keep as STRONG_REVISE because baselines are stronger but still proxy systems.

## Attack 4: The mechanism may be unnecessary

Verdict: addressed locally. Removing force-event tokens, decay memory, tail-risk planning, diagnostic probes, reset gates, or force-specific recurrence reduces success or worsens safety.

Action: preserve ablation evidence.

## Attack 5: It wins by being unsafe

Verdict: not supported locally. Proposed force-limit violation and damage are lower than the strongest non-oracle baseline.

Action: include safety table and limitation.

## Attack 6: The oracle gap is too large

Verdict: valid. Oracle combined-stress success is `0.833`; proposed is `0.664`.

Action: report as a limitation and motivation for real model learning.

## Attack 7: Related work is still shallow

Verdict: valid. v4 improves the boundary but does not complete a full manual survey.

Action: require deeper related work before submission.

## Terminal Action

STRONG_REVISE. Continue only with external experiments; do not submit this version to ICLR main.
