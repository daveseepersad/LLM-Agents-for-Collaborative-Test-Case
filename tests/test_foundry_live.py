"""Opt-in live checks against Azure AI Foundry deployments.

Run them before a long experiment to verify the endpoint, the Entra ID login (or
API key), the deployments, and that the agents' prompts, token accounting and
pytest loop work with the chosen models::

    RUN_FOUNDRY_LIVE_TESTS=1 python -m pytest tests/test_foundry_live.py -v

``FOUNDRY_LIVE_DEPLOYMENTS`` (comma separated, default ``gpt-5-mini``) selects the
deployments and ``FOUNDRY_LIVE_REASONING_EFFORT`` (default: the model's default) the
reasoning effort; set it to the value of your experiment config. A ``groq:`` prefix runs
the checks against a Groq model instead, e.g. ``groq:openai/gpt-oss-20b``.
"""

import json
import os
from concurrent.futures import ThreadPoolExecutor

import pytest
from langchain_core.prompts import ChatPromptTemplate

from src.agents.llm_factory import get_llm
from src.agents.multi_agent_collaborative.MultiAgentCollaborativeGraph import (
    MultiAgentCollaborativeGraph,
)
from src.agents.single_agent.SingleAgentChain import SingleAgentChain

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_FOUNDRY_LIVE_TESTS") != "1", reason="set RUN_FOUNDRY_LIVE_TESTS=1 to call Azure AI Foundry"
)

DEPLOYMENTS = [name.strip() for name in os.getenv("FOUNDRY_LIVE_DEPLOYMENTS", "gpt-5-mini").split(",") if name.strip()]
REASONING_EFFORT = os.getenv("FOUNDRY_LIVE_REASONING_EFFORT") or None
INPUT_FILE = "data/input_code/d02_stack.py"

# Same message structure as the agents' prompts: system, few-shot pair, real input.
ECHO_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", "Reply with the requested word only."),
        ("human", "Word: example"),
        ("ai", "example"),
        ("human", "Word: {word}"),
    ]
)


def foundry_llm(deployment):
    # The original experiments use temperature 0.2; it is dropped for models that only support the default.
    return get_llm(provider="azure_foundry", model_name=deployment, temperature=0.2, reasoning_effort=REASONING_EFFORT)


def total_tokens(response):
    # Same token accounting as the agents.
    return response.response_metadata.get("token_usage", {}).get("total_tokens", 0)


@pytest.mark.parametrize("deployment", DEPLOYMENTS)
def test_completion_reports_token_usage(deployment):
    response = (ECHO_PROMPT | foundry_llm(deployment)).invoke({"word": "pong"})

    assert "pong" in response.content.lower()
    assert total_tokens(response) > 0


@pytest.mark.parametrize("deployment", DEPLOYMENTS)
def test_concurrent_requests(deployment):
    # The competitive graph runs its two developers concurrently.
    chain = ECHO_PROMPT | foundry_llm(deployment)
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda word: chain.invoke({"word": word}), ["alpha", "beta"]))

    assert ["alpha" in responses[0].content.lower(), "beta" in responses[1].content.lower()] == [True, True]


@pytest.mark.parametrize("deployment", DEPLOYMENTS)
def test_planner_returns_json_test_plan(deployment, repo_cwd):
    graph = MultiAgentCollaborativeGraph(INPUT_FILE, "unused", foundry_llm(deployment), None, verbose=False)

    update = graph._plan_node(graph.initial_state)

    plan_text = update["test_plan"]
    plan = json.loads(plan_text[plan_text.index("[") : plan_text.rindex("]") + 1])
    assert isinstance(plan, list) and plan
    assert update["total_tokens"] > 0


@pytest.mark.parametrize("deployment", DEPLOYMENTS)
def test_single_agent_generates_passing_tests(deployment, repo_cwd):
    metrics = SingleAgentChain(INPUT_FILE, "unused", foundry_llm(deployment))._feed_the_chain()

    assert metrics["error"] == ""
    assert metrics["n_passed_tests"] > 0
    assert metrics["coverage_percent"] > 0
    assert metrics["total_tokens"] > 0
