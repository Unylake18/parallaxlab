# yt_0031 · narração v2 aprovada (Anexo A do handoff v1)

Tags permitidas: [curious], [thoughtful], [surprised], [happy], [excited], [serious]. Uma por parágrafo (o S2 tem duas). Sem [slowly] e sem [pause]. Números por extenso. Leituras: "éle" = L; "eme minúsculo/maiúsculo i j" = m_ij/M_ij; "esse minúsculo/maiúsculo de P" = s(P)/S(P); "cê um" = C¹; "alfa" = α. A linha **Tela** de cada âncora é só referência (o §5 manda).

### H1 · as três perguntas
**Tela:** os três painéis (dois metais, quarto de disco, x² + y² com 16Δ) entram um por pergunta; o ponto laranja troca de metal.
> [curious] Olha esta chapa feita de dois metais. Embaixo, a densidade é de um quilo por metro quadrado. Em cima, três. E, entre os dois, uma linha de solda. Agora divide a chapa em retanguinhos, como no vídeo passado. E os pedaços que cruzam a solda? Se o ponto escolhido cai do lado leve, a densidade é uma. Se cai do lado pesado, é três vezes maior! Será que as somas de Riemann ainda chegam a um único resultado? E lembra do quarto de disco? Quando a grade refinava, a área dos quadradinhos que cruzavam a borda diminuía. Mas isso acontece com qualquer borda? E tem a terceira pergunta: para provar que a massa da chapa do vídeo passado era trinta e dois terços, a gente fez uma conta sob medida, aquele dezesseis vezes o maior lado. Será que precisa inventar uma prova nova para cada função?

### H2 · a ideia do vídeo
**Tela:** os painéis sobem para uma fileira no topo; `O PROBLEMA NÃO É O SALTO` / `É ONDE ELE ACONTECE`.
> [serious] Então a pergunta de hoje é esta: como saber se uma integral dupla existe sem calcular o valor dela? E a resposta é surpreendente. Uma função pode ter descontinuidades e, mesmo assim, ser integrável. O que importa é onde essas descontinuidades acontecem e quanto espaço elas ocupam. E, no caminho, você vai ver por que a chapa de dois metais tem uma massa bem definida, mesmo com a densidade saltando na solda.

### A1 · bem-vindos
**Tela:** logo; `INTEGRAIS DUPLAS`; `NESTE VÍDEO: TAMPAS · CONTEÚDO NULO · TEOREMA`.
> [happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Este é o segundo vídeo do módulo de integrais duplas. No vídeo passado, a gente construiu a integral a partir das somas de Riemann; hoje a pergunta é quando dá para garantir que essas somas convergem. São três passos: medir a diferença entre a soma por cima e a soma por baixo, entender o que é conteúdo nulo e juntar tudo num teorema.

### B1-1 · piso e teto
**Tela:** D1, uma célula da chapa x² + y² e a barrinha dos valores; `m_ij` azul-claro, `M_ij` coral.
> [thoughtful] Começa pela chapa do vídeo passado. Pega um retanguinho da grade, o erre i j. Dentro dele, a função assume vários valores. Agora procura o maior número que fica abaixo de todos esses valores: esse é o piso da célula, eme minúsculo i j. O teto é o contrário: o menor número que fica acima de todos, eme maiúsculo i j. Na matemática, esses números se chamam ínfimo e supremo. Nos exemplos de hoje, eles são o menor e o maior valor de verdade. Mas nem toda função chega a atingir esses extremos, e por isso o nome certo é ínfimo e supremo. E a gente trabalha com funções limitadas, para que o piso e o teto existam.

### B1-2 · as duas somas
**Tela:** D2 e D3, o prédio por baixo e por cima; `s(P) ≤ ΣΣ f(X_ij)Δx_iΔy_j ≤ S(P)`.
> [curious] Multiplica o piso pela área da célula e soma em todas as células da grade: essa é a soma por baixo, esse minúsculo de P. Faz o mesmo com o teto e você tem a soma por cima, esse maiúsculo de P. E repara: qualquer ponto que você escolhe dentro de uma célula dá um valor entre o piso e o teto. Então qualquer soma de Riemann fica entre a soma por baixo e a soma por cima. Lê-se: esse minúsculo de P é menor ou igual à soma de Riemann, que é menor ou igual a esse maiúsculo de P. Todas as aproximações possíveis ficam presas entre duas paredes.

### B1-3 · o volume das tampas
**Tela:** D4, o prédio azul afunda e sobram as tampas; `S(P) − s(P) = ΣΣ (M_ij − m_ij) Δx_iΔy_j`; `OSCILAÇÃO` sob M_ij − m_ij.
> [thoughtful] Agora subtrai as duas somas. Em cada retanguinho sobra o teto menos o piso, vezes a área da base. Essa diferença entre teto e piso tem nome: a oscilação da função na célula. E olha no desenho: tirando o prédio azul, o de baixo, o que sobra do prédio de cima são as tampas coral. Cada tampa tem a altura do teto menos o piso. Então esse maiúsculo menos esse minúsculo de P é exatamente o volume de todas as tampas juntas. Guarda essa imagem, porque ela vai conduzir a demonstração inteira.

### B1-4 · quando as tampas somem
**Tela:** D5, as duas paredes; `∀ε > 0 ∃δ > 0 : Δ < δ ⇒ S(P) − s(P) < ε` → `f INTEGRÁVEL`.
> [serious] E aqui está o critério da aula. Se a diferença entre a soma por cima e a soma por baixo pode ficar tão pequena quanto se queira, só deixando a grade fina o bastante, então a função é integrável. Em épsilon e delta: para todo épsilon maior que zero, existe delta maior que zero tal que, se o maior lado da partição for menor que delta, a diferença entre as duas somas é menor que épsilon. Por que isso funciona? Porque toda soma de Riemann está presa entre as duas paredes. Quando as paredes se fecham num mesmo número, todas as escolhas são obrigadas a chegar nele também. Então, para provar que uma integral dupla existe, a gente persegue uma coisa só: fazer o volume das tampas sumir.

### B2-1 · onde estão as tampas?
**Tela:** a chapa com a solda, ρ₁ = 1 e ρ₂ = 3; uma célula do metal leve, uma do pesado, as células cruzadas em vermelho; o muro coral no 3D.
> [curious] Agora volta na chapa de dois metais. Embaixo da solda, um quilo por metro quadrado; em cima, três. É mais ou menos a diferença entre uma chapa de alumínio e uma de aço com a mesma espessura. Coloca uma grade. Numa célula inteira no metal leve, a densidade vale um em todo ponto: o piso é um, o teto é um, e a tampa tem altura zero. No metal pesado, o mesmo, com três. Mas, nas células atravessadas pela solda, aparecem as duas densidades: o piso é um e o teto é três. Tampa de altura dois, o tamanho do salto. E, juntas, essas tampas formam um muro coral em cima da solda.

### B2-2 · o muro vai sumindo
**Tela:** a grade refina 4 → 64; tabela n · células · por baixo · por cima · diferença; régua da massa apertando em 7,06.
> [thoughtful] Então a diferença entre as duas somas é o salto, dois, vezes a área das células que a solda atravessa. Refina a grade. Com quatro divisões por lado, cinco células cruzam a solda; a soma por baixo dá seis quilos e a por cima, oito e meio. Diferença de dois e meio. Com oito divisões, a diferença cai para um vírgula trinta e oito. Com dezesseis, setenta e cinco centésimos. Com trinta e duas, trinta e sete centésimos. Com sessenta e quatro, dezenove centésimos. As duas somas apertam em torno de sete vírgula zero seis quilos. E repara: o salto continua exatamente o mesmo. O que diminui é a área das células que atravessam a solda.

### B2-3 · a pergunta certa
**Tela:** só a solda branca; `A SOLDA CABE EM ÁREA PEQUENA?`.
> [curious] Então a descoberta é esta: o problema não era a densidade saltar. O problema era quanto espaço os pontos de descontinuidade ocupam. Se a região problemática pode ser coberta por retângulos de área total tão pequena quanto se queira, dá para controlar a contribuição dela na diferença entre as somas. E essa propriedade tem um nome: conteúdo nulo.

### B3-1 · a definição
**Tela:** a definição escrita a caneta em três linhas; sublinhados no ∪ e no m(A_i).
> [thoughtful] Monta a definição com a própria solda. A ideia é cobrir a linha inteira com retângulos, quantos você quiser, desde que seja um número finito. E a condição é: a soma das áreas tem que poder ficar menor que qualquer número positivo escolhido, o épsilon. Então a definição diz: um conjunto D tem conteúdo nulo se, para todo épsilon maior que zero, existe um número finito de retângulos, a um até a ene, tais que D está contido na união deles e a soma das áreas é menor que épsilon. Esse U grande é a união dos conjuntos. E eme de a i é a área do retângulo a i. Ou seja: cobrir o conjunto inteiro gastando menos área do que a tolerância permite.

### B3-2 · um orçamento de área
**Tela:** D6, a barra do orçamento; coberturas com 4, 16 e 64 retângulos.
> [curious] Pensa no épsilon como um orçamento. Alguém diz: você pode gastar no máximo um metro quadrado de cobertura. Quatro retângulos em volta da solda gastam quarenta e seis centésimos. Deu. Agora o orçamento cai para um quarto de metro quadrado. Tudo bem: dezesseis retângulos mais finos gastam doze centésimos. E se cair para cinco centésimos? Sessenta e quatro retângulos gastam três. Mas cuidado: três exemplos não demonstram nada. O que a definição pede é que funcione para qualquer orçamento positivo, por menor que seja. Isso é ter conteúdo nulo.

### B3-3 · o que tem e o que não tem
**Tela:** D7, quatro miniaturas; a barra estoura no disco cheio.
> [thoughtful] Alguns exemplos. Um ponto tem conteúdo nulo: basta um quadradinho em volta dele, tão pequeno quanto o orçamento pedir. Um número finito de pontos também: um quadradinho para cada um. Um segmento de reta: um retângulo comprido e cada vez mais fino. E daí saem duas regras úteis. Um pedaço de um conjunto de conteúdo nulo também tem conteúdo nulo, e juntar um número finito desses conjuntos continua dando conteúdo nulo. Agora, um disco cheio não tem. Para cobri-lo, os retângulos gastam pelo menos a área do disco, e um orçamento menor que isso nunca dá conta. Então a ideia não é o conjunto parecer fino no desenho. É dar para cobri-lo com área tão pequena quanto se queira.

### B4-1 · a parábola
**Tela:** D8 na parábola; as caixas se empilham numa coluna Δ × 4; 2 · 1 · 0,5.
> [curious] E uma curva inteira? Lembra da parábola do vídeo passado, xis ao quadrado? Divide o eixo em pedaços e, em cada pedaço, desenha uma caixa que vai do menor ao maior valor da curva ali. Juntas, as caixas cobrem a parábola. Agora o truque: a curva é crescente, então dá para empurrar as caixas para a direita e empilhar. Todas cabem numa coluna com a largura do maior lado e altura quatro, a subida total da parábola. Área total: no máximo quatro vezes o maior lado. Com quatro pedaços, dois; com oito, um; com dezesseis, meio. E refinando, fica tão pequena quanto se queira. O gráfico da parábola tem conteúdo nulo.

### B4-2 · a solda e o arco
**Tela:** D8 na solda (duas colunas) e no arco (uma coluna de altura 2); 1 · 0,5 · 0,25 · 0,125.
> [thoughtful] A solda não cresce o tempo todo: primeiro sobe, depois desce. Então separa os dois movimentos. As caixas da subida se empilham numa coluna de cinquenta e oito centésimos de altura, e as da descida numa de trinta e seis. Área total: no máximo noventa e quatro centésimos vezes o maior lado, que vai a zero junto com o maior lado. O arco do quarto de disco desce de dois até zero, então as caixas dele somam duas vezes o maior lado. Com quatro divisões, um metro quadrado; com oito, meio; com dezesseis, um quarto; com trinta e duas, um oitavo.

### B4-3 · o resultado geral
**Tela:** `f CONTÍNUA EM [a, b] ⇒ GRÁFICO DE f TEM CONTEÚDO NULO`; ícones de polígono, círculo e elipse com ✓.
> [serious] E dá para ir além dos exemplos: o gráfico de qualquer função contínua num intervalo fechado tem conteúdo nulo. Por quê? A área das caixas que cobrem o gráfico é exatamente a diferença entre a soma por cima e a soma por baixo da integral simples. E toda função contínua num intervalo fechado é integrável, então essa diferença vai a zero. O livro vai além: toda curva de classe cê um, ou seja, com uma parametrização de derivada contínua, também tem conteúdo nulo. E o mesmo vale para curvas feitas de um número finito desses pedaços: segmentos, polígonos, círculos, elipses e quase toda borda que aparece num problema. Para essas bordas, a primeira pergunta tem resposta: sim, a área some. Mas isso não quer dizer que qualquer fronteira imaginável tenha essa propriedade.

### B5-1 · interior, exterior e fronteira
**Tela:** D9, as três sondas no quarto de disco.
> [thoughtful] Agora a borda de uma região ganha nome matemático. Pega um ponto e desenha em volta dele uma bola aberta: um disquinho sem a circunferência da borda. Se dá para escolher uma bola inteira dentro da região B, o ponto é interior. Se dá para escolher uma inteira fora, é exterior. Mas existem pontos em que nenhuma das duas coisas acontece: não importa o quanto a bola encolhe, ela sempre pega pontos de B e pontos de fora. Esses são os pontos de fronteira. No quarto de disco, a fronteira é o arco e os dois segmentos sobre os eixos. E um detalhe: um ponto de fronteira pode pertencer à região ou não.

### B5-2 · a borda é uma solda
**Tela:** D10 em Three.js; `BORDA = SOLDA ENTRE f E 0`.
> [excited] E aqui as duas primeiras perguntas se encontram. Lembra como se integra numa região que não é retangular? Coloca a região dentro de um retângulo maior e faz a função valer zero fora dela. No quarto de disco, a função vale um dentro e zero fora. E o que acontece quando você atravessa a borda? A função salta de um para zero! A borda funciona exatamente como a solda da chapa de dois metais. Olha o prédio: as tampas só aparecem nos retângulos atravessados pela fronteira. E, se a fronteira tem conteúdo nulo, a área dessas células pode ficar tão pequena quanto se queira. Uma borda curva e uma linha de solda eram o mesmo problema.

### B6-1 · um delta para a chapa inteira
**Tela:** a chapa x² + y² com tampas em todas as células; `E ONDE f É CONTÍNUA?`.
> [curious] Só que falta uma peça. Na chapa de dois metais, longe da solda, a densidade era constante, e as tampas eram zero. Mas numa densidade que varia, como xis ao quadrado mais ípsilon ao quadrado, quase toda célula tem o piso diferente do teto. Então não basta cuidar de onde a função salta: onde ela é contínua, as tampas também têm que poder ficar pequenas. E aí aparece um detalhe. Ser contínua quer dizer que, perto de cada ponto, a função muda pouco. Mas dá para escolher uma única distância que sirva para todos os pontos da chapa ao mesmo tempo?

### B6-2 · continuidade uniforme
**Tela:** D11, a régua de dois pontos; o enunciado escrito a caneta; `ε = 1 → δ = 0,17`.
> [thoughtful] Dá, quando a região é fechada e limitada e a função é contínua nela: é o teorema de Heine-Cantor. Para todo épsilon maior que zero, existe delta maior que zero tal que quaisquer dois pontos da região, xis e ípsilon maiúsculos, a menos de delta um do outro, têm valores que diferem menos que épsilon. As barras duplas lê-se norma: a distância entre os dois pontos. O mesmo delta serve para todos os pares, e por isso se chama continuidade uniforme. Na chapa de densidade xis ao quadrado mais ípsilon ao quadrado, o canto de cima é o mais exigente, porque a função muda mais rápido ali. Com épsilon igual a um, um delta de dezessete centésimos serve na chapa inteira. É esse delta que controla, ao mesmo tempo, a oscilação de todas as células pequenas.

### B6-3 · por que fechado e limitado?
**Tela:** D12, sen(1/x) na chapa sem a borda esquerda; a régua encolhe e a diferença continua 2.
> [curious] E por que a região precisa ser fechada e limitada? Olha esta função: seno de um sobre xis, numa faixa sem a borda onde xis vale zero. Perto dessa borda que falta, ela oscila cada vez mais rápido. Dá para achar dois pontos tão próximos quanto você quiser, um onde o seno vale um e outro onde vale menos um. A diferença continua dois, e nenhum delta serve para a faixa inteira. Numa região fechada e limitada, isso não acontece. Se a continuidade uniforme falhasse, haveria pares de pontos cada vez mais próximos com valores sempre longe um do outro. Só que, numa região fechada e limitada, esses pares se aproximam de um mesmo ponto da própria região. E ali a função seria descontínua. Contradição.

### B7-1 · separando os pontos problemáticos
**Tela:** D13, etapas 1 a 3: cobertura de D (< ε₁), engorda (< 2ε₁), grade fina; zoom na célula que encosta na cobertura (§2, item 3).
> [serious] Agora a demonstração principal, juntando tudo. Pega uma função limitada num retângulo: existe um número eme maiúsculo que limita o módulo dos valores dela. E chama de D o conjunto dos pontos onde ela não é contínua, com conteúdo nulo. O objetivo é provar que ela é integrável. Primeiro, cobre D com um número finito de retângulos, gastando área total menor que épsilon um. Depois, engorda um pouquinho esses retângulos, sem passar de duas vezes épsilon um. Por que engordar? É uma margem de segurança: toda célula pequena da grade que encosta na cobertura original fica inteira dentro da cobertura engordada. Fora da cobertura, sobra uma região fechada onde a função é contínua, então a continuidade uniforme controla a função ali. Agora escolhe uma grade fina o bastante para respeitar as duas coisas: a margem e o delta da continuidade uniforme.

### B7-2 · dois grupos de tampas
**Tela:** D13, etapas 4 e 5: calmas e vermelhas, as duas cotas; `S(P) − s(P) < αε₂ + 4Mε₁`; `αε₂ < ε/2` e `4Mε₁ < ε/2` (§2, item 4).
> [thoughtful] As células da grade se dividem em dois grupos. O primeiro é o das células calmas, longe dos pontos problemáticos. Nelas, a continuidade uniforme garante que o teto e o piso estão muito próximos: cada tampa tem altura menor que épsilon dois. E a área total delas não passa da área do retângulo, que a gente chama de alfa. Contribuição: menos que alfa vezes épsilon dois. O segundo grupo é o das células vermelhas, perto das descontinuidades. Ali a função pode variar bastante, mas o módulo dela nunca passa de eme, então a tampa nunca passa de dois eme. E essas células cabem na cobertura engordada, de área menor que dois épsilon um. Contribuição: menos que quatro eme épsilon um. Somando os dois grupos, esse maiúsculo menos esse minúsculo de P é menor que alfa épsilon dois mais quatro eme épsilon um. Agora escolhe os dois épsilons para que cada parcela fique menor que metade da tolerância. Com épsilon dois igual a épsilon sobre dois alfa, o alfa cancela, e sobra épsilon sobre dois. Com épsilon um igual a épsilon sobre oito eme, o eme cancela, o quatro com o oito vira um meio, e sobra épsilon sobre dois de novo. Meio épsilon mais meio épsilon: a diferença fica menor que épsilon. As tampas somem! E, pelo critério do começo da aula, a função é integrável.

### B7-3 · o teorema
**Tela:** `TEOREMA 1`, o corolário (D = ∅), `TEOREMA 2` e a observação, em caixas de contorno fino.
> [excited] E esse é o teorema: se uma função é limitada num retângulo e o conjunto dos pontos onde ela é descontínua tem conteúdo nulo, então ela é integrável. Repara na força disso. Não precisa calcular o valor da integral nem testar mil grades: basta verificar duas propriedades da função. E sai uma consequência imediata. Se a função é contínua no retângulo inteiro, o conjunto das descontinuidades é vazio, e o vazio tem conteúdo nulo. Então toda função contínua num retângulo é integrável. Dá para ir além: numa região limitada com fronteira de conteúdo nulo, estende a função por zero. Se ela é contínua e limitada na região, a extensão só pode ser descontínua na fronteira, e o teorema garante a integral. E o livro ainda observa: pode ter descontinuidades dentro da região também, desde que fiquem num conjunto de conteúdo nulo.

### B7-4 · as três respostas
**Tela:** a fileira dos três painéis do hook volta e ganha os ✓; régua com 7,06.
> [happy] Agora volta nas três perguntas. O quarto de disco: a fronteira é um arco e dois segmentos, todos com conteúdo nulo. Então a função que vale um dentro e zero fora é integrável, e a área existe: é pi. A chapa de dois metais: a densidade fica entre um e três e só é descontínua na solda, que é o gráfico de uma função contínua e tem conteúdo nulo. A massa está bem definida: sete vírgula zero seis quilos, mais ou menos. E a chapa de densidade xis ao quadrado mais ípsilon ao quadrado: a função é contínua no retângulo inteiro, então é integrável, sem refazer a conta do dezesseis delta. Três problemas diferentes, um teorema só.

### B8-1 · a função de Dirichlet
**Tela:** D15, a célula com duas cores e o zoom que não muda; `POR CIMA = 4`, `POR BAIXO = 0`.
> [surprised] Mas toda função limitada é integrável? Não. Olha esta função estranha: vale um quando as duas coordenadas do ponto são números racionais, aqueles que se escrevem como fração de inteiros, e vale zero nos outros casos. Pega qualquer retanguinho da grade. Por menor que seja, ele tem pontos com as duas coordenadas racionais e pontos com pelo menos uma coordenada irracional. Então, em todas as células, o piso é zero e o teto é um. A soma por cima dá sempre quatro, a área do quadrado, e a soma por baixo dá sempre zero. Refina quanto quiser: a diferença continua quatro. As paredes nunca se aproximam, e essa função não é integrável no sentido de Riemann.

### B8-2 · uma fronteira que não some
**Tela:** o conjunto dos pontos racionais (pontilhado) e a fronteira = o quadrado todo; `CONDIÇÃO SUFICIENTE`.
> [thoughtful] E isso responde à última dúvida do vídeo passado: existem bordas que não somem? Existem. Pega o conjunto dos pontos do quadrado com as duas coordenadas racionais. Qualquer disquinho dentro do quadrado encontra pontos dele e pontos de fora. Então a fronteira dele é o quadrado inteiro: não é uma curva, é uma região de área positiva, e não tem conteúdo nulo. Um último cuidado: o teorema dá uma condição suficiente. Quando as hipóteses valem, a integral existe com certeza. Quando não valem, isso sozinho não prova que ela não existe. Aqui, a não integrabilidade saiu direto das somas, que nunca se aproximam.

### B9-1 · o teste em três perguntas
**Tela:** D16, quatro cartões e o checklist (LIMITADA? · SALTOS EM CONTEÚDO NULO? · FRONTEIRA EM CONTEÚDO NULO?).
> [curious] Num exercício, o teorema vira três perguntas. A função é limitada? As descontinuidades ficam num conjunto de conteúdo nulo? E a fronteira da região tem conteúdo nulo? Os exemplos do livro passam nas três. Xis mais ípsilon no disco de raio um: contínua, e a fronteira é uma circunferência. Xis mais ípsilon entre as parábolas ípsilon igual a xis ao quadrado e ípsilon igual a um mais xis ao quadrado: a fronteira são dois gráficos e dois segmentos. No disco, a função que vale um acima do eixo xis e menos um abaixo: uma chapa de dois metais com solda reta. E xis ao quadrado sobre xis ao quadrado mais ípsilon ao quadrado, valendo um na origem: só é descontínua na origem, e um ponto tem conteúdo nulo. As quatro são integráveis.

### B9-2 · por que isso importa
**Tela:** três cartões pequenos: `DOIS MATERIAIS` · `DIVISA NO MAPA` · `ALVO REDONDO`.
> [excited] E isso aparece fora dos exercícios: uma peça feita de dois materiais, a densidade de população que muda na divisa entre duas cidades, a probabilidade espalhada por igual dentro de um alvo redondo e zero fora dele. Todas essas funções têm descontinuidades. Mas são limitadas, e as descontinuidades moram em curvas, então a integral existe. O teorema amplia muito o tipo de função que dá para integrar com segurança.

### S1 · síntese
**Tela:** `TAMPAS · CONTEÚDO NULO · CONTINUIDADE UNIFORME`, e o teorema fecha embaixo (§2, item 5); o muro coral na solda.
> [thoughtful] Então olha o caminho. A soma por baixo e a soma por cima prendem todas as aproximações, e a diferença entre elas é o volume das tampas. Onde a função é contínua, a continuidade uniforme achata as tampas todas de uma vez. Onde ela é descontínua, as tampas podem ser altas, mas os pontos problemáticos precisam ficar num conjunto de conteúdo nulo: um conjunto que dá para cobrir com um número finito de retângulos, gastando tão pouca área quanto se queira. Juntando as duas ideias, sai o teorema. Uma integral dupla não exige que tudo seja contínuo: o importante é controlar a diferença entre as aproximações.

### S2 · o próximo vídeo e CTA
**Tela:** cartão `NO PRÓXIMO VÍDEO: PROPRIEDADES DA INTEGRAL DUPLA`; a chapa partida em duas regiões; `A SOLDA PESA ALGUMA COISA?`; depois o CTA padrão.
> [curious] Mas ficou uma pergunta. Na chapa de dois metais, dá para calcular a massa do pedaço leve e a do pesado separadamente. Então a massa total devia ser a soma das duas, certo? Só que os dois pedaços se encontram na solda, que fica na fronteira dos dois. Ela entra duas vezes na conta? E, no nosso modelo, a solda é uma linha sem espessura: ela tem alguma massa? No próximo vídeo, as propriedades da integral dupla: somar funções, tirar constante, comparar integrais, dividir a região em pedaços e entender por que mudar a função num conjunto de conteúdo nulo não muda a integral. [happy] Se essa aula te ajudou, deixa o like, se inscreve no Parallax Lab e conta nos comentários: em que outra situação uma grandeza muda de repente ao atravessar uma fronteira? Até a próxima!
