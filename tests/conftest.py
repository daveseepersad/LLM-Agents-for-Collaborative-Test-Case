from pathlib import Path

import pytest

from src.agents import llm_factory

REPO_ROOT = Path(__file__).resolve().parents[1]

FAKE_AZURE_ENDPOINT = "https://example-resource.openai.azure.com/"


@pytest.fixture(autouse=True)
def reset_fixed_temperature_registry():
    llm_factory._fixed_temperature_deployments.clear()
    yield
    llm_factory._fixed_temperature_deployments.clear()


@pytest.fixture
def repo_cwd(monkeypatch):
    # ConfigManager, the runners and the pytest runner resolve paths relative to the repository root.
    monkeypatch.chdir(REPO_ROOT)


@pytest.fixture
def groq_env(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-groq-key")


@pytest.fixture
def azure_env(monkeypatch):
    """Offline Azure AI Foundry settings using Entra ID auth with a fake token."""
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", FAKE_AZURE_ENDPOINT)
    for name in ("AZURE_OPENAI_API_KEY", "AZURE_OPENAI_API_VERSION", "OPENAI_API_VERSION"):
        monkeypatch.delenv(name, raising=False)

    def token_provider():
        return "fake-entra-token"

    monkeypatch.setattr(llm_factory, "_entra_token_provider", lambda: token_provider)
    return token_provider
