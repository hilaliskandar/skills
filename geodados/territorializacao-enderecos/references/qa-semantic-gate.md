# Controle semântico de QA de territorialização

Não equiparar a contagem de geometrias analíticas com contagens classificadas como 'ponto do estabelecimento'. Uma localização por setor, conjunto de quadras, quadra ou outro representante espacial pode produzir geometria sem representar posição predial.

Auditar o CSV via `scripts/audit_qa_csv.py entrada_QA.csv saida.json`. O script mantém alertas e detecta status OK inconsistentes com os números, porém não estabelece equivalência semântica de métricas ou explica por que um indicador é zero.

A conciliação metodológica requer identificar: expressão exata no notebook que calcula cada indicador, conjunto de classes admitidas, filtros, precedência de versão, valor esperado, data da geração e documentação aplicável. Em divergência, registrar hipótese (erro do script, rótulo amplo, expectativa obsoleta ou alteração do recorte) como **hipótese não confirmada**, não como diagnóstico.

Aprovação de estrutura, completude espacial e aptidão para densidade são avaliações diferentes. Não modificar os dados canônicos nem sobrescrever o CSV original como forma de eliminar alertas.
