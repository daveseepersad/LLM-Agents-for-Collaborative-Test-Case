#!/usr/bin/env python3
"""Reproduce the paper's Figures 3-5 and compare result sets against them.

Figures 3, 4 and 5 of Coppola et al. ("Do Multi-agent LLMs Improve Test Generation?",
SEAA 2026) show line coverage, mutation score and token usage averaged over every
module result (d01-d06) of all experiments in each configuration (Strong, Planner+,
Worker+, Weak) and architecture (single, collaborative, competitive). Experiments are
classified from their names with ``results_plot.classify_experiment``, as in the repository.

For every ``--source LABEL=RESULTS_DIR`` the script writes paper-style figures, and with
two or more sources it adds side-by-side comparison figures, a CSV of cell means, and a
markdown summary that checks the paper's RQ1-RQ3 findings for each source.

Usage:
    python replication/paper_figures.py \
        --source "Paper (Groq archive)=results" \
        --source "Replication (Foundry)=replication/foundry/results" \
        --out replication/figures
"""

from __future__ import annotations

import argparse
import glob
import json
import logging
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from results_plot import classify_experiment

EXIT_SUCCESS = 0
EXIT_ERROR = 2

CONFIGURATIONS = {"strong": "Strong", "strong_planner": "Planner+", "strong_worker": "Worker+", "weak": "Weak"}
ARCHITECTURES = ["single", "collaborative", "competitive"]
# Cells of the paper's figures: Single-Agent has no Planner+ or Worker+ configuration.
PAPER_CELLS = len(CONFIGURATIONS) * len(ARCHITECTURES) - 2
METRICS = {
    "coverage": ("Coverage by Architecture and Configuration", "Average Coverage (%)"),
    "mutation": ("Mutation Score by Architecture and Configuration", "Average Mutation Score (%)"),
    "tokens": ("Token Usage by Architecture and Configuration", "Average Tokens Used"),
}

logger = logging.getLogger("paper_figures")


def load_results(pattern: str) -> pd.DataFrame:
    """One row per module result in every results directory matching ``pattern``.

    A glob such as ``replication/foundry/rep*/results`` loads several runs of the grid;
    each directory becomes one ``run``.
    """
    directories = [Path(match) for match in sorted(glob.glob(pattern))] if glob.has_magic(pattern) else [Path(pattern)]
    rows = []
    for directory in directories:
        for path in sorted(directory.glob("*.json")):
            data = json.loads(path.read_text())
            architecture, strength = classify_experiment(data["experiment_name"])
            if architecture is None or strength not in CONFIGURATIONS:
                logger.warning("Skipping unclassified experiment %s", data["experiment_name"])
                continue
            for item in data["results"]:
                metrics = item.get("metrics") or {}
                rows.append(
                    {
                        "run": str(directory),
                        "experiment": data["experiment_name"],
                        "architecture": architecture,
                        "configuration": CONFIGURATIONS[strength],
                        "file": item["file"],
                        "status": item.get("status"),
                        "coverage": metrics.get("coverage_percent"),
                        "mutation": metrics.get("mutation_score_percent"),
                        "tokens": metrics.get("total_tokens"),
                        "iterations": metrics.get("iterations"),
                    }
                )
    return pd.DataFrame(rows)


def cell_means(results: pd.DataFrame, metric: str) -> pd.DataFrame:
    """Mean of a metric per configuration (rows) and architecture (columns), as in the paper.

    Like the paper, the mean is taken over all module results of all runs in a cell.
    """
    table = results.groupby(["configuration", "architecture"])[metric].mean().unstack()
    return table.reindex(index=list(CONFIGURATIONS.values()), columns=ARCHITECTURES)


def run_spread(results: pd.DataFrame, metric: str) -> tuple[pd.DataFrame, pd.DataFrame] | None:
    """Lowest and highest per-run cell means, or None for a single run."""
    if results["run"].nunique() < 2:
        return None
    per_run = [cell_means(frame, metric) for _, frame in results.groupby("run")]
    stacked = pd.concat(per_run, keys=range(len(per_run)))
    return stacked.groupby(level=1).min().reindex(per_run[0].index), stacked.groupby(level=1).max().reindex(per_run[0].index)


def _draw_bars(ax: plt.Axes, table: pd.DataFrame, title: str, ylabel: str, spread=None) -> None:
    width = 0.25
    positions = range(len(table.index))
    for offset, architecture in enumerate(ARCHITECTURES):
        values = table[architecture]
        yerr = None
        if spread is not None:
            low, high = spread
            yerr = [(values - low[architecture]).clip(lower=0), (high[architecture] - values).clip(lower=0)]
        ax.bar(
            [p + (offset - 1) * width for p in positions], values, width, label=architecture, color=f"C{offset}",
            yerr=yerr, capsize=3 if yerr is not None else 0, error_kw={"elinewidth": 1, "ecolor": "black"},
        )
    ax.set_xticks(list(positions), table.index)
    ax.set_title(title)
    ax.set_xlabel("Configuration")
    ax.set_ylabel(ylabel)


def plot_paper_figure(table: pd.DataFrame, metric: str, out_path: Path, subtitle: str | None = None, spread=None) -> None:
    title, ylabel = METRICS[metric]
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    _draw_bars(ax, table, title if subtitle is None else f"{title}\n{subtitle}", ylabel, spread)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_comparison(tables: dict[str, pd.DataFrame], metric: str, out_path: Path, spreads: dict | None = None) -> None:
    title, ylabel = METRICS[metric]
    spreads = spreads or {}
    fig, axes = plt.subplots(1, len(tables), figsize=(6.4 * len(tables), 4.8), sharey=True)
    for ax, (label, table) in zip(axes, tables.items()):
        _draw_bars(ax, table, label, ylabel, spreads.get(label))
        for container in ax.containers:
            if hasattr(container, "patches"):
                heights = [bar.get_height() for bar in container]
                labels = ["" if pd.isna(height) else f"{height:.{0 if metric == 'tokens' else 1}f}" for height in heights]
                ax.bar_label(container, labels=labels, fontsize=7, padding=2)
    axes[0].legend(loc="upper center", bbox_to_anchor=(0.5 * len(tables), -0.15), ncol=3)
    fig.suptitle(title if not any(spreads.values()) else f"{title} (error bars: range of per-run means)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def check_findings(tables: dict[str, pd.DataFrame]) -> list[tuple[str, str, bool]]:
    """Evaluate the paper's RQ1-RQ3 findings on one result set's cell means."""
    cov, mut, tok = tables["coverage"], tables["mutation"], tables["tokens"]
    multi = ["collaborative", "competitive"]
    ends = ["Strong", "Weak"]
    collab_cov = cov["collaborative"]
    comp_best = [config for config in cov.index if mut.loc[config, multi + ["single"]].idxmax() == "competitive"]
    # Token ratio of each multi-agent architecture to the Single-Agent baseline with the same models.
    token_ratios = tok.loc[ends, multi].div(tok.loc[ends, "single"], axis=0)
    gaps = (cov - mut).stack().dropna()
    checks = [
        ("RQ1", "Competitive coverage is near-complete (>= 99%) in every configuration",
         f"min {cov['competitive'].min():.1f}%", bool(cov["competitive"].min() >= 99)),
        ("RQ1", "Multi-agent coverage >= Single-Agent coverage (Strong, Weak)",
         ", ".join(f"{c}: {cov.loc[c, 'single']:.1f} vs {cov.loc[c, multi].min():.1f}" for c in ends),
         bool((cov.loc[ends, multi].min(axis=1) >= cov.loc[ends, "single"]).all())),
        ("RQ1", "Competitive >= Collaborative coverage in every configuration",
         ", ".join(f"{c}: {cov.loc[c, 'collaborative']:.1f}/{cov.loc[c, 'competitive']:.1f}" for c in cov.index),
         bool((cov["competitive"] >= cov["collaborative"]).all())),
        ("RQ1", "Single-Agent coverage drops with the Weak configuration",
         f"Strong {cov.loc['Strong', 'single']:.1f} vs Weak {cov.loc['Weak', 'single']:.1f}",
         bool(cov.loc["Weak", "single"] < cov.loc["Strong", "single"])),
        ("RQ1", "Collaborative coverage is lowest in Worker+",
         f"Worker+ {collab_cov['Worker+']:.1f}, min {collab_cov.idxmin()} {collab_cov.min():.1f}",
         bool(collab_cov.idxmin() == "Worker+")),
        ("RQ2", "Mutation scores are well below coverage (every cell at least 15 points lower)",
         f"smallest gap {gaps.min():.1f} points", bool((gaps >= 15).all())),
        ("RQ2", "Competitive has the highest mutation score in most configurations (>= 3 of 4)",
         f"{len(comp_best)} of 4 ({', '.join(comp_best) or 'none'})", len(comp_best) >= 3),
        ("RQ2", "Multi-agent mutation gains over Single-Agent are limited (< 10 points, Strong and Weak)",
         ", ".join(f"{c}: +{mut.loc[c, multi].max() - mut.loc[c, 'single']:.1f}" for c in ends),
         bool(((mut.loc[ends, multi].max(axis=1) - mut.loc[ends, "single"]) < 10).all())),
        ("RQ3", "Competitive uses the most tokens in every configuration",
         ", ".join(f"{c}: {tok.loc[c].idxmax()}" for c in tok.index),
         bool((tok.idxmax(axis=1) == "competitive").all())),
        ("RQ3", "Multi-agent uses several times the Single-Agent tokens with the same models (>= 3x, Strong and Weak)",
         f"{token_ratios.min().min():.1f}x to {token_ratios.max().max():.1f}x", bool((token_ratios >= 3).all().all())),
        ("RQ3", "Single-Agent with Weak models uses more tokens than with Strong models",
         f"Strong {tok.loc['Strong', 'single']:.0f} vs Weak {tok.loc['Weak', 'single']:.0f}",
         bool(tok.loc["Weak", "single"] > tok.loc["Strong", "single"])),
    ]
    return [(f"{rq}: {text}", value, ok) for rq, text, value, ok in checks]


def coverage_distribution(results: pd.DataFrame) -> pd.DataFrame:
    """Share of module results per coverage band and architecture, pooled over runs."""
    bands = pd.cut(
        results["coverage"], bins=[-1, 0, 59, 89, 99, 100], labels=["0%", "1-59%", "60-89%", "90-99%", "100%"]
    )
    table = pd.crosstab(results["architecture"], bands, normalize="index").mul(100)
    table = table.reindex(index=ARCHITECTURES, columns=["100%", "90-99%", "60-89%", "1-59%", "0%"], fill_value=0)
    table.insert(0, "module results", results.groupby("architecture").size().reindex(ARCHITECTURES))
    table.index.name = "architecture"
    return table


def consistency_report(tables: dict[str, dict], spreads: dict[str, dict]) -> list[str]:
    """For each single-run source, mark the cells that fall inside the range of a multi-run source."""
    lines = []
    singles = [label for label, spread in spreads.items() if all(value is None for value in spread.values())]
    multis = [label for label in spreads if label not in singles]
    for single in singles:
        for multi in multis:
            lines += ["", f"## {single} within the run-to-run range of {multi}", ""]
            for metric in METRICS:
                low, high = spreads[multi][metric]
                value = tables[single][metric]
                inside = (value >= low) & (value <= high)
                delta = value - tables[multi][metric]
                digits = 0 if metric == "tokens" else 1
                text = delta.map(lambda v, d=digits: "" if pd.isna(v) else f"{v:+,.{d}f}").astype(str)
                marks = text.where(~inside | delta.isna(), text + " (in range)").where(delta.notna(), "")
                count = int(inside.sum().sum())
                total = int(delta.notna().sum().sum())
                marks.index.name = f"{metric}: paper minus replication"
                lines += [f"{METRICS[metric][0]}: {count} of {total} cells in range.", "", markdown_text_table(marks), ""]
    return lines


def markdown_table(frame: pd.DataFrame, digits: int) -> str:
    return markdown_text_table(frame.map(lambda value: "" if pd.isna(value) else f"{value:,.{digits}f}"))


def markdown_text_table(frame: pd.DataFrame) -> str:
    header = "| " + " | ".join([frame.index.name or "", *map(str, frame.columns)]) + " |"
    rule = "|" + "---|" * (len(frame.columns) + 1)
    lines = [header, rule]
    for index, row in frame.iterrows():
        lines.append("| " + " | ".join([str(index), *map(str, row)]) + " |")
    return "\n".join(lines)


def slug(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


def parse_source(value: str) -> tuple[str, str]:
    label, separator, pattern = value.partition("=")
    if not separator:
        raise argparse.ArgumentTypeError(f"--source expects LABEL=RESULTS_DIR_OR_GLOB, got '{value}'")
    return label, pattern


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Reproduce the paper's Figures 3-5 and compare result sets.")
    parser.add_argument(
        "--source", type=parse_source, action="append", required=True,
        help="LABEL=RESULTS_DIR, or LABEL=GLOB matching one results directory per run",
    )
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "replication" / "figures", help="Output directory")
    return parser


def run(args: argparse.Namespace) -> int:
    args.out.mkdir(parents=True, exist_ok=True)
    tables: dict[str, dict[str, pd.DataFrame]] = {}
    spreads: dict[str, dict] = {}
    results_by_source: dict[str, pd.DataFrame] = {}
    report = ["# Paper figures and findings", ""]
    rows = []
    for label, pattern in args.source:
        results = load_results(pattern)
        if results.empty:
            logger.error("No classified results in %s", pattern)
            return EXIT_ERROR
        results_by_source[label] = results
        errors = int((results["status"] != "success").sum())
        counts = results.groupby(["configuration", "architecture"]).experiment.nunique().unstack()
        tables[label] = {metric: cell_means(results, metric) for metric in METRICS}
        spreads[label] = {metric: run_spread(results, metric) for metric in METRICS}
        for metric, table in tables[label].items():
            plot_paper_figure(table, metric, args.out / f"{slug(label)}_{metric}.png", label, spreads[label][metric])
            rows.append(table.stack().dropna().rename("value").reset_index().assign(source=label, metric=metric))
        report += [
            f"## {label}",
            "",
            (
                f"`{pattern}`: {results['run'].nunique()} run(s), {results.experiment.nunique()} experiments, "
                f"{len(results)} module results, {errors} errors, "
                f"{int(results['mutation'].isna().sum())} missing mutation scores."
            ),
            "",
            "Experiments per cell:",
            "",
            markdown_table(counts.reindex(index=list(CONFIGURATIONS.values()), columns=ARCHITECTURES), 0),
            "",
        ]
        for metric, table in tables[label].items():
            digits = 0 if metric == "tokens" else 1
            report += [f"### {METRICS[metric][0]}", "", markdown_table(table, digits), ""]
            if spreads[label][metric] is not None:
                low, high = spreads[label][metric]

                def fmt(value, digits=digits):
                    return f"{value:,.{digits}f}"

                spread_table = low.map(fmt).astype(str) + " to " + high.map(fmt).astype(str)
                spread_table = spread_table.where(low.notna(), "")
                report += ["Range of per-run means:", "", markdown_text_table(spread_table), ""]
        distribution = coverage_distribution(results).dropna(subset=["module results"])
        distribution_text = distribution.map(lambda value: f"{value:.1f}")
        distribution_text["module results"] = distribution["module results"].map(lambda value: f"{int(value)}")
        report += [
            "### Coverage of module results (% of module results per band)",
            "",
            markdown_text_table(distribution_text),
            "",
        ]

    # The findings compare cells across the grid, so they are only evaluated on complete grids.
    checks = {
        label: check_findings(metric_tables)
        for label, metric_tables in tables.items()
        if int(metric_tables["coverage"].notna().sum().sum()) == PAPER_CELLS
    }
    if checks:
        report += ["## Findings of the paper", "", "| Finding | " + " | ".join(tables) + " |", "|---" * (len(tables) + 1) + "|"]
        for index, (finding, _, _) in enumerate(next(iter(checks.values()))):
            cells = [
                f"{'yes' if checks[label][index][2] else 'no'} ({checks[label][index][1]})" if label in checks
                else "n/a (incomplete grid)"
                for label in tables
            ]
            report.append(f"| {finding} | " + " | ".join(cells) + " |")

    if len(tables) > 1:
        report += consistency_report(tables, spreads)
        for metric in METRICS:
            plot_comparison(
                {label: t[metric] for label, t in tables.items()},
                metric,
                args.out / f"compare_{metric}.png",
                {label: s[metric] for label, s in spreads.items()},
            )
        per_experiment = pd.concat(
            {
                label: frame.groupby("experiment")[["coverage", "mutation", "tokens", "iterations"]].mean()
                for label, frame in results_by_source.items()
            },
            axis=1,
        )
        per_experiment.to_csv(args.out / "per_experiment.csv")
        report += ["", "## Per experiment (mean over modules and runs)", ""]
        for metric in ("coverage", "mutation", "tokens"):
            frame = per_experiment.xs(metric, axis=1, level=1)
            frame.index.name = metric
            report += [markdown_table(frame, 0 if metric == "tokens" else 1), ""]
    pd.concat(rows).to_csv(args.out / "cell_means.csv", index=False)
    (args.out / "summary.md").write_text("\n".join(report) + "\n")
    print("\n".join(report))
    return EXIT_SUCCESS


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    return run(create_parser().parse_args())


if __name__ == "__main__":
    sys.exit(main())
