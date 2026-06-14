# Reproducibility Checklist

- Code entry point: `src/run_experiment.py`.
- Dependencies: `numpy`, `matplotlib`.
- Deterministic base seed: `100_2026`.
- Seeds: `0..6`.
- Results directory: `results/`.
- Figures directory: `figures/`.
- Tables are generated automatically from CSV outputs.
- PDF can be rebuilt with two `pdflatex` passes in `paper/`.

## Known Limits

- The benchmark is local and synthetic-physical, not hardware.
- No trained model checkpoint is released.
- No external benchmark data is consumed.
- Full trajectory logs are not stored to keep RAM and disk usage light; aggregate per-group metrics are stored instead.
