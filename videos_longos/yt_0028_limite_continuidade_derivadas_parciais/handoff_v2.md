# yt_0028 · CÁLCULO III · EP. 03 · Limite, continuidade e derivadas parciais
# Avaliação do preview v1 e HANDOFF v2

Data: 2026-11-11. Preview avaliado: `yt_0028_preview_v1_540p15.mp4` (12:21, 960×540/15). Material avaliado: o vídeo assistido quadro a quadro (1 quadro a cada 2 s, mais trechos a 5–15 fps nos pontos suspeitos), `comparacao_v1`, `sobreposicoes_v1.txt` e `holds.txt`.

A **Parte 1** é a avaliação, para o Kaio. A **Parte 2** é o handoff, para o Claude Code. Ela é autocontida e vem com a pasta `yt_0028_quadros_alvo_v2/` (31 quadros-alvo), com `verificacao/verifica_calc3_t3_sympy.py` (56 checagens, todas `True`) e com a narração nova (Anexo A).

---

# PARTE 1 · AVALIAÇÃO (para o Kaio)

## 1.1 Veredito

A base está boa:
- o sistema visual do EP. 01/02 foi respeitado (fundo, setas, cores, canto, caneta);
- os 18 alvos foram reproduzidos (diferença média de 3 a 8 em 255, posição exata);
- o relatório de sobreposição deu zero.

O que falta é **conteúdo visual**: cada definição aparece como fórmula, mas não ganha uma figura que a explique por partes. Isso aparece no relatório do próprio Claude Code: **54 trechos parados por mais de 3 s, o mais longo com 16 s**, quase todos em cima de definições (B1-3, B1-4, B2-3, B3-3, B5-3). A v2 resolve isso com uma interpretação geométrica para cada pedaço de cada definição e corrige 11 erros de animação. O vídeo vai de 12:21 para cerca de **14,5 min** (2.387 palavras de narração, dentro do limite de 15 min do módulo).

## 1.2 Erros de animação encontrados

| # | Onde | O que acontece | Causa provável | Correção (Parte 2, §5) |
|---|---|---|---|---|
| E1 | 1:33,8–1:36 | **A seta "cai do teto"**: no painel da direita, F(X) nasce com 3,4 u (476 px), sai pelo alto da tela e encolhe em 2 s. | O ponto X começa em (1,4; 0,9), longe de P, onde F(X) = (1,20; 3,18). | X começa a no máximo 0,6 u de P, e a regra nova R6 prende toda seta dentro do seu painel. |
| E2 | 8:43–8:46 | As setas ∂F/∂x e ∂F/∂y voam para a matriz como **borrões** âmbar e magenta. | Seta "escrita" com a caneta (contorno e preenchimento glifo a glifo). | A caneta é só para texto. Seta entra com `GrowArrow` e voa com `Transform`. |
| E3 | 8:55,6–8:57 | `= (1 −1; 2 0)` nasce de cópias da matriz simbólica que se **sobrepõem** e viram manchas. | `TransformByGlyphMap` de uma matriz 2×2 de frações para números. | Os números nascem na caneta, e cada um voa do valor já calculado no B4 (§6, B6-4). |
| E4 | 8:21–8:30 | O "zoom" não é zoom: o campo **corta** para setas iguais e depois corta de novo para o redemoinho. | Troca da grade sem passo intermediário. | Janela marcada ×10, que cresce até o palco, e o "tira a seta do centro" decomposto numa seta (§6, B6-1 a B6-3). |
| E5 | 6:25,8–6:27 | No começo do passeio vertical, aparece por 1 s uma **seta errada** (curta, para cima) e outra cinza, depois a certa. | F(P) recriada a partir de um vetor provisório. | O fantasma de F(P) sai da própria seta F(P) por `Transform` de cor. |
| E6 | 0:30 e 9:27 | `ÁREA 1.44 → 1.44` e `ÁREA × 1.42` com **ponto decimal**. | Formatação em inglês. | Vírgula sempre: `1,44`, `1,42` (os alvos já estavam com vírgula). |
| E7 | 11:56 | O resumo é **cortado**: `deformação = 1 e 1` ainda estava sendo escrita quando entra o CTA. | Corte do bloco pelo tempo do áudio estimado. | O S termina inteiro e fica ≥ 1,5 s parado antes do CTA. |
| E8 | 0:43–0:56 | O quadradinho do gancho deforma em 2,5 s e fica **13 s parado**. | O fluxo é rápido demais para a fala. | O mesmo fluxo, uma vez só, mais lento: ~6 s, até "Mas virou outra coisa". |
| E9 | 4:36–4:45 | A fórmula da continuidade fica **9 s sozinha** em tela vazia. | Cartões entram só depois. | O B3 começa pelos dois painéis com a definição em pedaços (alvo 08). |
| E10 | toda a peça | 54 trechos parados > 3 s; o máximo é 16 s. | Definição escrita de uma vez e depois esperando a fala. | Cada pedaço da definição tem um gatilho próprio (§6). O relatório deixa de ser só informativo: trecho parado > 3 s precisa de motivo escrito. |
| E11 | 8:58, 9:18, 11:30 | Legendas pequenas demais (`1ª COLUNA: ∂F/∂x…`, `QUINA DA DIREITA…`, `TAMBÉM VALE…`), com fórmula embutida em texto, ilegíveis no celular. | Tamanho de 20–24 px no 1080p. | Mínimo de 26 px para legenda e de 30 px para `MathTex`. Fórmula dentro de legenda vira `MathTex` à parte. |

## 1.3 O que cada definição ganha

| Definição (no vídeo e no livro) | v1 | v2: interpretação geométrica |
|---|---|---|
| **Limite** (ε-δ) | Discos ε e δ, uma volta na borda, e a definição escrita numa linha de 40 px. | Um desafio em 5 passos:<br>1. o ε é escolhido na chegada;<br>2. o seu δ gera a **mancha** (todas as pontas que saem do disco δ);<br>3. δ = 0,7 **vaza** (em vermelho) e encolhe até caber em 0,41;<br>4. a tabela ε → δ (1 → 0,41 · 0,5 → 0,21 · 0,25 → 0,10);<br>5. o **ponto furado** (0 < ‖X − P‖, X ∈ A) e o ponto de acumulação.<br>A definição fica **dividida entre as duas telas**: a metade "onde você anda" embaixo do painel esquerdo, a metade "onde a seta chega" embaixo do direito, com ⇒ no meio. Alvos 02–04. |
| Limite por componentes | Só a fórmula. | **Faixas**: \|P − L₁\| < ε e \|Q − L₂\| < ε formam um quadrado. O disco ε cabe no quadrado, e o quadrado cabe no disco de raio √2·ε. As duas "sombras" da ponta controlam a seta. Alvo 05. |
| Limite que não existe | Três caminhos e 2m/(1 + m²). | Mantido, e ganha a **forma polar**: G = (sen 2θ, 0). Num círculo minúsculo, a ponta varre o segmento [−1, 1], e nenhum disco ε = 0,5 cobre o segmento, seja qual for o L. O mesmo desafio do B1, perdido. Alvo 07. |
| **Continuidade** | Fórmula sozinha e três cartões ("contínuo / fora do domínio / descontínuo"). | Definição em **três pedaços** (① P no domínio, ② o limite existe, ③ limite = F(P)). Primeiro, o desafio do B1 com o ε centrado em F(P) (contínuo). Depois, três cartões, **cada um quebrando um pedaço**: a carga (①), o G (②) e um campo novo, todo (1, 0) com a seta do centro para cima (③, salto no ponto). Alvos 08–09. |
| **Derivada parcial** | Corda, quociente e tangente, em boa parte já certos. | O quociente vira **"a corda ÷ h"**, rotulado. A derivada é a **velocidade da ponta** quando você anda com velocidade 1 (é a leitura do próprio livro: a derivada de x ↦ F(x, y₀)). As **sombras** dela são ∂P/∂x = 1 e ∂Q/∂x = 2, e é por isso que a conta é por componentes. Alvos 10–11. |
| Interpretação geométrica do livro (Ex. 2) | Tangente à curva da ponta. | Mantida, e ampliada na **malha**: uma malhinha em volta de P vai para a tela da chegada. As linhas horizontais viram curvas âmbar e as verticais, curvas magenta, e cada célula vira **quase um paralelogramo** de lados h·∂F/∂x e k·∂F/∂y. Essa é a figura da fórmula da aproximação. Alvo 17. |
| **Classe C¹ / Cʳ** | Uma legenda de 22 px. | **Gráficos** ao longo do eixo vertical: ∂P/∂x vale 1 sempre no campo da aula, e no G vale 2/y, explode e é 0 na origem. Antes disso, a **previsão das parciais** do G (um ponto) contra a imagem de verdade (o segmento todo). Alvos 15–16. |
| **Matriz jacobiana** | Escrita, depois quadradinho e fluxo. | Zoom de verdade; a seta = **seta do centro + resto**; **J·H = h·(1ª coluna) + k·(2ª coluna)** com o paralelogramo das colunas. Alvos 18–22. |
| rot, div, deformações | Fórmulas pequenas sob os cartões. | **Matriz de movimentos**: cada número da tabela é um movimento de aresta (estica a horizontal, gira a horizontal, tomba a vertical, estica a vertical). Depois, as **combinações**: rot = soma dos giros; div = soma dos estiramentos; def₁ = diferença dos estiramentos; def₂ = diferença dos giros, que é quanto o ângulo reto fecha, como uma tesoura. Alvos 25–26. |

Todas as contas novas estão no script (bloco V2: V1 a V16), conferidas.

## 1.4 Cobertura do livro (§1.5 e §1.6) e da proposta

| Conteúdo | v1 | v2 |
|---|---|---|
| ε-δ com P ponto de acumulação e X ∈ A | Faltavam "X ∈ A" e "ponto de acumulação". | **Os dois entram** (na tela e na fala). |
| Limite ⇔ limite das componentes | Só a fórmula. | Com as faixas. |
| Continuidade (P ∈ A) e continuidade por componentes | Sim. | Sim, com os três pedaços. |
| Derivada parcial ① como limite | Sim. | Sim, com corda ÷ h. |
| ① = derivada da curva x ↦ F(x, y₀); existe ⇔ existem as das componentes | Implícito. | Explícito: velocidade da ponta e sombras. |
| Extensão para ℝⁿ → ℝᵐ | Não. | Uma frase (terceira direção, no espaço) e a curiosidade dos 9 números no resumo. |
| Ex. 2 (∂F/∂x tangente à imagem da reta y₀ constante) | Sim. | Sim, e a malha mostra as duas famílias de curvas. |
| Classe Cʳ e Cʳ ⇔ componentes | Só a legenda. | Gráficos, mais Cʳ falado. |
| Cʳ num conjunto não aberto (restrição de G) | Não. | **Fica de fora de propósito**: é uma tecnicalidade sem figura. |
| Ex. 1 do livro e os Exercícios 1.5 (‖F − L‖ → 0, F(P + H), composta, ‖F − L‖ ≤ M‖X − P‖, ‖F‖ > ‖L‖/2) | Não. | Ficam para o **3.1-E1**, o vídeo de exercícios, que o gancho final já promete. O Ex. 1 entra corrigido (∂F/∂y = (2y, 1/y)). |
| Proposta: tese (tabela → rot, div e 2 deformações), gancho do EP. 02, desafio, gancho do 3.1-E1 | Sim. | Sim, mais forte com a matriz de movimentos. |

## 1.5 O que fica como estava

O H (com o fluxo mais lento e vírgula), o A, os três caminhos do B2, a derivada em y, as derivadas no palco, o B5-1, o resíduo, a matriz, as colunas empurrando, o fluxo do modelo, os três cartões e os valores, a volta ao gancho, o desafio e o CTA.

---

# PARTE 2 · HANDOFF v2 (para o Claude Code)

**Fase:** só o **preview visual silencioso** do vídeo inteiro, em 960×540 a 15 fps. Não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

Unidade: `videos_longos/yt_0028_limite_continuidade_derivadas_parciais/` (já existe, da v1). Trabalhe nela e preserve a v1 em `renders/v1/`.

Este handoff é autocontido. Vem junto (zip `yt0028_handoff_v2_completo.zip`):
- `yt_0028_quadros_alvo_v2/`: os **31 quadros-alvo** 1920×1080, `00_folha_contato.jpg` e o gerador `sb28v2.html` (Canvas + KaTeX, `?k=<chave>`; rode com `fundo.png`, as fontes, `logo_crop.png` e `katex/` do lado). O gerador guarda as coordenadas exatas de tudo.
- `verificacao/verifica_calc3_t3_sympy.py` e a saída: **56 checagens, todas `True`**. O bloco novo é o V2 (V1 a V16).

A matemática, o roteiro e os textos estão aprovados pelo Kaio. Não rediscuta. Se encontrar uma inconsistência objetiva, reporte antes de mudar.

## 0. O que entregar

1. As seções alteradas da unidade (`sec_*.py`) e a `ficha.md` atualizada (§1).
2. O preview do vídeo inteiro, `renders/v2/yt_0028_preview_v2_540p15.mp4`, com a duração guiada pela narração do Anexo A (~14,5 min).
3. A prancha **render × alvo** dos 31 quadros, `renders/v2/qa/comparacao_v2.jpg`, mais o `.txt`.
4. Os relatórios `sobreposicoes_v2.txt` (R5), `setas_no_painel_v2.txt` (R6, novo) e `holds_v2.txt` (parado > 3 s, cada ocorrência com motivo).
5. Os quadros dos 11 erros (§5), mostrando o antes (v1) e o depois (v2) no mesmo tempo da fala: `renders/v2/qa/erros_v1_v2.jpg`.
6. O relatório de entrega (AGENTS.md).

## 1. Ficha (o que muda)

```
duracao_alvo: 14–15 min
quadros_alvo: yt_0028_quadros_alvo_v2 (31)
```

O resto da ficha da v1 continua (formato `longo_horizontal`, `CÁLCULO III · EP. 03`, bloco 3.1-T3, `solido_3d: nenhum do arsenal Blender, porque o vídeo é inteiro no plano`, `3d_threejs: nenhuma cena`, referência só na descrição).

## 2. Base de código

- Leia `docs/estado_atual.md`. Rode o script de verificação com o Python da `.venv` (56 linhas `True`). Se faltar sympy ou numpy, não instale nada: diga no relatório e siga.
- Continue na unidade da v1. Reaproveite `kit.py`, `v7.py`, `campo7`, `seta7`, `placa_min`, `TC`/`TX` (caneta), `painel`, o canto e o fundo milimetrado parado.
- **Renderize só o que muda**, por bloco (540p/15), e concatene. O A não muda. O H muda pouco (E6, E8). Os demais blocos mudam.
- Nada de `always_redraw` com `MathTex`. Para a mancha, o zoom e os contadores, use `ValueTracker` com **setas e polígonos** recalculados (`add_updater` em `VMobject`, sem texto), ou passos discretos de `Transform` (6–10 por segundo).
- Quadradinhos andam pelo **fluxo exato**, uma vez só.

## 3. Sistema visual (o da v1, com seis acréscimos)

### 3.1 Recapitulação da v1

- **Layouts.**
  - **A · palco + fórmulas:** palco com origem em (600, 540) px e 120 px/u; coluna de fórmulas em x = 1120.
  - **B · dois painéis:** painéis 700×560 em x 130–830 e 1090–1790, y 260–820. Nomes embaixo, em y = 868: `ONDE VOCÊ ANDA` / `ONDE A SETA CHEGA`. Fórmulas em y ≈ 955. Neste vídeo, 140 px/u nos dois painéis, salvo onde o alvo diz outra coisa.
  - **C · três cartões:** 480×460 em x = 140, 720 e 1300, y 250–710, 56 px/u.
  - Conversão para o Manim: x_m = (x_px − 960)/135; y_m = (540 − y_px)/135.
- **Setas de campo.** Só a flecha (haste 5 px, ponta 19 px, opaca). Comprimento comprimido L = Lmax·(0,4 + 0,6·t). Cor `#2EE6A0 → #8CFFD2`; contexto `#1A5F55`. No G, o comprimento é proporcional. Seta com menos de 6 px não é desenhada.
- **Regras.**
  - R1 · clareira por polígono;
  - R2 · placa mínima;
  - R3 · fórmula nova nunca nasce sobre fórmula velha;
  - R4 · rótulo junto do objeto;
  - R5 · QA de sobreposição medindo a seta inteira.
- **Pedacinho de fluido.** Chapa `#663A4C` com malha 4×4 `#FFB3BC` e contorno coral `#FF7A8A` 4 px; fantasma tracejado.
- **Cores.**

  | Papel | Cor |
  |---|---|
  | Campo, P, Q, F⃗, G⃗, L⃗ | menta `#2EE6A0`/`#8CFFD2` |
  | x, h, ∂/∂x | âmbar `#FFC24D` |
  | y, k, ∂/∂y | magenta `#EA63FF` |
  | ponto P, X, H, δ | laranja `#E08A3C` |
  | ε | `#8CFFD2` |
  | rot | violeta `#9C8CFF` |
  | div | azul-claro `#7FB2FF` |
  | deformação | lima `#C6F26B` |
  | GEO | `#B8C4DA` |
  | carga | `#267BFF` |

  Operadores em branco.
- **Álgebra.** Caneta em toda fórmula (traço finíssimo, glifo a glifo, sem flash). Termo que nasce no desenho voa para a fórmula. Fórmulas ficam na tela enquanto a cena dura.
- **Proibido:** partículas, laços, lupa, brilho, contorno ou transparência em seta, sombra, barras e qualquer efeito fora do alvo.

### 3.2 Acréscimos da v2

1. **Cor ALERTA `#FF5D5D`**, só para "escapou" e "errou": a parte da mancha fora do disco ε, as partes do segmento fora do ε no B2-3 e as frases `ALGUMAS PONTAS ESCAPAM…` e `A PREVISÃO ERRA FEIO`. Área de alerta: `#FF5D5D` misturado 55 % com o fundo, opaco.
2. **Mancha:** a imagem do disco δ pela função original, F(P + r(cos θ, sen θ)) com r ≤ δ. Na prática, é um polígono fechado com a imagem da borda (360 pontos), preenchido com `#8CFFD2` misturado 80 % com o fundo (opaco) e contornado com `#8CFFD2` 2 px. Ela é recalculada quando δ muda.
3. **Ponto furado:** P vazado. Anel laranja de 3 px, raio 9 px, com o miolo da cor do fundo. É usado só enquanto o limite ignora o ponto (B1). No B3, P volta cheio.
4. **Faixas e células:** `#B8C4DA` misturado 90 % com o fundo; a interseção e as células destacadas, 78 %. Opacas.
5. **R6 · seta dentro do painel:** nenhuma seta, curva ou mancha passa da moldura do seu painel, em nenhum quadro. Verificação automática, quadro a quadro, nos blocos B1, B2-3, B3-1, B4, B5-2 e B5-4 → `setas_no_painel_v2.txt`, com zero esperado. É a regra que pega o E1.
6. **Tamanho mínimo:** legenda (SGM) ≥ 26 px e `MathTex` ≥ 30 px no 1080p. Fórmula dentro de legenda vira `MathTex` à parte.
7. **Contadores ao vivo** (só no B1-2): `‖X − P‖ = 0,52` (laranja) embaixo do painel esquerdo e `‖F(X) − L‖ = 1,18` (menta) embaixo do direito, com 2 casas decimais, atualizados por `DecimalNumber` com `ValueTracker` (o número muda, o rótulo não). Eles somem quando a definição entra.

## 4. Números (conferidos no script)

**Campo da aula F = (1 + sen x − sen y, 2 sen x + 2 − cos x − cos y)**, ponto P = (0, 0):
- F(P) = (1, 0); ∂F/∂x = (1, 2); ∂F/∂y = (−1, 0); J = [[1, −1], [2, 0]];
- rot 3, div 1, deformações 1 e 1.

**ε-δ (L = F(P) = (1, 0)):**
- maior δ = 0,4156 para ε = 1; 0,2116 para ε = 0,5; 0,1073 para ε = 0,25. Na tela: **0,41 · 0,21 · 0,10**.
- δ = 0,7 com ε = 1: 61 % da borda da mancha fica fora, e a distância máxima é 1,69.

**G:**
- 2xy/(x² + y²) = sen 2θ;
- num círculo de qualquer raio, a ponta varre [−1, 1];
- ∂G/∂x = (2y(y² − x²)/(x² + y²)², 0), que no eixo vertical vale 2/y; ∂G/∂x(0, 0) = 0⃗.

**Faixas:** |ΔP|, |ΔQ| ≤ ‖Δ‖ ≤ √2·max(|ΔP|, |ΔQ|).

**Malha ±0,4** em volta de P (no alvo 17, que usa ±0,5 e 200 px/u, a ideia é a mesma): a imagem fica a no máximo 0,18 u do paralelogramo.

**Zoom × 10:**
- o ponto (−1; 1) do palco é H = (−0,1; 0,1);
- F = (0,800; −0,190), resto = (−0,200; −0,190) ≈ J·H = (−0,2; −0,2).

**J·H:** H = (0,9; 0,6) → h·(1, 2) + k·(−1, 0) = (0,9; 1,8) + (−0,6; 0) = (0,3; 1,8).

**Arestas** (quadradinho com a quina em P):
- aresta horizontal: estica ∂P/∂x = 1 e gira ∂Q/∂x = 2;
- aresta vertical: estica ∂Q/∂y = 0 e gira −∂P/∂y = 1, isto é, tomba para a esquerda.

Então:
- rot = 2 + 1 = 3;
- div = 1 + 0 = 1;
- def₁ = 1 − 0 = 1;
- def₂ = 2 − 1 = 1, a taxa em que o ângulo reto fecha.

**Valores da v1, que continuam:**
- quocientes em x: (0,84; 2,14), (0,96; 2,16), (0,99; 2,09), (1,00; 2,05) → (1, 2);
- quocientes em y: (−0,84; 0,46), (−0,96; 0,25), (−0,99; 0,10), (−1,00; 0,05) → (−1, 0);
- curva da ponta em x: (1 + sen s, 2 sen s + 1 − cos s); em y, o círculo de centro (1, 1) e raio 1;
- fluxos: gancho (x eᵗ, y e⁻ᵗ), t = 0 → 0,55; modelo e^{tJ}, t = 0 → 0,35, área × 1,42; (y, x) com cosh/senh.

## 5. Os 11 erros da v1: correção obrigatória

- **E1 · seta do teto (1:33,8).**
  - No B1-2, X começa em **(0,45; 0,35)** (a 0,57 u de P), não em (1,4; 0,9).
  - Em toda a cena, |X − P| ≤ 0,6, e assim a ponta de F(X) fica em x ≤ 1,9 e y ≤ 1,4 no painel direito.
  - R6 obrigatória.
- **E2 · setas viram borrão (8:43).**
  - Seta nunca passa pela caneta. Entra com `GrowArrow` (0,6 s) e voa com `Transform` (em arco).
  - A caneta é só para `MathTex`/`Text`.
- **E3 · matriz numérica sobreposta (8:55).**
  - A matriz simbólica fica.
  - `=` e os parênteses do numérico entram com `Create`.
  - Cada número entra por `TransformFromCopy` do valor colorido já calculado (o `(1, 2)` âmbar e o `(−1, 0)` magenta da coluna do B4-4, que fica até lá) e cai no lugar certo da coluna.
  - Nenhum `TransformByGlyphMap` de matriz.
- **E4 · zoom com cortes (8:21).** Ver B6-1 a B6-3 (§6).
- **E5 · seta errada no início do passeio vertical (6:26).** O fantasma de F(P) é a mesma seta, com a cor trocada para GEO e a espessura para 3 px (`animate`). Nada é recriado.
- **E6 · ponto decimal.** Vírgula em todo número na tela: `1,44`, `1,42`, `0,41`.
- **E7 · resumo cortado.**
  - O S tem a duração da fala dele, mais 1,5 s parado no fim.
  - O CTA começa depois.
  - Confira no último quadro do S que as três linhas e as duas legendas estão completas (alvo 31).
- **E8 · gancho parado.** O mesmo fluxo de 0 a 0,55, em **~6 s** com `rate_func=linear`, de "deixa o fluido andar" até "Mas virou outra coisa".
- **E9 · fórmula sozinha no B3.** O B3 começa no layout B (alvo 08), sem tela vazia.
- **E10 · parados > 3 s.** Todo pedaço da definição tem gatilho (§6). `holds_v2.txt` lista cada trecho > 3 s com o motivo. Nenhum trecho > 6 s sem justificativa.
- **E11 · letras pequenas.** Mínimos do §3.2-6. Refazer `1ª COLUNA: ∂F/∂x · 2ª COLUNA: ∂F/∂y` (alvo 21) como `MathTex` à parte, a 30 px.

## 6. Cena a cena (v2)

Gatilho = palavra do Anexo A em que a ação começa. **Alvo NN** = quadro de `yt_0028_quadros_alvo_v2/` (tolerância ±20 px na posição, ±5 % no tamanho, mesmo texto e mesmas cores). Onde não houver mudança, vale a descrição da v1, que já está implementada.

### H · gancho (alvo 01)
Igual à v1, com E6 e E8.

### A · bem-vindos
Igual à v1.

### B1 · chegar perto (layout B; alvos 02, 03, 04 e 05)

- **B1-1** ("duas telas"): igual à v1, mas no painel da direita a seta-alvo se chama **L⃗**, `#8CFFD2`, 7 px, rotulada `L⃗` à esquerda e embaixo da origem comum (alvo 02). P aparece **vazado** (anel) desde o início.
- **B1-2** ("Conforme você chega perto"):
  - X sai de (0,45; 0,35) e anda **uma vez** em espiral até ~0,03 de P (~4 s).
  - À direita, F(X) acompanha, sempre dentro do painel (R6).
  - Os contadores do §3.2-7 entram em "Os dois números de baixo" e vão diminuindo juntos.
  - Eles saem em "Então a definição vira um desafio".
- **B1-3** ("alguém escolhe uma tolerância") · **alvo 02:**
  - O disco ε = 1 aparece em volta da ponta de L⃗ (`Create`, 1 s), e `∀ ε > 0` entra na caneta em y = 205.
  - Em "Depois é a sua vez", o disco δ cresce de 0 até 0,41 em volta de P (preenchimento laranja escuro opaco e contorno laranja 3 px), e `∃ δ > 0` entra ao lado.
  - Em "todas essas pontas juntas formam uma mancha", a mancha nasce **junto com o δ** (`ValueTracker` em δ, polígono recalculado) e entra a legenda `A MANCHA = TODAS AS PONTAS QUE SAEM DO DISCO δ`.
  - Um X de amostra (a 0,62·δ, ângulo 0,9) com a sua seta e o F(X) correspondente ficam na tela.
  - As duas metades da definição entram embaixo, na caneta, em "A pergunta é uma só": `X ∈ A, 0 < ‖X − P‖ < δ`, depois `⟹` e depois `‖F(X) − L‖ < ε`.
- **B1-4** ("Com delta igual a zero vírgula sete") · **alvo 03:**
  - δ sobe para 0,7 (1,2 s). A mancha cresce, e a parte fora do disco ε fica ALERTA.
  - Entra `ALGUMAS PONTAS ESCAPAM: δ GRANDE DEMAIS` (ALERTA, SGM 30). Embaixo à esquerda, `δ = 0,7`.
  - Em "Diminui o delta", δ desce **devagar** de 0,7 a 0,41 (~2,5 s), e a parte vermelha some exatamente quando a mancha passa a caber.
  - Em "Achou", a linha de baixo volta para as duas metades.
- **B1-5** ("Se o desafio aperta para meio"):
  - ε encolhe para 0,5 e δ para 0,21, juntos (1,5 s); depois ε para 0,25 e δ para 0,10.
  - A tabela ε | δ do alvo 04 vai sendo preenchida, linha a linha, no canto do painel direito.
- **B1-6** ("o próprio ponto fica de fora") · **alvo 04:**
  - O anel de P pulsa uma vez em escala (1 → 1,4 → 1; isso não é brilho) e entra `O PRÓPRIO P FICA DE FORA` (laranja, no alto do painel esquerdo, com clareira na fileira de cima).
  - Em "ponto de acumulação", não entra figura nova: só a fala.
  - Em "Agora sim, escrito", `lim F(X) = L ⇔ ∀ε > 0 ∃δ > 0 :` é escrita em y = 200, completando a definição com as duas metades de baixo.
  - Em "A metade da esquerda", a metade esquerda se destaca (`Indicate` de escala 1,08, sem cor nova) e depois a direita.
- **B1-7** ("E tem um atalho") · **alvo 05**, layout A:
  - O palco é o plano da chegada, ampliado em volta da ponta de L⃗ (170 px/u, ε = 1 u).
  - Entram o disco ε e o ponto `F(X)` dentro dele.
  - As sombras são duas setas finas a partir da ponta de L⃗: a horizontal âmbar e a vertical magenta, com linhas tracejadas até o ponto.
  - Em "o contrário também vale": as duas faixas, a interseção quadrada e o disco √2·ε tracejado.
  - Coluna, na caneta, uma linha por gatilho: as duas implicações e o `lim F = L ⇔ lim P = L₁ e lim Q = L₂`.
  - A legenda `CONTROLAR A SETA = CONTROLAR AS DUAS SOMBRAS` entra em "o limite de cada componente".

### B2 · quando o limite não existe (alvos 06 e 07)

- **B2-1/B2-2:** iguais à v1 (alvo 06: três caminhos, coluna com G, a reta y = m x e os três valores).
- **B2-3** ("E dá para ver isso de um jeito mais bonito") · **alvo 07**, layout B:
  - A conta polar entra no alto, na caneta: `2xy/(x² + y²) = 2r² cos θ sen θ / r² = sen 2θ`.
  - Embaixo à esquerda, `G = (sen 2θ, 0)`.
  - Em "dá uma volta num círculo minúsculo", X dá **uma** volta no círculo de raio 0,38 (laranja). A seta de X é proporcional (G é a exceção) e muda de tamanho e de sentido.
  - À direita, a ponta varre o segmento [−1, 1] (menta, 6 px), que vai sendo desenhado por onde a ponta passa, com os rótulos −1 e 1.
  - Em "Agora joga o desafio", entram o ponto `L ?` em 0,3 e o disco ε = 0,5. As partes do segmento fora do disco ficam ALERTA.
  - Entra a legenda de baixo.
  - Opcional, se couber no tempo: o L desliza de 0,3 até −0,3 e volta, e sempre sobra vermelho.
- **B2-4** ("E fica um cuidado"): sem figura nova; as fórmulas continuam.

### B3 · continuidade (alvos 08 e 09)

- **B3-1** ("Agora a continuidade") · **alvo 08**, layout B:
  - O mesmo desafio do B1 com δ = 0,41 e ε = 1. P agora é **cheio**, com a sua seta F(P) curta no painel esquerdo, e no direito o rótulo vira `L⃗ = F⃗(P)`.
  - Os três pedaços entram no alto, um por gatilho ("Um", "Dois", "Três"): `① P NO DOMÍNIO ✓`, `② O LIMITE EXISTE ✓`, `③ LIMITE = F(P) ✓` (SGM 30, `#8CFFD2`).
  - A definição entra embaixo em "Na figura" e a mancha em "No nosso campo, a mancha cabe".
- **B3-2** ("três jeitos de dar errado") · **alvo 09**, layout C:
  - Os cartões entram um por gatilho: "No campo elétrico", "No campo encrenqueiro" e "E neste aqui".
  - Títulos `① FORA DO DOMÍNIO`, `② SEM LIMITE`, `③ SALTO NO PONTO`.
  - No cartão ③, o campo (1, 0) tem clareira no centro, a seta do ponto é para cima (menta, 7 px) e o limite é uma seta GEO tracejada para a direita, rotulada `L⃗`.
  - A definição fica embaixo. `CONTÍNUA ⇔ CADA COMPONENTE É CONTÍNUA` entra em "por componentes".

### B4 · derivada parcial (alvos 10, 11, 12 e 13)

- **B4-1** · **alvo 10:** igual à v1, mais `ΔF = F(P + h) − F(P) (corda)` no alto do painel direito em "liga a ponta velha à ponta nova". A corda é desenhada **antes** do quociente. Em "Divide esse vetor", o quociente nasce como cópia da corda que **estica** (`Transform` da corda para a seta ΔF/h, ancorada na ponta de F(P)).
- **B4-2** ("a velocidade da ponta") · **alvo 11:**
  - À esquerda, P anda pela reta âmbar com uma seta âmbar de comprimento fixo `VELOCIDADE 1`, uma vez, por ~2 s.
  - À direita, a ponta percorre a curva (s de −0,3 a 1) e a tangente ∂F/∂x = (1, 2) fica na ponta de F(P).
  - Em "duas sombras", as setas finas (3 px, âmbar) horizontal 1 e vertical 2 saem da tangente, com os rótulos `∂P/∂x = 1` e `∂Q/∂x = 2`.
  - Embaixo, na caneta: `∂F/∂x = (∂P/∂x, ∂Q/∂x) = (1, 2)`.
- **B4-3** · **alvo 12:** igual à v1, com o **E5** corrigido.
- **B4-4** · **alvo 13:** igual à v1. Em "num campo no espaço", entra embaixo da coluna a legenda `NO ESPAÇO: TAMBÉM ∂F/∂z` (SGM 26, GEO).

### B5 · o engano (alvos 14, 15, 16 e 17)

- **B5-1** · **alvo 14:** igual à v1, **sem** as duas linhas de C¹ no fim (elas vão para o B5-3 e o B5-4).
- **B5-2** ("Se você confiasse só nelas") · **alvo 15**, layout B:
  - À esquerda, o G com o quadradinho de lado 0,9 em volta da origem (malha âmbar/magenta).
  - À direita, o anel GEO na origem com `PREVISÃO DAS PARCIAIS: UM PONTO`.
  - Em "Mas olha a imagem de verdade", o segmento [−1, 1] cresce a partir do centro para os dois lados (1,2 s) e entra `IMAGEM DE VERDADE: O SEGMENTO TODO`.
  - `A PREVISÃO ERRA FEIO` (ALERTA) entra em "errou feio".
- **B5-3** ("O que faltou?") · **alvo 16**, layout B com **gráficos**:
  - Eixos presos à grade, origem dos dois gráficos em (480, 540) e (1440, 540), 120 px/u, setas de eixo GEO 2 px, rótulo `y` em magenta.
  - Esquerda: a reta âmbar `∂P/∂x(0, y) = cos 0 = 1`.
  - Direita: os dois ramos de 2/y (âmbar, 4 px, cortados na moldura), o ponto laranja na origem com `vale 0 na origem` e `↑ ∞`/`↓ −∞`.
  - Cada curva é traçada da esquerda para a direita (`Create`, 1,5 s). Os títulos entram na caneta, em cima.
  - `CLASSE C¹: AS PARCIAIS EXISTEM E SÃO CONTÍNUAS` (SG 34) entra em "classe cê um" e `CLASSE Cʳ: O MESMO ATÉ A ORDEM r` em "cê erre".
- **B5-4** ("E com ela vem a promessa") · **alvo 17**, layout B com **200 px/u nos dois painéis**:
  - À esquerda, a malha 2×2 (linhas âmbar e magenta a −0,5, 0 e 0,5) em volta de P, com a célula de cima à direita em GEO.
  - À direita, a malha imagem: as linhas são levadas pela função original, com 60 pontos por linha, e entram uma família por vez, horizontais e depois verticais, por `Transform` de cópias das linhas da esquerda (elas voam e curvam). O ponto F(P) fica **sem a seta** (ela ficaria embaixo da ∂F/∂y).
  - Em "quase um paralelogramo", entram o paralelogramo tracejado branco e as setas h·∂F/∂x e k·∂F/∂y.
  - A fórmula da aproximação entra embaixo, em "Escrito".

### B6 · a tabela (alvos 18 a 24)

- **B6-1** ("chega dez vezes mais perto") · **alvo 18**, layout A:
  - O palco tem o campo da aula, com P e a **janela** de lado 0,6 em volta de P (branca, 3 px) e o rótulo `× 10`.
  - Em "essa janelinha vira o palco inteiro", a janela cresce até as bordas do palco (~2 s), e as setas são **reavaliadas continuamente** em P + (X, Y)/s, com s de 1 a 10 (`ValueTracker`; as setas são `VMobject`, e não há texto em updater).
  - A comprimida passa de mmax 3,5 para 6 junto com s.
  - Entra `ZOOM × 10`, e a janela some no fim.
- **B6-2** ("Cada uma é a seta do centro, mais um restinho") · **alvo 19:**
  - No ponto (−1; 1) do palco, aparecem em **tamanho × 2** (avisado na legenda): F(P) em GEO, o resto em menta 7 px e F(X) em menta 5 px.
  - Coluna: `F(X) = F(P) + (F(X) − F(P))` e as legendas.
- **B6-3** ("Tira a seta do centro") · **alvo 20** (o b62 da v1):
  - O triângulo some.
  - Todas as setas perdem a parte F(P) de uma vez, por um único `Transform` para o campo residual.
  - O resto igual à v1.
- **B6-4** ("coloca as duas lado a lado") · **alvo 21:**
  - A matriz simbólica é escrita na caneta.
  - Os números entram como no **E3**: cada valor voa da coluna do B4-4.
  - `MATRIZ JACOBIANA` (SG 40) e a legenda das colunas, como `MathTex` de 30 px.
- **B6-5** ("E ela funciona assim") · **alvo 22**, modelo linear em contexto:
  - H (laranja) cresce de P até (0,9; 0,6).
  - No ponto X, a seta h·(1, 2) (âmbar) cresce, depois k·(−1, 0) (magenta) a partir da ponta dela, e por fim J·H (menta), que fecha o triângulo.
  - Coluna, na caneta: `J(h, k) = h(1, 2) + k(−1, 0)`, depois `= (h − k, 2h)` por `TransformByGlyphMap`, as legendas coloridas e o exemplo numérico.
- **B6-6** · **alvo 23** e **B6-7** · **alvo 24:** iguais à v1.

### B7 · quatro números, quatro medidas (alvos 25 a 30)

- **B7-1** ("lendo cada número da tabela como um movimento de aresta") · **alvo 25:**
  - Os parênteses grandes entram, e as quatro células aparecem na ordem da fala: em cima à esquerda, embaixo à esquerda, em cima à direita, embaixo à direita.
  - Em cada célula:
    - o quadradinho de arestas âmbar (horizontal) e magenta (vertical), com os outros dois lados tracejados GEO;
    - a seta do movimento cresce (`GrowArrow`);
    - em seguida, a **aresta se move uma vez** na direção da seta e volta (0,8 s ida, 0,8 s volta). Isso não é laço, é um movimento só, com retorno.
  - A célula de baixo à direita mostra `PARADA`.
  - Os valores e as legendas entram na caneta.
  - À direita, a matriz numérica (52 px) e as quatro legendas.
- **B7-2** ("Agora junta") · **alvo 26:**
  - À esquerda, o quadradinho grande com as duas setas das quinas: (1, 2) âmbar e (−1, 0) magenta.
  - As quatro linhas entram uma por gatilho: "rotacional", "divergente", "primeira deformação", "a segunda".
  - Em "como uma tesoura", as duas arestas giram juntas por 0,15 rad cada, uma em direção à outra, e voltam. O ângulo reto fecha e abre uma vez.
  - A legenda `def₂: QUANTO O ÂNGULO RETO FECHA, COMO UMA TESOURA` entra junto.
- **B7-3** · **alvo 27** e **B7-4** · **alvo 28:** os três cartões e os valores, iguais à v1. Os cartões entram em "Quatro números entram", e os valores logo depois.
- **B7-5** · **alvo 29:** igual à v1, mais uma ação. Em "A aresta horizontal estica, a vertical encolhe", as duas setas das quinas (1, 0) âmbar e (0, −1) magenta aparecem por 2 s nas quinas do quadradinho fantasma, antes do retângulo final.
- **B7-6** · **alvo 30:** igual à v1, mais uma ação. Em "As duas arestas giram uma contra a outra", as setas das quinas (0, 1) âmbar e (1, 0) magenta aparecem por 2 s. `TAMBÉM VALE: (x² − y², −2xy)` passa de 34 para 36 px e fica ≥ 4 s.

### S · resumo e CTA · alvo 31

- Igual à v1: a matriz e as três linhas, uma por gatilho.
- Em "uma curiosidade", entram as duas legendas `NO ESPAÇO: 9 NÚMEROS` e `3 DE GIRO + 1 DE VOLUME + 5 DE DEFORMAÇÃO`.
- **E7:** o S termina inteiro, fica 1,5 s parado e só então entra o CTA padrão, em "No próximo vídeo".

## 7. Narração e tempo

O preview é silencioso, e cada bloco dura o tempo estimado da fala do Anexo A. A v1 rendeu ~0,37 s por palavra, já com as animações. Atualize o `duracoes_estimadas.json`.

| Bloco | Palavras | Duração estimada |
|---|---|---|
| H | 155 | ~1,0 min |
| A | 52 | ~0,35 min |
| B1 | 473 | ~2,9 min |
| B2 | 227 | ~1,4 min |
| B3 | 215 | ~1,35 min |
| B4 | 312 | ~1,95 min |
| B5 | 284 | ~1,75 min |
| B6 | 213 | ~1,3 min |
| B7 | 326 | ~2,0 min |
| S + CTA | 130 | ~0,8 min + CTA |
| **Total** | **2.387** | **≈ 14,5 min** |

Se passar de 15:00, avise no relatório e não corte nada: o corte é decisão do Kaio. **Não gerar voz.**

## 8. O que NÃO fazer

- Nenhum 3D, partícula, lupa, laço contínuo, brilho, contorno ou transparência em seta, sombra ou barra.
- Nenhum efeito fora dos alvos.
- Não usar `ThreeDScene`.
- Não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md` nem nas unidades yt_0026 e yt_0027.
- Não citar livro nem o Atlas na tela.
- Não gerar voz, SRT, master, 1080p nem entrega. Não fazer commit nem push.

## 9. QA do preview (obrigatório)

1. **Render × alvo (31):** um still no estado completo de cada alvo, comparado a 960×540 (tolerância de 10 px nessa escala), na prancha `comparacao_v2.jpg`.
2. **R5 · sobreposição**, em cada gatilho, medindo a seta inteira → `sobreposicoes_v2.txt`.
3. **R6 · setas no painel**, quadro a quadro, nos blocos do §3.2-5 → `setas_no_painel_v2.txt` (zero esperado).
4. **Flash por quadro = 0:** nenhuma fórmula aparece inteira antes da caneta.
5. **Parado:** `holds_v2.txt` com motivo para cada trecho > 3 s e nenhum > 6 s sem justificativa.
6. **Os 11 erros:** `erros_v1_v2.jpg` com o antes e o depois de cada um.
7. **Números:** confira na tela os valores do §4 (δ, tabela ε-δ, quocientes, J·H, arestas, vírgulas).

## 10. Parada

Entregue o preview, a prancha, os quatro relatórios (`sobreposicoes_v2.txt`, `setas_no_painel_v2.txt`, `holds_v2.txt` e o de entrega) e a prancha dos erros. Pare e não inicie voz nem 1080p.

---

## Anexo A · Narração canônica v2 (com tags do ElevenLabs v4)

Uma tag por trecho, em inglês, valendo até a próxima. Sem `[slowly]` e sem `[pause]`. Nenhuma letra solta. Épsilon, delta, cê um e cê erre são ditos pelo nome. ≈ 2.387 palavras.

### H · O quadradinho que deforma

[curious] Lembra do campo que fechou o episódio passado? A componente horizontal é a própria coordenada horizontal, e a vertical é menos a coordenada vertical. Coloca um quadradinho de fluido no meio e faz as contas que a gente já conhece. O rotacional dá zero, em todo ponto: nenhuma rodinha gira. O divergente também dá zero: nenhum pedacinho muda de área.

[thoughtful] Então, pelas duas medidas, não acontece nada. Só que agora deixa o fluido andar… e o quadradinho estica para os lados e achata na vertical. A área continua a mesma, e ele não girou nem um grau. Mas virou outra coisa.

[curious] Então tem alguma coisa nesse campo que o rotacional e o divergente não enxergam. Que número mede isso? E de onde ele sai? A resposta está nas derivadas parciais do campo. Só que, para usar essas derivadas com segurança, a gente precisa começar pelo chão: o que quer dizer chegar perto de um ponto.

### A · Bem-vindos

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab. Hoje são três ideias que se apoiam uma na outra: limite, continuidade e derivadas parciais de um campo vetorial. E, no fim, a gente vai juntar tudo numa tabela de quatro números que mostra, bem de perto, como o campo muda em volta de um ponto.

### B1 · Chegar perto

[thoughtful] Vamos usar duas telas. Na da esquerda está o campo, e é ali que você anda: tem um ponto fixo, e você vai se aproximando dele. Na da direita, eu trago cada seta para a mesma origem, para comparar só onde a ponta dela chega.

[curious] Conforme você chega perto do ponto, a ponta da seta vai chegando perto de uma seta-alvo. Essa seta-alvo é a candidata a limite. Os dois números de baixo contam a história: a distância até o ponto encolhe, e a distância da ponta até o alvo encolhe junto. Só que "encolhe junto" ainda é vago. Então a definição vira um desafio.

[thoughtful] Primeiro, alguém escolhe uma tolerância na chegada: um disquinho de raio épsilon em volta da ponta do alvo. Qualquer épsilon pode ser escolhido, por isso a definição começa com "para todo épsilon". Depois é a sua vez: você responde com um disquinho de raio delta em volta do ponto. E olha o que acontece do outro lado: cada ponto do seu disco manda a ponta da seta para algum lugar, e todas essas pontas juntas formam uma mancha. A pergunta é uma só: a mancha cabe no disco épsilon?

[curious] Com delta igual a zero vírgula sete, não cabe: um monte de pontas escapa. Diminui o delta… e a mancha encolhe junto. Em zero vírgula quatro um, ela fica inteira por dentro. Achou: é isso que "existe delta" quer dizer. Se o desafio aperta para meio, você aperta para zero vírgula dois um. Para um quarto, zero vírgula um zero. O delta depende do épsilon, e o limite existe quando você sempre consegue responder.

[thoughtful] E tem um detalhe no seu disco: o próprio ponto fica de fora. É o "maior que zero" da definição. O limite só olha para quem está chegando, nunca para o que acontece em cima do ponto. Aliás, o ponto nem precisa estar no domínio: basta ter pontos do domínio tão perto dele quanto você quiser. O nome disso é ponto de acumulação. Agora sim, escrito: a seta-alvo é o limite quando, para todo épsilon positivo, existe um delta positivo tal que, para todo ponto do domínio a uma distância maior que zero e menor que delta, a seta fica a menos de épsilon do alvo. A metade da esquerda fala de onde você anda. A da direita, de onde a seta chega.

[curious] E tem um atalho. Se a ponta está no disco épsilon, as duas sombras dela, a horizontal e a vertical, ficam a menos de épsilon das sombras do alvo. E o contrário também vale: se as duas sombras estão perto, a ponta cai num quadrado, que cabe num disco só um pouquinho maior. Então o limite de um campo existe exatamente quando o limite de cada componente existe, e aí é o limite de funções de várias variáveis que você já conhece.

### B2 · Quando o limite não existe

[curious] Agora um campo encrenqueiro. Todas as setas são horizontais. Nos eixos, não tem seta nenhuma; nas diagonais, as setas têm tamanho um: numa delas apontam para a direita, na outra, para a esquerda.

[thoughtful] Vem andando até a origem pelo eixo horizontal: a seta é zero o caminho todo. Pela diagonal de subida: um, para a direita. Pela outra: um, para a esquerda. Numa reta qualquer pela origem, o campo vale o dobro da inclinação, dividido por um mais a inclinação ao quadrado. Muda a reta, muda o valor.

[curious] E dá para ver isso de um jeito mais bonito. Em coordenadas polares, a componente horizontal vira o seno do dobro do ângulo. O campo não depende da distância, só da direção. Então dá uma volta num círculo minúsculo em volta da origem: a ponta da seta varre o segmento inteiro, de menos um até um. E isso acontece em qualquer círculo, por menor que seja.

[thoughtful, emphatic] Agora joga o desafio. Escolhe um alvo qualquer e um épsilon de meio. O disco tem largura um, e o segmento tem largura dois: não cabe, seja qual for o alvo. Então não existe limite na origem. E fica um cuidado: dois caminhos com valores diferentes provam que o limite não existe. Mas todas as retas darem o mesmo valor ainda não provam que ele existe, porque dá para chegar por uma curva.

### B3 · Continuidade

[thoughtful] Agora a continuidade. A definição tem três pedaços, e cada um pode falhar. Um: o ponto está no domínio, então a seta do ponto existe. Dois: o limite ali existe. Três: o limite é igual à própria seta do ponto. Na figura, é o mesmo desafio de antes, só que agora o disco épsilon fica em volta da ponta da seta do próprio ponto. No nosso campo, a mancha cabe. Contínuo.

[curious] Agora, três jeitos de dar errado. No campo elétrico de uma carga, o ponto da carga nem está no domínio. Falha o primeiro pedaço, e a pergunta nem se faz; em todo o resto, ele é contínuo. No campo encrenqueiro, definido como zero na origem, a seta existe, mas o limite não: falha o segundo. E neste aqui todas as setas apontam para a direita, menos a do centro, que aponta para cima. O limite existe e é a seta para a direita, mas a seta do ponto é outra. Falha o terceiro: um salto bem em cima do ponto.

[thoughtful] E, de novo, por componentes: o campo é contínuo exatamente quando cada componente é contínua. Por isso quase todo campo que vem de fórmula é contínuo onde está definido: somas, produtos, quocientes com denominador diferente de zero e composições de funções contínuas continuam contínuas.

### B4 · Derivada parcial de um campo

[thoughtful] Agora sim: medir como a seta muda. Fica no ponto e anda só na horizontal, um passo. A seta muda de uma para outra, e a diferença entre as duas é um vetor, que liga a ponta velha à ponta nova. Divide esse vetor pelo tamanho do passo e encolhe o passo. Esse limite é a derivada parcial do campo na direção horizontal.

[curious] Com passo um, o quociente vale zero vírgula oito quatro e dois vírgula um quatro. Com meio, zero vírgula nove seis e dois vírgula um seis. Com passo cada vez menor, ele vai chegando em um e dois. E olha a tela da chegada: andando na horizontal, a ponta da seta desenha uma curva. A diferença é uma corda dessa curva, e, dividida pelo passo, ela vira a seta tangente. Então a derivada parcial é a velocidade da ponta, quando você anda na horizontal com velocidade um.

[thoughtful] E essa velocidade tem duas sombras. A horizontal diz quanto muda a componente horizontal do campo: um. A vertical diz quanto muda a componente vertical: dois. Por isso a conta é por componentes: a derivada do campo é a derivada de cada componente.

[curious] Agora na vertical. Andando para cima, a ponta anda num círculo, e o quociente vai chegando em menos um e zero: a derivada na direção vertical aponta para a esquerda, tangente ao círculo.

[thoughtful, emphatic] Então a derivada parcial de um campo não é um número: é um vetor, que diz como a seta muda quando você anda numa direção. Na conta, a derivada na horizontal dá cosseno e dois cossenos mais seno, da coordenada horizontal; no ponto, um e dois. A derivada na vertical dá menos cosseno e seno da coordenada vertical; no ponto, menos um e zero. A conta bate com o desenho. E, num campo no espaço, aparece uma terceira, na direção da profundidade, com a mesma ideia.

### B5 · O engano

[curious] Só que tem uma armadilha. Volta no campo encrenqueiro e calcula as derivadas parciais na origem. Pelo eixo horizontal, a seta é zero o tempo todo: derivada zero. Pelo vertical, mesma coisa. As duas existem, e as duas são zero.

[thoughtful] Se você confiasse só nelas, ia prever que, perto da origem, tudo vai para perto do zero: um quadradinho em volta da origem iria parar num ponto só. Mas olha a imagem de verdade: a ponta varre o segmento inteiro, de menos um até um. A previsão errou feio. As parciais só olham duas retas, e esse campo esconde tudo nas diagonais. Ele nem é contínuo na origem.

[thoughtful, emphatic] O que faltou? Olha as próprias derivadas, andando pelo eixo vertical. No nosso campo, a derivada na horizontal vale um o caminho todo, sem salto nenhum. No encrenqueiro, ela vale dois dividido pela altura: explode perto da origem, e na origem vale zero. Essa é a condição de classe cê um: as derivadas parciais existem e são contínuas. Classe cê erre é o mesmo, até as derivadas de ordem erre.

[curious] E com ela vem a promessa. Pega uma malhinha em volta do ponto e manda para a tela da chegada. As linhas horizontais viram curvas na direção da derivada horizontal, e as verticais, curvas na direção da derivada vertical. Cada quadradinho da malha vira quase um paralelogramo, com lados de passo vezes derivada. Escrito: a seta num ponto vizinho é a seta do ponto, mais o passo horizontal vezes a derivada na horizontal, mais o passo vertical vezes a derivada na vertical, com um erro que some mais rápido que o passo. O nosso campo, feito de senos e cossenos, é cê um. O encrenqueiro, não.

### B6 · A tabela

[curious] Então vamos usar isso. Pega o campo da aula e chega dez vezes mais perto do ponto: essa janelinha vira o palco inteiro. De perto, todas as setas ficam parecidas com a seta do centro. Cada uma é a seta do centro, mais um restinho. Tira a seta do centro de todas… e sobra só a mudança. Olha que campo arrumadinho.

[thoughtful] Bem de perto, essa mudança é escrita com as duas derivadas. Então coloca as duas lado a lado, como colunas: a derivada na horizontal na primeira, a derivada na vertical na segunda. Fica uma tabela de quatro números, com as derivadas das duas componentes nas duas direções. Ela tem nome: matriz jacobiana. No nosso ponto, um e menos um em cima, dois e zero embaixo.

[curious] E ela funciona assim: um passo com uma parte horizontal e uma vertical vira a parte horizontal vezes a primeira coluna, mais a parte vertical vezes a segunda. A seta do modelo é a soma das duas.

[thoughtful] Agora coloca um quadradinho com a quina no ponto. A quina da direita é empurrada pela primeira coluna; a de cima, pela segunda. Cada coluna empurra uma aresta. Solta o fluido no modelo… e o quadradinho gira, cresce e entorta, tudo ao mesmo tempo. Tudo isso estava nos quatro números.

### B7 · Quatro números, quatro medidas

[thoughtful] E dá para separar essa bagunça, lendo cada número da tabela como um movimento de aresta. Em cima, à esquerda: quanto a aresta horizontal estica. Aqui, um. Embaixo, à esquerda: quanto ela gira. Dois. Em cima, à direita: quanto a aresta vertical tomba para o lado. Menos um, para a esquerda. Embaixo, à direita: quanto ela estica. Zero.

[curious] Agora junta. Os dois giros no mesmo sentido, somados, dão o rotacional: dois mais um, três. Os dois estiramentos somados dão o divergente: um mais zero, um. E sobram duas comparações. Estiramento horizontal menos vertical: um. Essa é a primeira deformação, quanto o pedacinho estica mais numa direção do que na outra. E a diferença entre os dois giros: dois menos um, um. Essa é a segunda, quanto o ângulo reto do quadradinho fecha, como uma tesoura.

[thoughtful, emphatic] Quatro números entram, quatro medidas saem, e nada se perde no caminho. Bem de perto e sem a seta do centro, todo campo cê um se comporta como uma mistura de quatro campos simples: um redemoinho, uma explosão e duas deformações. E isso não é só matemática: num fluido, o atrito viscoso vem da deformação. Um bloco de fluido girando inteiro, rígido, não tem atrito viscoso nenhum por dentro.

[curious] Agora volta lá no começo. No campo que esticava o quadradinho, a tabela é um e zero em cima, zero e menos um embaixo. A aresta horizontal estica, a vertical encolhe na mesma medida, e ninguém gira. Rotacional zero, divergente zero, e a primeira deformação vale dois. É tudo deformação.

[happy] E lá no episódio passado ficou um desafio: achar outro campo, que não fosse constante, com rotacional e divergente zero. Um deles é este, que troca as coordenadas de lugar. As duas arestas giram uma contra a outra: a segunda deformação vale dois, e o quadradinho vira losango. É o mesmo campo de antes, girado quarenta e cinco graus. E quem achou um de segundo grau, como o da tela, também acertou.

### S · Síntese e encerramento

[thoughtful] Resumindo: limite é ganhar o desafio do épsilon com um delta. Continuidade é o limite igual à seta do ponto, sem salto. A derivada parcial é a velocidade da ponta numa direção. E, quando essas derivadas são contínuas, a tabela delas descreve o campo bem perto do ponto: giro, área e deformação. E uma curiosidade: no espaço, a tabela tem nove números, que se separam em três de giro, um de volume e cinco de deformação.

[excited] No próximo vídeo, a gente coloca o módulo inteiro para trabalhar em exercícios: campo vetorial, rotacional, divergente, limite e derivadas parciais, tudo junto. Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual dessas quatro medidas você acha que aparece mais na física? Até a próxima!
