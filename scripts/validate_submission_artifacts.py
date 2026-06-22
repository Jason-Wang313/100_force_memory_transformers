import csv
import hashlib
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS_PDF = Path("C:/Users/wangz/Downloads/100.pdf")
DESKTOP_PDF = Path("C:/Users/wangz/Desktop/100.pdf")
MAIN_TEX = ROOT / "paper" / "main.tex"

EXPECTED_ROWS = {
    "results/dataset_summary.csv": 23040,
    "results/rollouts.csv": 345600,
    "results/main_group_metrics.csv": 57600,
    "results/main_seed_metrics.csv": 150,
    "results/metrics.csv": 120,
    "results/hard_aggregate_seed_metrics.csv": 150,
    "results/hard_aggregate_metrics.csv": 15,
    "results/pairwise_stats.csv": 14,
    "results/ablation_rollouts.csv": 115200,
    "results/ablation_seed_metrics.csv": 100,
    "results/ablation_metrics.csv": 10,
    "results/stress_sweep_raw.csv": 288000,
    "results/stress_sweep_seed_metrics.csv": 1000,
    "results/stress_sweep.csv": 100,
    "results/fixed_risk_raw.csv": 138240,
    "results/fixed_risk_seed_metrics.csv": 120,
    "results/fixed_risk_metrics.csv": 12,
    "results/fixed_risk_pairwise_stats.csv": 10,
    "results/failure_cases.csv": 24,
}


def count_csv_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return max(sum(1 for _ in csv.reader(handle)) - 1, 0)


def pdf_pages(path: Path) -> int:
    completed = subprocess.run(["pdfinfo", str(path)], check=True, capture_output=True, text=True)
    match = re.search(r"^Pages:\s+(\d+)", completed.stdout, re.MULTILINE)
    if not match:
        raise RuntimeError("could not parse pdfinfo page count")
    return int(match.group(1))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> None:
    if not DOWNLOADS_PDF.exists():
        raise FileNotFoundError(DOWNLOADS_PDF)
    if DESKTOP_PDF.exists():
        raise RuntimeError(f"visible Desktop PDF is not allowed: {DESKTOP_PDF}")
    repo_numbered = list(ROOT.rglob("100.pdf"))
    if repo_numbered:
        raise RuntimeError(f"numbered PDF should not be inside repo: {repo_numbered[0]}")
    pages = pdf_pages(DOWNLOADS_PDF)
    if pages < 25:
        raise RuntimeError(f"PDF is too short: {pages} pages")
    tex = MAIN_TEX.read_text(encoding="utf-8")
    for required in ["citebordercolor={0 1 0}", "linkbordercolor={1 0.55 0}", "pdfborder={0 0 1.2}"]:
        if required not in tex:
            raise RuntimeError(f"missing bright boxed citation/link setting: {required}")
    for relative, expected in EXPECTED_ROWS.items():
        observed = count_csv_rows(ROOT / relative)
        if observed != expected:
            raise RuntimeError(f"{relative}: expected {expected} rows, observed {observed}")
    print(f"validated Paper 100 artifacts: pages={pages}, sha256={sha256(DOWNLOADS_PDF)}")


if __name__ == "__main__":
    main()
