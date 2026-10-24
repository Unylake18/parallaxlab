# yt_0011 — Como um campo magnético cria um campo elétrico? (Lei de Faraday) — sugestão de narração v2 (leitura em voz alta)

Status: **sugestão para revisão. Voz não gerada, sem tags.** Substitui a v1 (`narracao_sugestao.md`) como candidata. A tabela "Como falar as grandezas" da v1 continua valendo: variáveis sempre pelo nome, nunca pela letra.

Princípio: **a voz explica o porquê; o Manim mostra o como.** Os cancelamentos algébricos são guiados pela voz e executados pela animação.

Rodada que falta antes da voz: ritmo oral (trocar palavras que soam bem escritas mas travam faladas), pausas e pronúncia consistente de "rotacional", "fluxo", "força eletromotriz" e "derivada parcial".

---

## B00 — Hook, boas-vindas e promessa

**N001**

Olha para esse circuito.

A espira está parada. O fio está parado. Ninguém está girando nada, puxando nada, empurrando nada.

Agora presta atenção no campo magnético, aqui em magenta.

Ele começa a variar...

e o amperímetro responde.

Apareceu corrente.

**N002**

E aí tem um problema.

Se o fio inteiro está parado, aquela explicação que a gente usou para a força eletromotriz de movimento não pode ser a resposta.

As cargas estão se movendo dentro do fio, claro.

A pergunta é outra:

**quem está empurrando essas cargas?**

**N003**

Bem-vindos ao Parallax Lab!

Hoje a gente vai entender como a variação de um campo magnético está ligada ao surgimento de um campo elétrico induzido.

E, no caminho, a gente vai encontrar um resultado bem estranho:

vai existir campo elétrico num lugar onde o campo magnético é praticamente zero.

Parece errado.

Não é.

---

## B01 — Tirando a explicação anterior do caminho

**N004**

Primeiro, vamos eliminar uma possibilidade.

Quando o próprio condutor se move através de um campo magnético, existe aquela contribuição da força magnética associada ao movimento do fio.

É a carga multiplicada pelo produto vetorial entre a velocidade do condutor e o campo magnético.

Foi esse mecanismo que apareceu na força eletromotriz de movimento.

**N005**

Só que agora a velocidade do condutor é zero.

E atenção: estamos falando da velocidade do **fio inteiro**, não da velocidade das cargas dentro dele.

O condutor não está se deslocando.

Então aquela contribuição magnética causada pelo movimento do fio desaparece.

Mas a corrente continua ali.

Ótimo.

Agora o problema ficou interessante.

---

## B02 — O paradoxo

**N006**

A força eletromotriz associada ao movimento do condutor é zero...

mas a força eletromotriz medida no circuito não é.

Então alguma outra coisa está exercendo força sobre as cargas.

E a pergunta que vai guiar o resto do vídeo é exatamente essa:

**se não é o movimento do fio através do campo magnético, qual é o mecanismo agora?**

---

## B03 — Faraday já sabe quanto vale

**N007**

A lei de Faraday já consegue prever o resultado, mesmo antes de a gente entender o mecanismo.

Ela diz que uma variação do fluxo magnético está associada a uma força eletromotriz.

Vamos construir isso olhando para a própria figura.

**N008**

O campo magnético atravessa a espira.

Como ele é uniforme e perpendicular à área, o fluxo magnético é o campo magnético multiplicado pela área da espira.

E repare numa coisa importante:

a espira está parada.

A área não muda.

A orientação não muda.

Quem muda é o campo magnético.

**N009**

Então, quando colocamos essa expressão dentro da lei de Faraday, a derivada atua sobre o campo magnético.

A área permanece constante.

E chegamos a uma força eletromotriz igual a menos a área da espira multiplicada pela taxa de variação do campo magnético no tempo.

Ou, falando sem fórmula:

quanto mais rápido o campo magnético muda, maior é a força eletromotriz induzida.

**N010**

Só que isso responde **quanto**.

Ainda não responde **como**.

A equação já sabe o valor da força eletromotriz.

Mas ela ainda não contou para a gente o que está empurrando cada carga.

---

## B04 — Quanto não é mecanismo

**N011**

Vamos destacar uma carga no fio.

O circuito continua parado.

A contribuição magnética causada pelo movimento do condutor continua zero.

Então precisamos encontrar uma força por unidade de carga que exista mesmo com a espira inteira imóvel.

E agora aparece a peça que estava faltando.

---

## B05 — O campo elétrico induzido

**N012**

Para uma espira estacionária, a força eletromotriz pode ser escrita como a circulação do campo elétrico ao longo do circuito.

Ou seja: em cada pedacinho do caminho, a gente mede quanto o campo elétrico aponta na direção daquele pedacinho e soma isso ao redor da volta inteira.

**N013**

E isso tem uma interpretação física direta.

Se existe um campo elétrico ali, uma carga sente uma força elétrica igual à carga multiplicada pelo campo elétrico.

Não precisamos mover o fio para essa força existir.

**N014**

Agora juntamos as duas descrições da mesma força eletromotriz.

De um lado, a circulação do campo elétrico.

Do outro, menos a taxa de variação do fluxo magnético.

Portanto:

a circulação do campo elétrico ao redor de um caminho fechado é igual a menos a derivada do fluxo magnético em relação ao tempo.

Essa é a lei de Faraday na forma integral.

**N015**

E aqui está a primeira grande virada do vídeo:

um campo magnético que varia no tempo está associado a um campo elétrico mesmo quando não existe nenhum movimento mecânico do circuito.

O fio só tornou esse campo fácil de detectar.

---

## B06 — Circulação não determina a geometria inteira

**N016**

Mas segura um pouco antes de desenhar círculos por toda parte.

Essa equação nos deu a **circulação** do campo elétrico.

Ela ainda não determinou sozinha a geometria completa desse campo.

E o caminho que aparece na integral é justamente isso: um caminho que **nós escolhemos**.

Não é automaticamente uma linha de campo.

**N017**

Em cada ponto, existe um campo elétrico.

E existe também um pequeno pedaço orientado do caminho.

Na integral, entra a parte do campo elétrico que aponta ao longo desse pedaço.

Essa é a ideia do produto escalar que está aparecendo na tela.

**N018**

Então Faraday já respondeu uma pergunta global:

qual é a soma dessas contribuições ao redor da volta?

Para descobrir a forma do campo ponto a ponto, precisamos de mais uma ferramenta:

**simetria.**

Mas antes, vale comparar esse campo com o campo elétrico que a gente conhece da eletrostática.

---

## B07 — Eletrostática versus indução

**N019**

Num campo eletrostático, a circulação ao longo de qualquer caminho fechado é zero.

Ao percorrer a volta, algumas contribuições podem ser positivas, outras negativas, mas a soma completa se cancela.

Você volta para o ponto de partida sem acumular uma diferença líquida ao longo daquela volta.

**N020**

Quando o fluxo magnético varia, essa soma não precisa mais ser zero.

E isso muda bastante a natureza do campo.

O campo elétrico induzido por essa variação de fluxo não é, em geral, um campo eletrostático conservativo.

Se você passou anos fazendo amizade com a ideia de que campo elétrico sempre vem de carga parada...

o eletromagnetismo resolveu complicar essa amizade.

---

## B08 — O solenoide ideal

**N021**

Agora vamos escolher uma geometria em que dá para resolver tudo.

Vamos usar um solenoide ideal muito longo e desprezar os efeitos das extremidades.

Estamos olhando um corte transversal.

Dentro do raio do solenoide, o campo magnético é aproximadamente uniforme.

Fora, nesse modelo ideal, vamos tratá-lo como desprezível.

**N022**

Escolhemos o eixo que sai da tela como direção positiva.

O campo magnético aponta para fora da tela e está aumentando.

Para percorrer os caminhos, escolhemos o sentido anti-horário como positivo.

Guarda essa convenção.

O sinal que vai aparecer daqui a pouco depende dela.

**N023**

Agora usamos a simetria.

Pontos que estão à mesma distância do eixo são equivalentes por rotação.

E, neste modelo ideal, considerando apenas o campo elétrico induzido pela variação do campo magnético, sem acrescentar um campo eletrostático independente, o campo induzido aponta ao redor do eixo.

O valor da sua componente tangencial depende apenas da distância ao centro.

**N024**

Só agora os círculos aparecem.

E só porque essa geometria tem essa simetria.

O campo elétrico induzido não é "sempre circular".

Aqui ele é.

E como o campo magnético para fora da tela está aumentando, a componente definida como positiva no sentido anti-horário vai sair negativa.

Ou seja: o campo elétrico real gira no sentido horário.

Vamos deixar a conta provar isso.

---

## B09 — Primeiro caso: dentro

**N025**

Começamos com um círculo de raio menor que o raio do solenoide.

Por simetria, o campo elétrico é tangente ao caminho e tem o mesmo módulo em todos os pontos desse círculo.

Então a circulação vira a componente tangencial do campo elétrico multiplicada pelo comprimento da circunferência.

Esse comprimento é dois pi vezes o raio do círculo.

**N026**

Do outro lado da lei temos o fluxo magnético.

Como o círculo ainda está inteiro dentro da região magnética, a área atravessada pelo campo é pi vezes o raio ao quadrado.

É exatamente essa área que está acendendo na animação.

**N027**

Aplicando Faraday, a componente tangencial do campo elétrico multiplicada por dois pi vezes o raio é igual a menos pi vezes o raio ao quadrado multiplicado pela taxa de variação do campo magnético.

Agora a física acabou.

O resto é álgebra.

**N028**

Dividimos pelo comprimento do caminho, dois pi vezes o raio.

Os fatores de pi se cancelam.

Um dos fatores de raio também se cancela.

E sobra a componente tangencial do campo elétrico igual a menos metade do raio multiplicada pela taxa de variação do campo magnético.

**N029**

O sinal negativo confirma o sentido horário que a gente previu.

E o módulo cresce proporcionalmente à distância ao eixo.

No centro, ele começa em zero.

Conforme nos afastamos, ainda dentro da região magnética, ele cresce em linha reta.

---

## B10 — A borda muda a física

**N030**

Agora chegamos ao raio do solenoide.

E aqui vale prestar atenção em três coisas diferentes.

Existe o caminho que estamos percorrendo.

Existe a superfície delimitada por esse caminho.

E existe a parte dessa superfície onde realmente há campo magnético.

Enquanto o círculo está dentro do solenoide, essas duas áreas crescem juntas.

**N031**

Mas depois que o círculo ultrapassa a borda, isso muda.

O caminho continua crescendo.

A superfície delimitada por ele também.

Só que a região atravessada pelo campo magnético não cresce mais.

Ela ficou presa ao tamanho do solenoide.

E é exatamente essa mudança geométrica que vai inverter o comportamento do campo elétrico.

---

## B11 — Segundo caso: fora

**N032**

Agora o raio do círculo é maior que o raio do solenoide.

O fluxo magnético não usa mais a área do círculo inteiro.

Ele usa apenas a área da região onde existe campo magnético:

pi vezes o raio do solenoide ao quadrado.

**N033**

A circulação ainda usa o comprimento completo do caminho, dois pi vezes o raio do círculo.

Então a lei de Faraday nos dá a componente tangencial multiplicada por esse comprimento igual a menos pi vezes o raio do solenoide ao quadrado multiplicado pela taxa de variação do campo magnético.

**N034**

Dividimos novamente pelo comprimento do caminho.

Os fatores de pi se cancelam.

Mas agora o raio do solenoide fica fixo no numerador, enquanto o raio do caminho fica no denominador.

E chegamos à componente tangencial do campo elétrico igual a menos o raio do solenoide ao quadrado, dividido por duas vezes o raio do caminho, multiplicado pela taxa de variação do campo magnético.

**N035**

Esse resultado conta uma história bem simples.

Dentro, aumentar o caminho também aumentava a região de fluxo.

Fora, o caminho continua crescendo, mas o fluxo não.

Por isso o módulo do campo elétrico deixa de crescer e passa a cair como o inverso da distância.

---

## B12 — O perfil inteiro

**N036**

Agora junta os dois casos.

O ponto no gráfico e o círculo da esquerda representam exatamente a mesma distância ao eixo.

Não são duas ilustrações diferentes.

É a mesma situação física vista de duas maneiras.

**N037**

No centro, o campo elétrico é zero.

Dentro do solenoide, o módulo cresce linearmente.

Ao chegar à borda, as duas expressões dão exatamente o mesmo valor.

Então o campo é contínuo ali.

Mas a inclinação muda de repente: o gráfico faz uma quina.

**N038**

E depois da borda, o módulo passa a cair como o inverso da distância.

Então temos um perfil bem característico:

cresce em linha reta, atinge o máximo na borda e depois vai diminuindo.

E agora vem a parte realmente estranha.

---

## B13 — Campo magnético quase zero, campo elétrico não

**N039**

Escolhe um ponto fora do solenoide ideal.

Nesse ponto, o campo magnético é desprezível.

Mas o campo elétrico induzido não é zero.

Esse é um daqueles resultados que parecem defeito da conta até você perceber que é justamente o contrário.

É a física dizendo alguma coisa importante.

**N040**

A lei de Faraday não está dizendo que o campo elétrico em um ponto é determinado apenas pelo valor do campo magnético naquele mesmo ponto.

Na forma integral, o que importa é a variação do fluxo magnético através da superfície limitada pelo caminho.

O ponto está fora.

Mas o caminho que passa por ele ainda pode envolver toda a região onde o fluxo está mudando.

---

## B14 — Da visão global para a visão local

**N041**

Até agora, nossa descrição foi global.

A gente olha uma volta inteira e relaciona essa circulação ao fluxo através da superfície.

Mas agora aparece uma pergunta natural:

o que essa lei está dizendo **localmente**, em cada pequena região do espaço?

**N042**

Aqui entra o teorema de Stokes.

Temos uma superfície, seu contorno e uma orientação.

O sentido positivo do contorno é anti-horário.

O campo elétrico real, nesse exemplo, aponta no sentido horário.

Essas duas coisas não são a mesma coisa.

Uma é uma convenção de orientação.

A outra é o campo físico.

**N043**

Stokes transforma a circulação do campo elétrico ao longo da borda em uma integral do rotacional do campo elétrico sobre a superfície.

Do outro lado, como a superfície está parada, a derivada temporal entra na integral do fluxo magnético.

Então as duas integrais passam a estar escritas sobre a mesma superfície.

**N044**

E agora vem o passo conceitual.

Essa relação vale para qualquer superfície fixa apropriada.

Se ela vale para qualquer região que a gente escolha, então a igualdade precisa valer ponto a ponto.

E chegamos à forma local da lei de Faraday:

o rotacional do campo elétrico é igual a menos a derivada parcial do campo magnético em relação ao tempo.

Essa é a equação de Maxwell–Faraday.

A gente não começou com ela.

A gente chegou nela.

---

## B15 — Local e global não são a mesma pergunta

**N045**

E agora o próprio solenoide impede uma interpretação errada dessa equação.

Dentro da região magnética, o campo magnético varia no tempo.

Então o rotacional do campo elétrico é diferente de zero.

Até aqui, tranquilo.

**N046**

Mas olha para uma pequena volta inteiramente fora do solenoide.

Ali, no modelo ideal, a derivada temporal do campo magnético é zero.

Então o rotacional do campo elétrico também é zero naquela região.

E a circulação em uma pequena volta que fica totalmente ali fora também é zero.

Só que o campo elétrico naquele lugar não é zero.

**N047**

Agora aumente o caminho até ele envolver o solenoide.

A situação muda.

A circulação dessa volta grande não é zero, porque a superfície limitada por ela atravessa a região onde o fluxo magnético varia.

Então temos duas afirmações ao mesmo tempo:

localmente, o rotacional pode ser zero...

e globalmente, uma volta que envolve a região de fluxo variável pode ter circulação diferente de zero.

**N048**

Não existe contradição.

A forma diferencial responde uma pergunta local.

A forma integral responde uma pergunta sobre a volta inteira.

Misturar as duas escalas é que cria o paradoxo.

---

## B16 — Tire o fio

**N049**

Agora volta para o circuito do começo.

A gente colocou uma espira ali porque ela tem cargas livres e permite observar corrente.

Mas ela não é a origem do campo elétrico induzido.

Então vamos fazer um teste simples.

Tira a espira.

Tira o amperímetro.

O campo magnético continua variando.

E o campo elétrico induzido continua existindo.

**N050**

Esse é o payoff do vídeo:

**o fio não cria o campo.**

O fio apenas revela a existência dele.

---

## B17 — Síntese, CTA e próximo vídeo

**N051**

Então fica com essas duas versões da mesma lei.

Globalmente, a variação do fluxo magnético está ligada à circulação do campo elétrico ao redor de um caminho fechado.

Localmente, o rotacional do campo elétrico é igual a menos a derivada parcial do campo magnético em relação ao tempo.

E o exemplo do solenoide mostrou por que precisamos das duas.

**N052**

Se esse vídeo te ajudou a enxergar a lei de Faraday de um jeito diferente, deixa o like e se inscreve no Parallax Lab.

Ajuda bastante o canal e permite que a gente continue construindo essas ideias com calma, sem pular justamente a parte que faz a física fazer sentido.

**N053**

E essa história continua no próximo vídeo.

Até agora, um campo magnético variável produziu uma força eletromotriz e revelou um campo elétrico induzido.

Mas e quando o fluxo magnético é criado pela **própria corrente do circuito**?

O que acontece quando essa corrente tenta mudar?

É aí que aparece a indutância.

E com ela vem a próxima pergunta:

**onde fica armazenada a energia de um campo magnético?**

Valeu, pessoal.

E até o próximo vídeo.
