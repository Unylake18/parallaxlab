# Biot–Savart — narração condensada, com alvo de até 24 minutos

**Status:** proposta para aprovação. Esta substitui a versão expandida como proposta de produção; a anterior fica como referência explicativa. A prioridade é manter a explicação completa. Vinte e quatro minutos é o alvo editorial: se a locução compreensível e as pausas necessárias ultrapassarem esse tempo, registrar a duração real antes de decidir novos cortes.

**Base visual:** preview v4 de 17:38. Os tempos nas âncoras localizam eventos no preview; não são inícios da voz nem marcas exatas da montagem final. Os IDs N001–N083 foram preservados para facilitar a comparação com a versão expandida.

**Somente os parágrafos depois de Fala entram na voz.** Títulos, tempos, nomes dos eventos e orientações são editoriais. Grandezas são nomeadas pelo significado físico, sem letras soltas. A fala mantém as deduções, suas hipóteses e as conexões com Gauss; os cortes concentram-se em repetições, comentários laterais e leituras redundantes de fórmulas.

## B00 — Corrente, campo e força

### N001 | 00:00 | Pergunta inicial e primeiro fio

**Fala:**

Como calcular o campo magnético criado por uma corrente? No vídeo anterior, vimos a força sobre cargas em movimento. Hoje vamos partir da corrente, encontrar seu campo e calcular a força sobre outro fio. Bem-vindos ao Parallax Lab.

### N002 | 00:09 | Anéis de campo; relação entre corrente e campo

**Fala:**

O cinza representa o condutor; os marcadores verdes indicam a corrente convencional, sem escala de velocidade. Para um fio retilíneo muito longo, as linhas magenta são circunferências em planos perpendiculares ao fio. Suas setas indicam a direção do campo.

### N003 | 00:20 | Segundo fio e força magnética

**Fala:**

Colocamos um segundo fio paralelo ao primeiro. O campo do primeiro, tangente à circunferência, atua sobre a corrente do segundo. Para um trecho reto em campo uniforme, a força é a corrente multiplicada pelo produto vetorial entre o vetor comprimento e o campo. O vetor comprimento segue a corrente.

### N004 | 00:31 | Campo desconhecido; título da lei

**Fala:**

A lei experimental de Biot–Savart fornece esse campo. Vamos entender seus fatores e deduzir duas aplicações: o trecho reto e a espira circular.

## B01 — Regime magnetostático

### N005 | 00:46 | Volume atravessado pelo fio

**Fala:**

Magnetostática não significa cargas paradas. Elas circulam, mas a distribuição macroscópica de corrente permanece estável. Observe este volume imaginário atravessado pelo fio: se entra mais corrente do que sai, a carga dentro dele aumenta.

### N006 | 00:54 | Balanço da carga; entradas e saídas iguais

**Fala:**

A taxa de variação da carga é a corrente que entra menos a que sai. Quando elas se igualam, há transporte sem acúmulo líquido. O volume apenas delimita a região desse balanço.

### N007 | 01:13 | Equação da continuidade

**Fala:**

A equação da continuidade expressa a conservação local da carga. Ela relaciona a variação da densidade de carga ao divergente da densidade de corrente. A primeira é carga por volume; a segunda descreve direção do fluxo e corrente por área perpendicular. Divergente positivo significa saída líquida de corrente e diminuição da carga local.

### N008 | 01:21 | Divergente nulo; corrente independente do tempo

**Fala:**

Se a densidade de carga não varia, o divergente da densidade de corrente é zero. Exigimos também que a própria corrente não mude com o tempo. Ausência de acúmulo não prova, sozinha, corrente constante. Estudaremos essas fontes estacionárias, no vácuo ou aproximando o ar por vácuo.

## B02 — Fonte, observador e separação

### N009 | 01:35 | Fonte verde e ponto de observação

**Fala:**

Precisamos distinguir onde está a fonte e onde calculamos o campo. O ponto verde destaca um elemento da corrente. O ponto branco é o observador. Durante a integral, fixaremos o observador e percorreremos os elementos da fonte.

### N010 | 01:46 | Origem e dois vetores de posição

**Fala:**

Escolhemos uma origem. Um vetor localiza a fonte; outro, o observador. A pequena marca distingue o símbolo da posição da fonte. Esses vetores dependem da origem, mas a separação física entre os pontos não depende dessa escolha.

### N011 | 01:55 | Soma dos caminhos; diferença de posições

**Fala:**

Há dois caminhos da origem ao observador: diretamente, ou passando pela fonte. Portanto, posição da fonte mais vetor separação é igual à posição do observador. Isolando a separação, temos posição do observador menos posição da fonte. Essa ordem faz a seta apontar da fonte ao observador.

### N012 | 02:08 | Módulo; fonte se deslocando

**Fala:**

O vetor separação contém direção, sentido e comprimento. Seu módulo é a distância fonte–observador. Ao deslocar a fonte com o observador fixo, mudam a posição da fonte e a separação. É essa dependência que acompanharemos na integral.

### N013 | 02:23 | Elemento tangente e ângulo da lei

**Fala:**

O elemento orientado é tangente ao fio e segue a corrente convencional; seu módulo é o pequeno comprimento do trecho. O ângulo da lei fica entre esse elemento e o vetor separação.

## B03 — O significado da lei

### N014 | 02:29 | Lei experimental; elemento de corrente

**Fala:**

Biot–Savart é o ponto de partida experimental. A geometria esclarece sua forma, mas não demonstra sozinha a lei. Associamos a cada elemento uma contribuição infinitesimal; o campo da fonte inteira será sua soma.

### N015 | 02:33 | Corrente e comprimento multiplicando

**Fala:**

Mantendo distância e orientação, aumentar a corrente aumenta proporcionalmente a contribuição. Aumentar o pequeno comprimento também aumenta a parcela da fonte considerada. Por isso corrente e comprimento aparecem multiplicando.

### N016 | 02:39 | Afastamento; distância dobrada

**Fala:**

Mantendo os outros fatores, a contribuição cai com o quadrado da distância fonte–observador: dobrar essa distância reduz a parcela a um quarto. Isso ainda não descreve a queda do campo de um fio inteiro; falta integrar a fonte.

### N017 | 02:54 | Seno do ângulo

**Fala:**

O seno seleciona a parte do elemento perpendicular à separação. Para distância e elemento fixos, noventa graus dá contribuição máxima; vetores paralelos ou antiparalelos dão contribuição nula. É uma parcela do campo, não necessariamente o campo total.

### N018 | 03:04 | Permeabilidade magnética do vácuo; igualdade escalar

**Fala:**

O fator de proporcionalidade é a permeabilidade magnética do vácuo dividida por quatro pi. Ela estabelece a escala nas unidades do Sistema Internacional. Temos corrente, comprimento e seno no numerador, distância ao quadrado no denominador. Essa forma escalar dá a intensidade; falta registrar a direção.

### N019 | 03:16 | Paralelogramo e produto vetorial

**Fala:**

O produto vetorial reúne intensidade e direção. Seu módulo, usando o vetor unitário de separação, é comprimento do elemento vezes seno do ângulo. O paralelogramo representa essa dependência. A resultante é perpendicular aos dois vetores, com sentido dado pela mão direita.

### N020 | 03:33 | Normalização do vetor separação

**Fala:**

O vetor unitário conserva apenas direção e sentido: dividimos o vetor separação por seu módulo para obter comprimento um. Substituindo na lei, essa distância adicional no denominador multiplica a distância ao quadrado e forma o cubo.

### N021 | 03:49 | Duas formas equivalentes da lei

**Fala:**

A lei continua igual: o numerador agora contém o vetor separação completo, que também carrega distância. Portanto, o cubo no denominador não significa uma nova queda cúbica da contribuição. As duas formas são equivalentes.

## B04 — Correntes em linhas, superfícies e volumes

### N022 | 04:00 | Fio fino e integral de linha

**Fala:**

O fio fino idealiza uma seção pequena diante das distâncias relevantes. Integramos ao longo de uma linha. Como nas distribuições de carga das aulas de Gauss, também podemos ter fontes sobre superfícies ou volumes; aqui, porém, precisamos da corrente e de sua orientação.

### N023 | 04:16 | Faixa da lâmina; densidade superficial

**Fala:**

Na lâmina, escolhemos uma faixa alinhada à corrente. A densidade superficial mede corrente por largura transversal, em ampère por metro. Multiplicada pela largura da faixa, fornece sua corrente. A versão vetorial inclui o sentido do fluxo.

### N024 | 04:35 | Largura vezes comprimento; integral de superfície

**Fala:**

Multiplicamos a corrente dessa faixa pelo elemento orientado ao longo dela. Largura vezes comprimento forma a pequena área. O elemento de corrente vira densidade superficial vetorial vezes elemento de área. Conservamos o produto vetorial de Biot–Savart, agora somando sobre a superfície.

### N025 | 04:51 | Seção transversal do volume; densidade volumétrica de corrente

**Fala:**

No volume, escolhemos uma seção perpendicular ao fluxo local. A corrente nessa seção é o módulo da densidade de corrente vezes sua área, por isso a unidade é ampère por metro quadrado. Se a seção fosse inclinada, usaríamos a componente normal da densidade vetorial.

### N026 | 05:07 | Elemento de volume

**Fala:**

Área transversal vezes comprimento forma o elemento de volume. Assim, usamos densidade de corrente vetorial vezes elemento de volume. A medida da integral acompanha a distribuição: linha, superfície ou volume. Em todos os casos, as contribuições são calculadas no mesmo observador.

## B05 — Separar intensidade e direção

### N027 | 05:20 | Distância constante e gráfico do seno

**Fala:**

Vamos fixar corrente, comprimento do elemento e distância. O observador percorre um arco, mudando apenas a orientação da separação. O ponto no gráfico acompanha o seno e permite estudar isoladamente o efeito do ângulo.

### N028 | 05:30 | Contribuição nula; máximos e mínimos

**Fala:**

Com os vetores alinhados no mesmo sentido, a contribuição é zero. Cresce até noventa graus e depois diminui, zerando novamente em cento e oitenta graus. A corrente continua passando: quem zera é a contribuição daquele elemento, cujo produto vetorial se anula nesses alinhamentos.

### N029 | 06:05 | Perspectiva e regra da mão direita

**Fala:**

Para achar o sentido da contribuição não nula, aponte os dedos da mão direita ao longo do elemento orientado e curve-os em direção à separação, pelo menor ângulo. O polegar indica a contribuição magnética.

### N030 | 06:18 | Troca da ordem do produto

**Fala:**

Trocar a ordem dos vetores inverte o produto. Isso não modifica fisicamente a mesma corrente: mostra que usar a ordem errada na fórmula produz o sinal errado. Pela nossa convenção, primeiro vem o elemento; depois, a separação.

## B06 — Superposição e integral

### N031 | 06:23 | Contribuições dos elementos no mesmo observador

**Fala:**

Pela superposição, somamos as contribuições dos trechos no mesmo observador. Aqui elas apontam no mesmo sentido. Em outras geometrias, podem ter direções distintas e precisam ser somadas componente a componente, como fazemos com campos elétricos.

### N032 | 06:41 | Soma ponta com cauda

**Fala:**

Transportamos cópias das setas para somá-las ponta com cauda. A resultante liga o início da primeira ao fim da última. Essa construção não muda o ponto onde o campo foi calculado. Com poucos trechos finitos, temos uma aproximação.

### N033 | 06:49 | Refinamento e limite integral

**Fala:**

Refinamos a divisão da mesma fonte: cada trecho diminui, e seu número aumenta. A corrente e o comprimento total permanecem iguais. Quando os comprimentos tendem a zero, a soma converge para a integral das contribuições infinitesimais.

## B07 — Método de resolução

### N034 | 07:04 | Lista do método

**Fala:**

O método tem quatro perguntas: onde estão fonte e observador? Qual a direção das contribuições? Que variável percorre a fonte e como escrever seu elemento orientado? Quais limites incluem exatamente o trecho desejado?

### N035 | 07:16 | Direção, elemento e limites no desenho

**Fala:**

Aqui a mão direita dá contribuições saindo da tela. Percorreremos o fio pela coordenada horizontal, com o elemento orientado no sentido da corrente. Integraremos entre as duas extremidades. Definir variável, sentido e limites antes da conta evita erros de sinal e região.

## B08 — Contribuição de um trecho reto

### N036 | 07:29 | Trecho dentro do circuito

**Fala:**

Calcularemos apenas a contribuição do trecho reto. Ele pertence a um circuito: não é uma corrente estacionária com início e fim no vazio. Depois, seu campo pode ser somado vetorialmente ao do restante do circuito.

### N037 | 07:44 | Coordenadas do elemento e do observador

**Fala:**

A origem fica no pé da perpendicular que vem do observador. A coordenada da fonte mede sua posição horizontal, podendo ser negativa ou positiva. A distância perpendicular ao fio é fixa e positiva. O observador está acima da origem.

### N038 | 07:49 | Componentes da separação

**Fala:**

Da fonte ao observador, desfazemos o deslocamento horizontal e subimos a distância perpendicular. Por isso a componente horizontal da separação tem sinal oposto à coordenada da fonte. A componente vertical aponta para cima. A soma constrói o vetor separação.

### N039 | 07:54 | Distribuição do produto vetorial

**Fala:**

Distribuímos o produto vetorial pelas duas componentes. A horizontal é paralela ou antiparalela ao elemento e não contribui. A vertical produz a direção perpendicular ao plano, pelo produto da direção horizontal com a vertical. Pela mão direita, a contribuição sai da tela.

### N040 | 08:12 | Perspectiva; substituição em Biot–Savart

**Fala:**

A nova perspectiva mostra a mesma direção no espaço. Sobra distância perpendicular vezes pequeno deslocamento horizontal, orientados no eixo perpendicular ao plano. Substituímos esse produto em Biot–Savart. A corrente e a distância perpendicular são constantes; a separação fonte–observador ainda varia.

### N041 | 08:33 | Pitágoras e denominador

**Fala:**

O desenho fornece um triângulo retângulo. Seus catetos são a coordenada horizontal, em módulo, e a distância perpendicular; a hipotenusa é a separação. Pelo teorema de Pitágoras, a separação ao quadrado é a soma dos quadrados desses catetos. Seu cubo é essa soma elevada a três meios.

### N042 | 08:44 | Fonte em movimento e definição do ângulo de integração

**Fala:**

Quando a fonte anda, a intensidade muda, mas o sentido continua saindo da tela. Vamos localizá-la por um ângulo medido no observador a partir da perpendicular: zero no pé da perpendicular, positivo à direita, negativo à esquerda. Esse ângulo de integração difere do ângulo entre elemento e separação da lei.

### N043 | 09:03 | Tangente e mudança de variável

**Fala:**

Pelo triângulo, a tangente do ângulo de integração é a coordenada da fonte dividida pela distância perpendicular. Assim, a coordenada vira distância perpendicular vezes tangente. Escolhemos essa mudança porque a identidade trigonométrica simplificará a soma de quadrados no denominador.

### N044 | 09:11 | Diferencial da nova variável

**Fala:**

Também precisamos transformar o diferencial. A distância perpendicular é constante; a derivada da tangente é a secante ao quadrado. Portanto, o pequeno deslocamento vira distância perpendicular vezes secante ao quadrado, multiplicadas pelo diferencial do ângulo. Esse fator converte corretamente a medida da integração.

### N045 | 09:21 | Identidade trigonométrica no denominador

**Fala:**

Substituímos a coordenada no denominador e colocamos a distância perpendicular ao quadrado em evidência. Um mais tangente ao quadrado é secante ao quadrado. Como a distância é positiva e o ângulo está entre menos noventa e mais noventa graus, a secante é positiva. Elevando a três meios, obtemos distância perpendicular ao cubo vezes secante ao cubo.

### N046 | 09:39 | Cancelamentos de distâncias e secantes

**Fala:**

Há dois fatores de distância perpendicular no numerador: um do produto vetorial e outro do diferencial. Seu quadrado dividido pelo cubo deixa o inverso da distância. Secante ao quadrado dividida pela secante ao cubo deixa o inverso da secante, ou cosseno. Essa simplificação justifica a mudança de variável.

### N047 | 10:00 | Limites angulares nas extremidades

**Fala:**

A separação não desapareceu da física: foi reexpressa. Falta transformar os limites nas posições angulares das extremidades. No desenho, o pé da perpendicular fica entre elas; o ângulo da esquerda é negativo e o da direita, positivo.

### N048 | 10:08 | Integral do cosseno e diferença de senos

**Fala:**

Os fatores constantes saem da integral. A primitiva do cosseno é o seno, como podemos conferir derivando. Aplicando os limites, fica seno do ângulo da extremidade direita menos seno do ângulo da extremidade esquerda, multiplicados pelo fator constante.

### N049 | 10:19 | Dois ângulos positivos e resultado do trecho

**Fala:**

Podemos usar dois ângulos positivos, um para cada lado da perpendicular. O seno do limite negativo é o oposto do seno de seu módulo, então a diferença vira soma. Isso explica a forma final. Se as extremidades estiverem do mesmo lado da perpendicular, devemos preservar a expressão com limites assinados, sem aplicar automaticamente essa soma.

## B09 — Limite do fio infinito

### N050 | 10:32 | Extensão do trecho

**Fala:**

Estendemos o fio para os dois lados, mantendo a distância perpendicular fixa. Os dois ângulos positivos tendem a noventa graus; seus senos tendem a um. A soma fornece dois, que simplifica o quatro pi da lei. Obtivemos o fio infinito como limite do trecho finito.

### N051 | 10:54 | Resultado e interpretação da queda

**Fala:**

O campo integrado cai com o inverso da distância ao fio, embora cada contribuição tivesse inverso do quadrado da separação. A diferença vem da soma da fonte estendida. Para um fio real, a aproximação exige distância pequena diante das distâncias às pontas, considerando também o restante do circuito.

## B10 — Força entre fios paralelos

### N052 | 11:04 | Campo do primeiro fio

**Fala:**

Voltamos aos dois fios. Com corrente para cima no primeiro, seu campo entra na tela à direita e sai à esquerda. O xis indica entrada; o ponto, saída. Os símbolos uniformes mostram apenas direção. A intensidade depende da distância, como indica a fórmula.

### N053 | 11:16 | Campo na posição do segundo fio e força

**Fala:**

Usamos o campo do primeiro na posição do segundo. Com as correntes para cima, o vetor comprimento do segundo aponta para cima e o campo externo entra na tela. Seu produto vetorial aponta para o primeiro fio: atração. Nessa interação, usamos o campo do outro fio, não o campo próprio do segundo.

### N054 | 11:31 | Força por comprimento

**Fala:**

Como comprimento e campo são perpendiculares, o módulo da força é corrente vezes comprimento vezes campo externo. Dividindo pelo comprimento, obtemos permeabilidade magnética do vácuo vezes produto das correntes, divididos por dois pi vezes separação entre os fios. A unidade é newton por metro. Essa fórmula escalar fornece o módulo.

### N055 | 11:41 | Inversão de uma corrente

**Fala:**

Invertemos apenas a corrente do segundo fio. O campo do primeiro permanece, mas a força inverte: repulsão. Correntes paralelas no mesmo sentido se atraem; em sentidos opostos, se repelem. Estamos comparando estados estacionários.

## B11 — Espira circular: geometria, simetria e integral

### N056 | 11:49 | Vista frontal da espira

**Fala:**

Agora a corrente percorre uma espira circular. Queremos o campo no eixo perpendicular ao seu plano, passando pelo centro. A vista frontal mostra o sentido da corrente.

### N057 | 11:58 | Aviso de notação

**Fala:**

Atenção à notação: o símbolo usado antes para a distância agora representa o raio da espira. Outro símbolo representa a separação do elemento ao observador. A coordenada axial localiza o observador a partir do centro e tem sinal; a distância ao plano é seu módulo.

### N058 | 12:02 | Pequeno arco e ângulo da posição

**Fala:**

Percorremos a circunferência pelo ângulo de posição. O comprimento de um pequeno arco é raio vezes diferencial desse ângulo, medido em radianos. Esse fator converte ângulo em comprimento. O elemento orientado é tangente e segue a corrente.

### N059 | 12:10 | Mudança da vista frontal para a lateral

**Fala:**

Mudamos a perspectiva, sem girar fisicamente a fonte. De perfil, a espira aparece como uma linha; vemos o eixo e o observador. O símbolo junto ao elemento indica sua tangente saindo ou entrando no plano da imagem.

### N060 | 12:23 | Triângulo do raio, coordenada axial e separação

**Fala:**

Centro, elemento e observador formam um triângulo retângulo. Os catetos são o raio e a distância axial; a hipotenusa é a separação. Por Pitágoras, separação ao quadrado é raio ao quadrado mais coordenada axial ao quadrado. Para o observador fixo no eixo, todos os elementos têm essa mesma separação.

### N061 | 12:37 | Tangente perpendicular à separação

**Fala:**

A tangente é perpendicular ao raio e ao eixo. Como a separação está no plano formado por ambos, ela também é perpendicular à tangente. Isso vale para cada elemento da espira. O ângulo da lei é noventa graus, e seu seno vale um. Resta corrente vezes comprimento do elemento, sobre separação ao quadrado, com o fator de permeabilidade.

### N062 | 12:53 | Contribuição inclinada e projeção

**Fala:**

A mão direita dá uma contribuição inclinada, perpendicular à tangente e à separação. Vamos decompô-la em parte axial e parte transversal. Calcularemos a projeção axial e depois usaremos a simetria para justificar por que a transversal desaparece na soma.

### N063 | 12:58 | Cosseno da projeção; dois ângulos iguais

**Fala:**

A parte axial é o módulo da contribuição vezes o cosseno do ângulo entre ela e o eixo. O ângulo destacado no triângulo é igual a esse: seus lados são perpendiculares dois a dois. Isso permite calcular a projeção pela geometria do triângulo.

### N064 | 13:08 | Cateto adjacente sobre hipotenusa

**Fala:**

O cosseno é cateto adjacente sobre hipotenusa: raio dividido pela separação. Esse fator multiplica o módulo da contribuição para fornecer sua componente axial. Por ser uma projeção, seu módulo não ultrapassa o do vetor original.

### N065 | 13:27 | Elemento diametralmente oposto

**Fala:**

Considere agora o elemento diametralmente oposto, com igual comprimento e corrente. Sua distância ao observador é a mesma, então a contribuição tem o mesmo módulo. As partes transversais são opostas; as axiais apontam no mesmo sentido.

### N066 | 13:31 | Cancelamento transversal e soma axial

**Fala:**

Somadas ponta com cauda, as transversais retornam ao ponto inicial: cancelamento. As axiais se somam. Cada elemento tem um oposto, então o campo total sobre o eixo é axial. A simetria reduziu a integral vetorial à componente que sobrevive.

### N067 | 13:47 | Retorno a uma contribuição

**Fala:**

O par demonstrou a simetria. Integraremos a componente de um elemento por uma volta inteira, sem outro fator dois. Integrar pares por meia volta também funcionaria. O erro seria percorrer a volta completa e depois duplicá-la.

### N068 | 13:55 | Montagem do integrando axial

**Fala:**

Montamos a contribuição axial: Biot–Savart traz corrente, comprimento do elemento e inverso do quadrado da separação. A projeção acrescenta raio sobre separação. Esse primeiro fator de raio vem da projeção, não do comprimento do arco.

### N069 | 14:09 | Elemento de arco; dois raios e três separações

**Fala:**

Substituímos o comprimento do elemento por raio vezes diferencial do ângulo. Esse segundo raio vem do arco. Os dois raios formam o quadrado no numerador; a separação ao quadrado da lei e a separação da projeção formam o cubo no denominador.

### N070 | 14:25 | Pitágoras no cubo da separação

**Fala:**

Por Pitágoras, o cubo da separação é raio ao quadrado mais coordenada axial ao quadrado, tudo elevado a três meios. O expoente vem da raiz quadrada elevada ao cubo. O integrando agora multiplica o diferencial do ângulo ao redor da espira.

### N071 | 14:39 | Percurso de uma volta

**Fala:**

Percorremos uma volta com o observador fixo. Corrente, raio, coordenada axial e separação permanecem constantes; só varia o ângulo de posição. Essa simplificação depende de o observador estar no eixo.

### N072 | 14:48 | Resultante axial e integral

**Fala:**

Somando as contribuições, resta o campo axial; a seta individual inclinada dá lugar à resultante no eixo. Os fatores independentes do ângulo saem da integral. Resta integrar seu diferencial de zero a dois pi: a medida angular de uma volta completa.

### N073 | 15:07 | Simplificação do fator angular

**Fala:**

O dois pi da volta, dividido pelo quatro pi da lei, dá um meio. Daí vem o fator dois no denominador final. Ele não veio de contar novamente os pares opostos. Corrente, raio ao quadrado e a potência da separação permanecem.

### N074 | 15:14 | Resultado do campo no eixo

**Fala:**

O campo axial é permeabilidade magnética do vácuo vezes corrente vezes raio ao quadrado, divididos por duas vezes a soma do raio ao quadrado com a coordenada axial ao quadrado, elevada a três meios. Seu sentido segue a mão direita. O resultado vale no eixo da espira ideal de fio fino com corrente estacionária.

## B12 — Verificações do resultado

### N075 | 15:27 | Observador levado ao centro

**Fala:**

Vamos testar o centro. A coordenada axial é zero; a separação até cada elemento é o raio. O denominador vira duas vezes raio ao cubo. Simplificando com o raio ao quadrado do numerador, resta permeabilidade magnética do vácuo vezes corrente, divididas por duas vezes o raio.

### N076 | 15:42 | Direção de cada contribuição no centro

**Fala:**

A geometria confirma: no centro, tangente e separação estão no plano da espira; o produto vetorial é axial. Cada contribuição já aponta no sentido da resultante. Não há componente lateral para cancelar. Para igual corrente, uma espira menor dá campo central maior nessa idealização.

### N077 | 15:51 | Observador afastado; eixo graduado

**Fala:**

Agora afastamos o observador. A escala compara sua distância axial com o raio; o desenho da espira está ampliado para permanecer legível. Muito longe significa distância axial muito maior que o raio. É essa relação, não só a posição aparente na tela, que permite aproximar a fórmula.

### N078 | 16:08 | Fatoração exata antes da aproximação

**Fala:**

Colocamos a coordenada axial ao quadrado em evidência. Elevando a três meios, ela fornece seu módulo ao cubo. Sobra um mais raio ao quadrado sobre coordenada axial ao quadrado, todo o parêntese elevado a três meios. Até aqui, a igualdade é exata. Muito longe, a razão é pequena e esse parêntese elevado a três meios se aproxima de um.

### N079 | 16:18 | Queda cúbica e comparação com o fio

**Fala:**

O campo distante cai com o cubo da distância: ao dobrá-la, aproxima-se de um oitavo. Para o fio infinito, dobrar a distância reduz o campo à metade. São fontes de geometrias diferentes. A queda cúbica da espira é uma aproximação distante, não uma regra para todas as posições.

## B13 — Síntese

### N080 | 16:29 | Vetor separação, lei e soma

**Fala:**

Nos dois casos, fixamos o observador, percorremos a corrente, construímos a separação e integramos Biot–Savart. A geometria fornece distâncias e projeções; a orientação define os produtos vetoriais; a simetria revela os cancelamentos. Como em Gauss, escolher coordenadas convenientes não cria simetria: precisamos reconhecê-la na fonte.

### N081 | 16:57 | Comparação fio e espira

**Fala:**

No fio infinito, o campo envolve o fio e cai com o inverso da distância perpendicular. Na espira, a soma cancela as partes transversais no eixo, e o campo distante cai com o cubo da distância. Mesma lei; distribuições diferentes.

## B14 — Gancho e encerramento

### N082 | 17:11 | Linhas circulares e perguntas estruturais

**Fala:**

Que propriedades gerais esses campos obedecem? Neste exemplo, as linhas ao redor do fio são círculos fechados. O que revela o divergente do campo magnético? Como seu rotacional se relaciona com a corrente? Essas perguntas nos levam à lei de Ampère, no próximo vídeo.

### N083 | 17:24 | Logo oficial e CTA

**Fala:**

Se essa construção ajudou você a entender de onde vem cada termo, inscreva-se no Parallax Lab para acompanhar os próximos vídeos. Até a próxima!

---

## Sincronização e limite editorial — não narrar

- Aprovar e medir a voz antes de fechar a duração do vídeo. Não acelerar artificialmente a fala nem eliminar um passo central para cumprir uma estimativa de texto.
- Ajustar a duração das varreduras e os intervalos entre operações à fala. Manter os marcadores da corrente em movimento; não transformar o remapeamento em longas telas congeladas.
- Preservar âncoras internas nas unidades N039 (paralela e perpendicular), N046 (distâncias e secantes), N066 (cancelamento e soma), N069 (origens dos raios e cubo da separação) e N078 (fatoração exata e aproximação). O texto curto não autoriza fundir essas etapas.
- A integração da espira continua completa: arco, perpendicularidade, projeção, par oposto, integrando, volta e checagens. A do trecho continua com produto vetorial, mudança de variável e diferencial, denominador, cancelamentos e limites assinados.
- O CSV correspondente deixa os campos de áudio vazios até existir locução. O orçamento por bloco é provisório; pode redistribuir tempo entre unidades do mesmo bloco, preservando os encontros entre frase e evento.
- Se a voz pedir mais de 24 minutos com pausas adequadas, entregar a duração observada. Priorizar a compreensão, conforme a orientação do usuário. Não cortar hipóteses, justificativas ou operações sem uma decisão editorial explícita.
- Não gerar voz, legendas nem alterar a animação nesta etapa.
