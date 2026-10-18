#!/usr/bin/env python3
"""Diagnóstico inicial determinístico de GeoJSON, sem validação topológica."""
import argparse
import collections
import json
from pathlib import Path

def audit(data, key=None):
    if data.get("type") != "FeatureCollection" or not isinstance(data.get("features"), list):
        raise ValueError("Esperada FeatureCollection GeoJSON")
    features = data["features"]
    ids, types = [], collections.Counter()
    nulls = 0
    for feature in features:
        if feature.get("type") != "Feature":
            raise ValueError("Elemento não é Feature")
        geom = feature.get("geometry")
        if geom is None:
            nulls += 1
        else:
            types[geom.get("type", "unknown")] += 1
        if key:
            ids.append((feature.get("properties") or {}).get(key))
    present = [str(v) for v in ids if v is not None and str(v) != ""]
    duplicates = len(present) - len(set(present))
    return {
        "feature_count": len(features),
        "null_geometry_count": nulls,
        "geometry_types": dict(types),
        "key": key,
        "missing_key_count": len(ids) - len(present) if key else None,
        "duplicate_key_count": duplicates if key else None,
        "crs": "RFC 7946 WGS84 longitude/latitude assumed",
        "limitations": ["Não valida autointerseções, geometrias inválidas, CRS real, nem cardinalidade de junções."]
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input_geojson")
    p.add_argument("output_json")
    p.add_argument("--key")
    a = p.parse_args()
    data = json.loads(Path(a.input_geojson).read_text(encoding="utf-8"))
    result = audit(data, a.key)
    Path(a.output_json).write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__":
    main()
