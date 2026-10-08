#!/usr/bin/env python3
"""Recompute mutation scores that are missing from replication results.

``src.utils.mutmut_runner.get_mutation_metrics`` discards the score of a module when
mutmut reports any timed-out or suspicious mutant. Under heavy parallel load those are
timing artifacts, so this script re-runs the same function for each missing score, one
module at a time in an isolated workspace, like the repository's
``mutation_injection.ipynb`` does for the archived results. Filled values are marked
with ``"mutation_recomputed": true``. A final suite with 0% coverage cannot run at all
(mutmut's baseline fails), so it kills no mutant and is scored 0 with a ``mutation_note``.

Usage:
    python replication/fill_missing_mutation.py --out replication/foundry/rep1 replication/foundry/rep2
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from src.utils.mutmut_runner import get_mutation_metrics

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

logger = logging.getLogger("fill_missing_mutation")


def recompute(module: str, test_file: Path, attempts: int) -> dict | None:
    """Run the repository's mutation step for one module in a fresh workspace, retrying artifacts."""
    for _ in range(attempts):
        with tempfile.TemporaryDirectory(prefix="mutation_") as directory:
            workspace = Path(directory)
            (workspace / "data" / "input_code").mkdir(parents=True)
            (workspace / "tests").mkdir()
            shutil.copy2(REPO_ROOT / "data" / "input_code" / module, workspace / "data" / "input_code" / module)
            shutil.copy2(test_file, workspace / "tests" / test_file.name)
            # Each worker process has its own working directory, which mutmut uses for its cache.
            os.chdir(workspace)
            try:
                mutation = get_mutation_metrics(f"data/input_code/{module}", f"tests/{test_file.name}")
            finally:
                os.chdir(REPO_ROOT)
        if mutation is not None:
            return mutation
    return None


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recompute missing mutation scores in replication results.")
    parser.add_argument(
        "--out", type=Path, nargs="+", default=[REPO_ROOT / "replication" / "foundry" / "rep1"],
        help="Replication output directories (each with results/ and output_tests/)",
    )
    parser.add_argument("--attempts", type=int, default=3, help="Attempts per module")
    parser.add_argument("--workers", type=int, default=4, help="Modules to recompute in parallel")
    parser.add_argument(
        "--timezone", default=None,
        help="TZ for mutmut, e.g. Asia/Tokyo; d06 tests written for daytime fail from 00:00 to 06:00",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    # mutmut launches `pytest` from PATH, so this interpreter's environment must come first.
    os.environ["PATH"] = f"{Path(sys.executable).parent}{os.pathsep}{os.environ.get('PATH', '')}"
    if args.timezone:
        os.environ["TZ"] = args.timezone
        time.tzset()
    if datetime.now().hour < 6:  # noqa: DTZ005 - d06_complex_logic reads the local hour
        logger.warning("Local time is between 00:00 and 06:00, when d06_complex_logic changes behaviour; see --timezone")
    documents = {
        path: json.loads(path.read_text()) for out in args.out for path in sorted((out / "results").glob("*.json"))
    }
    changed: set[Path] = set()
    jobs = {}
    missing = 0
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for result_path, data in documents.items():
            for item in data["results"]:
                metrics = item.get("metrics") or {}
                if item.get("status") != "success" or metrics.get("mutation_score_percent") is not None:
                    continue
                if metrics.get("coverage_percent") == 0:
                    # The final suite cannot run (e.g. an import error), so it kills no mutant.
                    metrics.update(mutation_score_percent=0.0, mutation_note="test suite does not run; no mutant killed")
                    changed.add(result_path)
                    logger.info("%s %s: 0%% coverage, mutation score set to 0", data["experiment_name"], item["file"])
                    continue
                stem = Path(item["file"]).stem
                test_file = result_path.parent.parent / "output_tests" / data["experiment_name"] / f"test_{stem}.py"
                jobs[pool.submit(recompute, item["file"], test_file, args.attempts)] = (result_path, metrics, item["file"])
        logger.info("Recomputing %d missing mutation scores with %d workers", len(jobs), args.workers)
        for future in as_completed(jobs):
            result_path, metrics, module = jobs[future]
            mutation = future.result()
            logger.info("%s %s: %s", documents[result_path]["experiment_name"], module, mutation)
            if mutation is None:
                missing += 1
                continue
            metrics.update(mutation, mutation_recomputed=True)
            changed.add(result_path)
    for result_path in changed:
        result_path.write_text(json.dumps(documents[result_path], indent=4))
    if missing:
        logger.error("%d mutation scores are still missing", missing)
        return EXIT_FAILURE
    return EXIT_SUCCESS


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
    return run(create_parser().parse_args())


if __name__ == "__main__":
    sys.exit(main())
