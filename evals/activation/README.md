# Testes de seleção

O arquivo conflitos.csv contém expectativas de escolha, e não resultados comprovados. Execute cada prompt em conversa isolada, registre versão do modelo, skill selecionada, trilha e resultado. Um caso negativo deve detectar acionamento incorreto de skill vizinha; não basta selecionar corretamente em exemplos positivos. A CI estrutural não avalia essas escolhas.

## Cobertura e casos negativos

`conflitos.csv` reúne um exemplo positivo para cada uma das 13 skills; `conflitos_negative.csv` reúne 12 contrastes entre skills vizinhas. `evals/workflow/test_activation_fixtures.py`, executado pela CI, valida **somente** cobertura, unicidade e integridade das expectativas. Não envia os prompts ao modelo e não demonstra taxa real de seleção.

## Execução da avaliação comportamental

Para cada prompt, iniciar conversa independente; registrar data, configuração/modelo disponível, versão/commit da biblioteca, skill acionada, evidência observável e eventual skill indevida. Marcar `PASS` somente quando a skill esperada tiver sido efetivamente acionada e a proibida não; marcar `FAIL` em troca e `UNOBSERVABLE` se o ambiente não permitir observar a seleção. Reportar acertos, falhas e casos não observáveis separadamente. Não concluir eficácia de acionamento apenas porque a CI passou.

## Relatório e critério de liberação

Executar `python evals/activation/report.py --allow-incomplete` para visualizar contagens de aprovações, falhas, pendências e resultados não observáveis sem bloquear a consulta. Executar **sem** `--allow-incomplete` para exigir aprovação de **todos** os cenários registrados: o comando retorna código de erro enquanto houver `NOT_RUN`, `FAIL` ou `UNOBSERVABLE`. O campo `observed_accuracy` usa apenas casos realmente observados e pode ser nulo; jamais interpretá-lo como taxa global quando houver pendências. A CI verifica o programa e os fixtures, mas não executa sessões do modelo, portanto não deve aplicar o bloqueio comportamental como pré-requisito dos testes estruturais.
