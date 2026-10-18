import json, unittest
from pathlib import Path
class TestManifest(unittest.TestCase):
    def test_synthetic_resume_contract(self):
        path=Path(__file__).with_name("exemplo-manifest.json")
        run=json.loads(path.read_text(encoding="utf-8"))
        required={"schema_version","task_id","skill","skill_revision","cutoff","inputs","completed_steps","artifacts","open_questions","next_step","external_actions"}
        self.assertTrue(required.issubset(run))
        self.assertEqual(run["next_step"],"consultar-fonte-primaria")
        self.assertFalse(run["external_actions"])
if __name__=="__main__":unittest.main()
