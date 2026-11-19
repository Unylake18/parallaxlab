# yt_0043 · Cálculo III 3.5-T4: centro de massa e momento de inércia
## Avaliação do preview v1 + HANDOFF v2 (preview)

**Unidade:** `videos_longos/yt_0043_centro_massa_momento_inercia/` · `formato: longo_horizontal` · série Cálculo III (EP. 18 provisório)
**Fase aberta:** PREVIEW v2 (960×540, 15 fps). Não criar voz, SRT, master, 1080p nem entrega.
**Base:** o preview v1 (21:47, lotes PH → PA → PB1 → PB2 → PB3 → PB4 → PS) e o handoff v1.1, que continua valendo em tudo o que este documento não muda.
**Narração:** `yt_0043_narracao_v1.md` sem mudança. Nenhum gatilho novo; todo degrau novo de conta entra nos gatilhos que já existem.
**Anexo:** `yt0043_handoff_v2_completo.zip`, com este handoff, os 23 quadros-alvo v2, a folha de contato v2 e a narração v1.

---

## 1. Veredito

O QA automático do v1 está limpo. A base técnica pode ficar como está:
- alinhamento 3D × Manim de 0,01 px;
- 0 flashes;
- GM1–GM18 presentes;
- 149 gatilhos sem desvio;
- grade de 60 px exata em todos os stills.

O papel quadriculado está alinhado com os gráficos 2D e com o piso do 3D. **Não mexer na grade.**

O que reprova o v1 para seguir para a narração é visual e didático:

1. **Seis quadros-alvo meus estavam errados.** Corrigi todos na v2 (§3). Reproduza a v2, não a v1.
2. **Defeitos de montagem** que o QA automático não pega (§4):
   - 3D que some e deixa rótulos órfãos;
   - plaquinhas de rótulo em cima de arestas;
   - seta 3D encostando em texto;
   - coluna com 9 linhas;
   - cartão vazio no primeiro quadro.
3. **Nove contas com degraus pulados** (§5), contra a regra permanente da conta inteira.
4. **Palavras em fonte serifada dentro do MathTex** (§6).

---

## 2. Arquivos do zip

| arquivo | conteúdo |
|---|---|
| `yt_0043_v1_avaliacao_e_handoff_v2.md` | este documento |
| `quadros_alvo_v2/00_folha_contato_v2.jpg` | os 23 alvos lado a lado |
| `quadros_alvo_v2/NN_*.jpg` | alvos 1920×1080; os alterados na v2 estão listados no §3 |
| `yt_0043_narracao_v1.md` | narração (sem mudança, só referência dos gatilhos) |

A comparação lado a lado volta a ser obrigatória: render 540p normalizado para 1080p à esquerda, alvo v2 à direita. Use `comparacao_v2/*.jpg` no mesmo formato do v1.

---

## 3. Alvos corrigidos (erros meus no v1; reproduzir a v2)

### A1 · B1-1a · três bolinhas (`03_B1-1a_tres_bolinhas.jpg`)
No v1 o centro de massa ficava mais perto da m₃ (massa 2) do que da m₂ (massa 3). Isso desmentia a legenda "o centro de massa fica mais perto da mais pesada".

Posições novas, em unidades do mundo, mesma câmera do v1:
- m₁ = 1 em (2,4; 2,0; 0,4);
- m₂ = 3 em (2,3; 0,4; 1,1);
- m₃ = 2 em (0,4; 2,4; 1,8).

Resultado:
- CM = (1,683; 1,333; 1,217);
- distância do CM à m₂: 1,12;
- distância do CM à m₃: 1,77.

Na tela (1080p) o ⊕ fica a cerca de 130 px da m₂ e a cerca de 230 px da m₃. Raio da bolinha ∝ ∛m, como antes.

**Novo:** um fio tracejado magenta #EA63FF do ⊕ até o piso, igual aos fios das bolinhas. Isso deixa o ⊕ legível como ponto 3D.

**Critério:** no still, a distância em pixels ⊕–m₂ é menor que ⊕–m₃, e nenhuma bolinha ou rótulo cobre o rótulo do eixo y.

### A2 · B1-3b · contraexemplo ρ = 1 + x (`07_B1-3b_contraexemplo.jpg`)
No v1 o 3D não mostrava que o lado x > 0 pesa mais. Só havia duas células, uma clara e uma escura.

Na v2, um disco no piso da lata (z = 0, raio 1) recebe um degradê lima #C6F26B, com opacidade proporcional a (1 + x)/2:
- quase apagado em x = −1;
- forte em x = +1.

As duas células gêmeas ficam como estão (clara do lado x > 0, escura do lado −x). O rótulo "−x" sai de cima do eixo z: deslocar 70 px para a esquerda da célula.

Sem animação extra: o disco nasce com `FadeIn` curto (0,6 s) no gatilho de "ρ = 1 + x".

### A3 · B3-1 · momento de inércia (`10_B3-1_momento_inercia.jpg`)
- **Célula:** no v1 ela ficava bem na frente do eixo z (θ₁ = −0,18π). Na v2 vai para θ₁ = −0,05π (e θ₂ = θ₁ + π/10), à direita do eixo, com o fio s e a seta v livres.
- **Eixo z:** encurtar de z = 1,6 para z = 1,45. O rótulo z do v1 encostava no título do canto; na v2 fica abaixo de y = 150 px.

### A4 · B3-3 · cilindro e a casca (`12_B3-3_cilindro.jpg`)
- **No v1:** cilindro opaco e a casca como um anel fixo só na tampa, com s = 0,55.
- **Na v2:**
  - o cilindro fica em traço (a mesma lata em traço do resto do vídeo: 12 geratrizes, aros);
  - a casca é uma superfície **opaca pêssego** (cor do s) de raio s, altura h inteira, com aro pêssego no topo e na base;
  - o raio s vai de 0,1 até R = 1 em `ValueTracker`, durante o gatilho "a casca cresce até a parede": cerca de 4 s, `rate_func=linear`, uma vez só, e para em s = 0,55 no estado do still.
- **Coluna:** a chave "s²·s = s³" vira MathTex de 34 px (s² pêssego, s lima, s³ lima), não texto pequeno com sobrescrito unicode. O degrau G(b) − G(a) entra no §5 (D2).

### A5 · B3-5 · quem gira mais fácil (`14_B3-5_quem_gira.jpg`)
As três linhas s_G do v1 estavam erradas:
- no tubo ficavam fora da parede (1,33 R);
- no cilindro ficavam em cima da parede;
- na bola ficavam em cerca de 0,85 R.

Na v2, elas ficam no raio de giração verdadeiro, desenhado na escala do próprio corpo (R = raio do desenho):

| corpo | s_G | posição da linha |
|---|---|---|
| tubo fino | R | exatamente sobre a parede (tracejado pêssego por cima do traço cinza) |
| cilindro | R/√2 ≈ 0,707 R | dentro do retângulo |
| bola | √(2/5) R ≈ 0,632 R | dentro do círculo |

As linhas ficam tracejadas (dash 10/7), em pêssego, com espessura de 4 px. O rótulo s_G fica acima de cada linha, à direita.

**Critério:** medir no still a distância da linha ao eixo dividida pelo raio do desenho: 1,00 / 0,71 / 0,63 (± 0,01).

### A6 · B4-1, B4-2, B4-3 · lata pequena nas telas de conta (`15_`, `16_`, `17_`)
No v1, a tampa da lata pesada era cortada pela borda esquerda (x = 60 px).

Na v2, a lata pequena usa escala 0,60 e deslocamento (dx, dy) = (−20, +190) px em relação à câmera da série, e cabe inteira entre x = 110 e x = 570. A coluna de conta continua em x = 780.

Em B4-1, os rótulos "ALTURA / DENSIDADE / FATOR" do v1 estavam colados. Na v2 viram três legendas com quadradinho de cor, em y = 385:
- ■ ALTURA (azul) em x = 780;
- ■ DENSIDADE (ciano) em x = 950;
- ■ FATOR s (lima) em x = 1180.

### A7 · B4-6 · dois números (`20_B4-6_dois_numeros.jpg`)
No v1, os dois cortes ficavam lado a lado, a 170 px por unidade. A diferença 0,500 × 0,555 dava cerca de 9 px, invisível, e os números 0,500/0,555 ficavam em cima das linhas s_G.

Na v2:
- **Cortes:** os dois cortes ficam **empilhados**:
  - painéis de 840 × 390 em (60, 170) e (60, 590);
  - escala de 280 px por unidade;
  - lata de 560 × 280 px.
- **Referência z = 1/2:** em cada painel, um tracejado horizontal cinza #B8C4DA, que passa do retângulo, mais a legenda "■ TRACEJADO CINZA: z = 1/2" em y = 1020.
- **Os ⊕:**
  - na lata comum, o ⊕ fica em cima do tracejado;
  - na lata pesada, fica cerca de 15 px acima dele.
- **Rótulos:** `z̄ = 0,500` e `z̄ = 0,555` em MathTex, à direita do retângulo (x ≈ 775), fora das linhas s_G.
- **s_G:** tracejado pêssego em ±0,707 e ±0,747, com o rótulo à direita da linha.
- **Tabela da direita:** sem mudança.

### A8 · S2 · eixo na parede (`21_S2_eixo_parede.jpg`)
Só a palavra "EIXO", que agora é legenda Space Grotesk em âmbar presa à ponta da reta (não `\text` no MathTex).

---

## 4. Defeitos de implementação (corrigir no render)

Tempos no formato *lote · segundo dentro do lote*. Os lotes começam no vídeo em:

| lote | início |
|---|---|
| PH | 0 s |
| PA | 110,0 s |
| PB1 | 128,5 s |
| PB2 | 350,0 s |
| PB3 | 489,9 s |
| PB4 | 818,5 s |
| PS | 1238,1 s |

**I1 · Órfãos no fim do PB2 (PB2 · 139,73 s).** A taça some, mas o ⊕, as plaquinhas 2/3 e 1/2, o rótulo z e o tracejado ficam na tela. Tudo o que está preso a um 3D sai **no mesmo quadro** que o 3D (mesmo `FadeOut`/`AnimationGroup`).
**Critério:** nenhum rótulo, ⊕ ou tracejado preso ao 3D existe em quadro sem o 3D.

**I2 · Palco vazio com z órfão em B2-1 → B2-2 (PB2 · 65,27 s).** Mesma regra do I1. A troca de cena 3D é por corte limpo: o 3D novo e os seus rótulos entram juntos no quadro seguinte.

**I3 · Seta x tocando a legenda "TROCADO" (B1-3a).** Nenhum texto a menos de 24 px de traço 3D (seta, aresta, eixo). Mover a legenda para y = 1020 (faixa das legendas) ou encurtar a seta x 3D até a ponta parar 24 px antes.

**I4 · Plaquinhas sobre arestas.** São quatro casos:
- H2: as plaquinhas dm;
- B1-1b: a plaquinha Δm cobre o eixo z;
- B1-2: a plaquinha "−" é minúscula e sobreposta, e "z = z̄" fica em cima da borda do plano;
- B1-3: a plaquinha −x fica em cima do eixo.

Regra: a plaquinha (fundo escuro do rótulo) não pode cobrir eixo, aresta da lata nem borda de plano. Deslocar o rótulo para o lado livre, com haste de no máximo 90 px se preciso. O "−" de B1-2 vira MathTex de 34 px, igual aos outros sinais.

**I5 · B3-4 (bola), rótulos amontoados.**
- **Ponto P:** na v2 dos alvos fica em r = 0,85 R e φ = 0,31π (≈ 56°), e as plaquinhas s, φ e r se separam.
- **Rótulo φ:** junto ao arco.
- **Rótulo r:** no meio do raio, do lado de fora.
- **Rótulo s:** acima da sombra tracejada.

**I6 · B3-4b, o chip ∫sen³ encostando no logo.** A zona do logo (x > 1600 e y < 130) é proibida para texto. Começar o chip na coluna x = 1020, y = 140, com no máximo 560 px de largura; se não couber, quebrar em duas linhas.

**I7 · Coluna com 9 linhas (B1-1b e B4-1).** Máximo de 7 linhas por coluna. Ao passar disso, renovar a coluna: as linhas antigas saem, e o resultado que continua sendo usado vira chip no topo, voando (`TransformFromCopy`) da linha original.
- B1-1b: renovar depois de "Δm = ρ ΔV".
- B4-1: renovar depois da linha dos limites novos de u (o chip leva "u = s² + z²").

**I8 · B4-1, linha u/du apertada.** "u = s² + z² (z PARADO)" numa linha; "du = 2s ds ⇒ s ds = du/2" na linha de baixo. Mesmo tamanho (42 px).

**I9 · B2-2, o fator s.** Nas linhas 2 e 3 o fator s do jacobiano tem que estar em lima #C6F26B, como na linha 1. É o `\Js`; conferir que todas as ocorrências usam a macro.

**I10 · A1, cartão vazio no primeiro quadro.** O cartão do A1 (aviso de pré-requisito) nasce com o texto, ou o texto entra no mesmo quadro em que a borda do cartão termina. Nenhum quadro com cartão vazio.

**I11 · S1, cartões só na metade esquerda.** Os cartões do resumo ocupam x = 60–900 e deixam a metade direita vazia. Distribuir em toda a largura útil (x = 60–1860), em 2 colunas de 860 px, sem mudar texto nem ordem.

**I12 · B4-4, chip do (1 + z²)^{5/2}.** Ver D8 (§5).

**I13 · B4-6.** Ver A7 (§3).

**I14 · Escrita.** Mantém tudo do v1.1:
- caneta glifo a glifo;
- voos do desenho;
- GM1–GM18.

Os degraus novos do §5 também entram com caneta. Quando o degrau novo manipula a linha anterior, entra com `TransformByGlyphMap`, e a numeração continua: GM19, GM20, … Não use `FadeIn` de linha pronta.

---

## 5. Contas com degrau pulado (conta inteira; obrigatório)

Todos os degraus abaixo entram nos gatilhos que já existem, sem mudar a narração. Se algum não couber no tempo da âncora, **não acelere a caneta e não tire o degrau**: reporte a âncora e quantos segundos faltam.

**D1 · B1-3b (ρ = 1 + x).** Escrever a massa e o ∭x² dV inteiros:

```
M = ∭(1 + x) dV = ∭dV + ∭x dV = π·1²·1 + 0 = π              (∭x dV = 0 pela simetria)
x² = s² cos²θ
x² · s = s³ cos²θ                                              (s lima: o fator)
∭x² dV = ∫₀^{2π} cos²θ dθ · ∫₀¹ s³ ds · ∫₀¹ dz
∫₀^{2π} cos²θ dθ = [θ/2 + sen 2θ/4]₀^{2π} = (π + 0) − (0 + 0) = π
∫₀¹ s³ ds = [s⁴/4]₀¹ = 1/4 − 0 = 1/4
∫₀¹ dz = [z]₀¹ = 1 − 0 = 1
∭x² dV = π · 1/4 · 1 = π/4
x̄ = (π/4)/π = 1/4
```

Na tela, o alvo v2 mostra o essencial. Os três colchetes podem entrar numa segunda coluna, renovada (I7).

**D2 · B3-3 (cilindro).** Depois dos colchetes, a linha G(b) − G(a), já no alvo v2:

```
= k · [z]₀ʰ · [s⁴/4]₀ᴿ · [θ]₀^{2π}
= k · (h − 0) · (R⁴/4 − 0) · (2π − 0)
= πkR⁴h/2              M = k · πR²h
I_z = ½ (kπR²h) R² = ½ MR²
```

**D3 · B3-4a (∫₀^π sen³φ dφ).** O degrau da soma, já no alvo v2:

```
= (1 − 1/3) − (−1 + 1/3) = 2/3 + 2/3 = 4/3
```

**D4 · B3-4b (resultado da bola).** A divisão inteira:

```
I_z = k · 2π · 4/3 · R⁵/5 = 8πkR⁵/15
M = k · 4πR³/3
I_z / M = (8πkR⁵/15) / (4πkR³/3) = (8/15) · (3/4) · R² = 24/60 R² = 2/5 R²
I_z = 2/5 MR²
```

**D5 · B4-1 (integral em s do M_xy).** A multiplicação das frações e a linha explícita antes do GM10:

```
= ½ · ⅔ [u^{3/2}]_{z²}^{1+z²}
= ⅓ [u^{3/2}]_{z²}^{1+z²}                          (½ · ⅔ = ⅓)
= ⅓ [(1 + z²)^{3/2} − (z²)^{3/2}]                   (G(b) − G(a), com os limites substituídos)
= ⅓ [(1 + z²)^{3/2} − z³]                           (chip: z ≥ 0 ⇒ (z²)^{3/2} = z³)  ← GM10
```

**D6 · B4-2 (z̄).** A divisão de frações em degraus:

```
z̄ = [4π(2√2 − 1)/15] / [(π/12)(7√2 − 2 + 3 ln(1+√2))]
  = 4π(2√2 − 1)/15 · 12/(π(7√2 − 2 + 3 ln(1+√2)))
  = 48(2√2 − 1) / (15(7√2 − 2 + 3 ln(1+√2)))
  = 16(2√2 − 1) / (5(7√2 − 2 + 3 ln(1+√2)))        (48/15 = 16/5)
  ≈ 0,555
```

**D7 · B4-3 (integral em s do I_z).** Distribuir o ½ e escrever G(b) − G(a):

```
= ½ [⅖ u^{5/2} − z² · ⅔ u^{3/2}]_{z²}^{1+z²}
= [⅕ u^{5/2} − (z²/3) u^{3/2}]_{z²}^{1+z²}          (½ · ⅖ = ⅕;  ½ · ⅔ = ⅓)
= ⅕[(1 + z²)^{5/2} − (z²)^{5/2}] − (z²/3)[(1 + z²)^{3/2} − (z²)^{3/2}]
= ⅕[(1 + z²)^{5/2} − z⁵] − (z²/3)[(1 + z²)^{3/2} − z³]
```

**D8 · B4-4 (triângulo).** Novo chip na coluna, antes da linha "(1 + z²)^{5/2} dz = sec⁵t · sec²t dt". O chip **voa da hipotenusa** do triângulo (`TransformFromCopy` do rótulo √(1+z²) = sec t):

```
(1 + z²)^{5/2} = (√(1 + z²))⁵ = sec⁵t
```

O mesmo vale para a linha do z²(1 + z²)^{3/2}: (√(1 + z²))³ = sec³t, num chip menor ou na mesma linha.

**D9 · B4-5b (fechamento do I_z).** O 1/45 vira 4/180, e o 2π entra em degraus. O chip 1/45 continua visível na coluna como origem:

```
∫ em z = 19√2/180 + (1/12) ln(1+√2) + 1/45
1/45 = 4/180
∫ em z = (19√2 + 4)/180 + (1/12) ln(1+√2)
I_z = 2π [ (19√2 + 4)/180 + ln(1+√2)/12 ]
2π/180 = π/90        2π/12 = π/6 = 15π/90
I_z = (π/90)(19√2 + 4 + 15 ln(1+√2)) ≈ 1,539
```

---

## 6. Palavras dentro do MathTex (fonte serifada)

Toda palavra vai em Space Grotesk (`Text`), nunca `\text{}` no MathTex. No vídeo, o padrão é uma linha mista: texto Space Grotesk mais MathTex, alinhados pela linha de base (como `mixl`/`chipm` nos alvos v2).

| cena | v1 (serifado) | v2 |
|---|---|---|
| B1-3b | `\text{CILINDRO } R=1, h=1` | chip misto: ρ = 1 + x · CILINDRO · R = 1, h = 1 |
| B1-3a | `\text{SIMETRIA} ⇒ x̄ = ȳ = 0` | chip misto: SIMETRIA ⇒ x̄ = ȳ = 0 |
| B3-1 | `\text{UNIDADE: kg}·\text{m}^2` | chip: UNIDADE: kg · m² (tudo Space Grotesk) |
| B4-1 | `\text{SIMETRIA:} x̄ = ȳ = 0` | chip misto |
| B4-2 | `\text{CONFERE: CARTESIANAS…} M_xy ≈ 1,5318` | chip misto (texto menta) + MathTex |
| B4-4, B4-5a | `\text{SOBRA} = …` | SOBRA (Space Grotesk) + MathTex |
| B4-5a, B4-5b | `\int\text{ EM } z = …` | INTEGRAL EM z (Space Grotesk) + MathTex |
| B4-5b | `\text{CONFERE: …} ≈ 1,5391` | chip misto: CONFERE (…): I_z ≈ 1,5391 |
| S2 | `\text{EIXO}` | legenda Space Grotesk âmbar |

**Critério:** `texto_em_mathtex_v2.txt` deve listar 0 ocorrências de `\text{` com palavra (só unidades e símbolos permitidos, se houver).

---

## 7. QA do preview v2

Mantém os 20 itens do v1.1. Acrescenta cinco checagens visuais **medidas**, que o v1 não pegou:

1. **3D × texto:** distância mínima entre traço 3D projetado (eixos, setas, arestas: use o `timeline.json`) e caixa de texto ≥ 24 px. Relatório `texto_x_3d_v2.txt` com o pior caso por cena.
2. **Plaquinha × aresta:** nenhuma caixa de rótulo cruza segmento 3D projetado. Relatório `placas_x_arestas_v2.txt`.
3. **Órfãos nas emendas:** para cada saída ou troca de cena 3D, conferir o quadro anterior, o da troca e o seguinte. Nenhum rótulo preso ao 3D pode existir sem o seu 3D. Relatório `orfaos_v2.txt`, com os quadros PB2 · 65,27 s e PB2 · 139,73 s obrigatoriamente.
4. **Painel/cartão vazio:** nenhum quadro com cartão ou painel sem conteúdo (A1, S1, B3-5, B4-6). Relatório `paineis_vazios_v2.txt`.
5. **Geometria do s_G e do ⊕:**
   - **B3-5:** medir linha/raio no still: 1,00 · 0,71 · 0,63 (± 0,01).
   - **B1-1a:** distância ⊕–m₂ < ⊕–m₃ em pixels.
   - **B4-6:** o ⊕ da lata pesada fica ≥ 12 px acima do tracejado z = 1/2.

**Stills e comparação:**
- Refazer os 23 stills nos mesmos instantes do v1, mais os intermediários das cenas com degraus novos (D1–D9): um still logo depois de cada degrau novo.
- Comparação lado a lado com os alvos v2 em `comparacao_v2/`.
- Prancha das contas (`q/`) atualizada com cada degrau e o seu tempo.

**Render:** só os lotes afetados:
- PA (I10);
- PB1 (A1, A2, I3, I4, I7, D1);
- PB2 (I1, I2, I9);
- PB3 (A3, A4, A5, I5, I6, D2–D4);
- PB4 (A6, A7, I7, I8, D5–D9);
- PS (A8, I11).

O PH só muda nas plaquinhas dm do H2 (I4). Se isso for isolável, rerenderize só a âncora H2.

---

## 8. Parada e relatório

Ao terminar o preview v2:
1. listar os arquivos alterados;
2. listar os lotes rerenderizados, com o tempo de render e o custo por quadro do 3D;
3. dar o caminho do preview v2 e do zip para o GPT (`renders/v2/yt0043_v2_para_gpt.zip`), que deve incluir `qa/` (relatórios v2, stills, comparações e pranchas);
4. listar as âncoras em que um degrau novo não coube no tempo (D1–D9), com os segundos que faltam;
5. registrar a nova duração total;
6. parar. Não iniciar voz, 1080p nem entrega.
