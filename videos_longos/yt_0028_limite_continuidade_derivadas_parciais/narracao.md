# yt_0028 · narração por âncora (v5, fonte do `ancoras.json`)

Uma âncora por parágrafo da fala. As âncoras são PARÁGRAFOS, não as cenas do handoff.

### H1 · tela: campo (x, −y) nasce em onda a partir do centro (M1); `F⃗ = (x, −y)`; o quadradinho com malha entra; `rot F⃗ = 0`, `div F⃗ = 0` (alvo 01)
[curious] Lembra do campo que fechou o episódio passado? A componente horizontal é o próprio x, e a vertical é menos y. Coloca um quadradinho de fluido no meio e faz as contas que a gente já conhece. O rotacional dá zero, em todo ponto: nenhuma rodinha gira. O divergente também dá zero: nenhum pedacinho muda de área. Então, pelas duas medidas, não era para acontecer nada, certo?

### H2 · tela: o fluido anda: o quadradinho estica e achata; `ÁREA 1,44 → 1,44`; `MAS DEFORMA`
[thoughtful] Só que agora deixa o fluido andar… e olha o que acontece: o quadradinho estica para os lados e achata na vertical. A área continua a mesma, e ele não girou nem um grau. Mas a forma mudou completamente.

### H3 · tela: `QUE NÚMERO MEDE ISSO?`; `A RESPOSTA: AS DERIVADAS PARCIAIS`; `∂F/∂x`, `∂F/∂y`; `MAS ANTES, O CHÃO:` (alvo 02)
[curious] Então tem alguma coisa nesse campo que o rotacional e o divergente não enxergam. Que número mede isso? E de onde ele sai? A resposta está nas derivadas parciais do campo. Só que, para usar essas derivadas com segurança, a gente precisa começar pelo chão: o que quer dizer chegar perto de um ponto.

### A1 · tela: logo com os dois anéis e `BEM-VINDOS AO PARALLAX LAB`; depois título e a lista `NESTE VÍDEO` (§2.1, alvos 38 e 39); o canto entra no fim
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Esse é o terceiro episódio da nossa série de Cálculo três. Hoje a gente olha um campo vetorial bem de pertinho. [thoughtful] Porque a seta de um ponto não basta: é preciso entender as setas vizinhas. Para isso, entram três ideias, uma apoiada na outra. Primeiro, o limite: o que quer dizer chegar perto de um ponto, com o épsilon e o delta desenhados, e não só escritos. Depois, a continuidade: quando a seta não dá pulo, e três jeitos de ela falhar. E, por fim, as derivadas parciais, que medem como a seta muda em cada direção. [curious] No meio do caminho tem um engano, em que as derivadas parciais mentem sobre o campo. E, no final, a gente junta tudo numa tabela de quatro números, que revela o giro, a mudança de área e aquela deformação do quadradinho que ficou sem explicação. [happy] Então vamos começar pelo chão: o que é chegar perto?

### B1-1 · tela: layout B, dois painéis; a seta de X em destaque e a cópia que viaja para a origem (§2.4, alvo 41)
[thoughtful] Vamos usar duas telas. Na da esquerda está o campo, e é ali que você anda: tem um ponto fixo, e você vai se aproximando dele. A seta do lugar onde você está fica em destaque. Na da direita, eu trago essa seta para a mesma origem, para comparar só onde a ponta dela chega. Uma tela mostra por onde você anda; a outra, onde a seta chega.

### B1-2 · tela: os dois números (‖X − P‖ e ‖F(X) − L‖) encolhendo juntos; `∀ε`/`∃δ` ainda não
[curious] Conforme você chega perto do ponto, a ponta da seta vai chegando perto de uma seta-alvo. Essa seta-alvo é a candidata a limite. Os dois números de baixo contam a história: a distância até o ponto encolhe, e a distância da ponta até o alvo encolhe junto. Só que "encolhe junto" ainda é vago. Perto quanto? Então a definição vira um desafio.

### B1-3 · tela: o disco ε, o disco δ e a mancha das pontas (alvo 03)
[thoughtful] Primeiro, alguém escolhe uma tolerância na chegada: um disquinho de raio épsilon em volta da ponta do alvo. É como se dissesse: quero todas as respostas aqui dentro. Qualquer épsilon pode ser escolhido, por isso a definição começa com "para todo épsilon". Depois é a sua vez: você responde com um disquinho de raio delta em volta do ponto. E olha o que acontece do outro lado: cada ponto do seu disco manda a ponta da seta para algum lugar, e todas essas pontas juntas formam uma mancha. A pergunta é uma só: a mancha cabe no disco épsilon?

### B1-4 · tela: δ = 0,7 vaza em vermelho; δ = 0,41 cabe; tabela ε → δ (alvo 04)
[curious] Com delta igual a zero vírgula sete, não cabe: um monte de pontas escapa. Diminui o delta… e a mancha encolhe junto. Em zero vírgula quatro um, ela fica inteira por dentro. Achou: é isso que "existe delta" quer dizer. Se o desafio aperta para meio, você aperta para zero vírgula dois um. Para um quarto, zero vírgula um zero. O delta depende do épsilon, e o limite existe quando você sempre consegue responder.

### B1-5 · tela: ponto de acumulação, ponto isolado e a definição escrita (alvos 05 e 06)
[thoughtful] E tem um detalhe no seu disco: o próprio ponto fica de fora. É o "maior que zero" da definição. O limite só olha para quem está chegando, nunca para o que acontece em cima do ponto. Aliás, o ponto nem precisa estar no domínio: basta ter pontos do domínio tão perto dele quanto você quiser. O nome disso é ponto de acumulação. Já um ponto do domínio sozinho, sem vizinhos, não serve: ninguém chega perto dele. Agora sim, escrito: a seta-alvo é o limite quando, para todo épsilon positivo, existe um delta positivo tal que, para todo ponto do domínio a uma distância maior que zero e menor que delta, a seta fica a menos de épsilon do alvo. A metade da esquerda fala de onde você anda. A da direita, de onde a seta chega.

### B1-6 · tela: as sombras na grade e o quadrado que cabe no disco (alvo 07)
[curious] E tem um atalho. Se a ponta está no disco épsilon, as duas sombras dela, a horizontal e a vertical, ficam a menos de épsilon das sombras do alvo. E o contrário também vale: se as duas sombras estão perto, a ponta cai num quadrado, que cabe num disco só um pouquinho maior. Então o limite de um campo existe exatamente quando o limite de cada componente existe, e aí é o limite de funções de várias variáveis que você já conhece. Mas guarda uma coisa: com várias variáveis, o caminho pelo qual você chega pode mudar completamente a resposta.

### B2-1 · tela: o campo G, os três caminhos (alvo 08)
[curious] E é justamente isso que acontece com este campo encrenqueiro. Todas as setas são horizontais. Nos eixos, não tem seta nenhuma; nas diagonais, as setas têm tamanho um: numa delas apontam para a direita, na outra, para a esquerda. Só que a resposta muda com a direção por onde a gente chega.

### B2-2 · tela: a reta de inclinação m e `2m/(1+m²)`
[thoughtful] Vem andando até a origem pelo eixo horizontal: a seta é zero o caminho todo. Pela diagonal de subida: um, para a direita. Pela outra: um, para a esquerda. Numa reta qualquer pela origem, o campo vale o dobro da inclinação, dividido por um mais a inclinação ao quadrado. Três caminhos, três resultados diferentes. Muda a reta, muda o valor.

### B2-3 · tela: `G = (sen 2θ, 0)`, a volta no círculo e a ponta varrendo o segmento (alvo 09)
[curious] E dá para ver isso de um jeito mais bonito. Em coordenadas polares, a componente horizontal vira o seno do dobro do ângulo. O campo não depende da distância, só da direção. Então dá uma volta num círculo minúsculo em volta da origem: a ponta da seta varre o segmento inteiro, de menos um até um. Diminui o raio… e diminui de novo: acontece exatamente a mesma coisa, por menor que seja o círculo.

### B2-4 · tela: o desafio ε = 1/2 não cabe; o campo K e a parábola (alvo 10)
[thoughtful, emphatic] Agora joga o desafio. Escolhe um alvo qualquer e um épsilon de meio. O disco tem largura um, e o segmento tem largura dois: não cabe, seja qual for o alvo. Então não existe limite na origem. E fica um cuidado: dois caminhos com valores diferentes provam que o limite não existe. Mas todas as retas darem o mesmo valor ainda não provam que ele existe, porque dá para chegar por uma curva. Olha este campo: por qualquer reta, a seta vai para zero. Mas, pela parábola, ela fica em meio o caminho todo. Também não tem limite.

### B3-1 · tela: os três pedaços ①②③ (alvo 11)
[thoughtful] Agora a continuidade. A definição tem três pedaços, e cada um pode falhar. Um: o ponto está no domínio, então a seta do ponto existe. Dois: o limite ali existe. Três: o limite é igual à própria seta do ponto. Na figura, é o mesmo desafio de antes, só que agora o disco épsilon fica em volta da ponta da seta do próprio ponto. No nosso campo, a mancha cabe. Contínuo.

### B3-2 · tela: três cartões com os caminhantes (§2.5, alvos 42 e 12)
[curious] Agora, três jeitos de dar errado, e em cada um você vai chegando no ponto para ver o que a seta faz. No campo elétrico de uma carga, o ponto da carga nem está no domínio, e quanto mais você chega perto, mais a seta cresce. Falha o primeiro pedaço, e a pergunta nem se faz; em todo o resto, ele é contínuo. No campo encrenqueiro, definido como zero na origem, a seta existe, mas o limite não: dependendo do caminho por onde você chega, a seta vai para a direita, para a esquerda ou para zero. Falha o segundo. E neste aqui todas as setas apontam para a direita, menos a do centro, que aponta para cima. Chegando de qualquer lado, a seta é para a direita; só em cima do ponto ela vira para cima. O limite existe e é a seta para a direita, mas a seta do ponto é outra. Falha o terceiro: um salto bem em cima do ponto.

### B3-3 · tela: componentes e operações (alvo 13)
[thoughtful] E, de novo, por componentes: o campo é contínuo exatamente quando cada componente é contínua. Por isso quase todo campo que vem de fórmula é contínuo onde está definido: somas, produtos, quocientes com denominador diferente de zero e composições de funções contínuas continuam contínuas. A primeira componente do nosso campo é uma constante mais senos: contínua. E o campo da carga é um quociente: contínuo em todo lugar, menos em cima da carga.

### B4-1 · tela: a corda em x e o quociente (alvo 14)
[thoughtful] Agora sim: medir como a seta muda. Fica no ponto e anda só na horizontal, um passo. A seta muda de uma para outra, e a diferença entre as duas é um vetor, que liga a ponta velha à ponta nova. Divide esse vetor pelo tamanho do passo e encolhe o passo. Esse limite é a derivada parcial do campo na direção horizontal.

### B4-2 · tela: a velocidade da ponta e as sombras (alvo 15)
[curious] Com passo um, o quociente vale zero vírgula oito quatro e dois vírgula um quatro. Com meio, zero vírgula nove seis e dois vírgula um seis. Com passo cada vez menor, ele vai chegando em um e dois. E olha a tela da chegada: andando na horizontal, a ponta da seta desenha uma curva. A diferença é uma corda dessa curva, e, dividida pelo passo, ela vira a seta tangente. Então a derivada parcial é a velocidade da ponta, quando você anda na horizontal com velocidade um.

### B4-3 · tela: as duas sombras: `∂P/∂x = 1`, `∂Q/∂x = 2`
[thoughtful] E essa velocidade tem duas sombras. A horizontal diz quanto muda a componente horizontal do campo: um. A vertical diz quanto muda a componente vertical: dois. Por isso a conta é por componentes: a derivada do campo é a derivada de cada componente.

### B4-4 · tela: a derivada em y (alvo 16)
[curious] Agora na vertical. Andando para cima, a ponta anda num círculo, e o quociente vai chegando em menos um e zero: a derivada na direção vertical aponta para a esquerda, tangente ao círculo.

### B4-5 · tela: as derivadas no palco e as fórmulas (alvo 17)
[thoughtful, emphatic] Então a derivada parcial de um campo não é um número: é um vetor, que diz como a seta muda quando você anda numa direção. Na conta, a derivada na horizontal dá cosseno e dois cossenos mais seno, da coordenada horizontal; no ponto, um e dois. A derivada na vertical dá menos cosseno e seno da coordenada vertical; no ponto, menos um e zero. A conta bate com o desenho. E, num campo no espaço, aparece uma terceira, na direção da profundidade, com a mesma ideia.

### B5-1 · tela: o campo G: as duas parciais valem zero (alvo 18)
[curious] Só que tem uma armadilha. Volta no campo encrenqueiro e calcula as derivadas parciais na origem. Pelo eixo horizontal, a seta é zero o tempo todo: derivada zero. Pelo vertical, mesma coisa. As duas existem, e as duas são zero.

### B5-2 · tela: previsão × imagem de verdade (alvo 19)
[thoughtful] Se você confiasse só nelas, ia prever que, perto da origem, tudo vai para perto do zero: um quadradinho em volta da origem iria parar num ponto só. Mas olha a imagem de verdade: a ponta varre o segmento inteiro, de menos um até um. A previsão errou feio. As parciais só olham duas retas, e esse campo esconde tudo nas diagonais. Ele nem é contínuo na origem.

### B5-3 · tela: gráficos da derivada: sempre 1 × 2/y; classe C¹ (alvo 20)
[thoughtful, emphatic] O que faltou? Olha as próprias derivadas, andando pelo eixo vertical. No nosso campo, a derivada na horizontal vale um o caminho todo, sem salto nenhum. No encrenqueiro, ela vale dois dividido pela altura: explode perto da origem, e na origem vale zero. Essa é a condição de classe cê um: as derivadas parciais existem e são contínuas, numa vizinhança do ponto. Ela é suficiente para a aproximação linear funcionar. Classe cê erre é o mesmo, até as derivadas de ordem erre.

### B5-4 · tela: a malha vira quase paralelogramo (alvo 21) e o gráfico erro ÷ passo (alvo 22)
[curious] E com ela vem a promessa. Pega uma malhinha em volta do ponto e manda para a tela da chegada. As linhas horizontais viram curvas na direção da derivada horizontal, e as verticais, curvas na direção da derivada vertical. Cada quadradinho da malha vira quase um paralelogramo, com lados de passo vezes derivada. Escrito: a seta num ponto vizinho é a seta do ponto, mais o passo horizontal vezes a derivada na horizontal, mais o passo vertical vezes a derivada na vertical, com um erro que some mais rápido que o passo. O nosso campo, feito de senos e cossenos, é cê um. O encrenqueiro, não. E dá para ver isso dividindo o erro pelo passo. No nosso campo, quando o passo cai pela metade, essa conta cai pela metade também, e vai para zero. No encrenqueiro, ela dobra. É a diferença entre ter duas derivadas parciais e ter uma aproximação linear de verdade.

### B6-1 · tela: janela com zoom ×10, a seta do centro e o resto (alvos 23 a 25)
[curious] Então vamos usar isso. Pega o campo da aula e chega dez vezes mais perto do ponto: essa janelinha vira o palco inteiro. De perto, todas as setas ficam parecidas com a seta do centro. Cada uma é a seta do centro, mais um restinho. Tira a seta do centro de todas… e sobra só a mudança. Olha que campo arrumadinho.

### B6-2 · tela: a matriz jacobiana (alvo 26)
[thoughtful] Bem de perto, essa mudança é escrita com as duas derivadas. Então coloca as duas lado a lado, como colunas: a derivada na horizontal na primeira, a derivada na vertical na segunda. Fica uma tabela de quatro números, com as derivadas das duas componentes nas duas direções. Ela tem nome: matriz jacobiana. No nosso ponto, um e menos um em cima, dois e zero embaixo.

### B6-3 · tela: `J·H` como combinação das colunas (alvo 27)
[curious] E ela funciona assim: um passo com uma parte horizontal e uma vertical vira a parte horizontal vezes a primeira coluna, mais a parte vertical vezes a segunda. A seta do modelo é a soma das duas. É a primeira aproximação do campo perto do ponto.

### B6-4 · tela: as colunas empurram as arestas e o fluxo do modelo (alvos 28 e 29)
[thoughtful] Agora coloca um quadradinho com a quina no ponto. A quina da direita é empurrada pela primeira coluna; a de cima, pela segunda. Cada coluna empurra uma aresta. Solta o fluido no modelo… e o quadradinho gira, cresce e entorta, tudo ao mesmo tempo. Tudo isso, no modelo linear, estava nos quatro números.

### B7-1 · tela: a matriz de movimentos de aresta (alvo 30)
[thoughtful] E dá para separar essa bagunça, lendo cada número da tabela como um movimento de aresta. Em cima, à esquerda: quanto a aresta horizontal estica. Aqui, um. Embaixo, à esquerda: quanto ela gira. Dois. Em cima, à direita: quanto a aresta vertical tomba para o lado. Menos um, para a esquerda. Embaixo, à direita: quanto ela estica. Zero.

### B7-2 · tela: as combinações: rot, div, deformações (alvos 31 e 33)
[curious] Agora junta. Os dois giros no mesmo sentido, somados, dão o rotacional: dois mais um, três. Os dois estiramentos somados dão o divergente: um mais zero, um. E sobram duas comparações. Estiramento horizontal menos vertical: um. Essa é a primeira deformação, quanto o pedacinho estica mais numa direção do que na outra. E a diferença entre os dois giros: dois menos um, um. Essa é a segunda, quanto o ângulo reto do quadradinho fecha, como uma tesoura.

### B7-3 · tela: os três cartões, com o quadradinho agindo (§2.6, alvos 32 e 34)
[thoughtful, emphatic] Quatro números entram, quatro medidas saem, e nada se perde no caminho. Bem de perto e sem a seta do centro, a variação de primeira ordem de todo campo cê um é uma mistura de quatro campos simples: um redemoinho, uma explosão e duas deformações. Olha cada um agindo no quadradinho: o redemoinho gira, a explosão cresce, a deformação estica de um lado e achata do outro. E isso não é só matemática: num fluido newtoniano, o atrito viscoso vem da deformação. Um bloco de fluido girando inteiro, rígido, não tem atrito viscoso nenhum por dentro.

### B7-4 · tela: volta ao gancho: tudo é deformação (alvo 35)
[curious] Agora volta lá no começo. No campo que esticava o quadradinho, a tabela é um e zero em cima, zero e menos um embaixo. A aresta horizontal estica, a vertical encolhe na mesma medida, e ninguém gira. Rotacional zero, divergente zero, e a primeira deformação vale dois. É tudo deformação.

### B7-5 · tela: o desafio do episódio passado (alvo 36)
[happy] E lá no episódio passado ficou um desafio: achar outro campo, que não fosse constante, com rotacional e divergente zero. Um deles é este, que troca as coordenadas de lugar. As duas arestas giram uma contra a outra: a segunda deformação vale dois, e o quadradinho vira losango. É o mesmo campo de antes, girado quarenta e cinco graus. E quem achou um de segundo grau, como o da tela, também acertou. Rotacional e divergente, sozinhos, não dizem tudo sobre como um campo varia.

### S1 · tela: o resumo (alvo 37); a tag do zoom não aparece aqui (§2.7)
[thoughtful] Resumindo: limite é ganhar o desafio do épsilon com um delta. Continuidade é o limite igual à seta do ponto, sem salto. A derivada parcial é a velocidade da ponta numa direção. E, quando essas derivadas são contínuas, a tabela delas descreve o campo bem perto do ponto: giro, área e deformação. E uma curiosidade: no espaço, a tabela tem nove números, que se separam em três de giro, um de volume e cinco de deformação.

### S2 · tela: o cartão do próximo vídeo (§2.2, alvo 40), depois o CTA padrão
[excited] No próximo vídeo, é a vez de colocar a mão na massa: o integrador do módulo, só com exercícios. Campo vetorial, rotacional, divergente, limite e continuidade, derivadas parciais, tudo junto. E vai ser a sua hora de pegar um campo, montar a tabela e descobrir se o quadradinho vai girar, mudar de área ou deformar. [happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: qual dessas medidas, giro, expansão ou deformação, você acha que aparece mais na física? Até a próxima!
