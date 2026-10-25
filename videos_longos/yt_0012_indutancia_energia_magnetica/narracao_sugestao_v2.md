# yt_0012 — Sugestão de narração v2 (conteúdo revisado pelo GPT + revisão de TTS)

Base: v2 de conteúdo do GPT (a partir da `narracao_sugestao.md` v1). A física e o texto são os dele; aqui só entrou a revisão de TTS:
- "equação do circuito RL" → "equação do circuito com resistor e indutor" (regra dos longos: nunca letra solta; "RL" seria soletrado);
- aspas curvas tiradas do "dentro do fio" (o TTS pode ler a pontuação de forma estranha);
- `[short pause]` mantido só nos três pontos de virada (C01, C06, C14) e no palpite do C20;
- tags: uma por trecho de tela; `[excited]` só em U_B = ½LI² (C12) e no "a resistência cancela" (C19);
- o `montar_tags.py` repete a tag ativa no começo de cada bloco do ElevenLabs, para nenhum bloco começar sem tom.
Linhas `> tela:` são âncoras visuais e não são faladas. As tags `[ ]` não entram na legenda.

Status: **texto v2 para aprovação final de TTS**. Não gerar voz antes da confirmação.

---

## C01 — A previsão que falha

> tela: circuito aparece; bateria, chave, resistor e solenoide.

[curious] Olha esse circuito. Uma bateria, uma chave, um resistor e essa bobina comprida aqui, o solenoide. Tudo em série.

> tela: chave aberta; corrente zero.

[thoughtful] Com a chave aberta, não há corrente.

> tela: previsão ingênua; salto para a corrente final.

[curious] Agora eu fecho a chave. Se eu fingisse que a bobina não faz nada, a resposta seria imediata: lei de Ohm. A corrente iria direto para a força eletromotriz da bateria dividida pela resistência.

No gráfico, seria um degrau. Zero de um lado... valor final do outro.

> tela: chave fecha; curva real começa em zero.

[short pause] Vamos testar.

[curious] Só que não acontece isso.

A corrente começa em zero e cresce aos poucos. Ela vai se aproximando daquele valor final, mas não chega lá de uma vez.

> tela: campo magnético magenta cresce dentro do solenoide.

[thoughtful] E olha o solenoide. Enquanto a corrente cresce, o campo magnético dentro dele cresce junto.

Corrente aumentando... campo magnético aumentando.

> tela: "DEVERIA SALTAR. MAS NÃO SALTA."

[curious] Então temos um problema.

Sem a bobina, esperaríamos praticamente um salto.

Com a bobina, a corrente precisa de tempo.

O que, exatamente, está impedindo essa corrente de mudar instantaneamente?

## C02 — Bem-vindos e promessa

> tela: logo.

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

> tela: título.

[thoughtful] No vídeo passado, a gente viu que um campo magnético variável cria um campo elétrico induzido e uma força eletromotriz.

Hoje a gente vai virar essa ideia contra o próprio circuito.

O que acontece quando é a corrente do circuito que cria o campo... e esse campo, ao mudar, reage de volta sobre a própria corrente?

É daí que nasce a indutância.

E a gente vai seguir essa história até o fim: entender por que a corrente resiste a mudar, resolver o circuito, descobrir onde fica a energia que a bateria fornece...

e depois desligar a bateria para ver se essa energia realmente estava lá.

Spoiler: não é simplesmente dentro do fio.

## C03 — Indução mútua

> tela: segunda bobina aparece ao redor do solenoide.

[thoughtful] Antes de fazer uma bobina reagir ao próprio campo, vamos começar com duas.

Em volta do solenoide eu coloco uma segunda bobina, ligada a um medidor.

Ela não tem contato elétrico com o primeiro circuito.

Ela só envolve a região onde existe campo magnético.

> tela: corrente primária muda.

[curious] Agora olha a sequência.

A corrente no solenoide começa a mudar.

> tela: campo cresce.

O campo magnético produzido por ela muda.

> tela: fluxo atravessa bobina 2.

Esse campo atravessa as espiras da segunda bobina.

> tela: medidor responde.

E o medidor acusa uma força eletromotriz.

Corrente muda.

Campo muda.

Fluxo muda.

Força eletromotriz aparece.

Essa cadeia é a ideia inteira.

> tela: fluxo concatenado.

[thoughtful] Para contar o efeito em todas as espiras, usamos o fluxo concatenado.

É o fluxo magnético de cada volta, somado pelas voltas da bobina.

Se o mesmo fluxo atravessa cem espiras, ele entra cem vezes nessa soma.

> tela: corrente fica constante; medidor volta a zero.

[curious] Agora segura a corrente num valor constante.

O campo magnético continua existindo.

O fluxo continua atravessando a segunda bobina.

Mas o medidor volta para zero.

Esse detalhe é fundamental.

[thoughtful, emphatic] A segunda bobina não responde ao simples fato de existir campo magnético.

Ela responde à mudança do fluxo magnético.

> tela: Λ₂ = M I₁.

[thoughtful] Para esta geometria fixa, no nosso modelo ideal, o fluxo concatenado pela segunda bobina é proporcional à corrente no primeiro circuito.

Essa constante de proporcionalidade é a indutância mútua, que aparece na tela como M.

> tela: fem induzida.

[thoughtful] E quando derivamos isso no tempo e usamos a lei de Faraday, aparece a força eletromotriz induzida.

Ela é proporcional à rapidez com que a corrente do primeiro circuito muda.

O sinal negativo é a lei de Lenz: a resposta induzida aparece no sentido de se opor à mudança que a produziu.

> tela: cálculo de M.

[curious] E de onde vem a indutância mútua neste caso?

O fluxo concatenado é o número de espiras da segunda bobina, vezes o campo magnético, vezes a área realmente atravessada pelo campo.

E aqui existe uma pegadinha importante.

A segunda bobina pode ser maior que o solenoide.

Mas, no nosso modelo de solenoide muito longo, o campo relevante está praticamente todo dentro dele.

Então a área que entra na conta é a seção do solenoide.

> tela: B = μ₀ n I.

[thoughtful] Substituindo o campo do solenoide, a corrente aparece como um fator.

Tudo o que sobra multiplicando essa corrente forma a indutância mútua.

No nosso modelo no vácuo, ela depende da geometria do acoplamento e das propriedades magnéticas do meio.

Aqui, como estamos no vácuo, isso fica completamente determinado pela geometria que desenhamos.

## C04 — Reciprocidade

> tela: papéis das bobinas trocam.

[curious] Agora vamos inverter o experimento.

A segunda bobina recebe a fonte.

A corrente nela começa a mudar.

E agora quem sente a força eletromotriz é o primeiro circuito.

> tela: M₁₂ = M₂₁.

[thoughtful] No nosso modelo linear e recíproco, aparece um resultado elegante.

A indutância mútua é a mesma nos dois sentidos.

Troca quem produz o campo, troca quem recebe a força eletromotriz...

o acoplamento entre as duas bobinas continua sendo o mesmo.

> tela: "E SE O SEGUNDO CIRCUITO DESAPARECER?"

[curious] Só que agora vem a pergunta que interessa.

A segunda bobina reagia ao fluxo criado pelo solenoide.

Mas as próprias espiras do solenoide também estão dentro desse fluxo.

Então...

e se eu simplesmente remover a segunda bobina?

## C05 — De indução mútua para autoindução

> tela: bobina 2 desaparece; campo permanece.

[thoughtful] Tiramos a segunda bobina.

O campo magnético continua exatamente onde estava.

> tela: fluxo atravessa as próprias espiras.

[curious] E esse campo atravessa as próprias espiras que o produziram.

Ou seja, o circuito cria um campo...

e depois fica mergulhado no próprio campo.

> tela: Λ = L I.

[thoughtful] Então a mesma lógica vale para o próprio circuito.

O fluxo concatenado com suas próprias espiras é proporcional à corrente.

A constante agora se chama autoindutância.

Na tela, ela aparece como L.

A unidade é o henry.

> tela: ℰ_L = −L dI/dt.

[thoughtful, emphatic] E se a corrente muda, o fluxo próprio muda.

Pela lei de Faraday, surge uma força eletromotriz no próprio circuito.

A força eletromotriz autoinduzida é menos a autoindutância vezes a taxa de variação da corrente.

Esse é o primeiro grande resultado.

> tela: seta ciano indicando fem.

[thoughtful] A seta ciano mostra o sentido dessa força eletromotriz.

Agora presta atenção nela, porque ela vai mudar de direção conforme a corrente muda.

## C06 — O que o indutor realmente combate

> tela: corrente imposta sobe, fica constante e desce.

[curious] Para enxergar o sinal negativo sem esconder nada na álgebra, vamos controlar a corrente manualmente.

Primeiro ela aumenta.

Depois fica constante.

Depois diminui.

E ao lado, o gráfico mostra não só o valor da corrente, mas também sua inclinação.

> tela: corrente aumentando.

[thoughtful] Quando a corrente aumenta, a inclinação é positiva.

A força eletromotriz induzida aponta contra esse aumento.

O indutor tenta reduzir a rapidez com que a corrente cresce.

> tela: corrente constante.

[thoughtful] Agora a corrente fica constante.

A tangente fica horizontal.

A taxa de variação vai a zero.

E a força eletromotriz autoinduzida também vai a zero.

> tela: corrente diminuindo.

[curious] Depois a corrente começa a cair.

A inclinação fica negativa...

e a força eletromotriz troca de sentido.

Agora ela empurra a corrente no sentido em que ela já estava circulando.

Ela tenta impedir a queda.

[happy] O indutor é aquele amigo do contra.

Você quer aumentar a corrente, ele segura.

Você quer diminuir, ele tenta manter.

> tela: payoff.

[thoughtful, emphatic] Então guarda esta frase.

O indutor não se opõe à corrente.

[short pause]

Ele se opõe à mudança da corrente.

> tela: corrente constante, B diferente de zero, fem zero.

[curious] E isso resolve uma confusão comum.

Podemos ter corrente constante.

Podemos ter campo magnético diferente de zero.

E mesmo assim a força eletromotriz autoinduzida ser zero.

Porque o que importa não é a corrente existir.

É a corrente mudar.

No nosso modelo ideal, em corrente contínua estacionária, a queda de tensão induzida no indutor vai a zero...

mas o campo magnético continua lá.

## C07 — A equação do circuito RL

> tela: circuito original volta.

[thoughtful] Agora voltamos ao circuito do começo.

Fonte, resistor e indutor.

Vamos escolher o sentido da corrente como positivo e dar uma volta completa na malha.

Também vamos assumir que toda a resistência relevante está concentrada no resistor e que os fios são ideais.

> tela: bateria.

[thoughtful] A bateria fornece uma força eletromotriz positiva.

> tela: indutor.

[thoughtful] A força eletromotriz autoinduzida vale menos a autoindutância vezes a taxa de variação da corrente.

> tela: resistor.

[thoughtful] E o resistor produz a queda de resistência vezes corrente.

> tela: soma da malha.

[thoughtful] A soma na malha precisa fechar.

Então temos a força eletromotriz da bateria...

mais a força eletromotriz autoinduzida...

menos a queda no resistor...

igual a zero.

> tela: reorganização.

[thoughtful] Substituindo a expressão do indutor e reorganizando, chegamos à equação do circuito com resistor e indutor:

autoindutância vezes a taxa de variação da corrente...

mais resistência vezes corrente...

igual à força eletromotriz da bateria.

E aqui aparece o motivo matemático pelo qual a corrente não pode ser determinada de uma vez.

A própria taxa de variação dela faz parte da equação.

## C08 — Resolvendo a dinâmica

> tela: início da solução.

[curious] Vamos resolver.

É uma equação diferencial...

mas calma, ela é das boazinhas.

> tela: isolar derivada.

[thoughtful] Primeiro isolamos a taxa de variação da corrente.

> tela: corrente final e constante de tempo.

[thoughtful] Agora aparecem duas combinações que valem a pena nomear.

A força eletromotriz da bateria dividida pela resistência é a corrente final.

É o valor para o qual o circuito vai caminhar.

Já a autoindutância dividida pela resistência tem unidade de tempo.

Essa é a constante de tempo do circuito.

E ela vai comandar praticamente tudo daqui para a frente.

> tela: dI/dt = (I∞−I)/τ.

[thoughtful, emphatic] Com esses nomes, a equação fica muito mais interessante.

A rapidez com que a corrente muda é proporcional ao quanto ainda falta para chegar ao valor final.

Longe do final...

muda rápido.

Perto do final...

muda devagar.

É por isso que a curva vai deitando.

> tela: separação.

[thoughtful] Agora separamos as variáveis.

Tudo que envolve corrente vai para um lado.

Tudo que envolve tempo vai para o outro.

> tela: integrais.

[thoughtful] Integramos desde o instante em que a chave fecha.

A condição inicial é simples: no instante zero, a corrente também é zero.

A integral do lado da corrente produz um logaritmo.

A do lado do tempo produz o tempo dividido pela constante de tempo.

> tela: exponenciação.

[thoughtful] Exponenciando, eliminamos o logaritmo.

> tela: solução final.

[thoughtful, emphatic] E isolando a corrente, chegamos à solução.

A corrente é a corrente final multiplicada por um menos uma exponencial decrescente.

Confere os extremos.

No instante zero, a exponencial vale um e a corrente dá zero.

Muito tempo depois, a exponencial desaparece e a corrente tende ao valor final.

A curva misteriosa do começo agora saiu da equação.

## C09 — Uma escala de tempo controla tudo

> tela: circuito, gráfico e campo juntos.

[thoughtful] Agora vamos rodar essa carga de novo.

Só que desta vez olhando todas as peças ao mesmo tempo.

Circuito, gráfico, campo magnético e força eletromotriz obedecem ao mesmo relógio.

> tela: instante inicial.

[curious] No instante zero, a corrente ainda é zero.

Então a queda no resistor também é zero.

Isso significa que, naquele instante, toda a tensão disponível aparece associada à resposta do indutor.

A taxa inicial de crescimento da corrente é a força eletromotriz da bateria dividida pela autoindutância.

Essa é a maior inclinação da curva.

> tela: t = τ.

[thoughtful] Agora anda exatamente uma constante de tempo.

Substituindo na solução, a corrente chega a cerca de sessenta e três por cento do valor final.

Sessenta e três por cento.

Esse número aparece tanto em circuito exponencial que vale guardar.

E sim... cai em prova.

> tela: regime estacionário.

[thoughtful] Depois de umas cinco constantes de tempo, já estamos acima de noventa e nove por cento do valor final.

Na prática, o transiente acabou.

A corrente praticamente não muda mais.

A força eletromotriz autoinduzida desaparece.

Mas o campo magnético continua aceso.

Ele não desapareceu.

Ele simplesmente parou de mudar.

## C10 — B cresce enquanto o campo elétrico induzido desaparece

> tela: solenoide gira para vista axial.

[curious] Agora vamos olhar fisicamente para essa força eletromotriz.

Giramos o solenoide e olhamos pelo eixo.

Os pontos magenta representam o campo magnético atravessando a seção.

> tela: B proporcional à corrente.

[thoughtful] Dentro do solenoide ideal, o campo magnético acompanha a corrente.

Então, enquanto a corrente cresce, o campo cresce junto.

> tela: anéis de E.

[thoughtful] Só que, enquanto esse campo está mudando, Faraday diz que surge um campo elétrico induzido circulando ao redor dele.

São esses anéis ciano.

Dentro do solenoide, a intensidade cresce com a distância ao eixo.

Fora, ela diminui com a distância.

> tela: anéis reagem ao crescimento.

[thoughtful] E o sentido dos anéis vem da lei de Lenz.

Eles aparecem de forma a se opor à mudança do fluxo magnético.

> tela: B forte e constante; E desaparece.

[thoughtful, emphatic] Agora olha o que acontece no final.

O campo magnético ficou forte.

Mas ficou constante.

A taxa de variação desapareceu...

e o campo elétrico induzido desapareceu junto.

Esse é um ponto importante:

um campo magnético constante pode continuar exercendo força sobre cargas em movimento...

mas ele não produz este campo elétrico induzido de Faraday.

Faraday responde à mudança do campo magnético.

## C11 — Construir o campo custa energia

> tela: volta ao circuito.

[curious] Agora entra a segunda pergunta do vídeo.

Construir esse campo magnético saiu de graça?

Claro que não.

Enquanto a corrente cresce, a fonte precisa fornecer energia ao circuito.

A questão é: para onde essa energia vai?

> tela: medidores.

[thoughtful] Olha os três medidores.

A bateria fornece potência.

Uma parte é dissipada no resistor, como calor.

E outra parte está associada ao crescimento do campo magnético.

Vamos mostrar isso diretamente na equação.

> tela: multiplicar por corrente.

[thoughtful] Pegamos a equação da malha e multiplicamos tudo pela corrente.

Porque tensão vezes corrente é potência.

## C12 — A potência se divide

> tela: equação de potência.

[thoughtful] O primeiro termo é a potência fornecida pela bateria.

O segundo é corrente ao quadrado vezes resistência: a potência dissipada no resistor.

E sobra o termo do indutor.

> tela: regra da cadeia.

[curious] E esse termo esconde uma derivada bem conhecida.

A derivada da corrente ao quadrado traz duas vezes a corrente vezes a taxa de variação dela.

Então o termo do indutor pode ser escrito como a derivada de meio vezes autoindutância vezes corrente ao quadrado.

> tela: balanço de potência.

[thoughtful, emphatic] Agora a conta ganha significado físico.

Potência fornecida pela fonte...

é igual à potência dissipada como calor...

mais a taxa com que cresce a energia magnética.

> tela: U_B.

[excited] E aí aparece uma das fórmulas centrais do vídeo.

A energia magnética armazenada é meio vezes a autoindutância vezes a corrente ao quadrado.

> tela: replay com medidores.

[thoughtful] Vamos conferir durante a carga.

Exatamente no instante inicial, a corrente é zero, então todas essas potências também começam em zero.

Mas imediatamente depois, enquanto a corrente ainda é pequena, a dissipação no resistor ainda é fraca e a maior parte da potência que a bateria está fornecendo vai para construir o campo.

À medida que a corrente cresce, o aquecimento do resistor ganha importância.

E no regime estacionário, a energia magnética parou de crescer.

A fonte continua fornecendo potência...

mas ela vai toda para o resistor.

## C13 — Onde está essa energia?

> tela: circuito recua; fica campo.

[curious] Beleza.

Já sabemos quanto de energia está armazenado.

Mas onde ela está?

No fio?

No componente que chamamos de indutor?

Ou no campo magnético espalhado pelo espaço?

A fórmula que encontramos mistura uma propriedade do circuito, a autoindutância, com uma grandeza do estado do circuito, a corrente.

Mas dá para reescrever tudo em termos do próprio campo.

## C14 — Densidade de energia magnética

> tela: área, comprimento e volume.

[thoughtful] Vamos usar o solenoide justamente porque a geometria deixa isso muito claro.

Temos uma área de seção.

Temos um comprimento.

Quando essa área varre o comprimento do solenoide, ela forma o volume interno.

Área vezes comprimento.

> tela: fórmulas B e L.

[thoughtful] Para o solenoide ideal, conhecemos o campo magnético em função da corrente.

E também conhecemos a autoindutância em função da geometria.

> tela: substituir L.

[thoughtful] Substituímos a autoindutância na fórmula da energia.

> tela: reagrupar para B².

[curious] E agora olha o agrupamento.

Permeabilidade do vácuo, vezes espiras por metro, vezes corrente...

é exatamente o campo magnético.

Então toda aquela expressão se reorganiza como campo magnético ao quadrado...

dividido por duas vezes a permeabilidade do vácuo...

multiplicado pelo volume.

> tela: u_B.

[thoughtful, emphatic] Então, no vácuo, a energia por unidade de volume é campo magnético ao quadrado dividido por duas vezes a permeabilidade do vácuo.

E agora olha o que aconteceu.

Sumiram corrente, número de espiras, comprimento, área.

Sobrou o campo.

[short pause]

É nesse sentido que a energia está armazenada no campo magnético.

## C15 — Generalização

> tela: campo não uniforme.

[thoughtful] E no vácuo essa ideia não depende de o campo ser perfeitamente uniforme.

Num solenoide real, por exemplo, o campo se espalha nas bordas e varia de ponto para ponto.

> tela: pequeno elemento de volume.

[thoughtful] Então fazemos o que o cálculo sempre faz quando a coisa varia no espaço.

Pegamos um pedacinho pequeno.

Calculamos a energia naquele pequeno volume.

> tela: integral.

[thoughtful] E somamos todos os pedacinhos.

No limite contínuo, isso vira a integral da densidade de energia magnética pelo espaço.

Onde o campo é mais intenso, existe mais energia por volume.

Onde ele é fraco, existe menos.

Agora temos uma descrição espacial da energia.

Só falta uma prova.

Se essa energia realmente está no campo...

o que acontece quando a fonte desaparece?

## C16 — Comutação para a descarga

> tela: corrente estabelecida.

[curious] Vamos fazer o teste.

A corrente já chegou ao regime.

Existe campo magnético.

Existe energia armazenada.

Agora retiramos a bateria.

> tela: alerta sobre abrir circuito.

[thoughtful] Mas não vamos simplesmente abrir o circuito.

Se a gente tentasse forçar a corrente de um indutor a cair a zero instantaneamente, o modelo exigiria uma variação enorme da corrente e, portanto, uma tensão muito alta.

Num circuito real, isso pode aparecer como uma faísca na chave, além de efeitos parasitas que nosso modelo ideal está ignorando.

Então... não tenta reproduzir essa parte em casa.

> tela: caminho alternativo L-R.

[thoughtful] Em vez disso, a chave comuta para um caminho fechado formado apenas pelo indutor e pelo resistor.

A bateria sai.

O caminho continua fechado.

> tela: corrente continua no mesmo sentido.

[curious] E olha a corrente no instante da troca.

Ela não muda de valor.

Ela continua no mesmo sentido.

O que mudou foi quem está fornecendo a energia.

## C17 — O indutor sustenta a corrente

> tela: equação sem bateria.

[thoughtful] Agora a equação da malha não tem mais a bateria.

Sobra autoindutância vezes a taxa de variação da corrente...

mais resistência vezes corrente...

igual a zero.

> tela: solução da descarga.

[thoughtful] A solução é um decaimento exponencial.

A corrente começa no valor inicial e cai suavemente para zero, com a mesma constante de tempo de antes.

> tela: fem troca de sentido.

[curious] E olha a força eletromotriz do indutor.

A corrente agora está diminuindo.

Então a força eletromotriz muda de sentido e passa a empurrar as cargas a favor da corrente que já existia.

Lembra do amigo do contra?

É ele de novo.

Antes ele tentava impedir a corrente de crescer.

Agora tenta impedir a corrente de cair.

> tela: campo diminuindo.

[thoughtful] Só que agora não existe bateria alimentando o sistema.

Então o campo magnético vai diminuindo.

A energia armazenada nele está saindo.

A pergunta é: para onde?

## C18 — O campo vira calor

> tela: U_B e P_R.

[thoughtful] A corrente cai como uma exponencial.

Como a energia magnética depende da corrente ao quadrado, aparece uma exponencial com duas vezes o tempo dividido pela constante de tempo.

A potência dissipada no resistor também depende da corrente ao quadrado.

Então ela tem exatamente a mesma dependência temporal.

> tela: campo cai, resistor aquece.

[thoughtful] O campo enfraquece.

O resistor aquece.

Energia magnética diminuindo...

energia térmica sendo produzida.

> tela: área sob P_R.

[curious] E potência é energia por unidade de tempo.

Então a energia total transformada em calor até um instante qualquer é a área acumulada embaixo da curva de potência.

Essa área é a integral da potência no tempo.

Agora podemos fazer a conta final.

## C19 — A conservação fecha

> tela: integral total.

[curious] Quanto de calor aparece se esperarmos a descarga terminar?

Integramos a potência dissipada desde o instante inicial até infinito.

> tela: substituir corrente.

[thoughtful] Substituímos a corrente exponencial.

A integral que sobra vale metade da constante de tempo.

Então aparece resistência vezes corrente inicial ao quadrado...

vezes metade da constante de tempo.

> tela: τ = L/R.

[thoughtful] Agora substituímos a constante de tempo pela autoindutância dividida pela resistência.

E olha o que acontece.

A resistência cancela.

> tela: resultado.

[excited] E sobra meio vezes autoindutância vezes a corrente inicial ao quadrado.

Exatamente a energia magnética que existia antes da descarga.

Não aproximadamente.

Exatamente.

Toda a energia inicial do campo reapareceu como calor no resistor.

> tela: destaque da resistência cancelada.

[thoughtful] E a resistência desapareceu da energia total.

Igual meia na máquina de lavar.

Mas, nesse caso, a gente sabe para onde ela foi.

Ela continua controlando a velocidade da descarga.

Resistência maior significa uma constante de tempo menor e uma descarga mais rápida.

Resistência menor significa uma descarga mais lenta.

Mas a quantidade total de energia transformada em calor é a mesma.

> tela: U_B + Q_R constante.

[thoughtful, emphatic] E dá para ver a conservação instante a instante.

A energia magnética diminui.

O calor acumulado aumenta.

E a soma das duas permanece constante.

Uma curva entrega exatamente o que a outra recebe.

Conservação de energia desenhada na tela.

## C20 — Síntese e Maxwell

> tela: autoindução.

[calm, satisfied] Então agora dá para responder à pergunta do começo com cuidado.

Por que a corrente não salta?

Porque mudar a corrente muda o fluxo magnético criado pelo próprio circuito.

E, pela lei de Faraday e pela lei de Lenz, essa mudança produz uma força eletromotriz que se opõe à variação.

Com uma fonte de tensão finita e uma autoindutância finita, a taxa de variação da corrente também fica finita.

A corrente precisa de tempo.

> tela: energia magnética.

[thoughtful] E, ao mesmo tempo, construir a corrente significa construir um campo magnético.

A fonte fornece energia para isso.

Essa energia pode ser escrita como meio vezes autoindutância vezes corrente ao quadrado.

> tela: densidade.

[thoughtful] No vácuo, ela pode ser vista localmente como energia armazenada no campo magnético, com densidade proporcional ao quadrado do campo.

> tela: descarga.

[calm, satisfied] E quando retiramos a bateria mantendo um caminho fechado, essa energia volta.

O campo diminui.

A corrente continua por algum tempo.

E a energia magnética reaparece como calor no resistor.

Essa é a história completa:

a autoindução controla a dinâmica...

e a energia mostra onde foi parar o trabalho feito para construir o campo.

> tela: capacitor aparece.

[curious] Só que a eletrodinâmica ainda tem uma conta pendente.

Troca agora o indutor por um capacitor sendo carregado.

> tela: corrente chega às placas.

[thoughtful] A corrente percorre os fios e chega às placas.

Mas carga nenhuma atravessa o espaço vazio entre elas como corrente de condução.

> tela: caminho amperiano e primeira superfície.

[thoughtful] Agora desenha um mesmo contorno fechado ao redor do fio.

Pela lei de Ampère original, a circulação do campo magnético depende da corrente que atravessa uma superfície apoiada nesse contorno.

Se escolhemos uma superfície que corta o fio...

tem corrente atravessando.

> tela: segunda superfície passando entre placas.

[curious] Mas eu posso escolher outra superfície com exatamente a mesma borda.

Ela infla como uma bolsa e passa pelo espaço entre as placas do capacitor.

Ali não existe corrente de condução atravessando.

Então uma superfície diz que a corrente é diferente de zero...

e a outra diz que é zero.

> tela: mesmo contorno, duas respostas.

[curious] Mesmo contorno.

Duas respostas.

Alguma coisa está faltando na lei.

> tela: pergunta final.

[curious] Então fica a pergunta:

como o campo magnético sabe que o circuito continua do outro lado do capacitor?

[short pause]

Se você já tem um palpite, deixa nos comentários.

> tela: encerramento + próximo.

[calm, satisfied] Se essas conexões ajudaram você a enxergar a física por trás das equações, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

No próximo, a gente vai descobrir qual foi a peça que Maxwell acrescentou à lei de Ampère...

e por que essa correção acabou conectando eletricidade, magnetismo e luz.

Valeu, pessoal.

Até a próxima!
