# yt_0020 — narração v1.1 (Anexo A do handoff v1, 2026-11-02; congelada, aprovada pelo Kaio para o preview)

Título: Cinemática angular: por que a ponta da hélice chega a quase 1.000 km/h? Cada `###` é uma âncora; a linha do cabeçalho diz a tela, o resto é a fala.
Tags `[ ]` do ElevenLabs v4 não entram na contagem nem na legenda.

## HOOK

### H1 — tela: hélice Three.js girando, dois marcadores (10 cm e ponta), setas violeta curta e enorme
[curious] Olha essa hélice. Ela gira inteira junto: as pás são de metal rígido, nenhum pedaço fica para trás. Então dá vontade de dizer que todo ponto dela tem a mesma velocidade. Só que não tem.

### H2 — tela: 2.700 RPM, DIÂMETRO 1,9 m, ≈ 100 km/h, ≈ 970 km/h, barra da velocidade do som em 78%, selo NÚMEROS TÍPICOS
[thoughtful] Com números típicos de um avião pequeno, quase dois metros de diâmetro e duas mil e setecentas rotações por minuto, um ponto a dez centímetros do eixo anda a uns cem quilômetros por hora. Já a ponta da pá passa dos novecentos e sessenta: quase mil quilômetros por hora, perto de oitenta por cento da velocidade do som.

### H3 — tela: pergunta POR QUE A PONTA DA HÉLICE CHEGA A QUASE 1.000 km/h?; as duas setas piscam
[curious] E aí fica a pergunta. Se a hélice inteira gira no mesmo ritmo, por que cada pedaço dela anda numa velocidade diferente? E que número é esse, o ritmo da hélice, que vale para ela toda?

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: título e NESTE VÍDEO com três ícones
[thoughtful] Hoje a gente começa a rotação de corpos rígidos, pela cinemática angular: como descrever o giro de um corpo, sem se preocupar ainda com o que causa esse giro. Primeiro, como medir um giro com um ângulo. Depois, quão rápido e quão acelerado ele é. E por fim, como o giro do corpo inteiro vira a velocidade e a aceleração de cada ponto. No final, três exercícios para firmar tudo.

### A3 — tela: partícula num círculo, a_c = v²/r; muitas partículas viram o disco de referência
[thoughtful] Você já conhece o movimento circular de uma partícula só: ela anda num círculo, e tem uma aceleração apontando para o centro, a velocidade ao quadrado dividida pelo raio. A novidade agora é que o corpo inteiro gira, com infinitos pontos, cada um no seu círculo. E a gente quer um jeito de descrever todos eles de uma vez.

## T1 — COMO MEDIR UM GIRO?

### T1-1 — tela: disco de referência; CORPO RÍGIDO: DISTÂNCIAS FIXAS; EIXO FIXO; régua tracejada que não muda
[thoughtful] Vamos começar com um disco, girando em torno de um eixo que não se mexe. Primeiro, a hipótese que dá nome a tudo: corpo rígido. Quer dizer que a distância entre quaisquer dois pontos do corpo não muda. O disco não estica, não entorta, não amassa.

### T1-2 — tela: círculos dos três pontos; a linha pintada varre θ a partir da referência
[thoughtful] Repara no que acontece quando ele gira. Cada ponto anda num círculo centrado no eixo. E todos os pontos, juntos, giram do mesmo ângulo. Então, para saber onde está o disco inteiro, basta um número só: o ângulo entre essa linha pintada no disco e uma linha fixa de referência. Na tela ele aparece como teta, e daqui para a frente é só "o ângulo". [short pause] Um corpo rígido girando em torno de um eixo fixo tem um grau de liberdade só. Um número descreve o corpo todo.

### T1-3 — tela: três arcos s; θ = s/r; uma volta: s = 2πr → 1 VOLTA = 2π rad
[thoughtful] Agora, como medir esse ângulo? Em física, a gente mede em radianos. A ideia é simples: pega o comprimento do arco que um ponto percorreu e divide pela distância dele ao eixo. Olha os três pontos: para o mesmo giro, o de fora percorre um arco maior, mas também está mais longe. A divisão dá o mesmo número para os três. Esse número é o ângulo em radianos. E uma volta inteira é a circunferência dividida pelo raio: dois pi radianos.

### T1-4 — tela: s = r θ (θ EM rad); EM GRAUS: π/180 SOBRA; DICA
[thoughtful] E repara que o radiano é uma divisão de comprimento por comprimento: ele não tem dimensão de verdade. Por isso a relação "arco igual à distância ao eixo vezes o ângulo" fica limpa assim. Se você medir em graus, aparece um pi sobre cento e oitenta em toda fórmula daqui para a frente. É por isso que toda a rotação se escreve em radianos.

### T1-5 — tela: sinais; três voltas; mostrador 0°–360° e Δθ acumulado 2π, 4π, 6π
[curious] Mais dois combinados. O sentido: anti-horário é positivo, horário é negativo. E uma sutileza que vai importar lá no exercício do ventilador: o ângulo que a gente usa não volta a zero a cada volta. Se o disco deu três voltas, o deslocamento angular é seis pi radianos, não zero. O mostrador de zero a trezentos e sessenta graus diz onde a linha está. O ângulo acumulado diz quanto o disco girou.

## T2 — QUÃO RÁPIDO GIRA?

### T2-1 — tela: estroboscopia com Δt iguais; ω_méd = Δθ/Δt
[thoughtful] Agora, quão rápido gira? A ideia é a mesma da velocidade em uma dimensão, só que com ângulo no lugar de posição. A velocidade angular média é o deslocamento angular dividido pelo intervalo de tempo.

### T2-2 — tela: Δt encolhe; ω = dθ/dt; rad/s; seta curva ω
[thoughtful] E fazendo o intervalo de tempo ir a zero, vem a velocidade angular instantânea, que na tela aparece como ômega: a derivada do ângulo em relação ao tempo. A unidade é radiano por segundo. E pelo sinal do ângulo, velocidade angular positiva é giro anti-horário; negativa, horário.

### T2-3 — tela: mesmo Δθ para os três pontos; MESMO ω PARA O CORPO TODO
[thoughtful, emphatic] E aqui está a primeira ideia central do vídeo. Os três pontos varrem o mesmo ângulo no mesmo tempo. Então todos têm a mesma velocidade angular. A velocidade angular não é de um ponto: é do corpo inteiro. Já a velocidade de cada ponto, a gente vai ver daqui a pouco, depende de onde ele está.

### T2-4 — tela: 1 RPM = 2π rad / 60 s; 2.700 RPM ≈ 282,7 rad/s
[thoughtful] Na prática, motor e ventilador vêm em rotações por minuto. Para passar para radiano por segundo, cada volta vale dois pi radianos, e cada minuto, sessenta segundos. A hélice do começo, com duas mil e setecentas rotações por minuto, gira a uns duzentos e oitenta e três radianos por segundo.

### T2-5 — tela: cronômetro de volta; |ω| = 2πf = 2π/T; ressalvas
[thoughtful] Quando o giro é uniforme, sempre no mesmo ritmo, aparecem mais dois nomes: a frequência, que é o número de voltas por segundo, e o período, que é o tempo de uma volta. O tamanho da velocidade angular é dois pi vezes a frequência, ou dois pi dividido pelo período. Repara nas duas ressalvas. É o tamanho, porque a frequência é sempre positiva, mesmo num giro horário. E só vale com giro uniforme: se o giro acelera, cada volta demora um tempo diferente, e não existe um período só.

## T3 — E QUANDO O GIRO ACELERA?

### T3-1 — tela: α = dω/dt = d²θ/dt²; rad/s²; seta curva verde α
[thoughtful] E se o giro muda de ritmo? Aí entra a aceleração angular: a derivada da velocidade angular em relação ao tempo. Ou, derivando duas vezes, a segunda derivada do ângulo. A unidade é radiano por segundo ao quadrado.

### T3-2 — tela: três discos: GIRANDO MAIS RÁPIDO, FREANDO, TAMBÉM ACELERANDO
[curious] E o sinal aqui engana muita gente. Aceleração angular negativa não quer dizer "freando". Quer dizer só que a velocidade angular está mudando no sentido horário. Se a velocidade angular e a aceleração angular têm o mesmo sinal, o giro fica cada vez mais rápido. Se têm sinais opostos, o giro está freando.

### T3-3 — tela: gráfico ω(t) reta; inclinação α; ω = ω₀ + α t
[thoughtful] Agora o caso mais importante: aceleração angular constante. Se a taxa de variação é constante, a velocidade angular cresce como uma reta no tempo: velocidade angular igual à velocidade angular inicial, mais a aceleração angular vezes o tempo. A inclinação dessa reta é a própria aceleração angular.

### T3-4 — tela: tirinhas ω dt pintam a área; retângulo e triângulo; Δθ = ω₀ t + ½ α t²; inset da área com sinal
[thoughtful, emphatic] E o ângulo? Olha a área embaixo dessa reta. Num intervalo curtinho, o disco gira a velocidade angular vezes esse tempinho, que é uma tirinha fina de área. Somando todas as tirinhas, a área inteira embaixo do gráfico é o ângulo acumulado: a integral da velocidade angular no tempo. E essa área tem duas partes. O retângulo é a velocidade angular inicial vezes o tempo: o giro que o disco daria se não acelerasse. E o triângulo, com base igual ao tempo e altura igual à aceleração angular vezes o tempo, vale meio vezes a aceleração angular vezes o tempo ao quadrado: é o giro a mais que a aceleração deu. [curious] Só um cuidado: essa é uma área com sinal. Se o disco inverter o sentido, a parte abaixo do eixo conta negativo. Um disco que dá uma volta para um lado e uma volta para o outro tem deslocamento angular zero, mas girou quatro pi radianos no total. Então o deslocamento angular não é, necessariamente, o quanto ele girou.

### T3-5 — tela: ω² = ω₀² + 2α Δθ; trapézio Δθ = ½ (ω₀ + ω) t
[thoughtful] Daqui saem mais duas. Se você eliminar o tempo entre as duas equações, chega em: velocidade angular ao quadrado igual à inicial ao quadrado, mais duas vezes a aceleração angular vezes o deslocamento angular. E olhando a mesma área como um trapézio, o deslocamento angular é a média das velocidades angulares, inicial e final, vezes o tempo.

### T3-6 — tela: tabela linear × angular; MESMA MATEMÁTICA
[curious] Repara: são exatamente as equações do movimento uniformemente variado, com o ângulo no lugar da posição, a velocidade angular no lugar da velocidade e a aceleração angular no lugar da aceleração. E não é coincidência: é a mesma matemática, uma coordenada só, derivada duas vezes. Então a física nova não está aqui. Ela está na hora de passar do giro do corpo para o movimento de cada ponto.

## T4 — E CADA PONTO DO CORPO?

### T4-1 — tela: s = r θ → v_t = r ω; |v| = r |ω|; seta tangente
[thoughtful] Vamos lá. Um ponto a uma certa distância do eixo percorre um arco igual a essa distância vezes o ângulo. Como a distância ao eixo não muda, porque o corpo é rígido, é só derivar dos dois lados: a velocidade do ponto ao longo do círculo é a distância ao eixo vezes a velocidade angular. Ela tem sinal, como a velocidade angular: positiva no sentido anti-horário. E a rapidez, o tamanho da velocidade, é a distância ao eixo vezes o tamanho da velocidade angular. Sempre tangente ao círculo do ponto.

### T4-2 — tela: setas proporcionais ao raio; a hélice volta: 282,7 rad/s; 28 m/s; 269 m/s; EM RELAÇÃO AO EIXO
[excited] E o hook está respondido! A hélice inteira tem uma velocidade angular só, uns duzentos e oitenta e três radianos por segundo. Mas cada ponto multiplica esse número pela sua distância ao eixo. A dez centímetros, isso dá vinte e oito metros por segundo, uns cem quilômetros por hora. Na ponta, a noventa e cinco centímetros, dá duzentos e sessenta e nove metros por segundo: quase mil quilômetros por hora. O cubo não gira mais devagar: ele gira junto, só que está perto do eixo. E essa rapidez na ponta é um dos fatores que limitam o projeto de uma hélice. Ela é medida em relação ao eixo; em relação ao ar, ainda soma a velocidade do próprio avião. Perto da velocidade do som, os efeitos de compressão do ar aumentam o barulho e prejudicam a eficiência.

### T4-3 — tela: dois pontos opostos; MESMA RAPIDEZ · VELOCIDADES OPOSTAS
[curious] Agora, um cuidado. Olha esses dois pontos, em lados opostos do disco, à mesma distância do eixo. O tamanho da velocidade é o mesmo. Mas as setas apontam em sentidos contrários. Mesma rapidez, velocidades diferentes. A fórmula que a gente acabou de ver dá o tamanho; a direção completa, no espaço, a gente vai pegar daqui a pouco com um vetor.

### T4-4 — tela: seta verde a_t; v = r ω → a_t = r α
[thoughtful] Derivando mais uma vez: se o giro acelera, a velocidade do ponto muda de tamanho. Essa é a aceleração tangencial: a distância ao eixo vezes a aceleração angular. Ela aponta ao longo da tangente, junto com a velocidade quando o giro acelera, contra ela quando freia.

### T4-5 — tela: a_c para o eixo; a_c = v²/r = (rω)²/r = ω² r
[thoughtful, emphatic] Só que tem outra. Mesmo girando num ritmo constante, sem aceleração angular nenhuma, o ponto está acelerado, porque a direção da velocidade muda o tempo todo. É a aceleração centrípeta, que você já conhece: velocidade ao quadrado dividida pela distância ao eixo. Trocando a velocidade pela distância vezes a velocidade angular, fica: velocidade angular ao quadrado vezes a distância ao eixo. E ela aponta sempre para o eixo.

### T4-6 — tela: soma das acelerações; φ; a = √(a_t² + a_c²); tan φ; hélice a_c ≈ 7.750 g
[thoughtful] Então cada ponto tem duas acelerações perpendiculares: a tangencial, que muda o tamanho da velocidade, e a centrípeta, que muda a direção. A aceleração total é a soma das duas. O tamanho vem do Pitágoras. E o ângulo dela, medido a partir da direção que aponta para o eixo, tem tangente igual ao tamanho da tangencial dividido pela centrípeta. Para que lado ela se inclina, quem diz é o sinal da tangencial: para a frente se o giro acelera, para trás se freia. Repara também que a centrípeta cresce com o quadrado da velocidade angular. Na ponta da hélice, dá uns setenta e seis mil metros por segundo ao quadrado: perto de sete mil e setecentas vezes a aceleração da gravidade.

## T5 — PARA ONDE APONTA UM GIRO?

### T5-1 — tela: disco 3D; ATÉ AQUI: UM EIXO FIXO · UM ÂNGULO COM SINAL; pião e Terra
[curious] Até agora, todo giro acontecia em torno de um eixo fixo. Nesse caso, bastava um ângulo com sinal: mais para anti-horário, menos para horário. Mas e quando o corpo pode girar em torno de eixos diferentes? Pensa num pião, num satélite, na própria Terra. Aí a gente precisa dizer também em torno de qual eixo. E a pergunta natural é: dá para juntar tudo numa seta, num vetor?

### T5-2 — tela: dois livros, eixos fixos no laboratório, as duas ordens; capas terminam diferentes
[thoughtful] Vamos testar com um livro. Os dois eixos ficam parados no laboratório: eles não giram junto com o livro. Na esquerda, primeiro a gente gira noventa graus em torno deste eixo, e depois noventa graus em torno deste outro. Na direita, os mesmos dois giros, só que na ordem contrária. [short pause] Olha como eles terminam: a capa de um aponta para um lado, a do outro, para outro lado. A ordem mudou o resultado.

### T5-3 — tela: vetores comutam (3 m leste + 4 m norte); giros finitos não
[thoughtful, emphatic] E isso é sério. Vetor de verdade se soma em qualquer ordem: andar três metros para leste e depois quatro para norte leva ao mesmo lugar que fazer o contrário. Até dá para descrever um giro de noventa graus com uma seta, apontando o eixo, com tamanho igual ao ângulo. Mas juntar dois giros não é somar essas setas: o resultado depende da ordem, e soma de vetor não depende. Então giros finitos não se somam como vetores.

### T5-4 — tela: 10°, 5°, 1°; medidor DIFERENÇA ENTRE AS ORDENS; dθ⃗ comutam
[thoughtful] Só que agora repete com giros pequenos. Com dez graus, a diferença entre as duas ordens já é bem menor. Com um grau, quase some. Na verdade, ela diminui com o produto dos dois ângulos: se os dois giros caem pela metade, a diferença cai para um quarto. Para giros infinitesimais, ela some de vez, e os giros pequenininhos se somam como vetores, em qualquer ordem.

### T5-5 — tela: disco 3D com ω⃗; mão direita; ω⃗ = dθ⃗/dt
[thoughtful] E é por isso que a velocidade angular pode ser um vetor: ela é um giro infinitesimal dividido por um tempo infinitesimal. A seta fica em cima do eixo, com tamanho igual ao tamanho da velocidade angular. Aquele sinal de antes, mais ou menos, vira o sentido da seta ao longo do eixo. E o sentido vem da regra da mão direita: curva os dedos no sentido do giro, e o polegar aponta o vetor.

### T5-6 — tela: v⃗ = ω⃗ × r⃗; paralelogramo; r_⊥; O desliza no eixo
[thoughtful] Com o vetor, a velocidade de cada ponto ganha uma fórmula completa: é o produto vetorial da velocidade angular com o vetor posição do ponto. O produto vetorial de dois vetores dá um terceiro, perpendicular aos dois, com tamanho igual à área desse paralelogramo: o tamanho de um, vezes o tamanho do outro, vezes o seno do ângulo entre eles. E repara: o tamanho do vetor posição vezes esse seno é exatamente a distância do ponto ao eixo. Por isso o vetor posição pode começar em qualquer ponto do eixo. A parte dele que fica ao longo do eixo some no produto vetorial. O tamanho volta a ser a velocidade angular vezes a distância ao eixo, e a direção sai sozinha, tangente ao círculo do ponto.

### T5-7 — tela: dois pontos opostos no disco 3D; v⃗ opostas
[curious] E aquele cuidado dos dois pontos opostos? O produto vetorial resolve sozinho: o vetor posição de um aponta para um lado, o do outro, para o lado oposto, e as velocidades saem opostas.

### T5-8 — tela: α⃗; a⃗ = α⃗ × r⃗ + ω⃗ × (ω⃗ × r⃗); TANGENCIAL e CENTRÍPETA
[thoughtful, emphatic] Por fim, a aceleração angular também vira vetor: a derivada do vetor velocidade angular. Com eixo fixo, ela fica em cima do eixo: no mesmo sentido da velocidade angular quando o giro acelera, no sentido oposto quando freia. E agora dá para juntar tudo numa linha. Derivando a velocidade do ponto, aparecem dois termos. O primeiro é a aceleração angular, em produto vetorial com o vetor posição: é a aceleração tangencial. O segundo é a velocidade angular, em produto vetorial com a velocidade do próprio ponto: ele aponta para o eixo e tem tamanho velocidade angular ao quadrado vezes a distância ao eixo. É a centrípeta. As duas acelerações do disco estavam escondidas em dois produtos vetoriais. E quando o próprio eixo muda de direção, como num pião, a história fica mais rica: aí a aceleração angular nem aponta ao longo do eixo.

## E1 — O VENTILADOR QUE DESLIGA

### E1-1 — tela: ventilador de teto visto de baixo; 300 RPM, PARA EM 30 s, r = 0,60 m; O QUE ESTE PEDE; HIPÓTESES
[thoughtful] Vamos ao primeiro exercício. Um ventilador de teto gira a trezentas rotações por minuto, com pás de sessenta centímetros do eixo até a ponta. Desligado, ele para em trinta segundos, com aceleração angular constante. Quantas voltas ele dá até parar? E como é a aceleração da ponta da pá?

### E1-2 — tela: ω₀ = 10π ≈ 31,4; α = −π/3 ≈ −1,05; SINAIS OPOSTOS ⇒ FREANDO
[thoughtful] Primeiro, tudo em radianos. Trezentas rotações por minuto são cinco voltas por segundo: dez pi radianos por segundo, uns trinta e um vírgula quatro. A aceleração angular é a variação da velocidade angular, de trinta e um vírgula quatro até zero, dividida pelos trinta segundos: menos pi sobre três, uns menos um vírgula zero cinco radiano por segundo ao quadrado. Sinal contrário ao da velocidade angular: está freando, como tinha que ser.

### E1-3 — tela: gráfico ω(t); triângulo âmbar; 150π ≈ 471 rad → 75 voltas; mostrador × acumulado
[thoughtful] Para as voltas, a área embaixo do gráfico da velocidade angular. Aqui ela é um triângulo: metade de dez pi vezes trinta. Dá cento e cinquenta pi radianos, uns quatrocentos e setenta e um. Dividindo por dois pi: setenta e cinco voltas. E repara no mostrador: ele passa pelo zero setenta e cinco vezes, mas o ângulo acumulado nunca voltou atrás.

### E1-4 — tela: 0 a 10 s: ≈ 262 rad ≈ 41,7 voltas; 5/9 DA ÁREA
[curious] E uma curiosidade: quanto ele gira nos primeiros dez segundos, um terço do tempo? Com a equação do ângulo: trinta e um vírgula quatro vezes dez, menos meio vezes um vírgula zero cinco vezes cem. Uns duzentos e sessenta e dois radianos, quase quarenta e duas voltas. Mais da metade das voltas sai no primeiro terço do tempo, porque é quando ele está rápido. No gráfico dá para ver: a faixa do começo é a parte mais alta do triângulo.

### E1-5 — tela: setas na ponta (FORA DE ESCALA); v₀ ≈ 18,8; a_c ≈ 592 ≈ 60 g; a_t ≈ 0,63; em 10 s
[thoughtful] Agora a ponta da pá, no instante em que desliga. A velocidade é zero vírgula sessenta metro vezes trinta e um vírgula quatro: uns dezoito vírgula oito metros por segundo. A aceleração centrípeta é a velocidade angular ao quadrado vezes a distância ao eixo: uns quinhentos e noventa e dois metros por segundo ao quadrado, sessenta vezes a gravidade. E a tangencial, a distância vezes a aceleração angular, dá só zero vírgula sessenta e três. Dez segundos depois, a velocidade angular caiu para uns vinte e um radianos por segundo, e a centrípeta ainda está em duzentos e sessenta e três. A aceleração total quase não sai da direção do eixo: o ângulo dela com o raio é pouco mais de um décimo de grau.

### E1-6 — tela: |a_t| fixo × a_c caindo; ω² < |α| ⟹ t > 29,0 s; CONFERE; DICA
[excited] E quando a aceleração tangencial da freada finalmente fica maior que a centrípeta? Repara: a freada estava agindo desde o começo, com os mesmos zero vírgula sessenta e três o tempo todo. Só que a aceleração que mantém a ponta fazendo a curva era muito maior, e vai encolhendo com a velocidade angular. A distância ao eixo cancela dos dois lados, e sobra: velocidade angular ao quadrado menor que o tamanho da aceleração angular. Isso só acontece quando a velocidade angular cai abaixo de um vírgula zero dois radiano por segundo, depois dos vinte e nove segundos. Só no último segundo a freada passa a mandar na aceleração da ponta! [short pause] [thoughtful] Para conferir as voltas: a velocidade média é metade de cinco voltas por segundo, vezes trinta segundos, setenta e cinco. Bate.

## E2 — A CORRENTE DA BICICLETA

### E2-1 — tela: transmissão da bicicleta; coroa 10 cm, catraca 4 cm, roda 35 cm; 60 RPM; O QUE ESTE PEDE; HIPÓTESES
[thoughtful] Segundo exercício. Uma bicicleta com a coroa, a engrenagem dos pedais, de dez centímetros de raio; a catraca, a engrenagem pequena da roda traseira, de quatro centímetros; e a roda, de trinta e cinco centímetros. O ciclista pedala a sessenta rotações por minuto. Com que velocidade angular gira a roda?

### E2-2 — tela: CORPO 1 (coroa) e CORPO 2 (catraca + roda); a corrente pisca
[curious] Antes da conta, uma pergunta que pega muita gente. A gente acabou de ver que todos os pontos de um corpo rígido têm a mesma velocidade angular. Então por que a coroa e a catraca giram diferente? Porque são corpos diferentes, ligados pela corrente. Já a catraca e a roda, enquanto você pedala, giram presas uma na outra: na prática, são um corpo só, com a mesma velocidade angular.

### E2-3 — tela: elo com v_c nas duas bordas; ω₂ = 2,5 ω₁ = 5π ≈ 15,7; 5,50 m/s ≈ 19,8 km/h
[thoughtful] E o que a corrente faz? Ela não estica e não escorrega, então todos os elos andam com a mesma velocidade. Na coroa, essa velocidade é a velocidade angular da coroa vezes o raio da coroa. Na catraca, a da catraca vezes o raio da catraca. Igualando, a catraca gira dez quartos, duas vezes e meia mais rápido que a coroa. Sessenta rotações por minuto são dois pi radianos por segundo, então a roda gira a cinco pi, uns quinze vírgula sete. E a borda do pneu anda quinze vírgula sete vezes zero vírgula trinta e cinco: cinco e meio metros por segundo em relação ao eixo, quase vinte quilômetros por hora. Se o pneu não escorrega no chão, essa é a velocidade da bicicleta.

### E2-4 — tela: 60 → 90 RPM em 4 s; α₁ ≈ 0,785; α₂ ≈ 1,96; a ≈ 0,69; 5 voltas
[thoughtful] Agora o ciclista acelera a cadência, de sessenta para noventa rotações por minuto, em quatro segundos, de modo uniforme. A aceleração angular da coroa é uma diferença de pi radianos por segundo em quatro segundos: pi sobre quatro, uns zero vírgula setenta e oito. Como a relação da corrente vale a cada instante, a roda acelera duas vezes e meia mais: um vírgula noventa e seis. E, de novo com o pneu sem escorregar no chão, a bicicleta acelera isso vezes trinta e cinco centímetros: zero vírgula sessenta e nove metro por segundo ao quadrado. E nesses quatro segundos o pedal dá exatamente cinco voltas: a média entre uma e uma volta e meia por segundo, vezes quatro.

### E2-5 — tela: elo na coroa e na catraca: 0,63 m/s; a_c 3,9 e 9,9; DICA
[thoughtful, emphatic] E olha um detalhe. Na cadência de sessenta, um elo andando a zero vírgula sessenta e três metro por segundo tem aceleração centrípeta de três vírgula nove na coroa, e de nove vírgula nove na catraca. Mesma velocidade, raio menor: velocidade angular maior e aceleração centrípeta maior. A dica que fica vale para corrente, correia e engrenagem: dentro de um corpo rígido, todo mundo tem a mesma velocidade angular. Entre corpos acoplados sem escorregar, o que se iguala é a velocidade no ponto de contato.

## E3 — QUANTO GIRA A TERRA?

### E3-1 — tela: Sol, Terra inclinada em órbita, estrela distante; FORA DE ESCALA; A TERRA DÁ UMA VOLTA EM 24 h?
[curious] Último exercício, e esse pede cuidado. A Terra dá uma volta em vinte e quatro horas? Depende: uma volta em relação a quê?

### E3-2 — tela: vista de cima da órbita; meridiano; estrela × Sol; arco extra; DIA SIDERAL e DIA SOLAR MÉDIO
[thoughtful] Olha esse esquema, fora de escala. Ao meio-dia solar, o Sol cruza o meridiano do observador, aquela linha imaginária de norte a sul que passa sobre a cabeça dele. Vamos marcar também a direção de uma estrela muito distante, no mesmo meridiano. Depois de uma volta completa em relação às estrelas, a estrela volta ao meridiano. Só que, nesse tempo, a Terra também andou um pouquinho na órbita, no mesmo sentido do giro. Então o Sol ainda não voltou ao meridiano: a Terra precisa girar mais um pouco, quase um grau, para isso acontecer. O dia de vinte e quatro horas é o dia solar médio, a média do tempo de Sol a Sol ao longo do ano. A volta de verdade, em relação às estrelas, é um pouco mais curta: o dia sideral.

### E3-3 — tela: voltas no ano; 1/T_sid = 1/T_sol + 1/T_ano; 86.164 s; ω ≈ 7,292 × 10⁻⁵ rad/s
[thoughtful] Quanto mais curta? Conta as voltas num ano inteiro. Em relação ao Sol, são uns trezentos e sessenta e cinco dias e um quarto. Em relação às estrelas, uma volta a mais, porque a órbita inteira acrescenta um giro. Dividindo tudo pelo tempo de um ano: um sobre o dia sideral é igual a um sobre o dia solar, mais um sobre o ano. Dá oitenta e seis mil, cento e sessenta e quatro segundos: vinte e três horas, cinquenta e seis minutos e quatro segundos. E a velocidade angular da Terra é dois pi dividido por esse tempo: sete vírgula duzentos e noventa e dois vezes dez elevado a menos cinco radiano por segundo.

### E3-4 — tela: Terra geocêntrica; ω⃗; São Paulo; r⃗; r_⊥; λ; v⃗ para leste; HIPÓTESES
[thoughtful] Agora, com que velocidade São Paulo anda por causa desse giro? Usa o produto vetorial: a velocidade é a velocidade angular da Terra, em produto vetorial com o vetor que vai do centro da Terra até São Paulo. Repara: esse vetor sai do centro, que está em cima do eixo, então vale. E o tamanho do produto vetorial é a velocidade angular vezes a distância de São Paulo até o eixo, não até o centro. Essa distância é o raio da Terra vezes o cosseno da latitude.

### E3-5 — tela: r_⊥ ≈ 5.840 km; equador 465 m/s; São Paulo 426 m/s ≈ 1.530 km/h
[thoughtful] Com o raio da Terra de seis mil, trezentos e setenta e um quilômetros e a latitude de São Paulo, vinte e três vírgula cinquenta e cinco graus sul, a distância ao eixo fica uns cinco mil, oitocentos e quarenta quilômetros. No equador, a velocidade seria de quatrocentos e sessenta e cinco metros por segundo. Em São Paulo, quatrocentos e vinte e seis: mais de mil e quinhentos quilômetros por hora, para o leste. E atenção ao referencial: isso é só a parte da rotação, vista do centro da Terra, sem girar com ela. A velocidade em volta do Sol é outra história, e bem maior.

### E3-6 — tela: a_c para o eixo; λ entre a_c e a radial; 0,031 m/s²; CONFERE; DICA
[curious] E a aceleração centrípeta de São Paulo? Velocidade angular ao quadrado vezes a distância ao eixo: uns três centésimos de metro por segundo ao quadrado, três décimos por cento da gravidade. Pequena, mas repara para onde ela aponta: para o eixo da Terra, não para o centro. Ela faz com a direção do centro da Terra um ângulo igual à latitude. E o fio de prumo nem aponta exatamente para o centro: a rotação contribui para essa pequena diferença, assunto do módulo de referenciais não inerciais. [thoughtful] Conferindo: no polo, a distância ao eixo é zero, e a velocidade também; no equador, é máxima. E ficam duas dicas: na rotação, pergunte sempre "em relação a quê?". E a distância que importa é sempre até o eixo.

## SÍNTESE

### S1 — tela: três cartões PANEL; disco girando atrás
[calm, satisfied] Então, resumindo. Um corpo rígido girando em torno de um eixo fixo tem um ângulo, uma velocidade angular e uma aceleração angular para o corpo inteiro, e com aceleração angular constante valem as mesmas equações do movimento uniformemente variado. Cada ponto transforma esse giro em movimento multiplicando pela sua distância ao eixo: a velocidade, a aceleração tangencial e a centrípeta. E, como vetor, a velocidade de cada ponto é a velocidade angular em produto vetorial com a posição dele.

### S2 — tela: a hélice volta; O MESMO ω · DISTÂNCIAS DIFERENTES AO EIXO
[thoughtful] A pergunta inicial está respondida. O corpo inteiro compartilha o mesmo giro, mas cada ponto transforma esse giro em movimento de um jeito diferente. A ponta da hélice não gira mais rápido que o cubo: ela só está mais longe do eixo.

## ENCERRAMENTO

### EN1 — tela: logo com anéis; INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
[happy] Se essa aula ajudou você, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### EN2 — tela: desafio dos ponteiros; relógio estilizado
[curious] E fica um desafio para os comentários: depois do meio-dia, de quanto em quanto tempo os ponteiros das horas e dos minutos se encontram de novo? Dica: pense na velocidade angular de um em relação ao outro. Até a próxima!

## Números de conferência

Ver a tabela "Conferência numérica" do Anexo A (handoff v1) e `qa20.py`, seção NÚMEROS.
