# Dá para medir a luz com chocolate?

formato: curto_vertical
Série pública: **ABSURDO CALCULÁVEL · EP. 04** (aprovada pelo Kaio em 2026-11-01)

Fase: **final entregue (2026-11-02)**. Master e legendado 1080×1920 / 30 fps, CRF 14, 152,0 s. Voz ElevenLabs v4 (`qw7jgPZWOKrl10GsjQ82`) em **um bloco
contínuo** (`narracao_tags_v3.md` → `audio/narracao_v3.wav`, 150,7 s, 463 palavras, sem pausas inseridas). Sincronia por palavra:
`alinhar_voz.py` (forced alignment) → `sync_voz.py` reescreve o `timeline.json` com cada evento 0,12 s antes da palavra que o narra
(pior atraso medido no render a 30 fps: +0,09 s). 3D: Three.js (`render3d.js`, 1080×1920/30 fps, 0,37 s/quadro); Manim: render em 6 faixas de animações
(`-n`, uma pasta `media_fN` cada) e composição por `compor.py --midia media_f0,...`. Legenda `gerar_legenda.py` + `legenda_cores.py`
(`montar_legendado.py`, estilo padrão como vid_0027 e vid_0028). Preview 540×960 com voz: `renders/preview_v5_540x960.mp4`.
disciplina: Física II
bloco: Oscilações e ondas
modulo: 5.4 Superposição, interferência e ondas estacionárias (ponte: 6.12 / 7.1, velocidade da luz)
referencia: Sears e Moysés vol. 2 (ondas estacionárias); só na descrição, nunca na tela
headline: DÁ PARA MEDIR A LUZ COM CHOCOLATE?
pergunta_central: Por que duas manchas de chocolate derretido revelam o comprimento de onda do micro-ondas, e daí a velocidade da luz?
payoff: no modelo ideal, as manchas ficam a meio comprimento de onda; com a frequência do forno, c = 2·d·f ≈ 3,0·10⁸ m/s
duracao_alvo: ~150–160 s com voz (preview silencioso segue os tempos do §7)
3d_threejs: C01 (forno, prato parado, barra derretendo, câmera até a vista de cima)
solido_3d: nenhum do arsenal Blender (não há cavidade nem forno no arsenal); geometria nova em Three.js
