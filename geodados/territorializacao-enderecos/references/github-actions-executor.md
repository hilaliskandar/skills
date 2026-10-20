# Execução Parquet em GitHub Actions — executor público e privado

O fluxo `.github/workflows/parquet-synthetic.yml` instala PyArrow e executa teste de ida e volta com arquivo Parquet gerado em tempo de execução. O arquivo sintético não representa a base TIC–TIM e não contém dados reais de estabelecimento.

A execução pode ser iniciada manualmente no GitHub Actions após a presença do workflow na ramificação padrão, ou automaticamente por push/PR nos caminhos configurados. A aprovação demonstra apenas a infraestrutura de leitura e processamento do teste sintético.

**Não** inserir identificadores reais, links privados, credenciais, tokens de acesso ao Drive nem dados individualizados em workflows de repositório público. A etapa seguinte requer executor restrito ou configuração de segurança revisada, com autenticação de escopo mínimo e relatórios agregados. A skill não passa a acionar GitHub Actions automaticamente apenas pela existência deste workflow; isso requer ferramenta de despacho de workflow e permissões próprias.

## Executor privado WSL2 — procedimento validado

O executor efetivamente utilizado para dados reais está em `hilaliskandar/skills-executor-privado`, executado no runner privado `Desk-alexandre-2024-skills`, com acesso a arquivos locais sincronizados no WSL2. O workflow `audit.yml` exige `workflow_dispatch`, `auditar_dados_reais=true` e `caminho_local`, escreve agregados em `/home/alexandre/dados-tic-tim/auditorias/` e **não** versiona Parquets ou envia artifacts ao GitHub. A auditoria real R103.30 foi concluída: 20.471 estabelecimentos, 1.376.541 vínculos, 18.794 estabelecimentos com geometria e nenhum ponto predial confirmado pelo marcador. A origem dos valores negativos foi localizada no R87 e consta da referência `qa-r10330-notebook-correction.md`.

O workflow público de teste sintético não processa os dados reais. O workflow alternativo `drive-audit.yml`, dependente de Google Cloud e federação de identidade, **não faz parte da infraestrutura privada vigente**; sua presença na PR não constitui autorização nem recomendação para configurá-lo. O ChatGPT não dispõe, necessariamente, de permissão para despachar workflows; confirmar as capacidades da integração antes de declarar uma execução iniciada.
