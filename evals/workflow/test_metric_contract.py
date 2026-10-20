import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[2]/"geodados"/"territorializacao-enderecos"/"scripts"/"audit_metric_contract.py"
spec=importlib.util.spec_from_file_location("audit_metric_contract",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Tests(unittest.TestCase):
 def test_detect_conflicting_expected(self):
  x=[{"name":"pontos","predicate":"geometria AND ponto","expected":100,"expected_predicate":"geometria"}]
  self.assertEqual(m.audit(x)["errors"][0]["error"],"meta_sem_mesmo_predicado")
 def test_allow_matching(self):
  x=[{"name":"geometrias","predicate":"geometria","expected":100,"expected_predicate":"geometria"}]
  self.assertTrue(m.audit(x)["ok"])
 def test_allow_unverified_without_target(self):
  x=[{"name":"pontos","predicate":"geometria AND ponto","expected":None}]
  self.assertTrue(m.audit(x)["ok"])
if __name__=="__main__":unittest.main()
