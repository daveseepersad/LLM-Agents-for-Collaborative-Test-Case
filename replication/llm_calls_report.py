#!/usr/bin/env python3
"""Summarize the LLM call logs written by ``run_foundry_replication.py --log-llm-calls``.

Reports, per model, the calls and their token sizes, finish reasons and rate-limit
rejections, and how many days the logged workload needs under a daily token limit (Groq's
free tier allows 200K tokens per day per model).

Usage:
    python replication/llm_calls_report.py "replication/groq/pilot/llm_calls/*.jsonl"
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path

import pandas as pd

EXIT_SUCCESS = 0
EXIT_ERROR = 2

FREE_TIER_TOKENS_PER_DAY = 200_000
_LIMIT_KIND = re.compile(r"\((RPM|RPD|TPM|TPD)\)")


def load_calls(pattern: str) -> pd.DataFrame:
    rows = []
    for path in sorted(glob.glob(pattern)):
        experiment, _, run_pass = Path(path).stem.partition("__")
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            rows.append({"experiment": experiment, "pass": run_pass, **record})
    return pd.DataFrame(rows)


def rejection_kind(row: pd.Series) -> str:
    """Label of a failed attempt, e.g. ``413 TPM`` or ``429 TPD``."""
    match = _LIMIT_KIND.search(row["error"] or "")
    status = "" if pd.isna(row.get("status_code")) else f"{int(row['status_code'])} "
    return f"{status}{match.group(1) if match else 'other'}"


def summarize(calls: pd.DataFrame, tokens_per_day: int) -> pd.DataFrame:
    succeeded = calls[calls["error"].isna()] if "error" in calls else calls
    failed = calls[calls["error"].notna()] if "error" in calls else calls.iloc[0:0]
    # Failed attempts carry no model name; attribute them to the model of their experiment's calls.
    model_of = succeeded.groupby("experiment")["model"].agg(lambda models: "+".join(sorted(set(models))))
    rows = {}
    for model, group in succeeded.groupby("model"):
        tokens = group["total_tokens"].sum()
        span_hours = (group["end"].max() - group["start"].min()) / 3600
        rows[model] = {
            "calls": len(group),
            "prompt median": group["prompt_tokens"].median(),
            "prompt max": group["prompt_tokens"].max(),
            "completion median": group["completion_tokens"].median(),
            "completion max": group["completion_tokens"].max(),
            "finish=length": int((group["finish_reason"] == "length").sum()),
            "total tokens": tokens,
            "tokens/hour": round(tokens / span_hours) if span_hours > 0 else None,
            "min days at limit": round(tokens / tokens_per_day, 2),
        }
    summary = pd.DataFrame.from_dict(rows, orient="index")
    if not failed.empty:
        failed = failed.assign(model=failed["experiment"].map(model_of), kind=failed.apply(rejection_kind, axis=1))
        rejections = failed.groupby(["model", "kind"]).size().unstack(fill_value=0)
        summary = summary.join(rejections.add_prefix("rejected "), how="outer").fillna({col: 0 for col in rejections.add_prefix("rejected ").columns})
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pattern", help="Glob of llm_calls JSONL files")
    parser.add_argument("--tokens-per-day", type=int, default=FREE_TIER_TOKENS_PER_DAY, help="Daily token limit per model")
    args = parser.parse_args()
    calls = load_calls(args.pattern)
    if calls.empty:
        print(f"No calls found in {args.pattern}", file=sys.stderr)
        return EXIT_ERROR
    with pd.option_context("display.width", 200, "display.max_columns", None):
        print(summarize(calls, args.tokens_per_day).to_string())
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
