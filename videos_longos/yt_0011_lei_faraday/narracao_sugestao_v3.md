# yt_0011 — Como um campo magnético cria um campo elétrico? (Lei de Faraday) — narração v3 (rodada de ritmo oral)

Status: **texto para leitura em voz alta. Voz não gerada, sem tags ElevenLabs. `cena.py` não alterado.**

**Palavras faladas:** 2.197 (N001–N053, fora títulos, IDs e marcas de pausa).
**Estimativa a 2,85 palavras por segundo:** 12 min 51 s de fala, sem contar as pausas marcadas (a duração real vem da voz).
Base: `narracao_sugestao_v2.md`. Mesma física, mesma sequência, mesmos blocos B00–B17 e mesmos IDs N001–N053 (nenhum ID foi fundido).

## Principais mudanças em relação à v2

- Frases quebradas para uma respiração cada; pares de orações abstratas desfeitos.
- Menos "então", "agora" e "a gente" em sequência; mais perguntas que o espectador faria (N011, N041).
- N004 introduz "a famosa fem" uma única vez; depois só "força eletromotriz".
- N009 reforça que o que importa é a **rapidez** da variação do campo magnético, não o tamanho dele.
- N011 e N012: a pergunta termina N011 e a resposta ("o campo elétrico") abre N012.
- N023 dividida em respirações, mantendo a ressalva: só o campo induzido pela variação do campo magnético, sem campo eletrostático independente.
- Álgebra (N027–N028, N033–N034, N043): a voz diz a operação e o que cancela; a expressão completa é lida **uma vez só**, não antes e depois.
- N044 reordenada: o argumento ("vale para qualquer superfície, então vale ponto a ponto") vem antes da pausa e da revelação de Maxwell–Faraday; preservado "A gente não começou com ela. A gente chegou nela."
- N046–N048: mantida a distinção campo não nulo / rotacional local zero / pequena volta zero / grande volta não zero, com pausa depois do contraste.
- N052 encurtada (só a ideia central). N053 com uma única pergunta final, sobre a energia magnética.
- Humor: só em N020 (amizade com a eletrostática) e no "Parece errado. Não é." de N003; nenhum na derivação de Stokes, no local × global nem antes do payoff.

## Falas encurtadas

N002, N005, N007, N010, N012, N013, N014, N018, N020, N024, N027, N029, N030, N031, N033, N034, N035, N038, N040, N042, N043, N046, N047, N049, N052, N053.

## Como falar as grandezas (regra: pelo nome, nunca só pela letra)

| Na tela | Na fala |
|---|---|
| B (magenta) | **o campo magnético** |
| E (ciano) | **o campo elétrico** (induzido, quando for o caso) |
| ℰ | **a força eletromotriz** (N004 diz "a famosa fem"; depois só "força eletromotriz") |
| Φ_B | **o fluxo magnético** |
| dB/dt | **a taxa de variação do campo magnético no tempo** (forma integral); "o quanto ele muda a cada segundo" quando for intuição |
| ∂B/∂t | **a derivada parcial do campo magnético em relação ao tempo** (só em Maxwell–Faraday, onde a distinção local importa) |
| A | **a área da espira** |
| u | **a velocidade do condutor** (do fio inteiro, não a das cargas) |
| q | **a carga** |
| F/q | **a força por unidade de carga** |
| ∮ E·dℓ | **a circulação do campo elétrico ao longo do caminho** |
| dℓ | **um pedacinho orientado do caminho** |
| C | **o caminho** |
| S | **a superfície** que o caminho limita |
| R | **o raio do solenoide** |
| r | **o raio do círculo** (ou a distância ao eixo, conforme o contexto) |
| E_φ | **a componente tangencial do campo elétrico** (a que dá a volta no eixo) |
| φ̂, ẑ | **o sentido anti-horário**; **o eixo que sai da tela** |
| ∇×E | **o rotacional do campo elétrico** (sem dizer "nabla cruz") |
| π | **pi** |

Não narrar subscritos. Não dizer "E phi", "B ponto", "R grande", "r pequeno". Operações por extenso ("vezes", "dividido por", "ao quadrado", "igual a", "mais", "menos").

Marcas de pausa (fora da fala): `[pausa curta]`, `[pausa]`, `[respiro visual]`. As durações finais saem do sync.

Evitar: dizer "campo é zero" quando o que é zero é o rotacional; "campo elétrico induzido é sempre circular"; chamar o caminho de linha de campo; dizer que o fio cria o campo.

---

## B00 — Hook, boas-vindas e promessa

**N001**

Olha para esse circuito.

A espira está parada. O fio está parado. Ninguém está girando, puxando ou empurrando nada.

Agora presta atenção no campo magnético, aqui em magenta.

Ele começa a variar...

e o amperímetro responde.

Apareceu corrente.

[pausa curta]

**N002**

E aí tem um problema.

Se o fio inteiro está parado, a explicação da força eletromotriz de movimento não serve.

As cargas se movem dentro do fio, claro. A pergunta é outra.

[pausa curta]

Quem está empurrando essas cargas?

**N003**

Bem-vindos ao Parallax Lab!

Hoje a gente vai entender como a variação de um campo magnético está ligada ao surgimento de um campo elétrico induzido.

E, no caminho, vamos encontrar um resultado bem estranho: existe campo elétrico num lugar onde o campo magnético é praticamente zero.

Parece errado.

Não é.

---

## B01 — Tirando a explicação anterior do caminho

**N004**

Primeiro, vamos eliminar uma possibilidade.

Quando o próprio condutor se move dentro de um campo magnético, aparece uma força magnética por causa desse movimento: a carga vezes o produto vetorial entre a velocidade do condutor e o campo magnético.

Foi esse o mecanismo da força eletromotriz de movimento, a famosa fem.

**N005**

Só que agora a velocidade do condutor é zero.

Atenção: a velocidade do fio inteiro, não a das cargas lá dentro.

O fio não se desloca, então essa contribuição some.

Mas a corrente continua ali.

Ótimo. Agora o problema ficou interessante.

---

## B02 — O paradoxo

**N006**

A força eletromotriz de movimento é zero...

mas a força eletromotriz medida no circuito não é.

[pausa]

Então alguma outra coisa está empurrando as cargas.

E essa é a pergunta que guia o resto do vídeo: se não é o fio se movendo através do campo magnético, qual é o mecanismo agora?

---

## B03 — Faraday já sabe quanto vale

**N007**

A lei de Faraday já prevê o resultado, antes mesmo de a gente entender o mecanismo: uma variação do fluxo magnético está associada a uma força eletromotriz.

Vamos montar isso olhando para a figura.

**N008**

O campo magnético atravessa a espira.

Como ele é uniforme e perpendicular à área, o fluxo magnético é o campo magnético vezes a área da espira.

E repara: a espira está parada. A área não muda, a orientação não muda.

Quem muda é o campo magnético.

**N009**

Colocando isso na lei de Faraday, a derivada atua só no campo magnético, e a área sai de dentro dela.

A força eletromotriz fica igual a menos a área da espira vezes a taxa de variação do campo magnético no tempo.

Em palavras: o que importa não é o tamanho do campo, é a rapidez com que ele muda.

Quanto mais rápido muda, maior a força eletromotriz.

**N010**

Só que isso responde quanto.

Não responde como.

A equação sabe o valor da força eletromotriz, mas não nos contou o que empurra cada carga.

---

## B04 — Quanto não é mecanismo

**N011**

Vamos destacar uma carga no fio.

O circuito continua parado, e a contribuição magnética do movimento continua zero.

Então precisa existir uma força por unidade de carga que não dependa de mexer a espira.

Que força é essa?

---

## B05 — O campo elétrico induzido

**N012**

A peça que faltava é o campo elétrico.

Numa espira parada, a força eletromotriz pode ser escrita como a circulação do campo elétrico ao longo do circuito: em cada pedacinho do caminho, a gente pega quanto do campo aponta ao longo dele, e soma a volta inteira.

**N013**

E isso tem leitura física direta.

Se existe campo elétrico ali, a carga sente uma força elétrica: a carga vezes o campo elétrico.

Para essa força existir, ninguém precisa mover o fio.

**N014**

Agora juntamos as duas descrições da mesma força eletromotriz.

De um lado, a circulação do campo elétrico.

Do outro, menos a taxa de variação do fluxo magnético.

Logo, a circulação do campo elétrico ao redor de um caminho fechado é igual a menos a derivada do fluxo magnético no tempo.

Essa é a lei de Faraday na forma integral.

**N015**

E aqui está a primeira grande virada do vídeo:

um campo magnético que varia no tempo está associado a um campo elétrico, mesmo sem nenhum movimento mecânico do circuito.

[pausa]

O fio só tornou esse campo fácil de detectar.

---

## B06 — Circulação não determina a geometria inteira

**N016**

Mas segura, antes de desenhar círculos por toda parte.

Essa equação nos deu a circulação do campo elétrico.

Ela não determinou, sozinha, a geometria do campo.

E o caminho da integral é uma escolha nossa. Não é, automaticamente, uma linha de campo.

**N017**

Em cada ponto existe um campo elétrico, e um pedacinho orientado do caminho.

Na integral, entra só a parte do campo que aponta ao longo desse pedacinho.

É o produto escalar que aparece na tela.

**N018**

Então Faraday respondeu uma pergunta global: quanto vale a soma dessas contribuições ao redor da volta?

Para descobrir a forma do campo ponto a ponto, falta uma ferramenta: a simetria.

Mas, antes, uma comparação com a eletrostática.

---

## B07 — Eletrostática versus indução

**N019**

Na eletrostática, a circulação ao longo de qualquer caminho fechado é zero.

Algumas contribuições são positivas, outras negativas, e a soma se cancela.

Você volta ao ponto de partida sem acumular nada.

**N020**

Quando o fluxo magnético varia, essa soma não precisa ser zero.

E isso muda a natureza do campo: o campo elétrico induzido, em geral, não é conservativo como o eletrostático.

Se você passou anos achando que campo elétrico só vem de carga parada...

o eletromagnetismo acabou de complicar essa amizade.

---

## B08 — O solenoide ideal

**N021**

Agora vamos escolher uma geometria em que dá para resolver tudo: um solenoide ideal, muito longo, sem efeitos de extremidade.

Olhamos o corte transversal.

Dentro do raio do solenoide, o campo magnético é aproximadamente uniforme.

Fora, nesse modelo ideal, vamos tratá-lo como desprezível.

**N022**

O eixo que sai da tela é a direção positiva.

O campo magnético aponta para fora e está aumentando.

E, para percorrer os caminhos, escolhemos o sentido anti-horário como positivo.

Guarda essa convenção: o sinal da conta depende dela.

**N023**

Agora entra a simetria.

Pontos à mesma distância do eixo são equivalentes por rotação.

Então, neste modelo ideal, o campo elétrico induzido dá a volta no eixo.

Estamos considerando só o campo induzido pela variação do campo magnético, sem somar um campo eletrostático independente.

E a componente que dá a volta depende só da distância ao centro.

**N024**

Só agora aparecem os círculos.

E só porque esta geometria tem essa simetria: o campo elétrico induzido não é sempre circular.

Aqui, ele é.

Como o campo magnético, para fora da tela, está aumentando, a componente no sentido anti-horário sai negativa.

Ou seja: o campo real gira no sentido horário.

[pausa]

A conta vai provar.

---

## B09 — Primeiro caso: dentro

**N025**

Começamos com um círculo de raio menor que o raio do solenoide.

Por simetria, o campo elétrico é tangente ao caminho, com o mesmo módulo em todos os pontos.

A circulação, então, é a componente tangencial vezes o comprimento do círculo: dois pi vezes o raio.

**N026**

Do outro lado da lei, o fluxo magnético.

O círculo está inteiro dentro da região magnética, então a área atravessada é pi vezes o raio ao quadrado.

É essa área que acende na animação.

**N027**

Aplicando Faraday, a componente tangencial vezes dois pi vezes o raio é menos pi vezes o raio ao quadrado, vezes a taxa de variação do campo magnético.

A física acabou.

O resto é álgebra.

**N028**

Divide pelo comprimento do caminho.

Os pi se cancelam, e um dos fatores de raio também.

Sobra: menos metade do raio, vezes a taxa de variação do campo magnético.

**N029**

O sinal negativo confirma o sentido horário.

E o módulo cresce com a distância ao eixo: zero no centro, e em linha reta enquanto a gente se afasta, ainda dentro da região magnética.

---

## B10 — A borda muda a física

**N030**

Agora chegamos ao raio do solenoide, e vale separar três coisas.

O caminho que a gente percorre.

A superfície que ele limita.

E a parte dessa superfície onde existe campo magnético.

Enquanto o círculo está dentro, as duas áreas crescem juntas.

**N031**

Passou da borda, isso muda.

O caminho continua crescendo, a superfície também.

Mas a região atravessada pelo campo magnético não cresce mais: ficou presa ao tamanho do solenoide.

É essa mudança geométrica que vai inverter o comportamento do campo elétrico.

---

## B11 — Segundo caso: fora

**N032**

Agora o círculo é maior que o solenoide.

O fluxo magnético não usa mais a área do círculo: usa só a área da região magnética, pi vezes o raio do solenoide ao quadrado.

**N033**

A circulação continua usando o caminho inteiro: dois pi vezes o raio do círculo.

E a lei de Faraday liga os dois lados, do mesmo jeito que antes.

**N034**

Dividimos de novo pelo comprimento do caminho.

Os pi se cancelam.

Só que agora o raio do solenoide fica fixo, em cima, e o raio do caminho fica embaixo.

A componente tangencial é menos o raio do solenoide ao quadrado, sobre duas vezes o raio do caminho, vezes a taxa de variação do campo magnético.

**N035**

Esse resultado conta uma história simples.

Dentro, aumentar o caminho também aumentava o fluxo.

Fora, o caminho cresce, mas o fluxo não.

Por isso o campo deixa de crescer e passa a cair como o inverso da distância.

---

## B12 — O perfil inteiro

**N036**

Agora junta os dois casos.

O ponto do gráfico e o círculo da esquerda mostram exatamente a mesma distância ao eixo.

Não são duas ilustrações: é a mesma situação física, vista de dois jeitos.

**N037**

No centro, o campo elétrico é zero.

Dentro, o módulo cresce em linha reta.

[pausa]

Na borda, as duas expressões dão o mesmo valor, então o campo é contínuo.

Mas a inclinação muda de repente: o gráfico faz uma quina.

**N038**

Depois da borda, o módulo cai como o inverso da distância.

O perfil é este: sobe em linha reta, atinge o máximo na borda e vai diminuindo.

E agora vem a parte realmente estranha.

---

## B13 — Campo magnético quase zero, campo elétrico não

**N039**

Escolhe um ponto fora do solenoide.

Ali, o campo magnético é desprezível.

Mas o campo elétrico induzido não é zero.

[pausa]

Parece defeito da conta, até você perceber que é justamente o contrário: a física está dizendo algo importante.

**N040**

A lei de Faraday não diz que o campo elétrico num ponto depende só do campo magnético naquele ponto.

Na forma integral, o que importa é a variação do fluxo através da superfície que o caminho limita.

O ponto está fora, mas o caminho que passa por ele ainda envolve a região onde o fluxo muda.

---

## B14 — Da visão global para a visão local

**N041**

Até aqui, a descrição foi global: uma volta inteira, relacionada ao fluxo pela superfície.

Só que aparece uma pergunta natural.

O que essa lei diz localmente, em cada pequena região do espaço?

**N042**

Entra o teorema de Stokes.

Temos uma superfície, o contorno dela e uma orientação.

O sentido positivo do contorno é anti-horário. O campo elétrico real, neste exemplo, é horário.

São coisas diferentes: uma é convenção, a outra é o campo físico.

**N043**

Stokes transforma a circulação ao longo da borda numa integral do rotacional do campo elétrico sobre a superfície.

Do outro lado, como a superfície está parada, a derivada no tempo entra na integral do fluxo.

Agora as duas integrais estão sobre a mesma superfície.

**N044**

E vem o passo conceitual.

Essa relação vale para qualquer superfície fixa que a gente escolha.

Como essa igualdade vale para qualquer superfície fixa apropriada, a relação precisa valer localmente, ponto a ponto.

[pausa]

O rotacional do campo elétrico é igual a menos a derivada parcial do campo magnético em relação ao tempo.

Essa é a equação de Maxwell–Faraday.

A gente não começou com ela.

A gente chegou nela.

---

## B15 — Local e global não são a mesma pergunta

**N045**

O próprio solenoide impede uma leitura errada dessa equação.

Dentro da região magnética, o campo magnético varia no tempo, então o rotacional do campo elétrico não é zero.

Até aqui, tranquilo.

**N046**

Agora olha uma pequena volta inteiramente fora do solenoide.

No modelo ideal, a derivada do campo magnético ali é zero, então o rotacional do campo elétrico também.

A circulação dessa pequena volta é zero.

E, mesmo assim, o campo elétrico naquele lugar não é zero.

**N047**

Agora aumenta o caminho até envolver o solenoide.

A circulação dessa volta grande não é zero, porque a superfície que ela limita atravessa a região onde o fluxo varia.

Duas afirmações, ao mesmo tempo.

Localmente, o rotacional pode ser zero...

e uma volta que envolve a região de fluxo variável pode ter circulação diferente de zero.

[pausa]

**N048**

Não há contradição.

A forma diferencial responde uma pergunta local.

A forma integral responde sobre a volta inteira.

O paradoxo só aparece quando misturamos as duas escalas.

[respiro visual]

---

## B16 — Tire o fio

**N049**

Volta ao circuito do começo.

A gente colocou uma espira ali porque ela tem cargas livres e deixa a gente observar corrente.

Mas ela não é a origem do campo.

Tira a espira.

Tira o amperímetro.

O campo magnético continua variando.

E o campo elétrico induzido continua lá.

**N050**

O fio não cria esse campo.

O fio apenas revela a existência dele.

[respiro visual forte]

---

## B17 — Síntese, CTA e próximo vídeo

**N051**

Então fica com as duas versões da mesma lei.

Globalmente: a variação do fluxo magnético está ligada à circulação do campo elétrico ao redor de um caminho fechado.

Localmente: o rotacional do campo elétrico é menos a derivada parcial do campo magnético em relação ao tempo.

E o solenoide mostrou por que precisamos das duas.

**N052**

Se esse vídeo te ajudou, deixa o like e se inscreve no Parallax Lab.

Ajuda muito o canal.

**N053**

E essa história continua no próximo vídeo.

Até agora, vimos como a variação de um campo magnético produz uma força eletromotriz e revela um campo elétrico induzido.

Mas e quando o fluxo magnético é criado pela própria corrente do circuito?

O que acontece quando essa corrente tenta mudar?

É aí que aparece a indutância, e com ela uma pergunta:

onde fica armazenada a energia de um campo magnético?

Valeu, pessoal.

E até o próximo vídeo.

---

## Registro para a futura sincronização (não é fala)

- **Estado 3 (N006):** depois do paradoxo fica a pausa; não preencher com nova fala. A animação (hoje 4 a 5 s) se molda à voz.
- **Estado 5 (N011):** a fala tem a duração que a ideia pede; se sobrarem segundos na animação (hoje ~8 s), a animação encurta.
- **N033:** só liga os dois lados; o Manim mostra a igualdade e a leitura completa acontece em N034.
- **N044:** a revelação de Maxwell–Faraday só entra depois da pausa.
- **N050:** respiro visual forte antes da síntese; sem texto novo na tela.
