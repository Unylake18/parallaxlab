# yt_0017 — CENTRO DE MASSA · roteiro com narração v3.1 (sujeita a aprovação)

> v3 (2026-10-29, após o lote 1 v3 e a crítica do Kaio): o vídeo foi **dividido**. O yt_0017 fica com a teoria completa e dois exercícios ilustrativos (~19–20 min). Os exercícios difíceis (quadrado com furo, fio dobrado no cubo, naves no referencial do CM, rojão, gafanhoto, caixa de Einstein) vão para o vídeo seguinte, e o foguete vem depois dele.
> O que mudou em relação à v2.3: visual novo do hook e da granada (campo de provas em vácuo, granada de fragmentação que se estilhaça em cacos do próprio corpo, parábolas como gráfico); o ⊕ passou a ser **degradê ciano→magenta**; T1-8 novo (por partes); E1–E4 antigos saem e entram E1 placa com entalhe (dois caminhos, massa negativa) e E2 remador e estaca; síntese em quatro perguntas; EN2 com gancho para o vídeo de exercícios. HOOK → T2 mantém a fala da v2.3 (só "ponto branco" virou "ponto brilhando"); T3 e T4 mantêm a fala da v2 (sem o joão-bobo, que saiu com o E4 antigo).

Data: 2026-10-29. Título de trabalho: **Centro de massa: o ponto que uma explosão não consegue desviar**. Continua o yt_0016 (o EN2 dele promete a granada). Padrão: `padrao_video_longo.md` §5 e `roteiro_voz_elevenlabs_v4.md`. Tom de professor de cursinho, "a gente" e "você", nunca a letra solta.

**Como ler:** cada `###` é uma âncora (evento visual). A linha `tela:` diz o que aparece; a fala começa ~0,15 s depois e manda: a cena se estica. Tags `[ ]` do ElevenLabs v4, em inglês, **um só descritor**, uma por trecho, valendo até a próxima; não entram na legenda.

**Regras de tela da série (Kaio):** nada de livro na tela nem na fala (fontes só na descrição do YouTube); selo de ligação no lugar do selo de fonte; nunca tela só de álgebra (PALCO vivo enquanto a CONTA corre, variáveis saindo do desenho para a conta com TransformFromCopy); exercícios com esquema fixo à esquerda e álgebra à direita; nada de tempo morto.

**Cores (v3):** centro de massa ⊕ em **degradê ciano `#35D9FF` → magenta `#EA63FF`**, com halo e rastro em degradê com glow (assinatura do vídeo: nenhuma grandeza usa degradê); nas contas, R⃗_cm, X, Y em ciano-claro `#8BE9FF`; posições `GEO #B8C4DA`; velocidade violeta `#9C8CFF`; momento magenta `#EA63FF`; força `FC #5AA2FF`; impulso `JC #9CC7FF`; energia cinética ciano (só em barras); calor/energia química laranja `#FF7A3D`; corpos em aço `#7A8696` com luz B (recorte `#7FB2FF` + toque magenta); caixas `PANEL #0E2A52` com borda na cor da grandeza. Amarelo e verde não entram.
**Canto:** linha 1 `MECÂNICA · CENTRO DE MASSA`; linha 2 = capítulo. Os quatro blocos de teoria são **quatro perguntas**: onde está? como se move? que energia é do movimento relativo? como achar num corpo inteiro? Os dois exercícios testam a primeira e a segunda.

**Pausa útil × tempo morto:** numa transformação central (fórmula nascendo, termo cruzado zerando, ⊕ descolando da parábola, os dois caminhos do E1 caindo no mesmo ponto) uma pausa de 2–3 s é bem-vinda; o que não pode é tela parada sem informação nova por mais de ~4 s.

---

## HOOK

### H1 — tela: Three.js, CAMPO DE PROVAS EM VÁCUO (piso escuro com grade fina ciano até o horizonte, céu estrelado, brilho magenta baixo no horizonte); uma granada de fragmentação (corpo de aço escuro em gomos, cinta, alavanca) é lançada de um marco com luzes; câmera perto, acompanhando a subida; eixos x e y (m) acendem discretos; rastro fino e "fotos" fantasma a cada 0,5 s
[curious] Olha essa granada subindo. Sem resistência do ar, a gente sabe exatamente o caminho dela: uma parábola, a mesma de qualquer pedra jogada para cima.

### H2 — tela: no topo, as emendas entre os gomos acendem no degradê ciano→magenta; câmera lenta 0,5× por ~1 s; a granada se estilhaça em três cacos irregulares do próprio corpo (2, 1,5 e 1 kg; volumes proporcionais às massas), cada um girando; faíscas e fumaça sem massa somem em ~1 s; cada caco segue com rastro fino aço-azulado
Só que, lá no alto, ela explode. Três pedaços, de massas diferentes, voando cada um para um lado. Parece que a parábola acabou ali.

### H3 — tela: a câmera recua até a parábola inteira (eixos com marcas a cada 50 m); a parábola original aparece tracejada em branco a 50%; o ⊕ acende em degradê ciano→magenta sobre ela, com rastro em degradê e glow; pergunta centralizada SE A GRANADA EXPLODE NO MEIO DO VOO, O QUE CONTINUA NA PARÁBOLA?; congela 2 s antes do primeiro toque
[curious] Mas olha esse ponto brilhando. Os pedaços se espalham, e ele segue em cima da parábola, como se nada tivesse acontecido. Que ponto é esse? E por que a explosão não consegue mexer nele?

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: CENTRO DE MASSA · O PONTO QUE UMA EXPLOSÃO NÃO CONSEGUE DESVIAR; abaixo do título, pequena e a 25%, a granada se estilhaçando de novo no campo de provas
[thoughtful] Hoje o assunto é o centro de massa. E ele é a continuação direta do vídeo anterior.

### A3 — tela: PALCO: o cavalo e a pedra do vídeo anterior, com a fronteira tracejada, a corda em cinza (INTERNA) e as duas forças do chão em azul-claro; CONTA: dP⃗/dt = F⃗_ext, cada símbolo saindo do desenho
No vídeo anterior, a gente viu que, num sistema de vários corpos, as forças de dentro se cancelam aos pares. A taxa de variação do momento total só depende da força externa resultante. O cavalo anda porque o chão empurra, não porque a corda puxa.

### A4 — tela: o cavalo some; volta a granada no campo de provas, no enquadramento final do hook (grande, com eixos); a equação dP⃗/dt = F⃗_ext vai para o canto da CONTA e ganha ONDE?
[curious] Só que aquela equação fala do momento do sistema inteiro, e não diz onde. Hoje a gente vai achar um lugar para ela: um ponto que se move como se toda a massa estivesse ali e toda a força externa agisse ali.

## T1 — ONDE ESTÁ O CENTRO DE MASSA?

### T1-1 — tela: PALCO 2D, vista de cima (sem 3D: aqui ele não acrescenta nada): haltere com **as mesmas massas e a mesma proporção da régua do T1-2** (1 kg e 3 kg, separação 4: a leve a 3 unidades do ⊕, a pesada a 1), bolas de aço desenhadas em 2D com a luz B (gradiente radial, recorte `#7FB2FF`, toque magenta), girando em torno do ⊕ em degradê; rastros circulares finos aço-azulado de cada bola; selo pequeno CÂMERA ACOMPANHANDO O CENTRO DE MASSA; CONTA vazia com a pergunta ONDE ESTÁ?
[curious] Primeira pergunta: onde está o centro de massa? Olha esse haltere torto, com uma bola de três quilogramas e uma de um, girando. A câmera está acompanhando um ponto especial da haste, por isso ele parece parado. Cada bola dá a sua volta, mas é em torno desse ponto que tudo gira. E repara: ele fica bem mais perto da bola pesada.

### T1-2 — tela: o haltere para de girar **alinhado com a régua** e passa para a vista de perfil (mesma proporção: as bolas e o ⊕ não pulam de lugar); PALCO 2D: haste horizontal com régua de 0 a 4 m; 1 kg em x = 0 e 3 kg em x = 4 m; um apoio triangular desliza por baixo e a haste balança até parar equilibrada em x = 3 m; cotas 3 m e 1 m
Vamos achar esse ponto com números. Põe o mesmo haltere deitado sobre uma régua: a bola de um quilograma na posição zero, e a de três quilogramas a quatro metros. Onde a gente apoia a haste para ela ficar em equilíbrio? A três metros da leve, e a um metro da pesada.

### T1-3 — tela: cotas d₁ = 3 m e d₂ = 1 m saem da régua para a CONTA: m₁ d₁ = m₂ d₂ → 1 · 3 = 3 · 1; as setas de peso (azul-claro) nas bolas pulsam juntas
Por quê? É a regra da alavanca, a mesma da gangorra. A massa da leve vezes a distância dela até o apoio tem que ser igual à massa da pesada vezes a distância dela. Um vezes três, três vezes um. A massa grande, perto; a massa pequena, longe.

### T1-4 — tela: as distâncias viram (X − x₁) e (x₂ − X), com X sendo o apoio; CONTA: m₁ (X − x₁) = m₂ (x₂ − X) → m₁X − m₁x₁ = m₂x₂ − m₂X → m₁X + m₂X = m₁x₁ + m₂x₂ → X (m₁ + m₂) = m₁x₁ + m₂x₂ → X = (m₁x₁ + m₂x₂)/(m₁ + m₂) (cada passo com TransformByGlyphMap: abre parênteses, m₂X atravessa e troca de sinal, X em evidência, (m₁ + m₂) desce como divisor); caixa PANEL; substituição: (1·0 + 3·4)/4 = 3 m
[emphatic] Agora chama a posição do apoio de X e escreve as distâncias como diferenças de posição. Abre os parênteses, junta os dois termos com X do mesmo lado e põe o X em evidência... e aparece a fórmula do centro de massa: cada posição multiplicada pela sua massa, somadas, divididas pela massa total. É uma média das posições, só que pesada pelas massas. Colocando os números, dá três metros, exatamente o apoio.

### T1-5 — tela: a régua desliza para a esquerda (origem nova em x = −2 m); os números das posições mudam (2 e 6), a conta refaz e dá X = 5; o ⊕ fica parado na haste; selo pequeno: O NÚMERO MUDA, O PONTO NÃO
Repara numa coisa importante. Se a gente muda a origem da régua, todas as posições mudam, e o resultado da conta também muda. Mas o ponto na haste é o mesmo. O centro de massa é um lugar do sistema, não um número da régua.

### T1-6 — tela: PALCO: plano xy com três massas, 2 kg em (0, 0), 1 kg em (4, 0) e 1 kg em (2, 4), com setas de posição r⃗ᵢ em GEO saindo da origem (r⃗₁ = 0⃗ marcado na origem); CONTA: X = Σ mᵢxᵢ / M, Y = Σ mᵢyᵢ / M → R⃗_cm = Σ mᵢ r⃗ᵢ / M; números de cada massa saindo do desenho: Σ mᵢ r⃗ᵢ = 2(0, 0) + 1(4, 0) + 1(2, 4) = (6, 4) → R⃗_cm = (6, 4)/4 = (1,5; 1,0)
[thoughtful] Com muitos corpos, no plano ou no espaço, a ideia é a mesma, coordenada por coordenada. A coordenada horizontal do centro de massa é a média pesada das coordenadas horizontais; a vertical, das verticais; e a de profundidade, igual. Juntando tudo num vetor: a posição do centro de massa é a soma das massas vezes as posições, dividida pela massa total. Com essas três massas, a soma de massa vezes posição dá seis na horizontal e quatro na vertical. Dividindo pela massa total, quatro quilogramas, ele cai em um vírgula cinco e um metro.

### T1-7 — tela: Three.js: o plano do T1-6 vira uma bandeja de aço horizontal com as três massas, a câmera inclina para ~25°; um pino de aço sobe por baixo FORA do ⊕ e a bandeja tomba para o lado da massa maior; volta, pino exatamente no ⊕, bandeja parada; pesos em azul-claro; CONTA: Σ mᵢ (r⃗ᵢ − R⃗_cm) = Σ mᵢ r⃗ᵢ − M R⃗_cm = 0⃗; selo CENTRO DE GRAVIDADE; DICA: O CENTRO DE MASSA FICA MAIS PERTO DE ONDE ESTÁ A MAIOR PARTE DA MASSA
E é por isso que um corpo apoiado no centro de massa fica em equilíbrio. Apoia fora dele, e a chapa tomba para o lado onde tem mais massa. Apoia nele, e ela fica parada. Na conta: medindo cada posição a partir do centro de massa, a soma de massa vezes posição dá zero, porque é a soma de massa vezes posição menos a massa total vezes a posição do centro de massa. Com a gravidade igual em todo lugar, o peso de cada pedaço é proporcional à massa, e as alavancas dos pesos se compensam em todas as direções. Por isso ele também é chamado de centro de gravidade. Só se a gravidade mudasse de um ponto para outro do corpo é que os dois deixariam de coincidir.

### T1-8 — tela: PALCO: volta o plano do T1-6 (2 kg em (0, 0), 1 kg em (4, 0), 1 kg em (2, 4)); as duas massas de 1 kg se fundem numa partícula de 2 kg no ponto médio delas, (3, 2), com um segmento tracejado; depois o ⊕ aparece no meio do caminho entre as duas massas de 2 kg, em (1,5; 1,0), exatamente onde estava; CONTA: R⃗_cm = (M_I R⃗_I + M_II R⃗_II)/(M_I + M_II) → (2·(0, 0) + 2·(3, 2))/4 = (1,5; 1,0); selo POR PARTES
[curious] E tem um atalho que vai servir muito. Qualquer pedaço do sistema pode ser trocado por uma partícula só, com a massa daquele pedaço, sentada no centro de massa dele. Olha: as duas massas de um quilograma viram uma de dois, no ponto médio entre elas, em três e dois. Sobram duas massas de dois quilogramas, e o centro de massa fica no meio do caminho entre elas: de novo, um vírgula cinco e um. Por partes, dá o mesmo. E repara num detalhe: entre duas massas, o centro de massa divide a distância na razão inversa das massas. Massas iguais, bem no meio.

## T2 — COMO ELE SE MOVE?

### T2-1 — tela: PALCO, vista lateral: o mesmo haltere (1 kg e 3 kg) é jogado para cima girando; primeiro a câmera acompanha o ⊕ (o haltere só gira, como no T1-1); depois a câmera se afasta e revela que o ⊕ faz uma parábola limpa (rastro em degradê ciano→magenta, com glow) enquanto as bolas fazem curvas cheias de laços (rastros finos aço-azulado); rótulos TRANSLAÇÃO DO ⊕ e ROTAÇÃO EM TORNO DO ⊕ no desenho; CONTA: r⃗ᵢ = R⃗_cm + r⃗ᵢ′, com R⃗_cm (origem → ⊕) e r⃗ᵢ′ (⊕ → bola) desenhados
[curious] Segunda pergunta: como esse ponto se move? Lembra do haltere girando? Agora a câmera se afasta. O haltere foi jogado para cima, e as bolas fazem essas curvas cheias de laços. Mas o centro de massa faz uma parábola limpa, como uma pedra. São dois movimentos separados: o ponto andando, e o haltere girando em volta dele. Dá até para escrever isso: a posição de cada bola é a posição do centro de massa mais uma seta que só gira em volta dele.

### T2-2 — tela: PALCO: o haltere segue em loop lento; setas de velocidade das bolas (violeta) e a do ⊕, V⃗_cm; CONTA: M R⃗_cm = Σ mᵢ r⃗ᵢ → d/dt (M e mᵢ não mudam) → M V⃗_cm = Σ mᵢ dr⃗ᵢ/dt = Σ mᵢ v⃗ᵢ → V⃗_cm = Σ mᵢ v⃗ᵢ / M
[thoughtful] Para entender por quê, deriva a fórmula do centro de massa em relação ao tempo. Como as massas não mudam, a derivada passa para dentro da soma, e cada posição vira uma velocidade: a velocidade do centro de massa é a média das velocidades, pesada pelas massas.

### T2-3 — tela: CONTA: M V⃗_cm = Σ mᵢ v⃗ᵢ = P⃗ (os termos mᵢ v⃗ᵢ ficam magenta e se somam numa seta P⃗ magenta no ⊕); caixa: P⃗ = M V⃗_cm
[emphatic] E olha o que apareceu do lado direito. Massa vezes velocidade, somado para todos: é o momento total do sistema. Ou seja, o momento total é a massa total vezes a velocidade do centro de massa. É como se o sistema inteiro fosse uma partícula só, com toda a massa, sentada no centro de massa.

### T2-4 — tela: CONTA: M A⃗_cm = Σ mᵢ a⃗ᵢ = Σᵢ (F⃗ᵢ^ext + Σⱼ F⃗ᵢ₍ⱼ₎); as internas escritas em pares (F⃗₁₍₂₎ + F⃗₂₍₁₎) + (F⃗₁₍₃₎ + F⃗₃₍₁₎) + (F⃗₂₍₃₎ + F⃗₃₍₂₎), cada par recebe = 0⃗ no mesmo instante em que a mola dele acende e as setas de ação e reação aparecem nas duas massas; resultado: M A⃗_cm = F⃗_ext (caixa PANEL); PALCO: as três massas presas por molas, vibrando, o conjunto deslizando para a direita e o ⊕ com rastro reto
Derivando mais uma vez, aparece a aceleração. Massa vezes aceleração de cada partícula é a força resultante nela, e essa força tem duas partes: as internas, que as partículas fazem umas nas outras, e as externas. As internas vêm em pares de ação e reação: a força que a primeira faz na segunda é igual e contrária à que a segunda faz na primeira. Somando par por par, cada par dá zero. Sobra só isso: a massa total vezes a aceleração do centro de massa é igual à força externa resultante.

### T2-5 — tela: a caixa M A⃗_cm = F⃗_ext com o selo É O MESMO dP⃗/dt = F⃗_ext, AGORA COM UM LUGAR; o ponto de interrogação do A4 (ONDE?) some
[thoughtful] Repara que isso não é uma física nova. É a mesma equação do vídeo anterior, só que lida de outro jeito. Ela diz que o centro de massa se move como uma partícula de massa igual à do sistema, empurrada só pelas forças de fora. As forças de dentro podem fazer o que quiserem com as partes: no centro de massa, elas não chegam.

### T2-6 — tela: PALCO (Three.js, câmera frontal, céu do laboratório sem piso, selo VISTO DO CHÃO · NO ESPAÇO, SEM GRAVIDADE): a mesma granada, andando reto, se estilhaça nos mesmos três cacos do hook (massas 2, 1 e 1,5; direções 90°, 210° e 330° em relação ao ⊕); antes, P⃗ = M V⃗_cm (magenta) no ⊕; depois, as três setas mᵢ v⃗ᵢ em relação ao chão, saindo da borda de cada caco, deslizam e se somam ponta com ponta ao lado do ⊕ sobre a P⃗ de antes (tracejada); rótulos 2 KG, 1 KG, 1,5 KG; o ⊕ em degradê segue reto; CONTA: F⃗_ext = 0⃗ → V⃗_cm CONSTANTE
Primeiro, no espaço, longe de tudo, sem gravidade. Um corpo andando reto explode nos mesmos três pedaços do começo. A explosão é feita de forças internas, então o centro de massa nem percebe: continua reto, com a mesma velocidade. E olha o momento: antes, uma seta só. Depois, cada pedaço leva a sua parte, mas, somando as três setas ponta com ponta, volta exatamente a mesma seta de antes.

### T2-7 — tela: volta a granada no campo de provas, agora como gráfico (eixos x e y em m, marcas a cada 50 m, topo cotado (122,4; 81,6), fotos fantasma a cada 0,5 s); a seta do peso total M g⃗ (azul-claro) no ⊕; CONTA: F⃗_ext = M g⃗ → M A⃗_cm = M g⃗ → A⃗_cm = g⃗ (o M cancela, TransformByGlyphMap) → R⃗_cm(t) = R⃗₀ + V⃗₀ t + ½ g⃗ t²; o ⊕ sobre a parábola tracejada; resposta QUEM CONTINUA NA PARÁBOLA É O ⊕
[excited] Agora a granada. Durante o voo, sem ar, a única força externa é o peso de todos os pedaços juntos: a massa total vezes a gravidade. Então a massa total cancela, e a aceleração do centro de massa é a aceleração da gravidade, antes e depois da explosão. Integrando duas vezes, a posição dele é a posição inicial, mais a velocidade inicial vezes o tempo, mais meio de g vezes o tempo ao quadrado, sem nenhum termo da explosão. O centro de massa faz exatamente a mesma parábola que a granada inteira faria, exatamente como o haltere. A pergunta do começo está respondida: quem continua na parábola é o centro de massa.

### T2-8 — tela: a cena continua; o pedaço de 1 kg toca o chão (2,83 s depois da explosão) e fica parado; J⃗ do chão nele (azul-impulso, para cima e para trás); o ⊕ **não salta**: continua de onde estava, mas muda de direção e sai da parábola tracejada; CONTA (painel): J⃗ = m (0⃗ − v⃗) = 1 · (−4,02; 42,72) N·s → ΔV⃗_cm = J⃗/M = (−0,89; 9,49) m/s, com o triângulo V⃗_cm antes, V⃗_cm depois, ΔV⃗_cm; rótulo O CHÃO ENTROU NA CONTA
[curious] Mas cuidado com um detalhe. Isso vale enquanto nenhum pedaço encosta em nada. Quando o primeiro pedaço bate no chão e para, o chão dá um empurrão nele: é uma força externa nova. O centro de massa não pula de lugar, mas a velocidade dele muda nesse instante. E a conta é direta: o impulso do chão tira todo o momento do pedaço, a massa dele vezes a velocidade com que chegou. Dividindo pela massa total, sai a mudança na velocidade do centro de massa. Daí para a frente, ele sai da parábola.

### T2-9 — tela: PALCO: duas pessoas paradas num lago congelado, a 10 m, segurando uma corda; CONTA: X_cm = (60·0 + 40·10)/100 = 4 m; F⃗_ext = 0⃗ e V⃗_cm = 0⃗ → X_cm FIXO; elas puxam e deslizam uma para a outra; o ⊕ entre elas não se mexe e elas se encontram nele; depois, miniatura do Cyrano do vídeo anterior; selo DICA: O CENTRO DE MASSA SÓ ESCUTA A FORÇA EXTERNA
E, se não há força externa nenhuma, e o sistema começa parado, o centro de massa fica parado para sempre. Duas pessoas no gelo, a dez metros uma da outra, puxando uma corda. O centro de massa está em sessenta vezes zero mais quarenta vezes dez, dividido por cem: quatro metros da mais pesada. Ele não se mexe, então é exatamente ali que elas se encontram. E é por isso que a ideia do Cyrano, de jogar um ímã para cima para subir junto, nunca funciona: o centro de massa do conjunto não sobe.

## T3 — QUE ENERGIA É DO MOVIMENTO RELATIVO?

### T3-1 — tela: PALCO: a explosão no espaço de novo (os cacos da granada), **primeiro no laboratório**: tudo andando para a direita, setas de velocidade violeta em relação ao chão; rótulo VISTO DO CHÃO
[curious] Terceira pergunta, e ela é sobre energia. Olha a explosão de novo, vista do chão. Cada pedaço tem uma velocidade, e todas elas carregam um pedaço comum: o conjunto inteiro está andando para a direita.

### T3-2 — tela: PALCO: transição de referencial: a câmera passa a acompanhar o ⊕ (o ⊕ para no centro da tela); a seta comum V⃗_cm "sai" de todas as velocidades e fica no canto; sobram as velocidades relativas v⃗ᵢ′ (violeta clareado); rótulo VISTO DO CENTRO DE MASSA; CONTA: v⃗ᵢ = V⃗_cm + v⃗ᵢ′, cada seta saindo do desenho
[thoughtful] Agora a câmera passa a andar junto com o centro de massa. A parte comum some da tela, e sobra só o movimento de cada pedaço em relação ao centro de massa. Ou seja, a velocidade de cada pedaço é a velocidade do centro de massa mais a velocidade dele em relação ao centro de massa.

### T3-3 — tela: PALCO (visto do centro de massa): as três setas de momento **relativas ao CM** (magenta), de mesmo comprimento, saindo da borda dos pedaços; depois elas deslizam e, somadas ponta com ponta, fecham um triângulo; CONTA: Σ mᵢ v⃗ᵢ′ = Σ mᵢ v⃗ᵢ − M V⃗_cm = P⃗ − P⃗ = 0
Primeiro, um fato que você acabou de ver: nesse referencial, os pedaços se afastam de um ponto parado. E repara nas setas de momento, vistas daqui: as três têm o mesmo tamanho. Como saem separadas por ângulos iguais, só assim a soma dá zero, e por isso o pedaço mais leve é o que sai mais rápido. Agora a conta: somando massa vezes velocidade em relação ao centro de massa, dá o momento total menos a massa total vezes a velocidade do centro de massa. Mas isso é o momento menos ele mesmo: zero. Visto de cima do centro de massa, o momento do sistema é sempre zero.

### T3-4 — tela: CONTA: K = ½ Σ mᵢ (V⃗_cm + v⃗ᵢ′)² → ½ M V²_cm + V⃗_cm · Σ mᵢ v⃗ᵢ′ + ½ Σ mᵢ v′ᵢ²; o termo do meio acende, recebe o zero do passo anterior (TransformFromCopy) e some; caixa: K = ½ M V²_cm + K_rel, com a definição logo abaixo: K_rel = ½ Σ mᵢ |v⃗ᵢ − V⃗_cm|²; PALCO: duas barras ciano: K DO CENTRO DE MASSA e K RELATIVA
[emphatic] Agora a energia cinética. Abrindo o quadrado, aparecem três termos. O do meio carrega exatamente aquela soma que dá zero, então ele some. Sobra uma separação limpa: a energia cinética total é a energia do centro de massa andando, metade da massa total vezes a velocidade dele ao quadrado, mais a energia cinética do movimento relativo, dos pedaços em relação ao centro de massa. Repara: aqui é tudo energia de movimento. Não é a energia interna da termodinâmica, aquela das moléculas e das ligações químicas.

### T3-5 — tela: PALCO: replay da explosão (visto do chão); a barra K DO CENTRO DE MASSA (ciano) não muda; a barra K RELATIVA (ciano) nasce do zero no instante em que as emendas acendem; um reservatório laranja-escuro ENERGIA QUÍMICA esvazia ao mesmo tempo; rótulo ENERGIA QUÍMICA → K RELATIVA
Isso explica a explosão de um jeito novo. Parte da energia química guardada na granada vira energia cinética dos pedaços, uns em relação aos outros. A energia do centro de massa não muda por causa da explosão, porque a explosão é interna.

### T3-6 — tela: PALCO 2D: bloco de 2 kg a 6 m/s indo bater num bloco de 1 kg parado, e eles grudam; ao lado, uma barra empilhada: ANTES: 24 J (CENTRO DE MASSA) + 12 J (RELATIVA) = 36 J; DEPOIS: 24 J (CENTRO DE MASSA) + 12 J que saem da barra em laranja para DEFORMAÇÃO · AQUECIMENTO · SOM; CONTA: V_cm = 2·6/3 = 4 m/s; ½ M V²_cm = 24 J; K_rel = 12 J
[curious] E vale para as colisões também. Um bloco de dois quilogramas a seis metros por segundo bate num bloco de um quilograma parado, e eles grudam. A energia antes é trinta e seis joules. A do centro de massa, que anda a quatro metros por segundo com os três quilogramas, é vinte e quatro joules. Então a energia do movimento relativo é doze. Depois do choque, os blocos andam juntos, e sobram exatamente vinte e quatro. Os doze joules relativos deixaram de ser energia de movimento: viraram deformação, aquecimento, som. A colisão consumiu toda a energia relativa, e nada mais.

### T3-7 — tela: a barra de 24 J pisca e ganha um cadeado com o rótulo SEM FORÇA EXTERNA; miniatura da granada com a seta do peso e o rótulo COM GRAVIDADE, O CADEADO ABRE; selo DICA: NUMA COLISÃO, SÓ A ENERGIA RELATIVA PODE SE PERDER
Ou seja, sem força externa, uma colisão nunca pode perder mais do que a energia do movimento relativo. A energia do centro de massa fica trancada: é ela que garante que, depois de qualquer batida, o conjunto continue andando. Mas repara na condição: sem força externa. Na granada, a gravidade é externa e faz trabalho, então a energia do centro de massa dela muda, sim, ao longo da parábola.

## T4 — COMO ACHAR O CENTRO DE MASSA DE UM CORPO INTEIRO?

### T4-1 — tela: PALCO: uma barra uniforme dividida em 4, depois 8, depois 32 pedaços, cada um com um pontinho de massa e a seta de posição; CONTA: Σ mᵢ r⃗ᵢ / M → (1/M) ∫ r⃗ dm, com Δm virando dm (callback das somas de retângulos do vídeo sobre impulso)
[thoughtful] Última pergunta da teoria. Até agora foram pontos. E um corpo inteiro, uma barra, uma chapa, uma esfera? A gente corta em pedacinhos de massa, cada um na sua posição, e soma. Quanto menores os pedaços, melhor. No limite, a soma vira uma integral: a posição do centro de massa é a integral da posição vezes o pedacinho de massa, dividida pela massa total.

### T4-2 — tela: três ícones lado a lado: fio (dm = λ dℓ), chapa (dm = σ dA), sólido (dm = ρ dV), cada um com o elemento de massa acendendo
O pedacinho de massa depende do corpo. Num fio, é a densidade por comprimento vezes um pedacinho de comprimento. Numa chapa, a densidade por área vezes um pedacinho de área. Num sólido, a densidade vezes um pedacinho de volume.

### T4-3 — tela: barra, disco e esfera uniformes com o ⊕ no centro; depois um anel uniforme com o ⊕ no centro vazio, piscando; rótulo O CENTRO DE MASSA PODE FICAR FORA DO MATERIAL
[curious] Só que, muitas vezes, nem precisa integrar. Barra, disco, esfera uniformes: por simetria, o centro de massa está no centro. E olha o anel. Pela mesma simetria, o centro de massa fica no meio... onde não tem material nenhum.

### T4-4 — tela: barra de 2 m que vai do claro ao escuro (densidade crescente, λ = c x); CONTA: X = ∫₀ᴸ x · c x dx / ∫₀ᴸ c x dx = (L³/3)/(L²/2) = 2L/3 = 1,33 m; o ⊕ desliza do meio até 1,33 m; selo DICA: SIMETRIA PRIMEIRO. INTEGRAL SÓ PARA O QUE A SIMETRIA NÃO DIZ
Quando a simetria não resolve, entra a integral. Uma barra de dois metros que fica mais densa de uma ponta para a outra, com a densidade crescendo junto com a posição. Fazendo as duas integrais, o centro de massa fica a dois terços do comprimento: um vírgula trinta e três metros, mais perto da ponta pesada, como a intuição diria.

## E1 — PLACA COM ENTALHE (POR PARTES E MASSA NEGATIVA)

### E1-1 — tela: canto linha 2 EXERCÍCIO 1 · PLACA COM ENTALHE; selo POR PARTES: CADA PEDAÇO VIRA UMA PARTÍCULA; ESQUEMA (esquerda, fixo até o fim do exercício): placa quadrada de aço de 1 m de lado, cantos (0, 0), (1, 0), (1, 1), (0, 1); o triângulo de cima, com vértices (0, 1), (1, 1) e o centro (½, ½), sai da placa (recorte com borda tracejada e o vazio escuro); eixos x e y em GEO com marcas em ½ e 1; o eixo de simetria x = ½ acende tracejado; CONTA (direita): X = ½ m por simetria; Y = ?
[thoughtful] Primeiro exercício. Uma placa quadrada e uniforme, de um metro de lado, da qual alguém recortou um triângulo em cima, com a ponta no centro do quadrado. Onde fica o centro de massa do que sobrou? Por simetria, ele está na vertical do meio, em x igual a meio metro. Falta a altura. E dá para fazer de dois jeitos.

### E1-2 — tela: ESQUEMA: o que sobrou se divide em três triângulos iguais (embaixo, esquerda, direita), cada um com borda na cor de uma das massas da conta e área ¼ escrita dentro; em cada triângulo, os três vértices piscam e o centroide nasce na média deles: (½; ⅙), (⅙; ½), (⅚; ½), cada um virando uma partícula de massa ¼ (as placas somem, ficam as três partículas); CONTA: Y = (¼·⅙ + ¼·½ + ¼·½)/(¾) → (⅙ + ½ + ½)/3 → (7/6)/3 = 7/18 m ≈ 0,39 m (cada ¼ sai do triângulo dele com TransformFromCopy; o ¼ comum cancela com TransformByGlyphMap); o ⊕ em degradê acende em (½; 7/18)
Primeiro jeito: o que sobrou se divide em três triângulos iguais, cada um com um quarto da área do quadrado. E o centro de massa de um triângulo uniforme fica na média dos três vértices. Trocando cada triângulo por uma partícula no centro dele, as alturas dão um sexto, meio e meio. Como as três massas são iguais, o centro de massa é a média simples das alturas: sete dezoito avos de metro, uns trinta e nove centímetros. Repara que ficou abaixo do meio: o recorte tirou massa de cima.

### E1-3 — tela: ESQUEMA: os três triângulos se apagam; volta o quadrado inteiro (partícula de massa 1 em (½; ½), contorno ciano-claro) e, por cima, o triângulo recortado em magenta-escuro tracejado com o rótulo MASSA −¼ e o centroide dele em (½; ⅚); CONTA: Y = (M_□ Y_□ + M_△ Y_△)/(M_□ + M_△) → (1·½ + (−¼)·⅚)/(1 − ¼) → (½ − 5/24)/(¾) → (7/24)/(¾) = 7/18 m; o resultado cai **no mesmo ponto** do E1-2 (o ⊕ não pula; um anel pisca em volta dele); selo OS DOIS JEITOS DÃO O MESMO
[curious] Segundo jeito, e esse é um truque de verdade: massa negativa. O que sobrou é o quadrado inteiro menos o triângulo. Então a gente conta o quadrado inteiro, com massa um e centro de massa no meio, e soma o triângulo com massa negativa. O triângulo tem um quarto da área, e o centro de massa dele está a cinco sextos de altura, na média dos vértices. Meio, menos um quarto vezes cinco sextos, dividido por três quartos. E sai, de novo, sete dezoito avos. O mesmo ponto, por outro caminho.

### E1-4 — tela: ESQUEMA: a seta do centro do quadrado (½; ½) até o ⊕ (½; 7/18), rotulada FOGE DO FURO; selo DICA: BURACO = MASSA NEGATIVA. O CENTRO DE MASSA FOGE DO FURO; depois, à direita, miniatura do DESAFIO: disco de raio 1 m com furo de raio 0,5 m, centro do furo a 0,25 m do centro do disco; texto ONDE FICA O CENTRO DE MASSA? (sem resposta na tela)
[thoughtful] Guarda essa dica: um buraco funciona como massa negativa, e o centro de massa sempre foge do furo, para o lado onde sobrou mais material. E fica um desafio: um disco de um metro de raio, com um furo de meio metro de raio, cujo centro está a vinte e cinco centímetros do centro do disco. Onde fica o centro de massa? A resposta sai no próximo vídeo.

## E2 — REMADOR E ESTACA (O CENTRO DE MASSA NÃO SE MOVE)

### E2-1 — tela: canto linha 2 EXERCÍCIO 2 · REMADOR E ESTACA; selo SEM FORÇA EXTERNA, O CENTRO DE MASSA NÃO SE MOVE; ESQUEMA (esquerda, fixo): margem à esquerda com uma estaca; água lisa com reflexo leve; canoa 2D de perfil (3 m, 150 kg, aço), proa encostada na estaca, remador 2D limpo (silhueta de corpo inteiro, não boneco de palito; 75 kg) na popa; eixo x em GEO saindo da estaca para a direita (0 na estaca, 3 m na popa); o alcance do braço, 0,80 m à frente da proa, marcado por uma cota violeta-clara; CONTA: m = 75 kg · M_c = 150 kg · L = 3 m · ALCANCE = 0,80 m
[curious] Segundo exercício. Um remador de setenta e cinco quilogramas está na popa de uma canoa de cento e cinquenta quilogramas e três metros, parada, com a proa encostada numa estaca. Ele esqueceu de amarrar a canoa. Então levanta, anda até a proa, e estica o braço: o braço dele alcança oitenta centímetros à frente da proa. Será que ele consegue pegar a estaca?

### E2-2 — tela: ESQUEMA: o ⊕ do sistema remador + canoa acende em x = (75·3 + 150·1,5)/225 = 2 m, com uma linha vertical tracejada até a água; o remador anda até a proa e a canoa desliza para a direita ao mesmo tempo; o ⊕ e a linha **não se mexem**; duas setas de deslocamento em relação à água: remador (violeta, para a esquerda) e canoa (violeta, para a direita); CONTA: F⃗_ext,x = 0 e V_cm = 0 → X_cm FIXO
Na horizontal, a água quase não faz força, então não tem força externa. E tudo começa parado. Então o centro de massa do sistema, remador mais canoa, não pode sair do lugar. Quando ele anda para a frente, a canoa tem que andar para trás, para longe da estaca.

### E2-3 — tela: CONTA: Δx_r = −3 + Δx_c (deslocamento do remador em relação à água = em relação à canoa + o da canoa; o −3 sai da cota da canoa com TransformFromCopy) → m Δx_r + M_c Δx_c = 0 → 75 (−3 + Δx_c) + 150 Δx_c = 0 → 225 Δx_c = 225 → Δx_c = +1,0 m; Δx_r = −2,0 m; verificação: 75 · 2 = 150 · 1 (as duas setas do ESQUEMA ganham os valores 2,0 m e 1,0 m)
[thoughtful] Vamos às contas. O remador anda três metros em relação à canoa, para trás no eixo. Mas, em relação à água, o deslocamento dele é esses três metros mais o que a canoa andou. O centro de massa fixo diz que a massa do remador vezes o deslocamento dele, mais a massa da canoa vezes o dela, dá zero. Resolvendo, a canoa anda um metro para longe da estaca, e o remador anda só dois metros em relação à água. Confere: setenta e cinco vezes dois é igual a cento e cinquenta vezes um.

### E2-4 — tela: ESQUEMA: a proa agora está a 1,0 m da estaca; o braço estica 0,80 m e para; a distância que falta, 0,20 m, acende em laranja entre a mão e a estaca; CONTA: 1,0 m − 0,80 m = 0,20 m → NÃO ALCANÇA; selo DICA: DESLOCAMENTO EM RELAÇÃO À CANOA NÃO É DESLOCAMENTO EM RELAÇÃO À ÁGUA
[curious] Agora a resposta. A proa ficou a um metro da estaca, e o braço alcança oitenta centímetros. Faltam vinte centímetros. O certo era ter amarrado antes de levantar. E a dica que esse exercício deixa: o deslocamento em relação à canoa não é o deslocamento em relação à água. Quem está parado é o centro de massa, e é em relação à água que ele está parado.

## SÍNTESE

### S1 — tela: limpa; a granada se estilhaçando de novo no campo de provas (gráfico com eixos), os cacos, o peso total M g⃗ no ⊕ e o ⊕ em degradê sobre a parábola tracejada
[calm] Então, voltando à pergunta do começo. Quando a granada explode, as forças da explosão são internas, e força interna não mexe no centro de massa. A única força externa é o peso total, e por isso o centro de massa segue a mesma parábola. A pergunta inicial está respondida.

### S2 — tela: as quatro perguntas entram uma a uma, cada uma com seu desenho pequeno no PALCO e a fórmula colorida: ONDE ESTÁ? (bandeja + placa com entalhe) R⃗_cm = Σ mᵢ r⃗ᵢ / M · COMO SE MOVE? (granada + canoa) M A⃗_cm = F⃗_ext · QUE ENERGIA É RELATIVA? (barras) K = ½ M V²_cm + K_rel · CORPO INTEIRO? (barra λ = cx) R⃗_cm = (1/M) ∫ r⃗ dm
Resumindo em quatro perguntas. Onde está: na média das posições, pesada pelas massas, e dá para fazer por partes, até com massa negativa. Como se move: como uma partícula com toda a massa do sistema, empurrada só pelas forças de fora. Que energia é relativa: a energia cinética se divide na do centro de massa, que só muda com força externa, e na do movimento relativo, que as forças internas podem criar, como na explosão, ou consumir, como na colisão. E num corpo inteiro: a soma vira integral, mas simetria primeiro.

## ENCERRAMENTO

### EN1 — tela: FadeOut geral; logo com anéis; INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
Se esse ponto mudou o jeito como você vê uma explosão, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### EN2 — tela: selo DO VÍDEO DE COLISÕES EM 1D; a cena C04 do vídeo de colisões (re-renderizada a partir do código daquele vídeo, mesma cor e notação: 2 kg a +2 m/s, 1 kg a −2 m/s, eles grudam e seguem a +⅔ m/s); **agora com o ⊕ em degradê** em x_cm = (2x₁ + 1x₂)/3, andando a ⅔ m/s **o tempo todo**, antes, durante e depois da batida, com rastro em degradê; a fórmula daquele vídeo v_f = (m₁v₁ᵢ + m₂v₂ᵢ)/(m₁ + m₂) aparece e ganha embaixo "= V_cm" (TransformByGlyphMap), com V_cm violeta; selo JÁ ESTÁ NO CANAL: COLISÕES EM 1D (cartão final do YouTube no mesmo canto)
[curious] E lembra do vídeo de colisões, quando os dois blocos batem e grudam? A velocidade final era uma média ponderada das velocidades, pesada pelas massas. Agora ela tem nome: é a velocidade do centro de massa. Ele já andava assim antes da batida, e continua igual depois, porque a batida é interna. Se você ainda não viu, o vídeo de colisões em uma dimensão já está no canal.

### EN3 — tela: três prévias rápidas (~1,5 s cada), no visual do vídeo: (1) a placa quadrada com um furo redondo fora do centro e o ⊕ fugindo do furo; (2) Three.js: um fio dobrado em três arestas de um cubo, girando devagar, com o ⊕ em degradê **flutuando fora do fio**, dentro do cubo; (3) um gafanhoto 2D saltando de uma folha que recua na água; depois, PRÓXIMO VÍDEO: CENTRO DE MASSA · EXERCÍCIOS (ciano)
[excited] E no próximo vídeo, só exercícios, e dos difíceis. A placa com um furo redondo, o fio dobrado nas arestas de um cubo, com o centro de massa flutuando fora do fio, e um gafanhoto que salta de uma folha boiando, enquanto a folha foge dele. E a resposta do desafio do disco. Até a próxima!

---

**Palavras faladas (sem tags e sem as linhas `tela:`):** ~3.070. No ritmo medido no lote 1 v4 (2,7 palavras/s: 1.507 palavras em 9:18), o vídeo inteiro dá **~19 min** (lote 1 9:18 + lote 2 T3–T4 ~4:20 + lote 3 E1–EN ~5:20). Tags por bloco no texto. Se passar de 21 min, corte nesta ordem: (1) barra com λ = cx do T4-4; (2) T3-6/T3-7 (colisão 24 + 12 J).

**Pontos a confirmar antes da voz:** (1) K_rel × "energia interna" (T3-4) — mantida a distinção falada; (2) número e título do vídeo de exercícios e do foguete (EN2 não fala números).

## Números de conferência (g = 9,8 m/s²)

| Bloco | Valor falado / na tela | Exato |
|---|---|---|
| Hook / T2-7 | lançamento (30; 40) m/s; topo (122,4; 81,6) m em 4,08 s; alcance 244,9 m (só na tela) | (122,45; 81,63); 4,082 s; 244,90 m |
| H2 / T2-6 | cacos 2, 1,5 e 1 kg (M = 4,5 kg); momentos relativos iguais, a 90°, 210° e 330° | — |
| T1 | 3 m e 1 m; X = 5 com a origem em −2; (1,5; 1,0) m | 3,0; 5; (1,5; 1,0) |
| T1-8 | 2 kg em (3, 2); (2·(0, 0) + 2·(3, 2))/4 = (1,5; 1,0) | ✓ |
| T2-8 | 2,83 s depois da explosão; J⃗ = (−4,02; 42,72) N·s; ΔV⃗_cm = (−0,89; 9,49) m/s (só na tela) | 2,829 s |
| T2-9 | 60 kg e 40 kg a 10 m; X_cm = 4 m | 4 |
| T3 | 36 J; 4 m/s; 24 J; 12 J | 36; 4; 24; 12 |
| T4 | 1,33 m | 2L/3 com L = 2 |
| E1 | x = ½ m; Y = 7/18 m ≈ 39 cm; centroides (½; ⅙), (⅙; ½), (⅚; ½); recorte (½; ⅚), área ¼ | 0,3889 |
| E1 desafio | não falar a resposta: ⊕ a 1/12 m ≈ 8,3 cm do centro, do lado oposto ao furo | −0,25·0,25/0,75 = −1/12 |
| E2 | X_cm = 2 m; canoa +1,0 m; remador −2,0 m; faltam 20 cm | 75·3/225 = 1,0 |
| EN2 | 2 kg a +2 m/s e 1 kg a −2 m/s (exemplo do vídeo de colisões); V_cm = v_f = ⅔ m/s (só na tela) | (2·2 − 1·2)/3 = 0,667 |

## Fontes (só para a descrição do YouTube)
Sears, Física I, 14ª ed., §8.5 (centro de massa); Moysés Nussenzveig, Curso de Física Básica 1, cap. 8 (centro de massa, substituição por partes); Feynman, Lições de Física I, cap. 19. Números dos exemplos: construção do Parallax Lab.
