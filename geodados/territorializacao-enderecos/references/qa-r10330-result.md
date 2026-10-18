# Auditoria agregada R103.30 — interpretação

Na execução real de 18/10/2026 em runner privado com PyArrow, foram reconciliados 20.471 estabelecimentos e 1.376.541 vínculos. A classificação observada foi: **referência territorial local** 18.794 estabelecimentos, 1.228.272 vínculos; **sem geometria** 1.677 estabelecimentos, 148.269 vínculos; **pontos confirmados pelo marcador** 0 estabelecimentos, 0 vínculos. O campo `coordenada_eh_estabelecimento` existe.

**Regra de QA:** os indicadores `estabelecimentos_com_geometria` e `vinculos_com_geometria` não são equivalentes a `estabelecimentos_ponto_confirmado` e `vinculos_ponto_confirmado`. Geometria presente não comprova localização predial. Não comparar contagens de geometria com expectativas de pontos confirmados. Mesmo sem marcadores nulos, emitir aviso metodológico quando nenhum registro possui confirmação de ponto efetivo.

**Limite probatório:** a classificação do campo não esclarece sozinha se os valores `False` foram atribuídos intencionalmente ou por preenchimento padrão. Revisar a linhagem do notebook gerador e a definição formal do campo antes de alterar classificações. Não modificar o GeoParquet canônico em consequência desta auditoria.
