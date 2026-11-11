# yt_0026 · narração com tags (ElevenLabs v4), gerada de narracao.md (handoff v9)

## Texto corrido (para gravação)

[curious] Uma seta, num ponto só, mostra uma direção. Sozinha, ela quase não diz nada. Mas junta infinitas delas, e elas contam a história do espaço inteiro.

[thoughtful] É assim o tempo todo no Cálculo três. Quer o volume debaixo de uma superfície curva? Empilha colunas finíssimas… e elas viram um volume.

[thoughtful] Soma o empurrão de um campo em cada pedacinho de um caminho, ajudando num trecho, atrapalhando em outro… e sai o trabalho ao longo dele.

[thoughtful] Imagina uma corrente de água furando uma superfície. Conta o que atravessa cada pedacinho… e sai o fluxo.

[thoughtful, emphatic] E aí vem a surpresa. Quando você soma o que acontece em cada pedacinho de dentro, as trocas entre vizinhos se cancelam, e só sobra o que passa pela borda. No plano, esse é o teorema de Green. Numa superfície, o de Stokes. Num volume, o de Gauss. O local e o global estão conectados.

[excited] Isso é Cálculo três: do infinitamente pequeno ao espaço inteiro. E a primeira peça é justamente aquela seta, num ponto só.

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab, e que bom ter você aqui no primeiro vídeo do canal. O Cálculo três é a matéria em que tudo o que você já sabe sai da reta e do plano e passa a valer no espaço inteiro: é a matemática do vento, da gravidade, da eletricidade, do escoamento da água. O assunto de hoje é a primeira peça disso, a função que recebe um ponto e devolve uma seta. A gente vai ver o que ela é, por que o gráfico dela não cabe em lugar nenhum, e as duas maneiras de enxergar uma: como transformação e como campo vetorial. E já aviso: no meio do caminho tem um mistério, uma mesma fórmula que desenha duas coisas completamente diferentes. Para começar, olha só.

[curious] Olha essa folha de papel milimetrado, com uma bandeirinha desenhada. Agora uma regra bem simples pega cada ponto da folha e manda para outro lugar: ela troca as duas coordenadas de lugar e coloca um sinal de menos na primeira. E o resultado é esse: o plano inteiro gira um quarto de volta, de uma vez só, e a bandeira vai junto.

[thoughtful] Agora a mesma regra, sem mudar nada, desenhada de outro jeito. Em vez de mover os pontos, a gente pendura em cada ponto uma setinha com aquilo que a regra devolve. E aparece um redemoinho: setas girando em volta do centro, pequenas perto dele e cada vez maiores para fora.

[curious] Espera aí. É a mesma fórmula, sem mudar nada. Num desenho, ela gira o plano inteiro; no outro, vira um redemoinho de setas. Qual dos dois é o desenho certo dessa função? E por que ela precisa de dois desenhos, se uma função comum tem um gráfico só? É isso que a gente vai descobrir.

[thoughtful] Vamos começar pelo que você já conhece. Uma curva é uma função que recebe um número só, o tempo, por exemplo, e devolve um ponto do plano ou do espaço. E uma função de várias variáveis, do jeito que você viu até agora, faz o contrário: recebe um ponto e devolve um número só, como a temperatura em cada lugar de uma sala.

[thoughtful] Agora junta as duas ideias: uma função que recebe um ponto, com várias coordenadas, e devolve outro ponto, também com várias coordenadas. Ela parte de um conjunto, o domínio, num espaço de certa dimensão, e chega num espaço que pode ter outra dimensão. Repara que as curvas e as funções de várias variáveis são os casos extremos, em que a entrada ou a saída é um número só. Hoje o interesse está no resto: entra um ponto do plano e sai um ponto do plano, ou do espaço; entra um ponto do espaço e sai um vetor do espaço. E repara numa coisa: cada coordenada da saída é, sozinha, uma função comum, que recebe o ponto e devolve um número. São as funções componentes, e a função inteira é só elas lado a lado.

[curious] E aqui aparece o problema. Para uma função de duas variáveis a valores reais, o gráfico é uma superfície: duas coordenadas para a entrada, uma para a saída, três no total, e isso cabe no espaço. Só que, se entram duas coordenadas e saem duas, o gráfico precisaria de quatro eixos. Não cabe na tela, não cabe na sala, não cabe em lugar nenhum que a gente consiga ver.

[thoughtful, emphatic] Então a gente desiste do gráfico e desenha a função de dois outros jeitos. No primeiro, a função é uma máquina que move pontos: pega um conjunto e mostra no que ele se transforma. No segundo, a função pendura uma seta em cada ponto. São esses dois jeitos que vão responder a pergunta do começo.

[thoughtful] Primeiro jeito: a função como transformação. A ideia é desenhar dois planos lado a lado. À esquerda, o plano de entrada, de onde saem os pontos. À direita, o plano de saída, onde eles chegam. E a pergunta passa a ser: quando eu jogo um conjunto inteiro pela função, que forma ele ganha do outro lado?

[thoughtful] O exemplo clássico são as coordenadas polares. No plano de entrada, o eixo horizontal é um ângulo e o eixo vertical é um raio. A função pega esse par e devolve o ponto que está a essa distância da origem, girado desse ângulo: a coordenada horizontal é o raio vezes o cosseno do ângulo, e a vertical é o raio vezes o seno do ângulo. Essas duas fórmulas são as componentes da função.

[curious] Vamos acompanhar alguns pontos. Ângulo zero e raio dois: o ponto vai parar no eixo horizontal, a duas unidades da origem. Ângulo de noventa graus, mesmo raio: ele sobe para o eixo vertical. Ângulo de cento e oitenta graus e raio um: cai do lado esquerdo, a uma unidade da origem.

[thoughtful] Agora, em vez de pontos soltos, uma reta inteira. Fixa o raio em dois e deixa o ângulo correr de zero até uma volta completa. No plano de entrada, isso é um segmento horizontal. Do outro lado, é uma circunferência de raio dois. Ou seja, o segmento se enrolou. E se a gente fixa o ângulo e deixa o raio variar, sai um segmento que parte da origem, como um raio de roda de bicicleta.

[excited] Junta tudo e olha o retângulo inteiro: ângulo de zero a uma volta, raio de zero a dois. Cada faixa horizontal vira um anel, cada faixa vertical vira um raio da roda, e o retângulo se fecha num disco de raio dois!

[curious] Repara em duas coisas nas bordas. O lado de baixo do retângulo, onde o raio é zero, é um segmento inteiro… e ele vai todo parar num ponto só, a origem. A função esmagou um segmento num ponto. E os dois lados verticais, o de ângulo zero e o de ângulo de uma volta, caem exatamente um em cima do outro: o retângulo foi colado nele mesmo para fechar o disco.

[thoughtful] Esse disco tem nome: é a imagem do retângulo pela função, tudo o que a função faz sair dele. E a moral do primeiro jeito é essa: para enxergar uma transformação, você não fica olhando a fórmula; você acompanha conjuntos e vê no que eles viram. Só um aviso honesto: o retângulo se enrolando aos poucos é animação, para o olho acompanhar. A função liga direto cada ponto de entrada ao seu ponto de saída.

[curious] Agora um caso mais traiçoeiro. Uma função que repete a primeira entrada na primeira saída e, na segunda saída, coloca a soma dos quadrados das duas entradas. Como ela deforma o plano?

[thoughtful] A estratégia é a mesma: acompanhar retas. Fixa a segunda entrada em um e deixa a primeira correr. A coordenada horizontal da saída é a primeira entrada, e a vertical é esse valor ao quadrado, mais um: a parábola padrão, levantada uma unidade. Com a segunda entrada fixa em dois, a parábola sobe quatro unidades. Cada reta horizontal vira uma parábola, todas com o mesmo formato, empilhadas.

[curious] Só que tem um detalhe. A segunda entrada aparece ao quadrado. Então a reta em que ela vale menos um vai parar na mesma parábola da reta em que ela vale um. Duas retas diferentes, uma imagem só.

[thoughtful] E as retas verticais? Fixa a primeira entrada em um. A saída fica com coordenada horizontal um, e vertical igual a um mais o quadrado da segunda entrada. Enquanto a segunda entrada vem dos negativos até zero, o ponto desce pela vertical até a altura um; quando ela passa de zero, o ponto sobe de novo pelo mesmo caminho. A reta inteira vira uma semirreta, percorrida duas vezes: desce e volta.

[thoughtful, emphatic] Juntando tudo: essa função faz duas coisas. Primeiro, dobra o plano ao meio, ao longo do eixo horizontal, como quem dobra uma folha de papel: a metade de baixo cai em cima da metade de cima. Depois, estica essa meia-folha para cima. E a linha da dobra, onde a segunda entrada é zero, vira a borda da imagem: a parábola padrão. A imagem é tudo o que está sobre essa parábola ou acima dela… e nada abaixo.

[thoughtful] Dá para conferir sem desenho nenhum. Pega um ponto do plano de saída: quem chega nele? A primeira entrada tem que ser a coordenada horizontal do ponto, e o quadrado da segunda entrada tem que ser a altura menos o quadrado da coordenada horizontal. Acima da parábola, essa diferença é positiva: duas soluções, uma de cada lado da dobra. Na parábola, ela é zero: sobra uma só, a da linha da dobra. E abaixo ela é negativa; como nenhum número real ao quadrado dá negativo, ninguém chega lá.

[curious] E se a saída tiver três coordenadas? Pega cada ponto do plano e devolve um ponto do espaço: as duas primeiras coordenadas ficam iguais às da entrada, e a terceira, a altura, é a soma dos quadrados delas, ou seja, o quadrado da distância até a origem.

[thoughtful] Olha o que acontece com a folha. A origem fica no chão. A circunferência de raio um sobe para a altura um. A de raio dois sobe para a altura quatro. E a folha plana inteira vira uma tigela, um paraboloide.

[thoughtful] Repara numa coisa: essa tigela é exatamente o gráfico daquela função de duas variáveis que dá o quadrado da distância até a origem. Ou seja, o gráfico que você já conhecia é um caso particular de imagem de uma transformação. E essa ideia, fabricar uma superfície levantando uma folha plana, vai voltar quando a gente chegar às integrais de superfície.

[thoughtful] Agora o segundo jeito, que serve quando a entrada e a saída têm o mesmo número de coordenadas. Em vez de mandar o ponto para outro lugar, a gente desenha o vetor de saída com o pé no próprio ponto de entrada: um vetor aplicado no ponto. Lida desse jeito, a função se chama campo vetorial, e na tela o nome dela ganha uma setinha em cima, justamente para lembrar essa leitura. Em geral, um campo no plano se escreve com duas componentes, uma na direção de i e outra na direção de j, cada uma uma função comum das coordenadas.

[curious] O exemplo mais simples: um campo que devolve o mesmo vetor, uma unidade para cima, em qualquer ponto. Desenhado como campo, é o plano coberto de setas iguais, todas para cima, como um vento uniforme. Agora a mesma fórmula lida como transformação: todo ponto do plano vai parar no mesmo lugar, uma unidade acima da origem. O plano inteiro é esmagado num ponto só. Um desenho mostra vento; o outro, um colapso.

[thoughtful] Segundo exemplo: o campo que devolve, em cada ponto, o próprio vetor posição daquele ponto. Como campo, cada seta aponta para fora, para longe da origem, e o tamanho da seta é igual à distância até a origem. Perto do centro, setinhas curtas; longe, setas compridas; e, em cima de uma mesma circunferência centrada na origem, todas do mesmo tamanho. E como transformação? Cada ponto vai para… ele mesmo. É a identidade: nada se mexe. A fórmula que, como transformação, não faz absolutamente nada, como campo é uma explosão de setas para fora.

[thoughtful, emphatic] Então já dá para responder metade da pergunta do começo. Nenhum dos dois desenhos é o certo. A fórmula é a mesma; quem decide o desenho é a leitura. Como transformação, a pergunta é: para onde cada ponto vai? Como campo, a pergunta é: que seta cada ponto carrega?

[curious] Agora volta lá para o começo: a regra que troca as coordenadas de lugar e coloca um sinal de menos na primeira. Como transformação, ela leva cada ponto um quarto de volta adiante, em torno da origem, no sentido anti-horário. Por isso o plano inteiro girou. E como campo? Vamos desenhar sem decorar nada, só com três perguntas.

[thoughtful] Primeira pergunta: quanto o campo vale em alguns pontos? No ponto a uma unidade à direita da origem, a seta aponta para cima. No ponto uma unidade acima, aponta para a esquerda. À esquerda da origem, aponta para baixo; embaixo, para a direita. Já dá para sentir o giro.

[thoughtful] Segunda pergunta: onde o tamanho da seta é sempre o mesmo? O tamanho dessa seta é a raiz da soma dos quadrados das coordenadas, ou seja, a distância até a origem. Então, em cada circunferência centrada na origem, todas as setas têm o mesmo tamanho, e esse tamanho cresce com o raio.

[thoughtful, emphatic] Terceira pergunta: para onde a seta aponta, comparada com o vetor posição? Faz o produto escalar dos dois: sai menos o produto das coordenadas, mais o produto das coordenadas… que dá zero. E produto escalar zero quer dizer perpendicular. Cada seta é perpendicular ao vetor posição, ou seja, tangente à circunferência que passa por ali. Junta as três respostas e o redemoinho aparece sozinho: setas tangentes às circunferências, cada vez maiores para fora.

[curious] E quem é que se move nesse redemoinho? Aqui entra a derivada. Lê o campo como velocidade: a seta em cada ponto é a velocidade de quem passa por ali. Agora pega uma circunferência de raio qualquer, percorrida com o ângulo igual ao tempo. A derivada dessa curva em relação ao tempo é exatamente o vetor que o campo pendura no ponto onde a curva está. Ou seja, as circunferências são as trajetórias desse campo.

[excited] E olha que bonito: toda circunferência leva o mesmo tempo para dar uma volta, pequena ou grande. Bem no centro, a seta tem tamanho zero, e o ponto fica parado; longe do centro, a velocidade cresce na proporção do raio. É exatamente assim que se move cada pedacinho de um disco rígido girando a um radiano por segundo. Esse redemoinho é o campo de velocidades de um disco girando!

[thoughtful] E agora dá para ver onde as duas leituras se encontram. A transformação dá um quarto de volta de uma vez só. O campo, lido como velocidade, faz os pontos girarem sem parar. Deixa esse giro correr por um tempo de pi sobre dois, que é um quarto do tempo de uma volta… e cada ponto chega exatamente onde a transformação tinha levado. São operações diferentes, ligadas por esse tempo.

[curious] E no espaço? A mesma ideia, com uma dimensão a mais. Em cada ponto do espaço, uma seta que aponta para a origem, com tamanho igual a um dividido pelo quadrado da distância. Longe, setas quase sumindo; perto, cada vez maiores. É o formato do campo gravitacional em volta de uma estrela.

[thoughtful] Repara no domínio. Bem na origem, a distância é zero, e não dá para dividir por zero. Então esse campo está definido no espaço inteiro, menos um ponto: a origem. É por isso que a definição sempre começa dizendo de onde a função parte. O domínio faz parte da função.

[calm, satisfied] Então, a pergunta do começo está respondida. A mesma fórmula girava o plano e desenhava um redemoinho porque são duas leituras da mesma função. Como transformação, ela move os pontos, e a gente enxerga isso acompanhando conjuntos: segmentos viram circunferências, retângulos viram discos, folhas viram tigelas. Como campo, ela pendura uma seta em cada ponto, e a gente enxerga isso perguntando pelo tamanho e pela direção das setas. E as duas leituras são necessárias porque o gráfico, com quatro eixos, não cabe em lugar nenhum.

[thoughtful] Essas duas leituras não saem mais de cena no Cálculo três. As transformações voltam quando a gente trocar de coordenadas dentro de uma integral, e aquele disco das coordenadas polares volta junto. Os campos voltam nas integrais de linha, no fluxo e nos grandes teoremas. E aquela frase do começo, o local e o global estão conectados, é justamente para onde tudo isso caminha.

[curious] Fica uma pergunta para você pensar: se um barquinho de papel for levado por esse redemoinho, ele só dá voltas em torno do centro… ou também gira em torno de si mesmo? Deixa a sua resposta nos comentários. No próximo vídeo, a gente descobre como medir esse giro, ponto a ponto, e por que andar em círculo não é o mesmo que girar sobre si. Se essa aula te ajudou, deixa o like e se inscreve no Parallax Lab. Até a próxima!
