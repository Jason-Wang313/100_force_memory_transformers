# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

The v4 rebuild adds a paper-specific, multi-seed force-memory benchmark with strong baselines, ablations, uncertainty intervals, stress tests, failure cases, generated figures, and reproducible code. The local evidence supports the mechanism: force memory improves combined-stress success and safety relative to the strongest non-oracle baseline, `online_residual_system_id`.

The paper is not submission-ready because the evidence remains local. It still lacks real-robot validation, an external benchmark comparison, trained transformer checkpoints, videos/rollouts, and a full manual related-work synthesis.

Honest terminal action: keep as STRONG_REVISE. Do not submit to ICLR main until external empirical validation is added.
