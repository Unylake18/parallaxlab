# COLISÕES EM 2D — sugestão de narração (v1.1, sobre o preview v3)

Fonte da cena: `cena.py` v3 (preview `renders/yt_0014_preview_v3_960x540_15fps.mp4`, 490 s). Padrão: `docs/padrao_video_longo.md` §5 e
`docs/roteiro_voz_elevenlabs_v4.md`. Professor de cursinho **amigo e próximo**, conversado, com piada onde cabe, "a gente"/"você",
**nunca a letra solta**.

**Como ler:** cada `###` é uma **âncora** (evento visual). A linha `tela:` diz o que aparece; a fala que vem embaixo começa junto desse
evento. As linhas que começam com `>` são **notas de animação** (não são faladas): dizem o que se move durante a fala e o que precisa
ser esticado ou acrescentado na sincronização (⚠ = coisa nova a criar). A fala manda: nada aqui deve ser cortado para caber na animação.

**Regra de sincronia:** a cena **nunca fica parada enquanto a voz fala**; cada âncora tem sempre algo se movendo (termo que navega,
destaque que acompanha a palavra, varredura de ângulo, seta que cresce). O evento visual de cada âncora começa **no máximo 0,2 s depois
da primeira palavra da âncora** (e nunca antes dela). Os destaques (`Indicate`, caixas) entram junto da palavra que citam.

**Notação falada** (apresentada uma vez, depois só o nome): momento inicial do corpo um / do corpo dois, momento final do corpo um / do
corpo dois (na tela p⃗₁ᵢ, p⃗₂ᵢ, p⃗₁f, p⃗₂f); velocidades do mesmo jeito (v⃗₁ᵢ, v⃗₁f, v⃗₂f); **o ângulo de saída do corpo um** (θ₁, medido
para cima) e **o ângulo de saída do corpo dois** (θ₂, medido para baixo); **a razão das massas** (λ = m₂/m₁, falada "lambda" só na
apresentação); **o ângulo máximo** (θ_max); o centro e o raio do círculo (C⃗ e R). "Módulo" = o tamanho do vetor (dito uma vez). Momento
= "momento linear", também chamado "quantidade de movimento", na primeira vez; depois só "momento".

**Hipóteses ditas em voz alta, uma vez:** choque muito curto (impulso externo desprezível), massas constantes, movimento num plano,
alvo inicialmente parado nos problemas de espalhamento, colisão elástica só quando for dito.

**Dois pontos de física para você decidir (⚠):**
1. ⚠ No hook e no C08, os dois ângulos candidatos (25° e 40°) estão **fora** do cone de 14,5°: ambos são impossíveis para a razão um
   quarto. A cena marca só o 40° com X. A fala diz a verdade (os dois são proibidos); sugiro acrescentar um X também no 25°.
2. ⚠ No gancho, o texto do Kaio diz "efeitos completamente diferentes", mas o impulso é o mesmo e a translação do centro também; só o giro
   muda. Mantive o texto do Kaio como está (decisão dele).

---

## HOOK

### H1 — tela: disco pesado vem da esquerda com a seta de velocidade; o disco leve está parado
> movimento: o pesado já está andando desde a primeira palavra; a seta de velocidade acompanha o disco.
Olha essa colisão. Um disco pesado vem da esquerda e bate num disco leve, que estava parado ali, de boa.

### H2 — tela: depois do choque, o pesado desvia um pouquinho para cima e o leve sai para baixo; a trajetória real aparece
> movimento: os dois discos seguem andando; a trajetória real se desenha enquanto eles se afastam.
E repara no que acontece: o pesado não segue reto... ele desvia só um pouquinho para cima. E o leve sai de lado, para baixo.

### H3 — tela: duas direções tracejadas aparecem, uma de cada vez (vinte e cinco e quarenta graus); X no quarenta
> movimento: cada tracejada é desenhada devagar (Create ~1,2 s) enquanto a voz cita o ângulo; ⚠ acrescentar o X também no vinte e cinco.
Agora uma pergunta de curioso: será que o pesado poderia ter saído por qualquer caminho? Vinte e cinco graus para cima? Quarenta graus?

### H4 — tela: PARA ONDE ELA PODE SAIR?
> movimento: a pergunta entra com FadeIn e os dois X pulsam uma vez.
Spoiler: a natureza tem um segurança na porta, e ele não deixa passar qualquer direção. Por quê? É isso que a gente vai descobrir hoje.

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: COLISÕES EM 2D · NESTE VÍDEO: PARA ONDE OS CORPOS PODEM SAIR
Hoje a gente vai para as colisões em duas dimensões. A ideia é você sair daqui sabendo para onde os corpos podem sair depois de um choque... e, principalmente, para onde eles não podem. Sem bola de cristal: só geometria e uma boa dose de paciência. Bora?

## C01 — DO 1D PARA O 2D

### C01-1 — tela: trilho; um bloco bate no outro parado e os dois seguem pelo trilho
> movimento: a colisão roda inteira; depois do choque os blocos continuam andando até a próxima âncora.
Lembra do vídeo passado? A gente estudou colisões em uma dimensão: tudo acontecendo em cima de uma linha, um trilho. Um bloco bate no outro, e os dois seguem... sempre pelo mesmo trilho. Uma rua de mão única da física.

### C01-2 — tela: a grade aparece em volta; o trilho engrossa e raios tracejados saem do ponto do choque, um por vez
> movimento: os seis raios nascem em sequência (LaggedStart) acompanhando "sinuca", "cruzamento", "qualquer lado".
Só que a vida real não tem trilho. Pensa numa partida de sinuca, ou em dois carros se encontrando num cruzamento: depois do choque, cada corpo pode sair para qualquer lado do plano. Aquela linha era só um eixo, e agora o plano inteiro está liberado.

### C01-3 — tela: 1D = CASO ESPECIAL
> movimento: a frase entra com FadeIn e o trilho pisca uma vez (destaque de "caso especial").
Ou seja: a colisão em uma dimensão é só um caso especial. A física é a mesma de sempre; o que muda é que agora a geometria entra em cena. E já aviso: ela vai roubar a cena.

## C02 — MOMENTO É UM VETOR

### C02-1 — tela: ANTES: o corpo um com a seta de momento magenta; o corpo dois parado
> movimento: a seta cresce junto da fala; o corpo dois pulsa quando a voz diz "parado".
Vamos montar o cenário, passo a passo. Antes da colisão, o corpo um vem com o seu momento linear, que também aparece como quantidade de movimento: é a massa vezes a velocidade. O corpo dois está parado, então o momento dele é zero. Zero de movimento, zero de momento.

### C02-2 — tela: DEPOIS: os dois saem em direções diferentes, com os momentos finais
> movimento: os corpos andam até a posição final; as setas dos momentos crescem uma de cada vez.
Depois do choque, os dois saem em direções diferentes, cada um com o seu momento final: o momento final do corpo um e o momento final do corpo dois.

### C02-3 — tela: os termos de P⃗ᵢ = p⃗₁ᵢ saem do rótulo da figura e viram a primeira equação
> movimento: o rótulo do momento inicial viaja até a equação (nasce); a seta pulsa quando a voz cita o total.
O momento total antes é só o do corpo um, porque o corpo dois está parado. Simples assim.

### C02-4 — tela: P⃗_f = p⃗₁f + p⃗₂f, com os termos saindo dos rótulos finais
> movimento: os dois rótulos finais viajam até a equação; Indicate no sinal de mais.
Depois, o momento total é a soma dos dois momentos finais. Mas atenção, que aqui mora a pegadinha: é uma soma de vetores, e vetor tem direção. Não dá para somar só os tamanhos, senão a conta sai errada.

### C02-5 — tela: P⃗ᵢ = P⃗_f vira p⃗₁ᵢ = p⃗₁f + p⃗₂f; caixa dupla
> movimento: os símbolos "se desmancham" nos termos (glifos); a caixa se desenha; as duas setas finais piscam junto de "soma".
Agora a regra de ouro. Se o choque é muito curto, o impulso das forças de fora é desprezível, e o momento total se conserva: o de antes é igual ao de depois. Então o momento inicial do corpo um é igual à soma dos dois momentos finais. Essa é a equação-mãe do vídeo inteiro. Pode tatuar. Brincadeira... mas anota.

### C02-6 — tela: triângulo de momentos (título TRIÂNGULO DE MOMENTOS NO ESPAÇO FÍSICO): a seta inicial na base, depois a do corpo um, depois a do corpo dois fechando
> movimento: cada seta é copiada da figura para o triângulo (ReplacementTransform) no instante em que é citada; ~1,5 s cada.
E essa soma tem um jeito lindo de ser vista: um triângulo. Presta atenção na construção. Põe o momento inicial na base. O momento final do corpo um sai da mesma origem. E o do corpo dois começa na ponta desse, ponta com cauda, e vai até a ponta do momento inicial, fechando o triângulo. Três vetores, um triângulo fechado: isso é a conservação do momento, desenhada.

### C02-7 — tela: NO 1D: VETORES COLINEARES / NO 2D: A GEOMETRIA APARECE; o triângulo pulsa
> movimento: o triângulo "respira" (Indicate) e o texto do 2D entra por último.
Em uma dimensão, esse triângulo era uma reta: os três vetores ficavam alinhados, e não tinha graça nenhuma. Em duas dimensões, ele se abre, e a geometria aparece. Por isso hoje tem tanto desenho. Pode ir separando o transferidor mental.

## C03 — DUAS EQUAÇÕES E UMA CONDIÇÃO

### C03-1 — tela: eixos horizontal e vertical; as três setas do triângulo crescem sobre os eixos
> movimento: eixos se desenham; as setas crescem (GrowArrow) enquanto a voz descreve.
Agora a gente põe eixos para conseguir fazer conta. O horizontal é a direção do momento inicial, e o vertical é perpendicular a ele. O triângulo de momentos fica apoiado nesses eixos.

### C03-2 — tela: arco do ângulo de saída do corpo um (para cima) e do corpo dois (para baixo, a partir do prolongamento horizontal)
> movimento: o primeiro arco se desenha com a palavra "para cima"; o tracejado do prolongamento e o segundo arco com "para baixo"; a nota MEDIDO ABAIXO DO EIXO entra por último.
Vamos combinar os ângulos, que isso derruba muita gente. O ângulo de saída do corpo um é o que o momento final dele faz com o eixo, para cima. O ângulo de saída do corpo dois a gente mede para baixo, a partir do prolongamento da horizontal. Os dois são positivos, cada um medido para o seu lado. Combinado?

### C03-3 — tela: no alto, a equação vetorial p⃗₁ᵢ = p⃗₁f + p⃗₂f
> movimento: a equação entra por FadeIn e o triângulo pulsa em sincronia com "equação vetorial".
Lá em cima, fica a equação vetorial: o momento inicial é igual à soma dos momentos finais.

### C03-4 — tela: projeção no eixo horizontal (chaves sob o eixo); da equação vetorial sai a equação do eixo x
> movimento: o tracejado vertical desce da ponta do momento do corpo um; as duas chaves se abrem; a equação vetorial se desfaz na do eixo x (glifos).
Agora é só projetar, como quem faz sombra no chão. Na horizontal, o momento final do corpo um contribui com o módulo dele, que é o tamanho do vetor, vezes o cosseno do ângulo de saída. O do corpo dois faz a mesma coisa, com o cosseno do ângulo dele. E o momento inicial, que está inteiro na horizontal, é igual à soma dessas duas partes. Pronto: a equação do eixo horizontal.

### C03-5 — tela: chave vertical à direita (seno do corpo um igual ao seno do corpo dois); a equação do eixo vertical sai da vetorial
> movimento: a chave vertical cresce; a equação vetorial se desfaz de novo, agora na do eixo y; setas verticais piscam.
Na vertical, o momento inicial não tem parte nenhuma. Então o que sobe tem que ser igual ao que desce: o módulo do momento do corpo um vezes o seno do ângulo dele é igual ao do corpo dois vezes o seno do ângulo dele. Zero igual a uma coisa menos a outra: a equação do eixo vertical.

### C03-6 (opcional) — tela: UMA CONSERVAÇÃO VETORIAL ⇓ DUAS EQUAÇÕES ESCALARES
> movimento: as duas equações piscam em sequência; a flecha entra no meio.
Resumindo: uma conservação vetorial virou duas equações com números comuns. Menos assustador, né?

### C03-7 — tela: tudo sai; MAS AINDA FALTA UMA CONDIÇÃO FÍSICA
> movimento: o título entra e fica com o brilho pulsando levemente (Indicate) até os cartões aparecerem.
Só que repara: se a gente conhece o ângulo de saída do corpo um, ainda sobram o módulo dos dois momentos finais e o ângulo do corpo dois. São três incógnitas para duas equações, tipo tentar pagar três contas com duas notas. Falta alguma coisa, e essa coisa é uma condição física.

### C03-8 — tela: três cartões acendem em sequência: ELÁSTICA (K_i = K_f), COMPLETAMENTE INELÁSTICA (v⃗₁f = v⃗₂f), OUTRO CASO
> movimento: cada cartão acende com a palavra do tipo; Indicate na equação do cartão.
E essa condição vem do tipo de colisão, igualzinho ao vídeo passado. Se a colisão é elástica, a energia cinética se conserva: essa é a equação que faltava. Se é completamente inelástica, os dois saem grudados, com a mesma velocidade. Ou então o problema entrega a condição de outro jeito.

### C03-9 — tela: MOMENTO + CONDIÇÃO FÍSICA
Moral da história: momento, mais condição física. É o mesmo método de sempre, só que agora o momento vem em duas equações.

## C04 — MASSAS IGUAIS: O ÂNGULO RETO

### C04-1 — tela: ANTES (o corpo um chega, o dois parado) e DEPOIS (saem a trinta e a sessenta graus); hipótese m₁ = m₂ = m, v₂ᵢ = 0
> movimento: as duas figuras entram juntas e as setas de velocidade crescem; a faixa de hipótese pisca em cada item.
Vamos ao primeiro caso, o mais bonito: duas massas iguais, o alvo parado e uma colisão elástica. Pensa na sinuca: a bola branca bate numa bola parada, de massa igual. Quem nunca fez isso e ficou torcendo para a branca não cair na caçapa?

### C04-2 — tela: os rótulos de velocidade viajam para a equação m v⃗₁ᵢ = m v⃗₁f + m v⃗₂f; AS MASSAS SE CANCELAM
> movimento: cada rótulo voa da figura até a equação (nasce); os três "m" encolhem e saem para cima quando a voz diz "cancela".
Primeiro, o momento. O momento inicial é a massa vezes a velocidade inicial do corpo um. Depois, a soma dos dois momentos finais: a massa vezes a velocidade final de cada um. Repara: a massa é a mesma em todo mundo... então ela cancela. Sobra uma relação só de velocidades: a velocidade inicial é a soma vetorial das duas velocidades finais.

### C04-3 — tela: triângulo de velocidades (base: velocidade inicial; depois as duas finais, ponta com cauda)
> movimento: as setas crescem uma de cada vez; a ponta do triângulo balança devagar (o ponto Q desliza) para mostrar que o ângulo ainda é qualquer um.
Dá para desenhar essa relação também: um triângulo de velocidades, igualzinho ao de momentos, só que sem a massa. E olha: por enquanto, o ângulo entre as duas velocidades finais pode ser qualquer um. Fica de olho nele.

### C04-4 — tela: K_i = K_f → ½ m v₁ᵢ² = ½ m v₁f² + ½ m v₂f² → (cancela ½ m) → v₁ᵢ² = v₁f² + v₂f²
> movimento: o K vira o v (letra por letra); os ½ m aparecem e depois encolhem e saem; nenhum quadro parado.
Agora a energia. Como a colisão é elástica, a energia cinética total antes é igual à de depois. Escrevendo cada energia como meio vezes a massa vezes a velocidade ao quadrado, o meio e a massa cancelam de novo. E fica: o quadrado da velocidade inicial é igual ao quadrado da velocidade final de um, mais o quadrado da velocidade final do outro. Guarda essa: é uma soma de quadrados.

### C04-5 — tela: (v⃗₁ᵢ)² = (v⃗₁f + v⃗₂f)² nasce da relação recuada; abre em v₁ᵢ² = v₁f² + v₂f² + 2 v⃗₁f · v⃗₂f
> movimento: os termos da relação vetorial (fantasma em cima) voam para os parênteses; na expansão o expoente vira o "2" do termo cruzado.
Agora o truque. Pega a relação vetorial, aquela da soma, e eleva ao quadrado. O quadrado de uma soma é o primeiro ao quadrado, mais o segundo ao quadrado, mais duas vezes o produto entre eles. Só que, com vetores, esse produto tem nome: produto escalar. É o tamanho de um, vezes o tamanho do outro, vezes o cosseno do ângulo entre eles.

### C04-6 — tela: caixas ciano em v₁ᵢ² e em v₁f² + v₂f²; o que é igual à energia cancela; sobra 2 v⃗₁f · v⃗₂f = 0
> movimento: as duas caixas desenham-se; o fantasma da energia pulsa; os termos iguais encolhem e saem para baixo; o zero entra no fim.
Agora compara essa equação com a da energia. A parte de cima é igualzinha! Dois caminhos diferentes, o mesmo resultado. Então o que sobra é só o termo cruzado... e ele tem que ser zero. Duas vezes o produto escalar das velocidades finais é igual a zero.

### C04-7 — tela: 2 v⃗₁f · v⃗₂f = 0 vira v⃗₁f ⊥ v⃗₂f (caixa dupla); o ponto do triângulo desliza até o ângulo reto; marca de ângulo reto nas duas figuras
> movimento: o ponto do triângulo desliza (~2 s) até o ângulo reto; a marca de ângulo reto se desenha no triângulo e no DEPOIS.
E produto escalar zero quer dizer o quê? Como ele depende do cosseno do ângulo entre os vetores, e o cosseno só vale zero em noventa graus, os dois vetores são perpendiculares. Olha o triângulo: o ângulo entre as velocidades finais vira um ângulo reto. É o famoso noventa graus da sinuca: depois do choque, as duas bolas se afastam formando um ângulo reto.

### C04-8 — tela: NO CASO FRONTAL, UM DOS VETORES É NULO. NO DESVIO OBLÍQUO, NENHUM MÓDULO É NULO.
> movimento: as duas linhas entram uma de cada vez; a seta do alvo pulsa.
Um cuidado: se o choque for de frente, uma das velocidades finais é zero, e não dá para falar de ângulo com um vetor que não existe. Mas num desvio oblíquo, em que as duas bolas andam, é sempre noventa graus.

### C04-9 — tela: três pílulas: ELÁSTICA, MASSAS IGUAIS, ALVO PARADO
> movimento: cada pílula entra com a palavra; as três pulsam juntas em "as três".
E guarda as três condições juntas, porque o ângulo reto só vale se as três valem: colisão elástica, massas iguais e alvo parado. Faltou uma? Dá ruim.

## C05 — BILHAR

### C05-1 — tela: mesa de bilhar; a bola um com a seta de velocidade; cartão: velocidade inicial dez metros por segundo, ELÁSTICA; massas iguais, alvo parado, trinta graus
> movimento: a bola já se aproxima devagar da bola parada enquanto os cartões entram.
Bora aplicar isso num exercício clássico de bilhar. Uma bola vem a dez metros por segundo e bate numa bola parada, de mesma massa; a colisão é elástica. Depois do choque, a primeira bola desvia trinta graus em relação à direção original.

### C05-2 (opcional) — tela: choque; as bolas saem; arcos dos dois ângulos de saída
> movimento: choque em câmera lenta; os arcos se desenham junto das palavras "primeira" e "segunda".
A pergunta é: para onde sai a segunda bola, e com que velocidade cada uma sai?

### C05-3 — tela: triângulo retângulo grande: hipotenusa dez, catetos, ângulos de trinta e sessenta graus, marca de ângulo reto
> movimento: a hipotenusa cresce primeiro, depois o cateto da primeira bola, depois o da segunda; a marca de ângulo reto pulsa.
Como as massas são iguais, a gente já sabe o segredo: as duas velocidades finais são perpendiculares. Então o triângulo de velocidades é um triângulo retângulo, e a hipotenusa, o lado mais comprido, é a velocidade inicial: dez metros por segundo.

### C05-4 — tela: θ₁ + θ₂ = 90° ⇒ θ₂ = 60°
> movimento: o ângulo de sessenta graus pisca no triângulo e na mesa ao mesmo tempo.
O ângulo de uma bola mais o da outra dá noventa graus. Trinta mais sessenta: a segunda bola sai a sessenta graus, para o outro lado.

### C05-5 — tela: v₁f = v₁ᵢ cos 30° = 5√3 m/s; o cateto da primeira pulsa
> movimento: o cateto adjacente acende; a equação entra com os termos já nos lugares.
A velocidade da primeira é o cateto encostado no ângulo de trinta graus: dez vezes o cosseno de trinta graus. Cosseno de trinta é raiz de três sobre dois, então dá cinco raiz de três metros por segundo, mais ou menos oito vírgula sete.

### C05-6 — tela: a equação vira v₂f = v₁ᵢ sen 30° = 5 m/s (os símbolos se transformam); o outro cateto pulsa
> movimento: cosseno vira seno letra por letra; a raiz some e fica o cinco; o cateto da segunda pisca.
A da segunda é o outro cateto: dez vezes o seno de trinta graus. Seno de trinta é um meio... cinco metros por segundo. E confere com Pitágoras: setenta e cinco mais vinte e cinco dá cem, que é dez ao quadrado. Olha só: sinuca é aula de trigonometria disfarçada.

## C06 — MASSAS DIFERENTES

### C06-1 — tela: dois discos de tamanhos diferentes e "m₁ ≠ m₂"; A PERPENDICULARIDADE NÃO VALE; o triângulo de momentos com o ângulo de saída do corpo um
> movimento: os discos entram; o triângulo cresce e o arco do ângulo se desenha.
E se as massas forem diferentes? Aí o ângulo reto some: ele dependia de as massas serem iguais. Mas o triângulo de momentos continua valendo sempre, porque ele vem só da conservação. Então é nele que a gente vai trabalhar. Calma que a conta cresce um pouquinho, mas cada passo é simples, e eu vou junto com você.

### C06-2 — tela: os rótulos do triângulo viajam e formam p⃗₂f = p⃗₁ᵢ − p⃗₁f
> movimento: os três rótulos voam do triângulo até a equação; os lados do triângulo piscam em sequência.
Do triângulo sai direto: o momento final do corpo dois é o momento inicial menos o momento final do corpo um.

### C06-3 — tela: lei dos cossenos: cada vetor vira o seu quadrado e nasce o termo cruzado com o cosseno
> movimento: cada termo se desfaz no quadrado (glifos); o ângulo pisca na figura quando a voz diz "ângulo entre eles".
Agora, para ligar os tamanhos ao ângulo, a lei dos cossenos. É um Pitágoras com um ajuste: o quadrado de um lado é a soma dos quadrados dos outros dois, menos duas vezes o produto desses dois lados vezes o cosseno do ângulo entre eles. Se o ângulo for reto, o cosseno é zero e volta o Pitágoras de sempre. Aqui, o ângulo entre o momento inicial e o momento final do corpo um é o ângulo de saída.

### C06-4 — tela: energia elástica: momento ao quadrado sobre duas massas, com os numeradores vindos dos termos recuados; ELÁSTICA: K_i = K_f
> movimento: os três quadrados voam dos termos recuados até os numeradores; as barras de fração se desenham.
A condição física é a conservação da energia cinética. E dá para escrever a energia cinética usando o momento: é o momento ao quadrado, dividido por duas vezes a massa. Então a energia inicial do corpo um é igual à energia final do corpo um mais a do corpo dois. Repara que os quadrados dos momentos são os mesmos que apareceram na lei dos cossenos. Coincidência? Nenhuma.

### C06-5 — tela: λ = m₂/m₁ — RAZÃO DAS MASSAS
> movimento: o cartão entra e o lambda pulsa; o resto da equação continua na tela.
Para não carregar duas massas por aí, a gente cria uma ferramenta: a razão entre as massas, o corpo dois dividido pelo corpo um. Na tela ela aparece como a letra grega lambda. Daqui para frente eu falo só "a razão das massas".

### C06-6 — tela: p₂f² = λ (p₁ᵢ² − p₁f²)
> movimento: os quadrados trocam de lado, o sinal de mais vira menos e o denominador vira a razão (glifos).
Multiplicando a equação da energia por duas vezes a massa do corpo dois, o quadrado do momento final do corpo dois fica igual à razão das massas vezes a diferença entre o quadrado do momento inicial e o quadrado do momento final do corpo um.

### C06-7 — tela: as duas maneiras de escrever p₂f² (lei dos cossenos e energia) viajam para uma só equação
> movimento: os termos dos dois fantasmas voam para a equação nova; o sinal de igual entra por último.
Agora a gente tem duas maneiras de escrever a mesma coisa: o quadrado do momento final do corpo dois. Uma veio da geometria, outra veio da energia. Se são a mesma coisa, é só igualar.

### C06-8 — tela: a equação do segundo grau, tudo de um lado só; caixa dupla
> movimento: o lambda se reparte em um mais lambda e um menos lambda (glifos); a caixa se desenha; cada coeficiente pisca quando citado.
Arrumando tudo para um lado só, aparece uma equação do segundo grau, e a incógnita é o que a gente quer saber: o módulo do momento final do corpo um. Um mais a razão das massas, vezes esse módulo ao quadrado; menos duas vezes o momento inicial, vezes o cosseno do ângulo, vezes o módulo; mais um menos a razão das massas, vezes o momento inicial ao quadrado; tudo igual a zero.

### C06-9 — tela: O QUE ESSA EQUAÇÃO DIZ, GEOMETRICAMENTE, SOBRE TODOS OS MOMENTOS FINAIS POSSÍVEIS?
> movimento: a pergunta entra em duas linhas; a equação pulsa uma vez.
E agora a pergunta que importa, e que ninguém pergunta na escola: o que essa equação diz, geometricamente, sobre todos os momentos finais possíveis? Segura essa pergunta.

## C07 — A QUADRÁTICA É UM CÍRCULO

### C07-1 — tela: a equação cresce e ocupa o centro; p₁ᵢ cosθ₁ p₁f vira o produto escalar p⃗₁ᵢ · p⃗₁f; O PRODUTO ESCALAR APARECE
> movimento: o cosseno vira o ponto do produto escalar (glifos); as setas dos vetores aparecem sobre as letras.
Primeiro, um retoque. Lembra do produto escalar? Aquele produto do tamanho do momento inicial, vezes o tamanho do momento final, vezes o cosseno do ângulo, é exatamente o produto escalar dos dois vetores. Então a gente reescreve na forma vetorial, que é mais bonita e mais geral.

### C07-2 — tela: DIVIDA TUDO POR (1 + λ): o um mais lambda desce para baixo de cada termo
> movimento: os glifos de um mais lambda viajam para os denominadores (cópias); os parênteses ficam para trás; ~2,6 s.
Agora divide tudo por um mais a razão das massas. Olha o que acontece: esse um mais a razão vai parar embaixo de cada termo, e o primeiro termo fica limpinho, só o módulo ao quadrado.

### C07-3 — tela: COMPLETE O QUADRADO: SOME O MESMO TERMO DOS DOIS LADOS — o termo (p₁ᵢ/(1+λ))² nasce do termo do meio e aparece nos dois lados; o termo final atravessa a igualdade
> movimento: os glifos do termo central se copiam duas vezes (esquerda e direita); o último termo faz um arco por cima da igualdade; caixas coloridas no "primeiro" e no "segundo" termo acompanham a fala.
Agora o truque dos tempos de colégio: completar o quadrado. Aquele truque que você jurava que nunca ia usar na vida... chegou a hora. A ideia é esta: o primeiro termo ao quadrado, menos duas vezes o primeiro vezes o segundo, mais o segundo ao quadrado, é igual ao primeiro menos o segundo, tudo ao quadrado. No nosso caso, o primeiro é o momento final do corpo um, e o termo do meio já esconde o segundo: é o momento inicial dividido por um mais a razão das massas. Falta só o quadrado dele. Então a gente soma esse quadrado... nos dois lados, para a equação não mudar.

### C07-4 — tela: AGRUPE O QUADRADO PERFEITO: o lado esquerdo vira |p⃗₁f − p⃗₁ᵢ/(1+λ)|²
> movimento: os termos entram nas barras do módulo; o expoente vira o expoente da barra; os parênteses se fecham.
Agora o lado esquerdo virou um quadrado perfeito: o módulo do vetor "momento final do corpo um, menos o momento inicial dividido por um mais a razão das massas", tudo ao quadrado.

### C07-5 — tela: CONFERÊNCIA DO LADO DIREITO: 1/(1+λ)² − (1−λ)/(1+λ) = λ²/(1+λ)²; o lado direito vira (λ p₁ᵢ/(1+λ))²; caixa dupla
> movimento: as frações se juntam (glifos); a conferência aparece em baixo, termo por termo, enquanto a voz conta; a caixa se desenha no fim.
E o lado direito? São duas frações que simplificam bonito. Um sobre um mais a razão ao quadrado, menos um menos a razão sobre um mais a razão... dá a razão ao quadrado sobre um mais a razão ao quadrado. Está conferido na tela, pode pausar e fazer a conta. Então o lado direito é o quadrado de: razão das massas, vezes o momento inicial, sobre um mais a razão.

### C07-6 — tela: a álgebra se desmancha em |p⃗₁f − C⃗| = R, C⃗ = p⃗₁ᵢ/(1+λ), R = λ p₁ᵢ/(1+λ); entra o plano
> movimento: as frações viajam para as definições; o painel do plano entra por trás; nada fica parado.
Agora olha o que essa equação está dizendo. O módulo da diferença entre o vetor que a gente procura e um vetor fixo é igual a um número fixo. Chama o vetor fixo de centro e o número fixo de raio. Uma distância constante a partir de um ponto fixo... isso é a definição de um círculo!

### C07-7 — tela: PLANO DE p⃗₁f: eixos, seta do momento inicial, o círculo ciano nasce com o centro e o raio
> movimento: a seta cresce; o círculo se desenha (Create 1,8 s); o raio sobe do centro; os rótulos entram.
Então vamos desenhar um plano especial. Atenção: ele não é o espaço onde os corpos andam; é um mapa dos momentos finais possíveis do corpo um. O eixo horizontal é a parte do momento na direção original; o vertical, a parte perpendicular. Marca o momento inicial: uma seta na horizontal. O centro do círculo fica a um sobre um mais a razão dessa seta, e o raio é a razão das massas sobre um mais a razão. E aqui está o círculo.

### C07-8 — tela: CADA PONTO É UM p⃗₁f POSSÍVEL; o ponto percorre o círculo; p⃗₂f fecha o triângulo (UM PONTO DÁ p⃗₁f E p⃗₂f)
> movimento: o ponto anda pelo círculo (±55°, depois −70°, volta) o tempo todo da fala; as duas setas mudam de forma e sempre fecham.
Cada ponto desse círculo é um momento final possível para o corpo um. E, para cada ponto, o momento final do corpo dois é o que falta para fechar o triângulo até o momento inicial. Repara: movendo o ponto, o triângulo muda de forma... mas continua fechando. Um ponto só já entrega os dois momentos.

## C08 — DIREÇÕES POSSÍVEIS

### C08-1 — tela: o eixo horizontal se desenha até o primeiro ponto, na ponta do momento inicial; card: o momento final igual ao inicial, NADA MUDOU
> movimento: o eixo cresce; o flash no ponto acompanha "nada mudou".
Vamos passear pelo círculo. O eixo horizontal corta ele em dois pontos. O primeiro, na ponta do momento inicial: aqui o momento final do corpo um é igual ao inicial. Nada mudou: é como se os corpos nem tivessem se tocado. E esse estado também conserva tudo, por isso ele está no círculo.

### C08-2 — tela: o segundo ponto, mais atrás; card: p₁f = (m₁ − m₂)/(m₁ + m₂) p₁ᵢ; COLISÃO FRONTAL EM 1D
> movimento: o flash no segundo ponto; a fração do card se desenha termo por termo.
O segundo ponto é a colisão frontal. O corpo um continua na mesma linha, com o momento que a fórmula do vídeo passado dá: massa um menos massa dois, sobre a soma das massas, vezes o momento inicial. Ou seja: o 1D que a gente já conhecia estava escondido nesses dois pontos.

### C08-3 — tela: semirreta tracejada saindo da origem, com o ângulo de saída crescendo de cinco a dez graus; leitura do ângulo; DOIS JEITOS DE BATER, O MESMO DESVIO
> movimento: a semirreta gira o tempo todo da fala; os dois pontos de interseção e as duas setas acompanham.
Agora as direções oblíquas. Imagina uma semirreta saindo da origem, inclinada com um certo ângulo de saída do corpo um. Onde ela corta o círculo, existe um momento final possível naquela direção. Para ângulos pequenos, ela corta em dois pontos: dois jeitos de bater, o mesmo desvio. Um tira bastante momento do corpo um; o outro tira pouco, é de raspão.

### C08-4 — tela: o ângulo cresce; os dois pontos se aproximam e se fundem; TANGÊNCIA: AS DUAS SOLUÇÕES SE FUNDEM
> movimento: a semirreta continua girando (de dez graus até o ângulo da tangente, ~3 s); o anel pisca no ponto único.
Vai aumentando o ângulo... os dois pontos vão se aproximando... até virar um só. Esse é o instante da tangência: a semirreta encosta no círculo sem atravessar. É o limite.

### C08-5 — tela: o ângulo passa de vinte graus; SEM INTERSEÇÃO: SEM SOLUÇÃO FÍSICA
> movimento: a semirreta vai até vinte graus e fica "sem tocar"; a mensagem troca na hora certa.
E passando disso, a semirreta não toca o círculo. Sem interseção, sem solução: nenhum momento final é possível naquela direção. A natureza fechou a porta.

### C08-6 — tela: as duas tangentes e o cone; o espaço físico miniatura (ESPAÇO FÍSICO); a direção real do hook, a de vinte e cinco e a de quarenta graus
> movimento: as tangentes se desenham; o cone aparece; as três direções são desenhadas uma de cada vez com o rótulo; ⚠ X em cada uma das duas proibidas.
Vamos voltar ao disco pesado do começo. Desenhando as duas tangentes, aparece um cone: dentro dele, tem solução; fora, não. A colisão real ficou a dez vírgula nove graus: dentro do cone, em cima do círculo. Já vinte e cinco graus, e quarenta graus, ficam completamente fora. O segurança da porta não deixa passar.

### C08-7 — tela: AGORA SABEMOS POR QUÊ.
> movimento: a frase entra e a linha de quarenta graus pulsa.
Era essa a pergunta do começo, e o círculo respondeu: a geometria do momento só deixa passar algumas direções.

## C09 — O ÂNGULO MÁXIMO

### C09-1 — tela: o plano com o deslizador da razão das massas (zero vírgula cinco); o triângulo retângulo da tangente (marca de ângulo reto, o raio, a distância até o centro, o ângulo máximo)
> movimento: o triângulo se desenha em partes: tangente, raio, marca de ângulo reto, hipotenusa (⚠ destacar o trecho do eixo da origem até o centro); cada parte pisca quando citada.
Agora a gente vai tirar um número dessa geometria: qual é o maior desvio possível? Olha a tangente. Uma propriedade clássica da geometria: o raio que vai até o ponto de tangência é perpendicular à tangente. Então tem um triângulo retângulo aqui: a hipotenusa liga a origem ao centro do círculo, o cateto oposto ao ângulo é o raio, e o ângulo na origem é justamente o ângulo máximo.

### C09-2 — tela: sen θ_max = R/C = λ
> movimento: a fração se desenha; o cateto e a hipotenusa piscam; os dois valores do círculo aparecem e cancelam (Indicate).
Seno é cateto oposto sobre hipotenusa. Então o seno do ângulo máximo é o raio dividido pela distância até o centro. E essas duas medidas a gente já tem: o raio é a razão das massas vezes o momento inicial, sobre um mais a razão; a distância até o centro é o momento inicial sobre um mais a razão. Dividindo, quase tudo cancela... e sobra só a razão das massas. Que coisa linda.

### C09-3 — tela: θ_max = arcsen(m₂/m₁); caixa dupla
> movimento: os termos viajam de cima (θ_max e lambda), o lambda se desdobra em m₂/m₁; a caixa se desenha.
Logo, o ângulo máximo é o arco cujo seno é a razão das massas: o arco seno da massa do corpo dois sobre a massa do corpo um. Alvo bem mais leve que o projétil... ângulo máximo pequeno.

### C09-4 — tela: TRADUÇÃO ALGÉBRICA: Δ ≥ 0 ⇔ cos²θ ≥ 1 − λ² ⇔ sen θ ≤ λ
> movimento: as três linhas entram em sequência; o cone do plano pisca junto da palavra "cone".
E tem uma conferência algébrica, para quem desconfia de desenho. Na equação do segundo grau, o discriminante precisa ser maior ou igual a zero para existir solução. Fazendo a conta, isso é o mesmo que dizer que o cosseno ao quadrado do ângulo é maior ou igual a um menos a razão ao quadrado... que é o mesmo que o seno do ângulo ser menor ou igual à razão das massas. A álgebra e a geometria concordam. E quando duas coisas independentes concordam, é sinal de que a gente acertou.

### C09-5 — tela: o deslizador anda: a razão cai para um quarto e sobe até zero vírgula oitenta e cinco; o círculo encolhe e cresce; o cone fecha e abre
> movimento: o deslizador percorre os dois trechos (~5,5 s) durante toda a fala; o valor do ângulo máximo na leitura muda junto.
Vamos mexer na razão das massas, que é divertido. Quando o alvo fica mais leve, o círculo encolhe e o cone se fecha: o corpo pesado quase não se desvia. Quando o alvo fica mais pesado, o círculo cresce e o cone se abre.

### C09-6 — tela: razão igual a um; o círculo passa pela origem e a seta do momento inicial é um diâmetro; TEOREMA DE THALES
> movimento: o deslizador chega a um; ⚠ o diâmetro é traçado (tracejado) e as duas cordas, da origem e da ponta do diâmetro até o ponto, se desenham; o ângulo reto aparece no ponto.
Agora o caso especial: razão igual a um, massas iguais. O círculo passa pela origem, e o segmento que vai da origem até a ponta do momento inicial é um diâmetro. Aí entra um velho amigo da geometria, de mais de dois mil e quinhentos anos atrás: o teorema de Tales. Ele diz: pega um diâmetro e qualquer ponto da circunferência, liga esse ponto às duas pontas do diâmetro... e o ângulo que se forma é sempre reto. Sempre.

### C09-7 — tela: p⃗₁f ⊥ p⃗₂f; o ponto percorre o círculo (sessenta, cento e cinquenta, cento e oitenta graus); θ_max = 90°; p₁f = 0, RECUO FRONTAL
> movimento: o ponto anda sem parar durante a fala; o ângulo reto o acompanha; no fim, o vetor do corpo um encolhe até zero.
Agora liga os pontinhos. As duas pontas do diâmetro são a origem e a ponta do momento inicial. O ponto na circunferência é o momento final do corpo um. E os dois lados que chegam nesse ponto são justamente o momento final do corpo um e o do corpo dois. Resultado: os dois são perpendiculares. É o ângulo reto da sinuca! Só que agora a gente sabe de onde ele vem. Passeia com o ponto: o ângulo reto fica o tempo todo. O ângulo máximo de desvio vale noventa graus. E quando o ponto chega na ponta do diâmetro... o momento final do corpo um é zero. O corpo para, e o alvo leva tudo: é a colisão frontal de massas iguais, a troca de velocidades.

### C09-8 — tela: razão de um até dois; a origem fica dentro do círculo; A ORIGEM FICA DENTRO DO CÍRCULO; QUALQUER DIREÇÃO ATÉ 180°; A INCIDENTE PODE VOLTAR; NÃO EXISTE ÂNGULO MÁXIMO MENOR QUE 180°
> movimento: o deslizador sobe até dois (3 s); o ponto passa para a esquerda do eixo vertical; as três mensagens entram em sequência.
E se o alvo for mais pesado que o projétil? A razão das massas passa de um, e o círculo engole a origem. Agora qualquer semirreta que sai da origem, em qualquer direção, corta o círculo exatamente uma vez. Quer dizer: não existe ângulo máximo menor que cento e oitenta graus. O corpo incidente pode até voltar para trás. É a bolinha de pingue-pongue batendo numa bola de boliche.

### C09-9 (opcional) — tela: o resumo (as três situações lado a lado, em palavras)
> movimento: ⚠ cena nova, curta: três miniaturas do círculo (alvo leve, massas iguais, alvo pesado) aparecem em sequência com a fala.
Resumindo: alvo mais leve, existe um ângulo máximo. Massas iguais, o máximo é noventa graus. Alvo mais pesado, qualquer ângulo vale. Guarda isso, que cai em prova.

## C10 — ALFA CONTRA NÊUTRON

### C10-1 — tela: o plano com o círculo para a razão um quarto; alfa (quatro vezes a massa do nêutron) e nêutron; a razão vale um quarto
> movimento: os dois discos entram com a massa de cada um; o círculo respira uma vez.
Um exemplo de verdade, da física nuclear: uma partícula alfa bate num nêutron parado. A alfa tem quatro vezes a massa do nêutron, então a razão das massas é um quarto.

### C10-2 — tela: cone, tangentes e θ_max = arcsen ¼ ≈ 14,5°; arco do ângulo máximo
> movimento: as tangentes crescem; o arco se desenha; a equação entra.
O ângulo máximo de desvio da alfa é o arco seno de um quarto: uns catorze vírgula cinco graus. Por mais de raspão que seja o choque, a alfa nunca sai desviada mais do que isso. Ela é um caminhão contra um fusquinha: não se desvia fácil.

### C10-3 — tela: o ponto de tangência; a seta do momento final da alfa até o círculo e a do nêutron fechando o triângulo
> movimento: o ponto aparece; as duas setas crescem uma de cada vez.
Olha o caso extremo: o ponto de tangência. O momento final da alfa vai até o círculo no ângulo limite, e o do nêutron fecha o triângulo.

### C10-4 — tela: p₁f/p₁ᵢ = cos θ_max/(1 + λ) = √15/5 ≈ 0,775
> movimento: o θ_max desce para dentro do cosseno e o um quarto vira lambda no denominador (glifos); a tangente da figura pisca.
Quanto vale o momento da alfa nesse ponto? Pelo teorema de Pitágoras no triângulo retângulo da tangente: é a distância até o centro ao quadrado, menos o raio ao quadrado, tudo sob uma raiz. Dá o momento inicial vezes o cosseno do ângulo máximo, sobre um mais a razão. Com os números: raiz de quinze sobre cinco, uns zero vírgula sete sete cinco do momento inicial.

### C10-5 — tela: K₁f/K₁ᵢ = (p₁f/p₁ᵢ)² = 60 %
> movimento: a fração entra no parêntese; o sessenta por cento surge no fim.
Energia cinética é proporcional ao momento ao quadrado. Então a energia final da alfa é essa fração ao quadrado: sessenta por cento da inicial.

### C10-6 — tela: barra de energia (alfa e nêutron); K_n,f = 0,40 K_α,i; θ₂ ≈ 37,8°; arco do ângulo do nêutron
> movimento: a barra cresce em duas partes; o arco do nêutron se desenha; o sessenta vira quarenta (glifos).
Os outros quarenta por cento foram para o nêutron. E o nêutron sai a uns trinta e sete vírgula oito graus. Mas atenção: isso é no ângulo limite. Não é a transferência máxima de energia.

### C10-7 (opcional) — tela: NA COLISÃO FRONTAL: 4λ/(1+λ)² = 16/25 = 64 %
> movimento: a fração entra termo por termo; o ponto vai para o eixo e fica sobre o ponto da colisão frontal.
A transferência máxima acontece na colisão frontal: quatro vezes a razão das massas, sobre um mais a razão ao quadrado. Dá dezesseis vinte e cinco avos: sessenta e quatro por cento. Mesmo de frente, o nêutron não leva tudo. Para o alvo levar a energia toda, as massas precisam ser iguais.

## C11 — ACIDENTE EM 2D

### C11-1 — tela: cruzamento (pista azul); caminhão azul vindo do sul, carro violeta vindo do oeste; o enunciado com o problema; rótulos de massa e velocidade
> movimento: os veículos se aproximam devagar durante toda a leitura do enunciado; o rótulo de cada um aparece quando a voz o cita.
Hora de um problema com cara de prova. Um caminhão e um carro colidem num cruzamento e ficam presos um no outro. O caminhão tem três mil quilogramas e vinha para o norte a sessenta quilômetros por hora. O carro tem mil quilogramas e vinha para o leste a noventa quilômetros por hora. Depois do choque, o conjunto derrapa no asfalto, com coeficiente de atrito cinético zero vírgula cinco. A pergunta: qual a velocidade logo depois do choque, e quanto eles derrapam? Spoiler: o caminhão leva vantagem. Mas quanta?

### C11-2 — tela: o choque (flash); os veículos presos andam juntos; a seta da velocidade final
> movimento: choque em câmera lenta; os dois seguem juntos enquanto a seta cresce.
Primeiro, o sistema: caminhão e carro juntos. Durante o choque, o atrito com o asfalto é desprezível perto das forças de contato. Então o momento total, que é um vetor, se conserva. E como eles ficam presos, a condição física é uma só: a velocidade final é a mesma para os dois.

### C11-3 — tela: P⃗ᵢ = P⃗_f se abre nas duas componentes: leste (m · 25 = (M + m) v_fx) e norte (M · 50/3 = (M + m) v_fy)
> movimento: a equação se divide em duas linhas (glifos), cada uma com seus termos; a componente citada pisca.
Escrevo o momento antes igual ao momento depois, e separo em duas componentes. Na direção leste, só o carro tem momento: mil quilogramas vezes vinte e cinco metros por segundo, que é noventa quilômetros por hora. Isso é igual à massa total vezes a componente leste da velocidade final. Na direção norte, só o caminhão: três mil quilogramas vezes cinquenta sobre três metros por segundo, que são os sessenta quilômetros por hora. Igual à massa total vezes a componente norte.

### C11-4 — tela: v_fx = 6,25 m/s; v_fy = 12,5 m/s
> movimento: as contas viram números (glifos); as duas componentes pulsam.
Resolvendo: mil vezes vinte e cinco, dividido por quatro mil, dá seis vírgula vinte e cinco metros por segundo para o leste. E três mil vezes cinquenta sobre três, dividido por quatro mil, dá doze vírgula cinco metros por segundo para o norte.

### C11-5 — tela: tg θ = v_fy / v_fx = 2; θ ≈ 63,4°
> movimento: as duas componentes entram na fração; o dois vira o ângulo (glifos); o arco do ângulo se desenha na figura a partir do leste.
Agora, o ângulo da direção do movimento, medido a partir do leste: a tangente é a componente norte dividida pela componente leste, que dá dois. O ângulo cuja tangente é dois: sessenta e três vírgula quatro graus.

### C11-6 — tela: |v⃗_f| ≈ 13,98 m/s; o arco e a linha de referência do leste
> movimento: a seta de velocidade do conjunto fica pulsando devagar; o arco do ângulo acompanha.
E o módulo da velocidade: raiz da soma dos quadrados das componentes... quase catorze metros por segundo. Repara que o vetor aponta mais para o norte: o caminhão é mais pesado e puxa o conjunto para o lado dele.

### C11-7 — tela: O MOMENTO VALE SEM CONSERVAR K; barra de energia (ciano e laranja)
> movimento: as duas barras crescem; o laranja pisca quando a voz diz "perdeu".
E a energia cinética? Não se conserva: é uma colisão completamente inelástica. Uma boa parte virou energia interna: lataria amassada, calor. A barra mostra: o laranja é o que se perdeu. É quase metade da energia cinética.

### C11-8 (opcional) — tela: cartão do resultado: velocidade final (6,25; 12,5) m/s, ângulo e módulo
> movimento: as três linhas entram em sequência; as componentes da seta pulsam.
Então, resumindo o impacto: velocidade final com seis vírgula vinte e cinco para o leste e doze vírgula cinco para o norte; a sessenta e três vírgula quatro graus do leste; módulo de uns catorze metros por segundo.

### C11-9 — tela: IMPACTO: MOMENTO / DEPOIS: TRABALHO–ENERGIA; dados do atrito; ½ (M + m) v_f² = μ_k (M + m) g d
> movimento: o veículo conjunto começa a derrapar; a equação nasce junto.
Agora a colisão acabou, e começou outro processo: a derrapagem. Mudou o processo, muda o princípio. No impacto, momento. Depois dele, trabalho e energia: a energia cinética que o conjunto tinha logo depois do choque é toda gasta pelo trabalho do atrito, ao longo da distância percorrida. Meio vezes a massa total vezes a velocidade ao quadrado, igual ao coeficiente de atrito vezes a massa total vezes a aceleração da gravidade vezes a distância.

### C11-10 — tela: o conjunto derrapa até parar; a cota da distância aparece; d = v_f²/(2 μ_k g) ≈ 19,5 m; A MASSA CANCELA
> movimento: derrapagem completa; a cota se desenha; a equação se transforma (o meio vira o dois do denominador, os dois fatores de massa se anulam).
Olha ele derrapando. A massa total aparece nos dois lados, então cancela: não importa quão pesado seja o conjunto. A distância é a velocidade ao quadrado, dividido por duas vezes o coeficiente de atrito vezes a gravidade. Cento e noventa e cinco vírgula três, dividido por dez: uns dezenove vírgula cinco metros.

### C11-11 (opcional) — tela: COMO NO PÊNDULO: SEPARE OS PROCESSOS
E lembra do pêndulo balístico do vídeo passado? Mesma lição: no impacto, momento; depois, energia. Separa os processos e a vida fica fácil.

## C12 — EXPLOSÕES

### C12-1 — tela: um corpo parado; P⃗ᵢ = 0⃗
> movimento: a vinheta pulsa de leve; o corpo tem um tremor curto antes da explosão.
Agora o contrário de uma colisão: uma explosão. Um corpo parado, com momento total zero, vai se partir em três pedaços.

### C12-2 (opcional) — tela: flash; três fragmentos saem com as setas de momento; rastros
> movimento: explosão com onda; os fragmentos se afastam durante toda a fala.
Bum! Cada pedaço sai com o seu momento, uns mais rápidos, outros mais lentos, dependendo da massa.

### C12-3 — tela: SE PARTIU DO REPOUSO; Σ p⃗ₖ = 0⃗ vira p⃗₁ + p⃗₂ + p⃗₃ = 0⃗; os três momentos formam um triângulo fechado
> movimento: o triângulo é desenhado vetor por vetor, ponta com cauda; a soma se desdobra nos três termos.
Como o corpo estava parado e o impulso externo é desprezível, o momento total depois também é zero: a soma dos três momentos é o vetor nulo. E olha o triângulo: três vetores que somam zero se encaixam, ponta com cauda, e fecham. Com dois pedaços, eles sairiam opostos, em linha reta; com três, formam um triângulo.

### C12-4 — tela: barras de energia (interna e cinética) e K_i = 0 → K_f > 0; TOTAL: CONSTANTE
> movimento: a barra laranja encolhe enquanto a ciano cresce; a linha do total fica fixa.
E a energia? Antes, a energia cinética era zero. Depois, é maior que zero. De onde veio? Da energia interna, a química do explosivo, por exemplo, que se converte em cinética. O total é constante. É o inverso da colisão inelástica: lá, a cinética virava interna; aqui, a interna vira cinética.

## C13 — MÉTODO E SÍNTESE

### C13-1 — tela: cinco cartões; o primeiro: SISTEMA?; o sistema (os dois corpos) dentro da caixa tracejada
> movimento: os cartões entram em cascata; o marcador percorre os cartões o tempo todo.
Vamos juntar tudo num método, para você levar para a prova. Primeiro: qual é o sistema? Quem está dentro da caixa tracejada.

### C13-2 — tela: cartão dois: J_ext ≈ 0 ⇒ P⃗ᵢ = P⃗_f
> movimento: o marcador desce até o cartão dois; a equação entra.
Segundo: o impulso externo é desprezível durante o choque? Se sim, o momento total se conserva.

### C13-3 (opcional) — tela: cartão três: 1D: UMA COMPONENTE; 2D: DUAS + GEOMETRIA VETORIAL
Terceiro: quantas dimensões? Em uma, uma equação. Em duas, duas componentes, mais a geometria dos vetores.

### C13-4 — tela: cartão quatro: ELÁSTICA → K_i = K_f; COMPLETAMENTE INELÁSTICA → v⃗₁f = v⃗₂f; EXPLOSÃO; OUTRO CASO
> movimento: as quatro linhas entram em sequência, junto de cada tipo.
Quarto: qual é o tipo de evento? Elástica: a energia cinética se conserva. Completamente inelástica: a mesma velocidade final. Explosão: a energia interna alimenta a cinética. Ou outro caso, em que o enunciado dá a condição.

### C13-5 — tela: cartão cinco: SEPARE OS PROCESSOS: IMPACTO → DESLIZAMENTO
E quinto: depois da colisão, começou outro processo? Derrapagem, subida, queda? Então troca o princípio: separa os processos.

### C13-6 — tela: O QUE MUDOU DO 1D PARA O 2D?; as quatro linhas de resposta
> movimento: cada linha entra em FadeIn com a frase; o título pulsa uma vez no começo.
E a pergunta lá do começo? O que mudou do 1D para o 2D? A conservação do momento não mudou. O momento sempre foi um vetor. Em uma dimensão, a geometria ficava escondida dentro da linha. Em duas dimensões, ela aparece: direções, ângulos e estados possíveis.

### C13-7 — tela: faixa SISTEMA → P⃗ → GEOMETRIA → TIPO DE COLISÃO → NOVA ETAPA; 1D = MOMENTO + TIPO; 2D = MOMENTO + GEOMETRIA + TIPO
> movimento: os itens da faixa entram em sequência; as duas fórmulas de bolso entram por último; o "geometria" brilha uma vez.
Resumindo numa fórmula de bolso, para colar na parede: em uma dimensão, momento mais tipo de colisão. Em duas, momento, mais geometria, mais tipo de colisão. A geometria é o ingrediente novo... e, como você viu, é ela que decide quais finais são possíveis.

## C14 — GANCHO (texto do Kaio, mantido; o "Até a próxima!" fica para o encerramento)

### C14-1 — tela: um disco em aço e um projétil pequeno
> movimento: o projétil já se aproxima do disco; a vinheta respira.
Até aqui, a gente tratou os corpos como partículas. Isso significa que, para descrever a colisão, bastavam a massa, a velocidade e a direção do movimento. Mas corpos reais têm tamanho.

### C14-2 — tela: primeiro caso: o impacto no centro; o disco só translada; seta do impulso
> movimento: o projétil acelera até o contato (rush_into); flash; o disco desliza com a seta de velocidade do centro.
Agora imagina duas colisões com o mesmo impulso. Na primeira, o impacto acontece bem no centro do corpo. Nesse caso, o corpo pode simplesmente mudar o seu movimento de translação.

### C14-3 — tela: reset; segundo caso: o impacto fora do centro; o disco translada e gira
> movimento: o disco volta devagar; o projétil entra deslocado; o disco desliza e gira (marca radial e arco branco).
Na segunda, o impacto acontece deslocado para um dos lados. Aí, além de se mover, o corpo pode começar a girar.

### C14-4 — tela: a linha de ação e a distância entre ela e o centro; POR QUE O PONTO ONDE A FORÇA AGE IMPORTA?
> movimento: as linhas tracejadas se desenham; a chave e a distância aparecem; a pergunta entra.
E aí aparece uma pergunta nova: por que a mesma força pode produzir efeitos completamente diferentes, dependendo de onde ela é aplicada?

### C14-5 — tela: PRÓXIMO VÍDEO: POR QUE UMA FORÇA FAZ UM CORPO GIRAR? TORQUE E DINÂMICA DE ROTAÇÃO
> movimento: os três textos entram em sequência; o disco continua girando.
É justamente essa pergunta que leva ao conceito de torque. No próximo vídeo, a gente vai entender por que uma força faz um corpo girar, e como o ponto de aplicação muda completamente o resultado.

## ENCERRAMENTO

### E1 — tela: tudo sai; logo com anéis violeta; INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
> movimento: os anéis giram em sentidos alternados o tempo todo; a logo entra com escala.
Hoje a gente ligou momento, geometria e tipo de colisão para descobrir para onde os corpos podem sair, e para onde eles não podem. Se essas ideias ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### E2 — tela: POR QUE UMA FORÇA FAZ UM CORPO GIRAR? → PRÓXIMO VÍDEO: TORQUE E DINÂMICA DE ROTAÇÃO; disco com marca girando; ondas
> movimento: o disco gira e as ondas se abrem continuamente.
E fica a pergunta: por que uma força faz um corpo girar? Me conta aqui nos comentários: qual foi o que mais te surpreendeu, o ângulo reto da sinuca ou a direção proibida? Valeu demais por assistir, e até a próxima!

---

## Orçamento de tempo (fala × animação de hoje)

Estimativa: 2,8 palavras por segundo + 0,25 s por âncora. A voz real fica entre 2,7 e 3,0.

| Cena | Âncoras | Palavras | Fala ≈ | Animação hoje | Esticar × |
|---|---:|---:|---:|---:|---:|
| Hook | 4 | 93 | 34 s | 12,9 s | 2,7 |
| Abertura | 2 | 53 | 19 s | 6,7 s | 2,9 |
| C01 Do 1D para o 2D | 3 | 124 | 45 s | 11,9 s | 3,8 |
| C02 Momento é um vetor | 7 | 302 | 110 s | 23,7 s | 4,6 |
| C03 Duas equações e uma condição | 9 | 375 | 136 s | 29,5 s | 4,6 |
| C04 Massas iguais: o ângulo reto | 9 | 455 | 165 s | 44,0 s | 3,7 |
| C05 Bilhar | 6 | 219 | 80 s | 22,9 s | 3,5 |
| C06 Massas diferentes | 9 | 447 | 162 s | 31,1 s | 5,2 |
| C07 A quadrática é um círculo | 8 | 487 | 176 s | 45,2 s | 3,9 |
| C08 Direções possíveis | 7 | 294 | 107 s | 36,9 s | 2,9 |
| C09 O ângulo máximo (Thales) | 9 | 615 | 222 s | 49,7 s | 4,5 |
| C10 Alfa contra nêutron | 7 | 281 | 102 s | 24,7 s | 4,1 |
| C11 Acidente em 2D | 11 | 564 | 204 s | 47,7 s | 4,3 |
| C12 Explosões | 4 | 146 | 53 s | 20,7 s | 2,6 |
| C13 Método e síntese | 7 | 198 | 72 s | 37,5 s | 1,9 |
| C14 Gancho | 5 | 139 | 51 s | 30,6 s | 1,7 |
| Encerramento | 2 | 80 | 29 s | 14,2 s | 2,0 |
| **Total** | **109** | **4.872** | **≈ 29 min** (≈ 27 min a 3,0 p/s) | 8,2 min | 3,6 |

Sem as âncoras marcadas `(opcional)` (201 palavras): ≈ 28 min (≈ 26 min a 3,0 p/s). A ficha previa 15 a 16 min; como você pediu
detalhe (geometria, Tales, álgebra) e a cena se molda à voz, o vídeo vai para perto de 26 a 29 min. Se for longo demais, os cortes
que menos machucam são: C12 inteiro (explosões, 53 s), C10-7 (64 % na frontal), C09-9, C11-8, C11-11, C13-3 e C03-6.

## Como manter a cena sempre em movimento (kit para a sincronia)

Toda âncora precisa de pelo menos um destes, ligado à palavra que o cita (atraso máximo 0,2 s):
1. **Destaque que caminha:** uma caixa fina (`SurroundingRectangle`) passa de termo em termo da equação, na ordem em que a voz lê.
2. **Pulso no termo ou na seta citada** (`Indicate`), com o resto da cena atenuado (opacidade ~0,4) enquanto o citado fica aceso.
3. **Variáveis lentas:** o ângulo da semirreta (C08), o deslizador da razão das massas (C09), o ponto no círculo (C07, C09), o corpo derrapando (C11).
4. **Respiração** (escala 1,00 ↔ 1,02) nas setas de momento e no círculo, para nenhuma figura ficar congelada.
5. **Revelação por glifos com `run_time` esticado até o fim da frase;** o passo anterior só recua para o fantasma quando a voz termina o passo.
6. Fora da álgebra, `Create` mais lento (1,2 a 2 s) nas construções da geometria: tangente, raio, triângulo, diâmetro.

## Coisas novas a criar na cena (⚠)

1. X também na direção de 25° (hook C08-6 e H3): os dois ângulos candidatos são proibidos.
2. C09-1: destacar o trecho do eixo da origem até o centro (a hipotenusa do triângulo da tangente).
3. C09-6/7: desenhar o diâmetro (tracejado) e as duas cordas até o ponto; a marca de ângulo reto acompanha o ponto durante o passeio (Tales).
4. (Opcional) C09-9: três miniaturas do círculo (alvo leve, massas iguais, alvo pesado).
5. O resto é retiming e destaques sobre o que já existe.

## Para a fase de voz (depois da sua aprovação do texto)

- Tags (uma por trecho): `[curious]` no hook e nas perguntas; `[happy]` no bem-vindos; `[thoughtful]` na explicação; `[thoughtful, emphatic]` em conceitos-chave
  (equação-mãe do C02, ângulo reto do C04, completar o quadrado, Tales, método do C13); `[excited]` só em dois pontos: o ângulo reto da sinuca (C09-7) e
  "agora sabemos por quê" (C08-7); `[calm, satisfied]` no encerramento. Sem `[slowly]`. Pausa: `[short pause]` ou reticências.
- Conferir pronúncia: "lambda", "Tales", "arco seno", "nêutron", "cosseno".
- Sincronia: gerar a voz, extrair o tempo de cada âncora (ASR), travar `an(n, k)` no `cena.py`, e medir o atraso de cada âncora com um script
  (meta: ≤ 0,2 s, como no `conferir_sync.py` do yt_0013).
