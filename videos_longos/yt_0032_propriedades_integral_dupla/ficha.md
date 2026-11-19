# Propriedades da integral dupla

Série pública: **CÁLCULO III · EP. 07**

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 07
titulo: Propriedades da integral dupla
disciplina: Cálculo III
modulo: 3.2 Integrais duplas (o docs/mapa_curricular.md do repositório ainda usa a numeração antiga)
bloco: 3.2-T3
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §2.5 (só na descrição do YouTube; nada de livro na tela nem na fala)
unidades: x e y em metros; densidade em kg/m²; massa em kg
solido_3d: nenhum do arsenal Blender (caixas, muro e superfície feitos direto em Three.js, como nos EP. 05 e 06)
3d_threejs: b12 (rampas x² + y² empilhadas), b14 (camadas da chapa de dois metais), b21 (f dentro de g), b22 (chapa entre as lajes 1 e 3), b31 (muro na solda, altura M), b32 (muro de 100, n = 64), b61 (terraplanagem até 8/3), b14k (k = −1: caixas abaixo do chão)
duracao: 18:17,8 (master 1080p30; voz 18:13,8 + cauda do CTA) · narração v3.1, 3.186 palavras, 2,91 palavras/s
```

## Estado

- 2026-11-12 · handoff v1 (`yt_0032_handoff_v1.md`): preview visual silencioso do vídeo inteiro, 960×540 / 15 fps. Sem voz, SRT, master, 1080p nem entrega.
- Arte v1b (pedido do Kaio durante a rodada): chapa de dois metais em metal com degradê e escovado, solda como cordão real (corpo prata,
  bordas, escamas em V) depositado por uma ponta quente que esfria, balança com pivô, fiel, pratos em cuba e inclinação para o lado pesado.

## Estrutura

- `kit.py` (cópia do yt_0031), `v32.py` (cópia do v31.py + câmeras e pontos 3D desta unidade), `lib32.py` (peças desta unidade);
  `sec_h.py`, `sec_a.py`, `sec_b1.py` … `sec_b7.py`, `sec_s.py`; `cena.py` (lotes PH, PA, PB1 … PB7, PS).
- `threejs/`: `r3d.js` + `package.json` (cópia do yt_0031), `cena3d/c32.js` (porte do `referencia/c3d32.html`, estados por quadro) e uma
  página por cena (`b12.html` … `b61.html`). O b32 é o mesmo estado da cena b31 com n = 64 → 1024 e a altura desenhada 2,0 (o render usa a
  página b31 nos dois blocos, para o muro não trocar de cena).
- `ancoras.json` / `duracoes_estimadas.json`: `gerar_ancoras.py` (0,15 + palavras/3 + 0,35 por âncora).
- Render: `./render.sh LOTE` (2D), `./render3d.sh LOTE` (passagem seca → pedidos → r3d.js → render), `./render_todos.sh`, `montar.py`,
  `comparar.py --tudo`, `qa32.py`.

## Preview v1 (2026-11-12)

- `renders/v1/yt_0032_preview_v1_540p15.mp4`: 16 080 quadros = 17:52 (a narração estimada dá 17:49; +3 s do CTA).
- QA em `renders/v1/qa/`: R5 0 · flash 0 · alinhamento 3D 0,00 px (2D e three.js com a mesma câmera) · 8 glyph maps (16 passos) ·
  números do §4 conferidos · tela parada > 3 s: 1 trecho de 3,1 s (B6-4) · prancha `comparacao_v1.jpg` (26 alvos).
- Ritmo: `render_plano.sh` (passada seca + alongamento dos plays antes de esperas longas) e passos extras amarrados à fala.

## Preview v2 (2026-11-12, handoff v2)

- `renders/v2/yt_0032_preview_v2_540p15.mp4`: 17:52 (mesma narração v3). Re-renderizados: PH, PB1–PB7, PS (o PA não mudou).
- Correções: D1–D12 (todo termo com origem; ver `renders/v2/qa/origens_v2.txt`), R1–R9, T1–T7, palco sempre em movimento.
  Cena 3D nova `b14k` (k = −1 abaixo do chão) no modo k do `b14` (c32.js), nível do b61 tracejado, marca z acima do eixo não fica solta.
- QA v2 (`renders/v2/qa/`): R5 0 · flash 0 · alinhamento 0,02 px · 24 passos de glyph map (M1–M13) · 18 frações, todas \dfrac ≥ 26 px,
  \tfrac 0 · \text{} com frase 0 · palco parado > 6 s: 0 (11 trechos de 3–6 s) · rótulo órfão 0 · cartão Fubini 10,3 s.
- Código do v1 guardado em `v1_codigo/`; alvos v2 + v1 válidos em `referencia_v2/`.

## Final (2026-11-13, handoff final)

- Correções C1–C19 (stills em `renders/final/stills/`, prancha `renders/final/correcoes_final.jpg`); narração v3.1 (8 trocas; `narracao_v3.md` guarda a v3).
- Voz: ElevenLabs `eleven_v4`, voz `qw7jgPZWOKrl10GsjQ82`, 5 blocos, `audio/narracao_final.wav` 1093,76 s (QA em `qa/voz.txt`).
- Sincronia: `alinhar_voz.py` → `alinhamento_palavras.json` → `gerar_ancoras.py` (tempo real) → `render_plano.sh`; `qa/sync.txt` e
  `renders/final1080/qa/` (1080p: 265 gatilhos de −0,18 a +0,12 s).
- Final: `render1080.sh` → `montar_final.py` → `videos/montar_master.py` → `renders/yt_0032_master_final_1080p30.mp4` (CRF 14);
  `legenda.srt` (`gerar_srt.py`); `renders/capitulos_final.txt` (`capitulos.py`).
