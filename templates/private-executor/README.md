# Executor privado de auditoria GeoParquet

Modelo de implantação separado da biblioteca pública. Criar um repositório privado, instalar dependências PyArrow e Google Auth e usar autenticação federada OIDC com permissão restrita ao repositório executor. Não gravar credenciais, identificadores de estabelecimentos ou resultados sensíveis no repositório público. Testar com dados sintéticos antes de acessar o Google Drive. O acionamento automático pelo ChatGPT requer um conector que permita iniciar uma execução GitHub Actions; esse recurso não está disponível nas ferramentas GitHub desta sessão.
