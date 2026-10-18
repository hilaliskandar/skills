# Manifesto de execução — proposta transversal

Gerar por tarefa (fora da pasta da skill) um JSON com schema_version, task_id, skill, skill_revision, cutoff, inputs[{source_id, uri_or_locator, retrieved_at, content_hash}], completed_steps, artifacts, open_questions, next_step e external_actions.

Antes de retomar: validar revisão da skill; conferir integridade e vigência das fontes; confrontar IDs de ações externas; só então executar a primeira etapa não concluída. Não repetir publicações, envios ou atualizações irreversíveis apenas por ausência de histórico da conversa.

O manifesto é uma prática metodológica proposta e não um requisito do padrão Agent Skills.
