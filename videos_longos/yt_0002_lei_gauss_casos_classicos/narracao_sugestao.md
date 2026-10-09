# yt_0002 — sugestão de narração (v2.2, seletiva — aprovada para TTS)

Status: **v2.2 — texto seletivo, para regerar a voz.** Base: v2.1 (2.338 palavras → 12:56 de voz, ~3,0 palavras/s). A v3 expandida (3.282 palavras) foi descartada por preencher o relógio em vez de ensinar: aqui entram só os acréscimos que trazem intuição, interpretação ou comparação, e o resto do orçamento de 18:01 fica como espaço para a animação (leitura de gráfico, cancelamentos, mudanças de região, payoff). A duração do vídeo nasce da voz.
Versões anteriores guardadas: `narracao_sugestao_v2.1_voz_12min.md`.
Não substitui `narracao.md` (texto editorial da Produção). Mesma física, mesma ordem dos beats N01–N29, molde falado do yt_0001. Tempos = início de cada trecho no vídeo fechado de 18:01 (±1–2 s). Princípio: **a voz guia a atenção e explica o porquê; o Manim mostra o como.**

Correções desta versão: o fluxo não "se espalha" (a mesma carga envolvida corresponde a uma área maior, então o campo cai); nada de "campo passando pela superfície" (nas tampas, o campo é não nulo, mas a contribuição é zero); na esfera maciça, o campo é zero no centro pela simetria e pela fórmula, não por "carga envolvida zero"; no capacitor esférico, a carga total envolvida é zero e a simetria dá campo externo zero (sem "as cargas se anulam"); os perfis diferem pela área da superfície compatível com a simetria e pela carga envolvida.

## Como falar as grandezas

| Na tela | Na fala |
|---|---|
| E⃗, E, E(r), Eₓ | **o campo** (só "E" quando a fala é a própria fórmula); Eₓ: "a componente do campo, com sinal" |
| Φ | **o fluxo** |
| dA, A | **a área**; A da tampa: **a área da tampa** (nunca "A" solto) |
| n̂ | **a normal**; "normal exterior" quando importa o sentido |
| Q_env | **a carga envolvida** |
| λ | **lambda, a densidade linear de carga** (1ª vez); depois, "a carga por comprimento" |
| σ | **sigma, a densidade superficial de carga**; σ_face: "a densidade superficial *daquela face*" |
| ρ | **rô, a densidade volumétrica de carga** |
| L | **o comprimento do cilindro** (escolha nossa) |
| R | **o raio da fonte** (do cilindro de carga, da casca, da esfera); letra só quando a tela aponta |
| r | **o raio da gaussiana / a distância ao eixo (ou ao centro)** |
| a, b (condutores) | **o raio interno**, **o raio externo** |
| a (slab), x | **a meia espessura**, **a distância ao plano do meio** — nunca "a" solto |
| ε₀ | **épsilon zero** |
| 2πrL, 4πr² | "dois pi vezes o raio vezes o comprimento", "quatro pi vezes o raio ao quadrado" |
| 1/r, 1/r² | "um sobre a distância", "um sobre o raio ao quadrado" |
| E ∝ r | "o campo cresce em linha reta" |
| R⁻, R⁺ | "logo por dentro", "logo por fora" |

Evitar: dizer que carga envolvida zero *sozinha* dá campo zero (é carga envolvida zero **mais** a simetria; nos condutores, o campo zero vem do equilíbrio); dizer que o campo de uma placa finita "não cai com a distância" (é da chapa infinita); chamar o fator 2 de "regra" (vem de duas tampas); "o campo passa pela superfície" no sentido de contar linhas; "campo zero" onde o que é zero é a contribuição ao fluxo (tampas do cilindro); a mesma letra para duas coisas na mesma frase.

## Narração por blocos de tempo

### 1. Cold open (0:00–0:22)

| Tempo | Na tela | Fala |
|---|---|---|
| 0:00–0:07 | a linha, a esfera e as duas placas entram, uma de cada vez | Uma linha de carga, uma esfera e duas placas. |
| 0:07–0:14 | um perfil por vez: cai com a distância, cai mais rápido, constante | Na linha, o campo cai como um sobre a distância. Na esfera, como um sobre a distância ao quadrado. Entre placas ideais, ele fica constante. |
| 0:14–0:22 | um traço liga os três casos; a pergunta; destaque alternado | Três perfis diferentes, uma só Lei de Gauss. Então, o que muda de verdade? *(pausa)* |

### 2. Intro (0:22–0:36)

| Tempo | Na tela | Fala |
|---|---|---|
| 0:22–0:30 | PARALLAX LAB · LEI DE GAUSS · Três simetrias, um método | Fala, pessoal! Bem-vindos de volta ao Parallax Lab. |
| 0:30–0:36 | os casos clássicos: linha, esfera, placas, um de cada vez | No vídeo anterior, a simetria transformou fluxo em campo. Hoje a gente pega essa ideia e resolve os casos clássicos sem decorar uma fórmula pra cada desenho. |

### 3. Recap e algoritmo (0:36–1:17)

| Tempo | Na tela | Fala |
|---|---|---|
| 0:36–0:48 | a lei; uma superfície fechada com carga dentro; outra superfície com as mesmas cargas | A Lei de Gauss vale pra qualquer superfície fechada que você desenhar: o fluxo líquido do campo é a carga envolvida, só a que está lá dentro, dividida por épsilon zero. |
| 0:48–1:01 | uma carga externa: o campo entra de um lado e sai do outro; os vetores continuam lá | Uma carga que ficou fora não entra na carga envolvida, mas ainda pode criar campo sobre a superfície. O campo dela entra de um lado e sai do outro, e o fluxo líquido dá zero. Por isso, fluxo zero não significa campo zero. |
| 1:01–1:09 | a superfície vira uma moldura transparente em volta de uma fonte | Pra achar o campo direto, a gente precisa de simetria. É ela que diz a direção do campo e onde o módulo pode ser tratado como constante. A superfície é só uma moldura: organiza a conta, mas não cria simetria. |
| 1:09–1:17 | o algoritmo entra uma etapa por vez (leitura de ~3 s no fim) | Daí vem o método: identifica a fonte, reconhece a simetria, descobre a direção do campo, escolhe a gaussiana, simplifica o fluxo e calcula a carga envolvida, dividindo em regiões quando precisar. Vamos começar pela simetria cilíndrica. |

### 4. Linha: reconhecer a simetria (1:17–2:03)

| Tempo | Na tela | Fala |
|---|---|---|
| 1:17–1:28 | a linha azul; λ; a chave desliza ao longo dela; pontas tracejadas | Essa linha tem a mesma carga por comprimento em todo lugar: a densidade linear de carga, lambda. E ela é infinita, uma idealização que tira da conta o efeito das pontas. |
| 1:28–1:43 | uma janela anda ao longo da linha; na vista de cima, o ponto dá a volta | Imagina que você anda ao longo da linha, ou gira em volta dela: a fonte parece a mesma. Então o campo não pode preferir uma posição ao longo da linha, nem uma direção ao redor dela. |
| 1:43–1:56 | um par de cargas simétricas; as componentes axiais se anulam; os outros pares repetem | Agora pega um ponto e duas cargas da linha, uma acima e outra abaixo, à mesma distância. As componentes ao longo da linha se cancelam, e o mesmo vale pra todos os outros pares. |
| 1:56–2:03 | estado final: só o campo radial; E⃗ = E(r) r̂ | Sobra só a direção radial. Pra carga positiva, ela aponta pra fora, e o módulo só pode depender da distância até a linha. |

### 5. Linha: lateral e tampas (2:03–2:52)

| Tempo | Na tela | Fala |
|---|---|---|
| 2:03–2:11 | o cilindro gaussiano fechado; o raio e o comprimento marcados | Agora escolhe um cilindro fechado, com o mesmo eixo da linha. O raio dele é a distância onde você quer o campo. O comprimento é um trecho qualquer: escolha nossa. |
| 2:11–2:23 | a lateral vira contínua; normal e campo alinhados | Na lateral, todos os pontos estão à mesma distância da linha, então o campo tem o mesmo módulo e aponta na direção da normal. O fluxo lateral vira o campo vezes a área lateral. |
| 2:23–2:38 | as tampas; a normal é axial; produto escalar zero (5 s) | Nas tampas é diferente. O campo continua radial, mas a normal da tampa aponta ao longo do eixo. Os dois ficam perpendiculares, e o produto escalar entre eles dá zero. O campo ali não é nulo, mas a tampa não contribui pro fluxo. |
| 2:38–2:52 | tampas sem fluxo; só a lateral conta | Repara nisso: o campo não sumiu nas tampas. Quem some é a contribuição delas pro fluxo. E é isso que deixa só a lateral na conta. |

### 6. Linha: carga e resultado (2:52–3:36) — fórmula-âncora da família cilíndrica

| Tempo | Na tela | Fala |
|---|---|---|
| 2:52–3:00 | a área lateral; o trecho da linha dentro do cilindro | O fluxo é o campo vezes dois pi, vezes o raio, vezes o comprimento. E a carga envolvida é a densidade linear vezes o comprimento: só o pedaço da linha que está dentro. |
| 3:00–3:10 | Gauss; o comprimento aparece nos dois lados e cancela | Na Lei de Gauss, o comprimento aparece dos dois lados e cancela. Faz sentido: foi uma escolha nossa, não pode mandar no campo de uma linha infinita. |
| 3:10–3:27 | E em caixa; teste: dobrar r, as setas caem à metade | O campo vale lambda sobre o produto de dois pi, épsilon zero e a distância à linha: cai como um sobre a distância. Testa: dobra a distância. A área lateral dobra. Como a carga envolvida não mudou, o fluxo total também não muda. Então o campo precisa cair pela metade. |
| 3:27–3:36 | a primeira ferramenta; o cilindro fica | Essa é a nossa primeira ferramenta. O cilindro gaussiano fica; o que vai mudar é onde a carga está. |

### 7. Casca cilíndrica (3:36–4:22)

| Tempo | Na tela | Fala |
|---|---|---|
| 3:36–3:47 | o filamento vira uma parede; a gaussiana não muda | Agora a carga deixa de estar num fio e vai pra uma casca cilíndrica: fina, uniforme e infinita ao longo do eixo. Lambda continua sendo a carga total por comprimento. |
| 3:47–3:59 | r < R: carga envolvida zero e campo zero, com o selo da simetria | Com a gaussiana por dentro da casca, a carga envolvida é zero. E, pela simetria cilíndrica, o campo lá dentro também é zero. Só a carga envolvida zero não bastaria: a simetria completa o argumento. |
| 3:59–4:06 | r > R: toda a carga daquele comprimento; igual à linha | Por fora, a gaussiana envolve toda a carga daquele comprimento, e o resultado é exatamente o da linha. |
| 4:06–4:22 | o salto: dois estados, logo por dentro e logo por fora | Mas olha: ao atravessar a camada carregada, o campo salta de zero pra um valor diferente de zero. Uma casca não tem o perfil de um cilindro maciço, e já já a gente vê a diferença. |

### 8. Cilindro maciço (4:22–5:14)

| Tempo | Na tela | Fala |
|---|---|---|
| 4:22–4:32 | a casca ganha volume; ρ | Agora preenche o interior: em vez de uma casca, a carga fica espalhada por todo o volume de um isolante. A densidade passa a ser volumétrica, carga por volume: rô. |
| 4:32–4:46 | r < R: só a parte da fonte dentro da gaussiana; volume violeta | Com a gaussiana menor que o cilindro de carga, só entra na conta o pedaço que ficou dentro dela. Então, no volume, vale o raio da gaussiana, não o raio da fonte. |
| 4:46–4:55 | cancelamentos: π e L, depois uma potência do raio; riscados antes de sumir | A carga envolvida cresce com o raio ao quadrado, a área lateral cresce com o raio, e sobra o raio: o campo cresce em linha reta. |
| 4:55–5:14 | r > R: a carga congela em R²; r continua na área; duas medidas (4 s) | Quando a gaussiana passa pra fora, a carga envolvida para de crescer, porque já pegou o cilindro inteiro. Aí o raio da fonte, que é fixo, entra na carga, e o raio da gaussiana continua só na área. Dois raios diferentes, dois papéis diferentes. E o campo volta a cair como um sobre a distância. |

### 9. Cilindro: gráfico e continuidade (5:14–5:41)

| Tempo | Na tela | Fala |
|---|---|---|
| 5:14–5:30 | gráfico normalizado; marcador sincronizado com a gaussiana; em r = R os dois ramos se encontram | Juntando tudo num gráfico: no eixo, o campo é zero. Ele sobe em linha reta por dentro do cilindro e encontra a curva de fora exatamente na borda. A inclinação muda ali, mas o valor é o mesmo: o campo não salta. |
| 5:30–5:41 | o fantasma da casca, em violeta, só para comparar | A gente não colocou nenhuma camada de carga na superfície, então não existe salto. Compara com a casca: a gaussiana é a mesma, e o que muda é como a carga está distribuída. |

### 10. Cabo coaxial (5:41–6:22)

| Tempo | Na tela | Fala |
|---|---|---|
| 5:41–5:52 | o isolante vira condutor maciço; entra a casca externa, de carga oposta | Agora troca o isolante por um condutor maciço, com uma casca condutora em volta, no mesmo eixo. No equilíbrio, a carga do condutor de dentro fica na superfície dele, e as cargas por comprimento são iguais e opostas. |
| 5:52–6:00 | r < raio interno: holofote no núcleo; E = 0 | Dentro de um condutor em equilíbrio, o campo é zero; e uma gaussiana nessa região também não envolve carga. |
| 6:00–6:12 | no vão: holofote no vão; campo radial | No vão, entre os dois condutores, a gaussiana envolve a carga positiva do condutor de dentro. O campo é radial e cai como um sobre a distância, igual ao da linha. O raio da gaussiana, aqui, fica entre o raio interno e o raio externo. |
| 6:12–6:22 | por fora: as cargas se cancelam; campo confinado ao vão | Por fora das duas camadas, as cargas envolvidas se cancelam e, com essa simetria, o campo é zero. O campo fica preso no vão, apontando do positivo pro negativo. |

### 11. Ponte para o plano (6:22–6:32)

| Tempo | Na tela | Fala |
|---|---|---|
| 6:22–6:32 | quatro cortes com a mesma gaussiana violeta; "o que muda: a carga envolvida, por região" | Um único cilindro gaussiano resolveu quatro fontes: a linha, a casca, o cilindro maciço e o cabo coaxial. Mudou só a carga envolvida em cada região. E se a fonte for um plano inteiro? |

### 12. Folha infinita (6:32–8:24) — fórmula-âncora da família planar

| Tempo | Na tela | Fala |
|---|---|---|
| 6:32–6:43 | a folha; σ; um pedaço de área desliza | Essa chapa não condutora tem carga uniforme por área: a densidade superficial de carga, sigma. Ela é infinita nas duas direções do plano, então não tem borda pra distinguir um ponto de outro. |
| 6:43–6:55 | o ponto anda paralelo à folha; depois gira dentro do plano | Anda paralelo à chapa, ou gira dentro do plano: a fonte, vista daí, não muda. |
| 6:55–7:07 | pares simétricos; as componentes paralelas se anulam | Por simetria, as componentes paralelas ao plano se cancelam, por pares de cargas simétricas. Sobra só a componente perpendicular: o campo só pode ser perpendicular à chapa. |
| 7:07–7:14 | os dois lados: mesmo módulo, sentidos opostos | Pra carga positiva, ele aponta pra fora dos dois lados: sentidos opostos, módulos iguais, porque os dois lados são equivalentes. |
| 7:14–7:30 | o pillbox atravessa a folha; tampas: campo e normal paralelos; lateral: perpendiculares | Como superfície, um cilindro curto atravessando a chapa, uma caixinha fechada. Na lateral, o campo é tangente, então não contribui pro fluxo. Nas duas tampas, o campo e a normal exterior apontam pro mesmo lado, e as duas contribuem. |
| 7:30–7:45 | EA + EA = 2EA: a tampa da direita, depois a da esquerda (5 s) | O fluxo é o campo vezes a área da tampa de um lado, mais o campo vezes a área da tampa do outro: duas vezes o campo vezes a área. É daí que vem o fator dois. Ele não é uma regra decorada: é o número de tampas que contribuem. |
| 7:45–7:58 | a carga envolvida: o pedaço da folha dentro da caixa; a área cancela | A carga envolvida é sigma vezes essa mesma área, a do pedaço de chapa dentro da caixa. Na Lei de Gauss, a área cancela dos dois lados, e o campo vale sigma sobre duas vezes épsilon zero. |
| 7:58–8:24 | as tampas se afastam; A e a carga envolvida não mudam; campo constante (4 s) | Repara: não aparece distância nenhuma no resultado. Afasta as tampas: a área e a carga envolvida não mudam, então o campo não diminui. Isso vale pra chapa infinita. Numa placa real, o campo cai quando você se afasta bastante; por isso a gente não transfere essa conclusão automaticamente. |

### 13. Slab: carga na espessura (8:24–9:34)

| Tempo | Na tela | Fala |
|---|---|---|
| 8:24–8:37 | a folha ganha espessura; faces em ±(meia espessura); ρ | Agora a folha ganha espessura. A carga não está mais sobre uma superfície: está espalhada pelo volume, com densidade volumétrica, rô. O plano do meio vira nossa origem, e as duas faces ficam à mesma distância dele: a meia espessura. |
| 8:37–8:56 | ponto à direita, dentro; a fatia envolvida de espessura 2x (4 s); o 2 e a área cancelam | Começa com um ponto à direita, ainda dentro da placa. A caixa gaussiana é simétrica, com uma tampa de cada lado do plano do meio. Então a espessura que ela envolve é duas vezes a distância do ponto ao plano do meio. A carga envolvida cresce com essa distância, e o campo cresce em linha reta. |
| 8:56–9:05 | gráfico com sinal: Eₓ × x | No centro, por simetria, o campo é zero. Do outro lado, o sentido se inverte: por isso o gráfico mostra a componente do campo, com sinal. |
| 9:05–9:20 | as tampas passam das faces; carga constante; patamar | Quando a gaussiana passa das faces, ela já envolve toda a espessura da placa. A carga envolvida para de crescer, e o campo fica constante. |
| 9:20–9:34 | contínuo nas duas faces | Na passagem pelas faces, não existe camada de carga concentrada: só o fim da densidade volumétrica. Por isso o campo é contínuo ali, sem salto. |

### 14. Duas chapas opostas (9:34–10:16)

| Tempo | Na tela | Fala |
|---|---|---|
| 9:34–9:43 | a placa sai; entram duas folhas, +σ e −σ; cada uma sozinha | Agora troca a placa por duas chapas paralelas, com densidades iguais e de sinais opostos. Cada uma, sozinha, você já sabe resolver: é o campo da folha infinita. |
| 9:43–9:55 | por fora: dois vetores opostos de mesmo módulo se encontram e se anulam | Por fora das duas chapas, os campos têm sentidos opostos e o mesmo módulo, e se cancelam. O campo total, ali, é zero, dos dois lados. |
| 9:55–10:08 | entre as folhas: o mesmo sentido, soma; resultante | Entre as chapas, o campo da positiva aponta pra negativa, e o da negativa também. Os dois se somam: o dobro do campo de uma chapa só, uniforme, do positivo pro negativo. |
| 10:08–10:16 | estado final: campo uniforme só no vão | Esse é o campo do capacitor plano ideal, sem as bordas. A gente não vai calcular capacitância: o objetivo é entender onde o campo existe. |

### 15. Face de condutor e síntese planar (10:16–11:21)

| Tempo | Na tela | Fala |
|---|---|---|
| 10:16–10:28 | o plano vira a face de um condutor: metal à esquerda, vácuo à direita | Tem uma consequência curta que evita uma confusão comum. Junto à superfície de um condutor em equilíbrio, o campo dentro do metal é zero. Metal de um lado, vácuo do outro. |
| 10:28–10:50 | pillbox pequeno: a tampa de dentro, em E = 0; a lateral encolhe | Pega uma caixa gaussiana pequena, atravessando a face. A tampa de dentro está no metal, onde o campo é zero, então não contribui. A lateral também não contribui, quando a caixa fica bem achatada. Só sobra a tampa de fora. Então o fluxo é só o campo vezes a área, sem fator dois. Repara na diferença pra folha isolante: lá, as duas tampas contribuíam. |
| 10:50–11:05 | a densidade da face; comparação EA × 2EA | O campo logo fora vale a densidade superficial daquela face, dividida por épsilon zero. Cuidado com a palavra face: essa densidade é local, não é a carga total dividida pela área. Mudaram as hipóteses, não a Lei de Gauss. |
| 11:05–11:21 | a mesma caixa em quatro fontes; a casca esférica entra | A mesma caixa atravessou a chapa, a placa grossa, as duas chapas e a face do condutor. Em cada caso, mudou só a carga envolvida e a região. Falta a geometria que trata todas as direções igualmente ao redor de um centro: a esfera. Vamos pra ela. |

### 16. Casca esférica (11:21–12:11)

| Tempo | Na tela | Fala |
|---|---|---|
| 11:21–11:35 | a casca esférica azul; a rotação em torno do centro deixa tudo igual | Agora distribui uma carga total, uniformemente, numa casca esférica. Gira a esfera em torno do centro, em qualquer direção: a distribuição não muda. Nenhuma direção é especial. |
| 11:35–11:42 | só o campo radial; depende só da distância ao centro | Então o campo só pode ser radial, e o módulo só depende da distância ao centro. |
| 11:42–11:58 | a esfera gaussiana concêntrica (matemática, não material); mesmo módulo, paralelo à normal | A gaussiana é uma esfera com o mesmo centro. Em todos os pontos dela, o campo tem o mesmo módulo e aponta na direção da normal. Então o fluxo é o campo vezes a área da esfera: quatro pi vezes o raio ao quadrado. A superfície inteira contribui, sem tampas e sem laterais. |
| 11:58–12:11 | a pergunta que decide os ramos (3 s) | É a mesma construção do primeiro vídeo. A pergunta que decide tudo agora: a gaussiana envolve a casca, ou ainda está dentro dela? A carga envolvida depende da resposta. |

### 17. Casca esférica: as regiões (12:11–12:56) — fórmula-âncora da família esférica

| Tempo | Na tela | Fala |
|---|---|---|
| 12:11–12:20 | por dentro: carga envolvida zero; campo zero | Por dentro, a carga envolvida é zero e, pela simetria esférica, o campo também é zero. Isso não vale pra qualquer superfície vazia: precisa da simetria. |
| 12:20–12:32 | por fora: toda a carga da casca; E = Q/(4πε₀r²) | Por fora, a carga envolvida é a carga total da casca. O campo vale a carga total sobre o produto de quatro pi, épsilon zero e o raio ao quadrado: cai com um sobre o raio ao quadrado. |
| 12:32–12:41 | equivalência com a carga pontual no centro, só para pontos externos | É igual ao campo de uma carga pontual, com toda a carga da casca, colocada no centro. Mas só por fora. Por dentro, essa equivalência não vale. |
| 12:41–12:56 | o salto: logo por dentro e logo por fora | E aqui também tem um salto, como na casca cilíndrica: logo por dentro, zero; logo por fora, diferente de zero. É a camada de carga na superfície que faz o campo mudar de repente. |

### 18. Esfera maciça (12:56–14:00)

| Tempo | Na tela | Fala |
|---|---|---|
| 12:56–13:04 | a casca ganha volume; carga de volume | Agora preenche a esfera com carga uniforme num isolante. A gente já fez esse caso no primeiro vídeo, então só recupera o raciocínio. |
| 13:04–13:20 | por dentro: carga ∝ r³, área ∝ r²; 4π cancela; sobra r | Por dentro, a carga envolvida cresce com o cubo do raio, e a área da gaussiana cresce com o raio ao quadrado. Divide uma pela outra, e sobra o raio: o campo cresce em linha reta, a partir de zero no centro. |
| 13:20–13:35 | por fora: a carga congela; a área continua crescendo | Por fora, a carga envolvida para de crescer, porque já pegou a esfera inteira. A área continua crescendo com o raio ao quadrado. Então o campo passa a cair com um sobre o raio ao quadrado, como o de uma carga pontual. |
| 13:35–13:48 | gráfico sincronizado; os ramos se encontram em R (sem salto) | No gráfico, os dois ramos se encontram na borda, sem salto: não existe camada de carga na superfície da esfera maciça, ao contrário da casca. |
| 13:48–14:00 | comparação normalizada com o cilindro maciço (5 s) | Comparando com o cilindro maciço: os dois crescem em linha reta por dentro, mas a cauda do cilindro é um sobre o raio, e a da esfera, um sobre o raio ao quadrado. Cada gráfico está normalizado pelo valor na borda: dá pra comparar o formato, não a intensidade. |

### 19. Capacitor esférico (14:00–14:46)

| Tempo | Na tela | Fala |
|---|---|---|
| 14:00–14:10 | o isolante vira condutor maciço; entra a casca externa, de carga oposta | Agora troca a esfera isolante por uma esfera condutora maciça, em equilíbrio: a carga positiva vai pra superfície. Em volta, uma casca condutora com o mesmo centro e a carga oposta. |
| 14:10–14:24 | dentro do metal: E = 0; no vão: a gaussiana envolve só a carga positiva | Dentro do condutor central, o campo é zero, e a gaussiana ali não envolve carga. No vão, entre os dois condutores, ela envolve só a carga positiva, e o campo cai com um sobre o raio ao quadrado. |
| 14:24–14:34 | por fora: cargas envolvidas se cancelam; E = 0 | Depois da casca externa, a carga total envolvida é zero e, com a simetria esférica, o campo externo também é zero. |
| 14:34–14:46 | campo confinado ao vão | De novo, o campo fica preso entre os condutores. Mas o perfil não é o do coaxial, nem o das placas: a mesma lei, uma assinatura diferente em cada geometria. Ela vem de como a área da gaussiana cresce e de quanta carga ela envolve. |

### 20. Três capacitores (14:46–15:28)

| Tempo | Na tela | Fala |
|---|---|---|
| 14:46–15:02 | os três, um por vez, cada um com a lei do vão | Os três capacitores, lado a lado. Nas placas paralelas, o campo no vão é constante. No coaxial, ele cai com um sobre a distância ao eixo. No esférico, cai com um sobre o raio ao quadrado. |
| 15:02–15:10 | "exterior: E = 0, neste modelo" | Isso vale entre os condutores. Por fora, o campo é zero nesses modelos: cargas iguais e opostas, sem fonte externa. |
| 15:10–15:28 | os três diagramas pequenos, uma lei em cada | Não são três leis. São três formas de aplicar a mesma Lei de Gauss. O que muda é como cresce a área da superfície compatível com a simetria, enquanto a carga envolvida no vão fica fixa. É isso que dá perfis diferentes. Lembra do começo do vídeo? Era essa a pergunta. |

### 21. Área, carga fixa e potências (15:28–16:20)

| Tempo | Na tela | Fala |
|---|---|---|
| 15:28–15:43 | a esfera cresce; a área cresce; as setas caem | Olha de novo essas potências. Na esfera, a área da gaussiana cresce com o raio ao quadrado. Com a carga envolvida fixa, o campo precisa cair na mesma proporção pra manter o fluxo constante. |
| 15:43–15:57 | o cilindro, comprimento fixo | No cilindro, pra um comprimento escolhido, a área lateral cresce só com o raio. Então, com a carga envolvida fixa naquele trecho, o campo cai com um sobre o raio, mais devagar que na esfera. |
| 15:57–16:09 | o plano: as tampas se afastam, A e Q_env não mudam | No plano, afastar as tampas não aumenta a área delas, nem a carga envolvida. Então o campo fica constante. |
| 16:09–16:20 | o selo "simetria + carga envolvida fixa"; o interior dos maciços (4 s) | Mas isso não é regra de espalhamento pra qualquer fonte. Quem permite usar um único valor de campo é a simetria. E, por dentro dos maciços, a carga envolvida também cresce: olha sempre os dois lados da equação. |

### 22. Checklist aplicado (16:20–17:18)

| Tempo | Na tela | Fala |
|---|---|---|
| 16:20–16:37 | perguntas 1 a 3, no cilindro maciço | Antes de integrar, faz seis perguntas. Primeira: qual é a simetria da fonte? Segunda: em que direção o campo pode apontar? Terceira: de quais coordenadas o módulo do campo pode depender? Essas três vêm da fonte, antes de qualquer superfície. |
| 16:37–16:53 | pergunta 4; as três superfícies (esfera, cilindro, caixa curta) | Quarta: qual superfície fechada deixa o campo constante onde ele contribui e tangente onde não contribui? Esfera concêntrica na família esférica, cilindro coaxial na cilíndrica, caixa curta atravessando o plano na planar. |
| 16:53–17:06 | perguntas 5 e 6; decisão dentro/fora (5 s) | Quinta: quanta carga ela realmente envolve? Sexta: o problema precisa ser dividido em regiões? No cilindro maciço, por dentro, o raio da gaussiana entra no volume. Por fora, entra o raio da fonte. |
| 17:06–17:18 | "a superfície foi reaproveitada; a carga mudou" | A superfície foi a mesma. A carga mudou. É isso que você precisa reconhecer antes de procurar uma fórmula pronta. |

### 23. Payoff, pausa e encerramento (17:18–18:01)

| Tempo | Na tela | Fala |
|---|---|---|
| 17:18–17:36 | tela limpa; "IDENTIFIQUE A SIMETRIA DA FONTE" / "SUPERFÍCIE ÚTIL → CARGA ENVOLVIDA → CAMPO" | Você não precisa decorar um campo diferente pra cada desenho. Identifica a simetria da fonte, escolhe uma superfície onde o fluxo simplifica e calcula a carga envolvida na região. Esfera, cilindro e plano são três versões do mesmo raciocínio. |
| 17:36–17:38 | payoff sustentado | *(pausa de 2 s, sem fala)* |
| 17:38–18:01 | logo, anéis e "Inscreva-se para acompanhar os próximos vídeos" | No próximo vídeo de Gauss, a gente leva esse método pra problemas menos diretos, em que reconhecer a estratégia é justamente a parte difícil. Se esse vídeo te ajudou, deixa o like, compartilha e se inscreve no Parallax Lab. A gente se vê no próximo. |

## Contagem (palavras por janela do vídeo atual; cadência real da voz: ~3,0 palavras/s)

| Bloco | Janela atual | Palavras | Pal/s na janela | Fala a 3,0 pal/s | Fala − janela |
|---|---|---|---|---|---|
| 1. Cold open | 22 s | 48 | 2,18 | 16 s | −6 s |
| 2. Intro | 14 s | 35 | 2,50 | 12 s | −2 s |
| 3. Recap e algoritmo | 41 s | 150 | 3,66 | 50 s | +9 s |
| 4. Linha: reconhecer a simetria | 46 s | 124 | 2,70 | 41 s | −5 s |
| 5. Linha: lateral e tampas | 49 s | 133 | 2,71 | 44 s | −5 s |
| 6. Linha: carga e resultado | 44 s | 129 | 2,93 | 43 s | −1 s |
| 7. Casca cilíndrica | 46 s | 119 | 2,59 | 40 s | −6 s |
| 8. Cilindro maciço | 52 s | 143 | 2,75 | 48 s | −4 s |
| 9. Cilindro: gráfico e continuidade | 27 s | 75 | 2,78 | 25 s | −2 s |
| 10. Cabo coaxial | 41 s | 131 | 3,20 | 44 s | +3 s |
| 11. Ponte para o plano | 10 s | 34 | 3,40 | 11 s | +1 s |
| 12. Folha infinita | 112 s | 269 | 2,40 | 90 s | −22 s |
| 13. Slab: carga na espessura | 70 s | 172 | 2,46 | 57 s | −13 s |
| 14. Duas chapas opostas | 42 s | 111 | 2,64 | 37 s | −5 s |
| 15. Face de condutor e síntese planar | 65 s | 181 | 2,78 | 60 s | −5 s |
| 16. Casca esférica | 50 s | 125 | 2,50 | 42 s | −8 s |
| 17. Casca esférica: as regiões | 45 s | 125 | 2,78 | 42 s | −3 s |
| 18. Esfera maciça | 64 s | 181 | 2,83 | 60 s | −4 s |
| 19. Capacitor esférico | 46 s | 135 | 2,93 | 45 s | −1 s |
| 20. Três capacitores | 42 s | 107 | 2,55 | 36 s | −6 s |
| 21. Área, carga fixa e potências | 52 s | 126 | 2,42 | 42 s | −10 s |
| 22. Checklist aplicado | 58 s | 125 | 2,16 | 42 s | −16 s |
| 23. Payoff, pausa e encerramento | 43 s | 84 | 1,95 | 28 s | −15 s |
| **Total** | **1081 s** | **2862** | **2,65** | **954 s** | **−127 s** |

Cadência medida da voz (ElevenLabs, v2.1): 2.338 palavras em 12:56, ou seja, ~3,0 palavras/s. Fala estimada deste texto: ~15:54; o restante do orçamento de 18:01 é espaço de animação (leitura de gráfico, cancelamentos, mudanças de região, payoff). A duração final do vídeo nasce da voz medida. Janela mais curta que a fala (coluna final positiva) = a cena comprime a animação; mais longa = respiro visual.


## Ainda em aberto

1. **Cadência da voz:** a v2.1 saiu a ~3,0 palavras/s. Com ~3.100 palavras, a expectativa é ~17:00–17:30 de fala; o resto do orçamento de 18:01 vira respiro de animação. Se o ElevenLabs sair ainda mais rápido, o ajuste é a velocidade da voz, não mais texto.
2. **Partes do ElevenLabs:** limite de 5.000 caracteres por geração; o texto está dividido em blocos (`texto_narracao_bloco1..N.txt`), cada um em fronteira de assunto.
3. **Depois da voz:** alinhar (`gerar_sync.py alinhar`, ajustando `PARTE_DE` ao número de partes), passada a seco com `AJUSTAR=1`, passada a seco normal, `montar`, e só então o render final (ver `LEIA-ME_RENDER_FINAL.md`).
