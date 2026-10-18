#!/usr/bin/env python3
"""Compara estados antes/depois por ID; não julga a validade espacial das promoções."""
import argparse,csv,json
from collections import Counter
def index(rows,id_col,bonds_col,class_col):
    out={}
    for row in rows:
        key=row.get(id_col)
        if not key or key in out: raise ValueError("ID ausente ou duplicado")
        try: n=int(row[bonds_col])
        except (KeyError,TypeError,ValueError): raise ValueError("Vínculos inválidos")
        if n<0: raise ValueError("Vínculos negativos")
        out[key]=(n,row.get(class_col,""))
    return out
def audit(before,after):
    a=index(before,"record_id","vinculos","precision_class")
    b=index(after,"record_id","vinculos","precision_class")
    missing=sorted(set(a)-set(b));added=sorted(set(b)-set(a))
    changed_bonds=sorted(k for k in a.keys() & b.keys() if a[k][0]!=b[k][0])
    transitions=Counter((a[k][1],b[k][1]) for k in a.keys() & b.keys())
    return {"before_count":len(a),"after_count":len(b),
            "before_bonds":sum(v[0] for v in a.values()),"after_bonds":sum(v[0] for v in b.values()),
            "missing_ids":missing,"added_ids":added,"changed_bonds_ids":changed_bonds,
            "transitions":[{"from":x,"to":y,"count":n} for (x,y),n in sorted(transitions.items())],
            "conservation_ok":not(missing or added or changed_bonds) and sum(v[0] for v in a.values())==sum(v[0] for v in b.values()),
            "warning":"Transições de precisão exigem evidência externa e versão das regras; conservação não as valida."}
def main():
    p=argparse.ArgumentParser();p.add_argument("before_csv");p.add_argument("after_csv");p.add_argument("output_json")
    x=p.parse_args()
    def read(path):
        with open(path,encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
    result=audit(read(x.before_csv),read(x.after_csv))
    with open(x.output_json,"w",encoding="utf-8") as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write("\n")
    if not result["conservation_ok"]:raise SystemExit(2)
if __name__=="__main__":main()
