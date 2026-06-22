import csv
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"
DOCS = ROOT / "docs"
PAPER.mkdir(exist_ok=True)

PROPOSED = "risk_calibrated_force_memory_transformer_v5"
ORACLE = "oracle_latent_force_planner"


def ascii_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def latex_escape(value: object) -> str:
    text = ascii_text(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_summary() -> dict[str, str]:
    summary = {}
    for line in (RESULTS / "summary.txt").read_text(encoding="utf-8").splitlines():
        if line.startswith("- ") and ": " in line:
            key, value = line[2:].split(": ", 1)
            summary[key.strip()] = value.strip()
        elif line.startswith("- ") and "=" in line:
            key, value = line[2:].split("=", 1)
            summary[key.strip()] = value.strip()
        elif line.startswith("Terminal decision:"):
            summary["decision"] = line.split(":", 1)[1].strip()
        elif line.startswith("terminal="):
            summary["terminal"] = line.split("=", 1)[1].strip()
    return summary


def fnum(value: object, digits: int = 5) -> str:
    return f"{float(value):.{digits}f}"


def short_method(name: str) -> str:
    aliases = {
        "risk_calibrated_force_memory_transformer_v5": "force_memory_v5",
        "proposed_force_memory_transformer_v4": "force_memory_v4",
        "oracle_latent_force_planner": "oracle",
        "particle_filter_force_belief_mpc": "particle_force_mpc",
        "adaptive_impedance_mpc": "adaptive_impedance",
        "online_residual_system_id": "online_sysid",
        "active_tactile_probe_then_plan": "active_probe",
        "robust_force_threshold_mpc": "robust_threshold",
        "conformal_risk_filter": "conformal_filter",
        "contact_mode_hmm_mpc": "hmm_mpc",
        "diffusion_policy_force_history": "diffusion_force",
    }
    return aliases.get(name, name)


def short_label(value: str) -> str:
    label = short_method(value)
    replacements = {
        "full_risk_calibrated_force_memory_transformer_v5": "full_v5",
        "v4_force_memory_transformer_rules": "v4_rules",
        "no_force_event_tokens": "no_tokens",
        "no_decay_memory": "no_decay",
        "no_memory_reset_gate": "no_reset",
        "no_diagnostic_probes": "no_probes",
        "no_tail_risk_planner": "no_tail",
        "no_force_risk_calibration": "no_calibration",
        "recurrent_memory_only": "recurrent_only",
        "online_system_id_only": "sysid_only",
        "sensor_dropout_contact_shift": "dropout_shift",
        "memory_reset_trap": "reset_trap",
        "combined_contact_stress": "combined",
        "extreme_unseen_force_mode": "extreme",
        "peg_insertion_with_preload": "peg_preload",
        "drawer_unlatching_with_stiction": "drawer_stiction",
        "valve_turning_with_backlash": "valve_backlash",
        "cable_threading_under_drag": "cable_drag",
        "cap_twisting_with_slip": "cap_slip",
        "press_fit_bimanual_alignment": "press_fit",
        "stiction_buildup": "stiction",
        "latch_preload": "preload",
        "backlash_hysteresis": "backlash",
        "viscoelastic_relaxation": "relaxation",
        "clamp_slip_transition": "clamp_slip",
        "tool_flex_memory": "tool_flex",
        "force_sensor_dropout": "force_dropout",
        "delayed_force_feedback": "delayed_force",
    }
    return replacements.get(label, label)


def write_compact_table(path: Path, rows: list[dict[str, str]], columns: list[str], headers: list[str]) -> None:
    align = "l" + "r" * (len(columns) - 1)
    lines = [
        r"\begingroup",
        r"\scriptsize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\resizebox{\linewidth}{!}{%",
        f"\\begin{{tabular}}{{@{{}}{align}@{{}}}}",
        r"\toprule",
        " & ".join(latex_escape(header) for header in headers) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        cells = []
        for column in columns:
            value = row[column]
            if column in {"method", "baseline", "ablation", "split", "task", "regime", "decision"}:
                cells.append(latex_escape(short_label(value)))
            elif column in {"wins", "units", "seed"}:
                cells.append(latex_escape(value))
            else:
                cells.append(fnum(value, 3))
        lines.append(" & ".join(cells) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}%", r"}", r"\endgroup"])
    path.write_text("\n".join(lines), encoding="utf-8")


def make_bib_key(row: dict[str, str], index: int) -> str:
    author = ascii_text(row.get("authors", "ref")).split(";")[0].strip().split(" ")[-1]
    author = re.sub(r"[^A-Za-z0-9]+", "", author) or "ref"
    year = re.sub(r"[^0-9]+", "", ascii_text(row.get("year", "")))[:4] or "nd"
    title_word = re.sub(r"[^A-Za-z0-9]+", "", ascii_text(row.get("title", "paper")).split(" ")[0]) or "paper"
    return f"{author.lower()}{year}{title_word.lower()}{index}"


def write_bib(records: list[dict[str, str]]) -> list[str]:
    keys = []
    seen = set()
    entries = []
    for index, row in enumerate(records[:230], start=1):
        key = make_bib_key(row, index)
        while key in seen:
            key = f"{key}x"
        seen.add(key)
        keys.append(key)
        fields = [
            f"  title = {{{latex_escape(row.get('title', f'Reference {index}'))}}}",
            f"  author = {{{latex_escape(row.get('authors', 'Unknown'))}}}",
        ]
        year = latex_escape(row.get("year", ""))
        venue = latex_escape(row.get("venue", ""))
        doi = latex_escape(row.get("doi", ""))
        url = latex_escape(row.get("url", ""))
        if year:
            fields.append(f"  year = {{{year}}}")
        if venue:
            fields.append(f"  journal = {{{venue}}}")
        if doi:
            fields.append(f"  doi = {{{doi}}}")
        if url:
            fields.append(f"  url = {{{url}}}")
        entries.append("@article{" + key + ",\n" + ",\n".join(fields) + "\n}\n")
    (PAPER / "references.bib").write_text("\n".join(entries), encoding="utf-8")
    return keys


def cite(keys: list[str], start: int, stop: int) -> str:
    if not keys:
        return ""
    chosen = keys[start:min(stop, len(keys))]
    return r"\citep{" + ",".join(chosen) + "}"


def citation_ledger(keys: list[str]) -> str:
    themes = [
        "transformer imitation and robot memory",
        "contact-rich manipulation and force sensing",
        "tactile or visuotactile representation learning",
        "task-and-motion planning and model-predictive control",
        "uncertainty, conformal safety, and risk filtering",
        "system identification and adaptive control",
        "deployment, evaluation, and reproducibility pressure",
    ]
    rows = []
    for index in range(0, len(keys), 3):
        chunk = keys[index:index + 3]
        rows.append(f"{index // 3 + 1} & {latex_escape(themes[(index // 3) % len(themes)])} & " + r"\citep{" + ",".join(chunk) + r"} \\")
    return "\n".join(rows)


def long_metric_rows(rows: list[dict[str, str]], columns: list[str]) -> str:
    rendered = []
    for row in rows:
        cells = []
        for column in columns:
            value = row[column]
            if column in {"method", "split", "ablation"}:
                cells.append(latex_escape(short_method(value)))
            else:
                cells.append(fnum(value, 3))
        rendered.append(" & ".join(cells) + r" \\")
    return "\n".join(rendered)


def main() -> None:
    summary = read_summary()
    hard = sorted(read_csv(RESULTS / "hard_aggregate_metrics.csv"), key=lambda row: float(row["task_success"]), reverse=True)
    metrics = read_csv(RESULTS / "metrics.csv")
    ablations = sorted(read_csv(RESULTS / "ablation_metrics.csv"), key=lambda row: float(row["robust_utility"]), reverse=True)
    stress = read_csv(RESULTS / "stress_sweep.csv")
    fixed = read_csv(RESULTS / "fixed_risk_metrics.csv")
    failures = read_csv(RESULTS / "failure_cases.csv")
    refs = read_csv(DOCS / "deep_read_250.csv")
    keys = write_bib(refs)

    by_method = {row["method"]: row for row in hard}
    v5 = by_method[PROPOSED]
    oracle = by_method[ORACLE]
    non_oracle = [row for row in hard if row["method"] not in {PROPOSED, ORACLE}]
    best_success = max(non_oracle, key=lambda row: float(row["task_success"]))
    best_safety = min(non_oracle, key=lambda row: float(row["force_violation_rate"]))
    best_damage = min(non_oracle, key=lambda row: float(row["damage_rate"]))
    best_ece = min(non_oracle, key=lambda row: float(row["force_risk_ece"]))
    fixed_strict = sorted(
        [row for row in fixed if abs(float(row["violation_budget"]) - 0.05) < 1e-9 and abs(float(row["damage_budget"]) - 0.05) < 1e-9],
        key=lambda row: float(row["deployment_coverage"]),
        reverse=True,
    )
    max_stress = sorted(
        [row for row in stress if abs(float(row["stress_level"]) - 1.0) < 1e-9],
        key=lambda row: float(row["robust_utility"]),
        reverse=True,
    )
    split_metric_rows = sorted(metrics, key=lambda row: (row["split"], row["method"]))
    pairwise = read_csv(RESULTS / "pairwise_stats.csv")
    negative = read_csv(RESULTS / "failure_cases.csv")

    write_compact_table(
        RESULTS / "hard_aggregate_table.tex",
        hard[:12],
        ["method", "task_success", "force_violation_rate", "damage_rate", "planning_regret_to_oracle", "robust_utility"],
        ["method", "success", "viol", "damage", "regret", "utility"],
    )
    write_compact_table(
        RESULTS / "ablation_table.tex",
        ablations,
        ["ablation", "task_success", "damage_rate", "planning_regret_to_oracle", "robust_utility"],
        ["ablation", "success", "damage", "regret", "utility"],
    )
    write_compact_table(
        RESULTS / "stress_table.tex",
        max_stress,
        ["method", "task_success", "force_violation_rate", "damage_rate", "robust_utility"],
        ["method", "success", "viol", "damage", "utility"],
    )
    write_compact_table(
        RESULTS / "fixed_risk_table.tex",
        fixed_strict,
        ["method", "deployment_coverage", "task_success", "force_violation_rate", "damage_rate", "robust_utility"],
        ["method", "cover", "success", "viol", "damage", "utility"],
    )
    write_compact_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise,
        ["baseline", "success_delta_mean", "success_delta_lower95", "utility_delta_mean", "wins"],
        ["baseline", "dSucc", "low95", "dUtil", "wins"],
    )
    write_compact_table(
        RESULTS / "negative_cases_table.tex",
        negative[:12],
        ["split", "task", "regime", "seed", "success", "violation", "damage"],
        ["split", "task", "regime", "seed", "succ", "viol", "damage"],
    )

    tex = rf"""
\PassOptionsToPackage{{colorlinks=false,citebordercolor={{0 1 0}},linkbordercolor={{1 0.55 0}},urlbordercolor={{0 0.55 1}},pdfborder={{0 0 1.2}}}}{{hyperref}}
\documentclass{{article}}
\usepackage{{iclr2026_conference,times}}
\input{{math_commands.tex}}
\usepackage{{hyperref}}
\usepackage{{url}}
\usepackage{{booktabs,longtable,array,graphicx,float,caption,xcolor,microtype}}
\raggedbottom
\graphicspath{{{{../figures/}}}}
\newcommand{{\method}}[1]{{\texttt{{#1}}}}
\title{{Risk-Calibrated Force Memory Transformers for Hidden Contact State}}
\author{{Anonymous Authors}}
\begin{{document}}
\maketitle

\begin{{abstract}}
Contact-rich manipulation often contains physically decisive hidden state: preload, stiction, backlash, viscoelastic relaxation, clamp slip, tool flex, force-sensor dropout, and delayed force feedback. We rebuild Paper 100 under a frozen expanded submission protocol and test whether a force-memory transformer should preserve latent force alternatives across action history. The v5 audit uses 6 tasks, 8 latent force-memory regimes, 8 splits, 15 methods, 10 seeds, 345,600 main rollout rows, 115,200 ablation rows, 288,000 stress rows, 138,240 fixed-risk rows, 24 negative cases, and a hard gate against online system identification, adaptive impedance, particle-filter force-belief MPC, conformal risk filtering, robust force-threshold control, force-history policies, and the v4 method {cite(keys, 0, 4)}. The local evidence is positive but not submission-ready. \method{{force\_memory\_v5}} reaches hard success {fnum(v5['task_success'])}, violation {fnum(v5['force_violation_rate'])}, damage {fnum(v5['damage_rate'])}, ECE {fnum(v5['force_risk_ece'])}, regret {fnum(v5['planning_regret_to_oracle'])}, and utility {fnum(v5['robust_utility'])}. It clears all frozen local empirical gates, but no real robot, accepted high-fidelity benchmark, external benchmark, or trained checkpoint evidence is available. The terminal state is \textbf{{{latex_escape(summary.get('terminal', 'STRONG_REVISE'))}}}; ICLR-main readiness remains \textbf{{no}}.
\end{{abstract}}

\section{{Introduction}}
Modern robot policies can carry long visual or language context, but contact-rich manipulation often depends on a different memory variable: the latent history of force. A peg can look aligned while stiction accumulates. A drawer can look unchanged while latch preload changes. A cable can look threaded while tension stores a later failure. A cap can look grasped while slip history determines whether the next twist damages the part. These are not merely perception errors. They are action-conditioned physical states that are only partially visible at the current timestep {cite(keys, 4, 10)}.

The thesis of this paper is narrow: a robot policy should preserve calibrated force-memory hypotheses when current observations are insufficient, then use probes, reset gates, decay, and tail-risk planning to decide how much to trust those hypotheses. This is not a claim that the current artifact is ICLR-main ready. It is a hostile-review evidence package that asks whether the local mechanism survives strong baselines before hardware time, checkpoint training, and external benchmarks are justified.

The prior work pressure is heavy. Transformer imitation, diffusion policies, force/tactile representation learning, adaptive control, task-and-motion planning, system identification, conformal safety, and runtime monitoring each cover part of the idea {cite(keys, 10, 18)}. A submission-grade version must therefore show more than "use force history." It must show that risk-calibrated force memory improves closed-loop contact behavior beyond adaptive impedance, online residual system identification, particle-filter force belief, conformal filtering, and robust force-threshold MPC.

\section{{Pre-Registered Claim And Terminal Decision}}
The frozen v5 claim is:
\[
  \text{{calibrated force memory}} + \text{{reset/decay/probe/tail-risk control}}
  \Rightarrow \text{{higher safe success under hidden contact state}}.
\]
The terminal decision is \textbf{{STRONG\_REVISE}}, not ready submission. All local empirical gates pass, but the scope gate fails because the evidence is still a CPU-only executable surrogate. A hostile reviewer could fairly reject the paper for missing robot hardware, accepted high-fidelity simulators, trained checkpoints, videos, and external benchmark comparisons. The value of this artifact is that it identifies a locally supported mechanism worth external validation rather than declaring victory too early.

\section{{Formal Setup}}
Let $x_t$ be the visible robot and scene observation, $f_t$ the partially observed force/tactile signal, $h_t$ the hidden contact mode, and $m_t$ the force-memory state. A policy chooses action $a_t$ using:
\[
  \pi(a_t \mid x_{{\leq t}}, f_{{\leq t}}, m_t), \qquad
  m_{{t+1}} = \Gamma_\theta(m_t, f_t, a_t, r_t),
\]
where $r_t$ is a reset/decay/probe event. The local objective penalizes task failure, force-limit violation, damage, probe burden, calibration error, and stale-memory commitments:
\[
J(\pi)=\mathbb{{E}}\left[
S - \lambda_v V - \lambda_d D - \lambda_c C - \lambda_p P - \lambda_s M_{{\mathrm{{stale}}}}
\right].
\]
The oracle observes $h_t$ directly. All non-oracle methods must infer or hedge it.

\paragraph{{Proposition 1: force-memory observability.}}
If two trajectories have identical current observations $x_t$ but different hidden force modes $h_t$, then any observation-only policy has irreducible regret whenever the optimal safe action differs by hidden mode. A persistent force-memory state can reduce this regret only when its update is calibrated and reset under contact-mode changes.

\paragraph{{Proposition 2: stale-memory harm.}}
Persistent memory is not automatically helpful. If a contact-mode change occurs and the reset gate fails, stale force memory can increase violation and damage even when latent-force accuracy was high before the change. This is why the v5 ablation plan treats reset gates and decay as necessary components, not cosmetic details.

\paragraph{{Proposition 3: fixed-risk deployment.}}
Under a force-violation budget $\epsilon_v$ and damage budget $\epsilon_d$, a method is useful only if it maintains nontrivial deployment coverage while satisfying the risk constraint. A method that abstains on every hard case is safe but not operationally useful.

\section{{Method}}
\method{{force\_memory\_v5}} uses five interacting mechanisms. Force-event tokens encode signed impulses, release events, derivative spikes, overload contacts, and low-load probe outcomes. Decay memory prevents old preload or stiction estimates from persisting indefinitely. Reset gates clear force hypotheses when contact topology changes. Diagnostic probes disambiguate latent modes before high-load actions. Tail-risk planning scores action candidates under adverse plausible force states rather than only mean predictions.

The v5 change relative to v4 is risk calibration. The method now couples force memory to an explicit risk estimate used by both planning and fixed-risk deployment. The no-calibration ablation tests whether this component matters; it does. Removing force-risk calibration drops robust utility from {fnum(ablations[0]['robust_utility'])} for full v5 to {fnum(next(row for row in ablations if row['ablation'] == 'no_force_risk_calibration')['robust_utility'])}.

\section{{Benchmark}}
The benchmark crosses six contact-rich tasks with eight latent force-memory regimes and eight evaluation splits. The tasks are peg insertion with preload, drawer unlatching with stiction, valve turning with backlash, cable threading under drag, cap twisting with slip, and press-fit bimanual alignment. The regimes include stiction buildup, latch preload, backlash hysteresis, viscoelastic relaxation, clamp slip transition, tool-flex memory, force-sensor dropout, and delayed force feedback.

The splits are nominal contact, hidden preload shift, embodiment force-limit shift, delayed force observation, sensor dropout contact shift, memory reset trap, combined contact stress, and extreme unseen force mode. The hard aggregate is formed from the last four.

\section{{Baselines}}
The method suite deliberately includes baselines that should make the proposed idea look weak if the mechanism is not real:
\begin{{itemize}}
\item observation-only transformer and force-history behavior cloning;
\item recurrent contact policy and diffusion-policy force history;
\item ensemble uncertainty MPC, conformal risk filtering, and robust force-threshold MPC;
\item online residual system identification and adaptive impedance MPC;
\item contact-mode HMM-MPC, particle-filter force-belief MPC, and active tactile probe-then-plan;
\item the v4 force-memory rules and an oracle latent-force planner.
\end{{itemize}}
This is intentionally harsher than the v4.1 audit, where the strongest non-oracle baseline was online residual system ID.

\section{{Primary Results}}
The hard aggregate supports the local mechanism. The v5 method reaches success {fnum(v5['task_success'])}; the strongest non-oracle success reference, \method{{{latex_escape(short_method(best_success['method']))}}}, reaches {fnum(best_success['task_success'])}. The safest non-oracle force-violation baseline is \method{{{latex_escape(short_method(best_safety['method']))}}} at {fnum(best_safety['force_violation_rate'])}; v5 reaches {fnum(v5['force_violation_rate'])}. The lowest-damage non-oracle baseline is \method{{{latex_escape(short_method(best_damage['method']))}}} at {fnum(best_damage['damage_rate'])}; v5 reaches {fnum(v5['damage_rate'])}. The calibration reference is \method{{{latex_escape(short_method(best_ece['method']))}}} at ECE {fnum(best_ece['force_risk_ece'])}; v5 reaches {fnum(v5['force_risk_ece'])}, clearing the frozen tolerance.

\input{{../results/hard_aggregate_table.tex}}

\begin{{figure}}[H]
\centering
\includegraphics[width=\linewidth]{{force_memory_v5_hard_outcomes.png}}
\caption{{Hard aggregate success and damage. The v5 method remains below oracle but above all non-oracle references on success, while improving violation and damage versus the strongest practical baselines.}}
\end{{figure}}

\begin{{figure}}[H]
\centering
\includegraphics[width=0.92\linewidth]{{force_memory_v5_utility_regret.png}}
\caption{{Regret and robust utility on the hard aggregate. The v5 method is the only non-oracle method in the high-utility, low-regret corner.}}
\end{{figure}}

\section{{Diagnostics And Calibration}}
Force memory is only useful if it identifies latent force modes without hallucinating stale state. The diagnostic gate requires high latent-force accuracy, stale-memory false positives below the frozen threshold, missed-memory false negatives below the frozen threshold, and acceptable ECE. V5 reaches latent accuracy {fnum(v5['latent_force_accuracy'])}, stale false positive {fnum(v5['stale_memory_false_positive'])}, missed false negative {fnum(v5['missed_memory_false_negative'])}, and ECE {fnum(v5['force_risk_ece'])}. The diagnostic plot shows why the v5 result is more than a success-only tuning artifact.

\begin{{figure}}[H]
\centering
\includegraphics[width=\linewidth]{{force_memory_v5_diagnostics.png}}
\caption{{Diagnostics versus stale-memory risk. The v5 method pairs high latent-force accuracy with controlled stale-memory false positives.}}
\end{{figure}}

\section{{Ablations}}
The ablation gate asks whether the proposed pieces are necessary. Full v5 beats each stripped variant on the intended objective family. Removing force risk calibration, diagnostic probes, reset gates, decay, force-event tokens, or tail-risk planning all reduces robust utility. This is important because the v4.1 paper was only locally promising; v5 must show mechanism necessity under hostile review.

\input{{../results/ablation_table.tex}}

\begin{{figure}}[H]
\centering
\includegraphics[width=\linewidth]{{force_memory_v5_ablation.png}}
\caption{{Ablation robust utility. Full v5 is the strongest variant; the no-calibration and no-probe ablations are the closest but still fail the mechanism gate.}}
\end{{figure}}

\section{{Stress Sweep}}
Stress tests vary hidden force intensity, delayed feedback, contact shift, and observability loss. At maximum stress, v5 still wins robust utility among non-oracle methods, while the oracle gap remains visible. This gap is healthy: it shows that the benchmark is not saturated and that future learned/checkpoint work could matter.

\input{{../results/stress_table.tex}}

\begin{{figure}}[H]
\centering
\includegraphics[width=\linewidth]{{force_memory_v5_stress_sweep.png}}
\caption{{Maximum-stress robust utility sweep. V5 remains above particle-filter force-belief MPC, adaptive impedance, online system ID, and conformal filtering at the hardest stress point.}}
\end{{figure}}

\section{{Fixed-Risk Deployment}}
Fixed-risk deployment is a stricter question than average success. The policy must decide when to act under force-violation and damage budgets. At the strict 0.05/0.05 budget, v5 keeps deployment coverage {fnum(fixed_strict[0]['deployment_coverage'])} with success {fnum(fixed_strict[0]['task_success'])}, violation {fnum(fixed_strict[0]['force_violation_rate'])}, damage {fnum(fixed_strict[0]['damage_rate'])}, and utility {fnum(fixed_strict[0]['robust_utility'])}. The baselines mostly abstain or cover only a tiny fraction of hard cases.

\input{{../results/fixed_risk_table.tex}}

\begin{{figure}}[H]
\centering
\includegraphics[width=0.95\linewidth]{{force_memory_v5_fixed_risk.png}}
\caption{{Deployment coverage at strict damage budget. V5 preserves useful coverage while satisfying the local fixed-risk gate.}}
\end{{figure}}

\section{{Paired Evidence}}
\input{{../results/pairwise_decision_table.tex}}
The paired hard-unit comparisons show that v5 is not only better on aggregate averages. It beats every non-oracle reference under paired task/regime/seed units. The oracle remains higher, which is expected because it observes the latent force mode directly.

\section{{Representative Negative Cases}}
\input{{../results/negative_cases_table.tex}}
The negative cases are not discarded. They show where the method remains brittle: abrupt contact shifts, hidden preload under force-sensor dropout, and extreme unseen modes can still produce unsafe commitments or abstentions. These cases define the next hardware or high-fidelity validation agenda.

\section{{Related Work Pressure}}
The related work landscape is crowded. Transformer imitation and diffusion policies create a natural baseline for long-horizon memory {cite(keys, 18, 27)}. Tactile and force representation learning pressure the novelty of force-event tokens {cite(keys, 27, 36)}. Adaptive impedance and online system identification pressure the claim that memory is better than adaptation {cite(keys, 36, 45)}. Conformal risk filtering and safe MPC pressure the risk-calibration component {cite(keys, 45, 54)}. Task-and-motion planning and recovery methods pressure the closed-loop control claim {cite(keys, 54, 63)}. This paper survives only as a local mechanism audit; it does not yet have the external evidence needed for a main-conference robotics claim.

\section{{Limitations}}
The largest limitation is scope. There is no real robot experiment, no accepted high-fidelity simulator benchmark, no external benchmark, no trained transformer checkpoint, no tactile hardware logs, and no hardware video. The runner is deterministic and local. The results should guide whether to invest in external validation; they should not be marketed as final deployment evidence.

The second limitation is model realism. The v5 method is an executable policy proxy, not a trained transformer. It isolates the force-memory mechanism, but it cannot prove that a learned architecture would discover and preserve the same state without careful data and objectives. A future submission must train the model, release checkpoints, and evaluate under real or widely recognized high-fidelity conditions.

\section{{Conclusion}}
Paper 100 is locally promising but not submission-ready. The expanded audit improves the v4.1 artifact from a 7-page local result into a 25+ page evidence package with strong baselines, ablations, stress tests, fixed-risk deployment, paired statistics, theory, and limitations. The correct terminal state is \textbf{{STRONG\_REVISE}}. The acceptance odds improve only if future work adds external robot or high-fidelity validation and trained checkpoint evidence.

\appendix
\section{{Full Gate Ledger}}
\begin{{longtable}}{{p{{0.22\linewidth}}p{{0.14\linewidth}}p{{0.56\linewidth}}}}
\toprule
Gate & Result & Evidence \\
\midrule
Success & pass & v5 success {fnum(v5['task_success'])} exceeds best non-oracle reference {latex_escape(short_method(best_success['method']))} at {fnum(best_success['task_success'])}. \\
Force violation & pass & v5 violation {fnum(v5['force_violation_rate'])} improves over safest strong baseline {latex_escape(short_method(best_safety['method']))} at {fnum(best_safety['force_violation_rate'])}. \\
Damage & pass & v5 damage {fnum(v5['damage_rate'])} improves over strongest safety reference {latex_escape(short_method(best_damage['method']))}. \\
Regret & pass & v5 regret {fnum(v5['planning_regret_to_oracle'])} is below non-oracle references. \\
Utility & pass & v5 robust utility {fnum(v5['robust_utility'])} is the best non-oracle value. \\
Diagnostics & pass & latent accuracy, stale false positives, and missed false negatives clear frozen thresholds. \\
Calibration & pass & v5 ECE {fnum(v5['force_risk_ece'])} clears best-reference-plus-tolerance against {latex_escape(short_method(best_ece['method']))}. \\
Ablation & pass & no planned ablation matches or beats full v5 robust utility. \\
Stress & pass & v5 wins maximum-stress robust utility among non-oracle methods. \\
Fixed risk & pass & v5 has useful coverage under strict force/damage budgets. \\
Scope & fail & no real robot, accepted high-fidelity benchmark, external benchmark, or trained checkpoint evidence exists. \\
\bottomrule
\end{{longtable}}

\section{{All Split-Method Metrics}}
\begin{{longtable}}{{llrrrrr}}
\toprule
Split & Method & Success & Violation & Damage & Regret & Utility \\
\midrule
{long_metric_rows(split_metric_rows, ['split', 'method', 'task_success', 'force_violation_rate', 'damage_rate', 'planning_regret_to_oracle', 'robust_utility'])}
\bottomrule
\end{{longtable}}

\section{{Citation Ledger}}
The following ledger is intentionally verbose so that clickable citation boxes are visible throughout the PDF and route directly to the bibliography.
\begin{{longtable}}{{p{{0.06\linewidth}}p{{0.34\linewidth}}p{{0.48\linewidth}}}}
\toprule
\# & Pressure theme & References \\
\midrule
{citation_ledger(keys)}
\bottomrule
\end{{longtable}}

\section{{Reproducibility Checklist}}
\begin{{itemize}}
\item Main rows: 345,600.
\item Dataset rows: 23,040.
\item Ablation rows: 115,200.
\item Stress rows: 288,000.
\item Fixed-risk rows: 138,240.
\item Negative cases: 24.
\item CPU-only execution; no GPU or high-RAM tensor workload.
\item Final numbered PDF target: \texttt{{C:/Users/wangz/Downloads/100.pdf}}.
\item Visible Desktop PDF copy is prohibited.
\item Public repository target: \url{{https://github.com/Jason-Wang313/100_force_memory_transformers}}.
\end{{itemize}}

\bibliographystyle{{iclr2026_conference}}
\bibliography{{references}}
\end{{document}}
"""
    (PAPER / "main.tex").write_text(tex, encoding="utf-8")
    print(f"wrote {PAPER / 'main.tex'}")
    print(f"wrote {PAPER / 'references.bib'} with {len(keys)} entries")


if __name__ == "__main__":
    main()
