# yt_0008 — narração com audio tags (v4, revisão GPT ≤ 25 min, para gerar a voz)

Fonte do texto: `narracao_revisada_gpt.md` (revisão do GPT sobre a v1; "corrente envolvida" padronizado). Fala sem alteração de conteúdo; só (1) símbolos LaTeX trocados pela fala (ver tabela abaixo) e (2) tags em inglês nos pontos-chave, uma por frase, que valem até a próxima tag e não entram na legenda nem no SRT.
Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`. **Gerar só depois da confirmação do usuário** (gasta crédito). Âncoras e tempos: `narracao_ancoras.md`.

Letras faladas (a tela mostra o símbolo; a fala usa o nome): s → "ésse"; J → "jota"; r → "erre"; r′ → "erre linha"; R → "erre maiúsculo"; F → "efe"; C → "cê"; S → "esse maiúsculo"; K → "cá"; L → "ele maiúsculo"; n → "ene"; N → "ene maiúsculo".

## Texto corrido (para gravação)

[curious] Existe uma coisa estranha no campo magnético de um fio infinito.

As linhas de campo dão voltas completas ao redor da corrente. Tudo parece estar girando.

Mas, fora do fio, o rotacional desse campo é zero.

[curious] Como um campo pode circular em torno de uma corrente e, ao mesmo tempo, ter rotacional nulo quase em toda parte?

[thoughtful] É essa aparente contradição que vamos resolver hoje.

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab.

Nos vídeos anteriores, vimos a força magnética e aprendemos a calcular campos usando a lei de Biot–Savart. Agora vamos mudar a pergunta.

[thoughtful] Em vez de começar pela corrente e perguntar qual campo ela produz, vamos olhar para o próprio campo magnético e perguntar:

o que a sua geometria revela sobre as correntes que o produziram?

Esse caminho vai nos levar ao divergente do campo magnético, ao seu rotacional e, finalmente, à lei de Ampère.

[thoughtful] Comecemos pelo exemplo mais simples.

Este fio conduz uma corrente constante. Os marcadores verdes indicam o sentido convencional da corrente. O movimento desses marcadores é apenas uma representação visual do transporte de carga; sua velocidade no desenho não corresponde à velocidade real das cargas no material.

Ao redor do fio, o campo magnético forma circunferências.

O sentido é dado pela regra da mão direita.

Se apontamos o polegar no sentido da corrente, os dedos indicam o sentido em que o campo contorna o fio.

Até aqui, seguimos o caminho que já conhecemos:

uma distribuição de corrente é dada, usamos Biot–Savart e obtemos o campo magnético.

[curious] Mas agora vamos inverter o raciocínio.

As linhas são curvas.

[curious] Será que isso significa que o rotacional do campo é diferente de zero?

Vamos verificar.

[thoughtful] Visto de cima, o fio aparece como um ponto.

O símbolo com um ponto no centro indica uma corrente saindo da tela.

Escolhemos um ponto onde queremos observar o campo e medimos sua distância ao eixo do fio.

Vamos chamar essa distância radial de ésse.

Para um fio retilíneo infinito, Biot–Savart fornece um campo tangente às circunferências em torno do eixo.

Sua intensidade é igual à permeabilidade magnética do vácuo, vezes a corrente, dividida por dois pi vezes a distância ao eixo.

A permeabilidade magnética do vácuo é a constante indicada por mi zero.

[thoughtful] Agora calculamos o rotacional.

Na geometria cilíndrica, a componente relevante contém a derivada do produto entre a distância radial e a componente azimutal do campo.

Substituímos o campo do fio.

A distância ésse cancela com o fator inversamente proporcional a ésse.

Sobra apenas uma constante.

Isso também aparece no desenho.

Se dobramos a distância ao fio, a intensidade do campo cai pela metade.

Se triplicamos a distância, ela cai para um terço.

O produto entre distância e intensidade continua constante.

[slow, measured pace] Como a derivada de uma constante é zero, essa componente do rotacional desaparece.

E as demais componentes também são nulas.

Portanto, em qualquer ponto fora do eixo,

o campo magnético existe, suas linhas são curvas, mas seu rotacional é zero.

[slow, measured pace] Essa é a primeira ideia importante do vídeo:

curvatura de uma linha de campo e rotacional não são a mesma coisa.

[thoughtful] Para entender o que o rotacional realmente mede, vamos olhar localmente para o campo.

Imagine uma pequena sonda formada por um caminho fechado em torno do ponto que estamos observando.

Essa sonda possui uma área e uma direção normal, perpendicular à sua superfície.

A orientação entre o percurso da borda e essa normal segue a regra da mão direita.

Agora percorremos a borda da sonda e somamos, em cada pequeno trecho, a componente tangencial do campo magnético multiplicada pelo pequeno comprimento percorrido.

Essa soma é a circulação.

Depois dividimos essa circulação pela área da sonda.

E fazemos a área tender a zero.

O resultado fornece a componente do rotacional na direção da normal.

Isso explica por que simplesmente olhar uma linha curva não basta.

O rotacional mede uma circulação local, infinitesimal.

[thoughtful] Neste campo do fio, podemos enxergar o cancelamento diretamente.

Nos trechos radiais da pequena sonda, o campo magnético e o elemento de caminho são perpendiculares.

O produto escalar é zero.

Já nos dois arcos, há contribuição.

No arco mais próximo do fio, o campo é mais intenso, mas o arco é mais curto.

No arco mais distante, o campo é mais fraco, mas o percurso é mais longo.

Como a intensidade varia inversamente com a distância, essas duas contribuições possuem o mesmo módulo e sinais opostos.

Elas se cancelam.

Se girarmos a sonda para verificar outras orientações independentes, o resultado continua zero.

Portanto, o vetor rotacional é realmente nulo naquele ponto.

[curious] Mas agora vem a parte interessante.

O que acontece se aumentarmos o laço?

Enquanto o caminho não envolve o fio, a circulação continua nula.

Mas, no instante em que tentamos passar o caminho exatamente sobre o fio ideal, encontramos a singularidade do modelo.

O campo de um fio infinitamente fino não está definido no próprio eixo.

Depois que o laço passa a envolver a corrente, a situação muda.

A circulação deixa de ser zero.

Para um círculo centrado no fio, o campo é tangente em todos os pontos e possui a mesma intensidade ao longo de todo o caminho.

Então basta multiplicar a intensidade do campo pelo comprimento da circunferência.

O resultado é mi zero vezes a corrente.

É importante notar que ainda não estamos usando a lei de Ampère como ponto de partida.

Obtivemos esse resultado diretamente do campo calculado por Biot–Savart.

[curious] E surge a pergunta:

se o rotacional é zero em todos os pontos fora do fio, de onde vem essa circulação global não nula?

[slow, measured pace] A resposta está exatamente na região que deixamos de fora: o eixo.

[thoughtful] Antes de resolver essa singularidade, vamos investigar outra propriedade do campo magnético.

[curious] Será que o campo magnético possui fontes ou sumidouros?

Para responder, envolvemos uma pequena região do espaço com uma superfície fechada.

Nessa região pequena, podemos tratar o campo como aproximadamente uniforme.

Como nos vídeos sobre a lei de Gauss, as normais da superfície apontam para fora.

Onde o campo entra na caixa, o produto com a normal é negativo.

Onde ele sai, o produto é positivo.

Nas faces em que o campo é tangente, a contribuição é zero.

Somando todas as faces, o fluxo líquido se anula.

Se dividimos esse fluxo pelo volume e fazemos a região encolher até um ponto, encontramos o divergente do campo magnético.

O resultado é zero.

[slow, measured pace] Essa é a forma diferencial da lei de Gauss para o magnetismo.

[thoughtful] O contraste com o campo elétrico é importante.

Uma carga elétrica positiva isolada produz fluxo elétrico líquido para fora de uma superfície fechada.

Ela funciona como uma fonte do campo elétrico.

Para o campo magnético, não aparece um termo equivalente.

No eletromagnetismo clássico que estamos estudando, não existem cargas magnéticas isoladas funcionando como fontes ou sumidouros de campo magnético.

[curious] Agora vamos mostrar que esse resultado já está escondido dentro da própria lei de Biot–Savart.

Considere uma distribuição de corrente.

A densidade volumétrica de corrente, representada por jota, informa a direção da corrente e a quantidade de corrente por unidade de área transversal. Sua unidade é ampère por metro quadrado.

Escolhemos um pequeno elemento de volume dentro dessa distribuição.

Sua posição é a posição da fonte, representada por erre linha, ou "erre linha".

Também escolhemos o ponto onde queremos calcular o campo.

Essa é a posição do observador, representada por erre.

O vetor que liga a fonte ao observador é

erre maiúsculo, igual a erre menos erre linha.

Ele aponta da fonte para o observador.

Já erre maiúsculo, sem caráter vetorial, representa apenas o módulo desse vetor: a distância entre os dois pontos.

Biot–Savart soma as contribuições de todos os pequenos elementos de volume da distribuição de corrente.

Para simplificar a notação, vamos chamar o fator geométrico o vetor separação dividido pela distância ao cubo de efe.

Esse símbolo é apenas uma abreviação matemática.

Não representa força.

[thoughtful] Agora calculamos o divergente do campo magnético em relação à posição do observador.

Como estamos derivando em relação ao observador e integrando sobre a posição da fonte, podemos levar esse operador para dentro da integral nas condições consideradas.

Usamos então uma identidade vetorial para o divergente de um produto vetorial.

Ela produz dois termos.

No primeiro, aparece uma derivada da densidade de corrente da fonte em relação à posição do observador.

Mas a densidade jota de erre linha depende da posição da fonte.

Mudar o observador não altera a corrente naquele ponto-fonte.

Por isso esse termo é zero.

Isso é apenas independência entre as duas variáveis.

O segundo termo contém o rotacional do fator geométrico.

Mas esse fator pode ser escrito como menos o gradiente do inverso da distância.

E o rotacional de um gradiente é nulo.

Assim, os dois termos desaparecem e recuperamos

o divergente do campo magnético igual a zero.

Existe uma sutileza na singularidade em que fonte e observador coincidem, e vamos tratá-la explicitamente daqui a pouco.

[slow, measured pace] Antes, vale separar muito bem duas ideias que parecem semelhantes na notação, mas têm justificativas completamente diferentes.

O operador nabla sem marca deriva em relação à posição do observador.

Se movemos o observador e mantemos a fonte fixa, a separação muda, mas a densidade de corrente naquele ponto-fonte permanece a mesma.

Por isso uma derivada de jota de erre linha em relação a erre é zero.

Agora considere o operador nabla linha.

Ele deriva em relação à posição da própria fonte.

Nesse caso, quando percorremos a distribuição de corrente, jota pode mudar de um ponto para outro.

Esse campo pode variar espacialmente e, ainda assim, permanecer estacionário no tempo.

As linhas verdes mostram linhas de corrente.

Os marcadores representam convencionalmente o transporte de carga ao longo delas.

Agora escolhemos uma célula muito pequena dentro desse campo e ampliamos essa região.

Nesse pequeno volume, entra tanta corrente quanto sai.

Não existe acúmulo líquido de carga.

Por isso, em magnetostática, o divergente da densidade de corrente é zero.

[slow, measured pace] Perceba que agora a justificativa é física.

Antes, a derivada zerava porque fonte e observador eram variáveis independentes.

Agora, o divergente da corrente zera por conservação de carga no regime estacionário.

Com essa diferença clara, podemos voltar à lei de Biot–Savart.

[curious] Desta vez, em vez do divergente, calculamos o rotacional do campo magnético.

Nosso objetivo é descobrir como a circulação local do campo está relacionada à corrente.

A identidade vetorial correspondente expande o produto em quatro termos.

Dois deles envolvem derivadas da densidade de corrente da fonte em relação à posição do observador.

Pela independência que acabamos de discutir, esses dois termos desaparecem.

Ainda não usamos conservação de carga aqui.

Sobram duas parcelas.

A primeira contém a densidade de corrente multiplicada pelo divergente do fator geométrico.

A segunda envolve a variação desse fator na direção da corrente.

Vamos começar pela primeira.

O fator geométrico efe aponta radialmente para fora da posição da fonte.

Sua intensidade diminui com o quadrado da distância.

Em qualquer região que não contenha a fonte, seu divergente é zero.

[curious] Mas algo especial acontece quando envolvemos a fonte com uma esfera.

Na superfície dessa esfera, a intensidade cai como um sobre o raio ao quadrado.

Ao mesmo tempo, a área cresce como quatro pi vezes o raio ao quadrado.

Os dois fatores se cancelam.

O fluxo total é sempre quatro pi.

Mesmo se fizermos a esfera encolher cada vez mais em torno da fonte, esse fluxo não desaparece.

Temos então uma contribuição concentrada em um único ponto.

[slow, measured pace] E é exatamente esse tipo de objeto que a delta de Dirac descreve.

Em três dimensões, escrevemos uma delta centrada quando a posição da fonte coincide com a posição do observador.

[thoughtful] A delta de Dirac não deve ser pensada como uma função comum com um "valor infinito".

Ela é uma distribuição definida pela maneira como atua dentro de uma integral.

Depois que o fator quatro pi cancela o quatro pi presente em Biot–Savart, sobra uma integral envolvendo a densidade de corrente e a delta.

Fixamos o observador.

Agora imagine pesos cada vez mais concentrados nas fontes próximas desse ponto.

As contribuições mais afastadas perdem importância.

No limite, apenas a contribuição em que a posição da fonte coincide com a posição do observador sobrevive.

A delta seleciona exatamente esse valor.

A integral se reduz à densidade de corrente no próprio ponto observado.

[slow, measured pace] Portanto, a primeira parcela do rotacional produz

mi zero vezes a densidade de corrente.

[curious] Ainda precisamos verificar a segunda.

O fator geométrico depende apenas da diferença entre a posição do observador e a posição da fonte.

Se deslocamos os dois pontos juntos da mesma forma, essa diferença não muda.

Por isso, derivar o fator em relação ao observador equivale a derivá-lo em relação à fonte com sinal oposto.

Fazemos essa troca na segunda parcela.

O sinal negativo que já estava presente se combina com o novo sinal negativo.

Agora usamos a regra do produto e uma integração por partes, componente por componente.

O resultado se separa em duas contribuições.

A primeira é um termo de superfície.

Como estamos considerando uma distribuição de corrente localizada, podemos escolher essa superfície suficientemente distante para que nenhuma corrente a atravesse.

Esse termo então desaparece.

A segunda contribuição contém o divergente da densidade de corrente.

[slow, measured pace] Aqui, finalmente, entra a equação da continuidade.

Ela relaciona o divergente da corrente à variação temporal da densidade de carga.

No regime estacionário, a densidade de carga não está se acumulando nem diminuindo com o tempo.

Logo, o divergente da densidade de corrente é zero.

As duas contribuições desaparecem.

[excited] E sobra a relação local fundamental:

o rotacional do campo magnético é igual à permeabilidade magnética do vácuo vezes a densidade de corrente.

[slow, measured pace] Essa é a forma local da lei de Ampère na magnetostática.

É uma relação ponto a ponto.

Daqui a pouco vamos transformá-la numa relação global usando o teorema de Stokes.

[curious] Mas antes podemos voltar ao paradoxo do fio.

[thoughtful] Em vez de um fio matematicamente sem espessura, considere agora um cilindro de raio finito.

Dentro dele, a densidade de corrente é uniforme e aponta ao longo do eixo.

Por simetria, o campo magnético continua circulando em torno desse eixo.

Agora podemos usar diretamente a lei local que acabamos de demonstrar.

Uma pequena sonda inteiramente dentro do condutor mede rotacional igual a mi zero vezes a densidade de corrente.

Quando essa sonda atravessa parcialmente a fronteira, apenas parte de sua área contém corrente, e a leitura diminui.

Quando fica completamente fora, a leitura local vai a zero.

Agora escrevemos a equação diferencial para a componente azimutal do campo.

Multiplicando pela distância radial e integrando, aparece uma constante de integração.

Ao dividir novamente pela distância, essa constante produz um termo proporcional a um sobre a distância.

[thoughtful] Mas esse termo explodiria no eixo.

Para um fio com densidade de corrente distribuída de maneira regular, não existe motivo físico para o campo divergir no centro.

Portanto, a regularidade exige que essa constante seja zero.

Dentro do condutor, o campo cresce linearmente com a distância ao eixo.

Ele começa em zero no centro e atinge seu maior valor na superfície.

E o gráfico acompanha exatamente esse comportamento.

Agora vamos para fora do cilindro.

Ali não há densidade de corrente.

A solução assume a forma de uma constante dividida pela distância radial.

Mas ainda não sabemos o valor dessa constante.

Para escolhê-la, usamos a fronteira do condutor.

Nosso modelo possui corrente volumétrica no interior e nenhuma camada singular adicional de corrente exatamente na superfície.

Nessas condições, o campo deve se encontrar continuamente dos dois lados.

O ramo externo precisa passar pelo mesmo ponto em que termina a reta interna.

Essa condição fixa a constante.

A corrente total é igual à densidade de corrente multiplicada pela área da seção circular.

Substituindo esse resultado, recuperamos novamente o campo do fio fino:

mi zero vezes a corrente, dividido por dois pi vezes a distância ao eixo.

[calm, satisfied] Agora temos o perfil completo.

Dentro do fio, o campo cresce linearmente.

Fora, diminui inversamente com a distância.

O valor máximo ocorre na superfície.

E, mesmo onde não existe corrente local e o rotacional é zero, o campo magnético continua existindo.

[curious] Agora vamos comprimir esse fio.

Diminuímos seu raio, mas mantemos a corrente total fixa.

A área da seção fica menor.

Para conservar a mesma corrente, a densidade de corrente precisa aumentar.

No gráfico, o campo externo não muda.

Já o valor máximo, localizado na superfície, cresce e se aproxima cada vez mais do eixo.

No limite em que o raio tende a zero, toda a corrente fica concentrada sobre uma linha.

Agora usamos uma delta de Dirac em duas dimensões, nas direções transversais ao fio.

Ela é diferente da delta tridimensional que apareceu no núcleo de Biot–Savart.

Aqui o eixo do fio continua se estendendo.

Quando integramos essa densidade singular sobre a seção transversal, recuperamos a corrente total.

[excited] E finalmente resolvemos o paradoxo da abertura.

Fora do eixo, o rotacional é zero.

Mas no eixo existe uma contribuição singular concentrada.

[slow, measured pace] Portanto, um laço que envolve o fio não está simplesmente "somando zeros".

Ele envolve a região singular onde a corrente está localizada.

É por isso que a circulação global pode ser diferente de zero.

[thoughtful] Agora temos uma lei local:

rotacional do campo magnético igual a mi zero vezes densidade de corrente.

Vamos transformá-la numa relação para a corrente total.

Escolhemos um caminho fechado.

Chamemos esse contorno de cê.

E escolhemos uma superfície esse maiúsculo apoiada nessa mesma borda.

A orientação do percurso e a normal da superfície estão ligadas pela regra da mão direita.

Integramos a componente normal do rotacional sobre toda a superfície.

Do outro lado, integramos a densidade de corrente através dessa mesma superfície.

Cada pequeno elemento de área conta quanto de corrente o atravessa.

Se a corrente atravessa no sentido da normal, sua contribuição é positiva.

Se atravessa no sentido oposto, é negativa.

Correntes que não atravessam a superfície não entram nessa soma.

A soma algébrica dessas contribuições é a corrente envolvida.

Assim, a integral do rotacional sobre a superfície é igual à permeabilidade do vácuo vezes a corrente envolvida.

[curious] Agora falta transformar a superfície em sua borda.

E é exatamente isso que faz o teorema de Stokes.

Comecemos com duas pequenas células vizinhas.

Percorremos ambas com orientações compatíveis com a mesma normal.

Na aresta compartilhada, uma célula percorre o trecho num sentido e a outra percorre no sentido contrário.

Essas duas contribuições se cancelam.

Quando repetimos isso por toda a superfície, todas as bordas internas aparecem duas vezes com sentidos opostos.

Elas se cancelam aos pares.

No limite de uma divisão cada vez mais fina, a soma das pequenas circulações locais se transforma na integral do rotacional sobre a superfície.

E depois de todos os cancelamentos internos, sobra apenas o contorno externo.

[slow, measured pace] Esse é o teorema de Stokes.

[excited] Aplicando-o à lei local que encontramos, chegamos à forma integral da lei de Ampère:

a circulação do campo magnético ao longo de um caminho fechado é igual à permeabilidade magnética do vácuo vezes a corrente envolvida.

Continuamos falando de magnetostática.

E existe ainda uma pergunta importante.

[curious] Se mantemos a mesma borda, podemos trocar uma superfície plana por uma superfície curva?

Sim.

Considere duas superfícies diferentes apoiadas no mesmo contorno.

Juntas, elas formam uma superfície fechada.

No regime estacionário, o divergente da densidade de corrente é zero.

Portanto, o fluxo líquido de corrente através dessa superfície fechada também é zero.

Isso significa que a corrente líquida que atravessa uma superfície é exatamente a mesma que atravessa a outra.

Então a corrente envolvida pelo contorno não depende de qual superfície escolhemos para calculá-la.

[thoughtful] Agora temos uma lei poderosa.

Mas é importante separar duas coisas.

A lei de Ampère é verdadeira na magnetostática mesmo para um contorno complicado.

Isso não significa que ela sempre seja útil para calcular o campo.

Se direção e intensidade variam de forma desconhecida ao longo do caminho, conhecer apenas a circulação não permite descobrir o campo ponto a ponto.

[thoughtful] Como já vimos com a lei de Gauss, é a simetria que transforma a lei numa ferramenta de cálculo.

[slow, measured pace] A estratégia é:

primeiro, reconhecer as simetrias da fonte.

Depois, determinar a direção possível do campo.

Em seguida, escolher um caminho que explore essas simetrias.

E finalmente calcular a corrente envolvida.

[thoughtful] Vamos aplicar esse método a quatro geometrias.

Primeiro, o fio reto e infinito.

A fonte não muda se girarmos ao redor do fio.

Também não muda se deslocarmos ao longo de seu eixo.

Por isso, o campo depende apenas da distância radial e aponta tangencialmente às circunferências.

Escolhemos então uma circunferência centrada no fio.

Em todos os seus pontos, campo magnético e elemento de caminho são paralelos.

Além disso, a intensidade do campo é constante ao longo do percurso.

Ela pode sair da integral.

A circulação se torna intensidade do campo vezes comprimento da circunferência.

Esse comprimento é dois pi vezes a distância radial.

A corrente envolvida é simplesmente a corrente do fio.

Então obtemos novamente

o campo igual a mi zero vezes a corrente, dividido por dois pi vezes a distância.

É exatamente o resultado de Biot–Savart.

[calm, satisfied] Mas agora ele apareceu com uma conta muito mais curta graças à simetria.

[thoughtful] Segundo exemplo: uma lâmina infinita de corrente.

Aqui a corrente está distribuída sobre uma superfície.

Usamos uma densidade superficial de corrente, em ampères por metro.

Ela nos diz quanta corrente atravessa uma largura perpendicular ao movimento.

Vista de perfil, a corrente sai da tela.

Pela regra da mão direita, o campo aponta para um lado acima da lâmina e para o sentido oposto abaixo.

Os módulos são iguais.

Escolhemos um caminho retangular que atravessa a lâmina.

Nos lados perpendiculares ao campo, o produto escalar é zero.

Nos dois lados paralelos, campo e caminho têm a mesma direção.

Cada trecho contribui com intensidade vezes comprimento.

Por isso aparecem duas contribuições iguais.

Agora calculamos a corrente envolvida.

Se a densidade superficial vale cá e o caminho cobre uma largura ele maiúsculo, a corrente envolvida vale cá vezes ele maiúsculo.

Esse mesmo comprimento aparece dos dois lados da equação e cancela.

O resultado é:

o campo vale mi zero vezes a densidade superficial de corrente, dividido por dois.

No modelo de lâmina infinita, esse campo não depende da distância à superfície.

[thoughtful] Terceiro caso: o solenoide ideal infinito.

Um solenoide é formado por muitas espiras distribuídas ao longo de um eixo.

Chamamos de ene o número de espiras por unidade de comprimento.

Todas conduzem a mesma corrente.

Pela simetria do modelo infinito ideal, o campo deve apontar ao longo do eixo.

Mas ainda não vamos assumir seu valor nem dentro nem fora.

Primeiro escolhemos um retângulo completamente externo.

Os lados transversais não contribuem.

Nos dois lados paralelos ao eixo, as contribuições entram com sentidos opostos.

E esse caminho não envolve corrente.

A lei de Ampère mostra então que o campo externo possui o mesmo valor em diferentes distâncias do eixo.

Ou seja, é constante nessa região.

Agora usamos a condição física no infinito.

Considerando apenas o campo produzido pelo enrolamento, ele deve tender a zero quando nos afastamos indefinidamente.

A única constante compatível com esse limite é zero.

Portanto, para o solenoide infinito ideal, o campo externo é nulo.

Só agora usamos um segundo caminho.

Um lado fica dentro do solenoide.

O outro fica fora.

O trecho externo não contribui porque acabamos de mostrar que o campo ali é zero.

Os lados transversais também não contribuem.

Sobra apenas o trecho interno.

Se existem ene espiras por unidade de comprimento, um trecho de comprimento ele maiúsculo intercepta ene vezes ele espiras.

Cada uma transporta a mesma corrente.

Logo, a corrente envolvida é ene vezes ele vezes a corrente de cada espira.

Substituindo na lei de Ampère, o comprimento cancela.

O campo interno é igual a mi zero vezes o número de espiras por unidade de comprimento vezes a corrente.

E ele é uniforme no modelo ideal.

[thoughtful] Num solenoide real e finito, a situação é diferente.

Existem efeitos nas extremidades e um campo de retorno no exterior.

O resultado de campo externo exatamente zero pertence ao modelo infinito ideal.

[thoughtful] Nosso último exemplo é o toroide.

Podemos pensar nele como um solenoide curvado até formar um anel.

Aqui usamos ene maiúsculo para representar o número total de espiras.

Pela simetria do toroide ideal, escolhemos caminhos circulares centrados no eixo.

Na seção mostrada, as correntes aparecem saindo da tela de um lado e entrando pelo outro.

O campo é tangente a esses círculos e tem módulo constante em cada um.

Existem três regiões.

Primeiro, o vazio central.

Um caminho nessa região não envolve corrente líquida.

Com a simetria do toroide ideal, isso implica campo nulo.

Agora escolhemos um caminho dentro da região do enrolamento, entre o raio interno e o raio externo.

Esse caminho envolve uma contribuição de corrente para cada uma das ene maiúsculo espiras.

Portanto, a corrente envolvida vale ene maiúsculo vezes a corrente de cada espira.

A circulação fornece então um campo igual a mi zero vezes ene maiúsculo vezes a corrente, dividido por dois pi vezes a distância radial.

Finalmente, considere um caminho além do raio externo.

A superfície é atravessada por correntes em sentidos opostos.

A soma algébrica se cancela.

A corrente envolvida líquida é zero.

No toroide ideal, o campo externo também é zero.

[calm, satisfied] O gráfico reúne as três regiões:

zero no vazio central,

queda inversa dentro do enrolamento,

e zero fora.

[thoughtful] Agora podemos enxergar a estrutura completa.

Na eletrostática, o divergente do campo elétrico é proporcional à densidade de carga.

E o rotacional do campo elétrico é zero.

Na magnetostática, o divergente do campo magnético é zero.

E o rotacional do campo magnético é proporcional à densidade de corrente.

[slow, measured pace] Esses qualificadores são importantes.

Estamos falando de eletrostática e magnetostática.

Quando os campos variam no tempo, as equações completas de Maxwell acrescentam novos termos.

[slow, measured pace] Então, se você quiser guardar uma ideia central deste vídeo, não tente decorar quatro fórmulas separadas.

Fio, lâmina, solenoide e toroide obedecem à mesma lei.

O que muda é a simetria.

Reconheça a fonte.

Descubra que direção o campo pode ter.

Escolha um caminho que explore essa simetria.

E determine a corrente envolvida.

Essa é a lógica da lei de Ampère.

[curious] Mas ainda ficou uma última pergunta.

Vimos que o divergente do campo magnético é sempre zero.

Existe uma forma de construir um campo que já tenha essa propriedade automaticamente?

[thoughtful] Existe.

O divergente de qualquer rotacional é identicamente zero.

Isso sugere representar o campo magnético como o rotacional de outro campo:

o potencial vetor magnético.

E essa será a próxima etapa da nossa sequência.

[happy] Se esse vídeo te ajudou a entender não apenas como usar a lei de Ampère, mas de onde ela vem e por que ela funciona, deixa o like e se inscreve no Parallax Lab para acompanhar os próximos capítulos.

Nos vemos no próximo vídeo.
