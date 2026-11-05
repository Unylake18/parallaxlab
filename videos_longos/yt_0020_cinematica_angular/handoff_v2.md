# R1 (yt_0020) · Avaliação quadro a quadro do preview v1 e HANDOFF v2 — "Cinemática angular: por que a ponta da hélice chega a quase 1.000 km/h?"

2026-11-03 · Produção → Claude Code · unidade `videos_longos/yt_0020_cinematica_angular/`

Complementa o handoff v1: tudo que não é citado aqui continua valendo (física congelada, narração v1.1 já embutida nas âncoras do v1, cores por família, fundo, layout, G1–G28). **Não alterar texto da narração nem números.** Fase aberta: preview visual silencioso 960×540 / 15 fps do vídeo inteiro. Não criar voz, SRT, master, entrega, commit nem push.

Como foi feita a análise: as 11 pranchas do `qa_pranchas` (PH, PA, PT1–PT5, PE1–PE3, PS-EN), a prancha humana de 24 quadros e os 24 quadros de conferência em tamanho cheio, mais o `qa.txt`. Referência de quadro no formato da conferência: `âncora_%` (ex.: `T5-8_85` = âncora T5-8 a 85% da sua duração).

---

## 1. Veredito do v1

**O que está bom e não deve regredir:** física e números (34/34), proporções das setas, área = ângulo no T3-4, produto vetorial independente de O, corrente 2,5×, alinhamento 3D ≤ 0,54 px, duração (26:56), capítulos, fundo azul, cartões do resumo, tabela 1D ↔ giro do T3-6 (ideia certa), gráfico logarítmico do E1-6.

**O que reprova o v1 (pedido do Kaio + análise):**
1. **Portão G28 não foi cumprido.** O `qa.txt` registra **38.696 ocorrências** (ENCOSTADO 13.055, TEXTO SOBRE OBJETO 9.555, FORA DA ZONA 6.796, TEXTO PEQUENO 3.868, CALHA 3.520, CHAMADA CRUZA CORPO 774, OBJETO FORA DA MARGEM 279, SOBREPOSIÇÃO 252, SELO DUPLO 177, RÓTULO SOLTO 148, SEM PALCO 93, FORA DA MARGEM 91, TEXTO SOBRE CAIXA 58, LINHA ÓRFÃ 16, TRÂNSITO 7). O relatório chamou isso de "avisos menores"; não são: o handoff pede **zero** em todas essas classes, com exceção justificada por ocorrência. O Kaio contou ~23 sobreposições visíveis e coisas cortadas; a lista completa está no §4.
2. **Álgebra quase sem MF-Tools e fora da ordem de escrita.** As linhas entram prontas (FadeIn/Write da linha inteira) ou em blocos; quase não há `TransformByGlyphMap`, `TransformMatchingTex` nem `TransformFromCopy` saindo do desenho. O Kaio quer **usar e abusar do MF-Tools** e **cada linha escrita da esquerda para a direita, na ordem da álgebra, como se alguém estivesse escrevendo** (§2 e §5).
3. **Objetos pequenos e tela vazia.** Hélice ~20% do quadro, disco do T3-6 e ícones minúsculos, metade direita vazia em vários trechos (T1-3, T4-3, T4-6, E2-2). G3 pede 55–75% do ESQUEMA.
4. **Cor abaixo da meta** em 5 capítulos: Abertura 20,4%, T2 29,2%, E2 17,9%, E3 24,9%, Encerramento 29,4% (meta ≥ 30%). E o T5 deu 80,4% por um motivo errado: o disco 3D está pintado de lavanda chapado, cor que não é de nenhuma família (§6).
5. **3D e 2,5D sem acabamento.** Hélice com pás chapadas, disco 3D do T5 como elipse lisa sem espessura nem material, livros pequenos e ambíguos (não dá para ver para onde aponta a capa), Terra pequena; os desenhos 2D são planos (§7).

**Metas do v2 (critério de aceite):** G28 = 0 real (com `qa.txt` classificado); auditoria nova `ORDEM` = 0 falhas; 100% das linhas da CONTA construídas (nenhuma por FadeIn de linha inteira); objeto principal 55–75% do ESQUEMA; cor ≥ 30% em todos os capítulos, contando só cores de família; nenhum trecho parado ≥ 3 s; nenhuma coluna vazia > 5 s.

---

## 2. Escrita da álgebra: primitiva única (P0)

O mesmo defeito apareceu no R2 (yt_0021) e foi especificado assim; vale igual aqui. Se a unidade do yt_0021 já tiver essa primitiva implementada e validada, **copie** o código para a unidade do yt_0020 (não importe nem altere a outra unidade).

1. **Ordem por x.** Ordenar as partes da linha pelo x do glifo (esquerda → direita). Cada parte k começa em `t0 + k·δ` (δ entre 0,12 e 0,25 s, escolhido para a linha caber na fala). Nada à direita de uma vaga vazia aparece antes do seu instante. Nunca nasce o "esqueleto" (`=`, `+`, barras, parênteses) com buracos para as letras chegarem depois.
2. **Parte fixa** (`=`, `+`, número novo, operador): `Write` curto (≤ 0,2 s) na própria vaga, no seu instante. **Parte que voa** (símbolo que já existe no desenho ou na linha de cima): `TransformFromCopy` saindo da origem ~0,15 s antes e pousando na vaga no seu instante. O original fica onde estava (G14: cópia nunca sobre o original).
3. **Estruturas.** Fração: numerador → barra → denominador. Expoente junto da base. Parênteses: o de abertura nasce com o primeiro termo de dentro e o de fechamento depois do último. Raiz: símbolo → radicando. Integral: símbolo → limites → integrando → `dt′`. Limite: `lim` → `Δt→0` → fração.
4. **Passo entre linhas (`TransformByGlyphMap`):** a linha nova nasce já na vaga de baixo (nunca em cima da linha-mãe); os glifos mapeados viajam da linha de cima e os glifos novos entram **intercalados na mesma fila por x**. Termo que sai (cancelado com risco, ou que atravessa o `=`) sai **antes** do que ocupa o seu lugar.
5. **Caixa de resultado** (`PANEL` com borda): contorno e conteúdo entram juntos; nunca caixa vazia.
6. **Pausa de leitura** de 0,3 s depois da linha completa, antes de qualquer destaque.
7. **Números substituídos** saem do rótulo no desenho (cota, rótulo de rpm, eixo do gráfico), um por vez, na ordem da fala, e já na cor da grandeza (G24).
8. **Auditoria nova `ORDEM`** no `qa.txt`: para cada linha construída, registrar o instante em que cada glifo passa de 50% de opacidade; falha se existir par (i à esquerda de j) com `t_i > t_j + 0,05 s`. Conferir também por imagem a 10 fps durante cada construção: o conjunto de colunas visíveis (ou em voo) deve ser sempre um prefixo da linha.
9. **Contagem no `algebra.txt`:** por âncora, quantas linhas foram por `passo` (GlyphMap), por `TransformMatchingTex`, por construção com voos e por FadeIn. Meta: FadeIn só para enunciado, nota e selo; **zero linha de equação por FadeIn**.

---

## 3. Portão G28 de verdade (P0)

**Diagnóstico pela distribuição:** as classes grandes são sistemáticas (vêm de uma peça, não de uma cena): ENCOSTADO e TEXTO PEQUENO concentrados nos exercícios (PE1 12.846, PE2 6.906, PE3 5.533) indicam selo de 2–3 linhas com padding apertado e rótulos de ESQUEMA abaixo de 24 pt; FORA DA ZONA 1.948 só no PT3 indica CONTA posicionada fora da `Pilha`; CHAMADA CRUZA CORPO 774 no PT1 é a linha-guia de `EIXO FIXO` atravessando o disco. **Corrigir na peça primeiro** (selo, rótulo, pilha, chamada), depois cena por cena.

Regras que a correção deve seguir:
- **Nunca resolver encolhendo.** Linha larga quebra em duas linhas alinhadas pelo `=` (nunca fator < 0,85 na equação; o v1 chegou a 0,63 no PE2). Tamanhos mínimos do G1 valem em todo quadro: selo ≥ 24, frase-chave ≥ 30, rótulo MathTex no ESQUEMA ≥ 36, equação na CONTA ≥ 46.
- **Selos:** padding vertical ≥ 0,10 u, horizontal ≥ 0,16 u, entrelinha ≥ 1,15; selo alargado para caber em **uma** linha sempre que possível; no máximo 2 linhas. **Um selo por vez** na faixa de selo (G7). CÂMERA LENTA e FORA DE ESCALA viram um **marcador pequeno fixo no canto inferior do ESQUEMA** (não na faixa, não sobre setas), e um só por vez.
- **Rótulos** por `rotulo(obj, lados=[...])` com teste de colisão contra objetos, setas, rótulos e trajetórias dos próximos 2 s; rótulo de ponto que gira acompanha o ponto e fica sempre horizontal (G27).
- **Linha-guia** (chamada) nunca cruza corpo, pá, raio ou seta: sai pelo lado livre, em L se precisar.
- **Nada sai do quadro** (margem 0,45), inclusive setas longas em perspectiva e a órbita do E3.
- **`qa.txt` do v2:** tabela por classe e por lote, antes/depois; cada ocorrência que sobrar classificada como falso positivo **com motivo escrito**. Meta: 0 real.

---

## 4. Mapa quadro a quadro: sobreposições, cortes e defeitos (corrigir todos)

Numeração S = sobreposição, C = corte/fora do quadro, D = defeito de leitura. Os ~23 casos que o Kaio viu estão aqui dentro.

### Hook (PH)
- **S1 H2_85:** o arco curvo de `2.700 RPM` cruza a seta da ponta (as duas saem do mesmo canto). Seta curva no cubo, do lado oposto ao da seta da ponta.
- **S2 H2:** `CÂMERA LENTA ×90` e `NÚMEROS TÍPICOS` ao mesmo tempo, fora da faixa (SELO DUPLO). Ver regra de marcador no §3.
- **D1 H1–H2:** hélice ocupa ~20% do quadro, encostada no canto superior esquerdo, e a coluna de números pesa mais que o objeto. Hélice grande e centrada no PALCO (diâmetro ≈ 65% da altura), números entrando só depois e menores (§7.1).
- **D2 H1:** a seta do ponto a 10 cm é invisível (pela proporção 1 : 9,5 ela fica < 0,2 u). Não quebrar a proporção: mostrar a diferença com **rastros** dos dois pontos no mesmo Δt (rastro curto perto do eixo, rastro longo na ponta, violeta com fade), e a seta curta com um anel de destaque e o rótulo `≈ 100 km/h` preso a ela. Se ainda assim a seta curta ficar abaixo do G8, registrar exceção justificada.
- **D3 H2:** barra da velocidade do som sem a marca `78%` escrita e sem a ponta da hélice ligada à marca. Marca vertical violeta na barra com `78%`.

### Abertura (PA)
- **D4 A2–A3:** ícones pequenos, tela vazia e cor 20,4%. Ícones ≥ 1,2 u, em cor de família (arco âmbar, seta violeta, setas verdes). A3: a partícula maior, girando de verdade com a seta tangente violeta e a seta verde para o centro acompanhando; a multiplicação em várias partículas ocupa o PALCO inteiro antes de virar o disco.

### T1 · Como medir um giro? (PT1)
- **S3 T1-3_60:** rótulo `r` em cima da linha de referência tracejada. Rótulo do lado de baixo do raio, fora da linha.
- **S4 T1-1/T1-3:** chamada `EIXO FIXO` aponta para a **borda** do disco (a linha-guia cruza o disco, origem das 774 CHAMADA CRUZA CORPO). Deve apontar para o **centro** (o pino), com a linha saindo pelo lado livre.
- **D5 T1-3:** os pontos do raio são pequenos (≈ 6 px) e os arcos s₁, s₂, s₃ não nascem do movimento. Pontos ≥ 0,12 u; cada arco âmbar é **desenhado pelo próprio ponto** enquanto a linha pintada varre o θ.
- **D6 T1-3:** `θ = s/r` solta no alto da coluna direita, metade da tela vazia. Ver §5 (T1-3): θ, s e r voam do desenho.
- **D7 T1-4:** linha `EM GRAUS: s = rθ · π/180` espremida, `SOBRA` e o selo `DICA` escondidos/encostados. Uma linha por vez na `Pilha`; DICA só depois que a linha de graus sair ou subir a 40%.
- **S5 T1-5:** sinal `−` sobre a seta curva horária. Sinais `+` e `−` fora das setas, ao lado das pontas.
- **D8 T1-5_90:** as três voltas aparecem como anéis concêntricos em cima do marcador do eixo (parece alvo, não giro). Espiral âmbar que cresce para fora a cada volta, começando fora do pino.
- **D9 T1-5_90 (consistência):** o MOSTRADOR marca **57°** enquanto o ACUMULADO marca **Δθ = 18,85 rad** (= 6π, que deveria dar **0°** no mostrador). Mostrador e acumulado devem vir da mesma variável: `mostrador = Δθ mod 2π` em todo quadro. Auditoria nova `MOSTRADOR` (T1-5 e E1-3).
- **D10 T1-5:** `2π 4π 6π` órfãos numa linha sem relação. O contador mostra o valor atual sozinho e, no fim, `Δθ = 6π ≈ 18,85 rad` (âmbar), com o `6π` vindo da troca 2π → 4π → 6π por `TransformMatchingTex`.

### T2 · Quão rápido gira? (PT2)
- **D11 T2-1/T2-2:** as cópias estroboscópicas são linhas de diâmetro inteiro (parece um leque cortando o disco). Cópias só do raio pintado, com opacidade decrescente (60% → 15%).
- **S6 T2-2:** rótulo `Δθ` em cima de uma das linhas. Rótulo fora do arco, do lado de fora do disco.
- **D12 T2-1:** `ω_méd` escrito com `\text{méd}` reto e cinza; subscrito herda a cor da letra (violeta).
- **D13 T2-3_70:** setas violeta muito apagadas e finas (parecem fantasma) e linhas cinza do centro a cada ponto confundem com raios. Setas cheias (opacidade 100%, espessura ≥ 5), sem as linhas cinza; os três arcos âmbar com o mesmo Δθ marcado por um único arco âmbar perto do centro.
- **D14 T2-4:** ícone da hélice minúsculo no canto do PALCO. A hélice volta grande (≥ 50% do PALCO) e o `282,7 rad/s` voa da CONTA para o cubo dela.
- **D15 T2-5:** listas de durações de volta em texto. Mostrar no cronômetro: cada volta acende um segmento do anel do cronômetro, com o tempo da volta escrito ao lado do segmento; no giro acelerado os segmentos ficam visivelmente diferentes.

### T3 · E quando o giro acelera? (PT3)
- **D16 T3-2:** setas curvas ambíguas e o rótulo `FREANDO` não aparece. Três discos com as setas ω (violeta) e α (verde) em raios diferentes (ω por fora, α por dentro), rótulo embaixo de cada disco: `GIRANDO MAIS RÁPIDO`, `FREANDO`, `TAMBÉM ACELERANDO`.
- **D17 T3-4_45:** área pintada em marrom escuro (não é âmbar) e o triângulo sem distinção do retângulo. Retângulo âmbar 45% e triângulo âmbar 70%, separados por uma linha fina branca; rótulos `ω₀t` e `½αt²` dentro de cada um, em âmbar cheio; a tirinha `ω dt` âmbar 100%.
- **S7 T3-4_97:** o disco desce sobre o pico do gráfico e sobre o rótulo `+2π`. Disco do lado do gráfico (não acima dele), ou gráfico mais baixo.
- **D18 T3-4 inset:** área de baixo sem preenchimento (só contorno) e o `−2π` pequeno. Área de cima âmbar 45%, área de baixo âmbar 45% com hachura, `+2π` e `−2π` ≥ 36.
- **S8 T3 (selo ÁREA COM SINAL):** selo encostado sobre a CONTA. Selo na faixa, a CONTA começa abaixo dela.
- **D19 T3-6_95:** disco minúsculo e o rótulo `1D` cinza pequeno, coluna 1D sem cor nas grandezas de posição. Tirar o disco ou deixá-lo ≥ 1,5 u; títulos de coluna `MOVIMENTO EM LINHA` e `GIRO` do mesmo tamanho; cada linha angular nasce da linha linear (§5).

### T4 · E cada ponto do corpo? (PT4)
- **D20 T4-1:** `d/dt, COM r CONSTANTE` aparece como texto. Deve ser **conta**: o operador `d/dt` é escrito dos dois lados de `s = rθ`, o `r` sai para fora da derivada com um selo curto `r CONSTANTE` apontando para ele, e `ds/dt` vira `v_t`, `dθ/dt` vira `ω` (§5).
- **D21 T4-1:** o arco `s` é desenhado como círculo inteiro. Só o arco varrido.
- **S9 T4-2_60:** linha-guia de `282,7 rad/s` cruza a pá; `CÂMERA LENTA ×90` encostado na seta da ponta; `r₁ = 0,10 m` e `r₂ = 0,95 m` em lista com marcadores no rodapé, longe dos pontos; `0,10` órfão em alguns quadros. Rótulos r₁, r₂ presos aos pontos da pá (cota GEO do eixo ao ponto), `282,7 rad/s` no cubo sem linha-guia.
- **D22 T4-3_80:** metade direita vazia, só a frase `MESMA RAPIDEZ / VELOCIDADES OPOSTAS`. A conta `v = rω` com os dois pontos: `|v_A| = |v_B| = rω` e `v⃗_A = −v⃗_B` (o sinal saindo das setas).
- **D23 T4-4:** a seta verde `a_t` não aparece. Nascer na ponta da seta violeta, tangente, com o rótulo.
- **S10 T4-6_60:** `a_t`, `a_c` e `φ` amontoados na borda (setas curtas a < 0,3 u entre si). Inset de zoom (círculo com borda GEO, 2,5×) no ponto da borda com as duas setas e a soma; rótulos fora do inset.
- **D24 T4-6:** falta o fecho da hélice `PONTA: a_c = ω²r ≈ 7,6 × 10⁴ m/s² ≈ 7.750 g`. A hélice volta grande com a seta verde para o eixo na ponta.

### T5 · Para onde aponta um giro? (PT5)
- **D25 T5-1/T5-5/T5-6/T5-8:** disco 3D pintado de lavanda chapado, sem espessura visível nem material. Ver §7.2 (Three.js, aço com luz B).
- **D26 T5-1:** ícones do pião e da Terra minúsculos. ≥ 1,2 u cada, com o eixo e a seta ω⃗ violeta.
- **D27 T5-2_95 (leitura errada):** livros pequenos, câmera quase frontal; o livro da esquerda mostra a face de cima azul enquanto o rótulo diz `CAPA PARA BAIXO`: o espectador lê o contrário. Capa e contracapa com cores diferentes (capa com o logo, contracapa lisa escura), uma **seta normal à capa** (GEO, saindo dela) nos dois livros, câmera 3/4 por baixo e de lado, eixos x, y, z presentes. Os livros ocupam ≥ 55% do PALCO.
- **S11 T5-2:** sinal `≠` grande encostado nos livros. Entre os livros, com folga ≥ 0,3 u.
- **D28 T5-3:** o inset dos vetores (3 m leste + 4 m norte) aparece como retângulo sem setas legíveis e o texto é pequeno. Desenhar as duas ordens com setas GEO finas com ponta: a ordem A depois B e B depois A chegando no mesmo ponto, ponto final marcado.
- **D29 T5-4_30/75:** nas rodadas de 10°, 5° e 1° os livros parecem idênticos e a diferença não se vê. Sobrepor um **fantasma** do resultado de uma ordem sobre o outro livro, com o pequeno ângulo entre as setas normais marcado em âmbar (exagerado só no traço do arco, com o valor real escrito). Tabela que vai se preenchendo **na ordem da fala** (10°, depois 5°, depois 1°) com `÷4` entre 10° e 5°.
- **S12 T5-5:** a mão estilizada cobre o rótulo `ω⃗`. Mão do lado oposto ao rótulo; rótulo na ponta da seta.
- **S13 T5-6_72:** paralelogramo translúcido sai do disco (cunha flutuando à esquerda); `φ`, `O`, `r⊥` e `r⃗` amontoados. Paralelogramo entre ω⃗ e r⃗ de verdade (com O sobre o eixo), rótulos com lados escolhidos pelo teste de colisão.
- **D30 T5-6:** `sin` em vez de `sen`. Usar `\operatorname{sen}` em todo o vídeo.
- **D31 T5-6_82 (leitura errada):** com P na borda direita e câmera baixa, a seta `v⃗` sai **vertical** na tela, paralela a ω⃗: parece que v⃗ aponta ao longo do eixo. Escolher P na frente do disco (perto da câmera) para v⃗ ficar horizontal na tela, ou subir a câmera até o círculo de P aparecer bem aberto.
- **S14 T5-7:** `O` sobre `r⃗`.
- **S15 T5-8_85:** `a_t` sobre `a_c`; selos `ACELERA`/`FREIA` fora da faixa, encostados na seta; `EIXO FIXO` como selo extra.
- **C1 T5-8_85:** a seta `v⃗` sai pela borda esquerda do quadro (rótulo `v⃗` cortado). Escala da seta ou câmera.

### E1 · O ventilador que desliga (PE1)
- **S16 E1-1/E1-3:** rótulo `α` em cima de `300 RPM`. Seta α por dentro, rótulo do lado oposto.
- **S17 E1-1:** três selos ao mesmo tempo (CÂMERA LENTA, O QUE ESTE PEDE, HIPÓTESES). Um por vez; O QUE ESTE PEDE com no máximo uma linha (`PEDE: α E AS ACELERAÇÕES DA PONTA`).
- **D32 E1-3:** `Δθ = 471 rad / 75,0 VOLTAS / MOSTRADOR 0°` em lista no canto; `75,0` destoa da fala (75). Contador acumulado e mostrador presos ao ventilador, `75 VOLTAS`.
- **D33 E1-4:** a faixa de 0 a 10 s não se destaca no triângulo e o `5/9 DA ÁREA` não aparece. Faixa âmbar 100% sobre o triângulo a 45%.
- **S18 E1-5:** rótulos `a_t` e `a_c` sobrepostos; `v` sobre `r = 0,60 m`. Inset de zoom na ponta (como no T4-6).
- **S19 E1-6_80:** `CÂMERA LENTA ×30` e `FORA DE ESCALA` empilhados sobre a seta `v`; rótulo `v` solto no alto (RÓTULO SOLTO); `|a_t|` encostado no eixo `0,1`; `29,0 s` sobre a faixa verde. Um marcador só no canto do ESQUEMA; rótulos do gráfico com folga.
- **D34 E1-6:** DICA de 3 linhas apertada. Uma linha: `DICA: rpm → rad/s ANTES DE TUDO`; o sinal de α vai para a fala e a seta.

### E2 · A corrente da bicicleta (PE2)
- **C2 E2-2_90 e E2-5_85:** `r₂ = 4 cm` com o `r₂` **cortado pela catraca** (só aparece `₂ = 4 cm`). Rótulo fora da roda, com cota GEO até a catraca.
- **S20 E2-2:** `CATRACA` sobre os raios; `CORPO 1` sobre a seta de 60 RPM; `CORPO 2 / GIRAM JUNTAS AO PEDALAR` longe do corpo.
- **S21 E2-4:** seta α₂ risca `R = 35 cm`.
- **S22 E2-5_85:** `0,63 m/s` sobre `60 RPM`; `3,9 m/s²` sobre a seta; `9,9 m/s²` sobre os raios; setas pequenas. Inset de zoom na coroa e na catraca (dois círculos), cada um com o elo, a seta violeta 0,63 m/s e a seta verde a_c.
- **D35 E2:** selo HIPÓTESES de 3 linhas que fica na tela até o fim (G21: fica só até a primeira conta). Uma linha: `HIPÓTESES: CORRENTE NÃO ESTICA NEM ESCORREGA`; `PEDALANDO (RODA LIVRE ENGATADA)` vira rótulo no pedal.
- **D36 E2:** bicicleta plana e metade direita vazia até E2-5; cor 17,9%. Ver §6 e §7.3.
- **D37 E2-4:** `(PNEU SEM ESCORREGAR)` minúsculo. Rótulo ≥ 24 no contato do pneu com o chão.

### E3 · Quanto gira a Terra? (PE3)
- **C3 E3-2_75:** a órbita tracejada passa por cima do canto (título) e sai pela margem superior e esquerda. Desenhar só o **trecho** da órbita entre as duas posições da Terra, com o Sol dentro do PALCO.
- **D38 E3-2:** `ESTRELA MUITO DISTANTE` escrito ao lado do Sol (confunde: parece que o Sol é a estrela). A estrela fica na **borda do quadro**, com as duas direções paralelas para ela saindo das duas Terras e um marcador `→ ∞`.
- **S23 E3-2:** `≈ 1° (REAL)` sobre a seta; `FORA DE ESCALA` e `EXAGERADO` juntos (SELO DUPLO).
- **D39 E3-2:** falta `DIA SIDERAL ≈ 23 h 56 min`; à direita, `EM RELAÇÃO ÀS ESTRELAS` e `EM RELAÇÃO AO SOL` estão soltas (LINHA ÓRFÃ). Duas linhas completas: `EM RELAÇÃO ÀS ESTRELAS: DIA SIDERAL ≈ 23 h 56 min` e `EM RELAÇÃO AO SOL: DIA SOLAR MÉDIO = 24 h`, cada uma nascendo quando a estrela ou o Sol volta ao meridiano.
- **D40 E3-3:** `365,24/366,24` e `+1` embaixo da Terra; subscritos `sid`, `sol`, `ano` em `\text` cinza. Conta na `Pilha`; subscritos na cor da letra.
- **D41 E3-4_95:** Terra ocupando ~30% do PALCO; `λ` e `r⊥` minúsculos e sobrepostos; HIPÓTESES em 3 linhas. Terra ≥ 60% do PALCO, inset de zoom em São Paulo para `λ`, `r⊥` e `v⃗`; HIPÓTESES em uma linha (`HIPÓTESES: TERRA ESFÉRICA · REFERENCIAL SEM GIRAR COM ELA`).
- **D42 E3-5:** texto demais e nota pequena. A nota vira um selo de uma linha: `SÓ A ROTAÇÃO (NÃO É A VOLTA EM TORNO DO SOL)`.
- **S24 E3-6_90:** `PARA O EIXO (NÃO PARA O CENTRO)` cortado pelo eixo ω⃗; `a_c` sobre `r⊥`; fórmula da CONTA pequena (≈ 36 pt); CONFERE com fórmulas miúdas encostadas na borda. Rótulo fora da Terra; CONTA ≥ 46; CONFERE em duas linhas curtas com padding.

### Síntese e encerramento (PS-EN)
- **D43 S1_95:** disco à esquerda sem movimento útil e espaço morto. O disco gira com os três pontos e as setas violeta proporcionais enquanto os cartões entram.
- **D44 EN2:** cor 29,4%. Ponteiros com as setas curvas violeta cheias e o arco âmbar do ângulo entre eles.

---

## 5. MF-Tools por âncora (P0, usar e abusar)

Legenda: **V** = voa do desenho (`TransformFromCopy`); **GM** = `TransformByGlyphMap` (passo, cancelamento, termo atravessando o `=`); **TMT** = `TransformMatchingTex`; **E** = escrita em ordem (primitiva do §2). Toda linha é E; a tabela diz o que voa e o que é passo. Construir glyph maps só com o LaTeX estabilizado; `show_indices` só em desenvolvimento.

| Âncora | Linha(s) | Como construir |
|---|---|---|
| A3 | `a_c = v²/r` | `v` V da seta violeta, `r` V do raio; `a_c` V do rótulo da seta verde |
| T1-3 | `θ = s/r` → `θ = 2πr/r` → `θ = 2π` → `1 VOLTA = 2π rad` | `θ` V do arco, `s` V do arco âmbar, `r` V do raio; GM `s → 2πr` (o 2πr sai do arco da volta inteira); GM cancelamento de `r` com risco |
| T1-4 | `θ = s/r` → `s = rθ` | GM com o `r` **atravessando o `=`** (sai do denominador, pousa à esquerda do θ); depois a linha de graus: TMT de `s = rθ` → `s = rθ · π/180` e o fator `π/180` escrito com destaque |
| T1-5 | contador `Δθ` | TMT `2π → 4π → 6π`, no fim E `≈ 18,85 rad` |
| T2-1 | `ω_méd = Δθ/Δt` | `Δθ` V do arco entre duas cópias, `Δt` V do cronômetro |
| T2-2 | `ω_méd = Δθ/Δt` → `ω = lim_{Δt→0} Δθ/Δt` → `= dθ/dt` | GM (o `lim` entra antes da fração; `Δ → d` por glyph) |
| T2-4 | `1 RPM = 2π rad / 60 s` → `2.700 RPM → 2.700 · 2π/60 ≈ 282,7 rad/s` | `2.700` V do rótulo da hélice; `2π/60` V da linha de cima; resultado E, depois V até o cubo |
| T2-5 | `|ω| = 2πf = 2π/T` | `f` V do contador de voltas; GM `f → 1/T` |
| T3-1 | `α = dω/dt` → `= d²θ/dt²` | GM substituindo `ω` por `dθ/dt` |
| T3-3 | `ω = ω₀ + αt` | `ω₀` V do intercepto do gráfico, `α` V da inclinação acesa, `t` V do eixo |
| T3-4 | `Δθ = ∫₀ᵗ ω dt′` → `= ω₀t + ½αt²` → `θ = θ₀ + ω₀t + ½αt²` | integral E (símbolo → limites → integrando V da tirinha); `ω₀t` V do rótulo do retângulo, `½αt²` V do triângulo; GM `Δθ → θ − θ₀` e `θ₀` **atravessando o `=`** |
| T3-4 inset | `Δθ = 0 · GIRO TOTAL = 4π` | `+2π` e `−2π` V das áreas; GM soma com sinal → 0; soma dos módulos → 4π |
| T3-5 | `ω = ω₀ + αt` → `t = (ω − ω₀)/α` → (substitui) → `ω² = ω₀² + 2αΔθ`; trapézio: `Δθ = ½(ω₀ + ω)t` | GM isolando `t` (ω₀ e α atravessam o `=`); `t` V para dentro da linha do Δθ; resultado em caixa; no trapézio, `ω₀` e `ω` V das bases, `t` V da altura |
| T3-6 | 4 linhas da tabela | cada linha angular é GM **copiado** da linha linear (`x → θ`, `v → ω`, `a → α`, a linha 1D fica) |
| T4-1 | `s = rθ` → `d/dt(s) = r · d/dt(θ)` → `v_t = rω` | E do operador dos dois lados; GM `r` saindo da derivada; GM `ds/dt → v_t`, `dθ/dt → ω` |
| T4-2 | `v = rω` com números | `r` V das cotas (0,10 / 0,95), `ω` V do `282,7` do cubo; `× 3,6` GM para km/h |
| T4-4 | `v = rω` → `a_t = rα` | GM (`v → a_t`, `ω → α`) com `d/dt` como no T4-1 |
| T4-5 | `a_c = v²/r` → `(rω)²/r` → `r²ω²/r` → `ω²r` | GM substituição de `v`; GM cancelamento de um `r` com risco |
| T4-6 | `a = √(a_t² + a_c²)`; `tan φ = |a_t|/a_c`; hélice `a_c = ω²r ≈ …` | `a_t`, `a_c` V dos rótulos das setas; `φ` V do arco âmbar; na hélice `282,7` e `0,95` V |
| T5-3 | `A⃗ + B⃗ = B⃗ + A⃗` | `A⃗`, `B⃗` V das setas desenhadas; lado direito: GM **trocando de lugar** os dois termos |
| T5-4 | tabela `10° → 1,74°`, `5° → 0,44°`, `1° → 0,017°`; `dθ⃗₁ + dθ⃗₂ = dθ⃗₂ + dθ⃗₁` | cada valor V do medidor DIFERENÇA; `÷4` E entre as linhas 1 e 2; GM troca de lugar como no T5-3 |
| T5-5 | `ω⃗ = dθ⃗/dt`; `|ω⃗| = |ω|` | `ω⃗` V da seta; GM |
| T5-6 | `v⃗ = ω⃗ × r⃗` → `|v⃗| = ωr sen φ = ωr_⊥` | `ω⃗`, `r⃗` V das setas, `φ` V do arco; GM `r sen φ → r_⊥` (com o r⊥ do desenho piscando) |
| T5-8 | `α⃗ = dω⃗/dt`; `a⃗ = dv⃗/dt = d/dt(ω⃗ × r⃗) = α⃗ × r⃗ + ω⃗ × v⃗ = α⃗ × r⃗ + ω⃗ × (ω⃗ × r⃗)` | GM regra do produto (`d/dt` entra em cada fator); GM `v⃗ → ω⃗ × r⃗`; chaves E depois da linha; `a_t = αr_⊥` e `−ω²r⃗_⊥` V das chaves |
| E1-2 | `ω₀ = 300 · 2π/60 = 10π ≈ 31,4 rad/s`; `α = (0 − ω₀)/30 = −π/3 ≈ −1,05 rad/s²` | `300` V do rótulo, `30` V de `PARA EM 30 s`; `ω₀` V da linha de cima |
| E1-3 | `Δθ = ½ · 10π · 30 = 150π ≈ 471 rad` → `÷ 2π` → `75 VOLTAS` | `10π` V do eixo do gráfico, `30` V do eixo t; GM da divisão |
| E1-4 | `Δθ = 31,4 · 10 − ½ · 1,05 · 10² ≈ 262 rad ≈ 41,7 VOLTAS` | `31,4` e `1,05` V das linhas do E1-2, `10` V da faixa do gráfico |
| E1-5 | `v₀ = 0,60 · 31,4`, `a_c = 31,4² · 0,60`, `a_t = 0,60 · 1,05` | `0,60` V da cota, ω e α V das linhas de cima; uma linha por vez |
| E1-6 | `|a_t| > a_c ⟺ r|α| > ω²r ⟺ ω² < |α| ⟺ ω < 1,02` → `t > 29,0 s` | GM cancelamento do `r` com risco; GM isolando ω; `t` de `ω = ω₀ + αt` por GM |
| E2-3 | `v_c = ω₁r₁ = ω₂r₂` → `ω₂ = ω₁ · r₁/r₂ = 2,5 ω₁` → números | `r₁`, `r₂` V das cotas; GM com `r₂` **atravessando o `=`**; `2,5` E; `R` V da cota da roda |
| E2-4 | `α₁ = (3π − 2π)/4`, `α₂ = 2,5 α₁`, `a = α₂R`, `Δθ₁ = ½(2π + 3π)·4 = 10π` | `2,5` V da linha do E2-3; GM |
| E2-5 | `a_c = v²/r` (duas vezes) | `v` V da seta do elo, `r₁`/`r₂` V das cotas |
| E3-3 | `N_estrelas = N_sol + 1` → `÷ ano` → `1/T_sid = 1/T_sol + 1/T_ano` → `T_sid ≈ 86.164 s` → `ω = 2π/T_sid` | GM da divisão termo a termo; `86.400` V do rótulo do dia solar |
| E3-5 | `r_⊥ = R cos λ = 6.371 · cos 23,55° ≈ 5.840 km`; `v = ωR cos λ ≈ 426 m/s` | `λ` V do arco âmbar, `R` V da cota; `ω` V da linha do E3-3 |
| E3-6 | `a_c = ω²R cos λ ≈ 0,031 m/s² ≈ 0,32% DE g` | GM de `v = ωR cos λ` para `a_c = ω²R cos λ` |

---

## 6. Cor (P1)

- **Só cores de família contam** na métrica de tinta saturada: âmbar #FFC24D, violeta #9C8CFF, verde #3FE08B (+ ciano dos selos, que é da marca). O lavanda do disco do T5 sai (vira aço com luz B) e o T5 tem de continuar ≥ 30% com ω⃗, v⃗, α⃗, φ e o paralelogramo.
- **MathTex ≥ 50% colorida** (cor por token, inclusive números substituídos e subscritos: `ω_méd`, `T_sid` etc. herdam a cor da letra).
- **Abertura (20,4%):** ícones em cor de família e maiores; partícula com setas cheias.
- **T2 (29,2%):** setas violeta cheias no T2-3, arcos âmbar mais grossos, `282,7` violeta grande.
- **E2 (17,9%):** contorno de CORPO 1 e CORPO 2 em violeta 60% (é o mesmo ω de cada corpo), elos com a seta violeta, setas verdes de a_c nos insets, setas curvas violeta e verde nas rodas.
- **E3 (24,9%):** arco âmbar de 1° mais grosso, `ω⃗` violeta mais grosso, faixa âmbar do círculo de latitude, setas violeta para leste.
- **Encerramento (29,4%):** ver D44.

---

## 7. 3D (Three.js) e 2,5D no Manim (P1)

Divisão de papéis igual ao v1: Three.js dá o objeto e o fenômeno 3D; valores, rótulos, setas de sentido e contas são do Manim, presos pelo `timeline.json` (≤ 2 px).

### 7.1 Hélice (H1–H3, T2-4, T4-2, T4-6, S2)
- Pás com **torção** e perfil de aerofólio (corda maior perto do cubo, afinando para a ponta), spinner cônico, cubo com parafusos; material aço escovado PBR com luz B (key + rim) e reflexo suave; **faixa clara na ponta** de cada pá (como nas hélices reais), que marca visualmente o ponto que vai a 967 km/h.
- Câmera frontal ao disco da hélice (setas com o mesmo comprimento na tela), hélice centrada no PALCO com diâmetro ≈ 65% da altura do quadro.
- Rastros (D2) gerados no Three.js ou no Manim a partir do `timeline.json`, mesmo Δt para os dois pontos.

### 7.2 Disco 3D (T5-1, T5-5 a T5-8)
- Disco de aço com espessura visível (borda cilíndrica), chanfro leve, linha pintada âmbar na face de cima, pino central, sombra de contato suave num "chão" invisível. Câmera 3/4 com elevação ~30° (o círculo de P bem aberto).
- A transição do disco 2D (T4) para o 3D (T5-1) é contínua: o mesmo disco ganha volume e a câmera inclina (sem corte).

### 7.3 Livros (T5-2, T5-4)
- Livros grandes (≥ 55% do PALCO), capa com logo e cor viva, contracapa lisa escura, lombada de outra cor, páginas visíveis; **seta normal à capa**; câmera 3/4. Rotações com easing, uma de cada vez, nos dois lados ao mesmo tempo; hold 2 s no fim; fantasma de comparação no T5-4.

### 7.4 Terra (E3-1, E3-4, E3-6)
- Terra ≥ 60% do PALCO no E3-4/E3-6, textura com relevo suave, terminador dia/noite fraco, atmosfera fina; eixo de rotação como cilindro fino que atravessa a Terra (parte de trás oculta pela esfera); círculo de latitude de São Paulo como faixa âmbar sobre a superfície.

### 7.5 2,5D no Manim (todos os desenhos 2D)
- **Corpos de aço** (disco de referência, ventilador, coroa, catraca, roda, ícones): degradê radial com brilho deslocado para a luz B, borda clara (rim), sombra projetada suave (deslocada, 20–30% de opacidade), pino com highlight. Nada de forma chapada.
- **Ventilador (E1):** pás com degradê e leve perspectiva (visto de baixo), cubo com volume, motor no centro.
- **Bicicleta (E2):** coroa e catraca com dentes, raios finos, pneu com espessura e banda de rodagem, corrente com elos visíveis andando de verdade (os elos se movem com v_c).
- **Setas:** ponta afiada, leve glow da cor da grandeza (não borrado), espessura do G8.
- **Áreas:** preenchimento com opacidade e borda fina na cor cheia.
- **Insets de zoom** (T4-6, E1-5, E2-5, E3-4): círculo com borda GEO e linha fina até o ponto ampliado, escala escrita (`×3`).

---

## 8. Trechos parados e espaço morto (P1)

- **Coluna da direita vazia > 5 s** (exemplos vistos): T1-3, T4-3, T4-6, E2-2, E3-4 até a CONTA. Usar o tempo: o desenho centralizado e grande enquanto a coluna está vazia, deslizando para a esquerda quando a CONTA começa, ou a CONTA da âncora entrando junto com a fala correspondente.
- **Auditoria `PARADO`** com limiar de **3 s** (nenhum intervalo sem mudança de informação) e auditoria **COLUNA VAZIA** (região x > 0,6 u sem objeto por > 5 s). Meta 0.

---

## 9. Auditorias, render e entrega do v2

1. **G28** completo como no v1 (a cada 3 quadros dentro de cada `play` + estado final, Three.js pelas silhuetas), com o `qa.txt` classificado (§3). Meta 0 real.
2. **`ORDEM`** (§2 item 8), 0 falhas. **`algebra.txt`** com a contagem por âncora (§2 item 9), 0 linha por FadeIn.
3. **`MOSTRADOR`** (D9): `mostrador = Δθ mod 2π` em todo quadro do T1-5 e do E1-3.
4. **`PARADO`** 3 s e **`COLUNA VAZIA`** 5 s, 0.
5. **Caixa vazia:** falha se um contorno de caixa de resultado existir por > 0,3 s sem conteúdo.
6. **Tamanho do objeto principal** por âncora (55–75% do ESQUEMA) e tamanhos mínimos do G1.
7. **Cor por capítulo** só com cores de família (§6), ≥ 30% em todos; COR POR TOKEN (hoje 5 ocorrências) 0.
8. Manter as auditorias de física do v1 (todas OK) e o alinhamento 3D ≤ 2 px, agora também para a hélice, os livros e a Terra novos.
9. **Prancha humana** de 24 quadros de maior densidade **e** os mesmos 24 quadros de conferência do v1 (`H2_85`, `T1-3_60`, `T1-5_90`, `T2-3_70`, `T3-4_45`, `T3-4_97`, `T3-6_95`, `T4-2_60`, `T4-3_80`, `T4-6_60`, `T5-2_95`, `T5-4_30`, `T5-4_75`, `T5-6_72`, `T5-6_82`, `T5-8_85`, `E1-3_90`, `E1-6_80`, `E2-2_90`, `E2-5_85`, `E3-2_75`, `E3-4_95`, `E3-6_90`, `S1_95`) lado a lado v1 × v2. Mais uma **sequência de escrita** (10 fps) de 4 linhas: T3-4 (integral), T4-5 (cancelamento do r), T5-8 (regra do produto), E2-3 (r₂ atravessando o `=`).
10. Para cada item S/C/D do §4, declarar no relatório **corrigido / não corrigido / mudou de solução**, com o quadro conferido. O que não foi visto, dizer que não foi.
11. Render: preview 960×540 / 15 fps do vídeo inteiro (quase todos os capítulos mudam); zip `yt0020_v2_qa_pranchas.zip` com as pranchas por lote, a prancha humana, a comparação v1 × v2, as sequências de escrita, `qa.txt`, `algebra.txt` e `capitulos_v2.txt`.
12. **Relatório de entrega** (obrigatório): arquivos alterados, verificações com resultado (sem chamar falha de portão de "aviso menor"), caminho do preview e do zip, pendências reais. Parar sem iniciar voz, SRT, master nem entrega.

## 10. Ordem de trabalho

- **P0:** primitiva de escrita (§2) + `ORDEM`; tabela de MF-Tools (§5); peças de selo/rótulo/chamada/pilha (§3); todos os S e C do §4; D9 (mostrador), D27 e D31 (leituras erradas).
- **P1:** escala dos objetos (G3), Three.js novo (§7.1–7.4), 2,5D (§7.5), cor (§6), insets, trechos parados e colunas vazias (§8), demais D do §4.
- **P2:** auditorias e relatório (§9).
- Durante a iteração, renderizar só o lote alterado; no fechamento, o vídeo inteiro.

## 11. Decisões já tomadas (não reabrir)

Narração v1.1 congelada (~26:56 no v1); cores por família (ângulo âmbar #FFC24D, velocidade violeta #9C8CFF, aceleração verde #3FE08B, geometria GEO #B8C4DA, aço #7A8696 com luz B, painel #0E2A52); fundo azul do laboratório; 3D em Three.js (nunca Blender); `sen` em português; sem citar vídeos futuros; sem livros na tela; sem voz nem SRT nesta fase.
