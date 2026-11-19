# Longo · Cálculo III · 3.4-E1 · Exercícios integradores do módulo 3.4 · proposta v1

2026-11-15. Produção. Fontes: Guidorizzi, *Um Curso de Cálculo*, vol. 3, 6ª ed., §4.1–4.3 e **Exercícios 4.2 e 4.3** (conferidos no PDF do projeto, págs. 176–185 do arquivo); Stewart (§15.4, §15.9) só para a didática, de memória (o PDF de 1 GB não passa pela transferência do dispositivo). Todos os números: `verificacao/verifica_calc3_34e1_sympy.py` → **67/67 True** (saída em `verifica_calc3_34e1_saida.txt`).

Narração completa, com Tela e Gatilhos por âncora: `yt_0039_narracao_v1.md` (também no Anexo A). Quadros-alvo: `yt_0039_quadros_alvo_v1/`.

---

## 0. Identificação

| Campo | Valor |
|---|---|
| Unidade | `yt_0039` · **CÁLCULO III · EP. 14** (provisório; combinado com as threads do 3.5: yt_0040 = 3.5-T1, yt_0041 = 3.5-T2). No `K:\…\videos_longos` a última pasta é `yt_0037`; o yt_0038 ainda não foi criado lá |
| Formato | `longo_horizontal` · `tipo: exercicios` |
| Título | **Exercícios do módulo: jacobiano, polares e centro de massa** |
| Duração | narração 4.357 palavras ≈ **24:12** de voz → vídeo ≈ **25–27 min** (pedido: 25–30) |
| Referência | Guidorizzi vol. 3: Ex. 4.2-1h + 4.2-5 (faixa entre parábolas), 4.2-2e (oitavo de bola), 4.2-4 e 4.2-6 (elipse), 4.3-1b (meia elipse com ρ = k y), **4.3-1f (meia arruela com ρ = k r)**, 4.3-3 (Pappus). Stewart §15.9 (hipérboles u = xy, v = y/x). Só na descrição do YouTube |
| Pré-requisitos | EP. 03 (matriz jacobiana); EP. 05 (∬ como soma); EP. 08 (Fubini); EP. 09 (reta-sonda, entrada azul-claro/saída coral, ler a região nos limites); EP. 10 (o comprimento da fatia é o fator que faltava; bola 4πa³/3); EP. 11 (jacobiano, os cinco passos, ida × volta); EP. 12 (polares, dA = r dr dθ, metade de cima × 2); EP. 13 (massa, M_x, ȳ, ⊕, meio disco 4a/3π) |
| `solido_3d:` | nenhum do arsenal Blender, porque o oitavo de esfera e os sólidos de revolução (bola, bola oca, toro) são superfícies simples feitas direto em Three.js, como nos EP. 05–13 |
| `3d_threejs:` | 2 cenas: `octante` (E3: quarto de disco no chão + casca da esfera no 1º octante, pouso de cima) e `pappus` (E6: chapa em pé sobre o eixo x varrendo o sólido por um ângulo φ; formas meio disco, meia arruela, disco deslocado) |
| Ganchos cumpridos | **EP. 13 → aqui:** a meia arruela (homogênea cai no buraco, 28/(9π) ≈ 0,990; com ρ = k r volta, 45/(14π) ≈ 1,023) é o H1 e o E5, com a conta inteira. **Aqui → EP. 15 (3.5-T1):** o cubo de lado 2 com densidade x² + y² + z², "QUANTO PESA ESTE CUBO?" (combinado com a thread do 3.5-T1, que abre por ele e chega em 32) |

---

## 1. Ideia central

**Uma receita, uma divisão, seis problemas que começam parecidos e vão ficando mais espertos.**

- A receita são os **cinco passos** da troca de variáveis (escolher; x, y em função das novas; jacobiano em módulo; região nova borda por borda; calcular e conferir). Ela volta, com os mesmos números de passo, em E1, E2, E3 e E4.
- A divisão é **ȳ = M_x / m** (momento sobre massa). Ela volta em E4, E5 e E6.
- **Toda resposta tem conferência por outro caminho** (selo ✓ menta): área do trapézio × área fatiada (E1), pipa dos quatro cantos e densidade média (E2), um oitavo da bola (E3), πa² no caso a = b e massa fatiada em pé (E4), meio disco grande menos o pequeno (E5), e **Pappus confere a meia arruela sem integral nenhuma** (E6). O clímax é esse: duas contas que não têm nada a ver dão o mesmo 28/(9π).

O fio condutor visual é **a chapa e o seu ⊕**. A meia arruela abre o vídeo com o ⊕ indeciso perto do buraco, aparece de novo no E5 com a conta, é pendurada por um alfinete no E5-3 (o fio de prumo cruza no ar) e gira no E6 para virar uma bola oca.

### Tabela "exercício ↔ figura" (cada símbolo nasce do desenho)

| # | Enunciado / ideia | Figura que explica | Âncora |
|---|---|---|---|
| D1 | e^{y−x²}/(y−x²) trava nas duas ordens | tira em pé e tira deitada com `TRAVA`; `y − x²` acende no integrando e nas bordas | E1-1 |
| D2 | u = x, v = y − x², J = 1 | a tira em pé **escorrega** para baixo sem esticar (`SÓ ESCORREGA`) | E1-2 |
| D3 | região nova = trapézio 1 ≤ v ≤ 2, 0 ≤ u ≤ v | cada borda voa do xy para o uv já com a equação nova; cantos antes → depois | E1-2 |
| D4 | ∫₀^v (e^v/v) du = e^v | a tira deitada com a chave `COMPRIMENTO v` cancela o v de baixo | E1-3 |
| D5 | área 3/2 nas duas figuras | trapézio com bases 1 e 2; tiras em pé de comprimento 1 e 2 − x | E1-4 |
| D6 | u = xy, v = y/x, jacobiano da volta | grade de hipérboles e raios; a linha-regra `volta · ida = 1` | E2-2 |
| D7 | área (ln 2)/2 ≈ 0,347 | a pipa dos quatro cantos (diagonais 1 e 1/√2) ≈ 0,354 | E2-3 |
| D8 | massa (3/4) ln 2, densidade média 3/2 | quadrado do uv pintado em faixas; reta u = 3/2 no meio | E2-4 |
| D9 | ler a região nos limites | tira em pé varrendo, a saída desenha o quarto de círculo | E3-1 |
| D10 | πa³/6 = um oitavo da bola | Three.js `octante` + pouso de cima; raio varrendo | E3-1, E3-2 |
| D11 | polares esticadas, J = abr | o círculo e uma célula polar esticam juntos até a elipse | E4-1 |
| D12 | meia elipse com ρ = k y: ȳ = 3π/32 | mapa ciano em faixas horizontais; o ⊕ pousa; o meio disco achata e leva o centroide junto | E4-2 a E4-4 |
| D13 | meia arruela: 28/(9π) no buraco | lupa ×10 na borda r = 1; `NO BURACO` | E5-2 |
| D14 | fio de prumo | a chapa gira no alfinete, o fio cruza o buraco | E5-3 |
| D15 | ρ = k r: 45/(14π) volta | régua em pé 0,98 → 1,03; ⊕ sobe do buraco para a chapa | E5-4 |
| D16 | Pappus: V = 2π ȳ A | Three.js `pappus`: o quadradinho desenha o anel 2πy; a fatia deitada vira casca | E6-1 |
| D17 | bola e bola oca conferem os centroides | `pappus` com meio disco e meia arruela; o círculo do ⊕ | E6-2, E6-3 |
| D18 | a família ȳ(a, b) e os limites | meia arruela com ValueTracker em a: buraco some (a = 0), chapa vira arame (a = b) | E6-4 |
| D19 | toro 4π² | `pappus` com o disco deslocado | E6-5 |

---

## 2. Estrutura

| Bloco | Âncoras | Voz | Layout | Conteúdo |
|---|---|---:|---|---|
| H | H1, H2 | 1:20 | A sem coluna; cartão | A meia arruela: cai no buraco? E com a borda mais pesada? Os cinco passos e a divisão |
| A | A1 | 0:19 | cartão | Bem-vindos; os seis problemas em chips |
| E1 | E1-1 a E1-4 | 3:46 | A → B → A → B | **Faixa entre parábolas** (Guidorizzi 4.2-1h + 4.2-5): trava; J = 1; trapézio; e² − e; área 3/2 conferida |
| E2 | E2-1 a E2-4 | 3:51 | A → B → A | **Hipérboles** (Stewart): jacobiano da volta 1/(2v); área (ln 2)/2 e a pipa; massa (3/4) ln 2 e a densidade média 3/2 |
| E3 | E3-1, E3-2 | 2:03 | A + 3D | **Oitavo de bola** (Guidorizzi 4.2-2e): ler a região; polares com w = a² − r²; πa³/6 = bola/8 |
| E4 | E4-1 a E4-4 | 4:31 | A | **Elipse** (Guidorizzi 4.2-4, 4.2-6) πab; **meia elipse pesada** (4.3-1b) k/6, kπ/64, 3π/32; conferência em pé e o centroide que achata junto |
| E5 | E5-1 a E5-4 | 3:17 | A; cartão | **Meia arruela** (4.3-1f): área 3π/2; 28/(9π) no buraco; fio de prumo; ρ = k r: 45/(14π) volta |
| E6 | E6-1 a E6-5 | 3:36 | 3D + A | **Pappus** (4.3-3): prova pelo anel e pelas cascas; a bola; a bola oca confere 28/(9π); a família (meio disco e arame); a rosquinha 4π² |
| S | S1, S2 | 1:25 | cartão | Os cinco erros; o cubo pesado do próximo vídeo; CTA com o desafio do buraco |

---

## 3. Matemática conferida

Notação: polares (r, θ), dA = r dr dθ; ρ = densidade; x̄, ȳ; M_x = ∬ y ρ dA; m = ∬ ρ dA. Substituição de Cálculo I com **w** (não u, porque u é coordenada nova em E1 e E2). Raio de bola e semieixo = **a** (e **b**), nunca R maiúsculo.

### 3.1 CONTA INTEIRA (o texto exato da coluna, linha a linha)

Cada bloco `Cn` é uma etapa da coluna (≤ 7 linhas; a coluna limpa entre etapas e o resultado reutilizado sobe como **chip**). Palavras em Space Grotesk (maiúsculas); matemática em MathTex. Cada `→` dentro de uma linha é um glyph map ou um degrau escrito a caneta, nunca um salto.

**C1a · E1-2 · passos 1 a 3**
```
PASSO 1   u = x        v = y − x²
PASSO 2   x = u        y = v + u²
PASSO 3   J = | ∂x/∂u  ∂x/∂v |  =  | 1   0 |
              | ∂y/∂u  ∂y/∂v |     | 2u  1 |
          J = 1 · 1 − 0 · 2u = 1        |J| = 1
```
**C1b · E1-2 · passo 4** (chip `|J| = 1` no topo)
```
y = 1 + x²   →   v = 1
y = 2 + x²   →   v = 2
x = 0        →   u = 0
y = x + x²   →   v = u
(0,1)→(0,1)   (0,2)→(0,2)   (1,2)→(1,1)   (2,6)→(2,2)
B_uv:  1 ≤ v ≤ 2,   0 ≤ u ≤ v
```
**C1c · E1-3 · passo 5**
```
∬_A e^{y−x²}/(y−x²) dA = ∫₁² ∫₀^v (e^v / v) · 1 du dv
DE DENTRO   ∫₀^v (e^v/v) du = (e^v/v) [u]₀^v
                            = (e^v/v)(v − 0) = e^v          (o par v/v acende e some)
DE FORA     ∫₁² e^v dv = [e^v]₁² = e² − e¹
          = e² − e ≈ 4,67
```
**C1d · E1-4 · conferência**
```
ÁREA DE B = (1 + 2)/2 · 1 = 3/2                  (BASES 1 E 2, ALTURA 1)
ÁREA DE A = ∫₀¹ [(2 + x²) − (1 + x²)] dx + ∫₁² [(2 + x²) − (x + x²)] dx
          = ∫₀¹ 1 dx + ∫₁² (2 − x) dx              (os x² acendem e somem)
          = [x]₀¹ + [2x − x²/2]₁²
          = (1 − 0) + [(4 − 2) − (2 − 1/2)]
          = 1 + 1/2 = 3/2  ✓
```

**C2a · E2-2 · passos 1 a 3**
```
PASSO 1   u = xy        v = y/x
PASSO 2   uv = y²       u/v = x²
          x = √(u/v)    y = √(uv)                 DERIVAR DÁ TRABALHO
PASSO 3   ∂(u,v)/∂(x,y) = | y       x  |
                          | −y/x²  1/x |
          = y · (1/x) − x · (−y/x²) = y/x + y/x = 2y/x = 2v
          ∂(x,y)/∂(u,v) · ∂(u,v)/∂(x,y) = 1       IR E VOLTAR = NÃO FAZER NADA
          J = 1/(2v)      |J| = 1/(2v)            (v > 0)
```
**C2b · E2-3 · área** (chip `|J| = 1/(2v)`)
```
B_uv = [1, 2] × [1, 2]
ÁREA = ∫₁² ∫₁² 1/(2v) du dv
DE DENTRO   (1/(2v)) [u]₁² = (1/(2v))(2 − 1) = 1/(2v)
DE FORA     (1/2) [ln v]₁² = (1/2)(ln 2 − ln 1)        (chip: ln 1 = 0)
          = (ln 2)/2 ≈ 0,347
PIPA = (1 · 1/√2)/2 = √2/4 ≈ 0,354                    (DIAGONAIS 1 E 1/√2)  ✓
```
**C2c · E2-4 · massa**
```
m = ∬_R xy dA = ∫₁² ∫₁² u · 1/(2v) du dv             (xy → u)
DE DENTRO   (1/(2v)) [u²/2]₁² = (1/(2v))(4/2 − 1/2) = (1/(2v)) · 3/2 = 3/(4v)
DE FORA     (3/4) [ln v]₁² = (3/4)(ln 2 − 0)
          = (3/4) ln 2 ≈ 0,520 kg
DENSIDADE MÉDIA = m / ÁREA = ((3/4) ln 2) / ((1/2) ln 2) = 3/2   ✓ (MEIO DE 1 E 2)
```

**C3 · E3 · oitavo de bola**
```
(leitura)  0 ≤ x ≤ a,   0 ≤ y ≤ √(a² − x²)   ⇒   y² = a² − x²   ⇒   x² + y² = a²
           z = √(a² − x² − y²)   ⇒   x² + y² + z² = a²
(etapa A)  x² + y² = r²        0 ≤ r ≤ a        0 ≤ θ ≤ π/2
           ∫₀^{π/2} ∫₀^a √(a² − r²) · r dr dθ
           w = a² − r²,   dw = −2r dr   ⇒   r dr = −dw/2
           r = 0 → w = a²          r = a → w = 0
           ∫_{a²}^0 √w (−dw/2) = (1/2) ∫₀^{a²} w^{1/2} dw          O MENOS INVERTE OS LIMITES
(etapa B)  (1/2) [(2/3) w^{3/2}]₀^{a²} = (1/2)(2/3)((a²)^{3/2} − 0) = a³/3
           (a³/3) [θ]₀^{π/2} = (a³/3)(π/2 − 0) = πa³/6
           (4πa³/3) ÷ 8 = 4πa³/24 = πa³/6   ✓
```

**C4a · E4-1 · elipse**
```
x²/a² + y²/b² ≤ 1           x = a r cos θ        y = b r sen θ
a²r²cos²θ/a² + b²r²sen²θ/b² = r²(cos²θ + sen²θ) = r² ≤ 1
J = | a cos θ   −a r sen θ |  = abr cos²θ + abr sen²θ = abr
    | b sen θ    b r cos θ |
A = 2 ∫₀^π ∫₀¹ abr dr dθ = 2ab [r²/2]₀¹ [θ]₀^π = 2ab · 1/2 · π = πab        METADE DE CIMA × 2
a = b  ⇒  πa²  ✓
```
**C4b · E4-2 · meia elipse, a massa**
```
x² + 4y² ≤ 1,  y ≥ 0        ρ = k y           x̄ = 0 (SIMETRIA)
a = 1,  b = 1/2:   x = r cos θ,   y = (1/2) r sen θ,   |J| = 1 · (1/2) · r = r/2
0 ≤ r ≤ 1,   0 ≤ θ ≤ π
m = ∫₀^π ∫₀¹ k · (r sen θ)/2 · r/2 dr dθ = (k/4) ∫₀^π sen θ dθ · ∫₀¹ r² dr        SEPARA: SÓ θ · SÓ r
[−cos θ]₀^π = −cos π + cos 0 = 1 + 1 = 2          [r³/3]₀¹ = 1/3
m = (k/4) · 2 · (1/3) = k/6
```
**C4c · E4-3 · o momento e ȳ** (chip `m = k/6`)
```
M_x = ∬ y ρ dA = ∫₀^π ∫₀¹ ((r sen θ)/2)² · k · r/2 dr dθ = (k/8) ∫₀^π sen²θ dθ · ∫₀¹ r³ dr
sen²θ = (1 − cos 2θ)/2         [θ/2 − sen 2θ/4]₀^π = π/2 − (sen 2π)/4 − 0 = π/2
[r⁴/4]₀¹ = 1/4
M_x = (k/8) · (π/2) · (1/4) = kπ/64
ȳ = M_x/m = (kπ/64)/(k/6) = (kπ/64) · (6/k) = 6π/64 = 3π/32 ≈ 0,295
```
**C4d · E4-4 · conferência e comparação**
```
m = ∫₋₁¹ ∫₀^{√(1−x²)/2} k y dy dx
DE DENTRO   k [y²/2]₀^{√(1−x²)/2} = k · (1/2) · (1 − x²)/4 = k(1 − x²)/8
DE FORA     (k/8) [x − x³/3]₋₁¹ = (k/8)(2/3 + 2/3) = (k/8)(4/3) = k/6   ✓
HOMOGÊNEA   4b/(3π) = 4 · (1/2)/(3π) = 2/(3π) ≈ 0,212        (ρ = k y: 0,295)
```

**C5a · E5-1 · meia arruela, a área**
```
B: 1 ≤ r ≤ 2,   0 ≤ θ ≤ π          x̄ = 0 (SIMETRIA)         ρ = 1
A = ∫₀^π ∫₁² r dr dθ
DE DENTRO   [r²/2]₁² = 4/2 − 1/2 = 3/2
DE FORA     (3/2) [θ]₀^π = (3/2) π
A = 3π/2
π · 2²/2 − π · 1²/2 = 2π − π/2 = 3π/2   ✓
```
**C5b · E5-2 · o momento** (chip `A = 3π/2`)
```
M_x = ∬ y dA = ∫₀^π ∫₁² r sen θ · r dr dθ
DE DENTRO   sen θ [r³/3]₁² = sen θ (8/3 − 1/3) = (7/3) sen θ
DE FORA     (7/3) [−cos θ]₀^π = (7/3)(1 + 1) = 14/3
ȳ = (14/3)/(3π/2) = (14/3) · (2/(3π)) = 28/(9π) ≈ 0,990 < 1        NO BURACO
```
**C5c · E5-4 · ρ = k r** (duas etapas; chips `m = 7kπ/3` e `∫₀^π sen θ dθ = 2`)
```
m = ∫₀^π ∫₁² (k r) · r dr dθ                     (chaves DENSIDADE · JACOBIANO)
DE DENTRO   k [r³/3]₁² = k (8/3 − 1/3) = 7k/3
DE FORA     (7k/3) [θ]₀^π = 7kπ/3
---
M_x = ∫₀^π ∫₁² r sen θ · k r · r dr dθ
DE DENTRO   k sen θ [r⁴/4]₁² = k sen θ (16/4 − 1/4) = (15k/4) sen θ
DE FORA     (15k/4) · 2 = 15k/2
ȳ = (15k/2)/(7kπ/3) = (15k/2) · (3/(7kπ)) = 45/(14π) ≈ 1,023 > 1      VOLTA PARA A CHAPA
```

**C6a · E6-1 · Pappus**
```
ΔV ≈ 2πy ΔA
V = ∬_B 2πy dA = 2π ∬_B y dA = 2π M_x = 2π ȳ A          (ȳ = M_x/A, CHAPA HOMOGÊNEA)
VOLUME = ÁREA × CAMINHO DO CENTROIDE
∬_B 2πy dA = ∫₀^a 2πy L(y) dy                           CASCAS DO CÁLCULO I
```
**C6b · E6-2 · a bola**
```
ȳ = 4a/(3π)        A = πa²/2
V = 2π · 4a/(3π) · πa²/2 = 8a/3 · πa²/2 = 8πa³/6 = 4πa³/3   ✓
```
**C6c · E6-3 · a bola oca** (chips `A = 3π/2` e `28/(9π)`)
```
V = (4/3)π · 2³ − (4/3)π · 1³ = (4/3)π (8 − 1) = 28π/3
V = 2π ȳ A   ⇒   ȳ = V/(2πA)
ȳ = (28π/3)/(2π · 3π/2)          2π · 3π/2 = 3π²
ȳ = (28π/3) · 1/(3π²) = 28/(9π)   ✓  O MESMO NÚMERO
```
**C6d · E6-4 · a família**
```
ȳ = (4/3)π(b³ − a³) / (2π · (π/2)(b² − a²)) = 4(b³ − a³) / (3π(b² − a²))
b³ − a³ = (b − a)(a² + ab + b²)        b² − a² = (b − a)(a + b)
ȳ = 4(a² + ab + b²) / (3π(a + b))
a = 0:   4b²/(3πb) = 4b/(3π)                        MEIO DISCO
a = b:   4 · 3b²/(3π · 2b) = 2b/π ≈ 0,64 b          ARAME
```
**C6e · E6-5 · a rosquinha**
```
V = 2π · 2 · π · 1² = 4π² ≈ 39,5
```

### 3.2 Pontos de rigor (o que a fala respeita)

- **Hipóteses do teorema (EP. 11) em cada troca.** E1: φ(u, v) = (u, v + u²) é C¹ e bijetora no plano todo, inversa (x, y − x²), J = 1 ≠ 0. E2: φ(u, v) = (√(u/v), √(uv)) no aberto u, v > 0, C¹, injetora, J = 1/(2v) ≠ 0. Polares (E3, E4-2, E5) em retângulos com θ dentro de [0, π] ou [0, π/2]: φ leva o interior no interior, sem a costura de θ = 0 = 2π. **Elipse inteira (E4-1):** como no disco do EP. 12, a conta vai pela metade de cima e dobra, para não usar o retângulo [0, 1] × [0, 2π], em que φ(interior) ≠ interior.
- **"Trava" no E1:** a primitiva de e^w/w é a integral exponencial, não elementar. A fala diz "não se escreve com as funções do Cálculo um", como no EP. 09/11.
- **Jacobiano da volta (E2):** ψ ∘ φ = identidade ⇒ Jψ · Jφ = I (regra da cadeia) ⇒ det(Jφ) · det(Jψ) = 1. A fala diz "pela regra da cadeia". É a mesma conferência ida × volta do trapézio do EP. 11 (−2 × −1/2 = 1), agora usada como ferramenta.
- **Pipa (E2-3):** as diagonais (1, 1)–(1, 2) e (1/√2, √2)–(√2, √2) são perpendiculares (vertical e horizontal), então a área da pipa é d₁d₂/2. Os lados ao longo das retas coincidem com a região; só os lados das hipérboles diferem, e para lados opostos (a hipérbole de baixo deixa a região maior que a pipa; a de cima, menor). A fala diz "tiram um tiquinho de um lado e põem do outro" e não afirma igualdade: 0,347 contra 0,354.
- **Densidade média (E2-4):** como |J| só depende de v, a média de u ponderada pela área é a média simples de u em [1, 2], 3/2. Não é uma coincidência numérica.
- **Separar a integral (E4):** integrando produto g(θ) h(r) num retângulo ⇒ produto das integrais (Fubini + linearidade). Selo `SEPARA`.
- **Centroide que achata (E4-4):** a transformação (x, y) ↦ (x, y/2) leva o meio disco na meia elipse e multiplica toda área por 1/2; médias de posição vão junto. Fica como frase e imagem; o número 2/(3π) sai da fórmula do meio disco com b = 1/2. A densidade k y também é "distância ao eixo" depois de achatar, por isso 3π/16 vira 3π/32 (conferido no script, não entra na tela).
- **Meia arruela:** "homogênea" com ρ = 1 ⇒ m = A em número. O ⊕ em 0,990 está no buraco por 0,01 (a lupa ×10 deixa ver).
- **Pappus (E6-1):** vale para chapa homogênea de um lado só do eixo. A prova honesta é a das cascas: fatia deitada de comprimento L(y) vira casca de volume 2πy L(y) dy, e por Fubini ∫ 2πy L(y) dy = ∬ 2πy dA. O "anel 2πy ΔA" é a intuição; a fala diz as duas.
- **Arame (E6-4):** limite a → b da fórmula contínua; confere com o centro de massa do arame semicircular, 2b/π (∫₀^π b sen θ dθ / π). A fala diz "a chapa vira um arame".
- **Densidade com unidade:** em E2, ρ = xy em kg/m² (x, y em m) — a fala diz "quilos" no resultado; em E4/E5 o k carrega a unidade e cancela em ȳ.

---

## 4. Direção visual

### 4.1 Layouts (os da série)
- **A · palco + coluna:** palco à esquerda, coluna em x = 1080–1160. Grade de quadradinhos **da tela inteira** nascendo dos eixos do palco (`papel(ax)` sem `area`). Coluna ≤ 7 linhas por etapa, com chip no topo.
- **B · dois planos + coluna:** xy à esquerda, uv no meio, coluna em x = 1160 (E1-2, E1-4, E2-2). Cada plano com a grade dele, emenda vertical no meio do vão.
- **3D:** Three.js `octante` (E3) e `pappus` (E6), fundo violeta liso; a grade entra no pouso para o 2D.
- **Cartões** (H2, A1, E5-3, S1, S2): `papel(passo=0.5)` de borda a borda.

### 4.2 Cores (as da série; nada novo além do w)
| Papel | Cor |
|---|---|
| x, x̄, tira em pé, `a` como semieixo em x | âmbar `#FFC24D` |
| y, ȳ, M_x, tira deitada, `b`, cateto y = r sen θ | magenta `#EA63FF` |
| u e r / v e θ | laranja `#FF9440` / verde-água `#2EE6A6` (EP. 11–12) |
| J, \|J\|, o r do jacobiano, a célula | lima `#C6F26B` |
| ρ, k, m, mapas de densidade | ciano `#35D9FF` |
| w (substituição do Cálculo I) | lilás `#C9A7FF` |
| entrada / saída da fatia | azul-claro `#7FB2FF` / coral `#FF7A8A` |
| regiões, lápis, alfinete, fio, ícones, cartões | GEO `#B8C4DA` |
| `TRAVA`, `NO BURACO`, a borda r = 1 em E5, ✗ do S1 | ALERTA `#FF5D5D` |
| ✓, `VOLTA PARA A CHAPA`, `O MESMO NÚMERO`, molduras de resultado | menta `#8CFFD2` |
| ⊕ centro de massa / ⊕ vazado centroide | degradê ciano → magenta / branco `#F5F7FF` |

Operadores e colchetes em branco. A grandeza leva a cor.

### 4.3 Bloco a bloco (o essencial; o storyboard completo está na Tela de cada âncora, Anexo A)
- **H1:** 2D puro (não 3D): a meia arruela nasce do meio disco grande; o ⊕ com `?` anda no eixo; a borda r = 1 acende ALERTA no "abaixo de um"; o mapa ρ = k r pinta por cima. Ícones de bola e bola oca em traço no fim (promessa do E6).
- **E1:** o movimento-assinatura é a **tira que escorrega** (J = 1) e as **bordas que voam** de um plano para o outro com a equação nova.
- **E2:** a grade de hipérboles e raios cobre a região; a célula lima mostra o fator 1/(2v) (encolhe para cima, onde v é maior).
- **E3:** 3D `octante` só no "um oitavo de bola" e no pouso; a conta é 2D com o raio varrendo.
- **E4:** um movimento: o círculo estica em elipse (a célula junto). No E4-4, o meio disco achata (o ⊕ vazado desce junto).
- **E5:** a lupa ×10 na borda do buraco; o fio de prumo (rotação simples em torno do alfinete, sem balanço); a régua em pé do 0,98 ao 1,03.
- **E6:** 3D `pappus`, um giro por forma (6 s), câmera parada durante o giro. O círculo do centroide é tracejado magenta.
- **S2:** o cubo é extrusão 2D em perspectiva fixa feita no Manim (a chapa ganha altura), não uma cena 3D nova.

---

## 5. Reserva e corte

- **Para cortar (só se o vídeo passar de 28 min), nesta ordem:** (1) E6-5 rosquinha (−0:25); (2) E2-3 perde a pipa e fica só com a conta (−0:25); (3) E4-4 perde a conferência em pé e fica só com a comparação homogênea (−0:30); (4) E5-3 fio de prumo vira uma frase (−0:25); (5) E6-4 perde o caso a = 0 (fica o arame) (−0:15). Economia ≈ 2:00. **Não cortar:** a meia arruela inteira (cumpre o gancho), Pappus conferindo 28/(9π) (é o clímax), o jacobiano da volta (é a habilidade nova do E2), a conta inteira de qualquer exercício.
- **Reserva (não entra):** o paralelogramo ∛(y² − x²) do Guidorizzi 4.2-3 (9/32, |J| = 1/2: repete o trapézio do EP. 11); o disco x² + y² ≤ x com ∬ x dA = π/8 (cos⁴θ; bom para esféricas/cilíndricas depois); o triângulo com ρ = k √(x² + y²) (precisa de ∫ sec³θ); a vazão no cano (Poiseuille); o limiar do buraco a/b ≈ 0,494 vai para os comentários (desafio do CTA).

---

## 6. Decisões (recomendo todas; o Kaio decide)

1. **Número:** `yt_0039` · CÁLCULO III · **EP. 14** (combinado com as threads do 3.5-T1 e do 3.5-T2). Recomendo.
2. **Duração ≈ 25–27 min** (voz ≈ 24:12). Fica dentro dos 25–30 pedidos e deixa folga para a conta inteira esticar no render (o EP. 10 foi de 26 para 37 min com as escadas acrescentadas depois; aqui as escadas já estão completas desde a v1). Recomendo.
3. **Seis problemas** (parábolas, hipérboles, oitavo de bola, elipse + meia elipse pesada, meia arruela, Pappus), com conferência em todos. Alternativa: tirar o E2 (hipérboles) e ficar em ≈ 22 min; perde o jacobiano da volta, que é a habilidade que falta no módulo. Recomendo os seis.
4. **Pappus no fim** (Guidorizzi 4.3-3) como conferência sem integral da meia arruela, mais a família (meio disco e arame) e a rosquinha. É o "caso famoso" do módulo e a ponte natural para sólidos (o 3.5). Recomendo.
5. **H1 em 2D** (a meia arruela e o ⊕ com `?`), sem o lápis 3D: com o ponto no buraco não há onde apoiar o lápis, e o fio de prumo do E5-3 faz esse papel. Alternativa: lápis 3D com o ponto no ar. Recomendo o 2D.
6. **Duas cenas Three.js** (`octante`, `pappus`); o resto em Manim 2D. Recomendo.
7. **w para a substituição** do Cálculo I (u e v são coordenadas neste vídeo). Recomendo.
8. **Gancho do S2: o cubo de lado 2 com densidade x² + y² + z²** (combinado com a thread do 3.5-T1, que abre por ele). O desafio do CTA é o limiar do buraco (a/b ≈ 0,494, resposta não vai para a tela). Recomendo.

---

## 7. Observações

- Nenhuma fala cita "vídeo passado" ou "aula passada" (regra do projeto desde o EP. 10). O que vem do módulo entra como ferramenta: "o jacobiano", "o fator erre das polares", "o centroide do meio disco homogêneo, quatro á sobre três pi", "como no disco, metade de cima e dobra".
- **θ = "téta"** em toda a fala e em todos os gatilhos.
- Letras para a voz: "u", "vê", "dáblio" (w), "rô" (ρ), "cá" (k), "á" e "bê" (raio e semieixos), "xis barra", "ípsilon barra", "éle de ípsilon" (L(y)), "bê u vê" (B_uv). O ∂ não é lido sozinho.
- `docs/mapa_curricular.md` no repositório ainda usa a numeração antiga; a ficha leva `modulo: 3.4` com a nota, como nos EP. anteriores.
- Atlas: depois da entrega, yt_0039 entra como "Em produção" no 3.4-E1.

---

## Anexo A · Narração v1

Cópia integral de `yt_0039_narracao_v1.md` (abaixo).


# yt_0039 · CÁLCULO III · EP. 14 · Exercícios do módulo: jacobiano, polares e centro de massa
## Narração v1 (com tags do ElevenLabs v4) · por âncora, com a Tela e os Gatilhos

2026-11-15. Base: proposta `calculo3_34e1_exercicios_integradores_proposta_v1.md`. Todos os números saem de `verificacao/verifica_calc3_34e1_sympy.py` (67/67 True).

Regras desta fala:
- Tags permitidas: [curious], [thoughtful], [serious], [surprised], [happy], [excited]. Uma por parágrafo (o S2 tem duas, como nos EP. anteriores). Sem [slowly], sem [slow, measured pace], sem [pause].
- Números por extenso. Letras soletradas como hoje: "xis", "ípsilon", "erre", "á", "bê", "cá", "u", "vê", "dáblio", "rô", "eme". **θ é sempre "téta"** (nunca "teta" nem o símbolo).
- Nenhuma fala cita outro vídeo como "vídeo passado" ou "aula passada". O que o aluno já viu entra como ferramenta conhecida ("o jacobiano", "o fator erre das polares", "o centro de massa do meio disco").
- Conta inteira: cada degrau que está na coluna é lido. Nada de "dá" pulando degrau.
- Cadência 3 palavras/s.

### Tempo por âncora

| Âncora | Trecho | Palavras | Voz (s) | Início estimado |
|---|---|---:|---:|---:|
| H1 | a chapa que equilibra no buraco? | 146 | 48.7 | 0:00 |
| H2 | cinco passos e uma divisão | 95 | 31.7 | 0:48 |
| A1 | bem-vindos | 57 | 19.0 | 1:20 |
| E1-1 | a faixa entre parábolas: trava | 141 | 47.0 | 1:39 |
| E1-2 | os passos um a quatro | 242 | 80.7 | 2:26 |
| E1-3 | a conta: o comprimento cancela | 131 | 43.7 | 3:47 |
| E1-4 | conferindo pela área | 164 | 54.7 | 4:30 |
| E2-1 | as hipérboles: dois pedaços | 136 | 45.3 | 5:25 |
| E2-2 | o jacobiano da volta | 212 | 70.7 | 6:10 |
| E2-3 | a área e a pipa | 196 | 65.3 | 7:21 |
| E2-4 | a massa e a densidade média | 158 | 52.7 | 8:26 |
| E3-1 | ler a região nos limites | 148 | 49.3 | 9:19 |
| E3-2 | polares e o oitavo de bola | 223 | 74.3 | 10:08 |
| E4-1 | a elipse: polares esticadas | 229 | 76.3 | 11:23 |
| E4-2 | a meia elipse pesada: a massa | 214 | 71.3 | 12:39 |
| E4-3 | o momento e o centro de massa | 205 | 68.3 | 13:50 |
| E4-4 | conferindo a massa e comparando | 165 | 55.0 | 14:59 |
| E5-1 | a meia arruela: a área | 141 | 47.0 | 15:54 |
| E5-2 | o momento e o buraco | 155 | 51.7 | 16:41 |
| E5-3 | o fio de prumo | 98 | 32.7 | 17:32 |
| E5-4 | a borda mais pesada | 198 | 66.0 | 18:05 |
| E6-1 | Pappus: o volume pelo centroide | 165 | 55.0 | 19:11 |
| E6-2 | a bola confere o meio disco | 98 | 32.7 | 20:06 |
| E6-3 | a casca confere a meia arruela | 137 | 45.7 | 20:39 |
| E6-4 | a família: do meio disco ao arame | 184 | 61.3 | 21:24 |
| E6-5 | a rosquinha | 64 | 21.3 | 22:26 |
| S1 | síntese: os cinco erros | 128 | 42.7 | 22:47 |
| S2 | o próximo vídeo e CTA | 127 | 42.3 | 23:30 |
| **Total** | | **4.357** | **24:12** | |

Com as respirações entre âncoras e as esperas de leitura das contas (o padrão da série é ≈ +6 %), o vídeo fica em **≈ 25–26 min**; a conta inteira na tela costuma esticar mais 1 a 2 min no render.

---

### H1 · a chapa que equilibra no buraco?
**Tela:** layout A sem coluna, grade da tela inteira nascendo dos eixos (origem em (960, 820), 1 = 220 px). (1) O meio disco de raio 2 nasce em GEO translúcido; o meio disco de raio 1 **sai** dele (recorte com contorno tracejado), e fica a meia arruela. (2) `HOMOGÊNEA` (placa). (3) O eixo y acende branco tracejado (`SIMETRIA`). (4) Um ⊕ com `?` sobe e desce no eixo, entre y = 0,6 e y = 1,4, e para perto da borda do buraco (y ≈ 1), sem número. A borda r = 1 acende em ALERTA no gatilho "abaixo de um": a faixa 0 ≤ y < 1 do eixo vira `BURACO` (ALERTA). (5) O mapa radial ρ = k r (ciano, cresce para fora) pinta a chapa; `MAIS PESADA NA BORDA` em ciano; o ⊕ dá um pulinho para cima com `?`. (6) No fim, no canto inferior direito, entram dois ícones em traço GEO: uma bola e uma bola cortada ao meio (oca), com `SEM INTEGRAL` embaixo.
Canto: `A CHAPA E O BURACO`.
**Gatilhos:** "Olha esta chapa"→meio disco grande · "tira, do meio dele"→recorte · "meia arruela"→rótulo · "homogênea"→placa · "Pela simetria"→eixo acende · "Mas em que altura"→⊕ com ? anda · "abaixo de um"→borda r = 1 em ALERTA e `BURACO` · "a borda de fora pesar mais"→mapa ρ = k r e legenda · "sobe de volta"→⊕ pula · "uma bola e uma bola oca"→dois ícones e `SEM INTEGRAL`
> [curious] Olha esta chapa. É o que sobra de um meio disco de raio dois quando a gente tira, do meio dele, um meio disco de raio um. Ficou uma meia arruela. E ela é homogênea: a mesma densidade em todo ponto. A pergunta é: onde fica o centro de massa dela, o ponto em que ela equilibra? Pela simetria, ele está em cima do eixo ípsilon. Mas em que altura? Se a altura der abaixo de um, o centro de massa cai no buraco: num lugar onde não tem chapa nenhuma. E se a borda de fora pesar mais, com a densidade crescendo com a distância até o centro? Será que ele sobe de volta para a chapa? Hoje a gente responde as duas perguntas, com a conta inteira. E, no fim, uma bola e uma bola oca vão conferir esse número sem fazer integral nenhuma.

### H2 · cinco passos e uma divisão
**Tela:** cartão sem gráfico (grade padrão, passo 0,5). Coluna central (x = 560) a caneta, um item por gatilho, cada número num círculo GEO: `1 · ESCOLHER AS VARIÁVEIS NOVAS` · `2 · ESCREVER` `x, y` `EM FUNÇÃO DELAS` · `3 · JACOBIANO, EM MÓDULO` (com `|J|` em lima) · `4 · DESENHAR A REGIÃO NOVA` · `5 · CALCULAR E CONFERIR` (✓ menta). À direita (x = 1300), num painel: `CENTRO DE MASSA` / `\bar y = \dfrac{M_x}{m}` (M_x magenta, m ciano) / `MOMENTO ÷ MASSA`.
**Gatilhos:** "cinco passos"→painel · "escolher as variáveis"→1 · "xis e ípsilon em função delas"→2 · "o jacobiano"→3 · "a região nova"→4 · "calcular e conferir"→5 com ✓ · "uma divisão só"→painel da direita · "momento sobre massa"→fórmula
> [serious] Este vídeo junta o módulo inteiro, e tudo cabe em cinco passos e uma divisão. Toda troca de variáveis segue os mesmos cinco passos: escolher as variáveis novas; escrever xis e ípsilon em função delas; calcular o jacobiano e tomar o módulo; desenhar a região nova, borda por borda; e calcular e conferir por outro caminho. E o centro de massa é sempre uma divisão só: momento sobre massa. A ordem de hoje é a do módulo: primeiro o jacobiano, depois as polares, depois massa e centro de massa, e no fim a meia arruela.

### A1 · bem-vindos
**Tela:** logo; `EXERCÍCIOS DO MÓDULO`; embaixo, seis chips numerados que acendem um a um: `1 PARÁBOLAS` · `2 HIPÉRBOLES` · `3 OITAVO DE BOLA` · `4 ELIPSE` · `5 MEIA ARRUELA` · `6 PAPPUS`.
**Gatilhos:** "Bem-vindos"→logo · "seis problemas"→título · "duas parábolas"…"o teorema de Pappus"→os seis chips, um por item falado
> [happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Hoje é dia de exercício: seis problemas que começam parecidos e vão ficando mais espertos. Duas parábolas, duas hipérboles, um oitavo de bola, uma elipse, a meia arruela e, no fim, o teorema de Pappus. Pega papel e lápis: em cada um tem a hora de pausar o vídeo e tentar.

### E1-1 · a faixa entre parábolas: trava
**Tela:** layout A. Palco xy à esquerda (origem em (300, 960), 1 = 130 px; x de 0 a 2,4, y de 0 a 6,6), grade da tela inteira. As curvas nascem uma por gatilho: `y = 1 + x²` e `y = 2 + x²` (GEO), `y = x + x²` (GEO tracejado fino), o eixo `x = 0`; a região A acende em GEO translúcido, com os quatro cantos (0, 1), (0, 2), (1, 2), (2, 6) em pontos brancos pequenos. Coluna (x = 1080): o enunciado `\iint_A \dfrac{e^{y-x^2}}{y-x^2}\,dA` a caneta e a etiqueta `PAUSE E TENTE` ao lado. Tira em pé âmbar com a placa `TRAVA`; tira deitada magenta com `TRAVA`. Depois `y − x²` acende verde-água no expoente **e** no denominador; as bordas `y = 1 + x²` e `y = 2 + x²` acendem verde-água.
Canto: `1 · A FAIXA ENTRE PARÁBOLAS`.
**Gatilhos:** "Primeiro problema"→palco · "um mais xis ao quadrado"→curva 1 · "dois mais xis ao quadrado"→curva 2 · "xis mais xis ao quadrado"→curva 3 · "xis maior ou igual a zero"→eixo e região · "a integral dupla"→enunciado · "pausa o vídeo"→`PAUSE E TENTE` · "em pé"→tira âmbar · "Trava"→placa 1 · "deitada"→tira magenta · "trava também"→placa 2 · "ípsilon menos xis ao quadrado"→acende no integrando · "as bordas também"→bordas acendem
> [curious] Primeiro problema. A região A fica entre a parábola ípsilon igual a um mais xis ao quadrado e a parábola ípsilon igual a dois mais xis ao quadrado, acima da curva ípsilon igual a xis mais xis ao quadrado, com xis maior ou igual a zero. Calcule a integral dupla, em A, de é elevado a ípsilon menos xis ao quadrado, sobre ípsilon menos xis ao quadrado. Se quiser, pausa o vídeo e tenta. Fatia em pé: a integral de dentro, em ípsilon, pede a primitiva de é elevado a alguma coisa sobre essa mesma coisa, que não se escreve com as funções do Cálculo um. Trava. Fatia deitada: trava também. Agora repara: o integrando só enxerga ípsilon menos xis ao quadrado. E as bordas também: duas delas são ípsilon menos xis ao quadrado igual a um e igual a dois.

### E1-2 · os passos um a quatro
**Tela:** layout B: palco xy à esquerda (o mesmo), plano u, v no meio (origem em (640, 760), 1 = 170 px; u de 0 a 2,3 laranja, v de 0 a 2,3 verde-água), coluna em x = 1160. Coluna C1a (passos 1 a 3) e depois C1b (passo 4), em duas etapas (a coluna limpa entre elas, e o chip `|J| = 1` fica no topo). Passo 1: `u = x`, `v = y − x²` (o `y − x²` **voa** do expoente). Passo 2: `x = u`, `y = v + u²` (glyph map: o `x²` vira `u²` e atravessa a igualdade). Passo 3: a matriz das derivadas, o determinante, `|J| = 1` em lima. No palco xy, uma tira em pé âmbar fina (x = 0,6) **escorrega para baixo** sem esticar até o plano u, v (selo `SÓ ESCORREGA`). Passo 4: cada borda acende no xy e **voa** para o plano u, v já como a borda nova: `v = 1`, `v = 2`, `u = 0`, `v = u` (coral, saída); os quatro cantos com as coordenadas antes → depois. Fica o trapézio `B_{uv}` em GEO translúcido.
**Gatilhos:** "Passo um"→`u`, `v` · "Passo dois"→glyph map · "Passo três"→matriz · "um, zero"→1ª linha · "dois u, um"→2ª linha · "um vezes um"→det · "o jacobiano é um"→`|J| = 1` · "só escorrega"→a tira desce · "Passo quatro"→coluna limpa, chip `|J| = 1` sobe · "vê igual a um"…"vê igual a u"→as quatro bordas voam · "Os cantos conferem"→cantos · "um trapézio"→B_uv acende
> [thoughtful] Passo um: escolher. Chama xis de u, e ípsilon menos xis ao quadrado de vê. Passo dois: xis e ípsilon em função de u e vê. Xis é u. E, de vê igual a ípsilon menos xis ao quadrado, ípsilon é vê mais u ao quadrado. Passo três: o jacobiano. A derivada de xis em relação a u é um, em relação a vê, zero: a primeira linha é um, zero. A de ípsilon em relação a u é dois u, e em relação a vê, um: a segunda linha é dois u, um. O determinante: um vezes um, menos zero vezes dois u. O jacobiano é um. Faz sentido: com xis parado, ípsilon só perde xis ao quadrado. Cada fatia em pé só escorrega para baixo, sem esticar, e a área não muda. Passo quatro: a região nova, borda por borda. Ípsilon igual a um mais xis ao quadrado vira vê igual a um. Ípsilon igual a dois mais xis ao quadrado vira vê igual a dois. Xis igual a zero vira u igual a zero. E ípsilon igual a xis mais xis ao quadrado vira vê igual a u. Os cantos conferem: zero, um fica zero, um; zero, dois fica zero, dois; um, dois vai para um, um; e dois, seis vai para dois, dois. No plano u vê, a região é um trapézio: vê vai de um a dois, e, para cada vê, u vai de zero até vê.

### E1-3 · a conta: o comprimento cancela
**Tela:** layout A com o plano u, v no palco (o trapézio, uma tira deitada verde-água em v = 1,5: entrada azul-claro em u = 0, saída coral em u = v, chave `COMPRIMENTO v` embaixo dela). Coluna C1c por glyph maps: a integral montada (o `1` lima voa do chip; os limites voam do palco: `0` da entrada, `v` da saída, `1` e `2` das bordas); `DE DENTRO` (Space Grotesk) + a linha da integral de dentro; `[u]₀^v`; `(v − 0)`; o par `v`/`v` acende e some junto; `= e^v`; a de fora; `[e^v]₁²`; `e² − e¹`; `= e² − e ≈ 4,67` em menta, com ✓ e sem moldura.
**Gatilhos:** "Passo cinco"→integral montada · "vezes o módulo do jacobiano"→o `1` voa · "a de dentro"→linha de dentro · "não depende de u"→`e^v/v` acende, sai para fora · "u, de zero a vê"→`[u]₀^v` · "vê menos zero"→`(v − 0)` · "cancela"→o par some · "Sobra é elevado a vê"→`e^v` · "A de fora"→linha de fora · "é ao quadrado menos é"→resultado
> [excited] Passo cinco: calcular. A integral vira a integral de um a dois, da integral de zero a vê, de é elevado a vê sobre vê, vezes o módulo do jacobiano, que é um, dê u dê vê. A de dentro é em u, e é elevado a vê sobre vê não depende de u: sai da integral. Sobra a integral de dê u, que é u, de zero a vê: vê menos zero. E esse vê, o comprimento da fatia, cancela o vê de baixo. Sobra é elevado a vê. A de fora: a primitiva de é elevado a vê é ela mesma, de um a dois: é ao quadrado menos é elevado a um. A resposta é é ao quadrado menos é, mais ou menos quatro vírgula sessenta e sete.

### E1-4 · conferindo pela área
**Tela:** layout B (xy à esquerda, u, v no meio). Coluna C1d. Primeiro, no u, v: chaves `BASE 1` (em v = 1) e `BASE 2` (em v = 2), `ALTURA 1`; `ÁREA DE B = \dfrac{1+2}{2}\cdot 1 = \dfrac{3}{2}` (os três números voam das chaves). Depois no xy: tira em pé em x = 0,5 (entrada azul-claro em `1 + x²`, saída coral em `2 + x²`, chave `COMPRIMENTO 1`) e tira em x = 1,5 (entrada em `x + x²`, saída em `2 + x²`, chave `2 − x`); a coluna escreve as duas integrais com os colchetes e o resultado `= 3/2 ✓`. As duas áreas ficam lado a lado com `=` grande menta entre os dois palcos.
**Gatilhos:** "conferir pela área"→coluna limpa · "a área de B"→chaves no trapézio · "três meios"→conta do trapézio · "fatia em pé"→tira 1 · "o xis ao quadrado cancela"→os dois `x²` acendem e somem · "de um a dois"→tira 2 · "dois menos xis"→chave · "um meio"→colchete · "três meios de novo"→✓ e `=` menta
> [thoughtful] E como conferir? Pela área, que o jacobiano um promete conservar. A área de bê u vê é a de um trapézio: bases um e dois, altura um. Base média vezes altura: um mais dois sobre dois, vezes um, três meios. Agora a área de A direto em xis e ípsilon, fatiando em pé. De zero a um, a fatia sai em dois mais xis ao quadrado e entra em um mais xis ao quadrado: o xis ao quadrado cancela e o comprimento é um. De um a dois, ela entra em xis mais xis ao quadrado e sai em dois mais xis ao quadrado: comprimento dois menos xis. A primeira: xis de zero a um, um menos zero, um. A segunda: a primitiva é dois xis menos xis ao quadrado sobre dois; em dois, quatro menos dois; em um, dois menos um meio; a diferença é um meio. Um mais um meio: três meios de novo. A troca não ganhou nem perdeu área.

### E2-1 · as hipérboles: dois pedaços
**Tela:** layout A. Palco xy (origem em (260, 940), 1 = 330 px; x de 0 a 1,6, y de 0 a 2,3); as hipérboles `xy = 1`, `xy = 2` (GEO) e as retas `y = x`, `y = 2x` (GEO); a região R acende em GEO translúcido; os quatro cantos com pontos brancos. Enunciado na coluna: `ÁREA DE R` e `MASSA DE R COM` `\rho = xy` (ρ ciano), `PAUSE E TENTE`. Duas tiras em pé (x = 0,85 e x = 1,2) com entrada azul-claro e saída coral mostram a troca: à esquerda entra na hipérbole `xy = 1` e sai na reta `y = 2x`; à direita entra na reta `y = x` e sai na hipérbole `xy = 2`; tracejado vertical em `x = 1` e as marcas `\dfrac{1}{\sqrt2}` e `\sqrt2` no eixo; placa `2 INTEGRAIS` em ALERTA.
Canto: `2 · AS HIPÉRBOLES`.
**Gatilhos:** "Segundo problema"→palco · "xis ípsilon igual a um"→hipérbole 1 · "igual a dois"→hipérbole 2 · "ípsilon igual a xis"→reta 1 · "dois xis"→reta 2 · "a área"→enunciado 1 · "a massa"→enunciado 2 · "Pausa e tenta"→`PAUSE E TENTE` · "um sobre raiz de dois até raiz de dois"→marcas · "as bordas trocam"→tracejado em x = 1 · "entra na hipérbole de baixo"→tira 1 · "entra na reta de baixo"→tira 2 · "duas integrais"→placa
> [curious] Segundo problema. A região erre fica no primeiro quadrante, entre as hipérboles xis ípsilon igual a um e xis ípsilon igual a dois, e entre as retas ípsilon igual a xis e ípsilon igual a dois xis. Calcule a área dela, e a massa de uma chapa com esse formato e densidade rô igual a xis vezes ípsilon. Pausa e tenta. Fatiando em pé, a fatia vai de um sobre raiz de dois até raiz de dois, e em xis igual a um as bordas trocam: até ali ela entra na hipérbole de baixo e sai na reta de cima; depois, entra na reta de baixo e sai na hipérbole de cima. Seriam duas integrais, cada uma com o seu logaritmo. Mas olha as bordas de novo: são xis ípsilon constante e ípsilon sobre xis constante.

### E2-2 · o jacobiano da volta
**Tela:** layout B (xy à esquerda, plano u, v no meio, coluna em x = 1160). Coluna C2a. Passo 1: `u = xy`, `v = y/x` (u laranja, v verde-água); as hipérboles acendem laranja, as retas verde-água; a grade nova (hipérboles e raios) cobre a região. Passo 2: `uv = y²`, `u/v = x²` ⇒ `x = \sqrt{u/v}`, `y = \sqrt{uv}`; as raízes ganham a placa `DERIVAR DÁ TRABALHO`. Passo 3 pelo **atalho**: a matriz `\dfrac{\partial(u,v)}{\partial(x,y)}` com as quatro derivadas a caneta, uma por gatilho (`y`, `x`, `-y/x^2`, `1/x`); o determinante `y·\dfrac1x − x·\left(−\dfrac{y}{x^2}\right) = \dfrac{y}{x}+\dfrac{y}{x} = \dfrac{2y}{x} = 2v` (o `y/x` vira `v` por glyph map); depois a linha-regra `\dfrac{\partial(x,y)}{\partial(u,v)}\cdot\dfrac{\partial(u,v)}{\partial(x,y)} = 1` com o selo `IR E VOLTAR = NÃO FAZER NADA`; `J = \dfrac{1}{2v}` e `|J| = \dfrac{1}{2v}` (v > 0) em lima. No palco, uma célula da grade nova acende com `ÁREA ≈ \dfrac{1}{2v}\,\Delta u\,\Delta v`.
**Gatilhos:** "Passo um"→`u`, `v` · "a grade"→grade nova · "Passo dois"→`uv`, `u/v` · "raiz"→raízes e placa · "o atalho"→a matriz da ida · "derivada de u em relação a xis"…"um sobre xis"→quatro entradas · "o determinante"→linha do det · "dois vê"→glyph map · "ir e voltar"→linha-regra e selo · "um sobre dois vê"→J · "o módulo"→|J|
> [thoughtful] Passo um: u igual a xis ípsilon e vê igual a ípsilon sobre xis. As bordas viram u igual a um, u igual a dois, vê igual a um, vê igual a dois, e a grade nova é feita de hipérboles e de raios. Passo dois: multiplicando, u vê é ípsilon ao quadrado; dividindo, u sobre vê é xis ao quadrado. Então xis é raiz de u sobre vê, e ípsilon é raiz de u vê. Derivar essas raízes dá trabalho. Então vai o atalho: calcular o jacobiano da ida, de u e vê em relação a xis e ípsilon. A derivada de u em relação a xis é ípsilon, em relação a ípsilon, xis. A de vê em relação a xis é menos ípsilon sobre xis ao quadrado, e em relação a ípsilon, um sobre xis. O determinante: ípsilon vezes um sobre xis, menos xis vezes menos ípsilon sobre xis ao quadrado. Ípsilon sobre xis mais ípsilon sobre xis: dois ípsilon sobre xis, que é dois vê. Agora, ir e voltar é não fazer nada: o jacobiano da volta vezes o da ida dá um, pela regra da cadeia. Então o jacobiano que a gente quer é um sobre dois vê. E, como vê é positivo, o módulo é o mesmo.

### E2-3 · a área e a pipa
**Tela:** layout A com o plano u, v no palco: o quadrado [1, 2] × [1, 2] em GEO translúcido, com `B_{uv}`; a célula lima. Coluna C2b: a integral montada (`|J|` voa do chip; os limites voam das bordas), de dentro (`\dfrac{1}{2v}` sai, `[u]_1^2 = 2 − 1`), de fora (`\dfrac12[\ln v]_1^2`, `\dfrac12(\ln 2 − \ln 1)`, `\ln 1 = 0` com chip), `= \dfrac{\ln 2}{2} ≈ 0{,}347` em menta, sem moldura. Depois o palco volta para o xy: as duas diagonais da pipa dos quatro cantos (vertical de (1, 1) a (1, 2): `DIAGONAL 1`; horizontal em y = √2 de (1/√2, √2) a (√2, √2): `DIAGONAL` `\dfrac{1}{\sqrt2}`); a pipa em traço GEO; `PIPA = \dfrac{1\cdot\frac{1}{\sqrt2}}{2} = \dfrac{\sqrt2}{4} ≈ 0{,}354`; as faixas entre as hipérboles e os lados da pipa acendem (a de baixo menta `ENTRA`, a de cima ALERTA `SAI`); `0{,}347 ≈ 0{,}354` com `ESTIMATIVA DA PIPA` (GEO), sem ✓: é ordem de grandeza, não igualdade.
**Gatilhos:** "um quadrado"→B_uv · "a área"→integral · "a de dentro"→linha · "dois menos um"→`[u]` · "a de fora"→linha · "logaritmo de um é zero"→chip · "logaritmo de dois sobre dois"→resultado · "a pipa"→palco xy e pipa · "diagonal vezes diagonal"→chaves e conta · "raiz de dois sobre quatro"→`≈ 0,354` · "um tiquinho"→faixas · "bate"→✓
> [serious] Passo quatro: no plano u vê, a região é o quadrado de um a dois nas duas direções. Passo cinco: a área é a integral de um a dois, da integral de um a dois, de um sobre dois vê, dê u dê vê. A de dentro é em u, e um sobre dois vê sai: fica u de um a dois, dois menos um, um. Sobra um sobre dois vê. A de fora: um meio vezes logaritmo de vê, de um a dois. Logaritmo de dois menos logaritmo de um, e logaritmo de um é zero. A área é logaritmo de dois sobre dois, mais ou menos zero vírgula trezentos e quarenta e sete. Para conferir sem integral, liga os quatro cantos: dá uma pipa. As diagonais são perpendiculares: a vertical mede um, e a horizontal, raiz de dois menos um sobre raiz de dois, que é um sobre raiz de dois. Diagonal vezes diagonal sobre dois: raiz de dois sobre quatro, zero vírgula trezentos e cinquenta e quatro. As bordas curvas tiram um tiquinho de um lado e põem do outro, e a pipa chega bem perto: é uma estimativa, não a área exata.

### E2-4 · a massa e a densidade média
**Tela:** layout A com o plano u, v; o quadrado pintado em faixas verticais de ciano (u cresce para a direita = a densidade xy). Coluna C2c: `m = \iint_R xy\,dA` com `xy` virando `u` (glyph map); `= \int_1^2\!\int_1^2 u\cdot\dfrac{1}{2v}\,du\,dv`; de dentro `\dfrac{1}{2v}\left[\dfrac{u^2}{2}\right]_1^2 = \dfrac{1}{2v}\left(\dfrac42 − \dfrac12\right) = \dfrac{1}{2v}\cdot\dfrac32 = \dfrac{3}{4v}`; de fora `\dfrac34[\ln v]_1^2 = \dfrac34(\ln 2 − 0) = \dfrac34\ln 2 ≈ 0{,}520\ \mathrm{kg}`. Conferência: `DENSIDADE MÉDIA` (Space Grotesk) e, ao lado, em MathTex, `= \dfrac{m}{A} = \dfrac{\frac34\ln2}{\frac12\ln 2} = \dfrac32`; no palco a reta u = 3/2 acende branca no meio do quadrado, com `MEIO DE 1 E 2`; ✓.
**Gatilhos:** "a massa"→linha 1 · "xis ípsilon é u"→glyph map · "a de dentro"→colchete · "quatro meios menos um meio"→linha · "três sobre quatro vê"→resultado de dentro · "a de fora"→linha · "três quartos de logaritmo de dois"→resultado · "a densidade média"→linha · "três meios"→reta u = 3/2 · "só depende de vê"→|J| acende no chip · "bem no meio"→✓
> [thoughtful] Agora a massa. A densidade é xis vezes ípsilon, e xis vezes ípsilon é u. Então a massa é a integral de u vezes um sobre dois vê, no mesmo quadrado. A de dentro: um sobre dois vê, vezes u ao quadrado sobre dois, de um a dois. Quatro meios menos um meio, três meios. Três meios vezes um sobre dois vê: três sobre quatro vê. A de fora: três quartos de logaritmo de vê, de um a dois: três quartos de logaritmo de dois, mais ou menos zero vírgula cinquenta e dois quilos. E tem conferência esperta. A densidade média é a massa dividida pela área: três quartos de logaritmo de dois, sobre um meio de logaritmo de dois, três meios. Bem no meio entre um e dois. Faz sentido: o jacobiano só depende de vê, então, na direção do u, a área se espalha por igual, e a média de u é o ponto do meio.

### E3-1 · ler a região nos limites
**Tela:** layout A. Coluna (x = 1080): o enunciado `\int_0^a\left[\int_0^{\sqrt{a^2-x^2}}\sqrt{a^2-x^2-y^2}\,dy\right]dx` + `PAUSE E TENTE`. Palco xy (origem (300, 900), a = 520 px; papel nascendo dos eixos). Leitura dos limites: `x` de `0` a `a` (âmbar, as duas marcas no eixo); uma tira em pé âmbar varre de x = 0 a x = a: entrada azul-claro em `y = 0`, saída coral em `y = \sqrt{a^2-x^2}`; a saída deixa rastro e desenha o quarto de círculo; a coluna escreve `y^2 = a^2 − x^2 ⇒ x^2 + y^2 = a^2` (glyph map: o `x²` atravessa); o quarto de disco acende GEO com `QUARTO DE DISCO`. Depois o integrando: `z = \sqrt{a^2-x^2-y^2} ⇒ x^2+y^2+z^2 = a^2` e a cena 3D `octante` entra (câmera de cima e de lado; o quarto de disco no chão, a casca da esfera por cima, opaca, em ciano escuro; os três eixos) com `UM OITAVO DE BOLA`.
Canto: `3 · O OITAVO DE BOLA`.
**Gatilhos:** "Terceiro problema"→enunciado · "pausa"→`PAUSE E TENTE` · "xis vai de zero a á"→marcas · "entra em ípsilon igual a zero"→entrada · "sai na raiz"→saída · "elevando ao quadrado"→linhas da coluna · "é o círculo"→rastro fecha o arco · "um quarto de disco"→região · "o integrando"→linha de z · "a esfera de raio á"→3D · "um oitavo de bola"→legenda
> [curious] Terceiro problema, do jeito que cai em prova: passe para polares e calcule esta integral repetida. A integral de zero a á, da integral de zero a raiz de á ao quadrado menos xis ao quadrado, de raiz de á ao quadrado menos xis ao quadrado menos ípsilon ao quadrado. Pausa e tenta. O primeiro trabalho é ler a região nos limites. Xis vai de zero a á. Para cada xis, a fatia entra em ípsilon igual a zero e sai na raiz de á ao quadrado menos xis ao quadrado. Elevando ao quadrado: ípsilon ao quadrado mais xis ao quadrado igual a á ao quadrado. É o círculo de raio á, e a região é um quarto de disco. E o integrando? Zê igual àquela raiz é a esfera de raio á, a parte de cima. A integral é o volume embaixo dela: um oitavo de bola.

### E3-2 · polares e o oitavo de bola
**Tela:** o 3D faz o pouso de cima para o quarto de disco 2D (grade entra no pouso); o raio laranja varre de θ = 0 a π/2 (verde-água) com a tira radial entrada na origem, saída no arco. Coluna C3 em duas etapas. Etapa A: `x^2+y^2 = r^2`; `0 ≤ r ≤ a`, `0 ≤ θ ≤ \dfrac{\pi}{2}`; a integral `\int_0^{\pi/2}\!\int_0^a \sqrt{a^2-r^2}\;\Rj\,dr\,d\theta` (o fator r em lima, com chave `JACOBIANO`); a linha `w = a^2 - r^2,\quad dw = -2r\,dr ⇒ r\,dr = -\dfrac{dw}{2}` (w em lilás); a linha dos limites `r = 0 → w = a^2`, `r = a → w = 0`; `\int_{a^2}^{0}\sqrt{w}\left(-\dfrac{dw}{2}\right) = \dfrac12\int_0^{a^2} w^{1/2}\,dw` com o selo `O MENOS INVERTE OS LIMITES`. Etapa B (chip `DE DENTRO` no topo): `\dfrac12\left[\dfrac23 w^{3/2}\right]_0^{a^2} = \dfrac12\cdot\dfrac23\left((a^2)^{3/2} − 0\right) = \dfrac{a^3}{3}`; a de fora `\dfrac{a^3}{3}[\theta]_0^{\pi/2} = \dfrac{a^3}{3}\left(\dfrac{\pi}{2} − 0\right) = \dfrac{\pi a^3}{6}`; a conferência `\dfrac{4\pi a^3}{3} \div 8 = \dfrac{4\pi a^3}{24} = \dfrac{\pi a^3}{6}` ✓ com um ícone da bola cortada em oito (traço GEO).
**Gatilhos:** "xis ao quadrado mais ípsilon ao quadrado é erre ao quadrado"→linha 1 · "de zero a á"→raio varre · "de zero a pi sobre dois"→θ · "vezes erre"→fator lima · "o jacobiano das polares"→chave · "dáblio igual a"→linha w · "os limites"→linha dos limites · "o sinal de menos"→selo · "dois terços"→colchete · "á ao quadrado elevado a três meios"→`(a²)^{3/2}` acende · "á ao cubo sobre três"→resultado · "a de fora"→linha · "pi á ao cubo sobre seis"→resultado · "a bola inteira"→conferência · "um oitavo"→✓
> [thoughtful] Em polares, xis ao quadrado mais ípsilon ao quadrado é erre ao quadrado, então o integrando vira raiz de á ao quadrado menos erre ao quadrado. O quarto de disco é erre de zero a á e téta de zero a pi sobre dois. E não esquece o fator: vezes erre, o jacobiano das polares. A de dentro pede uma substituição: dáblio igual a á ao quadrado menos erre ao quadrado. Dê dáblio é menos dois erre dê erre, então erre dê erre é menos dê dáblio sobre dois. Os limites mudam: erre igual a zero dá dáblio igual a á ao quadrado; erre igual a á dá dáblio igual a zero. O sinal de menos inverte os limites: fica um meio da integral de zero a á ao quadrado de dáblio elevado a um meio. A primitiva é dois terços de dáblio elevado a três meios. Em á ao quadrado, á ao quadrado elevado a três meios é á ao cubo; em zero, zero. Um meio vezes dois terços vezes á ao cubo: á ao cubo sobre três. A de fora multiplica pelo comprimento do intervalo de téta, pi sobre dois: pi á ao cubo sobre seis. Confere com a bola inteira: quatro terços de pi á ao cubo, dividido por oito, é pi á ao cubo sobre seis. Um oitavo, certinho.

### E4-1 · a elipse: polares esticadas
**Tela:** layout A. Palco: o círculo unitário (GEO) com uma célula polar lima (r ≈ 0,7, θ ≈ 0,8) se estica em x por `a` (âmbar) e em y por `b` (magenta) até a elipse de semieixos a = 1,6 e b = 1 (1 = 260 px, centro em (520, 560)); a célula estica junto. Coluna C4a: `\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}\le 1`; `x = a\,r\cos\theta`, `y = b\,r\,\mathrm{sen}\,\theta`; a substituição `\dfrac{a^2r^2\cos^2\theta}{a^2}+\dfrac{b^2r^2\mathrm{sen}^2\theta}{b^2} = r^2(\cos^2\theta+\mathrm{sen}^2\theta) = r^2 \le 1` (os pares a²/a² e b²/b² acendem e somem); a matriz `\begin{vmatrix} a\cos\theta & -a r\,\mathrm{sen}\,\theta\\ b\,\mathrm{sen}\,\theta & b r\cos\theta\end{vmatrix}`; `= abr\cos^2\theta + abr\,\mathrm{sen}^2\theta = abr` (lima); a área pela metade de cima, dobrada (selo `METADE DE CIMA × 2`, como no disco): `A = 2\int_0^{\pi}\!\int_0^1 abr\,dr\,d\theta = 2ab\left[\dfrac{r^2}{2}\right]_0^1[\theta]_0^{\pi} = 2ab\cdot\dfrac12\cdot \pi = \pi ab`; `a = b ⇒ \pi a^2` ✓ (o chip).
Canto: `4 · A ELIPSE`.
**Gatilhos:** "Quarto problema"→elipse · "Estica as polares"→o círculo estica · "xis igual a á erre"→linha · "Substituindo"→linha da substituição · "cancela"→pares somem · "seno ao quadrado mais cosseno ao quadrado"→`(cos² + sen²)` acende · "o disco de raio um"→linha final · "o determinante"→matriz · "á bê erre"→resultado · "esticar por á e por bê"→a célula ganha a chave `× ab` · "metade de cima"→selo · "pi á bê"→área · "o pi á ao quadrado"→✓
> [curious] Quarto problema: a área da elipse xis ao quadrado sobre á ao quadrado mais ípsilon ao quadrado sobre bê ao quadrado menor ou igual a um. Polares comuns não endireitam a elipse. Estica as polares: xis igual a á erre cosseno de téta, e ípsilon igual a bê erre seno de téta. Substituindo: á ao quadrado erre ao quadrado cosseno ao quadrado sobre á ao quadrado; o á ao quadrado cancela. Do mesmo jeito, o bê ao quadrado cancela. Sobra erre ao quadrado vezes cosseno ao quadrado mais seno ao quadrado, que é um. A elipse vira erre menor ou igual a um: o disco de raio um. O jacobiano: o determinante de á cosseno de téta, menos á erre seno de téta; bê seno de téta, bê erre cosseno de téta. Á bê erre cosseno ao quadrado, mais á bê erre seno ao quadrado: á bê erre. Esticar por á e por bê multiplica a área por á bê, e as polares põem o erre. Para a área, como no disco, faz a metade de cima, téta de zero a pi, e dobra. Duas vezes á bê, vezes erre ao quadrado sobre dois de zero a um, vezes téta de zero a pi: duas vezes á bê vezes um meio vezes pi, pi á bê. Com á igual a bê, volta o pi á ao quadrado do círculo.

### E4-2 · a meia elipse pesada: a massa
**Tela:** layout A. Palco: a meia elipse `x² + 4y² ≤ 1, y ≥ 0` (a = 1, b = 1/2; 1 = 560 px, centro da base em (540, 800)), pintada com o mapa ciano de `ρ = k y` (faixas horizontais, mais claro em cima); a reta de simetria x = 0 tracejada; chave `DISTÂNCIA ATÉ O EIXO` `x` = `y` (magenta) num ponto. Coluna C4b (etapa A): o enunciado `x^2+4y^2\le 1,\ y\ge0`, `\rho = k\,y`, `PAUSE E TENTE`; `\bar x = 0` (SIMETRIA); `a = 1,\ b = \dfrac12`; `x = r\cos\theta`, `y = \dfrac12 r\,\mathrm{sen}\,\theta`, `|J| = 1\cdot\dfrac12\cdot r = \dfrac{r}{2}` (o `ab r` voa do chip do E4-1); `0\le r\le1,\ 0\le\theta\le\pi`. Etapa B (massa): `m = \int_0^{\pi}\!\int_0^1 k\cdot\dfrac{r\,\mathrm{sen}\,\theta}{2}\cdot\dfrac{r}{2}\,dr\,d\theta` (o `k y` voa da legenda; o `r/2` voa do chip); `= \dfrac{k}{4}\int_0^{\pi}\mathrm{sen}\,\theta\,d\theta\int_0^1 r^2\,dr` (selo `SEPARA: SÓ θ · SÓ r` em Space Grotesk, com θ e r em MathTex); `\left[-\cos\theta\right]_0^{\pi} = -\cos\pi + \cos 0 = 1 + 1 = 2`; `\left[\dfrac{r^3}{3}\right]_0^1 = \dfrac13`; `m = \dfrac{k}{4}\cdot 2\cdot\dfrac13 = \dfrac{k}{6}` (sobe como chip, sem moldura em volta).
Canto: `4 · A MEIA ELIPSE PESADA`.
**Gatilhos:** "meia elipse"→palco · "distância até o eixo xis"→mapa e chave · "Pausa e tenta"→`PAUSE E TENTE` · "a simetria"→x̄ = 0 · "á igual a um"→linha · "um meio de erre"→|J| · "téta de zero a pi"→limites · "A massa"→integral · "separa"→selo · "menos cosseno"→colchete θ · "erre ao cubo sobre três"→colchete r · "cá sobre seis"→resultado
> [thoughtful] Agora a elipse ganha massa. Uma chapa com a forma da meia elipse xis ao quadrado mais quatro ípsilon ao quadrado menor ou igual a um, com ípsilon positivo, e densidade proporcional à distância até o eixo xis: rô igual a cá vezes ípsilon. Onde fica o centro de massa? Pausa e tenta. Pela simetria em torno do eixo ípsilon, xis barra é zero. Aqui, á é um e bê é um meio: xis igual a erre cosseno de téta, ípsilon igual a um meio de erre seno de téta, e o módulo do jacobiano é á bê erre, erre sobre dois. A meia elipse é erre de zero a um e téta de zero a pi. A massa: a integral de cá vezes ípsilon, que é cá vezes erre seno de téta sobre dois, vezes erre sobre dois. O integrando separa num pedaço só de téta e num só de erre: cá sobre quatro, vezes a integral do seno de téta de zero a pi, vezes a integral de erre ao quadrado de zero a um. A primeira: menos cosseno de pi mais cosseno de zero, um mais um, dois. A segunda: erre ao cubo sobre três, um terço. A massa é cá sobre quatro, vezes dois, vezes um terço: cá sobre seis.

### E4-3 · o momento e o centro de massa
**Tela:** o mesmo palco. Coluna C4c (etapa C, chip `m = k/6` no topo): `M_x = \iint_B y\,\rho\,dA = \int_0^{\pi}\!\int_0^1 \left(\dfrac{r\,\mathrm{sen}\,\theta}{2}\right)^2 k\,\dfrac{r}{2}\,dr\,d\theta` (y magenta, k ciano); `= \dfrac{k}{8}\int_0^{\pi}\mathrm{sen}^2\theta\,d\theta\int_0^1 r^3\,dr` (o `1/4` do quadrado e o `1/2` do jacobiano viram `1/8`); `\mathrm{sen}^2\theta = \dfrac{1-\cos 2\theta}{2}` (chip `IDENTIDADE`); `\left[\dfrac{\theta}{2} - \dfrac{\mathrm{sen}\,2\theta}{4}\right]_0^{\pi} = \dfrac{\pi}{2} - \dfrac{\mathrm{sen}\,2\pi}{4} - 0 = \dfrac{\pi}{2}`; `\left[\dfrac{r^4}{4}\right]_0^1 = \dfrac14`; `M_x = \dfrac{k}{8}\cdot\dfrac{\pi}{2}\cdot\dfrac14 = \dfrac{k\pi}{64}`. Etapa D: `\bar y = \dfrac{M_x}{m} = \dfrac{k\pi/64}{k/6} = \dfrac{k\pi}{64}\cdot\dfrac{6}{k} = \dfrac{6\pi}{64} = \dfrac{3\pi}{32} \approx 0{,}295` (o par k/k acende e some; 6/64 simplifica por 2). No palco o ⊕ desce do topo e pousa em (0; 0,295), com as chaves `0,295` (magenta) e `ALTURA 0,5` (GEO).
**Gatilhos:** "o momento em relação ao eixo xis"→linha 1 · "ípsilon vezes rô"→y e ρ acendem · "um oitavo"→linha 2 · "seno ao quadrado"→chip · "téta sobre dois"→colchete · "seno de dois pi é zero"→linha · "erre à quarta"→colchete · "cá pi sobre sessenta e quatro"→resultado · "momento sobre massa"→linha ȳ · "o cá cancela"→par some · "três pi sobre trinta e dois"→resultado · "zero vírgula duzentos e noventa e cinco"→⊕ pousa
> [serious] O momento em relação ao eixo xis é a integral de ípsilon vezes rô: ípsilon ao quadrado vezes cá, vezes o jacobiano. Ípsilon ao quadrado é erre ao quadrado seno ao quadrado de téta sobre quatro; vezes erre sobre dois, um oitavo. Fica cá sobre oito, vezes a integral de seno ao quadrado de téta de zero a pi, vezes a integral de erre ao cubo de zero a um. Para o seno ao quadrado, a identidade: seno ao quadrado é um menos cosseno de dois téta, sobre dois. A primitiva é téta sobre dois menos seno de dois téta sobre quatro. Em pi: pi sobre dois, menos seno de dois pi sobre quatro, e seno de dois pi é zero. Em zero, zero. Dá pi sobre dois. A de erre: erre à quarta sobre quatro, um quarto. O momento é cá sobre oito, vezes pi sobre dois, vezes um quarto: cá pi sobre sessenta e quatro. E ípsilon barra é momento sobre massa: cá pi sobre sessenta e quatro, dividido por cá sobre seis. Inverte e multiplica, o cá cancela, e sobra seis pi sobre sessenta e quatro: três pi sobre trinta e dois, mais ou menos zero vírgula duzentos e noventa e cinco.

### E4-4 · conferindo a massa e comparando
**Tela:** palco xy da meia elipse com uma tira em pé âmbar (x = 0,35): entrada azul-claro em y = 0, saída coral em `y = \dfrac{\sqrt{1-x^2}}{2}`. Coluna C4d: `m = \int_{-1}^{1}\!\int_0^{\sqrt{1-x^2}/2} k\,y\,dy\,dx`; de dentro `k\left[\dfrac{y^2}{2}\right]_0^{\sqrt{1-x^2}/2} = k\cdot\dfrac{1}{2}\cdot\dfrac{1-x^2}{4} = \dfrac{k(1-x^2)}{8}`; de fora `\dfrac{k}{8}\left[x - \dfrac{x^3}{3}\right]_{-1}^{1} = \dfrac{k}{8}\left(\dfrac23 + \dfrac23\right) = \dfrac{k}{8}\cdot\dfrac43 = \dfrac{k}{6}` ✓ (o chip `m = k/6` acende ao lado). Depois a comparação: o centroide ⊕ vazado em (0; 0,212) com o chip `\dfrac{4b}{3\pi} = \dfrac{4\cdot\frac12}{3\pi} = \dfrac{2}{3\pi} \approx 0{,}212` (`HOMOGÊNEA`) e o ⊕ cheio em 0,295 (`ρ = k y`); seta magenta de 0,212 para 0,295 com `A DENSIDADE PUXA PARA CIMA`. O meio disco de raio 1 aparece por trás em traço GEO fino e **achata** até a meia elipse (um movimento), levando o ⊕ vazado de 0,424 para 0,212: `ESTICA JUNTO`.
**Gatilhos:** "conferir a massa"→tira · "fatiando em pé"→linha 1 · "ípsilon ao quadrado sobre dois"→de dentro · "um oitavo"→linha · "dois terços mais dois terços"→de fora · "cá sobre seis de novo"→✓ · "se a chapa fosse homogênea"→⊕ vazado · "quatro bê sobre três pi"→chip · "achatar o meio disco"→o meio disco achata · "estica junto"→legenda · "puxa o centro para cima"→seta
> [thoughtful] Dá para conferir a massa sem polares, fatiando em pé. Xis vai de menos um a um, e ípsilon de zero até raiz de um menos xis ao quadrado, sobre dois. A de dentro: cá vezes ípsilon ao quadrado sobre dois, no topo da fatia: cá vezes um meio vezes um menos xis ao quadrado sobre quatro, cá vezes um menos xis ao quadrado sobre oito. A de fora: cá sobre oito, vezes xis menos xis ao cubo sobre três, de menos um a um. Dois terços mais dois terços, quatro terços. Cá sobre oito vezes quatro terços: cá sobre seis de novo. E se a chapa fosse homogênea? A meia elipse é o meio disco achatado pela metade, e o centroide achata junto: quatro bê sobre três pi, com bê igual a um meio, dois sobre três pi, zero vírgula duzentos e doze. A densidade que cresce para cima puxa o centro de massa para cima, até zero vírgula duzentos e noventa e cinco.

### E5-1 · a meia arruela: a área
**Tela:** o H1 volta: a meia arruela (origem em (700, 860), 1 = 230 px), grade da tela inteira, raio laranja e θ verde-água. Coluna C5a (x = 1180): `B:\ 1\le r\le 2,\ 0\le\theta\le\pi` (os limites voam das bordas: `1` do arco de dentro, `2` do de fora, `0` e `π` das duas metades da base); `\bar x = 0` (SIMETRIA); `A = \int_0^{\pi}\!\int_1^2 \Rj\,dr\,d\theta`; de dentro `\left[\dfrac{r^2}{2}\right]_1^2 = \dfrac42 - \dfrac12 = \dfrac32`; de fora `\dfrac32[\theta]_0^{\pi} = \dfrac32\,\pi`; `A = \dfrac{3\pi}{2}`. Conferência: no palco o meio disco grande acende (`\dfrac{\pi\cdot 2^2}{2} = 2\pi`) e o pequeno (`\dfrac{\pi\cdot1^2}{2} = \dfrac{\pi}{2}`); `2\pi - \dfrac{\pi}{2} = \dfrac{3\pi}{2}` ✓.
Canto: `5 · A MEIA ARRUELA`.
**Gatilhos:** "Agora sim, a meia arruela"→palco · "erre de um a dois"→limites de r · "téta de zero a pi"→limites de θ · "xis barra é zero"→linha · "A área"→integral · "erre ao quadrado sobre dois"→colchete · "três meios"→de dentro · "três pi sobre dois"→resultado · "o meio disco grande"→2π · "o pequeno"→π/2 · "a diferença"→✓
> [curious] Agora sim, a meia arruela. Em polares, ela é um retângulo: erre vai de um a dois, e téta de zero a pi. A densidade é a mesma em todo lugar; pode chamar de um. Pela simetria, xis barra é zero; falta ípsilon barra, e para ele a gente precisa da área e do momento. A área é a integral de zero a pi, da integral de um a dois, de erre dê erre dê téta: o erre é o jacobiano. A de dentro: erre ao quadrado sobre dois, de um a dois. Quatro meios menos um meio: três meios. A de fora: três meios vezes pi. A área é três pi sobre dois. E confere: o meio disco grande tem pi vezes dois ao quadrado sobre dois, dois pi. O pequeno, pi sobre dois. A diferença: três pi sobre dois.

### E5-2 · o momento e o buraco
**Tela:** o mesmo palco; o cateto `y = r\,\mathrm{sen}\,\theta` do triângulo polar (ponto em r = 1,6, θ = 1,0) acende magenta. Coluna C5b (chip `A = 3π/2` no topo): `M_x = \iint_B y\,dA = \int_0^{\pi}\!\int_1^2 r\,\mathrm{sen}\,\theta\cdot\Rj\,dr\,d\theta` (o `r sen θ` voa do cateto); de dentro `\mathrm{sen}\,\theta\left[\dfrac{r^3}{3}\right]_1^2 = \mathrm{sen}\,\theta\left(\dfrac83 - \dfrac13\right) = \dfrac73\,\mathrm{sen}\,\theta`; de fora `\dfrac73\left[-\cos\theta\right]_0^{\pi} = \dfrac73(1+1) = \dfrac{14}{3}`; `\bar y = \dfrac{14/3}{3\pi/2} = \dfrac{14}{3}\cdot\dfrac{2}{3\pi} = \dfrac{28}{9\pi} \approx 0{,}990`. No palco o ⊕ desce e pousa em (0; 0,990), **dentro do buraco**, a 0,01 da borda r = 1; uma lupa (fundo opaco, ×10) mostra o ⊕ e a borda com `0,990 < 1`; `NO BURACO` em ALERTA.
**Gatilhos:** "o momento"→linha 1 · "ípsilon é erre seno de téta"→cateto voa · "erre ao cubo sobre três"→colchete · "oito terços menos um terço"→linha · "sete terços de seno"→resultado · "menos cosseno"→colchete θ · "catorze terços"→M_x · "momento sobre área"→ȳ · "vinte e oito sobre nove pi"→resultado · "zero vírgula novecentos e noventa"→⊕ pousa · "um centésimo"→lupa · "cai no buraco"→`NO BURACO`
> [serious] O momento em relação ao eixo xis é a integral de ípsilon dê á, e ípsilon é erre seno de téta. Fica a integral de erre seno de téta vezes erre, dê erre dê téta. A de dentro: seno de téta vezes erre ao cubo sobre três, de um a dois. Oito terços menos um terço, sete terços: sete terços de seno de téta. A de fora: sete terços vezes menos cosseno de téta, de zero a pi. Menos cosseno de pi é um; mais cosseno de zero, um: dois. O momento é catorze terços. E ípsilon barra é momento sobre área, porque a densidade é um: catorze terços sobre três pi sobre dois. Inverte e multiplica: catorze terços vezes dois sobre três pi, vinte e oito sobre nove pi. Mais ou menos zero vírgula novecentos e noventa. Menor que um, por um centésimo. O centro de massa da meia arruela homogênea cai no buraco.

### E5-3 · o fio de prumo
**Tela:** cartão 2D (grade padrão). A meia arruela em GEO opaco, presa por um alfinete branco na ponta de fora da base, à direita (2, 0). Ela **gira** em torno do alfinete até o repouso (um movimento, 1,5 s, sem balanço): o ⊕ fica exatamente abaixo do alfinete; o fio de prumo (traço branco fino com um peso pequeno) cai do alfinete e atravessa o buraco. A chapa volta à posição original com a linha do fio desenhada nela (tracejado branco). Depois o mesmo pela outra ponta (−2, 0): segunda linha. As duas linhas se cruzam no buraco, no ⊕. Legenda `O EQUILÍBRIO FICA NO AR`. Embaixo, três miniaturas em traço GEO com o ⊕ fora do corpo: `ANEL`, `FERRADURA`, `BUMERANGUE`.
**Gatilhos:** "recorta essa meia arruela"→chapa · "pendura por uma ponta"→alfinete · "ela gira"→a chapa gira · "fio de prumo"→fio · "pela outra ponta"→segunda · "se cruzam"→cruzamento e ⊕ · "no ar"→legenda · "anel"…"bumerangue"→miniaturas
> [excited] Dá para ver isso em casa. Recorta essa meia arruela num papelão e pendura por uma ponta, com um alfinete. Ela gira até o centro de massa ficar bem embaixo do alfinete. Pendura um fio de prumo no mesmo alfinete e risca a linha do fio. Agora pendura pela outra ponta e risca de novo. As duas linhas se cruzam no buraco, no ar, onde não tem papelão. O centro de massa não precisa estar dentro do corpo. Acontece com um anel, com uma ferradura, com um bumerangue. Nesses corpos, o ponto de equilíbrio fica fora da peça.

### E5-4 · a borda mais pesada
**Tela:** layout A, palco da meia arruela com o mapa radial `ρ = k r` (ciano cresce para fora). Coluna C5c em duas etapas. Etapa A (massa): `m = \int_0^{\pi}\!\int_1^2 (k\,r)\cdot\Rj\,dr\,d\theta` com as chaves `DENSIDADE` (ciano, no primeiro r) e `JACOBIANO` (lima, no segundo); de dentro `k\left[\dfrac{r^3}{3}\right]_1^2 = k\left(\dfrac83-\dfrac13\right) = \dfrac{7k}{3}`; de fora `\dfrac{7k}{3}[\theta]_0^{\pi} = \dfrac{7k\pi}{3}`. Etapa B (chip `m = 7kπ/3`): `M_x = \int_0^{\pi}\!\int_1^2 r\,\mathrm{sen}\,\theta\cdot k\,r\cdot \Rj\,dr\,d\theta`; de dentro `k\,\mathrm{sen}\,\theta\left[\dfrac{r^4}{4}\right]_1^2 = k\,\mathrm{sen}\,\theta\left(\dfrac{16}{4}-\dfrac14\right) = \dfrac{15k}{4}\,\mathrm{sen}\,\theta`; de fora `\dfrac{15k}{4}\cdot 2 = \dfrac{15k}{2}` (o `2` voa do chip `∫sen = 2` do E5-2); `\bar y = \dfrac{15k/2}{7k\pi/3} = \dfrac{15k}{2}\cdot\dfrac{3}{7k\pi} = \dfrac{45}{14\pi} \approx 1{,}023`. Etapa C, a comparação (alvo): coluna limpa com dois chips (`\dfrac{28}{9\pi}\approx 0{,}990` e `\dfrac{45}{14\pi}\approx 1{,}023`); régua em pé ampliada (0,98 a 1,03 em 600 px) à direita do palco, com as guias tracejadas das alturas: 0,990 (`HOMOGÊNEA`, branco, no buraco), 1,000 (`BORDA DO BURACO`, ALERTA), 1,023 (`ρ = k r`, ciano, na chapa); o ⊕ sobe do buraco para a chapa; `VOLTA PARA A CHAPA` em menta.
**Gatilhos:** "E se a borda pesar mais"→mapa · "dois erres"→chaves · "a massa"→integral · "sete cá sobre três"→de dentro · "sete cá pi sobre três"→m · "o momento"→integral · "três erres"→os três r acendem · "erre à quarta sobre quatro"→colchete · "quinze cá sobre quatro"→de dentro · "o mesmo dois"→o 2 voa · "quinze cá sobre dois"→M_x · "o cá cancela"→par some · "quarenta e cinco sobre catorze pi"→resultado · "um vírgula zero vinte e três"→régua e ⊕ sobe · "volta para a chapa"→legenda
> [curious] E se a borda pesar mais, com a densidade crescendo com a distância até o centro: rô igual a cá vezes erre? Agora aparecem dois erres na massa, e cada um tem um dono: um é da densidade, o outro é do jacobiano. A massa é a integral de cá erre vezes erre. A de dentro: cá vezes erre ao cubo sobre três, de um a dois: oito terços menos um terço, sete cá sobre três. A de fora multiplica por pi: sete cá pi sobre três. No momento, entram três erres: o ípsilon, que é erre seno de téta, a densidade e o jacobiano. A de dentro: cá seno de téta vezes erre à quarta sobre quatro, de um a dois. Dezesseis quartos menos um quarto, quinze quartos. A de fora traz o mesmo dois da integral do seno: quinze cá sobre dois. Ípsilon barra é quinze cá sobre dois, dividido por sete cá pi sobre três. Inverte e multiplica, o cá cancela: quarenta e cinco sobre catorze pi. Mais ou menos um vírgula zero vinte e três. Maior que um: com a borda mais pesada, o centro de massa volta para a chapa, por dois centésimos.

### E6-1 · Pappus: o volume pelo centroide
**Tela:** cena 3D `pappus` (Three.js). (1) O meio disco de raio a (GEO claro, opaco) em pé sobre o eixo x (âmbar), com um quadradinho lima a uma altura y e a chave `y` (magenta). (2) O meio disco gira em torno do eixo x (ângulo φ de 0 a 2π, 6 s, com começo e fim suaves) e o sólido varrido nasce atrás dele (ciano escuro opaco, só a parte já varrida); o quadradinho deixa um anel lima fino de raio y: legenda `ANEL DE COMPRIMENTO 2πy`. Ao fim, a bola inteira. (3) Corte para 2D (pouso do 3D para a vista de frente, ortográfica, grade entra): coluna C6a (x = 1120): `\Delta V \approx 2\pi y\,\Delta A`; `V = \iint_B 2\pi y\,dA` (glyph map, Δ → d e a soma vira ∬); `= 2\pi\iint_B y\,dA = 2\pi\,M_x` (o 2π sai); `= 2\pi\,\bar y\,A` (porque `\bar y = \dfrac{M_x}{A}` na chapa homogênea; chip). Selo grande: `VOLUME = ÁREA × CAMINHO DO CENTROIDE` com `2\pi\bar y` sob `CAMINHO`. Embaixo, à esquerda, a fatia deitada do meio disco na altura y (comprimento `L(y)`, entrada azul-claro, saída coral) e a linha `\iint_B 2\pi y\,dA = \int_0^a 2\pi y\,L(y)\,dy` com o selo `CASCAS DO CÁLCULO I`.
Canto: `6 · O TEOREMA DE PAPPUS`.
**Gatilhos:** "Último problema"→3D · "gira em torno do eixo xis"→começa a girar · "um anel"→anel lima · "dois pi ípsilon"→legenda · "a bola"→fim do giro · "Somando"→pouso e coluna · "dois pi sai"→linha · "momento"→M_x · "ípsilon barra vezes a área"→linha · "o caminho do centroide"→selo · "fatia deitada"→a fatia · "o método das cascas"→linha e selo
> [excited] Último problema, e ele junta tudo. Pega uma chapa homogênea acima do eixo xis e gira em torno do eixo xis. Ela varre um sólido. Qual o volume? Olha um quadradinho da chapa, de área delta á, a uma altura ípsilon. Girando, ele desenha um anel de comprimento dois pi ípsilon, e varre um volume de mais ou menos dois pi ípsilon vezes delta á. Somando, no limite: o volume é a integral dupla de dois pi ípsilon dê á. O dois pi sai, e o que sobra é o momento em relação ao eixo xis. E o momento é ípsilon barra vezes a área. Então o volume é a área vezes dois pi ípsilon barra: a área, vezes o caminho que o centroide percorre numa volta. Esse é o teorema de Pappus. E não é mágica: fatiando deitado, cada fatia, de comprimento éle de ípsilon, gira e vira uma casca de cilindro. É o método das cascas do Cálculo um, com a fatia inteira.

### E6-2 · a bola confere o meio disco
**Tela:** 3D `pappus` com o meio disco de raio a; o ⊕ vazado (centroide) em `4a/(3π)` desenha o seu círculo magenta tracejado durante um giro (a bola completa fica só em contorno de traço GEO, para o círculo do centroide aparecer). Coluna C6b: `\bar y = \dfrac{4a}{3\pi}` (chip `MEIO DISCO HOMOGÊNEO`); `A = \dfrac{\pi a^2}{2}`; `V = 2\pi\cdot\dfrac{4a}{3\pi}\cdot\dfrac{\pi a^2}{2}`; `= \dfrac{8a}{3}\cdot\dfrac{\pi a^2}{2}` (o π de cima cancela o de baixo); `= \dfrac{8\pi a^3}{6} = \dfrac{4\pi a^3}{3}` ✓ `A BOLA`.
**Gatilhos:** "o meio disco"→3D · "quatro á sobre três pi"→chip e ⊕ · "a área"→A · "o volume"→linha · "o pi cancela"→par some · "oito á sobre três"→linha · "quatro terços de pi á ao cubo"→✓ · "a bola"→legenda
> [happy] Testa no meio disco de raio á. O centroide dele fica a quatro á sobre três pi da base, e a área é pi á ao quadrado sobre dois. Girando em torno da base, ele varre uma bola. Pappus diz: dois pi vezes quatro á sobre três pi, vezes pi á ao quadrado sobre dois. Dois pi vezes quatro á sobre três pi: o pi cancela, oito á sobre três. Vezes pi á ao quadrado sobre dois: oito pi á ao cubo sobre seis, quatro terços de pi á ao cubo. O volume da bola, sem integral nenhuma.

### E6-3 · a casca confere a meia arruela
**Tela:** 3D `pappus` com a meia arruela 1 ≤ r ≤ 2: o giro varre a bola oca (o sólido parcial mostra o oco pela face do corte, como uma laranja descascada por dentro); depois pouso 2D. Coluna C6c: `V = \dfrac43\pi\cdot2^3 - \dfrac43\pi\cdot1^3 = \dfrac43\pi(8-1) = \dfrac{28\pi}{3}` (os raios 2 e 1 voam das bordas); `V = 2\pi\,\bar y\,A ⇒ \bar y = \dfrac{V}{2\pi A}` (glyph map: o `2πA` atravessa a igualdade); `= \dfrac{28\pi/3}{2\pi\cdot 3\pi/2}` (o `A = 3π/2` voa do chip do E5-1); `2\pi\cdot\dfrac{3\pi}{2} = 3\pi^2`; `= \dfrac{28\pi}{3}\cdot\dfrac{1}{3\pi^2} = \dfrac{28}{9\pi}` ✓ e o chip `\dfrac{28}{9\pi}` do E5-2 desce e encaixa ao lado: `O MESMO NÚMERO`.
**Gatilhos:** "a meia arruela"→3D · "uma bola oca"→o oco aparece · "a bola de raio dois menos a de raio um"→linha V · "vinte e oito pi sobre três"→resultado · "Pappus ao contrário"→glyph map · "a área"→A voa · "três pi ao quadrado"→linha · "vinte e oito sobre nove pi"→✓ · "o mesmo número"→chip encaixa
> [excited] Agora a meia arruela. Girando em torno da base, ela varre uma bola oca: a bola de raio dois menos a bola de raio um. O volume é quatro terços de pi vezes dois ao cubo, menos quatro terços de pi vezes um ao cubo: quatro terços de pi vezes oito menos um, vinte e oito pi sobre três. Agora usa Pappus ao contrário: ípsilon barra é o volume dividido por dois pi vezes a área. A área é três pi sobre dois, e dois pi vezes três pi sobre dois é três pi ao quadrado. Vinte e oito pi sobre três, dividido por três pi ao quadrado: vinte e oito sobre nove pi. O mesmo número da integral. Duas contas que não têm nada a ver, e o centro de massa cai no buraco nas duas.

### E6-4 · a família: do meio disco ao arame
**Tela:** layout A. Palco 2D: meia arruela genérica de raios `a` (dentro) e `b` (fora), com um `ValueTracker` em a; o ⊕ vazado acompanha a altura pela fórmula. Coluna C6d: `\bar y = \dfrac{\frac43\pi(b^3-a^3)}{2\pi\cdot\frac{\pi}{2}(b^2-a^2)} = \dfrac{4(b^3-a^3)}{3\pi(b^2-a^2)}`; as fatorações `b^3-a^3 = (b-a)(a^2+ab+b^2)` e `b^2-a^2 = (b-a)(a+b)` (o par `(b − a)` acende e some); `\bar y = \dfrac{4(a^2+ab+b^2)}{3\pi(a+b)}`. Dois casos-limite por chips, com o palco acompanhando: `a = 0:\ \dfrac{4b^2}{3\pi b} = \dfrac{4b}{3\pi}` (`MEIO DISCO`; o buraco some); `a = b:\ \dfrac{4\cdot 3b^2}{3\pi\cdot 2b} = \dfrac{2b}{\pi} \approx 0{,}64\,b` (`ARAME`; a chapa afina até virar um arco de arame, e o ⊕ fica a 0,64 b, no ar).
**Gatilhos:** "em geral"→palco genérico · "raios á e bê"→chaves · "a mesma conta"→linha 1 · "fatora"→fatorações · "bê menos á cancela"→par some · "com á igual a zero"→chip 1 e o buraco some · "o meio disco"→legenda · "á igual a bê"→chip 2 e a chapa afina · "dois bê sobre pi"→resultado · "arame"→legenda
> [thoughtful] E a mesma conta vale para qualquer meia arruela, de raio de dentro á e raio de fora bê. Quatro terços de pi vezes bê ao cubo menos á ao cubo, dividido por dois pi vezes pi sobre dois vezes bê ao quadrado menos á ao quadrado: quatro vezes bê ao cubo menos á ao cubo, sobre três pi vezes bê ao quadrado menos á ao quadrado. Fatora as duas diferenças. Bê ao cubo menos á ao cubo é bê menos á, vezes á ao quadrado mais á bê mais bê ao quadrado. Bê ao quadrado menos á ao quadrado é bê menos á, vezes á mais bê. O bê menos á cancela. Com á igual a zero, sem buraco: quatro bê ao quadrado sobre três pi bê, quatro bê sobre três pi, o meio disco. Com á igual a bê, a chapa vira um arame dobrado em meia volta: quatro vezes três bê ao quadrado, sobre três pi vezes dois bê, dois bê sobre pi. O centro de um arame em semicírculo fica a sessenta e quatro por cento do raio, no ar.

### E6-5 · a rosquinha
**Tela:** 3D `pappus` com o disco de raio 1 e centro a 2 do eixo (o disco em pé, chave `2` magenta do eixo até o centro, chave `1` do raio); o giro varre o toro opaco; o centro do disco desenha o círculo magenta tracejado de raio 2. Coluna C6e: `V = 2\pi\cdot 2\cdot\pi\cdot1^2 = 4\pi^2 \approx 39{,}5`, com as chaves `CAMINHO DO CENTRO` sob `2π · 2` e `ÁREA DO DISCO` sob `π · 1²`.
**Gatilhos:** "uma rosquinha"→3D · "a dois do eixo"→chave 2 · "raio um"→chave 1 · "o centro do disco"→círculo do centro · "dois pi vezes dois"→caminho · "pi vezes um ao quadrado"→área · "quatro pi ao quadrado"→resultado
> [happy] E um bônus: uma rosquinha. Um disco de raio um, com o centro a dois do eixo, girando em volta dele. O centroide do disco é o próprio centro, que percorre dois pi vezes dois. A área é pi vezes um ao quadrado. O volume do toro é quatro pi ao quadrado, mais ou menos trinta e nove vírgula cinco. Uma linha de conta.

### S1 · síntese: os cinco erros
**Tela:** cartão (grade padrão), cinco linhas que entram uma por gatilho, cada uma com ✗ ALERTA à esquerda e a correção em menta à direita: `ESQUECER O JACOBIANO` → `dA = r\,dr\,d\theta` · `JACOBIANO SEM MÓDULO, OU O DA IDA` → `|J|` e `INVERTA O DA IDA` (Space Grotesk) · `LIMITES SEM DESENHAR` → `BORDA POR BORDA` · `DIVIDIR PELA ÁREA COM ρ VARIÁVEL` → `\bar y = \dfrac{M_x}{m}` · `PAPPUS COM CHAPA NÃO HOMOGÊNEA` → `SÓ COM O CENTROIDE`. No fim, a miniatura da meia arruela com os dois ⊕ (0,990 e 1,023).
**Gatilhos:** "Resumindo"→cartão · "esquecer o jacobiano"→linha 1 · "o módulo"→linha 2 · "desenhar a região"→linha 3 · "dividir pela área"→linha 4 · "Pappus"→linha 5 · "a meia arruela"→miniatura
> [serious] Resumindo, os cinco erros que mais custam ponto neste módulo. Um: esquecer o jacobiano. Em polares, dê á é erre dê erre dê téta, sempre. Dois: usar o jacobiano sem módulo, ou usar o da ida no lugar do da volta. Se só a ida é fácil, inverte. Três: escrever os limites da região nova sem desenhar. Borda por borda, e os cantos conferem. Quatro: no centro de massa com densidade variável, dividir pela área. Divide pela massa: momento sobre massa. E cinco: usar Pappus com chapa não homogênea. Pappus fala do centroide, a geometria pura. E a meia arruela? Homogênea, o equilíbrio cai no buraco, em zero vírgula novecentos e noventa. Com a borda mais pesada, volta para a chapa, em um vírgula zero vinte e três.

### S2 · o próximo vídeo e CTA
**Tela:** à esquerda, a chapa [0, 2]² com o mapa ciano de `x² + y²` (a do quadrado da massa) em perspectiva 2D leve; ela **ganha altura** e vira um cubo de lado 2 em traço GEO (sem 3D novo: a extrusão é desenhada em Manim com três faces em perspectiva fixa), com o mapa ciano de `x² + y² + z²` nas faces visíveis e `MAIS PESADO LONGE DO CANTO`; `QUANTO PESA ESTE CUBO?`; uma caixinha lima pequena dentro do cubo com `Δx Δy Δz`. **Cartão:** moldura, `NO PRÓXIMO VÍDEO` e `INTEGRAL TRIPLA` entram juntos no gatilho "no próximo vídeo"; fica ≥ 8 s. Depois o CTA padrão (logo, anéis, INSCREVA-SE) com o desafio `A PARTIR DE QUE BURACO O CENTRO CAI NELE?`.
**Gatilhos:** "toda massa foi de chapa"→chapa · "dentro de um sólido"→a chapa vira cubo · "longe de um canto"→mapa e legenda · "Quanto pesa"→pergunta · "caixinhas"→caixinha · "no próximo vídeo"→cartão · "deixa o like"→CTA · "a partir de que tamanho de buraco"→desafio
> [curious] Até aqui, toda massa foi de chapa: densidade por área, integral dupla. E se a densidade mudar dentro de um sólido, ponto a ponto? Um cubo de lado dois, por exemplo, mais pesado longe de um canto: a densidade é xis ao quadrado mais ípsilon ao quadrado mais zê ao quadrado. Quanto pesa esse cubo? Aí a massa vira uma soma de caixinhas em três dimensões: a integral tripla. É o que a gente começa no próximo vídeo. [happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e fica o desafio para os comentários: a partir de que tamanho de buraco o centro de massa da meia arruela homogênea cai dentro dele? Dica: a fórmula da família já tem tudo. Até a próxima!

---

## Anexo B · Como cada símbolo é lido na fala

| Símbolo | Leitura | Primeira âncora |
|---|---|---|
| ∬_A f dA | integral dupla, em A, de f, dê á | E1-1 |
| e^{y − x²} | é elevado a ípsilon menos xis ao quadrado | E1-1 |
| u, v | u, vê | E1-2 |
| ∂(x, y)/∂(u, v), J | o jacobiano (de xis, ípsilon em relação a u, vê); ∂ não é lido sozinho | E1-2 |
| \|J\| | o módulo do jacobiano | E1-2 |
| B_uv | bê u vê | E1-4 |
| [F]ₐᵇ | F, de á a bê | E1-3 |
| ln v | logaritmo de vê | E2-3 |
| √(u/v) | raiz de u sobre vê | E2-2 |
| ρ | rô | E2-1 |
| r, θ | erre, téta | E3-2 |
| w | dáblio | E3-2 |
| (a²)^{3/2} | á ao quadrado elevado a três meios | E3-2 |
| a, b (semieixos) | á, bê | E4-1 |
| x̄, ȳ | xis barra, ípsilon barra | E4-2 |
| M_x | o momento em relação ao eixo xis (na coluna, "eme xis") | E4-3 |
| m | a massa (na coluna, "eme") | E4-2 |
| k | cá | E4-2 |
| sen²θ | seno ao quadrado de téta | E4-3 |
| ΔA, ΔV | delta á, delta vê | E6-1 |
| L(y) | éle de ípsilon | E6-1 |
| ≈ | mais ou menos | E1-3 |
