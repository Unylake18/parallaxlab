"""yt_0003 — dados da narração aprofundada (v2) com âncoras.

Cada bloco = (id, tempo_atual_aprox_s, evento_visual, texto).
 - id: âncora (A01…); a voz do bloco COMEÇA quando o evento visual acontece (a cena é que se molda à voz).
 - tempo_atual: onde o evento ocorre hoje no preview_v1_7 (±4 s) — só referência; o vídeo vai esticar.
 - texto: fala. Várias frases no mesmo bloco = a cena espera a fala inteira antes do próximo evento.
Marcador [SEGURAR] no evento = a cena precisa ganhar tempo (espera) para a fala caber.
"""

SECOES = []


def secao(titulo, resumo):
    SECOES.append({"titulo": titulo, "resumo": resumo, "blocos": []})


def b(id_, t, evento, texto, nota=""):
    SECOES[-1]["blocos"].append({"id": id_, "t": t, "evento": evento, "texto": texto.strip(), "nota": nota})


# ───────────────────────────────────────────────────────── 1. HOOK
secao("1. Hook e pergunta central", "Duas perguntas locais (divergente e rotacional) e o problema: como leis sobre superfícies e caminhos dizem algo sobre UM ponto.")
b("A01", 0.5, "O campo radial de uma carga positiva aparece, com partículas escoando para fora.",
  "Olha esse campo elétrico saindo de uma carga positiva. Cada setinha diz, naquele ponto do espaço, para onde o campo aponta e com que intensidade.")
b("A02", 2.0, "Aparece o símbolo nabla ponto E e a pergunta \"o campo nasce aqui?\"; um anel de teste pisca perto da carga.",
  "Agora eu quero te fazer uma pergunta que parece simples: neste pontinho aqui, o campo elétrico está nascendo? Existe uma fonte exatamente aí? Essa pergunta tem nome: é o divergente do campo elétrico, escrito nabla ponto E.")
b("A03", 3.7, "Entra o campo girante à direita, com nabla vezes F e a pergunta \"o campo gira aqui?\"; a rodinha gira.",
  "E tem uma segunda pergunta, de outra natureza. Neste outro campo, as setas dão voltas. Se eu colocar uma rodinha aqui, ela gira? Existe circulação local? Isso é o rotacional, escrito nabla vezes F — aqui F é só um nome genérico para um campo vetorial qualquer.")
b("A04", 5.9, "Surge o texto: \"Como leis sobre superfícies e caminhos inteiros dizem o que acontece em UM ponto?\"",
  "O problema é este: as leis que a gente conhece falam de superfícies inteiras e de caminhos inteiros. Como é que uma lei assim consegue dizer o que acontece em um único ponto? É isso que a gente vai construir hoje, devagar, passo a passo — e no final você vai ver que são duas ferramentas gêmeas: o divergente e o rotacional.",
  "[SEGURAR] ~10 s de fala sobre uma tela parada; é o momento certo para a pergunta respirar.")

# ───────────────────────────────────────────────────────── 2. LEI DE GAUSS INTEGRAL
secao("2. Do fluxo global à carga envolvida", "Reconstrução da lei de Gauss: dA, normal, E·dA, soma sobre a superfície, carga envolvida, densidade ρ, e o convite ao zoom.")
b("A05", 8.5, "Surge a superfície gaussiana S, um círculo em torno da carga.",
  "Vamos começar pelo que já existe. Imagine uma superfície fechada em volta da carga. A gente chama ela de superfície gaussiana, e vou chamar de S. Ela é só uma moldura imaginária que a gente escolhe para fazer a conta.")
b("A06", 11.3, "Um pedacinho da superfície brilha e recebe o rótulo dA.",
  "Agora olha só um pedacinho minúsculo dessa superfície. Esse pedacinho tem uma área muito pequena, que a gente escreve como dA: o elemento de área. Pense nele como um azulejo infinitamente pequeno colado na superfície.")
b("A07", 13.0, "Aparece o vetor normal n-chapéu; abaixo se constrói \"dA vetor = n-chapéu dA\".",
  "Só que a área, sozinha, não diz para onde o azulejo está virado. Por isso a gente desenha uma seta de comprimento um, perpendicular à superfície e apontando para fora: é o vetor normal unitário, a normal externa, que a gente escreve n-chapéu. Juntando os dois, nasce o elemento de área vetorial: dA vetor é igual a n-chapéu vezes dA. Tamanho do azulejo, e a direção para onde ele olha.")
b("A08", 14.8, "Aparece o vetor campo elétrico E no mesmo pedacinho; E também surge à direita.",
  "No mesmo pedacinho, a gente também enxerga o campo elétrico, o vetor E, que a carga produz ali.")
b("A09", 17.5, "E e dA se fundem em \"E ponto dA\".",
  "Agora a pergunta é: quanto desse campo atravessa esse azulejo? Para responder, a gente faz o produto escalar entre o campo elétrico e o elemento de área vetorial: E ponto dA. Se o campo é perpendicular ao azulejo, o produto é o maior possível. Se o campo só passa raspando, o produto é zero. É a medida de quanto campo realmente atravessa aquele pedacinho de superfície.")
b("A10", 21.1, "Doze pedaços acendem em volta da superfície, cada um com seu E; surge a soma de E ponto dA.",
  "Mas a superfície tem muitos pedacinhos. Então a gente faz isso em cada um deles e soma tudo: a soma de E ponto dA sobre todos os pedaços.")
b("A11", 25.7, "A soma vira a integral de superfície fechada, com o símbolo de círculo e o S embaixo.",
  "Quando os pedacinhos ficam infinitamente pequenos, a soma vira uma integral. E como a superfície é fechada, a gente coloca um circulozinho no sinal da integral: integral de superfície fechada de E ponto dA. Esse número tem nome: é o fluxo do campo elétrico através da superfície, que a gente representa pela letra grega maiúscula fi.")
b("A12", 30.3, "A superfície encolhe e uma pequena região é levada até um cubo à direita.",
  "O que a lei de Gauss diz é que esse fluxo não depende da forma da superfície, só do que está dentro dela. Então, em vez de olhar a superfície toda, vamos olhar uma região pequena, dentro de um cubinho. Já vamos ver por quê.")
b("A13", 36.3, "O cubo cresce, com cinco cargas pontuais dentro; surge Q_env e a lei de Gauss integral.",
  "Dentro do cubo, aparecem algumas cargas. Somando todas elas, a gente tem a carga envolvida, que a gente escreve Q com índice env, de envolvida. E a lei de Gauss diz: o fluxo do campo elétrico é igual à carga envolvida dividida por epsilon zero — a permissividade elétrica do vácuo, uma constante da natureza que mede o quão facilmente o campo se estabelece no vácuo.")
b("A14", 40.5, "Mais cargas pequenas; depois uma nuvem densa; Q_env se transforma em integral de rô dV.",
  "Mas e se a carga não for um punhado de partículas separadas? Se tiver muita carga, tão espalhada que a gente nem enxerga os grãos? Então a gente passa a descrever a carga por quanto existe em cada pedacinho de volume. Essa grandeza é a densidade volumétrica de carga, que a gente chama de rô. Em cada pedacinho de volume dV, a carga é rô vezes dV. Somando todos os pedacinhos de volume, a carga envolvida vira a integral de volume de rô dV.",
  "[SEGURAR] a troca Q_env → ∫ρ dV é um dos pontos centrais; deixar a nuvem de pontos visível durante toda a explicação.")
b("A15", 48.6, "A região se preenche como um meio contínuo; a lei se reescreve com um sobre epsilon zero vezes a integral de rô dV.",
  "Agora a gente pode reescrever a lei de Gauss com essa carga distribuída: o fluxo do campo elétrico pela superfície é igual a um sobre epsilon zero vezes a integral, no volume, da densidade de carga. Repare: do lado esquerdo, uma integral sobre a superfície; do lado direito, uma integral sobre o volume que ela envolve.")
b("A16", 53.9, "Aparece a pergunta \"Como isso vale ponto a ponto?\".",
  "Só que isso é uma lei global: ela fala do cubo inteiro. E a nossa pergunta é: como isso vale ponto a ponto?")
b("A17", 56.4, "Um anel marca o ponto P dentro do cubo.",
  "Vamos escolher um ponto, que eu vou chamar de P, e olhar com uma lupa cada vez mais forte em volta dele.")
b("A18", 59.9, "Zoom: a geometria global recua e o anel cresce.",
  "À medida que a gente se aproxima, o resto do cubo some, o resto do espaço some, e só sobra a vizinhança imediata do ponto. É nessa vizinhança minúscula que a gente vai fazer a pergunta.")

# ───────────────────────────────────────────────────────── 3. DIVERGENTE
secao("3. Divergente: fluxo líquido por volume", "Construção do cubo diferencial: x±dx/2, dA_x, normais, fluxo em cada face, diferença finita → derivada parcial, soma em x, y, z, divergente.")
b("B01", 64.5, "Surge um eixo x com o ponto P; aparece \"x_P = x\" e o texto \"Primeiro, um intervalo centrado em P\".",
  "Para fazer essa conta, vamos simplificar. Primeiro, só uma direção: o eixo x. O ponto P está sobre ele, na posição x. A gente vai escolher um intervalo pequeno, centrado em P, para olhar em volta.")
b("B02", 68.0, "Aparece o segmento com marcas nas pontas e a chave com \"dx\".",
  "O comprimento desse intervalo é dx: um deslocamento muito pequeno em x. O d na frente significa isso, uma quantidade infinitesimal.")
b("B03", 72.0, "A chave se divide em duas, cada metade rotulada dx sobre 2.",
  "Como o intervalo está centrado em P, ele se divide em duas metades iguais. Metade para a esquerda, metade para a direita. Cada uma mede dx sobre dois.")
b("B04", 75.2, "Os rótulos viram os extremos: x menos dx sobre 2 e x mais dx sobre 2.",
  "Então os dois extremos do intervalo ficam em x menos dx sobre dois, à esquerda, e x mais dx sobre dois, à direita. Guarda bem esses dois endereços, porque eles vão voltar daqui a pouco.")
b("B05", 80.3, "O segmento vira um cubo; aparecem dx, dy e dz nas arestas.",
  "Agora a gente faz a mesma ideia nas três dimensões. O intervalo vira um cubinho centrado em P, com arestas dx, dy e dz. É o nosso cubo diferencial. O cubo é pequeno o bastante para que a gente trate o campo dentro dele de forma bem simples.")
b("B06", 86.8, "A face direita do cubo é destacada e rotulada dA_x; surge \"dA_x = dy dz\".",
  "Vamos olhar a face da direita, aquela que é perpendicular ao eixo x. A área dela é a largura vezes a altura: dy vezes dz. A gente escreve dA com índice x, porque é a face cuja normal aponta na direção x. Então: dA_x é igual a dy dz.")
b("B07", 91.8, "Aparece a normal externa n-chapéu mais, apontando para fora, com a legenda \"normal externa\"; surge n+ = +x-chapéu.",
  "E para onde olha essa face? Para fora do cubo. A normal externa dela aponta no sentido positivo de x. Chamamos de n-chapéu mais, e vale mais x-chapéu — x-chapéu sendo o vetor unitário na direção x.")
b("B08", 98.1, "Destaca-se a face esquerda; aparece n-chapéu menos = menos x-chapéu e o texto \"normais externas opostas\".",
  "Já a face da esquerda olha para o lado contrário. A normal externa dela aponta para menos x. Então n-chapéu menos é igual a menos x-chapéu. As duas normais são opostas, e isso vai ser importantíssimo no cálculo do sinal.")
b("B09", 105.1, "Na face direita aparecem o campo E, a componente E_x e uma linha tracejada; surge \"d fi = E ponto dA\".",
  "Agora, o fluxo através da face direita. Aparece o campo elétrico E, inclinado, com o seu pedacinho que aponta na direção x: a componente x do campo elétrico, que a gente escreve E com índice x. O fluxo infinitesimal, d fi, é o campo ponto elemento de área: d fi é igual a E ponto dA.")
b("B10", 109.0, "A expressão vira \"d fi x mais = E ponto x-chapéu dy dz\".",
  "Como o elemento de área é a normal vezes a área, e a normal dessa face é x-chapéu, o produto escalar E ponto x-chapéu seleciona apenas a parte do campo que aponta na direção x.")
b("B11", 112.4, "Fica \"d fi x mais = E_x dy dz\"; a componente E_x pulsa.",
  "E essa parte do campo que aponta na direção x é justamente a componente E_x. Então o fluxo na face direita é E_x vezes dy dz. As componentes do campo nas direções y e z passam raspando por essa face: elas não atravessam, e por isso não entram na conta.")
b("B12", 115.4, "Aparece \"E_x (face) dy dz\".",
  "Mas em que ponto a gente calcula E_x? Na face. Como o campo pode variar de um ponto para outro, a gente precisa dizer: o valor de E_x lá onde fica a face.")
b("B13", 121.0, "Fica \"d fi x mais = E_x (x + dx/2) dy dz\"; o extremo x + dx/2 é copiado para a expressão.",
  "E onde fica a face da direita? Exatamente no extremo direito do intervalo: x mais dx sobre dois. Está vendo o endereço que a gente guardou lá atrás? Então o fluxo pela face da direita é E_x calculado em x mais dx sobre dois, vezes dy dz.")
b("B14", 127.0, "A expressão sobe; a face esquerda é destacada, com E, E_x e \"d fi x menos = E ponto (menos x-chapéu) dy dz\".",
  "Agora a face da esquerda. A conta é igual, mas com um detalhe crucial: a normal aponta para menos x. Então o produto escalar com a normal troca de sinal, e o fluxo na face esquerda é E ponto menos x-chapéu, dy dz.")
b("B15", 131.0, "Fica \"d fi x menos = menos E_x dy dz\".",
  "Isso dá menos E_x dy dz. O sinal negativo tem uma interpretação física linda: se o campo aponta para a direita, ele está entrando pela face da esquerda. Fluxo que entra conta como negativo.")
b("B16", 135.6, "Fica \"d fi x menos = menos E_x (x - dx/2) dy dz\".",
  "E onde a gente calcula E_x agora? Na face da esquerda, que fica em x menos dx sobre dois — o outro endereço que a gente guardou.")
b("B17", 144.1, "As duas expressões se fundem em um colchete: \"d fi x = [E_x(x+dx/2) − E_x(x−dx/2)] dy dz\".",
  "Agora é só somar as duas faces. O que sai pela direita, menos o que entra pela esquerda. Repare que os dois termos vêm das duas expressões que a gente acabou de construir. O fluxo líquido nas faces perpendiculares a x é: E_x na direita, menos E_x na esquerda, tudo vezes dy dz.",
  "[SEGURAR] bloco de ~14 s; a fusão das duas expressões é o coração do raciocínio.")
b("B18", 148.6, "Multiplica e divide por dx; surge um gráfico de E_x contra x com uma secante entre os dois pontos.",
  "Agora um truque muito comum: eu multiplico e divido por dx. Isso não muda nada. Mas deixa aparecer uma coisa familiar: a diferença do campo entre dois pontos, dividida pela distância entre eles. Olha no gráfico: aqui está E_x em função de x, mantendo y e z fixos. Os dois pontos são os extremos do intervalo. A reta que passa pelos dois é a secante, e a inclinação dela é exatamente essa diferença dividida por dx.")
b("B19", 159.6, "A secante vai virando a tangente conforme dx diminui.",
  "E o que acontece quando o intervalo encolhe? Quando dx tende a zero, os dois pontos se juntam, e a secante vira a tangente. A inclinação da tangente é a derivada. Como estamos variando só x e mantendo y e z fixos, chamamos de derivada parcial de E_x em relação a x.",
  "[SEGURAR] ~6 s de animação do dx → 0; a voz deve acompanhar o encolhimento, não antecipar.")
b("B20", 162.4, "A expressão vira \"d fi x = (∂E_x/∂x) dx dy dz\".",
  "Pronto: o fluxo líquido nas duas faces perpendiculares a x é a derivada parcial de E_x em relação a x, vezes dx dy dz. Em palavras: quanto o campo na direção x cresce, por unidade de distância, vezes o volume do cubo.")
b("B21", 165.6, "Uma chave mostra \"dV = dx dy dz\".",
  "E dx dy dz é o volume do cubinho. Eu chamo de dV.")
b("B22", 170.5, "A expressão fica \"d fi x = (∂E_x/∂x) dV\".",
  "Então: d fi x é igual à derivada parcial de E_x em x, vezes dV. Veja a beleza: o fluxo líquido, para o mesmo cubinho, é proporcional ao volume dele.")
b("B23", 175.0, "Aparecem as faces ±y e depois a linha \"d fi y = (∂E_y/∂y) dV\".",
  "Agora a mesma coisa nas faces de cima e de baixo. A normal da face de cima aponta para mais y, a de baixo para menos y. O raciocínio é idêntico, só trocando x por y, e o resultado é: d fi y é igual à derivada parcial de E_y em relação a y, vezes dV.")
b("B24", 182.6, "Aparecem as faces ±z e a linha \"d fi z = (∂E_z/∂z) dV\".",
  "E nas faces da frente e de trás, na direção z, a mesma coisa: d fi z é a derivada parcial de E_z em z, vezes dV.")
b("B25", 189.1, "Surge \"d fi = d fi x + d fi y + d fi z\".",
  "O fluxo total do cubo é a soma dos fluxos pelos três pares de faces: d fi é igual a d fi x mais d fi y mais d fi z.")
b("B26", 192.1, "As três linhas se juntam em \"d fi = (∂E_x/∂x + ∂E_y/∂y + ∂E_z/∂z) dV\".",
  "Colocando o dV em evidência, o fluxo líquido que sai do cubinho é: a soma das três derivadas parciais, vezes o volume.")
b("B27", 197.0, "Uma chave destaca a soma e aparece \"divergente de E\"; o cubo pisca em cada par de faces.",
  "E essa soma — a derivada de E_x em x, mais a de E_y em y, mais a de E_z em z — ganha um nome só agora, depois de a gente entender de onde ela vem: o divergente do campo elétrico.")
b("B28", 202.4, "A expressão vira \"d fi = (nabla ponto E) dV\", e depois \"nabla ponto E = d fi / dV\".",
  "A gente escreve com um símbolo: nabla ponto E. Nabla é aquele triângulo de cabeça para baixo, e o ponto é o produto escalar entre o operador nabla — que reúne as três derivadas parciais — e o campo. Resultado: d fi é nabla ponto E vezes dV. Isolando: o divergente é o fluxo líquido por unidade de volume.")
b("B29", 205.4, "Surge a definição com limite: \"∇·E = lim 1/ΔV ∮ E·dA\".",
  "E esse é o significado de verdade do divergente: faço um volume cada vez menor em torno de um ponto, calculo o fluxo líquido que sai pela superfície dele, divido pelo volume, e vejo o que sobra no limite. É o fluxo líquido, por unidade de volume, num ponto.")
b("B30", 210.2, "Cubo com fluxo saindo, e a legenda \"nabla ponto E maior que 0\".",
  "Se nesse ponto o fluxo líquido é para fora, as setas divergem, o divergente é positivo. Existe uma fonte ali.")
b("B31", 217.6, "Cubo com fluxo entrando; \"nabla ponto E menor que 0\".",
  "Se o fluxo líquido é para dentro, o divergente é negativo. Existe um sumidouro.")
b("B32", 222.8, "Cubo com campo uniforme atravessando; \"nabla ponto E = 0\" e o aviso \"nabla ponto E = 0 não implica E = 0\".",
  "E se tanto entra quanto sai, na mesma quantidade, o fluxo líquido é zero, o divergente é zero. Mas atenção: divergente zero não quer dizer campo zero. Quer dizer só que, naquele ponto, não nasce nem some campo. O campo pode ser enorme e ainda assim atravessar o cubinho sem acumular nada.",
  "Gancho: comparar com água num cano; se a mesma quantidade entra e sai, não há torneira nem ralo, mas a água se move.")

# ───────────────────────────────────────────────────────── 4. TEOREMA DA DIVERGÊNCIA
secao("4. Teorema da divergência", "Duas normais em cada interface interna, cancelamento, células 2→4→8, integral de volume = fluxo na fronteira.")
b("C01", 230.4, "Dois cubos vizinhos, A e B, com a interface em destaque e as duas normais.",
  "Agora uma pergunta que parece desvio, mas é a chave: o que acontece quando dois volumes vizinhos dividem uma face? Aqui temos o cubo A e o cubo B, grudados. A face do meio pertence aos dois.")
b("C02", 233.5, "Aparecem n_A e n_B e o texto \"A mesma face é saída para um volume e entrada para o vizinho\".",
  "Para o volume A, a normal externa dessa face aponta para a direita, para dentro do B. Para o volume B, a normal externa da mesma face aponta para a esquerda, para dentro do A. Uma mesma face, duas normais externas, uma para cada lado.")
b("C03", 238.9, "Surgem uma seta de campo atravessando os dois cubos e as equações n_A = +x e n_B = −x.",
  "Com um campo atravessando da esquerda para a direita: para o A, esse campo sai por essa face. Para o B, ele entra. n-chapéu A é mais x-chapéu e n-chapéu B é menos x-chapéu.")
b("C04", 247.3, "Aparecem fi_A = +E·dA e fi_B = −E·dA.",
  "Então o fluxo através dessa face, para o A, é mais E ponto dA. Para o B, é menos E ponto dA. É o mesmo número, com o sinal trocado.")
b("C05", 254.4, "As duas contribuições se somam e dão zero.",
  "Se eu somar o fluxo dos dois volumes, a contribuição dessa face interna aparece duas vezes, uma positiva e uma negativa, e se cancela. Mais E ponto dA mais menos E ponto dA é igual a zero.")
b("C06", 262.6, "A cena vira uma grade de células: 2, 4, 8.",
  "Agora imagina isso com muitos cubinhos: dois, quatro, oito, quantos quiser, todos juntos formando um bloco maior.")
b("C07", 272.0, "As faces internas acendem, cada uma com um par de normais; depois se apagam; o contorno externo é destacado.",
  "Cada face interna tem um par de normais opostas, e em cada uma o fluxo se cancela. Elas acendem e desaparecem do cálculo. O que sobrou? Só as faces da fronteira externa, aquelas que não têm vizinho para cancelar.")
b("C08", 281.3, "Legendas: \"faces internas: cancelam\" e \"só a fronteira permanece\".",
  "Esse é o ponto central: tudo o que acontece dentro cancela, só a fronteira permanece.")
b("C09", 289.8, "Surge a soma sobre as células de (nabla·E) ΔV e ela vira a integral de volume de nabla·E dV.",
  "Cada célula contribui com o seu divergente vezes o seu volume. Somando todas as células, a soma vira, no limite, a integral de volume do divergente do campo elétrico, integral em V de nabla ponto E dV.")
b("C10", 296.0, "Surge a soma sobre faces externas, que vira a integral de superfície fechada de E·dA.",
  "Mas essa mesma soma também é a soma de todos os fluxos de todas as faces, e como as internas se cancelam, sobram só as externas. E a soma dos fluxos pelas faces externas é a integral de superfície fechada de E ponto dA sobre a fronteira.")
b("C11", 302.5, "As duas integrais se fundem na igualdade do teorema.",
  "Os dois cálculos são da mesma quantidade. Então: a integral de superfície fechada de E ponto dA é igual à integral de volume de nabla ponto E dV. Esse é o teorema da divergência, também chamado teorema de Gauss.")
b("C13", 306.0, "Aparece a divisão em duas colunas: \"TEOREMA DA DIVERGÊNCIA\" e \"LEI DE GAUSS\", com o mesmo fluxo à esquerda e à direita.",
  "Agora olha duas ideias diferentes sobre o mesmo fluxo. O teorema da divergência é matemática pura: vale para qualquer campo vetorial razoável, não precisa ser elétrico. A lei de Gauss é física: ela fala especificamente do campo elétrico e das cargas que o produzem.")
b("C14", 307.0, "O fluxo do teorema vira a integral do divergente; o da lei vira um sobre epsilon zero vezes a integral de rô.",
  "Do lado do teorema, o fluxo é a integral do divergente do campo. Do lado da lei de Gauss, o fluxo é um sobre epsilon zero vezes a integral da densidade de carga. Duas leituras da mesma grandeza.")
b("C15", 316.5, "Fica \"∫ nabla·E dV = ∫ (rô/ε0) dV\" e depois \"∫ (nabla·E − rô/ε0) dV = 0\".",
  "Igualando as duas: a integral do divergente é igual à integral de rô sobre epsilon zero. Passando tudo para um lado, a integral, em V, de nabla ponto E menos rô sobre epsilon zero, dV, é igual a zero.")
b("C16", 320.8, "Um volume vai encolhendo ao redor de um ponto, com o texto \"Qualquer volume regular apropriado\".",
  "E isso vale para qualquer volume — grande, pequeno, o que a gente quiser. Então eu posso encolher o volume até um ponto. Se a integral é zero para qualquer volume, por menor que seja, a única possibilidade é que o que está dentro dela seja zero em cada ponto.")
b("C17", 323.8, "A equação vira \"nabla ponto E = rô sobre epsilon zero\", dentro de uma caixa.",
  "Isso nos dá a lei de Gauss na forma diferencial: nabla ponto E é igual a rô sobre epsilon zero. Em cada ponto do espaço: o divergente do campo elétrico é a densidade de carga ali, dividida por epsilon zero.")
b("C18", 330.0, "Aparecem \"rô > 0 ⇒ nabla·E > 0\" e depois \"rô < 0 ⇒ nabla·E < 0\".",
  "Se há carga positiva no ponto, o divergente é positivo: o campo nasce ali, a carga positiva é fonte. Se há carga negativa, o divergente é negativo: as linhas de campo morrem ali, a carga negativa é sumidouro. A carga é a fonte do campo — só que agora dito ponto a ponto.")

# ───────────────────────────────────────────────────────── 5. EXEMPLO κ
secao("5. Um exemplo: campo que cresce com a posição", "E = κ(x x̂ + y ŷ + z ẑ): três derivadas iguais a κ somam 3κ.")
b("K01", 334.0, "Campo com setas que crescem para longe da origem; surge a fórmula E = κ(x x-chapéu + y y-chapéu + z z-chapéu).",
  "Vamos ver como isso funciona num exemplo concreto, bem simples. Esse campo aqui tem a seguinte forma: E é kappa vezes x x-chapéu mais y y-chapéu mais z z-chapéu. Kappa é uma constante: um número fixo que diz o quanto o campo cresce a cada unidade de distância.")
b("K02", 337.5, "Um ponto de prova se afasta da origem e a seta cresce; surge \"|E| proporcional a r\".",
  "Quanto mais longe da origem, mais forte é o campo, proporcional à distância r. Ele aponta para fora e vai crescendo.")
b("K03", 342.0, "Eixos x, y, z e um ponto de prova sobre cada um, com E_x = κ x e a derivada parcial igual a κ.",
  "Vamos calcular o divergente. Pelo que a gente construiu, precisamos das derivadas parciais, uma por uma. A componente x do campo é kappa vezes x. Derivando em relação a x, sobra kappa. A componente y é kappa y; derivando em relação a y, kappa. A componente z é kappa z; derivando em relação a z, também kappa.")
b("K03b", 347.0, "Três kappas se somam: \"kappa + kappa + kappa\", que vira \"3 kappa\"; aparece \"nabla·E =\" ao lado.",
  "Somando as três, o divergente é três kappa. É constante, o mesmo em todo ponto do espaço. Isso nos conta algo físico: para um campo desse tipo, haveria carga distribuída uniformemente por todo o espaço, com densidade rô igual a três epsilon zero kappa, porque a lei de Gauss diz que rô é epsilon zero vezes o divergente.",
  "Observação para o roteiro: na tela hoje a legenda do κ está pequena demais (ver relatório); ajustar tamanho.")

# ───────────────────────────────────────────────────────── 6. CARGA PONTUAL E DELTA
secao("6. Carga pontual e a delta de Dirac", "Divergente zero fora da origem, fluxo constante, o conflito, o volume que encolhe, a delta tridimensional, rô = q δ³.")
b("D01", 351.2, "Campo de uma carga pontual; fórmula E = q/(4πε0) r-chapéu / r² e nabla·E = 0 (r ≠ 0).",
  "Vamos para o caso mais importante: uma única carga pontual. O campo dela é E igual a q sobre quatro pi epsilon zero, vezes r-chapéu sobre r ao quadrado. Aqui q é o valor da carga, r é a distância até ela, r-chapéu é o vetor unitário que aponta da carga para fora. É a lei de Coulomb, escrita como campo. Se a gente calcular o divergente dessa expressão, em qualquer ponto fora da origem, dá zero.")
b("D02", 360.6, "Um cubinho de prova passeia pelo campo e é marcado em três posições.",
  "Dá para sentir isso no cubinho: leve ele para lá, para cá, para onde quiser, menos para cima da carga. Sempre entra tanto campo quanto sai. O divergente é zero. A carga é a fonte, mas nenhum ponto fora dela é fonte.")
b("D03", 375.6, "O cubo some; surge uma esfera em volta da carga com o campo na fronteira; fluxo = q/ε0.",
  "Mas olha o que acontece com o fluxo através de uma esfera em volta da carga. A lei de Gauss diz: o fluxo é q sobre epsilon zero. E esse resultado não depende do raio da esfera.")
b("D04", 384.2, "A esfera encolhe, com a razão R sobre R zero caindo de 1 para 0,15, e a legenda \"FLUXO CONSTANTE\".",
  "Vamos fazer a esfera encolher. O raio R vai diminuindo, comparado com o raio inicial, R zero. Um, meio, um décimo... O campo na superfície fica cada vez mais forte, mas a área fica cada vez menor, e os dois efeitos se compensam exatamente: o fluxo continua o mesmo, q sobre epsilon zero. Isso acontece porque o campo cai com o quadrado da distância e a área da esfera cresce com o quadrado do raio.",
  "[SEGURAR] ~10 s de encolhimento; a voz explica o compromisso campo × área sem pressa.")
b("D05", 395.5, "Aparece \"fora da origem, o divergente é zero\" e a pergunta \"Onde está a fonte?\".",
  "Então temos um problema. Fora da origem, o divergente é zero. Mas o fluxo, por uma superfície em volta da origem, não é zero. Onde está a fonte?")
b("D06", 405.8, "Reaparecem as duas informações em conflito e a pergunta \"Como representar uma fonte inteira concentrada em um único ponto?\".",
  "Olha o conflito. De um lado, divergente zero em todo ponto fora da origem. Do outro, fluxo diferente de zero por qualquer superfície que envolva a origem. A única saída é que o divergente seja zero em todo lugar menos num ponto — mas que nesse ponto ele concentre toda a fonte. Como a gente representa matematicamente uma fonte inteira concentrada em um único ponto?")
b("D07", 409.2, "Um volume encolhe em torno da origem com Q_env = q; a legenda diz que a carga dentro não muda.",
  "Olha o que acontece com a carga envolvida quando o volume encolhe. O volume diminui, diminui... e a carga dentro continua sendo q. O volume vai a zero, a carga não vai.")
b("D08", 423.6, "Título \"Delta de Dirac tridimensional\" e o símbolo delta com índice 3 e r vetor.",
  "Precisamos de um objeto que faça exatamente isso: que seja zero fora de um ponto, e que, mesmo assim, integrado em qualquer região que contenha o ponto, dê um. Esse objeto se chama delta de Dirac tridimensional, e se escreve delta três de r.")
b("D09", 426.7, "Aparece a anotação \"(3): três dimensões, não potência\" e \"uma distribuição que concentra integral unitária num ponto\".",
  "Esse três no expoente não é uma potência. Delta ao cubo não é a ideia aqui. É só o aviso de que estamos em três dimensões. E a delta é o que os matemáticos chamam de distribuição: um objeto que concentra integral unitária num ponto.")
b("D10", 437.4, "Um volume V se aproxima da origem; aparece \"∫_V δ³(r) dV = 0\" e a legenda \"origem fora de V\".",
  "Pra entender o que ela faz, vamos usar um volume de teste, V. Quando a origem está fora desse volume, a integral da delta em V é zero. A delta vale zero em todos os pontos de V.")
b("D11", 449.0, "O volume atravessa a origem; um flash na carga; \"∫_V δ³ dV = 1\" e \"origem dentro de V\".",
  "Agora o volume avança até conter a origem. E o resultado muda: a integral da delta sobre V passa a ser um. A integral não vale 1 sobre a fronteira, e é por isso que a gente evita afirmar o valor justo quando a origem está na borda. Sempre um se a origem está dentro, sempre zero se está fora.")
b("D12", 457.6, "Aparecem \"não é uma função comum: só ganha sentido sob uma integral\" e a unidade [δ³] = m⁻³.",
  "É importante guardar: a delta não é uma função comum. Ela só ganha sentido dentro de uma integral. E tem unidade: como a integral da delta sobre um volume dá um número puro, a delta tem unidade de um sobre metro cúbico. Metro à menos três.")
b("D13", 460.6, "A carga q sobe e se transforma em \"rô(r) = q δ³(r)\".",
  "Agora a conexão com a física. A carga q está concentrada numa origem. A densidade de carga dessa configuração é rô de r igual a q vezes delta três de r. Zero em todo lugar, menos na origem, e integrando no volume, dá exatamente q.")
b("D14", 467.7, "Aparecem \"carga total q concentrada em r = 0\" e a lei de Gauss diferencial; as duas se fundem em ∇·E = (q/ε0) δ³(r).",
  "Colocando na lei de Gauss diferencial: nabla ponto E é rô sobre epsilon zero, que é q sobre epsilon zero vezes delta três de r.")
b("D15", 478.4, "O volume de teste encolhe sobre a carga; texto \"a delta resolve o conflito: divergente zero fora, fonte na origem\".",
  "E aí o conflito desaparece: fora da origem a delta é zero, então o divergente é zero. Na origem, a delta concentra tudo, então existe fonte. Divergente zero fora, fonte inteira na origem.",
  "Gancho: a mesma delta aparece na gravitação, onde uma massa pontual é fonte do campo gravitacional, e na mecânica quântica, onde descreve uma partícula perfeitamente localizada.")

# ───────────────────────────────────────────────────────── 7. COMPARAÇÃO F1/F2/Ω
secao("7. Mesmo divergente, outra geometria: Ω e o rotacional", "Dois campos F1 e F2 com divergente zero, a constante Ω controlando o giro, a sonda e o medidor de giro local, ∇×F.")
b("D16", 481.1, "Título \"Mesmo divergente, outra geometria\"; surge o campo uniforme F1 = F0 x-chapéu com um cubo de teste e ∇·F1 = 0.",
  "O divergente é uma pergunta sobre fonte. Mas existe outra pergunta sobre o campo, completamente diferente. Veja este primeiro campo. F1 é igual a F zero vezes x-chapéu: todas as setas apontam para a direita, com a mesma intensidade. O divergente dele é zero, porque o que entra num cubinho é igual ao que sai.")
b("D17", 486.4, "Surge o eixo com Ω e quatro pontos com setas tangenciais.",
  "Agora um campo bem diferente. Em vez de linhas retas, ele dá voltas em torno do centro. Em cada ponto, a seta é tangente a um círculo. E tem uma constante que controla o quão rápido ele gira: ômega, a letra grega maiúscula. Ômega maior, giro mais forte; ômega zero, sem giro.")
b("D18", 494.0, "O valor de Ω sobe de 0,6 a 1,3 e as setas crescem.",
  "Eu posso aumentar ômega, e as setas ficam mais fortes. Isso é só uma intensidade, é como o volume desse giro.")
b("D19", 500.0, "Ω vira a fórmula F2 = Ω(−y x-chapéu + x y-chapéu); aparece o campo completo.",
  "A fórmula completa desse campo, que eu vou chamar de F dois, é: ômega vezes menos y x-chapéu mais x y-chapéu. Em cada ponto de coordenadas x e y, o campo aponta perpendicularmente ao raio. Por isso ele gira. E se você calcular o divergente dele, dá zero também. Os dois campos, F um e F dois, têm divergente zero. Mas são completamente diferentes! Um é reto, o outro gira.")
b("D20", 508.7, "Telas lado a lado: F1 com sonda parada e F2 com sonda girando; surge o medidor GIRO LOCAL.",
  "Para enxergar essa diferença, imagine colocar uma rodinha de pás em cada campo, como uma roda d'água. No campo reto, as pás sentem a mesma força dos dois lados, e a roda fica parada. No campo que gira, o lado de cima empurra para um lado e o lado de baixo empurra para o outro, e a roda gira. Esse barrinha, o giro local, mostra isso: no campo reto, zero; no campo que gira, ele cresce com ômega.")
b("D21", 515.0, "Surge o operador \"nabla vezes F\" no centro, com \"mede o giro local do campo\".",
  "Existe um operador que mede esse giro: nabla vezes F, o rotacional do campo F. Ele faz, para o giro, o que o divergente faz para a fonte.")
b("D22", 519.8, "Aparecem ∇×F1 = 0 e ∇×F2 = 2Ω z-chapéu, com o símbolo da direção de z.",
  "Para o campo reto, o rotacional é zero. Para o campo que gira, o rotacional é dois ômega vezes z-chapéu. O dois aparece porque o giro local do campo é o dobro da velocidade angular do campo. E o z-chapéu diz a direção do giro: usando a regra da mão direita, se os dedos acompanham o giro, o polegar aponta para fora da tela, na direção z positiva.")
b("D23", 530.0, "A cena limpa e o operador vira \"nabla vezes E\", agora no campo eletrostático.",
  "Agora a pergunta que importa para a gente: e o campo eletrostático, aquele criado por cargas paradas? Ele gira ou não gira? É isso que a gente vai descobrir.")

# ───────────────────────────────────────────────────────── 8. CIRCULAÇÃO
secao("8. Circulação: acumular ao longo do caminho", "Integral de linha de E·dℓ entre a e b, só a componente radial conta, 1/r_a − 1/r_b, dois caminhos com o mesmo valor, ida por C1 e volta por C2: zero.")
b("E01", 525.9, "Carga pontual, pontos a e b, os raios r_a e r_b tracejados; surge o caminho C1.",
  "Para responder, a gente precisa de uma nova ferramenta: a circulação. Aqui está uma carga pontual, e dois pontos, a e b. A distância da carga até a é r a; a distância da carga até b é r b. E um caminho, C um, que vai de a até b.")
b("E02", 537.0, "Surge \"∫_C1 E·dℓ\"; um ponto percorre o caminho, com o vetor dℓ tangente e o campo E em cada posição.",
  "A gente quer somar, ao longo desse caminho, o quanto o campo ajuda ou atrapalha o movimento. Em cada ponto, tem o campo elétrico E, e tem o deslocamento infinitesimal ao longo do caminho, dℓ: uma setinha muito curta, tangente ao caminho, que aponta no sentido em que a gente está andando. Fazemos o produto escalar E ponto dℓ, e somamos tudo ao longo do caminho: integral em C um de E ponto dℓ. É a circulação ao longo do caminho. A barrinha embaixo mostra essa soma acumulando.")
b("E03", 549.6, "O caminho já foi percorrido; aparece a decomposição de dℓ em componente radial dr e a componente transversal.",
  "Qual é o valor dessa conta? Para uma carga pontual, o campo aponta sempre na direção radial. Então só a parte de dℓ que também é radial importa. Essa parte é o dr: a variação da distância até a carga. A parte transversal, perpendicular ao raio, não entra no produto escalar, porque é perpendicular ao campo.")
b("E04", 556.0, "Surge \"E·dℓ = q/(4πε0 r²) dr\".",
  "Então E ponto dℓ é q sobre quatro pi epsilon zero r ao quadrado, vezes dr.")
b("E05", 562.3, "A expressão vira \"∫ E·dℓ = q/(4πε0) ∫ dr/r²\" com limites de r_a a r_b.",
  "Somando ao longo do caminho, o r vai de r a até r b, então a integral é: q sobre quatro pi epsilon zero, vezes a integral de dr sobre r ao quadrado, indo de r a até r b.")
b("E06", 567.4, "A expressão vira q/(4πε0) vezes (1/r_a − 1/r_b); r_a e r_b piscam.",
  "E a integral de um sobre r ao quadrado, dr, é menos um sobre r. Calculando entre r a e r b, dá: um sobre r a, menos um sobre r b. Então a circulação ao longo do caminho C um é q sobre quatro pi epsilon zero vezes um sobre r a menos um sobre r b. Veja: o resultado só depende dos extremos. Não depende de como o caminho passa pelo meio.",
  "Gancho: isso é exatamente a forma da energia potencial de Coulomb, que aparece lá no fim.")
b("E07", 570.0, "O resultado sobe; surge um segundo caminho C2 com os mesmos extremos e outro tracer.",
  "Vamos conferir com outro caminho. Aqui está o C dois: sai do mesmo ponto a, chega no mesmo ponto b, mas dá uma volta bem diferente.")
b("E08", 583.7, "C2 percorrido; a expressão com C2 aparece igual à de C1.",
  "E o resultado é o mesmo: q sobre quatro pi epsilon zero, vezes um sobre r a menos um sobre r b. Outro caminho, a mesma circulação.")
b("E09", 596.3, "As duas se fundem: \"∫_C1 E·dℓ = ∫_C2 E·dℓ\"; o texto \"caminhos diferentes, mesmos extremos\".",
  "Então a circulação por C um é igual à circulação por C dois. Caminhos diferentes, mesmos extremos, mesmo valor. É uma propriedade de campos que, no jargão, são conservativos. Se você já viu trabalho de uma força conservativa, é a mesma ideia: o trabalho só depende da posição inicial e da final.")
b("E10", 600.5, "Aparece \"C = C1 − C2\".",
  "Agora a ideia decisiva: vai por C um e volta por C dois, no sentido contrário. Isso forma um caminho fechado, que eu vou chamar de C. Como a volta é feita ao contrário, o que a gente acumula na volta tem sinal oposto. Então a circulação do caminho fechado é C um menos C dois.")
b("E11", 609.0, "Um tracer percorre a volta completa; a barra acumula e volta ao zero.",
  "E olha o que acontece quando a gente anda esse caminho completo. A barra sobe na ida; na volta, ela desce, e fecha no zero. Quando a gente volta ao ponto inicial, não sobra nada.")
b("E12", 621.8, "Aparece \"∮_C E·dℓ = 0\".",
  "Então a circulação do campo elétrico, ao longo de qualquer caminho fechado, é zero: integral de linha fechada de E ponto dℓ igual a zero. Nenhum caminho fechado ganha energia dando voltas num campo eletrostático.",
  "Gancho: contraste com um moinho de água, onde a água que circula em volta de um redemoinho acumula circulação diferente de zero.")

# ───────────────────────────────────────────────────────── 9. STOKES
secao("9. Teorema de Stokes: da borda ao interior", "Circulação na borda = soma de pequenos giros locais no interior; ∇×F; F → E; ∇×E = 0.")
b("E13", 627.6, "O caminho fechado vira a curva C; surge \"∮_C F·dℓ\" e um ponto percorre a borda com setinhas dℓ tangentes.",
  "Agora a pergunta é: dá para ligar essa circulação, que é uma conta feita na borda de uma curva, com o giro local, que é uma coisa que acontece no interior? Imagine uma curva fechada C, e um campo qualquer, F. A circulação do campo ao longo da curva é a integral de linha fechada de F ponto dℓ. A gente anda sobre a borda, e o dℓ aponta tangente ao caminho.")
b("E14", 637.0, "Uma superfície S, preenchida, se estende dentro da curva; aparecem 7 pequenos rotores.",
  "Agora imagine uma superfície S, que tem essa curva como borda: como a película de uma bolha de sabão presa num aro. Dentro dessa película, em cada pedacinho, o campo faz um pequeno giro. São pequenos rotores locais, cada um medindo a circulação num pedacinho minúsculo.")
b("E15", 644.4, "Cada rotor vira um vetor nabla×F, com a normal n-chapéu e o rótulo dA.",
  "O giro de cada pedacinho vira um vetor: o rotacional do campo, nabla vezes F, apontando na direção do eixo do giro. Cada pedacinho tem a sua área, dA, e a sua normal, n-chapéu. A contribuição de cada pedacinho é o rotacional ponto n-chapéu, vezes dA: o quanto desse giro atravessa o pedacinho, na direção da normal.")
b("E16", 650.1, "Surge \"d A vetor = n-chapéu dA\" e depois \"(∇×F)·n-chapéu dA\".",
  "Isso a gente já viu antes: o elemento de área vetorial, dA vetor, é a normal vezes dA. Então a contribuição de cada pedacinho é nabla vezes F, ponto dA vetor.")
b("E17", 657.9, "A soma sobre os pedacinhos vira \"∫_S (∇×F)·dA\".",
  "Somando todos os pedacinhos da superfície, a soma vira uma integral de superfície: integral em S de rotacional de F ponto dA.")
b("E18", 661.7, "Aparece a igualdade completa do teorema de Stokes.",
  "E aí vem o teorema de Stokes. A circulação na borda é igual ao rotacional acumulado no interior: integral de linha fechada de F ponto dℓ é igual à integral de superfície de nabla vezes F ponto dA. O que acontece na borda é a soma de tudo que gira lá dentro, porque nos pedacinhos vizinhos o giro de um cancela com o do outro, igualzinho àquelas faces internas do cubo, e só sobra a borda.",
  "Gancho: mesma estrutura de cancelamento interno do teorema da divergência; um é o primo do outro.")
b("E19", 668.5, "O título muda para \"No campo eletrostático\"; F vira E; os rotores param.",
  "Agora, trocando F por E, o campo elétrico estático. Já sabemos que a circulação é zero em qualquer caminho fechado. Então os pequenos giros param.")
b("E20", 677.0, "Aparecem \"∮ E·dℓ = 0\" e depois \"0 = ∫ (∇×E)·dA\" e \"∫ (∇×E)·dA = 0\".",
  "Se a circulação na borda é zero, o rotacional acumulado no interior também é zero: integral de superfície de nabla vezes E ponto dA igual a zero. E isso vale para qualquer superfície que eu desenhe.")
b("E21", 689.5, "Um pequeno quadrado de superfície gira em várias orientações; \"(∇×E)·n-chapéu ΔA = 0\".",
  "Então eu posso pegar uma superfície minúscula, de área delta A, virada para onde eu quiser, e a conta continua dando zero. Em qualquer pequena superfície, em qualquer orientação, nabla vezes E ponto n-chapéu vezes delta A é zero. A única forma de isso ser verdade para toda orientação é que o próprio vetor, nabla vezes E, seja zero.")
b("E22", 695.6, "A equação vira \"∇×E = 0\", dentro de uma caixa.",
  "E aí está: o rotacional do campo elétrico estático é zero. O campo eletrostático é irrotacional.")

# ───────────────────────────────────────────────────────── 10. MAPA
secao("10. O mapa final", "Duas perguntas locais; dois operadores; duas leis; global → local.")
b("F01", 644.4, "Surge E(r) no topo; \"Há fonte local?\" à esquerda, com o cubo e o fluxo; \"FLUXO\".",
  "Vamos juntar tudo. No topo, o campo elétrico, que depende da posição. E duas perguntas, uma de cada lado. À esquerda: há fonte local? Para responder, usamos um cubinho e o fluxo através dele.")
b("F02", 657.9, "À esquerda: \"∇·E\" vira \"∇·E = ρ/ε0\", com a legenda \"GAUSS · GLOBAL → LOCAL\".",
  "A resposta vem do divergente. E o divergente do campo elétrico é a densidade de carga sobre epsilon zero. É a lei de Gauss, passando do global ao local.")
b("F03", 661.7, "À direita: \"Há circulação local?\", com a rodinha e o campo uniforme.",
  "À direita: há circulação local? Aqui usamos uma rodinha, o rotacional.")
b("F04", 684.3, "À direita: \"∇×E\" vira \"∇×E = 0\" com a legenda \"STOKES · GLOBAL → LOCAL\".",
  "O rotacional do campo eletrostático é zero. É o teorema de Stokes, também passando do global ao local.")
b("F05", 689.5, "Os dois lados pulsam juntos.",
  "Duas perguntas, dois operadores. Fonte local: divergente, que vale a densidade de carga sobre epsilon zero. Giro local: rotacional, que vale zero. É assim que a eletrostática inteira cabe em duas equações.")

# ───────────────────────────────────────────────────────── 11. FARADAY / POTENCIAL
secao("11. Faraday e o potencial elétrico", "Quando B varia no tempo o rotacional deixa de ser zero; na eletrostática ∂B/∂t = 0; V como campo escalar e E = −∇V.")
b("F06", 700.0, "Surge \"∇×E = −∂B/∂t\" com um campo B pulsando à esquerda.",
  "Mas calma, não é sempre zero. Esse resultado vale na eletrostática. Existe uma equação mais geral, a lei de Faraday: nabla vezes E é igual a menos a derivada parcial do campo magnético B em relação ao tempo. Se o campo magnético varia no tempo, o campo elétrico passa a ter rotacional. É o princípio dos geradores e dos transformadores.")
b("F07", 705.4, "B(t) oscila e depois congela; surge \"∂B/∂t = 0\".",
  "Na eletrostática, as cargas estão paradas, e não há campo magnético variando. Então a derivada de B em relação ao tempo é zero.")
b("F08", 713.2, "A expressão vira \"∇×E = −0\" e depois \"∇×E = 0\".",
  "E o termo da direita some: menos zero é zero. Aí o rotacional de E volta a ser zero. O zero da eletrostática não é um acaso: nasce de não haver variação de campo magnético.")
b("F09", 718.0, "Surge uma carga e arcos de equipotenciais, com rótulos V1, V2, V3.",
  "E agora uma ideia que sai desse zero. Como o rotacional é zero e o campo é conservativo, a gente pode descrever o campo elétrico por um único número em cada ponto do espaço: o potencial elétrico, V. Aqui estão superfícies de mesmo potencial, as equipotenciais: V um, V dois, V três.")
b("F10", 724.0, "Um ponto percorre uma equipotencial e depois sobe de V; surgem as setas branca (gradiente) e ciana (E).",
  "O potencial é um campo escalar: um número em cada ponto, sem direção. O gradiente de V, nabla V, é um vetor que aponta para onde V cresce mais depressa. E o campo elétrico aponta no sentido contrário, para onde V cai mais depressa.")
b("F11", 730.0, "\"∇V\" vira \"E = −∇V\"; texto: \"um campo vetorial descrito por um escalar\".",
  "Então: o campo elétrico é menos o gradiente do potencial. Um campo vetorial, com três componentes, descrito por um escalar, com um número só. Essa é a ponte para o próximo assunto: o potencial elétrico.",
  "Gancho: tem a ver com energia potencial, linhas de nível de um mapa topográfico e a ideia de que a água desce a ladeira.")

# ───────────────────────────────────────────────────────── 12. ENCERRAMENTO
secao("12. Payoff e CTA", "Fechamento e chamada para inscrição, no padrão de yt_0001/yt_0002.")
b("G01", 736.2, "Surge \"DIVERGENTE E ROTACIONAL\".",
  "Divergente e rotacional. Duas perguntas locais sobre um campo, que a gente aprendeu a responder a partir de superfícies e caminhos inteiros.")
b("G02", 741.0, "Surge \"FLUXO → FONTE LOCAL · CIRCULAÇÃO → GIRO LOCAL\".",
  "Fluxo, que vira fonte local. Circulação, que vira giro local. Gauss para o primeiro, Stokes para o segundo.")
b("G03", 748.0, "A logo Parallax Lab e anéis tracejados.",
  "Esse foi mais um passo dentro do eletromagnetismo, aqui no Parallax Lab.")
b("G04", 752.0, "Surge \"Inscreva-se para acompanhar os próximos vídeos\".",
  "Se esse vídeo te ajudou, se inscreve no canal para acompanhar os próximos. Até a próxima.")
