# yt_0034 · CÁLCULO III · EP. 09 · Regiões gerais e troca de ordem
# AVALIAÇÃO DO PREVIEW v1 + HANDOFF v2 · preview silencioso (540p, 15 fps)

2026-11-13. Produção → Claude Code. Este documento é **autocontido**. Ele vale junto com:
- o handoff v1, que continua na unidade como `handoff_v1.md`;
- a pasta `yt_0034_quadros_alvo_v2/` do zip. Ela traz 14 quadros-alvo novos `v2_*.jpg`, a folha de contato e o gerador `sb34v2.html`, que contém as chaves v1 **e** as v2.

Onde este documento e o v1 divergirem, **vale este**.

Fase aberta: **preview visual silencioso v2**. Sem voz, SRT, 1080p, master, entrega, commit ou push.

O pedido do Kaio, nas palavras dele: *"quero algo bem didático e construído conforme os últimos vídeos, sem sobreposições, bastante visual, rigor matemático e diversão"*.

---

## 0. O que entregar

1. A mesma unidade `videos_longos/yt_0034_regioes_gerais_troca_ordem/`, com as mudanças deste documento.
   - Antes de mexer, copie o v1 para `renders/v1/`.
   - Não apague nada do v1.
2. `renders/v2/yt_0034_preview_v2_540p15.mp4`: 960×540, 15 fps, sem áudio, no tempo da narração v2.1 (§6).
   - Rerrenderize **só as seções que mudam**: `sec_h`, `sec_b1`, `sec_b2`, `sec_b4`, `sec_b5`, `sec_b6`, `sec_b7`, `sec_b8` e `sec_s`.
   - Remonte com `montar.py`.
   - `sec_a` e `sec_b3` ficam como estão. Mudam só se o tempo do B1-1 empurrar uma âncora; aí vale o resultado do `gerar_ancoras.py`.
3. `renders/v2/qa/`: tudo o que o §8 pede.
4. A prancha render × alvo, que tem duas fontes:
   - os 26 alvos v1, exceto os que os v2 substituem: 04, 05, 17, 18, 20, 22, 23, 25 e 26 (o 01 continua sendo o estado final do H1);
   - os 14 alvos v2.
5. O relatório de entrega do AGENTS.md.

---

## 1. Avaliação do v1

**O que o v1 acertou e não muda:**
- o sistema visual (fundo violeta, grade `papel(ax)`, canto, cores por grandeza);
- os pousos 3D → 2D (≤ 0,02 px);
- as tiras pintando o triângulo no B4-1;
- a diagonal e o espelho do B5;
- o telhado B₁/B₂;
- o metal leve em três pedaços;
- a parábola de dois ramos com a troca de cor no S2;
- o cartão do próximo (10,9 s);
- os 31 passos de glyph map;
- flash zero.

**O que falta para o pedido do Kaio** se divide em três problemas:

1. **Palco vazio ou parado enquanto a voz fala de uma ideia visual.**
   - **H1, 0:00–0:37:** uma fórmula pequena no centro de uma tela vazia. A ideia central do vídeo, "a primitiva não se escreve", não tem imagem.
   - **H1, 0:39–0:51:** eixos vazios.
   - **B1-2:** duas caixas vazias por ~20 s. O painel da fatia é minúsculo (200×40 px) e não está ligado a nenhuma tira do palco.
   - **B2-1, 4:51–5:09:** a região genérica parada enquanto a voz lê o enunciado.
   - **B4-3, 9:51–10:21:** só coluna, sem palco, por 30 s.
   - **B7-2:** uma linha por vez e miniaturas de 100×50 px.
   - **S1, 15:39–15:57:** só uma miniatura pequena no centro.
   - O QA registrou **52 trechos de 3–5 s** de palco parado, todos justificados. Mas a soma é o que o Kaio sente como "pouco visual".
2. **Sobreposições que o QA de repouso não pegou.**
   - Elas acontecem durante movimentos, ou com objetos que o QA não classificou como texto.
   - A lista está no §2.
3. **Um ponto de rigor (corrigido aqui):**
   - No B1-2 a voz diz "cada fatia vale zero, depois f, depois zero". Com R = [0, 2]² isso é falso para o quarto de disco: a fatia em x = 1 vale f e depois zero, com um salto só.
   - O v1 contornou isso com uma "fatia qualquer" desligada do desenho, e é por isso que o painel não conversa com o palco.
   - Correção no §3.2: R ganha uma folga embaixo. Assim a fatia **do desenho** é zero, f, zero e tem dois saltos, como diz a voz e como no Guidorizzi (R qualquer contendo B).

---

## 2. Correções (defeitos objetivos)

Cada item traz o quadro do v1, o arquivo, o problema, a correção e o aceite. Os quadros do v1 estão no zip, em `defeitos_v1/`.

| # | Tempo v1 | Arquivo | Problema | Correção | Aceite |
|---|---|---|---|---|---|
| D1 | 9:07–9:11 | `sec_b4.py` B4-2 (`pena(p2b, R2b, … extra=pal.anim(0.6, faca=1.0))`) | Na cena2 deitada, o plano da faca (contorno magenta) sai do quadro por cima e cruza o canto. | A faca da cena2 tem o tamanho da caixa do sólido + 10 %. Se precisar, recorte o polígono projetado ao retângulo do palco. | Em todo quadro, o polígono da faca fica em x ∈ [40, 1080] e y ∈ [150, 1040] (1080p). Novo item no QA (§8.4). |
| D2 | 12:39–12:45 | `sec_b6.py` (`fundo = ret_px(300,390,600,640…)`, `fundo2`) | Os painéis da fatia (`sen(x³)` e `SINO`) são desenhados **sobre o palco**, com fundo opaco. Eles tapam a parábola, a região e o rótulo `y = x²`. | Os dois painéis vão para a faixa de baixo da coluna, lado a lado (alvo `v2_10`), e ficam até o fim do B6-1. As linhas da coluna sobem (§4, B6). | A interseção de qualquer painel com a caixa da grade do palco é zero. |
| D3 | 13:45–13:57 | `sec_b7.py` B7-1b (`pes = … mixh(BG_, PESADO, .25)`) | O metal pesado (25 %) e o leve (`LEVE`) ficam com quase a mesma cor: não se vê qual parte é a "região". | Pesado a 8 % e rótulos `LEVE` e `PESADO` dentro da chapa (alvo `v2_11`). Os rótulos `CHEIA`/`1 CORTE`/`2 CORTES` vão para x = 2,12, porque em 2,06 encostam na borda. | Contraste leve × pesado ≥ 2:1 em luminância. Rótulo a ≥ 12 px de qualquer traço. |
| D4 | 16:39–16:45 | `sec_s.py` S2 | `x = 2 − √(4 − y)` fica à esquerda do eixo y e o cruza. O erro já estava no alvo 26 v1. | O rótulo vai para dentro da região, à direita do ramo azul-claro, em y = 2,4 (alvo `v2_14`). | Sem cruzamento rótulo × eixo × curva. |
| D5 | 10:45–10:57 | `sec_b5.py` B5-1 (`cima = regiao(..., BG_, .78)`) | O degradê da densidade deixa o triângulo de cima "meio apagado". Não fica claro qual metade é a região. | Opacidade de `cima` 0,86, contorno branco 3 px no triângulo de baixo, `B` dentro dele e `FORA` em GEO no de cima (alvo `v2_09`). | Leitura "região = triângulo de baixo" sem a voz. |
| D6 | 4:13–4:21 | `sec_b1.py` B1-3 (`rr = curva(...)` sobre `segs`) | O raio `2` é traçado por cima das 10 fatias âmbar e o rótulo `2` cai entre elas. | Em "a geometria já", as fatias vão a 25 % antes do raio. O raio vai a 60°, com o rótulo `2` (placa) fora das fatias. | Rótulo sem traço por baixo. |
| D7 | 6:03 | `sec_b2.py` B2-2 | `x = a(y)` encosta na curva azul-claro. | Afastar 16 px para dentro da região. À esquerda não cabe, porque cruzaria o eixo. | Folga ≥ 12 px. |
| D8 | 7:45 | `sec_b3.py` (`passo(H0, H1, voos=…)`) | Os dois voos (`y` e `√(4 − y²)`) cruzam um sobre o outro por ~0,5 s. | Aplique `lag` de 0,3 s entre os voos e `path_arc` de sinais opostos. | As caixas dos grupos em voo não se cruzam por mais de 2 quadros. |
| D9 | 9:39 | `sec_b4.py` B4-2, `PASSO 3: CALCULAR` | O triângulo fica sem eixos, ticks e rótulos (o palco perde a referência). | Os eixos, os ticks `1` e os rótulos `y = x`/`x = 0` continuam no palco durante o Passo 3. | — |
| D10 | 8:06 e 11:55 | montagem (`palco vazio`) | 2 trechos de palco vazio > 0,5 s (486,80–487,33 e 715,33–715,87). | Na troca de palco, o novo entra enquanto o velho sai (sobreposição de 0,3 s). | Zero > 0,5 s. |
| D11 | 15:30–15:36 | `sec_b8.py` | O cartão 3 (peça recortada) fica só ~1,5 s na tela antes do S1. | Ele entra em "Na engenharia", não em "peça recortada". | Cartão 3 inteiro ≥ 3 s. |

---

## 3. Mudanças de conteúdo (didática, visual, rigor)

### 3.1 H1 · a integral que trava ganha imagem (alvos `v2_01`, `v2_02`)

- **"Olha esta integral"**
  - A integral a caneta **direto na coluna** (x = 1120, 50 px), não no centro.
  - O palco já nasce com o gráfico de `f = e^(−y²)` em y ∈ [−2,2; 2,2]:
    - eixo horizontal y em magenta e vertical f em ciano;
    - a curva desenhada a caneta, da esquerda para a direita, em ~2 s;
    - a grade nascendo dos eixos.
  - Escala do alvo: 210 px por unidade em y e 420 px por unidade em f.
- **"precisa de uma primitiva de é elevado a menos ípsilon ao quadrado"**
  - Um ponto âmbar `x` no eixo (em y = 0,3) e a tracejada até a curva; o `1` com a tracejada.
  - A área entre x e 1 pinta em ciano 32 %, da esquerda para a direita.
  - Na coluna, `∫ₓ¹ e^(−y²) dy =` a caneta.
- **"E aí trava"**: o `?` em ALERTA dentro da área e no fim da linha, e a placa `SEM PRIMITIVA EM FÓRMULA`.
- **"nada de polinômio, seno, logaritmo, nada"**: três etiquetas com ✗, uma por palavra: `POLINÔMIO`, `SENO`, `LOGARITMO`.
- **"A conta de dentro não sai, e a de fora nem começa"**
  - O ponto `x` anda de 0,3 a 0,8 e volta a 0,3 (`ValueTracker`), e a área muda junto: a área existe, mas não tem fórmula.
  - É o único movimento "de exploração" do H1 e está amarrado à voz.
- **"com a ordem trocada"**
  - O gráfico sai (0,4 s) e o glyph map 1 roda na coluna, como no v1.
  - As etiquetas ✗ e a área saem com o gráfico.
- **"os limites mudaram"** (alvo `v2_02`)
  - Os eixos do triângulo nascem **junto** com as duas tiras: a em pé com `x` e `1`, a deitada com `0` e `y`.
  - A região ainda não aparece. Nunca há eixos vazios no palco.
- **"Ela mora num triângulo"**: a região e as arestas nascem, como no alvo 01 v1 (estado final).

### 3.2 B1 · R com folga e a fatia do desenho (alvos `v2_03`, `v2_04`, `v2_05`)

**Rigor:**
- R passa a ser **[0, 2] × [−½, 2]**, um retângulo tracejado com folga embaixo.
- B ⊂ R continua valendo, e agora a fatia em x = 1 atravessa R de y = −½ a y = 2:
  - zero em [−½, 0);
  - f em [0, √3];
  - zero em (√3, 2].
- São dois saltos (em 0 e em √3, onde f ≠ 0), exatamente como a voz diz.
- A palavra da voz no B1-1 muda (§6).

**B1-1 (alvo `v2_03`)**
- Grade de −½ a 2,2 em y. Ticks `−½` e `2` em y.
- Ticks `1` e `2` em x **com placa**, porque as tracejadas de R e da tira passam por eles.
- Três `0` em GEO: um no canto de fora do arco e dois na faixa de baixo. Nenhum `0` a menos de 0,15 de qualquer traço.
- "a fatia atravessa": a tira tracejada apagada vai de −½ a 2. Em "só soma zeros" a parte de B (0 a √3) acende cheia, e os dois trechos de fora ficam tracejados.
- Coluna: `∫_{−1/2}^{2} F(1, y) dy = ∫₀^√3 f(1, y) dy`. Os limites `−1/2` e `2` (magenta) voam dos ticks.

**B1-2 (alvos `v2_04` e `v2_05`), layout A-pequeno, com o palco a 170 px/unidade**
- **"duas coisas"** (alvo `v2_04`)
  - As duas caixas nascem **com o título em GEO** e um círculo vazio no lugar do ✓: `F INTEGRÁVEL EM R`, `FATIA INTEGRÁVEL`.
  - No gatilho de cada hipótese, o círculo vira ✓ menta e o título vai a branco.
  - Nenhuma caixa vazia.
- **"zero, depois f, depois zero"** (alvo `v2_05`)
  - A tira em x = 1 acende no palco (tracejada âmbar em R inteiro, cheia em B).
  - Ao mesmo tempo nasce o **painel grande** embaixo: x ∈ [170, 900] e y ∈ [760, 1030] no 1080p.
    - Legenda `UMA FATIA: x = 1` (linha mista).
    - Eixo horizontal y (magenta) de −½ a 2,3, com ticks `−½`, `0`, `√3`, `2`. Os ticks `0` e `√3` são os mesmos do palco.
    - Eixo vertical f (ciano) no −½.
  - Os três trechos a caneta, na ordem da voz: `0` (ciano, de −½ a 0), `f` (de 0 a √3) e `0` (de √3 a 2).
  - Os dois saltos tracejados em ALERTA e `DOIS SALTOS`.
  - O painel some só em "nada de especial do disco".
- O resto do B1-2 fica como no v1.

### 3.3 B2-1 · o enunciado com o palco andando (sem alvo novo; alvo 07 v1 = estado final)

O palco nasce como no v1 (eixos, grade). Depois, cada parte do enunciado mexe nele:
- **"Sejam cê e dê"**: `c` a caneta em azul-claro e `d` em coral, uma de cada vez, da esquerda para a direita.
- **"no intervalo fechado de á até bê"**: as tracejadas âmbar em `a` e `b` e os ticks.
- **"A região B é o conjunto dos pontos"**: a região pinta (GEO 18 %).
- **"tais que xis está entre á e bê"**: uma faixa vertical âmbar a 10 % pinta de a até b e some.
- **"e ípsilon está entre cê de xis e dê de xis"**:
  - um ponto P branco aparece em (1,1; meio da fatia), com tracejadas finas até os dois eixos;
  - ele sobe até `d(1,1)` e desce até `c(1,1)`, sem sair de B, em 2 s.
- **"As chaves"** e **"tais que"**: só os sublinhados da coluna (v1). O ponto P sai.
- O resto fica como no v1 (tira, pontos, selo).

### 3.4 B4-2 · o sino inteiro (alvo `v2_06`)

- Na cena2 em pé, a coluna ganha embaixo um painel `O SINO INTEIRO`: x ∈ [1150, 1860] e y ∈ [610, 930].
  - O gráfico 2D de `e^(−y²)` em [−2,5; 2,5], em ciano 75 %.
  - O pedaço de 0 a 1 em ciano cheio, com a área pintada, e o rótulo `O PEDAÇO DO SÓLIDO` em ciano à direita do título.
- Entra em "pedaço do sino" e sai junto com F0/F1.
- **Motivo:** a cena2 mostra só y ∈ [0, 1], e o sólido não parece um sino. O painel diz de onde vem o nome, e o "sino" volta no B8 como curva normal.
- Folga ≥ 30 px entre o painel e a placa 3D que sai pela direita.

### 3.5 B4-3 · o erro clássico ganha palco e um gráfico (alvos `v2_07`, `v2_08`)

Layout A (palco à esquerda, coluna em x = 1120), não mais coluna à esquerda e painel à direita.

- **"trocar só o dê ípsilon com o dê xis"**
  - Coluna: a forma errada `∫₀¹ ∫ₓ¹ e^(−y²) dx dy`, com o `x` do limite e o `dx` em ALERTA, e `SÓ TROCOU dx COM dy`.
  - Palco: o quadrado [0, 1]² com eixos e a reta `x = 1` em coral.
- **"Olha o que acontece. A integral de dentro passa a ser em xis, de xis até um"**
  - Uma tira deitada em y = 0,55 nasce de x até 1.
  - O começo dela é um ponto **âmbar** com o rótulo `x ?` em ALERTA. No eixo x, um ponto âmbar `x` com tracejada até a tira.
- **"ao mesmo tempo, a variável que anda e o limite dela"**
  - O `x` do eixo anda (0,45 → 0,15 → 0,75 → 0,45, `ValueTracker`, 2,4 s), e o começo da tira anda junto: a fatia não tem onde começar.
  - Ficam dois contornos tracejados GEO nas posições extremas, a seta dupla âmbar sob o eixo e `O COMEÇO ANDA COM x` em ALERTA (alvo `v2_07`).
  - Coluna: `x É LIMITE E VARIÁVEL`.
- **"sobra um xis solto no resultado"**
  - Glyph map da forma errada para `= (1 − x) · ∫₀¹ e^(−y²) dy`. O `(1 − x)` vem dos limites `x` e `1` (voo).
  - `RESULTADO COM x?` com ✗.
- **"a integral dupla é um número: não pode depender de xis"** (alvo `v2_08`)
  - O palco troca para o gráfico do "resultado" em função de x: eixo x âmbar de 0 a 1, eixo vertical `RESULTADO` em GEO.
  - A reta `(1 − x) · 0,7468` em ALERTA, a caneta.
  - Os pontos x = 0,2 (`0,597`) e x = 0,8 (`0,149`) aparecem um de cada vez.
  - A tracejada menta em `0,316` (o valor certo, do H1) e, na coluna, `UMA INTEGRAL DUPLA É UM NÚMERO` em menta.
- **"limite de dentro só pode depender da variável de fora"**: `DENTRO: SÓ A VARIÁVEL DE FORA` (GEO).
- **"Por isso a troca certa começa pela região"**
  - O gráfico sai. Volta o triângulo com a tira deitada correta (de 0 a y), e a forma certa `∫₀¹ ∫₀^y e^(−y²) dx dy` com ✓ na coluna.
  - O estado final é o do painel direito do alvo 17 v1, só que no layout A.

Números (conferidos): ∫₀¹ e^(−y²) dy = 0,746824…; 0,8 · 0,746824 = 0,59746 → `0,597`; 0,2 · 0,746824 = 0,14936 → `0,149`; (1 − 1/e)/2 = 0,31606 → `0,316`.

### 3.6 B6-1 · painéis fora do palco (alvo `v2_10`)

A coluna fica assim:
- `A` em 210;
- a linha mista `sen(x³) SEM PRIMITIVA EM FÓRMULA` em 300;
- `N1` (`x = √y ⇔ y = x²`) em 410.
  - Depois da troca de cor da parábola, `N1` sai (0,4 s) e `B1`, `B2`, `B3` sobem: `B1` em 400, `B2` em 505, `B3` em 615.

Os painéis:
- **"não depende de ípsilon"**: painel `ESTA FATIA` em (1120, 705, 350×300). O retângulo `sen(x³)` × `x²` a 300 px/unidade em y e 200 px/unidade em f.
- **"no sino o comprimento"**: painel `NO SINO` em (1510, 705, 350×300), com o retângulo `e^(−y²)` × `y`.
- Os dois ficam até o fim do B6-1. O `x²` do painel 1 voa para `B2`, como no v1.

### 3.7 B7-2 · quando vale trocar com miniaturas grandes (alvo `v2_12`)

- Três painéis de 360×200 à esquerda, um por motivo, e o texto de 40 px à direita, com uma linha de apoio de 28 px em GEO:
  - `O RETÂNGULO TRAZ O FATOR`;
  - `EM PÉ: DUAS · DEITADO: UMA`;
  - `DE 0 ATÉ x`, com `0` e `x` em MathTex.
- Cada linha nasce no seu gatilho ("Primeiro", "Segundo", "Terceiro"). A miniatura nasce antes do texto e anima uma vez:
  1. o retângulo cresce sob o sino;
  2. as duas tiras em pé acendem nas duas metades e depois uma tira deitada atravessa as duas;
  3. a tira em pé vai de 0 até a diagonal.
- Rodapé `MESMA REGIÃO, MESMO VALOR` em menta, em "o valor não muda".

### 3.8 S1 · síntese em três painéis (alvo `v2_13`)

- **Topo:** três painéis de 520×380, um por gatilho:
  - **"estende a função por zero"**: `ESTENDE POR ZERO`, a região genérica dentro de R com `0` fora e uma tira em pé;
  - **"no máximo dois saltos"**: `NO MÁXIMO DOIS SALTOS`, o gráfico 0 | f | 0;
  - **"virar um retângulo"**: `A FATIA VIRA RETÂNGULO`, o sino com o retângulo.
- **Meio:** a fórmula-tese das duas ordens, centrada (46 px), em "entra numa curva e sai em outra".
- **Embaixo:** três selos, cada um no seu gatilho:
  - `QUARTO DE DISCO: π` em "deu pi";
  - `TRAVADA: (1 − 1/e)/2` em "um menos um sobre é";
  - `TROCAR = RELER` em "reler a mesma região".

---

## 4. Diversão sem efeito

As mudanças acima trazem o jogo que faltava, sem partícula, brilho, sombra, pulso, lupa ou laço:
- **H1:** as famílias de funções riscadas uma a uma e a área que existe mas "não tem nome".
- **B4-3:** a fatia que não sabe onde começar e o "resultado" que muda com x.
- **B4-2:** o sino inteiro, que anuncia a curva normal do B8.

Nada mais deve ser acrescentado.

---

## 5. Palco parado

- Meta do v2: **trechos de 3–5 s ≤ 20**, nenhum > 5 s, e **zero** no H1, no B4-3, no B7-2 e no S1.
- O recurso é sempre amarrar o palco à fala:
  - acender no palco o objeto que a coluna está lendo (troca de cor por 1–2 s e volta);
  - a tira andar quando a voz percorre a região;
  - o ponto P do B2-1.
- Nunca use movimento decorativo.
- O PB4, com 12 trechos, cai sozinho com o B4-3 novo. Nos que sobrarem, o relatório traz o motivo, como no v1.

---

## 6. Narração v2.1 (uma frase muda)

Só o **B1-1** muda; o resto da narração v2 fica igual.

- **Antes:** "A fatia atravessa o retângulo inteiro, de ípsilon zero até ípsilon dois. Só que, depois que sai do disco, ela só soma zeros. Então a integral da fatia é a mesma de zero até onde ela sai do disco."
- **Depois:** "A fatia atravessa o retângulo inteiro, de ípsilon igual a menos meio até ípsilon igual a dois. Só que, fora do disco, ela só soma zeros: embaixo, antes de entrar, e em cima, depois de sair. Então a integral da fatia é a mesma de zero, onde ela entra no disco, até onde ela sai."
- A frase cresce +11 palavras, ≈ +3,7 s no B1-1. Reorce as âncoras com `gerar_ancoras.py` (3 palavras/s).
- **Gatilhos do B1-1:** "a fatia atravessa" → a tira tracejada de −½ a 2; "só soma zeros" → os trechos de fora apagam; "onde ela entra no disco" → ponto azul-claro em y = 0.
- O B1-2 continua "cada fatia vale zero, depois f, depois zero de novo", que agora é verdade para a fatia do desenho.
- Atualize `narracao.md` da unidade (Anexo A) com esta frase.

---

## 7. O que NÃO fazer

- Não mexer no que o v1 acertou (§1).
- Nada de partícula, brilho, sombra, pulso, lupa, laço contínuo, barra ou cronômetro. "Acender" é trocar a cor por 1–2 s e voltar.
- Nenhum painel ou fundo opaco por cima do palco.
- Nenhum número de episódio, livro ou Atlas na tela.
- Não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md`, `pyproject.toml`, `uv.lock` nem em outras unidades.
- Sem voz, SRT, master, 1080p, entrega, commit ou push.

---

## 8. QA do preview v2 (obrigatório)

1. **Render × alvo:** os alvos v1 que valem + os 14 v2, a 960×540, com tolerância de 10 px → `comparacao_v2.jpg` + `.txt`.
2. **Sobreposições**, como no v1, **mais**:
   - painel × palco (caixa da grade);
   - rótulo × eixo, curva e tracejada (folga ≥ 12 px);
   - objetos em voo (D8).
   O teste roda também **durante** as animações, a cada 0,2 s, não só no repouso.
3. **Palco parado/vazio:** `palco_parado_v2.txt` com as metas do §5. Palco vazio > 0,5 s: zero.
4. **3D × canto (novo):** em todo quadro das cenas 1 e 2, nenhum pixel do render 3D com alfa > 0 em y < 150 ou x > 1080 (1080p). Gere `3d_canto_v2.txt`.
5. **Flash por quadro, origens e glyph maps:** como no v1, com o glyph map novo do B4-3 ((forma errada) → `(1 − x) · ∫…`) listado.
6. **Números:** `0,597`, `0,149`, `0,316`, `−1/2`, `√3` e os do v1, conferidos.
7. **Texto:** R-texto (≤ 6 palavras, ≥ 26 px) nas linhas novas. `O COMEÇO ANDA COM x` e `UMA INTEGRAL DUPLA É UM NÚMERO` têm 5 e 6 palavras.

---

## 9. Parada

Entregue:
- o preview v2;
- as pranchas;
- os relatórios do §8;
- o relatório de entrega: arquivos alterados, verificações, caminho do preview e limitações.

Pare. Não inicie voz, SRT, 1080p, master nem entrega.

> **Próximo passo da Produção:** se o v2 chegar só com ajustes milimétricos, o retorno será o **HANDOFF FINAL** (correções + narração fechada + voz/sync + 1080p/entrega, numa vez só).
