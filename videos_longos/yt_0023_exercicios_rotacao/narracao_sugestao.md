# ANEXO A · roteiro com narração v1 (fonte do `ancoras.json`)

Data: 2026-11-07. Narração **v1.1** (v1 + revisão técnica do GPT), ~4.930 palavras ≈ 30 min (62 âncoras; hook ≈ 34 s). A duração é estimativa; a voz mede.
Título: **Dinâmica da rotação: 4 problemas em que o momento de inércia decide tudo.**
Padrão: `padrao_video_longo.md` §5 e `roteiro_voz_elevenlabs_v4.md`. Tom de professor de cursinho, "a gente" e "você", nunca a letra solta (o símbolo é apresentado uma vez, depois só o nome). Números por extenso como serão falados; a tela pode ter mais casas.
Frase-guia: **começa pela física: identifica as forças, escolhe o eixo, escreve as equações, aplica os vínculos e confere.**

**Como ler:** cada `###` é uma âncora (evento visual). A linha `tela:` diz o que aparece; a fala começa ~0,15 s depois e manda: a cena se estica. Tags `[ ]` do ElevenLabs v4 em inglês, uma por trecho; não entram na legenda.

## HOOK

### H1 · tela: Three.js, carretel em 3/4 com os dois tambores e os enrolamentos opostos visíveis; bloco de 6,0 kg pendurado do tambor grande (direita) e de 10,0 kg do tambor pequeno (esquerda), parados; uma trava fina no carretel; rótulos rosa `6,0 kg` e `10,0 kg`; selo `QUAL DESCE?`
[curious] Dois blocos presos a um carretel que gira sem atrito. Seis quilos no tambor grande, dez no pequeno, com os fios enrolados em sentidos opostos. Quando eu soltar, qual dos dois desce? Apostou no mais pesado?

### H2 · tela: a trava sai; o bloco de 6 kg desce, o de 10 kg sobe, o carretel gira (faixa clara girando); rastros finos dos blocos; hold de 2 s no fim com os dois blocos já separados
[thoughtful] Olha o que acontece: o de seis quilos desce, e o de dez sobe. Sem motor, sem empurrão, sem truque.

### H3 · tela: a cena congela; acima, a pergunta `COMO O MAIS LEVE VENCE O MAIS PESADO?`; três etiquetas pequenas surgem perto dos objetos: `TORQUE` (carretel), `MOMENTO DE INÉRCIA` (carretel), `VÍNCULO` (fios)
[curious] Como o mais leve vence o mais pesado? A explicação está na geometria das forças e na inércia de quem gira. Hoje a gente resolve quatro problemas de rotação, montando as equações e conferindo cada resposta.

## ABERTURA

### A1 · tela: logo; `BEM-VINDOS AO PARALLAX LAB`
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab.

### A2 · tela: `DINÂMICA DA ROTAÇÃO: 4 PROBLEMAS EM QUE O MOMENTO DE INÉRCIA DECIDE TUDO`; abaixo, `NESTE VÍDEO:` e quatro ícones com rótulo: volante (`O VOLANTE`), haste com eixo (`A HASTE E O EIXO`), carretel (`O CARRETEL`), pêndulo de disco (`O PÊNDULO MAIS RÁPIDO`), cada um acendendo na palavra
[thoughtful] Os quatro problemas de hoje. Primeiro, um volante com um bloco pendurado, resolvido do começo ao fim, item por item, conferindo cada passo. Depois, uma haste que cai presa fora do centro, e a força que o eixo faz nela durante a queda. Em seguida, o carretel do começo. E por fim, um pêndulo de disco: onde colocar o eixo para ele oscilar o mais rápido possível?

### A3 · tela: canto linha 2 `CAIXA DE FERRAMENTAS`; disco de aço girando à esquerda; à direita, cinco cartões `PANEL` entrando um a um na palavra: `I = Σ m r²` · `I = I_cm + M d²` · `Σ τ_ext = I α` · `K = ½ I ω²` · `v = ω r · a_t = α r · a_c = ω² r`; cada cartão acende sua marca no disco
[thoughtful] Antes de começar, a caixa de ferramentas. O momento de inércia: a soma de cada massa vezes a sua distância ao eixo, ao quadrado. O teorema dos eixos paralelos, para trocar de eixo: o momento de inércia em torno do centro de massa, mais a massa total vezes a distância entre os eixos, ao quadrado. A segunda lei da rotação: a soma dos torques externos é igual ao momento de inércia vezes a aceleração angular. A energia cinética de rotação: metade do momento de inércia vezes a velocidade angular ao quadrado. E as pontes entre o giro e cada ponto do corpo: a velocidade é a velocidade angular vezes o raio, a aceleração tangencial é a aceleração angular vezes o raio, e a centrípeta é a velocidade angular ao quadrado vezes o raio. Com essas cinco, dá para fazer tudo de hoje.

## O DESAFIO DA RÉGUA

### D1 · tela: canto linha 2 `O DESAFIO DA RÉGUA`; Three.js, a régua de 1,0 m na dobradiça, com uma massa rosa `M` presa na ponta e a moeda em cima; linha `HIPÓTESES: MOEDA LEVE · DOBRADIÇA SEM ATRITO`; selo `A PONTA AINDA ACELERA MAIS QUE g?`
[curious] E já que a caixa está aberta, vamos usar logo. No vídeo sobre torque ficou um desafio: prender na ponta da régua uma massa igual à da própria régua, com a moeda em cima. A moeda é leve: ela só serve para mostrar se a régua foge dela. E a dobradiça continua sem atrito. A ponta ainda acelera mais que a gravidade?

### D2 · tela: setas azuis de peso no meio da régua e na ponta, braços `L/2` e `L` em GEO; CONTA: τ = Mg·L/2 + Mg·L = 3MgL/2 → I = ML²/3 + ML² = 4ML²/3 → α = τ/I = 9g/(8L) → a_ponta = α L = 9g/8
[thoughtful] O torque agora tem dois pesos. O da régua, aplicado no meio, com braço de metade do comprimento. E o da massa extra, na ponta, com braço do comprimento inteiro. Somando, três meios do peso vezes o comprimento. O momento de inércia também ganha a massa extra: um terço da massa vezes o comprimento ao quadrado, da régua, mais a massa vezes o comprimento ao quadrado, da ponta. Quatro terços, no total. Dividindo o torque pelo momento de inércia, a aceleração angular dá nove oitavos da aceleração da gravidade sobre o comprimento. E a ponta acelera isso vezes o comprimento: nove oitavos da gravidade.

### D3 · tela: largada em câmera lenta, a moeda se separa da ponta, mas pouco; barra a(r) de 0 a 9g/8 com a marca `8L/9` onde a_t = g (a marca antiga `2L/3` aparece apagada e desliza até `8L/9`); selo `CONFERE: 9/8 > 1`
[thoughtful, emphatic] Ou seja: ainda passa da gravidade, mas por pouco, só um oitavo. A massa na ponta aumentou o torque, só que aumentou ainda mais o momento de inércia, porque está longe do eixo. Antes, a ponta chegava a três meios da gravidade. Agora, nove oitavos. E o ponto em que a aceleração tangencial iguala a gravidade foi de dois terços para oito nonos do comprimento. A moeda ainda fica para trás, só que bem menos.

## E1 · O VOLANTE

### E1-1 · tela: canto linha 2 `EXERCÍCIO 1 · O VOLANTE`; ESQUEMA 3D fixo: o volante (anel, cubo, quatro raios, dois discos pequenos, tambor leve, fio, bloco de 10 kg); os dados nascem nas peças: `15 kg · R₁ = 0,30 m · R₂ = 0,40 m` (anel), `3,0 kg · 0,10 m` (cubo), `1,0 kg · 0,05 m · a 0,25 m` (discos), `r = 0,15 m` (tambor), `m = 10 kg` (bloco); trilha de itens no rodapé `a · b · c · d · e · f`
[thoughtful] Exercício um, o volante. Ele gira em torno de um eixo fixo horizontal e tem três partes. Um anel grosso de quinze quilos, com raio interno de trinta centímetros e externo de quarenta. Um cubo central, que é um disco maciço de três quilos e dez centímetros de raio. E dois discos pequenos de um quilo cada, com cinco centímetros de raio, presos em lados opostos, com os centros a vinte e cinco centímetros do eixo. Na frente do cubo tem um tambor leve, de quinze centímetros de raio, com um fio enrolado que segura um bloco de dez quilos. O bloco é solto do repouso.

### E1-2 · tela: selo `O QUE ESTE PEDE: I · a, α, T · O GIRO EM 1,5 s · A ENERGIA · O FREIO · O ARO`; depois linha `HIPÓTESES: EIXO SEM ATRITO · FIO LEVE, SEM ESTICAR NEM ESCORREGAR · RAIOS E TAMBOR SEM MASSA · g = 9,8 m/s²`
[curious] O que a gente quer? O momento de inércia do volante. A aceleração do bloco e a tração no fio. Quanto tudo gira em um segundo e meio. Para onde vai a energia. E o que acontece quando um freio entra em ação. As hipóteses: eixo sem atrito, fio leve que não estica nem escorrega no tambor, raios e tambor de massa desprezível, e a aceleração da gravidade de nove vírgula oito metros por segundo ao quadrado.

### E1-3 · tela: item `a` acende; o anel se destaca: nasce como disco cheio de 0,40 m e o miolo de 0,30 m sai (rosa translúcido); CONTA: σ = M/[π(R₂² − R₁²)] → I_anel = ½σπR₂⁴ − ½σπR₁⁴ = ½σπ(R₂² − R₁²)(R₂² + R₁²) = ½M(R₁² + R₂²) = ½ · 15 · (0,09 + 0,16) = 1,875 kg·m²
[thoughtful] Item a, o momento de inércia. Começa pelo anel, que é a peça mais importante. Um jeito bonito de ver: o anel é um disco cheio de quarenta centímetros, menos um disco de trinta que foi recortado do meio. A massa do anel está espalhada por igual na área dele, então a densidade por área é a massa do anel dividida pela área do anel. O momento de inércia de um disco é metade da massa vezes o raio ao quadrado, e a massa de cada disco é essa densidade vezes a área dele, que cresce com o raio ao quadrado. Fazendo a subtração e fatorando, sobra metade da massa do anel vezes a soma dos dois raios ao quadrado. Com os números: metade de quinze, vezes zero vírgula zero nove mais zero vírgula dezesseis. Dá um vírgula oito sete cinco quilograma metro quadrado.

### E1-4 · tela: selo `CONFERE: R₁ → 0 ⇒ ½MR² (DISCO) · R₁ → R₂ ⇒ MR² (ARO)`; o cubo e os discos pequenos se destacam; cota GEO de 0,25 m do eixo ao centro de um disco pequeno; CONTA: I_cubo = ½ · 3,0 · 0,10² = 0,015; I_disco = ½ · 1,0 · 0,05² + 1,0 · 0,25² = 0,06375 → dois discos: 0,1275
[thoughtful] Confere rápido. Se o furo some, raio interno zero, volta o disco: metade da massa vezes o raio ao quadrado. Se o anel fica fininho, com os dois raios iguais, vira massa vezes raio ao quadrado, o momento de inércia de um aro. A fórmula passa nos dois testes. Agora o cubo, um disco maciço: metade de três, vezes zero vírgula um ao quadrado, zero vírgula zero um cinco. E os discos pequenos, que não estão no eixo. Aqui entra o teorema dos eixos paralelos. Cada um tem metade de um quilo vezes cinco centímetros ao quadrado em torno do próprio centro, mais um quilo vezes vinte e cinco centímetros ao quadrado, pelo deslocamento. Os dois juntos: zero vírgula um dois sete cinco.

### E1-5 · tela: as três parcelas voam para a soma: I = 1,875 + 0,015 + 0,1275 = 2,0175 kg·m² (caixa rosa); duas barras horizontais lado a lado: `MASSA` (anel 75% · cubo 15% · discos 10%) e `I` (anel 92,9% · discos 6,3% · cubo 0,7%); selo `SEM M d²: 0,0025 (51× MENOS)`; item `a` ganha ✓; hold de 2 s
[thoughtful, emphatic] Somando tudo: dois vírgula zero dois quilograma metro quadrado. E repara no peso de cada parte. O anel tem três quartos da massa e responde por quase noventa e três por cento do momento de inércia. O cubo tem quinze por cento da massa e quase não conta. E os discos pequenos: sem o termo do deslocamento, dariam só zero vírgula zero zero dois cinco. Com ele, cinquenta e uma vezes mais. Massa longe do eixo é a que pesa no giro.

### E1-6 · tela: item `b` acende; bloco e volante se separam no ESQUEMA (o fio vira duas setas T); no bloco: peso `mg` para baixo e `T` para cima; no tambor: `T` tangente na borda, braço `r` em GEO; no centro: peso do volante e força do eixo com o rótulo `BRAÇO ZERO`
[thoughtful] Item b: a aceleração. Primeiro passo, sempre: separa os corpos. No bloco, duas forças: o peso, para baixo, e a tração do fio, para cima. No volante, a tração puxa a borda do tambor para baixo, com braço igual ao raio do tambor. O peso do volante e a força do eixo também atuam, mas passam pelo eixo: braço zero, torque zero. Por isso eles nem entram na equação da rotação.

### E1-7 · tela: CONTA, três linhas com rótulos à esquerda: `BLOCO: mg − T = m a` · `VOLANTE: T r = I α` · `VÍNCULO: a = α r`; cada termo voa do diagrama
[thoughtful] Então, três equações. Para o bloco, a segunda lei de Newton: o peso menos a tração é igual à massa do bloco vezes a aceleração. Para o volante, a segunda lei da rotação: a tração vezes o raio do tambor é igual ao momento de inércia vezes a aceleração angular. E o vínculo: como o fio não escorrega, a aceleração do bloco é a aceleração angular vezes o raio do tambor. É o vínculo que amarra a translação com a rotação.

### E1-8 · tela: CONTA: T = I α / r → T = I a / r² → mg − I a / r² = m a → a (m + I/r²) = mg → a = g / (1 + I/(m r²)) (caixa verde)
[curious] Agora a álgebra. Da equação do volante, a tração é o momento de inércia vezes a aceleração angular, dividido pelo raio. Trocando a aceleração angular pelo vínculo, fica momento de inércia vezes aceleração, sobre o raio ao quadrado. Coloca isso na equação do bloco, junta os termos com a aceleração e divide. Sai uma fórmula que vale guardar: a aceleração é a gravidade dividida por, um mais o momento de inércia sobre a massa do bloco vezes o raio do tambor ao quadrado.

### E1-9 · tela: selo `CONFERE: I → 0 ⇒ a = g · I → ∞ ⇒ a → 0`; depois o bloco fantasma rosa translúcido aparece numa moldura de comparação ao lado, **sem fio**: `INÉRCIA EQUIVALENTE I/r² ≈ 90 kg · NÃO É PESO EXTRA`; CONTA: I/r² = 2,0175 / 0,0225 ≈ 89,7 kg; hold de 2 s
[thoughtful] E essa fórmula conta uma história. Se o volante não tivesse inércia nenhuma, o termo some e a aceleração é a da gravidade: queda livre. Se o momento de inércia fosse enorme, a aceleração vai a zero, e o bloco mal se mexe. E tem um jeito ainda mais concreto de ler: o momento de inércia dividido pelo raio ao quadrado é uma inércia equivalente. Aqui, dois vírgula zero dois sobre zero vírgula zero dois dois cinco: quase noventa quilos. O volante tem vinte quilos, mas resiste à aceleração como noventa quilos andando em linha reta. Cuidado: não é uma massa extra puxando o fio. Quem puxa continua sendo só o peso do bloco. O giro acrescenta inércia, não força.

### E1-10 · tela: CONTA: a = 9,8 / (1 + 8,97) = 0,983 m/s² → α = a/r = 6,56 rad/s² → T = m (g − a) = 88,2 N; selo `CONFERE: T < mg = 98 N · T r = 13,2 N·m = I α`; setas no ESQUEMA crescem para os valores; item `b` ganha ✓
[thoughtful] Os números. A aceleração do bloco dá zero vírgula nove oito metro por segundo ao quadrado, um décimo da gravidade. Dividindo pelo raio do tambor, a aceleração angular: seis vírgula cinco seis radianos por segundo ao quadrado. E a tração: a massa do bloco vezes, a gravidade menos a aceleração. Oitenta e oito vírgula dois newtons. Confere: é menos que o peso do bloco, noventa e oito newtons, como deve ser, porque o bloco desce acelerando. E a tração vezes o raio dá treze vírgula dois newtons metro, exatamente o momento de inércia vezes a aceleração angular.

### E1-11 · tela: item `c` acende; simulação real de 0 a 1,5 s: o volante gira, o contador âmbar sobe até 7,37 rad / 1,17 volta, a régua GEO marca 1,11 m ao lado do bloco; CONTA: ω = α t = 9,83 rad/s → Δθ = ½ α t² = 7,37 rad = 1,17 volta → h = r Δθ = 1,11 m → v = r ω = 1,47 m/s; item `c` ganha ✓
[thoughtful] Item c: o que acontece em um segundo e meio. A aceleração angular é constante, então é cinemática angular pura. A velocidade angular é a aceleração angular vezes o tempo: nove vírgula oito três radianos por segundo. O ângulo girado é metade da aceleração angular vezes o tempo ao quadrado: sete vírgula três sete radianos, um pouco mais de uma volta. E o bloco desce esse ângulo vezes o raio do tambor: um vírgula um um metro, chegando a um vírgula quatro sete metro por segundo.

### E1-12 · tela: um ponto na borda do anel (0,40 m) com seta verde a_t (tangente, com inset `ZOOM ×4`) e seta verde a_c (para o eixo); ângulo âmbar de 3,9° entre a soma e o raio; CONTA: a_t = α R₂ = 2,62 m/s² · a_c = ω² R₂ = 38,7 m/s² ≈ 3,9 g
[curious] Uma conferência rápida: um ponto na borda do anel, a quarenta centímetros do eixo. A aceleração tangencial é a aceleração angular vezes o raio: dois vírgula seis dois metros por segundo ao quadrado. A centrípeta é a velocidade angular ao quadrado vezes o raio: trinta e oito vírgula sete, quase quatro vezes a gravidade. Ou seja, a aceleração total quase não sai da direção do raio: só uns quatro graus.

### E1-13 · tela: item `d` acende; três barras ciano: `mgh = 108,4 J` (cheia) e, abaixo, `K_vol = 97,5 J` (90%) + `K_bloco = 10,9 J` (10%) se encaixando nela; CONTA: m g h = 10 · 9,8 · 1,11 = 108,4 J; K_bloco = ½ m v² = 10,9 J; K_vol = ½ I ω² = 97,5 J; 10,9 + 97,5 = 108,4 ✓; K_vol/K_bloco = I/(m r²) = 8,97; hold de 2 s
[thoughtful, emphatic] Item d: a energia. Esse é o grande teste da resolução inteira. O peso do bloco realizou um trabalho de massa vezes gravidade vezes altura: cento e oito vírgula quatro joules. Para onde foi isso? A energia cinética do bloco, metade da massa vezes a velocidade ao quadrado, dá dez vírgula nove joules. A energia cinética de rotação do volante, metade do momento de inércia vezes a velocidade angular ao quadrado, dá noventa e sete vírgula cinco. Somando: cento e oito vírgula quatro. Fecha! E repara: o volante ficou com quase nove vezes a energia do bloco. É a mesma razão entre a massa equivalente e a massa do bloco. Noventa por cento da energia foi para o giro.

### E1-14 · tela: gráfico P(t) ao lado das barras: reta de 0 a 130 W em 1,5 s; a área do triângulo se pinta em ciano; CONTA: P = T v = τ ω = 130 W → K_vol = ½ P t = ½ · 130 · 1,5 = 97,5 J; item `d` ganha ✓
[thoughtful] E de onde vem a energia do volante, instante a instante? Do fio. A potência que o fio entrega é a tração vezes a velocidade do fio, que é o mesmo que o torque vezes a velocidade angular. Em um segundo e meio, cento e trinta watts. Como essa potência cresce em linha reta com o tempo, a energia acumulada é a área do triângulo: metade de cento e trinta vezes um e meio. Noventa e sete vírgula cinco. Bate de novo.

### E1-15 · tela: item `e` acende; o fio se solta e o bloco sai pelo rodapé; a pastilha de freio encosta no topo da borda do anel; setas azuis `N = 25 N` (para o eixo) e `f_at = 10 N` (tangente, contra o giro); dado `μ_c = 0,40`; CONTA: f_at = μ_c N = 0,40 · 25 = 10 N → τ = f_at R₂ = 10 · 0,40 = 4,0 N·m; rótulo `N: BRAÇO ZERO`
[curious] Item e: o freio. Nesse instante o fio se solta, e uma pastilha encosta na borda do anel, apertando com vinte e cinco newtons. O coeficiente de atrito cinético entre a pastilha e o anel é zero vírgula quatro. A força de atrito é esse coeficiente vezes a normal: dez newtons, tangente à borda, contra o giro. O torque dela é dez newtons vezes quarenta centímetros: quatro newtons metro. E a normal? Ela aponta direto para o eixo. Braço zero, torque zero.

### E1-16 · tela: o volante desacelera até parar, **em tempo real**; o contador âmbar sobe até 24,4 rad / 3,88 voltas; barra ciano `K_vol` esvaziando enquanto a barra laranja `CALOR (FREIO + VOLANTE)` enche, a pastilha e a borda do anel brilhando em laranja fraco; CONTA: α_f = τ / I = 1,98 rad/s² → t = ω / α_f = 4,96 s → Δθ = ω² / (2 α_f) = 24,4 rad ≈ 3,9 voltas → W = τ Δθ = 97,5 J = K_vol ✓; item `e` ganha ✓
[thoughtful] A desaceleração angular é o torque sobre o momento de inércia: um vírgula nove oito radiano por segundo ao quadrado. Para zerar nove vírgula oito três radianos por segundo, leva quatro vírgula nove seis segundos. E o ângulo até parar sai da versão angular da equação de Torricelli: a velocidade angular ao quadrado sobre duas vezes a desaceleração. Vinte e quatro vírgula quatro radianos, quase quatro voltas. Confere pela energia: o trabalho do atrito é o torque vezes o ângulo, quatro vezes vinte e quatro vírgula quatro, noventa e sete vírgula cinco joules. Exatamente a energia que o volante tinha. Ela foi dissipada pelo atrito, aquecendo a pastilha e o próprio anel.

### E1-17 · tela: item `f` acende; cenário novo, do repouso: dois volantes lado a lado, o original e um aro fino de 0,40 m (`MESMOS 20 kg`), cada um com seu bloco de 10 kg; selo `OUTRO VOLANTE · SOLTO DO REPOUSO`; os blocos são soltos juntos e o do aro fica para trás; fantasmas de inércia 90 e 142 kg, sem fio; setas verdes 0,983 e 0,644; CONTA: I_aro = 20 · 0,40² = 3,2 kg·m² → I/r² = 142 kg → a = 9,8 / (1 + 14,2) = 0,644 m/s²; item `f` ganha ✓
[curious] Último item, um teste de intuição. Imagina outro volante, com os mesmos vinte quilos, só que todos num aro fino de quarenta centímetros. Mesmo bloco, mesmo fio, e solta os dois do repouso, lado a lado. O momento de inércia do aro é vinte vezes zero vírgula quatro ao quadrado: três vírgula dois. A inércia equivalente pula para cento e quarenta e dois quilos, e a aceleração do bloco cai de zero vírgula nove oito para zero vírgula seis quatro.

### E1-18 · tela: selo `DICA: SEPARA OS CORPOS · UMA EQUAÇÃO POR CORPO · O VÍNCULO AMARRA`; a trilha `a b c d e f` inteira com ✓
[thoughtful, emphatic] Moral do volante: a massa total não decide nada sozinha. O que decide é onde ela está. E a dica de método vale para o vídeo inteiro: separa os corpos, escreve uma equação para cada um, e não esquece o vínculo. É ele que transforma três incógnitas em uma resposta.

## E2 · A HASTE E O EIXO

### E2-1 · tela: canto linha 2 `EXERCÍCIO 2 · A HASTE E O EIXO`; ESQUEMA 2D fixo: haste de aço horizontal, eixo a d/4 da ponta esquerda, cotas GEO `d` (haste inteira) e `d/4` (ponta ao eixo), rótulo rosa `M`; selo `O QUE ESTE PEDE: I · α(θ) · ω(θ) · A FORÇA DO EIXO`; trilha `a I · b α · c ω · d FORÇA`
[thoughtful] Exercício dois, a haste. Uma haste fina e uniforme, de massa M e comprimento d, gira em torno de um eixo horizontal que passa a um quarto do comprimento de uma das pontas. Ela é solta do repouso, na horizontal. A gente quer o momento de inércia, a aceleração angular e a velocidade angular ao longo da queda e, principalmente, a força que o eixo faz na haste.

### E2-2 · tela: linha `HIPÓTESES: EIXO SEM ATRITO · SEM RESISTÊNCIA DO AR`; o ⊕ do centro de massa acende no meio da haste, cota GEO `d/4` do eixo ao ⊕; CONTA: I = M d²/12 + M (d/4)² = (4/48 + 3/48) M d² = 7 M d²/48
[thoughtful] Hipóteses: eixo sem atrito e nada de resistência do ar. Primeiro, o momento de inércia. O centro de massa está no meio da haste, ou seja, a um quarto do comprimento do eixo. Então, pelos eixos paralelos: o momento de inércia em torno do centro, um doze avos da massa vezes o comprimento ao quadrado, mais a massa vezes um quarto do comprimento, ao quadrado. Um doze avos mais um dezesseis avos: sete quarenta e oito avos.

### E2-3 · tela: régua de comparação abaixo da haste: `EIXO NO CENTRO: 4/48` · `NOSSO EIXO: 7/48` · `EIXO NA PONTA: 16/48`, com o eixo da haste deslizando do centro até a ponta; selo `CONFERE: ENTRE OS DOIS`; item `a` ganha ✓
[curious] Faz sentido? Com o eixo no centro, seriam quatro quarenta e oito avos. Com o eixo na ponta, um terço, que é dezesseis quarenta e oito avos. O nosso eixo está entre os dois, e o resultado também. Ótimo.

### E2-4 · tela: a haste cai um pouco (θ âmbar abaixo da horizontal); seta azul do peso no ⊕ e braço GEO `(d/4) cos θ`; CONTA: τ = M g (d/4) cos θ → α = τ / I = (12/7)(g/d) cos θ; mostrador de α (verde) diminuindo até 0 na vertical; item `b` ganha ✓
[thoughtful] Agora a segunda lei da rotação. Mede o ângulo de queda a partir da horizontal. O único torque é o do peso, aplicado no centro de massa: o peso vezes o braço, que é um quarto do comprimento vezes o cosseno do ângulo. Dividindo pelo momento de inércia, a aceleração angular é doze sétimos da gravidade sobre o comprimento, vezes o cosseno do ângulo. Repara: ela não é constante. É máxima na largada e zero quando a haste passa pela vertical, porque ali o peso aponta direto para o eixo.

### E2-5 · tela: ⊕ desce, cota GEO vertical `(d/4) sen θ`; barra ciano U → K; CONTA: M g (d/4) sen θ = ½ I ω² → ω² = (24/7)(g/d) sen θ; item `c` ganha ✓
[thoughtful] Como a aceleração angular muda, nada de equação de aceleração constante. Para a velocidade angular, a ferramenta certa é a energia. O centro de massa desce um quarto do comprimento vezes o seno do ângulo. Essa energia potencial vira energia cinética de rotação, metade do momento de inércia vezes a velocidade angular ao quadrado. Isolando: a velocidade angular ao quadrado é vinte e quatro sétimos da gravidade sobre o comprimento, vezes o seno do ângulo.

### E2-6 · tela: item `d` acende; no ⊕, duas setas verdes: `a_t` (perpendicular à haste) e `a_c` (ao longo da haste, para o eixo); no eixo, a seta azul `F⃗` ainda tracejada (desconhecida); CONTA: F⃗ + M g⃗ = M a⃗_cm → a_t = α d/4 = (3/7) g cos θ · a_c = ω² d/4 = (6/7) g sen θ
[curious] E a força do eixo? Aqui está o pulo do gato. O eixo é a única força além do peso, então ela sai da segunda lei de Newton para o centro de massa: força do eixo mais peso igual à massa vezes a aceleração do centro de massa. E o centro de massa anda num círculo de raio um quarto do comprimento. Então a aceleração dele tem duas partes: a tangencial, aceleração angular vezes um quarto do comprimento, e a centrípeta, velocidade angular ao quadrado vezes um quarto do comprimento, apontando para o eixo.

### E2-7 · tela: a seta tracejada do eixo vira sólida, decomposta em `F_r` (ao longo da haste, para o eixo) e `F_⊥` (perpendicular, contra a queda); CONTA: F_r = (13/7) M g sen θ · F_⊥ = (4/7) M g cos θ; nota pequena: `d SUMIU`
[thoughtful] Projetando ao longo da haste e perpendicular a ela, as contas ficam curtas. Ao longo da haste, o eixo puxa para dentro com treze sétimos do peso vezes o seno do ângulo. Perpendicular à haste, ele segura com quatro sétimos do peso vezes o cosseno. E repara numa coisa curiosa: o comprimento da haste sumiu. A força no eixo só depende do peso e do ângulo.

### E2-8 · tela: parada em θ = 0: seta azul `4/7 Mg` para cima no eixo; seta verde `a_cm = 3g/7` para baixo no ⊕; régua de comparação `0 ··· 4/7 ··· 1` (queda livre ··· nosso eixo ··· segura tudo); selo `CONFERE: 0 < 4/7 < 1`
[thoughtful] Agora, o teste dos sentidos, em três posições. Na largada, ângulo zero: só sobra a parte perpendicular, quatro sétimos do peso, para cima. Faz sentido? O centro de massa começa descendo com três sétimos da gravidade. Se o eixo segurasse o peso inteiro, ele não desceria. Se não segurasse nada, cairia em queda livre. Quatro sétimos fica no meio. Confere.

### E2-9 · tela: parada em θ = 45°: seta azul de 1,37 Mg inclinada, apontando para cima e para o lado do eixo; componentes tracejadas `9/14 Mg` (horizontal) e `17/14 Mg` (vertical); no ⊕, a trajetória circular do centro de massa em GEO fino e a curva acesa
[curious] A quarenta e cinco graus aparece uma coisa que muita gente esquece: o eixo empurra de lado. A componente horizontal vale nove quatorze avos do peso, apontando para o lado do eixo, e a vertical, dezessete quatorze avos. No total, uma vírgula três sete vez o peso. E por que de lado? Porque o centro de massa está fazendo uma curva, e para curvar alguém precisa empurrar na horizontal. E a única força horizontal aqui é a do eixo.

### E2-10 · tela: parada em θ = 90°: seta azul `13/7 Mg` vertical para cima; seta verde a_c para cima no ⊕; selo pequeno `α = 0 · ω MÁXIMA`; depois uma queda contínua com as setas variando ao vivo e um gráfico pequeno |F|/Mg × θ de 4/7 a 13/7; hold de 2 s; item `d` ganha ✓
[thoughtful, emphatic] E na vertical, noventa graus: a aceleração angular é zero, a parte perpendicular some, e sobram treze sétimos do peso, para cima. Quase o dobro do peso. Repara: aceleração angular zero não quer dizer parada. Aqui a velocidade angular é a maior de toda a queda. É a aceleração centrípeta cobrando a conta: o centro de massa passa voando por baixo do eixo, e o eixo tem que puxá-lo para a curva. Ou seja, numa única queda, a força no eixo vai de quatro sétimos a treze sétimos do peso, e ainda muda de direção no caminho.

### E2-11 · tela: selo `DICA: FORÇA NO EIXO = NEWTON NO CENTRO DE MASSA, COM a_t E a_c`
[thoughtful] A dica deste: a força no eixo sempre sai da segunda lei de Newton para o centro de massa, com as duas acelerações, a tangencial e a centrípeta. Quem esquece a centrípeta erra a força justamente onde ela é maior.

## E3 · O CARRETEL

### E3-1 · tela: canto linha 2 `EXERCÍCIO 3 · O CARRETEL`; o carretel do hook de volta em 3/4, travado; dados nos objetos: `I = 0,50 kg·m²`, `R = 0,30 m`, `r = 0,10 m`, `m₁ = 6,0 kg`, `m₂ = 10,0 kg`; os enrolamentos opostos piscam; selo `ANTES DA CONTA: QUAL DESCE?`
[curious] Exercício três: o carretel do começo, agora com números. Ele tem momento de inércia de zero vírgula cinco quilograma metro quadrado e gira sem atrito. O tambor grande tem trinta centímetros de raio e segura o bloco de seis quilos. O pequeno tem dez centímetros e segura o de dez quilos, com o fio enrolado no sentido contrário. De novo, antes de qualquer conta: qual desce?

### E3-2 · tela: o carretel gira um ângulo pequeno Δθ (âmbar) e volta; réguas GEO nos blocos: `↓ R Δθ` no leve, `↑ r Δθ` no pesado (três vezes menor); CONTA: PERDE m₁ g R Δθ · GANHA m₂ g r Δθ → 6 · 0,30 = 1,8 > 10 · 0,10 = 1,0; selo `QUEM DECIDE: MASSA × RAIO`
[thoughtful] Tem um jeito de prever sem resolver nada. Imagina o carretel girando um ângulo pequeno no sentido em que o bloco leve desce. O bloco de seis quilos desce esse ângulo vezes trinta centímetros. O de dez quilos sobe o mesmo ângulo vezes dez centímetros: três vezes menos. Comparando as energias potenciais, o leve perde seis vezes zero vírgula três, um vírgula oito, e o pesado ganha só dez vezes zero vírgula um, um. Sobra energia, então o movimento acontece nesse sentido. Quem decide não é a massa sozinha: é a massa vezes o raio.

### E3-3 · tela: dolly contínuo até a vista frontal; diagramas de corpo livre: bloco leve (peso `m₁g` ↓, `T₁` ↑), bloco pesado (peso `m₂g` ↓, `T₂` ↑); no carretel, `T₁` na borda do tambor grande (direita) e `T₂` na do pequeno (esquerda), setas curvas de torque em sentidos opostos; centro com `BRAÇO ZERO`
[thoughtful, emphatic] Só que cuidado com um detalhe. No carretel, quem faz torque não são os pesos. São as trações dos fios. E quando tudo se move, as trações não são mais iguais aos pesos. Então, de novo, separa os corpos. No bloco leve, o peso para baixo e a primeira tração para cima. No pesado, o peso para baixo e a segunda tração para cima. No carretel, a primeira tração puxa a borda do tambor grande, de um lado, e a segunda puxa a borda do pequeno, do outro: torques em sentidos opostos.

### E3-4 · tela: CONTA, cinco linhas com rótulos: `LEVE: m₁g − T₁ = m₁a₁` · `PESADO: T₂ − m₂g = m₂a₂` · `CARRETEL: T₁R − T₂r = Iα` · `VÍNCULOS: a₁ = αR · a₂ = αr`
[thoughtful] As equações. O bloco leve desce: o peso dele menos a primeira tração é igual à massa dele vezes a aceleração. O pesado sobe: a segunda tração menos o peso dele é igual à massa dele vezes a aceleração dele. No carretel: a primeira tração vezes o raio grande, menos a segunda tração vezes o raio pequeno, é igual ao momento de inércia vezes a aceleração angular. E dois vínculos: o bloco leve acelera com a aceleração angular vezes o raio grande, e o pesado, vezes o raio pequeno.

### E3-5 · tela: as trações isoladas das linhas dos blocos voam para a linha do carretel; CONTA: α = (m₁R − m₂r) g / (I + m₁R² + m₂r²); o numerador acende junto com o selo do E3-2; o denominador ganha a nota `SEMPRE > 0`
[curious] Isola as trações nas equações dos blocos, troca as acelerações pelos vínculos e coloca tudo na equação do carretel. Aparece algo bonito. A aceleração angular é a gravidade vezes, massa leve vezes raio grande menos massa pesada vezes raio pequeno, dividido por momento de inércia mais massa leve vezes raio grande ao quadrado mais massa pesada vezes raio pequeno ao quadrado. Repara no numerador: é exatamente a comparação que a gente fez pela energia. E o denominador é sempre positivo: todo mundo que se move soma inércia. Por isso o sinal do numerador prevê o sentido.

### E3-6 · tela: CONTA: α = 0,8 · 9,8 / 1,14 = 6,88 rad/s² → a₁ = α R = 2,06 m/s² ↓ · a₂ = α r = 0,688 m/s² ↑; selo `CONFERE: a₁/a₂ = R/r = 3`; setas verdes nos blocos, na razão 3 : 1
[thoughtful] Com os números: zero vírgula oito vezes nove vírgula oito, sobre um vírgula catorze. Seis vírgula oito oito radianos por segundo ao quadrado. O bloco leve desce com dois vírgula zero seis metros por segundo ao quadrado, e o pesado sobe com zero vírgula seis nove. Primeira conferência: a razão entre as duas acelerações é três, a mesma razão entre os raios.

### E3-7 · tela: CONTA: T₁ = m₁(g − a₁) = 46,4 N < m₁g = 58,8 N · T₂ = m₂(g + a₂) = 104,9 N > m₂g = 98 N; depois duas verificações lado a lado: `CARRETEL SOZINHO: T₁R − T₂r = 3,44 = 0,50 · α` · `SISTEMA INTEIRO: (m₁R − m₂r) g = 7,84 = 1,14 · α` → `α = 6,88` nas duas; embaixo, pequeno e riscado: `7,84 / 0,50 = 15,7 ✗`; hold de 2 s
[thoughtful] Agora as trações. A primeira: seis vezes, nove vírgula oito menos dois vírgula zero seis. Quarenta e seis vírgula quatro newtons, menor que o peso do bloco leve, cinquenta e oito vírgula oito, porque ele desce acelerando. A segunda: dez vezes, nove vírgula oito mais zero vírgula seis nove. Cento e quatro vírgula nove, maior que o peso do pesado, porque ele sobe acelerando. E o torque das trações sobre o carretel dá três vírgula quatro quatro newtons metro. Dividido pelo momento de inércia do carretel, zero vírgula cinco, volta a aceleração angular: seis vírgula oito oito. E os sete vírgula oito quatro do numerador, massa vezes gravidade vezes raio? Também valem, só que para o sistema inteiro: divididos pela inércia total, um vírgula catorze, que inclui os dois blocos, dão os mesmos seis vírgula oito oito. O erro clássico seria misturar as duas coisas: dividir os sete vírgula oito quatro só pelo momento de inércia do carretel.

### E3-8 · tela: a simulação anda até o bloco leve descer 1,0 m (o pesado sobe 0,333 m); barras ciano: `ΔU = 58,8 − 32,7 = 26,1 J` = `K₁ + K₂ + K_carretel`; CONTA: v₁ = 2,03 m/s · v₂ = 0,677 m/s; selo `CONFERE: v₁² = 2 a₁ · 1,0 ⇒ 2,03 m/s`
[thoughtful] Segunda conferência, pela energia. Quando o bloco leve desce um metro, o pesado sobe um terço de metro. A energia potencial que sobra, cinquenta e oito vírgula oito menos trinta e dois vírgula sete, vinte e seis vírgula um joules, vira energia cinética dos dois blocos e do carretel. Resolvendo, o leve chega a dois vírgula zero três metros por segundo. E pela cinemática, com aceleração de dois vírgula zero seis durante um metro, dá o mesmo valor. Bate.

### E3-9 · tela: a montagem volta ao repouso, travada; o bloco de 10 kg é trocado por um de `18 kg`; a trava sai e o carretel fica parado; nota `α = 0 · PARTIU DO REPOUSO ⇒ FICA PARADO`; CONTA: m₂ r = m₁ R → m₂ = 6 · 0,30 / 0,10 = 18 kg; a pergunta do hook volta pequena no topo com a resposta `BRAÇO 3× MAIOR`
[curious] E que massa faria esse sistema ficar parado, se fosse solto de novo do repouso? Precisa que o numerador zere: massa pesada vezes dez centímetros igual a seis quilos vezes trinta. Dezoito quilos, três vezes a massa do leve, porque o braço é três vezes menor. Repara: isso zera a aceleração angular. Se o carretel já estivesse girando, ele continuaria girando com velocidade constante. Ele só fica parado porque partiu do repouso. E a pergunta do começo está respondida: o bloco mais leve desce porque puxa com um braço três vezes maior.

### E3-10 · tela: selo `DICA: MASSA × RAIO PREVÊ O SENTIDO · A EQUAÇÃO USA AS TRAÇÕES`
[thoughtful] A dica deste: num carretel, compara massa vezes raio para prever o sentido, mas escreve a equação com as trações. E confere com a razão das acelerações e com a energia.

## E4 · O PÊNDULO MAIS RÁPIDO

### E4-1 · tela: canto linha 2 `EXERCÍCIO 4 · O PÊNDULO MAIS RÁPIDO`; ESQUEMA 2D: dois discos de aço iguais ligados por haste leve, o de cima preso pelo centro no eixo; rótulos `M`, `R` em cada disco, cota GEO `l` entre os centros; oscilação pequena; selo `O QUE ESTE PEDE: O PERÍODO PARA ÂNGULOS PEQUENOS`
[thoughtful] Exercício quatro, o pêndulo de disco. Começa com uma montagem: dois discos iguais, de massa M e raio R, ligados por uma haste leve. O de cima é preso no eixo pelo próprio centro, e o de baixo fica pendurado, com os centros a uma distância l um do outro. Qual é o período das oscilações pequenas?

### E4-2 · tela: ao lado, um pêndulo simples (bolinha rosa num fio GEO de comprimento l); CONTA: I α = −m g l sen θ → I = m l² → α = −(g/l) sen θ ≈ −(g/l) θ → T = 2π √(l/g); selo `ÂNGULOS PEQUENOS: sen θ ≈ θ`
[thoughtful] A estratégia é comparar com o pêndulo simples, uma bolinha na ponta de um fio. Pela segunda lei da rotação: o momento de inércia da bolinha é a massa vezes o comprimento ao quadrado, e o torque do peso é a massa vezes a gravidade vezes o comprimento vezes o seno do ângulo, puxando de volta. Para ângulos pequenos, o seno é quase o próprio ângulo, e a aceleração angular fica proporcional ao ângulo, com sinal contrário. O período desse movimento é dois pi vezes a raiz do comprimento sobre a gravidade. Então, se o nosso pêndulo der a mesma equação com outro comprimento, a gente já sabe o período. É só usar o comprimento equivalente.

### E4-3 · tela: no pêndulo de dois discos, o peso do disco de cima com `BRAÇO ZERO` e o do de baixo com braço `l sen θ`; ⊕ do conjunto em l/2 com `2M · l/2 = M l`; CONTA: I = ½ M R² + (½ M R² + M l²) = M (R² + l²) → τ = −M g l sen θ → l_eq = I/(M_total d_CM) = I/(M l) = (R² + l²)/l → T = 2π √((R² + l²)/(g l)) = 1,159 s (R = 0,10 m, l = 0,30 m); o pêndulo simples de 0,333 m oscila em fase com os discos
[thoughtful] No nosso pêndulo, o torque vem só do disco de baixo: o peso do de cima passa pelo eixo. Já o momento de inércia tem os dois. O de cima, metade da massa vezes o raio ao quadrado. O de baixo, o mesmo, mais a massa vezes a distância ao quadrado, pelos eixos paralelos. E repara num detalhe: a massa total é o dobro da massa de um disco, e o centro de massa do conjunto fica no meio, a metade da distância. Massa total vezes a distância do eixo ao centro de massa dá a massa de um disco vezes a distância inteira. Dividindo o momento de inércia por isso, o comprimento equivalente é, raio ao quadrado mais distância ao quadrado, sobre a distância. Com raio de dez centímetros e distância de trinta, o período dá um vírgula um seis segundo. E olha o pêndulo simples equivalente ao lado: oscila junto, em fase.

### E4-4 · tela: a cena congela; entram duas montagens lado a lado (com e sem o disco de cima), soltas juntas, do repouso, do mesmo ângulo, defasando devagar; rótulos `1,159 s` e `1,129 s`
[curious] E o disco de cima, ajuda ou atrapalha? Monta dois pêndulos lado a lado, um com o disco de cima e outro sem, e solta os dois juntos, do mesmo ângulo. O disco de cima soma momento de inércia e não soma torque nenhum. Só deixa o pêndulo mais preguiçoso: sem ele, o período cai para um vírgula um três segundo.

### E4-5 · tela: fica um disco só, pendurado por haste leve, eixo a uma distância `l` do centro; o eixo começa a deslizar para cima e para baixo; selo `ONDE PÔR O EIXO PARA O PERÍODO SER MÍNIMO?`
[curious] Então tira o disco de cima. Fica um disco só, pendurado por uma haste leve, com o eixo a uma certa distância do centro. A pergunta agora é de projeto: onde pôr o eixo para o período ser o menor possível?

### E4-6 · tela: CONTA: I = ½ M R² + M l² → l_eq = I/(M l) = l + R²/(2l); o eixo desliza para longe (o segundo termo encolhe, `≈ PÊNDULO SIMPLES`) e para perto do centro (o segundo termo explode, `T → ∞`)
[thoughtful] O momento de inércia é metade da massa vezes o raio ao quadrado, mais a massa vezes a distância ao quadrado. O torque é o peso vezes a distância. Então o comprimento equivalente fica a distância mais o raio ao quadrado sobre duas vezes a distância. Olha os dois extremos. Eixo muito longe: o segundo termo some, e o disco vira uma bolinha num fio. Eixo quase no centro: o torque some, o segundo termo explode, e o período vai para infinito. Entre os dois extremos tem que haver um mínimo.

### E4-7 · tela: os três caminhos **em sequência** na CONTA, um por vez (o anterior sai e fica só a caixa): `DERIVADA: dl_eq/dl = 1 − R²/(2l²) = 0` → `PRODUTO FIXO: l · R²/(2l) = R²/2 ⇒ TERMOS IGUAIS` → `GRÁFICO`; os três chegam à mesma caixa: `l = R/√2 ≈ 7,07 cm · T_mín = 2π√(√2 R/g) = 0,755 s`; à direita, a curva T(l) desenhada enquanto o eixo desliza, com o ponto seguindo o eixo; hold de 2 s no mínimo
[thoughtful, emphatic] Vamos achar esse mínimo por três caminhos. Primeiro, a derivada: derivando o comprimento equivalente em relação à distância e igualando a zero, sai a distância igual ao raio sobre raiz de dois. Segundo, sem derivada nenhuma: os dois termos, a distância e o raio ao quadrado sobre duas vezes a distância, têm produto fixo, metade do raio ao quadrado. E quando o produto de dois números positivos é fixo, a soma é mínima quando eles são iguais. Mesma resposta. Terceiro, a curva do período em função da posição do eixo. O fundo dela cai exatamente em sete vírgula zero sete centímetros, para um disco de dez. Período mínimo: zero vírgula sete cinco cinco segundo.

### E4-8 · tela: dois eixos fantasma no disco, a 5 cm e a 10 cm do centro; os dois pontos na curva na mesma altura `0,777 s`; dois discos oscilando em fase; CONTA: l · l′ = R²/2 → 5 · 10 = 50 = 10²/2; hold de 2 s
[excited] E a curva ainda esconde um presente. Com o eixo a cinco centímetros ou a dez centímetros do centro, o período é o mesmo: zero vírgula sete sete sete segundo. É que o comprimento equivalente não muda quando a gente troca a distância pelo raio ao quadrado sobre duas vezes a distância. Cinco vezes dez dá cinquenta, que é exatamente metade de dez ao quadrado. Duas posições diferentes, o mesmo relógio.

### E4-9 · tela: o ponto de mínimo marcado no disco: o eixo cai **dentro** do disco (furo desenhado); no gráfico, a região l < R hachurada em GEO com `EIXO DENTRO DO DISCO`; o ponto l = R marcado: `0,777 s · +3%`; selo `CONFERE: PERTO DO FUNDO, A CURVA É QUASE PLANA`
[thoughtful] Só que repara onde caiu o mínimo: a sete centímetros do centro, num disco de dez. O eixo está dentro do disco. Isso é possível, se a gente fizer um furo. Mas se o disco tem que ficar pendurado por uma haste presa fora dele, a distância não pode ser menor que o raio. Aí o melhor permitido é o eixo bem na borda: zero vírgula sete sete sete segundo, só três por cento acima do mínimo. Porque perto do fundo a curva é quase plana: errar um pouco a posição do eixo quase não muda o período.

### E4-10 · tela: caixa `l_eq = I_eixo / (M_total · d_CM)`; selo `DICA: O RESTO É PÊNDULO SIMPLES`
[thoughtful] A dica deste: para qualquer pêndulo feito de corpo rígido, divide o momento de inércia em torno do eixo pela massa total vezes a distância do eixo ao centro de massa. Esse é o comprimento equivalente, e o resto é pêndulo simples.

## SÍNTESE

### S1 · tela: canto linha 2 `RESUMO`; quatro cartões `PANEL` entram um a um, com o objeto de cada exercício: `VOLANTE: a = g/(1 + I/mr²) · I/r² É MASSA EXTRA` (borda rosa) · `HASTE: O EIXO VAI DE 4/7 A 13/7 DO PESO` (borda azul) · `CARRETEL: MASSA × RAIO DECIDE · TRAÇÕES NO CARRETEL, PESOS NO SISTEMA` (borda rosa → azul) · `PÊNDULO: l = R/√2 · T_mín = 2π√(√2 R/g)` (borda branca)
[happy] Resumindo os quatro. No volante, a distribuição da massa decide a aceleração: o momento de inércia age como uma massa extra no fio. Na haste, a força no eixo não é constante: vai de quatro sétimos a treze sétimos do peso e muda de direção. No carretel, a geometria vence a massa: quem manda é massa vezes raio. As trações dão a equação do carretel, e os pesos dão a do sistema inteiro, cada um com a sua inércia. E no pêndulo, torque e momento de inércia viram ferramenta de projeto: o período é mínimo com o eixo a uma distância do centro igual ao raio sobre raiz de dois.

### S2 · tela: os cartões encolhem e entra a linha `DESENHA O SISTEMA → ESCOLHE O EIXO → ESCREVE AS EQUAÇÕES → APLICA OS VÍNCULOS → CONFERE`; atrás, o carretel do hook girando devagar
[calm, satisfied] E o método foi o mesmo nos quatro: começa pela física, não pela fórmula. Identifica as forças, escolhe o eixo, escreve as equações e usa os vínculos quando houver. Depois confere: pela energia, pelos sentidos das forças, pelos casos-limite ou por outro caminho. Uma conta que passa nesses testes é uma conta em que dá para confiar.

## ENCERRAMENTO

### EN1 · tela: FadeOut geral; logo com anéis; `INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS`
[happy] Se esse vídeo te ajudou, se inscreve no Parallax Lab para acompanhar os próximos vídeos. E antes de ir, um desafio para os comentários.

### EN2 · tela: o volante pequeno no canto com o bloco trocado por `20 kg`; `DESAFIO: A ACELERAÇÃO DOBRA?`
[curious] No volante, troca o bloco de dez quilos por um de vinte. A aceleração dobra? Mais que dobra? Menos? Usa a fórmula que a gente guardou e escreve a sua resposta aqui embaixo. Até a próxima!

---

## Conferência numérica (fonte única dos números da tela)

| Âncora | Grandeza | Valor |
|---|---|---|
| D2–D3 | α, a_ponta, ponto a_t = g | 9g/(8L); 9g/8; 8L/9 (antes: 3g/2 e 2L/3) |
| E1-3 | I_anel | 1,875 kg·m² |
| E1-4 | I_cubo; I por disco pequeno; dois discos | 0,015; 0,06375; 0,1275 |
| E1-5 | I total; anel/discos/cubo em I; em massa; sem M d² | 2,0175; 92,9% / 6,3% / 0,7%; 75% / 10% / 15%; 0,0025 (51×) |
| E1-9 | I/(m r²); massa equivalente I/r² | 8,967; 89,7 kg |
| E1-10 | a; α; T; T r = I α | 0,9833 m/s²; 6,555 rad/s²; 88,17 N; 13,23 N·m |
| E1-11 | em t = 1,5 s: ω; Δθ; voltas; h; v | 9,833 rad/s; 7,375 rad; 1,174; 1,106 m; 1,475 m/s |
| E1-12 | borda (0,40 m): a_t; a_c; a_c/g; ângulo; v da borda | 2,622 m/s²; 38,67 m/s²; 3,95; 3,9°; 3,93 m/s |
| E1-13 | mgh; K_bloco; K_vol; fração; razão | 108,41 J; 10,88 J; 97,53 J; 90,0%; 8,97 |
| E1-14 | P em 1,5 s; ½ P t | 130,0 W; 97,5 J |
| E1-15 | μ_c (cinético); N; f_at; τ | 0,40; 25 N; 10 N; 4,0 N·m |
| E1-16 | α_f; t até parar (tempo real); Δθ; voltas; W | 1,983 rad/s²; 4,96 s; 24,38 rad; 3,88; 97,5 J |
| E1-17 | I_aro; I/r²; a; α | 3,2 kg·m²; 142,2 kg; 0,644 m/s²; 4,29 rad/s² |
| EN2 | (só para a moderação dos comentários; não vai na tela) bloco de 20 kg | a = 9,8/(1 + 4,483) = 1,787 m/s², 1,82× (menos que o dobro) |
| E2-2 | I | 7Md²/48 |
| E2-4/E2-5 | α(θ); ω²(θ); para d = 1,0 m: α(0), ω(90°) | (12/7)(g/d) cos θ; (24/7)(g/d) sen θ; 16,8 rad/s²; 5,80 rad/s |
| E2-6/E2-7 | a_t; a_c; F_r; F_⊥ | (3/7) g cos θ; (6/7) g sen θ; (13/7) Mg sen θ; (4/7) Mg cos θ |
| E2-8 | θ = 0: F; a_cm | 4/7 Mg ↑; 3g/7 ↓ |
| E2-9 | θ = 45°: F_x; F_y; módulo | 9/14 Mg (para o lado do eixo); 17/14 Mg ↑; 1,374 Mg |
| E2-10 | θ = 90°: F | 13/7 Mg ≈ 1,857 Mg ↑ |
| E3-2 | m₁R; m₂r | 1,8; 1,0 kg·m |
| E3-5/E3-6 | denominador; α; a₁; a₂ | 1,14 kg·m²; 6,877 rad/s²; 2,063 m/s² ↓; 0,688 m/s² ↑ |
| E3-7 | T₁; T₂; carretel: T₁R − T₂r ÷ I; sistema: (m₁R − m₂r) g ÷ 1,14; erro de misturar | 46,42 N; 104,88 N; 3,44 ÷ 0,50 = 6,88; 7,84 ÷ 1,14 = 6,88; 7,84 ÷ 0,50 = 15,7 ✗ |
| E3-8 | ΔU; v₁; v₂; ω; tempo de 1,0 m | 26,13 J; 2,031 m/s; 0,677 m/s; 6,77 rad/s; 0,985 s |
| E3-9 | m₂ de equilíbrio | 18 kg |
| E4-3 | T (dois discos, R = 0,10, l = 0,30); l_eq | 1,159 s; 0,333 m |
| E4-4 | T sem o disco de cima; pêndulo simples de 0,30 m | 1,129 s; 1,099 s |
| E4-7 | l mínimo; l_eq mínimo; T mínimo | 7,07 cm; 14,14 cm; 0,755 s |
| E4-8 | T em 5 cm e em 10 cm | 0,777 s (iguais) |
| E4-9 | T em l = R; excesso | 0,777 s; +3,0% |
| E4 (gráfico) | T em 2, 20, 30, 40 cm | 1,043; 0,952; 1,129; 1,289 s |

## Capítulos do YouTube (provisórios; o `qa.txt` corrige os tempos)
0:00 Qual bloco desce? · 0:35 Caixa de ferramentas · 2:20 O desafio da régua · 3:30 Exercício 1: o volante · 14:00 Exercício 2: a haste e o eixo · 20:00 Exercício 3: o carretel · 25:00 Exercício 4: o pêndulo mais rápido · 30:00 Resumo
