---
name: territorializacao-enderecos
description: Localizar registros de estabelecimentos por endereço, CEP, face, quadra ou setor com classes de precisão e métricas de vínculos. Usar para correspondência RAIS-CNEFE ou geocodificação aproximada auditável.
---

# Territorialização de Endereços

## Procedimento
1. Inventariar fontes, anos, chaves e sistemas de referência.
2. Preservar CNPJ, CEP e códigos territoriais como strings.
3. Controlar estabelecimentos e vínculos totais e não alocados em cada etapa.
4. Construir níveis graduados de endereço, face, quadra, conjunto de quadras, setor e não alocado.
5. Aplicar correspondência aproximada com trilha de critérios, ambiguidades e distâncias.
6. Priorizar cobertura de vínculos sem atribuir precisão postal fictícia.
7. Exportar classe, geometria, método, evidência e métricas antes/depois.

## Critérios de qualidade
- Identificar fonte, data de referência, evidência e limite da análise.
- Separar fatos verificados, interpretação técnica, hipóteses e pendências.
- Não inventar normas, citações, valores ou resultados de execução.
- Não declarar publicação, aprovação ou decisão sem comprovação.
- Submeter atos externos e alterações sensíveis à revisão responsável.

## Entrega
Produzir resultado rastreável, quadro de evidências quando pertinente, lacunas e próximos encaminhamentos.

## Referências e métricas
- Consultar `references/matching-policy.md` para categorias de precisão, evidências mínimas e parâmetros versionados.
- Para resultados tabulares com uma linha por estabelecimento e classe definida, executar `scripts/coverage_report.py entrada.csv saida.json`.
- Conferir conservação de estabelecimentos e vínculos e distinguir cobertura estrita, aproximada e resíduos. O script é de auditoria de cobertura, **não executa geocodificação**.
- Não promover resultados ambíguos sem justificativa verificável. Registrar estado de execução e pendências quando houver interrupção.

## Compatibilidade histórica RAIS/CNEFE
- Consultar `references/rais-cnefe-classes.md` ao interpretar resultados AQ0–AQ4; verificar os notebooks e a versão das regras originais.
- Se a entrada contiver apenas a classificação histórica AQ0–AQ4, executar `scripts/normalize_historical_classes.py` para conversão conservadora antes de `scripts/coverage_report.py`.
- Para códigos R89–R93, exigir classe final documentada: não deduzir precisão a partir de uma etapa de refinamento.

## Controle de transições entre versões
- Em comparações com universo estável, consultar `references/transition-audit.md` e executar `scripts/audit_transitions.py` para verificar conservação de IDs e vínculos.
- Tratar mudança de classe como hipótese de promoção, não como prova de maior precisão; exigir evidências e regras da execução.

## Evidência das promoções
- Consultar `references/promotion-evidence.md` para auditar ganhos de precisão entre versões.
- Executar `scripts/check_promotion_evidence.py` quando houver tabela de transições com método, versão da regra e localizador de evidência.
- Não tomar a presença de campos como comprovação da exatidão do match; confrontar com as fontes e geometria.

## Consolidação de rodadas incrementais
- Consultar `references/consolidation-policy.md` quando uma base preservar geometria e coordenadas de várias versões.
- Exigir precedência explícita no manifesto e preservar a linhagem da geometria final; distinguir precisão territorial e confiança da associação.
- Utilizar somente registros espacialmente aptos para cada método; não usar fallback municipal como ponto local.

## Verificação de consolidações
- Quando houver manifesto de GeoParquet consolidado, consultar `references/qa-reconciliation.md` e executar `scripts/validate_consolidation_manifest.py`.
- Exigir distinção entre geometria analítica e ponto exato do estabelecimento. Preservar alertas de QA até confronto com definição e código gerador.

## Controle semântico de indicadores QA
- Consultar `references/qa-semantic-gate.md` e executar `scripts/audit_qa_csv.py` quando houver indicadores com valores observados, esperados e status.
- Não transformar `ALERTA` em aprovação por equiparar posições analíticas a pontos prediais; investigar fórmula, filtro e versão do notebook gerador.
