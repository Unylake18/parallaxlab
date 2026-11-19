# Jacobiano e mudança de variáveis

Série pública: **CÁLCULO III · EP. 11**

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 11
titulo: Jacobiano e mudança de variáveis
disciplina: Cálculo III
modulo: 3.4 Mudança de variáveis na integral dupla — o docs/mapa_curricular.md do repositório ainda usa a numeração antiga
bloco: 3.4-T1
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, cap. 4 (§4.1 Preliminares; §4.2 teorema e Exemplo 1); Stewart, seção de mudança de variáveis em integrais múltiplas (só na descrição do YouTube; nada de livro na tela além do "como no livro" da fala)
unidades: sem unidade (matemática pura)
solido_3d: nenhum do arsenal Blender (a única peça 3D, o produto vetorial em pé sobre um paralelogramo, é feita direto em Three.js)
3d_threejs: cena1 = o produto vetorial em pé (B4-2): o paralelogramo das setas ∂φ/∂u Δu e ∂φ/∂v Δv no chão, o vetor (∂φ/∂u Δu) ∧ (∂φ/∂v Δv) subindo em k com altura = área; decolagem da vista de cima (= o 2D do zoom), câmera oblíqua parada, pouso de volta na vista de cima
duracao_alvo: ≈ 22:36 (narração final v2: 4.071 palavras a 3 palavras/s)
duracao_real: 21:45,67 (master 1080p30; voz 21:41,68 = 3,13 palavras/s + 3,99 s do logo do CTA)
```

## Estado

- **2026-11-15 · FINAL entregue** (handoff final: K1–K16, narração final v2, voz ElevenLabs v4, sync, SRT, 1080p30, master CRF 14):
  `renders/yt_0036_master_final_1080p30.mp4` (21:45,67), `legenda.srt` (344 blocos), `renders/capitulos_final.txt`; preview com voz
  `renders/final/yt_0036_preview_final_540p15_voz.mp4`; entrega em `entregas/Cálculo III - EP 11 - Jacobiano e mudança de variáveis - 0036/`.
- **2026-11-15 · preview v2** (sem voz): `renders/v2/yt_0036_preview_v2_540p15.mp4` (21:42,53), papel na tela inteira.

- **2026-11-14 · preview v1** (só visual, sem voz): `renders/v1/yt_0036_preview_v1_540p15.mp4`, 960×540 / 15 fps, tempo pela
  narração v1 estimada (`ancoras.json`, `duracoes_estimadas.json`). Fundo violeta de Cálculo (papel v2). Voz, SRT, master e 1080p não iniciados.

## Estrutura

| lote | arquivo | blocos | alvos |
|---|---|---|---|
| PH | `sec_h.py` | H1, H2 | 01, 02 |
| PA | `sec_a.py` | A1 | 03 |
| PB1 | `sec_b1.py` | B1-1, B1-2 | 04 |
| PB2 | `sec_b2.py` | B2-1 | 05 |
| PB3 | `sec_b3.py` | B3-1, B3-2, B3-3 (+ início do B4-1) | 06, 07 |
| PB4 | `sec_b4.py` | B4-1, B4-2 (3D), B4-3 | 08–11 |
| PB5 | `sec_b5.py` | B5-1 … B5-4 | 12, 13 |
| PB6 | `sec_b6.py` | B6-1 … B6-4 | 14, 15 |
| PB7 | `sec_b7.py` | B7 (PAUSE E TENTE) | — |
| PB8 | `sec_b8.py` | B8 (Mercator, fluidos) | — |
| PS | `sec_s.py` | S1, S2 (cartão do próximo) | 16 |

- Kit: `kit.py`, `v36.py`, `lib36.py`, `pecas36.py`, `p36.py` (cópia renomeada do kit do yt_0035); peças deste vídeo em `j36.py`.
- 3D: `threejs/cena3d/c36.js` (porte de `referencia/c3d36.html`), pedidos em `threejs/pedidos3d/`, quadros em `threejs/q3d/`.
- Contas conferidas em `verificacao/` (sympy, 41/41).

## Comandos

```bash
./render.sh PB4            # um lote (preview 960×540 / 15 fps)
./render3d.sh PB4          # 3D do B4-2 (passada seca → pedidos → node r3d.js)
../../.venv/Scripts/python.exe montar.py v1
../../.venv/Scripts/python.exe comparar.py --tudo
../../.venv/Scripts/python.exe qa36.py
```
