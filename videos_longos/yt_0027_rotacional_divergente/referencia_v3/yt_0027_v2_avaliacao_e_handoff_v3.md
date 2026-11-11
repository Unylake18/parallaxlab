# yt_0027 · CÁLCULO III · EP. 02 · Rotacional e divergente
## Avaliação do preview v2 e HANDOFF v3 (para o Claude Code)

Data: 2026-11-11. Unidade: `videos_longos/yt_0027_*`. Fase: **preview visual v3** (540p/15 fps). Não gerar voz, SRT, master nem entrega nesta fase.

Este handoff **substitui o v2 só nos itens abaixo**. Todo o resto do v2 continua valendo: sistema visual (§2 do v2), 3D (§3), cena a cena (§4), mudanças de narração (§5), QA (§6). A narração-base continua sendo o Anexo A do v1 com as mudanças do v2 §5 e as deste v3 (§6).

Quadros-alvo v3: `yt_0027_quadros_alvo_v3/` (11 quadros + folha de contato + `00_v2_x_alvo_v3.jpg` + `00_sobreposicoes_no_v2.jpg`). Os geradores `sb27.html` (2D, `?k=<chave>`) e `c3d27.html` (3D, `?k=cubo3`) estão na pasta e servem de referência de geometria, cor e posição. As chaves novas são `b11, b13v3, b24v3, b52bv3, b61v3, f1v3, b73v3, b74a, b74b, s3, cta1`.

---

## 1. Avaliação do v2 (18:14)

O v2 melhorou muito. A escala está certa, as setas são regulares, não há partículas, os objetos de teste ficam presos, a coluna de fórmulas está organizada, e a física está como "campo × constante". O que falta agora é acabamento. Ficaram três cenas que não se explicam sozinhas (o cubo, o calor e o fechamento) e muitas sobreposições pequenas. Elas aparecem porque os rótulos e os objetos de teste ficam por cima das setas do campo, e porque linhas novas de fórmula são escritas por cima das antigas.

Pontos do Kaio, todos resolvidos neste handoff:

| # | Pedido do Kaio | Onde está a correção |
|---|---|---|
| K1 | O cubo com as setas saindo ficou feio | §3.3, alvo 05 |
| K2 | No começo, o vetor verde está apagado: usar um verde mais escuro ou outra cor só nessa representação | §3.1, alvo 01 |
| K3 | A narração falou rotacional e divergente, mas o terceiro ("deforma") ficou sem nada | §3.2 e §3.6, alvos 02 e 11 |
| K4 | Sobreposições no fim, quando escreve GREEN · STOKES · GAUSS | §3.5, alvo 10 |
| K5 | A repetição dos três cartões do começo no fim não precisa | §3.6, alvo 11 |
| K6 | Falta o gancho para o próximo vídeo, seguindo o mapa (Atlas) | §3.6 e §6 |
| K7 | O laplaciano virou "um quadrado laranja", não dá para entender | §3.4, alvos 08 e 09 |
| K8 | Umas 12 sobreposições além da do fim | §2, com 19 itens e a prancha `00_sobreposicoes_no_v2.jpg` |

Mea culpa: o "quadrado laranja" do calor e a repetição dos cartões vieram do meu handoff v2 e dos meus quadros-alvo (`b74`). O Claude Code seguiu o alvo. A correção está aqui.

---

## 2. Sobreposições: lista completa (tempos do preview v2)

A prancha `00_sobreposicoes_no_v2.jpg` mostra S01–S18 com o tempo no canto.

| # | Tempo v2 | Cena | O que sobrepõe | Correção |
|---|---|---|---|---|
| S01 | 3:13.8 | B2-2 | A 2ª linha `ω_AB = ∂Q/∂x` começa a ser escrita **em cima** da 1ª linha. As duas ficam encavaladas por ~1 s. | A 2ª linha nasce **abaixo** (y + 150 px), com `TransformByGlyphMap` a partir de uma cópia. Nenhuma fórmula é escrita sobre outra que ainda está na tela. |
| S02 | 4:08.8 | B2-4 | Os rótulos `1 rad/s` e `2 rad/s` e os raios tracejados ficam sobre as setas do campo, e a rodinha cobre os braços. | Usar clareira e placa (regra R1). Os rótulos ficam na ponta de fora de cada braço. A rodinha só entra depois que os braços saem. Ver alvo 03. |
| S03 | 4:38.8 | B2-5 | `⊙ k` e o arco violeta ficam sobre as setas. | Clareira de raio 1,35 u em volta da rodinha, cobrindo também o rótulo. |
| S04 | 5:13.8 | B2-6 | Uma barra azul **translúcida** vertical (marcador de raio) passa sobre as setas. A rodinha fica sobre as setas. | Tirar a barra: é transparência, e isso é proibido. Se precisar de referência de giro, basta a pá marcada da própria rodinha. Clareira em volta da rodinha. |
| S05 | 5:31.2 | B2-6 | `VORTICIDADE = 2ω (CORPO RÍGIDO)` fica espremido entre a linha das derivadas e a linha do rot, encostando nas duas. | Vai para uma linha própria abaixo de `ω = 1`, com 40 px de folga. |
| S06 | 6:13.8 | B3-1 | No mesmo ponto se empilham a rodinha, os braços tracejados, o arco violeta e as setas do campo. | Clareira de raio 1,0 u em volta da sonda. Os arcos de giro ficam fora da cruz. |
| S07 | 8:06.2 | B3-5/6 rio | As rodinhas da fileira do meio ficam **atravessadas** pelas setas, e a faixa violeta em degradê (preenchimento) cobre tudo. | As rodinhas ficam nas colunas entre as setas (deslocadas meio passo em x), com clareira. Tirar o degradê violeta e manter só os sinais `+`/`−` na margem e os arcos das rodinhas. |
| S08 | 9:51.2 / 10:13.8 | B4-4 | Os rótulos `h`, `k`, `x₀`, `x₀ + h` e as setas de fluxo das paredes ficam sobre as setas do campo. | Clareira em volta da caixa (caixa + 0,5 u). Rótulos com placa mínima. |
| S09 | 10:43.8 | B4-5 | `div F = 2 − x² − y²` é escrito **sobre** `div F = 2`, deixando duas fórmulas sobrepostas. A linha `(1, ½) … = 0,750` aparece fantasma. | Fazer a transformação no lugar (`TransformByGlyphMap` de `2` para `2 − x² − y²`), sem deixar a anterior. A linha do valor em `(1, ½)` entra só depois, inteira. |
| S10 | 11:06.2 | B4-6 | `div F = 0` e os contornos tracejados dos quadradinhos ficam sobre as setas. | Placa mínima e clareira. |
| S11 | 12:21.2 | B5-2 | Os números `0,927`, `0,219` e `0,490` ficam sobre as setas e grudados na caixa. | Ver alvo 04: clareira no retângulo da caixa e números afastados, cada um junto da sua seta. |
| S12 | 13:26.2 | B6-2 | Texto de depuração cinza `EIXO ALINHADO: 1,00 · DEITADA: 0`. | Remover. É debug, não é conteúdo. |
| S13 | 13:58.8 | B6-3 | A linha `div F` nasce espremida entre a linha do rot e as legendas violeta (DIREÇÃO/TAMANHO), que são do rot. | As legendas DIREÇÃO/TAMANHO vão logo abaixo do `rot F = ∇ × F`. A linha `div F = ∇ · F` vem por último, com 60 px de folga. |
| S14 | 14:26.2 | F1 | `FIO CARREGADO` fica sobre as setas. | Ver alvo 06: clareira no retângulo do rótulo e placa mínima. |
| S15 | 14:51.2 | F2 | `FIO COM CORRENTE` fica sobre as setas. | Mesma correção do F1. |
| S16 | 15:28.8 | B7-1 | As setas do gradiente passam por cima das curvas de nível e dos números 1, 2, 3, 4. | Ver alvo 07: setas em contexto (`#1A5F55`), números com placa e clareira em volta de cada número. |
| S17 | 16:06.2 | B7-3 | O `P` fica sobre o anel tracejado e sobre as setas. | Ver alvo 07: `P` abaixo do ponto, fora do anel, com clareira na região do ponto. |
| S18 | 17:51.2 | S3 | `GREEN · STOKES · GAUSS` é escrito **sobre** os dois painéis. | Ver §3.5 e o alvo 10. |
| S19 | 17:23.8 | S2 | Os círculos tracejados com `0` ficam sobre as setas, no canto dos painéis. | Clareira no círculo do `0`. |

### Regras que evitam a próxima rodada (valem para o vídeo inteiro)

- **R1 · Clareira.** Toda seta de campo cujo centro caia dentro do retângulo de um rótulo, de um número ou de um objeto de teste (rodinha, caixa, quadradinho, sonda) **não é desenhada** enquanto o objeto estiver ali. A margem é de 0,25 u. Ela volta com `FadeIn` quando o objeto sai. No Manim, é um filtro na hora de montar `campo7` (parâmetro `skip`), igual ao `clar()` do `sb27.html`.
- **R2 · Placa.** Todo rótulo solto sobre o desenho usa `placa_min` (`#091226` a 85 %, 4 px). É o mesmo `placa_min` do `v7.py` do yt_0026.
- **R3 · Fórmula nova não nasce sobre fórmula velha.** Ou a nova vai para a linha de baixo, ou a velha se transforma no lugar (`TransformByGlyphMap`/`TransformMatchingTex`) sem deixar cópia. A coluna de fórmulas começa sempre no alto (y ≈ 300), inclusive no B3 (no v2 a fórmula do vórtice ficou no pé da tela).
- **R4 · Rótulo de contador junto do objeto.** `ÁREA: 0,49 → 0,99` (B4-1) e `ÁREA DO PEDACINHO` (B5-2) ficavam no pé da coluna, longe do quadradinho. Passam a ficar na coluna logo abaixo da fórmula ativa, ou ao lado do objeto com placa.
- **R5 · QA automático de sobreposição.** Antes de entregar o v3, rodar uma checagem em cada gatilho: as caixas delimitadoras de todo texto e MathTex não podem se cruzar entre si, e nenhum texto pode cruzar uma seta de campo visível (centro da seta dentro da caixa do texto + 4 px). O relatório vai em `renders/v3/qa/sobreposicoes_v3.txt`, com zero ocorrências esperadas, e cada exceção precisa de justificativa.

---

## 3. Cenas reescritas

### 3.1 B1-1 · seta da velocidade (K2) · alvo 01

- **Só nesta cena**, o campo `(−y, 2x)` fica todo em **verde de contexto `#1A5F55`** (o verde escuro).
- O ponto de fluido que anda pela órbita (elipse tracejada GEO, fluxo exato `flT`) e a sua **seta de velocidade** ficam em **laranja `#E08A3C`**, a cor de ponto do projeto:
  - a seta tem 8 px de haste e 28 px de ponta, comprimento ≈ 0,3·|F| (≈ 110–130 px no lado direito da órbita);
  - o rótulo `\vec v` é laranja, com placa;
  - a seta acompanha o ponto e é sempre `F(ponto)`.
- Aplicar a clareira (R1) ao longo da seta e do rótulo, para nenhuma seta do campo cruzar a seta laranja.
- A coluna mostra `CAMPO = VELOCIDADE` e `\vec F = (−y, 2x)`.
- No B1-2 (lupa), o campo volta à cor normal.

### 3.2 B1-3 · os três cartões (K3) · alvo 02

- Os cartões ficam iguais aos do v2. Quando a fala nomeia, entram as tags:
  - `GIRA` ganha `ROTACIONAL` (violeta);
  - `MUDA DE ÁREA` ganha `DIVERGENTE` (azul-claro);
  - `DEFORMA` ganha **`NO FIM DA AULA`** (GEO).
- A narração ganha uma frase (§6) e a tag entra junto com ela.

### 3.3 B6-1 · cubo novo (K1) · alvo 05 · Three.js `cubo3`

O cubo do v2 tinha muitas setas por parede, cones vistos de frente (viravam "bolinhas"), luz/brilho e cubo pequeno. O cubo novo:

- **Campo e geometria:** `F = (x, y, z)` no cubo [1, 2]³. Em cada par de paredes entra 1 e sai 2, então a seta de saída tem o dobro do comprimento da de entrada. O saldo total é 3 = div F × volume (conferido no sympy, bloco V3).
- **Cubo:** a chapa `#1A2C52` translúcida a 32 % (sem escrever profundidade) e as arestas GEO. Sem luz, sem sombra, sem brilho: tudo em `MeshBasicMaterial` (cor chapada, como as colunas do yt_0026).
- **Setas:** **uma seta por parede**, no centro da parede, em cor chapada.
  - As de saída usam `#8CFFD2`, com comprimento 1,1. As de entrada usam `#2EE6A0`, com comprimento 0,55.
  - Haste r = 0,03; ponta: cone r = 0,095, altura 0,22.
- **Câmera do lado (+x, +y, +z)** (`ver([6.9, 5.1, 4.8])`, FOV 24°). As três paredes de saída ficam de frente com as setas longas. As de entrada ficam atrás, vistas através da chapa. Nenhuma seta aponta para a câmera, e as menores ficam com ≥ 0,8 do comprimento.
  - Movimento: um giro lento de ±10° em azimute durante a cena. Para no quadro do alvo quando a fórmula termina.
- **Pares de paredes coloridos:** uma moldura fina por dentro de cada parede, na cor do eixo: x âmbar `#FFC24D`, y magenta `#EA63FF`, z ciano `#35D9FF`.
  - Cada par **acende quando a parcela correspondente é escrita** (`∂P/∂x`, depois `∂Q/∂y`, depois `∂R/∂z`).
  - É o mesmo código de cores dos `∂x`, `∂y`, `∂z` da fórmula.
- **Coluna:** `div F = ∂P/∂x + ∂Q/∂y + ∂R/∂z` (CANETA), `CADA PAR DE PAREDES: SAI − ENTRA`, `SALDO POR UNIDADE DE VOLUME` e `CONTINUA SENDO UM NÚMERO`.
- Alinhamento 3D × Manim ≤ 2 px, como de costume (timeline com os centros das molduras, se houver rótulo preso).

### 3.4 B7-4 · calor que dá para entender (K7) · alvos 08 e 09

A cena vira um **gráfico de corte com a chapa embaixo, alinhada**:

- **Gráfico (em cima, x ∈ [−2,6; 2,6]):**
  - eixos GEO com `x` (âmbar) e `T` (azul-claro);
  - curva branca de 5 px: `T(x, 0, t)` da solução exata `T = 1 − (σ²/s)·e^{−r²/s}`, com `s = σ² + 4αt` e `σ² = 0,36`;
  - um vale no meio.
- **Ponto e vizinhos:**
  - `P` no fundo do vale, em laranja;
  - dois vizinhos em ±0,75, em GEO, ligados por um **segmento tracejado** com o rótulo `MÉDIA DOS VIZINHOS`;
  - uma **seta laranja de P até a média** com `SOBE`.
- **Chapa vista de cima (embaixo, mesma escala em x):**
  - mapa de cor `#4F8CFF` (frio) → `#F09A4A` (quente);
  - linha tracejada no meio marcando o corte;
  - rótulo `CHAPA VISTA DE CIMA`;
  - escala de cor com `FRIO`/`QUENTE`.
  - Agora o laranja tem legenda e um gráfico que explica.
- **Animação:** `4αt` vai de 0,06 a 0,5 em ~6 s. O vale se enche, a curva de `t = 0` fica tracejada com `ANTES`, a seta `SOBE` encurta e a mancha azul da chapa clareia (alvo 09). As bordas do vale descem um pouco: é física correta, o frio se espalha.
- **Coluna:** `∂T/∂t = α ∇²T` com `EQUAÇÃO DO CALOR`; `∇²T > 0 ⇒ T sobe`; `ABAIXO DA MÉDIA DOS VIZINHOS: ESQUENTA` (laranja); no fim, `E TAMBÉM: ONDAS, POTENCIAL ELÉTRICO…`.
- A cena dura ~14 s (no v2 eram ~4 s), com a fala nova do §6.

### 3.5 S3 · do local ao global, sem sobreposição (K4) · alvo 10

- `DO LOCAL AO GLOBAL` (Bold 56) no alto, com y ≈ 205.
- Os dois painéis do S2 encolhem para 620 × 500 e ficam em x = 250 e x = 1050, com y de 290 a 790.
- **Nome embaixo de cada painel, nunca por cima:**
  - à esquerda, `STOKES` (Bold 46) com a legenda `A VOLTA EM TORNO DO FIO`;
  - à direita, `GAUSS` com `A CERCA EM TORNO DO FIO`;
  - no pé, centralizado, `NO PLANO, OS DOIS VIRAM UM SÓ: GREEN` (GEO 32, y ≈ 995).
- Cada nome entra no gatilho da fala (§6).

### 3.6 S4 · a terceira coisa e o gancho (K3, K5, K6) · alvo 11

- **Sai** a repetição dos três cartões do B1 (K5).
- **Entra** o fechamento do "deforma":
  - canto `A TERCEIRA COISA`;
  - à esquerda, o campo `F = (x, −y)` (palco em (600, 560), 1 u = 110 px, passo 0,6, com clareira em volta do quadradinho);
  - um quadradinho coral de lado 1,2 no centro, deformado pelo **fluxo exato** `(x eᵗ, y e⁻ᵗ)` até t = 0,55: estica na horizontal, achata na vertical, a área não muda e ele não gira;
  - o contorno original fica tracejado.
- **Coluna:**
  - `F = (x, −y)`;
  - `rot F = 0` e `div F = 0` (CANETA, na fala);
  - `NENHUMA RODINHA GIRA` (violeta) e `NENHUM PEDACINHO MUDA DE ÁREA` (azul-claro);
  - `MAS O QUADRADINHO DEFORMA` (coral, 40);
  - `DESAFIO: ACHE OUTRO CAMPO ASSIM (NÃO CONSTANTE)` (GEO).
- Depois vem o CTA padrão do yt_0026: tudo sai, logo com os dois anéis girando, `INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS`, até o fim da fala + 3 s.
- **Gancho (K6):** só na narração, como no yt_0026 ("No próximo vídeo…"). O próximo tópico no mapa (Atlas, Cálculo III) é o **3.1-T3 · Limite, continuidade e derivadas parciais**. O gancho liga o "deforma" às derivadas parciais do campo, e é delas que sai a medida da deformação (texto no §6).

---

## 4. Melhorias gráficas gerais (padrões do yt_0026 finalizado)

1. **Sem quadro vazio nas trocas de seção.** No v2 há tela só com o fundo em 7:43.8, 11:28.8, 14:01–14:07 (≈ 5 s, e o canto some), 16:31.2 e 17:01.2 (painéis vazios). A cena seguinte entra enquanto a anterior sai (≤ 0,5 s de sobreposição de animação), como nas saídas de seção do yt_0026. O canto nunca some dentro do vídeo.
2. **Campo não nasce como "pontinhos".** Em 7:13.8 e 10:18.8 as setas crescem do comprimento zero e, por um instante, parecem pontos espalhados. Isso fica proibido. As setas entram com `FadeIn` já no comprimento final (com `LaggedStart` curto), ou `GrowArrow` a partir de 40 % do comprimento.
3. **Sem transparência e sem preenchimento decorativo:** a barra translúcida do B2-6 sai (S04), assim como o degradê violeta do rio (S07). O disco azul translúcido do mapa do divergente (B4-6) pode ficar, porque é dado (região div > 0), mas com as setas em contexto e o `+` fora das setas.
4. **Fórmulas e legendas na coluna, de cima para baixo** (R3), com a mesma folga entre linhas do yt_0026 (≥ 40 px entre a caixa de uma linha e a próxima).
5. **3D:** sem debug na tela (S12). As cenas 3D em material chapado (`MeshBasicMaterial`) seguem o padrão das colunas do yt_0026, sem cone de frente para a câmera.

---

## 5. O que NÃO muda

Hook, A1, B2 (exceto S01–S06), B3 (exceto S06/S07 e a posição da fórmula), B4, B5, B6-2/B6-3, F1/F2, B7-1 a B7-3 (exceto as clareiras) e S1/S2 ficam como no v2. Ficam também as cores, o canto, os capítulos e o ritmo.

---

## 6. Narração: mudanças do v3 (só as frases que mudam)

**B1-3:** trocar a última frase por:
> As duas primeiras ganham nome hoje: o giro é medido pelo rotacional, e a mudança de área, pelo divergente. A terceira, a deformação, fica guardada para o fim da aula.

**B7-4:** a fala inteira passa a ser:
> [curious] Agora olha uma chapa de metal com uma mancha fria no meio. No corte da chapa, a temperatura faz um vale. No fundo do vale, o ponto está abaixo da média dos vizinhos: o laplaciano é positivo, e esse ponto esquenta. O vale vai se enchendo. É assim que o laplaciano entra na equação do calor, e ele volta nas ondas, no potencial elétrico e em boa parte da física. Mas isso fica para mais à frente.

Gatilhos: "mancha fria" (chapa), "faz um vale" (gráfico), "abaixo da média dos vizinhos" (segmento e vizinhos), "esquenta" (seta SOBE), "vai se enchendo" (animação de t), "equação do calor" (fórmula).

**S3:** a fala inteira passa a ser:
> [thoughtful] E aí está a grande pergunta: como ligar o que acontece em cada ponto com o que acontece numa região inteira? Essa ponte entre o local e o global tem nome. A volta em torno do fio é assunto do teorema de Stokes; a cerca, do teorema de Gauss; e, no plano, os dois viram um só: o teorema de Green. Eles chegam mais à frente no Cálculo três.

Gatilhos: "Stokes", "Gauss" e "Green" (cada nome entra na sua palavra).

**S4:** a fala inteira passa a ser:
> [curious] E a terceira coisa lá do começo? Olha este campo: o x com o menos y. Faz a conta: o rotacional dá zero, e o divergente também, em todo ponto. Nenhuma rodinha gira, nenhum pedacinho muda de área… e mesmo assim o quadradinho estica para um lado e achata para o outro. Isso é a deformação. Desafio para os comentários: acha outro campo assim, que não seja constante, com rotacional zero e divergente zero. [excited] No próximo vídeo, a gente junta todas as derivadas parciais de um campo, e é delas que sai a medida dessa deformação. Se essa aula te ajudou, deixa o like e se inscreve no Parallax Lab. Até a próxima!

Gatilhos: "x com o menos y" (campo), "rotacional dá zero" e "divergente também" (CANETA das duas), "estica" (fluxo do quadradinho de 0 a 0,55 em ~2,5 s), "deformação" (`MAS O QUADRADINHO DEFORMA`), "Desafio" (legenda), "No próximo vídeo" (tudo sai, CTA).

Física conferida no sympy (bloco V3 de `verificacao/verifica_calc3_t2_sympy.py`, tudo True):
- rot e div de (x, −y) são zero;
- o fluxo exato preserva a área;
- o cubo de F = (x, y, z) tem saldo 3;
- a solução do calor resolve T_t = α∇²T, com ∇²T(0) = 4σ²/s² > 0.

---

## 7. Entregáveis do preview v3

1. `preview_yt0027_v3_960x540.mp4` (540p/15 fps). Rerenderizar **só** as seções afetadas: B1, B2, B3, B4, B5, B6, F, B7 e S. Na prática é quase tudo, mas cada seção pelo seu `trecho`.
2. `renders/v3/qa/lado_a_lado_*.png` com os 11 alvos v3, mais os 24 do v2 que não mudaram e que tocam as cenas corrigidas.
3. `renders/v3/qa/sobreposicoes_v3.txt` (R5): zero ocorrências, ou justificativa.
4. Folha de contato a cada 2,5 s, com uma lista de quadros vazios (esperado: nenhum).
5. Relatório no formato do AGENTS.md: arquivos alterados, verificações, renders, alinhamento 3D (px), pendências.
