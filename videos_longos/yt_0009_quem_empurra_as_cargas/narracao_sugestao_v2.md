# yt_0009 — Quem empurra as cargas? — sugestão de narração (v2)

Regra desta versão: a narração determina a duração e a animação se molda a ela. Sem meta de palavras. Cada frase precisa avançar a física, justificar uma transformação, interpretar o que aparece ou ligar duas ideias; o que só repetia saiu, e onde a construção pede tempo (Ohm, cena central, regime estacionário, fonte e FEM) ela ganhou fala. Estilo professor de cursinho, variáveis pelo nome (o símbolo é apresentado uma vez, junto do nome). Física corrigida em relação à v1: sem "corrente igual em todo lugar" no gancho; deriva sem número fixo; R como parâmetro efetivo do modelo ôhmico; resistência (não "seção menor") explicando a queda no resistor; carga superficial sem neutralidade volumétrica categórica; sem "atraso" físico entre E e J (a ordem é didática); J muda com a área, só a corrente total é igual nas seções em série; carga de prova positiva na fonte; FEM com interpretação energética restrita à fonte estacionária.

## B00–B01 · Gancho e título

N001 Olha este circuito. A bateria está aqui, deste lado. Agora acompanha o fio até este ponto, bem longe dela.

N002 Se existe uma carga aqui, que força está agindo sobre ela, agora? Não pode ser a bateria puxando essa carga à distância. Então, quem empurra as cargas?

N003 Bem-vindos ao Parallax Lab. Neste vídeo, a gente responde a essa pergunta passando pela Lei de Ohm e pela força eletromotriz.

N004 O caminho tem três perguntas encaixadas. Primeiro: que força age, localmente, sobre cada carga do fio? Depois: quem estabelece o campo elétrico ao longo do circuito inteiro? E, por fim: quem repõe a energia que o resistor dissipa?

N005 Vamos mergulhar no fio e começar pela primeira.

## B02 · Condução local

N006 Por dentro, um metal é uma rede de íons fixos, com elétrons livres passeando entre eles. Sem campo, esses elétrons se movem para todos os lados, colidem, mudam de rumo, tudo de forma desordenada. Em média, ninguém vai a lugar nenhum.

N007 Agora, neste trecho do fio, existe um campo elétrico: é a seta ciano. E é esse campo que age, localmente, sobre cada portador de carga. Repara na palavra localmente. A carga não precisa saber onde está a bateria; ela só sente o campo que existe exatamente onde ela está.

N008 A força sobre um portador é a carga dele vezes o campo elétrico. Para um elétron, a carga é negativa: menos e, onde e é o valor da carga elementar. Então a força sobre o elétron aponta contra o campo.

N009 Mas o que a gente vê não é uma fila de elétrons disparando pelo fio. Eles continuam desordenados. O campo só acrescenta, por cima da bagunça, uma velocidade média, a velocidade de deriva, no sentido oposto ao campo. A marca violeta mostra isso: o conjunto escorrega, mas escorrega pouco.

N010 Essa deriva é pequena perto do movimento microscópico, porque o elétron anda um pedacinho, colide com um íon, perde o rumo e recomeça. O campo empurra, as colisões embaralham, e o saldo médio é lento. Quão lento depende da corrente, da quantidade de portadores e da seção do fio; em situações usuais, fica entre frações de milímetro e milímetros por segundo.

N011 Em escala maior, essa deriva vira corrente. A densidade de corrente, que aparece na tela como a letra J, é o número de portadores por volume, vezes a carga de cada um, vezes a velocidade de deriva.

N012 Repara no sinal. Para elétrons, a carga é negativa, então a deriva é oposta ao campo, mas a densidade de corrente aponta no mesmo sentido do campo. As duas ficam paralelas, e é por isso que a corrente convencional é desenhada no sentido do campo.

N013 Agora uma definição que vai nos acompanhar o vídeo inteiro: a força por unidade de carga, que vamos chamar de f minúsculo, é a força dividida pela carga. No trecho de um resistor comum, ela é simplesmente o campo elétrico.

N014 E o material responde de um jeito simples, no modelo ôhmico: a densidade de corrente é a condutividade vezes a força por carga. Aqui, a condutividade vezes o campo elétrico. Pensa no cobre e na borracha: com o mesmo campo, o cobre tem uma densidade de corrente enorme e a borracha, quase nenhuma. Quem faz essa diferença é a condutividade.

N015 Guarda essa relação, porque ela já carrega dentro dela a Lei de Ohm que a gente conhece.

## B03 · O fio visto de longe

N016 Vamos afastar a câmera e olhar para o mesmo fio como um cilindro: um comprimento, que na tela é a letra L, e uma seção transversal com uma área, a letra A. Uma corrente, I, entra por uma ponta.

N017 Primeiro, a corrente. Ela é a soma da densidade de corrente que atravessa a seção. Se a densidade for uniforme, a conta é direta: a corrente é a densidade de corrente vezes a área. Isolando, a densidade de corrente é a corrente dividida pela área.

N018 Repara no que a gente fez: trocamos uma grandeza local, a densidade de corrente, por uma grandeza do fio inteiro, a corrente. Isso só funciona porque assumimos densidade uniforme na seção, uma boa aproximação para um fio comum com corrente contínua.

N019 Agora, o campo. A queda de potencial entre as duas pontas é a integral do campo ao longo do fio. Com campo uniforme e paralelo ao caminho, isso vira o campo vezes o comprimento. Chamando de V o módulo dessa queda de potencial, o campo é V dividido pelo comprimento.

N020 Resumindo, três relações sobre o mesmo fio. A densidade de corrente é a corrente dividida pela área. O campo é a queda de potencial dividida pelo comprimento. E a densidade de corrente é a condutividade vezes o campo.

N021 As duas primeiras são geométricas, falam do fio inteiro. A terceira é local, vale em cada ponto. O que a gente vai fazer agora é juntar as três.

## B04 · De J igual sigma E até V igual R I

N022 Começa pela relação do material: a densidade de corrente é a condutividade vezes o campo.

N023 Agora olha o que acontece. No lugar da densidade de corrente, entra a corrente dividida pela área, porque foi isso que a gente deduziu. E no lugar do campo, entra a queda de potencial dividida pelo comprimento.

N024 Fica assim: a corrente dividida pela área é igual à condutividade vezes a queda de potencial dividida pelo comprimento. Nada de novo, só substituição.

N025 Agora é álgebra, uma operação de cada vez. Multiplicando os dois lados pelo comprimento e pela área, a corrente vezes o comprimento passa a ser igual à condutividade vezes a área vezes a queda de potencial.

N026 Isolando a queda de potencial: a corrente, vezes o comprimento dividido pela condutividade vezes a área.

N027 Repara neste bloco: comprimento dividido por condutividade vezes área. Ele junta o material, por causa da condutividade, e a geometria, por causa do comprimento e da área. E, no modelo ôhmico linear, com material, geometria e temperatura fixos, ele não depende nem da corrente nem da queda de potencial.

N028 Esse bloco tem nome: é a resistência desse trecho de fio, um parâmetro macroscópico efetivo. Agora a Lei de Ohm aparece sozinha: a queda de potencial é a resistência vezes a corrente.

N029 Ou seja, a Lei de Ohm não caiu do céu. Ela nasce da lei local mais a geometria. E dá para ler a resistência com os olhos: mais comprimento, mais resistência; mais área, menos resistência; mais condutividade, menos resistência.

N030 A unidade também fecha: resistência é volt por ampère, e a esse quociente a gente chama de ohm.

N031 Olha como isso se aplica ao circuito. Nos fios, a resistência é muito pequena, então, para a mesma corrente, o potencial cai pouco. No resistor, a resistência é muito maior, então é nele que cai quase toda a queda de potencial.

## B05 · A segunda pergunta

N032 Voltando ao circuito inteiro: o campo existe em todo trecho, pequeno nos fios, grande no resistor. A fita azul mostra o potencial ao longo do caminho. Ele cai pouco nos fios, cai muito no resistor e sobe de novo dentro da fonte.

N033 O campo, na direção do fio, é a inclinação dessa fita. Mas isso levanta uma pergunta ainda melhor: quem estabelece esse campo ao longo do circuito inteiro?

## B06 · Conservação de carga

N034 Para responder, a gente precisa de uma ideia: a carga se conserva. Imagina um volume pequeno dentro do fio. Se entra mais corrente do que sai, a carga dentro dele só pode aumentar.

N035 Em forma local, isso é a equação da continuidade: a variação, no tempo, da densidade de carga, mais o divergente da densidade de corrente, é igual a zero. O divergente é um saldo local do fluxo: quanta corrente sai de um ponto menos quanta entra.

N036 Se esse saldo é positivo, sai mais do que entra, e a carga ali diminui. Se é negativo, a carga aumenta. A equação diz exatamente isso.

N037 Vamos integrar a equação no volume. A primeira parcela é a integral da variação da densidade de carga. A segunda, a integral do divergente da densidade de corrente.

N038 Agora o teorema da divergência entra em cena. A integral do divergente, no volume, é igual ao fluxo da densidade de corrente pela superfície que fecha o volume.

N039 A integral da densidade de carga é a carga que está dentro do volume. Então temos: a variação da carga no tempo, mais o fluxo pela superfície, igual a zero.

N040 E o fluxo pela superfície, aqui, são só as duas faces: sai uma corrente, entra outra. No fim, a variação da carga no tempo é a corrente que entra menos a corrente que sai. É exatamente a contabilidade que a gente imaginou.

## B07 · A cena central

N041 Agora vem a parte mais importante, então vamos devagar, uma coisa de cada vez. A ordem que você vai ver é uma ordem didática: a gente separa os passos para enxergar a causa e a consequência.

N042 Suponha que, por um instante, entre mais corrente do que sai desse trecho. Repara nas duas setas verdes: a de entrada é maior que a de saída.

N043 Então a carga dentro do volume aumenta: a variação da carga no tempo é positiva. O medidor azul mostra isso. É só contabilidade: o que entra e não sai fica guardado, porque a carga não surge nem desaparece.

N044 E onde essa carga fica? Num bom condutor, a redistribuição que importa aqui aparece principalmente como uma pequena quantidade de carga na superfície, na casca do condutor, e não como um fluido enchendo o volume inteiro.

N045 Essas cargas na superfície mudam o potencial ao redor delas. Olha a curva do potencial se deformando junto do acúmulo.

N046 E o campo, na direção do fio, é menos a derivada do potencial em relação à posição. Então, quando a inclinação do potencial muda, o campo muda. A redistribuição de carga altera o campo de um jeito que reduz o desbalanço entre a corrente que entra e a que sai. Na animação, isso aparece como o campo de entrada diminuindo e o de saída aumentando.

N047 E por que a corrente muda junto? Porque, no material ôhmico, a densidade de corrente é a condutividade vezes o campo. Mudou o campo, muda a densidade de corrente. É por isso que, na tela, primeiro a gente mostra a carga, depois o potencial, depois o campo, e só então a corrente.

N048 Repara como isso funciona como uma autorregulagem. O acúmulo de carga reduz justamente o desbalanço que o criou, e aproxima a corrente que entra da corrente que sai. O sistema se ajusta até o balanço fechar.

N049 Quando a corrente que entra iguala a que sai, a variação da carga fica zero e o acúmulo para. Mas repara: as cargas que se acumularam continuam lá.

## B07b · Do trecho para o circuito todo

N050 Isso não acontece só num ponto. Quando a gente abre a câmera, vê que o circuito inteiro se ajustou: existe uma distribuição de cargas na superfície dos condutores, já estabelecida, que produz, em cada região, o campo que ela precisa.

N051 E não pense nessa distribuição como uma onda de cargas viajando a partir deste ponto. A imagem mostra o estado final: um circuito já estabelecido, com as cargas na superfície no lugar certo para produzir o campo de cada trecho.

N052 A imagem é qualitativa. A quantidade de carga por área depende da geometria: dos cantos, dos terminais, das pontas do resistor. O que importa é a ideia: são essas cargas, espalhadas na superfície, que organizam o campo ao longo do circuito.

N053 Repara no que muda de um trecho para o outro. Num circuito em série, no regime estacionário, a corrente total é a mesma em todas as seções. Mas a densidade de corrente é a corrente dividida pela área, então ela pode mudar quando a área muda.

N054 E o campo local acompanha: ele é a densidade de corrente dividida pela condutividade, ou seja, a corrente dividida pela condutividade vezes a área. Por isso o campo é pequeno nos fios, de condutividade alta, e grande no resistor.

N055 Olha o marcador percorrendo a fita de potencial: o campo na direção do fio é a inclinação, com sinal de menos, do potencial ao longo do caminho. Inclinação suave nos fios, forte no resistor. E quem decide como o potencial cai ao longo do circuito é a distribuição das cargas superficiais.

## B08 · Regime estacionário

N056 Durante o ajuste, a densidade de carga muda no tempo. É a fase de transição.

N057 Quando o ajuste termina, a variação da densidade de carga no tempo é zero. E, pela equação da continuidade, o divergente da densidade de corrente também é zero: tudo o que entra em cada pedacinho sai.

N058 Mas atenção: as cargas na superfície não sumiram. Elas só pararam de se redistribuir. Regime estacionário não é a mesma coisa que ausência de cargas superficiais.

N059 Imagina fotografar o circuito em dois instantes diferentes depois do ajuste: a mesma distribuição de cargas, o mesmo campo, a mesma corrente. Tudo está em movimento, mas nada muda. É isso que estacionário quer dizer.

N060 Vale comparar com uma situação que você já conhece. No equilíbrio eletrostático, o campo elétrico dentro do condutor é zero e não existe corrente.

N061 Já num fio resistivo conduzindo corrente estacionária, o campo dentro do material não é zero. E a densidade de corrente continua sendo a condutividade vezes o campo. Para sustentar corrente num condutor resistivo como esse, é preciso campo, e esse campo é estabelecido pelas cargas na superfície.

N062 Então estacionário não é eletrostático. Um condutor com corrente não está em equilíbrio eletrostático.

## B09 · Quem repõe a energia

N063 Falta a última pergunta. As cargas perdem energia no resistor: ele esquenta. Então quem repõe essa energia?

N064 A fonte. E por que precisa ser algo que não é eletrostático? Porque o campo de cargas estáticas, sozinho, não mantém uma corrente circulando: ao dar uma volta completa, ele devolve tudo o que deu. Sem outra coisa trabalhando, a energia dissipada nunca seria reposta.

N065 Dentro da bateria, além do campo elétrico, existe uma força que não é eletrostática, ligada ao mecanismo da fonte. A gente vai chamar essa força, por unidade de carga, de f s. Aqui a bateria é só um modelo esquemático; não estamos entrando na química.

N066 Repara que os dois coexistem dentro da fonte. O campo elétrico, criado pelas cargas dos terminais, aponta do positivo para o negativo e tenta empurrar a carga para baixo. A força da fonte aponta no sentido oposto, e vence.

N067 Por isso a força total por unidade de carga é o campo elétrico mais a força da fonte. Para enxergar, vamos acompanhar uma carga de prova positiva, o portador convencional. Veja ela subindo, contra a tendência eletrostática: a régua de energia por carga vai crescendo.

## B10 · Força eletromotriz

N068 E é aqui que entra a força eletromotriz. Apesar do nome, ela não é uma força. Ela é definida como a integral, ao longo do circuito fechado, da força por unidade de carga.

N069 Vamos conferir a unidade. Newton por coulomb, vezes metro, é joule por coulomb, que é volt. Neste caso, de uma fonte estacionária, essa integral mede a energia entregue por unidade de carga.

N070 Agora a gente separa a força por carga em duas partes: a do campo elétrico e a da fonte. A força eletromotriz fica sendo a integral do campo mais a integral da força da fonte.

N071 Neste circuito de corrente contínua estacionária, sem indução magnética e sem movimento do circuito, o campo elétrico é conservativo. Então a integral do campo ao redor de uma volta completa é zero.

N072 Acompanha o marcador. Toda vez que a carga percorre um pedaço do circuito, o campo realiza trabalho sobre ela. Ao completar a volta, o trabalho total do campo é nulo. A barra do campo sobe nos fios e no resistor, e dentro da fonte ele contribui com sinal contrário e volta a zero. Já a força da fonte só contribui dentro da bateria, e a barra dela fica no valor da força eletromotriz.

N073 Cancelou o termo do campo, sobra: a força eletromotriz é a integral, ao redor do circuito, da força da fonte. É a fonte realizando trabalho não eletrostático e repondo energia nas cargas. O campo organiza o caminho; quem fornece a energia é a fonte.

## B11 · Energia

N074 E agora a energia fecha. Começa numa escala local: a potência por volume é a densidade de corrente vezes o campo. Na tela, a letra p minúscula.

N075 A potência total no resistor é a integral dessa potência por volume ao longo do resistor inteiro.

N076 Se o resistor é uniforme, a densidade de corrente e o campo são constantes. A integral vira: densidade de corrente vezes campo vezes o volume, que é a área vezes o comprimento.

N077 Agora reagrupa: densidade de corrente vezes área é a corrente, e campo vezes comprimento é a queda de potencial. É a mesma conta, só reagrupada, e a potência é a tensão vezes a corrente.

N078 E com a Lei de Ohm, a queda de potencial é a resistência vezes a corrente. Então a potência é a resistência vezes a corrente ao quadrado.

N079 Do lado da fonte, a potência fornecida é a força eletromotriz vezes a corrente. Num circuito ideal simples, com uma resistência total, a força eletromotriz é a resistência total vezes a corrente.

N080 Substituindo: a potência da fonte é a resistência vezes a corrente ao quadrado, exatamente a potência dissipada no resistor. Em regime estacionário, tudo o que a fonte fornece por segundo, o resistor transforma em calor.

N081 Um aviso: isso é um balanço esquemático. Não existem pacotes de energia viajando dentro dos elétrons.

## B12 · Payoff e encerramento

N082 Então, quem empurra as cargas? A bateria não empurra as cargas de longe.

N083 A fonte fornece energia e mantém a diferença de potencial. As cargas na superfície dos condutores organizam o campo elétrico ao longo de todo o circuito. E esse campo atua, localmente, sobre os portadores e, no material ôhmico, estabelece a densidade de corrente.

N084 Vale guardar estas quatro distinções. A bateria não cria a corrente diretamente em todo lugar. O divergente da corrente ser zero não cria o campo. As cargas superficiais não fornecem a energia. E força eletromotriz não é força.

N085 Cada peça tem um papel diferente, e é justamente essa separação de papéis que explica por que um circuito funciona.

N086 Se isso mudou a sua imagem de um circuito, inscreva-se no Parallax Lab. E conta nos comentários: você já conhecia o papel das cargas superficiais?
