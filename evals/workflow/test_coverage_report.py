import importlib.util
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[2]/"geodados"/"territorializacao-enderecos"/"scripts"/"coverage_report.py"
spec=importlib.util.spec_from_file_location("coverage_report",p)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class TestCoverage(unittest.TestCase):
    def test_counts_and_bonds(self):
        rows=[{"record_id":"01","vinculos":"100","precision_class":"quadra"},
              {"record_id":"02","vinculos":"5","precision_class":"setor"},
              {"record_id":"03","vinculos":"30","precision_class":"ambiguo"},
              {"record_id":"04","vinculos":"0","precision_class":"nao_alocado"}]
        got=mod.report(rows)
        self.assertEqual(got["total_estabelecimentos"],4)
        self.assertEqual(got["total_vinculos"],135)
        self.assertEqual(got["cobertura_estrita"]["vinculos"],100)
        self.assertEqual(got["cobertura_aproximada_adicional"]["estabelecimentos"],1)
        self.assertEqual(got["residuo"]["vinculos"],30)
        self.assertTrue(got["invariantes_conservacao"])
    def test_reject_duplicate(self):
        with self.assertRaisesRegex(ValueError,"duplicado"):
            mod.report([{"record_id":"001","vinculos":"1","precision_class":"face"},
                        {"record_id":"001","vinculos":"2","precision_class":"face"}])
    def test_reject_invalid_values(self):
        for bonds,cls in [("-1","quadra"),("1.5","quadra"),("2","logradouro")]:
            with self.subTest(bonds=bonds,cls=cls):
                with self.assertRaises(ValueError):
                    mod.report([{"record_id":"X","vinculos":bonds,"precision_class":cls}])
    def test_empty(self):
        got=mod.report([])
        self.assertEqual(got["total_estabelecimentos"],0)
        self.assertIsNone(got["cobertura_estrita"]["fracao_estabelecimentos"])
if __name__=="__main__":unittest.main()
