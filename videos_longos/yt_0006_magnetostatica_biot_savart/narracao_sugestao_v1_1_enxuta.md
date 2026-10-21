# yt_0006 — Lei de Biot–Savart: sugestão de narração (v1.1 enxuta, para fechar com o GPT antes do TTS)

Status: **v1.1 enxuta (alvo ~21–22 min de voz). Voz não gerada.** A v1 completa (~29 min) fica em `narracao_sugestao.md`. Depois de aprovado, vira `texto_narracao.txt` e a cópia com audio tags (`narracao_tags.md`) pela skill `gerar-narracao`.
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
| 0:00 | título "Como calcular o campo criado pela corrente?"; fio com corrente fluindo | Fala, pessoal! Bem-vindos de volta ao Parallax Lab. No vídeo anterior, a gente viu o que um campo magnético faz com uma carga em movimento. Hoje a pergunta é a inversa: como calcular o campo magnético criado por uma corrente? |
| 0:02.6 | fio de aço, traços verdes correndo, seta de I₁ | Aqui está um fio de metal, com uma corrente passando por ele: a corrente do primeiro fio, que na tela aparece como I um. Repara que os traços verdes correm, mas o fio fica parado. |
| 0:09.4 | três anéis magenta em volta do fio | Essa corrente cria em volta do fio um campo magnético. As linhas desse campo são círculos concêntricos: elas não saem do fio, elas envolvem o fio. |
| 0:12.6 | caixa "I₁ → B₁" | Da corrente do primeiro fio nasce o campo magnético do primeiro fio. É essa passagem que a gente quer entender. |
| 0:20.0 | entra o segundo fio; B₁ tangente ao anel | Agora coloca um segundo fio, paralelo ao primeiro. Exatamente onde ele está, o campo do primeiro é tangente ao círculo, ou seja, perpendicular ao fio. |
| 0:25.7 | I₂, vetor comprimento, F₂; nome "Força magnética sobre um fio" | Pelo segundo fio também passa corrente, e o campo do primeiro empurra as cargas que se movem nele. A força sobre o segundo fio é a corrente dele, vezes o vetor comprimento do fio, vezes o campo magnético do primeiro, com um produto vetorial. Essa é a força magnética sobre um fio, que a gente já conhece. |
| 0:31.0 | caixa "B₁ = ?" | Só que falta uma peça: como calcular o campo magnético do primeiro fio? |
| 0:33.4 | "Falta a regra…"; título "LEI DE BIOT–SAVART" | Falta a regra que liga o campo à corrente que o produz. Essa regra é a lei de Biot–Savart. Hoje a gente a constrói passo a passo, a partir da geometria, e aplica em dois casos clássicos: o fio reto e a espira circular. |

*Por quê:* Ørsted (1820) mostrou que a corrente cria campo; Biot e Savart mediram o campo de um fio longo e Ampère estudou a força entre fios. Os círculos vêm da simetria do fio reto. O 5.1 explicou o efeito do campo (força de Lorentz); o 5.2 explica a causa.

## B01 — Regime magnetostático (0:46–1:35)

| Tempo | Na tela | Fala |
|---|---|---|
| 0:45.9 | título "Corrente estacionária: fluxo sem acúmulo" | Antes da lei, um aviso: ela vale para o regime magnetostático. Vamos ver o que isso quer dizer. |
| 0:49.6 | fio atravessando um volume V; barra de Q | Imagina um fio atravessando um volume imaginário. Se entra mais corrente do que sai, a carga dentro do volume cresce. |
| 0:54.6 | dQ/dt = I_entra − I_sai | Em fórmula: a taxa de variação da carga no tempo é a corrente que entra menos a corrente que sai. É só a conservação da carga. |
| 0:58.7 | as setas ficam iguais | Agora entra e sai a mesma corrente. |
| 1:04.4 | I_entra = I_sai ⟹ dQ/dt = 0 | Então a diferença é zero, e a carga dentro do volume não muda: a corrente atravessa o volume sem se acumular. |
| 1:13.5 | ∂ρ/∂t + ∇·J = 0; nome "Equação da continuidade" | A mesma ideia, ponto a ponto. Chamando de rô a densidade de carga, e de J a densidade de corrente, que é a corrente por área, a taxa de variação da densidade de carga mais o divergente da densidade de corrente é zero. Essa é a equação da continuidade: a carga se conserva. |
| 1:21.4 | ∂ρ/∂t = 0 ⟹ ∇·J = 0 | Se a densidade de carga não muda no tempo, sobra: o divergente da densidade de corrente é zero. Sem acúmulo de carga. |
| 1:28.2 | caixa ∂J/∂t = 0; "Corrente independente do tempo." | Mas Biot–Savart pede uma segunda condição, que é outra ideia: a própria corrente não pode mudar no tempo. As duas juntas definem a magnetostática. |

*Por quê:* duas hipóteses distintas, que não podem ser fundidas: (1) conservação da carga com densidade estacionária, logo divergente de J igual a zero, e as correntes formam circuitos fechados; (2) corrente estacionária, logo campo constante no tempo. Com corrente variável entra o campo elétrico variável (Maxwell).

## B02 — Geometria fonte–observador (1:35–2:29)

| Tempo | Na tela | Fala |
|---|---|---|
| 1:35.1 | título "Construir a separação fonte–observador" | Agora a geometria, que é onde mais gente se perde. Para somar o campo de cada pedacinho da corrente, a gente precisa saber onde está cada pedacinho e onde estamos observando. |
| 1:39.0 | ponto verde no fio | Cada pedaço do fio é uma fonte do campo. Esse ponto verde marca uma delas. |
| 1:42.3 | aparece P | Queremos o campo em um ponto qualquer do espaço: o ponto de observação, que na tela aparece como P. |
| 1:45.6 | aparece O | Para localizar os dois, escolhemos uma origem qualquer, o ponto O. A escolha é livre: o resultado final não depende dela. |
| 1:48.7 | setas até a fonte e até P | Um vetor localiza a fonte: é a posição da fonte, que a gente escreve como r com uma linha. Outro localiza o observador: é a posição do observador, r sem a linha. A linha marca a fonte. |
| 1:53.1 | aparece o vetor R | Repara que existem dois caminhos da origem até o observador: o direto, ou o que passa pela fonte. |
| 1:55.2 | r′ + R = r | O segundo trecho, da fonte até o observador, é o vetor separação, que na tela aparece como R em negrito. Os dois caminhos chegam no mesmo lugar: posição da fonte mais vetor separação é igual à posição do observador. |
| 1:59.9 | R = r − r′ | Isolando: o vetor separação é a posição do observador menos a posição da fonte. Ele aponta da fonte até o observador. Repara na ordem: observador menos fonte. |
| 2:07.9 | R = \|R\|; nota "distância fonte–observador" | O módulo desse vetor, escrito R sem negrito, é a distância entre a fonte e o observador. Mesma letra, duas coisas: uma é vetor, a outra é só comprimento. |
| 2:12.1 | P fixo; a fonte anda | Segura o observador e anda com a fonte: só o vetor separação muda. |
| 2:22.7 | dℓ e θ | Falta o elemento de fio: um pedacinho do fio, tangente a ele e orientado no sentido da corrente. E o ângulo teta é o ângulo entre esse elemento de fio e o vetor separação. |

*Por quê:* convenção de Griffiths e de Jackson (r′ fonte, r ponto de campo, separação igual a r menos r′). O elemento orientado no sentido da corrente convencional permite escrever a lei como produto vetorial.

## B03 — A lei de Biot–Savart (2:29–4:00)

| Tempo | Na tela | Fala |
|---|---|---|
| 2:28.9 | título "Biot–Savart: uma lei experimental" | Agora a lei. Ela é experimental: nasceu das medidas de Biot e Savart, em mil oitocentos e vinte, e Laplace deu a forma que a gente usa. Vamos montá-la fator por fator. |
| 2:33.3 | I e dℓ; ⊙ em P | Primeiro, o elemento de corrente: a corrente vezes o pedacinho de fio. Mais corrente, ou um pedaço maior, dá uma contribuição maior ao campo no ponto de observação. |
| 2:38.5 | P se afasta | Segundo, a distância: quanto mais longe, mais fraca. |
| 2:43.2 | dB ∝ I dℓ / R² | A medida mostra que a dependência é com o inverso do quadrado da distância. |
| 2:47.3 | R → 2R ⟹ dB → dB/4 | Se a distância dobra, a contribuição cai para um quarto. |
| 2:54.2 | θ varia de 22° a 90° | Terceiro, a direção: só a parte do elemento que é perpendicular à separação conta. |
| 2:59.5 | dB ∝ I dℓ sen θ / R² | Isso entra com o seno de teta: noventa graus, seno um, contribuição máxima; zero grau, seno zero, nenhuma contribuição. |
| 3:04.0 | μ₀/4π; nome "constante de proporcionalidade"; nota | Para virar igualdade, falta uma constante: no Sistema Internacional, mi zero dividido por quatro pi. O mi zero é a permeabilidade magnética do vácuo, e vale, aproximadamente, quatro pi vezes dez elevado a menos sete tesla metro por ampère. |
| 3:09.7 | dB = (μ₀/4π) I dℓ sen θ / R² | Então o módulo do campo infinitesimal é mi zero sobre quatro pi, vezes a corrente, vezes o comprimento, vezes o seno, dividido pela distância ao quadrado. |
| 3:15.7 | paralelogramo de dℓ e R̂ | Comprimento vezes seno é a área do paralelogramo formado pelo elemento de fio e pelo vetor unitário de separação, e isso é o módulo do produto vetorial entre os dois. |
| 3:25.5 | "O produto vetorial guarda o módulo e a direção" | O produto vetorial guarda também a direção, perpendicular aos dois. Por isso a lei fica melhor escrita com ele. |
| 3:26.2 | dB = (μ₀/4π) I dℓ × R̂ / R² | O campo infinitesimal, agora como vetor, é mi zero sobre quatro pi, vezes a corrente, vezes o produto vetorial do elemento de fio pelo vetor unitário de separação, dividido pela distância ao quadrado. |
| 3:33.0 | R̂ = R/R | O vetor unitário de separação é o vetor separação dividido pelo seu módulo: comprimento um, só a direção. |
| 3:37.5 | R/R dentro da lei | Substituindo na lei, aparece o vetor separação dividido pela distância. |
| 3:41.7 | o R desce | Esse módulo passa para baixo e fica multiplicando a distância ao quadrado. |
| 3:48.8 | R·R² vira R³ | Distância vezes distância ao quadrado dá distância ao cubo: os expoentes se somam. |
| 3:49.5 | lei completa; nome "Lei de Biot–Savart" | E chegamos: o campo infinitesimal é mi zero sobre quatro pi, vezes a corrente, vezes o produto vetorial do elemento de fio pelo vetor separação, dividido pela distância ao cubo. Essa é a lei de Biot–Savart: o campo de um único elemento de corrente. |

*Por quê:* a dependência com o seno e com o inverso do quadrado da distância, para o elemento, é a forma de Laplace, que reproduz a medida de Biot e Savart quando integrada. O elemento isolado não existe fisicamente (a corrente estacionária forma circuitos fechados): só a integral é medida. As formas com R̂ sobre R ao quadrado e com R sobre R ao cubo são equivalentes. O mi zero valia exatamente quatro pi vezes dez elevado a menos sete até a revisão do SI de 2019; hoje é medido e coincide em precisão muito alta, por isso "aproximadamente".

## B04 — Da linha à superfície e ao volume (4:00–5:19)

| Tempo | Na tela | Fala |
|---|---|---|
| 4:00.3 | título "Da linha à superfície e ao volume" | Até aqui a corrente estava num fio fino. Mas ela pode se espalhar numa superfície, ou ocupar um volume. A lei é a mesma; muda o que a gente chama de elemento de corrente. |
| 4:04.1 | I dℓ; integral | No fio fino, o campo total é a integral, ao longo do fio, do elemento de corrente vezes o vetor unitário de separação, dividido pela distância ao quadrado. |
| 4:15.7 | faixa de largura dw; dI = K dw | Numa lâmina, pega uma faixa estreita, de largura dw. A corrente nela é a corrente por unidade de largura, que na tela aparece como K, vezes a largura. |
| 4:26.9 | K = K t̂; nota "A/m" | Com a direção da corrente, K vira um vetor: a densidade superficial de corrente, em ampère por metro. |
| 4:34.7 | da = dw dℓ; dI dℓ = K da | A largura vezes o comprimento é o elemento de área. Então o elemento de corrente é K vezes o elemento de área. |
| 4:41.8 | B = (μ₀/4π) ∫ K × R̂ / R² da | A lei para a superfície é a mesma, com K e o elemento de área no lugar do elemento de corrente. |
| 4:51.1 | dI = J dA⊥ | Num volume, a corrente atravessa uma seção transversal: a densidade de corrente vezes a área da seção. |
| 4:55.0 | J = J t̂; nota "A/m²" | A densidade de corrente também é vetor, em ampère por metro quadrado: corrente por área. |
| 5:07.2 | dτ = dA⊥ dℓ; dI dℓ = J dτ | A seção vezes o comprimento é o elemento de volume. O elemento de corrente vira J vezes o elemento de volume. |
| 5:15.8 | "A medida de integração acompanha a distribuição" | Repara no padrão: comprimento no fio, área na superfície, volume no sólido. O resto da lei não muda. |

*Por quê:* as três formas são equivalentes: I dℓ numa linha, K vezes da numa superfície, J vezes dτ num volume. O fio fino é o limite de uma distribuição de volume com seção pequena.

## B05 — Isolar o efeito do ângulo (5:19–6:23)

| Tempo | Na tela | Fala |
|---|---|---|
| 5:19.5 | título "Isolar o efeito do ângulo" | Vamos olhar só o efeito do ângulo, com a distância fixa. |
| 5:22.8 | dB ∝ sen θ; gráfico | Com a distância fixa, o campo infinitesimal é proporcional ao seno de teta. O ponto branco no gráfico acompanha o ângulo. |
| 5:29.9 | θ = 0; "dB = 0 neste elemento" | Com teta igual a zero, o elemento aponta direto para o ponto, e a contribuição desse elemento é zero, embora a corrente continue circulando. Repara no que é zero: só a contribuição deste elemento, não o campo total. |
| 5:36.7 | θ = 30°, 60° | Trinta graus, e a contribuição cresce; sessenta, e já está perto do máximo. |
| 5:48.5 | θ = 90° | Noventa graus: contribuição máxima para essa distância. |
| 5:54.4 | θ = 150°, 180° | Cento e cinquenta graus, ela volta a enfraquecer; com cento e oitenta, o elemento aponta para o lado oposto e a contribuição volta a ser zero. |
| 6:05.3 | "O produto vetorial dá também a direção"; vista 3D | Mas o produto vetorial também dá a direção, e para ver isso a gente muda para uma perspectiva em três dimensões. |
| 6:10.3 | regra da mão direita | Regra da mão direita: os dedos vão do elemento de fio para o vetor separação, e o polegar mostra o sentido do campo infinitesimal. |
| 6:17.8 | dℓ × R = −R × dℓ; a seta inverte | O produto vetorial é anticomutativo: trocar a ordem inverte o campo. Por isso a ordem importa: primeiro o elemento de fio, depois a separação. |

*Por quê:* o módulo do produto vetorial é dℓ R sen θ e o campo é perpendicular ao elemento e à separação. Se elemento e separação são paralelos, o produto é nulo: vale para a contribuição de um elemento, não para o campo total.

## B06 — Superposição: construir uma soma vetorial (6:23–7:04)

| Tempo | Na tela | Fala |
|---|---|---|
| 6:22.7 | título "Construir uma soma vetorial" | Como passar da contribuição de um elemento ao campo da corrente inteira? Pelo princípio da superposição. |
| 6:25.7 | cinco elementos, um de cada vez | Fixa um observador. Cada elemento dá uma contribuição, com direção e tamanho próprios. Pega cinco elementos e calcula cada uma. |
| 6:40.6 | resultante; B ≈ ΔB₁ + … + ΔB₅ | São vetores, então a soma é ponta com cauda. A resultante liga o início da primeira ao fim da última: é, aproximadamente, o campo total. |
| 6:48.3 | muitos elementos; B ≈ Σ ΔB_i | Com mais elementos, cada contribuição é menor e a aproximação melhora: o campo é a soma, de um até N, das contribuições. |
| 6:55.7 | B = ∫ dB | No limite em que cada pedaço tem comprimento zero e o número de pedaços vai ao infinito, a soma vira integral. |

*Por quê:* a lei é linear na corrente, então vale a superposição. A integral é vetorial, componente a componente.

## B07 — Aplicar o método (7:04–7:29)

| Tempo | Na tela | Fala |
|---|---|---|
| 7:03.7 | título "Aplicar o método ao desenho"; lista de quatro passos | O método tem quatro passos. Primeiro: quem produz o campo, e onde a gente calcula? A geometria dá o vetor separação, posição do observador menos posição da fonte. |
| 7:15.5 | "2 direção de dB"; ⊙ | Segundo: a direção. Pela regra da mão direita, aqui todas as contribuições apontam para fora da tela. |
| 7:18.6 | dℓ = dx x̂ | Terceiro: o elemento de fio e a variável. Percorrer o fio é percorrer a posição x: o elemento é dx, no sentido do eixo x. |
| 7:22.7 | B_trecho = ∫ dB | Quarto: os limites e a integral, entre as duas extremidades do trecho. |

## B08 — Trecho retilíneo finito (7:29–10:32)

### B08.1 — Geometria e produto vetorial (7:29–8:33)

| Tempo | Na tela | Fala |
|---|---|---|
| 7:28.7 | título "Contribuição de um trecho retilíneo do circuito" | Vamos aplicar tudo isso a um pedaço reto de fio. |
| 7:34.0 | trecho dentro de um circuito | Esse pedaço é só parte de um circuito: o campo total é a soma vetorial do campo do trecho com o do resto do circuito. Por enquanto, calculamos só o trecho. |
| 7:43.9 | dℓ = dx x̂ | O elemento de fio tem comprimento dx e aponta ao longo do fio, no sentido do eixo x. |
| 7:46.8 | descrições de x e a | Chama de x a posição do elemento ao longo do fio, medida a partir do pé da perpendicular, e de a a distância perpendicular do ponto ao fio. |
| 7:48.7 | R = −x x̂ + a ŷ | Então o vetor separação tem uma parte paralela ao fio, menos x vezes o vetor unitário do eixo x, e uma parte perpendicular, a vezes o vetor unitário do eixo y. |
| 7:53.1 | dℓ × R = dx x̂ × (−x x̂ + a ŷ) | Agora o produto vetorial do elemento de fio pelo vetor separação, que é o que a lei pede. |
| 7:57.7 | produto distribuído | Distribuindo, ele se divide em dois pedaços, um para cada parte do vetor separação. |
| 8:03.0 | parte paralela; x̂ × x̂ = 0 | Na parte paralela, o produto vetorial de um vetor com ele mesmo é zero: o elemento e essa parte apontam na mesma direção, então o seno do ângulo é zero. |
| 8:04.7 | parte perpendicular; x̂ × ŷ = ẑ | Na parte perpendicular, x chapéu vezes y chapéu dá z chapéu, pela regra da mão direita dos eixos. O termo paralelo some, multiplicado por zero. |
| 8:11.4 | a vista gira; ⊙ vira o eixo z | Sobra só a parte perpendicular: a vezes dx, na direção z. Na vista em três dimensões, o ponto no círculo vira o próprio eixo z, saindo da tela. |
| 8:19.2 | "Substitua na lei"; nome | Levando isso para a lei de Biot–Savart: |
| 8:22.8 | dB = (μ₀ I/4π) a dx / R³ ẑ | o campo infinitesimal é mi zero vezes a corrente, sobre quatro pi, vezes a vezes dx, dividido pela distância ao cubo, na direção z. |

*Por quê:* a escolha de x ao longo do fio e de a na perpendicular reduz o vetor separação a duas componentes. O produto paralelo nulo mostra, na forma vetorial, por que só a componente perpendicular importa.

### B08.2 — Pitágoras e substituição angular (8:33–10:00)

| Tempo | Na tela | Fala |
|---|---|---|
| 8:32.2 | triângulo (a, x, R); nome "Teorema de Pitágoras" | Só que a distância R muda quando o elemento anda. Pelo teorema de Pitágoras, no triângulo retângulo: R ao quadrado é x ao quadrado mais a ao quadrado. |
| 8:43.6 | "Mova o elemento" | Quando o elemento anda, o módulo muda, mas o sentido não: continua para fora da tela. |
| 8:56.7 | "θ e α são ângulos diferentes" | Atenção: aqui há dois ângulos. O teta é o da lei, entre o elemento e a separação. O alfa é outro: entre a perpendicular até o fio e o vetor separação. |
| 9:02.8 | tan α = x/a | A integral em x é difícil, então trocamos de variável. No triângulo, a tangente de alfa é x dividido por a. |
| 9:06.1 | x = a tan α | Logo, x é a vezes a tangente de alfa. |
| 9:10.1 | dx = a sec²α dα | Derivando: dx é a vezes a secante ao quadrado de alfa, vezes d alfa, porque a derivada da tangente é a secante ao quadrado. |
| 9:20.4 | "Reescreva o denominador" | Falta o denominador: x ao quadrado mais a ao quadrado. |
| 9:21.1 | x² + a² = a² tan²α + a² | Trocando x, fica a ao quadrado vezes tangente ao quadrado, mais a ao quadrado. |
| 9:24.1 | a²(1 + tan²α) = a² sec²α | Pondo a ao quadrado em evidência, aparece um mais tangente ao quadrado, que pela identidade trigonométrica é a secante ao quadrado. |
| 9:29.8 | (x²+a²)^{3/2} = a³ sec³α | Elevando a três meios: a ao cubo vezes secante ao cubo. |
| 9:34.6 | substituição no denominador | Agora o denominador inteiro está em função de alfa. |
| 9:39.1 | "Junte os a do numerador" | Simplificando: juntamos os dois a do numerador. |
| 9:43.1 | a²/a³ = 1/a | A ao quadrado sobre a ao cubo é um sobre a. |
| 9:47.0 | sec²α/sec³α = 1/sec α = cos α | Secante ao quadrado sobre secante ao cubo é um sobre a secante, e um sobre a secante é o cosseno de alfa. |
| 9:54.8 | dB = (μ₀ I / 4π a) cos α dα ẑ | O campo infinitesimal é mi zero vezes a corrente, sobre quatro pi a, vezes cosseno de alfa d alfa, na direção z. Repara que a distância R desapareceu: só ficou o ângulo. |

*Por quê:* x igual a a tangente de alfa torna o denominador um cubo de secante e cancela a secante ao quadrado de dx: esse é o motivo da substituição, não só um truque.

### B08.3 — Limites e resultado (10:00–10:32)

| Tempo | Na tela | Fala |
|---|---|---|
| 10:02.9 | extremidades; α_A e α_B | Os limites são os ângulos nas duas extremidades: o da esquerda é negativo, o da direita é positivo. |
| 10:07.0 | ∫ cos α dα ; [sen α] | O campo do trecho é mi zero vezes a corrente, sobre quatro pi a, vezes a integral do cosseno de alfa. A primitiva do cosseno é o seno. |
| 10:14.7 | sen α_B − sen α_A | Aplicando os limites: seno de alfa B menos seno de alfa A. |
| 10:18.2 | α_A = −α₁ ; α_B = α₂ | Chamando de alfa um o oposto de alfa A, que é positivo, a diferença de senos vira soma. |
| 10:22.3 | B_trecho = (μ₀ I / 4π a)(sen α₁ + sen α₂) | O resultado: o campo do trecho é mi zero vezes a corrente, sobre quatro pi a, vezes seno de alfa um mais seno de alfa dois. |

*Por quê:* resultado clássico do segmento reto (Griffiths, Exemplo 5.5). Vale para o trecho; o campo total soma todos os trechos do circuito fechado.

## B09 — O fio infinito como limite (10:32–11:04)

| Tempo | Na tela | Fala |
|---|---|---|
| 10:31.9 | título "O fio infinito como limite" | Agora um caso-limite: e se o fio for muito comprido? |
| 10:37.3 | os ângulos crescem | Conforme o fio cresce, alfa um e alfa dois se aproximam de noventa graus, e os dois senos tendem a um. |
| 10:49.8 | B_∞ = (μ₀ I/4π a)(1 + 1) | Colocando na fórmula, fica mi zero vezes a corrente, sobre quatro pi a, vezes um mais um. |
| 10:53.8 | B_∞ = μ₀ I / 2π a; nome | Ou seja, mi zero vezes a corrente, sobre dois pi vezes a distância. Esse é o campo de um fio retilíneo infinito. |
| 10:58.5 | "B ∝ 1/a" | O campo cai com o inverso da distância ao fio, e o fio infinito nasceu como o limite do trecho finito. |

*Por quê:* idealização boa quando o ponto está perto do fio comparado ao comprimento e longe das pontas. Concorda com a medida original de Biot e Savart.

## B10 — A força entre dois fios (11:04–11:49)

| Tempo | Na tela | Fala |
|---|---|---|
| 11:03.6 | título "A corrente cria o campo que produz a força" | Com esse campo, a gente fecha o que abriu no começo: a força entre dois fios. |
| 11:11.5 | ⊗ à direita, ⊙ à esquerda | O primeiro fio carrega corrente para cima. Pela regra da mão direita, à direita dele o campo entra na tela, o xis no círculo, e à esquerda sai, o ponto no círculo. Os símbolos mostram só o sentido, não o tamanho. |
| 11:15.2 | B₁ = μ₀ I₁ / 2π d | O campo do primeiro fio, na posição do segundo, é mi zero vezes a corrente do primeiro fio, sobre dois pi vezes a distância entre os fios. A intensidade está na fórmula: cai com um sobre a distância. |
| 11:22.4 | segundo fio, L, F₂ | A força sobre o segundo fio é a corrente dele, vezes o vetor comprimento, vezes o campo do primeiro, e aponta para o primeiro fio. |
| 11:30.8 | F₂/L = μ₀ I₁ I₂ / 2π d | Dividindo pelo comprimento, a força por unidade de comprimento é mi zero vezes as duas correntes, sobre dois pi vezes a distância. A unidade é newton por metro. |
| 11:36.0 | "os fios se atraem" | Correntes no mesmo sentido: os fios se atraem. |
| 11:40.7 | I₂ inverte | Inverte a corrente do segundo: o campo do primeiro não muda, mas a força inverte, e os fios se repelem. |

*Por quê:* observação de Ampère (1820). Até 2019 o ampère era definido por essa força: dois fios longos a um metro, com um ampère cada, se atraem com dois vezes dez elevado a menos sete newtons por metro. Pela terceira lei de Newton, o segundo fio puxa o primeiro com força igual e oposta.

## B11 — A espira circular no eixo (11:49–15:26)

### B11.1 — Duas vistas e o triângulo (11:49–12:40)

| Tempo | Na tela | Fala |
|---|---|---|
| 11:48.5 | título "Uma espira, duas vistas da mesma geometria" | Segundo caso: a espira circular. Queremos o campo magnético sobre o eixo dela. |
| 11:58 | legenda "Na espira, a notação muda" | Atenção: a notação muda. Na espira, R passa a ser o raio da espira. A separação entre o elemento e o ponto de observação passa a se chamar s. E z é a posição ao longo do eixo. |
| 12:01.6 | dℓ = R dφ | Um pedaço pequeno da espira corresponde a um ângulo pequeno, d fi. O comprimento desse arco é o raio vezes o ângulo, em radianos. |
| 12:09.9 | a espira gira de 0° a 90° | Giramos a espira de zero a noventa graus. De perfil, ela vira uma linha, e o eixo aparece, com o ponto de observação sobre ele. |
| 12:23.2 | zoom no triângulo (R, z, s) | Agora o triângulo: o raio da espira, a posição do ponto no eixo, e a separação, que liga o elemento ao ponto. |
| 12:27.0 | s² = R² + z²; nome "Teorema de Pitágoras" | É um triângulo retângulo. Pelo teorema de Pitágoras: a separação ao quadrado é o raio ao quadrado mais a posição no eixo ao quadrado. |

### B11.2 — Módulo, direção e projeção axial (12:36–13:27)

| Tempo | Na tela | Fala |
|---|---|---|
| 12:36.7 | θ = 90° | O elemento sai da tela e a separação está no plano da tela, então o ângulo entre eles é noventa graus, e o seno vale um. |
| 12:47.7 | dB = (μ₀/4π) I dℓ / s² | Biot–Savart fica: mi zero sobre quatro pi, vezes a corrente vezes o elemento, dividido pela separação ao quadrado. Aqui é a separação, não o raio. |
| 12:52.8 | seta de dB inclinada | Pela regra da mão direita, o campo infinitesimal é perpendicular à separação e ao elemento, por isso aponta inclinado. |
| 12:57.8 | "Projete no eixo"; dB_z = dB cos γ | Sobre o eixo, importa a componente ao longo do eixo: o campo infinitesimal vezes o cosseno do ângulo gama. |
| 13:03.5 | arcos de γ | Os dois ângulos gama são iguais, porque os lados são perpendiculares dois a dois. |
| 13:08.2 | cos γ = R/s | O triângulo dá o cosseno: cateto adjacente, que é o raio, sobre a hipotenusa, que é a separação. |
| 13:12.3 | dB_z = dB R/s | Então a parte axial é o campo infinitesimal vezes o raio sobre a separação. |

### B11.3 — Par oposto e cancelamento (13:27–13:55)

| Tempo | Na tela | Fala |
|---|---|---|
| 13:26.6 | elemento oposto | Agora o elemento diametralmente oposto, com a mesma distância até o ponto. |
| 13:30.8 | "As transversais cancelam" | As partes transversais têm o mesmo tamanho e sentidos opostos: postas uma depois da outra, voltam ao ponto de partida. Elas se cancelam. |
| 13:40.6 | "As axiais se somam" | As partes axiais têm o mesmo sentido, e se somam. |
| 13:46.4 | "Integre UMA contribuição" | Atenção: esse par serviu só para provar a simetria. Na integral, cada elemento entra uma vez só, senão o fator dois seria contado a mais. |

*Por quê:* a simetria em torno do eixo cancela as componentes transversais de elementos opostos; só a axial sobrevive.

### B11.4 — Álgebra do integrando (13:54–14:37)

| Tempo | Na tela | Fala |
|---|---|---|
| 13:54.0 | título "Do triângulo ao integrando axial" | Hora de montar o integrando. Partimos da lei no módulo. |
| 14:00.2 | dB_z = (μ₀/4π)(I dℓ / s²)(R/s) | A parte axial é mi zero sobre quatro pi, vezes a corrente vezes o elemento, sobre a separação ao quadrado, e tudo vezes o raio sobre a separação. |
| 14:08.5 | dℓ = R dφ; "Troque dℓ pelo arco" | Lembra do arco? O elemento é o raio vezes d fi. Trocamos. |
| 14:14.4 | R · R, s² · s | Agora o raio aparece duas vezes no numerador, e a separação aparece como ao quadrado e como separação simples no denominador. Agrupando: raio vezes raio, e separação ao quadrado vezes separação. |
| 14:20.3 | R², s³ | Raio vezes raio é raio ao quadrado. Separação ao quadrado vezes separação é separação ao cubo. |
| 14:24.6 | s³ = (R² + z²)^{3/2} | E a separação ao cubo, por Pitágoras, é raio ao quadrado mais posição no eixo ao quadrado, elevado a três meios. |
| 14:29.9 | dB_z = (μ₀/4π) I R² / (R²+z²)^{3/2} dφ | A parte axial de um elemento é mi zero sobre quatro pi, vezes a corrente vezes o raio ao quadrado, dividido por raio ao quadrado mais posição ao quadrado, elevado a três meios, vezes d fi. |

### B11.5 — Integral da volta e resultado (14:38–15:26)

| Tempo | Na tela | Fala |
|---|---|---|
| 14:38.8 | "Integre uma volta: só φ varia" | Agora uma volta inteira. O raio, a posição no eixo, a separação e a corrente não mudam. Só o ângulo de posição varia, de zero a dois pi. |
| 14:47.5 | seta B_z sobre o eixo | Somando todas as contribuições, a gente tem o campo total. A seta inclinada de um elemento sai, e fica só a seta axial: o campo sobre o eixo. |
| 14:53.3 | constantes saem da integral | Tudo o que não depende do ângulo sai da integral, e sobra só a integral de d fi, de zero a dois pi, que vale dois pi. |
| 15:06.4 | 2π/4π = 1/2 | Dois pi dividido pelo quatro pi da lei dá um meio. |
| 15:13.8 | B_z(z) = μ₀ I R² / 2(R²+z²)^{3/2} | E esse um meio vira o dois no denominador: o campo sobre o eixo é mi zero vezes a corrente vezes o raio ao quadrado, dividido por dois vezes raio ao quadrado mais posição ao quadrado, elevado a três meios. |
| 15:19.5 | nome "Campo no eixo de uma espira" | Esse é o campo no eixo de uma espira de corrente. |

*Por quê:* resultado clássico (Griffiths, Exemplo 5.6). A seta total sobre o eixo fecha a ideia: transversais cancelaram, axiais somaram. Duas fusões merecem etapa própria: raio vezes raio, e dois pi sobre quatro pi.

## B12 — Duas checagens (15:26–16:28)

| Tempo | Na tela | Fala |
|---|---|---|
| 15:26.5 | título "Checagem 1: o centro da espira" | Toda fórmula precisa de testes. Primeiro, o centro da espira. |
| 15:33.2 | B(0) = μ₀ I R² / 2R³ | Com a posição no eixo igual a zero, o denominador vira raio ao cubo. |
| 15:38.3 | B(0) = μ₀ I / 2R | Simplificando: mi zero vezes a corrente, sobre dois vezes o raio. |
| 15:42.4 | "No centro não há componente lateral" | No centro, a separação é igual ao raio e cada contribuição já aponta ao longo do eixo: não sobra componente lateral para cancelar. |
| 15:50.7 | título "Checagem 2: muito longe da espira" | Segundo teste: muito longe da espira. |
| 16:07.8 | "\|z\| ≫ R" | Quando a posição no eixo é muito maior que o raio, a distância domina o denominador. |
| 16:08.5 | (R²+z²)^{3/2} ≈ \|z\|³ | Pondo z ao cubo em evidência, sobra um mais raio ao quadrado sobre z ao quadrado, e essa fração tende a zero. O denominador é, aproximadamente, o módulo de z ao cubo. |
| 16:17.2 | B_z ∼ μ₀ I R² / 2\|z\|³ | Então o campo cai com um sobre z ao cubo, bem mais rápido que o um sobre a distância do fio. |
| 16:22.7 | fio: B ∝ a⁻¹ ; espira: B ∝ \|z\|⁻³ | Fio: proporcional a um sobre a. Espira, longe: proporcional a um sobre z ao cubo. |

*Por quê:* no centro, o resultado conhecido é mi zero vezes a corrente sobre dois raios. Longe, a espira se comporta como um dipolo magnético, cujo campo cai com o cubo da distância. Frase opcional: "É o comportamento típico de um dipolo magnético."

## B13 — Uma lei, geometrias diferentes (16:28–17:11)

| Tempo | Na tela | Fala |
|---|---|---|
| 16:28.2 | título "Uma lei; geometrias diferentes" | Amarrando tudo: a fonte e o observador constroem o vetor separação, e a lei de Biot–Savart dá a contribuição de cada elemento. |
| 16:41.2 | B = ∫ dB | Somar essas contribuições recupera o campo da fonte inteira. |
| 16:56.9 | o fio vira espira; legenda | A mesma lei, com outra fonte: no fio, o campo cai com um sobre a distância; na espira, longe, com um sobre z ao cubo. |

## B14 — Pergunta final e CTA (17:11–17:38)

| Tempo | Na tela | Fala |
|---|---|---|
| 17:10.8 | título "Que estrutura o campo magnético possui?"; círculos | Mas ainda falta algo. Olha as linhas do campo em volta da corrente: elas fecham sobre si mesmas. |
| 17:12 | "O que revela o divergente?" ; "E o rotacional? E Ampère?" | O que o divergente do campo magnético revela? E o rotacional? E o que a lei de Ampère tem a ver com isso? |
| 17:18.5 | "Que propriedades esse campo necessariamente possui?" | Que propriedades esse campo necessariamente possui? Essa é a pergunta do próximo vídeo. |
| 17:24 | CTA Parallax Lab | Se você gostou, se inscreve no canal para acompanhar os próximos. Valeu, pessoal, e até a próxima! |

---

## Decisões abertas para fechar com o GPT

1. **Abertura:** "Fala, pessoal!" como nos longos anteriores, ou entrada mais seca.
2. **Valor do mi zero:** falar "aproximadamente quatro pi vezes dez elevado a menos sete tesla metro por ampère" (proposto) ou omitir o número.
3. **Dipolo (B12):** manter a frase opcional ou deixar para o vídeo seguinte.
4. **Definição do ampère (B10):** a nota histórica do SI pré-2019 fica na fala ou só na descrição do vídeo.
5. **Aviso da notação da espira (11:58):** a legenda dura poucos segundos; a fala precisa acompanhar esse momento.
6. **Teaser:** "divergente, rotacional e a lei de Ampère" foi escolha minha a partir do gancho da tela; confirmar com o mapa curricular.
7. **O que a v1.1 cortou em relação à v1:** leitura quase literal de cada linha de álgebra (B08.2, B11.4), aberturas repetidas de cada passo do B05, a síntese em seis falas (B13 virou três) e algumas retomadas. A matemática, as definições de variáveis, o aviso da troca de notação, o "Por quê" científico e todas as âncoras de tempo foram mantidos.

## Estimativa de duração e folga da animação

Contagem automática: palavras da coluna Fala, a 2,8 palavras por segundo; a janela de cada linha vai do seu início até o início da linha seguinte.

| Bloco | Janela no vídeo | Palavras | Voz (2,8 p/s) | Folga extra necessária |
|---|---|---|---|---|
| B00 | 0:00.0–0:45.9 | 260 | 1:32.9 | +0:47.2 |
| B01 | 0:45.9–1:35.1 | 191 | 1:08.2 | +0:23.8 |
| B02 | 1:35.1–2:28.9 | 283 | 1:41.1 | +0:53.2 |
| B03 | 2:28.9–4:00.3 | 369 | 2:11.8 | +0:49.3 |
| B04 | 4:00.3–5:19.5 | 222 | 1:19.3 | +0:14.0 |
| B05 | 5:19.5–6:22.7 | 185 | 1:06.1 | +0:15.0 |
| B06 | 6:22.7–7:03.7 | 104 | 0:37.1 | +0:04.4 |
| B07 | 7:03.7–7:28.7 | 82 | 0:29.3 | +0:07.8 |
| B08 | 7:28.7–10:31.9 | 632 | 3:45.7 | +1:01.7 |
| B09 | 10:31.9–11:03.6 | 91 | 0:32.5 | +0:07.6 |
| B10 | 11:03.6–11:48.5 | 176 | 1:02.9 | +0:22.6 |
| B11 | 11:48.5–15:26.5 | 650 | 3:52.1 | +0:53.6 |
| B12 | 15:26.5–16:28.2 | 148 | 0:52.9 | +0:09.7 |
| B13 | 16:28.2–17:10.8 | 56 | 0:20.0 | +0:00.0 |
| B14 | 17:10.8–17:38.0 | 71 | 0:25.4 | +0:06.9 |
| **Total** | 0:00.0–17:38.0 | **3520** | **20:57.1** | **+6:17.1** |

Leitura: voz de cerca de 20:57.1 contra 17:38 de animação; o vídeo final deve ficar em torno de 23:55.1 depois do remapeamento por âncoras (a animação segura pausas nos trechos de maior folga).
