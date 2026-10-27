# vid_0027 — narração com audio tags v2 (detalhada, padrão dos longos)

Pedido do usuário (2026-10-26): narração didática e íntima, com conectivos, brincadeiras leves, bem-vindos e encerramento;
variáveis sempre pelo nome completo (nunca a letra solta); álgebra e geometria bem explicadas; a animação se molda à voz.
Base: storyboard do handoff v1 (C01–C10, física congelada) com as formas gerais da v3 (Ampère, fluxo, fluxo concatenado,
indutância, origem de ½LI², densidade de energia). Regras: `docs/roteiro_voz_elevenlabs_v4.md` e `docs/padrao_video_longo.md` §5.
Cuidados de física: ½LI² é a energia guardada quando a corrente tem aquele valor (entrou enquanto a corrente subia); a densidade
B²/2μ₀ é resultado geral, usado e não deduzido; as duas rotas conferem (não é coincidência nem "descoberta"); trecho longe das pontas.
Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`. Gerar só depois da confirmação do usuário.

## Texto corrido (para gravação)

[curious] Olha esse solenoide. Uma bobina comprida, com corrente correndo pelas espiras. Todo indutor guarda energia... mas onde, exatamente, ela fica guardada?

No fio, que é por onde a corrente passa? Ou no espaço aí dentro, onde não tem nada além de ar?

[short pause] Guarda o seu palpite. No final a gente confere.

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

[thoughtful] Hoje é exercício resolvido. A gente vai calcular a energia desse solenoide por dois caminhos diferentes... e cada caminho vai contar uma parte da história.

[thoughtful] Primeiro, o cenário. O solenoide é bem longo, as espiras estão enroladas por igual, e o núcleo é de ar.

Pelas espiras passa uma corrente, que na tela aparece como a letra I, em verde. Esses tracinhos verdes mostram o sentido da corrente, e a velocidade deles acompanha o valor dela.

Repara que o desenho é um corte. A gente serrou o solenoide ao meio, bem pelo eixo, e está olhando a metade de trás. Nos fios de cima, o pontinho quer dizer que a corrente sai da tela. Nos de baixo, o xis quer dizer que ela entra.

[thoughtful] O raio do solenoide é o raio dessas espiras. E o número de espiras por metro diz quantas voltas de fio cabem em cada metro de comprimento. Cuidado: não é o total de espiras. É a densidade do enrolamento.

E a gente vai trabalhar só num trecho, bem longe das pontas. Por quê? Porque nas pontas o campo se abre e fica bagunçado. No meio de um solenoide longo, ele se comporta direitinho. É lá que a gente vai morar.

[curious] Então, primeira pergunta: quanto vale o campo magnético aí dentro?

[thoughtful] Para isso, a lei de Ampère. Ela diz o seguinte: pega um caminho fechado, vai somando o campo magnético ao longo dele, pedacinho por pedacinho... e essa soma, a circulação, vale mi zero vezes a corrente total que atravessa a área delimitada pelo caminho.

Mi zero é a permeabilidade do vácuo, uma constante. E corrente total quer dizer corrente líquida: o que atravessa num sentido conta positivo, o que atravessa no outro conta negativo.

[thoughtful] O segredo é escolher um caminho esperto. A gente pega este retângulo: um lado logo abaixo da parede de cima, por dentro do solenoide, e o lado oposto lá fora, acima dela.

E combina o sentido de percorrer: anti-horário. No lado de dentro, a gente anda para a direita.

Agora vamos olhar lado por lado.

[thoughtful] No lado de dentro, o campo aponta para a direita, no mesmo sentido em que a gente anda. Campo e caminho paralelos: esse lado contribui com tudo, o campo vezes o comprimento do lado.

Nos dois lados verticais, o campo é perpendicular ao caminho. E andar perpendicular ao campo não soma nada.

E no lado de fora? Fora de um solenoide longo, o campo é praticamente zero. Também não soma.

[thoughtful, emphatic] Ou seja: aquela integral com cara de assustadora vira só isto. Campo vezes o comprimento do lado.

[curious] E a corrente que atravessa o retângulo? É só contar os fios da parede de cima que ficaram lá dentro.

[thoughtful] Se em cada metro cabem tantas espiras, num comprimento do lado cabem as espiras por metro vezes esse comprimento. E cada uma leva a corrente inteira. Repara que todas saem da tela, então elas somam, sem nenhum cancelamento.

Colocando na lei: campo vezes o comprimento do lado é igual a mi zero vezes as espiras por metro, vezes o comprimento do lado, vezes a corrente.

[thoughtful] Olha só: o comprimento do lado aparece dos dois lados da igualdade... então ele corta! [short pause] E sobra o campo dentro do solenoide: mi zero vezes as espiras por metro vezes a corrente.

[thoughtful, emphatic] E repara no que essa fórmula não tem: ela não depende de onde você está lá dentro. O campo é uniforme. E fora, praticamente zero. As duas coisas são consequência de o solenoide ser longo e bem enrolado.

[curious] Agora que a gente conhece o campo... quanto dele atravessa uma espira?

[thoughtful] Isso é o fluxo magnético. A definição geral é uma integral: em cada pedacinho da superfície, a gente pega a parte do campo que atravessa e soma tudo.

A superfície aqui é o disco de uma espira, a seção do solenoide. No desenho ele aparece de ladinho, como uma elipse, porque está em pé, atravessando o eixo.

[thoughtful] E olha que conveniente: o campo é o mesmo em todo o disco e atravessa ele de frente, perpendicular. Então, em cada pedacinho, sobra só campo vezes o pedacinho de área. E, como o campo é constante, ele sai da integral.

O que fica dentro da integral é só a soma dos pedacinhos de área: a área inteira do disco, pi vezes o raio ao quadrado.

[thoughtful] Ou seja: fluxo é campo vezes área. Trocando o campo pelo que a gente achou, o fluxo numa espira fica mi zero vezes as espiras por metro vezes a corrente, vezes pi vezes o raio ao quadrado.

[curious] Só que um indutor não tem uma espira só. Tem um monte!

[thoughtful] E o campo atravessa todas elas. Então, para o circuito, o que importa é o fluxo concatenado: o fluxo da primeira espira, mais o da segunda, mais o da terceira... até a última.

Como o campo é uniforme no trecho, cada espira enxerga exatamente o mesmo fluxo. E somar o mesmo número várias vezes é multiplicar. O fluxo concatenado é o número de espiras do trecho vezes o fluxo de uma.

[thoughtful] E quantas espiras tem no trecho? Espiras por metro vezes o comprimento do trecho. Dez espiras por metro, dois metros de trecho... vinte espiras. Sem mistério.

Juntando tudo: as espiras por metro aparecem duas vezes, uma na contagem e outra no fluxo, e viram espiras por metro ao quadrado. O fluxo concatenado fica mi zero, vezes espiras por metro ao quadrado, vezes a corrente, vezes pi, vezes o raio ao quadrado, vezes o comprimento do trecho.

[thoughtful, emphatic] É o mesmo fluxo, repetido em cada espira do trecho.

[thoughtful] Com isso, sai a indutância. A definição: indutância é o fluxo concatenado dividido pela corrente. Quanto fluxo concatenado você ganha para cada ampère de corrente. A unidade é o henry.

Substituindo o fluxo concatenado... a corrente aparece em cima e embaixo. Corta!

[thoughtful, emphatic] E a indutância fica mi zero, vezes espiras por metro ao quadrado, vezes pi vezes o raio ao quadrado, vezes o comprimento do trecho. Só geometria! Ela não depende da corrente. Depende de como o solenoide foi construído.

[curious] E de onde vem esse ao quadrado nas espiras por metro? Um fator vem do campo: mais espiras por metro, campo mais forte. O outro vem da contagem: mais espiras por metro, mais espiras abraçando esse campo. Enrolar mais ajuda duas vezes.

[thoughtful] Então, dobrou as espiras por metro? A indutância fica quatro vezes maior. Raio maior, disco maior, mais fluxo. Trecho mais comprido, mais espiras.

[curious] Beleza. Agora, a energia. Primeiro caminho: pelo circuito.

[thoughtful] Imagina a corrente começando em zero e subindo até o valor final. Enquanto ela sobe, o campo cresce junto, e o indutor reage: aparece uma força eletromotriz induzida, igual a menos a indutância vezes a taxa com que a corrente muda.

Esse sinal de menos diz que o indutor é do contra. Ele se opõe ao aumento da corrente.

[thoughtful] Para a corrente continuar subindo, a fonte precisa empurrar contra essa força eletromotriz. A potência que ela entrega é essa força eletromotriz, sem o sinal, vezes a corrente. Ou seja: indutância vezes corrente vezes a taxa de variação da corrente.

[thoughtful] Agora, potência é energia por tempo. Então, num pedacinho de tempo, a energia guardada cresce a potência vezes esse pedacinho de tempo. E esse tempo cancela com o tempo que estava na taxa de variação. Sobra: indutância vezes corrente vezes um pedacinho de corrente.

[thoughtful, emphatic] Para a energia total, a gente soma todos esses pedacinhos, desde a corrente zero até a corrente final. A integral da corrente dá a corrente ao quadrado sobre dois. Resultado: a energia vale meio vezes a indutância vezes a corrente ao quadrado.

[thoughtful] Só um cuidado com a interpretação. Essa é a energia guardada quando a corrente tem esse valor. Ela entrou enquanto a corrente subia. Com a corrente constante, ninguém está gastando nada: a energia só fica lá, guardada.

Trocando a indutância pela do solenoide: meio, vezes mi zero, vezes espiras por metro ao quadrado, vezes pi vezes o raio ao quadrado, vezes o comprimento do trecho, vezes a corrente ao quadrado.

Esse resultado vai lá para o alto da tela. Ele é a nossa referência.

[curious] Agora, o segundo caminho: pelo campo. Esquece o circuito um pouquinho e olha só para o espaço dentro do solenoide.

[thoughtful] A densidade de energia magnética é a energia por unidade de volume. Quanta energia tem em cada metro cúbico de campo.

E o eletromagnetismo tem um resultado geral para ela: a densidade de energia é o campo ao quadrado dividido por duas vezes mi zero. Vale para qualquer campo magnético no vácuo. Hoje a gente não vai deduzir; vai usar.

[thoughtful] Repara no brilho: onde tem campo, tem energia. Dentro do solenoide o campo é uniforme, então o brilho é igual em todo lugar. Fora, campo praticamente zero... tudo escuro.

[thoughtful] A energia total é a soma da densidade em cada pedacinho de volume. De novo uma integral, agora de volume.

Como a densidade é a mesma em todo o interior e zero fora, essa integral vira simplesmente densidade vezes o volume de dentro.

E esse volume? Pega o disco da seção e arrasta ao longo do trecho. Ele desenha um cilindro. E volume de cilindro é área da base vezes comprimento: pi vezes o raio ao quadrado vezes o comprimento do trecho.

[thoughtful] Então a energia é o campo ao quadrado sobre duas vezes mi zero, vezes pi, vezes o raio ao quadrado, vezes o comprimento.

Agora troca o campo por mi zero vezes as espiras por metro vezes a corrente. Elevando ao quadrado, tudo vai ao quadrado: mi zero ao quadrado, espiras por metro ao quadrado, corrente ao quadrado.

[thoughtful] Escreve o mi zero ao quadrado como mi zero vezes mi zero... e um deles cancela com o mi zero que está embaixo. [short pause]

Sobra: mi zero, vezes espiras por metro ao quadrado, vezes a corrente ao quadrado, sobre dois, vezes pi, vezes o raio ao quadrado, vezes o comprimento do trecho.

[curious] Agora reorganiza os fatores: o meio vai para a frente, a corrente ao quadrado vai para o final...

[excited] E é exatamente a mesma expressão lá de cima! Meio indutância vezes corrente ao quadrado é igual a densidade de energia vezes volume.

[thoughtful] E isso não é sorte. É a mesma energia, contada de dois jeitos. A conta pelo circuito e a conta pelo campo têm que concordar... e concordam.

[thoughtful, emphatic] Agora olha o que a conta pelo campo diz: a energia está espalhada no volume onde existe campo. O fio só conduz a corrente que cria esse campo.

[calm, satisfied] A pergunta do começo está respondida. A energia do indutor não está no fio. Está no campo magnético, no espaço dentro do solenoide.

Se você chutou "no espaço", pode comemorar. Se chutou "no fio"... relaxa, quase todo mundo chuta.

[calm, satisfied] Se esse exercício te ajudou a enxergar a física por trás da fórmula, se inscreve no Parallax Lab e conta nos comentários qual exercício você quer ver resolvido.

Valeu, pessoal. Até a próxima!
