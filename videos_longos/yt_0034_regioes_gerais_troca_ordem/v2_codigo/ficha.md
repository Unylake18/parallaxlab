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

## Preview v2 (2026-11-13)

- Handoff v2 (`yt_0034_handoff_v2.md`, referências em `referencia_v2/`):
  - correções D1–D11;
  - conteúdo novo no H1, B1, B2-1, B4-2, B4-3, B6, B7-2 e S1;
  - narração v2.1, que muda só a frase do B1-1 (3.043 palavras ≈ 17:04,9; âncoras regeradas).
- Código do v1 guardado em `v1_codigo/`.
- `renders/v2/yt_0034_preview_v2_540p15.mp4`: 15 423 quadros = 17:08,2 (com os 3 s do CTA).
- 3D, a pedido do Kaio ("muito flat"):
  - os dois sólidos ganharam tom por face (luz fixa), malha escura no teto, contorno e réguas finas nas paredes;
  - a faca é desenhada no lugar, ao longo do perímetro;
  - câmeras novas no B4-2: CAM_B42P (de trás e de cima, o teto curvo aparece) e CAM_B42 (cx 520);
  - a troca entre as duas câmeras anda em arco (`cam_mix(..., arco=True)`), para o sino não crescer até o canto no meio do caminho.
- Palco vivo (§5), com `realce()` em `pecas34.py`:
  - o objeto que a fala lê troca de cor por 1,6 s e volta (cópia mais clara por cima, 1,5 px mais grossa);
  - é guiado por updater de dt, então não bloqueia a cena nem move gatilho;
  - quando vem logo depois de uma marca, começa 0,4 s depois dela (os quadros-alvo ficam sem realce).
- Fins de lote do PB3 e do PB5 em 0,25 s (palco vazio ≤ 0,5 s).
- QA em `renders/v2/qa/`:
  - R5 contínuo 0 · flash 0;
  - folga rótulo × traço ≥ 12 px e painel × palco: 0 (auditoria a cada 0,2 s, também nas animações);
  - 3D × canto 0 de 747 PNGs;
  - alinhamento 3D 0,02 / 0,01 px;
  - 31 passos de glyph map (o mapa 9 é o novo do B4-3);
  - texto em MathTex 0;
  - palco parado > 5 s: 0 · 3–5 s: 2 (B1-1 e B3-1, com a fala ao lado; zero no H1, B4-3, B7-2 e S1);
  - palco vazio 0;
  - cartão do próximo vídeo 10,9 s;
  - prancha `comparacao_v2.jpg` + `.txt` (31 alvos).
- Diferenças conscientes dos alvos:
  - 09, 11, 14, 15 e v2_06: o 3D novo;
  - 14: a placa SEM PRIMITIVA fica embaixo do sólido;
  - v2_12: a 2ª miniatura traz a tira deitada.
- Os 2 quadros de canto sem a linha 2 (93,9 s) são a saída do H2 para o A1, como no v1.
