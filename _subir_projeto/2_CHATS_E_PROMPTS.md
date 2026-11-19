# Chats do Projeto (claude.ai e ChatGPT)

| Chat | Função | Quantos |
|---|---|---|
| 00 · Master / Estratégia | público, séries, prioridades, decisões duradouras (viram `decisoes.md`) | um só |
| 01 · Banco de Ideias | pautas, ganchos, títulos, encaixe no mapa curricular | um só |
| Produção · vid_NNNN / yt_NNNN | do enunciado ao handoff; depois, revisão das pranchas de preview | um por vídeo (arquivar ao entregar) |
| 02 · Revisor de rigor (opcional) | revisão fria de solução e roteiro | um só; cole só o enunciado, a solução e a pergunta |
| 03 · Métricas (quando houver dados) | desempenho, títulos, capas | depois |

Não é preciso um chat de Pipeline Técnico: a parte técnica fica com o Claude Code/Codex no repositório.

**Fluxo:** Ideias → Produção (gera o handoff) → agente de código (preview + pranchas) → de volta à Produção para revisar → voz → master → entrega.

## Prompts de abertura

**00 · Master**
> Leia estado_atual.md e decisoes.md. Resuma em 10 linhas onde o canal está (curtos, longos, séries e último EP de cada uma) e liste as 3 decisões estratégicas que estão em aberto.

**01 · Banco de Ideias**
> Com base no mapa_curricular.md e no estado_atual.md, proponha 5 pautas para o próximo curto (vid_0025) e 3 para o próximo longo, cada uma com gancho, série, posição no mapa e um candidato a solido_3d (ou "nenhum, porque ...").

**Produção · yt_NNNN (longo)**
> Vamos produzir o yt_NNNN: [assunto]. Siga o padrao_video_longo.md. Primeiro, a física congelada (convenções, sinais, fórmulas) e as hipóteses do modelo, com verificação. Depois a pergunta central, o payoff e o storyboard em blocos N01–NNN. Ainda não escreva a narração.

**Produção · vid_NNNN (curto)**
> Vamos produzir o vid_NNNN: [assunto], série [série]. Resolva e verifique primeiro. Depois o roteiro de 60–120 s com fala, tela e animação, seguindo roteiro_voz_elevenlabs_v4.md.
