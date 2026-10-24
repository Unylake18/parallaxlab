# Storyboard — yt_0011 · Lei de Faraday (18 estados)

Modos: FOCUS (um elemento dominante), SPLIT (fenômeno + matemática/gráfico), COMPARE (duas perspectivas), BUILD (derivação). Cores da série (iguais ao yt_0009): **B magenta**, **E e ℰ (fem) ciano**, **I verde**, **carga azul**, **força azul-claro**, **fluxo lilás-claro**, geometria/dℓ/S/C/r/R/A/u violeta, matéria cinza-aço, matemática branca. Texto de tela em caixa alta; minúsculas só no índice de variáveis.

Dois trackers soberanos:
- **`tau`**: tempo físico. B(tau), dB/dtau, fluxo, fem e a resposta elétrica (ponteiro, portadores, setas de E) derivam só dele.
- **`rT`**: raio do círculo de integração, superfície relevante, E_φ(r), setas de E e ponto do gráfico.

1. **Corrente sem movimento** (FOCUS). “A espira está parada. O fio está parado.” B(t) começa a crescer, o ponteiro responde, os portadores circulam; `I ≠ 0`; depois “O que está empurrando essas cargas?”. Em seguida identidade (“Bem-vindos ao Parallax Lab”) e promessa (título): gancho → identidade → promessa.
2. **Remover o mecanismo anterior**. “condutor parado”; `F_mov = q u×B` com `u = velocidade do condutor`; `u = 0` ⇒ `F_mov = 0`; a corrente continua.
3. **Paradoxo** (FOCUS limpo). `u×B = 0 mas ℰ ≠ 0`. “Então o que está empurrando as cargas?”
4. **Faraday ainda funciona** (SPLIT). `Φ_B = B(t)A` nasce da figura (B(t) pulsa, A acende); `ℰ = −dΦ_B/dt` → `−d/dt[B(t)A]` → `ℰ = −A dB/dt`, com A constante (espira imóvel).
5. **Quanto não é o mesmo que mecanismo**. Carga destacada (rótulo q); “Faraday: quanto vale a fem” × “que força local atua sobre q?”; `F/q = ?`.
6. **Campo elétrico induzido** (BUILD). `ℰ = ∮ F/q·dℓ` → `ℰ = ∮ E·dℓ`; seta de força `F_E = qE` na carga (rótulo afastado, fora da espira e das setas finas de E) e setas de E na espira; `ℰ = −dΦ_B/dt`; `∮_C E·dℓ = −dΦ_B/dt`.
7. **Circulação antes da geometria**. C é caminho escolhido, não linha de campo: em três pontos, E local (não tangente), dℓ e a parte tangencial; o escalar `E·dℓ` rotulado junto à projeção. Coluna direita em blocos verticais: fórmula `∮_C E·dℓ ≠ 0`; “C é um caminho que escolhemos…”; “Faraday estabeleceu circulação”; “Ainda não determinamos a geometria completa do campo”; pergunta de transição.
8. **Eletrostática × indução** (COMPARE). Contribuições locais de E·dℓ ao longo do caminho (sinais + e −): eletrostática soma 0; indução, mesmo sinal ⇒ `≠ 0`. Mensagem protegida: o campo induzido por fluxo variável não é, em geral, eletrostático conservativo.
9. **Geometria cilíndrica**. Corte transversal do solenoide ideal com eixo, R, +ẑ (⊙), +φ̂ anti-horário, B ≈ 0 fora; simetria: pontos à mesma distância do eixo são equivalentes por rotação; só o campo induzido pela variação de B ⇒ `E = E_φ(r)φ̂`; círculos ciano concêntricos; `E_φ < 0` ⇒ horário.
10. **Dentro, r < R** (SPLIT sincronizado). `∮E·dℓ = E_φ(2πr)` (contorno acende); `Φ_B = Bπr²` (área acende); `E_φ(2πr) = −πr²Ḃ`; glyph map `−πr²/2πr → −r/2`; `E_φ = −(r/2)Ḃ`, `|E| ∝ r`.
11. **Chegada a R**. Três objetos: caminho C, superfície S, parte de S com B. Em r = R coincidem; para r > R, C e S crescem e a parte com B fica em πR².
12. **Fora, r > R**. `Φ_B = BπR²` (região magnética acende); `E_φ(2πr) = −πR²Ḃ`; glyph map `−πR²/2πr → −R²/2r`; R² fixo (região) × r variável (caminho); `|E| ∝ 1/r`.
13. **Gráfico sincronizado** (SPLIT). `|E|(r)` com o mesmo `rT`; r = 0 verdadeiro (círculo some); ramo ativo em destaque (`r ≤ R` / `r ≥ R`); em r = R a geometria e o gráfico congelam, a expressão por partes sai e entram `|E(R⁻)| = |E(R⁺)| = (R/2)|Ḃ|`, a caixa `|E(R⁻)| = |E(R⁺)|`, “contínuo em R” e depois “a inclinação muda” (quina); a expressão por partes volta e o ponto segue pelo ramo `1/r`.
14. **Resultado contraintuitivo**. Ponto externo (r > R) com lupa sem B: `B(ponto) ≈ 0` **mas** `E(ponto) ≠ 0`; ligado ao caminho, à superfície S e ao fluxo interno (região magnética acende).
15. **Integral → diferencial** (BUILD). Ícone: S, C = ∂S, dℓ positivo anti-horário (violeta), E real horário (ciano), normal +z. `∮_C E·dℓ = −d/dt ∫_S B·da` → Stokes → S fixa (derivada entra) → agrupar `∫_S(∇×E + ∂B/∂t)·da = 0` → “Vale para qualquer S fixa.” (região pequena) → “Logo, ponto a ponto:” → `∇×E = −∂B/∂t`. Frases trocam em sequência (sai a antiga, entra a nova); a equação fica estável; nenhuma integral “cancelada”.
16. **Local não é global**. Dentro: `∂ₜB ≠ 0`, `∇×E ≠ 0`. Fora (momento 1): `∂ₜB = 0`, `∇×E = 0`, `E ≠ 0`. Pequena volta externa, que não envolve o eixo (momento 2): `∮_{C_peq} E·dℓ = 0`. Grande volta envolvendo o eixo (momento 3): `∮_{C_env} E·dℓ = −πR²Ḃ ≠ 0`. “Rotacional zero localmente não significa campo nulo.” Anéis secundários atenuados.
17. **Retirar o detector**. Só o detector sai (fio, espira, amperímetro, portadores); B(t) e os anéis de E permanecem. “O fio não cria esse campo. Ele apenas revela sua existência.” Respiro de ~7 s.
18. **Síntese + end card**. Global `∮_C E·dℓ = −dΦ_B/dt` × local `∇×E = −∂B/∂t` (nunca a síntese simplista “∂B/∂t ≠ 0 ⇒ ∇×E ≠ 0” isolada). Depois o end card da série: logo Parallax Lab centralizado e “PRÓXIMO VÍDEO: INDUTÂNCIA E ENERGIA MAGNÉTICA”, sem texto de CTA (like e inscrição só na narração).
