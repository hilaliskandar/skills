import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[2]/"geodados"/"territorializacao-enderecos"/"scripts"/"audit_position_flags.py"
spec=importlib.util.spec_from_file_location("audit_position_flags",p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class Tests(unittest.TestCase):
 def test_three_valued_flags(self):
  rows=[{"tem_geometria":"true","coordenada_eh_estabelecimento":"true"},
   {"tem_geometria":"1","coordenada_eh_estabelecimento":"false"},
   {"tem_geometria":"sim","coordenada_eh_estabelecimento":""},
   {"tem_geometria":"não","coordenada_eh_estabelecimento":""}]
  r=mod.audit(rows)
  self.assertEqual((r["com_geometria"],r["ponto_confirmado"],r["referencia_nao_predial"],r["natureza_indeterminada"]),(3,1,1,1))
  self.assertTrue(r["conservacao_ok"])
 def test_missing_flag_is_unknown(self):
  r=mod.audit([{"tem_geometria":"true"}])
  self.assertEqual(r["natureza_indeterminada"],1)
 def test_reject_unrecognized(self):
  with self.assertRaises(ValueError):
   mod.audit([{"tem_geometria":"True","coordenada_eh_estabelecimento":"talvez"}])
if __name__=="__main__":unittest.main()
