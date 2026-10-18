# Contrato de valores esperados em QA espacial

Cada indicador deve declarar um predicado de seleção, uma população de referência e a proveniência de seu valor esperado. Uma contagem baseada em `tem_geometria AND coordenada_eh_estabelecimento` não pode ser confrontada automaticamente com a contagem de `tem_geometria`.

Distinguir claramente `REFERENCIA_TERRITORIAL_LOCAL`, `PONTO_ESTABELECIMENTO` e `SEM_GEOMETRIA`. A presença de ponto geométrico não comprova endereço predial. Quando os indicadores de ponto forem zero e os de geometria forem positivos, preservar ambos e conferir distribuição, tipo de dados e nulidade do marcador original. Não alterar a classificação para cumprir uma meta numérica.

Para produção, definir valores esperados independentes para cada indicador, com versão da fonte e critérios verificáveis. Se a referência não existir, o indicador deve ser declarado informativo ou pendente, e não aprovado contra a população de outra métrica.
