#!/usr/bin/env python3
"""Batched external routing probe. NOT a native ChatGPT Skill activation test."""
import concurrent.futures
import csv
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "evals" / "activation"
MODEL = os.environ.get("ROUTER_TEST_MODEL", "gpt-4.1-mini")
API_KEY = os.environ.get("ROUTER_TEST_API_KEY", "") or os.environ.get("OPENAI_API_KEY", "")
BACKEND = os.environ.get("ROUTER_TEST_BACKEND", "responses")
API_BASE = os.environ.get("ROUTER_TEST_API_BASE", "")
BATCH_SIZE = max(1, min(int(os.environ.get("ROUTER_TEST_BATCH_SIZE", "13")), 25))
SMOKE_ONLY = os.environ.get("ROUTER_TEST_SMOKE_ONLY", "") == "true"


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def descriptions():
    found = {}
    for path in ROOT.glob("*/*/SKILL.md"):
        s = path.read_text(encoding="utf-8")
        name = re.search(r"(?m)^name:\s*(.+)$", s)
        desc = re.search(r"(?m)^description:\s*(.+)$", s)
        if name and desc:
            found[name.group(1).strip()] = desc.group(1).strip()
    return found


def probe(case, catalog):
    names = sorted(catalog)
    prompt = ("Choose the ONE most appropriate Skill for the user request. "
              "Return only the skill name from the catalog, without explanation. "
              "Do not execute the request.\n\nSkill catalog:\n"
              + "\n".join(f"{k}: {catalog[k]}" for k in names)
              + "\n\nUser request:\n" + case["prompt"])
    if BACKEND == "litellm":
        from litellm import completion
        routed_model = ("openai/" + MODEL) if API_BASE else MODEL
        options = {"api_base": API_BASE.rstrip("/") + "/v1"} if API_BASE else {}
        response = completion(model=routed_model, messages=[{"role":"user","content":prompt}],
                              api_key=API_KEY, max_tokens=80, temperature=0, **options)
        chosen = (response.choices[0].message.content or "").strip()
    elif BACKEND == "responses":
        chosen = query_responses(prompt)
    else:
        raise ValueError("Unknown backend")
    forbidden = case.get("forbidden_skill", "")
    return {"id": case["id"], "expected": case["expected_skill"], "selected": chosen,
            "forbidden": forbidden,
            "outcome": "PASS" if chosen == case["expected_skill"] and chosen != forbidden else "FAIL"}


def query_responses(prompt):
    data = json.dumps({"model": MODEL, "input": prompt, "max_output_tokens": 40}).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=data,
        headers={"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as response:
        payload = json.load(response)
    texts = [part.get("text", "") for item in payload.get("output", [])
             for part in item.get("content", []) if part.get("type") == "output_text"]
    return " ".join(texts).strip()


def main():
    if not API_KEY:
        print("ROUTER_PROXY_NOT_RUN: backend credential absent; no behavioral results.")
        return 2
    if BACKEND == "litellm" and API_BASE:
        req = urllib.request.Request(API_BASE.rstrip("/") + "/v1/models", headers={"Authorization": "Bearer " + API_KEY})
        try:
            with urllib.request.urlopen(req, timeout=8) as res:
                print("ROUTER_GATEWAY_AUTH_HTTP", res.status)
        except urllib.error.HTTPError as err:
            print("ROUTER_GATEWAY_AUTH_HTTP", err.code)
            return 2
        except urllib.error.URLError:
            print("ROUTER_GATEWAY_TRANSPORT_ERROR")
            return 2
    catalog = descriptions()
    cases = read_csv(CASES / "conflitos.csv") + read_csv(CASES / "conflitos_negative.csv")
    if len(cases) != 25 or set(c["expected_skill"] for c in cases) != set(catalog):
        raise ValueError("The 25-case fixture or the 13-skill catalog is inconsistent")
    if SMOKE_ONLY:
        cases = cases[:1]
    results = []
    for start in range(0, len(cases), BATCH_SIZE):
        batch = cases[start:start+BATCH_SIZE]
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(batch)) as executor:
            future_map = {executor.submit(probe, case, catalog): case for case in batch}
            for future in concurrent.futures.as_completed(future_map):
                case = future_map[future]
                try:
                    results.append(future.result())
                except Exception as err:
                    results.append({"id":case["id"],"expected":case["expected_skill"],
                                    "outcome":"ERROR","error_type":type(err).__name__})
        counts = {status:sum(x["outcome"] == status for x in results)
                  for status in ("PASS", "FAIL", "ERROR")}
        print(f"ROUTER_PROXY_BATCH {start//BATCH_SIZE + 1}: completed {len(results)}/{len(cases)}; {counts}")
    results.sort(key=lambda row:row["id"])
    summary = {"method":"external_model_choice_proxy_not_native_skill_activation",
               "backend":BACKEND,"model":MODEL,"cases":len(results),"passed":sum(r["outcome"]=="PASS" for r in results),
               "failed":sum(r["outcome"]=="FAIL" for r in results),
               "errors":sum(r["outcome"]=="ERROR" for r in results)}
    print("ROUTER_PROXY_SUMMARY " + json.dumps(summary, ensure_ascii=False))
    print("ROUTER_PROXY_CASES " + json.dumps(results, ensure_ascii=False))
    # Never populate execution-results.csv: this evaluates text selection, not ChatGPT's runtime.
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
