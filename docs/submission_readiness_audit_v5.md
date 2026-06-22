# Submission Readiness Audit v5

Paper: 100 force_memory_transformers

Date: 2026-06-22

Terminal decision: STRONG_REVISE

ICLR-main ready: no

## Artifact Lock

- PDF: `C:/Users/wangz/Downloads/100.pdf`.
- Pages: `32`.
- SHA256: `ADDCA0435B496A5A8A0783ED7BBCD6B7141F65E4A1FB740DAB3A6D353AB12D40`.
- GitHub: `https://github.com/Jason-Wang313/100_force_memory_transformers`.
- Desktop copy: not allowed and not required.

## Protocol

- Tasks: 6.
- Latent force-memory regimes: 8.
- Splits: 8.
- Methods: 15.
- Seeds: 10.
- Episodes per cell: 6.
- Main rollout rows: 345,600.
- Main group metric rows: 57,600.
- Main seed metric rows: 150.
- Main metric rows: 120.
- Hard aggregate metric rows: 15.
- Pairwise rows: 14.
- Ablation rows: 115,200.
- Stress rows: 288,000.
- Fixed-risk rows: 138,240.
- Negative cases: 24.

## Frozen Gate Outcomes

- Success gate: pass.
- Force-violation gate: pass.
- Damage gate: pass.
- Regret gate: pass.
- Utility gate: pass.
- Diagnostic gate: pass.
- Calibration gate: pass.
- Ablation gate: pass.
- Stress gate: pass.
- Fixed-risk gate: pass.
- Scope gate: fail.

## Main Metrics

- V5 success: `0.73941`.
- V5 force violation: `0.20825`.
- V5 damage: `0.09010`.
- V5 latent accuracy: `0.72231`.
- V5 stale false positive: `0.02630`.
- V5 missed false negative: `0.12917`.
- V5 ECE: `0.01744`.
- V5 cost: `0.39964`.
- V5 regret: `0.07661`.
- V5 utility: `0.32439`.

## Terminal Rationale

All frozen local empirical gates pass. The correct terminal state is STRONG_REVISE, not KILL_ARCHIVE. The correct submission-readiness state is still no because no real robot, accepted high-fidelity benchmark, external benchmark, or trained checkpoint evidence exists.
