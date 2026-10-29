# HANDOFF v6 — yt_0015 "Momento linear e impulso" (fechamento de tela antes da narração)

(cópia do handoff colado pelo Kaio em 2026-10-28; tempos m:ss são do preview v5 18:16)

Última rodada só de tela. Física e números não mudam. Narração v4 muda só a 1ª frase do T3-3:
"Agora assista à mesma colisão com uma câmera que anda junto com o carrinho da esquerda."
Fora: voz, SRT, master, entrega, commit, push. Não alterar template/, docs/, assets/, experimentos/threejs/.
Entrega: preview silencioso v6 960×540/15; zip v6_para_gpt.zip (preview, quadros_5fps/, stills).

Pedido do Kaio (v5): "Em 4:33 a representação está muito feia. A explosão acontece e não faz nada nos blocos; depois aparece um
carrinho olhando. Como assim? É carro ou bloco? ... Melhor melhorar no Manim, se ele conseguir; se não, volte para o 3D."

## 1. Regras gerais
- G1 troca de header: linha de cima parada; só a linha do capítulo (e selo) troca: FadeOut 0,3 s, depois FadeIn 0,3 s; nunca
  juntos. Nos cortes, conteúdo antigo sai antes do novo entrar. (casos: 3:16, 14:16)
- G2 escrita completa: toda expressão termina ≥ 1,0 s antes de FadeOut/transição; sem glifo isolado parado (2:28, 10:32 `0.`,
  11:16 `v.`, 12:36 `−` e `↖`, 16:40 `∘`, 17:12 `N ≈ 9,`). Write longo → Writes menores termo a termo.
- G3 transformações sem fantasma (1:36, 2:40, 6:00, 9:36, 13:16): TransformByGlyphMap com mapa explícito ou FadeOut→FadeIn; QA órfãos.
- G4 texto ≥ 24 px de versal em 1080p (≈12 px no 540p); legenda final com opacidade ≥ 0,85. Lista: 2:20 CÓPIA DE v⃗ NA ORIGEM;
  3:12 ESSE CASO FICA…; 5:42 Δp⃗; 6:24 legenda da mesa; 6:36 FORA DE ESCALA, REAÇÃO DO PESO, −P⃗; 8:16 CENTÉSIMOS DE SEGUNDO;
  8:24 RETÂNGULOS 4; 8:44 Δt_k → 0; 9:16 MESMA BASE, MESMA ÁREA; 9:36 Jx Jy; 13:36 MESMO TEMPO PARA PARAR; 13:44 d e 5d;
  13:52 MESMO VENTO, MESMA DISTÂNCIA; 16:20 FORÇA NO CHÃO + PESO = ?; 18:04 ?, F⃗, −F⃗ do cavalo.
- G5 nada parado > 6 s sem motivo. Nos exercícios o esquema "responde": termo escrito pulsa/acende no desenho.

## 2. T3 — POR QUE MASSA VEZES VELOCIDADE? (refazer inteiro)
Erros v5 (4:22–5:48): trilho vazio; blocos colados parados ~12 s; explosão não mexe os blocos; reaparecem separados sem continuidade;
ícone de automóvel "VISÃO DO CARRO"; fundo não corre; trilho pequeno no topo com rótulos minúsculos; halo radial atrás do trilho.
Decisão: Manim 2D, vista lateral, grande. 4 stills de teste antes do lote; se critério falhar após 1 ajuste → Three.js (trilho 3D do v3)
sem pedir. Reportar caminho.
Objetos:
- Trilho de ar: viga #7A8696 com furinhos; 90% da largura; faixa vertical 15%–55% da altura (T3-4: 12%–45%); régua a cada 0,5,
  finas, DIM #8FA3C4 (correm no T3-3). Sem halo.
- Carrinho: U invertido abraçando a viga ~1,4×0,7, #B8C4DA contorno #7A8696, bandeirola fina; letra A/B ≥ 36 px; massa (m, 2m, 3m)
  embaixo, fora. Nunca "bloco" nem carro de rua: sempre "carrinho". 2m = dobro do comprimento (dois corpos com emenda), 3m triplo.
- Velcro: faixa laranja curta na frente nas colisões que grudam; ao grudar se fundem.
- Explosão: mola comprimida entre A e B com trava (linha fina); trava queima com flash laranja 0,2 s; mola estica e empurra; mola cai/some 0,3 s.
- Setas de velocidade violeta #9C8CFF, no centro, um pouco acima; v = 1,0 unidade; rótulo ≥ 28 px ao lado da ponta. v = 0: `v = 0` embaixo, sem seta.
- Estroboscópio: fantasmas a cada 0,5 s (opacidade 0,25) em T3-1 e T3-2.
Storyboard (sem quadro de trilho vazio):
- T3-1 (≈12 s): trilho entra com A e B juntos no centro, mola + trava; legenda DOIS CARRINHOS IGUAIS · PARADOS; após 1,5 s trava
  queima, mola estica, andam no mesmo quadro; setas coladas andam junto; fantasmas espelhados; param a ~0,5 das pontas (batente);
  legenda MESMO EMPURRÃO, MESMA VELOCIDADE; fantasmas somem 0,4 s.
- T3-2 (≈10 s): voltam um contra o outro com v e v, velcro na frente; batem no centro, grudam (flash), param; setas encolhem; v = 0;
  legenda IGUAIS E OPOSTOS: O CONJUNTO PARA; separam (velcro solta com traço) e voltam às posições do T3-3 em 1 s, sem setas.
- T3-3 (≈16 s): duas faixas horizontais, cada uma com trilho inteiro 90%: cima VISTA DO CHÃO; baixo VISTA DE QUEM ANDA JUNTO COM A.
  Rótulo de referencial pequeno à esquerda, DIM, ≥ 24 px. Baixo: ícone de câmera de vídeo sobre A; régua bem visível. Mesma colisão
  ao mesmo tempo: cima A→v, B←v, grudam, v = 0. Baixo: A parado centro-esquerda (v = 0, câmera); régua e trilho deslizam p/ esquerda
  com v, seta DIM `chão: v ←`; B chega com 2v (seta dobro); grudam; conjunto sai p/ esquerda com v. Contato em câmera lenta 0,5×,
  faixas alinhadas, tracejado fino ligando os contatos. Tarja MESMA COLISÃO · OUTRO REFERENCIAL. Sinais: rótulos 2v e v sem negativo.
- T3-4 (≈20 s): faixa de cima some (0,4 s); a de baixo sobe para 12%–45% e a colisão 2v→0 roda em loop lento; conta grande embaixo
  nasce dos rótulos (m, 2v, 0, 2m, v voam) `m·2v + m·0 = 2m·v`; casos com massas diferentes (mesmos números do v5): par antigo sai pela
  direita enquanto o novo entra pela esquerda em movimento; conta anterior sobe e encolhe 70% (histórico ≤ 2 linhas); rótulos ≥ 28 px.
  Proibido trilho vazio e "só conta no canto".
- T3-5 (≈8 s): carrinho A entra no lugar do "bloco" com v⃗ e p⃗; selos DA SEGUNDA LEI e DA SIMETRIA convergem para um p⃗ = m v⃗ sem cópia; sem header sobreposto ao T4.
Stills de teste 1920×1080: T3-1_explosao_inicio (mola esticando, carrinhos a 0,3 do centro); T3-1_estrobo; T3-3_split (contato);
T3-4_conta. Critérios: carrinho ≥ 120 px; A/B ≥ 36 px; rótulos ≥ 28 px; folga ≥ 0,15; trilho ≥ 85%; prova da régua que corre (2
quadros a 0,5 s); nenhum quadro do T3 com trilho sem carrinho.

## 3. Correções pontuais (tempos v5)
T1: 0:44–0:56 cartão do título parado 12 s → 4 s; 8 s vão para A3 com miniaturas de colisões entrando uma a uma com P⃗ᵢ = P⃗_f.
1:12–1:20 SEGUNDA LEI sozinho → partícula e curva entram junto com o selo. 1:36 fantasma md v⃗/dt dobrado (ΣF = m a → m dv/dt) → glyph
map a⃗→dv⃗/dt. 2:20 G4. 2:28 px = m vx glifo deslocado → termo a termo. 2:40 resíduo à direita de ΣF = dp/dt. 2:44–2:56 painel das
barras ≥ 30% da altura útil; barras ≥ 0,35; rótulos px py pz ≥ 28 px embaixo de cada barra, folga ≥ 0,25. 3:12 G4.
T2: 3:16 dois headers + colchão vazio → G1; discos entram junto com o header.
T4: 5:42 Δp⃗ apagados G4. 5:52 Δt duplicado sob o cronômetro → um só. 6:00 Δ em negrito na transformação G3. 6:24 seta P⃗ entra com a
mesa; legenda G4. 6:36 −P⃗ encostado na seta, dentro da Terra, ≥ 28 px; FORA DE ESCALA ≥ 24 px embaixo da Terra.
T5: 7:04 eixos se desenham enquanto o bloco anda. 7:28 voos p₂−p₁ e t₂−t₁ em sequência sem cruzar. 9:04 caixa da conta corta eixo t
→ folga ≥ 0,25. 9:12 manter FORÇA DA PAREDE e bola FadeOut 0,4 s antes da troca. 9:16 G4; F_méd fora do retângulo à direita com
linha guia. 9:32 fantasmas p₁/p₂ e risco diagonal na origem → plano xy limpo. 9:36 dt duplicado em Jx = ∫ΣFx dt G3. 9:36–9:52 Δp = J
fora do triângulo, lado da hipotenusa, folga ≥ 0,15.
E1: 10:08–10:22 dados acendem no desenho. 10:24 pᵢ (←12) em cima, p_f (→8) abaixo, Δp (→20) embaixo da ponta de pᵢ à ponta de p_f com
tracejados verticais. 10:32 `0.` solto; risco reto só sobre 0,40(20 − 30) = −4 N·s. 10:48 mg à esquerda da seta do peso (ou esmaecer
DEPOIS). 10:56 |Δp|: 12 → 20 kg·m/s completo e parado ≥ 1 s.
E2: 11:00 bola já com seta 20 m/s. 11:06–11:28 21,2 acende nos catetos, Jx e Jy nascem dos catetos. 11:32 esquema já no tamanho final
desde 11:00; triângulo no espaço reservado. 11:44 `F_méd ∦ v_f` ou `F_méd ∥ Δp , não ∥ v_f`. 11:36–11:49 F_méd desliza sobre Δp.
E3: foguete fora do gráfico (coluna própria à esquerda, gráfico no meio, conta à direita); jato cresce com F(t) em sincronia com o
ponto na curva; ponto anda até (1,25 s; 781,25 N); rótulo à direita do ponto, folga ≥ 0,15 do eixo; 12:36 − e ↖ soltos, J ≈ 5,81×10³ meio escrito.
T6: 13:04 caixa × d vazia → entram juntas ou só quando usada. 13:16 três linhas K = ½mv² → v = p/m → K = p²/(2m) com glyph map.
13:20 bolas já andam. 14:08 F_res Δt = Δp entra com Write normal na coluna da conta. 14:16 G1.
E4: 14:17–14:30 parado no muro 3D → queda roda (v = √(2gh) nasce do h) ou clipe do hook em loop. 14:32–16:04 coluna esquerda com 2
miniaturas PERNAS DURAS / JOELHOS (~25% largura) a cena inteira; gráfico no meio, conta à direita; miniatura acende quando a conta fala
dela. 15:52 tabela com ícones (raquete, bola, carro contra muro).
E5: 16:08 `m = 2 mg (miligramas)` e na conta `m = 2 × 10⁻⁶ kg`. 16:20 G4. 16:40 ∘ solto; mv· meio escrito. 17:12 pulga sai, depois
pessoa e bloco 35 t entram, depois a conta.
Resumo/CTA: opcional 3 miniaturas que acendem; 17:27 parado 6 s; 18:00 `?` ≥ 48 px acima da cabeça do cavalo; F⃗/−F⃗ ≥ 28 px.

## 4. Parados medidos no v5 (dif. < 0,3 por 1 s)
1:53 (6) · 4:23 (10) · 7:12 (6) · 9:39 (6) · 10:08 (14) · 11:06 (15) · 11:22 (6) · 11:36 (13) · 12:03 (9) · 12:30 (6) · 12:44 (6) ·
13:20 (6) · 14:01 (6) · 14:17 (13) · 15:02 (8) · 15:11 (6) · 15:43 (7) · 17:27 (6).
Meta v6: zero > 8 s; no máximo 4 entre 6 e 8 s (resumo, CTA, fechamento de exercício).

## 5. QA
1 órfãos zero; 2 sobreposição folga ≥ 0,15 rótulos / ≥ 0,25 blocos (pior por capítulo); 3 legibilidade (24 px, opac ≥ 0,85);
4 escrita completa (último quadro do Write vs quadro antes da saída); 5 headers (nenhum quadro com 2 títulos); 6 parado na meta;
7 T3 stills + prova da régua. Stills 1920×1080: 4 do T3, T1-6, E1 (Δp 3 linhas), E2 (∦), E3 (foguete fora), E4 (miniaturas),
T6 (3 linhas), E5 (2 mg (miligramas)).

## 6. Relatório
arquivos alterados; lotes; caminho T3 e por quê; QA 1–7 com pior caso; frase trocada; duração; caminhos; pendências. Sem commit/push.
Não começar narração.
