# yt_0027 · CÁLCULO III · EP. 02 · Rotacional e divergente
## Avaliação do preview v3 e HANDOFF v4 (para o Claude Code). Último handoff visual antes da voz

Data: 2026-11-11. Unidade: `videos_longos/yt_0027_*`. Fase: **preview visual v4** (540p/15 fps). Não gerar voz, SRT, master nem entrega nesta fase. Depois do v4 aprovado, o próximo handoff é o de voz, sincronia, 1080p, SRT e entrega.

Este handoff **substitui o v3 só nos itens abaixo**. Todo o resto do v3 (e do v2) continua valendo: sistema visual, regras R1–R5, cenas reescritas do v3 e mudanças de narração do v3. A narração de trabalho é o `narracao.md` da unidade (versão do preview v3), com as mudanças do §5 deste handoff.

Quadros-alvo v4: `yt_0027_quadros_alvo_v4/`.
- `00_problemas_no_v3.jpg`: os 8 problemas do preview v3, cada um no tempo em que aparece.
- **Novos:** 14, 15, 16 e 17.
- **Repetidos do v3, porque não entraram no render:** 02, 11, 12 e 13 (malha) e 07 (clareira dos níveis).
- **Repetidos só como referência:** 01, 05 e 08.

Os geradores `sb27.html` e `c3d27.html` estão na pasta. As chaves novas são `d11`, `b26v4`, `d60` e `b63v4`.

---

## 1. Avaliação do v3 (19:00)

O v3 resolveu quase tudo do v2:
- o hook e o A1;
- os braços do B2;
- os painéis do B3 e o tornado;
- a área junto do quadradinho no B4-1;
- a tabela do B5-2 com clareira;
- o cubo novo (ficou igual ao alvo);
- a rodinha 3D;
- o F1/F2;
- o gráfico do calor (vale, média dos vizinhos, SOBE, ANTES);
- o S3 com STOKES/GAUSS/GREEN sem sobreposição;
- o S4 com o nome "deforma";
- o CTA.

O rio também ficou bom: as rodinhas estão entre as fileiras de setas e o degradê saiu.

Sobram três frentes:
1. **A malha do pedacinho não entrou.** O §3.7 do v3 foi acrescentado depois que o handoff já tinha sido colado. Ela volta aqui, no §4, como item obrigatório.
2. **P, Q e R aparecem sem definição.** A primeira vez que o Q aparece na tela é no B2-2, dentro de uma fórmula, e ninguém disse o que ele é. A fala dizia "componente vertical", mas a tela nunca liga a letra à componente. O §3 resolve isso.
3. **Oito defeitos de tela** (§2). O relatório de sobreposição do v3 deu "0 ocorrências", mas quatro desses defeitos são sobreposições. O R5 precisa olhar também as transições (§2, R6).

---

## 2. Defeitos do v3 (tempos do preview v3) · ver `00_problemas_no_v3.jpg`

| # | Tempo | Cena | Problema | Correção |
|---|---|---|---|---|
| N1 | 1:27–1:47 | B1-1 | Há **duas setas laranja**: uma parada em (1,6; 0), apontando para cima, e a do ponto que anda. | Sai a seta parada. Fica só o ponto andando com a sua seta `v` (alvo 01). |
| N2 | 2:17–2:22 | B1-3 | Os três painéis ficam **vazios por ~5 s** antes de os campos e os pedacinhos entrarem. | Painel, campo e pedacinho entram juntos, um cartão por frase. Painel vazio nunca aparece. |
| N3 | 3:18–3:22 | B2-2 | A linha `ω_AB ≈ [Q(x₀+h, y₀) − Q(x₀, y₀)]/h` aparece **duas vezes**, empilhada, e o `h` da de cima cai sobre o numerador da de baixo. | Uma linha só. O `TransformByGlyphMap` para `ω_AB = ∂Q/∂x` usa como origem **a mesma** linha que a CANETA escreveu, sem cópia. Antes do transform, conferir que só há uma instância visível desse MathTex. |
| N4 | 5:37–5:45 | B2-6 | `VORTICIDADE = 2ω (CORPO RÍGIDO)` fica espremida entre a linha das derivadas e a do rot, encostando nos denominadores. | Coluna nova do alvo 15: `F = (−y, x)` → `P = −y, Q = x` → derivadas → rot → `ω = 1` → VORTICIDADE por último, embaixo de tudo. Rodinha com clareira. |
| N5 | 12:52–13:10 | B6-1 | Cubo ok, mas as 3 setas de **entrada** aparecem através do vidro como borrões verde-escuros. | Ajuste fino: setas de entrada em menta a 70 %, comprimento 0,75 (era 0,55), com a ponta inteira visível. Molduras das paredes de trás a 50 %. O resto do cubo fica igual. |
| N6 | 13:50–14:08 | B6-3 | As legendas `DIREÇÃO…` e `TAMANHO…` ficam no meio da coluna, e o `rot = ∇ × F` e o `div` são escritos em volta delas. | Legendas **embaixo da rodinha 3D**. A coluna fica só com fórmulas, incluindo a forma aberta (alvo 17, §3.3). |
| N7 | 15:30–16:20 | B7-3 | Os números dos níveis (1, 2, 3, 4) ficam **sob as setas do gradiente** (o R1 não foi aplicado aqui). | Clareira nos 4 números, como no alvo 07. |
| N8 | 16:22–16:25 | B7-3 → B7-4 | A chapa laranja **entra por cima** do campo do laplaciano, e depois fica ~1,5 s sozinha na tela (de novo o "quadrado laranja"). | O B7-3 sai inteiro primeiro. Depois o gráfico entra e, 0,3 s depois, a chapa embaixo dele (alvo 08). A chapa nunca aparece sem o gráfico. |

Os quadros vazios do v3 (2:45, 8:42, 14:10 etc., todos ≤ 0,5 s) estão dentro da regra e ficam.

### R6 · QA de sobreposição também nas transições (novo, vale para o vídeo inteiro)

O `sobreposicoes_v3.txt` só olhou os quadros parados. N3, N4, N7 e N8 escaparam por isso. No v4:
- Amostrar a cada **0,2 s** em todo o vídeo, inclusive durante `Transform`, `FadeIn` e `FadeOut`. Não basta olhar nos gatilhos.
- Contar como sobreposição:
  - duas caixas de texto ou MathTex se cruzando (margem de 4 px);
  - texto sobre o centro de uma seta de campo visível;
  - um objeto de uma cena (chapa, painel, campo) sobre um objeto de outra.
- Acusar **duplicata**: dois MathTex com a mesma string visíveis ao mesmo tempo.
- Gravar o relatório em `renders/v4/qa/sobreposicoes_v4.txt`. Zero ocorrências esperadas; cada exceção com justificativa.

---

## 3. Definição de P, Q e R (pedido do Kaio) · alvos 14, 15, 16 e 17

**Decisão:** a definição formal entra em **dois momentos**, e não num bloco só no começo:
- **no plano, logo antes do primeiro uso** (B1-1a, novo): Ω aberto, `F(x, y) = (P(x, y), Q(x, y))`, P horizontal e Q vertical, com a seta decomposta;
- **na forma geral, em ℝⁿ, na abertura do B6** (B6-0, novo): `F = (F₁, …, Fₙ)` e o divergente como soma das derivadas de cada componente na própria direção.

**Por quê:**
- Um cartão em ℝⁿ antes do hook mataria a curiosidade.
- A forma geral só faz sentido quando a pessoa já viu os casos n = 2 e n = 3.
- Com o Ω definido no B1-1a, o `Ω = ℝ² − {(0,0)}` do vórtice (B3-2) passa a ter sentido.

Livro nenhum é citado, nem na tela nem na fala.

### 3.1 B1-1a · nomes das peças (novo, antes do B1-1) · alvo 14 · chave `d11`

- **Palco:** campo `(−y, 2x)` em **contexto** (verde escuro, como no B1-1). No ponto (0,5; 1,3), a seta do campo acende em menta claro, com 8 px e ponta 28.
- **Decomposição da seta:**
  - a componente horizontal sai do ponto (menta, 6 px, aponta para a esquerda, porque P < 0 ali);
  - a vertical sai da ponta da horizontal e chega à ponta da seta;
  - linhas-guia GEO tracejadas fecham o retângulo.
- **Rótulos com placa e clareira:** `P` embaixo da horizontal, `Q` ao lado da vertical, `F⃗` na ponta e `(x, y)` no ponto.
- **Coluna** (x = 1120, de cima para baixo, CANETA):
  1. `UM CAMPO NO PLANO`;
  2. `Ω ⊂ ℝ² aberto,  F⃗ : Ω → ℝ²`;
  3. `F⃗(x, y) = (P(x, y), Q(x, y))`;
  4. legendas `P: COMPONENTE HORIZONTAL` e `Q: COMPONENTE VERTICAL` (menta), e `P E Q COM DERIVADAS PARCIAIS CONTÍNUAS EM Ω` (GEO);
  5. `F⃗ = (−y, 2x)` e, embaixo, `P = −y,  Q = 2x`.
- **Cores:** P, Q e R em menta em todo o vídeo, como já estão; x âmbar, y magenta.
- **Saída:** a coluna sai e entra o B1-1 do v3 (ponto andando, `v` laranja, `CAMPO = VELOCIDADE`), com o mesmo campo. A troca é só na coluna; o campo não pisca.

### 3.2 B2-6 · P e Q do exemplo e a vorticidade no lugar · alvo 15 · chave `b26v4`

A coluna fica assim, de cima para baixo:
1. `F⃗ = (−y, x)`;
2. `P = −y,  Q = x` (nova);
3. `∂Q/∂x = 1,  ∂P/∂y = −1`;
4. `rot F⃗ = (1 − (−1)) k⃗ = 2 k⃗`;
5. `ω = 1`;
6. `VORTICIDADE = 2ω (CORPO RÍGIDO)`.

A rodinha fica em (1,5; 0), com clareira de 0,62 u nas setas polares.

### 3.3 B6-0 · em qualquer dimensão (novo, abre o B6, antes do cubo) · alvo 16 · chave `d60`

Esta cena é um cartão sem campo:
- título `EM QUALQUER DIMENSÃO`;
- `Ω ⊂ ℝⁿ aberto,  F⃗ = (F₁, F₂, …, Fₙ)`;
- legenda `CADA COMPONENTE COM DERIVADAS PARCIAIS EM Ω`;
- em destaque, `div F⃗ = ∂F₁/∂x₁ + ∂F₂/∂x₂ + ⋯ + ∂Fₙ/∂xₙ`;
- dois painéis sem preenchimento:
  - `NO PLANO (n = 2)` com `(F₁, F₂) = (P, Q)` e `(x₁, x₂) = (x, y)`;
  - `NO ESPAÇO (n = 3)` com `(F₁, F₂, F₃) = (P, Q, R)` e `(x₁, x₂, x₃) = (x, y, z)`;
- no pé, `DIVERGENTE: VALE EM QUALQUER n` (azul-claro) e `ROTACIONAL: CAMPO NO ESPAÇO (O DO PLANO É O CASO R = 0)` (violeta).

Os Fᵢ ficam em menta. Os xᵢ genéricos ficam em branco; só x, y e z têm as cores dos eixos.

Na transição para o B6-1, o painel `NO ESPAÇO` fica e vira a coluna do cubo: o `div` de três parcelas sobe para o topo da coluna. O resto sai.

### 3.4 B6-3 · rot aberto em componentes · alvo 17 · chave `b63v4`

- A rodinha 3D fica à esquerda, como no v3. `DIREÇÃO: EIXO DO GIRO MAIS RÁPIDO` e `TAMANHO: O DOBRO DESSA RAPIDEZ` ficam **embaixo dela**, centradas.
- A coluna começa em x = 1000, para caber a forma aberta. De cima para baixo:
  1. o determinante;
  2. `= (∂R/∂y − ∂Q/∂z,  ∂P/∂z − ∂R/∂x,  ∂Q/∂x − ∂P/∂y)`, em 40 px;
  3. a legenda violeta `3ª COMPONENTE = O ROTACIONAL DO PLANO`. No gatilho dela, a 3ª componente pisca em violeta uma vez (Indicate);
  4. `rot F⃗ = ∇ × F⃗  (∇ ∧ F⃗)`;
  5. `div F⃗ = ∇ · F⃗`.

Conferido no sympy: a expansão do determinante bate com as componentes, e o rot de `(P(x, y), Q(x, y), 0)` é `(0, 0, Q_x − P_y)`. O script `verifica_calc3_t2_sympy.py` (bloco V4) dá tudo True.

---

## 4. Malha no pedacinho de fluido (obrigatório, não entrou no v3) · alvos 02, 11, 12 e 13

Esta é a mesma representação aprovada para o yt_0028. Ela vale para **todo** pedacinho de fluido do vídeo:
- os três cartões do B1-3;
- o quadradinho do B4-1;
- os dois do B4-6;
- o setor da falsa fonte no B5-2;
- o do S4.

Não vale para a caixa fixa do B4-3/B4-4/B4-5 nem para a do B5-2 (caixa de contas). Essas continuam chapa GEO, sem malha.

**Aparência:**
- **Chapa:** preenchimento **opaco** `#6B3A4F` (coral escuro).
- **Contorno:** coral `#FF7A8A`, 3,5 px.
- **Malha 4×4:** 3 linhas em cada direção, `#E89AAA`, 2 px.
- O contorno inicial continua tracejado, coral a 60 %.
- Clareira (R1) em volta do pedacinho na posição final, com margem de 0,25 u.

**A malha é carregada pelo fluxo exato do campo.** Cada vértice anda com o fluxo, e as linhas são curvas amostradas com ~20 pontos por lado. O que a pessoa vê em cada caso:
- no giro, a malha gira junto, e é isso que mostra o giro;
- na explosão, ela cresce sem entortar;
- na deformação (B1-3 e S4), as células esticam e achatam;
- na falsa fonte, a malha usa coordenadas polares (r, θ): o setor fica mais largo e mais fino, e a malha acompanha.

**No Manim:** um `VGroup` (chapa + 6 curvas + contorno) com updater só durante o fluxo. Ao fim, `clear_updaters()`. A referência de geometria é a função `pedaco()` do `sb27.html` (chaves `b13m`, `b42m`, `b52m` e `ctam`).

---

## 5. Narração: mudanças do v4 (só as frases que mudam)

O texto ganha ~180 palavras (≈ +1 min). A duração do v4 vai para ~20 min.

**B1-1a (nova, entre o A1 e o B1-1):**
> [thoughtful] Antes de tudo, vamos dar nome às peças. Um campo vetorial no plano coloca uma seta em cada ponto de uma região aberta, que a gente chama de ômega. Aberta quer dizer sem a borda: dá para chegar perto de cada ponto por todos os lados, e é isso que deixa a gente derivar. Toda seta se quebra em duas partes. A parte horizontal a gente chama de P, e a vertical, de Q. E as duas mudam de ponto para ponto: P e Q são funções de x e de y. Neste campo, P é menos y, e Q é dois x. Então, daqui para frente, quando aparecer derivada de P ou de Q, é isso: a gente está olhando como uma das partes da seta muda.

Gatilhos:

| Palavra | O que acontece |
|---|---|
| "nome às peças" | a seta acende |
| "região aberta" | linha Ω |
| "duas partes" | decomposição |
| "horizontal… P" | rótulo P |
| "vertical, de Q" | rótulo Q |
| "funções de x e de y" | linha `F(x, y) = (P, Q)` |
| "Neste campo" | `F = (−y, 2x)` e `P = −y, Q = 2x` |

**B1-1:** trocar "E o campo é liso, com derivadas parciais contínuas. É isso que deixa todas as contas de hoje funcionarem." por:
> E P e Q são lisas, com derivadas parciais contínuas. É isso que deixa todas as contas de hoje funcionarem.

**B2-2:** trocar "essa razão vira a derivada da componente vertical do campo na direção horizontal." por:
> essa razão vira a derivada do Q, a componente vertical, na direção x.

**B2-3:** trocar "Por isso a velocidade angular dele é menos a derivada da componente horizontal na direção vertical." por:
> Por isso a velocidade angular dele é menos a derivada do P, a componente horizontal, na direção y.

**B2-6:** trocar "A componente vertical é a coordenada horizontal, então a primeira derivada dá um. A componente horizontal é menos a coordenada vertical, então a segunda dá menos um." por:
> Aqui, o P é menos y, e o Q é x. Então a derivada de Q em x dá um, e a de P em y dá menos um.

Gatilho: "o P é menos y" escreve a linha `P = −y, Q = x`.

**B4-2:** trocar "A definição é a soma de duas derivadas: a da componente horizontal na direção horizontal, mais a da componente vertical na direção vertical." por:
> A definição é a soma de duas derivadas: a do P na direção x, mais a do Q na direção y.

**B6-0 (nova, abre o B6, antes do B6-1):**
> [thoughtful] E repara numa coisa: a definição do divergente não depende da dimensão. Um campo numa região aberta de ℝⁿ tem n componentes, de F um até F n, e o divergente é a soma das derivadas de cada componente na sua própria direção. No plano, as duas componentes são o P e o Q; no espaço, chega o R. Já o rotacional é coisa do espaço: o do plano é só o caso em que o R é zero e nada depende de z.

Gatilhos:

| Palavra | O que acontece |
|---|---|
| "região aberta de ℝⁿ" | linha 1 |
| "soma das derivadas" | o `div` geral |
| "No plano" | painel n = 2 |
| "no espaço" | painel n = 3 |
| "Já o rotacional" | as duas legendas do pé |

Na fala, "ℝⁿ" é lido como "erre ene".

**B6-1:** trocar "E no espaço? O divergente ganha uma terceira parcela, a derivada da componente de altura na direção da altura, e a caixa vira um cubo" por:
> No espaço, o divergente tem três parcelas, a terceira é a derivada do R na direção z, e a caixa vira um cubo

**B6-3:** depois de "com as derivadas parciais numa linha e as componentes do campo na outra.", acrescentar:
> Abrindo o determinante, a terceira componente é exatamente a do plano: derivada de Q em x, menos derivada de P em y.

Gatilho: "Abrindo o determinante" escreve a forma aberta; "a do plano" faz a 3ª componente piscar e mostra a legenda.

O resto da narração fica como no `narracao.md` do v3.

---

## 6. O que NÃO muda

Tudo o que o §1 lista como resolvido fica como está:
- o rio;
- o B3;
- os números do B4/B5;
- o F1/F2;
- o laplaciano (exceto N7 e N8);
- o S1–S3;
- o S4 (exceto a malha);
- o CTA;
- as cores, o canto e os capítulos.

Os capítulos só ganham o deslocamento de tempo das duas cenas novas.

---

## 7. Entregáveis do preview v4

1. `preview_yt0027_v4_960x540.mp4` (540p/15 fps). Rerenderizar **só** as seções afetadas, cada uma pelo seu `trecho`: B1, B2, B4, B5 (malha), B6, B7 e S4.
2. `renders/v4/qa/lado_a_lado_*.png` com os alvos 02, 07, 08, 11, 12, 13, 14, 15, 16 e 17.
3. `renders/v4/qa/sobreposicoes_v4.txt` com a regra R6 (amostragem a cada 0,2 s, transições, duplicatas): zero ocorrências, ou justificativa.
4. Folha de contato a cada 2,5 s e a lista de quadros vazios.
5. Capítulos atualizados (`capitulos_v4.txt`).
6. Relatório no formato do AGENTS.md: arquivos alterados, verificações, renders, alinhamento 3D (px), pendências. Diga explicitamente que N1–N8 e a malha foram conferidos quadro a quadro.

**Próxima etapa (não fazer agora):** com o v4 aprovado, vem o handoff final de voz (ElevenLabs v4 com tags), sincronia pela voz contínua, 1080p CRF 14, SRT, master e entrega em `entregas/`.
