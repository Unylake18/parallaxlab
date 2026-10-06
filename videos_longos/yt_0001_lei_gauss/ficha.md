# yt_0001 — LEI DE GAUSS

**O segredo não é a integral — é a simetria**

## STATUS

`VOZ, SINCRONIA E FINAL 1080p`

Etapa final (2026-10-05): voz ElevenLabs (3 partes), sincronia por âncoras, legenda SRT com grafia normal, render 1920×1080/30. Antes:

`REVISÃO 2.1 — POLIMENTO DO SEGUNDO PREVIEW HORIZONTAL`

V2.1 (2026-10-05, handoff da Produção + adendo de rigor): sem redesenho, mesma ordem de blocos. Header
persistente `ELETROMAGNETISMO · LEI DE GAUSS`; watermark ~20% maior; ângulo sólido com nome e símbolo
juntos, ponte $d\theta=ds/r$ (2π rad) → $d\Omega=dA_\perp/r^2$ (4π sr), distinção $d\Omega$ (tamanho
angular) × $d\Omega_{\rm or}$ (com sinal); forma geral $Q_{\mathrm{env}}(r)$ em simetria esférica; frase da
continuidade em $r=R$; frase das idealizações infinitas; $\hat n$ azul elétrico e $d\vec A$ violeta;
checklist final progressivo; outro levemente polido.

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

Ângulo plano e ângulo sólido (tamanho angular, $\ge0$; $dA_\perp=dA\,|\cos\theta|$ é o tamanho da área projetada):
$$d\theta=\frac{ds}{r}\ \ (\text{volta: }2\pi\ \mathrm{rad}),\qquad
d\Omega=\frac{dA_\perp}{r^2}=\frac{dA\,|\cos\theta|}{r^2}\ \ (\text{todas as direções: }4\pi\ \mathrm{sr}).$$

Ângulo sólido orientado (o módulo some e o sinal vem de $\hat r\cdot\hat n$; para $q>0$: $+$ onde o campo sai, $-$ onde entra):
$$d\Omega_{\rm or}=\frac{\hat r\cdot\hat n}{r^2}\,dA=\frac{\cos\theta\,dA}{r^2}=\pm\,d\Omega.$$

Lei de Gauss ($Q_{\mathrm{env}}$ = carga envolvida: soma algébrica das cargas no interior da superfície):
$$\boxed{\oint_S\vec E\cdot d\vec A=\frac{Q_{\mathrm{env}}}{\varepsilon_0}}.$$

Simetria esférica:
$$\vec E(\vec r)=E(r)\hat r.$$

Elemento de volume esférico ($\vartheta$ = ângulo polar, distinto do $\theta$ do fluxo):
$$dV=dr'\cdot r'\,d\vartheta\cdot r'\sin\vartheta\,d\phi=r'^2\sin\vartheta\,dr'\,d\vartheta\,d\phi.$$

Forma geral em simetria esférica (densidade $\rho(r')$ qualquer):
$$E(r)=\frac{Q_{\mathrm{env}}(r)}{4\pi\varepsilon_0r^2},\qquad Q_{\mathrm{env}}(r)=4\pi\int_0^r\rho(r')\,r'^2dr'.$$

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

$dA\,|\cos\theta|$ é o tamanho da área projetada perpendicularmente à direção radial ($d\Omega=dA\,|\cos\theta|/r^2\ge0$). Com sinal:

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

Versão gravada (2026-10-05): narração Master aprovada pela Produção, gravada no ElevenLabs em 3 partes (`audio/partes/`). Grafia normal aqui e na legenda; o texto enviado ao TTS (`texto_narracao.txt`) usa só a grafia de fala "téta" e "Física três". A cena sincroniza pela voz (`sync.json`), não por esta seção.

Olha esses dois problemas.

Nos dois, dá pra desenhar uma superfície fechada e escrever exatamente a mesma Lei de Gauss.

No primeiro, a distribuição de carga é esfericamente simétrica, e em dois passos o campo aparece.

No segundo, eu só tiro a carga do centro da esfera.

A lei continua verdadeira.

O fluxo continua determinado.

E mesmo assim, eu não consigo tirar o campo daí.

Então, o que mudou?

Fala, pessoal!

Bem-vindos ao Parallax Lab.

Hoje a gente vai entender por que a Lei de Gauss resolve alguns problemas quase de graça e, em outros, parece não ajudar.

Spoiler: a chave é a simetria.

E a ordem importa: primeiro a fonte, depois o campo, e só então a superfície.

Pular essa ordem é o que faz muita gente decorar esfera e cilindro sem entender por quê.

Antes de responder, a gente precisa entender o que a Lei de Gauss mede.

Pega um pedacinho bem pequeno de uma superfície.

A área dele é só um número: o elemento de área.

De tão pequeno, ele praticamente coincide com o plano tangente.

Agora, a normal: a setinha azul, n chapéu.

Perpendicular ao plano, comprimento um: só direção.

Normal vezes área dá o vetor área, a seta violeta.

Repara: quando o pedaço encolhe, ela encolhe junto; a normal não.

Numa superfície fechada, cada ponto tem a sua normal, e a convenção é sempre apontar para fora.

Agora coloca esse pedaço num campo elétrico.

Repara que aparecem dois ângulos.

O de noventa graus, entre a normal e o plano, não entra na conta.

O que importa é o teta, em amarelo: entre o campo e a normal.

De frente, o fluxo é máximo.

Inclinando, ele diminui, e a normal e o vetor área giram junto.

Quando o campo passa tangente, raspando, o fluxo é zero.

E se o campo entra numa superfície fechada, contra a normal, a contribuição fica negativa.

É isso que o produto escalar faz.

E a integral fechada só repete essa soma pela superfície inteira.

Dica: o fluxo não conta linhas de campo.

As linhas são só um desenho; o fluxo é a soma de quanto campo atravessa cada pedacinho.

Agora coloca uma carga pontual positiva no centro de uma esfera.

Pela Lei de Coulomb, o campo aponta para fora e cai com o quadrado da distância.

Na esfera, campo e vetor área ficam paralelos.

E como todo ponto está à mesma distância da carga, o módulo do campo é o mesmo na superfície inteira.

Então dá pra tirar o campo da integral, e o fluxo vira o campo vezes a área da esfera.

Agora olha as barras quando o raio aumenta: o campo cai com um sobre o raio ao quadrado, mas a área cresce com o raio ao quadrado.

Uma coisa compensa exatamente a outra.

Por isso, qualquer esfera centrada na carga dá o mesmo fluxo: a carga sobre épsilon zero.

Ou seja, o fluxo mede algo mais profundo do que o campo num ponto.

Mas e se a superfície não for uma esfera?

Imagina um cone bem estreito de direções saindo da carga.

Ele corta um pedaço de uma superfície qualquer.

Aqui entra uma ideia nova: o ângulo sólido, o d ômega.

No plano, um ângulo pequeno é o arco dividido pelo raio, e a volta inteira vale dois pi radianos.

No espaço, é a mesma ideia com uma dimensão a mais: a área projetada dividida pelo raio ao quadrado.

Todas as direções juntas somam quatro pi esterradianos.

Na prática, o d ômega mede o tamanho aparente do pedaço visto da carga: qual abertura angular ele ocupa no espaço.

Se o pedaço está inclinado, conta a área projetada de frente para a carga.

E, mais longe, ele precisa ser maior para parecer do mesmo tamanho.

Daí o raio ao quadrado.

Área, inclinação e distância: juntas, formam o d ômega.

O d ômega é só tamanho, sempre positivo.

Já o d ômega orientado também leva em conta de que lado a superfície está sendo atravessada.

Para a carga positiva que estamos desenhando, ele fica positivo onde o campo sai e negativo onde entra.

E o fluxo pelo pedaço é a carga sobre quatro pi épsilon zero, vezes o d ômega orientado.

A distância sumiu.

Com a carga dentro, a soma orientada sobre toda a superfície totaliza quatro pi.

Quatro pi esterradianos: a área da esfera unitária inteira, e não a volta de um círculo.

Os quatro pi se cancelam: a carga sobre épsilon zero, para qualquer formato.

Agora coloca a carga do lado de fora.

O campo na superfície não some; em alguns pontos, é até forte.

Mas cada feixe que entra por um lado sai pelo outro: a contribuição orientada é negativa na entrada e positiva na saída.

No total, o fluxo líquido é zero.

Atenção: fluxo líquido zero não significa campo zero.

Com várias cargas, a superposição resolve: as de fora dão zero, as de dentro dão a própria carga sobre épsilon zero.

Somando, aparece a carga envolvida: a soma, com sinal, das cargas lá dentro.

E chegamos à Lei de Gauss: o fluxo por qualquer superfície fechada é a carga envolvida sobre épsilon zero.

Agora vem a parte mais importante do vídeo.

Se a lei vale para qualquer superfície, por que não desenhar qualquer uma e sair calculando o campo?

Olha: eu desloco a carga, mas ela continua dentro.

O fluxo continua sendo a carga sobre épsilon zero, exatamente.

Só que os pontos da esfera não estão mais à mesma distância da carga.

Então o módulo do campo muda de ponto para ponto.

E quase nunca aponta na direção da normal: o teta deixa de ser zero.

Por isso esse passo, em magenta, é proibido.

Não dá pra tirar o campo da integral.

A Lei de Gauss me deu um número: o fluxo total.

Mas o campo na superfície é uma função que muda de ponto para ponto.

Saber o fluxo não é saber o campo.

É aqui que entra a simetria.

E a ordem do raciocínio importa.

Você não começa escolhendo uma esfera porque quer que o problema fique esférico.

Você começa olhando para a carga.

Cuidado: formato de esfera não é simetria esférica.

Uma bola com mais carga de um lado parece uma esfera, mas, se eu giro, a fonte muda.

A pergunta certa é: o que eu posso fazer com essa fonte sem que ela mude?

Aqui, qualquer rotação em torno do centro deixa tudo igual.

Então não existe campo de lado: com uma meia volta em torno do eixo radial que passa por esse ponto, ele teria que inverter, sem a fonte mudar.

Sobra um campo radial, que só depende da distância.

Andando à mesma distância, a direção muda, mas o módulo não.

Só agora escolhemos a esfera concêntrica: nela, campo e vetor área são paralelos, e o módulo é constante.

Agora, e só agora, o campo sai da integral.

A superfície explora a simetria.

Ela não cria.

Bora usar isso numa esfera isolante com densidade de carga uniforme.

Primeiro, o campo dentro dela.

Pela simetria, antes de qualquer conta, já sabemos: o campo é radial e só depende da distância ao centro.

Então escolhemos uma gaussiana esférica, menor que a esfera física.

O lado do fluxo fica fácil: o campo vezes a área da gaussiana.

Falta a carga envolvida, a que está nesse volume violeta.

Como a densidade é uniforme, daria pra fazer só densidade vezes volume.

Mas vale ver o caminho que funciona sempre, até quando a densidade muda.

Antes, atenção a três letras parecidas: R maiúsculo é o raio da esfera física, fixo; r é o raio da gaussiana, onde medimos o campo; e r linha é a variável que percorre o volume na integral.

Um ponto lá dentro fica definido por três números.

O primeiro é a distância até o centro, o r linha.

O segundo é o ângulo polar, medido a partir do eixo z.

Na tela, a gente usa uma outra forma da letra teta para distinguir esse ângulo polar do teta que apareceu no fluxo.

E o terceiro é o ângulo azimutal, fi, que dá a volta em torno do eixo.

Variando cada um só um pouquinho, nasce um bloquinho.

Na direção radial, a espessura é d r linha.

Na polar, o arco é r linha vezes d teta.

Na azimutal, o ponto gira num círculo de raio r linha seno de teta, que encolhe perto dos polos.

Por isso, o arco é r linha seno de teta d fi.

Multiplicando os três, temos o elemento de volume.

Agora integramos a densidade com o r linha indo do centro até a gaussiana, porque só conta a carga lá dentro.

As integrais dos ângulos dão quatro pi, para qualquer densidade que dependa só da distância ao centro.

Guarda essa: a simetria resolve a geometria; a densidade só decide quanta carga existe dentro da gaussiana.

Com densidade constante, sobra a densidade vezes quatro terços de pi vezes o raio ao cubo.

Na Lei de Gauss, o quatro pi cancela dos dois lados, e o raio ao cubo sobre o raio ao quadrado deixa o raio uma vez só.

Resultado: o campo cresce linearmente com a distância ao centro, e no centro vale zero.

Isso só vale dentro da esfera.

Agora leva a gaussiana para fora da esfera.

Daqui pra frente, aumentar o raio não envolve mais carga: a barra da carga envolvida trava no total.

A área continua crescendo com o raio ao quadrado, então o campo passa a cair com um sobre o raio ao quadrado.

Isso vale fora da esfera.

E repara: aí fora, o campo é exatamente o de uma carga pontual com a carga total, colocada no centro.

Agora junta tudo no gráfico.

No centro, o campo começa em zero.

Dentro, cresce em linha reta.

Atinge o máximo na superfície.

E fora, cai com um sobre o raio ao quadrado.

Na superfície, as duas fórmulas dão o mesmo valor: o campo é contínuo, só a inclinação muda.

E é contínuo porque não existe uma camada de carga concentrada na superfície da esfera.

Agora repara no que deixou essa conta simples.

Não foi a integral.

Foi saber, antes de integrar, como o campo tinha que ser, por causa da simetria.

É daí que vêm as três superfícies gaussianas famosas: cada uma funciona porque a fonte possui a simetria correspondente.

Simetria esférica pede esfera concêntrica: a superfície toda contribui.

Uma linha infinita, uniformemente carregada, pede um cilindro coaxial: a lateral contribui e, nas tampas, o campo é tangente, fluxo zero.

Um plano infinito, uniformemente carregado, pede um cilindro curto atravessando o plano: agora as tampas contribuem e a lateral dá zero.

Na linha e no plano, essas simetrias são exatas nas idealizações infinitas.

Objetos finitos aproximam esse comportamento em regiões suficientemente afastadas das bordas ou extremidades.

Ou seja: não é receita decorada.

É consequência da simetria da fonte.

E isso também explica quando Gauss não é o caminho mais prático.

A carga deslocada do começo, uma barra finita, um disco visto fora do eixo, uma distribuição irregular: todos obedecem à Lei de Gauss.

Mas não existe superfície em que a simetria deixe trocar esse campo variável por um único valor de campo.

Gauss continua dando o fluxo total; o que ela não dá sozinha é o campo ponto a ponto.

Nesses casos, outro caminho funciona melhor.

Para uma carga pontual isolada, Coulomb direto resolve.

Se quiser usar Gauss, a superfície útil é uma esfera centrada na própria carga — não naquela esfera arbitrária do começo.

Para a barra, soma as contribuições de Coulomb ao longo dela.

Para o disco, no eixo, a simetria deixa somar anéis.

Fora do eixo, essa simplificação some: a integral fica bem mais pesada e muitas vezes vale resolver numericamente.

Para uma distribuição irregular, integra, na mão ou no computador.

Então, diante de um problema novo, não pergunta primeiro qual superfície você decorou.

Pergunta: qual é a simetria da fonte?

Ela define a direção do campo?

Diz de que coordenadas o módulo depende?

Existe uma superfície em que o campo seja constante onde contribui e tangente onde não deve contribuir?

E dá pra calcular a carga envolvida?

Se as peças se encaixam, como na esfera, Gauss resolve em poucas linhas.

Se não se encaixam, como na barra, a lei continua verdadeira; ela só não basta para achar o campo.

Voltando aos dois casos do começo, agora a diferença fica clara.

Nos dois, a Lei de Gauss é igualmente válida.

Mas só no primeiro a simetria transforma a integral do fluxo numa equação simples para o campo.

A Lei de Gauss fala sobre fluxo.

É a simetria da fonte que transforma fluxo em campo.

[PAUSA CURTA]

Se esse vídeo te ajudou a enxergar a Lei de Gauss de outro jeito, deixa o like: isso ajuda muito o canal.

Compartilha com aquele amigo que está sofrendo com Física 3.

E se inscreve no Parallax Lab, porque vem muito mais Física e Matemática por aí.

A gente se vê no próximo!

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

Construção ampliada. Um cone e um elemento. **ÂNGULO SÓLIDO** e $d\Omega$ entram juntos (o rótulo no
cone só nasce com o nome). Ponte curta: no plano $d\theta=ds/r$ (volta: 2π rad); no espaço
$d\Omega=dA_\perp/r^2$ (todas as direções: 4π sr; sr = esterradiano); o mesmo cone intercepta o pedaço
inclinado. Depois distância $r$, normal, inclinação $\theta$, $dA_\perp=dA\,|\cos\theta|$ e
$\boxed{d\Omega=dA\,|\cos\theta|/r^2}$; então $d\Omega_{\rm or}=(\hat r\cdot\hat n)\,dA/r^2=\pm d\Omega$ e a
substituição em $d\Phi_E$. Referência 3D: $4\pi$ = todas as direções (área da esfera de raio 1).

### Cena 08 — Carga interna × externa · `COMPARE`

Interna: $4\pi$. Externa: o mesmo cone corta dois elementos, $d\Omega_{\rm or}=-d\Omega$ e $d\Omega_{\rm or}=+d\Omega$ (áreas diferentes);
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
| Campo $\vec E$ (setas, $E$ nas equações, barras de $\lvert\vec E\rvert$) | ciano |
| Grandezas angulares ($\theta$, $\vartheta$, $\phi$, $d\theta$, $d\Omega$, arcos; marca de 90° com peso menor) | âmbar `#FFC24D` |
| Superfície gaussiana matemática (e $r$) | violeta, contorno tracejado; regiões que contribuem em traço contínuo |
| Distribuição física de carga (e $R$, $Q$) | azul, contorno contínuo e preenchimento |
| Volume envolvido | preenchimento violeta translúcido + legenda |
| Normal unitária $\hat n$ | azul elétrico `#267BFF`, seta fina e opaca |
| Vetor área $d\vec A$ e elemento $dA$ | violeta `#745CFF`: seta grossa; o pedaço com preenchimento translúcido |
| Área projetada $dA_\perp$ | branco (geometria neutra) |
| Matemática neutra e resultados | branco |
| Passo inválido ou conflito / componente hipotética | magenta, com rótulo |

A cor nunca é a única informação: contorno, transparência e rótulos distinguem os papéis. $\hat n$ e
$d\vec A$ também diferem por função: $\hat n$ curto e fino num ponto do elemento; $d\vec A$ grosso, no
centro, com comprimento que acompanha a área.

Hierarquia (V2.1): resultado/box > rótulo de caso e comentário auxiliar (menores, ~70% de opacidade) >
anotações geométricas. Boxes com margem interna maior e borda fina.

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
