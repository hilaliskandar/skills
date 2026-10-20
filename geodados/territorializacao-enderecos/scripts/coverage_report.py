#!/usr/bin/env python3
"""Auditoria determinística de classes territoriais; não realiza geocodificação."""
import argparse
import csv
import json
from collections import Counter

CLASSES=("endereco","face","quadra","conjunto_quadras","setor","ambiguo","nao_alocado")
STRICT={"endereco","face","quadra"}
APPROX={"conjunto_quadras","setor"}

def report(rows, id_column="record_id", bonds_column="vinculos", class_column="precision_class"):
    seen=set()
    counts=Counter()
    bonds=Counter()
    for line,row in enumerate(rows,2):
        key=row.get(id_column)
        if key is None or key == "":
            raise ValueError(f"Linha {line}: identificador ausente")
        if key in seen:
            raise ValueError(f"Linha {line}: identificador duplicado {key}")
        seen.add(key)
        cls=row.get(class_column)
        if cls not in CLASSES:
            raise ValueError(f"Linha {line}: classe inválida {cls!r}")
        raw=row.get(bonds_column)
        try:
            n=int(raw)
        except (ValueError,TypeError):
            raise ValueError(f"Linha {line}: vínculos não inteiros")
        if n<0:
            raise ValueError(f"Linha {line}: vínculos negativos")
        counts[cls]+=1
        bonds[cls]+=n
    total=len(seen)
    total_bonds=sum(bonds.values())
    def frac(n,den):
        return round(n/den,8) if den else None
    strict_count=sum(counts[k] for k in STRICT)
    approx_count=sum(counts[k] for k in APPROX)
    strict_bonds=sum(bonds[k] for k in STRICT)
    approx_bonds=sum(bonds[k] for k in APPROX)
    return {
        "total_estabelecimentos":total,
        "total_vinculos":total_bonds,
        "por_classe":{k:{"estabelecimentos":counts[k],"vinculos":bonds[k]} for k in CLASSES},
        "cobertura_estrita":{"estabelecimentos":strict_count,"vinculos":strict_bonds,
          "fracao_estabelecimentos":frac(strict_count,total),"fracao_vinculos":frac(strict_bonds,total_bonds)},
        "cobertura_aproximada_adicional":{"estabelecimentos":approx_count,"vinculos":approx_bonds,
          "fracao_estabelecimentos":frac(approx_count,total),"fracao_vinculos":frac(approx_bonds,total_bonds)},
        "residuo":{"estabelecimentos":counts["ambiguo"]+counts["nao_alocado"],
                   "vinculos":bonds["ambiguo"]+bonds["nao_alocado"]},
        "invariantes_conservacao":sum(counts.values())==total and sum(bonds.values())==total_bonds,
        "observacao":"Cobertura não comprova precisão postal; avaliar regras e geometria separadamente."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("input_csv");p.add_argument("output_json")
    p.add_argument("--id-column",default="record_id")
    p.add_argument("--bonds-column",default="vinculos")
    p.add_argument("--class-column",default="precision_class")
    a=p.parse_args()
    with open(a.input_csv,encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    data=report(rows,a.id_column,a.bonds_column,a.class_column)
    with open(a.output_json,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2);f.write("\n")
if __name__=="__main__":main()
