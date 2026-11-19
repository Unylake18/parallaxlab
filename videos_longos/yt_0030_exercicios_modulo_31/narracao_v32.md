# yt_0030 · narração v3.2 (Anexo A do handoff v3) — só para tempo e gatilhos nesta fase; não gerar voz

### H · Gancho

[curious] Três quadradinhos de fluido. Um só entorta. Outro gira, encolhe e entorta, tudo ao mesmo tempo. E, no terceiro campo, um gira sem crescer e o outro cresce sem girar. Embaixo, três fórmulas, fora de ordem. [thoughtful] A pergunta é: dá para saber qual fórmula faz qual filme só olhando para ela, antes de soltar o fluido? Dá. E hoje é você que vai fazer isso. [excited] E depois a gente vai usar exatamente as mesmas contas para responder uma pergunta que parece de outro mundo: por que o campo magnético de um fio enfraquece com um sobre a distância, e o campo de uma carga, com um sobre a distância ao quadrado? Não é decoreba. É o rotacional e o divergente escolhendo a lei.

### A · Bem-vindos

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Esse é o quarto episódio da nossa série de Cálculo três, e hoje é dia de colocar a mão na massa: o integrador do módulo, só com exercícios. [thoughtful] Vai ser uma escada: cada degrau deixa uma peça para o seguinte. Ler uma fórmula de dois jeitos, desenhar um campo, uma família de redemoinhos, duas regras, um campo que não melhora de perto e, no topo, o desafio do episódio passado: prever o quadradinho. [curious] Depois, as aplicações: um rio, um jato numa parede, mapas que não entortam e as leis do um sobre a distância. [happy] Então pega papel e caneta. Toda vez que aparecer um enunciado, pausa o vídeo e tenta antes de ver a resolução.

### D1 · Mesma fórmula, dois filmes

[thoughtful] Primeiro degrau. Uma função que recebe um par de números e devolve outro par: na primeira coordenada, a soma dos dois; na segunda, a diferença. Na tela: fi de u, v igual a u mais v, u menos v. Fi é só o nome da função. Primeiro, como transformação. No plano da esquerda fica o ponto de partida; no da direita, onde ele vai parar. Três itens: a imagem de uma reta, de um quadrado e de um círculo. Pausa o vídeo e tenta.

[curious] Começa por uma reta: o eixo horizontal da esquerda, onde o segundo número é zero. Aí a soma e a diferença ficam iguais ao primeiro número, e as duas coordenadas da direita saem iguais. O eixo vai parar na diagonal.

[thoughtful] Agora o quadrado de lado um. Como essa transformação é linear, ela leva segmento em segmento, então basta transformar os quatro cantos. A origem fica parada. O canto um, zero: a soma dá um mais zero, e a diferença, um menos zero. Ele vai para um, um. O canto um, um vai para dois, zero. E o canto zero, um vai para um, menos um. Liga os pontos: é um quadrado de novo, girado quarenta e cinco graus, com lado raiz de dois, a distância da origem até o ponto um, um. A área era um; agora é raiz de dois ao quadrado: dois. E olha a ordem dos cantos: na esquerda, eles davam a volta no sentido anti-horário; na direita, dão no horário. O quadrado foi espelhado.

[curious] E um círculo em volta da origem? Soma ao quadrado mais diferença ao quadrado. Abre os dois quadrados: num aparece mais duas vezes o produto, no outro, menos duas vezes o produto. Esses termos cruzados se cancelam, e sobra duas vezes a soma dos quadrados. Então a distância até a origem fica multiplicada por raiz de dois, e o círculo vira um círculo com o raio multiplicado por raiz de dois. E, como a área vai com o quadrado do raio, ela também dobra.

[thoughtful] Agora a mesma fórmula, lida como campo. A setinha em cima do F diz que o resultado é um vetor. Em cada ponto do plano, você pendura a seta com a soma e a diferença das coordenadas daquele ponto. No eixo horizontal, a coordenada vertical é zero, então as duas componentes ficam iguais: à direita da origem, as setas saem na diagonal, para cima. No eixo vertical, a seta é a coordenada vertical e menos ela: em cima da origem, as setas apontam para a direita e para baixo; embaixo, para a esquerda e para cima.

[curious] E aqui fica uma pergunta que eu vou guardar para o topo da escada. Como transformação, a área dobrou. Como campo, se a gente soltar um pedacinho de fluido nessas setas, a área dele também dobra? Guarda o seu palpite.

### D2 · Desenhar sem desenhar mil setas

[thoughtful] Segundo degrau: desenhar um campo sem calcular mil setas. O campo é este: a componente horizontal vale sempre um, e a vertical vale a coordenada horizontal menos a vertical. Pausa o vídeo e tenta desenhar.

[curious] O truque é procurar onde o campo não muda. A componente horizontal nunca muda. A vertical só depende da diferença entre as coordenadas. Então, em cima de uma reta onde essa diferença é constante, a seta é a mesma em todo ponto. A seta dupla da tela lê-se implica. E essas retas são as paralelas à diagonal.

[thoughtful] Na própria diagonal, a diferença é zero: a seta é um, zero, deitada, apontando para a direita. Uma reta abaixo, onde a diferença vale um: a seta é um, um, a quarenta e cinco graus. Mais uma abaixo, diferença dois: um, dois, mais empinada. E, acima da diagonal, a diferença fica negativa, e as setas apontam para baixo.

[curious] Agora é só copiar: uma seta por reta, repetida ao longo da reta inteira. E o campo inteiro está desenhado: setas que vão empinando à medida que você desce de reta em reta, e que se inclinam para baixo quando você sobe.

[thoughtful] Grava esse desenho, porque ele vai voltar. Esse empinar de reta em reta é uma derivada, e no topo da escada a gente vai ler isso numa tabela.

### D3 · A família de redemoinhos

[thoughtful] Terceiro degrau: uma família inteira de redemoinhos de uma vez. Começa pelo redemoinho do primeiro episódio, menos a coordenada vertical na primeira componente e a horizontal na segunda, e divide tudo pela distância ao quadrado elevada a um expoente alfa. Xis ao quadrado mais ípsilon ao quadrado é a distância ao quadrado. Cada valor do expoente alfa é um redemoinho diferente. Pausa o vídeo e tenta: o que muda com alfa zero, meio e um?

[curious] As setas são sempre tangentes às circunferências em volta da origem, então tudo dá a volta no sentido anti-horário. O que muda é o tamanho. O vetor de cima tem tamanho igual à distância, e o de baixo é a distância elevada a dois alfa. Então a rapidez é a distância elevada a um menos dois alfa. Com alfa zero, a rapidez cresce com a distância: é o disco girando rígido. Com alfa meio, a rapidez vale um em todo lugar. Com alfa um, ela cai com um sobre a distância: é o vórtice.

[thoughtful] Agora a conta do rotacional. Na tela, P e Q são as duas componentes, e o d arredondado é a derivada parcial. O rotacional é a derivada da componente vertical na direção horizontal, menos a derivada da componente horizontal na direção vertical. A componente vertical é a coordenada horizontal vezes a distância ao quadrado elevada a menos alfa. Regra do produto: a primeira parte dá a própria potência; a segunda, pela regra da cadeia, dá menos alfa vezes a potência com um a menos no expoente, vezes duas vezes a coordenada horizontal, vezes a coordenada horizontal de novo. Põe a potência com um a menos em evidência: sobra a distância ao quadrado menos dois alfa vezes o quadrado da coordenada horizontal. A outra derivada é igualzinha, com a vertical no lugar da horizontal e o sinal trocado. Na subtração, a distância ao quadrado aparece duas vezes, e os dois termos com alfa se juntam em dois alfa vezes a soma dos quadrados, que é a distância ao quadrado de novo. Sobra uma fórmula curtinha: dois menos dois alfa, dividido pela distância ao quadrado elevada a alfa. E o divergente? Agora é a soma: a derivada da componente horizontal na direção horizontal, mais a da vertical na direção vertical. Nas duas, só a regra da cadeia trabalha, e sai o mesmo termo, dois alfa vezes o produto das coordenadas vezes a potência com um a menos: uma vez com sinal de mais, outra com sinal de menos. Eles se cancelam: zero, para qualquer alfa. Nenhum desses redemoinhos muda a área do fluido.

[curious] Agora lê a fórmula. Alfa zero: dois menos zero, sobre a potência zero, que vale um. Rotacional dois, o giro do disco rígido. Alfa meio: dois menos um, sobre a distância. Todas as setas do mesmo tamanho e, mesmo assim, o rotacional é um sobre a distância. O quadradinho gira, e gira mais quanto mais perto do centro. Alfa um: dois menos dois dá zero. As partículas dão a volta, e o quadradinho não gira: o vórtice do segundo episódio.

[excited] E alfa dois? Dois menos quatro dá menos dois: o rotacional fica negativo. As setas continuam dando a volta no sentido anti-horário, e o quadradinho gira no sentido horário! Olha por quê: a seta do lado de dentro é bem mais forte que a do lado de fora, então a borda de dentro do quadradinho corre na frente, e ele vira para trás. O sentido da volta não é o sentido do giro.

[thoughtful] E na origem? Todos esses campos dividem por zero lá, então a pergunta é se existe limite. Lê-se: limite de F quando X tende à origem. Com alfa zero, não tem divisão nenhuma: é o disco rígido, já definido e contínuo na origem. Com alfa entre zero e meio, a fórmula não vale no centro, mas a rapidez vai a zero quando você chega nele. Então o limite é o vetor nulo e, definindo a seta da origem como zero, o campo fica contínuo. Com alfa meio, a rapidez fica um, mas a direção depende do caminho por onde você chega: não tem limite. E, com alfa maior que meio, a seta explode.

[curious] Último item: gira cada seta noventa graus, no sentido horário. O redemoinho vira uma explosão, com as setas apontando para fora. A componente horizontal nova é a vertical antiga, e a vertical nova é menos a horizontal antiga. Então o divergente novo é exatamente a conta do rotacional antigo, e os papéis se trocam: o rotacional vira zero, e o divergente vira os mesmos dois menos dois alfa sobre a distância ao quadrado elevada a alfa. Com alfa um, é a falsa fonte do segundo episódio. [thoughtful, emphatic] Guarda essa fórmula: dois menos dois alfa. Ela ainda vai escolher uma lei da física.

### D3b · Duas regras para qualquer campo

[thoughtful] Antes de subir, duas regras que valem para qualquer campo. Primeira: pega um campo que é o gradiente de uma função, ou seja, as componentes são as derivadas parciais dessa função. Na tela, nabla fi: lê-se gradiente de fi. E, daqui em diante, P com xis pequeno embaixo é a derivada parcial de P em relação a xis. Calcula o rotacional. A primeira componente é a derivada em relação à vertical da derivada em relação à profundidade, menos a derivada em relação à profundidade da derivada em relação à vertical. E as outras duas componentes têm a mesma cara: uma derivada mista, menos a mesma derivada mista com a ordem trocada. E, se a função é de classe cê dois, as derivadas mistas são iguais: é o teorema de Schwarz. Tudo cancela. No plano, só sobra a terceira componente, e ela também zera. Um gradiente nunca gira.

[curious] Lembra do campo que esticava o quadradinho no episódio passado? Ele é o gradiente da metade da diferença entre os quadrados das coordenadas. Por isso o quadradinho deformava, mas não girava.

[thoughtful] Segunda regra, agora no espaço, com três componentes. Calcula o rotacional de um campo e, depois, o divergente desse rotacional: a primeira componente é derivada na horizontal, a segunda na vertical e a terceira na profundidade. Aparecem seis derivadas mistas, e elas se cancelam aos pares, de novo por Schwarz. Um rotacional nunca diverge.

[curious] E isso vira teste. Alguém te dá este campo e pergunta: existe outro campo cujo rotacional é ele? Não precisa procurar. Calcula o divergente: a primeira parcela dá seno, a segunda dá menos seno, e a terceira dá um. Total: um. Se ele fosse um rotacional, o divergente teria que ser zero. Então não existe.

[thoughtful] E isso aparece na física. O campo magnético tem divergente zero em todo lugar: é a lei que diz que não existe polo magnético isolado. E, no espaço todo, isso permite escrever o campo magnético como o rotacional de outro campo, o potencial vetor. A seta dupla nos dois sentidos lê-se se e somente se. As duas ideias andam juntas, e a regra de hoje prova uma das metades: todo rotacional tem divergente zero.

[thoughtful, emphatic] E repara na hipótese: classe cê dois. Sem derivadas contínuas, a ferramenta pode falhar. No próximo degrau, a gente vê de perto o que acontece quando falta regularidade.

### D4 · O campo que não melhora de perto

[thoughtful] Quarto degrau, o mais difícil da escada. Este campo pega o vetor posição e multiplica pelo produto das coordenadas, dividido pela distância ao quadrado. Na origem, onde a fórmula divide por zero, a gente define a seta como zero.

[curious] Olha o desenho. Nas diagonais de subida, as setas apontam para fora. Nas outras diagonais, apontam para dentro. E, em cima dos eixos, não tem seta, porque o produto das coordenadas é zero. Pausa o vídeo e tenta os cinco itens.

[thoughtful] Item a: existe limite na origem? Calcula o tamanho da seta. As barras duplas da tela são esse tamanho, a norma; a barra simples é o módulo, o valor sem sinal. O vetor posição tem tamanho igual à distância, então a seta tem tamanho igual ao módulo do produto das coordenadas, dividido pela distância. Em polares, o produto das coordenadas é a distância ao quadrado vezes o cosseno e o seno do ângulo, e cosseno vezes seno é metade do seno do dobro do ângulo. Então o tamanho da seta é a distância vezes metade do módulo desse seno, e isso nunca passa da metade da distância.

[curious] Agora o desafio do épsilon. Épsilon é a tolerância na seta; delta, o raio onde você anda. Alguém escolhe um épsilon. Você responde com delta igual a dois épsilon. Se o ponto está a menos de delta da origem, a seta tem tamanho de no máximo a metade disso, ou seja, menos que épsilon. Venceu, para qualquer épsilon. O limite é o vetor nulo.

[thoughtful] Item b: é contínuo? O ponto está no domínio, porque a gente definiu a seta lá. O limite existe. E é igual à seta do ponto, zero. Os três pedaços passam: contínuo. Item c: as derivadas parciais na origem. Andando pelo eixo horizontal, a seta é zero o caminho todo: derivada zero. Na tela, ela é o limite, quando h tende a zero, da diferença das setas dividida pelo passo h. Pelo vertical, a mesma coisa. A tabela é toda zero: rotacional zero, divergente zero, deformação zero. A previsão seria: perto da origem, nada acontece.

[curious] Item d: confere com um zoom. No episódio passado, o zoom de dez vezes no campo da aula deixava as setas arrumadinhas, iguais ao modelo linear. Aqui, olha: o zoom de dez vezes dá exatamente o mesmo desenho. E o de cem vezes, também. Esse campo é homogêneo: multiplicar a posição por um número multiplica a seta pelo mesmo número. Na conta, o número aparece ao quadrado em cima e embaixo, cancela, e sobra uma vez. Então ele nunca fica parecido com a tabela, por mais perto que você chegue. Na diagonal, a seta tem sempre metade do tamanho do passo: o erro da tabela, dividido pelo passo, fica em meio e não vai a zero. Para o campo ser diferenciável na origem, essa razão teria que ir a zero. Não vai. Em qualquer vizinhança, por menor que seja, tem quadradinho crescendo nas diagonais de subida, encolhendo nas outras, e girando para os dois lados.

[thoughtful, emphatic] A tabela errou. E por quê? Item e: calcula a derivada da componente horizontal na direção horizontal, fora da origem. A componente horizontal é o quadrado da coordenada horizontal vezes a vertical, sobre a distância ao quadrado. Regra do quociente: no numerador, a derivada de cima vezes a de baixo, menos a de cima vezes a derivada de baixo. A derivada de cima é duas vezes o produto das coordenadas; a de baixo, duas vezes a horizontal. Os termos com a quarta potência se cancelam, e sobra duas vezes a coordenada horizontal vezes o cubo da vertical, sobre a distância à quarta. Agora olha essa derivada perto da origem. Nos eixos, ela vale zero. Na diagonal, as duas coordenadas são iguais: duas vezes a quarta potência, sobre quatro vezes a quarta potência, meio. E vale meio e vale meio na diagonal inteira, por mais perto que você chegue. Ela não é contínua na origem. O campo não é de classe cê um, e a tabela perde a garantia. Repara: o cê um é uma garantia, não uma exigência. Tem campo que não é cê um e mesmo assim é bem aproximado pela tabela. Só que aqui a gente provou, direto, que a aproximação falha.

[curious] E olha a escada: no episódio passado, o campo encrenqueiro nem era contínuo. Este é contínuo, tem as duas derivadas parciais e, mesmo assim, engana. Ter derivadas parciais não basta para a tabela descrever o campo de perto.

### D5 · O desafio prometido

[excited] Topo da escada! Chegou a hora do desafio do episódio passado. Três campos. Para cada um: monta a tabela, lê os quatro números e prevê se o quadradinho gira, muda de área ou deforma. Só depois a gente solta o fluido. A tabela se chama jacobiana, a letra J: derivadas de P em cima, de Q embaixo. Lembra das quatro medidas. Rotacional: o de baixo à esquerda menos o de cima à direita. Divergente: a diagonal somada. Primeira deformação, dê um: a diagonal subtraída. Segunda, dê dois: os dois de fora da diagonal, somados.

[thoughtful] Primeiro campo: a fórmula do primeiro degrau, a soma e a diferença das coordenadas. Pausa o vídeo e tenta.

[thoughtful] A tabela. A componente horizontal é a soma, então as derivadas dela são um e um. A vertical é a diferença: um e menos um. Em cima, um e um; embaixo, um e menos um. Agora as medidas. Rotacional: o de baixo à esquerda menos o de cima à direita, um menos um, zero. Divergente: a diagonal, um mais menos um, zero. Primeira deformação: um menos menos um, dois. Segunda: um mais um, dois. Previsão: não gira, não muda de área, só deforma.

[curious] Solta. O quadradinho estica numa direção, um pouco acima do eixo horizontal, achata na outra, e a área fica igual o tempo todo.

[excited] E aí está a resposta do palpite. Como transformação, essa fórmula dobrava a área. Como campo, ela não muda a área nenhuma. Por quê? Porque são dois filmes diferentes. A transformação leva cada ponto, de uma vez, para a imagem. O campo é uma velocidade: o fluido anda devagarinho, seguindo as setas, e quem mede a taxa de área desse fluido é o divergente, que aqui é zero. O fator de área de uma transformação é outro número, que vai aparecer quando a gente estudar mudança de variáveis.

[thoughtful] Segundo campo: o do segundo degrau, um na horizontal e a diferença na vertical. Pausa e tenta.

[thoughtful] A componente horizontal é constante: derivadas zero e zero. A vertical: um na direção horizontal e menos um na vertical. Tabela: zero e zero em cima; um e menos um embaixo. Rotacional: um menos zero, um. Divergente: zero mais menos um, menos um. Deformações: zero menos menos um, um; e um mais zero, um. Previsão: tudo junto. Gira no sentido anti-horário, encolhe e entorta.

[curious] E dava para ler isso no desenho do segundo degrau: andando para a direita, a seta empina, e esse é o um embaixo à esquerda. Andando para cima, a seta abaixa, e esse é o menos um. Solta: o quadradinho viaja para a direita, porque a seta do centro não é zero, e, no caminho, gira, encolhe e entorta. A viagem não está na tabela, porque a gente tirou a seta do centro. A tabela conta o que acontece com a forma.

[thoughtful] Terceiro campo: a primeira componente é a diferença dos quadrados das coordenadas; a segunda, duas vezes o produto delas. Agora a tabela não é constante. Derivando a diferença dos quadrados, sai duas vezes a coordenada horizontal na direção horizontal, e menos duas vezes a vertical na direção vertical: essa é a primeira linha. Derivando duas vezes o produto, sai duas vezes a vertical na direção horizontal, e duas vezes a horizontal na direção vertical: a segunda linha. Então o ponto importa. Pausa o vídeo e prevê nos três pontos: um, zero; zero, um; e um, um.

[curious] Rotacional: duas vezes a vertical, menos menos duas vezes a vertical: quatro vezes a vertical. Divergente: duas vezes a horizontal mais duas vezes a horizontal: quatro vezes a horizontal. E as duas deformações: cada uma é um termo menos ele mesmo. Zero, em qualquer ponto. No ponto um, zero: quatro vezes zero, rotacional zero; quatro vezes um, divergente quatro. Só cresce. No zero, um: rotacional quatro, divergente zero. Só gira. No um, um: gira e cresce.

[excited] Solta os três! Um cresce sem girar, um gira sem crescer, e o terceiro faz as duas coisas. E nenhum entorta: as quinas continuam em ângulo reto. E repara: a tabela fala do que acontece no ponto, naquele instante. Um quadradinho de tamanho finito sente a tabela mudando de um canto para o outro, e os lados até se curvam, mas tão pouco que nem dá para ver. Bem pequeno, esse campo nunca deforma um quadradinho. Guarda isso, porque ele tem nome, e vai aparecer na segunda parte.

[thoughtful, emphatic] Desafio cumprido. A fórmula do campo vira uma tabela, a tabela vira quatro números, e os quatro números contam o que acontece com um quadradinho bem pequeno, logo que você solta. E o cê um garante que essa leitura vale.

### P2 · Transição

[excited] Pronto: você já prevê um quadradinho só olhando a fórmula. Agora vem a melhor parte. Essas contas não ficam no papel. Elas descrevem água de verdade e escolhem leis da física. [thoughtful] Vamos começar por um rio.

### A1 · O rio

[thoughtful] Um canal de margens retas, com seis metros de largura. A água corre a um metro por segundo no meio, e a velocidade vai caindo até zero nas margens, numa parábola: a componente na direção do canal é um menos o quadrado da horizontal sobre nove. No meio dá um; nas margens, a três metros, dá um menos nove nonos, zero. Três perguntas: a água é incompressível? O escoamento gira? E onde o atrito é maior? Pausa o vídeo e tenta.

[curious] Primeira: a velocidade só tem a componente na direção do canal, e ela não muda ao longo do canal. Divergente zero: incompressível.

[thoughtful] Segunda: as linhas de corrente são retas, então dá vontade de dizer que não gira. Mas faz a conta. O rotacional é a derivada da componente na direção do canal, tomada na direção de uma margem para a outra: dá menos dois nonos da coordenada horizontal. Na margem esquerda, menos dois nonos vezes menos três: dois terços por segundo. um galho ali gira no sentido anti-horário. E lembra que o rotacional é o dobro da velocidade angular da rodinha: o galho gira com ômega, a velocidade angular, igual a um terço de radiano por segundo. E o período, o T da tela, o tempo de uma volta, é dois pi dividido por um terço, seis pi: uns dezenove segundos. Na margem direita, menos dois terços: gira no horário. E, bem no meio, zero: o galho desce o rio sem girar.

[curious] Olha os três quadradinhos. O do meio só viaja. Os das margens viajam, entortam e giram, cada um para um lado. Por quê? Perto da margem, a água do lado de dentro corre mais rápido que a do lado de fora, então a borda de dentro do quadradinho vai na frente.

[thoughtful] Terceira: o atrito. No episódio passado a gente viu que, num fluido como a água, o atrito viscoso vem da deformação: aqui, da diferença de velocidade entre camadas vizinhas. Aqui, a primeira deformação é zero, e a segunda é aquele mesmo menos dois nonos da coordenada horizontal. Máxima nas margens e zero no meio. É perto das margens que a água mais esfrega em si mesma.

### A2 · Água batendo na parede

[thoughtful] Segundo problema: um jato de água descendo e batendo numa parede, como a água da torneira batendo na pia. Num modelo ideal, perto do ponto do choque, a velocidade tem a coordenada horizontal na primeira componente e menos a vertical na segunda. É o campo do gancho do episódio passado, agora só na metade de cima, com a parede embaixo.

[curious] Primeiro: na parede, a componente vertical é zero. A água não atravessa a parede: ela desliza. Numa parede de verdade, uma camada fina de água gruda nela por causa da viscosidade, e esse modelo ideal ignora essa camada. Segundo: a tabela tem um e zero em cima, zero e menos um embaixo. Rotacional zero, divergente um menos um, zero, e primeira deformação um menos menos um, dois. A água não gira e não comprime: só deforma. Uma gota de tinta que desce pelo eixo se achata e se espalha pela parede, sempre com a mesma área. E as linhas de corrente são hipérboles, as curvas onde o produto das coordenadas é constante. Confere. Lê-se dê xis ípsilon, dê tê: a taxa de variação do produto no tempo. Andando com a água, o produto muda pela velocidade horizontal vezes a coordenada vertical, mais a horizontal vezes a velocidade vertical. Dá o produto menos o produto: zero. O produto não muda: a água anda em cima da hipérbole.

[thoughtful] Terceiro: esse campo é o gradiente da metade da diferença dos quadrados das coordenadas. Essa função tem nome: potencial de velocidade. E o laplaciano dela, escrito nabla dois fi, a soma das duas derivadas segundas, aquela curiosidade do segundo episódio, dá um menos um: zero.

[thoughtful, emphatic] E isso não é coincidência. Se a velocidade é um gradiente, ela é irrotacional, pela primeira das duas regras. Se, além disso, o divergente é zero, então o divergente do gradiente é zero. E o divergente do gradiente é o laplaciano. Escoamento irrotacional e incompressível quer dizer laplaciano do potencial igual a zero: a equação de Laplace. A mesma equação aparece no potencial elétrico numa região sem cargas e na temperatura de uma chapa em equilíbrio.

### A4 · Mapas que não entortam

[curious] Lembra do terceiro campo do desafio, aquele que nunca entorta? Vamos ver por quê. Deformação zero em todo lugar quer dizer duas equações. Iguala cada deformação a zero e passa um termo para o outro lado: a derivada horizontal da primeira componente igual à derivada vertical da segunda, e a derivada vertical da primeira igual a menos a derivada horizontal da segunda. Essas duas equações têm nome: equações de Cauchy-Riemann.

[thoughtful] Elas aparecem quando você junta as duas componentes num número complexo. O nosso campo é exatamente o quadrado do número complexo que tem a coordenada horizontal como parte real e a vertical como parte imaginária. Abre o quadrado; o i da tela é a unidade imaginária: o quadrado da horizontal, mais duas vezes a unidade imaginária vezes o produto, mais o quadrado da unidade imaginária vezes o quadrado da vertical. E o quadrado da unidade imaginária é menos um. Sobra a diferença dos quadrados na parte real e duas vezes o produto na imaginária. E toda função complexa derivável satisfaz essas equações: o cubo, a exponencial, todas.

[curious] Agora lê como transformação. Onde a derivada complexa não é zero, uma tabela assim só gira e muda a escala: quadradinhos pequenos viram quadradinhos, maiores ou menores, mas sempre com ângulos retos. Isso se chama mapa conforme. E você conhece um: o mapa-múndi de Mercator, aquele de parede de sala de aula, preserva os ângulos. Por isso a Groenlândia aparece quase do tamanho da África, mas com o formato certo em cada pedacinho.

[thoughtful] E o irmão desse campo, com o sinal da segunda componente trocado, faz o contrário: rotacional zero, divergente zero, só deformação.

### A3 · Por que um sobre a distância

[excited] E agora, o último problema, que fecha a escada inteira. Um fio comprido, com corrente, atravessando a tela. As linhas do campo magnético são circunferências em volta dele. A pergunta é: com que lei o campo enfraquece quando você se afasta? Pausa e pensa.

[thoughtful] A física diz duas coisas. Primeira, a simetria: o campo dá a volta no fio, e o tamanho só depende da distância. Supondo uma lei de potência, ele tem a forma do terceiro degrau: menos a coordenada vertical e a horizontal, divididas pela distância ao quadrado elevada a um expoente alfa que a gente não sabe. Segunda: fora do fio não tem corrente e, para campos que não mudam no tempo, a lei de Ampère diz que, onde não tem corrente, o rotacional do campo magnético é zero.

[curious] Agora usa a fórmula que a gente guardou. O rotacional é dois menos dois alfa, sobre a distância ao quadrado elevada a alfa. Para ser zero, só tem um jeito: o numerador zera, dois igual a dois alfa, e alfa igual a um. Então o tamanho do campo é a distância dividida pela distância ao quadrado: um sobre a distância. O campo do fio cai com um sobre a distância. A intensidade ainda depende da corrente; o que a conta escolhe é como ela cai.

[thoughtful] Faz o mesmo com um fio carregado. O campo elétrico aponta para fora, então ele é a explosão do terceiro degrau. Fora do fio não tem carga, e a lei de Gauss diz que o divergente é zero. Divergente: dois menos dois alfa, de novo. Alfa um, e o campo também cai com um sobre a distância.

[excited] E uma carga pontual, no espaço? Escreve o campo como o vetor posição dividido pela distância elevada a um expoente. O X maiúsculo é o vetor posição; as barras duplas, a distância; p, o expoente. No plano, o divergente seria dois menos esse expoente. Faz a conta de uma parcela: a derivada da coordenada horizontal sobre a distância elevada ao expoente, na direção horizontal. A derivada da distância, nessa direção, é a coordenada horizontal sobre a distância. Então dá um sobre a distância elevada ao expoente, menos o expoente vezes o quadrado da coordenada horizontal, sobre a distância elevada ao expoente mais dois. As outras parcelas são iguais, cada uma com a sua coordenada. Agora soma: os três primeiros termos dão três; e os quadrados das coordenadas somam a distância ao quadrado, que cancela o mais dois do expoente. Sobra o número de parcelas menos o expoente. No plano são duas parcelas; no espaço, três. Então o divergente no espaço é três menos o expoente, dividido pela distância elevada ao expoente. Para zerar, o expoente é três, e o tamanho do campo fica um sobre a distância ao quadrado. A lei do inverso do quadrado, a de Coulomb e a da gravitação.

[thoughtful, emphatic] No plano, o número que aparece é dois; no espaço, é três. O expoente da lei vem da dimensão do espaço: em três dimensões, o campo tem mais lugar para se espalhar. E fica o cuidado: não é o rotacional ou o divergente sozinhos que decidem a lei. É a lei física, o rotacional zero ou o divergente zero fora da fonte, junto com a simetria: as linhas em círculo em volta do fio e o campo radial em volta da carga. Com as duas juntas, não sobra escolha.

### S · Síntese, gancho e CTA

[thoughtful] Olha a escada inteira. A mesma fórmula conta dois filmes. Um campo se desenha pelas curvas onde ele não muda. O sentido da volta não é o sentido do giro. Um gradiente nunca gira, e um rotacional nunca diverge. Ter derivadas parciais não basta. E, com a tabela, você prevê o quadradinho antes de soltar. [curious] E, nas aplicações, um rio que gira nas margens, uma parede onde a água só deforma, mapas que nunca entortam e o um sobre a distância escolhido pela conta.

[excited] No próximo vídeo, a gente troca de pergunta. Até aqui, tudo foi medido num ponto, bem de perto. Agora é hora de somar pedacinhos. Uma chapa quadrada, de dois metros de lado, leve num canto e cada vez mais densa até o canto oposto. Pelo valor do centro, a massa dá oito quilos. Pela média dos quatro cantos, dezesseis. O dobro! Qual das duas está certa? A resposta exata vem de somar infinitos pedacinhos: a integral dupla.

[happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual degrau da escada foi o mais difícil para você? Até a próxima!
