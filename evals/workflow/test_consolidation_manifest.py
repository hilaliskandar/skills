import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[2]/"geodados"/"territorializacao-enderecos"/"scripts"/"validate_consolidation_manifest.py"
s=importlib.util.spec_from_file_location("validate_consolidation_manifest",p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def example():
 return {"crs":"EPSG:4674","n_estabelecimentos":3,"n_com_geometria":2,
 "n_sem_geometria":1,"precedencia_coordenadas":["r2","r1","ref"],
 "sha256_geoparquet":"f"*64}
class Tests(unittest.TestCase):
 def test_valid(self):self.assertTrue(m.validate(example())["ok"])
 def test_bad_totals(self):
  d=example();d["n_sem_geometria"]=2
  self.assertFalse(m.validate(d)["ok"])
 def test_duplicate_precedence(self):
  d=example();d["precedencia_coordenadas"]=["r2","r2"]
  self.assertFalse(m.validate(d)["ok"])
 def test_checksum(self):
  d=example();d["sha256_geoparquet"]="abc"
  self.assertFalse(m.validate(d)["ok"])
if __name__=="__main__":unittest.main()
