---
name: projeto-yt0002-gauss
description: "Estado e convenções da implementação do yt_0002 (Lei de Gauss, casos clássicos) em cena.py, por rodadas de beats"
metadata:
  node_type: memory
  type: project
  originSessionId: 00be2549-face-4cf9-bbd1-71f65a0436bd
  modified: 2026-10-07T21:24:33.143Z
---

`videos_longos/yt_0002_lei_gauss_casos_classicos/cena.py` (classe `LeiGaussCasosClassicos002`) é implementado por rodadas aprovadas pelo usuário; só `cena.py` é editado, preview 960×540/15 fps, sem voz/SRT/1080p/commit.

Estado (2026-10-07): vídeo completo N01–N29 implementado em cena.py (0:00–18:01, preview de 1081 s): cilíndrica (N04–N11), planar (N12–N15), esférica (N20–N23), N24 três capacitores, N25 áreas/potências, N26 checklist aplicado, N27 payoff, pausa de 2 s, N29 outro (logo + anéis, igual ao yt_0001). Sem voz/SRT/1080p/commit; falta integração/QA final (a duração real vem da voz) e pós-produção quando o usuário abrir essa fase. Numeração dos beats do handoff ≠ storyboard (N12–N15 cobrem N12–N19; N20–N23; N24–N29 = N24–N29); T_N* em `cena.py` são orçamento ajustado.

Rodadas de refinamento (2026-10-07): (a) correção física (placa N13 `slab_box`/`env_slab`/`slab_cota`, setas dos capacitores no vão, `play()` com saída-antes-da-entrada via `_choque`); (b) refinamento de textos + álgebra com MF-Tools: `gx` (MathTex de string única com checagem do nº de glifos e cores por índice), `gstrike` (riscos por glifo), `mv` (mapa de glifos) e `TransformByGlyphMap` nos cancelamentos do cilindro maciço (N08), folha (N12), placa (N13), duas folhas (N14) e esfera maciça (N22). Padrão: `self.play(TransformByGlyphMap(A, B, *mv(...), ([rem], []), ([], [intro])))` seguido de `self.remove(A)`; a cadeia inteira de uma conta precisa ser glyph-map (não misturar com `TransformMatchingTex`/`eqm`). Largura medida de `Text` vem ~10% maior que a real.

**Why:** a Produção/GPT revisa por blocos; o usuário repassa os frames ao GPT (ver [[feedback-enviar-frames]]).

**How to apply:** reutilize o sistema do arquivo — tipografia congelada (`title`/`body`/`note`/`label`, math `M_L/M_M/M_S`), coluna direita alinhada a `RL`, grade `Y_*`, `eqm` (MathTex com partes `{{ }}` para TransformMatchingTex sem fórmula fantasma), `GaussCyl`/`Pill` (gaussianas dinâmicas por tracker), `Dimmer` (holofote), `SO=n,m` para render parcial. Armadilhas: (1) o cache do Manim reaproveita trechos quando só cores mudam — use `--disable_caching` no render final; (2) nunca rode dois renders manim ao mesmo tempo na mesma pasta `media/`; (3) Text em Space Grotesk não tem glifos gregos (só MathTex); (4) em patches Python, strings com `\f`/`\v` viram caracteres de controle — grave por arquivo/Edit; (5) `cena.py` usa CRLF no Windows: leia com newline padrão.

## Estado em 2026-10-11 (atualização)

- Voz real (ElevenLabs, ~3,0 palavras/s) mudou o plano: o texto v2.2 (2.862 palavras, 4 blocos de TTS ≤ 5.000 caracteres) dá 15:51 de fala; o vídeo se molda à voz (cena.py converte os marcos editoriais at(t) pelos nós de sync.json).
- Pipeline: `gerar_sync.py alinhar` → passada a seco `AJUSTAR=1` → passada a seco → `gerar_sync.py montar` → `render_final.py` (grupos ≤ 3 em paralelo: 6 estouraram a RAM). Master 1080p de 15:58 pronto em `renders/yt_0002_final/`. Detalhes: `videos_longos/yt_0002_lei_gauss_casos_classicos/LEIA-ME_RENDER_FINAL.md`.
- Pendências: entrega formal (falta série/EP) e revisão futura de áudio/sincronização em alguns trechos, a pedido do usuário. WAV e renders ficam fora do Git.
- Dois PCs (trabalho KaioOrtiz / pessoal Pichau): vid_0019–0021 foram feitos no PC de trabalho e integrados à main em 2026-10-11 pela branch pc-trabalho (merge e0820a9). Ver docs/estado_atual.md ("Resumo rápido").
