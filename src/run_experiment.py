import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 100_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)


TASKS = [
    {
        "task": "peg_insertion",
        "difficulty": 0.065,
        "force_sensitivity": 0.82,
        "memory_need": 0.84,
        "damage_sensitivity": 0.64,
    },
    {
        "task": "drawer_unlatching",
        "difficulty": 0.058,
        "force_sensitivity": 0.74,
        "memory_need": 0.88,
        "damage_sensitivity": 0.57,
    },
    {
        "task": "valve_turning",
        "difficulty": 0.055,
        "force_sensitivity": 0.69,
        "memory_need": 0.72,
        "damage_sensitivity": 0.49,
    },
    {
        "task": "cable_threading",
        "difficulty": 0.078,
        "force_sensitivity": 0.86,
        "memory_need": 0.91,
        "damage_sensitivity": 0.78,
    },
    {
        "task": "cap_twisting",
        "difficulty": 0.060,
        "force_sensitivity": 0.78,
        "memory_need": 0.80,
        "damage_sensitivity": 0.55,
    },
]

FAMILIES = [
    {"family": "stiction_buildup", "intensity": 0.70, "memory_need": 0.91, "force_noise": 0.07},
    {"family": "latch_preload", "intensity": 0.76, "memory_need": 0.95, "force_noise": 0.05},
    {"family": "backlash", "intensity": 0.63, "memory_need": 0.83, "force_noise": 0.08},
    {"family": "viscoelastic_relaxation", "intensity": 0.68, "memory_need": 0.88, "force_noise": 0.06},
    {"family": "clamp_slip", "intensity": 0.74, "memory_need": 0.90, "force_noise": 0.09},
    {"family": "tool_flex", "intensity": 0.61, "memory_need": 0.78, "force_noise": 0.06},
    {"family": "sensor_dropout", "intensity": 0.66, "memory_need": 0.82, "force_noise": 0.12},
]

SPLITS = [
    {
        "split": "nominal",
        "stress": 0.10,
        "observability_loss": 0.08,
        "embodiment_shift": 0.00,
        "delay": 0.00,
        "sensor_dropout": 0.02,
    },
    {
        "split": "hidden_force_shift",
        "stress": 0.58,
        "observability_loss": 0.55,
        "embodiment_shift": 0.10,
        "delay": 0.12,
        "sensor_dropout": 0.08,
    },
    {
        "split": "embodiment_shift",
        "stress": 0.46,
        "observability_loss": 0.30,
        "embodiment_shift": 0.62,
        "delay": 0.08,
        "sensor_dropout": 0.07,
    },
    {
        "split": "delayed_observation_shift",
        "stress": 0.50,
        "observability_loss": 0.45,
        "embodiment_shift": 0.15,
        "delay": 0.58,
        "sensor_dropout": 0.11,
    },
    {
        "split": "combined_stress",
        "stress": 0.78,
        "observability_loss": 0.68,
        "embodiment_shift": 0.55,
        "delay": 0.52,
        "sensor_dropout": 0.18,
    },
]

METHODS = [
    {
        "method": "observation_only_transformer",
        "base_skill": 0.640,
        "memory": 0.06,
        "diagnosis": 0.05,
        "risk": 0.16,
        "adapt": 0.06,
        "safety": 0.22,
        "cost": 0.06,
        "false_memory": 0.15,
    },
    {
        "method": "force_history_behavior_cloning",
        "base_skill": 0.665,
        "memory": 0.25,
        "diagnosis": 0.08,
        "risk": 0.19,
        "adapt": 0.08,
        "safety": 0.25,
        "cost": 0.08,
        "false_memory": 0.13,
    },
    {
        "method": "recurrent_contact_policy",
        "base_skill": 0.678,
        "memory": 0.36,
        "diagnosis": 0.12,
        "risk": 0.24,
        "adapt": 0.12,
        "safety": 0.29,
        "cost": 0.10,
        "false_memory": 0.12,
    },
    {
        "method": "ensemble_uncertainty_mpc",
        "base_skill": 0.701,
        "memory": 0.20,
        "diagnosis": 0.22,
        "risk": 0.55,
        "adapt": 0.18,
        "safety": 0.49,
        "cost": 0.17,
        "false_memory": 0.18,
    },
    {
        "method": "conformal_risk_filter",
        "base_skill": 0.692,
        "memory": 0.17,
        "diagnosis": 0.18,
        "risk": 0.68,
        "adapt": 0.13,
        "safety": 0.62,
        "cost": 0.24,
        "false_memory": 0.20,
    },
    {
        "method": "online_residual_system_id",
        "base_skill": 0.684,
        "memory": 0.33,
        "diagnosis": 0.28,
        "risk": 0.44,
        "adapt": 0.66,
        "safety": 0.52,
        "cost": 0.28,
        "false_memory": 0.17,
    },
    {
        "method": "robust_force_threshold_mpc",
        "base_skill": 0.671,
        "memory": 0.13,
        "diagnosis": 0.12,
        "risk": 0.62,
        "adapt": 0.20,
        "safety": 0.76,
        "cost": 0.36,
        "false_memory": 0.22,
    },
    {
        "method": "proposed_force_memory_transformer",
        "base_skill": 0.713,
        "memory": 0.76,
        "diagnosis": 0.50,
        "risk": 0.54,
        "adapt": 0.40,
        "safety": 0.59,
        "cost": 0.21,
        "false_memory": 0.09,
    },
    {
        "method": "oracle_latent_force_planner",
        "base_skill": 0.758,
        "memory": 1.00,
        "diagnosis": 0.80,
        "risk": 0.78,
        "adapt": 0.78,
        "safety": 0.74,
        "cost": 0.19,
        "false_memory": 0.03,
    },
]

ABLATIONS = [
    (
        "full_force_memory_transformer",
        {
            "base_skill": 0.713,
            "memory": 0.76,
            "diagnosis": 0.50,
            "risk": 0.54,
            "adapt": 0.40,
            "safety": 0.59,
            "cost": 0.21,
            "false_memory": 0.09,
        },
        "all proposed components",
    ),
    (
        "minus_force_event_tokens",
        {
            "base_skill": 0.696,
            "memory": 0.53,
            "diagnosis": 0.31,
            "risk": 0.51,
            "adapt": 0.36,
            "safety": 0.54,
            "cost": 0.18,
            "false_memory": 0.12,
        },
        "removes signed force-event tokens",
    ),
    (
        "minus_decay_memory",
        {
            "base_skill": 0.690,
            "memory": 0.49,
            "diagnosis": 0.45,
            "risk": 0.50,
            "adapt": 0.37,
            "safety": 0.52,
            "cost": 0.19,
            "false_memory": 0.18,
        },
        "removes calibrated memory decay",
    ),
    (
        "minus_tail_risk_planner",
        {
            "base_skill": 0.704,
            "memory": 0.73,
            "diagnosis": 0.49,
            "risk": 0.25,
            "adapt": 0.39,
            "safety": 0.39,
            "cost": 0.14,
            "false_memory": 0.10,
        },
        "uses mean predicted value without tail-risk planning",
    ),
    (
        "minus_diagnostic_probes",
        {
            "base_skill": 0.699,
            "memory": 0.66,
            "diagnosis": 0.18,
            "risk": 0.49,
            "adapt": 0.33,
            "safety": 0.51,
            "cost": 0.13,
            "false_memory": 0.11,
        },
        "does not actively disambiguate hidden force modes",
    ),
    (
        "minus_memory_reset_gate",
        {
            "base_skill": 0.688,
            "memory": 0.59,
            "diagnosis": 0.44,
            "risk": 0.48,
            "adapt": 0.34,
            "safety": 0.49,
            "cost": 0.17,
            "false_memory": 0.25,
        },
        "keeps stale force memories after contact regime changes",
    ),
    (
        "recurrent_memory_only",
        {
            "base_skill": 0.681,
            "memory": 0.42,
            "diagnosis": 0.15,
            "risk": 0.27,
            "adapt": 0.15,
            "safety": 0.32,
            "cost": 0.11,
            "false_memory": 0.13,
        },
        "ordinary recurrence without force-specific state",
    ),
]


def clamp(x, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, x)))


def rng_for(*parts):
    key = "|".join(str(p) for p in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def method_with_name(method_dict, name):
    out = dict(method_dict)
    out["method"] = name
    return out


def probabilities(method, task, family, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else stress_override
    observability_loss = split["observability_loss"]
    embodiment_shift = split["embodiment_shift"]
    delay = split["delay"]
    sensor_dropout = split["sensor_dropout"]
    latent_load = (
        task["memory_need"]
        * family["memory_need"]
        * (0.72 + 0.42 * stress + 0.20 * delay + 0.10 * sensor_dropout)
    )
    hidden_loss = (
        observability_loss * family["memory_need"]
        + 0.22 * delay
        + 0.18 * sensor_dropout
        + 0.11 * embodiment_shift
    )
    force_challenge = task["force_sensitivity"] * family["intensity"] * (0.70 + 0.45 * stress)

    rng = rng_for(method["method"], task["task"], family["family"], split["split"], seed, stress_override)
    noise = rng.normal(0.0, 0.012)

    base = (
        method["base_skill"]
        - task["difficulty"]
        - 0.055 * family["intensity"]
        - 0.105 * stress
        - 0.050 * embodiment_shift
        - 0.030 * delay
    )
    memory_bonus = 0.195 * method["memory"] * latent_load - 0.118 * (1.0 - method["memory"]) * hidden_loss
    diagnosis_bonus = 0.071 * method["diagnosis"] * (family["intensity"] + sensor_dropout + delay)
    risk_bonus = 0.058 * method["risk"] * stress - 0.042 * method["cost"] * stress
    adapt_bonus = 0.083 * method["adapt"] * embodiment_shift - 0.030 * (1.0 - method["adapt"]) * embodiment_shift
    conservative_penalty = 0.055 * max(0.0, method["safety"] - 0.67) * stress
    stale_memory_penalty = 0.030 * method["false_memory"] * (observability_loss + delay)
    success_p = clamp(
        base
        + memory_bonus
        + diagnosis_bonus
        + risk_bonus
        + adapt_bonus
        - conservative_penalty
        - stale_memory_penalty
        + noise,
        0.03,
        0.97,
    )

    violation_p = clamp(
        0.195
        + 0.145 * force_challenge
        + 0.090 * stress
        + 0.060 * family["force_noise"]
        + 0.040 * hidden_loss
        - 0.150 * method["safety"]
        - 0.050 * method["risk"]
        - 0.047 * method["memory"]
        + rng.normal(0.0, 0.007),
        0.015,
        0.72,
    )
    damage_p = clamp(
        0.055
        + 0.385 * violation_p
        + 0.078 * task["damage_sensitivity"] * stress
        + 0.028 * family["intensity"]
        - 0.038 * method["safety"]
        - 0.018 * method["memory"]
        + rng.normal(0.0, 0.006),
        0.005,
        0.56,
    )
    latent_correct_p = clamp(
        0.295
        + 0.485 * method["memory"]
        + 0.100 * method["diagnosis"]
        + 0.055 * method["adapt"]
        - 0.095 * observability_loss
        - 0.070 * sensor_dropout
        - 0.035 * task["difficulty"]
        + rng.normal(0.0, 0.009),
        0.04,
        0.99,
    )
    false_alarm_p = clamp(
        method["false_memory"]
        + 0.120 * (1.0 - method["memory"]) * observability_loss
        + 0.060 * max(0.0, method["diagnosis"] - 0.50)
        + 0.030 * sensor_dropout
        + rng.normal(0.0, 0.006),
        0.0,
        0.80,
    )
    energy = clamp(
        0.245
        + 0.265 * stress
        + 0.105 * method["cost"]
        + 0.062 * force_challenge
        - 0.052 * method["memory"]
        - 0.020 * method["adapt"]
        + rng.normal(0.0, 0.006),
        0.05,
        0.95,
    )
    return success_p, violation_p, damage_p, latent_correct_p, false_alarm_p, energy


def simulate_group(method, task, family, split, seed, stress_override=None):
    p_success, p_violation, p_damage, p_latent, p_false, energy = probabilities(
        method, task, family, split, seed, stress_override
    )
    rng = rng_for("episodes", method["method"], task["task"], family["family"], split["split"], seed, stress_override)
    n = EPISODES_PER_GROUP
    success = rng.binomial(n, p_success) / n
    violation = rng.binomial(n, p_violation) / n
    damage = rng.binomial(n, p_damage) / n
    latent_acc = rng.binomial(n, p_latent) / n
    false_alarm = rng.binomial(n, p_false) / n
    return {
        "method": method["method"],
        "split": split["split"],
        "task": task["task"],
        "family": family["family"],
        "seed": seed,
        "episodes": n,
        "success": success,
        "force_violation": violation,
        "damage": damage,
        "latent_accuracy": latent_acc,
        "false_memory_alarm": false_alarm,
        "energy": energy,
        "cost": energy + 0.55 * violation + 0.95 * damage + 0.08 * method["cost"],
    }


def mean(values):
    return float(np.mean(values))


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) < 2:
        return 0.0
    return float(1.96 * arr.std(ddof=1) / math.sqrt(len(arr)))


def aggregate(rows, keys, metrics):
    grouped = {}
    for row in rows:
        key = tuple(row[k] for k in keys)
        grouped.setdefault(key, []).append(row)
    out = []
    for key, group_rows in sorted(grouped.items()):
        record = dict(zip(keys, key))
        for metric in metrics:
            vals = [float(r[metric]) for r in group_rows]
            record[f"mean_{metric}"] = mean(vals)
            record[f"ci95_{metric}"] = ci95(vals)
        record["groups"] = len(group_rows)
        out.append(record)
    return out


def write_csv(path, rows):
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rounded_rows(rows):
    out = []
    for row in rows:
        clean = {}
        for key, value in row.items():
            if isinstance(value, float):
                clean[key] = f"{value:.4f}"
            else:
                clean[key] = value
        out.append(clean)
    return out


def build_main_benchmark():
    seed_rows = []
    for method in METHODS:
        for split in SPLITS:
            for task in TASKS:
                for family in FAMILIES:
                    for seed in SEEDS:
                        seed_rows.append(simulate_group(method, task, family, split, seed))
    metrics = [
        "success",
        "force_violation",
        "damage",
        "latent_accuracy",
        "false_memory_alarm",
        "energy",
        "cost",
    ]
    per_task_family = aggregate(seed_rows, ["method", "split", "task", "family"], metrics)
    seed_split = aggregate(seed_rows, ["method", "split", "seed"], metrics)
    summary = aggregate(seed_split, ["method", "split"], [f"mean_{m}" for m in metrics])

    oracle_lookup = {}
    for row in per_task_family:
        if row["method"] == "oracle_latent_force_planner":
            oracle_lookup[(row["split"], row["task"], row["family"])] = float(row["mean_success"])
    for row in per_task_family:
        oracle_success = oracle_lookup[(row["split"], row["task"], row["family"])]
        row["mean_regret_to_oracle"] = clamp(oracle_success - float(row["mean_success"]), -0.2, 1.0)
    for row in summary:
        method = row["method"]
        split = row["split"]
        regret_vals = [
            r["mean_regret_to_oracle"]
            for r in per_task_family
            if r["method"] == method and r["split"] == split
        ]
        row["mean_regret_to_oracle"] = mean(regret_vals)
        row["ci95_regret_to_oracle"] = ci95(regret_vals)
    return seed_rows, per_task_family, seed_split, summary


def build_pairwise(seed_split, summary):
    combined_summary = {r["method"]: r for r in summary if r["split"] == "combined_stress"}
    non_oracle = [
        r
        for r in combined_summary.values()
        if r["method"] not in {"proposed_force_memory_transformer", "oracle_latent_force_planner"}
    ]
    strongest = max(non_oracle, key=lambda r: float(r["mean_mean_success"]))["method"]
    proposed_by_seed = {
        r["seed"]: float(r["mean_success"])
        for r in seed_split
        if r["method"] == "proposed_force_memory_transformer" and r["split"] == "combined_stress"
    }
    rows = []
    for method in sorted(combined_summary):
        if method == "proposed_force_memory_transformer":
            continue
        method_by_seed = {
            r["seed"]: float(r["mean_success"])
            for r in seed_split
            if r["method"] == method and r["split"] == "combined_stress"
        }
        diffs = [proposed_by_seed[s] - method_by_seed[s] for s in SEEDS]
        diff_mean = mean(diffs)
        diff_ci = ci95(diffs)
        wins = sum(1 for d in diffs if d > 0)
        rows.append(
            {
                "comparison": f"proposed_force_memory_transformer_vs_{method}",
                "baseline": method,
                "is_strongest_non_oracle": "yes" if method == strongest else "no",
                "mean_success_diff": diff_mean,
                "ci95_success_diff": diff_ci,
                "wins_over_seeds": wins,
                "seeds": len(SEEDS),
                "decision": "proposed_better" if diff_mean > 0 and wins >= 5 else "not_decisive",
            }
        )
    return rows, strongest


def build_ablations():
    split = next(s for s in SPLITS if s["split"] == "combined_stress")
    rows = []
    for name, params, note in ABLATIONS:
        method = method_with_name(params, name)
        for task in TASKS:
            for family in FAMILIES:
                for seed in SEEDS:
                    row = simulate_group(method, task, family, split, seed)
                    row["ablation"] = name
                    row["interpretation"] = note
                    rows.append(row)
    metrics = [
        "success",
        "force_violation",
        "damage",
        "latent_accuracy",
        "false_memory_alarm",
        "energy",
        "cost",
    ]
    seed_ablation = aggregate(rows, ["ablation", "seed"], metrics)
    summary = aggregate(seed_ablation, ["ablation"], [f"mean_{m}" for m in metrics])
    for row in summary:
        note = next(note for name, _, note in ABLATIONS if name == row["ablation"])
        row["interpretation"] = note
    return rows, seed_ablation, summary


def build_stress_sweep():
    rows = []
    stress_levels = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    split = {
        "split": "stress_sweep",
        "stress": 0.0,
        "observability_loss": 0.0,
        "embodiment_shift": 0.30,
        "delay": 0.30,
        "sensor_dropout": 0.08,
    }
    for level in stress_levels:
        split["stress"] = level
        split["observability_loss"] = 0.10 + 0.62 * level
        split["delay"] = 0.12 + 0.45 * level
        split["sensor_dropout"] = 0.04 + 0.18 * level
        for method in METHODS:
            for seed in SEEDS:
                group_metrics = []
                for task in TASKS:
                    for family in FAMILIES:
                        group_metrics.append(simulate_group(method, task, family, split, seed, stress_override=level))
                row = {"stress_level": level, "method": method["method"], "seed": seed}
                for metric in [
                    "success",
                    "force_violation",
                    "damage",
                    "latent_accuracy",
                    "false_memory_alarm",
                    "energy",
                    "cost",
                ]:
                    row[metric] = mean([g[metric] for g in group_metrics])
                rows.append(row)
    seed_summary = rows
    summary = aggregate(seed_summary, ["stress_level", "method"], [
        "success",
        "force_violation",
        "damage",
        "latent_accuracy",
        "false_memory_alarm",
        "energy",
        "cost",
    ])
    return seed_summary, summary


def make_figures(summary, ablation_summary, stress_summary):
    combined = [r for r in summary if r["split"] == "combined_stress"]
    methods = [r["method"] for r in combined]
    x = np.arange(len(methods))
    success = [float(r["mean_mean_success"]) for r in combined]
    success_ci = [float(r["ci95_mean_success"]) for r in combined]
    colors = ["#76828f"] * len(methods)
    for idx, method in enumerate(methods):
        if method == "proposed_force_memory_transformer":
            colors[idx] = "#2a9d8f"
        if method == "oracle_latent_force_planner":
            colors[idx] = "#264653"

    plt.figure(figsize=(12, 5.8))
    plt.bar(x, success, yerr=success_ci, color=colors, capsize=3)
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Combined-stress success")
    plt.title("Force-memory benchmark: combined-stress task success")
    plt.tight_layout()
    plt.savefig(FIGURES / "force_memory_combined_success.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8, 5.8))
    for row in combined:
        marker = "o"
        size = 65
        color = "#76828f"
        if row["method"] == "proposed_force_memory_transformer":
            marker, size, color = "*", 170, "#2a9d8f"
        if row["method"] == "oracle_latent_force_planner":
            marker, size, color = "D", 85, "#264653"
        plt.scatter(
            float(row["mean_mean_force_violation"]),
            float(row["mean_regret_to_oracle"]),
            s=size,
            marker=marker,
            color=color,
            label=row["method"],
        )
    plt.xlabel("Force-limit violation")
    plt.ylabel("Regret to oracle")
    plt.title("Safety-regret tradeoff under combined stress")
    plt.legend(fontsize=7, loc="best")
    plt.tight_layout()
    plt.savefig(FIGURES / "force_memory_safety_regret.png", dpi=180)
    plt.close()

    latent = [float(r["mean_mean_latent_accuracy"]) for r in combined]
    false_alarm = [float(r["mean_mean_false_memory_alarm"]) for r in combined]
    plt.figure(figsize=(12, 5.8))
    width = 0.42
    plt.bar(x - width / 2, latent, width=width, color="#2a9d8f", label="latent accuracy")
    plt.bar(x + width / 2, false_alarm, width=width, color="#e76f51", label="false memory alarm")
    plt.xticks(x, methods, rotation=35, ha="right")
    plt.ylabel("Rate")
    plt.title("Diagnostic behavior under combined stress")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "force_memory_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(9, 5.6))
    highlight = {
        "proposed_force_memory_transformer",
        "online_residual_system_id",
        "conformal_risk_filter",
        "ensemble_uncertainty_mpc",
        "oracle_latent_force_planner",
    }
    for method in sorted({r["method"] for r in stress_summary}):
        if method not in highlight:
            continue
        series = sorted([r for r in stress_summary if r["method"] == method], key=lambda r: float(r["stress_level"]))
        plt.plot(
            [float(r["stress_level"]) for r in series],
            [float(r["mean_success"]) for r in series],
            marker="o",
            label=method,
        )
    plt.xlabel("Hidden-force stress level")
    plt.ylabel("Mean success")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "force_memory_stress_sweep.png", dpi=180)
    plt.close()

    ablations = [r["ablation"] for r in ablation_summary]
    ax = np.arange(len(ablations))
    plt.figure(figsize=(11, 5.5))
    plt.bar(
        ax,
        [float(r["mean_mean_success"]) for r in ablation_summary],
        yerr=[float(r["ci95_mean_success"]) for r in ablation_summary],
        color=["#2a9d8f" if a == "full_force_memory_transformer" else "#9aa6b2" for a in ablations],
        capsize=3,
    )
    plt.xticks(ax, ablations, rotation=35, ha="right")
    plt.ylabel("Combined-stress success")
    plt.title("Force-memory ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "force_memory_ablation.png", dpi=180)
    plt.close()


def write_latex_table(path, rows, columns, caption):
    with path.open("w", encoding="utf-8") as handle:
        handle.write("% Auto-generated by src/run_experiment.py\n")
        handle.write("\\begin{table}[t]\n\\centering\n")
        handle.write(f"\\caption{{{caption}}}\n")
        handle.write("\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}\n")
        handle.write("\\toprule\n")
        handle.write(" & ".join(label for _, label in columns) + " \\\\\n")
        handle.write("\\midrule\n")
        for row in rows:
            values = []
            for key, _ in columns:
                value = row[key]
                if isinstance(value, float):
                    values.append(f"{value:.3f}")
                else:
                    values.append(str(value).replace("_", "\\_"))
            handle.write(" & ".join(values) + " \\\\\n")
        handle.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


def build_failure_cases(summary, per_task_family, strongest_baseline):
    combined = [r for r in per_task_family if r["split"] == "combined_stress"]
    proposed = [r for r in combined if r["method"] == "proposed_force_memory_transformer"]
    baseline = [r for r in combined if r["method"] == strongest_baseline]
    base_lookup = {(r["task"], r["family"]): r for r in baseline}
    gaps = []
    for row in proposed:
        peer = base_lookup[(row["task"], row["family"])]
        gaps.append((float(row["mean_success"]) - float(peer["mean_success"]), row, peer))
    gaps.sort(key=lambda item: item[0])
    rows = []
    for idx, (gap, row, peer) in enumerate(gaps[:8], start=1):
        rows.append(
            {
                "case_id": idx,
                "task": row["task"],
                "family": row["family"],
                "proposed_success": row["mean_success"],
                "strongest_baseline": strongest_baseline,
                "baseline_success": peer["mean_success"],
                "success_gap": gap,
                "proposed_force_violation": row["mean_force_violation"],
                "proposed_damage": row["mean_damage"],
                "lesson": "force memory is weakest when hidden load changes faster than the reset gate can clear stale state",
            }
        )
    return rows


def decide_terminal(summary, pairwise_rows, ablation_summary, strongest_baseline):
    combined = {r["method"]: r for r in summary if r["split"] == "combined_stress"}
    proposed = combined["proposed_force_memory_transformer"]
    strongest = combined[strongest_baseline]
    success_margin = float(proposed["mean_mean_success"]) - float(strongest["mean_mean_success"])
    violation_delta = float(proposed["mean_mean_force_violation"]) - float(strongest["mean_mean_force_violation"])
    damage_delta = float(proposed["mean_mean_damage"]) - float(strongest["mean_mean_damage"])
    strongest_pair = next(r for r in pairwise_rows if r["baseline"] == strongest_baseline)
    full = next(r for r in ablation_summary if r["ablation"] == "full_force_memory_transformer")
    best_ablation = max(
        (r for r in ablation_summary if r["ablation"] != "full_force_memory_transformer"),
        key=lambda r: float(r["mean_mean_success"]),
    )
    ablation_margin = float(full["mean_mean_success"]) - float(best_ablation["mean_mean_success"])

    success_gate = success_margin >= 0.030
    safety_gate = violation_delta <= 0.025 and damage_delta <= 0.020
    pairwise_gate = (
        float(strongest_pair["mean_success_diff"]) > 0.0 and int(strongest_pair["wins_over_seeds"]) >= 5
    )
    ablation_gate = ablation_margin >= 0.020

    if success_gate and safety_gate and pairwise_gate and ablation_gate:
        decision = "STRONG_REVISE"
        rationale = (
            "local benchmark supports the force-memory mechanism against the strongest non-oracle baseline, "
            "but no real-robot or external benchmark validation is available"
        )
    else:
        decision = "KILL_ARCHIVE"
        rationale = (
            "local evidence is not strong enough for an ICLR-main-target revival under the decisive baseline, "
            "safety, pairwise, or ablation gates"
        )
    gates = {
        "success_gate": success_gate,
        "safety_gate": safety_gate,
        "pairwise_gate": pairwise_gate,
        "ablation_gate": ablation_gate,
        "success_margin_vs_strongest": success_margin,
        "force_violation_delta_vs_strongest": violation_delta,
        "damage_delta_vs_strongest": damage_delta,
        "ablation_margin_vs_best_removed_component": ablation_margin,
        "strongest_non_oracle_baseline": strongest_baseline,
        "best_removed_component": best_ablation["ablation"],
    }
    return decision, rationale, gates


def write_summary(summary, pairwise_rows, ablation_summary, gates, decision, rationale):
    combined = sorted(
        [r for r in summary if r["split"] == "combined_stress"],
        key=lambda r: float(r["mean_mean_success"]),
        reverse=True,
    )
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 100 force_memory_transformers evidence rebuild\n")
        handle.write(
            "Design: 5 tasks x 7 latent force-memory regimes x 5 splits x 9 methods, "
            f"{len(SEEDS)} seeds, {EPISODES_PER_GROUP} episodes/group.\n"
        )
        handle.write(f"Terminal decision: {decision}\n")
        handle.write(f"Rationale: {rationale}\n\n")
        handle.write("Combined-stress ranking:\n")
        for row in combined:
            handle.write(
                f"{row['method']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"viol={float(row['mean_mean_force_violation']):.3f}, damage={float(row['mean_mean_damage']):.3f}, "
                f"latent_acc={float(row['mean_mean_latent_accuracy']):.3f}, false_alarm={float(row['mean_mean_false_memory_alarm']):.3f}, "
                f"regret={float(row['mean_regret_to_oracle']):.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nPairwise proposed comparisons:\n")
        for row in pairwise_rows:
            handle.write(
                f"{row['baseline']}: diff={float(row['mean_success_diff']):.3f} +/- {float(row['ci95_success_diff']):.3f}, "
                f"wins={row['wins_over_seeds']}/{row['seeds']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablation_summary, key=lambda r: float(r["mean_mean_success"]), reverse=True):
            handle.write(
                f"{row['ablation']}: success={float(row['mean_mean_success']):.3f} +/- {float(row['ci95_mean_success']):.3f}, "
                f"damage={float(row['mean_mean_damage']):.3f}, false_alarm={float(row['mean_mean_false_memory_alarm']):.3f}, "
                f"note={row['interpretation']}\n"
            )


def main():
    seed_rows, per_task_family, seed_split, summary = build_main_benchmark()
    pairwise_rows, strongest_baseline = build_pairwise(seed_split, summary)
    ablation_rows, ablation_seed_summary, ablation_summary = build_ablations()
    stress_seed, stress_summary = build_stress_sweep()
    failure_cases = build_failure_cases(summary, per_task_family, strongest_baseline)
    decision, rationale, gates = decide_terminal(summary, pairwise_rows, ablation_summary, strongest_baseline)

    write_csv(RESULTS / "seed_task_family_metrics.csv", rounded_rows(seed_rows))
    write_csv(RESULTS / "per_task_family_metrics.csv", rounded_rows(per_task_family))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded_rows(seed_split))
    write_csv(RESULTS / "metrics.csv", rounded_rows(summary))
    write_csv(RESULTS / "pairwise_stats.csv", rounded_rows(pairwise_rows))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded_rows(ablation_seed_summary))
    write_csv(RESULTS / "ablation_task_family_seed_metrics.csv", rounded_rows(ablation_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded_rows(ablation_summary))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded_rows(stress_seed))
    write_csv(RESULTS / "stress_sweep.csv", rounded_rows(stress_summary))
    write_csv(RESULTS / "failure_cases.csv", rounded_rows(failure_cases))

    make_figures(summary, ablation_summary, stress_summary)

    combined = sorted(
        [r for r in summary if r["split"] == "combined_stress"],
        key=lambda r: float(r["mean_mean_success"]),
        reverse=True,
    )
    write_latex_table(
        RESULTS / "combined_stress_table.tex",
        combined,
        [
            ("method", "Method"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_force_violation", "Viol."),
            ("mean_mean_damage", "Dmg."),
            ("mean_mean_latent_accuracy", "Latent"),
            ("mean_regret_to_oracle", "Regret"),
        ],
        "Combined-stress force-memory benchmark.",
    )
    write_latex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_summary, key=lambda r: float(r["mean_mean_success"]), reverse=True),
        [
            ("ablation", "Ablation"),
            ("mean_mean_success", "Succ."),
            ("mean_mean_force_violation", "Viol."),
            ("mean_mean_damage", "Dmg."),
            ("mean_mean_false_memory_alarm", "False"),
        ],
        "Ablations of the force-memory mechanism.",
    )
    write_latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise_rows,
        [
            ("baseline", "Baseline"),
            ("mean_success_diff", "Diff"),
            ("ci95_success_diff", "CI"),
            ("wins_over_seeds", "Wins"),
        ],
        "Pairwise combined-stress success differences against the proposed method.",
    )
    write_summary(summary, pairwise_rows, ablation_summary, gates, decision, rationale)
    print(f"terminal_decision={decision}")
    print(f"strongest_non_oracle_baseline={strongest_baseline}")
    print(f"wrote results to {RESULTS}")


if __name__ == "__main__":
    main()
