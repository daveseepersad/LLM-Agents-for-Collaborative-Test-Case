"""Offline tests for the configurable multi-agent loop (max_iterations and target_coverage)."""

import pytest
import yaml

from src import experiment_runner
from src.agents.multi_agent_collaborative.MultiAgentCollaborativeGraph import (
    MultiAgentCollaborativeGraph,
)
from src.agents.multi_agent_competitive.MultiAgentCompetitiveGraph import (
    END,
    MultiAgentCompetitiveGraph,
)
from src.ConfigManager import ConfigManager

INPUT_FILE = "data/input_code/d02_stack.py"


def collaborative(**loop_settings):
    return MultiAgentCollaborativeGraph(INPUT_FILE, "unused", None, None, verbose=False, **loop_settings)


def competitive(**loop_settings):
    return MultiAgentCompetitiveGraph(INPUT_FILE, "unused", None, None, None, verbose=False, **loop_settings)


def executed_state(graph, coverage, iterations=1, failed=0):
    return {**graph.initial_state, "coverage_percent": coverage, "iterations": iterations, "n_failed_tests": failed}


@pytest.mark.parametrize("build", [collaborative, competitive], ids=["collaborative", "competitive"])
def test_defaults_match_previous_hardcoded_loop(build, repo_cwd):
    graph = build()

    assert graph.initial_state["max_iterations"] == 5
    assert graph.target_coverage == 100


@pytest.mark.parametrize(
    ("build", "replan", "done"),
    [(collaborative, "replan", "end"), (competitive, "planner", END)],
    ids=["collaborative", "competitive"],
)
def test_target_coverage_controls_replanning(build, replan, done, repo_cwd):
    strict, lenient = build(), build(target_coverage=97)

    assert strict._route_to(executed_state(strict, coverage=98)) == replan
    assert lenient._route_to(executed_state(lenient, coverage=98)) == done
    assert lenient._route_to(executed_state(lenient, coverage=96)) == replan


@pytest.mark.parametrize(
    ("build", "done"), [(collaborative, "end"), (competitive, END)], ids=["collaborative", "competitive"]
)
def test_max_iterations_caps_the_loop(build, done, repo_cwd):
    graph = build(max_iterations=10)

    assert graph.initial_state["max_iterations"] == 10
    assert graph._route_to(executed_state(graph, coverage=50, iterations=10)) != done
    assert graph._route_to(executed_state(graph, coverage=50, iterations=11)) == done


@pytest.mark.parametrize(
    ("strategy", "runner", "models"),
    [
        ("collaborative_agents", "run_collaborative_agents", {"planner_model": "p", "generator_model": "g"}),
        (
            "competitive_agents",
            "run_competitive_agents",
            {"planner_model": "p", "generator_model_1": "g1", "generator_model_2": "g2"},
        ),
    ],
    ids=["collaborative", "competitive"],
)
@pytest.mark.parametrize(
    ("agent", "expected"),
    [({}, {"max_iterations": 5, "target_coverage": 100}), ({"max_iterations": 10, "target_coverage": 97}, None)],
    ids=["defaults", "configured"],
)
def test_run_experiment_passes_loop_settings(strategy, runner, models, agent, expected, repo_cwd, tmp_path, monkeypatch):
    captured = {}

    def fake_runner(**kwargs):
        captured.update(kwargs)
        return {"coverage_percent": 100, "n_passed_tests": 1, "n_failed_tests": 0, "failed_tests_infos": "", "total_tokens": 1}

    monkeypatch.setattr(experiment_runner, runner, fake_runner)
    monkeypatch.setattr(experiment_runner, "get_mutation_metrics", lambda **kwargs: None)
    config = tmp_path / "experiment.yaml"
    config.write_text(
        yaml.safe_dump(
            {
                "experiment": {"type": strategy, "input_path": INPUT_FILE},
                "llm": {"temperature": 0.2, **models},
                "agent": agent,
            }
        )
    )

    experiment_runner.run_experiment(ConfigManager(str(config)))

    expected = expected or agent
    assert {key: captured[key] for key in expected} == expected
