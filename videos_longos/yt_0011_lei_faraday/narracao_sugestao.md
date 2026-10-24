# yt_0011 — Como um campo magnético cria um campo elétrico? (Lei de Faraday) — sugestão de narração (v1, para fechar antes da voz)

Status: **sugestão para revisão. Voz não gerada, sem tags.** Base: a narração conceitual aprovada (`narracao.md`), o storyboard de 18 estados e o tom dos longos 0008 e 0009 (primeira pessoa do plural, íntimo, com humor leve, conectivos, perguntas que o espectador faria).

Princípio da série: **a voz explica o porquê; o Manim mostra o como.** O vídeo se molda à voz (remapeamento por âncoras): a fala pode ser mais longa que a animação silenciosa, e a animação segura onde indicado no fim.

Tamanho: 2.714 palavras de fala (N001–N052), cerca de **15 min 55 s** a ~2,85 palavras por segundo (a velocidade medida no 0009). Para chegar perto de 14 min, os cortes que menos doem são: N016 (repete N015), o final de N019, N030 (repete N026–N029), N039 e N048.

## Como falar as grandezas (regra: pelo nome, nunca só pela letra)

| Na tela | Na fala |
|---|---|
| B (magenta) | **o campo magnético** (1ª vez: "que na tela aparece em magenta") |
| E (ciano) | **o campo elétrico** (induzido, quando for o caso) |
| ℰ | **a força eletromotriz** (1ª vez: "a fem, a força eletromotriz") |
| Φ_B | **o fluxo magnético** |
| dB/dt | **a derivada do campo magnético em relação ao tempo**, ou "o quanto o campo magnético muda a cada segundo" |
| ∂B/∂t | **a derivada parcial do campo magnético em relação ao tempo** |
| A | **a área da espira** |
| u | **a velocidade do condutor** (do fio inteiro, não a das cargas lá dentro) |
| q | **a carga** |
| F/q | **a força por unidade de carga** |
| ∮ E·dℓ | **a circulação do campo elétrico ao longo do caminho** |
| dℓ | **um pedacinho do caminho, orientado** |
| C | **o caminho** (a espira, ou o caminho que escolhemos) |
| S | **a superfície** que o caminho limita |
| R | **o raio do solenoide** |
| r | **o raio do círculo** (do caminho) |
| E_φ | **a componente do campo elétrico ao longo da direção que dá a volta no eixo** |
| φ̂ | **o vetor unitário que dá a volta no eixo**, anti-horário |
| ẑ | **o eixo z**, que sai da tela |
| ∇×E | **o rotacional do campo elétrico** (1ª vez: "nabla cruz E") |
| π | **pi** |

Operações por extenso ("vezes", "dividido por", "ao quadrado", "igual a", "mais", "menos"). Letra solta só quando a tela aponta e o símbolo é novo. Não ler subscritos nem setas.

Evitar: dizer "o campo é zero" quando o que é zero é o rotacional; dizer que o campo elétrico induzido é "sempre circular" (só neste exemplo, por simetria); chamar o caminho de linha de campo; dizer que o fio cria o campo; dizer que os pontos azuis são elétrons (são portadores positivos fictícios, marcas da corrente convencional).

---

## B00 · Gancho, boas-vindas e promessa

N001 Olha esse circuito. A espira está parada. O fio está parado. Nada, absolutamente nada, está se movendo. Agora repara no campo magnético, aqui em magenta: ele começa a crescer. E o ponteiro do amperímetro... se mexe. Apareceu corrente.

N002 Pensa comigo: ninguém está girando essa espira, ninguém está puxando o fio através do campo. As cargas lá dentro andam, e a gente não sabe por quê. Então, afinal, quem está empurrando essas cargas?

N003 Bem-vindos ao Parallax Lab! Hoje a gente vai descobrir como um campo magnético que varia no tempo está ligado a um campo elétrico, o campo elétrico induzido, e por que esse campo é muito diferente daquele que a gente conhece da eletrostática.

N004 No caminho, vamos fazer um exemplo completo, com conta, gráfico e uma pegadinha lá no fim que muda a forma de olhar a lei de Faraday. Bora?

## B01 · Tirando a explicação antiga do caminho

N005 Primeiro, vamos tirar do caminho a explicação que a gente já conhece. Na força eletromotriz de movimento, o condutor se move dentro do campo magnético, as cargas vão junto com ele e o campo magnético empurra essas cargas de lado. A força era a carga vezes a velocidade vezes o campo magnético.

N006 Só que olha o que a gente tem aqui. A velocidade do condutor, do fio inteiro, não a das cargas lá dentro, é zero. Então essa força magnética de movimento vale zero. As cargas ainda podem andar dentro do fio, o que falta é saber quem as empurra.

## B02 · O paradoxo

N007 E é isso que torna esse caso tão bonito. A contribuição magnética do movimento é zero... mas a força eletromotriz não é zero. Existe corrente sem que o fio esteja cortando linha de campo nenhuma. Se a conta do movimento não explica, então falta alguma coisa na nossa descrição. Que força está agindo sobre as cargas agora?

## B03 · Faraday ainda prevê a fem

N008 A lei de Faraday já entrega metade da resposta. Ela diz que, quando o fluxo magnético muda, aparece uma força eletromotriz. Vamos montar isso devagar.

N009 O fluxo magnético, para um campo uniforme e perpendicular à espira, é o campo magnético vezes a área da espira. Repara na área, aqui em violeta: ela é fixa, a espira não muda de tamanho nem gira. Quem muda, sozinho, é o campo magnético.

N010 A força eletromotriz é menos a derivada do fluxo magnético em relação ao tempo. Colocando o fluxo, fica menos a derivada de campo magnético vezes área. Como a área não muda, ela sai da derivada: a força eletromotriz é menos a área vezes a derivada do campo magnético em relação ao tempo, ou seja, vezes o quanto o campo magnético muda a cada segundo.

N011 Ótimo: a lei diz quanto vale a força eletromotriz. Mas atenção, porque aqui mora uma pegadinha. Saber quanto vale não é saber quem empurra.

## B04 · Quanto não é o mesmo que mecanismo

N012 Esse é um ponto que passa batido fácil. Vamos destacar uma carga dentro do fio. O fio continua parado, a força magnética de movimento continua ausente. Então a gente precisa de uma força por unidade de carga que exista mesmo sem o circuito se mexer. Que força é essa? Ela é a peça que falta.

## B05 · Surge o campo elétrico induzido

N013 Lembra como a força eletromotriz é definida? É a integral, ao longo do circuito, da força por unidade de carga. Numa espira parada, quem pode fazer esse papel? Só pode ser um campo elétrico: a força sobre a carga é a carga vezes o campo elétrico. Olha a seta azul-clara sobre a carga: é essa força.

N014 Então a força por unidade de carga é o campo elétrico, e a força eletromotriz passa a ser a circulação do campo elétrico ao longo do caminho: a integral do campo elétrico, produto escalar com cada pedacinho do caminho, em volta de toda a espira.

N015 Agora junta com o que a gente acabou de ver. A mesma força eletromotriz também é menos a derivada do fluxo magnético no tempo. São duas maneiras de descrever o mesmo fenômeno, então tem que dar igual. E aqui está a virada: a circulação do campo elétrico ao longo do caminho fechado é igual a menos a derivada do fluxo magnético em relação ao tempo. Essa é a lei de Faraday na forma integral.

N016 Para quem gosta de ir direto ao ponto: um campo magnético que varia no tempo está ligado a um campo elétrico capaz de empurrar cargas mesmo quando o fio inteiro está parado. Esse é o campo elétrico induzido.

## B06 · Circulação antes da geometria

N017 Mas calma, cuidado com o que essa equação já permite concluir. Ela diz que existe circulação do campo elétrico ao longo desse caminho. Só isso. E repara: o caminho é uma escolha nossa, a gente que desenhou. Ele não é uma linha de campo.

N018 Em cada ponto, o campo elétrico aponta para um lado, o pedacinho do caminho aponta para outro. E o que entra na conta é só a parte do campo que vai ao longo do caminho: o produto escalar entre os dois. É o quanto o campo empurra ao longo do caminho, vezes o tamanho do pedacinho.

N019 Então Faraday estabeleceu a circulação. Ele ainda não disse, sozinho, que o campo precisa ser um monte de círculos perfeitos. A forma do campo depende também da simetria do problema. Qual é, então, a forma desse campo numa geometria que a gente consegue resolver? Já, já. Antes, uma comparação rápida.

## B07 · Eletrostática versus indução

N020 Pega o campo elétrico de uma carga parada, a eletrostática, e dá uma volta em qualquer caminho fechado. Em alguns trechos o campo ajuda, o sinal é positivo; em outros atrapalha, o sinal é negativo. No final, tudo se cancela e a circulação é zero. Você sai de um ponto, dá a volta inteira e volta ao mesmo lugar sem ganhar nem perder nada.

N021 Aqui não. Quando o fluxo magnético varia, os trechos contribuem com o mesmo sinal, e a circulação não é zero. Por isso o campo elétrico induzido por um fluxo magnético variável não é, em geral, um campo eletrostático conservativo. Se você já decorou que campo elétrico só nasce de carga, pode abrir uma exceção hoje: a gente te perdoa.

## B08 · O exemplo cilíndrico

N022 Para resolver de verdade, vamos usar um modelo idealizado: um solenoide ideal, muito longo, desprezando os efeitos das pontas. A gente olha o corte transversal. Dentro de um raio, o raio do solenoide, o campo magnético é aproximadamente uniforme; fora, vamos tratá-lo como desprezível.

N023 O eixo z sai da tela, é esse símbolo aqui, e o campo magnético aponta nessa direção e está crescendo: a derivada dele em relação ao tempo é positiva. Para o sentido de percorrer os caminhos, a gente escolhe o anti-horário. Guarda essa convenção, porque o sinal da conta depende dela.

N024 Agora entra a simetria. Pontos à mesma distância do eixo são equivalentes: se você gira o sistema em torno do eixo, nada muda. Considerando só o campo elétrico induzido pela variação do campo magnético, sem somar um campo eletrostático independente, esse campo aponta na direção que dá a volta no eixo, e a componente dele nessa direção tem o mesmo valor ao longo de cada círculo.

N025 Só agora, e só neste exemplo, as linhas do campo elétrico viram círculos em volta do eixo. E repara: como o campo magnético está crescendo, a componente do campo elétrico, nessa direção anti-horária, vai ser negativa. Então o campo elétrico real gira no sentido horário. A conta vai confirmar.

## B09 · Dentro do solenoide

N026 Primeiro caso: um círculo de raio menor que o raio do solenoide. Por simetria, o campo elétrico é tangente ao círculo inteiro e tem o mesmo valor em todo ponto dele. Então a circulação é só a componente do campo elétrico vezes o comprimento do círculo: dois pi vezes o raio. Olha o contorno acendendo na tela.

N027 Do outro lado da lei, o fluxo magnético. O campo magnético atravessa uma área de pi vezes o raio ao quadrado, então o fluxo é o campo magnético vezes pi vezes o raio ao quadrado, e a área acende aqui em violeta.

N028 A lei de Faraday diz que a circulação é menos a derivada do fluxo em relação ao tempo. Só o campo magnético muda; a área é fixa. Então fica: a componente do campo elétrico vezes dois pi raio é igual a menos pi vezes o raio ao quadrado, vezes a derivada do campo magnético em relação ao tempo.

N029 Agora é álgebra, e dá para ver. Divide os dois lados por dois pi vezes o raio. O pi do alto cancela o pi de baixo, e o raio ao quadrado dividido pelo raio vira só o raio. Sobra: a componente do campo elétrico é igual a menos o raio sobre dois, vezes a derivada do campo magnético em relação ao tempo.

N030 O que isso quer dizer? O módulo do campo elétrico cresce em linha reta com o raio: quanto mais longe do centro, mas ainda dentro da região magnética, maior é o campo elétrico induzido. E o sinal negativo decide o sentido: campo magnético crescendo para fora da tela, campo elétrico gira no sentido horário.

## B10 · A borda: o que muda quando o círculo cresce

N031 Agora chegamos à borda da região onde existe campo magnético. Até aqui, aumentar o raio fazia duas coisas ao mesmo tempo: aumentava o comprimento do caminho e aumentava a área atravessada pelo campo magnético. Repara em três objetos: o caminho, em violeta; a superfície que ele limita, também em violeta; e a parte dessa superfície que realmente tem campo magnético, em magenta. Enquanto o círculo está dentro, as duas áreas são a mesma.

N032 E se a gente continuar crescendo depois do raio do solenoide? O caminho continua crescendo. A superfície também. Mas a parte com campo magnético não: ela trava em pi vezes o raio do solenoide ao quadrado. A região magnética acabou. Essa diferença muda completamente a forma como o campo elétrico depende da distância.

## B11 · Fora do solenoide

N033 Para um raio maior que o do solenoide, o fluxo magnético não depende mais do raio do círculo. Ele fica fixo: o campo magnético vezes pi vezes o raio do solenoide ao quadrado. O comprimento do caminho, porém, continua sendo dois pi vezes o raio do círculo.

N034 A lei dá: a componente do campo elétrico vezes dois pi raio é igual a menos pi vezes o raio do solenoide ao quadrado, vezes a derivada do campo magnético em relação ao tempo. Divide por dois pi raio: o pi cancela e sobra menos o raio do solenoide ao quadrado, sobre dois vezes o raio do círculo, vezes a derivada.

N035 Repara na diferença entre os dois casos. O raio do solenoide é fixo, é o tamanho da região magnética. O raio do círculo é variável, é o tamanho do caminho. Dentro, o raio do círculo aparecia em cima; fora, ele aparece embaixo. Por isso o campo elétrico, que crescia em linha reta, agora cai como um sobre o raio. Tudo isso saiu da mesma lei.

## B12 · O perfil completo

N036 Agora dá para enxergar o campo inteiro de uma vez. O gráfico mostra o módulo do campo elétrico em função do raio, e o ponto nele é exatamente o círculo da esquerda: mesmo raio, mesmo estado, só mudou o jeito de olhar. O gráfico não é uma informação separada da geometria, é a mesma física vista de outra perspectiva.

N037 No centro, o campo elétrico é zero. Dentro do solenoide, o módulo cresce proporcionalmente ao raio. Na borda, as duas expressões se encontram no mesmo valor: o raio do solenoide sobre dois, vezes a derivada. Então a curva é contínua, mas repara: ela muda de inclinação ali, forma uma quina. Depois, do lado de fora, o campo cai como um sobre o raio.

## B13 · O resultado contraintuitivo

N038 E agora aparece uma consequência que parece estranha. Escolhe um ponto fora do solenoide ideal. Aqui, o campo magnético é praticamente zero. Mesmo assim, o campo elétrico induzido não é zero.

N039 Isso mostra que a lei de Faraday não diz que o campo elétrico num ponto depende só do campo magnético naquele mesmo ponto. O que entra é a variação do fluxo magnético através da superfície que o caminho limita. O campo elétrico pode existir aqui fora, mesmo que o campo magnético seja desprezível exatamente aqui.

## B14 · Da forma global para a local

N040 Até agora tratamos a lei de Faraday de forma global: o que acontece em volta de um caminho está ligado ao que acontece com o fluxo através da superfície que ele limita. Mas dá para perguntar algo mais local: o que a variação do campo magnético significa em cada pedacinho do espaço?

N041 Vamos organizar a figura. Aqui está a superfície, e aqui o caminho que é a borda dela. O sentido positivo de percorrer o caminho é o anti-horário, em violeta, e a normal sai da tela. Repara que o campo elétrico real, em azul, gira ao contrário: o sentido positivo é uma convenção nossa, não a direção do campo.

N042 A lei na forma integral diz que a circulação do campo elétrico ao longo do caminho é menos a derivada, no tempo, do fluxo do campo magnético pela superfície. Agora entra o teorema de Stokes: a circulação ao longo da borda vira o fluxo do rotacional do campo elétrico pela superfície. Troca no lado esquerdo.

N043 Do lado direito, se a superfície está parada, a derivada em relação ao tempo pode entrar dentro da integral, e vira a derivada parcial do campo magnético em relação ao tempo. Juntando tudo do mesmo lado, a integral, sobre a superfície, de rotacional do campo elétrico mais a derivada parcial do campo magnético, é zero.

N044 Aqui vem o argumento que fecha. Isso vale para qualquer superfície fixa. Pega uma região cada vez menor, cada vez mais perto de um ponto: a integral continua zero. Então o que está dentro dela tem que ser zero em cada ponto. E chegamos à forma local da lei de Faraday: o rotacional do campo elétrico é igual a menos a derivada parcial do campo magnético em relação ao tempo. É a equação de Maxwell–Faraday, uma das equações de Maxwell. E você acabou de construir ela, passo a passo.

## B15 · Local não é global

N045 Mas o exemplo que a gente acabou de resolver impede uma leitura errada dessa equação. Dentro do solenoide, o campo magnético varia. Então a derivada parcial dele no tempo é diferente de zero, e o rotacional do campo elétrico também.

N046 Fora do solenoide ideal, o campo magnético é desprezível e a derivada dele também é zero. Ali, localmente, o rotacional do campo elétrico é zero. Mesmo assim, o campo elétrico não é zero. E olha uma pequena volta aqui fora, que não envolve o eixo: a circulação dela é zero, como o rotacional pede.

N047 Agora pega uma volta grande, que envolve o solenoide inteiro. A circulação dela é menos pi vezes o raio do solenoide ao quadrado, vezes a derivada do campo magnético em relação ao tempo. Diferente de zero! Não existe contradição: rotacional zero localmente não significa campo nulo. E uma volta que envolve a região onde o fluxo varia pode ter circulação diferente de zero.

N048 É justamente por isso que as formas integral e diferencial são duas perspectivas complementares da mesma lei: a global enxerga o caminho inteiro, a local enxerga cada pedacinho.

## B16 · O fio não cria o campo

N049 Agora volta para o circuito do começo. A gente usou o fio porque ele tem cargas livres e deixa a gente observar uma corrente. Mas ele não é a origem desse campo elétrico. Retira a espira. Retira o amperímetro. Deixa só o campo magnético variando no espaço. O campo magnético continua lá, e o campo elétrico induzido também. O fio não cria esse campo. Ele apenas revela a existência dele.

## B17 · Síntese, encerramento e ponte

N050 Então a história completa é esta. Globalmente, uma variação do fluxo magnético está ligada à circulação do campo elétrico. Localmente, o rotacional do campo elétrico é menos a derivada parcial do campo magnético em relação ao tempo. E isso não significa que o campo elétrico só existe onde o campo magnético varia localmente: o solenoide mostrou o contrário.

N051 Se esse vídeo te ajudou a enxergar a lei de Faraday de outro jeito, deixa o like e se inscreve no Parallax Lab. Ajuda muito o canal, e a gente agradece de coração.

N052 E essa história ainda não acabou. A gente viu como um campo magnético que varia cria um campo elétrico. No próximo vídeo, a pergunta é: o que acontece quando o fluxo criado pela própria corrente de um circuito reage às mudanças dessa corrente? É daí que nasce a indutância. E junto vem uma pergunta ainda mais curiosa: onde fica armazenada a energia de um campo magnético? Valeu, pessoal, e até o próximo vídeo!

---

## Pontos em que a animação precisa segurar (a animação se molda à voz)

- **N001 a N004:** manter o circuito vivo (ponteiro e portadores) durante o gancho; título só depois de "Bem-vindos".
- **N009 a N010:** a área acende junto de "área da espira" e o campo magnético pulsa junto de "quem muda"; segurar a troca de `−d/dt[B(t)A]` para `−A dB/dt`.
- **N013 a N015:** a seta de força azul-clara na carga entra em "olha a seta azul-clara"; a equação final só após "tem que dar igual".
- **N018:** os três pontos locais (campo elétrico, pedacinho do caminho e parte tangencial) acendem em sequência com a explicação do produto escalar.
- **N020 e N021:** os sinais (+ e −) entram um a um; segurar o painel da indução até "mesmo sinal".
- **N022 a N025:** corte transversal, eixo, raio do solenoide, convenção anti-horária e só depois os círculos do campo elétrico.
- **N026 a N029:** contorno, área e glyph map do cancelamento seguem a fala; **N033 a N035:** idem no caso externo.
- **N031 e N032:** os três objetos (caminho, superfície, parte com campo magnético) acendem um por vez.
- **N036 e N037:** o ponto do gráfico percorre centro, ramo linear, borda (congela para a continuidade e a quina) e ramo `1/r`.
- **N041 a N044:** cada passo de Stokes na tela espera a fala; o pedaço de superfície encolhe em "região cada vez menor".
- **N046 e N047:** pequena volta externa antes da volta grande envolvente.
- **N049:** o detector sai sozinho; segurar o respiro depois da frase final antes da síntese.
- **N051 e N052:** o end card da série (logo e "próximo vídeo") entra na ponte, sem texto de like e inscrição.
