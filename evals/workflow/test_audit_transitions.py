import importlib.util
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[2]/"geodados"/"territorializacao-enderecos"/"scripts"/"audit_transitions.py"
s=importlib.util.spec_from_file_location("audit_transitions",p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Tests(unittest.TestCase):
 def test_promotion_preserves_bonds(self):
  a=[{"record_id":"001","vinculos":"40","precision_class":"ambiguo"}]
  b=[{"record_id":"001","vinculos":"40","precision_class":"quadra"}]
  r=m.audit(a,b);self.assertTrue(r["conservation_ok"]);self.assertEqual(r["transitions"][0]["count"],1)
 def test_detect_loss_and_bonds(self):
  a=[{"record_id":"001","vinculos":"40","precision_class":"ambiguo"},{"record_id":"002","vinculos":"5","precision_class":"setor"}]
  b=[{"record_id":"001","vinculos":"41","precision_class":"quadra"}]
  r=m.audit(a,b);self.assertFalse(r["conservation_ok"]);self.assertEqual(r["missing_ids"],["002"]);self.assertEqual(r["changed_bonds_ids"],["001"])
 def test_duplicate_rejected(self):
  x=[{"record_id":"001","vinculos":"1","precision_class":"setor"}]
  with self.assertRaises(ValueError):m.audit(x+x,x)
if __name__=="__main__":unittest.main()
