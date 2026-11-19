# ANEXO A · roteiro com narração v1 (fonte do `ancoras.json`)

Narração **v1**, ~2.200 palavras ≈ 13,6 min a 2,7 palavras/s (42 âncoras; hook ≈ 33 s; cortáveis: B1-8 ≈ 20 s, B5-5 ≈ 15 s). A duração é estimativa; a voz mede.
Padrão: `padrao_video_longo.md` §5 e `roteiro_voz_elevenlabs_v4.md`. Tom de professor de cursinho, "a gente" e "você", nunca a letra solta (o símbolo é apresentado uma vez, depois só o nome). Números por extenso como serão falados.

**Como ler:** cada `###` é uma âncora (evento visual). A linha `tela:` diz o que aparece; a fala começa ~0,15 s depois e manda: a cena se estica. Tags `[ ]` do ElevenLabs v4 em inglês, uma por trecho; não entram na legenda. `[CORTÁVEL]` marca o que sai primeiro se passar do tempo.

## HOOK

### H1 · tela: `P_34`; pêndulo cônico no pórtico de aço, bolinha com faixa rosa girando num círculo horizontal, rastro GEO, o fio varrendo um cone translúcido; duas voltas
[curious] Olha esse pêndulo. Em vez de ir e voltar, a bolinha anda num círculo deitado, sempre na mesma altura, sempre com a mesma rapidez. Volta depois de volta, a velocidade angular não muda nada.

### H2 · tela: congela; seta azul do peso na bolinha; vetor posição laranja do prego até a bolinha; seta azul do torque do peso saindo do prego, horizontal; topo: `O PESO FAZ TORQUE EM RELAÇÃO AO PREGO`
[thoughtful] Só que repara numa coisa. Em relação ao prego lá em cima, o peso da bolinha tem braço. Ele faz torque, e esse torque não é zero. E a gente sabe que torque muda o momento angular.

### H3 · tela: volta a girar; a seta do torque gira junto com a bolinha; topo troca para `COMO EXISTE TORQUE SEM ω AUMENTAR?`; hold de 2 s
[curious] Então como pode existir torque sem a velocidade angular aumentar? O que é que esse torque está mudando?

## ABERTURA

### A1 · tela: logo; `BEM-VINDOS AO PARALLAX LAB`; o pêndulo girando desfocado atrás
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab.

### A2 · tela: `MOMENTO ANGULAR DO CORPO RÍGIDO`; `NESTE VÍDEO:` e três ícones (cone · haltere torto · roda) acendendo nas palavras
[thoughtful] Hoje o assunto é o momento angular de um corpo rígido. E a gente vai responder essa pergunta em três passos: primeiro esse pêndulo, depois um haltere torto girando num eixo, e no fim a roda de um carro. Os três contam a mesma história.

## B1 · UM L QUE SÓ VIRA

### B1-1 · tela: canto linha 2 `UM L QUE SÓ VIRA`; `P_34` congelada, bolinha em φ = 0; r⃗ laranja do prego à bolinha, p⃗ magenta tangente, marca de ângulo reto; CONTA: L⃗ = r⃗ × p⃗ → |L⃗| = r p → = ℓ m v
[thoughtful] Antes de somar muitas partículas, vamos entender uma só. O momento angular da bolinha em relação ao prego é o produto vetorial do vetor posição com o momento linear. O vetor posição vai do prego até a bolinha, ao longo do fio. O momento linear é tangente ao círculo, na horizontal. Os dois são perpendiculares, então o tamanho do momento angular é o comprimento do fio vezes o momento linear.

### B1-2 · tela: L⃗ magenta-claro sai do prego, perpendicular ao fio, inclinado para fora, do lado da bolinha; o plano (eixo, fio) aparece translúcido; ícone 2.5D da mão direita
[thoughtful] E a direção? Perpendicular ao fio e perpendicular ao momento linear. Pela regra da mão direita, ele aponta para cima e para fora, inclinado para o lado da bolinha. Repara: ele não aponta ao longo do eixo de rotação.

### B1-3 · tela: L⃗ se decompõe em L_z (vertical, cheia) e L_h (horizontal, tracejada); ângulo θ âmbar entre o fio e o eixo; CONTA: R = ℓ sen θ · v = ω R → L_z = \|L⃗\| sen θ → = m R² ω · L_h = \|L⃗\| cos θ → = m ω ℓ² sen θ cos θ
[thoughtful] Vale separar esse vetor em duas partes: uma vertical, ao longo do eixo, e uma horizontal. O raio do círculo é o comprimento do fio vezes o seno do ângulo. Fazendo a conta, a parte vertical fica a massa vezes o raio ao quadrado vezes a velocidade angular. Ou seja, momento de inércia vezes velocidade angular, igualzinho ao círculo de sempre. A parte horizontal é a novidade.

### B1-4 · tela: volta a girar; L⃗ gira junto; L_z parada; a ponta de L⃗ desenha um círculo horizontal fino magenta-claro; mostrador de \|L⃗\| constante
[curious] Agora deixa o pêndulo girar. A parte vertical fica parada. Mas a parte horizontal acompanha a bolinha, e a ponta do momento angular desenha um círculo. O tamanho não muda… a direção muda o tempo todo. E um vetor que muda de direção está mudando.

### B1-5 · tela: congela; inset `VISTA DE CIMA` do círculo da ponta: L_h girando de um ângulo ω dt; dL⃗ tangente; a seta do torque do peso desliza do prego até a ponta e coincide com dL⃗; CONTA: \|dL⃗\| = L_h ω dt → \|dL⃗/dt\| = ω L_h · τ = m g R → = m g ℓ sen θ
[thoughtful] Num intervalo de tempo pequeno, a parte horizontal gira de um ângulo igual à velocidade angular vezes esse tempo. Então a variação do momento angular é a parte horizontal vezes a velocidade angular vezes o tempo, e aponta na tangente desse círculo. Agora olha o torque do peso: o braço é o raio do círculo, e ele aponta exatamente na mesma direção. O torque não está acelerando o giro. Ele está virando o momento angular.

### B1-6 · tela: CONTA: τ⃗ = dL⃗/dt → m g ℓ sen θ = ω · m ω ℓ² sen θ cos θ → (m, ℓ e sen θ cancelam) → g = ω² ℓ cos θ → ω² = g/(ℓ cos θ) → ℓ = 1,00 m, θ = 30° → ω = 3,36 rad/s · período 1,87 s; hold de 2 s
[thoughtful, emphatic] E isso já dá física de verdade. Iguala o torque à taxa de variação do momento angular. A massa cancela, um comprimento cancela, o seno cancela, e sobra: a velocidade angular ao quadrado é a gravidade dividida pelo comprimento do fio vezes o cosseno do ângulo. Com um metro de fio a trinta graus, dá três vírgula três seis radianos por segundo, uma volta a cada um vírgula oito sete segundo. É a única velocidade angular em que esse pêndulo gira nesse ângulo.

### B1-7 · tela: frase-chave `RAPIDEZ CONSTANTE · VELOCIDADE MUDA DE DIREÇÃO`; v⃗ violeta da bolinha em três posições, mesmo comprimento; ao lado, L⃗ em três posições, mesmo comprimento
[thoughtful] Só um cuidado com as palavras. A rapidez da bolinha é constante, mas a velocidade dela muda de direção, e por isso existe aceleração centrípeta. Com o momento angular é a mesma coisa: o tamanho é constante, mas o vetor muda.

### B1-8 · `[CORTÁVEL]` · tela: selo `DE OUTRO PONTO`; a origem desce do prego para o centro do círculo; L⃗ fica vertical e parado; τ do peso e τ do fio, opostos, somam zero
[thoughtful] Um detalhe: se você medir tudo em relação ao centro do círculo, em vez do prego, o momento angular fica vertical e constante, e o torque do peso cancela o torque do fio. As duas contas estão certas: o momento angular depende do ponto.

## B2 · UM CORPO INTEIRO

### B2-1 · tela: canto linha 2 `UM CORPO INTEIRO`; `V_34`: a batata de cubinhos de aço presa ao eixo vertical da bancada, girando; selo `HIPÓTESES: FORÇAS INTERNAS AOS PARES, NA MESMA LINHA`; CONTA: L⃗ = Σ r⃗ᵢ × p⃗ᵢ → dL⃗/dt = Σ τ⃗_ext
[thoughtful] Agora, um corpo inteiro. Um corpo rígido é um monte de pedacinhos, cada um com o seu momento angular em relação a uma origem fixa. O momento angular do corpo é a soma de todos eles. E, quando a gente deriva essa soma, as forças internas aparecem aos pares, iguais, opostas e na mesma linha, então os torques delas se cancelam. Sobra: o torque externo total é a taxa de variação do momento angular do corpo.

### B2-2 · tela: um cubinho acende (rosa); seu círculo horizontal GEO; origem O no eixo, na altura do centro de massa; r⃗ᵢ laranja de O ao cubinho; r⃗ᵢ se abre em ρ⃗ᵢ (horizontal) + zᵢ ẑ (vertical, tracejado); v⃗ᵢ violeta tangente; CONTA: r⃗ᵢ = ρ⃗ᵢ + zᵢ ẑ
[thoughtful] Pega um pedacinho só. Com o eixo fixo, ele anda num círculo horizontal. A gente coloca a origem num ponto fixo do eixo e quebra o vetor posição em duas partes: uma horizontal, que é o raio do círculo desse pedacinho, e uma vertical, que é a altura dele em relação à origem.

### B2-3 · tela: CONTA: L⃗ᵢ = r⃗ᵢ × mᵢ v⃗ᵢ → = ρ⃗ᵢ × mᵢ v⃗ᵢ + zᵢ ẑ × mᵢ v⃗ᵢ; no desenho, dois vetores magenta-claro saem do cubinho: um vertical (do ρ⃗ᵢ) e um horizontal (do zᵢ), apontando para o eixo
[thoughtful] Aí o momento angular desse pedacinho também se quebra em dois. A parte do raio dá um vetor vertical, ao longo do eixo. A parte da altura dá um vetor horizontal. Exatamente como no pêndulo.

### B2-4 · tela: CONTA: mᵢ ρᵢ vᵢ → mᵢ ρᵢ² ω → L_z = Σ mᵢ ρᵢ² ω → = (Σ mᵢ ρᵢ²) ω → L_z = I_z ω; os cubinhos acendem em onda, de dentro para fora, e cada um empilha uma fatia na seta vertical
[thoughtful] Soma as partes verticais. Cada uma é a massa vezes o raio vezes a velocidade, e a velocidade é a velocidade angular vezes o raio. Então cada pedacinho dá massa vezes raio ao quadrado vezes velocidade angular. A velocidade angular é a mesma para todos e sai da soma, e o que sobra dentro é o momento de inércia em relação ao eixo. A componente do momento angular ao longo do eixo é o momento de inércia vezes a velocidade angular. Sempre, para qualquer corpo rígido girando em torno de um eixo fixo.

### B2-5 · tela: CONTA: τ⃗ = dL⃗/dt → τ_z = dL_z/dt → (I_z constante) → τ_z = I_z α
[thoughtful] E, como o corpo é rígido, o momento de inércia não muda. Pegando só a componente da lei do torque ao longo do eixo, sai o torque igual a momento de inércia vezes aceleração angular. Aquela equação que a gente já usava é só uma componente da lei geral.

### B2-6 · tela: as setas horizontais de muitos cubinhos piscam, apontando para lados diferentes; na CONTA, abaixo de L_z = I_z ω: L⃗_⊥ = ?
[curious] Mas repara no que essa igualdade não diz. Ela fala só da componente ao longo do eixo. E as partes horizontais de cada pedacinho? Elas se cancelam ou se somam? Para ver, vamos para o caso mais simples possível.

## B3 · O HALTERE TORTO

### B3-1 · tela: canto linha 2 `O HALTERE TORTO`; `H_34`: bancada com motor, coluna com dois mancais abaixo, eixo vertical, haste a 30° do eixo com duas esferas de faixa rosa; gira a 1 volta/s; selo `HIPÓTESES: HASTE SEM MASSA · MASSAS PONTUAIS · ω CONSTANTE`; rótulos m = 0,40 kg, ℓ = 0,30 m, α = 30°
[thoughtful] Um haltere torto: duas massas iguais, de quatrocentos gramas, nas pontas de uma haste. A haste está presa ao eixo pelo meio, mas inclinada, a trinta graus do eixo, com cada massa a trinta centímetros do centro. O centro de massa fica bem no eixo, e um motor mantém a rotação em uma volta por segundo.

### B3-2 · tela: congela com a haste no plano xz; a massa de cima acende; seu círculo GEO; r⃗₁ = ρ⃗₁ + z₁ ẑ; L⃗₁ sai da massa: parte vertical e parte horizontal apontando para dentro, para o lado oposto ao dela
[thoughtful] Cada massa descreve um círculo horizontal, como a bolinha do exemplo anterior. Pega a massa de cima. A altura dela é positiva, então a parte horizontal do momento angular dela aponta para dentro, para o lado oposto ao dela.

### B3-3 · tela: a massa de baixo acende; CONTA: ρ⃗₂ = −ρ⃗₁ · z₂ = −z₁ → z₂ ρ⃗₂ = (−z₁)(−ρ⃗₁) → z₂ ρ⃗₂ = z₁ ρ⃗₁ (os dois sinais de menos se encontram e somem); no desenho, L⃗₂ sai da massa de baixo com a parte horizontal apontando para o mesmo lado da de L⃗₁
[curious] Agora a massa de baixo. Ela está do outro lado do eixo, então o raio dela aponta para o lado oposto. Mas a altura também trocou de sinal, porque ela está abaixo da origem. Duas trocas de sinal juntas… e o produto não troca. A parte horizontal da massa de baixo aponta para o mesmo lado que a da massa de cima.

### B3-4 · tela: os dois L⃗ᵢ, cada um nascendo na sua massa, deslizam para a origem e se somam ponta com cauda: vertical com vertical, horizontal com horizontal; nasce o L⃗ total, inclinado; hold de 2 s
[thoughtful, emphatic] Leva os dois para a mesma origem e soma. As partes verticais se somam, claro. Mas as partes horizontais também se somam, mesmo com as massas em lados opostos. O resultado é um momento angular inclinado, que não aponta ao longo do eixo.

### B3-5 · tela: dolly para `H_LADO` (ortográfica, perpendicular ao plano eixo–haste); marca de ângulo reto entre L⃗ e a haste; ângulo de 60° âmbar entre L⃗ e o eixo; CONTA: L_z = 2 m (ℓ sen α)² ω → = 0,113 kg·m²/s · L_⊥ = 2 m ℓ² ω sen α cos α → = 0,196 kg·m²/s
[thoughtful] De lado, dá para ver a geometria inteira. O momento angular fica perpendicular à haste, a sessenta graus do eixo. A parte ao longo do eixo continua sendo o momento de inércia vezes a velocidade angular: zero vírgula cento e treze. Mas a parte transversal é ainda maior: zero vírgula cento e noventa e seis.

### B3-6 · tela: CONTA: L⃗_⊥ = −ω Σ mᵢ zᵢ ρ⃗ᵢ → componentes: Σ m x z · Σ m y z → rótulo rosa `PRODUTOS DE INÉRCIA`; no desenho, os dois retângulos "massa × altura × raio" das duas massas acendem iguais
[thoughtful] A parte transversal vem da soma da massa vezes a altura vezes o raio de cada pedacinho. Em coordenadas, são as somas da massa vezes x vezes z, e da massa vezes y vezes z. Essas somas têm nome: produtos de inércia. Elas medem o quanto a massa está distribuída de um jeito torto em relação ao eixo.

### B3-7 · tela: volta a `H_34` e a girar; L⃗ inteiro gira junto, sempre no plano translúcido (eixo, haste); a ponta desenha um círculo; L_z parada
[curious] E agora, com o haltere girando, o que acontece com esse vetor? A parte transversal está presa ao haltere, então gira junto com ele. A ponta do momento angular desenha um círculo, como no pêndulo. O tamanho fica, a direção muda.

## B4 · EIXO PRINCIPAL

### B4-1 · tela: canto linha 2 `EIXO PRINCIPAL`; um segundo haltere, inclinado para o outro lado, entra no mesmo cubo formando um X; as partes transversais dos dois apontam em sentidos opostos e somam zero; o L⃗ total fica vertical
[thoughtful] Então que distribuição de massa faria essa parte transversal sumir? Um jeito simples: para cada pedacinho, um parceiro igual, na mesma altura, do outro lado do eixo. Aí os produtos de inércia zeram. Por exemplo: um segundo haltere, inclinado para o outro lado, formando um xis. As partes transversais se cancelam, e o momento angular volta a apontar ao longo do eixo.

### B4-2 · tela: CONTA: L⃗_⊥ = 0 → L⃗ = I ω⃗; rótulo `EIXO PRINCIPAL`; três ícones 2.5D pequenos: disco, roda, haltere perpendicular ao eixo
[thoughtful] Quando isso acontece, o momento angular é o momento de inércia vezes o vetor velocidade angular, inteirinho, paralelo ao eixo. Um eixo assim se chama eixo principal de inércia. Um disco girando pelo centro, uma roda bem feita, um haltere perpendicular ao eixo: todos giram em torno de um eixo principal.

### B4-3 · tela: `V_34`: a batata volta, girando no eixo de antes, com L⃗ inclinado girando; selo `REMONTADA`; ela para, gira inteira devagar até um eixo principal (calculado) ficar vertical, e volta a girar; L⃗ alinha com o eixo; os três eixos principais acendem por 1 s em GEO
[curious] E aqui tem um detalhe importante: simetria ajuda, mas não é obrigatória. Essa batata não tem simetria nenhuma. Girando num eixo qualquer, o momento angular sai torto. Mas existem três direções perpendiculares, só dela, em que ele fica alinhado. Girando em torno de qualquer uma delas, não sobra parte transversal. A simetria é só um jeito fácil de achar esses eixos.

## B5 · O QUE OS MANCAIS FAZEM

### B5-1 · tela: canto linha 2 `O QUE OS MANCAIS FAZEM`; `H_34`, haltere torto girando; inset `VISTA DE CIMA` com L⃗_⊥ girando e dL⃗ tangente; CONTA: dL⃗/dt = ω⃗ × L⃗ → \|dL⃗/dt\| = ω L_⊥ → τ = 2 m ℓ² ω² sen α cos α
[thoughtful] De volta ao haltere torto. A velocidade angular é constante, mas a parte transversal do momento angular está mudando de direção. Pela mesma conta do pêndulo, a taxa de variação é a velocidade angular vezes a parte transversal. Pela lei geral, isso precisa de um torque externo desse tamanho.

### B5-2 · tela: CONTA: ω = 2π rad/s · L_⊥ = 0,196 → τ = 1,23 N·m · τ_z = 0 → α = 0; no desenho, τ⃗ azul na origem, horizontal, perpendicular ao plano (eixo, haste), girando junto, sempre 90° à frente de L⃗_⊥
[thoughtful] Com uma volta por segundo, dá um vírgula vinte e três newton metro. E repara na direção: o torque é horizontal, perpendicular ao eixo. Ele não tem componente ao longo do eixo, por isso não muda a velocidade angular. Ele só vira o momento angular. É a resposta da pergunta do começo, agora num corpo rígido.

### B5-3 · tela: os dois mancais (abaixo do haltere, a 0,40 m um do outro) acendem; setas azuis F⃗ horizontais e opostas nos dois, girando; cota GEO d = 0,40 m; CONTA: τ = F d → F = τ/d → = 1,23/0,40 → F = 3,1 N; selo `ATENÇÃO: SÓ A PARTE DO BINÁRIO`
[thoughtful] Quem dá esse torque? O eixo, pelos dois mancais. Eles empurram em sentidos opostos, formando um binário, e esse par de forças gira junto com o haltere. Com os mancais a quarenta centímetros um do outro, cada um empurra com uns três newtons. [short pause] Atenção: essa é só a parte das forças que mantém a rotação imposta. A força total no apoio também inclui segurar o peso.

### B5-4 · tela: selo `CONFERE`; setas azuis F⃗_c nas duas massas, horizontais, para o eixo, opostas, em alturas diferentes; cota vertical de 0,52 m; CONTA: F_c = m ω² ρ → = 0,40 · (2π)² · 0,15 → = 2,37 N → binário = F_c · 2ℓ cos α → = 2,37 · 0,52 → = 1,23 N·m; hold de 2 s
[curious] Dá para conferir por outro caminho, só com forças. Cada massa anda num círculo, então precisa de uma força centrípeta apontando para o eixo: dois vírgula trinta e sete newtons. As duas forças são opostas, mas estão em alturas diferentes, separadas por cinquenta e dois centímetros. Forças opostas em linhas diferentes formam um binário… e dá de novo um vírgula vinte e três newton metro. A geometria do momento angular e as forças contam a mesma coisa.

### B5-5 · tela: mostrador de rotação 1 → 3 voltas/s (a 3 voltas/s, 72° por quadro: mostrar em `CÂMERA LENTA` 1/3); τ e F crescem; CONTA: τ ∝ ω² → × 9 → τ = 11,1 N·m · F = 27,7 N
[thoughtful] E esse torque cresce com o quadrado da velocidade angular. Com três voltas por segundo, ele fica nove vezes maior: quase vinte e oito newtons em cada mancal. Por isso essa história importa tanto para coisas que giram rápido.

## B6 · A RODA

### B6-1 · tela: canto linha 2 `A RODA`; `R_34`: roda de carro (pneu, aro de liga) num eixo horizontal com dois apoios; dois excessos rosa diametralmente opostos, um em cada face (selo `FORA DE ESCALA` no tamanho dos blocos); a roda é posta em três posições e fica parada em cada uma; selo `HIPÓTESES: EIXO HORIZONTAL · ATRITO DESPREZÍVEL`
[thoughtful] Agora uma roda de carro com dois excessos de massa de vinte gramas, em lados opostos e em faces opostas da roda. O centro de massa continua no eixo. Com o eixo horizontal e atrito desprezível, a roda não tem uma posição preferida por causa do peso: deixa ela em qualquer posição, e ela fica. Parada, ela parece balanceada.

### B6-2 · tela: a roda gira (`CÂMERA LENTA`); cada excesso descreve seu círculo; a parte transversal do L do par aparece, como no haltere, e gira; CONTA: Σ m x z ≠ 0
[thoughtful] Mas, girando, é exatamente o haltere torto: duas massas em lados opostos do eixo e em posições diferentes ao longo dele. O produto de inércia não é zero, e o momento angular sai inclinado. O centro de massa pode estar no eixo e ainda existir um binário girante.

### B6-3 · tela: CONTA: v = 100 km/h · R = 0,30 m → ω = v/R → = 92,6 rad/s (≈ 15 voltas/s) → F = m ω² ρ → ≈ 34 N → binário ≈ 7 N·m; setas azuis nos excessos e nos apoios, girando
[thoughtful] A cem quilômetros por hora, uma roda de trinta centímetros de raio dá quase quinze voltas por segundo. Cada excesso de vinte gramas precisa de uma força centrípeta de uns trinta e quatro newtons, mais ou menos o peso de três quilos e meio. E os dois juntos formam um binário de quase sete newton metro, girando quinze vezes por segundo.

### B6-4 · tela: as setas dos apoios alternando; ao lado, gráfico pequeno da força horizontal num apoio × tempo, senoide de ~15 por segundo; CONTA: 50 km/h → binário ÷ 4
[thoughtful] Esse binário transmite esforços periódicos aos apoios e pode provocar vibração. E, como ele cresce com o quadrado da velocidade, a cinquenta quilômetros por hora fica quatro vezes menor. Por isso o efeito costuma aparecer mais em velocidade alta.

### B6-5 · tela: dois contrapesos de aço claro entram, um em cada face, do lado oposto a cada excesso; a parte transversal de L encolhe até zero; L⃗ alinha com o eixo; as setas dos apoios somem; rótulo `EIXO PRINCIPAL`
[thoughtful] O balanceamento dinâmico corrige a distribuição de massa. Neste caso, um contrapeso em cada face, do lado oposto a cada excesso, zera o produto de inércia. Numa roda real, a máquina mede onde e quanto colocar. O eixo da roda volta a ser um eixo principal, o momento angular fica alinhado com ele, e os apoios não precisam mais fazer esse binário.

## SÍNTESE E ENCERRAMENTO

### S1 · tela: canto linha 2 `RESUMO`; `H_34` girando devagar à esquerda com L⃗ girando; à direita, escritas uma a uma: L_z = I_z ω · τ⃗ = dL⃗/dt · Eixo principal: L⃗ = I ω⃗; depois três cartões `PANEL`: `L_z = Iω NÃO É O VETOR INTEIRO` · `L GIRANDO PEDE TORQUE` · `EIXO PRINCIPAL: L ∥ ω`
[calm, satisfied] Então, como pode existir torque sem a velocidade angular aumentar? Quando o torque é perpendicular ao eixo, ele não muda a rapidez do giro: ele muda a direção do momento angular. No pêndulo, isso aconteceu com uma partícula só. No haltere torto e na roda, aconteceu porque a massa estava distribuída torta em relação ao eixo. Resumindo: a componente ao longo do eixo é sempre o momento de inércia vezes a velocidade angular. Mas o vetor inteiro só fica paralelo ao eixo quando o eixo é principal. Fora disso, ele gira com o corpo, e manter o eixo no lugar custa torque.

### S2 · tela: o haltere fica menor à esquerda; à direita, a batata de cubinhos girando se abre e se fecha devagar, sem nada tocando nela
[curious] E fica uma pergunta para você: e se nenhum torque externo agir sobre um corpo que muda de forma enquanto gira? O que acontece com a rotação dele?

### EN · tela: encerramento padrão (logo, anéis violeta, `INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS`); pergunta para os comentários: `E SE A RODA TIVESSE UM EXCESSO SÓ, NUMA FACE SÓ?`
[happy] Se essas conexões ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos. E deixa nos comentários: se a roda tivesse um excesso de massa só, numa face só, os apoios sentiriam só um binário, ou alguma coisa a mais? Até a próxima!

