# yt_0009 — Quem empurra as cargas? — sugestão de narração (v1)

Estilo: professor de cursinho, variáveis pelo nome (o símbolo é apresentado uma vez, junto do nome), conectivos que conduzem o raciocínio. Alvo: mesma contagem de fala do yt_0006 (~3.400 palavras), para a mesma voz (ElevenLabs v4). Cada unidade (N###) corresponde a um trecho da cena; a sincronização estica as pausas do vídeo conforme a voz. Sem tags nesta versão (ver `narracao_tags.md`).

## B00–B01 · Gancho, título e mapa

N001 Olha este circuito. De um lado, uma bateria. Do outro, um resistor. E, ligando os dois, um fio comprido.

N002 Agora imagina uma carga bem aqui, neste trecho do fio, lá longe da bateria. A bateria ficou para trás. Que força está agindo sobre essa carga, agora?

N003 Repara: não pode ser a bateria puxando a carga à distância. Ela não alcança este ponto. Então, afinal, quem empurra as cargas?

N004 Pensa assim: este circuito é um laço fechado, e a corrente é a mesma em todo o caminho. Ela passa pela bateria, pelo fio de cima, pelo resistor, pelo fio de baixo e volta. Então a pergunta vale para qualquer ponto do laço, não só para este.

N005 Bem-vindos ao Parallax Lab. Neste vídeo vamos descobrir quem empurra as cargas, passando pela Lei de Ohm e pela força eletromotriz.

N006 O caminho tem três perguntas, uma dentro da outra. Primeiro: que força age, localmente, sobre cada carga do fio? Depois: quem estabelece o campo elétrico ao longo de um circuito inteiro? E, por fim: quem repõe a energia que o resistor dissipa?

N007 Vamos mergulhar no fio e começar pela primeira.

## B02 · Condução local

N008 Por dentro, um metal é uma rede de íons fixos, com elétrons livres passeando entre eles. Enquanto não existe campo, esses elétrons se movem para todos os lados, batem, mudam de direção, de forma totalmente desordenada. Em média, ninguém vai a lugar nenhum.

N009 Agora ligamos o circuito. Neste trecho do fio passa a existir um campo elétrico, o que a gente vê na tela como esta seta ciano. E é esse campo que age, localmente, sobre cada portador de carga.

N010 E repara na palavra que a gente vai repetir muito: localmente. A carga não precisa saber onde está a bateria. Ela só sente o campo que existe exatamente no lugar onde ela está.

N011 A força sobre um portador é a carga dele vezes o campo elétrico. Para um elétron, a carga é negativa: menos e, o valor da carga elementar. Então a força sobre o elétron aponta no sentido contrário ao do campo.

N012 Mas olha o que acontece de verdade. Os elétrons continuam desordenados. Não é uma fila de elétrons disparando pelo fio. O campo só acrescenta, por cima da bagunça, uma velocidade média muito pequena, a velocidade de deriva, para o lado oposto ao campo. É isso que a marca violeta mostra: o conjunto inteiro escorrega devagarzinho.

N013 Por que essa deriva é tão pequena? Porque o elétron anda um pedacinho, bate num íon, perde o rumo, anda outro pedacinho, bate de novo. O campo vai empurrando, mas as colisões vão embaralhando. No fim das contas, a velocidade média de deriva em um fio comum é da ordem de milímetros por segundo, muito menor do que a velocidade desordenada dos elétrons.

N014 Em escala maior, essa deriva vira corrente. A densidade de corrente, que aparece na tela como a letra J, é o número de portadores por volume, vezes a carga de cada um, vezes a velocidade de deriva.

N015 Repara no sinal: para elétrons, a carga é negativa. Então a deriva é oposta ao campo, mas a densidade de corrente aponta no mesmo sentido do campo. As duas ficam paralelas, e é por isso que a gente desenha a corrente convencional no sentido do campo.

N016 Agora uma definição que vai nos acompanhar o vídeo inteiro: a força por unidade de carga, que vamos chamar de f minúsculo, é a força dividida pela carga. E, num trecho resistivo comum, essa força por carga é simplesmente o campo elétrico.

N017 O material responde de um jeito simples: a densidade de corrente é a condutividade vezes a força por carga. Aqui, a condutividade vezes o campo elétrico. Guarda essa relação, porque ela já carrega dentro dela a Lei de Ohm que a gente conhece.

N018 Uma comparação ajuda. Pensa em um material muito condutor, como o cobre, e em outro quase isolante, como a borracha. Com o mesmo campo, o cobre tem uma densidade de corrente enorme e a borracha, quase nenhuma. Quem faz essa diferença é a condutividade.

## B03 · O fio visto de longe

N019 Vamos afastar a câmera e olhar para o mesmo fio como um cilindro: um comprimento, que na tela é a letra L, e uma seção transversal com uma certa área, a letra A. Uma corrente, I, entra por uma ponta.

N020 Primeiro, a corrente. Ela é a soma da densidade de corrente que atravessa a seção. Se a densidade for uniforme, a conta é direta: corrente igual à densidade de corrente vezes a área. Isolando, a densidade de corrente é a corrente dividida pela área.

N021 Repara no que a gente está fazendo: trocando uma grandeza local, a densidade de corrente, por uma grandeza do fio inteiro, a corrente. Isso só funciona porque assumimos que a densidade é uniforme na seção. É uma boa aproximação para um fio comum conduzindo corrente contínua.

N022 Agora, o campo. A queda de potencial entre as duas pontas é a integral do campo ao longo do fio. Com campo uniforme e paralelo ao caminho, isso vira o campo vezes o comprimento. Chamando de V o módulo dessa queda de potencial, o campo é V dividido pelo comprimento.

N023 Resumindo, temos três relações sobre o mesmo fio. A densidade de corrente é a corrente dividida pela área. O campo é a queda de potencial dividida pelo comprimento. E a densidade de corrente é a condutividade vezes o campo.

N024 A terceira relação é local, vale em cada ponto. As outras duas são geométricas, falam do fio inteiro. O que a gente vai fazer agora é juntar as três.

N025 E repara também nas unidades. Densidade de corrente é ampère por metro quadrado. Campo é volt por metro. Então a condutividade tem que ser ampère por volt por metro: a unidade que fecha a conta.

## B04 · De J igual sigma E até V igual R I

N026 Começa pela relação do material: densidade de corrente igual à condutividade vezes campo.

N027 Agora olha o que acontece. No lugar da densidade de corrente, entra a corrente dividida pela área, porque foi isso que a gente deduziu. E no lugar do campo, entra a queda de potencial dividida pelo comprimento.

N028 Fica assim: a corrente dividida pela área é igual à condutividade vezes a queda de potencial dividida pelo comprimento. Nada de novo, só substituição.

N029 Agora é álgebra. Multiplicando os dois lados pelo comprimento e pela área, a corrente vezes o comprimento passa a ser igual à condutividade vezes a área vezes a queda de potencial.

N030 Repara que, a cada passo, a gente só faz uma operação por vez: multiplicar os dois lados pela mesma quantidade ou isolar uma grandeza. Nada de truque. É álgebra honesta, e cada termo que se move tem uma origem física visível na tela.

N031 Isolando a queda de potencial, temos: a corrente vezes o comprimento, dividido pela condutividade vezes a área.

N032 Repara neste bloco: comprimento dividido por condutividade vezes área. Ele só depende do material, por causa da condutividade, e da geometria do fio, por causa do comprimento e da área. Não depende nem da corrente, nem da queda de potencial.

N033 Vale parar um segundo aqui, porque este bloco é o coração da Lei de Ohm. Ele diz que o fio é um objeto com uma única característica elétrica: o quanto ele resiste. E essa característica sai de três coisas que você pode medir com uma régua e uma tabela: comprimento, área e condutividade do material.

N034 Esse bloco tem nome: é a resistência. E agora a Lei de Ohm aparece sozinha: a queda de potencial é a resistência vezes a corrente.

N035 Isso significa que a Lei de Ohm não caiu do céu: ela nasce da lei local mais a geometria. E dá para ler a resistência com os olhos: se o fio fica mais comprido, a resistência aumenta; se ele fica mais grosso, a resistência diminui.

N036 Dá até para conferir a unidade. Resistência é volt por ampère, e esse nome você conhece: ohm. Por isso a Lei de Ohm tem esse nome, e por isso a unidade da resistência carrega o nome de quem a descobriu.

## B05 · A segunda pergunta

N037 Voltando ao circuito inteiro, o campo existe em todo trecho: pequeno nos fios, grande no resistor. A fita azul mostra o potencial ao longo do caminho. Ele cai um pouquinho nos fios, cai muito no resistor e sobe de novo dentro da fonte.

N038 Olha como isso aparece no circuito: nos fios, a resistência é muito pequena, porque a condutividade é altíssima, então o potencial cai pouco. No resistor, a condutividade é menor e a seção costuma ser mais fina, então quase toda a queda de potencial acontece ali.

N039 O campo é a inclinação dessa fita. Mas isso levanta uma pergunta melhor: quem estabelece esse campo ao longo do circuito inteiro?

## B06 · Conservação de carga

N040 Para responder, a gente precisa de uma ideia: a carga se conserva. Imagina um volume pequeno dentro do fio. Se entra mais corrente do que sai, a carga dentro dele só pode aumentar.

N041 Em forma local, isso é a equação da continuidade: a variação, no tempo, da densidade de carga, mais o divergente da densidade de corrente, é igual a zero. O divergente diz quanta corrente sai de cada ponto.

N042 Pensa no divergente como uma espécie de saldo local do fluxo: quanta corrente está saindo de um ponto menos quanta está entrando. Se esse saldo é positivo, está saindo mais do que entrando, e a carga naquele ponto diminui. Se é negativo, a carga aumenta.

N043 Vamos integrar essa equação no volume. A primeira parcela é a integral da variação da densidade de carga. A segunda, a integral do divergente da densidade de corrente.

N044 Agora o teorema da divergência entra em cena. A integral do divergente, no volume, é igual ao fluxo da densidade de corrente pela superfície que fecha o volume.

N045 A integral da densidade de carga é a carga que está dentro do volume. Então temos: a variação da carga no tempo, mais o fluxo pela superfície, igual a zero.

N046 E o fluxo pela superfície, aqui, são só as duas faces: a corrente que sai, menos a que entra. No fim, a variação da carga no tempo é a corrente que entra menos a corrente que sai. É exatamente a conta de balanço que a gente imaginou.

## B07 · A cena central

N047 Agora vem a parte mais importante. Suponha que, por um instante, entre mais corrente do que sai desse trecho. Repara nas duas setas verdes: a de entrada é maior que a de saída.

N048 Então a carga dentro do volume aumenta: a variação da carga no tempo é positiva. O medidor azul mostra isso.

N049 Isso é só contabilidade: o que entra e não sai fica guardado. Não existe mágica, só o princípio de que a carga não surge nem desaparece.

N050 E onde essa carga se acumula? Na superfície do condutor. Não no volume, como se fosse um fluido enchendo um tanque: o interior continua neutro, e o excesso fica na casca.

N051 Isso tem a ver com o que a gente já viu: dentro de um condutor, qualquer excesso de carga é empurrado para a superfície. O interior fica neutro, e o excesso mora na casca. Na corrente estacionária isso continua valendo, com uma diferença importante: o campo dentro do material não é zero.

N052 Essas cargas na superfície mudam o potencial ao redor delas. Olha a curva do potencial se deformando junto do acúmulo.

N053 E o campo é menos a derivada do potencial em relação à posição. Então, quando a inclinação do potencial muda, o campo muda. O campo de entrada diminui, o campo de saída aumenta.

N054 E por que a corrente muda? Porque a densidade de corrente é a condutividade vezes o campo. Mudou o campo, mudou a corrente, com um pequeno atraso: primeiro a carga, depois o potencial, depois o campo, e só então a corrente.

N055 Repara como isso é uma espécie de autorregulagem. O acúmulo de carga reduz exatamente a diferença que o criou: ele diminui o campo de entrada e aumenta o de saída, e com isso aproxima a corrente que entra da corrente que sai. O sistema se ajusta sozinho, até o balanço fechar.

N056 O ajuste continua até a corrente que entra igualar a que sai. Aí a variação da carga fica zero e o acúmulo para. Mas repara: as cargas que se acumularam ficam lá.

## B07b · Do trecho para o circuito todo

N057 Isso não acontece só num ponto. Quando a gente abre a câmera, vê que o circuito inteiro se ajustou: existe uma distribuição de cargas na superfície dos condutores, já estabelecida, que produz, em cada região, o campo certo.

N058 Aqui a imagem é qualitativa. A quantidade de carga por área depende da geometria: dos cantos, dos terminais, das pontas do resistor. O que importa é a ideia: são essas cargas, espalhadas na superfície, que organizam o campo ao longo do circuito.

N059 E não pense nessa distribuição como algo que viaja de um ponto para o resto do circuito. O que a imagem mostra é o estado final: um circuito já estabelecido, com as cargas na superfície no lugar certo para produzir o campo que cada trecho precisa.

N060 Por isso o campo é pequeno nos fios e grande no resistor, mesmo com a mesma corrente passando por todos. A densidade de corrente é parecida em todo lugar; o campo é que se adapta ao material, porque a condutividade do resistor é menor.

N061 Olha o marcador percorrendo a fita de potencial: o campo na direção do fio é a inclinação, com sinal de menos, do potencial ao longo do caminho. Inclinação suave nos fios, inclinação forte no resistor.

N062 Resumindo o que a fita mostra: o campo é grande onde o potencial cai rápido e pequeno onde ele cai devagar. E quem decide como o potencial cai ao longo do circuito é justamente a distribuição das cargas superficiais.

## B08 · Regime estacionário

N063 Durante esse ajuste, a densidade de carga muda no tempo. Essa é a fase de transição.

N064 Quando o ajuste termina, a variação da densidade de carga no tempo é zero. E, pela equação da continuidade, o divergente da densidade de corrente também é zero: tudo o que entra em cada pedacinho sai.

N065 Mas atenção: as cargas na superfície não sumiram. Elas só pararam de se redistribuir. Regime estacionário não é a mesma coisa que ausência de cargas superficiais.

N066 Imagina fotografar o circuito em dois instantes diferentes depois do ajuste: a mesma distribuição de cargas, o mesmo campo, a mesma corrente. Tudo está em movimento, mas nada muda. É isso que estacionário quer dizer.

N067 É por isso que, em um fio com corrente, o campo não é zero. Para sustentar corrente, é preciso campo. E para existir esse campo, são precisas essas cargas na superfície.

N068 Vale comparar com uma situação que você já conhece. No equilíbrio eletrostático, o campo elétrico dentro do condutor é zero e não existe corrente.

N069 Já num fio resistivo conduzindo corrente estacionária, o campo dentro do material não é zero. E a densidade de corrente continua sendo a condutividade vezes o campo.

N070 Então estacionário não é eletrostático. Um condutor com corrente não está em equilíbrio eletrostático.

## B09 · Quem repõe a energia

N071 Falta a última pergunta. As cargas perdem energia no resistor: ele esquenta. Então quem repõe essa energia?

N072 A fonte. Dentro da bateria, além do campo elétrico, existe uma força que não é eletrostática, ligada ao mecanismo da fonte. A gente vai chamar essa força, por unidade de carga, de f s.

N073 E por que precisa ser uma força não eletrostática? Porque o campo das cargas estáticas, sozinho, não consegue manter uma corrente circulando: ao dar uma volta completa no circuito, ele devolve tudo o que deu. Sem outra coisa trabalhando, a energia que o resistor dissipa nunca seria reposta.

N074 Repara que os dois coexistem dentro da fonte. O campo elétrico, criado pelas cargas dos terminais, aponta do positivo para o negativo e tenta empurrar a carga para baixo. A força da fonte aponta no sentido oposto, e é mais forte.

N075 Por isso a força total por unidade de carga é o campo elétrico mais a força da fonte. Veja o portador subindo, contra a tendência eletrostática: a régua de energia por carga vai crescendo. Aqui, a bateria é só um modelo esquemático, não estamos entrando na química.

## B10 · Força eletromotriz

N076 E é aqui que entra a força eletromotriz. Apesar do nome, ela não é uma força. Ela é definida como a integral, ao longo do circuito fechado, da força por unidade de carga.

N077 Antes de entrar na conta, vale dizer: o nome é um acidente histórico. Ninguém mediu isso em newtons. O que a gente chama de força eletromotriz mede a energia que a fonte entrega a cada unidade de carga que passa por ela.

N078 Vamos conferir a unidade. Newton por coulomb, vezes metro, é joule por coulomb, que é volt. A força eletromotriz é energia por carga.

N079 Agora vamos separar a força por carga em duas partes: a do campo elétrico e a da fonte. A força eletromotriz fica sendo a integral do campo mais a integral da força da fonte.

N080 Neste circuito de corrente contínua estacionária, sem indução magnética e sem movimento do circuito, o campo elétrico é conservativo. Então a integral do campo ao redor de uma volta completa é zero.

N081 Acompanha o marcador: o campo contribui ao longo dos fios e do resistor, mas, dentro da fonte, ele contribui com sinal contrário e cancela tudo na volta. A barra do campo sobe e volta a zero. Já a força da fonte só contribui dentro da bateria, e a barra dela fica no valor da força eletromotriz.

N082 A ideia por trás é simples: toda vez que a carga percorre um pedaço do circuito, o campo realiza trabalho sobre ela. Ao completar a volta e voltar ao ponto de partida, o trabalho total do campo é nulo, porque o campo é conservativo. Se a carga ainda assim ganhou energia, quem deu foi a fonte.

N083 Cancelou o termo do campo, sobra: a força eletromotriz é a integral, ao redor do circuito, da força da fonte. É a fonte realizando trabalho não eletrostático e repondo energia nas cargas.

N084 Em outras palavras: o campo elétrico organiza o caminho, mas quem fornece a energia é a fonte. As duas funções são diferentes, e é importante não misturar uma com a outra.

## B11 · Energia

N085 E agora a energia fecha. Comece numa escala local: a potência por volume é a densidade de corrente vezes o campo. Essa é a potência por volume, que na tela aparece como a letra p minúscula.

N086 A potência total no resistor é a integral dessa potência por volume, ao longo do resistor inteiro.

N087 Se o resistor é uniforme, a densidade de corrente e o campo são constantes. A integral vira: densidade de corrente vezes campo vezes o volume, que é a área vezes o comprimento.

N088 Agora reagrupa os fatores: densidade de corrente vezes área é a corrente, e campo vezes comprimento é a queda de potencial. A potência é a tensão vezes a corrente.

N089 Repara em como cada fator do volume ganhou um significado novo: a área foi para junto da densidade de corrente e virou corrente, o comprimento foi para junto do campo e virou tensão. É a mesma conta, só reagrupada.

N090 E com a Lei de Ohm, a queda de potencial é a resistência vezes a corrente. Então a potência é a resistência vezes a corrente ao quadrado.

N091 Do lado da fonte, a potência fornecida é a força eletromotriz vezes a corrente. Num circuito ideal simples, com uma resistência total, a força eletromotriz é a resistência vezes a corrente.

N092 Substituindo: a potência da fonte é a resistência vezes a corrente ao quadrado, exatamente a potência dissipada no resistor. Tudo o que a fonte fornece, o resistor dissipa. A energia fecha.

N093 Em termos físicos, é uma conta de balanço: a fonte entrega energia por segundo e o resistor transforma energia por segundo em calor. Em regime estacionário, esses dois números têm que ser iguais.

N094 Um aviso: isso é um balanço esquemático. Não existem pacotes de energia viajando dentro dos elétrons.

## B12 · Payoff e encerramento

N095 Então, quem empurra as cargas? A bateria não empurra as cargas de longe.

N096 A fonte fornece energia e mantém a diferença de potencial. As cargas na superfície dos condutores organizam o campo elétrico ao longo de todo o circuito. E esse campo atua, localmente, sobre os portadores, produzindo a corrente.

N097 E essas ideias se encaixam como camadas. Na fonte, a força não eletrostática fornece energia. Na superfície, as cargas organizam o campo. No circuito, o campo age em cada portador. E na condução, a densidade de corrente responde ao campo.

N098 Vale guardar estas quatro distinções. A bateria não cria a corrente diretamente em todo lugar. O divergente da corrente ser zero não cria o campo. As cargas superficiais não são a fonte de energia. E força eletromotriz não é força.

N099 E este é o recado final: cada uma dessas peças tem um papel diferente, e é justamente essa separação de papéis que explica por que um circuito funciona.

N100 Se isso mudou a sua imagem de um circuito, inscreva-se no Parallax Lab. E conta nos comentários: você já conhecia o papel das cargas superficiais?
