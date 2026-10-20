# Compatibilidade RAIS/CNEFE — classificação histórica

Esta tabela é uma interpretação **operacional provisória** das classes documentadas no histórico de territorialização de estabelecimentos. Antes de processar resultados efetivos, confrontar com os notebooks e seus dicionários de dados. Não interpretar prefixos de regras R89–R93 como níveis espaciais por si só.

| Código histórico | Classe normalizada | Racional | Revisão |
|---|---|---|---|
| AQ0_SEM_ALOCACAO | nao_alocado | Sem alocação | não, salvo evidência suplementar |
| AQ1_QUADRA | quadra | Referência na quadra | verificar regra AQ1 antes de produção |
| AQ2_CONJUNTO_QUADRAS | conjunto_quadras | Localização por conjunto | verificar regra AQ2 |
| AQ3_SETOR | setor | Localização no setor | verificar regra AQ3 |
| AQ4_CEP_MULTIUNIDADE | ambiguo | CEP associado a múltiplas unidades | revisão necessária |

Classes R90_C_LOG_EXCEPCIONAL, R90_D_AMBIGUO e demais R89–R93 devem ser resolvidas pelas colunas finais de classe/precisão produzidas em cada execução, **não pelo prefixo de etapa**. Por exemplo, uma promoção R91 por numeração não prova automaticamente a precisão de endereço.

A conversão não permite falsamente atribuir 'endereco' ou 'face' apenas com AQ1–AQ4. A distinção entre cobertura estrita e aproximada é uma convenção da versão corrente, que pode ser revista segundo os critérios do projeto.

Conferência obrigatória: total de registros, total de vínculos, regras de exclusão, casos ambiguamente classificados, lista de classes não reconhecidas e versão dos notebooks.
