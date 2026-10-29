# yt_0015 — MOMENTO LINEAR E IMPULSO · narração v5.3 (Produção, 29/10, aprovada para a voz)

Fonte: texto v5.3 colado pelo Kaio em 2026-10-29 (v5 do Claude Code → v5.1 Produção → v5.2 revisão do GPT → v5.3). Aqui ficam só as
falas, com o `tela:` de cada âncora; as notas de produção e o histórico de mudanças ficam no texto colado. A v4 está em
`narracao_sugestao_v4.md` (e as âncoras dela em `ancoras_v4.json`). `gerar_ancoras.py` lê este arquivo até "## Números de conferência".

---

## HOOK

### H1 — tela: (3D) muro de 2,5 m; o manequim pula e chega de pernas esticadas; CÂMERA LENTA no impacto
[curious] Olha essa queda. O nosso boneco de testes pula de um muro de dois metros e meio e chega no chão de pernas esticadas, duras feito um cabo de vassoura. Em câmera lenta dá para ver: o corpo para quase de uma vez, e o tranco vai direto para os ossos.

### H2 — tela: (3D) a mesma queda, agora os joelhos dobram e o quadril desce
Agora a mesma queda, do mesmo muro, com o mesmo boneco. Só que, dessa vez, ele chega dobrando os joelhos e deixando o quadril descer.

### H3 — tela: (3D) as duas aterrissagens lado a lado; POR QUE DOBRAR OS JOELHOS SALVA SUAS PERNAS?
[thoughtful] Pensa comigo: a altura é a mesma, a velocidade de chegada é a mesma, e nos dois casos o corpo termina parado. Então por que dobrar os joelhos salva as suas pernas? Spoiler: não é mágica, nem academia de perna. São duas ideias da física que a gente vai construir hoje: momento linear e impulso.

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: MOMENTO LINEAR E IMPULSO; painéis NESTE VÍDEO: UM CORPO e NO PRÓXIMO: VÁRIOS CORPOS
[thoughtful] Hoje o assunto é momento linear e impulso, com um foco bem claro: um corpo só e uma força agindo nele ao longo do tempo. Olha a bolinha: a força empurra, e a velocidade cresce enquanto a força age. À direita, o próximo capítulo da série: vários corpos batendo, e o momento total se conservando.

### A3 — tela: DOS VÍDEOS DE COLISÕES; P⃗ᵢ = P⃗_f em destaque
[curious] Nos vídeos de colisões, essa igualdade foi a nossa ferramenta: momento total antes igual ao momento total depois. Hoje a gente vai até a raiz dela.

## T1 — DE ONDE VEM O MOMENTO

### T1-1 — tela: eixos x, y, z; partícula numa curva no espaço; SEGUNDA LEI DE NEWTON; ΣF⃗ = m a⃗
[thoughtful] Vamos começar do que você já conhece: a segunda lei de Newton. Uma bolinha de aço fazendo uma trajetória qualquer pelo espaço. Em cada instante ela tem uma velocidade, a seta violeta, tangente à trajetória, e sente uma força resultante, a seta azul, que vai entortando a trajetória para o lado de dentro da curva. A segunda lei diz: força resultante é massa vezes aceleração.

### T1-2 — tela: LUPA; Δv⃗ → dv⃗; ΣF⃗ = m dv⃗/dt → ΣF⃗ = d(m v⃗)/dt; MASSA CONSTANTE
[curious] Mas o que é a aceleração? Vamos usar uma lupa. Pego a velocidade agora e a velocidade um instantinho depois, saindo do mesmo ponto. A diferença entre elas é a variação da velocidade, e repara: conforme o intervalo encolhe, ela aponta junto com a força. A aceleração é essa variação dividida pelo pedacinho de tempo: a derivada da velocidade. Então a força resultante é a massa vezes a derivada da velocidade. E, se a massa não muda, ela entra na derivada sem alterar nada: a força resultante é a derivada da massa vezes a velocidade.

### T1-3 — tela: a seta do momento nasce da velocidade; p⃗ = m v⃗; MOMENTO LINEAR · OU QUANTIDADE DE MOVIMENTO; kg·m/s
[thoughtful, emphatic] Esse produto, massa vezes velocidade, aparece tanto que ganhou nome: momento linear, ou quantidade de movimento. Na tela, ele vai ser sempre esta seta magenta. Como a massa é positiva, o momento aponta para o mesmo lado da velocidade: é a mesma seta, esticada pela massa. E a unidade sai da definição: quilograma vezes metro por segundo.

### T1-4 — tela: dois carros iguais a 20 m/s, norte e leste; |p⃗₁| = |p⃗₂| e p⃗₁ ≠ p⃗₂
[curious] E atenção: o momento é um vetor de verdade. Dois carros iguais, a vinte metros por segundo, um indo para o norte e o outro para o leste. O tamanho do momento é o mesmo nos dois. Mas os momentos são diferentes, porque apontam para lados diferentes. O velocímetro dos dois marca a mesma coisa; o GPS, com certeza, não.

### T1-5 — tela: CÓPIA DE v⃗ NA ORIGEM; componentes nos eixos; pₓ = m vₓ · p_y = m v_y · p_z = m v_z
[thoughtful] Na prática, a gente trabalha com componentes. Copio a seta da velocidade para a origem e projeto nos três eixos: aparece a parte da velocidade em x, em y e em z. E cada parte do momento é a massa vezes a parte da velocidade na mesma direção. Três equações com números no lugar de uma com setas.

### T1-6 — tela: ΣF⃗ = dp⃗/dt; barras pₓ, p_y, p_z com as setinhas da força; ΣFₓ = dpₓ/dt etc.; CADA DIREÇÃO CUIDA DA SUA
[thoughtful] Agora volta na segunda lei e troca massa vezes velocidade pelo nome novo: a força resultante é a taxa de variação do momento. Olha o painel: cada barra magenta é uma componente do momento, e a setinha azul ao lado é a componente da força. Seta para cima, a barra cresce; seta para baixo, a barra diminui. A força em x só mexe no momento em x, e o mesmo vale em y e em z. Cada direção cuida da sua vida.

### T1-7 — tela: A FORMA ORIGINAL DE NEWTON · REFERENCIAL INERCIAL; foguete soltando gás; MASSA VARIÁVEL
[curious] Curiosidade: foi assim, falando em quantidade de movimento, que o próprio Newton escreveu a segunda lei. Ela vale em referenciais inerciais, e é por ela que a gente vai chegar nos casos em que a massa muda, como um foguete jogando gás para trás. Só que aí tem uma pegadinha: é preciso escolher direitinho o que entra no sistema, e esse cuidado fica para um vídeo desta série. Hoje a massa fica quietinha.

## T2 — O FATO EXPERIMENTAL

### T2-1 — tela: COLCHÃO DE AR; SEM FORÇA DE FORA?; EXPERIÊNCIA 1 (BATIDA ELÁSTICA): trocam de velocidade
[thoughtful] Então a força resultante muda o momento. E se nenhuma força de fora agir? Vamos ao laboratório. Dois discos iguais sobre um colchão de ar, tipo uma mesa de air hockey: o ar por baixo elimina o atrito. Na primeira experiência, eles vêm um contra o outro com a mesma velocidade, numa batida bem elástica, daquelas que não perdem energia, e voltam, cada um com a velocidade do outro.

### T2-2 — tela: EXPERIÊNCIA 2: um parado; quem vinha para, o parado sai com v
Na segunda, um disco está parado e o outro chega. Depois da batida, quem vinha para, e quem estava parado sai com a velocidade do primeiro. Igualzinho à sinuca.

### T2-3 — tela: EXPERIÊNCIA 3: CHICLETE (MASSA DESPREZÍVEL); grudam, seguem com v/2
Na terceira, a gente gruda um pedacinho de chiclete num dos discos, tão leve que a massa dele nem entra na conta. E não pergunta de onde veio esse chiclete. Eles batem, ficam juntos, e o conjunto segue com metade da velocidade.

### T2-4 — tela: tabela ANTES | DEPOIS montada a partir dos discos
[curious] Três finais completamente diferentes. Mas olha a tabela: em cada linha, a massa vezes a velocidade de um disco mais a do outro. Antes e depois, essa soma é a mesma nas três. E com massas diferentes ela continua a mesma.

### T2-5 — tela: P⃗ = p⃗₁ + p⃗₂ = constante; PRINCÍPIO DE CONSERVAÇÃO DO MOMENTO (SISTEMA ISOLADO)
[thoughtful, emphatic] Isso é uma lei da natureza, tirada direto da experiência: o princípio de conservação do momento. Os momentos de cada disco mudam na batida, mas a soma, o momento total, fica sempre igual: mesmo tamanho e mesmo sentido. Num sistema isolado, sem força de fora, ele não muda.

## T3 — POR QUE MASSA VEZES VELOCIDADE?

### T3-1 — tela: trilho de ar; mola com trava; v ?, m v ?, m v² ?; a mola empurra; estroboscópio
[curious] Agora, uma pergunta que quase ninguém faz. Por que justamente massa vezes velocidade? Por que não a velocidade sozinha, ou a massa vezes a velocidade ao quadrado? Tem um argumento de simetria muito bonito para isso. Dois carrinhos iguais, parados, com uma mola comprimida entre eles, presa por uma trava. A trava solta, a mola empurra. E, como os carrinhos são iguais, não tem por que um sair mais rápido: saem com a mesma velocidade, um para cada lado. Os fantasmas são fotos a cada meio segundo, e o espaçamento é igual dos dois lados.

### T3-2 — tela: velcro; batem, grudam e param; IGUAIS E OPOSTOS: O CONJUNTO PARA
[thoughtful] Agora outra experiência: velcro na frente, os dois vêm um contra o outro com a mesma velocidade, batem, grudam... e param. Faz sentido: com tudo simétrico, o conjunto não tem para que lado escolher andar.

### T3-3 — tela: VISTA DO CHÃO × VISTA DE QUEM ANDA JUNTO COM A; câmera; régua correndo; B com 2v; o conjunto sai com v
[curious] Agora vem o truque. Assista à mesma colisão com uma câmera que anda junto com o carrinho da esquerda. Em cima, quem está parado no chão; embaixo, a câmera. Para ela, o carrinho A está parado e quem anda é o chão, para a esquerda: olha a régua correndo. O carrinho B vem da direita, andando para a esquerda, com o dobro da velocidade. E o conjunto, que no chão ficava parado, para a câmera vai embora para a esquerda, com a velocidade original. Mesma colisão, outro ponto de vista.

### T3-4 — tela: m·2v + m·0 = 2m·v; casos m × 2m e 2m × 3m; ANTES = DEPOIS, SEMPRE
[thoughtful] Então a gente ganhou, sem conta nenhuma, uma colisão nova: um carrinho com o dobro da velocidade bate num igual parado, e os dois seguem com metade dela. Olha a conta nascendo dos rótulos: massa vezes o dobro da velocidade, mais zero, dá o dobro da massa vezes a velocidade. Fecha certinho. Agora testa a massa vezes a velocidade ao quadrado: antes dá quatro vezes a massa vezes a velocidade ao quadrado; depois, só duas vezes. Não fecha. E a velocidade sozinha cai assim que as massas são diferentes: olha os outros casos, com um carrinho de massa dupla e um de massa tripla. Em todos eles, só a massa vezes a velocidade fecha. Antes igual a depois, sempre. Isso não é uma demonstração de que nada mais no universo se conserva, tá? Mas mostra por que, entre os candidatos, é esse que a natureza escolhe.

### T3-5 — tela: DA SEGUNDA LEI e DA SIMETRIA convergem para p⃗ = m v⃗; MOMENTO LINEAR
[thoughtful, emphatic] Repara: a grandeza que a segunda lei de Newton entregou lá no começo é a mesma que a simetria aponta agora. Dois caminhos diferentes, o mesmo lugar. Não é coincidência. É o momento linear.

## T4 — DA CONSERVAÇÃO À TERCEIRA LEI

### T4-1 — tela: Δp⃗₁ = −Δp⃗₂; O QUE UM GANHA, O OUTRO PERDE
[thoughtful] Agora uma virada que vale ouro. Pensa nos dois discos como um sistema isolado: nenhuma força de fora, só um empurrando o outro. Se o momento total não muda, tudo o que um disco ganha o outro perde. A variação do momento do primeiro é menos a variação do momento do segundo.

### T4-2 — tela: cronômetro; ÷ Δt; Δt → 0; dp⃗₁/dt = −dp⃗₂/dt
Divide os dois lados pelo tempo da colisão, e vai encolhendo esse tempo, como no cronômetro. O que sobra é a taxa de variação: a derivada do momento de um é menos a derivada do momento do outro, a cada instante.

### T4-3 — tela: F⃗₁₍₂₎ = −F⃗₂₍₁₎; TERCEIRA LEI DE NEWTON
[thoughtful, emphatic] Só que, lembra do começo? A taxa de variação do momento é a força. Então a força que o segundo disco faz no primeiro é igual e oposta à que o primeiro faz no segundo. Olha só quem apareceu: a terceira lei de Newton, saindo da conservação do momento.

### T4-4 — tela: bloco na mesa; AS DUAS NO BLOCO; a Terra com −P⃗; AÇÃO E REAÇÃO AGEM EM CORPOS DIFERENTES
[curious] E aqui mora uma pegadinha clássica. Ação e reação agem sempre em corpos diferentes. O peso e a normal estão os dois no bloco, então não são ação e reação. A reação do peso é o bloco puxando a Terra para cima. E a reação da normal é o bloco empurrando a mesa para baixo. E a Terra está fora de escala, tá? Prometo que ela é um pouquinho maior.

### T4-5 — tela: cargas em movimento; F⃗₁₍₂₎ ≠ −F⃗₂₍₁₎; MOMENTO DAS PARTÍCULAS + MOMENTO DO CAMPO = CONSTANTE
[thoughtful] E por que partir da conservação? Porque ela é mais funda. Entre cargas elétricas em movimento, as forças podem não ser iguais e opostas: a terceira lei falha. Mas a conservação continua valendo se a gente contar também o momento do campo. Ela sobrevive onde a terceira lei não chega.

## T5 — IMPULSO

### T5-1 — tela: bloco sem atrito; força constante de t₁ a t₂; gráficos F × t e p × t
[thoughtful] Até aqui, a gente olhou para o momento num instante. Agora a pergunta é: o que uma força faz com ele ao longo de um tempo? Isso é o impulso, e vamos construir passo a passo. O caso mais simples: um bloco sem atrito e uma força resultante constante, que liga num instante e desliga noutro. Olha os gráficos andando juntos. Em cima, a força: um degrau. Embaixo, o momento: como a taxa de variação dele é a força, e a força é constante, ele sobe em linha reta. A inclinação da reta é a própria força.

### T5-2 — tela: triângulo de inclinação; ΣF⃗ (t₂ − t₁) = p⃗₂ − p⃗₁
Com taxa constante, a derivada é a variação total dividida pelo intervalo. No triângulo: na vertical, o momento final menos o inicial; na horizontal, o instante final menos o inicial. Agora passa o intervalo para o outro lado, multiplicando: força resultante vezes o tempo em que ela age é igual ao momento final menos o inicial.

### T5-3 — tela: J⃗ = ΣF⃗ Δt = p⃗₂ − p⃗₁; IMPULSO; unidades
[thoughtful, emphatic] Esse produto, força resultante vezes intervalo, se chama impulso. É um vetor, na direção da força, e é a área do retângulo embaixo do gráfico. E as unidades: newton vezes segundo é quilograma vezes metro por segundo ao quadrado, vezes segundo; um segundo cancela, e sobra quilograma vezes metro por segundo. A mesma unidade do momento, como tinha que ser.

### T5-4 — tela: bola na parede; FORÇA DA PAREDE; CENTÉSIMOS DE SEGUNDO
[curious] Só que, numa colisão de verdade, a força não é constante. Antes do contato, a força da parede é praticamente zero. Quando a bola encosta, ela sobe muito rápido, chega num pico enquanto a bola amassa, e volta a zero quando ela se solta. Tudo em centésimos de segundo.

### T5-5 — tela: RETÂNGULOS 4 → 8 → 32; QUANTO MAIS FINO, MAIS COLA NA CURVA
[thoughtful] Então a gente faz o que todo bom físico faz: fatia o problema. Em cada pedacinho de tempo, a força é quase constante, e vale o caso simples: o momento muda de força vezes o pedacinho de tempo. Cada retângulo vira um pedacinho da variação do momento, somado na seta da bola. Quatro, oito, trinta e dois... quanto mais fino, mais a soma cola na curva.

### T5-6 — tela: a soma vira a integral; ∫ dp⃗ = p⃗₂ − p⃗₁; O IMPULSO DA FORÇA RESULTANTE É A VARIAÇÃO DO MOMENTO
[thoughtful, emphatic] No limite, a soma vira a integral da força resultante no tempo, do instante inicial ao final. Agora troca a força pela derivada do momento: o pedacinho de tempo cancela, e os limites, que eram instantes, viram o momento inicial e o final. Somar pedacinhos de momento dá o momento final menos o inicial. Então vale para qualquer força: o impulso da força resultante é igual à variação do momento.

### T5-7 — tela: F_méd; MESMA BASE, MESMA ÁREA; outra curva com a mesma área
Geometricamente, o impulso é a área embaixo da curva da força. E a força média é a força constante que daria o mesmo impulso no mesmo intervalo: a altura de um retângulo com a mesma base e a mesma área. Olha embaixo: outra forma, mesma área, vinte newtons vezes segundo. Mesmo impulso. Só a área importa.

### T5-8 — tela: plano xy; Δp⃗ = J⃗; Jₓ e J_y; E O MESMO EM z
[thoughtful] E, como o impulso é um vetor, a gente trabalha componente por componente. A variação do momento vai da ponta do momento inicial até a ponta do final; projetando, aparece o impulso em x e em y. Em x, o impulso é a integral da força em x, é a força média em x vezes o intervalo, e é a massa vezes a velocidade final em x menos a inicial. Em y, a mesmíssima coisa, e em z também.

### T5-9 — tela: DICA: IMPULSO É VETOR
[thoughtful] Uma dica que vale ponto na prova: escolha os eixos, escreva componente por componente, e respeite os sinais.

## E1 — BOLA NA PAREDE

### E1-1 — tela: parede; +x; ANTES 30 m/s ←; DEPOIS 20 m/s →; m = 0,40 kg; Δt = 0,010 s
[thoughtful] Teoria montada, hora de colocar a mão na massa. E a gente começa pelo sinal, que é onde todo mundo escorrega. Uma bola de quatrocentos gramas chega numa parede a trinta metros por segundo, para a esquerda, e volta a vinte, para a direita. O contato dura um centésimo de segundo. Primeiro passo: escolher o positivo. Aqui, para a direita.

### E1-2 — tela: vᵢ = −30 · v_f = +20; três setas; J = 20 N·s
Então a velocidade inicial é menos trinta e a final é mais vinte. Olha as três setas: o momento inicial para a esquerda, o final para a direita, e a variação ligando as pontas, para a direita. O impulso é a massa vezes a velocidade final menos a inicial: zero vírgula quatro vezes cinquenta. Vinte newtons vezes segundo, para a direita.

### E1-3 — tela: −4 N·s riscado; A PAREDE PUXOU A BOLA?
[curious] Sem o sinal, alguém faria vinte menos trinta e acharia menos quatro, como se a parede puxasse a bola. Parede com ímã de bola não existe. O sinal é física.

### E1-4 — tela: F_méd = 2.000 N; mg = 3,9 N
[thoughtful] E a força? A força média é o impulso dividido pelo tempo: vinte sobre um centésimo, dois mil newtons. Perto disso, o peso, três vírgula nove newtons, é uma setinha. Umas quinhentas vezes menor. Por isso, num choque rápido, o peso sai da conta sem culpa.

### E1-5 — tela: PARAR × REBATER; |Δp⃗|: 12 → 20 kg·m/s; DICA
[thoughtful] E repara: para só parar a bola, o momento iria de doze até zero. Para rebater, vai até zero e ainda volta: a variação sobe para vinte. Rebater pede mais impulso do que só parar. Quem já devolveu uma cortada no vôlei sabe do que eu estou falando.

## E2 — CHUTE EM 2D

### E2-1 — tela: ANTES 20 m/s ←; DEPOIS 30 m/s a 45°
[thoughtful] Agora em duas dimensões. A mesma bola chega a vinte metros por segundo, para a esquerda, leva um chute e sai a trinta, a quarenta e cinco graus, para cima e para a direita. Contato de um centésimo de segundo.

### E2-2 — tela: 21,2 nos catetos; Jₓ = 16,5 N·s; J_y = 8,5 N·s
Componente por componente. A quarenta e cinco graus, a velocidade final tem as duas partes iguais: uns vinte e um vírgula dois metros por segundo. Na horizontal, a bola ia a vinte para a esquerda e volta a vinte e um vírgula dois para a direita: o impulso horizontal dá dezesseis vírgula cinco newtons vezes segundo. Na vertical, ela não tinha nada e ganhou vinte e um vírgula dois: oito vírgula cinco.

### E2-3 — tela: triângulo dos momentos; 1,9×10³ N a 27°; F⃗_méd ∥ Δp⃗ · F⃗_méd ∦ v⃗_f
[curious] Dividindo pelo tempo, a força média dá uns mil e novecentos newtons, a vinte e sete graus. Mas espera: a bola saiu a quarenta e cinco! Olha o triângulo dos momentos: a seta que fecha o triângulo, a variação do momento, está a vinte e sete graus, e a força média encaixa certinho em cima dela. A força não aponta para onde a bola vai; ela aponta para onde o momento muda.

### E2-4 — tela: DICA: F_MÉD APONTA PARA Δp⃗
[thoughtful] Dica: desenhe o triângulo dos momentos. A força média aponta sempre para a variação do momento.

## E3 — FORÇA QUE CRESCE COM O TEMPO

### E3-1 — tela: foguete; F × t; m = 2.150 kg (MASSA ≈ CONSTANTE (APROXIMAÇÃO)); F = A t²; (1,25 s; 781,25 N); A = 500 N/s²
[thoughtful] Agora uma força que muda com o tempo, para usar a integral de verdade. Um foguete de dois mil cento e cinquenta quilos, no espaço, com um motor cuja força é uma constante vezes o tempo ao quadrado. Repara no jato crescendo junto com o ponto da curva. Em um vírgula vinte e cinco segundo, a força vale setecentos e oitenta e um vírgula vinte e cinco newtons, então a constante é quinhentos newtons por segundo ao quadrado. E um combinado: um foguete de verdade perde massa ao queimar combustível, mas, nesse trecho curto, a gente trata a massa como constante. É uma aproximação.

### E3-2 — tela: retângulos entre 2,0 e 3,5 s; J ≈ 5,81×10³ N·s
Qual é o impulso entre dois segundos e três e meio? A área embaixo da parábola. Os retângulos mostram a ideia; a integral faz a conta: a integral do tempo ao quadrado é o tempo ao cubo sobre três. Dá uns cinco mil oitocentos e doze newtons vezes segundo.

### E3-3 — tela: Δv = 2,70 m/s; F_méd = 3.875 N
[curious] Dividindo pela massa, a velocidade do foguete sobe dois vírgula setenta metros por segundo. Parece pouco, mas são mais de duas toneladas. E a força média do trecho, a área dividida por um segundo e meio, é de três mil oitocentos e setenta e cinco newtons.

## T6 — MOMENTO OU ENERGIA?

### T6-1 — tela: bloco com a força; × Δt → IMPULSO → Δp⃗ · · Δr⃗ → TRABALHO → ΔK
[thoughtful] Agora o insight mais importante da aula. A mesma força resultante pode ser acumulada de dois jeitos. No tempo, ela dá o impulso, que muda o momento. Na distância, contando a parte da força que está na direção do deslocamento, ela dá o trabalho, que muda a energia cinética.

### T6-2 — tela: K = ½ m v²; v = p/m; K = p²/(2m)
E as duas conversam. A energia cinética é metade da massa vezes a velocidade ao quadrado; a velocidade é o momento dividido pela massa. Substituindo: a energia cinética é o momento ao quadrado sobre duas vezes a massa.

### T6-3 — tela: 0,50 kg a 4,0 m/s e 0,10 kg a 20 m/s; p = 2,0; MESMO TEMPO PARA PARAR; K = 4 J e 20 J; d e 5d
[curious] Olha esse exemplo. Você, de luva, vai agarrar uma bola de meio quilo a quatro metros por segundo ou uma de cem gramas a vinte. As duas têm o mesmo momento, dois quilogramas vezes metro por segundo: mesmo impulso. Então, se a luva frear as duas com a mesma força constante, o tempo para parar é o mesmo. Mas a energia cinética da leve é cinco vezes maior, vinte joules contra quatro. Com essa mesma força constante, a luva precisa recuar cinco vezes mais para segurar a leve. Parece estranho, mas é a bolinha leve que dá mais trabalho. E dá trabalho no sentido da física mesmo.

### T6-4 — tela: barcos m e 2m no gelo; SEM ATRITO · PARTEM DO REPOUSO · MESMA FORÇA CONSTANTE; MESMA ENERGIA; MOMENTO √2 VEZES MAIOR
[thoughtful] E o contrário: dois barcos no gelo, sem atrito, partindo do repouso, um com o dobro da massa do outro, cada um recebendo a mesma força horizontal constante até a mesma linha de chegada. O vento na tela é só a nossa forma de desenhar essa força. Mesma força, mesma distância: mesma energia cinética. Mas o pesado demora mais, fica mais tempo sob o vento, e chega com raiz de dois vezes mais momento.

### T6-5 — tela: F⃗_res Δt = Δp⃗ · F⃗_res · Δr⃗ = ΔK (W_res = ∫F⃗_res · dr⃗ = ΔK); DICA
[thoughtful, emphatic] Guarda essa dica: se o problema fala de tempo, pense em impulso e momento. Se fala de distância, pense em trabalho e energia.

## E4 — DE VOLTA AO MURO

### E4-1 — tela: (3D) muro; h = 2,5 m; m = 80 kg; v = 7,0 m/s; Δp = 560 kg·m/s
[curious] E agora a gente tem tudo o que precisa para voltar ao muro do começo. O boneco tem oitenta quilos e cai de dois metros e meio. Da altura sai a velocidade de chegada: uns sete metros por segundo. Para parar, o momento dele vai de quinhentos e sessenta quilogramas vezes metro por segundo até zero. Nos dois casos.

### E4-2 — tela: miniaturas; dois retângulos de mesma área (560 N·s) em escala real; MODELO: DESACELERAÇÃO CONSTANTE; Δt = 0,01 s × 0,143 s
[thoughtful, emphatic] Então o impulso resultante é o mesmo nas duas aterrissagens: a mesma área. O que muda é o formato. Para fazer as contas, vamos usar um modelo simples: em cada aterrissagem, a desaceleração é constante, então a força resultante é um retângulo no gráfico. De perna dura, o corpo para em um centésimo de segundo: um retângulo altíssimo e fininho. Dobrando os joelhos e descendo meio metro, uns catorze centésimos: um retângulo baixo e largo. Na vida real a força sobe e desce, mas a área é a mesma. E o gráfico está em escala real, sem trapaça.

### E4-3 — tela: CAMINHO 1 · IMPULSO: 56.000 N e 3.920 N
[thoughtful] Primeiro caminho, pelo impulso: a força resultante média é a área dividida pelo tempo. De perna dura, cinquenta e seis mil newtons, para cima. Dobrando os joelhos, uns três mil novecentos e vinte.

### E4-4 — tela: CAMINHO 2 · TRABALHO: W_res = ΔK = −1.960 J; |F_res|·d = 1.960 J; 3.920 N e 56.000 N
Segundo caminho, pela dica de agora há pouco: o problema também tem uma distância. A energia cinética na chegada é mil novecentos e sessenta joules, e ela tem que sumir. Repara no sinal: a força resultante aponta para cima, e o corpo ainda desce. Por isso o trabalho dela é negativo, menos mil novecentos e sessenta joules. Em módulo, a força vezes a distância tem que tirar esses mil novecentos e sessenta. Em meio metro de agachamento, dá três mil novecentos e vinte newtons. De perna dura, o corpo para em três centímetros e meio, e dá de novo cinquenta e seis mil. Os dois teoremas concordam, e concordam porque, no nosso modelo, a força é constante.

### E4-5 — tela: N = F_res + m g; faixa do peso; ≈ 72 pesos e ≈ 6 pesos
[curious] Só que a pergunta de verdade é com que força o chão empurra você, e o chão ainda segura o seu peso. Então a força do chão é a resultante mais o peso. De perna dura, umas setenta e duas vezes o seu peso. Dobrando os joelhos... umas seis.

### E4-6 — tela: MAIS TEMPO E MAIS DISTÂNCIA · MENOS FORÇA; ícones AIRBAG · CAPACETE · CARRO QUE AMASSA
[excited] Está aí a resposta! Dobrar os joelhos não muda o impulso: muda o tempo e a distância da parada, e isso derruba a força nos seus ossos de setenta e dois para seis pesos. É a física do airbag, do capacete e do colchão do salto em altura: todos esticam o tempo e a distância da parada. E é por isso que carro moderno amassa de propósito na frente. Amassar é ganhar tempo.

## E5 — A PULGA

### E5-1 — tela: pulga; ZOOM; h = 50 cm · m = 2 mg (MILIGRAMAS) · d = 1 mm; FORÇA NO CHÃO ÷ PESO = ?
[curious] Agora um desafio, com a atleta mais subestimada do reino animal: a pulga. Dois miligramas, e é miligrama mesmo, de massa. No nosso problema, ela pula meio metro de altura. Na vida real é um pouco menos, mas a gente dá esse desconto para ela. E, no empurrão, estica as patas e sobe só um milímetro antes de sair do chão. Com que força ela empurra o chão, comparada com o peso dela?

### E5-2 — tela: v = 3,13 m/s; CAMINHO 1 · DISTÂNCIA (ACELERAÇÃO CONSTANTE NO ESTICÃO); a = 500 g
[thoughtful] Para subir meio metro, ela precisa sair a uns três vírgula um metros por segundo. O problema dá uma distância, o milímetro do esticão, então vamos pela distância. Supondo que, nesse esticão, ela acelere de forma constante, a aceleração é a velocidade ao quadrado sobre duas vezes essa distância. Repara que isso vira a gravidade vezes a altura do pulo dividida pelo esticão. Quinhentas vezes a gravidade.

### E5-3 — tela: CAMINHO 2 · TEMPO: Δt = 0,64 ms; F_res = m v/Δt = m v²/(2d)
Pelo tempo também dá, e serve de conferência. Com aceleração constante, a velocidade média no esticão é metade da velocidade de saída, então o empurrão dura uns sessenta e quatro centésimos de milissegundo, e o momento de saída dividido por esse tempo dá a mesma força. A mesma física pelos dois teoremas.

### E5-4 — tela: N = m g (h/d + 1) = 501 pesos; NÃO 500; DICA
[thoughtful, emphatic] Agora a pegadinha: a pergunta é a força que a pulga faz no chão, não a força resultante. Como no muro, o chão também segura o peso. Esse mais um aqui é o peso: quinhentos e um pesos, e não quinhentos. Força de contato não é força resultante.

### E5-5 — tela: pessoa de 70 kg e bloco de 35 t; ≈ 1 grama-força
[curious] Em números, cerca de um grama-força. Parece nada, né? Mas, na proporção, é como uma pessoa de setenta quilos empurrando o chão com o peso de trinta e cinco toneladas. Da próxima vez que você vir uma pulga, mais respeito.

## SÍNTESE

### S1 — tela: RESUMO; o gráfico do muro (dois retângulos de mesma área); MESMO IMPULSO · MAIS TEMPO ⇒ MENOS FORÇA MÉDIA
[thoughtful] Então, a pergunta do começo está respondida. Dobrar os joelhos não muda o impulso resultante necessário para parar você: ele é sempre a variação do momento. O que muda é o tempo da parada, e junto com ele a distância. Mesma área, mais tempo, menos força média.

### S2 — tela: p⃗ = m v⃗ · J⃗ = ∫F⃗_res dt = Δp⃗ · TEMPO → MOMENTO · DISTÂNCIA → ENERGIA
[calm, satisfied] Resumindo: o momento é massa vezes velocidade, a grandeza que sai da segunda lei e que a natureza conserva. O impulso da força resultante é a área embaixo da força no tempo e é igual à variação do momento. E, na hora do problema: tempo conversa com momento, distância conversa com energia.

## ENCERRAMENTO

### F1 — tela: logo com anéis; INSCREVA-SE
[happy] Se essa aula ajudou você a enxergar o momento de outro jeito, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### F2 — tela: (3D) cavalo e pedra; COMO ELE ANDA?; PRÓXIMO VÍDEO: CONSERVAÇÃO DO MOMENTO EM SISTEMAS
[curious] E fica a pergunta para o próximo vídeo: se a corda puxa o cavalo para trás com a mesma força com que puxa a pedra para a frente, como é que o cavalo sai do lugar? Deixa o seu palpite nos comentários. No próximo vídeo: o momento de um sistema inteiro. Até a próxima!

---

## Números de conferência (g = 9,8 m/s²)

| Bloco | Valor falado | Exato |
|---|---|---|
| E1 | 20 N·s; 2.000 N; ~500 pesos; 12 e 20 kg·m/s | 20; 2.000; 510; 12 e 20 |
| E2 | 21,2; 16,5 e 8,5 N·s; ~1.900 N a 27° | 21,21; 16,49 e 8,49; 1.854 N a 27,2° |
| E3 | 500 N/s²; ~5.812 N·s; 2,70 m/s; 3.875 N | 500; 5.812,5; 2,703; 3.875 |
| T6 | p = 2,0; K = 4 e 20 J; √2 | ok |
| E4 | 7,0 m/s; 560; 0,01 e 1/7 s; 56.000 e 3.920 N; −1.960 J; 0,5 m e 3,5 cm; 72 e 6 pesos | 72,4 e 6,0 |
| E5 | 3,1 m/s; 500 g; 0,64 ms; 501 pesos; 1 gf; 35 t | 3,130; 0,639 ms; 35,07 t |
