# yt_0021 — narração v4 com tags (para gravação)

## Texto corrido (para gravação)

[curious] Olha esses dois bastões. Na verdade, é o mesmo bastão: mesma madeira, mesma massa, mesmo comprimento. A única diferença é onde ele está preso. Aqui o eixo passa pela ponta do cabo; aqui, pela ponta grossa. E a gente vai levar os dois, do repouso até a mesma velocidade angular.

[thoughtful] O bastão tem nove décimos de quilo e oitenta e quatro centímetros. Os dois giram até dez radianos por segundo, e a gente está de cima, no plano horizontal, então a altura não muda e não entra energia potencial nessa história. Resultado: segurando pelo cabo, o braço entrega quatorze joules. Segurando pela ponta grossa, só sete. Exatamente a metade, para o mesmo bastão, na mesma velocidade angular.

[curious] E aí fica a pergunta. A massa não mudou. A velocidade angular final não mudou. O que, então, mudou para a energia dobrar? E mais: existe um número que diga, para qualquer corpo e qualquer eixo, quanto custa fazer ele girar?

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

[thoughtful] Hoje a gente vai construir uma das grandezas mais importantes da rotação: o momento de inércia. Primeiro, de onde ele aparece, a partir da energia de um corpo girando. Depois, de que ele depende e como calcular, até com integral. E por fim, dois atalhos poderosos: os eixos paralelos e os eixos perpendiculares. No final, três exercícios para firmar tudo.

[thoughtful] Você já sabe que um ponto de um corpo que gira anda com velocidade igual à velocidade angular vezes a distância ao eixo. E sabe que uma partícula com velocidade v tem energia cinética meio m v ao quadrado. Junta as duas ideias: um corpo que gira é uma multidão de partículas, cada uma no seu círculo. Qual é a energia de toda essa multidão?

[thoughtful] Vamos cortar o disco em pedacinhos, tão pequenos que cada um pode ser tratado como uma partícula. O pedaço número i tem massa m i e está a uma distância r i do eixo. Como o corpo é rígido e gira em torno de um eixo fixo, todos os pedaços têm a mesma velocidade angular, mas a velocidade de cada um depende da sua distância: v i é a velocidade angular vezes r i.

[thoughtful] A energia cinética desse pedaço é meio m i vezes v i ao quadrado. Troca v i por velocidade angular vezes r i. Fica meio, m i, r i ao quadrado, velocidade angular ao quadrado. Repara de onde veio o r i ao quadrado: a velocidade é proporcional à distância, e a energia é proporcional ao quadrado da velocidade.

[thoughtful] Para achar a energia do corpo todo, soma a de todos os pedaços. E aqui acontece uma coisa linda: a velocidade angular é a mesma para todos, então ela sai da soma. Sobra, dentro do parêntese, a soma de cada massa vezes o quadrado da sua distância ao eixo. Esse parêntese só depende do corpo e de onde está o eixo. Não depende de quão rápido ele gira.

[happy] E esse parêntese ganha nome: momento de inércia. A gente escreve I, e a unidade é quilograma vezes metro ao quadrado. A energia cinética de rotação fica meio, momento de inércia, velocidade angular ao quadrado. Olha a tradução: a massa da translação vira o momento de inércia da rotação, a velocidade vira a velocidade angular. Mesma forma, mesma ideia.

[thoughtful] Duas observações. Primeira: isso não é uma energia nova. É a mesma meio m v ao quadrado de sempre, só que somada pedaço por pedaço, e o momento de inércia é o jeito de guardar essa soma. Segunda: o r i que entra na conta é a distância ao eixo, e não a distância até a origem ou até o centro do corpo. Se o pedaço está lá em cima, mas no eixo, ele não contribui com nada.

[thoughtful] Vamos a um caso simples: um haltere. Duas massas iguais, de dois quilos, nas pontas de uma haste leve de um metro. Com o eixo bem no meio, cada massa está a meio metro. A conta é só somar: m vezes meio metro ao quadrado, duas vezes. Dá um quilograma vezes metro ao quadrado.

[excited] Agora muda o eixo: ele passa por uma das massas. Mesmo haltere, mesmas massas. Uma massa fica em cima do eixo e não conta. A outra fica a um metro, e o quadrado dela é enorme. O resultado é dois quilogramas vezes metro ao quadrado: o dobro. E essa é a ideia mais importante do vídeo: o momento de inércia não é uma propriedade do objeto sozinho. É uma propriedade da distribuição de massa em relação a um eixo.

[thoughtful] E repara no quadrado. Se você afasta uma massa do eixo para o dobro da distância, a contribuição dela quadruplica. Uma massa pequena, longe do eixo, pode pesar tanto quanto uma massa grande, perto. Um quarto da massa, no dobro da distância, dá exatamente a mesma contribuição.

[thoughtful] Dá para resumir um corpo inteiro com um único comprimento. O raio de giração é a distância em que, concentrando toda a massa num anel fino, teríamos o mesmo momento de inércia. Escreve I igual a massa total vezes k ao quadrado. No haltere são quatro quilos e I igual a um, então k é a raiz de um quarto: meio metro.

[thoughtful] Mas quase nenhum corpo real é um punhado de bolinhas. A massa é contínua. Então a soma vira integral: a gente fatia o corpo em pedaços de massa d m e soma r ao quadrado vezes d m. Numa barra fina, a massa por comprimento é a massa total dividida pelo comprimento, e cada fatia de largura d x tem massa lambda vezes d x.

[thoughtful] Eixo na ponta da barra. A fatia que está a uma distância x contribui com x ao quadrado vezes lambda d x. Integra de zero até L. A integral de x ao quadrado é x ao cubo sobre três, e sobra a massa vezes o comprimento ao quadrado sobre três. Olha o brilho das fatias: as de longe dominam a conta, porque o quadrado cresce rápido.

[excited] Agora o eixo no centro. Os limites vão de menos L sobre dois a mais L sobre dois, e dá M L ao quadrado sobre doze: quatro vezes menor. Dá para ver sem integral: são duas meias-barras, cada uma com metade da massa e metade do comprimento, girando pela ponta. Cada uma vale M sobre dois, vezes L sobre dois ao quadrado, sobre três. Duas delas: um doze avos.

[thoughtful] E se toda a massa do nosso bastão, nove décimos de quilo ao longo de oitenta e quatro centímetros, estivesse distribuída uniformemente? Pela ponta, o momento de inércia seria zero vírgula dois um dois quilogramas metro ao quadrado; pelo centro, zero vírgula zero cinco três. Mesmo corpo, dois eixos, fator quatro. Mas o nosso bastão de verdade não é uniforme, e a gente já volta nele.

[thoughtful] Vamos juntar uma tabela de formas. E se o corpo é um aro, com toda a massa na borda? Cada pedaço está à mesma distância R, então a soma de m i R ao quadrado é R ao quadrado vezes a soma das massas. Sem integral: I igual a M R ao quadrado.

[thoughtful] Agora o disco maciço. Corta em anéis finos, como as camadas de uma cebola. Um anel de raio r e largura d r tem área dois pi r d r, e massa a densidade por área vezes essa área. Cada anel é um aro, então contribui com r ao quadrado vezes sua massa. Integra de zero até R, e o resultado é meio M R ao quadrado.

[excited] Compara. Mesma massa, mesmo raio: o aro tem o dobro do momento de inércia do disco. No disco, metade da massa está dentro deste círculo. Mas olha só: ela responde por apenas um quarto do momento de inércia. Os outros três quartos vêm da metade que está mais longe do eixo. No aro, toda a massa está na borda, onde o quadrado pesa mais.

[thoughtful] Para a esfera maciça, a gente fatia em discos finos ao longo do eixo. Pelo triângulo retângulo, o disco na altura z tem raio raiz de R ao quadrado menos z ao quadrado. A massa dele é a densidade vezes pi vezes esse raio ao quadrado, vezes d z, e o momento de inércia a gente já sabe: meio da massa vezes o raio ao quadrado. Integra de menos R até R, com a densidade igual à massa sobre o volume, e dá dois quintos de M R ao quadrado.

[thoughtful] Esses números formam uma tabela que vale a pena guardar. Todos assumem corpos homogêneos e o eixo de simetria. E o aro e a casca esférica são de parede fina; se a parede for grossa, o número é outro. O fator na frente do M R ao quadrado só depende da forma: quanto mais massa perto do eixo, menor ele é. A barra fica numa linha separada porque usa o comprimento, não o raio.

[curious] E se o eixo não passa pelo centro do corpo? Lembra da barra: pelo centro, um doze avos; pela ponta, um terço. A diferença é um quarto de M L ao quadrado, que é exatamente a massa vezes o quadrado da distância entre os dois eixos. Será coincidência? Não. Vale para qualquer corpo.

[thoughtful] Pega um corpo qualquer e um eixo pelo centro de massa. Agora um segundo eixo, paralelo, a uma distância d. Para um pedaço i, a posição vista do segundo eixo é a posição vista do centro de massa mais o vetor d. Eleva ao quadrado: r i ao quadrado é r linha ao quadrado, mais duas vezes d escalar r linha, mais d ao quadrado.

[excited] Multiplica por m i e soma. O primeiro termo é o momento de inércia em torno do centro de massa. O último é a massa total vezes d ao quadrado. E o do meio? Dentro do parêntese tem a soma de m i vezes r linha, que é a massa total vezes a posição do centro de massa, vista do próprio centro de massa. Zero: os vetores se compensam, como no polígono fechado da esquerda. O termo cruzado desaparece, e fica: I igual a I cm mais M d ao quadrado.

[thoughtful] Tem uma segunda leitura, que é pura energia. Com o eixo fixo, o centro de massa anda num círculo de raio d, com velocidade ômega d. A energia do corpo é a do centro de massa andando, meio M v cm ao quadrado, mais a do giro em torno do centro de massa, meio I cm ômega ao quadrado. Substitui, e aparece meio vezes I cm mais M d ao quadrado, vezes ômega ao quadrado. Mas a energia em torno do eixo fixo é meio I vezes ômega ao quadrado. Comparando, sai o mesmo teorema.

[thoughtful, emphatic] Dois cuidados. Primeiro, olha o gráfico: cada ponto da curva é um eixo paralelo, e o menor momento de inércia está no centro de massa. Para qualquer lado, afastar o eixo só soma M d ao quadrado. Segundo, o erro clássico: o teorema parte sempre do centro de massa. Entre dois eixos fora dele, somar M d ao quadrado dá errado: A e B têm o mesmo I, mas essa conta daria um B bem maior. E a conferência: um doze avos mais um quarto dá um terço.

[excited] Agora dá para voltar ao bastão. Ele tem duas metades de quarenta e dois centímetros: o cabo, de duzentos e cinquenta gramas, e a parte grossa, de seiscentos e cinquenta. A gente calcula cada metade pelo seu centro e soma o termo de eixos paralelos. Com o eixo na ponta do cabo, o centro do cabo está a vinte e um centímetros, e o da parte grossa a sessenta e três. Dá zero vírgula dois oito dois quilogramas metro ao quadrado. Com o eixo na ponta grossa, é o contrário: a parte grossa fica a vinte e um, e o cabo a sessenta e três. Dá zero vírgula um quatro um. Exatamente a metade. A parte grossa, com quase três quartos da massa, está a sessenta e três centímetros do eixo num caso e a vinte e um no outro: três vezes mais perto, nove vezes menos no quadrado. Esse é o segredo.

[thoughtful] Um atalho que vale ouro, mas só para placas finas, planas. Coloca a placa no plano x y e o eixo z saindo perpendicular dela. A distância de um pedaço ao eixo z é raiz de x ao quadrado mais y ao quadrado, por Pitágoras. Então r ao quadrado é x ao quadrado mais y ao quadrado, e a soma de m r ao quadrado se divide em duas.

[thoughtful] E repara: a soma de m vezes y ao quadrado é justamente o momento de inércia em torno do eixo x, porque o y de cada pedaço é a distância dele ao eixo x. O mesmo para m x ao quadrado e o eixo y. Então o momento de inércia em torno do eixo perpendicular é a soma dos outros dois. Isso só funciona para placas, onde todo ponto tem z igual a zero.

[excited] Olha o prêmio. No disco, os eixos x e y no diâmetro são equivalentes, por simetria. Então os dois momentos de inércia são iguais, e a soma deles é o do eixo perpendicular: meio M R ao quadrado. Cada um vale um quarto de M R ao quadrado. Sem nenhuma integral. E no aro, pelo diâmetro, dá meio M R ao quadrado.

[thoughtful] E dá para usar a mesma ideia na esfera, como uma conferência independente. Somando os três momentos de inércia, cada ponto contribui com y ao quadrado mais z ao quadrado, mais x ao quadrado mais z ao quadrado, mais x ao quadrado mais y ao quadrado: duas vezes r ao quadrado, com r a distância ao centro. Na esfera, os três são iguais, então I é dois terços da integral de r ao quadrado d m. Na casca fina, r é R: dois terços de M R ao quadrado. Na maciça, a integral dá três quintos, e dois terços de três quintos é dois quintos: o mesmo resultado dos discos empilhados, por outro caminho.

[thoughtful] Primeiro exercício. Um carretel, que a gente vai tratar como um disco maciço de dois quilos e dez centímetros de raio, gira em torno de um eixo fixo, sem atrito. Uma corda leve está enrolada nele, e na ponta tem um bloco de um quilo. Solta do repouso. Qual é a velocidade do bloco depois de descer um metro? A corda não escorrega.

[thoughtful] Aqui a energia resolve rápido. A energia potencial que o bloco perde vira dois pedaços de energia cinética: a do bloco, que desce, e a do carretel, que gira. E a corda não escorrega, então a velocidade do bloco é igual à velocidade angular vezes o raio.

[excited] O momento de inércia do disco é meio M R ao quadrado. E ômega é v sobre R. Quando você substitui, o R ao quadrado do momento de inércia cancela o R ao quadrado do denominador, e a energia do carretel vira um quarto de M v ao quadrado. Olha que bonito: o raio sumiu. É como se o carretel fosse uma massa extra, de M sobre dois, andando junto com o bloco.

[thoughtful] Agora substitui: duas vezes um, vezes nove vírgula oito, vezes um, sobre um mais dois sobre dois. Dá nove vírgula oito dentro da raiz quadrada. Tirando a raiz, a velocidade é três vírgula treze metros por segundo. Dividindo pelo raio de zero vírgula um metro, a velocidade angular é trinta e um vírgula três radianos por segundo. Por isso a animação está em câmera lenta.

[thoughtful] Para conferir, olha a divisão da energia. De nove vírgula oito joules disponíveis, quatro vírgula nove vão para o bloco e quatro vírgula nove para o carretel. Metade e metade, e isso não é coincidência: o carretel conta como M sobre dois, que aqui é um quilo, igual à massa do bloco. E o bloco desce a três vírgula treze, menos que os quatro vírgula quarenta e três de uma queda livre, porque parte da energia ficou no giro.

[thoughtful] Uma pergunta para fixar: e se o carretel fosse um aro, de mesma massa e mesmo raio? O momento de inércia dobra, o carretel passa a valer uma massa extra de M inteira, e o bloco desce a dois vírgula cinquenta e seis. Fica a dica: quando uma corda não escorrega, escreve tudo em termos de v, e trata o momento de inércia dividido pelo raio ao quadrado como uma massa extra somada à do bloco.

[curious] Segundo exercício. Uma haste uniforme de um metro, presa na base por um pino sem atrito, está quase em pé. A gente solta do repouso, com uma inclinação tão pequena que pode ser desprezada. Qual é a velocidade da ponta ao alcançar a horizontal, imediatamente antes de tocar o chão? E ela chega mais rápida ou mais devagar que uma pedra solta da mesma altura?

[thoughtful] A energia potencial que a haste perde é a do centro de massa, que desce meio comprimento: M g L sobre dois. Ela vira energia de rotação em torno do pino. E o momento de inércia em torno do pino é o da barra pela ponta, M L ao quadrado sobre três, que a gente calculou no começo.

[excited] Cancela a massa, e a velocidade angular é raiz de três g sobre L: cinco vírgula quarenta e dois radianos por segundo. A ponta anda ômega vezes L, ou seja, cinco vírgula quarenta e dois metros por segundo. Uma pedra solta de um metro chega com quatro vírgula quarenta e três. A ponta da haste chega mais rápido que a pedra.

[thoughtful] E tem um ponto especial. Se a gente compara cada ponto da haste com uma pedra solta da altura dele, só o ponto que está a dois terços do comprimento chega igualzinho à pedra. Acima disso, o ponto ganha da queda livre. Abaixo, perde. É a velocidade crescendo linearmente com a distância ao pino, contra uma raiz.

[thoughtful, emphatic] Cuidado: comparamos velocidades finais, não tempos de queda. A haste não está em queda livre: o pino exerce forças que mudam o movimento de cada ponto. Mas o pino é fixo, então o ponto onde ele empurra não se desloca, e essa força não realiza trabalho. Por isso a conservação da energia basta para achar a velocidade final.

[thoughtful] Última variação: prende na ponta uma bolinha tão pequena que podemos tratá-la como massa pontual, com a mesma massa da haste. O momento de inércia passa de um terço para quatro terços de M L ao quadrado. A energia disponível sobe de meio para três meios de M g L. Resultado: a ponta chega a quatro vírgula setenta metros por segundo, menor que antes, mas ainda maior que na queda livre. A bolinha acrescentou energia, mas aumentou ainda mais a inércia.

[curious] Terceiro exercício, o mais completo. Uma placa circular de trinta centímetros de raio, da qual a gente tirou um recorte circular com metade do raio, encostado na borda e passando pelo centro O. A placa que sobrou tem um quilo e meio, mas o disco inteiro teria dois quilos. O eixo é horizontal, perpendicular à placa, passando por O. A gente solta de uma posição em que a linha do centro de massa até O está na horizontal. Qual é a velocidade angular quando o centro de massa passa embaixo de O? Eixo ideal, sem atrito.

[thoughtful] Plano: o momento de inércia é uma soma, então a gente pode somar com sinal. Momento de inércia do disco inteiro, menos o do pedaço que foi retirado. O disco inteiro, em torno de O, é meio M zero R ao quadrado: zero vírgula zero nove quilogramas metro ao quadrado. O pedaço retirado tem um quarto da área, então um quarto da massa: meio quilo.

[excited] Mas atenção: o momento de inércia do recorte tem que ser em torno de O, não do centro dele. Eixos paralelos: meio m vezes R sobre dois ao quadrado, mais m vezes R sobre dois ao quadrado, porque o centro dele está a R sobre dois de O. Dá três trinta e dois avos de M zero R ao quadrado. Tira do disco inteiro e sobra treze trinta e dois avos: zero vírgula zero sete três quilogramas metro ao quadrado. Em termos da massa que sobrou, treze vinte e quatro avos de M R ao quadrado.

[thoughtful] Onde está o centro de massa? A mesma ideia de massa negativa. O disco inteiro tem o centro de massa em O. O recorte, de massa negativa, está a R sobre dois. A média ponderada dá menos R sobre seis: cinco centímetros de O, do lado oposto ao recorte. É essa distância que faz a placa virar um pêndulo.

[thoughtful] Agora a energia. O centro de massa desce R sobre seis: cinco centímetros. A energia potencial perdida é M g R sobre seis, e vira energia de rotação em torno de O: meio I O ômega ao quadrado. Cancela a massa, e ômega ao quadrado é oito g sobre treze R. Com R de trinta centímetros, dá quatro vírgula quarenta e oito radianos por segundo.

[thoughtful] O centro de massa passa a vinte e dois centímetros por segundo, e os pontos mais afastados do eixo, a um vírgula trinta e quatro metros por segundo. Conferência: o momento de inércia em torno do próprio centro de massa dá trinta e sete setenta e dois avos de M R ao quadrado, que é menor que o de O. E somando M vezes R sobre seis ao quadrado, volta exatamente ao de O. Os teoremas se fecham.

[thoughtful, emphatic] Uma observação final. Se o eixo passasse pelo centro de massa, a energia potencial não mudaria em posição nenhuma, e a placa ficaria parada onde você deixasse. O recorte é o que a transforma num pêndulo. Aqui, o que importa é a combinação: massa negativa para o centro de massa e para o momento de inércia, eixos paralelos para levar tudo ao mesmo eixo, e conservação da energia.

[happy] Pra fechar, três cartões. Um: o momento de inércia é a soma de cada massa vezes o quadrado da sua distância ao eixo, e muda com o eixo. Dois: a energia cinética de rotação é meio I ômega ao quadrado. Três: dois atalhos, eixos paralelos a partir do centro de massa, e eixos perpendiculares para placas.

[thoughtful] E a resposta do começo. A parte grossa concentra a maior parte da massa do bastão. Com o eixo no cabo, o centro dela fica a sessenta e três centímetros do eixo; com o eixo na ponta grossa, a vinte e um. O termo de eixos paralelos dela, massa vezes distância ao quadrado, cai nove vezes. Mas o cabo faz o contrário: passa a ficar longe, e o termo dele sobe. A soma dos dois pedaços muda por um fator dois. Mesma massa, mesma velocidade angular, o dobro da energia.

[happy] Se esse vídeo te ajudou, se inscreve no canal para acompanhar os próximos. E fica de olho nos comentários, que eu deixei um desafio para você.

[curious] O desafio. Um cilindro maciço e um cilindro oco de parede fina, com a mesma massa e o mesmo raio, descem a mesma rampa rolando sem escorregar. Quem chega primeiro? Usa o fator da tabela, o c, e escreve sua resposta aqui embaixo. A gente vai explorar isso no módulo de rolamento.
