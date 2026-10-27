# yt_0009 — Quem empurra as cargas? — sugestão de narração (v8)

Alvo: 12 a 15 minutos de voz. Esta versão tem 2.449 palavras que, a ~2,85 palavras por segundo (velocidade medida na v6), dão cerca de 14 min 19 s. Mantém a ordem, a física e a didática da v5; corta repetição e reformulações. **Todas as variáveis são ditas pelo nome, nunca pela letra** (regra do projeto, `docs/roteiro_voz_elevenlabs_v4.md`): corrente, densidade de corrente, área, comprimento, queda de potencial, resistência, condutividade, campo elétrico, força por unidade de carga, força da fonte, força eletromotriz, densidade de potência, potência total. Nenhuma letra do alfabeto é lida na fala; só o nome da grandeza.

## B00–B01 · Gancho e título

N001 Olha este circuito. A bateria está aqui, o resistor está do outro lado. Agora acompanha o fio até este ponto, bem longe dos dois. É justamente aqui que aparece o problema.

N002 Se existe uma carga neste trecho e existe corrente passando por aqui, alguma coisa está agindo sobre essa carga neste exato instante. Mas o quê? A bateria não está puxando essa carga de longe. Então, afinal, quem empurra as cargas?

N003 Bem-vindos ao Parallax Lab. Hoje a gente vai responder essa pergunta e, no caminho, entender de onde vem a Lei de Ohm e o que a força eletromotriz realmente significa.

N004 A resposta tem três partes. Primeiro: que força age localmente sobre as cargas dentro do fio? Depois: quem estabelece o campo elétrico ao longo de todo o circuito? E, por fim: se o resistor dissipa energia, quem repõe essa energia?

N005 Quando essas três peças se encaixarem, a Lei de Ohm deixa de parecer uma fórmula decorada e o papel da bateria fica muito mais claro. Vamos começar entrando no próprio fio.

## B02 · Condução local

N006 Por dentro, um metal é uma rede de íons fixos, com elétrons livres passeando entre eles. Sem campo, esses elétrons se movem para todos os lados, colidem, mudam de rumo, tudo de forma desordenada. Em média, ninguém vai a lugar nenhum.

N007 Agora existe um campo elétrico neste trecho: é a seta ciano. E é esse campo que age, localmente, sobre cada portador. A carga não precisa saber onde está a bateria; ela só sente o campo que existe exatamente onde ela está.

N008 A força sobre um portador é a carga dele vezes o campo elétrico. Para um elétron, a carga é negativa, então a força sobre ele aponta contra o campo.

N009 Mas não é uma fila de elétrons disparando pelo fio. Eles continuam desordenados. O campo só acrescenta, por cima da bagunça, uma velocidade média, a velocidade de deriva, no sentido oposto ao campo. A marca violeta mostra isso: o conjunto escorrega, mas escorrega pouco.

N010 Em escala maior, essa deriva vira corrente. A densidade de corrente é o número de portadores por volume, vezes a carga de cada um, vezes a velocidade de deriva. Como a carga do elétron é negativa, a deriva é oposta ao campo, mas a densidade de corrente aponta no mesmo sentido do campo. É por isso que a corrente convencional é desenhada no sentido do campo.

N011 Agora uma definição que vai nos acompanhar o vídeo inteiro: a força por unidade de carga é a força dividida pela carga. No trecho de um resistor comum, ela é simplesmente o campo elétrico.

N012 E o material responde de forma simples, no modelo ôhmico: a densidade de corrente é a condutividade vezes a força por unidade de carga, ou seja, a condutividade vezes o campo elétrico. Guarda essa relação: ela já carrega dentro dela a Lei de Ohm.

## B03 · O fio visto de longe

N013 Vamos afastar a câmera e olhar o fio como um cilindro, com um comprimento e uma área de seção transversal. A corrente entra por uma ponta.

N014 A corrente é o fluxo da densidade de corrente através da seção. Se a densidade for uniforme, a integral fica direta: a corrente é a densidade de corrente vezes a área. Isolando, a densidade de corrente é a corrente dividida pela área. Isso vale como boa aproximação para um fio comum.

N015 Agora o campo. O módulo da queda de potencial entre as duas pontas vem da integral do campo ao longo do fio. Com campo uniforme e paralelo ao caminho, esse módulo é o campo vezes o comprimento. Então o campo é o módulo da queda de potencial dividido pelo comprimento.

N016 Resumindo: a densidade de corrente é a corrente dividida pela área; o campo é a queda de potencial dividida pelo comprimento; e a densidade de corrente é a condutividade vezes o campo. As duas primeiras falam do fio inteiro, a terceira vale em cada ponto. Agora vamos juntar as três.

## B04 · Da lei local até a Lei de Ohm

N017 Começa pela relação do material: a densidade de corrente é a condutividade vezes o campo.

N018 Agora olha o que acontece. No lugar da densidade de corrente entra a corrente dividida pela área. E no lugar do campo entra a queda de potencial dividida pelo comprimento. Nada de novo, só substituição: a corrente dividida pela área é a condutividade vezes a razão entre a queda de potencial e o comprimento.

N019 Agora é álgebra, uma operação de cada vez. Multiplicamos os dois lados pela área vezes o comprimento. Do lado esquerdo sobra a corrente vezes o comprimento; do direito, a condutividade vezes a área vezes a queda de potencial.

N020 Isolando a queda de potencial, ela é a corrente vezes o comprimento, dividida pelo produto da condutividade pela área.

N021 Repara neste bloco: o comprimento dividido pelo produto da condutividade pela área. Ele junta o material e a geometria. E, no modelo ôhmico linear, com material, geometria e temperatura fixos, não depende nem da corrente nem da queda de potencial.

N022 Esse bloco tem nome: é a resistência desse trecho de fio, um parâmetro macroscópico efetivo. E a Lei de Ohm aparece sozinha: a queda de potencial é a resistência vezes a corrente.

N023 A Lei de Ohm não caiu do céu: ela nasce da lei local mais a geometria. Mais comprimento, mais resistência; mais área, menos; mais condutividade, menos. E a unidade fecha: resistência é volt por ampère, o que a gente chama de ohm.

N024 No circuito, antecipando o regime estacionário que vamos justificar daqui a pouco, a mesma corrente total atravessa os elementos em série. Nos fios a resistência é muito pequena, então o potencial cai pouco. No resistor ela é muito maior, e é ali que cai quase toda a queda de potencial.

## B05 · A segunda pergunta

N025 De volta ao circuito inteiro: o campo existe em todo trecho, pequeno nos fios e grande no resistor. A fita azul mostra o potencial ao longo do caminho: cai pouco nos fios, muito no resistor, e sobe de novo dentro da fonte. O campo, na direção do fio, é a inclinação dessa fita. Mas quem estabelece esse campo ao longo do circuito inteiro?

## B06 · Conservação de carga

N026 Para responder, precisamos de uma ideia: a carga se conserva. Imagina um volume pequeno dentro do fio. Se entra mais corrente do que sai, a carga dentro dele só pode aumentar.

N027 Em forma local, é a equação da continuidade: a variação, no tempo, da densidade de carga, mais o divergente da densidade de corrente, é zero. O divergente mede, numa vizinhança muito pequena, se sai mais fluxo de corrente do que entra.

N028 Integrando no volume, a primeira parcela vira a variação da carga dentro dele. Na segunda, o teorema da divergência transforma a integral do divergente no fluxo da densidade de corrente pela superfície que fecha o volume.

N029 Neste trecho quase unidimensional, as faces laterais não contribuem; sobram a face de entrada e a de saída. No fim, a variação da carga no tempo é a corrente que entra menos a corrente que sai. É exatamente a contabilidade que a gente imaginou.

## B07 · A cena central

N030 Agora vem a parte mais importante, então vamos devagar. A ordem que você vai ver é didática: separamos os passos para enxergar causa e consequência.

N031 Suponha que, por um instante, entre mais corrente do que sai. Repara nas duas setas verdes: a de entrada é maior que a de saída. Então a carga dentro do volume aumenta, e o medidor azul mostra isso. É só contabilidade: o que entra e não sai fica guardado.

N032 E onde essa carga fica? Num bom condutor, a redistribuição que importa aqui aparece principalmente como uma pequena quantidade de carga na superfície, na casca do condutor, e não como um fluido enchendo o volume.

N033 Essas cargas mudam o potencial ao redor delas. Olha a curva do potencial se deformando junto do acúmulo. O campo, na direção do fio, é menos a derivada do potencial em relação à posição: quando a inclinação muda, o campo muda. A redistribuição altera o campo de um jeito que reduz o desbalanço entre a corrente que entra e a que sai; aqui, o campo de entrada diminui e o de saída aumenta.

N034 E por que a corrente muda junto? Porque, no material ôhmico, a densidade de corrente é a condutividade vezes o campo. Mudou o campo, mudou a densidade de corrente. É por isso que, na tela, mostramos primeiro a carga, depois o potencial, depois o campo, e só então a corrente.

N035 Funciona como um mecanismo de ajuste, uma realimentação eletrostática: o acúmulo reduz justamente o desbalanço que o criou. Quando a corrente que entra iguala a que sai, o acúmulo para. Mas repara: as cargas que se acumularam continuam lá.

## B07b · Do trecho para o circuito todo

N036 Isso não acontece só num ponto. Quando a câmera abre, vemos que o circuito inteiro se ajustou: existe uma distribuição de cargas na superfície dos condutores, já estabelecida, que produz em cada região um campo compatível com a geometria, os materiais e o regime estacionário. Não é uma onda de cargas viajando a partir deste ponto; é o estado final. A imagem é qualitativa.

N037 Repara no que muda de um trecho para outro. Num circuito em série, no regime estacionário, a corrente total é a mesma em todas as seções. Mas a densidade de corrente é a corrente dividida pela área, então pode mudar quando a área muda. E o campo local é a corrente dividida pelo produto da condutividade pela área. Por isso, para a mesma corrente total, o campo é maior onde o produto da condutividade pela área é menor: pequeno nos fios, grande no resistor.

N038 Olha o marcador percorrendo a fita de potencial: o campo na direção do fio é a inclinação, com sinal de menos, do potencial ao longo do caminho. E a distribuição superficial de cargas estabelece como o potencial varia ao longo do circuito.

## B08 · Regime estacionário

N039 Durante o ajuste, a densidade de carga muda no tempo. Quando ele termina, essa variação é zero e, pela equação da continuidade, o divergente da densidade de corrente também é zero: tudo o que entra em cada pedacinho sai.

N040 Mas atenção: as cargas na superfície não sumiram. Elas só pararam de se redistribuir. Regime estacionário não é ausência de cargas superficiais. Tudo está em movimento, mas nada muda: é isso que estacionário quer dizer.

N041 Compara com o que você já conhece. No equilíbrio eletrostático, o campo dentro do condutor é zero e não existe corrente. Já num fio resistivo com corrente estacionária, o campo dentro do material não é zero, e a densidade de corrente continua sendo a condutividade vezes o campo. Para sustentar corrente num condutor resistivo como esse é preciso campo, estabelecido pelas cargas na superfície. Então estacionário não é eletrostático.

## B09 · Quem repõe a energia

N042 Falta a última pergunta. No resistor, energia elétrica é dissipada em forma de calor. Então quem repõe essa energia?

N043 A fonte. E esse mecanismo precisa ser não eletrostático, porque o campo elétrico conservativo, sozinho, não fornece energia líquida numa volta completa: tudo o que dá num trecho, toma de volta no resto do caminho.

N044 Dentro da bateria, além do campo elétrico, existe uma força que não é eletrostática, ligada ao mecanismo da fonte. Chamamos de força da fonte, por unidade de carga. A bateria aqui é só um modelo esquemático; não entramos na química.

N045 Repara que os dois coexistem. Dentro da fonte, o campo elétrico continua existindo e aponta, do positivo para o negativo, tentando empurrar a carga para baixo. A força da fonte atua no sentido oposto e vence. A força total por unidade de carga é o campo elétrico mais a força da fonte.

N046 Para enxergar o balanço, vamos acompanhar uma carga de prova positiva. Veja ela subindo, contra a tendência eletrostática: a régua de energia por carga vai crescendo.

## B10 · Força eletromotriz

N047 E é aqui que entra a força eletromotriz. Apesar do nome, ela não é uma força. Ela é a integral, ao longo do circuito fechado, da força por unidade de carga. Newton por coulomb, vezes metro, é joule por coulomb, que é volt: neste caso, de uma fonte estacionária, ela mede energia entregue por unidade de carga.

N048 Separando a força por unidade de carga em campo elétrico e força da fonte, a força eletromotriz é a integral do campo mais a integral da força da fonte.

N049 Neste circuito de corrente contínua estacionária, sem indução magnética e sem movimento do circuito, o campo elétrico é conservativo. Então a integral do campo numa volta completa é zero. Acompanha o marcador: o campo realiza trabalho nos fios e no resistor, mas dentro da fonte contribui com sinal contrário, e a barra dele volta a zero. Já a força da fonte só contribui dentro da bateria, e a barra dela fica no valor da força eletromotriz.

N050 Cancelou o termo do campo, sobra: a força eletromotriz é a integral, ao redor do circuito, da força da fonte. É a fonte realizando trabalho não eletrostático e repondo energia nas cargas. O campo dirige a condução nos trechos passivos; quem repõe a energia é a fonte.

## B11 · Energia

N051 E agora a energia fecha. Numa escala local, a densidade de potência transferida pelo campo para a matéria é o produto escalar da densidade de corrente pelo campo elétrico. No resistor ôhmico, isso aparece como dissipação.

N052 A potência total no resistor é a integral dessa densidade de potência ao longo dele. Se o resistor é uniforme, a densidade de corrente e o campo são constantes e paralelos: a potência é a densidade de corrente vezes o campo vezes o volume, que é a área vezes o comprimento.

N053 Reagrupando: densidade de corrente vezes área é a corrente, e campo vezes comprimento é a queda de potencial. A potência é a queda de potencial vezes a corrente. Com a Lei de Ohm, é a resistência vezes a corrente ao quadrado.

N054 Do lado da fonte, a potência fornecida é a força eletromotriz vezes a corrente. Num modelo ideal, com toda a resistência concentrada, a força eletromotriz é a resistência vezes a corrente. Substituindo, a potência da fonte é a resistência vezes a corrente ao quadrado: exatamente a potência dissipada pelos elementos resistivos. É um balanço esquemático; não existem pacotes de energia viajando dentro dos elétrons.

## B12 · Payoff e encerramento

N055 Então, quem empurra as cargas? A bateria não empurra as cargas de longe.

N056 A fonte fornece energia e mantém a diferença de potencial. A distribuição superficial de cargas estabelece o campo elétrico ao longo de todo o circuito. E esse campo atua, localmente, sobre os portadores e, no material ôhmico, estabelece a densidade de corrente.

N057 Vale guardar quatro distinções. A bateria não cria a corrente diretamente em todo lugar. O divergente da densidade de corrente ser zero não cria o campo. As cargas superficiais não fornecem a energia. E força eletromotriz não é força.

N058 Se isso mudou a sua imagem de um circuito, inscreva-se no Parallax Lab. E conta nos comentários: você já conhecia o papel das cargas superficiais?
