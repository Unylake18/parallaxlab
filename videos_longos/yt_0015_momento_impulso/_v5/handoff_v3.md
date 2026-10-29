# HANDOFF v3 — yt_0015 "Momento linear e impulso" (preview silencioso v3, polimento visual)

Física, números, textos de tela e narração **não mudam** em relação ao v2 (`narracao_sugestao.md` = narração v3 congelada).
Esta rodada é **só tela**: disposição, construção, animação e três peças ilustradas (cavalo, mãos, pulga).

## 0. Contexto
- O Kaio avaliou o v2: disposição em tela, construção e animação precisam melhorar; o cavalo do CTA está muito ruim. Conteúdo aprovado.
- Sem voz, SRT, master, entrega, commit ou push. Não alterar `template/`, `docs/`, `assets/`, `experimentos/threejs/`.
- Rodada: preview silencioso v3 960×540 / 15 fps, completo, mais os stills da §7.

## 1. Diagnóstico do v2
Bom e fica: header + selo; tabela do T1; Riemann do T5; E3 com área; painéis do E4; DICA; resumo; manequim 3D.
Problemas: (1) metade da tela vazia (T4, E1-3, E2, vetor J, T5 parede pequena, cartões das colisões, título e "MAIS TEMPO…"
descentralizados); (2) painéis vazios antes do conteúdo (T6, E5, E4); (3) contraste baixo (mesa do T3, barcos do T6, selo DIM 0,6
sobre 3D); (4) sobreposições (rótulo (1,25 s; 781,25 N), Δp⃗ e p⃗_f na ponta, F⃗_méd cruzando o triângulo, F⃗ e 2m nos barcos,
"COM m CONSTANTE" colado no dt, faixa mg sobre o eixo, N = F_res + mg colado em "PERNAS DURAS", foguete no logo); (5) gráficos F_res(t)
do E4 e RESUMO fora de escala (pernas duras deve ser 14× mais estreito e alto: 56.000 N em 0,01 s; joelhos pico ~5.900 N em 0,143 s);
(6) 3D e 2D sem costura (T2 corta de 3D para 2D; manequim no topo estoura o quadro; H3 com escalas diferentes; 860 s boneco 2D);
(7) peças fracas (cavalo, mãos, pulga); (8) pausas mortas de 10–13 s: 47–57, 205–217, 491–504, 582–595, 622–633, 637–649, 680–693,
766–777 s; (9) "2.5 m" com vírgula; chiclete vermelho sem rótulo.

## 2. Grade de layout (todas as cenas 2D)
| Zona | Região | Uso |
|---|---|---|
| HEADER | y > 2,75, x < 3,5 | header 2 linhas + selo |
| LOGO | canto sup. direito | nada a menos de 0,4 |
| PALCO | x ∈ [−6,6; 0,6], y ∈ [−3,0; 2,5] | figura, gráfico, objeto físico |
| CONTA | x ∈ [1,0; 6,6], y ∈ [−3,0; 2,5] | dados (topo), álgebra (meio), resultado (baixo), em coluna, à esquerda |
| CENTRO | centro da tela, largura ≤ 9 | uma ideia só |
| DOIS PAINÉIS | 2 × largura 6,2, vão 0,4, centrados, topo y = 2,3 | comparação lado a lado |
| LEGENDA | y ∈ [−3,7; −3,1], centrada | frase curta de fechamento |
| DICA | canto inf. direito, largura ≤ 4,2 | com DICA ativa, LEGENDA em x < 2 |
Regras: toda cena em PALCO + CONTA, CENTRO ou DOIS PAINÉIS; objeto sozinho = CENTRO com ≥ 35% da largura; zona vazia > 6 s não pode;
centralizar pela tela inteira; folga ≥ 0,25; rótulos fora da linha; painel entra com o primeiro conteúdo; selo DIM 0,85; sobre 3D,
faixa #050816 a 0,55 atrás do header.

## 3. Construção e animação
Equação: Write ou TransformMatchingTex (nunca FadeIn de equação derivada). Gráfico: eixos Create → rótulos → curva Create → área da
esquerda para a direita. Vetor: GrowArrow do ponto de aplicação, rótulo depois. Resultado: caixa/sublinhado Create + Indicate; E4 e E5
piscam nos dois painéis juntos. Pausas longas: realces (Indicate, sublinhado, opacidade 0,4 do que já foi dito). Transição 0,4 s.
Movimento com smooth ou física real.

## 4. Correções por bloco
Hook: câmera recua (≤ 70% da altura, 0,8 de folga abaixo do header), `2,5 m`; H3 dois cenários idênticos e espelhados lado a lado,
rótulos na mesma linha de base centrados sob cada muro, manequim ≥ 35% da altura do muro na tela; aço menos cromado (metalness ~0,4,
roughness ~0,45); pergunta centrada.
A1–A3: cartões das colisões e título centrados na tela, cartões maiores.
T1: chiclete cinza claro com rótulo CHICLETE.
T2: trilho 3D no T2 inteiro (perspectiva → lateral), rótulos m, v⃗, 2m presos aos carrinhos; VISÃO DO CARRO no PALCO; as três equações
do fim em coluna no CENTRO, alinhadas pelo =, ANTES = DEPOIS como LEGENDA; p⃗ = m v⃗ com bloco maior no PALCO e textos na CONTA.
T3: discos e cadeia numa composição só, "O QUE UM GANHA, O OUTRO PERDE" como LEGENDA; mesa/bloco em aço com borda GEO, P⃗ e N⃗ azuis,
Terra como arco grande na base com a reação no centro, frase como LEGENDA; cargas: v violeta, F azul, rótulos fora, desigualdade na
CONTA, retângulo do campo como LEGENDA.
T4: CENTRO; = m a⃗ por TransformMatchingTex, COM m CONSTANTE embaixo; A FORMA DE NEWTON como LEGENDA; REFERENCIAL INERCIAL centrado abaixo.
T5: parede e bola maiores no PALCO (60% da altura), gráfico na CONTA; contador RETÂNGULOS no canto do gráfico; Σ na CONTA virando ∫
por TransformMatchingTex; cancelamento do dt no CENTRO grande, risco com Create e os dois dt saindo juntos; J⃗ no CENTRO, vetor ≥ 5 u,
rótulo J⃗ = ∫F⃗_res dt e MESMA DIREÇÃO DE Δp⃗.
E1: antes/depois maior no PALCO, dados na CONTA; F⃗ sai do ponto de contato; mg = 3,9 N ≥ 24; conta F_méd na CONTA alinhada; +x curto.
E2: triângulo maior no PALCO; F⃗_méd paralela a Δp⃗ deslocada para fora; rótulos afastados da ponta; F⃗_méd ∥ Δp⃗ ≠ v⃗_f na CONTA;
p⃗ᵢ entra com p⃗_f.
E3: rótulo do ponto fora da curva; foguete no PALCO longe do logo.
T6: dois painéis entram com conteúdo; K = p²/2m no CENTRO por substituição; mãos (§5.2); barcos opacos, raias de gelo claras, F⃗ na
popa, m/2m acima do barco, CHEGADA tracejada; setas p (1 e √2) lado a lado na CONTA.
E4: 3D com câmera igual à do hook; gráficos F_res(t) em escala real com o mesmo eixo vertical (56.000 N em 0,01 s; joelhos pico
≈ 5.900 N = 1,5·560/0,143 em 0,143 s), marcas 3.920 e 56.000, ÁREA = 560 N·s sob cada uma, lupa se precisar; medir áreas.
N = F_res + mg como título na CONTA; faixa mg na mesma escala; ≈ 72 / ≈ 6 PESOS piscando juntos; "MAIS TEMPO…" centrado.
E5: pulga maior no PALCO, régua de 50 cm, zoom no painel direito; painéis com conteúdo; 501 pesos no CENTRO; 70 kg × 35 t com o
manequim 3D renderizado como imagem.
RESUMO: o mesmo gráfico em escala real do E4. F1 sem mudança.

## 5. Peças ilustradas
5.1 Cavalo e pedra (F2), asset reutilizável em `assets_unidade/cavalo/` (hook do yt_0016). Plano A: modelo 3D CC0 (ex.: Horse da
Quaternius), LICENCA.txt com URL e licença; vista lateral (fov ≤ 20°), ~45% da largura; aço fosco (metalness 0,3, roughness 0,6),
crina/cauda #B8C4DA, sem transparência; clip de passo lento, inclinado; pedra icosaedro com ruído #4A5262 com sombra; corda tubo GEO
do peitoral à pedra; chão igual ao do hook; camada Manim via compor.py. Plano B: SVG CC0 de silhueta com SVGMobject, aço com
contorno GEO, sem transparência; proibido montar à mão. Setas #5AA2FF na altura da corda, presas às pontas (F⃗ na pedra, −F⃗ no
peitoral), mesmo comprimento, pulsando; interrogação suave; pergunta em cima; PRÓXIMO VÍDEO como LEGENDA; sem header.
5.2 Mãos do T6: mão aberta de perfil 2D preenchida (palma + 4 dedos + polegar), bola na palma, cota d e 5d, p e K na CONTA.
5.3 Pulga: perfil preenchido, corpo oval, cabeça pequena, 6 patas (traseiras longas, fêmur grosso), ≥ 0,6 u no plano geral, salto
com trajetória tracejada até 50 cm; no zoom as patas esticam 1 mm.

## 6. Paleta e textos
Sem mudança. Nada de vermelho ou verde. Decimais com vírgula, milhar com ponto.

## 7. Render e QA
Stills 1920×1080: H3; T2 lateral; E2; T6 (mãos); E4 escala real; E5 zoom; F2. QA: sobreposição (folga ≥ 0,25); vazio (> 6 s com
uma metade vazia); centralização (|x| < 0,1); pausas > 8 s sem mudança; áreas T5 e E4; alinhamento 3D × Manim ≤ 2 px (hook, T2, E4, F2).

## 8. Parada e relatório
Preview v3 completo; relatório AGENTS.md com auditorias, áreas, cavalo (plano, fonte, licença), Teste do arsenal, pendências.
