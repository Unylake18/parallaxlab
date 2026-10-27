# Narração integral — Quando a simetria não está na configuração inteira (V3)

Versão editorial: 2026-10-13 (V3, mais didática; substitui a V1/V2). Português do Brasil. Sem voz gerada.

Janelas são orçamento de montagem, não timestamps. Trechos entre colchetes orientam a produção e não são falados. Equações e movimentos estão em `storyboard.md`. Modelo: eletrostática no vácuo, distribuições de carga prescritas. As duas esferas do primeiro problema são distribuições volumétricas idealizadas; a sobreposição é uma construção matemática, não a descrição de dois corpos materiais impenetráveis ocupando o mesmo espaço. Alvo desta versão: 12–15 min (referência ≈ 14:15).

## Roteiro

### N01 · 0:00–0:35 · Pergunta

Duas esferas do mesmo tamanho se sobrepõem. Uma tem densidade de carga positiva, a outra, negativa, com o mesmo valor. Vamos calcular o campo elétrico num ponto dentro da região em comum. Esse ponto, que vamos chamar de P, é só o lugar onde calculamos o campo; as cargas ficam onde estão. E a pergunta: se P mudar de lugar, o campo muda?

[ANIMAÇÃO: duas distribuições se encontrando; legenda "corte de duas distribuições esféricas"; P rotulado percorre a região comum. Sem revelar a resposta. Ciência antes da marca.]

### N02 · 0:35–0:45 · Intro humana

Você está no Parallax Lab. Hoje a Lei de Gauss vai parecer falhar, e vamos ver por quê.

[TELA: sistema de intro dos longos; título LEI DE GAUSS; subtítulo Superposição.]

### N03 · 0:45–1:50 · Primeiro conflito

Você já sabe usar a Lei de Gauss: o fluxo do campo por uma superfície fechada é a carga envolvida sobre epsilon zero. Em geral, o campo varia de ponto a ponto, então a integral não vira um produto simples. Para escrever o fluxo como o campo vezes a área da superfície, precisamos de uma superfície em que o campo seja perpendicular a ela e tenha o mesmo módulo em todos os seus pontos. Não confunda essa área com o ponto chamado A, que aparece logo em seguida.

Vamos tentar. Uma esfera centrada na distribuição positiva: a negativa estraga a simetria, e nos pontos A e B o campo tem valor e ângulo diferentes. Centrada na negativa: o mesmo problema, do outro lado. Envolvendo tudo: continua sem a simetria necessária.

A Lei de Gauss continua verdadeira. O que falta é a simetria esférica que nos daria uma superfície com essas propriedades, para obter o campo diretamente.

[TELA: a legenda e os títulos usam os símbolos (ρ, O₊, O₋, r⃗, r⃗′, E⃗); as grafias de pronúncia ficam só no texto de voz.]

[ANIMAÇÃO: P0 em destaque; uma gaussiana que muda de centro e raio, com amostras reais do campo; pontos A e B com normais. Gauss permanece válida.]

### N04 · 1:50–2:35 · Superposição

Mas cada esfera, sozinha, é perfeitamente simétrica. E na eletrostática os campos se somam: se a distribuição total é a soma de duas distribuições, o campo total é a soma dos dois campos. Isso vale mesmo quando o total não tem simetria nenhuma.

Atenção: isto é uma decomposição matemática. Não estamos separando as cargas de verdade; só calculando por partes. E sempre válido não quer dizer sempre útil: só ajuda quando sabemos o campo de cada parte. Então vamos começar por uma esfera sozinha.

[ANIMAÇÃO: configuração = esfera + esfera; parcelas de densidade ligadas às de campo; selo "sempre válido ≠ sempre útil"; a esfera positiva cresce e vira o objeto do próximo bloco.]

### N05 · 2:35–4:45 · Ferramenta: campo dentro de uma esfera uniforme

Considere uma esfera isolante com carga espalhada de forma uniforme por todo o volume. A densidade rô é a carga por unidade de volume: a carga total dividida pelo volume da esfera, em coulombs por metro cúbico. Uniforme quer dizer que ela é a mesma em todos os pontos.

Queremos o campo num ponto P dentro da esfera, a uma distância r do centro. Para usar Gauss, escolhemos uma superfície imaginária: uma esfera menor, concêntrica, que passa justamente por P. Ela não é um objeto físico; é uma ferramenta de cálculo.

Quanta carga essa superfície envolve? Só a do volume de raio r, e não a da esfera inteira. Esse volume é quatro terços de pi r ao cubo, e a carga envolvida é rô vezes esse volume.

Agora o fluxo. Por simetria, o campo é radial e tem o mesmo módulo em toda essa superfície, e a normal aponta para fora, na mesma direção do campo. Então E sai da integral, e sobra a área: quatro pi r ao quadrado.

Igualamos à carga envolvida sobre epsilon zero e isolamos E. O quatro pi cancela, e r ao cubo sobre r ao quadrado deixa um r: E é rô r sobre três epsilon zero.

Se dobrarmos r, a carga envolvida multiplica por oito, a área por quatro, e o campo por dois: ele cresce linearmente com a distância ao centro.

Falta um passo, porque vamos somar campos que apontam para lados diferentes: precisamos da forma vetorial. O vetor r chapéu tem tamanho um e aponta do centro para fora. Multiplicado por r, vira o vetor posição de P, medido a partir do centro. Então o campo é rô sobre três epsilon zero vezes o vetor posição. Chamamos essa constante de C, só uma abreviação. E o campo é C vezes o vetor posição.

[ANIMAÇÃO (~2:10): volume carregado, superfície gaussiana imaginária e campo são três camadas distintas; R e r em destaque; Q_env com o volume sombreado; fluxo com normal e campo paralelos; substituição e cancelamentos com \cancel; r → 2r com ×8, ×4, ×2; r̂ unitário e r r̂ = r⃗. Sinais de carga esquemáticos.]

### N06 · 4:45–5:40 · Mapa de centros, P e vetores posição

Voltemos às duas esferas. Marque o centro da positiva, O mais, e o da negativa, O menos. A seta d vai de O mais até O menos: ela é fixa, só depende de onde estão as esferas.

Agora o ponto P. Um vetor posição é uma seta que começa numa origem e termina no ponto: o comprimento é a distância, e a ponta indica direção e sentido. De O mais até P, temos r mais. De O menos até o mesmo P, r menos. É o mesmo ponto; os vetores são diferentes porque a origem é outra.

[ANIMAÇÃO: um símbolo por vez, ligado ao elemento do desenho e a uma linha da legenda compacta: O₊, O₋, d⃗, P, r⃗₊, r⃗₋. Anatomia da seta (início, ponta, comprimento).]

### N07 · 5:40–6:55 · Soma, vetor oposto e relação central

Como esses vetores se relacionam? Vamos de O mais até P por dois caminhos. No direto, seguimos a seta r mais. No outro, seguimos d até O menos, e depois r menos até P. Este marcador não é P; ele só percorre o trajeto. Os dois caminhos começam e terminam nos mesmos pontos, então fazem o mesmo deslocamento. Somar vetores é isso: colocar o início de um na ponta do outro. Logo, r mais é igual a d mais r menos.

Isolando d: r mais menos r menos é igual a d. E subtrair r menos é somar o vetor oposto: a mesma seta, com o mesmo comprimento, em sentido invertido. Colocando menos r menos na ponta de r mais, chegamos a O menos: o deslocamento total é d.

[ANIMAÇÃO: figura ampliada, esferas recuadas; marcador de percurso (anel, distinto de P); soma ponta com cauda; vetor oposto por inversão da cópia de r⃗₋.]

### N08 · 6:55–7:45 · Campos parciais, sentidos e a constante C

Vamos aos campos. A esfera positiva produz em P um campo que se afasta do centro dela, proporcional ao vetor posição: C vezes r mais. Repare: o comprimento de r mais é uma distância; o comprimento da seta de campo é a intensidade do campo. A constante C faz essa conversão, e o desenho usa outra escala para o campo.

A negativa puxa: o campo aponta para o centro dela. Por isso o sinal de menos: menos C vezes r menos tem a mesma direção de r menos, mas o sentido invertido.

[ANIMAÇÃO: campos ancorados em P, um de cada vez; guias tracejadas de P a O₊ e O₋; C como abreviação de ρ/3ε₀; distância (vetor posição) × intensidade (campo).]

### N09 · 7:45–8:35 · Soma geométrica e resultado

O campo total é a soma dos dois. Na seta, colocamos o início do segundo na ponta do primeiro, e a resultante liga o início do primeiro ao fim do segundo. Na álgebra: C r mais menos C r menos. Colocamos C em evidência: C vezes r mais menos r menos. E essa diferença é d. O campo total é C vezes d: aponta no mesmo sentido de d, de O mais para O menos.

Curioso: nesta lente, a densidade total é zero, as cargas se cancelam, e mesmo assim há campo.

[ANIMAÇÃO: cópia de E⃗₋ desliza até a ponta de E⃗₊; resultante comparada a d⃗; fatoração sincronizada; lente com ρ_tot = 0 e E ≠ 0.]

### N10 · 8:35–9:30 · Mover P

Onde está P nessa resposta? Sumiu. Vamos conferir movendo P. Lembre: as esferas ficam paradas; P é só o lugar onde calculamos o campo. Veja os vetores posição mudando, e os campos de cada esfera mudando também. Agora deixamos só a resultante: é sempre a mesma seta, em módulo, direção e sentido; só muda o ponto em que ela está ancorada. Em vários pontos da lente, o campo é o mesmo.

[ANIMAÇÃO: P rotulado percorre a lente; primeira passagem com parciais; segunda só com a resultante; ao final, várias setas iguais.]

### N11 · 9:30–10:15 · Por que as variações se cancelam

Por que isso acontece? Chamamos de delta a diferença: valor depois menos valor antes. Quando P se desloca, os dois vetores posição terminam no novo P, e os centros não se mexem. Então a variação é a mesma: delta r mais é igual a delta r menos. A variação do campo é C delta r mais menos C delta r menos: duas parcelas iguais, de sentidos opostos, que se cancelam. Cada campo muda. A soma não.

[ANIMAÇÃO: P e P′, ΔP = Δr⃗₊ = Δr⃗₋; cancelamento de CΔr⃗₊ e −CΔr⃗₋; "depois menos antes".]

### N12 · 10:15–11:20 · Segundo problema: a cavidade

Agora um segundo problema. Temos uma esfera isolante carregada, com densidade uniforme mais rô, e um buraco esférico deslocado do centro. Qual é o campo dentro do buraco? Essa configuração é uma generalização nossa do problema anterior, e também não tem a simetria esférica necessária para obter o campo diretamente.

Como reconstruí-la? Imagine a esfera cheia, com densidade mais rô, somada a uma esfera fictícia de densidade menos rô, justamente onde está o buraco. Fora da cavidade só existe a esfera cheia: mais rô. Dentro, mais rô mais menos rô dá zero: é como se a carga tivesse sido retirada. Atenção: não há carga negativa de verdade no buraco; é uma decomposição matemática. E já sabemos calcular o campo interno de cada esfera.

[ANIMAÇÃO: primeiro a esfera física com buraco; pergunta; depois cheia + fictícia tracejada; densidades dentro e fora; pares +ρ/−ρ se cancelam; equivalência em miniaturas.]

### N13 · 11:20–12:05 · Mapa de variáveis da cavidade

Vamos organizar os símbolos. R é o raio da esfera grande; a é o raio da cavidade. O vetor d vai do centro grande ao centro da cavidade. Para a cavidade ficar inteiramente dentro, o ponto mais distante dela, na distância d mais a, precisa ser menor que R. Repare também: o campo interno que obtivemos não usa R; vale em qualquer ponto interno à esfera correspondente, com a mesma densidade. Por isso, se mudarmos o raio da cavidade, mantendo a densidade e os centros, nada muda nesse raciocínio.

[ANIMAÇÃO: R, a e d⃗ um por vez, com legenda; ray do centro grande passando pela cavidade: |d⃗| + a comparado a R; a varia com ρ e d⃗ fixos.]

### N14 · 12:05–13:10 · Campo dentro da cavidade

Escolha um ponto P dentro da cavidade. O vetor r vai do centro grande até P. O vetor r linha, com apóstrofo, vai do centro da cavidade até o mesmo P: o apóstrofo só indica outra origem, não é derivada. Pelo caminho em dois trechos, r é igual a d mais r linha. A esfera cheia dá C vezes r; a fictícia dá menos C vezes r linha. Somando: C vezes r menos r linha, que é C vezes d. Dentro da cavidade, o campo é rô sobre três epsilon zero vezes d: uniforme. Mova P: as parcelas mudam; o total, não. E se deslocarmos a cavidade em outra direção, o campo gira junto: ele sempre acompanha d.

[ANIMAÇÃO: figura ampliada; marcador distinto de P; legenda de r⃗ e r⃗′; mesma gramática de N07; P percorre a cavidade; no fim, o deslocamento d⃗ muda de direção e a resultante o acompanha.]

### N15 · 13:10–13:40 · Alcance e limites

Quanto mais deslocada a cavidade, maior o campo: ele é proporcional a d. Mas cuidado com o alcance. A superposição vale sempre na eletrostática; o campo uniforme, não. Ele depende desta estrutura: densidade uniforme, cavidade esférica, campos lineares com o mesmo coeficiente e centros fixos. Uma cavidade de outro formato não herda esse resultado.

[ANIMAÇÃO: |d⃗| cresce e a resultante cresce junto; três hipóteses ligadas à figura; esboço de cavidade de outro formato marcado como "não garantido".]

### N16 · 13:40–14:15 · Checagens e estratégia

Testes. Se os centros coincidem, d é zero e o campo é zero. Trocando o sinal da densidade, o campo inverte. E as unidades: rô d sobre epsilon zero é newton por coulomb. A estratégia que fica: diante de uma geometria difícil, decomponha em problemas simétricos que você sabe resolver, e use a superposição.

[ANIMAÇÃO: uma checagem ativa por vez, com o estado sustentado antes de restaurar; fecho com os próprios objetos: sobreposição → decomposição → esfera simétrica → soma vetorial.]
