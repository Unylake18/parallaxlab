# yt_0030 · CÁLCULO III · EP. 04 · Exercícios do módulo 3.1
# AVALIAÇÃO DO PREVIEW v1 + HANDOFF v2 · preview silencioso (540p, 15 fps)

2026-11-11. Produção → Claude Code. Documento **autocontido**: vale junto com o handoff v1 (que continua na unidade como `handoff_v1.md`) e com a pasta `yt_0030_quadros_alvo_v2/` do zip (22 quadros-alvo novos `v2_*.jpg`, a folha de contato e o gerador `sb30v2.html`, que contém as chaves v1 **e** as v2). Onde este documento e o v1 divergirem, **vale este**.

Fase aberta: **preview visual silencioso v2**. Sem voz, sem SRT, sem 1080p, sem master, sem entrega, sem commit e sem push.

O pedido do Kaio, nas palavras dele: *"corrigir animação, sobreposição, MF-Tools, álgebra. Preciso que seja mais didático, mais passo a passo, sem colocar do nada os termos."*

---

## 0. O que entregar

1. A mesma unidade `videos_longos/yt_0030_exercicios_modulo_31/`, com as mudanças deste documento (copie o v1 para `renders/v1/` antes de mexer; não apague nada do v1).
2. `renders/v2/yt_0030_preview_v2_540p15.mp4` (960×540, 15 fps, sem áudio), com o tempo da narração **v3.1** (§6 e Anexo A).
3. `renders/v2/qa/`: tudo o que o §8 pede, incluindo os dois relatórios novos `origens_v2.txt` e `glyphmaps_v2.txt`.
4. A prancha render × alvo: os 29 alvos v1 que continuam valendo + os 22 alvos v2.
5. O relatório de entrega do AGENTS.md.

---

## 1. Avaliação do v1

O v1 acertou o sistema visual (fundo, grade, layouts, cores, quadradinho, alinhamento ≤ 4 px, R5/R7/R10 zerados) e a duração. **Não precisa mexer em nada disso.** O problema está na **álgebra** e no **ritmo**.

### 1.1 Termos que aparecem do nada (o principal)

A caneta escreve glifo a glifo, mas a linha **já nasce com o resultado**. O aluno vê o que a conta dá, não de onde vem. Bloco a bloco:

| Bloco | No v1 | O que falta |
|---|---|---|
| D1 | Os cantos voam para (1, 1), (2, 0), (1, −1) sem conta | φ(1, 0) = (1 + 0, 1 − 0) = (1, 1), com o 1 e o 0 vindo do canto |
| D1 | A reta vira y = x sem conta | φ(u, 0) = (u, u) |
| D1 | No campo, as setas dos eixos só "estão lá" | F(x, 0) = (x, x) e F(0, y) = (y, −y) |
| D3 | ∂Q/∂x surge inteira; Q nunca é escrito; as linhas sobem e somem, ficam linhas soltas começando por "=" | P, Q e s primeiro; o molde da regra do produto; cada passo na mesma linha |
| D3 | div é uma linha só | ∂P/∂x e ∂Q/∂y calculadas, depois o cancelamento |
| D3 | α = 0, ½, 1, 2 dão o rot sem substituir | (2 − 2α)/s^α com o α trocado |
| D3 | O giro de 90° troca rot ↔ div sem explicar | w = (Q, −P), e por isso div w = rot v |
| D3b | ∇φ, a fórmula do rot e as identidades aparecem inteiras | rot F (molde) → P = φ_x … → as mistas → Schwarz |
| D4 | ‖F‖ em polares de uma vez; ∂P/∂x pula a regra do quociente | Cada passo, com o desenho de r, θ, x, y no palco |
| D5 | As entradas da tabela aparecem prontas; rot/div/d₁/d₂ aparecem como números, sem fórmula | P e Q → derivadas → tabela → fórmula-mãe → substituição → número |
| A1 | rot = −2x/9 sem conta | A tabela do rio e a fórmula-mãe |
| A3 | A fórmula do rot é reescrita do nada; a soma Σ fica espremida | A parcela pela regra do produto e da cadeia, as três parcelas, a soma |
| A4 | Cauchy-Riemann aparece pronta | d₁ = 0 e d₂ = 0, cada uma com um termo atravessando a igualdade |

### 1.2 MF-Tools quase sem uso

No vídeo inteiro há ~6 `TransformByGlyphMap` (vários caindo no `TransformMatchingShapes` de reserva do `tbgm30`). Toda manipulação algébrica precisa ser um glyph map com mapa explícito (§3).

### 1.3 Tela parada

O `holds_v1.txt` tem **28 trechos parados > 6 s** e 76 > 3 s. Os piores:
- A3-5: 15,5 s;
- D5-11: 14,7 s;
- A3-6: 14,5 s;
- A2-2: 12,6 s;
- D5-5: 12,6 s;
- A2-2: 11,3 s;
- A3-5: 10,5 s;
- H-1: 9,7 s.

O gancho fica 34 s com a mesma imagem. O §5 dá um evento para cada um dos 28.

### 1.4 Palco vazio ou tela só de álgebra

Isso fere a regra "nunca uma tela só de álgebra":

| Bloco | Trecho |
|---|---|
| D1 | 1:28–1:48 |
| D2 | 3:32–3:56 |
| D3b | 8:20–8:52 |
| D5 | 13:36–13:50 |
| A2 | início |
| A3 | início |
| A4 | 20:56–21:20 |

### 1.5 Sobreposições que o QA não pegou

O R5 mede seta × seta e seta × fórmula, mas não pegou estes casos:
- **A4:** os textos de Mercator e do "irmão" caem dentro do painel esquerdo, em cima da malha.
- **D5 ③:** os rótulos longos (`(1, 0): SÓ CRESCE` etc.) ficam sobre as setas.
- **Coluna:** pilhas de 4 ou 5 legendas SG Medium seguidas (D3c, D4, A3), uma colada na outra.

### 1.6 Uma inconsistência objetiva (corrigida aqui)

No D5 ③, o v1 mediu "quinas a menos de 2° do reto" no **quadrilátero dos quatro cantos**. Só que o fluxo de z² é z/(1 − tz), uma transformação **conforme**: na imagem exata, as quinas ficam em **90° exatos**. Os lados se curvam menos de 1 % do lado (0,85 % com lado 0,3; 0,28 % com lado 0,1), o que é invisível na tela. Por isso a fala muda (Anexo A, D5) e a tela passa a dizer `QUINAS RETAS (90°)` (§4, D5).

### 1.7 Itens do relatório v1 que ficam como estão

Ficam como o v1 fez:
- logo no gancho;
- tabela J colorida por **coluna** (∂/∂x âmbar, ∂/∂y magenta), como no gerador;
- as legendas que o v1 acrescentou, `FIO CARREGADO` e `TER DERIVADAS PARCIAIS NÃO BASTA`, desde que respeitem o limite de legendas (R13);
- o galho do A1, se for só um segmento simples girando no ritmo real.

Os gatilhos atrasados 0,4–1,0 s passam a ter tolerância de **0,2 s** (§8).

---

## 2. Regras novas da álgebra (valem para o vídeo inteiro)

**R11 · Todo termo tem origem.** Cada glifo de fórmula entra na tela por **um** destes três caminhos, e só por eles:

| Origem | Quando | Como |
|---|---|---|
| (a) caneta | o termo é dito pela fala naquele instante | `Write` glifo a glifo, sincronizado com a palavra que o nomeia |
| (b) voo | o termo já existe em outro lugar visível (desenho, célula da tabela, componente do campo, linha anterior, rótulo de ponto) | `TransformFromCopy` da peça-fonte para a peça-alvo (0,6–0,8 s), com a peça-fonte acendendo na cor dela durante o voo |
| (c) glyph map | o termo é a linha anterior manipulada | `TransformByGlyphMap` (MF-Tools 1.4.9) da linha anterior para a nova, com mapa explícito |

O relatório `origens_v2.txt` lista **toda** linha de fórmula do vídeo: tempo, texto, origem (a/b/c) e, para (b) e (c), a fonte. Linhas "sem origem" esperadas: **zero**.

**R12 · Fórmula-mãe antes do número.** Nenhum número de rot, div, d₁, d₂, derivada ou norma aparece sem que a fórmula geral esteja escrita antes e o número venha por substituição:
1. molde (ex.: `rot = Q_x − P_y`);
2. substituição (as peças voam das células: `rot = 1 − 1`);
3. resultado (glyph map: `rot = 0`).

Vale também para as regras do produto, do quociente e da cadeia: o molde com as peças (`(x)′·s^{−α} + x·(s^{−α})′`, `(N′D − ND′)/D²`) vem antes da conta.

**R13 · Quadro de contas sem linha órfã.**
- No máximo **5 linhas** de conta na coluna ao mesmo tempo (mais o enunciado no topo).
- Uma linha que começa por "=" só existe enquanto a linha de cima, com o lado esquerdo, está visível.
- Quando faltar espaço, as linhas **se fundem** numa só por glyph map (o lado esquerdo da primeira mais o resultado da última). Nunca se faz `FadeOut` da linha de cima deixando a de baixo solta.
- No máximo **2 legendas** SG Medium seguidas na coluna.

**R14 · Cancelamento visível.**
1. O par que cancela fica coral `#FF7A8A` ao mesmo tempo (0,3 s).
2. Um traço coral fino (2 px) risca cada termo, como caneta (`Create`, 0,3 s).
3. O par some junto no glyph map seguinte (`auto_fade`).

Nos alvos, isso aparece como `\cancel` coral. Quando há vários pares (D3b), um par por vez, no ritmo da fala.

**R15 · Palco nunca vazio durante a conta.**
- Enquanto a coluna calcula, o palco mostra o objeto da conta: o campo, o quadradinho, o ponto com r e θ, a componente P, as curvas de nível.
- Quando a fala cita uma peça do desenho ("a componente vertical", "a seta do lado de dentro"), a peça acende na cor dela por 1 s e depois volta.
- Nada de lupa, brilho ou pulso: só mudança de cor.

**R16 · Nenhum hold > 6 s.**
- Todo trecho parado > 6 s ganha um evento ligado a uma palavra da fala (§5).
- Holds de 3–6 s são aceitos se a fala estiver lendo o que está na tela (motivo no `holds_v2.txt`).

**Notação de índice:** a partir do D3b, `P_x` = ∂P/∂x (legenda `ÍNDICE = DERIVADA: φx = ∂φ/∂x` na primeira vez, alvo `v2_i1`). D5, A1, A2 e A4 usam índices: as linhas ficam curtas e legíveis a 34–36 px. O D3 e o D4 continuam com ∂/∂ em fração, porque ali a derivada é calculada por extenso.

**Tamanho mínimo:** `MathTex` ≥ 30 px no 1080p, **contando** frações (nada de `\tfrac` com derivadas parciais: os glifos ficam com ~19 px).

---

## 3. MF-Tools: como usar aqui

- Use os helpers da unidade: `Pz` (peças em `MathTex` de string única) + `tbgm30`.
- **A reserva `TransformMatchingShapes` do `tbgm30` passa a contar como falha:** cada vez que ela for usada, `glyphmaps_v2.txt` registra, e o esperado é zero. Se um mapa não fechar, ajuste as peças; não troque de animação.
- Os mapas listados no §4 são os mínimos. Meta: **≥ 90 `TransformByGlyphMap`** no vídeo (a lista do §4 soma ~110).
- `glyphmaps_v2.txt`: tempo, bloco, linha A → linha B, número de pares mapeados, se usou `auto_fade`.
- `show_indices` só no desenvolvimento; nada de índice no render.
- Substituição com voo (R11-b): o molde é copiado (`TransformFromCopy`) para a linha nova; as peças que mudam (u → 1, v → 0, ∂Q/∂x → 1) saem com `auto_fade` enquanto os valores voam da fonte para o lugar delas; o resto casa por glyph map.

---

## 4. Bloco a bloco: a álgebra passo a passo

Formato: **"fala" → o que acontece**. Gatilho = palavra entre aspas (tempo pela posição na narração v3.1 ÷ 3, §6). Alvo `v2_*` = estado final daquele trecho (tolerância ±20 px, mesmo texto e cores). As linhas LaTeX exatas estão no `sb30v2.html` (procure a chave).

### H · Gancho (alvo 03 v1 + `v2_h2`)

1. **"Três fórmulas"** → as três fórmulas embaixo dos cartões, em caneta, uma por cartão (0,6 s cada).
2. **"três quadradinhos de fluido"** → as redes de setas + os fantasmas tracejados entram (`FadeIn` 0,6 s cada, um depois do outro).
3. **"Um vai girar."** → `QUAL GIRA?` em caneta. **"Outro vai mudar de área."** → `QUAL MUDA DE ÁREA?`. **"E um vai entortar."** → `QUAL ENTORTA?`. O título se escreve em três pedaços.
4. **"só olhando a fórmula"** → um traço GEO de 2 px se desenha embaixo de cada fórmula, da esquerda para a direita, 0,4 s cada.
5. **"antes de soltar o fluido?"** → um `?` coral (SG Bold 40) no centro de cada fantasma.
6. **"Dá."** → `A FÓRMULA JÁ SABE`. Os quadradinhos continuam parados (eles só andam no D5).
7. **"por que o campo magnético de um fio"** → os três cartões saem e entram dois (alvo `v2_h2`): à esquerda o fio ⊙ com o campo de α = 1 e `FIO COM CORRENTE`; o título troca para `POR QUE 1/r? POR QUE 1/r²?`.
8. **"com um sobre a distância"** → `|B| ∝ 1/r`. **"e o campo de uma carga"** → o cartão da carga entra. **"ao quadrado?"** → `|E| ∝ 1/r²`.
9. **"É o rotacional e o divergente escolhendo a lei."** → `rot B = 0` (violeta) e `div E = 0` (azul) em caneta, um em cada cartão.

### A · Bem-vindos (alvos 01 v1 + `v2_ab2`)

As cinco linhas de `NESTE VÍDEO:` entram uma por trecho da fala (`duo`, 32 px):
- `DOIS FILMES · TRANSFORMAÇÃO E CAMPO` → "Primeiro, ler uma fórmula";
- `REDEMOINHOS · ROT, DIV E DUAS REGRAS` → "Depois, uma família inteira";
- `DE PERTO · LIMITE, CONTINUIDADE E PARCIAIS` → "Aí vem um campo";
- `O DESAFIO · PREVER O QUADRADINHO` → "no topo da escada";
- `AS APLICAÇÕES · RIO, PAREDE, MAPAS E FIOS` → "Na segunda parte".

O resto como no v1.

### D1 · Mesma fórmula, dois filmes (alvos `v2_d1q`, `v2_d1r`, `v2_d1c` + 04–06 v1)

1. Abertura do bloco: o layout B entra **com os eixos e o quadrado ①②③④ já no painel esquerdo**, para o palco não ficar vazio; φ(u, v) em caneta embaixo à esquerda.
2. **Reta** ("onde o segundo número é zero"):
   - O eixo u acende em âmbar.
   - Embaixo à direita: cópia do molde → φ(u, 0) = (u + 0, u − 0), com o 0 voando do rótulo `v = 0`.
   - Glyph map → φ(u, 0) = (u, u).
   - O eixo voa para a diagonal; `y = x` sai do (u, u) por glyph map.
3. **Cantos** ("O canto um, zero"), alvo `v2_d1q`:
   - Cópia do molde φ(u, v) = (u + v, u − v) para a direita.
   - O **1** (âmbar) e o **0** (magenta) voam do rótulo `(1, 0)` do canto ② para os lugares de u e v; os u e v saem por `auto_fade`. Fica φ(1, 0) = (1 + 0, 1 − 0).
   - Glyph map → `= (1, 1)`.
   - O `(1, 1)` voa para o ponto ② do painel direito, e o canto ② voa junto (`TransformFromCopy` do ponto).
   - ③ e ④ em seguida (0,8 s cada): glyph map da linha anterior trocando só os números (1, 1 → 1 + 1, 1 − 1 → (2, 0); depois 0, 1 → (1, −1)).
4. **Lado e área** ("lado raiz de dois"): `ℓ = √(1² + 1²) = √2` em caneta, com os dois 1 voando do ponto (1, 1); glyph map → `área = (√2)² = 2`. Depois `ESPELHADO` (coral) na seta curva da ordem dos cantos.
5. **Círculo** (alvo `v2_d1r`), quatro glyph maps encadeados:
   - x² + y² = (u + v)² + (u − v)², com x e y voando da fórmula φ;
   - abre os quadrados → u² + 2uv + v² + u² − 2uv + v²;
   - cancela ±2uv (R14);
   - funde → 2u² + 2v² = 2(u² + v²) ⇒ r′ = √2·r.

   A linha final substitui as duas (R13) e chega ao alvo 05 v1.
6. **Campo** (alvo `v2_d1c`, depois o 06 v1):
   - Rede inteira na cor de contexto.
   - **"No eixo horizontal"** → as setas do eixo horizontal acendem em menta; na coluna, F(x, 0) = (x + 0, x − 0) = (x, x) (molde → substituição → glyph map), e `AS DUAS COMPONENTES IGUAIS: DIAGONAL`.
   - **"No eixo vertical"** → idem com F(0, y) = (y, −y).
   - **"E aqui fica uma pergunta"** → a coluna troca para a do alvo 06 v1 (R10 dentro da coluna: o novo entra enquanto o velho sai).

### D2 · Desenhar sem mil setas (alvos 07, 08 v1)

1. O palco entra **com a diagonal tracejada** desde o começo (não vazio).
2. **"só depende da diferença"** → x − y = c ⇒ f = (1, c), por glyph map a partir de f = (1, x − y): o bloco `x − y` vira `c`.
3. **"Na própria diagonal, a diferença é zero"** → cópia de `(1, c)` → glyph map `c → 0` → o rótulo `(1, 0)` voa para a reta. O mesmo para c = 1, 2 e depois −1, −2.

### D3 · A família de redemoinhos (alvos `v2_d3r1`, `v2_d3r2`, `v2_d3r3`, `v2_d3g` + 09–11 v1)

Palco: o redemoinho de α = ½ com as circunferências r = 1, 2, 3 tracejadas (GEO, 35 %) e o fantasma do quadradinho em (1,75; 0).

1. **"tangentes às circunferências"** → as circunferências se desenham (`Create`, 1 s).
2. **Rapidez** ("O vetor de cima tem tamanho igual à distância"), três glyph maps: ‖v‖ = ‖(−y, x)‖/s^α → = r/r^{2α} → = r^{1−2α}. O r de cima acende junto com o raio de uma circunferência.
3. **rot** (alvo `v2_d3r1`), na ordem da fala:
   - `rot = ∂Q/∂x − ∂P/∂y` em caneta ("a derivada da componente vertical…").
   - `Q = x·s^{−α}, s = x² + y²`: o `x` voa do numerador de v e o `x² + y²` voa do denominador para virar `s`.
   - Molde da regra do produto: ∂Q/∂x = (x)′·s^{−α} + x·(s^{−α})′ ("Regra do produto").
   - Linha de baixo: = 1·s^{−α} + x·(−α s^{−α−1}·2x). O `1` em caneta em "a primeira parte"; a cadeia em caneta em "pela regra da cadeia", com o `2x` em "vezes duas vezes a coordenada horizontal".
   - **No palco:** "a componente vertical" → as componentes verticais das setas do semieixo x > 0 acendem por 1 s.
4. **Fusão** (alvo `v2_d3r2`):
   - As duas linhas da regra fundem-se (R13) em ∂Q/∂x = s^{−α} − 2αx² s^{−α−1} (x·x → x², −α·2 → −2α).
   - **"Põe a potência com um a menos em evidência"** → glyph map → ∂Q/∂x = s^{−α−1}(s − 2αx²).
   - **"A outra derivada é igualzinha"** → `TransformFromCopy` da linha de ∂Q/∂x para a de baixo, com glyph map: Q → P, ∂x → ∂y, x² → y², e um `−` em caneta na frente.
   - P = −y s^{−α} aparece na linha de P e Q antes disso (voo do −y do numerador de v).
5. **Substituição no rot:**
   - Cópia do molde rot.
   - As duas derivadas voam para os seus lugares: rot = s^{−α−1}(s − 2αx²) − (−s^{−α−1}(s − 2αy²)).
   - Glyph map −(−·) → +.
   - **"a distância ao quadrado aparece duas vezes"** → s^{−α−1}(s − 2αx² + s − 2αy²).
   - **"os dois termos com alfa se juntam"** → s^{−α−1}(2s − 2α(x² + y²)).
   - **"que é a distância ao quadrado de novo"** → `x² + y²` → `s` (a legenda `s = x² + y²` acende junto).
   - Depois → s^{−α−1}(2s − 2αs) → (2 − 2α)/s^α → (2 − 2α)/(x² + y²)^α.
   - São **6 glyph maps** em sequência, uma linha só, sempre com o lado esquerdo `rot =`.
6. **div** (alvo `v2_d3r3`):
   - As linhas de ∂Q/∂x e ∂P/∂y fundem-se no rot final (sobe para o topo da coluna).
   - `div = ∂P/∂x + ∂Q/∂y` em caneta.
   - ∂P/∂x = −y(−α s^{−α−1}·2x) = 2αxy s^{−α−1} ("só a regra da cadeia trabalha").
   - ∂Q/∂y por cópia + glyph map (x ↔ y onde cabe, sinal).
   - Substituição → os dois termos voam → cancelamento R14 → `div = 0`.
   - **No palco:** "Nenhum desses redemoinhos muda a área" → o quadradinho é solto (como o v1).
7. **Lendo a fórmula:** para cada α, a linha `rot = (2 − 2α)/s^α` ganha embaixo a substituição, com o valor de α voando do seletor `α = 0 ½ 1 2`:
   - (2 − 2·0)/s⁰ = 2;
   - (2 − 1)/s^{1/2} = 1/r;
   - (2 − 2)/s = 0;
   - (2 − 4)/s² = −2/r⁴.

   A cada troca, um glyph map da linha anterior (só os números mudam). O resto como no v1.
8. **Na origem** (alvo 11 v1): a linha `‖v‖ = r^{1−2α} → 0 se α < ½` em caneta na coluna, no "a rapidez vai a zero".
9. **Giro de 90°** (alvo `v2_d3g`):
   - Embaixo, v = (P, Q) = (−y, x)/s^α.
   - **"A componente horizontal nova é a vertical antiga"** → cópia → glyph map → w = (Q, −P) = (x, y)/s^α, com o Q e o −P voando das posições trocadas.
   - **"o divergente novo é exatamente a conta do rotacional antigo"** → div w = ∂Q/∂x − ∂P/∂y = rot v = (2 − 2α)/s^α, com a fórmula do rot voando da linha de v.
   - Depois, rot w = 0 pela troca simétrica.

### D3b · Duas regras (alvos `v2_i1`, `v2_i2a`, `v2_i2b` + 13 v1)

1. **"pega um campo que é o gradiente"** → no palco, as curvas de nível de φ = (x² − y²)/2 (hipérboles GEO tracejadas) e a rede de ∇φ (as setas cruzam as curvas em ângulo reto). Rótulo com placa embaixo à esquerda (alvo `v2_i1`). **O palco não fica vazio.**
2. **"as componentes são as derivadas parciais"** → F = ∇φ: P = φ_x, Q = φ_y, R = φ_z, e a legenda do índice.
3. **"Calcula o rotacional"** → o molde rot F em vetor coluna, com as três linhas em caneta (R_y − Q_z; P_z − R_x; Q_x − P_y).
4. **"A primeira componente é…"** → a linha 1 do molde é copiada para o vetor de rot ∇φ: R_y → φ_zy e Q_z → φ_yz, por glyph map (R → φ_z, depois o índice y entra). **"E as outras duas componentes têm a mesma cara"** → linhas 2 e 3 do mesmo jeito, mais rápido.
5. **"as derivadas mistas são iguais"** → as legendas de Schwarz; depois R14 em cada linha, um par por vez → `= 0⃗`.
6. **"No plano, só sobra a terceira componente"** → a linha 3 acende enquanto o palco mostra as curvas de nível; depois **"Lembra do campo que esticava o quadradinho"** → o quadradinho é solto na sela (alvo 13 v1).
7. **div rot F** (alvo `v2_i2a`):
   - O palco troca para o giro com o quadradinho.
   - rot F em linha (topo).
   - **"a primeira componente é derivada na horizontal…"** → div(rot F) = ∂/∂x(R_y − Q_z) + ∂/∂y(P_z − R_x) + ∂/∂z(Q_x − P_y), com cada parêntese voando da componente correspondente de rot F.
   - Glyph map → R_yx − Q_zx + P_zy − R_xy + Q_xz − P_yz.
   - **"Aparecem seis derivadas mistas, e elas se cancelam aos pares"** → R14 três vezes: o par R, o par Q, o par P → `= 0`.
8. **O teste** (alvo `v2_i2b`):
   - O quadro anterior se funde em `div(rot F) = 0` (topo).
   - O campo do enunciado em caneta.
   - **"Calcula o divergente"** → as três parcelas, cada componente voando para o seu ∂/∂.
   - **"a primeira parcela dá seno"** → glyph map parcela a parcela → sen y − sen y + 1; R14 no par → `1 ≠ 0` → `NÃO EXISTE`.
9. **Física** (hold de 8,6 s em 9:44):
   - **"divergente zero em todo lugar"** → `div B = 0`.
   - **"o rotacional de outro campo, o potencial vetor"** → `⇔ B = rot A` (`NO ESPAÇO TODO` em GEO).
   - **"a regra de hoje prova uma das metades"** → a linha de baixo: `B = rot A ⇒ div B = div(rot A) = 0`, com o `div(rot ·) = 0` voando do topo.

### D4 · O campo que não melhora de perto (alvos `v2_d4p`, `v2_d4q` + 15–18 v1)

1. **Item a** (alvo `v2_d4p`), com o palco (F₄ na cor de contexto) mostrando um ponto a r = 2, θ = 0,6 rad:
   - o raio r (GEO);
   - x (segmento âmbar no eixo);
   - y (segmento magenta tracejado);
   - o arco θ.

   Cada peça se desenha na palavra que a nomeia. Na coluna, os passos:
   - ‖F‖ = (|xy|/r²)·‖(x, y)‖ = (|xy|/r²)·r = |xy|/r (2 glyph maps);
   - x = r cos θ, y = r sen θ (x e y voam dos segmentos do palco);
   - xy = r² cos θ sen θ = r²·sen 2θ/2;
   - ‖F‖ = r|sen 2θ|/2 ≤ r/2 (glyph map + `≤ r/2` em caneta).
2. **ε-δ:** a cadeia `0 < ‖X‖ < δ = 2ε ⇒ ‖F(X)‖ ≤ ‖X‖/2 < δ/2 = ε`, em quatro pedaços, cada um na sua palavra.
3. **Item c:**
   - O ponto âmbar anda no eixo horizontal; ao lado dele, a linha `F(h, 0) = (h·0/h²)(h, 0) = 0⃗` (o h voa do rótulo do ponto).
   - Depois `∂F/∂x(0, 0) = lim (F(h, 0) − F(0, 0))/h = 0⃗`. Os dois zeros voam para a coluna 1 de J.
   - O mesmo no vertical para a coluna 2.
   - As quatro medidas com a fórmula-mãe (R12): rot = 0 − 0 = 0 etc.
4. **Item d:**
   - **"multiplicar a posição por um número"** → F(sx, sy) = (sx·sy)/(s²x² + s²y²)·(sx, sy).
   - **"aparece ao quadrado em cima e embaixo, cancela"** → R14 em s²/s².
   - → s·F(x, y).
   - Razão na diagonal: F(h, h) = (h/2, h/2) ⇒ ‖erro‖/‖H‖ = (h√2/2)/(h√2) = ½.
5. **Item e** (alvo `v2_d4q`):
   - O palco mostra **só a componente horizontal P** (setas âmbar horizontais); o campo inteiro sai.
   - P = xy/(x² + y²)·x = x²y/(x² + y²), com o `x` voando de (x, y).
   - Molde do quociente com N e D.
   - **"A derivada de cima é…"** → N′ = 2xy e D′ = 2x em caneta, voando para o molde.
   - A expansão, depois R14 em 2x³y, depois 2xy³/(x² + y²)².
   - **"Na diagonal, as duas coordenadas são iguais"** → y = x: 2x·x³/(2x²)² = 2x⁴/4x⁴ = ½.
   - Depois os pontos nas circunferências e o alvo 18 v1.
6. **"no episódio passado o campo encrenqueiro nem era contínuo"** (hold de 7 s em 13:22):
   - na coluna, `ANTES: NEM CONTÍNUO` (GEO);
   - depois `AGORA:` e três selos acendendo na fala: `CONTÍNUO ✓` ("Este é contínuo"), `PARCIAIS ✓` ("tem as duas derivadas parciais"), `TABELA ✗` ("e, mesmo assim, engana").

   Nada de "EP. 03" escrito na tela.

### D5 · O desafio prometido (alvos `v2_d5a`, `v2_d5c1`, `v2_d5c2` + 19–21 v1)

1. **Abertura** ("Lembra das quatro medidas"):
   - Antes do campo ①, a coluna escreve o molde da tabela J = (P_x P_y; Q_x Q_y), com as colunas âmbar/magenta.
   - Embaixo, as quatro fórmulas-mãe: rot = Q_x − P_y, div = P_x + Q_y, d₁ = P_x − Q_y, d₂ = Q_x + P_y.
   - Cada fórmula se escreve enquanto as **células** que ela usa acendem na cor da medida (rot violeta: as células Q_x e P_y; e assim por diante).
   - O palco já mostra f₁ com o quadradinho parado.
2. **Campo ①** (alvo `v2_d5a`):
   - P = x + y voa da 1ª componente de F, Q = x − y da 2ª.
   - **"as derivadas dela são um e um"** → P_x = 1, P_y = 1 em caneta.
   - Os números voam para as células: o molde J vira J = (1 1; 1 −1) por glyph map. O molde fica à esquerda do `=` (alvo).
   - **Medidas:** em cada uma, a fórmula-mãe já escrita ganha `= 1 − 1`, com os números voando das células (que acendem), e depois `= 0` por glyph map. O mesmo para div, d₁, d₂, no ritmo da fala ("um menos um, zero").
   - Selos `GIRA ✗ · ÁREA ✗ · DEFORMA ✓`. Solta.
3. **Resposta do palpite** (hold de 12,6 s em 14:39):
   - **"A transformação leva cada ponto, de uma vez, para a imagem"** → uma cópia tracejada do quadradinho **salta** (0,6 s, uma vez) para a imagem dele por φ (o quadrado de área 2).
   - **"O campo é uma velocidade: o fluido anda devagarinho"** → o quadradinho real é solto de novo (t de 0 a 0,5, 2 s).
   - **"quem mede a taxa de área… é o divergente, que aqui é zero"** → a linha `div = … = 0` da coluna acende em azul.
   - **"mudança de variáveis"** → `COMO TRANSFORMAÇÃO: ÁREA × 2` (coral).
4. **Campo ②:** o mesmo roteiro do ①:
   - F → P, Q;
   - derivadas → células → J = (0 0; 1 −1);
   - as quatro substituições: 1 − 0 = 1, 0 + (−1) = −1, 0 − (−1) = 1, 1 + 0 = 1;
   - selos.

   Depois:
   - **"esse é o um embaixo à esquerda"** → a célula Q_x acende junto com duas setas do campo (as de antes já estavam no v1).
   - **"porque a gente tirou a seta do centro"** (hold de 6,5 s) → a seta do centro do quadradinho, f₂(−1,8; −0,6) = (1; −1,2), aparece em branco no ponto de partida, e só então `A VIAGEM É A SETA DO CENTRO` se escreve.
5. **Campo ③** (alvo `v2_d5c1`):
   - P = x² − y² → P_x = 2x, P_y = −2y; Q = 2xy → Q_x = 2y, Q_y = 2x, cada uma na sua palavra.
   - Células → J.
   - As substituições: 2y − (−2y) = 4y; 2x + 2x = 4x; R14 em 2x − 2x → 0; R14 em 2y + (−2y) → 0.
   - `NUNCA ENTORTA`.
   - Rótulos do palco **curtos**: `(1, 0)`, `(0, 1)`, `(1, 1)`, com placa, em clareira (sem `SÓ CRESCE` no palco).
6. **Previsão nos pontos** (alvo `v2_d5c2`):
   - O quadro de ③ se funde numa linha: `rot = 4y, div = 4x, d₁ = d₂ = 0`.
   - Três linhas, uma por ponto: `(1, 0): rot = 4·0 = 0, div = 4·1 = 4`, com o 1 e o 0 voando do rótulo do ponto no palco. Embaixo de cada uma, a leitura (`SÓ CRESCE` / `SÓ GIRA` / `GIRA E CRESCE`, SG Medium 28, branco).
7. **"Solta os três!"** → os três juntos. Depois:
   - **"as quinas continuam em ângulo reto"** → marcas de ângulo reto (2 px, branco) nas quinas do (1, 1);
   - `QUINAS RETAS (90°) NOS TRÊS`;
   - **"os lados até se curvam, mas tão pouco que nem dá para ver"** → só a legenda `A TABELA FALA DO PONTO, NAQUELE INSTANTE` (nada de régua de curvatura: < 1 % do lado);
   - **"Bem pequeno"** → o (1, 1) é solto de novo com lado 0,1 (1,5 s).

   Isso cobre o hold de 14,7 s em 16:52.
8. **"Desafio cumprido"** → a cadeia `FÓRMULA → TABELA → 4 NÚMEROS → QUADRADINHO` (como no v1), com cada termo da cadeia voando da peça correspondente da coluna.

### P2 · Transição

`PARTE 2` + `AS APLICAÇÕES`. Depois:
- **"água de verdade"** → `ÁGUA DE VERDADE` (menta, SG Medium 30);
- **"leis da física"** → `LEIS DA FÍSICA` (azul);

as duas embaixo do título. Isso acaba com o hold de 7 s.

### A1 · O rio (alvo `v2_a1`)

1. **"a componente na direção do canal é…"** → v = (0, 1 − x²/9).
   - **"No meio dá um"** → o `1` acende junto com a seta do meio.
   - **"nas margens… zero"** → `x = ±3: 1 − 9/9 = 0`, e `v = 0⃗` com placa junto de cada margem no palco.
2. Molde J (índices) → J = (0 0; −2x/9 0).
   - div = P_x + Q_y = 0 + 0 = 0.
   - rot = Q_x − P_y = −2x/9 − 0 = −2x/9 (R12, com voo das células).
3. **"Na margem esquerda, menos dois nonos vezes menos três"** → `x = −3: rot = 2/3`, com o −3 voando do rótulo da margem.
   - **"o rotacional é o dobro da velocidade angular"** → ω = rot/2 = 1/3 rad/s.
   - **"dois pi dividido por um terço"** → T = 2π/ω = 6π ≈ 19 s.

   Isso cobre o hold de 9,4 s em 18:16.
4. **"a água do lado de dentro corre mais rápido"** (hold de 7,3 s) → as duas setas da borda de dentro e da borda de fora do quadradinho da esquerda acendem, as outras vão para o contexto por 2 s.
5. **Atrito** (hold de 8,6 s):
   - **"da diferença de velocidade entre camadas vizinhas"** → duas setas vizinhas perto da margem acendem e depois duas no meio;
   - d₁ = P_x − Q_y = 0, d₂ = Q_x + P_y = −2x/9 com voo das células.

### A2 · Água batendo na parede (alvo `v2_a2`)

1. Palco com a parede desde o primeiro quadro.
2. **"na parede, a componente vertical é zero"** → `v(x, 0) = (x, −0) = (x, 0)`, com o 0 voando da parede; as setas da fileira de baixo acendem (quase deitadas).
3. **"Numa parede de verdade"** → legenda `MODELO IDEAL: SEM A CAMADA QUE GRUDA` (GEO).
4. Tabela (1 0; 0 −1) → as substituições R12 (rot 0 − 0, div 1 + (−1), d₁ 1 − (−1) = 2).
5. **"Uma gota de tinta"** → solta.
6. **Hipérboles** (hold de 11,3 s):
   - v = (x, −y) = (u, v);
   - **"o produto muda pela velocidade horizontal vezes…"** → d(xy)/dt = u·y + x·v (caneta);
   - u e v voam de (u, v) e são substituídos → = x·y + x·(−y);
   - R14 → 0;
   - um ponto laranja anda sobre a hipérbole xy = 2 (2 s, uma vez) enquanto `O PRODUTO NÃO MUDA` se escreve.
7. φ = (x² − y²)/2: φ_x = x, φ_y = −y ⇒ ∇φ = v, com o v voando do topo. Depois ∇²φ = φ_xx + φ_yy = 1 + (−1) = 0.
8. **A cadeia** (holds de 7,7 s + 7,8 s), cada pedaço na sua frase:
   - `v = ∇φ ⇒ rot v = 0`;
   - `div v = 0`;
   - `⇒ div ∇φ = 0`;
   - `div ∇φ = ∇²φ`;
   - `∇²φ = 0 · EQUAÇÃO DE LAPLACE`.

### A4 · Mapas que não entortam (alvo `v2_a4`)

1. O layout B entra **com as duas malhas já paradas** (antes da fala sobre Cauchy-Riemann), para o palco não ficar vazio.
2. **"Iguala cada deformação a zero e passa um termo para o outro lado"**:
   - d₁ = P_x − Q_y = 0 → glyph map com o Q_y **atravessando o `=`** → P_x = Q_y;
   - o mesmo em d₂ → P_y = −Q_x.

   Este é o caso típico do MF-Tools: o termo voa por cima da igualdade e troca de sinal.
3. **"Abre o quadrado"** → (x + iy)² = x² + 2ixy + i²y²; **"é menos um"** → glyph map → (x² − y²) + i(2xy); os dois parênteses voam para F = (x² − y², 2xy) (escrito à direita).
4. **"lê como transformação"** → a malha voa e se curva (como o v1). **"sempre com ângulos retos"** → marcas de ângulo reto em 3 quinas da malha da direita.
5. **"Mercator"** (hold de 8,2 s) → o nome do painel direito (y = 868) troca para `COMO NO MAPA DE MERCATOR: ÂNGULOS PRESERVADOS`. **Nenhum texto dentro do painel esquerdo.**
6. **"o irmão"** → as linhas de baixo (y 945–1022) trocam (R10) por:
   - `(x² − y², −2xy): J = (2x −2y; −2y −2x)`;
   - `rot = −2y − (−2y) = 0 · div = 2x − 2x = 0 · SÓ DEFORMA`.

### A3 · Por que um sobre a distância (alvos `v2_a3p`, `v2_a3s` + 26, 27 v1)

1. **Fio** (hold de 9,3 s em 22:25):
   - **"o campo dá a volta no fio"** → circunferências tracejadas;
   - **"o tamanho só depende da distância"** → um raio r com rótulo;
   - **"Supondo uma lei de potência"** → B = (−y, x)/(x² + y²)^α em caneta.
2. **"Agora usa a fórmula que a gente guardou"** → a linha final do D3, `rot = (2 − 2α)/(x² + y²)^α`, reaparece **no mesmo lugar e no mesmo estilo** do D3 (FadeIn 0,6 s), com a etiqueta GEO `DO TERCEIRO DEGRAU`. É uma lembrança, não um termo novo. Em seguida, glyph map v → B.
   - **"o numerador zera"** → `2 − 2α = 0`;
   - glyph map: 2α atravessa → `2 = 2α`;
   - → `α = 1`.
   - ‖B‖ = r/r^{2α} = r/r² = 1/r, com o r^{1−2α} lembrado do D3.
3. **Fio carregado:** cópia da linha do rot → glyph map rot → div → `div E = (2 − 2α)/s^α = 0 ⇒ α = 1`.
4. **Carga** (alvo `v2_a3p`, cobre o hold de 15,5 s):
   - E = X/‖X‖^p, X = (x, y, z);
   - **"A derivada da distância, nessa direção"** → ∂‖X‖/∂x = x/‖X‖;
   - **"a derivada da coordenada horizontal sobre…"** → o molde do produto e da cadeia: ∂/∂x(x/‖X‖^p) = 1/‖X‖^p + x·(−p‖X‖^{−p−1})·x/‖X‖, com o x/‖X‖ voando da linha anterior;
   - glyph map → = 1/‖X‖^p − px²/‖X‖^{p+2}.
5. **Soma** (alvo `v2_a3s`, cobre o hold de 10,5 s):
   - a linha da parcela se funde (R13);
   - **"As outras parcelas são iguais"** → duas cópias com glyph map x → y e x → z;
   - **"Agora soma"** → as três voam para `div E = 3/‖X‖^p − p(x² + y² + z²)/‖X‖^{p+2}`;
   - **"somam a distância ao quadrado"** → glyph map `x² + y² + z²` → `‖X‖²`;
   - **"cancela o mais dois"** → R14 no ‖X‖² com o +2 do expoente;
   - → (3 − p)/‖X‖^p.
   - Depois `NO PLANO: 2 PARCELAS ⇒ (2 − p)`.
6. **"o expoente é três"** (hold de 7,3 s):
   - p = 3 ⇒ ‖E‖ = r/r³ = 1/r²;
   - **"a de Coulomb e a da gravitação"** → `COULOMB · GRAVITAÇÃO` (GEO), um nome por vez;
   - o gráfico |E| × distância (como o do alvo 26), com a curva 1/r² em menta e a 1/r tracejada em GEO, para comparar.
7. **Fecho** (hold de 14,5 s): a coluna se funde em `div E = (3 − p)/‖X‖^p` e mostra quatro linhas, uma por frase, no máximo 2 de cada vez (R13):
   - `NO PLANO: 2 · NO ESPAÇO: 3`;
   - `O EXPOENTE VEM DA DIMENSÃO`;
   - `LEI FÍSICA: rot = 0 OU div = 0 FORA DA FONTE`;
   - `+ SIMETRIA ⇒ NÃO SOBRA ESCOLHA` (`CÍRCULOS EM VOLTA DO FIO · RADIAL EM VOLTA DA CARGA` na fala "junto com a simetria").

### S · Síntese, gancho e CTA (alvos 28, 29 v1)

1. A escada sobe **um degrau por frase** (6 degraus, 6 gatilhos). No degrau 3, `VOLTA ≠ GIRO` entra em "o sentido da volta", depois de um `2 − 2α` pequeno em "saem da mesma conta". No degrau 4, `GRADIENTE NÃO GIRA` e depois `ROTACIONAL NÃO DIVERGE`, cada um na sua frase. Isso cobre o hold de 7,7 s.
2. **Cartão do próximo vídeo** (hold de 7 s):
   - `NO PRÓXIMO VÍDEO` + o título;
   - **"tudo foi medido num ponto, bem de perto"** → um quadradinho coral pequeno (lado 0,3 u) no lugar da chapa encolhe até virar um ponto (1 s);
   - **"somar pedacinhos"** → a chapa [0, 2]² entra dividida em 4×4 pedacinhos (traço GEO) e se preenche com a densidade;
   - depois a régua e os palpites (como o v1).

---

## 5. Os 28 trechos parados > 6 s do v1 e a correção de cada um

| v1 | Dur. | Bloco | Correção (§4) |
|---|---|---|---|
| 0:04.87 | 6,9 s | H | título em três pedaços, traço sob as fórmulas, `?` nos fantasmas |
| 0:22.47 | 9,7 s | H | cartões do fio e da carga, `∝`, rot B = 0 / div E = 0 |
| 5:04.20 | 8,1 s | D3 | circunferências + rapidez em três passos |
| 5:45.73 | 8,3 s | D3 | molde do produto + cadeia em caneta sincronizada |
| 8:18.33 | 8,9 s | D3b | curvas de nível + gradiente no palco, P = φ_x… |
| 8:40.40 | 7,5 s | D3b | linhas do rot ∇φ uma por vez, pares cancelando |
| 9:44.93 | 8,6 s | D3b | div B = 0 ⇔ B = rot A, depois a metade provada |
| 10:46.00 | 8,3 s | D4 | ponto, r, θ, x, y no palco + polares passo a passo |
| 13:22.53 | 7,0 s | D4 | ANTES / AGORA com três selos |
| 14:39.33 | 12,6 s | D5 | salto da transformação × fluxo + div acende |
| 15:47.33 | 6,5 s | D5 | a seta do centro aparece |
| 16:52.67 | 14,7 s | D5 | ângulos retos + quadradinho pequeno |
| 17:25.73 | 7,0 s | P2 | ÁGUA DE VERDADE / LEIS DA FÍSICA |
| 18:16.00 | 9,4 s | A1 | rot(−3), ω, T |
| 18:41.80 | 7,3 s | A1 | setas das bordas acendem |
| 18:53.60 | 8,6 s | A1 | setas vizinhas + d₁, d₂ com voo |
| 19:34.87 | 12,6 s | A2 | v(x, 0), setas da parede, modelo ideal, tabela |
| 20:06.80 | 11,3 s | A2 | d(xy)/dt passo a passo + ponto na hipérbole |
| 20:30.60 | 7,7 s | A2 | cadeia gradiente → Laplace (1ª metade) |
| 20:38.60 | 7,8 s | A2 | cadeia (2ª metade) |
| 21:45.27 | 8,2 s | A4 | ângulos retos + nome do painel Mercator |
| 22:25.73 | 9,3 s | A3 | circunferências, raio, fórmula de B |
| 23:42.47 | 15,5 s | A3 | parcela: molde, ∂‖X‖/∂x, glyph map |
| 24:01.27 | 10,5 s | A3 | cópias y, z, soma, ‖X‖², cancelamento |
| 24:20.13 | 7,3 s | A3 | p = 3, Coulomb/gravitação, gráfico 1/r² × 1/r |
| 24:32.80 | 14,5 s | A3 | as quatro linhas do fecho, uma por frase |
| 25:08.07 | 7,7 s | S | degraus 3 e 4 em dois tempos |
| 25:41.40 | 7,0 s | S | quadradinho → ponto → chapa em pedacinhos |

Os tempos mudam na v3.1; o `holds_v2.txt` mostra a nova lista (esperado: zero > 6 s).

---

## 6. Tempo (narração v3.1)

A narração v3 ganhou ~490 palavras **só onde a tela agora mostra um passo que a fala não dizia** (Anexo A; cada mudança na tabela A.0). Nada foi tirado. Orçamento a 3 palavras/s:

| Bloco | v3 | v3.1 | Início | Duração |
|---|---|---|---|---|
| H | 103 | 103 | 0:00 | 34 s |
| A | 161 | 161 | 0:34 | 54 s |
| D1 | 372 | 438 | 1:28 | 146 s |
| D2 | 213 | 213 | 3:54 | 71 s |
| D3 | 642 | 756 | 5:05 | 252 s |
| D3b | 324 | 351 | 9:17 | 117 s |
| D4 | 628 | 692 | 11:14 | 231 s |
| D5 | 678 | 750 | 15:04 | 250 s |
| P2 | 36 | 36 | 19:14 | 12 s |
| A1 | 305 | 345 | 19:26 | 115 s |
| A2 | 302 | 323 | 21:21 | 108 s |
| A4 | 199 | 263 | 23:09 | 88 s |
| A3 | 527 | 550 | 24:37 | 183 s |
| S | 225 | 225 | 27:40 | 75 s |
| **Total** | **4.715** | **5.206** | | **≈ 28:55** |

- Troque o texto do `tempos.py` pelo Anexo A (v3.1) e recalcule os gatilhos (posição da palavra ÷ 3). A `cena.py` continua lendo só o `tempos.py`.
- Duração aceita do preview: 28:55 ± 15 s. O teto do Kaio é ~30 min.
- Se o passo a passo não couber no tempo da fala de algum trecho, **não acelere abaixo de 0,5 s por glyph map**. Avise no relatório o trecho e quantos segundos faltam; a Produção ajusta a fala.

---

## 7. O que NÃO fazer

- Não mexer no que o v1 acertou (sistema visual, cores, layouts, quadradinho, alinhamento, transições).
- Nada de 3D, partícula, brilho, sombra, pulso, lupa, laço contínuo, barra ou cronômetro. "Acender" = trocar a cor por 1–2 s e voltar.
- Nada de caixa em volta de fórmula (`\boxed` só no seletor de α, que já existe).
- Nenhum número de episódio, livro ou Atlas na tela. Não escrever "EP. 03".
- Não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md`, `pyproject.toml`, `uv.lock` nem nas unidades yt_0026–yt_0029.
- Sem voz, SRT, master, 1080p de vídeo, entrega, commit ou push.

---

## 8. QA do preview v2 (obrigatório)

1. **Render × alvo** (51 = 29 v1 + 22 v2) a 960×540, tolerância de 10 px → `comparacao_v2.jpg` + `.txt`. Dos v1, valem como estão: 01, 02 (a versão nova é `v2_ab2`), 04–22 e 23–29 **no estado final do trecho**. Onde houver um alvo v2 do mesmo trecho, o v2 é o estado intermediário daquela conta e o v1 o final.
2. **`origens_v2.txt` (novo, R11):** toda linha de fórmula, com tempo, texto, origem (a caneta / b voo / c glyph map) e fonte. Esperado: zero sem origem.
3. **`glyphmaps_v2.txt` (novo):** todos os `TransformByGlyphMap`, com tempo e bloco. Meta ≥ 90; reservas `TransformMatchingShapes` = 0.
4. **R12:** lista de todo valor de rot/div/d₁/d₂/derivada que aparece, com o tempo da fórmula-mãe correspondente (sempre antes).
5. **R13:** máximo de linhas de conta simultâneas por bloco (≤ 5); linhas que começam por "=" sem a de cima visível = 0; legendas seguidas ≤ 2.
6. **R5/R7/R10** como no v1 (zero), **mais** texto × setas e texto × malha (o caso do A4 e do D5 ③).
7. **Holds:** `holds_v2.txt`; zero > 6 s.
8. **Gatilhos:** atraso de cada evento em relação à palavra ≤ 0,2 s (`gatilhos_v2.txt`, só os que passarem).
9. **Tamanho:** nenhuma fórmula com glifo < 30 px no 1080p (frações incluídas).
10. **Números:** `numeros_v2.txt`, como no v1, com os novos valores intermediários. Todos conferidos no `verifica_calc3_e1_passos_v2.py` (71/71, no zip).
11. **`PAUSE E TENTE`:** as 10 ocorrências, como no v1.

---

## 9. Parada

Entregue o preview v2, as pranchas, os relatórios do §8 e o relatório de entrega (arquivos alterados, verificações, caminho do preview, limitações, trechos onde o passo a passo apertou o tempo). Pare: não inicie voz, SRT, 1080p, master nem entrega.

---

## Anexo A · Narração v3.1 (v3 + acréscimos do passo a passo)

Só para tempo e gatilhos nesta fase. **Não gerar voz.** É a narração v3 aprovada com as mudanças da tabela A.0 abaixo (só acréscimos onde a tela mostra um passo novo, mais a correção do D5 ③ do §1.6). Mesmas regras de estilo.

### A.0 · O que mudou da v3 para a v3.1

| # | Bloco | v3 | v3.1 |
|---|---|---|---|
| 1 | D1 | O canto um, zero vai para um, um. | O canto um, zero: a soma dá um mais zero, e a diferença, um menos zero. Ele vai para um, um. |
| 2 | D1 | com lado raiz de dois. A área era um; agora é dois. | com lado raiz de dois, a distância da origem até o ponto um, um. A área era um; agora é raiz de dois ao quadrado: dois. |
| 3 | D1 | Soma ao quadrado mais diferença ao quadrado: os termos cruzados se cancelam, | Soma ao quadrado mais diferença ao quadrado. Abre os dois quadrados: num aparece mais duas vezes o produto, no outro, menos duas vezes o produto. Esses termos cruzados se cancelam, |
| 4 | D1 | No eixo horizontal, à direita da origem, as setas saem na diagonal, para cima. No eixo vertical, em cima da origem, elas apontam | No eixo horizontal, a coordenada vertical é zero, então as duas componentes ficam iguais: à direita da origem, as setas saem na diagonal, para cima. No eixo vertical, a seta é a coordenada vertical e menos ela: em cima da origem, as setas apontam |
| 5 | D3 | O que muda é o tamanho: a rapidez é a distância elevada a um menos dois alfa. | O que muda é o tamanho. O vetor de cima tem tamanho igual à distância, e o de baixo é a distância elevada a dois alfa. Então a rapidez é a distância elevada a um menos dois alfa. |
| 6 | D3 | E o divergente? Faz a mesma conta com a soma, e os termos se cancelam: zero, para qualquer alfa. | E o divergente? Agora é a soma: a derivada da componente horizontal na direção horizontal, mais a da vertical na direção vertical. Nas duas, só a regra da cadeia trabalha, e sai o mesmo termo, dois alfa vezes o produto das coordenadas vezes a potência com um a menos: uma vez com sinal de mais, outra com sinal de menos. Eles se cancelam: zero, para qualquer alfa. |
| 7 | D3 | Alfa zero: rotacional dois, | Alfa zero: dois menos zero, sobre a potência zero, que vale um. Rotacional dois, |
| 8 | D3 | Alfa meio: todas as setas do mesmo tamanho, e mesmo assim | Alfa meio: dois menos um, sobre a distância. Todas as setas do mesmo tamanho e, mesmo assim, |
| 9 | D3 | E alfa dois? O rotacional fica negativo. | E alfa dois? Dois menos quatro dá menos dois: o rotacional fica negativo. |
| 10 | D3 | Faz as contas de novo, e os papéis se trocam: | A componente horizontal nova é a vertical antiga, e a vertical nova é menos a horizontal antiga. Então o divergente novo é exatamente a conta do rotacional antigo, e os papéis se trocam: |
| 11 | D3b | Tudo cancela. Um gradiente nunca gira. | Tudo cancela. No plano, só sobra a terceira componente, e ela também zera. Um gradiente nunca gira. |
| 12 | D3b | o divergente desse rotacional. Aparecem | o divergente desse rotacional: a primeira componente é derivada na horizontal, a segunda na vertical e a terceira na profundidade. Aparecem |
| 13 | D4 | Em polares, o produto das coordenadas é a distância ao quadrado vezes metade do seno do dobro do ângulo. | Em polares, o produto das coordenadas é a distância ao quadrado vezes o cosseno e o seno do ângulo, e cosseno vezes seno é metade do seno do dobro do ângulo. |
| 14 | D4 | multiplicar a posição por um número multiplica a seta pelo mesmo número. | multiplicar a posição por um número multiplica a seta pelo mesmo número. Na conta, o número aparece ao quadrado em cima e embaixo, cancela, e sobra uma vez. |
| 15 | D4 | menos a de cima vezes a derivada de baixo. | menos a de cima vezes a derivada de baixo. A derivada de cima é duas vezes o produto das coordenadas; a de baixo, duas vezes a horizontal. |
| 16 | D4 | Na diagonal, vale meio, | Na diagonal, as duas coordenadas são iguais: duas vezes a quarta potência, sobre quatro vezes a quarta potência, meio. E vale meio |
| 17 | D5 | Só depois a gente solta o fluido. | Só depois a gente solta o fluido. Lembra das quatro medidas. Rotacional: o de baixo à esquerda menos o de cima à direita. Divergente: a diagonal somada. Primeira deformação: a diagonal subtraída. Segunda: os dois de fora da diagonal, somados. |
| 18 | D5 | Rotacional: quatro vezes a coordenada vertical. Divergente: quatro vezes a horizontal. E as duas deformações dão zero, em qualquer ponto. No ponto um, zero: rotacional zero, divergente quatro. Só cresce. No zero, um: rotacional quatro, divergente zero. Só gira. | Rotacional: duas vezes a vertical, menos menos duas vezes a vertical: quatro vezes a vertical. Divergente: duas vezes a horizontal mais duas vezes a horizontal: quatro vezes a horizontal. E as duas deformações: cada uma é um termo menos ele mesmo. Zero, em qualquer ponto. No ponto um, zero: quatro vezes zero, rotacional zero; quatro vezes um, divergente quatro. Só cresce. No zero, um: rotacional quatro, divergente zero. Só gira. |
| 19 | A1 | numa parábola. Três perguntas: | numa parábola: a componente na direção do canal é um menos o quadrado da horizontal sobre nove. No meio dá um; nas margens, a três metros, dá um menos nove nonos, zero. Três perguntas: |
| 20 | A1 | Na margem esquerda, ele vale dois terços por segundo: | Na margem esquerda, menos dois nonos vezes menos três: dois terços por segundo. |
| 21 | A1 | uma volta a cada dezenove segundos, mais ou menos. | e uma volta leva dois pi dividido por um terço, seis pi: uns dezenove segundos. |
| 22 | A2 | Segundo: rotacional zero, divergente zero, primeira deformação dois. | Segundo: a tabela tem um e zero em cima, zero e menos um embaixo. Rotacional zero, divergente um menos um, zero, e primeira deformação um menos menos um, dois. |
| 23 | A4 | Deformação zero em todo lugar quer dizer duas equações: | Deformação zero em todo lugar quer dizer duas equações. Iguala cada deformação a zero e passa um termo para o outro lado: |
| 24 | A4 | O nosso campo é exatamente o quadrado do número complexo que tem a coordenada horizontal como parte real e a vertical como parte imaginária. | O nosso campo é exatamente o quadrado do número complexo que tem a coordenada horizontal como parte real e a vertical como parte imaginária. Abre o quadrado: o quadrado da horizontal, mais duas vezes a unidade imaginária vezes o produto, mais o quadrado da unidade imaginária vezes o quadrado da vertical. E o quadrado da unidade imaginária é menos um. Sobra a diferença dos quadrados na parte real e duas vezes o produto na imaginária. |
| 25 | A3 | Para ser zero, só tem um jeito: alfa igual a um. | Para ser zero, só tem um jeito: o numerador zera, dois igual a dois alfa, e alfa igual a um. |
| 26 | A3 | na direção horizontal. Dá um sobre | na direção horizontal. A derivada da distância, nessa direção, é a coordenada horizontal sobre a distância. Então dá um sobre |
| 27 | D5 | E nenhum entorta: as quinas continuam praticamente em ângulo reto. Praticamente, porque a tabela fala do que acontece no ponto, naquele instante. Um quadradinho de tamanho finito sente a tabela mudando de um canto para o outro, e pode entortar um tiquinho. | E nenhum entorta: as quinas continuam em ângulo reto. E repara: a tabela fala do que acontece no ponto, naquele instante. Um quadradinho de tamanho finito sente a tabela mudando de um canto para o outro, e os lados até se curvam, mas tão pouco que nem dá para ver. |

Regras seguidas: tom de professor de cursinho, conectivos, uma tag por trecho, sem [slowly]; nunca a letra solta (as coordenadas são "a horizontal" e "a vertical"; os parâmetros são "o expoente alfa" e "o expoente"); nada de livros nem do Atlas na fala; o próximo vídeo só pelo tema. Os `[PAUSA NA TELA]` não são silêncio: a voz continua (WAV contínuo); a tag `PAUSE E TENTE` aparece enquanto a fala diz "pausa o vídeo e tenta".

### H · Gancho

[curious] Três fórmulas, três quadradinhos de fluido. Um vai girar. Outro vai mudar de área. E um vai entortar. [thoughtful] A pergunta é: dá para saber qual é qual só olhando a fórmula, antes de soltar o fluido? Dá. E hoje é você que vai fazer isso. [excited] E depois a gente vai usar exatamente as mesmas contas para responder uma pergunta que parece de outro mundo: por que o campo magnético de um fio enfraquece com um sobre a distância, e o campo de uma carga, com um sobre a distância ao quadrado? Não é decoreba. É o rotacional e o divergente escolhendo a lei.

### A · Bem-vindos

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Esse é o quarto episódio da nossa série de Cálculo três, e hoje é dia de colocar a mão na massa: o integrador do módulo, só com exercícios. [thoughtful] Vai ser uma escada. Cada degrau usa uma ferramenta e deixa uma peça para o degrau seguinte. Primeiro, ler uma fórmula de dois jeitos: como transformação e como campo. Depois, uma família inteira de redemoinhos, com o rotacional e o divergente, e duas regras que valem para qualquer campo. Aí vem um campo que não melhora de perto, para testar limite, continuidade e derivadas parciais. E, no topo da escada, o desafio do episódio passado: montar a tabela e prever o quadradinho. [curious] Na segunda parte, as aplicações: um rio, um jato batendo numa parede, mapas que não entortam e as leis do um sobre a distância. [happy] Então pega papel e caneta. Toda vez que aparecer um enunciado, pausa o vídeo e tenta antes de ver a resolução.

### D1 · Mesma fórmula, dois filmes

[thoughtful] Primeiro degrau. Uma função que recebe um par de números e devolve outro par: na primeira coordenada, a soma dos dois; na segunda, a diferença. Primeiro, como transformação. No plano da esquerda fica o ponto de partida; no da direita, onde ele vai parar. Três itens: a imagem de uma reta, de um quadrado e de um círculo. Pausa o vídeo e tenta.

[curious] Começa por uma reta: o eixo horizontal da esquerda, onde o segundo número é zero. Aí a soma e a diferença ficam iguais ao primeiro número, e as duas coordenadas da direita saem iguais. O eixo vai parar na diagonal.

[thoughtful] Agora o quadrado de lado um. Como essa transformação é linear, ela leva segmento em segmento, então basta transformar os quatro cantos. A origem fica parada. O canto um, zero: a soma dá um mais zero, e a diferença, um menos zero. Ele vai para um, um. O canto um, um vai para dois, zero. E o canto zero, um vai para um, menos um. Liga os pontos: é um quadrado de novo, girado quarenta e cinco graus, com lado raiz de dois, a distância da origem até o ponto um, um. A área era um; agora é raiz de dois ao quadrado: dois. E olha a ordem dos cantos: na esquerda, eles davam a volta no sentido anti-horário; na direita, dão no horário. O quadrado foi espelhado.

[curious] E um círculo em volta da origem? Soma ao quadrado mais diferença ao quadrado. Abre os dois quadrados: num aparece mais duas vezes o produto, no outro, menos duas vezes o produto. Esses termos cruzados se cancelam, e sobra duas vezes a soma dos quadrados. Então a distância até a origem fica multiplicada por raiz de dois, e o círculo vira um círculo com o raio multiplicado por raiz de dois. E, como a área vai com o quadrado do raio, ela também dobra.

[thoughtful] Agora a mesma fórmula, lida como campo. Em cada ponto do plano, você pendura a seta com a soma e a diferença das coordenadas daquele ponto. No eixo horizontal, a coordenada vertical é zero, então as duas componentes ficam iguais: à direita da origem, as setas saem na diagonal, para cima. No eixo vertical, a seta é a coordenada vertical e menos ela: em cima da origem, as setas apontam para a direita e para baixo; embaixo, para a esquerda e para cima.

[curious] E aqui fica uma pergunta que eu vou guardar para o topo da escada. Como transformação, a área dobrou. Como campo, se a gente soltar um pedacinho de fluido nessas setas, a área dele também dobra? Guarda o seu palpite.

### D2 · Desenhar sem desenhar mil setas

[thoughtful] Segundo degrau: desenhar um campo sem calcular mil setas. O campo é este: a componente horizontal vale sempre um, e a vertical vale a coordenada horizontal menos a vertical. Pausa o vídeo e tenta desenhar.

[curious] O truque é procurar onde o campo não muda. A componente horizontal nunca muda. A vertical só depende da diferença entre as coordenadas. Então, em cima de uma reta onde essa diferença é constante, a seta é a mesma em todo ponto. E essas retas são as paralelas à diagonal.

[thoughtful] Na própria diagonal, a diferença é zero: a seta é um, zero, deitada, apontando para a direita. Uma reta abaixo, onde a diferença vale um: a seta é um, um, a quarenta e cinco graus. Mais uma abaixo, diferença dois: um, dois, mais empinada. E, acima da diagonal, a diferença fica negativa, e as setas apontam para baixo.

[curious] Agora é só copiar: uma seta por reta, repetida ao longo da reta inteira. E o campo inteiro está desenhado: setas que vão empinando à medida que você desce de reta em reta, e que se inclinam para baixo quando você sobe.

[thoughtful] Grava esse desenho, porque ele vai voltar. Esse empinar de reta em reta é uma derivada, e no topo da escada a gente vai ler isso numa tabela.

### D3 · A família de redemoinhos

[thoughtful] Terceiro degrau: uma família inteira de redemoinhos de uma vez. Começa pelo redemoinho do primeiro episódio, menos a coordenada vertical na primeira componente e a horizontal na segunda, e divide tudo pela distância ao quadrado elevada a um expoente alfa. Cada valor do expoente alfa é um redemoinho diferente. Pausa o vídeo e tenta: o que muda com alfa zero, meio e um?

[curious] As setas são sempre tangentes às circunferências em volta da origem, então tudo dá a volta no sentido anti-horário. O que muda é o tamanho. O vetor de cima tem tamanho igual à distância, e o de baixo é a distância elevada a dois alfa. Então a rapidez é a distância elevada a um menos dois alfa. Com alfa zero, a rapidez cresce com a distância: é o disco girando rígido. Com alfa meio, a rapidez vale um em todo lugar. Com alfa um, ela cai com um sobre a distância: é o vórtice.

[thoughtful] Agora a conta do rotacional: a derivada da componente vertical na direção horizontal, menos a derivada da componente horizontal na direção vertical. A componente vertical é a coordenada horizontal vezes a distância ao quadrado elevada a menos alfa. Regra do produto: a primeira parte dá a própria potência; a segunda, pela regra da cadeia, dá menos alfa vezes a potência com um a menos no expoente, vezes duas vezes a coordenada horizontal, vezes a coordenada horizontal de novo. Põe a potência com um a menos em evidência: sobra a distância ao quadrado menos dois alfa vezes o quadrado da coordenada horizontal. A outra derivada é igualzinha, com a vertical no lugar da horizontal e o sinal trocado. Na subtração, a distância ao quadrado aparece duas vezes, e os dois termos com alfa se juntam em dois alfa vezes a soma dos quadrados, que é a distância ao quadrado de novo. Sobra uma fórmula curtinha: dois menos dois alfa, dividido pela distância ao quadrado elevada a alfa. E o divergente? Agora é a soma: a derivada da componente horizontal na direção horizontal, mais a da vertical na direção vertical. Nas duas, só a regra da cadeia trabalha, e sai o mesmo termo, dois alfa vezes o produto das coordenadas vezes a potência com um a menos: uma vez com sinal de mais, outra com sinal de menos. Eles se cancelam: zero, para qualquer alfa. Nenhum desses redemoinhos muda a área do fluido.

[curious] Agora lê a fórmula. Alfa zero: dois menos zero, sobre a potência zero, que vale um. Rotacional dois, o giro do disco rígido. Alfa meio: dois menos um, sobre a distância. Todas as setas do mesmo tamanho e, mesmo assim, o rotacional é um sobre a distância. O quadradinho gira, e gira mais quanto mais perto do centro. Alfa um: dois menos dois dá zero. As partículas dão a volta, e o quadradinho não gira: o vórtice do segundo episódio.

[excited] E alfa dois? Dois menos quatro dá menos dois: o rotacional fica negativo. As setas continuam dando a volta no sentido anti-horário, e o quadradinho gira no sentido horário! Olha por quê: a seta do lado de dentro é bem mais forte que a do lado de fora, então a borda de dentro do quadradinho corre na frente, e ele vira para trás. O sentido da volta não é o sentido do giro.

[thoughtful] E na origem? Todos esses campos dividem por zero lá, então a pergunta é se existe limite. Com alfa zero, não tem divisão nenhuma: é o disco rígido, já definido e contínuo na origem. Com alfa entre zero e meio, a fórmula não vale no centro, mas a rapidez vai a zero quando você chega nele. Então o limite é o vetor nulo e, definindo a seta da origem como zero, o campo fica contínuo. Com alfa meio, a rapidez fica um, mas a direção depende do caminho por onde você chega: não tem limite. E, com alfa maior que meio, a seta explode.

[curious] Último item: gira cada seta noventa graus, no sentido horário. O redemoinho vira uma explosão, com as setas apontando para fora. A componente horizontal nova é a vertical antiga, e a vertical nova é menos a horizontal antiga. Então o divergente novo é exatamente a conta do rotacional antigo, e os papéis se trocam: o rotacional vira zero, e o divergente vira os mesmos dois menos dois alfa sobre a distância ao quadrado elevada a alfa. Com alfa um, é a falsa fonte do segundo episódio. [thoughtful, emphatic] Guarda essa fórmula: dois menos dois alfa. Ela ainda vai escolher uma lei da física.

### D3b · Duas regras para qualquer campo

[thoughtful] Antes de subir, duas regras que valem para qualquer campo. Primeira: pega um campo que é o gradiente de uma função, ou seja, as componentes são as derivadas parciais dessa função. Calcula o rotacional. A primeira componente é a derivada em relação à vertical da derivada em relação à profundidade, menos a derivada em relação à profundidade da derivada em relação à vertical. E as outras duas componentes têm a mesma cara: uma derivada mista, menos a mesma derivada mista com a ordem trocada. E, se a função é de classe cê dois, as derivadas mistas são iguais: é o teorema de Schwarz. Tudo cancela. No plano, só sobra a terceira componente, e ela também zera. Um gradiente nunca gira.

[curious] Lembra do campo que esticava o quadradinho no episódio passado? Ele é o gradiente da metade da diferença entre os quadrados das coordenadas. Por isso o quadradinho deformava, mas não girava.

[thoughtful] Segunda regra, agora no espaço, com três componentes. Calcula o rotacional de um campo e, depois, o divergente desse rotacional: a primeira componente é derivada na horizontal, a segunda na vertical e a terceira na profundidade. Aparecem seis derivadas mistas, e elas se cancelam aos pares, de novo por Schwarz. Um rotacional nunca diverge.

[curious] E isso vira teste. Alguém te dá este campo e pergunta: existe outro campo cujo rotacional é ele? Não precisa procurar. Calcula o divergente: a primeira parcela dá seno, a segunda dá menos seno, e a terceira dá um. Total: um. Se ele fosse um rotacional, o divergente teria que ser zero. Então não existe.

[thoughtful] E isso aparece na física. O campo magnético tem divergente zero em todo lugar: é a lei que diz que não existe polo magnético isolado. E, no espaço todo, isso permite escrever o campo magnético como o rotacional de outro campo, o potencial vetor. As duas ideias andam juntas, e a regra de hoje prova uma das metades: todo rotacional tem divergente zero.

[thoughtful, emphatic] E repara na hipótese: classe cê dois. Sem derivadas contínuas, a ferramenta pode falhar. No próximo degrau, a gente vê de perto o que acontece quando falta regularidade.

### D4 · O campo que não melhora de perto

[thoughtful] Quarto degrau, o mais difícil da escada. Este campo pega o vetor posição e multiplica pelo produto das coordenadas, dividido pela distância ao quadrado. Na origem, onde a fórmula divide por zero, a gente define a seta como zero.

[curious] Olha o desenho. Nas diagonais de subida, as setas apontam para fora. Nas outras diagonais, apontam para dentro. E, em cima dos eixos, não tem seta, porque o produto das coordenadas é zero. Pausa o vídeo e tenta os cinco itens.

[thoughtful] Item a: existe limite na origem? Calcula o tamanho da seta. O vetor posição tem tamanho igual à distância, então a seta tem tamanho igual ao módulo do produto das coordenadas, dividido pela distância. Em polares, o produto das coordenadas é a distância ao quadrado vezes o cosseno e o seno do ângulo, e cosseno vezes seno é metade do seno do dobro do ângulo. Então o tamanho da seta é a distância vezes metade do módulo desse seno, e isso nunca passa da metade da distância.

[curious] Agora o desafio do épsilon. Alguém escolhe um épsilon. Você responde com delta igual a dois épsilon. Se o ponto está a menos de delta da origem, a seta tem tamanho de no máximo a metade disso, ou seja, menos que épsilon. Venceu, para qualquer épsilon. O limite é o vetor nulo.

[thoughtful] Item b: é contínuo? O ponto está no domínio, porque a gente definiu a seta lá. O limite existe. E é igual à seta do ponto, zero. Os três pedaços passam: contínuo. Item c: as derivadas parciais na origem. Andando pelo eixo horizontal, a seta é zero o caminho todo: derivada zero. Pelo vertical, a mesma coisa. A tabela é toda zero: rotacional zero, divergente zero, deformação zero. A previsão seria: perto da origem, nada acontece.

[curious] Item d: confere com um zoom. No episódio passado, o zoom de dez vezes no campo da aula deixava as setas arrumadinhas, iguais ao modelo linear. Aqui, olha: o zoom de dez vezes dá exatamente o mesmo desenho. E o de cem vezes, também. Esse campo é homogêneo: multiplicar a posição por um número multiplica a seta pelo mesmo número. Na conta, o número aparece ao quadrado em cima e embaixo, cancela, e sobra uma vez. Então ele nunca fica parecido com a tabela, por mais perto que você chegue. Na diagonal, a seta tem sempre metade do tamanho do passo: o erro da tabela, dividido pelo passo, fica em meio e não vai a zero. Para o campo ser diferenciável na origem, essa razão teria que ir a zero. Não vai. Em qualquer vizinhança, por menor que seja, tem quadradinho crescendo nas diagonais de subida, encolhendo nas outras, e girando para os dois lados.

[thoughtful, emphatic] A tabela errou. E por quê? Item e: calcula a derivada da componente horizontal na direção horizontal, fora da origem. A componente horizontal é o quadrado da coordenada horizontal vezes a vertical, sobre a distância ao quadrado. Regra do quociente: no numerador, a derivada de cima vezes a de baixo, menos a de cima vezes a derivada de baixo. A derivada de cima é duas vezes o produto das coordenadas; a de baixo, duas vezes a horizontal. Os termos com a quarta potência se cancelam, e sobra duas vezes a coordenada horizontal vezes o cubo da vertical, sobre a distância à quarta. Agora olha essa derivada perto da origem. Nos eixos, ela vale zero. Na diagonal, as duas coordenadas são iguais: duas vezes a quarta potência, sobre quatro vezes a quarta potência, meio. E vale meio e vale meio na diagonal inteira, por mais perto que você chegue. Ela não é contínua na origem. O campo não é de classe cê um, e a tabela perde a garantia. Repara: o cê um é uma garantia, não uma exigência. Tem campo que não é cê um e mesmo assim é bem aproximado pela tabela. Só que aqui a gente provou, direto, que a aproximação falha.

[curious] E olha a escada: no episódio passado, o campo encrenqueiro nem era contínuo. Este é contínuo, tem as duas derivadas parciais e, mesmo assim, engana. Ter derivadas parciais não basta para a tabela descrever o campo de perto.

### D5 · O desafio prometido

[excited] Topo da escada! Chegou a hora do desafio do episódio passado. Três campos. Para cada um: monta a tabela, lê os quatro números e prevê se o quadradinho gira, muda de área ou deforma. Só depois a gente solta o fluido. Lembra das quatro medidas. Rotacional: o de baixo à esquerda menos o de cima à direita. Divergente: a diagonal somada. Primeira deformação: a diagonal subtraída. Segunda: os dois de fora da diagonal, somados.

[thoughtful] Primeiro campo: a fórmula do primeiro degrau, a soma e a diferença das coordenadas. Pausa o vídeo e tenta.

[thoughtful] A tabela. A componente horizontal é a soma, então as derivadas dela são um e um. A vertical é a diferença: um e menos um. Em cima, um e um; embaixo, um e menos um. Agora as medidas. Rotacional: o de baixo à esquerda menos o de cima à direita, um menos um, zero. Divergente: a diagonal, um mais menos um, zero. Primeira deformação: um menos menos um, dois. Segunda: um mais um, dois. Previsão: não gira, não muda de área, só deforma.

[curious] Solta. O quadradinho estica numa direção, um pouco acima do eixo horizontal, achata na outra, e a área fica igual o tempo todo.

[excited] E aí está a resposta do palpite. Como transformação, essa fórmula dobrava a área. Como campo, ela não muda a área nenhuma. Por quê? Porque são dois filmes diferentes. A transformação leva cada ponto, de uma vez, para a imagem. O campo é uma velocidade: o fluido anda devagarinho, seguindo as setas, e quem mede a taxa de área desse fluido é o divergente, que aqui é zero. O fator de área de uma transformação é outro número, que vai aparecer quando a gente estudar mudança de variáveis.

[thoughtful] Segundo campo: o do segundo degrau, um na horizontal e a diferença na vertical. Pausa e tenta.

[thoughtful] A componente horizontal é constante: derivadas zero e zero. A vertical: um na direção horizontal e menos um na vertical. Tabela: zero e zero em cima; um e menos um embaixo. Rotacional: um menos zero, um. Divergente: zero mais menos um, menos um. Deformações: zero menos menos um, um; e um mais zero, um. Previsão: tudo junto. Gira no sentido anti-horário, encolhe e entorta.

[curious] E dava para ler isso no desenho do segundo degrau: andando para a direita, a seta empina, e esse é o um embaixo à esquerda. Andando para cima, a seta abaixa, e esse é o menos um. Solta: o quadradinho viaja para a direita, porque a seta do centro não é zero, e, no caminho, gira, encolhe e entorta. A viagem não está na tabela, porque a gente tirou a seta do centro. A tabela conta o que acontece com a forma.

[thoughtful] Terceiro campo: a primeira componente é a diferença dos quadrados das coordenadas; a segunda, duas vezes o produto delas. Agora a tabela não é constante. Derivando a diferença dos quadrados, sai duas vezes a coordenada horizontal na direção horizontal, e menos duas vezes a vertical na direção vertical: essa é a primeira linha. Derivando duas vezes o produto, sai duas vezes a vertical na direção horizontal, e duas vezes a horizontal na direção vertical: a segunda linha. Então o ponto importa. Pausa o vídeo e prevê nos três pontos: um, zero; zero, um; e um, um.

[curious] Rotacional: duas vezes a vertical, menos menos duas vezes a vertical: quatro vezes a vertical. Divergente: duas vezes a horizontal mais duas vezes a horizontal: quatro vezes a horizontal. E as duas deformações: cada uma é um termo menos ele mesmo. Zero, em qualquer ponto. No ponto um, zero: quatro vezes zero, rotacional zero; quatro vezes um, divergente quatro. Só cresce. No zero, um: rotacional quatro, divergente zero. Só gira. No um, um: gira e cresce.

[excited] Solta os três! Um cresce sem girar, um gira sem crescer, e o terceiro faz as duas coisas. E nenhum entorta: as quinas continuam em ângulo reto. E repara: a tabela fala do que acontece no ponto, naquele instante. Um quadradinho de tamanho finito sente a tabela mudando de um canto para o outro, e os lados até se curvam, mas tão pouco que nem dá para ver. Bem pequeno, esse campo nunca deforma um quadradinho. Guarda isso, porque ele tem nome, e vai aparecer na segunda parte.

[thoughtful, emphatic] Desafio cumprido. A fórmula do campo vira uma tabela, a tabela vira quatro números, e os quatro números contam o que acontece com um quadradinho bem pequeno, logo que você solta. E o cê um garante que essa leitura vale.

### P2 · Transição

[excited] Pronto: você já prevê um quadradinho só olhando a fórmula. Agora vem a melhor parte. Essas contas não ficam no papel. Elas descrevem água de verdade e escolhem leis da física. [thoughtful] Vamos começar por um rio.

### A1 · O rio

[thoughtful] Um canal de margens retas, com seis metros de largura. A água corre a um metro por segundo no meio, e a velocidade vai caindo até zero nas margens, numa parábola: a componente na direção do canal é um menos o quadrado da horizontal sobre nove. No meio dá um; nas margens, a três metros, dá um menos nove nonos, zero. Três perguntas: a água é incompressível? O escoamento gira? E onde o atrito é maior? Pausa o vídeo e tenta.

[curious] Primeira: a velocidade só tem a componente na direção do canal, e ela não muda ao longo do canal. Divergente zero: incompressível.

[thoughtful] Segunda: as linhas de corrente são retas, então dá vontade de dizer que não gira. Mas faz a conta. O rotacional é a derivada da componente na direção do canal, tomada na direção de uma margem para a outra: dá menos dois nonos da coordenada horizontal. Na margem esquerda, menos dois nonos vezes menos três: dois terços por segundo. um galho ali gira no sentido anti-horário. E lembra que o rotacional é o dobro da velocidade angular da rodinha: o galho gira a um terço de radiano por segundo, e uma volta leva dois pi dividido por um terço, seis pi: uns dezenove segundos. Na margem direita, menos dois terços: gira no horário. E, bem no meio, zero: o galho desce o rio sem girar.

[curious] Olha os três quadradinhos. O do meio só viaja. Os das margens viajam, entortam e giram, cada um para um lado. Por quê? Perto da margem, a água do lado de dentro corre mais rápido que a do lado de fora, então a borda de dentro do quadradinho vai na frente.

[thoughtful] Terceira: o atrito. No episódio passado a gente viu que, num fluido como a água, o atrito viscoso vem da deformação: aqui, da diferença de velocidade entre camadas vizinhas. Aqui, a primeira deformação é zero, e a segunda é aquele mesmo menos dois nonos da coordenada horizontal. Máxima nas margens e zero no meio. É perto das margens que a água mais esfrega em si mesma.

### A2 · Água batendo na parede

[thoughtful] Segundo problema: um jato de água descendo e batendo numa parede, como a água da torneira batendo na pia. Num modelo ideal, perto do ponto do choque, a velocidade tem a coordenada horizontal na primeira componente e menos a vertical na segunda. É o campo do gancho do episódio passado, agora só na metade de cima, com a parede embaixo.

[curious] Primeiro: na parede, a componente vertical é zero. A água não atravessa a parede: ela desliza. Numa parede de verdade, uma camada fina de água gruda nela por causa da viscosidade, e esse modelo ideal ignora essa camada. Segundo: a tabela tem um e zero em cima, zero e menos um embaixo. Rotacional zero, divergente um menos um, zero, e primeira deformação um menos menos um, dois. A água não gira e não comprime: só deforma. Uma gota de tinta que desce pelo eixo se achata e se espalha pela parede, sempre com a mesma área. E as linhas de corrente são hipérboles, as curvas onde o produto das coordenadas é constante. Confere: andando com a água, o produto muda pela velocidade horizontal vezes a coordenada vertical, mais a horizontal vezes a velocidade vertical. Dá o produto menos o produto: zero. O produto não muda: a água anda em cima da hipérbole.

[thoughtful] Terceiro: esse campo é o gradiente da metade da diferença dos quadrados das coordenadas. Essa função tem nome: potencial de velocidade. E o laplaciano dela, aquela curiosidade do segundo episódio, dá um menos um: zero.

[thoughtful, emphatic] E isso não é coincidência. Se a velocidade é um gradiente, ela é irrotacional, pela primeira das duas regras. Se, além disso, o divergente é zero, então o divergente do gradiente é zero. E o divergente do gradiente é o laplaciano. Escoamento irrotacional e incompressível quer dizer laplaciano do potencial igual a zero: a equação de Laplace. A mesma equação aparece no potencial elétrico numa região sem cargas e na temperatura de uma chapa em equilíbrio.

### A4 · Mapas que não entortam

[curious] Lembra do terceiro campo do desafio, aquele que nunca entorta? Vamos ver por quê. Deformação zero em todo lugar quer dizer duas equações. Iguala cada deformação a zero e passa um termo para o outro lado: a derivada horizontal da primeira componente igual à derivada vertical da segunda, e a derivada vertical da primeira igual a menos a derivada horizontal da segunda. Essas duas equações têm nome: equações de Cauchy-Riemann.

[thoughtful] Elas aparecem quando você junta as duas componentes num número complexo. O nosso campo é exatamente o quadrado do número complexo que tem a coordenada horizontal como parte real e a vertical como parte imaginária. Abre o quadrado: o quadrado da horizontal, mais duas vezes a unidade imaginária vezes o produto, mais o quadrado da unidade imaginária vezes o quadrado da vertical. E o quadrado da unidade imaginária é menos um. Sobra a diferença dos quadrados na parte real e duas vezes o produto na imaginária. E toda função complexa derivável satisfaz essas equações: o cubo, a exponencial, todas.

[curious] Agora lê como transformação. Onde a derivada complexa não é zero, uma tabela assim só gira e muda a escala: quadradinhos pequenos viram quadradinhos, maiores ou menores, mas sempre com ângulos retos. Isso se chama mapa conforme. E você conhece um: o mapa-múndi de Mercator, aquele de parede de sala de aula, preserva os ângulos. Por isso a Groenlândia aparece quase do tamanho da África, mas com o formato certo em cada pedacinho.

[thoughtful] E o irmão desse campo, com o sinal da segunda componente trocado, faz o contrário: rotacional zero, divergente zero, só deformação.

### A3 · Por que um sobre a distância

[excited] E agora, o último problema, que fecha a escada inteira. Um fio comprido, com corrente, atravessando a tela. As linhas do campo magnético são circunferências em volta dele. A pergunta é: com que lei o campo enfraquece quando você se afasta? Pausa e pensa.

[thoughtful] A física diz duas coisas. Primeira, a simetria: o campo dá a volta no fio, e o tamanho só depende da distância. Supondo uma lei de potência, ele tem a forma do terceiro degrau: menos a coordenada vertical e a horizontal, divididas pela distância ao quadrado elevada a um expoente alfa que a gente não sabe. Segunda: fora do fio não tem corrente e, para campos que não mudam no tempo, a lei de Ampère diz que, onde não tem corrente, o rotacional do campo magnético é zero.

[curious] Agora usa a fórmula que a gente guardou. O rotacional é dois menos dois alfa, sobre a distância ao quadrado elevada a alfa. Para ser zero, só tem um jeito: o numerador zera, dois igual a dois alfa, e alfa igual a um. Então o tamanho do campo é a distância dividida pela distância ao quadrado: um sobre a distância. O campo do fio cai com um sobre a distância. A intensidade ainda depende da corrente; o que a conta escolhe é como ela cai.

[thoughtful] Faz o mesmo com um fio carregado. O campo elétrico aponta para fora, então ele é a explosão do terceiro degrau. Fora do fio não tem carga, e a lei de Gauss diz que o divergente é zero. Divergente: dois menos dois alfa, de novo. Alfa um, e o campo também cai com um sobre a distância.

[excited] E uma carga pontual, no espaço? Escreve o campo como o vetor posição dividido pela distância elevada a um expoente. No plano, o divergente seria dois menos esse expoente. Faz a conta de uma parcela: a derivada da coordenada horizontal sobre a distância elevada ao expoente, na direção horizontal. A derivada da distância, nessa direção, é a coordenada horizontal sobre a distância. Então dá um sobre a distância elevada ao expoente, menos o expoente vezes o quadrado da coordenada horizontal, sobre a distância elevada ao expoente mais dois. As outras parcelas são iguais, cada uma com a sua coordenada. Agora soma: os três primeiros termos dão três; e os quadrados das coordenadas somam a distância ao quadrado, que cancela o mais dois do expoente. Sobra o número de parcelas menos o expoente. No plano são duas parcelas; no espaço, três. Então o divergente no espaço é três menos o expoente, dividido pela distância elevada ao expoente. Para zerar, o expoente é três, e o tamanho do campo fica um sobre a distância ao quadrado. A lei do inverso do quadrado, a de Coulomb e a da gravitação.

[thoughtful, emphatic] No plano, o número que aparece é dois; no espaço, é três. O expoente da lei vem da dimensão do espaço: em três dimensões, o campo tem mais lugar para se espalhar. E fica o cuidado: não é o rotacional ou o divergente sozinhos que decidem a lei. É a lei física, o rotacional zero ou o divergente zero fora da fonte, junto com a simetria: as linhas em círculo em volta do fio e o campo radial em volta da carga. Com as duas juntas, não sobra escolha.

### S · Síntese, gancho e CTA

[thoughtful] Olha a escada inteira. A mesma fórmula conta dois filmes, e é o divergente que mede a área do fluido. Um campo se desenha pelas curvas onde ele não muda. O rotacional de um redemoinho e o divergente de uma explosão saem da mesma conta, e o sentido da volta não é o sentido do giro. Um gradiente nunca gira, e um rotacional nunca diverge. Ter derivadas parciais não basta: a tabela só vale quando elas são contínuas. E, com ela, você prevê o quadradinho antes de soltar. [curious] E nas aplicações: um rio reto que gira nas margens, uma parede onde a água só se deforma, mapas que nunca entortam, e o rotacional e o divergente escolhendo o um sobre a distância e o um sobre a distância ao quadrado.

[excited] No próximo vídeo, a gente troca de pergunta. Até aqui, tudo foi medido num ponto, bem de perto. Agora é hora de somar pedacinhos. Uma chapa quadrada, de dois metros de lado, leve num canto e cada vez mais densa até o canto oposto: qual é a massa dela? Oito quilos? Dezesseis? A resposta exata vem de uma soma de infinitos pedacinhos: a integral dupla.

[happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual degrau da escada foi o mais difícil para você? Até a próxima!

*(Na tela do gancho: cartão `NO PRÓXIMO VÍDEO` · `SOMA DE RIEMANN E INTEGRAL DUPLA` com a chapa colorida [0, 2]² e a régua da massa com `8 kg?` e `16 kg?`, as mesmas peças do yt_0029. Sem número de episódio nem Atlas. Depois, o CTA padrão.)*


---

## Anexo B · Conferência

- `verificacao/verifica_calc3_e1_sympy.py` (v1, 75 checagens): continua valendo para os números finais.
- `verificacao/verifica_calc3_e1_passos_v2.py` (novo): confere **cada linha intermediária** deste handoff (71 checagens, todas True). Rode com `python -I`; a saída está em `verifica_calc3_e1_passos_v2_saida.txt`.
- O fluxo de z² é conforme: quinas a 90° exatos; curvatura dos lados < 1 % do lado (§1.6).
