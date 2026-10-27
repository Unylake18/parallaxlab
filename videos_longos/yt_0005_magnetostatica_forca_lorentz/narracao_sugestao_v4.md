# yt_0005 — Magnetostática: narração (v4, enxuta para ~23 min, antes de qualquer TTS)

Status: **texto para revisão humana. Sem audio tags, sem voz, sem SRT, sem `texto_narracao.txt`.** Fonte da fala: este Markdown.
Ordem de produção: **física → narração natural → remapeamento da animação → duração resultante.** **Nenhuma ideia física central é cortada por duração. A narração é condensada sempre que a animação já comunica uma operação com clareza.** B00 a B09 e o CTA estão completos, inclusive a continuidade (B06) e Thomson (B07 e B08). Regra da v3: a **primeira ocorrência** de um raciocínio é explicada em detalhe; nas recorrências, a fala só remete ao que já foi aprendido; a voz não verbaliza símbolo por símbolo o que o Manim já movimenta (cancelamentos, deslocamento de termos, unidades, geometria).

> **TEMPOS NÃO SÃO LIMITES.** A coluna "Tempo atual" é só uma referência do contínuo `renders/entrega_pre_narracao/yt0005_continuo_pre_narracao_540p30.mp4` (14:57). A sincronização final é por **âncora visual** (o acontecimento na tela que a frase acompanha) e a animação será remapeada para caber na voz.

Princípio de todo trecho: (1) o que queremos descobrir; (2) que informação já temos; (3) por que esta operação ajuda; (4) o que o resultado significa fisicamente. **A voz explica a intenção, a origem dos termos, a justificativa e a interpretação; o Manim mostra as operações, os deslocamentos, os vetores, os gráficos e a geometria.** A fala não lê a álgebra.

Formato das tabelas: `| Tempo atual | Âncora visual | Fala |`.

**Revisão de oralidade (v2.1).** Lida como fala real, sem cortar bloco nem justificativa: (1) fórmulas lidas "ao pé da letra" viraram frases ("a força magnética escalar a velocidade" → "o produto escalar entre a força magnética e a velocidade"); (2) conectivos em excesso foram variados ("Então" 31 → 5, "Agora" 26 → 14, "Repara" 18 → 7; entram "Logo", "Portanto", "Assim", "Ou seja", "Olha", "Vale notar"); (3) células longas foram quebradas em frases curtas (a maior caiu de 98 para ~90 palavras; nenhuma frase passa de 34 palavras); (4) repetições removidas (limites do B01.3, "A física é a mesma" duplicado, resultado do B08 dito duas vezes); (5) **correção de conteúdo:** o fecho do B06 dizia que Gauss tinha sido "usado aqui", o que não é verdade; agora só separa as três peças (identidade matemática, conservação da carga, lei de Gauss). Versão anterior guardada em `narracao_sugestao_v2_pre_oralidade.md`. Script: `qa/oralidade_patch.py`.

**v2.2 (precisão e oralidade, sem mexer na arquitetura).** Seis patches de conteúdo: (1) B00 sem "só porque tem corrente": a fala só constata que mudar o sentido da corrente muda a interação, e que a corrente carrega alguma informação física essencial, sem concluir nada sobre contribuição elétrica; (2) B02.8: "a força de Lorentz não cria a componente paralela" virou "neste problema, a força magnética não cria nem altera essa componente; ela já estava na condição inicial e permanece constante" (prepara o B07, onde o campo elétrico volta); (3) comparações quantitativas sempre pelo **módulo da carga** (frequência e raio); (4) B04: "não transfere nada" virou "não realiza trabalho nesse deslocamento"; (5) B06: o divergente "mede a taxa líquida de saída de carga por unidade de volume, no limite de uma região muito pequena"; (6) B09: "a corrente espalhada num material é a densidade de corrente" virou "quando esse transporte de carga está distribuído pelo volume, a gente o descreve localmente pela densidade de corrente". Leitura oral contínua: bordões próximos desfeitos ("Atenção", "E repara", "Olha" encadeados no B02.4 e B02.6, "Olha a imagem" colado em "Um ponto importante" no B02.8); os paralelismos de início de frase que sobraram (B01.3, B06.3, B09) são intencionais, porque contrastam dois casos. Versão anterior guardada em `narracao_sugestao_v2.1.md`.

**v3 (condensação editorial).** Meta: ~5 mil palavras de densidade, mantendo todas as ideias físicas e âncoras. Cortado: comentário sobre o comentário, leitura do que a animação já demonstra, segundos exemplos de uma operação já ensinada, e repetições entre células vizinhas. Preservado, com explicação detalhada na primeira vez: Lorentz → Newton, equações acopladas → equação harmônica → seno e cosseno, condições iniciais → constantes, velocidade → posição (primeira integral completa; a segunda "por analogia"), integral → circunferência → raio, trabalho → potência → trabalho magnético nulo, corrente → densidade de corrente, balanço global → continuidade local, seletor → razão carga-massa. Principais enxugamentos: B01 (paralelo, antiparalelo e repouso numa só frase); B02.2 (determinante: um produto por vez, o sinal difícil da componente horizontal e a conclusão "cada componente controla a aceleração na outra direção"); B04 (motor em poucas frases); B05 (sinal da carga e sentido da corrente explicados uma só vez; sigma, rô e elementos de área nomeados à medida que aparecem); B06 (quatro estados viram equilíbrio, saída maior e entrada maior; ponte com Gauss numa frase); B07 e B08 (carga negativa direta; unidades na tela); B09 (recapitulação curta). Versão anterior guardada em `narracao_sugestao_v2.2.md`. Script: `qa/v3_patch.py`.

**v3.1 (cinco patches finais, sem outra condensação).** (1) legenda do B00 na cena trocada para "se cada fio é neutro, por que mudar o sentido da corrente muda a interação?", alinhando a tela à fala; (2) período: a comparação vale para partículas "no mesmo campo magnético, com a mesma massa e o mesmo módulo de carga, no regime não relativístico"; (3) B05: "um fio contém muitíssimos portadores móveis" e o modelo de portadores positivos é "legítimo como representação da corrente convencional"; (4) B07: "dá pra selecionar uma rapidez ajustando os campos" (o seletor não altera a rapidez de ninguém); (5) B08: "com o mesmo módulo do campo magnético nas duas etapas". Versão anterior guardada em `narracao_sugestao_v3.md`. **Texto-base congelado.**

**v4 (enxugamento para ~23 min, sem tocar nas ideias centrais).** Cortes sobre a v3.1: B01 (extremos e decomposição da velocidade em uma frase cada); B02.9 e B02.10 (verificação centrípeta e duas partículas reduzidas a uma frase de ponte; o papel de força centrípeta é dito de novo, curto, no B08); B03 (as variações viram uma frase; casos limite e q → −q saem da fala, a animação os mostra); B04 (motor em uma frase; "se outra força realizasse trabalho" sai, já dito antes); B05 (lâmina em uma frase com K e sigma; várias espécies em duas frases); B06 (três estados do balanço, normais e volume fixo condensados); B07 (regimes do gráfico e carga negativa em uma frase cada); B08 (cancelamento e isolamento juntos; resultado da caixa, "trabalho zero" repetido e unidades saem da fala, ficam na tela); B09 (recapitulação em uma frase) e redundâncias pontuais (medidores, "mesma força escrita de forma econômica", unidade de voltas por segundo, órbitas livres dos elétrons). Células com "—" não têm fala: a âncora fica na tabela e a animação segue sozinha (o remapeamento dá a ela o tempo de leitura). Preservados em detalhe: Lorentz → Newton, equações acopladas → oscilador → seno e cosseno, condições iniciais, espaço das velocidades, integração (primeira completa), circunferência → raio → período, trabalho → potência → trabalho magnético nulo, corrente → densidade de corrente, balanço → continuidade local, seletor → razão carga-massa. Versão anterior guardada em `narracao_sugestao_v3.1.md`. Script: `qa/v4_patch.py`.

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
| 0:00 | título MAGNETOSTÁTICA e a pergunta "O que um campo magnético realmente faz?" | Fala, pessoal! Bem-vindos de volta ao Parallax Lab. Hoje o assunto é magnetostática, e a gente começa por uma pergunta simples: o que um campo magnético realmente faz? |
| 0:06 | entram os dois fios paralelos, cada um com sua corrente no mesmo sentido, e os pulsos verdes correm | Pega dois fios de metal, paralelos, neutros como um todo, e faz passar uma corrente em cada um, no mesmo sentido. |
| 0:09 | as barras se curvam uma na direção da outra; setas de força | Os dois fios se atraem, sem que ninguém encoste neles: existe uma interação à distância. |
| 0:12 | a corrente do segundo fio inverte; as barras relaxam e se afastam; setas de força para fora | Inverte o sentido da corrente em um dos fios, e a interação muda: em vez de atração, repulsão. |
| 0:15 | legenda da cena: "se cada fio é neutro, por que mudar o sentido da corrente muda a interação?" | Cada fio, como um todo, é neutro, e mesmo assim existe transporte de carga. Mudar o sentido desse transporte muda a própria interação. Então a corrente carrega alguma informação física essencial aqui. A pergunta é: o que, no movimento das cargas, produz essa interação? |
| 0:18 | uma lente se fecha sobre um pedaço do fio; "olhando para uma carga em movimento" | Pra responder, a gente aproxima a imagem até enxergar uma única carga em movimento, e entende o que o campo magnético faz com ela. |

*Comentário científico:* a observação é a de Ampère (1820): correntes paralelas no mesmo sentido se atraem, em sentidos opostos se repelem. Neutralidade líquida **não** permite concluir, sozinha, nada sobre a presença ou a ausência de campo elétrico: o vídeo usa a neutralidade só como surpresa e não deduz daí que a interação é de uma natureza ou de outra. A explicação completa de onde vem o campo é o tema do próximo vídeo.

---

## B01 — A força de Lorentz e a geometria da força magnética

### B01.1 — A força de Lorentz

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 0:25 | aparece uma carga positiva com o vetor velocidade; as linhas de campo magnético entram | Aqui está uma carga elétrica, que na tela aparece como q, positiva, se movendo com uma certa velocidade dentro de um campo magnético. As linhas são só um jeito de desenhar o campo, não obstáculos. |
| 0:32 | a lei completa F = q(E + v × B) aparece | A força de Lorentz sobre uma carga tem duas partes: uma do campo elétrico, que existe mesmo com a carga parada, e outra do campo magnético, que só existe se a carga está em movimento. |
| 0:35 | o termo elétrico sai; sobra a força magnética numa caixa | Hoje o foco é a segunda parte, a força magnética: a carga multiplicada pelo produto vetorial entre o vetor velocidade e o campo magnético. |

### B01.2 — Direção e sentido: a regra da mão direita

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 0:40 | surgem a linha auxiliar paralela ao campo e o ângulo θ; o símbolo ⊗ da força aparece junto à carga | O produto vetorial dá um vetor perpendicular ao plano da velocidade e do campo. Mas isso deixa dois sentidos possíveis. Como escolher? |
| 0:42 | o símbolo ⊗ cresce, com a nota "entra na tela" | Pela regra da mão direita, e a ordem importa: primeiro a velocidade, depois o campo. Dedos na velocidade, fechando em direção ao campo: o polegar é o sentido do produto vetorial, que, para carga positiva, é o da força magnética. |
| 0:44 | destaque no símbolo ⊗ | Aqui o resultado entra na tela, e o xis dentro do círculo representa isso: a parte de trás de uma seta entrando. Se a força saísse da tela, o símbolo seria um ponto dentro do círculo: a ponta da seta vindo na nossa direção. |

### B01.3 — O módulo da força

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 0:44 | a fórmula do módulo; as leituras do ângulo e do seno | O módulo da força é o módulo da carga, vezes a rapidez, vezes a intensidade do campo, vezes o seno do ângulo entre a velocidade e o campo. Rapidez, e não velocidade: no módulo entra só o tamanho do vetor. |
| 0:47 | o ângulo varia de sessenta até oitenta e cinco graus e volta para quarenta; as leituras do seno acompanham | Mantendo fixos o módulo da carga, a rapidez e o campo, só o ângulo muda a força: quanto menor o ângulo, menor o seno e menor a força. |
| 0:50 | o ângulo vai a zero; aparece "velocidade paralela ao campo: força nula" | Nos extremos a força é nula: com a velocidade paralela ou antiparalela ao campo, ou com a carga parada. E com a velocidade perpendicular, o seno vale um e a força é a máxima. |
| 0:53 | o ângulo passa por quarenta e cinco graus; depois chega a noventa; "força máxima" | — |

### B01.4 — O sinal da carga

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 0:56 | aparece "q > 0 ⇒ ⊗"; depois a carga troca de sinal, com um clarão, e vira "q < 0 ⇒ ⊙" | Para o sinal da carga: o produto vetorial é o mesmo, mas a força é a carga vezes esse produto. Então, para carga negativa, aplica-se a mesma regra da mão direita e inverte-se o sentido. |
| 0:59 | a nota "mesmo módulo, sentido oposto" | O módulo é o mesmo; só o sentido muda: de entrar na tela para sair dela. |

### B01.5 — Só a componente perpendicular importa

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 1:02 | o diagrama ganha espaço; a velocidade se decompõe, com setas violeta e branca e linhas tracejadas | Dá pra decompor a velocidade em uma componente paralela e uma perpendicular ao campo. A paralela, no produto vetorial com o campo, dá zero: não contribui em nada. |
| 1:05 | a componente da velocidade paralela ao campo; "produto vetorial dela com o campo é zero" | — |
| 1:08 | a componente perpendicular, com a fórmula da força magnética escrita só com ela | Toda a força magnética vem da componente perpendicular: a carga vezes essa componente, em produto vetorial com o campo. |

### B01.6 — Uma escolha de caso

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 1:14 | o painel mostra "v = v perpendicular" e, depois, "agora vamos escolher o caso: componente paralela igual a zero" | Pra estudar o movimento, vamos escolher um caso: a componente paralela da velocidade vale zero. É uma condição inicial nossa, não uma regra da natureza, e mais adiante a gente tira essa restrição. |

*Comentário científico:* a força magnética é o termo dependente da velocidade na força de Lorentz (Lorentz, 1895; Heaviside e Thomson trabalharam formas anteriores). O sentido vem do produto vetorial, que é um pseudovetor: por isso a regra da mão direita, e por isso o sinal da carga inverte o sentido. A linha de campo é uma representação gráfica; a força depende do valor do campo no ponto onde a carga está.

---

## B02 — A trajetória nasce da lei de Lorentz

### B02.1 — A vista muda; os eixos e as hipóteses

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 1:20 | a vista gira até olhar ao longo do campo; as linhas viram pontos; "a perspectiva muda; a física não" | Agora olhamos ao longo do campo: as linhas viram pontinhos saindo da tela. A perspectiva muda, a física não. |
| 1:26 | aparecem os eixos y e z e a legenda "B ao longo de x"; B = B x̂; v = (v_x, v_y, v_z) | Escolhemos os eixos com o campo ao longo do eixo x. A velocidade tem então três componentes: uma ao longo do campo, e duas no plano perpendicular, uma horizontal e uma vertical. |
| 1:28 | aparece a legenda das hipóteses | Três hipóteses, válidas pra toda essa análise. O campo é uniforme: mesma intensidade e direção em toda a região. É constante: não varia no tempo. E o regime é não relativístico: velocidades pequenas comparadas com a da luz, de modo que a dinâmica de Newton vale. E só a força magnética atua. |

### B02.2 — O produto vetorial por componentes

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 1:32 | o determinante entra, com x̂, ŷ, ẑ na primeira linha; as componentes da velocidade na segunda; o campo, zero e zero na terceira | A pergunta é: como cada componente da velocidade produz aceleração nas outras direções? O produto vetorial entre a velocidade e o campo responde, e a gente calcula com um determinante: vetores unitários na primeira linha, componentes da velocidade na segunda, componentes do campo na terceira. |
| 1:38 | o menor da direção do campo é destacado; o resultado "= 0" aparece; "força ao longo do campo igual a zero" | Na direção do campo, tudo fica multiplicado por zero: não há força ao longo do campo. |
| 1:41 | o menor da direção horizontal é destacado, com as setas tracejadas que mostram quais termos se multiplicam | Na direção horizontal, sobra a componente ao longo do campo vezes zero, menos a componente vertical vezes o campo. O menor vale menos o campo vezes a componente vertical, mas a posição no determinante traz um sinal negativo. Menos vezes menos dá mais: resultado positivo. |
| 1:44 | o menor da direção vertical é destacado; o resultado aparece | Na direção vertical, o menor vale menos o campo vezes a componente horizontal, e a posição não acrescenta sinal: fica negativo. |
| 1:50 | os três resultados se juntam: v × B = (0, B v_z, −B v_y) | Juntando: nada ao longo do campo; na horizontal, o campo vezes a componente vertical; na vertical, menos o campo vezes a componente horizontal. Cada componente da velocidade controla a aceleração na outra direção. Guarda essa troca: tudo o que vem depois nasce dela. Isto ainda é só o produto vetorial: falta multiplicar pela carga. |

### B02.3 — Newton + Lorentz: as equações do movimento

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 1:56 | "Newton + Lorentz": massa vezes aceleração igual à carga vezes o resultado do produto vetorial | Entra a segunda lei de Newton: a massa vezes a aceleração é a força total, que aqui é só a magnética, já multiplicada pela carga. Até agora a lei de Lorentz dizia pra onde a força aponta; com Newton, ela passa a determinar o movimento. |
| 2:02 | as três equações por componente surgem, uma por vez; a primeira ganha a legenda "v_x constante" | Saem três equações. Na primeira, a aceleração ao longo do campo é zero: essa componente é constante. |
| 2:08 | a segunda equação; depois a terceira | Nas outras duas, a aceleração horizontal é o fator carga vezes campo dividido pela massa, multiplicado pela componente vertical da velocidade; e a vertical é menos esse fator vezes a componente horizontal. Uma componente alimenta a outra, com sinal oposto, e é esse sinal que vai produzir oscilação. Componente negativa só indica sentido negativo do eixo; rapidez negativa não existe. |

### B02.4 — Desacoplar, substituir e fazer nascer a frequência

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 2:14 | a aceleração horizontal é derivada; aparece a segunda derivada | Temos duas funções misturadas, e queremos uma equação com só uma delas. Derivamos, no tempo, a equação da componente horizontal. O fator carga vezes campo dividido pela massa sai da derivada, porque é constante. |
| 2:20 | a terceira equação sobe e a derivada da componente vertical é substituída | Sobrou a derivada da componente vertical, que a terceira equação já nos dá. Substituímos: o mesmo fator reaparece, agora com sinal negativo, multiplicando a componente horizontal. |
| 2:26 | o fator aparece ao quadrado; a equação ganha o título "Equação do oscilador harmônico para a componente horizontal" | O fator fica ao quadrado, com sinal negativo. Passando tudo pro mesmo lado: a segunda derivada da componente horizontal, mais esse fator ao quadrado vezes a própria componente, igual a zero. É a equação do oscilador harmônico, e quem a obedece é uma componente da velocidade; a partícula não está presa a mola nenhuma. Só a estrutura matemática é a mesma. |
| 2:32 | a forma geral: segunda derivada de uma função mais ω² vezes a função, igual a zero | Nessa forma, a constante ao quadrado é a frequência angular ao quadrado: a taxa com que a fase avança, em radianos por segundo. |
| 2:35 | a expressão ω² é substituída pelo módulo da raiz, depois por ω_c = ∣q∣B/m | Tomando o valor positivo, que mede o quão rápido a fase gira, e deixando o sentido da rotação pro sinal da carga: a frequência angular é o módulo da carga vezes o campo, dividido pela massa. Esta é a frequência angular ciclotrônica, e ela nasceu da equação de movimento. |
| 2:38 | a caixa com a frequência angular ciclotrônica e o nome; a legenda "sinal de q ⇒ sentido de rotação" | Maior módulo da carga, campo mais intenso ou massa menor: giro mais rápido. |

### B02.5 — A solução, as constantes e as condições iniciais

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 2:44 | "derivar 2× troca o sinal: qual função?" | Qual função, derivada duas vezes, volta com o sinal trocado e multiplicada pela frequência ao quadrado? |
| 2:50 | a segunda derivada do seno e a do cosseno, uma por vez | O seno resolve: a segunda derivada do seno de frequência vezes tempo é menos a frequência ao quadrado vezes o próprio seno. O cosseno também. |
| 2:56 | a solução geral: a primeira constante vezes cosseno mais a segunda constante vezes seno | Como a equação é linear, qualquer combinação serve: a primeira constante vezes cosseno, mais a segunda constante vezes seno. As condições iniciais vão fixar essas duas constantes. |
| 3:02 | "q positiva: componente horizontal inicial zero, componente vertical inicial igual à velocidade perpendicular"; a primeira constante vira zero | Pra carga positiva da tela: componente horizontal inicial zero, vertical inicial igual à velocidade perpendicular. Com a horizontal zero no instante inicial, o cosseno vale um e o seno zero, então a primeira constante é zero. |
| 3:08 | a equação acoplada em t = 0; "em t = 0"; a derivada da solução; a segunda constante é identificada | A condição da componente vertical entra pela equação acoplada: no instante inicial, a aceleração horizontal é a frequência angular vezes a componente vertical, que vale a velocidade perpendicular. Do outro lado, a derivada da solução é a frequência angular vezes a segunda constante. Logo a segunda constante é a velocidade perpendicular. Uma condição sobre a componente vertical fixou a constante da horizontal: é o acoplamento. |
| 3:14 | "v_z = (1/ω_c) dv_y/dt"; a derivada da solução entra | A componente vertical sai da mesma equação acoplada: é a derivada da horizontal dividida pela frequência angular. |
| 3:20 | os dois resultados lado a lado: seno e cosseno | Resultado: horizontal igual à velocidade perpendicular vezes seno, vertical igual à velocidade perpendicular vezes cosseno. |

### B02.6 — Dois espaços, uma ideia: a trajetória real e o espaço das velocidades

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 3:26 | os dois cartões entram: "trajetória real" e "espaço das velocidades"; os gráficos das duas componentes; o ponto em cada gráfico | Duas figuras diferentes. No cartão de cima, a trajetória real: o ponto é a posição da partícula. No de baixo, o espaço das velocidades: o ponto não é posição, as coordenadas são as duas componentes da velocidade, e o vetor parte da origem com comprimento igual à rapidez perpendicular. À direita, os gráficos, no mesmo instante. |
| 3:32 | a ponta do vetor dá a primeira volta no espaço das velocidades; a legenda "componentes senoidais, defasadas de noventa graus" | Seno e cosseno, defasados em noventa graus: quando um está no máximo, o outro passa por zero. A ponta do vetor percorre um círculo. |
| 3:38 | a soma dos quadrados e a identidade trigonométrica | Somando os quadrados das componentes, sobra a velocidade perpendicular ao quadrado, porque seno ao quadrado mais cosseno ao quadrado vale um. A direção muda sempre, a rapidez não. Isso não quer dizer que não há aceleração: a força magnética muda continuamente a direção do vetor velocidade sem aumentar nem diminuir a rapidez. |
| 3:50 | a carga troca de sinal com um clarão; "q negativa"; a componente horizontal troca de sinal; o vetor passa a girar no outro sentido; "mesmo módulo" | Com carga negativa e as mesmas condições iniciais, a órbita e o vetor giram no sentido contrário, com a mesma frequência angular: o módulo da carga fixa a rapidez do giro, e o sinal, o sentido. |

### B02.7 — Da velocidade à posição: integração e circunferência

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 4:05 | "a velocidade já gira; agora: onde está a partícula?"; v_y = dy/dt | Onde está a partícula? A velocidade é a taxa de variação da posição, então, pra recuperar a posição, a gente integra. |
| 4:12 | a integral com os limites: de y inicial até y em cada instante, e de zero até t; "de t' = 0 até t" | Integramos a componente horizontal da velocidade, de zero até o instante observado. O tempo dentro da integral é só uma variável auxiliar; o limite de cima é o instante que importa. |
| 4:16 | a primitiva do seno com "mais C"; depois "C se cancela nos limites" | A primitiva do seno é menos cosseno dividido pela frequência angular: a divisão vem de a derivada do cosseno trazer esse fator. A constante de integração se cancela nos limites. |
| 4:20 | a avaliação dos limites; a expressão com "um menos cosseno" | Avaliando os dois limites, o cosseno em zero vale um, e daí o um menos cosseno. A posição horizontal menos a inicial é a velocidade perpendicular sobre a frequência angular, vezes um menos cosseno. |
| 4:26 | o mesmo caminho para a componente vertical, com limites; a primitiva do cosseno é o seno | Repetindo para a componente vertical, a integral do cosseno dá o seno. |
| 4:35 | "esse fator vai ser o raio da órbita"; as duas coordenadas reescritas | Nas duas coordenadas aparece o mesmo fator, a velocidade perpendicular dividida pela frequência angular. Ele será o raio da órbita. |
| 4:38 | as expressões elevadas ao quadrado; a soma; "cosseno² mais seno² = 1" | Queremos reconhecer a curva sem depender do instante. Como as coordenadas têm seno e cosseno da mesma fase, passamos o raio pro outro lado, elevamos ao quadrado e somamos: seno ao quadrado mais cosseno ao quadrado vale um, e o tempo desaparece. |
| 4:42 | a equação da circunferência; o centro e o raio são marcados no desenho | Sobra a equação de uma circunferência, com centro e raio que saem da álgebra. A trajetória circular não foi suposta: saiu da lei de Lorentz com a segunda lei de Newton. |
| 4:46 | "R = v⊥/ω_c = m v⊥/(∣q∣ B)"; a caixa e o nome "raio da órbita magnética" | Com a frequência já conhecida, o raio é a massa vezes a velocidade perpendicular, dividido pelo módulo da carga vezes o campo. Maior massa ou velocidade perpendicular: órbita maior. Maior módulo da carga ou campo mais intenso: órbita mais fechada. |

### B02.8 — A componente ao longo do campo (a animação já antecipa a hélice)

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 4:50 | aparece "a aceleração ao longo do campo igual a zero ⇒ a componente é constante"; o eixo do campo; começa a desenhar uma trajetória | E a componente ao longo do campo? A primeira equação já respondeu: é constante. Se for zero, temos só o círculo. |
| 4:55 | "nova condição inicial: componente paralela diferente de zero, já em t = 0"; a hélice é desenhada | Na imagem, se não for zero, o círculo avança ao longo do campo e sai uma hélice. Vamos fechar primeiro o período e voltar a essa ideia com calma. |
| 5:00 | a legenda "a Lorentz não cria a componente paralela; ela preserva" | Um ponto importante: neste problema, a força magnética não cria nem altera essa componente. Ela já estava na condição inicial e permanece constante. |

### B02.9 — Verificação centrípeta e período

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 5:05 | volta o círculo, com o campo saindo da tela; "a força magnética é perpendicular à velocidade, só muda a direção da velocidade" | — |
| 5:20 | "a força magnética fornece a força centrípeta"; as duas expressões igualadas | Como verificação, a força magnética faz o papel de força centrípeta, e igualar o módulo dela à massa vezes a rapidez ao quadrado dividida pelo raio dá o mesmo raio. |
| 5:35 | "período: circunferência dividida pela rapidez"; a expressão; a substituição do raio; o cancelamento da velocidade perpendicular | O período é o tempo de uma volta: o comprimento da circunferência, dois pi vezes o raio, dividido pela velocidade perpendicular. Substituindo o raio, a velocidade perpendicular aparece em cima e embaixo e se cancela: sobra dois pi vezes a massa, dividido pelo módulo da carga vezes o campo. |
| 5:45 | "velocidades transversais diferentes mudam o raio, mas não o período" | A velocidade sumiu. Uma partícula mais rápida percorre uma circunferência maior, e o raio cresce na mesma proporção, então o tempo da volta é o mesmo. Comparando partículas no mesmo campo magnético, com a mesma massa e o mesmo módulo de carga, isso vale no regime não relativístico. |

### B02.10 — Duas partículas

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 5:50 | duas partículas partem juntas; os raios são diferentes; o relógio de fase; o clarão na passagem; "T₁ = T₂" | Duas partículas, raios diferentes, e passam juntas pelo ponto de partida a cada período. |

*Comentário científico:* a independência do período em relação à velocidade (não relativística) é o princípio do cíclotron de Lawrence: partículas mais rápidas descrevem círculos maiores no mesmo tempo, então um campo elétrico alternado de frequência fixa acelera em fase. Em velocidades relativísticas, o período passa a depender da energia da partícula, o que é a razão do síncrotron. O raio de giro é conhecido como raio de Larmor ou girorraio. As três hipóteses valem para esta análise do movimento; mais tarde o vídeo introduz o campo elétrico (B07) e situações com acumulação de carga (B06).

---

## B03 — A hélice

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 6:02 | "nova condição inicial: x(t) = x₀ + v_∥ t"; a velocidade como soma de duas componentes | Voltamos à ideia em aberto. Nova condição inicial: a velocidade tem uma componente paralela ao campo diferente de zero, já definida desde o instante inicial. |
| 6:14 | a hélice se forma; "componente paralela = constante (já definida)"; "círculo + translação = hélice" | Ao longo do campo, a partícula avança com velocidade constante; no plano perpendicular, continua girando. Círculo mais translação é uma hélice: a mesma solução de Lorentz, com a componente paralela diferente de zero. |
| 6:20 | "círculo + translação = hélice" na caixa | — |
| 6:26 | o passo p marcado ao lado da hélice; "p = 2π m ∣v_∥∣ / (∣q∣ B)" | A hélice tem o raio, que vem da componente perpendicular, e o passo: a distância, medida ao longo do eixo, entre dois pontos correspondentes separados por uma volta. Não é o comprimento sobre a curva. Como é distância, usa-se o módulo da componente paralela: o passo é esse módulo vezes o período, dois pi vezes a massa vezes o módulo da componente paralela, dividido pelo módulo da carga vezes o campo. |
| 6:32 | "velocidade perpendicular menor: raio menor, passo igual" | Comparando condições iniciais diferentes: com menos velocidade perpendicular, o raio diminui e o passo fica igual; com mais componente paralela, o passo cresce e o raio fica igual. Sem componente perpendicular, sobra um movimento retilíneo ao longo do campo. |
| 6:44 | "componente paralela maior: passo maior, raio igual" | — |
| 6:46 | os dois limites | — |
| 6:50 | "q → −q: gira ao contrário, avança igual" | — |

*Comentário científico:* o movimento helicoidal em torno das linhas de campo é a base do confinamento magnético, da aurora e da deriva de partículas nos cinturões de radiação. O passo mede só deslocamento ao longo do eixo, não o comprimento da hélice.

---

## B04 — Por que a partícula não fica mais rápida? Trabalho, potência e energia

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 7:02 | "retomando o caso: componente paralela igual a zero"; a hélice some e o círculo reaparece | Retomamos o círculo, com a componente paralela igual a zero, e a pergunta que precisamos responder. |
| 7:08 | "A partícula está acelerando. Então por que ela não fica mais rápida?"; o painel do vetor velocidade; o medidor de rapidez; a = F_B/m ≠ 0 | A partícula acelera, porque a direção da velocidade muda sempre. Então por que não fica mais rápida? Porque existe aceleração sem mudança de rapidez: o vetor gira, e o módulo dele, a rapidez, fica o mesmo, como mostra o medidor. |
| 7:20 | a velocidade e a força a noventa graus; "v velocidade", "F_B força magnética" | Pra entender, usamos trabalho. A velocidade é tangente à trajetória e a força magnética aponta pro centro: formam um ângulo reto. |
| 7:26 | "Trabalho em um deslocamento": dW = F · dr; o pequeno deslocamento nasce preso à partícula | O trabalho num pequeno deslocamento é o produto escalar entre a força e o deslocamento, que seleciona a componente da força na direção do deslocamento. Só ela transfere energia mecânica; a componente perpendicular não realiza trabalho nesse deslocamento. |
| 7:36 | "Potência instantânea": P = dW/dt | Dividindo o trabalho por um pequeno intervalo de tempo, no limite, temos a taxa instantânea: a potência. |
| 7:40 | P = F · dr/dt; "dr/dt = v"; P = F · v | Aparece a derivada do deslocamento no tempo, que é a velocidade: a potência de qualquer força é o produto escalar entre a força e a velocidade. |
| 7:48 | "Potência da força magnética": P_B = F_B · v; depois q(v × B) · v | Para a força magnética, a carga vezes o produto vetorial da velocidade pelo campo, em produto escalar com a velocidade. |
| 7:54 | "v × B ⊥ v"; P_B = 0 | Mas esse produto vetorial é perpendicular à velocidade, então o produto escalar é zero: potência magnética nula em todo instante. |
| 8:00 | "Trabalho da força magnética": W_B = ∫ P_B dt = 0 | O trabalho é a integral da potência: zero também. Atenção: trabalho nulo não é força nula. A força pode ser grande e mudar muito a direção, com trabalho zero. E a conclusão vem só da perpendicularidade entre força e velocidade: não depende de a trajetória ser circular nem de o campo ser uniforme. |
| 8:04 | "Energia cinética": E_c = ½ m ∣v∣²; "só a força magnética atua" | A energia cinética é metade da massa vezes a rapidez ao quadrado. |
| 8:08 | "Teorema trabalho–energia": ΔE_c = W_B = 0; "E_c constante ⇒ ∣v∣ constante" | Pelo teorema do trabalho e energia, a variação da energia cinética é o trabalho total. Só a força magnética atua, então a energia cinética e a rapidez ficam constantes. |
| 8:12 | a nota "E_c pode mudar se outra força realizar trabalho" | — |
| 8:16 | os quatro cards se acendem na ordem: fonte elétrica, corrente, interação magnética, movimento mecânico | Isso não quer dizer que um motor não transfira energia: ela vem da fonte elétrica, e o campo magnético organiza as forças que a convertem em movimento. |

*Comentário científico:* o teorema do trabalho e energia dá o argumento rigoroso para rapidez constante. A afirmação "força magnética não realiza trabalho" é sobre a força sobre cada carga; num motor, a energia sai da fonte, e o campo magnético redireciona as forças entre as partes do circuito. A conclusão vale para qualquer campo magnético, uniforme ou não, desde que só a força magnética atue.

---

## B05 — Da carga individual à corrente: linha, superfície, volume

### B05.1 — Muitas cargas num fio

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 8:24 | um fio cinza com portadores azuis em movimento; a seta da corrente verde; os símbolos do campo; "uma carga em movimento: F = q v × B" | Vamos levar isso a um fio. Cada carga em movimento sente a força magnética, e um fio contém muitíssimos portadores móveis. Pra simplificar, representamos os portadores como cargas positivas efetivas. |
| 8:30 | "muitas cargas: portadores positivos efetivos; representação conveniente, não um metal real" | Num metal real são elétrons, negativos, indo no sentido oposto ao da corrente convencional. Mas a contribuição pra corrente depende do produto da carga pela velocidade: invertendo os dois, o sentido da corrente convencional é o mesmo. Por isso esse modelo é legítimo como representação da corrente convencional. |

### B05.2 — Um pedaço do fio: carga, comprimento e corrente

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 8:35 | um trecho do fio é marcado, com o comprimento dℓ; depois a carga contida | Num pequeno trecho do fio, de um pequeno elemento de comprimento, há uma pequena quantidade de carga dos portadores. |
| 8:40 | "λ: carga por comprimento"; λ = dq/dℓ; dq = λ dℓ | Com lambda, a densidade linear de carga dos portadores, essa quantidade é lambda vezes o elemento de comprimento. É a densidade dos portadores, não a carga líquida do fio: um fio pode ser neutro e ter corrente. |
| 8:46 | a seção transversal e "um pequeno intervalo de tempo: a carga cruza a seção" | Corrente é a carga que atravessa uma seção por unidade de tempo: a taxa de transporte de carga. |
| 8:50 | I = dq/dt; "em dt, cada portador percorre v dt"; dq = λ v dt | Num pequeno intervalo de tempo, cada portador percorre a velocidade de deriva vezes esse intervalo, e não a agitação térmica, que em média não transporta carga numa direção. A carga que cruza a seção é lambda vezes a velocidade de deriva vezes o intervalo. |
| 8:56 | o intervalo de tempo é riscado em cima e embaixo; "I = λ v" | O intervalo se cancela: a corrente é lambda vezes a velocidade de deriva. |

### B05.3 — A força chega ao fio

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 9:05 | "dF = dq v × B"; a seta dF; o elemento de comprimento orientado | A força no trecho é a pequena quantidade de carga vezes a velocidade, em produto vetorial com o campo. |
| 9:10 | dq = λ dℓ; "v e dℓ: mesmo sentido"; λ v = I | Trocando a carga por lambda vezes o elemento de comprimento, e lambda vezes a velocidade pela corrente: a força no trecho é a corrente vezes o elemento de comprimento, no sentido da corrente, em produto vetorial com o campo. |
| 9:14 | dF = I dℓ × B na caixa | Somamos todos os trechos: a força sobre o fio inteiro é uma integral. |
| 9:20 | F = ∫ I dℓ × B; "dℓ segue a corrente convencional"; o título "Força magnética sobre um fio com corrente" | A força age sobre os portadores, e as interações deles com a rede do material transferem essa força ao corpo do condutor: é assim que a força sobre cargas móveis vira força sobre o fio. |

### B05.4 — Da linha para a superfície

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 9:30 | "a linha ganha largura"; uma lâmina cinza com setas verdes | — |
| 9:32 | a faixa de largura dw; "K: corrente por largura"; dI = ∣K∣ dw | Numa lâmina, a corrente se espalha pela largura: a densidade superficial de corrente, que na tela aparece como K, é a corrente por unidade de largura. E, com sigma, a densidade superficial de carga, ela é sigma vezes a velocidade. |
| 9:35 | o elemento de área dA_sup e a carga dq; "σ: carga por área"; dq = σ dA_sup | — |
| 9:38 | "espécie com velocidade v"; K = σ v | — |

### B05.5 — Da superfície para o volume

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 9:42 | "a superfície ganha espessura"; o prisma | Com espessura, o condutor é um volume. |
| 9:44 | a área perpendicular ao escoamento marcada; "Densidade de corrente: J = corrente por área; dI = ∣J∣ dA⊥" | A densidade de corrente, que na tela aparece como J, é a corrente por unidade de área transversal ao escoamento; uma fatia dela é seu módulo vezes a área perpendicular. |
| 9:50 | "Corrente total": I = ∫ J · da | Somando as fatias sobre uma superfície, a corrente total é a integral do produto escalar entre a densidade de corrente e o elemento vetorial de área, orientado pela normal. Em superfície inclinada, o produto escalar seleciona só a componente que atravessa. |
| 9:56 | o pequeno volume dτ com a carga dq; "ρ: carga por volume"; dq = ρ dτ; J = ρ v | Do lado da carga, rô, a densidade volumétrica de carga: a carga de um pequeno elemento de volume é rô vezes o volume, e, para uma espécie de portador, a densidade de corrente é rô vezes a velocidade. |
| 10:02 | "duas espécies de portador"; ρ₁ > 0, ρ₂ < 0; J = ρ₁v₁ + ρ₂v₂; "ρ_i com sinal" | Com várias espécies, somamos as contribuições com seus sinais. Mesmo com carga líquida zero, a densidade de corrente pode não ser zero. |
| 10:08 | F = ∫ I dℓ × B → ∫ K × B dA → ∫ J × B dτ; "a mesma interação: linha, superfície, volume" | Não são três leis: é a mesma interação escrita pra um fio, uma lâmina e um volume. A corrente é a taxa de transporte de carga; a densidade superficial a distribui pela largura; a densidade de corrente a distribui por área, e o fluxo dela recupera a corrente total. |

*Comentário científico:* a densidade linear de carga usada para deduzir I = λv é a dos portadores móveis, não a densidade líquida macroscópica do fio, que pode ser nula. A velocidade relevante é a velocidade média de deriva. Para elétrons de condução, carga negativa e velocidade de deriva oposta à corrente convencional dão a mesma contribuição que carga positiva e velocidade de sentido da corrente. A força sobre o fio é a resultante das forças sobre os portadores, transmitidas ao material por colisões e interações com a rede. A distinção entre densidade superficial de corrente (corrente por largura) e densidade volumétrica de corrente (corrente por área) é geométrica: a primeira tem unidades de ampère por metro, a segunda, de ampère por metro quadrado.

---

## B06 — Conservação da carga: a equação da continuidade

### B06.1 — Fluxo, corrente e volume de controle

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 10:20 | o prisma cinza se reduz a uma referência; entra o campo de setas verdes da densidade de corrente | Até aqui o interesse era a corrente estacionária. Agora permitimos, temporariamente, que entrada e saída de carga sejam diferentes, pra entender a conservação da carga na forma geral; depois voltamos ao estacionário. |
| 10:26 | uma superfície S aparece, com o elemento vetorial de área; "I = ∫ J · da; corrente = fluxo de J" | Fluxo mede quanto de uma grandeza atravessa uma superfície, levando em conta a orientação. Aqui a grandeza é a carga: a corrente através da superfície é o fluxo da densidade de corrente, a integral do produto escalar com o elemento vetorial de área. |
| 10:32 | a faixa "v dt" que atravessa a superfície em um pequeno intervalo | — |
| 10:38 | a superfície vira a fronteira de um volume; "Volume de controle"; a fronteira; a carga dos portadores; "J entra", "J sai" | Fechando a superfície, ela vira a fronteira de um volume de controle: uma região matemática, não um pedaço de material. Dentro há os portadores; pela fronteira, a densidade de corrente entra de um lado e sai do outro. É a mesma ferramenta dos vídeos de Gauss: superfície fechada, normais e fluxo. |

### B06.2 — O balanço: quatro estados

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 10:44 | "variação = entra − sai"; aparecem a corrente de entrada, a corrente de saída, a taxa e a carga dentro do volume; "câmera lenta" | O balanço é de contabilidade: a variação da carga dentro é o que entra menos o que sai. A animação está em câmera lenta, mas a lei é a mesma. |
| 10:46 | estado 1: entrada igual à saída; a carga dentro fica constante | Entrada igual à saída: a carga dentro fica constante. Saída maior, ela diminui; entrada maior, aumenta. A carga não aparece nem some. |
| 10:50 | estado 2: a corrente de saída cresce; a legenda "saída maior que entrada: a carga dentro diminui"; os portadores deixam o volume mais depressa | — |
| 10:56 | a corrente de saída volta ao valor da entrada; o medidor da taxa volta a zero | — |
| 10:58 | estado 3: a corrente de entrada cresce; "entrada maior que saída: a carga dentro aumenta" | — |
| 11:04 | a corrente de entrada volta; novo equilíbrio | — |

### B06.3 — Normais externas e o sinal

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 11:05 | as normais externas aparecem nas duas faces; "J · n < 0" na entrada e "J · n > 0" na saída | Usamos a normal pra fora: na entrada, o produto escalar é negativo; na saída, positivo. A integral na fronteira é o fluxo líquido pra fora: o que sai menos o que entra. |
| 11:12 | "fluxo líquido para fora"; a integral sobre a fronteira é igual à saída menos a entrada | — |
| 11:16 | "dQ/dt = −∮ J · da" | A variação da carga dentro é menos esse fluxo: se o fluxo líquido pra fora é positivo, a carga armazenada diminui. A conservação é a igualdade completa entre os dois balanços. |

### B06.4 — Forma integral, divergência e forma local

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 11:20 | "rô: carga por volume"; Q_int = ∫ ρ dτ | A carga dentro é a integral da densidade volumétrica de carga no volume, que é fixo: só a densidade pode variar no tempo. |
| 11:26 | "V fixo: só ρ varia com t" | — |
| 11:30 | "forma integral": d/dt ∫ ρ dτ = −∮ J · da; as duas metades acendem no desenho | Forma integral: a taxa de variação da carga dentro é menos o fluxo da densidade de corrente pela fronteira. |
| 11:35 | "teorema da divergência": o fluxo na fronteira vira uma integral no volume; aparece o divergente da densidade de corrente | Agora o teorema da divergência, uma identidade matemática: o fluxo através de uma fronteira fechada é a integral, no volume, do divergente do campo. O divergente da densidade de corrente mede a taxa líquida de saída de carga por unidade de volume, no limite de uma região muito pequena. O líquido importa: pode haver corrente atravessando uma região de divergente zero, se entra tanto quanto sai. |
| 11:40 | as pequenas células com setas de entrada e de saída | — |
| 11:42 | a derivada passa para dentro da integral como derivada parcial; a taxa local de variação da densidade de carga | Com volume fixo, a derivada entra na integral como derivada parcial: a taxa local de variação da densidade de carga. Então a integral dessa taxa mais o divergente da densidade de corrente é zero. |
| 11:50 | "V é qualquer"; a integral igual a zero; a expressão local | Passo sutil: uma integral nula num volume poderia vir de cancelamentos. Mas vale pra qualquer volume, em qualquer lugar; então, com regularidade, o que está dentro da integral é zero em cada ponto. Daí vem a equação local. |
| 11:56 | "Equação da continuidade": ∇·J = −∂ρ/∂t | O divergente da densidade de corrente é menos a taxa local de variação da densidade de carga: a equação da continuidade, a conservação da carga ponto a ponto. Teorema da divergência é identidade matemática; conservação da carga e lei de Gauss são afirmações físicas distintas. |

### B06.5 — Retorno ao regime estacionário

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 12:00 | "magnetostática": a taxa local de variação da densidade de carga igual a zero; depois o divergente igual a zero | No regime estacionário, o da magnetostática, a densidade de carga em cada ponto não muda no tempo: a taxa local é zero, e o divergente da densidade de corrente também. |
| 12:05 | "J ≠ 0, a corrente existe"; "∇·J = 0, nenhuma carga se acumula"; "corrente estacionária: não é nula" | Corrente estacionária não é corrente nula: ela existe e passa carga, mas nada se acumula em lugar nenhum. Também não significa ausência de portadores. Entra e sai à mesma taxa, ponto a ponto. |

*Comentário científico:* a equação da continuidade é a forma local da conservação da carga elétrica, e o teorema da divergência é só matemática (Gauss–Ostrogradski). A passagem de "integral nula em qualquer volume" para "integrando nulo" usa, além da arbitrariedade do volume, a regularidade (continuidade) do integrando. O sinal de menos vem da convenção da normal externa e não é, por si só, a conservação. Em regime estacionário, o divergente da densidade de corrente é zero; este resultado é local, e o vídeo **não** afirma nada geral sobre a topologia das linhas de corrente. Também não afirma que "carga líquida zero" é a mesma coisa que "regime estacionário".

---

## B07 — Thomson: o seletor de velocidades

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 12:10 | o volume de controle e a densidade de corrente se dissolvem; entram o feixe e a região do campo magnético | Voltamos a uma carga, agora com dois campos. O objetivo: ver como duas forças opostas podem se cancelar e deixar a carga atravessar sem desvio. |
| 12:14 | "Agora escolhemos um novo sistema de eixos adequado ao aparelho": o triedro; "v = v x̂" | Novos eixos, adequados ao aparelho, diferentes do bloco anterior: a velocidade da carga é ao longo do eixo horizontal. |
| 12:18 | entram as placas; "E = E ŷ"; depois o campo magnético "B = B ẑ" | Entre duas placas, um campo elétrico na vertical; na mesma região, um campo magnético saindo da tela. |
| 12:22 | F_E aparece com o seu nome; "F_E = qE" | O campo elétrico empurra a carga positiva pra cima: força elétrica é a carga vezes o campo elétrico, e o módulo não depende da rapidez. |
| 12:26 | F_B aparece com o seu nome; a regra da mão direita; "x̂ × ẑ = −ŷ" | O campo magnético empurra pra baixo: a carga vezes o produto vetorial da velocidade pelo campo, e a regra da mão direita confere. Esse módulo cresce com a rapidez. |
| 12:30 | a resultante F_y; "F_y = q(E − vB)" | Uma força constante pra cima, outra pra baixo crescendo com a rapidez: existe uma rapidez em que os módulos se igualam e as forças se cancelam. Esse cancelamento é o coração do seletor: dá pra selecionar uma rapidez ajustando os campos. A força vertical é a carga vezes: campo elétrico menos rapidez vezes campo magnético. |
| 12:35 | "F_y/q = E − vB" na caixa | Dividindo pela carga, sobra uma expressão só de campos e rapidez. |

### B07.2 — O gráfico

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 12:40 | o aparato vai pra esquerda; entra o gráfico à direita, com o eixo da rapidez | No gráfico, o eixo horizontal é a rapidez e o vertical é a força vertical dividida pela carga. Pra carga positiva, o sinal dessa quantidade é o da força vertical; pra negativa, não, e já voltamos a isso. |
| 12:44 | o ponto percorre a reta; o feixe acompanha o mesmo valor de rapidez | O ponto e o feixe dependem da mesma rapidez: ao aumentar, o ponto desce pela reta. |
| 12:50 | "rapidez atual menor que a selecionada: força líquida para cima"; o feixe desvia para cima | O feixe desvia pra cima se a rapidez é menor que a selecionada, e pra baixo se é maior. As curvas fora da condição selecionada são esquemáticas. |
| 12:56 | "rapidez atual maior que a selecionada"; o feixe desvia para baixo; "trajetórias esquemáticas" | — |
| 13:02 | o ponto cruza o zero; "rapidez selecionada = E/B"; "Condição de seleção de velocidades"; o feixe sai reto | Onde a reta cruza o zero, a força líquida é nula, com rapidez igual ao campo elétrico dividido pelo campo magnético. Resultante zero não significa campos zero: as duas forças existem e se cancelam. |
| 13:10 | "o seletor não iguala velocidades: seleciona" | O seletor não iguala velocidades: deixa passar sem desvio só quem já entrou com a rapidez apropriada; quem tem outra rapidez desvia, pra cima ou pra baixo. |
| 13:20 | a carga troca de sinal; "F_y/q = E − vB não depende do sinal; F_y, sim"; a rapidez selecionada vale para qualquer sinal | Com carga negativa, as forças invertem, mas a rapidez selecionada é a mesma. |

*Comentário científico:* é o princípio do filtro de velocidades (filtro de Wien) usado em espectrômetros de massa e relacionado ao trabalho de J. J. Thomson (1897) sobre a razão carga-massa do elétron. A força elétrica independe da rapidez e a magnética cresce com ela, daí a existência de uma rapidez de cancelamento. A resultante nula exige que as duas forças estejam presentes e se cancelem. As trajetórias fora da condição selecionada são esquemáticas: mostram o sentido do desvio, não a solução completa em campos cruzados.

---

## B08 — Medindo a razão carga-massa

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 13:30 | o campo elétrico é desligado; o rótulo "só B, mesmo v"; uma região magnética; o feixe se curva | Partículas com a rapidez já determinada pelo seletor entram numa região só com campo magnético. Desligar o campo elétrico aqui não significa que o seletor funcione sem ele: ele já fez o trabalho. |
| 13:35 | a trajetória desenha um arco; o raio é marcado | Sob só o campo magnético, a partícula descreve um arco de circunferência, e podemos medir o raio no desenho. |
| 13:40 | "∣q∣ v B = m v²/R"; o campo magnético, em magenta | A força magnética faz o papel de força centrípeta, a resultante que aponta pro centro: o módulo da carga vezes a rapidez vezes o campo, igual à massa vezes a rapidez ao quadrado dividida pelo raio. |
| 13:44 | a rapidez é cancelada | Cancelando uma rapidez e isolando: a razão entre o módulo da carga e a massa é a rapidez dividida pelo produto do campo magnético e do raio. |
| 13:48 | "∣q∣/m = v/(B R)"; a massa desce, o campo magnético atravessa a igualdade | — |
| 13:52 | "usando a velocidade selecionada (mesmo módulo de B nas duas etapas)"; v = E/B é levado até a fórmula | A rapidez vem do seletor: campo elétrico dividido pelo campo magnético. Com o mesmo módulo do campo magnético nas duas etapas, a razão fica o campo elétrico dividido pelo produto entre o quadrado do campo magnético e o raio. |
| 13:58 | a caixa "Razão carga–massa em módulo" | — |
| 14:00 | "↑ vem do seletor"; "com E e B conhecidos, medir R fornece ∣q∣/m"; o sentido da curva dá o sinal | O que cada parte fornece: os campos conhecidos dão a rapidez; o raio dá a razão entre o módulo da carga e a massa; o sentido da curva dá o sinal da carga. O experimento não dá carga e massa separadas: dá a razão. |
| 14:04 | o módulo da velocidade permanece o mesmo, trabalho magnético zero | — |
| 14:06 | as unidades: m/s e C/kg | — |

*Comentário científico:* o desenho é uma **representação didática** do princípio de medição associado ao trabalho de Thomson; a semicircunferência mostrada não reproduz literalmente o aparato histórico de 1897, que usava deflexão de um feixe de raios catódicos em campos elétrico e magnético em um tubo. O experimento mede a razão entre o módulo da carga e a massa, não os dois separadamente. O valor numérico moderno da razão carga-massa do elétron não é necessário aqui e foi removido do texto falado.

---

## B09 — Síntese e a pergunta que fica

| Tempo atual | Âncora visual | Fala |
|---|---|---|
| 14:10 | "força magnética: a lei que sustenta tudo": F_B = q v × B | Recapitulando: a força magnética gera círculos e hélices; cargas organizadas formam a corrente, descrita localmente pela densidade de corrente; e, com dois campos, uma carga vira o seletor e a medida da razão entre carga e massa. |
| 14:15 | o círculo; o vetor velocidade; "componente paralela = 0: círculo, frequência angular = ∣q∣B/m" | — |
| 14:18 | a hélice; "componente paralela diferente de zero: hélice" | — |
| 14:21 | o fio cinza com cargas; a seta da corrente; "muitas cargas: corrente" | — |
| 14:24 | o campo de setas verdes; "densidade de corrente em regime estacionário"; o divergente igual a zero | — |
| 14:27 | o aparato de Thomson em esquema; v = E/B; ∣q∣/m = E/(B²R) | — |
| 14:33 | os dois fios do começo; a corrente verde se move; os anéis de campo magnético | Voltando aos dois fios: a corrente em cada um é transporte organizado de carga. O campo magnético age sobre os portadores móveis, e a força é transmitida ao material. |
| 14:39 | as setas de atração; a corrente de ambos no mesmo sentido | Com correntes no mesmo sentido, a força mostrada é de atração. Já sabemos como um campo conhecido age sobre uma corrente; falta saber de onde vem esse campo. |
| 14:44 | "Como uma corrente cria B?" | Como uma corrente cria um campo magnético? |
| 14:48 | o CTA: PARALLAX LAB; "Inscreva-se para acompanhar os próximos vídeos"; "Próximo: como uma corrente gera campo magnético" | Essa pergunta leva à lei de Biot–Savart, tema do próximo vídeo. Se quiser acompanhar, se inscreve no canal. A gente se vê por lá! |

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

1. ~~Legenda da cena em B00~~ **resolvida na v3.1:** a legenda da cena passou a ser "se cada fio é neutro, por que mudar o sentido da corrente muda a interação?" (ajuste em `cena.py`; o contínuo precisa ser re-renderizado para refletir).
2. **Texto de tela do B06:** "variação = entra − sai" está bem. Os rótulos em tela de B07 ("rapidez atual menor/maior que a selecionada") conversam com a fala; vale conferir na revisão visual com a voz.
3. **Valor numérico de Thomson:** removido da fala; se quiserem contexto histórico, pode voltar como frase curta, sem número.
4. **Duração:** a v4 tem 4.256 palavras de fala, que a 3,0 palavras por segundo (cadência medida no yt_0002) dão cerca de 23,6 min de voz (26 min a 2,7), contra 14:57 da animação atual; o remapeamento da animação pela voz resolve a diferença. As 29 âncoras sem fala ("—") são trechos em que a animação segue sozinha; no remapeamento elas ganham só o tempo de leitura.
5. **Tom:** esta versão está sem audio tags; elas entram numa cópia (`narracao_tags.md`) só depois da revisão humana do texto e de uma revisão de oralidade (ler como fala real e tirar repetições).
