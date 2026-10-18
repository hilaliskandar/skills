import importlib.util
from pathlib import Path
import unittest
path=Path(__file__).resolve().parents[2]/"geodados"/"territorializacao-enderecos"/"scripts"/"normalize_historical_classes.py"
spec=importlib.util.spec_from_file_location("normalize_historical_classes",path)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class TestHistorical(unittest.TestCase):
    def test_conservative_mapping_and_preservation(self):
        codes=["AQ0_SEM_ALOCACAO","AQ1_QUADRA","AQ2_CONJUNTO_QUADRAS","AQ3_SETOR","AQ4_CEP_MULTIUNIDADE"]
        rows=[{"record_id":f"00{i}","vinculos":str(i),"classe_historica":c} for i,c in enumerate(codes)]
        result=mod.convert(rows)
        self.assertEqual([r["precision_class"] for r in result],["nao_alocado","quadra","conjunto_quadras","setor","ambiguo"])
        self.assertEqual(result[-1]["requires_review"],"true")
        self.assertEqual([r["original_class"] for r in result],codes)
        self.assertEqual(sum(int(r["vinculos"]) for r in result),10)
    def test_reject_unknown_refinement_rule(self):
        with self.assertRaisesRegex(ValueError,"não mapeada"):
            mod.convert([{"record_id":"001","vinculos":"3","classe_historica":"R91_PROMOVIDO"}])
    def test_reject_negative_links(self):
        with self.assertRaisesRegex(ValueError,"inválidos"):
            mod.convert([{"record_id":"001","vinculos":"-1","classe_historica":"AQ1_QUADRA"}])
if __name__=="__main__":unittest.main()
