#!/usr/bin/env python3
"""Validação estrutural de manifesto geoespacial; não valida geometrias."""
import argparse,json
def validate(d):
    required=("crs","n_estabelecimentos","n_com_geometria","n_sem_geometria","precedencia_coordenadas","sha256_geoparquet")
    errors=[f"Campo ausente: {k}" for k in required if k not in d]
    if errors: return {"ok":False,"errors":errors}
    n=d["n_estabelecimentos"];with_geo=d["n_com_geometria"];without=d["n_sem_geometria"]
    if any(type(x) is not int or x<0 for x in (n,with_geo,without)): errors.append("Contagens devem ser inteiros não negativos")
    elif with_geo+without!=n: errors.append("Não conservação do universo")
    seq=d["precedencia_coordenadas"]
    if not isinstance(seq,list) or not seq or not all(isinstance(x,str) and x.strip() for x in seq) or len(seq)!=len(set(seq)):
        errors.append("Precedência inválida ou duplicada")
    checksum=d["sha256_geoparquet"]
    if not isinstance(checksum,str) or len(checksum)!=64 or any(c not in "0123456789abcdefABCDEF" for c in checksum):
        errors.append("SHA-256 inválido")
    if not isinstance(d["crs"],str) or not d["crs"].startswith("EPSG:"): errors.append("CRS não explícito")
    return {"ok":not errors,"errors":errors,"record_count":n}
def main():
    p=argparse.ArgumentParser();p.add_argument("manifest_json");a=p.parse_args()
    with open(a.manifest_json,encoding="utf-8") as f:data=json.load(f)
    result=validate(data);print(json.dumps(result,ensure_ascii=False,indent=2))
    if not result["ok"]:raise SystemExit(2)
if __name__=="__main__":main()
