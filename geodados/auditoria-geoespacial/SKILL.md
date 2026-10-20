---
name: auditoria-geoespacial
description: Auditar arquivos geoespaciais e junções por CRS, integridade das geometrias, unicidade das chaves e cardinalidade. Usar para controle de qualidade de GeoPackage, GeoJSON, shapefile ou tabelas espaciais.
---

# Auditoria Geoespacial

## Procedimento
1. Confirmar EPSG e transformação.
2. inspecionar geometrias vazias, inválidas e duplicadas.
3. preservar identificadores de texto e zeros à esquerda.
4. testar cardinalidade das junções.
5. produzir relatório de integridade e incertezas..

## Qualidade
- Registrar fonte, data de corte, resultados, limitações e pendências.
- Não inventar dados, normas, citações ou resultados de execução.
- Distinguir informação verificada, inferência e recomendação.

## Recursos de auditoria
- Consultar `references/audit-levels.md` para distinguir inspeção determinística de GeoJSON e validação topológica completa.
- Executar `scripts/audit_geojson.py` quando o arquivo de entrada for GeoJSON; reportar explicitamente suas limitações.
