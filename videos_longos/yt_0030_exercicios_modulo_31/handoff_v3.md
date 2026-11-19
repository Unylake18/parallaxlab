# yt_0030 · CÁLCULO III · EP. 04 · Exercícios do módulo 3.1
# AVALIAÇÃO DO PREVIEW v2 + HANDOFF v3 · preview silencioso (540p, 15 fps)

2026-11-12. Produção → Claude Code. Documento **autocontido**. Ele vale junto com o handoff v2 (`yt_0030_v1_avaliacao_e_handoff_v2.md`, que vai de novo dentro do zip) e com a pasta `yt_0030_quadros_alvo_v3/` do zip: 11 quadros-alvo novos `v3_*.jpg`, a folha de contato e o gerador `sb30v3.html`, que contém as chaves v1, v2 **e** v3. Tudo o que o v2 pede e este documento não muda continua valendo (regras R1–R16, cores, layouts, MF-Tools, QA). Onde os dois divergirem, **vale este**.

Fase aberta: **preview visual silencioso v3**. Sem voz, sem SRT, sem 1080p, sem master, sem entrega, sem commit e sem push.

O pedido do Kaio, nas palavras dele: *"veja se tem alguma outra melhoria: sobreposição, didática, MF-Tools, gancho pro próximo vídeo, introdução maneira com hook."*

Mais uma regra nova do Kaio para toda a série de Cálculo: **a narração lê em voz alta os símbolos da tela** ("nem todo mundo sabe ler a linguagem da matemática"). Isso entrou na narração v3.2 (Anexo A) e muda alguns gatilhos (§4).

---

## 0. O que entregar

1. A mesma unidade `videos_longos/yt_0030_exercicios_modulo_31/`. Antes de mexer, copie o v2 para `renders/v2/` (se ainda não estiver lá) e não apague nada.
2. `renders/v3/yt_0030_preview_v3_540p15.mp4` (960×540, 15 fps, sem áudio), com o tempo da narração **v3.2** (§4 e Anexo A).
3. `renders/v3/qa/`: tudo o que o §6 pede.
4. A prancha render × alvo: os alvos v1/v2 que continuam valendo mais os 11 alvos v3 (lista no §2.0).
5. O relatório de entrega do AGENTS.md.

---

## 1. Avaliação do v2

O v2 resolveu o que o Kaio pediu no v1. A álgebra agora é passo a passo: 138 glyph maps, nenhum termo sem origem, fórmula-mãe antes do número e cancelamento em coral. Os holds acima de 6 s foram zerados e os gatilhos estão em dia. **Não mexa no que já funciona:** sistema visual, cores, quadradinho, alinhamento, a álgebra do D1 ao D5 e do A1 ao A3, e as ferramentas `alg30.py`, `holds_fala.py` e `quadros_v2.py`.

O que ainda falta está em quatro frentes: o começo (gancho e abertura), algumas telas sobrepostas, palcos vazios ou parados, e uns poucos passos que a fala diz mas a tela não mostra. Os tempos abaixo são **do preview v2**.

### 1.1 Gancho e abertura (o que o Kaio chamou de "introdução maneira com hook")

- **0:00–0:34 · gancho parado.** Os três cartões ficam estáticos com os quadradinhos tracejados. O gancho promete "um vai girar, outro vai mudar de área, um vai entortar", mas nada se mexe. Na segunda metade, o fio e a carga também aparecem parados.
- **0:34–1:28 · abertura de 54 s quase parada.** Entre 0:38 e 0:44 a tela tem só o logo e "CÁLCULO III". Depois, uma lista de texto vai aparecendo linha a linha.
- **Correção:** um gancho em forma de **jogo de pares** (três filmes em cima e três fórmulas fora de ordem embaixo; a resposta vem no D5) e uma abertura em forma de **escada**, o mesmo desenho do resumo final. Detalhes no §2 H e A.

### 1.2 Sobreposições e erros de tela

| v2 | O que aparece | Correção |
|---|---|---|
| 2:16–2:22 | O texto "O 1 E O 0 VOAM DO CANTO; O (1, 1) VOA PARA A DIREITA" aparece no vídeo. **O erro é da Produção:** era uma nota de instrução dentro do alvo `v2_d1q`. | Tirar. Nenhuma nota de alvo vai para a tela. O `v2_d1q` continua valendo **sem essa linha**. |
| 3:40 | Na troca da coluna do D1, a linha velha e a nova ficam uma em cima da outra. | A velha sai (`FadeOut` 0,3 s) e só então a nova é escrita, ou um glyph map de uma na outra. |
| 4:00–4:22 | Os rótulos (1, −2), (1, −1) e (1, 0) se amontoam no canto de cima à direita. | Alvo `v3_d2b`: cada rótulo fica em cima da sua reta, com placa, em alturas diferentes e longe da borda. |
| 12:48–12:50 | A linha "rot = … , div = … = 0 + 0 = 0" encosta na margem direita. | Conferir na auditoria que fica ≤ 1800 px. Se não couber, rot e div vão em duas linhas (o R13 permite: a coluna tem 5 linhas nesse momento). |
| 15:12 e 23:36 | O quadradinho fica todo âmbar (15:12) e o setor de z² fica todo coral (23:36). É um pulso, e o v2 §7 proíbe. | Tirar. "Acender" é só trocar a cor do **contorno** por 1–2 s. |
| 17:36–17:58 | No campo ③ aparecem buracos sem setas onde os quadradinhos e os rótulos **ainda vão** entrar. | A área livre só some quando o objeto entra: as setas debaixo dele saem no mesmo `AnimationGroup` em que ele aparece. Vale para o vídeo inteiro. |
| 19:02 | "FÓRMULA → TABELA → 4 NÚMEROS → QUADRADINHO" é escrito por cima de "SÓ CRESCE / SÓ GIRA". | Primeiro a coluna sai (os três resultados ficam só nos rótulos do palco). Depois a frase é escrita sozinha e fica pelo menos 3 s. |
| 24:06 | Uma cópia do setor de z² passa deslocada por cima do setor. | Conferir e tirar a cópia. |
| 25:42–26:08 | O rótulo "\|B\|" do gráfico encosta na linha "‖B‖ = r/r^{2α} = …", e a curva corta a fórmula. | O gráfico desce para a faixa y = 760–900 px. A fórmula fica acima de 700 px e o rótulo do eixo fica fora da coluna de texto. |
| 26:38 | As linhas de y e de z nascem empilhadas em cima da linha de x. | Cada uma nasce no próprio lugar, por um glyph map de uma cópia da linha de x em que só os x trocam de letra (§3). |
| 26:44 | O cancelamento de ‖X‖² vira um borrão branco por ~1 s. | Glyph map explícito, passo a passo (§3). |

### 1.3 Palco vazio ou parado (R15 de verdade, não só no medidor de holds)

O `holds_fala.py` mede a tela inteira, e uma fórmula sendo escrita embaixo já conta como movimento. Por isso estes trechos passaram com o **palco** parado:

| v2 | Trecho | O que pôr no palco |
|---|---|---|
| 1:28–1:50 | D1, painel direito vazio por ~22 s | Um ponto-demonstração: na frase "no da direita, onde ele vai parar", o ponto (1, 2) da esquerda voa em arco até (3, −1) na direita e fica apagado (40%) até os cantos começarem. |
| 2:46–2:58 | D1, círculo: painel direito vazio enquanto a conta é escrita | O círculo da direita (raio r√2) nasce na frase "a distância fica multiplicada por raiz de dois", a partir de uma cópia do círculo da esquerda que cresce. |
| 3:14–3:16 | D1, palco vazio enquanto o F é escrito | O campo começa a nascer junto com a fórmula, pelo eixo horizontal. |
| 4:00–4:22 | D2, palco só com a diagonal | Em "sem calcular mil setas", o palco mostra a grade de pontinhos onde iriam as setas (cor de contexto). Em "procurar onde o campo não muda", entram as retas tracejadas. Em "é só copiar", as setas enchem reta por reta. |
| 12:52–13:00 | D4, painel do zoom vazio 8 s | Na esquerda, um quadrado pequeno em volta da origem (1/10 do lado do painel) cresce até ocupar o painel da direita. O rótulo passa de "ZOOM × 1" a "× 10" e depois a "× 100", com o desenho idêntico. |
| 17:06–17:18 | D5 ②, quadradinho parado 12 s | Em "andando para a direita, a seta empina", duas setas da mesma horizontal **acendem** (só a cor, 1–2 s): a da esquerda e a da direita. Em "andando para cima, a seta abaixa", duas setas da mesma vertical. É a ligação com o D2. |
| 19:14–19:26 | Cartão "PARTE 2" quase vazio, 12 s | A escada da abertura volta (§2 P2). |
| 21:22–21:30 | A2, palco só com a parede, 8 s | Em "um jato de água descendo", o campo nasce linha a linha de cima para baixo, até a parede. |
| 23:10–24:36 | A4, **86 s** com a malha e a imagem paradas | Alvo `v3_a4` e §2 A4: a morfose por z^s, os ângulos retos marcados, o círculo pequeno e o Mercator. |
| 24:38–24:42 | A3, o fio sozinho | O campo nasce do fio para fora, em anéis. |
| 27:40–27:48 | RESUMO com uma caixa só | A escada já existe desde a abertura e só troca os rótulos (§2 S). |
| 28:24–28:30 | Cartão do próximo vídeo só com o título; depois a chapa sem a história | Alvo `v3_gan`, montado frase a frase (§2 S). |

### 1.4 Didática: a fala diz, a tela não mostra

- **D3, α = ½ na origem:** "a direção depende do caminho" só é dito. Alvo `v3_d3or`: dois caminhos chegando à origem, um por cada eixo, com a seta diferente em cada um.
- **D3, círculos r = 1, 2, 3:** estão apagados demais. Use GEO a 80%, traço de 2,5 px.
- **D3b, gradiente:** as setas estão tão densas que as curvas de nível somem. Alvo `v3_d3bg`: passo 1, curvas de nível tracejadas e setas perpendiculares a elas.
- **D4, zoom (13:12 → 13:14):** o s² aparece em cima e embaixo e some sem cancelamento visível. Corrigir com glyph map e coral (§3).
- **D4, ∂P/∂x (14:10–14:16):** a linha passa para a forma com barra "/(x²+y²)²". Fica em fração (`\dfrac`) do começo ao fim.
- **A2:** a fala diz "a água anda na hipérbole", mas o palco não desenha hipérbole nenhuma, embora o alvo `v2_a2` tivesse as hipérboles tracejadas. Alvo `v3_a2`: as hipérboles, mais a mesma gota marcada a cada 0,4 s em xy = 1.
- **A3:** "2 = 2α ⇒ α = 1" pula o passo "rot B = 0 ⇒ 2 − 2α = 0". Corrigir com glyph map (§3).
- **A3, 24:58–25:50:** uma linha branca diagonal até o fio, sem rótulo. Se for o r, ganha o rótulo "r" com placa. Se não for nada, sai.
- **Leitura dos símbolos** (regra nova): narração v3.2 e sublinhado no §4.

### 1.5 R13 no D5 (a exceção do relatório v2)

O conflito existe, mas é das linhas soltas "P = x + y: P_x = 1, P_y = 1" e "Q = …", e não das fórmulas-mãe. Resolução, alvo `v3_d5a`:

- **P e Q nascem como chaves** sob as componentes do F: `\underbrace{x+y}_{P}`, num glyph map sobre a própria linha do F.
- Cada derivada é calculada **no caminho até a célula**. Uma cópia da componente (`TransformFromCopy`) sai da chave. Um rótulo pequeno ∂/∂x a acompanha por 0,5 s. Um `TransformByGlyphMap` transforma a cópia no número (x + y → 1), que pousa na célula da J. Nada fica escrito fora da J. No campo ③ é igual: x² − y² → 2x, e assim por diante.
- A coluna fica no máximo com **F (enunciado, com as chaves) + J + 4 medidas**. O enunciado não conta como linha de conta, então são 5 linhas: o R13 é cumprido sem exceção.
- As fórmulas-mãe continuam como no v2: aparecem na apresentação do desafio e, em cada campo, são reescritas uma a uma logo antes do número (R12).

### 1.6 Fica como está

O vídeo inteiro fora do que está listado acima. Em particular: os passos da álgebra de D1, D3, D4 (limite, δ = 2ε, parciais), D5 ① ② ③, A1 e A3; a dupla "ONDE VOCÊ ANDA / A MANCHA DAS PONTAS CABE NO DISCO" do δ-ε (12:10–12:36, muito boa); os três quadradinhos do rio; os checks "DOMÍNIO ✓ LIMITE ✓ IGUAL À SETA ✓"; e o gráfico 1/r × 1/r² (27:08).

---

## 2. Bloco a bloco: o que muda

### 2.0 Alvos v3 e o que eles substituem

| Alvo v3 | Substitui | Momento |
|---|---|---|
| `52_v3_h1` | 03 `h` (v1) | Gancho, 1ª metade, estado final |
| `53_v3_h2` | `v2_h2` | Gancho, 2ª metade, estado final |
| `54_v3_ab` | 01/02 (v1) e `v2_ab2` | Abertura, escada completa |
| `55_v3_d2b` | 08 `d2b` (v1) | D2, estado final |
| `56_v3_d3or` | (novo) | D3, "e na origem?", α = ½ |
| `57_v3_d3bg` | o **palco** do `v2_i1` | D3b, primeira regra. A coluna do alvo é o estado do meio; a final continua a do `v2_i1` |
| `58_v3_d5a` | `v2_d5a` | D5 campo ①, estado final da coluna |
| `59_v3_a2` | `v2_a2` | A2, depois de "a água anda em cima da hipérbole" |
| `60_v3_a4` | `v2_a4` | A4, estado com Cauchy-Riemann |
| `61_v3_s` | 28 `s` (v1) | Resumo, estado final |
| `62_v3_gan` | 29 `gan` (v1) | Cartão do próximo vídeo, estado final |

Todos os outros alvos v1 e v2 continuam valendo como no handoff v2 (§8 dele). O `v2_d1q` vale **sem** a linha de legenda de baixo.

### H · Gancho (alvos `v3_h1`, `v3_h2`)

Fala (v3.2) e tela, frase por frase:

1. "Três quadradinhos de fluido." Os três palcos nascem com o campo em cor de contexto e um quadradinho tracejado em cada um (dois no terceiro).
2. "Um só entorta." O quadradinho do palco 1 é solto (`fl1`, ~2 s) e para no estado do alvo. A legenda "SÓ ENTORTA" é escrita.
3. "Outro gira, encolhe e entorta, tudo ao mesmo tempo." O palco 2 é solto (`fl2`), com a seta curva de giro, e a legenda é escrita.
4. "E, no terceiro campo, um gira sem crescer e o outro cresce sem girar." O palco 3 é solto (`fl3`, pontos (0, 1) e (1, 0)), com a seta curva só no (0, 1).
5. "Embaixo, três fórmulas, fora de ordem." As três caixas são escritas a caneta, na ordem ③, ①, ②, e os três "?" âmbar aparecem.
6. "A pergunta é: dá para saber qual fórmula faz qual filme…?" O título "QUAL FÓRMULA FAZ QUAL FILME?" é escrito. Os filmes **não** se repetem (laço contínuo é proibido).
7. "E depois a gente vai usar exatamente as mesmas contas…" Os cartões saem e entra o `v3_h2`. Em "campo magnético de um fio", o fio, o círculo r e a seta. Em "enfraquece com um sobre a distância", o círculo 2r é traçado e uma cópia da seta desliza até ele **encolhendo para a metade** (o "÷2" escrito). Em "carga, com um sobre a distância ao quadrado", a mesma coisa à direita, com "÷4".
8. "É o rotacional e o divergente escolhendo a lei." As duas leis embaixo (|B| ∝ 1/r, |E| ∝ 1/r²) são escritas a caneta.

O jogo de pares é **respondido no D5**: quando cada campo do desafio é fechado, a caixa da fórmula do gancho correspondente aparece pequena no canto do palco por 2 s (é uma lembrança, `FadeIn`). Não precisa voltar ao gancho.

### A · Bem-vindos (alvo `v3_ab`)

- O logo **pequeno**, à esquerda, e o título "CÁLCULO III · EXERCÍCIOS DO MÓDULO" nascem juntos com "Fala, pessoal!". Nada de tela só com o logo.
- "Vai ser uma escada…" O primeiro degrau é desenhado: a caixa (traço) e depois o ícone e o texto.
- Cada item da fala desenha um degrau: dois filmes, desenhar um campo, redemoinhos, duas regras, não melhora de perto, o desafio. Cada degrau leva ~0,8 s.
- "Depois, as aplicações:" As quatro caixas da Parte 2 aparecem a 45%, uma por nome falado.
- "Então pega papel e caneta…" A escada fica. A transição para o D1 é o degrau "DOIS FILMES" crescendo até virar o palco.
- **Ícones:** mini-campos de 64 px desenhados com as funções do próprio vídeo (o gerador mostra cada um em `icone()`), sem texto dentro. Este mesmo desenho volta no P2 e no S.

### D1

- Tirar a nota do `v2_d1q` (§1.2).
- O ponto-demonstração (§1.3).
- O círculo da direita nasce da cópia do da esquerda (§1.3).
- O campo nasce junto com a fórmula do F (§1.3).
- A troca da coluna em 3:40 sem sobreposição (§1.2).
- Leituras (Anexo A): "fi de u, v…" com sublinhado sob φ(u, v); "a setinha em cima do F" com sublinhado sob a seta do F.

### D2 (alvo `v3_d2b`)

A grade de pontinhos, depois as retas e depois as setas reta por reta (§1.3). Os rótulos ficam como no alvo. Leitura: "a seta dupla da tela lê-se implica", com sublinhado sob o ⇒.

### D3 (alvo `v3_d3or`)

- Círculos mais visíveis (§1.4).
- **Na origem, α = ½:** na frase "com alfa meio, a rapidez fica um, mas a direção depende do caminho", o ponto laranja anda pelo eixo x em direção à origem, parando em 3 posições. Em cada uma, a seta do campo acende (vertical, para cima). Depois, o ponto magenta faz o mesmo pelo eixo y (seta para a esquerda). Na coluna, as duas linhas "pelo eixo x: v → (0, 1)" e "pelo eixo y: v → (−1, 0)" são escritas, cada uma com o valor voando da seta, e depois vem "NÃO TEM LIMITE" em coral.
- Leituras: "xis ao quadrado mais ípsilon ao quadrado…" (sublinhado sob x² + y²); "P e Q… o d arredondado…" (sublinhado sob ∂Q/∂x na fórmula-mãe do rot); "limite de F quando X tende à origem" (a fórmula `\lim_{X\to 0}\vec F(X)` é escrita pequena na coluna nessa hora, se ainda não estiver).

### D3b (alvo `v3_d3bg`)

Palco do gradiente com passo 1 e curvas de nível tracejadas (hipérboles x² − y² = k e as diagonais). As setas são perpendiculares às curvas. Leituras: "nabla fi" (sublinhado sob ∇φ), "P com xis pequeno embaixo" (sublinhado sob φ_x, que é a primeira vez do índice) e "se e somente se" (sublinhado sob ⇔).

### D4

- O zoom crescendo para o painel da direita (§1.3).
- O s² cancelado (§3).
- A fração no ∂P/∂x (§1.4).
- A margem em 12:48 (§1.2).
- Leituras: "barras duplas… a norma; a barra simples é o módulo" (sublinhados sob ‖F‖ e sob |xy|); "épsilon… delta…" (sublinhados sob ε e δ na linha do desafio); "o limite, quando h tende a zero…" (sublinhado sob lim_{h→0}).

### D5 (alvo `v3_d5a`)

- R13 pela §1.5.
- Sem flash em 15:12.
- Setas acendendo no campo ② (§1.3).
- Buracos só com o objeto presente (§1.2).
- A frase-cadeia de 19:02 sozinha (§1.2).
- As caixas do gancho voltando como lembrança ao fechar cada campo (§2 H).
- Leituras: "jacobiana, a letra J" (sublinhado sob o J); "dê um", "dê dois" (sublinhado sob d₁ e d₂ na apresentação das quatro medidas).

### P2 · Transição

A escada da abertura volta, com a Parte 1 a 100%. Em "água de verdade", as caixas do rio, do jato e dos mapas acendem para 100%. Em "leis da física", acende a do 1/r. Em "Vamos começar por um rio", a caixa do rio cresce até virar o palco do A1. Nada de cartão vazio.

### A1

Fica como está. Leituras: "ômega, a velocidade angular" (sublinhado sob ω) e "o período, o T da tela" (sublinhado sob T).

### A2 (alvo `v3_a2`)

- O campo nasce de cima para baixo (§1.3).
- As hipérboles tracejadas nascem em "as linhas de corrente são hipérboles". A de xy = 1 fica em branco.
- Em "a água anda em cima da hipérbole", a gota laranja percorre a hipérbole xy = 1 deixando os pontos a cada 0,4 s, como no alvo (fluxo exato `flSela`).
- Leituras: "dê xis ípsilon, dê tê" (sublinhado sob d(xy)/dt); "nabla dois fi" (sublinhado sob ∇²φ).

### A4 (alvo `v3_a4`), o trecho que mais precisa de movimento

1. "Deformação zero em todo lugar…" Malha à esquerda, painel da direita vazio. As duas equações de Cauchy-Riemann saem de d₁ = 0 e d₂ = 0 por glyph map, embaixo, como no v2.
2. "o quadrado do número complexo…" A abertura de (x + iy)² fica como no v2. Leitura: "o i da tela é a unidade imaginária" (sublinhado sob i).
3. "Agora lê como transformação." **Morfose por z^s, com s indo de 1 a 2.** Uma cópia da malha da esquerda vai para a direita e se dobra continuamente: o ponto r·e^{iθ} vai para r^s·e^{isθ} (`zpow(s)` no gerador). Toda z^s é conforme fora da origem, então os ângulos ficam retos **durante toda a morfose**. Os três cantinhos de 90° (marcas brancas finas) andam junto com a malha. Isso substitui a imagem pronta do v2.
4. "quadradinhos pequenos viram quadradinhos…" O círculo pequeno da esquerda é copiado e vira o círculo da direita (só cresce, continua círculo).
5. "o mapa-múndi de Mercator…" A malha da direita sai e entra um **reticulado de Mercator** desenhado com linhas: meridianos verticais igualmente espaçados e paralelos em y = ln tan(π/4 + φ/2) para φ = 0°, 15°, …, 75°. Os paralelos se afastam à medida que sobem. Em três latitudes (0°, 45° e 70°), um círculo pequeno do mesmo tamanho na Terra aparece com raio proporcional a 1/cos φ: continua círculo e cresce. Na fala "a Groenlândia aparece quase do tamanho da África, mas com o formato certo", o círculo de 70° acende. Sem mapa, contorno de país ou textura: só linhas e círculos.
6. "o irmão desse campo…" Como no v2, embaixo, com "SÓ DEFORMA" longe da borda (≥ 60 px do rodapé).

### A3

- O campo nasce do fio (§1.3).
- A linha diagonal com ou sem rótulo (§1.4).
- rot B = 0 ⇒ 2 − 2α = 0 ⇒ α = 1 por glyph map (§3).
- O gráfico fora da coluna (§1.2).
- As linhas de y e de z por glyph map (§3).
- O cancelamento de ‖X‖² sem borrão (§3).
- Leitura: "o X maiúsculo é o vetor posição; as barras duplas, a distância; p, o expoente" (três sublinhados em sequência na linha do E).

### S · Síntese, gancho do próximo vídeo e CTA (alvos `v3_s`, `v3_gan`)

**Síntese.** A escada da abertura volta inteira. Cada frase da síntese troca o rótulo de um degrau, do tema para a lição (`FadeTransform` do texto, com o contorno acendendo 1 s): DOIS FILMES → MESMA FÓRMULA, DOIS FILMES; DESENHAR UM CAMPO → CURVAS ONDE NÃO MUDA; REDEMOINHOS → VOLTA ≠ GIRO; DUAS REGRAS → GRADIENTE NÃO GIRA; NÃO MELHORA DE PERTO → PARCIAIS NÃO BASTAM; O DESAFIO → A TABELA PREVÊ. Depois, as quatro da Parte 2: O RIO → RIO QUE GIRA NAS MARGENS; O JATO NA PAREDE → PAREDE: SÓ DEFORMA; MAPAS → MAPAS QUE NÃO ENTORTAM; 1/r E 1/r² → A CONTA ESCOLHE A LEI. Estado final = `v3_s`.

**Gancho do próximo vídeo (`v3_gan`).** São as mesmas peças da abertura do EP. 05, para o espectador reconhecer:

1. "No próximo vídeo, a gente troca de pergunta." O título é escrito.
2. "Agora é hora de somar pedacinhos." A chapa nasce com a cor partindo do canto (0, 0) e se espalhando.
3. "leve num canto e cada vez mais densa até o canto oposto." ρ = x² + y² é escrito e os quatro valores dos cantos (0, 4, 4, 8) aparecem.
4. "Pelo valor do centro, a massa dá oito quilos." O ponto do centro (2) acende e o 2 voa para a linha "centro: 2 · 4 m² = 8 kg". O 8 voa para a régua.
5. "Pela média dos quatro cantos, dezesseis." Os quatro valores voam para a linha dos cantos; o 16 voa para a régua.
6. "O dobro!" O texto aparece.
7. "Qual das duas está certa?" O texto aparece em menta.
8. "A resposta exata vem de somar infinitos pedacinhos: a integral dupla." Uma grade 8×8 fina é traçada sobre a chapa (traço, sem flash), como no EP. 05.

Depois, o CTA padrão, como no v2. Sem número de episódio, sem Atlas e sem a resposta (10,67 kg).

---

## 3. MF-Tools: o que muda

Tudo continua pela `alg30.py`, com `TransformByGlyphMap` de string única, cancelamento coral e `auto_fade`. São mapas novos ou corrigidos:

| # | Bloco | De → para | Como |
|---|---|---|---|
| 1 | D5 (todos os campos) | componente da chave → número na célula da J | Cópia da componente, rótulo ∂/∂x por 0,5 s e glyph map da expressão para o número. Ex.: `x+y` → `1`; `x^2-y^2` → `2x` (o 2 do expoente desce para a frente e o y² some em coral). |
| 2 | D4 zoom | `\dfrac{s^2xy}{s^2(x^2+y^2)}(sx,sy)` → `\dfrac{xy}{x^2+y^2}\,s(x,y)` | O s² de cima e o de baixo acendem em coral, são riscados e saem juntos (`auto_fade`). O s de (sx, sy) sai para fora do parêntese. |
| 3 | D4 ∂P/∂x | `\dfrac{2xy(x^2+y^2)-x^2y\cdot 2x}{(x^2+y^2)^2}` → `\dfrac{2x^3y+2xy^3-2x^3y}{(x^2+y^2)^2}` → `\dfrac{2xy^3}{(x^2+y^2)^2}` | Distributiva num mapa e o par 2x³y em coral no outro. Sempre `\dfrac`, nunca barra. |
| 4 | A3 fio | `\operatorname{rot}\vec B=\dfrac{2-2\alpha}{(\dots)^\alpha}=0` → `2-2\alpha=0` → `2=2\alpha` → `\alpha=1` | O numerador voa e o denominador sai (o "= 0" fica). O −2α atravessa a igualdade (sinal troca). Dividir por 2. Três mapas. |
| 5 | A3 carga | linha de x → linhas de y e de z | `TransformFromCopy` da linha de x para o lugar da de y, com mapa que só troca os glifos x → y (magenta). Depois o mesmo para z. Uma de cada vez; nunca empilhadas. |
| 6 | A3 carga | `\dfrac{p(x^2+y^2+z^2)}{\|X\|^{p+2}}` → `\dfrac{p\|X\|^2}{\|X\|^p\|X\|^2}` → `\dfrac{p}{\|X\|^p}` | Primeiro a soma vira ‖X‖² (com a chave "= ‖X‖²" por 1 s). Depois o expoente p + 2 se separa em p e 2. O par ‖X‖² fica coral e é riscado. Por fim, (3 − p)/‖X‖^p. Quatro mapas, nenhum com morfose livre (é o borrão de 26:44). |
| 7 | A2 | `\varphi_x=x` → `\varphi_{xx}=1` | O índice ganha o segundo x e o valor vira 1. |

Meta: ≥ 145 glyph maps no total; `TransformMatchingShapes` = 0.

---

## 4. Narração v3.2, leitura dos símbolos e tempo

### 4.1 O que mudou

A tabela A.0 (no Anexo A) lista as 23 mudanças:

- 18 trechos de leitura de símbolo (22 símbolos, Anexo B);
- o gancho novo (jogo de pares);
- o cartão do próximo vídeo com 8 × 16 kg;
- a abertura mais curta (a escada mostra o que a fala listava);
- a síntese mais curta (a escada mostra as lições).

### 4.2 Sublinhado do gatilho falado (regra nova)

Quando a voz lê um símbolo, ele ganha um **sublinhado fino**: `Underline`, 2 px, GEO, `Create` em 0,3 s no início da leitura e `FadeOut` 0,3 s no fim. Isso **não** é pulso: o símbolo não muda de cor nem de tamanho. Se o símbolo ainda não estiver na tela na hora da leitura, ele é escrito a caneta nesse momento. Lista completa no Anexo B.

### 4.3 Tempo (3 palavras/s)

| Bloco | v3.1 | v3.2 | Início | Duração |
|---|---|---|---|---|
| H | 103 | 123 | 0:00 | 41 s |
| A | 161 | 121 | 0:41 | 40 s |
| D1 | 438 | 472 | 1:21 | 157 s |
| D2 | 213 | 220 | 3:58 | 73 s |
| D3 | 756 | 797 | 5:12 | 266 s |
| D3b | 351 | 389 | 9:37 | 130 s |
| D4 | 692 | 743 | 11:47 | 248 s |
| D5 | 750 | 770 | 15:55 | 257 s |
| P2 | 36 | 36 | 20:11 | 12 s |
| A1 | 345 | 360 | 20:23 | 120 s |
| A2 | 323 | 347 | 22:23 | 116 s |
| A4 | 263 | 271 | 24:19 | 90 s |
| A3 | 550 | 565 | 25:49 | 188 s |
| S | 227 | 193 | 28:58 | 64 s |
| **Total** | **5.208** | **5.407** | | **≈ 30:02** |

- Troque o texto do `tempos.py` pelo Anexo A (v3.2) e recalcule os gatilhos.
- Duração aceita do preview: 30:02 ± 15 s. É o teto do Kaio (~30 min); não passe.
- Se algum trecho não couber, avise no relatório com os segundos que faltam e a Produção ajusta a fala.

---

## 5. O que NÃO fazer

Vale tudo do §7 do v2, mais:

- Nenhuma nota de alvo ou de instrução na tela. Legenda na tela só se o handoff disser "legenda" ou se ela estiver no alvo **e** fizer sentido para o espectador.
- Nenhum preenchimento sólido como destaque (os casos de 15:12 e 23:36).
- Nenhum mapa-múndi, contorno de país ou textura no Mercator: só linhas e círculos.
- Os filmes do gancho tocam uma vez; nada em laço.
- Não mexer nas unidades yt_0026–yt_0029. Pegue o EP. 05 só como referência visual para o cartão (as cores e a régua já estão no `v3_gan`).

---

## 6. QA do preview v3 (obrigatório)

Tudo o que o §8 do v2 pede (prancha, `origens`, `glyphmaps`, R12, R13, R5/R7/R10, holds, gatilhos, tamanho ≥ 30 px, números, PAUSE E TENTE), agora com o sufixo `_v3` e mais:

1. **Prancha** com os alvos v1/v2 que valem (§2.0) mais os 11 v3.
2. **`palco_parado_v3.txt` (novo):** a mesma medida dos holds, mas só dentro do palco (layout A: 120–1080 × 180–900; layout B: cada painel). Zero trechos > 8 s sem mudança no palco enquanto a voz fala daquele palco. Os 86 s do A4 são o caso que esta medida pega.
3. **`painel_vazio_v3.txt` (novo):** no layout B, nenhum painel vazio > 2 s depois da primeira frase que fala dele.
4. **`leituras_v3.txt` (novo):** para cada leitura do Anexo B, o tempo da palavra, o símbolo sublinhado e se ele já estava na tela. Esperado: 22/22.
5. **`R13_v3.txt`:** D5 com no máximo 5 linhas de conta (o enunciado F com as chaves não conta). Zero exceções.
6. **Sobreposição:** a auditoria de caixas também em transição. Meça nos quadros a 25%, 50% e 75% de cada `Transform`, além do estado final. Os casos de 3:40, 19:02, 24:06, 26:38 e 26:44 do v2 têm de aparecer como zero.
7. **Áreas livres:** nenhuma área sem setas antes de o objeto dela existir.
8. **Margens:** nenhum texto além de 1800 px na coluna nem a menos de 60 px do rodapé.

---

## 7. Parada

Entregue o preview v3, as pranchas, os relatórios do §6 e o relatório de entrega (arquivos alterados, verificações, caminho do preview, limitações e trechos onde o tempo apertou). Pare: não inicie voz, SRT, 1080p, master nem entrega.

---

## Anexo A · Narração v3.2

Só para tempo e gatilhos nesta fase. **Não gerar voz.** É a narração v3.1 do handoff v2 com as mudanças da tabela A.0 (leitura dos símbolos, gancho e cartão do próximo vídeo novos, abertura e síntese mais curtas).

Regras seguidas: tom de professor de cursinho, conectivos, uma tag por trecho, sem [slowly]; a letra só aparece na fala quando a voz **lê o símbolo da tela** ("na tela…", "lê-se…"); no resto, as coordenadas continuam "a horizontal" e "a vertical"; nada de livros nem do Atlas na fala; o próximo vídeo só pelo tema. Os `[PAUSA NA TELA]` não são silêncio: a voz continua (WAV contínuo); a tag `PAUSE E TENTE` aparece enquanto a fala diz "pausa o vídeo e tenta".

### A.0 · O que mudou da v3.1 para a v3.2

| # | Bloco | Tipo | v3.1 | v3.2 | Δ palavras |
|---|---|---|---|---|---|
| 1 | H | gancho | Três fórmulas, três quadradinhos de fluido. Um vai girar. Outro vai mudar de área. E um vai entortar. [thoughtful] A pergunta é: dá para saber qual é qual só olhando a fórmula, antes de soltar o fluido? | Três quadradinhos de fluido. Um só entorta. Outro gira, encolhe e entorta, tudo ao mesmo tempo. E, no terceiro campo, um gira sem crescer e o outro cresce sem girar. Embaixo, três fórmulas, fora de ordem. [thoughtful] A pergunta é: dá para saber qual fórmula faz qual filme só olhando para ela, antes de soltar o fluido? | +20 |
| 2 | A | corte | Vai ser uma escada. Cada degrau usa uma ferramenta e deixa uma peça para o degrau seguinte. Primeiro, ler uma fórmula de dois jeitos: como transformação e como campo. Depois, uma família inteira de redemoinhos, com o rotacional e o divergente, e duas regras que valem para qualquer campo. Aí vem um campo que não melhora de perto, para testar limite, continuidade e derivadas parciais. E, no topo da escada, o desafio do episódio passado: montar a tabela e prever o quadradinho. | Vai ser uma escada: cada degrau deixa uma peça para o seguinte. Ler uma fórmula de dois jeitos, desenhar um campo, uma família de redemoinhos, duas regras, um campo que não melhora de perto e, no topo, o desafio do episódio passado: prever o quadradinho. | -37 |
| 3 | A | corte | Na segunda parte, as aplicações: um rio, um jato batendo numa parede, mapas que não entortam e as leis do um sobre a distância. | Depois, as aplicações: um rio, um jato numa parede, mapas que não entortam e as leis do um sobre a distância. | -3 |
| 4 | D1 | leitura | na segunda, a diferença. Primeiro, como transformação. | na segunda, a diferença. Na tela: fi de u, v igual a u mais v, u menos v. Fi é só o nome da função. Primeiro, como transformação. | +21 |
| 5 | D1 | leitura | [thoughtful] Agora a mesma fórmula, lida como campo. | [thoughtful] Agora a mesma fórmula, lida como campo. A setinha em cima do F diz que o resultado é um vetor. | +13 |
| 6 | D2 | leitura | a seta é a mesma em todo ponto. | a seta é a mesma em todo ponto. A seta dupla da tela lê-se implica. | +7 |
| 7 | D3 | leitura | elevada a um expoente alfa. Cada valor | elevada a um expoente alfa. Xis ao quadrado mais ípsilon ao quadrado é a distância ao quadrado. Cada valor | +12 |
| 8 | D3 | leitura | [thoughtful] Agora a conta do rotacional: a derivada | [thoughtful] Agora a conta do rotacional. Na tela, P e Q são as duas componentes, e o d arredondado é a derivada parcial. O rotacional é a derivada | +20 |
| 9 | D3 | leitura | então a pergunta é se existe limite. | então a pergunta é se existe limite. Lê-se: limite de F quando X tende à origem. | +9 |
| 10 | D3b | leitura | as componentes são as derivadas parciais dessa função. | as componentes são as derivadas parciais dessa função. Na tela, nabla fi: lê-se gradiente de fi. E, daqui em diante, P com xis pequeno embaixo é a derivada parcial de P em relação a xis. | +27 |
| 11 | D3b | leitura | o rotacional de outro campo, o potencial vetor. | o rotacional de outro campo, o potencial vetor. A seta dupla nos dois sentidos lê-se se e somente se. | +11 |
| 12 | D4 | leitura | Item a: existe limite na origem? Calcula o tamanho da seta. | Item a: existe limite na origem? Calcula o tamanho da seta. As barras duplas da tela são esse tamanho, a norma; a barra simples é o módulo, o valor sem sinal. | +20 |
| 13 | D4 | leitura | Agora o desafio do épsilon. Alguém escolhe um épsilon. | Agora o desafio do épsilon. Épsilon é a tolerância na seta; delta, o raio onde você anda. Alguém escolhe um épsilon. | +12 |
| 14 | D4 | leitura | a seta é zero o caminho todo: derivada zero. | a seta é zero o caminho todo: derivada zero. Na tela, ela é o limite, quando h tende a zero, da diferença das setas dividida pelo passo h. | +19 |
| 15 | D5 | leitura | Lembra das quatro medidas. | A tabela se chama jacobiana, a letra J: derivadas de P em cima, de Q embaixo. Lembra das quatro medidas. | +16 |
| 16 | D5 | leitura | Primeira deformação: a diagonal subtraída. Segunda: os dois de fora da diagonal, somados. | Primeira deformação, dê um: a diagonal subtraída. Segunda, dê dois: os dois de fora da diagonal, somados. | +4 |
| 17 | A1 | leitura | o galho gira a um terço de radiano por segundo, e uma volta leva | o galho gira com ômega, a velocidade angular, igual a um terço de radiano por segundo. E o período, o T da tela, o tempo de uma volta, é | +15 |
| 18 | A2 | leitura | Confere: andando com a água, | Confere. Lê-se dê xis ípsilon, dê tê: a taxa de variação do produto no tempo. Andando com a água, | +14 |
| 19 | A2 | leitura | E o laplaciano dela, aquela curiosidade do segundo episódio, | E o laplaciano dela, escrito nabla dois fi, a soma das duas derivadas segundas, aquela curiosidade do segundo episódio, | +10 |
| 20 | A4 | leitura | Abre o quadrado: o quadrado da horizontal, | Abre o quadrado; o i da tela é a unidade imaginária: o quadrado da horizontal, | +8 |
| 21 | A3 | leitura | Escreve o campo como o vetor posição dividido pela distância elevada a um expoente. | Escreve o campo como o vetor posição dividido pela distância elevada a um expoente. O X maiúsculo é o vetor posição; as barras duplas, a distância; p, o expoente. | +15 |
| 22 | S | corte | [thoughtful] Olha a escada inteira. A mesma fórmula conta dois filmes, e é o divergente que mede a área do fluido. Um campo se desenha pelas curvas onde ele não muda. O rotacional de um redemoinho e o divergente de uma explosão saem da mesma conta, e o sentido da volta não é o sentido do giro. Um gradiente nunca gira, e um rotacional nunca diverge. Ter derivadas parciais não basta: a tabela só vale quando elas são contínuas. E, com ela, você prevê o quadradinho antes de soltar. [curious] E nas aplicações: um rio reto que gira nas margens, uma parede onde a água só se deforma, mapas que nunca entortam, e o rotacional e o divergente escolhendo o um sobre a distância e o um sobre a distância ao quadrado. | [thoughtful] Olha a escada inteira. A mesma fórmula conta dois filmes. Um campo se desenha pelas curvas onde ele não muda. O sentido da volta não é o sentido do giro. Um gradiente nunca gira, e um rotacional nunca diverge. Ter derivadas parciais não basta. E, com a tabela, você prevê o quadradinho antes de soltar. [curious] E, nas aplicações, um rio que gira nas margens, uma parede onde a água só deforma, mapas que nunca entortam e o um sobre a distância escolhido pela conta. | -46 |
| 23 | S | gancho | Uma chapa quadrada, de dois metros de lado, leve num canto e cada vez mais densa até o canto oposto: qual é a massa dela? Oito quilos? Dezesseis? A resposta exata vem de uma soma de infinitos pedacinhos: a integral dupla. | Uma chapa quadrada, de dois metros de lado, leve num canto e cada vez mais densa até o canto oposto. Pelo valor do centro, a massa dá oito quilos. Pela média dos quatro cantos, dezesseis. O dobro! Qual das duas está certa? A resposta exata vem de somar infinitos pedacinhos: a integral dupla. | +12 |

### H · Gancho

[curious] Três quadradinhos de fluido. Um só entorta. Outro gira, encolhe e entorta, tudo ao mesmo tempo. E, no terceiro campo, um gira sem crescer e o outro cresce sem girar. Embaixo, três fórmulas, fora de ordem. [thoughtful] A pergunta é: dá para saber qual fórmula faz qual filme só olhando para ela, antes de soltar o fluido? Dá. E hoje é você que vai fazer isso. [excited] E depois a gente vai usar exatamente as mesmas contas para responder uma pergunta que parece de outro mundo: por que o campo magnético de um fio enfraquece com um sobre a distância, e o campo de uma carga, com um sobre a distância ao quadrado? Não é decoreba. É o rotacional e o divergente escolhendo a lei.

### A · Bem-vindos

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Esse é o quarto episódio da nossa série de Cálculo três, e hoje é dia de colocar a mão na massa: o integrador do módulo, só com exercícios. [thoughtful] Vai ser uma escada: cada degrau deixa uma peça para o seguinte. Ler uma fórmula de dois jeitos, desenhar um campo, uma família de redemoinhos, duas regras, um campo que não melhora de perto e, no topo, o desafio do episódio passado: prever o quadradinho. [curious] Depois, as aplicações: um rio, um jato numa parede, mapas que não entortam e as leis do um sobre a distância. [happy] Então pega papel e caneta. Toda vez que aparecer um enunciado, pausa o vídeo e tenta antes de ver a resolução.

### D1 · Mesma fórmula, dois filmes

[thoughtful] Primeiro degrau. Uma função que recebe um par de números e devolve outro par: na primeira coordenada, a soma dos dois; na segunda, a diferença. Na tela: fi de u, v igual a u mais v, u menos v. Fi é só o nome da função. Primeiro, como transformação. No plano da esquerda fica o ponto de partida; no da direita, onde ele vai parar. Três itens: a imagem de uma reta, de um quadrado e de um círculo. Pausa o vídeo e tenta.

[curious] Começa por uma reta: o eixo horizontal da esquerda, onde o segundo número é zero. Aí a soma e a diferença ficam iguais ao primeiro número, e as duas coordenadas da direita saem iguais. O eixo vai parar na diagonal.

[thoughtful] Agora o quadrado de lado um. Como essa transformação é linear, ela leva segmento em segmento, então basta transformar os quatro cantos. A origem fica parada. O canto um, zero: a soma dá um mais zero, e a diferença, um menos zero. Ele vai para um, um. O canto um, um vai para dois, zero. E o canto zero, um vai para um, menos um. Liga os pontos: é um quadrado de novo, girado quarenta e cinco graus, com lado raiz de dois, a distância da origem até o ponto um, um. A área era um; agora é raiz de dois ao quadrado: dois. E olha a ordem dos cantos: na esquerda, eles davam a volta no sentido anti-horário; na direita, dão no horário. O quadrado foi espelhado.

[curious] E um círculo em volta da origem? Soma ao quadrado mais diferença ao quadrado. Abre os dois quadrados: num aparece mais duas vezes o produto, no outro, menos duas vezes o produto. Esses termos cruzados se cancelam, e sobra duas vezes a soma dos quadrados. Então a distância até a origem fica multiplicada por raiz de dois, e o círculo vira um círculo com o raio multiplicado por raiz de dois. E, como a área vai com o quadrado do raio, ela também dobra.

[thoughtful] Agora a mesma fórmula, lida como campo. A setinha em cima do F diz que o resultado é um vetor. Em cada ponto do plano, você pendura a seta com a soma e a diferença das coordenadas daquele ponto. No eixo horizontal, a coordenada vertical é zero, então as duas componentes ficam iguais: à direita da origem, as setas saem na diagonal, para cima. No eixo vertical, a seta é a coordenada vertical e menos ela: em cima da origem, as setas apontam para a direita e para baixo; embaixo, para a esquerda e para cima.

[curious] E aqui fica uma pergunta que eu vou guardar para o topo da escada. Como transformação, a área dobrou. Como campo, se a gente soltar um pedacinho de fluido nessas setas, a área dele também dobra? Guarda o seu palpite.

### D2 · Desenhar sem desenhar mil setas

[thoughtful] Segundo degrau: desenhar um campo sem calcular mil setas. O campo é este: a componente horizontal vale sempre um, e a vertical vale a coordenada horizontal menos a vertical. Pausa o vídeo e tenta desenhar.

[curious] O truque é procurar onde o campo não muda. A componente horizontal nunca muda. A vertical só depende da diferença entre as coordenadas. Então, em cima de uma reta onde essa diferença é constante, a seta é a mesma em todo ponto. A seta dupla da tela lê-se implica. E essas retas são as paralelas à diagonal.

[thoughtful] Na própria diagonal, a diferença é zero: a seta é um, zero, deitada, apontando para a direita. Uma reta abaixo, onde a diferença vale um: a seta é um, um, a quarenta e cinco graus. Mais uma abaixo, diferença dois: um, dois, mais empinada. E, acima da diagonal, a diferença fica negativa, e as setas apontam para baixo.

[curious] Agora é só copiar: uma seta por reta, repetida ao longo da reta inteira. E o campo inteiro está desenhado: setas que vão empinando à medida que você desce de reta em reta, e que se inclinam para baixo quando você sobe.

[thoughtful] Grava esse desenho, porque ele vai voltar. Esse empinar de reta em reta é uma derivada, e no topo da escada a gente vai ler isso numa tabela.

### D3 · A família de redemoinhos

[thoughtful] Terceiro degrau: uma família inteira de redemoinhos de uma vez. Começa pelo redemoinho do primeiro episódio, menos a coordenada vertical na primeira componente e a horizontal na segunda, e divide tudo pela distância ao quadrado elevada a um expoente alfa. Xis ao quadrado mais ípsilon ao quadrado é a distância ao quadrado. Cada valor do expoente alfa é um redemoinho diferente. Pausa o vídeo e tenta: o que muda com alfa zero, meio e um?

[curious] As setas são sempre tangentes às circunferências em volta da origem, então tudo dá a volta no sentido anti-horário. O que muda é o tamanho. O vetor de cima tem tamanho igual à distância, e o de baixo é a distância elevada a dois alfa. Então a rapidez é a distância elevada a um menos dois alfa. Com alfa zero, a rapidez cresce com a distância: é o disco girando rígido. Com alfa meio, a rapidez vale um em todo lugar. Com alfa um, ela cai com um sobre a distância: é o vórtice.

[thoughtful] Agora a conta do rotacional. Na tela, P e Q são as duas componentes, e o d arredondado é a derivada parcial. O rotacional é a derivada da componente vertical na direção horizontal, menos a derivada da componente horizontal na direção vertical. A componente vertical é a coordenada horizontal vezes a distância ao quadrado elevada a menos alfa. Regra do produto: a primeira parte dá a própria potência; a segunda, pela regra da cadeia, dá menos alfa vezes a potência com um a menos no expoente, vezes duas vezes a coordenada horizontal, vezes a coordenada horizontal de novo. Põe a potência com um a menos em evidência: sobra a distância ao quadrado menos dois alfa vezes o quadrado da coordenada horizontal. A outra derivada é igualzinha, com a vertical no lugar da horizontal e o sinal trocado. Na subtração, a distância ao quadrado aparece duas vezes, e os dois termos com alfa se juntam em dois alfa vezes a soma dos quadrados, que é a distância ao quadrado de novo. Sobra uma fórmula curtinha: dois menos dois alfa, dividido pela distância ao quadrado elevada a alfa. E o divergente? Agora é a soma: a derivada da componente horizontal na direção horizontal, mais a da vertical na direção vertical. Nas duas, só a regra da cadeia trabalha, e sai o mesmo termo, dois alfa vezes o produto das coordenadas vezes a potência com um a menos: uma vez com sinal de mais, outra com sinal de menos. Eles se cancelam: zero, para qualquer alfa. Nenhum desses redemoinhos muda a área do fluido.

[curious] Agora lê a fórmula. Alfa zero: dois menos zero, sobre a potência zero, que vale um. Rotacional dois, o giro do disco rígido. Alfa meio: dois menos um, sobre a distância. Todas as setas do mesmo tamanho e, mesmo assim, o rotacional é um sobre a distância. O quadradinho gira, e gira mais quanto mais perto do centro. Alfa um: dois menos dois dá zero. As partículas dão a volta, e o quadradinho não gira: o vórtice do segundo episódio.

[excited] E alfa dois? Dois menos quatro dá menos dois: o rotacional fica negativo. As setas continuam dando a volta no sentido anti-horário, e o quadradinho gira no sentido horário! Olha por quê: a seta do lado de dentro é bem mais forte que a do lado de fora, então a borda de dentro do quadradinho corre na frente, e ele vira para trás. O sentido da volta não é o sentido do giro.

[thoughtful] E na origem? Todos esses campos dividem por zero lá, então a pergunta é se existe limite. Lê-se: limite de F quando X tende à origem. Com alfa zero, não tem divisão nenhuma: é o disco rígido, já definido e contínuo na origem. Com alfa entre zero e meio, a fórmula não vale no centro, mas a rapidez vai a zero quando você chega nele. Então o limite é o vetor nulo e, definindo a seta da origem como zero, o campo fica contínuo. Com alfa meio, a rapidez fica um, mas a direção depende do caminho por onde você chega: não tem limite. E, com alfa maior que meio, a seta explode.

[curious] Último item: gira cada seta noventa graus, no sentido horário. O redemoinho vira uma explosão, com as setas apontando para fora. A componente horizontal nova é a vertical antiga, e a vertical nova é menos a horizontal antiga. Então o divergente novo é exatamente a conta do rotacional antigo, e os papéis se trocam: o rotacional vira zero, e o divergente vira os mesmos dois menos dois alfa sobre a distância ao quadrado elevada a alfa. Com alfa um, é a falsa fonte do segundo episódio. [thoughtful, emphatic] Guarda essa fórmula: dois menos dois alfa. Ela ainda vai escolher uma lei da física.

### D3b · Duas regras para qualquer campo

[thoughtful] Antes de subir, duas regras que valem para qualquer campo. Primeira: pega um campo que é o gradiente de uma função, ou seja, as componentes são as derivadas parciais dessa função. Na tela, nabla fi: lê-se gradiente de fi. E, daqui em diante, P com xis pequeno embaixo é a derivada parcial de P em relação a xis. Calcula o rotacional. A primeira componente é a derivada em relação à vertical da derivada em relação à profundidade, menos a derivada em relação à profundidade da derivada em relação à vertical. E as outras duas componentes têm a mesma cara: uma derivada mista, menos a mesma derivada mista com a ordem trocada. E, se a função é de classe cê dois, as derivadas mistas são iguais: é o teorema de Schwarz. Tudo cancela. No plano, só sobra a terceira componente, e ela também zera. Um gradiente nunca gira.

[curious] Lembra do campo que esticava o quadradinho no episódio passado? Ele é o gradiente da metade da diferença entre os quadrados das coordenadas. Por isso o quadradinho deformava, mas não girava.

[thoughtful] Segunda regra, agora no espaço, com três componentes. Calcula o rotacional de um campo e, depois, o divergente desse rotacional: a primeira componente é derivada na horizontal, a segunda na vertical e a terceira na profundidade. Aparecem seis derivadas mistas, e elas se cancelam aos pares, de novo por Schwarz. Um rotacional nunca diverge.

[curious] E isso vira teste. Alguém te dá este campo e pergunta: existe outro campo cujo rotacional é ele? Não precisa procurar. Calcula o divergente: a primeira parcela dá seno, a segunda dá menos seno, e a terceira dá um. Total: um. Se ele fosse um rotacional, o divergente teria que ser zero. Então não existe.

[thoughtful] E isso aparece na física. O campo magnético tem divergente zero em todo lugar: é a lei que diz que não existe polo magnético isolado. E, no espaço todo, isso permite escrever o campo magnético como o rotacional de outro campo, o potencial vetor. A seta dupla nos dois sentidos lê-se se e somente se. As duas ideias andam juntas, e a regra de hoje prova uma das metades: todo rotacional tem divergente zero.

[thoughtful, emphatic] E repara na hipótese: classe cê dois. Sem derivadas contínuas, a ferramenta pode falhar. No próximo degrau, a gente vê de perto o que acontece quando falta regularidade.

### D4 · O campo que não melhora de perto

[thoughtful] Quarto degrau, o mais difícil da escada. Este campo pega o vetor posição e multiplica pelo produto das coordenadas, dividido pela distância ao quadrado. Na origem, onde a fórmula divide por zero, a gente define a seta como zero.

[curious] Olha o desenho. Nas diagonais de subida, as setas apontam para fora. Nas outras diagonais, apontam para dentro. E, em cima dos eixos, não tem seta, porque o produto das coordenadas é zero. Pausa o vídeo e tenta os cinco itens.

[thoughtful] Item a: existe limite na origem? Calcula o tamanho da seta. As barras duplas da tela são esse tamanho, a norma; a barra simples é o módulo, o valor sem sinal. O vetor posição tem tamanho igual à distância, então a seta tem tamanho igual ao módulo do produto das coordenadas, dividido pela distância. Em polares, o produto das coordenadas é a distância ao quadrado vezes o cosseno e o seno do ângulo, e cosseno vezes seno é metade do seno do dobro do ângulo. Então o tamanho da seta é a distância vezes metade do módulo desse seno, e isso nunca passa da metade da distância.

[curious] Agora o desafio do épsilon. Épsilon é a tolerância na seta; delta, o raio onde você anda. Alguém escolhe um épsilon. Você responde com delta igual a dois épsilon. Se o ponto está a menos de delta da origem, a seta tem tamanho de no máximo a metade disso, ou seja, menos que épsilon. Venceu, para qualquer épsilon. O limite é o vetor nulo.

[thoughtful] Item b: é contínuo? O ponto está no domínio, porque a gente definiu a seta lá. O limite existe. E é igual à seta do ponto, zero. Os três pedaços passam: contínuo. Item c: as derivadas parciais na origem. Andando pelo eixo horizontal, a seta é zero o caminho todo: derivada zero. Na tela, ela é o limite, quando h tende a zero, da diferença das setas dividida pelo passo h. Pelo vertical, a mesma coisa. A tabela é toda zero: rotacional zero, divergente zero, deformação zero. A previsão seria: perto da origem, nada acontece.

[curious] Item d: confere com um zoom. No episódio passado, o zoom de dez vezes no campo da aula deixava as setas arrumadinhas, iguais ao modelo linear. Aqui, olha: o zoom de dez vezes dá exatamente o mesmo desenho. E o de cem vezes, também. Esse campo é homogêneo: multiplicar a posição por um número multiplica a seta pelo mesmo número. Na conta, o número aparece ao quadrado em cima e embaixo, cancela, e sobra uma vez. Então ele nunca fica parecido com a tabela, por mais perto que você chegue. Na diagonal, a seta tem sempre metade do tamanho do passo: o erro da tabela, dividido pelo passo, fica em meio e não vai a zero. Para o campo ser diferenciável na origem, essa razão teria que ir a zero. Não vai. Em qualquer vizinhança, por menor que seja, tem quadradinho crescendo nas diagonais de subida, encolhendo nas outras, e girando para os dois lados.

[thoughtful, emphatic] A tabela errou. E por quê? Item e: calcula a derivada da componente horizontal na direção horizontal, fora da origem. A componente horizontal é o quadrado da coordenada horizontal vezes a vertical, sobre a distância ao quadrado. Regra do quociente: no numerador, a derivada de cima vezes a de baixo, menos a de cima vezes a derivada de baixo. A derivada de cima é duas vezes o produto das coordenadas; a de baixo, duas vezes a horizontal. Os termos com a quarta potência se cancelam, e sobra duas vezes a coordenada horizontal vezes o cubo da vertical, sobre a distância à quarta. Agora olha essa derivada perto da origem. Nos eixos, ela vale zero. Na diagonal, as duas coordenadas são iguais: duas vezes a quarta potência, sobre quatro vezes a quarta potência, meio. E vale meio e vale meio na diagonal inteira, por mais perto que você chegue. Ela não é contínua na origem. O campo não é de classe cê um, e a tabela perde a garantia. Repara: o cê um é uma garantia, não uma exigência. Tem campo que não é cê um e mesmo assim é bem aproximado pela tabela. Só que aqui a gente provou, direto, que a aproximação falha.

[curious] E olha a escada: no episódio passado, o campo encrenqueiro nem era contínuo. Este é contínuo, tem as duas derivadas parciais e, mesmo assim, engana. Ter derivadas parciais não basta para a tabela descrever o campo de perto.

### D5 · O desafio prometido

[excited] Topo da escada! Chegou a hora do desafio do episódio passado. Três campos. Para cada um: monta a tabela, lê os quatro números e prevê se o quadradinho gira, muda de área ou deforma. Só depois a gente solta o fluido. A tabela se chama jacobiana, a letra J: derivadas de P em cima, de Q embaixo. Lembra das quatro medidas. Rotacional: o de baixo à esquerda menos o de cima à direita. Divergente: a diagonal somada. Primeira deformação, dê um: a diagonal subtraída. Segunda, dê dois: os dois de fora da diagonal, somados.

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

[thoughtful] Segunda: as linhas de corrente são retas, então dá vontade de dizer que não gira. Mas faz a conta. O rotacional é a derivada da componente na direção do canal, tomada na direção de uma margem para a outra: dá menos dois nonos da coordenada horizontal. Na margem esquerda, menos dois nonos vezes menos três: dois terços por segundo. um galho ali gira no sentido anti-horário. E lembra que o rotacional é o dobro da velocidade angular da rodinha: o galho gira com ômega, a velocidade angular, igual a um terço de radiano por segundo. E o período, o T da tela, o tempo de uma volta, é dois pi dividido por um terço, seis pi: uns dezenove segundos. Na margem direita, menos dois terços: gira no horário. E, bem no meio, zero: o galho desce o rio sem girar.

[curious] Olha os três quadradinhos. O do meio só viaja. Os das margens viajam, entortam e giram, cada um para um lado. Por quê? Perto da margem, a água do lado de dentro corre mais rápido que a do lado de fora, então a borda de dentro do quadradinho vai na frente.

[thoughtful] Terceira: o atrito. No episódio passado a gente viu que, num fluido como a água, o atrito viscoso vem da deformação: aqui, da diferença de velocidade entre camadas vizinhas. Aqui, a primeira deformação é zero, e a segunda é aquele mesmo menos dois nonos da coordenada horizontal. Máxima nas margens e zero no meio. É perto das margens que a água mais esfrega em si mesma.

### A2 · Água batendo na parede

[thoughtful] Segundo problema: um jato de água descendo e batendo numa parede, como a água da torneira batendo na pia. Num modelo ideal, perto do ponto do choque, a velocidade tem a coordenada horizontal na primeira componente e menos a vertical na segunda. É o campo do gancho do episódio passado, agora só na metade de cima, com a parede embaixo.

[curious] Primeiro: na parede, a componente vertical é zero. A água não atravessa a parede: ela desliza. Numa parede de verdade, uma camada fina de água gruda nela por causa da viscosidade, e esse modelo ideal ignora essa camada. Segundo: a tabela tem um e zero em cima, zero e menos um embaixo. Rotacional zero, divergente um menos um, zero, e primeira deformação um menos menos um, dois. A água não gira e não comprime: só deforma. Uma gota de tinta que desce pelo eixo se achata e se espalha pela parede, sempre com a mesma área. E as linhas de corrente são hipérboles, as curvas onde o produto das coordenadas é constante. Confere. Lê-se dê xis ípsilon, dê tê: a taxa de variação do produto no tempo. Andando com a água, o produto muda pela velocidade horizontal vezes a coordenada vertical, mais a horizontal vezes a velocidade vertical. Dá o produto menos o produto: zero. O produto não muda: a água anda em cima da hipérbole.

[thoughtful] Terceiro: esse campo é o gradiente da metade da diferença dos quadrados das coordenadas. Essa função tem nome: potencial de velocidade. E o laplaciano dela, escrito nabla dois fi, a soma das duas derivadas segundas, aquela curiosidade do segundo episódio, dá um menos um: zero.

[thoughtful, emphatic] E isso não é coincidência. Se a velocidade é um gradiente, ela é irrotacional, pela primeira das duas regras. Se, além disso, o divergente é zero, então o divergente do gradiente é zero. E o divergente do gradiente é o laplaciano. Escoamento irrotacional e incompressível quer dizer laplaciano do potencial igual a zero: a equação de Laplace. A mesma equação aparece no potencial elétrico numa região sem cargas e na temperatura de uma chapa em equilíbrio.

### A4 · Mapas que não entortam

[curious] Lembra do terceiro campo do desafio, aquele que nunca entorta? Vamos ver por quê. Deformação zero em todo lugar quer dizer duas equações. Iguala cada deformação a zero e passa um termo para o outro lado: a derivada horizontal da primeira componente igual à derivada vertical da segunda, e a derivada vertical da primeira igual a menos a derivada horizontal da segunda. Essas duas equações têm nome: equações de Cauchy-Riemann.

[thoughtful] Elas aparecem quando você junta as duas componentes num número complexo. O nosso campo é exatamente o quadrado do número complexo que tem a coordenada horizontal como parte real e a vertical como parte imaginária. Abre o quadrado; o i da tela é a unidade imaginária: o quadrado da horizontal, mais duas vezes a unidade imaginária vezes o produto, mais o quadrado da unidade imaginária vezes o quadrado da vertical. E o quadrado da unidade imaginária é menos um. Sobra a diferença dos quadrados na parte real e duas vezes o produto na imaginária. E toda função complexa derivável satisfaz essas equações: o cubo, a exponencial, todas.

[curious] Agora lê como transformação. Onde a derivada complexa não é zero, uma tabela assim só gira e muda a escala: quadradinhos pequenos viram quadradinhos, maiores ou menores, mas sempre com ângulos retos. Isso se chama mapa conforme. E você conhece um: o mapa-múndi de Mercator, aquele de parede de sala de aula, preserva os ângulos. Por isso a Groenlândia aparece quase do tamanho da África, mas com o formato certo em cada pedacinho.

[thoughtful] E o irmão desse campo, com o sinal da segunda componente trocado, faz o contrário: rotacional zero, divergente zero, só deformação.

### A3 · Por que um sobre a distância

[excited] E agora, o último problema, que fecha a escada inteira. Um fio comprido, com corrente, atravessando a tela. As linhas do campo magnético são circunferências em volta dele. A pergunta é: com que lei o campo enfraquece quando você se afasta? Pausa e pensa.

[thoughtful] A física diz duas coisas. Primeira, a simetria: o campo dá a volta no fio, e o tamanho só depende da distância. Supondo uma lei de potência, ele tem a forma do terceiro degrau: menos a coordenada vertical e a horizontal, divididas pela distância ao quadrado elevada a um expoente alfa que a gente não sabe. Segunda: fora do fio não tem corrente e, para campos que não mudam no tempo, a lei de Ampère diz que, onde não tem corrente, o rotacional do campo magnético é zero.

[curious] Agora usa a fórmula que a gente guardou. O rotacional é dois menos dois alfa, sobre a distância ao quadrado elevada a alfa. Para ser zero, só tem um jeito: o numerador zera, dois igual a dois alfa, e alfa igual a um. Então o tamanho do campo é a distância dividida pela distância ao quadrado: um sobre a distância. O campo do fio cai com um sobre a distância. A intensidade ainda depende da corrente; o que a conta escolhe é como ela cai.

[thoughtful] Faz o mesmo com um fio carregado. O campo elétrico aponta para fora, então ele é a explosão do terceiro degrau. Fora do fio não tem carga, e a lei de Gauss diz que o divergente é zero. Divergente: dois menos dois alfa, de novo. Alfa um, e o campo também cai com um sobre a distância.

[excited] E uma carga pontual, no espaço? Escreve o campo como o vetor posição dividido pela distância elevada a um expoente. O X maiúsculo é o vetor posição; as barras duplas, a distância; p, o expoente. No plano, o divergente seria dois menos esse expoente. Faz a conta de uma parcela: a derivada da coordenada horizontal sobre a distância elevada ao expoente, na direção horizontal. A derivada da distância, nessa direção, é a coordenada horizontal sobre a distância. Então dá um sobre a distância elevada ao expoente, menos o expoente vezes o quadrado da coordenada horizontal, sobre a distância elevada ao expoente mais dois. As outras parcelas são iguais, cada uma com a sua coordenada. Agora soma: os três primeiros termos dão três; e os quadrados das coordenadas somam a distância ao quadrado, que cancela o mais dois do expoente. Sobra o número de parcelas menos o expoente. No plano são duas parcelas; no espaço, três. Então o divergente no espaço é três menos o expoente, dividido pela distância elevada ao expoente. Para zerar, o expoente é três, e o tamanho do campo fica um sobre a distância ao quadrado. A lei do inverso do quadrado, a de Coulomb e a da gravitação.

[thoughtful, emphatic] No plano, o número que aparece é dois; no espaço, é três. O expoente da lei vem da dimensão do espaço: em três dimensões, o campo tem mais lugar para se espalhar. E fica o cuidado: não é o rotacional ou o divergente sozinhos que decidem a lei. É a lei física, o rotacional zero ou o divergente zero fora da fonte, junto com a simetria: as linhas em círculo em volta do fio e o campo radial em volta da carga. Com as duas juntas, não sobra escolha.

### S · Síntese, gancho e CTA

[thoughtful] Olha a escada inteira. A mesma fórmula conta dois filmes. Um campo se desenha pelas curvas onde ele não muda. O sentido da volta não é o sentido do giro. Um gradiente nunca gira, e um rotacional nunca diverge. Ter derivadas parciais não basta. E, com a tabela, você prevê o quadradinho antes de soltar. [curious] E, nas aplicações, um rio que gira nas margens, uma parede onde a água só deforma, mapas que nunca entortam e o um sobre a distância escolhido pela conta.

[excited] No próximo vídeo, a gente troca de pergunta. Até aqui, tudo foi medido num ponto, bem de perto. Agora é hora de somar pedacinhos. Uma chapa quadrada, de dois metros de lado, leve num canto e cada vez mais densa até o canto oposto. Pelo valor do centro, a massa dá oito quilos. Pela média dos quatro cantos, dezesseis. O dobro! Qual das duas está certa? A resposta exata vem de somar infinitos pedacinhos: a integral dupla.

[happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual degrau da escada foi o mais difícil para você? Até a próxima!

*(Na tela do gancho: alvo `v3_gan`, montado frase a frase como no §2 S. Sem número de episódio nem Atlas. Depois, o CTA padrão.)*

---

## Anexo B · Leitura dos símbolos (sublinhado no gatilho)

| # | Bloco | Símbolo na tela | Como a voz lê (trecho da v3.2) | Sublinhado sob |
|---|---|---|---|---|
| 1 | D1 | φ(u, v) = (u + v, u − v) | "fi de u, v igual a u mais v, u menos v. Fi é só o nome da função" | φ(u, v) |
| 2 | D1 | F⃗ | "a setinha em cima do F diz que o resultado é um vetor" | a seta do F |
| 3 | D2 | ⇒ | "a seta dupla da tela lê-se implica" | ⇒ |
| 4 | D3 | x² + y² | "xis ao quadrado mais ípsilon ao quadrado é a distância ao quadrado" | x² + y² |
| 5 | D3 | ∂Q/∂x, P, Q | "P e Q são as duas componentes, e o d arredondado é a derivada parcial" | P, Q e depois ∂ (na fórmula-mãe do rot) |
| 6 | D3 | lim_{X→0} F⃗(X) | "limite de F quando X tende à origem" | lim e X → 0 |
| 7 | D3b | ∇φ | "nabla fi: lê-se gradiente de fi" | ∇φ |
| 8 | D3b | φ_x (índice) | "P com xis pequeno embaixo é a derivada parcial de P em relação a xis" | o índice x de φ_x |
| 9 | D3b | ⇔ | "a seta dupla nos dois sentidos lê-se se e somente se" | ⇔ |
| 10 | D4 | ‖F⃗‖ | "as barras duplas da tela são esse tamanho, a norma" | ‖F⃗‖ |
| 11 | D4 | \|xy\| | "a barra simples é o módulo, o valor sem sinal" | \|xy\| |
| 12 | D4 | ε | "épsilon é a tolerância na seta" | ε |
| 13 | D4 | δ | "delta, o raio onde você anda" | δ |
| 14 | D4 | lim_{h→0} | "o limite, quando h tende a zero, da diferença das setas dividida pelo passo h" | lim_{h→0} |
| 15 | D5 | J | "a tabela se chama jacobiana, a letra J" | J |
| 16 | D5 | d₁, d₂ | "primeira deformação, dê um… segunda, dê dois" | d₁, depois d₂ |
| 17 | A1 | ω | "ômega, a velocidade angular" | ω |
| 18 | A1 | T | "o período, o T da tela, o tempo de uma volta" | T |
| 19 | A2 | d(xy)/dt | "dê xis ípsilon, dê tê: a taxa de variação do produto no tempo" | d(xy)/dt |
| 20 | A2 | ∇²φ | "escrito nabla dois fi, a soma das duas derivadas segundas" | ∇²φ |
| 21 | A4 | i | "o i da tela é a unidade imaginária" | i |
| 22 | A3 | X, ‖X‖, p | "o X maiúsculo é o vetor posição; as barras duplas, a distância; p, o expoente" | X, ‖X‖ e p, um de cada vez |

Regra para os próximos blocos ou vídeos: a primeira vez que um símbolo novo aparece, a voz lê; depois disso, a fala volta aos nomes ("a horizontal", "a derivada"). O sublinhado só existe durante a leitura.
