import importlib.util
import unittest
from pathlib import Path

path = Path(__file__).resolve().parents[2] / "evals" / "activation" / "report.py"
spec = importlib.util.spec_from_file_location("activation_report", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class TestActivationReport(unittest.TestCase):
    def test_pending_cannot_approve(self):
        r = module.evaluate([{"case_id":"a", "status":"PASS"},
                             {"case_id":"b", "status":"NOT_RUN"}])
        self.assertFalse(r["release_gate_passed"])
        self.assertFalse(r["complete"])
        self.assertEqual(r["observed_accuracy"], 1.0)

    def test_all_pass(self):
        r = module.evaluate([{"case_id":"a", "status":"PASS"},
                             {"case_id":"b", "status":"PASS"}])
        self.assertTrue(r["release_gate_passed"])

    def test_unobservable_is_not_pass(self):
        r = module.evaluate([{"case_id":"a", "status":"UNOBSERVABLE"}])
        self.assertFalse(r["release_gate_passed"])
        self.assertIsNone(r["observed_accuracy"])

    def test_failure_blocks_release(self):
        r = module.evaluate([{"case_id":"a", "status":"FAIL"}])
        self.assertFalse(r["release_gate_passed"])

    def test_duplicate_case_rejected(self):
        with self.assertRaises(ValueError):
            module.evaluate([{"case_id":"a", "status":"PASS"},
                             {"case_id":"a", "status":"PASS"}])

if __name__ == "__main__":
    unittest.main()
