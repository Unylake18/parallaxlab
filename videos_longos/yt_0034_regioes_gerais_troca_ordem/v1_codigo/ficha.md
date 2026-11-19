# Regiões gerais e troca de ordem

Série pública: **CÁLCULO III · EP. 09**

```
formato: longo_horizontal
tipo: teoria_visual
serie_publica: CÁLCULO III · EP. 09
titulo: Regiões gerais e troca de ordem
disciplina: Cálculo III
modulo: 3.3 Cálculo de integrais duplas (o docs/mapa_curricular.md do repositório ainda usa a numeração antiga)
bloco: 3.3-T2
referencia: Guidorizzi, Um Curso de Cálculo, vol. 3, §3.1, Exemplos 4 a 14 e Corolários 1 e 2 (só na descrição do YouTube; nada de livro na tela nem na fala)
unidades: x e y em metros; densidade em kg/m²; massa em kg; áreas em m²
solido_3d: nenhum do arsenal Blender (a cunha z = y sobre o quarto de disco e o sino z = e^(−y²) sobre o triângulo, feitos direto em Three.js, como nos EP. 05 a 08)
3d_threejs: cena1 = cunha z = y sobre o quarto de disco de raio 2 (b31 faca em pé em x = 1 + pouso lateral = triângulo; b32 faca deitada em y = 1 + pouso lateral = retângulo); cena2 = sino z = e^(−y²) sobre o triângulo 0 ≤ x ≤ y ≤ 1 (b42p faca em pé em x = 0,4, teto curvo, sem pouso; b42 faca deitada em y = 0,6 + pouso lateral = retângulo)
duracao_alvo: ≈ 17 min (narração v2: 3.027 palavras ≈ 16:59)
```

## Estado

- 2026-11-13 · handoff v1 (`yt_0034_handoff_v1.md`): preview visual silencioso do vídeo inteiro, 960×540 / 15 fps. Sem voz, SRT, master, 1080p nem entrega.

## Estrutura

- `kit.py` (cópia do yt_0032), `v34.py` (cópia do v32.py + câmera com fov/ortográfica, pouso lateral `cam_pouso`, pontos das cenas 1 e 2; sem
  mapa de glifos próprio), `lib34.py` (cópia do lib32.py; `junta` devolve à cena a fórmula escrita por partes), `pecas34.py` (vistas, tiras com
  entrada/saída, painel lateral, linha mista, `passo` = TransformByGlyphMap com glifo novo pela caneta ou voo, R5 contínuo).
- Seções: `sec_h.py`, `sec_a.py`, `sec_b1.py` … `sec_b8.py`, `sec_s.py`; `cena.py` (lotes PH, PA, PB1 … PB8, PS; 3D em PB3 e PB4).
- `threejs/`: `r3d.js` + `package.json` (cópia do yt_0032), `cena3d/c34.js` (porte do `referencia/c3d34.html`, estados por quadro: cresce, faca,
  corte, face, sai, zs, câmera perspectiva ou ortográfica), `cena1.html`, `cena2.html`.
- `ancoras.json` / `duracoes_estimadas.json`: `gerar_ancoras.py` (0,15 + palavras/3 + 0,35 por âncora; hífen conta uma palavra, como o §6).
- Render: `./render.sh LOTE`, `./render3d.sh LOTE`, `./render_todos.sh`, `./seco.sh LOTE` (passada seca), `montar.py`, `comparar.py --tudo`, `qa34.py`.

## Preview v1 (2026-11-13)

- `renders/v1/yt_0034_preview_v1_540p15.mp4`: 15 341 quadros = 17:02,7 (narração estimada 16:59,5 + 3 s do CTA); `renders/v1/lotes_v1.json`.
- QA em `renders/v1/qa/`: R5 contínuo (0,5 s, também durante as animações) 0 · flash 0 · alinhamento 3D 0,02 px (rótulos) e 0,01 px (três pousos;
  saída de escala (a) na cena 2) · 31 passos de glyph map (mapas 1–12) · \text{} com frase 0, \tfrac 0 · palco parado > 5 s: 0 (52 de 3–5 s, com a
  fala ao lado) · cartão do próximo vídeo 10,9 s · prancha `comparacao_v1.jpg` (26 alvos).
- Diferenças conscientes dos alvos: alvo 20 (o sb34 sombreia a faixa entre y = x e a parábola; o texto pede a região embaixo da parábola, e é ela
  que está no render); B1-2 → B1-3 (a região genérica volta ao disco); B6-1 painel pequeno no canto de cima (o de baixo é a região); S1 primeiras
  miniaturas à esquerda; cartão do S2 em "como fica a troca" (≥ 8 s).
