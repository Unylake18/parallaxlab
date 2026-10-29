# yt_0015 — MOMENTO LINEAR E IMPULSO · roteiro com narração v4 (Parte 1 de 2)

Data: 2026-10-28. v4 = v3 com a teoria refeita no começo (T1 novo: o momento sai da segunda lei, com componentes em 3D; T5: impulso construído do caso constante até a integral e as componentes) e sem citação de livro na fala nem na tela.
v3 original: 2026-10-27 (guardada em `narracao_sugestao_v3.md`). Este é o **vídeo 1: uma partícula**. Os exercícios E6–E9 e a teoria de sistemas vão para o yt_0016.
Regras de fala: tom de professor de cursinho, "a gente" e "você", nunca a letra solta, tags de um só descritor (`[thoughtful]`,
`[curious]`, `[emphatic]`, `[excited]`, `[happy]`), uma por trecho; "impulso resultante" quando for o da força resultante.

**Como ler:** cada `###` é uma âncora (evento visual). A linha `tela:` diz o que aparece; a fala começa ~0,15 s depois.

---

## HOOK

### H1 — tela: (3D) muro de concreto de 2,5 m; manequim articulado em aço no topo; ele pula e aterrissa de pernas esticadas; tremor curto no impacto
[curious] Olha essa queda. Uma pessoa pula de um muro de dois metros e meio e chega no chão de pernas esticadas, duras. O corpo para quase de uma vez, e o impacto vai direto para os ossos.

### H2 — tela: (3D) reset; mesma queda; agora os joelhos dobram ~90°, o quadril desce meio metro, os braços vêm à frente
Agora a mesma pessoa, o mesmo muro, a mesma altura. Só que, dessa vez, ela dobra os joelhos quando chega no chão.

### H3 — tela: (3D) as duas aterrissagens lado a lado, câmera abre; texto central POR QUE DOBRAR OS JOELHOS SALVA SUAS PERNAS?
A queda é a mesma, a velocidade de chegada é a mesma, e nos dois casos o corpo termina parado. Então por que dobrar os joelhos salva as suas pernas? Para responder com cuidado, a gente vai precisar de duas ideias: momento linear e impulso.

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: MOMENTO LINEAR E IMPULSO · NESTE VÍDEO: O QUE UMA FORÇA FAZ AO LONGO DO TEMPO
[thoughtful] Hoje o assunto é momento linear e impulso. Neste vídeo a gente olha para um corpo só e para o que uma força faz com ele ao longo do tempo. No próximo, a gente junta vários corpos e entende por que o momento total se conserva.

### A3 — tela: miniaturas dos vídeos de colisões com P⃗ᵢ = P⃗_f
Nos vídeos de colisões, a conservação do momento foi a nossa ferramenta. Hoje a gente vai até a raiz dela.

## T1 — DE ONDE VEM O MOMENTO

### T1-1 — tela: (3D) eixos x, y, z; uma partícula de aço percorre uma trajetória curva no espaço deixando um rastro fino; v⃗ (violeta) tangente à trajetória e F⃗_res (azul-claro) sobre ela; na CONTA: ΣF⃗ = m a⃗
[thoughtful] Vamos começar do que você já conhece: a segunda lei de Newton. Uma partícula de massa m andando pelo espaço, numa trajetória qualquer. Em cada instante ela tem uma velocidade, tangente à trajetória, e a força resultante sobre ela é a massa vezes a aceleração.

### T1-2 — tela: a⃗ nasce da animação (v⃗ em dois instantes próximos, a diferença Δv⃗ encolhendo para dv⃗) e entra na conta: ΣF⃗ = m dv⃗/dt; o m desliza para dentro da derivada: ΣF⃗ = d(m v⃗)/dt; selo MASSA CONSTANTE
Só que a aceleração é a taxa com que a velocidade muda: a derivada da velocidade no tempo. Então a força resultante é a massa vezes a derivada da velocidade. E, se a massa é constante, ela pode entrar na derivada sem mudar nada. A força resultante é a derivada, no tempo, da massa vezes a velocidade.

### T1-3 — tela: m v⃗ em destaque na conta; na partícula, a seta magenta p⃗ nasce da seta violeta v⃗, esticada pelo fator m; p⃗ = m v⃗; MOMENTO LINEAR · QUANTIDADE DE MOVIMENTO; unidade kg·m/s
[emphatic] Esse produto, massa vezes velocidade, merece um nome: momento linear, ou quantidade de movimento. Na tela ele vai ser sempre esta seta magenta. Como a massa é positiva, o momento aponta para o mesmo lado da velocidade, e a unidade é quilograma metro por segundo.

### T1-4 — tela: vista de cima; dois carros iguais a 20 m/s, um para o norte e outro para o leste; setas magenta do mesmo tamanho em direções diferentes; |p⃗₁| = |p⃗₂| e p⃗₁ ≠ p⃗₂
[curious] E o momento é um vetor de verdade. Dois carros iguais, a vinte metros por segundo, um indo para o norte e o outro para o leste. O tamanho do momento é o mesmo. Mas os momentos são diferentes, porque apontam para lados diferentes.

### T1-5 — tela: (3D) de volta à partícula; v⃗ se projeta nos três eixos (tracejados até x, y e z); os rótulos vx, vy, vz saem da animação e descem para a conta; px = m vx · py = m vy · pz = m vz
[thoughtful] Na prática, a gente trabalha com componentes. Projeta a velocidade nos três eixos: aparecem as componentes em x, em y e em z. Cada componente do momento é a massa vezes a componente da velocidade naquela direção. São três equações escalares no lugar de uma vetorial.

### T1-6 — tela: substituição na conta: ΣF⃗ = dp⃗/dt (caixa); depois as três: ΣFx = dpx/dt · ΣFy = dpy/dt · ΣFz = dpz/dt; na partícula, F⃗_res também se projeta nos eixos, e três barras magenta (px, py, pz) mudam, cada uma na taxa da sua componente de força
Agora volta na segunda lei e troca massa vezes velocidade pelo momento. A força resultante é a taxa de variação do momento. E, componente por componente: a força em x só mexe no momento em x, a força em y só mexe no momento em y, e o mesmo vale em z. Cada direção cuida da sua.

### T1-7 — tela: ΣF⃗ = dp⃗/dt com os selos A FORMA ORIGINAL DE NEWTON e REFERENCIAL INERCIAL; no PALCO, um foguete soltando gás com MASSA VARIÁVEL
[emphatic] Essa é, aliás, a forma em que o próprio Newton escreveu a segunda lei, falando em quantidade de movimento. Ela vale em referenciais inerciais e é mais geral que massa vezes aceleração: continua fazendo sentido quando a massa muda, como num foguete. Esse caso fica para um vídeo desta série.

## T2 — O FATO EXPERIMENTAL

### T2-1 — tela: colchão de ar visto de cima; dois discos de aço iguais; EXPERIÊNCIA 1: vêm com velocidades opostas e TROCAM as velocidades
[thoughtful] Então a força muda o momento. E quando nenhuma força de fora age? Vamos à experiência. Dois discos iguais deslizando sobre um colchão de ar, praticamente sem atrito. Na primeira experiência, eles vêm um contra o outro com a mesma velocidade, batem... e voltam, cada um com a velocidade que o outro tinha.

### T2-2 — tela: EXPERIÊNCIA 2: um parado, o outro chega com v; o primeiro PARA e o segundo sai com v
Na segunda, um disco está parado e o outro chega. Depois da batida, quem vinha para, e quem estava parado sai com a velocidade que o primeiro trazia.

### T2-3 — tela: EXPERIÊNCIA 3: um pedacinho de chiclete; grudam e seguem com v/2
Na terceira, a gente gruda um pedacinho de chiclete num deles. Agora eles batem, ficam juntos, e o conjunto segue com metade da velocidade.

### T2-4 — tela: a tabela das três experiências (ANTES | DEPOIS) montada linha a linha a partir dos discos, que ficam pequenos à esquerda; m·v₁ + m·v₂ em magenta; o total é igual nas duas colunas em todas as linhas
[curious] Três finais completamente diferentes. Mas olha a última coluna: massa vezes velocidade de um, mais massa vezes velocidade do outro. Antes e depois, essa soma é a mesma nas três. E se a gente repete com massas diferentes, ela continua a mesma.

### T2-5 — tela: os dois discos da experiência 3 colidindo em loop lento, com as setas p⃗₁, p⃗₂ e a soma P⃗ (magenta, tamanho constante) acompanhando; P⃗ = p⃗₁ + p⃗₂ = CONSTANTE · PRINCÍPIO DE CONSERVAÇÃO DO MOMENTO (SISTEMA ISOLADO)
[emphatic] Isso é uma lei da natureza tirada direto da experiência: o princípio de conservação do momento. Num sistema isolado, a soma das massas vezes as velocidades não muda.

## T3 — POR QUE MASSA VEZES VELOCIDADE?

### T3-1 — tela: (3D) trilho de ar; dois carrinhos iguais com uma cápsula de explosão; explodem e saem com setas violeta iguais e opostas
[curious] Mas por que é justamente essa grandeza que se conserva? Por que não a velocidade sozinha, ou a massa vezes a velocidade ao quadrado? Tem um argumento de simetria lindo para isso. Dois carrinhos iguais, parados, com uma pequena explosão entre eles. Como os dois são iguais, não tem por que um sair mais rápido: eles saem com a mesma velocidade, um para cada lado.

### T3-2 — tela: (3D) dois carrinhos iguais vindo com a mesma velocidade; batem, grudam e PARAM
[thoughtful] Pelo mesmo motivo, dois carrinhos iguais que vêm um contra o outro com a mesma velocidade e grudam ficam parados. É pura simetria.

### T3-3 — tela: (3D) a câmera passa a andar junto com o carrinho da esquerda; VISÃO DO CARRO; um parado, o outro chega com 2v, o conjunto sai com v
Agora assista à mesma colisão de dentro de um carro que anda junto com o carrinho da esquerda. Para você, ele está parado. O outro vem com o dobro da velocidade. E o conjunto, que no chão estava parado, para você passa andando com a velocidade original.

### T3-4 — tela: (3D recuado, o trilho continua visível em cima) m·2v + m·0 = 2m·v; depois os casos m contra 2m e 2m contra 3m, cada um com a sua colisão rodando no trilho enquanto a conta fecha
[thoughtful] Então um carrinho com o dobro da velocidade bate num igual parado e os dois seguem com metade dela. Massa vezes o dobro da velocidade, mais zero, dá o dobro da massa vezes a velocidade. Repetindo o truque com massas diferentes, sempre fecha.

### T3-5 — tela: o bloco com v⃗ (violeta) e p⃗ (magenta) do T1 volta ao lado da soma; p⃗ = m v⃗ aparece duas vezes, com os selos DA SEGUNDA LEI e DA SIMETRIA convergindo para ele
[emphatic] Repara: a grandeza que a segunda lei de Newton entregou é a mesma que a simetria aponta. Não é coincidência. É o momento linear.

## T4 — DA CONSERVAÇÃO À TERCEIRA LEI

### T4-1 — tela: Δp⃗₁ = −Δp⃗₂ (o que um ganha, o outro perde); os dois discos da experiência 2 colidindo, com as setas Δp⃗ saindo do contato
[thoughtful] Agora vem uma virada que poucos livros fazem. Se o momento total não muda, então tudo o que um disco ganha de momento o outro perde. A variação do momento do primeiro é menos a variação do momento do segundo.

### T4-2 — tela: divide os dois lados por Δt; Δt → 0; dp⃗₁/dt = −dp⃗₂/dt (TransformMatchingTex passo a passo); um relógio de colisão encolhendo Δt no PALCO
Divide os dois lados pelo tempo da colisão. E, como esse tempo é curtíssimo, a gente pode pensar a cada instante: a taxa de variação do momento de um é menos a taxa do outro.

### T4-3 — tela: dp⃗₁/dt vira F⃗₁₍₂₎ e dp⃗₂/dt vira F⃗₂₍₁₎ → F⃗₁₍₂₎ = −F⃗₂₍₁₎; setas azul-claro iguais e opostas nos discos
[emphatic] Só que, como a gente viu no começo, a taxa de variação do momento é a força. Então a força que o segundo faz no primeiro é igual e oposta à força que o primeiro faz no segundo. Saiu a terceira lei de Newton, da conservação do momento.

### T4-4 — tela: AÇÃO E REAÇÃO AGEM EM CORPOS DIFERENTES; bloco na mesa: P (peso) e N (normal) no bloco; a reação do peso desenhada na Terra
[curious] E aqui mora uma armadilha clássica. Ação e reação agem sempre em corpos diferentes. Por isso a normal da mesa não é a reação do peso do bloco: as duas estão no bloco. A reação do peso é a força com que o bloco puxa a Terra para cima.

### T4-5 — tela: duas cargas em movimento com forças não opostas (esquema) + uma "nuvem" de campo; MOMENTO DAS PARTÍCULAS + MOMENTO DO CAMPO = CONSTANTE
[thoughtful] E por que vale a pena partir da conservação? Porque ela é mais funda. Entre cargas em movimento, a terceira lei pode falhar: as forças não ficam iguais e opostas. Mas a conservação continua valendo se a gente contar também o momento que o próprio campo carrega. A conservação sobrevive onde a terceira lei não chega.

## T5 — IMPULSO

### T5-1 — tela: bloco num piso sem atrito; força resultante constante F⃗ de t₁ a t₂ (relógio no PALCO); a seta magenta do bloco cresce; à direita, gráfico F × t (retângulo crescendo) e, abaixo dele, gráfico p × t (reta subindo, inclinação = F)
[thoughtful] Agora o impulso, construído passo a passo. Primeiro o caso mais simples: uma força resultante constante, agindo de um instante t um até um instante t dois. Se a força é constante, a taxa de variação do momento também é constante: o gráfico do momento no tempo é uma reta, e a inclinação dessa reta é a força.

### T5-2 — tela: o triângulo de inclinação aparece no gráfico p × t; o cateto vertical vira p⃗₂ − p⃗₁ e o horizontal vira t₂ − t₁ na conta: ΣF⃗ = dp⃗/dt → ΣF⃗ = (p⃗₂ − p⃗₁)/(t₂ − t₁) → ΣF⃗ (t₂ − t₁) = p⃗₂ − p⃗₁ (o (t₂ − t₁) atravessa a igualdade)
Taxa constante quer dizer que a derivada é a variação total dividida pelo intervalo: momento final menos momento inicial, sobre t dois menos t um. Agora passa o intervalo multiplicando. A força resultante vezes o tempo em que ela age é igual ao momento final menos o inicial.

### T5-3 — tela: J⃗ = ΣF⃗ Δt = p⃗₂ − p⃗₁ (caixa); no gráfico F × t a área do retângulo acende na cor do impulso; unidades: N·s = (kg·m/s²)·s = kg·m/s
[emphatic] Esse produto, força resultante vezes intervalo, se chama impulso. É um vetor, com a direção da força, e é a área do retângulo embaixo do gráfico. E repara nas unidades: newton vezes segundo é quilograma metro por segundo ao quadrado, vezes segundo, que dá quilograma metro por segundo. Impulso e momento têm a mesma unidade, como tinha que ser.

### T5-4 — tela: bola chegando numa parede (colisão horizontal); gráfico F_x(t) com rótulo FORÇA DA PAREDE: zero, sobe rápido, pico, desce; a bola deforma e volta sincronizada com a curva
[curious] Só que numa colisão de verdade a força não é constante. Na direção da colisão, antes do contato a força é praticamente zero. Quando a bola encosta na parede, a força horizontal sobe muito rápido, chega num pico e volta a zero quando a bola se solta. Tudo em centésimos de segundo.

### T5-5 — tela: retângulos de Riemann sob F_x(t): 4 → 8 → 32; Σ F⃗ₖ Δtₖ na conta; a cada retângulo, um pedacinho de Δp⃗ se soma na seta da bola
Então a gente fatia o tempo em pedacinhos. Em cada pedacinho a força é quase constante, e vale o caso simples: o momento muda a força vezes aquele pedacinho de tempo. Somando todos os pedacinhos, aparece a soma desses retângulos. Quanto mais fino o corte, mais a soma cola na curva.

### T5-6 — tela: Σ F⃗ₖ Δtₖ → ∫ₜ₁ᵗ² ΣF⃗ dt; depois ∫ₜ₁ᵗ² (dp⃗/dt) dt = ∫ dp⃗ (limites p⃗₁ e p⃗₂) = p⃗₂ − p⃗₁; o dt se cancela e os limites trocam de t₁, t₂ para p⃗₁, p⃗₂; enquanto isso, a área do gráfico é preenchida e a seta p⃗ da bola acompanha
[emphatic] No limite, a soma vira a integral da força resultante no tempo, de t um a t dois. Agora troca a força pela derivada do momento. O dt se cancela, e os limites, que eram tempos, viram o momento inicial e o momento final. A integral de dp é só o momento final menos o inicial. Então o teorema vale para qualquer força, constante ou não: o impulso da força resultante é igual à variação do momento.

### T5-7 — tela: J⃗ = ∫ΣF⃗ dt = F⃗_méd (t₂ − t₁); área preenchida (#9CC7FF); o retângulo de mesma base e mesma área; depois duas curvas de formas diferentes e mesma área
Geometricamente, o impulso é a área embaixo da curva da força. E a força média é a força constante que, no mesmo intervalo, daria o mesmo impulso: a altura de um retângulo com a mesma base e a mesma área. Repara: duas forças com formas completamente diferentes, mas com a mesma área, dão o mesmo impulso. Só a área importa.

### T5-8 — tela: no PALCO, p⃗₁, p⃗₂ e Δp⃗ num plano xy com as componentes projetadas nos eixos; na CONTA: Jx = ∫ΣFx dt = (F_méd)x Δt = m v₂x − m v₁x; Jy = ∫ΣFy dt = (F_méd)y Δt = m v₂y − m v₁y; E O MESMO EM z
[thoughtful] E, como tudo aqui é vetor, na prática a gente escreve componente por componente. Em x, o impulso é a integral da força em x, é a força média em x vezes o intervalo, e é a massa vezes a velocidade final em x menos a inicial em x. O mesmo em y, e o mesmo em z. É exatamente isso que vai aparecer nos exercícios.

### T5-9 — tela: selo DICA: IMPULSO É VETOR: COMPONENTE POR COMPONENTE, COM SINAL
[thoughtful] Uma dica de prova: escolha os eixos, escreva componente por componente, e respeite os sinais.

## E1 — BOLA NA PAREDE

### E1-1 — tela: bola de 0,40 kg a 30 m/s para a esquerda, volta a 20 m/s; contato 0,010 s; eixo +x à direita
[thoughtful] Vamos usar o teorema do impulso, prestando atenção no sinal. Uma bola de quatrocentos gramas chega numa parede a trinta metros por segundo, para a esquerda, e volta a vinte metros por segundo, para a direita. O contato dura um centésimo de segundo.

### E1-2 — tela: vᵢ = −30 m/s, v_f = +20 m/s; J = 0,40·(20 − (−30)) = 20 N·s
Com a direita positiva, a velocidade inicial é menos trinta e a final é mais vinte. O impulso é a massa vezes a velocidade final menos a inicial: zero vírgula quatro vezes cinquenta, vinte newtons vezes segundo, para a direita.

### E1-3 — tela: a conta sem sinal 0,40·(20 − 30) = −4 N·s riscada; A PAREDE PUXOU A BOLA?
[curious] Sem o sinal, sairia menos quatro, como se a parede puxasse a bola para dentro dela. O sinal é física.

### E1-4 — tela: F_méd = 20/0,010 = 2.000 N; o peso da bola (3,9 N) como seta minúscula
A força média é vinte dividido por um centésimo: dois mil newtons, umas quinhentas vezes o peso da bola. Por isso, durante o choque, o peso some da conta.

### E1-5 — tela: DICA: REBATER PEDE MAIS IMPULSO QUE PARAR; Δp até zero × Δp até zero e volta
[thoughtful] Dica: rebater pede mais impulso do que só parar. Para parar, o momento vai até zero; para rebater, vai até zero e ainda volta.

## E2 — CHUTE EM 2D

### E2-1 — tela: bola 0,40 kg chega a 20 m/s para a esquerda; sai a 30 m/s a 45°; Δt = 0,010 s
[thoughtful] Agora as componentes entram em jogo, em duas dimensões. A mesma bola chega a vinte metros por segundo, para a esquerda, leva um chute e sai a trinta metros por segundo, a quarenta e cinco graus para cima e para a direita.

### E2-2 — tela: componentes v_f,x = v_f,y = 21,2 m/s; Jx = 0,40·(21,2 + 20) = 16,5 N·s; Jy = 0,40·21,2 = 8,5 N·s
Componente por componente: a velocidade final tem as duas partes iguais, uns vinte e um vírgula dois metros por segundo. O impulso horizontal dá dezesseis vírgula cinco newtons vezes segundo, e o vertical, oito vírgula cinco.

### E2-3 — tela: triângulo p⃗ᵢ, p⃗_f, Δp⃗; F⃗_méd = 1,9×10³ N a 27°; arcos de 27° e 45°
[curious] Dividindo pelo tempo, a força média tem uns mil e novecentos newtons, a vinte e sete graus. Mas a bola saiu a quarenta e cinco! A força não decide para onde a bola vai; ela decide quanto o momento muda. Ela aponta na direção da variação do momento, a seta que fecha o triângulo.

### E2-4 — tela: DICA: F_MÉD APONTA PARA Δp, NÃO PARA A VELOCIDADE FINAL
[thoughtful] Dica: desenhe o triângulo de momentos. A força média está sempre na direção da variação do momento.

## E3 — FORÇA QUE CRESCE COM O TEMPO

### E3-1 — tela: foguete 2.150 kg no espaço; F = A t² com o ponto (1,25 s; 781,25 N); A = 500 N/s²
[thoughtful] Agora uma força que muda com o tempo, para usar a integral de verdade. Um foguete de dois mil cento e cinquenta quilos, no espaço, com um motor cuja força cresce com o quadrado do tempo: em um vírgula vinte e cinco segundo, ela vale setecentos e oitenta e um vírgula vinte e cinco newtons. A massa, aqui, a gente trata como constante. A constante sai dividindo pelo tempo ao quadrado: quinhentos newtons por segundo ao quadrado.

### E3-2 — tela: retângulos de Riemann entre 2,0 e 3,5 s convergindo; depois J = (500/3)(3,5³ − 2,0³) ≈ 5,81×10³ N·s
Qual é o impulso entre dois segundos e três e meio? É a área embaixo da parábola. Os retângulos mostram a ideia; a integral faz a conta: a integral do tempo ao quadrado é o tempo ao cubo sobre três. Dá uns cinco mil oitocentos e doze newtons vezes segundo.

### E3-3 — tela: Δv = J/m = 2,70 m/s; retângulo da força média 3.875 N
[curious] Dividindo pela massa, a velocidade aumenta dois vírgula setenta metros por segundo nesse intervalo. E a força média do trecho, área dividida por um segundo e meio, é de uns três mil oitocentos e setenta e cinco newtons.

## T6 — MOMENTO × ENERGIA CINÉTICA

### T6-1 — tela: uma seta de força sobre um bloco; dois painéis: ×Δt → IMPULSO → Δp e ×d → TRABALHO → ΔK
[thoughtful] Agora o insight mais importante do capítulo. A mesma força resultante pode ser somada de dois jeitos. Somada no tempo, ela dá o impulso, que muda o momento. Somada na distância, ela dá o trabalho, que muda a energia cinética.

### T6-2 — tela: K = p²/(2m) nascendo de K = ½mv² e p = mv (substituição animada)
E as duas grandezas se conversam: a energia cinética é o momento ao quadrado dividido por duas vezes a massa.

### T6-3 — tela: duas bolas: 0,50 kg a 4,0 m/s e 0,10 kg a 20 m/s; p = 2,0 kg·m/s nas duas; K = 4 J × 20 J; a mão recuando 1× e 5×
[curious] Olha esse exemplo. Você vai agarrar uma bola de meio quilo a quatro metros por segundo ou uma de cem gramas a vinte. As duas têm o mesmo momento, dois quilogramas metro por segundo. Então pedem o mesmo impulso: com a mesma força média, levam o mesmo tempo para parar. Mas a bola leve tem cinco vezes mais energia cinética, vinte joules contra quatro. Com a mesma força, a sua mão precisa recuar cinco vezes mais.

### T6-4 — tela: dois barcos no gelo (m e 2m), o mesmo vento, a mesma linha de chegada: MESMA ENERGIA, MOMENTO √2 VEZES MAIOR no pesado
[thoughtful] E o contrário: dois barcos no gelo, um com o dobro da massa do outro, empurrados pelo mesmo vento até a mesma linha de chegada. Mesma força, mesma distância: mesma energia cinética na chegada. Só que o pesado demora mais, fica mais tempo sob a força, e chega com raiz de dois vezes mais momento.

### T6-5 — tela: DICA: TEMPO → IMPULSO → MOMENTO · DISTÂNCIA → TRABALHO → ENERGIA
[emphatic] Guarda essa dica: se o problema fala de tempo, pense em impulso e momento. Se fala de distância, pense em trabalho e energia.

## E4 — DE VOLTA AO MURO

### E4-1 — tela: o muro em 3D recuado; 80 kg, h = 2,5 m; v = √(2·9,8·2,5) = 7,0 m/s; Δp = 560 kg·m/s
[curious] Agora sim, o muro. A pessoa tem oitenta quilos e cai de dois metros e meio: chega a sete metros por segundo. Para parar, o momento dela cai de quinhentos e sessenta quilogramas metro por segundo até zero, nos dois casos.

### E4-2 — tela: dois gráficos F_res(t) com a mesma área 560 N·s: PERNAS DURAS (Δt = 0,01 s) × JOELHOS (Δt ≈ 0,143 s)
[emphatic] Então o impulso resultante é o mesmo nas duas aterrissagens. O que muda é a forma da curva. De perna dura, o corpo para em um centésimo de segundo. Dobrando os joelhos e descendo, digamos, meio metro, leva uns catorze centésimos.

### E4-3 — tela: CAMINHO 1 (IMPULSO): F_res,méd = 560/Δt → 56.000 N × 3.920 N
[thoughtful] Primeiro caminho, pelo impulso: dividindo a mesma área por tempos tão diferentes, a força resultante média é de cinquenta e seis mil newtons de perna dura, e três mil novecentos e vinte dobrando os joelhos.

### E4-4 — tela: CAMINHO 2 (TRABALHO): F_res·d = ΔK = ½·80·7,0² = 1.960 J; d = 0,5 m → 3.920 N; d = 3,5 cm → 56.000 N
Segundo caminho, pela dica que a gente acabou de ver: o problema também tem uma distância. A energia cinética na chegada é mil novecentos e sessenta joules. Para tirá-la em meio metro de agachamento, a força resultante média é de três mil novecentos e vinte newtons. De perna dura, o corpo para em só três centímetros e meio, e dá de novo cinquenta e seis mil. Os dois teoremas concordam.

### E4-5 — tela: N = F_res + m g; faixa do peso (784 N); ≈ 72 PESOS × ≈ 6 PESOS
[thoughtful] Só que a pergunta é com que força o chão empurra você, e o chão ainda segura o seu peso. Somando o peso: umas setenta e duas vezes o seu peso de perna dura... e umas seis vezes dobrando os joelhos.

### E4-6 — tela: MAIS TEMPO E MAIS DISTÂNCIA · MENOS FORÇA; mini-tabela: SAQUE ≈ 49 kgf · PÊNALTI ≈ 92 kgf · CARRO A 60 km/h ≈ 25 tf
[excited] Está aí a resposta. Dobrar os joelhos não muda o impulso resultante: muda o tempo e a distância da parada, e isso derruba a força nos seus ossos. É a física do airbag, do capacete e do colchão do salto em altura. Só como curiosidade, num carro de uma tonelada e meia parando num muro em um décimo de segundo, são umas vinte e cinco toneladas-força.

## E5 — A PULGA

### E5-1 — tela: pulga (2 mg) pulando 50 cm; zoom nas patas esticando 1 mm
[curious] Agora um desafio de verdade. Uma pulga de dois miligramas pula cinquenta centímetros de altura. Durante o impulso, ela estica as patas e sobe só um milímetro antes de sair do chão. Com que força média ela empurra o chão, comparada com o peso dela?

### E5-2 — tela: v = √(2gh) = 3,13 m/s; CAMINHO 1 (DISTÂNCIA): a = v²/(2d) = g·h/d = 500 g
[thoughtful] Para subir meio metro, ela sai a uns três vírgula um metros por segundo. O problema dá uma distância, um milímetro, então vamos pela distância: a aceleração é a velocidade ao quadrado sobre duas vezes a distância, que dá a gravidade vezes a altura do pulo dividida por um milímetro. Quinhentas vezes a gravidade.

### E5-3 — tela: CAMINHO 2 (TEMPO): Δt = 2d/v = 0,64 ms; F_res = m v/Δt = m v²/(2d) (as duas expressões se fundem)
Pelo tempo também dá: o empurrão dura uns sessenta e quatro centésimos de milissegundo, e o momento final dividido por esse tempo dá exatamente a mesma força. É a mesma física pelos dois teoremas.

### E5-4 — tela: N = m(a + g) = m g (h/d + 1) = 501 PESOS; o "+1" pisca; DICA: CONTATO ≠ RESULTANTE
[emphatic] E a armadilha: a pergunta é a força que a pulga faz no chão, não a força resultante. Como no muro, o chão também segura o peso dela. São quinhentos e um pesos, e não quinhentos. Dica: força de contato não é força resultante.

### E5-5 — tela: N ≈ 1,0×10⁻³ kgf; silhueta humana de 70 kg ao lado de um bloco de 35 t
[curious] Em números, um grama-força. Parece nada. Mas, proporcionalmente, é como se uma pessoa de setenta quilos empurrasse o chão com o peso de trinta e cinco toneladas.

## SÍNTESE

### S1 — tela: as duas curvas F_res(t) do muro com a mesma área
[thoughtful] Então, a pergunta do começo. Dobrar os joelhos não muda o impulso resultante necessário para parar você: ele continua sendo a variação do momento. O que muda é o tempo, e com ele a distância. Mais tempo, menos força média.

### S2 — tela: p⃗ = m v⃗ · J⃗ = ∫F⃗_res dt = Δp⃗ · TEMPO → MOMENTO · DISTÂNCIA → ENERGIA
Resumindo: o momento é a grandeza que a natureza conserva. O impulso da força resultante é a área embaixo da força no tempo e é igual à variação do momento. E o tempo conversa com o momento, enquanto a distância conversa com a energia.

## ENCERRAMENTO

### F1 — tela: FadeOut geral; logo com anéis; INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
Se essa aula ajudou você, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### F2 — tela: (3D ou 2D) um cavalo puxando uma pedra por uma corda; SE A CORDA PUXA O CAVALO PARA TRÁS COM A MESMA FORÇA, COMO ELE ANDA? → PRÓXIMO VÍDEO: CONSERVAÇÃO DO MOMENTO EM SISTEMAS (ciano)
[curious] E fica a pergunta para o próximo: se a corda puxa o cavalo para trás com a mesma força com que puxa a pedra para a frente, como é que o cavalo consegue andar? No próximo vídeo: o momento de um sistema inteiro. Até a próxima!

---

## Números de conferência (g = 9,8 m/s²)

| Bloco | Valor | Exato |
|---|---|---|
| E1 | 20 N·s; 2.000 N; ~500 pesos da bola | 20; 2000; 510 |
| E2 | 21,2; 16,5 e 8,5 N·s; ~1.900 N a 27° | 21,21; 16,49 e 8,49; 1.854 N a 27,2° |
| E3 | 500 N/s²; ~5.812 N·s; 2,70 m/s; ~3.875 N | 500; 5.812,5; 2,703; 3.875 |
| T6 | p = 2,0; K = 4 e 20 J; razão de p dos barcos √2 | ok |
| E4 | 7,0 m/s; 560; 0,01 s e 1/7 s; 56.000 e 3.920 N; ΔK = 1.960 J; d = 0,5 m e 3,5 cm; 72 e 6 pesos | 72,4 e 6,0 |
| E5 | 3,13 m/s; 500 g; 0,64 ms; 501 pesos; 1 gf; 35 t | 3,130; 0,639 ms; 35,07 t |

**Contagem:** ~2938 palavras → ~18.1 min de fala a 2,7 palavras/s (mais as pausas visuais).

---

## Fontes (só para a descrição do YouTube; nada disso vai para a tela nem para a fala)
- Teoria: Sears & Zemansky, Física I, 14ª ed., §8.1 (segunda lei com momento, componentes, teorema do impulso, momento × energia cinética); H. Moysés Nussenzveig, Curso de Física Básica 1, §4.5 (experiências com discos, conservação → terceira lei); Feynman, Lições de Física I, cap. 10 (argumento de simetria; momento do campo).
- Exercício 1: Sears, Exemplo 8.2 · Exercício 2: Sears, Exemplo 8.3 · Exercício 3: Sears, Exercício 8.11 · Exercício 4: Moysés, Problema 9.1 (com o caminho do trabalho) · Exercício 5: Moysés, Problema 4.7.

## Texto corrido (para gravação)
O texto corrido do anexo v4 é a concatenação das falas acima, na ordem das âncoras (não repetido aqui).
