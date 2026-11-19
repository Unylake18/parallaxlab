---
name: fechar-versao-final
description: Fecha a versão final de um vídeo - QA completo, confere CRF 14 no master/legendado, roda videos/entregar.py e informa a pasta em entregas/. Usar só quando o usuário pedir para fechar/entregar a versão final de um vid_NNNN ou yt_NNNN.
---

# Fechar versão final

Só execute quando a fase de fechamento foi aberta explicitamente. Sem pedido, não monte master, voz, SRT nem legendado.

## Passos

1. `git status --short`; preserve alterações existentes.
2. Confirme com a `ficha.md`: formato, série/EP/assunto (`Série pública: **NOME · EP. N**` e `# Assunto`) ou `videos/entregas_registro.json`.
3. **QA completo** (obrigatório no fechamento): cena sem debug de MF-Tools, textos/valores conferidos contra o briefing, voz alinhada, legenda (curto: legendado embutido; longo: `.srt` separado), cartão final/capa.
4. **Qualidade**: render final em 1080p+ já sai com CRF 14 (`template/qualidade.py`). Confira o master:
   `uv run python -c "import av,re;c=av.open('ARQ.mp4');d=b''.join(bytes(p) for _,p in zip(range(4),c.demux(c.streams.video[0])));print(re.search(rb'crf=([0-9.]+)',d).group(1))"` → esperado `14.0`. Master em CRF 23 só melhora re-renderizando.
5. Legendado (`videos/montar_legendado.py`) com `--crf auto`; master pelos scripts `montar_master.py` / `montar_final.py` (voz colada sem recompressão).
6. Entregue: `uv run python videos/entregar.py vid_NNNN` (copia, não move nem apaga). Resultado em `entregas/Série - EP NN - Assunto - NNNN/` com master, legendado, legenda, capa, audio/, texto/, manifesto; número do vídeo no fim de todo nome.
7. Relatório de entrega (skill `relatorio-entrega`) com o caminho da pasta em `entregas/` e o zip para o GPT (em `renders/` da unidade, nunca em `entregas/`).
8. **Limpeza do rastro**: quando o usuário disser que a versão final está aprovada (zip do GPT já usado), rode
   `uv run python videos/limpar_rastro.py vid_NNNN` (simulação), confira a lista e depois `--apagar`. Sai o que não está no Git:
   vídeos, zips, logs, quadros/imagens de `renders`/`qa`/`frames*`/`media*`, cache do Manim e `node_modules`, em todos os
   worktrees; ficam código, áudio e a pasta da entrega. Atalho: `videos/entregar.py vid_NNNN --limpar`.

## Regras
- Não deixe finais soltos em `renders/`.
- Não faça commit/PR/push sem pedido.
- Não use CRF abaixo de 14 sem evidência medida.
