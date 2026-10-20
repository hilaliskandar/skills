# Reconciliação de manifestos e controles de qualidade

Comparar universo e registros com/sem geometria com os metadados do produto. Antes de aceitar um indicador de QA, identificar a sua **definição**, unidade, versão do script, denominador e regra que determina seu valor esperado.

O atributo 'possui geometria analítica' não é sinônimo de 'ponto exato do estabelecimento'. Não reconciliar automaticamente métricas de semântica diferente. Quando um controle registra ALERTA, manter o alerta, consultar o código gerador e a metodologia, e determinar se houve falha de implementação, expectativa desatualizada ou interpretação incompatível.

Utilizar `scripts/validate_consolidation_manifest.py manifesto.json` para conferir contagens, precedência e formato de checksum. Esse script não verifica o hash do arquivo material nem a validade de geometrias; uma confirmação de integridade exige acesso ao artefato e cálculo independente do SHA-256.

Não copiar para o repositório público IDs de arquivos internos, bases de estabelecimento, vínculos individualizados ou manifestos de produção.
