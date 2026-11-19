# yt_0021 — sugestão de narração v2 (a partir dos quadros do preview v7)

Base: narração congelada v1.1 (`narracao_sugestao.md`), conferida contra o preview v7 960×540. **Só 4 âncoras mudam de texto** (T2-4, T4-1, T4-3, T5-3) e 3 trocam a tag `[serious]`; as outras ficam como estão, porque a tela mostra o que a fala descreve. Cada bloco traz o horário no preview v7, o que aparece na tela e a fala. Tags `[ ]` do ElevenLabs v4; não entram na legenda.

**Como foi conferido:** vi os quadros das pranchas PH (hook), PT2, PT4 e PT5 e li as descrições de tela das demais âncoras (handoffs v1–v6 e código das seções). Não revi uma a uma as pranchas PT1, PT3, PT6, PE1–PE3, PA e PS-EN para esta sugestão; nessas o texto segue o congelado e o bloco traz a descrição do handoff, marcada como 'quadro não revisto'.

**Aviso de sincronia:** o vídeo foi moldado à voz por âncora (2,65 palavras/s). T2-4 fica em 62 palavras (era 64), T4-1 em 53 (era 51), T4-3 em 49 (era 45) e T5-3 em 92 (era 82); T5-3, T4-3 e T4-1 ficam um pouco mais longas, e o ajuste de duração delas é da fase de sync, depois da voz.

**Pontos para o GPT refinar:**
- `[serious]` (T5-5, E2-5, E3-7) não está na lista validada de tags; troquei por `[thoughtful, emphatic]`.
- Muitas âncoras abrem com 'Agora…' ou 'Então…'; vale variar os conectivos (docs/roteiro_voz_elevenlabs_v4.md).
- Símbolos lidos como 'm i', 'r i', 'I cm', 'ômega': confirmar a pronúncia na voz v4.
- Abertura (A1–A2) e CTA (EN1–EN2) seguem o congelado; revisar contra `docs/padrao_video_longo.md`.
- Números falados com precisão simplificada (a tela mostra mais casas): conferir E3 (0,0731 e 0,0694) e T3-4 (0,212 e 0,053).


## HOOK

### H1 · 0:00–0:19 · 20 s · 52 palavras

*Quadros v7: 0:18 · dois bastões girando (eixo na ponta do cabo e na ponta grossa), barras de ENERGIA subindo, legendas EIXO NA PONTA DO CABO / DA PONTA GROSSA.*

[curious] Olha esses dois bastões. São exatamente o mesmo bastão: mesma madeira, mesma massa, mesmo comprimento. A única diferença é onde ele está preso. Aqui o eixo passa pela ponta do cabo, e aqui pela ponta grossa. E a gente vai levar os dois, partindo do repouso, até girar na mesma velocidade angular.

### H2 · 0:19–0:45 · 25 s · 67 palavras

*Quadros v7: 0:43 · M = 0,90 kg, L = 0,84 m, ω = 10 rad/s nos dois, barras 14,1 J e 7,06 J, selo NÚMEROS DE EXEMPLO · PLANO HORIZONTAL · EIXO VERTICAL.*

[thoughtful] O bastão tem nove décimos de quilo e oitenta e quatro centímetros. Os dois giram até dez radianos por segundo, e a gente está de cima, no plano horizontal, então a altura não muda e não entra energia potencial nessa história. Resultado: segurando pelo cabo, o braço entrega quatorze joules. Segurando pela ponta grossa, só sete. Exatamente a metade, para o mesmo bastão, na mesma velocidade angular.

### H3 · 0:45–1:00 · 16 s · 41 palavras

*Quadros v7: 0:59 · a pergunta POR QUE O MESMO BASTÃO EXIGE O DOBRO DE ENERGIA PARA GIRAR? aparece acima das duas cenas, barras no máximo.*

[curious] E aí fica a pergunta. A massa não mudou. A velocidade angular final não mudou. O que, então, mudou para a energia dobrar? E mais: existe um número que diga, para qualquer corpo e qualquer eixo, quanto custa fazer ele girar?


## ABERTURA

### A1 · 1:00–1:03 · 3 s · 6 palavras

*Tela (descrição do handoff; quadro não revisto): logo; BEM-VINDOS AO PARALLAX LAB*

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 · 1:03–1:26 · 23 s · 60 palavras

*Tela (descrição do handoff; quadro não revisto): MOMENTO DE INÉRCIA: POR QUE O MESMO BASTÃO EXIGE O DOBRO DE ENERGIA PARA GIRAR?; abaixo, NESTE VÍDEO: e três ícones com rótulo: soma de pedaços (ENERGIA DE UM GIRO), haltere com eixo móvel (MOMENTO DE INÉRCIA), barra com dois eixos (EIXOS PARALELOS)*

[thoughtful] Hoje a gente vai construir uma das grandezas mais importantes da rotação: o momento de inércia. Primeiro, de onde ele aparece, a partir da energia de um corpo girando. Depois, de que ele depende e como calcular, até com integral. E por fim, dois atalhos poderosos: os eixos paralelos e os eixos perpendiculares. No final, três exercícios para firmar tudo.

### A3 · 1:26–1:51 · 25 s · 66 palavras

*Tela (descrição do handoff; quadro não revisto): uma partícula girando num círculo, seta violeta tangente, rótulo ½mv²; ela se multiplica em muitas e os círculos viram o corpo de referência (disco) dividido em pedaços rosa*

[thoughtful] Você já sabe que um ponto de um corpo que gira anda com velocidade igual à velocidade angular vezes a distância ao eixo. E sabe que uma partícula com velocidade v tem energia cinética meio m v ao quadrado. Agora junta as duas ideias: um corpo que gira é uma multidão de partículas, cada uma no seu círculo. Qual é a energia de toda essa multidão?


## T1

### T1-1 · 1:51–2:19 · 28 s · 74 palavras

*Tela (descrição do handoff; quadro não revisto): canto linha 2 QUANTA ENERGIA TEM UM GIRO?; o corpo de referência (disco de aço) dividido em pedaços rosa; cada pedaço i com massa mᵢ (rosa) e distância rᵢ ao eixo (GEO); setas violeta vᵢ crescendo com rᵢ; selo HIPÓTESES: CORPO RÍGIDO · EIXO FIXO*

[thoughtful] Vamos cortar o disco em pedacinhos, tão pequenos que cada um pode ser tratado como uma partícula. O pedaço número i tem massa m i e está a uma distância r i do eixo. Como o corpo é rígido e gira em torno de um eixo fixo, todos os pedaços têm a mesma velocidade angular, mas a velocidade de cada um depende da sua distância: v i é a velocidade angular vezes r i.

### T1-2 · 2:19–2:42 · 23 s · 62 palavras

*Tela (descrição do handoff; quadro não revisto): sobre o pedaço i, ENERGIA DO PEDAÇO: ½ mᵢ vᵢ² (ciano), mᵢ sai do pedaço e vᵢ da seta; CONTA: vᵢ = ω rᵢ → ½ mᵢ (ω rᵢ)² = ½ mᵢ rᵢ² ω²*

[thoughtful] A energia cinética desse pedaço é meio m i vezes v i ao quadrado. Agora troca v i por velocidade angular vezes r i. Fica meio, m i, r i ao quadrado, velocidade angular ao quadrado. Repara onde o r i ao quadrado apareceu: ele vem de a velocidade ser proporcional à distância, e a energia ser proporcional ao quadrado da velocidade.

### T1-3 · 2:42–3:08 · 26 s · 68 palavras

*Tela (descrição do handoff; quadro não revisto): CONTA: K = Σ ½ mᵢ rᵢ² ω² = ½ ( Σ mᵢ rᵢ² ) ω²; o ω² atravessa a soma (destaque: É IGUAL PARA TODOS OS PEDAÇOS); o parêntese acende em rosa; a energia dos pedaços (ciano) soma numa barra única*

[thoughtful] Para achar a energia do corpo todo, soma a de todos os pedaços. E aqui acontece uma coisa linda: a velocidade angular é a mesma para todos, então ela sai da soma. Sobra, dentro do parêntese, a soma de cada massa vezes o quadrado da sua distância ao eixo. Esse parêntese só depende do corpo e de onde está o eixo. Não depende de quão rápido ele gira.

### T1-4 · 3:08–3:30 · 22 s · 59 palavras

*Tela (descrição do handoff; quadro não revisto): CONTA: I = Σ mᵢ rᵢ² [kg·m²]; K = ½ I ω² em PANEL com borda ciano; tabela de tradução montando linha por linha: m ↔ I, v ↔ ω, ½ m v² ↔ ½ I ω²*

[happy] E esse parêntese ganha nome: momento de inércia. A gente escreve I, e a unidade é quilograma vezes metro ao quadrado. A energia cinética de rotação fica meio, momento de inércia, velocidade angular ao quadrado. Olha a tradução: a massa da translação vira o momento de inércia da rotação, a velocidade vira a velocidade angular. Mesma forma, mesma ideia.

### T1-5 · 3:30–4:00 · 29 s · 78 palavras

*Tela (descrição do handoff; quadro não revisto): o corpo ganha um pedaço fora do plano do disco, num pino vertical longe do plano; r_⊥ (GEO tracejado) do eixo até o pedaço, distinto de r⃗ da origem; selo ATENÇÃO: A DISTÂNCIA É AO EIXO; texto pequeno NÃO É ENERGIA NOVA*

[thoughtful] Duas observações. Primeira: isso não é uma energia nova. É a mesma meio m v ao quadrado de sempre, só que somada pedaço por pedaço, e o momento de inércia é o jeito de guardar essa soma. Segunda: o r i que entra na conta é a distância ao eixo, e não a distância até a origem ou até o centro do corpo. Se o pedaço está lá em cima, mas no eixo, ele não contribui com nada.


## T2

### T2-1 · 4:00–4:20 · 20 s · 54 palavras

*Quadros v7: 4:19 · haltere 2 × 2 kg, L = 1 m, quadrados sob cada massa; I = m(L/2)² + m(L/2)² = ½ m L², e a caixa fecha em ½·2·1² = 1 kg·m².*

[thoughtful] Vamos a um corpo simples: um haltere. Duas massas iguais, de dois quilos, nas pontas de uma haste leve de um metro. Com o eixo bem no meio, cada massa está a meio metro. A conta é só somar: m vezes meio metro ao quadrado, duas vezes. Dá um quilograma vezes metro ao quadrado.

### T2-2 · 4:20–4:49 · 29 s · 77 palavras

*Quadros v7: 4:47 · eixo na massa da esquerda (r = 0), quadrado grande sob a outra; selo IDEIA CENTRAL: I DEPENDE DO EIXO; I = m·0² + mL² = 2 kg·m².*

[excited] Agora o eixo passa por uma das massas. Mesmo haltere, mesmas massas. Uma massa fica em cima do eixo e não conta. A outra fica a um metro, e o quadrado dela é enorme. O resultado é dois quilogramas vezes metro ao quadrado: o dobro. E essa é a ideia mais importante do vídeo: o momento de inércia não é uma propriedade do objeto sozinho. É uma propriedade da distribuição de massa em relação a um eixo.

### T2-3 · 4:49–5:07 · 18 s · 47 palavras

*Quadros v7: 5:06 · parábola m r², pontos 1 kg a 0,2 m e 0,25 kg a 0,4 m (ambos 0,04 kg·m²), seta r → 2r: ×4.*

[thoughtful] E repara no quadrado. Se você afasta uma massa do eixo para o dobro da distância, a contribuição dela quadruplica. Uma massa pequena, longe do eixo, pode pesar tanto quanto uma massa grande, perto. Um quarto da massa, no dobro da distância, dá exatamente a mesma contribuição.

### T2-4 · 5:07–5:31 · 24 s · 62 palavras · **TEXTO MUDOU**

*Quadros v7: M = 4 kg no anel, I = M k², k = √(I/M) = √(1/4) = 0,5 m = L/2; cartão PERGUNTA 'qual é o raio de giração de um corpo inteiro?'.*

[thoughtful] Dá para resumir um corpo com um número de comprimento. O raio de giração é a distância em que, concentrando toda a massa num anel fino, teríamos o mesmo momento de inércia. Escreve I igual a massa total vezes k ao quadrado. No haltere são quatro quilos e I igual a um, então k é a raiz de um quarto: meio metro.


## T3

### T3-1 · 5:31–5:56 · 25 s · 65 palavras

*Tela (descrição do handoff; quadro não revisto): canto linha 2 E QUANDO A MASSA É CONTÍNUA?; barra de aço de comprimento L fatiada em fatias dx; cada fatia com dm = λ dx (rosa); CONTA: I = Σ mᵢ rᵢ² → ∫ r² dm; λ = M/L*

[thoughtful] Mas quase nenhum corpo real é um punhado de bolinhas. A massa é contínua. Então a soma vira integral: a gente fatia o corpo em pedaços de massa d m e soma r ao quadrado vezes d m. Numa barra fina, a massa por comprimento é a massa total dividida pelo comprimento, e cada fatia de largura d x tem massa lambda vezes d x.

### T3-2 · 5:56–6:21 · 25 s · 66 palavras

*Tela (descrição do handoff; quadro não revisto): eixo na ponta da barra; fatias com brilho ∝ x², a mais distante a mais brilhante; gráfico x² ao lado com a área enchendo; CONTA: I = ∫₀ᴸ x² (M/L) dx = (M/L)(L³/3) = ML²/3*

[thoughtful] Eixo na ponta da barra. A fatia que está a uma distância x contribui com x ao quadrado vezes lambda d x. Integra de zero até L. A integral de x ao quadrado é x ao cubo sobre três, e sobra a massa vezes o comprimento ao quadrado sobre três. Olha o brilho das fatias: as de longe dominam a conta, porque o quadrado cresce rápido.

### T3-3 · 6:21–6:48 · 28 s · 72 palavras

*Tela (descrição do handoff; quadro não revisto): eixo no centro da barra; fatias dos dois lados; CONTA: I = ∫₋ᴸ/₂^ᴸ/₂ x² (M/L) dx = ML²/12; selo QUATRO VEZES MENOR; a barra se parte em duas meias-barras, cada uma de massa M/2 e comprimento L/2 girando pela ponta*

[excited] Agora o eixo no centro. Os limites vão de menos L meio a mais L meio, e dá a massa vezes L ao quadrado sobre doze. Quatro vezes menor que pela ponta. E dá para enxergar o porquê sem integral: pelo centro são duas meias-barras, cada uma com metade da massa e metade do comprimento, girando pela ponta. Metade da massa, um quarto do quadrado do comprimento, vezes dois: um doze avos.

### T3-4 · 6:48–7:12 · 23 s · 61 palavras

*Tela (descrição do handoff; quadro não revisto): as duas barras lado a lado com os valores para a barra uniforme de 0,90 kg e 0,84 m: pela ponta 0,212 kg·m², pelo centro 0,053 kg·m²; selo MESMA BARRA, DOIS EIXOS, OUTRO I*

[thoughtful] Com a barra uniforme do nosso bastão, de nove décimos de quilo e oitenta e quatro centímetros, o momento de inércia pela ponta seria duzentos e doze gramas-metro quadrado, e pelo centro, cinquenta e três. A mesma barra, dois eixos, e um fator quatro. Guarda esses números: o nosso bastão de verdade não é uniforme, e a gente vai voltar nele.


## T4

### T4-1 · 7:12–7:31 · 19 s · 53 palavras · **TEXTO MUDOU**

*Quadros v7: cartão PERGUNTA 'e um aro, com toda a massa na borda?'; pontos rosa em volta do aro, R tracejado, I = Σ mᵢR² = (Σ mᵢ)R² = M R².*

[thoughtful] Vamos juntar uma tabela de formas. E se o corpo é um aro, com toda a massa na borda? Cada pedaço está à mesma distância R, então a soma de m i R ao quadrado é R ao quadrado vezes a soma das massas. Sem integral: I igual a M R ao quadrado.

### T4-2 · 7:31–7:57 · 25 s · 67 palavras

*Quadros v7: 7:55 · disco em anéis, um anel rosa destacado, dm = σ 2πr dr; σ = M/πR²; integral até ½ M R².*

[thoughtful] Agora o disco maciço. Corta em anéis finos, como as camadas de uma cebola. Um anel de raio r e largura d r tem área dois pi r d r, e massa a densidade por área vezes essa área. Cada anel é um aro, então contribui com r ao quadrado vezes sua massa. Integra de zero até R, e o resultado é meio M R ao quadrado.

### T4-3 · 7:57–8:14 · 17 s · 49 palavras · **TEXTO MUDOU**

*Quadros v7: aro e disco lado a lado; o disco mostra um círculo tracejado rosa rotulado METADE DA MASSA; selo O DOBRO: O ARO TEM O DOBRO; I_aro = M R², I_disco = ½ M R². (A metade da massa fica dentro de r = R/√2; a fala usa a ideia sem citar o número.)*

[excited] Compara. Mesma massa, mesmo raio: o aro tem o dobro do momento de inércia do disco. No disco, metade da massa cabe dentro do círculo tracejado, perto do eixo, onde o quadrado da distância é pequeno. No aro, toda a massa está na borda, onde o quadrado pesa mais.

### T4-4 · 8:14–8:47 · 33 s · 89 palavras

*Quadros v7: 8:45 · esfera em discos empilhados, disco rosa na altura z com raio √(R²−z²); dm, dI, ρ = M/(4/3 πR³), integral e I = ⅖ M R².*

[thoughtful] Para a esfera maciça, a gente fatia em discos finos, empilhados ao longo do eixo. O disco na altura z tem raio raiz de R ao quadrado menos z ao quadrado, então a massa dele é a densidade vezes pi vezes esse raio ao quadrado vezes d z. E cada disco já sabemos: meio da massa dele vezes o raio ao quadrado. Integra de menos R até R, usando a densidade como a massa total sobre o volume, e o resultado é dois quintos de M R ao quadrado.

### T4-5 · 8:47–9:15 · 28 s · 74 palavras

*Quadros v7: 9:13 · tabela I = c M R² (aro 1 · casca ⅔ · disco ½ · esfera ⅖) e linha da barra ML²/12 centro · ML²/3 ponta; selo CORPOS HOMOGÊNEOS · EIXO DE SIMETRIA.*

[thoughtful] Esses números formam uma tabela que vale a pena guardar. Todos assumem corpos homogêneos e o eixo de simetria. E o aro e a casca esférica são de parede fina; se a parede for grossa, o número é outro. O fator na frente do M R ao quadrado só depende da forma: quanto mais massa perto do eixo, menor ele é. A barra fica numa linha separada porque usa o comprimento, não o raio.


## T5

### T5-1 · 9:15–9:35 · 20 s · 53 palavras

*Quadros v7: 9:34 · barra com d = L/2, I_centro = ML²/12, I_ponta = ML²/3, diferença M(L/2)²; barra rosa de I.*

[curious] E se o eixo não passa pelo centro do corpo? Lembra da barra: pelo centro, um doze avos; pela ponta, um terço. A diferença é um quarto de M L ao quadrado, que é exatamente a massa vezes o quadrado da distância entre os dois eixos. Será coincidência? Não. Vale para qualquer corpo.

### T5-2 · 9:35–10:00 · 25 s · 65 palavras

*Quadros v7: 9:58 · placa irregular com CM (ponto branco), O à esquerda, r⃗ᵢ = r⃗′ᵢ + d⃗, rᵢ² = r′ᵢ² + 2d⃗·r⃗′ᵢ + d²; cartão PERGUNTA sobre eixo fora do CM.*

[thoughtful] Pega um corpo qualquer e um eixo pelo centro de massa. Agora um segundo eixo, paralelo, a uma distância d. Para um pedaço i, a posição vista do segundo eixo é a posição vista do centro de massa mais o vetor d. Eleva ao quadrado: r i ao quadrado é r linha ao quadrado, mais duas vezes d escalar r linha, mais d ao quadrado.

### T5-3 · 10:00–10:31 · 31 s · 92 palavras · **TEXTO MUDOU**

*Quadros v7: à esquerda, polígono fechado de setas laranja (os r⃗′ᵢ somando zero) com Σ mᵢ r⃗′ᵢ = 0⃗; cartão POR QUÊ? O CM, VISTO DE SI MESMO, ESTÁ NA ORIGEM; o termo do meio é riscado; I = I_cm + M d² em PANEL.*

[excited] Agora multiplica por m i e soma. O primeiro termo é o momento de inércia em torno do centro de massa. O último é a massa total vezes d ao quadrado. E o do meio? Dentro do parêntese tem a soma de m i vezes r linha, que é a massa total vezes a posição do centro de massa, vista do próprio centro de massa. Zero: os vetores se compensam, como no polígono fechado da esquerda. O termo cruzado desaparece, e fica: I igual a I cm mais M d ao quadrado.

### T5-4 · 10:31–11:06 · 36 s · 95 palavras

*Quadros v7: 11:04 · placa girando em O, v_cm = ωd, barras K (CM + GIRO) e I (Md² + I_cm); selo A MESMA ENERGIA LIDA DE DOIS JEITOS; K = ½Mv²cm + ½I_cm ω² = ½ I_O ω².*

[thoughtful] Tem uma segunda leitura, que é pura energia. Com o eixo fixo, o centro de massa anda num círculo de raio d, com velocidade ω d. A energia do corpo é a do centro de massa andando, meio M v cm ao quadrado, mais a do giro em torno do centro de massa, meio I cm ômega ao quadrado. Substitui, e aparece meio vezes I cm mais M d ao quadrado, vezes ômega ao quadrado. Mas a energia em torno do eixo fixo é meio I vezes ômega ao quadrado. Comparando, sai o mesmo teorema.

### T5-5 · 11:06–11:38 · 32 s · 84 palavras · tag trocada

*Quadros v7: 11:36 · parábola I(d) com mínimo I_cm; I_B = I_A + M d²_AB riscado em vermelho, A E B FORA DO CM: ERRADO; conferência ML²/12 + M(L/2)² = ML²/3 ✓.*

[thoughtful, emphatic] Dois cuidados. Primeiro: o menor momento de inércia, entre todos os eixos paralelos, é o do centro de massa. Afastar o eixo só soma. Segundo, o erro clássico: o teorema vale entre o eixo do centro de massa e outro paralelo. Se você tem o momento de inércia em um eixo qualquer e quer em outro, não pode simplesmente somar M d ao quadrado: volta primeiro ao centro de massa. E a conferência: a barra, um doze avos mais um quarto, dá um terço.

### T5-6 · 11:38–12:35 · 57 s · 151 palavras

*Quadros v7: 12:30 · bastão: cabo 0,25 kg e parte grossa 0,65 kg (0,42 m cada metade), distâncias 0,21 e 0,63 m; I_cabo = 0,282, I_grossa = 0,141, razão 2; 0,63 → 0,21: ÷3 ⇒ d² ÷ 9.*

[excited] Agora dá para voltar ao bastão. Ele tem duas metades de quarenta e dois centímetros: o cabo, de duzentos e cinquenta gramas, e a parte grossa, de seiscentos e cinquenta. A gente calcula cada metade pelo seu centro e soma o termo de eixos paralelos. Com o eixo na ponta do cabo, o centro do cabo está a vinte e um centímetros, e o da parte grossa a sessenta e três. Dá duzentos e oitenta e dois gramas-metro quadrado. Com o eixo na ponta grossa, é o contrário: a parte grossa fica a vinte e um, e o cabo a sessenta e três. Dá cento e quarenta e um. Exatamente a metade. A parte grossa, com quase três quartos da massa, está a sessenta e três centímetros do eixo num caso e a vinte e um no outro: três vezes mais perto, nove vezes menos no quadrado. Esse é o segredo.


## T6

### T6-1 · 12:35–13:01 · 26 s · 69 palavras

*Tela (descrição do handoff; quadro não revisto): canto linha 2 UM ATALHO PARA PLACAS; placa fina no plano xy com os eixos x, y no plano e z saindo dela (GEO); um pedaço em (x, y) com r², x², y² no triângulo retângulo; CONTA: r² = x² + y² → I_z = Σ m r² = Σ m x² + Σ m y²; selo SÓ PARA PLACAS FINAS*

[thoughtful] Um atalho que vale ouro, mas só para placas finas, planas. Coloca a placa no plano x y e o eixo z saindo perpendicular dela. A distância de um pedaço ao eixo z é raiz de x ao quadrado mais y ao quadrado, por Pitágoras. Então r ao quadrado é x ao quadrado mais y ao quadrado, e a soma de m r ao quadrado se divide em duas.

### T6-2 · 13:01–13:29 · 28 s · 74 palavras

*Tela (descrição do handoff; quadro não revisto): a soma de m y² acende junto com o eixo x e a de m x² com o eixo y; CONTA: I_z = I_x + I_y (rosa); na placa, destaque: Σ m y² é o momento de inércia em torno do eixo x (cada pedaço fica a y do eixo x)*

[thoughtful] E repara: a soma de m vezes y ao quadrado é justamente o momento de inércia em torno do eixo x, porque o y de cada pedaço é a distância dele ao eixo x. O mesmo para m x ao quadrado e o eixo y. Então o momento de inércia em torno do eixo perpendicular é a soma dos outros dois. Isso só funciona para placas, onde todo ponto tem z igual a zero.

### T6-3 · 13:29–13:52 · 23 s · 62 palavras

*Tela (descrição do handoff; quadro não revisto): disco fino com os eixos x e y no diâmetro e z perpendicular; CONTA: por simetria I_x = I_y → 2 I_x = ½ M R² → I_diâmetro = ¼ M R²; ao lado, aro: M R² → ½ M R²; selo SEM INTEGRAL*

[excited] Olha o prêmio. No disco, os eixos x e y no diâmetro são equivalentes, por simetria. Então os dois momentos de inércia são iguais, e a soma deles é o do eixo perpendicular: meio M R ao quadrado. Cada um vale um quarto de M R ao quadrado. Sem nenhuma integral. E no aro, pelo diâmetro, dá meio M R ao quadrado.

### T6-4 · 13:52–14:34 · 42 s · 112 palavras

*Tela (descrição do handoff; quadro não revisto): a esfera do T4-4 com os três eixos x, y, z pelo centro; CONTA: I_x + I_y + I_z = 2 ∫ r² dm; esfera: I = ⅔ ∫ r² dm; casca fina: I = ⅔ M R²; maciça: ∫ r² dm = ⅗ M R² → I = ⅔·⅗ M R² = ⅖ M R²*

[thoughtful] E dá para usar a mesma ideia na esfera, como uma conferência independente. Somando os três momentos de inércia, cada ponto contribui com y ao quadrado mais z ao quadrado, mais x ao quadrado mais z ao quadrado, mais x ao quadrado mais y ao quadrado: duas vezes r ao quadrado, com r a distância ao centro. Na esfera, os três são iguais, então I é dois terços da integral de r ao quadrado d m. Na casca fina, r é R: dois terços de M R ao quadrado. Na maciça, a integral dá três quintos, e dois terços de três quintos é dois quintos. Duas contas completamente diferentes, o mesmo resultado.


## E1

### E1-1 · 14:34–14:58 · 24 s · 63 palavras

*Tela (descrição do handoff; quadro não revisto): canto linha 2 EXERCÍCIO 1 · O BLOCO E O CARRETEL; ESQUEMA fixo à esquerda: carretel (disco de aço, M = 2,0 kg, R = 0,10 m) com eixo fixo sem atrito e corda leve enrolada; bloco m = 1,0 kg pendurado, h = 1,0 m indicada (GEO); barras de energia ao lado; selo O QUE ESTE PEDE: v DO BLOCO APÓS DESCER 1,0 m; HIPÓTESES: CORDA NÃO ESCORREGA · SAI DO REPOUSO*

[thoughtful] Primeiro exercício. Um carretel, que a gente vai tratar como um disco maciço de dois quilos e dez centímetros de raio, gira em torno de um eixo fixo, sem atrito. Uma corda leve está enrolada nele, e na ponta tem um bloco de um quilo. Solta do repouso. Qual é a velocidade do bloco depois de descer um metro? A corda não escorrega.

### E1-2 · 14:58–15:16 · 18 s · 47 palavras

*Tela (descrição do handoff; quadro não revisto): CONTA: ENERGIA: m g h = ½ m v² + ½ I ω²; dos rótulos: m g h (ciano), ½ m v², ½ I ω²; selo CONDIÇÃO: v = ω R (CORDA NÃO ESCORREGA)*

[thoughtful] Aqui a energia resolve rápido. A energia potencial que o bloco perde vira dois pedaços de energia cinética: a do bloco, que desce, e a do carretel, que gira. E a corda não escorrega, então a velocidade do bloco é igual à velocidade angular vezes o raio.

### E1-3 · 15:16–15:44 · 28 s · 73 palavras

*Tela (descrição do handoff; quadro não revisto): CONTA: I = ½ M R² (disco); ½ I ω² = ½ (½ M R²)(v/R)² = ¼ M v²; o R se cancela com risco; m g h = ½ m v² + ¼ M v² = ½ (m + M/2) v²*

[excited] O momento de inércia do disco é meio M R ao quadrado. E ômega é v sobre R. Quando você substitui, o R ao quadrado do momento de inércia cancela o R ao quadrado do denominador, e a energia do carretel vira um quarto de M v ao quadrado. Olha que bonito: o raio sumiu. É como se o carretel fosse uma massa extra, de M sobre dois, andando junto com o bloco.

### E1-4 · 15:44–16:04 · 20 s · 53 palavras

*Tela (descrição do handoff; quadro não revisto): CONTA: v = √( 2 m g h / (m + M/2) ) = √( 2·1,0·9,8·1,0 / 2,0 ) = 3,13 m/s (violeta); ω = v/R = 31,3 rad/s; câmera lenta no carretel com selo CÂMERA LENTA ×4*

[thoughtful] Agora só substituir: duas vezes um, vezes nove vírgula oito, vezes um, dividido por dois. Isso dá três vírgula treze metros por segundo. A velocidade angular do carretel é essa velocidade dividida por zero vírgula um metro: trinta e um vírgula três radianos por segundo. Por isso a animação está em câmera lenta.

### E1-5 · 16:04–16:33 · 30 s · 79 palavras

*Tela (descrição do handoff; quadro não revisto): barras de energia: total 9,8 J; bloco 4,9 J e carretel 4,9 J (metade e metade, ciano); ao lado, queda livre de 1 m: 4,43 m/s; selo CONFERE: A SOMA DAS BARRAS É m g h*

[thoughtful] Para conferir, olha a divisão da energia. De nove vírgula oito joules disponíveis, quatro vírgula nove vão para o bloco e quatro vírgula nove para o carretel. Metade e metade, e isso não é coincidência: o carretel conta como M sobre dois, que aqui é um quilo, igual à massa do bloco. E o bloco desce a três vírgula treze, menos que os quatro vírgula quarenta e três de uma queda livre, porque parte da energia ficou no giro.

### E1-6 · 16:33–17:02 · 29 s · 76 palavras

*Tela (descrição do handoff; quadro não revisto): o carretel é trocado por um aro de mesma massa e raio; CONTA: I = M R² → v = √( 2 m g h / (m + M) ) = 2,56 m/s; selo DICA: CORDA SEM ESCORREGAR ⇒ ESCREVA TUDO EM v; I/R² VIRA UMA MASSA EXTRA*

[thoughtful] Uma pergunta para fixar: e se o carretel fosse um aro, de mesma massa e mesmo raio? O momento de inércia dobra, o carretel passa a valer uma massa extra de M inteira, e o bloco desce a dois vírgula cinquenta e seis. Fica a dica: quando uma corda não escorrega, escreve tudo em termos de v, e trata o momento de inércia dividido pelo raio ao quadrado como uma massa extra somada à do bloco.


## E2

### E2-1 · 17:02–17:26 · 24 s · 64 palavras

*Tela (descrição do handoff; quadro não revisto): canto linha 2 EXERCÍCIO 2 · A HASTE QUE TOMBA; ESQUEMA fixo à esquerda: haste uniforme de L = 1,0 m articulada no chão (pino), quase vertical; ponto L/2 do CM e ponta marcados; selo O QUE ESTE PEDE: VELOCIDADE DA PONTA AO CHEGAR NA HORIZONTAL; HIPÓTESES: SAI DO REPOUSO · PINO SEM ATRITO*

[curious] Segundo exercício. Uma haste uniforme de um metro está em pé, articulada na base por um pino sem atrito. Dá um tiquinho de empurrão e ela tomba, sem escorregar na base. Qual é a velocidade da ponta quando a haste bate na horizontal? E a pergunta de bônus: essa ponta chega mais rápido ou mais devagar do que uma pedra solta da mesma altura?

### E2-2 · 17:26–17:48 · 22 s · 58 palavras

*Tela (descrição do handoff; quadro não revisto): CONTA: ENERGIA: o CM desce L/2 → M g L/2 = ½ I ω²; I = ML²/3 (eixo no pino, extremo da barra); selo DICA: ENERGIA POTENCIAL É A DO CM; CINÉTICA, A DO GIRO EM TORNO DO PINO*

[thoughtful] A energia potencial que a haste perde é a do centro de massa, que desce meio comprimento: M g L sobre dois. Ela vira energia de rotação em torno do pino. E o momento de inércia em torno do pino é o da barra pela ponta, M L ao quadrado sobre três, que a gente calculou no começo.

### E2-3 · 17:48–18:11 · 23 s · 61 palavras

*Tela (descrição do handoff; quadro não revisto): CONTA: M g L/2 = ½ (ML²/3) ω² → ω = √(3g/L) = 5,42 rad/s; v_ponta = ω L = √(3 g L) = 5,42 m/s (violeta); ao lado, pedra em queda livre de 1 m: √(2 g L) = 4,43 m/s*

[excited] Cancela a massa, e a velocidade angular é raiz de três g sobre L: cinco vírgula quarenta e dois radianos por segundo. A ponta anda ômega vezes L, ou seja, cinco vírgula quarenta e dois metros por segundo. Uma pedra solta de um metro chega com quatro vírgula quarenta e três. A ponta da haste chega mais rápido que a pedra.

### E2-4 · 18:11–18:33 · 22 s · 57 palavras

*Tela (descrição do handoff; quadro não revisto): gráfico da velocidade final de cada ponto da haste em função da distância r ao pino: reta ω r (violeta) cruzando a curva √(2 g r) da queda livre da altura r; cruzamento marcado em r = 2L/3; CONTA: ω r = √(2 g r) → r = 2L/3*

[thoughtful] E tem um ponto especial. Se a gente compara cada ponto da haste com uma pedra solta da altura dele, só o ponto que está a dois terços do comprimento chega igualzinho à pedra. Acima disso, o ponto ganha da queda livre. Abaixo, perde. É a velocidade crescendo linearmente com a distância ao pino, contra uma raiz.

### E2-5 · 18:33–18:52 · 19 s · 50 palavras · tag trocada

*Tela (descrição do handoff; quadro não revisto): selo CUIDADO: VELOCIDADE FINAL, NÃO TEMPO DE QUEDA; texto pequeno O PINO EXERCE FORÇA: A HASTE NÃO ESTÁ EM QUEDA LIVRE*

[thoughtful, emphatic] Cuidado com o que isso quer dizer. A gente comparou velocidades finais, não tempos de queda. E a haste não está em queda livre: o pino empurra, e isso muda o movimento de cada ponto. Só a energia, que a gente usou, ignora esses detalhes e entrega o resultado final.

### E2-6 · 18:52–19:19 · 27 s · 72 palavras

*Tela (descrição do handoff; quadro não revisto): uma bola de mesma massa M presa na ponta; CONTA: I = ML²/3 + ML² = 4ML²/3; energia disponível: M g L/2 + M g L = 3/2 M g L; ω² = 9g/(4L) → v_ponta = 3/2 √(g L) = 4,70 m/s; selo MAIS MASSA NA PONTA, PONTA MAIS LENTA*

[thoughtful] Última variação: prende uma bola de mesma massa na ponta. O momento de inércia vai de um terço para quatro terços de M L ao quadrado. A energia disponível sobe de meio para três meios de M g L. Resultado: a ponta chega a quatro vírgula setenta metros por segundo, menor que antes, ainda maior que a queda livre. Mais massa na ponta aumentou a energia, mas aumentou ainda mais a inércia.


## E3

### E3-1 · 19:19–19:55 · 36 s · 96 palavras

*Tela (descrição do handoff; quadro não revisto): canto linha 2 EXERCÍCIO 3 · A PLACA COM RECORTE; ESQUEMA fixo à esquerda: disco de raio R = 0,30 m do qual foi retirado um disco de raio R/2 com centro a R/2 de O, tangente à borda externa e passando por O; massa que sobrou M = 1,5 kg (o disco inteiro teria M₀ = 2,0 kg; o recorte retirou 0,5 kg); eixo horizontal em O, perpendicular à placa; posição inicial: segmento O–CM na horizontal; selo O QUE ESTE PEDE: VELOCIDADE ANGULAR QUANDO O CM PASSA ABAIXO DE O*

[curious] Terceiro exercício, o mais completo. Uma placa circular de trinta centímetros de raio, da qual a gente tirou um recorte circular com metade do raio, encostado na borda e passando pelo centro O. A placa que sobrou tem um quilo e meio, mas o disco inteiro teria dois quilos. O eixo é horizontal, perpendicular à placa, passando por O. A gente solta de uma posição em que a linha do centro de massa até O está na horizontal. Qual é a velocidade angular quando o centro de massa passa embaixo de O? Eixo ideal, sem atrito.

### E3-2 · 19:55–20:20 · 25 s · 65 palavras

*Tela (descrição do handoff; quadro não revisto): CONTA: I_O = I_disco inteiro − I_recorte; I_disco = ½ M₀ R² = 0,090 kg·m² (massa rosa); o recorte (rosa tracejado) e sua massa M₀/4 = 0,50 kg destacados*

[thoughtful] Plano: o momento de inércia é uma soma, então a gente pode somar com sinal. Momento de inércia do disco inteiro, menos o do pedaço que foi retirado. O disco inteiro, em torno de O, é meio M zero R ao quadrado: zero vírgula zero nove quilogramas metro ao quadrado. O pedaço retirado tem um quarto da área, então um quarto da massa: meio quilo.

### E3-3 · 20:20–20:57 · 38 s · 100 palavras

*Tela (descrição do handoff; quadro não revisto): CONTA (eixos paralelos para o recorte): I_recorte = ½ (M₀/4)(R/2)² + (M₀/4)(R/2)² = 3/32 M₀ R² = 0,0169 kg·m²; I_O = ½ M₀R² − 3/32 M₀R² = 13/32 M₀ R² = 0,0731 kg·m²; também 13/24 M R²; selo DICA: SUBTRAIA I SÓ DEPOIS DE LEVAR TUDO PARA O MESMO EIXO*

[excited] Mas atenção: o momento de inércia do recorte tem que ser em torno de O, e não do centro dele. Então eixos paralelos: o do centro dele, meio m r ao quadrado, mais m d ao quadrado, com a distância de meio R. Dá três trinta e dois avos de M zero R ao quadrado. Tira do disco inteiro, e sobra treze trinta e dois avos de M zero R ao quadrado, ou seja, zero vírgula zero setenta e três quilogramas metro ao quadrado. Em termos da massa que sobrou, treze vinte e quatro avos de M R ao quadrado.

### E3-4 · 20:57–21:19 · 22 s · 58 palavras

*Tela (descrição do handoff; quadro não revisto): CM como ponto branco a R/6 de O no lado oposto ao recorte; CONTA: x_cm = ( M₀·0 − (M₀/4)(R/2) ) / (3M₀/4) = −R/6 = −5 cm; selo MASSA NEGATIVA PARA O RECORTE; o CM aparece no esquema*

[thoughtful] Onde está o centro de massa? A mesma ideia de massa negativa. O disco inteiro tem o centro de massa em O. O recorte, de massa negativa, está a meio R. A média ponderada dá menos R sobre seis: cinco centímetros de O, do lado oposto ao recorte. É essa distância que faz a placa virar um pêndulo.

### E3-5 · 21:19–21:44 · 25 s · 65 palavras

*Tela (descrição do handoff; quadro não revisto): animação: a placa gira de O–CM horizontal até o CM embaixo de O; barras de energia (U → K); CONTA: M g (R/6) = ½ I_O ω² → ω² = 8g/(13R); ω = √( 8·9,8 / (13·0,30) ) = 4,48 rad/s*

[thoughtful] Agora a energia. O centro de massa desce R sobre seis: cinco centímetros. A energia potencial perdida é M g R sobre seis, e vira energia de rotação em torno de O: meio I O ômega ao quadrado. Cancela a massa, e ômega ao quadrado é oito g sobre treze R. Com R de trinta centímetros, dá quatro vírgula quarenta e oito radianos por segundo.

### E3-6 · 21:44–22:12 · 28 s · 75 palavras

*Tela (descrição do handoff; quadro não revisto): números: v_cm = ω R/6 = 0,22 m/s; ponto mais distante: ω R = 1,34 m/s (violeta); I_cm = 37/72 M R² = 0,0694 kg·m² < I_O; selo CONFERE: I_O = I_cm + M (R/6)²*

[thoughtful] O centro de massa passa a vinte e dois centímetros por segundo, e os pontos mais afastados do eixo, a um vírgula trinta e quatro. Conferência: o momento de inércia em torno do próprio centro de massa dá trinta e sete setenta e dois avos de M R ao quadrado, que é menor que o de O. E somando M vezes R sobre seis ao quadrado, volta exatamente ao de O. Os teoremas se fecham.

### E3-7 · 22:12–22:38 · 26 s · 68 palavras · tag trocada

*Tela (descrição do handoff; quadro não revisto): selo DICA: SE O EIXO PASSASSE PELO CM, NADA SE MOVERIA; a mesma placa com o eixo no CM, parada em qualquer posição*

[thoughtful, emphatic] Uma observação final. Se o eixo passasse pelo centro de massa, a energia potencial não mudaria em posição nenhuma, e a placa ficaria parada onde você deixasse. O recorte é o que a transforma num pêndulo. Aqui, o que importa é a combinação: massa negativa para o centro de massa e para o momento de inércia, eixos paralelos para levar tudo ao mesmo eixo, e conservação da energia.


## SÍNTESE

### S1 · 22:38–22:59 · 21 s · 56 palavras

*Tela (descrição do handoff; quadro não revisto): três cartões em PANEL aparecendo um por vez, bordas rosa / ciano / GEO: I = Σ m r² = ∫ r² dm · MOMENTO DE INÉRCIA DEPENDE DO EIXO; K = ½ I ω²; I = I_cm + M d² · I_z = I_x + I_y (PLACAS)*

[happy] Pra fechar, três cartões. Um: o momento de inércia é a soma de cada massa vezes o quadrado da sua distância ao eixo, e muda com o eixo. Dois: a energia cinética de rotação é meio I ômega ao quadrado. Três: dois atalhos, eixos paralelos a partir do centro de massa, e eixos perpendiculares para placas.

### S2 · 22:59–23:30 · 30 s · 81 palavras

*Tela (descrição do handoff; quadro não revisto): o bastão do hook reaparece; a parte grossa sublinhada: a 0,63 m do eixo no cabo, a 0,21 m do eixo na ponta grossa; barras de energia 14,1 J e 7,06 J*

[thoughtful] E a resposta do começo. A parte grossa tem a maior parte da massa do bastão. Com o eixo no cabo, essa massa está a sessenta e três centímetros do eixo. Com o eixo na ponta grossa, a vinte e um. Três vezes mais perto, nove vezes menos no quadrado. É por isso que o mesmo bastão custa o dobro de energia: o momento de inércia dobrou, porque a distribuição de massa em relação ao eixo mudou, e não a massa.


## ENCERRAMENTO

### EN1 · 23:30–23:40 · 10 s · 26 palavras

*Tela (descrição do handoff; quadro não revisto): encerramento padrão (FadeOut geral, self.clear(), logo horizontal com anéis violeta); INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS*

[happy] Se esse vídeo te ajudou, se inscreve no canal para acompanhar os próximos. E fica de olho nos comentários, que eu deixei um desafio para você.

### EN2 · 23:40–23:59 · 20 s · 52 palavras

*Tela (descrição do handoff; quadro não revisto): rampa inclinada com dois cilindros de mesma massa e mesmo raio, um maciço e outro oco de parede fina, partindo juntos do topo; texto DESAFIO: QUEM CHEGA PRIMEIRO, ROLANDO SEM ESCORREGAR?*

[curious] O desafio. Um cilindro maciço e um cilindro oco de parede fina, com a mesma massa e o mesmo raio, descem a mesma rampa rolando sem escorregar. Quem chega primeiro? Usa o fator da tabela, o c, e escreve sua resposta aqui embaixo. A gente vai explorar isso no módulo de rolamento.
