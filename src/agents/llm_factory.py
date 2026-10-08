"""
Centralizza e semplifica la creazione delle istanze dei modelli LLM (Factory Pattern).

Supported providers:

``groq``
    Groq Cloud, used by the original experiments. Requires ``GROQ_API_KEY``. The client
    requests the model's maximum output and waits out rate limits, so experiments also run
    on the free tier (see ``GroqChatModel``).
``azure_foundry`` (aliases: ``azure``, ``foundry``, ``azure_openai``)
    A chat deployment in an Azure AI Foundry / Azure OpenAI resource, such as
    ``gpt-5-mini``. The model name is the *deployment* name. Requires
    ``AZURE_OPENAI_ENDPOINT``. Uses ``AZURE_OPENAI_API_KEY`` when it is set and
    otherwise authenticates with Microsoft Entra ID through
    ``DefaultAzureCredential`` (for example an ``az login`` session).

The experiment-wide provider is ``llm.provider`` in the experiment config. A
single role can use another provider by prefixing its model with the provider
name, e.g. ``"groq:llama-3.3-70b-versatile"`` or ``"azure_foundry:gpt-5-mini"``.
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import time
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import groq
import openai
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import AzureChatOpenAI

load_dotenv()

logger = logging.getLogger(__name__)

GROQ = "groq"
AZURE_FOUNDRY = "azure_foundry"
DEFAULT_PROVIDER = GROQ

_PROVIDER_ALIASES = {
    "groq": GROQ,
    "azure_foundry": AZURE_FOUNDRY,
    "azure": AZURE_FOUNDRY,
    "foundry": AZURE_FOUNDRY,
    "azure_openai": AZURE_FOUNDRY,
}

DEFAULT_AZURE_API_VERSION = "2025-04-01-preview"
DEFAULT_AZURE_MAX_RETRIES = 6
# Without an explicit timeout LangChain disables the openai SDK's own 600 s default, so a
# stalled request would block an experiment forever instead of being retried.
DEFAULT_AZURE_TIMEOUT = 600
AZURE_TOKEN_SCOPE = "https://cognitiveservices.azure.com/.default"
# LangChain disables the groq SDK's timeout in the same way.
DEFAULT_GROQ_TIMEOUT = 600
# Longest time one Groq call may spend waiting out rate limits before the error is raised.
# The daily token limit refills continuously (200K tokens a day on the free tier), and a
# request waits until its prompt plus Groq's estimate of its completion has refilled, which
# takes up to about 9 hours for the largest gpt-oss requests.
DEFAULT_GROQ_RATE_LIMIT_MAX_WAIT = 12 * 3600
# Groq answers 413 "Request too large ... tokens per minute (TPM)" when the prompt plus its
# estimate of the completion, which follows the model's recent completions up to `max_tokens`,
# would exceed the per-minute token limit (8K on the free tier). After a long answer this can
# refuse every request for several minutes, so such a request is retried for up to this long.
DEFAULT_GROQ_REQUEST_TOO_LARGE_MAX_WAIT = 30 * 60

# Config keys (under `llm:`) that name the model of an agent role.
MODEL_CONFIG_KEYS = ("model", "planner_model", "generator_model", "generator_model_1", "generator_model_2")
# Optional config keys (under `llm:`) forwarded to the chat model.
LLM_OPTION_KEYS = ("reasoning_effort", "max_retries", "timeout", "max_tokens")

# Azure deployments that rejected a custom temperature at runtime (lower-case names).
_fixed_temperature_deployments: set[str] = set()


def _provider_key(provider: str) -> str:
    return provider.strip().lower().replace("-", "_")


def normalize_provider(provider: str | None) -> str:
    """Return the canonical provider name, defaulting to Groq."""
    if provider is None:
        return DEFAULT_PROVIDER
    try:
        return _PROVIDER_ALIASES[_provider_key(provider)]
    except KeyError:
        supported = ", ".join(sorted(set(_PROVIDER_ALIASES.values())))
        raise ValueError(f"Unknown LLM provider '{provider}'. Supported providers: {supported}.") from None


def resolve_model(model_name: str, provider: str | None = None) -> tuple[str, str]:
    """Split an optional ``"<provider>:"`` prefix off a model name.

    Returns:
        ``(provider, model_name)`` where provider is canonical. Without a known
        prefix the model name is returned unchanged with the given provider.
    """
    if not model_name:
        raise ValueError("A model name is required.")
    prefix, separator, rest = model_name.partition(":")
    if separator and _provider_key(prefix) in _PROVIDER_ALIASES:
        if not rest.strip():
            raise ValueError(f"Missing model name after provider prefix in '{model_name}'.")
        return normalize_provider(prefix), rest.strip()
    return normalize_provider(provider), model_name


def supports_temperature(model_name: str, provider: str | None = None, reasoning_effort: str | None = None) -> bool:
    """Whether a non-default temperature may be sent to the model.

    Reasoning models on Azure (o-series and gpt-5, except gpt-5 chat variants or
    ``reasoning_effort="none"``) only accept their default temperature of 1.
    Deployments with other names that reject a temperature are detected at
    runtime and remembered for the rest of the process.
    """
    provider, model_name = resolve_model(model_name, provider)
    if provider != AZURE_FOUNDRY:
        return True
    name = model_name.lower()
    if name in _fixed_temperature_deployments or name.startswith(("o1", "o3", "o4")):
        return False
    return not (name.startswith("gpt-5") and "chat" not in name and reasoning_effort != "none")


def effective_temperature(
    model_name: str,
    provider: str | None = None,
    temperature: float | None = None,
    reasoning_effort: str | None = None,
) -> float | None:
    """Temperature sent with each request; ``None`` means the provider default applies."""
    if temperature is None or not supports_temperature(model_name, provider, reasoning_effort):
        return None
    return temperature


def _is_unsupported_temperature_error(error: openai.BadRequestError) -> bool:
    message = str(error).lower()
    mentions_temperature = getattr(error, "param", None) == "temperature" or "temperature" in message
    return mentions_temperature and ("unsupported" in message or "not supported" in message)


class FoundryChatModel(AzureChatOpenAI):
    """``AzureChatOpenAI`` that falls back to the default temperature when a deployment rejects a custom one."""

    def invoke(self, input: Any, config: Any = None, *, stop: list[str] | None = None, **kwargs: Any) -> Any:
        try:
            return super().invoke(input, config, stop=stop, **kwargs)
        except openai.BadRequestError as error:
            if not self._drop_rejected_temperature(error):
                raise
        return super().invoke(input, config, stop=stop, **kwargs)

    async def ainvoke(self, input: Any, config: Any = None, *, stop: list[str] | None = None, **kwargs: Any) -> Any:
        try:
            return await super().ainvoke(input, config, stop=stop, **kwargs)
        except openai.BadRequestError as error:
            if not self._drop_rejected_temperature(error):
                raise
        return await super().ainvoke(input, config, stop=stop, **kwargs)

    def _drop_rejected_temperature(self, error: openai.BadRequestError) -> bool:
        if not _is_unsupported_temperature_error(error):
            return False
        # Another thread sharing this model may already have dropped the temperature.
        if self.temperature is not None:
            logger.warning(
                "Deployment '%s' rejected temperature=%s; retrying with the provider default temperature.",
                self.deployment_name,
                self.temperature,
            )
            self.temperature = None
        _fixed_temperature_deployments.add((self.deployment_name or "").lower())
        return True


@lru_cache(maxsize=1)
def _entra_token_provider():
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider

    # Keep experiment logs readable: the credential chain logs every probe at INFO.
    for name in ("azure.identity", "azure.core.pipeline.policies.http_logging_policy"):
        azure_logger = logging.getLogger(name)
        if azure_logger.level == logging.NOTSET:
            azure_logger.setLevel(logging.WARNING)

    return get_bearer_token_provider(DefaultAzureCredential(), AZURE_TOKEN_SCOPE)


_RETRY_IN = re.compile(r"try again in (?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>[\d.]+)s)?")
_RATE_LIMIT_KIND = re.compile(r"\((RPM|RPD|TPM|TPD)\)")


def _rate_limit_delay(error: groq.APIStatusError) -> float:
    """Seconds Groq asks to wait: the ``retry-after`` header, else the "try again in" hint."""
    response = getattr(error, "response", None)
    try:
        return float(response.headers["retry-after"])
    except (AttributeError, KeyError, TypeError, ValueError):
        pass
    match = _RETRY_IN.search(str(error))
    if match and any(match.groupdict().values()):
        parts = {name: float(value or 0) for name, value in match.groupdict().items()}
        return parts["hours"] * 3600 + parts["minutes"] * 60 + parts["seconds"]
    return 60.0


def _is_too_large_for_minute_limit(error: groq.APIStatusError) -> bool:
    return error.status_code == 413 and "(TPM)" in str(error)


@dataclass
class _GroqRetries:
    """Waits spent on one Groq call so far."""

    waited: float = 0.0
    too_large: int = 0
    too_large_waited: float = 0.0


class GroqChatModel(ChatGroq):
    """``ChatGroq`` that waits out rate limits, including the daily ones, instead of failing.

    The groq SDK only honours ``retry-after`` values of up to 60 seconds. On the free tier a
    daily token or request limit asks for longer waits, which would otherwise fail the call.
    Requests refused as too large for the per-minute token limit are retried with a growing
    pause for up to ``request_too_large_max_wait`` seconds.
    """

    rate_limit_max_wait: float = DEFAULT_GROQ_RATE_LIMIT_MAX_WAIT
    request_too_large_max_wait: float = DEFAULT_GROQ_REQUEST_TOO_LARGE_MAX_WAIT

    def invoke(self, input: Any, config: Any = None, *, stop: list[str] | None = None, **kwargs: Any) -> Any:
        retries = _GroqRetries()
        while True:
            try:
                return super().invoke(input, config, stop=stop, **kwargs)
            except groq.APIStatusError as error:
                delay = self._retry_delay(error, retries)
            time.sleep(delay)

    async def ainvoke(self, input: Any, config: Any = None, *, stop: list[str] | None = None, **kwargs: Any) -> Any:
        retries = _GroqRetries()
        while True:
            try:
                return await super().ainvoke(input, config, stop=stop, **kwargs)
            except groq.APIStatusError as error:
                delay = self._retry_delay(error, retries)
            await asyncio.sleep(delay)

    def _retry_delay(self, error: groq.APIStatusError, retries: _GroqRetries) -> float:
        """Seconds to wait before retrying; re-raises errors that should not, or no longer, be retried."""
        too_large = _is_too_large_for_minute_limit(error)
        if isinstance(error, groq.RateLimitError):
            delay = _rate_limit_delay(error) + 1
        elif too_large:
            # Groq's retry-after for these can be as short as a second, so back off as well.
            delay = max(_rate_limit_delay(error) + 1, min(60.0, 5.0 * 2**retries.too_large))
            if retries.too_large_waited + delay > self.request_too_large_max_wait:
                raise error
        else:
            raise error
        if retries.waited + delay > self.rate_limit_max_wait:
            raise error
        retries.waited += delay
        if too_large:
            retries.too_large += 1
            retries.too_large_waited += delay
            logger.warning(
                "Groq refused a request to %s as too large for the tokens-per-minute limit; "
                "retrying in %.0f s (%.0f of %.0f s used).",
                self.model_name,
                delay,
                retries.too_large_waited,
                self.request_too_large_max_wait,
            )
        else:
            kind = _RATE_LIMIT_KIND.search(str(error))
            logger.warning(
                "Groq rate limit%s reached for %s; waiting %.0f s before retrying.",
                f" ({kind.group(1)})" if kind else "",
                self.model_name,
                delay,
            )
        return delay


def _build_groq_llm(model_name, temperature, reasoning_effort, max_retries, timeout, max_tokens):
    kwargs: dict[str, Any] = {
        "model_name": model_name,
        "api_key": os.getenv("GROQ_API_KEY"),
        "timeout": DEFAULT_GROQ_TIMEOUT if timeout is None else timeout,
    }
    if temperature is not None:
        kwargs["temperature"] = temperature
    if reasoning_effort is not None:
        kwargs["reasoning_effort"] = reasoning_effort
    if max_retries is not None:
        kwargs["max_retries"] = max_retries
    llm = GroqChatModel(**kwargs)
    if max_tokens is None:
        # Groq's server-side default output limit can be far below the model's own (2,048
        # tokens for gpt-oss-20b on the free tier in October 2026), which cuts reasoning models
        # off before they answer, so request the model's maximum explicitly.
        max_tokens = (getattr(llm, "profile", None) or {}).get("max_output_tokens")
    llm.max_tokens = max_tokens
    return llm


def _build_azure_foundry_llm(deployment, temperature, reasoning_effort, max_retries, timeout, max_tokens):
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not endpoint:
        raise ValueError(
            "AZURE_OPENAI_ENDPOINT is not set. Set it (e.g. in .env) to your Azure AI Foundry resource, "
            "for example https://<resource>.openai.azure.com/"
        )
    kwargs: dict[str, Any] = {
        "azure_endpoint": endpoint,
        "azure_deployment": deployment,
        # Some Foundry models (e.g. gpt-oss) reject requests whose body has no `model`.
        "model": deployment,
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION") or os.getenv("OPENAI_API_VERSION") or DEFAULT_AZURE_API_VERSION,
        "max_retries": DEFAULT_AZURE_MAX_RETRIES if max_retries is None else max_retries,
        "timeout": DEFAULT_AZURE_TIMEOUT if timeout is None else timeout,
    }
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if api_key:
        kwargs["api_key"] = api_key
    else:
        kwargs["azure_ad_token_provider"] = _entra_token_provider()
    if reasoning_effort is not None:
        kwargs["reasoning_effort"] = reasoning_effort
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens

    applied_temperature = effective_temperature(deployment, AZURE_FOUNDRY, temperature, reasoning_effort)
    if applied_temperature is not None:
        kwargs["temperature"] = applied_temperature
    elif temperature is not None and temperature != 1:
        logger.warning(
            "Deployment '%s' only supports its default temperature (1); ignoring temperature=%s.",
            deployment,
            temperature,
        )
    return FoundryChatModel(**kwargs)


def get_llm(
    provider: str | None = DEFAULT_PROVIDER,
    model_name: str = "llama-3.1-8b-instant",
    temperature: float | None = 0,
    *,
    reasoning_effort: str | None = None,
    max_retries: int | None = None,
    timeout: float | None = None,
    max_tokens: int | None = None,
):
    """Create the chat model for one agent role.

    Args:
        provider: Default provider (``groq`` or ``azure_foundry``); a provider
            prefix on ``model_name`` takes precedence.
        model_name: Groq model id, or Azure AI Foundry deployment name.
        temperature: Sampling temperature. Ignored, with a warning, for Azure
            deployments that only support their default temperature.
        reasoning_effort: Optional reasoning effort for reasoning models
            (e.g. ``minimal``, ``low``, ``medium``, ``high``).
        max_retries: Retries on transient errors. Defaults to the client default
            for Groq and to ``DEFAULT_AZURE_MAX_RETRIES`` for Azure.
        timeout: Request timeout in seconds. Defaults to ``DEFAULT_GROQ_TIMEOUT``
            for Groq and to ``DEFAULT_AZURE_TIMEOUT`` for Azure.
        max_tokens: Maximum completion tokens per call. Defaults to the model's
            maximum output for Groq and to the deployment default for Azure.

    Raises:
        ValueError: If the provider is unknown or Azure settings are missing.
    """
    provider, model_name = resolve_model(model_name, provider)
    if provider == GROQ:
        return _build_groq_llm(model_name, temperature, reasoning_effort, max_retries, timeout, max_tokens)
    return _build_azure_foundry_llm(model_name, temperature, reasoning_effort, max_retries, timeout, max_tokens)


def llm_options_from_config(llm_config: dict | None) -> dict[str, Any]:
    """Extract the optional ``get_llm`` keyword arguments set in the ``llm`` config section."""
    llm_config = llm_config or {}
    return {key: llm_config[key] for key in LLM_OPTION_KEYS if llm_config.get(key) is not None}


def total_tokens(response: Any) -> int:
    """Total tokens reported for one chat response.

    Some Foundry deployments occasionally return a response without usage; the call is then
    counted as 0 tokens with a warning instead of failing the module.
    """
    usage = (getattr(response, "response_metadata", None) or {}).get("token_usage") or {}
    if usage.get("total_tokens") is None:
        logger.warning("Response without token usage; counting 0 tokens for this call.")
        return 0
    return usage["total_tokens"]


def describe_llm_config(llm_config: dict | None) -> dict[str, Any]:
    """Summarize the provider, model and temperature actually used by each configured role."""
    llm_config = llm_config or {}
    provider = normalize_provider(llm_config.get("provider"))
    temperature = llm_config.get("temperature")
    reasoning_effort = llm_config.get("reasoning_effort")

    models = {}
    for key in MODEL_CONFIG_KEYS:
        if llm_config.get(key):
            role_provider, model_name = resolve_model(llm_config[key], provider)
            models[key] = {
                "provider": role_provider,
                "model": model_name,
                "temperature": effective_temperature(model_name, role_provider, temperature, reasoning_effort),
            }

    return {
        "provider": provider,
        "temperature": temperature,
        "reasoning_effort": reasoning_effort,
        "models": models,
    }
