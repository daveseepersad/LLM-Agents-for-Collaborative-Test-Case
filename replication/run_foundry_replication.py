#!/usr/bin/env python3
"""Replicate the paper's experiment grid on Azure AI Foundry.

Re-runs the 28 configurations in ``configs/experiments`` (Coppola et al., "Do Multi-agent
LLMs Improve Test Generation?", SEAA 2026) with each Groq model mapped to an Azure AI
Foundry deployment, and writes one results file per experiment in the same format as
``results/``.

The archived results in ``results/`` were produced by three code versions, which this
script reproduces by default (``--protocol archive``):

* Era A, 2026-01-18..23: modules d01-d05; multi-agent loops ran up to ``max_iterations=10``
  and re-planned while coverage was below 100%.
* Era B, 2026-01-26/27: ``d06_complex_logic`` was run later and appended to every
  multi-agent results file, with ``max_iterations=5``; the collaborative loop then re-planned
  only below 97% coverage.
* Era C, 2026-01-31: five collaborative configurations were re-run on all modules with
  the era B settings.

``--protocol head`` instead runs every module with the current defaults (5 iterations, 100%).

Each pass runs in an isolated copy of the repository (the pytest and mutmut steps use
the working directory), so passes run in parallel.

A mapping target with a provider prefix runs that model elsewhere, e.g.
``--map openai/gpt-oss-20b=groq:openai/gpt-oss-20b`` keeps the paper's gpt-oss-20b on Groq.

Usage:
    python replication/run_foundry_replication.py --out replication/foundry/rep1 --workers 10
    python replication/run_foundry_replication.py --only single_gptoss20B --map openai/gpt-oss-20b=gpt-5-nano
    python replication/run_foundry_replication.py --out replication/groq/pilot --only single_gptoss20B \\
        --map openai/gpt-oss-20b=groq:openai/gpt-oss-20b --workers 1 --log-llm-calls
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import yaml

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_ERROR = 2

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "configs" / "experiments"
CALL_LOG_SCRIPT = Path(__file__).resolve().parent / "llm_call_log.py"
MODULES = sorted(path.name for path in (REPO_ROOT / "data" / "input_code").glob("*.py"))
LATE_MODULE = "d06_complex_logic.py"
MODEL_KEYS = ("model", "planner_model", "generator_model", "generator_model_1", "generator_model_2")

# Groq model ids used by the paper -> Azure AI Foundry deployment names. gpt-oss-20b has no
# serverless Foundry deployment and Llama-4-Scout is a Marketplace offer, so the two small
# models use the closest available models that can perform every agent role the archive
# shows the originals performing (see replication/README.md).
DEFAULT_MODEL_MAP = {
    "openai/gpt-oss-120b": "gpt-oss-120b",
    "llama-3.3-70b-versatile": "Llama-3.3-70B-Instruct",
    "openai/gpt-oss-20b": "gpt-5-nano",
    "meta-llama/llama-4-scout-17b-16e-instruct": "Llama-4-Maverick-17B-128E-Instruct-FP8",
}

# Collaborative configurations whose archived results were all produced on 2026-01-31 (era C).
ERA_C_CONFIGS = {
    "collaborative_gptoss120B_llamaScout17B",
    "collaborative_gptoss20B_llama70B",
    "collaborative_llama70B_gptoss20B",
    "collaborative_llamaScout17B_gptoss120B",
    "collaborative_llamaScout17B_llama70B",
}

# Top-level repository content that is not needed to run an experiment.
COPY_EXCLUDES = {".git", ".venv", "results", "research", "report", "report_img", "plots", "replication", "tests"}
CACHE_NAMES = {"__pycache__", ".pytest_cache", ".ruff_cache", ".mutmut-cache", ".coverage"}

logger = logging.getLogger("replication")


@dataclass
class Pass:
    experiment: str
    name: str
    modules: list[str]
    agent: dict = field(default_factory=dict)


def plan_passes(experiment: str, strategy: str, protocol: str) -> list[Pass]:
    """Split an experiment into passes with the loop settings of the requested protocol."""
    if strategy == "single_agent":
        return [Pass(experiment, "all", MODULES)]
    if protocol == "head":
        return [Pass(experiment, "all", MODULES, {"max_iterations": 5, "target_coverage": 100})]

    late = {"max_iterations": 5, "target_coverage": 97 if strategy == "collaborative_agents" else 100}
    if experiment in ERA_C_CONFIGS:
        return [Pass(experiment, "all", MODULES, late)]
    early_modules = [module for module in MODULES if module != LATE_MODULE]
    return [
        Pass(experiment, "a", early_modules, {"max_iterations": 10, "target_coverage": 100}),
        Pass(experiment, "b", [LATE_MODULE], late),
    ]


def foundry_config(original: dict, model_map: dict[str, str], agent: dict) -> dict:
    """Return the original experiment config with Foundry deployments and the pass loop settings."""
    llm = {key: value for key, value in original["llm"].items() if key not in MODEL_KEYS}
    llm["provider"] = "azure_foundry"
    for key in MODEL_KEYS:
        if key in original["llm"]:
            llm[key] = model_map[original["llm"][key]]
    config = {"experiment": {**original["experiment"], "input_path": "data/input_code"}, "llm": llm}
    if agent:
        config["agent"] = {**original.get("agent", {}), **agent}
    return config


def _ignore_for_copy(directory: str, names: list[str]) -> list[str]:
    at_root = Path(directory) == REPO_ROOT
    in_data = Path(directory) == REPO_ROOT / "data"
    return [
        name
        for name in names
        if (at_root and name in COPY_EXCLUDES) or name in CACHE_NAMES or (in_data and name == "output_tests")
    ]


def prepare_workspace(work_dir: Path, run_pass: Pass, config: dict) -> Path:
    """Copy the repository, keep only the pass modules, and write the pass config."""
    # Workspaces hold a copy of .env with the API keys, so keep them private to this user.
    work_dir.mkdir(parents=True, exist_ok=True)
    if work_dir.stat().st_uid == os.getuid():
        work_dir.chmod(0o700)
    workspace = work_dir / f"{run_pass.experiment}__{run_pass.name}"
    if workspace.exists():
        shutil.rmtree(workspace)
    shutil.copytree(REPO_ROOT, workspace, ignore=_ignore_for_copy)
    if (workspace / ".env").exists():
        (workspace / ".env").chmod(0o600)
    for module in (workspace / "data" / "input_code").glob("*.py"):
        if module.name not in run_pass.modules:
            module.unlink()
    config_path = workspace / "configs" / "experiments" / f"{run_pass.experiment}.yaml"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False))
    return workspace


def run_pass_in_workspace(workspace: Path, run_pass: Pass, timeout: int, log_llm_calls: bool = False) -> dict:
    env = os.environ.copy()
    # mutmut launches `pytest` from PATH, so this interpreter's environment must come first.
    env["PATH"] = f"{Path(sys.executable).parent}{os.pathsep}{env.get('PATH', '')}"
    config = f"configs/experiments/{run_pass.experiment}.yaml"
    command = [sys.executable, "-m", "src.experiment_runner", "--config", config]
    if log_llm_calls:
        shutil.copy2(CALL_LOG_SCRIPT, workspace / CALL_LOG_SCRIPT.name)
        command = [sys.executable, CALL_LOG_SCRIPT.name, "--config", config]
    started = time.monotonic()
    with (workspace / "run.log").open("w", encoding="utf-8") as log:
        completed = subprocess.run(
            command, cwd=workspace, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=timeout, check=False
        )
    elapsed = round(time.monotonic() - started)
    result_files = sorted((workspace / "results").glob(f"{run_pass.experiment}_*.json"))
    if completed.returncode != 0 or not result_files:
        raise RuntimeError(f"exit code {completed.returncode}; see {workspace / 'run.log'}")
    return {"data": json.loads(result_files[-1].read_text()), "elapsed_seconds": elapsed, "workspace": workspace}


def merge_passes(experiment: str, passes: list[Pass], outcomes: dict[str, dict], out_dir: Path, meta: dict) -> Path:
    """Write one results file for the experiment and collect its test suites and logs."""
    first = outcomes[passes[0].name]["data"]
    results = sorted(
        (item for run_pass in passes for item in outcomes[run_pass.name]["data"]["results"]), key=lambda item: item["file"]
    )
    # Local time, like the run ids of src/ConfigManager.py.
    timestamp = datetime.now().isoformat(timespec="seconds").replace(":", "-")  # noqa: DTZ005
    merged = {
        "run_id": f"{experiment}_{timestamp}",
        "experiment_name": experiment,
        "timestamp": timestamp,
        "temperature": first["temperature"],
        "llm": first.get("llm"),
        "replication": {
            **meta,
            "passes": [
                {
                    "name": run_pass.name,
                    "modules": run_pass.modules,
                    "agent": run_pass.agent,
                    "run_id": outcomes[run_pass.name]["data"]["run_id"],
                    "elapsed_seconds": outcomes[run_pass.name]["elapsed_seconds"],
                }
                for run_pass in passes
            ],
        },
        "results": results,
    }
    (out_dir / "results").mkdir(parents=True, exist_ok=True)
    result_path = out_dir / "results" / f"{merged['run_id']}.json"
    result_path.write_text(json.dumps(merged, indent=4))

    tests_dir = out_dir / "output_tests" / experiment
    logs_dir = out_dir / "logs"
    if tests_dir.exists():
        shutil.rmtree(tests_dir)
    tests_dir.mkdir(parents=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    for run_pass in passes:
        workspace = outcomes[run_pass.name]["workspace"]
        for test_file in (workspace / "data" / "output_tests").glob("*/test_*.py"):
            shutil.copy2(test_file, tests_dir / test_file.name)
        shutil.copy2(workspace / "run.log", logs_dir / f"{experiment}__{run_pass.name}.log")
        call_log = workspace / "llm_calls.jsonl"
        if call_log.exists():
            (out_dir / "llm_calls").mkdir(exist_ok=True)
            shutil.copy2(call_log, out_dir / "llm_calls" / f"{experiment}__{run_pass.name}.jsonl")
    return result_path


def summarize(results: list[dict]) -> str:
    metrics = [item.get("metrics") or {} for item in results]
    errors = sum(item.get("status") != "success" for item in results)

    def mean(key: str) -> str:
        values = [m[key] for m in metrics if m.get(key) is not None]
        return f"{sum(values) / len(values):.1f}" if values else "n/a"

    return f"cov={mean('coverage_percent')} mut={mean('mutation_score_percent')} tok={mean('total_tokens')} errors={errors}"


def warn_if_night(timezone: str | None) -> None:
    """d06_complex_logic changes behaviour between 00:00 and 06:00 local time (a deliberate trap)."""
    if timezone:
        os.environ["TZ"] = timezone
        time.tzset()
    if datetime.now().hour < 6:  # noqa: DTZ005 - the module under test reads the local hour
        logger.warning(
            "Local time is between 00:00 and 06:00: d06_complex_logic takes its night-time branch, so "
            "tests written for daytime fail. Use --timezone to evaluate at daytime, like the other runs."
        )


def model_host(model: str) -> str:
    """Provider that serves a mapped model: its ``provider:`` prefix, else Azure AI Foundry."""
    prefix, separator, _ = model.partition(":")
    return prefix if separator else "azure_foundry"


def parse_mapping(values: list[str]) -> dict[str, str]:
    mapping = {}
    for value in values:
        source, separator, target = value.partition("=")
        if not separator or not source or not target:
            raise ValueError(f"--map expects <groq-model>=<deployment>, got '{value}'")
        mapping[source] = target
    return mapping


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Replicate the paper's experiment grid on Azure AI Foundry.")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "replication" / "foundry" / "rep1", help="Output directory (one per run of the grid)")
    parser.add_argument("--work-dir", type=Path, default=Path("/tmp/foundry_replication_work"), help="Workspace directory")
    parser.add_argument("--workers", type=int, default=8, help="Passes to run in parallel")
    parser.add_argument("--protocol", choices=["archive", "head"], default="archive", help="Loop settings to use")
    parser.add_argument("--only", nargs="*", default=None, help="Experiment names to run (default: all 28)")
    parser.add_argument("--map", nargs="*", default=[], help="Override model mappings: <groq-model>=<deployment>")
    parser.add_argument("--force", action="store_true", help="Re-run experiments that already have results")
    parser.add_argument("--timeout", type=int, default=4 * 3600, help="Timeout per pass in seconds")
    parser.add_argument(
        "--timezone", default=None,
        help="TZ for the experiment processes, e.g. Asia/Tokyo; d06 behaves differently from 00:00 to 06:00",
    )
    parser.add_argument(
        "--log-llm-calls", action="store_true",
        help="Log every LLM call (tokens, finish reason, rate-limit errors) to <out>/llm_calls/",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    warn_if_night(args.timezone)
    model_map = {**DEFAULT_MODEL_MAP, **parse_mapping(args.map)}
    # The paper's grid: every config whose models are all Groq models of the paper.
    configs = {}
    for path in sorted(CONFIG_DIR.glob("*.yaml")):
        config = yaml.safe_load(path.read_text())
        if all(config["llm"].get(key) in (None, *DEFAULT_MODEL_MAP) for key in MODEL_KEYS):
            configs[path.stem] = config
    selected = args.only or sorted(configs)
    unknown = sorted(set(selected) - set(configs))
    if unknown:
        logger.error("Unknown experiments: %s", ", ".join(unknown))
        return EXIT_ERROR

    done = {path.name.rsplit("_", 1)[0] for path in (args.out / "results").glob("*.json")}
    todo = [name for name in selected if args.force or name not in done]
    logger.info("Model map: %s", model_map)
    logger.info("%d experiments selected, %d to run (protocol=%s)", len(selected), len(todo), args.protocol)

    plans = {name: plan_passes(name, configs[name]["experiment"]["type"], args.protocol) for name in todo}
    tasks = [
        (run_pass, prepare_workspace(args.work_dir, run_pass, foundry_config(configs[name], model_map, run_pass.agent)))
        for name, passes in plans.items()
        for run_pass in passes
    ]
    # Longest passes first: competitive, then collaborative, then single agent.
    order = {"competitive_agents": 0, "collaborative_agents": 1, "single_agent": 2}
    tasks.sort(key=lambda task: (order[configs[task[0].experiment]["experiment"]["type"]], -len(task[0].modules)))

    outcomes: dict[str, dict[str, dict]] = {name: {} for name in plans}
    failed: set[str] = set()
    lock = threading.Lock()
    used_models = {model_map[configs[name]["llm"][key]] for name in todo for key in MODEL_KEYS if key in configs[name]["llm"]}
    meta = {
        "protocol": args.protocol,
        "model_map": model_map,
        "host": "+".join(sorted({model_host(model) for model in used_models})) or "azure_foundry",
        "timezone": os.environ.get("TZ"),
    }

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(run_pass_in_workspace, ws, run_pass, args.timeout, args.log_llm_calls): run_pass
            for run_pass, ws in tasks
        }
        for future in as_completed(futures):
            run_pass = futures[future]
            label = f"{run_pass.experiment}[{run_pass.name}]"
            try:
                outcome = future.result()
            except Exception as error:  # noqa: BLE001 - report every failed pass and keep running the others
                logger.error("FAILED %s: %s", label, error)
                failed.add(run_pass.experiment)
                continue
            logger.info("done %s in %ss: %s", label, outcome["elapsed_seconds"], summarize(outcome["data"]["results"]))
            with lock:
                outcomes[run_pass.experiment][run_pass.name] = outcome
                passes = plans[run_pass.experiment]
                if len(outcomes[run_pass.experiment]) == len(passes) and run_pass.experiment not in failed:
                    path = merge_passes(run_pass.experiment, passes, outcomes[run_pass.experiment], args.out, meta)
                    merged = json.loads(path.read_text())
                    logger.info("MERGED %s -> %s: %s", run_pass.experiment, path.name, summarize(merged["results"]))

    if failed:
        logger.error("%d experiments failed: %s", len(failed), ", ".join(sorted(failed)))
        return EXIT_FAILURE
    return EXIT_SUCCESS


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
    try:
        return run(create_parser().parse_args())
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return EXIT_ERROR


if __name__ == "__main__":
    sys.exit(main())
