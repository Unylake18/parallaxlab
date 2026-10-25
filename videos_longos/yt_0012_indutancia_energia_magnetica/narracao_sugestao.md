# yt_0012 — Sugestão de narração v1 (com audio tags do Eleven v4)

Base: handoff de Produção (C01–C20, cinco payoffs) + varredura quadro a quadro do preview V3 (844 s, um quadro a cada 3,5 s).
Estilo: `docs/roteiro_voz_elevenlabs_v4.md` e `docs/padrao_video_longo.md` §5 — professor de cursinho, "a gente", conectivos,
variável sempre pelo nome (nunca a letra solta), hipóteses ditas uma vez, fechamento na pergunta do gancho, CTA com a prévia.
A fala manda: cada cena se estica para caber nela (âncoras na sincronia). Linhas `> tela:` são a âncora visual da frase seguinte
e **não são faladas**. As tags `[ ]` não entram na legenda.

Status: **sugestão para revisão**. Não gerar voz antes da aprovação do texto.

---

## C01 — A previsão que falha (gancho)

> tela: circuito aparece; índice ℰ₀ / R / I

[curious] Olha esse circuito. Uma bateria, uma chave, uma bobina comprida, que a gente chama de solenoide, e um resistor. Tudo em série, um atrás do outro.

> tela: "CHAVE ABERTA: NENHUMA CORRENTE", cartão I = 0

[thoughtful] Com a chave aberta, não passa nada. A corrente é zero.

> tela: "A PREVISÃO INGÊNUA: UM SALTO", I = ℰ₀/R e o degrau tracejado no gráfico

[curious] Agora me diz: se eu fechar a chave, o que acontece? A resposta de primeira é a lei de Ohm: a corrente vira, na hora, a força eletromotriz da bateria dividida pela resistência. No gráfico, isso seria um degrau: zero num instante, valor máximo no instante seguinte.

> tela: "FECHAMOS A CHAVE" → "A CORRENTE CRESCE AOS POUCOS"; traços verdes começam a correr

[short pause] Então vamos fechar.

[surprised] Só que a corrente não pula. Ela começa em zero e vai subindo aos poucos, numa curva suave, até encostar no valor que a gente esperava. Esse valor de chegada eu vou chamar de corrente final.

> tela: "O CAMPO B CRESCE JUNTO" — o magenta acende dentro do solenoide

[thoughtful] E repara no solenoide: o campo magnético lá dentro, aqui em magenta, também começa em zero e cresce junto com a corrente. Os dois andam de mãos dadas.

> tela: "DEVERIA SALTAR. MAS NÃO SALTA."

[curious] Ou seja: pela lei de Ohm, a corrente deveria saltar. Mas não salta. Alguém nesse circuito está segurando a corrente. Quem?

## C02 — Bem-vindos e promessa

> tela: logo + "BEM-VINDOS AO PARALLAX LAB"

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

> tela: "POR QUE A CORRENTE RESISTE A MUDAR?" + "NESTE VÍDEO"

[thoughtful] No vídeo passado, a gente viu que um campo magnético que varia no tempo cria uma força eletromotriz. Hoje a pergunta é: e quando quem cria esse campo é a própria corrente do circuito? A gente vai descobrir por que a corrente resiste a mudar, de onde vem essa resistência, e uma coisa ainda mais bonita: onde fica guardada a energia que a bateria gasta para montar o campo. Spoiler: não é no fio.

## C03 — Indução mútua

> tela: "UMA SEGUNDA BOBINA, EM VOLTA DO SOLENOIDE" → "COM UM MEDIDOR"; índice I₁ / N₂ / ℰ₂

[thoughtful] Para entender o que segura a corrente, vamos dar um passo para trás e usar duas bobinas. Em volta do solenoide eu enrolo uma segunda bobina, a bobina dois, com um medidor ligado nela. Ela não encosta no circuito: está só abraçando o solenoide por fora.

Daqui pra frente, a corrente no solenoide vai ser a corrente um, o número de voltas da bobina dois é o número de espiras da bobina dois, e o que o medidor lê é a força eletromotriz induzida na bobina dois.

> tela: "A CORRENTE I₁ MUDA..." → "...O CAMPO B₁ CRESCE..." → "...ATRAVESSA A BOBINA 2..." → "...E SURGE UMA FEM ℰ₂"

[curious] Agora olha a sequência, que ela é uma corrente de causa e efeito. A corrente um começa a mudar... o campo magnético do solenoide cresce... esse campo atravessa as espiras da bobina dois... e o ponteiro do medidor se mexe. Apareceu força eletromotriz na bobina dois.

> tela: cadeia I₁ → B₁ → Λ₂ → ℰ₂; índice "fluxo concatenado pela bobina 2"

[thoughtful] No cartão está a cadeia inteira. O elo do meio tem um nome: o fluxo concatenado pela bobina dois. É o fluxo magnético em uma espira, somado em todas as espiras da bobina. Se a bobina tem cem voltas, o mesmo campo é contado cem vezes.

> tela: "CORRENTE CONSTANTE: PONTEIRO NO ZERO"

[curious] E quando a corrente um para de crescer e fica constante? O campo continua lá, atravessando a bobina dois... mas o ponteiro volta para o zero.

> tela: "SÓ HÁ FEM ENQUANTO I₁ MUDA"; Λ₂ = M I₁

[thoughtful, emphatic] Guarda isso: a bobina dois não reage ao campo. Ela reage à mudança do campo. Lembrando Faraday: força eletromotriz é menos a taxa de variação do fluxo.

Como o fluxo concatenado é proporcional à corrente um, a gente escreve: fluxo concatenado igual à indutância mútua vezes a corrente um. A indutância mútua é só a constante de proporcionalidade, e na tela ela aparece como a letra M.

> tela: "INDUÇÃO MÚTUA" — ℰ₂ = −M dI₁/dt

[thoughtful] Derivando no tempo, sai a lei da indução mútua: a força eletromotriz na bobina dois é menos a indutância mútua vezes a taxa de variação da corrente um.

> tela: "DE ONDE VEM M?" → Λ₂ = N₂ B₁ A; "SÓ A ÁREA DO SOLENOIDE CONTA"

[curious] Tá, mas de onde vem esse número? Vamos calcular. O fluxo concatenado é o número de espiras da bobina dois, vezes o campo do solenoide, vezes uma área. E aqui tem uma pegadinha boa: qual área? A da bobina dois é maior... só que, num solenoide longo, o campo magnético só existe dentro dele. Fora, é praticamente zero. Então a única área que conta é a área da seção do solenoide.

> tela: B₁ = μ₀ n I₁ → Λ₂ = N₂ μ₀ n I₁ A; "M SÓ DEPENDE DA GEOMETRIA"; índice n

[thoughtful] O campo dentro do solenoide é a permeabilidade do vácuo, vezes o número de espiras por metro, vezes a corrente um. Substituindo, a corrente um aparece multiplicando tudo... e o que sobra na frente dela é a indutância mútua: permeabilidade do vácuo, vezes espiras por metro do solenoide, vezes o número de espiras da bobina dois, vezes a área da seção.

[thoughtful, emphatic] Repara que não sobrou corrente nem tempo nessa expressão. A indutância mútua só depende da geometria: de como as bobinas são enroladas e de como uma abraça a outra.

## C04 — Reciprocidade

> tela: "TROCANDO OS PAPÉIS DAS BOBINAS" → "A BOBINA 2 VIRA A FONTE"; medidor vira FONTE

[curious] Agora vamos inverter o jogo. A bateria sai de cena, e quem recebe uma fonte é a bobina dois. A corrente dela, a corrente dois, passa a variar.

> tela: "A FEM APARECE NO SOLENOIDE"; ℰ₁ e a seta ciano no solenoide

[thoughtful] E agora é o solenoide que sente uma força eletromotriz. Mesma geometria, papéis trocados.

> tela: "O MESMO M NOS DOIS SENTIDOS" — cartão RECIPROCIDADE M₁₂ = M₂₁

[thoughtful] E aqui vem um resultado elegante: o coeficiente que liga um ao outro é exatamente o mesmo nos dois sentidos. A indutância mútua da bobina um na dois é igual à da bobina dois na um. Não vou provar agora, mas guarda: é uma propriedade da geometria, não de quem está mandando corrente.

> tela: "E SE O SEGUNDO CIRCUITO DESAPARECER?"

[curious] Só que isso levanta uma pergunta curiosa. A bobina dois sentia o fluxo do solenoide... mas o próprio solenoide também está mergulhado no campo que ele mesmo cria. E se o segundo circuito desaparecer?

## C05 — A mútua vira autoindução

> tela: "SEM A BOBINA 2, O CAMPO CONTINUA" — a bobina 2 some, Λ₂ = M I₁ fica

[thoughtful] Vamos tirar a bobina dois. O campo magnético continua ali, do mesmo jeito.

> tela: "O FLUXO ATRAVESSA AS PRÓPRIAS ESPIRAS" — Λ₂ = M I₁ vira Λ = L I

[curious] E esse campo atravessa quem? As próprias espiras do solenoide! O solenoide concatena o próprio fluxo. Então a mesma ideia vale aqui: o fluxo concatenado pelo próprio solenoide é proporcional à corrente dele. A constante agora se chama autoindutância. Na tela, ela aparece como L. A unidade dela é o henry.

> tela: "FEM AUTOINDUZIDA" — ℰ_L = −L dI/dt

[thoughtful, emphatic] E se a corrente muda, o fluxo muda... e o solenoide induz uma força eletromotriz nele mesmo: a força eletromotriz autoinduzida é menos a autoindutância vezes a taxa de variação da corrente. É o nosso primeiro grande resultado.

> tela: "SETA CIANO: O SENTIDO DA FEM"

[thoughtful] A seta ciano em cima do solenoide mostra para que lado essa força eletromotriz empurra as cargas. O mais fica na ponta da seta, o menos fica na cauda. Fica de olho nela, que agora ela vai trabalhar.

## C06 — O que o indutor realmente combate

> tela: "O QUE O INDUTOR REALMENTE COMBATE" → solenoide sozinho; "CORRENTE IMPOSTA: SOBE, PARA, DESCE"

[curious] Para ver o sinal de menos em ação, vamos isolar o solenoide e impor uma corrente nele. A gente controla: primeiro ela sobe, depois fica parada, depois desce. Do lado, o gráfico da corrente, com uma reta tangente mostrando a inclinação a cada instante.

> tela: "CORRENTE AUMENTANDO: FEM CONTRA"

[thoughtful] Primeiro, a corrente aumentando. A inclinação é positiva... e a seta ciano aponta contra a corrente. O solenoide tenta segurar o aumento.

> tela: topo do gráfico, tangente horizontal, seta encolhe

[thoughtful] No topo, a corrente para de mudar: a tangente fica deitada, e a seta some.

> tela: "CORRENTE DIMINUINDO: FEM A FAVOR"

[curious] E agora a corrente diminuindo. A inclinação ficou negativa... e a seta virou: ela empurra a favor da corrente. O solenoide tenta segurar a queda.

[happy] O indutor é aquele amigo do contra. Você quer acelerar, ele segura. Você quer frear, ele empurra.

> tela: "O INDUTOR NÃO SE OPÕE À CORRENTE." → "ELE SE OPÕE À MUDANÇA DA CORRENTE."

[thoughtful, emphatic] Então presta atenção na frase, porque é a frase mais importante do vídeo até aqui. O indutor não se opõe à corrente. [short pause] Ele se opõe à mudança da corrente.

> tela: "E COM CORRENTE CONSTANTE?" — I ≠ 0, dI/dt = 0 ⇒ ℰ_L = 0

[curious] E com corrente constante? Tem corrente, tem campo magnético... mas a taxa de variação da corrente é zero. Logo, a força eletromotriz autoinduzida também é zero. Corrente parada, indutor quietinho. Para a corrente contínua estável, o solenoide é só um pedaço de fio.

## C07 — A equação do circuito

> tela: "DE VOLTA AO CIRCUITO: A LEI DAS MALHAS" → "UMA VOLTA NA MALHA"

[thoughtful] Agora a gente volta ao circuito do começo, com a bateria e o resistor. Para descobrir como a corrente cresce, vamos dar uma volta completa na malha somando as tensões. Lei das malhas: deu a volta, a soma tem que fechar em zero. Uma hipótese: toda a resistência do circuito está no resistor, os fios são ideais.

> tela: "A BATERIA: +ℰ₀"

[thoughtful] Primeiro, a bateria: ela eleva o potencial pela força eletromotriz da bateria. Sinal positivo.

> tela: "O INDUTOR: −L dI/dt"

[thoughtful] Depois, o indutor. Enquanto a corrente cresce, a seta dele está contra, então ele entra com menos a autoindutância vezes a taxa de variação da corrente.

> tela: "O RESISTOR: −RI"

[thoughtful] Por fim, o resistor: queda de resistência vezes corrente. Sinal negativo.

> tela: "A SOMA FECHA EM ZERO" — cartão LEI DAS MALHAS

[thoughtful] Somando os três, dá zero.

> tela: "ORGANIZANDO" → L dI/dt + RI = ℰ₀ (EQUAÇÃO DO CIRCUITO RL)

[thoughtful] Organizando, passando os termos com a corrente para um lado: autoindutância vezes a taxa de variação da corrente, mais resistência vezes corrente, igual à força eletromotriz da bateria. Essa é a equação do circuito RL. Cada termo é um componente: o primeiro é o indutor, o segundo é o resistor, o da direita é a bateria.

## C08 — Resolvendo a dinâmica

> tela: "DIVIDINDO POR L"

[curious] Vamos resolver. É uma equação diferencial, mas calma, que ela é das boazinhas. Primeiro, a gente isola a taxa de variação da corrente, dividindo tudo pela autoindutância.

> tela: "R/L EM EVIDÊNCIA"

[thoughtful] Depois coloca resistência sobre autoindutância em evidência. Dentro do parêntese aparecem duas coisas que merecem nome.

> tela: "DUAS COMBINAÇÕES GANHAM NOME" — I∞ = ℰ₀/R, τ = L/R; índice

[thoughtful] A força eletromotriz da bateria dividida pela resistência é a corrente final, aquela que a lei de Ohm previu. E a autoindutância dividida pela resistência tem unidade de tempo: é a constante de tempo do circuito. Guarda essa, que ela vai mandar em tudo.

> tela: "LONGE DO FINAL, MUDA DEPRESSA" — dI/dt = (I∞ − I)/τ

[thoughtful, emphatic] Com esses nomes, a equação fica linda: a taxa de variação da corrente é a distância até a corrente final, dividida pela constante de tempo. Lê em voz alta comigo: longe do final, a corrente muda depressa. Perto do final, ela quase não muda. É por isso que a curva vai deitando.

> tela: "SEPARANDO AS VARIÁVEIS"

[thoughtful] Agora o truque clássico: separar as variáveis. Tudo que tem corrente vai para um lado, tudo que tem tempo vai para o outro.

> tela: "INTEGRANDO DESDE I(0) = 0" → "AS DUAS INTEGRAIS"

[thoughtful] Integramos os dois lados: a corrente de zero até um valor qualquer, o tempo de zero até um instante qualquer. A condição inicial é a da chave recém-fechada: corrente zero no instante zero. A integral da esquerda dá um logaritmo, a da direita dá o tempo dividido pela constante de tempo.

> tela: "EXPONENCIANDO"

[thoughtful] Para tirar o logaritmo, exponenciamos: a fração da corrente que ainda falta é a exponencial de menos o tempo sobre a constante de tempo.

> tela: "ISOLANDO A CORRENTE" — cartão CORRENTE NA CARGA

[thoughtful, emphatic] E isolando a corrente, chegamos lá: a corrente é a corrente final vezes um menos a exponencial de menos o tempo sobre a constante de tempo. Confere com o que a gente viu no começo: começa em zero e tende à corrente final. A curva do gancho agora tem nome e sobrenome.

## C09 — Uma única escala de tempo controla tudo

> tela: "UMA ÚNICA ESCALA DE TEMPO CONTROLA TUDO" — gráfico zerado, seta ciano na bateria

[thoughtful] Agora vamos rodar a carga de novo, olhando tudo ao mesmo tempo: o circuito, o campo e o gráfico obedecem ao mesmo relógio.

> tela: "NO INÍCIO, |ℰ_L| = ℰ₀" — t = 0: I = 0, dI/dt = ℰ₀/L; tangente tracejada

[curious] No instante zero, a corrente é zero. Então o resistor não derruba nada, e a bateria inteira fica contra o indutor: a força eletromotriz autoinduzida tem o mesmo tamanho da força eletromotriz da bateria. É o momento em que a corrente sobe mais rápido: a taxa de variação inicial é a força eletromotriz da bateria dividida pela autoindutância. A reta tracejada mostra essa inclinação inicial. Repara onde ela chega na corrente final: exatamente em uma constante de tempo.

> tela: "EM t = τ: 63% DO VALOR FINAL"

[thoughtful] E depois de uma constante de tempo? É só trocar o tempo pela constante de tempo na fórmula: sobra um menos a exponencial de menos um, vezes a corrente final. Isso dá mais ou menos sessenta e três por cento da corrente final. Esse sessenta e três por cento cai em prova, viu? Anota aí.

> tela: "REGIME: A FEM SOME" — t ≫ τ

[thoughtful] Depois de umas cinco constantes de tempo, na prática, acabou: a corrente chegou na corrente final, a taxa de variação vai a zero, e a força eletromotriz autoinduzida some. Repara que o campo magnético continua aceso. Ele parou de mudar, só isso.

## C10 — O campo magnético fica, o campo elétrico induzido some

> tela: "OLHANDO O SOLENOIDE DE FRENTE" → "GIRANDO O SOLENOIDE"; vista axial; índice B / a / r / E_φ

[curious] E onde está essa força eletromotriz, fisicamente? Vamos girar o solenoide e olhar de frente, pelo eixo. Os pontinhos são o campo magnético saindo da tela. O raio do solenoide é o raio da bobina, e a distância ao eixo é o quanto a gente se afasta do centro.

> tela: B(t) = μ₀ n I(t)

[thoughtful] O campo magnético lá dentro acompanha a corrente: permeabilidade do vácuo, vezes espiras por metro, vezes a corrente naquele instante.

> tela: "SURGE UM CAMPO ELÉTRICO EM ANÉIS" — anéis ciano; r < a e r > a

[thoughtful] E enquanto a corrente muda, o campo magnético muda. E a gente aprendeu no vídeo passado: campo magnético variando vem acompanhado de campo elétrico induzido, em anéis. Dentro do solenoide, ele cresce com a distância ao eixo. Fora, ele cai com a distância. Esse é o campo que empurra as cargas nas espiras: a força eletromotriz autoinduzida é a volta inteira desse campo.

> tela: "LENZ: OS ANÉIS SE OPÕEM AO AUMENTO DE B"

[thoughtful] E o sinal de menos é a lei de Lenz: os anéis giram no sentido que se opõe ao aumento do campo magnético.

> tela: "B CONSTANTE: OS ANÉIS SOMEM" — regime: B ≠ 0, E_ind = 0

[thoughtful, emphatic] Com o tempo, a corrente estabiliza... o campo magnético fica constante... e os anéis somem. No regime, tem campo magnético, mas o campo elétrico induzido é zero. Campo magnético parado não empurra ninguém.

## C11 — Construir o campo custa energia

> tela: "CONSTRUIR O CAMPO CUSTA ENERGIA" — volta ao circuito

[curious] Agora vem a pergunta de energia. Montar esse campo magnético saiu de graça? Durante a subida, o indutor ficou empurrando contra a corrente. Empurrar contra quem passa custa trabalho. Então alguém pagou.

> tela: "A BATERIA ENTREGA POTÊNCIA" → "PARTE ESQUENTA O RESISTOR..." → "...PARTE VAI PARA O CAMPO"; três medidores

[thoughtful] Olha os três medidores. A bateria entrega potência. Uma parte esquenta o resistor: é a potência de Joule, em laranja. E a outra parte... vai para o campo, no medidor do meio. No índice: potência da fonte, potência dissipada no resistor, e potência que vai para o campo.

> tela: "MULTIPLICANDO A MALHA POR I"

[thoughtful] Vamos provar isso com a equação da malha. Truque: tensão vezes corrente é potência. Então multiplicamos a equação inteira pela corrente.

## C12 — A potência se divide

> tela: "O TERMO DO INDUTOR VAI PARA A DIREITA"

[thoughtful] Passamos o termo do indutor para a direita. Fica: força eletromotriz da bateria vezes corrente, igual a corrente ao quadrado vezes resistência, mais autoindutância vezes corrente vezes a taxa de variação da corrente.

> tela: "REGRA DA CADEIA"

[curious] E esse último termo esconde uma derivada. A regra da cadeia, nossa velha conhecida do cálculo: a derivada da corrente ao quadrado é duas vezes a corrente vezes a taxa de variação dela. Então autoindutância vezes corrente vezes a taxa de variação da corrente é a derivada, no tempo, de meio vezes autoindutância vezes corrente ao quadrado.

> tela: "CADA TERMO É UMA POTÊNCIA" — cartão BALANÇO DE POTÊNCIA

[thoughtful, emphatic] E agora cada termo é uma potência. A potência da fonte é igual à potência de Joule mais a taxa com que a energia do campo cresce. É o balanço de potência do circuito.

> tela: "A ENERGIA GUARDADA NO CAMPO" — U_B = ½ L I²

[excited] E a coisa que está sendo derivada tem nome: é a energia magnética. Meio vezes a autoindutância vezes a corrente ao quadrado. Essa é a energia guardada no campo magnético do indutor!

> tela: "NO INÍCIO, CAMPO; NO FIM, CALOR" — replay da carga com os medidores

[thoughtful] Repetindo a carga com os medidores: no comecinho, a corrente é pequena, quase nada esquenta, e quase toda a potência da bateria vai para o campo. Conforme a corrente cresce, o resistor vai pegando uma fatia maior. E no regime, o campo para de crescer e a bateria só alimenta o calor. No início, campo. No fim, calor.

## C13 — Onde está essa energia?

> tela: "ONDE ESTÁ ESSA ENERGIA?" → "NO FIO? NA BATERIA? OU NO CAMPO?" — o circuito some, fica o solenoide

[curious] Beleza, a energia está guardada. Mas guardada onde? No fio? Na bateria? Ou no próprio campo magnético, no espaço dentro do solenoide? A fórmula da energia magnética fala de autoindutância e corrente, que são propriedades do circuito... Mas olha o que acontece quando a gente reescreve tudo em termos do campo.

## C14 — Densidade de energia

> tela: "A SEÇÃO: ÁREA A" → "O COMPRIMENTO: ℓ" → "A SEÇÃO VARRE O VOLUME" (V = Aℓ)

[thoughtful] O solenoide tem uma seção, com uma área, e um comprimento. Se a gente arrasta a seção ao longo do comprimento, ela varre o volume interno: área vezes comprimento.

> tela: "NO SOLENOIDE: B = μ₀nI E L = μ₀n²Aℓ"; índice n, μ₀, A, ℓ

[thoughtful] Duas fórmulas do solenoide longo. O campo magnético: permeabilidade do vácuo, vezes espiras por metro, vezes a corrente. E a autoindutância: permeabilidade do vácuo, vezes espiras por metro ao quadrado, vezes a área, vezes o comprimento.

> tela: "TROCANDO L"

[thoughtful] Agora troca a autoindutância na energia magnética.

> tela: "APARECE O CAMPO B = μ₀nI"

[curious] Reagrupando, olha quem aparece: permeabilidade do vácuo, vezes espiras por metro, vezes corrente... é o próprio campo magnético! Ao quadrado, dividido por duas vezes a permeabilidade do vácuo, vezes área vezes comprimento.

> tela: "Aℓ É O VOLUME" → "ENERGIA POR VOLUME" → "A ENERGIA MORA NO CAMPO"; cartão DENSIDADE DE ENERGIA MAGNÉTICA

[thoughtful, emphatic] E área vezes comprimento é o volume. Então, dividindo a energia pelo volume, sobra a densidade de energia magnética: campo magnético ao quadrado, dividido por duas vezes a permeabilidade do vácuo. Sumiram o número de espiras, a área, o comprimento, a corrente. Sobrou só o campo. [short pause] A energia mora no campo.

## C15 — Generalização

> tela: "VALE PARA QUALQUER CAMPO" → "CAMPO REAL: NÃO UNIFORME"

[thoughtful] E isso vale para qualquer campo magnético, não só para o solenoide perfeito. Num solenoide de verdade, o campo não é uniforme: espalha nas pontas, enfraquece fora.

> tela: "CADA dτ GUARDA SUA PARTE" — dU_B = B²/2μ₀ dτ; índice elemento de volume

[thoughtful] Sem problema. A gente corta o espaço em pedacinhos de volume. Cada elemento de volume guarda a sua parte: a densidade ali, vezes o volume do pedacinho.

> tela: "SOMANDO TODOS OS PEDAÇOS" — U_B = 1/(2μ₀) ∫ B² dτ

[thoughtful] E somando todos os pedaços, a energia magnética total é a integral do campo ao quadrado em todo o espaço, dividida por duas vezes a permeabilidade do vácuo. Onde o campo é forte, tem muita energia. Onde ele é fraco, quase nada.

## C16 — Comutação para a descarga

> tela: "AGORA: TIRAR A BATERIA SEM ABRIR O CIRCUITO"

[curious] Agora a prova de fogo. Se a energia está mesmo no campo, ela tem que conseguir voltar sozinha. Vamos tirar a bateria.

> tela: "ABRIR A CHAVE? A CORRENTE NÃO PODE SALTAR" — U_B,0 = ½ L I₀²; índice I₀

[thoughtful] Mas cuidado: se eu simplesmente abrir a chave, eu estou pedindo para a corrente cair a zero num instante. E a gente já sabe: o indutor odeia mudança brusca. Ele responderia com uma força eletromotriz enorme, que vira faísca na chave. Não tenta isso em casa. No instante da troca, a corrente é a corrente inicial, e o campo guarda a energia inicial do campo: meio vezes autoindutância vezes a corrente inicial ao quadrado.

> tela: "UM CAMINHO SÓ PELO RESISTOR" → "A CHAVE VAI DE A PARA B"

[thoughtful] Então a gente cria um caminho alternativo: um ramo que fecha o circuito só pelo resistor. A chave passa da posição a para a posição b. A bateria sai, mas o circuito continua fechado.

> tela: "O INDUTOR SUSTENTA A CORRENTE"

[thoughtful] E repara: a corrente continua circulando, no mesmo sentido, sem salto nenhum.

## C17 — O indutor sustenta a corrente

> tela: "A MESMA MALHA, SEM BATERIA" — L dI/dt + RI = 0

[thoughtful] A equação é a mesma malha, só que sem a bateria: autoindutância vezes a taxa de variação da corrente, mais resistência vezes corrente, igual a zero. Mesma constante de tempo de antes.

> tela: cartão CORRENTE NA DESCARGA — I(t) = I₀ e^(−t/τ)

[thoughtful] A solução agora é ainda mais simples: a corrente é a corrente inicial vezes a exponencial de menos o tempo sobre a constante de tempo. Ela começa na corrente inicial e cai suavemente para zero.

> tela: "CORRENTE CAINDO: FEM A FAVOR" — a seta ciano vira

[curious] E olha a seta ciano. A corrente está caindo, então ela virou: agora empurra a favor da corrente. Lembra do amigo do contra? É ele de novo. É o indutor que está sustentando a corrente, sem bateria nenhuma. E o campo magnético vai apagando junto.

## C18 — O campo vira calor

> tela: "O CAMPO VIRA CALOR" — U_B(t) e P_R(t), split com gráficos

[thoughtful] Vamos acompanhar a energia. A energia do campo cai com o dobro da rapidez da corrente, porque depende da corrente ao quadrado: energia inicial do campo vezes a exponencial de menos duas vezes o tempo sobre a constante de tempo. E a potência no resistor cai do mesmo jeito: resistência vezes corrente inicial ao quadrado, vezes a mesma exponencial.

> tela: "O CAMPO PERDE, O RESISTOR RECEBE"

[thoughtful] O campo perde, o resistor recebe. Repara que as duas curvas descem juntas, no mesmo relógio.

> tela: "A ÁREA SOB P_R É O CALOR" — área laranja; Q_R(t) = ∫₀ᵗ P_R dt'

[thoughtful] E a potência é energia por tempo. Então a área embaixo da curva da potência no resistor é a energia que virou calor. O calor acumulado no resistor até um instante qualquer é essa área, a integral da potência no tempo.

## C19 — A conservação fecha

> tela: "O CALOR TOTAL" — E_calor = ∫₀^∞ I²R dt

[curious] E quanto calor sai no total, esperando até o fim? É a integral, de zero até infinito, da corrente ao quadrado vezes a resistência.

> tela: "SUBSTITUINDO A CORRENTE" → "A INTEGRAL VALE τ/2"

[thoughtful] Substituímos a corrente da descarga. A integral da exponencial de menos duas vezes o tempo sobre a constante de tempo, de zero a infinito, vale metade da constante de tempo. Fica: resistência vezes corrente inicial ao quadrado, vezes metade da constante de tempo.

> tela: "USANDO τ = L/R" → "O R CANCELA"

[thoughtful] Agora usamos que a constante de tempo é autoindutância sobre resistência... e olha que bonito: a resistência de cima cancela com a de baixo.

> tela: "R SÓ DECIDE O RITMO" — cartão TODA A ENERGIA DO CAMPO VIRA CALOR

[excited] Sobra meio vezes autoindutância vezes a corrente inicial ao quadrado. É exatamente a energia inicial do campo! Toda a energia que estava guardada no campo magnético apareceu como calor no resistor. Nem um joule a mais, nem um a menos.

[thoughtful] E a resistência sumiu do resultado, igual meia na máquina de lavar. Ela não decide quanto calor sai: isso quem decide é o campo. A resistência só decide o ritmo. Resistência grande, descarga rápida. Resistência pequena, descarga lenta. O total é o mesmo.

> tela: "A SOMA FICA CONSTANTE" — U_B(t) + Q_R(t) = U_B,0; curvas cruzadas

[thoughtful, emphatic] E dá para ver isso instante a instante. A energia do campo cai, o calor acumulado sobe, e a soma das duas fica sempre igual à energia inicial do campo. Uma curva cai, a outra cresce, e a soma não sai do lugar. Conservação de energia, desenhada.

## C20 — Síntese e o gancho de Maxwell

> tela: "SÍNTESE" → "O INDUTOR REAGE À MUDANÇA" — ℰ_L = −L dI/dt

[calm, satisfied] Então vamos juntar tudo. Primeiro: o indutor reage à mudança. A força eletromotriz autoinduzida é menos a autoindutância vezes a taxa de variação da corrente. É por isso que a corrente não salta.

> tela: "A ENERGIA FICA NO CAMPO" — U_B = ½ L I²

[calm, satisfied] Segundo: montar a corrente custa energia, e essa energia fica guardada: meio vezes autoindutância vezes corrente ao quadrado.

> tela: "DENSIDADE B²/2μ₀"

[calm, satisfied] Terceiro: ela está no campo, espalhada pelo espaço, com densidade igual ao campo magnético ao quadrado sobre duas vezes a permeabilidade do vácuo.

> tela: "E VOLTA INTEIRA COMO CALOR" — E_calor = U_B,0

[calm, satisfied] E quarto: sem a bateria, ela volta inteira, e vira calor no resistor.

[thoughtful] A pergunta inicial está respondida. A corrente não salta porque, para mudar a corrente, é preciso mudar o campo magnético, e mudar o campo custa energia, que não aparece de um instante para o outro. E essa energia mora no campo.

> tela: "E SE, NO LUGAR DO SOLENOIDE, HOUVER UM CAPACITOR?" — o solenoide vira capacitor

[curious] Agora, para terminar, uma provocação. E se, no lugar do solenoide, a gente colocasse um capacitor carregando?

> tela: "A CORRENTE CHEGA ÀS PLACAS..." → "...MAS NÃO ATRAVESSA"

[thoughtful] A corrente chega às placas... mas não atravessa. Entre as placas tem só um vão vazio. Nenhuma carga pula de uma placa para a outra.

> tela: "LEI DE AMPÈRE EM VOLTA DO FIO"; índice corrente que atravessa a superfície

[thoughtful] Agora pega a lei de Ampère: a circulação do campo magnético em volta de um anel é a permeabilidade do vácuo vezes a corrente que atravessa uma superfície apoiada nesse anel.

> tela: "DISCO S₁: O FIO ATRAVESSA"

[thoughtful] Se a superfície é um disco, o fio atravessa: a corrente que atravessa é a corrente do circuito.

> tela: "BOLSA S₂: NADA ATRAVESSA"

[curious] Mas eu posso escolher outra superfície com a mesma borda: uma bolsa, que passa por dentro do capacitor, no meio das placas. Por ali não passa fio nenhum. A corrente que atravessa é zero.

> tela: "O MESMO ANEL, DUAS RESPOSTAS"

[curious] O mesmo anel, duas respostas diferentes. Alguma coisa está faltando na lei de Ampère.

> tela: "COMO O CAMPO MAGNÉTICO SABE QUE O CIRCUITO CONTINUA?"

[curious] Então fica a pergunta: como o campo magnético sabe que o circuito continua do outro lado do capacitor? [short pause] Deixa nos comentários o seu palpite.

> tela: logo, anéis, "INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS" + prévia

[calm, satisfied] Se essas conexões ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos. No próximo, a gente vai atrás dessa peça que falta: a corrente de deslocamento, o ajuste que Maxwell fez na lei de Ampère. Valeu, pessoal. Até a próxima!
