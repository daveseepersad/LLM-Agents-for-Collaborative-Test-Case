"""Offline tests for the replication tooling in replication/ (paper figures and run plan)."""

import json
import sys
from concurrent.futures import ThreadPoolExecutor

import groq
import httpx
import pandas as pd
import pytest
import yaml
from langchain_core.tracers import context as tracer_context

from tests.conftest import REPO_ROOT
from tests.test_llm_factory import FakeGroq, groq_completion

sys.path.insert(0, str(REPO_ROOT / "replication"))
import llm_call_log
import paper_figures
import run_foundry_replication as replication

# Bar heights of the paper's Figures 3-5 (coverage %, mutation score %, tokens).
PAPER_FIGURES = {
    "coverage": {
        "Strong": (97.2, 98.6, 99.9), "Planner+": (None, 97.7, 99.7), "Worker+": (None, 94.9, 99.7), "Weak": (91.4, 97.2, 99.8),
    },
    "mutation": {
        "Strong": (66.5, 67.4, 75.4), "Planner+": (None, 70.8, 66.6), "Worker+": (None, 64.4, 72.9), "Weak": (64.9, 67.3, 71.0),
    },
    "tokens": {
        "Strong": (2200, 12121, 18476), "Planner+": (None, 16043, 29168), "Worker+": (None, 17064, 35150),
        "Weak": (4155, 23270, 28721),
    },
}


@pytest.fixture(scope="module")
def archive():
    return paper_figures.load_results(str(REPO_ROOT / "results"))


@pytest.mark.parametrize("metric", PAPER_FIGURES)
def test_archive_reproduces_paper_figures(archive, metric):
    table = paper_figures.cell_means(archive, metric)
    tolerance = 1 if metric == "tokens" else 0.1

    for configuration, values in PAPER_FIGURES[metric].items():
        for architecture, expected in zip(paper_figures.ARCHITECTURES, values):
            actual = table.loc[configuration, architecture]
            if expected is None:
                # Planner+ and Worker+ are undefined for the Single-Agent baseline
                assert pd.isna(actual)
            else:
                assert actual == pytest.approx(expected, abs=tolerance), (configuration, architecture)


def test_paper_findings_hold_on_archive(archive):
    tables = {metric: paper_figures.cell_means(archive, metric) for metric in paper_figures.METRICS}

    failed = [finding for finding, _, ok in paper_figures.check_findings(tables) if not ok]

    assert failed == []


def test_single_run_has_no_spread(archive):
    assert paper_figures.run_spread(archive, "coverage") is None


def test_partial_result_set_is_compared_per_experiment(tmp_path):
    partial = tmp_path / "partial"
    partial.mkdir()
    for name in ("single_gptoss20B", "collaborative_gptoss120B_gptoss120B"):
        source = next((REPO_ROOT / "results").glob(f"{name}_2026-*.json"))
        (partial / source.name).write_text(source.read_text())
    args = paper_figures.create_parser().parse_args(
        ["--source", f"Paper={REPO_ROOT / 'results'}", "--source", f"Partial={partial}", "--out", str(tmp_path / "out")]
    )

    assert paper_figures.run(args) == paper_figures.EXIT_SUCCESS

    summary = (tmp_path / "out" / "summary.md").read_text()
    assert "| RQ1: Competitive coverage is near-complete (>= 99%) in every configuration | yes" in summary
    assert "n/a (incomplete grid)" in summary
    per_experiment = pd.read_csv(tmp_path / "out" / "per_experiment.csv", header=[0, 1], index_col=0)
    assert per_experiment.loc["single_gptoss20B", ("Partial", "coverage")] == per_experiment.loc["single_gptoss20B", ("Paper", "coverage")]
    assert pd.isna(per_experiment.loc["single_gptoss120B", ("Partial", "coverage")])


def test_era_c_configs_match_archive_dates():
    rerun_on_jan_31 = {
        json.loads(path.read_text())["experiment_name"]
        for path in (REPO_ROOT / "results").glob("*.json")
        if json.loads(path.read_text())["timestamp"].startswith("2026-01-31")
    }

    assert rerun_on_jan_31 == replication.ERA_C_CONFIGS


@pytest.mark.parametrize(
    ("experiment", "strategy", "expected"),
    [
        ("single_gptoss120B", "single_agent", [("all", 6, {})]),
        (
            "collaborative_gptoss120B_gptoss120B",
            "collaborative_agents",
            [("a", 5, {"max_iterations": 10, "target_coverage": 100}), ("b", 1, {"max_iterations": 5, "target_coverage": 97})],
        ),
        ("collaborative_gptoss20B_llama70B", "collaborative_agents", [("all", 6, {"max_iterations": 5, "target_coverage": 97})]),
        (
            "competitive_gptoss120B_gptoss120B_llama70B",
            "competitive_agents",
            [("a", 5, {"max_iterations": 10, "target_coverage": 100}), ("b", 1, {"max_iterations": 5, "target_coverage": 100})],
        ),
    ],
)
def test_archive_protocol_passes(experiment, strategy, expected):
    passes = replication.plan_passes(experiment, strategy, "archive")

    assert [(p.name, len(p.modules), p.agent) for p in passes] == expected
    assert sorted(module for p in passes for module in p.modules) == replication.MODULES


def test_head_protocol_uses_current_defaults():
    passes = replication.plan_passes("competitive_gptoss120B_gptoss120B_llama70B", "competitive_agents", "head")

    assert [(p.name, len(p.modules), p.agent) for p in passes] == [("all", 6, {"max_iterations": 5, "target_coverage": 100})]


@pytest.mark.parametrize("config_file", sorted((REPO_ROOT / "configs" / "experiments").glob("*.yaml")), ids=lambda p: p.stem)
def test_paper_configs_map_to_foundry(config_file):
    original = yaml.safe_load(config_file.read_text())
    if not all(original["llm"].get(key) in (None, *replication.DEFAULT_MODEL_MAP) for key in replication.MODEL_KEYS):
        pytest.skip("not part of the paper's grid")

    config = replication.foundry_config(original, replication.DEFAULT_MODEL_MAP, {"max_iterations": 10})

    assert config["llm"]["provider"] == "azure_foundry"
    assert config["llm"]["temperature"] == original["llm"]["temperature"] == 0.2
    for key in replication.MODEL_KEYS:
        if key in original["llm"]:
            assert config["llm"][key] == replication.DEFAULT_MODEL_MAP[original["llm"][key]]
    assert config["agent"]["max_iterations"] == 10


@pytest.mark.parametrize(("model", "host"), [("gpt-5-nano", "azure_foundry"), ("groq:openai/gpt-oss-20b", "groq")])
def test_model_host(model, host):
    assert replication.model_host(model) == host


def test_groq_mapping_routes_the_role_to_groq():
    original = yaml.safe_load((REPO_ROOT / "configs" / "experiments" / "collaborative_gptoss120B_gptoss20B.yaml").read_text())
    model_map = {**replication.DEFAULT_MODEL_MAP, **replication.parse_mapping(["openai/gpt-oss-20b=groq:openai/gpt-oss-20b"])}

    config = replication.foundry_config(original, model_map, {})

    assert config["llm"]["planner_model"] == "groq:openai/gpt-oss-20b"
    assert config["llm"]["generator_model"] == "gpt-oss-120b"


def test_workspace_keeps_the_api_keys_private(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    (repo / "data" / "input_code").mkdir(parents=True)
    (repo / "configs" / "experiments").mkdir(parents=True)
    for module in ("d01_bank.py", "d02_stack.py"):
        (repo / "data" / "input_code" / module).write_text("")
    (repo / ".env").write_text("GROQ_API_KEY=secret\n")
    (repo / ".env").chmod(0o644)
    monkeypatch.setattr(replication, "REPO_ROOT", repo)
    work_dir = tmp_path / "work"
    work_dir.mkdir(mode=0o755)

    workspace = replication.prepare_workspace(work_dir, replication.Pass("single_gptoss20B", "all", ["d01_bank.py"]), {"llm": {}})

    assert work_dir.stat().st_mode & 0o777 == 0o700
    assert (workspace / ".env").stat().st_mode & 0o777 == 0o600
    assert sorted(path.name for path in (workspace / "data" / "input_code").iterdir()) == ["d01_bank.py"]
    assert yaml.safe_load((workspace / "configs" / "experiments" / "single_gptoss20B.yaml").read_text()) == {"llm": {}}


@pytest.fixture
def call_log(tmp_path):
    hooks = tracer_context._configure_hooks
    registered = list(hooks)
    yield llm_call_log.enable(tmp_path / "llm_calls.jsonl")
    hooks[:] = registered


def test_llm_call_log_records_every_call(call_log):
    message = "Request too large for model `openai/gpt-oss-20b` in organization `org_01abcdefghijklmnopqrstuvwx`"
    rejected = httpx.Response(400, json={"error": {"message": message, "type": "invalid_request_error"}})
    llm = FakeGroq(groq_completion(), rejected).model()

    llm.invoke("hi")
    # The competitive graph's developers run in worker threads.
    with ThreadPoolExecutor(max_workers=1) as pool, pytest.raises(groq.BadRequestError):
        pool.submit(llm.invoke, "hi").result()

    success, failure = [json.loads(line) for line in call_log.path.read_text().splitlines()]
    assert success["model"] == "openai/gpt-oss-20b"
    assert (success["prompt_tokens"], success["completion_tokens"], success["total_tokens"]) == (5, 1, 6)
    assert success["finish_reason"] == "stop"
    assert success["end"] >= success["start"]
    assert failure["status_code"] == 400
    assert failure["error"].startswith("BadRequestError")
    assert "organization `org_<redacted>`" in failure["error"]
