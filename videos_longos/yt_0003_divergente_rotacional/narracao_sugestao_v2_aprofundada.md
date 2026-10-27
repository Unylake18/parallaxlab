# yt_0003 — sugestão de narração v2 (aprofundada, curso pré-vestibular)

Status: **proposta para o GPT lapidar.** Texto sem pressa de relógio: **5674 palavras ≈ 34.4 min de voz a 2.75 palavras/s**. O vídeo atual (preview V1.7) dura 12:49; **o vídeo passa a se moldar à voz**: cada bloco abaixo é uma âncora, e a cena espera a fala terminar antes do próximo evento visual (marcador [SEGURAR] onde a espera é maior). Mesma física e mesma ordem do vídeo; nada de física nova.

Princípio: **a voz explica o porquê e nomeia cada grandeza por extenso; o Manim mostra o como.** Estilo de professor de cursinho: devagar, concreto, com analogias e ganchos para assuntos vizinhos, sem ler a tela.

## Como falar as grandezas

| Na tela | Na fala |
|---|---|
| E (vetor) | **o campo elétrico** (nunca só "E"); E_x: **a componente x do campo elétrico** |
| ∇·E | **o divergente do campo elétrico** ("nabla ponto E" na 1ª vez, depois "o divergente") |
| ∇×F, ∇×E | **o rotacional** do campo (F = "um campo vetorial qualquer") |
| Φ | **o fluxo** do campo elétrico ("fi" só na 1ª vez) |
| dA, dA (vetor) | **o elemento de área**; dA vetor = **o elemento de área vetorial** |
| n̂ | **o vetor normal unitário, a normal externa** |
| S | **a superfície gaussiana S** (superfície fechada) |
| Q_env | **a carga envolvida** |
| ρ | **rô, a densidade volumétrica de carga** |
| ε₀ | **epsilon zero, a permissividade elétrica do vácuo** |
| dV, dx, dy, dz | **o elemento de volume**; **dx, dy, dz: pequenos deslocamentos em x, y e z** |
| x̂, ŷ, ẑ | **os vetores unitários nas direções x, y e z** |
| ∂E_x/∂x | **a derivada parcial da componente x do campo em relação a x** |
| κ | **kappa, uma constante** |
| q, r, r̂ | **a carga q**, **a distância r**, **o vetor unitário radial** |
| δ³(r) | **delta de Dirac tridimensional** (o 3 não é potência) |
| Ω | **ômega maiúsculo, constante que controla a intensidade do giro** |
| dℓ | **o deslocamento infinitesimal ao longo do caminho** |
| r_a, r_b | **a distância da carga ao ponto a**; **… ao ponto b** |
| C, C₁, C₂ | **a curva fechada C**; **o caminho C um**; **o caminho C dois** |
| ∮ | **integral sobre um caminho (ou superfície) fechado(a)** |
| B | **o campo magnético**; ∂B/∂t = **a derivada parcial do campo magnético no tempo** |
| V | **o potencial elétrico** (escalar); ∇V = **o gradiente do potencial** |

Regra: toda grandeza nova entra com nome completo; nas repetições próximas pode encurtar ("o campo", "o fluxo"), mas **símbolo solto só quando a tela está apontando para ele**.

## Como as âncoras funcionam

- Cada bloco `A01…G04` começa a ser falado **no instante do evento visual** descrito; a cena (`self.ancora("ID")`, a criar na próxima fase, na linha do evento) espera a voz acabar o bloco antes de seguir.
- Tempo `≈ mm:ss` = onde o evento ocorre **hoje** no preview V1.7 (±4 s); serve só para achar o quadro. O tempo final nasce da voz.
- Mesmo formato do yt_0002 (`ancoras_voz.py`: instante do evento → início da fala); a lista pronta está em `ancoras_voz_v2.py` e o texto corrido (para TTS) em `texto_narracao_v2.txt`.
- Onde a fala é muito mais longa que a animação atual, o bloco traz **[SEGURAR]** e a cena precisa de espera extra (ou animação mais lenta).


## 1. Hook e pergunta central  
*Duas perguntas locais (divergente e rotacional) e o problema: como leis sobre superfícies e caminhos dizem algo sobre UM ponto.*  
_198 palavras ≈ 72 s de voz_

**A01 · ≈0:00** — *O campo radial de uma carga positiva aparece, com partículas escoando para fora.*  
> Olha esse campo elétrico saindo de uma carga positiva. Cada setinha diz, naquele ponto do espaço, para onde o campo aponta e com que intensidade.

**A02 · ≈0:02** — *Aparece o símbolo nabla ponto E e a pergunta "o campo nasce aqui?"; um anel de teste pisca perto da carga.*  
> Agora eu quero te fazer uma pergunta que parece simples: neste pontinho aqui, o campo elétrico está nascendo? Existe uma fonte exatamente aí? Essa pergunta tem nome: é o divergente do campo elétrico, escrito nabla ponto E.

**A03 · ≈0:03** — *Entra o campo girante à direita, com nabla vezes F e a pergunta "o campo gira aqui?"; a rodinha gira.*  
> E tem uma segunda pergunta, de outra natureza. Neste outro campo, as setas dão voltas. Se eu colocar uma rodinha aqui, ela gira? Existe circulação local? Isso é o rotacional, escrito nabla vezes F — aqui F é só um nome genérico para um campo vetorial qualquer.

**A04 · ≈0:05** — *Surge o texto: "Como leis sobre superfícies e caminhos inteiros dizem o que acontece em UM ponto?"*  
> O problema é este: as leis que a gente conhece falam de superfícies inteiras e de caminhos inteiros. Como é que uma lei assim consegue dizer o que acontece em um único ponto? É isso que a gente vai construir hoje, devagar, passo a passo — e no final você vai ver que são duas ferramentas gêmeas: o divergente e o rotacional. E já adianto: essas duas ferramentas, divergente e rotacional, são a base de metade das equações de Maxwell, o conjunto que descreve toda a eletricidade e todo o magnetismo.

_[SEGURAR] ~10 s de fala sobre uma tela parada; é o momento certo para a pergunta respirar._


## 2. Do fluxo global à carga envolvida  
*Reconstrução da lei de Gauss: dA, normal, E·dA, soma sobre a superfície, carga envolvida, densidade ρ, e o convite ao zoom.*  
_646 palavras ≈ 235 s de voz_

**A05 · ≈0:08** — *Surge a superfície gaussiana S, um círculo em torno da carga.*  
> Vamos começar pelo que já existe. Imagine uma superfície fechada em volta da carga. A gente chama ela de superfície gaussiana, e vou chamar de S. Ela é só uma moldura imaginária que a gente escolhe para fazer a conta.

**A06 · ≈0:11** — *Um pedacinho da superfície brilha e recebe o rótulo dA.*  
> Agora olha só um pedacinho minúsculo dessa superfície. Esse pedacinho tem uma área muito pequena, que a gente escreve como dA: o elemento de área. Pense nele como um azulejo infinitamente pequeno colado na superfície.

**A07 · ≈0:13** — *Aparece o vetor normal n-chapéu; abaixo se constrói "dA vetor = n-chapéu dA".*  
> Só que a área, sozinha, não diz para onde o azulejo está virado. Por isso a gente desenha uma seta de comprimento um, perpendicular à superfície e apontando para fora: é o vetor normal unitário, a normal externa, que a gente escreve n-chapéu. Juntando os dois, nasce o elemento de área vetorial: dA vetor é igual a n-chapéu vezes dA. Tamanho do azulejo, e a direção para onde ele olha.

**A08 · ≈0:14** — *Aparece o vetor campo elétrico E no mesmo pedacinho; E também surge à direita.*  
> No mesmo pedacinho, a gente também enxerga o campo elétrico, o vetor E, que a carga produz ali.

**A09 · ≈0:17** — *E e dA se fundem em "E ponto dA".*  
> Agora a pergunta é: quanto desse campo atravessa esse azulejo? Para responder, a gente faz o produto escalar entre o campo elétrico e o elemento de área vetorial: E ponto dA. Se o campo é perpendicular ao azulejo, o produto é o maior possível. Se o campo só passa raspando, o produto é zero. É a medida de quanto campo realmente atravessa aquele pedacinho de superfície.

**A10 · ≈0:21** — *Doze pedaços acendem em volta da superfície, cada um com seu E; surge a soma de E ponto dA.*  
> Mas a superfície tem muitos pedacinhos. Então a gente faz isso em cada um deles e soma tudo: a soma de E ponto dA sobre todos os pedaços.

**A11 · ≈0:25** — *A soma vira a integral de superfície fechada, com o símbolo de círculo e o S embaixo.*  
> Quando os pedacinhos ficam infinitamente pequenos, a soma vira uma integral. E como a superfície é fechada, a gente coloca um circulozinho no sinal da integral: integral de superfície fechada de E ponto dA. Esse número tem nome: é o fluxo do campo elétrico através da superfície, que a gente representa pela letra grega maiúscula fi.

**A12 · ≈0:30** — *A superfície encolhe e uma pequena região é levada até um cubo à direita.*  
> O que a lei de Gauss diz é que esse fluxo não depende da forma da superfície, só do que está dentro dela. Então, em vez de olhar a superfície toda, vamos olhar uma região pequena, dentro de um cubinho. Já vamos ver por quê.

**A13 · ≈0:36** — *O cubo cresce, com cinco cargas pontuais dentro; surge Q_env e a lei de Gauss integral.*  
> Dentro do cubo, aparecem algumas cargas. Somando todas elas, a gente tem a carga envolvida, que a gente escreve Q com índice env, de envolvida. E a lei de Gauss diz: o fluxo do campo elétrico é igual à carga envolvida dividida por epsilon zero — a permissividade elétrica do vácuo, uma constante da natureza que mede o quão facilmente o campo se estabelece no vácuo.

**A14 · ≈0:40** — *Mais cargas pequenas; depois uma nuvem densa; Q_env se transforma em integral de rô dV.*  
> Mas e se a carga não for um punhado de partículas separadas? Se tiver muita carga, tão espalhada que a gente nem enxerga os grãos? Então a gente passa a descrever a carga por quanto existe em cada pedacinho de volume. Essa grandeza é a densidade volumétrica de carga, que a gente chama de rô. Em cada pedacinho de volume dV, a carga é rô vezes dV. Somando todos os pedacinhos de volume, a carga envolvida vira a integral de volume de rô dV.

_[SEGURAR] a troca Q_env → ∫ρ dV é um dos pontos centrais; deixar a nuvem de pontos visível durante toda a explicação._

**A15 · ≈0:48** — *A região se preenche como um meio contínuo; a lei se reescreve com um sobre epsilon zero vezes a integral de rô dV.*  
> Agora a gente pode reescrever a lei de Gauss com essa carga distribuída: o fluxo do campo elétrico pela superfície é igual a um sobre epsilon zero vezes a integral, no volume, da densidade de carga. Repare: do lado esquerdo, uma integral sobre a superfície; do lado direito, uma integral sobre o volume que ela envolve.

**A16 · ≈0:53** — *Aparece a pergunta "Como isso vale ponto a ponto?".*  
> Só que isso é uma lei global: ela fala do cubo inteiro. E a nossa pergunta é: como isso vale ponto a ponto?

**A17 · ≈0:56** — *Um anel marca o ponto P dentro do cubo.*  
> Vamos escolher um ponto, que eu vou chamar de P, e olhar com uma lupa cada vez mais forte em volta dele.

**A18 · ≈0:59** — *Zoom: a geometria global recua e o anel cresce.*  
> À medida que a gente se aproxima, o resto do cubo some, o resto do espaço some, e só sobra a vizinhança imediata do ponto. É nessa vizinhança minúscula que a gente vai fazer a pergunta.


## 3. Divergente: fluxo líquido por volume  
*Construção do cubo diferencial: x±dx/2, dA_x, normais, fluxo em cada face, diferença finita → derivada parcial, soma em x, y, z, divergente.*  
_1294 palavras ≈ 471 s de voz_

**B01 · ≈1:04** — *Surge um eixo x com o ponto P; aparece "x_P = x" e o texto "Primeiro, um intervalo centrado em P".*  
> Para fazer essa conta, vamos simplificar. Primeiro, só uma direção: o eixo x. O ponto P está sobre ele, na posição x. A gente vai escolher um intervalo pequeno, centrado em P, para olhar em volta.

**B02 · ≈1:07** — *Aparece o segmento com marcas nas pontas e a chave com "dx".*  
> O comprimento desse intervalo é dx: um deslocamento muito pequeno em x. O d na frente significa isso, uma quantidade infinitesimal.

**B03 · ≈1:12** — *A chave se divide em duas, cada metade rotulada dx sobre 2.*  
> Como o intervalo está centrado em P, ele se divide em duas metades iguais. Metade para a esquerda, metade para a direita. Cada uma mede dx sobre dois.

**B04 · ≈1:16** — *Os rótulos viram os extremos: x menos dx sobre 2 e x mais dx sobre 2.*  
> Então os dois extremos do intervalo ficam em x menos dx sobre dois, à esquerda, e x mais dx sobre dois, à direita. Guarda bem esses dois endereços, porque eles vão voltar daqui a pouco.

**B05 · ≈1:20** — *O segmento vira um cubo; aparecem dx, dy e dz nas arestas.*  
> Agora a gente faz a mesma ideia nas três dimensões. O intervalo vira um cubinho centrado em P, com arestas dx, dy e dz. É o nosso cubo diferencial. O cubo é pequeno o bastante para que a gente trate o campo dentro dele de forma bem simples.

**B06 · ≈1:25** — *A face direita do cubo é destacada e rotulada dA_x; surge "dA_x = dy dz".*  
> Vamos olhar a face da direita, aquela que é perpendicular ao eixo x. A área dela é a largura vezes a altura: dy vezes dz. A gente escreve dA com índice x, porque é a face cuja normal aponta na direção x. Então: dA_x é igual a dy dz.

**B07 · ≈1:31** — *Aparece a normal externa n-chapéu mais, apontando para fora, com a legenda "normal externa"; surge n+ = +x-chapéu.*  
> E para onde olha essa face? Para fora do cubo. A normal externa dela aponta no sentido positivo de x. Chamamos de n-chapéu mais, e vale mais x-chapéu — x-chapéu sendo o vetor unitário na direção x.

**B08 · ≈1:37** — *Destaca-se a face esquerda; aparece n-chapéu menos = menos x-chapéu e o texto "normais externas opostas".*  
> Já a face da esquerda olha para o lado contrário. A normal externa dela aponta para menos x. Então n-chapéu menos é igual a menos x-chapéu. As duas normais são opostas, e isso vai ser importantíssimo no cálculo do sinal.

**B09 · ≈1:44** — *Na face direita aparecem o campo E, a componente E_x e uma linha tracejada; surge "d fi = E ponto dA".*  
> Agora, o fluxo através da face direita. Aparece o campo elétrico E, inclinado, com o seu pedacinho que aponta na direção x: a componente x do campo elétrico, que a gente escreve E com índice x. O fluxo infinitesimal, d fi, é o campo ponto elemento de área: d fi é igual a E ponto dA.

**B10 · ≈1:48** — *A expressão vira "d fi x mais = E ponto x-chapéu dy dz".*  
> Como o elemento de área é a normal vezes a área, e a normal dessa face é x-chapéu, o produto escalar E ponto x-chapéu seleciona apenas a parte do campo que aponta na direção x.

**B11 · ≈1:52** — *Fica "d fi x mais = E_x dy dz"; a componente E_x pulsa.*  
> E essa parte do campo que aponta na direção x é justamente a componente E_x. Então o fluxo na face direita é E_x vezes dy dz. As componentes do campo nas direções y e z passam raspando por essa face: elas não atravessam, e por isso não entram na conta.

**B12 · ≈1:55** — *Aparece "E_x (face) dy dz".*  
> Mas em que ponto a gente calcula E_x? Na face. Como o campo pode variar de um ponto para outro, a gente precisa dizer: o valor de E_x lá onde fica a face.

**B13 · ≈1:59** — *Fica "d fi x mais = E_x (x + dx/2) dy dz"; o extremo x + dx/2 é copiado para a expressão.*  
> E onde fica a face da direita? Exatamente no extremo direito do intervalo: x mais dx sobre dois. Está vendo o endereço que a gente guardou lá atrás? Então o fluxo pela face da direita é E_x calculado em x mais dx sobre dois, vezes dy dz.

**B14 · ≈2:04** — *A expressão sobe; a face esquerda é destacada, com E, E_x e "d fi x menos = E ponto (menos x-chapéu) dy dz".*  
> Agora a face da esquerda. A conta é igual, mas com um detalhe crucial: a normal aponta para menos x. Então o produto escalar com a normal troca de sinal, e o fluxo na face esquerda é E ponto menos x-chapéu, dy dz.

**B15 · ≈2:11** — *Fica "d fi x menos = menos E_x dy dz".*  
> Isso dá menos E_x dy dz. O sinal negativo tem uma interpretação física linda: se o campo aponta para a direita, ele está entrando pela face da esquerda. Fluxo que entra conta como negativo.

**B16 · ≈2:14** — *Fica "d fi x menos = menos E_x (x - dx/2) dy dz".*  
> E onde a gente calcula E_x agora? Na face da esquerda, que fica em x menos dx sobre dois — o outro endereço que a gente guardou.

**B17 · ≈2:20** — *As duas expressões se fundem em um colchete: "d fi x = [E_x(x+dx/2) − E_x(x−dx/2)] dy dz".*  
> Agora é só somar as duas faces. O que sai pela direita, menos o que entra pela esquerda. Repare que os dois termos vêm das duas expressões que a gente acabou de construir. O fluxo líquido nas faces perpendiculares a x é: E_x na direita, menos E_x na esquerda, tudo vezes dy dz.

_[SEGURAR] bloco de ~14 s; a fusão das duas expressões é o coração do raciocínio._

**B18 · ≈2:26** — *Multiplica e divide por dx; surge um gráfico de E_x contra x com uma secante entre os dois pontos.*  
> Agora um truque muito comum: eu multiplico e divido por dx. Isso não muda nada. Mas deixa aparecer uma coisa familiar: a diferença do campo entre dois pontos, dividida pela distância entre eles. Olha no gráfico: aqui está E_x em função de x, mantendo y e z fixos. Os dois pontos são os extremos do intervalo. A reta que passa pelos dois é a secante, e a inclinação dela é exatamente essa diferença dividida por dx.

**B19 · ≈2:30** — *A secante vai virando a tangente conforme dx diminui.*  
> E o que acontece quando o intervalo encolhe? Quando dx tende a zero, os dois pontos se juntam, e a secante vira a tangente. A inclinação da tangente é a derivada. Como estamos variando só x e mantendo y e z fixos, chamamos de derivada parcial de E_x em relação a x.

_[SEGURAR] ~6 s de animação do dx → 0; a voz deve acompanhar o encolhimento, não antecipar._

**B20 · ≈2:40** — *A expressão vira "d fi x = (∂E_x/∂x) dx dy dz".*  
> Pronto: o fluxo líquido nas duas faces perpendiculares a x é a derivada parcial de E_x em relação a x, vezes dx dy dz. Em palavras: quanto o campo na direção x cresce, por unidade de distância, vezes o volume do cubo.

**B21 · ≈2:45** — *Uma chave mostra "dV = dx dy dz".*  
> E dx dy dz é o volume do cubinho. Eu chamo de dV.

**B22 · ≈2:51** — *A expressão fica "d fi x = (∂E_x/∂x) dV".*  
> Então: d fi x é igual à derivada parcial de E_x em x, vezes dV. Veja a beleza: o fluxo líquido, para o mesmo cubinho, é proporcional ao volume dele.

**B23 · ≈2:55** — *Aparecem as faces ±y e depois a linha "d fi y = (∂E_y/∂y) dV".*  
> Agora a mesma coisa nas faces de cima e de baixo. A normal da face de cima aponta para mais y, a de baixo para menos y. O raciocínio é idêntico, só trocando x por y, e o resultado é: d fi y é igual à derivada parcial de E_y em relação a y, vezes dV.

**B24 · ≈3:04** — *Aparecem as faces ±z e a linha "d fi z = (∂E_z/∂z) dV".*  
> E nas faces da frente e de trás, na direção z, a mesma coisa: d fi z é a derivada parcial de E_z em z, vezes dV.

**B25 · ≈3:08** — *Surge "d fi = d fi x + d fi y + d fi z".*  
> O fluxo total do cubo é a soma dos fluxos pelos três pares de faces: d fi é igual a d fi x mais d fi y mais d fi z.

**B26 · ≈3:12** — *As três linhas se juntam em "d fi = (∂E_x/∂x + ∂E_y/∂y + ∂E_z/∂z) dV".*  
> Colocando o dV em evidência, o fluxo líquido que sai do cubinho é: a soma das três derivadas parciais, vezes o volume.

**B27 · ≈3:16** — *Uma chave destaca a soma e aparece "divergente de E"; o cubo pisca em cada par de faces.*  
> E essa soma — a derivada de E_x em x, mais a de E_y em y, mais a de E_z em z — ganha um nome só agora, depois de a gente entender de onde ela vem: o divergente do campo elétrico.

**B28 · ≈3:20** — *A expressão vira "d fi = (nabla ponto E) dV", e depois "nabla ponto E = d fi / dV".*  
> A gente escreve com um símbolo: nabla ponto E. Nabla é aquele triângulo de cabeça para baixo, e o ponto é o produto escalar entre o operador nabla — que reúne as três derivadas parciais — e o campo. Resultado: d fi é nabla ponto E vezes dV. Isolando: o divergente é o fluxo líquido por unidade de volume.

**B29 · ≈3:28** — *Surge a definição com limite: "∇·E = lim 1/ΔV ∮ E·dA".*  
> E esse é o significado de verdade do divergente: faço um volume cada vez menor em torno de um ponto, calculo o fluxo líquido que sai pela superfície dele, divido pelo volume, e vejo o que sobra no limite. É o fluxo líquido, por unidade de volume, num ponto.

**B30 · ≈3:32** — *Cubo com fluxo saindo, e a legenda "nabla ponto E maior que 0".*  
> Se nesse ponto o fluxo líquido é para fora, as setas divergem, o divergente é positivo. Existe uma fonte ali.

**B31 · ≈3:38** — *Cubo com fluxo entrando; "nabla ponto E menor que 0".*  
> Se o fluxo líquido é para dentro, o divergente é negativo. Existe um sumidouro.

**B32 · ≈3:44** — *Cubo com campo uniforme atravessando; "nabla ponto E = 0" e o aviso "nabla ponto E = 0 não implica E = 0".*  
> E se tanto entra quanto sai, na mesma quantidade, o fluxo líquido é zero, o divergente é zero. Mas atenção: divergente zero não quer dizer campo zero. Quer dizer só que, naquele ponto, não nasce nem some campo. O campo pode ser enorme e ainda assim atravessar o cubinho sem acumular nada. Pensa numa mangueira: se entra por um lado a mesma água que sai pelo outro, não tem torneira nem ralo no meio, mas a água se move. É isso: divergente zero, campo diferente de zero.

_Gancho: comparar com água num cano; se a mesma quantidade entra e sai, não há torneira nem ralo, mas a água se move._


## 4. Teorema da divergência  
*Duas normais em cada interface interna, cancelamento, células 2→4→8, integral de volume = fluxo na fronteira.*  
_643 palavras ≈ 234 s de voz_

**C01 · ≈3:46** — *Dois cubos vizinhos, A e B, com a interface em destaque e as duas normais.*  
> Agora uma pergunta que parece desvio, mas é a chave: o que acontece quando dois volumes vizinhos dividem uma face? Aqui temos o cubo A e o cubo B, grudados. A face do meio pertence aos dois.

**C02 · ≈3:52** — *Aparecem n_A e n_B e o texto "A mesma face é saída para um volume e entrada para o vizinho".*  
> Para o volume A, a normal externa dessa face aponta para a direita, para dentro do B. Para o volume B, a normal externa da mesma face aponta para a esquerda, para dentro do A. Uma mesma face, duas normais externas, uma para cada lado.

**C03 · ≈3:56** — *Surgem uma seta de campo atravessando os dois cubos e as equações n_A = +x e n_B = −x.*  
> Com um campo atravessando da esquerda para a direita: para o A, esse campo sai por essa face. Para o B, ele entra. n-chapéu A é mais x-chapéu e n-chapéu B é menos x-chapéu.

**C04 · ≈4:00** — *Aparecem fi_A = +E·dA e fi_B = −E·dA.*  
> Então o fluxo através dessa face, para o A, é mais E ponto dA. Para o B, é menos E ponto dA. É o mesmo número, com o sinal trocado.

**C05 · ≈4:06** — *As duas contribuições se somam e dão zero.*  
> Se eu somar o fluxo dos dois volumes, a contribuição dessa face interna aparece duas vezes, uma positiva e uma negativa, e se cancela. Mais E ponto dA mais menos E ponto dA é igual a zero.

**C06 · ≈4:14** — *A cena vira uma grade de células: 2, 4, 8.*  
> Agora imagina isso com muitos cubinhos: dois, quatro, oito, quantos quiser, todos juntos formando um bloco maior.

**C07 · ≈4:22** — *As faces internas acendem, cada uma com um par de normais; depois se apagam; o contorno externo é destacado.*  
> Cada face interna tem um par de normais opostas, e em cada uma o fluxo se cancela. Elas acendem e desaparecem do cálculo. O que sobrou? Só as faces da fronteira externa, aquelas que não têm vizinho para cancelar.

**C08 · ≈4:26** — *Legendas: "faces internas: cancelam" e "só a fronteira permanece".*  
> Esse é o ponto central: tudo o que acontece dentro cancela, só a fronteira permanece.

**C09 · ≈4:30** — *Surge a soma sobre as células de (nabla·E) ΔV e ela vira a integral de volume de nabla·E dV.*  
> Cada célula contribui com o seu divergente vezes o seu volume. Somando todas as células, a soma vira, no limite, a integral de volume do divergente do campo elétrico, integral em V de nabla ponto E dV.

**C10 · ≈4:39** — *Surge a soma sobre faces externas, que vira a integral de superfície fechada de E·dA.*  
> Mas essa mesma soma também é a soma de todos os fluxos de todas as faces, e como as internas se cancelam, sobram só as externas. E a soma dos fluxos pelas faces externas é a integral de superfície fechada de E ponto dA sobre a fronteira.

**C11 · ≈4:50** — *As duas integrais se fundem na igualdade do teorema.*  
> Os dois cálculos são da mesma quantidade. Então: a integral de superfície fechada de E ponto dA é igual à integral de volume de nabla ponto E dV. Esse é o teorema da divergência, também chamado teorema de Gauss.

**C13 · ≈4:59** — *Aparece a divisão em duas colunas: "TEOREMA DA DIVERGÊNCIA" e "LEI DE GAUSS", com o mesmo fluxo à esquerda e à direita.*  
> Agora olha duas ideias diferentes sobre o mesmo fluxo. O teorema da divergência é matemática pura: vale para qualquer campo vetorial razoável, não precisa ser elétrico. A lei de Gauss é física: ela fala especificamente do campo elétrico e das cargas que o produzem.

**C14 · ≈5:04** — *O fluxo do teorema vira a integral do divergente; o da lei vira um sobre epsilon zero vezes a integral de rô.*  
> Do lado do teorema, o fluxo é a integral do divergente do campo. Do lado da lei de Gauss, o fluxo é um sobre epsilon zero vezes a integral da densidade de carga. Duas leituras da mesma grandeza.

**C15 · ≈5:07** — *Fica "∫ nabla·E dV = ∫ (rô/ε0) dV" e depois "∫ (nabla·E − rô/ε0) dV = 0".*  
> Igualando as duas: a integral do divergente é igual à integral de rô sobre epsilon zero. Passando tudo para um lado, a integral, em V, de nabla ponto E menos rô sobre epsilon zero, dV, é igual a zero.

**C16 · ≈5:13** — *Um volume vai encolhendo ao redor de um ponto, com o texto "Qualquer volume regular apropriado".*  
> E isso vale para qualquer volume — grande, pequeno, o que a gente quiser. Então eu posso encolher o volume até um ponto. Se a integral é zero para qualquer volume, por menor que seja, a única possibilidade é que o que está dentro dela seja zero em cada ponto.

**C17 · ≈5:18** — *A equação vira "nabla ponto E = rô sobre epsilon zero", dentro de uma caixa.*  
> Isso nos dá a lei de Gauss na forma diferencial: nabla ponto E é igual a rô sobre epsilon zero. Em cada ponto do espaço: o divergente do campo elétrico é a densidade de carga ali, dividida por epsilon zero.

**C18 · ≈5:22** — *Aparecem "rô > 0 ⇒ nabla·E > 0" e depois "rô < 0 ⇒ nabla·E < 0".*  
> Se há carga positiva no ponto, o divergente é positivo: o campo nasce ali, a carga positiva é fonte. Se há carga negativa, o divergente é negativo: as linhas de campo morrem ali, a carga negativa é sumidouro. A carga é a fonte do campo — só que agora dito ponto a ponto.


## 5. Um exemplo: campo que cresce com a posição  
*E = κ(x x̂ + y ŷ + z ẑ): três derivadas iguais a κ somam 3κ.*  
_187 palavras ≈ 68 s de voz_

**K01 · ≈5:29** — *Campo com setas que crescem para longe da origem; surge a fórmula E = κ(x x-chapéu + y y-chapéu + z z-chapéu).*  
> Vamos ver como isso funciona num exemplo concreto, bem simples. Esse campo aqui tem a seguinte forma: E é kappa vezes x x-chapéu mais y y-chapéu mais z z-chapéu. Kappa é uma constante: um número fixo que diz o quanto o campo cresce a cada unidade de distância.

**K02 · ≈5:31** — *Um ponto de prova se afasta da origem e a seta cresce; surge "|E| proporcional a r".*  
> Quanto mais longe da origem, mais forte é o campo, proporcional à distância r. Ele aponta para fora e vai crescendo.

**K03 · ≈5:36** — *Eixos x, y, z e um ponto de prova sobre cada um, com E_x = κ x e a derivada parcial igual a κ.*  
> Vamos calcular o divergente. Pelo que a gente construiu, precisamos das derivadas parciais, uma por uma. A componente x do campo é kappa vezes x. Derivando em relação a x, sobra kappa. A componente y é kappa y; derivando em relação a y, kappa. A componente z é kappa z; derivando em relação a z, também kappa.

**K03b · ≈5:46** — *Três kappas se somam: "kappa + kappa + kappa", que vira "3 kappa"; aparece "nabla·E =" ao lado.*  
> Somando as três, o divergente é três kappa. É constante, o mesmo em todo ponto do espaço. Isso nos conta algo físico: para um campo desse tipo, haveria carga distribuída uniformemente por todo o espaço, com densidade rô igual a três epsilon zero kappa, porque a lei de Gauss diz que rô é epsilon zero vezes o divergente.

_Observação para o roteiro: na tela hoje a legenda do κ está pequena demais (ver relatório); ajustar tamanho._


## 6. Carga pontual e a delta de Dirac  
*Divergente zero fora da origem, fluxo constante, o conflito, o volume que encolhe, a delta tridimensional, rô = q δ³.*  
_754 palavras ≈ 274 s de voz_

**D01 · ≈5:52** — *Campo de uma carga pontual; fórmula E = q/(4πε0) r-chapéu / r² e nabla·E = 0 (r ≠ 0).*  
> Vamos para o caso mais importante: uma única carga pontual. O campo dela é E igual a q sobre quatro pi epsilon zero, vezes r-chapéu sobre r ao quadrado. Aqui q é o valor da carga, r é a distância até ela, r-chapéu é o vetor unitário que aponta da carga para fora. É a lei de Coulomb, escrita como campo. Se a gente calcular o divergente dessa expressão, em qualquer ponto fora da origem, dá zero.

**D02 · ≈5:56** — *Um cubinho de prova passeia pelo campo e é marcado em três posições.*  
> Dá para sentir isso no cubinho: leve ele para lá, para cá, para onde quiser, menos para cima da carga. Sempre entra tanto campo quanto sai. O divergente é zero. A carga é a fonte, mas nenhum ponto fora dela é fonte.

**D03 · ≈6:17** — *O cubo some; surge uma esfera em volta da carga com o campo na fronteira; fluxo = q/ε0.*  
> Mas olha o que acontece com o fluxo através de uma esfera em volta da carga. A lei de Gauss diz: o fluxo é q sobre epsilon zero. E esse resultado não depende do raio da esfera.

**D04 · ≈6:24** — *A esfera encolhe, com a razão R sobre R zero caindo de 1 para 0,15, e a legenda "FLUXO CONSTANTE".*  
> Vamos fazer a esfera encolher. O raio R vai diminuindo, comparado com o raio inicial, R zero. Um, meio, um décimo... O campo na superfície fica cada vez mais forte, mas a área fica cada vez menor, e os dois efeitos se compensam exatamente: o fluxo continua o mesmo, q sobre epsilon zero. Isso acontece porque o campo cai com o quadrado da distância e a área da esfera cresce com o quadrado do raio.

_[SEGURAR] ~10 s de encolhimento; a voz explica o compromisso campo × área sem pressa._

**D05 · ≈6:34** — *Aparece "fora da origem, o divergente é zero" e a pergunta "Onde está a fonte?".*  
> Então temos um problema. Fora da origem, o divergente é zero. Mas o fluxo, por uma superfície em volta da origem, não é zero. Onde está a fonte?

**D06 · ≈6:37** — *Reaparecem as duas informações em conflito e a pergunta "Como representar uma fonte inteira concentrada em um único ponto?".*  
> Olha o conflito. De um lado, divergente zero em todo ponto fora da origem. Do outro, fluxo diferente de zero por qualquer superfície que envolva a origem. A única saída é que o divergente seja zero em todo lugar menos num ponto — mas que nesse ponto ele concentre toda a fonte. Como a gente representa matematicamente uma fonte inteira concentrada em um único ponto?

**D07 · ≈6:39** — *Um volume encolhe em torno da origem com Q_env = q; a legenda diz que a carga dentro não muda.*  
> Olha o que acontece com a carga envolvida quando o volume encolhe. O volume diminui, diminui... e a carga dentro continua sendo q. O volume vai a zero, a carga não vai.

**D08 · ≈6:46** — *Título "Delta de Dirac tridimensional" e o símbolo delta com índice 3 e r vetor.*  
> Precisamos de um objeto que faça exatamente isso: que seja zero fora de um ponto, e que, mesmo assim, integrado em qualquer região que contenha o ponto, dê um. Esse objeto se chama delta de Dirac tridimensional, e se escreve delta três de r.

**D09 · ≈6:48** — *Aparece a anotação "(3): três dimensões, não potência" e "uma distribuição que concentra integral unitária num ponto".*  
> Esse três no expoente não é uma potência. Delta ao cubo não é a ideia aqui. É só o aviso de que estamos em três dimensões. E a delta é o que os matemáticos chamam de distribuição: um objeto que concentra integral unitária num ponto.

**D10 · ≈6:51** — *Um volume V se aproxima da origem; aparece "∫_V δ³(r) dV = 0" e a legenda "origem fora de V".*  
> Pra entender o que ela faz, vamos usar um volume de teste, V. Quando a origem está fora desse volume, a integral da delta em V é zero. A delta vale zero em todos os pontos de V.

**D11 · ≈6:57** — *O volume atravessa a origem; um flash na carga; "∫_V δ³ dV = 1" e "origem dentro de V".*  
> Agora o volume avança até conter a origem. E o resultado muda: a integral da delta sobre V passa a ser um. A integral não vale 1 sobre a fronteira, e é por isso que a gente evita afirmar o valor justo quando a origem está na borda. Sempre um se a origem está dentro, sempre zero se está fora. Quando a origem está exatamente na superfície do volume, o valor não é definido de forma simples. Por isso a gente não afirma nada nesse instante: só olha o antes e o depois.

**D12 · ≈7:04** — *Aparecem "não é uma função comum: só ganha sentido sob uma integral" e a unidade [δ³] = m⁻³.*  
> É importante guardar: a delta não é uma função comum. Ela só ganha sentido dentro de uma integral. E tem unidade: como a integral da delta sobre um volume dá um número puro, a delta tem unidade de um sobre metro cúbico. Metro à menos três.

**D13 · ≈7:08** — *A carga q sobe e se transforma em "rô(r) = q δ³(r)".*  
> Agora a conexão com a física. A carga q está concentrada numa origem. A densidade de carga dessa configuração é rô de r igual a q vezes delta três de r. Zero em todo lugar, menos na origem, e integrando no volume, dá exatamente q.

**D14 · ≈7:13** — *Aparecem "carga total q concentrada em r = 0" e a lei de Gauss diferencial; as duas se fundem em ∇·E = (q/ε0) δ³(r).*  
> Colocando na lei de Gauss diferencial: nabla ponto E é rô sobre epsilon zero, que é q sobre epsilon zero vezes delta três de r.

**D15 · ≈7:21** — *O volume de teste encolhe sobre a carga; texto "a delta resolve o conflito: divergente zero fora, fonte na origem".*  
> E aí o conflito desaparece: fora da origem a delta é zero, então o divergente é zero. Na origem, a delta concentra tudo, então existe fonte. Divergente zero fora, fonte inteira na origem. Essa mesma ideia aparece na gravitação, onde uma massa pontual é a fonte do campo gravitacional, e na mecânica quântica, onde a delta descreve uma partícula perfeitamente localizada.

_Gancho: a mesma delta aparece na gravitação, onde uma massa pontual é fonte do campo gravitacional, e na mecânica quântica, onde descreve uma partícula perfeitamente localizada._


## 7. Mesmo divergente, outra geometria: Ω e o rotacional  
*Dois campos F1 e F2 com divergente zero, a constante Ω controlando o giro, a sonda e o medidor de giro local, ∇×F.*  
_407 palavras ≈ 148 s de voz_

**D16 · ≈7:34** — *Título "Mesmo divergente, outra geometria"; surge o campo uniforme F1 = F0 x-chapéu com um cubo de teste e ∇·F1 = 0.*  
> O divergente é uma pergunta sobre fonte. Mas existe outra pergunta sobre o campo, completamente diferente. Veja este primeiro campo. F1 é igual a F zero vezes x-chapéu: todas as setas apontam para a direita, com a mesma intensidade. O divergente dele é zero, porque o que entra num cubinho é igual ao que sai.

**D17 · ≈7:38** — *Surge o eixo com Ω e quatro pontos com setas tangenciais.*  
> Agora um campo bem diferente. Em vez de linhas retas, ele dá voltas em torno do centro. Em cada ponto, a seta é tangente a um círculo. E tem uma constante que controla o quão rápido ele gira: ômega, a letra grega maiúscula. Ômega maior, giro mais forte; ômega zero, sem giro.

**D18 · ≈7:41** — *O valor de Ω sobe de 0,6 a 1,3 e as setas crescem.*  
> Eu posso aumentar ômega, e as setas ficam mais fortes. Isso é só uma intensidade, é como o volume desse giro.

**D19 · ≈7:48** — *Ω vira a fórmula F2 = Ω(−y x-chapéu + x y-chapéu); aparece o campo completo.*  
> A fórmula completa desse campo, que eu vou chamar de F dois, é: ômega vezes menos y x-chapéu mais x y-chapéu. Em cada ponto de coordenadas x e y, o campo aponta perpendicularmente ao raio. Por isso ele gira. E se você calcular o divergente dele, dá zero também. Os dois campos, F um e F dois, têm divergente zero. Mas são completamente diferentes! Um é reto, o outro gira.

**D20 · ≈8:11** — *Telas lado a lado: F1 com sonda parada e F2 com sonda girando; surge o medidor GIRO LOCAL.*  
> Para enxergar essa diferença, imagine colocar uma rodinha de pás em cada campo, como uma roda d'água. No campo reto, as pás sentem a mesma força dos dois lados, e a roda fica parada. No campo que gira, o lado de cima empurra para um lado e o lado de baixo empurra para o outro, e a roda gira. Esse barrinha, o giro local, mostra isso: no campo reto, zero; no campo que gira, ele cresce com ômega.

**D21 · ≈8:15** — *Surge o operador "nabla vezes F" no centro, com "mede o giro local do campo".*  
> Existe um operador que mede esse giro: nabla vezes F, o rotacional do campo F. Ele faz, para o giro, o que o divergente faz para a fonte.

**D22 · ≈8:25** — *Aparecem ∇×F1 = 0 e ∇×F2 = 2Ω z-chapéu, com o símbolo da direção de z.*  
> Para o campo reto, o rotacional é zero. Para o campo que gira, o rotacional é dois ômega vezes z-chapéu. O dois aparece porque o giro local do campo é o dobro da velocidade angular do campo. E o z-chapéu diz a direção do giro: usando a regra da mão direita, se os dedos acompanham o giro, o polegar aponta para fora da tela, na direção z positiva.

**D23 · ≈8:36** — *A cena limpa e o operador vira "nabla vezes E", agora no campo eletrostático.*  
> Agora a pergunta que importa para a gente: e o campo eletrostático, aquele criado por cargas paradas? Ele gira ou não gira? É isso que a gente vai descobrir.


## 8. Circulação: acumular ao longo do caminho  
*Integral de linha de E·dℓ entre a e b, só a componente radial conta, 1/r_a − 1/r_b, dois caminhos com o mesmo valor, ida por C1 e volta por C2: zero.*  
_582 palavras ≈ 212 s de voz_

**E01 · ≈8:46** — *Carga pontual, pontos a e b, os raios r_a e r_b tracejados; surge o caminho C1.*  
> Para responder, a gente precisa de uma nova ferramenta: a circulação. Aqui está uma carga pontual, e dois pontos, a e b. A distância da carga até a é r a; a distância da carga até b é r b. E um caminho, C um, que vai de a até b.

**E02 · ≈8:51** — *Surge "∫_C1 E·dℓ"; um ponto percorre o caminho, com o vetor dℓ tangente e o campo E em cada posição.*  
> A gente quer somar, ao longo desse caminho, o quanto o campo ajuda ou atrapalha o movimento. Em cada ponto, tem o campo elétrico E, e tem o deslocamento infinitesimal ao longo do caminho, dℓ: uma setinha muito curta, tangente ao caminho, que aponta no sentido em que a gente está andando. Fazemos o produto escalar E ponto dℓ, e somamos tudo ao longo do caminho: integral em C um de E ponto dℓ. É a circulação ao longo do caminho. A barrinha embaixo mostra essa soma acumulando.

**E03 · ≈8:58** — *O caminho já foi percorrido; aparece a decomposição de dℓ em componente radial dr e a componente transversal.*  
> Qual é o valor dessa conta? Para uma carga pontual, o campo aponta sempre na direção radial. Então só a parte de dℓ que também é radial importa. Essa parte é o dr: a variação da distância até a carga. A parte transversal, perpendicular ao raio, não entra no produto escalar, porque é perpendicular ao campo.

**E04 · ≈8:59** — *Surge "E·dℓ = q/(4πε0 r²) dr".*  
> Então E ponto dℓ é q sobre quatro pi epsilon zero r ao quadrado, vezes dr.

**E05 · ≈9:03** — *A expressão vira "∫ E·dℓ = q/(4πε0) ∫ dr/r²" com limites de r_a a r_b.*  
> Somando ao longo do caminho, o r vai de r a até r b, então a integral é: q sobre quatro pi epsilon zero, vezes a integral de dr sobre r ao quadrado, indo de r a até r b.

**E06 · ≈9:06** — *A expressão vira q/(4πε0) vezes (1/r_a − 1/r_b); r_a e r_b piscam.*  
> E a integral de um sobre r ao quadrado, dr, é menos um sobre r. Calculando entre r a e r b, dá: um sobre r a, menos um sobre r b. Então a circulação ao longo do caminho C um é q sobre quatro pi epsilon zero vezes um sobre r a menos um sobre r b. Veja: o resultado só depende dos extremos. Não depende de como o caminho passa pelo meio.

_Gancho: isso é exatamente a forma da energia potencial de Coulomb, que aparece lá no fim._

**E07 · ≈9:11** — *O resultado sobe; surge um segundo caminho C2 com os mesmos extremos e outro tracer.*  
> Vamos conferir com outro caminho. Aqui está o C dois: sai do mesmo ponto a, chega no mesmo ponto b, mas dá uma volta bem diferente.

**E08 · ≈9:21** — *C2 percorrido; a expressão com C2 aparece igual à de C1.*  
> E o resultado é o mesmo: q sobre quatro pi epsilon zero, vezes um sobre r a menos um sobre r b. Outro caminho, a mesma circulação.

**E09 · ≈9:23** — *As duas se fundem: "∫_C1 E·dℓ = ∫_C2 E·dℓ"; o texto "caminhos diferentes, mesmos extremos".*  
> Então a circulação por C um é igual à circulação por C dois. Caminhos diferentes, mesmos extremos, mesmo valor. É uma propriedade de campos que, no jargão, são conservativos. Se você já viu trabalho de uma força conservativa, é a mesma ideia: o trabalho só depende da posição inicial e da final.

**E10 · ≈9:28** — *Aparece "C = C1 − C2".*  
> Agora a ideia decisiva: vai por C um e volta por C dois, no sentido contrário. Isso forma um caminho fechado, que eu vou chamar de C. Como a volta é feita ao contrário, o que a gente acumula na volta tem sinal oposto. Então a circulação do caminho fechado é C um menos C dois.

**E11 · ≈9:31** — *Um tracer percorre a volta completa; a barra acumula e volta ao zero.*  
> E olha o que acontece quando a gente anda esse caminho completo. A barra sobe na ida; na volta, ela desce, e fecha no zero. Quando a gente volta ao ponto inicial, não sobra nada.

**E12 · ≈9:42** — *Aparece "∮_C E·dℓ = 0".*  
> Então a circulação do campo elétrico, ao longo de qualquer caminho fechado, é zero: integral de linha fechada de E ponto dℓ igual a zero. Nenhum caminho fechado ganha energia dando voltas num campo eletrostático. Compara com um redemoinho: na água, ao dar uma volta em torno do centro, você ganha circulação. No campo eletrostático, dar a volta não rende nada.

_Gancho: contraste com um moinho de água, onde a água que circula em volta de um redemoinho acumula circulação diferente de zero._


## 9. Teorema de Stokes: da borda ao interior  
*Circulação na borda = soma de pequenos giros locais no interior; ∇×F; F → E; ∇×E = 0.*  
_466 palavras ≈ 169 s de voz_

**E13 · ≈9:46** — *O caminho fechado vira a curva C; surge "∮_C F·dℓ" e um ponto percorre a borda com setinhas dℓ tangentes.*  
> Agora a pergunta é: dá para ligar essa circulação, que é uma conta feita na borda de uma curva, com o giro local, que é uma coisa que acontece no interior? Imagine uma curva fechada C, e um campo qualquer, F. A circulação do campo ao longo da curva é a integral de linha fechada de F ponto dℓ. A gente anda sobre a borda, e o dℓ aponta tangente ao caminho.

**E14 · ≈9:57** — *Uma superfície S, preenchida, se estende dentro da curva; aparecem 7 pequenos rotores.*  
> Agora imagine uma superfície S, que tem essa curva como borda: como a película de uma bolha de sabão presa num aro. Dentro dessa película, em cada pedacinho, o campo faz um pequeno giro. São pequenos rotores locais, cada um medindo a circulação num pedacinho minúsculo.

**E15 · ≈10:01** — *Cada rotor vira um vetor nabla×F, com a normal n-chapéu e o rótulo dA.*  
> O giro de cada pedacinho vira um vetor: o rotacional do campo, nabla vezes F, apontando na direção do eixo do giro. Cada pedacinho tem a sua área, dA, e a sua normal, n-chapéu. A contribuição de cada pedacinho é o rotacional ponto n-chapéu, vezes dA: o quanto desse giro atravessa o pedacinho, na direção da normal.

**E16 · ≈10:09** — *Surge "d A vetor = n-chapéu dA" e depois "(∇×F)·n-chapéu dA".*  
> Isso a gente já viu antes: o elemento de área vetorial, dA vetor, é a normal vezes dA. Então a contribuição de cada pedacinho é nabla vezes F, ponto dA vetor.

**E17 · ≈10:14** — *A soma sobre os pedacinhos vira "∫_S (∇×F)·dA".*  
> Somando todos os pedacinhos da superfície, a soma vira uma integral de superfície: integral em S de rotacional de F ponto dA.

**E18 · ≈10:22** — *Aparece a igualdade completa do teorema de Stokes.*  
> E aí vem o teorema de Stokes. A circulação na borda é igual ao rotacional acumulado no interior: integral de linha fechada de F ponto dℓ é igual à integral de superfície de nabla vezes F ponto dA. O que acontece na borda é a soma de tudo que gira lá dentro, porque nos pedacinhos vizinhos o giro de um cancela com o do outro, igualzinho àquelas faces internas do cubo, e só sobra a borda. É o mesmo truque de cancelamento interno do teorema da divergência, agora para giros em vez de fluxos: um é primo do outro.

_Gancho: mesma estrutura de cancelamento interno do teorema da divergência; um é o primo do outro._

**E19 · ≈10:28** — *O título muda para "No campo eletrostático"; F vira E; os rotores param.*  
> Agora, trocando F por E, o campo elétrico estático. Já sabemos que a circulação é zero em qualquer caminho fechado. Então os pequenos giros param.

**E20 · ≈10:37** — *Aparecem "∮ E·dℓ = 0" e depois "0 = ∫ (∇×E)·dA" e "∫ (∇×E)·dA = 0".*  
> Se a circulação na borda é zero, o rotacional acumulado no interior também é zero: integral de superfície de nabla vezes E ponto dA igual a zero. E isso vale para qualquer superfície que eu desenhe.

**E21 · ≈10:45** — *Um pequeno quadrado de superfície gira em várias orientações; "(∇×E)·n-chapéu ΔA = 0".*  
> Então eu posso pegar uma superfície minúscula, de área delta A, virada para onde eu quiser, e a conta continua dando zero. Em qualquer pequena superfície, em qualquer orientação, nabla vezes E ponto n-chapéu vezes delta A é zero. A única forma de isso ser verdade para toda orientação é que o próprio vetor, nabla vezes E, seja zero.

**E22 · ≈10:58** — *A equação vira "∇×E = 0", dentro de uma caixa.*  
> E aí está: o rotacional do campo elétrico estático é zero. O campo eletrostático é irrotacional.


## 10. O mapa final  
*Duas perguntas locais; dois operadores; duas leis; global → local.*  
_150 palavras ≈ 55 s de voz_

**F01 · ≈11:04** — *Surge E(r) no topo; "Há fonte local?" à esquerda, com o cubo e o fluxo; "FLUXO".*  
> Vamos juntar tudo. No topo, o campo elétrico, que depende da posição. E duas perguntas, uma de cada lado. À esquerda: há fonte local? Para responder, usamos um cubinho e o fluxo através dele.

**F02 · ≈11:09** — *À esquerda: "∇·E" vira "∇·E = ρ/ε0", com a legenda "GAUSS · GLOBAL → LOCAL".*  
> A resposta vem do divergente. E o divergente do campo elétrico é a densidade de carga sobre epsilon zero. É a lei de Gauss, passando do global ao local.

**F03 · ≈11:17** — *À direita: "Há circulação local?", com a rodinha e o campo uniforme.*  
> À direita: há circulação local? Aqui usamos uma rodinha, o rotacional.

**F04 · ≈11:24** — *À direita: "∇×E" vira "∇×E = 0" com a legenda "STOKES · GLOBAL → LOCAL".*  
> O rotacional do campo eletrostático é zero. É o teorema de Stokes, também passando do global ao local.

**F05 · ≈11:30** — *Os dois lados pulsam juntos.*  
> Duas perguntas, dois operadores. Fonte local: divergente, que vale a densidade de carga sobre epsilon zero. Giro local: rotacional, que vale zero. É assim que a eletrostática inteira cabe em duas equações. E repara que a eletrostática inteira cabe em duas equações: divergente de E igual a rô sobre epsilon zero, e rotacional de E igual a zero.


## 11. Faraday e o potencial elétrico  
*Quando B varia no tempo o rotacional deixa de ser zero; na eletrostática ∂B/∂t = 0; V como campo escalar e E = −∇V.*  
_279 palavras ≈ 101 s de voz_

**F06 · ≈11:40** — *Surge "∇×E = −∂B/∂t" com um campo B pulsando à esquerda.*  
> Mas calma, não é sempre zero. Esse resultado vale na eletrostática. Existe uma equação mais geral, a lei de Faraday: nabla vezes E é igual a menos a derivada parcial do campo magnético B em relação ao tempo. Se o campo magnético varia no tempo, o campo elétrico passa a ter rotacional. É o princípio dos geradores e dos transformadores.

**F07 · ≈11:46** — *B(t) oscila e depois congela; surge "∂B/∂t = 0".*  
> Na eletrostática, as cargas estão paradas, e não há campo magnético variando. Então a derivada de B em relação ao tempo é zero.

**F08 · ≈11:54** — *A expressão vira "∇×E = −0" e depois "∇×E = 0".*  
> E o termo da direita some: menos zero é zero. Aí o rotacional de E volta a ser zero. O zero da eletrostática não é um acaso: nasce de não haver variação de campo magnético.

**F09 · ≈12:00** — *Surge uma carga e arcos de equipotenciais, com rótulos V1, V2, V3.*  
> E agora uma ideia que sai desse zero. Como o rotacional é zero e o campo é conservativo, a gente pode descrever o campo elétrico por um único número em cada ponto do espaço: o potencial elétrico, V. Aqui estão superfícies de mesmo potencial, as equipotenciais: V um, V dois, V três.

**F10 · ≈12:06** — *Um ponto percorre uma equipotencial e depois sobe de V; surgem as setas branca (gradiente) e ciana (E).*  
> O potencial é um campo escalar: um número em cada ponto, sem direção. O gradiente de V, nabla V, é um vetor que aponta para onde V cresce mais depressa. E o campo elétrico aponta no sentido contrário, para onde V cai mais depressa.

**F11 · ≈12:11** — *"∇V" vira "E = −∇V"; texto: "um campo vetorial descrito por um escalar".*  
> Então: o campo elétrico é menos o gradiente do potencial. Um campo vetorial, com três componentes, descrito por um escalar, com um número só. Essa é a ponte para o próximo assunto: o potencial elétrico. Se você já viu um mapa topográfico, é a mesma ideia: as linhas de nível são as equipotenciais, e a água, como o campo, escorre pela direção de maior descida.

_Gancho: tem a ver com energia potencial, linhas de nível de um mapa topográfico e a ideia de que a água desce a ladeira._


## 12. Payoff e CTA  
*Fechamento e chamada para inscrição, no padrão de yt_0001/yt_0002.*  
_68 palavras ≈ 25 s de voz_

**G01 · ≈12:18** — *Surge "DIVERGENTE E ROTACIONAL".*  
> Divergente e rotacional. Duas perguntas locais sobre um campo, que a gente aprendeu a responder a partir de superfícies e caminhos inteiros.

**G02 · ≈12:22** — *Surge "FLUXO → FONTE LOCAL · CIRCULAÇÃO → GIRO LOCAL".*  
> Fluxo, que vira fonte local. Circulação, que vira giro local. Gauss para o primeiro, Stokes para o segundo.

**G03 · ≈12:30** — *A logo Parallax Lab e anéis tracejados.*  
> Esse foi mais um passo dentro do eletromagnetismo, aqui no Parallax Lab.

**G04 · ≈12:33** — *Surge "Inscreva-se para acompanhar os próximos vídeos".*  
> Se esse vídeo te ajudou, se inscreve no canal para acompanhar os próximos. Até a próxima.


## Comparação voz × cena (por seção)

| Seção | Palavras | Voz estimada | Início atual no vídeo |
|---|---|---|---|
| 1. Hook e pergunta central | 198 | 72 s | 0:00 |
| 2. Do fluxo global à carga envolvida | 646 | 235 s | 0:08 |
| 3. Divergente: fluxo líquido por volume | 1294 | 471 s | 1:04 |
| 4. Teorema da divergência | 643 | 234 s | 3:46 |
| 5. Um exemplo: campo que cresce com a posição | 187 | 68 s | 5:29 |
| 6. Carga pontual e a delta de Dirac | 754 | 274 s | 5:52 |
| 7. Mesmo divergente, outra geometria: Ω e o rotacional | 407 | 148 s | 7:34 |
| 8. Circulação: acumular ao longo do caminho | 582 | 212 s | 8:46 |
| 9. Teorema de Stokes: da borda ao interior | 466 | 169 s | 9:46 |
| 10. O mapa final | 150 | 55 s | 11:04 |
| 11. Faraday e o potencial elétrico | 279 | 101 s | 11:40 |
| 12. Payoff e CTA | 68 | 25 s | 12:18 |
| **Total** | **5674** | **34.4 min** | vídeo atual 12:49 |

O vídeo tende a ficar com ~2,7× a duração atual (12:49 → ~34 min). Se o GPT achar longo, cortar primeiro os ganchos e as repetições; a ordem e as âncoras não mudam.
