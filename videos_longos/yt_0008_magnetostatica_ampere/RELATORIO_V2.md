# yt_0008 · 5.3 — V2: reconstrução visual (relatório)

Data: 2026-10-19. Escopo: rodada estrutural pedida pelo handoff "V2" (implementação visual). Física, matemática, N01–N23, ordem
didática e as quatro aplicações não foram reabertas. Sem voz, SRT, master, 1080p, capa, publicação, commit ou push.
Arquivos alterados só dentro da unidade. `RELATORIO.md` descreve a V1.

## A. Correções estruturais
- **Lifecycle / duplicações.** Causa confirmada no código: `LaggedStart(*[Create(r) for r in rings0])` faz o Manim adicionar CADA anel à
  cena; `self.remove(rings0)` removia só o grupo, e os anéis antigos ficavam vivos (anéis congelados atrás da sonda e do divergente).
  O mesmo padrão existia em N02 (setas), N06 (níveis e setas de F), N09 (setas radiais) e N15 (malha). V2: `purge()` remove a família
  inteira e limpa os updaters; `out()` = fade + purge; `clear()` usa `purge()` e registra um censo (`census_after_clear` no
  `qa_timeline.json`) que deu **zero objetos sobreviventes** em todos os trechos. Grupos que dependem da vista nunca fazem fade enquanto a
  vista gira (isso derrubou dois renders da V2 durante o desenvolvimento e foi corrigido).
- **Pontas de seta microscópicas.** `arrow()` limita a ponta a 35% do comprimento; as pontas dos laços eram segmentos de 0,04 rad e
  desapareciam. V2: `arrowhead()` desenha cabeças triangulares de tamanho fixo na tela, usadas em anéis, sondas e amperianos.
- **`J_at`.** O vetor da V1 não era tangente às elipses desenhadas (componente normal de até 22% na borda). V2 (em `fisica.py`):
  J = ∇×(ψẑ) com ψ = (dx/a)² + (dy/b)² → tangente às MESMAS elipses e ∇'·J = 0 exato. QA novo: J·n̂ = 2·10⁻¹⁶ e ∇'·J = 0.
- **Delta (N09).** A integral 1 da figura deixou de ser fingida: a altura desenhada tem teto e, quando ele corta o pico, aparece
  "altura fora de escala". A grade de setas passa exatamente pelo observador, então sobra uma única contribuição.
- **Projeção.** `tau < 0` = vista de cima (destra), para que o sentido de circulação percebido seja o físico.

## B. N01–N05 (reconstruídos)
- **N01:** fio + UM círculo, sentido de B com pontas grandes; depois o mesmo círculo copiado para outras duas alturas (três círculos
  iguais, mesmo raio e opacidade) → simetria ao longo do eixo.
- **N02:** passa para a vista de cima. P, s e um vetor B grande tangente; três raios com comprimentos ∝ 1/s. Álgebra rastreável:
  B_φ vem do cartão, o s é riscado antes de sair, e o desenho responde: P se afasta e se aproxima com leituras de s, B_φ e s·B_φ
  (constante). Só depois vêm d/ds(constante) = 0 e o rotacional nulo.
- **N03:** fundo simplificado (um círculo atenuado e duas setas locais), sonda maior com normal e chamada para ∂A. O setor de prova vai
  para 2D (vista de cima). A rotação da sonda foi preservada, com as três componentes.
- **N04:** a expansão sincroniza geometria, equação e nota: o laço para no instante em que cruza o eixo (flash no fio), e só então
  I_enc = 0 → I e ∮ = 0 → μ0I. Nota "calculado com o campo de Biot–Savart"; o nome Ampère ainda não aparece.
- **N05:** cena nova, local: caixa grande, linhas de B atravessando, normais para fora, face de entrada −Φ_B e de saída +Φ_B,
  −Φ_B + Φ_B = 0 → ∮ = 0 → ∇·B = 0. A carga elétrica vem depois, com espaço próprio.

## C. N06–N10 (preservados e refinados)
- Cores fonte/observador e movimentos separados de r e r′ preservados. Rótulos tirados da região densa (os papéis saem depois de
  nomeados); a origem dos vetores-posição foi afastada para r e r′ abrirem em leque.
- Identidades (N06 e N08): o diagrama recua e a matemática cresce. A correspondência termo a termo é destacada antes de qualquer
  eliminação. Os dois termos com derivada de J(r′) em r são riscados depois da justificativa ("variáveis independentes, não continuidade").
- N07: célula de continuidade maior, alinhada com J, com "entra/sai", entrando só depois de a fonte parar.
- N09: J atenuado enquanto F é o protagonista; esfera visível (disco translúcido, brilho e equador); texto "divergente zero fora da
  singularidade"; seleção progressiva pelo delta.
- N10: troca ∇ → −∇′ destacada nos dois lugares antes da substituição. Integração por partes em dois cortes separados: primeiro o termo
  de superfície (corrente localizada), com o outro termo ainda visível; depois ∇′·J = 0 (continuidade + magnetostática).

## D. N11–N15
- **Fio finito:** cilindro em 2.5D (com três círculos iguais) que gira até a seção transversal 2D. Nela: ⊙ de J, sonda radial com B ∝ s
  ou 1/s e um ponto sincronizado no gráfico. A marca s = a nasce do rótulo a da geometria.
- **C/s:** uma curva única com C (ValueTracker) explode perto do eixo; a regularidade leva C a 0 e o gráfico vira B ∝ s.
- **C_ext:** uma curva única desliza ("diferentes valores de C") até passar pelo ponto de dentro em s = a. A nota diz "sem corrente
  superficial singular".
- **Limite a → 0:** marcadores de J encolhem com a região; pilar com volume I e "altura fora de escala" quando cortado; o gráfico corta
  a curva com seta (nunca achata). O paradoxo do N02 é resolvido na mesma vista de cima.
- **Stokes:** começa com DUAS células ampliadas: o lado comum é percorrido nos dois sentidos e cancela. Só depois vem a malha completa.
  A cúpula S₂ preserva a borda, e o fundo S₁ fica visível para formar o volume fechado V.

## E. N16–N20
- **N16:** em 2D (vista de cima), com vetores grandes. O caminho irregular se deforma em círculo.
- **N17:** 2.5D só para estabelecer, depois 2D. Primeiro um dℓ e um B grandes e paralelos, depois o mesmo em todo o círculo. O círculo se
  desenrola num segmento 2πs, e o rótulo voa para a equação.
- **N18:** seta K grande sobre a lâmina em 2.5D. A lâmina afina até virar o corte 2D, onde está toda a aplicação: lados curtos
  "B ⊥ dℓ ⇒ 0", lados longos BL + BL, faixa de largura L destacada na própria lâmina → KL.
- **N19:** ordem preservada. Caminho 1 tracejado ("todo fora"), com B(a)L − B(b)L = 0 nascendo dos lados, deslizamento e B(s→∞) = 0.
  Caminho 2 contínuo ("dentro + fora"), com contagem numerada das espiras → μ0(nL)I. O esquema do solenoide finito ganhou palco
  próprio, com linhas internas e de retorno conectadas.
- **N20:** setas de corrente sobre as espiras (sobe na face interna, desce na externa). Na vista de cima: enrolamento atenuado, a, b e s
  marcados na geometria, um amperiano por vez e um ponto no gráfico seguindo o amperiano. Nenhum campo desenhado fora do enrolamento.

## F. Álgebra / MF-Tools
- `TransformByGlyphMap` (via `show`/`gmap`, origem explícita de cada termo): N02 (B_φ entra, s riscado e cancelado), N04 (0 → μ0I),
  N05 (−Φ+Φ), N06 (identidade → dois termos, termo nulo), N08 (quatro termos nascendo dos termos da identidade, dois riscados),
  N09 (4π, delta → J(r)), N10 (∇ → (−∇′), sinais, superfície → 0, ∇′·J → 0), N11/N12 (1/s atravessa, s² → s, C/s sai, C_ext), N13,
  N14/N15 (Stokes, I₁ + I₂ − I₃ → I_enc), N17 (B·dℓ → B dℓ, 2πs vindo do segmento desenrolado), N18 (BL, KL, L cancela),
  N19 (B(a)L − B(b)L, (nL) → n), N20.
- `TransformMatchingTex`: não foi necessário.
- Fade: só onde não há termo em comum (quadro eletrostática × magnetostática, cartões de definição).
- Matching abandonado: na V1, "I₁ → I_enc" mapeava uma parcela no total. Agora I_enc nasce da soma inteira.

## G. 2.5D × 2D
- **2.5D (profundidade é a informação):** fio em N01, sonda girando em N03, caixa em N05, cilindro em N11, superfície, normal,
  correntes e cúpula em N14–N15, estabelecimento de N17/N18/N19/N20 (fio, lâmina, hélice, toroide).
- **2D (raciocínio):** dependência radial em N02, setor em N03, seção do fio finito em N11–N13, caminhos de N16–N17, corte da lâmina,
  corte do solenoide, vista de cima do toroide, gráficos.

## H. Render
Ver o relatório de entrega no chat (comandos, trechos, duração, caminhos).

## I. Problemas restantes
Ver o relatório de entrega no chat.
