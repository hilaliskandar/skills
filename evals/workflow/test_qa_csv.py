import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[2]/"geodados"/"territorializacao-enderecos"/"scripts"/"audit_qa_csv.py"
spec=importlib.util.spec_from_file_location("audit_qa_csv",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Tests(unittest.TestCase):
 def test_preserve_alerts(self):
  x=[{"indicador":"n_estabelecimentos","valor":"3","esperado":"3","status":"OK"},
     {"indicador":"ponto_estabelecimento","valor":"0","esperado":"2","status":"ALERTA"}]
  r=m.audit(x)
  self.assertFalse(r["aprovado_sem_ressalvas"])
  self.assertEqual(r["pendencias"][0]["indicador"],"ponto_estabelecimento")
 def test_reject_misleading_ok(self):
  r=m.audit([{"indicador":"n","valor":"1","esperado":"2","status":"OK"}])
  self.assertFalse(r["aprovado_sem_ressalvas"])
 def test_allow_info_without_expected(self):
  r=m.audit([{"indicador":"geometry","valor":"2","esperado":"","status":"INFO"}])
  self.assertTrue(r["aprovado_sem_ressalvas"])
 def test_duplicate(self):
  x={"indicador":"n","valor":"1","esperado":"1","status":"OK"}
  with self.assertRaises(ValueError):m.audit([x,x])
if __name__=="__main__":unittest.main()
