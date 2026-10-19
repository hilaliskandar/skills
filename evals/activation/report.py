#!/usr/bin/env python3
"""Aggregate the recorded selection results without executing a model."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATES = {"NOT_RUN", "PASS", "FAIL", "UNOBSERVABLE"}

def evaluate(rows):
    counts = Counter()
    seen = set()
    for row in rows:
        case = row["case_id"].strip()
        if not case or case in seen:
            raise ValueError("Case ID absent or duplicated")
        seen.add(case)
        status = row["status"].strip()
        if status not in STATES:
            raise ValueError(f"Invalid status for {case}: {status}")
        counts[status] += 1
    total = sum(counts.values())
    return {
        "total": total,
        "passed": counts["PASS"],
        "failed": counts["FAIL"],
        "not_run": counts["NOT_RUN"],
        "unobservable": counts["UNOBSERVABLE"],
        "observed": counts["PASS"] + counts["FAIL"],
        "observed_accuracy": (counts["PASS"] / (counts["PASS"] + counts["FAIL"])
                              if counts["PASS"] + counts["FAIL"] else None),
        "complete": total > 0 and counts["NOT_RUN"] == 0 and counts["UNOBSERVABLE"] == 0,
        "release_gate_passed": total > 0 and counts["PASS"] == total,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=ROOT / "execution-results.csv")
    parser.add_argument("--allow-incomplete", action="store_true",
                        help="Generate an informative report without failing on pending cases")
    args = parser.parse_args()
    with args.results.open(encoding="utf-8", newline="") as f:
        result = evaluate(list(csv.DictReader(f)))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not args.allow_incomplete and not result["release_gate_passed"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
