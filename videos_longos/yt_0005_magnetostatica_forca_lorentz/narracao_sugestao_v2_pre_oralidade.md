# yt_0005 — Magnetostática: narração (v2, reescrita integral, antes de qualquer TTS)

Status: **texto para revisão humana. Sem audio tags, sem voz, sem SRT, sem `texto_narracao.txt`.** Fonte da fala: este Markdown.
Ordem de produção: **física → narração natural → remapeamento da animação → duração resultante.** A duração é consequência da explicação, não limite dela. Nenhum bloco foi cortado por causa de tempo: B00 a B09 e o CTA estão completos, inclusive a continuidade (B06) e Thomson (B07 e B08).

> **TEMPOS NÃO SÃO LIMITES.** A coluna "Tempo atual" é só uma referência do contínuo `renders/entrega_pre_narracao/yt0005_continuo_pre_narracao_540p30.mp4` (14:57). A sincronização final é por **âncora visual** (o acontecimento na tela que a frase acompanha) e a animação será remapeada para caber na voz.

Princípio de todo trecho: (1) o que queremos descobrir; (2) que informação já temos; (3) por que esta operação ajuda; (4) o que o resultado significa fisicamente. **A voz explica a intenção, a origem dos termos, a justificativa e a interpretação; o Manim mostra as operações, os deslocamentos, os vetores, os gráficos e a geometria.** A fala não lê a álgebra.

Formato das tabelas: `| Tempo atual | Âncora visual | Fala |`.

## Como falar as grandezas (nome por extenso; o símbolo só aparece associado ao nome uma vez, quando nasce na tela)

| Na tela | Na fala |
|---|---|
| I₁, I₂, I | **a corrente do primeiro fio**, **a corrente do segundo fio**, **a corrente** |
| **F**, **F**_B | **a força**; **a força magnética** |
| q | **a carga elétrica** |
| **v**, módulo de **v** | **o vetor velocidade**; **a rapidez** (quando é o módulo) |
| v_∥ | **a componente da velocidade paralela ao campo** |
| v_⊥ | **a componente perpendicular da velocidade** (depois: **a velocidade perpendicular**) |
| **B**, **E** | **o campo magnético**; **o campo elétrico** |
| θ | **o ângulo entre a velocidade e o campo magnético** |
| v_x, v_y, v_z | **a componente da velocidade ao longo do campo**; **a componente horizontal da velocidade**; **a componente vertical da velocidade** |
| m | **a massa** |
| dv/dt | **a aceleração** (ou **a taxa de variação da velocidade no tempo**) |
| ω_c | **a frequência angular ciclotrônica** |
| R | **o raio da órbita** |
| T | **o período** |
| p | **o passo da hélice** |
| C₁, C₂ | **a primeira constante da solução**, **a segunda constante da solução** |
| P, W | **a potência**, **o trabalho** |
| E_c | **a energia cinética** (nunca confundir com o campo elétrico) |
| dr | **um pequeno deslocamento** |
| dℓ | **um pequeno elemento de comprimento** |
| dq | **uma pequena quantidade de carga** |
| dt | **um pequeno intervalo de tempo** |
| λ | **lambda, a densidade linear de carga** (1ª vez); depois **a densidade linear de carga** |
| σ | **sigma, a densidade superficial de carga** (1ª vez); depois **a densidade superficial de carga** |
| ρ | **rô, a densidade volumétrica de carga** (1ª vez); depois **a densidade volumétrica de carga** |
| **K** | **a densidade superficial de corrente** |
| **J** | **a densidade de corrente** (se precisar: **densidade volumétrica de corrente**) |
| d**a** | **um elemento vetorial de área, orientado pela normal** |
| dτ | **um pequeno elemento de volume** |
| Q_int | **a carga dentro do volume** |
| ∇·**J** | **o divergente da densidade de corrente** |
| ∂ρ/∂t | **a taxa local de variação da densidade de carga** |
| E/B | **o campo elétrico dividido pelo campo magnético** |
| E/(B²R) | **o campo elétrico dividido pelo produto entre o quadrado do campo magnético e o raio** |

Operações por extenso: "vezes", "dividido por", "ao quadrado", "mais", "menos", "igual a", "seno", "cosseno", "derivada em relação ao tempo", "integral", "produto escalar", "produto vetorial". Nunca "J é rô v" nem "dq é lambda dℓ": **"a densidade de corrente é a densidade volumétrica de carga multiplicada pela velocidade"** e **"a pequena quantidade de carga é a densidade linear de carga multiplicada pelo pequeno elemento de comprimento"**.

Evitar: "a velocidade que atravessa o campo" (linhas de campo não são obstáculos materiais); "a força magnética gira a velocidade, não acelera"; "o sinal de menos é a conservação"; "a carga líquida é zero, então a força não é elétrica"; "a massa efetiva aumenta"; "divergente zero obriga linhas fechadas".

---

## B00 — Abertura e gancho

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 0:00 | título MAGNETOSTÁTICA e a pergunta "O que um campo magnético realmente faz?" | Fala, pessoal! Bem-vindos de volta ao Parallax Lab. Hoje o assunto é magnetostática, e a gente começa com uma pergunta que parece simples: o que um campo magnético realmente faz? |
| 0:06 | entram os dois fios paralelos, cada um com sua corrente no mesmo sentido, e os pulsos verdes correm | Pega dois fios de metal, paralelos, eletricamente neutros como um todo. Agora faz passar uma corrente em cada um deles, no mesmo sentido. |
| 0:09 | as barras se curvam uma na direção da outra; setas de força | O que acontece? Os dois fios se atraem. Repara que ninguém encostou neles: existe uma interação à distância, e ela aparece só porque tem corrente passando. |
| 0:12 | a corrente do segundo fio inverte; as barras relaxam e se afastam; setas de força para fora | Agora inverte o sentido da corrente em um dos fios. E a interação muda de natureza: em vez de atração, repulsão. |
| 0:15 | legenda da cena sobre a carga líquida | E aqui tem um detalhe curioso. Cada fio, como um todo, é neutro. Mesmo sem carga líquida macroscópica, existe transporte de carga, e existe uma interação entre os fios. Então a pergunta é: por que mudar o sentido desse transporte muda a interação? |
| 0:18 | uma lente se fecha sobre um pedaço do fio; "olhando para uma carga em movimento" | Pra responder, a gente não vai olhar o fio inteiro. Vai aproximar a imagem até enxergar uma única carga em movimento, e entender o que o campo magnético faz com ela. |

*Comentário científico:* a observação é a de Ampère (1820): correntes paralelas no mesmo sentido se atraem, em sentidos opostos se repelem. Neutralidade líquida **não** permite concluir, sozinha, nada sobre a presença ou a ausência de campo elétrico: o vídeo usa a neutralidade só como surpresa e não deduz daí que a interação é de uma natureza ou de outra. A explicação completa de onde vem o campo é o tema do próximo vídeo.

---

## B01 — A força de Lorentz e a geometria da força magnética

### B01.1 — A força de Lorentz

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 0:25 | aparece uma carga positiva com o vetor velocidade; as linhas de campo magnético entram | Aqui está a nossa carga elétrica, que na tela aparece como q, positiva, se movendo com uma certa velocidade. Em volta dela, as linhas do campo magnético. Lembrando: essas linhas são um jeito de desenhar o campo. Elas não são obstáculos, a carga passa por elas sem esbarrar em nada. |
| 0:32 | a lei completa F = q(E + v × B) aparece | A força que um campo eletromagnético faz sobre uma carga tem duas partes. Uma vem do campo elétrico, e essa existe mesmo com a carga parada. A outra vem do campo magnético, e essa só existe se a carga está em movimento. Juntas, elas formam a força de Lorentz. |
| 0:35 | o termo elétrico sai; sobra a força magnética numa caixa | Hoje o foco é só a segunda parte, a força magnética: a carga elétrica multiplicada pelo produto vetorial entre o vetor velocidade e o campo magnético. |

### B01.2 — Direção e sentido: a regra da mão direita

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 0:40 | surgem a linha auxiliar paralela ao campo e o ângulo θ; o símbolo ⊗ da força aparece junto à carga | O produto vetorial dá um vetor perpendicular ao plano formado pela velocidade e pelo campo magnético. Só que perpendicular a um plano são dois sentidos possíveis. Então, como a gente escolhe um? |
| 0:42 | o símbolo ⊗ cresce, com a nota "entra na tela" | Pela regra da mão direita, e a ordem importa: primeiro o vetor velocidade, depois o campo magnético. Aponta os dedos da mão direita no sentido da velocidade e fecha os dedos em direção ao campo magnético. O polegar mostra o sentido do produto vetorial. Para uma carga positiva, esse é o sentido da força magnética. |
| 0:44 | destaque no símbolo ⊗ | Nesse desenho, o resultado é um vetor entrando na tela. E o símbolo de um xis dentro de um círculo representa exatamente isso: a parte de trás de uma seta que está entrando na tela. Quando a força sai da tela, o símbolo é um ponto dentro de um círculo: a ponta de uma seta vindo na nossa direção. |

### B01.3 — O módulo da força

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 0:44 | a fórmula do módulo; as leituras do ângulo e do seno | Agora, o tamanho dessa força. O módulo da força magnética é o módulo da carga, vezes a rapidez, vezes a intensidade do campo magnético, vezes o seno do ângulo entre a velocidade e o campo. Repara que aqui eu falei rapidez, e não velocidade: é só o tamanho do vetor velocidade que entra no módulo. |
| 0:47 | o ângulo varia de sessenta até oitenta e cinco graus e volta para quarenta; as leituras do seno acompanham | Mantendo fixos o módulo da carga, a rapidez e o campo, o que muda é só o ângulo. Quando o ângulo diminui, o seno diminui, e a força fica menor. Quando o ângulo se aproxima de noventa graus, o seno se aproxima de um, e a força se aproxima do máximo. |
| 0:50 | o ângulo vai a zero; aparece "velocidade paralela ao campo: força nula" | E nos extremos: se a velocidade é paralela ao campo, o ângulo é zero, o seno é zero, e a força magnética é nula. Se for antiparalela, o ângulo é cento e oitenta graus, e o seno também é zero. E se a carga está parada, a rapidez é zero, e o termo magnético é nulo. |
| 0:53 | o ângulo passa por quarenta e cinco graus; depois chega a noventa; "força máxima" | Entre esses extremos, a força cresce. E quando a velocidade é perpendicular ao campo, o seno vale um e a força é a máxima possível para aquela rapidez e aquele campo. |

### B01.4 — O sinal da carga

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 0:56 | aparece "q > 0 ⇒ ⊗"; depois a carga troca de sinal, com um clarão, e vira "q < 0 ⇒ ⊙" | E o sinal da carga? O produto vetorial da velocidade pelo campo é o mesmo. Mas a força magnética é a carga vezes esse produto. Então, para uma carga negativa, a gente aplica a regra da mão direita do mesmo jeito e inverte o sentido do resultado. |
| 0:59 | a nota "mesmo módulo, sentido oposto" | O módulo da força continua o mesmo. O que muda é só o sentido: de entrando na tela, passa a saindo da tela. |

### B01.5 — Só a componente perpendicular importa

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 1:02 | o diagrama ganha espaço; a velocidade se decompõe, com setas violeta e branca e linhas tracejadas | A gente pode organizar tudo isso decompondo o vetor velocidade em duas componentes: uma na direção do campo magnético e outra perpendicular a ele. |
| 1:05 | a componente da velocidade paralela ao campo; "produto vetorial dela com o campo é zero" | A componente paralela ao campo, quando entra no produto vetorial com o campo, dá zero. Ela não contribui em nada para a força magnética. |
| 1:08 | a componente perpendicular, com a fórmula da força magnética escrita só com ela | Toda a força magnética vem da componente perpendicular à direção do campo: a carga vezes a componente perpendicular da velocidade, vezes o campo, em produto vetorial. A força é a mesma de antes, só escrita de um jeito mais econômico. |

### B01.6 — Uma escolha de caso

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 1:14 | o painel mostra "v = v perpendicular" e, depois, "agora vamos escolher o caso: componente paralela igual a zero" | Pra estudar o movimento da carga, a gente vai escolher um caso, só pra começar: a componente da velocidade paralela ao campo vale zero. Então a velocidade é só a perpendicular. Essa é uma condição inicial que a gente escolhe, não uma regra da natureza. Mais adiante, a gente tira essa restrição. |

*Comentário científico:* a força magnética é o termo dependente da velocidade na força de Lorentz (Lorentz, 1895; Heaviside e Thomson trabalharam formas anteriores). O sentido vem do produto vetorial, que é um pseudovetor: por isso a regra da mão direita, e por isso o sinal da carga inverte o sentido. A linha de campo é uma representação gráfica; a força depende do valor do campo no ponto onde a carga está.

---

## B02 — A trajetória nasce da lei de Lorentz

### B02.1 — A vista muda; os eixos e as hipóteses

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 1:20 | a vista gira até olhar ao longo do campo; as linhas viram pontos; "a perspectiva muda; a física não" | Agora a gente muda o ponto de vista: olha ao longo da direção do campo magnético. Visto assim, as linhas de campo viram pontinhos, saindo da tela. A perspectiva muda, mas a física é exatamente a mesma. |
| 1:26 | aparecem os eixos y e z e a legenda "B ao longo de x"; B = B x̂; v = (v_x, v_y, v_z) | Agora vamos escolher os eixos com o campo magnético apontando ao longo do eixo x. Com isso, o vetor velocidade tem três componentes: uma ao longo do campo, e duas no plano perpendicular a ele, uma na horizontal e outra na vertical. |
| 1:28 | aparece a legenda das hipóteses | Antes de começar a conta, três hipóteses, que valem pra toda essa análise do movimento. Primeira: o campo magnético é uniforme, quer dizer, tem a mesma intensidade e a mesma direção em todos os pontos da região que a gente analisa. Segunda: ele é constante, quer dizer, não varia com o tempo. Terceira: o regime é não relativístico, ou seja, as velocidades são pequenas o bastante, comparadas com a velocidade da luz, pra dinâmica de Newton ser uma boa aproximação. E vamos considerar só a força magnética agindo sobre a carga. |

### B02.2 — O produto vetorial por componentes

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 1:32 | o determinante entra, com x̂, ŷ, ẑ na primeira linha; as componentes da velocidade na segunda; o campo, zero e zero na terceira | Agora uma pergunta concreta: o que queremos descobrir é como cada componente da velocidade produz aceleração nas outras direções. E o produto vetorial entre a velocidade e o campo responde a isso. Pra calcular, a gente monta um determinante. Na primeira linha, os três vetores unitários, um para cada direção. Na segunda, as componentes da velocidade. Na terceira, as componentes do campo: a intensidade do campo, zero e zero. |
| 1:38 | o menor da direção do campo é destacado; o resultado "= 0" aparece; "força ao longo do campo igual a zero" | Começando pela direção ao longo do campo. Cobre a linha e a coluna dessa direção, e sobram quatro números: a componente horizontal vezes zero, menos a componente vertical vezes zero. Tudo vezes zero. Então não existe força ao longo do campo. Isso confirma o que a gente já sabia: o campo magnético não age na própria direção dele. |
| 1:41 | o menor da direção horizontal é destacado, com as setas tracejadas que mostram quais termos se multiplicam | Agora a direção horizontal. Cobre a linha e a coluna dessa direção. O que sobra é a componente ao longo do campo vezes zero, menos a componente vertical vezes o campo. Esse menor vale menos o campo vezes a componente vertical. Só que a posição dessa direção no determinante traz um sinal negativo na frente. Menos vezes menos dá mais. O resultado final é positivo: o campo vezes a componente vertical, na direção horizontal. |
| 1:44 | o menor da direção vertical é destacado; o resultado aparece | Por fim, a direção vertical. Cobrindo linha e coluna, sobra a componente ao longo do campo vezes zero, menos a componente horizontal vezes o campo. Aqui a posição não traz sinal negativo extra, então o sinal negativo do menor permanece: menos o campo vezes a componente horizontal, na direção vertical. |
| 1:50 | os três resultados se juntam: v × B = (0, B v_z, −B v_y) | Juntando tudo: zero na direção do campo, o campo vezes a componente vertical na direção horizontal, e menos o campo vezes a componente horizontal na direção vertical. Repara numa coisa importante: cada uma dessas duas direções depende da componente da velocidade da outra direção. Guarda essa troca, porque tudo o que vem depois nasce dela. E um lembrete: isso é só o produto vetorial entre a velocidade e o campo. Pra ter a força magnética, ainda falta multiplicar pela carga elétrica. |

### B02.3 — Newton + Lorentz: as equações do movimento

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 1:56 | "Newton + Lorentz": massa vezes aceleração igual à carga vezes o resultado do produto vetorial | Agora entra a segunda lei de Newton: a massa vezes a aceleração é igual à força total. Aqui, a força total é só a força magnética, que acabamos de calcular, já multiplicada pela carga. Então a lei de Lorentz deixa de dizer só para onde a força aponta. Junto com Newton, ela passa a determinar o movimento. |
| 2:02 | as três equações por componente surgem, uma por vez; a primeira ganha a legenda "v_x constante" | Separando por componentes, saem três equações. A primeira: a aceleração ao longo do campo é zero. Então a componente da velocidade ao longo do campo é constante. É a componente que o campo magnético não consegue alterar. |
| 2:08 | a segunda equação; depois a terceira | As outras duas são mais interessantes. A aceleração na direção horizontal é igual à carga vezes o campo, dividido pela massa, multiplicado pela componente vertical da velocidade. E a aceleração na direção vertical é igual a menos esse mesmo fator, multiplicado pela componente horizontal da velocidade. Ou seja: a componente vertical determina a aceleração horizontal, a horizontal determina a vertical, com sinal oposto. Uma componente alimenta a outra. E uma observação: uma componente negativa da velocidade significa só movimento no sentido negativo do eixo. Não existe rapidez negativa. |

### B02.4 — Desacoplar, substituir e fazer nascer a frequência

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 2:14 | a aceleração horizontal é derivada; aparece a segunda derivada | Temos duas funções desconhecidas misturadas uma na outra. O que a gente quer é uma equação que envolva só uma delas. Pra isso, derivamos a equação da componente horizontal mais uma vez em relação ao tempo. O fator carga vezes campo dividido pela massa sai da derivada sem mudar, porque, neste problema, essas três grandezas são constantes. |
| 2:20 | a terceira equação sobe e a derivada da componente vertical é substituída | Do lado direito sobrou a derivada da componente vertical. E essa a gente já conhece: é exatamente o que diz a terceira equação. Então substituímos, usando uma informação que já tínhamos. Repara de onde veio cada pedaço: o mesmo fator, carga vezes campo dividido pela massa, que já estava ali, e agora aparece de novo, com sinal negativo, multiplicando a componente horizontal. |
| 2:26 | o fator aparece ao quadrado; a equação ganha o título "Equação do oscilador harmônico para a componente horizontal" | Juntando os dois fatores, ele aparece ao quadrado, com sinal negativo. Passando tudo para o mesmo lado: a segunda derivada da componente horizontal, mais esse fator ao quadrado vezes a própria componente, é igual a zero. Essa é a equação do oscilador harmônico. Atenção: quem obedece a essa equação é uma componente da velocidade. A partícula não é uma massa presa a uma mola. O que a gente tem é a mesma estrutura matemática do oscilador. |
| 2:32 | a forma geral: segunda derivada de uma função mais ω² vezes a função, igual a zero | Essa forma é conhecida: a segunda derivada de uma função mais uma constante ao quadrado vezes a própria função é igual a zero. Em física, quem faz o papel dessa constante é a frequência angular, que mede a taxa com que a fase avança, em radianos por segundo. Então a frequência angular ao quadrado é igual ao fator carga vezes campo dividido pela massa, tudo ao quadrado. |
| 2:35 | a expressão ω² é substituída pelo módulo da raiz, depois por ω_c = ∣q∣B/m | Tirando a raiz, a gente escolhe o valor positivo, porque queremos caracterizar o quão rápido a fase gira. O sinal da carga fica responsável pelo sentido da rotação. Resultado: a frequência angular é o módulo da carga vezes o campo magnético, dividido pela massa. Esta é a frequência angular ciclotrônica. E repara: ela nasceu da equação de movimento. Não foi definida à mão. |
| 2:38 | a caixa com a frequência angular ciclotrônica e o nome; a legenda "sinal de q ⇒ sentido de rotação" | Ela depende do módulo da carga, da intensidade do campo e da massa. Carga maior, campo mais forte, partícula mais leve: giro mais rápido. |

### B02.5 — A solução, as constantes e as condições iniciais

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 2:44 | "derivar 2× troca o sinal: qual função?" | Agora, a pergunta. Qual função, derivada duas vezes, volta com o sinal trocado e multiplicada pela frequência angular ao quadrado? |
| 2:50 | a segunda derivada do seno e a do cosseno, uma por vez | O seno resolve: a segunda derivada do seno de frequência vezes tempo é menos a frequência ao quadrado vezes o próprio seno. E o cosseno também resolve, do mesmo jeito. |
| 2:56 | a solução geral: a primeira constante vezes cosseno mais a segunda constante vezes seno | Como a equação é linear, qualquer combinação dos dois também é solução. Então a solução geral é a primeira constante vezes o cosseno, mais a segunda constante vezes o seno. Essas duas constantes dependem de como a gente começa o movimento. |
| 3:02 | "q positiva: componente horizontal inicial zero, componente vertical inicial igual à velocidade perpendicular"; a primeira constante vira zero | Vamos escolher o caso da carga positiva que a gente já está vendo. No instante inicial, a componente horizontal da velocidade vale zero, e a componente vertical vale a velocidade perpendicular. Com a componente horizontal igual a zero no instante inicial, o cosseno vale um e o seno vale zero. Então a primeira constante da solução tem de ser zero. |
| 3:08 | a equação acoplada em t = 0; "em t = 0"; a derivada da solução; a segunda constante é identificada | A informação sobre a componente vertical ainda não foi usada. Ela entra pela equação acoplada. No instante inicial, a aceleração horizontal é a frequência angular vezes a componente vertical, que vale a velocidade perpendicular. Do outro lado, a derivada da solução, no instante zero, é a frequência angular vezes a segunda constante. Igualando, a segunda constante é a velocidade perpendicular. Vale a pena reparar: uma condição sobre a componente vertical determinou uma constante da componente horizontal. É por causa do acoplamento entre as duas equações. |
| 3:14 | "v_z = (1/ω_c) dv_y/dt"; a derivada da solução entra | E a componente vertical sai da mesma equação acoplada: é a derivada da componente horizontal, dividida pela frequência angular. Derivando o seno, aparece o cosseno vezes a frequência, e a frequência cancela. |
| 3:20 | os dois resultados lado a lado: seno e cosseno | Resultado: a componente horizontal é a velocidade perpendicular vezes o seno da frequência vezes o tempo. E a componente vertical é a velocidade perpendicular vezes o cosseno. |

### B02.6 — Dois espaços, uma ideia: a trajetória real e o espaço das velocidades

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 3:26 | os dois cartões entram: "trajetória real" e "espaço das velocidades"; os gráficos das duas componentes; o ponto em cada gráfico | Agora são duas figuras diferentes, e vale a pena não confundir. No cartão de cima está a trajetória real: o ponto informa a posição da partícula no plano. No cartão de baixo está o espaço das velocidades. Aqui, o ponto não informa posição nenhuma. As coordenadas dele são as duas componentes da velocidade naquele instante. O vetor parte da origem desse espaço, e o comprimento dele é a rapidez da componente perpendicular. À direita, os gráficos das duas componentes no tempo. É tudo o mesmo instante nas quatro figuras. |
| 3:32 | a ponta do vetor dá a primeira volta no espaço das velocidades; a legenda "componentes senoidais, defasadas de noventa graus" | Olha as duas componentes. Uma é um seno, a outra é um cosseno: são componentes senoidais, defasadas em noventa graus. Quando uma está no máximo, a outra passa por zero. E a ponta do vetor percorre um círculo no espaço das velocidades. |
| 3:38 | a soma dos quadrados e a identidade trigonométrica | Somando os quadrados das duas componentes, dá a velocidade perpendicular ao quadrado multiplicada por seno ao quadrado mais cosseno ao quadrado, que vale um. Então a rapidez da componente perpendicular não muda. A direção do vetor velocidade muda continuamente, e a rapidez, não. Mas atenção: isso não quer dizer que não há aceleração. Há aceleração, e é ela que muda a direção. A força magnética muda continuamente a direção do vetor velocidade sem aumentar nem diminuir a rapidez. |
| 3:50 | a carga troca de sinal com um clarão; "q negativa"; a componente horizontal troca de sinal; o vetor passa a girar no outro sentido; "mesmo módulo" | E se a carga for negativa, com as mesmas condições iniciais? A órbita passa a girar no sentido contrário. No espaço das velocidades, o vetor também gira no sentido contrário. A componente horizontal troca de sinal, e a vertical continua sendo o cosseno. E a frequência angular ciclotrônica tem o mesmo módulo. O módulo da carga decide a rapidez do giro. O sinal da carga decide o sentido. |

### B02.7 — Da velocidade à posição: integração e circunferência

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 4:05 | "a velocidade já gira; agora: onde está a partícula?"; v_y = dy/dt | A velocidade a gente já tem. Mas onde está a partícula? A velocidade é a taxa de variação da posição no tempo. Então, pra recuperar a posição, a gente faz o caminho inverso: integra. |
| 4:12 | a integral com os limites: de y inicial até y em cada instante, e de zero até t; "de t' = 0 até t" | Do lado esquerdo, a integral do pequeno deslocamento, desde a posição inicial até a posição em cada instante. Do lado direito, a integral da componente horizontal da velocidade, desde o instante zero até o instante observado. Repara que o tempo dentro da integral é uma variável auxiliar, só pra percorrer o caminho. O limite de cima é que é o instante que nos interessa. |
| 4:16 | a primitiva do seno com "mais C"; depois "C se cancela nos limites" | A primitiva do seno é menos o cosseno, dividido pela frequência angular. Essa divisão aparece porque, ao derivar o cosseno, sai um fator de frequência, e a gente precisa desfazer isso. A constante de integração se cancela quando avalia nos dois limites. |
| 4:20 | a avaliação dos limites; a expressão com "um menos cosseno" | Avaliando no limite de cima e subtraindo o do limite de baixo, o cosseno em zero vale um. Por isso aparece um menos cosseno: é a diferença entre os dois limites. Resultado: a posição horizontal menos a inicial é a velocidade perpendicular dividida pela frequência angular, vezes um menos o cosseno. |
| 4:26 | o mesmo caminho para a componente vertical, com limites; a primitiva do cosseno é o seno | Pra componente vertical, o caminho é o mesmo. A primitiva do cosseno é o seno dividido pela frequência. Em zero, o seno vale zero, e sobra só o limite de cima: a velocidade perpendicular dividida pela frequência, vezes o seno. |
| 4:35 | "esse fator vai ser o raio da órbita"; as duas coordenadas reescritas | Repara que nas duas coordenadas aparece o mesmo fator: a velocidade perpendicular dividida pela frequência angular. Esse fator vai aparecer exatamente como o raio da órbita. Vamos identificá-lo como o raio. |
| 4:38 | as expressões elevadas ao quadrado; a soma; "cosseno² mais seno² = 1" | Agora queremos reconhecer a curva geometricamente, sem depender do instante. As duas coordenadas têm o seno e o cosseno da mesma fase. Então a gente passa o raio pro outro lado na primeira, eleva as duas ao quadrado e soma. Seno ao quadrado mais cosseno ao quadrado vale um, e o tempo desaparece. |
| 4:42 | a equação da circunferência; o centro e o raio são marcados no desenho | O que sobra é: a posição horizontal menos o centro, ao quadrado, mais a posição vertical menos a inicial, ao quadrado, igual ao raio ao quadrado. Isso é a equação de uma circunferência. A trajetória circular não foi suposta: ela saiu da lei de Lorentz junto com a segunda lei de Newton. |
| 4:46 | "R = v⊥/ω_c = m v⊥/(∣q∣ B)"; a caixa e o nome "raio da órbita magnética" | E como a gente já sabe quem é a frequência angular, o raio é a massa vezes a velocidade perpendicular, dividido pelo produto entre o módulo da carga e o campo magnético. Mais massa ou mais velocidade, curva mais aberta. Mais carga ou mais campo, curva mais fechada. |

### B02.8 — A componente ao longo do campo (a animação já antecipa a hélice)

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 4:50 | aparece "a aceleração ao longo do campo igual a zero ⇒ a componente é constante"; o eixo do campo; começa a desenhar uma trajetória | E a componente ao longo do campo? A primeira equação do movimento já respondeu: a aceleração ao longo do campo é zero, então essa componente é constante. Se ela for zero, a gente tem só o círculo que acabamos de ver. |
| 4:55 | "nova condição inicial: componente paralela diferente de zero, já em t = 0"; a hélice é desenhada | Agora, repara na imagem: se essa componente não for zero, o círculo avança ao longo do campo, e o que sai é uma hélice. Esse resultado já aponta para a hélice. Vamos fechar primeiro o período e depois voltar a essa ideia com calma. |
| 5:00 | a legenda "a Lorentz não cria a componente paralela; ela preserva" | Um ponto importante: a força de Lorentz não cria essa componente da velocidade. Ela só a preserva. Ela já estava lá desde o instante inicial. |

### B02.9 — Verificação centrípeta e período

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 5:05 | volta o círculo, com o campo saindo da tela; "a força magnética é perpendicular à velocidade, só muda a direção da velocidade" | Voltando ao círculo. A força magnética é sempre perpendicular à velocidade. Por isso ela só muda a direção da velocidade. |
| 5:20 | "a força magnética fornece a força centrípeta"; as duas expressões igualadas | Dá pra conferir o raio por outro caminho. Primeiro, um esclarecimento: força centrípeta não é uma força nova. É o nome que se dá ao papel da força resultante quando ela aponta para o centro de uma trajetória circular. Aqui, esse papel é desempenhado pela força magnética. O módulo dela, a carga vezes a rapidez vezes o campo, tem de ser igual à massa vezes a rapidez ao quadrado dividida pelo raio. Isolando o raio, sai o mesmo resultado. A gente chegou ao mesmo raio por um segundo caminho. |
| 5:35 | "período: circunferência dividida pela rapidez"; a expressão; a substituição do raio; o cancelamento da velocidade perpendicular | Agora o período, que é o tempo de uma volta completa. Uma volta é o comprimento da circunferência, dois pi vezes o raio, e a rapidez é a velocidade perpendicular. Então o período é dois pi vezes o raio dividido pela velocidade perpendicular. Substituindo o raio que acabamos de achar, a velocidade perpendicular aparece em cima e embaixo, e as duas se cancelam. Sobra dois pi vezes a massa, dividido pelo módulo da carga vezes o campo magnético. |
| 5:45 | "velocidades transversais diferentes mudam o raio, mas não o período" | Olha o que sumiu: a velocidade. Uma partícula mais rápida percorre uma circunferência maior, e o raio cresce exatamente na mesma proporção que a rapidez. Por isso o tempo total de uma volta fica o mesmo. Isso vale sob as hipóteses desse problema: regime não relativístico, campo uniforme, mesma massa, mesmo módulo de carga, mesmo campo. |

### B02.10 — Duas partículas

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 5:50 | duas partículas partem juntas; os raios são diferentes; o relógio de fase; o clarão na passagem; "T₁ = T₂" | Vamos ver isso acontecer. Duas partículas, com a mesma massa, o mesmo módulo de carga, no mesmo campo, mas com velocidades perpendiculares diferentes. Os raios saem diferentes. Mesmo assim, as duas completam cada volta juntas, e passam pelo ponto de partida no mesmo instante, a cada período. Os períodos são iguais. |

*Comentário científico:* a independência do período em relação à velocidade (não relativística) é o princípio do cíclotron de Lawrence: partículas mais rápidas descrevem círculos maiores no mesmo tempo, então um campo elétrico alternado de frequência fixa acelera em fase. Em velocidades relativísticas, o período passa a depender da energia da partícula, o que é a razão do síncrotron. O raio de giro é conhecido como raio de Larmor ou girorraio. As três hipóteses valem para esta análise do movimento; mais tarde o vídeo introduz o campo elétrico (B07) e situações com acumulação de carga (B06).

---

## B03 — A hélice

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 6:02 | "nova condição inicial: x(t) = x₀ + v_∥ t"; a velocidade como soma de duas componentes | Agora a gente volta à ideia que ficou em aberto. Uma nova condição inicial: a velocidade tem uma componente paralela ao campo diferente de zero, já definida desde o instante inicial. |
| 6:14 | a hélice se forma; "componente paralela = constante (já definida)"; "círculo + translação = hélice" | Ao longo do campo, a partícula anda com velocidade constante. No plano perpendicular ao campo, ela continua girando no círculo que a gente já conhece. Um círculo somado a uma translação ao longo do campo é uma hélice. Não é uma regra nova: é a mesma solução da lei de Lorentz, só com a componente paralela diferente de zero. |
| 6:20 | "círculo + translação = hélice" na caixa | Repara que a componente paralela e a perpendicular não se misturam: cada uma segue sua própria equação. |
| 6:26 | o passo p marcado ao lado da hélice; "p = 2π m ∣v_∥∣ / (∣q∣ B)" | A hélice tem duas medidas. O raio, que vem da componente perpendicular, e o passo. O passo é a distância medida ao longo do eixo da hélice entre dois pontos correspondentes, separados por uma volta completa. Não é o comprimento percorrido sobre a curva. Como é uma distância, a gente usa o módulo da componente paralela. Então o passo é o módulo da componente paralela vezes o período: dois pi vezes a massa vezes o módulo da componente paralela, dividido pelo módulo da carga vezes o campo magnético. |
| 6:32 | "velocidade perpendicular menor: raio menor, passo igual" | Agora comparando condições iniciais diferentes. Repara: o campo não está mudando a rapidez de uma mesma partícula durante o movimento. A gente está comparando partículas que começaram diferentes. Com a velocidade perpendicular menor, o raio fica menor, e o passo fica o mesmo, porque o período não mudou. |
| 6:44 | "componente paralela maior: passo maior, raio igual" | Com a componente paralela maior, o passo cresce, porque a partícula avança mais em cada volta. E o raio fica o mesmo, porque ele só depende da componente perpendicular. |
| 6:46 | os dois limites | Dois casos limite ajudam a fixar. Componente paralela igual a zero: um círculo. Componente perpendicular igual a zero: nenhuma força, e a partícula segue em linha reta, com velocidade constante, ao longo do campo. |
| 6:50 | "q → −q: gira ao contrário, avança igual" | E o sinal da carga? Com o mesmo módulo de carga, a mesma massa e as mesmas condições iniciais, uma carga negativa gira no sentido contrário. Mas avança ao longo do campo exatamente da mesma forma, porque a componente paralela não é afetada pela força. O raio, o período e o passo ficam iguais. |

*Comentário científico:* o movimento helicoidal em torno das linhas de campo é a base do confinamento magnético, da aurora e da deriva de partículas nos cinturões de radiação. O passo mede só deslocamento ao longo do eixo, não o comprimento da hélice.

---

## B04 — Por que a partícula não fica mais rápida? Trabalho, potência e energia

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 7:02 | "retomando o caso: componente paralela igual a zero"; a hélice some e o círculo reaparece | Voltando ao círculo, com a componente paralela igual a zero. Tem uma pergunta que a gente precisa responder. |
| 7:08 | "A partícula está acelerando. Então por que ela não fica mais rápida?"; o painel do vetor velocidade; o medidor de rapidez; a = F_B/m ≠ 0 | A partícula está acelerando, porque a direção da velocidade muda o tempo todo. Então por que ela não fica mais rápida? A resposta é que existe aceleração sem mudança de rapidez. O vetor velocidade gira, e o módulo dele, que é a rapidez, fica o mesmo. O medidor mostra isso. |
| 7:20 | a velocidade e a força a noventa graus; "v velocidade", "F_B força magnética" | Pra entender isso a fundo, a gente vai usar trabalho. Repara na imagem: a velocidade é tangente à trajetória, e a força magnética aponta para o centro. Formam um ângulo reto. |
| 7:26 | "Trabalho em um deslocamento": dW = F · dr; o pequeno deslocamento nasce preso à partícula | O trabalho de uma força num pequeno deslocamento é o produto escalar entre a força e o deslocamento. O produto escalar seleciona a componente da força na direção do deslocamento. É essa componente que controla a transferência de energia mecânica naquele deslocamento. A componente perpendicular ao deslocamento não transfere nada. |
| 7:36 | "Potência instantânea": P = dW/dt | Tomando a taxa instantânea de realização de trabalho, a gente tem a potência. Do trabalho elementar, passamos para a taxa de trabalho no tempo, e isso é a potência. |
| 7:40 | P = F · dr/dt; "dr/dt = v"; P = F · v | Substituindo o trabalho pelo produto escalar, aparece a derivada do deslocamento em relação ao tempo. E essa derivada é exatamente a velocidade. Então a potência de qualquer força é o produto escalar entre a força e a velocidade. |
| 7:48 | "Potência da força magnética": P_B = F_B · v; depois q(v × B) · v | Agora aplicamos à força magnética. A potência é a força magnética escalar a velocidade. Substituindo a força magnética pela carga vezes o produto vetorial da velocidade pelo campo, ficamos com a carga vezes esse produto vetorial, em produto escalar com a velocidade. |
| 7:54 | "v × B ⊥ v"; P_B = 0 | Só que o produto vetorial entre a velocidade e o campo é perpendicular à velocidade. Então esse produto escalar é zero. A potência magnética é zero em todo instante. |
| 8:00 | "Trabalho da força magnética": W_B = ∫ P_B dt = 0 | E o trabalho total é a integral da potência no tempo. Integrando zero, o trabalho também é zero. Importante: trabalho magnético nulo não significa força magnética nula. A força pode ser grande e mudar fortemente a direção da velocidade, ao mesmo tempo em que o trabalho continua zero. E essa conclusão vem só da perpendicularidade entre a força e a velocidade. Ela não depende de a trajetória ser circular, nem exige, por si só, um campo uniforme. |
| 8:04 | "Energia cinética": E_c = ½ m ∣v∣²; "só a força magnética atua" | A energia cinética é metade da massa vezes a rapidez ao quadrado. |
| 8:08 | "Teorema trabalho–energia": ΔE_c = W_B = 0; "E_c constante ⇒ ∣v∣ constante" | Pelo teorema do trabalho e energia, a variação da energia cinética é igual ao trabalho total. Se só a força magnética atua, o trabalho é zero, a energia cinética fica constante e a rapidez também. |
| 8:12 | a nota "E_c pode mudar se outra força realizar trabalho" | Mas cuidado: se existir outra força realizando trabalho, a energia cinética pode mudar, mesmo com o trabalho magnético igual a zero. Aqui, a gente supôs que só a força magnética atua. |
| 8:16 | os quatro cards se acendem na ordem: fonte elétrica, corrente, interação magnética, movimento mecânico | E um motor elétrico? Então de onde vem a energia? A fonte fornece energia. O campo elétrico pode realizar trabalho sobre as cargas, e as forças eletromagnéticas sobre os portadores são transmitidas ao material. Assim, o sistema converte energia elétrica em movimento mecânico. A parcela magnética sobre cada carga não realiza trabalho, mas o sistema como um todo pode transferir energia. |

*Comentário científico:* o teorema do trabalho e energia dá o argumento rigoroso para rapidez constante. A afirmação "força magnética não realiza trabalho" é sobre a força sobre cada carga; num motor, a energia sai da fonte, e o campo magnético redireciona as forças entre as partes do circuito. A conclusão vale para qualquer campo magnético, uniforme ou não, desde que só a força magnética atue.

---

## B05 — Da carga individual à corrente: linha, superfície, volume

### B05.1 — Muitas cargas num fio

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 8:24 | um fio cinza com portadores azuis em movimento; a seta da corrente verde; os símbolos do campo; "uma carga em movimento: F = q v × B" | Agora vamos levar tudo isso para um fio. Cada carga em movimento sente a força magnética. Um fio tem muitíssimas cargas em movimento. Pra simplificar, a gente representa os portadores como cargas positivas efetivas: é um modelo, e a gente vai ver por que ele funciona. |
| 8:30 | "muitas cargas: portadores positivos efetivos; representação conveniente, não um metal real" | Num metal de verdade, os portadores são elétrons, negativos, que se deslocam no sentido oposto ao da corrente convencional. Mas a contribuição para a corrente depende do produto da carga pela velocidade. Se a gente inverte o sinal da carga e a direção da velocidade ao mesmo tempo, a contribuição para a corrente convencional fica no mesmo sentido. Por isso o modelo com portadores positivos é legítimo. |

### B05.2 — Um pedaço do fio: carga, comprimento e corrente

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 8:35 | um trecho do fio é marcado, com o comprimento dℓ; depois a carga contida | Vamos olhar um pequeno trecho do fio. O comprimento dele é um pequeno elemento de comprimento. A carga dos portadores contida nesse trecho é uma pequena quantidade de carga. |
| 8:40 | "λ: carga por comprimento"; λ = dq/dℓ; dq = λ dℓ | Chamando de lambda a densidade linear de carga, ou seja, a carga dos portadores por unidade de comprimento: a pequena quantidade de carga é a densidade linear de carga multiplicada pelo pequeno elemento de comprimento. Um detalhe importante: essa densidade é a dos portadores que a gente está considerando. Não é a carga líquida macroscópica do fio. Um fio pode ter carga líquida aproximadamente zero e ainda ter corrente diferente de zero. |
| 8:46 | a seção transversal e "um pequeno intervalo de tempo: a carga cruza a seção" | E o que é a corrente? É a quantidade de carga que atravessa uma seção do fio em cada intervalo de tempo. |
| 8:50 | I = dq/dt; "em dt, cada portador percorre v dt"; dq = λ v dt | Num pequeno intervalo de tempo, cada portador percorre a velocidade vezes esse intervalo. Aqui a velocidade que importa é a velocidade média de deriva dos portadores, e não a agitação térmica desordenada, que em média não transporta carga numa direção. Então a quantidade de carga que cruza a seção é a densidade linear de carga, vezes a velocidade de deriva, vezes o intervalo de tempo. |
| 8:56 | o intervalo de tempo é riscado em cima e embaixo; "I = λ v" | O intervalo de tempo aparece em cima e embaixo, e se cancela. A corrente é a densidade linear de carga multiplicada pela velocidade de deriva. |

### B05.3 — A força chega ao fio

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 9:05 | "dF = dq v × B"; a seta dF; o elemento de comprimento orientado | Agora a força sobre esse pequeno trecho. Cada portador sente a força magnética. A força total no trecho é a pequena quantidade de carga vezes a velocidade vezes o campo magnético, em produto vetorial. |
| 9:10 | dq = λ dℓ; "v e dℓ: mesmo sentido"; λ v = I | Trocando a pequena quantidade de carga pela densidade linear de carga vezes o elemento de comprimento, e reconhecendo que a velocidade tem o mesmo sentido do elemento, a densidade linear de carga vezes a velocidade é a corrente. |
| 9:14 | dF = I dℓ × B na caixa | Então a força no trecho é a corrente vezes o elemento de comprimento, orientado no sentido da corrente, em produto vetorial com o campo magnético. |
| 9:20 | F = ∫ I dℓ × B; "dℓ segue a corrente convencional"; o título "Força magnética sobre um fio com corrente" | Somando todos os trechos do fio, a gente tem uma integral: a força sobre o fio inteiro. E repara no sentido: o elemento de comprimento segue a corrente convencional. Uma observação importante sobre como a força chega ao fio: a força magnética age, microscopicamente, sobre os portadores. As interações desses portadores com a rede do material transferem essa força para o corpo do condutor. É assim que a força sobre cargas móveis aparece como força sobre o fio. Os elétrons de um metal não descrevem livremente as órbitas do bloco anterior: eles colidem e interagem com o material. |

### B05.4 — Da linha para a superfície

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 9:30 | "a linha ganha largura"; uma lâmina cinza com setas verdes | E se o condutor não é um fio fino, mas uma lâmina? A corrente passa a se espalhar na largura. |
| 9:32 | a faixa de largura dw; "K: corrente por largura"; dI = ∣K∣ dw | A densidade superficial de corrente, que na tela aparece como K em negrito, mede a corrente por unidade de largura transversal ao escoamento. Uma faixa de largura pequena carrega uma pequena corrente, igual ao módulo da densidade superficial de corrente vezes a largura da faixa. |
| 9:35 | o elemento de área dA_sup e a carga dq; "σ: carga por área"; dq = σ dA_sup | Do lado da carga: sigma, a densidade superficial de carga. A pequena quantidade de carga num elemento de área da superfície é a densidade superficial de carga multiplicada pela área do elemento. |
| 9:38 | "espécie com velocidade v"; K = σ v | Para uma espécie de portador com velocidade, a densidade superficial de corrente é a densidade superficial de carga multiplicada pela velocidade. |

### B05.5 — Da superfície para o volume

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 9:42 | "a superfície ganha espessura"; o prisma | E se a lâmina ganha espessura? Agora o condutor é um volume. |
| 9:44 | a área perpendicular ao escoamento marcada; "Densidade de corrente: J = corrente por área; dI = ∣J∣ dA⊥" | A densidade de corrente, J, é a corrente por unidade de área transversal ao escoamento, num ponto do volume. Uma fatia dessa corrente é o módulo da densidade de corrente vezes a área perpendicular ao escoamento. |
| 9:50 | "Corrente total": I = ∫ J · da | Somando todas essas fatias sobre uma superfície, a corrente total é a integral do produto escalar entre a densidade de corrente e o elemento vetorial de área, orientado pela normal. E vale a pena notar: se a superfície é inclinada, o produto escalar com o vetor área seleciona só a componente do escoamento que atravessa a superfície. |
| 9:56 | o pequeno volume dτ com a carga dq; "ρ: carga por volume"; dq = ρ dτ; J = ρ v | Do lado da carga, rô, a densidade volumétrica de carga. A pequena quantidade de carga num pequeno elemento de volume é a densidade volumétrica de carga multiplicada pelo pequeno elemento de volume. Para uma espécie de portador, a densidade de corrente é a densidade volumétrica de carga multiplicada pela velocidade. |
| 10:02 | "duas espécies de portador"; ρ₁ > 0, ρ₂ < 0; J = ρ₁v₁ + ρ₂v₂; "ρ_i com sinal" | Com mais de uma espécie de portador, a gente soma as contribuições, cada uma com o seu sinal e a sua velocidade. Uma carga negativa indo para a esquerda contribui como corrente para a direita. E repara: mesmo que a carga líquida seja zero, a densidade de corrente pode ser diferente de zero. |
| 10:08 | F = ∫ I dℓ × B → ∫ K × B dA → ∫ J × B dτ; "a mesma interação: linha, superfície, volume" | Resumindo: não são três leis. É a mesma interação, escrita pra um fio fino, pra uma lâmina e pra um volume. Na linha entra a corrente, na superfície a densidade superficial de corrente, no volume a densidade de corrente. A física é a mesma. É a mesma física escrita de outra forma. |

*Comentário científico:* a densidade linear de carga usada para deduzir I = λv é a dos portadores móveis, não a densidade líquida macroscópica do fio, que pode ser nula. A velocidade relevante é a velocidade média de deriva. Para elétrons de condução, carga negativa e velocidade de deriva oposta à corrente convencional dão a mesma contribuição que carga positiva e velocidade de sentido da corrente. A força sobre o fio é a resultante das forças sobre os portadores, transmitidas ao material por colisões e interações com a rede. A distinção entre densidade superficial de corrente (corrente por largura) e densidade volumétrica de corrente (corrente por área) é geométrica: a primeira tem unidades de ampère por metro, a segunda, de ampère por metro quadrado.

---

## B06 — Conservação da carga: a equação da continuidade

### B06.1 — Fluxo, corrente e volume de controle

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 10:20 | o prisma cinza se reduz a uma referência; entra o campo de setas verdes da densidade de corrente | Até aqui, a gente estava interessado em corrente estacionária. Agora vamos permitir, temporariamente, que a entrada e a saída de carga sejam diferentes, pra entender a conservação da carga na forma mais geral. Depois voltamos ao estacionário. Primeiro, olha a densidade de corrente como um campo de setas verdes. |
| 10:26 | uma superfície S aparece, com o elemento vetorial de área; "I = ∫ J · da; corrente = fluxo de J" | Fluxo mede quanto de uma grandeza atravessa uma superfície, levando em conta a orientação dela. Aqui, a grandeza transportada é carga. Então a corrente através de uma superfície é o fluxo da densidade de corrente através dela: a integral do produto escalar entre a densidade de corrente e o elemento vetorial de área, que aponta na normal. |
| 10:32 | a faixa "v dt" que atravessa a superfície em um pequeno intervalo | Pra visualizar: num pequeno intervalo de tempo, atravessa a superfície a carga contida na fatia de espessura igual à velocidade vezes o intervalo. |
| 10:38 | a superfície vira a fronteira de um volume; "Volume de controle"; a fronteira; a carga dos portadores; "J entra", "J sai" | Agora fecha essa superfície. Ela passa a ser a fronteira de uma região do espaço, um volume de controle. É uma região matemática, imaginária: não é um pedaço de material. Dentro dela há carga, os portadores positivos efetivos. Pela fronteira, a densidade de corrente entra de um lado e sai do outro. Se isso lembra os vídeos anteriores, é por isso: estamos usando de novo uma superfície fechada, normais e fluxo. Mas agora o fluxo é da densidade de corrente, e aparece num balanço de conservação. |

### B06.2 — O balanço: quatro estados

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 10:44 | "variação = entra − sai"; aparecem a corrente de entrada, a corrente de saída, a taxa e a carga dentro do volume; "câmera lenta" | O balanço é uma contabilidade. A variação da carga dentro do volume é o que entra menos o que sai. Aqui estão os medidores: a corrente que entra, a corrente que sai, a taxa de variação da carga dentro do volume e a carga dentro do volume. Um aviso: a animação está em câmera lenta, mas a lei é a mesma. |
| 10:46 | estado 1: entrada igual à saída; a carga dentro fica constante | Primeiro estado: a corrente que entra é igual à que sai. A taxa de variação é zero, e a carga dentro do volume fica constante. |
| 10:50 | estado 2: a corrente de saída cresce; a legenda "saída maior que entrada: a carga dentro diminui"; os portadores deixam o volume mais depressa | Segundo estado: a corrente de saída fica maior que a de entrada. Sai mais do que entra, então a carga dentro do volume diminui. A taxa de variação é negativa. |
| 10:56 | a corrente de saída volta ao valor da entrada; o medidor da taxa volta a zero | Quando as duas voltam a ser iguais, a taxa volta a ser zero, e a carga dentro do volume para de variar. |
| 10:58 | estado 3: a corrente de entrada cresce; "entrada maior que saída: a carga dentro aumenta" | Terceiro estado: agora entra mais do que sai, e a carga dentro do volume aumenta. A taxa é positiva. |
| 11:04 | a corrente de entrada volta; novo equilíbrio | E de novo, quando as duas voltam a ser iguais, a carga fica constante. O que entra, ou fica armazenado, ou sai: a carga não aparece nem some. |

### B06.3 — Normais externas e o sinal

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 11:05 | as normais externas aparecem nas duas faces; "J · n < 0" na entrada e "J · n > 0" na saída | Pra escrever isso com cuidado, a gente usa sempre a normal que aponta para fora do volume. Na face de entrada, a densidade de corrente aponta contra a normal, então o produto escalar é negativo. Na face de saída, aponta junto com a normal, e o produto escalar é positivo. |
| 11:12 | "fluxo líquido para fora"; a integral sobre a fronteira é igual à saída menos a entrada | A integral desse produto escalar sobre a fronteira inteira é o fluxo líquido para fora: o que sai menos o que entra. |
| 11:16 | "dQ/dt = −∮ J · da" | Então a variação da carga dentro do volume é menos esse fluxo líquido para fora. O sinal de menos expressa isto: quando o fluxo líquido para fora é positivo, a carga armazenada dentro diminui. A conservação da carga é a igualdade completa entre esses dois balanços: o que muda dentro e o que atravessa a fronteira. |

### B06.4 — Forma integral, divergência e forma local

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 11:20 | "rô: carga por volume"; Q_int = ∫ ρ dτ | Agora a carga dentro do volume: é a soma da densidade volumétrica de carga em todo o volume. Uma integral sobre o volume. |
| 11:26 | "V fixo: só ρ varia com t" | O volume é fixo. Então, o que pode mudar no tempo é só a densidade volumétrica de carga. |
| 11:30 | "forma integral": d/dt ∫ ρ dτ = −∮ J · da; as duas metades acendem no desenho | Isso dá a forma integral da conservação da carga. De um lado, a taxa de variação da carga dentro do volume. Do outro, menos o fluxo da densidade de corrente pela fronteira. Uma metade fala do que está dentro, a outra fala do que atravessa a fronteira. |
| 11:35 | "teorema da divergência": o fluxo na fronteira vira uma integral no volume; aparece o divergente da densidade de corrente | Agora o teorema da divergência. É uma identidade matemática: o fluxo de um campo através de uma fronteira fechada é igual à integral, no volume dentro dela, do divergente desse campo. E o que é o divergente? O divergente da densidade de corrente mede a saída líquida de corrente por unidade de volume, no limite de uma região muito pequena. A palavra líquida é importante: pode existir corrente atravessando uma região com divergente zero, se entra tanto quanto sai. |
| 11:40 | as pequenas células com setas de entrada e de saída | Veja nas células pequenas: nelas, entra e sai a mesma quantidade, então o divergente é zero. |
| 11:42 | a derivada passa para dentro da integral como derivada parcial; a taxa local de variação da densidade de carga | Como o volume é fixo, a derivada no tempo pode entrar na integral, e vira uma derivada parcial: a taxa local de variação da densidade de carga. Então a integral dessa taxa local mais o divergente da densidade de corrente é igual a zero. |
| 11:50 | "V é qualquer"; a integral igual a zero; a expressão local | Aqui tem um passo sutil. Uma integral igual a zero, em um volume específico, poderia acontecer só porque contribuições positivas e negativas se cancelam. Mas essa equação vale para qualquer volume, escolhido em qualquer lugar. Sob as condições usuais de regularidade, isso exige que a própria expressão dentro da integral seja zero em cada ponto. É assim que a gente passa da equação integral para uma equação local. |
| 11:56 | "Equação da continuidade": ∇·J = −∂ρ/∂t | O resultado: o divergente da densidade de corrente é igual a menos a taxa local de variação da densidade de carga. Essa é a equação da continuidade. Ela é a conservação da carga escrita ponto a ponto. Repara na diferença entre as peças: o teorema da divergência é uma identidade matemática. A conservação da carga é uma afirmação física. E a lei de Gauss é outra afirmação física, de outro tipo. A gente usou uma e outra aqui, mas não são a mesma coisa. |

### B06.5 — Retorno ao regime estacionário

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 12:00 | "magnetostática": a taxa local de variação da densidade de carga igual a zero; depois o divergente igual a zero | Agora voltamos ao regime estacionário, que é o da magnetostática. Em regime estacionário, a densidade de carga em cada ponto não muda no tempo. Então a taxa local de variação é zero, e o divergente da densidade de corrente também é zero. |
| 12:05 | "J ≠ 0, a corrente existe"; "∇·J = 0, nenhuma carga se acumula"; "corrente estacionária: não é nula" | Mas atenção ao que isso quer dizer. Corrente estacionária não é corrente nula. A densidade de corrente existe, e continua passando carga. O que não existe é aumento ou diminuição da carga armazenada em lugar nenhum. Também não quer dizer ausência de portadores, nem que a carga armazenada seja necessariamente zero. Entra e sai à mesma taxa, ponto a ponto. |

*Comentário científico:* a equação da continuidade é a forma local da conservação da carga elétrica, e o teorema da divergência é só matemática (Gauss–Ostrogradski). A passagem de "integral nula em qualquer volume" para "integrando nulo" usa, além da arbitrariedade do volume, a regularidade (continuidade) do integrando. O sinal de menos vem da convenção da normal externa e não é, por si só, a conservação. Em regime estacionário, o divergente da densidade de corrente é zero; este resultado é local, e o vídeo **não** afirma nada geral sobre a topologia das linhas de corrente. Também não afirma que "carga líquida zero" é a mesma coisa que "regime estacionário".

---

## B07 — Thomson: o seletor de velocidades

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 12:10 | o volume de controle e a densidade de corrente se dissolvem; entram o feixe e a região do campo magnético | Voltamos a uma carga individual, agora com mais de um campo. O objetivo é descobrir como duas forças opostas podem se cancelar e fazer uma carga atravessar uma região sem desvio. |
| 12:14 | "Agora escolhemos um novo sistema de eixos adequado ao aparelho": o triedro; "v = v x̂" | E aqui um aviso: a gente escolhe agora um novo sistema de eixos, adequado ao aparelho. No bloco anterior, o campo magnético estava ao longo de outro eixo. Aqui, a velocidade da carga é ao longo do eixo horizontal. |
| 12:18 | entram as placas; "E = E ŷ"; depois o campo magnético "B = B ẑ" | Entre duas placas, existe um campo elétrico apontando na vertical. E nessa mesma região, um campo magnético, saindo da tela. |
| 12:22 | F_E aparece com o seu nome; "F_E = qE" | O campo elétrico empurra a carga positiva para cima. A força elétrica é a carga vezes o campo elétrico. Repara numa coisa: esse módulo não depende da rapidez da carga. |
| 12:26 | F_B aparece com o seu nome; a regra da mão direita; "x̂ × ẑ = −ŷ" | O campo magnético empurra a carga pra baixo. A força magnética é a carga vezes a velocidade vezes o campo magnético. O produto vetorial entre a direção do movimento e a direção do campo aponta pra baixo, e pode conferir com a regra da mão direita. Esse módulo cresce com a rapidez. |
| 12:30 | a resultante F_y; "F_y = q(E − vB)" | Então temos uma força elétrica constante pra cima e uma força magnética que cresce com a rapidez, pra baixo. Logo existe uma rapidez específica em que os dois módulos se igualam, e as forças, opostas, se cancelam. Esse é o coração físico do seletor. A força vertical total é a carga vezes o campo elétrico menos a rapidez vezes o campo magnético. |
| 12:35 | "F_y/q = E − vB" na caixa | Dividindo pela carga, sobra uma expressão que depende só do campo elétrico, do campo magnético e da rapidez. |

### B07.2 — O gráfico

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 12:40 | o aparato vai pra esquerda; entra o gráfico à direita, com o eixo da rapidez | Vamos olhar isso num gráfico. O eixo horizontal é a rapidez. O eixo vertical é a força vertical dividida pela carga. Para a carga positiva do nosso caso-base, o sinal dessa quantidade coincide com o sinal da força vertical. Para uma carga negativa, não coincide, e a gente já volta a isso. |
| 12:44 | o ponto percorre a reta; o feixe acompanha o mesmo valor de rapidez | O ponto no gráfico e o feixe no aparelho dependem da mesma rapidez. Quando a rapidez aumenta, o ponto desce pela reta. |
| 12:50 | "rapidez atual menor que a selecionada: força líquida para cima"; o feixe desvia para cima | Com a rapidez menor que um certo valor, a força elétrica ganha, e a força líquida aponta pra cima, no caso da carga positiva. O feixe desvia pra cima. |
| 12:56 | "rapidez atual maior que a selecionada"; o feixe desvia para baixo; "trajetórias esquemáticas" | Com a rapidez maior, a força magnética ganha, e a força líquida aponta pra baixo. Repara que as curvas desenhadas fora da condição selecionada são esquemáticas: servem pra mostrar o sentido do desvio. Não são a solução quantitativa completa do movimento em campos cruzados. |
| 13:02 | o ponto cruza o zero; "rapidez selecionada = E/B"; "Condição de seleção de velocidades"; o feixe sai reto | No ponto em que a reta cruza o zero, a força líquida é nula. A rapidez correspondente é o campo elétrico dividido pelo campo magnético. É a rapidez selecionada. E atenção: resultante zero não quer dizer campo elétrico zero, nem campo magnético zero, nem forças zero. As duas forças existem e se cancelam. |
| 13:10 | "o seletor não iguala velocidades: seleciona" | E o que o seletor faz? Ele não muda todas as partículas para a mesma rapidez. Na geometria idealizada, ele deixa passar sem desvio as partículas que já entraram com a rapidez apropriada. As outras desviam. |
| 13:20 | a carga troca de sinal; "F_y/q = E − vB não depende do sinal; F_y, sim"; a rapidez selecionada vale para qualquer sinal | E se a carga for negativa? As duas forças invertem o sentido. A força vertical total troca de sinal, e o desvio, nas rapidezes diferentes da selecionada, troca de lado. Mas o ponto de cancelamento é o mesmo, porque o módulo da carga sai da conta. Então a rapidez selecionada vale para qualquer carga, positiva ou negativa. |

*Comentário científico:* é o princípio do filtro de velocidades (filtro de Wien) usado em espectrômetros de massa e relacionado ao trabalho de J. J. Thomson (1897) sobre a razão carga-massa do elétron. A força elétrica independe da rapidez e a magnética cresce com ela, daí a existência de uma rapidez de cancelamento. A resultante nula exige que as duas forças estejam presentes e se cancelem. As trajetórias fora da condição selecionada são esquemáticas: mostram o sentido do desvio, não a solução completa em campos cruzados.

---

## B08 — Medindo a razão carga-massa

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 13:30 | o campo elétrico é desligado; o rótulo "só B, mesmo v"; uma região magnética; o feixe se curva | Agora consideramos partículas que já tiveram a rapidez determinada pelo seletor. Elas entram, depois, numa região onde existe só campo magnético. E atenção: desligar o campo elétrico na segunda região não significa que o seletor continua funcionando sem ele. O seletor já fez o trabalho dele. A partir daqui, o campo elétrico dessa região é zero, e a partícula só sente a força magnética. |
| 13:35 | a trajetória desenha um arco; o raio é marcado | Sob só o campo magnético, a partícula faz um arco de circunferência, que a gente já conhece. Pra um dado campo, o raio depende da partícula. Então a gente pode medir esse raio no desenho. |
| 13:40 | "∣q∣ v B = m v²/R"; o campo magnético, em magenta | Escrevendo: o módulo da carga, vezes a rapidez, vezes o campo magnético, igual à massa vezes a rapidez ao quadrado, dividida pelo raio da órbita. |
| 13:44 | a rapidez é cancelada | Cancelando uma rapidez dos dois lados, ficamos com o módulo da carga vezes o campo magnético igual à massa vezes a rapidez, dividida pelo raio. |
| 13:48 | "∣q∣/m = v/(B R)"; a massa desce, o campo magnético atravessa a igualdade | Agora isolando a razão entre o módulo da carga e a massa: a massa passa pra baixo, de um lado, e o campo magnético passa pra baixo, do outro. Resultado: a razão entre o módulo da carga e a massa é a rapidez dividida pelo produto entre o campo magnético e o raio. |
| 13:52 | "usando a velocidade selecionada (mesmo módulo de B nas duas etapas)"; v = E/B é levado até a fórmula | E a rapidez? Ela vem do seletor: campo elétrico dividido por campo magnético. Substituindo, e usando o mesmo valor do campo magnético nas duas etapas, a gente chega a: o campo elétrico dividido pelo produto entre o quadrado do campo magnético e o raio. |
| 13:58 | a caixa "Razão carga–massa em módulo" | Esse é o resultado: a razão entre o módulo da carga e a massa é igual ao campo elétrico dividido pelo produto entre o quadrado do campo magnético e o raio. |
| 14:00 | "↑ vem do seletor"; "com E e B conhecidos, medir R fornece ∣q∣/m"; o sentido da curva dá o sinal | Vale organizar o que cada parte do experimento fornece. Os campos conhecidos determinam a rapidez selecionada. O raio da curva permite determinar a razão entre o módulo da carga e a massa, com os dois campos conhecidos. E o sentido da curvatura permite inferir o sinal da carga, conhecendo a orientação do campo e da velocidade. Mas repara: o experimento não fornece a carga e a massa separadamente. Fornece a razão entre elas. |
| 14:04 | o módulo da velocidade permanece o mesmo, trabalho magnético zero | E o que a gente viu antes continua valendo: a rapidez permanece constante e o trabalho magnético é zero. |
| 14:06 | as unidades: m/s e C/kg | Conferindo as unidades: campo elétrico dividido por campo magnético dá metros por segundo, uma rapidez. E o campo elétrico dividido pelo produto entre o quadrado do campo magnético e o raio dá coulombs por quilograma, que é exatamente uma carga dividida por uma massa. |

*Comentário científico:* o desenho é uma **representação didática** do princípio de medição associado ao trabalho de Thomson; a semicircunferência mostrada não reproduz literalmente o aparato histórico de 1897, que usava deflexão de um feixe de raios catódicos em campos elétrico e magnético em um tubo. O experimento mede a razão entre o módulo da carga e a massa, não os dois separadamente. O valor numérico moderno da razão carga-massa do elétron não é necessário aqui e foi removido do texto falado.

---

## B09 — Síntese e a pergunta que fica

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 14:10 | "força magnética: a lei que sustenta tudo": F_B = q v × B | Vamos recapitular. Tudo o que a gente fez partiu de uma lei: a força magnética, a carga vezes o produto vetorial da velocidade pelo campo magnético. |
| 14:15 | o círculo; o vetor velocidade; "componente paralela = 0: círculo, frequência angular = ∣q∣B/m" | Com a componente paralela da velocidade igual a zero, a trajetória é um círculo, girando na frequência angular ciclotrônica. |
| 14:18 | a hélice; "componente paralela diferente de zero: hélice" | Com a componente paralela diferente de zero, o círculo avança ao longo do campo, e a trajetória é uma hélice. |
| 14:21 | o fio cinza com cargas; a seta da corrente; "muitas cargas: corrente" | Quando existe transporte organizado de carga, a gente descreve esse movimento coletivo como corrente elétrica. |
| 14:24 | o campo de setas verdes; "densidade de corrente em regime estacionário"; o divergente igual a zero | E a corrente espalhada num material é a densidade de corrente, que em regime estacionário tem divergente zero: a carga não se acumula. |
| 14:27 | o aparato de Thomson em esquema; v = E/B; ∣q∣/m = E/(B²R) | E, voltando a uma carga individual, o seletor de velocidades e a medida da razão carga-massa. |
| 14:33 | os dois fios do começo; a corrente verde se move; os anéis de campo magnético | E agora a gente volta aos dois fios do começo. A corrente em cada fio é transporte organizado de carga. O campo magnético age sobre os portadores móveis, e essa força é transmitida ao material do condutor. |
| 14:39 | as setas de atração; a corrente de ambos no mesmo sentido | No caso dos dois fios paralelos com correntes no mesmo sentido, a força resultante mostrada é de atração. Já sabemos como um campo magnético conhecido age sobre uma corrente. Ainda falta descobrir de onde vem esse campo: como uma distribuição de corrente produz o campo magnético que age sobre o outro fio. |
| 14:44 | "Como uma corrente cria B?" | Então a pergunta que fica é: como uma corrente cria um campo magnético? |
| 14:48 | o CTA: PARALLAX LAB; "Inscreva-se para acompanhar os próximos vídeos"; "Próximo: como uma corrente gera campo magnético" | Essa é a pergunta que leva à lei de Biot–Savart, que é o tema do próximo vídeo. Se você quer acompanhar, se inscreve no canal. A gente se vê por lá! |

*Comentário científico:* o fecho retorna ao gancho: a interação entre fios é a ação do campo magnético criado por uma corrente sobre a outra, mas ainda não calculamos esse campo. A força chega ao fio porque a força magnética age sobre os portadores móveis e é transmitida ao material. O vídeo termina na pergunta, sem responder, e não adianta Biot–Savart.

---

## Âncoras visuais críticas para o remapeamento (resumo por bloco)

**B02:** menor da primeira componente destacado · menor da segunda · menor da terceira · os três resultados se juntam · Newton entra · primeira equação (componente ao longo do campo constante) · segunda e terceira equações acopladas · a segunda equação é derivada · a terceira equação é substituída · o fator aparece ao quadrado (equação harmônica) · frequência angular aparece · derivar duas vezes (seno e cosseno) · solução geral aparece · a primeira constante é zerada · a segunda constante é encontrada pela equação acoplada · a componente vertical sai da equação acoplada · os dois cartões entram (trajetória real e espaço das velocidades) · a ponta do vetor dá a primeira volta · a soma dos quadrados · o sinal da carga troca · a integral recebe os limites · a primitiva com mais C · o limite inferior é aplicado · o fator é identificado como o raio · as equações são elevadas ao quadrado · a identidade trigonométrica elimina o tempo · o círculo é reconhecido · a hélice é antecipada · a verificação centrípeta entra · o período cancela a velocidade perpendicular · as duas partículas entram.

**B06:** estado equilibrado · saída maior · retorno ao equilíbrio · entrada maior · novo equilíbrio · normais externas · forma integral · divergência (e as células pequenas) · forma local · retorno ao estacionário.

**B07:** o novo sistema de eixos · F_E entra · F_B entra (com a mão direita) · a resultante · o ponto percorre o gráfico · o feixe desvia para cima · o feixe desvia para baixo · a raiz (cruza o zero) · a carga troca de sinal.

**B08:** o campo elétrico desliga · a curva aparece · o raio é medido · a rapidez do seletor é reutilizada (v = E/B é levado até a fórmula) · a razão carga-massa fecha · a leitura experimental (o que cada parte fornece).

## Seção de produção: o que a animação precisa

**A animação atual é uma base visual; a duração final será remapeada pela voz.** Nenhum bloco será cortado, nem a continuidade (B06), nem Thomson (B07 e B08).

Trechos que certamente precisam crescer (pausa, repetição de quadro útil, ou extensão da animação) para acomodar a voz:

- B00: título, atração, inversão e o gancho da neutralidade;
- B01: regra da mão direita (novo passo), módulo com os casos limite (paralelo, antiparalelo, repouso);
- B02: determinante (cada menor e cada sinal), Newton, equações acopladas, substituição na EDO, identificação da frequência angular, condições iniciais (as duas constantes), espaço das velocidades (duas figuras), integração (limites e primitiva), eliminação do tempo, centrípeta, período, duas partículas;
- B03: passo da hélice e as variações;
- B04: trabalho, potência, trabalho magnético nulo ≠ força nula, o cartão de motor;
- B05: passagem carga → corrente (portadores, velocidade de deriva), lâmina, volume, espécies;
- B06: transição para a situação geral, os quatro estados do balanço, as normais externas, a forma integral, a divergência, a forma local, o retorno ao estacionário;
- B07: eixos novos, as duas forças, o gráfico, a inversão de carga;
- B08: leitura experimental e as unidades;
- B09: síntese e retorno aos fios.

## Pontos que ainda exigem decisão humana

1. **Legenda da cena em B00 (cap3):** hoje a tela diz "se a carga líquida é zero, de onde vem a força?". A fala foi escrita sem concluir nada pela neutralidade, mas a legenda sugere a conclusão. Sugestão (para uma rodada de cena, não agora): trocar por algo como "se cada fio é neutro, por que mudar o sentido da corrente muda a interação?".
2. **Texto de tela do B06:** "variação = entra − sai" está bem. Os rótulos em tela de B07 ("rapidez atual menor/maior que a selecionada") conversam com a fala; vale conferir na revisão visual com a voz.
3. **Valor numérico de Thomson:** removido da fala; se quiserem contexto histórico, pode voltar como frase curta, sem número.
4. **Duração:** o texto é longo de propósito. O corte, se vier, é decisão editorial posterior, depois de ouvir a voz.
5. **Tom:** esta versão está sem audio tags; elas entram numa cópia (`narracao_tags.md`) só depois da revisão humana do texto e de uma revisão de oralidade (ler como fala real e tirar repetições).
