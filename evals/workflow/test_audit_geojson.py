import importlib.util
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[2]/"geodados"/"auditoria-geoespacial"/"scripts"/"audit_geojson.py"
spec=importlib.util.spec_from_file_location("audit_geojson",p)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
class TestGeoJSON(unittest.TestCase):
    def test_null_and_duplicate_ids(self):
        data={"type":"FeatureCollection","features":[
            {"type":"Feature","properties":{"CD_SETOR":"001"},"geometry":None},
            {"type":"Feature","properties":{"CD_SETOR":"001"},"geometry":{"type":"Point","coordinates":[0,0]}},
            {"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[1,1]}}]}
        result=mod.audit(data,"CD_SETOR")
        self.assertEqual(result["null_geometry_count"],1)
        self.assertEqual(result["duplicate_key_count"],1)
        self.assertEqual(result["missing_key_count"],1)
    def test_reject_incorrect_root(self):
        with self.assertRaises(ValueError):
            mod.audit({"type":"Feature","geometry":None})
if __name__=="__main__":
    unittest.main()
