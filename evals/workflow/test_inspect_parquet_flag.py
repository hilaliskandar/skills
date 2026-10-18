import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[2]/"geodados"/"territorializacao-enderecos"/"scripts"/"inspect_parquet_flag.py"
spec=importlib.util.spec_from_file_location("inspect_parquet_flag",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestParquetFlag(unittest.TestCase):
 def test_3_states(self):
  r=m.summarize([True,True,True,False],[True,False,None,None],[10,20,30,5])
  self.assertEqual(r["estabelecimentos"],{"verdadeiro":1,"falso":1,"desconhecido":1,"sem_geometria":1})
  self.assertEqual(r["vinculos"]["verdadeiro"],10)
 def test_strings(self):
  r=m.summarize(["true","sim"],["false",""],[3,4])
  self.assertEqual(r["estabelecimentos"]["desconhecido"],1)
 def test_mismatch(self):
  with self.assertRaises(ValueError):m.summarize([True],[True,False],[1])
if __name__=="__main__":unittest.main()
