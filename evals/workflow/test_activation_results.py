"""Verify the activation evidence ledger; this is NOT a model selection test."""
import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "evals" / "activation"

def records(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

class TestActivationEvidence(unittest.TestCase):
    def test_complete_case_inventory(self):
        expected = {r["id"]: r for filename in ("conflitos.csv", "conflitos_negative.csv")
                    for r in records(filename)}
        results = records("execution-results.csv")
        ids = [r["case_id"] for r in results]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), set(expected))
        for r in results:
            self.assertIn(r["status"], {"NOT_RUN", "PASS", "FAIL", "UNOBSERVABLE"})
            if r["status"] == "NOT_RUN":
                self.assertFalse(r["actual_skill"] or r["evidence"])
            else:
                self.assertTrue(r["model"] and r["library_commit"] and r["evidence"])
                if r["status"] == "PASS":
                    self.assertEqual(r["actual_skill"], expected[r["case_id"]]["expected_skill"])
                    forbidden = expected[r["case_id"]].get("forbidden_skill")
                    self.assertNotEqual(r["actual_skill"], forbidden)
                elif r["status"] == "FAIL":
                    self.assertTrue(r["actual_skill"])

if __name__ == "__main__":
    unittest.main()
