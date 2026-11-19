# HANDOFF v2 · yt_0041 · CÁLCULO III · EP. 16 · Coordenadas esféricas na integral tripla

Data: 2026-11-16. Fase: **preview v2** (540p15, silencioso). Não gere voz, SRT, 1080p nem entrega.
Base: o preview v1 do Claude Code (19:48,8, QA limpo, kit copiado do yt_0037) e o handoff v1.1, que continua valendo em tudo o que este documento não muda.

Formato `longo_horizontal`, série Cálculo I–IV:
- fundo violeta liso;
- grade `papel(ax)` de borda a borda no 2D (3D e CTA ficam lisos);
- 3D em Three.js; álgebra em Manim com caneta finíssima.

**Notação (lei de Gauss):** ρ = densidade (ciano), r = distância (laranja), R = raio fixo, s = r sen φ = sombra (pêssego), φ a partir de +z em [0, π], θ longitude, T = a transformação.

**Cores:**

| Grandeza | Cor |
|---|---|
| r | `#FF9440` |
| φ | `#B48CFF` |
| θ | `#2EE6A6` |
| s | `#FFC08A` |
| r² sen φ | `#C6F26B` |
| ρ | `#35D9FF` |
| x | `#FFC24D` |
| y | `#EA63FF` |
| z | `#5AA2FF` |

**Conversão px → Manim (1080p):** `x_m = (x_px − 960)/120`, `y_m = (540 − y_px)/120`. O `config_horizontal.py` usa o quadro 16 × 9.

---

## 0. O que muda, em uma frase por eixo

1. **Leitura:** fórmulas maiores, com a coluna ocupando a metade direita (§2).
2. **Perspectiva:**
   - a bola é cortada por um **octante**, não por uma cunha de frente: acaba o "coração";
   - endereço com **duas vistas 2D**;
   - casquinha e lata com o **corte meridiano 2D**;
   - receita com **sólido** (§3).
3. **Sobreposições:** as 27 correções da §1, cada uma com critério de aceite.
4. **Conta inteira:** os degraus que faltavam (menores 2×2, massa até c, cone e esfera cartesianos, ordem da substituição) entram com glyph maps (§4).
5. **Narração v1.4:** a tela mostra todos os degraus com calma e a voz conversa como professor durante a conta, sem ler número por número e sem silêncio; ≈ 22:12 (§5).

---

## 1. Quadros-alvo v2 (pasta `yt_0041_quadros_alvo_v2/`)

São 11 alvos novos, só das cenas que mudam. A folha de contato é `00_folha_contato_v2.jpg`.

| Arquivo | Bloco | Estado final da cena |
|---|---|---|
| `01_H1_bola_octante_v2.jpg` | H1 | Bola com o octante cortado; `PESADA NA CASCA` acima, à direita; coluna a 50 px |
| `03_B1-1_endereco_duas_vistas_v2.jpg` | B1-1 | 3D à esquerda; painéis PÁGINA (DE LADO) e CHÃO (DE CIMA); 4 fórmulas a 50 px |
| `07_B2-2_duas_polares_v2.jpg` | B2-2 | Dois painéis grandes; 2×2 da página embaixo à esquerda; cartão OS FATORES SE MULTIPLICAM |
| `08a_B2-3_menores_v2.jpg` | B2-3, etapa 1 | Matriz a 44 px, menor M₃₁ tracejado, escada do M₃₁, linha do M₃₂ |
| `08b_B2-3_expansao_v2.jpg` | B2-3, etapa 2 | Chips M₃₁ e M₃₂ no topo; expansão em 4 linhas; moldura; chip dV |
| `10b_B3-2_receita_v2.jpg` | B3-2 | Região sólida (duas cascas, dois cones), sonda ENTRA/SAI, selos ①②③ |
| `11_B4_cebola_octante_v2.jpg` | B4 | Cebola em quartos de anel, casca laranja; 5 linhas |
| `12_B5_massa_ate_c_v2.jpg` | B5, etapa 2 | Bola com o contorno r = 0,84; MÉDIA; MASSA ATÉ c em 3 linhas |
| `13a_B6-1_casquinha_corte_v2.jpg` | B6-1 | 3D pequeno; corte meridiano grande; cone e esfera desde as cartesianas |
| `13b_B6-2_substituicao_v2.jpg` | B6-2 | Corte à esquerda; escada da substituição na ordem certa |
| `14_S2_lata_corte_v2.jpg` | S2 | Lata 3D pequena; corte 1 × 1 com as duas sondas; cartão do próximo vídeo |

**Fontes dos alvos:**
- `sb41.html` (compositor canvas + KaTeX; `?k=<chave>`; as chaves v2 são `h1v2 b1v2 b22v2 b23v2 b23bv2 b32 b4v2 b5v2 b61 b62 s2v2`);
- `c3d41.html` (Three.js r128; as chaves 3D novas são `bola8 bola8c cebola8 receita`);
- `r3d.js` (render por Playwright, PNG transparente + `r3d_pts.json` com as coordenadas de tela);
- `shot2.js` (gera os 11 JPG).

Copie a geometria das funções `bolaOct` e da chave `receita` do `c3d41.html` para o `threejs/` da unidade.

**Os alvos v1.1 que continuam valendo** (`yt_0041_quadros_alvo_v1_1/`), com a regra de tamanho da §2 aplicada:
- 02 H2;
- 04 B1-2, com as duas vistas do 03 v2 no lugar das fórmulas e as do ponto (2, π/6, π/3);
- 05 B1-3, com a ordem nova da §3.3;
- 06 B2-1, com a órbita da §3.4;
- 09 B2-4;
- 10 B3-1.

**Os alvos têm prioridade sobre o texto quando houver dúvida de posição.** O que o alvo não mostra (ordem, voo, tempo) está nas seções abaixo.

---

## 2. Regra de tamanho (vale para o vídeo todo)

O v1 mediu ≈ 24–30 px de glifo a 1080p, com um terço da tela vazio. Na v2:

| Elemento | Tamanho de referência (KaTeX font-size, igual aos alvos) | Altura de maiúscula a 1080p |
|---|---|---|
| Fórmula principal | 50–54 | ≈ 36–40 px |
| Fórmula secundária / matriz | 44 | ≈ 32 px |
| Legenda Space Grotesk | 30 | ≈ 22 px de x-height, ≥ 26 px de corpo |
| Rótulo 3D (letra) | 36–42 | — |

**Layout:**
- **Coluna** a partir de x = 1010 px até a margem direita (48 px). O 3D ocupa de x = 48 a 960.
- No máximo **5 linhas por etapa**. Quando passar, a coluna renova e o resultado sobe como **chip no topo** (nunca uma linha órfã começando por `=`).
- **Blocos 2D** (B2-2, B2-3): ocupam a tela inteira, como nos alvos 07, 08a e 08b.
- **Painel 2D dentro de cena 3D** (B1-1, B6-1, B6-2, S2): painel opaco `#16123A` com cantos de 14 px, **grade própria** de 30 px em `#2B2558` e borda `GEO` a 45 %. É o `painel2d()` do `sb41.html`. O painel cobre o 3D por baixo, então nada do 3D aparece atrás dele.

**Critério de aceite:**
- medir no 1080p final a altura do `x` da fórmula principal de cada bloco: ≥ 34 px;
- nenhum texto com corpo < 26 px.

---

## 3. Vistas novas

### 3.1 Octante (H1, B4, B5, B7)
- **Corte:** tira-se o octante θ ∈ [−π/2, 0], φ ∈ [0, π/2] (x > 0, y < 0, z > 0 no Three.js; ver `bolaOct` no `c3d41.html`). Aparecem três faces de quarto de disco: θ = 0, θ = −π/2 e φ = π/2 (o chão).
- **Faces:** pintadas pela cor da distância (`corFace(r)`):
  - H1/B5: degradê escuro no centro → ciano na borda;
  - B4: bandas [0; 0,2; 0,4; 0,6; 0,7; 0,8; 1], com a faixa 0,6–0,7 em laranja (a casca de raio r, espessura dr).
- **Câmera:** `ver([9.2, −6.2, 5.8], [0, 0, −0.1], 600, 560)`, SC = 2.
- **B5:** o contorno laranja de r = 0,84 aparece nas três faces (chave `bola8c`).
- **Rótulos:** os eixos x e y só aparecem se a ponta estiver visível. Os pontos `ex`, `ey` e `ez` do `r3d_pts.json` são as pontas; o y fica fora da bola no octante.

### 3.2 Duas vistas no endereço (B1-1, B1-2)
- O 3D do ponto fica à esquerda (esc 0,95).
- Na coluna entram dois painéis 2D de 420 × 350:
  - **PÁGINA (DE LADO):** z para cima, s para o lado, segmento r, arco φ e tracejados;
  - **CHÃO (DE CIMA):** x, y, segmento s, arco θ e tracejados.
- **Ordem:**
  1. o triângulo 3D acende;
  2. o painel PÁGINA desenha (eixos → r → φ → tracejados), e `z = r cos φ` voa do cateto vertical do painel e `s = r sen φ` do horizontal;
  3. o painel CHÃO desenha, e `x = s cos θ` e `y = s sen θ` voam dele;
  4. a segunda igualdade (`= r sen φ cos θ`) é um glyph map que troca o s pela sua fórmula.
- **Rótulos:** r e φ fora do segmento (r a 14 px do lado de fora do triângulo; φ dentro do arco); s e θ no painel do chão, sem tocar o tracejado.

### 3.3 Caixa vira bola (B1-3)
1. A caixa entra com eixos e rótulos.
2. A célula lima acende na caixa e fica 2 s.
3. A seta T entra.
4. **Uma cópia** da célula viaja ao longo da seta e se deforma até a casca curva na bola. A original fica na caixa em contorno lima.
5. As bordas ruins acendem nas duas peças juntas.

Critério: a seta nunca aparece antes da caixa, e a célula nunca é uma lasca menor que 30 px.

### 3.4 Caixinha curva (B2-1)
- Uma órbita única de ≈ 35° em 4 s logo depois da célula ampliada, para mostrar a aresta Δr. A câmera para antes da primeira aresta acender.
- As arestas acendem uma por vez. Cada rótulo (`Δr`, `r Δφ`, `r sen φ Δθ`) fica numa placa **fora** da célula, com fio-guia fino até a aresta.
- As miniaturas POLO e EQUADOR ficam uma por linha. O painel cresce até a RAZÃO caber, com 30 px de margem.

### 3.5 Receita sólida (B3-2), alvo 10b
- **Região:** r ∈ [0,5; 1], φ ∈ [π/6, π/3], θ ∈ [0, 3π/2], renderizada como sólido:
  - casca de fora `#C46A78`;
  - casca de dentro azul-claro;
  - cones e tampas das pontas em lima.
- **Sonda:** sai da origem em φ = π/4, tracejada até a entrada e cheia até a saída. Pontos: O branco, ENTRA azul-claro, SAI coral.
- **Câmera:** `ver([9.0, −6.8, 4.6], [0, 0, 0.25], 600, 560)`.
- **Corte de cena:** corte seco depois do B3-1 (sem dissolve sobre a caixa). Isso corrige o item 17.

### 3.6 Casquinha com o corte meridiano (B6-1, B6-2), alvos 13a e 13b
- **Corte meridiano** (página θ = cte) num `painel2d`:
  - eixo z (até 2,3) e eixo s (até 1,45);
  - reta do cone a 45° (violeta);
  - círculo r = 2 cos φ de centro (0, 1) (coral);
  - região preenchida em ciano a 30 %;
  - tracejados até (1, 1);
  - marcas `1` e `2`.
- **B6-1:**
  - painel 540 × 900 em (430, 140), escala 260 px/unidade, origem (520, 990);
  - 3D pequeno no canto (esc 0,55);
  - sonda laranja em φ = π/6 com o ponto coral na esfera.
  - Rótulos, todos com placa e sem tocar linha: `r = 2 cos φ` à esquerda do ponto; `φ = π/4` acima da reta, fora do círculo; `(1, 1)` à esquerda, embaixo do ponto.
- **B6-2:**
  - o painel vai para a esquerda (440 × 900 em (60, 140), escala 230, origem (130, 990));
  - sem a sonda;
  - a coluna começa em x = 560.
- **Conferência π/3 + 2π/3:** no mesmo painel. O triângulo do cone fica violeta e a meia bola de cima ciano (etapa 2 do `corteCasq`). Nada se separa no espaço.

### 3.7 Lata com o corte meridiano (S2), alvo 14
- Lata 3D pequena no alto à esquerda (esc 0,55), sem cruzar o título do canto.
- **Corte 1 × 1** num `painel2d` de 560 × 480 em (60, 560), escala 300, origem (150, 990):
  - diagonal tracejada em vermelho-alerta;
  - sonda da parede com `r = 1/sen φ` à direita do ponto;
  - sonda da tampa com `r = 1/cos φ` dentro do quadrado, embaixo da tampa, com placa.
- A legenda `A FÓRMULA RACHA NA DIAGONAL: φ = π/4` vai para a coluna, na cor de alerta, e não fica solta no desenho.
- O cartão do próximo vídeo fica à direita.

### 3.8 Câmera
Uma órbita curta só onde ela revela profundidade: H1 (já existe), B2-1 (§3.4) e B6-1 (já existe). Nunca durante a escrita. O resto fica parado.

---

## 4. Conta inteira (degraus novos e ordem)

Cada `→` é um `TransformByGlyphMap` com mapa explícito (MathTex de string única nos dois lados). Os glyph maps só são montados depois que o LaTeX estiver estável. O termo que vem do desenho voa por `TransformFromCopy`. O cancelamento é feito em dois tempos: o par acende na mesma cor e some junto.

### A1 · B2-3, os menores 2×2 (alvos 08a e 08b)

**Etapa 1 (08a):**
1. Matriz a 44 px; legenda `1ª COLUNA: EM r · 2ª: EM φ · 3ª: EM θ`; seta `LINHA DE BAIXO: + − +`.
2. Tracejado lima em volta do menor do cos φ (linhas 1–2, colunas 2–3). Legenda `O MENOR DO cos φ: TAMPA A LINHA 3 E A COLUNA 1`.
3. `M_{31} = r\cos\varphi\cos\theta\cdot r\sin\varphi\cos\theta-(-r\sin\varphi\sin\theta)\cdot r\cos\varphi\sin\theta`. Os quatro fatores **voam** das quatro células do menor, na ordem diagonal principal → diagonal secundária.
4. `→ = r^2\sin\varphi\cos\varphi\cos^2\theta + r^2\sin\varphi\cos\varphi\sin^2\theta`. Glyph map: os r se juntam em r², o sen φ e o cos φ se agrupam e o (−)(−) vira +.
5. `→ = r^2\sin\varphi\cos\varphi\,\underbrace{(\cos^2\theta+\sin^2\theta)}_{=1} = r^2\sin\varphi\cos\varphi`.
6. O mesmo para o M₃₂: tracejado nas colunas 1 e 3; legenda `O MENOR DO −r sen φ: TAMPA A LINHA 3 E A COLUNA 2`. Três linhas, como no M₃₁:
   - `M_{32} = \sin\varphi\cos\theta\cdot r\sin\varphi\cos\theta-(-r\sin\varphi\sin\theta)\cdot\sin\varphi\sin\theta`;
   - `= r\sin^2\varphi\cos^2\theta + r\sin^2\varphi\sin^2\theta`;
   - `= r\sin^2\varphi\,(\cos^2\theta+\sin^2\theta) = r\sin^2\varphi`.

   O alvo 08a mostra o M₃₂ numa linha só, por falta de altura. No vídeo, a escada do M₃₁ sobe e vira chip **antes** de o M₃₂ começar, e o M₃₂ ganha as mesmas 3 linhas.

**Etapa 2 (08b):**
1. Chips `M₃₁ = r² sen φ cos φ` (lima) e `M₃₂ = r sen²φ` no topo.
2. Linha 1: `\det = +\cos\varphi\cdot M_{31} - (-r\sin\varphi)\cdot M_{32} + 0\cdot M_{33}`. O cos φ e o −r sen φ voam da linha de baixo da matriz; os sinais voam da legenda `+ − +`.
3. Linha 2: `= \cos\varphi\cdot r^2\sin\varphi\cos\varphi + r\sin\varphi\cdot r\sin^2\varphi + 0`. Os chips voam para o lugar de M₃₁ e M₃₂; o `−(−` vira `+` em dois tempos.
4. Linha 3: `= r^2\sin\varphi\cos^2\varphi + r^2\sin^3\varphi`.
5. Linha 4: `= r^2\sin\varphi\,\underbrace{(\cos^2\varphi+\sin^2\varphi)}_{=1} = r^2\sin\varphi`, com moldura verde-menta **folgada**: 18 px de cada lado, sem tocar glifo.
6. Chip `dV = r² sen φ dr dφ dθ` à direita da moldura. É ele que voa no B3-1 (glyph map 9, item 16).
7. Legenda `0 ≤ φ ≤ π: SEN φ ≥ 0, O MÓDULO NÃO MUDA NADA`.

### A2 · B4 (alvo 11)
Sempre `\dfrac{4\pi R^3}{3}` (nunca `\tfrac43\pi R^3`). Linhas, nesta ordem:
1. `\int_0^{2\pi}\!\int_0^{\pi} r^2\sin\varphi\,d\varphi\,d\theta = r^2\cdot[-\cos\varphi]_0^{\pi}\cdot[\theta]_0^{2\pi}`;
2. `= r^2\cdot 2\cdot 2\pi = 4\pi r^2`, com `ÁREA DA ESFERA`;
3. `V = \int_0^R 4\pi r^2\,dr = 4\pi\big[\tfrac{r^3}{3}\big]_0^R = \dfrac{4\pi R^3}{3}`;
4. `\dfrac{d}{dR}\Big(\dfrac{4\pi R^3}{3}\Big) = 4\pi R^2`, com `ENGORDAR = UMA CASCA`;
5. `ρ SÓ DE r: \iiint\rho\,dV = \int_0^R \rho(r)\,4\pi r^2\,dr`.

O 2 e o 2π da linha 2 voam do teste da bola (B2-4), guardados como chip.

### A3 · B5, massa até c (alvo 12)
**Etapa 1:** como no v1.1 (M = π). O chip `V = 4π/3 (R = 1)` voa do resultado do B2-4 (item 21: nasce na coluna, nunca no topo centralizado).

**Etapa 2** (a etapa 1 vira o chip `M = π`):
1. `MÉDIA \dfrac{M}{V} = \dfrac{\pi}{4\pi/3} = \pi\cdot\dfrac{3}{4\pi} = \dfrac34`;
2. `MASSA ATÉ c  M(c) = \int_0^{2\pi}\!\int_0^{\pi}\!\int_0^{c} r^3\sin\varphi\,dr\,d\varphi\,d\theta`. Glyph map da integral do M = π: o limite 1 vira c;
3. `= \Big[\dfrac{r^4}{4}\Big]_0^c\cdot 2\cdot 2\pi = \Big(\dfrac{c^4}{4}-0\Big)\cdot 2\cdot 2\pi = \pi c^4`. O 2 e o 2π voam da etapa 1;
4. `\pi c^4 = \dfrac{\pi}{2} \;\Rightarrow\; c^4 = \dfrac12 \;\Rightarrow\; c = \sqrt[4]{\dfrac12} \approx 0{,}84`;
5. Legenda `METADE DA MASSA MORA NOS 16% DE FORA DO RAIO`. O contorno r = 0,84 acende na bola no gatilho "metade da massa".

### A4 · B6-1, cone e esfera desde as cartesianas (alvo 13a)
1. `CONE  z = \sqrt{x^2+y^2}`;
2. `→ r\cos\varphi = r\sin\varphi \;\Rightarrow\; \operatorname{tg}\varphi = 1 \;\Rightarrow\; \varphi = \dfrac{\pi}{4}`. Glyph map: z → r cos φ e √(x² + y²) → s → r sen φ, com as chaves voando das fórmulas do B1-1 (guardadas como chip);
3. `ESFERA  x^2+y^2+z^2 = 2z`;
4. `→ r^2 = 2r\cos\varphi \;\Rightarrow\; r = 2\cos\varphi \quad (r>0)`. Glyph map: x² + y² + z² → r² e z → r cos φ; o r que divide some em dois tempos;
5. `x^2+y^2+(z-1)^2 = 1`, com `CENTRO (0, 0, 1)`;
6. `V = \int_0^{2\pi}\!\int_0^{\pi/4}\!\int_0^{2\cos\varphi} r^2\sin\varphi\,dr\,d\varphi\,d\theta`. Os limites voam do corte 2D: π/4 da reta do cone, 2 cos φ do rótulo da esfera.

### A5 · B6-2, a substituição na ordem (alvo 13b)
O chip `V = …` fica no topo da coluna (x = 560). Linhas, nesta ordem, uma por vez:
1. `\Big[\dfrac{r^3}{3}\Big]_0^{2\cos\varphi}\sin\varphi = \dfrac{(2\cos\varphi)^3}{3}\sin\varphi - 0 = \dfrac83\cos^3\varphi\,\sin\varphi`;
2. `u = \cos\varphi,\quad du = -\sin\varphi\,d\varphi`;
3. `\varphi = 0 \to u = 1,\qquad \varphi = \dfrac{\pi}{4} \to u = \dfrac{\sqrt2}{2}`;
4. `\int_0^{\pi/4}\dfrac83\cos^3\varphi\,\sin\varphi\,d\varphi = \dfrac83\int_1^{\sqrt2/2} u^3\,(-du)`. Os limites 1 e √2/2 voam da linha 3; u³ e −du voam das linhas 2 e 3;
5. `→ = \dfrac83\int_{\sqrt2/2}^{1} u^3\,du`, com a legenda `O MENOS INVERTE OS LIMITES`. Glyph map: os dois limites trocam de lugar em arco e o `−` e os parênteses somem juntos;
6. `= \dfrac83\Big[\dfrac{u^4}{4}\Big]_{\sqrt2/2}^{1} = \dfrac83\Big(\dfrac14-\dfrac1{16}\Big) = \dfrac83\cdot\dfrac3{16} = \dfrac12`;
7. Etapa seguinte: `V = 2π · 1/2 = π ✓` e `CONFERE π/3 + 2π/3 = π` (corte 2D pintado).

**Itens 23 e 24:**
- a integral nova nunca nasce antes de u, du e os limites;
- quando a coluna renova, a última linha sobe junto com o chip, numa só animação, e nunca fica órfã.

### A6 · B2-4
Os degraus extras que o v1 desenhou (`R³/3 − 0`, `2π − 0`) ficam na tela. Pela regra da §5, a voz não os lê número por número: conversa sobre cada integral (potência, primitiva do seno, volta inteira) enquanto eles são escritos.

---

## 5. Narração v1.4 (a tela mostra a álgebra, a voz conversa como professor)

Arquivo: `yt_0041_narracao_v1_4.md`. Ele substitui o v1.1 e o v1.2. Total: **3.967 palavras, ≈ 22:12**. Nenhuma âncora ficou mais curta que na v1.2.

**Regra permanente do Kaio (2026-11-15, com o esclarecimento das 21:30):**
- A coluna escreve **todos** os degraus da §4, **com calma**, no ritmo padrão da caneta. Não acelere a escrita.
- A voz **não lê número por número**, mas também **nunca deixa a tela escrevendo em silêncio**. Na conta mecânica, ela conversa como professor enquanto o degrau é escrito: diz a ação, lembra o que o aluno já sabe e avisa o sinal que engana. Exemplos: "diagonal principal menos diagonal secundária", "menos com menos vira mais", "o MMC é dezesseis".
- Cada âncora traz a **Coluna** marcada [ensina] / [mecânica] e os **gatilhos** novos. A Tela é a da v1.2 com as mudanças deste handoff. Os gatilhos da v1.4 valem sobre os da v1.2.

**Sincronia:**
- A cena segue a voz (WAV contínuo).
- Cada degrau começa no seu gatilho ou no trecho de conversa que o acompanha.
- Se uma escada não couber no tempo da fala, **reporte** em vez de acelerar a caneta ou inserir silêncio. A correção é na narração.

**Frases-gatilho:** use as da v1.4 tal como estão. O v1 reescreveu cinco delas. Se alguma não casar com a tela, reporte em vez de reescrever.

## 6. As 27 correções do v1 (tempo do v1 → o que fazer → aceite)

| # | v1 | Bloco | Correção | Aceite |
|---|---|---|---|---|
| 1 | 0:00–0:03 | H1 | O rótulo do eixo y só aparece com a ponta visível; no octante, o y fica fora da bola | Nenhum rótulo pintado sobre a superfície |
| 2 | 0:04–0:52 | H1 | `PESADA NA CASCA` em (640, 215) a 1080p, acima e à direita da bola (alvo 01); `LEVE NO CENTRO` embaixo, com fio | Seta do eixo x sem cruzar placa |
| 3 | 1:38–1:47 | A1 | O texto do 2º chip nasce dentro dele, pela caneta, sem voo | Nada pousa ao lado do logo |
| 4 | 1:56–3:15 | B1-1 | r e s a ≥ 14 px do segmento, do lado de fora do triângulo (no 3D, s com deslocamento (−40, −30)) | Rótulo sem tocar segmento nem tracejado |
| 5 | 2:12–3:12 | B1-1 | As legendas φ/θ nascem no lugar final, abaixo das fórmulas (y ≈ 975 e 1025) | Nenhum texto se move depois de escrito |
| 6 | 4:10–4:18 | B1-3 | Ordem da §3.3 | A seta T nunca existe sem a caixa |
| 7 | 4:30–4:36 | B1-3 | A cópia viaja e a original fica em contorno (§3.3) | Célula ≥ 30 px; seta sem cruzar a célula |
| 8 | 5:12–6:36 | B2-1 | Placas fora da célula, com fio-guia | Nenhuma placa sobre aresta |
| 9 | 6:16–6:36 | B2-1 | Uma miniatura por linha | Sem sobreposição |
| 10 | 6:24–6:36 | B2-1 | O painel cresce até a RAZÃO ter 30 px de margem | A fração dentro do painel |
| 11 | 6:40–7:35 | B2-2 | Layout do alvo 07 (dois painéis 880 × 560 e o 2×2 a 44 px) | Tela sem terço vazio |
| 12 | 7:22–7:26 | B2-2 | O rótulo de origem fica; a cópia sobe em arco por cima. Sem a seta entre os painéis; os subtítulos `(r, φ) → (s, z)` e `(s, θ) → (x, y)` vão ao lado dos títulos | Nenhum voo cruza a própria origem |
| 13 | 9:12–10:30 | B2-4 | Célula esc 0,6 ou no hemisfério de trás; `2π` fora do equador, com placa; `π` colado ao arco | Nada sobre a página vermelha |
| 14 | 10:24–10:30 | B2-4 | Painel de erros +30 px | 30 px de margem |
| 15 | 10:36–11:52 | B3-1 | A célula fica na caixa e na bola, ligadas pela seta T | A imagem-mãe é igual à do B1-3 |
| 16 | 11:08 | B3-1 | O chip dV voa do B2-3 (alvo 08b) para o lugar do módulo do jacobiano | Glyph map 9 com origem |
| 17 | 11:50–11:58 | B3-1→B3-2 | Corte seco; `O CORTE: VOLUME ZERO` com fio até a costura | Sem dissolve sobreposto |
| 18 | 12:00–12:30 | B3-2 | Receita sólida (§3.5) | A região se lê sem narração |
| 19 | 12:12 | B3-2 | `ENTRA` com placa e fio (alvo 10b) | Sem texto sobre linha |
| 20 | 12:32–13:35 | B4 | Octante e cebola (alvo 11) | Sem "coração"; rótulos fora das cascas |
| 21 | 13:36 | B5 | O chip nasce na coluna (A3) | Nada no topo centralizado |
| 22 | 15:44–17:58 | B6 | Corte 2D (alvo 13a): rótulos no 2D, com placa | Placas sem tocar aresta nem sonda |
| 23 | 17:12–17:20 | B6-2 | Ordem do A5 | u, du e os limites antes da integral nova |
| 24 | 17:40 | B6-2 | A última linha sobe com o chip | Zero linha órfã começando por `=` |
| 25 | 19:20–19:40 | S2 | Corte 1 × 1 (alvo 14) | Rótulo na sua sonda; RACHA na coluna |
| 26 | 18:04–18:08 | B7 | O ✓ entra no gatilho da miniatura | ✓ com atraso ≤ 0,3 s |
| 27 | H1, B4, B5, B7 | — | Octante (§3.1) também no B7 | Nenhuma vista de cunha de frente |

---

## 7. QA do preview v2 (relatório obrigatório)

1. **Tamanho:** altura do `x` da fórmula principal por bloco (tabela), ≥ 34 px a 1080p. Nenhum texto < 26 px.
2. **Sobreposição:** zero texto sobre texto, aresta, segmento, seta ou tracejado, por quadro (R5 com selo, canto e eixos incluídos). As entradas `R5V` de trânsito podem ficar, desde que nenhum voo cruze a própria linha de origem.
3. **Flash por quadro:** zero eventos (caneta, sem preview do destino).
4. **Escada:** cada degrau do §4 listado com o tempo em que aparece. Para os degraus com gatilho (narração v1.4), informe também o tempo da frase; diferença ≤ 0,3 s. Nenhum degrau escrito em silêncio; liste qualquer escada que não coube na fala.
5. **Glyph maps:** lista dos `TransformByGlyphMap` por bloco (esperado: A1 ≥ 6, A3 ≥ 2, A4 ≥ 2, A5 ≥ 2).
6. **3D:** alinhamento 3D × Manim ≤ 2 px nas cenas novas (bola8, bola8c, cebola8, receita, casquinha e lata pequenas). Informar resolução e custo por quadro.
7. **Os 27 itens da §6:** um por linha, com OK/NÃO e o tempo do v2.
8. **Comparação com os alvos v2:** um quadro do estado final de cada um dos 11 alvos, lado a lado com o alvo.
9. **Linha órfã:** zero.
10. **Tela parada:** não há portão automático. Só é erro a tela vazia > 0,5 s ou a voz à frente da tela. Nada de animar a espera.

---

## 8. O que NÃO mexer

- A matemática e os resultados: M = π, 3/4, 0,84, V = π, 4πR³/3, 6,58 R³, 4,19 R³, 2 + √3.
- Cores, notação, fundo, grade e caneta.
- Os três caminhos do fator e a ordem dos blocos.
- O 3D já aprovado das cenas que não mudam (h2, caixa, caixinha, ponto).
- O kit de QA herdado do yt_0037.
- Nenhum efeito novo: sem pulso, brilho, partícula, sombra ou palco vivo.
- Documentos globais, template, assets e outras unidades.

## 9. Entrega desta fase
- Preview 540p15 silencioso.
- Relatório da §7.
- Prancha de comparação com os alvos.
- Pare, sem voz, sem 1080p e sem entrega.
