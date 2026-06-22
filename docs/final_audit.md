# Final Audit

Paper 100 v5-expanded was rebuilt and rerun as a hostile-review force-memory evidence audit.

## Evidence Audit

The v5 benchmark evaluates hidden contact-force state across task, regime, split, seed, and method axes. The 2026-06-22 rerun produced 345,600 main rollout rows, 115,200 ablation rows, 288,000 stress rows, 138,240 fixed-risk rows, and 24 negative cases.

The proposed v5 method improves the local hard aggregate over the strongest non-oracle references: success `0.73941` vs `0.59054`, force violation `0.20825` vs `0.27023`, damage `0.09010` vs `0.14141`, regret `0.07661` vs `0.22067`, and utility `0.32439` vs `-0.05496`.

## Terminal Decision

STRONG_REVISE.

The result is strong enough to keep alive as an ICLR-main-target research project, but not ready for submission. The manuscript must not claim real robot readiness, external benchmark superiority, accepted high-fidelity simulator validation, or deployed transformer performance.

## Verification Targets

- Re-run: `python src\run_experiment.py`.
- Manuscript generator: `python scripts\generate_manuscript.py`.
- Artifact validator: `python scripts\validate_submission_artifacts.py`.
- Main table: `results/hard_aggregate_table.tex`.
- Ablation table: `results/ablation_table.tex`.
- Stress table: `results/stress_table.tex`.
- Fixed-risk table: `results/fixed_risk_table.tex`.
- Pairwise table: `results/pairwise_decision_table.tex`.
- PDF target: `C:/Users/wangz/Downloads/100.pdf`.
- PDF SHA256: `ADDCA0435B496A5A8A0783ED7BBCD6B7141F65E4A1FB740DAB3A6D353AB12D40`.

## Visual QA

The 32-page PDF was rendered and inspected after table compaction. The title page, result-table pages, citation-ledger page, and bibliography tail fit without visible clipping. The protocol keeps `100.pdf` in Downloads only and does not copy it to the visible Desktop.
