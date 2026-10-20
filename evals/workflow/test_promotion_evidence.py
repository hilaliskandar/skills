import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[2]/"geodados"/"territorializacao-enderecos"/"scripts"/"check_promotion_evidence.py"
spec=importlib.util.spec_from_file_location("check_promotion_evidence",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Tests(unittest.TestCase):
 def test_verified_promotion(self):
  x=[{"record_id":"001","before_class":"ambiguo","after_class":"quadra","method":"quadra_modal","rule_version":"r1","source_locator":"tabela:2"}]
  self.assertTrue(m.evaluate(x)["evidence_complete"])
 def test_missing_source(self):
  x=[{"record_id":"002","before_class":"setor","after_class":"face","method":"numeração","rule_version":"r2","source_locator":""}]
  r=m.evaluate(x)
  self.assertFalse(r["evidence_complete"])
  self.assertEqual(r["unsubstantiated_promotions"][0]["missing"],["source_locator"])
 def test_unknown_precision(self):
  with self.assertRaises(ValueError):m.evaluate([{"record_id":"a","before_class":"AQ1","after_class":"endereco"}])
 def test_duplicate(self):
  x={"record_id":"001","before_class":"setor","after_class":"setor"}
  with self.assertRaises(ValueError):m.evaluate([x,x])
if __name__=="__main__":unittest.main()
