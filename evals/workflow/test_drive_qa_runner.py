"""Tests for the Drive executor, using only in-memory synthetic data."""
import importlib.util
import json
import os
from pathlib import Path
from unittest import TestCase, main, mock

@__import__('unittest').skipUnless(importlib.util.find_spec('pyarrow') and importlib.util.find_spec('google'), 'Drive dependencies absent')
@mock.patch.dict(os.environ, {"DRIVE_FILE_ID":"synthetic-id","DRIVE_OUTPUT_FOLDER_ID":"synthetic-folder","EXPECTED_ESTABLISHMENTS":"4","EXPECTED_BONDS":"65","GITHUB_RUN_ID":"123"})
class TestDriveRunner(TestCase):
    def test_mock_drive_roundtrip(self):
        import pyarrow as pa
        import pyarrow.parquet as pq
        import io
        source=io.BytesIO()
        pq.write_table(pa.table({
            "tem_geometria":[True,True,True,False],
            "coordenada_eh_estabelecimento":[True,False,None,None],
            "quantidade_vinculos_ativos":[10,20,30,5],
        }),source)
        data=source.getvalue()
        class Response:
            def __init__(self,payload=b""):self.payload=payload
            def raise_for_status(self):return None
            def iter_content(self,chunk_size):yield self.payload
        class Session:
            def __init__(self):self.upload=None
            def get(self,*args,**kwargs):return Response(data)
            def post(self,*args,**kwargs):
                self.upload=kwargs["data"]
                return Response()
        session=Session()
        path=Path(__file__).resolve().parents[2]/"scripts"/"drive_qa_runner.py"
        spec=importlib.util.spec_from_file_location("drive_qa_runner",path)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with mock.patch.object(module.google.auth,"default",return_value=(object(),None)):
            with mock.patch.object(module,"AuthorizedSession",return_value=session):
                module.run()
        self.assertIsNotNone(session.upload)
        body=session.upload.decode("utf-8")
        self.assertIn('"total": 4',body)
        self.assertIn('"total_vinculos": 65',body)
        self.assertIn('"ponto_confirmado": 1',body)
        self.assertIn('"referencia_local": 1',body)
        self.assertIn('"indeterminado": 1',body)
        self.assertIn('"sem_geometria": 1',body)
    def test_reject_wrong_expected_totals(self):
        import pyarrow as pa
        import pyarrow.parquet as pq
        import io
        output=io.BytesIO()
        pq.write_table(pa.table({"tem_geometria":[True],"quantidade_vinculos_ativos":[5]}),output)
        class R:
            def raise_for_status(self):pass
            def iter_content(self,chunk_size):yield output.getvalue()
        class Session:
            def get(self,*a,**k):return R()
            def post(self,*a,**k):raise AssertionError("must not upload when conservation fails")
        path=Path(__file__).resolve().parents[2]/"scripts"/"drive_qa_runner.py"
        spec=importlib.util.spec_from_file_location("drive_qa_runner",path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with mock.patch.object(module.google.auth,"default",return_value=(object(),None)):
            with mock.patch.object(module,"AuthorizedSession",return_value=Session()):
                with self.assertRaises(ValueError):
                    module.run()
if __name__=="__main__":main()
