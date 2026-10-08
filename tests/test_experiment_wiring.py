"""Offline tests that the LLM provider settings flow from the YAML configs to the agents and results."""

import json

import pytest
import yaml
from langchain_groq import ChatGroq

from src import experiment_runner
from src.agents.llm_factory import (
    AZURE_FOUNDRY,
    GROQ,
    FoundryChatModel,
    describe_llm_config,
    get_llm,
    llm_options_from_config,
    normalize_provider,
)
from src.agents.multi_agent_collaborative import multi_agent_collaborative_runner
from src.agents.multi_agent_competitive import multi_agent_competitive_runner
from src.agents.single_agent import single_agent_runner
from src.ConfigManager import ConfigManager
from src.tracker import save_run_metrics
from tests.conftest import REPO_ROOT

CONFIG_FILES = sorted((REPO_ROOT / "configs" / "experiments").glob("*.yaml"))
GPT5_MINI_CONFIGS = ["single_gpt5mini", "collaborative_gpt5mini_gpt5mini", "competitive_gpt5mini_gpt5mini_gpt5mini"]
REQUIRED_MODEL_KEYS = {
    "single_agent": {"model"},
    "collaborative_agents": {"planner_model", "generator_model"},
    "competitive_agents": {"planner_model", "generator_model_1", "generator_model_2"},
}
OPTIONS = {"reasoning_effort": "low", "max_retries": 3}


class FakeAgent:
    def __init__(self, *args, **kwargs):
        pass

    def invoke(self):
        return {"coverage_percent": 100}


@pytest.fixture
def recorded_llms(monkeypatch):
    calls = []

    def fake_get_llm(**kwargs):
        calls.append(kwargs)
        return object()

    for module, agent_class in [
        (single_agent_runner, "SingleAgentChain"),
        (multi_agent_collaborative_runner, "MultiAgentCollaborativeGraph"),
        (multi_agent_competitive_runner, "MultiAgentCompetitiveGraph"),
    ]:
        monkeypatch.setattr(module, "get_llm", fake_get_llm)
        monkeypatch.setattr(module, agent_class, FakeAgent)
    return calls


def write_config(tmp_path, llm):
    path = tmp_path / "experiment.yaml"
    experiment = {"type": "single_agent", "input_path": "data/input_code/d02_stack.py"}
    path.write_text(yaml.safe_dump({"experiment": experiment, "llm": llm}))
    return str(path)


@pytest.mark.parametrize(
    ("run", "models"),
    [
        (lambda **kw: single_agent_runner.run_single_agent("in.py", "out", model="m", **kw), ["m"]),
        (lambda **kw: multi_agent_collaborative_runner.run_collaborative_agents("in.py", "out", "p", "g", **kw), ["p", "g"]),
        (
            lambda **kw: multi_agent_competitive_runner.run_competitive_agents("in.py", "out", "p", "g1", "g2", **kw),
            ["p", "g1", "g2"],
        ),
    ],
    ids=["single", "collaborative", "competitive"],
)
def test_runners_forward_provider_and_options(recorded_llms, run, models):
    metrics = run(temperature=0.2, provider=AZURE_FOUNDRY, llm_options=OPTIONS)

    assert metrics["coverage_percent"] == 100
    assert recorded_llms == [
        {"provider": AZURE_FOUNDRY, "model_name": model, "temperature": 0.2, **OPTIONS} for model in models
    ]


def test_runners_default_to_factory_provider(recorded_llms):
    single_agent_runner.run_single_agent("in.py", "out", model="m")

    assert recorded_llms == [{"provider": None, "model_name": "m", "temperature": 0}]


def test_run_experiment_passes_llm_settings_from_config(repo_cwd, tmp_path, monkeypatch):
    captured = {}

    def fake_run_single_agent(**kwargs):
        captured.update(kwargs)
        return {"coverage_percent": 100, "n_passed_tests": 1, "n_failed_tests": 0, "failed_tests_infos": "", "total_tokens": 10}

    monkeypatch.setattr(experiment_runner, "run_single_agent", fake_run_single_agent)
    monkeypatch.setattr(experiment_runner, "get_mutation_metrics", lambda **kwargs: None)
    config = write_config(
        tmp_path, {"provider": "foundry", "model": "gpt-5-mini", "temperature": 1.0, "reasoning_effort": "low"}
    )

    results = experiment_runner.run_experiment(ConfigManager(config))

    assert [result["status"] for result in results] == ["success"]
    assert captured["provider"] == AZURE_FOUNDRY
    assert captured["llm_options"] == {"reasoning_effort": "low"}
    assert captured["model"] == "gpt-5-mini"
    assert captured["temperature"] == 1.0


def test_run_experiment_rejects_unknown_provider(repo_cwd, tmp_path):
    config = write_config(tmp_path, {"provider": "bedrock", "model": "m", "temperature": 0.2})

    with pytest.raises(ValueError, match="Unknown LLM provider"):
        experiment_runner.run_experiment(ConfigManager(config))


@pytest.mark.parametrize("config_file", CONFIG_FILES, ids=lambda path: path.stem)
def test_experiment_configs_build_their_llms(config_file, repo_cwd, groq_env, azure_env):
    cfg = ConfigManager(str(config_file))
    llm_config = cfg.config["llm"]
    described = describe_llm_config(llm_config)

    assert REQUIRED_MODEL_KEYS[cfg.get("experiment", "type")] <= set(described["models"])
    expected_provider = AZURE_FOUNDRY if config_file.stem in GPT5_MINI_CONFIGS else GROQ
    assert described["provider"] == expected_provider

    provider = normalize_provider(llm_config.get("provider"))
    options = llm_options_from_config(llm_config)
    for key, role in described["models"].items():
        llm = get_llm(provider=provider, model_name=llm_config[key], temperature=llm_config["temperature"], **options)
        assert isinstance(llm, ChatGroq if role["provider"] == GROQ else FoundryChatModel)


@pytest.mark.parametrize("name", GPT5_MINI_CONFIGS)
def test_gpt5_mini_configs_use_default_temperature(name, repo_cwd):
    llm_config = ConfigManager(f"configs/experiments/{name}.yaml").config["llm"]
    roles = describe_llm_config(llm_config)["models"].values()

    assert {role["model"] for role in roles} == {"gpt-5-mini"}
    assert all(role["temperature"] is None for role in roles)
    assert llm_config["temperature"] == 1.0


class FakeConfigManager:
    run_id = "exp_2026-01-01T00-00-00"
    experiment_name = "exp"

    def __init__(self, llm):
        self.config = {"llm": llm}

    def get(self, section, key):
        return self.config.get(section, {}).get(key)


def saved_metrics(tmp_path, llm):
    (tmp_path / "results").mkdir()
    save_run_metrics(FakeConfigManager(llm), [{"file": "d02_stack.py", "status": "success", "metrics": {}}])
    return json.loads((tmp_path / "results" / f"{FakeConfigManager.run_id}.json").read_text())


def test_save_run_metrics_records_llm_metadata(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    saved = saved_metrics(tmp_path, {"provider": "azure_foundry", "model": "gpt-5-mini", "temperature": 1.0})

    assert saved["temperature"] == 1.0
    assert saved["llm"]["models"]["model"] == {"provider": AZURE_FOUNDRY, "model": "gpt-5-mini", "temperature": None}
    assert saved["results"][0]["file"] == "d02_stack.py"


def test_save_run_metrics_keeps_results_when_metadata_fails(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    saved = saved_metrics(tmp_path, {"provider": "bedrock", "model": "m", "temperature": 0.2})

    assert "Unknown LLM provider" in saved["llm"]["error"]
    assert saved["results"][0]["status"] == "success"
