# yt_0030 · CÁLCULO III · EP. 04 · Exercícios do módulo 3.1
# HANDOFF v1 · preview silencioso do vídeo inteiro (540p, 15 fps)

2026-11-11. Produção → Claude Code. Este documento é **autocontido**: tudo o que a implementação precisa está aqui e na pasta `yt_0030_quadros_alvo_v1/` do zip (29 quadros-alvo 1920×1080, a folha de contato e o gerador `sb30.html`, que é a fonte exata de posições e cores).

Fase aberta: **preview visual silencioso**. Sem voz, sem SRT, sem 1080p, sem master, sem entrega, sem commit e sem push.

O briefing (matemática, física, roteiro, cores e quadros) é especificação de implementação. Se achar uma inconsistência objetiva, reporte antes de mudar o escopo.

---

## 0. O que entregar

1. A unidade nova `videos_longos/yt_0030_<slug>/` (sugestão: `yt_0030_exercicios_modulo_31`), com `ficha.md` (§1), `cena.py`, `tempos.py` (§6) e `renders/`.
2. O preview inteiro: `renders/v1/yt_0030_preview_v1_540p15.mp4` (960×540, 15 fps, sem áudio).
3. A prancha **render × alvo** dos 29 quadros: `renders/v1/qa/comparacao_v1.jpg` + `.txt` (§8).
4. Os relatórios de QA em `renders/v1/qa/` (§8): `alinhamento_v1.txt`, `sobreposicoes_v1.txt` (R5), `setas_na_chapa_v1.txt` (R7), `transicoes_v1.txt` (R10), `holds_v1.txt` e `numeros_v1.txt`.
5. O relatório de entrega do AGENTS.md.

---

## 1. Ficha

```
formato: longo_horizontal
Série pública: **CÁLCULO III · EP. 04**
# Exercícios do módulo 3.1: campos, rotacional, divergente, limite e derivadas parciais
disciplina: Cálculo III
bloco: 3 · Funções de várias variáveis a valores vetoriais
modulo: 3.1 · Campos vetoriais, rotacional, divergente, limite, continuidade e derivadas parciais
item: 3.1-E1 · exercícios integradores do módulo
referencia: Guidorizzi vol. 3 (exercícios 1.1–1.5 e §1.6) e Stewart cap. 16, só como inspiração e régua de rigor (nada disso aparece na tela ou na fala)
duracao_alvo: ≈ 26:12 de fala (4.715 palavras a 3 p/s); vídeo ≈ 27–28 min; teto ~30 min
quadros_alvo: yt_0030_quadros_alvo_v1 (29)
sistema_visual: o do EP. 03 (yt_0028 v4/v5): fundo violeta liso + grade que nasce dos eixos (assets/calculo/papel.py v2), variante B (FUNDO_PAINEL = "grade")
3d_threejs: nenhuma cena (decisão do Kaio: 2D simples e bem feito, com movimento; o 3D atrapalha a leitura dos vetores)
solido_3d: nenhum do arsenal Blender
anterior: yt_0028 · EP. 03 (o gancho dele promete o desafio do D5)
proximo: yt_0029 · EP. 05 · Soma de Riemann e integral dupla (cartão NO PRÓXIMO VÍDEO no fim)
```

---

## 2. Sistema visual (o do EP. 03, sem novidade)

Use o `yt_0028` como modelo de código (mesma biblioteca `papel.py` v2, mesmos helpers de seta, chapa, malha e caneta). Copie o que precisar para a unidade; **não altere** o `yt_0028` nem nada global.

### 2.1 Fundo, grade e molduras

| Item | Valor |
|---|---|
| Fundo da câmera | degradê vertical `#18143A → #0F0C26` (`usar_papel(self)`) |
| Grade | `#2B2558`, traço 1,2, `z_index = −10`, parada; nasce dos eixos de cada painel (`papel(ax, area, passo)`) |
| Passo | 0,25 u; se o quadradinho der < 20 px no 1080p, 0,5 u |
| Moldura de painel | `#CDC3F0`, opacidade 0,38, 2 px, cantos 8 px |
| Placa de texto (R2) | `#161236`, opacidade 0,9 |
| Canto (2 linhas) | linha 1 `CÁLCULO III · EXERCÍCIOS DO MÓDULO` (SG Medium 22 px, `#C8D6F0` a 60 %), em (36, 73); linha 2 = título da cena (SG Bold 36 px, branco), em (36, 118) |
| Logo | `logo_crop.png` em (1650, 24), em todas as cenas menos a abertura e o cartão do próximo vídeo |

Conversão px → Manim: **x_m = (x_px − 960)/135, y_m = (540 − y_px)/135, u_m = (px por unidade)/135**.

### 2.2 Layouts (px no 1080p)

| Layout | Moldura | Origem | Escala | Quadradinho | Alvos |
|---|---|---|---|---|---|
| **A** palco + coluna | x 120–1080, y 180–900 | (600, 540) | 120 px/u | 0,25 (30 px) | 06–09, 13–15, 18–21, 23, 26, 27 |
| A, alvo 22 (campo ③) | idem | **(360, 780)** | **240 px/u** | 0,25 (60 px) | 22 |
| A, alvo 24 (parede) | idem | **(600, 840)** | 120 px/u | 0,25 (30 px) | 24 |
| **B** dois painéis | x 120–840 e 1080–1800, y 180–900 | esq. (480, 540), dir. (1440, 540) | 144 px/u | 0,25 (36 px) | 12, 16, 17 |
| B, alvos 04–05 (D1) | idem | esq. **(408, 540)**, dir. **(1260, 540)** | 144 px/u | 36 px | 04, 05 |
| B, alvo 25 (mapas) | idem | esq. **(300, 756)**, dir. **(1260, 792)** | 144 px/u | 36 px | 25 |
| **C** três cartões | x 120–600, 720–1200, 1320–1800; y 300–780 | centro de cada cartão, y = 540 | 60 px/u | **0,5** (30 px) | 03, 10, 11 |

- Coluna de fórmulas (A): x = 1120, de y ≈ 260 a ≈ 860.
- B: nomes dos painéis em y = 868 (SG Medium 28 px, GEO, centrados em 480 e 1440); fórmula em y ≈ 950–965.
- C: rótulos sob cada cartão de y ≈ 830 a ≈ 920.
- Toda origem é um nó da grade; tudo o que é do desenho usa `ax.c2p`.

### 2.3 Cores

| Papel | Cor |
|---|---|
| Campo, P, Q, R, F⃗, v⃗, f⃗, B⃗, E⃗, G⃗ | verde-menta `#2EE6A0 → #8CFFD2` (pela intensidade); contexto `#1A5F55` |
| x, u, ∂/∂x, linha 1 da tabela | âmbar `#FFC24D` |
| y, v, ∂/∂y, linha 2 da tabela | magenta `#EA63FF` |
| ponto, δ | laranja `#E08A3C` |
| ε | `#8CFFD2` |
| rot | violeta `#9C8CFF` (também a seta curva de giro) |
| div | azul-claro `#7FB2FF` |
| deformação (d₁, d₂) | lima `#C6F26B` |
| quadradinho | chapa `#663A4C` (coral misturado 62 % com o fundo, opaca) + malha 4×4 `#FFB3BC` 2 px + contorno coral `#FF7A8A` 4 px; fantasma tracejado coral |
| geometria auxiliar (eixos, retas, paredes, hipérboles) | GEO `#B8C4DA` |
| carga | `#267BFF` |
| operadores, α, p, números puros | branco `#F5F7FF` |

### 2.4 Setas de campo

- Só a flecha: haste 5 px, ponta 19 px, opaca, sem contorno e sem transparência.
- Comprimento comprimido: L = Lmax·(0,4 + 0,6·t), t = min(1, |F|/mmax), Lmax = 0,84·passo. Rede de passo 0,5 u nos layouts A e B (centros em nós da grade) e 0,75 u nos cartões.
- **Proporcional com teto** onde o tamanho é a matemática (D3c, D4, A1): L = Lmax·min(1, |F|/mref). Seta com menos de 6 px não é desenhada.
- Os valores de `mmax`/`mref` de cada alvo estão no `sb30.html` (função `campo`/`campoP` de cada chave).

### 2.5 Regras (as do EP. 03, todas valem)

- **R1 · clareira por polígono:** nenhuma seta a menos de 0,25 u de fórmula, rótulo, quadradinho (posição atual e fantasma) ou seta curva de giro.
- **R2 · placa mínima:** rótulo em cima de desenho ganha placa `#161236` a 0,9, justa ao texto.
- **R3:** fórmula nova nunca nasce sobre fórmula velha.
- **R4:** rótulo junto do seu objeto.
- **R5 · sobreposição:** QA em cada gatilho, medindo a seta inteira.
- **R7 · seta na chapa:** a seta só é desenhada se cabe inteira a ≥ 18 px da moldura do painel. Nenhum texto, linha auxiliar (retas, diagonais, paredes, hachuras, hipérboles) ou placa cruza a moldura: as linhas auxiliares são **recortadas** na moldura.
- **R10 · transição:** nenhuma tela com menos de um objeto além do canto e do logo por mais de 0,8 s; o layout novo entra enquanto o antigo sai (`FadeIn` + `FadeOut` de 0,4 s no mesmo `AnimationGroup`). O canto entra no fim da abertura.
- Tamanho mínimo: legenda (SG Medium) ≥ 24 px e `MathTex` ≥ 30 px no 1080p.

### 2.5.1 Álgebra (regra permanente)

Toda fórmula entra no modo **caneta**: `Write` glifo a glifo, da esquerda para a direita, traço finíssimo (~0,7) que depois preenche na cor da grandeza. Nada existe na tela antes da sua vez. Um termo que nasce do desenho **voa** do desenho para a fórmula (`TransformFromCopy`). Manipulação algébrica (cancelar, pôr em evidência, trocar rot ↔ div) por `TransformByGlyphMap` do MF-Tools, com `MathTex` de string única nos dois lados; `TransformMatchingTex` quando o casamento for óbvio. Nada de índices de debug no vídeo.

### 2.6 Tag `PAUSE E TENTE`

Chip no canto inferior direito: texto SG Bold 30 px branco, placa `#161236` a 0,9, borda GEO 2 px, cantos 10 px; borda direita em x = 1880, de y = 968 a 1030 (ver alvos 07, 15 e 19). `FadeIn` 0,3 s, fica ≈ 3 s, `FadeOut` 0,3 s, **enquanto a fala diz "pausa o vídeo e tenta"** (a voz não para: WAV contínuo). Nada de cronômetro ou barra.

Ocorrências (10): A (demonstração, no "pausa o vídeo e tenta antes de ver a resolução"), D1, D2, D3, D4, D5 ①, D5 ②, D5 ③, A1, A3 ("pausa e pensa").

### 2.7 O quadradinho de fluido

Desenhe **a imagem exata** do quadrado pelo fluxo (não um quadrilátero pelos 4 cantos): amostre cada lado com 30 pontos, mapeie pelo fluxo e use o polígono resultante como chapa + contorno. A malha 4×4 são 3 + 3 linhas internas mapeadas do mesmo jeito. O fantasma tracejado fica na posição inicial. "Soltar" = animar t de 0 até t_final com `ValueTracker` em ≈ 2 s (`rate_func = linear`), uma vez, e parar no estado final (é o quadro-alvo). Seta curva de giro (violeta, 4 px, ponta 18 px): arco de ~110° em volta do **centro atual** do quadradinho, do lado de cima e à direita; anti-horário para rot > 0, horário para rot < 0.

---

## 3. Campos, fluxos e números (todos conferidos no SymPy: 75/75)

### 3.1 Campos

| Nome | Fórmula | Onde |
|---|---|---|
| f₁ | (x + y, x − y) | H ①, D1c, D5 ① |
| f₂ | (1, x − y) | H ②, D2, D5 ② |
| f₃ | (x² − y², 2xy) | H ③, D5 ③, A4 |
| v_α (redemoinho) | (−y, x)/(x² + y²)^α | D3, A3 (B⃗) |
| w_α (explosão) | (x, y)/(x² + y²)^α | D3d, A3 (fio carregado) |
| sela = ∇φ, φ = (x² − y²)/2 | (x, −y) | D3b (i1), A2 |
| giro | (−y, x) | D3b (i2) |
| F₄ | xy/(x² + y²) · (x, y), F₄(0, 0) = 0⃗ | D4 |
| rio | (0, 1 − x²/9), −3 < x < 3 | A1 |
| carga (corte) | (x, y)/(x² + y²)^{3/2} | A3 |

### 3.2 Fluxos exatos (posição de um ponto p₀ = (x₀, y₀) no tempo t)

| Fluxo | Fórmula | Quadradinho (centro, lado) e t_final |
|---|---|---|
| ① f₁ | p(t) = cosh(√2 t)·p₀ + (sinh(√2 t)/√2)·A·p₀, A = [[1, 1], [1, −1]] | (0, 0), 1,2 · t = 0,5 |
| ② f₂ | x = x₀ + t; y = x₀ + t − 1 + (y₀ − x₀ + 1)·e^{−t} | (−1,8; −0,6), 1,1 · t = 0,7; desenhar também a trajetória tracejada branca do centro com ponta |
| ③ f₃ = z² | z(t) = z₀/(1 − t·z₀), com z = x + iy | (1, 0), (0, 1), (1, 1), lado 0,3 · t = 0,1 |
| v_α | gira cada ponto em torno da origem pelo ângulo θ = t·r^{−2α} | D3: (1,75; 0), 0,7 (palco) e (2,2; 0), 0,6 (cartões); t tal que o centro gire 0,35 rad: t = 0,35·r_c^{2α} |
| giro | rotação rígida de ângulo t | (1,6; 0), 1 · t = 0,6 |
| sela | (x₀eᵗ, y₀e^{−t}) | i1: (0, 0), 1,2 · t = 0,55; A2: (0, 3), 1 · t = 0,9 |
| rio | (x₀, y₀ + (1 − x₀²/9)·t) | (−2,4; −1,6), (0; −1,6), (2,4; −1,6), lado 0,9 · t = 1,2 |
| F₄ (D4, painel ×10) | sem forma fechada: RK4, dt = 0,01 | 2 quadradinhos de lado 0,4 nas diagonais (1, 1)/√2·1,2 e (−1, 1)/√2·1,2 · t = 0,6 |

### 3.3 Números que vão para a tela

- **D1:** cantos (0,0)→(0,0), (1,0)→(1,1), (1,1)→(2,0), (0,1)→(1,−1); lado √2, área 1 → 2, ordem invertida (espelhado), det = −2; círculo r → r√2 (área × 2).
- **D2:** na reta x − y = c a seta é (1, c): (1, 0), (1, 1), (1, 2), e (1, −1), (1, −2) acima da diagonal.
- **D3:** rapidez r^{1−2α}; rot = (2 − 2α)/(x² + y²)^α; div = 0. α = 0: rot 2. α = ½: rot 1/r. α = 1: rot 0. α = 2: rot −2/r⁴ (gira ↻ com a volta ↺). Origem: α = 0 já é contínuo; 0 < α < ½ contínuo definindo v(0) = 0⃗; α = ½ sem limite (tamanho 1, direção muda); α > ½ explode. Giro de 90° no sentido horário: w = (x, y)/(x² + y²)^α, div = (2 − 2α)/(x² + y²)^α, rot = 0.
- **D3b:** rot ∇φ = (φ_zy − φ_yz, φ_xz − φ_zx, φ_yx − φ_xy) = 0⃗ (Schwarz, φ de classe C²); div(rot F⃗) = (R_yx − R_xy) + (P_zy − P_yz) + (Q_xz − Q_zx) = 0; teste: (x sen y, cos y, z − xy) tem div = sen y − sen y + 1 = 1 ≠ 0 ⇒ não é rotacional.
- **D4:** ‖F₄‖ = |xy|/r = r|sen 2θ|/2 ≤ r/2 ⇒ δ = 2ε; tabela na origem toda zero; homogêneo de grau 1 (F(sX) = sF(X)); ‖erro‖/‖H‖ = ½ na diagonal; ∂P/∂x = 2xy³/(x² + y²)²: 0 nos eixos, ½ na diagonal de subida, −½ na outra, em qualquer raio ⇒ não é C¹. Fora da origem: div = sen 2θ, rot = −cos 2θ (não vão para a tela; só para conferir os quadradinhos).
- **D5 ①:** J = [[1, 1], [1, −1]]; rot 0, div 0, d₁ 2, d₂ 2 · estica a 22,5° do eixo horizontal, fator e^{√2 t}, área constante.
- **D5 ②:** J = [[0, 0], [1, −1]]; rot 1, div −1, d₁ 1, d₂ 1 · área × e^{−t} (em t = 0,7: × 0,50) e viaja.
- **D5 ③:** J = [[2x, −2y], [2y, 2x]]; rot 4y, div 4x, d₁ = d₂ = 0. (1, 0): só cresce · (0, 1): só gira · (1, 1): gira e cresce. Conferência com lado 0,2 e t = 0,12: ângulos das quinas 91,6° / 91,2° / 91,3°; giro 0° / 13,9° / 15,7°; área × 1,76 / 1,01 / 1,68.
- **A1:** div 0; rot = −2x/9: +2/3 s⁻¹ na margem esquerda (↺), 0 no meio, −2/3 s⁻¹ na direita (↻); galho a 1/3 rad/s (uma volta a cada ≈ 19 s); d₁ = 0, d₂ = −2x/9 (atrito viscoso máximo nas margens).
- **A2:** rot 0, div 0, d₁ = 2; φ = (x² − y²)/2; ∇²φ = 1 − 1 = 0; linhas de corrente xy = constante.
- **A4:** d₁ = d₂ = 0 ⇔ P_x = Q_y e P_y = −Q_x (Cauchy-Riemann); (x + iy)² = x² − y² + i·2xy. O irmão (x² − y², −2xy): rot 0, div 0, só deforma.
- **A3:** fio com corrente: rot B⃗ = (2 − 2α)/(x² + y²)^α = 0 ⇒ α = 1 ⇒ |B| = 1/r. Fio carregado: div E⃗ = 0 ⇒ α = 1 ⇒ 1/r. Carga no espaço: ∂/∂x[x/‖X‖^p] = 1/‖X‖^p − p·x²/‖X‖^{p+2}; somando: div = (3 − p)/‖X‖^p (no plano, (2 − p)) ⇒ p = 3 ⇒ |E| = 1/r².
- **Gancho do próximo:** chapa [0, 2]² com densidade x² + y² (leve no canto (0, 0), densa no (2, 2)); régua 0–20 kg com `8 kg?` (âmbar) e `16 kg?` (magenta). (Massa real 32/3 ≈ 10,7 kg: **não** aparece.)

Todos os números com vírgula decimal na tela.

---

## 4. Cena a cena

**Alvo NN** = quadro `NN_<chave>.jpg` de `yt_0030_quadros_alvo_v1/` (tolerância ±20 px na posição e ±5 % no tamanho; mesmo texto e mesmas cores). O alvo é o **estado final** de cada trecho. Os tempos são do orçamento a 3 p/s (§6).

### H · Gancho (0:00–0:34) · alvo 03

- Layout C. Os três cartões entram com a rede de setas (`FadeIn` em 0,6 s cada, um depois do outro, no "Três fórmulas"), cada um com o fantasma tracejado do quadradinho; as fórmulas embaixo em caneta. Título `QUAL GIRA? QUAL MUDA DE ÁREA? QUAL ENTORTA?` em caneta. `A FÓRMULA JÁ SABE` no "Dá".
- **Nenhum quadradinho anda no gancho** (eles só andam no D5).
- No "por que o campo magnético de um fio…": a linha do título troca (`FadeOut`/`FadeIn` 0,4 s) por `POR QUE 1/r? POR QUE 1/r²?` (SG Bold 40 px, branco). Sem canto, sem logo do canto.

### A · Bem-vindos (0:34–1:28) · alvos 01 e 02

- Abertura clássica do EP. 03: logo com os dois anéis tracejados + `BEM-VINDOS AO PARALLAX LAB` (alvo 01).
- A logo sobe e encolhe (1 s) para o alvo 02: `CÁLCULO III`, `EXERCÍCIOS DO MÓDULO`, `NESTE VÍDEO:` e as três linhas, **uma por vez**, sincronizadas: `A ESCADA · CINCO DEGRAUS DE PROBLEMAS` ("Vai ser uma escada"), `O DESAFIO · PREVER O QUADRADINHO` ("no topo da escada"), `AS APLICAÇÕES · RIO, PAREDE, MAPAS E FIOS` ("Na segunda parte").
- No "pausa o vídeo e tenta antes de ver a resolução": o chip `PAUSE E TENTE` aparece (demonstração).
- Fim: tudo sai; o canto e o logo do canto entram (R10).

### D1 · Mesma fórmula, dois filmes (1:28–3:32) · alvos 04, 05, 06

1. Canto `MESMA FÓRMULA, DOIS FILMES`. Layout B com os eixos; nomes `ONDE VOCÊ ESTÁ (u, v)` / `ONDE VAI PARAR (x, y)`. Embaixo à esquerda, φ(u, v) = (u + v, u − v) em caneta (u âmbar, v magenta); embaixo à direita, provisório, `RETA · QUADRADO · CÍRCULO` (SG Medium 32 px, GEO). `PAUSE E TENTE`.
2. **Reta:** o eixo u (âmbar, 5 px) acende com `v = 0`; uma cópia voa para a direita e pousa na diagonal y = x (`TransformFromCopy` pelo mapa linear), com o rótulo `y = x`.
3. **Quadrado:** os quatro cantos aparecem com os números ①–④ (placas); cada canto voa para a sua imagem **na ordem da fala** (origem fica; ② → (1, 1); ③ → (2, 0); ④ → (1, −1)); os lados se ligam, a chapa e a malha preenchem (alvo 04). O texto provisório troca por `ÁREA 1 → 2 · ESPELHADO` (coral). Uma seta curva pequena GEO dentro de cada quadrado mostra a ordem dos números: ↺ à esquerda, ↻ à direita (1,5 s, depois sai).
4. **Círculo** (alvo 05): os quadrados saem; círculo de raio r (coral) com o raio desenhado; ele voa para a direita como r√2. Embaixo, em caneta: (u + v)² + (u − v)² = 2(u² + v²); os termos cruzados ±2uv se cancelam por `TransformByGlyphMap` (escreva primeiro a forma expandida u² + 2uv + v² + u² − 2uv + v², cancele, junte).
5. **Como campo** (alvo 06): troca para o layout A (R10). A rede de f₁ entra por colunas, da esquerda para a direita (1 s). No "No eixo horizontal, à direita da origem", as setas desse semieixo ficam em destaque e as outras vão para a cor de contexto por 2 s; o mesmo no "No eixo vertical". Coluna: fórmula, `COMO TRANSFORMAÇÃO: ÁREA × 2`, `COMO CAMPO: A ÁREA TAMBÉM DOBRA?`, `GUARDA O PALPITE`.

### D2 · Desenhar sem mil setas (3:32–4:43) · alvos 07, 08

1. Canto `DESENHAR SEM MIL SETAS`. Palco vazio com a grade; f⃗ = (1, x − y) em caneta. `PAUSE E TENTE` (alvo 07 mostra onde).
2. "procurar onde o campo não muda": x − y = c ⇒ f⃗ = (1, c) em caneta.
3. A diagonal (c = 0) aparece tracejada; **uma** seta (1, 0) nasce num ponto e cópias deslizam ao longo da reta (0,8 s); o rótulo `(1, 0)` com placa. Depois c = 1 e c = 2 do mesmo jeito (alvo 07). Depois c = −1 e c = −2, acima, apontando para baixo.
4. "E o campo inteiro está desenhado": a rede completa entra **na cor de contexto** atrás das retas (alvo 08). Legendas `DESCENDO DE RETA EM RETA, A SETA EMPINA` e, no "é uma derivada", `ESSE EMPINAR É UMA DERIVADA` (âmbar).
5. Retas recortadas na moldura (R7).

### D3 · A família de redemoinhos (4:43–8:17) · alvos 09, 10, 11, 12

1. Canto `A FAMÍLIA DE REDEMOINHOS`. Palco; a fórmula de v⃗ em caneta; a linha `α = 0  ½  1  2` com a caixa no valor atual. `PAUSE E TENTE`.
2. **α correndo** (o único movimento contínuo do campo; `ValueTracker`, só durante a troca): α vai de 0 a ½ a 1 (1,5 s cada) enquanto a fala descreve a rapidez; `‖v⃗‖ = r^{1−2α}` na coluna.
3. **A conta do rotacional**, na coluna, em caneta, com s = x² + y² (as linhas antigas sobem e somem quando faltar espaço, R3):
   - ∂Q/∂x = s^{−α} − α·s^{−α−1}·2x·x
   - = s^{−α−1}(s − 2αx²)
   - ∂P/∂y = −s^{−α−1}(s − 2αy²)
   - rot = s^{−α−1}(2s − 2α(x² + y²)) = (2 − 2α)/s^α (os dois termos com α se juntam por `TransformByGlyphMap`)
   - div = 2αxy·s^{−α−1} − 2αxy·s^{−α−1} = 0
   No fim fica só o resultado, como no alvo 09 (rot e div coloridos).
4. **Lendo a fórmula:** para α = 0, ½, 1 e 2, nessa ordem: α troca (1 s), o quadradinho é solto (2 s) e a seta curva aparece (anti-horária para 0 e ½; nenhuma para 1; **horária** para 2). O estado α = ½ é o alvo 09. No α = 2 ("Olha por quê"), as duas setas do campo na borda de dentro e na de fora do quadradinho ficam em destaque (a de dentro é maior).
5. **Resumo em cartões** (alvo 10), no "O sentido da volta não é o sentido do giro": os três cartões α = 0 / 1 / 2 com os quadradinhos no estado final e a legenda `TODAS AS SETAS DÃO A VOLTA NO SENTIDO ANTI-HORÁRIO`.
6. **Na origem** (alvo 11): três cartões com setas proporcionais com teto (0 < α < ½, α = ½, α = 1). O ponto da origem: cheio (menta) no primeiro, vazado (anel GEO) nos outros dois. Os rótulos entram conforme a fala; `α = 0 NÃO DIVIDE POR NADA: JÁ É CONTÍNUO NA ORIGEM` primeiro, porque a fala começa por ele.
7. **Giro de 90°** (alvo 12): layout B; à esquerda o redemoinho α = 1; o painel direito começa como cópia e **cada seta gira 90° no sentido horário em torno do próprio centro** (1,2 s, todas juntas). As fórmulas embaixo: rot v⃗ e div v⃗ à esquerda; à direita, a cópia troca rot ↔ div por `TransformByGlyphMap`.

### D3b · Duas regras (8:17–10:05) · alvos 13, 14

1. Canto `DUAS REGRAS · UM GRADIENTE NUNCA GIRA`. Coluna: rot ∇φ com as três componentes em caneta, uma por vez; as mistas trocadas acendem em pares; `= 0⃗` no "Tudo cancela"; legenda de Schwarz.
2. "Lembra do campo que esticava o quadradinho no episódio passado?": no palco entra a sela com φ = (x² − y²)/2 e ∇φ = (x, −y) no topo da coluna; o quadradinho é solto e deforma sem girar (alvo 13). `DEFORMA, MAS NÃO GIRA` (lima).
3. Canto `DUAS REGRAS · UM ROTACIONAL NUNCA DIVERGE`. div(rot F⃗) em caneta, as seis mistas cancelando aos pares (`TransformByGlyphMap`), `= 0`. No palco, o giro rígido com o quadradinho que gira sem mudar de área (alvo 14).
4. O teste: `EXISTE UM CAMPO G COM` + rot G⃗ = (x sen y, cos y, z − xy) ?; div parcela por parcela (sen y, −sen y, 1) voando para a soma; `NÃO EXISTE` (coral).
5. "E isso aparece na física": `div B = 0 ⇔ B = rot A (NO ESPAÇO TODO)` em menta. A última fala (classe C²) puxa o D4: o `C²` da legenda de Schwarz acende em coral por 1 s.

### D4 · O campo que não melhora de perto (10:05–13:34) · alvos 15, 16, 17, 18

1. Canto `O CAMPO QUE NÃO MELHORA DE PERTO`. Palco com F₄, setas proporcionais com teto; as diagonais tracejadas e o círculo de raio 2 tracejado (recortados na moldura). A fórmula e a definição na origem em caneta. As três legendas das direções conforme a fala. Lista de itens + `PAUSE E TENTE` (alvo 15).
2. **Item a:** ‖F⃗‖ = |xy|/r = r|sen 2θ|/2 ≤ r/2 em caneta, com a passagem por polares.
3. **ε-δ** (alvo 16): layout B, os nomes do EP. 03 (`ONDE VOCÊ ANDA` à esquerda). Disco δ laranja à esquerda; à direita, o disco ε e a **mancha das pontas** (rosácea ρ = ε|sen 2θ|, preenchida em menta a 35 % sobre o fundo, opaca no fim, contorno `#8CFFD2` 2 px), que encosta no disco ε só nas diagonais. `ValueTracker` ε de 1 a 0,5 e de volta (δ = 2ε acompanha), uma vez, no "para qualquer épsilon". Fórmula da implicação embaixo.
4. **Item b:** embaixo, as três caixinhas `DOMÍNIO ✓ · LIMITE ✓ · IGUAL À SETA ✓` acendendo uma a uma (SG Bold 30 px; ✓ em menta), no lugar da fórmula do ε-δ. `CONTÍNUO`.
5. **Item c:** volta ao palco (alvo 15 como base). Um ponto âmbar anda pelo eixo horizontal e um magenta pelo vertical (1,5 s cada): nenhuma seta aparece. A tabela J = [[0, 0], [0, 0]] e `rot 0 · div 0 · d₁ 0 · d₂ 0` em caneta; `PREVISÃO: PERTO DA ORIGEM, NADA ACONTECE` (GEO).
6. **Item d · zoom** (alvo 17): layout B, `ZOOM × 1` e `ZOOM × 10`; depois o rótulo da direita troca para `ZOOM × 100` e o desenho não muda (é o ponto). F(sX) = sF(X) em caneta e a legenda. No "tem quadradinho crescendo nas diagonais de subida, encolhendo nas outras", os dois quadradinhos do §3.2 (F₄, RK4) são soltos no painel da direita.
7. **Item e** (alvo 18): palco com F₄ em contexto; ∂P/∂x em caneta, com a regra do quociente em duas linhas antes do resultado (os termos de quarta potência se cancelam por `TransformByGlyphMap`). Os pontos nas três circunferências (r = 2,5; 1,25; 0,625) acendem de fora para dentro: GEO pequenos nos eixos (valor 0) e âmbar nas diagonais (±½), com os rótulos `0`, `½`, `−½`. `NÃO É C¹` (coral), a razão do erro e as duas legendas finais.

### D5 · O desafio prometido (13:34–17:20) · alvos 19, 20, 21, 22

Para cada campo: enunciado e `PAUSE E TENTE` → tabela → quatro medidas → previsão → soltar. A tabela se monta com cada derivada **voando** da componente para a sua célula (linha 1 âmbar = derivadas de P; linha 2 = derivadas de Q; coluna 1 ∂/∂x, coluna 2 ∂/∂y, como no EP. 03). As medidas entram com as cores (rot violeta, div azul-claro, d₁/d₂ lima). A previsão vira três selos `GIRA ✗/✓ · ÁREA ✗/✓ · DEFORMA ✗/✓` antes de soltar.

1. **Campo ①** (alvos 19 → 20): f₁ no palco com o quadradinho parado; perguntas `GIRA? MUDA DE ÁREA? DEFORMA?` e `PAUSE E TENTE` (alvo 19). Tabela e medidas; `SÓ DEFORMA`. Solta (t = 0,5). A resposta do palpite: `ÁREA CONSTANTE (div = 0)` e `COMO TRANSFORMAÇÃO: ÁREA × 2` (coral) (alvo 20).
2. **Campo ②** (alvo 21): f⃗ = (1, x − y); tabela e medidas; `GIRA ↺ · ENCOLHE · ENTORTA`. No "dava para ler isso no desenho do segundo degrau", o 1 e o −1 da tabela piscam (uma vez, 0,3 s) enquanto duas setas do campo acendem: andando para a direita a seta empina; andando para cima, abaixa. Solta (t = 0,7), com a trajetória do centro tracejada e a legenda `A VIAGEM É A SETA DO CENTRO, NÃO ESTÁ NA TABELA`.
3. **Campo ③** (alvo 22): origem (360, 780), 240 px/u. Tabela simbólica, rot 4y, div 4x, d₁ = d₂ = 0, `NUNCA ENTORTA`. `PAUSE E TENTE` com os três pontos marcados (fantasmas). Solta os três juntos (t = 0,1), com as setas curvas em (0, 1) e (1, 1) e os rótulos com placa. Legenda das quinas e `A TABELA FALA DO PONTO, NAQUELE INSTANTE`.
4. "Desafio cumprido": a coluna mostra por 2 s a cadeia `FÓRMULA → TABELA → 4 NÚMEROS → QUADRADINHO` (SG Bold 32 px, setas GEO).

### P2 · Transição (17:20–17:32) · sem alvo

Tela de passagem, sem palco: `PARTE 2` (SG Medium 28 px, GEO) e `AS APLICAÇÕES` (SG Bold 54 px), centrados em y ≈ 500–580. Entra enquanto o D5 sai (R10) e sai enquanto o A1 entra.

### A1 · O rio (17:32–19:14) · alvo 23

Canto `APLICAÇÃO · O RIO`. Margens em x = ±3 (GEO 5 px, hachura curta para fora, recortadas). Primeiro o perfil: só a linha de setas de y = −2,5 (proporcionais), depois a rede inteira. Enunciado curto na coluna (`CANAL DE 6 m · 1 m/s NO MEIO · ZERO NAS MARGENS`) + `PAUSE E TENTE`; depois troca pelas contas: v⃗, div, rot, d₁ e d₂, cada uma no seu trecho de fala. Os três quadradinhos são soltos juntos (t = 1,2); setas curvas ↺ à esquerda, ↻ à direita. Legendas como no alvo.

### A2 · Água batendo na parede (19:14–20:55) · alvo 24

Canto `APLICAÇÃO · ÁGUA BATENDO NA PAREDE`. Origem (600, 840): parede em y = 0 (GEO 6 px, hachura embaixo), rede de (x, −y) só em y ≥ 0,5, hipérboles xy = c tracejadas (c = 0,5; 1; 2; 3,5), tudo recortado na moldura. A "gota de tinta" é o quadradinho em (0, 3), solto até t = 0,9. A conferência "andando com a água, o produto muda pela…": u·y + x·v = xy − xy = 0, em caneta. Depois φ, ∇²φ e `EQUAÇÃO DE LAPLACE`.

### A4 · Mapas que não entortam (20:55–22:01) · alvo 25

Canto `APLICAÇÃO · MAPAS QUE NÃO ENTORTAM`. Layout B. Primeiro as duas equações de Cauchy-Riemann em caneta (embaixo). Depois a malha de quadradinhos [0,5; 1,5] × [0; 1] à esquerda e a sua imagem por z² à direita: a malha voa e se curva (`ValueTracker` s de 0 a 1 em z ↦ (1 − s)z + s·z², 2 s). As quinas ficam em ângulo reto. Legenda `CAUCHY-RIEMANN · (x + iy)² = x² − y² + i·2xy`. No "Mercator", só o texto `MAPA DE MERCATOR: PRESERVA OS ÂNGULOS` (GEO), sem imagem de mapa. No "irmão", `(x² − y², −2xy): rot 0 · div 0 · SÓ DEFORMA`.

### A3 · Por que um sobre a distância (22:01–24:56) · alvos 26, 27

1. Canto `APLICAÇÃO · POR QUE UM SOBRE A DISTÂNCIA`. O fio ⊙ no centro (anel branco + ponto); rótulo `FIO COM CORRENTE` com placa. `PAUSE E TENTE` no "Pausa e pensa".
2. B⃗ = (−y, x)/(x² + y²)^α com α branco. `ValueTracker` α de 0,3 a 1 (2 s) com o campo se ajustando e, ao lado, o valor ao vivo de 2 − 2α (`DecimalNumber`, 2 casas, vírgula) chegando a 0,00. `⇒ α = 1`, ‖B⃗‖ = r/r² = 1/r e o gráfico simples |B| × distância (alvo 26). Frase final da fala: a intensidade depende da corrente; nada na tela.
3. Fio carregado: o campo vira a explosão w₁ (cada seta gira 90° no sentido horário, como no D3d) e `div E = 0 ⇒ α = 1` em caneta, no lugar do bloco do B.
4. Carga no espaço (alvo 27): o centro vira a carga azul `+`, o campo vira o corte radial; `CORTE PELO PLANO` com placa. A conta de uma parcela em caneta, depois a soma; `NO PLANO:` (2 − p) e `NO ESPAÇO:` (3 − p); `p = 3 ⇒ 1/r²`. Legendas da dimensão e da hipótese.

### S · Síntese, gancho e CTA (24:56–26:12) · alvos 28, 29

1. Canto `RESUMO`. A escada sobe degrau a degrau, cada um no seu trecho de fala (alvo 28); as quatro aplicações entram à direita no "E nas aplicações".
2. Cartão `NO PRÓXIMO VÍDEO` (alvo 29) no "No próximo vídeo": sem canto e sem logo; a chapa colorida [0, 2]² entra, depois a régua e os dois palpites (`8 kg?` no "Oito quilos?", `16 kg?` no "Dezesseis?"). Sem número de episódio nem Atlas.
3. CTA padrão da série, igual ao do EP. 03.

---

## 5. Transições (R10)

Em toda troca de layout, o layout novo entra enquanto o antigo sai (0,4 s no mesmo `AnimationGroup`). Trocas deste vídeo: H → A, A → D1 (entra o canto), D1 B → A, D2 → D3, palco → cartões (D3), cartões → B (D3d), D3 → D3b, D3b → D4, D4 palco ↔ B (duas vezes), D4 → D5, D5 ② → ③ (muda a origem do palco: a grade nova entra com o campo), D5 → P2 → A1, A1 → A2 (origem muda), A2 → A4, A4 → A3, A3 → S, S → cartão, cartão → CTA. `transicoes_v1.txt` lista todas, com zero ocorrências esperadas.

---

## 6. Tempo do preview silencioso

Não há voz nesta fase. O preview usa o **orçamento a 3 palavras por segundo** de cada parágrafo da narração (Anexo A), para a duração bater com a fala futura:

| Bloco | Palavras | Início | Duração |
|---|---|---|---|
| H | 103 | 0:00 | 34 s |
| A | 161 | 0:34 | 54 s |
| D1 | 372 | 1:28 | 124 s |
| D2 | 213 | 3:32 | 71 s |
| D3 | 642 | 4:43 | 214 s |
| D3b | 324 | 8:17 | 108 s |
| D4 | 628 | 10:05 | 209 s |
| D5 | 678 | 13:34 | 226 s |
| P2 | 36 | 17:20 | 12 s |
| A1 | 305 | 17:32 | 102 s |
| A2 | 302 | 19:14 | 101 s |
| A4 | 199 | 20:55 | 66 s |
| A3 | 526 | 22:01 | 175 s |
| S | 225 | 24:56 | 75 s |
| **Total** | **4.715** | | **≈ 26:12** |

- Monte um `tempos.py` com os gatilhos de cada animação como **posição da palavra na narração** (início do parágrafo + palavra-gatilho) ÷ 3. Na fase da voz, esse arquivo é trocado pelos tempos medidos no WAV contínuo (a cena segue a voz) sem mexer na `cena.py`.
- Os textos de `[PAUSA NA TELA]` não existem: a voz nunca para; a tag `PAUSE E TENTE` só aparece por cima da fala.
- Duração aceita do preview: 26:12 ± 10 s. Holds > 3 s com motivo no `holds_v1.txt`; nenhum > 6 s sem justificativa.

---

## 7. O que NÃO fazer

- Nenhum 3D (nem Three.js), partícula, lupa, brilho, sombra, pulso, contorno ou transparência em seta, laço contínuo, barra ou cronômetro.
- Grade só por `papel(...)`, parada, fora dos painéis a tela fica lisa; nenhuma linha grossa.
- Nenhum livro, número de exercício ou Atlas na tela. Nenhum vídeo não publicado citado como existente (o cartão do próximo é só pelo tema).
- Não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md`, `pyproject.toml`, `uv.lock` nem nas unidades yt_0026–yt_0029.
- Não gerar voz, SRT, master, 1080p de vídeo nem entrega. Não fazer commit nem push.
- Não cortar conteúdo para encurtar. Se a duração sair do intervalo, avise; a ordem de corte (primeiro A4, depois o α = 2 do D3) é decisão da Produção.

---

## 8. QA do preview (obrigatório)

1. **Render × alvo (29)** a 960×540, tolerância de 10 px nessa escala → `comparacao_v1.jpg` + `.txt` (alvo à esquerda, render à direita, tempo do quadro usado).
2. **Alinhamento** (`alinhamento_v1.txt`), em stills 1080p dos 29 alvos: moldura em linha da grade nos 4 lados (resíduo ≤ 1 px); origem em nó; centro de cada seta de rede em nó.
3. **R5 · sobreposição** em cada gatilho, medindo a seta inteira → `sobreposicoes_v1.txt`.
4. **R7 · seta na chapa**, quadro a quadro → `setas_na_chapa_v1.txt` (zero esperado), incluindo linhas auxiliares recortadas e textos que não cruzam molduras.
5. **R10 · transições** → `transicoes_v1.txt` (zero esperado).
6. **Flash por quadro = 0:** nenhuma fórmula aparece inteira antes da caneta.
7. **Holds** → `holds_v1.txt`.
8. **Números** (`numeros_v1.txt`): todos os valores do §3.3 que aparecem na tela, com o tempo e o quadro; vírgula decimal; quadradinhos do D5 ③ com os ângulos das quinas medidos no polígono final (< 2° do reto).
9. **`PAUSE E TENTE`:** as 10 ocorrências listadas com início e fim.

---

## 9. Parada

Entregue o preview v1 silencioso, a prancha render × alvo, os relatórios de QA e o relatório de entrega (arquivos alterados, verificações, caminho do preview, limitações). Pare: não inicie voz, SRT, 1080p, master nem entrega.

---

## Anexo A · Narração canônica (v3)

Só para tempo e gatilhos nesta fase. **Não gerar voz.** Texto idêntico ao da proposta v3 aprovada.

Regras seguidas: tom de professor de cursinho, conectivos, uma tag por trecho, sem [slowly]; nunca a letra solta (as coordenadas são "a horizontal" e "a vertical"; os parâmetros são "o expoente alfa" e "o expoente"); nada de livros nem do Atlas na fala; o próximo vídeo só pelo tema. Os `[PAUSA NA TELA]` não são silêncio: a voz continua (WAV contínuo); a tag `PAUSE E TENTE` aparece enquanto a fala diz "pausa o vídeo e tenta".

### H · Gancho

[curious] Três fórmulas, três quadradinhos de fluido. Um vai girar. Outro vai mudar de área. E um vai entortar. [thoughtful] A pergunta é: dá para saber qual é qual só olhando a fórmula, antes de soltar o fluido? Dá. E hoje é você que vai fazer isso. [excited] E depois a gente vai usar exatamente as mesmas contas para responder uma pergunta que parece de outro mundo: por que o campo magnético de um fio enfraquece com um sobre a distância, e o campo de uma carga, com um sobre a distância ao quadrado? Não é decoreba. É o rotacional e o divergente escolhendo a lei.

### A · Bem-vindos

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Esse é o quarto episódio da nossa série de Cálculo três, e hoje é dia de colocar a mão na massa: o integrador do módulo, só com exercícios. [thoughtful] Vai ser uma escada. Cada degrau usa uma ferramenta e deixa uma peça para o degrau seguinte. Primeiro, ler uma fórmula de dois jeitos: como transformação e como campo. Depois, uma família inteira de redemoinhos, com o rotacional e o divergente, e duas regras que valem para qualquer campo. Aí vem um campo que não melhora de perto, para testar limite, continuidade e derivadas parciais. E, no topo da escada, o desafio do episódio passado: montar a tabela e prever o quadradinho. [curious] Na segunda parte, as aplicações: um rio, um jato batendo numa parede, mapas que não entortam e as leis do um sobre a distância. [happy] Então pega papel e caneta. Toda vez que aparecer um enunciado, pausa o vídeo e tenta antes de ver a resolução.

### D1 · Mesma fórmula, dois filmes

[thoughtful] Primeiro degrau. Uma função que recebe um par de números e devolve outro par: na primeira coordenada, a soma dos dois; na segunda, a diferença. Primeiro, como transformação. No plano da esquerda fica o ponto de partida; no da direita, onde ele vai parar. Três itens: a imagem de uma reta, de um quadrado e de um círculo. Pausa o vídeo e tenta.

[curious] Começa por uma reta: o eixo horizontal da esquerda, onde o segundo número é zero. Aí a soma e a diferença ficam iguais ao primeiro número, e as duas coordenadas da direita saem iguais. O eixo vai parar na diagonal.

[thoughtful] Agora o quadrado de lado um. Como essa transformação é linear, ela leva segmento em segmento, então basta transformar os quatro cantos. A origem fica parada. O canto um, zero vai para um, um. O canto um, um vai para dois, zero. E o canto zero, um vai para um, menos um. Liga os pontos: é um quadrado de novo, girado quarenta e cinco graus, com lado raiz de dois. A área era um; agora é dois. E olha a ordem dos cantos: na esquerda, eles davam a volta no sentido anti-horário; na direita, dão no horário. O quadrado foi espelhado.

[curious] E um círculo em volta da origem? Soma ao quadrado mais diferença ao quadrado: os termos cruzados se cancelam, e sobra duas vezes a soma dos quadrados. Então a distância até a origem fica multiplicada por raiz de dois, e o círculo vira um círculo com o raio multiplicado por raiz de dois. E, como a área vai com o quadrado do raio, ela também dobra.

[thoughtful] Agora a mesma fórmula, lida como campo. Em cada ponto do plano, você pendura a seta com a soma e a diferença das coordenadas daquele ponto. No eixo horizontal, à direita da origem, as setas saem na diagonal, para cima. No eixo vertical, em cima da origem, elas apontam para a direita e para baixo; embaixo, para a esquerda e para cima.

[curious] E aqui fica uma pergunta que eu vou guardar para o topo da escada. Como transformação, a área dobrou. Como campo, se a gente soltar um pedacinho de fluido nessas setas, a área dele também dobra? Guarda o seu palpite.

### D2 · Desenhar sem desenhar mil setas

[thoughtful] Segundo degrau: desenhar um campo sem calcular mil setas. O campo é este: a componente horizontal vale sempre um, e a vertical vale a coordenada horizontal menos a vertical. Pausa o vídeo e tenta desenhar.

[curious] O truque é procurar onde o campo não muda. A componente horizontal nunca muda. A vertical só depende da diferença entre as coordenadas. Então, em cima de uma reta onde essa diferença é constante, a seta é a mesma em todo ponto. E essas retas são as paralelas à diagonal.

[thoughtful] Na própria diagonal, a diferença é zero: a seta é um, zero, deitada, apontando para a direita. Uma reta abaixo, onde a diferença vale um: a seta é um, um, a quarenta e cinco graus. Mais uma abaixo, diferença dois: um, dois, mais empinada. E, acima da diagonal, a diferença fica negativa, e as setas apontam para baixo.

[curious] Agora é só copiar: uma seta por reta, repetida ao longo da reta inteira. E o campo inteiro está desenhado: setas que vão empinando à medida que você desce de reta em reta, e que se inclinam para baixo quando você sobe.

[thoughtful] Grava esse desenho, porque ele vai voltar. Esse empinar de reta em reta é uma derivada, e no topo da escada a gente vai ler isso numa tabela.

### D3 · A família de redemoinhos

[thoughtful] Terceiro degrau: uma família inteira de redemoinhos de uma vez. Começa pelo redemoinho do primeiro episódio, menos a coordenada vertical na primeira componente e a horizontal na segunda, e divide tudo pela distância ao quadrado elevada a um expoente alfa. Cada valor do expoente alfa é um redemoinho diferente. Pausa o vídeo e tenta: o que muda com alfa zero, meio e um?

[curious] As setas são sempre tangentes às circunferências em volta da origem, então tudo dá a volta no sentido anti-horário. O que muda é o tamanho: a rapidez é a distância elevada a um menos dois alfa. Com alfa zero, a rapidez cresce com a distância: é o disco girando rígido. Com alfa meio, a rapidez vale um em todo lugar. Com alfa um, ela cai com um sobre a distância: é o vórtice.

[thoughtful] Agora a conta do rotacional: a derivada da componente vertical na direção horizontal, menos a derivada da componente horizontal na direção vertical. A componente vertical é a coordenada horizontal vezes a distância ao quadrado elevada a menos alfa. Regra do produto: a primeira parte dá a própria potência; a segunda, pela regra da cadeia, dá menos alfa vezes a potência com um a menos no expoente, vezes duas vezes a coordenada horizontal, vezes a coordenada horizontal de novo. Põe a potência com um a menos em evidência: sobra a distância ao quadrado menos dois alfa vezes o quadrado da coordenada horizontal. A outra derivada é igualzinha, com a vertical no lugar da horizontal e o sinal trocado. Na subtração, a distância ao quadrado aparece duas vezes, e os dois termos com alfa se juntam em dois alfa vezes a soma dos quadrados, que é a distância ao quadrado de novo. Sobra uma fórmula curtinha: dois menos dois alfa, dividido pela distância ao quadrado elevada a alfa. E o divergente? Faz a mesma conta com a soma, e os termos se cancelam: zero, para qualquer alfa. Nenhum desses redemoinhos muda a área do fluido.

[curious] Agora lê a fórmula. Alfa zero: rotacional dois, o giro do disco rígido. Alfa meio: todas as setas do mesmo tamanho, e mesmo assim o rotacional é um sobre a distância. O quadradinho gira, e gira mais quanto mais perto do centro. Alfa um: dois menos dois dá zero. As partículas dão a volta, e o quadradinho não gira: o vórtice do segundo episódio.

[excited] E alfa dois? O rotacional fica negativo. As setas continuam dando a volta no sentido anti-horário, e o quadradinho gira no sentido horário! Olha por quê: a seta do lado de dentro é bem mais forte que a do lado de fora, então a borda de dentro do quadradinho corre na frente, e ele vira para trás. O sentido da volta não é o sentido do giro.

[thoughtful] E na origem? Todos esses campos dividem por zero lá, então a pergunta é se existe limite. Com alfa zero, não tem divisão nenhuma: é o disco rígido, já definido e contínuo na origem. Com alfa entre zero e meio, a fórmula não vale no centro, mas a rapidez vai a zero quando você chega nele. Então o limite é o vetor nulo e, definindo a seta da origem como zero, o campo fica contínuo. Com alfa meio, a rapidez fica um, mas a direção depende do caminho por onde você chega: não tem limite. E, com alfa maior que meio, a seta explode.

[curious] Último item: gira cada seta noventa graus, no sentido horário. O redemoinho vira uma explosão, com as setas apontando para fora. Faz as contas de novo, e os papéis se trocam: o rotacional vira zero, e o divergente vira os mesmos dois menos dois alfa sobre a distância ao quadrado elevada a alfa. Com alfa um, é a falsa fonte do segundo episódio. [thoughtful, emphatic] Guarda essa fórmula: dois menos dois alfa. Ela ainda vai escolher uma lei da física.

### D3b · Duas regras para qualquer campo

[thoughtful] Antes de subir, duas regras que valem para qualquer campo. Primeira: pega um campo que é o gradiente de uma função, ou seja, as componentes são as derivadas parciais dessa função. Calcula o rotacional. A primeira componente é a derivada em relação à vertical da derivada em relação à profundidade, menos a derivada em relação à profundidade da derivada em relação à vertical. E as outras duas componentes têm a mesma cara: uma derivada mista, menos a mesma derivada mista com a ordem trocada. E, se a função é de classe cê dois, as derivadas mistas são iguais: é o teorema de Schwarz. Tudo cancela. Um gradiente nunca gira.

[curious] Lembra do campo que esticava o quadradinho no episódio passado? Ele é o gradiente da metade da diferença entre os quadrados das coordenadas. Por isso o quadradinho deformava, mas não girava.

[thoughtful] Segunda regra, agora no espaço, com três componentes. Calcula o rotacional de um campo e, depois, o divergente desse rotacional. Aparecem seis derivadas mistas, e elas se cancelam aos pares, de novo por Schwarz. Um rotacional nunca diverge.

[curious] E isso vira teste. Alguém te dá este campo e pergunta: existe outro campo cujo rotacional é ele? Não precisa procurar. Calcula o divergente: a primeira parcela dá seno, a segunda dá menos seno, e a terceira dá um. Total: um. Se ele fosse um rotacional, o divergente teria que ser zero. Então não existe.

[thoughtful] E isso aparece na física. O campo magnético tem divergente zero em todo lugar: é a lei que diz que não existe polo magnético isolado. E, no espaço todo, isso permite escrever o campo magnético como o rotacional de outro campo, o potencial vetor. As duas ideias andam juntas, e a regra de hoje prova uma das metades: todo rotacional tem divergente zero.

[thoughtful, emphatic] E repara na hipótese: classe cê dois. Sem derivadas contínuas, a ferramenta pode falhar. No próximo degrau, a gente vê de perto o que acontece quando falta regularidade.

### D4 · O campo que não melhora de perto

[thoughtful] Quarto degrau, o mais difícil da escada. Este campo pega o vetor posição e multiplica pelo produto das coordenadas, dividido pela distância ao quadrado. Na origem, onde a fórmula divide por zero, a gente define a seta como zero.

[curious] Olha o desenho. Nas diagonais de subida, as setas apontam para fora. Nas outras diagonais, apontam para dentro. E, em cima dos eixos, não tem seta, porque o produto das coordenadas é zero. Pausa o vídeo e tenta os cinco itens.

[thoughtful] Item a: existe limite na origem? Calcula o tamanho da seta. O vetor posição tem tamanho igual à distância, então a seta tem tamanho igual ao módulo do produto das coordenadas, dividido pela distância. Em polares, o produto das coordenadas é a distância ao quadrado vezes metade do seno do dobro do ângulo. Então o tamanho da seta é a distância vezes metade do módulo desse seno, e isso nunca passa da metade da distância.

[curious] Agora o desafio do épsilon. Alguém escolhe um épsilon. Você responde com delta igual a dois épsilon. Se o ponto está a menos de delta da origem, a seta tem tamanho de no máximo a metade disso, ou seja, menos que épsilon. Venceu, para qualquer épsilon. O limite é o vetor nulo.

[thoughtful] Item b: é contínuo? O ponto está no domínio, porque a gente definiu a seta lá. O limite existe. E é igual à seta do ponto, zero. Os três pedaços passam: contínuo. Item c: as derivadas parciais na origem. Andando pelo eixo horizontal, a seta é zero o caminho todo: derivada zero. Pelo vertical, a mesma coisa. A tabela é toda zero: rotacional zero, divergente zero, deformação zero. A previsão seria: perto da origem, nada acontece.

[curious] Item d: confere com um zoom. No episódio passado, o zoom de dez vezes no campo da aula deixava as setas arrumadinhas, iguais ao modelo linear. Aqui, olha: o zoom de dez vezes dá exatamente o mesmo desenho. E o de cem vezes, também. Esse campo é homogêneo: multiplicar a posição por um número multiplica a seta pelo mesmo número. Então ele nunca fica parecido com a tabela, por mais perto que você chegue. Na diagonal, a seta tem sempre metade do tamanho do passo: o erro da tabela, dividido pelo passo, fica em meio e não vai a zero. Para o campo ser diferenciável na origem, essa razão teria que ir a zero. Não vai. Em qualquer vizinhança, por menor que seja, tem quadradinho crescendo nas diagonais de subida, encolhendo nas outras, e girando para os dois lados.

[thoughtful, emphatic] A tabela errou. E por quê? Item e: calcula a derivada da componente horizontal na direção horizontal, fora da origem. A componente horizontal é o quadrado da coordenada horizontal vezes a vertical, sobre a distância ao quadrado. Regra do quociente: no numerador, a derivada de cima vezes a de baixo, menos a de cima vezes a derivada de baixo. Os termos com a quarta potência se cancelam, e sobra duas vezes a coordenada horizontal vezes o cubo da vertical, sobre a distância à quarta. Agora olha essa derivada perto da origem. Nos eixos, ela vale zero. Na diagonal, vale meio, e vale meio na diagonal inteira, por mais perto que você chegue. Ela não é contínua na origem. O campo não é de classe cê um, e a tabela perde a garantia. Repara: o cê um é uma garantia, não uma exigência. Tem campo que não é cê um e mesmo assim é bem aproximado pela tabela. Só que aqui a gente provou, direto, que a aproximação falha.

[curious] E olha a escada: no episódio passado, o campo encrenqueiro nem era contínuo. Este é contínuo, tem as duas derivadas parciais e, mesmo assim, engana. Ter derivadas parciais não basta para a tabela descrever o campo de perto.

### D5 · O desafio prometido

[excited] Topo da escada! Chegou a hora do desafio do episódio passado. Três campos. Para cada um: monta a tabela, lê os quatro números e prevê se o quadradinho gira, muda de área ou deforma. Só depois a gente solta o fluido.

[thoughtful] Primeiro campo: a fórmula do primeiro degrau, a soma e a diferença das coordenadas. Pausa o vídeo e tenta.

[thoughtful] A tabela. A componente horizontal é a soma, então as derivadas dela são um e um. A vertical é a diferença: um e menos um. Em cima, um e um; embaixo, um e menos um. Agora as medidas. Rotacional: o de baixo à esquerda menos o de cima à direita, um menos um, zero. Divergente: a diagonal, um mais menos um, zero. Primeira deformação: um menos menos um, dois. Segunda: um mais um, dois. Previsão: não gira, não muda de área, só deforma.

[curious] Solta. O quadradinho estica numa direção, um pouco acima do eixo horizontal, achata na outra, e a área fica igual o tempo todo.

[excited] E aí está a resposta do palpite. Como transformação, essa fórmula dobrava a área. Como campo, ela não muda a área nenhuma. Por quê? Porque são dois filmes diferentes. A transformação leva cada ponto, de uma vez, para a imagem. O campo é uma velocidade: o fluido anda devagarinho, seguindo as setas, e quem mede a taxa de área desse fluido é o divergente, que aqui é zero. O fator de área de uma transformação é outro número, que vai aparecer quando a gente estudar mudança de variáveis.

[thoughtful] Segundo campo: o do segundo degrau, um na horizontal e a diferença na vertical. Pausa e tenta.

[thoughtful] A componente horizontal é constante: derivadas zero e zero. A vertical: um na direção horizontal e menos um na vertical. Tabela: zero e zero em cima; um e menos um embaixo. Rotacional: um menos zero, um. Divergente: zero mais menos um, menos um. Deformações: zero menos menos um, um; e um mais zero, um. Previsão: tudo junto. Gira no sentido anti-horário, encolhe e entorta.

[curious] E dava para ler isso no desenho do segundo degrau: andando para a direita, a seta empina, e esse é o um embaixo à esquerda. Andando para cima, a seta abaixa, e esse é o menos um. Solta: o quadradinho viaja para a direita, porque a seta do centro não é zero, e, no caminho, gira, encolhe e entorta. A viagem não está na tabela, porque a gente tirou a seta do centro. A tabela conta o que acontece com a forma.

[thoughtful] Terceiro campo: a primeira componente é a diferença dos quadrados das coordenadas; a segunda, duas vezes o produto delas. Agora a tabela não é constante. Derivando a diferença dos quadrados, sai duas vezes a coordenada horizontal na direção horizontal, e menos duas vezes a vertical na direção vertical: essa é a primeira linha. Derivando duas vezes o produto, sai duas vezes a vertical na direção horizontal, e duas vezes a horizontal na direção vertical: a segunda linha. Então o ponto importa. Pausa o vídeo e prevê nos três pontos: um, zero; zero, um; e um, um.

[curious] Rotacional: quatro vezes a coordenada vertical. Divergente: quatro vezes a horizontal. E as duas deformações dão zero, em qualquer ponto. No ponto um, zero: rotacional zero, divergente quatro. Só cresce. No zero, um: rotacional quatro, divergente zero. Só gira. No um, um: gira e cresce.

[excited] Solta os três! Um cresce sem girar, um gira sem crescer, e o terceiro faz as duas coisas. E nenhum entorta: as quinas continuam praticamente em ângulo reto. Praticamente, porque a tabela fala do que acontece no ponto, naquele instante. Um quadradinho de tamanho finito sente a tabela mudando de um canto para o outro, e pode entortar um tiquinho. Bem pequeno, esse campo nunca deforma um quadradinho. Guarda isso, porque ele tem nome, e vai aparecer na segunda parte.

[thoughtful, emphatic] Desafio cumprido. A fórmula do campo vira uma tabela, a tabela vira quatro números, e os quatro números contam o que acontece com um quadradinho bem pequeno, logo que você solta. E o cê um garante que essa leitura vale.

### P2 · Transição

[excited] Pronto: você já prevê um quadradinho só olhando a fórmula. Agora vem a melhor parte. Essas contas não ficam no papel. Elas descrevem água de verdade e escolhem leis da física. [thoughtful] Vamos começar por um rio.

### A1 · O rio

[thoughtful] Um canal de margens retas, com seis metros de largura. A água corre a um metro por segundo no meio, e a velocidade vai caindo até zero nas margens, numa parábola. Três perguntas: a água é incompressível? O escoamento gira? E onde o atrito é maior? Pausa o vídeo e tenta.

[curious] Primeira: a velocidade só tem a componente na direção do canal, e ela não muda ao longo do canal. Divergente zero: incompressível.

[thoughtful] Segunda: as linhas de corrente são retas, então dá vontade de dizer que não gira. Mas faz a conta. O rotacional é a derivada da componente na direção do canal, tomada na direção de uma margem para a outra: dá menos dois nonos da coordenada horizontal. Na margem esquerda, ele vale dois terços por segundo: um galho ali gira no sentido anti-horário. E lembra que o rotacional é o dobro da velocidade angular da rodinha: o galho gira a um terço de radiano por segundo, uma volta a cada dezenove segundos, mais ou menos. Na margem direita, menos dois terços: gira no horário. E, bem no meio, zero: o galho desce o rio sem girar.

[curious] Olha os três quadradinhos. O do meio só viaja. Os das margens viajam, entortam e giram, cada um para um lado. Por quê? Perto da margem, a água do lado de dentro corre mais rápido que a do lado de fora, então a borda de dentro do quadradinho vai na frente.

[thoughtful] Terceira: o atrito. No episódio passado a gente viu que, num fluido como a água, o atrito viscoso vem da deformação: aqui, da diferença de velocidade entre camadas vizinhas. Aqui, a primeira deformação é zero, e a segunda é aquele mesmo menos dois nonos da coordenada horizontal. Máxima nas margens e zero no meio. É perto das margens que a água mais esfrega em si mesma.

### A2 · Água batendo na parede

[thoughtful] Segundo problema: um jato de água descendo e batendo numa parede, como a água da torneira batendo na pia. Num modelo ideal, perto do ponto do choque, a velocidade tem a coordenada horizontal na primeira componente e menos a vertical na segunda. É o campo do gancho do episódio passado, agora só na metade de cima, com a parede embaixo.

[curious] Primeiro: na parede, a componente vertical é zero. A água não atravessa a parede: ela desliza. Numa parede de verdade, uma camada fina de água gruda nela por causa da viscosidade, e esse modelo ideal ignora essa camada. Segundo: rotacional zero, divergente zero, primeira deformação dois. A água não gira e não comprime: só deforma. Uma gota de tinta que desce pelo eixo se achata e se espalha pela parede, sempre com a mesma área. E as linhas de corrente são hipérboles, as curvas onde o produto das coordenadas é constante. Confere: andando com a água, o produto muda pela velocidade horizontal vezes a coordenada vertical, mais a horizontal vezes a velocidade vertical. Dá o produto menos o produto: zero. O produto não muda: a água anda em cima da hipérbole.

[thoughtful] Terceiro: esse campo é o gradiente da metade da diferença dos quadrados das coordenadas. Essa função tem nome: potencial de velocidade. E o laplaciano dela, aquela curiosidade do segundo episódio, dá um menos um: zero.

[thoughtful, emphatic] E isso não é coincidência. Se a velocidade é um gradiente, ela é irrotacional, pela primeira das duas regras. Se, além disso, o divergente é zero, então o divergente do gradiente é zero. E o divergente do gradiente é o laplaciano. Escoamento irrotacional e incompressível quer dizer laplaciano do potencial igual a zero: a equação de Laplace. A mesma equação aparece no potencial elétrico numa região sem cargas e na temperatura de uma chapa em equilíbrio.

### A4 · Mapas que não entortam

[curious] Lembra do terceiro campo do desafio, aquele que nunca entorta? Vamos ver por quê. Deformação zero em todo lugar quer dizer duas equações: a derivada horizontal da primeira componente igual à derivada vertical da segunda, e a derivada vertical da primeira igual a menos a derivada horizontal da segunda. Essas duas equações têm nome: equações de Cauchy-Riemann.

[thoughtful] Elas aparecem quando você junta as duas componentes num número complexo. O nosso campo é exatamente o quadrado do número complexo que tem a coordenada horizontal como parte real e a vertical como parte imaginária. E toda função complexa derivável satisfaz essas equações: o cubo, a exponencial, todas.

[curious] Agora lê como transformação. Onde a derivada complexa não é zero, uma tabela assim só gira e muda a escala: quadradinhos pequenos viram quadradinhos, maiores ou menores, mas sempre com ângulos retos. Isso se chama mapa conforme. E você conhece um: o mapa-múndi de Mercator, aquele de parede de sala de aula, preserva os ângulos. Por isso a Groenlândia aparece quase do tamanho da África, mas com o formato certo em cada pedacinho.

[thoughtful] E o irmão desse campo, com o sinal da segunda componente trocado, faz o contrário: rotacional zero, divergente zero, só deformação.

### A3 · Por que um sobre a distância

[excited] E agora, o último problema, que fecha a escada inteira. Um fio comprido, com corrente, atravessando a tela. As linhas do campo magnético são circunferências em volta dele. A pergunta é: com que lei o campo enfraquece quando você se afasta? Pausa e pensa.

[thoughtful] A física diz duas coisas. Primeira, a simetria: o campo dá a volta no fio, e o tamanho só depende da distância. Supondo uma lei de potência, ele tem a forma do terceiro degrau: menos a coordenada vertical e a horizontal, divididas pela distância ao quadrado elevada a um expoente alfa que a gente não sabe. Segunda: fora do fio não tem corrente e, para campos que não mudam no tempo, a lei de Ampère diz que, onde não tem corrente, o rotacional do campo magnético é zero.

[curious] Agora usa a fórmula que a gente guardou. O rotacional é dois menos dois alfa, sobre a distância ao quadrado elevada a alfa. Para ser zero, só tem um jeito: alfa igual a um. Então o tamanho do campo é a distância dividida pela distância ao quadrado: um sobre a distância. O campo do fio cai com um sobre a distância. A intensidade ainda depende da corrente; o que a conta escolhe é como ela cai.

[thoughtful] Faz o mesmo com um fio carregado. O campo elétrico aponta para fora, então ele é a explosão do terceiro degrau. Fora do fio não tem carga, e a lei de Gauss diz que o divergente é zero. Divergente: dois menos dois alfa, de novo. Alfa um, e o campo também cai com um sobre a distância.

[excited] E uma carga pontual, no espaço? Escreve o campo como o vetor posição dividido pela distância elevada a um expoente. No plano, o divergente seria dois menos esse expoente. Faz a conta de uma parcela: a derivada da coordenada horizontal sobre a distância elevada ao expoente, na direção horizontal. Dá um sobre a distância elevada ao expoente, menos o expoente vezes o quadrado da coordenada horizontal, sobre a distância elevada ao expoente mais dois. As outras parcelas são iguais, cada uma com a sua coordenada. Agora soma: os três primeiros termos dão três; e os quadrados das coordenadas somam a distância ao quadrado, que cancela o mais dois do expoente. Sobra o número de parcelas menos o expoente. No plano são duas parcelas; no espaço, três. Então o divergente no espaço é três menos o expoente, dividido pela distância elevada ao expoente. Para zerar, o expoente é três, e o tamanho do campo fica um sobre a distância ao quadrado. A lei do inverso do quadrado, a de Coulomb e a da gravitação.

[thoughtful, emphatic] No plano, o número que aparece é dois; no espaço, é três. O expoente da lei vem da dimensão do espaço: em três dimensões, o campo tem mais lugar para se espalhar. E fica o cuidado: não é o rotacional ou o divergente sozinhos que decidem a lei. É a lei física, o rotacional zero ou o divergente zero fora da fonte, junto com a simetria: as linhas em círculo em volta do fio e o campo radial em volta da carga. Com as duas juntas, não sobra escolha.

### S · Síntese, gancho e CTA

[thoughtful] Olha a escada inteira. A mesma fórmula conta dois filmes, e é o divergente que mede a área do fluido. Um campo se desenha pelas curvas onde ele não muda. O rotacional de um redemoinho e o divergente de uma explosão saem da mesma conta, e o sentido da volta não é o sentido do giro. Um gradiente nunca gira, e um rotacional nunca diverge. Ter derivadas parciais não basta: a tabela só vale quando elas são contínuas. E, com ela, você prevê o quadradinho antes de soltar. [curious] E nas aplicações: um rio reto que gira nas margens, uma parede onde a água só se deforma, mapas que nunca entortam, e o rotacional e o divergente escolhendo o um sobre a distância e o um sobre a distância ao quadrado.

[excited] No próximo vídeo, a gente troca de pergunta. Até aqui, tudo foi medido num ponto, bem de perto. Agora é hora de somar pedacinhos. Uma chapa quadrada, de dois metros de lado, leve num canto e cada vez mais densa até o canto oposto: qual é a massa dela? Oito quilos? Dezesseis? A resposta exata vem de uma soma de infinitos pedacinhos: a integral dupla.

[happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual degrau da escada foi o mais difícil para você? Até a próxima!

*(Na tela do gancho: cartão `NO PRÓXIMO VÍDEO` · `SOMA DE RIEMANN E INTEGRAL DUPLA` com a chapa colorida [0, 2]² e a régua da massa com `8 kg?` e `16 kg?`, as mesmas peças do yt_0029. Sem número de episódio nem Atlas. Depois, o CTA padrão.)*

---


---

## Anexo B · Conferência

`verificacao/verifica_calc3_e1_sympy.py` (75 checagens, todas True; saída em `verificacao/verifica_calc3_e1_saida.txt`). Os dois vão no zip.
