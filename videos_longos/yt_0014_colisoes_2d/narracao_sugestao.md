# COLISÕES EM 2D — sugestão de narração (v1.2.1, ~16 min, sobre o preview v3)

Fonte da cena: `cena.py` v3 (preview `renders/yt_0014_preview_v3_960x540_15fps.mp4`, 490 s). Orçamento: plano de corte do chat de Produção (~2.490 palavras).
Padrão: `docs/padrao_video_longo.md` §5 e `docs/roteiro_voz_elevenlabs_v4.md`. Professor de cursinho **amigo e próximo**, "a gente"/"você",
**nunca a letra solta**, no máximo uma piada por cena (duas em C04 e C09). v1.1 guardada em `narracao_sugestao_v1_1.md`.

**Regra desta versão:** *a tela mostra os termos; a voz diz só a jogada* ("divide por um mais a razão das massas", "soma o mesmo termo dos
dois lados"). Nada de ler cada termo da equação em voz alta. Os passos de álgebra e geometria continuam; só mudam de "leitura" para "jogada".

**Como ler:** cada `###` é uma **âncora** (evento visual). `tela:` diz o que aparece; a fala começa junto desse evento. Linhas com `>` são
**notas de animação** (não faladas); ⚠ = coisa nova a criar. A cena se molda à voz.

**Sincronia:** a cena **nunca fica parada enquanto a voz fala** (kit de movimento no fim do arquivo). O evento visual de cada âncora começa
**no máximo 0,2 s depois da primeira palavra** da âncora (nunca antes).

**Notação falada** (apresentada uma vez, depois só o nome): momento inicial/final do corpo um e do corpo dois (p⃗₁ᵢ, p⃗₁f, p⃗₂f); velocidade
inicial/final (v⃗₁ᵢ, v⃗₁f, v⃗₂f); **o ângulo de saída do corpo um** (θ₁, para cima) e **do corpo dois** (θ₂, para baixo); **a razão das massas**
(λ = m₂/m₁, falada "lambda" só na apresentação); **o ângulo máximo** (θ_max); o centro e o raio do círculo. "Módulo" = tamanho do vetor.

**Retomada (v1.2.1):** o C01-1 diz que este vídeo continua o anterior e relembra o método (o tipo de colisão dá a condição que falta); o C03-3
diz "sobra incógnita para equação" (em geral são quatro incógnitas: módulos e ângulos de saída), sem cravar "três".

**Hipóteses ditas uma vez (C02):** choque muito curto (impulso externo desprezível), massas constantes, movimento num plano; alvo parado e
elástica só quando dito.

---

## HOOK

### H1 — tela: disco pesado vem da esquerda e bate no leve parado; depois o pesado desvia para cima e o leve sai para baixo; a trajetória real se desenha
> movimento: os dois discos andam o tempo todo; a trajetória real se desenha enquanto eles se afastam.
Olha essa colisão. Um disco pesado vem da esquerda e bate num disco leve, parado. Repara: o pesado desvia só um pouquinho para cima, e o leve sai de lado.

### H2 — tela: duas direções tracejadas (vinte e cinco e quarenta graus), uma de cada vez; ⚠ X nas duas
> movimento: cada tracejada se desenha devagar (~1,2 s) com o ângulo citado; ⚠ os dois X pulsam no fim.
Será que o pesado poderia ter saído por qualquer caminho? Vinte e cinco graus? Quarenta graus?

### H3 — tela: PARA ONDE ELA PODE SAIR?
> movimento: a pergunta entra com FadeIn; os dois X piscam uma vez.
Spoiler: a natureza tem um segurança na porta, e ele não deixa passar qualquer direção. Por quê? É isso que a gente vai descobrir hoje.

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: COLISÕES EM 2D · NESTE VÍDEO: PARA ONDE OS CORPOS PODEM SAIR
Hoje a gente vai para as colisões em duas dimensões. A ideia é você sair daqui sabendo para onde os corpos podem sair depois de um choque... e, principalmente, para onde eles não podem. Sem bola de cristal: só geometria e uma boa dose de paciência. Bora?

## C01 — DO 1D PARA O 2D

### C01-1 — tela: trilho; um bloco bate no outro parado; a grade aparece e raios tracejados saem do ponto do choque, um por vez
> movimento: a colisão roda inteira; os seis raios nascem em sequência (LaggedStart) com "sinuca", "cruzamento", "qualquer lado".
Este vídeo é a continuação direta do anterior. Lá, tudo acontecia numa linha, um trilho, e a gente viu que conservar o momento não basta: o tipo de colisão dá a condição que falta. Agora a gente mantém essa lógica e muda uma coisa só. Só que a vida real não tem trilho. Pensa numa sinuca, ou em dois carros num cruzamento: depois do choque, cada corpo pode sair para qualquer lado do plano.

### C01-2 — tela: 1D = CASO ESPECIAL
> movimento: a frase entra e o trilho pisca uma vez.
Ou seja: uma dimensão é só um caso especial. A física é a mesma; o que muda é que agora a geometria entra em cena.

## C02 — MOMENTO É UM VETOR

### C02-1 — tela: ANTES (corpo um com a seta de momento, corpo dois parado) e DEPOIS (os dois saem em direções diferentes)
> movimento: a seta cresce com a fala; o corpo dois pulsa em "parado"; os corpos andam até a posição final e as setas finais crescem uma de cada vez.
Antes da colisão, o corpo um vem com o seu momento linear, também chamado de quantidade de movimento: a massa vezes a velocidade. O corpo dois está parado, então o momento dele é zero. Depois, os dois saem em direções diferentes, cada um com o seu momento final.

### C02-2 — tela: P⃗ᵢ = p⃗₁ᵢ e P⃗_f = p⃗₁f + p⃗₂f, com os termos saindo dos rótulos da figura
> movimento: os rótulos viajam até as equações; Indicate no sinal de mais.
O momento total antes é só o do corpo um. Depois, é a soma dos dois momentos finais. Mas atenção: é soma de vetores, e vetor tem direção. Não dá para somar só os tamanhos.

### C02-3 — tela: P⃗ᵢ = P⃗_f vira p⃗₁ᵢ = p⃗₁f + p⃗₂f; caixa dupla
> movimento: os símbolos se desmancham nos termos (glifos); a caixa se desenha; as duas setas finais piscam em "soma".
Num choque muito curto, com massas constantes e tudo no plano, o impulso externo é desprezível, e o momento total se conserva: antes é igual a depois. Essa é a equação-mãe do vídeo. Pode tatuar. Brincadeira... mas anota.

### C02-4 — tela: triângulo de momentos (TRIÂNGULO DE MOMENTOS NO ESPAÇO FÍSICO); NO 1D: VETORES COLINEARES / NO 2D: A GEOMETRIA APARECE
> movimento: cada seta é copiada da figura para o triângulo (~1,5 s cada); o triângulo "respira" no fim.
E essa soma vira um triângulo: o momento inicial na base, o final do corpo um saindo da mesma origem, e o do corpo dois ponta com cauda, fechando. Em uma dimensão era uma reta. Em duas, ele se abre, e a geometria aparece.

## C03 — DUAS EQUAÇÕES E UMA CONDIÇÃO

### C03-1 — tela: eixos; as setas do triângulo crescem sobre eles; arco do ângulo do corpo um (para cima) e do corpo dois (para baixo, a partir do prolongamento horizontal)
> movimento: eixos se desenham; os arcos se desenham com "para cima" e "para baixo"; a nota MEDIDO ABAIXO DO EIXO entra por último.
Agora a gente põe eixos: o horizontal na direção do momento inicial. O ângulo de saída do corpo um se mede para cima; o do corpo dois, para baixo, a partir da horizontal. Combinado? Isso derruba muita gente.

### C03-2 — tela: da equação vetorial saem as equações dos eixos horizontal e vertical; chaves das projeções
> movimento: o tracejado vertical desce da ponta do momento do corpo um; as chaves se abrem; a equação vetorial se desfaz em duas (glifos).
Projeta no eixo horizontal: o momento inicial é a soma das duas projeções, cada uma com o cosseno do seu ângulo. Projeta no vertical: o que sobe é igual ao que desce, com o seno. Uma conservação vetorial virou duas equações com números comuns.

### C03-3 — tela: tudo sai; MAS AINDA FALTA UMA CONDIÇÃO FÍSICA; três cartões acendem (ELÁSTICA, COMPLETAMENTE INELÁSTICA, OUTRO CASO); MOMENTO + CONDIÇÃO FÍSICA
> movimento: o título pulsa; cada cartão acende com a palavra do tipo, com Indicate na equação.
Só que ainda sobra incógnita para equação: os módulos dos dois momentos e os ângulos de saída. É tipo tentar pagar várias contas com duas notas. Falta uma condição física, e ela vem do tipo de colisão. Elástica: a energia cinética se conserva. Completamente inelástica: os dois saem com a mesma velocidade. Ou o problema entrega outra. Moral da história: momento, mais condição física.

## C04 — MASSAS IGUAIS: O ÂNGULO RETO

### C04-1 — tela: ANTES e DEPOIS (saem a trinta e a sessenta graus); hipótese m₁ = m₂ = m, v₂ᵢ = 0
> movimento: as duas figuras entram juntas; as setas de velocidade crescem; a faixa de hipótese pisca item a item.
Primeiro caso, o mais bonito: massas iguais, alvo parado e colisão elástica. Pensa na sinuca: a bola branca bate numa parada, de massa igual. Quem nunca torceu para a branca não cair na caçapa?

### C04-2 — tela: os rótulos de velocidade viajam para m v⃗₁ᵢ = m v⃗₁f + m v⃗₂f; AS MASSAS SE CANCELAM; triângulo de velocidades
> movimento: cada rótulo voa até a equação; os três "m" encolhem e saem; o triângulo cresce e o ponto da ponta balança devagar (o ângulo ainda é qualquer um).
Pelo momento, a massa é a mesma em todo mundo, então cancela. Sobra a velocidade inicial igual à soma vetorial das duas velocidades finais: um triângulo de velocidades. E repara: por enquanto, o ângulo entre as finais pode ser qualquer um.

### C04-3 — tela: K_i = K_f → ½ m v₁ᵢ² = ½ m v₁f² + ½ m v₂f² → v₁ᵢ² = v₁f² + v₂f²
> movimento: o K vira o v (letra por letra); os ½ m aparecem e depois encolhem e saem.
Pela energia cinética, o meio e a massa cancelam também: o quadrado da velocidade inicial é igual à soma dos quadrados das duas velocidades finais. Guarda essa.

### C04-4 — tela: (v⃗₁ᵢ)² = (v⃗₁f + v⃗₂f)² nasce da relação recuada; abre em v₁ᵢ² = v₁f² + v₂f² + 2 v⃗₁f · v⃗₂f
> movimento: os termos da relação vetorial (fantasma em cima) voam para os parênteses; na expansão o expoente vira o "2" do termo cruzado.
Agora o truque: eleva ao quadrado a relação vetorial. Aparece um termo cruzado, o produto escalar das duas velocidades finais: o tamanho de um, vezes o do outro, vezes o cosseno do ângulo entre eles.

### C04-5 — tela: caixas ciano em v₁ᵢ² e em v₁f² + v₂f²; o que é igual à energia cancela; sobra 2 v⃗₁f · v⃗₂f = 0
> movimento: as caixas se desenham; o fantasma da energia pulsa; os termos iguais encolhem e saem para baixo; o zero entra no fim.
Compara com a energia: a parte de cima é igualzinha! Dois caminhos, o mesmo resultado. Então o termo cruzado tem que ser zero.

### C04-6 — tela: 2 v⃗₁f · v⃗₂f = 0 vira v⃗₁f ⊥ v⃗₂f (caixa dupla); o ponto do triângulo desliza até o ângulo reto; marcas de ângulo reto nas duas figuras
> movimento: o ponto desliza (~2 s) até o ângulo reto; a marca se desenha no triângulo e no DEPOIS.
E produto escalar zero, com o cosseno do ângulo, só acontece em noventa graus: as duas velocidades finais são perpendiculares. É o famoso ângulo reto da sinuca.

### C04-7 — tela: NO CASO FRONTAL, UM DOS VETORES É NULO. NO DESVIO OBLÍQUO, NENHUM MÓDULO É NULO.
> movimento: as duas linhas entram uma de cada vez; a seta do alvo pulsa.
Um cuidado: no choque frontal, uma das velocidades finais é zero, e não dá para falar de ângulo. No desvio oblíquo, é sempre noventa graus.

### C04-8 — tela: três pílulas: ELÁSTICA, MASSAS IGUAIS, ALVO PARADO
> movimento: cada pílula entra com a palavra; as três pulsam juntas em "as três".
E guarda as três condições juntas: elástica, massas iguais e alvo parado. Faltou uma? Dá ruim.

## C05 — BILHAR

### C05-1 — tela: mesa; bola um a dez metros por segundo, elástica, massas iguais, alvo parado, trinta graus; choque e arcos dos dois ângulos
> movimento: a bola já se aproxima enquanto os cartões entram; choque em câmera lenta; os arcos se desenham com "primeira" e "segunda".
Um exercício clássico de bilhar: uma bola a dez metros por segundo bate numa parada, de mesma massa, em colisão elástica, e desvia trinta graus. Para onde vai a segunda, e com que velocidades?

### C05-2 — tela: triângulo retângulo grande (hipotenusa dez; ângulos de trinta e sessenta graus; marca de ângulo reto); θ₁ + θ₂ = 90° ⇒ θ₂ = 60°
> movimento: a hipotenusa cresce primeiro, depois cada cateto; o ângulo de sessenta graus pisca no triângulo e na mesa.
Massas iguais: as velocidades finais são perpendiculares, então o triângulo é retângulo, com a hipotenusa igual a dez. Trinta e sessenta dão noventa: a segunda sai a sessenta graus.

### C05-3 — tela: v₁f = v₁ᵢ cos 30° = 5√3 m/s; a equação vira v₂f = v₁ᵢ sen 30° = 5 m/s
> movimento: o cateto da primeira acende; o cosseno vira seno letra por letra; a raiz some; o cateto da segunda pisca.
A primeira é o cateto do trinta: dez vezes o cosseno de trinta, cinco raiz de três, uns oito vírgula sete metros por segundo. A segunda é o outro cateto: dez vezes o seno de trinta, cinco metros por segundo. Pitágoras confere. Olha só: sinuca é aula de trigonometria disfarçada.

## C06 — MASSAS DIFERENTES

### C06-1 — tela: dois discos de tamanhos diferentes (m₁ ≠ m₂); A PERPENDICULARIDADE NÃO VALE; triângulo de momentos; p⃗₂f = p⃗₁ᵢ − p⃗₁f
> movimento: os discos entram; o triângulo cresce; os rótulos viajam para a equação; os lados piscam em sequência.
E se as massas forem diferentes? O ângulo reto some. Mas o triângulo de momentos continua valendo, porque vem só da conservação. Dele sai que o momento final do corpo dois é o inicial menos o final do corpo um.

### C06-2 — tela: lei dos cossenos: cada vetor vira o seu quadrado e nasce o termo cruzado com o cosseno
> movimento: cada termo se desfaz no quadrado (glifos); o ângulo pisca na figura em "ângulo de saída".
A lei dos cossenos liga os tamanhos ao ângulo: é um Pitágoras com um ajuste, menos duas vezes o produto dos lados vezes o cosseno do ângulo de saída. Se o ângulo for reto, volta o Pitágoras de sempre.

### C06-3 — tela: energia: momento ao quadrado sobre duas massas (numeradores vindos dos termos recuados); λ = m₂/m₁ — RAZÃO DAS MASSAS; p₂f² = λ (p₁ᵢ² − p₁f²)
> movimento: os quadrados voam dos termos recuados até os numeradores; o cartão da razão entra e o lambda pulsa; os quadrados trocam de lado (glifos).
A condição física é a energia cinética conservada, que dá para escrever com o momento: momento ao quadrado sobre duas vezes a massa. Para não carregar duas massas, a gente cria a razão entre elas, o corpo dois dividido pelo corpo um, que na tela aparece como lambda. Daqui para frente, só "a razão das massas".

### C06-4 — tela: as duas maneiras de escrever p₂f² viajam para uma equação; a equação do segundo grau em caixa dupla; O QUE ESSA EQUAÇÃO DIZ, GEOMETRICAMENTE, SOBRE TODOS OS MOMENTOS FINAIS POSSÍVEIS?
> movimento: os termos dos dois fantasmas voam para a equação nova; o lambda se reparte em um mais lambda e um menos lambda; a caixa se desenha; a pergunta entra em duas linhas.
Igualando as duas formas do quadrado do momento do corpo dois, sai uma equação do segundo grau no módulo do momento final do corpo um. A gente não vai resolver. A gente vai perguntar: o que ela diz, geometricamente, sobre todos os momentos finais possíveis? Segura essa pergunta.

## C07 — A QUADRÁTICA É UM CÍRCULO

### C07-1 — tela: a equação cresce e ocupa o centro; p₁ᵢ cosθ₁ p₁f vira o produto escalar; o um mais lambda desce para baixo de cada termo
> movimento: o cosseno vira o ponto do produto escalar (glifos); os glifos de um mais lambda viajam para os denominadores (~2,6 s).
Primeiro, o produto dos tamanhos vezes o cosseno é o produto escalar: a gente reescreve na forma vetorial. Depois, divide tudo por um mais a razão das massas: o um mais a razão vai parar embaixo de cada termo.

### C07-2 — tela: COMPLETE O QUADRADO: SOME O MESMO TERMO DOS DOIS LADOS; o termo (p₁ᵢ/(1+λ))² nasce do termo do meio e aparece nos dois lados; o último termo atravessa a igualdade
> movimento: os glifos do termo central se copiam duas vezes; o último termo faz um arco por cima da igualdade; caixas coloridas no "primeiro" e no "segundo" termo acompanham a fala.
Agora o truque dos tempos de colégio: completar o quadrado. Aquele que você jurava que nunca ia usar na vida... chegou a hora. Um quadrado perfeito tem esse formato: o primeiro ao quadrado, menos duas vezes o primeiro vezes o segundo, mais o segundo ao quadrado. Aqui, o termo do meio já esconde o segundo: o momento inicial dividido por um mais a razão. Falta só o quadrado dele, e a gente soma nos dois lados, para a equação não mudar.

### C07-3 — tela: AGRUPE O QUADRADO PERFEITO; CONFERÊNCIA DO LADO DIREITO; o lado direito vira (λ p₁ᵢ/(1+λ))²; caixa dupla
> movimento: os termos entram nas barras do módulo; as frações se juntam (glifos); a conferência aparece em baixo, termo por termo; a caixa se desenha no fim.
Agora o lado esquerdo é um quadrado perfeito: o módulo de um vetor, ao quadrado. E o lado direito simplifica bonito: a conferência está na tela, pode pausar. Fica o quadrado da razão das massas vezes o momento inicial, sobre um mais a razão.

### C07-4 — tela: a álgebra se desmancha em |p⃗₁f − C⃗| = R, C⃗ = p⃗₁ᵢ/(1+λ), R = λ p₁ᵢ/(1+λ)
> movimento: as frações viajam para as definições; o painel do plano entra por trás; nada fica parado.
Olha o que a equação diz: o módulo da diferença entre o vetor que a gente procura e um vetor fixo é igual a um número fixo. Uma distância constante de um ponto fixo... isso é um círculo! O vetor fixo é o centro, e o número fixo é o raio.

### C07-5 — tela: PLANO DE p⃗₁f: eixos, seta do momento inicial, o círculo ciano nasce com o centro e o raio
> movimento: a seta cresce; o círculo se desenha (Create ~1,8 s); o raio sobe do centro; os rótulos entram.
Então vamos desenhar um plano especial, que não é o espaço onde os corpos andam: é o mapa dos momentos finais possíveis do corpo um. O eixo horizontal é a parte do momento na direção original; o vertical, a perpendicular. O centro fica a um sobre um mais a razão do momento inicial; o raio, a razão das massas sobre um mais a razão.

### C07-6 — tela: CADA PONTO É UM p⃗₁f POSSÍVEL; o ponto percorre o círculo; p⃗₂f fecha o triângulo
> movimento: o ponto anda pelo círculo o tempo todo da fala; as duas setas mudam de forma e sempre fecham.
Cada ponto do círculo é um momento final possível para o corpo um. E, para cada ponto, o momento do corpo dois fecha o triângulo. Um ponto só entrega os dois momentos.

## C08 — DIREÇÕES POSSÍVEIS

### C08-1 — tela: o eixo horizontal corta o círculo em dois pontos; no primeiro, NADA MUDOU; no segundo, COLISÃO FRONTAL EM 1D (p₁f = (m₁ − m₂)/(m₁ + m₂) p₁ᵢ)
> movimento: o eixo cresce; flash em cada ponto no momento citado; a fração do card se desenha termo por termo.
O eixo horizontal corta o círculo em dois pontos. No primeiro, o momento final é igual ao inicial: nada mudou, os corpos nem se tocaram. No segundo, é a colisão frontal, com a fórmula do vídeo passado. O caso de uma dimensão estava escondido nesses dois pontos.

### C08-2 — tela: semirreta tracejada saindo da origem com o ângulo de saída crescendo; DOIS JEITOS DE BATER, O MESMO DESVIO
> movimento: a semirreta gira o tempo todo da fala; os dois pontos e as duas setas acompanham.
Agora as direções oblíquas: uma semirreta saindo da origem, com um certo ângulo de saída. Onde ela corta o círculo, existe um momento final possível. Para ângulos pequenos, corta em dois pontos: dois jeitos de bater, o mesmo desvio. Um tira bastante momento do corpo um; o outro é de raspão.

### C08-3 — tela: o ângulo cresce; os dois pontos se fundem; TANGÊNCIA; depois SEM INTERSEÇÃO: SEM SOLUÇÃO FÍSICA
> movimento: a semirreta continua girando até a tangente (~3 s) e passa para vinte graus; o anel pisca no ponto único; a mensagem troca na hora certa.
Aumentando o ângulo, os dois pontos se aproximam até virar um só: a tangência. Passou disso, a semirreta não toca o círculo, e sem interseção não existe solução. A natureza fechou a porta.

### C08-4 — tela: as duas tangentes e o cone; o espaço físico em miniatura; a direção real do hook (dez vírgula nove graus), a de vinte e cinco e a de quarenta; ⚠ X nas duas proibidas
> movimento: as tangentes se desenham; o cone aparece; as três direções entram uma de cada vez com o rótulo; os dois X pulsam.
Voltando ao disco pesado do começo: as duas tangentes formam um cone. A colisão real, a dez vírgula nove graus, está dentro. Vinte e cinco graus e quarenta graus ficam fora, os dois proibidos. O segurança da porta não deixa passar.

### C08-5 — tela: AGORA SABEMOS POR QUÊ.
> movimento: a frase entra e a linha de quarenta graus pulsa.
Era essa a pergunta do começo, e o círculo respondeu: a geometria do momento só deixa passar algumas direções.

## C09 — O ÂNGULO MÁXIMO

### C09-1 — tela: plano com o deslizador da razão das massas (zero vírgula cinco); triângulo retângulo da tangente (tangente, raio, marca de ângulo reto, hipotenusa, ângulo máximo)
> movimento: o triângulo se desenha em partes (tangente, raio, marca, ⚠ hipotenusa destacada do eixo); cada parte pisca quando citada.
Agora um número: qual é o maior desvio possível? Olha a tangente. O raio até o ponto de tangência é perpendicular a ela. Então temos um triângulo retângulo: a hipotenusa vai da origem ao centro, o cateto oposto é o raio, e o ângulo na origem é o ângulo máximo.

### C09-2 — tela: sen θ_max = R/C = λ; θ_max = arcsen(m₂/m₁); caixa dupla
> movimento: a fração se desenha; o cateto e a hipotenusa piscam; os valores cancelam (Indicate); o lambda se desdobra em m₂/m₁.
Seno é cateto oposto sobre hipotenusa: o raio sobre a distância até o centro. Substituindo, quase tudo cancela e sobra só a razão das massas. Então o ângulo máximo é o arco seno da razão das massas: massa do corpo dois sobre a do corpo um. Que coisa linda.

### C09-3 — tela: TRADUÇÃO ALGÉBRICA: Δ ≥ 0 ⇔ cos²θ ≥ 1 − λ² ⇔ sen θ ≤ λ
> movimento: as três linhas entram em sequência; o cone do plano pisca em "cone".
E a álgebra concorda: para a equação do segundo grau ter solução, o discriminante precisa ser maior ou igual a zero, e isso dá exatamente seno do ângulo menor ou igual à razão das massas. Dois caminhos independentes, o mesmo resultado: sinal de que a gente acertou.

### C09-4 — tela: o deslizador anda: a razão cai para um quarto e sobe até zero vírgula oitenta e cinco; o círculo encolhe e cresce; o cone fecha e abre
> movimento: o deslizador percorre os dois trechos (~5 s) durante toda a fala; o ângulo máximo na leitura muda junto.
Mexendo na razão das massas: alvo mais leve, círculo menor, cone mais fechado. Alvo mais pesado, círculo maior, cone mais aberto.

### C09-5 — tela: razão igual a um; o círculo passa pela origem e a seta do momento inicial é um diâmetro; TEOREMA DE THALES
> movimento: o deslizador chega a um; ⚠ o diâmetro é traçado (tracejado) e as duas cordas, da origem e da ponta do diâmetro até o ponto, se desenham; o ângulo reto aparece no ponto.
Agora o caso especial: massas iguais, razão igual a um. O círculo passa pela origem, e o momento inicial vira um diâmetro. Aí entra um velho amigo, de mais de dois mil e quinhentos anos: o teorema de Tales. Pega um diâmetro e qualquer ponto da circunferência, liga às duas pontas... e o ângulo é sempre reto.

### C09-6 — tela: p⃗₁f ⊥ p⃗₂f; o ponto percorre o círculo (sessenta, cento e cinquenta, cento e oitenta graus); θ_max = 90°; p₁f = 0, RECUO FRONTAL
> movimento: o ponto anda sem parar durante a fala; o ângulo reto o acompanha; no fim, o vetor do corpo um encolhe até zero.
As pontas do diâmetro são a origem e a ponta do momento inicial; o ponto é o momento final do corpo um. Os dois lados que chegam nele são os momentos finais dos dois corpos, e portanto perpendiculares. É o ângulo reto da sinuca! Só que agora a gente sabe de onde ele vem. E quando o ponto chega na origem, o corpo um para e o alvo leva tudo: é a troca de velocidades da colisão frontal.

### C09-7 — tela: razão de um até dois; a origem fica dentro do círculo; QUALQUER DIREÇÃO ATÉ 180°; A INCIDENTE PODE VOLTAR; NÃO EXISTE ÂNGULO MÁXIMO MENOR QUE 180°
> movimento: o deslizador sobe até dois (~3 s); o ponto passa para a esquerda do eixo vertical; as três mensagens entram em sequência.
E se o alvo for mais pesado? A razão passa de um, e o círculo engole a origem: toda semirreta corta o círculo uma vez, em qualquer direção, até cento e oitenta graus. O corpo incidente pode voltar para trás. É a bolinha de pingue-pongue numa bola de boliche.

## C10 — ALFA CONTRA NÊUTRON

### C10-1 — tela: alfa (quatro vezes a massa do nêutron) e nêutron; a razão vale um quarto; cone, tangentes e θ_max = arcsen ¼ ≈ 14,5°
> movimento: os discos entram com a massa de cada um; o círculo respira; as tangentes crescem e o arco se desenha.
Um exemplo de física nuclear: uma partícula alfa, com quatro vezes a massa do nêutron, bate num nêutron parado. A razão das massas é um quarto, e o ângulo máximo é o arco seno de um quarto: uns catorze vírgula cinco graus. É um caminhão contra um fusquinha.

### C10-2 — tela: o ponto de tangência; p₁f/p₁ᵢ = cos θ_max/(1 + λ) = √15/5 ≈ 0,775; K₁f/K₁ᵢ = 60 %
> movimento: as duas setas crescem; o θ_max desce para dentro do cosseno (glifos); a fração entra no parêntese; o sessenta por cento surge no fim.
No ponto de tangência, o momento da alfa é raiz de quinze sobre cinco do inicial, uns zero vírgula setenta e sete. Como a energia vai com o quadrado do momento, a alfa fica com sessenta por cento da energia cinética.

### C10-3 — tela: barra de energia (alfa e nêutron); K_n,f = 0,40 K_α,i; θ₂ ≈ 37,8°; NA COLISÃO FRONTAL: 16/25 = 64 %
> movimento: a barra cresce em duas partes; o arco do nêutron se desenha; o sessenta vira quarenta (glifos); a frontal entra por último.
Os outros quarenta por cento vão para o nêutron, que sai a uns trinta e sete vírgula oito graus. Mas atenção: isso é no ângulo limite; não é a transferência máxima de energia. Essa acontece de frente, e vale dezesseis vinte e cinco avos: sessenta e quatro por cento.

## C11 — ACIDENTE EM 2D

### C11-1 — tela: cruzamento (pista cinza-azulada neutra); caminhão em aço claro vindo do sul e carro em aço escuro vindo do oeste, vistos de cima; enunciado e rótulos de massa e velocidade (as cores ficam só para os vetores)
> movimento: os veículos se aproximam devagar durante toda a leitura; cada rótulo aparece quando a voz o cita.
Hora de um problema com cara de prova. Um caminhão de três mil quilogramas, indo para o norte a sessenta quilômetros por hora, bate num carro de mil quilogramas, indo para o leste a noventa. Eles ficam presos e derrapam, com coeficiente de atrito cinético zero vírgula cinco. Quer saber a velocidade logo depois do choque e quanto eles derrapam.

### C11-2 — tela: choque; P⃗ᵢ = P⃗_f se abre nas componentes leste (m · 25 = (M + m) v_fx) e norte (M · 50/3 = (M + m) v_fy)
> movimento: choque em câmera lenta; os veículos presos andam juntos enquanto a equação se divide em duas linhas (glifos); a componente citada pisca.
Durante o choque, o momento, que é vetorial, se conserva; a energia cinética não, porque os dois ficam presos. Escreve o momento em duas componentes: para o leste, só o carro tem momento; para o norte, só o caminhão. Cada uma é igual à massa total vezes a componente da velocidade final.

### C11-3 — tela: v_fx = 6,25 m/s; v_fy = 12,5 m/s; tg θ = 2; θ ≈ 63,4°; |v⃗_f| ≈ 13,98 m/s; o arco do ângulo a partir do leste
> movimento: as contas viram números (glifos); as duas componentes entram na fração; o dois vira o ângulo; a seta do conjunto pulsa devagar.
Resolvendo: seis vírgula vinte e cinco metros por segundo para o leste, e doze vírgula cinco para o norte. A tangente do ângulo é dois: sessenta e três vírgula quatro graus a partir do leste. O módulo é quase catorze metros por segundo. O vetor aponta mais para o norte: o caminhão é mais pesado e puxa o conjunto.

### C11-4 — tela: O MOMENTO VALE SEM CONSERVAR K; barra de energia (ciano e laranja)
> movimento: as duas barras crescem; o laranja pisca quando a voz diz "virou".
E a energia? Quase metade da energia cinética virou lataria amassada e calor.

### C11-5 — tela: IMPACTO: MOMENTO / DEPOIS: TRABALHO–ENERGIA; ½ (M + m) v_f² = μ_k (M + m) g d vira d = v_f²/(2 μ_k g) ≈ 19,5 m; o conjunto derrapa e a cota aparece; COMO NO PÊNDULO: SEPARE OS PROCESSOS
> movimento: o conjunto derrapa até parar; a equação se transforma (o meio vira o dois do denominador, os dois fatores de massa se anulam); a cota se desenha.
Agora a colisão acabou, e começou outro processo: a derrapagem. Mudou o processo, muda o princípio: no impacto, momento; depois, trabalho e energia. A energia cinética que sobrou é gasta pelo atrito, e a massa total cancela. A distância é a velocidade ao quadrado, dividida por duas vezes o atrito vezes a gravidade: uns dezenove vírgula cinco metros. Como no pêndulo do vídeo passado: separa os processos.

## C12 — EXPLOSÕES

### C12-1 — tela: um corpo parado; flash; três fragmentos com setas de momento; Σ p⃗ₖ = 0⃗ vira p⃗₁ + p⃗₂ + p⃗₃ = 0⃗ (triângulo fechado); barras de energia: K_i = 0 → K_f > 0
> movimento: explosão com onda; o triângulo é desenhado vetor por vetor, ponta com cauda; a barra laranja encolhe enquanto a ciano cresce; a linha do total fica fixa.
Agora, o contrário de uma colisão: uma explosão. O corpo estava parado, com momento total zero; como o impulso externo é desprezível, os três pedaços saem com momentos que somam zero, formando um triângulo fechado. A energia cinética vai de zero para positiva: a energia interna vira cinética, sem criar energia nenhuma.

## C13 — MÉTODO E SÍNTESE

### C13-1 — tela: cinco cartões (SISTEMA?, IMPULSO EXTERNO DESPREZÍVEL?, QUANTAS DIMENSÕES?, TIPO DE EVENTO?, NOVA ETAPA DEPOIS?) com o marcador percorrendo
> movimento: os cartões entram em cascata; o marcador desce de cartão em cartão com a voz; cada conteúdo entra junto da palavra.
O método, em cinco passos. Um: qual é o sistema? Dois: o impulso externo é desprezível? Três: quantas dimensões? Em duas, duas componentes mais a geometria. Quatro: qual é o tipo de evento? Elástica, grudou, explosão ou outro. Cinco: começou outro processo depois? Então separa os processos.

### C13-2 — tela: O QUE MUDOU DO 1D PARA O 2D?; as linhas de resposta; faixa SISTEMA → P⃗ → GEOMETRIA → TIPO DE COLISÃO → NOVA ETAPA; 1D = MOMENTO + TIPO; 2D = MOMENTO + GEOMETRIA + TIPO
> movimento: o título pulsa; cada linha entra em FadeIn; a faixa e as fórmulas de bolso entram por último; "geometria" brilha uma vez.
E a pergunta do começo: o que mudou de uma para duas dimensões? A conservação do momento não mudou: ele sempre foi um vetor. Em uma dimensão, a geometria ficava escondida na linha; em duas, ela aparece e decide quais finais são possíveis. Momento mais tipo de colisão virou momento, mais geometria, mais tipo de colisão.

## C14 — GANCHO (texto do Kaio, sem cortes; o "Até a próxima!" fica para o encerramento)

### C14-1 — tela: um disco em aço e um projétil pequeno
> movimento: o projétil já se aproxima do disco; a vinheta respira.
Até aqui, a gente tratou os corpos como partículas. Isso significa que, para descrever a colisão, bastavam a massa, a velocidade e a direção do movimento. Mas corpos reais têm tamanho.

### C14-2 — tela: primeiro caso: o impacto no centro; o disco só translada; seta do impulso
> movimento: o projétil acelera até o contato; flash; o disco desliza com a seta de velocidade do centro.
Agora imagina duas colisões com o mesmo impulso. Na primeira, o impacto acontece bem no centro do corpo. Nesse caso, o corpo pode simplesmente mudar o seu movimento de translação.

### C14-3 — tela: reset; segundo caso: o impacto fora do centro; o disco translada e gira
> movimento: o disco volta devagar; o projétil entra deslocado; o disco desliza e gira (marca radial e arco branco).
Na segunda, o impacto acontece deslocado para um dos lados. Aí, além de se mover, o corpo pode começar a girar.

### C14-4 — tela: a linha de ação e a distância até o centro; POR QUE O PONTO ONDE A FORÇA AGE IMPORTA?
> movimento: as linhas tracejadas se desenham; a chave e a distância aparecem; a pergunta entra.
E aí aparece uma pergunta nova: por que a mesma força pode produzir efeitos completamente diferentes, dependendo de onde ela é aplicada?

### C14-5 — tela: PRÓXIMO VÍDEO: POR QUE UMA FORÇA FAZ UM CORPO GIRAR? TORQUE E DINÂMICA DE ROTAÇÃO
> movimento: os três textos entram em sequência; o disco continua girando.
É justamente essa pergunta que leva ao conceito de torque. No próximo vídeo, a gente vai entender por que uma força faz um corpo girar, e como o ponto de aplicação muda completamente o resultado.

## ENCERRAMENTO

### E1 — tela: tudo sai; logo com anéis violeta; INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
> movimento: os anéis giram em sentidos alternados o tempo todo; a logo entra com escala.
Hoje a gente usou momento, geometria e tipo de colisão para descobrir para onde os corpos podem sair, e para onde eles não podem. Se isso ajudou você, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### E2 — tela: PRÓXIMO VÍDEO: TORQUE E DINÂMICA DE ROTAÇÃO; disco com marca girando; ondas
> movimento: o disco gira e as ondas se abrem continuamente.
E fica a pergunta: por que uma força faz um corpo girar? Me conta nos comentários: o que mais te surpreendeu, o ângulo reto da sinuca ou a direção proibida? Valeu demais por assistir, e até a próxima!

---

## Orçamento de tempo (v1.2: fala × animação de hoje)

Estimativa: 2,8 palavras por segundo + 0,25 s por âncora (a voz real fica entre 2,7 e 3,0).

| Cena | Âncoras | Palavras | Meta do corte | Fala ≈ | Animação hoje | Esticar × |
|---|---:|---:|---:|---:|---:|---:|
| Hook | 3 | 71 | 80 | 26 s | 12,9 s | 2,0 |
| Abertura | 2 | 53 | 53 | 19 s | 6,7 s | 2,9 |
| C01 | 2 | 99 | 55 | 36 s | 11,9 s | 3,0 |
| C02 | 4 | 165 | 130 | 60 s | 23,7 s | 2,5 |
| C03 | 3 | 146 | 130 | 53 s | 29,5 s | 1,8 |
| C04 | 8 | 228 | 240 | 83 s | 44,0 s | 1,9 |
| C05 | 3 | 113 | 100 | 41 s | 22,9 s | 1,8 |
| C06 | 4 | 183 | 170 | 66 s | 31,1 s | 2,1 |
| C07 | 6 | 311 | 300 | 113 s | 45,2 s | 2,5 |
| C08 | 5 | 188 | 215 | 68 s | 36,9 s | 1,9 |
| C09 | 7 | 351 | 300 | 127 s | 49,7 s | 2,6 |
| C10 | 3 | 138 | 175 | 50 s | 24,7 s | 2,0 |
| C11 | 5 | 251 | 190 | 91 s | 47,7 s | 1,9 |
| C12 | 1 | 52 | 60 | 19 s | 20,7 s | 0,9 |
| C13 | 2 | 103 | 90 | 37 s | 37,5 s | 1,0 |
| C14 (gancho) | 5 | 139 | 139 | 51 s | 30,6 s | 1,7 |
| Encerramento | 2 | 76 | 60 | 28 s | 14,2 s | 1,9 |
| **Total** | **65** | **2.667** | **2.487** | **≈ 16,1 min** (≈ 14,8 min a 3,0 p/s; ≈ 17,1 min a 2,6 p/s) | 8,2 min | 2,0 |

Fiquei **180 palavras acima do orçamento** (2.667 contra 2.487), de propósito, onde você disse que ficou corrido: C09 (+51, a tangente e o Tales),
C11 (+61, o enunciado e a derrapagem), C01 (+44, a retomada obrigatória: este vídeo continua o anterior e o tipo de colisão dá a condição
que falta), C07 (+11, o quadrado perfeito explicado), C03 (+16) e C02 (+35). Cortei abaixo da meta em C04 (−12), C08 (−27) e C10 (−37).
**Ritmo real:** a 2,8 palavras por segundo dá ~16,1 min; com pausas, a voz em português costuma ficar em 2,5 a 2,7, o que dá ~16,5 a 17,5 min.
Por isso vale um **teste de ritmo** (~100 palavras do C07-2, o trecho mais denso) antes de aprovar o texto: ver `narracao_teste_c07.md`.
Se precisar cortar, o C12 vira uma frase no C13 (−35 palavras) e depois o C10-3 (a frase da frontal). Se quiser voltar a ~20 min, os trechos
para devolver são: a leitura dos termos no C06-4, o C09-4 (deslizador) e o C11-3 (valores falados um a um).

Estiramento médio da animação: **2,0×** (de 8,2 para ~16 min), contra 3,6× na v1.1. C12 e C13 não precisam esticar; C09, C07, C02 e C01
são os que mais pedem retiming.

## Revisão de física (v1.2, todas as cenas)

Conferi também C05, C06, C11, C12 e C13, que o plano de corte ainda não tinha lido:
- **C05:** 10 cos 30° = 5√3 ≈ 8,66; 10 sen 30° = 5; (5√3)² + 5² = 100 = 10²; momento nos dois eixos fecha (7,5 + 2,5 = 10; 4,33 − 4,33 = 0).
- **C06:** p₂f = p₁ᵢ − p₁f; lei dos cossenos com o ângulo de saída; energia p²/2m; multiplicar por 2m₂ dá p₂f² = λ(p₁ᵢ² − p₁f²); igualando:
  (1+λ)p₁f² − 2p₁ᵢ cosθ₁ p₁f + (1−λ)p₁ᵢ² = 0. Sem erro.
- **C11:** 90 km/h = 25 m/s; 60 km/h = 50/3 m/s; v_fx = 1000·25/4000 = 6,25; v_fy = 3000·(50/3)/4000 = 12,5; tg θ = 2 → 63,4°; |v⃗_f| = 13,98 m/s;
  K_i = 729 kJ, K_f = 391 kJ (perda de 46 %, "quase metade"); d = v_f²/(2μg) = 195,3/10 = 19,5 m.
- **C12:** três momentos que somam zero formam triângulo fechado; K_i = 0 → K_f > 0 com a energia total constante (interna → cinética). Sem erro.
- **C13:** método e a resposta ao hook consistentes com a ficha.
- Também revisei a v1.1 em C04 e C07 a C10, sem erro. O X nos **dois** ângulos do hook (25° e 40°) entrou nesta versão (H2 e C08-4).

## Como manter a cena sempre em movimento (kit para a sincronia)

Toda âncora precisa de pelo menos um destes, ligado à palavra que o cita (atraso máximo 0,2 s):
1. **Destaque que caminha:** caixa fina (`SurroundingRectangle`) passando de termo em termo, na ordem em que a voz fala.
2. **Pulso no termo ou na seta citada** (`Indicate`), com o resto atenuado (opacidade ~0,4) enquanto o citado fica aceso.
3. **Variáveis lentas:** o ângulo da semirreta (C08), o deslizador da razão das massas (C09), o ponto no círculo (C07, C09), o corpo derrapando (C11).
4. **Respiração** (escala 1,00 ↔ 1,02) nas setas de momento e no círculo, para nenhuma figura ficar congelada.
5. **Revelação por glifos com `run_time` esticado até o fim da frase;** o passo anterior só recua para o fantasma quando a voz termina o passo.
6. Construções de geometria com `Create` mais lento (1,2 a 2 s): tangente, raio, triângulo, diâmetro.

## Coisas novas a criar na cena (⚠)

1. X nas **duas** direções do hook (25° e 40°): H2 e C08-4.
2. C09-1: destacar o trecho do eixo da origem até o centro (a hipotenusa do triângulo da tangente).
3. C09-5/6: desenhar o diâmetro (tracejado) e as duas cordas até o ponto; a marca de ângulo reto acompanha o ponto durante o passeio (Tales).
4. O resto é retiming e destaques sobre o que já existe. O resumo C09-9 saiu, então não há cena nova a criar ali.

## Para a fase de voz (depois da aprovação do texto v1.2)

- Tags (uma por trecho): `[curious]` no hook e nas perguntas; `[happy]` no bem-vindos; `[thoughtful]` na explicação; `[thoughtful, emphatic]` em conceitos-chave
  (equação-mãe do C02, ângulo reto do C04, completar o quadrado, Tales, método do C13); `[excited]` só em dois pontos: o ângulo reto da sinuca (C09-6) e
  "agora sabemos por quê" (C08-5); `[calm, satisfied]` no encerramento. Sem `[slowly]`. Pausa: `[short pause]` ou reticências.
- Conferir pronúncia: "lambda", "Tales", "arco seno", "nêutron", "cosseno".
- Sincronia: gerar a voz, extrair o tempo de cada âncora (ASR), travar `an(n, k)` no `cena.py`, medir o atraso de cada âncora com script
  (meta ≤ 0,2 s, como no `conferir_sync.py` do yt_0013). **Só gerar a voz depois da sua confirmação** (gasta crédito).
