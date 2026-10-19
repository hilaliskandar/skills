# Diagnóstico e correção do QA R103.30

Fonte examinada: notebook original `TIC_TIM_Gerar_GeoParquet_R103_30.ipynb`, células 4 e 5, recuperado do Google Drive em 18/10/2026.

**Causa confirmada dos dois alertas:** a célula 5 calcula `direto = tem_geometria & coordenada_eh_estabelecimento.fillna(False).astype(bool)`, mas compara `direto.sum()` a **18.794**, valor de **todas as geometrias**. Também compara os vínculos associados a `direto` a **1.228.272**, valor de **todos os vínculos com geometria**. São conceitos distintos.

**R103.30 observado:** 20.471 estabelecimentos, 1.376.541 vínculos; 18.794 referências locais com 1.228.272 vínculos; 1.677 sem geometria com 148.269 vínculos; nenhum ponto confirmado pelo marcador.

**Correção da célula 5 sem reescrever o GeoParquet:**

```python
com_geom = gdf['tem_geometria'].fillna(False).astype(bool)
vinc = pd.to_numeric(gdf['quantidade_vinculos_ativos'], errors='coerce')
coord_raw = gdf['coordenada_eh_estabelecimento'] if 'coordenada_eh_estabelecimento' in gdf.columns else pd.Series(pd.NA, index=gdf.index)
coord_bool = coord_raw.astype('boolean')
ponto_confirmado = com_geom & coord_bool.eq(True).fillna(False)
add('estabelecimentos_com_geometria', int(com_geom.sum()), 18794, 'OK' if int(com_geom.sum()) == 18794 else 'ALERTA')
vg = float(vinc.loc[com_geom].sum())
add('vinculos_com_geometria', vg, 1228272, 'OK' if abs(vg-1228272) < 0.5 else 'ALERTA')
add('estabelecimentos_ponto_confirmado', int(ponto_confirmado.sum()))
add('vinculos_ponto_confirmado', float(vinc.loc[ponto_confirmado].sum()))
add('marcador_ponto_ausente', int((com_geom & coord_bool.isna()).sum()))
```

Não atribuir `esperado=0` aos pontos confirmados apenas por terem retornado zero: trata-se de constatação, não de meta de qualidade. A célula 4 utiliza `fillna(False)` e colapsa ausências em negativas para `qualidade_geometria_final`. Recomenda-se avaliar separadamente as ausências em `coord_raw` antes de decidir se a classe `REFERENCIA_TERRITORIAL_LOCAL` é suficientemente respaldada. Não atualizar o GeoParquet nem substituir o QA histórico; gerar um novo QA versionado e manter a proveniência.

## Implementação complementar

Notebook QA v2 somente leitura, salvo no Google Drive: https://drive.google.com/file/d/1EQFvqA8Iw5EK2VEGRRucBO8zDsMIKqTN/view . Ele lê o GeoParquet canônico, verifica SHA-256, calcula indicadores independentes de cobertura geométrica e ponto confirmado, produz CSV e JSON agregados e **não publica arquivos no Drive por padrão**. Não substitui o notebook gerador nem reexecuta a consolidação geográfica. O notebook foi validado sintaticamente, mas ainda não foi executado no Colab.

## Encerramento da linhagem do marcador

A origem da atribuição uniforme foi **localizada na célula de código 10 do notebook R87** `87_TERRITORIALIZACAO_CEP_CNEFE_EMPREGADORES_MAIS10_2025_v1.ipynb` (Drive ID `1JZYV52BdJPp5TKODXk8BQVZGIWiQG12x`): `pareado['coordenada_eh_estabelecimento']=False`. Na mesma etapa, a referência espacial é construída por município+CEP usando o CNEFE, e a geometria é descrita como referência CNEFE do CEP. Portanto, a negativa uniforme é cautela metodológica inicial; **não constitui verificação negativa individual de precisão predial**. Checkpoints de R99 a R103.30 foram auditados e apresentam 20.471 falsos, sem positivos ou nulos. A origem computacional está documentada; eventual confirmação posicional de estabelecimentos exige trabalho específico, separado e versionado. Registro detalhado no repositório privado: `docs/origem-coordenada-eh-estabelecimento-r87-20261018.md`.
