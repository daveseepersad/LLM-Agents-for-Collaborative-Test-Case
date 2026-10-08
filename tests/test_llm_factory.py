"""Offline tests for the Groq / Azure AI Foundry LLM factory (no network access)."""

import asyncio
import functools
import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

import groq
import httpx
import openai
import openai._base_client as openai_base_client
import pytest
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq

from src.agents import llm_factory
from src.agents.llm_factory import (
    AZURE_FOUNDRY,
    DEFAULT_AZURE_API_VERSION,
    DEFAULT_AZURE_MAX_RETRIES,
    DEFAULT_AZURE_TIMEOUT,
    DEFAULT_GROQ_TIMEOUT,
    GROQ,
    FoundryChatModel,
    GroqChatModel,
    describe_llm_config,
    effective_temperature,
    get_llm,
    llm_options_from_config,
    normalize_provider,
    resolve_model,
    supports_temperature,
    total_tokens,
)
from tests.conftest import FAKE_AZURE_ENDPOINT

# The HTTP library used by the installed openai SDK (httpx2 for openai>=3, httpx before).
httpx_lib = getattr(openai_base_client, "httpx2", None) or openai_base_client.httpx

COMPLETION = {
    "id": "chatcmpl-test",
    "object": "chat.completion",
    "created": 1_700_000_000,
    "model": "custom-reasoner",
    "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": "pong"}}],
    "usage": {"prompt_tokens": 5, "completion_tokens": 1, "total_tokens": 6},
}
TEMPERATURE_REJECTED = {
    "error": {
        "message": "Unsupported value: 'temperature' does not support 0.2 with this model. "
        "Only the default (1) value is supported.",
        "type": "invalid_request_error",
        "param": "temperature",
        "code": "unsupported_value",
    }
}
OTHER_BAD_REQUESTS = [
    {"error": {"message": "Invalid 'messages'.", "type": "invalid_request_error", "param": "messages", "code": None}},
    {
        "error": {
            "message": "Invalid type for 'temperature': expected a decimal, but got a string instead.",
            "type": "invalid_request_error",
            "param": "temperature",
            "code": "invalid_type",
        }
    },
]


def request_payload(llm):
    return llm._get_request_payload([HumanMessage(content="hi")])


class FakeDeployment:
    """Mock HTTP transport for one Azure deployment that records each request."""

    def __init__(self, reject_temperature=False, error_body=None, barrier=None, omit_usage=False):
        self.reject_temperature = reject_temperature
        self.error_body = error_body
        self.barrier = barrier
        self.omit_usage = omit_usage
        self.requests = []
        self.raw_requests = []

    def __call__(self, request):
        body = json.loads(request.content)
        self.requests.append(body)
        self.raw_requests.append(request)
        if self.barrier is not None and "temperature" in body:
            self.barrier.wait()
        if self.error_body is not None:
            return httpx_lib.Response(400, json=self.error_body)
        if self.reject_temperature and "temperature" in body:
            return httpx_lib.Response(400, json=TEMPERATURE_REJECTED)
        if self.omit_usage:
            return httpx_lib.Response(200, json={key: value for key, value in COMPLETION.items() if key != "usage"})
        return httpx_lib.Response(200, json=COMPLETION)

    def model(self, deployment="custom-reasoner", temperature=0.2):
        return FoundryChatModel(
            azure_endpoint=FAKE_AZURE_ENDPOINT,
            azure_deployment=deployment,
            model=deployment,
            api_version=DEFAULT_AZURE_API_VERSION,
            api_key="test-azure-key",
            temperature=temperature,
            max_retries=0,
            http_client=httpx_lib.Client(transport=httpx_lib.MockTransport(self)),
            http_async_client=httpx_lib.AsyncClient(transport=httpx_lib.MockTransport(self)),
        )


# --- provider and model resolution -------------------------------------------------


@pytest.mark.parametrize(
    ("provider", "expected"),
    [
        (None, GROQ),
        ("groq", GROQ),
        ("azure_foundry", AZURE_FOUNDRY),
        ("Azure-Foundry", AZURE_FOUNDRY),
        ("azure", AZURE_FOUNDRY),
        ("foundry", AZURE_FOUNDRY),
        ("azure_openai", AZURE_FOUNDRY),
    ],
)
def test_normalize_provider(provider, expected):
    assert normalize_provider(provider) == expected


def test_normalize_provider_rejects_unknown_provider():
    with pytest.raises(ValueError, match="Unknown LLM provider 'bedrock'"):
        normalize_provider("bedrock")


@pytest.mark.parametrize(
    ("model_name", "provider", "expected"),
    [
        ("llama-3.3-70b-versatile", None, (GROQ, "llama-3.3-70b-versatile")),
        ("openai/gpt-oss-120b", "groq", (GROQ, "openai/gpt-oss-120b")),
        ("meta-llama/llama-4-scout-17b-16e-instruct", "groq", (GROQ, "meta-llama/llama-4-scout-17b-16e-instruct")),
        ("gpt-5-mini", "azure_foundry", (AZURE_FOUNDRY, "gpt-5-mini")),
        ("azure_foundry:gpt-5-mini", "groq", (AZURE_FOUNDRY, "gpt-5-mini")),
        ("foundry:gpt-oss-120b", None, (AZURE_FOUNDRY, "gpt-oss-120b")),
        ("Azure: Llama-3.3-70B-Instruct", None, (AZURE_FOUNDRY, "Llama-3.3-70B-Instruct")),
        ("groq:llama-3.3-70b-versatile", "azure_foundry", (GROQ, "llama-3.3-70b-versatile")),
        ("not-a-provider:model", "groq", (GROQ, "not-a-provider:model")),
    ],
)
def test_resolve_model(model_name, provider, expected):
    assert resolve_model(model_name, provider) == expected


@pytest.mark.parametrize(("model_name", "message"), [("", "model name is required"), ("azure:", "Missing model name")])
def test_resolve_model_rejects_missing_model(model_name, message):
    with pytest.raises(ValueError, match=message):
        resolve_model(model_name)


# --- temperature support -----------------------------------------------------------


@pytest.mark.parametrize(
    ("model_name", "provider", "reasoning_effort", "expected"),
    [
        ("gpt-5-mini", AZURE_FOUNDRY, None, False),
        ("gpt-5-mini", AZURE_FOUNDRY, "medium", False),
        ("GPT-5.4", AZURE_FOUNDRY, None, False),
        ("gpt-5.4", AZURE_FOUNDRY, "none", True),
        ("gpt-5-chat", AZURE_FOUNDRY, None, True),
        ("o3-mini", AZURE_FOUNDRY, None, False),
        ("o4-mini", AZURE_FOUNDRY, None, False),
        ("gpt-oss-120b", AZURE_FOUNDRY, None, True),
        ("Llama-3.3-70B-Instruct", AZURE_FOUNDRY, None, True),
        ("openai/gpt-oss-120b", GROQ, None, True),
        ("azure_foundry:gpt-5-mini", GROQ, None, False),
    ],
)
def test_supports_temperature(model_name, provider, reasoning_effort, expected):
    assert supports_temperature(model_name, provider, reasoning_effort) is expected


def test_effective_temperature():
    assert effective_temperature("gpt-oss-120b", AZURE_FOUNDRY, 0.2) == 0.2
    assert effective_temperature("gpt-5-mini", AZURE_FOUNDRY, 0.2) is None
    assert effective_temperature("llama-3.3-70b-versatile", GROQ, 0.0) == 0.0
    assert effective_temperature("llama-3.3-70b-versatile", GROQ, None) is None


# --- Groq --------------------------------------------------------------------------


def test_get_llm_groq_keeps_original_behaviour(groq_env):
    llm = get_llm(provider="groq", model_name="llama-3.3-70b-versatile", temperature=0.2)

    assert isinstance(llm, ChatGroq)
    assert llm.model_name == "llama-3.3-70b-versatile"
    assert llm.temperature == 0.2
    assert llm.groq_api_key.get_secret_value() == "test-groq-key"
    assert llm.max_retries == 2
    assert llm.request_timeout == DEFAULT_GROQ_TIMEOUT
    assert llm.client._client.timeout == DEFAULT_GROQ_TIMEOUT


def test_get_llm_groq_forwards_options(groq_env):
    llm = get_llm("groq", "openai/gpt-oss-120b", 0.2, reasoning_effort="low", max_retries=4, timeout=30, max_tokens=4096)

    assert llm.reasoning_effort == "low"
    assert llm.max_retries == 4
    assert llm.request_timeout == 30
    assert llm._default_params["max_tokens"] == 4096


@pytest.mark.parametrize("model", ["openai/gpt-oss-20b", "openai/gpt-oss-120b"])
def test_get_llm_groq_requests_the_model_maximum_output(groq_env, model):
    # Groq's server default caps gpt-oss-20b at 2,048 completion tokens, which cuts off its reasoning.
    llm = get_llm("groq", model, 0.2)

    assert isinstance(llm, GroqChatModel)
    assert llm._default_params["max_tokens"] == 65536


def test_get_llm_groq_without_model_profile_sends_no_max_tokens(groq_env):
    llm = get_llm("groq", "not-a-known-model", 0.2)

    assert llm.max_tokens is None
    assert "max_tokens" not in llm._default_params


# --- Groq rate limits -----------------------------------------------------------------

DAILY_LIMIT_MESSAGE = (
    "Rate limit reached for model `openai/gpt-oss-20b` in organization `org_test` service tier `on_demand` "
    "on tokens per day (TPD): Limit 200000, Used 199500, Requested 1200. Please try again in 5m24.5s."
)


def rate_limited(message=DAILY_LIMIT_MESSAGE, retry_after="325"):
    headers = {"retry-after": retry_after} if retry_after else {}
    return httpx.Response(429, json={"error": {"message": message, "type": "tokens", "code": "rate_limit_exceeded"}}, headers=headers)


def groq_completion():
    return httpx.Response(200, json={**COMPLETION, "model": "openai/gpt-oss-20b"})


class FakeGroq:
    """Mock HTTP transport for the Groq API that replies with the queued responses in order."""

    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []

    def __call__(self, request):
        self.requests.append(json.loads(request.content))
        return self.responses.pop(0)

    def model(self, **kwargs):
        transport = httpx.MockTransport(self)
        return GroqChatModel(
            model="openai/gpt-oss-20b",
            api_key="test-groq-key",
            max_retries=0,
            http_client=httpx.Client(transport=transport),
            http_async_client=httpx.AsyncClient(transport=transport),
            **kwargs,
        )


@pytest.fixture
def sleeps(monkeypatch):
    recorded = []

    async def async_sleep(seconds):
        recorded.append(seconds)

    monkeypatch.setattr(llm_factory, "time", type("FakeTime", (), {"sleep": staticmethod(recorded.append)}))
    monkeypatch.setattr(llm_factory, "asyncio", type("FakeAsyncio", (), {"sleep": staticmethod(async_sleep)}))
    return recorded


def test_groq_rate_limit_waits_for_retry_after_then_succeeds(sleeps, caplog):
    groq_api = FakeGroq(rate_limited(), groq_completion())

    with caplog.at_level(logging.WARNING, logger=llm_factory.__name__):
        response = groq_api.model().invoke("hi")

    assert response.content == "pong"
    assert sleeps == [326.0]
    assert len(groq_api.requests) == 2
    assert "rate limit (TPD) reached for openai/gpt-oss-20b; waiting 326 s" in caplog.text


def test_groq_rate_limit_waits_async(sleeps):
    groq_api = FakeGroq(rate_limited(), groq_completion())

    response = asyncio.run(groq_api.model().ainvoke("hi"))

    assert response.content == "pong"
    assert sleeps == [326.0]


def test_groq_rate_limit_without_header_uses_the_message_hint(sleeps):
    groq_api = FakeGroq(rate_limited(retry_after=None), groq_completion())

    groq_api.model().invoke("hi")

    assert sleeps == [5 * 60 + 24.5 + 1]


def test_groq_rate_limit_gives_up_when_the_wait_budget_is_used(sleeps):
    groq_api = FakeGroq(rate_limited(retry_after="60"), rate_limited(retry_after="60"), groq_completion())

    with pytest.raises(groq.RateLimitError):
        groq_api.model(rate_limit_max_wait=100).invoke("hi")

    assert sleeps == [61.0]
    assert len(groq_api.requests) == 2


TOO_LARGE_FOR_MINUTE_MESSAGE = (
    "Request too large for model `openai/gpt-oss-20b` in organization `org_test` service tier `on_demand` "
    "on tokens per minute (TPM): Limit 8000, Requested 8291, please reduce your message size and try again."
)


def too_large_for_minute(retry_after="30"):
    headers = {"retry-after": retry_after} if retry_after else {}
    return httpx.Response(413, json={"error": {"message": TOO_LARGE_FOR_MINUTE_MESSAGE, "type": "tokens", "code": "rate_limit_exceeded"}}, headers=headers)


def test_groq_request_too_large_for_the_minute_limit_is_retried(sleeps, caplog):
    groq_api = FakeGroq(too_large_for_minute(), groq_completion())

    with caplog.at_level(logging.WARNING, logger=llm_factory.__name__):
        response = groq_api.model().invoke("hi")

    assert response.content == "pong"
    assert sleeps == [31.0]
    assert "too large for the tokens-per-minute limit; retrying in 31 s (31 of 1800 s used)" in caplog.text


def test_groq_request_too_large_backs_off_when_retry_after_is_short(sleeps):
    groq_api = FakeGroq(*[too_large_for_minute(retry_after="1")] * 3, too_large_for_minute(retry_after=None), groq_completion())

    asyncio.run(groq_api.model().ainvoke("hi"))

    assert sleeps == [5.0, 10.0, 20.0, 61.0]


def test_groq_request_too_large_gives_up_when_its_wait_budget_is_used(sleeps):
    groq_api = FakeGroq(*[too_large_for_minute(retry_after="1")] * 3, groq_completion())

    with pytest.raises(groq.APIStatusError) as error:
        groq_api.model(request_too_large_max_wait=20).invoke("hi")

    assert error.value.status_code == 413
    assert sleeps == [5.0, 10.0]
    assert len(groq_api.requests) == 3


def test_groq_waits_for_rate_limits_between_requests_too_large(sleeps):
    groq_api = FakeGroq(too_large_for_minute(retry_after="1"), rate_limited(retry_after="20"), too_large_for_minute(retry_after="1"), groq_completion())

    groq_api.model().invoke("hi")

    assert sleeps == [5.0, 21.0, 10.0]


def test_groq_other_request_too_large_errors_are_not_retried(sleeps):
    too_large = httpx.Response(413, json={"error": {"message": "Request Entity Too Large", "type": "invalid_request_error"}})
    groq_api = FakeGroq(too_large)

    with pytest.raises(groq.APIStatusError) as error:
        groq_api.model().invoke("hi")

    assert error.value.status_code == 413
    assert sleeps == []
    assert len(groq_api.requests) == 1


def test_groq_bad_requests_are_not_retried(sleeps):
    groq_api = FakeGroq(httpx.Response(400, json={"error": {"message": "invalid model", "type": "invalid_request_error"}}))

    with pytest.raises(groq.BadRequestError):
        groq_api.model().invoke("hi")

    assert sleeps == []


# --- Azure AI Foundry --------------------------------------------------------------


def test_get_llm_azure_gpt5_mini_omits_temperature(azure_env):
    llm = get_llm(provider="azure_foundry", model_name="gpt-5-mini", temperature=0.2, reasoning_effort="medium")

    assert isinstance(llm, FoundryChatModel)
    assert llm.deployment_name == "gpt-5-mini"
    assert llm.azure_endpoint == FAKE_AZURE_ENDPOINT
    assert llm.openai_api_version == DEFAULT_AZURE_API_VERSION
    assert llm.max_retries == DEFAULT_AZURE_MAX_RETRIES
    assert llm.request_timeout == DEFAULT_AZURE_TIMEOUT
    assert llm.root_client.timeout == DEFAULT_AZURE_TIMEOUT
    assert llm.azure_ad_token_provider is azure_env
    assert llm.temperature is None

    payload = request_payload(llm)
    assert "temperature" not in payload
    assert payload["reasoning_effort"] == "medium"
    assert payload["model"] == "gpt-5-mini"


def test_get_llm_azure_keeps_temperature_for_models_that_support_it(azure_env):
    llm = get_llm(provider="azure", model_name="gpt-oss-120b", temperature=0.2, max_retries=1, timeout=60)

    payload = request_payload(llm)
    assert payload["temperature"] == 0.2
    assert payload["model"] == "gpt-oss-120b"
    assert "reasoning_effort" not in payload
    assert llm.max_retries == 1
    assert llm.request_timeout == 60


def test_get_llm_azure_sends_max_tokens_only_when_configured(azure_env):
    assert "max_completion_tokens" not in request_payload(get_llm("azure_foundry", "gpt-oss-120b", 0.2))
    assert request_payload(get_llm("azure_foundry", "gpt-oss-120b", 0.2, max_tokens=1000))["max_completion_tokens"] == 1000


def test_get_llm_azure_uses_api_key_when_set(azure_env, monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test-azure-key")

    llm = get_llm(provider="azure_foundry", model_name="gpt-5-mini")

    assert llm.openai_api_key.get_secret_value() == "test-azure-key"
    assert llm.azure_ad_token_provider is None


def test_get_llm_azure_api_version_override(azure_env, monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

    assert get_llm("azure_foundry", "gpt-5-mini").openai_api_version == "2024-12-01-preview"


def test_get_llm_azure_requires_endpoint(azure_env, monkeypatch):
    monkeypatch.delenv("AZURE_OPENAI_ENDPOINT")

    with pytest.raises(ValueError, match="AZURE_OPENAI_ENDPOINT"):
        get_llm(provider="azure_foundry", model_name="gpt-5-mini")


def test_get_llm_prefix_overrides_default_provider(azure_env, groq_env):
    assert isinstance(get_llm(provider="groq", model_name="azure_foundry:gpt-5-mini"), FoundryChatModel)
    assert isinstance(get_llm(provider="azure_foundry", model_name="groq:llama-3.3-70b-versatile"), ChatGroq)


def test_ignored_temperature_is_logged(azure_env, caplog):
    with caplog.at_level(logging.WARNING, logger=llm_factory.__name__):
        get_llm("azure_foundry", "gpt-5-mini", temperature=0.2)

    assert "ignoring temperature=0.2" in caplog.text


def test_default_temperature_is_not_logged(azure_env, caplog):
    with caplog.at_level(logging.WARNING, logger=llm_factory.__name__):
        get_llm("azure_foundry", "gpt-5-mini", temperature=1.0)

    assert caplog.text == ""


# --- wire-level contract: requests sent and token usage read by the agents ----------


def test_groq_request_and_token_usage(groq_env, monkeypatch):
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(200, json={**COMPLETION, "model": "openai/gpt-oss-20b"})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    monkeypatch.setattr(llm_factory, "GroqChatModel", functools.partial(GroqChatModel, http_client=http_client))

    response = get_llm("groq", "openai/gpt-oss-20b", temperature=0.2).invoke("hi")

    # The agents read token usage from this exact path.
    assert response.response_metadata["token_usage"]["total_tokens"] == 6
    body = json.loads(requests[0].content)
    assert (body["model"], body["temperature"], body["max_tokens"]) == ("openai/gpt-oss-20b", 0.2, 65536)
    assert requests[0].headers["authorization"] == "Bearer test-groq-key"


def test_foundry_request_and_token_usage(azure_env, monkeypatch):
    deployment = FakeDeployment()
    http_client = httpx_lib.Client(transport=httpx_lib.MockTransport(deployment))
    monkeypatch.setattr(llm_factory, "FoundryChatModel", functools.partial(FoundryChatModel, http_client=http_client))

    response = get_llm("azure_foundry", "gpt-5-mini", temperature=0.2, reasoning_effort="medium").invoke("hi")

    assert response.response_metadata["token_usage"]["total_tokens"] == 6
    request = deployment.raw_requests[0]
    assert str(request.url) == (
        f"{FAKE_AZURE_ENDPOINT}openai/deployments/gpt-5-mini/chat/completions?api-version={DEFAULT_AZURE_API_VERSION}"
    )
    assert request.headers["authorization"] == "Bearer fake-entra-token"
    body = deployment.requests[0]
    assert "temperature" not in body
    assert (body["model"], body["reasoning_effort"]) == ("gpt-5-mini", "medium")


# --- runtime temperature fallback ---------------------------------------------------


def test_rejected_temperature_is_retried_without_it(azure_env, caplog):
    deployment = FakeDeployment(reject_temperature=True)
    llm = deployment.model()

    with caplog.at_level(logging.WARNING, logger=llm_factory.__name__):
        response = llm.invoke("hi")

    assert response.content == "pong"
    assert response.response_metadata["token_usage"]["total_tokens"] == 6
    assert [body.get("temperature") for body in deployment.requests] == [0.2, None]
    assert llm.temperature is None
    assert "rejected temperature=0.2" in caplog.text

    # Later models for the same deployment no longer send a temperature.
    assert supports_temperature("custom-reasoner", AZURE_FOUNDRY) is False
    assert get_llm("azure_foundry", "custom-reasoner", temperature=0.2).temperature is None
    described = describe_llm_config({"provider": "azure_foundry", "temperature": 0.2, "model": "custom-reasoner"})
    assert described["models"]["model"]["temperature"] is None


def test_rejected_temperature_is_retried_without_it_async():
    deployment = FakeDeployment(reject_temperature=True)

    response = asyncio.run(deployment.model().ainvoke("hi"))

    assert response.content == "pong"
    assert len(deployment.requests) == 2


def test_rejected_temperature_is_retried_by_concurrent_callers():
    # Both calls send the temperature before either handles the rejection (the competitive graph runs in threads).
    deployment = FakeDeployment(reject_temperature=True, barrier=threading.Barrier(2, timeout=10))
    llm = deployment.model()

    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(llm.invoke, ["hi", "hello"]))

    assert [response.content for response in responses] == ["pong", "pong"]
    assert sorted(body.get("temperature") or 0 for body in deployment.requests) == [0, 0, 0.2, 0.2]


def test_accepted_temperature_is_sent_once():
    deployment = FakeDeployment()

    deployment.model(deployment="gpt-oss-120b").invoke("hi")

    assert [body.get("temperature") for body in deployment.requests] == [0.2]


@pytest.mark.parametrize("error_body", OTHER_BAD_REQUESTS, ids=["messages", "temperature-type"])
def test_other_bad_requests_are_not_retried(error_body):
    deployment = FakeDeployment(error_body=error_body)
    llm = deployment.model()

    with pytest.raises(openai.BadRequestError):
        llm.invoke("hi")

    assert len(deployment.requests) == 1
    assert llm.temperature == 0.2
    assert supports_temperature("custom-reasoner", AZURE_FOUNDRY) is True


# --- config helpers ----------------------------------------------------------------


def test_total_tokens_reads_usage(azure_env):
    deployment = FakeDeployment()

    assert total_tokens(deployment.model(deployment="gpt-oss-120b").invoke("hi")) == 6


@pytest.mark.parametrize(
    "response",
    [AIMessage(content="x", response_metadata={"token_usage": None}), AIMessage(content="x"), object()],
    ids=["usage-none", "no-usage", "no-metadata"],
)
def test_total_tokens_without_usage_counts_zero_with_warning(response, caplog):
    with caplog.at_level(logging.WARNING, logger=llm_factory.__name__):
        assert total_tokens(response) == 0

    assert "without token usage" in caplog.text


def test_response_without_usage_does_not_fail():
    deployment = FakeDeployment(omit_usage=True)

    response = deployment.model(deployment="gpt-oss-120b").invoke("hi")

    assert response.content == "pong"
    assert total_tokens(response) == 0


def test_llm_options_from_config():
    config = {"provider": "azure_foundry", "temperature": 1.0, "reasoning_effort": "low", "max_retries": None, "timeout": 120, "max_tokens": 8192}

    assert llm_options_from_config(config) == {"reasoning_effort": "low", "timeout": 120, "max_tokens": 8192}
    assert llm_options_from_config(None) == {}


def test_describe_llm_config_reports_each_role():
    config = {
        "temperature": 0.2,
        "planner_model": "azure_foundry:gpt-5-mini",
        "generator_model_1": "foundry:gpt-oss-120b",
        "generator_model_2": "llama-3.3-70b-versatile",
    }

    assert describe_llm_config(config) == {
        "provider": GROQ,
        "temperature": 0.2,
        "reasoning_effort": None,
        "models": {
            "planner_model": {"provider": AZURE_FOUNDRY, "model": "gpt-5-mini", "temperature": None},
            "generator_model_1": {"provider": AZURE_FOUNDRY, "model": "gpt-oss-120b", "temperature": 0.2},
            "generator_model_2": {"provider": GROQ, "model": "llama-3.3-70b-versatile", "temperature": 0.2},
        },
    }
