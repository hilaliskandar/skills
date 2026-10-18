# Consolidação de geometrias de rodadas incrementais

Quando uma base preserva posições geradas em várias rodadas, distinguir:
- universo econômico integral;
- conjunto com posição analítica;
- conjunto com posição apta para cada tipo de análise;
- fallback de visualização, que não deve ser tratado como localização intraurbana.

## Precedência
A precedência de rodadas **deve vir de manifesto versionado da execução**; nunca inferir por ordem alfabética das colunas. Para cada identificador, selecionar a primeira coordenada válida segundo a precedência explícita e registrar a rodada que forneceu a geometria. Coordenadas vazias, fora de intervalo ou com par latitude/longitude incompleto não são válidas.

## Duas dimensões da qualidade
Precisão territorial (endereço, face, quadra, setor, CEP, área etc.) e confiança da associação são eixos distintos. Não deduzir confiança exclusivamente da precisão geométrica nem tratar centroide de área como endereço real.

## Política por finalidade
Estatísticas econômicas usam o universo integral; análises espacialmente sensíveis usam apenas o subconjunto cuja qualidade territorial seja apropriada à escala. Fallback municipal nunca deve participar de densidades, centralidades ou distâncias locais sem justificativa metodológica específica.

## Auditoria
Conservar identificadores e vínculos entre entrada e saída; registrar contagens e vínculos com/sem geometria; registrar fonte e rodada de cada posição; produzir manifesto com versão, fontes e checksum dos artefatos.

Este guia é generalizado para reuso. Parâmetros, nomes de rodadas e dados de bases restritas pertencem ao manifesto de cada execução, fora do repositório público.
