# Testes de seleção

O arquivo conflitos.csv contém expectativas de escolha, e não resultados comprovados. Execute cada prompt em conversa isolada, registre versão do modelo, skill selecionada, trilha e resultado. Um caso negativo deve detectar acionamento incorreto de skill vizinha; não basta selecionar corretamente em exemplos positivos. A CI estrutural não avalia essas escolhas.

## Cobertura e casos negativos

`conflitos.csv` reúne um exemplo positivo para cada uma das 13 skills; `conflitos_negative.csv` reúne 12 contrastes entre skills vizinhas. `evals/workflow/test_activation_fixtures.py`, executado pela CI, valida **somente** cobertura, unicidade e integridade das expectativas. Não envia os prompts ao modelo e não demonstra taxa real de seleção.

## Execução da avaliação comportamental

Para cada prompt, iniciar conversa independente; registrar data, configuração/modelo disponível, versão/commit da biblioteca, skill acionada, evidência observável e eventual skill indevida. Marcar `PASS` somente quando a skill esperada tiver sido efetivamente acionada e a proibida não; marcar `FAIL` em troca e `UNOBSERVABLE` se o ambiente não permitir observar a seleção. Reportar acertos, falhas e casos não observáveis separadamente. Não concluir eficácia de acionamento apenas porque a CI passou.

## Relatório e critério de liberação

Executar `python evals/activation/report.py --allow-incomplete` para visualizar contagens de aprovações, falhas, pendências e resultados não observáveis sem bloquear a consulta. Executar **sem** `--allow-incomplete` para exigir aprovação de **todos** os cenários registrados: o comando retorna código de erro enquanto houver `NOT_RUN`, `FAIL` ou `UNOBSERVABLE`. O campo `observed_accuracy` usa apenas casos realmente observados e pode ser nulo; jamais interpretá-lo como taxa global quando houver pendências. A CI verifica o programa e os fixtures, mas não executa sessões do modelo, portanto não deve aplicar o bloqueio comportamental como pré-requisito dos testes estruturais.


## Evidência de roteamento externo — 19/10/2026

O executor `evals/activation/router_proxy_batches.py` classificou as solicitações a partir das descrições das 13 skills, utilizando **LiteLLM local** (`127.0.0.1:4000`) e **OpenRouter/NVIDIA Nemotron** (`openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`). O resultado foi obtido no runner privado, sem publicar credenciais:

- Workflow: [execução 39223800242](https://github.com/hilaliskandar/skills-executor-privado/actions/runs/39223800242), job `117965094687`.
- Primeiro lote: 13 PASS, 0 FAIL, 0 ERROR.
- Segundo lote: 12 PASS, 0 FAIL, 0 ERROR.
- Total: **25/25 seleções corretas (100%)**, **0 violações de formato**, **0 erros de infraestrutura**; autenticação HTTP 200.
- Protocolo: seleção textual com catálogo de descriptions, prompt original de escolha de skill, limite de saída de 192 tokens, temperatura zero. Este resultado se refere àquela execução; não prova repetibilidade estatística.
- Limitação essencial: **teste indireto de classificação textual**, não um registro de acionamento nativo no ambiente ChatGPT. **Não** preencher `execution-results.csv` como `PASS` com base nesta evidência. A homologação nativa continua pendente.

O workflow público `.github/workflows/activation-proxy-batch.yml` é **manual** (`workflow_dispatch`), para não iniciar chamadas a provedores por qualquer push nem produzir reprovações automáticas por falta de segredo. Requer `OPENROUTER_API_KEY` se executado diretamente no GitHub hospedado. O workflow do executor privado utiliza o gateway LiteLLM local e sua credencial virtual `ALE20_LITELLM_API_KEY`. Nenhuma credencial deve constar nos arquivos ou relatórios.

Para a homologação nativa por cenário e o registro de evidências, seguir [HOMOLOGACAO-NATIVA.md](HOMOLOGACAO-NATIVA.md).
