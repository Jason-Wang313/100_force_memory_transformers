# Paper 100 Rebuild Plan: Force Memory Transformers

Started: 2026-06-14 22:40:00 +0100

## Goal

Rebuild Paper 100 from a synthetic archive memo into an honest ICLR-main-target evidence package if, and only if, the evidence supports it. The falsifiable claim is that persistent force-memory state helps a robot policy keep hidden contact modes explicit after visual observations become ambiguous.

## Claimed Mechanism

The proposed method, `proposed_force_memory_transformer`, keeps a compact memory of contact impulses, force derivatives, release events, and recent high-load failures. It should help under partially observed manipulation where the current visual/geometric state is insufficient to infer latent force state.

## Benchmark To Build

Create a RAM-light but rigorous executable benchmark with vectorized NumPy simulation rather than heavyweight neural training. The benchmark will cover:

- 5 contact-rich manipulation tasks: peg insertion, drawer unlatching, valve turning, cable threading, and cap twisting.
- 7 latent force-memory regimes: stiction buildup, latch preload, backlash, viscoelastic relaxation, clamp slip, tool flex, and sensor dropout.
- 5 evaluation splits: nominal, hidden-force shift, embodiment shift, delayed-observation shift, and combined stress.
- 9 methods: observation-only transformer proxy, behavior cloning with force history, recurrent contact policy, ensemble uncertainty MPC, conformal risk filter, online residual system ID, robust force-threshold MPC, proposed force-memory transformer, and oracle latent-force planner.
- 7 random seeds with independent task/family episodes and uncertainty intervals.

## Evidence Requirements

The rebuild must produce:

- Per-method combined-stress success, damage, force-limit violation, regret, energy cost, latent-state accuracy, and memory false-alarm rate.
- Per-task/per-family breakdowns to expose where the mechanism helps or fails.
- Pairwise seed-level tests against the strongest non-oracle baseline.
- Stress sweep over hidden-force intensity.
- Ablations for force-event tokens, decay memory, tail-risk planning, diagnostic probing, and memory reset.
- Negative/failure cases with concrete conditions and lessons.
- Figures and LaTeX tables generated from result files.

## Terminal Gate

Mark `STRONG_REVISE` only if the proposed method:

- Beats the strongest non-oracle closed-loop baseline on combined-stress task success by a practically meaningful margin.
- Does not trade success for materially worse force violation or damage.
- Has a positive pairwise seed-level advantage over the strongest baseline.
- Survives core ablations: no ablation removing force memory, force events, or tail-risk planning may match or beat the full method.
- Has limitations framed honestly, including no real hardware validation.

Otherwise mark `KILL_ARCHIVE` with the strongest failure evidence and preserve the repo as a negative empirical audit.

## Execution Steps

1. Replace the template probability script with a paper-specific force-memory benchmark and deterministic output generation.
2. Generate metrics, seed metrics, per-task/per-family tables, pairwise tests, stress-sweep files, ablation files, failure cases, and figures.
3. Update README, status docs, claims, gate decision, reproducibility checklist, reviewer attacks, novelty docs, and final audit.
4. Rewrite `paper/main.tex` as either an evidence-backed submission-style report or a negative archive report based on the terminal gate.
5. Compile the PDF and copy only `100.pdf` to `C:/Users/wangz/Downloads/100.pdf`.
6. Verify finite CSVs, py_compile, LaTeX, PDF hash, no Desktop PDF, clean child repo, public GitHub push, and root report consistency.

## RAM Discipline

Use vectorized arrays, streamed CSV writing where useful, and aggregate tables rather than storing full trajectories. Do not reduce evidence quality: keep all seeds, methods, tasks, families, splits, stress levels, ablations, and failure cases.

## Execution Result

Completed: 2026-06-14 22:47:15 +0100

The benchmark was implemented and run. Terminal gate result: STRONG_REVISE. The proposed method beat the strongest non-oracle baseline, `online_residual_system_id`, on combined-stress success and safety, and no core ablation matched the full method. The paper remains not ICLR-main ready because no real robot or external benchmark validation is available.
