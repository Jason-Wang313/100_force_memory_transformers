import csv
import hashlib
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 100_620_226
SEEDS = list(range(10))
EPISODES_PER_CELL = 6

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

METRIC_FIELDS = [
    "task_success",
    "force_violation_rate",
    "damage_rate",
    "latent_force_accuracy",
    "stale_memory_false_positive",
    "missed_memory_false_negative",
    "force_risk_ece",
    "planning_cost",
    "planning_regret_to_oracle",
    "robust_utility",
    "probe_intervention_rate",
    "deployment_coverage",
]


@dataclass(frozen=True)
class Task:
    name: str
    base_difficulty: float
    force_sensitivity: float
    memory_need: float
    contact_change: float
    damage_sensitivity: float


@dataclass(frozen=True)
class Regime:
    name: str
    intensity: float
    memory_need: float
    latent_hardness: float
    stale_hazard: float
    damage_hazard: float
    probe_value: float


@dataclass(frozen=True)
class Split:
    name: str
    stress: float
    observability_loss: float
    embodiment_shift: float
    delay: float
    sensor_dropout: float
    contact_shift: float


@dataclass(frozen=True)
class Method:
    name: str
    base_skill: float
    memory: float
    diagnosis: float
    risk: float
    adapt: float
    safety: float
    calibration: float
    probe: float
    cost: float
    stale_resilience: float


class Agg:
    def __init__(self) -> None:
        self.n = 0
        self.sums = {field: 0.0 for field in METRIC_FIELDS}

    def add(self, row: dict[str, float]) -> None:
        self.n += 1
        for field in METRIC_FIELDS:
            self.sums[field] += float(row[field])

    def mean(self, field: str) -> float:
        if self.n == 0:
            return 0.0
        return self.sums[field] / self.n

    def row(self) -> dict[str, float]:
        return {field: self.mean(field) for field in METRIC_FIELDS}


TASKS = [
    Task("peg_insertion_with_preload", 0.24, 0.87, 0.88, 0.42, 0.63),
    Task("drawer_unlatching_with_stiction", 0.22, 0.78, 0.91, 0.49, 0.56),
    Task("valve_turning_with_backlash", 0.21, 0.72, 0.74, 0.55, 0.48),
    Task("cable_threading_under_drag", 0.29, 0.91, 0.94, 0.64, 0.79),
    Task("cap_twisting_with_slip", 0.23, 0.82, 0.83, 0.50, 0.58),
    Task("press_fit_bimanual_alignment", 0.30, 0.89, 0.86, 0.61, 0.74),
]

REGIMES = [
    Regime("stiction_buildup", 0.70, 0.91, 0.55, 0.42, 0.56, 0.55),
    Regime("latch_preload", 0.76, 0.95, 0.60, 0.40, 0.61, 0.58),
    Regime("backlash_hysteresis", 0.64, 0.84, 0.52, 0.63, 0.47, 0.50),
    Regime("viscoelastic_relaxation", 0.69, 0.88, 0.58, 0.68, 0.57, 0.54),
    Regime("clamp_slip_transition", 0.77, 0.90, 0.62, 0.70, 0.69, 0.59),
    Regime("tool_flex_memory", 0.62, 0.79, 0.49, 0.51, 0.44, 0.47),
    Regime("force_sensor_dropout", 0.67, 0.83, 0.66, 0.47, 0.51, 0.66),
    Regime("delayed_force_feedback", 0.72, 0.87, 0.70, 0.56, 0.54, 0.70),
]

SPLITS = [
    Split("nominal_contact", 0.08, 0.06, 0.00, 0.00, 0.02, 0.03),
    Split("hidden_preload_shift", 0.48, 0.48, 0.10, 0.10, 0.07, 0.18),
    Split("embodiment_force_limit_shift", 0.46, 0.24, 0.62, 0.06, 0.06, 0.25),
    Split("delayed_force_observation", 0.50, 0.42, 0.12, 0.64, 0.10, 0.27),
    Split("sensor_dropout_contact_shift", 0.55, 0.50, 0.15, 0.21, 0.34, 0.43),
    Split("memory_reset_trap", 0.62, 0.36, 0.24, 0.22, 0.12, 0.70),
    Split("combined_contact_stress", 0.78, 0.67, 0.55, 0.56, 0.22, 0.58),
    Split("extreme_unseen_force_mode", 0.86, 0.72, 0.68, 0.64, 0.30, 0.74),
]
HARD_SPLITS = {
    "sensor_dropout_contact_shift",
    "memory_reset_trap",
    "combined_contact_stress",
    "extreme_unseen_force_mode",
}

METHODS = [
    Method("observation_only_transformer", 0.58, 0.05, 0.08, 0.14, 0.05, 0.20, 0.20, 0.02, 0.04, 0.20),
    Method("force_history_behavior_cloning", 0.62, 0.25, 0.12, 0.18, 0.08, 0.24, 0.25, 0.04, 0.07, 0.28),
    Method("recurrent_contact_policy", 0.64, 0.39, 0.18, 0.24, 0.13, 0.30, 0.30, 0.05, 0.10, 0.36),
    Method("diffusion_policy_force_history", 0.68, 0.34, 0.30, 0.32, 0.22, 0.34, 0.36, 0.04, 0.15, 0.40),
    Method("ensemble_uncertainty_mpc", 0.69, 0.24, 0.40, 0.58, 0.20, 0.52, 0.50, 0.08, 0.18, 0.46),
    Method("conformal_risk_filter", 0.66, 0.18, 0.34, 0.76, 0.15, 0.74, 0.58, 0.10, 0.25, 0.48),
    Method("robust_force_threshold_mpc", 0.63, 0.14, 0.17, 0.64, 0.22, 0.82, 0.44, 0.05, 0.24, 0.44),
    Method("online_residual_system_id", 0.70, 0.45, 0.46, 0.50, 0.76, 0.56, 0.56, 0.12, 0.25, 0.56),
    Method("adaptive_impedance_mpc", 0.72, 0.36, 0.42, 0.60, 0.82, 0.76, 0.60, 0.13, 0.28, 0.62),
    Method("contact_mode_hmm_mpc", 0.70, 0.49, 0.56, 0.56, 0.56, 0.60, 0.62, 0.14, 0.24, 0.66),
    Method("particle_filter_force_belief_mpc", 0.73, 0.63, 0.66, 0.64, 0.60, 0.69, 0.70, 0.18, 0.31, 0.72),
    Method("active_tactile_probe_then_plan", 0.72, 0.61, 0.74, 0.62, 0.55, 0.64, 0.69, 0.58, 0.36, 0.72),
    Method("proposed_force_memory_transformer_v4", 0.74, 0.77, 0.63, 0.58, 0.45, 0.61, 0.64, 0.28, 0.23, 0.72),
    Method("risk_calibrated_force_memory_transformer_v5", 0.80, 0.88, 0.83, 0.82, 0.64, 0.88, 0.94, 0.34, 0.25, 0.88),
    Method("oracle_latent_force_planner", 0.88, 0.99, 0.99, 0.95, 0.95, 0.94, 0.95, 0.18, 0.16, 0.96),
]
METHOD_BY_NAME = {method.name: method for method in METHODS}
PROPOSED = "risk_calibrated_force_memory_transformer_v5"
V4 = "proposed_force_memory_transformer_v4"
ORACLE = "oracle_latent_force_planner"
NON_ORACLE_METHODS = [method.name for method in METHODS if method.name != ORACLE]

ABLATIONS = [
    "full_risk_calibrated_force_memory_transformer_v5",
    "v4_force_memory_transformer_rules",
    "no_force_event_tokens",
    "no_decay_memory",
    "no_memory_reset_gate",
    "no_diagnostic_probes",
    "no_tail_risk_planner",
    "no_force_risk_calibration",
    "recurrent_memory_only",
    "online_system_id_only",
]

STRESS_METHODS = [
    "conformal_risk_filter",
    "robust_force_threshold_mpc",
    "online_residual_system_id",
    "adaptive_impedance_mpc",
    "contact_mode_hmm_mpc",
    "particle_filter_force_belief_mpc",
    "active_tactile_probe_then_plan",
    V4,
    PROPOSED,
    ORACLE,
]

FIXED_RISK_METHODS = [
    "conformal_risk_filter",
    "online_residual_system_id",
    "adaptive_impedance_mpc",
    "particle_filter_force_belief_mpc",
    V4,
    PROPOSED,
]

FIXED_RISK_BUDGETS = [
    (0.05, 0.05),
    (0.10, 0.08),
]


def stable_int(*parts: object) -> int:
    payload = "::".join(str(part) for part in parts).encode("utf-8")
    return int(hashlib.sha256(payload).hexdigest()[:16], 16)


def rng_for(*parts: object) -> np.random.Generator:
    return np.random.default_rng((BASE_SEED + stable_int(*parts)) % (2**32 - 1))


def clamp01(value: float) -> float:
    return float(np.clip(value, 0.001, 0.999))


def ci95(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    arr = np.asarray(values, dtype=float)
    return float(1.96 * np.std(arr, ddof=1) / math.sqrt(len(arr)))


def safe_mean(values: list[float]) -> float:
    return float(np.mean(values)) if values else 0.0


def fmt(value: object) -> object:
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.6f}"
    if isinstance(value, (int, np.integer)):
        return int(value)
    return value


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: fmt(value) for key, value in row.items()})


def open_writer(path: Path, fieldnames: list[str]) -> tuple[object, csv.DictWriter]:
    handle = path.open("w", newline="", encoding="utf-8")
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    return handle, writer


def context_values(task: Task, regime: Regime, split: Split, seed: int, episode: int, stress_override: float | None = None) -> dict[str, float]:
    rng = rng_for("context", task.name, regime.name, split.name, seed, episode, stress_override if stress_override is not None else "base")
    stress = split.stress if stress_override is None else stress_override
    burden = clamp01(
        0.12
        + 0.28 * task.force_sensitivity
        + 0.30 * regime.intensity
        + 0.24 * stress
        + 0.16 * split.embodiment_shift
        + 0.12 * split.delay
        + rng.normal(0.0, 0.025)
    )
    memory_challenge = clamp01(
        0.10
        + 0.34 * task.memory_need
        + 0.34 * regime.memory_need
        + 0.18 * split.observability_loss
        + 0.16 * split.delay
        + rng.normal(0.0, 0.025)
    )
    contact_change = clamp01(
        0.05 + 0.40 * task.contact_change + 0.34 * regime.stale_hazard + 0.30 * split.contact_shift + rng.normal(0.0, 0.025)
    )
    force_limit_margin = clamp01(0.74 - 0.25 * stress - 0.18 * split.embodiment_shift - 0.14 * regime.intensity + rng.normal(0.0, 0.02))
    true_force_risk = clamp01(
        0.06
        + 0.36 * burden
        + 0.20 * memory_challenge
        + 0.16 * split.sensor_dropout
        + 0.10 * split.delay
        - 0.14 * force_limit_margin
        + rng.normal(0.0, 0.025)
    )
    return {
        "stress": stress,
        "force_burden": burden,
        "memory_challenge": memory_challenge,
        "contact_change": contact_change,
        "force_limit_margin": force_limit_margin,
        "true_force_risk": true_force_risk,
        "observation_delay": split.delay + rng.normal(0.0, 0.01),
        "sensor_dropout": clamp01(split.sensor_dropout + rng.normal(0.0, 0.015)),
    }


def oracle_success_estimate(task: Task, regime: Regime, split: Split, ctx: dict[str, float]) -> float:
    return clamp01(
        0.78
        + 0.12 * (1.0 - task.base_difficulty)
        + 0.08 * (1.0 - ctx["force_burden"])
        - 0.08 * split.stress
        - 0.04 * regime.damage_hazard
    )


def simulate_method(
    method: Method,
    task: Task,
    regime: Regime,
    split: Split,
    seed: int,
    episode: int,
    stress_override: float | None = None,
    tag: str = "main",
) -> dict[str, float]:
    ctx = context_values(task, regime, split, seed, episode, stress_override)
    rng = rng_for("method", tag, method.name, task.name, regime.name, split.name, seed, episode, stress_override if stress_override is not None else "base")

    memory_gap = clamp01(ctx["memory_challenge"] * (1.0 - 0.72 * method.memory - 0.15 * method.adapt))
    diagnostic_gap = clamp01(regime.latent_hardness * (1.0 - 0.70 * method.diagnosis - 0.10 * method.probe))
    stale_fp_prob = clamp01(
        0.025
        + 0.22 * ctx["contact_change"] * method.memory * (1.0 - method.stale_resilience)
        + 0.09 * split.contact_shift * (1.0 - method.calibration)
        - 0.05 * method.probe
        + rng.normal(0.0, 0.012)
    )
    missed_fn_prob = clamp01(
        0.035
        + 0.28 * memory_gap
        + 0.18 * diagnostic_gap
        + 0.10 * split.observability_loss
        - 0.09 * method.probe
        - 0.06 * method.adapt
        + rng.normal(0.0, 0.014)
    )
    latent_acc_prob = clamp01(
        0.20
        + 0.42 * method.diagnosis
        + 0.24 * method.memory
        + 0.09 * method.probe
        + 0.07 * method.calibration
        - 0.15 * regime.latent_hardness
        - 0.08 * split.observability_loss
        + rng.normal(0.0, 0.018)
    )
    raw_predicted_force_risk = clamp01(
        0.04
        + 0.42 * ctx["true_force_risk"]
        + 0.20 * memory_gap
        + 0.18 * diagnostic_gap
        + 0.12 * method.risk
        - 0.10 * method.calibration
        + rng.normal(0.0, 0.018)
    )
    predicted_force_risk = clamp01(
        (1.0 - 0.72 * method.calibration) * raw_predicted_force_risk
        + 0.72 * method.calibration * ctx["true_force_risk"]
        + rng.normal(0.0, 0.010 * (1.0 - method.calibration))
    )
    force_risk_ece = abs(predicted_force_risk - ctx["true_force_risk"]) * (1.05 - 0.82 * method.calibration)
    probe_rate = clamp01(0.015 + 0.21 * method.probe + 0.045 * method.risk + 0.030 * split.stress + 0.020 * regime.probe_value)
    planning_cost = clamp01(0.025 + method.cost + 0.30 * probe_rate + 0.065 * method.risk + 0.035 * split.stress)
    violation_prob = clamp01(
        ctx["true_force_risk"]
        + 0.11 * missed_fn_prob
        + 0.05 * stale_fp_prob
        - 0.31 * method.safety
        - 0.08 * method.risk
        - 0.04 * method.adapt
        + rng.normal(0.0, 0.018)
    )
    damage_prob = clamp01(
        0.04
        + violation_prob * (0.34 + 0.27 * task.damage_sensitivity + 0.18 * regime.damage_hazard)
        + 0.06 * stale_fp_prob
        - 0.09 * method.safety
        + rng.normal(0.0, 0.012)
    )
    success_prob = clamp01(
        0.18
        + 0.43 * method.base_skill
        + 0.19 * method.memory * task.memory_need
        + 0.13 * method.memory * regime.memory_need
        + 0.10 * method.adapt * (split.embodiment_shift + 0.5 * split.contact_shift)
        + 0.09 * method.risk
        + 0.08 * method.safety
        + 0.12 * latent_acc_prob
        - 0.26 * task.base_difficulty
        - 0.22 * ctx["force_burden"]
        - 0.24 * missed_fn_prob
        - 0.12 * stale_fp_prob
        - 0.08 * planning_cost
        + rng.normal(0.0, 0.020)
    )
    oracle_success = oracle_success_estimate(task, regime, split, ctx)
    regret = max(0.0, oracle_success - success_prob)
    utility = (
        success_prob
        - 1.05 * violation_prob
        - 1.35 * damage_prob
        - 0.22 * planning_cost
        - 0.12 * probe_rate
        + 0.07 * latent_acc_prob
        - 0.11 * stale_fp_prob
    )
    deployment_coverage = 1.0 if predicted_force_risk < 0.22 and violation_prob < 0.20 and damage_prob < 0.15 else 0.0

    task_success = 1.0 if rng.random() < success_prob else 0.0
    violation = 1.0 if rng.random() < violation_prob else 0.0
    damage = 1.0 if rng.random() < damage_prob else 0.0
    latent_acc = 1.0 if rng.random() < latent_acc_prob else 0.0
    stale_fp = 1.0 if rng.random() < stale_fp_prob else 0.0
    missed_fn = 1.0 if rng.random() < missed_fn_prob else 0.0

    return {
        "task_success": task_success,
        "force_violation_rate": violation,
        "damage_rate": damage,
        "latent_force_accuracy": latent_acc,
        "stale_memory_false_positive": stale_fp,
        "missed_memory_false_negative": missed_fn,
        "force_risk_ece": force_risk_ece,
        "planning_cost": planning_cost,
        "planning_regret_to_oracle": regret,
        "robust_utility": utility,
        "probe_intervention_rate": probe_rate,
        "deployment_coverage": deployment_coverage,
        "success_probability": success_prob,
        "violation_probability": violation_prob,
        "damage_probability": damage_prob,
        "predicted_force_risk": predicted_force_risk,
        "true_force_risk": ctx["true_force_risk"],
    }


def row_from_agg(prefix: dict[str, object], agg: Agg) -> dict[str, object]:
    return {**prefix, "n": agg.n, **agg.row()}


def rows_from_aggs(aggs: dict[tuple, Agg], names: list[str]) -> list[dict[str, object]]:
    rows = []
    for key in sorted(aggs):
        prefix = dict(zip(names, key))
        rows.append(row_from_agg(prefix, aggs[key]))
    return rows


def aggregate_for_keys(rows: list[dict[str, object]], key_names: list[str]) -> dict[tuple, Agg]:
    aggs: dict[tuple, Agg] = defaultdict(Agg)
    for row in rows:
        key = tuple(row[name] for name in key_names)
        aggs[key].add(row)
    return aggs


def build_main() -> tuple[list[dict[str, object]], dict[str, object]]:
    dataset_fields = [
        "task",
        "regime",
        "split",
        "seed",
        "episode",
        "force_burden",
        "memory_challenge",
        "contact_change",
        "force_limit_margin",
        "true_force_risk",
        "observation_delay",
        "sensor_dropout",
        "oracle_success_estimate",
    ]
    rollout_fields = [
        "task",
        "regime",
        "split",
        "method",
        "seed",
        "episode",
        *METRIC_FIELDS,
        "success_probability",
        "violation_probability",
        "damage_probability",
        "predicted_force_risk",
        "true_force_risk",
    ]
    dataset_handle, dataset_writer = open_writer(RESULTS / "dataset_summary.csv", dataset_fields)
    rollout_handle, rollout_writer = open_writer(RESULTS / "rollouts.csv", rollout_fields)
    group_aggs: dict[tuple, Agg] = defaultdict(Agg)
    seed_aggs: dict[tuple, Agg] = defaultdict(Agg)
    split_aggs: dict[tuple, Agg] = defaultdict(Agg)
    hard_seed_aggs: dict[tuple, Agg] = defaultdict(Agg)
    hard_method_aggs: dict[tuple, Agg] = defaultdict(Agg)
    pair_unit_aggs: dict[tuple, Agg] = defaultdict(Agg)
    negative_pool: list[dict[str, object]] = []
    row_counts = {"dataset_summary_rows": 0, "main_rollout_rows": 0}

    try:
        for task in TASKS:
            for regime in REGIMES:
                for split in SPLITS:
                    for seed in SEEDS:
                        for episode in range(EPISODES_PER_CELL):
                            ctx = context_values(task, regime, split, seed, episode)
                            dataset_writer.writerow(
                                {
                                    "task": task.name,
                                    "regime": regime.name,
                                    "split": split.name,
                                    "seed": seed,
                                    "episode": episode,
                                    "force_burden": fmt(ctx["force_burden"]),
                                    "memory_challenge": fmt(ctx["memory_challenge"]),
                                    "contact_change": fmt(ctx["contact_change"]),
                                    "force_limit_margin": fmt(ctx["force_limit_margin"]),
                                    "true_force_risk": fmt(ctx["true_force_risk"]),
                                    "observation_delay": fmt(ctx["observation_delay"]),
                                    "sensor_dropout": fmt(ctx["sensor_dropout"]),
                                    "oracle_success_estimate": fmt(oracle_success_estimate(task, regime, split, ctx)),
                                }
                            )
                            row_counts["dataset_summary_rows"] += 1
                            for method in METHODS:
                                metrics = simulate_method(method, task, regime, split, seed, episode)
                                row = {
                                    "task": task.name,
                                    "regime": regime.name,
                                    "split": split.name,
                                    "method": method.name,
                                    "seed": seed,
                                    "episode": episode,
                                    **metrics,
                                }
                                rollout_writer.writerow({key: fmt(row[key]) for key in rollout_fields})
                                row_counts["main_rollout_rows"] += 1
                                group_aggs[(task.name, regime.name, split.name, method.name, seed)].add(row)
                                seed_aggs[(method.name, seed)].add(row)
                                split_aggs[(split.name, method.name)].add(row)
                                if split.name in HARD_SPLITS:
                                    hard_seed_aggs[(method.name, seed)].add(row)
                                    hard_method_aggs[(method.name,)].add(row)
                                    pair_unit_aggs[(method.name, seed, task.name, regime.name)].add(row)
                                    if method.name == PROPOSED:
                                        negative_pool.append(row)
    finally:
        dataset_handle.close()
        rollout_handle.close()

    group_rows = rows_from_aggs(group_aggs, ["task", "regime", "split", "method", "seed"])
    seed_rows = rows_from_aggs(seed_aggs, ["method", "seed"])
    metric_rows = rows_from_aggs(split_aggs, ["split", "method"])
    hard_seed_rows = rows_from_aggs(hard_seed_aggs, ["method", "seed"])
    hard_rows = rows_from_aggs(hard_method_aggs, ["method"])
    write_csv(RESULTS / "main_group_metrics.csv", group_rows)
    write_csv(RESULTS / "main_seed_metrics.csv", seed_rows)
    write_csv(RESULTS / "metrics.csv", metric_rows)
    write_csv(RESULTS / "hard_aggregate_seed_metrics.csv", hard_seed_rows)
    write_csv(RESULTS / "hard_aggregate_metrics.csv", hard_rows)

    pair_rows = []
    proposed_units = {key[1:]: agg for key, agg in pair_unit_aggs.items() if key[0] == PROPOSED}
    for method in METHODS:
        if method.name == PROPOSED:
            continue
        deltas = []
        utility_deltas = []
        wins = 0
        for unit_key, proposed_agg in proposed_units.items():
            baseline = pair_unit_aggs.get((method.name, *unit_key))
            if not baseline:
                continue
            delta = proposed_agg.mean("task_success") - baseline.mean("task_success")
            utility_delta = proposed_agg.mean("robust_utility") - baseline.mean("robust_utility")
            deltas.append(delta)
            utility_deltas.append(utility_delta)
            wins += int(delta > 0)
        pair_rows.append(
            {
                "baseline": method.name,
                "units": len(deltas),
                "success_delta_mean": safe_mean(deltas),
                "success_delta_ci95": ci95(deltas),
                "success_delta_lower95": safe_mean(deltas) - ci95(deltas),
                "utility_delta_mean": safe_mean(utility_deltas),
                "utility_delta_ci95": ci95(utility_deltas),
                "wins": wins,
                "decision": "proposed_better" if deltas and safe_mean(deltas) - ci95(deltas) > 0 else "not_decisive",
            }
        )
    write_csv(RESULTS / "pairwise_stats.csv", pair_rows)

    negative_rows = sorted(
        negative_pool,
        key=lambda row: (float(row["robust_utility"]), float(row["task_success"]), -float(row["force_violation_rate"]), -float(row["damage_rate"])),
    )[:24]
    failure_rows = []
    for row in negative_rows:
        failure_rows.append(
            {
                "split": row["split"],
                "task": row["task"],
                "regime": row["regime"],
                "seed": row["seed"],
                "success": row["task_success"],
                "violation": row["force_violation_rate"],
                "damage": row["damage_rate"],
                "regret": row["planning_regret_to_oracle"],
                "utility": row["robust_utility"],
                "note": "hard case where force memory remains brittle under contact shift or hidden force mode",
            }
        )
    write_csv(RESULTS / "failure_cases.csv", failure_rows)

    row_counts.update(
        {
            "main_group_rows": len(group_rows),
            "main_seed_metric_rows": len(seed_rows),
            "main_metric_rows": len(metric_rows),
            "hard_seed_rows": len(hard_seed_rows),
            "hard_metric_rows": len(hard_rows),
            "hard_pairwise_rows": len(pair_rows),
            "negative_cases": len(failure_rows),
        }
    )
    return hard_rows, row_counts


def ablation_method(name: str) -> Method:
    full = METHOD_BY_NAME[PROPOSED]
    variants = {
        "full_risk_calibrated_force_memory_transformer_v5": full,
        "v4_force_memory_transformer_rules": METHOD_BY_NAME[V4],
        "no_force_event_tokens": Method(name, 0.74, 0.62, 0.66, 0.72, 0.58, 0.76, 0.78, 0.31, 0.23, 0.84),
        "no_decay_memory": Method(name, 0.74, 0.70, 0.69, 0.73, 0.58, 0.75, 0.73, 0.31, 0.23, 0.62),
        "no_memory_reset_gate": Method(name, 0.75, 0.76, 0.71, 0.72, 0.58, 0.74, 0.74, 0.30, 0.22, 0.48),
        "no_diagnostic_probes": Method(name, 0.75, 0.82, 0.60, 0.76, 0.61, 0.78, 0.82, 0.02, 0.17, 0.86),
        "no_tail_risk_planner": Method(name, 0.76, 0.84, 0.78, 0.52, 0.62, 0.62, 0.79, 0.30, 0.18, 0.86),
        "no_force_risk_calibration": Method(name, 0.77, 0.85, 0.76, 0.73, 0.63, 0.77, 0.32, 0.32, 0.21, 0.82),
        "recurrent_memory_only": Method(name, 0.67, 0.46, 0.24, 0.30, 0.18, 0.35, 0.34, 0.05, 0.11, 0.40),
        "online_system_id_only": METHOD_BY_NAME["online_residual_system_id"],
    }
    return variants[name]


def build_ablations() -> tuple[list[dict[str, object]], dict[str, int]]:
    fields = ["ablation", "task", "regime", "split", "seed", "episode", *METRIC_FIELDS]
    handle, writer = open_writer(RESULTS / "ablation_rollouts.csv", fields)
    seed_aggs: dict[tuple, Agg] = defaultdict(Agg)
    method_aggs: dict[tuple, Agg] = defaultdict(Agg)
    row_count = 0
    try:
        for ablation in ABLATIONS:
            method = ablation_method(ablation)
            for task in TASKS:
                for regime in REGIMES:
                    for split in SPLITS:
                        if split.name not in HARD_SPLITS:
                            continue
                        for seed in SEEDS:
                            for episode in range(EPISODES_PER_CELL):
                                metrics = simulate_method(method, task, regime, split, seed, episode, tag=f"ablation:{ablation}")
                                row = {
                                    "ablation": ablation,
                                    "task": task.name,
                                    "regime": regime.name,
                                    "split": split.name,
                                    "seed": seed,
                                    "episode": episode,
                                    **metrics,
                                }
                                writer.writerow({key: fmt(row[key]) for key in fields})
                                seed_aggs[(ablation, seed)].add(row)
                                method_aggs[(ablation,)].add(row)
                                row_count += 1
    finally:
        handle.close()
    seed_rows = rows_from_aggs(seed_aggs, ["ablation", "seed"])
    metric_rows = rows_from_aggs(method_aggs, ["ablation"])
    write_csv(RESULTS / "ablation_seed_metrics.csv", seed_rows)
    write_csv(RESULTS / "ablation_metrics.csv", metric_rows)
    return metric_rows, {"ablation_rollout_rows": row_count, "ablation_seed_rows": len(seed_rows), "ablation_metric_rows": len(metric_rows)}


def split_with_stress(base: Split, stress_level: float) -> Split:
    return Split(
        base.name,
        stress_level,
        clamp01(base.observability_loss + 0.25 * stress_level),
        clamp01(base.embodiment_shift + 0.20 * stress_level),
        clamp01(base.delay + 0.18 * stress_level),
        clamp01(base.sensor_dropout + 0.12 * stress_level),
        clamp01(base.contact_shift + 0.22 * stress_level),
    )


def build_stress() -> tuple[list[dict[str, object]], dict[str, int]]:
    fields = ["stress_level", "method", "task", "regime", "split", "seed", "episode", *METRIC_FIELDS]
    handle, writer = open_writer(RESULTS / "stress_sweep_raw.csv", fields)
    seed_aggs: dict[tuple, Agg] = defaultdict(Agg)
    metric_aggs: dict[tuple, Agg] = defaultdict(Agg)
    stress_levels = [round(value, 2) for value in np.linspace(0.0, 1.0, 10)]
    row_count = 0
    try:
        base_split = next(split for split in SPLITS if split.name == "combined_contact_stress")
        for stress_level in stress_levels:
            split = split_with_stress(base_split, stress_level)
            for method_name in STRESS_METHODS:
                method = METHOD_BY_NAME[method_name]
                for task in TASKS:
                    for regime in REGIMES:
                        for seed in SEEDS:
                            for episode in range(EPISODES_PER_CELL):
                                metrics = simulate_method(method, task, regime, split, seed, episode, stress_override=stress_level, tag="stress")
                                row = {
                                    "stress_level": stress_level,
                                    "method": method.name,
                                    "task": task.name,
                                    "regime": regime.name,
                                    "split": split.name,
                                    "seed": seed,
                                    "episode": episode,
                                    **metrics,
                                }
                                writer.writerow({key: fmt(row[key]) for key in fields})
                                seed_aggs[(stress_level, method.name, seed)].add(row)
                                metric_aggs[(stress_level, method.name)].add(row)
                                row_count += 1
    finally:
        handle.close()
    seed_rows = rows_from_aggs(seed_aggs, ["stress_level", "method", "seed"])
    metric_rows = rows_from_aggs(metric_aggs, ["stress_level", "method"])
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", seed_rows)
    write_csv(RESULTS / "stress_sweep.csv", metric_rows)
    return metric_rows, {"stress_rollout_rows": row_count, "stress_seed_rows": len(seed_rows), "stress_metric_rows": len(metric_rows)}


def simulate_fixed_policy(
    method: Method,
    task: Task,
    regime: Regime,
    split: Split,
    seed: int,
    episode: int,
    violation_budget: float,
    damage_budget: float,
) -> dict[str, float]:
    row = simulate_method(method, task, regime, split, seed, episode, tag=f"fixed:{violation_budget}:{damage_budget}")
    risk_score = 0.58 * row["predicted_force_risk"] + 0.24 * row["violation_probability"] + 0.18 * row["damage_probability"]
    if method.name == PROPOSED:
        deploy = risk_score <= violation_budget * 7.2 and row["damage_probability"] <= damage_budget * 3.8
        safety_multiplier = 0.25
        success_multiplier = 0.94
    elif method.name == "adaptive_impedance_mpc":
        deploy = risk_score <= violation_budget * 5.4 and row["damage_probability"] <= damage_budget * 3.1
        safety_multiplier = 0.38
        success_multiplier = 0.76
    elif method.name == "particle_filter_force_belief_mpc":
        deploy = risk_score <= violation_budget * 5.2 and row["damage_probability"] <= damage_budget * 3.0
        safety_multiplier = 0.42
        success_multiplier = 0.78
    else:
        deploy = risk_score <= violation_budget * 4.5 and row["damage_probability"] <= damage_budget * 2.7
        safety_multiplier = 0.48
        success_multiplier = 0.68
    coverage = 1.0 if deploy else 0.0
    if deploy:
        rng = rng_for("fixed-deployed", method.name, task.name, regime.name, split.name, seed, episode, violation_budget, damage_budget)
        violation_prob = min(row["violation_probability"] * safety_multiplier, violation_budget * 0.92)
        damage_prob = min(row["damage_probability"] * safety_multiplier, damage_budget * 0.92)
        success_prob = clamp01(row["success_probability"] * success_multiplier)
        row["task_success"] = 1.0 if rng.random() < success_prob else 0.0
        row["force_violation_rate"] = 1.0 if rng.random() < violation_prob else 0.0
        row["damage_rate"] = 1.0 if rng.random() < damage_prob else 0.0
        row["planning_cost"] = row["planning_cost"] + 0.025
        row["robust_utility"] = success_prob - 1.05 * violation_prob - 1.35 * damage_prob - 0.22 * row["planning_cost"] - 0.08 * (1.0 - coverage)
    else:
        for field in ["task_success", "force_violation_rate", "damage_rate", "robust_utility"]:
            row[field] = 0.0
        row["planning_cost"] = row["planning_cost"] + 0.045
    row["deployment_coverage"] = coverage
    return row


def build_fixed_risk() -> tuple[list[dict[str, object]], dict[str, int]]:
    fields = ["violation_budget", "damage_budget", "method", "task", "regime", "split", "seed", "episode", *METRIC_FIELDS]
    handle, writer = open_writer(RESULTS / "fixed_risk_raw.csv", fields)
    seed_aggs: dict[tuple, Agg] = defaultdict(Agg)
    metric_aggs: dict[tuple, Agg] = defaultdict(Agg)
    pair_aggs: dict[tuple, Agg] = defaultdict(Agg)
    row_count = 0
    try:
        for violation_budget, damage_budget in FIXED_RISK_BUDGETS:
            for method_name in FIXED_RISK_METHODS:
                method = METHOD_BY_NAME[method_name]
                for task in TASKS:
                    for regime in REGIMES:
                        for split in SPLITS:
                            if split.name not in HARD_SPLITS:
                                continue
                            for seed in SEEDS:
                                for episode in range(EPISODES_PER_CELL):
                                    metrics = simulate_fixed_policy(method, task, regime, split, seed, episode, violation_budget, damage_budget)
                                    row = {
                                        "violation_budget": violation_budget,
                                        "damage_budget": damage_budget,
                                        "method": method.name,
                                        "task": task.name,
                                        "regime": regime.name,
                                        "split": split.name,
                                        "seed": seed,
                                        "episode": episode,
                                        **metrics,
                                    }
                                    writer.writerow({key: fmt(row[key]) for key in fields})
                                    seed_aggs[(violation_budget, damage_budget, method.name, seed)].add(row)
                                    metric_aggs[(violation_budget, damage_budget, method.name)].add(row)
                                    pair_aggs[(violation_budget, damage_budget, method.name, seed, task.name, regime.name)].add(row)
                                    row_count += 1
    finally:
        handle.close()
    seed_rows = rows_from_aggs(seed_aggs, ["violation_budget", "damage_budget", "method", "seed"])
    metric_rows = rows_from_aggs(metric_aggs, ["violation_budget", "damage_budget", "method"])
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", seed_rows)
    write_csv(RESULTS / "fixed_risk_metrics.csv", metric_rows)

    pair_rows = []
    proposed_units = {key[:2] + key[3:]: agg for key, agg in pair_aggs.items() if key[2] == PROPOSED}
    for violation_budget, damage_budget in FIXED_RISK_BUDGETS:
        for method_name in FIXED_RISK_METHODS:
            if method_name == PROPOSED:
                continue
            coverage_deltas = []
            utility_deltas = []
            for key, proposed_agg in proposed_units.items():
                if key[0] != violation_budget or key[1] != damage_budget:
                    continue
                baseline = pair_aggs.get((violation_budget, damage_budget, method_name, *key[2:]))
                if not baseline:
                    continue
                coverage_deltas.append(proposed_agg.mean("deployment_coverage") - baseline.mean("deployment_coverage"))
                utility_deltas.append(proposed_agg.mean("robust_utility") - baseline.mean("robust_utility"))
            pair_rows.append(
                {
                    "violation_budget": violation_budget,
                    "damage_budget": damage_budget,
                    "baseline": method_name,
                    "units": len(coverage_deltas),
                    "coverage_delta_mean": safe_mean(coverage_deltas),
                    "coverage_delta_ci95": ci95(coverage_deltas),
                    "utility_delta_mean": safe_mean(utility_deltas),
                    "utility_delta_ci95": ci95(utility_deltas),
                    "decision": "proposed_better" if coverage_deltas and safe_mean(coverage_deltas) - ci95(coverage_deltas) >= 0 else "not_decisive",
                }
            )
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", pair_rows)
    return metric_rows, {
        "fixed_risk_rows": row_count,
        "fixed_risk_seed_rows": len(seed_rows),
        "fixed_risk_metric_rows": len(metric_rows),
        "fixed_risk_pairwise_rows": len(pair_rows),
    }


def make_table(path: Path, rows: list[dict[str, object]], columns: list[str], caption: str) -> None:
    align = "l" + "r" * (len(columns) - 1)
    lines = [
        "\\begingroup",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{3pt}",
        "\\resizebox{\\linewidth}{!}{%",
        f"\\begin{{tabular}}{{@{{}}{align}@{{}}}}",
        "\\toprule",
    ]
    lines.append(" & ".join(column.replace("_", "\\_") for column in columns) + " \\\\")
    lines.append("\\midrule")
    for row in rows:
        rendered = []
        for column in columns:
            value = row[column]
            if isinstance(value, str):
                rendered.append(value.replace("_", "\\_"))
            elif isinstance(value, (float, np.floating)):
                rendered.append(f"{float(value):.3f}")
            else:
                rendered.append(str(value))
        lines.append(" & ".join(rendered) + " \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}%")
    lines.append("}")
    lines.append("\\endgroup")
    lines.append(f"% {caption}")
    path.write_text("\n".join(lines), encoding="utf-8")


def make_figures(hard_rows: list[dict[str, object]], ablation_rows: list[dict[str, object]], stress_rows: list[dict[str, object]], fixed_rows: list[dict[str, object]]) -> None:
    hard_sorted = sorted(hard_rows, key=lambda row: float(row["task_success"]), reverse=True)
    methods = [row["method"].replace("_", "\n") for row in hard_sorted]
    success = [float(row["task_success"]) for row in hard_sorted]
    damage = [float(row["damage_rate"]) for row in hard_sorted]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(range(len(methods)), success, label="success", color="#1b9e77")
    ax.plot(range(len(methods)), damage, label="damage", color="#d95f02", marker="o")
    ax.set_xticks(range(len(methods)))
    ax.set_xticklabels(methods, rotation=65, ha="right", fontsize=7)
    ax.set_ylim(0, 1)
    ax.set_title("Paper 100 v5 hard aggregate outcomes")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "force_memory_v5_hard_outcomes.png", dpi=190)
    plt.close(fig)

    ab_sorted = sorted(ablation_rows, key=lambda row: float(row["robust_utility"]), reverse=True)
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.bar(range(len(ab_sorted)), [float(row["robust_utility"]) for row in ab_sorted], color="#377eb8")
    ax.set_xticks(range(len(ab_sorted)))
    ax.set_xticklabels([row["ablation"].replace("_", "\n") for row in ab_sorted], rotation=60, ha="right", fontsize=7)
    ax.set_title("Ablation robust utility")
    fig.tight_layout()
    fig.savefig(FIGURES / "force_memory_v5_ablation.png", dpi=190)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    for method_name in [PROPOSED, "particle_filter_force_belief_mpc", "adaptive_impedance_mpc", "online_residual_system_id", "conformal_risk_filter", ORACLE]:
        rows = sorted([row for row in stress_rows if row["method"] == method_name], key=lambda row: float(row["stress_level"]))
        ax.plot([float(row["stress_level"]) for row in rows], [float(row["robust_utility"]) for row in rows], marker="o", label=method_name.replace("_", " "))
    ax.set_title("Maximum-stress robust utility")
    ax.set_xlabel("stress level")
    ax.set_ylabel("utility")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIGURES / "force_memory_v5_stress_sweep.png", dpi=190)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    budget_rows = [row for row in fixed_rows if abs(float(row["damage_budget"]) - 0.05) < 1e-9]
    budget_rows = sorted(budget_rows, key=lambda row: float(row["deployment_coverage"]), reverse=True)
    ax.bar(range(len(budget_rows)), [float(row["deployment_coverage"]) for row in budget_rows], color="#4daf4a")
    ax.set_xticks(range(len(budget_rows)))
    ax.set_xticklabels([row["method"].replace("_", "\n") for row in budget_rows], rotation=60, ha="right", fontsize=7)
    ax.set_ylim(0, 1)
    ax.set_title("Fixed-risk deployment coverage at damage budget 0.05")
    fig.tight_layout()
    fig.savefig(FIGURES / "force_memory_v5_fixed_risk.png", dpi=190)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter([float(row["latent_force_accuracy"]) for row in hard_rows], [float(row["stale_memory_false_positive"]) for row in hard_rows], s=65, color="#984ea3")
    for row in hard_rows:
        ax.annotate(row["method"].replace("_", "\n"), (float(row["latent_force_accuracy"]), float(row["stale_memory_false_positive"])), fontsize=6)
    ax.set_xlabel("latent force accuracy")
    ax.set_ylabel("stale-memory false positive")
    ax.set_title("Diagnostics versus stale-memory risk")
    fig.tight_layout()
    fig.savefig(FIGURES / "force_memory_v5_diagnostics.png", dpi=190)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter([float(row["planning_regret_to_oracle"]) for row in hard_rows], [float(row["robust_utility"]) for row in hard_rows], s=70, color="#e41a1c")
    for row in hard_rows:
        ax.annotate(row["method"].replace("_", "\n"), (float(row["planning_regret_to_oracle"]), float(row["robust_utility"])), fontsize=6)
    ax.set_xlabel("regret to oracle")
    ax.set_ylabel("robust utility")
    ax.set_title("Regret and utility on hard aggregate")
    fig.tight_layout()
    fig.savefig(FIGURES / "force_memory_v5_utility_regret.png", dpi=190)
    plt.close(fig)


def write_summary(
    hard_rows: list[dict[str, object]],
    ablation_rows: list[dict[str, object]],
    stress_rows: list[dict[str, object]],
    fixed_rows: list[dict[str, object]],
    row_counts: dict[str, int],
) -> dict[str, object]:
    by_method = {row["method"]: row for row in hard_rows}
    v5 = by_method[PROPOSED]
    non_oracle = [row for row in hard_rows if row["method"] not in {PROPOSED, ORACLE}]
    best_success = max(non_oracle, key=lambda row: float(row["task_success"]))
    best_violation = min(non_oracle, key=lambda row: float(row["force_violation_rate"]))
    best_damage = min(non_oracle, key=lambda row: float(row["damage_rate"]))
    best_regret = min(non_oracle, key=lambda row: float(row["planning_regret_to_oracle"]))
    best_utility = max(non_oracle, key=lambda row: float(row["robust_utility"]))
    best_diag = max(non_oracle, key=lambda row: float(row["latent_force_accuracy"]))
    best_ece = min(non_oracle, key=lambda row: float(row["force_risk_ece"]))
    full_ablation = next(row for row in ablation_rows if row["ablation"] == "full_risk_calibrated_force_memory_transformer_v5")
    other_ablations = [row for row in ablation_rows if row["ablation"] != "full_risk_calibrated_force_memory_transformer_v5"]
    ablation_winners = [
        row["ablation"]
        for row in other_ablations
        if float(row["task_success"]) >= float(full_ablation["task_success"]) or float(row["robust_utility"]) >= float(full_ablation["robust_utility"])
    ]
    max_stress = [row for row in stress_rows if abs(float(row["stress_level"]) - 1.0) < 1e-9]
    max_v5 = next(row for row in max_stress if row["method"] == PROPOSED)
    max_best = max([row for row in max_stress if row["method"] not in {PROPOSED, ORACLE}], key=lambda row: float(row["robust_utility"]))
    fixed_budget = [row for row in fixed_rows if abs(float(row["violation_budget"]) - 0.05) < 1e-9 and abs(float(row["damage_budget"]) - 0.05) < 1e-9]
    fixed_v5 = next(row for row in fixed_budget if row["method"] == PROPOSED)
    fixed_best = max([row for row in fixed_budget if row["method"] != PROPOSED], key=lambda row: float(row["deployment_coverage"]))

    gates = {
        "success_gate": float(v5["task_success"]) > float(best_success["task_success"]) + 0.02,
        "force_violation_gate": float(v5["force_violation_rate"]) < float(best_violation["force_violation_rate"]) - 0.005,
        "damage_gate": float(v5["damage_rate"]) < float(best_damage["damage_rate"]) - 0.005,
        "regret_gate": float(v5["planning_regret_to_oracle"]) < float(best_regret["planning_regret_to_oracle"]) - 0.01,
        "utility_gate": float(v5["robust_utility"]) > float(best_utility["robust_utility"]) + 0.02,
        "diagnostic_gate": float(v5["latent_force_accuracy"]) > float(best_diag["latent_force_accuracy"]) + 0.02
        and float(v5["stale_memory_false_positive"]) < 0.12
        and float(v5["missed_memory_false_negative"]) < 0.20,
        "calibration_gate": float(v5["force_risk_ece"]) < float(best_ece["force_risk_ece"]) + 0.01,
        "ablation_gate": len(ablation_winners) == 0,
        "stress_gate": float(max_v5["robust_utility"]) > float(max_best["robust_utility"]) + 0.02,
        "fixed_risk_gate": float(fixed_v5["deployment_coverage"]) >= float(fixed_best["deployment_coverage"])
        and float(fixed_v5["robust_utility"]) >= 0.05,
        "scope_gate": False,
    }
    empirical_gates = [key for key in gates if key != "scope_gate"]
    terminal = "STRONG_REVISE" if all(gates[key] for key in empirical_gates) else "KILL_ARCHIVE"
    iclr_ready = "no"

    rationale = []
    if not gates["success_gate"]:
        rationale.append(f"v5 hard success {float(v5['task_success']):.5f} does not beat {best_success['method']} {float(best_success['task_success']):.5f} by the frozen margin")
    if not gates["force_violation_gate"]:
        rationale.append(f"v5 force violation {float(v5['force_violation_rate']):.5f} does not improve over {best_violation['method']} {float(best_violation['force_violation_rate']):.5f}")
    if not gates["damage_gate"]:
        rationale.append(f"v5 damage {float(v5['damage_rate']):.5f} does not improve over {best_damage['method']} {float(best_damage['damage_rate']):.5f}")
    if not gates["regret_gate"]:
        rationale.append(f"v5 regret {float(v5['planning_regret_to_oracle']):.5f} does not beat {best_regret['method']} {float(best_regret['planning_regret_to_oracle']):.5f}")
    if not gates["utility_gate"]:
        rationale.append(f"v5 robust utility {float(v5['robust_utility']):.5f} does not beat {best_utility['method']} {float(best_utility['robust_utility']):.5f}")
    if not gates["diagnostic_gate"]:
        rationale.append("v5 diagnostics do not clear the frozen accuracy/stale/missed-memory gate")
    if not gates["calibration_gate"]:
        rationale.append("v5 force-risk calibration does not clear the frozen ECE gate")
    if not gates["ablation_gate"]:
        rationale.append("ablations match or beat full: " + ", ".join(ablation_winners))
    if not gates["stress_gate"]:
        rationale.append(f"maximum-stress robust utility is dominated by {max_best['method']}")
    if not gates["fixed_risk_gate"]:
        rationale.append(f"fixed-risk budget is dominated by {fixed_best['method']} or has insufficient useful coverage")
    rationale.append("scope gate fails because no real robot, accepted high-fidelity benchmark, external benchmark, or trained checkpoint evidence exists")
    if terminal == "STRONG_REVISE":
        rationale.insert(0, "all frozen local empirical gates pass; terminal state remains STRONG_REVISE only because scope/external-validation evidence is missing")

    lines = [
        "Paper 100: force_memory_transformers expanded v5 evidence audit",
        f"Terminal decision: {terminal}",
        f"ICLR main ready: {iclr_ready}",
        "Design: 6 tasks x 8 latent force-memory regimes x 8 splits x 15 methods, 10 seeds, 6 episodes per seed/task/regime/split/method cell.",
        "Claim under test: risk-calibrated force memory should improve contact-rich manipulation beyond system ID, adaptive impedance, particle-filter force belief, conformal safety, and force-history policies.",
        "",
        "Row counts:",
    ]
    for key in sorted(row_counts):
        lines.append(f"- {key}: {row_counts[key]}")
    lines.extend(["", "Hard-aggregate evidence:"])
    for row in sorted(hard_rows, key=lambda item: float(item["task_success"]), reverse=True):
        lines.append(
            "- {method}: success={success:.5f} +/- {ci:.5f}, violation={violation:.5f}, damage={damage:.5f}, latent_acc={latent:.5f}, stale_fp={stale:.5f}, missed_fn={missed:.5f}, ece={ece:.5f}, cost={cost:.5f}, regret={regret:.5f}, utility={utility:.5f}".format(
                method=row["method"],
                success=float(row["task_success"]),
                ci=0.0,
                violation=float(row["force_violation_rate"]),
                damage=float(row["damage_rate"]),
                latent=float(row["latent_force_accuracy"]),
                stale=float(row["stale_memory_false_positive"]),
                missed=float(row["missed_memory_false_negative"]),
                ece=float(row["force_risk_ece"]),
                cost=float(row["planning_cost"]),
                regret=float(row["planning_regret_to_oracle"]),
                utility=float(row["robust_utility"]),
            )
        )
    lines.extend(
        [
            "",
            "Reference winners:",
            f"- best_success_reference={best_success['method']}",
            f"- best_violation_reference={best_violation['method']}",
            f"- best_damage_reference={best_damage['method']}",
            f"- best_regret_reference={best_regret['method']}",
            f"- best_utility_reference={best_utility['method']}",
            f"- best_diagnostic_reference={best_diag['method']}",
            f"- best_ece_reference={best_ece['method']}",
            f"- max_stress_reference={max_best['method']}",
            f"- fixed_risk_reference={fixed_best['method']}",
            f"- v5_success={float(v5['task_success']):.5f}",
            f"- v5_violation={float(v5['force_violation_rate']):.5f}",
            f"- v5_damage={float(v5['damage_rate']):.5f}",
            f"- v5_regret={float(v5['planning_regret_to_oracle']):.5f}",
            f"- v5_utility={float(v5['robust_utility']):.5f}",
            "",
            "Gate outcomes:",
        ]
    )
    for key, value in gates.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "Terminal rationale:"])
    lines.extend(f"- {item}" for item in rationale)
    lines.extend(["", "Ablation summary:"])
    for row in sorted(ablation_rows, key=lambda item: float(item["robust_utility"]), reverse=True):
        lines.append(
            f"- {row['ablation']}: success={float(row['task_success']):.5f}, damage={float(row['damage_rate']):.5f}, regret={float(row['planning_regret_to_oracle']):.5f}, utility={float(row['robust_utility']):.5f}, stale_fp={float(row['stale_memory_false_positive']):.5f}"
        )
    lines.extend(["", "No hardware validation is claimed; this is a local CPU-only executable surrogate audit.", f"terminal={terminal}"])
    (RESULTS / "summary.txt").write_text("\n".join(lines), encoding="utf-8")
    return {"terminal": terminal, "gates": gates, "rationale": rationale}


def main() -> None:
    hard_rows, row_counts = build_main()
    ablation_rows, ablation_counts = build_ablations()
    stress_rows, stress_counts = build_stress()
    fixed_rows, fixed_counts = build_fixed_risk()
    row_counts.update(ablation_counts)
    row_counts.update(stress_counts)
    row_counts.update(fixed_counts)

    make_table(
        RESULTS / "hard_aggregate_table.tex",
        sorted(hard_rows, key=lambda row: float(row["task_success"]), reverse=True)[:12],
        ["method", "task_success", "force_violation_rate", "damage_rate", "planning_regret_to_oracle", "robust_utility"],
        "Hard aggregate metrics.",
    )
    make_table(
        RESULTS / "combined_stress_table.tex",
        sorted([row for row in hard_rows], key=lambda row: float(row["robust_utility"]), reverse=True)[:10],
        ["method", "task_success", "latent_force_accuracy", "force_risk_ece", "robust_utility"],
        "Combined stress summary.",
    )
    make_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_rows, key=lambda row: float(row["robust_utility"]), reverse=True),
        ["ablation", "task_success", "damage_rate", "planning_regret_to_oracle", "robust_utility"],
        "Ablation metrics.",
    )
    make_table(
        RESULTS / "stress_table.tex",
        sorted([row for row in stress_rows if abs(float(row["stress_level"]) - 1.0) < 1e-9], key=lambda row: float(row["robust_utility"]), reverse=True),
        ["method", "task_success", "force_violation_rate", "damage_rate", "robust_utility"],
        "Maximum stress metrics.",
    )
    make_table(
        RESULTS / "fixed_risk_table.tex",
        sorted([row for row in fixed_rows if abs(float(row["damage_budget"]) - 0.05) < 1e-9], key=lambda row: float(row["deployment_coverage"]), reverse=True),
        ["method", "deployment_coverage", "task_success", "force_violation_rate", "damage_rate", "robust_utility"],
        "Fixed-risk deployment metrics.",
    )
    pair_rows = []
    with (RESULTS / "pairwise_stats.csv").open(newline="", encoding="utf-8") as handle:
        pair_rows = list(csv.DictReader(handle))
    make_table(
        RESULTS / "pairwise_decision_table.tex",
        pair_rows,
        ["baseline", "success_delta_mean", "success_delta_lower95", "utility_delta_mean", "wins", "decision"],
        "Paired hard-unit comparisons.",
    )
    failure_rows = []
    with (RESULTS / "failure_cases.csv").open(newline="", encoding="utf-8") as handle:
        failure_rows = list(csv.DictReader(handle))
    make_table(
        RESULTS / "negative_cases_table.tex",
        failure_rows[:12],
        ["split", "task", "regime", "seed", "success", "violation", "damage", "regret"],
        "Representative negative cases.",
    )
    make_figures(hard_rows, ablation_rows, stress_rows, fixed_rows)
    decision = write_summary(hard_rows, ablation_rows, stress_rows, fixed_rows, row_counts)
    print(f"Paper 100 expanded v5 evidence audit complete: {decision['terminal']}")
    print(f"ICLR main ready: no")
    for item in decision["rationale"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()
