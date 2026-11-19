# Cálculo III · 3.5-E1 · Exercícios do módulo: integral tripla · Proposta v1

> 2026-11-18. Unidade provisória **yt_0044 · CÁLCULO III · EP. 19** (segue o yt_0043 = EP. 18; a pasta `K:\...\videos_longos` vai até o yt_0043, então o 0044 está livre). Duração ≈ **28:56** (narração v1, 5.168 palavras a 3 p/s). O Kaio liberou passar dos 30 min (2026-11-18), então nada foi cortado.
> Matemática conferida no sympy: **94/94** (`verificacao/verifica_calc3_35e1_sympy.py` + saída), com conferências numéricas no scipy.

## 0. Identificação

| Campo | Valor |
|---|---|
| Série pública | CÁLCULO III · EP. 19 (provisório) |
| Título | Exercícios do módulo: integral tripla |
| Bloco | 3.5-E1 (integrador do módulo 3.5) |
| Entra | definição (soma de Riemann e conteúdo nulo) · redução à integral dupla · mudança de variáveis e esféricas · cilíndricas · centro de massa e momento de inércia |
| Referência | Guidorizzi vol. 3, cap. 5 (exercícios 5.4-3, 5.4-4, 5.7-4/6 como base dos E1, E2 e E5); didática do Stewart. Livro só na descrição |
| Notação | ρ densidade (ciano) · s distância ao eixo (pêssego) · r distância à origem (laranja) · R, h, L fixos · φ e α só nas esféricas · d distância entre eixos (lilás) |
| Gancho pago | o desafio do EP. 18: a lata girando pelo eixo na parede, **(3/2)MR²**, direto e por Steiner (E5 e E6) |
| Gancho deixado | a hélice na parede da lata e uma força ao longo dela ⇒ **integrais de linha** (3.6-T1). Desafio dos comentários: o cone girando por um diâmetro da tampa, (3/20)MR² + (1/10)Mh² (fora da tela) |

## 1. Ideia central

Uma receita em quatro perguntas (**onde está o corpo? qual sistema? entra e sai; conferir**) aplicada a seis problemas que começam parecidos e vão subindo. Cada problema termina com um **confere por outro caminho** (✓ menta): Riemann × Fubini, centroide × integral, cilíndricas × esféricas, esféricas × fatias, polo no centro × polo na dobradiça, Steiner × conta direta.

| Exercício | Corpo e pergunta | Assuntos do módulo | Confere por |
|---|---|---|---|
| E1 | cubo [0,1]³, ρ = x + y + z: massa, x̄, a folha z = 1 | definição (Riemann, limite das somas, conteúdo nulo), redução | soma de Riemann = Fubini; simetria |
| E2 | tetraedro x + y + z ≤ 1, ρ = x + y: massa e z̄ | redução à dupla (sombra), substituição, troca de ordem | centroide (densidade linear) |
| E3 | cone (h/R)s ≤ z ≤ h: V, z̄, I_z | cilíndricas, centro de massa, momento de inércia | volume em esféricas |
| E4 | meia bola: z̄; e com ρ = k r | esféricas | fatias; caso-limite "tudo na casca" |
| E5 | a lata na dobradiça | cilíndricas com polo deslocado | polo na dobradiça (s ≤ 2R cos θ) |
| E6 | Steiner em geral: cubo pela aresta, bola encostada, o erro clássico | teorema dos eixos paralelos | conta direta |

## 2. Estrutura (27 âncoras, ≈ 28:56)

| Bloco | Âncoras | Tempo |
|---|---|---:|
| Abertura | H1 a lata na dobradiça · H2 a receita · A1 bem-vindos | 2:04 |
| E1 cubo | E1-1 chute e Riemann · E1-2 o limite · E1-3 a conta exata · E1-4 x̄ · E1-5 a folha | 5:31 |
| E2 tetraedro | E2-1 sombra e sonda · E2-2 massa · E2-3 centroide · E2-4 z̄ trocando a ordem | 4:45 |
| E3 cone | E3-1 volume · E3-2 z̄ · E3-3 I_z · E3-4 volume em esféricas | 4:30 |
| E4 meia bola | E4-1 z̄ em esféricas · E4-2 fatias · E4-3 ρ = k r | 3:24 |
| E5 lata | E5-1 polo no centro · E5-2 três pedaços · E5-3 polo na dobradiça | 3:36 |
| E6 Steiner | E6-1 o teorema · E6-2 cubo pela aresta · E6-3 bola e o erro clássico | 3:28 |
| Fecho | S1 síntese · S2 hélice e o próximo vídeo | 1:37 |

O tempo de cada âncora está na narração v1.

## 3. Matemática: CONTA INTEIRA, degrau a degrau

Cada linha abaixo é uma linha da tela, nessa ordem. Os IDs batem com a verificação sympy. O LaTeX pronto, com as macros da série, está no `keys44.js` dos quadros-alvo (uma chave por alvo).

### C1 · E1 · o cubo 0 ≤ x, y, z ≤ 1, ρ = x + y + z
- C1.1 chute: ρ(centro)·V = (3/2)·1 = 3/2.
- C1.2 n = 2: Δx = Δy = Δz = 1/2, ΔV = 1/8; pontos médios: cada coordenada é 1/4 ou 3/4; cada coordenada soma 4·(1/4) + 4·(3/4) = 1 + 3 = 4; soma dos ρ = 3·4 = 12; Σ ρ ΔV = 12·(1/8) = 3/2.
- C1.3 canto de baixo: 3(4·0 + 4·½) = 6 → 6·⅛ = 3/4; canto de cima: 3(4·½ + 4·1) = 18 → 18·⅛ = 9/4.
- C1.4–C1.6 tabela n = 2, 4, 10: baixo 0,75 · 1,125 · 1,35; meio 1,5 sempre; cima 2,25 · 1,875 · 1,65.
- C1.7–C1.8 3/2 − 3/(2n) ≤ ∭ρ dV ≤ 3/2 + 3/(2n); cima − baixo = 3/n → 0 (Δ = 1/n → 0).
- C1.9 ∫₀¹(x+y+z)dz = [xz + yz + z²/2]₀¹ = x + y + 1/2.
- C1.10 ∫₀¹(x + y + 1/2)dy = [xy + y²/2 + y/2]₀¹ = x + 1/2 + 1/2 = x + 1.
- C1.11 ∫₀¹(x + 1)dx = [x²/2 + x]₀¹ = 1/2 + 1 = 3/2 ✓ (= Riemann).
- C1.12 simetria: trocar x por y não muda cubo nem ρ ⇒ x̄ = ȳ = z̄; M_yz = ∭x² + ∭xy + ∭xz; ∭x² = (1/3)·1·1 = 1/3; ∭xy = (1/2)(1/2)·1 = 1/4 (= ∭xz).
- C1.13–C1.15 M_yz = 1/3 + 1/4 + 1/4 = 4/12 + 3/12 + 3/12 = 10/12 = 5/6.
- C1.14 x̄ = (5/6)/(3/2) = (5/6)(2/3) = 10/18 = 5/9 ≈ 0,556; (x̄, ȳ, z̄) = (5/9, 5/9, 5/9).
- C1.16 a folha z = 1: ρ = x + y + 1 ≤ 3; 0 ≤ soma ≤ 3·(1·Δz) = 3Δz → 0 ⇒ ∭_folha ρ dV = 0 (sem ponto interior: volume zero).

### C2 · E2 · tetraedro x + y + z ≤ 1, x, y, z ≥ 0, ρ = x + y
- C2.1 sonda: z = 0 → z = 1 − x − y; sombra 0 ≤ x ≤ 1, 0 ≤ y ≤ 1 − x; M = ∫₀¹∫₀^{1−x}∫₀^{1−x−y}(x + y) dz dy dx.
- C2.2 ∫₀^{1−x−y}(x+y)dz = (x+y)[z]₀^{1−x−y} = (x+y)(1−x−y).
- C2.3 w = x + y (x parado): dw = dy; y = 0 → w = x; y = 1 − x → w = 1.
- C2.4–C2.5 ∫ₓ¹ w(1−w)dw = [w²/2 − w³/3]ₓ¹ = (1/2 − 1/3) − (x²/2 − x³/3) = 1/6 − x²/2 + x³/3.
- C2.6 M = ∫₀¹(1/6 − x²/2 + x³/3)dx = [x/6 − x³/6 + x⁴/12]₀¹ = 1/6 − 1/6 + 1/12 = **1/12**.
- C2.7–C2.8 confere: centroide = média dos 4 vértices = (1/4, 1/4, 1/4); ρ(centroide) = 1/2; V = (½·1·1)·1·⅓ = 1/6; ½·⅙ = 1/12 ✓.
- C2.9–C2.10 vale só para densidade linear: ∭(Ax+By+Cz+D)dV = V·(valor no centroide). ALERTA: ρ = x² dá 1/60, não 1/96.
- C2.11–C2.13 M_xy = ∫₀¹∫ₓ¹ ½ w(1−w)² dw dx; troca a ordem (0 ≤ x ≤ w ≤ 1): = ∫₀¹ ½ w(1−w)²(∫₀ʷ dx)dw = ∫₀¹ ½ w²(1−w)² dw.
- C2.14 w²(1−w)² = w² − 2w³ + w⁴; ∫₀¹ = [w³/3 − w⁴/2 + w⁵/5]₀¹ = 1/3 − 1/2 + 1/5 = 10/30 − 15/30 + 6/30 = 1/30.
- C2.15–C2.16 M_xy = ½·1/30 = 1/60; z̄ = (1/60)/(1/12) = 12/60 = **1/5** (abaixo do centroide 1/4: a ponta de cima é leve).

### C3 · E3 · cone (h/R)s ≤ z ≤ h, ρ = k
- C3.1 entra na parede z = (h/R)s, sai na tampa z = h; sombra 0 ≤ s ≤ R, 0 ≤ θ ≤ 2π; dV = s ds dθ dz.
- C3.2 ∫_{hs/R}^h s dz = s[z]_{hs/R}^h = s(h − hs/R) = hs − (h/R)s².
- C3.3 ∫₀^R(hs − (h/R)s²)ds = [hs²/2 − (h/R)s³/3]₀^R = hR²/2 − hR²/3 = hR²/6.
- C3.4 V = 2π·hR²/6 = **πR²h/3** (um terço do cilindro).
- C3.5 ∫ z s dz = s[z²/2]_{hs/R}^h = s(h²/2 − h²s²/(2R²)) = h²s/2 − h²s³/(2R²).
- C3.6 ∫₀^R(...)ds = [h²s²/4 − h²s⁴/(8R²)]₀^R = h²R²/4 − h²R²/8 = h²R²/8.
- C3.7–C3.8 ∭z dV = 2π·h²R²/8 = πR²h²/4; z̄ = (πR²h²/4)/(πR²h/3) = **3h/4** do vértice (h/4 da tampa).
- C3.9 ∫ s³ dz = s³(h − hs/R) = hs³ − (h/R)s⁴ (s² da distância · s do fator = s³).
- C3.10 ∫₀^R(hs³ − (h/R)s⁴)ds = hR⁴/4 − hR⁴/5 = hR⁴/20.
- C3.11–C3.12 I_z = k·2π·hR⁴/20 = πkR⁴h/10; M = kπR²h/3; I_z = **(3/10)MR²** (cilindro 1/2: a massa do cone mora perto do eixo).
- C3.14 esféricas: 0 ≤ φ ≤ α, tg α = R/h; tampa z = h ⇒ r cos φ = h ⇒ r = h/cos φ.
- C3.15 ∫₀^{h/cos φ} r² dr = h³/(3cos³φ).
- C3.16 u = cos φ, du = −sen φ dφ; φ = 0 → u = 1; φ = α → u = cos α; (h³/3)∫₀^α sen φ/cos³φ dφ = (h³/3)∫₁^{cos α} −u⁻³ du = (h³/3)[u⁻²/2]₁^{cos α}.
- C3.17 = (h³/3)·(1/cos²α − 1)/2 = (h³/3)·tg²α/2 = (h³/3)·R²/(2h²) = hR²/6.
- C3.18 V = 2π·hR²/6 = πR²h/3 ✓ (o mesmo hR²/6).

### C4 · E4 · meia bola 0 ≤ r ≤ R, 0 ≤ φ ≤ π/2
- C4.1 M = k·2π·[−cos φ]₀^{π/2}·R³/3 = k·2π·1·R³/3 = (2/3)πkR³ (com [−cos φ]₀^{π/2} = 0 − (−1) = 1).
- C4.2 z = r cos φ; M_xy = k∭ r cos φ · r² sen φ dr dφ dθ = k·2π·(∫₀^{π/2} sen φ cos φ dφ)·R⁴/4.
- C4.3 ∫₀^{π/2} sen φ cos φ dφ = [sen²φ/2]₀^{π/2} = 1/2 − 0 = 1/2.
- C4.4–C4.5 M_xy = k·2π·½·R⁴/4 = πkR⁴/4; z̄ = (πkR⁴/4)/((2/3)πkR³) = (1/4)/(2/3)·R = **3R/8**.
- C4.6–C4.8 fatias: disco de raio √(R² − z²), área π(R² − z²); ∭z dV = ∫₀^R z·π(R² − z²)dz = π[R²z²/2 − z⁴/4]₀^R = π(R⁴/2 − R⁴/4) = πR⁴/4 ✓; V = π[R²z − z³/3]₀^R = 2πR³/3 ✓; z̄ = 3R/8 ✓.
- C4.9–C4.11 ρ = k r: M = k·2π·1·R⁴/4 = πkR⁴/2; M_xy = k·2π·½·R⁵/5 = πkR⁵/5; z̄ = (πkR⁵/5)/(πkR⁴/2) = **2R/5**; 3R/8 = 0,375R < 2R/5 = 0,4R.
- C4.13–C4.14 caso-limite tudo na casca: z̄ = R/2 (só na tela, como chip; a fórmula geral (n+3)R/(2(n+4)) fica fora).

### C5 · E5 · a lata na dobradiça: (x − R)² + y² ≤ R², 0 ≤ z ≤ h, ρ = k
- C5.1 eixo de giro = eixo z; I_z = ∭(x² + y²)k dV; polo no centro da lata: x = R + s cos θ, y = s sen θ, z = z; o fator continua s.
- C5.2 x² + y² = (R + s cos θ)² + (s sen θ)² = R² + 2Rs cos θ + s²cos²θ + s²sen²θ = R² + 2Rs cos θ + s².
- C5.3 ① kR²∭s dz ds dθ = R²·(kπR²h) = MR².
- C5.4 ② 2kR(∫₀^{2π}cos θ dθ)(∫₀^R s² ds)(∫₀^h dz) = 2kR·0·… = 0.
- C5.5 ③ k∭s²·s dz ds dθ = k·h·R⁴/4·2π = πkR⁴h/2 = MR²/2.
- C5.6 I_z = MR² + 0 + MR²/2 = **(3/2)MR²** (três vezes o giro pelo centro).
- C5.7 polo na dobradiça: (x−R)² + y² ≤ R² ⇔ x² + y² ≤ 2Rx ⇔ s² ≤ 2Rs cos θ ⇔ s ≤ 2R cos θ, −π/2 ≤ θ ≤ π/2.
- C5.8 ∫₀^{2R cos θ} s³ ds = (2R cos θ)⁴/4 = 4R⁴cos⁴θ.
- C5.9–C5.10 cos⁴θ = ((1 + cos 2θ)/2)² = (1 + 2cos 2θ + cos²2θ)/4; cos²2θ = (1 + cos 4θ)/2 ⇒ cos⁴θ = 3/8 + ½cos 2θ + ⅛cos 4θ.
- C5.11 ∫_{−π/2}^{π/2}cos⁴θ dθ = [3θ/8 + sen 2θ/4 + sen 4θ/32] = 3π/8 + 0 + 0.
- C5.12 I_z = k·h·4R⁴·3π/8 = (3/2)(kπR²h)R² = (3/2)MR² ✓.

### C6 · E6 · Steiner
- C6.1 CM na origem, eixo novo paralelo ao z por (d, 0): I = ∭((x − d)² + y²)dm; (x − d)² + y² = (x² + y²) − 2dx + d².
- C6.2 I = ∭(x² + y²)dm − 2d∭x dm + d²∭dm = I_cm − 2d·Mx̄ + Md²; x̄ = 0 ⇒ **I = I_cm + Md²**.
- C6.3–C6.4 cubo de aresta L centrado: ∭x² dV = [x³/3]_{−L/2}^{L/2}·L² = (L³/24 + L³/24)L² = L⁵/12; I_cm = k(L⁵/12 + L⁵/12) = kL⁵/6 = ML²/6.
- C6.5–C6.6 d = L/√2 (meia diagonal da face) ⇒ d² = L²/2; I_aresta = ML²/6 + ML²/2 = ML²/6 + 3ML²/6 = 4ML²/6 = **(2/3)ML²**.
- C6.7 confere direto: k∫₀^L∫₀^L∫₀^L(x² + y²)dz dy dx = k(L⁵/3 + L⁵/3) = (2/3)ML² ✓.
- C6.8 bola, eixo tangente: (2/5)MR² + MR² = **(7/5)MR²**.
- C6.10 ✗ erro clássico (lata, parede A → parede oposta B): I_B = I_A + M(2R)² = (3/2 + 4)MR² = (11/2)MR².
- C6.12 ✓ volta ao centro: I_cm = I_A − MR² = (3/2 − 1)MR² = MR²/2; vai à outra parede: I_B = MR²/2 + MR² = (3/2)MR².
- C6.13 (reserva, desafio dos comentários, não vai à tela) cone por um diâmetro da tampa: (3/20)MR² + (1/10)Mh².

## 4. Direção visual

- Fundo da série Cálculo: violeta liso com papel de borda a borda (também sob o 3D); só o CTA liso. Sistema 3D G1–G6 do yt_0041 em diante.
- **Three.js** para tudo que precisa de câmera: cubo (densidade, caixinhas, sonda, diagonal, folha), tetraedro (sonda, centroide), cone (volume, CM, casca), meia bola (octante aberto, fatia), lata (parede, dobradiça), hélice. Câmeras fixas por bloco.
- **Manim 2D** onde o 2D explica melhor: a régua das somas do E1-2, o triângulo (x, w) do E2-4, o corte do cone em esféricas do E3-4, os dois cortes do E4-3, as vistas de cima do E5-1/E5-3 e do E6, a receita, a síntese.
- Cores fixas: s `#FFC08A`, θ `#2EE6A6`, z `#5AA2FF`, x `#FFC24D`, y `#EA63FF`, r `#FF9440`, φ/α `#B48CFF`, ρ `#35D9FF`, fator do volume lima `#C6F26B`, u/w `#E08A3C`, d lilás `#B9A6FF`, ALERTA `#FF5D5D`, GEO `#B8C4DA`, menta `#8CFFD2`, entrada `#7FB2FF`, saída `#FF7A8A`, hélice `#FFB36B`, ⊕ do CM com degradê ciano → magenta.
- Sem efeitos. Destaque = sublinhado fino ou contorno que acende e apaga.
- 26 quadros-alvo em `yt_0044_quadros_alvo_v1/` (+ folha de contato). Os alvos fixam posição, tamanho, câmera e cor; o caminho até eles segue os gatilhos da narração.

## 5. Plano de corte (se o Kaio quiser encurtar)

Nada cortado na v1 (liberado passar de 30 min). Se precisar: E4-3 (ρ = k r) −1:01; E6-2 (cubo pela aresta) −1:07; E1-2 reduzido à tabela −0:40 ⇒ ≈ 26:08. **Não cortar** E5 (paga o gancho) nem E1-5 (conteúdo nulo é o único lugar do módulo inteiro em que ele reaparece).

## 6. Decisões

1. A lata da dobradiça abre (H1) e fecha o arco (E5 + E6-3), pagando o desafio do EP. 18 duas vezes: conta inteira e Steiner.
2. Polo deslocado (x = R + s cos θ) como caminho principal, porque o atalho de Steiner **aparece sozinho** nos três pedaços; o polo na dobradiça (s ≤ 2R cos θ, cos⁴) é a conferência.
3. O "chute do centroide" aparece duas vezes: acerta no cubo e no tetraedro (densidade linear) e falha com ρ = x² (ALERTA), para o aluno não generalizar.
4. A folha z = 1 (E1-5) mostra o conteúdo nulo em ação: tampa, parede e costura não mudam a integral.
5. O erro clássico do Steiner entre dois eixos fora do CM vai para a tela com ✗ e a correção ✓.
6. O resultado (3/20)MR² + (1/10)Mh² do desafio final não aparece na tela.
7. Nenhum vídeo não publicado é citado: só "nas cilíndricas", "a gente já sabe".

## 7. Para o Kaio

- Confirmar **yt_0044 · EP. 19**.
- Duração ≈ 28:56 (liberada acima de 30 min).
- O próximo vídeo (3.6-T1, integrais de linha) precisa abrir com a hélice na parede da lata e a força que empurra a conta (gancho do S2).

## Anexo A · Narração

`yt_0044_narracao_v1.md` (27 âncoras, Tela/Coluna/Gatilhos/fala; 176 gatilhos conferidos por script).

## Anexo B · Leitura dos símbolos na fala

x barra, z barra; "rô" só para a densidade; "téta", "fi", "alfa"; s, r, R, h, k, d, L, M, I lidos como letra; M_xy = "M x y"; I_cm = "I do centro de massa"; ∭ = "a integral tripla"; Δ = "delta".
