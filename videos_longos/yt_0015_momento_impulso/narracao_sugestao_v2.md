# yt_0015 (provisório) — MOMENTO LINEAR E IMPULSO · roteiro com narração v2 · CONGELADA (2026-10-27)

Data: 2026-10-27. **v2:** ajustes da revisão do Kaio (letras soltas, C02 sem alegação histórica, C03 com a força da parede, fecho de Foucault mais preciso). Tags compostas trocadas por `[emphatic]` (decisão do Kaio) e síntese com "impulso resultante". Narração congelada. Fonte da física e dos números: `pautas/yt_0015_momento_impulso_briefing.md` (v2, sem corte, com as correções do
hook e de Snell). Padrão: `docs/padrao_video_longo.md` §5 e `docs/roteiro_voz_elevenlabs_v4.md`. Tom de professor de cursinho, "a gente"
e "você", nunca a letra solta.

**Como ler:** cada `###` é uma âncora (evento visual). A linha `tela:` diz o que aparece e a fala embaixo começa ~0,15 s depois.
A fala manda: a cena se estica para acompanhar. As tags `[ ]` são do ElevenLabs v4, em inglês, uma por trecho, valendo até a próxima;
não entram na legenda. A seção "Texto corrido" no fim é a que vai para a geração da voz, só quando o Kaio pedir.

**Notação falada:** momento linear = "momento linear" ou "quantidade de movimento" na primeira vez, depois "momento". p⃗ = momento;
J⃗ = impulso; F_res = força resultante; F_méd = força média; N = força do chão (normal); vᵢ, v_f = velocidade inicial e final.
**Cores na tela:** velocidade violeta, momento magenta, força azul-claro, impulso e área sob F(t) `#9CC7FF`, corpos em aço.

---

## HOOK

### H1 — tela: silhueta de uma pessoa em cima de um muro (2,5 m); ela cai e aterrissa de pernas duras; flash de impacto no pé
[curious] Olha essa queda. Uma pessoa pula de um muro de dois metros e meio e cai de pernas esticadas, duras. O impacto vai direto para os ossos.

### H2 — tela: reset; mesma queda, mas agora os joelhos dobram e o corpo desce até agachar
Agora a mesma pessoa, o mesmo muro, a mesma altura. Só que, dessa vez, ela dobra os joelhos quando chega no chão.

### H3 — tela: as duas aterrissagens lado a lado; MESMA QUEDA. MESMA VELOCIDADE. POR QUE DOBRAR OS JOELHOS SALVA SUAS PERNAS?
A queda é a mesma, a velocidade de chegada é a mesma, e o corpo para nos dois casos. Então por que dobrar os joelhos salva as suas pernas? É isso que a gente vai responder hoje.

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: MOMENTO LINEAR E IMPULSO · NESTE VÍDEO: O QUE UMA FORÇA FAZ AO LONGO DO TEMPO
[thoughtful] Hoje o assunto é momento linear e impulso: o que uma força faz quando age durante um certo tempo.

### A3 — tela: miniaturas dos vídeos de colisões (1D e 2D) com a equação de conservação do momento
Nos vídeos de colisões, a gente usou a conservação do momento como ferramenta, sem parar para perguntar de onde ela vem. Hoje é a vez dela. E no caminho vamos resolver vários exercícios, dos mais diretos até alguns bem cabeludos.

## C01 — POR QUE MASSA VEZES VELOCIDADE?

### C01-1 — tela: trilho de ar; dois carrinhos iguais, parados, com uma pequena carga explosiva entre eles
[curious] Primeiro, uma pergunta que quase nenhum livro faz: por que a grandeza importante é a massa vezes a velocidade? Por que não a velocidade sozinha, ou a massa vezes a velocidade ao quadrado? O Feynman tem um argumento lindo para isso, e ele começa num trilho de ar, sem atrito.

### C01-2 — tela: explosão; os carrinhos saem com velocidades iguais e opostas (setas violeta do mesmo tamanho)
[thoughtful] Dois carrinhos idênticos, parados, com uma pequena explosão entre eles. Para que lado o mais rápido vai? Não tem como escolher: os dois são iguais, então eles saem com a mesma velocidade, um para cada lado. Isso é pura simetria.

### C01-3 — tela: dois carrinhos iguais vindo um contra o outro com a mesma velocidade; colidem, grudam e PARAM
Agora o contrário: dois carrinhos iguais, vindo um contra o outro com a mesma velocidade. Eles batem e grudam. Para onde vai o conjunto? De novo, simetria: para lugar nenhum. Ele para.

### C01-4 — tela: a mesma colisão vista de um carro que anda junto com o carrinho da esquerda; VISÃO DO CARRO
[curious] Aqui vem a jogada. Imagine que você assiste a essa mesma colisão de dentro de um carro, andando junto com o carrinho da esquerda. Para você, esse carrinho está parado. O outro vem na sua direção com o dobro da velocidade. E, depois da batida, o conjunto, que no chão estava parado, para você passa andando com a velocidade original.

### C01-5 — tela: na visão do carro: m com 2v + m parado → 2m com v; embaixo, m·2v + m·0 = 2m·v (magenta)
[thoughtful] Então a gente descobriu um fato novo: um carrinho com o dobro da velocidade bate num igual parado, gruda, e os dois seguem com metade daquela velocidade. Repara na conta: massa vezes o dobro da velocidade, mais zero, dá exatamente o dobro da massa vezes a velocidade. A soma de massa vezes velocidade é a mesma antes e depois.

### C01-6 — tela: mais casos rápidos (m contra 2m, 2m contra 3m), cada um com a soma Σ m·v batendo antes e depois
Repetindo o truque com massas diferentes, um contra dois, dois contra três, o resultado é sempre o mesmo: a soma de massa vezes velocidade fecha.

### C01-7 — tela: m·v destacado; riscados v sozinho e m·v²
[emphatic] Atenção para o que esse argumento faz e o que ele não faz. Ele mostra qual é a grandeza certa: massa vezes velocidade. O porquê de ela se conservar vem das leis de Newton, e a gente chega lá daqui a pouco.

## C02 — MOMENTO LINEAR

### C02-1 — tela: um bloco com a seta de velocidade (violeta) e, logo abaixo, a seta de momento (magenta); p⃗ = m v⃗
[thoughtful] Essa grandeza tem nome: momento linear, que também aparece como quantidade de movimento. Na tela, o momento vai aparecer como esta seta magenta. É a massa vezes a velocidade. Como a massa é positiva, o momento aponta sempre para o mesmo lado da velocidade. Ou seja, o momento é um vetor.

### C02-2 — tela: unidade kg·m/s = N·s
A unidade é quilograma vezes metro por segundo, que, como a gente vai ver, é a mesma coisa que newton vezes segundo.

### C02-3 — tela: F⃗_res = dp⃗/dt; ao lado, com m constante, = m a⃗ (sem selo histórico)
Em linguagem moderna, a segunda lei de Newton fica especialmente limpa assim: a força resultante é a taxa de variação do momento, a derivada do momento em relação ao tempo. Se a massa não muda, isso é a massa vezes a aceleração de sempre. Mas essa forma, com o momento, é a que vai abrir as portas hoje.

## C03 — IMPULSO

### C03-1 — tela: bola chegando numa parede (colisão horizontal); no gráfico ao lado, F_x(t), rotulado FORÇA DA PAREDE, nasce: zero, sobe muito rápido, desce, zero
[curious] Agora olha uma colisão de verdade, em câmera lenta. Na direção da colisão, antes do contato, a força é praticamente zero. Quando a bola encosta na parede, a força horizontal sobe muito rápido, chega num pico e cai de novo a zero quando a bola se solta. Tudo isso em centésimos de segundo.

### C03-2 — tela: a área sob F_x(t) se preenche em azul (#9CC7FF); em seguida, o teorema geral J⃗ = ∫ F⃗_res dt = Δp⃗ (na colisão horizontal, a força da parede é a resultante na direção x)
[thoughtful] Se a força resultante é a derivada do momento, então somando a força ao longo do tempo a gente recupera a variação do momento. Essa soma é a integral da força no tempo, e tem nome: impulso. Ou seja, o impulso da força resultante é igual à variação do momento. Geometricamente, o impulso é a área embaixo da curva da força.

### C03-3 — tela: um retângulo de base Δt e mesma área que a curva; a altura dele é F_méd; F_méd = J/Δt
E aqui entra uma ideia muito útil: a força média. É a altura de um retângulo com a mesma base de tempo e a mesma área da curva. Então a força média é o impulso dividido pelo tempo de contato.

### C03-4 — tela: a curva se estreita e fica mais alta, com a área constante (contador da área parado)
[emphatic] Repara no que isso diz. Se a variação do momento está fixada, a área está fixada. Aí, quanto menor o tempo de contato, mais alta tem que ser a força. Guarda essa imagem, que ela vai responder a pergunta do começo.

## C04 — EXERCÍCIO 1: BOLA NA PAREDE (Sears, Exemplo 8.2)

### C04-1 — tela: ANTES: bola de 0,40 kg indo para a esquerda a 30 m/s; DEPOIS: voltando para a direita a 20 m/s; contato 0,010 s; eixo +x para a direita
[thoughtful] Vamos para o primeiro exercício. Uma bola de quatrocentos gramas chega numa parede a trinta metros por segundo, indo para a esquerda, e volta a vinte metros por segundo, para a direita. O contato dura um centésimo de segundo. Qual é o impulso, e qual é a força média da parede?

### C04-2 — tela: vᵢ = −30 m/s e v_f = +20 m/s; o sinal negativo pisca
Primeiro, o eixo: para a direita é positivo. Então a velocidade inicial é menos trinta, e a final é mais vinte.

### C04-3 — tela: J = 0,40·(20 − (−30)) = 20 N·s; as setas de momento antes e depois e o Δp⃗ apontando para a direita
O impulso é a massa vezes a velocidade final menos a velocidade inicial: zero vírgula quatro vezes vinte menos menos trinta. Dá vinte newtons vezes segundo, para a direita. Faz sentido: a parede empurra a bola de volta.

### C04-4 — tela: a conta errada, sem sinal: 0,40·(20 − 30) = −4 N·s, riscada em vermelho-apagado; "A PAREDE PUXOU A BOLA?"
[curious] E se alguém esquece o sinal? Faz vinte menos trinta, e sai menos quatro newtons vezes segundo. Isso diria que a parede puxou a bola para dentro dela! O sinal não é detalhe: o sinal é a física.

### C04-5 — tela: F_méd = 20 / 0,010 = 2.000 N; ao lado, o peso da bola, 3,9 N, como uma setinha minúscula
[thoughtful] A força média é o impulso dividido pelo tempo: vinte dividido por um centésimo, dois mil newtons. Compara com o peso da bola, menos de quatro newtons. Por isso, durante o choque, a gente pode esquecer o peso.

### C04-6 — tela: comparação: PARAR (Δp até zero) × REBATER (Δp até zero e volta)
E um detalhe que vai voltar mais adiante: rebater exige mais impulso do que só parar. Para parar, o momento vai até zero. Para rebater, ele vai até zero e ainda volta.

## C05 — EXERCÍCIO 2: CHUTE EM 2D (Sears, Exemplo 8.3)

### C05-1 — tela: bola de 0,40 kg chegando a 20 m/s para a esquerda; o pé chuta; ela sai a 30 m/s a 45° para cima e para a direita; Δt = 0,010 s
[thoughtful] Agora em duas dimensões. A mesma bola de quatrocentos gramas chega a vinte metros por segundo, para a esquerda. Leva um chute e sai a trinta metros por segundo, a quarenta e cinco graus para cima e para a direita. O contato dura de novo um centésimo de segundo.

### C05-2 — tela: componentes: v_f,x = v_f,y = 21,2 m/s; vᵢ,x = −20 m/s, vᵢ,y = 0
Como o impulso é vetor, a gente trabalha por componentes. A velocidade final tem as duas partes iguais, cerca de vinte e um vírgula dois metros por segundo. A inicial só tem a parte horizontal, menos vinte.

### C05-3 — tela: Jx = 0,40·(21,2 + 20) = 16,5 N·s; Jy = 0,40·21,2 = 8,5 N·s
O impulso horizontal é zero vírgula quatro vezes vinte e um vírgula dois mais vinte: dezesseis vírgula cinco newtons vezes segundo. O vertical é zero vírgula quatro vezes vinte e um vírgula dois: oito vírgula cinco.

### C05-4 — tela: triângulo de momentos: p⃗ᵢ, p⃗_f e Δp⃗ = p⃗_f − p⃗ᵢ fechando o triângulo; F⃗_méd sobre Δp⃗: 1,9×10³ N a 27°
[curious] Dividindo pelo tempo, a força média tem cerca de mil e novecentos newtons, a vinte e sete graus acima da horizontal. Só que a bola saiu a quarenta e cinco graus! Por que a força não aponta para onde a bola foi?

### C05-5 — tela: o ângulo de 27° (Δp⃗) e o de 45° (v⃗_f) lado a lado, em arcos brancos finos
[emphatic] Porque a força não decide para onde a bola vai. Ela decide quanto o momento muda. A força média aponta na direção da variação do momento, que é a seta que fecha o triângulo. Como a bola já vinha andando, a direção final é outra.

## C06 — EXERCÍCIO 3: FORÇA QUE CRESCE COM t² (Sears, Exercício 8.11)

### C06-1 — tela: foguete de 2.150 kg no espaço; gráfico F(t) = A t², ponto marcado em (1,25 s; 781,25 N)
[thoughtful] Até aqui, a força média bastou. Agora uma força que muda de um jeito conhecido. Um foguete de dois mil cento e cinquenta quilos, no espaço, liga um motor cuja força cresce com o quadrado do tempo. Em um vírgula vinte e cinco segundo, ela vale setecentos e oitenta e um vírgula vinte e cinco newtons. A massa do foguete, aqui, a gente trata como constante.

### C06-2 — tela: A = 781,25 / 1,25² = 500 N/s²
Primeiro, a constante: setecentos e oitenta e um vírgula vinte e cinco dividido por um vírgula vinte e cinco ao quadrado. Dá quinhentos newtons por segundo ao quadrado.

### C06-3 — tela: a área sob a parábola entre t = 2,0 s e t = 3,5 s se preenche; J = ∫ 500 t² dt = (500/3)(3,5³ − 2,0³)
Qual é o impulso entre dois segundos e três e meio? Aqui não tem atalho: é a área embaixo da parábola, ou seja, a integral. A integral do tempo ao quadrado é o tempo ao cubo sobre três. Então o impulso é quinhentos sobre três, vezes três e meio ao cubo menos dois ao cubo.

### C06-4 — tela: J ≈ 5,81×10³ N·s; Δv = J/m = 2,70 m/s; o retângulo da força média, 3.875 N, aparece por cima
[curious] O resultado é cerca de cinco mil, oitocentos e doze newtons vezes segundo. Dividindo pela massa, a velocidade do foguete aumenta dois vírgula setenta metros por segundo nesse intervalo. E repara no retângulo: a força média desse trecho é a área dividida por um segundo e meio, uns três mil oitocentos e setenta e cinco newtons.

## C07 — DE VOLTA AO MURO (Moysés, Problema 9.1)

### C07-1 — tela: volta a pessoa no muro; 80 kg, h = 2,5 m; v = √(2·9,8·2,5) = 7,0 m/s
[curious] Agora sim, de volta ao muro. A pessoa tem oitenta quilos e cai de dois metros e meio. Ela chega no chão a raiz de duas vezes nove vírgula oito vezes dois e meio: sete metros por segundo.

### C07-2 — tela: Δp = 80·7,0 = 560 kg·m/s, em magenta, igual nos dois casos
Para parar, o momento dela tem que cair de quinhentos e sessenta quilogramas metro por segundo até zero. E isso vale nos dois casos, de perna dura ou dobrando os joelhos.

### C07-3 — tela: dois gráficos F_res(t) lado a lado, com a MESMA ÁREA (560 N·s) preenchida: PERNAS DURAS (alto e estreito, Δt = 0,01 s) × JOELHOS (baixo e largo, Δt = 0,14 s)
[emphatic] Então a área embaixo da força resultante é a mesma nas duas aterrissagens: quinhentos e sessenta newtons vezes segundo. O que muda é a forma. De perna dura, o corpo para em um centésimo de segundo. Dobrando os joelhos e descendo, digamos, meio metro, a parada leva uns catorze centésimos.

### C07-4 — tela: F_res,méd = 56.000 N (pernas duras) e 3.920 N (joelhos)
Dividindo a mesma área por tempos tão diferentes: de perna dura, a força resultante média é de cinquenta e seis mil newtons. Dobrando os joelhos, três mil novecentos e vinte.

### C07-5 — tela: N = F_res + m g; o peso (784 N) entra como uma faixa fina somada em cada gráfico; ≈ 72 PESOS × ≈ 6 PESOS
[thoughtful] Só que a pergunta é com que força o chão empurra você. E o chão, além de parar o corpo, ainda segura o seu peso. Então a força do chão é a força resultante mais o peso. De perna dura, isso dá umas setenta e duas vezes o seu peso. Dobrando os joelhos... umas seis vezes.

### C07-6 — tela: PERGUNTA RESPONDIDA: MESMO IMPULSO, MAIS TEMPO, MENOS FORÇA
[excited] Está aí a resposta. Dobrar os joelhos não muda o impulso: muda o tempo. E esticar o tempo derruba a força que chega nos seus ossos. É o mesmo princípio do airbag, do capacete e do colchão do salto em altura.

### C07-7 — tela: tabela rápida em kgf: SAQUE DE TÊNIS ≈ 49 kgf · PÊNALTI ≈ 92 kgf · CARRO A 60 km/h NO MURO ≈ 25 tf
[thoughtful] Só para ter uma noção, o Moysés pede algumas forças médias em quilograma-força. Num saque de tênis, uns quarenta e nove quilogramas-força na bola. Num pênalti, uns noventa e dois. E um carro de uma tonelada e meia, a sessenta quilômetros por hora, parando num muro em um décimo de segundo: umas vinte e cinco toneladas-força.

## C08 — EXERCÍCIO CABELUDO: A PULGA (Moysés, Problema 4.7)

### C08-1 — tela: pulga (2 mg) pulando 50 cm de altura; zoom: as patas esticam 1 mm antes de sair do chão
[curious] Agora um cabeludo do Moysés. Uma pulga de dois miligramas pula cinquenta centímetros de altura. Durante o impulso, ela estica as patas e sobe só um milímetro antes de sair do chão. Com que força média ela empurra o chão, comparada com o peso dela?

### C08-2 — tela: v = √(2gh) = 3,13 m/s
[thoughtful] Primeiro, a velocidade de saída: para subir cinquenta centímetros, ela sai a raiz de duas vezes a gravidade vezes a altura, uns três vírgula um metros por segundo.

### C08-3 — tela: CAMINHO 1: a = v²/(2d) = g·h/d = 500 g
Agora dá para ir por dois caminhos. Pela cinemática: ela ganha essa velocidade em um milímetro. Supondo aceleração constante, a aceleração é a velocidade ao quadrado sobre duas vezes a distância. Isso dá a gravidade vezes a altura do pulo dividida por um milímetro: quinhentas vezes a gravidade.

### C08-4 — tela: CAMINHO 2: Δt = 2d/v = 0,64 ms; F_res = m v / Δt; as duas expressões coincidem
Pelo impulso: o tempo do empurrão é duas vezes a distância dividido pela velocidade, uns sessenta e quatro centésimos de milissegundo. A força resultante é o momento final dividido por esse tempo. E, fazendo a conta, sai exatamente a mesma coisa. Os dois caminhos são a mesma física.

### C08-5 — tela: N = m(a + g) = m g (h/d + 1) = 501 PESOS; o "+1" pisca
[emphatic] Agora a armadilha. A pergunta é a força que a pulga faz no chão, e não a força resultante. Do mesmo jeito que no muro, o chão também segura o peso dela durante o empurrão. Então são quinhentos e um pesos, e não quinhentos. Esse mais um é o peso que muita gente esquece.

### C08-6 — tela: N ≈ 9,8×10⁻³ N ≈ 1,0×10⁻³ kgf; silhueta humana de 70 kg ao lado de um bloco de 35 t
[curious] Em números, cerca de um centésimo de newton, ou um grama-força. Parece nada. Mas, proporcionalmente, é como se uma pessoa de setenta quilos empurrasse o chão com o peso de trinta e cinco toneladas.

## C09 — POR QUE O MOMENTO SE CONSERVA

### C09-1 — tela: dois corpos que interagem; F⃗₁₂ e F⃗₂₁ iguais e opostas (azul-claro)
[thoughtful] Agora a promessa do começo: por que o momento se conserva. Pega dois corpos que se empurram. Pela terceira lei de Newton, a força que um faz no outro é igual e oposta à força que o outro faz no primeiro.

### C09-2 — tela: dp⃗₁/dt = F⃗₁₂ e dp⃗₂/dt = F⃗₂₁; somando: d(p⃗₁ + p⃗₂)/dt = 0
Então, a cada instante, o momento que um ganha é exatamente o momento que o outro perde. Somando as duas equações, as forças internas se cancelam aos pares, e a soma dos momentos não muda.

### C09-3 — tela: com forças externas: dP⃗/dt = F⃗_ext; P⃗ = soma dos momentos (magenta)
[emphatic] Com muitos corpos, a ideia é a mesma. Todas as forças internas se cancelam, e só sobram as externas. A taxa de variação do momento total é a força externa resultante. Ou seja, se a força externa resultante é zero, o momento total se conserva. É isso que diz um sistema isolado.

### C09-4 — tela: a equação separada por componentes: dPx/dt = F_ext,x; dPy/dt = F_ext,y
E repara num detalhe precioso: isso vale componente por componente. Se não há força externa na horizontal, o momento horizontal se conserva, mesmo que o vertical mude. Os próximos exercícios mostram por que isso importa.

## C10 — EXERCÍCIO 6: AGARRAR OU REBATER (Sears, Exercício 8.20)

### C10-1 — tela: você (70,0 kg) parado no gelo; uma bola de 0,600 kg chega a 10,0 m/s
[thoughtful] Você está parado no gelo, sem atrito, com setenta quilos. Um amigo joga uma bola de seiscentos gramas a dez metros por segundo.

### C10-2 — tela: AGARRA: V = 0,600·10,0 / 70,6 = 0,085 m/s
Se você agarra a bola, os dois seguem juntos. O momento antes era só o da bola, seis quilogramas metro por segundo. Dividindo pela massa total, setenta vírgula seis, você sai a uns oito centímetros e meio por segundo.

### C10-3 — tela: REBATE: a bola volta a 8,0 m/s; 70,0·V = 0,600·(10,0 + 8,0); V = 0,154 m/s; ao lado, miniatura do E1 (parar × rebater)
[curious] E se a bola bate no seu peito e volta a oito metros por segundo? Agora a bola perdeu todo o momento que tinha e ainda ganhou momento para o outro lado. Esse momento todo vai para você: uns quinze centímetros por segundo, quase o dobro. É o mesmo efeito da parede: rebater transfere mais momento do que agarrar.

## C11 — EXERCÍCIO 7: O CAÇADOR NO LAGO (Sears, Exercício 8.25)

### C11-1 — tela: caçador + arma (72,5 kg) no lago congelado; bala de 4,20 g a 965 m/s, tiro horizontal
[thoughtful] Um caçador está parado num lago congelado, sem atrito. Ele e a arma têm setenta e dois vírgula cinco quilos. A bala tem quatro vírgula dois gramas e sai a novecentos e sessenta e cinco metros por segundo.

### C11-2 — tela: tiro horizontal: V = 0,00420·965 / 72,5 = 0,0559 m/s
Atirando na horizontal, o momento total era zero e continua zero. Então o recuo é o momento da bala dividido pela massa do caçador: uns cinco vírgula seis centímetros por segundo.

### C11-3 — tela: agora o tiro sai a 56° acima da horizontal; aparece a normal do gelo (azul-claro) empurrando para cima durante o disparo
[curious] Agora ele atira para cima, a cinquenta e seis graus. A bala leva momento para cima... e o caçador não afunda no gelo. Quem segurou ele?

### C11-4 — tela: Py NÃO SE CONSERVA (a normal é externa e impulsiva); Px SE CONSERVA; V = 0,0559·cos 56° = 0,031 m/s
[emphatic] Foi o gelo. Durante o disparo, a normal cresce de repente e absorve o momento vertical. Então, na vertical, o sistema não está isolado. Na horizontal, está. Por isso só a parte horizontal do momento da bala volta no caçador: o recuo cai para uns três centímetros por segundo, o anterior vezes o cosseno de cinquenta e seis graus.

## C12 — EXERCÍCIO 8: OS GASES DO RIFLE (Sears, Exercício 8.17)

### C12-1 — tela: rifle de 2,80 kg apoiado frouxamente; bala de 7,20 g sai a 601 m/s EM RELAÇÃO AO CANO; rifle recua a 1,85 m/s em relação ao chão
[curious] Mais um tiro, agora com uma pegadinha. A bala sai a seiscentos e um metros por segundo em relação ao cano, e o rifle recua a um vírgula oitenta e cinco metros por segundo em relação ao chão. A pergunta: os gases que saem junto carregam algum momento?

### C12-2 — tela: velocidade da bala em relação ao chão: 601 − 1,85 = 599,15 m/s; p_bala = 4,31 kg·m/s; p_rifle = −5,18 kg·m/s
[thoughtful] Primeiro, a velocidade da bala em relação ao chão: o cano está andando para trás, então ela é seiscentos e um menos um vírgula oitenta e cinco. O momento da bala fica em quatro vírgula trinta e um quilogramas metro por segundo, para a frente. O do rifle, cinco vírgula dezoito, para trás.

### C12-3 — tela: as setas não fecham; aparece uma nuvem de gases com p_gases = +0,866 kg·m/s; agora a soma dá zero
Só que o momento total antes era zero, e essas duas setas não se cancelam. Falta alguém no sistema: os gases. Eles carregam cerca de zero vírgula oitenta e sete quilogramas metro por segundo para a frente.

### C12-4 — tela: SISTEMA = BALA + RIFLE + GASES
[emphatic] A lição: a conservação vale para o sistema inteiro. Se a conta não fecha, quase sempre tem alguém escondido que você deixou de fora.

## C13 — CABELUDO FINAL: NEWTON E A LUZ (Moysés, Problema 9.2)

### C13-1 — tela: retrato estilizado do século XVII; raio de luz desenhado como um fluxo de bolinhas (corpúsculos)
[curious] Para fechar, um problema que mistura física e história. No século dezessete, o Newton defendia que a luz era feita de corpúsculos, bolinhas muito rápidas. Será que o impulso consegue explicar a reflexão e a refração da luz nesse modelo?

### C13-2 — tela: um corpúsculo bate num espelho; o impulso aparece perpendicular à superfície; componente tangencial igual, normal invertida; θ₁′ = θ₁
[thoughtful] Comece pela reflexão. O espelho só empurra na direção perpendicular à superfície. Então o impulso é todo normal: ele inverte a parte normal da velocidade e não mexe na parte paralela ao espelho. O resultado é que o ângulo de reflexão é igual ao de incidência.

### C13-3 — tela: agora ar → água; o impulso normal acelera o corpúsculo para dentro da água; a componente tangencial se mantém; v₁ sen θ₁ = v₂ sen θ₂
Agora a passagem do ar para a água. No modelo, a superfície dá de novo um impulso só normal. Então a parte da velocidade paralela à superfície se conserva. Escrevendo isso com os ângulos medidos a partir da normal: a velocidade no ar vezes o seno do ângulo no ar é igual à velocidade na água vezes o seno do ângulo na água.

### C13-4 — tela: sen θ₁ / sen θ₂ = CONSTANTE (a forma da lei de Snell) → no modelo de Newton: = v₂/v₁
[emphatic] E aí aparece a forma da lei de Snell: o seno de um ângulo dividido pelo seno do outro é uma constante. Só que, no modelo de Newton, essa constante é a velocidade na água dividida pela velocidade no ar.

### C13-5 — tela: o raio se aproxima da normal na água (θ₂ < θ₁) → v₂/v₁ > 1 → NEWTON: LUZ MAIS RÁPIDA NA ÁGUA
[curious] Agora olha o que a gente vê de verdade: ao entrar na água, a luz se aproxima da normal. O ângulo na água é menor. Então, pelo modelo, a velocidade na água teria que ser maior que no ar. Os corpúsculos acelerariam ao entrar na água.

### C13-6 — tela: 1850 · FOUCAULT: A LUZ É MAIS LENTA NA ÁGUA; o "v₂ > v₁" é riscado; ao lado, na descrição ondulatória: sen θ₁ / sen θ₂ = v₁/v₂
[excited] Por quase dois séculos, ninguém conseguiu medir. Até que, em mil oitocentos e cinquenta, o Foucault mediu a luz na água... e ela era mais lenta. A previsão do modelo corpuscular de Newton caiu. Na descrição ondulatória, a relação entre os ângulos e as velocidades aparece invertida, e é essa que a natureza segue.

### C13-7 — tela: IMPULSO CERTO + MODELO ERRADO = PREVISÃO TESTÁVEL
[thoughtful] E repara que o teorema do impulso estava certo o tempo todo. O que estava errado era o modelo de luz. Uma física correta, aplicada com cuidado, fez uma previsão que dava para medir, e a natureza decidiu.

## SÍNTESE

### S1 — tela: limpa; as duas curvas F_res(t) do muro com a mesma área
[calm, satisfied] Então, voltando à pergunta do começo. Dobrar os joelhos não muda o impulso resultante necessário para parar você: ele continua sendo a variação do momento. O que muda é o tempo. Mais tempo, menos força média.

### S2 — tela: as duas equações-chave: J⃗ = ∫ F⃗_res dt = Δp⃗ e dP⃗/dt = F⃗_ext
Resumindo o vídeo em duas equações. O impulso da força resultante é a área embaixo da força no tempo, e é igual à variação do momento. E o momento total de um sistema só muda com força externa, componente por componente.

## ENCERRAMENTO

### E1 — tela: FadeOut geral; logo com anéis; INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
Se esses exercícios ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### E2 — tela: granada explodindo no ar, fragmentos para todos os lados, um ponto seguindo a parábola; SE A GRANADA EXPLODE NO AR, O QUE CONTINUA NA PARÁBOLA? → PRÓXIMO VÍDEO: CENTRO DE MASSA (ciano)
[curious] E fica a pergunta para o próximo: se uma granada explode no meio do voo, os pedaços voam para todo lado... mas alguma coisa continua exatamente na mesma parábola. O quê? No próximo vídeo: centro de massa. Até a próxima!

---

## Números de conferência (todos do briefing v2, g = 9,8 m/s²)

| Bloco | Valor falado | Exato |
|---|---|---|
| C04 | 20 N·s; 2.000 N; peso < 4 N | 20; 2000; 3,92 |
| C05 | 21,2 m/s; 16,5 e 8,5 N·s; ~1.900 N a 27° | 21,21; 16,49 e 8,49; 1854 N a 27,2° |
| C06 | 500 N/s²; ~5.812 N·s; 2,70 m/s; ~3.875 N | 500; 5812,5; 2,703; 3875 |
| C07 | 7 m/s; 560; 0,01 s × 0,14 s; 56.000 N × 3.920 N; ~72 × ~6 pesos | 7,000; 560; 0,143 s; 56.000 e 3.920 N; 72,4 e 6,0 |
| C07 tabela | 49 kgf; 92 kgf; 25 tf | 48,98; 91,84; 25,51 |
| C08 | 3,1 m/s; 500 g; 0,64 ms; 501 pesos; ~1 gf; 35 t | 3,130; 500; 0,639; 501; 1,0 gf; 35,07 t |
| C10 | 8,5 cm/s; 15 cm/s | 0,0850; 0,1543 m/s |
| C11 | 5,6 cm/s; 3 cm/s | 0,0559; 0,0313 m/s |
| C12 | 599,15 m/s; 4,31; 5,18; 0,87 kg·m/s | 4,3139; 5,18; 0,8661 |

**Contagem:** ~3.050 palavras de fala → ~19 min a 2,7 palavras/s (a voz real fica entre 17 e 19 min).

**Pontos a confirmar antes da voz**
1. C07: o "meio metro" do agachamento é estimativa nossa (o Moysés só dá o 0,01 s da perna dura). A fala já diz "digamos".
2. C13: Foucault, 1850, luz mais lenta na água: fato histórico bem estabelecido, mas vale conferir numa fonte se for para a descrição.
3. C01: a fala diz que o argumento escolhe **qual grandeza**, e que a conservação vem de dP⃗/dt = F⃗_ext em C09 (correção do Kaio).

---

## Texto corrido (para gravação)

[curious] Olha essa queda. Uma pessoa pula de um muro de dois metros e meio e cai de pernas esticadas, duras. O impacto vai direto para os ossos.

Agora a mesma pessoa, o mesmo muro, a mesma altura. Só que, dessa vez, ela dobra os joelhos quando chega no chão.

A queda é a mesma, a velocidade de chegada é a mesma, e o corpo para nos dois casos. Então por que dobrar os joelhos salva as suas pernas? É isso que a gente vai responder hoje.

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

[thoughtful] Hoje o assunto é momento linear e impulso: o que uma força faz quando age durante um certo tempo.

Nos vídeos de colisões, a gente usou a conservação do momento como ferramenta, sem parar para perguntar de onde ela vem. Hoje é a vez dela. E no caminho vamos resolver vários exercícios, dos mais diretos até alguns bem cabeludos.

[curious] Primeiro, uma pergunta que quase nenhum livro faz: por que a grandeza importante é a massa vezes a velocidade? Por que não a velocidade sozinha, ou a massa vezes a velocidade ao quadrado? O Feynman tem um argumento lindo para isso, e ele começa num trilho de ar, sem atrito.

[thoughtful] Dois carrinhos idênticos, parados, com uma pequena explosão entre eles. Para que lado o mais rápido vai? Não tem como escolher: os dois são iguais, então eles saem com a mesma velocidade, um para cada lado. Isso é pura simetria.

Agora o contrário: dois carrinhos iguais, vindo um contra o outro com a mesma velocidade. Eles batem e grudam. Para onde vai o conjunto? De novo, simetria: para lugar nenhum. Ele para.

[curious] Aqui vem a jogada. Imagine que você assiste a essa mesma colisão de dentro de um carro, andando junto com o carrinho da esquerda. Para você, esse carrinho está parado. O outro vem na sua direção com o dobro da velocidade. E, depois da batida, o conjunto, que no chão estava parado, para você passa andando com a velocidade original.

[thoughtful] Então a gente descobriu um fato novo: um carrinho com o dobro da velocidade bate num igual parado, gruda, e os dois seguem com metade daquela velocidade. Repara na conta: massa vezes o dobro da velocidade, mais zero, dá exatamente o dobro da massa vezes a velocidade. A soma de massa vezes velocidade é a mesma antes e depois.

Repetindo o truque com massas diferentes, um contra dois, dois contra três, o resultado é sempre o mesmo: a soma de massa vezes velocidade fecha.

[emphatic] Atenção para o que esse argumento faz e o que ele não faz. Ele mostra qual é a grandeza certa: massa vezes velocidade. O porquê de ela se conservar vem das leis de Newton, e a gente chega lá daqui a pouco.

[thoughtful] Essa grandeza tem nome: momento linear, que também aparece como quantidade de movimento. Na tela, o momento vai aparecer como esta seta magenta. É a massa vezes a velocidade. Como a massa é positiva, o momento aponta sempre para o mesmo lado da velocidade. Ou seja, o momento é um vetor.

A unidade é quilograma vezes metro por segundo, que, como a gente vai ver, é a mesma coisa que newton vezes segundo.

Em linguagem moderna, a segunda lei de Newton fica especialmente limpa assim: a força resultante é a taxa de variação do momento, a derivada do momento em relação ao tempo. Se a massa não muda, isso é a massa vezes a aceleração de sempre. Mas essa forma, com o momento, é a que vai abrir as portas hoje.

[curious] Agora olha uma colisão de verdade, em câmera lenta. Na direção da colisão, antes do contato, a força é praticamente zero. Quando a bola encosta na parede, a força horizontal sobe muito rápido, chega num pico e cai de novo a zero quando a bola se solta. Tudo isso em centésimos de segundo.

[thoughtful] Se a força resultante é a derivada do momento, então somando a força ao longo do tempo a gente recupera a variação do momento. Essa soma é a integral da força no tempo, e tem nome: impulso. Ou seja, o impulso da força resultante é igual à variação do momento. Geometricamente, o impulso é a área embaixo da curva da força.

E aqui entra uma ideia muito útil: a força média. É a altura de um retângulo com a mesma base de tempo e a mesma área da curva. Então a força média é o impulso dividido pelo tempo de contato.

[emphatic] Repara no que isso diz. Se a variação do momento está fixada, a área está fixada. Aí, quanto menor o tempo de contato, mais alta tem que ser a força. Guarda essa imagem, que ela vai responder a pergunta do começo.

[thoughtful] Vamos para o primeiro exercício. Uma bola de quatrocentos gramas chega numa parede a trinta metros por segundo, indo para a esquerda, e volta a vinte metros por segundo, para a direita. O contato dura um centésimo de segundo. Qual é o impulso, e qual é a força média da parede?

Primeiro, o eixo: para a direita é positivo. Então a velocidade inicial é menos trinta, e a final é mais vinte.

O impulso é a massa vezes a velocidade final menos a velocidade inicial: zero vírgula quatro vezes vinte menos menos trinta. Dá vinte newtons vezes segundo, para a direita. Faz sentido: a parede empurra a bola de volta.

[curious] E se alguém esquece o sinal? Faz vinte menos trinta, e sai menos quatro newtons vezes segundo. Isso diria que a parede puxou a bola para dentro dela! O sinal não é detalhe: o sinal é a física.

[thoughtful] A força média é o impulso dividido pelo tempo: vinte dividido por um centésimo, dois mil newtons. Compara com o peso da bola, menos de quatro newtons. Por isso, durante o choque, a gente pode esquecer o peso.

E um detalhe que vai voltar mais adiante: rebater exige mais impulso do que só parar. Para parar, o momento vai até zero. Para rebater, ele vai até zero e ainda volta.

[thoughtful] Agora em duas dimensões. A mesma bola de quatrocentos gramas chega a vinte metros por segundo, para a esquerda. Leva um chute e sai a trinta metros por segundo, a quarenta e cinco graus para cima e para a direita. O contato dura de novo um centésimo de segundo.

Como o impulso é vetor, a gente trabalha por componentes. A velocidade final tem as duas partes iguais, cerca de vinte e um vírgula dois metros por segundo. A inicial só tem a parte horizontal, menos vinte.

O impulso horizontal é zero vírgula quatro vezes vinte e um vírgula dois mais vinte: dezesseis vírgula cinco newtons vezes segundo. O vertical é zero vírgula quatro vezes vinte e um vírgula dois: oito vírgula cinco.

[curious] Dividindo pelo tempo, a força média tem cerca de mil e novecentos newtons, a vinte e sete graus acima da horizontal. Só que a bola saiu a quarenta e cinco graus! Por que a força não aponta para onde a bola foi?

[emphatic] Porque a força não decide para onde a bola vai. Ela decide quanto o momento muda. A força média aponta na direção da variação do momento, que é a seta que fecha o triângulo. Como a bola já vinha andando, a direção final é outra.

[thoughtful] Até aqui, a força média bastou. Agora uma força que muda de um jeito conhecido. Um foguete de dois mil cento e cinquenta quilos, no espaço, liga um motor cuja força cresce com o quadrado do tempo. Em um vírgula vinte e cinco segundo, ela vale setecentos e oitenta e um vírgula vinte e cinco newtons. A massa do foguete, aqui, a gente trata como constante.

Primeiro, a constante: setecentos e oitenta e um vírgula vinte e cinco dividido por um vírgula vinte e cinco ao quadrado. Dá quinhentos newtons por segundo ao quadrado.

Qual é o impulso entre dois segundos e três e meio? Aqui não tem atalho: é a área embaixo da parábola, ou seja, a integral. A integral do tempo ao quadrado é o tempo ao cubo sobre três. Então o impulso é quinhentos sobre três, vezes três e meio ao cubo menos dois ao cubo.

[curious] O resultado é cerca de cinco mil, oitocentos e doze newtons vezes segundo. Dividindo pela massa, a velocidade do foguete aumenta dois vírgula setenta metros por segundo nesse intervalo. E repara no retângulo: a força média desse trecho é a área dividida por um segundo e meio, uns três mil oitocentos e setenta e cinco newtons.

[curious] Agora sim, de volta ao muro. A pessoa tem oitenta quilos e cai de dois metros e meio. Ela chega no chão a raiz de duas vezes nove vírgula oito vezes dois e meio: sete metros por segundo.

Para parar, o momento dela tem que cair de quinhentos e sessenta quilogramas metro por segundo até zero. E isso vale nos dois casos, de perna dura ou dobrando os joelhos.

[emphatic] Então a área embaixo da força resultante é a mesma nas duas aterrissagens: quinhentos e sessenta newtons vezes segundo. O que muda é a forma. De perna dura, o corpo para em um centésimo de segundo. Dobrando os joelhos e descendo, digamos, meio metro, a parada leva uns catorze centésimos.

Dividindo a mesma área por tempos tão diferentes: de perna dura, a força resultante média é de cinquenta e seis mil newtons. Dobrando os joelhos, três mil novecentos e vinte.

[thoughtful] Só que a pergunta é com que força o chão empurra você. E o chão, além de parar o corpo, ainda segura o seu peso. Então a força do chão é a força resultante mais o peso. De perna dura, isso dá umas setenta e duas vezes o seu peso. Dobrando os joelhos... umas seis vezes.

[excited] Está aí a resposta. Dobrar os joelhos não muda o impulso: muda o tempo. E esticar o tempo derruba a força que chega nos seus ossos. É o mesmo princípio do airbag, do capacete e do colchão do salto em altura.

[thoughtful] Só para ter uma noção, o Moysés pede algumas forças médias em quilograma-força. Num saque de tênis, uns quarenta e nove quilogramas-força na bola. Num pênalti, uns noventa e dois. E um carro de uma tonelada e meia, a sessenta quilômetros por hora, parando num muro em um décimo de segundo: umas vinte e cinco toneladas-força.

[curious] Agora um cabeludo do Moysés. Uma pulga de dois miligramas pula cinquenta centímetros de altura. Durante o impulso, ela estica as patas e sobe só um milímetro antes de sair do chão. Com que força média ela empurra o chão, comparada com o peso dela?

[thoughtful] Primeiro, a velocidade de saída: para subir cinquenta centímetros, ela sai a raiz de duas vezes a gravidade vezes a altura, uns três vírgula um metros por segundo.

Agora dá para ir por dois caminhos. Pela cinemática: ela ganha essa velocidade em um milímetro. Supondo aceleração constante, a aceleração é a velocidade ao quadrado sobre duas vezes a distância. Isso dá a gravidade vezes a altura do pulo dividida por um milímetro: quinhentas vezes a gravidade.

Pelo impulso: o tempo do empurrão é duas vezes a distância dividido pela velocidade, uns sessenta e quatro centésimos de milissegundo. A força resultante é o momento final dividido por esse tempo. E, fazendo a conta, sai exatamente a mesma coisa. Os dois caminhos são a mesma física.

[emphatic] Agora a armadilha. A pergunta é a força que a pulga faz no chão, e não a força resultante. Do mesmo jeito que no muro, o chão também segura o peso dela durante o empurrão. Então são quinhentos e um pesos, e não quinhentos. Esse mais um é o peso que muita gente esquece.

[curious] Em números, cerca de um centésimo de newton, ou um grama-força. Parece nada. Mas, proporcionalmente, é como se uma pessoa de setenta quilos empurrasse o chão com o peso de trinta e cinco toneladas.

[thoughtful] Agora a promessa do começo: por que o momento se conserva. Pega dois corpos que se empurram. Pela terceira lei de Newton, a força que um faz no outro é igual e oposta à força que o outro faz no primeiro.

Então, a cada instante, o momento que um ganha é exatamente o momento que o outro perde. Somando as duas equações, as forças internas se cancelam aos pares, e a soma dos momentos não muda.

[emphatic] Com muitos corpos, a ideia é a mesma. Todas as forças internas se cancelam, e só sobram as externas. A taxa de variação do momento total é a força externa resultante. Ou seja, se a força externa resultante é zero, o momento total se conserva. É isso que diz um sistema isolado.

E repara num detalhe precioso: isso vale componente por componente. Se não há força externa na horizontal, o momento horizontal se conserva, mesmo que o vertical mude. Os próximos exercícios mostram por que isso importa.

[thoughtful] Você está parado no gelo, sem atrito, com setenta quilos. Um amigo joga uma bola de seiscentos gramas a dez metros por segundo.

Se você agarra a bola, os dois seguem juntos. O momento antes era só o da bola, seis quilogramas metro por segundo. Dividindo pela massa total, setenta vírgula seis, você sai a uns oito centímetros e meio por segundo.

[curious] E se a bola bate no seu peito e volta a oito metros por segundo? Agora a bola perdeu todo o momento que tinha e ainda ganhou momento para o outro lado. Esse momento todo vai para você: uns quinze centímetros por segundo, quase o dobro. É o mesmo efeito da parede: rebater transfere mais momento do que agarrar.

[thoughtful] Um caçador está parado num lago congelado, sem atrito. Ele e a arma têm setenta e dois vírgula cinco quilos. A bala tem quatro vírgula dois gramas e sai a novecentos e sessenta e cinco metros por segundo.

Atirando na horizontal, o momento total era zero e continua zero. Então o recuo é o momento da bala dividido pela massa do caçador: uns cinco vírgula seis centímetros por segundo.

[curious] Agora ele atira para cima, a cinquenta e seis graus. A bala leva momento para cima... e o caçador não afunda no gelo. Quem segurou ele?

[emphatic] Foi o gelo. Durante o disparo, a normal cresce de repente e absorve o momento vertical. Então, na vertical, o sistema não está isolado. Na horizontal, está. Por isso só a parte horizontal do momento da bala volta no caçador: o recuo cai para uns três centímetros por segundo, o anterior vezes o cosseno de cinquenta e seis graus.

[curious] Mais um tiro, agora com uma pegadinha. A bala sai a seiscentos e um metros por segundo em relação ao cano, e o rifle recua a um vírgula oitenta e cinco metros por segundo em relação ao chão. A pergunta: os gases que saem junto carregam algum momento?

[thoughtful] Primeiro, a velocidade da bala em relação ao chão: o cano está andando para trás, então ela é seiscentos e um menos um vírgula oitenta e cinco. O momento da bala fica em quatro vírgula trinta e um quilogramas metro por segundo, para a frente. O do rifle, cinco vírgula dezoito, para trás.

Só que o momento total antes era zero, e essas duas setas não se cancelam. Falta alguém no sistema: os gases. Eles carregam cerca de zero vírgula oitenta e sete quilogramas metro por segundo para a frente.

[emphatic] A lição: a conservação vale para o sistema inteiro. Se a conta não fecha, quase sempre tem alguém escondido que você deixou de fora.

[curious] Para fechar, um problema que mistura física e história. No século dezessete, o Newton defendia que a luz era feita de corpúsculos, bolinhas muito rápidas. Será que o impulso consegue explicar a reflexão e a refração da luz nesse modelo?

[thoughtful] Comece pela reflexão. O espelho só empurra na direção perpendicular à superfície. Então o impulso é todo normal: ele inverte a parte normal da velocidade e não mexe na parte paralela ao espelho. O resultado é que o ângulo de reflexão é igual ao de incidência.

Agora a passagem do ar para a água. No modelo, a superfície dá de novo um impulso só normal. Então a parte da velocidade paralela à superfície se conserva. Escrevendo isso com os ângulos medidos a partir da normal: a velocidade no ar vezes o seno do ângulo no ar é igual à velocidade na água vezes o seno do ângulo na água.

[emphatic] E aí aparece a forma da lei de Snell: o seno de um ângulo dividido pelo seno do outro é uma constante. Só que, no modelo de Newton, essa constante é a velocidade na água dividida pela velocidade no ar.

[curious] Agora olha o que a gente vê de verdade: ao entrar na água, a luz se aproxima da normal. O ângulo na água é menor. Então, pelo modelo, a velocidade na água teria que ser maior que no ar. Os corpúsculos acelerariam ao entrar na água.

[excited] Por quase dois séculos, ninguém conseguiu medir. Até que, em mil oitocentos e cinquenta, o Foucault mediu a luz na água... e ela era mais lenta. A previsão do modelo corpuscular de Newton caiu. Na descrição ondulatória, a relação entre os ângulos e as velocidades aparece invertida, e é essa que a natureza segue.

[thoughtful] E repara que o teorema do impulso estava certo o tempo todo. O que estava errado era o modelo de luz. Uma física correta, aplicada com cuidado, fez uma previsão que dava para medir, e a natureza decidiu.

[calm, satisfied] Então, voltando à pergunta do começo. Dobrar os joelhos não muda o impulso resultante necessário para parar você: ele continua sendo a variação do momento. O que muda é o tempo. Mais tempo, menos força média.

Resumindo o vídeo em duas equações. O impulso da força resultante é a área embaixo da força no tempo, e é igual à variação do momento. E o momento total de um sistema só muda com força externa, componente por componente.

Se esses exercícios ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

[curious] E fica a pergunta para o próximo: se uma granada explode no meio do voo, os pedaços voam para todo lado... mas alguma coisa continua exatamente na mesma parábola. O quê? No próximo vídeo: centro de massa. Até a próxima!
