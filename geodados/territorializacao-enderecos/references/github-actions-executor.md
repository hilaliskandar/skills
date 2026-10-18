# Executor automatizado por GitHub Actions — etapa sintética

O fluxo `.github/workflows/parquet-synthetic.yml` instala PyArrow e executa teste de ida e volta com arquivo Parquet gerado em tempo de execução. O arquivo sintético não representa a base TIC–TIM e não contém dados reais de estabelecimento.

A execução pode ser iniciada manualmente no GitHub Actions após a presença do workflow na ramificação padrão, ou automaticamente por push/PR nos caminhos configurados. A aprovação demonstra apenas a infraestrutura de leitura e processamento do teste sintético.

**Não** inserir identificadores reais, links privados, credenciais, tokens de acesso ao Drive nem dados individualizados em workflows de repositório público. A etapa seguinte requer executor restrito ou configuração de segurança revisada, com autenticação de escopo mínimo e relatórios agregados. A skill não passa a acionar GitHub Actions automaticamente apenas pela existência deste workflow; isso requer ferramenta de despacho de workflow e permissões próprias.
