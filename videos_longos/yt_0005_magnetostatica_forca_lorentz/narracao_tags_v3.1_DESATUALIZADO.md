# yt_0005 — Narração com audio tags (Eleven v4)

Cópia de `narracao_sugestao.md` (v3.1, texto-base congelado): o texto falado é idêntico, só com tags `[ ]` inseridas.
Regras: uma tag por frase, em inglês, fora da legenda e do `.srt`; base `[thoughtful]`/`[curious]`; `[excited]` só nas descobertas; `[slow, measured pace]` nos conceitos-chave; `[calm, satisfied]` no fechamento. Se uma tag soar errada ou for lida em voz alta, apague-a ou troque por uma vizinha e gere de novo.
Status: **só simulação (`--seco`); voz não gerada.**

## Texto corrido (para gravação)

[curious] Fala, pessoal! Bem-vindos de volta ao Parallax Lab. Hoje o assunto é magnetostática, e a gente começa por uma pergunta simples: o que um campo magnético realmente faz?

[thoughtful] Pega dois fios de metal, paralelos, neutros como um todo, e faz passar uma corrente em cada um, no mesmo sentido.

[thoughtful] Os dois fios se atraem, sem que ninguém encoste neles: existe uma interação à distância.

[thoughtful] Inverte o sentido da corrente em um dos fios, e a interação muda: em vez de atração, repulsão.

[curious] Cada fio, como um todo, é neutro, e mesmo assim existe transporte de carga. Mudar o sentido desse transporte muda a própria interação. Então a corrente carrega alguma informação física essencial aqui. A pergunta é: o que, no movimento das cargas, produz essa interação?

[thoughtful] Pra responder, a gente aproxima a imagem até enxergar uma única carga em movimento, e entende o que o campo magnético faz com ela.

[thoughtful] Aqui está uma carga elétrica, que na tela aparece como q, positiva, se movendo com uma certa velocidade dentro de um campo magnético. As linhas de campo são só um jeito de desenhar o campo: a carga passa por elas sem esbarrar em nada.

[thoughtful] A força de Lorentz sobre uma carga tem duas partes: uma do campo elétrico, que existe mesmo com a carga parada, e outra do campo magnético, que só existe se a carga está em movimento.

[thoughtful] Hoje o foco é a segunda parte, a força magnética: a carga multiplicada pelo produto vetorial entre o vetor velocidade e o campo magnético.

[curious] O produto vetorial dá um vetor perpendicular ao plano da velocidade e do campo. Mas isso deixa dois sentidos possíveis. Como escolher?

[thoughtful] Pela regra da mão direita, e a ordem importa: primeiro a velocidade, depois o campo magnético. Dedos no sentido da velocidade, fechando em direção ao campo: o polegar mostra o sentido do produto vetorial, que, para carga positiva, é o da força magnética.

[thoughtful] Aqui o resultado entra na tela, e o xis dentro do círculo representa isso: a parte de trás de uma seta entrando. Se a força saísse da tela, o símbolo seria um ponto dentro do círculo: a ponta da seta vindo na nossa direção.

[thoughtful] O módulo da força é o módulo da carga, vezes a rapidez, vezes a intensidade do campo, vezes o seno do ângulo entre a velocidade e o campo. Rapidez, e não velocidade: no módulo entra só o tamanho do vetor.

[thoughtful] Mantendo fixos o módulo da carga, a rapidez e o campo, só o ângulo muda a força: quanto menor o ângulo, menor o seno e menor a força.

[thoughtful] Nos extremos, a força é nula: com a velocidade paralela ao campo o ângulo é zero; antiparalela, cento e oitenta graus; e com a carga parada, a rapidez é zero.

[thoughtful] E com a velocidade perpendicular ao campo, o seno vale um e a força é a máxima possível.

[thoughtful] Para o sinal da carga: o produto vetorial é o mesmo, mas a força é a carga vezes esse produto. Então, para carga negativa, aplica-se a mesma regra da mão direita e inverte-se o sentido.

[thoughtful] O módulo é o mesmo; só o sentido muda: de entrar na tela para sair dela.

[thoughtful] Dá pra organizar isso decompondo a velocidade em uma componente paralela e uma perpendicular ao campo.

[thoughtful] A paralela, no produto vetorial com o campo, dá zero: não contribui em nada.

[thoughtful] Toda a força magnética vem da componente perpendicular: a carga vezes essa componente, em produto vetorial com o campo. É a mesma força, escrita de forma mais econômica.

[thoughtful] Pra estudar o movimento, vamos escolher um caso: a componente paralela da velocidade vale zero. É uma condição inicial nossa, não uma regra da natureza, e mais adiante a gente tira essa restrição.

[thoughtful] Agora olhamos ao longo da direção do campo: as linhas viram pontinhos saindo da tela. A perspectiva muda, a física não.

[thoughtful] Escolhemos os eixos com o campo ao longo do eixo x. A velocidade tem então três componentes: uma ao longo do campo, e duas no plano perpendicular, uma horizontal e uma vertical.

[thoughtful] Três hipóteses, válidas pra toda essa análise. O campo é uniforme: mesma intensidade e direção em toda a região. É constante: não varia no tempo. E o regime é não relativístico: velocidades pequenas comparadas com a da luz, de modo que a dinâmica de Newton vale. E só a força magnética atua.

[curious] A pergunta é: como cada componente da velocidade produz aceleração nas outras direções? O produto vetorial entre a velocidade e o campo responde, e a gente calcula com um determinante: vetores unitários na primeira linha, componentes da velocidade na segunda, componentes do campo na terceira.

[thoughtful] Na direção do campo, tudo fica multiplicado por zero: não há força ao longo do campo.

[thoughtful] Na direção horizontal, sobra a componente ao longo do campo vezes zero, menos a componente vertical vezes o campo. O menor vale menos o campo vezes a componente vertical, mas a posição no determinante traz um sinal negativo. Menos vezes menos dá mais: resultado positivo.

[thoughtful] Na direção vertical, o menor vale menos o campo vezes a componente horizontal, e a posição não acrescenta sinal: fica negativo.

[slow, measured pace] Juntando: nada ao longo do campo; na horizontal, o campo vezes a componente vertical; na vertical, menos o campo vezes a componente horizontal. Cada componente da velocidade controla a aceleração na outra direção. Guarda essa troca: tudo o que vem depois nasce dela. Isto ainda é só o produto vetorial: falta multiplicar pela carga.

[thoughtful] Entra a segunda lei de Newton: a massa vezes a aceleração é a força total, que aqui é só a magnética, já multiplicada pela carga. Até agora a lei de Lorentz dizia pra onde a força aponta; com Newton, ela passa a determinar o movimento.

[thoughtful] Saem três equações. Na primeira, a aceleração ao longo do campo é zero: essa componente é constante.

[thoughtful] Nas outras duas, a aceleração horizontal é o fator carga vezes campo dividido pela massa, multiplicado pela componente vertical da velocidade; e a vertical é menos esse fator vezes a componente horizontal. Uma componente alimenta a outra, com sinal oposto, e é esse sinal que vai produzir oscilação. Componente negativa só indica sentido negativo do eixo; rapidez negativa não existe.

[thoughtful] Temos duas funções misturadas, e queremos uma equação com só uma delas. Derivamos, no tempo, a equação da componente horizontal. O fator carga vezes campo dividido pela massa sai da derivada, porque é constante.

[thoughtful] Sobrou a derivada da componente vertical, que a terceira equação já nos dá. Substituímos: o mesmo fator reaparece, agora com sinal negativo, multiplicando a componente horizontal.

[thoughtful] O fator fica ao quadrado, com sinal negativo. Passando tudo pro mesmo lado: a segunda derivada da componente horizontal, mais esse fator ao quadrado vezes a própria componente, igual a zero. É a equação do oscilador harmônico, e quem a obedece é uma componente da velocidade; a partícula não está presa a mola nenhuma. Só a estrutura matemática é a mesma.

[thoughtful] Nessa forma, a constante ao quadrado é a frequência angular ao quadrado: a taxa com que a fase avança, em radianos por segundo.

[thoughtful] Tomando o valor positivo, que mede o quão rápido a fase gira, e deixando o sentido da rotação pro sinal da carga: a frequência angular é o módulo da carga vezes o campo, dividido pela massa. [excited] Esta é a frequência angular ciclotrônica, e ela nasceu da equação de movimento. Dividindo por dois pi, teríamos voltas por segundo; aqui trabalhamos em radianos por segundo.

[thoughtful] Maior módulo da carga, campo mais intenso ou massa menor: giro mais rápido.

[curious] Qual função, derivada duas vezes, volta com o sinal trocado e multiplicada pela frequência ao quadrado?

[thoughtful] O seno resolve: a segunda derivada do seno de frequência vezes tempo é menos a frequência ao quadrado vezes o próprio seno. O cosseno também.

[thoughtful] Como a equação é linear, qualquer combinação serve: a primeira constante vezes cosseno, mais a segunda constante vezes seno. As condições iniciais vão fixar essas duas constantes.

[thoughtful] Pra carga positiva da tela: componente horizontal inicial zero, vertical inicial igual à velocidade perpendicular. Com a horizontal zero no instante inicial, o cosseno vale um e o seno zero, então a primeira constante é zero.

[thoughtful] A condição da componente vertical entra pela equação acoplada: no instante inicial, a aceleração horizontal é a frequência angular vezes a componente vertical, que vale a velocidade perpendicular. Do outro lado, a derivada da solução é a frequência angular vezes a segunda constante. Logo a segunda constante é a velocidade perpendicular. Uma condição sobre a componente vertical fixou a constante da horizontal: é o acoplamento.

[thoughtful] A componente vertical sai da mesma equação acoplada: é a derivada da horizontal dividida pela frequência angular.

[thoughtful] Resultado: horizontal igual à velocidade perpendicular vezes seno, vertical igual à velocidade perpendicular vezes cosseno.

[thoughtful] Duas figuras diferentes. No cartão de cima, a trajetória real: o ponto é a posição da partícula. No de baixo, o espaço das velocidades: o ponto não é posição, as coordenadas são as duas componentes da velocidade, e o vetor parte da origem com comprimento igual à rapidez perpendicular. À direita, os gráficos, no mesmo instante.

[thoughtful] Seno e cosseno, defasados em noventa graus: quando um está no máximo, o outro passa por zero. A ponta do vetor percorre um círculo.

[thoughtful] Somando os quadrados das componentes, sobra a velocidade perpendicular ao quadrado, porque seno ao quadrado mais cosseno ao quadrado vale um. A direção muda sempre, a rapidez não. Isso não quer dizer que não há aceleração: a força magnética muda continuamente a direção do vetor velocidade sem aumentar nem diminuir a rapidez.

[thoughtful] Com carga negativa e as mesmas condições iniciais, a órbita e o vetor giram no sentido contrário: a componente horizontal troca de sinal e a vertical continua um cosseno. A frequência tem o mesmo módulo. O módulo da carga decide a rapidez do giro; o sinal, o sentido.

[curious] Onde está a partícula? Já sabemos como a velocidade varia; falta ligá-la à trajetória. A velocidade é a taxa de variação da posição, então, pra recuperar a posição, a gente integra.

[thoughtful] Integramos a componente horizontal da velocidade, de zero até o instante observado. O tempo dentro da integral é só uma variável auxiliar; o limite de cima é o instante que importa.

[thoughtful] A primitiva do seno é menos cosseno dividido pela frequência angular: a divisão vem de a derivada do cosseno trazer esse fator. A constante de integração se cancela nos limites.

[thoughtful] Avaliando os dois limites, o cosseno em zero vale um, e daí o um menos cosseno. A posição horizontal menos a inicial é a velocidade perpendicular sobre a frequência angular, vezes um menos cosseno.

[thoughtful] Repetindo para a componente vertical, a integral do cosseno dá o seno.

[thoughtful] Nas duas coordenadas aparece o mesmo fator, a velocidade perpendicular dividida pela frequência angular, que é a distância percorrida por radiano de fase. Ele será o raio da órbita.

[thoughtful] Queremos reconhecer a curva sem depender do instante. Como as coordenadas têm seno e cosseno da mesma fase, passamos o raio pro outro lado, elevamos ao quadrado e somamos: seno ao quadrado mais cosseno ao quadrado vale um, e o tempo desaparece.

[thoughtful] Sobra a equação de uma circunferência, com centro e raio que saem da álgebra. [excited] A trajetória circular não foi suposta: saiu da lei de Lorentz com a segunda lei de Newton.

[thoughtful] Com a frequência já conhecida, o raio é a massa vezes a velocidade perpendicular, dividido pelo módulo da carga vezes o campo. Maior massa ou velocidade perpendicular: órbita maior. Maior módulo da carga ou campo mais intenso: órbita mais fechada.

[curious] E a componente ao longo do campo? A primeira equação já respondeu: é constante. Se for zero, temos só o círculo.

[thoughtful] Na imagem, se não for zero, o círculo avança ao longo do campo e sai uma hélice. Vamos fechar primeiro o período e voltar a essa ideia com calma.

[thoughtful] Um ponto importante: neste problema, a força magnética não cria nem altera essa componente. Ela já estava na condição inicial e permanece constante.

[thoughtful] Voltando ao círculo: a força magnética é perpendicular à velocidade, então só muda a direção.

[thoughtful] Dá pra conferir o raio por outro caminho. Força centrípeta não é uma força nova: é o nome do papel da resultante quando ela aponta pro centro da trajetória circular, e aqui esse papel é da força magnética. Igualando o módulo dela à massa vezes a rapidez ao quadrado dividida pelo raio, sai o mesmo raio: dois caminhos, mesmo resultado.

[thoughtful] O período é o tempo de uma volta: o comprimento da circunferência, dois pi vezes o raio, dividido pela velocidade perpendicular. Substituindo o raio, a velocidade perpendicular aparece em cima e embaixo e se cancela: sobra dois pi vezes a massa, dividido pelo módulo da carga vezes o campo.

[excited] A velocidade sumiu. Uma partícula mais rápida percorre uma circunferência maior, e o raio cresce na mesma proporção, então o tempo da volta é o mesmo. Comparando partículas no mesmo campo magnético, com a mesma massa e o mesmo módulo de carga, isso vale no regime não relativístico.

[thoughtful] Duas partículas, mesma massa, mesmo módulo de carga, mesmo campo, velocidades perpendiculares diferentes: raios diferentes, e mesmo assim passam juntas pelo ponto de partida a cada período. Períodos iguais.

[thoughtful] Voltamos à ideia em aberto. Nova condição inicial: a velocidade tem uma componente paralela ao campo diferente de zero, já definida desde o instante inicial.

[thoughtful] Ao longo do campo, a partícula avança com velocidade constante; no plano perpendicular, continua girando. [excited] Círculo mais translação é uma hélice: a mesma solução de Lorentz, com a componente paralela diferente de zero.

[thoughtful] As duas componentes não se misturam: cada uma segue a sua equação.

[thoughtful] A hélice tem o raio, que vem da componente perpendicular, e o passo: a distância, medida ao longo do eixo, entre dois pontos correspondentes separados por uma volta. Não é o comprimento sobre a curva. Como é distância, usa-se o módulo da componente paralela: o passo é esse módulo vezes o período, dois pi vezes a massa vezes o módulo da componente paralela, dividido pelo módulo da carga vezes o campo.

[thoughtful] Comparando condições iniciais diferentes, não uma mesma partícula mudando: com velocidade perpendicular menor, o raio diminui e o passo continua o mesmo, porque o período não mudou.

[thoughtful] Com a componente paralela maior, o passo cresce e o raio fica igual.

[thoughtful] Casos limite: componente paralela zero, círculo; componente perpendicular zero, nenhuma força e movimento retilíneo uniforme ao longo do campo.

[thoughtful] Com carga negativa, mesma massa e mesmas condições iniciais, ela gira ao contrário e avança igual ao longo do campo. Raio, período e passo não mudam.

[thoughtful] Retomamos o círculo, com a componente paralela igual a zero, e a pergunta que precisamos responder.

[curious] A partícula acelera, porque a direção da velocidade muda sempre. Então por que não fica mais rápida? Porque existe aceleração sem mudança de rapidez: o vetor gira, e o módulo dele, a rapidez, fica o mesmo, como mostra o medidor.

[thoughtful] Pra entender, usamos trabalho. A velocidade é tangente à trajetória e a força magnética aponta pro centro: formam um ângulo reto.

[thoughtful] O trabalho num pequeno deslocamento é o produto escalar entre a força e o deslocamento, que seleciona a componente da força na direção do deslocamento. Só ela transfere energia mecânica; a componente perpendicular não realiza trabalho nesse deslocamento.

[thoughtful] Dividindo o trabalho por um pequeno intervalo de tempo, no limite, temos a taxa instantânea: a potência.

[thoughtful] Aparece a derivada do deslocamento no tempo, que é a velocidade: a potência de qualquer força é o produto escalar entre a força e a velocidade.

[thoughtful] Para a força magnética, a carga vezes o produto vetorial da velocidade pelo campo, em produto escalar com a velocidade.

[thoughtful] Mas esse produto vetorial é perpendicular à velocidade, então o produto escalar é zero: [excited] potência magnética nula em todo instante.

[slow, measured pace] O trabalho é a integral da potência: zero também. Atenção: trabalho nulo não é força nula. A força pode ser grande e mudar muito a direção, com trabalho zero. E a conclusão vem só da perpendicularidade entre força e velocidade: não depende de a trajetória ser circular nem de o campo ser uniforme.

[thoughtful] A energia cinética é metade da massa vezes a rapidez ao quadrado.

[thoughtful] Pelo teorema do trabalho e energia, a variação da energia cinética é o trabalho total. Só a força magnética atua, então a energia cinética e a rapidez ficam constantes.

[thoughtful] Se outra força realizasse trabalho, a energia cinética poderia mudar, mesmo com trabalho magnético nulo.

[thoughtful] Isso não quer dizer que um motor não transfira energia. A energia vem da fonte elétrica; o campo elétrico realiza trabalho sobre as cargas, e as forças sobre os portadores são transmitidas ao material. A parcela magnética sobre cada carga não realiza trabalho.

[thoughtful] Vamos levar isso a um fio. Cada carga em movimento sente a força magnética, e um fio contém muitíssimos portadores móveis. Pra simplificar, representamos os portadores como cargas positivas efetivas.

[thoughtful] Num metal real são elétrons, negativos, indo no sentido oposto ao da corrente convencional. Mas a contribuição pra corrente depende do produto da carga pela velocidade: invertendo os dois, o sentido da corrente convencional é o mesmo. Por isso esse modelo é legítimo como representação da corrente convencional.

[thoughtful] Num pequeno trecho do fio, de um pequeno elemento de comprimento, há uma pequena quantidade de carga dos portadores.

[thoughtful] Com lambda, a densidade linear de carga dos portadores, essa quantidade é lambda vezes o elemento de comprimento. É a densidade dos portadores, não a carga líquida do fio: um fio pode ser neutro e ter corrente.

[thoughtful] Corrente é a carga que atravessa uma seção por unidade de tempo: a taxa de transporte de carga.

[thoughtful] Num pequeno intervalo de tempo, cada portador percorre a velocidade de deriva vezes esse intervalo, e não a agitação térmica, que em média não transporta carga numa direção. A carga que cruza a seção é lambda vezes a velocidade de deriva vezes o intervalo.

[thoughtful] O intervalo se cancela: a corrente é lambda vezes a velocidade de deriva.

[thoughtful] A força no trecho é a pequena quantidade de carga vezes a velocidade, em produto vetorial com o campo.

[thoughtful] Trocando a carga por lambda vezes o elemento de comprimento, e lambda vezes a velocidade pela corrente: a força no trecho é a corrente vezes o elemento de comprimento, no sentido da corrente, em produto vetorial com o campo.

[thoughtful] Somamos todos os trechos: a força sobre o fio inteiro é uma integral.

[thoughtful] A força age sobre os portadores, e as interações deles com a rede do material transferem essa força ao corpo do condutor: é assim que a força sobre cargas móveis vira força sobre o fio. Os elétrons não descrevem órbitas livres como antes: eles colidem com o material.

[curious] E se o condutor é uma lâmina? A corrente se espalha pela largura.

[thoughtful] A densidade superficial de corrente, que na tela aparece como K, é a corrente por unidade de largura transversal ao escoamento: uma faixa estreita carrega uma pequena corrente igual a esse módulo vezes a largura.

[thoughtful] Do lado da carga, sigma, a densidade superficial de carga: a carga de um elemento de área é sigma vezes a área.

[thoughtful] Para uma espécie de portador, a densidade superficial de corrente é sigma vezes a velocidade.

[thoughtful] Com espessura, o condutor é um volume.

[thoughtful] A densidade de corrente, que na tela aparece como J, é a corrente por unidade de área transversal ao escoamento; uma fatia dela é seu módulo vezes a área perpendicular.

[thoughtful] Somando as fatias sobre uma superfície, a corrente total é a integral do produto escalar entre a densidade de corrente e o elemento vetorial de área, orientado pela normal. Em superfície inclinada, o produto escalar seleciona só a componente que atravessa.

[thoughtful] Do lado da carga, rô, a densidade volumétrica de carga: a carga de um pequeno elemento de volume é rô vezes o volume, e, para uma espécie de portador, a densidade de corrente é rô vezes a velocidade.

[thoughtful] Com várias espécies, somamos as contribuições, cada uma com seu sinal e sua velocidade: carga negativa indo pra esquerda contribui como corrente pra direita. Mesmo com carga líquida zero, a densidade de corrente pode não ser zero.

[thoughtful] Não são três leis: é a mesma interação escrita pra um fio, uma lâmina e um volume. A corrente é a taxa de transporte de carga; a densidade superficial a distribui pela largura; a densidade de corrente a distribui por área, e o fluxo dela recupera a corrente total.

[thoughtful] Até aqui o interesse era a corrente estacionária. Agora permitimos, temporariamente, que entrada e saída de carga sejam diferentes, pra entender a conservação da carga na forma geral; depois voltamos ao estacionário. Olha a densidade de corrente como setas verdes.

[thoughtful] Fluxo mede quanto de uma grandeza atravessa uma superfície, levando em conta a orientação. Aqui a grandeza é a carga: a corrente através da superfície é o fluxo da densidade de corrente, a integral do produto escalar com o elemento vetorial de área.

[thoughtful] Num pequeno intervalo, atravessa a carga contida na fatia de espessura velocidade vezes intervalo.

[thoughtful] Fechando a superfície, ela vira a fronteira de um volume de controle: uma região matemática, não um pedaço de material. Dentro há os portadores; pela fronteira, a densidade de corrente entra de um lado e sai do outro. É a mesma ferramenta dos vídeos de Gauss, superfície fechada, normais e fluxo, mas agora num balanço de conservação.

[thoughtful] O balanço é de contabilidade: a variação da carga dentro é o que entra menos o que sai. Os medidores mostram a corrente de entrada, a de saída, a taxa de variação e a carga dentro. A animação está em câmera lenta, mas a lei é a mesma.

[thoughtful] Entrada igual à saída: a taxa é zero e a carga dentro fica constante.

[thoughtful] Saída maior que entrada: a carga dentro diminui, com taxa negativa.

[thoughtful] Voltando a igualar, a taxa volta a zero.

[thoughtful] Entrada maior que saída: a carga dentro aumenta.

[thoughtful] O que entra ou fica armazenado ou sai: a carga não aparece nem some.

[thoughtful] Usamos a normal que aponta pra fora. Na entrada, a densidade de corrente aponta contra a normal e o produto escalar é negativo; na saída, é positivo.

[thoughtful] A integral na fronteira inteira é o fluxo líquido pra fora: o que sai menos o que entra.

[thoughtful] A variação da carga dentro é menos esse fluxo: se o fluxo líquido pra fora é positivo, a carga armazenada diminui. A conservação é a igualdade completa entre os dois balanços.

[thoughtful] A carga dentro é a integral da densidade volumétrica de carga em todo o volume.

[thoughtful] O volume é fixo, então só a densidade pode variar no tempo.

[thoughtful] Forma integral: a taxa de variação da carga dentro é menos o fluxo da densidade de corrente pela fronteira. Uma metade é o que está dentro, a outra o que atravessa.

[thoughtful] Agora o teorema da divergência, uma identidade matemática: o fluxo através de uma fronteira fechada é a integral, no volume, do divergente do campo. O divergente da densidade de corrente mede a taxa líquida de saída de carga por unidade de volume, no limite de uma região muito pequena. O líquido importa: pode haver corrente atravessando uma região de divergente zero, se entra tanto quanto sai.

[thoughtful] Nestas células, entra e sai o mesmo: divergente zero.

[thoughtful] Com volume fixo, a derivada entra na integral como derivada parcial: a taxa local de variação da densidade de carga. Então a integral dessa taxa mais o divergente da densidade de corrente é zero.

[thoughtful] Passo sutil: uma integral nula num volume poderia vir de cancelamentos. Mas vale pra qualquer volume, em qualquer lugar; então, com regularidade, o que está dentro da integral é zero em cada ponto. Daí vem a equação local.

[thoughtful] O divergente da densidade de corrente é menos a taxa local de variação da densidade de carga: [excited] a equação da continuidade, a conservação da carga ponto a ponto. Teorema da divergência é identidade matemática; conservação da carga e lei de Gauss são afirmações físicas distintas.

[thoughtful] No regime estacionário, o da magnetostática, a densidade de carga em cada ponto não muda no tempo: a taxa local é zero, e o divergente da densidade de corrente também.

[slow, measured pace] Corrente estacionária não é corrente nula: ela existe e passa carga, mas nada se acumula em lugar nenhum. Também não significa ausência de portadores. Entra e sai à mesma taxa, ponto a ponto.

[thoughtful] Voltamos a uma carga, agora com dois campos. O objetivo: ver como duas forças opostas podem se cancelar e deixar a carga atravessar sem desvio.

[thoughtful] Novos eixos, adequados ao aparelho, diferentes do bloco anterior: a velocidade da carga é ao longo do eixo horizontal.

[thoughtful] Entre duas placas, um campo elétrico na vertical; na mesma região, um campo magnético saindo da tela.

[thoughtful] O campo elétrico empurra a carga positiva pra cima: força elétrica é a carga vezes o campo elétrico, e o módulo não depende da rapidez.

[thoughtful] O campo magnético empurra pra baixo: a carga vezes o produto vetorial da velocidade pelo campo, e a regra da mão direita confere. Esse módulo cresce com a rapidez.

[thoughtful] Uma força constante pra cima, outra pra baixo crescendo com a rapidez: existe uma rapidez em que os módulos se igualam e as forças se cancelam. [excited] Esse cancelamento é o coração do seletor: dá pra selecionar uma rapidez ajustando os campos. A força vertical é a carga vezes: campo elétrico menos rapidez vezes campo magnético.

[thoughtful] Dividindo pela carga, sobra uma expressão só de campos e rapidez.

[thoughtful] No gráfico, o eixo horizontal é a rapidez e o vertical é a força vertical dividida pela carga. Pra carga positiva, o sinal dessa quantidade é o da força vertical; pra negativa, não, e já voltamos a isso.

[thoughtful] O ponto e o feixe dependem da mesma rapidez: ao aumentar, o ponto desce pela reta.

[thoughtful] Rapidez menor que a selecionada: ganha a força elétrica, e o feixe desvia pra cima.

[thoughtful] Rapidez maior: ganha a magnética, e desvia pra baixo. As curvas fora da condição selecionada são esquemáticas: mostram o sentido do desvio, não a solução completa.

[thoughtful] Onde a reta cruza o zero, a força líquida é nula, com rapidez igual ao campo elétrico dividido pelo campo magnético. Resultante zero não significa campos zero: as duas forças existem e se cancelam.

[slow, measured pace] O seletor não iguala velocidades: deixa passar sem desvio só quem já entrou com a rapidez apropriada; quem tem outra rapidez desvia, pra cima ou pra baixo.

[thoughtful] Com carga negativa, as duas forças invertem; fora da rapidez selecionada o desvio troca de lado, mas o cancelamento é o mesmo, porque o módulo da carga sai da conta.

[thoughtful] Partículas com a rapidez já determinada pelo seletor entram numa região só com campo magnético. Desligar o campo elétrico aqui não significa que o seletor funcione sem ele: ele já fez o trabalho.

[thoughtful] Sob só o campo magnético, a partícula descreve um arco de circunferência, e podemos medir o raio no desenho.

[thoughtful] É a mesma ideia do círculo do B02: a força magnética faz o papel de centrípeta: o módulo da carga vezes a rapidez vezes o campo, igual à massa vezes a rapidez ao quadrado dividida pelo raio.

[thoughtful] Cancelando uma rapidez, o módulo da carga vezes o campo é a massa vezes a rapidez dividida pelo raio.

[thoughtful] Isolando: a razão entre o módulo da carga e a massa é a rapidez dividida pelo produto do campo magnético e do raio.

[thoughtful] A rapidez vem do seletor: campo elétrico dividido pelo campo magnético. É aqui que o seletor se conecta ao raio. Com o mesmo módulo do campo magnético nas duas etapas, a razão fica o campo elétrico dividido pelo produto entre o quadrado do campo magnético e o raio.

[excited] Esse é o resultado da caixa.

[slow, measured pace] O que cada parte fornece: os campos conhecidos dão a rapidez; o raio dá a razão entre o módulo da carga e a massa; o sentido da curva dá o sinal da carga. O experimento não dá carga e massa separadas: dá a razão.

[thoughtful] A rapidez continua constante e o trabalho magnético é zero.

[thoughtful] As unidades, na tela, conferem: metros por segundo pra rapidez e coulombs por quilograma pra razão.

[thoughtful] Recapitulando: tudo partiu de uma lei, a força magnética, a carga vezes o produto vetorial da velocidade pelo campo.

[thoughtful] Sem componente paralela, a trajetória é um círculo na frequência angular ciclotrônica.

[thoughtful] Com componente paralela, o círculo avança e a trajetória é uma hélice.

[thoughtful] Quando há transporte organizado de carga, descrevemos esse movimento como corrente elétrica.

[thoughtful] Distribuído pelo volume, ele se descreve localmente pela densidade de corrente, que no regime estacionário tem divergente zero.

[thoughtful] E, numa carga individual, o seletor e a razão entre carga e massa.

[thoughtful] Voltando aos dois fios: a corrente em cada um é transporte organizado de carga. O campo magnético age sobre os portadores móveis, e a força é transmitida ao material.

[thoughtful] Com correntes no mesmo sentido, a força mostrada é de atração. Já sabemos como um campo conhecido age sobre uma corrente; falta saber de onde vem esse campo.

[curious] Como uma corrente cria um campo magnético?

[calm, satisfied] Essa pergunta leva à lei de Biot–Savart, tema do próximo vídeo. Se quiser acompanhar, se inscreve no canal. A gente se vê por lá!
