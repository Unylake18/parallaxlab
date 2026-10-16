# yt_0003 — microedições de narração/storyboard (V1.6)

Escopo: apenas os cinco pontos reabertos no handoff V1.6 (dA e normais · x ± dx/2 · diferença finita → derivada parcial ·
delta de Dirac · Ω) mais C₁/C₂ e Stokes. Física, ordem e arquitetura continuam congeladas. Nenhuma voz foi gerada.

O texto-base V1.2 (Narração + Storyboard) não está versionado neste repositório; por isso cada item abaixo traz a
**frase nova proposta**, o ponto do vídeo em que entra e o que ela substitui/complementa. Tempos são do preview V1.6.

| # | Onde (preview) | Frase proposta (pt-BR) | Efeito no storyboard |
|---|---|---|---|
| 1 | Abertura, 0:04–0:20 | "Em cada pedacinho da superfície, a área ganha uma direção: o vetor área aponta para fora, na normal." | `dA`, `n̂` e `dA = n̂ dA` nascem no patch; `E` e `dA` se juntam em `E·dA` antes do `∮`. |
| 2 | Abertura, 0:21–0:28 | "Somando essas contribuições por toda a superfície, chegamos ao fluxo." | Patches com `E` → `Σ` → `∮ E·dA`. |
| 3 | Gauss, 0:57–1:10 | "Quando as cargas viram uma densidade, a carga envolvida passa a ser a integral de ρ no volume." | `Q_env` vira `∫ρ dV` dentro da lei; zoom conceitual no ponto P. |
| 4 | Divergente, 0:05–0:21 | "Começamos por um ponto P e por um intervalo dx centrado nele: duas metades de dx sobre dois, uma para cada lado. Os extremos são x menos dx sobre dois e x mais dx sobre dois." | Eixo → P → segmento dx → duas metades → extremos `x ± dx/2` → cubo. |
| 5 | Divergente, 0:25–0:47 | "A face perpendicular a x tem arestas dy e dz; a área dela é dy dz. A normal externa aponta para fora: mais x na direita, menos x na esquerda." | `dy`, `dz` nas arestas → `dA_x = dy dz`; normais `n̂₊`, `n̂₋` com chamada "normal externa". |
| 6 | Divergente, 0:53–1:36 | "O fluxo por uma face é E ponto dA. Como a normal é x, só a componente E_x entra. Essa componente é calculada na posição da face: x mais dx sobre dois. Na esquerda, a normal inverte o sinal." | `dΦ = E·dA` → `E·x̂` → `E_x` → `E_x(face)` → `E_x(x + dx/2)`; esquerda com sinal negativo. |
| 7 | Divergente, 1:43–2:20 | "A diferença dividida por dx é a inclinação da secante entre as duas faces. Com y e z fixos, quando dx tende a zero a secante vira tangente: é a derivada parcial de E_x em relação a x." | Mini gráfico `E_x × x`; "y e z fixos"; secante → tangente; razão → `∂E_x/∂x`. |
| 8 | Divergente, 2:20–3:00 | "Repetindo para y e para z, somamos os três pares de faces. Essa soma de derivadas é o divergente de E." | `dΦ_x + dΦ_y + dΦ_z`; chave "divergente de E"; `∇·E`. |
| 9 | Teorema, 0:00–0:35 | "Na face compartilhada, a normal de A é mais x e a de B é menos x: a mesma face é saída para um e entrada para o vizinho; as contribuições se cancelam." | `n̂_A`, `n̂_B`, `Φ_A + Φ_B = 0`; depois 2 → 4 → 8 células. |
| 10 | Delta, 1:15–1:40 | "Como representar uma carga inteira concentrada em um único ponto? Encolhendo o volume, a carga dentro dele continua q. Esse é o delta de Dirac tridimensional: delta, o índice três entre parênteses indica três dimensões, não potência." | Volume encolhe com `Q_env = q`; nome `δ⁽³⁾(r)` com callout "(3) = três dimensões, não potência". |
| 11 | Delta, 1:40–2:10 | "Definimos I de V como a integral do delta no volume: zero quando a origem está fora; um quando ela está dentro. Não é uma função comum: é uma distribuição." | `I(V) ≡ ∫δ⁽³⁾dV`, volume atravessa a origem; depois `ρ = q δ⁽³⁾(r)` com o `q` copiado da carga. |
| 12 | F₁ × F₂, 0:07–0:20 | "Ômega controla a intensidade do giro: à direita o vetor sobe, em cima vai para a esquerda, à esquerda desce, embaixo vai para a direita. Quanto maior o ômega, mais forte o giro." | Eixos, quatro vetores tangentes, `Ω` varia; só depois `F₂ = Ω(−y x̂ + x ŷ)`. |
| 13 | Circulação, 0:00–0:36 | "Chamamos de C₁ e C₂ dois caminhos de a até b. Os dois dão o mesmo resultado." | `∫_{C₁}` e `∫_{C₂}` substituem I₁ e I₂; `∫_{C₁} = ∫_{C₂}`. |
| 14 | Circulação, 0:36–1:10 | "Ida por C₁ e volta por C₂ fecham a curva: os extremos coincidem e a circulação fechada é zero." | `C = C₁ − C₂`, volta completa, `∮_C E·dl = 0`. |
| 15 | Stokes, 0:08–0:40 | "Em cada pedacinho da superfície, a normal e o rotacional dão a contribuição local: o quanto do rotacional atravessa o patch. Somando os patches, temos a integral de superfície." | Um patch com `dA`, `n̂` e `∇×E` → `Σ` → `∫_S (∇×E)·dA`. |
| 16 | Stokes, 0:40–1:02 | "Enquanto isso, a circulação na borda: o rotacional acumulado no interior é igual à circulação na borda." | Tracer em C; `∮_C E·dl = ∫_S (∇×E)·dA`. |
| 17 | Stokes, 1:02–1:38 | "Como a circulação é zero, a integral do rotacional é zero para qualquer superfície; aproximando um único patch, em qualquer orientação, o rotacional é zero." | Zoom no patch; três orientações; `∇×E = 0`. |
