# Biblioteca de Skills

Coleção de 13 skills distribuídas em oito áreas de trabalho, voltadas a pesquisa científica, planejamento urbano, gestão pública, dados territoriais e publicação editorial.

## Estrutura
- **urbanismo** — Inventários de normas, planos diretores e parâmetros territoriais
- **radares** — Coleta, revisão e auditoria dos radares editoriais
- **pesquisa** — Fichamento acadêmico, avaliação científica e rastreabilidade
- **legislacao-urbanistica** — Leitura de dispositivos e revisão de minutas normativas
- **diagnostico-municipal** — Diagnósticos territoriais e índices municipais
- **governanca-publica** — Contratações, notas técnicas e atos administrativos
- **geodados** — Territorialização de estabelecimentos e auditoria espacial
- **editorial** — Revisão autoral e gestão de publicações

Cada skill possui `SKILL.md` e `agents/openai.yaml`. A validação estrutural não substitui testes funcionais. O repositório é público: não incluir credenciais, processos restritos, dados pessoais ou arquivos internos.

## Utilização
Abra o diretório da skill desejada e utilize as instruções de `SKILL.md` como ponto de entrada. Para instalar no ChatGPT, empacote uma única skill por arquivo ZIP, preservando seu diretório. Versão inicial experimental — requer validação com casos reais.


## Estado dos testes e critérios para integração

A biblioteca dispõe de 13 skills e 25 cenários de seleção: 13 casos positivos e 12 de contraste entre skills próximas. Os workflows públicos de validação estrutural e de execução sintética de Parquet estão aprovados no commit `3c521c56` da PR #2.

A avaliação externa de roteamento por descrições foi executada em 19/10/2026, usando LiteLLM em runner privado e o modelo `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`. Na [execução 39223800242](https://github.com/hilaliskandar/skills-executor-privado/actions/runs/39223800242), os dois lotes (13 e 12) obtiveram **25/25 seleções corretas, zero respostas fora do formato e zero erros de infraestrutura**. Trata-se de classificação textual a partir dos metadados das skills, e **não** de acionamento nativo no ChatGPT. Ver método, limitações e casos em [evals/activation/README.md](evals/activation/README.md).

**A PR #2 permanece em rascunho, sem homologação nativa.** O arquivo `evals/activation/execution-results.csv` conserva `NOT_RUN` nos 25 casos nativos. Não usar os resultados do LiteLLM para preencher artificialmente esse registro.

Para homologar no ChatGPT, testar cada cenário em conversa independente com a biblioteca efetivamente instalada, documentar skill acionada, modelo, commit e evidência observável. Marcar `PASS` somente quando houver prova da seleção; marcar `UNOBSERVABLE` quando a execução não oferecer observabilidade suficiente. Consultar o relatório com `python evals/activation/report.py --allow-incomplete`; executar sem essa opção apenas para o bloqueio final da homologação.

O workflow externo de proxy no repositório público exige acionamento manual. O executor no repositório privado usa o gateway LiteLLM local; ambos devem manter chaves e dados reservados fora do código e dos logs.
