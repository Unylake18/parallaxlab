# yt_0003 — Narração V3 GPT

## Princípio desta versão

A voz é a referência de ritmo. O Manim entra para demonstrar, destacar, transformar e esperar a conclusão de cada ideia. Os tempos atuais do preview V1.7 servem apenas para localizar o evento visual; não são metas de duração final.

A narração evita ler a tela. Ela explica o raciocínio que conecta uma imagem à próxima. Toda grandeza é apresentada pelo nome na primeira ocorrência; depois pode ser encurtada quando o referente estiver inequívoco.

### Convenção de fala

- **\(\mathbf E\)**: campo elétrico; \(E_x\): componente x do campo elétrico.
- **\(\nabla\cdot\mathbf E\)**: divergente do campo elétrico; na primeira vez, “nabla ponto E”.
- **\(\nabla\times\mathbf F\)**: rotacional do campo vetorial; na primeira vez, “nabla vetorial F” ou “nabla cruz F”, conforme a voz padrão da série.
- **\(d\mathbf A\)**: elemento de área vetorial; \(dA\): elemento de área.
- **\(\hat{\mathbf n}\)**: vetor normal unitário, ou normal externa.
- **\(\rho\)**: rô, densidade volumétrica de carga.
- **\(\varepsilon_0\)**: epsilon zero, permissividade elétrica do vácuo.
- **\(\kappa\)**: kappa, constante escalar que controla a taxa de crescimento do campo.
- **\(\delta^{(3)}\)**: delta de Dirac tridimensional.
- **\(\Omega\)**: ômega maiúsculo, parâmetro escalar que controla a intensidade do campo giratório.
- **\(d\boldsymbol\ell\)**: deslocamento infinitesimal tangente ao caminho.
- **\(V\)** no final: potencial elétrico, um campo escalar.

---

# 1. HOOK — duas perguntas locais

### H01 — campo radial e fonte
**Evento visual:** campo radial de uma carga positiva; surge a ideia de “o campo nasce aqui?”.

> Uma lei de campo pode ser escrita de duas maneiras muito diferentes. Uma delas olha uma superfície inteira ou um caminho inteiro. A outra tenta responder uma pergunta local: o que está acontecendo exatamente neste ponto do espaço?

### H02 — divergente
**Evento visual:** aparece \(\nabla\cdot\mathbf E\).

> Para um campo elétrico, a primeira pergunta é: existe fonte aqui? O campo está, localmente, saindo mais do que entrando? A ferramenta que responde isso é o **divergente do campo elétrico**, escrito nabla ponto E.

### H03 — campo giratório e rotacional
**Evento visual:** campo genérico giratório com pequena sonda; aparece \(\nabla\times\mathbf F\).

> A segunda pergunta é diferente: existe uma tendência local de giro? Se eu colocasse uma pequena sonda geométrica nesse campo, ela tenderia a girar? A ferramenta para isso é o **rotacional**. Aqui eu escrevo nabla cruz F porque, por enquanto, F representa um campo vetorial qualquer.

### H04 — pergunta central
**Evento visual:** global → local.

> O desafio de hoje é entender como essas duas perguntas locais nascem de leis globais. A Lei de Gauss fala de fluxo através de uma superfície fechada. A circulação fala do campo acumulado ao longo de um caminho. A gente vai partir dessas quantidades globais, entrar no detalhe de um ponto e chegar a duas equações locais da eletrostática.

---

# 2. LEI DE GAUSS — reconstruindo o fluxo

### G01 — superfície gaussiana
**Evento visual:** superfície fechada S em torno da carga.

> Começa pela Lei de Gauss. Imagine uma superfície fechada envolvendo a carga. Essa superfície é uma construção matemática; ela não precisa ser uma casca material. A gente escolhe essa superfície para medir quanto campo elétrico atravessa a sua fronteira.

### G02 — elemento de área
**Evento visual:** um patch da superfície recebe \(dA\).

> Pegue um pedacinho muito pequeno da superfície. A área desse pedacinho é o **elemento de área**, dA. Mas a área, sozinha, não diz para que lado a superfície está orientada.

### G03 — normal e elemento de área vetorial
**Evento visual:** entra \(\hat{\mathbf n}\), depois \(d\mathbf A=\hat{\mathbf n}\,dA\).

> Por isso associamos a esse pedacinho uma seta perpendicular à superfície: a **normal externa**. Quando juntamos o tamanho da área com essa direção, obtemos o **elemento de área vetorial**. O vetor dA aponta para fora e tem módulo igual à área do pedacinho.

### G04 — produto escalar e fluxo local
**Evento visual:** \(\mathbf E\) e \(d\mathbf A\) se combinam em \(\mathbf E\cdot d\mathbf A\).

> No mesmo ponto existe o campo elétrico. O produto escalar entre o campo elétrico e o elemento de área vetorial mede quanto do campo atravessa aquele pedaço de superfície. Se o campo atravessa de frente, a contribuição é máxima. Se o campo corre tangente à superfície, essa contribuição é zero.

### G05 — integral de fluxo
**Evento visual:** patches se acumulam e viram \(\oint_S\mathbf E\cdot d\mathbf A\).

> Fazemos isso para todos os pedacinhos e somamos. No limite de pedacinhos infinitesimais, a soma vira uma integral sobre a superfície fechada. Essa integral é o **fluxo elétrico total** através da superfície.

### G06 — carga envolvida
**Evento visual:** cubo/volume com cargas; surge \(Q_{\rm env}\).

> A Lei de Gauss conecta esse fluxo a uma quantidade física muito simples: a **carga envolvida**. Não importa como essa carga está distribuída dentro da superfície; o fluxo líquido total depende da carga líquida que ficou lá dentro.

### G07 — discreto para contínuo
**Evento visual:** cargas discretas tornam-se distribuição; \(Q_{\rm env}\to\int_V\rho\,dV\).

> Se a carga estiver espalhada continuamente, em vez de somar partículas uma por uma usamos a **densidade volumétrica de carga**, rô. Rô responde: quanta carga existe por unidade de volume em torno daquele ponto? Num elemento de volume dV, a carga é aproximadamente rô vezes dV. Somando o volume inteiro, a carga envolvida vira a integral de rô dV.

### G08 — a forma integral e a pergunta local
**Evento visual:** \(\oint_S\mathbf E\cdot d\mathbf A=(1/\varepsilon_0)\int_V\rho\,dV\), depois foco em P.

> Então a Lei de Gauss diz: o fluxo do campo elétrico pela superfície fechada é igual a um sobre epsilon zero vezes a carga distribuída dentro do volume. Só que isso ainda é uma afirmação global. Ela fala do volume inteiro. O próximo passo é perguntar: como extrair dessa conta uma informação sobre um único ponto P?

---

# 3. DIVERGENTE — fluxo líquido por unidade de volume

### D01 — intervalo centrado em P
**Evento visual:** eixo x, ponto P, segmento total dx.

> Para enxergar o que acontece localmente, vamos construir um pequeno volume **centrado** no ponto P. Comece só pela direção x. O ponto P tem coordenada x, e ao redor dele escolhemos um intervalo muito pequeno de comprimento dx.

### D02 — por que \(x\pm dx/2\)
**Evento visual:** o intervalo divide-se em duas metades.

> Como o ponto está no centro, metade desse comprimento fica para cada lado. Por isso a face da esquerda está em x menos dx sobre dois, e a face da direita está em x mais dx sobre dois. Essas expressões não são um truque algébrico; são simplesmente as coordenadas das duas faces de um cubo centrado em P.

### D03 — construir o cubo e a face x
**Evento visual:** surgem dx, dy, dz e a face perpendicular a x.

> Agora dê espessura ao intervalo nas direções y e z. Nasce um cubinho diferencial. A face perpendicular ao eixo x tem lados dy e dz; portanto sua área é dy vezes dz.

### D04 — normais externas
**Evento visual:** normais \(\hat{\mathbf n}_+=+\hat{\mathbf x}\), \(\hat{\mathbf n}_-=-\hat{\mathbf x}\).

> Repara nas normais externas. Na face direita, a normal aponta no sentido positivo de x. Na face esquerda, aponta no sentido negativo. É a mesma direção geométrica, mas com sentidos opostos. Esse detalhe vai produzir o sinal de menos no fluxo líquido.

### D05 — fluxo da face direita
**Evento visual:** \(d\Phi_{x,+}=\mathbf E\cdot(+\hat x)\,dy\,dz\).

> Comecemos pela face direita. O fluxo através dela é o campo elétrico ponto o elemento de área vetorial. Como a normal dessa face aponta em x, o produto escalar seleciona justamente a **componente x do campo elétrico**. As outras componentes não atravessam essa face; elas correm paralelas a ela.

### D06 — por que avaliar em \(x+dx/2\)
**Evento visual:** o rótulo da coordenada da face é copiado para \(E_x\).

> E em que posição devemos avaliar essa componente? Na posição da própria face. A face direita está em x mais dx sobre dois. Por isso aparece a componente x do campo elétrico avaliada em x mais dx sobre dois, multiplicada pela área dy dz.

### D07 — fluxo da face esquerda
**Evento visual:** face esquerda, normal negativa.

> Na face esquerda acontece o mesmo, mas a normal externa aponta para menos x. O produto escalar traz um sinal negativo. A componente do campo é avaliada agora em x menos dx sobre dois, que é a posição dessa face.

### D08 — fluxo líquido em x
**Evento visual:** as duas contribuições se unem.

> O fluxo líquido associado ao par de faces em x é a contribuição da direita mais a contribuição da esquerda. Como a esquerda já carrega o sinal da normal, o resultado fica como a diferença entre os valores da componente x do campo nas duas faces, vezes dy dz.

### D09 — a razão de diferenças
**Evento visual:** multiplicar/dividir por dx; aparece gráfico \(E_x\times x\).

> Agora vem o passo que transforma geometria em cálculo. Multiplique e divida essa diferença por dx. O que aparece no numerador é a variação da componente x do campo entre duas posições muito próximas. No denominador está a distância entre essas posições.

### D10 — secante para tangente
**Evento visual:** secante converge para tangente, \(dx\to0\).

> No gráfico da componente x do campo em função de x, essa razão é a inclinação média entre as duas faces: a inclinação de uma secante. Quando fazemos dx tender a zero, as duas faces se aproximam do ponto P, a secante vira tangente, e a inclinação média vira uma derivada.

### D11 — por que derivada parcial
**Evento visual:** \(\partial E_x/\partial x\), com y e z fixos.

> É uma **derivada parcial** porque estamos variando x enquanto mantemos y e z fixos. Então essa razão de diferenças tende à derivada parcial da componente x do campo elétrico em relação a x.

### D12 — reconhecer o volume
**Evento visual:** \(dx\,dy\,dz=dV\).

> O resto da expressão é dx vezes dy vezes dz. Mas isso é exatamente o pequeno volume do cubo: dV. Portanto, a contribuição das faces x para o fluxo líquido é a derivada parcial de E x em relação a x, vezes dV.

### D13 — contribuições y e z
**Evento visual:** o mesmo cubo destaca pares de faces y e z.

> Agora repita o mesmo raciocínio nos outros dois pares de faces. Nas faces perpendiculares a y, a contribuição depende de quanto a componente y do campo muda na direção y. Nas faces perpendiculares a z, depende de quanto a componente z muda na direção z.

### D14 — fluxo total
**Evento visual:** \(d\Phi=d\Phi_x+d\Phi_y+d\Phi_z\).

> O fluxo líquido total do cubinho é a soma dessas três contribuições. Isso é importante: não estamos somando “as componentes do campo”. Estamos somando **as taxas de saída** associadas a cada direção.

### D15 — definição do divergente
**Evento visual:** a soma das três derivadas recebe o nome \(\nabla\cdot\mathbf E\).

> A soma da derivada parcial de E x em x, de E y em y e de E z em z recebe um nome: **divergente do campo elétrico**. O divergente é, portanto, a taxa de fluxo líquido que sai de um volume infinitesimal por unidade de volume.

### D16 — definição geométrica local
**Evento visual:** \(\nabla\cdot\mathbf E=\lim_{\Delta V\to0}\frac{1}{\Delta V}\oint_{\partial V}\mathbf E\cdot d\mathbf A\).

> Essa interpretação é mais importante que decorar a fórmula em coordenadas. Pegue um volume pequeno em torno do ponto, calcule quanto campo líquido sai pela sua fronteira, divida pelo volume e faça o volume encolher. O limite é o divergente naquele ponto.

### D17 — positivo, negativo e zero
**Evento visual:** mesmo cubo em três regimes.

> Se sai mais campo do que entra, o divergente é positivo: comportamento de fonte. Se entra mais do que sai, é negativo: comportamento de sumidouro. Se entra exatamente o que sai, o divergente é zero.

### D18 — zero não significa campo zero
**Evento visual:** campo uniforme atravessando o cubo.

> E cuidado: divergente zero não quer dizer campo elétrico zero. Um campo uniforme pode atravessar o cubo inteiro com intensidade diferente de zero e, mesmo assim, ter fluxo líquido nulo, porque tudo o que entra de um lado sai do outro.

---

# 4. TEOREMA DA DIVERGÊNCIA — por que o interior cancela

### T01 — dois volumes vizinhos
**Evento visual:** dois cubos compartilham uma face.

> Agora coloque dois pequenos volumes lado a lado. Eles compartilham a mesma face interna. Para o volume da esquerda, essa face tem normal apontando para um lado. Para o volume da direita, a normal externa aponta exatamente para o lado oposto.

### T02 — cancelamento da face comum
**Evento visual:** \(+\Phi\) e \(-\Phi\) se cancelam.

> O campo atravessando essa interface é o mesmo. O que conta como fluxo saindo de um volume conta como fluxo entrando no vizinho. Por isso a mesma contribuição aparece uma vez com sinal positivo e outra com sinal negativo. Na soma, cancela.

### T03 — muitos volumes
**Evento visual:** 2 → 4 → 8 → grade/bloco.

> Se dividirmos um volume grande em muitos cubinhos, isso acontece em todas as interfaces internas. Cada face compartilhada aparece duas vezes, com normais opostas. Uma a uma, as contribuições internas desaparecem da soma.

### T04 — sobra a fronteira
**Evento visual:** fronteira externa destacada.

> O que não tem parceiro para cancelar? Só a fronteira externa. Então somar o divergente em todos os pequenos volumes internos é equivalente a somar o fluxo apenas pela superfície externa do volume total.

### T05 — passagem às integrais
**Evento visual:** somas viram integrais.

> Quando as células ficam infinitesimais, a soma do divergente vezes o pequeno volume vira uma integral de volume. E a soma do fluxo pelas faces externas vira a integral de superfície fechada do campo elétrico ponto dA.

### T06 — teorema da divergência
**Evento visual:** igualdade final.

> Essa igualdade é o **teorema da divergência**: o fluxo através da fronteira é igual à soma, no interior, de todas as fontes e sumidouros locais medidos pelo divergente. É uma ponte direta entre o global e o local.

---

# 5. LEI DE GAUSS DIFERENCIAL

### L01 — mesmo fluxo, duas leituras
**Evento visual:** teorema da divergência e Lei de Gauss lado a lado.

> Agora temos duas maneiras de escrever o mesmo fluxo. Pela matemática, o fluxo é a integral do divergente no volume. Pela Lei de Gauss, o mesmo fluxo é a integral da densidade de carga dividida por epsilon zero.

### L02 — igualar os volumes
**Evento visual:** os lados de volume se aproximam.

> Como os dois lados representam a mesma quantidade, podemos igualar as integrais de volume. E essa igualdade não depende de um volume específico: ela vale para qualquer volume regular que escolhermos.

### L03 — localizar
**Evento visual:** volume encolhe em torno de um ponto.

> Se duas integrais são iguais para qualquer volume, inclusive volumes arbitrariamente pequenos em torno de qualquer ponto, então os integrandos precisam coincidir ponto a ponto. É exatamente aí que a lei global se torna local.

### L04 — payoff de Gauss diferencial
**Evento visual:** \(\boxed{\nabla\cdot\mathbf E=\rho/\varepsilon_0}\).

> Chegamos à Lei de Gauss na forma diferencial: o divergente do campo elétrico, em cada ponto, é igual à densidade volumétrica de carga naquele ponto dividida por epsilon zero. Carga positiva produz divergente positivo. Carga negativa produz divergente negativo. A carga é a fonte local do campo elétrico.

---

# 6. EXEMPLO — campo que cresce linearmente

### K01 — apresentar kappa
**Evento visual:** \(\mathbf E=\kappa(x\hat x+y\hat y+z\hat z)\).

> Veja um exemplo simples. O campo elétrico é kappa vezes x na direção x, mais kappa vezes y na direção y, mais kappa vezes z na direção z. Kappa é uma **constante escalar**: ela controla o quanto o campo cresce quando nos afastamos da origem.

### K02 — derivadas das componentes
**Evento visual:** eixos x, y e z; cada derivada dá kappa.

> A componente x é kappa x, então sua derivada parcial em relação a x é kappa. A componente y é kappa y, então a derivada em y também é kappa. E o mesmo vale para z.

### K03 — interpretar o resultado
**Evento visual:** \(\nabla\cdot\mathbf E=3\kappa\), depois \(\rho=3\varepsilon_0\kappa\).

> Somando as três contribuições, o divergente vale três kappa em todo ponto. Pela Lei de Gauss diferencial, isso corresponde a uma densidade de carga uniforme, rô igual a três epsilon zero kappa. O exemplo mostra que o divergente não é uma abstração separada da física: ele mede diretamente a densidade de fonte necessária para produzir aquele padrão de campo.

---

# 7. CARGA PONTUAL E DELTA DE DIRAC

### P01 — campo coulombiano
**Evento visual:** campo de uma carga pontual.

> Agora vem o caso que força a gente a ser mais cuidadoso: uma carga pontual. O campo elétrico de Coulomb é q sobre quatro pi epsilon zero, vezes o vetor radial unitário dividido por r ao quadrado. Fora da origem, se calcularmos o divergente desse campo, o resultado é zero.

### P02 — cubo de teste fora da origem
**Evento visual:** cubo percorre diferentes posições.

> Isso faz sentido localmente. Coloque um cubinho em qualquer ponto que não seja a posição da carga. O campo pode ser forte, fraco, variar de direção, mas o fluxo líquido daquele cubinho tende a zero. Não existe carga dentro dele.

### P03 — esfera gaussiana e fluxo constante
**Evento visual:** esfera em torno da carga; \(\Phi_E=q/\varepsilon_0\).

> Só que uma superfície fechada que envolve a carga sempre tem fluxo q sobre epsilon zero. E isso continua verdadeiro se a esfera for ficando menor.

### P04 — por que o fluxo não muda
**Evento visual:** raio diminui enquanto o fluxo permanece constante.

> Quando o raio diminui, o campo na superfície aumenta como um sobre r ao quadrado. Ao mesmo tempo, a área da esfera diminui como r ao quadrado. Um efeito compensa exatamente o outro. O fluxo permanece constante, mesmo quando a superfície é comprimida em torno da carga.

### P05 — conflito
**Evento visual:** \(\nabla\cdot\mathbf E=0\) para \(r\neq0\) versus fluxo não nulo.

> Então aparece o conflito: o divergente é zero em todos os pontos fora da origem, mas qualquer superfície que envolva a origem detecta uma fonte finita. A fonte inteira foi concentrada num único ponto.

### P06 — motivar a delta
**Evento visual:** título Delta de Dirac tridimensional.

> Para representar matematicamente uma fonte pontual, precisamos de um objeto que seja zero fora da origem, mas cuja integral consiga guardar um valor finito exatamente ali. Esse objeto é a **delta de Dirac tridimensional**, escrita delta superscrito três de r vetor.

### P07 — o que a delta é
**Evento visual:** volume fora e dentro da origem.

> A delta não deve ser pensada como uma função comum com um valor “muito alto” na origem. Ela é uma **distribuição**: o jeito correto de entendê-la é pelo que ela faz dentro de integrais. Se um volume não contém a origem, a integral da delta nesse volume é zero. Se a origem está no interior do volume, a integral vale um.

### P08 — propriedade de amostragem
**Evento visual sugerido:** pequena função de teste ou apenas destaque no valor da origem.

> Uma forma ainda mais útil de dizer isso é: quando multiplicamos a delta por uma função suave e integramos, a delta seleciona o valor dessa função na origem. Em símbolos, a integral de f de r vezes delta tridimensional de r devolve f de zero. Ela funciona como um seletor idealizado de um único ponto.

### P09 — densidade de uma carga pontual
**Evento visual:** \(\rho(\mathbf r)=q\delta^{(3)}(\mathbf r)\).

> Agora multiplique essa distribuição pela carga q. A densidade de carga fica rô de r igual a q vezes delta de Dirac tridimensional. Fora da origem, a densidade é zero. Mas se integrarmos em qualquer volume que contenha a origem, recuperamos exatamente a carga total q.

### P10 — resolver Gauss diferencial
**Evento visual:** substituir \(\rho\) na Lei de Gauss diferencial.

> Substituindo essa densidade na Lei de Gauss diferencial, o divergente do campo da carga pontual é q sobre epsilon zero vezes a delta de Dirac tridimensional. O aparente paradoxo desaparece: o divergente é zero em todo lugar regular e toda a fonte fica concentrada na origem.

### P11 — conexão sem desvio excessivo
**Evento visual:** hold curto antes da próxima seção.

> Essa mesma ferramenta reaparece sempre que a física idealiza algo concentrado num ponto: uma massa pontual na gravitação, uma força impulsiva no tempo, uma fonte localizada. A ideia é sempre a mesma: zero quase em toda parte, mas efeito integral finito.

---

# 8. DIVERGENTE NÃO DETERMINA A GEOMETRIA — entra o rotacional

### R01 — campo uniforme F1
**Evento visual:** \(\mathbf F_1=F_0\hat x\), divergente zero.

> Saber o divergente ainda não conta toda a história geométrica de um campo. Considere primeiro um campo uniforme, F um: todas as setas têm o mesmo tamanho e apontam na direção x. O que entra em um pequeno volume é exatamente o que sai. O divergente é zero.

### R02 — construir F2 e explicar ômega
**Evento visual:** quatro vetores tangenciais e parâmetro \(\Omega\).

> Agora construa um campo completamente diferente. Em cada ponto, a seta é tangente a um círculo em torno da origem. O parâmetro ômega maiúsculo é uma constante escalar que controla a intensidade desse campo giratório. Se F fosse um campo de velocidades de um corpo em rotação rígida, ômega teria o papel de uma velocidade angular.

### R03 — entender \(-y\hat x+x\hat y\)
**Evento visual:** vetores em quatro posições cardeais.

> Olha os quatro pontos principais. À direita da origem, o vetor aponta para cima. Acima, aponta para a esquerda. À esquerda, aponta para baixo. Abaixo, aponta para a direita. É exatamente o padrão produzido por menos y na direção x mais x na direção y: sempre tangente aos círculos.

### R04 — mesmo divergente
**Evento visual:** \(\nabla\cdot\mathbf F_1=0\), \(\nabla\cdot\mathbf F_2=0\).

> E aqui está a surpresa: o divergente desse campo também é zero. Então dois campos com geometrias completamente diferentes podem ter o mesmo divergente. O divergente detecta fonte e sumidouro; ele não mede giro.

### R05 — sonda de giro
**Evento visual:** rodinha parada em F1 e girando em F2.

> Para enxergar a diferença, imagine uma pequena roda de pás usada apenas como sonda geométrica. No campo uniforme, não existe tendência líquida de rotação. No campo giratório, a roda tende a girar. Precisamos de um segundo operador para medir isso.

### R06 — rotacional
**Evento visual:** surge \(\nabla\times\mathbf F\).

> Esse operador é o **rotacional**. Ele é um vetor: seu módulo mede a intensidade da tendência local de giro e sua direção dá o eixo desse giro, pela regra da mão direita.

### R07 — F2
**Evento visual:** \(\nabla\times\mathbf F_2=2\Omega\hat z\).

> Para este campo específico, o rotacional vale dois ômega na direção z positiva. O fator dois é característico desse padrão de rotação rígida. O ponto importante não é decorar o resultado: é perceber que o rotacional distingue imediatamente o campo giratório do campo uniforme, embora os dois tenham divergente zero.

### R08 — pergunta para E
**Evento visual:** F transforma em E.

> Agora podemos fazer a pergunta física: e o campo elétrico eletrostático, produzido por cargas paradas? Ele pode ter circulação local, ou o seu rotacional é zero? Para responder, vamos primeiro estudar a circulação ao longo de um caminho.

---

# 9. CIRCULAÇÃO DO CAMPO ELETROSTÁTICO

### C01 — caminho de a até b
**Evento visual:** carga, pontos a e b, raios \(r_a\), \(r_b\), caminho \(C_1\).

> Pegue uma carga pontual e dois pontos, a e b. A distância da carga até a é r a; até b é r b. Agora escolha qualquer caminho C um ligando esses dois pontos.

### C02 — elemento de linha e significado físico
**Evento visual:** tracer com \(d\boldsymbol\ell\) tangente e \(\mathbf E\) no mesmo ponto.

> Ao caminhar por essa curva, o deslocamento infinitesimal d ell é sempre tangente ao caminho. Em cada ponto fazemos o produto escalar entre o campo elétrico e d ell. Integrar esse produto ao longo do caminho significa acumular o quanto o campo favorece ou se opõe ao deslocamento. Fisicamente, essa integral é o **trabalho do campo por unidade de carga** entre os dois pontos.

### C03 — decomposição radial/transversal
**Evento visual:** \(d\boldsymbol\ell\) dividido em componente radial e transversal.

> No campo de uma carga pontual, o campo elétrico aponta radialmente. Então só a componente radial do deslocamento contribui para o produto escalar. A parte transversal é perpendicular ao campo e tem produto escalar zero. A componente radial é simplesmente dr, a pequena variação da distância até a carga.

### C04 — montar a integral
**Evento visual:** \(\mathbf E\cdot d\boldsymbol\ell=\frac{q}{4\pi\varepsilon_0r^2}dr\), depois integral em r.

> Por isso o produto escalar vira q sobre quatro pi epsilon zero, vezes dr sobre r ao quadrado. Ao integrar do ponto a até o ponto b, a variável radial vai de r a até r b.

### C05 — antiderivada e resultado
**Evento visual:** \(\int dr/r^2\to 1/r_a-1/r_b\).

> A primitiva de um sobre r ao quadrado é menos um sobre r. Avaliando nos extremos, o resultado fica proporcional a um sobre r a menos um sobre r b. Repara no que desapareceu: a forma detalhada do caminho.

### C06 — segundo caminho
**Evento visual:** surge \(C_2\) com os mesmos extremos.

> Escolha agora um segundo caminho, completamente diferente, mas com os mesmos pontos inicial e final. Como r a e r b são os mesmos, o valor da integral também é o mesmo.

### C07 — campo conservativo
**Evento visual:** igualdade entre integrais de \(C_1\) e \(C_2\).

> Essa independência do caminho é a marca de um campo conservativo. Em mecânica, é a mesma ideia da força gravitacional ou da força elástica ideal: o trabalho entre dois pontos depende dos extremos, não do trajeto usado para chegar lá.

### C08 — fechar o caminho
**Evento visual:** \(C=C_1-C_2\), tracer completa volta.

> Faça então a ida por C um e a volta pelo caminho C dois percorrido no sentido contrário. Juntos, eles formam uma curva fechada. A contribuição da volta entra com sinal oposto e cancela a contribuição da ida.

### C09 — circulação fechada zero
**Evento visual:** \(\boxed{\oint_C\mathbf E\cdot d\boldsymbol\ell=0}\).

> Portanto, em eletrostática, a circulação do campo elétrico ao redor de qualquer caminho fechado regular é zero. Em linguagem de trabalho: depois de uma volta completa, o campo não fornece trabalho líquido por unidade de carga.

### C10 — ponte para potencial
**Evento visual:** hold curto.

> Guarda essa conclusão, porque ela vai reaparecer no final: se a integral entre dois pontos independe do caminho, podemos descrever essa diferença usando um potencial escalar.

---

# 10. STOKES — da borda ao giro local

### S01 — curva fechada genérica
**Evento visual:** curva C e campo genérico F, d ell tangente.

> Antes de voltar ao campo elétrico, vamos formular a ponte matemática para um campo vetorial qualquer F. Na borda C, a circulação é a integral de F ponto d ell ao longo da curva fechada.

### S02 — preencher a borda com uma superfície
**Evento visual:** surge superfície S delimitada por C.

> Agora preencha essa curva com uma superfície S. Pense numa película esticada sobre um aro. A curva é a borda; a superfície é o interior.

### S03 — pequenos loops e cancelamento interno
**Evento visual:** pequenos rotores/loops nos patches.

> Divida mentalmente essa superfície em muitos pedacinhos. Em cada pedacinho, uma circulação microscópica mede a tendência local de giro. Quando colocamos os pedacinhos lado a lado, as bordas internas aparecem duas vezes, percorridas em sentidos opostos. Elas se cancelam. Exatamente como as faces internas se cancelaram no teorema da divergência, aqui as bordas internas das pequenas células cancelam entre si.

### S04 — o que o rotacional representa
**Evento visual:** pequenos rotores tornam-se vetores \(\nabla\times\mathbf F\), com normal.

> O rotacional condensa essa circulação local em um vetor. A componente do rotacional na direção normal à superfície mede, no limite, a circulação por unidade de área de um loop muito pequeno naquele ponto. É por isso que o eixo do pequeno giro e a normal do patch aparecem juntos.

### S05 — contribuição do patch
**Evento visual:** \((\nabla\times\mathbf F)\cdot d\mathbf A\).

> Para um pequeno elemento de área, a contribuição é o rotacional ponto o elemento de área vetorial. O produto escalar seleciona justamente a parte do rotacional que atravessa aquele patch na direção da normal.

### S06 — integrar o interior
**Evento visual:** soma dos patches vira \(\int_S(\nabla\times\mathbf F)\cdot d\mathbf A\).

> Somando todos os patches e tomando o limite, obtemos a integral de superfície do rotacional. As bordas internas desapareceram por cancelamento; sobra apenas a circulação na borda externa C.

### S07 — Teorema de Stokes
**Evento visual:** igualdade completa.

> Esse é o **teorema de Stokes**: a circulação do campo ao longo da borda C é igual ao fluxo do rotacional através de qualquer superfície S que tenha C como borda, desde que o campo seja regular na região. Borda e interior são duas leituras da mesma estrutura geométrica.

### S08 — aplicar ao campo eletrostático
**Evento visual:** F transforma em E; rotores param.

> Agora troque o campo genérico F pelo campo elétrico eletrostático. A gente acabou de demonstrar que a circulação do campo elétrico em qualquer curva fechada é zero. Portanto, a integral de superfície do rotacional do campo elétrico também é zero.

### S09 — localizar Stokes
**Evento visual:** selecionar pequena superfície regular e variar orientação.

> Escolha uma superfície muito pequena numa região onde o campo é regular — sem atravessar a posição singular de uma carga pontual. Se a integral é zero para qualquer pequeno patch e para qualquer orientação da normal, não basta uma componente do rotacional ser zero: o vetor inteiro precisa ser zero.

### S10 — payoff do rotacional
**Evento visual:** \(\boxed{\nabla\times\mathbf E=0}\).

> Chegamos à segunda equação local da eletrostática: o rotacional do campo elétrico é zero. O campo eletrostático é **irrotacional**. Isso não quer dizer que suas linhas precisam ser retas; quer dizer que não existe circulação local líquida.

---

# 11. MAPA FINAL — duas perguntas, duas leis

### M01 — fontes
**Evento visual:** ramo do divergente.

> Agora dá para resumir a eletrostática em duas perguntas. Primeira: existe fonte local? A resposta está no divergente. A Lei de Gauss diferencial diz que o divergente do campo elétrico é a densidade de carga dividida por epsilon zero.

### M02 — circulação
**Evento visual:** ramo do rotacional.

> Segunda: existe circulação local? A resposta está no rotacional. Em eletrostática, o rotacional do campo elétrico é zero.

### M03 — global para local
**Evento visual:** mapa conecta Gauss e Stokes.

> E repara na simetria do raciocínio. Gauss transforma uma informação de fluxo na fronteira em uma afirmação sobre fontes no interior. Stokes transforma uma informação de circulação na borda em uma afirmação sobre giro local no interior. Nos dois casos, uma lei global ganha uma forma local.

---

# 12. FARADAY E POTENCIAL — a porta para o próximo vídeo

### F01 — Faraday geral
**Evento visual:** \(\nabla\times\mathbf E=-\partial\mathbf B/\partial t\), B varia.

> Mas o rotacional do campo elétrico não é zero em toda situação da eletrodinâmica. A forma geral é a lei de Faraday: o rotacional do campo elétrico é igual a menos a derivada temporal do campo magnético. Um campo magnético que muda com o tempo produz um campo elétrico com circulação. É a base da indução eletromagnética.

### F02 — regime eletrostático
**Evento visual:** B congela, \(\partial\mathbf B/\partial t\to0\).

> No regime eletrostático, os campos não variam no tempo. Em particular, a derivada do campo magnético em relação ao tempo é zero. A lei de Faraday então reduz exatamente ao resultado que encontramos: rotacional do campo elétrico igual a zero.

### F03 — diferença de potencial
**Evento visual:** equipotenciais \(V_1,V_2,V_3\).

> E lembra da circulação? Como a integral do campo entre dois pontos independe do caminho, podemos definir uma grandeza escalar chamada **potencial elétrico**. A diferença de potencial entre dois pontos é o negativo da integral do campo elétrico ao longo de qualquer caminho ligando esses pontos.

### F04 — gradiente
**Evento visual:** \(\nabla V\) normal às equipotenciais, \(\mathbf E\) em sentido oposto.

> O potencial atribui um número a cada ponto do espaço. As superfícies em que esse número é constante são as equipotenciais. O gradiente do potencial aponta para a direção em que o potencial cresce mais rapidamente. O campo elétrico aponta no sentido oposto, para onde o potencial cai mais rapidamente.

### F05 — teaser final
**Evento visual:** \(\boxed{\mathbf E=-\nabla V}\).

> Por isso o campo elétrico pode ser escrito como menos o gradiente do potencial. É uma simplificação poderosa: em vez de procurar diretamente um vetor com três componentes, muitas vezes podemos primeiro encontrar um único campo escalar. E essa é a próxima ideia que vale construir com calma: o potencial elétrico.

---

# 13. PAYOFF E CTA

### CTA01 — payoff
**Evento visual:** divergente e rotacional lado a lado.

> Hoje a gente saiu de duas perguntas geométricas e chegou às duas leis locais da eletrostática. Divergente mede fonte local. Rotacional mede circulação local. Para o campo elétrico eletrostático, a fonte é a densidade de carga e a circulação local é zero.

### CTA02 — encerramento
**Evento visual:** CTA no padrão dos episódios 1 e 2.

> Se essa construção te ajudou a enxergar o que essas equações realmente querem dizer, se inscreve no canal. No próximo passo, a gente usa exatamente esse caráter conservativo para construir o potencial elétrico. Até a próxima.

---

## Notas de implementação das âncoras

1. Cada âncora deve começar no evento visual descrito e a cena deve aguardar o término da fala antes de avançar para o próximo evento conceitual.
2. Não sincronizar a voz por timestamps absolutos do preview V1.7; sincronizar por IDs/eventos.
3. Um mesmo anchor pode conter várias microanimações que ilustrem a fala. Não congelar a tela enquanto o texto continua explicando.
4. Para TTS, preservar frases completas por âncora; evitar cortar respirações no meio de uma dedução.
5. A sequência da diferença finita para derivada, a delta de Dirac, a circulação e Stokes devem receber mais tempo visual do que no preview atual.
6. Na delta, evitar a frase “a delta vale infinito na origem”. A versão correta aqui é operacional: distribuição definida pelo seu efeito sob integrais.
7. Na mecânica quântica, evitar dizer que a delta “é uma partícula perfeitamente localizada” como afirmação física literal; se houver gancho, falar em idealizações/localizações pontuais ou estados de posição generalizados.
8. Em Faraday, dizer “no regime eletrostático os campos não variam no tempo”, em vez de inferir apenas de “cargas paradas”.
