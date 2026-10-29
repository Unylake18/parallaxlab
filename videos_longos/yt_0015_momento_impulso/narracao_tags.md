# yt_0015 — narração com audio tags (v5.3, para gerar a voz)

Fonte: `narracao_sugestao.md` (âncoras ### = parágrafos daqui, na mesma ordem); gerado por `gerar_narracao_tags.py`. Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`. Tags em inglês, valendo até a próxima; não entram na legenda nem no SRT.

## Texto corrido (para gravação)

[curious] Olha essa queda. O nosso boneco de testes pula de um muro de dois metros e meio e chega no chão de pernas esticadas, duras feito um cabo de vassoura. Em câmera lenta dá para ver: o corpo para quase de uma vez, e o tranco vai direto para os ossos.

[curious] Agora a mesma queda, do mesmo muro, com o mesmo boneco. Só que, dessa vez, ele chega dobrando os joelhos e deixando o quadril descer.

[thoughtful] Pensa comigo: a altura é a mesma, a velocidade de chegada é a mesma, e nos dois casos o corpo termina parado. Então por que dobrar os joelhos salva as suas pernas? Spoiler: não é mágica, nem academia de perna. São duas ideias da física que a gente vai construir hoje: momento linear e impulso.

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

[thoughtful] Hoje o assunto é momento linear e impulso, com um foco bem claro: um corpo só e uma força agindo nele ao longo do tempo. Olha a bolinha: a força empurra, e a velocidade cresce enquanto a força age. À direita, o próximo capítulo da série: vários corpos batendo, e o momento total se conservando.

[curious] Nos vídeos de colisões, essa igualdade foi a nossa ferramenta: momento total antes igual ao momento total depois. Hoje a gente vai até a raiz dela.

[thoughtful] Vamos começar do que você já conhece: a segunda lei de Newton. Uma bolinha de aço fazendo uma trajetória qualquer pelo espaço. Em cada instante ela tem uma velocidade, a seta violeta, tangente à trajetória, e sente uma força resultante, a seta azul, que vai entortando a trajetória para o lado de dentro da curva. A segunda lei diz: força resultante é massa vezes aceleração.

[curious] Mas o que é a aceleração? Vamos usar uma lupa. Pego a velocidade agora e a velocidade um instantinho depois, saindo do mesmo ponto. A diferença entre elas é a variação da velocidade, e repara: conforme o intervalo encolhe, ela aponta junto com a força. A aceleração é essa variação dividida pelo pedacinho de tempo: a derivada da velocidade. Então a força resultante é a massa vezes a derivada da velocidade. E, se a massa não muda, ela entra na derivada sem alterar nada: a força resultante é a derivada da massa vezes a velocidade.

[thoughtful, emphatic] Esse produto, massa vezes velocidade, aparece tanto que ganhou nome: momento linear, ou quantidade de movimento. Na tela, ele vai ser sempre esta seta magenta. Como a massa é positiva, o momento aponta para o mesmo lado da velocidade: é a mesma seta, esticada pela massa. E a unidade sai da definição: quilograma vezes metro por segundo.

[curious] E atenção: o momento é um vetor de verdade. Dois carros iguais, a vinte metros por segundo, um indo para o norte e o outro para o leste. O tamanho do momento é o mesmo nos dois. Mas os momentos são diferentes, porque apontam para lados diferentes. O velocímetro dos dois marca a mesma coisa; o GPS, com certeza, não.

[thoughtful] Na prática, a gente trabalha com componentes. Copio a seta da velocidade para a origem e projeto nos três eixos: aparece a parte da velocidade em x, em y e em z. E cada parte do momento é a massa vezes a parte da velocidade na mesma direção. Três equações com números no lugar de uma com setas.

[thoughtful] Agora volta na segunda lei e troca massa vezes velocidade pelo nome novo: a força resultante é a taxa de variação do momento. Olha o painel: cada barra magenta é uma componente do momento, e a setinha azul ao lado é a componente da força. Seta para cima, a barra cresce; seta para baixo, a barra diminui. A força em x só mexe no momento em x, e o mesmo vale em y e em z. Cada direção cuida da sua vida.

[curious] Curiosidade: foi assim, falando em quantidade de movimento, que o próprio Newton escreveu a segunda lei. Ela vale em referenciais inerciais, e é por ela que a gente vai chegar nos casos em que a massa muda, como um foguete jogando gás para trás. Só que aí tem uma pegadinha: é preciso escolher direitinho o que entra no sistema, e esse cuidado fica para um vídeo desta série. Hoje a massa fica quietinha.

[thoughtful] Então a força resultante muda o momento. E se nenhuma força de fora agir? Vamos ao laboratório. Dois discos iguais sobre um colchão de ar, tipo uma mesa de air hockey: o ar por baixo elimina o atrito. Na primeira experiência, eles vêm um contra o outro com a mesma velocidade, numa batida bem elástica, daquelas que não perdem energia, e voltam, cada um com a velocidade do outro.

[thoughtful] Na segunda, um disco está parado e o outro chega. Depois da batida, quem vinha para, e quem estava parado sai com a velocidade do primeiro. Igualzinho à sinuca.

[thoughtful] Na terceira, a gente gruda um pedacinho de chiclete num dos discos, tão leve que a massa dele nem entra na conta. E não pergunta de onde veio esse chiclete. Eles batem, ficam juntos, e o conjunto segue com metade da velocidade.

[curious] Três finais completamente diferentes. Mas olha a tabela: em cada linha, a massa vezes a velocidade de um disco mais a do outro. Antes e depois, essa soma é a mesma nas três. E com massas diferentes ela continua a mesma.

[thoughtful, emphatic] Isso é uma lei da natureza, tirada direto da experiência: o princípio de conservação do momento. Os momentos de cada disco mudam na batida, mas a soma, o momento total, fica sempre igual: mesmo tamanho e mesmo sentido. Num sistema isolado, sem força de fora, ele não muda.

[curious] Agora, uma pergunta que quase ninguém faz. Por que justamente massa vezes velocidade? Por que não a velocidade sozinha, ou a massa vezes a velocidade ao quadrado? Tem um argumento de simetria muito bonito para isso. Dois carrinhos iguais, parados, com uma mola comprimida entre eles, presa por uma trava. A trava solta, a mola empurra. E, como os carrinhos são iguais, não tem por que um sair mais rápido: saem com a mesma velocidade, um para cada lado. Os fantasmas são fotos a cada meio segundo, e o espaçamento é igual dos dois lados.

[thoughtful] Agora outra experiência: velcro na frente, os dois vêm um contra o outro com a mesma velocidade, batem, grudam... e param. Faz sentido: com tudo simétrico, o conjunto não tem para que lado escolher andar.

[curious] Agora vem o truque. Assista à mesma colisão com uma câmera que anda junto com o carrinho da esquerda. Em cima, quem está parado no chão; embaixo, a câmera. Para ela, o carrinho A está parado e quem anda é o chão, para a esquerda: olha a régua correndo. O carrinho B vem da direita, andando para a esquerda, com o dobro da velocidade. E o conjunto, que no chão ficava parado, para a câmera vai embora para a esquerda, com a velocidade original. Mesma colisão, outro ponto de vista.

[thoughtful] Então a gente ganhou, sem conta nenhuma, uma colisão nova: um carrinho com o dobro da velocidade bate num igual parado, e os dois seguem com metade dela. Olha a conta nascendo dos rótulos: massa vezes o dobro da velocidade, mais zero, dá o dobro da massa vezes a velocidade. Fecha certinho. Agora testa a massa vezes a velocidade ao quadrado: antes dá quatro vezes a massa vezes a velocidade ao quadrado; depois, só duas vezes. Não fecha. E a velocidade sozinha cai assim que as massas são diferentes: olha os outros casos, com um carrinho de massa dupla e um de massa tripla. Em todos eles, só a massa vezes a velocidade fecha. Antes igual a depois, sempre. Isso não é uma demonstração de que nada mais no universo se conserva, tá? Mas mostra por que, entre os candidatos, é esse que a natureza escolhe.

[thoughtful, emphatic] Repara: a grandeza que a segunda lei de Newton entregou lá no começo é a mesma que a simetria aponta agora. Dois caminhos diferentes, o mesmo lugar. Não é coincidência. É o momento linear.

[thoughtful] Agora uma virada que vale ouro. Pensa nos dois discos como um sistema isolado: nenhuma força de fora, só um empurrando o outro. Se o momento total não muda, tudo o que um disco ganha o outro perde. A variação do momento do primeiro é menos a variação do momento do segundo.

[thoughtful] Divide os dois lados pelo tempo da colisão, e vai encolhendo esse tempo, como no cronômetro. O que sobra é a taxa de variação: a derivada do momento de um é menos a derivada do momento do outro, a cada instante.

[thoughtful, emphatic] Só que, lembra do começo? A taxa de variação do momento é a força. Então a força que o segundo disco faz no primeiro é igual e oposta à que o primeiro faz no segundo. Olha só quem apareceu: a terceira lei de Newton, saindo da conservação do momento.

[curious] E aqui mora uma pegadinha clássica. Ação e reação agem sempre em corpos diferentes. O peso e a normal estão os dois no bloco, então não são ação e reação. A reação do peso é o bloco puxando a Terra para cima. E a reação da normal é o bloco empurrando a mesa para baixo. E a Terra está fora de escala, tá? Prometo que ela é um pouquinho maior.

[thoughtful] E por que partir da conservação? Porque ela é mais funda. Entre cargas elétricas em movimento, as forças podem não ser iguais e opostas: a terceira lei falha. Mas a conservação continua valendo se a gente contar também o momento do campo. Ela sobrevive onde a terceira lei não chega.

[thoughtful] Até aqui, a gente olhou para o momento num instante. Agora a pergunta é: o que uma força faz com ele ao longo de um tempo? Isso é o impulso, e vamos construir passo a passo. O caso mais simples: um bloco sem atrito e uma força resultante constante, que liga num instante e desliga noutro. Olha os gráficos andando juntos. Em cima, a força: um degrau. Embaixo, o momento: como a taxa de variação dele é a força, e a força é constante, ele sobe em linha reta. A inclinação da reta é a própria força.

[thoughtful] Com taxa constante, a derivada é a variação total dividida pelo intervalo. No triângulo: na vertical, o momento final menos o inicial; na horizontal, o instante final menos o inicial. Agora passa o intervalo para o outro lado, multiplicando: força resultante vezes o tempo em que ela age é igual ao momento final menos o inicial.

[thoughtful, emphatic] Esse produto, força resultante vezes intervalo, se chama impulso. É um vetor, na direção da força, e é a área do retângulo embaixo do gráfico. E as unidades: newton vezes segundo é quilograma vezes metro por segundo ao quadrado, vezes segundo; um segundo cancela, e sobra quilograma vezes metro por segundo. A mesma unidade do momento, como tinha que ser.

[curious] Só que, numa colisão de verdade, a força não é constante. Antes do contato, a força da parede é praticamente zero. Quando a bola encosta, ela sobe muito rápido, chega num pico enquanto a bola amassa, e volta a zero quando ela se solta. Tudo em centésimos de segundo.

[thoughtful] Então a gente faz o que todo bom físico faz: fatia o problema. Em cada pedacinho de tempo, a força é quase constante, e vale o caso simples: o momento muda de força vezes o pedacinho de tempo. Cada retângulo vira um pedacinho da variação do momento, somado na seta da bola. Quatro, oito, trinta e dois... quanto mais fino, mais a soma cola na curva.

[thoughtful, emphatic] No limite, a soma vira a integral da força resultante no tempo, do instante inicial ao final. Agora troca a força pela derivada do momento: o pedacinho de tempo cancela, e os limites, que eram instantes, viram o momento inicial e o final. Somar pedacinhos de momento dá o momento final menos o inicial. Então vale para qualquer força: o impulso da força resultante é igual à variação do momento.

[thoughtful, emphatic] Geometricamente, o impulso é a área embaixo da curva da força. E a força média é a força constante que daria o mesmo impulso no mesmo intervalo: a altura de um retângulo com a mesma base e a mesma área. Olha embaixo: outra forma, mesma área, vinte newtons vezes segundo. Mesmo impulso. Só a área importa.

[thoughtful] E, como o impulso é um vetor, a gente trabalha componente por componente. A variação do momento vai da ponta do momento inicial até a ponta do final; projetando, aparece o impulso em x e em y. Em x, o impulso é a integral da força em x, é a força média em x vezes o intervalo, e é a massa vezes a velocidade final em x menos a inicial. Em y, a mesmíssima coisa, e em z também.

[thoughtful] Uma dica que vale ponto na prova: escolha os eixos, escreva componente por componente, e respeite os sinais.

[thoughtful] Teoria montada, hora de colocar a mão na massa. E a gente começa pelo sinal, que é onde todo mundo escorrega. Uma bola de quatrocentos gramas chega numa parede a trinta metros por segundo, para a esquerda, e volta a vinte, para a direita. O contato dura um centésimo de segundo. Primeiro passo: escolher o positivo. Aqui, para a direita.

[thoughtful] Então a velocidade inicial é menos trinta e a final é mais vinte. Olha as três setas: o momento inicial para a esquerda, o final para a direita, e a variação ligando as pontas, para a direita. O impulso é a massa vezes a velocidade final menos a inicial: zero vírgula quatro vezes cinquenta. Vinte newtons vezes segundo, para a direita.

[curious] Sem o sinal, alguém faria vinte menos trinta e acharia menos quatro, como se a parede puxasse a bola. Parede com ímã de bola não existe. O sinal é física.

[thoughtful] E a força? A força média é o impulso dividido pelo tempo: vinte sobre um centésimo, dois mil newtons. Perto disso, o peso, três vírgula nove newtons, é uma setinha. Umas quinhentas vezes menor. Por isso, num choque rápido, o peso sai da conta sem culpa.

[thoughtful] E repara: para só parar a bola, o momento iria de doze até zero. Para rebater, vai até zero e ainda volta: a variação sobe para vinte. Rebater pede mais impulso do que só parar. Quem já devolveu uma cortada no vôlei sabe do que eu estou falando.

[thoughtful] Agora em duas dimensões. A mesma bola chega a vinte metros por segundo, para a esquerda, leva um chute e sai a trinta, a quarenta e cinco graus, para cima e para a direita. Contato de um centésimo de segundo.

[thoughtful] Componente por componente. A quarenta e cinco graus, a velocidade final tem as duas partes iguais: uns vinte e um vírgula dois metros por segundo. Na horizontal, a bola ia a vinte para a esquerda e volta a vinte e um vírgula dois para a direita: o impulso horizontal dá dezesseis vírgula cinco newtons vezes segundo. Na vertical, ela não tinha nada e ganhou vinte e um vírgula dois: oito vírgula cinco.

[curious] Dividindo pelo tempo, a força média dá uns mil e novecentos newtons, a vinte e sete graus. Mas espera: a bola saiu a quarenta e cinco! Olha o triângulo dos momentos: a seta que fecha o triângulo, a variação do momento, está a vinte e sete graus, e a força média encaixa certinho em cima dela. A força não aponta para onde a bola vai; ela aponta para onde o momento muda.

[thoughtful] Dica: desenhe o triângulo dos momentos. A força média aponta sempre para a variação do momento.

[thoughtful] Agora uma força que muda com o tempo, para usar a integral de verdade. Um foguete de dois mil cento e cinquenta quilos, no espaço, com um motor cuja força é uma constante vezes o tempo ao quadrado. Repara no jato crescendo junto com o ponto da curva. Em um vírgula vinte e cinco segundo, a força vale setecentos e oitenta e um vírgula vinte e cinco newtons, então a constante é quinhentos newtons por segundo ao quadrado. E um combinado: um foguete de verdade perde massa ao queimar combustível, mas, nesse trecho curto, a gente trata a massa como constante. É uma aproximação.

[thoughtful] Qual é o impulso entre dois segundos e três e meio? A área embaixo da parábola. Os retângulos mostram a ideia; a integral faz a conta: a integral do tempo ao quadrado é o tempo ao cubo sobre três. Dá uns cinco mil oitocentos e doze newtons vezes segundo.

[curious] Dividindo pela massa, a velocidade do foguete sobe dois vírgula setenta metros por segundo. Parece pouco, mas são mais de duas toneladas. E a força média do trecho, a área dividida por um segundo e meio, é de três mil oitocentos e setenta e cinco newtons.

[thoughtful] Agora o insight mais importante da aula. A mesma força resultante pode ser acumulada de dois jeitos. No tempo, ela dá o impulso, que muda o momento. Na distância, contando a parte da força que está na direção do deslocamento, ela dá o trabalho, que muda a energia cinética.

[thoughtful] E as duas conversam. A energia cinética é metade da massa vezes a velocidade ao quadrado; a velocidade é o momento dividido pela massa. Substituindo: a energia cinética é o momento ao quadrado sobre duas vezes a massa.

[curious] Olha esse exemplo. Você, de luva, vai agarrar uma bola de meio quilo a quatro metros por segundo ou uma de cem gramas a vinte. As duas têm o mesmo momento, dois quilogramas vezes metro por segundo: mesmo impulso. Então, se a luva frear as duas com a mesma força constante, o tempo para parar é o mesmo. Mas a energia cinética da leve é cinco vezes maior, vinte joules contra quatro. Com essa mesma força constante, a luva precisa recuar cinco vezes mais para segurar a leve. Parece estranho, mas é a bolinha leve que dá mais trabalho. E dá trabalho no sentido da física mesmo.

[thoughtful] E o contrário: dois barcos no gelo, sem atrito, partindo do repouso, um com o dobro da massa do outro, cada um recebendo a mesma força horizontal constante até a mesma linha de chegada. O vento na tela é só a nossa forma de desenhar essa força. Mesma força, mesma distância: mesma energia cinética. Mas o pesado demora mais, fica mais tempo sob o vento, e chega com raiz de dois vezes mais momento.

[thoughtful, emphatic] Guarda essa dica: se o problema fala de tempo, pense em impulso e momento. Se fala de distância, pense em trabalho e energia.

[curious] E agora a gente tem tudo o que precisa para voltar ao muro do começo. O boneco tem oitenta quilos e cai de dois metros e meio. Da altura sai a velocidade de chegada: uns sete metros por segundo. Para parar, o momento dele vai de quinhentos e sessenta quilogramas vezes metro por segundo até zero. Nos dois casos.

[thoughtful, emphatic] Então o impulso resultante é o mesmo nas duas aterrissagens: a mesma área. O que muda é o formato. Para fazer as contas, vamos usar um modelo simples: em cada aterrissagem, a desaceleração é constante, então a força resultante é um retângulo no gráfico. De perna dura, o corpo para em um centésimo de segundo: um retângulo altíssimo e fininho. Dobrando os joelhos e descendo meio metro, uns catorze centésimos: um retângulo baixo e largo. Na vida real a força sobe e desce, mas a área é a mesma. E o gráfico está em escala real, sem trapaça.

[thoughtful] Primeiro caminho, pelo impulso: a força resultante média é a área dividida pelo tempo. De perna dura, cinquenta e seis mil newtons, para cima. Dobrando os joelhos, uns três mil novecentos e vinte.

[thoughtful] Segundo caminho, pela dica de agora há pouco: o problema também tem uma distância. A energia cinética na chegada é mil novecentos e sessenta joules, e ela tem que sumir. Repara no sinal: a força resultante aponta para cima, e o corpo ainda desce. Por isso o trabalho dela é negativo, menos mil novecentos e sessenta joules. Em módulo, a força vezes a distância tem que tirar esses mil novecentos e sessenta. Em meio metro de agachamento, dá três mil novecentos e vinte newtons. De perna dura, o corpo para em três centímetros e meio, e dá de novo cinquenta e seis mil. Os dois teoremas concordam, e concordam porque, no nosso modelo, a força é constante.

[curious] Só que a pergunta de verdade é com que força o chão empurra você, e o chão ainda segura o seu peso. Então a força do chão é a resultante mais o peso. De perna dura, umas setenta e duas vezes o seu peso. Dobrando os joelhos... umas seis.

[excited] Está aí a resposta! Dobrar os joelhos não muda o impulso: muda o tempo e a distância da parada, e isso derruba a força nos seus ossos de setenta e dois para seis pesos. É a física do airbag, do capacete e do colchão do salto em altura: todos esticam o tempo e a distância da parada. E é por isso que carro moderno amassa de propósito na frente. Amassar é ganhar tempo.

[curious] Agora um desafio, com a atleta mais subestimada do reino animal: a pulga. Dois miligramas, e é miligrama mesmo, de massa. No nosso problema, ela pula meio metro de altura. Na vida real é um pouco menos, mas a gente dá esse desconto para ela. E, no empurrão, estica as patas e sobe só um milímetro antes de sair do chão. Com que força ela empurra o chão, comparada com o peso dela?

[thoughtful] Para subir meio metro, ela precisa sair a uns três vírgula um metros por segundo. O problema dá uma distância, o milímetro do esticão, então vamos pela distância. Supondo que, nesse esticão, ela acelere de forma constante, a aceleração é a velocidade ao quadrado sobre duas vezes essa distância. Repara que isso vira a gravidade vezes a altura do pulo dividida pelo esticão. Quinhentas vezes a gravidade.

[thoughtful] Pelo tempo também dá, e serve de conferência. Com aceleração constante, a velocidade média no esticão é metade da velocidade de saída, então o empurrão dura uns sessenta e quatro centésimos de milissegundo, e o momento de saída dividido por esse tempo dá a mesma força. A mesma física pelos dois teoremas.

[thoughtful, emphatic] Agora a pegadinha: a pergunta é a força que a pulga faz no chão, não a força resultante. Como no muro, o chão também segura o peso. Esse mais um aqui é o peso: quinhentos e um pesos, e não quinhentos. Força de contato não é força resultante.

[curious] Em números, cerca de um grama-força. Parece nada, né? Mas, na proporção, é como uma pessoa de setenta quilos empurrando o chão com o peso de trinta e cinco toneladas. Da próxima vez que você vir uma pulga, mais respeito.

[thoughtful] Então, a pergunta do começo está respondida. Dobrar os joelhos não muda o impulso resultante necessário para parar você: ele é sempre a variação do momento. O que muda é o tempo da parada, e junto com ele a distância. Mesma área, mais tempo, menos força média.

[calm, satisfied] Resumindo: o momento é massa vezes velocidade, a grandeza que sai da segunda lei e que a natureza conserva. O impulso da força resultante é a área embaixo da força no tempo e é igual à variação do momento. E, na hora do problema: tempo conversa com momento, distância conversa com energia.

[happy] Se essa aula ajudou você a enxergar o momento de outro jeito, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

[curious] E fica a pergunta para o próximo vídeo: se a corda puxa o cavalo para trás com a mesma força com que puxa a pedra para a frente, como é que o cavalo sai do lugar? Deixa o seu palpite nos comentários. No próximo vídeo: o momento de um sistema inteiro. Até a próxima!
