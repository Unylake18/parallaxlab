# yt_0015 — MOMENTO LINEAR E IMPULSO · sugestão de narração v5 (sobre o preview v6)

Data: 2026-10-29. Escrita em cima do preview v6 (`renders/preview_yt0015_v6_960x540.mp4`, 18:15), analisado âncora por âncora, com o
conteúdo do handoff v4 (T1 da segunda lei, T2 discos, T3 simetria, T4 terceira lei, T5 impulso, E1–E5, T6, síntese). A v4
(`narracao_sugestao.md`) continua sendo a fonte dos tempos do preview; esta v5 é a proposta para a voz.

**Padrão:** `docs/padrao_video_longo.md` §5 e `docs/roteiro_voz_elevenlabs_v4.md`. Professor de cursinho, próximo, "a gente" e "você",
conectivos em toda virada, **nunca a letra solta** (sempre o nome da grandeza), no máximo uma brincadeira por cena. A animação se molda à
voz, então a fala pode explicar com calma: o que importa é o aprendizado.

**Como ler:** cada `###` é uma âncora (os IDs são os mesmos do `cena.py`, então a sincronia só estica a cena). `tela:` descreve o que o v6
já mostra. Linhas com `>` são notas para a animação (não são faladas); ⚠ marca um ajuste de tela que a fala pede. Tags do ElevenLabs v4
em inglês, uma por trecho.

**Notação falada** (o símbolo da tela, e como a voz diz): p⃗ = **o momento** (ou momento linear); P⃗ = **o momento total**; v⃗ = **a
velocidade**; ΣF⃗ ou F⃗_res = **a força resultante**; a⃗ = **a aceleração**; m = **a massa**; J⃗ = **o impulso**; Δp⃗ = **a variação do
momento**; dp⃗ e dt = **um pedacinho de momento** e **um pedacinho de tempo**; t₁, t₂ = **o instante inicial** e **o instante final**;
F_méd = **a força média**; K = **a energia cinética**; N = **a força do chão** (a normal); m g = **o peso**; h = **a altura**; d = **a
distância de freada** (ou de agachamento, ou o esticão das patas da pulga).

**Hipóteses ditas uma vez:** massa constante (T1); colchão de ar e trilho de ar sem atrito (T2, T3); choque curto, em que o peso fica
pequeno perto da força do choque (E1), e quando o peso volta para a conta (E4, E5); gelo sem atrito (T6).

---

## HOOK

### H1 — tela: (3D) muro de 2,5 m; o manequim pula e chega de pernas esticadas; CÂMERA LENTA no impacto
[curious] Olha essa queda. O nosso boneco de testes pula de um muro de dois metros e meio e chega no chão de pernas esticadas, duras feito um cabo de vassoura. Em câmera lenta dá para ver: o corpo para quase de uma vez, e o tranco vai direto para os ossos.

### H2 — tela: (3D) a mesma queda, agora os joelhos dobram e o quadril desce
Agora a mesma queda, do mesmo muro, com o mesmo boneco. Só que, dessa vez, ele chega dobrando os joelhos e deixando o quadril descer.

### H3 — tela: (3D) as duas aterrissagens lado a lado: PERNAS DURAS × JOELHOS DOBRADOS; POR QUE DOBRAR OS JOELHOS SALVA SUAS PERNAS?
[thoughtful] Pensa comigo: a altura é a mesma, a velocidade de chegada é a mesma, e nos dois casos o corpo termina parado. Então por que dobrar os joelhos salva as suas pernas? Spoiler: não é mágica, nem academia de perna. São duas ideias da física que a gente vai construir hoje: momento linear e impulso.

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: título MOMENTO LINEAR E IMPULSO; depois os painéis NESTE VÍDEO: UM CORPO (uma bola empurrada por uma força, com a velocidade crescendo) e NO PRÓXIMO: VÁRIOS CORPOS (miniaturas de colisões com P⃗ᵢ = P⃗_f)
[thoughtful] Hoje o assunto é momento linear e impulso, com um foco bem claro: um corpo só e uma força agindo nele ao longo do tempo. Olha a bolinha: a força empurra, e a velocidade cresce enquanto a força age. À direita, o próximo capítulo da série: vários corpos batendo, e o momento total se conservando.

### A3 — tela: as miniaturas vão para o centro: DOS VÍDEOS DE COLISÕES; P⃗ᵢ = P⃗_f em destaque
[curious] Nos vídeos de colisões, essa igualdade foi a nossa ferramenta: momento total antes igual ao momento total depois. Hoje a gente vai até a raiz dela.

## T1 — DE ONDE VEM O MOMENTO

### T1-1 — tela: eixos x, y, z; uma partícula de aço de massa m percorre uma curva no espaço; selo SEGUNDA LEI DE NEWTON; a velocidade (violeta) tangente à curva e a força resultante (azul); na conta: ΣF⃗ = m a⃗
[thoughtful] Vamos começar do que você já conhece: a segunda lei de Newton. Uma bolinha de aço fazendo uma trajetória qualquer pelo espaço. Em cada instante ela tem uma velocidade, a seta violeta, tangente à trajetória, e sente uma força resultante, a seta azul, que aponta para o lado de dentro da curva. A segunda lei diz: força resultante é massa vezes aceleração.

### T1-2 — tela: LUPA: a velocidade em dois instantes próximos, da mesma origem; a diferença entre elas encolhe (Δt → 0) e vira dv⃗, paralela à força; a⃗ = dv⃗/dt entra na conta: ΣF⃗ = m dv⃗/dt; o m entra na derivada: ΣF⃗ = d(m v⃗)/dt; selo MASSA CONSTANTE
[curious] Mas o que é a aceleração? Vamos usar uma lupa. Pego a velocidade agora e a velocidade um instantinho depois, saindo do mesmo ponto. A diferença entre elas é a variação da velocidade, e repara: conforme o intervalo encolhe, ela aponta junto com a força. A aceleração é essa variação dividida pelo pedacinho de tempo: a derivada da velocidade. Então a força resultante é a massa vezes a derivada da velocidade. E, se a massa não muda, ela entra na derivada sem alterar nada: a força resultante é a derivada da massa vezes a velocidade.

### T1-3 — tela: a seta magenta do momento nasce da seta da velocidade, esticada pela massa; p⃗ = m v⃗ na caixa; MOMENTO LINEAR · OU QUANTIDADE DE MOVIMENTO; [p] = kg·m/s
[thoughtful, emphatic] Esse produto, massa vezes velocidade, aparece tanto que ganhou nome: momento linear, ou quantidade de movimento. Na tela, ele vai ser sempre esta seta magenta. Como a massa é positiva, o momento aponta para o mesmo lado da velocidade: é a mesma seta, esticada pela massa. E a unidade sai da definição: quilograma vezes metro por segundo.

### T1-4 — tela: vista de cima, duas estradas: dois carros iguais a 20 m/s, um para o norte e outro para o leste, com setas magenta iguais; |p⃗₁| = |p⃗₂| (MESMO TAMANHO) e p⃗₁ ≠ p⃗₂ (DIREÇÕES DIFERENTES); as duas setas copiadas para uma origem comum
[curious] E atenção: o momento é um vetor de verdade. Dois carros iguais, a vinte metros por segundo, um indo para o norte e o outro para o leste. O tamanho do momento é o mesmo. Mas os momentos são diferentes, porque apontam para lados diferentes. Nenhum GPS vai dizer que esses carros vão para o mesmo lugar.

### T1-5 — tela: de volta à partícula; CÓPIA DE v⃗ NA ORIGEM; a caixa tracejada até os três eixos; as componentes da velocidade acendem nos eixos e descem para a conta: pₓ = m vₓ · p_y = m v_y · p_z = m v_z; TRÊS EQUAÇÕES ESCALARES NO LUGAR DE UMA VETORIAL
[thoughtful] Na prática, a gente trabalha com componentes. Copio a seta da velocidade para a origem e projeto nos três eixos: aparece a parte da velocidade em x, em y e em z. E cada parte do momento é a massa vezes a parte da velocidade na mesma direção. Três equações com números no lugar de uma com setas.

### T1-6 — tela: ΣF⃗ = dp⃗/dt na caixa; a partícula anda devagar com a força resultante nela; painel com três barras magenta (pₓ, p_y, p_z) com as setinhas azuis da força ao lado; ΣFₓ = dpₓ/dt · ΣF_y = dp_y/dt · ΣF_z = dp_z/dt acendendo uma de cada vez; CADA DIREÇÃO CUIDA DA SUA
[thoughtful] Agora volta na segunda lei e troca massa vezes velocidade pelo nome novo: a força resultante é a taxa de variação do momento. Olha o painel: cada barra magenta é uma componente do momento, e a setinha azul ao lado é a componente da força. Seta para cima, a barra cresce; seta para baixo, a barra diminui. A força em x só mexe no momento em x, e o mesmo vale em y e em z. Cada direção cuida da sua vida.

### T1-7 — tela: ΣF⃗ = dp⃗/dt; selos A FORMA ORIGINAL DE NEWTON e REFERENCIAL INERCIAL; um foguete andando e soltando gás; MASSA VARIÁVEL; ESSE CASO FICA PARA UM VÍDEO DESTA SÉRIE
[curious] Curiosidade: foi assim, falando em quantidade de movimento, que o próprio Newton escreveu a segunda lei. Ela vale em referenciais inerciais e é até mais geral do que massa vezes aceleração: continua fazendo sentido quando a massa muda, como num foguete jogando gás para trás. Mas esse caso fica para um vídeo desta série. Hoje a massa fica quietinha.

## T2 — O FATO EXPERIMENTAL

### T2-1 — tela: COLCHÃO DE AR · VISTO DE CIMA; SEM FORÇA DE FORA?; EXPERIÊNCIA 1: dois discos iguais vêm um contra o outro com a mesma velocidade e trocam de velocidade
[thoughtful] Então a força resultante muda o momento. E se nenhuma força de fora agir? Vamos ao laboratório. Dois discos iguais sobre um colchão de ar, tipo uma mesa de air hockey: o ar por baixo elimina o atrito. Na primeira experiência, eles vêm um contra o outro com a mesma velocidade, batem... e voltam, cada um com a velocidade do outro.

### T2-2 — tela: EXPERIÊNCIA 2: um disco parado; o outro chega com v; quem vinha para e o parado sai com v
Na segunda, um disco está parado e o outro chega. Depois da batida, quem vinha para, e quem estava parado sai com a velocidade do primeiro. Igualzinho à sinuca.

### T2-3 — tela: EXPERIÊNCIA 3: um pedacinho de CHICLETE num dos discos; batem, grudam e o conjunto segue com metade da velocidade
Na terceira, a gente gruda um pedacinho de chiclete num dos discos, e não pergunta de onde veio esse chiclete. Eles batem, ficam juntos, e o conjunto segue com metade da velocidade.

### T2-4 — tela: tabela ANTES | DEPOIS montada linha a linha a partir dos discos, que repetem cada experiência à esquerda; em cada linha, massa vezes velocidade de um mais a do outro, e o total igual nas duas colunas
[curious] Três finais completamente diferentes. Mas olha a tabela: em cada linha, a massa vezes a velocidade de um disco mais a do outro. Antes e depois, essa soma é a mesma nas três. E com massas diferentes ela continua a mesma.

### T2-5 — tela: a experiência 3 em loop lento, com as setas do momento de cada disco e a soma (sempre do mesmo tamanho); P⃗ = p⃗₁ + p⃗₂ = constante; PRINCÍPIO DE CONSERVAÇÃO DO MOMENTO (SISTEMA ISOLADO)
[thoughtful, emphatic] Isso é uma lei da natureza, tirada direto da experiência: o princípio de conservação do momento. Os momentos de cada disco mudam na batida, mas a soma, o momento total, fica sempre do mesmo tamanho. Num sistema isolado, ele não muda.

## T3 — POR QUE MASSA VEZES VELOCIDADE?

### T3-1 — tela: trilho de ar; os carrinhos iguais A e B deslizam até o centro e se encaixam numa mola comprimida, presa por uma trava; candidatos v ?, m v ? (em destaque) e m v² ?; DOIS CARRINHOS IGUAIS · PARADOS; a trava queima, a mola empurra, os dois saem; estroboscópio; MESMO EMPURRÃO, MESMA VELOCIDADE
[curious] Mas por que justamente massa vezes velocidade? Por que não a velocidade sozinha, ou a massa vezes a velocidade ao quadrado? Tem um argumento de simetria muito bonito para isso. Dois carrinhos iguais, parados, com uma mola comprimida entre eles, presa por uma trava. A trava solta, a mola empurra. E, como os carrinhos são iguais, não tem por que um sair mais rápido: saem com a mesma velocidade, um para cada lado. Os fantasmas são fotos a cada meio segundo, e o espaçamento é igual dos dois lados.

### T3-2 — tela: os dois voltam um contra o outro com a mesma velocidade, com velcro na frente; batem, grudam e param; v = 0; IGUAIS E OPOSTOS: O CONJUNTO PARA
[thoughtful] Agora o filme ao contrário: velcro na frente, os dois vêm um contra o outro com a mesma velocidade, batem, grudam... e param. Pura simetria.

### T3-3 — tela: a tela se divide: VISTA DO CHÃO em cima e VISTA DE QUEM ANDA JUNTO COM A embaixo, com uma câmera de vídeo sobre o carrinho A; embaixo, A parado, a régua e o chão correndo para a esquerda (CHÃO: v), B chegando com 2v; CÂMERA LENTA no contato, com uma linha ligando as duas faixas; o conjunto sai com v; MESMA COLISÃO · OUTRO REFERENCIAL
[curious] Agora vem o truque. Assista à mesma colisão com uma câmera que anda junto com o carrinho da esquerda. Em cima, quem está parado no chão; embaixo, a câmera. Para ela, o carrinho A está parado e quem anda é o chão: olha a régua correndo. O outro carrinho chega com o dobro da velocidade. E o conjunto, que no chão ficava parado, para a câmera passa andando com a velocidade original. Mesma colisão, outro ponto de vista.

### T3-4 — tela: só a faixa de baixo; a colisão 2v → 0 roda devagar; os rótulos voam dos carrinhos para a conta: m·2v + m·0 = 2m·v; depois os casos m × 2m (m·2v + 2m·(−v) = 3m·0) e 2m × 3m (2m·3v + 3m·(−2v) = 5m·0), com o histórico descendo; ANTES = DEPOIS, SEMPRE
[thoughtful] Então a gente ganhou, sem conta nenhuma, uma colisão nova: um carrinho com o dobro da velocidade bate num igual parado, e os dois seguem com metade dela. Olha a conta nascendo dos rótulos: massa vezes o dobro da velocidade, mais zero, dá o dobro da massa vezes a velocidade. Com a velocidade sozinha, ou ao quadrado, não fecharia. E, repetindo o truque com massas diferentes, sempre fecha.

### T3-5 — tela: o carrinho A com as setas da velocidade e do momento; os selos DA SEGUNDA LEI e DA SIMETRIA convergem para um p⃗ = m v⃗; MOMENTO LINEAR
[thoughtful, emphatic] Repara: a grandeza que a segunda lei de Newton entregou lá no começo é a mesma que a simetria aponta agora. Dois caminhos diferentes, o mesmo lugar. Não é coincidência. É o momento linear.

## T4 — DA CONSERVAÇÃO À TERCEIRA LEI

### T4-1 — tela: os discos da experiência 2 em loop; as setas da variação do momento saem do ponto de contato; Δp⃗₁ = −Δp⃗₂; O QUE UM GANHA, O OUTRO PERDE
[thoughtful] Agora uma virada que vale ouro. Se o momento total não muda, tudo o que um disco ganha o outro perde. A variação do momento do primeiro é menos a variação do momento do segundo.

### T4-2 — tela: um cronômetro da colisão; os dois lados divididos pelo intervalo de tempo; o intervalo encolhe (Δt → 0): dp⃗₁/dt = −dp⃗₂/dt; TAXA DE VARIAÇÃO DO MOMENTO
Divide os dois lados pelo tempo da colisão, e vai encolhendo esse tempo, como no cronômetro. O que sobra é a taxa de variação: a derivada do momento de um é menos a derivada do momento do outro, a cada instante.

### T4-3 — tela: as derivadas viram forças: F⃗₁₍₂₎ = −F⃗₂₍₁₎ (caixa); as setas azuis iguais e opostas nos discos; TERCEIRA LEI DE NEWTON
[thoughtful, emphatic] Só que, lembra do começo? A taxa de variação do momento é a força. Então a força que o segundo disco faz no primeiro é igual e oposta à que o primeiro faz no segundo. Olha só quem apareceu: a terceira lei de Newton, saindo da conservação do momento.

### T4-4 — tela: bloco numa mesa, com o peso e a normal no bloco (AS DUAS NO BLOCO); a Terra (FORA DE ESCALA) com a reação do peso, −P⃗, puxada para cima; AÇÃO E REAÇÃO AGEM EM CORPOS DIFERENTES
[curious] E aqui mora uma pegadinha clássica. Ação e reação agem sempre em corpos diferentes. O peso e a normal estão os dois no bloco, então não são ação e reação. A reação do peso é o bloco puxando a Terra para cima. E a Terra está fora de escala, tá? Prometo que ela é um pouquinho maior.

### T4-5 — tela: duas cargas em movimento, com velocidades e forças que não são opostas: F⃗₁₍₂₎ ≠ −F⃗₂₍₁₎, ENTRE CARGAS EM MOVIMENTO; uma nuvem de campo em volta; MOMENTO DAS PARTÍCULAS + MOMENTO DO CAMPO = CONSTANTE
[thoughtful] E por que partir da conservação? Porque ela é mais funda. Entre cargas elétricas em movimento, as forças podem não ser iguais e opostas: a terceira lei falha. Mas a conservação continua valendo se a gente contar também o momento do campo. Ela sobrevive onde a terceira lei não chega.

## T5 — IMPULSO

### T5-1 — tela: um bloco num piso SEM ATRITO; a força resultante constante age de t₁ a t₂ (cronômetro); a seta do momento cresce; à direita, o gráfico da força no tempo (um degrau) e, embaixo, o do momento no tempo (uma rampa); inclinação = ΣF
[thoughtful] Agora o impulso, passo a passo. O caso mais simples: um bloco sem atrito e uma força resultante constante, que liga num instante e desliga noutro. Olha os gráficos andando juntos. Em cima, a força: um degrau. Embaixo, o momento: como a taxa de variação dele é a força, e a força é constante, ele sobe em linha reta. A inclinação da reta é a própria força.

### T5-2 — tela: o triângulo de inclinação no gráfico do momento; o cateto vertical (p⃗₂ − p⃗₁) e o horizontal (t₂ − t₁) voam para a conta: ΣF⃗ = dp⃗/dt → ΣF⃗ = (p⃗₂ − p⃗₁)/(t₂ − t₁) → ΣF⃗ (t₂ − t₁) = p⃗₂ − p⃗₁
Com taxa constante, a derivada é a variação total dividida pelo intervalo. No triângulo: na vertical, o momento final menos o inicial; na horizontal, o instante final menos o inicial. Agora passa o intervalo para o outro lado, multiplicando: força resultante vezes o tempo em que ela age é igual ao momento final menos o inicial.

### T5-3 — tela: J⃗ = ΣF⃗ Δt = p⃗₂ − p⃗₁ (caixa); IMPULSO · VETOR, NA DIREÇÃO DA FORÇA; o retângulo embaixo do degrau acende; N·s = (kg·m/s²)·s = kg·m/s (um segundo cancela); A MESMA UNIDADE DO MOMENTO
[thoughtful, emphatic] Esse produto, força resultante vezes intervalo, se chama impulso. É um vetor, na direção da força, e é a área do retângulo embaixo do gráfico. E as unidades: newton vezes segundo é quilograma vezes metro por segundo ao quadrado, vezes segundo; um segundo cancela, e sobra quilograma vezes metro por segundo. A mesma unidade do momento, como tinha que ser.

### T5-4 — tela: uma bola chega numa parede e volta, amassando e desamassando; o gráfico Fₓ(t) com o rótulo FORÇA DA PAREDE: zero, sobe rápido, pico, desce; CENTÉSIMOS DE SEGUNDO
[curious] Só que, numa colisão de verdade, a força não é constante. Antes do contato, a força da parede é praticamente zero. Quando a bola encosta, ela sobe muito rápido, chega num pico enquanto a bola amassa, e volta a zero quando ela se solta. Tudo em centésimos de segundo.

### T5-5 — tela: retângulos embaixo da curva: RETÂNGULOS 4 → 8 → 32; cada retângulo vira um pedacinho da variação do momento, somado na seta da bola; Σₖ F⃗ₖ Δtₖ na conta; QUANTO MAIS FINO, MAIS COLA NA CURVA
[thoughtful] Então a gente faz o que todo bom físico faz: fatia o problema. Em cada pedacinho de tempo, a força é quase constante, e vale o caso simples: o momento muda a força vezes o pedacinho. Cada retângulo vira um pedacinho da variação do momento, somado na seta da bola. Quatro, oito, trinta e dois... quanto mais fino, mais a soma cola na curva.

### T5-6 — tela: a soma vira a integral: J⃗ = ∫ₜ₁ᵗ² ΣF⃗ dt; depois = ∫ (dp⃗/dt) dt; o dt se cancela e os limites viram p⃗₁ e p⃗₂: = ∫ dp⃗ = p⃗₂ − p⃗₁; a área enche da esquerda para a direita e a seta do momento da bola acompanha; O IMPULSO DA FORÇA RESULTANTE É A VARIAÇÃO DO MOMENTO
[thoughtful, emphatic] No limite, a soma vira a integral da força resultante no tempo, do instante inicial ao final. Agora troca a força pela derivada do momento: o pedacinho de tempo cancela, e os limites, que eram instantes, viram o momento inicial e o final. Somar pedacinhos de momento dá o momento final menos o inicial. Então vale para qualquer força: o impulso da força resultante é igual à variação do momento.

### T5-7 — tela: J⃗ = ∫ΣF⃗ dt = F⃗_méd (t₂ − t₁); o retângulo da força média com a mesma base (MESMA BASE, MESMA ÁREA), com F_méd ao lado; embaixo, uma outra curva, de forma triangular; ÁREA = 20,0 N·s nas duas; SÓ A ÁREA IMPORTA
Geometricamente, o impulso é a área embaixo da curva da força. E a força média é a força constante que daria o mesmo impulso no mesmo intervalo: a altura de um retângulo com a mesma base e a mesma área. Olha embaixo: outra forma, mesma área, vinte newtons vezes segundo. Mesmo impulso. Só a área importa.

### T5-8 — tela: plano xy com o momento inicial, o momento final e a variação Δp⃗ = J⃗ fechando o triângulo; as projeções tracejadas Jₓ e J_y nos eixos; na conta, Jₓ = ∫ΣFₓ dt = (F_méd)ₓ Δt = m v₂ₓ − m v₁ₓ e o mesmo para y; E O MESMO EM z
[thoughtful] E, como o impulso é um vetor, a gente trabalha componente por componente. A variação do momento vai da ponta do momento inicial até a ponta do final; projetando, aparece o impulso em x e em y. Em x, o impulso é a integral da força em x, é a força média em x vezes o intervalo, e é a massa vezes a velocidade final em x menos a inicial. Em y, a mesmíssima coisa, e em z também.

### T5-9 — tela: DICA: IMPULSO É VETOR: COMPONENTE POR COMPONENTE, COM SINAL
[thoughtful] Uma dica que vale ponto na prova: escolha os eixos, escreva componente por componente, e respeite os sinais.

## E1 — BOLA NA PAREDE

### E1-1 — tela: parede; eixo +x para a direita; ANTES: bola a 30 m/s para a esquerda; DEPOIS: bola a 20 m/s para a direita; m = 0,40 kg (a bola acende); Δt = 0,010 s (flash no contato com a parede)
[thoughtful] Hora de colocar a mão na massa, começando pelo sinal, que é onde todo mundo escorrega. Uma bola de quatrocentos gramas chega numa parede a trinta metros por segundo, para a esquerda, e volta a vinte, para a direita. O contato dura um centésimo de segundo. Primeiro passo: escolher o positivo. Aqui, para a direita.

### E1-2 — tela: vᵢ = −30 m/s · v_f = +20 m/s; o momento inicial (←), o final (→) e a variação (→) em três linhas, com tracejados ligando as pontas; J = 0,40 (20 − (−30)) = 20 N·s
Então a velocidade inicial é menos trinta e a final é mais vinte. Olha as três setas: o momento inicial para a esquerda, o final para a direita, e a variação ligando as pontas, para a direita. O impulso é a massa vezes a velocidade final menos a inicial: zero vírgula quatro vezes cinquenta. Vinte newtons vezes segundo, para a direita.

### E1-3 — tela: a conta sem sinal, 0,40 (20 − 30) = −4 N·s, riscada; A PAREDE PUXOU A BOLA?
[curious] Sem o sinal, alguém faria vinte menos trinta e acharia menos quatro, como se a parede puxasse a bola. Parede com ímã de bola não existe. O sinal é física.

### E1-4 — tela: a bola encostada na parede; a força média sai da bola para a direita; F_méd = 20/0,010 = 2.000 N; o peso, minúsculo, mg = 3,9 N; UMAS 500 VEZES O PESO
[thoughtful] E a força? A força média é o impulso dividido pelo tempo: vinte sobre um centésimo, dois mil newtons. Perto disso, o peso, três vírgula nove newtons, é uma setinha. Umas quinhentas vezes menor. Por isso, num choque rápido, o peso sai da conta sem culpa.

### E1-5 — tela: o ANTES/DEPOIS volta; PARAR × REBATER, com a variação do momento em cada caso; |Δp⃗|: 12 → 20 kg·m/s; DICA: REBATER PEDE MAIS IMPULSO QUE PARAR
[thoughtful] E repara: para só parar a bola, o momento iria de doze até zero. Para rebater, vai até zero e ainda volta: a variação sobe para vinte. Rebater pede mais impulso do que parar. Por isso bola que quica na mão arde mais.

## E2 — CHUTE EM 2D

### E2-1 — tela: ANTES: a bola chega a 20 m/s para a esquerda; o pé; DEPOIS: ela sai a 30 m/s, a 45° acima da horizontal; m = 0,40 kg; Δt = 0,010 s
[thoughtful] Agora em duas dimensões. A mesma bola chega a vinte metros por segundo, para a esquerda, leva um chute e sai a trinta, a quarenta e cinco graus, para cima e para a direita. Contato de um centésimo de segundo.

### E2-2 — tela: os catetos tracejados da velocidade final acendem com 21,2 em cada um; v_f,x = v_f,y = 21,2 m/s; Jₓ = 0,40 (21,2 + 20) = 16,5 N·s; J_y = 0,40 · 21,2 = 8,5 N·s, cada um nascendo do seu cateto
Componente por componente. A quarenta e cinco graus, a velocidade final tem as duas partes iguais: uns vinte e um vírgula dois metros por segundo. Na horizontal, a bola ia a vinte para a esquerda e volta a vinte e um vírgula dois para a direita: o impulso horizontal dá dezesseis vírgula cinco newtons vezes segundo. Na vertical, ela não tinha nada e ganhou vinte e um vírgula dois: oito vírgula cinco.

### E2-3 — tela: no espaço reservado, o triângulo dos momentos (inicial, final e a variação fechando); F_méd = Δp/Δt; 1,9×10³ N a 27°; arcos de 27° e de 45°; a força média desliza até ficar em cima da variação do momento e volta; F⃗_méd ∥ Δp⃗ · F⃗_méd ∦ v⃗_f
[curious] Dividindo pelo tempo, a força média dá uns mil e novecentos newtons, a vinte e sete graus. Mas espera: a bola saiu a quarenta e cinco! Olha o triângulo dos momentos: a seta que fecha o triângulo, a variação do momento, está a vinte e sete graus, e a força média encaixa certinho em cima dela. A força não decide para onde a bola vai; ela decide quanto o momento muda.

### E2-4 — tela: DICA: F_MÉD APONTA PARA Δp⃗, NÃO PARA A VELOCIDADE FINAL
[thoughtful] Dica: desenhe o triângulo dos momentos. A força média aponta sempre para a variação do momento.

## E3 — FORÇA QUE CRESCE COM O TEMPO

### E3-1 — tela: o foguete numa coluna à esquerda, com o jato crescendo junto com a força; o gráfico F × t (uma parábola) no meio; m = 2.150 kg; F = A t²; o ponto anda pela curva até (1,25 s; 781,25 N); A = 781,25/1,25² = 500 N/s²
[thoughtful] Agora uma força que muda com o tempo, para usar a integral de verdade. Um foguete de dois mil cento e cinquenta quilos, no espaço, com um motor cuja força é uma constante vezes o tempo ao quadrado. Repara no jato crescendo junto com o ponto da curva. Em um vírgula vinte e cinco segundo, a força vale setecentos e oitenta e um vírgula vinte e cinco newtons, então a constante é quinhentos newtons por segundo ao quadrado. A massa, aqui, a gente trata como constante.

### E3-2 — tela: retângulos entre 2,0 e 3,5 s convergindo; a área preenchida; J = ∫₂,₀³,⁵ 500 t² dt = (500/3)(3,5³ − 2,0³); J ≈ 5,81×10³ N·s
Qual é o impulso entre dois segundos e três e meio? A área embaixo da parábola. Os retângulos mostram a ideia; a integral faz a conta: a integral do tempo ao quadrado é o tempo ao cubo sobre três. Dá uns cinco mil oitocentos e doze newtons vezes segundo.

### E3-3 — tela: Δv = J/m = 2,70 m/s; o retângulo da força média; F_méd = 3.875 N
[curious] Dividindo pela massa, a velocidade do foguete sobe dois vírgula setenta metros por segundo. Parece pouco, mas são mais de duas toneladas. E a força média do trecho, a área dividida por um segundo e meio, é de três mil oitocentos e setenta e cinco newtons.

## T6 — MOMENTO OU ENERGIA?

### T6-1 — tela: um bloco com a força resultante; o painel × Δt → IMPULSO → Δp⃗ entra primeiro; depois o painel × d → TRABALHO → ΔK
[thoughtful] Agora o insight mais importante da aula. A mesma força resultante pode ser acumulada de dois jeitos. No tempo, ela dá o impulso, que muda o momento. Na distância, ela dá o trabalho, que muda a energia cinética.

### T6-2 — tela: as duas bolas e as luvas no PALCO; na conta, em três linhas: K = ½ m v²; p = m v → v = p/m; K = p²/(2m) na caixa
E as duas conversam. A energia cinética é metade da massa vezes a velocidade ao quadrado; a velocidade é o momento dividido pela massa. Substituindo: a energia cinética é o momento ao quadrado sobre duas vezes a massa.

### T6-3 — tela: bola de 0,50 kg a 4,0 m/s e bola de 0,10 kg a 20 m/s indo para as luvas; p = 2,0 kg·m/s nas duas; MESMO TEMPO PARA PARAR; K = 4 J e K = 20 J; as luvas recuam d e 5d
[curious] Olha esse exemplo. Você, de luva, vai agarrar uma bola de meio quilo a quatro metros por segundo ou uma de cem gramas a vinte. As duas têm o mesmo momento, dois quilogramas vezes metro por segundo: mesmo impulso, então, com a mesma força, o mesmo tempo para parar. Mas a energia cinética da leve é cinco vezes maior, vinte joules contra quatro. Com a mesma força, a luva precisa recuar cinco vezes mais. A leve é a que arde.

### T6-4 — tela: dois barcos no gelo (m e 2m), o mesmo vento, a mesma linha de CHEGADA; MESMO VENTO, MESMA DISTÂNCIA; MESMA ENERGIA; m → p e 2m → √2 p; MOMENTO √2 VEZES MAIOR
[thoughtful] E o contrário: dois barcos no gelo, um com o dobro da massa do outro, com o mesmo vento até a mesma linha de chegada. Mesma força, mesma distância: mesma energia cinética. Mas o pesado demora mais, fica mais tempo sob o vento, e chega com raiz de dois vezes mais momento.

### T6-5 — tela: os barcos ficam; na conta: F⃗_res Δt = Δp⃗ e F⃗_res d = ΔK; FORÇA CONSTANTE; DICA: TEMPO → IMPULSO → MOMENTO · DISTÂNCIA → TRABALHO → ENERGIA
[thoughtful, emphatic] Guarda essa dica: se o problema fala de tempo, pense em impulso e momento. Se fala de distância, pense em trabalho e energia.

## E4 — DE VOLTA AO MURO

### E4-1 — tela: (3D) o muro com a cota h = 2,5 m; o boneco cai de pernas duras e depois de joelhos dobrados; m = 80 kg; v = √(2·9,8·2,5) = 7,0 m/s nasce da altura; Δp = 80 · 7,0 = 560 kg·m/s; NOS DOIS CASOS
[curious] Agora sim, de volta ao muro. O boneco tem oitenta quilos e cai de dois metros e meio. Da altura sai a velocidade de chegada: uns sete metros por segundo. Para parar, o momento dele vai de quinhentos e sessenta quilogramas vezes metro por segundo até zero. Nos dois casos.

### E4-2 — tela: as miniaturas PERNAS DURAS e JOELHOS na coluna esquerda, acendendo quando são citadas; o gráfico da força resultante no tempo, em escala real: o retângulo alto e fino das pernas duras e a curva baixa e larga dos joelhos; ÁREA = 560 N·s nas duas; Δt = 0,01 s × Δt ≈ 0,143 s
[thoughtful, emphatic] Então o impulso resultante é o mesmo nas duas aterrissagens: a mesma área. O que muda é o formato. De perna dura, o corpo para em um centésimo de segundo: um retângulo altíssimo e fininho. Dobrando os joelhos e descendo meio metro, uns catorze centésimos: uma curva baixa e larga. E o gráfico está em escala real, sem trapaça.

### E4-3 — tela: CAMINHO 1 · IMPULSO: F_res,méd = 560/Δt; DURAS 560/0,01 = 56.000 N; JOELHOS 560/(1/7) ≈ 3.920 N
[thoughtful] Primeiro caminho, pelo impulso: a força resultante média é a área dividida pelo tempo. De perna dura, cinquenta e seis mil newtons. Dobrando os joelhos, uns três mil novecentos e vinte.

### E4-4 — tela: CAMINHO 2 · TRABALHO: F_res d = ΔK = ½·80·7,0² = 1.960 J; d = 0,5 m: 1.960/0,5 = 3.920 N; d = 3,5 cm: 1.960/0,035 = 56.000 N
Segundo caminho, pela dica de agora há pouco: o problema também tem uma distância. A energia cinética na chegada é mil novecentos e sessenta joules. Tirando isso em meio metro de agachamento, a força média é de três mil novecentos e vinte newtons. De perna dura, o corpo para em três centímetros e meio, e dá de novo cinquenta e seis mil. Os dois teoremas concordam.

### E4-5 — tela: N = F_res + m g; a faixa do peso (784 N) no gráfico; PERNAS DURAS 56.784/784 ≈ 72 pesos; JOELHOS 4.704/784 ≈ 6 pesos
[curious] Só que a pergunta de verdade é com que força o chão empurra você, e o chão ainda segura o seu peso. Então a força do chão é a resultante mais o peso. De perna dura, umas setenta e duas vezes o seu peso. Dobrando os joelhos... umas seis.

### E4-6 — tela: MAIS TEMPO E MAIS DISTÂNCIA · MENOS FORÇA; mini-tabela com ícones: SAQUE DE TÊNIS ≈ 49 kgf · PÊNALTI ≈ 92 kgf · CARRO A 60 KM/H NO MURO ≈ 25 tf
[excited] Está aí a resposta! Dobrar os joelhos não muda o impulso: muda o tempo e a distância da parada, e isso derruba a força nos seus ossos de setenta e dois para seis pesos. É a física do airbag, do capacete e do colchão do salto em altura. Num saque de tênis são uns quarenta e nove quilos-força; num pênalti, uns noventa e dois; e num carro a sessenta por hora no muro, umas vinte e cinco toneladas-força. Por isso carro moderno amassa de propósito: amassar é ganhar tempo.

## E5 — A PULGA

### E5-1 — tela: a pulga pulando 50 cm; ZOOM nas patas esticando; h = 50 cm · m = 2 mg (MILIGRAMAS) · d = 1 mm; FORÇA NO CHÃO ÷ PESO = ?
[curious] Agora um desafio, com a atleta mais subestimada do reino animal: a pulga. Dois miligramas, e é miligrama mesmo, de massa. Ela pula cinquenta centímetros de altura, mas, no empurrão, estica as patas e sobe só um milímetro antes de sair do chão. Com que força ela empurra o chão, comparada com o peso dela?

### E5-2 — tela: v = √(2gh) = 3,13 m/s; CAMINHO 1 · DISTÂNCIA: a = v²/(2d) = g h/d = 500 g; F_res = m a = m v²/(2d)
[thoughtful] Para subir meio metro, ela precisa sair a uns três vírgula um metros por segundo. O problema dá uma distância, o milímetro do esticão, então vamos pela distância: a aceleração é a velocidade ao quadrado sobre duas vezes essa distância. Repara que isso vira a gravidade vezes a altura do pulo dividida pelo esticão. Quinhentas vezes a gravidade.

### E5-3 — tela: CAMINHO 2 · TEMPO: Δt = 2d/v = 0,64 ms; F_res = m v/Δt = m v²/(2d); as duas expressões acendem juntas; A MESMA FÍSICA PELOS DOIS TEOREMAS
Pelo tempo também dá, e serve de conferência: o empurrão dura uns sessenta e quatro centésimos de milissegundo, e o momento de saída dividido por esse tempo dá a mesma força. A mesma física pelos dois teoremas.

### E5-4 — tela: N = m(a + g) = m g (h/d + 1); o "+ 1" pisca; N = 501 pesos (caixa); NÃO 500; DICA: CONTATO ≠ RESULTANTE
[thoughtful, emphatic] Agora a pegadinha: a pergunta é a força que a pulga faz no chão, não a força resultante. Como no muro, o chão também segura o peso. Esse mais um aqui é o peso: quinhentos e um pesos, e não quinhentos. Força de contato não é força resultante.

### E5-5 — tela: a pulga sai; entram uma pessoa de 70 kg e um bloco de 35 t; N = 501 · (2×10⁻⁶ kg) · 9,8 ≈ 9,8×10⁻³ N ≈ 1,0×10⁻³ kgf · UM GRAMA-FORÇA
[curious] Em números, cerca de um grama-força. Parece nada, né? Mas, na proporção, é como uma pessoa de setenta quilos empurrando o chão com o peso de trinta e cinco toneladas. Da próxima vez que você vir uma pulga, mais respeito.

## SÍNTESE

### S1 — tela: RESUMO; o gráfico do muro com as duas curvas de mesma área; MESMO IMPULSO · MAIS TEMPO ⇒ MENOS FORÇA MÉDIA
[thoughtful] Então, a pergunta do começo está respondida. Dobrar os joelhos não muda o impulso resultante necessário para parar você: ele é sempre a variação do momento. O que muda é o tempo da parada, e junto com ele a distância. Mesma área, mais tempo, menos força média.

### S2 — tela: p⃗ = m v⃗ · J⃗ = ∫F⃗_res dt = Δp⃗ · TEMPO → MOMENTO · DISTÂNCIA → ENERGIA
[calm, satisfied] Resumindo: o momento é massa vezes velocidade, a grandeza que sai da segunda lei e que a natureza conserva. O impulso da força resultante é a área embaixo da força no tempo e é igual à variação do momento. E, na hora do problema: tempo conversa com momento, distância conversa com energia.

## ENCERRAMENTO

### F1 — tela: logo com anéis; INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
[happy] Se essa aula ajudou você a enxergar o momento de outro jeito, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### F2 — tela: (3D) o cavalo puxando a pedra pela corda; F⃗ na pedra e −F⃗ no cavalo; ?; SE A CORDA PUXA O CAVALO PARA TRÁS COM A MESMA FORÇA, COMO ELE ANDA?; PRÓXIMO VÍDEO: CONSERVAÇÃO DO MOMENTO EM SISTEMAS
[curious] E fica a pergunta para o próximo vídeo: se a corda puxa o cavalo para trás com a mesma força com que puxa a pedra para a frente, como é que o cavalo sai do lugar? Deixa o seu palpite nos comentários. No próximo vídeo: o momento de um sistema inteiro. Até a próxima!

---

## Notas para a tela (pedidas pela fala; nada muda na física nem nos números)
- ⚠ **E4-6:** a fala termina com "amassar é ganhar tempo"; o ícone do carro contra o muro pode pulsar nessa frase.
- Observado na análise do v6 (tela, não fala): no T5-8 o rótulo `J_y` fica perto de `Δp⃗ = J⃗`; no T6-2 os glifos que descem para
  `K = p²/(2m)` passam por cima da linha `v = p/m` durante 1 s.

## Números de conferência (g = 9,8 m/s²)

| Bloco | Valor falado | Exato |
|---|---|---|
| E1 | 20 N·s; 2.000 N; ~500 pesos; 12 e 20 kg·m/s | 20; 2.000; 510; 12 e 20 |
| E2 | 21,2; 16,5 e 8,5 N·s; ~1.900 N a 27° | 21,21; 16,49 e 8,49; 1.854 N a 27,2° |
| E3 | 500 N/s²; ~5.812 N·s; 2,70 m/s; 3.875 N | 500; 5.812,5; 2,703; 3.875 |
| T6 | p = 2,0; K = 4 e 20 J; √2 | ok |
| E4 | 7,0 m/s; 560; 0,01 e 1/7 s; 56.000 e 3.920 N; 1.960 J; 0,5 m e 3,5 cm; 72 e 6 pesos; 49 kgf, 92 kgf, 25 tf | 72,4 e 6,0 |
| E5 | 3,1 m/s; 500 g; 0,64 ms; 501 pesos; 1 gf; 35 t | 3,130; 0,639 ms; 35,07 t |

**Contagem:** ~3.540 palavras → ~22 min de fala a 2,7 palavras/s (a v4 tinha ~2.940 e ~18 min). Tags: 25 thoughtful, 19 curious, 9 thoughtful+emphatic, 2 happy, 1 excited, 1 calm+satisfied.
