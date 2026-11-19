# yt_0014 — narração com audio tags (v1.2.1, para gerar a voz)

Fonte: `narracao_sugestao.md` (âncoras ### = parágrafos daqui, na mesma ordem); gerado por `gerar_narracao_tags.py`. Tags em inglês, valendo até a próxima; não entram na legenda nem no SRT. **Sem tags de ritmo lento (pedido do usuário).**

## Texto corrido (para gravação)

[curious] Olha essa colisão. Um disco pesado vem da esquerda e bate num disco leve, parado. Repara: o pesado desvia só um pouquinho para cima, e o leve sai de lado.

Será que o pesado poderia ter saído por qualquer caminho? Vinte e cinco graus? Quarenta graus?

Spoiler: a natureza tem um segurança na porta, e ele não deixa passar qualquer direção. Por quê? [short pause] É isso que a gente vai descobrir hoje.

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

[thoughtful] Hoje a gente vai para as colisões em duas dimensões. A ideia é você sair daqui sabendo para onde os corpos podem sair depois de um choque... e, principalmente, para onde eles não podem. Sem bola de cristal: só geometria e uma boa dose de paciência. Bora?

Este vídeo é a continuação direta do anterior. Lá, tudo acontecia numa linha, um trilho, e a gente viu que conservar o momento não basta: o tipo de colisão dá a condição que falta. Agora a gente mantém essa lógica e muda uma coisa só. Só que a vida real não tem trilho. Pensa numa sinuca, ou em dois carros num cruzamento: depois do choque, cada corpo pode sair para qualquer lado do plano.

Ou seja: uma dimensão é só um caso especial. A física é a mesma; o que muda é que agora a geometria entra em cena.

Antes da colisão, o corpo um vem com o seu momento linear, também chamado de quantidade de movimento: a massa vezes a velocidade. O corpo dois está parado, então o momento dele é zero. Depois, os dois saem em direções diferentes, cada um com o seu momento final.

O momento total antes é só o do corpo um. Depois, é a soma dos dois momentos finais. Mas atenção: é soma de vetores, e vetor tem direção. Não dá para somar só os tamanhos.

[thoughtful, emphatic] Num choque muito curto, com massas constantes e tudo no plano, o impulso externo é desprezível, e o momento total se conserva: antes é igual a depois. Essa é a equação-mãe do vídeo. Pode tatuar. Brincadeira... mas anota.

[curious] E essa soma vira um triângulo: o momento inicial na base, o final do corpo um saindo da mesma origem, e o do corpo dois ponta com cauda, fechando. Em uma dimensão era uma reta. Em duas, ele se abre, e a geometria aparece.

[thoughtful] Agora a gente põe eixos: o horizontal na direção do momento inicial. O ângulo de saída do corpo um se mede para cima; o do corpo dois, para baixo, a partir da horizontal. Combinado? Isso derruba muita gente.

Projeta no eixo horizontal: o momento inicial é a soma das duas projeções, cada uma com o cosseno do seu ângulo. Projeta no vertical: o que sobe é igual ao que desce, com o seno. Uma conservação vetorial virou duas equações com números comuns.

[thoughtful, emphatic] Só que ainda sobra incógnita para equação: os módulos dos dois momentos e os ângulos de saída. É tipo tentar pagar várias contas com duas notas. Falta uma condição física, e ela vem do tipo de colisão. Elástica: a energia cinética se conserva. Completamente inelástica: os dois saem com a mesma velocidade. Ou o problema entrega outra. Moral da história: momento, mais condição física.

[curious] Primeiro caso, o mais bonito: massas iguais, alvo parado e colisão elástica. Pensa na sinuca: a bola branca bate numa parada, de massa igual. Quem nunca torceu para a branca não cair na caçapa?

[thoughtful] Pelo momento, a massa é a mesma em todo mundo, então cancela. Sobra a velocidade inicial igual à soma vetorial das duas velocidades finais: um triângulo de velocidades. E repara: por enquanto, o ângulo entre as finais pode ser qualquer um.

Pela energia cinética, o meio e a massa cancelam também: o quadrado da velocidade inicial é igual à soma dos quadrados das duas velocidades finais. Guarda essa.

[curious] Agora o truque: eleva ao quadrado a relação vetorial. Aparece um termo cruzado, o produto escalar das duas velocidades finais: o tamanho de um, vezes o do outro, vezes o cosseno do ângulo entre eles.

[thoughtful] Compara com a energia: a parte de cima é igualzinha! Dois caminhos, o mesmo resultado. Então o termo cruzado tem que ser zero.

[thoughtful, emphatic] E produto escalar zero, com o cosseno do ângulo, só acontece em noventa graus: as duas velocidades finais são perpendiculares. É o famoso ângulo reto da sinuca.

[thoughtful] Um cuidado: no choque frontal, uma das velocidades finais é zero, e não dá para falar de ângulo. No desvio oblíquo, é sempre noventa graus.

[thoughtful, emphatic] E guarda as três condições juntas: elástica, massas iguais e alvo parado. Faltou uma? Dá ruim.

[curious] Um exercício clássico de bilhar: uma bola a dez metros por segundo bate numa parada, de mesma massa, em colisão elástica, e desvia trinta graus. Para onde vai a segunda, e com que velocidades?

[thoughtful] Massas iguais: as velocidades finais são perpendiculares, então o triângulo é retângulo, com a hipotenusa igual a dez. Trinta e sessenta dão noventa: a segunda sai a sessenta graus.

A primeira é o cateto do trinta: dez vezes o cosseno de trinta, cinco raiz de três, uns oito vírgula sete metros por segundo. A segunda é o outro cateto: dez vezes o seno de trinta, cinco metros por segundo. Pitágoras confere. Olha só: sinuca é aula de trigonometria disfarçada.

[curious] E se as massas forem diferentes? O ângulo reto some. Mas o triângulo de momentos continua valendo, porque vem só da conservação. Dele sai que o momento final do corpo dois é o inicial menos o final do corpo um.

[thoughtful] A lei dos cossenos liga os tamanhos ao ângulo: é um Pitágoras com um ajuste, menos duas vezes o produto dos lados vezes o cosseno do ângulo de saída. Se o ângulo for reto, volta o Pitágoras de sempre.

A condição física é a energia cinética conservada, que dá para escrever com o momento: momento ao quadrado sobre duas vezes a massa. Para não carregar duas massas, a gente cria a razão entre elas, o corpo dois dividido pelo corpo um, que na tela aparece como lambda. Daqui para frente, só "a razão das massas".

[curious] Igualando as duas formas do quadrado do momento do corpo dois, sai uma equação do segundo grau no módulo do momento final do corpo um. A gente não vai resolver. A gente vai perguntar: o que ela diz, geometricamente, sobre todos os momentos finais possíveis? Segura essa pergunta.

[thoughtful] Primeiro, o produto dos tamanhos vezes o cosseno é o produto escalar: a gente reescreve na forma vetorial. Depois, divide tudo por um mais a razão das massas: o um mais a razão vai parar embaixo de cada termo.

[thoughtful, emphatic] Agora o truque dos tempos de colégio: completar o quadrado. Aquele que você jurava que nunca ia usar na vida... [short pause] chegou a hora. Um quadrado perfeito tem esse formato: o primeiro ao quadrado, menos duas vezes o primeiro vezes o segundo, mais o segundo ao quadrado. Aqui, o termo do meio já esconde o segundo: o momento inicial dividido por um mais a razão. Falta só o quadrado dele, e a gente soma nos dois lados, para a equação não mudar.

[thoughtful] Agora o lado esquerdo é um quadrado perfeito: o módulo de um vetor, ao quadrado. E o lado direito simplifica bonito: a conferência está na tela, pode pausar. Fica o quadrado da razão das massas vezes o momento inicial, sobre um mais a razão.

[thoughtful, emphatic] Olha o que a equação diz: o módulo da diferença entre o vetor que a gente procura e um vetor fixo é igual a um número fixo. Uma distância constante de um ponto fixo... isso é um círculo! O vetor fixo é o centro, e o número fixo é o raio.

[thoughtful] Então vamos desenhar um plano especial, que não é o espaço onde os corpos andam: é o mapa dos momentos finais possíveis do corpo um. O eixo horizontal é a parte do momento na direção original; o vertical, a perpendicular. O centro fica a um sobre um mais a razão do momento inicial; o raio, a razão das massas sobre um mais a razão.

Cada ponto do círculo é um momento final possível para o corpo um. E, para cada ponto, o momento do corpo dois fecha o triângulo. Um ponto só entrega os dois momentos.

[curious] O eixo horizontal corta o círculo em dois pontos. No primeiro, o momento final é igual ao inicial: nada mudou, os corpos nem se tocaram. No segundo, é a colisão frontal, com a fórmula do vídeo passado. O caso de uma dimensão estava escondido nesses dois pontos.

[thoughtful] Agora as direções oblíquas: uma semirreta saindo da origem, com um certo ângulo de saída. Onde ela corta o círculo, existe um momento final possível. Para ângulos pequenos, corta em dois pontos: dois jeitos de bater, o mesmo desvio. Um tira bastante momento do corpo um; o outro é de raspão.

Aumentando o ângulo, os dois pontos se aproximam até virar um só: a tangência. Passou disso, a semirreta não toca o círculo, e sem interseção não existe solução. A natureza fechou a porta.

[curious] Voltando ao disco pesado do começo: as duas tangentes formam um cone. A colisão real, a dez vírgula nove graus, está dentro. Vinte e cinco graus e quarenta graus ficam fora, os dois proibidos. O segurança da porta não deixa passar.

[excited] Era essa a pergunta do começo, e o círculo respondeu: a geometria do momento só deixa passar algumas direções.

[curious] Agora um número: qual é o maior desvio possível? Olha a tangente. O raio até o ponto de tangência é perpendicular a ela. Então temos um triângulo retângulo: a hipotenusa vai da origem ao centro, o cateto oposto é o raio, e o ângulo na origem é o ângulo máximo.

[thoughtful] Seno é cateto oposto sobre hipotenusa: o raio sobre a distância até o centro. Substituindo, quase tudo cancela e sobra só a razão das massas. Então o ângulo máximo é o arco seno da razão das massas: massa do corpo dois sobre a do corpo um. Que coisa linda.

E a álgebra concorda: para a equação do segundo grau ter solução, o discriminante precisa ser maior ou igual a zero, e isso dá exatamente seno do ângulo menor ou igual à razão das massas. Dois caminhos independentes, o mesmo resultado: sinal de que a gente acertou.

Mexendo na razão das massas: alvo mais leve, círculo menor, cone mais fechado. Alvo mais pesado, círculo maior, cone mais aberto.

[thoughtful, emphatic] Agora o caso especial: massas iguais, razão igual a um. O círculo passa pela origem, e o momento inicial vira um diâmetro. Aí entra um velho amigo, de mais de dois mil e quinhentos anos: o teorema de Tales. Pega um diâmetro e qualquer ponto da circunferência, liga às duas pontas... [short pause] e o ângulo é sempre reto.

[excited] As pontas do diâmetro são a origem e a ponta do momento inicial; o ponto é o momento final do corpo um. Os dois lados que chegam nele são os momentos finais dos dois corpos, e portanto perpendiculares. É o ângulo reto da sinuca! Só que agora a gente sabe de onde ele vem. E quando o ponto chega na origem, o corpo um para e o alvo leva tudo: é a troca de velocidades da colisão frontal.

[curious] E se o alvo for mais pesado? A razão passa de um, e o círculo engole a origem: toda semirreta corta o círculo uma vez, em qualquer direção, até cento e oitenta graus. O corpo incidente pode voltar para trás. É a bolinha de pingue-pongue numa bola de boliche.

Um exemplo de física nuclear: uma partícula alfa, com quatro vezes a massa do nêutron, bate num nêutron parado. A razão das massas é um quarto, e o ângulo máximo é o arco seno de um quarto: uns catorze vírgula cinco graus. É um caminhão contra um fusquinha.

[thoughtful] No ponto de tangência, o momento da alfa é raiz de quinze sobre cinco do inicial, uns zero vírgula setenta e sete. Como a energia vai com o quadrado do momento, a alfa fica com sessenta por cento da energia cinética.

[thoughtful, emphatic] Os outros quarenta por cento vão para o nêutron, que sai a uns trinta e sete vírgula oito graus. Mas atenção: isso é no ângulo limite; não é a transferência máxima de energia. Essa acontece de frente, e vale dezesseis vinte e cinco avos: sessenta e quatro por cento.

[curious] Hora de um problema com cara de prova. Um caminhão de três mil quilogramas, indo para o norte a sessenta quilômetros por hora, bate num carro de mil quilogramas, indo para o leste a noventa. Eles ficam presos e derrapam, com coeficiente de atrito cinético zero vírgula cinco. Quer saber a velocidade logo depois do choque e quanto eles derrapam.

[thoughtful] Durante o choque, o momento, que é vetorial, se conserva; a energia cinética não, porque os dois ficam presos. Escreve o momento em duas componentes: para o leste, só o carro tem momento; para o norte, só o caminhão. Cada uma é igual à massa total vezes a componente da velocidade final.

Resolvendo: seis vírgula vinte e cinco metros por segundo para o leste, e doze vírgula cinco para o norte. A tangente do ângulo é dois: sessenta e três vírgula quatro graus a partir do leste. O módulo é quase catorze metros por segundo. O vetor aponta mais para o norte: o caminhão é mais pesado e puxa o conjunto.

E a energia? Quase metade da energia cinética virou lataria amassada e calor.

[thoughtful, emphatic] Agora a colisão acabou, e começou outro processo: a derrapagem. Mudou o processo, muda o princípio: no impacto, momento; depois, trabalho e energia. A energia cinética que sobrou é gasta pelo atrito, e a massa total cancela. A distância é a velocidade ao quadrado, dividida por duas vezes o atrito vezes a gravidade: uns dezenove vírgula cinco metros. Como no pêndulo do vídeo passado: separa os processos.

[curious] Agora, o contrário de uma colisão: uma explosão. O corpo estava parado, com momento total zero; como o impulso externo é desprezível, os três pedaços saem com momentos que somam zero, formando um triângulo fechado. A energia cinética vai de zero para positiva: a energia interna vira cinética, sem criar energia nenhuma.

[thoughtful] O método, em cinco passos. Um: qual é o sistema? Dois: o impulso externo é desprezível? Três: quantas dimensões? Em duas, duas componentes mais a geometria. Quatro: qual é o tipo de evento? Elástica, grudou, explosão ou outro. Cinco: começou outro processo depois? Então separa os processos.

[thoughtful, emphatic] E a pergunta do começo: o que mudou de uma para duas dimensões? A conservação do momento não mudou: ele sempre foi um vetor. Em uma dimensão, a geometria ficava escondida na linha; em duas, ela aparece e decide quais finais são possíveis. Momento mais tipo de colisão virou momento, mais geometria, mais tipo de colisão.

[thoughtful] Até aqui, a gente tratou os corpos como partículas. Isso significa que, para descrever a colisão, bastavam a massa, a velocidade e a direção do movimento. Mas corpos reais têm tamanho.

[curious] Agora imagina duas colisões com o mesmo impulso. Na primeira, o impacto acontece bem no centro do corpo. Nesse caso, o corpo pode simplesmente mudar o seu movimento de translação.

[thoughtful] Na segunda, o impacto acontece deslocado para um dos lados. Aí, além de se mover, o corpo pode começar a girar.

[curious] E aí aparece uma pergunta nova: por que a mesma força pode produzir efeitos completamente diferentes, dependendo de onde ela é aplicada?

[thoughtful] É justamente essa pergunta que leva ao conceito de torque. No próximo vídeo, a gente vai entender por que uma força faz um corpo girar, e como o ponto de aplicação muda completamente o resultado.

[calm, satisfied] Hoje a gente usou momento, geometria e tipo de colisão para descobrir para onde os corpos podem sair, e para onde eles não podem. Se isso ajudou você, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

[happy] E fica a pergunta: por que uma força faz um corpo girar? Me conta nos comentários: o que mais te surpreendeu, o ângulo reto da sinuca ou a direção proibida? Valeu demais por assistir, e até a próxima!
