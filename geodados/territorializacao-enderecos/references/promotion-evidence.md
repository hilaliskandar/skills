# Auditoria de evidências de promoção

Aplicar `scripts/check_promotion_evidence.py transicoes.csv auditoria.json` às transições que possuem as colunas record_id, before_class, after_class, method, rule_version e source_locator.

O script demanda método, versão da regra e localizador de fonte para mudanças para classes de maior precisão. Sua hierarquia de precisão é operacional e simplificada: nao_alocado/ambiguo (0), setor (1), conjunto_quadras (2), quadra (3), face (4), endereco (5). Uma passagem entre ambíguo e não alocado não é contada como promoção.

Limitação: o script verifica presença de evidência declarada, não sua qualidade, correção ou suficiência. É indispensável validar a regra e consultar resultados efetivos dos notebooks RAIS/CNEFE antes de usar a auditoria para certificar promoções. Não comparar classes históricas AQ e R diretamente sem o mapeamento documentado.
