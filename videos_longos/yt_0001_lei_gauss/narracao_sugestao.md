# yt_0001 — sugestão de narração

Status: **NARRAÇÃO MASTER APROVADA PARA GERAÇÃO DE VOZ** (texto do TTS: `texto_narracao.txt`). Histórico: Master congelada para teste de voz (5 patches + 3 microajustes da 1ª revisão; congelamento da 2ª revisão: dΩ em módulo, abertura angular, soma orientada, contribuição orientada na carga externa, q > 0, condutores cortado, intro encurtada). Próximo passo: teste de pronúncia; depois seção 12 da ficha + remapeamento, sem aumentar os 16:41.

LEI DE GAUSS: O SEGREDO NÃO É A INTEGRAL — É A SIMETRIA. Preview V2.1 silencioso de 16:41.
Tom dos curtos, adaptado ao longo: frases curtas, conectivos ("agora", "então", "só que", "por isso", "repara",
"cuidado"), uma ideia por frase, grandezas por extenso e proximidade ("a gente", "pega", "olha").
Princípio: **a voz explica o porquê e desenrosca o que pode confundir na tela; o Manim mostra o como.**
A voz não lê a lousa: cancelamentos, primitivas e substituições longas ficam na animação.

Arquitetura mantida (ficha, seção 9): cold open → intro "Fala, pessoal" → aula → payoff → pausa → CTA.
A saudação vem **depois** do cold open, porque a ficha proíbe abrir com ela. Se a Produção preferir abrir já com
"Fala, pessoal", basta trocar a ordem dos blocos 1 e 2 (o cold open vira o "nesse vídeo…").

## Como falar as grandezas

| Na tela | Na fala |
|---|---|
| E⃗, E, E(r) | **o campo** (o "E" só quando a fala é a fórmula: "tirar o E da integral") |
| dA | **d A**, "um pedacinho de área" |
| n̂ | **a normal**, "n chapéu" na 1ª vez |
| d⃗A | **o vetor área** |
| θ (âmbar) | **teta** (no texto do TTS: **téta**; teste de pronúncia aprovado) — sempre "o ângulo entre o campo e a normal" |
| ϑ | **ângulo polar**, "outra grafia de teta" na 1ª vez; depois "d teta" |
| φ | **fi**, "ângulo azimutal" |
| dA⊥ | **área projetada** ("d A perpendicular" só se precisar nomear) |
| dΩ, dΩ_or | **d ômega**, **d ômega orientado**; na carga externa, "contribuição orientada" (nunca "menos d ômega" solto) |
| sr | **esterradianos** |
| ε₀ | **épsilon zero** |
| Q_env | **a carga envolvida** |
| ρ, ρ(r) | **a densidade**, "rô de r" |
| R, r, r′ | só no trecho da legenda e no elemento de volume, onde a tela aponta as letras; no resto, **o raio da esfera**, **o raio da gaussiana / a distância ao centro**, **dentro / fora da esfera** |
| 1/r², r² | "um sobre o raio ao quadrado", "o raio ao quadrado" |

Evitar: dizer que o sinal do d ômega orientado vem do campo (vem de r̂·n̂; "sai/entra" vale para a carga positiva desenhada); dizer que a simetria esférica exige fonte infinita (só linha e plano são idealizações infinitas); "o campo passa pela superfície" no sentido de contar linhas (o fluxo é uma soma); dizer que a gaussiana
"cria" simetria; chamar o d ômega orientado de "tamanho aparente" (o tamanho é o d ômega, sempre positivo).

## Narração por blocos de tempo

Tempos = instantes em que cada beat começa no preview V2.1 (calculados pela própria cena, precisão de ±1–2 s).
Cada linha é um trecho de fala que deve cair sobre aquele trecho de tela; a voz real depois ajusta a cena pelas
âncoras (lista no fim). `[...]` = cortável. Onde o trecho ficou apertado, a fala foi enxugada para ≤ ~2,8 palavras/s.

### 1. Cold open (0:00–0:33)

| Tempo | Na tela | Fala |
|---|---|---|
| 0:00–0:08 | dois problemas; superfícies; a mesma Lei de Gauss escrita nos dois | Olha esses dois problemas. Nos dois, dá pra desenhar uma superfície fechada e escrever exatamente a mesma Lei de Gauss. |
| 0:08–0:15 | esquerda: setas radiais; E·4πr² → E = Q/(4πε₀r²) | No primeiro, a distribuição de carga é esfericamente simétrica, e em dois passos o campo aparece. |
| 0:15–0:24 | direita: a carga sai do centro; destaque na lei e no fluxo | No segundo, eu só tiro a carga do centro da esfera. A lei continua verdadeira. O fluxo continua determinado. |
| 0:24–0:33 | "E⃗ = ?"; "Então o que mudou?" | E mesmo assim, eu não consigo tirar o campo daí. Então, o que mudou? *(pausa)* |

### 2. Intro (0:33–0:57)

| Tempo | Na tela | Fala |
|---|---|---|
| 0:33–0:44 | PARALLAX LAB · LEI DE GAUSS; depois os dois casos voltam e piscam | Fala, pessoal! Bem-vindos ao Parallax Lab. Hoje a gente vai entender por que a Lei de Gauss resolve alguns problemas quase de graça e, em outros, parece não ajudar. |
| 0:44–0:57 | "fonte → campo → superfície" acende palavra a palavra; a superfície da esquerda vira a da próxima cena | Spoiler: a chave é a simetria. E a ordem importa: primeiro a fonte, depois o campo, e só então a superfície. Pular essa ordem é o que faz muita gente decorar esfera e cilindro sem entender por quê. |

### 3. Fluxo e vetor área (0:57–2:41)

| Tempo | Na tela | Fala |
|---|---|---|
| 0:57–1:09 | superfície fechada → o pedaço dA amplia; "dA: área do elemento (um número)" | Antes de responder, a gente precisa entender o que a Lei de Gauss mede. Pega um pedacinho bem pequeno de uma superfície. A área dele é só um número: o elemento de área. |
| 1:09–1:15 | plano tangente tracejado | De tão pequeno, ele praticamente coincide com o plano tangente. |
| 1:15–1:21 | n̂ azul, curto, com marca de 90°; "\|n̂\| = 1" | Agora, a normal: a setinha azul, n chapéu. Perpendicular ao plano, comprimento um: só direção. |
| 1:21–1:31 | d⃗A violeta, grosso; "d⃗A = n̂ dA"; o pedaço encolhe e volta | Normal vezes área dá o vetor área, a seta violeta. Repara: quando o pedaço encolhe, ela encolhe junto; a normal não. |
| 1:31–1:39 | superfície fechada com normais para fora; "normal exterior" | Numa superfície fechada, cada ponto tem a sua normal, e a convenção é sempre apontar para fora. |
| 1:39–1:53 | campo uniforme (ciano); pedaço inclina; beat do 90° (âmbar, fraco) → beat do θ (âmbar, forte); dΦ = E dA cosθ | Agora coloca esse pedaço num campo elétrico. Repara que aparecem dois ângulos. O de noventa graus, entre a normal e o plano, não entra na conta. O que importa é o teta, em amarelo: entre o campo e a normal. |
| 1:53–1:59 | θ → 0°; cos θ = 1; barra máxima | De frente, o fluxo é máximo. |
| 1:59–2:05 | θ → 40°; n̂ e d⃗A giram com o pedaço | Inclinando, ele diminui, e a normal e o vetor área giram junto. |
| 2:05–2:12 | θ → 90°; barra zera | Quando o campo passa tangente, raspando, o fluxo é zero. |
| 2:12–2:20 | superfície fechada ao fundo; θ → 150°; dΦ < 0 | E se o campo entra numa superfície fechada, contra a normal, a contribuição fica negativa. |
| 2:20–2:28 | destaque na equação; normais em toda a superfície; Φ = ∮E⃗·d⃗A | É isso que o produto escalar faz. E a integral fechada só repete essa soma pela superfície inteira. |
| 2:28–2:41 | setas viram linhas de campo e esmaecem; normais piscam; caixa | [Dica: o fluxo não conta linhas de campo. As linhas são só um desenho; o fluxo é a soma de quanto campo atravessa cada pedacinho.] |

### 4. Coulomb e esfera (2:41–3:45)

| Tempo | Na tela | Fala |
|---|---|---|
| 2:41–2:52 | esfera com a carga no centro; E⃗ = q/(4πε₀r²) r̂; setas radiais | Agora coloca uma carga pontual positiva no centro de uma esfera. Pela Lei de Coulomb, o campo aponta para fora e cai com o quadrado da distância. |
| 2:52–2:57 | normais; "E⃗ ∥ d⃗A"; ∮E⃗·d⃗A → ∮E dA | Na esfera, campo e vetor área ficam paralelos. |
| 2:57–3:06 | o raio gira; rótulos E nos três pontos | E como todo ponto está à mesma distância da carga, o módulo do campo é o mesmo na superfície inteira. |
| 3:06–3:13 | E sai da integral; os arcos somam → E·4πr² | Então dá pra tirar o campo da integral, e o fluxo vira o campo vezes a área da esfera. |
| 3:13–3:28 | barras 1/r², r² e Φ; o raio cresce; Φ = q/(4πε₀r²)·4πr² com cortes | Agora olha as barras quando o raio aumenta: o campo cai com um sobre o raio ao quadrado, mas a área cresce com o raio ao quadrado. Uma coisa compensa exatamente a outra. |
| 3:28–3:45 | Φ = q/ε₀ em caixa; o raio varia e o fluxo fica parado | Por isso, qualquer esfera centrada na carga dá o mesmo fluxo: a carga sobre épsilon zero. Ou seja, o fluxo mede algo mais profundo do que o campo num ponto. |

### 5. Ângulo sólido e Lei de Gauss (3:45–6:17)

| Tempo | Na tela | Fala |
|---|---|---|
| 3:45–3:52 | a esfera vira uma superfície qualquer; cone saindo da carga | Mas e se a superfície não for uma esfera? Imagina um cone bem estreito de direções saindo da carga. |
| 3:52–3:56 | pedaço violeta cortado pelo cone | Ele corta um pedaço de uma superfície qualquer. |
| 3:56–4:01 | "ÂNGULO SÓLIDO dΩ" + rótulo dΩ no cone (âmbar) | Aqui entra uma ideia nova: o ângulo sólido, o d ômega. |
| 4:01–4:09 | no plano: dθ = ds/r; "volta completa: 2π rad" | No plano, um ângulo pequeno é o arco dividido pelo raio, e a volta inteira vale dois pi radianos. |
| 4:09–4:18 | no espaço: cone 3D com dA⊥; dΩ = dA⊥/r²; "4π sr"; "sr = esterradiano" | No espaço, é a mesma ideia com uma dimensão a mais: a área projetada dividida pelo raio ao quadrado. Todas as direções juntas somam quatro pi esterradianos. |
| 4:18–4:26 | pedaço inclinado no mesmo cone; "dΩ = tamanho aparente do pedaço, visto da carga" | Na prática, o d ômega mede o tamanho aparente do pedaço visto da carga: qual abertura angular ele ocupa no espaço. |
| 4:26–4:39 | desenho principal: n̂, θ, dA⊥ = dA\|cosθ\|; o mesmo cone corta um pedaço mais longe | Se o pedaço está inclinado, conta a área projetada de frente para a carga. E, mais longe, ele precisa ser maior para parecer do mesmo tamanho. Daí o raio ao quadrado. |
| 4:39–4:44 | dA⊥ vira dA\|cosθ\| dentro da fração; caixa dΩ = dA\|cosθ\|/r² | Área, inclinação e distância: juntas, formam o d ômega. |
| 4:44–4:52 | "orientado: dΩ_or = (r̂·n̂)dA/r² = cosθ dA/r²" (o módulo some); "dΩ_or = ±dΩ · + sai, − entra" | O d ômega é só tamanho, sempre positivo. Já o d ômega orientado também leva em conta de que lado a superfície está sendo atravessada. Para a carga positiva que estamos desenhando, ele fica positivo onde o campo sai e negativo onde entra. |
| 4:52–4:58 | dΦ = E⃗·d⃗A → Coulomb → a fração vira dΩ_or | E o fluxo pelo pedaço é a carga sobre quatro pi épsilon zero, vezes o d ômega orientado. |
| 4:58–5:04 | o cone varre a superfície inteira; ∮dΩ_or = 4π | A distância sumiu. Com a carga dentro, a soma orientada sobre toda a superfície totaliza quatro pi. |
| 5:04–5:15 | "todas as direções = 4π sr (esfera unitária)" | Quatro pi esterradianos: a área da esfera unitária inteira, e não a volta de um círculo. |
| 5:15–5:21 | Φ = q/(4πε₀)·4π = q/ε₀ | Os quatro pi se cancelam: a carga sobre épsilon zero, para qualquer formato. |
| 5:21–5:30 | carga interna × carga externa; campo da carga externa na superfície | Agora coloca a carga do lado de fora. O campo na superfície não some; em alguns pontos, é até forte. |
| 5:30–5:40 | cone externo: "dΩ_or = −dΩ" na entrada, "dΩ_or = +dΩ" na saída | Mas cada feixe que entra por um lado sai pelo outro: a contribuição orientada é negativa na entrada e positiva na saída. |
| 5:40–5:45 | ∮dΩ_or = 0 | No total, o fluxo líquido é zero. Atenção: fluxo líquido zero não significa campo zero. |
| 5:45–5:59 | três cargas; q₃ fora: "0 no fluxo"; q₁/ε₀ e q₂/ε₀ | Com várias cargas, a superposição resolve: as de fora dão zero, as de dentro dão a própria carga sobre épsilon zero. |
| 5:59–6:06 | Q_env = q₁ + q₂; "soma algébrica das cargas internas" | Somando, aparece a carga envolvida: a soma, com sinal, das cargas lá dentro. |
| 6:06–6:17 | Lei de Gauss em caixa | E chegamos à Lei de Gauss: o fluxo por qualquer superfície fechada é a carga envolvida sobre épsilon zero. *(pausa)* |

### 6. Superfície ruim (6:17–7:22)

| Tempo | Na tela | Fala |
|---|---|---|
| 6:17–6:28 | esfera com a carga no centro e normais; ∮E⃗·d⃗A = q/ε₀ | Agora vem a parte mais importante do vídeo. Se a lei vale para qualquer superfície, por que não desenhar qualquer uma e sair calculando o campo? |
| 6:28–6:39 | a carga desliza, continua dentro; destaque no fluxo | Olha: eu desloco a carga, mas ela continua dentro. O fluxo continua sendo a carga sobre épsilon zero, exatamente. |
| 6:39–6:51 | três pontos com distâncias tracejadas; E₁ ≠ E₂ ≠ E₃ | Só que os pontos da esfera não estão mais à mesma distância da carga. Então o módulo do campo muda de ponto para ponto. |
| 6:51–6:57 | arcos θ (âmbar) entre campo e normal; θᵢ ≠ 0 | E quase nunca aponta na direção da normal: o teta deixa de ser zero. |
| 6:57–7:05 | ∮E⃗·d⃗A ?= E∮dA → "≠" em magenta, riscado | Por isso esse passo, em magenta, é proibido. Não dá pra tirar o campo da integral. |
| 7:05–7:16 | sonda percorre a esfera; barra de \|E⃗\| e θ mudando | A Lei de Gauss me deu um número: o fluxo total. Mas o campo na superfície é uma função que muda de ponto para ponto. |
| 7:16–7:22 | FLUXO CONHECIDO ≠ CAMPO LOCAL CONHECIDO | Saber o fluxo não é saber o campo. *(pausa)* |

### 7. Simetria da fonte (7:22–8:42)

| Tempo | Na tela | Fala |
|---|---|---|
| 7:22–7:33 | gaussiana desenhada antes da fonte, riscada em magenta | É aqui que entra a simetria. E a ordem do raciocínio importa. Você não começa escolhendo uma esfera porque quer que o problema fique esférico. |
| 7:33–7:46 | fonte simétrica; bola com carga de um lado girando | Você começa olhando para a carga. Cuidado: formato de esfera não é simetria esférica. Uma bola com mais carga de um lado parece uma esfera, mas, se eu giro, a fonte muda. |
| 7:46–7:56 | setas de rotação; a fonte simétrica gira e nada muda | A pergunta certa é: o que eu posso fazer com essa fonte sem que ela mude? Aqui, qualquer rotação em torno do centro deixa tudo igual. |
| 7:56–8:06 | componente tangencial hipotética (magenta) inverte com meia volta e vira radial; E⃗ = E(r) r̂ | Então não existe campo de lado: com uma meia volta em torno do eixo radial que passa por esse ponto, ele teria que inverter, sem a fonte mudar. |
| 8:06–8:15 | sonda à mesma distância; "o mesmo em todo o percurso" | Sobra um campo radial, que só depende da distância. Andando à mesma distância, a direção muda, mas o módulo não. |
| 8:15–8:29 | gaussiana concêntrica; normais; destaque no campo | Só agora escolhemos a esfera concêntrica: nela, campo e vetor área são paralelos, e o módulo é constante. |
| 8:29–8:42 | ∮E⃗·d⃗A = E(r)∮dA → E(r)·4πr²; "A SUPERFÍCIE EXPLORA A SIMETRIA. ELA NÃO A CRIA." | Agora, e só agora, o campo sai da integral. A superfície explora a simetria. Ela não cria. *(pausa)* |

### 8. Esfera uniforme (8:42–12:19)

| Tempo | Na tela | Fala |
|---|---|---|
| 8:42–8:58 | esfera azul com ρ; ponto interno e sua seta; campo radial em vários pontos | Bora usar isso numa esfera isolante com densidade de carga uniforme. Primeiro, o campo dentro dela. Pela simetria, antes de qualquer conta, já sabemos: o campo é radial e só depende da distância ao centro. |
| 8:58–9:10 | gaussiana r < R; E(r)·4πr² = Q_env/ε₀ | Então escolhemos uma gaussiana esférica, menor que a esfera física. O lado do fluxo fica fácil: o campo vezes a área da gaussiana. |
| 9:10–9:18 | volume envolvido (violeta); Q_env = ρV_env | Falta a carga envolvida, a que está nesse volume violeta. Como a densidade é uniforme, daria pra fazer só densidade vezes volume. |
| 9:18–9:25 | Q_env = ∫ρ dV | Mas vale ver o caminho que funciona sempre, até quando a densidade muda. |
| 9:25–9:44 | zoom; eixo z; legenda R, r, r′ linha a linha | Antes, atenção a três letras parecidas: R maiúsculo é o raio da esfera física, fixo; r é o raio da gaussiana, onde medimos o campo; e r linha é a variável que percorre o volume na integral. |
| 9:44–9:51 | ponto e r′ variando | Um ponto lá dentro fica definido por três números. O primeiro é a distância até o centro, o r linha. |
| 9:51–10:01 | ângulo polar ϑ (âmbar); "ϑ ângulo polar ≠ θ ângulo do fluxo" | O segundo é o ângulo polar, medido a partir do eixo z. Na tela, a gente usa uma outra forma da letra teta para distinguir esse ângulo polar do teta que apareceu no fluxo. |
| 10:01–10:08 | φ dá a volta em torno de z | E o terceiro é o ângulo azimutal, fi, que dá a volta em torno do eixo. |
| 10:08–10:15 | bloquinho; aresta radial dr′ | Variando cada um só um pouquinho, nasce um bloquinho. Na direção radial, a espessura é d r linha. |
| 10:15–10:20 | aresta polar r′dϑ | Na polar, o arco é r linha vezes d teta. |
| 10:20–10:34 | círculo azimutal de raio r′sinϑ, encolhendo perto do polo; aresta r′sinϑ dφ | Na azimutal, o ponto gira num círculo de raio r linha seno de teta, que encolhe perto dos polos. Por isso, o arco é r linha seno de teta d fi. |
| 10:34–10:38 | dV = dr′ · r′dϑ · r′sinϑ dφ, com chaves | Multiplicando os três, temos o elemento de volume. |
| 10:38–10:47 | Q_env(r) = ∫₀ʳρ(r′)r′²dr′ ∫sinϑ dϑ ∫dφ; r′ varre de 0 a r | Agora integramos a densidade com o r linha indo do centro até a gaussiana, porque só conta a carga lá dentro. |
| 10:47–10:54 | chaves 2 e 2π; Q_env(r) = 4π∫₀ʳρ(r′)r′²dr′ | As integrais dos ângulos dão quatro pi, para qualquer densidade que dependa só da distância ao centro. |
| 10:54–11:02 | E(r) = Q_env(r)/(4πε₀r²); "a simetria resolve a geometria · ρ(r) só determina quanta carga há dentro de r" | Guarda essa: a simetria resolve a geometria; a densidade só decide quanta carga existe dentro da gaussiana. |
| 11:02–11:10 | ρ constante → Q_env = ⁴⁄₃πρr³ | Com densidade constante, sobra a densidade vezes quatro terços de pi vezes o raio ao cubo. |
| 11:10–11:23 | substitui; corta 4π; r³/r² = r; E = ρr/3ε₀ em caixa; "interior (r < R)" | Na Lei de Gauss, o quatro pi cancela dos dois lados, e o raio ao cubo sobre o raio ao quadrado deixa o raio uma vez só. |
| 11:23–11:35 | r varia: o campo cresce em linha reta; E(0) = 0 | Resultado: o campo cresce linearmente com a distância ao centro, e no centro vale zero. Isso só vale dentro da esfera. |
| 11:35–11:48 | interior atenuado; a gaussiana atravessa r = R; a barra Q_env trava | Agora leva a gaussiana para fora da esfera. Daqui pra frente, aumentar o raio não envolve mais carga: a barra da carga envolvida trava no total. |
| 11:48–12:03 | E·4πr² = Q/ε₀ → Q/(4πε₀r²) → ρR³/(3ε₀r²) em caixa; "exterior (r > R)" | A área continua crescendo com o raio ao quadrado, então o campo passa a cair com um sobre o raio ao quadrado. Isso vale fora da esfera. |
| 12:03–12:19 | carga pontual Q no centro (a esfera esmaece); "r > R" | E repara: aí fora, o campo é exatamente o de uma carga pontual com a carga total, colocada no centro. |

### 9. Gráfico (12:19–13:07)

| Tempo | Na tela | Fala |
|---|---|---|
| 12:19–12:28 | eixos; E(0) = 0; a reta nasce | Agora junta tudo no gráfico. No centro, o campo começa em zero. Dentro, cresce em linha reta. |
| 12:28–12:37 | pico ρR/3ε₀; queda 1/r² | Atinge o máximo na superfície. E fora, cai com um sobre o raio ao quadrado. |
| 12:37–12:46 | E(R⁻) = E(R⁺); tangentes; "inclinações diferentes" | Na superfície, as duas fórmulas dão o mesmo valor: o campo é contínuo, só a inclinação muda. |
| 12:46–12:53 | "sem camada superficial de carga em R" | E é contínuo porque não existe uma camada de carga concentrada na superfície da esfera. |
| 12:53–13:07 | E⃗(r⃗) = E(r) r̂ em destaque | Agora repara no que deixou essa conta simples. Não foi a integral. Foi saber, antes de integrar, como o campo tinha que ser, por causa da simetria. |

### 10. Três simetrias (13:07–14:07)

| Tempo | Na tela | Fala |
|---|---|---|
| 13:07–13:22 | esfera concêntrica; "toda a superfície: E⃗ ∥ d⃗A ⇒ contribui" | É daí que vêm as três superfícies gaussianas famosas: cada uma funciona porque a fonte possui a simetria correspondente. Simetria esférica pede esfera concêntrica: a superfície toda contribui. |
| 13:22–13:39 | linha infinita + cilindro coaxial; lateral ∥, tampas ⊥ | Uma linha infinita, uniformemente carregada, pede um cilindro coaxial: a lateral contribui e, nas tampas, o campo é tangente, fluxo zero. |
| 13:39–13:54 | plano infinito + cilindro curto; tampas ∥, lateral ⊥ | Um plano infinito, uniformemente carregado, pede um cilindro curto atravessando o plano: agora as tampas contribuem e a lateral dá zero. |
| 13:54–14:07 | "simetrias exatas só nas idealizações infinitas" → fonte → simetria → forma do campo → superfície útil | Na linha e no plano, essas simetrias são exatas nas idealizações infinitas. Objetos finitos aproximam esse comportamento em regiões suficientemente afastadas das bordas ou extremidades. Ou seja: não é receita decorada. É consequência da simetria da fonte. |

### 11. Quando Gauss não ajuda + método (14:07–15:52)

| Tempo | Na tela | Fala |
|---|---|---|
| 14:07–14:22 | carga deslocada, barra, disco fora do eixo, distribuição irregular; tentativas de gaussiana; a lei | E isso também explica quando Gauss não é o caminho mais prático. A carga deslocada do começo, uma barra finita, um disco visto fora do eixo, uma distribuição irregular: todos obedecem à Lei de Gauss. |
| 14:22–14:40 | "A LEI CONTINUA VÁLIDA. A SIMETRIA NÃO FECHA O PROBLEMA."; destaque nos campos e na lei | Mas não existe superfície em que a simetria deixe trocar esse campo variável por um único valor de campo. Gauss continua dando o fluxo total; o que ela não dá sozinha é o campo ponto a ponto. |
| 14:40–14:52 | caminhos: esfera centrada na carga; somar Coulomb ao longo da barra | Nesses casos, outro caminho funciona melhor. Para uma carga pontual isolada, Coulomb direto resolve. Se quiser usar Gauss, a superfície útil é uma esfera centrada na própria carga — não naquela esfera arbitrária do começo. Para a barra, soma as contribuições de Coulomb ao longo dela. |
| 14:52–15:00 | disco: anéis; irregular: células | Para o disco, no eixo, a simetria deixa somar anéis. Fora do eixo, essa simplificação some: a integral fica bem mais pesada e muitas vezes vale resolver numericamente. Para uma distribuição irregular, integra, na mão ou no computador. |
| 15:00–15:07 | "com condutores: potencial ∇²V = −ρ/ε₀ e condições de contorno" | *(sem fala: trecho cortado; o tempo vai para os caminhos alternativos e o rótulo de condutores sai da tela no remapeamento)* |
| 15:07–15:16 | ícones das superfícies saem; esfera uniforme × barra finita; linha SIMETRIA DA FONTE | Então, diante de um problema novo, não pergunta primeiro qual superfície você decorou. Pergunta: qual é a simetria da fonte? |
| 15:16–15:23 | linhas DIREÇÃO DE E⃗ e DEPENDÊNCIA ESPACIAL | Ela define a direção do campo? Diz de que coordenadas o módulo depende? |
| 15:23–15:36 | linhas SUPERFÍCIE COMPATÍVEL e CARGA ENVOLVIDA | Existe uma superfície em que o campo seja constante onde contribui e tangente onde não deve contribuir? E dá pra calcular a carga envolvida? |
| 15:36–15:43 | GAUSS É UM BOM MÉTODO?; coluna da esfera em destaque: "sim" | Se as peças se encaixam, como na esfera, Gauss resolve em poucas linhas. |
| 15:43–15:52 | coluna da barra em destaque: "não: Coulomb" | Se não se encaixam, como na barra, a lei continua verdadeira; ela só não basta para achar o campo. |

*Opcional, só se a voz deixar folga no fim do bloco 11:* "Dica de prova: passa por essas cinco perguntas antes de
desenhar qualquer superfície." (+15 palavras, ~6 s).

### 12. Retorno, payoff e encerramento (15:52–16:41)

| Tempo | Na tela | Fala |
|---|---|---|
| 15:52–16:00 | os dois casos do começo; a Lei de Gauss nos dois | Voltando aos dois casos do começo, agora a diferença fica clara. Nos dois, a Lei de Gauss é igualmente válida. |
| 16:00–16:08 | esquerda: ∮ → EA; direita: "≠" em magenta | Mas só no primeiro a simetria transforma a integral do fluxo numa equação simples para o campo. |
| 16:08–16:17 | tela limpa: "A LEI DE GAUSS FALA SOBRE FLUXO." / "É A SIMETRIA DA FONTE QUE TRANSFORMA FLUXO EM CAMPO." | A Lei de Gauss fala sobre fluxo. É a simetria da fonte que transforma fluxo em campo. *(pausa ≈ 1,5 s)* |
| 16:17–16:41 | logo, anéis e "Inscreva-se para acompanhar os próximos vídeos"; duas ondas discretas | Se esse vídeo te ajudou a enxergar a Lei de Gauss de outro jeito, deixa o like: isso ajuda muito o canal. Compartilha com aquele amigo que está sofrendo com Física 3. E se inscreve no Parallax Lab, porque vem muito mais Física e Matemática por aí. A gente se vê no próximo! |

## Contagem (ritmo de referência do preview: 2,45 palavras/s)

| Bloco | Janela | Duração | Palavras | Pal/s |
|---|---|---|---|---|
| 1 Cold open | 0:00–0:33 | 33 s | 69 | 2,09 |
| 2 Intro | 0:33–0:57 | 24 s | 68 | 2,83 |
| 3 Fluxo e vetor área | 0:57–2:41 | 104 s | 220 | 2,12 |
| 4 Coulomb e esfera | 2:41–3:45 | 64 s | 136 | 2,12 |
| 5 Ângulo sólido e Lei de Gauss | 3:45–6:17 | 152 s | 361 | 2,38 |
| 6 Superfície ruim | 6:17–7:22 | 65 s | 131 | 2,02 |
| 7 Simetria da fonte | 7:22–8:42 | 80 s | 166 | 2,08 |
| 8 Esfera uniforme | 8:42–12:19 | 217 s | 454 | 2,09 |
| 9 Gráfico | 12:19–13:07 | 48 s | 89 | 1,85 |
| 10 Três simetrias | 13:07–14:07 | 60 s | 107 | 1,78 |
| 11 Quando Gauss não ajuda + método | 14:07–15:52 | 105 s | 242 | 2,30 |
| 12 Retorno, payoff e encerramento | 15:52–16:41 | 49 s | 107 | 2,18 |
| **Total** | | **1001 s** | **2150** | **2,15** |

Contagem sem a dica opcional do bloco 11 (o trecho de condutores foi cortado). A narração da ficha (seção 12) tem 2374 palavras: esta versão é ~9% mais
enxuta e deixa tempo de leitura para as equações, como nos curtos. Os blocos 9 e 10 têm folga; se a voz vier rápida,
é lá que cabe respiro (ou uma frase a mais), não acelerando o resto.

Remapeamento sem aumentar os 16:41: o tempo é redistribuído **dentro dos próprios blocos** (a ideia nova não é
acelerada; o tempo sai dos holds vizinhos):

| Região | Palavras | Janela atual | Precisa (2,85 pal/s) | Redistribuição |
|---|---|---|---|---|
| 4:44–5:15 (dΩ_or → fluxo → 4π) | 94 | 31 s | ~33 s | ~5 s do hold do "4π sr" (5:04–5:15) vão para o nascimento do dΩ_or (4:44); os ~2 s restantes saem do resultado q/ε₀ e da entrada da carga externa (5:15–5:30) |
| 14:40–15:07 (caminhos alternativos) | 83 | 27 s | ~29 s | os ~7 s do trecho de condutores (cortado) vão para a esfera centrada e o disco; ~2 s saem das folgas do checklist (15:07–15:36) |
| 0:33–0:57 (intro) | 68 | 24 s | ~24 s | cabe com a intro encurtada |

Trechos ainda no limite (~3,0 palavras/s), sem ação necessária: 4:09, 4:52 e 5:40; cada um tem folga logo depois.

## Âncoras para a sincronia (depois do áudio real)

"Então, o que mudou?" → pergunta · "fonte, depois o campo" → cadeia fonte → campo → superfície · "d A" → pedaço ·
"setinha azul" → n̂ · "seta violeta" → d⃗A · "para fora" → normais exteriores · "noventa graus" → beat do 90° ·
"o teta, em amarelo" → beat do θ · "raspando" → θ = 90° · "negativa" → superfície fechada · "linhas de campo" →
linhas · "olha as barras" → barras 1/r² × r² · "q sobre épsilon zero" (bloco 4) → caixa · "ângulo sólido, o d ômega"
→ título · "dois pi radianos" → 2π rad · "quatro pi esterradianos" → 4π sr · "inclinado" → dA⊥ = dA cosθ ·
"sempre positivo" → dΩ_or = ±dΩ · "a distância sumiu" → dΦ = q/(4πε₀) dΩ_or · "soma orientada" → varredura ·
"lado de fora" → carga externa · "negativa na entrada" → cone externo · "carga envolvida" → Q_env · "em magenta" → passo
riscado · "formato de esfera" → bola assimétrica · "meia volta" → componente tangencial · "três letras parecidas" →
legenda R / r / r′ · "nasce um bloquinho" → elemento de volume · "dão quatro pi" → Q_env(r) geral · "guarda essa"
→ E(r) = Q_env(r)/(4πε₀r²) · "densidade constante" → 4/3 πρr³ · "para fora da esfera" → gaussiana externa ·
"junta tudo no gráfico" → eixos · "camada de carga" → nota em R · "Na linha e no plano" → idealizações ·
"Pergunta:" → checklist · "como na esfera" / "como na barra" → destaques de coluna · "fala sobre fluxo" → payoff ·
"deixa o like" → logo.

## Notas de gravação

- **Mesma voz e configuração dos curtos.** Gerar por bloco (12 parágrafos) facilita medir e encaixar; uma tomada
  única dá prosódia mais contínua. Testar os dois num trecho do bloco 5.
- **Pausas reais** (0,6–1 s) depois de: "Então, o que mudou?", "Saber o fluxo não é saber o campo", "Ela não cria",
  "a carga envolvida sobre épsilon zero" (Lei de Gauss), e "transforma fluxo em campo" (≈ 1,5 s antes do CTA).
- **A voz não duplica a lousa:** cancelamento de 4π e de r³/r², as três integrais avaliadas uma a uma e a
  substituição de Q no exterior ficam só na animação.
- **Teste curto de TTS antes da tomada:** "d ômega orientado", "esterradianos", "r linha seno de teta d fi",
  "rô de r", "épsilon zero", "n chapéu" e "d A perpendicular" (caso a tela ou a voz precisem dele).
- **"em amarelo"** (bloco 3): a tela usa âmbar. Se o TTS ou a Produção preferirem, trocar por "o teta, o ângulo
  destacado".
- **Pendência técnica:** a cena cronometra a animação pelas falas da seção 12 da ficha e exige que cada fala exista
  lá literalmente. Se este texto substituir o da ficha, a etapa de voz precisa atualizar a seção 12 e remapear os
  marcos da cena. Até lá, a ficha continua sendo a referência de tempo do preview.
