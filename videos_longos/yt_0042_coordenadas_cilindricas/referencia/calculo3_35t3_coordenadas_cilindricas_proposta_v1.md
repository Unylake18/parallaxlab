# Cálculo III · 3.5-T3 · Coordenadas cilíndricas na integral tripla · proposta v1

**Unidade:** `yt_0042` (provisório) · **EP. 17** (provisório, segue o EP. 16 esféricas = yt_0041) · `longo_horizontal` · teoria
**Referência:** Guidorizzi, vol. 3, §5.6 (coordenadas cilíndricas; Ex. 1 lata com densidade √(x² + y² + z²); Ex. 2 cilindro fora do eixo com teto z = x + y). Livro só na descrição do YouTube.
**Arquivos irmãos:** narração `yt_0042_narracao_v1.md` · handoff `yt_0042_handoff_v1.md` · prompt do agente externo `yt_0042_prompt_agente_externo.md` · alvos `yt_0042_quadros_alvo_v1/` · sympy `verificacao/verifica_calc3_35t3_sympy.py` (56/56).

---

## 1. Decisões

| # | Decisão | Origem |
|---|---|---|
| D1 | **s = distância ao eixo z** (a sombra do EP. 16 e o s do Griffiths). r = distância até a origem (r² = s² + z²); ρ = densidade; R, h = raio e altura fixos; T = a transformação; u, t = substituições. | Kaio, card de 2026-11-16 |
| D2 | Hook = a lata do gancho do EP. 16 (mesma densidade): trava em cartesianas e racha em esféricas. Payoff = o Ex. 1 do livro com a conta inteira. | Produção |
| D3 | O fator s sai por três caminhos: arestas (Δs, sΔθ, Δz), polares × altura, determinante 3×3 por Laplace na linha de baixo. | igual ao EP. 16 |
| D4 | Teste do cilindro πR²h + erro clássico sem o s = 2πRh (área do rótulo, m²). | Produção |
| D5 | B4 = Ex. 2 com polo deslocado para (1, 0); V = π/2 + 2/3. A Observação do livro imprime π/2 + 3/2: é erro de digitação (conferido por sympy e por integração numérica em cartesianas). O polo na origem fica como desafio para os comentários. | Produção |
| D6 | Na lata, a ordem importa: z por dentro trava (logaritmo); s por dentro, o s do fator completa a substituição u = s² + z². | Produção |
| D7 | A integral de z usa o triângulo (z = tg t) e a recorrência da sec⁵ (n = 5 e n = 3), com os valores lidos do triângulo t = π/4. | Produção |
| D8 | Gancho: "No próximo vídeo: centro de massa e momento de inércia na integral tripla" (3.5-T4 do Atlas). Na série de Cálculo isso é permitido. | regra da série |
| D9 | Duração ≈ 20:11 (3.600 palavras a 3 p/s). Fica acima do 8–15 do Atlas, mas no padrão dos irmãos (EP. 15 ≈ 20:27, EP. 16 ≈ 22:12). Plano de corte no §5. | Produção |
| D10 | 3D em Three.js (lata, grade, ponto, caixa, latagrade, caixinha, cilindro, deslocado, giro); 2D em Manim com papel de borda a borda. | regra do canal |

## 2. Fio do vídeo

1. **H1–H2:** a lata pesada trava em cartesianas e racha em esféricas → a grade da lata (cilindros, páginas, andares) → "qual é o volume de cada pedaço?"
2. **B1:** o endereço (s, θ, z), com s = distância ao eixo e não à origem; ponto (2, π/3, 3/2) → (1, √3, 3/2), r = 5/2 (3-4-5 pela metade); a caixa vira a lata, com duas bordas ruins (eixo e costura).
3. **B2:** ΔV ≈ s Δs Δθ Δz (arestas; números π/96 e π/32, razão 3, aqui o ≈ é exato); polares × altura; determinante = s; teste do cilindro πR²h e o erro 2πRh.
4. **B3:** o teorema geral e a lata em duas metades; a receita (sombra em polares + sonda em pé).
5. **B4:** o cilindro fora do eixo (polo deslocado): V = π/2 + 2/3 e a leitura termo a termo.
6. **B5:** a lata pesada: s por dentro (u), z pelo triângulo, sec⁵ pela recorrência, M = (π/12)(7√2 − 2 + 3 ln(1 + √2)) ≈ 2,76; média ≈ 0,88.
7. **B6–S2:** quando usar; síntese; girar a lata (I = ∭ s² ρ dV) → gancho do próximo vídeo.

## 3. Contas linha a linha (o que a tela escreve)

**C1 · ponto (B1-2).** (s, θ, z) = (2, π/3, 3/2) · x = 2 cos(π/3) = 2 · 1/2 = 1 · y = 2 sen(π/3) = 2 · √3/2 = √3 · z = 3/2 · x² + y² = 1 + 3 = 4 = 2² ✓ · r = √(4 + 9/4) = √(25/4) = 5/2.

**C2 · células (B2-1).** Δs = 1/2, Δθ = π/6, Δz = 1/2 · eixo: s̄ = 1/4 → (1/4)(1/2)(π/6)(1/2) = π/96 ≈ 0,033 · parede: s̄ = 3/4 → π/32 ≈ 0,098 · razão = 3. Exato porque ∫ₐᵇ s ds = s̄ (b − a).

**C3 · determinante (B2-3).**
| linha | conteúdo |
|---|---|
| 1 | ∂(x, y, z)/∂(s, θ, z) = \|cos θ, −s sen θ, 0; sen θ, s cos θ, 0; 0, 0, 1\| |
| 2 | = 0 · M₃₁ − 0 · M₃₂ + 1 · M₃₃ (Laplace na linha de baixo, sinais + − +) |
| 3 | M₃₃ = \|cos θ, −s sen θ; sen θ, s cos θ\| |
| 4 | M₃₃ = cos θ · s cos θ − (−s sen θ) · sen θ |
| 5 | = s cos²θ + s sen²θ |
| 6 | = s (cos²θ + sen²θ), com a chave "= 1" |
| 7 | = s · chip s ≥ 0 ⇒ \|J\| = s |

**C4 · cilindro (B2-4).** V = ∫₀^{2π}∫₀^R∫₀^h s dz ds dθ = [z]₀^h · [s²/2]₀^R · [θ]₀^{2π} = (h − 0) · (R²/2 − 0) · (2π − 0) = πR²h ✓ · sem o s: h · R · 2π = 2πRh (m²: área do rótulo).

**C5 · fora do eixo (B4).**
| linha | conteúdo |
|---|---|
| 1 | x² + y² − 2x ≤ 0, 0 ≤ z ≤ x + y, x, y ≥ 0 |
| 2 | x² − 2x + 1 + y² ≤ 1 |
| 3 | (x − 1)² + y² ≤ 1 |
| 4 | x = 1 + s cos θ, y = s sen θ, z = z · jacobiano continua s |
| 5 | ① 0 ≤ θ ≤ π, 0 ≤ s ≤ 1 · ② 0 ≤ z ≤ 1 + s cos θ + s sen θ |
| 6 | ③ V = ∫₀^π ∫₀^1 ∫₀^{1 + s cos θ + s sen θ} s dz ds dθ |
| 7 | ∫₀^{teto} s dz = [s z]₀^{teto} = s(1 + s cos θ + s sen θ) − 0 = s + s² cos θ + s² sen θ |
| 8 | ∫₀^1 (…) ds = [s²/2 + (s³/3) cos θ + (s³/3) sen θ]₀^1 = 1/2 + (1/3) cos θ + (1/3) sen θ |
| 9 | ∫₀^π (…) dθ = [θ/2 + (1/3) sen θ − (1/3) cos θ]₀^π |
| 10 | chips sen π = 0, cos π = −1, cos 0 = 1 |
| 11 | = (π/2 + 0 + 1/3) − (0 + 0 − 1/3) |
| 12 | = π/2 + 2/3 ≈ 2,24 ✓ · leitura: 1 → π/2, cos θ → 0, sen θ → 2/3 |

**C6 · lata, integral em s (B5-2).** u = s² + z² (z parado) · du = 2s ds ⇒ s ds = du/2 · s = 0 → u = z²; s = 1 → u = 1 + z² · ∫₀^1 √(s² + z²) s ds = (1/2)∫_{z²}^{1+z²} u^{1/2} du = (1/2)(2/3)[u^{3/2}]_{z²}^{1+z²} = (1/3)[(1 + z²)^{3/2} − (z²)^{3/2}] = (1/3)[(1 + z²)^{3/2} − z³] (z ≥ 0).

**C7 · integral em z (B5-3).** ∫₀^1 (1/3)[(1 + z²)^{3/2} − z³] dz = (1/3)∫₀^1 (1 + z²)^{3/2} dz − (1/3)[z⁴/4]₀^1 = (1/3) I − 1/12 · I = ∫₀^1 (1 + z²)^{3/2} dz · z = tg t, dz = sec²t dt · z = 0 → t = 0; z = 1 → t = π/4 · 1 + tg²t = sec²t ⇒ (1 + z²)^{3/2} = sec³t · I = ∫₀^{π/4} sec³t · sec²t dt = ∫₀^{π/4} sec⁵t dt.

**C8 · sec⁵ (B5-4).** ∫secⁿ = secⁿ⁻² tg/(n − 1) + (n − 2)/(n − 1) ∫secⁿ⁻² · n = 5: ∫sec⁵ = (1/4) sec³ tg + (3/4)∫sec³ · n = 3: ∫sec³ = (1/2) sec tg + (1/2)∫sec, ∫sec = ln|sec + tg| · t = π/4: sec = √2, tg = 1; t = 0: sec = 1, tg = 0 · [(1/4) sec³ tg]₀^{π/4} = (1/4)(√2)³ · 1 − 0 = 2√2/4 = √2/2 · ∫₀^{π/4} sec³ = (√2/2 + (1/2) ln(√2 + 1)) − (0 + (1/2) ln 1) · I = √2/2 + (3/4)(√2/2 + (1/2) ln(1 + √2)) = 4√2/8 + 3√2/8 + (3/8) ln(1 + √2) = 7√2/8 + (3/8) ln(1 + √2) ≈ 1,568.

**C9 · massa (B5-5).** M = 2π[(1/3) I − 1/12] = 2π[7√2/24 + (1/8) ln(1 + √2) − 1/12] = 7√2π/12 + (π/4) ln(1 + √2) − π/6 = (π/12)(7√2 − 2 + 3 ln(1 + √2)) ≈ 2,76 ✓ · cartesianas no computador ≈ 2,7603 · média M/π ≈ 0,88; ρ vai de 0 a √2.

**C10 · reserva (S2, não escrito como conta).** I = ∭ s² ρ dV; em cilíndricas s² · s = s³.

## 4. Verificação

`verificacao/verifica_calc3_35t3_sympy.py` → **56/56 True** (saída em `verifica_calc3_35t3_saida.txt`). Inclui as duas conferências numéricas em cartesianas (scipy): V do B4 = 2,23746 e M do B5 = 2,76031.

## 5. Plano de corte (se o Kaio quiser ≈ 15–17 min)

| Corte | Economia | Efeito |
|---|---:|---|
| Tirar o B4 inteiro (cilindro fora do eixo) e levar para o 3.5-E1 de exercícios | −2:52 | ≈ 17:19; a receita do B3-2 fica sem exemplo com teto variável |
| Juntar B2-2 ao B2-1 (só a frase "polares vezes a altura") | −0:30 | perde a vista DE LADO |
| Tirar o B6 (quando usar) | −0:30 | a escolha fica só na síntese |

Recomendação: manter tudo no preview v1 e decidir o corte vendo o vídeo.

## 6. Quadros-alvo (17)

`yt_0042_quadros_alvo_v1/`: 01 H1 · 02 H2 · 03 B1-1 · 04 B1-2 · 05 B1-3 · 06 B2-1 · 07 B2-2 · 08 B2-3 · 09 B2-4 · 10 B3-1 · 11 B4-1 (etapa 2) · 12 B4-2 (tela da conta em θ) · 13 B5-2 · 14 B5-3 · 15 B5-4 (etapa 2) · 16 B5-5 · 17 S2 + `00_folha_contato_v1.jpg`. Geradores: `sb42.html` (2D, `?k=<chave>`), `c3d42.html` (3D Three.js, `?k=<cena>`), `shot42.js`, `r3d42.js`, `r3d_pts.json` (pontos 3D de cada cena para prender rótulos).
