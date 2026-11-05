# R1 (yt_0020) · Avaliação do preview v2 e HANDOFF v3 (2026-11-04)

Complementa os handoffs v1 e v2 (o que não é citado aqui continua valendo; narração v1.1 congelada, 26:56). Fase: preview visual silencioso 960×540 / 15 fps. Sem voz, SRT, master, entrega, commit nem push. Rodada de **acabamento**: não mexer no que já está certo. O v3 é candidato a **congelar o visual** (o Kaio quer ir para a narração depois): tudo da lista entra; se restar sobreposição, corte ou linha nascendo sobre outra, não declare fechado: reporte. Dizer item a item corrigido / não corrigido / mudou de solução, com o quadro conferido; o que não foi visto, dizer.

Mantido da v2 (não regredir): G28 0 real; ORDEM 0 falhas; 0 linha de equação por FadeIn; hélice com pás torcidas; livros 3/4; insets de zoom; E3-2 com estrela na borda e as duas linhas de referencial; mostrador = Δθ mod 2π; alinhamento 3D ≤ 0,57 px; capa para baixo/direita; v⃗ horizontal na tela.

## 2. REGRA DE COR DOS OPERADORES (P0) — JÁ IMPLEMENTADA NO `kit.py` (`_operadores_neutros`, chamada em `eqp`)
Só a grandeza leva cor; `d`, `dt`, `∫`, `lim`, `t`, `Δt`, `=`, `+`, barras, parênteses, expoentes numéricos ficam brancos. θ, Δθ, s, φ, λ âmbar; ω, ω₀, v, v_t violeta; α, a, a_t, a_c verde; r, R, r⊥, r₁, r₂ GEO; números substituídos na cor da grandeza. `Δθ` inteiro âmbar; `Δt` branco. `dθ/dt`: θ âmbar, `d`/`dt` brancos. Integral: Δθ âmbar, ∫, limites e `dt′` brancos, ω violeta. `ω` violeta com a mesma saturação em qualquer tamanho (sem pálido em frações/expoentes). O pós-passe do `eqp` já recolore por forma toda parte com d/∫/lim/\frac{\Delta; **se uma equação sua montar a MathTex por outro caminho (Mc, MathTex direto, lbl) e tiver d/dt/∫/lim, aplique a mesma regra**. Em `TransformByGlyphMap` o glifo neutro continua neutro durante o voo. Conferir: T2-2 (`dt` não pode ser violeta), T3-1, T3-4 (ω da integral igual aos outros), T4-1, T4-4, T5-5, T5-8, `m/s²` do eixo do gráfico do E1-6 (unidade branca), `t` dos eixos, `v₁`, `v₂` (subscrito herda a cor da letra), `ω_méd`, `T_sid`, `α₁`, `α₂`, rótulos `ω₂` da roda no E2.

## 3. Cor por capítulo (P1)
Alvo ≥ 30% pela métrica de família (qa20) **e** ≥ 30% pela métrica larga (qualquer tinta saturada). Aumentar cor de verdade, sem pintar aço, fundo ou tipografia neutra:
- E3 (8,4%): arco âmbar de 1° mais grosso e maior; ω⃗ violeta grosso; faixa âmbar da latitude mais larga; v⃗ violeta; λ âmbar maior.
- T5 (12,5%): ω⃗, v⃗, α⃗, φ e paralelogramo mais cheios; livros: seta normal à capa em GEO e fantasma do resultado em âmbar; disco 3D de aço (não lilás).
- E2 (17,3%): contornos de CORPO 1/2 em violeta 60%, setas curvas violeta e verde nas rodas, elos com seta violeta.
- Hook, Abertura, T1, T2, T4: setas e arcos na espessura do G8 e cor cheia, números grandes em cor; arco âmbar θ mais grosso no T1; 282,7 rad/s violeta grande.
- Resumo e E1: bordas dos cartões e caixas na cor da família (2–3 pontos).

## 4. Espaço, escala, colunas vazias (P1)
- COLUNA VAZIA (meta 0): T1-1 0–5,7 s; T2-1 0–8,3, T2-3 32,5–39,3, T2-4 54,0–59,7; T3-2 15,1–25,1, T3-3 35,5–45,3; T4-1 0–5,3, T4-3 86,5–92,5; E2-1 0–5,3, E2-5 137,3–145,1. Ou a CONTA/enunciado/equação de partida entra mais cedo, ou o desenho nasce grande e centrado e só desliza quando a coluna for ocupada. T3-2/T3-3: antecipar a legenda da regra (`MESMO SINAL ⇒ MAIS RÁPIDO`) e a reta `ω = ω₀` já escrita.
- TAMANHO (55–75% do ESQUEMA): disco do T3 35% (T3-1, T3-2), disco do T4 38% (22% no T4-6), hélice PH 52% da altura (pedido 65%), PT4 47%, PS 49%. T3-2: três discos ≥ 1,6 u usando a largura toda. T3-3: disco ≥ 1,5 u ao lado do gráfico. Hélice do PH D ≈ 65% da altura. T4-1…T4-5: disco no tamanho do T1/T2 (59%). Envelopes < 55%: T3-1 53, T4-1 47, T4-3 54, T4-4 51, T4-5 48.

## 5. Defeitos pontuais (corrigir)
1. **E1-5 (25%):** `0,60` duplicado sobre `r = 0,60 m` (cópia do voo sobre o original, G14). O `0,60` sai do rótulo, o rótulo original fica 40% enquanto o número voa, sem sobreposição.
2. **E1-6 (70%):** linha `⟺ ω < 1,02 rad/s` / `ω = ω₀ + αt` / `⟹ t …` cortada na borda direita; a última (`⟹ t > 29,0 s`) não aparece. Garantir que a CONTA cabe (duas linhas alinhadas pelo `⟺`). `|a_t|` e `a_c` do gráfico com `m/s²` sobre `a_c`: afastar.
3. **E1-1:** `r = 0,60 m` embaixo da hélice, longe do raio; cota GEO do eixo à ponta da pá.
4. **E1-3 (25%):** `Δθ = 341 rad` / `54,2 VOLTAS`: o mostrador acompanha o contador sem salto e sem trocar de fonte.
5. **T3-4 (70%):** gráfico do inset ω(t) sem preenchimento âmbar nem `+2π`/`−2π`; garantir área de cima (âmbar 45%) e de baixo (âmbar 45% com hachura) preenchidas e rotuladas enquanto o disco vai e volta; caixa do resultado entra junto do conteúdo.
6. **T4-6 (70%):** hélice com seta verde minúscula e coluna vazia: entrar com `PONTA: a_c = ω²r ≈ 7,6 × 10⁴ m/s² ≈ 7.750 g` (282,7 e 0,95 voando da hélice), seta verde de a_c com comprimento do G8, hélice maior.
7. **T4-6 (25%):** `φ` e `a_c` colados por baixo do inset: ≥ 0,15 u entre rótulos; `a` fora do inset.
8. **T4-2:** coluna com 5 linhas no mesmo bloco; `O MESMO ω · SETAS ∝ r` + `v = rω` uma só chamada curta; contas saem dos rótulos `r₁ = 0,10 m` e `r₂ = 0,95 m` (≥ 36, GEO cheio, não 60%).
9. **T5-3:** `VETORES: A⃗ + B⃗ = B⃗ + A⃗` e `GIROS FINITOS:` sem continuação (rótulo órfão): completar `(A, DEPOIS B) ≠ (B, DEPOIS A)` e o selo `GIRO FINITO NÃO SE SOMA COMO VETOR`; inset dos vetores com rótulos (`N`, `4 m`, `3 m`) ≥ 24.
10. **T5-5:** mão vira borrão sobre o eixo: silhueta nítida (dedos curvados no sentido do giro, polegar ao longo de ω⃗, contorno GEO, preenchimento ≥ 60%); `MÃO DIREITA` fora da silhueta.
11. **T5-1…T5-8:** disco 3D lilás-acinzentado e claro: baixar o brilho da face de cima, mais contraste no aro e na linha pintada âmbar.
12. **T5-6/T5-7:** `O` e `r⃗` com caixinha cinza escura atrás: rótulo sem fundo e linha-guia curta.
13. **T5-8:** `a⃗_c` e `a⃗_t` verdes sem a seta correspondente visível; `FORA DE ESCALA` encostado no limite; a nota `EIXO FIXO` some.
14. **T2-4/T4-2/PS:** `282,7` dentro do cubo: só ≥ 36 e legível sobre o aço; senão ao lado do cubo com linha-guia curta.
15. **PE3:** `EXAGERADO` único encostado no rodapé; Terra do E3-2 minúscula (≈ 0,5 u) e órbita sem Sol no palco: Terra ≥ 1,1 u, Sol maior; `≈ 1° (REAL)` do mesmo tamanho dos outros rótulos.
16. **PE2:** `PEDALANDO (RODA LIVRE ENGATADA)` solto: ancorar no pedal com linha-guia. `r₂ = 4 cm` do rodapé cota a catraca por traço longo: aproximar. Insets do E2-5 (`×3`) com `0,63 m/s` e `3,9 m/s²` na mesma linha: duas linhas (v violeta, a verde).
17. **PA e PH:** conferir A2/A3 (ícones ≥ 1,2 u) e a barra do som com a marca 78%.

## 6. Auditorias a fechar (qa20, feito por outro agente) — mas cada lote deve **registrar** o que for preciso
PRODUTO VETORIAL T5-8: registrar `a3d` e medir `a⃗ = α⃗×r⃗ + ω⃗×(ω⃗×r⃗)` (erro ≤ 1%). CAIXA VAZIA: estender às caixas por `passo`/`pg`/FadeIn. COR POR TOKEN: registrar partes das 3 MathTex sem partes (PT3 ×2, PE1 ×1). E1-5: medir `a_c : a_t` do inset. COR OPERADOR nova (glifos d, dt, ∫, lim, t com cor ≠ neutra = falha). G28: marcar o degradê de `disco_aco` como `fundo_de_objeto`; rótulo `θ` do T4-1 (4,1–4,5 s) do lado de fora do arco (hoje cruza raio e pontos).

## 7. Animação e álgebra
Manter a primitiva de escrita. v2: 67 esc, 69 esc+voo, 44 passo, só 2 tmt. **Usar e abusar de `TransformMatchingTex`** onde a expressão se repete e a correspondência é clara: T3-1 (`α = dω/dt → d²θ/dt²`), T3-5 (`ω² = ω₀² + 2αΔθ`), T4-1/T4-4 (`dv_t/dt`), T5-4 (`dθ⃗₁ + dθ⃗₂`), E1-4 (`Δθ = 31,4·10 − ½ …`), E3-3 (`1/T_sid`). Meta ≥ 10 usos no vídeo; `passo` (GlyphMap) onde o termo atravessa o `=` ou cancela. `fade-texto` só para enunciado/nota/selo.

## 9. P0 de álgebra (linhas nascendo sobre a linha-mãe)
1. **T5-8 (216,3–217,8 s, regra do produto):** `= α⃗×r⃗ + ω⃗×v⃗` nasce em cima de `= d/dt(ω⃗×r⃗)` (217,26–217,66 s: `=` e `×` sobre o `d/dt`; ω⃗ voa por cima do r⃗ da linha de cima). Regra 4 do v2 §2.4: a linha nova nasce já na vaga de baixo, os glifos mapeados viajam em arco e o ω⃗ só pousa depois que o r⃗ da linha-mãe saiu.
2. **E2-3 (62,9–63,5 s):** `ω₂ = ω₁ r₁/r₂` nasce sobre `v_c = ω₁r₁ = ω₂r₂`; `r₁`,`r₂` flutuam sobre `ω₁`. Nascer embaixo; `r₂` atravessa o `=` por arco sem cruzar texto. `r₁`/`r₂` da fração em GEO cheio (#B8C4DA 100%).
3. **T4-5 (146,3–146,7 s):** `r²` pisca em negrito duplicado ~0,4 s antes do risco (cópia sobre o original, G14): uma cópia só.

## 11. Adendo por lote
**PT1:** T1-1: coluna vazia 5,7 s; selo `CORPO RÍGIDO: DISTÂNCIAS FIXAS` desde o começo e a cota `20 cm` na primeira fala. T1-2: trajetórias finas (≈15%) sobem para 40%; selo `TODOS OS PONTOS: MESMO ÂNGULO` quando o θ nasce. T1-3: `θ = s/r` e `s₁/r₁ = s₂/r₂ = s₃/r₃ = 1,0 rad` em duas linhas coladas: folga ≥ 0,25 u; selo `ÂNGULO EM RADIANOS: ARCO ÷ RAIO` em duas linhas com padding (G1). T1-4: `EM GRAUS: s = rθ · π/180` com `π/180` dentro de caixa retangular e `SOBRA` colado: caixa só no fator, folga 0,12 u; `SOBRA` selo separado abaixo apontando para o fator; `EM GRAUS:` em branco. T1-5: contador três vezes (`Δθ = 18,85 rad`, `VOLTA A VOLTA: 6π`, `Δθ = 6π ≈ 18,85 rad`): deixar só `Δθ = 6π ≈ 18,85 rad`; ícones `+`/`−` com setas ≥ 1,0 u; mostrador estourado (cinza quase branco): fundo azul de painel e ponteiro âmbar.
**PT2:** T2-1: retas cinza atravessando o disco (diâmetros inteiros): só o raio pintado com opacidade decrescente, estilo do T2-2. T2-2: `dt` violeta (regra de cor); CONTA ok. T2-3: arcos âmbar concêntricos e setas violeta parecem fantasmas: arcos grossos (≥ 6), setas cheias; selo `MESMO ω PARA O CORPO TODO` sozinho (coluna vazia 6,9 s): trazer `ω = Δθ/Δt` com `ω` voando do selo. T2-4: hélice pequena (≈ 1,5 u): ≥ 55% do ESQUEMA, `2.700 RPM` no cubo; `CÂMERA LENTA ×90` padronizado. T2-5: anel do cronômetro com quatro rótulos `4,0 s` encostados (`VOLTA ATUAL`); cronômetro maior, um rótulo por segmento com folga; selo `ATENÇÃO SÓ COM GIRO UNIFORME · f > 0 MESMO NO GIRO HORÁRIO` em duas linhas com padding (G1).
**PH:** H1 (0–13 s): hélice só ~35% da altura à esquerda, metade direita vazia: centrada e maior (D ≈ 65% da altura) até a coluna entrar em H2; setas violeta só em H2, nascendo 0,2 s tarde. H2: `NÚMEROS TÍPICOS` entra sozinho 3–4 s antes dos números: junto do primeiro número. H3: a pergunta `POR QUE A PONTA DA HÉLICE CHEGA A QUASE 1.000 km/h?` no mesmo tamanho dos números: frase-chave (≥ 30, maior que os números) e números recuam a 60% quando ela entra.
**PA:** A2 ícones ≈ 1,0 u → ≥ 1,4 u; `NESTE VÍDEO:` ciano pequeno; terceiro ícone (disco + duas setas) maior (setas 40% do ícone). A3: partícula ≈ 0,4 u pequena e a CONTA `a_c = v²/r` só a 55% (metade direita vazia ~8 s): CONTA entra com a primeira fala (`v` voa da seta violeta, `r` do raio); círculos concêntricos terminam com partículas nítidas.

## 8. Entrega (cada lote)
Render só do lote; `[tempo] total` igual ao atual; G28 0 real; relatório item a item com quadro conferido.
