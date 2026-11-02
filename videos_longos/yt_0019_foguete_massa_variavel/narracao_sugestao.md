# yt_0019 — roteiro com narração v1.2 (aprovada para o handoff)

> v1.2 (2026-10-31): segunda revisão do GPT, aceita. (a) T1-4, T2-1b e T2-7: no carrinho, o que é zero é a **componente horizontal** da velocidade relativa da areia (ela cai com velocidade vertical em relação ao carrinho): u_rel,x = 0 × u_rel,x = −v_ex. (b) T3-1: no fim, o gás empurra a estrutura **e a carga útil**. (c) Física congelada: na decolagem tardia, m₀ das fórmulas de subida é a massa no instante da decolagem. Aprovada para o handoff v1.

Fonte: Anexo A do handoff v1 (2026-10-31). Título: **Por que um foguete é quase todo combustível?** Física I · Momento e colisões · 4.9.
Cada `###` é uma âncora; a linha `tela:` não é fala; tags `[ ]` não entram na legenda.

## HOOK

### H1 — tela: Three.js, foguete de dois estágios de aço com luz B na rampa, piso com grade ciano, céu do laboratório; câmera sobe devagar da base até a cápsula no topo
[curious] Olha esse foguete na rampa. Dezenas de metros de altura... e quase tudo isso é tanque.

### H2 — tela: o casco fica translúcido em corte: os tanques acendem; ao lado, uma barra vertical de massa se enche: PROPELENTE ~89% em baixo, ESTRUTURA ~9% no meio, CARGA ÚTIL ~2% no topo (a cápsula pisca pequena); selo pequeno ORDEM DE GRANDEZA
[thoughtful] Se você colocar tudo na balança, perto de nove décimos da massa é propelente: o combustível mais o oxidante que ele queima. A carga que de fato vai para a órbita, o satélite ou a cápsula, é uma fatia de poucos por cento, lá no topo.

### H3 — tela: duas barras "propelente" lado a lado, a segunda com o dobro; ao lado de cada uma, uma seta violeta de velocidade final: a segunda cresce bem menos que o dobro; pergunta POR QUE UM FOGUETE É QUASE TODO COMBUSTÍVEL?, acima da cena
[curious] E aí vem a pergunta. Se precisa ir mais rápido, por que não é só dobrar o combustível? Porque dobrar o combustível não dobra a velocidade, nem de longe. E para entender por quê, a gente precisa responder outra coisa antes: como um foguete acelera no espaço, se lá não tem nada para ele empurrar?

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: POR QUE UM FOGUETE É QUASE TODO COMBUSTÍVEL?; abaixo, NESTE VÍDEO: e três ícones com rótulo
[thoughtful] Hoje o assunto é o foguete: um corpo que perde massa enquanto anda. Primeiro, de onde vem a força que empurra o foguete. Depois, quanta velocidade cada quilo de combustível compra, e aí aparece um logaritmo que manda no projeto de qualquer foguete. E no fim, por que os foguetes que vão para a órbita quase sempre são feitos em estágios.

### A3 — tela: patinadores de aço se empurram; setas magenta iguais e opostas; ⊕ parado; CONTA: ΣF⃗_ext = dP⃗/dt → F⃗_ext = 0 ⇒ P⃗ CONSTANTE
Lembrando a base de tudo: para um sistema de partículas, a força externa resultante é a taxa de variação do momento total. Sem força externa, o momento total não muda. Dois patinadores parados que se empurram saem com momentos iguais e opostos, e o centro de massa dos dois fica onde estava. Guarda essa cena, porque o foguete é exatamente isso, só que com um dos patinadores virando gás.

## T1 — QUANDO A MASSA MUDA, O QUE VALE?

### T1-1 — tela: carrinho com caçamba de areia no trilho, seta v; furo; SEM ATRITO
[curious] Começa com uma situação mais simples que o foguete. Um carrinho anda num trilho sem atrito, carregado de areia. No fundo da caçamba tem um furo, e a areia vai vazando. Pergunta: o carrinho acelera?

### T1-2 — tela: CONTA p = m v → F = d(mv)/dt = m dv/dt + v dm/dt → F = 0 → dv/dt = −(v/m) dm/dt; fantasma acelera
[thoughtful] Uma tentação é pegar a segunda lei na forma de momento, força igual à derivada de massa vezes velocidade, e derivar o produto: massa vezes a derivada da velocidade, mais velocidade vezes a derivada da massa. Não tem força horizontal, então isso dá zero. E aí sairia que a derivada da velocidade é menos a velocidade dividida pela massa, vezes a taxa com que a massa muda. Como a massa está diminuindo, essa taxa é negativa, e a aceleração dá positiva. Ou seja, o carrinho aceleraria só por perder areia.

### T1-3 — tela: grãos com a mesma velocidade horizontal, em parábola sob o carrinho; fantasma NÃO; última linha riscada
[curious] Só que isso não acontece. Olha os grãos: cada um sai do furo com a mesma velocidade horizontal do carrinho. Ninguém empurra ninguém. O grão cai em parábola, sempre embaixo do carrinho, e o carrinho segue com a mesma velocidade. A conta estava errada.

### T1-4 — tela: contorno SISTEMA (carrinho + grãos); ΣF⃗_ext = dP⃗/dt SÓ PARA SISTEMA FECHADO; P_x CONSTANTE
[thoughtful, emphatic] E o erro está na escolha do sistema. A lei "força externa igual à derivada do momento" vale para um sistema fechado, que é sempre feito da mesma matéria. O carrinho sozinho não é um sistema fechado: ele perde pedaço o tempo todo. Então a gente inclui na conta a areia que já saiu. Carrinho mais areia: aí sim, sem força externa horizontal, o momento horizontal total fica constante. E como cada grão sai com a velocidade horizontal do carrinho, o carrinho não precisa mudar a sua.

### T1-5 — tela: DICA: MASSA VARIÁVEL: ESCOLHA O SISTEMA QUE INCLUI O QUE SAI
Essa é a dica do vídeo inteiro. Em problema de massa variável, não existe uma lei nova. Existe escolha de sistema: você sempre inclui o que entra ou o que sai.

## T2 — DE ONDE VEM O EMPUXO?

### T2-1 — tela: Three.js, foguete no espaço, motor aceso, jato de partículas claras
[curious] Agora sim, o foguete. Ele está no espaço, longe de tudo, sem força externa nenhuma. E não tem ar, nem chão, nem nada atrás dele para empurrar. Então de onde vem a força?

### T2-1b — tela: carrinho (u_rel,x = 0) e foguete (u_rel,x = −v_ex) lado a lado; hold ~2 s
[thoughtful] Olha os dois lado a lado. O carrinho perde massa, e o foguete também. A diferença está numa coisa só: com que velocidade, em relação ao corpo, a massa sai. No carrinho, a areia sai sem velocidade horizontal em relação a ele, e ninguém empurra ninguém na horizontal. No foguete, o gás é jogado para trás com força. Então já dá para apostar: se o foguete empurra o gás para trás, o gás empurra o foguete para a frente. Vamos ver isso na conta.

### T2-2 — tela: INSTANTE t: foguete m, v; SISTEMA; HIPÓTESES: v_ex CONSTANTE · SEM A PARCELA DE PRESSÃO NO BOCAL
[thoughtful] Vamos escolher bem o sistema, como no carrinho. Num instante qualquer, o foguete tem uma massa e uma velocidade. Esse é o nosso sistema: o foguete com todo o propelente que ainda está dentro dele. E duas hipóteses do modelo: o gás sai sempre com a mesma velocidade em relação ao foguete, e a gente despreza a contribuição da diferença de pressão na saída do bocal.

### T2-3 — tela: INSTANTE t + dt: m + dm, v + dv; nuvem −dm; v_ex; v − v_ex; SISTEMA envolve foguete e nuvem
Um instante depois, o motor jogou para trás um pouquinho de gás. Aqui tem um detalhe de sinal. A variação da massa do foguete, que na tela aparece como dm, é negativa, porque ele perdeu massa. Então o foguete agora tem massa m mais dm, que é menor, e a velocidade aumentou um pouquinho. E o gás tem massa menos dm, que é positiva. Esse gás sai com uma velocidade bem definida em relação ao foguete: a velocidade de exaustão, que na tela aparece como v com índice ex. Para quem olha de fora, a velocidade do gás é a velocidade do foguete menos a velocidade de exaustão.

### T2-4 — tela: m v = (m + dm)(v + dv) + (−dm)(v − v_ex) → cancelamentos → m dv = −v_ex dm
[thoughtful] Sem força externa, o momento desse sistema antes é igual ao momento depois. Antes: massa vezes velocidade. Depois: o foguete, massa mais dm vezes velocidade mais dv, somado com o gás, menos dm vezes a velocidade dele. Abrindo os parênteses, a massa vezes a velocidade aparece dos dois lados e cancela. Os termos com velocidade vezes dm também se cancelam. Sobra um termo dm vezes dv, que é o produto de duas coisas minúsculas, muito menor que o resto, e some no limite... [short pause] E fica isso: a massa vezes a variação da velocidade é igual a menos a velocidade de exaustão vezes a variação da massa.

### T2-5 — tela: ÷ dt → F_emp = v_ex |dm/dt|; seta do empuxo; unidades
[thoughtful, emphatic] Divide tudo pelo intervalo de tempo. Do lado esquerdo, massa vezes aceleração. Do lado direito, a velocidade de exaustão vezes a taxa com que o foguete perde massa, a vazão, que fica positiva porque o sinal de menos já cuidou disso. Esse lado direito faz o papel de uma força. É o empuxo: velocidade de exaustão vezes a vazão de massa. E as unidades fecham: metros por segundo vezes quilogramas por segundo dá quilograma metro por segundo ao quadrado, que é newton.

### T2-6 — tela: Three.js: foguete parte do repouso; nuvem para a esquerda; ⊕ FOGUETE + GÁS parado; câmera recua
[curious] E repara no que isso quer dizer. O foguete não empurra o espaço nem o ar. Ele empurra o próprio gás para trás, e o gás empurra o foguete para a frente: ação e reação, força interna do sistema. É a cena dos patinadores de novo. Se o foguete começou parado, o centro de massa do foguete mais todo o gás que já saiu continua parado, enquanto o foguete dispara para um lado e a nuvem se espalha para o outro.

### T2-7 — tela: m dv⃗/dt = ΣF⃗_ext + u⃗_rel dm/dt; foguete e carrinho
[thoughtful] Dá para escrever isso de um jeito que vale para qualquer corpo que ganha ou perde massa. Massa vezes aceleração é igual à força externa mais a velocidade relativa da massa que entra ou sai, vezes a taxa de variação da massa. No foguete, a velocidade relativa é a de exaustão, para trás, e aparece o empuxo. No carrinho, a areia sai sem velocidade horizontal em relação a ele, então, na horizontal, o termo some: por isso ele não acelera. Uma equação, os dois casos.

## T3 — QUANTA VELOCIDADE O COMBUSTÍVEL COMPRA?

### T3-1 — tela: barra de massa; dv = −v_ex dm/m → integral → Δv = v_ex ln(m₀/m_f); inset do mesmo quilo de gás
[curious] Agora a pergunta que interessa para o começo do vídeo: quanta velocidade o foguete ganha queimando todo o propelente? Volta na equação: massa vezes dv igual a menos a velocidade de exaustão vezes dm. Passa a massa para o outro lado: a variação da velocidade é menos a velocidade de exaustão vezes dm dividido pela massa. Repara no que isso diz: o ganho com um quilo de gás depende da massa do foguete naquele momento. No começo, esse quilo empurra o foguete inteiro, cheio, e rende pouco. No fim, empurra só a estrutura e a carga útil, e rende muito. É essa massa no denominador que pede a integral, e é dela que vai sair o logaritmo. Então integra, da massa inicial até a massa final. A integral de dm sobre a massa é o logaritmo natural. E o sinal de menos inverte a fração.

### T3-2 — tela: PANEL Δv = v_ex ln(m₀/m_f); EQUAÇÃO DE TSIOLKOVSKY; R = RAZÃO DE MASSAS
[thoughtful, emphatic] E chegamos à equação do foguete, a equação de Tsiolkovsky: o ganho de velocidade é a velocidade de exaustão vezes o logaritmo da razão entre a massa inicial e a massa final. Essa razão tem nome: razão de massas.

### T3-3 — tela: CONFERE: R = 1 → Δv = 0; v_ex → 0 → Δv → 0
Confere: se o foguete não queima nada, a massa final é igual à inicial, o logaritmo de um é zero, e ele não ganha velocidade. E se o gás sai cada vez mais devagar, o ganho também vai a zero. Faz sentido.

### T3-4 — tela: v × t de dois foguetes (10 s e 10 min), mesmo Δv; NO ESPAÇO, A VAZÃO NÃO MUDA O Δv
[curious] E repara no que não está na fórmula: a vazão. Um foguete que queima tudo em dez segundos e outro que queima em dez minutos, com a mesma velocidade de exaustão e a mesma razão de massas, chegam na mesma velocidade final. No espaço, a pressa não muda o resultado; só muda quanto tempo ele leva para chegar lá.

### T3-5 — tela: Δv/v_ex × R; marcas em e, e², e³; setas ×e
[thoughtful] Agora o gráfico do ganho de velocidade, medido em velocidades de exaustão, contra a razão de massas. A curva é um logaritmo, e ela deita rápido. Para ganhar uma velocidade de exaustão, a razão de massas é o número e, uns dois vírgula sete. Para ganhar duas, a razão não dobra: vai a e ao quadrado, uns sete vírgula quatro. Para três, e ao cubo, uns vinte. Cada degrau a mais de velocidade multiplica a razão de massas por dois vírgula sete. É por isso que dobrar o combustível nunca dobra a velocidade.

### T3-6 — tela: v_ex ≈ 3,0 km/s; v_órbita ≈ 7,8 km/s; ORÇAMENTO 9 km/s; R = e³ ≈ 20; barra 95% / 5%
[curious] Vamos colocar números. Um bom motor químico joga o gás a uns três quilômetros por segundo. Para ficar em órbita baixa, a velocidade é de uns sete vírgula oito quilômetros por segundo. Só que no caminho a gravidade e o ar ainda cobram a parte deles, então a gente adota um orçamento de nove quilômetros por segundo de ganho de velocidade. Nove dividido por três dá três velocidades de exaustão. Então a razão de massas é e ao cubo, uns vinte... [short pause] Ou seja, no fim da queima sobra um vigésimo da massa. Noventa e cinco por cento do foguete tem que ser propelente. Aí está a primeira metade da resposta.

### T3-7 — tela: Three.js: foguete do repouso; medidor v/v_ex; partículas por sentido; 63% QUEIMADO · v = v_ex
[thoughtful] E tem uma consequência estranha. Se o foguete partiu do repouso, sem gravidade, quando a razão de massas passa de e, ou seja, depois de queimar sessenta e três por cento da massa inicial, o ganho de velocidade passa da própria velocidade de exaustão. O foguete fica mais rápido que o gás que ele cospe.

### T3-8 — tela: partículas novas brancas para a frente; v_ex continua para trás; hold 2–3 s
[curious] E aí, no referencial em que o foguete começou parado, o gás recém-expelido não vai mais para trás. Ele anda para a frente, só que mais devagar que o foguete. E mesmo assim empurra. Porque o que importa para o empuxo é a velocidade do gás em relação ao foguete, e essa continua sendo a velocidade de exaustão, para trás. Visto do foguete, esse gás continua sendo lançado para trás.

## T4 — E A GRAVIDADE?

### T4-1 — tela: Three.js rampa; empuxo e peso; HIPÓTESES: SUBIDA VERTICAL · g CONSTANTE · SEM AR
[curious] Até aqui, o foguete estava no espaço. Na rampa, tem uma força externa que não dá para ignorar: o peso. Vamos supor subida vertical, gravidade constante e sem resistência do ar.

### T4-2 — tela: m dv/dt = v_ex |dm/dt| − m g; DECOLA NA LARGADA SE v_ex |dm/dt| > m₀ g; SENÃO, ESPERA NA RAMPA
[thoughtful] A equação ganha um termo: massa vezes aceleração é igual ao empuxo menos o peso. E já sai a primeira condição: para sair do chão logo na largada, o empuxo tem que ser maior que o peso inicial. Se não for, o foguete fica apoiado na rampa, queimando propelente, até a massa cair o bastante para o empuxo vencer o peso. E daqui para a frente as contas valem depois que ele sai do chão, quando a plataforma já não empurra mais.

### T4-3 — tela: Δv = v_ex ln(m₀/m_f) − g t_q; PERDA POR GRAVIDADE; v × t curta × longa
Integrando de novo, contando a queima a partir da decolagem e para qualquer jeito de queimar, o resultado é o mesmo logaritmo, menos a aceleração da gravidade vezes o tempo de queima. Esse último termo é a perda por gravidade: durante todo o tempo em que o motor funciona, a gravidade vai tirando velocidade. E agora a vazão importa, sim. Queimar mais rápido deixa menos tempo para a gravidade cobrar.

### T4-4 — tela: a = v_ex |dm/dt| / m − g; gráfico a × t
[thoughtful] E olha a aceleração. O empuxo fica constante, mas a massa vai caindo. Então a aceleração cresce durante toda a queima, e cresce muito no final, quando o tanque está quase vazio.

## E1 — DECOLAGEM

### E1-1 — tela: ESQUEMA foguete na rampa; dados; O QUE ESTE PEDE: EMPUXO CONTRA PESO; HIPÓTESES
[curious] Primeiro exercício. Um foguete de vinte toneladas, das quais dezesseis são propelente, sobe na vertical. O gás sai a dois mil e quinhentos metros por segundo, e o motor queima cento e vinte quilos por segundo. Gravidade constante e sem resistência do ar. Ele decola? Com que aceleração? E com que velocidade termina a queima?

### E1-2 — tela: F_emp = 300.000 N; P = 196.000 N; DECOLA; a₀ = 5,2 m/s²
[thoughtful] Primeiro, empuxo contra peso. Empuxo: velocidade de exaustão vezes vazão, dois mil e quinhentos vezes cento e vinte, trezentos mil newtons. Peso: vinte mil quilos vezes nove vírgula oito, cento e noventa e seis mil newtons. O empuxo ganha, então ele decola. A aceleração inicial é a força resultante dividida pela massa: cento e quatro mil newtons sobre vinte mil quilos, cinco vírgula dois metros por segundo ao quadrado.

### E1-3 — tela: t_q ≈ 133 s; R = 5; 4.024; 1.307; 2.717 m/s
Agora o tempo de queima: dezesseis mil quilos a cento e vinte por segundo, uns cento e trinta e três segundos. A massa final é de quatro mil quilos, então a razão de massas é cinco. No espaço, isso daria dois mil e quinhentos vezes o logaritmo de cinco: uns quatro mil e vinte metros por segundo. Só que aqui a gravidade cobra nove vírgula oito vezes cento e trinta e três, uns mil e trezentos metros por segundo. Sobram uns dois mil e setecentos metros por segundo. Quase um terço do ganho foi embora só para vencer a gravidade.

### E1-4 — tela: a_f ≈ 65,2 m/s² (RESULTANTE); a_sentida = 75 m/s² (O QUE A CARGA SENTE); manequim; CONFERE; DICA
[curious] E no último instante da queima? Empuxo de trezentos mil newtons, agora empurrando só quatro mil quilos: a aceleração resultante vai a uns sessenta e cinco metros por segundo ao quadrado, quase sete vezes a gravidade. E o que a carga sente é ainda mais. A gravidade puxa tudo junto, por igual, e não aperta ninguém contra o assento: quem aperta é só o empuxo. Então a carga sente o empuxo dividido pela massa, setenta e cinco metros por segundo ao quadrado, mais de sete vezes e meia o próprio peso. Por isso muitos foguetes reduzem o motor em certas fases do voo. Confere com o que a gente viu: a razão de massas é cinco, maior que e, então no espaço esse foguete passaria da velocidade do próprio gás. E passa mesmo: quatro mil contra dois mil e quinhentos. E a dica: compara empuxo com peso antes de qualquer conta.

## E2 — POR QUE ESTÁGIOS? (responde o hook)

### E2-1 — tela: estágio em corte: CARGA P, PROPELENTE f, ESTRUTURA 0,1 f; v_ex = 3,0 km/s; ORÇAMENTO 9 km/s
[curious] Agora, a segunda metade da pergunta do começo. Um foguete não é só propelente: tem tanque, motor, estrutura. Vamos supor que essa estrutura pese dez por cento do propelente que ela carrega. Gás a três quilômetros por segundo, e o orçamento, de novo, é de nove quilômetros por segundo, com as perdas já incluídas nesse número. Dá para fazer com um estágio só?

### E2-2 — tela: m₀ = P + 1,1 f; m_f = P + 0,1 f; P → 0: R = 11; 7,2 km/s < 9 ✗
[thoughtful] No começo, o foguete tem a carga, o propelente e a estrutura: a carga mais um vírgula um vezes o propelente. No fim, sobram a carga e a estrutura vazia: a carga mais zero vírgula um vezes o propelente. Agora pega o caso mais generoso possível: carga zero. A razão de massas fica um vírgula um dividido por zero vírgula um, que é onze. E três vezes o logaritmo de onze dá sete vírgula dois quilômetros por segundo... [short pause] Não chega. Nem sem carga nenhuma. O tanque vazio é peso morto que o foguete carrega até o fim.

### E2-3 — tela: Three.js: separação de estágios no espaço
[curious] A saída é não carregar o tanque vazio. Divide o foguete em dois. O primeiro estágio queima, e quando esvazia, é jogado fora, com motor e tudo. Aí o segundo estágio acende, bem mais leve, e começa uma razão de massas nova.

### E2-4 — tela: R = e^1,5 ≈ 4,48; f₂ ≈ 5,34 P; m₀₂ ≈ 6,88 P; m₀₁ ≈ 47,3 P
[thoughtful] Vamos dividir o orçamento meio a meio: quatro vírgula cinco quilômetros por segundo para cada estágio. Isso é uma vez e meia a velocidade de exaustão, então cada estágio precisa de uma razão de massas de e elevado a um vírgula cinco, uns quatro vírgula quarenta e oito. Começa pelo de cima. A conta é a mesma de antes, só que agora ela fecha: o propelente do segundo estágio sai cinco vírgula três vezes a carga, e o segundo estágio inteiro, cheio, pesa seis vírgula nove vezes a carga. Agora o truque: para o primeiro estágio, o segundo estágio inteiro é a carga. A conta se repete igualzinha, e o foguete completo na rampa pesa seis vírgula nove vezes seis vírgula nove... uns quarenta e sete vezes a carga útil.

### E2-5 — tela: barra 89 / 9 / 2; 1 t DE CARGA → 47 t NA RAMPA; NESTE MODELO
[excited] E olha o que saiu. Com esse orçamento e essas hipóteses, para cada tonelada de carga útil, quarenta e sete toneladas na rampa. A carga é dois por cento do foguete, e o propelente, quase noventa por cento. É exatamente o retrato do foguete do começo: quase todo combustível.

### E2-6 — tela: CONFERE: ESTRUTURA → 0 ⇒ UM ESTÁGIO BASTA (R = 20); DIVISÃO MEIO A MEIO = ESCOLHA DIDÁTICA; DICA
[thoughtful] Confere: se a estrutura não pesasse nada, um estágio só bastaria, com aquela razão de massas de vinte. É a estrutura que obriga a dividir. E uma observação honesta: dividir a velocidade meio a meio entre os estágios foi uma escolha para deixar a conta limpa. Na engenharia, essa divisão é otimizada, e os estágios de verdade têm motores e tamanhos diferentes. A dica fica: o logaritmo cobra pela razão de massas, e cada estágio começa uma razão nova.

## E3 — A ESTEIRA DE AREIA

### E3-1 — tela: esteira, funil; v = 1,5 m/s; 20 kg/s; O QUE ESTE PEDE: MASSA QUE ENTRA; HIPÓTESES
[curious] Agora o foguete ao contrário: massa entrando. Um funil despeja areia numa esteira, vinte quilos por segundo. A esteira anda a um vírgula cinco metros por segundo, constante. A areia cai na vertical, sem velocidade horizontal. Que força o motor da esteira precisa fazer? E com que potência?

### E3-2 — tela: SISTEMA na areia; atrito, reação, motor; 30 N
[thoughtful] Escolhe o sistema seguindo a areia. A cada segundo, chegam vinte quilos de areia sem velocidade horizontal. Depois de escorregar um pouco, esses mesmos vinte quilos saem andando junto com a esteira, a um vírgula cinco metros por segundo. Então a esteira precisa entregar à areia trinta quilogramas metro por segundo de momento, a cada segundo. Isso é uma força de trinta newtons, que a esteira faz na areia pelo atrito. Por ação e reação, a areia puxa a esteira para trás com os mesmos trinta newtons. E, para a esteira não perder velocidade, o motor tem que compensar: trinta newtons.

### E3-3 — tela: 45 W; 22,5 W; barras; 22,5 W laranja ?
[curious] A potência é força vezes velocidade: trinta vezes um vírgula cinco, quarenta e cinco watts. Agora a energia cinética que a areia ganha por segundo: metade da vazão vezes a velocidade ao quadrado, vinte e dois vírgula cinco watts... [short pause] Exatamente a metade. O motor paga quarenta e cinco, e a areia só leva vinte e dois e meio. Para onde foi o resto?

### E3-4 — tela: grão no referencial da esteira; rastro laranja; NÃO DEPENDE DO ATRITO
[thoughtful, emphatic] Vai para o escorregamento. Quando o grão cai na esteira, ele ainda está parado, e a esteira passa por baixo dele. Ele escorrega até pegar a velocidade da esteira, e o atrito nesse escorregamento esquenta tudo. Agora olha do referencial da esteira: ali, cada grão chega a um vírgula cinco metros por segundo para trás e escorrega até parar. Ele perde toda a energia cinética que tinha nesse referencial, metade da massa vezes a velocidade ao quadrado, e isso vira calor. É a mesma quantidade que ele ganha visto do chão. Por isso é sempre metade, e não importa o atrito: um atrito maior faz o grão escorregar menos tempo, só que com uma força maior, e o calor dá o mesmo.

### E3-5 — tela: CONFERE unidades; DICA: O MOTOR PAGA O DOBRO
Confere: quilogramas por segundo vezes metros por segundo ao quadrado dá joule por segundo, que é watt. E a dica: quando a massa entra parada e a esteira não muda de velocidade, o motor sempre paga o dobro da energia cinética que entrega.

## SÍNTESE

### S1 — tela: três cartões; foguete do hook com a barra 89 · 9 · 2; pergunta do hook
[calm, satisfied] Então, voltando à pergunta do começo. O foguete acelera empurrando o próprio gás, e o empuxo é a velocidade de exaustão vezes a vazão. Só que a velocidade que ele ganha cresce com o logaritmo da razão de massas, e o logaritmo cobra caro: cada velocidade de exaustão a mais multiplica a razão por dois vírgula sete. Com o gás a três quilômetros por segundo e nove quilômetros por segundo para chegar à órbita, a conta pede um foguete que é quase todo propelente, e ainda dividido em estágios para jogar fora o tanque vazio. E tudo isso saiu de uma ideia só: escolher o sistema que inclui o que sai.

## ENCERRAMENTO

### EN1 — tela: logo com anéis; INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
Se essa conta mudou o jeito como você olha para um foguete, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### EN2 — tela: desafio; ícone de comentário
[curious] E fica um desafio para os comentários: um foguete de um estágio só, sem contar a estrutura, precisa ganhar o dobro da velocidade de exaustão. Que fração da massa inicial tem que ser propelente? Até a próxima!

## Números de conferência (g = 9,8 m/s²)

Ver a tabela do Anexo A do handoff v1 (reproduzida em `ficha.md`).
