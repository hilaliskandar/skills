import importlib.util,unittest
from pathlib import Path
p=Path(__file__).resolve().parents[2]/"geodados"/"territorializacao-enderecos"/"scripts"/"check_notebook_qa.py"
spec=importlib.util.spec_from_file_location("check_notebook_qa",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Tests(unittest.TestCase):
 def test_detect_implicit_cast(self):
  nb={"cells":[{"cell_type":"code","source":["coord_est = df['coordenada_eh_estabelecimento'].fillna(False).astype(bool)"]}]}
  self.assertIn("conversao_implicita_desconhecido_para_falso",m.inspect_notebook(nb)["issues"])
 def test_safe_notebook(self):
  nb={"cells":[{"cell_type":"code","source":["print('ok')"]}]}
  self.assertTrue(m.inspect_notebook(nb)["ok"])
if __name__=="__main__":unittest.main()
