# Magnetostática — Lei de Biot–Savart

formato: longo_horizontal
natureza: teoria_visual
solido_3d: nenhum — vetores, espira e projeção espacial em Manim (2.5D por projeção própria); sem integração Blender.

Identificação editorial do handoff: **5.2**, continuação direta do 5.1 longo.
Posição curricular: **6.8 Campo magnético e Biot–Savart** em `docs/mapa_curricular.md`.

Fase: cena completa → preview horizontal 960×540 / 15 fps. Sem voz, sync, SRT, master, capa ou publicação.

Classe: `YT0006BiotSavart` (`cena.py`), uma cena contínua, 17 seções.

## Redesenho v4 (2026-10-17)
Cena reescrita por completo, no padrão do yt_0005: B magenta · corrente verde · F azul claro · fios azul claro · geometria (R, r, s, a, x, z) violeta; cartões azul-escuro.
- Equações em cartões à direita (principal + auxiliar), diagrama maior à esquerda, legenda inferior em 28 pt com matemática em `$…$`.
- Nenhum termo surge do nada: o primeiro termo de cada equação voa de uma cópia do rótulo no diagrama; as demais etapas usam `TransformByGlyphMap` (MF-Tools) com mapa por termo (`kit.py: gmap`, `base.py: show`).
- 2.5D: anéis de B em torno do fio, correntes em fio/lâmina/volume, mão direita com dB fora do plano, espira girando da vista frontal à lateral; demais cenas em 2D.

Estrutura: `kit.py` (paleta, equações com tokens, gmap) · `base.py` (projeção, slots de equação, legenda) · `sec1`–`sec7.py` (conteúdo) · `fisica.py` (estados físicos, inalterado) · `contato.py`, `juntar.py` (utilitários de QA/montagem).
`cena_anterior_codex.py` = versão anterior (referência, não importada). `qa_*.py` e `preview_trechos.py` pertencem à estrutura antiga e não funcionam mais.

Revisão profunda v5 (2026-10-18): ver `RELATORIO_REVISAO.md`. Preview atual: `renders/preview/YT0006BiotSavart_preview.mp4` — 16min47s (antes: 15min14s), 960×540 / 15 fps, silencioso (renderizado em 3 trechos por limite de memória e juntado por cópia de pacotes). Quadros a 1 fps em `renders/preview/quadros_1fps/`.
Render por trecho: `SEG=<seção>[,<seção>] uv run python -m manim -r 960,540 --fps 15 cena.py YT0006BiotSavart`.
