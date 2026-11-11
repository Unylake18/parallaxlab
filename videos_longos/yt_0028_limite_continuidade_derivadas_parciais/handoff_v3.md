# yt_0028 · CÁLCULO III · EP. 03 · Limite, continuidade e derivadas parciais
# Avaliação do preview v2 e HANDOFF v3

Data: 2026-11-11. Base: preview v2 (`yt_0028_preview_v2_540p15.mp4`, 14:42) e o QA que veio junto.

---

# PARTE 1 · AVALIAÇÃO (para o Kaio)

## 1.1 Veredito

A v2 cumpriu o handoff:
- os 31 alvos foram reproduzidos (diferença de 4 a 7 em 255);
- sobreposições: zero; setas fora do painel: zero.

O problema é o que você viu: **o desenho briga com o fundo**. São dois motivos, medidos no preview:

1. **A grade passa por dentro dos desenhos.** Os painéis são só uma moldura, sem preenchimento. Então as linhas do milimetrado cortam cada seta de campo, cada disco ε, cada fórmula fina. Com 100 a 200 setas por tela, a grade vira ruído.
2. **Quase alinhado parece erro.** As molduras ficam a 5–20 px das linhas grossas da grade:

   | Elemento (v2) | Posição | Linha grossa mais próxima | Erro |
   |---|---|---|---|
   | Painéis B, borda esquerda | x = 130 e 1090 | 120 e 1080 | 10 px |
   | Painéis B, borda direita | x = 830 e 1790 | 840 e 1800 | 10 px |
   | Painéis B, topo e base | y = 260 e 820 | 300 e 780 | 40 px |
   | Cartões C | x = 140 e 1300; y = 250 e 710 | 120 e 1320; 300 e 660 | 20 a 50 px |
   | Escalas internas | 140, 170, 190, 200, 56 px/u | grade de 120 px | linhas e lados que não batem |

   A grade grossa fica em x = 0, 120, 240 … 1920 e y = 60, 180, 300 … 1020.

## 1.2 A solução: opaco só no desenho, e tudo encaixado na grade

As duas ideias que você sugeriu entram juntas:

- **Chapa opaca atrás de todo desenho.** Cada palco, painel e cartão vira uma chapa escura e opaca (`#060D1E`, um pouco mais escura que o fundo), com moldura fina. Dentro dela não tem grade. O campo, a mancha, a malha e o pedacinho ficam limpos.
- **Toda chapa nas linhas grossas.** As bordas caem exatamente nas linhas grossas. A grade só aparece nas margens e nos corredores entre chapas, e ali ela fica como moldura, alinhada.
- **Coluna de fórmulas sem grade.** Do lado das fórmulas, a grade termina numa linha grossa e a coluna fica lisa. Fórmula fina não fica mais cortada por linha.
- **Onde há gráfico com eixos, a grade é o papel.** Nos gráficos e nas arestas, não tem chapa: a origem fica num cruzamento grosso e a unidade é múltipla da grade. Fica assim:
  - as faixas |P − L₁| < ε e |Q − L₂| < ε caem nas linhas grossas;
  - nos gráficos de classe C¹, os eixos ficam em cima das linhas grossas;
  - o quadradinho das arestas tem 2 casas grossas de lado.

A prancha `00_antes_v2_depois_v3.jpg` mostra o mesmo momento nas duas versões (desafio ε-δ, derivadas no palco, três cartões e arestas).

## 1.3 Trechos parados que sobraram

A v2 ainda tem 7 trechos parados com mais de 6 s. A maioria cai onde o meu handoff v2 mandava "sem figura nova". Agora cada um ganha uma figura que explica o que a fala diz:

| Onde (v2) | Parado | O que entra na v3 |
|---|---|---|
| H, 0:43–0:56 | 13 s | **Alvo 02 novo.** Entram `∂F/∂x` e `∂F/∂y`. Depois, o P com três discos encolhendo: "chegar perto de um ponto". |
| B1, 3:01–3:18 | 16 s | **Alvo 05 novo: ponto de acumulação.**<br>• O P fica fora do domínio A, mas todo disco em volta dele tem ponto de A.<br>• O Q é de A, mas está sozinho: ninguém chega perto dele. |
| B2, 5:20–5:33 | 13,5 s | **Alvo 10 novo: "dá para chegar por uma curva"**, com o campo K = (x²y/(x⁴ + y²), 0).<br>• Por toda reta, a seta vai para 0.<br>• Pela parábola y = x², ela fica em 1/2.<br>• Então o limite não existe. |
| B3, 6:24–6:32 | 8 s | Sem alvo novo. No cartão ③, o L tracejado e a seta do ponto entram cada um na sua palavra. |
| B3, 6:37–6:52 | 15 s | **Alvo 13 novo: por componentes.**<br>• A primeira componente do nosso campo = constante + senos.<br>• O campo da carga = quociente, contínuo fora da carga.<br>• Soma, produto, quociente e composição. |
| B5, 10:16–10:30 | 14 s | **Alvo 22 novo: "o erro some".** É o erro dividido pelo passo:<br>• no nosso campo, 0,33 → 0,15 → 0,07, caindo pela metade;<br>• no encrenqueiro, 2 → 4 → 8, dobrando. |
| B7, 12:46–13:05 | 9 s + 8 s | **Alvo 34 novo.** Na palavra "atrito viscoso", o cartão DEFORMA ganha moldura lima e "O ATRITO VISCOSO VEM DAQUI". O cartão GIRA ganha moldura violeta e "GIRO RÍGIDO: SEM ATRITO VISCOSO". |

Os números novos foram conferidos no script: V17 a V21, **61 checagens, todas `True`**.

## 1.4 Outros ajustes de animação

- **1:16–1:24:** os dois painéis ficam vazios por ~5 s. Na v3, a chapa entra junto com o primeiro objeto dela, e nenhuma chapa fica vazia por mais de 0,5 s.
- **4:44–4:52:** o painel da direita fica vazio enquanto a fórmula polar é escrita. Mesma regra.
- **6:00:** a tela fica quase vazia (só a definição) por ~4 s entre os dois desafios do B3 e os cartões. Os cartões entram em "três jeitos de dar errado".
- **11:48–11:56:** os parênteses gigantes da matriz de movimentos aparecem sozinhos. Eles entram junto com a primeira célula.
- O "ZOOM × 10" e o "MODELO LINEAR LOCAL" saem de dentro do palco e ficam acima da chapa, sem placa.

## 1.5 Duração

A fala ganha 4 frases curtas (+119 palavras), que cobrem as figuras novas. A estimativa vai de 14:42 para **~15:25**.

Se quiser ficar abaixo de 15 min, dá para cortar a frase e a metade do Q no ponto de acumulação (−7 s) e os dois exemplos do B3 (−13 s). Fica com você. O handoff manda não cortar sem a sua decisão.

---

# PARTE 2 · HANDOFF v3 (para o Claude Code)

**Fase:** só o **preview visual silencioso** do vídeo inteiro, em 960×540 a 15 fps. Não gerar voz, SRT, master, 1080p de vídeo nem entrega. Não fazer commit nem push.

Unidade: `videos_longos/yt_0028_limite_continuidade_derivadas_parciais/` (já implementada na v2). Preserve a v2 em `renders/v2/`.

**O handoff v2 continua valendo em tudo o que este não muda:**
- matemática, cores, caneta, regras R1 a R6;
- tamanhos mínimos;
- cena a cena da v2.

Este documento traz o sistema de chapas, as posições novas, 6 cenas novas e a narração v3 completa (Anexo A).

Vem junto (zip `yt0028_handoff_v3_completo.zip`):
- `yt_0028_quadros_alvo_v3/`: **37 quadros-alvo** 1920×1080, a `00_folha_contato.jpg`, a `00_antes_v2_depois_v3.jpg` e o gerador `sb28v3.html` (Canvas + KaTeX, `?k=<chave>`; `&z=0` desliga as zonas de texto). Junto, na mesma pasta: `katex/`, as fontes, o `fundo.png` e o `logo_crop.png`. O gerador tem as coordenadas exatas de tudo.
- `verificacao/verifica_calc3_t3_sympy.py` e a saída: **61 checagens `True`**. O bloco novo é o V3 (V17–V21).

A matemática, o roteiro e os textos estão aprovados pelo Kaio. Não rediscuta. Se encontrar uma inconsistência objetiva, reporte antes de mudar. Por exemplo, a grade do `assets/calculo/papel.py` não estar em x = 960 ± 120k e y = 540 ± 120k no 1080p.

## 0. O que entregar

1. As seções alteradas (`sec_*.py`) e a `ficha.md` (§1).
2. O preview inteiro, `renders/v3/yt_0028_preview_v3_540p15.mp4`, com a duração da narração do Anexo A (~15,4 min).
3. A prancha **render × alvo** dos 37 quadros, `renders/v3/qa/comparacao_v3.jpg`, mais o `.txt`.
4. Os relatórios em `renders/v3/qa/`:
   - **`alinhamento_v3.txt` (novo, §9.2);**
   - `sobreposicoes_v3.txt` (R5);
   - `setas_na_chapa_v3.txt` (R7, que substitui o R6);
   - `holds_v3.txt`.
5. A prancha `antes_depois_v3.jpg`, com os mesmos 4 momentos da `00_antes_v2_depois_v3.jpg`, mas renderizados.
6. O relatório de entrega (AGENTS.md).

## 1. Ficha (o que muda)

```
duracao_alvo: ~15,4 min (aguarda decisão do Kaio se passar de 15:00)
quadros_alvo: yt_0028_quadros_alvo_v3 (37)
sistema_visual: chapas opacas nas linhas grossas (v3); papel só em gráfico/aresta
```

## 2. Sistema visual v3

### 2.1 A grade (referência)

- Fundo milimetrado parado, como na v2.
- Linhas grossas no 1080p: **x = 120k** (0, 120 … 1920) e **y = 60 + 120k** (60, 180 … 1020).
- Linhas finas a cada 24 px.
- Conversão para o Manim: x_m = (x_px − 960)/135 e y_m = (540 − y_px)/135. Uma casa grossa = 120/135 = **0,8889 u** do Manim.
- Linhas grossas em unidades do Manim: x_m = 0,8889·j e y_m = 0,8889·i, com i e j inteiros. A origem do Manim é um cruzamento grosso.

### 2.2 Chapa (novo)

| Propriedade | Valor |
|---|---|
| Forma | `RoundedRectangle`, raio 8 px (0,059 u) |
| Preenchimento | `#060D1E`, opacidade 1 |
| Moldura | `#B8C4DA` com opacidade 0,30, ~2 px no 1080p |
| Cantos | os 4 em cruzamentos de linhas grossas, **erro ≤ 1 px no 1080p** |
| Ordem z | fundo < chapa < tudo o que fica dentro dela |

- **Entrada:** junto com o primeiro objeto dela (`FadeIn` de 0,4 s no mesmo `AnimationGroup`).
- **R8 · chapa vazia:** nenhuma chapa vazia por mais de 0,5 s.
- **Persistência:** a chapa fica parada enquanto o layout não muda. Entre alvos do mesmo layout (ex.: 03 → 04 → 05 → 06), só o conteúdo troca.
- **Saída:** junto com o conteúdo.
- **Sem efeitos:** a chapa não brilha, não pulsa e não tem sombra.

### 2.3 Zona de texto (novo)

Retângulo sem moldura, da **cor do fundo** (`#091226`, opaco), que esconde a grade atrás de colunas e linhas de fórmulas. As bordas ficam em linhas grossas (a zona começa 1 px para dentro, para a linha grossa da borda continuar visível). Ordem z: fundo < zona < texto. A zona entra e sai com o layout.

| Layout | Zona (px, 1080p) |
|---|---|
| A (palco + coluna) | x 1080–1920, y 180–1020 |
| B (dois painéis) | x 120–1800, y 900–1020 (linha de fórmulas de baixo) |
| C (três cartões) | x 120–1800, y 780–1020 (títulos, subtítulos e fórmulas) |
| Alvo 07 (sombras, papel) | x 1080–1920, y 180–1020 |
| Alvo 20 (gráficos C¹, papel) | x 120–1800, y 900–1020 |
| Alvo 30 (matriz de movimentos) | x 1200–1920, y 180–1020 |
| Alvo 31 (arestas) | x 840–1920, y 180–1020 |
| Alvo 13 (componentes, página) | x 120–1800, y 180–1020 |

As fórmulas de **topo** dos layouts B (alvos 03, 06, 09, 10, 11) sobem para **y = 135** (acima das chapas) com a placa mínima R2 atrás. O mesmo vale para `4 NÚMEROS ENTRAM…`, em **y = 245**.

### 2.4 Layouts v3 (px no 1080p)

| Layout | Chapas | Conteúdo |
|---|---|---|
| **A** palco + coluna | 1 chapa x 120–1080, y 180–900 | Palco com origem (600, 540) e 120 px/u (sem mudança).<br>Rede de setas: passo 0,5 u, x ∈ [−3,5; 3,5] e y ∈ [−3; 3], filtrada pela R7. Na prática, as linhas ficam de −2,5 a 2,5.<br>Coluna de fórmulas em x = 1110–1120, como na v2. No alvo 17 a coluna sai de 1090 para **1110**, e as linhas "= (…)" saem de 1150 para 1170. |
| **B** dois painéis | 2 chapas 720×720: x 120–840 e 1080–1800, y 180–900 | Centros e escalas internas iguais aos da v2: esquerda (480, 540) a 140 px/u; direita como cada alvo.<br>Nomes (`ONDE VOCÊ ANDA` …) em y = 868, **dentro** da chapa.<br>Fórmulas de baixo em y ≈ 955–975, na zona. |
| **C** três cartões | 3 chapas 480×480: x 120, 720 e 1320; y 300–780 | Centros **(360 \| 960 \| 1560, 540)**, 56 px/u. Os centros x mudam de 380/960/1540 para 360/960/1560, e o y de 480 para 540.<br>Títulos em y ≈ 830–835; subtítulos em y ≈ 880.<br>Fórmulas dos alvos 32–34 em y ≈ 912, valores em y ≈ 995. A definição do alvo 12 em y ≈ 962. |

Como a chapa é opaca, a escala **dentro** dela é livre: 140, 200 e 56 px/u continuam. O que precisa encaixar é a chapa.

### 2.5 Papel: cenas sem chapa, presas na grade

| Alvo | Origem (px) | Escala | O que cai nas linhas grossas |
|---|---|---|---|
| 07 · sombras (B1-7) | (600, 540) | **240 px/u** (era 170) | Faixas \|x\| ≤ 1 (y de −1,5 a 1,5) e \|y\| ≤ 1 (x de −2 a 2): bordas em x = 360/840 e y = 300/780. Disco ε com raio 240 px; disco √2·ε com 339 px. Coluna em x = 1130. |
| 20 · classe C¹ (B5-3) | (480, 540) e (1440, 540) | 120 px/u | Eixos em cima das linhas grossas. **Sem moldura de painel.** Nomes em y = 868, no papel. |
| 30 · matriz de movimentos (B7-1) | quinas das células em (480, 420), (960, 420), (480, 780) e (960, 780) | **120 px/u** (era 130) | Lados de 1 u = 1 casa grossa. Parênteses em x = 390 e 1170 (y 280–920); matriz J em x = 1290; legendas em x = 1294. |
| 31 · arestas (B7-2) | quina em (360, 780) | **150 px/u**, S = 1,6 | Aresta de 240 px: x 360–600 e y 540–780. Coluna em x = 940, na zona. |

### 2.6 Regras novas

- **R7 · seta inteira na chapa (substitui a R6):**
  - toda seta de campo, curva, mancha e rótulo de um desenho fica a **≥ 18 px** da moldura da sua chapa, em todo quadro;
  - seta de rede que não cabe **não é desenhada** (a rede fica simétrica: as linhas e colunas que sobram têm a mesma folga dos dois lados);
  - verificação quadro a quadro, em todos os blocos com chapa → `setas_na_chapa_v3.txt`, com zero esperado.
- **R8 · chapa vazia ≤ 0,5 s** (§2.2).
- **R9 · alinhamento:** cantos das chapas, origens de papel e bordas de faixa a ≤ 1 px da linha grossa no 1080p (§9.2).

## 3. Cena a cena (só o que muda)

**Alvo NN** = quadro de `yt_0028_quadros_alvo_v3/` (tolerância de ±20 px na posição e ±5 % no tamanho; o mesmo texto e as mesmas cores). Gatilho = palavra do Anexo A.

Em **todos** os alvos antigos (01, 03, 04, 06–09, 11, 12, 14–21, 23–33, 35–37):
- aplicar as chapas, as zonas e as posições do §2;
- o conteúdo e o tempo são os da v2;
- a única mudança de texto: o alvo 12 (B3-2) perde a legenda `CONTÍNUA ⇔ CADA COMPONENTE É CONTÍNUA`, que vira a primeira linha do alvo 13.

### H · gancho (alvos 01 e 02)
- **Alvo 01:** palco na chapa A, e a coluna na zona.
- **Alvo 02 (novo, H-4)**, trecho "Então tem alguma coisa nesse campo…" até "chegar perto de um ponto". Gatilhos:
  1. "Que número mede isso?": `QUE NÚMERO MEDE ISSO?` (SG 40, branco). As linhas `F = …`, `rot`, `div` e `MAS DEFORMA` saem antes.
  2. "nas derivadas parciais": a legenda `A RESPOSTA: AS DERIVADAS PARCIAIS` (GEO 30) e, com a caneta, `∂F/∂x    ∂F/∂y` (48 px).
  3. "começar pelo chão": o pedacinho e o fantasma saem (0,6 s), e o campo vai para a cor de contexto `#1A5F55` (0,8 s), com clareira de raio 1,05 u no centro.
  4. "chegar perto de um ponto":
     - P cheio no centro (laranja, 10 px);
     - três círculos tracejados laranja (2,5 px, traço 8/8) de raios 0,95, 0,6 e 0,3 u, criados do maior para o menor (0,5 s cada);
     - `MAS ANTES, O CHÃO:` (GEO 30) e `CHEGAR PERTO DE UM PONTO` (SG 38, laranja `#E08A3C`).
  - Corte para o A.

### B1 · chegar perto (alvos 03, 04, 05, 06 e 07)
- **03, 04 e 06:** chapas B. O `∀ε > 0  ∃δ > 0` e a definição do topo vão para y = 135 com placa. O recorte da mancha que vaza usa a chapa da direita (x 1080–1800, y 180–900).
- **Alvo 05 (novo, B1-5 · ponto de acumulação)**, entre "Aliás, o ponto nem precisa estar no domínio" e "Agora sim, escrito". As chapas B ficam; o conteúdo troca. Gatilhos:
  1. "nem precisa estar no domínio":
     - o campo e os discos do painel esquerdo saem;
     - entra o domínio **A**: disco de centro (−0,75; 0) e raio 1,45 u (unidades do painel, 140 px/u), com preenchimento `#2EE6A0` misturado 84 % com `#060D1E` (opaco) e borda menta tracejada (2 px, 9/8);
     - **P vazado** em (0,7; 0), na borda e fora de A, e o rótulo `A` (40 px).
  2. "tão perto dele quanto você quiser":
     - três discos tracejados laranja em volta de P, de raios 1,0, 0,6 e 0,3 u, do maior para o menor;
     - cada um com um ponto branco (6 px) de A dentro, em P + 0,72r·(cos φ, sen φ), com φ = 2,75, 2,95 e 3,05 rad;
     - no alto da chapa: `TODO DISCO EM VOLTA DE P` / `TEM PONTO DE A` (SGM 26, branco).
  3. "ponto de acumulação": o nome `P: PONTO DE ACUMULAÇÃO` em y = 868 e, embaixo, com a caneta: `P de acumulação de A:  ∀δ > 0, ∃X ∈ A, 0 < ‖X − P‖ < δ`.
  4. "sozinho, sem vizinhos", na chapa da direita (origem (1440, 540), 140 px/u):
     - um pedaço de A: disco de centro (−1,45; −0,3), raio 1,45;
     - **Q** cheio (menta, 9 px) em (1,1; 0,85), com o disco de raio 0,5 (GEO 90 % opaco, borda laranja tracejada);
     - o texto `Q É DE A, MAS ESTÁ SOZINHO:` / `NINGUÉM CHEGA PERTO DELE`;
     - o nome `Q: PONTO ISOLADO`.
  5. "Agora sim, escrito": o conteúdo do 05 sai, e entra o 06 (a definição). As chapas continuam.
- **Alvo 07:** papel a 240 px/u (§2.5).

### B2 · quando o limite não existe (alvos 08, 09 e 10)
- **08:** chapa A. **09:** chapas B, e a forma polar no topo em y = 135.
- **Alvo 10 (novo, B2-4 · a curva)**, depois de "porque dá para chegar por uma curva". As chapas B ficam. Gatilhos:
  1. "Olha este campo":
     - no topo, com a caneta, `K = (x²y/(x⁴ + y²), 0)` no lugar da forma polar;
     - no painel esquerdo, o campo K em cor de contexto (setas horizontais e proporcionais, desenhadas com 2·K porque |K| ≤ 1/2);
     - as retas tracejadas GEO y = x, y = −x e y = 0, mais o rótulo `y = mx`.
  2. "por qualquer reta, a seta vai para zero":
     - X anda pela reta y = x de (1,2; 1,2) até ~0,05 da origem (2 s);
     - no painel direito (origem (1440, 560), 140 px/u, segmento de −1 a 1 com marcas −1, 0, 1/2 e 1), a seta K(X) encolhe até 0;
     - legenda `PELAS RETAS: A PONTA VAI PARA 0` (GEO).
  3. "pela parábola":
     - a parábola y = x² (laranja, 4 px, x de −1,3 a 1,3) e o rótulo `y = x²`;
     - X anda por ela de x = 1,3 até x = 0,15 (2,5 s), e a seta do painel direito fica **parada em 1/2**;
     - legenda `PELA PARÁBOLA: FICA EM 1/2` (laranja).
  4. "Também não tem limite": embaixo, `TODA RETA DÁ 0, A CURVA DÁ 1/2: O LIMITE NÃO EXISTE`.
  - Números: V17 e V18.

### B3 · continuidade (alvos 11, 12 e 13)
- **11:** chapas B, e o `① ② ③` em y = 150 com placa.
- **12:** cartões C (§2.4).
  - Os cartões entram em "três jeitos de dar errado". A tela não fica vazia entre o 11 e o 12.
  - No cartão ③, o L tracejado entra em "O limite existe e é a seta para a direita", e a seta do ponto (para cima) em "a seta do ponto é outra". Antes elas entravam juntas, o que dava o parado de 8 s.
- **Alvo 13 (novo, B3-3 · por componentes)**, página limpa (zona x 120–1800, y 180–1020, sem chapa). Os cartões saem em "E, de novo, por componentes". Gatilhos:
  1. "cada componente é contínua": `F = (P, Q) contínuo ⟺ P e Q contínuas` (46 px, y = 270).
  2. "somas, produtos, quocientes … e composições": `SOMA · PRODUTO · QUOCIENTE (DENOMINADOR ≠ 0) · COMPOSIÇÃO` (SG 32, menta, y = 880) e `DE FUNÇÕES CONTÍNUAS CONTINUAM CONTÍNUAS` (GEO 28, y = 935).
  3. "constante mais senos": `P = 1 + sen x − sen y` (48 px, y = 450) com chaves por baixo (`constante`, `composição`, `composição`, em GEO).
  4. "o campo da carga é um quociente": `E = (x/(x² + y²)^{3/2}, y/(x² + y²)^{3/2})` (44 px, y = 640) e a legenda `QUOCIENTE: CONTÍNUO ONDE O DENOMINADOR NÃO É ZERO, OU SEJA, FORA DA CARGA` (GEO 26).

### B4 · derivada parcial (alvos 14 a 17)
- **14, 15 e 16:** chapas B. O `ΔF = …(corda)` do 14 fica dentro da chapa da direita, no alto (y = 215).
- **17:** chapa A, com a coluna em x = 1110 (§2.4).

### B5 · o engano (alvos 18 a 22)
- **18:** chapa A. **19 e 21:** chapas B. **20:** papel (§2.5).
- **Alvo 22 (novo, B5-5 · o erro some)**, depois de "com um erro que some mais rápido que o passo". As chapas B ficam. Gatilhos:
  1. "O nosso campo, feito de senos e cossenos, é cê um": o conteúdo do 21 sai, e o nome da esquerda vira `NOSSO CAMPO: CLASSE C¹`.
  2. "O encrenqueiro, não": o nome da direita vira `O ENCRENQUEIRO: NÃO É C¹`.
  3. "dividindo o erro pelo passo": no alto das duas chapas, `ERRO ÷ PASSO: CAI PELA METADE` (menta) e `ERRO ÷ PASSO: DOBRA → ∞` (ALERTA). Embaixo, com a caneta: `‖erro‖/‖H‖ → 0 quando H → 0`.
  4. "quando o passo cai pela metade":
     - na esquerda (origem (480, 640), 140 px/u, base GEO de x = −2,1 a 2,1), três setas menta **verticais** em x = −1,4, 0 e 1,4;
     - alturas 0,33·4,2, 0,145·4,2 e 0,068·4,2 u, uma por vez (`GrowArrow`, 0,6 s);
     - embaixo de cada uma, `passo 0,5`, `passo 0,25` e `passo 0,125`; em cima, `0,33`, `0,15` e `0,07`;
     - em "vai para zero", `→ 0`.
  5. "ela dobra":
     - na direita (origem (1160, 540), 70 px/u), três setas ALERTA **horizontais**, de comprimentos 2, 4 e 8 u, nas alturas 2,2, 0 e −2,2, uma por vez;
     - rótulos `passo 0,5 / 0,25 / 0,125` em cima e `2 / 4 / 8` na ponta.
  - Números: V19 e V20.
  - O erro é F(P + H) − F(P) − h·∂F/∂x − k·∂F/∂y (o que sobra da aproximação do alvo 21), no máximo sobre ‖H‖ = passo.

### B6 · a tabela (alvos 23 a 29)
- Chapa A em todos.
- `ZOOM × 10` e `MODELO LINEAR LOCAL` vão para **fora da chapa**, acima dela: `ZOOM × 10` centrado em (190, 152), 28 px; `MODELO LINEAR LOCAL` em x = 290, y = 162 (SGM 26, GEO), sem placa.

### B7 · quatro números, quatro medidas (alvos 30 a 36)
- **30:** papel (§2.5). Os parênteses entram **junto com a primeira célula**, não antes.
- **31:** papel a 150 px/u (§2.5). A linha def₁ é escrita em dois tempos: `estica_H − estica_V` em "estica mais numa direção", e o `= 1 − 0 = 1` em seguida.
- **32 e 33:** cartões C.
- **Alvo 34 (novo, B7-4b · atrito viscoso):**
  - em "o atrito viscoso vem da deformação": a moldura do cartão DEFORMA vira **lima `#C6F26B`, 4 px**, e entra no alto dele `O ATRITO VISCOSO VEM DAQUI` (SGM 22, lima, y = 334);
  - em "girando inteiro, rígido": a moldura do cartão GIRA vira **violeta `#9C8CFF`, 4 px**, e entra `GIRO RÍGIDO: SEM ATRITO VISCOSO` (violeta);
  - troca de cor da moldura com `stroke` direto (0,3 s), sem brilho e sem pulso.
- **35 e 36:** chapa A.

### S · resumo (alvo 37)
Chapa A, e a coluna na zona. O resto é como na v2.

## 4. Números novos (script, bloco V3)

| # | Conta | Valor |
|---|---|---|
| V17 | K = x²y/(x⁴ + y²) em y = m x, com x → 0 | 0, para todo m (e 0 nos eixos) |
| V18 | K na parábola y = x² | 1/2 em todo ponto (x ≠ 0) |
| V19 | Nosso campo: máx ‖F(P + H) − F(P) − J·H‖/‖H‖ com ‖H‖ = 0,5 · 0,25 · 0,125 | 0,33 · 0,15 · 0,07 (o máximo é em H = (−passo, 0)) |
| V20 | Encrenqueiro: parciais 0, então máx ‖G(H)‖/‖H‖ | 2 · 4 · 8 (em θ = 45°) |
| V21 | P = (0,7; 0) na borda do disco aberto A (centro (−0,75; 0), raio 1,45) | P ∉ A, e todo disco em volta de P toca A |

## 5. Holds

`holds_v3.txt`: todo trecho parado > 3 s com motivo, e **nenhum > 6 s**. As únicas exceções aceitas são o S (resumo falado, com o 1,5 s parado antes do CTA) e o B6-2 (6,2 s), cada uma com motivo escrito. Os 7 trechos do §1.3 precisam sumir.

## 6. Narração e tempo

A narração é a do Anexo A (v3 = v2 + 4 frases, marcadas com ▶ no Anexo só para referência; o ▶ não é falado). O preview continua silencioso, com cada bloco durando o tempo estimado da fala (~0,37 s por palavra, como medido na v2).

| Bloco | Palavras | Duração estimada |
|---|---|---|
| H + A | ~210 | ~1:16 (sem mudança) |
| B1 | 491 (+18) | ~3:01 |
| B2 | 259 (+32) | ~1:36 |
| B3 | 247 (+32) | ~1:31 |
| B4 | 319 | ~1:54 |
| B5 | 321 (+37) | ~1:58 |
| B6 | 217 | ~1:18 |
| B7 | 332 | ~2:01 |
| S + CTA | 135 | ~0:52 |
| **Total** | **~2.506** | **≈ 15:25** |

Se passar de 15:00, avise no relatório e **não corte nada**: o corte é decisão do Kaio. Não gerar voz.

## 7. O que NÃO fazer

- Nenhum 3D, partícula, lupa, laço contínuo, brilho, sombra, pulso, contorno ou transparência em seta, nem barra.
- Chapa sem efeito nenhum (só preenchimento e moldura).
- Não pôr grade nova dentro das chapas nem mudar o `fundo`.
- Não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md` nem nas unidades yt_0026 e yt_0027.
- Não citar livro nem o Atlas na tela.
- Não gerar voz, SRT, master, 1080p de vídeo nem entrega. Não fazer commit nem push.

## 8. Implementação (sugestão)

- Um helper na própria unidade, por exemplo `chapa(x0_px, y0_px, x1_px, y1_px)`, que converte px → Manim (§2.1) e **falha com `assert`** se algum canto não estiver numa linha grossa (x % 120 == 0 e (y − 60) % 120 == 0).
- O mesmo vale para `zona(...)` e para a origem dos papéis.
- Um filtro `cabe(seta, chapa, folga=18 px)` na construção das redes de setas (R7).
- Nada disso vai para `template/` nem para `assets/`: fica na unidade.

## 9. QA do preview (obrigatório)

1. **Render × alvo (37):** um still no estado completo de cada alvo, comparado a 960×540 (tolerância de 10 px nessa escala), em `comparacao_v3.jpg` + `.txt`.
2. **Alinhamento (novo) → `alinhamento_v3.txt`:**
   - renderize **em 1080p só os stills** dos 37 alvos (`-s`, sem vídeo);
   - para cada chapa, zona, origem de papel e borda de faixa: coordenada em px, a linha grossa mais próxima e o resíduo;
   - critério: **≤ 1 px**;
   - inclua um recorte 1:1 de um canto de chapa sobre a grade, por alvo, numa prancha `alinhamento_v3.jpg`.
3. **R5 · sobreposição** em cada gatilho, com a seta inteira → `sobreposicoes_v3.txt`.
4. **R7 · setas na chapa**, quadro a quadro, em todos os blocos com chapa → `setas_na_chapa_v3.txt` (zero esperado).
5. **R8 · chapa vazia:** liste toda chapa sem conteúdo por mais de 0,5 s (zero esperado).
6. **Flash por quadro = 0:** nenhuma fórmula aparece inteira antes da caneta.
7. **Holds:** como no §5.
8. **Números:** os valores do §4 na tela, com vírgula decimal.

## 10. Parada

Entregue:
- o preview;
- as pranchas `comparacao_v3`, `alinhamento_v3` e `antes_depois_v3`;
- os relatórios (`alinhamento`, `sobreposicoes`, `setas_na_chapa`, `holds`, R8);
- o relatório de entrega.

Pare e não inicie voz nem 1080p de vídeo.

---

## Anexo A · Narração canônica v3 (com tags do ElevenLabs v4)

As frases novas da v3 estão marcadas com ▶ (a marca não é falada).

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

[thoughtful] E tem um detalhe no seu disco: o próprio ponto fica de fora. É o "maior que zero" da definição. O limite só olha para quem está chegando, nunca para o que acontece em cima do ponto. Aliás, o ponto nem precisa estar no domínio: basta ter pontos do domínio tão perto dele quanto você quiser. O nome disso é ponto de acumulação. ▶ Já um ponto do domínio sozinho, sem vizinhos, não serve: ninguém chega perto dele. Agora sim, escrito: a seta-alvo é o limite quando, para todo épsilon positivo, existe um delta positivo tal que, para todo ponto do domínio a uma distância maior que zero e menor que delta, a seta fica a menos de épsilon do alvo. A metade da esquerda fala de onde você anda. A da direita, de onde a seta chega.

[curious] E tem um atalho. Se a ponta está no disco épsilon, as duas sombras dela, a horizontal e a vertical, ficam a menos de épsilon das sombras do alvo. E o contrário também vale: se as duas sombras estão perto, a ponta cai num quadrado, que cabe num disco só um pouquinho maior. Então o limite de um campo existe exatamente quando o limite de cada componente existe, e aí é o limite de funções de várias variáveis que você já conhece.

### B2 · Quando o limite não existe

[curious] Agora um campo encrenqueiro. Todas as setas são horizontais. Nos eixos, não tem seta nenhuma; nas diagonais, as setas têm tamanho um: numa delas apontam para a direita, na outra, para a esquerda.

[thoughtful] Vem andando até a origem pelo eixo horizontal: a seta é zero o caminho todo. Pela diagonal de subida: um, para a direita. Pela outra: um, para a esquerda. Numa reta qualquer pela origem, o campo vale o dobro da inclinação, dividido por um mais a inclinação ao quadrado. Muda a reta, muda o valor.

[curious] E dá para ver isso de um jeito mais bonito. Em coordenadas polares, a componente horizontal vira o seno do dobro do ângulo. O campo não depende da distância, só da direção. Então dá uma volta num círculo minúsculo em volta da origem: a ponta da seta varre o segmento inteiro, de menos um até um. E isso acontece em qualquer círculo, por menor que seja.

[thoughtful, emphatic] Agora joga o desafio. Escolhe um alvo qualquer e um épsilon de meio. O disco tem largura um, e o segmento tem largura dois: não cabe, seja qual for o alvo. Então não existe limite na origem. E fica um cuidado: dois caminhos com valores diferentes provam que o limite não existe. Mas todas as retas darem o mesmo valor ainda não provam que ele existe, porque dá para chegar por uma curva. ▶ Olha este campo: por qualquer reta, a seta vai para zero. Mas, pela parábola, ela fica em meio o caminho todo. Também não tem limite.

### B3 · Continuidade

[thoughtful] Agora a continuidade. A definição tem três pedaços, e cada um pode falhar. Um: o ponto está no domínio, então a seta do ponto existe. Dois: o limite ali existe. Três: o limite é igual à própria seta do ponto. Na figura, é o mesmo desafio de antes, só que agora o disco épsilon fica em volta da ponta da seta do próprio ponto. No nosso campo, a mancha cabe. Contínuo.

[curious] Agora, três jeitos de dar errado. No campo elétrico de uma carga, o ponto da carga nem está no domínio. Falha o primeiro pedaço, e a pergunta nem se faz; em todo o resto, ele é contínuo. No campo encrenqueiro, definido como zero na origem, a seta existe, mas o limite não: falha o segundo. E neste aqui todas as setas apontam para a direita, menos a do centro, que aponta para cima. O limite existe e é a seta para a direita, mas a seta do ponto é outra. Falha o terceiro: um salto bem em cima do ponto.

[thoughtful] E, de novo, por componentes: o campo é contínuo exatamente quando cada componente é contínua. Por isso quase todo campo que vem de fórmula é contínuo onde está definido: somas, produtos, quocientes com denominador diferente de zero e composições de funções contínuas continuam contínuas. ▶ A primeira componente do nosso campo é uma constante mais senos: contínua. E o campo da carga é um quociente: contínuo em todo lugar, menos em cima da carga.

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

[curious] E com ela vem a promessa. Pega uma malhinha em volta do ponto e manda para a tela da chegada. As linhas horizontais viram curvas na direção da derivada horizontal, e as verticais, curvas na direção da derivada vertical. Cada quadradinho da malha vira quase um paralelogramo, com lados de passo vezes derivada. Escrito: a seta num ponto vizinho é a seta do ponto, mais o passo horizontal vezes a derivada na horizontal, mais o passo vertical vezes a derivada na vertical, com um erro que some mais rápido que o passo. O nosso campo, feito de senos e cossenos, é cê um. O encrenqueiro, não. ▶ E dá para ver isso dividindo o erro pelo passo. No nosso campo, quando o passo cai pela metade, essa conta cai pela metade também, e vai para zero. No encrenqueiro, ela dobra.

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
