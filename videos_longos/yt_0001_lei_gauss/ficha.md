# yt_0001 — LEI DE GAUSS

**O segredo não é a integral — é a simetria**

## STATUS

`REVISÃO 2 — SEGUNDO PREVIEW HORIZONTAL`

A Produção aprovou o conteúdo em 2026-10-03 (preview 1). Em 2026-10-04, a análise crítica do preview 1
autorizou uma revisão localizada: construção da normal e do vetor área, retomada das coordenadas
esféricas, uma operação por transformação, domínios das fórmulas, regiões que contribuem nas simetrias
clássicas, terminologia (carga envolvida, `Q_{\mathrm{env}}`, cilindro gaussiano curto), consistência de
cores, caminhos alternativos quando Gauss não simplifica, ritmo e tela final.

Continuam preservados: tese; pergunta central; sequência didática; cold open; apresentação do canal;
exemplo da esfera uniforme; payoff científico separado do CTA. Fora do escopo autorizado, a implementação
não redesenha o conteúdo.

> Nota de transcrição (2026-10-03): no texto colado da ficha Master, várias equações chegaram sem o lado
> esquerdo e sem `\boxed`. Foram restaurados só os lados esquerdos óbvios e o destaque em caixa; as
> formas canônicas foram confirmadas pela Produção. Patch textual aprovado aplicado na narração (seção 12):
> frase da equivalência externa.

## 1. IDENTIDADE

- ID: `yt_0001`
- Slug: `yt_0001_lei_gauss`
- formato: `longo_horizontal`
- natureza: `teoria_visual`
- Curso: `Física III`
- Eixo: `Eletricidade e Magnetismo`
- macroassunto: `eletromagnetismo`
- Módulo: `Lei de Gauss`
- Destino: `YouTube long-form`
- Aspect ratio: `16:9`
- Preview: `960×540 / 15 fps`
- Final planejado: `1920×1080 / 30 fps`
- Duração: preview 1 com 11:57; a revisão 2 acrescenta a construção da normal, as coordenadas esféricas
  e os caminhos alternativos, e fica mais longa. Não encurtar conteúdo físico necessário para perseguir
  duração artificial.

## 2. TÍTULO

Título de trabalho aprovado:

**LEI DE GAUSS: O SEGREDO NÃO É A INTEGRAL — É A SIMETRIA**

Alternativa editorial: *Lei de Gauss: quando ela realmente encontra o campo elétrico?*

O título não deve ser alterado durante a implementação.

## 3. TESE

A Lei de Gauss determina o fluxo elétrico através de qualquer superfície fechada; é a simetria da
distribuição de carga que, em situações especiais, transforma essa informação global numa equação
simples para o campo elétrico.

## 4. PERGUNTA CENTRAL

Quando a Lei de Gauss realmente permite calcular o campo elétrico, e por que escolher qualquer
superfície fechada não basta?

## 5. PAYOFF

A Lei de Gauss fala sobre fluxo.
É a simetria da fonte que transforma fluxo em campo.

## 6. HIPÓTESES

- Trabalhar em eletrostática.
- Superfícies gaussianas são superfícies matemáticas fechadas e orientáveis.
- O vetor área de uma superfície fechada utiliza a normal exterior.
- Nenhuma carga pontual singular será colocada exatamente sobre a superfície de integração.
- A simetria discutida refere-se às fontes analisadas e ao campo produzido por elas.
- Fontes das simetrias clássicas são idealizadas: linha infinita uniforme, plano infinito uniforme.
- Na esfera uniforme: $\rho>0$ é constante para $r<R$.
- Não existe camada superficial singular adicional em $r=R$.

## 7. PRÉ-REQUISITOS

O espectador já conhece em nível introdutório:

- campo elétrico de carga pontual;
- vetores;
- princípio de superposição;
- produto escalar;
- integral como soma contínua.

Vetor área, fluxo, integral de superfície e coordenadas esféricas serão reconstruídos visualmente.

## 8. EQUAÇÕES CANÔNICAS

Área escalar, normal unitária e vetor área:
$$dA,\qquad |\hat n|=1,\qquad d\vec A=\hat n\,dA.$$

Fluxo diferencial ($\theta$ = ângulo entre $\vec E$ e $\hat n$):
$$d\Phi_E=\vec E\cdot d\vec A=E\,dA\cos\theta.$$

Campo de carga pontual:
$$\vec E=\frac{q}{4\pi\varepsilon_0r^2}\hat r.$$

Ângulo sólido orientado:
$$d\Omega_{\rm or}=\frac{\cos\theta\,dA}{r^2}.$$

Lei de Gauss ($Q_{\mathrm{env}}$ = carga envolvida: soma algébrica das cargas no interior da superfície):
$$\boxed{\oint_S\vec E\cdot d\vec A=\frac{Q_{\mathrm{env}}}{\varepsilon_0}}.$$

Simetria esférica:
$$\vec E(\vec r)=E(r)\hat r.$$

Elemento de volume esférico ($\vartheta$ = ângulo polar, distinto do $\theta$ do fluxo):
$$dV=dr'\cdot r'\,d\vartheta\cdot r'\sin\vartheta\,d\phi=r'^2\sin\vartheta\,dr'\,d\vartheta\,d\phi.$$

Esfera uniforme, carga envolvida:
$$Q_{\mathrm{env}}(r)=\frac43\pi\rho r^3,\qquad r<R.$$

Campo interior:
$$\boxed{E(r)=\frac{\rho r}{3\varepsilon_0}},\qquad r<R.$$

Carga total:
$$Q=\frac43\pi R^3\rho.$$

Campo exterior:
$$\boxed{E(r)=\frac{1}{4\pi\varepsilon_0}\frac{Q}{r^2}=\frac{\rho R^3}{3\varepsilon_0r^2}},\qquad r>R.$$

Fronteira:
$$\boxed{E(R)=\frac{\rho R}{3\varepsilon_0}}.$$

Limites:
$$E(0)=0\qquad\text{e}\qquad E(r)\to0\quad(r\to\infty).$$

## 9. ARQUITETURA EDITORIAL

A ordem definitiva é:

COLD OPEN → INTRO HUMANA CURTA → AULA → PAYOFF CIENTÍFICO → PAUSA → CTA / END SCREEN

Não começar com saudação. O problema físico deve aparecer antes do branding.

## 10. ESTRUTURA TEMPORAL

Referência do preview 1 (guia; a revisão 2 alonga os blocos 3, 5, 8, 10 e 11):

| Tempo (preview 1) | Bloco |
| --- | --- |
| 0:00–0:30 | Cold open / paradoxo |
| 0:30–0:43 | Intro do Parallax Lab |
| 0:43–2:08 | Fluxo e vetor área |
| 2:08–3:23 | Coulomb + esfera |
| 3:23–4:33 | Ângulo sólido + Lei de Gauss |
| 4:33–5:31 | Lei verdadeira ≠ campo resolvido |
| 5:31–6:28 | Simetria da fonte |
| 6:28–8:33 | Esfera uniforme |
| 8:33–9:18 | Gráfico sincronizado |
| 9:18–10:08 | Esfera × linha × plano |
| 10:08–11:08 | Quando Gauss ajuda + método de decisão |
| 11:08–11:38 | Retorno aos casos + payoff |
| 11:38–11:40 | Pausa |
| 11:40–11:57 | CTA / end screen |

Os tempos não são rígidos. A voz final determina a sincronização definitiva.

## 11. DERIVAÇÕES

### 11.1 Fluxo

Um elemento de superfície tem área escalar $dA$. Seu plano tangente define a normal unitária $\hat n$,
perpendicular ao plano. O vetor área é

$$d\vec A=\hat n\,dA.$$

Numa superfície fechada, $\hat n$ é a normal exterior em cada ponto. Se $\theta$ é o ângulo entre o
campo e a normal (não o ângulo de 90° entre a normal e o plano tangente):

$$d\Phi_E=\vec E\cdot d\vec A=E\,dA\cos\theta.$$

Em uma superfície fechada:

$$\Phi_E=\oint_S\vec E\cdot d\vec A.$$

### 11.2 Carga pontual em esfera centrada

Pela Lei de Coulomb:

$$\vec E=\frac{q}{4\pi\varepsilon_0r^2}\hat r.$$

Numa esfera centrada, campo e normal se alinham ($d\vec A=\hat r\,dA$), logo $\vec E\cdot d\vec A=E\,dA$.
Como $E$ é igual em todos os pontos, sai da integral, e a soma dos elementos de área é a área da esfera:

$$\Phi_E=\oint_S\vec E\cdot d\vec A=\oint_SE\,dA=E\oint_SdA=E\,4\pi r^2=\frac q{\varepsilon_0}.$$

Interpretação obrigatória: o campo diminui como $1/r^2$, enquanto a área cresce como $r^2$.

### 11.3 Superfície arbitrária

$$d\Phi_E=\frac{q}{4\pi\varepsilon_0r^2}(\hat r\cdot\hat n)\,dA=\frac{q}{4\pi\varepsilon_0}\frac{\cos\theta\,dA}{r^2}.$$

$dA\cos\theta$ é a área projetada perpendicularmente à direção radial. Definir:

$$d\Omega_{\rm or}=\frac{\cos\theta\,dA}{r^2},\qquad d\Phi_E=\frac{q}{4\pi\varepsilon_0}\,d\Omega_{\rm or}.$$

Carga interna: $\oint_Sd\Omega_{\rm or}=4\pi$ (ângulo sólido de todas as direções do espaço, área da esfera
de raio 1). Carga externa: $\oint_Sd\Omega_{\rm or}=0$ — o mesmo cone corta dois elementos com contribuições
orientadas $-d\Omega$ e $+d\Omega$; o cancelamento é do fluxo, não do campo local.

Com superposição:

$$\boxed{\oint_S\vec E\cdot d\vec A=\frac{Q_{\mathrm{env}}}{\varepsilon_0}}.$$

### 11.4 Simetria esférica

Uma distribuição esfericamente simétrica é invariante por rotações ao redor do centro. Forma esférica,
sozinha, não basta: carga dependente da direção quebra a simetria. Consequentemente, para a fonte simétrica:

$$\vec E(\vec r)=E(r)\hat r.$$

Numa esfera concêntrica, $d\vec A=\hat r\,dA$ e $\vec E\cdot d\vec A=E(r)\,dA$. Como $r$ é constante sobre a
esfera:

$$\oint_S\vec E\cdot d\vec A=E(r)\oint_SdA=E(r)\,4\pi r^2.$$

Esse passo só é permitido depois de a simetria estabelecer a forma do campo.

### 11.5 Esfera uniforme — interior

Três raios distintos: $R$ (esfera física, fixo), $r$ (superfície gaussiana e ponto de observação),
$r'$ (variável de integração). Coordenadas esféricas: $r'$, ângulo polar $\vartheta$ (a partir do eixo $z$),
ângulo azimutal $\phi$. O ponto que varia $\phi$ percorre um círculo de raio $r'\sin\vartheta$.

$$dV=dr'\cdot r'\,d\vartheta\cdot r'\sin\vartheta\,d\phi=r'^2\sin\vartheta\,dr'\,d\vartheta\,d\phi.$$

Para $r<R$, só conta a carga dentro da gaussiana ($0\le r'\le r$):

$$Q_{\mathrm{env}}=\int_V\rho\,dV=\rho\int_0^r r'^2dr'\int_0^\pi\sin\vartheta\,d\vartheta\int_0^{2\pi}d\phi
=\rho\cdot\frac{r^3}{3}\cdot2\cdot2\pi=\frac43\pi\rho r^3.$$

Gauss, uma operação por passo:

$$E(r)\,4\pi r^2=\frac{1}{3\varepsilon_0}\,4\pi\rho r^3
\;\Rightarrow\;E(r)\,r^2=\frac{\rho r^3}{3\varepsilon_0}
\;\Rightarrow\;\boxed{E(r)=\frac{\rho r}{3\varepsilon_0}},\qquad r<R.$$

### 11.6 Exterior

Para $r>R$, a carga envolvida já é toda a carga: $Q_{\mathrm{env}}=Q=\frac43\pi R^3\rho$. Então:

$$E(r)\,4\pi r^2=\frac Q{\varepsilon_0}\;\Rightarrow\;E(r)=\frac{Q}{4\pi\varepsilon_0r^2}
\;\Rightarrow\;\boxed{E(r)=\frac{\rho R^3}{3\varepsilon_0r^2}},\qquad r>R.$$

Condição textual obrigatória: para pontos externos a toda a região ocupada por essa distribuição
esfericamente simétrica, o campo é igual ao produzido por uma carga pontual de carga total $Q$
colocada no centro.

### 11.7 Simetrias clássicas (sem resolver linha e plano por completo)

| Fonte idealizada | Superfície útil | Contribui | Fluxo nulo |
| --- | --- | --- | --- |
| esfericamente simétrica | esfera concêntrica | toda a superfície ($\vec E\parallel d\vec A$) | — |
| linha infinita uniforme | cilindro coaxial | lateral ($\vec E\parallel d\vec A$) | tampas ($\vec E\perp d\vec A$) |
| plano infinito uniforme | cilindro gaussiano curto | as duas tampas ($\vec E\parallel d\vec A$) | lateral ($\vec E\perp d\vec A$) |

### 11.8 Quando Gauss não simplifica: caminhos adequados

| Caso | Caminho |
| --- | --- |
| carga pontual deslocada | Coulomb diretamente, ou esfera centrada na carga |
| segmento finito | somar (integrar) contribuições de Coulomb ao longo do segmento |
| disco finito, no eixo | somar anéis concêntricos |
| distribuição irregular conhecida | integração de Coulomb, analítica ou numérica |
| condutores / condições de contorno | resolver o potencial (Laplace/Poisson) com as condições de contorno |

A Lei de Gauss continua válida em todos; nenhuma forma de superfície é proibida — só não permite a
simplificação desejada para o campo.

## 12. NARRAÇÃO FINAL

Olha esses dois problemas.

Nos dois, eu consigo desenhar uma superfície fechada e escrever exatamente a mesma Lei de Gauss.

No primeiro, a distribuição de carga é perfeitamente simétrica. Em poucos passos, o campo elétrico aparece.

No segundo, eu coloco uma carga fora do centro de uma esfera. A Lei de Gauss continua verdadeira. O fluxo continua perfeitamente determinado. E mesmo assim eu não consigo simplesmente descobrir o campo sobre a esfera.

Então o que mudou?

Fala, pessoal. Bem-vindos ao Parallax Lab.

Hoje a gente vai entender por que a Lei de Gauss resolve alguns problemas quase instantaneamente e, em outros, parece não ajudar.

E a chave para entender isso é a simetria.

E é justamente essa diferença que faz muita gente aprender a usar esferas e cilindros gaussianos sem realmente entender por quê.

Antes de responder, precisamos entender o que a Lei de Gauss está medindo.

Pegue um pedacinho muito pequeno de uma superfície. Sua área é um número: d A.

De tão pequeno, esse pedacinho praticamente coincide com um plano: o plano tangente naquele ponto.

A normal, n chapéu, é um vetor de comprimento um, perpendicular a esse plano.

Multiplicando a normal pela área, obtemos o vetor área. Ele aponta na direção da normal, e seu tamanho representa a área do pedacinho.

Numa superfície fechada, cada ponto tem a sua própria normal. E, por convenção, escolhemos sempre a normal que aponta para fora.

Agora coloque esse elemento num campo elétrico.

O ângulo que importa aqui não é o de noventa graus entre a normal e a superfície. É o ângulo teta entre o campo e a normal.

Se o campo atravessa a superfície de frente, a contribuição para o fluxo é máxima.

Se inclinarmos o elemento, a normal e o vetor área inclinam junto com ele.

Se o campo passa tangente à superfície, não atravessa aquele elemento. A contribuição é zero.

E se o campo aponta para dentro de uma superfície fechada, enquanto a normal aponta para fora, a contribuição é negativa.

É isso que o produto escalar está fazendo.

A integral fechada apenas repete essa soma por toda a superfície.

Ela não está contando literalmente linhas de campo. As linhas são uma representação. O fluxo é essa soma matemática de quanto do campo atravessa cada elemento de área.

Agora coloque uma carga pontual no centro de uma esfera.

Pela Lei de Coulomb, o campo aponta radialmente e seu módulo diminui com o quadrado da distância.

Na superfície da esfera, campo e vetor área apontam na mesma direção.

Além disso, todos os pontos estão à mesma distância da carga. Então o módulo do campo é igual em toda a esfera.

Nesse caso, podemos tirar E da integral.

O fluxo vira o campo multiplicado pela área da esfera.

E aqui acontece algo importante.

Quando aumentamos o raio, o campo cai como um sobre o raio ao quadrado.

Mas a área da esfera cresce como o raio ao quadrado.

Uma coisa compensa exatamente a outra.

Por isso, não importa qual esfera centrada na carga escolhamos: o fluxo total é sempre q dividido por épsilon zero.

Isso já sugere que o fluxo está capturando alguma coisa mais profunda do que o valor local do campo.

Mas a superfície precisa mesmo ser uma esfera?

Imagine agora um pequeno cone de direções partindo da carga.

Esse cone intercepta um pedaço de uma superfície arbitrária.

Se o pedaço está inclinado, entra um fator de projeção. Se está mais distante, sua área precisa crescer proporcionalmente ao quadrado da distância para ocupar o mesmo tamanho angular visto pela carga.

A combinação entre área, inclinação e distância define um pequeno ângulo sólido.

E o fluxo produzido pela carga através daquele pedaço depende exatamente desse ângulo sólido orientado.

Se a superfície fechada envolve a carga, todos esses pequenos ângulos sólidos completam quatro pi.

Quatro pi é o ângulo sólido de todas as direções do espaço: a área de uma esfera de raio um, e não a volta de um círculo.

O resultado continua sendo q dividido por épsilon zero, independentemente da forma da superfície.

Agora coloque a carga fora.

O campo sobre a superfície não desaparece.

Pode até ser muito intenso em alguns lugares.

Mas cada feixe que entra numa região da superfície volta a sair por outra. Com a orientação correta, as contribuições se cancelam no fluxo líquido.

Por isso uma carga externa contribui zero para o fluxo total fechado.

E como campos elétricos obedecem ao princípio de superposição, podemos repetir o argumento para várias cargas.

As cargas externas cancelam no fluxo líquido.

As internas contribuem com suas cargas divididas por épsilon zero.

Somadas, elas formam a carga envolvida: a soma algébrica das cargas que estão dentro da superfície.

E chegamos à Lei de Gauss.

O fluxo do campo elétrico por qualquer superfície fechada é igual à carga total envolvida dividida por épsilon zero.

Agora vem a parte mais importante do vídeo.

Se essa lei vale para qualquer superfície fechada, por que não desenhar qualquer uma e calcular o campo?

Coloque uma carga pontual deslocada do centro desta esfera.

A carga continua dentro.

Portanto o fluxo continua sendo q dividido por épsilon zero.

Isso é exato.

Mas olhe o campo sobre a superfície.

Os pontos da esfera não estão todos à mesma distância da carga.

Então o módulo de E varia de ponto para ponto.

E, na maior parte da esfera, o campo também não aponta na direção da normal.

Portanto este passo é inválido.

Eu não posso transformar a integral em E vezes a área da esfera.

A Lei de Gauss me deu um número: o fluxo total.

Mas o campo sobre a superfície é uma função que muda de ponto para ponto.

Saber o fluxo total não significa conhecer o campo em cada ponto.

É aqui que entra a simetria.

E a ordem do raciocínio importa.

Você não começa escolhendo uma esfera porque quer que o problema fique esférico.

Você começa olhando para a distribuição de carga.

E forma esférica não basta. Uma bola com mais carga de um lado tem forma de esfera, mas, se eu girá-la, a fonte muda.

Pergunte: quais transformações deixam essa fonte fisicamente igual?

Considere uma distribuição esfericamente simétrica.

Se eu girá-la em torno do centro, nada muda.

Não existe nenhuma direção tangencial privilegiada.

O campo produzido por essa distribuição precisa apontar radialmente, e seu módulo só pode depender da distância ao centro.

Se eu me mover mantendo a mesma distância ao centro, a direção do campo muda, mas o módulo é sempre o mesmo.

Só depois de descobrir isso escolhemos uma esfera concêntrica.

Nessa esfera, o campo é paralelo ao vetor área.

E como todos os pontos têm o mesmo raio, o módulo do campo é constante.

Agora, e somente agora, podemos tirar E da integral.

A esfera gaussiana não criou a simetria.

Ela apenas explorou uma simetria que a distribuição de carga já possuía.

Vamos usar isso numa esfera isolante com densidade volumétrica uniforme.

Primeiro queremos o campo num ponto dentro da esfera.

Pela simetria, sabemos antes de fazer qualquer conta que o campo é radial e depende apenas da distância ao centro.

Escolhemos então uma superfície gaussiana esférica de raio menor que o raio da esfera física.

O lado do fluxo fica simples: campo vezes a área da superfície gaussiana.

Agora precisamos da carga realmente envolvida por ela.

Como a densidade é uniforme, poderíamos simplesmente multiplicar densidade por volume.

Mas vale a pena enxergar a versão que também funcionará quando a densidade deixar de ser constante.

Para isso, vale relembrar as coordenadas esféricas. E repare em três letras parecidas: R maiúsculo é o raio fixo da esfera física; r é o raio da superfície gaussiana, onde medimos o campo; e r linha é a variável que percorre o volume durante a integração.

Um ponto do volume fica determinado por três números. Primeiro, a distância r linha até o centro.

Depois, o ângulo polar, medido a partir do eixo z. Vamos escrevê-lo com outra grafia de teta, para não confundir com o ângulo do fluxo.

Por fim, o ângulo azimutal, fi, que dá a volta em torno do eixo z.

Variando cada coordenada um pouquinho, formamos um pequeno bloco. Na direção radial, sua espessura é d r linha.

Na direção polar, o arco tem comprimento r linha vezes d teta.

Na direção azimutal, o ponto gira num círculo de raio r linha seno de teta, um círculo que encolhe perto dos polos. Por isso esse arco mede r linha seno de teta d fi.

Multiplicando as três dimensões, temos o elemento de volume.

Integramos a densidade com r linha indo de zero até r, porque só conta a carga que está dentro da superfície gaussiana.

Para densidade constante, o resultado é exatamente a densidade vezes quatro terços de pi vezes o raio ao cubo.

Substituindo na Lei de Gauss, primeiro cancelamos quatro pi dos dois lados.

Depois, o raio ao cubo da carga dividido pelo raio ao quadrado da área deixa um único fator de raio.

Por isso, dentro da esfera uniforme, o campo cresce linearmente com a distância ao centro. Esse resultado vale só para r menor que R.

No centro ele vale zero.

Agora mova a superfície gaussiana para fora da esfera física.

A partir daqui, aumentar o raio da superfície não envolve mais carga.

Toda a carga da esfera já está dentro.

Então a carga envolvida fica constante, enquanto a área gaussiana continua crescendo como o raio ao quadrado.

O campo passa a cair como um sobre o raio ao quadrado. Agora o resultado vale para r maior que R.

E, para pontos externos a toda a região ocupada por essa distribuição esfericamente simétrica, o resultado é exatamente o mesmo campo que seria produzido por uma carga pontual com a carga total da esfera colocada no centro.

Agora podemos enxergar todo o comportamento no gráfico.

No centro, o campo começa em zero.

Dentro da esfera, cresce em linha reta.

Atinge seu maior valor na superfície.

E, do lado de fora, passa a cair como um sobre o raio ao quadrado.

As duas expressões fornecem exatamente o mesmo valor na superfície.

O campo é contínuo ali, embora a inclinação do gráfico mude.

E repare no que realmente tornou toda essa conta simples.

Não foi a existência de uma integral.

Foi sabermos, antes de integrar, como o campo precisava se comportar por causa da simetria.

É daí que surgem as três superfícies gaussianas famosas. Cada uma pressupõe uma fonte idealizada.

Se a fonte possui simetria esférica, uma esfera concêntrica acompanha essa simetria. Ali, toda a superfície contribui para o fluxo.

Se temos uma linha infinita e uniforme, o campo depende apenas da distância ao eixo. Um cilindro coaxial aproveita isso: na lateral, o campo é paralelo ao vetor área e contribui; nas tampas, ele é tangente, e o fluxo é zero.

Para um plano infinito uniformemente carregado, a simetria obriga o campo a ser perpendicular ao plano. Um cilindro gaussiano curto atravessando o plano inverte os papéis: as duas tampas contribuem, e a lateral tem fluxo zero.

Essas formas não são receitas arbitrárias.

Elas são consequências da simetria das fontes.

E isso também explica quando Gauss não é o método mais prático.

A carga deslocada do começo, uma barra finita, um disco observado fora do eixo ou uma distribuição irregular continuam obedecendo perfeitamente à Lei de Gauss.

Mas normalmente não existe uma superfície fechada na qual a simetria nos permita substituir toda aquela informação local do campo por um único E.

Gauss ainda fornece o fluxo total.

O que ela não fornece sozinha é a distribuição ponto a ponto do campo.

Nesses casos, outro caminho funciona melhor. Para a carga deslocada, basta Coulomb, ou uma esfera centrada nela. Para a barra, somamos as contribuições de Coulomb ao longo do comprimento. Para o disco, no eixo, somamos anéis. Para uma distribuição irregular, integramos, de forma analítica ou numérica.

E, em problemas com condutores, costuma ser melhor resolver o potencial, com as condições de contorno.

Então, diante de um problema novo, não pergunte primeiro qual superfície gaussiana você decorou.

Pergunte qual é a simetria da distribuição de carga.

Essa simetria determina a direção possível do campo?

Ela diz de quais coordenadas o módulo pode depender?

Existe uma superfície fechada em que o campo tenha módulo constante nas regiões que contribuem, ou fique tangente nas regiões que não devem contribuir?

E você consegue calcular a carga envolvida?

Se essas peças se encaixam, a Lei de Gauss provavelmente transforma um problema difícil em poucas linhas.

Se não se encaixam, a lei continua verdadeira. Ela simplesmente pode não ser suficiente para determinar o campo local.

Voltando aos dois casos do começo, agora a diferença fica clara.

Nos dois, a Lei de Gauss era igualmente válida.

Mas apenas em um deles a simetria permitia transformar a integral de fluxo numa equação simples para o campo.

A Lei de Gauss fala sobre fluxo.

É a simetria da fonte que transforma fluxo em campo.

[PAUSA CURTA]

Se esse vídeo te ajudou a enxergar a Lei de Gauss de outro jeito, se inscreve no Parallax Lab, porque vem mais Física e Matemática por aqui.

E se você conhece alguém sofrendo com Física 3, compartilha esse vídeo com essa pessoa.

Deixa o like se curtiu, e a gente se vê no próximo.

## 13. STORYBOARD

### Cena 01 — Cold open · `COMPARE`

Mostrar dois problemas.

Esquerda: fonte esfericamente simétrica; superfície concêntrica; vetores radiais; simplificação possível.

Direita: carga deslocada; esfera gaussiana; vetores variáveis; mesma Lei de Gauss; campo não resolvido.

Encerrar na pergunta: **Então o que mudou?** Nenhum branding antes desse ponto.

### Cena 02 — Intro · `FOCUS`

Manter os dois problemas como contexto residual. Entrar discretamente: PARALLAX LAB · LEI DE GAUSS.
Sem vinheta longa. Na promessa ("a chave é a simetria"), destacar em sequência fonte → campo → superfície;
a superfície gaussiana da esquerda vira a superfície fechada da cena seguinte.

### Cenas 03–04 — Normal, vetor área e produto escalar · `FOCUS` → `BUILD`

Elemento na superfície fechada → ampliação. Construir em etapas: área escalar $dA$; plano tangente;
$\hat n$ unitário com marca de 90°; $d\vec A=\hat n\,dA$ (o comprimento de $d\vec A$ acompanha a área,
$\hat n$ não). Voltar à superfície fechada: normal local em vários pontos e escolha da normal exterior.
Campo uniforme: distinguir o ângulo reto ($\hat n$ × plano) do ângulo $\theta$ ($\vec E$ × $\hat n$).
Inclinar o elemento: normal e vetor área acompanham. Sincronizar $\theta$, $\cos\theta$, projeção e sinal:
0° → máximo; 90° → zero; entrada numa superfície fechada → negativo.

### Cena 05 — Coulomb + esfera · `SPLIT`

$\oint_S\vec E\cdot d\vec A\rightarrow\oint_SE\,dA\rightarrow E\oint_SdA\rightarrow E\,4\pi r^2$, cada passo
com sua ação: campo e normal se alinham; pontos revelam o mesmo módulo; $E$ sai da integral; a soma dos
elementos de área vira a área da esfera.

### Cena 06 — Cancelamento geométrico · `SPLIT`

Aumentar $r$: vetores diminuem, área aumenta; barras $1/r^2$, $r^2$ e $\Phi_E$ constante.
Resultado $\Phi_E=q/\varepsilon_0$; última variação de raio prepara a deformação da superfície.

### Cena 07 — Ângulo sólido · `BUILD`

Construção ampliada. Um cone e um elemento com distância $r$, normal, inclinação $\theta$ e área projetada
$dA\cos\theta$; depois $d\Omega_{\rm or}=\cos\theta\,dA/r^2$. Referência 3D: $4\pi$ = todas as direções
(área da esfera de raio 1).

### Cena 08 — Carga interna × externa · `COMPARE`

Interna: $4\pi$. Externa: o mesmo cone corta dois elementos, $-d\Omega$ e $+d\Omega$ (áreas diferentes);
campo local visível. Superposição: cada carga recebe sua contribuição ($q_1/\varepsilon_0$, $q_2/\varepsilon_0$,
$0$); montar $Q_{\mathrm{env}}=q_1+q_2$ (soma algébrica das cargas internas). Concluir na Lei de Gauss em caixa.

### Cena 09 — Superfície ruim · `COMPARE / BUILD`

Deslocar a carga, mantendo-a dentro. Três pontos, um de cada vez: distância, direção do campo, normal,
ângulo $\theta_i$, módulos $E_1\neq E_2\neq E_3$. Tentar $\oint\vec E\cdot d\vec A\overset{?}{=}E\oint dA$
e invalidar (magenta). Uma sonda percorre a esfera com leituras de $|\vec E|$ e $\theta$.
Payoff: **FLUXO CONHECIDO ≠ CAMPO LOCAL CONHECIDO**

### Cena 10 — Simetria · `FOCUS`

Erro de ordem: escolher a esfera antes da fonte. Forma esférica ≠ simetria esférica (bola com mais carga
de um lado muda ao girar). Fonte simétrica invariante por rotações; componente tangencial rotulada como
hipotética e eliminada. Sonda a distância fixa do centro: direção muda, módulo constante. Só então a
esfera gaussiana. Mensagem: **A SUPERFÍCIE EXPLORA A SIMETRIA. ELA NÃO A CRIA.**

### Cena 11 — Esfera uniforme interna · `SPLIT / BUILD`

Esfera física $R$ (azul, contorno contínuo); gaussiana $r<R$ (violeta tracejado); volume envolvido com
preenchimento violeta e legenda. $E(r)\,4\pi r^2=Q_{\mathrm{env}}/\varepsilon_0$.

### Cena 12 — Coordenadas esféricas e elemento de volume · `SPLIT` (~50 s)

Legenda $R$ / $r$ / $r'$. Ponto percorre $r'$; ângulo polar $\vartheta$ a partir de $z$; azimute $\phi$
dando a volta. Bloco: $dr'$, $r'\,d\vartheta$, $r'\sin\vartheta\,d\phi$; círculo de raio $r'\sin\vartheta$
encolhendo perto do polo. $dV$ com chaves por fator. O elemento fica dentro da gaussiana; $r'$ varre de 0
a $r$. Integrais avaliadas uma a uma ($r^3/3$, $2$, $2\pi$) → $Q_{\mathrm{env}}=\frac43\pi\rho r^3$.

### Cena 13 — Campo interior · `BUILD`

Substituir; cancelar $4\pi$; reduzir $r^3/r^2\rightarrow r$; $\boxed{E(r)=\rho r/3\varepsilon_0}$ com o
rótulo **interior ($r<R$)**. Crescimento linear; $E(0)=0$.

### Cena 14 — Exterior · `BUILD`

Interior fica identificado e atenuado. Gaussiana atravessa $r=R$; barra de $Q_{\mathrm{env}}$ congela em
$Q$. $E\,4\pi r^2=Q/\varepsilon_0\rightarrow Q/(4\pi\varepsilon_0r^2)\rightarrow\boxed{\rho R^3/(3\varepsilon_0r^2)}$
com rótulo **exterior ($r>R$)**. Equivalência com carga pontual, só para pontos externos.

### Cena 15 — Gráfico sincronizado · `SPLIT`

Mesmo parâmetro $r$ controla gaussiana, ponto físico e ponto do gráfico. Cada expressão ligada ao seu
ramo com o domínio. $E(0)=0$; pausa no máximo; $E(R^-)=E(R^+)$ com inclinações diferentes;
$Q_{\mathrm{env}}=Q$ constante no exterior.

### Cena 16 — Três simetrias · `COMPARE`

Cada fonte idealizada construída grande, com elementos representativos: esfera (toda a superfície,
$\vec E\parallel d\vec A$); linha infinita + cilindro coaxial (lateral $\parallel$, tampas $\perp$, fluxo
nulo); plano infinito + cilindro gaussiano curto (tampas $\parallel$, lateral $\perp$, fluxo nulo).
Depois, quadro comparativo com fonte → simetria → forma do campo → superfície útil.

### Cena 17 — Casos ruins e caminhos adequados · `COMPARE`

Carga deslocada, barra finita, disco fora do eixo, distribuição irregular. Mensagem: **A LEI CONTINUA
VÁLIDA. A SIMETRIA NÃO FECHA O PROBLEMA.** Para cada caso, uma animação curta do caminho adequado (seção
11.8) e menção ao potencial com condições de contorno. Sem riscos sobre superfícies.

### Cena 18 — Método de decisão · `FOCUS`

SIMETRIA DA FONTE → DIREÇÃO DE E → DEPENDÊNCIA ESPACIAL → SUPERFÍCIE COMPATÍVEL → CARGA ENVOLVIDA →
GAUSS É UM BOM MÉTODO?, cada pergunta aplicada a dois exemplos (esfera uniforme × barra finita).

### Cena 19 — Retorno · `COMPARE`

Reapresentar os dois casos iniciais. No simétrico: $\oint\rightarrow EA$. No ruim: a integral não colapsa.

### Cena 20 — Payoff · `FOCUS`

Tela limpa. **A LEI DE GAUSS FALA SOBRE FLUXO** e depois **É A SIMETRIA DA FONTE QUE TRANSFORMA FLUXO EM
CAMPO**. Pausa de aproximadamente 1–2 s. Nenhum CTA nesse momento.

### Cena 21 — Outro · `FOCUS / END SCREEN`

Sem destinos definidos para vídeos recomendados: logo centralizado e mensagem curta, anéis tracejados com
movimento discreto. Sem links ou títulos inventados. Nenhuma nova matemática.

## 14. SEMÂNTICA VISUAL

| Elemento | Convenção |
| --- | --- |
| Campo $\vec E$ e grandezas associadas (inclusive $\theta$, $E$ nas equações) | ciano |
| Superfície gaussiana matemática (e $r$) | violeta, contorno tracejado; regiões que contribuem em traço contínuo |
| Distribuição física de carga (e $R$, $Q$) | azul, contorno contínuo e preenchimento |
| Volume envolvido | preenchimento violeta translúcido + legenda |
| Normal e vetor área | branco: $\hat n$ fino e opaco, $d\vec A$ grosso e translúcido |
| Matemática neutra e resultados | branco |
| Passo inválido ou conflito / componente hipotética | magenta, com rótulo |

A cor nunca é a única informação: contorno, transparência e rótulos distinguem os papéis.

## 15. TIPOGRAFIA

Texto: `Space Grotesk` via helpers vigentes. Matemática: `MathTex`. Validar legibilidade em `960×540`.

## 16. PARÂMETROS

- $R$: raio fixo da esfera física.
- $r$: distância ao centro / raio da superfície gaussiana / parâmetro sincronizado do gráfico.
- $r'$: variável de integração.
- $\theta$: ângulo entre $\vec E$ e $\hat n$ (fluxo). $\vartheta$: ângulo polar das coordenadas esféricas.

Nunca misturar $r$ e $r'$, nem $\theta$ e $\vartheta$.

## 17. QA FÍSICO

O preview não pode sugerir que:

1. a Lei de Gauss só vale com simetria;
2. uma esfera gaussiana cria simetria;
3. cargas externas não criam campo;
4. fluxo zero implica campo zero;
5. $Q_{\mathrm{env}}=0$ implica $\vec E=0$;
6. qualquer distribuição esférica arbitrária tem campo externo pontual sem condição espacial;
7. superfície gaussiana precisa ser física;
8. vetor área sempre aponta radialmente;
9. Gauss fornece $E$ ponto a ponto em geral;
10. fluxo conta literalmente linhas de campo;
11. alguma forma de superfície é proibida;
12. uma fórmula vale fora do seu domínio ($r<R$ / $r>R$).

## 18. QA VISUAL

Verificar:

- textos legíveis em 960×540;
- equações legíveis, sem sobreposição confusa nas transformações;
- normal identificável antes da equação;
- os três fatores de $dV$ apontáveis na geometria; elemento dentro do volume integrado;
- cada fórmula acompanhada do seu domínio;
- lateral e tampas com contribuições demonstradas;
- vetores suficientemente espessos;
- esfera física, gaussiana e volume envolvido visualmente distintos;
- cores consistentes entre desenho e equação;
- $r$, $r'$ e $R$ inequívocos;
- gráfico contínuo em $R$;
- carga deslocada claramente dentro da esfera; módulos variando; normais e campo não paralelos;
- carga externa criando campo local;
- toda pausa longa com função de leitura, demonstração ou encerramento;
- payoff separado do CTA; tela final com ação clara.

## 19. REGRA DE IMPLEMENTAÇÃO

A implementação pode decidir detalhes técnicos como: classes; helpers; trackers; organização de
funções; reutilização de componentes; estratégia de render.

Ela NÃO pode decidir novamente, fora do escopo autorizado: física; narrativa; ordem; exemplo; matemática;
texto da narração; payoff; CTA; conteúdo do storyboard.

A cena verifica, ao ser importada, que cada fala usada para cronometrar a animação existe literalmente
nesta seção 12.

## 20. CONDIÇÃO DE PARADA

Parar quando existir o preview horizontal em `960×540 / 15 fps` suficiente para avaliação humana de:
ritmo; composição; legibilidade; narrativa visual; física; sincronização.

Não avançar automaticamente para: 1080p; 30 fps; voz final; SRT; thumbnail; publicação;
refinamento final.
