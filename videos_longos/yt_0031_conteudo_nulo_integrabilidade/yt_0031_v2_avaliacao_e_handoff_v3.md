# yt_0031 · CÁLCULO III · EP. 06 · Conteúdo nulo e integrabilidade
# AVALIAÇÃO DO PREVIEW v2 + HANDOFF v3 · preview PARCIAL (só os blocos afetados)

2026-11-13. Produção → Claude Code. Documento **autocontido**. Vale junto com o handoff v2, que continua na unidade (G1–G8 continuam valendo), e com a pasta `yt_0031_quadros_alvo_v3/` do zip:
- os 31 alvos do v2;
- **3 alvos novos**: `21b_B6_contradicao.jpg`, `23b_B7_substituicoes.jpg` e `28a_B9_perguntas.jpg`;
- o `sb31.html` com as chaves novas `b63c`, `b72s` e `b91a`.

Onde este documento e o v2 divergirem, **vale este**.

Fase aberta: **preview v3 parcial, silencioso**. Sem voz, sem SRT, sem 1080p, sem master, sem entrega, sem commit e sem push. Se este v3 passar, o próximo passo é a voz.

---

## 0. O que entregar

1. Re-renderizar **só** as seções afetadas (§2) em 540p15 e remontar o vídeo inteiro: `renders/v3/yt_0031_preview_v3_540p15.mp4`. As seções que não mudaram são reaproveitadas do v2, sem re-render.
2. Cortes curtos de cada bloco refeito: `renders/v3/blocos/<bloco>.mp4`, para o Kaio ver rápido.
3. `renders/v3/qa/`, com QA **só dos blocos refeitos** (§4), mais duas checagens no vídeo inteiro: FLASH e a costura dos tempos.
4. A prancha `comparacao_v3.jpg`, com os alvos dos blocos refeitos (incluindo os 3 novos).
5. O relatório de entrega do AGENTS.md. Inclua a explicação da divergência do §3.3.

---

## 1. Avaliação do v2

O v2 resolveu quase tudo do v1:
- origens: 0 linhas sem origem;
- 13 glyph maps, com os 5 obrigatórios;
- nenhum `FadeIn` de fórmula e FLASH = 0;
- palco vazio: 0;
- linha 2 do canto presente desde o primeiro quadro;
- alinhamento 3D em 0,00 px;
- contagens de caixas seguindo a voz;
- cores certas em todos os blocos.

A álgebra do B1-2, do B1-3 (mapa 1, voo da cota no sentido certo), do B3-1, do B4-1, do B4-2, do B6-2 e do B7-3 está **aprovada**.

Sobram três problemas graves e uma lista curta de médios. Todos ficam em blocos isolados.

### As três escolhas que você deixou em aberto
- **(a) S1, ordem 1, 3, 2.** Cada caixa entrar na sua palavra está certo. O defeito é a caixa de baixo nascer antes da do meio e deixar um buraco. **Solução: trocar as posições** (§2, S1). A coluna passa a se encher de cima para baixo, na ordem da fala.
- **(b) A linha `altura de cada tampa = 3 − 1 = 2` só no começo do B2-2.** Aprovado: o 2 precisa voar do muro. O defeito real é ela sair cedo demais (§2, B2-2).
- **(c) Zooms do B6-3 em "um onde o seno" / "outro onde vale".** Não. A sequência de zoom **é** o "tão próximos quanto você quiser". Siga a tabela do v2 e use "um onde… / outro onde…" para acender o +1 e o −1 (§2, B6-3).

---

## 2. Correções, bloco a bloco

Os tempos são do preview v2. Os arquivo:linha são da unidade como está agora. Cada item tem um **aceite** que precisa aparecer no QA.

### ALTA 1 · B2-2 · 4:52.7–4:53.4 · a fórmula-chave fica só ~0,3 s na tela (`sec_b2.py:118-125`)
- A coluna fica completa em 4:52.73 e começa a sair em 4:53.0, enquanto a voz ainda diz "…que a solda atravessa. Refina a grade".
- **Correção:**
  1. A coluna inteira fica até "com quatro divisões" (≈ 4:55.5).
  2. Nessa palavra, `S(P) − s(P) = 2 · (área das células na solda)` **sobe** (`Transform` de posição, 0,6 s, sem reescrever) para **acima da tabela**, em y ≈ 220 px no 1080p, a 34 px. Ela fica até o fim do B2-2.
  3. As outras linhas da coluna saem nesse momento.
  4. Tire `FORA DA SOLDA: TAMPA ZERO` da coluna (a `TAMPA 0` já está na célula).
- **Aceite:** a linha `S(P) − s(P) = 2 · (…)` aparece em ≥ 95 % dos quadros entre 4:52.7 e o fim do B2-2. Ela não toca a tabela (R5).

### ALTA 2 · B7-2 · 14:30.8–14:35.7 · substituições sem as escolhas de ε (`sec_b7.py:170-200`) · alvo **23b (novo)**
Hoje as escolhas ε₂ = ε/(2α) e ε₁ = ε/(8M) nunca aparecem escritas. `α·ε/(2α)` nasce longe do termo, cada passo dura ~0,6 s e a soma final embola sobre "S(P)".

**Narração:** entra **uma frase nova** no B7-2, logo depois de "…menor que metade da tolerância." (texto exato no Anexo A). O B7-2 cresce ≈ 15 s e tudo dali em diante desloca igual. Refaça o tempo das seções seguintes pela narração estimada, sem mudar mais nada nelas.

**Coluna, de cima para baixo** (posições do alvo 23b, no 1080p):

| y | Linha | Origem |
|---|---|---|
| 250 | `S(P) − s(P) < αε₂ + 4Mε₁` (42 px) | já existe (mapa 2 do v2). As linhas `CALMAS`/`VERMELHAS` saem antes, com a cota de cada uma já dentro dela. |
| 345 | `ESCOLHA DOS DOIS ε` (legenda menta, 26 px) | caneta, em "escolhe os dois épsilons" |
| 420 | `ε₂ = ε/(2α)` e, ao lado, `ε₁ = ε/(8M)` (38 px, `\dfrac`, ε₁ e ε₂ em menta) | `ε₂` e `ε₁` **voam** da linha de 250; o resto vai a caneta, cada um na sua palavra da frase nova |
| 550 | `αε₂ = α · ε/(2α) = ε/2` | `αε₂` voa da linha de 250; `ε/(2α)` voa da linha de 420; o par `α … α` fica coral, ganha `\cancel` coral e some no mapa seguinte, que deixa `ε/2` |
| 690 | `4Mε₁ = 4M · ε/(8M) = ε/2` | mesmo esquema: `M` com `M` riscados juntos; `4` e `8` riscados juntos, com um `2` pequeno (`\underset{2}{\cancel{8}}`) — **não** transforme o 8 em 2 |
| 840 | `S(P) − s(P) < ε/2 + ε/2 = ε` (42 px) | os dois `ε/2` voam das linhas 550 e 690; `S(P) − s(P) <` voa da linha de 250 |
| 960 | `AS TAMPAS SOMEM` (ciano, 40 px) | caneta, em "As tampas somem!" |

- Cada `ε/2` fica **≥ 1,2 s** parado antes da soma.
- Os glifos que saem usam `auto_fade` **antes** do mapa, para não embolarem (o caso de 14:35.0).
- Se faltar altura, `ESCOLHA DOS DOIS ε` pode sair quando a linha de 550 entrar. Nada mais muda de lugar.
- **Aceite:**
  - `glyphmaps_v3.txt` mostra os mapas 3 e 4 com os cancelamentos;
  - `origens_v3.txt` mostra a fonte das 6 linhas;
  - nenhum quadro com glifos sobrepostos entre 14:28 e o fim do B7-2;
  - render × alvo 23b ≤ 10 px.

### ALTA 3 · B6-3 · 12:37.7–12:55.3 · a contradição não tem figura (`sec_b6.py:252-262`) · alvo **21b (novo)**
O trecho de "Numa região fechada e limitada…" até "Contradição" dura ~17 s com a figura do sen(1/x) parada. Há um parado de 4,2 s em 12:45.3.

- **Troca de cena** em "Numa região fechada e limitada, isso não acontece":
  - a lupa e a coluna do sen(1/x) saem;
  - a chapa vira o mapa contínuo x² + y² (o mesmo `mapaDens` do B1);
  - a borda esquerda, que estava tracejada, fica **contínua e branca** (`Create`, 0,5 s);
  - entra `FECHADA E LIMITADA` sobre a chapa.
- Em "Se a continuidade uniforme falhasse": `SE NENHUM δ SERVISSE:` na coluna.
- Em "haveria pares de pontos cada vez mais próximos":
  - os **3 pares** laranja entram um após o outro, com a régua de 60 → 30 → 12 px, andando sobre o tracejado em direção a P*;
  - `PARES CADA VEZ MAIS PRÓXIMOS` na coluna.
- Em "com valores sempre longe um do outro": `VALORES SEMPRE LONGE`.
- Em "esses pares se aproximam de um mesmo ponto da própria região":
  - o anel branco em P* e o rótulo `P*` (com placa);
  - `NA CHAPA FECHADA E LIMITADA,` / `OS PARES SE ACUMULAM EM P*`.
- Em "E ali a função seria descontínua":
  - `DESCONTÍNUA EM P*?` (coral, 28 px, com placa) sobre o anel;
  - `MAS f É CONTÍNUA EM P*` (ciano) na coluna.
- Em "Contradição": `CONTRADIÇÃO` (ALERTA, 48 px).
- Posições: as do alvo 21b.
- **Aceite:** nenhum parado > 3 s entre 12:37 e o fim do B6-3; render × alvo 21b ≤ 10 px.

### B6-3, zooms (`sec_b6.py:246-247`)
- As trocas de zoom voltam para a tabela do v2:
  - zoom 1 em "Dá para achar dois pontos";
  - zoom 2 em "tão próximos";
  - zoom 3 em "quanto você quiser".
- Elas ficam a ~0,3 s uma da outra na fala, e por isso cada troca dura **0,3 s** (corte suave, sem `Wait`). A distância na coluna troca junto.
- Depois dos três zooms: a placa `+1` acende em "um onde o seno vale um" e a `−1` em "outro onde vale menos um".
- **Confira o mapeamento da janela no zoom 3:** o ponto −1 tem que cair no meio da faixa escura (no zoom 1 ele cai). Use x = 1/(3π/2 + 6π) = 0,0424 e x = 1/(π/2 + 6π) = 0,0490 na janela [0,035; 0,06].
- Os glifos embolados em 12:34.3 saem com `auto_fade` antes do mapa.

### MÉDIA-ALTA · B9-1 · 17:25.5–17:33.4 · palco quase vazio (`sec_b9.py:21-40`) · alvo **28a (novo)**
- Por ~8 s, a tela tinha só os chips de 28 px no topo. Agora:
  - `O TESTE DO TEOREMA` (legenda) aparece em "o teorema vira três perguntas";
  - cada pergunta entra **grande, no centro**, na sua palavra ("é limitada?", "conteúdo nulo?", "a fronteira…"): o texto numa moldura, a 44 px, em y = 430 / 540 / 650 (posições do alvo 28a).
- Em "Os exemplos do livro passam nas três":
  - as três molduras **sobem e encolhem** até virar os chips do topo (`ReplacementTransform`, 0,8 s; o texto é o mesmo, só a escala muda);
  - na mesma hora, o cartão 1 entra.
- Daí em diante, siga o alvo 28 do v2.

### MÉDIA · B2-1 · 4:30.9–4:43.5 · `TAMPA 0` cortado (`sec_b2.py:61`)
- A borda branca de cima da célula passa por dentro das letras de `TAMPA 0`.
- A placa `ρ = 1` vai para a célula vizinha. `TAMPA 0` (24 px, com placa) fica centrado na sua célula, a ≥ 10 px de todas as bordas.
- Em "No metal pesado, o mesmo" (o parado de 3,0 s em 4:31.07): uma célula do metal pesado ganha contorno laranja e `TAMPA 0` próprio.

### MÉDIA · B1-2 · 2:27.5–2:54.8 · `TAMPAS` antes da hora (`sec_b1.py:92`; o mesmo em `sec_b6.py:53`)
- O conceito só chega em "são as tampas coral" (3:11.9). Tire o rótulo `TAMPAS` do B1-2.
- No B6-1, em 11:11, o mesmo rótulo encosta na aresta: afaste-o ≥ 16 px.

### MÉDIA · B1-3 · 3:20.8 · linha órfã `= VOLUME DAS TAMPAS` (`sec_b1.py:223`)
- A linha vira `S(P) − s(P) = VOLUME DAS TAMPAS`, com o lado esquerdo **voando** da linha de cima.
- Antecipe o voo da cota para "sobra o teto menos o piso". Os parênteses vazios ficavam ~3 s na tela (2:57.4–3:01.5).
- Em "Guarda essa imagem" (parado de 3:13.4): a cota coral acende.

### MÉDIA · símbolos pequenos (troca de LaTeX, sem mudar o tempo)
| Onde | Hoje | Fica |
|---|---|---|
| B3-3, 7:28.9–7:39.5 (`sec_b3.py:238`) | ε de ~12 px, cinza, sem placa | **ε em menta, 44 px, com placa**, ao lado da barra |
| B3-2, 6:39–6:58 (`sec_b3.py:37` e `:121`) | `\tfrac14` | `\dfrac{1}{4}` |
| H1, 0:36–0:49 (`sec_h.py:98`) | `\tfrac{32}{3}` | `\dfrac{32}{3}` |
| S2, 19:14–19:41 (`sec_s.py:84`) | `\textstyle\iint_{\text{leve}}…`, índices de ~14 px | sem `\textstyle`, 44 px |
| B4-3, 9:15–9:31 (`sec_b4.py:250`) | `C¹` em Space Grotesk (o ¹ some) | `C^1` em LaTeX, seguido da legenda `: DERIVADA CONTÍNUA` |
| B7-3, 14:41–15:28 (`sec_b7.py:219-227`) | T1 menor que T2; miniaturas de 120/90/160/120 px; `D = ∅` a 26 px | T1 quebrado depois de "e" (como no alvo 24), as duas linhas a 38 px; **miniaturas com 130 px** nas quatro caixas; `D = ∅` a 34 px |

### MÉDIA · B5-2/B6-1 · 10:43–11:26 · miniatura do muro cortada (`sec_b5.py:7`, `:124`, `:126`)
- A quina da frente e o eixo x param na borda de baixo do cartão, por causa do recorte fixo da imagem.
- Reduza a imagem para 88 % **ou** suba 40 px, com ≥ 16 px de margem nos quatro lados.
- A legenda da miniatura vai de 22 para 24 px.

### MÉDIA · B5-1 · 9:44–10:13 · texto demais e fora da ordem (`sec_b5.py:32`, `:65`)
- A coluna chega a 6 linhas. `TODA BOLA PEGA B / E PEGA FORA DE B` (escrita em 10:00) fica **acima** de `BOLA ABERTA…` (escrita em 9:44).
- Correção:
  - `BOLA ABERTA…` sai quando a sonda interior entrar;
  - as linhas ficam na ordem da fala, de cima para baixo;
  - `FRONTEIRA DE B` e `O ARCO + OS 2 SEGMENTOS` viram uma linha só: `FRONTEIRA: ARCO + 2 SEGMENTOS`.
- Máximo de 4 linhas na coluna ao mesmo tempo.
- Parados: em "pega um ponto" (9:36.5), o ponto nasce; a sonda interior entra em "Se dá para escolher uma bola inteira dentro" (9:44.4).

### MÉDIA · B7-1 · 13:07–13:43 · 9 itens de texto em duas colunas
- Uma coluna só, em x = 1120, com os passos `1 · COBRE D: ÁREA < ε₁` → `2 · ENGORDA: ÁREA < 2ε₁` → `3 · GRADE: MARGEM E δ`.
  - `3 · GRADE MENOR QUE OS DOIS δ` estava errado: a margem nunca foi chamada de δ.
- Tire `f LIMITADA`, que repete `|f| ≤ M`.
- Parado de 4,7 s em 13:07.3: a solda e o `D` acendem em "O objetivo é provar".
- Máximo de 5 linhas na coluna.

### MÉDIA · B4-3 · 9:23–9:31 · ordem das formas (`sec_b4.py:264`)
- A voz diz "segmentos, polígonos, círculos, elipses". As formas ficam nessa ordem, da esquerda para a direita: **SEGMENTO, POLÍGONO, CÍRCULO, ELIPSE**, em x = 1070 / 1290 / 1510 / 1730, cada uma entrando na sua palavra.
- Parados:
  - em 9:03.0, o topo das caixas acende coral em "soma por cima" e a base azul-clara em "soma por baixo";
  - em 9:24.7, as quatro formas acendem juntas em "quase toda borda".

### MÉDIA · S1 · 18:35–18:54 · ordem das caixas (`sec_s.py:35`)
- As posições trocam: `TAMPAS` em y = 260, `CONTINUIDADE UNIFORME` em y = 410 e `CONTEÚDO NULO` em y = 560.
- Cada uma entra na sua frase. A coluna se enche de cima para baixo.
- O alvo 30 vale com essas posições.

### H2 · 0:52–0:58 · a pergunta do vídeo sem texto
- Em "como saber se uma integral dupla existe sem calcular o valor dela?": `EXISTE SEM CALCULAR?` (40 px, centro, caneta).
- Ele sai quando `O PROBLEMA NÃO É O SALTO` entra.

### Eventos para os parados que pediam evento
Ligue cada evento à palavra indicada, com atraso ≤ 0,2 s:

| Tempo v2 | Bloco | Evento |
|---|---|---|
| 3:45.9 | B1-4 | o segmento entre as paredes acende em "a diferença entre as duas somas" |
| 6:30.9 | B3-2 | a marca ε = 1 acende em "um metro quadrado" |
| 7:47.7 | B4-1 | `CAIXAS: DO PISO AO TETO` entra em "do menor ao maior valor" (hoje entra depois) |
| 8:32.6 | B4-2 | as caixas da solda refinam de 8 para 16 em "vai a zero junto com o maior lado" |
| 10:15.3 | B5-2 | o arco acende em "numa região que não é retangular" |
| 13:59.0 | B7-2 | o contorno da chapa acende em "a área do retângulo"; `α: ÁREA DO RETÂNGULO` entra em "a gente chama de alfa" (hoje 2 s atrasado) |
| 15:48.3 | B7-4 | a solda do painel dos dois metais acende em "só é descontínua na solda" |
| 19:08.4 | S2 | o pedaço leve acende em "a massa do pedaço leve" e o pesado em "e a do pesado" |

### Itens pequenos (entram junto, são baratos)
- **B6-2, 12:03:** o rótulo `X` fica a ~10 px do `f(X)` das barras. Afaste-o ≥ 16 px. Os pares tracejados no canto de baixo ficam: são os pares "calmos" do alvo 20.
- **B8-1, 16:44.9:** `4 CONTRA ZERO…` está a ~12 px de `64 × 64`. Afaste ≥ 16 px.
- **B8-2, 16:56:** o fundo vermelho do quadrado só entra em "a fronteira dele é o quadrado inteiro".
- **A1, 1:33.8:** o contorno do chip 3 nasce junto com o texto, não antes.
- **B3-1, 6:27.9:** `NÚMERO FINITO DE RETÂNGULOS` fica ≥ 16 px abaixo de `∪: UNIÃO…`.
- **B1-4:** `S(P) DESCE` e `s(P) SOBE` ficam com o `S(P)` e o `s(P)` em LaTeX (com as cores) e `DESCE`/`SOBE` em Space Grotesk.
- **B4-1, 8:10.1:** os glifos embolados saem com `auto_fade` antes do mapa.

---

## 3. QA (só dos blocos refeitos, salvo onde indicado)

1. **R5 ampliado de verdade.** O R5 do v2 deu 0, mas não pegou o `TAMPA 0` cortado nem a miniatura cortada. Acrescente dois cruzamentos:
   - texto contra **borda de célula da grade** (só quando o texto está sobre a chapa);
   - texto e 3D contra a **borda do recorte de imagem** (miniaturas e cartões).
   Esperado: zero nos blocos refeitos.
2. **Parados (G3):** nenhum > 3 s nos blocos refeitos, salvo "voz lendo a tela" com o motivo em `parados_v3.txt`.
3. **Divergência a explicar:** a última linha de `qa/cadeia.txt` diz "R5 58 · gatilhos >0,2 2", mas `sobreposicoes_v2.txt` dá 0 e `gatilhos_v2.txt` dá 1. Diga qual vale e por quê. Se 58 for o número certo, liste as 58.
4. **Glyph maps e origens:** `glyphmaps_v3.txt` e `origens_v3.txt` para B1-3, B2-2, B6-3 e B7-2.
5. **Render × alvo:** os alvos dos blocos refeitos, incluindo 21b, 23b e 28a, com tolerância de 10 px → `comparacao_v3.jpg`.
6. **Vídeo inteiro:** FLASH = 0. Duração = v2 + o acréscimo do B7-2. Nenhum salto na costura entre seção reaproveitada e seção refeita (primeiro e último quadro de cada costura lado a lado em `costuras_v3.jpg`).

---

## 4. O que NÃO fazer
- Não mexer nos blocos aprovados além do que está listado.
- Nada de efeito novo. "Acender" = trocar a cor por 1–2 s e voltar.
- Nenhum `FadeIn` de fórmula ou de glifo de fórmula.
- Não mexer em `template/`, `assets/`, `docs/`, `AGENTS.md`, `pyproject.toml`, `uv.lock` nem em outras unidades.
- Sem voz, SRT, master, 1080p de vídeo, entrega, commit ou push.

## 5. Parada
Entregue o preview v3, os cortes por bloco, a prancha, o QA e o relatório de entrega. Pare.

---

## Anexo A · A frase nova do B7-2

A frase entra entre "…menor que metade da tolerância." e "As tampas somem!":

> Com épsilon dois igual a épsilon sobre dois alfa, o alfa cancela, e sobra épsilon sobre dois. Com épsilon um igual a épsilon sobre oito eme, o eme cancela, o quatro com o oito vira um meio, e sobra épsilon sobre dois de novo. Meio épsilon mais meio épsilon: a diferença fica menor que épsilon.

(≈ 50 palavras, ≈ 16 s a 3 palavras/s.)

Gatilhos dela:

| Palavra | Evento |
|---|---|
| "épsilon dois igual a" | linha de 420, metade da esquerda |
| "alfa cancela" | o par α coral + `\cancel` |
| "épsilon um igual a" | linha de 420, metade da direita |
| "o eme cancela" | o par M |
| "o quatro com o oito" | 4 e 8 riscados, entra o 2 pequeno |
| "Meio épsilon mais meio épsilon" | a linha de 840 |

**Se o Kaio preferir a narração sem a frase**, o B7-2 fica com o tempo do v2. As linhas de 420 a 840 entram nas palavras "escolhe os dois épsilons", "cada parcela" e "menor que metade da tolerância", e o fim da cena estica até "As tampas somem!", com cada `ε/2` ≥ 1,2 s na tela.
