import importlib.util
from pathlib import Path
import unittest

path=Path(__file__).resolve().parents[2]/"diagnostico-municipal"/"indicadores-priorizacao"/"scripts"/"compute_index.py"
spec=importlib.util.spec_from_file_location("compute_index",path)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class TestIndex(unittest.TestCase):
    def test_direction_and_missing(self):
        cfg={"id_column":"municipio","missing":"exclude_and_report","indicators":{"deficit":{"weight":2,"direction":"higher_is_priority"},"investimento":{"weight":1,"direction":"lower_is_priority"}}}
        rows=[{"municipio":"A","deficit":"10","investimento":"100"},{"municipio":"B","deficit":"20","investimento":"50"},{"municipio":"C","deficit":"","investimento":"40"}]
        got=module.compute(rows,cfg)
        self.assertEqual(got["results"][0]["id"],"B")
        self.assertAlmostEqual(got["results"][0]["score"],1)
        self.assertEqual(got["excluded_ids"],["C"])
    def test_constant_is_not_discriminatory(self):
        cfg={"id_column":"id","indicators":{"x":{"weight":1,"direction":"lower_is_priority"}}}
        got=module.compute([{"id":"A","x":"3"},{"id":"B","x":"3"}],cfg)
        self.assertEqual([r["score"] for r in got["results"]],[0,0])
        self.assertEqual(got["constant_indicators"],["x"])
    def test_reject_zero_weights(self):
        cfg={"id_column":"id","indicators":{"x":{"weight":0,"direction":"higher_is_priority"}}}
        with self.assertRaises(ValueError): module.compute([{"id":"A","x":"1"}],cfg)

    def test_reject_duplicate_ids(self):
        cfg={"id_column":"id","indicators":{"x":{"weight":1,"direction":"higher_is_priority"}}}
        with self.assertRaisesRegex(ValueError,"duplicado"):
            module.compute([{"id":"A","x":"1"},{"id":"A","x":"2"}],cfg)
    def test_reject_blank_ids(self):
        cfg={"id_column":"id","indicators":{"x":{"weight":1,"direction":"higher_is_priority"}}}
        with self.assertRaisesRegex(ValueError,"ausente"):
            module.compute([{"id":" ","x":"1"}],cfg)
    def test_preserve_leading_zero_ids(self):
        cfg={"id_column":"id","indicators":{"x":{"weight":1,"direction":"higher_is_priority"}}}
        self.assertEqual(module.compute([{"id":"001","x":"1"},{"id":"002","x":"2"}],cfg)["results"][0]["id"],"002")

if __name__=="__main__":unittest.main()
