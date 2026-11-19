# Cálculo III · 3.5-T4 · Centro de massa e momento de inércia na integral tripla · proposta v1

**Unidade:** `yt_0043` (provisório) · **EP. 18** (provisório, segue o EP. 17 cilíndricas = yt_0042) · `longo_horizontal` · teoria
**Referência:** Guidorizzi, vol. 3, §5.7 (definições de momento de inércia por energia cinética e de centro de massa; Ex. 1 esfera homogênea em relação a um diâmetro; Ex. 2 centro de massa do corpo homogêneo x² + y² ≤ z ≤ 1; Exercícios 5.7: Steiner, cilindro fora do eixo, semiesfera). Didática do Stewart §15.8 (momentos M_yz, M_xz, M_xy; I_x, I_y, I_z; raio de giração). Livros só na descrição do YouTube.
**Arquivos irmãos:** narração `yt_0043_narracao_v1.md` (arquivo separado, para o refino do GPT) · handoff `yt_0043_handoff_v1.md` (Claude Code) · alvos `yt_0043_quadros_alvo_v1/` (sistema 3D G1–G6) · sympy `verificacao/verifica_calc3_35t4_sympy.py` (62/62).

---

## 1. Decisões

| # | Decisão | Origem |
|---|---|---|
| D1 | Notação da série desde o 3.5: **ρ = densidade** (ciano), **s = distância ao eixo** (pêssego; o Guidorizzi chama de r), **r = distância até a origem** (laranja), φ só nas esféricas, R e h fixos, **k = densidade constante**. Centro de massa (x̄, ȳ, z̄); momentos em relação aos planos M_yz, M_xz, M_xy; momento de inércia I (I_z quando precisar do eixo); raio de giração **s_G** (I = M s_G², "a distância ao eixo do anel equivalente"; não uso k, que já é a densidade). | série + Kaio (2026-11-16) |
| D2 | **Hook = cumprir o gancho do EP. 17**: a lata pesada (x² + y² ≤ 1, 0 ≤ z ≤ 1, ρ = √(x² + y² + z²)) agora gira. Duas perguntas: onde equilibra (z̄) e quanto custa girar (I_z). Payoff = as duas contas inteiras no fim, comparadas com a lata comum (z̄ = 1/2, I = MR²/2). | gancho do yt_0042 |
| D3 | **Não repetir o 3.4-T3** (massa e centro de massa na chapa): a média ponderada entra em 3 bolinhas e vai direto para o corpo 3D; o "∫(x − x̄) dm = 0" vira o plano z = z̄ que equilibra o corpo (com uma coordenada a mais). A chapa é lembrada como conteúdo ("uma chapa apoiada num lápis"), sem citar vídeo. | coordenação + regra do canal |
| D4 | **Simetria com o porquê**: x = s cos θ e ∫₀^{2π} cos θ dθ = 0 matam x̄ e ȳ quando corpo **e** densidade giram juntos; contraexemplo ρ = 1 + x no cilindro (x̄ = 1/4). | rigor (hipótese explícita + contraexemplo) |
| D5 | Exemplo do centro de massa = **a taça** (Guidorizzi §5.7 Ex. 2, x² + y² ≤ z ≤ 1 homogênea): V = π/2, ∭ z dV = π/3, z̄ = 2/3; chute 1/2 errado porque a taça é larga em cima. Em cilíndricas (continua a série). | Guidorizzi |
| D6 | Momento de inércia **nasce da energia** (como o Guidorizzi): v = ωs, K = ½(s² dm)ω² ⇒ I = ∭ s² ρ dV. Ênfase: s é distância ao **eixo**, não à origem (I_z usa x² + y²; troca o eixo, troca o I). | Guidorizzi + Stewart |
| D7 | Clássicos: cilindro homogêneo **MR²/2** (cilíndricas, s² · s = s³, a promessa do EP. 17) e bola homogênea **(2/5)MR²** (Guidorizzi Ex. 1, esféricas, s = r sen φ = a sombra do EP. 16, u = cos φ com o limite invertido). Comparação com o tubo fino MR² e o raio de giração. Sem a corrida na rampa (Kaio recusou essa pauta). | Guidorizzi + preferências |
| D8 | Lata pesada, **z̄**: s por dentro (u = s² + z², igual à massa) e, em z, o z de fora é a derivada de 1 + z² (w = 1 + z²): **não precisa do triângulo**. M_xy = 4π(2√2 − 1)/15 ≈ 1,532; z̄ ≈ 0,555. | Produção |
| D9 | Lata pesada, **I_z**: s³ = s² · s, s² = u − z²; em z, o triângulo (z = tg t), tg² = sec² − 1 e a recorrência **n = 7**, reaproveitando I₅ = ∫₀^{π/4} sec⁵ = 7√2/8 + (3/8) ln(1 + √2). I_z = (π/90)(19√2 + 4 + 15 ln(1 + √2)) ≈ 1,539; I/M ≈ 0,558 (comum 0,5). | Produção |
| D10 | **Dois resultados vêm do EP. 17** e entram como chip com legenda de origem, sem citar o vídeo: M ≈ 2,76 ("A MASSA DA LATA PESADA (EM CILÍNDRICAS)") e I₅ ("DAS CILÍNDRICAS: RECORRÊNCIA n = 5 E n = 3"). A voz diz "a gente já tirou nas cilíndricas". **Ponto para o Kaio confirmar** (§6). | Produção |
| D11 | Gancho para o **3.5-E1** (exercícios integradores do módulo): girar a lata em volta de uma reta da parede ("como uma porta na dobradiça"), sem dar o número. O 3.5-E1 precisa cumprir: lata homogênea, eixo x = R, y = 0 ⇒ I = (3/2)MR² direto e por Steiner (I_cm + MR²) (C11, conferido). Desafio nos comentários: z̄ da meia bola uniforme (3R/8). | regra da série |
| D12 | Duração ≈ 21:48 (3.892 palavras a 3 p/s), acima do 8–15 do Atlas, no padrão dos irmãos (EP. 15 ≈ 22:29, EP. 16 ≈ 22:12). Plano de corte no §5. | Produção |
| D13 | 3D em Three.js (lataGiro, lataDuas, cmPontos, lataPlano, lataSim, taca, giroCel, distEixo, cilindroH, esferaOct, lataParede); 2D em Manim; papel de borda a borda em toda tela, também sob o 3D, com piso quadriculado (G1–G6). Corte meridiano 2D quando o 3D não basta (B3-5, B4-6). | regra do canal |

## 2. Fio do vídeo

1. **H1–H2:** a lata pesada gira; duas perguntas (equilíbrio e giro), respostas da lata comum na tela (1/2 e MR²/2); "uma conta por pedaço": dm = ρ dV, z · dm e s² · dm.
2. **B1:** do sistema de pontos ao corpo (x̄ = M_yz/M, ȳ, z̄); o plano z = z̄ equilibra (∭(z − z̄)ρ dV = 0); simetria pelo cos θ e o contraexemplo ρ = 1 + x.
3. **B2:** a taça: montar em cilíndricas, k cancela, chute 1/2 ✗, z̄ = 2/3.
4. **B3:** I da energia; distância ao eixo; cilindro MR²/2; bola (2/5)MR²; tubo, cilindro e bola lado a lado, raio de giração.
5. **B4:** a lata pesada: z̄ ≈ 0,555 (sem triângulo) e I ≈ 1,539 (triângulo + sec⁷); lado a lado com a lata comum.
6. **S1–S2:** síntese; eixo na parede → exercícios do módulo.

## 3. Definição formal ↔ figura (cada símbolo nasce do desenho)

| Definição / fato | Figura | Movimento único |
|---|---|---|
| x̄ = Σmᵢxᵢ/Σmᵢ (três vezes) | 3 bolinhas no piso, ⊕ perto da pesada | o ⊕ entra no fim |
| Δm ≈ ρ ΔV → ∭ x ρ dV | lata em traço + 1 célula com x, y, z tracejados | a célula acende; x, y, z voam para a coluna |
| M_xy = ∭ z ρ dV ("distância ao plano xy") | o z da célula | o tracejado z acende |
| ∭(z − z̄)ρ dV = 0 | plano z = z̄ (contorno menta) + células + e − com fios até o plano | os fios crescem até o plano |
| ∫₀^{2π} cos θ dθ = 0 ⇒ x̄ = 0 | duas células gêmeas em θ e θ + π, placas x e −x | as duas acendem juntas |
| contraexemplo ρ = 1 + x | as mesmas células, a da direita mais clara | só a cor muda |
| taça s² ≤ z ≤ 1 | sólido opaco, ¼ aberto, sonda entra/sai | a sonda cresce do fundo à boca |
| z̄ = 2/3 > 1/2 | ⊕ no eixo + tracejado em 1/2 | o ⊕ entra |
| v = ωs, K = ½(s²dm)ω² | célula na parede + fio s + seta v tangente + arco ω | a seta v cresce |
| s² = x² + y² (eixo z) ≠ r² | ponto P, fio horizontal s até o eixo z, fio até o eixo x, segmento r | um fio por vez |
| I = MR²/2 | cilindro opaco + casca de raio s em traço | a casca cresce de s = 0 a R |
| s = r sen φ | bola com octante aberto, raio r, ângulo φ, fio s | o fio s acende |
| tubo / cilindro / bola + s_G | 3 cortes meridianos 2D com a linha s_G | as linhas s_G entram |
| lata pesada z̄ ≈ 0,555, s_G ≈ 0,747 | dois cortes meridianos 2D (comum × pesada) | ⊕ e s_G entram lado a lado |

## 4. Contas linha a linha (o que a tela escreve)

Cada linha é um degrau (ID usado em `self.degrau`). [e] = a voz ensina; [m] = a voz diz ação e resultado.

**C1 · o plano que equilibra (B1-2).**
| degrau | linha |
|---|---|
| C1.1 | ∭ (z − z̄) ρ dV [e] |
| C1.2 | = ∭ z ρ dV − z̄ ∭ ρ dV [m] |
| C1.3 | = M_xy − z̄ M [m] |
| C1.4 | = M z̄ − z̄ M = 0 [e] |

**C2 · simetria e contraexemplo (B1-3).**
| degrau | linha |
|---|---|
| C2.1 | ρ = ρ(s, z) (não depende de θ) [e] |
| C2.2 | M_yz = ∫∫ (∫₀^{2π} cos θ dθ) s² ρ ds dz (x = s cos θ; o s do fator) [e] |
| C2.3 | ∫₀^{2π} cos θ dθ = [sen θ]₀^{2π} = 0 − 0 = 0 [m] |
| C2.4 | ⇒ x̄ = 0; igual para y: ȳ = 0 · chip CORPO E DENSIDADE GIRAM JUNTOS ⇒ CENTRO DE MASSA NO EIXO [e] |
| C2.5 | ρ = 1 + x (cilindro R = 1, h = 1) [e] |
| C2.6 | M = ∭ (1 + x) dV = π + 0 = π [m] |
| C2.7 | M_yz = ∭ x(1 + x) dV = ∭ x dV + ∭ x² dV [m] |
| C2.8 | ∭ x² dV = ∫₀^{2π} cos²θ dθ · ∫₀^1 s³ ds · ∫₀^1 dz = π · (1/4) · 1 = π/4 [m] |
| C2.9 | x̄ = (π/4)/π = 1/4 · chip A DENSIDADE QUEBROU A SIMETRIA [e] |

**C3 · volume da taça (B2-2, etapa 1).**
| degrau | linha |
|---|---|
| C3.1 | V = ∫₀^{2π} ∫₀^1 ∫_{s²}^1 s dz ds dθ [e] |
| C3.2 | ∫_{s²}^1 s dz = [s z]_{s²}^1 = s · 1 − s · s² = s − s³ [m] |
| C3.3 | ∫₀^1 (s − s³) ds = [s²/2 − s⁴/4]₀^1 = 1/2 − 1/4 = 1/4 [m] |
| C3.4 | V = 2π · 1/4 = π/2 [m] |

**C4 · momento e z̄ da taça (B2-2, etapa 2).**
| degrau | linha |
|---|---|
| C4.1 | ∭ z dV = ∫₀^{2π} ∫₀^1 ∫_{s²}^1 z s dz ds dθ [e] |
| C4.2 | ∫_{s²}^1 z s dz = s [z²/2]_{s²}^1 = s (1/2 − s⁴/2) = s/2 − s⁵/2 [m] |
| C4.3 | ∫₀^1 (s/2 − s⁵/2) ds = [s²/4 − s⁶/12]₀^1 = 1/4 − 1/12 = 1/6 [m] |
| C4.4 | ∭ z dV = 2π · 1/6 = π/3 [m] |
| C4.5 | z̄ = (π/3)/(π/2) = 2/3 (moldura) [e] |

**C5 · energia do giro (B3-1).** v = ω s · K = (1/2) dm v² = (1/2)(s² dm) ω² · um ponto I = m s² · vários I = Σ mᵢ sᵢ² · corpo I = ∭ s² ρ dV (moldura) · unidade kg · m².

**C6 · cilindro homogêneo (B3-3).**
| degrau | linha |
|---|---|
| C6.1 | I_z = ∫₀^{2π} ∫₀^R ∫₀^h s² · k · s dz ds dθ (chave s² · s = s³) [e] |
| C6.2 | = k · [z]₀^h · [s⁴/4]₀^R · [θ]₀^{2π} [m] |
| C6.3 | = k · h · R⁴/4 · 2π = πkR⁴h/2 [m] |
| C6.4 | M = k · πR²h [e] |
| C6.5 | I_z = (1/2)(kπR²h) R² = (1/2) M R² (moldura) [e] |
| C6.6 | CASCA FINA: I = MR² [e] |

**C7 · bola homogênea (B3-4).**
| degrau | linha |
|---|---|
| C7.1 | s = r sen φ ⇒ s² = r² sen²φ [e] |
| C7.2 | dV = r² sen φ dr dφ dθ (chip lima) [e] |
| C7.3 | I_z = ∫₀^{2π} ∫₀^π ∫₀^R r² sen²φ · k · r² sen φ dr dφ dθ [e] |
| C7.4 | = k · [θ]₀^{2π} · ∫₀^π sen³φ dφ · [r⁵/5]₀^R = k · 2π · (∫₀^π sen³φ dφ) · R⁵/5 [m] |
| C7.5 | sen³φ = (1 − cos²φ) sen φ [e] |
| C7.6 | u = cos φ, du = −sen φ dφ [e] |
| C7.7 | φ = 0 → u = 1; φ = π → u = −1 [e] |
| C7.8 | ∫₀^π sen³φ dφ = ∫₁^{−1} (1 − u²)(−du) = ∫_{−1}^1 (1 − u²) du [m] |
| C7.9 | = [u − u³/3]_{−1}^1 = (1 − 1/3) − (−1 + 1/3) = 2/3 + 2/3 = 4/3 [m] |
| C7.10 | I_z = k · 2π · 4/3 · R⁵/5 = 8πkR⁵/15 [m] |
| C7.11 | M = k · (4/3)πR³ [e] |
| C7.12 | I_z = (8/15)/(4/3) · MR² = (2/5) MR² (moldura) [e] |

**C8 · raio de giração (B3-5).** I = M s_G² · tubo s_G = R · cilindro R/√2 ≈ 0,71R · bola √(2/5) R ≈ 0,63R.

**C9 · lata pesada: z̄ (B4-1, B4-2).**
| degrau | linha |
|---|---|
| C9.1 | chip M = (π/12)(7√2 − 2 + 3 ln(1 + √2)) ≈ 2,76 · chip SIMETRIA: x̄ = ȳ = 0 [e] |
| C9.2 | M_xy = ∫₀^{2π} ∫₀^1 ∫₀^1 z √(s² + z²) s ds dz dθ (chaves ALTURA, DENSIDADE, FATOR) [e] |
| C9.3 | u = s² + z² (z parado) [e] |
| C9.4 | du = 2s ds ⇒ s ds = du/2; s = 0 → u = z², s = 1 → u = 1 + z² [e] |
| C9.5 | ∫₀^1 √(s² + z²) s ds = (1/2) ∫_{z²}^{1+z²} u^{1/2} du = (1/2)(2/3)[u^{3/2}]_{z²}^{1+z²} [m] |
| C9.6 | = (1/3)[(1 + z²)^{3/2} − z³] · placa z ≥ 0: (z²)^{3/2} = z³ [m] |
| C9.7 | ∫₀^1 z · (1/3)[(1 + z²)^{3/2} − z³] dz = (1/3)∫₀^1 z(1 + z²)^{3/2} dz − (1/3)∫₀^1 z⁴ dz [m] |
| C9.8 | w = 1 + z², dw = 2z dz ⇒ z dz = dw/2; z = 0 → w = 1, z = 1 → w = 2 [e] |
| C9.9 | ∫₀^1 z(1 + z²)^{3/2} dz = (1/2)∫₁^2 w^{3/2} dw = (1/2)(2/5)[w^{5/2}]₁^2 = (1/5)(2^{5/2} − 1) = (1/5)(4√2 − 1) · chip 2^{5/2} = 2² · √2 = 4√2 [m] |
| C9.10 | (1/3)∫₀^1 z⁴ dz = (1/3)[z⁵/5]₀^1 = 1/15 [m] |
| C9.11 | (1/3)(4√2 − 1)/5 − 1/15 = (4√2 − 2)/15 [m] |
| C9.12 | M_xy = 2π(4√2 − 2)/15 = 4π(2√2 − 1)/15 ≈ 1,532 [m] |
| C9.13 | z̄ = M_xy/M = [4π(2√2 − 1)/15] / [(π/12)(7√2 − 2 + 3 ln(1 + √2))] [e] |
| C9.14 | = 16(2√2 − 1)/[5(7√2 − 2 + 3 ln(1 + √2))] ≈ 0,555 (moldura) [m] |
| C9.15 | LATA COMUM: z̄ = 0,5 · chip CONFERE: CARTESIANAS NO COMPUTADOR ≈ 1,5318 [e] |

**C10 · lata pesada: I_z (B4-3, B4-4, B4-5).**
| degrau | linha |
|---|---|
| C10.1 | I_z = ∫₀^{2π} ∫₀^1 ∫₀^1 s² √(s² + z²) s ds dz dθ (chaves DISTÂNCIA AO EIXO², DENSIDADE, FATOR) [e] |
| C10.2 | s³ ds = s² · s ds; u = s² + z² ⇒ s² = u − z², s ds = du/2 [e] |
| C10.3 | ∫₀^1 s³ √(s² + z²) ds = (1/2)∫_{z²}^{1+z²} (u − z²) u^{1/2} du = (1/2)∫_{z²}^{1+z²} (u^{3/2} − z² u^{1/2}) du [m] |
| C10.4 | = (1/2)[(2/5)u^{5/2} − z²(2/3)u^{3/2}]_{z²}^{1+z²} [m] |
| C10.5 | = (1/5)[(1 + z²)^{5/2} − z⁵] − (z²/3)[(1 + z²)^{3/2} − z³] · placa (z²)^{5/2} = z⁵ [m] |
| C10.6 | −(1/5)z⁵ + (1/3)z⁵ = (2/15)z⁵ ⇒ ∫₀^1 (2/15)z⁵ dz = (2/15)(1/6) = 1/45 [m] |
| C10.7 | SOBRA: (1/5)∫₀^1 (1 + z²)^{5/2} dz − (1/3)∫₀^1 z²(1 + z²)^{3/2} dz [e] |
| C10.8 | z = tg t, dz = sec²t dt; z = 0 → t = 0, z = 1 → t = π/4 [e] |
| C10.9 | (1 + z²)^{5/2} dz = sec⁵t · sec²t dt = sec⁷t dt [m] |
| C10.10 | z²(1 + z²)^{3/2} dz = tg²t · sec³t · sec²t dt = (sec²t − 1) sec⁵t dt = (sec⁷t − sec⁵t) dt [e] |
| C10.11 | SOBRA = (1/5)I₇ − (1/3)(I₇ − I₅) = (1/3)I₅ − (2/15)I₇, Iₙ = ∫₀^{π/4} secⁿt dt [m] |
| C10.12 | chip I₅ = 7√2/8 + (3/8) ln(1 + √2) (DAS CILÍNDRICAS) · cartão RECORRÊNCIA ∫secⁿ = secⁿ⁻² tg/(n − 1) + (n − 2)/(n − 1)∫secⁿ⁻² [e] |
| C10.13 | n = 7: I₇ = [(1/6) sec⁵t tg t]₀^{π/4} + (5/6) I₅ [m] |
| C10.14 | chips t = π/4: sec = √2, tg = 1 · t = 0: tg = 0 [e] |
| C10.15 | = (1/6)(√2)⁵ · 1 − 0 + (5/6)I₅ = 4√2/6 + (5/6)I₅ = 2√2/3 + (5/6)I₅ · chip (√2)⁵ = 4√2 [m] |
| C10.16 | SOBRA = (1/3)I₅ − (2/15)(2√2/3 + (5/6)I₅) = (1/3)I₅ − 4√2/45 − (1/9)I₅ = (2/9)I₅ − 4√2/45 [m] |
| C10.17 | (2/9)I₅ = (2/9)(7√2/8 + (3/8) ln(1 + √2)) = 7√2/36 + (1/12) ln(1 + √2) [m] |
| C10.18 | 7√2/36 − 4√2/45 = 35√2/180 − 16√2/180 = 19√2/180 [m] |
| C10.19 | ∫ EM z = 19√2/180 + (1/12) ln(1 + √2) + 1/45 [m] |
| C10.20 | I_z = 2π[(19√2 + 4)/180 + (1/12) ln(1 + √2)] = (π/90)(19√2 + 4 + 15 ln(1 + √2)) ≈ 1,539 (moldura) [m] |
| C10.21 | chip CONFERE: CARTESIANAS NO COMPUTADOR ≈ 1,5391 [e] |
| C10.22 | (B4-6) I/M ≈ 1,539/2,760 ≈ 0,558 R² · s_G = √0,558 ≈ 0,747 R (comum 0,5 e 0,707) [m] |

**C11 · reserva do gancho (não vai à tela).** lata homogênea, eixo x = R, y = 0: I = ∭ ((x − R)² + y²) k dV = (3/2) MR² = MR²/2 + MR² (Steiner). Fica para o 3.5-E1.

## 5. Duração e plano de corte

≈ 21:48 com tudo. Se o Kaio quiser perto de 18 min, o corte que menos machuca (sem tocar no gancho): tirar a bola (B3-4, 1:29) e levá-la para o 3.5-E1, encurtar o B3-5 para tubo × cilindro (−0:20) e tirar o contraexemplo ρ = 1 + x do B1-3 (−0:35, fica só a frase "a simetria tem que ser dos dois") → ≈ 19:20. Cortar a conta do I da lata pesada (B4-3 a B4-5, 3:27) quebraria a promessa do EP. 17: não recomendo.

## 6. Pontos para o Kaio

1. **Número:** `yt_0043` · EP. 18 (próximo livre depois do yt_0042 nas pautas; o GitHub está atrasado em relação ao K:).
2. **Dois chips vindos do EP. 17** (D10): a massa da lata (≈ 2,76) e a secante à quinta. Alternativa se não quiser depender do vídeo anterior: refazer a massa em 4 degraus (+1:00) e a sec⁵ em 5 (+1:10).
3. **Duração** (§5).

## 7. Verificação

`verificacao/verifica_calc3_35t4_sympy.py`: **62/62 True** (saída em `verifica_calc3_35t4_saida.txt`). Cobre cada degrau de C1–C11, a taça em cartesianas (z̄ = 2/3), o contraexemplo em cartesianas (π/4), I_z e M_xy da lata pesada por integração numérica em cartesianas (scipy tplquad: 1,5391 e 1,5318) e as identidades sec⁷/sec⁵.
Checagens objetivas: casos-limite (tubo fino s = R ⇒ MR²; lata homogênea ⇒ z̄ = 1/2, I = MR²/2 > comparação), unidade kg · m², ∭(z − z̄)ρ dV = 0 conferido na taça e na lata, z̄ da lata pesada dentro de (0,5; 1) e I/M dentro de (0,5; 1) como a física exige (densidade crescente para fora).
