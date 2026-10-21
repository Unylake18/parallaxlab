# yt_0006 — Lei de Biot–Savart: sugestão de narração (v1, para fechar com o GPT antes do TTS)

Status: **sugestão para revisão. Voz não gerada.** Depois de aprovado, vira `texto_narracao.txt` e a cópia com audio tags (`narracao_tags.md`) pela skill `gerar-narracao`.
Base de tempo: o preview aprovado `renders/preview/YT0006BiotSavart_acabamento_v4.mp4` (17:38, 960×540, 15 fps, sem áudio). Os tempos são o **início** de cada evento (legenda, fórmula ou nome de lei), registrados por instrumentação do próprio código e calibrados com as seções renderizadas (±1,5 s).
Princípio (igual ao yt_0001, yt_0002 e yt_0005): **a voz explica o porquê; o Manim mostra o como.** A fala não lê a álgebra: diz o que cada passo quer, de onde vem cada termo e o que o resultado significa. **O vídeo se molda à voz** (remapeamento por âncoras): este roteiro é mais longo do que a animação, e isso é esperado. No fim há a estimativa por bloco e a lista dos pontos em que a animação precisa de folga.

Arquitetura: gancho (do 5.1 para o 5.2) → regime magnetostático → geometria fonte–observador → a lei → distribuições (linha, superfície, volume) → clínica do ângulo → superposição → método → trecho retilíneo finito → fio infinito → força entre fios → espira no eixo → duas checagens → síntese → gancho para o próximo vídeo → CTA.

## Como falar as grandezas (regra: pelo nome, nunca só pela letra)

| Na tela | Na fala |
|---|---|
| I₁, I₂, I | **a corrente do primeiro fio**, **a corrente do segundo fio**, **a corrente** (1ª vez: "a corrente, que na tela aparece como I") |
| **B**, **B**₁ | **o campo magnético**; **o campo magnético do primeiro fio** |
| **F**₂ | **a força sobre o segundo fio** |
| **L** (fio 2) | **o vetor comprimento do fio** (1ª vez: "que na tela aparece como L") |
| V, Q, dQ/dt | **o volume**; **a carga dentro do volume**; **a taxa de variação da carga no tempo** |
| I_entra, I_sai | **a corrente que entra**; **a corrente que sai** |
| ρ, **J** | **rô, a densidade de carga**; **a densidade de corrente, que é a corrente por área** |
| ∇·**J** | **o divergente da densidade de corrente** |
| P, O | **o ponto de observação**; **a origem** |
| **r′**, **r** | **a posição da fonte**; **a posição do observador** |
| **R** (negrito) | **o vetor separação, da fonte até o observador** |
| R (sem negrito) | **a distância entre a fonte e o observador** (o módulo do vetor separação) |
| **R̂** | **o vetor unitário de separação** (o vetor separação dividido pelo seu módulo) |
| dℓ, d**ℓ** | **um pedacinho do fio**; **o elemento de fio, orientado no sentido da corrente** |
| θ | **o ângulo entre o elemento de fio e o vetor separação** (depois: "o ângulo teta") |
| μ₀ | **mi zero, a permeabilidade magnética do vácuo** |
| K, **K**, dw | **a densidade superficial de corrente, corrente por largura**; **a largura da faixa** |
| da, dA⊥, dτ | **o elemento de área**; **a área da seção transversal**; **o elemento de volume** |
| **t̂** | **o vetor unitário tangente ao caminho, na direção da corrente** |
| x, a | **a posição do elemento ao longo do fio, medida a partir do pé da perpendicular**; **a distância perpendicular do ponto ao fio** |
| x̂, ŷ, ẑ | **os vetores unitários nos eixos x, y e z** |
| α | **o ângulo alfa, entre a perpendicular até o fio e o vetor separação** (nunca confundir com o ângulo teta) |
| α_A, α_B ; α₁, α₂ | **o ângulo alfa na extremidade inicial e na final**; **alfa um e alfa dois, os dois ângulos positivos** |
| B_trecho, B_total, B_restante | **o campo do trecho**, **o campo total**, **o campo do resto do circuito** |
| B_∞ | **o campo do fio infinito** |
| d | **a distância entre os dois fios** |
| F₂/L | **a força por unidade de comprimento** |
| Na espira: R | **o raio da espira** (mudou de significado: avisar) |
| s | **a separação entre o elemento e o ponto de observação** |
| z | **a posição do ponto ao longo do eixo** (a distância do ponto ao plano da espira) |
| φ, dφ | **o ângulo de posição do elemento na volta**; **um pedacinho desse ângulo** |
| γ | **o ângulo gama** (do triângulo, entre a separação e o raio) |
| dB_z, d**B**_⊥ | **a parte axial do campo infinitesimal**; **a parte transversal do campo infinitesimal** |
| B_z | **o campo magnético sobre o eixo** |

Operações por extenso ("vezes", "dividido por", "ao quadrado", "ao cubo", "elevado a três meios", "igual a", "mais", "menos"). Funções: "seno", "cosseno", "tangente", "secante", "integral de … até …", "derivada de … em relação a …". Números como serão falados. Letra só quando a tela aponta e o símbolo é novo.

Evitar: dizer "campo zero" onde o que é zero é a contribuição de um elemento; dizer que o elemento de corrente "existe sozinho" (ele é uma construção que só faz sentido dentro da integral); falar "constante do vácuo" para o mi zero (sempre "permeabilidade magnética do vácuo"); chamar de "R" a distância geral e o raio da espira sem avisar a troca; confundir o ângulo teta (da lei) com o ângulo alfa (da substituição); ler a álgebra símbolo por símbolo.

---

## B00 — Do 5.1 para o 5.2: a pergunta (0:00–0:46)

| Tempo | Na tela | Fala |
|---|---|---|
| 0:00 | título "Como calcular o campo criado pela corrente?"; fio com corrente fluindo | Fala, pessoal! Bem-vindos de volta ao Parallax Lab. No vídeo anterior, a gente viu o que um campo magnético faz com uma carga em movimento. Hoje a pergunta é a inversa: de onde vem esse campo? Como calcular o campo magnético criado por uma corrente? |
| 0:02.6 | fio de aço, traços verdes correndo, seta de I₁ | Aqui está um fio de metal. Dentro dele passa uma corrente elétrica, que na tela aparece como I um: a corrente do primeiro fio. Repara que os traços verdes correm, mas o fio, em si, fica parado. |
| 0:09.4 | três anéis magenta em volta do fio | Essa corrente cria, em volta do fio, um campo magnético. As linhas desse campo são círculos concêntricos: elas não saem do fio, elas envolvem o fio. A tela desenha só alguns círculos, mas o campo existe em todos os pontos ao redor. |
| 0:12.6 | caixa "I₁ → B₁" | Resumindo: da corrente do primeiro fio nasce o campo magnético do primeiro fio. E é essa passagem, da corrente para o campo, que a gente quer entender. |
| 0:20.0 | entra o segundo fio; um anel maior passa por ele; B₁ no fio 2 | Agora coloca um segundo fio, paralelo ao primeiro. Exatamente no lugar onde ele está, o campo do primeiro é tangente ao círculo. Ou seja, é perpendicular ao fio. |
| 0:25.7 | I₂, vetor comprimento, F₂ azul; caixa "Força magnética sobre um fio" | Por esse segundo fio também passa corrente, a corrente do segundo fio. E o campo do primeiro fio empurra as cargas que estão em movimento nele. A força sobre o segundo fio é a corrente do segundo fio, vezes o vetor comprimento do fio, vezes o campo magnético do primeiro, e esse "vezes" final é um produto vetorial. Essa é a força magnética sobre um fio, que a gente já conhece. |
| 0:31.0 | caixa "B₁ = ?" | Só que falta uma peça. A gente sabe o que o campo faz com o segundo fio, mas ainda não sabe calcular o próprio campo do primeiro. Quanto vale o campo magnético do primeiro fio? |
| 0:33.4 | legenda "Falta a regra que liga o campo à corrente que o produz"; depois título "LEI DE BIOT–SAVART" | Falta a regra que liga o campo à corrente que o produz. E essa regra tem nome: é a lei de Biot–Savart. Hoje a gente vai construir essa lei passo a passo, a partir da geometria, e depois aplicar em dois casos clássicos: o fio reto e a espira circular. |

*Por quê:* a observação de Ørsted (1820) mostrou que a corrente cria campo magnético; logo depois, Biot e Savart mediram o campo de um fio longo e Ampère estudou a força entre fios. As linhas circulares vêm da simetria do fio reto: nada distingue um ponto de um círculo em volta do fio de outro. O gancho precisa deixar claro que o 5.1 explicou o efeito do campo (força de Lorentz) e que o 5.2 explica a causa (como a corrente gera o campo).

## B01 — Regime magnetostático (0:46–1:35)

| Tempo | Na tela | Fala |
|---|---|---|
| 0:45.9 | título "Corrente estacionária: fluxo sem acúmulo" | Antes de escrever a lei, um aviso: ela vale para um regime específico, chamado magnetostático. Vamos ver o que isso quer dizer. |
| 0:49.6 | fio atravessando um volume V; barra da carga Q | Imagina um pedaço de fio atravessando um volume imaginário, que na tela aparece como V, o volume. Se entra mais corrente do que sai, a carga dentro do volume cresce com o tempo. A barra azul mostra isso. |
| 0:54.6 | dQ/dt = I_entra − I_sai | Em fórmula: a taxa de variação da carga dentro do volume, no tempo, é igual à corrente que entra menos a corrente que sai. É só a conservação da carga, contada na entrada e na saída. |
| 0:58.7 | as duas setas ficam iguais | Agora imagina que entra e sai exatamente a mesma corrente. |
| 1:04.4 | I_entra = I_sai ⟹ dQ/dt = 0 | Então a diferença é zero, e a taxa de variação da carga no tempo também. A carga dentro do volume não muda. |
| 1:09.0 | legenda "Q permanece constante…" | A corrente atravessa o volume, mas não se acumula nele. |
| 1:13.5 | ∂ρ/∂t + ∇·J = 0; nome "Equação da continuidade" | A mesma ideia, agora ponto a ponto. Chamando de rô a densidade de carga, e de J a densidade de corrente, que é a corrente por área, a equação diz: a taxa de variação da densidade de carga no tempo, mais o divergente da densidade de corrente, é igual a zero. Essa é a equação da continuidade, e ela só diz que a carga se conserva. |
| 1:21.4 | ∂ρ/∂t = 0 ⟹ ∇·J = 0 | Se a densidade de carga não muda no tempo, o primeiro termo desaparece, e sobra: o divergente da densidade de corrente é zero. Em palavras: sem acúmulo de carga. |
| 1:28.2 | caixa ∂J/∂t = 0 | Mas a lei de Biot–Savart pede uma segunda condição, que é outra ideia: a própria densidade de corrente não pode mudar no tempo. A derivada dela em relação ao tempo é zero. |
| 1:30.4 | legenda "Corrente independente do tempo." | Corrente independente do tempo. As duas condições juntas definem a magnetostática. |

*Por quê:* são duas hipóteses distintas e o texto não pode fundi-las. (1) Conservação da carga com densidade estacionária ⇒ divergente de J igual a zero: as linhas de corrente não começam nem terminam, formam circuitos fechados. (2) Corrente estacionária ⇒ o campo magnético é constante no tempo. Quando a corrente varia, o campo elétrico variável também contribui para o campo magnético (Maxwell); isso fica para depois.

## B02 — Geometria fonte–observador (1:35–2:29)

| Tempo | Na tela | Fala |
|---|---|---|
| 1:35.1 | título "Construir a separação fonte–observador" | Agora a parte que mais confunde quem estuda esse assunto: a geometria. Para somar o campo de cada pedacinho da corrente, a gente precisa saber exatamente onde está cada pedacinho, e onde estamos observando. |
| 1:39.0 | fio; ponto verde sobre ele | Cada pedaço do fio é uma fonte do campo. Esse ponto verde marca uma delas. |
| 1:42.3 | aparece P | E queremos o campo em um ponto qualquer do espaço: o ponto de observação, que na tela aparece como P. |
| 1:45.6 | aparece O | Para localizar os dois, a gente escolhe uma origem qualquer, o ponto O. A escolha é livre: o resultado final não vai depender dela. |
| 1:48.7 | setas de O até a fonte e até P; "posição da fonte", "posição do observador" | A partir da origem, um vetor localiza a fonte: é a posição da fonte, que a gente escreve como r com uma linha. Outro vetor localiza o ponto de observação: é a posição do observador, r sem a linha. Cuidado com essa linha: ela marca a fonte. |
| 1:53.1 | aparece o vetor R; "fonte → observador" | Repara que existem dois caminhos da origem até o ponto de observação. O direto, que é a posição do observador. Ou o que passa pela fonte: primeiro vai até a fonte, e depois da fonte até o observador. |
| 1:55.2 | r′ + R = r | Esse segundo trecho, da fonte até o observador, é o vetor separação, que na tela aparece como R em negrito. Os dois caminhos chegam no mesmo lugar. Então: a posição da fonte, mais o vetor separação, é igual à posição do observador. |
| 1:59.9 | R = r − r′ | Isolando o vetor separação: ele é a posição do observador menos a posição da fonte. Ou seja, aponta da fonte até o observador. Repara na ordem: observador menos fonte. |
| 2:06.2 | seta pisca | O comprimento dessa seta é uma distância. |
| 2:07.9 | R = \|R\|; nota "distância fonte–observador" | A gente escreve R, sem negrito, para o módulo do vetor separação: a distância entre a fonte e o observador. São duas coisas diferentes com a mesma letra: uma é vetor, com direção e sentido; a outra é só o comprimento. |
| 2:12.1 | P fixo; a fonte anda no fio | Pra fixar a ideia: segura o observador parado e anda com a fonte ao longo do fio. Só o vetor separação muda. Cada posição da fonte tem o seu. |
| 2:22.7 | dℓ e o ângulo θ | Falta um último ingrediente: o elemento de fio, um pedacinho do fio, com uma orientação. Ele é tangente ao fio e aponta no sentido da corrente. E o ângulo teta é o ângulo entre esse elemento de fio e o vetor separação. |

*Por quê:* convenção de Griffiths e de Jackson: r′ marca a fonte, r marca o ponto de campo, o vetor separação é r menos r′. O elemento de fio orientado no sentido da corrente convencional é o que permite escrever a lei como produto vetorial.

## B03 — A lei de Biot–Savart (2:29–4:00)

| Tempo | Na tela | Fala |
|---|---|---|
| 2:28.9 | título "Biot–Savart: uma lei experimental" | Agora a lei. Ela é experimental: nasceu das medidas de Biot e Savart, em mil oitocentos e vinte, e Laplace escreveu a forma que a gente usa hoje. Vamos montar a lei fator por fator, vendo o que cada medida diz. |
| 2:33.3 | I e dℓ; símbolo ⊙ em P | Primeiro fator: o elemento de corrente, que é a corrente vezes o pedacinho de fio. Cada elemento produz uma contribuição ao campo no ponto de observação. Mais corrente, ou um pedaço maior, dá uma contribuição maior: o campo infinitesimal é proporcional à corrente vezes o comprimento do elemento. |
| 2:38.5 | P se afasta | Segundo fator: a distância. Quanto mais longe está o observador, mais fraca é a contribuição. |
| 2:43.2 | dB ∝ I dℓ / R² | A medida mostra que a dependência é com o inverso do quadrado da distância. Então: proporcional à corrente vezes o comprimento, dividido pela distância ao quadrado. |
| 2:47.3 | R → 2R ⟹ dB → dB/4 | Um teste mental: se a distância dobra, a contribuição cai para um quarto, porque dois ao quadrado é quatro. |
| 2:54.2 | o ângulo varia de 22° a 90° | Terceiro fator: a direção. Só a parte do elemento de fio que é perpendicular à separação conta. |
| 2:59.5 | dB ∝ I dℓ sen θ / R² | Isso entra com o seno do ângulo teta. Com teta igual a noventa graus, o seno vale um, e a contribuição é máxima. Com teta igual a zero, o seno vale zero, e não há contribuição. |
| 3:04.0 | caixa μ₀/4π; nome "constante de proporcionalidade"; nota | Para virar uma igualdade, falta uma constante. No Sistema Internacional, ela é mi zero dividido por quatro pi. O mi zero é a permeabilidade magnética do vácuo, e diz o quanto o vácuo deixa o campo magnético se estabelecer. Vale, aproximadamente, quatro pi vezes dez elevado a menos sete, em tesla metro por ampère. |
| 3:09.7 | dB = (μ₀/4π) · I dℓ sen θ / R² | Com ela, o módulo do campo infinitesimal é mi zero sobre quatro pi, vezes a corrente, vezes o comprimento, vezes o seno do ângulo, tudo dividido pela distância ao quadrado. |
| 3:15.7 | paralelogramo de dℓ e R̂ | Repara: comprimento vezes seno tem um significado geométrico. É a área do paralelogramo formado pelo elemento de fio e pelo vetor unitário de separação. |
| 3:20.5 | \|dℓ × R̂\| = dℓ sen θ | E essa área é exatamente o módulo do produto vetorial entre os dois. |
| 3:25.5 | legenda "O produto vetorial guarda o módulo e a direção" | Só que o produto vetorial guarda duas coisas: o módulo, e também a direção, perpendicular aos dois vetores. |
| 3:26.2 | dB = (μ₀/4π) I dℓ × R̂ / R² | Por isso a lei fica melhor escrita assim: o campo infinitesimal, agora como vetor, é mi zero sobre quatro pi, vezes a corrente, vezes o produto vetorial do elemento de fio pelo vetor unitário de separação, dividido pela distância ao quadrado. |
| 3:33.0 | R̂ = R/R | O vetor unitário de separação é o próprio vetor separação dividido pelo seu módulo. Ele tem comprimento um e guarda só a direção. |
| 3:37.5 | R/R dentro da lei | Agora é só substituir na lei. Dentro do produto vetorial aparece o vetor separação dividido pela distância. |
| 3:41.7 | o R sobe/desce | Esse módulo, que está embaixo no numerador, passa para baixo, e fica multiplicando a distância ao quadrado que já estava lá. |
| 3:48.8 | R·R² vira R³ | Distância vezes distância ao quadrado dá distância ao cubo: os expoentes se somam. |
| 3:49.5 | lei completa; nome "Lei de Biot–Savart" | E chegamos: o campo infinitesimal é mi zero sobre quatro pi, vezes a corrente, vezes o produto vetorial do elemento de fio pelo vetor separação, dividido pela distância ao cubo. Essa é a lei de Biot–Savart. |
| 3:55.1 | legenda "O campo de um elemento de corrente" | E repara no que ela dá: o campo de um único elemento de corrente, um pedacinho. Para ter o campo de um circuito inteiro, a gente vai precisar somar todos. |

*Por quê:* Biot e Savart mediram o campo de um fio longo (proporcional ao inverso da distância); a dependência com o seno e com o inverso do quadrado da distância para o elemento é a forma de Laplace, que reproduz essa medida quando integrada. Atenção científica: o elemento de corrente isolado não existe fisicamente, porque a corrente estacionária forma circuitos fechados; só a integral sobre o circuito é medida. A forma com o vetor unitário (R̂/R²) e a forma com o vetor separação (**R**/R³) são equivalentes. O mi zero valia exatamente quatro pi vezes dez elevado a menos sete newton por ampère ao quadrado até a revisão do SI de 2019; hoje é medido e coincide com esse valor em precisão muito alta, então a fala "aproximadamente" é a correta.

## B04 — Da linha à superfície e ao volume (4:00–5:19)

| Tempo | Na tela | Fala |
|---|---|---|
| 4:00.3 | título "Da linha à superfície e ao volume" | Até aqui, a corrente estava concentrada em um fio fino. Mas nem toda corrente é assim: ela pode se espalhar em uma superfície, ou ocupar um volume inteiro. A lei é a mesma; o que muda é o que a gente chama de elemento de corrente. |
| 4:04.1 | I dℓ; integral na caixa auxiliar | No fio fino, a fonte é a corrente vezes o elemento de fio. E o campo total é a integral, ao longo do fio, desse elemento vezes o vetor unitário de separação, dividido pela distância ao quadrado. |
| 4:10.9 | a faixa se abre em lâmina | Numa lâmina, a corrente se espalha em largura. |
| 4:15.7 | faixa de largura dw; dI = K dw | Pega uma faixa estreita, de largura dw. A corrente que passa por ela é a corrente por unidade de largura, que na tela aparece como K, vezes a largura da faixa. |
| 4:22.6 | dℓ = t̂ dℓ | O elemento de fio, por sua vez, é o vetor unitário tangente ao caminho, que dá a direção da corrente, vezes o comprimento. |
| 4:26.9 | K = K t̂; nota "A/m" | Juntando, a densidade superficial de corrente vira um vetor: o valor da corrente por largura, vezes a direção da corrente. A unidade é ampère por metro. |
| 4:34.7 | da = dw dℓ | A largura da faixa vezes o comprimento é a área do elemento de superfície. |
| 4:38.4 | dI dℓ = K da | Então o elemento de corrente fica: a densidade superficial de corrente vezes o elemento de área. |
| 4:41.8 | B = (μ₀/4π) ∫ K × R̂ / R² da | E a lei, para uma superfície: o campo é mi zero sobre quatro pi, vezes a integral, sobre a superfície, da densidade superficial de corrente vezes o vetor unitário de separação, dividido pela distância ao quadrado. |
| 4:46.3 | a lâmina vira bloco | Num volume, a corrente atravessa uma seção transversal. |
| 4:51.1 | dI = J dA⊥ | A corrente que passa por uma seção pequena é a densidade de corrente vezes a área dessa seção. |
| 4:55.0 | J = J t̂; nota "A/m²" | A densidade de corrente também é um vetor, com a direção da corrente. E a unidade é ampère por metro quadrado: corrente por área. |
| 5:03.0 | dτ = dA⊥ dℓ | A seção transversal vezes o comprimento que ela percorre é o volume do elemento. |
| 5:07.2 | bloco verde; dI dℓ = J dτ | Então o elemento de corrente vira a densidade de corrente vezes o elemento de volume. |
| 5:11.4 | B = (μ₀/4π) ∫ J × R̂ / R² dτ | E a lei, para um volume: a integral, sobre o volume, da densidade de corrente vezes o vetor unitário de separação, dividido pela distância ao quadrado. |
| 5:15.8 | legenda "A medida de integração acompanha a distribuição" | Repara no padrão: a medida de integração acompanha a distribuição. Comprimento no fio, área na superfície, volume no sólido. O resto da lei não muda. |

*Por quê:* as três formas são equivalentes: o elemento de corrente é I dℓ numa linha, K vezes da numa superfície e J vezes dτ num volume. O fio fino é o limite de uma distribuição de volume com seção muito pequena. A distinção de unidades (ampère, ampère por metro, ampère por metro quadrado) ajuda a reconhecer qual forma usar.

## B05 — Isolar o efeito do ângulo (5:19–6:23)

| Tempo | Na tela | Fala |
|---|---|---|
| 5:19.5 | título "Isolar o efeito do ângulo" | Agora vamos olhar só o efeito do ângulo, deixando a distância fixa. |
| 5:22.8 | dB ∝ sen θ; gráfico do seno | Com a distância fixa, o campo infinitesimal é proporcional ao seno do ângulo teta. O gráfico ao lado mostra o seno, de zero a cento e oitenta graus, e o ponto branco acompanha o ângulo. |
| 5:29.9 | θ = 0; "dB = 0 neste elemento" | Com teta igual a zero, o elemento de fio aponta direto para o ponto de observação. A contribuição desse elemento é zero, embora a corrente continue circulando. Repara no que é zero: é só a contribuição deste elemento, não o campo total. |
| 5:36.7 | θ = 30° | Com trinta graus, a contribuição já começa a crescer. |
| 5:42.6 | θ = 60° | Sessenta graus: está bem mais perto do máximo. |
| 5:48.5 | θ = 90° | Noventa graus: contribuição máxima, para essa distância. |
| 5:54.4 | θ = 150° | Cento e cinquenta graus: ela volta a enfraquecer. O seno de cento e cinquenta é igual ao de trinta. |
| 6:00.2 | θ = 180° | E com cento e oitenta graus, o elemento aponta para o lado oposto, e a contribuição volta a ser zero. |
| 6:05.3 | legenda "O produto vetorial dá também a direção"; a vista gira | Mas o produto vetorial também dá a direção, e para enxergar isso a gente muda a vista, para uma perspectiva em três dimensões. |
| 6:10.3 | seta de dB perpendicular ao plano; regra da mão direita | É a regra da mão direita: os dedos vão do elemento de fio para o vetor separação, e o polegar mostra o sentido do campo infinitesimal. |
| 6:15.0 | dℓ × R = −R × dℓ | O produto vetorial é anticomutativo: trocar a ordem dos fatores troca o sinal. |
| 6:17.8 | a seta inverte | Por isso a ordem importa: primeiro o elemento de fio, depois o vetor separação. Se a gente inverter, o campo aponta para o lado contrário. |

*Por quê:* o módulo do produto vetorial é dℓ R sen θ, e o campo infinitesimal é perpendicular tanto ao elemento quanto à separação. Quando o elemento é paralelo ou antiparalelo à separação, o produto é nulo: isso vale para a contribuição de um elemento, não para o campo total.

## B06 — Superposição: construir uma soma vetorial (6:23–7:04)

| Tempo | Na tela | Fala |
|---|---|---|
| 6:22.7 | título "Construir uma soma vetorial" | Agora, como transformar a contribuição de um elemento no campo da corrente inteira? Pelo princípio da superposição. |
| 6:25.7 | fio, P, e os cinco elementos aparecendo um de cada vez | Fixa um observador. Cada elemento da fonte dá uma contribuição, com sua direção e seu tamanho. Pega cinco elementos, e para cada um calcula a contribuição ao campo no ponto de observação. |
| 6:33 | as setas são transportadas para uma região livre | Como cada contribuição é um vetor, a soma é uma soma de vetores: a gente coloca a ponta de uma na cauda da outra. |
| 6:40.6 | resultante; B ≈ ΔB₁ + ΔB₂ + … + ΔB₅ | Ponta a ponta, a resultante liga o início da primeira ao fim da última. Ela é, aproximadamente, o campo total: a soma das cinco contribuições. |
| 6:48.3 | cinquenta elementos menores | Agora refina: mais elementos, cada um com contribuição menor. A aproximação melhora. |
| 6:51.5 | B ≈ Σ ΔB_i | Com N elementos, o campo é aproximadamente a soma, de i igual a um até N, de cada contribuição. |
| 6:55.7 | B = ∫ dB | No limite em que cada pedaço tem comprimento zero, e o número de pedaços vai ao infinito, a soma vira integral: o campo é a integral do campo infinitesimal. |

*Por quê:* na magnetostática vale a superposição, porque a lei é linear na corrente: o campo de várias correntes é a soma dos campos de cada uma. A integral é vetorial, calculada componente a componente.

## B07 — Aplicar o método (7:04–7:29)

| Tempo | Na tela | Fala |
|---|---|---|
| 7:03.7 | título "Aplicar o método ao desenho"; lista de quatro passos | Vamos resumir o método em quatro passos. |
| 7:07.8 | "1 separação R" | Primeiro: quem produz o campo, e onde a gente quer calculá-lo? |
| 7:10.7 | R = r − r′ | A geometria fornece o vetor separação, a posição do observador menos a da fonte, e com ele a distância e a direção. |
| 7:15.5 | "2 direção de dB"; símbolo ⊙ | Segundo: a direção do campo infinitesimal. Pela regra da mão direita, aqui todas as contribuições apontam para fora da tela. |
| 7:18.6 | dℓ = dx x̂ | Terceiro: o elemento de fio e a variável de integração. Percorrer o fio é percorrer a posição x, e o elemento é dx, no sentido do eixo x. |
| 7:22.7 | B_trecho = ∫ dB de x_A até x_B | Quarto: os limites e a integral. O campo do trecho é a integral do campo infinitesimal, entre as duas extremidades do trecho. |

## B08 — Trecho retilíneo finito (7:29–10:32)

### B08.1 — Geometria e produto vetorial (7:29–8:33)

| Tempo | Na tela | Fala |
|---|---|---|
| 7:28.7 | título "Contribuição de um trecho retilíneo do circuito" | Vamos aplicar tudo isso em um caso real: um pedaço reto de fio. |
| 7:34.0 | o trecho dentro de um circuito fechado | Só que um pedaço reto é apenas parte de um circuito. O campo total é a soma vetorial do campo do trecho com o campo do resto do circuito. |
| 7:38.0 | "Calcule só o trecho" | Por enquanto, a gente calcula só o trecho. |
| 7:43.9 | dℓ = dx x̂ | O elemento de fio é dx, vezes o vetor unitário do eixo x: tem comprimento dx e aponta ao longo do fio. |
| 7:46.8 | x e a em tela; descrições "posição do elemento" e "distância até P" | Chama de x a posição do elemento ao longo do fio, medida a partir do pé da perpendicular. E de a a distância perpendicular do ponto ao fio. |
| 7:48.7 | R = −x x̂ + a ŷ | Agora o vetor separação. Do elemento até o ponto de observação, a gente anda menos x na direção do fio, e a na direção perpendicular. |
| 7:52.4 | partes paralela e perpendicular em destaque | O vetor separação tem uma parte paralela ao fio, e uma parte perpendicular ao fio. |
| 7:53.1 | dℓ × R = dx x̂ × (−x x̂ + a ŷ) | Agora o produto vetorial do elemento de fio pelo vetor separação, que é o que a lei pede. |
| 7:57.7 | produto distribuído | Distribuindo o produto, ele se divide em dois pedaços, um para cada parte do vetor separação. |
| 8:03.0 | destaque na parte paralela; x̂ × x̂ = 0 | A parte paralela: o produto vetorial de um vetor com ele mesmo é zero. Faz sentido: o elemento de fio e a parte paralela apontam na mesma direção, então o seno do ângulo entre eles é zero. |
| 8:04.7 | destaque na parte perpendicular; x̂ × ŷ = ẑ | A parte perpendicular: x chapéu vezes y chapéu dá z chapéu, que é a regra da mão direita aplicada aos eixos. |
| 8:06.4 | o termo paralelo vira zero | Repara: o termo da parte paralela some, porque foi multiplicado por zero. |
| 8:10.7 | legenda "A parte paralela zera" | Sobra só a parte perpendicular: a distância a, vezes dx, na direção z, que sai da tela. |
| 8:11.4 | a vista gira; ⊙ vira o eixo z | Para ver isso melhor, a vista gira: o símbolo de ponto dentro do círculo vira o próprio eixo z, saindo da tela. |
| 8:15.7 | dℓ × R = a dx ẑ | Então, o produto vetorial vale a vezes dx, no sentido de z. |
| 8:19.2 | legenda "Substitua na lei"; nome "Lei de Biot–Savart" | Agora a gente leva isso para a lei de Biot–Savart. |
| 8:22.8 | dB = (μ₀ I/4π) a dx / R³ ẑ | O campo infinitesimal fica: mi zero vezes a corrente, sobre quatro pi, vezes a distância perpendicular a vezes dx, dividido pela distância ao cubo, na direção z. |

*Por quê:* a escolha de x como coordenada ao longo do fio e de a como distância perpendicular reduz o vetor separação a duas componentes. O zero do produto vetorial paralelo explica por que só a componente perpendicular de R importa: é o seno da lei, na forma vetorial.

### B08.2 — Pitágoras e substituição angular (8:33–10:00)

| Tempo | Na tela | Fala |
|---|---|---|
| 8:32.2 | triângulo (a, x, R); nome "Teorema de Pitágoras" | Mas a distância R muda quando o elemento anda ao longo do fio. Pelo teorema de Pitágoras, no triângulo retângulo: R ao quadrado é x ao quadrado mais a ao quadrado. |
| 8:37.0 | dB = … a dx / (x² + a²)^{3/2} | Trocando na fórmula: no denominador fica x ao quadrado mais a ao quadrado, elevado a três meios. |
| 8:43.6 | "Mova o elemento"; ângulos θ e α | Vamos ver o que muda quando o elemento anda. O módulo do campo infinitesimal muda, mas o sentido não: continua para fora da tela. |
| 8:56.7 | "θ (da lei) e α (da perpendicular) são ângulos diferentes" | Atenção: aqui existem dois ângulos diferentes. O teta é o da lei, entre o elemento de fio e o vetor separação. O alfa é outro: é o ângulo entre a perpendicular até o fio e o vetor separação. |
| 9:02.8 | tan α = x/a | A integral em x é difícil. Então a gente troca de variável, e o triângulo ajuda: a tangente de alfa é x dividido por a. |
| 9:06.1 | "Troque x por α"; x = a tan α | Trocando x por alfa: x é a vezes a tangente de alfa. |
| 9:10.1 | dx = a sec²α dα | Derivando em relação a alfa: dx é a vezes a secante ao quadrado de alfa, vezes d alfa. |
| 9:13.5 | legenda "Derive" | A derivada da tangente é a secante ao quadrado. É daí que ela vem. |
| 9:16.1 | dx entra na fórmula | Esse dx, a gente leva para dentro da fórmula, no lugar do dx antigo. |
| 9:20.4 | "Reescreva o denominador" | Falta reescrever o denominador em função de alfa. |
| 9:21.1 | x² + a² = a² tan²α + a² | Primeiro, trocando x por a tangente de alfa: a ao quadrado vezes tangente ao quadrado, mais a ao quadrado. |
| 9:24.1 | a²(1 + tan²α) | Pondo a ao quadrado em evidência: a ao quadrado, vezes um mais tangente ao quadrado. |
| 9:26.9 | a² sec²α | Pela identidade trigonométrica, um mais tangente ao quadrado é secante ao quadrado. |
| 9:29.8 | (x²+a²)^{3/2} = a³ sec³α | Elevando a três meios: a ao cubo vezes secante ao cubo. |
| 9:34.6 | substituição no denominador | Agora o denominador inteiro está escrito em função de alfa. |
| 9:39.1 | "Junte os a do numerador" | Simplificando: primeiro, juntar os dois a do numerador, que viram a ao quadrado. |
| 9:43.1 | a²/a³ = 1/a | A ao quadrado sobre a ao cubo é um sobre a. |
| 9:47.0 | sec²α / sec³α = 1/sec α | Secante ao quadrado sobre secante ao cubo é um sobre secante. |
| 9:50.9 | 1/sec α = cos α | E um sobre a secante é exatamente o cosseno de alfa. |
| 9:54.1 | "Fica cos α dα" | Então sobra o cosseno de alfa vezes d alfa. |
| 9:54.8 | dB = (μ₀ I / 4π a) cos α dα ẑ | O campo infinitesimal é mi zero vezes a corrente, sobre quatro pi a, vezes cosseno de alfa vezes d alfa, na direção z. Repara que a distância R desapareceu: só ficou o ângulo. |

*Por quê:* x igual a a tangente de alfa torna o denominador um cubo de secante e cancela a secante ao quadrado vinda de dx; esse é o motivo da substituição, e não só truque algébrico. Nunca confundir teta (ângulo na lei) com alfa (ângulo na substituição): são complementares em cada elemento.

### B08.3 — Limites e resultado (10:00–10:32)

| Tempo | Na tela | Fala |
|---|---|---|
| 10:02.9 | extremidades do trecho; α_A e α_B | Os limites de integração são os ângulos nas duas extremidades do trecho. O da esquerda é negativo, e o da direita é positivo. |
| 10:07.0 | integral de cos α | Então o campo do trecho é mi zero vezes a corrente, sobre quatro pi a, vezes a integral do cosseno de alfa, de alfa A até alfa B. |
| 10:11.1 | [sen α] | A primitiva do cosseno é o seno. |
| 10:14.7 | sen α_B − sen α_A | Aplicando os limites: seno de alfa B menos seno de alfa A. |
| 10:18.2 | α_A = −α₁ ; α_B = α₂ | Como alfa A é negativo, chama de alfa um o oposto dele, que é positivo. O seno de menos alfa um é menos o seno de alfa um, e a diferença vira soma. |
| 10:22.3 | B_trecho = (μ₀ I / 4π a)(sen α₁ + sen α₂) | E o resultado é: o campo do trecho é mi zero vezes a corrente, sobre quatro pi a, vezes seno de alfa um mais seno de alfa dois. |

*Por quê:* é o resultado clássico do campo de um segmento reto (Griffiths, Exemplo 5.5). Direção: para fora da tela, com o ponto no semiplano da regra da mão direita da corrente. Só vale para o trecho: o campo total de um circuito fechado soma todos os trechos.

## B09 — O fio infinito como limite (10:32–11:04)

| Tempo | Na tela | Fala |
|---|---|---|
| 10:31.9 | título "O fio infinito como limite" | Agora, um caso-limite: e se o fio for muito, muito comprido? |
| 10:37.3 | os ângulos crescem; cartão com os graus | Conforme o fio cresce, os dois ângulos, alfa um e alfa dois, se aproximam de noventa graus. O cartão mostra o valor: passa de oitenta e cinco graus. |
| 10:45.8 | sen α₁ → 1, sen α₂ → 1 | O seno de noventa graus vale um. Então os dois senos tendem a um. |
| 10:49.8 | B_∞ = (μ₀ I / 4π a)(1 + 1) | Colocando na fórmula: mi zero vezes a corrente, sobre quatro pi a, vezes um mais um. |
| 10:53.8 | B_∞ = μ₀ I / 2π a; nome "Campo de um fio retilíneo infinito" | E isso dá mi zero vezes a corrente, sobre dois pi vezes a distância. Esse é o campo de um fio retilíneo infinito. |
| 10:58.5 | legenda "B ∝ 1/a" | Repara: o campo cai com o inverso da distância ao fio. E o fio infinito nasceu como o limite do trecho finito. |

*Por quê:* o fio infinito é uma idealização, boa quando o ponto está perto do fio comparado ao comprimento, e longe das pontas. Esse resultado concorda com a medida original de Biot e Savart (campo proporcional ao inverso da distância).

## B10 — A força entre dois fios (11:04–11:49)

| Tempo | Na tela | Fala |
|---|---|---|
| 11:03.6 | título "A corrente cria o campo que produz a força" | Com o campo do fio infinito, a gente consegue fechar o que abriu no começo do vídeo: a força entre dois fios. |
| 11:07.5 | fio 1, I₁ para cima | O primeiro fio carrega uma corrente para cima. |
| 11:11.5 | símbolos ⊗ à direita e ⊙ à esquerda | Pela regra da mão direita: à direita do fio, o campo entra na tela, e a gente desenha um xis dentro do círculo. À esquerda, o campo sai, e é o ponto dentro do círculo. Esses símbolos mostram só o sentido do campo, não o tamanho. |
| 11:15.2 | B₁ = μ₀ I₁ / 2π d; nome | O campo do primeiro fio, na posição do segundo, é mi zero vezes a corrente do primeiro fio, sobre dois pi vezes a distância entre os fios. |
| 11:19.0 | legenda "A intensidade está na fórmula" | A intensidade está na fórmula: o campo cai com um sobre a distância. Os símbolos só indicam o sentido. |
| 11:22.4 | segundo fio, L e F₂ | A força sobre o segundo fio é a corrente dele, vezes o vetor comprimento, vezes o campo do primeiro. Pela regra da mão direita, ela aponta para o primeiro fio. |
| 11:26.8 | F₂ = I₂ L μ₀ I₁ / 2π d | Colocando o campo do primeiro fio na fórmula, a força é a corrente do segundo fio, vezes o comprimento, vezes mi zero vezes a corrente do primeiro fio, sobre dois pi vezes a distância. |
| 11:30.8 | F₂/L = μ₀ I₁ I₂ / 2π d; unidade N/m | Dividindo pelo comprimento, a força por unidade de comprimento é mi zero vezes as duas correntes, sobre dois pi vezes a distância. A unidade é newton por metro. |
| 11:36.0 | legenda "Mesmo sentido: os fios se atraem" | Com as correntes no mesmo sentido, os fios se atraem. |
| 11:40.7 | I₂ inverte | Agora inverte a corrente do segundo fio. O campo do primeiro não muda, mas a força inverte: os fios se repelem. |

*Por quê:* é a observação de Ampère (1820): correntes paralelas atraem, antiparalelas repelem. Até a revisão do SI de 2019, o ampère era definido por essa força: dois fios longos a um metro de distância, cada um com um ampère, se atraem com dois vezes dez elevado a menos sete newtons por metro. Pela terceira lei de Newton, o segundo fio também puxa o primeiro com força igual e oposta.

## B11 — A espira circular no eixo (11:49–15:26)

### B11.1 — Duas vistas da mesma geometria (11:49–12:36)

| Tempo | Na tela | Fala |
|---|---|---|
| 11:48.5 | título "Uma espira, duas vistas da mesma geometria" | Segundo caso: a espira circular. A gente quer o campo magnético sobre o eixo dela. |
| 11:52.5 | vista frontal; aço com traços verdes; seta de I | Primeiro, a vista frontal. A corrente percorre a espira, e a espira tem um raio. |
| 11:58 | legenda "Na espira, a notação muda" | Atenção, porque a notação muda. Na espira, R passa a ser o raio da espira. A separação entre o elemento e o ponto de observação passa a se chamar s. E z é a posição ao longo do eixo. Depois, a gente mantém esses nomes colados na figura. |
| 12:01.6 | dℓ = R dφ | Pega um pedaço pequeno da espira, que corresponde a um ângulo pequeno, d fi. O comprimento desse arco é o raio vezes esse ângulo, com o ângulo em radianos. |
| 12:09.9 | a espira gira de 0° a 90° | Agora a gente gira a mesma espira, de zero a noventa graus. Vista de perfil, ela vira uma linha, e o eixo aparece. |
| 12:15.2 | P no eixo; ⊙ do dℓ | O ponto de observação está sobre o eixo, e o elemento de fio aponta para fora da tela. |

### B11.2 — Triângulo, módulo e direção (12:23–13:18)

| Tempo | Na tela | Fala |
|---|---|---|
| 12:23.2 | zoom no triângulo (R, z, s) | Agora o triângulo. Os três lados são: o raio da espira, a posição do ponto no eixo, e a separação, que liga o elemento ao ponto. |
| 12:27.0 | s² = R² + z²; nome "Teorema de Pitágoras" | É um triângulo retângulo. Pelo teorema de Pitágoras: a separação ao quadrado é o raio ao quadrado mais a posição no eixo ao quadrado. |
| 12:36.7 | θ = 90° | O elemento de fio sai da tela, e a separação está no plano da tela. Então o ângulo entre eles é noventa graus. |
| 12:39.9 | "Biot–Savart no módulo" | Biot–Savart, no módulo, com a distância sendo agora a separação. |
| 12:44.1 | sen 90° | Com o seno de noventa graus. |
| 12:47.0 | legenda "sen 90° = 1" | Que vale um. |
| 12:47.7 | dB = (μ₀/4π) I dℓ / s² | O campo infinitesimal é mi zero sobre quatro pi, vezes a corrente vezes o comprimento do elemento, dividido pela separação ao quadrado. Repara: aqui é a separação ao quadrado, e não o raio. |
| 12:52.8 | seta de dB oblíqua | Pela regra da mão direita, o campo infinitesimal é perpendicular à separação e perpendicular ao elemento. Por isso ele aponta inclinado. |

### B11.3 — Projeção axial, par oposto e cancelamento (12:57–13:55)

| Tempo | Na tela | Fala |
|---|---|---|
| 12:57.8 | "Projete no eixo" | Mas o que importa sobre o eixo é a componente ao longo do eixo. Vamos projetar. |
| 12:58.5 | dB_z = dB cos γ | A parte axial é o campo infinitesimal vezes o cosseno do ângulo gama. |
| 13:03.5 | arcos de γ nos dois vértices | Os dois ângulos gama são iguais, porque os lados correspondentes são perpendiculares dois a dois. |
| 13:08.2 | cos γ = R/s | E o triângulo dá o cosseno: é o cateto adjacente, que é o raio, dividido pela hipotenusa, que é a separação. |
| 13:12.3 | dB_z = dB R/s | Então a parte axial é o campo infinitesimal vezes o raio dividido pela separação. |
| 13:17.8 | "Mova P" | Se o ponto anda no eixo, a parte axial acompanha a separação. |
| 13:26.6 | elemento oposto aparece | Agora o elemento diametralmente oposto, na mesma espira, com a mesma distância até o ponto. |
| 13:30.8 | "As transversais cancelam"; setas ciano | As partes transversais, uma de cada lado, têm o mesmo tamanho e sentidos opostos. Pondo uma depois da outra, voltam ao ponto de partida: elas se cancelam. |
| 13:40.6 | "As axiais se somam"; dB_z + dB_z = 2 dB_z | Já as partes axiais têm o mesmo sentido, e se somam. |
| 13:46.4 | legenda "O par mostrou a simetria. Integre UMA contribuição" | Atenção: esse par serviu só para provar a simetria. Na integral, a gente usa uma contribuição por elemento, não duas. Senão o fator dois seria contado a mais. |
| 13:50.3 | dB_z sozinho | Voltamos a uma contribuição: a parte axial de um elemento. |

*Por quê:* a simetria em torno do eixo faz as componentes transversais de elementos opostos se cancelarem; só a componente axial sobrevive. O par é uma demonstração, não uma etapa da conta: integrando em toda a volta, cada elemento já entra uma única vez.

### B11.4 — Álgebra do integrando (13:54–14:37)

| Tempo | Na tela | Fala |
|---|---|---|
| 13:54.0 | título "Do triângulo ao integrando axial" | Hora de montar o integrando. A gente parte do triângulo e da lei. |
| 13:57.3 | dB = (μ₀/4π) I dℓ / s² no cartão auxiliar | Vamos substituir o campo infinitesimal pelo módulo da lei. |
| 14:00.2 | dB_z = (μ₀/4π)(I dℓ / s²)(R/s) | Então a parte axial é mi zero sobre quatro pi, vezes a corrente vezes o elemento, dividido pela separação ao quadrado, e tudo isso vezes o raio sobre a separação. |
| 14:05.3 | dℓ = R dφ | Lembra do arco: o elemento de fio é o raio vezes d fi. |
| 14:08.5 | "Troque dℓ pelo arco" | Troca o elemento de fio por esse arco. |
| 14:09.1 | dB_z = … I R dφ R / s² s | Aparece o raio duas vezes no numerador, e a separação ao quadrado e a separação no denominador. |
| 14:14.4 | "Agrupe os dois fatores de R" | Agrupa: raio vezes raio, e separação ao quadrado vezes separação. |
| 14:15.1 | R · R, s² · s | Mostrando as duas multiplicações. |
| 14:20.3 | R², s³ | Raio vezes raio é o raio ao quadrado. Separação ao quadrado vezes separação é a separação ao cubo. |
| 14:24.6 | s³ = (R² + z²)^{3/2} | A separação ao cubo, por Pitágoras, é raio ao quadrado mais a posição no eixo ao quadrado, elevado a três meios. |
| 14:27.7 | "Use s² = R² + z²" | Colocamos isso no denominador. |
| 14:29.9 | dB_z = (μ₀/4π) I R² / (R²+z²)^{3/2} dφ | A parte axial de um elemento é mi zero sobre quatro pi, vezes a corrente vezes o raio ao quadrado, dividido por raio ao quadrado mais posição no eixo ao quadrado, elevado a três meios, vezes d fi. |

### B11.5 — Integral da volta e resultado (14:38–15:26)

| Tempo | Na tela | Fala |
|---|---|---|
| 14:38.8 | "Integre uma volta: só φ varia" | Agora a gente dá uma volta inteira. O raio, a posição no eixo, a separação e a corrente não mudam. O que muda é o ângulo de posição, que vai de zero a dois pi. |
| 14:47.5 | "Somadas, as contribuições formam o campo total B"; seta B_z sobre o eixo | Somando todas as contribuições, a gente tem o campo magnético total. Repara que a seta inclinada de um elemento sai, e fica só a seta axial: o campo sobre o eixo. |
| 14:49.0 | B_z = ∫₀^{2π} … dφ | O campo sobre o eixo é a integral, de zero a dois pi, da parte axial de cada elemento. |
| 14:53.3 | constantes saem da integral | Tudo o que não depende do ângulo sai da integral, e sobra só a integral de d fi. |
| 14:57.5 | legenda "O que não depende de φ sai da integral" | Resta somar o ângulo da volta. |
| 14:58.2 | ∫₀^{2π} dφ = 2π | A integral de d fi, de zero a dois pi, vale dois pi. |
| 15:02.0 | B_z = … · 2π | Então o campo sobre o eixo é aquela mesma expressão, vezes dois pi. |
| 15:06.4 | legenda "A volta inteira dá 2π; junto com o 4π da lei, resta 1/2" | Dois pi dividido por quatro pi, do mi zero sobre quatro pi, dá um meio. |
| 15:07.1 | 2π/4π | Dois pi sobre quatro pi. |
| 15:10.3 | 2π/4π = 1/2 | É igual a um meio. |
| 15:13.8 | B_z(z) = μ₀ I R² / 2(R²+z²)^{3/2}; o 2 vem do 1/2 | E esse um meio vira o dois no denominador. O campo sobre o eixo é mi zero vezes a corrente vezes o raio ao quadrado, dividido por dois vezes raio ao quadrado mais posição no eixo ao quadrado, elevado a três meios. |
| 15:19.5 | nome "Campo no eixo de uma espira" | Esse é o campo no eixo de uma espira de corrente. |

*Por quê:* o resultado clássico (Griffiths, Exemplo 5.6): campo no eixo de uma espira. A seta total sobre o eixo fecha a ideia visual: as componentes transversais cancelaram e as axiais somaram. A álgebra usa duas fusões que valem uma etapa própria: raio vezes raio dá raio ao quadrado, e dois pi sobre quatro pi dá um meio.

## B12 — Duas checagens (15:26–16:28)

| Tempo | Na tela | Fala |
|---|---|---|
| 15:26.5 | título "Checagem 1: o centro da espira" | Toda fórmula deve passar por testes. Primeiro: o centro da espira. |
| 15:27.2 | "Leve P até z = 0"; P anda | Leva o ponto de observação até a posição zero no eixo, que é o centro. |
| 15:33.2 | B(0) = μ₀ I R² / 2R³ | Colocando z igual a zero, o denominador vira raio ao cubo, e o campo é mi zero vezes a corrente vezes o raio ao quadrado, dividido por dois vezes o raio ao cubo. |
| 15:37.7 | legenda "A separação é igual ao raio" | Faz sentido: no centro, a separação até cada elemento é igual ao raio. |
| 15:38.3 | B(0) = μ₀ I / 2R | Simplificando: mi zero vezes a corrente, dividido por dois vezes o raio. |
| 15:42.4 | setas axiais coincidem; legenda "No centro não há componente lateral" | No centro, cada contribuição já aponta ao longo do eixo. Não sobra componente lateral para cancelar. |
| 15:50.7 | título "Checagem 2: muito longe da espira" | Segundo teste: muito longe da espira. |
| 15:51.8 | B_z(z) | A expressão geral continua valendo. |
| 15:54.9 | "Afastamos P do centro" | Afasta o ponto do centro. |
| 16:00.1 | esquema graduado em z/R | Aqui a espira foi ampliada só para permanecer legível. A régua marca a posição em unidades do raio. |
| 16:07.8 | "\|z\| ≫ R" | Quando a posição no eixo é muito maior que o raio, a distância domina o denominador. |
| 16:08.5 | (R²+z²)^{3/2} = \|z\|³(1 + R²/z²)^{3/2} | Pondo o módulo de z ao cubo em evidência, sobra um mais raio ao quadrado sobre z ao quadrado, elevado a três meios. |
| 16:12.8 | R²/z² → 0 | Quando o raio é muito menor, essa fração tende a zero. Então o denominador é, aproximadamente, o módulo de z ao cubo. |
| 16:17.2 | B_z ∼ μ₀ I R² / 2\|z\|³ | E o campo cai com um sobre z ao cubo. |
| 16:21.4 | legenda "Longe, o campo cai como 1/\|z\|³" | Repara que isso cai bem mais rápido que o um sobre a distância do fio. |
| 16:22.7 | fio: B ∝ a⁻¹ ; espira: B ∝ \|z\|⁻³ | Fio: campo proporcional a a elevado a menos um. Espira: proporcional ao módulo de z elevado a menos três. |

*Por quê:* a checagem no centro dá um resultado conhecido (mi zero vezes a corrente sobre dois raios). Longe, a espira se comporta como um dipolo magnético, e o campo de um dipolo cai com o cubo da distância. Frase opcional para o final do bloco: "É o comportamento típico de um dipolo magnético, e a gente volta nisso mais para frente."

## B13 — Uma lei, geometrias diferentes (16:28–17:11)

| Tempo | Na tela | Fala |
|---|---|---|
| 16:28.2 | título "Uma lei; geometrias diferentes" | Vamos amarrar tudo. |
| 16:32.4 | R = r − r′ | A fonte e o observador constroem o vetor separação: posição do observador menos posição da fonte. |
| 16:36.2 | lei de Biot–Savart | A lei de Biot–Savart dá a contribuição de cada elemento, com direção e intensidade próprias. |
| 16:41.2 | B = ∫ dB | Somar essas contribuições recupera o campo da fonte inteira. |
| 16:49.8 | B_∞ = μ₀ I / 2π a | Para um fio infinito, o campo cai com um sobre a distância. |
| 16:56.9 | o fio vira espira | E a mesma lei, com outra fonte, dá a espira. |
| 17:00.6 | B_z(z) | O campo sobre o eixo, com o raio da espira e a posição no eixo. |
| 17:05.0 | legenda "Fio: B ∝ a⁻¹ · espira (longe): B ∝ \|z\|⁻³" | A mesma lei, duas geometrias, dois comportamentos: no fio, o campo cai com um sobre a distância; na espira, longe, com um sobre z ao cubo. |

## B14 — Pergunta final e CTA (17:11–17:38)

| Tempo | Na tela | Fala |
|---|---|---|
| 17:10.8 | título "Que estrutura o campo magnético possui?"; círculos em volta da fonte | Mas a gente ainda não terminou. Olha de novo para as linhas do campo em volta da corrente: elas fecham sobre si mesmas. |
| 17:12 | "O que revela o divergente?" ; "E o rotacional? E Ampère?" | O que o divergente do campo magnético revela? E o rotacional? E o que a lei de Ampère tem a ver com isso? |
| 17:18.5 | legenda "Que propriedades esse campo necessariamente possui?" | Que propriedades esse campo magnético necessariamente possui? Essa é a pergunta do próximo vídeo. |
| 17:24 | CTA Parallax Lab; anéis tracejados; "Inscreva-se…" | Se você gostou do vídeo, se inscreve no canal para acompanhar os próximos. Valeu, pessoal, e até a próxima! |
| 17:30 | "Próximo: divergente, rotacional e a lei de Ampère" | No próximo vídeo: o divergente, o rotacional e a lei de Ampère. |

*Por quê:* a lei de Biot–Savart leva a duas propriedades locais do campo (o divergente e o rotacional), e a lei de Ampère é a forma integral da segunda. É o gancho natural para o próximo vídeo.

---

## Decisões abertas para fechar com o GPT

0. **Duração (decisão principal):** esta v1 é a versão completa e detalhada pedida, mas soma cerca de 4,9 mil palavras, ou ~29 minutos de voz (contra 17:38 da animação). Se o vídeo final tiver de ficar perto de 22 a 24 minutos, o caminho é enxugar a fala (não a animação): reduzir as linhas de leitura de álgebra em B08.2, B11.4 e B03, que concentram a maior folga, e fundir as linhas curtas do B05 e do B13. Os blocos que mais pesam: B11 (5:12 de voz), B08 (4:52), B03 (3:06). Posso gerar uma v1.1 enxuta mantendo as âncoras de tempo.
1. **Abertura:** "Fala, pessoal!" como nos longos anteriores, ou entrada mais seca por já estarmos no meio da série.
2. **Valor do mi zero:** falar "aproximadamente quatro pi vezes dez elevado a menos sete tesla metro por ampère" (proposto) ou omitir o número e deixar só "permeabilidade magnética do vácuo".
3. **Dipolo (B12):** manter a frase opcional sobre o dipolo magnético, ou deixar só para o vídeo seguinte.
4. **Definição do ampère (B10):** a nota histórica do SI pré-2019 fica na fala ou só na descrição do vídeo.
5. **Aviso da notação da espira (11:58):** a legenda aparece por alguns segundos; confirmar que a fala acompanha exatamente esse momento.
6. **Teaser:** "divergente, rotacional e a lei de Ampère" foi escolha minha a partir do gancho da tela; confirmar com a ordem do mapa curricular.

## Estimativa de duração e folga da animação

Contagem automática: palavras da coluna Fala de cada linha, a 2,8 palavras por segundo; a janela de cada linha vai do seu início até o início da linha seguinte.

| Bloco | Janela no vídeo | Palavras | Voz (2,8 p/s) | Folga extra necessária |
|---|---|---|---|---|
| B00 | 0:00.0–0:45.9 | 335 | 1:59.6 | +1:13.7 |
| B01 | 0:45.9–1:35.1 | 276 | 1:38.6 | +0:53.2 |
| B02 | 1:35.1–2:28.9 | 368 | 2:11.4 | +1:17.9 |
| B03 | 2:28.9–4:00.3 | 522 | 3:06.4 | +1:35.5 |
| B04 | 4:00.3–5:19.5 | 367 | 2:11.1 | +0:55.8 |
| B05 | 5:19.5–6:22.7 | 239 | 1:25.4 | +0:31.3 |
| B06 | 6:22.7–7:03.7 | 158 | 0:56.4 | +0:15.4 |
| B07 | 7:03.7–7:28.7 | 110 | 0:39.3 | +0:15.9 |
| B08 | 7:28.7–10:31.9 | 819 | 4:52.5 | +2:01.0 |
| B09 | 10:31.9–11:03.6 | 114 | 0:40.7 | +0:10.5 |
| B10 | 11:03.6–11:48.5 | 245 | 1:27.5 | +0:45.2 |
| B11 | 11:48.5–15:26.5 | 874 | 5:12.1 | +1:56.6 |
| B12 | 15:26.5–16:28.2 | 239 | 1:25.4 | +0:33.5 |
| B13 | 16:28.2–17:10.8 | 106 | 0:37.9 | +0:06.7 |
| B14 | 17:10.8–17:38.0 | 91 | 0:32.5 | +0:09.5 |
| **Total** | 0:00.0–17:38.0 | **4863** | **28:56.8** | **+12:41.7** |

Leitura: a voz soma cerca de 28:56.8, contra 17:38 de animação. A folga extra (soma dos trechos em que a fala de uma linha passa da janela até o próximo evento) é de cerca de 12:41.7: é isso que a animação precisa segurar (pausas de leitura, paradas em quadro) para a voz caber, e é o que o remapeamento por âncoras resolve. Por isso o vídeo final deve ficar em torno de 30:19.7, e não nos 17:38 do preview mudo. Blocos com maior folga pedem as pausas mais longas: veja a coluna da direita.
