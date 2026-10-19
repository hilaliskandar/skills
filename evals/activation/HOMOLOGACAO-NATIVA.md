# Procedimento de homologação nativa no ChatGPT

## Objetivo e condição de liberação
Comprovar o **acionamento efetivo** da skill correta em 25 cenários, e não apenas uma escolha textual feita por modelo externo. O resultado do LiteLLM (25/25 na execução privada 39223800242) é evidência de roteamento indireto e **não substitui** este procedimento.

## Pré-condições
1. Instalar no ambiente ChatGPT as **13 skills** na versão exata da PR #2 e registrar o SHA do commit avaliado.
2. Confirmar que os metadados de cada skill estão visíveis à plataforma e que é possível observar qual skill foi acionada.
3. Criar uma conversa **nova e independente** para cada caso, sem antecipar ao modelo o nome da skill esperada ou proibida. Executar exatamente o texto do campo `prompt`, sem complementar requisitos, salvo documentação de eventual bloqueio por insumo ausente.
4. Usar os 13 casos de `conflitos.csv` e os 12 casos de `conflitos_negative.csv`, preservando seus IDs. Registrar modelo, data e versão da biblioteca.

## Execução e evidências
- Registrar o nome da **skill efetivamente acionada**, e não um nome mencionado na resposta.
- Guardar URL/registro de execução ou outro identificador de evidência verificável. Não registrar chaves, dados sensíveis nem conteúdo reservado.
- Verificar nos casos negativos se a skill `forbidden_skill` não foi acionada indevidamente.
- `PASS`: acionamento observável e correspondente a `expected_skill`, sem acionamento da proibida.
- `FAIL`: acionamento observável divergente, ou acionamento da skill proibida.
- `UNOBSERVABLE`: não existe sinal observável suficiente para atestar a seleção; não presumir `PASS`.
- `NOT_RUN`: execução não realizada.

## Registro
O arquivo `execution-results.csv` contém as colunas `case_id,actual_skill,status,evidence,model,library_commit`. Atualizar uma linha por caso com referência persistente. Não inserir observações do proxy LiteLLM como se fossem evidência de execução nativa.

Depois:
```bash
python evals/activation/report.py --allow-incomplete
python evals/activation/report.py
```

O primeiro comando fornece acompanhamento parcial. O segundo bloqueia a liberação quando ainda houver cenários não executados, não observáveis, reprovados ou metadados de evidência insuficientes.

## Decisão de merge
Exigir os checks estruturais e sintéticos aprovados, além de **25/25 PASS nativos com evidência e commit consistentes**. Na ausência de observabilidade, manter a homologação pendente e explicitar a limitação; não contornar o critério inventando provas. A PR permanece em rascunho até a decisão responsável de integração.
