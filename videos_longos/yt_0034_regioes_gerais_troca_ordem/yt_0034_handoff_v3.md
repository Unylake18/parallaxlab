# yt_0034 · CÁLCULO III · EP. 09 · Regiões gerais e troca de ordem
# AVALIAÇÃO DO PREVIEW v2 + HANDOFF v3 · preview silencioso (540p, 15 fps)

Para o Claude Code. Handoff autocontido: tudo o que precisa está aqui e no zip `yt0034_handoff_v3_completo.zip` (este documento + `yt_0034_narracao_v3.md`, a fala completa já montada + `yt_0034_quadros_alvo_v3/` com 7 quadros-alvo, a folha de contato e as fontes `sb34v3.html` e `c3d34.html`, que já têm as chaves novas `s3i`, `s3p`, `s3d` do sino).
Base: o código do preview v2 (`sec_h`, `sec_a`, `sec_b1`…`sec_b8`, `sec_s`, `lib34.py`, `pecas34.py`, `kit.py`, `qa34.py`, `montar.py`). Só a unidade `videos_longos/yt_0034_regioes_gerais_troca_ordem/` muda.
Briefing de Produção: matemática, roteiro e quadros-alvo abaixo são especificação. Inconsistência objetiva: reportar antes de ampliar o escopo.

---

## 0. O que entregar

1. Preview v3 silencioso do vídeo inteiro, 540p / 15 fps, com a narração v3 (§7) como trilha-guia de tempo (TTS provisório ou duração estimada a 3 palavras/s, como no v2).
2. QA do §9, no mesmo formato do v2 (`qa/`), mais a lista das contas do §2 com o tempo em que cada passo aparece.
3. Zip `yt0034_v3_para_gpt` (em partes, se passar de 30 MB), com o preview, o código, o QA e a ficha atualizada.
4. Antes do preview: aplicar o §10 (regra CONTAS SEM PULAR no AGENTS.md e no docs/padrao_video_longo.md, pedido explícito do Kaio).
5. Parar. Sem voz final, sem 1080p, sem entrega.

---

## 1. Avaliação do v2

**O que melhorou e fica:** o QA veio limpo (sobreposição 0, flash 0, palco vazio 0, 3D no canto 0, cartão 10,9 s). Ficam como estão: o gráfico do sino com a área no H1, a fatia zero/f/zero do B1-2, a cunha 3D com o pouso, o B4-3 com o começo que anda e o gráfico `(1 − x)·0,7468`, a chapa do B5, os painéis do B6 na coluna, o B7 com leve/pesado e o S1 em três painéis.

**O que ainda não funciona.** O Kaio não está curtindo, e com razão. O v2 resolveu os defeitos, mas o vídeo ainda **mostra pouco o fenômeno e corta as contas**:

| # | Onde | Problema | Correção (seção) |
|---|---|---|---|
| P1 | H1, 0:00–0:20 | Abre com uma fórmula e um gráfico pequeno; nos primeiros 10 s não há promessa visual nem virada. | Abertura nova com a peça 3D e as duas facas (§4) |
| P2 | B4-2, 9:09–9:21 | **O sino 3D não lê.** Em pé: duas peças separadas, ligadas por uma linha âmbar. Deitada: uma placa magenta solta, sem a peça em volta. (A culpa é do quadro-alvo v1, que pedia para afastar as peças. Aqui ele é substituído.) | Sino refeito: peça inteira, a parte da frente da faca vira traço, câmera de frente para cada corte (§3.1) |
| P3 | o vídeo todo | O fenômeno central (volume = soma das áreas das fatias, em qualquer sentido) aparece só em dois 3D. No resto, o palco é a região plana. | Imagem nova: a **área de cada fatia como função**, as duas curvas com a mesma área embaixo (§3.2) |
| P4 | B1-3, B3-1, B3-2, B4-2, B5-2, B6, B7-1, B8 | **Contas puladas**: `π·2²/4` sem a integral; `(8 − 8/3)/2` direto; `[−(4 − y²)^{3/2}/3]` direto; `[−e^(−y²)/2]` direto; `8/3 + 2y² − 4y³/3` sem F(2) − F(y); `(1 − cos 1)/3` sem a substituição; `1/2 + 1/2` sem primitiva; `7/16` sem origem. | Regra CONTA INTEIRA e as 9 contas escritas passo a passo (§2) |
| P5 | B4-1 (8:15–8:27), B6 (12:03–12:15) | Fórmula sozinha no centro e palco vazio por ~12 s. | Aberturas com o palco já armado e os limites voando (§5) |
| P6 | 12:21 | A região do B6 aparece como uma mancha lilás que se deforma até virar a região. | Pintar com tiras em pé depois da curva lida (§5) |
| P7 | 0:39 | O glyph map do H1 passa por um quadro embaralhado (termos cruzando no meio). | §5 |
| P8 | A1, 1:39–1:51 | Os cinco chips nascem como caixas vazias, e o texto entra depois. | §5 |
| P9 | S2 | O gancho é um cartão parado. Promete "a parábola vira duas curvas?" e só. | Gancho com a saída trocando de curva na frente do aluno, mais três promessas concretas (§6) |

Resumo: **o v3 é uma passada de conteúdo, não de correção.** Entram uma abertura nova, o sino 3D refeito, a imagem da área da fatia (duas vezes: na cunha e no sino), todas as contas inteiras, as aberturas do B4-1 e do B6 e um gancho novo. Com isso a narração cresce cerca de 4 min (≈ 21 min no total). Isso é esperado e está dentro do padrão da série.

---

## 2. Regra CONTA INTEIRA (vale para o vídeo todo)

Toda conta do vídeo segue a escada abaixo, **sem pular degrau**. Cada degrau é uma linha a caneta ou um `TransformByGlyphMap` a partir da linha de cima, e a narração lê cada degrau (§7).

- **O1 · primitiva com colchete:** `∫ₐᵇ g = [G]ₐᵇ = G(b) − G(a) = número`. O `G(b)` e o `G(a)` aparecem escritos, com os valores substituídos (nunca só a resposta).
- **O3 · comprimento = saída − entrada:** a integral de 1 (ou de uma constante) na fatia é escrita como `[x]` ou `[y]` entre os limites e depois como `saída − entrada`.
- **O4 · substituição:** linha `u = …  ⇒  du = …  ⇒  (o pedaço da integral) = …du`, e logo abaixo a linha **dos limites novos** (`y = 0 → u = …`, `y = 1 → u = …`). Se o limite inverte, a linha do sinal aparece (`−∫₄⁰ = ∫₀⁴`).
- **O2 · origem geométrica:** quando o desenho dá a expressão (raiz como altura, comprimento da fatia), a expressão nasce no desenho com uma chave e voa para a coluna (`TransformFromCopy`).
- A coluna nunca passa de 7 linhas. Quando enche, as linhas já usadas sobem e saem por glyph map, e o resultado parcial vira chip no topo da coluna (padrão da série). Nunca fica linha órfã começando por "=".

### As 9 contas (texto exato da coluna; cores do kit: x âmbar, y magenta, f ciano, entrada azul-claro, saída coral, resultado menta)

**C1 · B1-3 · a área π (quadro-alvo `v3_03`).** Origem no desenho: o ponto da fatia na circunferência, o raio `2` até ele, o ângulo `θ` medido a partir do eixo y, o cateto horizontal `x = 2 sen θ` (âmbar) e o cateto vertical `√(4 − x²) = 2 cos θ` (magenta). As duas expressões nascem no desenho e voam para a coluna.
```
∫₀² √(4 − x²) dx
x = 2 sen θ  ⇒  dx = 2 cos θ dθ
x = 0 → θ = 0        x = 2 → θ = π/2
= ∫₀^{π/2} 2cos θ · 2cos θ dθ = ∫₀^{π/2} 4cos²θ dθ
cos²θ = (1 + cos 2θ)/2
= 2[θ + sen 2θ/2]₀^{π/2}
= 2(π/2 + 0) − 2(0 + 0) = π
```
Depois, a conferência geométrica que já existia: `π · 2²/4 = π` (chave "UM QUARTO DO DISCO") e a régua 3,25 · 3,17 · 3,15 → π.

**C2 · B3-1 · cunha em pé.**
```
∫₀^{√(4−x²)} y dy = [y²/2]₀^{√(4−x²)} = (√(4−x²))²/2 − 0²/2 = (4 − x²)/2
∫₀² (4 − x²)/2 dx = ½[4x − x³/3]₀²
= ½[(8 − 8/3) − (0 − 0)] = ½ · 16/3 = 8/3
```
Mantém a chave "BASE · ALTURA / 2" no triângulo, que confere `(4 − x²)/2`.

**C3 · B3-2 · cunha deitada (substituição com limite invertido).**
```
∫₀^{√(4−y²)} y dx = y[x]₀^{√(4−y²)} = y√(4 − y²)
∫₀² y√(4 − y²) dy
u = 4 − y²  ⇒  du = −2y dy  ⇒  y dy = −du/2
y = 0 → u = 4        y = 2 → u = 0
= −½∫₄⁰ √u du = ½∫₀⁴ u^{1/2} du
= ½[⅔ u^{3/2}]₀⁴ = ½ · ⅔ · 8 = 8/3  ✓
```
O `y` que multiplica e o `−2y` do `du` acendem juntos (cor menta) antes da linha do `u`.

**C4 · B4-2 · sino, passo 3 (quadro-alvo `v3_06`).** O palco é a fatia deitada em 2D, que vem do pouso: o retângulo magenta com a chave `y` = COMPRIMENTO embaixo e `e^(−y²)` = ALTURA ao lado. O `y` voa da chave para a primeira linha.
```
∫₀^y e^(−y²) dx = e^(−y²)[x]₀^y = y e^(−y²)
∫₀¹ y e^(−y²) dy
u = y²  ⇒  du = 2y dy  ⇒  y dy = du/2
y = 0 → u = 0        y = 1 → u = 1
= ½∫₀¹ e^(−u) du = ½[−e^(−u)]₀¹
= ½(−e^(−1) − (−e⁰)) = (1 − 1/e)/2
≈ (1 − 0,368)/2 ≈ 0,316
```

**C5 · B5-1 · triângulo de baixo, em pé.**
```
∫₀^x (x² + y²) dy = [x²y + y³/3]₀^x = (x³ + x³/3) − 0 = 4x³/3
∫₀² 4x³/3 dx = (4/3)[x⁴/4]₀² = (4/3)(16/4 − 0) = 16/3
```

**C6 · B5-2 · o mesmo triângulo, deitado.**
```
∫_y² (x² + y²) dx = [x³/3 + y²x]_y²
= (8/3 + 2y²) − (y³/3 + y³) = 8/3 + 2y² − 4y³/3
∫₀² (8/3 + 2y² − 4y³/3) dy = [8y/3 + 2y³/3 − y⁴/3]₀²
= 16/3 + 16/3 − 16/3 = 16/3  ✓
```

**C7 · B6 · sen(x³) (substituição u = x³).** A primeira linha usa o painel ESTA FATIA que já existe: o `x²` voa da chave do comprimento.
```
∫₀^{x²} sen(x³) dy = sen(x³)[y]₀^{x²} = x² sen(x³)
∫₀¹ x² sen(x³) dx
u = x³  ⇒  du = 3x² dx  ⇒  x² dx = du/3
x = 0 → u = 0        x = 1 → u = 1
= ⅓∫₀¹ sen u du = ⅓[−cos u]₀¹ = ⅓(−cos 1 + cos 0) = (1 − cos 1)/3 ≈ 0,153
```

**C8 · B7-1 · telhado.** Comprimento = saída − entrada em cada ordem.
```
EM PÉ:   ∫_{−1}^0 (1 + x) dx + ∫₀¹ (1 − x) dx
       = [x + x²/2]_{−1}^0 + [x − x²/2]₀¹ = (0 − (−½)) + (½ − 0) = ½ + ½ = 1
DEITADO: ∫₀¹ [(1 − y) − (y − 1)] dy = ∫₀¹ (2 − 2y) dy = [2y − y²]₀¹ = 1
```
Na versão deitada, o `(1 − y)` voa do rótulo coral e o `(y − 1)` voa do rótulo azul-claro.

**C9 · B8 · Ana e Bia, 7/16 pelo complemento (O2).** Em vez de três integrais, o que fica de fora são dois triângulos nos cantos, com catetos 3/4 (chaves nos catetos).
```
fora = 2 · ½ · (3/4)² = 9/16
chance = 1 − 9/16 = 7/16 ≈ 44%
```

Todas as contas foram conferidas em sympy: π, 8/3 (três caminhos), (1 − 1/e)/2 ≈ 0,31606, A(0,2) ≈ 0,5495, A(0,6) ≈ 0,4186, (1 − cos 1)/3 ≈ 0,15323, 16/3 (nas duas ordens), telhado 1 (nas duas), 9/2 (gancho).

---

## 3. Representação dos fenômenos

### 3.1 O sino 3D refeito (Three.js, cena 2; quadros-alvo `v3_01`, `v3_02`)

Fonte de referência: `c3d34.html`, chaves `s3i` (peça inteira), `s3p` (faca em pé), `s3d` (faca deitada). Portar a lógica para a cena 2 da unidade. A parte nova é a função `traco()` e as duas câmeras.

- **A peça nunca se separa.** Nada de afastar as metades.
- **Faca em pé em x = 0,2** (era 0,4; em 0,2 o teto mostra o ombro do sino e fica claramente curvo). Fica opaca a parte `0 ≤ x ≤ 0,2` (a face do corte olha para +x, de frente para a câmera) com a face **âmbar**. A parte `x > 0,2` vira **traço**: só as arestas (contorno do chão, contorno do teto, arestas verticais), em tubos finos `#6C7698`, raio 0,0065 (mundo ×2). Sem transparência, sem brilho.
- **Faca deitada em y = 0,6.** Fica opaca a parte `y ≥ 0,6` com a face **magenta** (olha para −y), e a parte `y < 0,6` vira traço.
- **Câmeras, uma de frente para cada corte** (fov 22°, up = +z, alvo (1,0; 1,1; 0,4) no mundo ×2):
  - CAMP (em pé): posição (10,6; −2,5; 6,6);
  - CAMD (deitada): posição (4,0; −8,9; 6,6).
  - Entre as duas, a câmera **orbita em 2 s (ease in-out)**, com a peça inteira opaca durante a órbita. A órbita começa só depois que a face âmbar apaga.
- **Rótulos do Manim** presos aos pontos projetados (`ex`, `ez`, `faca`), ≤ 2 px: `x`, `f`, `x = 0,2` / `y = 0,6` com placa.
- **Ordem no B4-2:**
  1. passo 2 em 2D (já existe);
  2. a peça sobe sobre o triângulo (CAMP);
  3. a faca em pé (`v3_01` sem a coluna da abertura);
  4. o pouso lateral para a fatia em pé 2D (teto curvo);
  5. volta e órbita para CAMD;
  6. a faca deitada (`v3_02`);
  7. o pouso para o retângulo 2D, que vira o palco do passo 3 (`v3_06`).
- A cunha 3D do B3 (cena 1) **fica como no v2**: ela já lia bem.

### 3.2 A área de cada fatia (imagem nova, duas vezes; quadros-alvo `v3_04`, `v3_05`)

É a imagem que faltava para o "por que o Fubini vale": **o volume é a soma das áreas das fatias**, e as duas ordens dão curvas de área diferentes com a mesma área embaixo.

- **Cunha, fim do B3-2 (`v3_04`).** Dois gráficos lado a lado no palco:
  - EM PÉ: TRIÂNGULOS, `A(x) = (4 − x²)/2` em [0, 2], âmbar;
  - DEITADA: RETÂNGULOS, `A(y) = y√(4 − y²)` em [0, 2], magenta.
  - Ponto marcado em `x = 1` (A = 1,5, o triângulo do 3D) e em `y = 1` (A = √3 ≈ 1,73, o retângulo do 3D). Cada ponto nasce **voando da face colorida do pouso** que acabou de sair.
  - A curva é traçada da esquerda para a direita, com o ponto deslizando (a fatia andando).
  - Depois, as duas áreas pintam e recebem `8/3` (menta).
  - Coluna: `A(x)`, `A(y)` e `∫₀² A(x)dx = ∫₀² A(y)dy = 8/3`.
  - Selo: CURVAS DIFERENTES, MESMA ÁREA.
- **Sino, B4-2 depois das duas facas (`v3_05`).** Igual, em [0, 1]:
  - EM PÉ: `A(x) = ∫ₓ¹ e^(−y²) dy`. Calcular com `math.erf`: `A(x) = (√π/2)(erf 1 − erf x)`. Ela cai de 0,7468 a 0; ponto em `x = 0,2` (≈ 0,549). Selo: SEM FÓRMULA, MAS EXISTE.
  - DEITADA: `A(y) = y e^(−y²)`; ponto em `y = 0,6` (≈ 0,419).
  - As duas áreas pintam e recebem `0,316`.
  - A frase da narração "só que a da direita a gente sabe integrar" acende a curva magenta; corte para o passo 3.
- Escalas iguais nos dois gráficos de cada par. Grade só no palco, nascendo dos eixos.

---

## 4. Abertura nova (0:00–0:16) + H1 ajustado

A abertura (âncora nova **H0**) dá a promessa e a virada antes de qualquer explicação. Ela usa a cena 2 do sino (mesmas chaves do §3.1), a coluna à direita e o canto "UMA INTEGRAL QUE TRAVA".

| t (s) | Gatilho | Tela |
|---|---|---|
| 0,0–1,0 | "Olha esta peça" | O triângulo do chão pinta por tiras em pé (rápido), com os eixos x, y e z. |
| 1,0–2,5 | "Olha esta peça" | A peça sobe do chão (z de 0 até e^(−y²)), câmera CAMP parada. |
| 2,5–4,5 | "integral dupla" | A integral a caneta na coluna. |
| 4,5–7,5 | "trava logo na primeira conta" | A faca em pé desce em x = 0,2: a parte de trás vira traço, a face âmbar acende, `∫ₓ¹ e^(−y²) dy = ?`, ✗ SEM PRIMITIVA EM FÓRMULA. Estado final = `v3_01`. |
| 7,5–10,0 | "faca no outro sentido" | A face âmbar apaga, o traço volta a sólido, a órbita para CAMD (2 s). O ✗ e a linha do `?` saem. |
| 10,0–13,5 | "em duas linhas" | A faca deitada em y = 0,6, a face magenta; glyph map da integral para a ordem trocada; o resultado a caneta (exato primeiro). |
| 13,5–16,0 | "Só mudou a faca" | ✓ MESMA PEÇA, OUTRA FACA. Estado final = `v3_02`. |

No **H1**, a peça sai e entra o gráfico do sino do v2 (que fica). A integral **não é reescrita**: ela já está na coluna. O texto do H1 muda (§7) para não repetir o resultado. O glyph map do H1 (para a ordem trocada) passa a acontecer com a frase "teto reto", e os limites que mudaram acendem no desenho como no v2.

---

## 5. Aberturas com palco e pequenos ajustes

- **B4-1 (P5).** A integral do hook volta **direto na posição da coluna** (voo a partir do chip, nunca no centro). Os eixos com a grade `papel` já estão no palco no mesmo instante. Os limites voam um a um, na ordem da voz:
  1. `0` e `1` para o eixo x;
  2. o `x` de baixo vira a reta `y = x` (azul-claro, traçada da origem);
  3. o `1` de cima vira a reta `y = 1` (coral).
  4. Depois, as tiras em pé pintam o triângulo.
  
  Palco nunca vazio: no máximo 1,5 s de eixos sem objeto.
- **B6 (P5, P6).** Mesmo esquema:
  1. a fórmula nasce na coluna com o palco armado;
  2. os limites voam (`0` e `1` no eixo y, a curva `x = √y` traçada de baixo para cima, a reta `x = 1`);
  3. a tira deitada aparece;
  4. o glyph map `x = √y ⇔ y = x²` acontece;
  5. **só depois** a região é pintada por tiras em pé, da esquerda para a direita, entre `y = 0` e `y = x²`.
  
  Nunca usar Transform de forma para pintar a região (é a mancha das 12:21).
- **H1, glyph map (P7).** Refazer o mapa para que nenhum glifo cruze outro no meio do caminho: os limites que mudam saem por `auto_fade` e entram a caneta; os termos que ficam (`∫`, `e^(−y²)`) só deslizam. Conferir os quadros do meio da animação no QA (§9).
- **A1 (P8).** Cada chip nasce inteiro: a borda e o texto juntos, na mesma animação (caneta no texto, traço na borda, simultâneos).
- **B4-3, o erro clássico.** Fica. Só ajustar a frase da fala ao `x = 0,2` se ela citar 0,4 (a do v2 não cita).

---

## 6. Gancho novo (S2; quadro-alvo `v3_07`)

O gancho precisa mostrar o problema acontecendo, e não só perguntar.

1. A região entre `y = x` e `y = 4x − x²` (0 ≤ x ≤ 3) é traçada: a reta coral, o ramo esquerdo da parábola azul-claro e o ramo direito coral. A tira em pé atravessa em 1 s: uma conta.
2. A tira **deitada** começa embaixo, em y ≈ 1,5: entra na parábola (azul-claro) e sai na reta (coral). Ela **sobe devagar**. A linha tracejada `y = 3` (ALERTA) aparece um instante antes, e na passagem por y = 3 o ponto coral de saída **pula da reta para o ramo direito**, junto com o selo A SAÍDA TROCA. A tira continua até y = 3,5 e para. Os rótulos `x = 2 − √(4 − y)` e `x = 2 + √(4 − y)` voam do glyph map `y = 4x − x² ⇒ x = 2 ∓ √(4 − y)`, que é escrito na coluna antes do cartão. A cópia da tira em y = 1,5 fica apagada (alpha 0,35) para comparar.
3. O cartão NO PRÓXIMO VÍDEO: EXERCÍCIOS DO MÓDULO entra no gatilho falado e fica **≥ 8 s**, com os três itens acendendo um a um, na voz:
   - 1. A PARÁBOLA VIRA DUAS CURVAS;
   - 2. `sen y / y` SÓ SAI TROCANDO;
   - 3. DOIS CILINDROS: UM VOLUME SEM π.
4. Depois, o CTA padrão.

(Para a Produção: o EP. 10 precisa cumprir os três itens. Hoje a proposta dele cumpre: a parábola é o E4, `sen y / y` está no E5 e os dois cilindros no E7.)

---

## 7. Narração v3 (substitui os trechos abaixo; o resto da narração v2.1 fica igual. A fala inteira, montada, está em `yt_0034_narracao_v3.md`)

Tags permitidas: [curious], [thoughtful], [surprised], [happy], [excited], [serious]. Uma por parágrafo (S2 tem duas). Números por extenso. Leitura dos símbolos como no Anexo B da v2.1. Acrescentar ao Anexo B: "teta" para θ e "u" para u.

### H0 · a peça e as duas facas (NOVO, antes do H1)
**Gatilhos:** "Olha esta peça"→chão e a peça sobe · "integral dupla"→integral a caneta · "trava logo na primeira conta"→faca em pé + ✗ · "faca no outro sentido"→órbita + faca deitada · "em duas linhas"→glyph map + resultado · "Só mudou a faca"→✓
> [curious] Olha esta peça. O volume dela é uma integral dupla, e essa integral trava logo na primeira conta. Agora, a mesma peça, cortada com a faca no outro sentido: em duas linhas, sai metade de um menos um sobre é. Mesma peça, mesmo volume. Só mudou a faca.

### H1 · uma integral que trava (SUBSTITUI)
**Gatilhos:** "Vamos devagar"→a peça sai, entra o gráfico do sino · "E aí trava"→placa e chips riscados · "teto curvo"→a área de x até 1 no gráfico acende · "teto reto"→glyph map para a ordem trocada · "os limites mudaram"→limites acendem · "um triângulo"→o triângulo · "os limites novos"→a tira deitada no triângulo
> [thoughtful] Vamos devagar. A integral é esta: integral de zero a um, da integral de xis até um, de é elevado a menos ípsilon ao quadrado, dê ípsilon, dê xis. O é é o número de Euler, dois vírgula setenta e um e pouco. Pela regra do vídeo passado, a gente começa por dentro: precisa de uma primitiva de é elevado a menos ípsilon ao quadrado. E aí trava. Essa primitiva existe, mas não se escreve com nenhuma combinação das funções do Cálculo um: nada de polinômio, seno, logaritmo, nada. Na peça, cada fatia em pé tem o teto curvo, um pedaço do sino. Com a ordem trocada, integral de zero a um, da integral de zero até ípsilon, dê xis, dê ípsilon, cada fatia deitada tem o teto reto. E repara: os limites mudaram. O xis até um virou zero até ípsilon. A gente não trocou só o dê xis com o dê ípsilon: mudou o jeito de percorrer a região. Porque essa integral não mora num retângulo. Ela mora num triângulo. E aí entram duas perguntas: como fica o teorema de Fubini quando a região não é um retângulo? E como achar os limites novos sem mudar o valor?

### B1-3 · a área pi (SUBSTITUI; conta C1)
**Gatilhos:** "f igual a um"→coluna · "comprimento da fatia"→segmento acende · "dá a área"→varredura · "o desenho entrega"→ponto na circunferência e raio 2 · "teta"→ângulo · "dois seno de teta"→cateto x voa · "dois cosseno de teta"→cateto vertical voa · "dê xis é"→linha 2 · "Os limites mudam junto"→linha 3 · "quatro cosseno ao quadrado"→linha 4 · "um mais cosseno de dois teta"→linha 5 · "A primitiva"→linha 6 · "Resultado: pi"→linha 7 · "a geometria confirma"→`π·2²/4` com a chave · "três vírgula vinte e cinco"…"três vírgula quinze"→régua · "o valor exato"→ponto π
> [happy] Agora o caso mais simples: f igual a um. A integral de dentro, de zero até raiz de quatro menos xis ao quadrado, de um, dê ípsilon, é só o comprimento da fatia. E somar os comprimentos de todas as fatias dá a área. Fica a integral de zero a dois de raiz de quatro menos xis ao quadrado, dê xis. Vamos fazer essa conta inteira, porque o desenho entrega a substituição. Liga o ponto de cima da fatia com a origem: é um raio, de tamanho dois. Chamando de teta o ângulo com o eixo ípsilon, o xis é dois seno de teta, e a altura, raiz de quatro menos xis ao quadrado, é dois cosseno de teta. Então dê xis é dois cosseno de teta, dê teta. Os limites mudam junto: xis igual a zero é teta igual a zero, e xis igual a dois é teta igual a pi sobre dois. A integral vira a integral de zero a pi sobre dois de quatro cosseno ao quadrado de teta, dê teta. E cosseno ao quadrado é um mais cosseno de dois teta, sobre dois. A primitiva fica dois vezes, teta mais seno de dois teta sobre dois. Em pi sobre dois, dá dois vezes pi sobre dois; em zero, dá zero. Resultado: pi. E a geometria confirma: um quarto de pi erre ao quadrado, com raio dois, também dá pi. Lembra das caixinhas? Com quatro divisões, três vírgula vinte e cinco; com dezesseis, três vírgula dezessete; com trinta e duas, três vírgula quinze. Elas estavam chegando em pi, três vírgula catorze. Fatiando, sai o valor exato.

### B3-1 · a cunha: a fatia em pé é um triângulo (SUBSTITUI; conta C2)
**Gatilhos:** como no v2, mais: "ípsilon ao quadrado sobre dois"→`[y²/2]` · "No limite de cima"→`G(b) − G(a)` · "quatro xis menos xis ao cubo sobre três"→primitiva de fora · "dezesseis terços"→`½ · 16/3` · "oito terços de quilo"→resultado
> [curious] Agora uma chapa em forma de quarto de disco, mas com densidade que cresce com a altura: ípsilon quilos por metro quadrado. Desenhando a densidade como altura, aparece uma cunha. Fatia em pé, em xis igual a um. A fatia vai de zero até raiz de quatro menos xis ao quadrado, e a altura dela em cada ponto é o próprio ípsilon: ela é um triângulo. A integral de dentro é de zero até raiz de quatro menos xis ao quadrado, de ípsilon, dê ípsilon. A primitiva de ípsilon é ípsilon ao quadrado sobre dois. No limite de cima, raiz de quatro menos xis ao quadrado, ao quadrado, sobre dois; no de baixo, zero. Fica quatro menos xis ao quadrado, sobre dois. E é exatamente a área do triângulo: base vezes altura sobre dois, com base e altura iguais a raiz de quatro menos xis ao quadrado. Agora a de fora: integral de zero a dois de quatro menos xis ao quadrado, sobre dois. O meio sai para fora, e a primitiva de quatro menos xis ao quadrado é quatro xis menos xis ao cubo sobre três. Em dois, oito menos oito terços, que dá dezesseis terços; em zero, zero. Metade de dezesseis terços: oito terços de quilo.

### B3-2 · a fatia deitada é um retângulo (SUBSTITUI; conta C3 + `v3_04`)
**Gatilhos:** os do v2 até "um retângulo", mais: "ípsilon vezes xis"→`y[x]` · "quase a derivada"→`y` e `−2y` acendem · "chama u"→linha do u · "os limites mudam junto"→linha dos limites · "O menos inverte"→`−∫₄⁰ = ∫₀⁴` · "dois terços de u elevado a três meios"→primitiva · "oito terços de novo"→✓ · "como funções"→corte para `v3_04` · "triângulo"→curva âmbar · "retângulo"→curva magenta · "a mesma: oito terços"→áreas pintam · "Isso é o Fubini"→selo · "Guarda essa diferença"→cartão `EM PÉ: ALTURA MUDA → TRIÂNGULO` / `DEITADA: ALTURA FIXA → RETÂNGULO`
> [thoughtful] Agora deitado. Primeiro, um passo que vai aparecer em toda troca de ordem: a curva tem que ser lida pelo outro eixo. Ípsilon igual a raiz de quatro menos xis ao quadrado. Eleva ao quadrado, isola o xis e fica com a raiz positiva, porque aqui o xis é positivo: xis igual a raiz de quatro menos ípsilon ao quadrado. E olha a fatia: a altura é ípsilon em todo ponto dela, então ela é um retângulo. A integral de dentro é ípsilon vezes xis, de zero até raiz de quatro menos ípsilon ao quadrado: altura vezes comprimento, ípsilon vezes raiz de quatro menos ípsilon ao quadrado. Agora a de fora, de zero a dois. Repara: o ípsilon que multiplica é quase a derivada do que está dentro da raiz. Então chama u de quatro menos ípsilon ao quadrado. Dê u é menos dois ípsilon dê ípsilon, então ípsilon dê ípsilon é menos dê u sobre dois. E os limites mudam junto: ípsilon igual a zero dá u igual a quatro, e ípsilon igual a dois dá u igual a zero. O menos inverte os limites, e fica meio da integral de zero a quatro de raiz de u, dê u. A primitiva de raiz de u é dois terços de u elevado a três meios, e quatro elevado a três meios é oito. Meio vezes dois terços vezes oito: oito terços de novo. Agora olha as fatias como funções. Em pé, a área de cada triângulo é quatro menos xis ao quadrado, sobre dois. Deitada, a área de cada retângulo é ípsilon vezes raiz de quatro menos ípsilon ao quadrado. São curvas diferentes, mas a área embaixo das duas é a mesma: oito terços. Isso é o Fubini: o volume é a soma das áreas das fatias, em qualquer sentido. Guarda essa diferença. Quando a fatia vai na direção em que a função não muda, a integral de dentro vira altura vezes comprimento. E esse comprimento pode ser exatamente o fator que falta na conta de fora.

### B4-2 · reler deitado: as duas facas no sino (SUBSTITUI; §3.1 + `v3_05`)
**Gatilhos:** "reler o triângulo deitado"→passo 2 · "sai na diagonal"→limite `y` voa · "olha a peça"→a peça sobe (CAMP) · "zero vírgula dois"→faca em pé · "travava"→pouso: fatia em pé 2D · "zero vírgula seis"→órbita + faca deitada · "um retângulo"→pouso: retângulo · "a área de cada fatia"→corte para `v3_05` · "não tem fórmula, mas existe"→curva âmbar + selo · "ípsilon vezes é"→curva magenta · "mesma área embaixo"→áreas pintam · "a da direita"→curva magenta acende
> [excited] Segundo passo: reler o triângulo deitado. Agora o ípsilon vai de zero a um, e, para cada ípsilon, a fatia entra no eixo, em xis igual a zero, e sai na diagonal, em xis igual a ípsilon. E olha a peça de novo. Em pé, em xis igual a zero vírgula dois, o teto da fatia é um pedaço do sino, curvo, e é por isso que a conta travava. Deitada, em ípsilon igual a zero vírgula seis, o é elevado a menos ípsilon ao quadrado não muda ao longo da fatia: o teto é reto, e a fatia é um retângulo. Agora desenha a área de cada fatia. Em pé, a área é a integral de xis até um do sino: ela não tem fórmula, mas existe, e vai caindo até zero. Deitada, a área é ípsilon vezes é elevado a menos ípsilon ao quadrado. Curvas diferentes, mesma área embaixo. Só que a da direita a gente sabe integrar.

### B4-2b · passo 3: calcular (NOVO; conta C4, `v3_06`)
**Gatilhos:** "Terceiro passo"→palco: retângulo com as chaves · "sai para fora"→`e^(−y²)[x]` · "altura vezes comprimento"→`y e^(−y²)` (o `y` voa da chave) · "a de fora"→linha 2 · "quase a derivada do expoente"→`y` e `−y²` acendem · "Chama u"→linha do u · "Ípsilon igual a zero"→limites · "meio da integral"→linha 5 · "Em um"…"Em zero"→linha 6 · "Metade disso"→resultado
> [thoughtful] Terceiro passo: calcular. A de dentro é a integral de zero até ípsilon de é elevado a menos ípsilon ao quadrado, dê xis. O é elevado a menos ípsilon ao quadrado não depende de xis e sai para fora; sobra xis, de zero até ípsilon, que dá ípsilon. Altura vezes comprimento. Agora a de fora: integral de zero a um de ípsilon vezes é elevado a menos ípsilon ao quadrado, dê ípsilon. Esse ípsilon, que veio do comprimento da fatia, é quase a derivada do expoente. Chama u de ípsilon ao quadrado: dê u é dois ípsilon dê ípsilon, então ípsilon dê ípsilon é dê u sobre dois. Ípsilon igual a zero dá u igual a zero, e ípsilon igual a um dá u igual a um. Fica meio da integral de zero a um de é elevado a menos u, dê u. A primitiva é menos é elevado a menos u. Em um, menos um sobre é; em zero, menos um. Menos um sobre é, menos menos um: um menos um sobre é. Metade disso: zero vírgula três um seis. A integral que travava virou uma conta de poucas linhas, porque a gente mudou o jeito de percorrer a região.

### B5-1 · a chapa cortada na diagonal (SUBSTITUI só o fim; conta C5)
> … A integral de dentro vai de zero até xis, de xis ao quadrado mais ípsilon ao quadrado, dê ípsilon. A primitiva em ípsilon é xis ao quadrado vezes ípsilon, mais ípsilon ao cubo sobre três. Em ípsilon igual a xis, dá xis ao cubo mais xis ao cubo sobre três; em zero, zero. Somando, quatro terços de xis ao cubo. A de fora: quatro terços de xis à quarta sobre quatro, de zero a dois, dá quatro terços vezes quatro: dezesseis terços de quilo.

(O início, até "dê ípsilon.", fica igual ao v2.1.)

### B5-2 · a outra ordem e o espelho (SUBSTITUI só o meio; conta C6)
> … Repara que o limite de baixo mudou: antes era o zero, agora é a diagonal. A primitiva em xis é xis ao cubo sobre três, mais ípsilon ao quadrado vezes xis. Em xis igual a dois, oito terços mais dois ípsilon ao quadrado; em xis igual a ípsilon, ípsilon ao cubo sobre três mais ípsilon ao cubo. Subtraindo: oito terços, mais dois ípsilon ao quadrado, menos quatro terços de ípsilon ao cubo. A primitiva disso, de zero a dois, dá dezesseis terços, mais dezesseis terços, menos dezesseis terços. Sobra dezesseis terços. Mesmo valor, como o teorema garante. …

(O começo e o espelho, do "E tem uma conferência" em diante, ficam iguais ao v2.1.)

### B6-1 · seno de xis ao cubo (SUBSTITUI só o fim; conta C7)
> … Como seno de xis ao cubo não depende de ípsilon, a fatia é um retângulo, e a de dentro dá seno de xis ao cubo vezes ípsilon, de zero até xis ao quadrado: xis ao quadrado vezes seno de xis ao cubo. No sino, o comprimento da fatia trouxe o fator ípsilon; aqui, trouxe xis ao quadrado, que é quase a derivada de xis ao cubo. Chama u de xis ao cubo: dê u é três xis ao quadrado dê xis. Xis de zero a um dá u de zero a um. Fica um terço da integral de zero a um de seno de u, dê u. A primitiva é menos cosseno de u: menos cosseno de um, mais cosseno de zero. Resultado: um menos cosseno de um, sobre três. Mais ou menos zero vírgula um cinco três.

### B7-1 · quando a região se divide (SUBSTITUI só o trecho da conta; conta C8)
> … a integral vira duas integrais somadas. À esquerda, a primitiva de um mais xis é xis mais xis ao quadrado sobre dois; de menos um a zero, dá meio. À direita, a de um menos xis, de zero a um, dá meio também. Meio mais meio: área um. Fatiando deitado, toda fatia entra pela esquerda, em xis igual a ípsilon menos um, e sai pela direita, em xis igual a um menos ípsilon. O comprimento é a saída menos a entrada: dois menos dois ípsilon. Integrando de zero a um, dois ípsilon menos ípsilon ao quadrado: um. Uma conta só. …

### B8 · regiões gerais no mundo (SUBSTITUI só o trecho do cálculo; conta C9)
> … "Eles se encontram" é a faixa em volta da diagonal, de um quarto de hora para cada lado. Fatiando, essa faixa daria três pedaços. Mas tem um atalho: olha o que fica de fora. São dois triângulos nos cantos, com catetos de três quartos. Cada um tem área meio de três quartos ao quadrado; os dois juntos, nove dezesseis avos. A chance de eles se encontrarem é um menos nove dezesseis avos: sete dezesseis avos, quase quarenta e quatro por cento. …

### S2 · o próximo vídeo e CTA (SUBSTITUI)
**Gatilhos:** "um desafio"→região · "Em pé, é uma conta só"→tira em pé · "Agora deitado"→tira deitada embaixo · "a saída troca"→linha y = 3 e o pulo do ponto coral + selo · "vira duas curvas"→glyph map + os dois rótulos · "No próximo vídeo"→cartão · "essa parábola"…"sem pi nenhum"→itens 1–3 · "deixa o like"→CTA
> [curious] E fica um desafio. Olha a região entre a reta ípsilon igual a xis e a parábola ípsilon igual a quatro xis menos xis ao quadrado. Em pé, é uma conta só. Agora deitado. Lá embaixo, a fatia entra na parábola e sai na reta. Mas, quando ela passa de ípsilon igual a três, a saída troca: deixa a reta e vai para o outro lado da parábola. E, lida pelo eixo ípsilon, a parábola vira duas curvas: dois menos raiz de quatro menos ípsilon, e dois mais raiz de quatro menos ípsilon. Quantas contas aparecem? E o valor fecha? No próximo vídeo, os exercícios do módulo: essa parábola, uma integral de seno de ípsilon sobre ípsilon que só sai trocando a ordem, e dois cilindros que se cruzam e dão um volume sem pi nenhum. [happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual integral você já viu travar numa ordem e sair na outra? Até a próxima!

### Tempo

| Âncora | Palavras v2.1 | Palavras v3 | Voz (s) | Início estimado |
|---|---:|---:|---:|---:|
| H0 (novo) | — | 48 | 16.0 | 0:00 |
| H1 | 212 | 200 | 66.7 | 0:16 |
| H2 | 67 | 67 | 22.3 | 1:22 |
| A1 | 61 | 61 | 20.3 | 1:45 |
| B1-1 | 198 | 198 | 66.0 | 2:05 |
| B1-2 | 173 | 173 | 57.7 | 3:11 |
| B1-3 | 125 | 269 | 89.7 | 4:08 |
| B2-1 | 158 | 158 | 52.7 | 5:38 |
| B2-2 | 158 | 158 | 52.7 | 6:31 |
| B3-1 | 141 | 208 | 69.3 | 7:24 |
| B3-2 | 168 | 338 | 112.7 | 8:33 |
| B4-1 | 115 | 115 | 38.3 | 10:26 |
| B4-2 | 173 | 160 | 53.3 | 11:04 |
| B4-2b (novo) | — | 201 | 67.0 | 11:57 |
| B4-3 | 134 | 134 | 44.7 | 13:04 |
| B5-1 | 127 | 150 | 50.0 | 13:49 |
| B5-2 | 129 | 165 | 55.0 | 14:39 |
| B6-1 | 188 | 253 | 84.3 | 15:34 |
| B7-1 | 182 | 243 | 81.0 | 16:58 |
| B7-2 | 127 | 127 | 42.3 | 18:19 |
| B8 | 162 | 191 | 63.7 | 19:02 |
| S1 | 125 | 125 | 41.7 | 20:05 |
| S2 | 120 | 168 | 56.0 | 20:47 |
| **Total** | **3043** | **3910** | **21:43** | |

A 3 palavras/s: v2.1 ≈ 16:54 de fala; v3 ≈ 21:43 (+867 palavras). Com respiros e o CTA, o vídeo deve ficar perto de 22 min.

---

## 8. O que NÃO fazer

- Não separar as peças do sólido em nenhum 3D (nem no sino, nem na cunha).
- Não usar transparência, brilho, sombra ou partícula. O traço é linha fina opaca.
- Não escrever nenhum resultado sem os degraus do §2. Nem por seta, nem por "dá".
- Não abrir cena com a fórmula no centro e o palco vazio.
- Não pintar região por Transform de forma (sempre por tiras).
- Não rerenderizar o 1080p nem gerar voz. Fase: preview v3.
- Não alterar `template/`, `assets/` nem outras unidades.

## 9. QA do preview v3 (obrigatório)

Repetir o QA do v2 (sobreposição, flash por quadro com zero eventos, palco parado > 5 s = 0, palco vazio, folga, 3D no canto, cartão ≥ 8 s) e acrescentar:

1. **CONTAS:** tabela com as 9 contas (C1–C9), cada degrau com o tempo em que aparece e a frase da fala que o dispara. Nenhum degrau ausente.
2. **SINO 3D:** quadros em CAMP e CAMD (estado final de cada faca) ao lado de `v3_01`/`v3_02`; as peças nunca se afastam; alinhamento dos rótulos ≤ 2 px (`timeline.json`).
3. **ÁREAS DAS FATIAS:** quadros finais do B3-2 e do B4-2 ao lado de `v3_04`/`v3_05`. Conferir os valores numéricos `A(0,2) ≈ 0,549`, `A(0,6) ≈ 0,419`, `A(1) = 1,5` e `A(1) ≈ 1,73`.
4. **ABERTURAS:** quadros em 0:00, 0:02, 0:05, 0:09, 0:12, 0:15. Para o B4-1 e o B6, os 4 primeiros segundos, um quadro por segundo (nenhum com o palco vazio).
5. **GLYPH MAPS:** para o H1 e os glyph maps novos do §2, um quadro no meio da animação (50 %) de cada. Nenhum glifo cruzando outro.
6. **GANCHO:** quadros antes, durante e depois do pulo da saída em y = 3, mais o quadro do cartão com os três itens.
7. Duração total e por âncora, comparando com a tabela do §7.

## 10. Documentação global: regra CONTAS SEM PULAR (pedido explícito do Kaio, 2026-11-14)

Este handoff autoriza editar dois arquivos globais, **só com os trechos abaixo**. Fazer isso antes de começar o preview e listar no relatório.

**a) `AGENTS.md`**, na seção "Animações matemáticas", logo depois do item **Escrita (desde 2026-11-08)**, acrescentar:

```
- **Contas sem pular (desde 2026-11-14):** toda conta, em longo ou curto, é desenvolvida passo a passo, na tela e na fala, do básico ao avançado. Nenhum resultado aparece sem os degraus:
  - primitiva com colchete `[G]ₐᵇ` → `G(b) − G(a)` com os valores substituídos → número;
  - substituição com a linha `u = … ⇒ du = …`, a linha dos limites novos e o sinal quando o limite inverte;
  - substituição trigonométrica com o triângulo no desenho;
  - comprimento da fatia = saída − entrada;
  - número que vem da geometria nasce no desenho com chave e voa para a coluna.
  Nada de "dá" nem de seta pulando degrau; a narração lê cada degrau (acrescentar frases se preciso). O QA lista cada conta com o tempo de cada degrau. Detalhe: `docs/padrao_video_longo.md` §8.
```

**b) `docs/padrao_video_longo.md`**, no fim do §8 (escrita da álgebra), acrescentar a subseção:

```
### 8.x Contas sem pular (desde 2026-11-14)

Regra do Kaio para todos os vídeos com conta. Cada degrau é uma linha a caneta ou um TransformByGlyphMap a partir da linha de cima.

| Forma | Escada obrigatória |
|---|---|
| O1 primitiva | `∫ₐᵇ g = [G]ₐᵇ = G(b) − G(a) = número` (G(b) e G(a) escritos com os valores) |
| O2 geometria | a expressão nasce no desenho com chave (base·altura/2, πr², altura = 2 cos θ…) e voa para a coluna |
| O3 comprimento | `[x]` ou `[y]` entre os limites → saída − entrada |
| O4 substituição | `u = … ⇒ du = … ⇒ (pedaço) = …du`; linha dos limites novos; linha do sinal se o limite inverte |
| O5 valor no ponto | `f(x₀, y₀)` com a conta |
| O6 fórmula-mãe | a fórmula geral antes de qualquer número |

- A coluna tem no máximo 7 linhas; o resultado parcial vira chip no topo; nunca linha órfã começando por "=".
- A narração lê cada degrau; se a fala não cobre um degrau, acrescentar a frase.
- QA obrigatório: tabela "CONTAS" com cada degrau, o tempo em que aparece e a frase que o dispara. Nenhum degrau ausente.
- Modelo: as contas C1–C9 do yt_0034 (handoff v3 §2).
```

Não mexer em mais nada desses dois arquivos. Sem commit/push, salvo pedido do Kaio.

## 11. Parada

Aplicar o §10 (docs), depois entregar o preview v3 + QA + zip e parar. Relatório no formato do AGENTS.md: arquivos alterados, verificações com resultados, caminhos dos artefatos, pendências reais.
