# yt_0017 — CENTRO DE MASSA · narração com audio tags (v4, a partir da v3.2)

Sugestão para a fase de voz (ElevenLabs v4, voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`). **Não gerada.** A fonte da fala continua sendo
`narracao_sugestao.md` (v3.2); este arquivo é a cópia com tags e com as poucas trocas que a análise quadro a quadro do preview v6 pediu.
3075 palavras ≈ 19.0 min a 2,7 palavras/s (a v3.2 tem 3063).

## Análise quadro a quadro (preview v6 × fala v3.2)

Quatro quadros por âncora (10%, 35%, 60% e 85% do trecho), nos seis lotes. A fala e a tela batem em todas as âncoras: cada entrada da cena
já cai na palavra que a anuncia (`self.em`). O que mudou na fala, e por quê:

| Âncora | Tela | Fala v3.2 | Sugestão |
|---|---|---|---|
| T1-4 | régua com X − x₁ e x₂ − X; a conta isola X | "chama a posição do apoio de X … põe o X em evidência" (letra solta) | "a posição do apoio … põe essa posição em evidência" (§5: nunca a letra) + `[short pause]` antes da fórmula |
| T2-7 | R⃗_cm(t) = R⃗₀ + V⃗₀t + ½g⃗t² | "meio de g vezes o tempo ao quadrado" | "metade da aceleração da gravidade vezes o tempo ao quadrado" |
| E1-1 | X = ½ m POR SIMETRIA; o eixo x = ½ acende | "em x igual a meio metro" | "a meio metro da borda" |
| EN1 | v_f = V_cm → = Σ mᵢvᵢ/M (da caixa do T2-2) → = (m₁v₁ᵢ + m₂v₂ᵢ)/(m₁ + m₂) → ⅔ m/s | só "a velocidade final é a do centro de massa: dois terços…" (os passos 2 e 3 passam calados) | "…a do centro de massa, a média das velocidades pesada pelas massas: dois terços…" (+8 palavras, ~3 s) |
| E1-3, T3-3 | o resultado nasce no centro da tela (7/18; o 0⃗) | sem respiro antes do resultado | `[short pause]` antes de "sete dezoito avos" e de "zero" |
| T1-4, T2-3, T3-4 | conceito-chave na caixa | tag `[emphatic]` sozinha | `[thoughtful, emphatic]` (a combinação validada) |
| T1-7, T2-4, T3-7 | caixa central do bloco (equilíbrio, 3ª lei, cadeado) | `[thoughtful]`/`[curious]` | `[thoughtful, emphatic]` |
| S1 | a granada de novo, "QUEM CONTINUA NA PARÁBOLA É O ⊕" | `[calm]` | `[calm, satisfied]` (fechamento na pergunta do hook) |

Sem mudança de fala: hook, abertura, T1-1–T1-3, T1-5–T1-8, T2-1–T2-6, T2-8–T2-9, T3 (exceto a pausa), T4, E1-2, E1-4, E2, S2, EN2.

**Na tela (não é fala, fica anotado):** no T1-8 o selo `DO T1-6: Σ mᵢr⃗ᵢ = (6, 4)` usa o código interno da âncora; o espectador não sabe o que
é "T1-6". Sugestão para a próxima rodada de tela: `DE ANTES:` ou `DA CONTA DE ANTES:`.

**Tempo:** as trocas somam +12 palavras (T1-4, T2-7, E1-1 e EN1). Depois de gerada a voz, as âncoras e a cena são ajustadas à
duração real (a voz manda); nada aqui exige render agora.

**Tags:** [curious] ×14, [thoughtful] ×12, [thoughtful, emphatic] ×6, [short pause] ×4, [happy] ×2, [excited] ×1, [calm, satisfied] ×1. Uma tag por trecho, em inglês, sem `[slowly]` nem `[pause]`.

## Roteiro por âncora (com tags)

### HOOK

**H1** · 25 palavras · ~9.3 s  
[curious] Olha essa granada subindo. Sem resistência do ar, a gente sabe exatamente o caminho dela: uma parábola, a mesma de qualquer pedra jogada para cima.

**H2** · 24 palavras · ~8.9 s  
Só que, lá no alto, ela explode. Três pedaços, de massas diferentes, voando cada um para um lado. Parece que a parábola acabou ali.

**H3** · 34 palavras · ~12.6 s  
[curious] Mas olha esse ponto brilhando. Os pedaços se espalham, e ele segue em cima da parábola, como se nada tivesse acontecido. Que ponto é esse? E por que a explosão não consegue mexer nele?


### ABERTURA

**A1** · 7 palavras · ~2.6 s  
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

**A2** · 17 palavras · ~6.3 s  
[thoughtful] Hoje o assunto é o centro de massa. E ele é a continuação direta do vídeo anterior.

**A3** · 45 palavras · ~16.7 s  
No vídeo anterior, a gente viu que, num sistema de vários corpos, as forças de dentro se cancelam aos pares. A taxa de variação do momento total só depende da força externa resultante. O cavalo anda porque o chão empurra, não porque a corda puxa.

**A4** · 42 palavras · ~15.6 s  
[curious] Só que aquela equação fala do momento do sistema inteiro, e não diz onde. Hoje a gente vai achar um lugar para ela: um ponto que se move como se toda a massa estivesse ali e toda a força externa agisse ali.


### T1 — ONDE ESTÁ O CENTRO DE MASSA?

**T1-1** · 62 palavras · ~23.0 s  
[curious] Primeira pergunta: onde está o centro de massa? Olha esse haltere torto, com uma bola de três quilogramas e uma de um, girando. A câmera está acompanhando um ponto especial da haste, por isso ele parece parado. Cada bola dá a sua volta, mas é em torno desse ponto que tudo gira. E repara: ele fica bem mais perto da bola pesada.

**T1-2** · 52 palavras · ~19.3 s  
Vamos achar esse ponto com números. Põe o mesmo haltere deitado sobre uma régua: a bola de um quilograma na posição zero, e a de três quilogramas a quatro metros. Onde a gente apoia a haste para ela ficar em equilíbrio? A três metros da leve, e a um metro da pesada.

**T1-3** · 48 palavras · ~17.8 s  
Por quê? É a regra da alavanca, a mesma da gangorra. A massa da leve vezes a distância dela até o apoio tem que ser igual à massa da pesada vezes a distância dela. Um vezes três, três vezes um. A massa grande, perto; a massa pequena, longe.

**T1-4** · 76 palavras · ~28.1 s  
[thoughtful, emphatic] Agora escreve as distâncias como diferenças entre a posição de cada bola e a posição do apoio. Abre os parênteses, junta os dois termos com a posição do apoio do mesmo lado e põe essa posição em evidência... [short pause] e aparece a fórmula do centro de massa: cada posição multiplicada pela sua massa, somadas, divididas pela massa total. É uma média das posições, só que pesada pelas massas. Colocando os números, dá três metros, exatamente o apoio.

**T1-5** · 45 palavras · ~16.7 s  
Repara numa coisa importante. Se a gente muda a origem da régua, todas as posições mudam, e o resultado da conta também muda. Mas o ponto na haste é o mesmo. O centro de massa é um lugar do sistema, não um número da régua.

**T1-6** · 94 palavras · ~34.8 s  
[thoughtful] Com muitos corpos, no plano ou no espaço, a ideia é a mesma, coordenada por coordenada. A coordenada horizontal do centro de massa é a média pesada das coordenadas horizontais; a vertical, das verticais; e a de profundidade, igual. Juntando tudo num vetor: a posição do centro de massa é a soma das massas vezes as posições, dividida pela massa total. Com essas três massas, a soma de massa vezes posição dá seis na horizontal e quatro na vertical. Dividindo pela massa total, quatro quilogramas, ele cai em um vírgula cinco e um metro.

**T1-7** · 129 palavras · ~47.8 s  
[thoughtful, emphatic] E é por isso que um corpo apoiado no centro de massa fica em equilíbrio. Apoia fora dele, e a chapa tomba para o lado onde tem mais massa. Apoia nele, e ela fica parada. Na conta: medindo cada posição a partir do centro de massa, a soma de massa vezes posição dá zero, porque é a soma de massa vezes posição menos a massa total vezes a posição do centro de massa. Com a gravidade igual em todo lugar, o peso de cada pedaço é proporcional à massa, e as alavancas dos pesos se compensam em todas as direções. Por isso ele também é chamado de centro de gravidade. Só se a gravidade mudasse de um ponto para outro do corpo é que os dois deixariam de coincidir.

**T1-8** · 104 palavras · ~38.5 s  
[curious] E tem um atalho que vai servir muito. Qualquer pedaço do sistema pode ser trocado por uma partícula só, com a massa daquele pedaço, sentada no centro de massa dele. Olha: as duas massas de um quilograma viram uma de dois, no ponto médio entre elas, em três e dois. Sobram duas massas de dois quilogramas, e o centro de massa fica no meio do caminho entre elas: de novo, um vírgula cinco e um. Por partes, dá o mesmo. E repara num detalhe: entre duas massas, o centro de massa divide a distância na razão inversa das massas. Massas iguais, bem no meio.


### T2 — COMO ELE SE MOVE?

**T2-1** · 83 palavras · ~30.7 s  
[curious] Segunda pergunta: como esse ponto se move? Lembra do haltere girando? Agora a câmera se afasta. O haltere foi jogado para cima, e as bolas fazem essas curvas cheias de laços. Mas o centro de massa faz uma parábola limpa, como uma pedra. São dois movimentos separados: o ponto andando, e o haltere girando em volta dele. Dá até para escrever isso: a posição de cada bola é a posição do centro de massa mais uma seta que só gira em volta dele.

**T2-2** · 47 palavras · ~17.4 s  
[thoughtful] Para entender por quê, deriva a fórmula do centro de massa em relação ao tempo. Como as massas não mudam, a derivada passa para dentro da soma, e cada posição vira uma velocidade: a velocidade do centro de massa é a média das velocidades, pesada pelas massas.

**T2-3** · 55 palavras · ~20.4 s  
[thoughtful, emphatic] E olha o que apareceu do lado direito. Massa vezes velocidade, somado para todos: é o momento total do sistema. Ou seja, o momento total é a massa total vezes a velocidade do centro de massa. É como se o sistema inteiro fosse uma partícula só, com toda a massa, sentada no centro de massa.

**T2-4** · 91 palavras · ~33.7 s  
[thoughtful, emphatic] Derivando mais uma vez, aparece a aceleração. Massa vezes aceleração de cada partícula é a força resultante nela, e essa força tem duas partes: as internas, que as partículas fazem umas nas outras, e as externas. As internas vêm em pares de ação e reação: a força que a primeira faz na segunda é igual e contrária à que a segunda faz na primeira. Somando par por par, cada par dá zero. Sobra só isso: a massa total vezes a aceleração do centro de massa é igual à força externa resultante.

**T2-5** · 64 palavras · ~23.7 s  
[thoughtful] Repara que isso não é uma física nova. É a mesma equação do vídeo anterior, só que lida de outro jeito. Ela diz que o centro de massa se move como uma partícula de massa igual à do sistema, empurrada só pelas forças de fora. As forças de dentro podem fazer o que quiserem com as partes: no centro de massa, elas não chegam.

**T2-6** · 69 palavras · ~25.6 s  
Primeiro, no espaço, longe de tudo, sem gravidade. Um corpo andando reto explode nos mesmos três pedaços do começo. A explosão é feita de forças internas, então o centro de massa nem percebe: continua reto, com a mesma velocidade. E olha o momento: antes, uma seta só. Depois, cada pedaço leva a sua parte, mas, somando as três setas ponta com ponta, volta exatamente a mesma seta de antes.

**T2-7** · 114 palavras · ~42.2 s  
[excited] Agora a granada. Durante o voo, sem ar, a única força externa é o peso de todos os pedaços juntos: a massa total vezes a gravidade. Então a massa total cancela, e a aceleração do centro de massa é a aceleração da gravidade, antes e depois da explosão. Integrando duas vezes, a posição dele é a posição inicial, mais a velocidade inicial vezes o tempo, mais metade da aceleração da gravidade vezes o tempo ao quadrado, sem nenhum termo da explosão. O centro de massa faz exatamente a mesma parábola que a granada inteira faria, exatamente como o haltere. A pergunta do começo está respondida: quem continua na parábola é o centro de massa.

**T2-8** · 93 palavras · ~34.4 s  
[curious] Mas cuidado com um detalhe. Isso vale enquanto nenhum pedaço encosta em nada. Quando o primeiro pedaço bate no chão e para, o chão dá um empurrão nele: é uma força externa nova. O centro de massa não pula de lugar, mas a velocidade dele muda nesse instante. E a conta é direta: o impulso do chão tira todo o momento do pedaço, a massa dele vezes a velocidade com que chegou. Dividindo pela massa total, sai a mudança na velocidade do centro de massa. Daí para a frente, ele sai da parábola.

**T2-9** · 94 palavras · ~34.8 s  
E, se não há força externa nenhuma, e o sistema começa parado, o centro de massa fica parado para sempre. Duas pessoas no gelo, a dez metros uma da outra, puxando uma corda. O centro de massa está em sessenta vezes zero mais quarenta vezes dez, dividido por cem: quatro metros da mais pesada. Ele não se mexe, então é exatamente ali que elas se encontram. E é por isso que a ideia do Cyrano, de jogar um ímã para cima para subir junto, nunca funciona: o centro de massa do conjunto não sobe.


### T3 — QUE ENERGIA É DO MOVIMENTO RELATIVO?

**T3-1** · 35 palavras · ~13.0 s  
[curious] Terceira pergunta, e ela é sobre energia. Olha a explosão de novo, vista do chão. Cada pedaço tem uma velocidade, e todas elas carregam um pedaço comum: o conjunto inteiro está andando para a direita.

**T3-2** · 56 palavras · ~20.7 s  
[thoughtful] Agora a câmera passa a andar junto com o centro de massa. A parte comum some da tela, e sobra só o movimento de cada pedaço em relação ao centro de massa. Ou seja, a velocidade de cada pedaço é a velocidade do centro de massa mais a velocidade dele em relação ao centro de massa.

**T3-3** · 108 palavras · ~40.0 s  
Primeiro, um fato que você acabou de ver: nesse referencial, os pedaços se afastam de um ponto parado. E repara nas setas de momento, vistas daqui: as três têm o mesmo tamanho. Como saem separadas por ângulos iguais, só assim a soma dá zero, e por isso o pedaço mais leve é o que sai mais rápido. Agora a conta: somando massa vezes velocidade em relação ao centro de massa, dá o momento total menos a massa total vezes a velocidade do centro de massa. Mas isso é o momento menos ele mesmo: [short pause] zero. Visto de cima do centro de massa, o momento do sistema é sempre zero.

**T3-4** · 85 palavras · ~31.5 s  
[thoughtful, emphatic] Agora a energia cinética. Abrindo o quadrado, aparecem três termos. O do meio carrega exatamente aquela soma que dá zero, então ele some. Sobra uma separação limpa: a energia cinética total é a energia do centro de massa andando, metade da massa total vezes a velocidade dele ao quadrado, mais a energia cinética do movimento relativo, dos pedaços em relação ao centro de massa. Repara: aqui é tudo energia de movimento. Não é a energia interna da termodinâmica, aquela das moléculas e das ligações químicas.

**T3-5** · 42 palavras · ~15.6 s  
[thoughtful] Isso explica a explosão de um jeito novo. Parte da energia química guardada na granada vira energia cinética dos pedaços, uns em relação aos outros. A energia do centro de massa não muda por causa da explosão, porque a explosão é interna.

**T3-6** · 100 palavras · ~37.0 s  
[curious] E vale para as colisões também. Um bloco de dois quilogramas a seis metros por segundo bate num bloco de um quilograma parado, e eles grudam. A energia antes é trinta e seis joules. A do centro de massa, que anda a quatro metros por segundo com os três quilogramas, é vinte e quatro joules. Então a energia do movimento relativo é doze. Depois do choque, os blocos andam juntos, e sobram exatamente vinte e quatro. Os doze joules relativos deixaram de ser energia de movimento: viraram deformação, aquecimento, som. A colisão consumiu toda a energia relativa, e nada mais.

**T3-7** · 69 palavras · ~25.6 s  
[thoughtful, emphatic] Ou seja, sem força externa, uma colisão nunca pode perder mais do que a energia do movimento relativo. A energia do centro de massa fica trancada: é ela que garante que, depois de qualquer batida, o conjunto continue andando. Mas repara na condição: sem força externa. Na granada, a gravidade é externa e faz trabalho, então a energia do centro de massa dela muda, sim, ao longo da parábola.


### T4 — COMO ACHAR O CENTRO DE MASSA DE UM CORPO INTEIRO?

**T4-1** · 64 palavras · ~23.7 s  
[thoughtful] Última pergunta da teoria. Até agora foram pontos. E um corpo inteiro, uma barra, uma chapa, uma esfera? A gente corta em pedacinhos de massa, cada um na sua posição, e soma. Quanto menores os pedaços, melhor. No limite, a soma vira uma integral: a posição do centro de massa é a integral da posição vezes o pedacinho de massa, dividida pela massa total.

**T4-2** · 39 palavras · ~14.4 s  
[thoughtful] O pedacinho de massa depende do corpo. Num fio, é a densidade por comprimento vezes um pedacinho de comprimento. Numa chapa, a densidade por área vezes um pedacinho de área. Num sólido, a densidade vezes um pedacinho de volume.

**T4-3** · 39 palavras · ~14.4 s  
[curious] Só que, muitas vezes, nem precisa integrar. Barra, disco, esfera uniformes: por simetria, o centro de massa está no centro. E olha o anel. Pela mesma simetria, o centro de massa fica no meio... onde não tem material nenhum.

**T4-4** · 60 palavras · ~22.2 s  
Quando a simetria não resolve, entra a integral. Uma barra de dois metros que fica mais densa de uma ponta para a outra, com a densidade crescendo junto com a posição. Fazendo as duas integrais, o centro de massa fica a dois terços do comprimento: um vírgula trinta e três metros, mais perto da ponta pesada, como a intuição diria.


### E1 — PLACA COM ENTALHE

**E1-1** · 59 palavras · ~21.9 s  
[thoughtful] Primeiro exercício. Uma placa quadrada e uniforme, de um metro de lado, da qual alguém recortou um triângulo em cima, com a ponta no centro do quadrado. Onde fica o centro de massa do que sobrou? Por simetria, ele está na vertical do meio, a meio metro da borda. Falta a altura. E dá para fazer de dois jeitos.

**E1-2** · 90 palavras · ~33.3 s  
Primeiro jeito: o que sobrou se divide em três triângulos iguais, cada um com um quarto da área do quadrado. E o centro de massa de um triângulo uniforme fica na média dos três vértices. Trocando cada triângulo por uma partícula no centro dele, as alturas dão um sexto, meio e meio. Como as três massas são iguais, o centro de massa é a média simples das alturas: sete dezoito avos de metro, uns trinta e nove centímetros. Repara que ficou abaixo do meio: o recorte tirou massa de cima.

**E1-3** · 91 palavras · ~33.7 s  
[curious] Segundo jeito, e esse é um truque de verdade: massa negativa. O que sobrou é o quadrado inteiro menos o triângulo. Então a gente conta o quadrado inteiro, com massa um e centro de massa no meio, e soma o triângulo com massa negativa. O triângulo tem um quarto da área, e o centro de massa dele está a cinco sextos de altura, na média dos vértices. Meio, menos um quarto vezes cinco sextos, dividido por três quartos. E sai, de novo... [short pause] sete dezoito avos. O mesmo ponto, por outro caminho.

**E1-4** · 73 palavras · ~27.0 s  
[thoughtful] Guarda essa dica: um buraco funciona como massa negativa, e o centro de massa sempre foge do furo, para o lado onde sobrou mais material. E fica um desafio: um disco de um metro de raio, com um furo de meio metro de raio, cujo centro está a vinte e cinco centímetros do centro do disco. Onde fica o centro de massa? Usa a massa negativa e deixa a sua resposta nos comentários.


### E2 — REMADOR E ESTACA

**E2-1** · 63 palavras · ~23.3 s  
[curious] Segundo exercício. Um remador de setenta e cinco quilogramas está na popa de uma canoa de cento e cinquenta quilogramas e três metros, parada, com a proa encostada numa estaca. Ele esqueceu de amarrar a canoa. Então levanta, anda até a proa, e estica o braço: o braço dele alcança oitenta centímetros à frente da proa. Será que ele consegue pegar a estaca?

**E2-2** · 49 palavras · ~18.1 s  
[thoughtful] Na horizontal, a água quase não faz força, então não tem força externa. E tudo começa parado. Então o centro de massa do sistema, remador mais canoa, não pode sair do lugar. Quando ele anda para a frente, a canoa tem que andar para trás, para longe da estaca.

**E2-3** · 94 palavras · ~34.8 s  
[thoughtful] Vamos às contas. O remador anda três metros em relação à canoa, para trás no eixo. Mas, em relação à água, o deslocamento dele é esses três metros mais o que a canoa andou. O centro de massa fixo diz que a massa do remador vezes o deslocamento dele, mais a massa da canoa vezes o dela, dá zero. Resolvendo, a canoa anda um metro para longe da estaca, e o remador anda só dois metros em relação à água. Confere: setenta e cinco vezes dois é igual a cento e cinquenta vezes um.

**E2-4** · 67 palavras · ~24.8 s  
[curious] Agora a resposta. A proa ficou a um metro da estaca, e o braço alcança oitenta centímetros. Faltam vinte centímetros. O certo era ter amarrado antes de levantar. E a dica que esse exercício deixa: o deslocamento em relação à canoa não é o deslocamento em relação à água. Quem está parado é o centro de massa, e é em relação à água que ele está parado.


### SÍNTESE

**S1** · 49 palavras · ~18.1 s  
[calm, satisfied] Então, voltando à pergunta do começo. Quando a granada explode, as forças da explosão são internas, e força interna não mexe no centro de massa. A única força externa é o peso total, e por isso o centro de massa segue a mesma parábola. A pergunta inicial está respondida.

**S2** · 91 palavras · ~33.7 s  
Resumindo em quatro perguntas. Onde está: na média das posições, pesada pelas massas, e dá para fazer por partes, até com massa negativa. Como se move: como uma partícula com toda a massa do sistema, empurrada só pelas forças de fora. Que energia é relativa: a energia cinética se divide na do centro de massa, que só muda com força externa, e na do movimento relativo, que as forças internas podem criar, como na explosão, ou consumir, como na colisão. E num corpo inteiro: a soma vira integral, mas simetria primeiro.


### ENCERRAMENTO

**EN1** · 114 palavras · ~42.2 s  
[curious] E isso já diz muito sobre colisões. Dois blocos vêm um contra o outro, batem e grudam. A batida é interna, então o centro de massa nem percebe: segue reto, com a mesma velocidade. E, grudados, os dois só podem andar junto com ele. Então a velocidade final é a do centro de massa, a média das velocidades pesada pelas massas: [short pause] dois terços de metro por segundo. Agora olha a mesma batida andando junto com o centro de massa. Os dois chegam com momentos iguais e opostos, e param. Toda a energia relativa vira outra coisa, e a do centro de massa fica. É isso que a gente vai explorar no módulo de colisões.

**EN2** · 24 palavras · ~8.9 s  
[happy] Se esse ponto mudou o jeito como você vê uma explosão, se inscreve no Parallax Lab para acompanhar os próximos vídeos. Até a próxima!


## Texto corrido (para gravação)

[curious] Olha essa granada subindo. Sem resistência do ar, a gente sabe exatamente o caminho dela: uma parábola, a mesma de qualquer pedra jogada para cima.

Só que, lá no alto, ela explode. Três pedaços, de massas diferentes, voando cada um para um lado. Parece que a parábola acabou ali.

[curious] Mas olha esse ponto brilhando. Os pedaços se espalham, e ele segue em cima da parábola, como se nada tivesse acontecido. Que ponto é esse? E por que a explosão não consegue mexer nele?

[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

[thoughtful] Hoje o assunto é o centro de massa. E ele é a continuação direta do vídeo anterior.

No vídeo anterior, a gente viu que, num sistema de vários corpos, as forças de dentro se cancelam aos pares. A taxa de variação do momento total só depende da força externa resultante. O cavalo anda porque o chão empurra, não porque a corda puxa.

[curious] Só que aquela equação fala do momento do sistema inteiro, e não diz onde. Hoje a gente vai achar um lugar para ela: um ponto que se move como se toda a massa estivesse ali e toda a força externa agisse ali.

[curious] Primeira pergunta: onde está o centro de massa? Olha esse haltere torto, com uma bola de três quilogramas e uma de um, girando. A câmera está acompanhando um ponto especial da haste, por isso ele parece parado. Cada bola dá a sua volta, mas é em torno desse ponto que tudo gira. E repara: ele fica bem mais perto da bola pesada.

Vamos achar esse ponto com números. Põe o mesmo haltere deitado sobre uma régua: a bola de um quilograma na posição zero, e a de três quilogramas a quatro metros. Onde a gente apoia a haste para ela ficar em equilíbrio? A três metros da leve, e a um metro da pesada.

Por quê? É a regra da alavanca, a mesma da gangorra. A massa da leve vezes a distância dela até o apoio tem que ser igual à massa da pesada vezes a distância dela. Um vezes três, três vezes um. A massa grande, perto; a massa pequena, longe.

[thoughtful, emphatic] Agora escreve as distâncias como diferenças entre a posição de cada bola e a posição do apoio. Abre os parênteses, junta os dois termos com a posição do apoio do mesmo lado e põe essa posição em evidência... [short pause] e aparece a fórmula do centro de massa: cada posição multiplicada pela sua massa, somadas, divididas pela massa total. É uma média das posições, só que pesada pelas massas. Colocando os números, dá três metros, exatamente o apoio.

Repara numa coisa importante. Se a gente muda a origem da régua, todas as posições mudam, e o resultado da conta também muda. Mas o ponto na haste é o mesmo. O centro de massa é um lugar do sistema, não um número da régua.

[thoughtful] Com muitos corpos, no plano ou no espaço, a ideia é a mesma, coordenada por coordenada. A coordenada horizontal do centro de massa é a média pesada das coordenadas horizontais; a vertical, das verticais; e a de profundidade, igual. Juntando tudo num vetor: a posição do centro de massa é a soma das massas vezes as posições, dividida pela massa total. Com essas três massas, a soma de massa vezes posição dá seis na horizontal e quatro na vertical. Dividindo pela massa total, quatro quilogramas, ele cai em um vírgula cinco e um metro.

[thoughtful, emphatic] E é por isso que um corpo apoiado no centro de massa fica em equilíbrio. Apoia fora dele, e a chapa tomba para o lado onde tem mais massa. Apoia nele, e ela fica parada. Na conta: medindo cada posição a partir do centro de massa, a soma de massa vezes posição dá zero, porque é a soma de massa vezes posição menos a massa total vezes a posição do centro de massa. Com a gravidade igual em todo lugar, o peso de cada pedaço é proporcional à massa, e as alavancas dos pesos se compensam em todas as direções. Por isso ele também é chamado de centro de gravidade. Só se a gravidade mudasse de um ponto para outro do corpo é que os dois deixariam de coincidir.

[curious] E tem um atalho que vai servir muito. Qualquer pedaço do sistema pode ser trocado por uma partícula só, com a massa daquele pedaço, sentada no centro de massa dele. Olha: as duas massas de um quilograma viram uma de dois, no ponto médio entre elas, em três e dois. Sobram duas massas de dois quilogramas, e o centro de massa fica no meio do caminho entre elas: de novo, um vírgula cinco e um. Por partes, dá o mesmo. E repara num detalhe: entre duas massas, o centro de massa divide a distância na razão inversa das massas. Massas iguais, bem no meio.

[curious] Segunda pergunta: como esse ponto se move? Lembra do haltere girando? Agora a câmera se afasta. O haltere foi jogado para cima, e as bolas fazem essas curvas cheias de laços. Mas o centro de massa faz uma parábola limpa, como uma pedra. São dois movimentos separados: o ponto andando, e o haltere girando em volta dele. Dá até para escrever isso: a posição de cada bola é a posição do centro de massa mais uma seta que só gira em volta dele.

[thoughtful] Para entender por quê, deriva a fórmula do centro de massa em relação ao tempo. Como as massas não mudam, a derivada passa para dentro da soma, e cada posição vira uma velocidade: a velocidade do centro de massa é a média das velocidades, pesada pelas massas.

[thoughtful, emphatic] E olha o que apareceu do lado direito. Massa vezes velocidade, somado para todos: é o momento total do sistema. Ou seja, o momento total é a massa total vezes a velocidade do centro de massa. É como se o sistema inteiro fosse uma partícula só, com toda a massa, sentada no centro de massa.

[thoughtful, emphatic] Derivando mais uma vez, aparece a aceleração. Massa vezes aceleração de cada partícula é a força resultante nela, e essa força tem duas partes: as internas, que as partículas fazem umas nas outras, e as externas. As internas vêm em pares de ação e reação: a força que a primeira faz na segunda é igual e contrária à que a segunda faz na primeira. Somando par por par, cada par dá zero. Sobra só isso: a massa total vezes a aceleração do centro de massa é igual à força externa resultante.

[thoughtful] Repara que isso não é uma física nova. É a mesma equação do vídeo anterior, só que lida de outro jeito. Ela diz que o centro de massa se move como uma partícula de massa igual à do sistema, empurrada só pelas forças de fora. As forças de dentro podem fazer o que quiserem com as partes: no centro de massa, elas não chegam.

Primeiro, no espaço, longe de tudo, sem gravidade. Um corpo andando reto explode nos mesmos três pedaços do começo. A explosão é feita de forças internas, então o centro de massa nem percebe: continua reto, com a mesma velocidade. E olha o momento: antes, uma seta só. Depois, cada pedaço leva a sua parte, mas, somando as três setas ponta com ponta, volta exatamente a mesma seta de antes.

[excited] Agora a granada. Durante o voo, sem ar, a única força externa é o peso de todos os pedaços juntos: a massa total vezes a gravidade. Então a massa total cancela, e a aceleração do centro de massa é a aceleração da gravidade, antes e depois da explosão. Integrando duas vezes, a posição dele é a posição inicial, mais a velocidade inicial vezes o tempo, mais metade da aceleração da gravidade vezes o tempo ao quadrado, sem nenhum termo da explosão. O centro de massa faz exatamente a mesma parábola que a granada inteira faria, exatamente como o haltere. A pergunta do começo está respondida: quem continua na parábola é o centro de massa.

[curious] Mas cuidado com um detalhe. Isso vale enquanto nenhum pedaço encosta em nada. Quando o primeiro pedaço bate no chão e para, o chão dá um empurrão nele: é uma força externa nova. O centro de massa não pula de lugar, mas a velocidade dele muda nesse instante. E a conta é direta: o impulso do chão tira todo o momento do pedaço, a massa dele vezes a velocidade com que chegou. Dividindo pela massa total, sai a mudança na velocidade do centro de massa. Daí para a frente, ele sai da parábola.

E, se não há força externa nenhuma, e o sistema começa parado, o centro de massa fica parado para sempre. Duas pessoas no gelo, a dez metros uma da outra, puxando uma corda. O centro de massa está em sessenta vezes zero mais quarenta vezes dez, dividido por cem: quatro metros da mais pesada. Ele não se mexe, então é exatamente ali que elas se encontram. E é por isso que a ideia do Cyrano, de jogar um ímã para cima para subir junto, nunca funciona: o centro de massa do conjunto não sobe.

[curious] Terceira pergunta, e ela é sobre energia. Olha a explosão de novo, vista do chão. Cada pedaço tem uma velocidade, e todas elas carregam um pedaço comum: o conjunto inteiro está andando para a direita.

[thoughtful] Agora a câmera passa a andar junto com o centro de massa. A parte comum some da tela, e sobra só o movimento de cada pedaço em relação ao centro de massa. Ou seja, a velocidade de cada pedaço é a velocidade do centro de massa mais a velocidade dele em relação ao centro de massa.

Primeiro, um fato que você acabou de ver: nesse referencial, os pedaços se afastam de um ponto parado. E repara nas setas de momento, vistas daqui: as três têm o mesmo tamanho. Como saem separadas por ângulos iguais, só assim a soma dá zero, e por isso o pedaço mais leve é o que sai mais rápido. Agora a conta: somando massa vezes velocidade em relação ao centro de massa, dá o momento total menos a massa total vezes a velocidade do centro de massa. Mas isso é o momento menos ele mesmo: [short pause] zero. Visto de cima do centro de massa, o momento do sistema é sempre zero.

[thoughtful, emphatic] Agora a energia cinética. Abrindo o quadrado, aparecem três termos. O do meio carrega exatamente aquela soma que dá zero, então ele some. Sobra uma separação limpa: a energia cinética total é a energia do centro de massa andando, metade da massa total vezes a velocidade dele ao quadrado, mais a energia cinética do movimento relativo, dos pedaços em relação ao centro de massa. Repara: aqui é tudo energia de movimento. Não é a energia interna da termodinâmica, aquela das moléculas e das ligações químicas.

[thoughtful] Isso explica a explosão de um jeito novo. Parte da energia química guardada na granada vira energia cinética dos pedaços, uns em relação aos outros. A energia do centro de massa não muda por causa da explosão, porque a explosão é interna.

[curious] E vale para as colisões também. Um bloco de dois quilogramas a seis metros por segundo bate num bloco de um quilograma parado, e eles grudam. A energia antes é trinta e seis joules. A do centro de massa, que anda a quatro metros por segundo com os três quilogramas, é vinte e quatro joules. Então a energia do movimento relativo é doze. Depois do choque, os blocos andam juntos, e sobram exatamente vinte e quatro. Os doze joules relativos deixaram de ser energia de movimento: viraram deformação, aquecimento, som. A colisão consumiu toda a energia relativa, e nada mais.

[thoughtful, emphatic] Ou seja, sem força externa, uma colisão nunca pode perder mais do que a energia do movimento relativo. A energia do centro de massa fica trancada: é ela que garante que, depois de qualquer batida, o conjunto continue andando. Mas repara na condição: sem força externa. Na granada, a gravidade é externa e faz trabalho, então a energia do centro de massa dela muda, sim, ao longo da parábola.

[thoughtful] Última pergunta da teoria. Até agora foram pontos. E um corpo inteiro, uma barra, uma chapa, uma esfera? A gente corta em pedacinhos de massa, cada um na sua posição, e soma. Quanto menores os pedaços, melhor. No limite, a soma vira uma integral: a posição do centro de massa é a integral da posição vezes o pedacinho de massa, dividida pela massa total.

[thoughtful] O pedacinho de massa depende do corpo. Num fio, é a densidade por comprimento vezes um pedacinho de comprimento. Numa chapa, a densidade por área vezes um pedacinho de área. Num sólido, a densidade vezes um pedacinho de volume.

[curious] Só que, muitas vezes, nem precisa integrar. Barra, disco, esfera uniformes: por simetria, o centro de massa está no centro. E olha o anel. Pela mesma simetria, o centro de massa fica no meio... onde não tem material nenhum.

Quando a simetria não resolve, entra a integral. Uma barra de dois metros que fica mais densa de uma ponta para a outra, com a densidade crescendo junto com a posição. Fazendo as duas integrais, o centro de massa fica a dois terços do comprimento: um vírgula trinta e três metros, mais perto da ponta pesada, como a intuição diria.

[thoughtful] Primeiro exercício. Uma placa quadrada e uniforme, de um metro de lado, da qual alguém recortou um triângulo em cima, com a ponta no centro do quadrado. Onde fica o centro de massa do que sobrou? Por simetria, ele está na vertical do meio, a meio metro da borda. Falta a altura. E dá para fazer de dois jeitos.

Primeiro jeito: o que sobrou se divide em três triângulos iguais, cada um com um quarto da área do quadrado. E o centro de massa de um triângulo uniforme fica na média dos três vértices. Trocando cada triângulo por uma partícula no centro dele, as alturas dão um sexto, meio e meio. Como as três massas são iguais, o centro de massa é a média simples das alturas: sete dezoito avos de metro, uns trinta e nove centímetros. Repara que ficou abaixo do meio: o recorte tirou massa de cima.

[curious] Segundo jeito, e esse é um truque de verdade: massa negativa. O que sobrou é o quadrado inteiro menos o triângulo. Então a gente conta o quadrado inteiro, com massa um e centro de massa no meio, e soma o triângulo com massa negativa. O triângulo tem um quarto da área, e o centro de massa dele está a cinco sextos de altura, na média dos vértices. Meio, menos um quarto vezes cinco sextos, dividido por três quartos. E sai, de novo... [short pause] sete dezoito avos. O mesmo ponto, por outro caminho.

[thoughtful] Guarda essa dica: um buraco funciona como massa negativa, e o centro de massa sempre foge do furo, para o lado onde sobrou mais material. E fica um desafio: um disco de um metro de raio, com um furo de meio metro de raio, cujo centro está a vinte e cinco centímetros do centro do disco. Onde fica o centro de massa? Usa a massa negativa e deixa a sua resposta nos comentários.

[curious] Segundo exercício. Um remador de setenta e cinco quilogramas está na popa de uma canoa de cento e cinquenta quilogramas e três metros, parada, com a proa encostada numa estaca. Ele esqueceu de amarrar a canoa. Então levanta, anda até a proa, e estica o braço: o braço dele alcança oitenta centímetros à frente da proa. Será que ele consegue pegar a estaca?

[thoughtful] Na horizontal, a água quase não faz força, então não tem força externa. E tudo começa parado. Então o centro de massa do sistema, remador mais canoa, não pode sair do lugar. Quando ele anda para a frente, a canoa tem que andar para trás, para longe da estaca.

[thoughtful] Vamos às contas. O remador anda três metros em relação à canoa, para trás no eixo. Mas, em relação à água, o deslocamento dele é esses três metros mais o que a canoa andou. O centro de massa fixo diz que a massa do remador vezes o deslocamento dele, mais a massa da canoa vezes o dela, dá zero. Resolvendo, a canoa anda um metro para longe da estaca, e o remador anda só dois metros em relação à água. Confere: setenta e cinco vezes dois é igual a cento e cinquenta vezes um.

[curious] Agora a resposta. A proa ficou a um metro da estaca, e o braço alcança oitenta centímetros. Faltam vinte centímetros. O certo era ter amarrado antes de levantar. E a dica que esse exercício deixa: o deslocamento em relação à canoa não é o deslocamento em relação à água. Quem está parado é o centro de massa, e é em relação à água que ele está parado.

[calm, satisfied] Então, voltando à pergunta do começo. Quando a granada explode, as forças da explosão são internas, e força interna não mexe no centro de massa. A única força externa é o peso total, e por isso o centro de massa segue a mesma parábola. A pergunta inicial está respondida.

Resumindo em quatro perguntas. Onde está: na média das posições, pesada pelas massas, e dá para fazer por partes, até com massa negativa. Como se move: como uma partícula com toda a massa do sistema, empurrada só pelas forças de fora. Que energia é relativa: a energia cinética se divide na do centro de massa, que só muda com força externa, e na do movimento relativo, que as forças internas podem criar, como na explosão, ou consumir, como na colisão. E num corpo inteiro: a soma vira integral, mas simetria primeiro.

[curious] E isso já diz muito sobre colisões. Dois blocos vêm um contra o outro, batem e grudam. A batida é interna, então o centro de massa nem percebe: segue reto, com a mesma velocidade. E, grudados, os dois só podem andar junto com ele. Então a velocidade final é a do centro de massa, a média das velocidades pesada pelas massas: [short pause] dois terços de metro por segundo. Agora olha a mesma batida andando junto com o centro de massa. Os dois chegam com momentos iguais e opostos, e param. Toda a energia relativa vira outra coisa, e a do centro de massa fica. É isso que a gente vai explorar no módulo de colisões.

[happy] Se esse ponto mudou o jeito como você vê uma explosão, se inscreve no Parallax Lab para acompanhar os próximos vídeos. Até a próxima!
