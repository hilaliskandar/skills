#!/usr/bin/env python3
"""Linter conservador para QA de notebooks ipynb. Não executa dados."""
import argparse,json,re
def inspect_notebook(nb):
    cells=nb.get("cells",[])
    code="\n".join("".join(c.get("source",[])) for c in cells if c.get("cell_type")=="code")
    issues=[]
    if "coordenada_eh_estabelecimento" in code and re.search(r"fillna\(False\)\.astype\(bool\)",code):
        issues.append("conversao_implicita_desconhecido_para_falso")
    if re.search(r"gdf\['tem_geometria'\]\s*&\s*gdf\.get\('coordenada_eh_estabelecimento'",code):
        for name in ("estabelecimentos_ponto_estabelecimento","vinculos_ponto_estabelecimento"):
            if re.search(r"add\(['\"]"+name+r"['\"],.*?,\s*\d+\s*,",code):
                issues.append("meta_fixa_de_ponto_requer_auditoria:"+name)
    return {"ok":not issues,"issues":issues,
       "limitation":"Alertas heurísticos de código; não demonstram distribuição de coluna ou erro de dados."}
def main():
    p=argparse.ArgumentParser();p.add_argument("input_ipynb")
    a=p.parse_args()
    with open(a.input_ipynb,encoding="utf-8") as f:nb=json.load(f)
    result=inspect_notebook(nb);print(json.dumps(result,ensure_ascii=False,indent=2))
    if result["issues"]:raise SystemExit(2)
if __name__=="__main__":main()
