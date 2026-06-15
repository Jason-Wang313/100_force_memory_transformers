# Paper 100 ICLR-Main Submission-Readiness Execution Plan

Timestamp: 2026-06-15

Paper: `100_force_memory_transformers`

Repository: `C:/Users/wangz/robotics_massive_pool_paper_factory/100_force_memory_transformers`

GitHub target: https://github.com/Jason-Wang313/100_force_memory_transformers

PDF target: `C:/Users/wangz/Downloads/100.pdf`

Desktop policy: do not copy a PDF or paper artifact to the visible Desktop.

## Goal

Recheck whether Paper 100 remains an evidence-backed `STRONG_REVISE` project under a fresh continuation rerun. The paper may stay alive only if the force-memory mechanism again beats strong non-oracle baselines on closed-loop success and safety, survives ablations, and keeps its limitations honest.

## Non-Negotiable Evidence Rule

This paper cannot be called ICLR-main ready from the current local evidence alone. The best possible continuation decision is `STRONG_REVISE`: promising enough to continue, still not ready for main-track submission without real robot or external benchmark validation. If the local evidence fails the mechanism gates, downgrade to `KILL_ARCHIVE`.

## Step 1: Baseline State Audit

1. Confirm the child repository is clean or identify unrelated local changes before editing.
2. Confirm `origin` points to the public GitHub repository.
3. Inspect current `README.md`, `child_status.md`, `paper/main.tex`, `docs/*decision*`, `docs/*gate*`, and `results/summary.txt`.
4. Record the current root-ledger state in `GLOBAL_POOL_STATUS.md`, `BATCH_STATUS.md`, `SUBMISSION_STATUS.md`, `MASTER_REPORT.md`, and `MASTER_SUBMISSION_REPORT.md`.
5. Confirm the current `C:/Users/wangz/Downloads/100.pdf` exists, and confirm no visible Desktop copy exists.

## Step 2: Fresh Experiment Rerun

Run the full paper-specific evidence pipeline without reducing rigor:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py *> C:\Users\wangz\robotics_massive_pool_paper_factory\logs\100_force_memory_transformers_continuation_rerun_20260615.log
```

Expected scope:

1. Five contact-rich manipulation tasks.
2. Seven latent force-memory regimes.
3. Five evaluation splits.
4. Nine methods.
5. Seven deterministic seeds.
6. Ablations, paired comparisons, stress sweep, failure cases, figures, LaTeX tables, and `results/summary.txt`.

## Step 3: CSV And Artifact Integrity Gates

Verify after rerun:

1. `results/metrics.csv` covers method/split aggregates.
2. `results/per_task_family_metrics.csv` covers method/split/task/family aggregates.
3. `results/seed_task_family_metrics.csv` covers seed/task/family/method/split groups.
4. `results/seed_split_metrics.csv` covers seed/method/split groups.
5. `results/pairwise_stats.csv` contains proposed-vs-baseline paired tests.
6. `results/ablation_metrics.csv`, `results/ablation_seed_metrics.csv`, and `results/ablation_task_family_seed_metrics.csv` cover full and removed-component variants.
7. `results/stress_sweep.csv` and `results/stress_sweep_seed_metrics.csv` cover hidden-force intensity.
8. `results/failure_cases.csv`, `figures/*.png`, and `results/*table.tex` are regenerated and referenced.

Any missing, stale, or internally inconsistent artifact blocks `STRONG_REVISE`.

## Step 4: Local Strong-Revise Gates

The proposed method, `proposed_force_memory_transformer`, must pass all local gates:

1. Success gate: beat the strongest non-oracle baseline on combined-stress task success by a practically meaningful margin.
2. Safety gate: avoid trading success for materially worse force-limit violation or damage.
3. Pairwise gate: show positive paired seed-level advantage over the strongest non-oracle baseline.
4. Diagnostic gate: improve latent-force accuracy without excessive false memory alarms.
5. Ablation gate: no removal of force-event tokens, decay memory, reset gates, diagnostic probes, or tail-risk planning may match or beat the full method on the claimed mechanism metrics.
6. Stress gate: hidden-force stress sweep must not reverse in favor of online residual system ID, ensemble uncertainty MPC, conformal risk filtering, recurrent contact policy, or robust force-threshold MPC.
7. Scope gate: the paper must explicitly say this is local executable evidence, not real robot validation, not a trained transformer checkpoint, and not an external benchmark result.

## Step 5: Claim And Paper Rewrite

If all local gates pass:

1. Keep terminal decision `STRONG_REVISE`.
2. State that the local mechanism is promising but not ICLR-main ready.
3. Preserve measured success, safety, pairwise, ablation, stress, and limitation claims.
4. Add a v4.1 continuation audit note to docs and the paper.

If any decisive local gate fails:

1. Downgrade to `KILL_ARCHIVE`.
2. Rewrite the paper as a negative evidence audit.
3. Explain exactly which baseline, ablation, safety, or stress gate failed.
4. Do not keep a positive submission label through prose polish.

## Step 6: PDF Build And Log Verification

Build the paper from `paper/` and copy only the numbered PDF to Downloads:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
Copy-Item -LiteralPath main.pdf -Destination C:\Users\wangz\Downloads\100.pdf -Force
```

Then verify:

1. LaTeX exits cleanly.
2. BibTeX has no real missing citation or undefined-reference warnings.
3. Only harmless rerunfilecheck metadata remains, if present.
4. `C:/Users/wangz/Downloads/100.pdf` exists with a fresh hash.
5. No `100.pdf` exists on the visible Desktop.

## Step 7: Repository And Root Ledger Update

After the decision and PDF are final:

1. Update `README.md`, `child_status.md`, `docs/claims.md`, `docs/final_audit.md`, `docs/iclr_main_gate.md`, `docs/submission_readiness_decision.md`, `docs/submission_version_log.md`, and stale review/attack docs.
2. Commit all Paper 100 changes in the child repository.
3. Push to `origin/main`.
4. Verify local and remote child commits match.
5. Verify the GitHub repository is public.
6. Update the root status files so Paper 100 is marked as continuation re-audited on 2026-06-15 with the final decision, PDF path, SHA, and public GitHub URL.

## Final Acceptance Checklist

Paper 100 is complete only when all of the following are true:

1. Fresh experiment log exists in the root `logs/` directory.
2. CSVs, figures, tables, summary, paper, and docs all reflect the same decision.
3. `C:/Users/wangz/Downloads/100.pdf` is the only final PDF copy requested by this workflow.
4. The child repo is clean after commit and push.
5. Local commit equals `origin/main`.
6. GitHub visibility is public.
7. Root ledgers are updated through Paper 100.
8. The final decision is evidence-backed `STRONG_REVISE` or evidence-backed `KILL_ARCHIVE`, with no cosmetic upgrade allowed.
