# Reconciliação de classificações geoespaciais

Antes de calcular indicadores, separar: (1) geometria disponível; (2) evidência de ponto correspondente ao estabelecimento; (3) referência territorial local; (4) informação desconhecida; (5) fallback municipal. Não utilizar `fillna(False).astype(bool)` para confundir ausência de evidência com negação. Para strings, mapear explicitamente verdadeiro/falso e registrar valores não reconhecidos.

Um indicador calculado por `geometria AND flag_ponto` não pode herdar o valor esperado de `geometria`, salvo demonstração de equivalência entre as populações. Gerar controles distintos para contagem de geometrias e contagem de pontos confirmados; quando não houver meta independente para pontos, atribuir estado informativo ou pendente. Reconciliar separadamente quantidade de estabelecimentos e soma de vínculos.

Uma análise de código estática não substitui leitura independente da coluna no arquivo de produção. Para validar a distribuição, executar a auditoria Parquet em ambiente com leitor instalado; conservar cópias e checksums. Não alterar artefatos canônicos apenas para eliminar alertas.
