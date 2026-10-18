#!/usr/bin/env python3
"""Índice min-max auditável; somente bibliotecas da instalação Python."""
import argparse, csv, json, math
from pathlib import Path

def compute(rows, config):
    indicators = config["indicators"]
    if not indicators: raise ValueError("Nenhum indicador")
    weights = [float(v["weight"]) for v in indicators.values()]
    if any(not math.isfinite(w) or w < 0 for w in weights) or sum(weights) <= 0:
        raise ValueError("Pesos inválidos")
    policy = config.get("missing", "exclude_and_report")
    if policy != "exclude_and_report": raise ValueError("Política de ausentes não suportada")
    valid, excluded = [], []
    for row in rows:
        try:
            values = {name: float(row[name]) for name in indicators}
            if not all(math.isfinite(v) for v in values.values()): raise ValueError()
            valid.append((row, values))
        except (ValueError, TypeError, KeyError):
            excluded.append(row.get(config["id_column"], ""))
    if not valid: raise ValueError("Nenhuma linha válida")
    ranges = {name: (min(v[name] for _,v in valid), max(v[name] for _,v in valid)) for name in indicators}
    scores=[]
    for row, values in valid:
        detail={}
        for name, spec in indicators.items():
            lo,hi=ranges[name]
            value=0.0 if hi==lo else (values[name]-lo)/(hi-lo)
            direction=spec["direction"]
            if direction == "lower_is_priority" and hi != lo: value=1-value
            elif direction != "higher_is_priority" and direction != "lower_is_priority":
                raise ValueError("Direção inválida: "+direction)
            detail[name]=value
        score=sum(detail[name]*float(spec["weight"]) for name,spec in indicators.items())/sum(weights)
        scores.append({"id":row[config["id_column"]],"score":round(score,12),"normalized":detail})
    scores.sort(key=lambda x:(-x["score"],x["id"]))
    return {"results":scores,"excluded_ids":excluded,"indicator_ranges":ranges,"constant_indicators":[k for k,(a,b) in ranges.items() if a==b]}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input_csv");ap.add_argument("config_json");ap.add_argument("output_json")
    args=ap.parse_args()
    with open(args.input_csv,encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
    with open(args.config_json,encoding="utf-8") as f: config=json.load(f)
    result=compute(rows,config)
    Path(args.output_json).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
