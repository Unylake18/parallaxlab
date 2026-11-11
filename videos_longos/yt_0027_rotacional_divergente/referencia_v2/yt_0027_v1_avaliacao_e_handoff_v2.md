# yt_0027 · CÁLCULO III · EP. 02 — avaliação do preview v1 e HANDOFF v2 (refazer o visual por quadros-alvo)

Data: 2026-11-10. Entrada: `yt0027_v1_para_claude.zip` (preview 17,45 min, folha de contato, 6 stills).
Unidade: `videos_longos/yt_0027_rotacional_divergente/`. Formato `longo_horizontal`.

**Este handoff substitui toda a parte visual do handoff v1** (§2, §3, §4 e as linhas `tela:` do Anexo A). Continuam valendo do v1: a ficha, a matemática (Anexo B), os fluxos exatos (Anexo C) e a narração do `narracao.md` atual, com as três mudanças do §6. O sistema visual agora é **o mesmo do yt_0026 v7/v8**, que o Kaio aprovou ("bem bom, quase fechar").

O Kaio pediu: "melhorar muito tudo: sobreposições, animações, escalas, álgebra".

---

## 0. Quadros-alvo (a especificação visual)

A pasta `yt_0027_quadros_alvo_v2/` (o Kaio copia para `videos_longos/yt_0027_rotacional_divergente/referencia_v2/`) traz **24 quadros a 1920×1080**, a folha de contato e uma comparação "v1 × alvo".
- **Composição:** o render tem que reproduzir o quadro-alvo na âncora indicada: mesmas posições, escala, cores e texto. **Tolerância:** ±20 px na posição, ±5 % no tamanho.
- **Construção:** `sb27.html` (2D, Canvas + KaTeX) e `c3d27.html` (as três vistas Three.js) têm as coordenadas exatas. Leia o código: os números (origens, unidades, raios, tempos de fluxo) estão lá. No vídeo, as fórmulas são `MathTex` com as mesmas cores e a mesma altura na tela.
- Se algo não der para reproduzir, diga o quê e por quê. Não invente outra coisa.

| quadro | âncora | quadro | âncora |
|---|---|---|---|
| 01 H2 | fim do H2 (t = 3,9 de fluxo, aprox.) | 13 B4-5 | fim do B4-5 |
| 02 H3 | congelamento (t = 3π) | 14 B4-6 | fim do B4-6 |
| 03 B1-3 | fim do B1-3 | 15 B5-2 | meio do B5-2 (setor) |
| 04 B2-2 | fim do B2-2 | 16 B5-2 | fim do B5-2 (caixa) |
| 05 B2-3 | fim do B2-3 | 17 B6-1 | fim do B6-1 |
| 06 B2-4 | fim do B2-4 | 18 B6-2 | meio do B6-2 (eixo a 50°) |
| 07 B2-5 | fim do B2-5 | 19 B6-3 | fim do B6-3 |
| 08 B3-1/2 | fim do B3-2 | 20 F1 | fim do F1 |
| 09 B3-4 | fim do B3-4 | 21 F2 | fim do F2 |
| 10 B3-6 | fim do B3-6 | 22 B7-3 | fim do B7-3 |
| 11 B4-2 | fim do B4-2 | 23 B7-4 | meio do B7-4 |
| 12 B4-4 | fim do B4-4 | 24 S2 | fim do S2 |

---

## 1. Avaliação do v1 (o que estava errado)

O que funcionou e fica: a matemática (todos os números do QA batem), o fluxo exato, o canto alto com a placa do tamanho do texto (`fundo27.py`), o verde-menta sem contorno e sem brilho, a ordem das cenas e a sincronia por gatilhos.

O que não funcionou:
1. **Escala:** o desenho ocupa pouco do palco, enquanto as rodinhas, braços e quadradinhos ficam minúsculos (rodinha com ~45 px). Há grandes vazios no meio da tela.
2. **Setas de campo:** são irregulares (fora da grade) e esparsas. Com o comprimento proporcional, viram tracinhos e pontinhos (no vórtice, no B1 e no F). O handoff v1 pedia isso; a regra do yt_0026 v7 (comprimento comprimido) resolve.
3. **Pontinhos de fluido no fundo:** o Kaio já tinha recusado isso no yt_0026 ("nunca pedi isso"). Eles sujam todas as cenas de palco (B1, B2, B4, F).
4. **Objetos de teste andando pelo campo:** no B2, a cruz dos braços é levada pela correnteza, fica pequena, sai do centro e os rótulos `2 rad/s` e `3/2 rad/s` se separam dela. No B3-1, a cruz vira um arco comprido.
5. **Laços:** o quadradinho do B4-1 e o setor do B5-2 crescem e voltam ao começo várias vezes. Parece um bug.
6. **Tinta em xadrez:** no vórtice, vira uma nuvem de anéis finos e não mostra a espiral.
7. **Lupa com linhas de chamada** (B1-2, B4-5): um círculo solto ligado por linhas a um quadradinho de 10 px. Os números da caixa aparecem um por vez, sem histórico.
8. **3D:** há sombra no chão (cubo e rodinha), cones grossos, setas de frente virando bolinhas e uma barra `RAPIDEZ DO GIRO`. Sombras e barras estão proibidas desde o yt_0026 v7.
9. **Sobreposições:** `2 rad/s` sob o braço, `0,927` colado na borda do furo, rótulos sobre setas, fórmulas do B4-4 muito pequenas.
10. **Álgebra:** fórmulas pequenas e soltas, uma só por vez, sem o passo que explica (por exemplo, a regra do quociente no vórtice). Faltava a coluna de fórmulas organizada.
11. **Trechos parados** (B7-4 por até 4,8 s): o aquecimento acabava antes da fala.
12. **A1:** dois ícones minúsculos soltos no meio da tela.

Causa principal: o handoff v1 foi escrito sobre o sistema visual v4/v5 do yt_0026 (brilho, contorno, chapas, tinta), que o próprio yt_0026 abandonou no v7. A culpa é do handoff, não da implementação.

---

## 2. Sistema visual (igual ao yt_0026 v7/v8)

### 2.1 O que sai do vídeo (em todas as cenas)
1. **Pontinhos/partículas de fluido** (fundo, B1, B2, B4, F, S): apagar o helper e todas as chamadas. Um ponto só aparece quando é *o* ponto da explicação: A, B, C, P, os vizinhos de P no B7-3, ou o ponto que anda com a sua seta no B1-1.
2. **Tinta em xadrez.** No hook, ela vira **uma fita só** (§4, H).
3. **Lupa com linhas de chamada** (B1-2 e B4-5).
4. **Laços** de animação: cada movimento roda **uma vez**. Se a cena precisa mostrar o antes, o estado inicial fica como fantasma tracejado.
5. **Sombra, névoa e barras** no 3D (nenhum `ShadowMaterial`/`castShadow`/`Fog`) e a barra `RAPIDEZ DO GIRO`.
6. **Brilho, contorno ou transparência** nas setas (continua como no v1).
7. A regra "nenhum trecho parado acima de 1,5 s" **deixa de valer**, porque foi ela que gerou os pontinhos. Agora: parado no máximo 3 s, e nunca preencher com efeito. Se a fala continua e a cena acabou, o próximo passo da cena entra mais cedo.

### 2.2 Escala fixa (a mesma em todo o vídeo)
| layout | onde | geometria a 1080p |
|---|---|---|
| **A · palco + fórmulas** | B1-1/2, B2, B3-1/2, B3-4, B4, B5-1/2, B6, F, B7 | origem do palco em **(600, 540) px**, **1 u = 120 px** (um quadrado da grade grossa); campo até r ≈ 3 u (x 240–960, y 180–900). Coluna de fórmulas alinhada à esquerda em **x = 1120 px**. |
| **B · dois painéis** | H, B3-3, B5-3, S2 | painéis 700×560 com só a moldura (borda `#B8C4DA` a 35 %, raio 14, **sem preenchimento**, v8), em x 130–830 e 1090–1790, y 260–820; origens em **(480, 540)** e **(1440, 540)**; **1 u = 96 px**. Texto embaixo, centrado em y ≈ 900–960. |
| **C · cartões** | B1-3, S1, S4 | três cartões de 480×460 em x = 140, 720 e 1300, y 250–710 (1 u = 56 px); texto embaixo. |
| **rio** | B3-5/6 | faixa de x 96 a 1824, origem (960, 500), 1 u = 90 px, \|y\| ≤ 3 u; fórmulas embaixo em y ≈ 940. |

Todas as origens caem num cruzamento da grade grossa. Conversão para o Manim: x_m = (x_px − 960)/135; y_m = (540 − y_px)/135.

### 2.3 Setas de campo
- **Forma:** só a flecha: haste de 5 px e ponta cheia de 19–20 px a 1080p. Opacidade 1.
- **Posição:** centrada no ponto da grade, com passo de **0,5 u no palco** (60 px) e 0,6 u nos painéis.
- **Comprimento comprimido:** L = Lmax·(0,4 + 0,6·t), com t = min(1, |F|/mmax) e Lmax = 0,84 × passo. Cor de `#2EE6A0` (t = 0) a `#8CFFD2` (t = 1). Pular r < rmin (o centro e o furo ficam limpos).
- **Hook e tornado:** as setas ficam em **anéis** (r = 1; 1,5; 2; 2,5), com espaçamento de 0,62 u ao longo do anel. Assim existe um anel exatamente em r = 1, onde os dois campos coincidem. O mmax é **comum aos dois painéis** (2,5); é ele que faz "a seta de fora maior à esquerda e menor à direita".
- **Campo de contexto:** quando o objeto de teste é o assunto (braços, caixa, rodinha), o campo vira a mesma seta em `#1A5F55` opaco. Nunca usar opacidade.
- Se o kit do yt_0026 v7 já tem esse helper, **copie** (não importe).

### 2.4 Objetos de teste (grandes e parados no lugar certo)
- **Rodinha:** 4 pás coral (largura 0,30 R), cubo escuro com anel coral; a **pá marcada é a pá inteira em azul-claro** `#A9CCFF` (a faixa do v1 não aparecia). Raio: 0,42 u no hook (40 px), 1,05 u no B2 (126 px), 0,30–0,38 u no tornado e no rio.
- **Braços:** traço coral de 7 px com pontas de 10 px. O B2 é **na origem** do campo (−y, 2x), onde F = 0: os braços giram sem ser levados, e a cruz fica parada no centro do palco. Isso muda o v1 (A = (0,5; 0,25)); a fala não muda.
- **Quadradinho, setor e caixa:** com o tamanho do quadro-alvo.
- **Giro:** arco violeta de 4 px com ponta (↺/↻), colado no objeto.

### 2.5 Cores (sem mudança no aprovado; dois ajustes)
- Campo verde-menta. Componentes P, Q, R e F⃗ também verde-menta. x âmbar, y magenta, **z ciano `#35D9FF`** (era verde, e ficava parecido com o campo). ω, rot e arcos de giro em violeta; o número do div e o saldo em azul-claro; objetos de teste em coral.
- **∇φ** em verde-menta (é um campo); φ e T em azul-claro. Pontos da explicação (A, P, vizinhos) em laranja `#E08A3C`, como no yt_0026.
- **Física:** E⃗ verde-menta (campo), B⃗ magenta, fio carregado azul `#267BFF` com `+`, fio com corrente verde `#3FE08B` com ⊙.

### 2.6 Texto e rótulos
- Todo rótulo solto (A, B, C, h, k, x₀, `2 rad/s`, números da caixa, `div = 0`, `FIO CARREGADO`, P) ganha a **placa mínima** do v8: `#091226` a 85 %, padding 4–6 px, sem borda.
- **Nenhum rótulo sobre seta ou traço:** a distância mínima entre a caixa do texto e qualquer seta ou traço é de 6 px. Se colidir, mova o rótulo, nunca o desenho.
- Canto como está (v8 com `fundo27.py`). Painéis sem preenchimento.

### 2.7 Álgebra
- **Coluna de fórmulas** em x = 1120 px, alinhada à esquerda, com as linhas e alturas do quadro-alvo. As fórmulas **ficam** na tela enquanto a cena dura: a coluna é o "quadro" da aula. Uma fórmula só sai quando a cena troca.
- **Alturas:** fórmula principal com KaTeX 52–56 px no alvo; secundária 40–46 px. Ajuste o `font_size` do `MathTex` até a altura na tela bater (±5 %). Nada menor que 38 px.
- **Caneta** em toda fórmula nova (sem flash). `TransformByGlyphMap` onde a conta continua a anterior:
  - B2-2: `≈` com quociente → `= ∂Q/∂x`;
  - B2-5: a forma geral → os números;
  - B3-2: o meio da regra do quociente → o resultado;
  - B4-5: `2 − x² − y²` → `2 − 1 − ¼ = 0,750`.
- **A conta aparece inteira** onde a fala diz "fazendo as derivadas" (B3-2), "a conta confirma" (B3-6) e "as derivadas dizem o mesmo" (B5-2, fala nova). As linhas estão nos quadros 08, 10 e 15 e foram conferidas no sympy (bloco V2 de `verifica_calc3_t2_sympy.py`).

---

## 3. 3D (Three.js): três vistas, simples
Material, luz e setas como no `f27.js`, **sem sombra, sem névoa, sem chão**. Fundo transparente, composto sobre o milimetrado (como na tigela do yt_0026 v7). Construção e câmera em `c3d27.html`.
1. **`cubo` (B6-1, quadro 17):** cubo de aresta 1,6, faces opacas em três tons e arestas claras. Uma seta grande por face (centro) e 4 menores, com o campo (x, y, z) a partir do centro. Câmera fixa em (4,6; −5,4; 2,6); no máximo 20° de órbita no bloco inteiro. As setas crescem face por face (`GrowArrow` 3D).
2. **`roda` (B6-2 e B6-3, quadros 18 e 19):**
   - O giro rígido em torno de W, inclinado 35°, aparece como 2 anéis de 10 setas finas (raio 1,9, alturas ±0,9 ao longo de W) e uma linha-guia escura.
   - A rodinha de pás 3D tem 4 pás coral (0,8 × 0,55), a pá marcada em azul-claro, um eixo GEO e um cubo escuro.
   - B6-2: o eixo n sai de W e inclina até ficar ⟂ a W em 6 s. A rapidez em cada quadro é W·n (fase = ∫ W·n dt). O eixo do giro aparece tracejado. Na coluna, o número `ω_roda = 1,00 → 0,00 rad/s` em violeta (`DecimalNumber`) substitui a barra.
   - B6-3: n volta a W em 2 s e a seta violeta do rot cresce ao longo de W (comprimento 2|W| na escala da cena). O determinante e as notações entram na coluna (quadro 19).
   - Câmera fixa em (6,4; −5,6; 2,4).

Relatório: custo por quadro e alinhamento (≤ 2 px) como no v1.

---

## 4. Cena por cena (animação)

Tempos de fluxo e escalas estão no `sb27.html`. "Fluxo exato" quer dizer: as fórmulas do Anexo C do v1. Câmera lenta é permitida (registre o fator), mas sempre com um fator só por cena.

### H · dois redemoinhos (layout B, sem canto; quadros 01 e 02)
- **H1:**
  - Os painéis entram (`Create` da moldura).
  - O campo cresce anel por anel, do centro para fora, nos dois painéis ao mesmo tempo.
  - A **fita de tinta** é desenhada: uma faixa azul-clara (`#7FB2FF` a 50 % com uma linha `#A9CCFF` fina, largura 0,15 u = 14 px), radial, de r = 0,75 a 2,5, apontando **para cima**. Ela fica por baixo das setas.
  - As rodinhas pousam em (1, 0), com a pá marcada para cima.
- **H2:**
  - O fluxo exato corre de t = 0 a 2π (uma volta) **sincronizado com a fala**. "No primeiro…" mostra o painel esquerdo; "completou um giro" cai em t = 2π.
  - Depois o fluxo continua até t = 3π, durante "No segundo… a pá marcada fica apontando para cima".
  - À esquerda, a fita gira inteira e reta, e a rodinha gira junto. À direita, a fita se enrola em espiral (quadro 02) e a rodinha nunca muda de orientação.
- **H3** (quadro 02):
  - Tudo congela em t = 3π.
  - A circunferência r = 1 é desenhada (`#A9CCFF`, 4 px).
  - As setas do anel r = 1 engrossam **aos pares** (a mesma posição nos dois painéis ao mesmo tempo, 8 pares em ~2 s; 7 px, `#8CFFD2`).
  - Entra a frase `AS MESMAS SETAS. POR QUE SÓ UMA GIRA?`.

### A1
Abertura padrão do yt_0026 (logo, `BEM-VINDOS AO PARALLAX LAB`, título `ROTACIONAL E DIVERGENTE`, linha `NESTE VÍDEO: GIRO · ESPALHAMENTO · NUM PONTO SÓ`). **Sem os ícones.** O canto entra no fim.

### B1 · um pedacinho de fluido
- **B1-1:**
  - Palco com o campo (−y, 2x), grade completa.
  - **Um** ponto laranja anda pela trajetória exata, levando a sua seta de velocidade (seta verde-menta presa ao ponto, comprimento real × 0,4). O rastro tracejado GEO fica.
  - O selo `CAMPO = VELOCIDADE · ESCOAMENTO ESTACIONÁRIO · CAMPO LISO` vai na coluna (legenda azul-clara, três linhas), não numa caixa.
- **B1-2:**
  - O palco **aproxima** em volta de um ponto (escala do grupo, 3 passos ×2, ×4, ×8). A cada passo, as setas são **refeitas** com o mesmo espaçamento na tela (crossfade de 0,4 s) e vão ficando quase iguais.
  - A diferença entre duas setas vizinhas é marcada por um segmento coral entre as pontas.
  - A caneta escreve `\dfrac{\Delta \vec F}{h} \;\to\; \dfrac{\partial \vec F}{\partial x}` na coluna.
  - Sem lupa e sem linhas de chamada.
- **B1-3** (quadro 03): os três cartões. Em cada um, o quadrado coral faz o movimento uma vez (girar, crescer, esticar), com o original tracejado. `ROTACIONAL` e `DIVERGENTE` entram embaixo na fala.

### B2 · rotacional (layout A; quadros 04 a 07)
- **B2-1:**
  - O campo (−y, 2x) entra **cheio**.
  - Quando o braço aparece, o campo passa a contexto (escuro, 0,6 s).
  - O braço AB vai de (0, 0) a (1,5; 0).
- **B2-2** (quadro 04):
  - A seta de velocidade em B cresce: (0, 3), comprimento real × 0,4.
  - O braço gira pelo fluxo exato de t = 0 a 0,28 em ~2 s, com o fantasma tracejado no lugar inicial e o arco violeta.
  - Fórmulas na coluna: a linha 1 vira a linha 2 por `TransformByGlyphMap`.
- **B2-3** (quadro 05):
  - O braço AC vai de (0, 0) a (0; 1,5). A seta em C é (−1,5; 0).
  - O braço gira pelo fluxo exato de t = 0 a 0,15.
  - A miniatura da regra geral (braço tracejado, duas setas para a direita, a de cima maior, arco horário, `HORÁRIO ⇒ sinal −`) entra na frase "se a ponta de cima anda para a direita mais rápido…".
  - Na frase "Neste campo…", entra a linha de baixo.
- **B2-4** (quadro 06):
  - Os dois braços juntos pelo fluxo exato de t = 0 a 0,5: a tesoura abre (2 e 1 rad/s).
  - Os rótulos violeta `2 rad/s` e `1 rad/s` acompanham a ponta de cada braço, por fora, com placa.
  - Na frase "uma rodinha de pás não vira tesoura", os braços viram tracejado e a **rodinha grande** (R = 1,05 u) entra no centro, girando a 1,5 rad/s até o fim da âncora.
  - A coluna mostra 2, 1 e a média.
- **B2-5** (quadro 07): a rodinha continua girando, entram o arco ↺ e `⊙ k⃗`. Na coluna, quatro linhas; a última sai da primeira por `TransformByGlyphMap`.
- **B2-6:**
  - Mesmo layout A, com o campo (−y, x) em anéis (como o painel esquerdo do hook), a fita e a rodinha em órbita (uma volta).
  - Coluna: `\vec F = (-y,\ x)`; `\dfrac{\partial Q}{\partial x} = 1,\quad \dfrac{\partial P}{\partial y} = -1`; `\operatorname{rot}\vec F = \bigl(1 - (-1)\bigr)\vec k = 2\,\vec k`; `\omega = 1`.
  - Na frase da vorticidade, entra a legenda `VORTICIDADE = 2ω (CORPO RÍGIDO)`.

### B3 · dois enganos
- **B3-1/2** (quadro 08):
  - Vórtice no palco (furo r = 0,55).
  - Cruz com braço radial de (1,35; 0) a (2,25; 0) e braço tangencial de (1,8; −0,45) a (1,8; 0,45).
  - Fluxo exato de t = 0 a 1,07 (o centro anda 0,33 rad) em ~3 s. O fantasma tracejado e o arco da órbita ficam. No fim, entram os arcos ↻ (radial) e ↺ (tangencial).
  - Depois a cruz vira tracejado e uma rodinha (R = 0,4) entra no centro e anda mais 2 s pela órbita **sem girar**.
  - Coluna: a regra do quociente completa para ∂Q/∂x, a linha de ∂P/∂y, `rot F = 0` e o domínio.
- **B3-3:**
  - Layout B com os dois campos do hook (sem fita), o anel r = 1 aceso.
  - Na frase "a seta de fora é mais forte / mais fraca", a seta do anel r = 1,5 na mesma posição angular nos dois painéis ganha um anel coral (r = 0,32 u) em volta.
  - Embaixo: `\vec F\ \text{irrotacional} \iff \operatorname{rot}\vec F = \vec 0`.
- **B3-4** (quadro 09):
  - Os painéis saem e o palco do tornado cresce anel por anel: o miolo r < 1 com o giro rígido e o lado de fora com o vórtice, colados na circunferência.
  - Rodinha de dentro girando (arco ↺), rodinha de fora em órbita sem girar.
  - Coluna: `MODELO DE TORNADO` e as quatro linhas.
- **B3-5/6** (quadro 10):
  - O rio, as margens e o perfil parabólico à esquerda (`Create`). Sem tinta.
  - Rodinhas presas (3 linhas × 3), girando a y/9 com câmera rápida ×3 (registrar), para o giro aparecer: em y = 1,8, ~0,6 rad/s na tela.
  - Na frase "A conta confirma", o mapa violeta entra com os `+` e `−` e as fórmulas embaixo.

### B4 · divergente
- **B4-1/2** (quadro 11):
  - Explosão (x, y) cheia.
  - O quadrado coral (lado 0,7 em (1,25; 0,85)) anda pelo fluxo exato de t = 0 a 0,35, **uma vez**, com o fantasma tracejado.
  - A legenda `ÁREA` conta de 0,49 a 0,99 durante o movimento.
  - Coluna conforme o quadro.
- **B4-3/4** (quadro 12):
  - O campo vira contexto. A caixa [0,5; 2]² é desenhada (chapa a 55 %).
  - As setas das paredes crescem com a fala: primeiro direita e esquerda (só a componente horizontal), depois cima e baixo. Escala de 0,45 u por unidade de campo, e as de entrada ficam visivelmente menores.
  - h, k, x₀ e x₀ + h com placa. Coluna com 3 linhas na fala.
- **B4-5** (quadro 13):
  - Campo da fonte-anel. Os quadrados aninhados de lado 1, ½, ¼ e ⅛ em (1, ½) aparecem **um por frase** ("encolhe… de novo… de novo"), e a cada um entra a linha da tabela.
  - O último é coral. **Sem lupa:** os quadrados ficam no palco, na escala do palco.
  - Depois, a seta ↓ e as duas linhas de baixo.
- **B4-6** (quadro 14):
  - Disco de luz (r < √2) com `+`, anel de sombra com `−`, círculo tracejado com `div F = 0` (placa).
  - Dois quadrados: dentro cresce, fora encolhe (uma vez, com fantasmas).
  - Coluna com as legendas e as duas linhas de física (água, bomba de bicicleta).

### B5 · a falsa fonte
- **B5-1:** palco com a falsa fonte e o furo; `\vec F = \dfrac{(x,\ y)}{x^2+y^2}` na coluna.
- **B5-2a** (quadro 15): o setor coral anda pelo fluxo exato de t = 0 a 2, **uma vez** (raios finais 2,33 e 2,56), com o fantasma tracejado. Entram as duas derivadas e `div F = 0`, e a legenda de área (`0,28 → 0,28`).
- **B5-2b** (quadro 16): o campo vira contexto. A caixa [1, 2] × [−½, ½], as quatro setas das paredes e os números junto de cada parede. Coluna: `ENTRA`, `SAI` com a soma, `saldo = 0`.
- **B5-3:** layout B, explosão × falsa fonte, `div = 2` e `div = 0` embaixo.

### B6 · no espaço
Quadros 17, 18 e 19 (ver §3).

### F · na física
- **F1** (quadro 20):
  - Volta o palco da falsa fonte. O furo se enche com o disco azul com `+` e o rótulo `FIO CARREGADO` (placa).
  - Coluna:
    - `\vec E = \dfrac{\lambda}{2\pi\varepsilon_0}\,\dfrac{(x,\ y)}{x^2+y^2}`, com a legenda `= FALSA FONTE × CONSTANTE`;
    - `\nabla\cdot\vec E = \dfrac{\rho}{\varepsilon_0}`;
    - a linha "fora do fio";
    - `A CARGA MORA NO FURO` em azul.
- **F2** (quadro 21): volta o vórtice. As setas passam de verde-menta a **magenta** em 1 s; o furo vira o disco verde com ⊙. Coluna conforme o quadro.

### B7 · laplaciano
- **B7-1:**
  - Palco com as curvas de nível de φ = x² + y² (círculos azul-claros com os valores 1–4, placa).
  - O gradiente (2x, 2y) entra cheio, em verde-menta.
  - Coluna: `\nabla^2\varphi = \nabla\cdot\nabla\varphi`.
- **B7-2:** as linhas da conta na coluna; o gradiente vira contexto.
- **B7-3** (quadro 22):
  - O ponto P = (1, ½) laranja, a circunferência tracejada de raio 0,4 e os 8 vizinhos laranja acendendo em volta.
  - Coluna com os dois números (`φ(P) = 1,25` e `1,41`) e as linhas de baixo. **Sem barras.**
- **B7-4** (quadro 23):
  - A chapa ocupa o palco inteiro (720×720 px), com o mapa frio→quente.
  - O aquecimento usa o núcleo exato com o tempo **esticado para durar a âncora toda** (t de 0 a 1,5 ao longo da fala), para não sobrar tela parada.
  - O rótulo `∇²T > 0 / ESQUENTA` fica no ponto frio. Coluna com a equação e as legendas.

### S · resumo
- **S1:** layout C com dois cartões (x = 280 e 1160, 480 de largura). À esquerda, a rodinha girando, com a fórmula do rot embaixo. À direita, a caixa com as setas saindo, com a fórmula do div embaixo.
- **S2** (quadro 24):
  - Layout B: vórtice magenta com o fio de corrente e falsa fonte verde-menta com o fio carregado (campos em contexto).
  - O laço e a cerca acendem com as setas de circulação e de fluxo; os laços longe ficam tracejados, com `0`.
  - Embaixo, as duas linhas.
- **S3:** os dois painéis encolhem e sobem. No centro entra `DO LOCAL AO GLOBAL` (Bold 56); embaixo, `GREEN · STOKES · GAUSS`, um por vez.
- **S4:** os três cartões do B1-3 voltam por ~2 s (a dica) e depois entra o CTA padrão.

---

## 5. Narração
Fica a do `narracao.md` atual (2.686 palavras). Mudam só três falas; regenere o `ancoras.json`:
- **B5-2:** depois de "…a área não muda.", acrescentar: "As derivadas dizem o mesmo: as duas parcelas do divergente se cancelam."
- **F1:** depois de "…em volta de um fio comprido carregado, visto de frente.", acrescentar: "É a nossa falsa fonte, multiplicada por uma constante."
- **F2:** depois de "…em volta de um fio com corrente.", acrescentar: "De novo, o nosso vórtice vezes uma constante."

Duração: continua em ~17 min. Não corte nada por conta própria; o corte é decisão do Kaio (§9 do handoff v1).

---

## 6. QA desta rodada
1. **Lado a lado:** 24 stills de 1920×1080, o render à esquerda e o quadro-alvo à direita, na âncora da tabela do §0. Para cada um, liste o que diverge (posição em px, tamanho em %).
2. **`[proibidos]`:** busca no código da unidade por pontinhos/partículas, `ShadowMaterial`, `castShadow`, `Fog`, brilho ou contorno de seta, lupa com linhas de chamada e barras. Tem que dar **zero**.
3. **`[campo]`:** a menor seta ≥ 0,4 × a maior em cada família; nenhuma seta de campo com opacidade < 1; setas centradas na grade (erro ≤ 1 px).
4. **`[colisão]`:** a menor distância entre cada rótulo ou fórmula e qualquer seta ou traço deve ser ≥ 6 px. Liste os casos.
5. **`[escala]`:** as origens e a unidade de cada cena conferem com o §2.2.
6. **`[laços]`:** nenhum objeto volta ao estado inicial dentro da mesma âncora.
7. **Matemática e fluxo:** os mesmos números do v1, mais o tesoura em t = 0,5 (pontas em (1,140; 1,378) e (−0,689; 1,140)), a cruz do vórtice em t = 1,07 e `ω_roda = cos 50° = 0,64` no quadro 18.
8. **Parados > 3 s:** listar.
9. Sincronia, `FLASH POR QUADRO` = 0, canto e fundo, como no v1.

## 7. Entrega
1. **Primeiro, os 24 lado a lado** e a lista de divergências (pode mandar antes do preview).
2. Depois, o preview inteiro a 960×540 / 15 fps, a folha de contato e o pacote `zip_claude.py` com os lado a lado.
3. **Não fazer:** voz, SRT, master, 1080p final, entrega, commit ou push. Não alterar `template/`, `assets/`, `docs/` nem o yt_0026 (só copiar dele).
