#!/usr/bin/env python3
"""Audita um CSV de controle de qualidade sem equiparar indicadores distintos."""
import argparse,csv,json,math

def audit(rows):
    seen=set(); issues=[]; records=[]
    for number,row in enumerate(rows,2):
        name=(row.get("indicador") or "").strip()
        status=(row.get("status") or "").strip().upper()
        if not name or name in seen: raise ValueError(f"Linha {number}: indicador ausente ou duplicado")
        seen.add(name)
        actual=(row.get("valor") or "").strip()
        expected=(row.get("esperado") or "").strip()
        def number_or_none(raw):
            if not raw:return None
            v=float(raw)
            if not math.isfinite(v):raise ValueError("Valor não finito")
            return v
        try:a=number_or_none(actual);e=number_or_none(expected)
        except ValueError:raise ValueError(f"Linha {number}: valor ou esperado inválido")
        problems=[]
        if status not in {"OK","ALERTA","INFO"}: problems.append("status_desconhecido")
        if status=="ALERTA":problems.append("alerta_reportado")
        if status=="OK" and e is not None and a!=e:problems.append("ok_incompatível_com_esperado")
        if status=="OK" and a is None:problems.append("ok_sem_valor")
        if problems:issues.append({"indicador":name,"problems":problems})
        records.append({"indicador":name,"status":status,"valor":a,"esperado":e})
    return {"indicadores":len(records),"aprovado_sem_ressalvas":not issues,
      "pendencias":issues,"registros":records,
      "limite":"Não igualar geometria analítica a ponto predial: comparar apenas métricas com definição idêntica."}

def main():
    p=argparse.ArgumentParser();p.add_argument("qa_csv");p.add_argument("output_json")
    a=p.parse_args()
    with open(a.qa_csv,encoding="utf-8-sig",newline="") as f: result=audit(list(csv.DictReader(f)))
    with open(a.output_json,"w",encoding="utf-8") as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write("\n")
    if not result["aprovado_sem_ressalvas"]:raise SystemExit(2)
if __name__=="__main__":main()
