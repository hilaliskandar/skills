#!/usr/bin/env python3
"""Private Drive input -> aggregate JSON in Drive. No row-level output."""
import hashlib, io, json, os, tempfile
from pathlib import Path
from collections import Counter
import google.auth
from google.auth.transport.requests import AuthorizedSession
import pyarrow.parquet as pq

def run():
    fid=os.environ["DRIVE_FILE_ID"]
    folder=os.environ["DRIVE_OUTPUT_FOLDER_ID"]
    credentials,_=google.auth.default(scopes=["https://www.googleapis.com/auth/drive"])
    session=AuthorizedSession(credentials)
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)/"input.parquet"
        response=session.get("https://www.googleapis.com/drive/v3/files/"+fid,params={"alt":"media"},timeout=120,stream=True)
        response.raise_for_status()
        sha=hashlib.sha256()
        with p.open("wb") as stream:
            for chunk in response.iter_content(1024*1024):
                if chunk: stream.write(chunk);sha.update(chunk)
        pf=pq.ParquetFile(p)
        fields=set(pf.schema_arrow.names)
        geom="tem_geometria"
        point="coordenada_eh_estabelecimento"
        links="quantidade_vinculos_ativos"
        if not {geom,links}.issubset(fields):raise ValueError("Required fields missing")
        has_point=point in fields
        counts=Counter();bonds=Counter()
        cols=[geom,links]+([point] if has_point else [])
        for batch in pf.iter_batches(columns=cols,batch_size=8192):
            d=batch.to_pydict()
            for idx,geo in enumerate(d[geom]):
                if geo is not True and geo is not False:raise ValueError("Unknown geometry state")
                flag=d[point][idx] if has_point else None
                if not geo: category="sem_geometria"
                elif flag is True:category="ponto_confirmado"
                elif flag is False:category="referencia_local"
                else:category="indeterminado"
                n=int(d[links][idx])
                if n<0:raise ValueError("Negative links")
                counts[category]+=1;bonds[category]+=n
        result={"sha256":sha.hexdigest(),"flag_presente":has_point,"total":sum(counts.values()),
                "total_vinculos":sum(bonds.values()),"estabelecimentos_por_classe":dict(counts),
                "vinculos_por_classe":dict(bonds)}
        payload=json.dumps(result,ensure_ascii=False,indent=2).encode("utf-8")
        name="qa-agregado-"+os.environ.get("GITHUB_RUN_ID","manual")+".json"
        metadata=json.dumps({"name":name,"parents":[folder],"mimeType":"application/json"}).encode()
        boundary="aggregate_boundary"
        body=b"--"+boundary.encode()+b"\r\nContent-Type: application/json\r\n\r\n"+metadata+b"\r\n"
        body+=b"--"+boundary.encode()+b"\r\nContent-Type: application/json\r\n\r\n"+payload+b"\r\n--"+boundary.encode()+b"--\r\n"
        upload=session.post("https://www.googleapis.com/upload/drive/v3/files",params={"uploadType":"multipart","fields":"id"},data=body,headers={"Content-Type":"multipart/related; boundary="+boundary},timeout=120)
        upload.raise_for_status()
        print("Aggregate QA uploaded to Drive successfully. No row-level data emitted.")
if __name__=="__main__":run()
