#!/usr/bin/env python3
"""Inspeção independente da flag predial em arquivo Parquet/GeoParquet existente."""
import argparse,json,math
from collections import Counter

TRUE={True,"true","1","sim","s","yes","y"}
FALSE={False,"false","0","não","nao","n","no"}
def classify(value):
    if value is None:return "desconhecido"
    if isinstance(value,float) and math.isnan(value):return "desconhecido"
    v=value.strip().lower() if isinstance(value,str) else value
    if v=="":return "desconhecido"
    if v in TRUE:return "verdadeiro"
    if v in FALSE:return "falso"
    return "invalido"

def summarize(geometry_flags,predial_flags,bonds):
    if not(len(geometry_flags)==len(predial_flags)==len(bonds)):
        raise ValueError("Colunas com comprimentos diferentes")
    c=Counter();v=Counter()
    for geom,flag,bond in zip(geometry_flags,predial_flags,bonds):
        g=classify(geom)
        if g not in {"verdadeiro","falso"}:raise ValueError("Marcador de geometria inválido")
        status=classify(flag) if g=="verdadeiro" else "sem_geometria"
        c[status]+=1
        if bond is None or isinstance(bond,bool):
            raise ValueError("Vínculos ausentes ou inválidos")
        try:
            n=float(bond)
        except (ValueError,TypeError,OverflowError):
            raise ValueError("Vínculos inválidos") from None
        if not math.isfinite(n) or n<0 or not n.is_integer():
            raise ValueError("Vínculos devem ser inteiros não negativos")
        v[status]+=int(n)
    return {"estabelecimentos":dict(c),"vinculos":dict(v),"total":len(geometry_flags)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("geoparquet");p.add_argument("output_json")
    p.add_argument("--flag",default="coordenada_eh_estabelecimento")
    p.add_argument("--geometry-flag",default="tem_geometria")
    p.add_argument("--bonds",default="quantidade_vinculos_ativos")
    args=p.parse_args()
    try:import pyarrow.parquet as pq
    except ImportError:raise SystemExit("Dependência ausente: pip install pyarrow")
    pf=pq.ParquetFile(args.geoparquet)
    fields=set(pf.schema_arrow.names)
    missing=[x for x in (args.geometry_flag,args.bonds) if x not in fields]
    if missing:raise SystemExit("Campos obrigatórios ausentes: "+", ".join(missing))
    has_flag=args.flag in fields
    cols=[args.geometry_flag,args.bonds]+([args.flag] if has_flag else [])
    t=pq.read_table(args.geoparquet,columns=cols)
    flags=t[args.flag].to_pylist() if has_flag else [None]*t.num_rows
    result=summarize(t[args.geometry_flag].to_pylist(),flags,t[args.bonds].to_pylist())
    result["flag_presente_no_esquema"]=has_flag
    result["nome_flag"]=args.flag
    result["interpretacao"]="Indicadores de geometria e ponto efetivo não possuem necessariamente o mesmo denominador."
    with open(args.output_json,"w",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2);f.write("\n")
if __name__=="__main__":main()
