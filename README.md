# 100 Force Memory Transformers

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE for an ICLR-main-target project, not submission-ready.

Paper 100 was rebuilt from a template archive into a paper-specific force-memory benchmark and rerun on 2026-06-15. The continuation evidence supports the core local mechanism: persistent force-memory state improves closed-loop success under hidden contact-force shifts relative to observation-only, recurrent, uncertainty, conformal-risk, robust-threshold, and online residual system-ID baselines. The result is still not ICLR-main ready because it lacks real-robot runs, an external benchmark such as LIBERO/RLBench/Meta-World/real manipulation data, and a trained deployable transformer checkpoint.

## Key Evidence

- Benchmark design: 5 tasks x 7 latent force-memory regimes x 5 splits x 9 methods.
- Seeds: 7 independent seeds, 84 episodes per method/task/family/split/seed group.
- Strongest non-oracle baseline: `online_residual_system_id`.
- Combined stress: proposed success `0.664 +/- 0.006`; strongest baseline success `0.504 +/- 0.008`.
- Safety: proposed force-violation `0.231` and damage `0.161`, both below the strongest baseline.
- Ablation gate: full method success `0.660`; best removed-component ablation `minus_tail_risk_planner` success `0.628`.
- Max stress: proposed success `0.662`, while `online_residual_system_id` reaches `0.486`.

## Reproduce Evidence

```powershell
python src\run_experiment.py
```

Outputs are written to `results/` and `figures/`.

The continuation rerun log is stored at:

- `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/100_force_memory_transformers_continuation_rerun_20260615.log`

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/100.pdf`

## Honest Limitation

This is a strong local audit, not a submission-ready robotics result. Revival requires external robot or accepted high-fidelity benchmark validation, trained checkpoint release, hardware or benchmark videos, and a deeper manual related-work synthesis.
