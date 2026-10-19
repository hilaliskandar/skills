"""Validação estática do inventário de prompts; NÃO executa modelo ou skills."""
import csv
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACT = ROOT / "evals" / "activation"

def load(name):
    with (ACT / name).open(encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))

class ActivationFixtures(unittest.TestCase):
    def test_unique_ids_and_nonblank_prompts(self):
        items = load("conflitos.csv") + load("conflitos_negative.csv")
        ids = [row["id"] for row in items]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(row["prompt"].strip() and row["reason"].strip() for row in items))

    def test_every_skill_has_positive_example(self):
        names = {p.parent.name for p in ROOT.glob("*/*/SKILL.md")}
        positives = {row["expected_skill"] for row in load("conflitos.csv")}
        self.assertEqual(names, positives)

    def test_negative_examples_cover_distinct_existing_skills(self):
        names = {p.parent.name for p in ROOT.glob("*/*/SKILL.md")}
        cases = load("conflitos_negative.csv")
        self.assertGreaterEqual(len(cases), 12)
        for case in cases:
            self.assertIn(case["expected_skill"], names)
            self.assertIn(case["forbidden_skill"], names)
            self.assertNotEqual(case["expected_skill"], case["forbidden_skill"])

if __name__ == "__main__":
    unittest.main()
