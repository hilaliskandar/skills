#!/usr/bin/env python3
"""Conversor conservador AQ0–AQ4 para relatório de cobertura; sem geocodificação."""
import argparse, csv
from pathlib import Path

MAP={
    "AQ0_SEM_ALOCACAO":("nao_alocado","aq0_sem_alocacao"),
    "AQ1_QUADRA":("quadra","aq1_quadra"),
    "AQ2_CONJUNTO_QUADRAS":("conjunto_quadras","aq2_conjunto"),
    "AQ3_SETOR":("setor","aq3_setor"),
    "AQ4_CEP_MULTIUNIDADE":("ambiguo","aq4_multiunidade")
}
def convert(rows, id_column="record_id", bonds_column="vinculos", historical_column="classe_historica"):
    result=[]
    for i,row in enumerate(rows,2):
        code=(row.get(historical_column) or "").strip()
        if code not in MAP:
            raise ValueError(f"Linha {i}: classe não mapeada {code!r}; verificar saída final dos notebooks")
        cls,rule=MAP[code]
        if not (row.get(id_column) or "").strip():
            raise ValueError(f"Linha {i}: identificador ausente")
        try:
            b=int(row[bonds_column])
            if b<0: raise ValueError()
        except (KeyError,TypeError,ValueError):
            raise ValueError(f"Linha {i}: vínculos inválidos")
        result.append({"record_id":row[id_column],"vinculos":str(b),
                       "precision_class":cls,"original_class":code,
                       "conversion_rule":rule,"requires_review":"true" if cls=="ambiguo" else "false"})
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("input_csv");p.add_argument("output_csv")
    p.add_argument("--id-column",default="record_id")
    p.add_argument("--bonds-column",default="vinculos")
    p.add_argument("--historical-column",default="classe_historica")
    a=p.parse_args()
    with open(a.input_csv,encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    result=convert(rows,a.id_column,a.bonds_column,a.historical_column)
    with open(a.output_csv,"w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=["record_id","vinculos","precision_class","original_class","conversion_rule","requires_review"])
        writer.writeheader();writer.writerows(result)
if __name__=="__main__":main()
