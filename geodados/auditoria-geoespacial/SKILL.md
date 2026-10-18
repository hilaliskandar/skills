---
name: auditoria-geoespacial
description: Auditar GeoJSON, shapefiles, GeoPackages e tabelas espaciais, verificando CRS, geometrias, cobertura, unicidade e integridade de junções.
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
