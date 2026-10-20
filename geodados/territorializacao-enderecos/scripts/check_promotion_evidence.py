#!/usr/bin/env python3
"""Audita evidências de promoções; não verifica se a geometria está correta."""
import argparse,csv,json
RANK={"nao_alocado":0,"ambiguo":0,"setor":1,"conjunto_quadras":2,"quadra":3,"face":4,"endereco":5}
def evaluate(rows):
    issues=[];promotions=0;unchanged=0
    seen=set()
    for i,row in enumerate(rows,2):
        key=row.get("record_id","").strip()
        if not key or key in seen: raise ValueError(f"Linha {i}: ID ausente ou duplicado")
        seen.add(key)
        before=row.get("before_class","").strip()
        after=row.get("after_class","").strip()
        if before not in RANK or after not in RANK: raise ValueError(f"Linha {i}: classe inválida")
        if RANK[after]>RANK[before]:
            promotions+=1
            needed=("method","rule_version","source_locator")
            missing=[x for x in needed if not row.get(x,"").strip()]
            if missing: issues.append({"record_id":key,"missing":missing})
        else: unchanged+=1
    return {"records":len(seen),"promotions":promotions,"other_transitions":unchanged,
            "unsubstantiated_promotions":issues,"evidence_complete":not issues,
            "limitations":"Preenchimento não comprova validade da fonte; verificar regra e geometria separadamente."}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("input_csv");p.add_argument("output_json")
    a=p.parse_args()
    with open(a.input_csv,encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
    result=evaluate(rows)
    with open(a.output_json,"w",encoding="utf-8") as f: json.dump(result,f,ensure_ascii=False,indent=2);f.write("\n")
    if not result["evidence_complete"]: raise SystemExit(2)
if __name__=="__main__":main()
