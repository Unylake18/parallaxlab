# ANEXO A · roteiro com narração v1 (fonte do `ancoras.json`)

Copiado sem reescrita do HANDOFF v1 (2026-11-07). Tags `[ ]` do ElevenLabs v4 não entram na legenda.

## HOOK

### H1 · tela: `C_34`; mesa de ar de aço escovado, disco com aro rosa girando em círculo de 0,60 m em volta do furo, preso pelo fio que desce pelo furo até o puxador embaixo; rastro curto; duas voltas
[curious] Olha essa mesa de ar. O disco desliza praticamente sem atrito, preso a um fio que passa por um furinho bem no meio da mesa e desce até a mão de alguém, lá embaixo.

### H2 · tela: o puxador desce 0,30 m; o disco espirala para dentro e dispara; mais duas voltas rápidas a 0,30 m (tempo real)
[curious] Agora a pessoa puxa o fio. O raio cai pela metade… e o disco passa a dar quatro voltas no tempo em que antes dava uma.

### H3 · tela: congela; seta azul da tração no disco apontando para o furo; topo: `O FIO SÓ PUXA PARA O CENTRO. QUEM EMPURRA O DISCO PARA O LADO?`; hold de 2 s
[thoughtful] Só que repara numa coisa. O fio só consegue puxar o disco para o furo, ou seja, para o centro. Ele nunca empurra para o lado. Então, se ninguém empurra o disco para o lado, de onde veio esse giro a mais?

## ABERTURA

### A1 · tela: logo; `BEM-VINDOS AO PARALLAX LAB`; a mesa girando desfocada atrás
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab.

### A2 · tela: `MOMENTO ANGULAR DE UMA PARTÍCULA`; `NESTE VÍDEO:` e três ícones (reta com ponto ao lado · círculo · espiral) acendendo nas palavras
[thoughtful] Hoje o assunto é o momento angular de uma partícula. A gente vai ver que até um corpo andando em linha reta tem momento angular, descobrir o que faz ele mudar e, no fim, voltar para essa mesa e responder a pergunta.

## B1 · DE p PARA L

### B1-1 · tela: canto linha 2 `DE p PARA L`; `C_34` congelada, fio removido, disco congelado a 0,50 m do furo, a seta magenta p⃗ em sentido anti-horário; CONTA: p⃗ = m v⃗ · F⃗ = dp⃗/dt; cartão pequeno τ⃗ = r⃗ × F⃗
[thoughtful] Vamos começar pelo que a gente já conhece. O momento linear é a massa vezes a velocidade, e a segunda lei de Newton diz que a força resultante é a taxa com que esse momento muda no tempo. E lembrando do torque: para medir o efeito de giro de uma força em torno de um ponto, a gente fazia o produto vetorial do vetor posição com a força.

### B1-2 · tela: r⃗ laranja do furo ao disco; paralelogramo GEO entre r⃗ e p⃗; GM: τ⃗ = r⃗ × F⃗ → L⃗ = r⃗ × p⃗
[thoughtful, emphatic] Então vem a pergunta natural: e se, em vez da força, a gente fizer o mesmo produto com o momento linear? Escolhe um ponto, que aqui vai ser o furo. Desenha o vetor posição, do furo até a partícula, e faz o produto vetorial dele com o momento linear. Isso tem nome: é o momento angular da partícula em relação a esse ponto.

### B1-3 · tela: dolly para `C_L`; L⃗ magenta-claro saindo do furo, perpendicular ao tampo; ícone da mão direita ao lado
[thoughtful] Como todo produto vetorial, o resultado é perpendicular aos dois vetores. O vetor posição e o momento estão no plano da mesa, então o momento angular aponta para fora do plano. O sentido vem da regra da mão direita: os dedos vão do vetor posição para o momento, e o polegar mostra o momento angular. Aqui ele aponta para cima.

### B1-4 · tela: volta a `C_34`; ângulo φ âmbar entre r⃗ e p⃗; braço r⊥ tracejado laranja do furo até a reta de p⃗, ângulo reto; CONTA: |L⃗| = r p sen φ → (r sen φ) p → r⊥ p
[thoughtful] E o tamanho? É a distância ao ponto, vezes o momento, vezes o seno do ângulo entre os dois. Só que repara: a distância vezes o seno é exatamente este segmento aqui, a distância do ponto até a reta por onde o momento passa. É o braço do momento, igualzinho ao braço de alavanca do torque. Ou seja: o momento angular é o momento linear vezes o braço.

### B1-5 · tela: CONTA: [L] = kg·m²/s
[thoughtful] Por isso a unidade é quilograma vezes metro quadrado por segundo. E guarda essa imagem: o que importa não é só quanto momento a partícula tem, mas a que distância do ponto passa a linha do movimento.

## B2 · UMA RETA TAMBÉM GIRA

### B2-1 · tela: canto linha 2 `UMA RETA TAMBÉM GIRA`; dolly para `C_TOPO`; três pinos O₁, O₂ (o furo), O₃; o disco solto atravessa a mesa em linha reta a 1,5 m/s; rótulos m = 0,20 kg, v = 1,5 m/s, d = 0,40 m
[curious] Agora um teste que pega muita gente. Solta o disco do fio e deixa ele atravessar a mesa em linha reta, com velocidade constante. Ninguém faz força nele. Ele tem momento angular?

### B2-2 · tela: em O₁ (sobre a reta), r⃗ sempre ao longo de p⃗; rótulo `L = 0`
[thoughtful] Depende do ponto. Em relação a um ponto em cima da própria reta, o vetor posição e o momento ficam sempre na mesma direção. O braço é zero, então o momento angular é zero.

### B2-3 · tela: em O₂, r⃗ acompanha o disco, braço d constante, ⊗ magenta-claro; CONTA: L_z = −m v d = −0,12 kg·m²/s
[thoughtful] Agora em relação ao furo, que fica a quarenta centímetros da reta. Visto daqui, o disco passa girando no sentido horário em volta do furo. O braço é a distância do furo até a reta, e ele não muda. Então o momento angular vale menos a massa, vezes a velocidade, vezes essa distância: menos zero vírgula doze quilograma metro quadrado por segundo. O sinal negativo é o sentido horário, para dentro da mesa.

### B2-4 · tela: em O₃, do outro lado da reta, ⊙ magenta-claro; `L_z = +0,12`
[thoughtful] E de um ponto do outro lado da reta, o mesmo disco gira no sentido contrário: o momento angular troca de sinal. Ou seja, momento angular não é uma propriedade só da partícula. É da partícula junto com o ponto que você escolheu.

### B2-5 · tela: a partir do furo, três triângulos de Δt = 0,5 s pintados em GEO, mesma base 0,75 m e mesma altura 0,40 m; hold de 2 s
[curious] E tem uma imagem bonita escondida aqui. Liga o furo ao disco e olha a área que esse segmento varre. Em tempos iguais o disco anda distâncias iguais, e a altura até o furo é sempre a mesma. Triângulos com a mesma base e a mesma altura têm a mesma área. O segmento varre áreas iguais em tempos iguais.

### B2-6 · tela: CONTA: dA = ½|r⃗ × v⃗ dt| → dA/dt = |L⃗|/2m = 0,30 m²/s
[thoughtful, emphatic] E isso não é coincidência. A área de cada triângulo fininho é metade do produto vetorial do vetor posição com o deslocamento. Trocando a velocidade pelo momento dividido pela massa, aparece o momento angular: a área varrida por segundo é o momento angular dividido pelo dobro da massa. Momento angular constante, área por segundo constante.

## B3 · O QUE MUDA L

### B3-1 · tela: canto linha 2 `O QUE MUDA L`; sai a mesa; desenho 2.5D: ponto O, pedra rosa; CONTA: L⃗ = r⃗ × p⃗ → dL⃗/dt = (dr⃗/dt) × p⃗ + r⃗ × (dp⃗/dt)
[curious] Então o que faz o momento angular mudar? Vamos derivar a definição no tempo. É a derivada de um produto, então são duas parcelas: a derivada do vetor posição vezes o momento, mais o vetor posição vezes a derivada do momento.

### B3-2 · tela: GM: (dr⃗/dt) vira v⃗ e (dp⃗/dt) vira F⃗; v⃗ × m v⃗ riscado com `PARALELOS` → 0
[thoughtful] A derivada da posição é a velocidade, e a derivada do momento é a força resultante. Só que olha a primeira parcela: velocidade vezes massa vezes velocidade. São dois vetores na mesma direção, e o produto vetorial de vetores paralelos é zero. Ela some.

### B3-3 · tela: GM: r⃗ × F⃗ vira τ⃗ → τ⃗ = dL⃗/dt; F⃗ = dp⃗/dt sobe ao lado; selo `HIPÓTESES: PONTO FIXO · REFERENCIAL INERCIAL · τ E L NO MESMO PONTO`
[thoughtful, emphatic] Sobra o vetor posição vezes a força, que é o torque. Então o torque resultante é a taxa de variação do momento angular. Olha como fica parecido com a segunda lei: a força muda o momento linear, o torque muda o momento angular. Só com um cuidado: o ponto tem que estar parado num referencial inercial, e o torque e o momento angular têm que ser medidos em relação ao mesmo ponto.

### B3-4 · tela: selo `CONFERE`; a pedra de 0,50 kg solta do repouso a d = 0,40 m à direita de O; cota d laranja; seta azul mg; r⃗ acompanha a pedra
[curious] Vamos conferir com algo bem simples: uma pedra de meio quilo solta do repouso, quarenta centímetros à direita de um ponto. Ela cai reto, sem girar nada. Será que ela ganha momento angular em relação a esse ponto?

### B3-5 · tela: CONTA: L_z = x p_y − y p_x → = d(−m g t) → L_z = −m g d t · τ_z = −m g d = −1,96 N·m; gráfico L_z × t, reta de 0 a −1,18 em 0,60 s, triângulo de inclinação; hold de 2 s
[thoughtful] Ganha. O braço continua sendo os quarenta centímetros, mas o momento para baixo cresce com o tempo. Então o momento angular cresce em linha reta: menos a massa, vezes a gravidade, vezes a distância, vezes o tempo. Negativo, porque a pedra passa girando no sentido horário em volta do ponto. E o torque do peso? É menos a massa vezes a gravidade vezes a mesma distância: menos um vírgula noventa e seis newton metro, constante. É exatamente a inclinação dessa reta. Confere.

## B4 · O CÍRCULO

### B4-1 · tela: canto linha 2 `O CÍRCULO`; de volta à mesa em `C_TOPO`, fio preso, órbita de 0,60 m a 1,5 m/s; r⃗ ⟂ v⃗ com ângulo reto; CONTA: |L⃗| = r⊥ p → r⊥ = R → L = m v R → L = m R² ω
[thoughtful] Agora o caso que todo mundo associa ao momento angular: o movimento circular, com o ponto no centro. Aqui o vetor posição é sempre perpendicular à velocidade, então o braço é o próprio raio. O momento angular é a massa, vezes a velocidade, vezes o raio. E como a velocidade é a velocidade angular vezes o raio, fica a massa vezes o raio ao quadrado vezes a velocidade angular.

### B4-2 · tela: GM: m R² vira I → L = I ω; o I rosa acende no aro do disco; números I = 0,072 kg·m² · L = 0,18
[thoughtful] E a massa vezes o raio ao quadrado é o momento de inércia da partícula em relação a esse eixo. Então, no círculo, o momento angular é o momento de inércia vezes a velocidade angular.

### B4-3 · tela: seta azul da tração no disco apontando para o furo; rótulo `τ = 0`; L constante no mostrador
[thoughtful] No movimento circular uniforme, a única força no plano é a tração do fio, e ela aponta para o centro. Força na mesma linha do vetor posição não faz torque. Torque zero, momento angular constante. Faz sentido: velocidade constante, raio constante.

### B4-4 · tela: seta azul F_t tangente ao disco por 1 s; mostrador de ω violeta de 2,5 a 5,0 rad/s; CONTA: τ_z = dL_z/dt → d(m R² ω)/dt → (R FIXO) m R² dω/dt → τ_z = I α
[thoughtful] Agora imagina que alguém dá um empurrão de lado no disco, tangente ao círculo, enquanto o fio segura o raio. Essa força tangencial faz torque, e o momento angular cresce. Escrevendo a lei com o momento angular igual a massa vezes raio ao quadrado vezes velocidade angular, e com o raio fixo, a massa e o raio saem da derivada. Sobra o momento de inércia vezes a aceleração angular. É a segunda lei da rotação, saindo direto de torque igual à variação do momento angular.

### B4-5 · tela: o rótulo `R FIXO` pisca; nota pequena ao lado de τ_z = I α: `SÓ PORQUE R NÃO MUDOU`
[curious] Só que guarda este detalhe, porque ele vai salvar a gente daqui a pouco: o torque igual a momento de inércia vezes aceleração angular só saiu assim porque o raio ficou fixo.

## B5 · FORÇA CENTRAL

### B5-1 · tela: canto linha 2 `FORÇA CENTRAL`; Manim 2.5D: ponto O, partícula, força F⃗ sempre apontando para O; CONTA: τ⃗ = r⃗ × F⃗ → F⃗ ∥ r⃗ → τ⃗ = 0 → dL⃗/dt = 0 → L⃗ constante
[thoughtful, emphatic] Agora a ideia mais poderosa do vídeo. Uma força central é uma força que aponta sempre na linha que liga a partícula a um ponto fixo, para ele ou para longe dele. Como ela fica na mesma direção do vetor posição, o torque em relação a esse ponto é zero. E torque zero significa momento angular constante. Não importa o tamanho da força, nem como ela muda: se ela é central, o momento angular em relação ao centro não muda.

### B5-2 · tela: Manim 2.5D, vista inclinada como a `C_L`: plano GEO, L⃗ fixo perpendicular a ele, a trajetória curva presa ao plano
[thoughtful] Daí saem duas consequências. A primeira: o momento angular é perpendicular ao vetor posição e à velocidade. Se ele não muda de direção, a partícula nunca sai do plano perpendicular a ele. O movimento fica num plano. E se o momento angular for zero, a partícula anda numa reta que passa pelo centro.

### B5-3 · tela: na trajetória, triângulos de mesmo tempo com áreas iguais; dA/dt = |L⃗|/2m acende
[thoughtful] A segunda: lembra que a área varrida por segundo é o momento angular dividido pelo dobro da massa? Se o momento angular é constante, a área por segundo também é. Áreas iguais em tempos iguais, para qualquer força central: um fio, uma mola presa num ponto, a gravidade do Sol.

### B5-4 · tela: construção de Newton: A → B em Δt; prolongamento fantasma B → c (sem chute); chute Δp⃗ magenta em B apontando para O; ponto real C; triângulos OAB, OBc e OBC; reta tracejada paralela a OB passando por c e C; hold de 2 s
[curious] O Newton tinha uma prova geométrica linda disso. Sem força, a partícula iria de A para B e depois para c, com o mesmo passo, e os triângulos teriam a mesma área, como na reta. Agora, no ponto B, ela leva um chute apontando para o centro. Ela vai parar em C, e não em c. Só que o chute foi na direção do centro, então C está numa reta paralela ao segmento até o centro. Mesma base, mesma altura: o triângulo novo tem a mesma área que o antigo. Chute central não muda a área.

### B5-5 · tela: órbita elíptica com o Sol no foco; 12 setores de mesmo tempo alternando tons de GEO; o planeta acelera perto do Sol
[thoughtful] Por isso um planeta anda mais rápido perto do Sol e mais devagar longe dele: perto, o braço é curto, então a velocidade tem que ser maior para varrer a mesma área. O resto das leis dos planetas a gente explora no módulo de gravitação.

## B6 · DE VOLTA À MESA

### B6-1 · tela: canto linha 2 `DE VOLTA À MESA`; `C_34`, a mesa com o disco a 0,60 m; selo `HIPÓTESES: SEM ATRITO · FIO IDEAL · DISCO PEQUENO`; seta azul T⃗ apontando para o furo
[thoughtful] Agora sim, de volta à mesa. O fio passa pelo furo, então a tração aponta sempre para o furo. É uma força central em relação ao furo. Então o momento angular do disco em relação ao furo não muda, mesmo enquanto alguém puxa o fio.

### B6-2 · tela: dolly para `C_TOPO`; reprise da puxada em 0,5× (`CÂMERA LENTA`); mostradores r, I, ω, L; CONTA: L = I ω · I = m r² → m r² ω = constante → r ÷ 2 ⇒ I ÷ 4 ⇒ ω × 4
[thoughtful] No disco, o momento angular é o momento de inércia vezes a velocidade angular, e o momento de inércia é a massa vezes o raio ao quadrado. Quando o raio cai pela metade, o momento de inércia cai para um quarto. Para o produto continuar o mesmo, a velocidade angular tem que quadruplicar: de dois e meio para dez radianos por segundo.

### B6-3 · tela: a puxada congela em r = 0,45 m; CONTA: τ⃗ = dL⃗/dt (`LEI GERAL`) → τ_z = d(I ω)/dt → I dω/dt + (dI/dt) ω → τ_z = I α + İ ω; ao lado, τ_z = I α com `SÓ COM I CONSTANTE`; hold de 2 s
[curious] Mas espera. Torque zero e a velocidade angular aumentando? Isso não contradiz o torque igual a momento de inércia vezes aceleração angular? [short pause] Não contradiz. A lei geral é o torque igual à variação do momento angular. Derivando o momento de inércia vezes a velocidade angular, a regra do produto dá duas parcelas: o momento de inércia vezes a aceleração angular, mais a taxa de variação do momento de inércia vezes a velocidade angular. A versão curta só vale quando o momento de inércia é constante, e lá no círculo ele era. Aqui não é.

### B6-4 · tela: CONTA: 0 = I α + İ ω → I α = −İ ω → I = 0,0405 · ω = 4,44 · İ = −0,054 → α = +5,9 rad/s²
[thoughtful] Com torque zero, a primeira parcela tem que cancelar a segunda. Como o raio está diminuindo, o momento de inércia está caindo, e a aceleração angular sai positiva. No meio da puxada, a quarenta e cinco centímetros do furo, ela dá quase seis radianos por segundo ao quadrado, sem torque nenhum.

### B6-5 · tela: mostradores lado a lado: ω 2,5 → 10 (× 4) e v_θ 1,5 → 3,0 (× 2); CONTA: v_θ = L/(m r) · ω = L/(m r²); hold de 2 s
[thoughtful] E repara numa diferença que obriga a pensar no raio. A velocidade angular quadruplicou, mas a velocidade do disco ao longo da volta só dobrou: de um e meio para três metros por segundo. A velocidade angular depende do raio ao quadrado, a velocidade tangencial depende só do raio.

### B6-6 · tela: triângulos de 0,20 s ao longo da espiral, todos com 0,090 m²; cada um mais baixo e mais largo que o anterior
[thoughtful] E as áreas? Continuam iguais em tempos iguais, durante a puxada inteira. Com o raio menor, o triângulo fica mais baixo, então tem que ficar mais largo: o disco percorre mais arco a cada instante. É a mesma imagem da reta e do planeta.

### B6-7 · tela: congela em r = 0,45 m; inset `ZOOM ×3`: v⃗ = v_r (para o furo) + v_θ (tangente), ângulo âmbar 8,5°; T⃗ para o furo; a componente de T⃗ ao longo de v⃗ acende
[curious] Falta uma pergunta: e a energia? Quem deu energia para o disco correr mais? Olha a velocidade durante a puxada. A trajetória é uma espiral, então a velocidade tem uma parte ao longo da volta e uma parte apontando para o furo. A tração também aponta para o furo. Então a tração tem uma componente na direção do movimento, e faz trabalho positivo. Força central não faz torque, mas pode fazer trabalho.

### B6-8 · tela: barras ciano: K₀ = 0,225 J, K_f = 0,900 J, W = 0,675 J entrando na diferença; selo `ESTADOS COM v_r = 0`; CONTA: W = ΔK = 0,900 − 0,225 = 0,675 J · P = T v_r (0,53 W em r = 0,45 m); hold de 2 s
[thoughtful] A energia cinética vai de zero vírgula duzentos e vinte e cinco para zero vírgula novecentos joule, quatro vezes mais, comparando os dois estados em que o disco não está se aproximando do furo. Os zero vírgula seiscentos e setenta e cinco joule de diferença são o trabalho da mão, entregue pelo fio. Ou seja: o momento angular se conservou, e a energia cinética não.

### B6-9 · tela: selo `ATENÇÃO`; gráfico T × r de 0,75 N em 0,60 m a 6,0 N em 0,30 m, com a nota `PUXADA SEM ACELERAÇÃO RADIAL`
[thoughtful] E por isso fica cada vez mais difícil puxar. Com a puxada sem acelerar o disco para dentro, a tração cresce com o inverso do cubo do raio: de zero vírgula setenta e cinco newton para seis newton quando o raio cai pela metade.

## SÍNTESE E ENCERRAMENTO

### S1 · tela: canto linha 2 `RESUMO`; `C_34` girando devagar, disco a 0,30 m; à direita, escritas uma a uma: L⃗ = r⃗ × p⃗ · τ⃗ = dL⃗/dt · τ⃗ = 0 ⇒ L⃗ constante; depois três cartões `PANEL`: `NÃO PRECISA DE CÍRCULO` · `TORQUE ZERO, ω PODE MUDAR` · `L CONSERVA, K NÃO`
[calm, satisfied] A pergunta inicial está respondida. Ninguém empurrou o disco para o lado. A tração é central, então não faz torque, e o momento angular em relação ao furo ficou constante. Com o raio menor, a única forma de manter esse momento angular é girar mais rápido. E a energia extra veio da mão, que fez trabalho pelo fio. Resumindo em três ideias: momento angular não precisa de círculo; torque zero não quer dizer velocidade angular constante; e conservar momento angular não é conservar energia.

### S2 · tela: a mesa fica menor à esquerda; à direita, uma nuvem de partículas girando juntas em volta de um eixo, cada uma com o seu r⃗ × p⃗ pequeno
[curious] E fica uma pergunta para você: e se, em vez de uma partícula, for um corpo inteiro girando, feito de milhões delas? Como somar todos esses momentos angulares?

### EN · tela: encerramento padrão (logo, anéis violeta, `INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS`); pergunta para os comentários: `UMA PEDRA CAINDO RETO TEM MOMENTO ANGULAR? EM RELAÇÃO A QUAL PONTO?`
[happy] Se essas conexões ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos. E deixa nos comentários: em relação a qual ponto uma pedra caindo reto tem momento angular zero? Até a próxima!

## FIM
