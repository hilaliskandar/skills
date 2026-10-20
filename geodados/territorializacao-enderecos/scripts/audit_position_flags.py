#!/usr/bin/env python3
"""Audita flags de posição sem converter informação desconhecida em falsa."""
import argparse,csv,json
TRUE={"true","1","sim","s","yes","y"}
FALSE={"false","0","não","nao","n","no"}

def parse_flag(value):
    if value is None or str(value).strip()=="":return None
    x=str(value).strip().lower()
    if x in TRUE:return True
    if x in FALSE:return False
    raise ValueError("Marcador booleano não reconhecido: "+str(value))

def audit(rows, geometry_column="tem_geometria", flag_column="coordenada_eh_estabelecimento"):
    out={"total":0,"com_geometria":0,"ponto_confirmado":0,"referencia_nao_predial":0,
         "natureza_indeterminada":0,"sem_geometria":0}
    for i,row in enumerate(rows,2):
        out["total"]+=1
        try:g=parse_flag(row.get(geometry_column))
        except ValueError as e:raise ValueError(f"Linha {i}: {e}")
        if g is None:raise ValueError(f"Linha {i}: geometria indeterminada")
        if g is False:
            out["sem_geometria"]+=1
            continue
        out["com_geometria"]+=1
        try:flag=parse_flag(row.get(flag_column))
        except ValueError as e:raise ValueError(f"Linha {i}: {e}")
        if flag is True:out["ponto_confirmado"]+=1
        elif flag is False:out["referencia_nao_predial"]+=1
        else:out["natureza_indeterminada"]+=1
    out["conservacao_ok"]=(out["com_geometria"]+out["sem_geometria"]==out["total"] and
      out["ponto_confirmado"]+out["referencia_nao_predial"]+out["natureza_indeterminada"]==out["com_geometria"])
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument("input_csv");p.add_argument("output_json")
    p.add_argument("--geometry-column",default="tem_geometria")
    p.add_argument("--flag-column",default="coordenada_eh_estabelecimento")
    args=p.parse_args()
    with open(args.input_csv,encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    result=audit(rows,args.geometry_column,args.flag_column)
    with open(args.output_json,"w",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2);f.write("\n")
if __name__=="__main__":main()
