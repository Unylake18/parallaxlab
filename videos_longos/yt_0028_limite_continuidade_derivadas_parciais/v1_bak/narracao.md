# yt_0028 · narração canônica (Anexo A do handoff v1.2) — uma âncora por parágrafo (fonte do ancoras.json)

### H1 · H · O quadradinho que deforma

[curious] Lembra do campo que fechou o episódio passado? A componente horizontal é a própria coordenada horizontal, e a vertical é menos a coordenada vertical. Coloca um quadradinho de fluido no meio e faz as contas que a gente já conhece. O rotacional dá zero, em todo ponto: nenhuma rodinha gira. O divergente também dá zero: nenhum pedacinho muda de área.

### H2 · H · O quadradinho que deforma

[thoughtful] Então, pelas duas medidas, não acontece nada. Só que agora deixa o fluido andar… e o quadradinho estica para os lados e achata na vertical. A área continua a mesma, e ele não girou nem um grau. Mas virou outra coisa.

### H3 · H · O quadradinho que deforma

[curious] Então tem alguma coisa nesse campo que o rotacional e o divergente não enxergam. Que número mede isso? E de onde ele sai? A resposta está nas derivadas parciais do campo. Só que, para usar essas derivadas com segurança, a gente precisa começar pelo chão: o que quer dizer chegar perto de um ponto.

### A1 · A · Bem-vindos

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab. Hoje são três ideias que se apoiam uma na outra: limite, continuidade e derivadas parciais de um campo vetorial. E, no fim, a gente vai juntar tudo numa tabela de quatro números que mostra, bem de perto, como o campo muda em volta de um ponto.

### B1-1 · B1 · Chegar perto

[thoughtful] Vamos usar duas telas. Na da esquerda está o campo, e é ali que você anda: você escolhe um ponto e vai se aproximando dele. Na da direita, eu pego cada seta e trago para a mesma origem, para comparar só onde a ponta dela chega.

### B1-2 · B1 · Chegar perto

[curious] Repara: conforme você chega perto do ponto, a ponta da seta chega perto da ponta da seta do ponto. É isso que o limite quer dizer. Mas "perto" precisa de um número. Então funciona como um desafio. Alguém escolhe uma tolerância lá na chegada: um disquinho de raio épsilon em volta da ponta. E você precisa responder com um disquinho de raio delta em volta do ponto, de um jeito que todo mundo que estiver dentro do seu disco mande a ponta da seta para dentro do disco dele.

### B1-3 · B1 · Chegar perto

[thoughtful] Com épsilon igual a um, um delta de zero vírgula quatro um já resolve: dá a volta na borda do disco e a ponta não sai do disco da chegada. Se o desafio aperta para meio, você aperta também, para zero vírgula dois um. O limite existe quando você sempre consegue responder, por menor que seja o épsilon. Escrito, é exatamente essa frase: para todo épsilon positivo existe um delta positivo tal que, se a distância até o ponto é maior que zero e menor que delta, a distância da seta até o limite é menor que épsilon. E repara nesse maior que zero: o próprio ponto fica de fora. O limite só olha para quem está chegando, e isso vai fazer diferença daqui a pouco.

### B1-4 · B1 · Chegar perto

[curious] E tem um atalho muito bom. Uma seta está perto de outra exatamente quando cada componente está perto da componente correspondente. Então o limite de um campo existe quando o limite de cada componente existe, e aí é só fazer o limite de funções de várias variáveis que você já conhece. E repara na curva que a ponta desenhou quando você deu a volta no disco: ela não é um círculo. A seta muda mais depressa numa direção do que em outra. E medir essa mudança, direção por direção, é exatamente o trabalho das derivadas parciais.

### B2-1 · B2 · Quando o limite não existe

[curious] Agora um campo encrenqueiro. Todas as setas são horizontais. Nos eixos, não tem seta nenhuma; nas diagonais, as setas têm tamanho um: numa delas apontam para a direita, na outra, para a esquerda.

### B2-2 · B2 · Quando o limite não existe

[thoughtful] Vem andando até a origem pelo eixo horizontal: a seta é zero o caminho todo. Agora vem pela diagonal de subida: a seta é um, para a direita, o caminho todo. E pela outra diagonal: um, para a esquerda. Em cada reta que passa pela origem, o campo é constante, e cada reta tem a sua constante. Fazendo a conta numa reta qualquer pela origem, o campo vale o dobro da inclinação, dividido por um mais a inclinação ao quadrado. Muda a reta, muda o valor.

### B2-3 · B2 · Quando o limite não existe

[thoughtful, emphatic] Então não existe limite na origem. Não tem disquinho em volta da origem que mande todas as pontas para perto de uma seta só. E fica um cuidado importante: dois caminhos dando valores diferentes provam que o limite não existe. Mas todas as retas darem o mesmo valor ainda não provam que ele existe, porque dá para chegar por uma curva.

### B3-1 · B3 · Continuidade

[thoughtful] Agora a continuidade. Um campo é contínuo num ponto do domínio quando o limite ali existe e é igual à própria seta do ponto. Na prática: chegando perto, a seta não dá salto.

### B3-2 · B3 · Continuidade

[curious] Olha três casos. No primeiro, o nosso campo de antes: em volta do ponto, as setas vizinhas são parecidas com a do ponto. Contínuo. No segundo, o campo elétrico de uma carga. Em cima da carga, o campo nem existe: a pergunta "é contínuo ali?" nem se faz, porque continuidade só se pergunta em ponto do domínio. Em todo o resto, ele é contínuo. No terceiro, o campo encrenqueiro, agora definido na origem como zero. Ali ele existe, mas não tem limite. Isso, sim, é descontínuo.

### B3-3 · B3 · Continuidade

[thoughtful] E, de novo, dá para trabalhar por componentes: o campo é contínuo exatamente quando cada componente é contínua. Por isso quase todo campo que vem de fórmula é contínuo onde está definido, porque somas, produtos, quocientes com denominador diferente de zero e composições de funções contínuas continuam contínuas.

### B4-1 · B4 · Derivada parcial de um campo

[thoughtful] Agora sim: medir como a seta muda. Fica no ponto e anda só na horizontal, um passo pequeno. A seta muda de uma para outra, e a diferença entre as duas é um vetor. Divide esse vetor pelo tamanho do passo e encolhe o passo. Esse limite é a derivada parcial do campo na direção horizontal.

### B4-2 · B4 · Derivada parcial de um campo

[curious] Olha os números. Com passo um, o quociente vale zero vírgula oito quatro e dois vírgula um quatro. Com meio, zero vírgula nove seis e dois vírgula um seis. Com passo cada vez menor, ele vai chegando em um e dois. E repara no que acontece lá na tela da chegada: andando na horizontal, a ponta da seta desenha uma curva. A derivada parcial na direção horizontal é exatamente a seta tangente a essa curva, a velocidade da ponta quando você anda na horizontal com velocidade um.

### B4-3 · B4 · Derivada parcial de um campo

[thoughtful] Agora na vertical. Andando para cima, a ponta da seta anda num círculo. E o quociente vai chegando em menos um e zero: a derivada parcial na direção vertical aponta para a esquerda, tangente ao círculo.

### B4-4 · B4 · Derivada parcial de um campo

[thoughtful, emphatic] Então a derivada parcial de um campo não é um número: é um vetor, e ele diz como a seta muda quando você anda numa direção. E a conta é por componentes: derivada da componente horizontal e derivada da componente vertical. Aqui, a derivada na direção horizontal dá cosseno e dois cossenos mais seno, todos da coordenada horizontal; no ponto, um e dois. A derivada na direção vertical dá menos cosseno e seno da coordenada vertical; no ponto, menos um e zero. A conta bate com o desenho.

### B5-1 · B5 · O engano

[curious] Só que tem uma armadilha. Volta no campo encrenqueiro. Calcula as derivadas parciais na origem. Andando pelo eixo horizontal, a seta é zero o tempo todo, então a derivada na direção horizontal é zero. Pelo eixo vertical, mesma coisa: a derivada na direção vertical é zero. As duas existem, e as duas são zero.

### B5-2 · B5 · O engano

[thoughtful] Quem olhasse só para essas duas derivadas ia achar que, perto da origem, o campo quase não muda. E ele nem é contínuo ali! As derivadas parciais só olham duas retas, a horizontal e a vertical, e esse campo esconde tudo nas diagonais.

### B5-3 · B5 · O engano

[thoughtful, emphatic] Por isso aparece a condição de classe cê um: as derivadas parciais existem e são contínuas. Com ela, aí sim, as parciais contam a história inteira perto do ponto: a seta num ponto vizinho é a seta do ponto, mais o passo horizontal vezes a derivada na horizontal, mais o passo vertical vezes a derivada na vertical, com um erro que some mais rápido que o passo. O nosso campo, feito de senos e cossenos, é cê um. O encrenqueiro, não.

### B6-1 · B6 · A tabela

[curious] Então vamos usar isso. Pega o campo da aula e chega bem perto do ponto, dez vezes mais perto. De perto, todas as setas ficam quase iguais à seta do centro. Agora tira a seta do centro de todas elas. O que sobra é só a mudança… e olha que campo arrumadinho apareceu.

### B6-2 · B6 · A tabela

[thoughtful] Bem de perto, essa mudança é escrita com as duas derivadas parciais. Então coloca as duas lado a lado, como colunas: a derivada na horizontal na primeira e a derivada na vertical na segunda. Fica uma tabela de quatro números, com as derivadas das duas componentes nas duas direções. Ela tem nome: matriz jacobiana. No nosso ponto, ela vale um e menos um em cima, dois e zero embaixo.

### B6-3 · B6 · A tabela

[curious] E agora a parte bonita. Usa essa tabela como modelo do campo bem pertinho do ponto e coloca um quadradinho com a quina no ponto. A quina da direita está um passo para o lado, então ela é empurrada pela primeira coluna. A quina de cima está um passo para cima, então é empurrada pela segunda coluna. Cada coluna da tabela empurra uma aresta. Solta o fluido no modelo… e o quadradinho gira, cresce e entorta, tudo ao mesmo tempo. Tudo isso estava guardado nos quatro números.

### B7-1 · B7 · Quatro números, quatro medidas

[thoughtful] E dá para separar essa bagunça. O giro vem de uma combinação da tabela: a derivada da componente vertical na horizontal, menos a da componente horizontal na vertical. É o rotacional. A mudança de área vem de outra: a soma das duas derivadas da diagonal da tabela. É o divergente.

### B7-2 · B7 · Quatro números, quatro medidas

[curious] Só que a tabela tem quatro números, e até agora a gente usou duas combinações. As outras duas são a deformação. A primeira é a derivada da componente horizontal na horizontal, menos a da vertical na vertical: ela diz quanto o pedacinho estica no horizontal mais do que no vertical. A segunda é a derivada da componente vertical na horizontal, mais a da horizontal na vertical: ela faz a mesma comparação, só que entre as duas diagonais.

### B7-3 · B7 · Quatro números, quatro medidas

[thoughtful, emphatic] No nosso ponto: rotacional três, divergente um, e deformação um e um. Quatro números entram, quatro medidas saem, e nada se perde no caminho. Bem de perto e sem a seta do centro, todo campo cê um se comporta como uma mistura de quatro campos simples: um redemoinho, uma explosão e duas deformações. E isso não é só matemática: num fluido, o atrito viscoso vem da deformação. Um bloco de fluido girando inteiro, rígido, não tem atrito viscoso nenhum por dentro.

### B7-4 · B7 · Quatro números, quatro medidas

[curious] Agora volta lá no começo. No campo que esticava o quadradinho, a tabela é um e zero em cima, zero e menos um embaixo. Rotacional zero, divergente zero, e a primeira deformação vale dois. É tudo deformação: estica na horizontal e achata na vertical, na mesma medida.

### B7-5 · B7 · Quatro números, quatro medidas

[happy] E lá no episódio passado ficou um desafio: achar outro campo, que não fosse constante, com rotacional e divergente zero. Um deles é este, que troca as coordenadas de lugar. A tabela dá zero e um em cima, um e zero embaixo. Agora quem vale dois é a segunda deformação: o quadradinho estica numa diagonal e achata na outra. É o mesmo campo de antes, girado quarenta e cinco graus. E quem achou um de segundo grau, como o da tela, também acertou.

### S1 · S · Síntese e encerramento

[thoughtful] Então, resumindo a aula: limite é chegar perto e a seta chegar perto também. Continuidade é a seta não dar salto. A derivada parcial diz como a seta muda numa direção. E, quando essas derivadas são contínuas, as quatro juntas descrevem como o campo muda bem perto do ponto: giro, área e deformação.

### S2 · S · Síntese e encerramento

[excited] No próximo vídeo, a gente coloca o módulo inteiro para trabalhar em exercícios: campo vetorial, rotacional, divergente, limite e derivadas parciais, tudo junto. Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual dessas quatro medidas você acha que aparece mais na física? Até a próxima!
