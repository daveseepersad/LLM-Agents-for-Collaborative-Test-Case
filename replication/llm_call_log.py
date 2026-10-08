#!/usr/bin/env python3
"""Run ``src.experiment_runner`` and log every LLM call to ``llm_calls.jsonl``.

Each line records one chat-model call: start and end time, model, prompt, completion and
total tokens and the finish reason, or the error (for example a Groq rate-limit rejection;
the calls that ``GroqChatModel`` retries are logged once per attempt). The replication
driver copies this file into each pass workspace and runs it instead of the experiment
runner when ``--log-llm-calls`` is set.

Usage (from the repository root or a workspace copy of it):
    python llm_call_log.py --config configs/experiments/single_gptoss20B.yaml
"""

from __future__ import annotations

import json
import re
import threading
import time
from contextvars import ContextVar
from pathlib import Path
from typing import Any

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.tracers.context import register_configure_hook

LOG_FILE = "llm_calls.jsonl"
# Groq's rate-limit messages name the organization; the logs are meant to be shareable.
_ORGANIZATION_ID = re.compile(r"\borg_[0-9a-z]{8,}\b", re.IGNORECASE)


class LLMCallLog(BaseCallbackHandler):
    """Callback handler that appends one JSON line per chat-model call."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()
        self._started: dict[Any, float] = {}

    def _write(self, record: dict) -> None:
        with self._lock, self.path.open("a", encoding="utf-8") as log:
            log.write(json.dumps(record) + "\n")

    def on_chat_model_start(self, serialized: Any, messages: Any, *, run_id: Any, **kwargs: Any) -> None:
        self._started[run_id] = time.time()

    def on_llm_end(self, response: Any, *, run_id: Any, **kwargs: Any) -> None:
        output = response.llm_output or {}
        usage = output.get("token_usage") or {}
        generation = response.generations[0][0] if response.generations and response.generations[0] else None
        if not usage and generation is not None and hasattr(generation, "message"):
            usage = generation.message.response_metadata.get("token_usage") or {}
        self._write(
            {
                "start": self._started.pop(run_id, None),
                "end": time.time(),
                "model": output.get("model_name"),
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
                "finish_reason": (generation.generation_info or {}).get("finish_reason") if generation else None,
            }
        )

    def on_llm_error(self, error: BaseException, *, run_id: Any, **kwargs: Any) -> None:
        self._write(
            {
                "start": self._started.pop(run_id, None),
                "end": time.time(),
                "status_code": getattr(error, "status_code", None),
                "error": _ORGANIZATION_ID.sub("org_<redacted>", f"{type(error).__name__}: {str(error)[:500]}"),
            }
        )


def enable(path: Path | str = LOG_FILE) -> LLMCallLog:
    """Log the calls of every chat model invoked from now on in this process."""
    handler = LLMCallLog(Path(path))
    # A context variable's default is visible in every thread, including the worker threads
    # that run the competitive graph's two developers.
    register_configure_hook(ContextVar("llm_call_log", default=handler), inheritable=True)
    return handler


if __name__ == "__main__":
    enable()
    from src import experiment_runner

    experiment_runner.run()
