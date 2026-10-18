#!/usr/bin/env python3
"""Verifica coerência declarativa de métricas e metas de QA. Não executa GeoParquet."""
import argparse,json

def audit(metrics):
    if not isinstance(metrics,list): raise ValueError("Esperada lista de métricas")
    errors=[];seen=set()
    for m in metrics:
        name=m.get("name");predicate=m.get("predicate");expected=m.get("expected")
        definition=m.get("expected_predicate")
        if not isinstance(name,str) or not name: raise ValueError("Nome da métrica ausente")
        if name in seen: raise ValueError("Métrica duplicada: "+name)
        seen.add(name)
        if not isinstance(predicate,str) or not predicate.strip():errors.append({"name":name,"error":"predicado_ausente"})
        if expected is not None and (not isinstance(definition,str) or definition.strip()!=predicate.strip()):
            errors.append({"name":name,"error":"meta_sem_mesmo_predicado"})
    return {"ok":not errors,"errors":errors,"metric_count":len(metrics)}

def main():
    p=argparse.ArgumentParser();p.add_argument("contract_json")
    a=p.parse_args()
    with open(a.contract_json,encoding="utf-8") as f: data=json.load(f)
    result=audit(data["metrics"])
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if not result["ok"]:raise SystemExit(2)
if __name__=="__main__":main()
