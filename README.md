# 100 Force Memory Transformers

Submission-hardening version: v5-expanded

Terminal decision: STRONG_REVISE for an ICLR-main-target project, not submission-ready.

Paper 100 was rebuilt into a larger CPU-only, RAM-light force-memory evidence audit on 2026-06-22. The v5 protocol tests whether risk-calibrated force memory improves contact-rich manipulation under hidden force state without hiding weaknesses behind pretty plots. All frozen local empirical gates pass, but the scope gate fails because there is still no real robot evidence, no accepted high-fidelity benchmark, no external benchmark, and no trained checkpoint.

Canonical PDF: `C:/Users/wangz/Downloads/100.pdf`

PDF status: 32 pages, SHA256 `ADDCA0435B496A5A8A0783ED7BBCD6B7141F65E4A1FB740DAB3A6D353AB12D40`

GitHub: `https://github.com/Jason-Wang313/100_force_memory_transformers`

## Key Evidence

- Design: 6 tasks x 8 latent force-memory regimes x 8 splits x 15 methods.
- Execution: 10 seeds, 6 episodes per seed/task/regime/split/method cell.
- Main rollout rows: 345,600.
- Ablation rollout rows: 115,200.
- Stress-sweep rollout rows: 288,000.
- Fixed-risk rollout rows: 138,240.
- Negative cases: 24.
- Main local method: `risk_calibrated_force_memory_transformer_v5`.
- Best non-oracle success reference: `proposed_force_memory_transformer_v4`.
- Hard success: v5 `0.73941` vs v4 `0.59054`.
- Force violation: v5 `0.20825` vs adaptive impedance `0.27023`.
- Damage: v5 `0.09010` vs adaptive impedance `0.14141`.
- Regret: v5 `0.07661` vs v4 `0.22067`.
- Utility: v5 `0.32439` vs particle-filter force-belief MPC `-0.05496`.
- Calibration: v5 ECE `0.01744`, within the frozen tolerance of the conformal-risk reference.
- Fixed-risk strict damage-budget coverage: v5 remains useful while satisfying the local damage gate.

## Gate Result

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

Terminal rationale: all frozen local empirical gates pass, so the paper remains worth continuing as STRONG_REVISE. It is not ICLR-main ready because the missing external-validation evidence is decisive.

## Reproduce Evidence

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
python scripts\validate_submission_artifacts.py
```

Outputs are written to `results/`, `figures/`, and `paper/`. The numbered PDF must exist only at `C:/Users/wangz/Downloads/100.pdf`; the protocol does not copy it to the visible Desktop.

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The manuscript uses boxed clickable citation links through `hyperref` settings in `paper/main.tex`.

## Honest Limitation

This is a strong local audit, not a submission-ready robotics result. Revival requires real robot or accepted high-fidelity benchmark validation, an external benchmark comparison, trained checkpoints, videos or rollout traces, and deeper manual related-work synthesis.
