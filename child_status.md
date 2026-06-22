# Child Status

Paper: 100 force_memory_transformers

Status: SUCCESS_STRONG_REVISE

Hardening version: v5-expanded

Last update: 2026-06-22

PDF: C:/Users/wangz/Downloads/100.pdf

PDF pages: 32

PDF SHA256: ADDCA0435B496A5A8A0783ED7BBCD6B7141F65E4A1FB740DAB3A6D353AB12D40

GitHub: https://github.com/Jason-Wang313/100_force_memory_transformers

Evidence: fresh 2026-06-22 v5 rerun of a larger local force-memory benchmark with 6 tasks, 8 latent regimes, 8 splits, 15 methods, 10 seeds, 345,600 main rollout rows, 115,200 ablation rows, 288,000 stress rows, 138,240 fixed-risk rows, and 24 negative cases. The proposed risk-calibrated force-memory transformer reaches hard success 0.73941, force violation 0.20825, damage 0.09010, ECE 0.01744, regret 0.07661, and utility 0.32439.

ICLR main ready: no. All frozen local empirical gates pass, but the scope gate fails because real robot validation, accepted high-fidelity benchmark validation, external benchmark comparison, and trained checkpoints are missing.
