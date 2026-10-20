# Auditoria de mudanças entre etapas

Executar `scripts/audit_transitions.py antes.csv depois.csv resultado.json` depois de normalizar os nomes das colunas record_id, vinculos e precision_class. Registrar origem e versão de ambos os arquivos.

O script detecta IDs ausentes/adicionados, mudanças no número de vínculos por estabelecimento e matriz de transições entre classes. Seu código de saída é 2 se falhar a conservação. A análise não comprova a justificativa das promoções; cada mudança para classe mais precisa exige regra versionada, fonte e evidência.

A auditoria pressupõe população fixa por etapa. Se a metodologia introduziu deliberadamente novos registros ou novas fontes de vínculos, NÃO forçar a conservação: separar universos comparáveis e documentar a mudança antes de usar a ferramenta.
