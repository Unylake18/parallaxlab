# yt_0044 · CÁLCULO III · EP. 19 · Exercícios do módulo: integral tripla
# Avaliação do preview v1 + HANDOFF v2 (preview)

**Para:** Claude Code, no repositório (`videos_longos/yt_0044_*`).
**Fase:** PREVIEW v2 (540p / 15 fps). Sem voz, sem SRT, sem 1080p, sem entrega.
**Vale junto com:** `yt_0044_handoff_v1_1.md`. Tudo o que este documento não muda continua valendo como está no v1.1: contas, 2D, gatilhos, lotes, GM1–GM21 e QA de 20 itens. Onde os dois diferem, vale este.
**Referência nova:** `referencia/yt_0044_quadros_alvo_v2/` (substitui a pasta `_v1` como alvo visual) e `yt0044_3d_v1_x_v2.jpg` (prancha antes/depois dos 16 quadros 3D).

---

## 0. Veredito do preview v1

**Ainda não vai para a narração.** O que está aprovado e não deve ser mexido:
- a matemática (63/63 degraus);
- todo o 2D: colunas, painéis, H2, E1-2, E2-4 etapa 2, E3-4, E4-3, E5-1 etapa 1, E5-3, E6 e S1;
- a escrita (caneta, voo, glyph map, FLASH 0);
- o alinhamento 3D × Manim (0,010 px).

**O que reprova é o 3D**, e a causa está nos alvos v1, não na implementação. O preview reproduziu fielmente desenhos que já vinham poluídos. O Kaio pediu: "melhorar muito as representações gráficas do 3D, ficar tudo alinhado na grade, sem poluir demais, deixando bem legível, sem sobreposições". Os problemas medidos nos alvos v1 e no preview:

| # | Problema | Onde |
|---|---|---|
| P1 | O piso quadriculado vai até a borda da tela, sem fim nem moldura, e compete com o papel | todas as cenas 3D |
| P2 | A origem O e o eixo z caem entre as linhas do papel, então o 3D "flutua" fora da grade | todas |
| P3 | Letras soltas (R, h, 2R, Δz) ficam em cima de arestas e faces, em vez de cotas | H1, E1-5, E3-1/2/3, E5-2 |
| P4 | Placas e marcas encostadas umas nas outras: φ sobre ⊕, `raio` sobre ⊕, 1/2 sobre 5/9, h/2 sobre 3h/4 | E1-4, E3-2, E4-1, E4-2 |
| P5 | Arame redundante: caixa de arame em volta do cubo de caixinhas, pés tracejados da sonda, contorno duplo na sombra do tetra, verticais da hélice | E1-1, E1-3, E2-1/2, S2 |
| P6 | Tetraedro grande demais (piso enorme, eixo encostando no título) e centroide grudado na origem | E2-1/2/3 |
| P7 | Lata grande demais no H1 e no E5-2, com o piso cortado pela borda | H1, E5-2 |
| P8 | Tracejado h/2 invisível dentro do cone | E3-2 |

As três pendências do relatório v1 também entram nesta passada (§4).

---

## 1. Regras 3D novas (G7–G12, somam-se a G1–G6)

- **G2 (revista) · Piso finito com moldura.** O piso fica só em volta do objeto: linhas internas `#3E4474` a cada 0,5 unidade e moldura `#545A8C` com 1,5× a espessura. Extensões na tabela `PISOK` do `_tail3d.txt` v2: lata [−1,5; 1,5]²; dobradiça [−0,5; 2,5] × [−1,5; 1,5]; cubos [−0,5; 1,5]²; tetra [−0,25; 1,25]²; cone, meia bola e hélice [−1,5; 1,5]². O piso fica em z = −0,03, **abaixo** das faces, e nunca as atravessa.
- **G7 · Escala que cabe.** O 3D nunca é cortado pela borda nem pelo clip da coluna. Os fatores `DF` estão no `cenas44.js` v2: lata 2,0; cubos 1,55; tetra 1,85 com SC 2,4; cone 1,6; meia bola 1,6; hélice 2,0.
- **G8 · Origem na grade.** O ponto O projetado cai **numa interseção do papel de 60 px** (função `cena3d` do `sb44.html` v2: `SNAP`). O eixo z sobe sobre uma linha vertical do papel. Para implementar: depois de posicionar o PNG pelo offset (OL/OC/OT/OM), desloque o 3D **e todos os rótulos presos a ele** pelo mesmo `SNAP` (arredonda O para múltiplo de 60 px em 1080p, ou 30 px em 540p). A tolerância de alinhamento continua ≤ 2 px.
- **G10 · Cota em vez de letra solta.** Uma medida (2R, h, Δz, h/4, 3h/4) é uma **cota**: segmento fino `#C9D2E6` com tracinhos nas pontas, paralelo à medida e **fora** do objeto, com a placa no meio (helper `cota(A,B,nome,fora)` no `cenas44.js` v2). R é um **raio desenhado** na tampa, com a placa no meio do raio.
- **G11 · Distância mínima.** Duas marcas (placa, ⊕, ponto, rótulo de eixo) ficam a **≥ 40 px** uma da outra em 1080p (os centros) e nenhuma placa cobre ⊕, ponto ou aresta de destaque.
- **G12 · Sem arame redundante.** Uma aresta aparece uma vez só: sem caixa de arame em volta de sólido opaco, sem contorno duplicado sobre face preenchida, sem pés tracejados, sem verticais decorativas. Faces opacas.

**Continua proibido** (memória da série): pulso, palco vivo, tracer, brilho, sombra, partícula, câmera se mexendo. Todas as câmeras continuam fixas.

---

## 2. Correções cena a cena (o alvo v2 é a referência; a prancha mostra o antes e o depois)

| Alvo v2 | Cena 3D | O que muda |
|---|---|---|
| 01 H1 | `lataParede` | Lata menor (DF 2,0), piso [−1,5; 1,5]² com moldura e inteiro na tela. Eixo central azul curto, só acima da tampa. Eixo da parede tracejado ALERTA até z = 1,75. Seta de giro em z = 1,6. A placa `EIXO` sai e entra a **cota `2R`** no chão, na frente da lata. |
| 03 E1-1 | `cuboCaixas` | Sai a caixa de arame externa. As 8 caixinhas afastadas com as placas de ρ no topo. Placas a ≥ 40 px entre si. |
| 05 E1-3 | `cuboSonda` | Saem os pés tracejados no chão. Sonda azul-claro (entra em z = 0) → coral (sai em z = 1). |
| 06 E1-4 | `cuboDiag` | O anel do centro vira um **tracinho GEO** na diagonal em (½,½,½), com placa `1/2`. O ⊕ (raio 13 px, sem anel) fica em (5/9,5/9,5/9) com placa `5/9`. As duas placas ficam em lados opostos da diagonal. |
| 07 E1-5 | `cuboFolha` | Um contorno só da camada de altura Δz, mais a **cota `Δz`** na aresta da frente. A tampa lima continua. A cota está pequena no alvo: no Manim, placa de 28 px no mínimo. |
| 08–10 E2-1/2/3 | `tetraSonda`, `tetraCent` | Nova câmera `ver([8.6,4.2,5.4],[.36,.36,.30],600,560)`, SC 2,4 e DF 1,85. Piso [−0,25; 1,25]². A sombra pêssego é **só preenchida**, sem contorno duplicado. O eixo z fica abaixo do título (y > 110). No E2-3, o centroide (¼,¼,¼) aparece **separado** da origem, com os tracejados GEO aos vértices. |
| 12 E3-1 | `cone` | R = raio desenhado na tampa com placa. h = cota vertical em `Cc(1.32,−.62π)`, fora do cone. Sonda em tt = −0,25. |
| 13 E3-2 | `coneCm` | A cota h se divide em **3h/4** (do vértice ao ⊕) e **h/4** (do ⊕ à tampa), com as placas nos meios. O tracejado h/2 sai do miolo e vai para o **quarto aberto** (onde a fatia foi tirada), com a placa `h/2` ao lado. O ⊕ fica em z = 3h/4. |
| 14 E3-3 | `coneCasca` | A mesma cota h e o raio R desenhado. A casca pêssego de raio s, o fio s com placa (28 px) e a seta de giro. |
| 16 E4-1 | `semi` | Arco de φ com raio 0,30 e placa em 0,44. O ponto P vai para ff = 0,36π e rr = 0,85. r, φ e z ficam com as placas centradas, todas a ≥ 40 px do ⊕ (3R/8). |
| 17 E4-2 | `semiFatia` | A fatia sobe para zf = 0,8. O raio da fatia é desenhado em ângulo −0,06π, com a placa `√(R²−z²)` **fora** da cúpula. O ⊕ fica visível. |
| 19–20 E5-1/2 | `lataDobradica`, `lataDob3` | DF 2,0, piso [−0,5; 2,5] × [−1,5; 1,5] inteiro. Eixo z azul na parede até 1,75 e seta de giro em 1,6. O fio R e as placas R e s ficam fora das arestas. |
| 26 S2 | `helice` | Saem as verticais da lata (só os dois anéis em traço). A conta fica na frente (t = 2π − 0,75) com a seta F mais longa e a placa F deslocada. |

**Placas e eixos (sb44.html v2):** os rótulos x, y, z dos eixos ficam a +0,10/+0,12 da ponta (`eixos3` no `_head3d.txt` v2). As placas de variável têm no mínimo 28 px em 1080p.

O 2D dos alvos 02, 04, 11 (painel), 15, 18, 21–25 **não mudou**. O pixel desses alvos v2 é igual ao do v1.

---

## 3. Como portar

1. Troque `referencia/yt_0044_quadros_alvo_v1/` por `referencia/yt_0044_quadros_alvo_v2/` (zip). Não apague o v1 antes de o preview v2 passar.
2. No `threejs/c44.js` da unidade, porte do `cenas44.js` v2 **os mesmos parâmetros**: câmeras, SC, DF, `cota()`, `PISOK` e `piso()` com moldura, `eixos3` com os rótulos novos. Os estados animáveis continuam os da tabela do v1.1 §4, com estas trocas:
   - `cuboDiag.centro` = tracinho GEO (não anel);
   - `cuboFolha.caixas` = camada única + cota Δz;
   - `cone*`: estado novo `cotas` (raio R + cota h; em `coneCm`, a divisão 3h/4 + h/4 e o tracejado h/2 no quarto aberto);
   - `lataParede`: estado novo `cota` (2R) no lugar da placa `EIXO`.
3. No `Palco3D` do Manim, aplique o `SNAP` do G8 (O em múltiplo de 60 px a 1080p) ao PNG **e** aos rótulos. Meça de novo o alinhamento.
4. Rerrenderize **só os lotes com 3D**: **PH, PE1, PE2, PE3, PE4, PE5, PS**. **PE6 e PA não mudam** (não rerrenderizar; reutilizar os segmentos do v1).
5. Ordem sugerida: PE3 (calibra cotas e SNAP) → PE2 (câmera nova do tetra) → PE1 → PE4 → PE5 → PH → PS.

---

## 4. Pendências do relatório v1 (resolver nesta passada)

1. **Gatilho em +0,33 s:** puxe-o para ≤ 0,2 s (a regra da série). Recalcule só aquele trecho.
2. **Pausas de 0,6 a 4 s com só o papel e o título na tela:** não pode haver tela vazia. Na troca de etapa, o desenho da etapa nova entra **no começo** da pausa (o 3D já posto ou a primeira linha começando a ser escrita); a pausa fica sobre conteúdo. **Não** resolver com efeito (sem pulso, tracer ou palco vivo). Liste no relatório cada pausa > 0,5 s com o que está na tela.
3. **Emenda PE4 → PE5 com o degradê a ~30 %:** o fundo tem que estar **idêntico** dos dois lados da emenda (mesmo degradê, mesmo papel, mesma fase). Corrija a origem (provavelmente o PE5 nasce com o fundo em transição); não esconda com fade. Gere `emendas_v2.jpg` (último quadro de cada lote × primeiro do seguinte).

---

## 5. QA v2 (soma-se aos 20 itens do v1.1)

| Item | Critério |
|---|---|
| Q21 · Piso | Todo piso inteiro na tela, com moldura, sem atravessar faces (16 quadros 3D) |
| Q22 · Grade | O projetado no cruzamento do papel: erro ≤ 2 px em 1080p, listado por cena |
| Q23 · Cotas | Nenhuma letra de medida solta em cima de aresta ou face: cada uma é cota ou raio desenhado |
| Q24 · Distância | Menor distância entre centros de marcas por quadro ≥ 40 px (tabela por cena, com o par mais próximo) |
| Q25 · Arame | Zero caixa de arame externa, contorno duplo, pés tracejados ou verticais na hélice |
| Q26 · Corte | Nenhum pixel do 3D cortado pela borda nem passando do clip da coluna (G3) |
| Q27 · Pausas | Lista das pausas > 0,5 s com o conteúdo na tela; zero tela só com papel e título |
| Q28 · Emendas | `emendas_v2.jpg`, com o fundo idêntico nos dois lados de toda emenda |
| Q29 · Comparação | Para os 16 quadros 3D, uma prancha lado a lado alvo v2 × preview v2 (mesmo instante, 1080p nativo) |

Os quadros conferidos são em resolução cheia (sem reduzir). Os stills de comparação são 1080p nativos, como no v1.1.

---

## 6. O que entregar

- O preview v2 em 540p / 15 fps (mp4 inteiro). Só os lotes 3D foram refeitos; os outros, emendados do v1.
- `qa/` com Q1–Q29.
- `comparacao_v2/` com os 16 pares alvo × preview, `emendas_v2.jpg` e a prancha geral.
- Um zip para avaliação, no mesmo formato do v1 (`yt0044_v2_para_gpt.zip` + quadros em partes, se precisar).
- O relatório obrigatório do AGENTS.md: arquivos alterados; renders feitos e tempos; o alinhamento medido; Q21–Q29; o que não deu.

## 7. Parada

Pare depois do preview v2 e do relatório. **Não** comece voz, SRT, 1080p nem entrega. Sem commit, branch ou push, salvo pedido.
