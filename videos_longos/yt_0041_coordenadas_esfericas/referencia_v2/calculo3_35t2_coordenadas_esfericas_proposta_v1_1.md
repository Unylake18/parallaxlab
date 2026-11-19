# Longo · Coordenadas esféricas na integral tripla (Cálculo III · 3.5-T2) · proposta v1.1

Planejamento da Produção, 2026-11-15. Guidorizzi vol. 3 primeiro (§5.5, coordenadas esféricas; o teorema de mudança de variáveis na tripla), Stewart para a didática (§15.8: a "cunha esférica" e a casquinha de sorvete). Nenhum número depende do Stewart: o PDF dele tem ~1 GB e não foi aberto.

**v1.1 (2026-11-15):** a notação passou a ser a dos vídeos da lei de Gauss, por decisão do Kaio: ρ = densidade, r = distância ao centro, R = raio fixo, s = sombra no chão. Nenhum número mudou. A fala ganhou uma frase no B1-1 avisando que os livros de Cálculo chamam a distância de rô. Os quadros-alvo foram refeitos com as letras novas.

Arquivos desta entrega, todos em `pautas/`:
- esta proposta;
- `verificacao/verifica_calc3_35t2_sympy.py` + `verifica_calc3_35t2_saida.txt` (**63/63 True**);
- `yt_0041_quadros_alvo_v1_1/` (14 quadros-alvo + `00_folha_contato_v1.jpg`, o gerador `sb41.html` + `shot.js` e a cena Three.js de referência `c3d41.html` + `r3d.js`, com os PNGs e `r3d_pts.json` das 11 cenas);
- `yt_0041_narracao_v1_1.md` (o Anexo A em arquivo separado);
- `yt_0041_handoff_v1_1.md` + `yt0041_handoff_v1_1_completo.zip` (preview 540p15 silencioso).

## 0. Identificação

| Campo | Valor |
|---|---|
| Unidade | `yt_0041` · `longo_horizontal` · `teoria_visual` |
| Mapa | Cálculo III · 3.5 · **3.5-T2 Coordenadas esféricas**. Antes: 3.5-T1 Integral tripla e redução à dupla. Depois: 3.5-T3 Coordenadas cilíndricas |
| Referência | Guidorizzi vol. 3, §5.5: x = r sen φ cos θ, y = r sen φ sen θ, z = r cos φ, o jacobiano r² sen φ, o teorema com T(B̊) = B̊, T injetora e J ≠ 0 no interior; Ex. 5 (a bola com densidade igual à distância ao centro, M = π) e Exercício 5.5-4 (cone + esfera x² + y² + z² = 2z, aqui com a = 1). O gancho usa §5.6 Ex. 1 (a lata, em cilíndricas). Stewart §15.8 para a cunha esférica com três arestas e a casquinha |
| Série pública | CÁLCULO III · **EP. 16** (confirmado pelo Kaio em 2026-11-15: yt_0039 = EP. 14, yt_0040 = EP. 15) |
| Tag do canto | `CÁLCULO III · INTEGRAL TRIPLA` |
| Pergunta central | Qual é o volume de um pedaço da grade de cascas, cones e páginas, e por que ele é r² sen φ? |
| Promessa | Entender o endereço esférico, tirar o fator r² sen φ por três caminhos e calcular três integrais que travam em cartesianas: a bola (4πR³/3), a bola pesada (M = π) e a casquinha (V = π) |
| Duração | **3.538 palavras ≈ 19:49** (tabela no Anexo A, medida por script). Plano de corte para ≈ 16:00 no §5 |
| `solido_3d:` | nenhum do arsenal Blender |
| `3d_threejs:` | **11 cenas** em `c3d41.html`: `bola` (degradê radial de densidade, cunha de 90°), `grade` (esfera em traço + células do polo e do equador), `superf` (cone, página e meia casca), `ponto` (P com a página e a sombra), `caixa` e `caixa2` (a caixa rφθ inteira e partida em θ = π), `bolagrade` (a bola com a costura e o eixo), `caixinha` (a célula com as três arestas), `cebola` (uma casca), `casquinha` (cone + calota, sonda), `lata` (as duas sondas) |
| Notação | **Igual aos vídeos da lei de Gauss** (decisão do Kaio, 2026-11-15): **ρ = densidade, r = distância ao centro, R = raio fixo da bola** (no lugar do a), **s = r sen φ = a sombra no chão** (o s do Griffiths). φ é o ângulo a partir de +z, como no Guidorizzi; a transformação se chama **T**. O Guidorizzi e o Stewart chamam a distância de ρ: a fala avisa uma vez no B1-1 |

**Cobre:**
- o endereço (r, φ, θ), com o triângulo da página e a sombra s = r sen φ;
- a transformação T: a caixa [0, R] × [0, π] × [0, 2π] vira a bola, com as três bordas ruins;
- o fator r² sen φ por três caminhos (arestas, duas polares em sequência, determinante 3×3 por Laplace);
- o teste da bola e os dois erros clássicos (sem r²: metro; sem sen φ: número errado com unidade certa);
- o teorema com as hipóteses do Guidorizzi, aplicado à bola em duas metades;
- a receita com a sonda radial;
- a cebola: ∫∫ r² sen φ dφ dθ = 4πr² (área = derivada do volume);
- a bola pesada do hook (M = π, média 3/4, metade da massa além de 0,84);
- a casquinha (V = π, com substituição e limites novos; conferida pela geometria);
- quando usar e quando não usar esféricas.

**Fora (reserva do 3.5-E1):**
- a gaussiana 3D ∭ e^{−(x²+y²+z²)} = π^{3/2};
- Guidorizzi §5.5 Ex. 7, 8 e 9 (calotas, regiões entre esferas e cones);
- as transformações lineares do §5.4, Ex. 1 e 2;
- o centro de massa da semibola (vai bem no exercício integrador).

## 1. Ideia central

**Em coordenadas esféricas, a grade vira cascas, cones e páginas, e o pedacinho de volume é r² sen φ dr dφ dθ: cresce com o quadrado da distância e encolhe perto dos polos. É o jacobiano de T, e é ele que transforma bolas e cones em caixas.**

Frases de tela: `dV = r² sen φ dr dφ dθ` e `A GRADE CERTA SIMPLIFICA A REGIÃO`.

**Arco narrativo** (o mesmo das polares):
1. A pergunta: a bola pesada trava, e qual é o volume de cada pedaço da grade nova?
2. A ferramenta: o endereço, o fator por três caminhos e o teorema.
3. A conquista: a bola pesada do começo sai em três linhas.
4. A aplicação: a casquinha, com substituição.
5. O limite da ferramenta: a lata racha, e isso puxa as cilíndricas.

### Definição ↔ figura (toda definição formal com figura própria)

| # | Enunciado | Figura | Bloco |
|---|---|---|---|
| D1 | r = distância até a origem; φ = ângulo a partir de +z, em [0, π]; θ = ângulo das polares, em [0, 2π] | P com o segmento r, o arco φ junto do eixo z, o arco θ no chão (alvo 03) | B1-1 |
| D2 | z = r cos φ, s = r sen φ, x = r sen φ cos θ, y = r sen φ sen θ | A página com o triângulo retângulo e a sombra s no chão (alvo 03) | B1-1 |
| D3 | x² + y² + z² = r²; (2, π/6, π/3) ↦ (1/2, √3/2, √3) | O mesmo desenho com os números (alvo 04) | B1-2 |
| D4 | T(r, φ, θ) = (x, y, z); a caixa vira a bola; r = 0 → origem; φ = 0, π → eixo z; θ = 0, 2π → mesma página | Caixa rφθ e bola, com a mesma célula lima e as bordas ruins em ALERTA (alvo 05) | B1-3 |
| D5 | ΔV ≈ Δr · rΔφ · r sen φ Δθ = r² sen φ Δr Δφ Δθ | A caixinha curva com as três arestas nas cores das variáveis (alvo 06) | B2-1 |
| D6 | composição de duas polares: fator r (página) × fator s (chão) = r² sen φ | Dois painéis 2D, página e chão (alvo 07) | B2-2 |
| D7 | ∂(x, y, z)/∂(r, φ, θ) = r² sen φ ≥ 0 | A matriz 3×3 com a linha de baixo acesa (alvo 08) | B2-3 |
| D8 | Teorema (Guidorizzi): T de classe C¹, B_rφθ compacto com fronteira de conteúdo nulo, T(interior) = interior, T injetora e J ≠ 0 no interior | O enunciado + a caixa partida em θ = π e a bola em duas metades (alvo 10) | B3-1 |
| D9 | Receita: θ e φ por números, r pela sonda radial (entra/sai) | A sonda saindo da origem, entra azul-claro, sai coral | B3-2 |
| D10 | ∫∫ r² sen φ dφ dθ = 4πr² | Uma casca laranja (alvo 11) | B4 |
| D11 | cone φ = π/4; esfera r = 2 cos φ | A casquinha 3D com a sonda (alvo 13) | B6-1 |
| D12 | lata: r = 1/sen φ (parede), r = 1/cos φ (tampa), racha em φ = π/4 | A lata com as duas sondas (alvo 14) | S2 |

## 2. Estrutura

| Bloco | Âncoras | Voz | Conteúdo | Alvo |
|---|---|---:|---|---|
| H | H1–H2 | 1:32 | A bola pesada trava; a grade nova e a pergunta | 01, 02 |
| A | A1 | 0:16 | Bem-vindos | — |
| B1 | B1-1 a B1-3 | 3:14 | O endereço, o ponto de exemplo, a caixa vira a bola | 03, 04, 05 |
| B2 | B2-1 a B2-4 | 5:32 | O fator por três caminhos e o teste da bola | 06, 07, 08, 09 |
| B3 | B3-1, B3-2 | 2:00 | O teorema (duas metades) e a receita | 10 |
| B4 | B4 | 1:02 | A cebola: área da esfera | 11 |
| B5 | B5 | 1:35 | A bola pesada: M = π | 12 |
| B6 | B6-1, B6-2 | 2:52 | A casquinha | 13 |
| B7 | B7 | 0:27 | Quando usar | — |
| S | S1, S2 | 1:20 | Síntese; a lata; próximo vídeo; CTA | 14 |

## 3. Matemática e a conta inteira

Todos os números estão no script sympy (63/63; IDs entre colchetes). O script usa ρ para a distância e a para o raio fixo (a notação dos livros); o vídeo usa r e R.

### A conta inteira (texto exato da coluna)

Cores: r laranja `#FF9440`, φ violeta `#B48CFF`, θ verde-água `#2EE6A6`, a sombra s pêssego `#FFC08A`, x âmbar `#FFC24D`, y magenta `#EA63FF`, z azul `#5AA2FF`, o fator **r² sen φ lima `#C6F26B` em todas as linhas**, a densidade ρ ciano `#35D9FF`, u `#E08A3C`, entrada azul-claro `#7FB2FF`, saída coral `#FF7A8A`, ALERTA `#FF5D5D`, moldura do resultado menta `#8CFFD2`.

**C1 · H1, a trava (alvo 01)** [H1a]
1. `DENSIDADE ρ = √(x² + y² + z²)`
2. `MASSA = ∭_B √(x² + y² + z²) dV`
3. `= ∫_{−1}^{1} ∫_{−√(1−x²)}^{√(1−x²)} ∫_{−√(1−x²−y²)}^{√(1−x²−y²)} √(x² + y² + z²) dz dy dx`
4. `∫ √(k² + z²) dz = ½[z√(k² + z²) + k² ln(z + √(k² + z²))]`, `COM k² = x² + y²`
5. selo `TRAVA` + `RAIZ E LOGARITMO JÁ NA DE DENTRO`

**C2 · B1-1, o endereço (alvo 03)** [B1f, B1g]
1. `z = r cos φ`
2. `s = r sen φ` + `SOMBRA NO CHÃO`
3. `x = s cos θ = r sen φ cos θ`
4. `y = s sen θ = r sen φ sen θ`
5. `r ≥ 0, 0 ≤ φ ≤ π, 0 ≤ θ ≤ 2π`

**C3 · B1-2, o ponto (alvo 04)** [B1a–B1e]
1. `(r, φ, θ) = (2, π/6, π/3)`
2. `z = 2 cos(π/6) = 2 · √3/2 = √3`
3. `s = 2 sen(π/6) = 2 · 1/2 = 1`
4. `x = 1 · cos(π/3) = 1/2`, `y = 1 · sen(π/3) = √3/2`
5. `x² + y² + z² = 1/4 + 3/4 + 3 = 4 = 2²` ✓
6. chip `x² + y² + z² = r²`

**C4 · B2-1, as arestas e os dois pedaços (alvo 06)** [B2a–B2g]
1. `ARESTA 1 Δr` · `ARESTA 2 rΔφ (ARCO = RAIO · ÂNGULO)` · `ARESTA 3 (r sen φ)Δθ (RAIO DO PARALELO)`
2. `ΔV ≈ Δr · rΔφ · r sen φ Δθ`
3. `= r² sen φ Δr Δφ Δθ`
4. painel: `Δr = 1/2, Δφ = Δθ = π/6, r̄ = 3/4`
5. `POLO (3/4)² · sen(π/12) · 1/2 · π/6 · π/6 ≈ 0,020` (exato: (7π/144)(1 − √3/2) ≈ 0,0205)
6. `EQUADOR (3/4)² · sen(5π/12) · 1/2 · π/6 · π/6 ≈ 0,075` (exato: 7π/288 ≈ 0,0764)
7. `RAZÃO sen(5π/12)/sen(π/12) = 2 + √3 ≈ 3,7`

As aproximações usam o ponto do meio, como a fala diz. A razão das aproximações é exatamente 2 + √3; a razão exata das células também é 2 + √3 (≈ 3,73) [B2f, B2g].

**C5 · B2-2, duas polares (alvo 07)** [B2h–B2j]
1. página: `|cos φ  −r sen φ ; sen φ  r cos φ| = cos φ · r cos φ − (−r sen φ) · sen φ = r cos²φ + r sen²φ = r`
2. chão: `FATOR s`
3. `r · s = r · r sen φ = r² sen φ`

**C6 · B2-3, o determinante (alvo 08)** [B2k–B2t]
1. `∂(x, y, z)/∂(r, φ, θ) = | sen φ cos θ   r cos φ cos θ   −r sen φ sen θ ; sen φ sen θ   r cos φ sen θ   r sen φ cos θ ; cos φ   −r sen φ   0 |`
2. `LINHA DE BAIXO: + − +`
3. `= cos φ · r² cos φ sen φ (cos²θ + sen²θ) − (−r sen φ) · r sen²φ (cos²θ + sen²θ) + 0`, com as duas chaves `= 1`
4. `= r² sen φ cos²φ + r² sen³φ`
5. `= r² sen φ (cos²φ + sen²φ) = r² sen φ` (chave `= 1`, moldura menta)
6. chip `dV = r² sen φ dr dφ dθ`; legenda `0 ≤ φ ≤ π: SEN φ ≥ 0, O MÓDULO NÃO MUDA NADA`

Os dois menores, se a fala ou o QA pedirem a linha extra: `M₃₁ = r cos φ cos θ · r sen φ cos θ − (−r sen φ sen θ) · r cos φ sen θ = r² sen φ cos φ (cos²θ + sen²θ)` e `M₃₂ = sen φ cos θ · r sen φ cos θ − (−r sen φ sen θ) · sen φ sen θ = r sen²φ (cos²θ + sen²θ)`. No vídeo, cada menor é sublinhado na matriz no instante em que o termo dele é escrito. A ordem (θ, r, φ) do Guidorizzi dá o mesmo +r² sen φ [B2t].

**C7 · B2-4, o teste da bola (alvo 09)** [B2u–B2z2]
1. `V = ∫₀^{2π} ∫₀^π ∫₀^R r² sen φ dr dφ dθ`
2. `∫₀^R r² dr = [r³/3]₀^R = R³/3` (a fala diz "menos zero")
3. `∫₀^π sen φ dφ = [−cos φ]₀^π = −cos π − (−cos 0) = 1 + 1 = 2`
4. `∫₀^{2π} dθ = 2π`
5. `V = R³/3 · 2 · 2π = 4πR³/3` ✓
6. `SEM r² ⇒ R · 2 · 2π = 4πR` + `METRO` ✗
7. `SEM sen φ ⇒ R³/3 · π · 2π = 2π²R³/3 ≈ 6,58 R³` ✗ + `UNIDADE CERTA, NÚMERO ERRADO (O CERTO ≈ 4,19 R³)`

**C7b · B3-1, o teorema (alvo 10)** [B3a, B3b]
1. `T: Ω ⊂ ℝ³ → ℝ³ DE CLASSE C¹ · B_uvw COMPACTO, FRONTEIRA DE CONTEÚDO NULO`
2. `NO INTERIOR: T(B̊_uvw) = B̊ · T INJETORA · ∂(x, y, z)/∂(u, v, w) ≠ 0`
3. `∭_B f(x, y, z) dx dy dz = ∭_{B_uvw} f(T(u, v, w)) |∂(x, y, z)/∂(u, v, w)| du dv dw`
4. glyph map para o caso esférico (não está no alvo): `∭_B f dx dy dz = ∭_{B_rφθ} f(T(r, φ, θ)) r² sen φ dr dφ dθ`
5. legendas `METADE θ ≤ π`, `METADE θ ≥ π`, `O CORTE: VOLUME ZERO`

**C8 · B4, a cebola (alvo 11)** [B4a–B4c]
1. `∫₀^{2π} ∫₀^π r² sen φ dφ dθ = r² · [−cos φ]₀^π · [θ]₀^{2π}`
2. `= r² · 2 · 2π = 4πr²` + `ÁREA DA ESFERA`
3. `V = ∫₀^R 4πr² dr = 4π[r³/3]₀^R = 4πR³/3`
4. `d/dR (4πR³/3) = 4πR²` + `ENGORDAR = UMA CASCA`
5. `ρ SÓ DE r: ∭ ρ dV = ∫₀^R ρ(r) 4πr² dr` (não está no alvo)

**C9 · B5, a bola pesada (alvo 12)** [B5a–B5f]
Etapa 1:
1. `ρ = √(x² + y² + z²) = √(r²) = r (r ≥ 0)`
2. `M = ∫₀^{2π} ∫₀^π ∫₀^1 r · r² sen φ dr dφ dθ` (chaves `DENSIDADE` ciano e `JACOBIANO` lima)
3. `= ∫₀^{2π} ∫₀^π ∫₀^1 r³ sen φ dr dφ dθ` (não está no alvo)
4. `= [r⁴/4]₀^1 · [−cos φ]₀^π · [θ]₀^{2π}`
5. `= (1/4 − 0) · (1 + 1) · (2π − 0) = π` ✓
6. `CONFERE: CARTESIANAS NO COMPUTADOR = 3,14159…` (não está no alvo)

Etapa 2 (a coluna sobe):
7. `MÉDIA M/V = π/(4π/3) = π · 3/(4π) = 3/4`
8. `MASSA ATÉ c: c⁴/4 · 2 · 2π = πc⁴` (não está no alvo)
9. `πc⁴ = π/2 ⇒ c⁴ = 1/2 ⇒ c = ⁴√(1/2) ≈ 0,84` (o alvo tem a forma curta `πc⁴ = π/2 ⇒ c = ⁴√(1/2) ≈ 0,84`)

**C10 · B6, a casquinha (alvo 13)** [B6a–B6n]
1. `CONE r cos φ = r sen φ ⇒ tg φ = 1 ⇒ φ = π/4`
2. `ESFERA r² = 2r cos φ ⇒ r = 2 cos φ` (legenda `x² + y² + (z − 1)² = 1`)
3. `V = ∫₀^{2π} ∫₀^{π/4} ∫₀^{2 cos φ} r² sen φ dr dφ dθ`
4. `[r³/3]₀^{2 cos φ} sen φ = (8 cos³φ/3 − 0) sen φ = (8/3) cos³φ sen φ`
5. `u = cos φ, du = −sen φ dφ` · `φ = 0 → u = 1, φ = π/4 → u = √2/2`
6. `∫₀^{π/4} (8/3) cos³φ sen φ dφ = (8/3) ∫_{√2/2}^{1} u³ du` (o sinal de du inverte os limites; glyph map)
7. `= (8/3) [u⁴/4]_{√2/2}^{1} = (8/3)(1/4 − 1/16)` (com `(√2/2)⁴ = 4/16 = 1/4`, `÷ 4 = 1/16`)
8. `= (8/3) · (3/16) = 1/2`
9. `V = 2π · 1/2 = π` ✓
10. `CONFERE π/3 + 2π/3 = π` + `CONE + MEIA BOLA`

O encontro: `r = 2 cos(π/4) = √2`, `(s, z) = (1, 1)` [B6d]. Conferido também em cilíndricas [B6m].

### Pontos de rigor
- **φ de 0 a π, não 2π.** O ponto do outro lado do eixo já tem outro θ. A fala do B1-1 explica isso.
- **Fronteira de conteúdo nulo e duas metades.** T leva o interior da caixa (0, a) × (0, π) × (0, 2π) na bola sem a página θ = 0 e sem o eixo z; a página está no interior da bola, então T(interior) ≠ interior. Em cada metade, θ ∈ (0, π) e θ ∈ (π, 2π), T(interior) é exatamente o interior da meia bola (conferido por amostragem [B3a]), T é injetora e J = r² sen φ > 0 [B3b]. O corte, a origem e o eixo têm volume zero, e a aditividade soma as metades. É o mesmo argumento das polares (disco em duas metades).
- **O módulo do jacobiano.** sen φ ≥ 0 em [0, π], então |J| = r² sen φ. Se alguém usar φ a partir do plano xy (latitude), o fator vira r² cos φ: o vídeo não usa essa convenção e não a menciona.
- **Δ e d.** Na caixinha, `ΔV ≈`; no teorema e daí em diante, `dV =`. Nada de `dV ≈`.
- **A primitiva do H1 existe** (com ln) e é elementar; o problema é que as duas integrais de fora ficam muito pesadas. A tela diz `TRAVA` (trava a conta à mão), nunca `SEM PRIMITIVA`.
- **A razão 2 + √3** vale tanto para as aproximações quanto para as células exatas, porque o fator em φ é ∫ sen φ dφ = cos φ₁ − cos φ₂, e (cos π/3 − cos π/2)/(cos 0 − cos π/6) = (1/2)/(1 − √3/2) = 2 + √3.
- **Notação de Gauss.** ρ é sempre densidade, r a distância, R o raio fixo, s a sombra. Nenhuma linha usa δ ou a.

## 4. Direção visual

**Layouts** (os mesmos da série): palco 3D + coluna (H1, H2, B1-1, B1-2, B1-3, B2-1, B4, B5, B6, S2), 2D em dois painéis (B2-2) e coluna larga 2D (B2-3, B2-4, B3-1).

**Grade:** toda cena 2D com o papel de borda a borda (papelTela; `papel(passo=0.5)` quando não há eixos, `papel(ax)` sem `area` quando há eixos). Só o 3D Three.js e o cartão do CTA ficam lisos. Painéis por cima do papel com fundo opaco.

**3D (Three.js, cena por quadro + `timeline.json` dos pontos):**
- **sem transparência, sem brilho, sem sombra projetada:** faces com tom chapado fixo por normal (luz fixa `LDIR = (0,55; −0,75; 0,45)`);
- **a peça nunca se separa:** o que fica fora do corte vira traço `#6C7698`; a cunha de 90° é aberta voltada para a câmera;
- a bola do H1 e do B5 tem o degradê radial da densidade (escuro no centro → ciano na casca), sem halo;
- as células são lima com contorno escuro; as arestas da caixinha são tubos finos nas cores das variáveis;
- a câmera gira devagar só no H1 e no B6-1, e para exatamente no quadro do alvo antes de a coluna começar;
- rótulos, setas, números e fórmulas são do Manim, presos aos pontos do `timeline.json` (≤ 2 px).

**Bloco a bloco:** a Tela e os Gatilhos de cada âncora estão no Anexo A. Os pontos de atenção:
- **H1:** a câmera gira em volta da bola por ~5 s antes da coluna. A integral cartesiana entra limite a limite, de fora para dentro.
- **H2:** as três famílias (cascas, cones, páginas) entram uma por vez, cada uma com a sua linha no painel; depois as duas células com `?`.
- **B1-3:** a célula lima é o mesmo objeto na caixa e na bola (deforma, não duplica).
- **B2-1:** as três arestas acendem uma por vez e voam para a linha `ΔV ≈` (cada uma na cor da sua variável).
- **B2-3:** a matriz é escrita coluna por coluna. Cada menor é sublinhado na matriz no instante em que o seu termo é escrito.
- **B3-1:** a costura acende em ALERTA; a caixa se parte em θ = π e as metades voam (azul-claro e coral, tons chapados).
- **B5:** a miniatura da bola do H1 volta, e no fim a casca de 0,84 a 1 acende.
- **B6:** a coluna passa de 6 linhas, então se renova: a C10 1–3 na primeira tela (B6-1) e a C10 4–10 na segunda (B6-2), com a integral montada como título pequeno no topo.
- **S2:** o cartão do próximo vídeo fica ≥ 8 s.

## 5. Reserva e corte

**Reserva para o 3.5-E1** (exercícios integradores do módulo), com a conta pronta no sympy das threads que pegarem: a gaussiana 3D (π^{3/2}), Guidorizzi §5.5 Ex. 7–9, as lineares do §5.4 (Ex. 1–2) e o centro de massa da semibola.

**Plano de corte, se o Kaio quiser ≈ 16:00** (−3:50, sem tocar na conta inteira):

| Corte | Economia |
|---|---:|
| B2-2 (duas polares) vira uma frase no fim do B2-1: "dá para ver também como duas polares, uma na página e uma no chão: erre vezes ésse" | −0:45 |
| B4 (cebola) vira duas frases no B5 ("a área da esfera aparece de graça: quatro pi erre ao quadrado") | −0:45 |
| B3-2 (receita) entra dentro do B6-1, onde a sonda já aparece | −0:30 |
| B5 perde a média 3/4 e o 0,84 | −0:25 |
| B1-2 (ponto) fica só com a altura, a sombra e Pitágoras | −0:25 |
| B7 vira a primeira frase do S2 | −0:20 |
| B2-4 mantém só o erro sem sen φ (o mais traiçoeiro) | −0:20 |
| H1 lê a primitiva em uma frase ("já vem com raiz e logaritmo") | −0:20 |

## 6. Decisões (o Kaio decide)
1. **Duração.** A v1 tem ≈ 19:49, acima dos 8–15 do Atlas, como a v1 das polares (20:45 → 15:20 na v2). Recomendo cortar para ≈ 16:00 pelo plano do §5 na v2, depois que você olhar os quadros. Se preferir manter tudo, a v1 já está pronta para o preview.
2. **Hook com a bola pesada** (Guidorizzi §5.5 Ex. 5). Recomendo: é o exemplo do próprio livro, trava de verdade em cartesianas e sai em três linhas em esféricas.
3. **A casquinha** (Guidorizzi Exercício 5.5-4, com a = 1, e Stewart §15.8). Recomendo: tem a substituição com limites novos e confere pela geometria.
4. **Gancho da lata** para as cilíndricas (mesmo integrando, §5.6 Ex. 1). Recomendo; a thread do 3.5-T3 precisa abrir com ela (ver §7).
5. **Leitura de cada degrau** mantida (regras da conta inteira e da leitura dos símbolos).

## 7. Observações
- **Nenhum vídeo é citado.** A fala diz "as polares que você já conhece", nunca "vídeo passado" ou um número de EP. O único futuro citado é o próximo vídeo (cilíndricas), no gancho.
- **Notação.** Igual aos vídeos da lei de Gauss e ao EP. 13: ρ é densidade. A distância ao centro é r, o raio fixo é R e a sombra é s. Como o Guidorizzi e o Stewart chamam a distância de ρ, o B1-1 avisa uma vez ("nos livros de Cálculo essa distância costuma se chamar rô"). As threads do 3.5-T1 e do 3.5-T3 devem usar a mesma notação (no 3.5-T3, a distância ao eixo é s).
- **3.5-T3 (cilíndricas)** deve abrir pela lata deste gancho: a mesma densidade √(x² + y² + z²) em x² + y² ≤ 1, 0 ≤ z ≤ 1. O valor (Guidorizzi §5.6 Ex. 1) é π(7√2 − 2 + 3 ln(1 + √2))/12 ≈ 2,76 [B7c]. Este vídeo não mostra esse número.
- **Pronúncia.** "téta" sempre, com acento. O teste do R e do S está no Anexo C; no texto da voz, toda variável latina é escrita como a letra maiúscula (regra do Kaio, Anexo B).
- **Numeração.** `yt_0041` · EP. 16, confirmado pelo Kaio (2026-11-15).

---

## Anexo A · Narração v1.1 (tags do ElevenLabs v4)

### Tempo por âncora

| Âncora | Palavras | Tempo |
|---|---:|---:|
| H1 · a bola pesada na casca | 157 | 0:52.8 |
| H2 · a grade nova e a pergunta | 117 | 0:39.5 |
| A1 · bem-vindos | 47 | 0:16.2 |
| B1-1 · o endereço esférico | 260 | 1:27.2 |
| B1-2 · um ponto de exemplo | 160 | 0:53.8 |
| B1-3 · a caixa vira a bola | 156 | 0:52.5 |
| B2-1 · a caixinha curva: três arestas | 292 | 1:37.8 |
| B2-2 · duas polares em sequência | 161 | 0:54.2 |
| B2-3 · o determinante | 285 | 1:35.5 |
| B2-4 · o teste da bola | 252 | 1:24.5 |
| B3-1 · o teorema, metade por metade | 249 | 1:23.5 |
| B3-2 · a receita e a sonda radial | 107 | 0:36.2 |
| B4 · a cebola: área da esfera | 184 | 1:01.8 |
| B5 · a bola pesada: M = π | 283 | 1:34.8 |
| B6-1 · a casquinha: as superfícies e os limites | 231 | 1:17.5 |
| B6-2 · a casquinha: a conta | 281 | 1:34.2 |
| B7 · quando usar esféricas | 79 | 0:26.8 |
| S1 · síntese | 95 | 0:32.2 |
| S2 · a lata e o próximo vídeo | 142 | 0:47.8 |
| **Total** | **3538** | **19:48.8** |

Contagem por script (palavras sem as tags; 0,15 s + palavras/3 + 0,35 s por âncora, a 3 palavras/s).

Regras da fala: "téta" sempre; variáveis latinas como a letra maiúscula (R, S, X, Y, Z, D V, a transformação T), sem fonética forçada; gregas pelo nome ("rô" só a densidade, "fi", "delta", "pi"); nenhum vídeo citado (nada de "vídeo passado"); cada degrau da conta é lido; tags em inglês, uma por trecho, sem [slowly].

### H1 · a bola pesada na casca
**Tela:** alvo 01. A bola 3D com o degradê radial (escura no centro, ciano forte na casca), as legendas `LEVE NO CENTRO` e `PESADA NA CASCA`; à direita, a caneta escreve `DENSIDADE ρ = √(x² + y² + z²)`, `MASSA = ∭_B √(x² + y² + z²) dV`, a integral cartesiana com os três pares de limites, a primitiva de dentro com `k² = x² + y²`; fecha com o selo `TRAVA` e `RAIZ E LOGARITMO JÁ NA DE DENTRO`.
**Gatilhos:**
- "Imagina uma bola"→bola 3D, câmera girando devagar;
- "fica mais pesada"→as duas legendas;
- "que aqui a gente chama de rô"→linha DENSIDADE;
- "Quanto pesa"→linha MASSA;
- "os limites já assustam"→integral cartesiana, limite por limite, de fora para dentro;
- "a integral de dentro"→a primitiva com o colchete;
- "Trava"→selo TRAVA.
> [curious] Imagina uma bola de raio um que fica mais pesada à medida que você se afasta do centro. A densidade, que aqui a gente chama de rô, é a própria distância até o centro: raiz de X ao quadrado mais Y ao quadrado mais Z ao quadrado. Quanto pesa essa bola? A massa é a integral tripla da densidade na bola. Em cartesianas, os limites já assustam: X de menos um a um; Y entre menos e mais raiz de um menos X ao quadrado; Z entre menos e mais raiz de um menos X ao quadrado menos Y ao quadrado. E a integral de dentro, em Z, chamando X ao quadrado mais Y ao quadrado de K ao quadrado, tem primitiva um meio de: Z vezes raiz de K ao quadrado mais Z ao quadrado, mais K ao quadrado vezes o logaritmo de Z mais essa raiz. Raiz e logaritmo, e ainda faltam duas integrais. Trava.

### H2 · a grade nova e a pergunta
**Tela:** alvo 02. A esfera em traço; as duas células lima com `?` (`PERTO DO POLO` e `NO EQUADOR`); o painel `A GRADE NOVA` com `CASCAS r = cte`, `CONES φ = cte`, `PÁGINAS θ = cte` e `MESMO Δr, Δφ, Δθ`. As três famílias de superfície entram uma por vez no 3D (alvo auxiliar `r3d_superf.png`: cone violeta, página verde-água, meia casca laranja). Fecha com `QUAL É O VOLUME DE CADA PEDAÇO?` no canto.
**Gatilhos:**
- "a bola é redonda"→a bola do H1 perde o degradê e vira traço;
- "cascas"→casca laranja + linha CASCAS;
- "cones"→cone violeta + linha CONES;
- "páginas"→página verde-água + linha PÁGINAS;
- "Repara nestes dois pedaços"→as duas células lima;
- "o mesmo delta R"→linha MESMO;
- "qual é o volume"→os dois `?` e o título do canto.
> [thoughtful] Só que a bola é redonda, e a densidade só depende de uma coisa: da distância até o centro. Então troca a grade. Em vez de cubinhos, cascas esféricas, uma dentro da outra; cones saindo da origem, em volta do eixo Z; e páginas, como as de um livro aberto em volta desse eixo. Repara nestes dois pedaços da grade nova. Os dois têm o mesmo delta R, o mesmo delta fi e o mesmo delta téta. Mas o de perto do polo é fininho, e o do equador é gordo. [serious] Então a pergunta do vídeo é: qual é o volume de cada pedaço dessa grade? Quando a gente responder, essa bola pesada sai em três linhas.

### A1 · bem-vindos
**Tela:** logo; `COORDENADAS ESFÉRICAS NA INTEGRAL TRIPLA`; `NESTE VÍDEO: O ENDEREÇO · O r² sen φ · O TEOREMA · A BOLA · A CASQUINHA`.
> [happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Hoje é dia de coordenadas esféricas na integral tripla: o endereço de um ponto no espaço, o fator de volume, R ao quadrado seno de fi, o teorema, e três contas: a bola, a bola pesada e uma casquinha de sorvete.

### B1-1 · o endereço esférico
**Tela:** alvo 03. Eixos 3D com o chão em polares (círculos e raios finos); P branco; o segmento r laranja; o arco φ violeta junto do eixo z; a página: triângulo retângulo com preenchimento chapado escuro `#1E3A4A` e contorno fino (sem transparência); a sombra s pêssego no chão; o arco θ verde-água no chão. Coluna: `z = r cos φ`, `s = r sen φ` + `SOMBRA NO CHÃO`, `x = s cos θ = r sen φ cos θ`, `y = s sen θ = r sen φ sen θ`, `r ≥ 0, 0 ≤ φ ≤ π, 0 ≤ θ ≤ 2π`, legendas `φ: DO POLO NORTE (0) AO POLO SUL (π)` e `θ: A LONGITUDE, IGUAL ÀS POLARES`.
**Gatilhos:**
- "a distância de P até a origem"→segmento r;
- "o ângulo entre o eixo Z"→arco φ;
- "Fi zero é o polo norte"→legenda φ;
- "o téta de sempre"→arco θ + legenda θ;
- "um triângulo retângulo"→a página;
- "Z igual a R cosseno de fi"→linha z, com r e φ voando do desenho;
- "a sombra de P no chão"→a sombra s acende + linha s;
- "X igual a S cosseno de téta"→linha x, o s voando da linha de cima;
- "Y igual"→linha y;
- "Os intervalos"→linha dos intervalos.
> [thoughtful] Primeiro, o endereço. Um ponto P no espaço fica com três números. O primeiro é a distância de P até a origem, e ela se chama R. Nos livros de Cálculo essa distância costuma se chamar rô; aqui, como na física, o rô fica para a densidade. O segundo é o ângulo entre o eixo Z, do lado positivo, e o segmento que vai da origem até P. Esse ângulo se chama fi. Fi zero é o polo norte, fi igual a pi sobre dois é o equador, e fi igual a pi é o polo sul. O terceiro é o téta de sempre: o ângulo das polares, medido no chão, a partir do eixo X. Agora, as contas. Na página que passa por P, o desenho é um triângulo retângulo, com hipotenusa R e o ângulo fi junto do eixo Z. O cateto em pé é a altura: Z igual a R cosseno de fi. O cateto deitado é a sombra de P no chão, que a gente chama de S: S igual a R seno de fi. E no chão são as polares: X igual a S cosseno de téta, que é R seno de fi cosseno de téta; Y igual a S seno de téta, que é R seno de fi seno de téta. Os intervalos: R maior ou igual a zero, fi de zero a pi, e téta de zero a dois pi. Fi só vai até pi porque, passando do polo sul, você já estaria do outro lado, e esse lado o téta já cobre.

### B1-2 · um ponto de exemplo
**Tela:** alvo 04. O mesmo desenho com os números: `2` no r, `π/6` no φ, `π/3` no θ, `√3` na altura, `s = 1` na sombra. Coluna: `(r, φ, θ) = (2, π/6, π/3)`; `z = 2 cos(π/6) = 2 · √3/2 = √3`; `s = 2 sen(π/6) = 2 · 1/2 = 1`; `x = 1 · cos(π/3) = 1/2`, `y = 1 · sen(π/3) = √3/2`; `x² + y² + z² = 1/4 + 3/4 + 3 = 4 = 2²` ✓; chip `x² + y² + z² = r²`.
**Gatilhos:**
- "R igual a dois"→linha do ponto, os números voam para o desenho;
- "A altura"→linha z;
- "A sombra"→linha s;
- "Agora no chão"→linha x e y;
- "Confere com Pitágoras"→linha da soma + ✓;
- "Isso vale sempre"→chip.
> [curious] Um exemplo para conferir. R igual a dois, fi igual a pi sobre seis, téta igual a pi sobre três. A altura: Z igual a dois vezes cosseno de pi sobre seis, que é dois vezes raiz de três sobre dois: raiz de três. A sombra: S igual a dois vezes seno de pi sobre seis, dois vezes um meio: um. Agora no chão: X igual a um vezes cosseno de pi sobre três, um meio; Y igual a um vezes seno de pi sobre três, raiz de três sobre dois. Confere com Pitágoras: X ao quadrado mais Y ao quadrado mais Z ao quadrado é um quarto, mais três quartos, mais três, que dá quatro, que é dois ao quadrado. É a distância, R, ao quadrado. E isso vale sempre: X ao quadrado mais Y ao quadrado mais Z ao quadrado é igual a R ao quadrado. Por isso a densidade da bola pesada, em esféricas, vira simplesmente R.

### B1-3 · a caixa vira a bola
**Tela:** alvo 05. À esquerda, a caixa (r, φ, θ) com grade fina nas faces e uma célula lima; a seta `T(r, φ, θ)`; à direita, a bola com a célula curva. As faces ruins da caixa em ALERTA tracejado; na bola, a costura (página θ = 0) em ALERTA, o eixo z tracejado e a origem (alvo auxiliar `r3d_bolagrade.png`). Coluna: `UMA CAIXA!` + `0 ≤ r ≤ 1, 0 ≤ φ ≤ π, 0 ≤ θ ≤ 2π`; `BORDAS RUINS`: `r = 0 → ORIGEM`, `φ = 0, φ = π → EIXO z`, `θ = 0, θ = 2π → MESMA PÁGINA`.
**Gatilhos:**
- "Ela se chama T"→rótulo T na seta;
- "é uma caixa"→caixa + `UMA CAIXA!` + intervalos;
- "vira a bola"→a célula lima voa da caixa para a bola (um único objeto que se deforma; nada de cópia);
- "A face R igual a zero"→face em ALERTA + linha 1;
- "As faces fi igual a zero e fi igual a pi"→faces + linha 2 + eixo tracejado;
- "as faces téta igual a zero e téta igual a dois pi"→faces + linha 3 + costura.
> [thoughtful] Agora olha isso como uma transformação. Ela se chama T, porque a letra fi agora é do ângulo. T leva o ponto R, fi, téta no ponto X, Y, Z. E repara no lado das coordenadas: R de zero a um, fi de zero a pi, téta de zero a dois pi. É uma caixa! A transformação T pega essa caixa e transforma na bola de raio um. Uma célula da caixa vira uma célula curva da bola. Mas três pares de faces da caixa se comportam mal. A face R igual a zero, um retângulo inteiro, cai num ponto só: a origem. As faces fi igual a zero e fi igual a pi caem em cima do eixo Z: um retângulo vira um segmento. E as faces téta igual a zero e téta igual a dois pi caem na mesma página, uma em cima da outra. Guarda essas três bordas, que elas voltam no teorema.

### B2-1 · a caixinha curva: três arestas
**Tela:** alvo 06. Zoom na célula do equador (r de 0,62 a 1); a aresta Δr laranja, a aresta rΔφ violeta no meridiano, a aresta r sen φ Δθ verde-água no paralelo; o raio do paralelo `s = r sen φ` em pêssego tracejado; o arco φ. Coluna: `ARESTA 1 Δr`; `ARESTA 2 rΔφ` + `ARCO = RAIO · ÂNGULO`; `ARESTA 3 (r sen φ)Δθ` + `RAIO DO PARALELO`; `ΔV ≈ Δr · rΔφ · r sen φ Δθ`; `= r² sen φ Δr Δφ Δθ` (r² sen φ em lima). Painel: `Δr = 1/2, Δφ = Δθ = π/6, r̄ = 3/4`; `POLO (3/4)² · sen(π/12) · 1/2 · π/6 · π/6 ≈ 0,020`; `EQUADOR (3/4)² · sen(5π/12) · 1/2 · π/6 · π/6 ≈ 0,075`; `RAZÃO 2 + √3 ≈ 3,7`.
**Gatilhos:**
- "três arestas"→a câmera chega na célula;
- "delta R"→aresta 1;
- "no meridiano"→aresta 2 + arco φ;
- "no paralelo"→aresta 3;
- "o raio dele é a sombra"→raio do paralelo tracejado + legenda;
- "quase o produto"→linha ΔV, cada aresta voando da sua cor no desenho;
- "Junta os erres"→glyph map para `r² sen φ`;
- "Com delta R igual a um meio"→painel;
- "perto do polo"→linha POLO;
- "No equador"→linha EQUADOR;
- "A razão"→linha RAZÃO.
> [thoughtful] Agora, a pergunta do começo: qual é o volume de uma célula dessa grade? Ela é quase uma caixinha, só que curva, com três arestas. A primeira vai na direção do raio, e mede delta R. A segunda anda no meridiano, de fi até fi mais delta fi, num círculo de raio R. Arco é raio vezes ângulo, então ela mede R delta fi. A terceira anda no paralelo, de téta até téta mais delta téta. Mas o paralelo não tem raio R: o raio dele é a sombra, S igual a R seno de fi. Então ela mede R seno de fi delta téta. O volume é quase o produto das três: delta V é aproximadamente delta R, vezes R delta fi, vezes R seno de fi delta téta. Junta os erres: R ao quadrado seno de fi, delta R, delta fi, delta téta. E é esse seno de fi que separa os dois pedaços do começo. Com delta R igual a um meio, delta fi e delta téta iguais a pi sobre seis, e R médio igual a três quartos: perto do polo, o fi do meio é pi sobre doze, e a conta é três quartos ao quadrado, vezes seno de pi sobre doze, vezes um meio, vezes pi sobre seis, vezes pi sobre seis, aproximadamente zero vírgula zero vinte. No equador, o fi do meio é cinco pi sobre doze, e a mesma conta dá zero vírgula zero setenta e cinco. A razão é o seno de cinco pi sobre doze dividido pelo seno de pi sobre doze, que é dois mais raiz de três, quase três vírgula sete. Mesmo delta R, mesmo delta fi, mesmo delta téta, e o pedaço do equador é quase quatro vezes maior.

### B2-2 · duas polares em sequência
**Tela:** alvo 07 (2D, grade de papel na tela inteira). Painel esquerdo `NA PÁGINA θ`: eixos s (horizontal) e z (vertical), o ponto, r laranja, arco φ a partir do eixo z, `z = r cos φ` e `s = r sen φ` tracejados. Embaixo: `|cos φ  −r sen φ ; sen φ  r cos φ| = r cos²φ + r sen²φ = r`. Seta `(r, φ) → (s, z)`. Painel direito `NO CHÃO`: eixos x e y, o s e o arco θ; `FATOR s`. Cartão `OS FATORES SE MULTIPLICAM`: `r · s`, `= r · r sen φ`, `= r² sen φ`.
**Gatilhos:**
- "fica numa página"→painel esquerdo;
- "Isso é uma polar"→arco φ a partir do eixo z;
- "O determinante dela"→determinante 2×2, degrau a degrau;
- "desce para o chão"→seta + painel direito;
- "fator S"→`FATOR s`;
- "Os fatores se multiplicam"→cartão, linha 1;
- "E S é R seno de fi"→linha 2 (s voa de `s = r sen φ`);
- "R ao quadrado seno de fi"→linha 3.
> [curious] Tem um segundo caminho, com as polares que você já conhece. Primeiro, fica numa página, com téta parado. Nela, o ponto tem altura Z igual a R cosseno de fi e sombra S igual a R seno de fi. Isso é uma polar, só que com o ângulo medido a partir do eixo Z. O determinante dela é: cosseno de fi vezes R cosseno de fi, menos, menos R seno de fi vezes seno de fi. Fica R cosseno ao quadrado de fi mais R seno ao quadrado de fi, que dá R. Esse passo multiplica a área da página por R. Depois, desce para o chão: S e téta viram X e Y, uma polar comum, com fator S. E quando duas transformações vêm em sequência, os fatores se multiplicam: R vezes S. Só que S é R seno de fi. Então R vezes R seno de fi: R ao quadrado seno de fi. O mesmo fator, por outro caminho.

### B2-3 · o determinante
**Tela:** alvo 08 (2D, grade na tela inteira). Legenda `1ª COLUNA: EM r · 2ª: EM φ · 3ª: EM θ`; `∂(x, y, z)/∂(r, φ, θ) =` matriz 3×3; seta `LINHA DE BAIXO: + − +`; a linha da expansão com as duas chaves `= 1`; `= r² sen φ cos²φ + r² sen³φ`; moldura menta `= r² sen φ (cos²φ + sen²φ) = r² sen φ` com a chave `= 1`; chip `dV = r² sen φ dr dφ dθ`; legenda `0 ≤ φ ≤ π: SEN φ ≥ 0, O MÓDULO NÃO MUDA NADA`.
**Gatilhos:**
- "A primeira coluna"→coluna 1 a caneta, de cima para baixo (e assim cada coluna);
- "usa a linha de baixo"→a linha 3 acende + `+ − +`;
- "O primeiro termo"→termo 1, com cos φ voando da matriz e o menor 2×2 sublinhado na matriz;
- "O segundo é menos"→termo 2;
- "O terceiro é zero"→`+ 0`;
- "Fica"→linha da soma;
- "Põe R ao quadrado seno de fi em evidência"→linha da moldura;
- "o módulo não muda nada"→legenda;
- "Três caminhos"→chip dV.
> [serious] E o terceiro caminho é o jacobiano: a matriz das derivadas de X, Y e Z em R, fi e téta. A primeira coluna é a derivada em R: seno de fi cosseno de téta; seno de fi seno de téta; cosseno de fi. A segunda é a derivada em fi: R cosseno de fi cosseno de téta; R cosseno de fi seno de téta; menos R seno de fi. A terceira é a derivada em téta: menos R seno de fi seno de téta; R seno de fi cosseno de téta; e zero. Para expandir, usa a linha de baixo, que tem um zero, com os sinais mais, menos, mais. O primeiro termo é cosseno de fi vezes o seu menor: R ao quadrado cosseno de fi seno de fi, vezes cosseno ao quadrado de téta mais seno ao quadrado de téta, que é um. O segundo é menos, menos R seno de fi, vezes o seu menor: R seno ao quadrado de fi, vezes cosseno ao quadrado de téta mais seno ao quadrado de téta, que de novo é um. O terceiro é zero vezes alguma coisa: zero. Fica R ao quadrado seno de fi cosseno ao quadrado de fi, mais R ao quadrado seno ao cubo de fi. Põe R ao quadrado seno de fi em evidência: sobra cosseno ao quadrado de fi mais seno ao quadrado de fi, que é um. O determinante é R ao quadrado seno de fi. E como fi vai de zero a pi, o seno de fi nunca é negativo: o módulo não muda nada. Três caminhos, o mesmo fator: D V igual a R ao quadrado seno de fi, D R, D fi, D téta.

### B2-4 · o teste da bola
**Tela:** alvo 09. À esquerda, a bola 3D em traço (`bolagrade`) com a célula lima, a costura em ALERTA e o eixo tracejado (liso, é 3D). Coluna: `V = ∫₀^{2π}∫₀^π∫₀^R r² sen φ dr dφ dθ`; `∫₀^R r² dr = [r³/3]₀^R = R³/3`; `∫₀^π sen φ dφ = [−cos φ]₀^π = −cos π − (−cos 0) = 1 + 1 = 2`; `∫₀^{2π} dθ = 2π`; `V = R³/3 · 2 · 2π = 4πR³/3` ✓; painel de erros: `SEM r² ⇒ R · 2 · 2π = 4πR` + `METRO` ✗; `SEM sen φ ⇒ R³/3 · π · 2π = 2π²R³/3 ≈ 6,58 R³` ✗ + `UNIDADE CERTA, NÚMERO ERRADO (O CERTO ≈ 4,19 R³)`.
**Gatilhos:**
- "a bola é a caixa"→integral montada, com os limites `R`, `π` e `2π` voando da bola (raio, eixo, volta inteira);
- "se separa em três"→nada de esqueleto: cada linha só nasce quando a fala chega nela;
- "A de R"→linha 2; "A de fi"→linha 3; "A de téta"→linha 4;
- "Multiplica"→linha V + ✓;
- "Esqueceu o R ao quadrado"→painel 1;
- "Esqueceu o seno de fi"→painel 2.
> [serious] Antes do teorema, um teste com uma resposta que todo mundo conhece: o volume da bola de raio R. Em esféricas, a bola é a caixa: R de zero a R, fi de zero a pi, téta de zero a dois pi. E o integrando é só o fator, R ao quadrado seno de fi. Como os limites são constantes e o fator é um produto, a integral se separa em três. A de R: R ao cubo sobre três, de zero a R, que dá R ao cubo sobre três, menos zero. A de fi: a primitiva de seno de fi é menos cosseno de fi, de zero a pi: menos cosseno de pi, menos, menos cosseno de zero. Isso é um mais um: dois. A de téta: téta de zero a dois pi, dois pi. Multiplica: R ao cubo sobre três, vezes dois, vezes dois pi: quatro terços de pi R ao cubo. É o volume da bola. Agora, os dois erros clássicos. Esqueceu o R ao quadrado? A de R dá só R, e o resultado é quatro pi R: metro, não metro cúbico. Esqueceu o seno de fi? A de fi dá pi em vez de dois, e sai dois pi ao quadrado R ao cubo sobre três, quase seis vírgula seis R ao cubo. A unidade está certa, mas o número está errado: a bola de verdade tem quatro vírgula dezenove R ao cubo. Esse erro a unidade não pega, então confere sempre o seno de fi.

### B3-1 · o teorema, metade por metade
**Tela:** alvo 10. Em cima, as duas peças 3D (lisas): a caixa partida em θ = π (`caixa2`, metades azul-claro e coral em tons chapados, faces ruins em ALERTA tracejado), a seta `T` e a bola com a célula lima e a costura em ALERTA; legendas `METADE θ ≤ π`, `METADE θ ≥ π` e `O CORTE: VOLUME ZERO`. Embaixo, o painel opaco do enunciado geral (sobre a grade de borda a borda): `T: Ω ⊂ ℝ³ → ℝ³ DE CLASSE C¹ · B_uvw COMPACTO, FRONTEIRA DE CONTEÚDO NULO`; `NO INTERIOR: T(B̊_uvw) = B̊ · T INJETORA · ∂(x, y, z)/∂(u, v, w) ≠ 0`; `∭_B f(x, y, z) dx dy dz = ∭_{B_uvw} f(T(u, v, w)) |∂(x, y, z)/∂(u, v, w)| du dv dw`. Depois, um glyph map leva a última linha ao caso esférico: `(u, v, w) → (r, φ, θ)` e `|∂(x, y, z)/∂(u, v, w)| → r² sen φ` (o lima voa do chip `dV` do B2-3): `∭_B f dx dy dz = ∭_{B_rφθ} f(T(r, φ, θ)) r² sen φ dr dφ dθ`.
**Gatilhos:**
- "do jeito do Guidorizzi"→enunciado linha a linha;
- "três coisas"→legenda NO INTERIOR, item por item;
- "Então a integral tripla"→a fórmula geral;
- "Nas esféricas"→glyph map para o caso esférico;
- "tem um problema"→a costura acende em ALERTA na bola;
- "em duas metades"→a caixa se parte; as metades voam;
- "volume zero"→legenda `O CORTE: VOLUME ZERO`.
> [serious] Agora, o teorema, do jeito do Guidorizzi. Ele vale para qualquer transformação T de U, V, W, de classe C um. Do lado das coordenadas, a região B U V W é compacta, e a fronteira dela tem conteúdo nulo. E no interior valem três coisas: T leva o interior no interior, T é injetora, e o jacobiano não se anula. Então a integral tripla de F em B, D X D Y D Z, é igual à integral tripla em B U V W de F de T de U, V, W, vezes o módulo do jacobiano, D U D V D W. Nas esféricas, U, V, W são R, fi, téta, e o módulo do jacobiano é R ao quadrado seno de fi. Para a bola inteira, tem um problema. A imagem do interior da caixa é a bola sem uma página: a página téta igual a zero fica de fora, e ela está dentro da bola. Então a gente corta a bola em duas metades: téta de zero a pi, e téta de pi a dois pi. Em cada metade, a hipótese vale ao pé da letra: o interior da meia caixa vai inteiro no interior da meia bola, sem repetir ponto, e o fator é positivo, porque R é positivo e fi está entre zero e pi. O corte, a origem e o eixo têm volume zero, então as duas metades se somam. E a bola inteira, com téta de zero a dois pi, vale.

### B3-2 · a receita e a sonda radial
**Tela:** a bola em traço com uma região genérica (casca entre dois cones); os selos `① θ: QUANTO GIRA EM VOLTA DE z`, `② φ: DE QUE CONE A QUE CONE`, `③ r: A SONDA SAI DA ORIGEM`; a sonda entra em azul-claro e sai em coral; cartão `θ E φ FORA: NÚMEROS · r DENTRO: DA SONDA`.
**Gatilhos:** "Téta"→selo ①; "Fi"→selo ②; "solta uma sonda"→selo ③ + a sonda; "entra"→azul-claro; "sai"→coral; "É por isso"→cartão.
> [thoughtful] Na prática, a receita tem três perguntas. Téta: de que ângulo a que ângulo a região gira em volta do eixo Z? Fi: de que cone a que cone ela vai, a partir do polo norte? E R: para cada direção, solta uma sonda saindo da origem. Onde ela entra na região é o limite de baixo; onde ela sai é o limite de cima. A sonda é sempre radial: sai da origem e vai reto. É por isso que as esféricas combinam com bolas, com cones de vértice na origem e com integrandos que têm X ao quadrado mais Y ao quadrado mais Z ao quadrado.

### B4 · a cebola: área da esfera
**Tela:** alvo 11. A bola cortada em cunha, com uma casca laranja (r de 0,6 a 0,7) e as legendas `CASCA DE RAIO r` e `ESPESSURA dr`. Coluna: `∫₀^{2π}∫₀^π r² sen φ dφ dθ = r² · [−cos φ]₀^π · [θ]₀^{2π}`; `= r² · 2 · 2π = 4πr²` + `ÁREA DA ESFERA`; `V = ∫₀^R 4πr² dr = 4π[r³/3]₀^R = 4πR³/3`; `d/dR (4πR³/3) = 4πR²` + `ENGORDAR = UMA CASCA`; por último (não está no alvo) `ρ SÓ DE r: ∭ ρ dV = ∫₀^R ρ(r) 4πr² dr`.
**Gatilhos:**
- "Fixa R"→a casca acende;
- "A de fi dá dois"→linha 1;
- "a bola é uma cebola"→as cascas se empilham (5 cascas, do centro para fora, sem brilho);
- "Somando as cascas"→linha 2;
- "derivando"→linha 3 + selo;
- "Para uma densidade"→legenda.
> [curious] Uma leitura bonita desse fator. Fixa R e integra só em fi e téta: a integral de zero a dois pi e de zero a pi de R ao quadrado seno de fi, D fi D téta. A de fi dá dois, igual no teste da bola; a de téta dá dois pi. Fica quatro pi R ao quadrado: a área da esfera de raio R. Então a bola é uma cebola: cascas esféricas finas, cada uma com área quatro pi R ao quadrado e espessura D R. Somando as cascas, a integral de zero a R de quatro pi R ao quadrado D R é quatro pi R ao cubo sobre três, de zero a R: quatro pi R ao cubo sobre três, o volume. E o caminho contrário: derivando o volume, quatro terços de pi R ao cubo, em relação a R, sai quatro pi R ao quadrado, a área. Engordar a bola é acrescentar uma casca. Então, se a densidade só depende de R, a integral tripla vira uma integral simples em R, com o peso quatro pi R ao quadrado.

### B5 · a bola pesada: M = π
**Tela:** alvo 12 (canto `DE VOLTA À BOLA`). A bola do H1 com o degradê volta à esquerda. Coluna, etapa 1: `ρ = √(x² + y² + z²) = √(r²) = r (r ≥ 0)`; `M = ∫₀^{2π}∫₀^π∫₀^1 r · r² sen φ dr dφ dθ` com as chaves `DENSIDADE` (ciano) e `JACOBIANO` (lima) por 2 s; `= ∫₀^{2π}∫₀^π∫₀^1 r³ sen φ dr dφ dθ` (não está no alvo); `= [r⁴/4]₀^1 · [−cos φ]₀^π · [θ]₀^{2π}`; `= (1/4 − 0) · (1 + 1) · (2π − 0) = π` ✓; legenda `CONFERE: CARTESIANAS NO COMPUTADOR = 3,14159…` (não está no alvo). Etapa 2 (a coluna sobe): `MÉDIA M/V = π/(4π/3) = π · 3/(4π) = 3/4`; `MASSA ATÉ c: πc⁴ = π/2 ⇒ c = ⁴√(1/2) ≈ 0,84`, com a casca de 0,84 a 1 acesa na bola.
**Gatilhos:**
- "a bola pesada do começo"→miniatura do H1;
- "que em esféricas é só R"→linha ρ (o r voa do chip do B1-2);
- "O R da densidade"→chave DENSIDADE; "o fator"→chave JACOBIANO;
- "Junta"→glyph map r · r² → r³;
- "E separa em três"→a linha dos três colchetes, um fator por vez ("A de R", "A de fi", "A de téta");
- "A massa é pi"→moldura;
- "com o computador"→legenda CONFERE;
- "a densidade média"→painel linha 1; "metade da massa"→painel linha 2, com a casca de 0,84 a 1 acesa na miniatura.
> [thoughtful] Agora sim, a bola pesada do começo. A densidade rô é raiz de X ao quadrado mais Y ao quadrado mais Z ao quadrado, que em esféricas é só R. A massa é a integral de zero a dois pi, de zero a pi e de zero a um, de R vezes R ao quadrado seno de fi, D R D fi D téta. Um R é da densidade; o R ao quadrado seno de fi é o fator. Junta: R ao cubo seno de fi. E separa em três. A de R: R à quarta sobre quatro, de zero a um: um quarto menos zero, um quarto. A de fi: menos cosseno de fi, de zero a pi, que dá dois, igual na bola. A de téta: dois pi. Multiplica: um quarto, vezes dois, vezes dois pi. [excited] A massa é pi. Aquela integral que travava em cartesianas sai em três linhas. E o computador, fazendo a conta em cartesianas, confere: três vírgula um quatro um cinco nove. [thoughtful] Mais duas leituras. O volume da bola é quatro pi sobre três, então a densidade média é a massa dividida pelo volume: pi sobre quatro pi sobre três, que é pi vezes três sobre quatro pi, três quartos. E a mesma conta, só que até um raio C, dá C à quarta sobre quatro, vezes dois, vezes dois pi: pi C à quarta. Metade da massa é pi sobre dois. Pi C à quarta igual a pi sobre dois dá C à quarta igual a um meio, e C igual à raiz quarta de um meio, cerca de zero vírgula oitenta e quatro. Metade da massa mora nos dezesseis por cento de fora do raio.

### B6-1 · a casquinha: as superfícies e os limites
**Tela:** alvo 13, metade de cima da coluna. A casquinha 3D (cone violeta embaixo, calota esférica de cima em ciano, cortada em cunha para mostrar a sonda laranja e a página); `φ = π/4` no cone; `r = 2 cos φ` na calota; o ponto de encontro com `1` de altura. Coluna: `CONE r cos φ = r sen φ ⇒ φ = π/4`; `ESFERA r² = 2r cos φ ⇒ r = 2 cos φ`; (na fala, o completamento de quadrado com a legenda `x² + y² + (z − 1)² = 1`); `V = ∫₀^{2π}∫₀^{π/4}∫₀^{2 cos φ} r² sen φ dr dφ dθ`.
**Gatilhos:**
- "uma casquinha de sorvete"→3D girando até a vista do alvo;
- "O cone"→linha CONE;
- "A esfera"→linha ESFERA + legenda do centro (0, 0, 1);
- "Téta"/"Fi"/"R"→os três limites a caneta, cada um quando a fala chega nele, com a sonda saindo da origem e parando na calota;
- "o encontro"→ponto de encontro + `1`.
> [curious] Agora, uma região que não é bola: uma casquinha de sorvete. Embaixo, o cone Z igual à raiz de X ao quadrado mais Y ao quadrado. Em cima, a esfera X ao quadrado mais Y ao quadrado mais Z ao quadrado igual a dois Z. Primeiro, cada superfície em esféricas. O cone: Z é R cosseno de fi, e a raiz de X ao quadrado mais Y ao quadrado é a sombra, S, que é R seno de fi. R cosseno de fi igual a R seno de fi: a tangente de fi é um, e fi é pi sobre quatro. O cone inteiro é uma superfície de fi constante. A esfera: o lado esquerdo é R ao quadrado, o lado direito é dois R cosseno de fi. Divide por R: R igual a dois cosseno de fi. Completando o quadrado em Z, ela é a esfera de raio um com centro em zero, zero, um, e passa pela origem. Agora a receita. Téta: a casquinha gira inteira, de zero a dois pi. Fi: do eixo, zero, até o cone, pi sobre quatro. R: a sonda sai da origem, que é a ponta da casquinha, e sai pela esfera, em R igual a dois cosseno de fi. Na borda do cone, R vale dois cosseno de pi sobre quatro, raiz de dois: o encontro está na altura um, com sombra um.

### B6-2 · a casquinha: a conta
**Tela:** alvo 13, metade de baixo da coluna (a coluna rola para cima quando passar de 6 linhas). `[r³/3]₀^{2 cos φ} sen φ = (8/3) cos³φ sen φ`; `u = cos φ, du = −sen φ dφ` e `φ = 0 → u = 1, φ = π/4 → u = √2/2`; `(8/3)∫_{√2/2}^1 u³ du = (8/3)[u⁴/4]_{√2/2}^1 = (8/3)(1/4 − 1/16) = (8/3) · (3/16) = 1/2`; `V = 2π · 1/2 = π` ✓; `CONFERE π/3 + 2π/3 = π` + `CONE + MEIA BOLA` (o 3D separa as duas peças por cor: cone violeta, meia bola ciano; a peça nunca se separa no espaço).
**Gatilhos:**
- "A de dentro"→linha 1;
- "pede uma substituição"→linha u, du;
- "Os limites"→linha dos limites;
- "O menos do D U inverte"→linha da integral em u, com os limites trocando de lugar num glyph map;
- "Primitiva"→colchete, depois os dois valores;
- "Oito terços vezes três dezesseis avos"→`= 1/2`;
- "Volume"→linha V + ✓;
- "Confere pela geometria"→as duas peças mudam de cor + linha CONFERE.
> [serious] Monta: V igual à integral de zero a dois pi, de zero a pi sobre quatro, e de zero a dois cosseno de fi, de R ao quadrado seno de fi, D R D fi D téta. A de dentro, em R: R ao cubo sobre três, de zero a dois cosseno de fi, vezes seno de fi. Dois cosseno de fi, ao cubo, é oito cosseno ao cubo de fi; sobre três, menos zero. Fica oito terços de cosseno ao cubo de fi seno de fi. A do meio, em fi, pede uma substituição: U igual a cosseno de fi, D U igual a menos seno de fi D fi. Os limites: fi igual a zero dá U igual a um; fi igual a pi sobre quatro dá U igual a raiz de dois sobre dois. O menos do D U inverte os limites: fica oito terços da integral de raiz de dois sobre dois até um de U ao cubo, D U. Primitiva: U à quarta sobre quatro. Em um, dá um quarto. Em raiz de dois sobre dois: raiz de dois sobre dois, à quarta, é quatro dezesseis avos, que é um quarto; dividido por quatro, um dezesseis avos. Um quarto menos um dezesseis avos é três dezesseis avos. Oito terços vezes três dezesseis avos: um meio. A de fora, em téta, multiplica por dois pi. Volume: dois pi vezes um meio, igual a pi. [curious] Confere pela geometria? A casquinha é um cone de raio um e altura um, com volume pi sobre três, mais a meia bola de cima, de raio um, com volume dois pi sobre três. Pi sobre três mais dois pi sobre três: pi.

### B7 · quando usar esféricas
**Tela:** três miniaturas com ✓ (bola, casca, casquinha) e uma com ✗ (a lata, só a silhueta); legendas `✓ BOLAS, CASCAS, CONES COM VÉRTICE NA ORIGEM`, `✓ x² + y² + z² NO INTEGRANDO`, `✗ PAREDES QUE NÃO PASSAM PELA ORIGEM`.
> [thoughtful] Então, quando usar esféricas? Quando a região vem de bolas, cascas e cones com vértice na origem, e quando o integrando tem X ao quadrado mais Y ao quadrado mais Z ao quadrado. A sonda radial entra e sai por uma superfície só, e os limites ficam simples. E quando não usar? Quando a região tem paredes que não passam pela origem. Aí a sonda sai às vezes por uma parede, às vezes por outra, e os limites racham.

### S1 · síntese
**Tela:** três colunas com ✓: `ENDEREÇO (r, φ, θ)` com o mini desenho do B1-1; `dV = r² sen φ dr dφ dθ` com `ARESTAS · DUAS POLARES · DETERMINANTE`; `BOLA 4πR³/3 · BOLA PESADA π · CASQUINHA π`.
> [thoughtful] Resumindo. O endereço esférico é R, a distância até a origem; fi, o ângulo a partir do polo norte; e téta, o ângulo das polares. O pedacinho de volume é R ao quadrado seno de fi, D R D fi D téta, e ele sai por três caminhos: as arestas, as duas polares e o determinante. O teorema pede as hipóteses no interior, e a bola entra em duas metades. Com isso, a bola deu quatro terços de pi R ao cubo, a bola pesada deu pi, e a casquinha deu pi, conferida pela geometria.

### S2 · a lata e o próximo vídeo
**Tela:** alvo 14. A lata 3D (cilindro x² + y² ≤ 1, 0 ≤ z ≤ 1) cortada em cunha; duas sondas laranja saindo da origem: uma para na parede (`r = 1/sen φ`), outra na tampa (`r = 1/cos φ`); a diagonal da quina tracejada em coral; `RACHA EM φ = π/4`. Coluna: `MESMO INTEGRANDO √(x² + y² + z²)`; `x² + y² ≤ 1, 0 ≤ z ≤ 1`. Cartão (≥ 8 s): `NO PRÓXIMO VÍDEO · COORDENADAS CILÍNDRICAS · POLARES NO CHÃO + A ALTURA z`; CTA.
**Gatilhos:**
- "numa lata"→a lata + coluna;
- "pela parede"→sonda 1 + rótulo;
- "pela tampa"→sonda 2 + rótulo;
- "racha"→diagonal + legenda;
- "No próximo vídeo"→cartão;
- "deixa o like"→CTA.
> [curious] E fica uma pergunta para o próximo vídeo. A mesma densidade, raiz de X ao quadrado mais Y ao quadrado mais Z ao quadrado, mas agora numa lata: o cilindro X ao quadrado mais Y ao quadrado menor ou igual a um, com Z de zero a um. Em esféricas, a sonda que sai pela parede para em R igual a um sobre seno de fi; a que sai pela tampa para em R igual a um sobre cosseno de fi. A região racha em fi igual a pi sobre quatro, bem na quina. Para uma lata, a grade certa é outra. No próximo vídeo: coordenadas cilíndricas, as polares no chão mais a altura Z. [happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual sólido você quer ver em esféricas? Até a próxima!

---

## Anexo B · Leitura dos símbolos

Regra do Kaio (2026-11-15): no texto da voz, **toda variável latina é escrita como a própria letra maiúscula** (o ElevenLabs lê certo), sem fonética forçada ("erre", "xis", "dê"…). Letras gregas vão pelo nome que funciona: "téta" (com acento), "fi", "rô", "delta", "pi". Na tela, as letras seguem minúsculas/maiúsculas conforme a matemática.

| Símbolo | Texto da voz |
|---|---|
| x, y, z | X, Y, Z |
| r (distância ao centro) | R |
| R (raio fixo) | R |
| s (a sombra) | S |
| ρ (densidade) | rô |
| φ | fi |
| θ | téta (nunca "teta") |
| k (no H1), c (no B5), u | K, C, U |
| T, B, B_uvw, f, C¹ | T, B, B U V W, F, C um |
| Δr, Δφ, Δθ, ΔV | delta R, delta fi, delta téta, delta V |
| dV, dr dφ dθ | D V; D R, D fi, D téta |
| r² sen φ | R ao quadrado seno de fi |
| r̄ | R médio |
| cos²φ, sen³φ | cosseno ao quadrado de fi, seno ao cubo de fi |
| [G]ₐᵇ | "G, de a até b" e depois os dois valores, um de cada vez |
| ∭ | integral tripla |
| (1/2)^{1/4} | raiz quarta de um meio |
| ln | logaritmo |

## Anexo C · Teste de pronúncia (gerado em 2026-11-15)

Seis amostras em `pautas/yt_0041_teste_pronuncia/` (voz `qw7jgPZWOKrl10GsjQ82`, `eleven_v4`): o raio fixo escrito "erre", "R" e "érre"; a sombra escrita "esse", "S" e "S". O Kaio aprovou a 2 ("R") e a 5 ("S") e estendeu a regra a todas as variáveis: no texto da voz, a letra maiúscula, sem fonética forçada (Anexo B). "Fi" e "rô" seguem como estão (o teste de "téta" do EP. 13 mostrou que as letras soletradas funcionam).
