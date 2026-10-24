# Narração — yt_0011 · Lei de Faraday (versão conceitual vigente; sem voz)

Sem sincronização de áudio nesta fase. Moldura: gancho → “Bem-vindos ao Parallax Lab” → promessa; no final: payoff → CTA curto → ponte conceitual.

## Abertura — hook + identidade + promessa

Olha para esse circuito.
A espira está parada. O fio está parado.
Mesmo assim, quando o campo magnético começa a variar...
aparece uma corrente.
O que está empurrando essas cargas?

Bem-vindos ao Parallax Lab.

Hoje vamos entender como um campo magnético variável está associado a um campo elétrico induzido — e por que esse campo é diferente daquele da eletrostática.

## Bloco 2 — Removendo o mecanismo anterior

No caso da fem de movimento, a explicação vinha da força magnética sobre cargas que se moviam junto com o condutor.
Aparecia o termo velocidade vetorial vezes campo magnético.
Mas aqui a velocidade do condutor — não a das cargas dentro dele — é zero.
Então essa contribuição magnética do movimento é zero.
As cargas ainda podem se mover dentro do fio; o que falta é o que as empurra.

## Bloco 3 — O paradoxo

E é isso que torna esse caso tão importante.
A contribuição magnética associada ao movimento do fio é zero...
mas a força eletromotriz não é.
Existe corrente sem que o condutor esteja cortando linhas de campo.
Então falta alguma coisa na nossa descrição.
Que campo está exercendo força sobre as cargas agora?

## Bloco 4 — Faraday ainda prevê a fem

A lei de Faraday já nos diz uma parte da resposta.
Uma variação do fluxo magnético produz uma força eletromotriz.
E, neste caso, a espira não muda de tamanho nem de orientação.
A área é constante.
Quem muda é o próprio campo magnético.
Para um campo uniforme e perpendicular à espira, o fluxo é simplesmente B vezes A.
Então a fem vale menos A vezes a taxa de variação de B.
A lei consegue prever quanto vale a fem.
Mas ainda falta responder uma pergunta física:
o que exerce essa força sobre cada carga?

## Bloco 5 — Quanto não é o mesmo que por quê

Esse é um ponto fácil de passar rápido demais.
Saber o valor da fem não identifica automaticamente o mecanismo que acelera as cargas.
O fio continua parado.
A força magnética de movimento continua ausente.
Então precisamos procurar uma força por unidade de carga que possa existir mesmo sem movimento mecânico do circuito.

## Bloco 6 — Surge o campo elétrico induzido

Para um circuito estacionário, a força eletromotriz pode ser escrita como a circulação do campo elétrico ao longo do circuito.
A força sobre cada carga é q vezes E: a força por unidade de carga é o campo elétrico.
E agora as duas expressões precisam representar o mesmo fenômeno.
A circulação de E ao redor do caminho fechado é igual a menos a taxa de variação do fluxo magnético.
Essa é a mudança conceitual central.
Um campo magnético que varia no tempo está associado a um campo elétrico capaz de empurrar cargas mesmo quando o fio inteiro está parado.
Esse é o campo elétrico induzido.

## Bloco 7 — Circulação antes da geometria

Mas cuidado com o que essa equação já nos permite concluir.
Ela diz que existe circulação de campo elétrico ao redor desse caminho.
O caminho C é uma escolha nossa; ele não é uma linha de campo.
Ela ainda não diz, sozinha, que todas as linhas de campo precisam ser círculos perfeitos.
A geometria do campo depende também da simetria do problema.
Então vamos escolher um caso em que essa simetria seja forte o bastante para determinar a forma de E.

## Bloco 8 — Por que esse campo é diferente da eletrostática

Antes disso, compare com a eletrostática.
Num campo eletrostático, a circulação ao longo de qualquer caminho fechado é zero.
Você pode sair de um ponto, dar uma volta inteira e retornar ao mesmo lugar sem acumular uma diferença líquida de potencial ao longo do percurso.
Aqui não.
Quando o fluxo magnético varia, essa circulação pode ser diferente de zero.
Portanto, o campo elétrico induzido não é simplesmente o mesmo tipo de campo conservativo que encontramos na eletrostática.

## Bloco 9 — O exemplo cilíndrico

Vamos usar um modelo idealizado: um solenoide muito longo.
Vamos desprezar os efeitos das extremidades.
Dentro de um raio R, o campo magnético é aproximadamente uniforme.
Fora, vamos tratá-lo como desprezível.
Escolhemos o eixo z saindo da tela e fazemos B aumentar nessa direção.
Agora entra a simetria.
Pontos à mesma distância do eixo são equivalentes por rotação.
Neste modelo, considerando apenas o campo induzido associado à variação de B, sem acrescentar um campo eletrostático independente, E é azimutal.
Sua componente tangencial tem o mesmo valor ao longo de cada círculo.
Nesta geometria específica, as linhas de E são círculos ao redor do eixo.

## Bloco 10 — Dentro da região magnética

Primeiro escolha um círculo de raio r menor que R.
Ao longo desse círculo, a simetria garante que o módulo de E é constante e que o campo é tangente ao caminho inteiro.
Então a circulação vira E vezes o comprimento da circunferência.
E o fluxo magnético envolvido cresce com a área pi r ao quadrado.
Aplicando Faraday e dividindo pelo comprimento dois pi r, o pi cancela e r ao quadrado sobre r vira r: o módulo de E é proporcional a r.
Mais longe do centro, mas ainda dentro da região magnética, maior é o módulo do campo elétrico induzido.
E o sinal negativo determina o sentido.
Como o campo magnético para fora da tela está aumentando, o campo elétrico induzido circula no sentido horário.

## Bloco 11 — O que muda em R?

Agora chegamos à borda da região onde existe campo magnético.
Até aqui, aumentar r fazia duas coisas ao mesmo tempo:
aumentava o comprimento do caminho e também aumentava a área atravessada por B.
Mas o que acontece se continuarmos aumentando r depois de ultrapassar R?
O caminho continua crescendo.
A área onde existe campo magnético, não.
E essa diferença muda completamente a dependência de E com a distância.

## Bloco 12 — Fora da região magnética

Para r maior que R, a região magnética parou de crescer, mas o caminho continua aumentando.
O fluxo não depende mais da área pi r ao quadrado: o campo B só ocupa a região interna de raio R.
Então o fluxo relevante fica limitado a B vezes pi R ao quadrado.
Mas o comprimento do caminho continua sendo dois pi r.
Por isso, agora o campo elétrico precisa cair como um sobre r.
Dentro, o módulo de E crescia linearmente.
Fora, o módulo de E diminui com a distância: R ao quadrado é fixo e r é variável.
Tudo isso sai da mesma lei.

## Bloco 13 — O perfil completo de E

Agora podemos enxergar o campo inteiro de uma vez.
No centro, E começa em zero.
Dentro da região magnética, seu módulo cresce proporcionalmente a r.
Na borda, as duas expressões se encontram no mesmo valor.
E depois, do lado de fora, o campo cai como um sobre r.
O gráfico não é uma informação separada da geometria.
Ele é exatamente a mesma física vista de outra perspectiva.
Cada posição r no espaço corresponde ao ponto certo na curva.

## Bloco 14 — B quase zero, E diferente de zero

E agora aparece uma consequência que parece estranha à primeira vista.
Escolha um ponto fora do solenoide ideal.
Nesse ponto, o campo magnético é praticamente zero.
Mesmo assim, o campo elétrico induzido não é zero.
Isso significa que Faraday não está dizendo que o valor de E em um ponto é determinado apenas pelo valor de B naquele mesmo ponto.
O que aparece na forma integral é a variação do fluxo magnético através da região delimitada pelo caminho.
O campo elétrico pode existir aqui fora mesmo que B seja desprezível exatamente aqui.

## Bloco 15 — Da forma global para a forma local

Até agora tratamos Faraday de maneira global.
O que acontece ao redor de um contorno está relacionado ao que acontece com o fluxo através da superfície limitada por esse contorno.
Mas podemos perguntar algo mais local:
o que a variação do campo magnético significa em cada pequena região do espaço?
Usando o teorema de Stokes, a circulação de E pode ser relacionada ao rotacional de E através da superfície.
E, para uma superfície fixa, a variação do fluxo pode ser escrita usando a derivada temporal do próprio campo magnético.
Como essa relação vale para qualquer superfície fixa apropriada, o integrando precisa satisfazer a igualdade em cada ponto.
Chegamos à forma local da lei de Faraday:
o rotacional de E é igual a menos a derivada temporal de B.
Essa é uma das equações de Maxwell.

## Bloco 16 — Local não é global

E aqui o exemplo que acabamos de resolver impede uma interpretação errada dessa equação.
Dentro da região magnética, B está variando.
Então a derivada temporal de B é diferente de zero, e o campo elétrico possui rotacional diferente de zero.
Mas fora do solenoide ideal, B é desprezível e sua derivada temporal também é zero.
Ali, localmente, o rotacional de E é zero.
Só que E não é zero.
E uma volta completa que envolve o solenoide ainda pode ter circulação diferente de zero.
Não há contradição.
Rotacional zero localmente não significa campo nulo.
E uma curva que envolve a região onde o fluxo magnético está variando pode continuar apresentando circulação global não nula.
É justamente por isso que as formas integral e diferencial devem ser entendidas como duas perspectivas complementares da mesma lei.

## Bloco 17 — O fio não cria o campo (payoff físico)

Agora volte ao circuito do começo.
Nós usamos o fio porque ele oferece cargas livres e permite observar uma corrente.
Retire a espira. Retire o amperímetro.
O campo magnético continua lá, e o campo elétrico induzido também.
O fio não cria esse campo. Ele apenas revela sua existência.

*(Respiro visual real após essa frase; sem CTA nem texto novo na tela.)*

## Bloco 18 — Síntese (sem repetir o payoff)

Então a história completa é esta.
Globalmente, uma variação do fluxo magnético está associada à circulação do campo elétrico.
E localmente, Maxwell–Faraday nos diz:
o rotacional de E é igual a menos a derivada temporal de B.
Mas isso não significa que E só possa existir onde B está variando localmente.
O solenoide ideal mostrou o contrário.

## CTA

Se esse vídeo te ajudou, deixa o like e se inscreve no Parallax Lab.

## Ponte para o próximo vídeo

No próximo vídeo, vamos investigar como o fluxo criado pela própria corrente reage às mudanças dessa corrente — e onde fica armazenada a energia de um campo magnético.

---

**Nota de produção (não falar):** CTA único e curto: like + inscrição. Sem sino, comentário, compartilhamento ou sequência adicional de pedidos. A ponte tem uma única culminação (energia magnética), sem repetir a pergunta.

---

Não desenvolver nesta unidade `ℰ_L = −L dI/dt`, `U_B = ½LI²` nem `u_B = B²/2μ₀`: pertencem ao próximo vídeo.
