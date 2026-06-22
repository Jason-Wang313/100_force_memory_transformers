# Reproducibility Checklist

- Code entry point: `src/run_experiment.py`.
- Manuscript generator: `scripts/generate_manuscript.py`.
- Artifact validator: `scripts/validate_submission_artifacts.py`.
- Dependencies: `numpy`, `matplotlib`, LaTeX, BibTeX, Poppler `pdfinfo` for validation.
- Deterministic base seed: `100_2026`.
- Seeds: `0..9`.
- Results directory: `results/`.
- Figures directory: `figures/`.
- Tables are generated automatically from CSV outputs.
- PDF can be rebuilt with `pdflatex`, `bibtex`, and two final `pdflatex` passes in `paper/`.
- Canonical numbered PDF: `C:/Users/wangz/Downloads/100.pdf`.
- Expected PDF pages: `32`.
- Expected PDF SHA256: `ADDCA0435B496A5A8A0783ED7BBCD6B7141F65E4A1FB740DAB3A6D353AB12D40`.
- The validator checks row counts, PDF location, page count, hash, absence of a Desktop PDF copy, and boxed citation settings.

## Known Limits

- The benchmark is local and synthetic-physical, not hardware.
- No trained model checkpoint is released.
- No external benchmark data is consumed.
- Full trajectory logs are streamed to CSV to keep RAM light; the protocol avoids loading the full experiment into memory at once.
