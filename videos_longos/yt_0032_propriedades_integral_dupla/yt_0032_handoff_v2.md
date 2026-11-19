# yt_0032 · CÁLCULO III · EP. 07 · Propriedades da integral dupla
# AVALIAÇÃO DO PREVIEW v1 + HANDOFF v2 · preview silencioso (540p, 15 fps)

2026-11-12. Produção → Claude Code. Documento **autocontido**. Ele vale junto com o handoff v1, que já está na unidade, e com a pasta `yt_0032_quadros_alvo_v2/` do zip. Essa pasta traz:
- 16 quadros-alvo novos (`*_v2_*.jpg`) e a folha de contato;
- os geradores `sb32.html` e `c3d32.html`, que têm as chaves v1 **e** as v2;
- a cena 3D nova `b14k`.

Onde este documento e o v1 divergirem, **vale este**.

Fase aberta: **preview visual silencioso v2**. Não fazer voz, SRT, 1080p, master, entrega, commit nem push.

O pedido do Kaio: *"avaliar as possíveis correções de didática, representação visual, MF-Tools, sobreposições"*.

---

## 0. O que entregar

1. A mesma unidade `videos_longos/yt_0032_propriedades_integral_dupla/`, com as mudanças deste documento. O v1 fica em `renders/v1/`; não apague nada dele.
2. `renders/v2/yt_0032_preview_v2_540p15.mp4`: 960×540, 15 fps, sem áudio, no tempo da **narração v3**, que não muda (§6).
   - Re-renderize **só os blocos que mudam** (lista no §4).
   - Os outros entram por cache ou cópia das seções do v1.
3. Em `renders/v2/qa/`, tudo o que o §8 pede. São quatro relatórios novos: `fracoes_v2.txt`, `texto_em_mathtex_v2.txt`, `palco_parado_v2.txt` e `origens_v2.txt`.
4. A prancha render × alvo `comparacao_v2.jpg`, com os 16 alvos v2 e os alvos v1 que continuam valendo nos blocos que você re-renderizou.
5. O relatório de entrega do AGENTS.md.

---

## 1. Avaliação do v1

O v1 está bom de sistema e não precisa mexer nisto:
- fundo violeta e papel;
- os layouts;
- as cores;
- as 7 cenas Three.js com alinhamento de 0,00 px;
- R5 e flash zerados;
- 8 glyph maps;
- os números, todos certos;
- a duração de 17:52.

**A arte que o Kaio pediu no meio da rodada fica como está:**
- o cordão de solda: corpo prateado, escamas em V e ponta laranja que esfria;
- o metal com degradê e escovado;
- a balança com pivô, ponteiro, pratos em cuia, inclinação e amortecimento;
- os mapas de cor ajustados.

Nada deste documento desfaz isso. Onde um alvo v2 mostra a balança, a solda ou o metal mais simples, **vale a arte do v1**. Os alvos são esquemas de posição e conteúdo, não de acabamento.

Os problemas do v1 estão em quatro frentes: (1.1) termos que aparecem sem origem, (1.2) representações que não mostram o que a fala diz, (1.3) tipografia e sobreposições, e (1.4) palco parado. Os glyph maps vêm no §3.

### 1.1 Didática: termo sem origem

Pela regra da série, nada aparece pronto: cada termo tem a fórmula-mãe antes do número, e cada valor voa da fonte.

| # | Bloco | No v1 | v2 |
|---|---|---|---|
| D1 | B1-2 (≈1:50) | `Σ (f + g) ΔA = …` aparece, mas nunca se diz que f é a rampa x² e g a rampa y² | `f = x²` (âmbar) e `g = y²` (lilás) **voam dos rótulos das rampas** antes do Σ. Gatilhos: "xis ao quadrado, uma rampa…" e "ípsilon ao quadrado…". Alvo `05_B1-2_v2` |
| D2 | B1-4 (≈3:00) | `∬ k f = k ∬ f` sem nenhum valor de k na tela, e o caso k < 0, que a fala cita, não aparece | Chips `k = 2`, `k = ½` e `k = −1` nos gatilhos "dois", "meio" e "negativo". Para k = −1, cena 3D nova `b14k`: as caixas **descem abaixo do chão** e aparece `CONTRIBUIÇÃO TROCA DE SINAL`. Depois, `k f(Xᵢⱼ) ΔA` com `CADA PARCELA × k`. Alvo `07a_B1-4_v2` |
| D3 | B3-1 (≈4:50) | `∬ ≤ M · área` sem integrando nem módulo | `\|∬_B f\| ≤ M · área da cobertura`, com o M preso **no topo do muro**. Alvo `10_B3-1_v2` |
| D4 | B3-3 (≈6:40) | `≈ 135 g` aparece pronto | Fórmula-mãe `m ≈ ρ · L · largura`. O 6 voa do rótulo de densidade, o 2,25 da linha medida e o 0,01 da cota do cordão. Glyph map até `0,135 kg` e depois `135 g`. Em seguida, `0,01 → 0,001` e `13 g`. Alvo `12_B3-3_v2` |
| D5 | B4-1 (≈7:30) | `{(x, y) ∈ B \| f ≠ g}` aparece sem que f e g tenham sido definidos | `f: ρ = 1 NA SOLDA` (ciano) e `g: ρ = 100 NA SOLDA` (lilás), mais `IGUAIS FORA DA SOLDA`, **antes** do conjunto. Gatilhos: "A do metal leve, um?" … "Ou aquele exagero de cem?". Alvo `13_B4-1_v2` |
| D6 | B4-2 (≈8:30) | `h` e `D` surgem sem definição | Sem letras novas. A diferença é escrita `f − g`, o furo é o `disco` do B7, e o texto diz `f COM FURO NA ORIGEM`. Os 3 passos do glyph map ficam visíveis (§3, mapa M10). Alvo `14_B4-2_v2` |
| D7 | B5-2 (≈10:20) | Os termos `∬_B + ∬_{B₁} − ∬_{B∩B₁}` não têm o integrando, e o `0,4` não tem origem | Todo termo leva `f`. A linha da solda é `∬_{B∪B₁} f = ∬_B f + ∬_{B₁} f − 0`. A faixa nasce de `0,2 · 2 = 0,4 m²`, com o 0,2 vindo da cota da faixa e o 2 do lado da chapa, e segue em `4 + 0,4 = 4,4 m²` (mapa M11). Alvo `16_B5-2_v2` |
| D8 | B6-1 (≈11:10) | `8/3` aparece direto | `média = massa / área`, depois `= (32/3) / 4`, com o 32/3 voando da régua da massa e o 4 da área, depois `= 8/3 ≈ 2,67` (mapa M12). Alvo `18_B6-1_v2` |
| D9 | B6-3 (≈12:45) | A prova não termina na fórmula do teorema | Depois de "Esse é o ponto érre, ésse": `f(r, s) = média = ∬f/α` e, por glyph map, `∬_B f = α f(r, s)`. O ponto (r, s) fica marcado no caminho. Alvo `20_B6-3_v2` |
| D10 | S2 (≈16:59) | `12 − 2 · área leve` aparece sem origem | Na fala "conta no papel": `3 kg/m² NA CHAPA TODA, MENOS 2 NO PEDAÇO LEVE`, depois `massa = 3 · 4 − 2 · área leve`, depois `7,06 = 12 − 2 · área leve` (mapa M13). Alvo `26_S2_v2` |
| D11 | S2 (17:28) | O cartão `NO PRÓXIMO VÍDEO · TEOREMA DE FUBINI` fica ≈ 1 s na tela e o CTA o atropela | O cartão entra em "É isso que vamos ver no próximo episódio, com o teorema de Fubini" e **fica até "deixa o like…" terminar** (≥ 8 s). O CTA entra só em "E conta nos comentários" |
| D12 | B1-1 (≈1:10) | `LIMITE DAS SOMAS DE RIEMANN` é escrito antes da integral, que é o que a fala apresenta | Ordem da fala: primeiro `f, g` e `k`, depois a frase sobre convergência ("suas somas de Riemann convergem…"), depois `∬_B f(x, y) dx dy`, com o sublinhado em ∬, B e dx dy nos gatilhos |

### 1.2 Representação: o desenho não mostra o que a fala diz

| # | Bloco | No v1 | v2 |
|---|---|---|---|
| R1 | H1 (0:00–0:40) | Os números da balança ficam em cima dos fios dos pratos | `2,472 kg` e `4,584 kg` **embaixo** de cada prato. As frases da coluna em Space Grotesk. Alvo `01_H1_v2` |
| R2 | B2-2 (≈4:05) | `13 kg? ERRO` é uma frase solta | Régua da massa até 14, com a faixa [4, 12] menta, 7,06 dentro (✓) e **13 marcado como ✗ vermelho fora da faixa**. Texto: `13 kg: FORA DA FAIXA, ERRO`. Alvo `09_B2-2_v2` |
| R3 | 4:06–4:10 | Na transição B2→B3 sobra uma caixa ciano órfã e um traço solto | Sai tudo do B2 antes de o B3 entrar. A régua da QA "rótulo órfão" (§8) pega isso |
| R4 | B3-1 / B3-2 (4:50–6:20) | Na vista frontal, não se vê a **largura** do muro sumindo, que é o argumento. Os rótulos 100 e M ficam abaixo do topo do muro | Inset 2D de **vista de cima** (canto inferior direito) com a cobertura menta da solda em n = 64. A cada refinamento, as células do inset e a largura do muro 3D afinam juntas. `ρ = 100` e `M` vão **presos ao topo do muro** (ponto 3D no `timeline.json`). `COTA, NÃO MASSA` fica ao lado do título da tabela. Alvos `10_B3-1_v2` e `11_B3-2_v2` |
| R5 | B5-1 (≈9:50–10:05) | Os números da mini-balança têm ≈ 22 px, com um duplicado fantasma às 10:00, e os pedaços não se reencontram | Números ≥ 26 px. Um só `2,472` e um só `4,584`, que voam para a soma. Os pedaços **voltam a se encaixar** na solda em "sem arredondar, o total é sete vírgula zero seis" |
| R6 | B6-1 (≈11:10–11:50) | O nível é uma caixa de arestas verticais. `ACIMA DO NÍVEL` continua na tela depois que o coral some. O `8/3` é minúsculo e vertical | O nível é **só um retângulo tracejado no topo**, na altura 8/3, sem arestas verticais. Cada legenda sai junto com o que ela legenda. O `8/3` fica na horizontal, ≥ 30 px, com `\dfrac`. A cena termina **nivelada**, como já está no v1. Alvo `18_B6-1_v2` |
| R7 | B6-3 (12:30–13:20) | O gráfico ao longo do caminho não tem as marcas 0 e 8. O `8/3` está girado e pequeno, e o arco ficou cinza | Eixo vertical com 0, 8/3 e 8 na horizontal, à esquerda. O arco de raio 1,63 volta a ter cor (a do alvo, a mesma do caminho), e não cinza. Alvo `20_B6-3_v2` |
| R8 | B6-5 (≈14:20) | Os cartões não dizem **qual** média, e o ícone da bacia é ambíguo | Subtítulos `TEMPERATURA MÉDIA`, `ALTURA MÉDIA DA CHUVA`, `NÍVEL MÉDIO` e `BRILHO MÉDIO`. A bacia vira uma região de contorno irregular com pingos. Alvo `22_B6-5_v2` |
| R9 | B7-1 (≈14:50) | O `1` fica em cima da borda do disco | Os rótulos `1` e `0` ficam **dentro** do disco, perto dos eixos. `(0, 0): 0/0` com `\dfrac`. Alvo `23_B7-1_v2` |

### 1.3 Tipografia e sobreposições

| # | Onde | No v1 | v2 |
|---|---|---|---|
| T1 | Vídeo inteiro | Frases em serifa dentro de `MathTex`: "integráveis em B", "tem conteúdo nulo", "E SE ρ = 100 NA SOLDA?", "MÉDIA ≈ 1,76", "no disco de raio 1", "compacto, fronteira…", "não muda", "numa chapa de 4" | **Palavra é Space Grotesk** (`Text`, maiúsculas). `\text{}` só para o nome de uma grandeza dentro de uma equação (`média`, `área`, `disco`, `massa`, `área leve`). Uma linha mista é `Text` + `MathTex` lado a lado, com respiro ≥ 0,15 (ver `mista()` no `sb32.html`) |
| T2 | B6-1, B6-3, B7-1, B7-2 (e qualquer outra) | `\tfrac` ilegível: 8/3, 8π/9, 0/0 e o B7-2 inteiro | `\dfrac` sempre. Nenhum glifo de fração abaixo de 26 px em 1080p (13 px no preview 540p). Nenhum rótulo girado. Alvos `18`, `20`, `23` e `24_B7-2_v2` |
| T3 | B3-1 | `\|f\| ≤ M LIMITADA` grudado | `\|f\| ≤ M` e, com respiro, `f LIMITADA` em Space Grotesk |
| T4 | B5-1 | `∪UNIÃO` grudado | Rótulos de leitura (`∪ UNIÃO`, `∩ INTERSEÇÃO`) com espaço e alinhados abaixo do símbolo |
| T5 | B6-2 | ✓ e ✗ encostados nos ícones | ✓ e ✗ a ≥ 0,2 de cada ícone, à direita |
| T6 | B1-1 | `UM NÚMERO FIXO` embaixo de `k constante`, quase encostado | `k CONSTANTE` e, na linha de baixo, `UM NÚMERO FIXO` em GEO, com respiro ≥ 0,2 |
| T7 | B6-2 | `ALGUM PONTO` embaixo de `MÉDIA`, encostado | Mesmo tratamento do T6 |

### 1.4 Palco parado ou vazio

O QA do v1 só achou um trecho parado (B6-4, 3,1 s), porque mede a **tela inteira**: a coluna escrevendo esconde o palco parado. Medindo só o palco:

| Trecho | O que acontece | v2 |
|---|---|---|
| 8:40–8:52 (B4-2) | O painel do furo fica vazio | Entra o disco do B7 com a origem tracejada, que se preenche com 3 valores diferentes (0, 1, 5), enquanto o contador fica parado. Gatilho: "podemos preenchê-los com valores limitados" |
| 10:45–10:50 (B5-3) | As miniaturas param | Cada miniatura se parte e se remonta no seu gatilho ("peça montada", "éle", "materiais diferentes") |
| 12:44–12:56 (B6-3) | Palco sem fórmula, só o gráfico parado | Entram os passos do mapa M7 (§3) e o ponto percorrendo o caminho |
| 13:33–13:40 e 13:58,9–14:02 (B6-4) | Degraus parados | A linha da média 1,76 desliza entre os degraus em "passando por cima da média". No beat (c), o ponto laranja nasce na solda |
| 16:59–17:14 (S2) | Chapa parada | A grade refina em "grades cada vez mais finas", a fórmula da massa entra em "conta no papel" (D10) e as fatias verticais entram em "fatiar a região" |

---

## 2. Regras novas (valem para o vídeo inteiro)

1. **Palavra em Space Grotesk, matemática em `MathTex`.** Não pode haver frase portuguesa em serifa. Exceção: `\text{}` para nome de grandeza dentro de equação.
2. **Fração sempre `\dfrac`**, ≥ 26 px em 1080p, sem rotação. Um passo algébrico por linha.
3. **Rótulo de objeto 3D preso ao ponto que ele nomeia**, exportado no `timeline.json` (topo do muro, nível 8/3), alinhado ≤ 2 px, como no v1.
4. **Legenda sai com o objeto**: nada de "ACIMA DO NÍVEL" sem o coral, nem caixa sem dono depois de uma transição.
5. **Todo termo com origem**: a fórmula-mãe antes do número, cada valor voando da fonte (`TransformFromCopy`) e cada passo como glyph map. É a regra da série, reforçada nos itens D1–D10.

---

## 3. MF-Tools: os mapas

Construa cada mapa só depois de o LaTeX final estar estável. Use `MathTex` de string única dos dois lados. Os índices de desenvolvimento não podem ficar no vídeo.

| Mapa | Bloco | De → para | Detalhe |
|---|---|---|---|
| M1, M2 | B1-3, B1-4 | (v1) | Hoje só acrescentam "= …". No M1, o parêntese abre e `32/3` se parte em `16/3 + 16/3` (os dois 16 vêm do 32, os dois 3 do 3). No M2, `1 · 4 + 2 · 1,53` → `4 + 3,06` → `7,06`, com cada produto colapsando no seu resultado |
| M6 | B5-2 | `∬_{B∪B₁} f = ∬_B f + ∬_{B₁} f − ∬_{B∩B₁} f` → `… − 0` → `∬_{B∪B₁} f = ∬_B f + ∬_{B₁} f` | O v1 perdeu o lado esquerdo. Ele **fica**. O último termo acende em menta, vira `0` e **sai junto com o sinal −** |
| M7 | B6-3 | `m α ≤ ∬f ≤ M α` → `m ≤ \dfrac{∬f}{α} ≤ M` → `m ≤ \text{média} ≤ M` | Passo intermediário obrigatório: os dois α deslizam para baixo de uma barra de fração (`÷ α` em GEO ao lado). Só então `∬f/α` vira `média`. Gatilho: "Dividindo pela área" |
| M8 | B6-3 | `f(r, s) = \text{média} = \dfrac{∬f}{α}` → `∬_B f = α\, f(r, s)` | O α atravessa a igualdade, e a linha final é a fórmula do teorema. Gatilho: "Esse é o ponto érre, ésse" |
| M9 | B3-3 | `m ≈ ρ · L · \text{largura}` → `≈ 6 · 2{,}25 · 0{,}01` → `≈ 0{,}135\ \text{kg}` → `= 135\ \text{g}`; `0{,}01 → 0{,}001` → `13\ \text{g}` | Os valores voam da cena (rótulo do 6, linha L, cota do cordão) |
| M10 | B4-2 | `∬ f − ∬ g` → `∬ (f − g)` → `= 0` | Os 3 passos ficam visíveis. O `f − g` liga às caixas (zero fora, muro na solda) |
| M11 | B5-2 | `0{,}2 · 2` → `0{,}4\ \text{m}^2`; `4 + 0{,}4` → `4{,}4\ \text{m}^2` | O 0,2 vem da cota da faixa, o 2 do lado da chapa |
| M12 | B6-1 | `\text{média} = \dfrac{\text{massa}}{\text{área}}` → `\dfrac{32/3}{4}` → `\dfrac{8}{3} ≈ 2{,}67` | 32/3 da régua, 4 da área |
| M13 | S2 | `\text{massa} = 3 · 4 − 2 · \text{área leve}` → `7{,}06 = 12 − 2 · \text{área leve}` | O `3 · 4` colapsa em `12`. Não precisa resolver (área leve = 2,4721); o próximo episódio faz isso |
| M3–M5 | (v1) | Ficam como estão | |

Total esperado: **≥ 14 glyph maps**. O v1 tinha 8.

---

## 4. Blocos a re-renderizar

| Bloco | Itens | Alvos v2 | Alvos v1 que continuam valendo no bloco |
|---|---|---|---|
| H1 | R1, T1 | 01 | 02 |
| B1-1 | D12, T6 | n/a | 04 |
| B1-2 | D1 | 05 | n/a |
| B1-3 | M1 | n/a | 06 |
| B1-4 | D2, M2 + cena 3D nova `b14k` | 07a | 07 (camadas) |
| B2-2 + transição | R2, R3 | 09 | 08 |
| B3-1, B3-2 | D3, R4, T3 | 10, 11 | n/a |
| B3-3 | D4, M9 | 12 | n/a |
| B4-1, B4-2 | D5, D6, M10, palco | 13, 14 | n/a |
| B5-1, B5-2, B5-3 | R5, T4, D7, M6, M11, palco | 16 | 15, 17 |
| B6-1 | D8, R6, M12 | 18 | n/a |
| B6-2 | T1, T5, T7 | n/a | 19 |
| B6-3 | D9, R7, M7, M8, palco | 20 | n/a |
| B6-4 | palco | n/a | 21 |
| B6-5 | R8 | 22 | n/a |
| B7-1, B7-2 | R9, T2 | 23, 24 | n/a |
| S2 | D10, D11, M13, palco | 26 | n/a |

**Não mudam:** H2, A1, B2-1 e S1. Varra-os ainda assim com o QA T1/T2 (§8): se aparecer frase em serifa ou `\tfrac`, corrija só isso.

**Cena 3D nova `b14k`** (`c3d32.html?k=b14k`):
- as caixas de f = x² + y², n = 4, com altura negativa (`z0 = −ZS·v`) abaixo do chão;
- o chão em contorno com grade;
- câmera `ver([4.9, −7.4, 1.6], [1, 1, −.55], 600, 470)` e eixo z de −2,3 a 0,4;
- pontos em `r3d_pts.json` (`b14k`: `ex`, `ey`, `ez`, `kq`, `chao`).

Porte para o `threejs/` da unidade como as outras sete. A transição k = 2 → ½ → −1 pode usar a cena `b14` do v1 com a escala z animada e terminar em `b14k`.

---

## 5. Quadros-alvo v2

Ficam em `yt_0032_quadros_alvo_v2/` (1920×1080). A folha de contato é `00_folha_contato_v2.jpg`.

| Arquivo | Bloco · gatilho |
|---|---|
| `01_H1_v2_balanca_rotulos_fora_dos_fios.jpg` | H1 · "Usando os valores sem arredondar" |
| `05_B1-2_v2_f_e_g_nas_rampas_3D.jpg` | B1-2 · "Então a soma de Riemann de éfe mais gê" |
| `07a_B1-4_v2_k_menos_1_3D.jpg` | B1-4 · "se é negativo, a contribuição troca de sinal" |
| `09_B2-2_v2_13_fora_da_faixa_3D.jpg` | B2-2 · "já saberíamos que tem erro" |
| `10_B3-1_v2_integral_com_modulo_3D.jpg` | B3-1 · "limitada por eme vezes a área da cobertura" |
| `11_B3-2_v2_vista_de_cima_3D.jpg` | B3-2 · "Com sessenta e quatro divisões por lado" |
| `12_B3-3_v2_massa_do_cordao.jpg` | B3-3 · "Com um milímetro, uns treze gramas" |
| `13_B4-1_v2_f_e_g_definidos.jpg` | B4-1 · "a integral de éfe é igual à de gê" |
| `14_B4-2_v2_sem_letras_novas.jpg` | B4-2 · "O valor da integral não depende de como preenchemos o furo" |
| `16_B5-2_v2_faixa_com_origem.jpg` | B5-2 · "Os quatro décimos extras são a faixa contada duas vezes" |
| `18_B6-1_v2_media_formula_mae_3D.jpg` | B6-1 · "O volume retirado e o preenchido são iguais" |
| `20_B6-3_v2_divide_por_alfa_e_conclusao.jpg` | B6-3 · "Esse é o ponto érre, ésse" |
| `22_B6-5_v2_o_que_e_a_media.jpg` | B6-5 · "O brilho médio de uma região numa imagem digital" |
| `23_B7-1_v2_rotulos_dentro.jpg` | B7-1 · "pelo eixo horizontal, o valor é um; pelo vertical, zero" |
| `24_B7-2_v2_fracoes_grandes.jpg` | B7-2 · "cada um vale pi sobre dois" |
| `26_S2_v2_massa_com_origem.jpg` | S2 · "numa conta no papel" |

O alvo mostra o **estado no gatilho**. A ordem de entrada é a da fala, e nada aparece antes da vez. A arte do v1 (cordão, metal, balança) prevalece sobre o esquema do alvo.

---

## 6. Tempo

A **narração v3 não muda** (Anexo A do handoff v1 e `narracao_v3.md` no zip). A contagem de 3.168 palavras contra 3.160 não importa. O preview v2 deve ficar entre 17:40 e 18:10. Nenhum item deste documento pede frase nova: todos os gatilhos já existem na v3.

O sympy não está na `.venv`. Não o instale lá (AGENTS.md: não alterar dependências). Para rodar `verifica_calc3_32t3_sympy.py`, use `uvx --with sympy python …` ou um Python do sistema. Também pode pular: os números já foram conferidos (19 checagens `True`), e os do M9–M13 estão no §7.

---

## 7. Números dos mapas novos (conferidos)

- 6 · 2,25 · 0,01 = 0,135 kg = 135 g; 6 · 2,25 · 0,001 = 0,0135 kg ≈ 13 g.
- 0,2 · 2 = 0,4 m²; 4 + 0,4 = 4,4 m².
- (32/3)/4 = 8/3 ≈ 2,667.
- 3 · 4 − 2 · 2,4721 = 7,0558 ≈ 7,06. A área leve vale 2,4721, e 2,472 · 1 + (4 − 2,472) · 3 = 7,056.
- m = 0 e M = 8 na chapa [0, 2]², com f = x² + y²; 8/3 ∈ [0, 8].
- Raio do arco: √(8/3) = 1,633.

---

## 8. QA do preview v2 (obrigatório)

Repetir o do v1 (R5 = 0, flash por quadro = 0, alinhamento 3D ≤ 2 px, prancha) e acrescentar:

1. **`fracoes_v2.txt`**: para cada `MathTex` com fração, a altura do numerador em px (1080p equivalente). Nenhuma abaixo de 26, nenhuma `\tfrac` no código (`grep -n tfrac` = 0) e nenhum rótulo girado.
2. **`texto_em_mathtex_v2.txt`**: liste todo `\text{…}` com mais de uma palavra ou com verbo. O esperado é zero frase, só nomes de grandeza.
3. **`palco_parado_v2.txt`**: mede trechos parados **só na área do palco** (máscara sem a coluna e sem o canto). Nenhum trecho com mais de 6 s de palco parado enquanto a voz fala. Liste também os trechos de 3 a 6 s.
4. **`origens_v2.txt`**: para cada número ou termo dos itens D1–D10, diga de onde ele voa (objeto-fonte) ou qual mapa o produz.
5. **Rótulo órfão**: em cada fronteira de beat, nenhum mobject cujo dono saiu (a caixa ciano das 4:06 e o "ACIMA DO NÍVEL").
6. **Cartão Fubini**: tempo de tela ≥ 8 s, e o CTA não se sobrepõe a ele.
7. **Contagem de glyph maps**: ≥ 14, com a lista mapa → bloco → tempo.

---

## 9. O que NÃO fazer

- Mudar a narração, os números ou a ordem das cenas.
- Desfazer a arte do meio da rodada (cordão, metal, balança, mapas de cor).
- Acrescentar efeito: partícula, brilho, sombra, névoa, transparência decorativa ou câmera girando sem motivo.
- Fazer 3D dentro do Manim (ThreeDScene). Todo 3D, inclusive o `b14k`, é Three.js.
- Re-renderizar blocos que não mudaram.
- Gerar voz, SRT, 1080p, master ou entrega, e fazer commit ou push.

---

## 10. Parada

Entregue o preview v2, a prancha e os relatórios do §8, e pare. No relatório:
- os arquivos alterados;
- os blocos re-renderizados e o tempo de cada um;
- os resultados do QA;
- o caminho do MP4;
- as pendências reais.

Não comece a fase de voz.
