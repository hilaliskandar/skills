import importlib.util
import tempfile
import unittest
from pathlib import Path

class TestParquetRuntime(unittest.TestCase):
    def test_actual_parquet_roundtrip(self):
        import pyarrow as pa
        import pyarrow.parquet as pq
        p=Path(__file__).resolve().parents[2]/"geodados"/"territorializacao-enderecos"/"scripts"/"inspect_parquet_flag.py"
        spec=importlib.util.spec_from_file_location("inspect_parquet_flag",p)
        mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/"test_fixture.parquet"
            table=pa.table({"tem_geometria":[True,True,True,False],"coordenada_eh_estabelecimento":[True,False,None,None],"quantidade_vinculos_ativos":[10,20,30,5]})
            pq.write_table(table,source)
            reloaded=pq.read_table(source)
            result=mod.summarize(*[reloaded[x].to_pylist() for x in ("tem_geometria","coordenada_eh_estabelecimento","quantidade_vinculos_ativos")])
            self.assertEqual(result["total"],4)
            self.assertEqual(result["estabelecimentos"]["verdadeiro"],1)
            self.assertEqual(result["estabelecimentos"]["desconhecido"],1)
            self.assertEqual(result["vinculos"]["falso"],20)
if __name__=="__main__":unittest.main()
