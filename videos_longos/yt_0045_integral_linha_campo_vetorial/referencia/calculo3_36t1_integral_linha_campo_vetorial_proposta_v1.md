# Cálculo III · 3.6-T1 · Integral de um campo vetorial sobre uma curva · proposta v1

**Unidade:** `yt_0045` (provisório) · **EP. 20** (provisório, segue o yt_0044 = EP. 19, exercícios do módulo de integral tripla) · `longo_horizontal` · teoria
**Referência:** Guidorizzi, vol. 3, §6.1 (trabalho por soma de F(γ(tᵢ)) · (γ(tᵢ) − γ(tᵢ₋₁)) e γ(tᵢ) − γ(tᵢ₋₁) ≈ γ′(tᵢ)Δtᵢ; definição com F contínuo no aberto Ω e γ de classe C¹; Ex. 1 com integrando ímpar t + 2t³ e trabalho zero) e §6.2 (outra notação: ∫_γ P dx + Q dy e ∫_γ P dx + Q dy + R dz; Ex. 2 na elipse, sentido anti-horário; Exercício 8, círculo de raio R). Didática do Stewart §16.2 (trabalho, campo que gira, notação P dx + Q dy + R dz). Livros só na descrição do YouTube.
**Arquivos irmãos:** narração `yt_0045_narracao_v1.md` · handoff `yt_0045_handoff_v1.md` (Claude Code) · alvos `yt_0045_quadros_alvo_v1/` (18 alvos) · sympy `verificacao/verifica_calc3_36t1_sympy.py` (39/39).

---

## 1. Decisões

| # | Decisão | Origem |
|---|---|---|
| D1 | **Componentes P, Q, R** (como nos livros e no EP. 01, e vão voltar em Green e Stokes). A hélice usa a **lata do canal (raio 1, altura 1)**: γ(t) = (cos t, sen t, c t). R maiúsculo só aparece como raio nos exemplos do plano (círculo do redemoinho, S2) e como 3ª componente no cartão geral do B6-1, nunca os dois na mesma tela. | Kaio, 2026-11-18 (card) |
| D2 | **Hook = cumprir o gancho do EP. 19**: hélice na parede da lata, conta de colar, força: quanto trabalho numa volta? Payoff no B7 com a conta inteira. | gancho do yt_0044 |
| D3 | Cores: **campo F verde-menta `#2EE6A0`** (padrão do EP. 01 para campos), **γ′ e deslocamentos (Δγᵢ, dγ) violeta `#B48CFF`** (EP. 01: violeta só γ′), curva/hélice laranja `#FFB36B`, t `#E08A3C`, x âmbar, y magenta, z azul, W branco. Sinal: ajuda = lima `#C6F26B`, de lado = GEO, atrapalha = ALERTA. **Atenção:** no S2 do EP. 19 a seta F está azul; aqui ela é verde-menta (ver §6). | série |
| D4 | Construção pela física, no rigor do Guidorizzi: força constante no reto (W = F · (B − A)) → partição do **tempo** e cordas → Δγᵢ ≈ γ′(tᵢ)Δtᵢ → soma de Riemann de g(t) = F(γ(t)) · γ′(t) → definição. Hipóteses explícitas (F contínuo no aberto Ω, γ de classe C¹) com o porquê de cada uma (existência da integral; erro da troca → 0). | Guidorizzi §6.1 |
| D5 | Três exemplos 2D que ensinam o **sentido do sinal**: redemoinho (−y, x) no círculo (ajuda sempre: 2πR²), no raio (de lado: 0) e o "vento" (x, y) na parábola (contra na ida, a favor na volta: 0). O redemoinho no círculo é conferido **pela soma de Riemann exata** n R² sen(2π/n) → 2πR². | Produção |
| D6 | Duas sementes sem prometer vídeo: **"o dobro da área"** (círculo 2πR² e elipse 4π = 2 · 2π) aponta para o teorema de Green; **"só importam as pontas"** (F = (x, y), primitiva = ½(x² + y²)) aponta para os campos conservativos. Os dois citados como "mais adiante no curso". | Produção |
| D7 | Outra notação deduzida, não decretada: dx = x′(t) dt é a mesma regra da substituição; alerta "não é ∫ em x mais ∫ em y: volta sempre para o t". Exemplo na notação: a elipse (Guidorizzi §6.2, Ex. 2). | Guidorizzi §6.2 |
| D8 | Força da hélice com significado: **F = (−y, x, −1)** = redemoinho + peso de uma unidade. W = 2π − 2πc = (2 × área da tampa) − (peso × subida). Na lata do canal (duas voltas sobem 1 ⇒ c = 1/(4π)): **W = 2π − 1/2 ≈ 5,78**; empata em c = 1. | Produção |
| D9 | Gancho do **3.6-T2** (mudança de parâmetro e curvas C¹ por partes): o mesmo círculo percorrido duas vezes mais rápido (γ₂(u) = (R cos 2u, R sen 2u), 0 ≤ u ≤ π), ao contrário, e um caminho com quina. Sem dar a resposta (C9 conferido: 2πR² e −2πR²). Desafio dos comentários: a conta da volta mais rápida. | regra da série |
| D10 | Fala sem θ (evita a palavra e o símbolo); a única menção às cilíndricas é falada no H1. Nada de "ds" nesta aula (o comprimento de arco é o 3.6-T3, e s já é a distância ao eixo). | pronúncia + notação |
| D11 | 3D só na hélice (Three.js: `helice`, `heliceCampo`, `heliceLeitura`, câmera da lata do yt_0043/44, fixa); o resto em 2D Manim com papel nascendo dos eixos de borda a borda. | regra do canal |
| D12 | Duração ≈ 19:00 (3.390 palavras a 3 p/s), acima do 8–15 do Atlas, no padrão dos irmãos. Plano de corte no §5. | Produção |

## 2. Fio do vídeo

1. **H1–H2:** a hélice na parede da lata e a pergunta do trabalho; a curva não tem área nem volume; só a parte da força ao longo do caminho trabalha; somar trabalhinhos.
2. **B1:** força constante, caminho reto: W = F · (B − A) = |F||B − A| cos α; os três sinais.
3. **B2–B3:** partição do tempo, cordas Δγᵢ, Δγᵢ ≈ γ′(tᵢ)Δtᵢ, soma de Riemann de g(t), limite, definição e receita em três passos.
4. **B4:** redemoinho no círculo (2πR²), conferido pela soma exata; no raio (0); "o dobro da área".
5. **B5:** o vento para fora na parábola: 0, explicado pelas duas metades e pela primitiva ½(x² + y²).
6. **B6:** outra notação (P dx + Q dy, P dx + Q dy + R dz) e a elipse (4π = 2 × área).
7. **B7:** a hélice paga: W = 2π − 2πc, leitura física, a lata do canal, o empate.
8. **S1–S2:** síntese; mais rápido, ao contrário, com quina → próximo vídeo.

## 3. Definição formal ↔ figura (cada símbolo nasce do desenho)

| Símbolo | Nasce de | Onde |
|---|---|---|
| γ(t) | posição da conta no instante t; a régua do tempo de a a b embaixo do palco | B2-1 |
| tᵢ, Δtᵢ | marcas na régua do tempo | B2-1 |
| Δγᵢ = γ(tᵢ) − γ(tᵢ₋₁) | corda violeta entre pontos vizinhos da curva | B2-1 |
| F(γ(tᵢ)) | seta verde no ponto de chegada do pedaço | B2-1 |
| γ′(tᵢ)Δtᵢ | seta violeta tracejada na lupa, quase igual à corda | B2-2 |
| g(t) = F(γ(t)) · γ′(t) | "um número para cada t": o ângulo entre a seta verde e a violeta | B2-2, B3 |
| dγ = γ′(t) dt | apelido do deslocamento minúsculo | B3 |
| dx = x′(t) dt | projeção da curva no eixo x (mini-desenho) | B6-1 |

## 4. Contas linha a linha (o que a tela escreve)

Todos os degraus abaixo vão à tela. IDs para `self.degrau(...)`.

**C1 · força constante, caminho reto (B1)**
- C1.1 `W = F · (B − A)`
- C1.2 `B − A = (4 − 1, 1 − 1) = (3, 0)`
- C1.3 `W = 2 · 3 + 1 · 0 = 6`
- C1.4 `W = |F| |B − A| cos α` (confere: √5 · 3 · 2/√5 = 6; não vai à tela)
- C1.5 três chips: cos α > 0 ⇒ W > 0; α = 90° ⇒ W = 0; cos α < 0 ⇒ W < 0

**C2 · da soma à integral (B2-1, B2-2, B3)**
- C2.1 `a = t₀ < t₁ < ⋯ < tₙ = b`
- C2.2 `Δγᵢ = γ(tᵢ) − γ(tᵢ₋₁)`
- C2.3 `TRABALHINHO ≈ F(γ(tᵢ)) · Δγᵢ`
- C2.4 `W ≈ Σᵢ F(γ(tᵢ)) · Δγᵢ`
- C2.5 `Δγᵢ ≈ γ′(tᵢ) Δtᵢ`
- C2.6 `W ≈ Σᵢ F(γ(tᵢ)) · γ′(tᵢ) Δtᵢ`
- C2.7 `g(t) = F(γ(t)) · γ′(t)`
- C2.8 `W ≈ Σᵢ g(tᵢ) Δtᵢ`
- C2.9 `máx Δtᵢ → 0: W = ∫ₐᵇ F(γ(t)) · γ′(t) dt`
- C2.10 chip `γ DE CLASSE C¹: O ERRO DA TROCA SOME NO LIMITE`
- C2.11 (B3) `∫_γ F · dγ = ∫ₐᵇ F(γ(t)) · γ′(t) dt` · `dγ = γ′(t) dt`

*Porquê do C2.10 (rigor, não vai à tela):* γ(tᵢ) − γ(tᵢ₋₁) = ∫ γ′(u) du em [tᵢ₋₁, tᵢ] = γ′(tᵢ)Δtᵢ + Eᵢ, com |Eᵢ| ≤ ω(máx Δt) Δtᵢ, onde ω é o módulo de continuidade uniforme de γ′ em [a, b] (γ′ contínua num compacto). Com |F(γ(t))| ≤ M em [a, b]: |Σ F(γ(tᵢ)) · Eᵢ| ≤ M ω(máx Δt)(b − a) → 0. A integral existe porque t ↦ F(γ(t)) · γ′(t) é contínua em [a, b].

**C4 · redemoinho no círculo (B4-1), no raio (B4-3) e a soma exata (B4-2)**
- C4.1 `F(x, y) = (−y, x)` · `γ(t) = (R cos t, R sen t), 0 ≤ t ≤ 2π`
- C4.2 `① F(γ(t)) = (−R sen t, R cos t)`
- C4.3 `② γ′(t) = (−R sen t, R cos t)`
- C4.4 `③ F(γ(t)) · γ′(t) = R² sen²t + R² cos²t = R²(sen²t + cos²t) = R²`
- C4.5 `W = ∫₀^{2π} R² dt = R²[t]₀^{2π} = R²(2π − 0) = 2πR²`
- C4.6 `F(γ(tᵢ)) · Δγᵢ = (−R sen tᵢ)(R cos tᵢ − R cos tᵢ₋₁) + (R cos tᵢ)(R sen tᵢ − R sen tᵢ₋₁)`
- C4.7 `= R²(sen tᵢ cos tᵢ₋₁ − cos tᵢ sen tᵢ₋₁)` (os termos −R² sen tᵢ cos tᵢ e +R² cos tᵢ sen tᵢ se cancelam)
- C4.8 `= R² sen(tᵢ − tᵢ₋₁) = R² sen(2π/n)`
- C4.9 `Σᵢ = n R² sen(2π/n)`
- C4.10 `n = 4: 4R² · n = 8: ≈ 5,66R² · n = 16: ≈ 6,12R²`
- C4.11 `n → ∞: n sen(2π/n) → 2π ⇒ 2πR² ≈ 6,28R²` ✓
- C4.12 `γ(t) = (t, 0), 0 ≤ t ≤ R`
- C4.13 `F(γ(t)) = (0, t), γ′(t) = (1, 0)`
- C4.14 `F(γ(t)) · γ′(t) = 0 · 1 + t · 0 = 0 ⇒ W = ∫₀ᴿ 0 dt = 0`
- C4.15 `NA VOLTA: 2πR² = 2 · πR² = 2 × ÁREA DO DISCO`

**C5 · o vento para fora (B5-1, B5-2)**
- C5.1 `F(x, y) = (x, y)` · `γ(t) = (t, t²), −1 ≤ t ≤ 1`
- C5.2 `① F(γ(t)) = (t, t²)` · `② γ′(t) = (1, 2t)`
- C5.3 `③ F(γ(t)) · γ′(t) = t · 1 + t² · 2t = t + 2t³`
- C5.4 `W = ∫₋₁¹ (t + 2t³) dt = [t²/2 + t⁴/2]₋₁¹`
- C5.5 `= (1/2 + 1/2) − (1/2 + 1/2) = 1 − 1 = 0`
- C5.6 `IDA: ∫₋₁⁰ (t + 2t³) dt = 0 − 1 = −1`
- C5.7 `VOLTA: ∫₀¹ (t + 2t³) dt = 1 − 0 = +1`
- C5.8 `t²/2 + t⁴/2 = ½(x² + y²) NO PONTO γ(t)`
- C5.9 `AS DUAS PONTAS À DISTÂNCIA √2 ⇒ W = 0` ✓

**C6 · outra notação (B6-1)**
- C6.1 `F = (P, Q), γ(t) = (x(t), y(t))`
- C6.2 `F(γ(t)) · γ′(t) dt = P(x(t), y(t)) x′(t) dt + Q(x(t), y(t)) y′(t) dt`
- C6.3 `dx = x′(t) dt, dy = y′(t) dt`
- C6.4 `∫_γ F · dγ = ∫_γ P dx + Q dy`
- C6.5 `NO ESPAÇO: F = (P, Q, R) ⇒ ∫_γ P dx + Q dy + R dz`
- C6.6 `REDEMOINHO: ∫_γ −y dx + x dy`

**C7 · a elipse (B6-2)**
- C7.1 `∫_γ −y dx + x dy, x = 2 cos t, y = sen t, 0 ≤ t ≤ 2π`
- C7.2 `dx = −2 sen t dt, dy = cos t dt`
- C7.3 `−y dx = −sen t · (−2 sen t dt) = 2 sen²t dt`
- C7.4 `x dy = 2 cos t · cos t dt = 2 cos²t dt`
- C7.5 `−y dx + x dy = 2(sen²t + cos²t) dt = 2 dt`
- C7.6 `∫₀^{2π} 2 dt = 2[t]₀^{2π} = 4π`
- C7.7 `ÁREA DA ELIPSE = π · 2 · 1 = 2π ⇒ 4π = 2 × ÁREA` ✓ (área por integral dupla conferida no sympy)

**C8 · a hélice (B7-1, B7-2, B7-3)**
- C8.1 `γ(t) = (cos t, sen t, c t), 0 ≤ t ≤ 2π` · `F(x, y, z) = (−y, x, −1)`
- C8.2 `W = ∫_γ −y dx + x dy − dz`
- C8.3 `dx = −sen t dt, dy = cos t dt, dz = c dt`
- C8.4 `−y dx = −sen t · (−sen t dt) = sen²t dt`
- C8.5 `x dy = cos t · cos t dt = cos²t dt`
- C8.6 `−dz = −c dt`
- C8.7 `W = ∫₀^{2π} (sen²t + cos²t − c) dt = ∫₀^{2π} (1 − c) dt`
- C8.8 `= (1 − c)[t]₀^{2π} = (1 − c)(2π − 0)`
- C8.9 `= 2π − 2πc`
- C8.10 `2π = 2 · (π · 1²) = 2 × ÁREA DA TAMPA`
- C8.11 `2πc = z(2π) − z(0) = SUBIDA NUMA VOLTA ⇒ −2πc = −1 × SUBIDA`
- C8.12 `NOSSA LATA: 2 VOLTAS SOBEM 1 ⇒ 2πc = 1/2 ⇒ c = 1/(4π)`
- C8.13 `W = 2π − 1/2 ≈ 5,78 > 0`
- C8.14 `W = 0 ⟺ 2π − 2πc = 0 ⟺ c = 1`
- (reserva, não vai à tela) duas voltas na lata: 4π − 1; soma com 20 000 pedaços = 5,78319.

**C9 · gancho (S2, só as perguntas na tela)**
- C9.1 `γ₁(t) = (R cos t, R sen t), 0 ≤ t ≤ 2π` · `γ₂(u) = (R cos 2u, R sen 2u), 0 ≤ u ≤ π`
- (reserva para o 3.6-T2) γ₂ dá 2πR² (igual); ao contrário dá −2πR².

## 5. Duração e plano de corte

≈ 19:00 (3.390 palavras). Se o Kaio quiser chegar perto de 15 min: tirar o **B4-2** (soma exata, −1:04) e o **B5** inteiro (−1:58) ⇒ ≈ 15:58; nesse caso o S1 perde o item "só as pontas" e o B6-2 continua. Não cortar o B2-2 (é a ponte da definição) nem o B7.

## 6. Pontos para o Kaio

1. Confirmar `yt_0045` / EP. 20.
2. Duração ≈ 19:00 contra 8–15 do Atlas (corte sugerido no §5).
3. Cor da força: no S2 do EP. 19 (alvo 26) a seta F está **azul** `#5AA2FF`; aqui é **verde-menta** (cor de campo do EP. 01). Se quiser casar, trocar a seta no EP. 19 é uma linha (`cenas44.js`, cena `helice`, cor da seta) antes do preview dele.

## 7. Verificação

`verificacao/verifica_calc3_36t1_sympy.py` → **39/39 True** (C1–C9, inclusive a soma de Riemann exata do círculo, a área da elipse por integral dupla e uma soma numérica com 20 000 pedaços na hélice). `verificacao/confere_narracao_45.py` → 120 gatilhos, 0 faltando.
