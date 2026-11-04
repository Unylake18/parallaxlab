# yt_0022 (provisório) — Torque e a segunda lei da rotação · roteiro com narração v1.1

> v1.1 (2026-11-03): revisão do GPT da narração v1, trazida pelo Kaio e conferida contra a física. Estrutura, blocos e números preservados; mudam só T4-3, T4-4 e T6-2.
>
> | # | Âncora | Mudança | Situação |
> |---|---|---|---|
> | 1 | T4-3 | a = \|α\|r é a aceleração **tangencial**; ela é a aceleração toda **só no instante da largada**, porque ω = 0 e a centrípeta ω²r ainda é zero | aceito (a v1 falava de "cada ponto tem aceleração igual a…" sem o "no instante") |
> | 2 | T4-4 | mᵢ(\|α\|rᵢ − g) é a **resultante das forças além do peso** sobre a fatia (vizinhos e, na fatia da ponta presa, também a dobradiça), não "a força do resto da régua"; na soma os pares internos se cancelam e sobra a dobradiça, Mg/4 para cima | aceito (o rótulo da v1 confundia as duas coisas; a soma e o número já estavam certos) |
> | 3 | T6-2 | equilíbrio estático é **permanecer** em repouso, não ter velocidade zero num instante; a régua recém-solta tem ω = 0 e α ≠ 0 | aceito (liga o T6 ao hook) |

Data: 2026-11-03. Fase: **roteiro** (sem handoff, voz ou render). Parte da proposta v2 (`rotacao_r3_torque_proposta_v2.md`), com a decisão do Kaio do §9b: **vídeo só de teoria**. Os exercícios (polia que pesa, o que o pino sente, disco que para) vão para o R4.
Título: **Torque: por que a ponta da régua acelera mais que a gravidade?** Mapa: Física I · Rotação · 4.11 (página 1.12), vídeo 3 de 7.
Padrão: `padrao_video_longo.md` §5 e `roteiro_voz_elevenlabs_v4.md`. Tom de professor de cursinho, "a gente" e "você", nunca a letra solta.
Frase-guia: **para girar, não basta força: importa onde e em que direção ela age em relação ao eixo; e Στ = Iα é a segunda lei de Newton somada pedaço por pedaço.**
Duração: ~3.070 palavras ≈ 19 min a 2,7 palavras/s (com os holds visuais, ~19–20 min). A voz real decide; a cena se estica.

**Como ler:** cada `###` é uma âncora (evento visual). A linha `tela:` diz o que aparece; a fala começa ~0,15 s depois e manda. Tags `[ ]` do ElevenLabs v4 em inglês, uma por trecho, valendo até a próxima; não entram na legenda.

**Regras de tela da série:** nada de livro na tela nem na fala (fontes só na descrição); nunca tela só de álgebra; teoria sempre com um desenho 2,5D ou o 3D acontecendo junto; variáveis nascem no desenho e voam para a CONTA; álgebra escrita da esquerda para a direita; selos HIPÓTESES / CONFERE / DICA / ATENÇÃO numa faixa só, um de cada vez; nada de tempo morto; nenhum vídeo citado pelo nome nem como "anterior/próximo" (permitido: "no módulo de rolamento", "no módulo de momento angular", "no módulo de equilíbrio").

**Cores por família (decididas):** torque τ e força F azul-claro `#5AA2FF` (τ desenhado como **arco-seta curva** em volta do eixo no 2D e como vetor ao longo do eixo com arco no 3D; F como seta reta); massa e I rosa `#FF7EB6`; velocidade e ω violeta `#9C8CFF`; aceleração, α e g verde `#3FE08B`; ângulo θ, φ, dθ e arcos âmbar `#FFC24D`; vetor posição r⃗ laranja queimado `#D2823A`; distâncias e geometria (r⊥, L, R, d, linha de ação) `GEO #B8C4DA`; energia, trabalho e potência ciano `#35D9FF`; corpos em aço `#7A8696` com luz B; caixas `PANEL #0E2A52`. **Número substituído herda a cor da grandeza** (100 N·m azul, 14,7 rad/s² verde, 41,9 kW ciano). `=` e `−` brancos.
**Fundo:** céu do laboratório em todas as cenas (`fundo_lab.png`: #0B1A3A → #08122B → #0A1030, estrelas fracas, brilho magenta baixo).
**Canto:** linha 1 `MECÂNICA · TORQUE`; linha 2 = bloco da vez.
**Three.js:** `regua` (H1–H3, T4-1, T4-3, S2), `porta` (T1-1, T1-2, T2-1, T2-2). Tudo o mais em Manim 2,5D.
**Convenção de sinal (dita no T1-4 e usada até o fim):** anti-horário positivo. A régua do hook fica à **direita** da dobradiça e cai no sentido **horário**.

---

## HOOK

### H1 — tela: Three.js, câmera a 3/4 descendo até a vista frontal ao plano da queda e parando ali; mesa de laboratório, régua de metal de 1 m presa por uma dobradiça na beira, estendida para a direita na horizontal, apoiada por um dedo (silhueta 2D) na ponta; duas moedas de aço claro em cima: uma na ponta, outra no meio; rótulos L = 1,0 m (GEO), MOEDA NA PONTA, MOEDA NO MEIO
[curious] Olha esse experimento. Uma régua de um metro, presa numa dobradiça na beira da mesa, segurada na horizontal. Em cima dela, duas moedas: uma bem na ponta, outra no meio. Agora a gente vai tirar o dedo e deixar a régua cair. Pensa rápido: as moedas vão junto com ela?

### H2 — tela: o dedo sai; câmera lenta (selo CÂMERA LENTA ×10) de 0 a 0,15 s; a ponta da régua desce e a moeda da ponta fica "flutuando" acima dela, com a folga crescendo (inset de zoom ×3 na ponta, rótulo da folga em GEO: 5,4 cm em 0,15 s); a moeda do meio continua apoiada; setas verdes de aceleração no instante da largada: na moeda da ponta, g; na ponta da régua, 3g/2, maior; no meio da régua, 0,75 g; selo NO INSTANTE DA LARGADA
[thoughtful] Repara no que acontece. A moeda do meio desce junto com a régua, encostada nela. Mas a moeda da ponta fica para trás: a régua literalmente foge de baixo dela. Em um décimo e meio de segundo já tem mais de cinco centímetros de folga entre as duas. E a moeda, lembra, está caindo em queda livre, com a aceleração da gravidade. Então a ponta da régua está descendo mais depressa do que algo em queda livre.

### H3 — tela: pergunta POR QUE A PONTA DA RÉGUA ACELERA MAIS QUE A GRAVIDADE?, acima da cena congelada; as duas setas verdes da ponta piscam juntas; selo pequeno RÉGUA UNIFORME · MOEDAS LEVES · DOBRADIÇA SEM ATRITO
[curious] E aí fica a pergunta. A régua só está caindo pelo próprio peso. Ninguém está empurrando ela para baixo. Como é que a ponta dela consegue acelerar mais do que a gravidade? Para responder isso, a gente precisa de uma grandeza nova: o torque.

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: TORQUE: POR QUE A PONTA DA RÉGUA ACELERA MAIS QUE A GRAVIDADE?; abaixo, NESTE VÍDEO: e três ícones com rótulo, cada um animando quando citado: porta com seta de força e linha tracejada até a dobradiça (BRAÇO DE ALAVANCA), disco com seta curva azul e seta curva verde (Στ = Iα), roda com arco âmbar varrido e barra ciano (TRABALHO E POTÊNCIA)
[thoughtful] Hoje a gente vai entender o que faz um corpo começar a girar, ou girar mais rápido. Primeiro, por que a posição e a direção da força importam tanto, e o que é o braço de alavanca. Depois, a segunda lei de Newton da rotação, saindo direto da segunda lei que você já conhece. E por fim, trabalho e potência no giro, e o que acontece quando nada acelera.

### A3 — tela: um bloco de aço 2,5D sobre o chão, uma seta azul F empurrando e uma seta verde a no mesmo sentido; CONTA: F = m a; ao lado, o bloco vira um disco de aço preso num eixo; a mesma seta azul empurra a borda e o disco começa a girar; uma interrogação no lugar da equação
[thoughtful] Na translação, a história é simples: força resultante é massa vezes aceleração. Empurra mais forte, acelera mais. Só que agora prende o corpo num eixo. A mesma força, empurrando em lugares diferentes, faz o corpo girar mais, girar menos, ou não girar nada. Então, na rotação, o que faz o papel da força?

## T1 — ONDE EMPURRAR A PORTA?

### T1-1 — tela: canto linha 2 ONDE EMPURRAR A PORTA?; Three.js, porta vista de cima (retângulo de aço com dobradiça à esquerda marcada com eixo GEO, maçaneta à direita); uma seta azul F = 20 N, perpendicular à porta, aplicada primeiro perto da dobradiça (0,15 m) e depois na maçaneta (0,75 m); a porta mal gira no primeiro caso e abre bem no segundo; arco âmbar do giro em cada caso
[curious] Começa com uma coisa que você faz todo dia. Por que a maçaneta fica longe da dobradiça? Experimenta empurrar a porta com a mesma força, vinte newtons, em dois lugares. Perto da dobradiça, a porta quase não se mexe. Lá na maçaneta, ela abre fácil. A força é a mesma. O que mudou foi a distância até o eixo.

### T1-2 — tela: na maçaneta, a seta azul gira em três direções: perpendicular à porta (a porta abre), inclinada a 30° da porta (abre menos), apontando para a dobradiça (nada acontece); a reta suporte da força aparece tracejada em GEO, a LINHA DE AÇÃO; selo FORÇA APONTADA PARA O EIXO NÃO GIRA
[thoughtful] E não é só a distância. Na mesma maçaneta, muda a direção da força. Empurrando perpendicular à porta, ela abre bem. Inclinando a força, abre menos. E se você empurrar apontando para a dobradiça, a porta não gira nada, por mais forte que seja o empurrão. Então importam três coisas: o tamanho da força, a distância ao eixo e o ângulo entre elas.

### T1-3 — tela: a porta vira esquema 2D (aço com luz B) e desliza para a esquerda; do eixo sai o vetor r⃗ (laranja) até o ponto de aplicação; a força F⃗ (azul) com o ângulo φ (âmbar) entre r⃗ e F⃗; duas leituras construídas lado a lado: (1) a linha de ação tracejada e, do eixo até ela, o segmento perpendicular r⊥ (GEO), com a CONTA r⊥ = r sen φ; (2) F decomposta em F∥ (ao longo de r⃗, apagada) e F⊥ (perpendicular a r⃗, cheia), com a CONTA F⊥ = F sen φ; as duas convergem na CONTA τ = r F sen φ = r⊥ F = r F⊥ em PANEL azul
[thoughtful, emphatic] Juntando as três coisas numa grandeza só, a gente chega no torque, que na tela aparece como a letra grega tau. O torque é a distância ao eixo, vezes a força, vezes o seno do ângulo entre as duas. E dá para ler isso de dois jeitos. Primeiro jeito: a distância do eixo até a linha de ação da força, medida na perpendicular, é o braço de alavanca. Torque é força vezes braço de alavanca. Segundo jeito: separa a força em uma parte ao longo da distância e uma parte perpendicular. A parte ao longo só puxa o eixo, não gira nada. Quem gira é a parte perpendicular. É a mesma conta, lida pelos dois lados.

### T1-4 — tela: o esquema da porta com um arco-seta azul anti-horário rotulado + e um horário rotulado −; selo CONVENÇÃO: ANTI-HORÁRIO POSITIVO; CONTA: [τ] = N · m; ao lado, riscado em cinza: J; nota NÃO É ENERGIA
[thoughtful] Dois detalhes antes de seguir. O torque tem sentido: a gente combina que girar no anti-horário é positivo e no horário é negativo, e vai usar isso até o fim do vídeo. E a unidade é newton vezes metro. Repara que newton vezes metro é a mesma combinação do joule, mas torque não é energia. Por isso ninguém escreve joule no torque. O joule vai aparecer daqui a pouco, quando o torque agir ao longo de um ângulo.

### T1-5 — tela: chave de roda 2,5D (aço com luz B) num parafuso de roda; mão em silhueta empurrando a ponta; rótulos 0,40 m (GEO) e 250 N (azul); CONTA: τ = 0,40 · 250 = 100 N · m (azul); a força gira para 30° da chave: τ = 0,40 · 250 · sen 30° = 50 N · m; depois um cano encaixa na chave, o braço vira 0,80 m e a mesma força de 125 N dá os mesmos 100 N · m; selo DICA: PARAFUSO EMPERRADO? AUMENTE O BRAÇO
[curious] Um exemplo de verdade. Você está trocando o pneu e empurra a ponta de uma chave de roda de quarenta centímetros com duzentos e cinquenta newtons, perpendicular à chave. O torque é zero vírgula quatro vezes duzentos e cinquenta: cem newtons metro. Se você empurrar torto, a trinta graus da chave, o seno de trinta é meio, e o torque cai para cinquenta. E aí vem o truque de quem já ficou na estrada: encaixa um cano na chave. Com o braço dobrado, oitenta centímetros, metade da força já dá os mesmos cem newtons metro.

## T2 — O TORQUE É UM VETOR

### T2-1 — tela: canto linha 2 O TORQUE É UM VETOR; Three.js, a porta de novo, câmera orbitando do topo para 3/4 e parando; o Manim prende r⃗ (laranja) e F⃗ (azul) no plano da porta, saindo do mesmo ponto da dobradiça; o paralelogramo de r⃗ e F⃗ se preenche em azul translúcido, com a borda cheia; rótulo ÁREA = r F sen φ
[thoughtful] Até aqui o torque foi um número com sinal. Mas ele é mais do que isso: ele é um vetor. Olha a porta de um ângulo diferente. A distância ao eixo e a força estão no plano da porta. Desenha o paralelogramo que elas formam. A área desse paralelogramo é a base vezes a altura: a distância, vezes a força, vezes o seno do ângulo. Exatamente o tamanho do torque.

### T2-2 — tela: um vetor azul τ⃗ nasce na dobradiça, perpendicular ao plano de r⃗ e F⃗, ao longo do eixo, com o arco-seta do sentido de giro em volta; ícone de mão direita 2D: dedos indo de r⃗ para F⃗, polegar no sentido de τ⃗; CONTA: τ⃗ = r⃗ × F⃗; selo REGRA DA MÃO DIREITA
[thoughtful, emphatic] E a direção do torque é perpendicular a esse paralelogramo, ao longo do eixo de giro. Para achar o sentido, usa a regra da mão direita: os dedos vão da distância para a força, e o polegar aponta o torque. Isso tem nome: produto vetorial. O torque é o vetor posição, cruz, a força.

### T2-3 — tela: no esquema 2D, a força gira em torno do ponto de aplicação: quando fica paralela a r⃗, o paralelogramo achata até sumir e τ⃗ encolhe a zero; depois a ordem dos vetores se inverte (F⃗ primeiro, r⃗ depois) e τ⃗ vira para o outro lado; CONTA: r⃗ × F⃗ = − F⃗ × r⃗ · F⃗ ∥ r⃗ ⇒ τ⃗ = 0⃗
[thoughtful] O paralelogramo explica de uma vez as coisas que a porta mostrou. Força ao longo da distância achata o paralelogramo: área zero, torque zero. E a ordem importa: trocar a ordem do produto inverte a mão, e o torque passa a apontar para o outro lado.

### T2-4 — tela: eixos x e y (GEO) no plano do esquema; r⃗ = (x, y) e F⃗ = (F_x, F_y) com as componentes desenhadas; CONTA: τ_z = x F_y − y F_x; substituição com a chave do T1-5: r⃗ = (0,40; 0) m, F⃗ = (0; 250) N → τ_z = 0,40 · 250 − 0 · 0 = 100 N · m
[curious] E em componentes, como fica? Para movimentos num plano, só sobra a componente do torque perpendicular ao plano, a componente z. Ela é a coordenada x da posição vezes a parte vertical da força, menos a coordenada y vezes a parte horizontal. Testa com a chave de roda: posição de zero vírgula quatro metro no eixo x, força de duzentos e cinquenta newtons para cima. Dá cem newtons metro de novo. A conta vetorial e o braço de alavanca contam a mesma história.

### T2-5 — tela: a chave de roda com a força de 250 N na ponta; dois pontos marcados: o parafuso O e o meio da chave P; o mesmo F⃗ com r⃗ medido a partir de cada um: τ_O = 100 N · m, τ_P = 50 N · m; selo O TORQUE DEPENDE DO PONTO; nota TORQUE EM RELAÇÃO A UM EIXO = COMPONENTE AO LONGO DO EIXO
[thoughtful] Agora um cuidado importante. O torque é sempre calculado em relação a um ponto. A mesma força, medida a partir do parafuso, dá cem newtons metro. Medida a partir do meio da chave, só cinquenta, porque a distância mudou. Então nunca fala "o torque dessa força" sem dizer em relação a quê. E quando o corpo gira preso num eixo, o que interessa é a componente do torque ao longo desse eixo. É ela que vai entrar na segunda lei da rotação.

## T3 — DE NEWTON A Στ = Iα

### T3-1 — tela: canto linha 2 DE NEWTON A Στ = Iα; disco de aço 2,5D preso num eixo fixo (cruz GEO), dividido em pedaços rosa; selo HIPÓTESES: CORPO RÍGIDO · EIXO FIXO · COMPONENTES AO LONGO DO EIXO; o disco começa a acelerar, seta curva violeta ω crescendo e seta curva verde α
[thoughtful] Agora a parte mais importante do vídeo. A gente vai descobrir a lei que diz como o torque muda o giro, sem inventar nada: só usando a segunda lei de Newton. As hipóteses, ditas uma vez: corpo rígido, girando em torno de um eixo fixo, e a gente vai olhar só as componentes dos torques ao longo desse eixo.

### T3-2 — tela: um pedaço i destacado, com massa mᵢ (rosa) a uma distância rᵢ (GEO) do eixo; nele, a força total sobre o pedaço decomposta em componente tangencial F_t,i (azul, cheia) e radial (azul, apagada); a aceleração tangencial a_t,i (verde) no mesmo sentido; CONTA: a_t,i = rᵢ α; F_t,i = mᵢ a_t,i = mᵢ rᵢ α
[thoughtful] Pega um pedacinho do disco, um pedaço qualquer, com a sua massa, a uma certa distância do eixo. Como o corpo inteiro gira junto, todo pedaço tem a mesma aceleração angular. Só que cada um anda num círculo de raio diferente, então a aceleração tangencial desse pedaço é a distância ao eixo vezes a aceleração angular. Agora aplica Newton nesse pedaço, na direção tangente: a força tangencial sobre ele é a massa vezes a aceleração tangencial. Ou seja, massa, vezes distância, vezes aceleração angular.

### T3-3 — tela: o rᵢ voa do desenho e multiplica os dois lados da CONTA; TransformByGlyphMap: rᵢ F_t,i = mᵢ rᵢ² α; o lado esquerdo acende em azul com o rótulo τᵢ (TORQUE NO PEDAÇO) e um arco-seta azul pequeno em volta do eixo, saindo do pedaço; nota: A COMPONENTE RADIAL TEM BRAÇO ZERO
[thoughtful] Agora o truque. Multiplica os dois lados pela distância ao eixo. Do lado esquerdo, fica distância vezes força tangencial: isso é justamente o torque dessa força em relação ao eixo. Do lado direito, aparece massa vezes distância ao quadrado vezes aceleração angular. E a parte radial da força? Ela aponta para o eixo, então o braço dela é zero. Ela só faz o pedaço andar em círculo, não muda o giro.

### T3-4 — tela: CONTA: Σ τᵢ = Σ mᵢ rᵢ² α; todos os pedaços do disco acendem juntos com seus arcos-seta azuis; a soma se divide em duas linhas: Σ τ_ext + Σ τ_int
[curious] Agora soma isso para todos os pedaços do disco. Do lado esquerdo, a soma de todos os torques sobre todos os pedaços. Só que repara: esses torques vêm de dois tipos de força. Tem as forças externas, como o peso ou o empurrão da sua mão. E tem as forças internas, que um pedaço do disco faz no outro para manter tudo rígido. O que acontece com essas internas?

### T3-5 — tela: dois pedaços A e B ligados por uma linha fina; forças internas F⃗_AB e F⃗_BA (azul) de mesmo tamanho, sentidos opostos, sobre a linha que une os dois (rótulo MESMA LINHA DE AÇÃO); do eixo, o mesmo braço r⊥ (GEO) até essa linha comum; arcos-seta azuis iguais e opostos que se apagam juntos; CONTA: τ_AB + τ_BA = 0; selo HIPÓTESE: FORÇAS INTERNAS NA LINHA QUE UNE OS PEDAÇOS; depois o mesmo cancelamento varre o disco inteiro, par por par
[thoughtful, emphatic] Olha um par de pedaços. Pela terceira lei, a força que um faz no outro tem o mesmo tamanho e sentido oposto. E aqui entra uma hipótese que a gente precisa dizer em voz alta: essas forças agem na mesma linha, a linha que une os dois pedaços. Se estão na mesma linha, têm o mesmo braço de alavanca. Mesmo braço, mesma força, sentidos opostos: os torques se cancelam. E isso vale par por par, no disco inteiro. Todos os torques internos somem.

### T3-6 — tela: CONTA, construída: Σ τ_ext,z = ( Σ mᵢ rᵢ² ) α; o parêntese acende em rosa e voa para o rótulo I_z; resultado em PANEL azul/rosa/verde: Σ τ_ext,z = I_z α; ao lado, tabela de tradução montando linha por linha, cada linha nascendo da esquerda: F ↔ τ · m ↔ I · a ↔ α · ΣF = m a ↔ Στ = I α
[excited] E sobra só isto: a soma dos torques externos é igual a esse parêntese vezes a aceleração angular. Só que esse parêntese, a soma de cada massa vezes o quadrado da sua distância ao eixo, é exatamente o momento de inércia! Ele não apareceu porque alguém inventou: ele saiu da própria segunda lei de Newton. Então a segunda lei da rotação é esta: soma dos torques externos igual a momento de inércia vezes aceleração angular. E a tradução fica completa: a força vira torque, a massa vira momento de inércia, a aceleração vira aceleração angular.

### T3-7 — tela: três quadrinhos com selo ATENÇÃO: ONDE VALE: (1) disco em eixo fixo, marcado ✓; (2) roda rolando com eixo pelo centro de massa, que anda junto, marcado ✓ com nota MOVIMENTO PLANO; (3) pião inclinado com o eixo mudando de direção, marcado ✗ com nota PRECISA DE MOMENTO ANGULAR
[thoughtful] Só que toda lei tem o seu domínio, e essa aqui também. Ela vale para eixo fixo, que foi o que a gente demonstrou. Vale também para um eixo que passa pelo centro de massa, mesmo que ele esteja acelerando, desde que o movimento seja num plano e o eixo não mude de direção. Isso a gente usa no módulo de rolamento. Agora, para um pião com o eixo tombando e mudando de direção, essa equação simples não dá conta. Ali precisa do momento angular, que a gente vê no módulo de momento angular.

## T4 — O TORQUE DO PESO

### T4-1 — tela: canto linha 2 O TORQUE DO PESO; a régua do hook volta (Three.js, vista frontal) e vira esquema 2D, horizontal, dobradiça à esquerda; pedaços mᵢ (rosa) com o peso de cada um mᵢ g (azul) e o braço horizontal xᵢ (GEO) até a dobradiça; CONTA: τ_peso = Σ mᵢ g xᵢ = g Σ mᵢ xᵢ = M g x_cm; os pesos pequenos se juntam numa seta única M g saindo do CM (ponto branco com contorno GEO), a L/2
[thoughtful] Agora a gente tem tudo para voltar à régua. Primeiro, qual é o torque do peso dela? Cada pedacinho tem o seu peso, massa vezes gravidade, e o seu braço, que é a distância horizontal até a dobradiça. Somando, a gravidade sai da soma, e sobra a soma de cada massa vezes a sua posição. Só que isso é a massa total vezes a posição do centro de massa! Ou seja: o peso inteiro age como se estivesse concentrado no centro de massa. Na régua uniforme, bem no meio.

### T4-2 — tela: arco-seta azul horário na dobradiça, rotulado com sinal; CONTA, construída com cada letra voando do desenho: τ_z = − M g · L/2 · I = M L²/3 (rosa, rótulo PELA PONTA) · α_z = τ_z / I = − (M g L/2) / (M L²/3) = − 3g / (2L); o M some com risco; selo O SINAL DIZ: GIRA NO HORÁRIO; depois |α| = 3g/(2L) = 14,7 rad/s² (verde) com L = 1,0 m
[thoughtful] Com a régua à direita da dobradiça, o peso faz ela girar no sentido horário, então pela nossa convenção o torque é negativo: menos massa, vezes gravidade, vezes metade do comprimento. O momento de inércia de uma barra uniforme girando pela ponta é um terço da massa vezes o comprimento ao quadrado. Divide um pelo outro. A massa some, e a aceleração angular fica menos três vezes a gravidade sobre duas vezes o comprimento. O sinal só diz que gira no horário. Em tamanho, com um metro de régua, dá catorze vírgula sete radianos por segundo ao quadrado.

### T4-3 — tela: a régua com um eixo r ao longo dela; selo NO INSTANTE DA LARGADA: ω = 0 ⇒ a_c = 0 (a_c = ω² r riscado em cinza); a reta a_t(r) = |α| r em verde subindo da dobradiça até a ponta, com as setinhas verdes verticais para baixo em cada ponto; linha horizontal tracejada g (verde clara) cruzando a reta em r = 2L/3 (marca GEO, rótulo 2L/3 ≈ 67 cm); na ponta, a = |α| L = 3g/2 = 14,7 m/s²; a moeda do meio (a 50 cm, abaixo de 2L/3) e a moeda da ponta (acima) reaparecem nos seus lugares; CONTA: |α| r = g ⇒ r = 2L/3
[excited] E agora a resposta. Atenção: a gente está olhando o instante exato da largada. Nesse momento a régua ainda não tem velocidade angular, então não existe aceleração centrípeta. Toda a aceleração de cada ponto é tangencial, vertical para baixo, e vale a aceleração angular vezes a distância à dobradiça. Na ponta, a um metro, isso dá três meios da gravidade: catorze vírgula sete metros por segundo ao quadrado. Mais do que os nove vírgula oito da moeda em queda livre! E qual ponto desce exatamente com a gravidade? Iguala aceleração angular vezes distância à gravidade: dá dois terços do comprimento, uns sessenta e sete centímetros. A moeda do meio está antes disso, onde a régua desce mais devagar que a gravidade, por isso fica apoiada. A moeda da ponta está depois, e fica para trás.

### T4-4 — tela: a régua em fatias; sobre cada fatia, uma seta azul da RESULTANTE DAS FORÇAS ALÉM DO PESO, mᵢ(|α| rᵢ − g) (positivo para baixo): para cima perto da dobradiça, encolhendo, zero em 2L/3, para baixo e crescendo até a ponta; rótulos SEGURADA PELOS VIZINHOS e PUXADA PELOS VIZINHOS; na fatia presa à dobradiça, a seta se divide em duas partes, VIZINHOS e DOBRADIÇA; na soma, os pares internos entre fatias vizinhas aparecem como setas opostas e se apagam juntos, sobrando só a parte da dobradiça, para cima; CONTA: Σ mᵢ (|α| rᵢ − g) = M (3g/4 − g) = − M g/4 ⇒ DOBRADIÇA: M g/4 PARA CIMA; selo NÃO HÁ NADA VIOLANDO A GRAVIDADE
[thoughtful, emphatic] Mas, espera aí: quem puxa a ponta para baixo mais forte que a gravidade? Olha cada fatia. Ela precisa descer com a aceleração que a rotação manda, só que o peso dela sozinho só daria a gravidade. Então sobre cada fatia tem uma força a mais, além do peso, que é a diferença. Quem faz essa força são as fatias vizinhas, e, na fatia presa, também a dobradiça. Perto da dobradiça, essa força segura a fatia, para ela descer mais devagar. Depois dos dois terços, ela puxa a fatia para baixo. Agora soma tudo: as forças entre fatias vizinhas se cancelam aos pares, e sobra só a dobradiça, segurando um quarto do peso. Então não há nada violando a gravidade. A ponta da régua não está em queda livre: o caminho dela é imposto pela rigidez e pela dobradiça.

### T4-5 — tela: lado a lado, 2,5D: um cabo de vassoura de 1,2 m e um lápis de 15 cm, cada um em pé apoiado num dedo (silhueta), ambos inclinados do mesmo ângulo pequeno; CONTA: α = 3g sen θ / (2L) ⇒ α ∝ 1/L; α_lápis / α_vassoura = 1,2 / 0,15 = 8; os dois tombam juntos e um relógio ao lado de cada: o lápis cai em um tempo √8 ≈ 2,8 vezes menor; selo TEMPO ∝ √L
[curious] E essa mesma conta explica uma coisa que você já tentou fazer. Por que equilibrar um cabo de vassoura em pé na mão é fácil, e um lápis é quase impossível? Tratando os dois como hastes apoiadas na ponta, a aceleração angular é proporcional a um sobre o comprimento. O lápis é oito vezes mais curto, então, no mesmo ângulo, ele gira com aceleração angular oito vezes maior. E o tombo inteiro acontece num tempo umas duas vírgula oito vezes menor, a raiz de oito. Com a vassoura, a sua mão tem tempo de corrigir. Com o lápis, não.

## T5 — TRABALHO E POTÊNCIA NO GIRO

### T5-1 — tela: canto linha 2 TRABALHO E POTÊNCIA NO GIRO; roda de aço 2,5D num eixo; uma força tangencial F_t (azul) empurrando a borda; a roda gira um ângulo dθ (arco âmbar) e a borda anda ds = R dθ (GEO); CONTA: dW = F_t ds = F_t R dθ = τ dθ (ciano); W = ∫ τ dθ; nota: N · m · rad = J
[thoughtful] Agora, o torque e a energia. Empurra a borda de uma roda com uma força tangencial. Quando a roda gira um ângulo pequenininho, a borda anda o raio vezes esse ângulo. O trabalho da força é força vezes deslocamento: força tangencial, vezes raio, vezes o ângulo. Só que força tangencial vezes raio é o torque. Então o trabalho é o torque vezes o ângulo. E para um giro grande, é a integral do torque em relação ao ângulo. Aqui sim aparece o joule.

### T5-2 — tela: gráfico τ(θ) ao lado da roda; a área sob a curva enche em ciano enquanto a roda gira; CONTA, construída: τ = I α = I (dω/dt) = I ω (dω/dθ) → ∫ τ dθ = ∫ I ω dω = ½ I ω_f² − ½ I ω_i² (ciano); selo CONFERE: É A MESMA ENERGIA DE ROTAÇÃO
[thoughtful] E dá para conferir que isso bate com a energia de rotação. Troca o torque por momento de inércia vezes aceleração angular. A aceleração angular é a variação da velocidade angular no tempo, que dá para escrever como velocidade angular vezes a variação dela por ângulo. Integrando, sai meio, momento de inércia, velocidade angular final ao quadrado, menos o mesmo com a inicial. A energia cinética de rotação, que vinha de somar meia massa vezes velocidade ao quadrado de cada pedaço, agora sai da força. As duas descrições contam a mesma história.

### T5-3 — tela: CONTA: P = dW/dt = τ dθ/dt = τ ω; ao lado, um motor 2,5D com o eixo girando: rótulos 100 N · m (azul) e 4.000 RPM → 418,9 rad/s (violeta); duas barras multiplicando numa barra ciano: P = 100 · 418,9 ≈ 41,9 kW ≈ 57 cv; selo NÚMEROS TÍPICOS
[curious] E a potência? É o trabalho por tempo: torque vezes ângulo por tempo, ou seja, torque vezes velocidade angular. É o força vezes velocidade da rotação. Um motor pequeno de carro, com números típicos, dá uns cem newtons metro a quatro mil rotações por minuto. Quatro mil rotações por minuto são uns quatrocentos e dezenove radianos por segundo. Multiplica: quase quarenta e dois quilowatts, uns cinquenta e sete cavalos.

### T5-4 — tela: duas engrenagens 2,5D engrenadas, a pequena no motor e a grande na roda (razão 3 : 1); na pequena, ω alto (violeta grande) e τ pequeno (azul curto); na grande, ω/3 e 3τ; a barra ciano de potência igual nas duas; selo MESMA POTÊNCIA (SEM PERDAS); rótulos MARCHA BAIXA: MUITO TORQUE, POUCO GIRO
[thoughtful] E aí entra o câmbio. Com a mesma potência, se uma engrenagem reduz a rotação três vezes, ela multiplica o torque três vezes, desprezando as perdas. É por isso que a primeira marcha arranca o carro e sobe ladeira: muito torque na roda, pouca rotação. Na marcha alta é o contrário: pouco torque, muita rotação.

## T6 — QUANDO NADA ACELERA

### T6-1 — tela: canto linha 2 QUANDO NADA ACELERA; disco de aço 2,5D **deitado, eixo vertical, visto de cima** (o peso não faz torque em torno do eixo), com o CM marcado fora do eixo (furo de um lado), girando com ω constante (seta curva violeta de tamanho fixo); α = 0 (verde, riscado); o CM descreve um círculo e uma seta azul ΣF⃗ = M a⃗_cm aponta do CM para o eixo, girando junto; rótulo MANCAL; CONTA: α = 0 ⇒ Σ τ_z = 0, MAS Σ F⃗ ≠ 0⃗
[curious] E se nada estiver acelerando o giro? Cuidado com uma armadilha aqui. Pensa num disco deitado, girando em torno de um eixo vertical, com o centro de massa fora do eixo, e com velocidade angular constante. A aceleração angular é zero, então a soma dos torques ao longo do eixo é zero. Mas o centro de massa está andando em círculo. Ele tem aceleração centrípeta, e alguém faz essa força: o mancal, puxando para o eixo. Então girar com velocidade angular constante não quer dizer força resultante zero.

### T6-2 — tela: o disco para; selo EQUILÍBRIO ESTÁTICO = CONTINUA PARADO; inset pequeno da régua recém-solta com ω = 0 (violeta) e α ≠ 0 (verde), rótulo PARADA NUM INSTANTE ≠ EQUILÍBRIO; CONTA em PANEL: Σ F⃗ = 0⃗ e Σ τ⃗ = 0⃗; depois, construída: τ⃗_P′ = τ⃗_P + (r⃗_P − r⃗_P′) × Σ F⃗, o termo do produto acende e vai a zero por TransformByGlyphMap quando ΣF⃗ = 0⃗; rótulo QUALQUER PONTO SERVE
[thoughtful, emphatic] O caso em que as duas coisas valem juntas é o equilíbrio estático. E repara: equilíbrio estático quer dizer que o corpo continua parado, e não só que a velocidade dele é zero num instante. A régua, no instante em que você solta, tem velocidade angular zero, mas já tem aceleração angular. Para continuar parado, a força resultante e o torque resultante precisam ser zero. E aqui tem um presente: se a força resultante é zero, o torque total não depende do ponto que você escolhe. Trocando o ponto, aparece um termo extra, que é um vetor cruz a força resultante. Força resultante zero, termo extra zero. Qualquer ponto serve.

### T6-3 — tela: gangorra 2,5D com o apoio no meio; à esquerda, uma criança (silhueta) de 30 kg a 1,5 m (rosa, GEO); à direita, um adulto de 45 kg a 1,0 m; CONTA com o ponto no apoio: 30 · g · 1,5 = 45 · g · 1,0 (o g some com risco); a força do apoio sai da conta com o selo BRAÇO ZERO; depois, de ΣF = 0: N = (30 + 45) g ≈ 735 N (azul); selo DICA: ESCOLHA O PONTO ONDE ESTÁ A FORÇA QUE VOCÊ NÃO CONHECE
[thoughtful] E isso vira uma dica poderosa. Escolhe o ponto onde está a força que você não conhece: o braço dela é zero e ela some da equação. Na gangorra, pega o próprio apoio. Uma criança de trinta quilos a um metro e meio equilibra um adulto de quarenta e cinco quilos a um metro, porque trinta vezes um e meio dá quarenta e cinco vezes um. A força do apoio nem entrou. Depois, com força resultante zero, ela sai fácil: segura o peso dos dois, uns setecentos e trinta e cinco newtons.

### T6-4 — tela: a régua do hook, horizontal, segurada: na dobradiça e no dedo, setas azuis M g/2 cada (EQUILÍBRIO ESTÁTICO); o dedo sai e a seta da dobradiça encolhe para M g/4 (o valor do T4-4); rótulos SEGURANDO: M g/2 · SOLTOU: M g/4; nota: ESCADAS, TOMBAMENTO E CENTRO DE GRAVIDADE → MÓDULO DE EQUILÍBRIO
[curious] E olha que bonito, de volta à régua. Enquanto o dedo segura a ponta, ela está em equilíbrio estático: pelo torque em torno da dobradiça, o dedo segura metade do peso, e a dobradiça a outra metade. No instante em que o dedo sai, o equilíbrio acaba, a régua começa a girar, e a força na dobradiça cai para um quarto do peso. Soltar a régua alivia a dobradiça. O resto do equilíbrio, escadas, tombamento, centro de gravidade, fica para o módulo de equilíbrio.

## SÍNTESE E ENCERRAMENTO

### S1 — tela: cinco cartões em PANEL, um por vez, bordas azul / azul / rosa-verde / ciano / azul: τ = r⊥ F = r F⊥ (BRAÇO DE ALAVANCA) · τ⃗ = r⃗ × F⃗ (DEPENDE DO PONTO) · Σ τ_ext,z = I_z α (EIXO FIXO OU PELO CM, NO PLANO) · W = ∫ τ dθ · P = τ ω · EQUILÍBRIO ESTÁTICO: Σ F⃗ = 0⃗ e Σ τ⃗ = 0⃗
[happy] Pra fechar, cinco cartões. Um: torque é força vezes braço de alavanca. Dois: ele é um vetor, o produto vetorial da posição pela força, e depende do ponto escolhido. Três: a segunda lei da rotação, soma dos torques externos igual a momento de inércia vezes aceleração angular, que sai de Newton aplicado a cada pedaço. Quatro: o trabalho é a integral do torque no ângulo, e a potência é torque vezes velocidade angular. Cinco: equilíbrio estático, força e torque resultantes zero.

### S2 — tela: a régua 3D do hook reaparece em câmera lenta; sobre ela, a reta a(r) verde com a marca de 2L/3 e a seta da dobradiça M g/4; a moeda da ponta flutua
[calm, satisfied] E a pergunta do começo está respondida. A ponta da régua acelera mais que a gravidade porque a régua é um corpo rígido girando em torno da dobradiça. O torque do peso dá a ela uma aceleração angular, e cada ponto acelera na proporção da distância ao eixo. Depois de dois terços do comprimento, isso passa da gravidade, e os vizinhos puxam a ponta para baixo. Na ponta, três meios de g. A moeda, que está em queda livre, simplesmente não acompanha.

### EN1 — tela: encerramento padrão (FadeOut geral, `self.clear()`, logo horizontal com anéis violeta); INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
[happy] Se esse vídeo te ajudou, se inscreve no canal para acompanhar os próximos. E deixei um desafio para você aqui embaixo.

### EN2 — tela: a régua com uma massa extra (rosa) igual à da régua presa na ponta, e uma moeda em cima da massa; texto DESAFIO: A PONTA AINDA ACELERA MAIS QUE g?; nos últimos 3 s a régua é solta e a imagem congela antes de mostrar a moeda
[curious] O desafio. Prende na ponta da régua uma massa igual à massa da própria régua, e coloca a moeda em cima dela. Agora a ponta ainda acelera mais que a gravidade? Calcula o novo torque, o novo momento de inércia, e escreve sua resposta nos comentários. Até a próxima!

---

## Conferência numérica (tabela para a auditoria `NÚMEROS`)

| Item | Valor |
|---|---|
| Hook: régua uniforme L = 1,0 m, dobradiça na ponta, solta da horizontal | |α| = 3g/(2L) = 14,70 rad/s² · ponta 3g/2 = 14,70 m/s² · meio (0,5 m) 0,75 g = 7,35 m/s² · ponto com g: 2L/3 = 0,667 m |
| Hook: folga entre a moeda da ponta e a régua | 0,6 cm em 0,05 s · 2,4 cm em 0,10 s · 5,4 cm em 0,15 s · 9,3 cm em 0,20 s · régua da horizontal à vertical em 0,484 s |
| Hook: moeda do meio (r = 0,5 m, μ_e = 0,5, μ_c = 0,4) | parada sobre a régua até ~2,9° (0,082 s); escorrega 1,5 mm até 0,15 s; sai da régua em ~17° (0,20 s) → a cena do hook para em 0,15 s |
| T1-1 porta, F = 20 N perpendicular | a 0,15 m: 3 N·m · na maçaneta a 0,75 m: 15 N·m · a 30°: 7,5 N·m (só se a cena mostrar números) |
| T1-5 / T2-4 / T2-5 chave de roda | 0,40 m × 250 N = 100 N·m · a 30°: 50 N·m · cano 0,80 m × 125 N = 100 N·m · em relação ao meio da chave (0,20 m): 50 N·m |
| T4-1/T4-2 | τ_z = −MgL/2 · I = ML²/3 · α_z = −3g/(2L) |
| T4-4 resultante das forças além do peso em cada fatia | mᵢ(|α|rᵢ − g) · soma M(3g/4 − g) = −Mg/4 → dobradiça Mg/4 para cima · conferência pelo CM: N·L/2 = (ML²/12)·|α| |
| T4-5 vassoura × lápis | 1,2 m / 0,15 m = 8 · α 12,25 × 98,0 rad/s² · sen θ (por radiano de inclinação) · tempo ∝ √L → √8 = 2,83 |
| T5-3 motor | 4.000 rpm = 418,88 rad/s · P = 41,89 kW = 56,95 cv (1 cv = 735,5 W) |
| T5-4 câmbio | redução 3 : 1 → ω/3 e 3τ, mesma potência (sem perdas) |
| T6-1 disco com CM fora do eixo | só qualitativo (se precisar de número: M = 2,0 kg, d = 5 cm, ω = 10 rad/s → ΣF = Mω²d = 10 N) |
| T6-3 gangorra | 30 × 1,5 = 45 × 1,0 · apoio (30 + 45) × 9,8 = 735 N |
| T6-4 régua segurada | dedo Mg/2 · dobradiça Mg/2 · solta: dobradiça Mg/4 |
| Desafio (resposta só nos comentários) | τ = 3MgL/2 · I = 4ML²/3 · α = 9g/(8L) · ponta 9g/8 = 11,0 m/s² > g: sim |

## Notas para quem vai implementar

- **Tags:** 18 `[thoughtful]`, 11 `[curious]`, 5 `[thoughtful, emphatic]`, 2 `[excited]` (T3-6 e T4-3), 3 `[happy]`, 1 `[calm, satisfied]`. Sem `[slowly]`, `[slow, measured pace]` nem `[pause]`.
- **Letras faladas:** nenhuma; todas as grandezas pelo nome (o índice i fica só na tela).
- **A moeda do meio** não pode ser animada como queda livre nem colada por decreto: o Three.js integra o contato (normal, atrito estático e cinético, separação quando N ≤ 0) e o hook mostra só até 0,15 s.
- **Sinais:** o T1-4 fixa anti-horário positivo; o T4-2 mostra τ_z e α_z negativos uma vez; do T4-3 em diante, módulos com o arco do sentido desenhado.
