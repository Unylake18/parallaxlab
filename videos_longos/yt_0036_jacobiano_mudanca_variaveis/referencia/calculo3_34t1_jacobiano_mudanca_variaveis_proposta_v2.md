# Longo · Jacobiano e mudança de variáveis (Cálculo III · 3.4-T1) · proposta v2

2026-11-14 · thread "Planejar jacobiano e mudança de variáveis" · **proposta v2** = v1 + o refino do GPT filtrado (o §8 diz o que entrou e o que não entrou). Substitui a v1. A matemática não mudou (o GPT conferiu as mesmas contas); mudaram a abertura (o 1/2 vira pergunta e só é explicado no B3-3), a leitura do fator 5, a escala do vetor da cena 3D, o porquê de cada hipótese e algumas frases de ponte.

Fases cobertas: questão → solução → verificação → roteiro → storyboard. A narração completa, com tela e gatilhos por âncora, está no Anexo A; a leitura dos símbolos, no Anexo B. A matemática foi conferida em `pautas/verificacao/verifica_calc3_34t1_sympy.py`: **41 checagens, todas `True`** (saída em `verifica_calc3_34t1_saida.txt`). Quadros-alvo principais em `pautas/calculo3_34t1_quadros_alvo_v1/` (os alvos 01 e 10 foram refeitos para a v2; folha de contato `00_folha_contato_v2.jpg`).

Este vídeo vem logo depois dos exercícios integradores (EP. 10, yt_0035) e **cumpre o gancho dele**. A narração v3 do EP. 10 termina assim: "a integral de é elevado a xis mais ípsilon sobre xis menos ípsilon, neste trapézio. Em pé, trava. Deitado, trava também. Mas, se você trocar as próprias variáveis, usando a soma xis mais ípsilon e a diferença xis menos ípsilon como coordenadas novas, a conta sai em três linhas. Só que aparece um meio na frente, que ninguém chamou. De onde vem esse meio?" O cartão era `NO PRÓXIMO VÍDEO: MUDANÇA DE VARIÁVEIS` / `DE ONDE VEM ESSE 1/2?`. O vídeo cumpre as três promessas:
1. **O trapézio trava nas duas ordens** → H1 mostra as duas fatias e a placa `TRAVA` (a primitiva pede a integral exponencial, Ei, que não é elementar: checagem T13).
2. **Com u = x + y e v = x − y a conta sai em poucas linhas** → B6 faz a conta inteira, do jacobiano ao número (3/4)(e − 1/e) ≈ 1,763.
3. **De onde vem o 1/2** → o H1 só mostra o contraste (3 células da grade nova, área 3/2 no papel) e deixa a pergunta "cada célula vale meio quadradinho?"; o B3-3 responde pelo determinante, e o B6-4 confere com a área do trapézio.

**Divisão do módulo 3.4 (combinada com a thread do 3.4-T2 em 2026-11-14):** este vídeo fica com o §4.1 do Guidorizzi (o jacobiano como fator local de área) e o **teorema de mudança de variáveis** do §4.2, com as hipóteses e a justificativa pela soma de Riemann, e com os exemplos que não são polares. O 3.4-T2 faz o caso polar inteiro (o retângulo polar e o jacobiano r, que é o exemplo do §4.1 do livro, limites em polares, a integral de Gauss). Aqui não se calcula o jacobiano polar nem se resolve nada em polares: as polares aparecem só no cartão do gancho. **A série usa r e θ nas polares** (ρ é densidade desde o EP. 05).

Segue o sistema visual da série: fundo violeta liso `#18143A → #0F0C26` com a grade `papel(ax)` nascendo dos eixos, álgebra no modo caneta (glifo a glifo, traço finíssimo), termo com origem no desenho voando do desenho, cada passo algébrico por `TransformByGlyphMap`, fórmula-mãe antes do número, regra CONTA INTEIRA (§3.1), nenhuma partícula, nenhum brilho, nenhuma sombra. Manim é o padrão; Three.js só onde a câmera trabalha (uma cena, decisão 5).

## 0. Identificação

| Campo | Valor |
|---|---|
| Unidade | `yt_0036` (provisório: no C:\ a pasta `videos_longos/` vai até o `yt_0034`; o yt_0035 está em produção. Conferir no PC que o yt_0036 está livre) · `longo_horizontal` · `teoria_visual` |
| Mapa (divisão v2 e Atlas) | Cálculo III · **3.4 Mudança de variáveis na integral dupla** · **3.4-T1 Jacobiano e mudança de variáveis** (8–15 min), "Preliminares: Jacobiano". O seguinte é o **3.4-T2 Coordenadas polares**, que vira o gancho |
| Referência | Guidorizzi, *Um Curso de Cálculo*, vol. 3, 6ª ed., **cap. 4**: **§4.1 Preliminares** (retângulo A → B = φ(A); comprimento de arco ds = ‖γ′(t)‖ dt e Δs ≅ ‖γ′(t)‖ Δt; arcos MN e MQ pelas derivadas parciais; área de B ≅ ‖∂φ/∂u ∧ ∂φ/∂v‖ Δu Δv; o determinante com i, j, k; definição de ∂(x, y)/∂(u, v); "fator de ampliação (ou contração) local de área"); **§4.2** (a soma de Riemann ① → ② → ③, o **Teorema de mudança de variáveis na integral dupla** com as hipóteses, o quadro-receita e o **Exemplo 1**, trapézio 1 ≤ x + y ≤ 2 com cos(x − y)/sen(x + y) = 1). Conferido nas págs. 142–154 do PDF do projeto. Didática do Stewart (seção de mudança de variáveis em integrais múltiplas): a grade de u, v desenhada no plano xy, a transformação (u² − v², 2uv) do quadrado unitário na região entre parábolas, o trapézio de vértices (1, 0), (2, 0), (0, −2), (0, −1) com e^((x+y)/(x−y)), e a dica de escolher u e v pelo integrando e pelas bordas. *Não abri o PDF do Stewart: o Kaio liberou `docs\livros`, mas o PDF (~1,08 GB) passa do limite de cópia, e ele escolheu seguir sem; os exemplos são os clássicos da seção e foram todos refeitos e conferidos no SymPy* |
| Série pública | CÁLCULO III · **EP. 11** (provisório) |
| Tag do canto | linha 1 `CÁLCULO III · MUDANÇA DE VARIÁVEIS`; linha 2 = título da cena |
| Pergunta narrativa | O trapézio do desafio trava nas duas ordens. Trocando as próprias variáveis, ele sai em poucas linhas, mas com um 1/2 na frente. De onde vem esse 1/2? |
| Pergunta central | Quando se troca (x, y) por (u, v), quanto muda cada pedacinho de área, e como isso entra na integral dupla? |
| Pré-requisitos | Cálculo I (substituição, ∫ f(g(t)) g′(t) dt; comprimento de arco); vetores (área do paralelogramo = ‖w₁ ∧ w₂‖); **EP. 03** (derivadas parciais, C¹, matriz jacobiana: cada coluna leva um lado do quadradinho; div = soma dos estiramentos); EP. 05 (soma de Riemann); EP. 06 (conteúdo nulo); EP. 08 e 09 (Fubini, regiões gerais, ler a região pelos limites, entrada azul-claro e saída coral) |
| Duração | narração do Anexo A: **3.614 palavras** (sem tags) ≈ **20:17** com as pausas entre âncoras (decisão 2; a v1 tinha 3.394 ≈ 19:03; o §5 corta para ≈ 19:05) |
| `solido_3d:` | nenhum do arsenal Blender, porque a única peça 3D é o produto vetorial em pé sobre um paralelogramo, feito direto em Three.js |
| `3d_threejs:` | 1 cena (decisão 5): **o produto vetorial em pé**: o paralelogramo das setas ∂φ/∂u Δu e ∂φ/∂v Δv no chão (plano xy), o vetor (∂φ/∂u Δu) ∧ (∂φ/∂v Δv) subindo na direção k com altura = área do paralelogramo (as setas e o vetor na MESMA escala: o vetor é dos deslocamentos, não das derivadas sozinhas, senão a altura seria o fator e não a área); câmera oblíqua parada, um pouso lento para a vista de cima, que vira o 2D do B4-2 no mesmo quadro |

**Cobre:** a troca de variável do Cálculo I como régua esticada (dx = g′(t) dt) e o fator de comprimento de uma curva (Δs ≅ ‖γ′(t)‖ Δt); a transformação φ de classe C¹ e a imagem de um retângulo; o caso linear (o quadrado vira paralelogramo, área = |ad − bc| pela figura e pela álgebra; colunas = matriz jacobiana do EP. 03; mesmo fator em toda a grade); o sinal do determinante como orientação e o porquê do módulo; o caso não linear (a grade curva, o fator que muda de ponto para ponto, a célula que de perto vira paralelogramo, o produto vetorial e o determinante com i, j, k, a definição do jacobiano ∂(x, y)/∂(u, v)); a tabela que mostra |J| Δu Δv acertando cada vez mais; a soma de Riemann que leva à fórmula; **o teorema com as hipóteses**, cada uma com figura, e o contraexemplo da dobra; a conferência da área 8/3 da região entre parábolas sem jacobiano (fatiando deitado); **o trapézio do gancho do começo ao número**; o Exemplo 1 do Guidorizzi como "pause e tente" (o sinal do jacobiano muda quando u e v trocam de papel, o módulo não); aplicações (mapa de Mercator e fluidos).

**Fora:** coordenadas polares (o 3.4-T2; aqui só o cartão do gancho); massa e centro de massa (3.4-T3); a demonstração completa do teorema (o Guidorizzi também não faz: "enunciaremos sem demonstração"); mudança de variáveis na integral tripla (§5.5); a regra do jacobiano da inversa em geral (aparece só como conferência no trapézio, ∂(u, v)/∂(x, y) = −2, sem enunciar o teorema da função inversa).

## 1. Ideia central (uma só)

**Trocar as variáveis troca a grade do papel. Cada célula da grade nova, de lados Δu e Δv, ocupa no papel uma área de mais ou menos |∂(x, y)/∂(u, v)| Δu Δv. Por isso, na integral, dx dy vira |J| du dv: o jacobiano é o fator local de área.**

Frases de tela que resumem o vídeo: `JACOBIANO = FATOR LOCAL DE ÁREA` e `dx dy = |J| du dv`.

**Fio condutor:** a célula da grade. Na régua do Cálculo I ela é um segmento que estica (fator 2); no caso linear ela vira paralelogramo e todas esticam igual (fator 5); no caso curvo cada uma estica de um jeito (fator 4u² + 4v²), mas de perto vira paralelogramo; no trapézio cada uma encolhe pela metade (fator 1/2). A imagem que volta é **a grade de u, v desenhada por cima do papel de x, y**, com uma célula acesa no estilo do quadradinho do EP. 03 (chapa `#663A4C`, malha `#FFB3BC`).

**Regra da série (Kaio, 2026-11-11):** cada definição ou enunciado formal vem com uma figura própria, e o símbolo nasce do desenho.

| # | Enunciado formal (Guidorizzi cap. 4) | Figura que o acompanha | Bloco |
|---|---|---|---|
| D1 | Cálculo I: x = g(t) ⇒ Δx ≅ g′(t) Δt; ∫₀² x dx = ∫₀¹ (2t) · 2 dt | Duas réguas paralelas: a de t (laranja, 0 a 1) em cima e a de x (âmbar, 0 a 2) embaixo; um segmento Δt acende e as duas pontas descem por linhas finas até a régua de x, onde o segmento fica com o dobro do comprimento; rótulo `Δx = 2 Δt` | B1-1 |
| D2 | Δs ≅ ‖γ′(t)‖ Δt (§4.1) | A curva γ (branca) com o arco de γ(t) a γ(t + Δt) aceso em lima; a seta γ′(t) Δt (branca) tangente em γ(t), quase cobrindo o arco; Δt encolhe (um movimento) e a seta gruda no arco | B1-2 |
| D3 | φ: Ω ⊂ ℝ² → ℝ², (x, y) = φ(u, v), C¹; A retângulo, B = φ(A) = {φ(u, v) : (u, v) ∈ A} | Layout B (dois planos): à esquerda o plano u, v (eixos laranja u e verde-água v) com o retângulo A no estilo quadradinho (chapa + malha 4 × 4), lados `Δu` e `Δv`; seta curva `φ` por cima; à direita o plano x, y com B, quadrilátero curvo com cantos M, N, P, Q; as retas `u₀ CONSTANTE`, `v₀ CONSTANTE` viram curvas com o mesmo rótulo | B2-1 |
| D4 | Linear φ(u, v) = (2u + v, u + 3v): o quadrado unitário vira o paralelogramo das colunas (2, 1) e (1, 3) | Layout B: o quadrado à esquerda; à direita a grade inteira inclinada (linhas laranja e verde-água) e o paralelogramo aceso; os lados viram setas `(2, 1)` (laranja) e `(1, 3)` (verde-água) que **voam** para as colunas da matriz `[[2, 1], [1, 3]]` na coluna de fórmulas | B3-1 |
| D5 | Área = (a + b)(c + d) − ac − bd − 2bc = ad − bc = det; numa célula Δu × Δv a imagem tem área 5 Δu Δv | O paralelogramo dentro da caixa 3 × 4 (traço GEO); os seis pedaços que sobram acendem e saem um por vez, cada um com a sua área a caneta (`2·1/2`, `1·3/2`, `1·1`); a conta `12 − 2 − 3 − 2 = 5`; depois, a mesma figura com letras e a álgebra por glyph map até `ad − bc` | B3-1, B3-2 |
| D6 | Sinal do determinante = orientação; área = módulo | O quadrado com uma seta circular anti-horária (u depois v); a imagem (losango de vértices (0, 0), (1/2, 1/2), (1, 0), (1/2, −1/2)) com a seta horária; selo `VIROU DE COSTAS`; `det = −1/2` → `ÁREA = |−1/2| = 1/2` | B3-3 |
| D7 | Não linear φ(u, v) = (u² − v², 2uv) em [0, 1]² | Layout B: a malha 4 × 4 do quadrado à esquerda; à direita a grade curva (parábolas), as células coloridas pelo tamanho (as de perto da origem pequenas, as perto de φ(1, 1) = (0, 2) grandes); rótulos das bordas `x = 1 − y²/4` (u = 1) e `x = y²/4 − 1` (v = 1) | B4-1 |
| D8 | Arco MN ≅ ‖∂φ/∂u‖ Δu; arco MQ ≅ ‖∂φ/∂v‖ Δv; área de B ≅ ‖∂φ/∂u ∧ ∂φ/∂v‖ Δu Δv | Zoom na célula de canto M = φ(0,75; 0,5) = (0,3125; 0,75): o quadrilátero curvo MNPQ, as setas `∂φ/∂u Δu` (laranja) e `∂φ/∂v Δv` (verde-água) saindo de M e o paralelogramo tracejado que elas formam; depois a cena Three.js: o paralelogramo no chão e o vetor `(∂φ/∂u Δu) ∧ (∂φ/∂v Δv)` em pé, com altura = área do paralelogramo (lima); a álgebra tira `Δu Δv` para fora e sobra `‖∂φ/∂u ∧ ∂φ/∂v‖`, o fator | B4-2 |
| D9 | (∂φ/∂u) ∧ (∂φ/∂v) = det[i j k; x_u y_u 0; x_v y_v 0] = (x_u y_v − x_v y_u) k; ∂(x, y)/∂(u, v) = det[x_u x_v; y_u y_v] | Coluna de fórmulas: o determinante 3 × 3 a caneta; a terceira coluna (zeros) acende e o desenvolvimento pela coluna do k sobra o 2 × 2; a transposta por glyph map (linha vira coluna); moldura lima na definição | B4-3 |
| D10 | J = 4u² + 4v²; |J(M)| = 3,25; razão área exata ÷ |J(M)| Δu Δv → 1 | As quatro derivadas voam das fórmulas de x e y para a matriz; a célula de M com Δ = 0,25 → 0,1 → 0,05 → 0,01 (zoom acompanhando), e uma tabela de três colunas `Δ · EXATA · |J| ΔuΔv` com a razão `1,44 · 1,16 · 1,08 · 1,02` | B4-3 |
| D11 | ∬_B f ≅ Σ f(x̄ᵢ, ȳⱼ) α(Bᵢⱼ) ≅ Σ f(φ(ūᵢ, v̄ⱼ)) |J(ūᵢ, v̄ⱼ)| Δuᵢ Δvⱼ → ∬_{B_uv} f(φ(u, v)) |J| du dv (①, ②, ③ do livro) | Layout B: partição de B_uv em Rᵢⱼ à esquerda; à direita as imagens Bᵢⱼ; um ponto branco (ūᵢ, v̄ⱼ) e a sua imagem (x̄ᵢ, ȳⱼ) ligados pela seta φ; coluna com a cadeia ① → ② → ③, cada termo voando do desenho (α(Bᵢⱼ) da célula da direita; Δuᵢ Δvⱼ da célula da esquerda) | B5-1 |
| D12 | Teorema (§4.2): φ C¹ no aberto Ω; B_uv ⊂ Ω compacto, fronteira de conteúdo nulo; B = φ(B_uv); φ(B̊_uv) = B̊; φ inversível em B̊_uv; ∂(x, y)/∂(u, v) ≠ 0 em B̊_uv; f integrável em B ⇒ ∬_B f dx dy = ∬_{B_uv} f(φ(u, v)) |∂(x, y)/∂(u, v)| du dv | Enunciado a caneta, uma hipótese por linha; ao lado, uma miniatura por hipótese que acende no gatilho: (1) a região dentro de um aberto Ω tracejado; (2) a fronteira de B_uv acendendo fina com `CONTEÚDO NULO`; (3) o miolo levado no miolo (interior GEO, borda branca); (4) a dobra em ALERTA (D13); (5) a célula que não colapsa; quadro-receita do livro embaixo | B5-2 |
| D13 | Contraexemplo: φ(u, v) = (u², v) em [−1, 1] × [0, 1]: ∬ |J| = ∫∫ 2|u| = 2, mas a área da imagem [0, 1]² é 1; J = 2u zera em u = 0 | O retângulo [−1, 1] × [0, 1] à esquerda, metade esquerda laranja-claro, direita verde-água-claro; à direita as duas metades caem uma sobre a outra no quadrado [0, 1]² (a esquerda **dobra** por cima, um movimento); `∬|J| = 2` × `ÁREA = 1` em ALERTA; a linha u = 0 acende com `J = 0` | B5-3 |
| D14 | Área da região entre parábolas: ∬ 4(u² + v²) du dv = 8/3 = ∫₀² (2 − y²/2) dy | Layout B com a região curva à direita; coluna com as duas contas inteiras; à direita, a tira deitada entra na parábola azul-claro e sai na coral, `COMPRIMENTO = SAÍDA − ENTRADA`; `8/3 = 8/3 ✓` | B5-4 |
| D15 | Trapézio: u = x + y, v = x − y; x = (u + v)/2, y = (u − v)/2; J = −1/2; B_uv = {1 ≤ v ≤ 2, −v ≤ u ≤ v} | Layout B: o trapézio no papel com a grade inclinada (retas x + y = k laranja, x − y = m verde-água, passo 1) e uma célula acesa (lado 1/√2, área 1/2); os quatro lados acendem um por um com a equação e **voam** para o plano u, v, onde viram `u = v` (coral, saída), `v = 2`, `u = −v` (azul-claro, entrada), `v = 1`; os quatro cantos com as coordenadas | B6-1, B6-2 |
| D16 | ∫₁² ∫_{−v}^{v} e^{u/v} · (1/2) du dv = (3/4)(e − 1/e) | O plano u, v com a tira deitada (fatia em u, vê congelado), entrada azul-claro em u = −v, saída coral em u = v; a coluna inteira por glyph maps (§3.1, C10–C16) | B6-3 |
| D17 | Conferência f = 1: 3 · 1/2 = 3/2 = 2 − 1/2 | As 3 células da grade nova acendem no trapézio de u, v (área 3); no papel, o trapézio grande (triângulo 2 · 2/2) menos o pequeno (1 · 1/2), `3/2`; `1/2 = O JACOBIANO` | B6-4 |
| D18 | Guidorizzi Ex. 1: u = x − y, v = x + y; J = +1/2; ∬ cos(x − y)/sen(x + y) = 1 | O trapézio 1 ≤ x + y ≤ 2 no primeiro quadrante; `PAUSE E TENTE`; depois a mesma escada (bordas → v = 1, v = 2, v = u, v = −u; J = +1/2 com a nota `SINAL TROCOU, MÓDULO NÃO`) | B7 |
| D19 | Mercator: fator de área sec²(latitude); fluido: d/dt det(I + tJ) em t = 0 = traço = div | Dois cartões de traço GEO: (1) uma grade de latitude e longitude em Mercator, as células crescendo para o norte, `× sec² (LATITUDE)`, uma célula em 72° com `≈ × 10`; (2) o quadradinho do EP. 03 escoando com `ÁREA × (1 + t · div F + …)` | B8 |

**Payoff:** no S1, os quatro ✓: `RÉGUA: dx = g′(t) dt` · `LINEAR: ÁREA × |ad − bc|` · `CURVA: ÁREA ≅ |J| ΔuΔv` · `TRAPÉZIO: (3/4)(e − 1/e)`.

**Hook (≈ 1:31):** o trapézio do desafio, as duas fatias com `TRAVA`; o expoente e as bordas acendem nas partes `x + y` e `x − y`; a grade inclinada nasce por cima do papel; o trapézio se endireita no plano u, v (um movimento); `1/2 ·` aparece na frente da integral com `?`; a grade conta: 3 células de u, v, mas área 3/2 no papel; a célula inclinada acende com `ÁREA ?` e a pergunta "de onde sai esse meio?" fica aberta até o B3-3.

## 2. Estrutura

| Bloco | Âncoras | Voz | Layout | Conteúdo | Figuras |
|---|---|---:|---|---|---|
| H | H1–H2 | 1:31 | B | O trapézio que trava, a grade nova, o 1/2 como pergunta; a tese | D15 (prévia) |
| A | A1 | 0:20 | padrão | Bem-vindos; `A RÉGUA · O PARALELOGRAMO · O FATOR LOCAL · O TEOREMA · O TRAPÉZIO` | — |
| B1 | B1-1 a B1-2 | 1:41 | A | **A régua esticada.** Substituição do Cálculo I, fator de comprimento de uma curva | D1, D2 |
| B2 | B2-1 | 0:50 | B | **A transformação.** φ, o retângulo A e a imagem B | D3 |
| B3 | B3-1 a B3-3 | 2:21 | B + A | **O paralelogramo.** Caso linear, a área pela figura, o determinante, o sinal | D4–D6 |
| B4 | B4-1 a B4-3 | 3:12 | B + 3D → A | **O fator local.** A grade curva, a célula vira paralelogramo, o produto vetorial, o jacobiano | D7–D10 |
| B5 | B5-1 a B5-4 | 3:49 | B + A | **O teorema.** A soma de Riemann, o enunciado com as hipóteses, a dobra, a conferência 8/3 | D11–D14 |
| B6 | B6-1 a B6-4 | 3:29 | B + A | **O trapézio.** Escolher u, v, o jacobiano, a região nova, a conta, a conferência | D15–D17 |
| B7 | B7 | 1:07 | A | **Pause e tente** (Ex. 1 do livro) | D18 |
| B8 | B8 | 0:41 | cartões | **No mundo.** Mercator e fluidos | D19 |
| S | S1–S2 | 1:15 | A + cartão | Síntese; gancho para coordenadas polares; CTA | — |

Tempo por âncora no Anexo A. Soma ≈ 20:17 (0,15 s + palavras/3 + 0,35 s por âncora, como nos EP. 05 a 10, com os 3 palavras/s medidos pelo Kaio). A cena estica para seguir a voz (WAV contínuo).

## 3. Matemática conferida

Script: `pautas/verificacao/verifica_calc3_34t1_sympy.py` (sympy 1.14 + numpy + scipy). As 41 linhas dão `True`.

| # | Afirmação usada no vídeo | Checagem |
|---|---|---|
| L1–L2 | ∫₀² x dx = 2; com x = 2t, ∫₀¹ (2t) · 2 dt = 2 | ✓ |
| P1 | (a + b)(c + d) − ac − bd − 2bc = ad − bc | ✓ |
| P2–P4 | (a, c, 0) ∧ (b, d, 0) = (0, 0, ad − bc); o det 3 × 3 com i, j, k dá (ad − bc) k; det da transposta = det | ✓ |
| P5–P6 | φ(u, v) = (2u + v, u + 3v): det = 2 · 3 − 1 · 1 = 5; pela figura 3 · 4 − 2 − 3 − 2 = 5 | ✓ |
| T0–T1 | u = x + y, v = x − y ⇔ x = (u + v)/2, y = (u − v)/2; J = (1/2)(−1/2) − (1/2)(1/2) = **−1/2** | ✓ |
| T2 | ∂(u, v)/∂(x, y) = 1 · (−1) − 1 · 1 = −2; (−2)(−1/2) = 1 | ✓ |
| T3–T4 | Grade inclinada: célula de lado 1/√2, área 1/2; o quadrado unitário de u, v vai no losango (0, 0), (1/2, 1/2), (1, 0), (1/2, −1/2) com área orientada −1/2 (sentido horário) | ✓ |
| T5–T6 | Cantos (1, 0), (2, 0), (0, −2), (0, −1) → (1, 1), (2, 2), (−2, 2), (−1, 1); lados y = 0 → u = v, x − y = 2 → v = 2, x = 0 → u = −v, x − y = 1 → v = 1 | ✓ |
| T7–T8 | ∫_{−v}^{v} e^{u/v} du = v(e − 1/e); d/du (v e^{u/v}) = e^{u/v} | ✓ |
| T9–T10 | ∫₁² v dv = 3/2; total = (1/2)(e − 1/e)(3/2) = **(3/4)(e − 1/e) ≈ 1,762802** | ✓ |
| T11 | Numérica no plano x, y (dblquad, fatiando deitado em duas faixas): 1,762802 | ✓ |
| T12 | f = 1: área no plano u, v = ∫₁² 2v dv = 3; no papel 3 · 1/2 = 3/2 = 2 − 1/2 | ✓ |
| T13–T14 | (x + y)/(x − y) = −1 + 2x/(x − y) = 1 + 2y/(x − y); com t = x − y a fatia pede ∫ e^{a/t} dt = t e^{a/t} − a Ei(a/t): **não elementar nas duas ordens** | ✓ |
| G1–G4 | Ex. 1 do Guidorizzi: u = x − y, v = x + y, J = **+1/2**; ∫_{−v}^{v} cos u / sen v du = 2; (1/2) ∫₁² 2 dv = **1**; numérica igual | ✓ |
| N1–N2 | φ(u, v) = (u² − v², 2uv): J = (2u)(2u) − (−2v)(2v) = **4u² + 4v²**; bordas u = 1 → x = 1 − y²/4, v = 1 → x = y²/4 − 1 | ✓ |
| N3–N4 | Área = ∫₀¹∫₀¹ 4(u² + v²) du dv = **8/3**; deitado ∫₀² (2 − y²/2) dy = 4 − 4/3 = **8/3** | ✓ |
| N5–N6 | J(0, 0) = 0; J(1, 1) = 8; J(0,75; 0,5) = 4(0,5625 + 0,25) = **3,25** | ✓ |
| N7 | Área exata da célula pela fronteira (fórmula do cadarço, sem usar J) = ∬ J na célula | ✓ |
| — | Célula de canto M = (0,75; 0,5): Δ = 0,25 → exata 0,2917 × 0,2031 (razão 1,44); Δ = 0,1 → 0,03777 × 0,03250 (1,16); Δ = 0,05 → 0,008767 × 0,008125 (1,08); Δ = 0,01 → 0,000330 × 0,000325 (1,02) | impresso |
| N8 | (reserva) ∬ y dA = 2 nas duas formas | ✓ |
| H1–H2 | Dobra φ(u, v) = (u², v) em [−1, 1] × [0, 1]: ∬ |J| = 2 ≠ 1 = área; ∬ J (sem módulo) = 0 | ✓ |
| D1 | d/dt det(I + tJ) em t = 0 = a + d = traço = div | ✓ |
| M1–M2 | Mercator: y = ln(sec φ + tg φ), dy/dφ = sec φ; fator de área sec² φ; sec²(72°) ≈ 10,47 | ✓ |
| Z1 | Gancho do 3.4-T2: ∬_{x²+y²≤1} e^{−(x²+y²)} dA = π(1 − 1/e) ≈ 1,9859 (numérica) | ✓ |

### 3.1 CONTA INTEIRA (o texto exato da coluna, linha a linha)

Cada linha entra a caneta ou por glyph map a partir da anterior; nenhum número aparece sem a linha que o produz. A narração lê cada degrau (Anexo A). Cor: x âmbar, y magenta, u laranja, v verde-água, |J| lima, f ciano, entrada azul-claro, saída coral, operadores brancos.

**C1 · régua (B1-1)**
1. `∫₀² x dx = [x²/2]₀² = 2²/2 − 0²/2 = 2`
2. `x = 2t ⇒ dx = 2 dt` · `x = 0 ⇒ t = 0` · `x = 2 ⇒ t = 1`
3. `∫₀² x dx = ∫₀¹ (2t) · 2 dt = 4 ∫₀¹ t dt = 4 [t²/2]₀¹ = 4 · (1/2 − 0) = 2 ✓`

**C2 · área do paralelogramo pela figura (B3-1)**
1. `CAIXA: (2 + 1)(1 + 3) = 3 · 4 = 12`
2. `− 2 · (2 · 1)/2 = − 2` (dois triângulos de catetos 2 e 1)
3. `− 2 · (1 · 3)/2 = − 3` (dois triângulos de catetos 1 e 3)
4. `− 2 · (1 · 1) = − 2` (dois retangulinhos 1 × 1)
5. `ÁREA = 12 − 2 − 3 − 2 = 5`

**C3 · a mesma conta com letras (B3-2)**
1. `ÁREA = (a + b)(c + d) − 2 · ac/2 − 2 · bd/2 − 2 · bc`
2. `= ac + ad + bc + bd − ac − bd − 2bc` (o produto aberto; `ac` e `−ac` acendem juntos e somem; `bd` e `−bd` idem)
3. `= ad + bc − 2bc = ad − bc`
4. `= det [a b; c d]` (a matriz com as colunas (a, c) e (b, d), voando das setas) · `2 · 3 − 1 · 1 = 5 ✓`

**C4 · o sinal (B3-3)**
1. `x = (u + v)/2, y = (u − v)/2` → colunas `(1/2, 1/2)` e `(1/2, −1/2)`
2. `det = (1/2)(−1/2) − (1/2)(1/2) = −1/4 − 1/4 = −1/2`
3. `ÁREA = |−1/2| = 1/2`

**C5 · as derivadas e o jacobiano do caso curvo (B4-3)**
1. `x = u² − v², y = 2uv`
2. `∂x/∂u = 2u` · `∂x/∂v = −2v` · `∂y/∂u = 2v` · `∂y/∂v = 2u` (cada uma voa para a casa da matriz)
3. `∂(x, y)/∂(u, v) = det [2u −2v; 2v 2u] = (2u)(2u) − (−2v)(2v) = 4u² + 4v²`
4. `EM M = (0,75; 0,5): 4 · 0,5625 + 4 · 0,25 = 2,25 + 1 = 3,25`

**C6 · produto vetorial → jacobiano (B4-2/B4-3, Guidorizzi)**
1. `∂φ/∂u ∧ ∂φ/∂v = det [i j k; x_u y_u 0; x_v y_v 0]`
2. `= (x_u y_v − x_v y_u) k` (os termos com i e j têm um zero: acendem e somem)
3. `= det [x_u x_v; y_u y_v] k` (transposta por glyph map: linha vira coluna, o det não muda)
4. `‖∂φ/∂u ∧ ∂φ/∂v‖ = |∂(x, y)/∂(u, v)|` (moldura lima)

**C7 · soma de Riemann → fórmula (B5-1)**
1. `∬_B f dx dy ≅ Σᵢ Σⱼ f(x̄ᵢ, ȳⱼ) α(Bᵢⱼ)` ①
2. `α(Bᵢⱼ) ≅ |J(ūᵢ, v̄ⱼ)| Δuᵢ Δvⱼ` · `(x̄ᵢ, ȳⱼ) = φ(ūᵢ, v̄ⱼ)`
3. `≅ Σᵢ Σⱼ f(φ(ūᵢ, v̄ⱼ)) |J(ūᵢ, v̄ⱼ)| Δuᵢ Δvⱼ` ②
4. `→ ∬_{B_uv} f(φ(u, v)) |∂(x, y)/∂(u, v)| du dv` ③

**C8 · área 8/3 com jacobiano (B5-4)**
1. `ÁREA = ∬_{[0,1]²} (4u² + 4v²) du dv`
2. `∫₀¹ (4u² + 4v²) du = [4u³/3 + 4v² u]₀¹ = 4/3 + 4v²`
3. `∫₀¹ (4/3 + 4v²) dv = [4v/3 + 4v³/3]₀¹ = 4/3 + 4/3 = 8/3`

**C9 · área 8/3 sem jacobiano, deitado (B5-4)**
1. `u = 1: x = 1 − v², y = 2v ⇒ v = y/2 ⇒ x = 1 − y²/4` (SAÍDA, coral)
2. `v = 1: x = u² − 1, y = 2u ⇒ u = y/2 ⇒ x = y²/4 − 1` (ENTRADA, azul-claro)
3. `COMPRIMENTO = (1 − y²/4) − (y²/4 − 1) = 2 − y²/2`
4. `∫₀² (2 − y²/2) dy = [2y − y³/6]₀² = 4 − 8/6 = 4 − 4/3 = 8/3 ✓`

**C10 · trapézio: variáveis e inversa (B6-1)**
1. `u = x + y` · `v = x − y`
2. `u + v = 2x ⇒ x = (u + v)/2` · `u − v = 2y ⇒ y = (u − v)/2`

**C11 · trapézio: jacobiano (B6-1)**
1. `∂x/∂u = 1/2` · `∂x/∂v = 1/2` · `∂y/∂u = 1/2` · `∂y/∂v = −1/2`
2. `∂(x, y)/∂(u, v) = (1/2)(−1/2) − (1/2)(1/2) = −1/4 − 1/4 = −1/2`
3. `|J| = 1/2` · conferência: `∂(u, v)/∂(x, y) = 1 · (−1) − 1 · 1 = −2` · `(−2) · (−1/2) = 1`

**C12 · trapézio: a região nova (B6-2)**
1. `y = 0: u = x, v = x ⇒ u = v` · `x − y = 2 ⇒ v = 2` · `x = 0: u = y, v = −y ⇒ u = −v` · `x − y = 1 ⇒ v = 1`
2. `(1, 0) → (1, 1)` · `(2, 0) → (2, 2)` · `(0, −2) → (−2, 2)` · `(0, −1) → (−1, 1)`
3. `B_uv: 1 ≤ v ≤ 2, −v ≤ u ≤ v`

**C13 · trapézio: a integral montada (B6-3)**
1. `∬_B e^{(x+y)/(x−y)} dx dy = ∫₁² ∫_{−v}^{v} e^{u/v} · (1/2) du dv` (o `u` e o `v` do expoente voam de C10; o `1/2` voa de C11; os limites voam do plano u, v)

**C14 · trapézio: a de dentro (B6-3)**
1. `PRIMITIVA EM u: v e^{u/v}` · `CONFERE: d/du (v e^{u/v}) = v · (1/v) e^{u/v} = e^{u/v} ✓`
2. `∫_{−v}^{v} e^{u/v} du = [v e^{u/v}]_{u=−v}^{u=v} = v e^{v/v} − v e^{−v/v}`
3. `= v e − v e^{−1} = v (e − 1/e)`

**C15 · trapézio: a de fora (B6-3)**
1. `(1/2) ∫₁² v (e − 1/e) dv = (1/2)(e − 1/e) ∫₁² v dv`
2. `∫₁² v dv = [v²/2]₁² = 4/2 − 1/2 = 3/2`
3. `= (1/2)(e − 1/e)(3/2) = (3/4)(e − 1/e) ≈ 1,763`

**C16 · trapézio: conferência f = 1 (B6-4)**
1. `PLANO u, v: ∫₁² (v − (−v)) dv = ∫₁² 2v dv = [v²]₁² = 4 − 1 = 3`
2. `× |J| = 3 · 1/2 = 3/2`
3. `PAPEL: 2 · 2/2 − 1 · 1/2 = 2 − 1/2 = 3/2 ✓`

**C17 · Ex. 1 do livro (B7)**
1. `u = x − y, v = x + y ⇒ x = (u + v)/2, y = (v − u)/2`
2. `J = (1/2)(1/2) − (1/2)(−1/2) = 1/4 + 1/4 = 1/2`
3. `x + y = 1 ⇒ v = 1` · `x + y = 2 ⇒ v = 2` · `y = 0 ⇒ v = u` · `x = 0 ⇒ v = −u` · `B_uv: 1 ≤ v ≤ 2, −v ≤ u ≤ v`
4. `∫_{−v}^{v} (cos u)/(sen v) du = (1/sen v) [sen u]_{−v}^{v} = (sen v − sen(−v))/sen v = 2 sen v / sen v = 2`
5. `(1/2) ∫₁² 2 dv = (1/2) · 2 · (2 − 1) = 1`

**Pontos de rigor que a fala respeita:**
- **A justificativa do B5-1 é a do livro, e é heurística.** O Guidorizzi escreve "é razoável esperar" e enuncia o teorema "sem demonstração". A fala diz "o livro enuncia sem demonstrar, porque a prova completa é longa" e não chama a cadeia de prova.
- **Fator 5 (B3-2):** a fala diz que toda célula tem a área **multiplicada** por cinco (área da imagem = 5 Δu Δv), não que toda célula tem área cinco.
- **Comprimento com sinal (B1-1):** Δx ≅ g′(t) Δt é deslocamento com sinal; o fator de comprimento é |g′(t)|. Com g′ = 2 não há diferença; a fala avisa numa frase, e isso prepara o sinal do determinante.
- **Hipóteses (B5-2):** são condições **suficientes** deste enunciado, não necessárias para toda mudança de variáveis; a fala diz o papel de cada uma (tabela do §3.2).
- **A dobra (B5-3):** quem conta a área duas vezes é a **sobreposição**; o J = 0 em u = 0 é a segunda hipótese violada, não a causa do 2.
- **"Fator local":** a fala nunca diz que a célula **é** um paralelogramo; diz "de perto, quase", e a tabela do B4-3 mostra a razão indo para 1 (1,44 → 1,02). O canto M é o do livro (u₀, v₀); com o centro da célula a aproximação seria melhor, mas o vídeo segue o livro.
- **Sinal:** o determinante pode ser negativo; a área é o módulo. O B3-3 explica o sinal como orientação (o quadrado "virou de costas") e o B7 mostra que trocar quem é u e quem é v troca o sinal e mantém o módulo.
- **Hipóteses (B5-2):** a fala lê todas, na ordem do livro, e diz que na **borda** o teorema permite que φ não seja injetora e que o jacobiano zere (só o interior é exigido). Não promete nada sobre polares além de "isso vai fazer diferença no próximo vídeo".
- **A dobra (B5-3)** viola duas hipóteses ao mesmo tempo (não inversível no interior e J = 0 em u = 0, ponto interior). A fala aponta as duas.
- **Trapézio (B6):** o teorema pede x, y em função de u, v (φ vai do plano u, v para o x, y); por isso a fala isola x e y antes do jacobiano. A conferência pelo ∂(u, v)/∂(x, y) = −2 é só conferência ("ida dobra, volta divide por dois"), sem enunciar a regra geral da inversa.
- **"Trava" (H1):** a fala diz "a primitiva não se escreve com as funções do Cálculo um", como no EP. 09 (não cita Ei nem Liouville).
- **Mercator (B8):** com a Terra tomada como esfera (a fala diz isso), o fator de área do mapa em relação ao globo é sec²(latitude) (checagem M1). "A Groenlândia parece do tamanho da África, que é umas catorze vezes maior": áreas 2,17 e 30,4 milhões de km² (dado de geografia geral, sem número na tela além de `≈ × 10`).
- **Fluidos (B8):** d/dt det(I + tJ) em t = 0 = traço = div (checagem D1). Para t pequeno, det(I + t DF) = 1 + t div F + O(t²); a fala diz "um, mais tê vezes o divergente, mais termos menores" e "a taxa com que o fator **começa** a mudar", nada além disso.

### 3.2 O papel de cada hipótese (para a fala do B5-2)

| Hipótese | Papel na explicação | Miniatura |
|---|---|---|
| φ de classe C¹ no aberto Ω | as derivadas são contínuas: de perto a célula é quase o paralelogramo das derivadas, com erro controlado | 1 |
| B_uv compacto, fronteira de conteúdo nulo | a região é integrável (EP. 06): a borda não pesa na soma | 2 |
| B = φ(B_uv), φ(B̊_uv) = B̊ | as duas regiões se correspondem: o miolo vai no miolo | 3 |
| φ inversível no interior | nenhum pedaço é contado duas vezes (a dobra do B5-3) | 4 |
| J ≠ 0 no interior | nenhuma célula de dentro colapsa num segmento ou ponto | 5 |
| f integrável em B | a integral do lado de x, y existe | — |

## 4. Direção visual

### 4.1 Layouts

- **A · palco + fórmulas:** palco à esquerda, coluna de fórmulas à direita (x = 1120), como nos EP. 05 a 10.
- **B · dois planos (novo para este módulo, herdeiro do layout de dois painéis do EP. 03):** plano u, v à esquerda (painel 640 × 640, origem num nó da grade), plano x, y à direita (mesmo tamanho), a seta curva `φ` por cima entre os dois; a coluna de fórmulas vai para uma faixa embaixo (y ≥ 820) ou o layout volta para A quando a conta cresce. Cada painel com o seu `papel(ax)`; escalas próprias por painel (`papel(ax, area=...)`).
- **3D (Three.js):** só no B4-2 (decisão 5). Câmera oblíqua parada, o vetor sobe, um pouso lento para a vista de cima, que vira o 2D do zoom no mesmo quadro (alinhamento ≤ 2 px pelo `timeline.json`). O B4-2 tem que funcionar só com o 2D (o 3D é a entrada).

### 4.2 Cores (decisão 4)

| Elemento | Cor | Situação |
|---|---|---|
| f, integrando | ciano `#35D9FF` | como nos EP. 05 a 10 |
| x | âmbar `#FFC24D` | cor de x da série (mantida pelo Kaio) |
| y | magenta `#EA63FF` | cor de y da série |
| **u**, retas u constante, ∂φ/∂u | **laranja `#FF9440`** | nova (a thread do 3.4-T2 usa a mesma para r) |
| **v**, retas v constante, ∂φ/∂v | **verde-água `#2EE6A6`** | nova (no 3.4-T2, θ) |
| **\|J\|**, fator de área, o vetor ∧ | **lima `#C6F26B`** | a cor da deformação do EP. 03 (no 3.4-T2, o r que vem do jacobiano) |
| Célula da grade (A, Rᵢⱼ, o quadradinho) | chapa `#663A4C` + malha `#FFB3BC` | o quadradinho aprovado no EP. 03 |
| Curva de entrada / de saída da fatia | azul-claro `#7FB2FF` / coral `#FF7A8A` | do EP. 09 |
| Região B, caixas, cartões | GEO `#B8C4DA` | da série |
| Dobra, determinante negativo | ALERTA `#FF5D5D` | da série |
| Pontos de amostra (ūᵢ, v̄ⱼ), (x̄ᵢ, ȳⱼ) | branco | não usar o laranja `#E08A3C` do EP. 05 (brigaria com o u) |

Operadores (∫, ∬, ∧, ≅, ⇒, det, | |) em branco. Nas derivadas parciais, o numerador na cor da função (x âmbar, y magenta) e o denominador na cor da variável (u laranja, v verde-água). O `1/2` do trapézio é lima desde o H1 (era branco no cartão do EP. 10; aqui ganha a cor do jacobiano quando a fala diz "jacobiano").

### 4.3 Bloco a bloco (o essencial; o storyboard completo vai no handoff)

- **H:** layout B direto: o trapézio no papel com as duas tiras e as placas `TRAVA`; o expoente na coluna, `x + y` e `x − y` acendem; as bordas `x − y = 1` e `x − y = 2` acendem; a grade inclinada nasce (retas laranja e verde-água, uma família por vez); o trapézio **voa** para o plano u, v e se endireita; `1/2 ·` lima com `?`; as 3 células do trapézio de u, v contadas (`ÁREA 3`); no papel `ÁREA 3/2`; uma célula inclinada acende com `ÁREA ?` (a resposta fica para o B3-3). H2: as duas linhas da tese.
- **B1:** layout A sem palco de gráfico: as duas réguas; a coluna C1; depois a curva γ com a seta tangente.
- **B2:** layout B com o quadradinho do EP. 03 à esquerda e o quadrilátero curvo à direita (a transformação do B4, para a figura já ser a de verdade). Ordem: primeiro um ponto vai pela seta φ, depois um segmento (o lado Δu vira curva), por último a célula inteira; três movimentos curtos.
- **B3:** layout B com a grade inteira se inclinando (um movimento: a grade de u, v é transformada pelo `apply_matrix`); as setas voam para a matriz; a caixa 3 × 4 e os seis pedaços saindo; a álgebra em A; o sinal com a seta circular.
- **B4:** layout B com a malha 4 × 4 curvando (um `ApplyPointwiseFunction`); as células coloridas pelo tamanho (escala de cinza GEO → lima); zoom na célula de M; a cena Three.js; a coluna C5–C6 em A; a tabela do Δ.
- **B5:** layout B com a partição e a cadeia ①②③; o enunciado em A com miniaturas; a dobra em B; a conferência 8/3 em A com a região curva no palco.
- **B6:** layout B do trapézio (o mesmo do H), agora com a escada inteira; a conta em A com o plano u, v no palco.
- **B7:** layout A, o trapézio do livro, `PAUSE E TENTE` por 3 s, a escada C17 em ritmo mais rápido (cada linha ainda a caneta).
- **B8:** dois cartões de traço GEO, sem foto e sem efeito.
- **S:** S1 com `dx dy = |J| du dv` grande e os quatro ✓. S2: o disco x² + y² ≤ 1 com `∬ e^{−(x²+y²)} dA` e as duas placas `TRAVA`; a grade quadrada some e nasce a grade de círculos e raios (laranja e verde-água: r e θ); uma célula do anel acende com `ÁREA ≅ ? · Δr Δθ`; cartão `NO PRÓXIMO VÍDEO: COORDENADAS POLARES` / `QUAL É O FATOR DA GRADE DE CÍRCULOS?` no gatilho falado e por pelo menos 8 s; depois o CTA padrão.

## 5. Reserva e corte

- **Para cortar (só se o WAV passar muito de 19 min), nesta ordem:** (1) o B8 encurta (Mercator ou fluidos, um só; −0:20); (2) o B7 perde as frases repetidas, mantendo J = +1/2 e o módulo (−0:20); (3) o B4-3 perde uma linha da tabela (−0:08); (4) pequenas retomadas no B1 e no B5 (−0:20). Economia ≈ 1:10. **Não cortar:** a conta inteira do trapézio, o sinal do determinante, o zoom local do B4, as hipóteses do teorema e a conferência 8/3 (dois métodos diferentes chegando no mesmo número).
- **Reserva (não entra na v1):** ∬ y dA = 2 na região entre parábolas (Stewart), nas duas formas (checagem N8); a região entre as hipérboles xy = 1, xy = 2 e as retas y = x, y = 2x com u = xy, v = y/x (bom para o 3.4-E1, conferir antes de usar); transformação linear da elipse em círculo (vai para o 3.4-T2 como polares elípticas, a combinar com aquela thread).

## 6. Decisões (recomendo todas; o Kaio decide)

1. **Número:** `yt_0036` · CÁLCULO III · **EP. 11**. Conferir no PC que o yt_0036 está livre. Recomendo.
2. **Duração ≈ 20:17** (a v1 tinha 19:03; o refino somou ≈ 1:15 em frases de ponte e no papel das hipóteses). O Atlas diz 8–15; os EP. 05 a 09 ficaram entre 17 e 22 min. O §5 corta ≈ 1 min se precisar. Recomendo manter, porque este vídeo carrega o §4.1 inteiro **e** o teorema do §4.2 (a divisão combinada com o 3.4-T2), e a regra CONTA INTEIRA alonga o trapézio.
3. **Divisão com o 3.4-T2** (já combinada entre as threads): o teorema formal fica aqui; o exemplo polar do §4.1 do livro, o jacobiano r e todas as contas em polares ficam no T2; polares com **r e θ** (ρ é densidade na série). Recomendo.
4. **Cores novas:** u laranja `#FF9440`, v verde-água `#2EE6A6`, |J| lima `#C6F26B` (deformação do EP. 03), célula no estilo do quadradinho do EP. 03. O T2 já adotou as mesmas para r, θ e o r do jacobiano. Veja nos quadros-alvo 04, 07 e 12. Se alguma incomodar, a troca vale para os dois vídeos.
5. **3D: uma cena Three.js** (o produto vetorial em pé, a área virando altura) no B4-2, porque é o único lugar onde a câmera mostra algo que o 2D não mostra (o k saindo do plano). Alternativa: nenhuma cena 3D, com o vetor ∧ desenhado em perspectiva 2D. Recomendo a cena.
6. **Exemplo curvo = (u² − v², 2uv) do Stewart** (região entre parábolas), porque dá a grade mais clara do "fator que muda" (0 na origem, 8 no canto) e se confere sem jacobiano fatiando deitado (o método do EP. 09). Alternativa: as hipérboles com u = xy, v = y/x. Recomendo o do Stewart.
7. **Ex. 1 do Guidorizzi como "pause e tente" (B7)**: mostra que o sinal do jacobiano depende de quem é u e quem é v, e que o método vale para outro integrando. Recomendo manter (o GPT também).
8. **Gancho para o 3.4-T2** (combinado com aquela thread): o disco unitário com ∬ e^{−(x²+y²)} dA, que trava nas duas ordens; a grade de círculos e raios; "qual é o fator dessa grade?". O T2 abre por aí e chega em π(1 − 1/e), que conversa com o (1 − 1/e)/2 do sino do EP. 09. Recomendo.

## 7. Observações

- A fala usa "no vídeo passado" para o EP. 10 (exercícios integradores, onde ficou o desafio), "quando a gente estudou derivadas parciais" para o EP. 03 (matriz jacobiana, quadradinho, div), "quando a gente estudou conteúdo nulo" para o EP. 06, "no vídeo das regiões gerais" para o EP. 09 e "quando a gente construiu a integral dupla" para o EP. 05. A série sai em sequência; nenhum vídeo futuro é citado além do gancho padrão "no próximo vídeo".
- Letras para a voz: "u", "vê" (v), "fi" (φ), "ômega" (Ω), "bê u vê" (B_uv), "erre í jota" (Rᵢⱼ), "bê í jota" (Bᵢⱼ), "u barra", "vê barra", "gama" e "gama linha" (γ, γ′), "delta u", "delta vê", "cá" (k), "jota" (j). O jacobiano é lido "o jacobiano de xis, ípsilon em relação a u, vê"; o símbolo ∂ não é lido sozinho. Se o ElevenLabs ler "u" como conjunção, o teste de voz decide se escreve "ú".
- O EP. 03 chamou a matriz de "matriz jacobiana"; aqui o **determinante** dela é "o jacobiano". A fala faz a ponte uma vez (B3-1, B4-3) e depois diz só "o jacobiano".
- `docs/mapa_curricular.md` no repositório ainda usa a numeração antiga; a ficha leva `modulo: 3.4` com a nota, como nos EP. 02–10.
- **Quadros-alvo v1** (`pautas/calculo3_34t1_quadros_alvo_v1/`, 16 + folha de contato `00_folha_contato_v1.jpg`; gerador `sb36.html` + `shot.js`): 01 H1 grade nova e o 1/2 contado · 02 H2 tese · 03 A1 · 04 B1-1 régua · 05 B2-1 transformação · 06 B3-1 paralelogramo na caixa · 07 B3-3 sinal · 08 B4-1 grade curva · 09 B4-2 zoom · 10 B4-2 produto vetorial dos deslocamentos (esboço do 3D, v2) · 11 B4-3 jacobiano e tabela · 12 B5-2 teorema · 13 B5-3 dobra · 14 B6-2 região nova · 15 B6-3 conta · 16 S2 gancho polar. São de referência (canvas + KaTeX). O 10 é o PNG da cena Three.js de referência `c3d36.html` (`?k=obl`; `?k=topo` dá a vista de cima, igual ao alvo 09) com os rótulos do Manim. Handoff de preview: `pautas/yt_0036_handoff_v1.md` + `yt0036_handoff_v1_completo.zip`.

## 8. Filtro do refino do GPT (o que entrou na v2)

O Kaio pediu para usar o refino "se for somar". O GPT conferiu as mesmas contas e não achou erro de matemática; o refino é de forma e de fala. Ficou só o que acrescenta clareza ou rigor sem trocar a estrutura.

**Entrou**

| # | Onde | O que mudou | Por que soma |
|---|---|---|---|
| G1 | H1 | O 1/2 vira pergunta: 3 células da grade nova, mas área 3/2 no papel; a célula acende com `ÁREA ?`. "É elevado à fração…" na fala. | O gancho fica com mistério; a explicação só vem no B3-3, onde há determinante para sustentar. |
| G2 | B1-1 | Δx tem sinal; o fator de comprimento é \|g′\|. | Prepara o sinal do determinante (B3-3) numa frase. |
| G3 | B2-1 | Ponto → lado → célula inteira (três movimentos curtos). | O espectador vê o que φ faz antes de ver a célula deformada. |
| G4 | B3-2 | "A área é multiplicada por cinco" (5 Δu Δv), não "toda célula tem área cinco". | Rigor: o 5 é fator, não área. |
| G5 | B3-3 | Fecha a primeira parte do desafio e pergunta pela grade curva. | Ponte para o B4. |
| G6 | B4-2 + alvo 10 | O vetor em pé é (∂φ/∂u Δu) ∧ (∂φ/∂v Δv); os deltas saem depois. | Corrige a escala: com as derivadas sozinhas a altura seria o fator, não a área. |
| G7 | B4-3 | A tabela usa o jacobiano do canto M para a célula inteira (a fala diz). | Diz de onde vem o erro que a tabela mede. |
| G8 | B5-1 | "a soma fica **quase**…" | É a ideia da prova, não a prova. |
| G9 | B5-2 + §3.2 | O papel de cada hipótese numa frase cada; "essas condições bastam; não são as únicas possíveis". | O enunciado deixa de ser lista; condições suficientes, não necessárias. |
| G10 | B5-3 | O mecanismo do 2 é a sobreposição; J = 0 na dobra é outra hipótese violada. | Rigor: a causa certa do erro. |
| G11 | B6-4 | Uma frase de fechamento ("a troca não fez mágica…"). | Fecha o gancho com a ideia do vídeo. |
| G12 | B7 | A lição do sinal × módulo passa para o fim (a frase do meio saiu). | Mesma mensagem, sem repetir. |
| G13 | B8 | Mercator com a Terra esférica; fluido com 1 + t div F + … (det(I + t DF) = 1 + t div F + O(t²) no §3). | Rigor sem conta nova na tela. |
| G14 | §5 | Ordem de corte do GPT: B8 → repetições do B7 → uma linha da tabela → retomadas; não cortar trapézio, sinal, zoom, hipóteses nem o 8/3. | Melhor que a v1, que cortava o 8/3 e o B7. |

**Não entrou**

- Renomear B_uv para A (ou A para B_uv) em todo o vídeo: o Guidorizzi usa A para o retângulo pequeno do §4.1 e B_uv para a região do teorema; a v1 já segue o livro.
- Reescrever o Anexo A inteiro: o próprio GPT pediu mudanças pontuais; as 11 âncoras que ele não tocou ficaram como na v1.
- O S2 "não revelar o r": a v1 já não revelava (a célula do anel leva `ÁREA ≅ ? · Δr Δθ`).
- Escrever O(t²) na tela do B8: fica `+ …`; o O(t²) está só no §3.

**Custo:** +220 palavras, de 19:03 para 20:17. O §5 corta ≈ 1:10 se o WAV passar muito disso.

## Anexo A · Narração v2 (com tags do ElevenLabs v4)

É a narração v1 com as mudanças pontuais do refino filtrado (lista no §8 da proposta v2): H1, B1-1, B2-1, B3-2, B3-3, B4-2, B4-3, B5-1, B5-2, B5-3, B6-4, B7 e B8. As outras 11 âncoras não mudaram.

Tags permitidas: [curious], [thoughtful], [surprised], [happy], [excited], [serious]. Uma por parágrafo (o S2 tem duas, como nos EP. 05 a 10). Sem [slowly] e sem [pause]. Números por extenso na fala. Tela e gatilhos por âncora.

### Tempo por âncora

| Âncora | Trecho | Palavras | Voz (s) | Início estimado |
|---|---|---:|---:|---:|
| H1 | o desafio do vídeo passado | 217 | 72.8 | 0:00 |
| H2 | a ideia do vídeo | 52 | 17.8 | 1:12 |
| A1 | bem-vindos | 60 | 20.5 | 1:30 |
| B1-1 | a régua esticada | 194 | 65.2 | 1:51 |
| B1-2 | o fator numa curva | 105 | 35.5 | 2:56 |
| B2-1 | a transformação | 148 | 49.8 | 3:31 |
| B3-1 | o caso reto: o paralelogramo | 152 | 51.2 | 4:21 |
| B3-2 | o determinante | 132 | 44.5 | 5:12 |
| B3-3 | o sinal e o módulo | 134 | 45.2 | 5:57 |
| B4-1 | a grade curva | 98 | 33.2 | 6:42 |
| B4-2 | de perto, um paralelogramo | 177 | 59.5 | 7:15 |
| B4-3 | o jacobiano | 298 | 99.8 | 8:15 |
| B5-1 | da área para a integral | 163 | 54.8 | 9:55 |
| B5-2 | o teorema | 215 | 72.2 | 10:49 |
| B5-3 | por que inversível | 130 | 43.8 | 12:02 |
| B5-4 | conferindo o teorema | 174 | 58.5 | 12:45 |
| B6-1 | o trapézio: as variáveis e o jacobiano | 201 | 67.5 | 13:44 |
| B6-2 | o trapézio: a região nova | 145 | 48.8 | 14:51 |
| B6-3 | o trapézio: a conta | 173 | 58.2 | 15:40 |
| B6-4 | a conferência | 102 | 34.5 | 16:38 |
| B7 | pause e tente | 200 | 67.2 | 17:13 |
| B8 | o jacobiano no mundo | 122 | 41.2 | 18:20 |
| S1 | síntese | 92 | 31.2 | 19:01 |
| S2 | o próximo vídeo e CTA | 130 | 43.8 | 19:32 |
| **Total** | | **3614** | **20:17** | |

### H1 · o desafio do vídeo passado
**Tela:** layout B. À direita, o trapézio de vértices (1, 0), (2, 0), (0, −2), (0, −1) no papel (GEO translúcido), `∬ e^{(x+y)/(x−y)} dA` a caneta na faixa de baixo; tira em pé âmbar com a placa `TRAVA`; tira deitada magenta com a placa `TRAVA`; no expoente, `x + y` acende laranja e `x − y` acende verde-água; as bordas `x − y = 1` e `x − y = 2` acendem verde-água; nascem as retas `x + y = k` (laranja) e depois `x − y = m` (verde-água), passo 1; à esquerda nasce o plano u, v e o trapézio **voa** para ele, endireitando: `1 ≤ v ≤ 2`, `−v ≤ u ≤ v`; `1/2 ·` aparece em lima na frente da integral com `?`; as células do trapézio de u, v acendem (duas inteiras, `1` e `2`, e duas metades, `½ + ½`: `3 CÉLULAS`) e no papel `ÁREA 3/2`; por último uma célula da grade inclinada acende (chapa + malha) com `ÁREA ?` (a resposta, `1/2`, só aparece no B3-3).
**Gatilhos:** "ficou um desafio"→trapézio · "Fatia em pé"→tira âmbar · "Trava"→placa 1 · "deitada"→tira magenta · "trava também"→placa 2 · "a soma"→`x + y` · "a diferença"→`x − y` · "as bordas também"→bordas acendem · "uma grade nova"→retas nascem · "o trapézio fica reto"→voo para o plano u, v · "um meio na frente"→`1/2 ?` · "três quadradinhos"→1, 2, ½ + ½ · "três meios"→`ÁREA 3/2` · "meio quadradinho do papel"→célula acesa com `ÁREA ?`
> [curious] No fim do vídeo passado, ficou um desafio: este trapézio, com cantos em um, zero; dois, zero; zero, menos dois; e zero, menos um, e a integral dupla de é elevado à fração xis mais ípsilon sobre xis menos ípsilon. Fatia em pé: a integral de dentro, em ípsilon, pede uma primitiva que não se escreve com as funções do Cálculo um. Trava. Fatia deitada: trava também. Nenhuma das duas ordens resolve. Agora repara no expoente. Ele só enxerga duas coisas: a soma, xis mais ípsilon, e a diferença, xis menos ípsilon. E as bordas também: duas delas são retas de xis menos ípsilon constante. Então chama a soma de u e a diferença de vê. As retas de u constante e de vê constante formam uma grade nova, inclinada, por cima do papel. E, nessa grade, o trapézio fica reto: vê vai de um a dois, e u vai de menos vê até vê. A conta sai rapidinho. Só que aparece um meio na frente, que ninguém chamou. E repara: o trapézio tem três quadradinhos da grade nova, contando as duas metades das pontas, mas a área dele no papel é três meios. Então cada quadradinho da grade nova vale só meio quadradinho do papel? De onde sai esse meio? É isso que este vídeo responde.

### H2 · a ideia do vídeo
**Tela:** a célula inclinada grande no centro, com `Δu` e `Δv` nos lados; `JACOBIANO = FATOR LOCAL DE ÁREA` a caneta; embaixo, `dx dy = |J| du dv` (o `|J|` em lima).
**Gatilhos:** "a grade muda"→célula · "estica ou encolhe"→a célula pulsa uma vez de tamanho (um movimento, sem brilho) · "jacobiano"→linha 1 · "vira o módulo"→linha 2
> [serious] E esse é o assunto de hoje. Quando você troca as variáveis, a grade muda, e cada pedacinho de área muda de tamanho. O número que diz quanto ele estica ou encolhe se chama jacobiano. E, na integral, dê xis dê ípsilon vira o módulo do jacobiano vezes dê u dê vê.

### A1 · bem-vindos
**Tela:** logo; `JACOBIANO E MUDANÇA DE VARIÁVEIS`; `NESTE VÍDEO: A RÉGUA · O PARALELOGRAMO · O FATOR LOCAL · O TEOREMA · O TRAPÉZIO`.
**Gatilhos:** "Bem-vindos"→logo · "as próprias variáveis"→título · "a régua esticada"…"do começo ao número"→os cinco itens acendem um a um
> [happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Até aqui, a gente calculou integrais duplas fatiando em xis e em ípsilon. Hoje a gente troca as próprias variáveis. Vamos ver a régua esticada do Cálculo um, o paralelogramo das transformações lineares, o fator local de área, o teorema de mudança de variáveis e, no fim, o trapézio inteiro, do começo ao número.

### B1-1 · a régua esticada
**Tela:** D1 + C1. A coluna: `∫₀² x dx = [x²/2]₀² = 2²/2 − 0²/2 = 2`; as duas réguas (t em cima, x embaixo); `x = 2t ⇒ dx = 2 dt` com os limites `t = 0`, `t = 1` voando das pontas da régua; a conta `∫₀¹ (2t) · 2 dt = 4 ∫₀¹ t dt = 4 [t²/2]₀¹ = 4 · 1/2 = 2 ✓`; no fim, `x = g(t) ⇒ Δx ≅ g′(t) Δt`.
**Gatilhos:** "dá dois"→linha 1 · "xis igual a dois tê"→réguas · "zero a um"→limites voam · "dois dê tê"→`dx = 2 dt` · "duas vezes maior"→o segmento desce e dobra · "fator de comprimento"→rótulo `× 2` · "quatro vezes um meio"→conta · "o mesmo valor"→✓ · "gê linha de tê"→última linha
> [thoughtful] Começa onde você já sabe. No Cálculo um, a integral de zero a dois de xis, dê xis, dá dois: a primitiva é xis ao quadrado sobre dois, e fica quatro sobre dois menos zero. Agora troca a variável: xis igual a dois tê. Quando tê vai de zero a um, xis vai de zero a dois. E o dê xis vira dois dê tê. Por quê? Olha as duas réguas. A do tê tem comprimento um; a do xis, dois. Cada pedacinho delta tê vira um pedacinho delta xis duas vezes maior. Esse dois é o fator de comprimento da troca. E a conta confirma: a integral de zero a um de dois tê, vezes dois, dê tê, é quatro vezes a integral de tê, que é um meio. Quatro vezes um meio, dois. O mesmo valor. Quando a troca não é tão simples, xis igual a gê de tê, o fator muda de lugar para lugar: delta xis é mais ou menos gê linha de tê vezes delta tê. E esse delta xis tem sinal; o fator de comprimento é o módulo de gê linha. Guarda esse sinal: ele volta no determinante.

### B1-2 · o fator numa curva
**Tela:** D2. A curva γ (branca) com `γ(t)` e `γ(t + Δt)`; o arco `Δs` em lima; a seta `γ′(t) Δt` tangente; `Δs ≅ ‖γ′(t)‖ Δt`; Δt encolhe (um movimento) e a seta gruda no arco; no fim, `NO PLANO: FATOR DE ÁREA = ?`.
**Gatilhos:** "um ponto andando"→curva · "um arco"→arco lima · "vetor velocidade"→seta · "a norma"→fórmula · "Quanto menor"→Δt encolhe · "qual é o fator de área"→cartão
> [curious] E se o caminho for uma curva? Gama de tê é um ponto andando no plano. Num tempinho delta tê, ele percorre um arco, delta esse. A derivada, gama linha de tê, é o vetor velocidade, tangente à curva. Então gama linha vezes delta tê é uma setinha tangente, e o comprimento dela, a norma de gama linha de tê vezes delta tê, quase cobre o arco. Quanto menor o delta tê, melhor. Numa dimensão, o fator é sempre o tamanho de uma derivada. E aí vem a pergunta do vídeo: no plano, quando um retângulo vira outra figura, qual é o fator de área?

### B2-1 · a transformação
**Tela:** D3. Layout B. À esquerda, o plano u, v com o retângulo A (chapa + malha), lados `Δu` (laranja) e `Δv` (verde-água), canto `(u₀, v₀)`; seta curva `φ`; à direita, B = φ(A), quadrilátero curvo com cantos `M`, `N`, `P`, `Q`; as retas `u₀ CONSTANTE` e `v₀ CONSTANTE` à esquerda e as curvas correspondentes à direita; faixa de baixo a caneta: `(x, y) = φ(u, v)` · `φ DE CLASSE C¹ NO ABERTO Ω` · `B = φ(A)`.
**Gatilhos:** "fi de u, vê"→fórmula · "de classe cê um"→linha 2 · "um retângulo A"→retângulo · "delta u e delta vê"→rótulos · "a imagem dele"→B · "Um ponto vai num ponto"→um ponto branco voa pela seta φ · "vira uma curva"→o lado Δu vira curva, depois o lado Δv · "M, N, P e Q"→cantos · "quanto vale a área de B"→B acende
> [serious] Vamos dar nome às coisas, como no livro. Fi de u, vê igual a xis, ípsilon: uma transformação que leva cada ponto do plano u vê num ponto do plano xis ípsilon. Ela é de classe cê um num aberto ômega: as derivadas parciais existem e são contínuas, como a gente viu quando estudou derivadas parciais. Pega um retângulo A, de lados paralelos aos eixos, contido em ômega, com lados delta u e delta vê. A imagem dele, B igual a fi de A, é o conjunto dos pontos fi de u, vê com u, vê em A. Um ponto vai num ponto. Um lado, delta u, vira uma curva, e o lado delta vê também. E o retângulo inteiro vira um quadrilátero curvo, com cantos M, N, P e Q. A pergunta é: quanto vale a área de B quando delta u e delta vê são pequenos?

### B3-1 · o caso reto: o paralelogramo
**Tela:** D4, D5 + C2. Layout B: a grade de u, v se inclina inteira (um movimento); o quadrado unitário vira o paralelogramo; os lados viram as setas `(2, 1)` laranja e `(1, 3)` verde-água, que voam para a matriz `[2 1; 1 3]` (sem selo: só a fala cita o EP. 03); a caixa 3 × 4 em GEO, e os seis pedaços saem um a um com a área a caneta; `12 − 2 − 3 − 2 = 5`.
**Gatilhos:** "dois u mais vê"→fórmula · "retas viram retas"→grade inclina · "dois, um"→seta laranja · "um, três"→seta verde-água · "as colunas da matriz"→setas voam · "derivadas parciais"→a matriz ganha moldura fina · "caixa de três por quatro"→caixa · "um de área cada"→2 triângulos saem · "um e meio de área cada"→2 triângulos saem · "um por um"→2 retangulinhos saem · "cinco"→`= 5`
> [thoughtful] Antes da curva, o caso reto. Fi de u, vê igual a dois u mais vê, u mais três vê. É uma transformação linear: retas viram retas, e o quadrado de lado um vira um paralelogramo. Para onde vão os lados? O lado do u, de zero, zero até um, zero, vai para dois, um. O lado do vê vai para um, três. Esses dois vetores são as colunas da matriz dois, um; um, três. É a matriz jacobiana que a gente viu nas derivadas parciais: cada coluna diz para onde vai um lado do quadradinho. E a área? Põe o paralelogramo numa caixa de três por quatro: área doze. Tira dois triângulos de catetos dois e um, um de área cada. Tira dois triângulos de catetos um e três, um e meio de área cada. E tira dois retangulinhos de um por um. Doze, menos dois, menos três, menos dois: cinco.

### B3-2 · o determinante
**Tela:** D5 com letras + C3. A mesma figura com `a`, `b`, `c`, `d` nas pontas das setas; a coluna por glyph maps: o produto aberto, `ac` e `−ac` acendem juntos e somem, `bd` e `−bd` idem, `bc − 2bc` vira `−bc`; `= ad − bc = det [a b; c d]`; `2 · 3 − 1 · 1 = 5 ✓`; a grade inteira com todas as células acesas e `5` em cada uma (as quatro mais próximas).
**Gatilhos:** "Com letras"→letras · "A caixa é á mais bê"→linha 1 · "Abrindo o produto"→linha 2 · "cancela"→pares somem · "sobra menos bê cê"→linha 3 · "o determinante"→det · "cinco"→✓ · "toda célula"→células com 5 · "o mesmo em todo lugar"→selo `FATOR CONSTANTE`
> [serious] Agora com letras: as colunas á, cê e bê, dê. A caixa é á mais bê, vezes cê mais dê. Tira duas vezes á cê sobre dois, duas vezes bê dê sobre dois e dois bê cê. Abrindo o produto: á cê, mais á dê, mais bê cê, mais bê dê. O á cê cancela, o bê dê cancela, e bê cê menos dois bê cê sobra menos bê cê. Fica á dê menos bê cê: o determinante da matriz. Dois vezes três, menos um vezes um: cinco. E, como a transformação é linear, toda célula da grade, de lados delta u e delta vê, vira um paralelogramo de área cinco vezes delta u vezes delta vê: a área é multiplicada por cinco. E o fator é o mesmo em todo lugar.

### B3-3 · o sinal e o módulo
**Tela:** D6 + C4. Layout B: o quadrado com a seta circular anti-horária (`u` depois `v`); à direita o losango com a seta horária; selo `VIROU DE COSTAS` em ALERTA; coluna: as colunas `(1/2, 1/2)` e `(1/2, −1/2)`, `det = (1/2)(−1/2) − (1/2)(1/2) = −1/4 − 1/4 = −1/2`, `ÁREA = |−1/2| = 1/2`; o `1/2` ganha a cor lima e voa para o canto, onde fica como chip até o B6.
**Gatilhos:** "de trás para a frente"→fórmulas · "um meio, um meio"→colunas · "menos um meio"→det · "Área negativa?"→ALERTA · "anti-horário"→seta 1 · "sentido horário"→seta 2 · "virou de costas"→selo · "o módulo"→`|−1/2| = 1/2` · "o meio do trapézio"→chip
> [curious] Agora a troca do trapézio, de trás para a frente: xis igual a u mais vê sobre dois, ípsilon igual a u menos vê sobre dois. As colunas são um meio, um meio, e um meio, menos um meio. O determinante: um meio vezes menos um meio, menos um meio vezes um meio. Menos um quarto, menos um quarto: menos um meio. Área negativa? Não. Anda pelo quadrado no sentido anti-horário: primeiro o lado do u, depois o do vê. Na imagem, a volta sai no sentido horário: o quadrado virou de costas. O sinal conta isso, a orientação. A área é o módulo: um meio. É o meio do trapézio, e a primeira parte do desafio está paga. Falta a outra: e quando a transformação não é linear, e a grade sai curva?

### B4-1 · a grade curva
**Tela:** D7. Layout B: a malha 4 × 4 do quadrado [0, 1]² à esquerda; à direita a grade se curva (um movimento); as bordas ganham rótulos `u = 1 → x = 1 − y²/4` e `v = 1 → x = y²/4 − 1`; as células se pintam pelo tamanho (GEO apagado → lima); a célula perto da origem e a perto do topo acendem com `PEQUENA` e `GRANDE`.
**Gatilhos:** "que entorta"→fórmulas · "a parábola"→rótulos · "quadriláteros curvos"→grade curva · "quase somem"→célula pequena · "crescem"→célula grande · "muda de ponto para ponto"→pintura pelo tamanho
> [thoughtful] Agora uma transformação que entorta: xis igual a u ao quadrado menos vê ao quadrado, e ípsilon igual a dois u vê, no quadrado de zero a um. A reta u igual a um vira a parábola xis igual a um menos ípsilon ao quadrado sobre quatro. A reta vê igual a um vira a parábola xis igual a ípsilon ao quadrado sobre quatro menos um. As células viram quadriláteros curvos. E repara no tamanho: perto da origem, elas quase somem; lá em cima, elas crescem. Aqui não existe um fator só: ele muda de ponto para ponto.

### B4-2 · de perto, um paralelogramo
**Tela:** D8 + Three.js. Zoom na célula de canto `M` (alvo 09): o quadrilátero curvo `MNPQ` (chapa + malha); as setas `∂φ/∂u Δu` (laranja) e `∂φ/∂v Δv` (verde-água) saindo de M; o paralelogramo tracejado lima; `ARCO MN ≅ ‖∂φ/∂u‖ Δu` e `ARCO MQ ≅ ‖∂φ/∂v‖ Δv`. A célula curva vira o paralelogramo (um movimento) e a vista de cima **decola** para a cena Three.js (a vista ortográfica de cima é o mesmo quadro do 2D): o paralelogramo no chão, as duas setas dos deslocamentos, o vetor `(∂φ/∂u Δu) ∧ (∂φ/∂v Δv)` sobe em lima até a altura 3,25 (unidade local = Δ), `ALTURA = ÁREA DO PARALELOGRAMO` (alvo 10); a linha `= Δu Δv ‖∂φ/∂u ∧ ∂φ/∂v‖` com os deltas saindo para fora por glyph map; pouso de volta na vista de cima, que vira o 2D no mesmo quadro.
**Gatilhos:** "dá zoom"→zoom · "vê constante"→lado MN acende · "a setinha"→seta laranja · "delta vê"→seta verde-água · "o paralelogramo dessas duas setas"→tracejado e a célula curva vira o paralelogramo · "Põe as duas setas"→decolagem para o 3D · "fica em pé"→vetor sobe · "a altura dele é a área"→rótulo · "saem para fora"→a linha dos deltas · "vista de cima"→pouso
> [serious] Então dá zoom numa célula, com canto M em u igual a zero vírgula setenta e cinco e vê igual a zero vírgula cinco. O lado MN é a curva de vê constante, andando delta u. Como na curva do começo, ele é quase a setinha da derivada parcial de fi em relação a u, vezes delta u. E o lado MQ é quase a derivada parcial de fi em relação a vê, vezes delta vê. Então a célula é quase o paralelogramo dessas duas setas. E a área de um paralelogramo, lá de vetores, é a norma do produto vetorial. Põe as duas setas, já com o delta u e o delta vê, no chão do espaço, com terceira coordenada zero: o produto vetorial delas fica em pé, na direção cá, e a altura dele é a área do paralelogramo. Os deltas são números, então saem para fora: a área é delta u vezes delta vê vezes a norma do produto vetorial das duas derivadas. Agora volta para a vista de cima, e calcula essa norma.

### B4-3 · o jacobiano
**Tela:** D9, D10 + C6, C5. Layout A: a coluna C6 (o det 3 × 3, a coluna dos zeros acende, sobra o 2 × 2 com o k, a transposta por glyph map, a moldura lima na definição `∂(x, y)/∂(u, v) = det [x_u x_v; y_u y_v]`); `ÁREA DE B ≅ |∂(x, y)/∂(u, v)| Δu Δv` · `FATOR LOCAL DE ÁREA`; depois C5: as quatro derivadas voam de `x = u² − v²` e `y = 2uv` para a matriz, `4u² + 4v²`, `3,25` em M; no palco, a célula de M encolhendo (Δ = 0,25 → 0,1 → 0,05 → 0,01) e a tabela `Δ · EXATA · |J| ΔuΔv · RAZÃO` preenchendo (1,44 · 1,16 · 1,08 · 1,02); por fim `J(0, 0) = 0` e `J(1, 1) = 8` nos cantos da grade.
**Gatilhos:** "i, jota e cá"→det 3 × 3 · "têm zero"→coluna acende · "sobra só o cá"→2 × 2 · "trocando linha por coluna"→transposta · "jacobiano de xis, ípsilon"→moldura · "fator de ampliação"→selo · "dois u"…"dois u"→as quatro derivadas voam · "quatro u ao quadrado mais quatro vê ao quadrado"→J · "três vírgula vinte e cinco"→M · "um vírgula quarenta e quatro"…"um vírgula zero dois"→linhas da tabela · "zero na origem"→`J(0, 0) = 0` · "oito"→`J(1, 1) = 8`
> [serious] O produto vetorial é o determinante com i, jota e cá na primeira linha, as derivadas de xis e de ípsilon em relação a u na segunda, e em relação a vê na terceira, com zero no fim das duas. Os termos com i e com jota têm zero, então sobra só o cá, multiplicado por um determinante dois por dois. Trocando linha por coluna, que não muda o determinante, ele vira a matriz jacobiana: derivadas de xis na primeira linha, de ípsilon na segunda. Esse número se chama o jacobiano de xis, ípsilon em relação a u, vê. E a área da célula é mais ou menos o módulo do jacobiano, vezes delta u, vezes delta vê. O livro chama esse módulo de fator de ampliação, ou de contração, local de área. Na nossa grade: a derivada de xis em relação a u é dois u, em relação a vê, menos dois vê; a de ípsilon em relação a u é dois vê, e em relação a vê, dois u. Dois u vezes dois u, menos menos dois vê vezes dois vê: quatro u ao quadrado mais quatro vê ao quadrado. No ponto M, três vírgula vinte e cinco. E dá para medir o quanto ele acerta, usando o jacobiano do canto M para a célula inteira. Com a célula de lado zero vírgula vinte e cinco, a área de verdade é um vírgula quarenta e quatro vezes o que o jacobiano prevê. Com lado zero vírgula um, um vírgula dezesseis. Com zero vírgula zero cinco, um vírgula zero oito. Com zero vírgula zero um, um vírgula zero dois. Quanto menor a célula, mais ele acerta. E repara: o jacobiano dá zero na origem, onde as células somem, e oito no canto um, um, onde elas crescem.

### B5-1 · da área para a integral
**Tela:** D11 + C7. Layout B: a partição de B_uv em retangulinhos `Rᵢⱼ` à esquerda e as imagens `Bᵢⱼ` à direita; um ponto branco `(ūᵢ, v̄ⱼ)` e a sua imagem `(x̄ᵢ, ȳⱼ)` com a seta φ; faixa de baixo: a cadeia ① → ② → ③, com `α(Bᵢⱼ)` voando da célula da direita e `Δuᵢ Δvⱼ` da célula da esquerda; na passagem ② → ③ a partição se refina (um movimento).
**Gatilhos:** "retangulinhos, erre í jota"→partição · "bê í jota"→imagens · "soma de Riemann"→① · "imagem de um ponto"→pontos e seta · "o módulo do jacobiano"→α voa e vira |J| Δu Δv · "a soma fica quase"→② · "no plano u vê"→o ② acende a célula da esquerda · "as divisões encolhem"→refino · "dê u dê vê"→③
> [thoughtful] Agora junta tudo na integral. Divide a região do plano u vê em retangulinhos, erre í jota. Cada um vira, no papel, um pedacinho, bê í jota. A integral de f sobre B é quase a soma de f num ponto de cada pedacinho, vezes a área do pedacinho, como na soma de Riemann. Escolhe esse ponto como a imagem de um ponto do retangulinho: xis barra, ípsilon barra igual a fi de u barra, vê barra. E a área do pedacinho é quase o módulo do jacobiano vezes delta u vezes delta vê. Então a soma fica quase a soma de f de fi de u barra, vê barra, vezes o módulo do jacobiano, vezes delta u, vezes delta vê. E repara: essa é uma soma de Riemann no plano u vê! Quando as divisões encolhem, ela vai para a integral dupla, no plano u vê, de f de fi de u, vê, vezes o módulo do jacobiano, dê u dê vê.

### B5-2 · o teorema
**Tela:** D12. Layout A: o enunciado a caneta, uma hipótese por linha (`φ DE CLASSE C¹ NO ABERTO Ω` · `B_uv ⊂ Ω COMPACTO, FRONTEIRA DE CONTEÚDO NULO` · `B = φ(B_uv)` e `φ(B̊_uv) = B̊` · `φ INVERSÍVEL NO INTERIOR` · `∂(x, y)/∂(u, v) ≠ 0 NO INTERIOR` · `f INTEGRÁVEL EM B` · `⇒ ∬_B f dx dy = ∬_{B_uv} f(φ(u, v)) |∂(x, y)/∂(u, v)| du dv`), sublinhado de leitura no gatilho; ao lado, uma miniatura por hipótese; no fim, o quadro-receita do livro: `dx dy = |∂(x, y)/∂(u, v)| du dv` · `DETERMINAR B_uv COM B = φ(B_uv)`.
**Gatilhos:** "sem demonstrar"→título `TEOREMA` · "classe cê um"→linha 1 · "compacto"→linha 2 · "conteúdo nulo"→fronteira acende · "o interior vai no interior"→linha 3 · "inversível"→linha 4 · "diferente de zero"→linha 5 · "integrável"→linha 6 · "é igual"→⇒ · "Na prática"→quadro-receita
> [serious] O livro enuncia esse resultado sem demonstrar, porque a prova completa é longa, mas cada hipótese tem um papel. Fi de classe cê um num aberto ômega: as derivadas são contínuas, e de perto a célula é quase o paralelogramo. Bê u vê contido em ômega, compacto, quer dizer, fechado e limitado, e com fronteira de conteúdo nulo, como a gente viu quando estudou conteúdo nulo: a borda não pesa na soma. B é a imagem, fi de bê u vê, e o interior vai no interior: as duas regiões se correspondem. Fi inversível no interior de bê u vê: dois pontos diferentes de dentro não caem no mesmo lugar, e nenhum pedaço é contado duas vezes. E o jacobiano diferente de zero em todo ponto do interior: nenhuma célula de dentro se achata. Nessas condições, se f é integrável em B, a integral dupla de f sobre B é igual à integral sobre bê u vê de f de fi de u, vê, vezes o módulo do jacobiano, dê u dê vê. Essas condições bastam; não são as únicas possíveis. Na prática, é uma receita de dois passos: dê xis dê ípsilon vira o módulo do jacobiano dê u dê vê, e você descobre a região bê u vê que fi leva em B.

### B5-3 · por que inversível
**Tela:** D13. Layout B: o retângulo [−1, 1] × [0, 1] à esquerda (metades laranja-claro e verde-água-claro); `φ(u, v) = (u², v)`; a metade esquerda dobra por cima da direita (um movimento) e as duas caem no quadrado [0, 1]²; coluna: `∬ |J| du dv = ∫₀¹ ∫₋₁¹ 2|u| du dv = 2` × `ÁREA DA IMAGEM = 1` em ALERTA; a linha u = 0 acende com `J = 2u = 0`; a parte sobreposta acende com o selo `SOBREPOSIÇÃO: CONTOU DUAS VEZES`; por último a borda de um quadrado genérico acende fina com `NA BORDA, PODE`.
**Gatilhos:** "se não for"→retângulo · "u ao quadrado"→fórmula · "dobra por cima"→dobra · "dá dois"→conta · "a área do quadrado é um"→ALERTA · "a sobreposição"→selo · "zera no meio"→linha u = 0 · "na borda"→selo final
> [curious] Por que exigir que fi seja inversível? Olha o que acontece se não for. Fi de u, vê igual a u ao quadrado, vê, no retângulo com u entre menos um e um. A metade da esquerda dobra por cima da direita, e as duas caem no mesmo quadrado de lado um. O jacobiano é dois u, e a integral do módulo dele dá dois. Mas a área do quadrado é um. Quem conta a área duas vezes é a sobreposição: cada ponto do quadrado recebe um pedaço de cada metade. E o jacobiano ainda zera no meio, na dobra, um ponto do interior: outra hipótese que falha. Já na borda, o teorema deixa o jacobiano zerar, e deixa fi não ser injetora. Isso vai fazer diferença no próximo vídeo.

### B5-4 · conferindo o teorema
**Tela:** D14 + C8, C9. Layout A com a região entre parábolas no palco; coluna C8 inteira; depois a tira deitada no palco: entrada na parábola azul-claro `x = y²/4 − 1`, saída na coral `x = 1 − y²/4`; C9 inteira (as duas curvas vêm das bordas por glyph map: `v = y/2` substituído); `8/3 = 8/3 ✓`.
**Gatilhos:** "f igual a um"→C8 linha 1 · "Por dentro, em u"→linha 2 · "Por fora, em vê"→linha 3 · "sem jacobiano"→tira deitada · "entra na parábola"→azul-claro · "sai na"→coral · "a saída menos a entrada"→C9 linha 3 · "oito terços"→C9 linha 4 · "Bateu"→✓
> [happy] Testa o teorema na região das parábolas, com f igual a um, que dá a área. A área é a integral no quadrado de quatro u ao quadrado mais quatro vê ao quadrado. Por dentro, em u: quatro u ao cubo sobre três, mais quatro vê ao quadrado vezes u, de zero a um, que dá quatro terços mais quatro vê ao quadrado. Por fora, em vê: quatro vê sobre três, mais quatro vê ao cubo sobre três, de zero a um: quatro terços mais quatro terços, oito terços. Agora confere sem jacobiano, fatiando deitado, como no vídeo das regiões gerais. A fatia entra na parábola da esquerda, xis igual a ípsilon ao quadrado sobre quatro menos um, e sai na da direita, xis igual a um menos ípsilon ao quadrado sobre quatro. O comprimento é a saída menos a entrada: dois menos ípsilon ao quadrado sobre dois. A integral de zero a dois dá dois ípsilon menos ípsilon ao cubo sobre seis: quatro menos oito sextos, quatro menos quatro terços, oito terços. Bateu.

### B6-1 · o trapézio: as variáveis e o jacobiano
**Tela:** D15 + C10, C11. Layout B do H (o trapézio com a grade inclinada); coluna: `u = x + y` · `v = x − y`, os dois `x + y` e `x − y` voando do expoente; `u + v = 2x ⇒ x = (u + v)/2` e `u − v = 2y ⇒ y = (u − v)/2` por glyph map; as quatro derivadas; `J = −1/2` (o chip lima do B3-3 volta e encaixa); `|J| = 1/2`; a conferência `∂(u, v)/∂(x, y) = −2`; no palco, uma célula da grade inclinada acende com `LADO 1/√2` e `ÁREA 1/2`.
**Gatilhos:** "Passo um"→`u`, `v` voam · "Soma as duas"→x · "Subtrai"→y · "Passo três"→derivadas · "menos um meio"→J · "um meio"→|J| · "pelo outro lado"→conferência · "divide por dois"→`(−2)(−1/2) = 1` · "um sobre raiz de dois"→célula
> [serious] Agora sim, o trapézio. Passo um: escolher as variáveis. O integrando pede a soma e a diferença, e as bordas também. Então u igual a xis mais ípsilon, e vê igual a xis menos ípsilon. Passo dois: o teorema quer xis e ípsilon em função de u e vê. Soma as duas: u mais vê é dois xis, então xis é u mais vê sobre dois. Subtrai: u menos vê é dois ípsilon, então ípsilon é u menos vê sobre dois. Passo três: o jacobiano. A derivada de xis em relação a u é um meio, em relação a vê, um meio; a de ípsilon em relação a u é um meio, e em relação a vê, menos um meio. Um meio vezes menos um meio, menos um meio vezes um meio: menos um quarto menos um quarto, menos um meio. Módulo: um meio. E dá para conferir pelo outro lado: o jacobiano de u, vê em relação a xis, ípsilon é um vezes menos um, menos um vezes um: menos dois. A ida dobra a área, e a volta divide por dois. No papel, cada célula da grade inclinada tem lado um sobre raiz de dois, e área um meio.

### B6-2 · o trapézio: a região nova
**Tela:** D15 + C12. Layout B: os quatro lados do trapézio acendem um por um com a equação e **voam** para o plano u, v, virando `u = v` (coral), `v = 2`, `u = −v` (azul-claro), `v = 1`; os quatro cantos com as coordenadas antes e depois; a tira deitada no plano u, v (v congelado), entrada azul-claro e saída coral; `B_uv: 1 ≤ v ≤ 2, −v ≤ u ≤ v`.
**Gatilhos:** "Passo quatro"→lado 1 · "u igual a vê"→`u = v` · "vê igual a dois"→lado 2 · "u igual a menos vê"→lado 3 · "vê igual a um"→lado 4 · "Os cantos conferem"→cantos · "entra em menos vê"→azul-claro · "sai em vê"→coral · "bê u vê"→a linha final
> [thoughtful] Passo quatro: a região nova. Cada lado do trapézio vira um lado novo. O de cima, ípsilon igual a zero: aí u e vê ficam iguais a xis, então u igual a vê. A borda xis menos ípsilon igual a dois vira vê igual a dois. O lado xis igual a zero: u fica ípsilon e vê fica menos ípsilon, então u igual a menos vê. E a borda xis menos ípsilon igual a um vira vê igual a um. Os cantos conferem: um, zero vai para um, um; dois, zero vai para dois, dois; zero, menos dois vai para menos dois, dois; e zero, menos um vai para menos um, um. No plano u vê, vê vai de um a dois, e, para cada vê, a fatia em u entra em menos vê e sai em vê. Essa é a região bê u vê.

### B6-3 · o trapézio: a conta
**Tela:** D16 + C13, C14, C15. Layout A com o plano u, v no palco (a tira deitada); a coluna por glyph maps: a integral montada (o `1/2` lima voa do chip; os limites voam do palco); a primitiva e a conferência da derivada; o colchete; `v (e − 1/e)`; a de fora; `[v²/2]₁² = 4/2 − 1/2 = 3/2`; `(1/2)(e − 1/e)(3/2) = (3/4)(e − 1/e) ≈ 1,763`.
**Gatilhos:** "Passo cinco"→C13 · "o vê está congelado"→a tira acende · "vê vezes é elevado"→primitiva · "deriva e confere"→conferência · "Colchete"→C14 linha 2 · "é menos um sobre é"→C14 linha 3 · "Por fora"→C15 linha 1 · "três meios"→C15 linha 2 · "três quartos"→C15 linha 3 · "um vírgula setenta e seis"→≈
> [serious] Passo cinco: a conta. A integral fica a integral de um a dois, em vê, da integral de menos vê até vê, em u, de é elevado a u sobre vê, vezes um meio, dê u, dê vê. Por dentro, o vê está congelado, e o expoente é só u vezes um número. A primitiva de é elevado a u sobre vê, em u, é vê vezes é elevado a u sobre vê: deriva e confere, vê vezes um sobre vê dá um. Colchete de menos vê até vê: vê vezes é elevado a um, menos vê vezes é elevado a menos um. Fica vê vezes, é menos um sobre é. Por fora: um meio, vezes é menos um sobre é, vezes a integral de um a dois de vê, dê vê. A primitiva é vê ao quadrado sobre dois: quatro sobre dois menos um sobre dois, três meios. Um meio vezes três meios, três quartos. Resultado: três quartos de é menos um sobre é, mais ou menos um vírgula setenta e seis.

### B6-4 · a conferência
**Tela:** D17 + C16. Layout B: as 3 células da grade nova acendem no trapézio de u, v (`1, 2, 3`); a coluna C16; no papel, o triângulo grande de catetos 2 (GEO) e o pequeno de catetos 1 (ALERTA tracejado) que sai; `3/2 = 3/2 ✓`; o `1/2` lima ganha o rótulo `O JACOBIANO`.
**Gatilhos:** "f igual a um"→células · "dois vê"→C16 linha 1 · "três"→`= 3` · "vezes o fator"→linha 2 · "No papel"→triângulos · "três meios"→✓ · "é o jacobiano"→rótulo
> [happy] E o teste de sempre, com f igual a um. No plano u vê, a fatia vai de menos vê até vê: comprimento dois vê. A integral de um a dois de dois vê dá vê ao quadrado, quatro menos um, três. Vezes o fator, um meio: três meios. No papel, o trapézio é o triângulo grande, de catetos dois, área dois, menos o pequeno, de catetos um, área um meio: três meios também. O meio que ninguém chamou é o jacobiano. A troca não fez mágica: escolheu a grade em que tudo fica simples, e pagou com o fator de área.

### B7 · pause e tente
**Tela:** D18 + C17. Layout A: o trapézio `1 ≤ x + y ≤ 2`, `x ≥ 0`, `y ≥ 0` no palco, `∬ cos(x − y)/sen(x + y) dx dy`; `PAUSE E TENTE` por 3 s; a escada C17 linha a linha (ritmo mais rápido, cada linha a caneta); nota `SINAL TROCOU, MÓDULO NÃO` ao lado do `J = +1/2`; `= 1 ✓`.
**Gatilhos:** "Pausa o vídeo"→`PAUSE E TENTE` · "u igual a xis menos ípsilon"→C17 linha 1 · "mais um meio"→linha 2 · "trocaram de papel"→nota · "vê igual a um"→linha 3 · "dois seno de vê"→linha 4 · "dá um"→linha 5
> [curious] Pausa o vídeo e tenta este, que é do livro: a integral do cosseno de xis menos ípsilon sobre o seno de xis mais ípsilon, no trapézio entre xis mais ípsilon igual a um e xis mais ípsilon igual a dois, no primeiro quadrante. Pronto? O livro escolhe u igual a xis menos ípsilon e vê igual a xis mais ípsilon. Então xis é u mais vê sobre dois, e ípsilon é vê menos u sobre dois. O jacobiano: um meio vezes um meio, menos um meio vezes menos um meio, um quarto mais um quarto, mais um meio. As bordas viram vê igual a um, vê igual a dois, vê igual a u e vê igual a menos u. Por dentro, um sobre seno de vê sai da integral, e o seno de u, de menos vê até vê, dá seno de vê menos seno de menos vê, dois seno de vê. Dividido por seno de vê: dois. Por fora, um meio vezes a integral de um a dois de dois: um meio vezes dois vezes um, que dá um. O sinal mudou porque u e vê trocaram de papel; o fator de área, que é o módulo, não.

### B8 · o jacobiano no mundo
**Tela:** D19. Dois cartões de traço GEO: (1) a grade de Mercator (meridianos verticais, paralelos cada vez mais espaçados para o norte), uma célula em 72° acesa com `× sec²(LATITUDE)` e `≈ × 10`; (2) o quadradinho do EP. 03 escoando num campo (um movimento curto), `ÁREA × (1 + t · div F + …)` (o `…` é o resto de ordem t², sem escrever O(t²) na tela).
**Gatilhos:** "Mercator"→cartão 1 · "mais de dez vezes"→`≈ × 10` · "catorze vezes"→a célula do equador ao lado · "nos fluidos"→cartão 2 · "um, mais tê vezes o divergente"→`1 + t · div F + …`
> [thoughtful] O jacobiano aparece fora da integral também. No mapa do mundo mais comum, a projeção de Mercator, tratando a Terra como uma esfera, o fator de área é a secante da latitude ao quadrado. Na altura da Groenlândia, uns setenta e dois graus norte, cada pedacinho aparece mais de dez vezes maior do que perto do equador. É por isso que a Groenlândia parece do tamanho da África, que é umas catorze vezes maior. E nos fluidos: num tempo curtinho tê, cada pedacinho da água estica ou encolhe, e o fator de área fica um, mais tê vezes o divergente, mais termos menores. O divergente, a soma dos estiramentos das derivadas parciais, é a taxa com que o fator começa a mudar.

### S1 · síntese
**Tela:** `dx dy = |J| du dv` grande no topo; quatro caixas com ✓: `RÉGUA: dx = g′(t) dt` · `LINEAR: ÁREA × |ad − bc|` · `CURVA: ÁREA ≅ |J| ΔuΔv` · `TRAPÉZIO: (3/4)(e − 1/e)`.
**Gatilhos:** "Na régua"→caixa 1 · "No caso linear"→caixa 2 · "Na transformação curva"→caixa 3 · "no trapézio"→caixa 4 · "o fator local de área"→fórmula do topo acende
> [serious] Resumindo. Na régua do Cálculo um, o dê xis vira gê linha de tê dê tê. No caso linear, o quadrado vira paralelogramo, e a área se multiplica pelo módulo do determinante, á dê menos bê cê. Na transformação curva, cada célula é quase um paralelogramo, e a área dela é o módulo do jacobiano vezes delta u vezes delta vê. E, no trapézio, a troca certa transformou duas ordens travadas numa conta de cinco passos. Trocar as variáveis é trocar a grade, e o jacobiano é o fator local de área.

### S2 · o próximo vídeo e CTA
**Tela:** o disco x² + y² ≤ 1 no papel com `∬ e^{−(x²+y²)} dA`; tira em pé e tira deitada, cada uma com `TRAVA`; a grade quadrada some e nasce a grade de círculos (laranja) e raios (verde-água), com `r` e `θ`; uma célula do anel acende (chapa + malha) com `ÁREA ≅ ? · Δr Δθ`; cartão `NO PRÓXIMO VÍDEO: COORDENADAS POLARES` / `QUAL É O FATOR DA GRADE DE CÍRCULOS?` (≥ 8 s); depois o CTA padrão.
**Gatilhos:** "um desafio"→disco · "Em pé, trava"→placa 1 · "deitado, trava"→placa 2 · "círculos e raios"→grade nova · "pedaço de anel"→célula · "Qual é o fator"→`?` · "no próximo vídeo"→cartão · "deixa o like"→CTA
> [curious] E fica um desafio. O disco de raio um, e a integral de é elevado a menos, xis ao quadrado mais ípsilon ao quadrado. É o sino do vídeo das regiões gerais, agora girado em volta da origem. Em pé, trava; deitado, trava. Mas o disco pede outra grade: círculos e raios, com as variáveis erre e teta. Só que a célula dessa grade não é um retângulo: é um pedaço de anel, mais largo longe do centro. Qual é o fator de área dela? É o que a gente descobre no próximo vídeo: coordenadas polares. [happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual troca de variável você já fez sem saber que tinha um jacobiano escondido? Até a próxima!

## Anexo B · Como cada símbolo é lido na fala

| Símbolo | Como se lê | Âncora |
|---|---|---|
| ∬ e^{(x+y)/(x−y)} dA | "a integral dupla de é elevado à fração xis mais ípsilon sobre xis menos ípsilon" | H1 |
| u, v | "u", "vê" | H1 |
| dx dy = \|J\| du dv | "dê xis dê ípsilon vira o módulo do jacobiano vezes dê u dê vê" | H2 |
| x = 2t, dx = 2 dt | "xis igual a dois tê", "dois dê tê" | B1-1 |
| Δt, Δx | "delta tê", "delta xis" | B1-1 |
| g′(t) | "gê linha de tê" | B1-1 |
| γ(t), γ′(t), ‖γ′(t)‖ | "gama de tê", "gama linha de tê", "a norma de gama linha de tê" | B1-2 |
| Δs | "delta esse" | B1-2 |
| (x, y) = φ(u, v) | "fi de u, vê igual a xis, ípsilon" | B2-1 |
| Ω, C¹ | "ômega", "classe cê um" | B2-1 |
| B = φ(A) | "B igual a fi de A" | B2-1 |
| [a b; c d], ad − bc | "a matriz á, bê; cê, dê", "á dê menos bê cê" | B3-2 |
| \|−1/2\| | "o módulo de menos um meio" | B3-3 |
| ∂φ/∂u | "a derivada parcial de fi em relação a u" | B4-2 |
| ∧ | "produto vetorial" | B4-2 |
| i, j, k | "i, jota, cá" | B4-3 |
| ∂(x, y)/∂(u, v) | "o jacobiano de xis, ípsilon em relação a u, vê" | B4-3 |
| Rᵢⱼ, Bᵢⱼ | "erre í jota", "bê í jota" | B5-1 |
| ū, v̄, x̄, ȳ | "u barra", "vê barra", "xis barra", "ípsilon barra" | B5-1 |
| B_uv | "bê u vê" | B5-2 |
| B̊ | (não lido; a fala diz "o interior de B") | B5-2 |
| (3/4)(e − 1/e) | "três quartos de é menos um sobre é" | B6-3 |
| cos(x − y)/sen(x + y) | "o cosseno de xis menos ípsilon sobre o seno de xis mais ípsilon" | B7 |
| sec²(latitude) | "a secante da latitude ao quadrado" | B8 |
| 1 + t · div F + … | "um, mais tê vezes o divergente, mais termos menores" | B8 |
| r, θ | "erre", "teta" | S2 |
