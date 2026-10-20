# GitHub Actions + Google Drive: instalação opt-in

O workflow `.github/workflows/drive-audit.yml` está **desativado por padrão**. Ele depende de `ENABLE_DRIVE_AUDIT=true` e de configuração prévia de identidade federada.

Antes de ativar: configurar provedor OIDC do Google com restrições de organização/repositório/ref e vincular conta de serviço apenas à identidade autorizada. Conceder à conta de serviço acesso de leitura ao arquivo específico e escrita apenas à pasta de saída no Drive. Configurar segredos GitHub `GCP_WIF_PROVIDER`, `GCP_SERVICE_ACCOUNT`, `DRIVE_FILE_ID`, `DRIVE_OUTPUT_FOLDER_ID`. Não salvar chaves JSON. Usar política de aprovação em GitHub Environments quando houver dados sensíveis.

Testar inicialmente com Parquet sintético no Drive. Conferir com auditoria de logs que nenhum identificador individual ou nome de arquivo restrito apareça. O processamento grava somente JSON agregado na pasta do Drive e não produz artefatos do Actions.

O GitHub Actions em repositório público possui logs acessíveis publicamente. Mesmo com restrições de acesso, avaliar permissões organizacionais, legislação de proteção de dados e pertinência desse executor para arquivos de produção. O fluxo permanece manual via GitHub UI; a integração atual do ChatGPT não oferece acionamento de workflow sob demanda.

Limitação do executor: depende das colunas `tem_geometria`, `coordenada_eh_estabelecimento` (opcional) e `quantidade_vinculos_ativos`; exige marcadores de geometria booleanos. Executa classificação agregada, não geocodificação nem validação topológica.
