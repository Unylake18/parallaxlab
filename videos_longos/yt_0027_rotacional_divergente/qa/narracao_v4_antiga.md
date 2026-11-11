# yt_0027 · narração por âncora (Anexo A do handoff v1 + as três falas novas do handoff v2 §5 e as quatro do handoff v3 §6, 2026-11-11; fonte do ancoras.json)

Cada `###` é uma âncora (evento visual). A linha do cabeçalho traz o `tela:`; a fala começa ~0,15 s depois. Tags `[ ]` do ElevenLabs v4 não são faladas.

## H · DOIS REDEMOINHOS

### H1 · tela: dois painéis iguais lado a lado, campo em setas e tinta em xadrez; à esquerda (−y, x), à direita (−y, x)/(x² + y²) com o furo; uma rodinha coral cai em cada painel no ponto (1, 0)
[curious] Olha esses dois redemoinhos. Nos dois, tudo dá voltas em torno do centro. Agora vamos soltar uma rodinha de pás em cada um, exatamente na mesma distância do centro, e deixar a correnteza levar.

### H2 · tela: as duas órbitas completas ao mesmo tempo; à esquerda a tinta gira rígida e a rodinha gira junto; à direita a tinta se enrola em espiral e a rodinha volta com a pá marcada para cima
[thoughtful] No primeiro, a rodinha dá a volta e, no caminho, vai girando em torno de si mesma: quando completa a volta, ela também completou um giro. No segundo… olha só: ela dá a volta inteira e chega do mesmo jeito que saiu. A pá marcada fica apontando para cima o tempo todo, igualzinho à cabine de uma roda-gigante.

### H3 · tela: congela; a circunferência r = 1 acende nos dois painéis; as setas sobre ela acendem aos pares, uma de cada lado ao mesmo tempo
[curious] E agora vem a parte mais estranha. Em cima dessa circunferência por onde as rodinhas passaram, os dois campos são idênticos: seta por seta, mesmo tamanho, mesma direção. As duas rodinhas passaram exatamente pelas mesmas setas! Então por que uma gira e a outra não? E, afinal, o que quer dizer um campo girar num ponto?

## A · BEM-VINDOS

### A1 · tela: logo; `BEM-VINDOS AO PARALLAX LAB`; título `ROTACIONAL E DIVERGENTE` e `NESTE VÍDEO: GIRO · ESPALHAMENTO · NUM PONTO SÓ`; o canto entra
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab. Hoje a aula é sobre duas medidas que um campo vetorial carrega em cada ponto: o rotacional, que mede o giro, e o divergente, que mede o espalhamento. A gente vai descobrir de onde vêm as fórmulas, o que elas medem de verdade, por que o desenho de longe engana… e onde tudo isso aparece na física. Vai ter rodinha, caixa, rio, tornado e até fio elétrico. Bora?

## B1 · UM PEDACINHO DE FLUIDO

### B1-1a · tela: (handoff v4 §3.1) campo (−y, 2x) em contexto; a seta em (0,5; 1,3) acende e se decompõe em P (horizontal) e Q (vertical); coluna Ω ⊂ ℝ² aberto, F(x, y) = (P(x, y), Q(x, y)), P = −y, Q = 2x
[thoughtful] Antes de tudo, vamos dar nome às peças. Um campo vetorial no plano coloca uma seta em cada ponto de uma região aberta, que a gente chama de ômega. Aberta quer dizer sem a borda: dá para chegar perto de cada ponto por todos os lados, e é isso que deixa a gente derivar. Toda seta se quebra em duas partes. A parte horizontal a gente chama de P, e a vertical, de Q. E as duas mudam de ponto para ponto: P e Q são funções de x e de y. Neste campo, P é menos y, e Q é dois x. Então, daqui para frente, quando aparecer derivada de P ou de Q, é isso: a gente está olhando como uma das partes da seta muda.

### B1-1 · tela: campo (−y, 2x) com pontinhos de fluido andando; selo pequeno `CAMPO = VELOCIDADE · ESCOAMENTO ESTACIONÁRIO · CAMPO LISO`
[thoughtful] Primeiro, uma combinação. Durante a aula inteira, a gente vai ler o campo como a velocidade de um fluido: a seta em cada ponto é a velocidade de quem passa por ali, e o escoamento não muda com o tempo. E P e Q são lisas, com derivadas parciais contínuas. É isso que deixa todas as contas de hoje funcionarem.

### B1-2 · tela: a lupa sobre um ponto; três passos de zoom; as setas da lupa ficando quase iguais; a diferença entre a ponta de uma seta e a da vizinha em coral; CANETA `\dfrac{\Delta \vec F}{h} \;\to\; \dfrac{\partial \vec F}{\partial x}`
[curious] Agora pega uma lupa e chega bem pertinho de um ponto. De perto, as setas ficam quase todas iguais. Quase! Se fossem exatamente iguais, um pedacinho de fluido ali só seria carregado, sem mudar nada. Toda a graça está nas pequenas diferenças entre uma seta e a vizinha. E diferença entre vizinhos, dividida pela distância, quando os vizinhos ficam cada vez mais perto, tem nome: derivada parcial.

### B1-3 · tela: três miniaturas, uma por frase: `GIRA`, `MUDA DE ÁREA`, `DEFORMA`; depois `GIRA` ganha `ROTACIONAL` e `MUDA DE ÁREA` ganha `DIVERGENTE`
[thoughtful] Então solta um quadradinho de fluido nesse ponto e deixa ele andar um instante. Além de ser carregado, ele pode fazer três coisas. Pode girar. Pode crescer ou encolher, mudando de área. E pode se deformar, esticando para um lado e achatando para o outro, sem mudar de área. As duas primeiras ganham nome hoje: o giro é medido pelo rotacional, e a mudança de área, pelo divergente. A terceira, a deformação, fica guardada para o fim da aula.

## B2 · ROTACIONAL

### B2-1 · tela: campo (−y, 2x); braço horizontal coral AB; nas pontas, só as componentes verticais do campo (ciano), a de B maior; a diferença entre elas em coral
[thoughtful] Vamos começar pelo giro. Em vez da rodinha inteira, pega só duas partículas de fluido vizinhas, uma ao lado da outra na horizontal, ligadas por um braço. Cada ponta do braço é carregada pela seta do campo no lugar onde ela está.

### B2-2 · tela: o braço gira um pouco no anti-horário (fluxo exato); CANETA `\omega_{AB} \approx \dfrac{Q(x_0 + h,\, y_0) - Q(x_0,\, y_0)}{h}`; h encolhe; `TransformByGlyphMap` para `\omega_{AB} = \dfrac{\partial Q}{\partial x}`
[curious] Repara só na parte vertical dessas setas. Se a ponta da direita sobe mais rápido que a da esquerda, o braço gira no sentido anti-horário. E com que rapidez? A diferença entre as duas velocidades verticais, dividida pelo comprimento do braço. Agora encolhe o braço: essa razão vira a derivada do Q, a componente vertical, na direção x. Essa é a velocidade angular do braço horizontal.

### B2-3 · tela: ao lado, um braço-fantasma GEO tracejado com setas para a direita, a de cima maior, tombando no horário; depois o braço vertical coral AC no campo, com a ponta de cima indo para a esquerda mais rápido, girando no anti-horário; CANETA `\omega_{AC} = -\dfrac{\partial P}{\partial y}`, com o sinal de menos por último; embaixo `-(-1) = 1`
[thoughtful] Agora um braço vertical, com uma partícula embaixo e outra em cima. Para ele, o que importa é a parte horizontal das setas. Se a ponta de cima anda para a direita mais rápido que a de baixo, o braço tomba para a direita, no sentido horário. Por isso a velocidade angular dele é menos a derivada do P, a componente horizontal, na direção y. Neste campo, a ponta de cima vai para a esquerda: menos com menos dá mais, e o braço gira no anti-horário, a um radiano por segundo.

### B2-4 · tela: a cruz dos dois braços pelo fluxo exato: abre e fecha como tesoura; rótulos violeta `2 rad/s` e `1 rad/s`; a rodinha rígida aparece por cima e gira a `3/2 rad/s`
[curious] Só que os dois braços não precisam girar juntos. O horizontal gira a dois radianos por segundo, e o vertical, a um só: a cruz abre e fecha como uma tesoura! E uma rodinha de pás não vira tesoura: aqui ela é uma sonda ideal, bem pequena e rígida, que só mede o giro. Então ela gira na média dos dois braços: um radiano e meio por segundo.

### B2-5 · tela: CANETA `\operatorname{rot}\vec F = \left(\dfrac{\partial Q}{\partial x} - \dfrac{\partial P}{\partial y}\right)\vec k` e embaixo `= 2\,\omega\,\vec k`; ao lado da rodinha, `\odot` com `\vec k` e o arco ↺; no campo: `2 - (-1) = 3`
[thoughtful, emphatic] E é daí que nasce o rotacional. Ele é a soma dessas duas velocidades angulares: a derivada da componente vertical na horizontal, menos a derivada da componente horizontal na vertical. Ou seja, o dobro da velocidade angular da rodinha. No plano, ele é um vetor perpendicular à folha: apontando para fora dela, o giro é anti-horário; para dentro, horário. Neste campo, ele vale três, e a rodinha gira a três meios.

### B2-6 · tela: volta o painel esquerdo do hook com a rodinha; CANETA `\vec F = (-y,\ x)`, `\dfrac{\partial Q}{\partial x} = 1`, `\dfrac{\partial P}{\partial y} = -1`, `\operatorname{rot}\vec F = 2\,\vec k`, `\omega = 1`; a rodinha completa um giro junto com uma volta
[thoughtful] Agora testa no primeiro redemoinho do começo, o campo que troca as coordenadas de lugar e põe um sinal de menos na primeira. Aqui, o P é menos y, e o Q é x. Então a derivada de Q em x dá um, e a de P em y dá menos um. Um menos menos um: o rotacional vale dois, em todo ponto. A rodinha gira a um radiano por segundo, exatamente o ritmo com que ela dá a volta no centro. Por isso ela completa um giro a cada volta. Na física, o rotacional da velocidade de um fluido tem nome, vorticidade, e para qualquer coisa girando como um corpo rígido ele vale o dobro da velocidade angular. Metade do mistério está resolvida!

## B3 · DOIS ENGANOS

### B3-1 · tela: vórtice grande; cruz coral no ponto (1, 0), braço radial e braço tangencial; pelo fluxo exato o radial tomba no horário (a ponta de dentro adiantada) e o tangencial gira no anti-horário; rodinha rígida por cima, parada
[curious] E o segundo redemoinho? É o mesmo campo de giro, só que dividido pelo quadrado da distância até o centro. Repara no que isso faz com os vizinhos. Pega o braço que aponta para fora: a ponta de dentro está mais perto do centro, onde tudo dá a volta mais rápido, e a ponta de fora vai ficando para trás. Então esse braço tomba no sentido horário.

### B3-2 · tela: CANETA, uma embaixo da outra, `\dfrac{\partial Q}{\partial x} = \dfrac{y^2 - x^2}{(x^2+y^2)^2}` e `\dfrac{\partial P}{\partial y} = \dfrac{y^2 - x^2}{(x^2+y^2)^2}` (os numeradores piscam juntos); `\operatorname{rot}\vec F = \vec 0` em `\Omega = \mathbb{R}^2 - \{(0,0)\}`; o furo pulsa
[thoughtful] Já o braço que acompanha a circunferência é levado pela própria curva e gira no sentido anti-horário. E os dois giram exatamente na mesma rapidez, em sentidos opostos. Fazendo as derivadas, as duas parcelas do rotacional dão a mesma expressão… e a diferença é zero. Em todo ponto, menos na origem, que nem faz parte do domínio.

### B3-3 · tela: os dois painéis do hook; na circunferência as setas iguais; logo fora dela, a seta de fora maior à esquerda e menor à direita (destaque coral nas duas); CANETA `\vec F\ \text{irrotacional} \iff \operatorname{rot}\vec F = \vec 0` (sem caixa)
[thoughtful, emphatic] Então essa é a resposta da pergunta do começo. Na circunferência, os dois campos eram iguais seta por seta, mas o rotacional não olha só a seta do ponto: ele olha como as setas mudam em volta dele. No primeiro redemoinho, a seta de fora é mais forte; no segundo, ela é mais fraca, na medida exata para o giro desaparecer. Um campo assim, com rotacional zero em todo o domínio, se chama irrotacional. Trajetória curva não quer dizer giro.

### B3-4 · tela: os dois painéis se fundem num só: miolo r < 1 com o giro rígido, fora com o vórtice, colados na circunferência; rodinha no miolo girando, rodinha fora só passeando; rótulo `MODELO DE TORNADO`
[excited] E olha que bonito: cola os dois redemoinhos nessa circunferência, o primeiro por dentro e o segundo por fora. Encaixa certinho, porque ali as setas são iguais. Esse é o modelo clássico de um tornado: o miolo gira como um corpo rígido, e em volta dele o ar dá voltas sem girar. Uma rodinha no miolo gira; fora dele, só passeia.

### B3-5 · tela: o rio: faixa |y| < 3, margens em chapa escura, setas para a direita mais longas no meio, perfil parabólico na margem esquerda; tinta em faixas verticais se curvando em parábola; pontinhos andando em linha reta
[curious] E o contrário também engana. Olha um rio: a água anda em linha reta, para a direita, mais rápida no meio e mais devagar perto das margens. Nenhuma partícula faz curva. Agora espalha rodinhas presas em eixos pelo rio inteiro.

### B3-6 · tela: 5 × 3 rodinhas presas girando a y/9; mapa violeta do rotacional com `+` em cima e `−` embaixo, y = 0 tracejado; CANETA `\vec F = \left(1 - \dfrac{y^2}{9},\ 0\right)` e `\operatorname{rot}\vec F = \dfrac{2y}{9}\,\vec k`
[thoughtful] Na metade de cima, a pá de baixo de cada rodinha está mais perto do meio, onde a água corre mais, e é empurrada mais forte: a rodinha gira no sentido anti-horário. Na metade de baixo, é o contrário, e ela gira no horário. E bem no meio, onde as pás de cima e de baixo são empurradas igual, ela fica parada. A conta confirma: o rotacional é proporcional à altura, positivo em cima, zero no meio e negativo embaixo. Trajetória reta, e mesmo assim tem giro! É por isso que um galho boiando perto da margem vai girando enquanto desce o rio.

## B4 · DIVERGENTE

### B4-1 · tela: campo (x, y); quadradinho coral pelo fluxo exato, crescendo; contador `ÁREA` subindo
[thoughtful] Agora a segunda medida. Volta para o quadradinho de fluido e olha o campo que aponta para fora, a explosão de setas. Aqui o quadradinho não gira: ele cresce. Os lados vão sendo esticados, e a área aumenta.

### B4-2 · tela: CANETA `\operatorname{div}\vec F = \dfrac{\partial P}{\partial x} + \dfrac{\partial Q}{\partial y}`; rótulo `É UM NÚMERO`; na explosão, `1 + 1 = 2`
[thoughtful] O divergente mede exatamente isso. A definição é a soma de duas derivadas: a do P na direção x, mais a do Q na direção y. E repara: o resultado é um número, não um vetor. Esse número é a taxa com que a área de um pedacinho de fluido muda, por unidade de área. Positivo, ele se expande; negativo, se contrai; zero, a área se conserva. Na explosão, o divergente vale dois em todo ponto.

### B4-3 · tela: o quadradinho some; entra uma caixa GEO parada; setas atravessam as quatro paredes; placa `SAI − ENTRA`
[curious] Mas por que a área muda? Para enxergar, troca o quadradinho que anda por uma caixa parada, desenhada no chão. O fluido passa por ela. E a pergunta vira: a cada segundo, sai mais fluido do que entra?

### B4-4 · tela: paredes direita e esquerda acendem (só a componente horizontal); CANETA linha 1 `[P(x_0 + h) - P(x_0)]\,k \approx \dfrac{\partial P}{\partial x}\,hk`; paredes de cima e de baixo; linha 2 `[Q(y_0 + k) - Q(y_0)]\,h \approx \dfrac{\partial Q}{\partial y}\,hk`; linha 3 `\dfrac{\text{saldo}}{hk} \to \dfrac{\partial P}{\partial x} + \dfrac{\partial Q}{\partial y} = \operatorname{div}\vec F`
[thoughtful] Pela parede da direita, o fluido sai com a componente horizontal do campo naquela parede; pela da esquerda, entra com a componente horizontal de lá. A diferença, vezes a altura da parede, é o saldo na horizontal. E, de novo, diferença entre vizinhos dividida pela distância vira derivada: o saldo horizontal é a derivada da componente horizontal na horizontal, vezes a área da caixa. Em cima e embaixo, a mesma coisa com a componente vertical. Somando e dividindo pela área, sobra… o divergente. Ou seja, a fórmula não caiu do céu: ela é o saldo do que sai, por unidade de área.

### B4-5 · tela: campo `\vec F = \left(x - \tfrac{x^3}{3},\ y - \tfrac{y^3}{3}\right)`; caixa de lado 1 centrada em (1, ½); placa `0{,}583`; a caixa encolhe em três passos com a lupa: `0{,}708`, `0{,}740`, `0{,}747`; por fim `\operatorname{div}\vec F = 2 - x^2 - y^2` e `\operatorname{div}\vec F(1, \tfrac12) = 0{,}750`
[excited] Vamos testar num campo de verdade. Nesse aqui, o fluido se espalha perto do centro e se comprime longe dele. Coloca a caixa num ponto e calcula o saldo por unidade de área. Agora encolhe a caixa pela metade. E de novo. E de novo! Os números vão chegando em três quartos. E três quartos é exatamente o divergente nesse ponto. O divergente é o que sobra desse saldo quando a caixa encolhe até virar o ponto.

### B4-6 · tela: mapa do divergente: disco de luz r < √2 com `+`, anel de sombra com `−`, círculo tracejado com `\operatorname{div} = 0`; um quadradinho coral dentro se expandindo e outro fora se contraindo
[thoughtful] E dá para pintar o plano inteiro com esse número. Dentro de um disco, o divergente é positivo: ali cada pedacinho de fluido se expande. Fora dele, é negativo: ali cada pedacinho se contrai. Na fronteira, um círculo inteiro de divergente zero. E repara que ninguém está criando nem destruindo fluido: o divergente mede o quanto ele se espalha ou se aperta. A água, por exemplo, quase não muda de volume, então num escoamento de água o divergente da velocidade é praticamente zero. Já o ar sendo comprimido numa bomba de bicicleta tem divergente negativo.

## B5 · A FALSA FONTE

### B5-1 · tela: campo `\vec F = \dfrac{(x,\ y)}{x^2 + y^2}` com o furo; setas para fora, mais curtas longe
[curious] Só que o divergente também engana quem olha de longe. Olha esse campo: todas as setas apontam para fora, como uma fonte. Ele é a explosão dividida pelo quadrado da distância, então as setas enfraquecem conforme se afastam.

### B5-2 · tela: setor coral pelo fluxo exato, mais largo e mais fino, contador `ÁREA` parado; depois a caixa [1, 2] × [−½, ½] com `ENTRA 0{,}927` e `SAI 0{,}490 + 0{,}219 + 0{,}219 = 0{,}927`; CANETA `\operatorname{div}\vec F = 0` em `\Omega`
[thoughtful] Solta um pedacinho de fluido. Ele se alarga para os lados, porque as setas se abrem em leque… mas fica mais fino na direção de fora, porque a frente anda mais devagar que a traseira. E as duas coisas se compensam exatamente: a área não muda. As derivadas dizem o mesmo: as duas parcelas do divergente se cancelam. Coloca uma caixa parada: o que entra é exatamente o que sai. O divergente é zero em todo ponto do domínio.

### B5-3 · tela: lado a lado, a explosão com `\operatorname{div} = 2` e a falsa fonte com `\operatorname{div} = 0`, as duas com setas para fora
[thoughtful, emphatic] Então setas apontando para fora não quer dizer fonte. O divergente mede o saldo em cada pedacinho, e aqui, em cada pedacinho, o saldo é zero: as setas enfraquecem na medida exata em que se espalham.

## B6 · NO ESPAÇO

### B6-0 · tela: (handoff v4 §3.3) EM QUALQUER DIMENSÃO: Ω ⊂ ℝⁿ aberto, F = (F₁, …, Fₙ); div F = ∂F₁/∂x₁ + ⋯ + ∂Fₙ/∂xₙ; painéis n = 2 e n = 3; DIVERGENTE: VALE EM QUALQUER n; ROTACIONAL: CAMPO NO ESPAÇO
[thoughtful] E repara numa coisa: a definição do divergente não depende da dimensão. Um campo numa região aberta de ℝⁿ tem n componentes, de F um até F n, e o divergente é a soma das derivadas de cada componente na sua própria direção. No plano, as duas componentes são o P e o Q; no espaço, chega o R. Já o rotacional é coisa do espaço: o do plano é só o caso em que o R é zero e nada depende de z.

### B6-1 · tela: Three.js `cubo_saldo`; Manim `\operatorname{div}\vec F = \dfrac{\partial P}{\partial x} + \dfrac{\partial Q}{\partial y} + \dfrac{\partial R}{\partial z}`
[thoughtful] No espaço, o divergente tem três parcelas, a terceira é a derivada do R na direção z, e a caixa vira um cubo, com seis paredes. O raciocínio é o mesmo: o saldo do que sai, agora por unidade de volume. E continua sendo um número.

### B6-2 · tela: Three.js `rodinha_eixo`: eixo da rodinha alinhado com o giro, rápida; inclinando, mais devagar; deitada, parada
[curious] Já o rotacional fica ainda mais interessante. No espaço, a rodinha pode ter o eixo apontando para qualquer lado. Olha um fluido girando como um corpo rígido, em torno de um eixo inclinado. Com o eixo da rodinha alinhado com o eixo do giro, ela gira o mais rápido possível. Inclina a rodinha, e ela gira mais devagar. Deita a rodinha de lado, e ela para.

### B6-3 · tela: a rodinha volta ao eixo do giro; a seta violeta do rot acende ao longo dele; à direita, CANETA o determinante `\operatorname{rot}\vec F = \begin{vmatrix} \vec i & \vec j & \vec k \\ \partial_x & \partial_y & \partial_z \\ P & Q & R \end{vmatrix}`, depois `= \nabla \times \vec F` com `\nabla \wedge \vec F` menor ao lado, e `\operatorname{div}\vec F = \nabla \cdot \vec F`
[thoughtful, emphatic] Então, no espaço, o rotacional é um vetor de verdade: a direção dele é o eixo em que a rodinha gira mais rápido, e o tamanho é o dobro dessa rapidez. Cada componente é o rotacional de um dos planos coordenados, e as três se organizam num determinante simbólico, com as derivadas parciais numa linha e as componentes do campo na outra. Abrindo o determinante, a terceira componente é exatamente a do plano: derivada de Q em x, menos derivada de P em y. Por isso o rotacional também aparece escrito como um produto vetorial do nabla com o campo, e o divergente, como um produto escalar.

## F · NA FÍSICA

### F1 · tela: volta a falsa fonte; no furo entra o corte do fio carregado (disco azul com `+`); CANETA `\nabla \cdot \vec E = \dfrac{\rho}{\varepsilon_0}`; o furo acende com o rótulo `A CARGA ESTÁ AQUI`
[excited] E agora vem a parte que eu mais gosto: esses campos estranhos estão espalhados pela física inteira. Lembra da falsa fonte? Ela tem exatamente o formato do campo elétrico em volta de um fio comprido carregado, visto de frente. É a nossa falsa fonte, multiplicada por uma constante. E o furo na origem… é o próprio fio! A lei de Gauss, na forma local, diz que o divergente do campo elétrico é a densidade de carga dividida por uma constante. Fora do fio não tem carga, e o divergente dá zero, igualzinho à nossa conta. A carga mora toda no furo.

### F2 · tela: volta o vórtice; no furo entra o corte do fio com corrente (disco verde com `\odot`); as setas passam de ciano para magenta; CANETA `\nabla \times \vec B = \mu_0 \vec J` e, embaixo, `\nabla \cdot \vec B = 0`
[curious] E o vórtice? É o formato do campo magnético em volta de um fio com corrente. De novo, o nosso vórtice vezes uma constante. Em situações que não mudam com o tempo, o rotacional do campo magnético é proporcional à densidade de corrente. Fora do fio não passa corrente, e o rotacional dá zero, como a gente calculou: a corrente está toda no furo. E tem mais: o divergente do campo magnético é zero sempre, em todo lugar. Até hoje, ninguém encontrou um polo magnético isolado.

## B7 · LAPLACIANO

### B7-1 · tela: φ = x² + y² como chapa azul-claro com curvas de nível; o gradiente acende em ciano (explosão); CANETA `\nabla^2\varphi = \nabla \cdot \nabla\varphi`
[curious] E tem mais uma combinação que vale a pena conhecer desde já. Pega uma função que dá um número em cada ponto, como uma temperatura, e calcula o gradiente dela: um campo de setas apontando para onde ela cresce mais rápido. Agora tira o divergente desse campo. O resultado se chama laplaciano: o divergente do gradiente, o nabla aplicado duas vezes.

### B7-2 · tela: CANETA `\varphi = x^2 + y^2`, `\nabla\varphi = (2x,\ 2y)`, `\nabla^2\varphi = 2 + 2 = 4`; depois `\varphi = x^2 + y^2 + z^2 \ \Rightarrow\ \nabla^2\varphi = 6`
[thoughtful] Por exemplo, a soma dos quadrados das coordenadas no plano. O gradiente dela é uma explosão de setas, o dobro do vetor posição, e o divergente dessa explosão dá quatro. No espaço, somando também o quadrado da altura, dá seis.

### B7-3 · tela: ponto (1, ½) com uma circunferência pequena em volta; oito pontinhos nela acendem; barras `VALOR NO PONTO` (1,25) e `MÉDIA EM VOLTA` (1,41), com `+`
[thoughtful, emphatic] E o que esse número diz? Ele compara o valor da função num ponto com a média dos vizinhos em volta. Laplaciano positivo: o ponto está abaixo da média ao redor. Negativo: está acima. Zero: ele é exatamente a média dos vizinhos.

### B7-4 · tela: (handoff v3 §3.4) gráfico de corte com o vale e a chapa vista de cima alinhada; P, vizinhos, SOBE; o vale se enche
[curious] Agora olha uma chapa de metal com uma mancha fria no meio. No corte da chapa, a temperatura faz um vale. No fundo do vale, o ponto está abaixo da média dos vizinhos: o laplaciano é positivo, e esse ponto esquenta. O vale vai se enchendo. É assim que o laplaciano entra na equação do calor, e ele volta nas ondas, no potencial elétrico e em boa parte da física. Mas isso fica para mais à frente.

## S · RESUMO

### S1 · tela: tela limpa; à esquerda a rodinha com `\operatorname{rot}\vec F = \left(\dfrac{\partial Q}{\partial x} - \dfrac{\partial P}{\partial y}\right)\vec k = 2\omega\,\vec k`; à direita a caixa com `\operatorname{div}\vec F = \dfrac{\partial P}{\partial x} + \dfrac{\partial Q}{\partial y}`
[calm, satisfied] Então, a pergunta do começo está respondida. As duas rodinhas passavam pelas mesmas setas, mas giro não é coisa de uma seta só: é coisa de como as setas mudam em volta do ponto. O rotacional mede isso com duas derivadas, e vale o dobro da velocidade angular de uma rodinha de pás. O divergente mede, com outras duas, o saldo do que sai de uma caixinha, por unidade de área. Duas medidas locais, feitas num ponto só.

### S2 · tela: vórtice e falsa fonte em miniatura lado a lado, com os fios nos furos; rodinhas paradas e caixinhas com `0` em vários pontos; um laço GEO em volta do furo do vórtice com setas de circulação acendendo sempre no mesmo sentido; uma cerca GEO em volta do furo da falsa fonte com todas as setas saindo; um laço longe do furo, apagado
[curious] Mas repara no que sobrou. No vórtice, nenhum ponto gira. Só que, se você der uma volta em torno do furo, o campo empurra o tempo todo no mesmo sentido: essa volta não tem saldo zero. Na falsa fonte, nenhum pedacinho se expande. Só que, se você cercar o furo, tudo atravessa a cerca para fora. Longe do furo, qualquer volta e qualquer cerca dão saldo zero. Em cada ponto, nada; em volta do fio, alguma coisa.

### S3 · tela: (handoff v3 §3.5) DO LOCAL AO GLOBAL; os dois painéis; STOKES e GAUSS embaixo de cada um; GREEN no pé
[thoughtful] E aí está a grande pergunta: como ligar o que acontece em cada ponto com o que acontece numa região inteira? Essa ponte entre o local e o global tem nome. A volta em torno do fio é assunto do teorema de Stokes; a cerca, do teorema de Gauss; e, no plano, os dois viram um só: o teorema de Green. Eles chegam mais à frente no Cálculo três.

### S4 · tela: (handoff v3 §3.6) A TERCEIRA COISA: (x, −y), o quadradinho deforma; rot = 0 e div = 0; desafio; CTA
[curious] E a terceira coisa lá do começo? Olha este campo: o x com o menos y. Faz a conta: o rotacional dá zero, e o divergente também, em todo ponto. Nenhuma rodinha gira, nenhum pedacinho muda de área… e mesmo assim o quadradinho estica para um lado e achata para o outro. Isso é a deformação. Desafio para os comentários: acha outro campo assim, que não seja constante, com rotacional zero e divergente zero. [excited] No próximo vídeo, a gente junta todas as derivadas parciais de um campo, e é delas que sai a medida dessa deformação. Se essa aula te ajudou, deixa o like e se inscreve no Parallax Lab. Até a próxima!
