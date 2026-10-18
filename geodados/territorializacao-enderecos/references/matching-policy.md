# Política de territorialização e precisão

## Objetivo
Situar estabelecimentos para análise territorial, não garantir endereço postal exato. Preservar CEP, CNPJ e CD_SETOR como texto. O registro da geometria deve sempre estar associado ao método, à evidência e à escala de precisão.

## Classes mínimas
- endereco: comprovado por endereço e numeração compatíveis.
- face: lado/face de quadra defensável por numeração ou evidência equivalente.
- quadra: identificação da quadra sem posição precisa no lote.
- conjunto_quadras: conjunto reduzido e documentado de quadras.
- setor: setor censitário, usado apenas se níveis mais finos não forem defensáveis.
- ambiguo: candidatos incompatíveis, sem regra de desempate confiável.
- nao_alocado: evidência insuficiente.

## Critérios de correspondência
Normalizar logradouro por procedimento versionado, mantendo o texto original. Tratar tipo, título e nome separadamente e documentar correspondências aproximadas. Limiares para distância, dominância de quadra, CEP multiunidade e promoção entre classes são **parâmetros de execução**, não constantes universais. Identificar a versão da regra e justificar cada promoção. Nenhum caso ambíguo será promovido automaticamente apenas para aumentar cobertura.

## Saídas auditáveis
Cada registro deve incluir identificador, vínculos, classe, método, identificador da geometria, número de candidatos, escore, distância quando aplicável, fonte, versão da regra e necessidade de revisão manual. Não equiparar 'localizado por setor' a 'endereço exato'.

## Conservação
Contagens antes = soma por classes; vínculos antes = soma por classes. Medir cobertura estrita, cobertura aproximada e resíduos separadamente. Comparar bases e versões utilizando a mesma definição de classes.
