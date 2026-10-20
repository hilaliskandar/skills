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


def check_release_evidence(rows, expected):
    """Verify exact coverage and proof metadata, without asserting proof authenticity."""
    by_id = {row["case_id"].strip(): row for row in rows}
    if len(by_id) != len(rows) or set(by_id) != set(expected):
        raise ValueError("Recorded cases differ from expected 25-case inventory")
    problems = []
    for case, row in by_id.items():
        if row["status"] != "PASS":
            continue
        if row.get("actual_skill", "").strip() != expected[case]:
            problems.append(case + ": skill mismatch")
        if not all(row.get(field, "").strip() for field in ("evidence", "model", "library_commit")):
            problems.append(case + ": missing proof metadata")
    return problems

def expected_cases():
    out = {}
    for filename in ("conflitos.csv", "conflitos_negative.csv"):
        with (ROOT / filename).open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                if row["id"] in out:
                    raise ValueError("Duplicate case in fixtures")
                out[row["id"]] = row["expected_skill"]
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=ROOT / "execution-results.csv")
    parser.add_argument("--allow-incomplete", action="store_true",
                        help="Generate an informative report without failing on pending cases")
    args = parser.parse_args()
    with args.results.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    result = evaluate(rows)
    problems = check_release_evidence(rows, expected_cases())
    result["proof_metadata_issues"] = problems
    result["release_gate_passed"] = result["release_gate_passed"] and not problems
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not args.allow_incomplete and not result["release_gate_passed"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
