# Níveis de auditoria de dados espaciais

Nível 1: verificação inicial GeoJSON pela biblioteca padrão Python. Contagens de feições, geometrias nulas, tipos geométricos e chaves ausentes/duplicadas. Executar `scripts/audit_geojson.py entrada.geojson saida.json --key CD_SETOR` quando houver arquivo compatível. Manter códigos territoriais como texto.

Nível 2: auditoria geométrica completa exige ferramenta espacial efetiva (GeoPandas, Shapely, GDAL ou banco espacial) e disponibilidade no ambiente. Testar CRS de origem, validade topológica, área, limites, sobreposições e junções com métricas apropriadas. Não declarar nível 2 com base apenas no script de nível 1.

O GeoJSON RFC 7946 usa coordenadas WGS84 em ordem longitude/latitude; não inferir que o arquivo de entrada seguiu a especificação corretamente. Exigir verificação adicional quando a proveniência espacial for duvidosa.
