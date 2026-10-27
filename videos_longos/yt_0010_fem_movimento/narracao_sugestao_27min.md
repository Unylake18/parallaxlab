# FEM DE MOVIMENTO E REGRA DO FLUXO MAGNÉTICO — narração consolidada (base física: revisão do Work; base de voz: Claude)

Estilo: professor de cursinho, íntimo e didático; variáveis sempre pelo nome. Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`. A animação se molda à voz (não à duração do preview silencioso).

### N00 — abertura

Fala, pessoal! Bem-vindos ao Parallax Lab.

Hoje a gente vai pegar um único experimento e espremer dele bastante física.

Uma barra metálica desliza sobre dois trilhos dentro de um campo magnético. O circuito está fechado, aparece corrente e o resistor começa a dissipar energia.

Sem bateria.

Só que aí aparece um problema meio incômodo: a força magnética sobre uma carga é sempre perpendicular à velocidade da própria carga. E, se a força é perpendicular à velocidade, ela não realiza trabalho.

Então... de onde está vindo a energia que aparece no resistor?

Essa é a pergunta que vai guiar o vídeo inteiro.

E o mais legal é que, quando a gente terminar, força de Lorentz, força eletromotriz, regra do fluxo e conservação de energia vão parecer partes da mesma história, porque são.

### N01 — o fenômeno

Por enquanto, só acompanha a cena.

A barra é puxada para a direita com velocidade constante.

Enquanto ela se move, existe corrente no circuito e o resistor dissipa energia. O destaque laranja representa justamente essa potência dissipada.

Guarda bem esse aparato, porque a gente não vai trocar de experimento daqui a pouco.

É essa mesma barra que vamos entender primeiro pelas forças, depois pelo fluxo magnético e, por último, pelo balanço completo de energia.

### N02 — convenções e modelo

Antes de fazer conta, vamos combinar os sentidos.

A direção horizontal positiva aponta para a direita. A vertical positiva aponta para cima. E a terceira direção sai da tela, em direção a quem está assistindo.

As cruzinhas representam um campo magnético uniforme entrando na tela.

A barra se move para a direita.

A distância entre os trilhos é o comprimento ativo da barra.

E, no nosso modelo, a resistência elétrica fica concentrada naquele resistor. A resistência da barra e dos trilhos será desprezada.

Também vamos desprezar o atrito mecânico.

São simplificações importantes. Elas deixam a gente enxergar com clareza quem está fazendo o quê no balanço de forças e de energia.

### N03 — a barra carrega os portadores

Vamos aproximar a barra.

Esses marcadores positivos representam cargas positivas de prova e, junto com elas, o sentido convencional da corrente.

Não estamos dizendo que os portadores reais de um metal são cargas positivas. Estamos escolhendo uma representação que deixa os sentidos mais fáceis de acompanhar.

Agora repara numa primeira coisa.

A barra inteira se move para a direita.

Então os portadores dentro dela também são carregados para a direita simplesmente porque fazem parte do material.

Ou seja: antes mesmo de falar em corrente, existe uma velocidade associada ao movimento da própria barra.

### N04 — a força associada ao movimento da barra

Escolhe uma carga positiva de prova.

Vamos olhar primeiro a parcela da força magnética associada ao movimento da barra.

Ela é a carga multiplicada pelo produto vetorial entre a velocidade da barra e o campo magnético.

A velocidade aponta para a direita.

O campo magnético entra na tela.

Pela regra da mão direita, o produto vetorial aponta para cima.

Então essa parcela da força magnética empurra a carga positiva para cima, ao longo da barra.

E esse sentido vai aparecer novamente daqui a pouco como o sentido da corrente convencional.

### N05 — força eletromotriz de movimento

Agora queremos medir o efeito dessa força ao longo de todo o circuito.

Para isso, não integramos simplesmente uma força. Usamos a força por unidade de carga e calculamos sua circulação ao redor do caminho fechado.

Essa quantidade é a força eletromotriz.

E aqui vale uma observação porque o nome é meio traiçoeiro: força eletromotriz não é uma força medida em newtons.

Ela é energia por unidade de carga.

A unidade é volt, que equivale a joule por coulomb.

No caso da força eletromotriz de movimento, aparece o produto vetorial entre a velocidade do material do circuito e o campo magnético.

E olha o que simplifica nosso problema: os trilhos e o resistor estão parados.

A única parte do circuito com velocidade é a barra.

Além disso, velocidade e campo são perpendiculares e têm módulos constantes ao longo dela.

Então a integral se reduz a campo magnético vezes comprimento ativo da barra vezes velocidade da barra.

Essa é a força eletromotriz produzida pelo movimento.

### N06 — fechando o circuito

Com o circuito fechado, a força eletromotriz estabelece uma corrente.

As cargas se redistribuem pelo condutor e aparece também um campo elétrico interno ao longo das partes estacionárias do circuito, responsável por manter o movimento dos portadores nesses trechos.

No modelo resistivo que estamos usando, a corrente é a força eletromotriz dividida pela resistência total.

Então substituímos o resultado anterior.

A corrente é o campo magnético vezes o comprimento da barra vezes a velocidade da barra, tudo dividido pela resistência.

E o sentido convencional é este: sobe pela barra, segue para a esquerda no trilho superior, desce pelo resistor e volta pelo trilho inferior.

Anti-horário.

### N07 — dissipação

Agora a corrente atravessa o resistor.

A potência dissipada nele é a resistência multiplicada pela corrente ao quadrado.

Como a resistência é positiva e a corrente aparece ao quadrado, essa potência é positiva.

O brilho laranja vai representar essa potência instantânea.

Não é uma simulação da temperatura real do resistor. A gente não está calculando aquecimento, resfriamento ou capacidade térmica.

É só um código visual: mais potência, mais destaque.

Guarda isso porque, quando a barra começar a desacelerar, esse brilho também vai mudar.

### N08 — duas velocidades diferentes

Agora vem uma distinção importante.

A velocidade da barra não é a velocidade completa de um portador.

O portador acompanha o movimento do material para a direita.

Mas, além disso, por causa da corrente, ele tem uma velocidade média em relação ao próprio material: a velocidade de deriva.

Na nossa representação com cargas positivas, essa deriva aponta para cima na barra.

Então a velocidade total do portador é a soma dessas duas contribuições: o movimento da barra mais a deriva em relação à barra.

É essa velocidade total que entra na força magnética completa sobre a carga.

### N09 — por que o campo não realiza trabalho

A força magnética completa sobre o portador é a carga multiplicada pelo produto vetorial entre a velocidade total do portador e o campo magnético.

E uma propriedade do produto vetorial é justamente produzir um vetor perpendicular à velocidade.

Por isso, o produto escalar entre a força magnética e a velocidade total é zero.

E força em produto escalar com velocidade é potência.

Então a potência da força magnética sobre a carga é zero.

O campo magnético não aumenta nem diminui diretamente a energia cinética da carga.

Ele desvia o movimento.

Guarda esse detalhe: aqui usamos a velocidade total do portador, e não somente a velocidade da barra.

### N10 — o paradoxo

Agora coloca as duas coisas lado a lado.

No resistor: potência dissipada maior que zero.

Na carga: potência da força magnética igual a zero.

As duas afirmações estão corretas.

Então... de onde vem a energia?

Esse é o coração do vídeo.

Para responder, até agora está faltando um personagem na nossa história.

Quem está puxando a barra?

### N11 — arrasto magnético sobre a barra

Vamos parar de olhar uma carga isolada e olhar a barra inteira.

Existe corrente subindo pela barra.

E um condutor com corrente dentro de um campo magnético sofre uma força.

A direção vem do produto vetorial entre o vetor comprimento da barra e o campo magnético.

O vetor comprimento acompanha a corrente e aponta para cima.

O campo entra na tela.

O produto vetorial aponta para a esquerda.

Então a força magnética sobre a barra é contrária ao movimento.

É um arrasto.

Como os vetores são perpendiculares, o módulo dessa força é corrente vezes comprimento da barra vezes campo magnético.

### N12 — alguém está puxando

Mas a barra está andando com velocidade constante.

Se existe uma força magnética para a esquerda e a velocidade não muda, alguma outra força precisa equilibrar esse arrasto.

Ela é a força externa.

Mesmo módulo, sentido oposto.

Para a direita.

Em outras palavras: tem alguém puxando essa barra.

E esse alguém não está ali só para decoração.

Ele é quem vai pagar a conta de energia.

### N13 — quem paga a conta

Vamos calcular a potência fornecida por quem puxa.

Como a força externa e a velocidade apontam para o mesmo sentido, a potência externa é o módulo da força multiplicado pela velocidade da barra.

Substituímos a força externa pelo módulo da força magnética.

Aparece corrente vezes comprimento vezes campo magnético vezes velocidade.

Agora agrupamos campo magnético, comprimento e velocidade.

Mas esse produto a gente já conhece.

É a força eletromotriz de movimento.

Então a potência externa vira corrente vezes força eletromotriz.

E, usando a relação resistiva do circuito, isso vira corrente ao quadrado vezes resistência.

Exatamente a potência dissipada no resistor.

Pronto.

A potência fornecida mecanicamente por quem puxa é igual à potência dissipada.

O campo magnético entra no acoplamento, mas ele não é uma fonte de energia.

Ele faz a ponte.

Quem puxa paga a conta.

E isso também resolve aquela aparente contradição.

A força magnética total não realiza trabalho sobre uma carga individual, mas ela acopla o movimento macroscópico da barra à deriva dos portadores e produz uma força de reação sobre o condutor.

Para manter a barra em movimento, o agente externo precisa fazer trabalho.

É essa energia mecânica que termina sendo dissipada no resistor.

### N14 — a mesma física, agora pelo fluxo

Até aqui entendemos de onde vem a energia quando a velocidade é mantida constante.

Agora vamos olhar o mesmo fenômeno de outro jeito.

Mesmo aparato.

Mesma barra.

Só muda a descrição.

Vamos prestar atenção na área do circuito.

Se a distância horizontal entre o lado fixo e a barra é a distância indicada na tela, a área é o comprimento da barra multiplicado por essa distância.

Quando a barra avança, essa distância aumenta.

Então a área aumenta.

### N15 — orientação e fluxo

Para definir o fluxo magnético com sinal, precisamos orientar a superfície.

Vamos escolher o circuito no sentido anti-horário.

Pela regra da mão direita, isso define uma normal apontando para fora da tela.

Só que o nosso campo magnético aponta para dentro.

Campo e normal estão em sentidos opostos.

Por isso, o produto escalar entre eles é negativo.

Como o campo é uniforme, o fluxo magnético é menos o módulo do campo multiplicado pela área.

E substituindo a área, fica menos campo magnético vezes comprimento da barra vezes distância.

O sinal não apareceu por capricho.

Ele nasceu da orientação que acabamos de escolher.

### N16 — variando o fluxo

Agora a barra anda.

A taxa de variação daquela distância horizontal é exatamente a velocidade da barra.

Então, derivando o fluxo no tempo, campo e comprimento permanecem constantes e sobra: menos campo vezes comprimento vezes velocidade.

Repara numa coisa que costuma confundir.

A área está aumentando.

Mas o fluxo está ficando mais negativo.

Isso não é contradição.

A área aumenta em módulo, enquanto o sinal do fluxo depende da orientação entre campo e normal.

### N17 — algo conhecido apareceu

Agora compara.

A força eletromotriz que encontramos pela força de Lorentz era campo vezes comprimento vezes velocidade.

A derivada do fluxo é menos esse mesmo produto.

Então uma expressão é o negativo da outra.

A gente não inventou uma fórmula nova.

A mesma física começou a aparecer com outra linguagem.

### N18 — regra do fluxo

E chegamos a: a força eletromotriz é igual a menos a taxa de variação do fluxo magnético.

Essa é a regra do fluxo neste problema.

E presta atenção no contexto.

O campo magnético continua estacionário.

Ele não está mudando no tempo.

O fluxo muda porque o circuito está mudando de geometria.

A barra se move, a área muda e, com ela, muda o fluxo.

Mais adiante a gente vai encontrar outro mecanismo para mudar o fluxo.

Mas não ainda.

### N19 — será que depende do retângulo?

Tem uma pergunta natural agora.

Será que essa relação só funcionou porque escolhemos um retângulo bonitinho?

Vamos trocar o contorno por uma forma qualquer.

Ele continua fechado.

Mantemos uma orientação para o percurso e a normal correspondente.

E agora cada pedacinho do circuito pode ter sua própria velocidade local.

Alguns podem se mover mais, outros menos e alguns podem até ficar parados.

### N20 — faixa varrida

Compara o contorno em dois instantes muito próximos.

Aqui ele está num instante.

E aqui, um intervalo de tempo depois.

Entre as duas posições aparece uma faixa fininha.

Essa é a superfície varrida pelo movimento do contorno naquele intervalo.

Como o campo magnético continua estacionário, é essa mudança de superfície que produz a mudança de fluxo.

### N21 — construindo um elemento da faixa

Vamos ampliar só um pedacinho.

Temos um pequeno elemento de comprimento orientado ao longo do contorno.

Durante um pequeno intervalo de tempo, esse pedacinho se desloca.

O deslocamento é a velocidade local multiplicada pelo intervalo de tempo.

Agora olha para os dois vetores.

O deslocamento e o elemento de comprimento formam um pequeno paralelogramo.

O elemento vetorial de área dessa faixa vem do produto vetorial entre o deslocamento e o elemento de comprimento.

Substituindo o deslocamento, aparece o produto vetorial entre velocidade e elemento de comprimento, multiplicado pelo intervalo de tempo.

### N22 — conferindo o sinal antes da álgebra

Antes de sair manipulando símbolos, vamos conferir se essa orientação faz sentido no caso que já conhecemos.

Na barra, o elemento de comprimento aponta para cima.

A velocidade aponta para a direita.

Velocidade em produto vetorial com elemento de comprimento aponta para fora da tela.

Então o elemento de área da faixa aponta para fora.

Mas o campo magnético entra na tela.

Logo, campo em produto escalar com esse elemento de área é negativo.

Ótimo.

O sinal já está na geometria.

A álgebra agora só precisa respeitar isso.

### N23 — somando a faixa

Voltamos para o contorno inteiro.

Para encontrar a variação total do fluxo, somamos as contribuições de todos esses pequenos elementos da faixa.

Dividimos pelo intervalo de tempo e tomamos o limite.

O resultado é uma integral ao redor do contorno.

Dentro dela aparece o campo magnético em produto escalar com velocidade em produto vetorial com elemento de comprimento.

A conta está simplesmente somando, ao redor de todo o circuito, quanto cada pedaço contribui para a superfície varrida.

### N24 — de onde nasce o sinal de menos

Agora temos um produto misto.

Uma identidade do produto escalar triplo permite reorganizar esses vetores sem mudar o valor.

Podemos escrever o produto entre campo, velocidade e elemento de comprimento numa ordem equivalente em que aparece campo em produto vetorial com velocidade, em produto escalar com o elemento de comprimento.

Mas a força eletromotriz usa a ordem oposta: velocidade em produto vetorial com campo.

E inverter os fatores de um produto vetorial troca o sinal.

É exatamente daí que aparece o sinal de menos nessa passagem.

Não é um sinal decorativo.

É orientação.

### N25 — reconhecendo a força eletromotriz

Depois dessa reorganização, a integral que aparece é justamente a circulação da força magnética de movimento por unidade de carga.

Ou seja: a força eletromotriz de movimento.

Então a taxa de variação do fluxo é menos a força eletromotriz.

Ou, escrevendo do jeito mais conhecido: a força eletromotriz é menos a taxa de variação do fluxo magnético.

E agora não foi só para o retângulo.

A gente mostrou a estrutura para um contorno móvel geral, dentro de um campo magnético estacionário.

### N26 — voltamos para os trilhos

Beleza.

Agora volta comigo para a barra.

Mesmos trilhos.

Mesmo resistor.

Mesmo campo magnético.

A barra ainda está sendo puxada.

Existe corrente, existe força magnética de arrasto e existe uma força externa compensando esse arrasto.

Até aqui, tudo conhecido.

Agora vamos mudar uma única coisa.

### N27 — e se ninguém continuar puxando?

E se a gente simplesmente soltar a barra?

Nesse instante, ela ainda possui uma velocidade inicial.

A força externa desaparece.

E a gente vai congelar a imagem exatamente aqui.

O experimento fica parado visualmente no instante da soltura enquanto a matemática descobre o que acontecerá depois.

Também entra uma hipótese importante.

Vamos desprezar a autoindutância do circuito.

Ou seja: no nosso modelo, a corrente acompanha instantaneamente a força eletromotriz pela relação resistiva.

Se a autoindutância fosse importante, apareceria uma dinâmica adicional para a corrente.

Não é o problema que queremos resolver agora.

### N28 — a corrente não desaparece

Soltar a barra não faz a velocidade virar zero instantaneamente.

Ela ainda está se movendo.

Então ainda existe força eletromotriz de movimento.

Se ainda existe força eletromotriz, continua existindo corrente.

E, se ainda existe corrente na barra dentro do campo, continua existindo força magnética de arrasto.

Só que agora ninguém está compensando essa força.

Então a barra vai desacelerar.

### N29 — força em função da velocidade

Vamos escrever isso.

Na direção horizontal, a força é negativa porque aponta para a esquerda.

O módulo da força magnética é corrente vezes comprimento da barra vezes campo magnético.

Agora substituímos a corrente.

Ela é campo magnético vezes comprimento vezes velocidade, dividido pela resistência.

Juntando os fatores, a força fica igual a menos campo magnético ao quadrado vezes comprimento ao quadrado, dividido pela resistência, multiplicando a velocidade.

Isso já conta uma história.

A força de arrasto é proporcional à velocidade.

Quanto mais a barra desacelera, menor fica a própria força que está freando a barra.

### N30 — equação do movimento

Agora entra a segunda lei de Newton.

Massa vezes taxa de variação da velocidade é igual à força resultante.

Substituindo a força que acabamos de encontrar, a taxa de variação da velocidade fica negativa e proporcional à própria velocidade.

Não é um exercício novo.

É exatamente a mesma barra do começo, só que agora ninguém está puxando.

Vamos resolver essa equação.

### N31 — separando as variáveis

Primeiro dividimos pela massa e pela velocidade.

Depois multiplicamos pelo diferencial de tempo.

De um lado fica o diferencial da velocidade dividido pela velocidade.

Do outro fica menos campo magnético ao quadrado vezes comprimento ao quadrado, dividido por massa vezes resistência, multiplicando o diferencial de tempo.

Agora as grandezas que variam estão separadas.

Velocidade de um lado.

Tempo do outro.

Então podemos integrar.

### N32 — usando a condição inicial

Na integral da velocidade, começamos na velocidade inicial e terminamos na velocidade do instante que queremos estudar.

No tempo, começamos em zero e vamos até esse mesmo instante.

A integral do diferencial da velocidade dividido pela velocidade produz um logaritmo natural.

Então aparece o logaritmo da velocidade atual dividida pela velocidade inicial.

Do outro lado, campo, comprimento, massa e resistência são parâmetros constantes.

A integral do diferencial de tempo produz simplesmente o tempo decorrido.

### N33 — nasce a constante de tempo

Agora olha para o coeficiente que multiplica o tempo.

Ele tem unidade de inverso de tempo.

Então é conveniente definir o inverso dele como uma constante de tempo.

Essa constante, que vamos chamar de tau, é massa vezes resistência divididas por campo magnético ao quadrado vezes comprimento ao quadrado.

Com essa definição, a equação fica muito mais transparente.

O logaritmo da razão entre as velocidades é igual a menos o tempo dividido pela constante de tempo.

Agora aplicamos a exponencial aos dois lados.

A exponencial desfaz o logaritmo.

E, finalmente, multiplicamos pela velocidade inicial.

Resultado: a velocidade da barra é a velocidade inicial multiplicada por uma exponencial decrescente.

### N34 — o que tau quer dizer

Antes de soltar a animação, vamos entender esse resultado.

Depois de um intervalo igual a uma constante de tempo, a velocidade caiu para cerca de trinta e sete por cento do valor inicial.

É um sobre o número de Euler.

Uma constante de tempo maior significa um decaimento mais lento.

Uma constante de tempo menor significa que a barra perde velocidade mais rapidamente.

E a curva se aproxima continuamente de zero.

No nosso modelo ideal, ela não chega exatamente a zero em um tempo finito.

Isso depende das hipóteses que escolhemos: sem atrito mecânico e com autoindutância desprezível.

### N35 — agora deixa a física andar

Agora sim: soltamos o relógio.

À esquerda, a barra evolui no tempo.

À direita, o gráfico mostra a velocidade dividida pela velocidade inicial.

O mesmo tempo controla os dois.

A barra continua andando para a direita, mas cada vez menos durante intervalos iguais.

E o ponto no gráfico acompanha exatamente essa desaceleração.

Não são duas histórias.

É a mesma soltura representada de duas maneiras.

### N36 — a corrente acompanha a velocidade

Vamos repetir exatamente a mesma soltura, agora olhando para a corrente.

No instante inicial, a corrente é campo magnético vezes comprimento vezes velocidade inicial, dividido pela resistência.

Como campo, comprimento e resistência são constantes, a corrente é proporcional à velocidade.

Então, se a velocidade decai exponencialmente, a corrente também.

Com a mesma constante de tempo.

A corrente é a corrente inicial multiplicada pela mesma exponencial decrescente.

E isso vale porque estamos dentro daquela aproximação de autoindutância desprezível.

### N37 — duas grandezas, a mesma curva

Agora normalizamos.

Dividimos a velocidade pelo valor inicial.

E dividimos a corrente pelo valor inicial.

As duas razões começam em um.

E as duas seguem exatamente a mesma exponencial.

Por isso as curvas coincidem.

Isso não significa que velocidade e corrente sejam a mesma coisa.

Significa que, relativamente aos seus próprios valores iniciais, elas caem na mesma proporção.

### N38 — potência cai mais rápido

Agora entra a potência.

A potência inicial é a resistência multiplicada pela corrente inicial ao quadrado.

E, como a potência depende do quadrado da corrente, quando elevamos a exponencial da corrente ao quadrado, o expoente dobra.

Então a potência cai com uma exponencial que tem menos duas vezes o tempo dividido pela constante de tempo.

Repara no gráfico.

A curva laranja desce mais rápido.

E agora o marcador acompanha justamente a potência.

O resistor também perde destaque mais rapidamente porque o brilho está representando essa potência instantânea.

### N39 — um tau depois

Vamos olhar um instante concreto.

Depois de uma constante de tempo, a corrente está em aproximadamente trinta e sete por cento do valor inicial.

Mas a potência já caiu para aproximadamente catorze por cento.

Porque ela depende da corrente ao quadrado.

É o quadrado aparecendo na imagem.

### N40 — de potência para energia

Agora queremos saber quanta energia foi dissipada no total.

Energia é a integral da potência no tempo.

Mas tem uma sutileza no gráfico.

O eixo vertical não mostra a potência em watts.

Ele mostra a potência dividida pela potência inicial.

Então a área sob essa curva normalizada tem unidade de tempo.

Ela ainda não é energia.

Para virar energia, precisamos multiplicar essa área pela potência inicial.

Potência vezes tempo dá energia.

Watt vezes segundo dá joule.

Enquanto a região sombreada cresce até um instante qualquer, ela representa a energia já dissipada dividida pela potência inicial.

No limite de tempo infinito, obtemos a área total.

### N41 — escrevendo a integral

Vamos colocar isso na conta.

A potência instantânea é a potência inicial multiplicada pela exponencial de menos duas vezes o tempo dividido pela constante de tempo.

A potência inicial não depende do tempo.

Então ela pode sair da integral.

E também vamos precisar escrever essa potência inicial usando os parâmetros do nosso sistema.

Ela é campo magnético ao quadrado vezes comprimento ao quadrado vezes velocidade inicial ao quadrado, dividido pela resistência.

A mesma expressão aparece se começarmos pela corrente inicial ao quadrado vezes a resistência.

### N42 — fazendo a integral

Agora calculamos a integral da exponencial.

Uma primitiva é menos a constante de tempo dividida por dois, multiplicando a própria exponencial.

Quer conferir?

Se a gente derivar, o menos dois dividido pela constante de tempo que vem do expoente cancela exatamente o fator da frente.

Voltamos ao integrando.

Agora avaliamos entre zero e o limite de tempo infinito.

No infinito, a exponencial tende a zero.

Em zero, ela vale um.

Então sobra a constante de tempo dividida por dois.

Portanto, a energia dissipada total é a potência inicial multiplicada pela constante de tempo dividida por dois.

### N43 — os cancelamentos

Agora vem uma parte bem bonita.

Vamos substituir a potência inicial e a constante de tempo.

A potência inicial traz campo magnético ao quadrado, comprimento ao quadrado e velocidade inicial ao quadrado, divididos pela resistência.

A constante de tempo traz massa vezes resistência, divididos por campo magnético ao quadrado vezes comprimento ao quadrado.

Organizamos tudo sem perder a igualdade completa.

O que vai sobreviver?

Um meio.

A massa.

E a velocidade inicial ao quadrado.

O restante aparece em razões.

Resistência dividida por resistência: um.

Campo magnético ao quadrado dividido pelo próprio campo magnético ao quadrado: um.

Comprimento ao quadrado dividido pelo próprio comprimento ao quadrado: um.

Então resta: um meio vezes massa vezes velocidade inicial ao quadrado.

E olha o que isso está dizendo.

Campo magnético, comprimento e resistência influenciam a constante de tempo.

Ou seja, influenciam quão rápido a energia é dissipada.

Mas eles não determinam quanta energia a barra possuía inicialmente.

### N44 — reconhecendo a energia

E um meio vezes massa vezes velocidade inicial ao quadrado tem um nome conhecido.

Energia cinética inicial.

Então, quando o tempo tende ao infinito, toda a energia dissipada no resistor é igual à energia cinética que a barra tinha no instante em que foi solta.

Não apareceu energia do nada.

Depois da soltura, ninguém realizou mais trabalho externo sobre a barra.

Ela simplesmente foi perdendo a energia cinética que já possuía.

E essa energia terminou dissipada no resistor.

### N45 — caso um: velocidade imposta

Agora dá para colocar os dois regimes lado a lado.

Primeiro, quando mantemos a velocidade constante.

Existe uma força externa compensando o arrasto.

A energia cinética da barra não muda.

E a potência fornecida externamente é igual à potência dissipada no resistor.

Nesse regime, a energia vem continuamente de quem puxa.

### N46 — caso dois: barra livre

Agora soltamos a barra.

No começo, toda a energia disponível está na forma de energia cinética.

Nada ainda foi dissipado.

Conforme o tempo passa, a parcela cinética diminui e a energia já dissipada aumenta.

Mas a soma permanece constante.

Em qualquer instante: energia cinética atual mais energia já dissipada é igual à energia cinética inicial.

E tem um detalhe importante.

Em qualquer tempo finito do nosso modelo, ainda resta alguma energia cinética.

É somente no limite em que o tempo tende ao infinito que essa parcela vai a zero e a energia dissipada tende à energia cinética inicial inteira.

A coluna não está criando nem destruindo energia.

Ela só mostra a mesma quantidade sendo redistribuída.

### N47 — finalmente respondendo à pergunta

Agora podemos voltar à pergunta do começo.

Se a barra está sendo puxada com velocidade constante, de onde vem a energia dissipada?

Do trabalho realizado por quem puxa.

A igualdade entre potência externa e potência dissipada mostra isso diretamente.

Não existe uma fonte escondida de energia dentro do campo magnético.

### N48 — qual é, então, o papel do campo?

E quando soltamos a barra?

A energia vem da energia cinética que ela já tinha.

Então qual é o papel do campo magnético?

O campo fornece o acoplamento entre o movimento mecânico da barra e a corrente no circuito.

Ele permite que o movimento produza força eletromotriz, corrente e arrasto.

Mas ele não fornece a energia.

Esse é o fechamento da história.

Com velocidade imposta: trabalho externo vira energia dissipada.

Com a barra livre: energia cinética inicial vira energia dissipada.

E, nos dois casos, o balanço fecha.

### N49 — encerramento

E é isso, pessoal.

Hoje a gente começou com uma barra andando sobre dois trilhos e conseguiu ligar três descrições que muitas vezes aparecem separadas nos livros: a força sobre as cargas, a regra do fluxo magnético, e a conservação da energia.

Se esse tipo de conexão te ajuda a entender o que existe por trás das fórmulas, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

E agora fica uma pergunta.

Hoje o campo magnético ficou estacionário e quem mudou foi o circuito.

Mas e se acontecer o contrário?

E se o circuito ficar parado e o campo magnético mudar no tempo?

Aí surge uma física nova na nossa história: o campo elétrico induzido.

É o próximo passo: lei de Faraday e campo magnético variável.

Até a próxima!
