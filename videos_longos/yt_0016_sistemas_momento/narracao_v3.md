# yt_0016 — MOMENTO EM SISTEMAS · roteiro com narração v3 (Parte 2 de 2 do yt_0015)

v3 (2026-10-29, handoff_v4.md, Anexo A): a v2 com o hook reescrito (H1–H3, mais curto; o par da terceira lei é cavalo × pedra pela corda) e as linhas `tela:` de A2, A6, T8-6, T9-5 a T9-7, T10-1, C-1 e C-2 atualizadas. O resto da fala é igual à v2, palavra por palavra (v2 em `narracao_sugestao.md`).

Data: 2026-10-28 (v2: abertura ligada ao vídeo anterior, T7 derivado passo a passo a partir de dois corpos, linhas `tela:` com PALCO vivo e 3D; o resto da fala igual à v1). v1: 2026-10-27 (`narracao_sugestao_v1.md`). Fonte da física e dos números: `pautas/yt_0016_sistemas_briefing.md` (aprovado pelo Kaio, com os ajustes de T8, T9 e T10 e a correção de que a
energia do caçador fica na **bala**). Distribuição com o yt_0015 conferida: aqui entram a derivação para N partículas, o cavalo e a pedra, a escolha do sistema, a divisão da
energia e E6–E9 + coda. Padrão: `padrao_video_longo.md` §5 e `roteiro_voz_elevenlabs_v4.md`. Tom de professor de cursinho, "a gente" e "você", nunca a letra solta.

**Como ler:** cada `###` é uma âncora (evento visual). A linha `tela:` diz o que aparece; a fala começa ~0,15 s depois e manda: a cena se estica. Tags `[ ]` do
ElevenLabs v4, em inglês, **um só descritor**, uma por trecho, valendo até a próxima; não entram na legenda. Pontos em que a tela mostra símbolo, a fala diz o nome por extenso.

**Regras de tela da série (Kaio, 2026-10-28):** nada de livro na tela nem na fala (fontes só na descrição); selo de ligação com a teoria no lugar do selo de fonte; nunca tela só de álgebra (esquema/animação no palco enquanto a conta corre, variáveis saindo do desenho para a conta); exercícios com esquema fixo à esquerda e álgebra à direita.

**Cores:** velocidade violeta, momento magenta, força azul-claro, impulso `#9CC7FF`, energia cinética ciano, calor laranja, corpos em aço. **Canto:** linha 1
`MECÂNICA · MOMENTO EM SISTEMAS`; linha 2 = capítulo (tabela da §4 do briefing).

---

## HOOK

### H1 — tela: (3D) o cavalo já andando desde o primeiro quadro, puxando a pedra pela corda presa no balancim; câmera lateral baixa; as setas T⃗ (na pedra, para a frente) e −T⃗ (no balancim, para trás) entram juntas
[curious] O cavalo puxa a pedra para a frente pela corda. E, pela terceira lei de Newton, a pedra puxa o cavalo para trás com uma força do mesmo tamanho.

### H2 — tela: (3D) as duas setas pulsam juntas; = entre os módulos; push-in lento até a corda; interrogação suave sobre o cavalo
Se as duas forças são iguais e opostas, como é que o cavalo anda, e ainda leva a pedra junto?

### H3 — tela: (3D) a câmera recua; o cavalo apaga para 40%; texto central SE A CORDA PUXA O CAVALO PARA TRÁS COM A MESMA FORÇA, COMO ELE ANDA?
A resposta está em duas ideias: o que é um sistema, e quais forças mudam o momento dele.

## ABERTURA

### A1 — tela: logo; BEM-VINDOS AO PARALLAX LAB
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab!

### A2 — tela: miniatura parada do último quadro do hook (zoom lento), com a pergunta embaixo; MOMENTO EM SISTEMAS · NESTE VÍDEO: O QUE MUDA O MOMENTO DE VÁRIOS CORPOS
[thoughtful] Hoje o assunto é o momento de vários corpos juntos. E a gente começa exatamente onde o vídeo anterior terminou: com esse cavalo e essa pergunta.

### A3 — tela: PALCO: o disco do vídeo anterior deslizando; a seta da força resultante (azul-claro) age por um instante e a seta do momento (magenta) cresce; a curva da força no tempo se desenha ao lado com a área preenchida (#9CC7FF). CONTA: F⃗_res = dp⃗/dt → J⃗ = ∫F⃗_res dt = Δp⃗, cada símbolo saindo do desenho (TransformFromCopy). Painel e conta sem se tocar (folga ≥ 0,25)
No vídeo anterior, a gente olhou para um corpo só. A pergunta era: o que uma força faz com o momento de um corpo? E a resposta foi: a força resultante é a taxa de variação do momento, e, somada no tempo, o impulso resultante é a variação do momento. A área embaixo da curva da força.

### A4 — tela: PALCO: os dois discos do vídeo anterior colidindo no colchão de ar; durante o contato, as duas setas de força iguais e opostas; as setas de momento antes e depois. CONTA: Δp⃗₁ = −Δp⃗₂ → P⃗ = CONSTANTE (DOIS CORPOS SOZINHOS)
Depois, com dois discos batendo, a gente viu que o momento que um ganha é exatamente o que o outro perde. Dois corpos sozinhos, sem nada de fora mexendo neles: o momento total não muda.

### A5 — tela: PALCO: volta o cavalo (3D) puxando a pedra; primeiro uma fronteira tracejada só em volta do cavalo, e a força da corda nele aparece em azul-claro, como uma força sobre ele; depois a fronteira cresce até envolver cavalo, corda e pedra, e a mesma seta fica cinza apagado. Legenda curta embaixo: UM CORPO: TODA FORÇA CONTA → SISTEMA: INTERNAS × EXTERNAS
[curious] Só que o mundo real quase nunca é tão limpo. O cavalo pisa no chão, a pedra raspa no chão, a corda liga os dois. E aqui está a diferença entre os dois vídeos. Quando você olha para o cavalo sozinho, a força da corda é uma força como outra qualquer, e entra na força resultante dele. Mas, quando você olha para o cavalo, a corda e a pedra juntos, essa mesma força passa a ser uma força de dentro. A pergunta de hoje é: as forças de dentro mudam o momento do conjunto, ou não?

### A6 — tela: CENTRO, sem o cavalo: mapa dos dois vídeos em duas colunas: VÍDEO ANTERIOR · UM CORPO → F⃗_res = dp⃗/dt (apagado, ícone do disco); HOJE · MUITOS CORPOS → ? (ícone das três esferas); o ? vai para o canto da CONTA e vira dP⃗/dt = F⃗^ext no fim do T7
[thoughtful] No vídeo anterior, a conservação do momento era um fato sobre dois corpos isolados. Hoje ela vira uma ferramenta para qualquer sistema, mesmo com forças de fora agindo. E, no caminho, a gente aprende a escolher o sistema certo para cada problema.

## T7 — SISTEMAS DE PARTÍCULAS

### T7-1 — tela: PALCO (3D): três esferas de aço ligadas por molas, flutuando e vibrando devagar, dentro de uma fronteira tracejada (SISTEMA); as molas pulsam em azul-claro (internas); peso e normal entram de fora (externas)
[thoughtful] Primeiro, uma combinação. Um sistema é o grupo de corpos que a gente escolhe acompanhar, dentro de uma fronteira que a gente mesmo desenha. As forças que os corpos de dentro fazem entre si são as forças internas. As que vêm de fora da fronteira são as forças externas. Essa escolha é nossa, e ela vai decidir tudo.

### T7-2 — tela: PALCO: só duas esferas, a primeira e a segunda, ligadas por uma mola, oscilando; as forças da mola em cada uma (azul-claro, iguais e opostas) e o peso de cada uma vindo de fora. CONTA: dp⃗₁/dt = F⃗₁₍₂₎ + F⃗₁^ext e dp⃗₂/dt = F⃗₂₍₁₎ + F⃗₂^ext, cada força saindo do desenho por TransformFromCopy
Comece pelo caso mais simples: dois corpos ligados por uma mola. Sobre o primeiro agem a força da mola, que vem do segundo, e as forças de fora, como o peso. Pela segunda lei na forma com o momento, a taxa de variação do momento do primeiro é a soma dessas forças. O mesmo vale para o segundo.

### T7-3 — tela: CONTA: as duas equações somadas: d(p⃗₁ + p⃗₂)/dt = F⃗₁₍₂₎ + F⃗₂₍₁₎ + F⃗^ext; F⃗₁₍₂₎ e F⃗₂₍₁₎ se cancelam (TransformByGlyphMap) → dP⃗/dt = F⃗^ext. PALCO: as duas setas da mola piscam juntas quando se cancelam na conta; as esferas continuam oscilando
[curious] Agora soma as duas equações. À esquerda, aparece a taxa de variação do momento total. À direita, as duas forças da mola: pela terceira lei, uma é igual e oposta à outra, então elas se cancelam. Sobra só a força externa. A mola continua trabalhando, mas o momento total só responde ao que vem de fora.

### T7-4 — tela: PALCO: volta a terceira esfera, presa às outras por molas; a partícula escolhida acende. CONTA: para a partícula i: dp⃗ᵢ/dt = Σⱼ F⃗ᵢ₍ⱼ₎ + F⃗ᵢ^ext; legenda: i RECEBE DE j
[thoughtful] E com muitos corpos? Pega uma partícula qualquer do sistema. A taxa de variação do momento dela é a soma das forças que as outras partículas do sistema fazem nela, mais a força externa sobre ela.

### T7-5 — tela: CONTA: soma sobre todas as partículas: dP⃗/dt = Σᵢ Σⱼ F⃗ᵢ₍ⱼ₎ + F⃗^ext, com P⃗ = soma dos momentos (magenta); PALCO: as três esferas seguem vibrando, com a seta do momento total (magenta) parada no meio delas
Agora a gente soma essa equação para todas as partículas. À esquerda, a soma dos momentos de todas vira o momento total do sistema. À direita, sobram duas somas: a soma dupla das forças internas e a força externa total.

### T7-6 — tela: PALCO à esquerda (as três esferas) + matriz de pares (i, j) à direita; quando a célula (1, 2) e a (2, 1) acendem, a mola entre a primeira e a segunda esfera pulsa no PALCO no mesmo instante; depois (1, 3)/(3, 1) e (2, 3)/(3, 2); a diagonal é vazia
[curious] E a soma dupla das forças internas? Olha a tabela. Cada linha é quem recebe a força, cada coluna é quem faz a força. A força que a partícula um recebe da dois está aqui, e a força que a dois recebe da um está aqui. É o mesmo par da mola que a gente acabou de ver. Pela terceira lei, as duas são iguais e opostas, então a soma delas dá zero. A mesma coisa acontece com cada par. Todas as células se apagam duas a duas.

### T7-7 — tela: dP⃗/dt = F⃗^ext (destaque, o ponto de interrogação do A6 vira essa equação); PALCO: as esferas vibrando e a seta magenta do momento total parada; selo DICA: PRIMEIRO DEFINA O SISTEMA. SÓ FORÇA EXTERNA ENTRA NA VARIAÇÃO DO MOMENTO TOTAL
[emphatic] Sobrou só isto: a taxa de variação do momento total é a força externa resultante. As forças internas, por maiores que sejam, não aparecem. Ou seja, só uma força de fora muda o momento total de um sistema.

### T7-8 — tela: PALCO (3D): um disco sobre gelo recebe um binário (duas forças externas iguais e opostas em pontos diferentes); o disco gira e o centro não sai do lugar. CONTA: SE A FORÇA EXTERNA RESULTANTE = 0 → P⃗ CONSTANTE
[thoughtful] Repara numa sutileza. Para o momento total se conservar, o sistema não precisa estar isolado do mundo. Basta a força externa resultante ser zero. Um exemplo bonito: duas forças externas iguais e opostas, aplicadas em pontos diferentes de um disco. O momento total não muda, mas o disco gira. Essa história de girar fica para o módulo de rotação.

### T7-9 — tela: PALCO: uma bola lançada em parábola, com a seta do peso só na vertical e a componente horizontal do momento (magenta) de tamanho fixo o tempo todo; CONTA: dPₓ/dt = F^ext_x; dP_y/dt = F^ext_y; no fim, uma linha pequena: MOMENTO DAS PARTÍCULAS + MOMENTO DO CAMPO = CONSTANTE, com duas cargas em movimento e uma nuvem de campo esboçadas
E tem mais: isso vale componente por componente. Se não há força externa na horizontal, o momento horizontal se conserva, mesmo que o vertical mude. E lembra do vídeo anterior: quando a terceira lei falha, como entre cargas em movimento, a conservação continua valendo se a gente contar o momento do campo.

## T8 — FORÇA INTERNA NÃO MOVE O SISTEMA

### T8-1 — tela: (3D) volta o cavalo, que arrasta a pedra acelerando devagar (0,32 m/s²) do começo ao fim do bloco; fronteira tracejada em volta de cavalo, corda e pedra; a tensão na corda em cinza apagado (INTERNA); aparecem em azul-claro: atrito do chão nas patas (para a frente) e atrito do chão na pedra (para trás) (EXTERNAS)
[thoughtful] Vamos voltar ao cavalo, agora com a ferramenta nova. Desenha a fronteira em volta do cavalo, da corda e da pedra. A força da corda é interna: ela puxa a pedra para a frente e o cavalo para trás, e some da conta do sistema. As forças que contam são as externas na horizontal: o atrito do chão nas patas do cavalo, que empurra para a frente, e o atrito do chão na pedra, que puxa para trás. O peso e a normal ficam na vertical e se cancelam.

### T8-2 — tela: cavalo 600 kg; pedra 800 kg; ATRITO CINÉTICO NA PEDRA = 0,3 · 800 · 9,8 = 2.352 N; empurrão do chão nas patas = 2.800 N
Vamos dar números. O cavalo tem seiscentos quilogramas, a pedra tem oitocentos, e a pedra já está deslizando, então vale o coeficiente de atrito cinético, zero vírgula três. O atrito do chão na pedra é zero vírgula três vezes oitocentos vezes nove vírgula oito: dois mil, trezentos e cinquenta e dois newtons, para trás. Suponha que o chão empurre o cavalo para a frente com dois mil e oitocentos newtons.

### T8-3 — tela: SISTEMA: (2.800 − 2.352) = (600 + 800) · a; a = 0,32 m/s²
[curious] E a corda? Nem aparece. A força externa resultante é dois mil e oitocentos menos dois mil, trezentos e cinquenta e dois, quatrocentos e quarenta e oito newtons, e ela acelera a massa total, mil e quatrocentos quilogramas. A aceleração do conjunto é zero vírgula trinta e dois metros por segundo ao quadrado.

### T8-4 — tela: separando: PEDRA: T − 2.352 = 800 · 0,32 → T = 2.608 N; CAVALO: 2.800 − T = 600 · 0,32 → 192 N; os dois lados batem
Agora, só para conferir, separa os dois corpos. Na pedra: a tensão menos o atrito dá a massa dela vezes a aceleração, então a corda puxa com dois mil, seiscentos e oito newtons. No cavalo: o empurrão do chão menos essa mesma tensão deixa cento e noventa e dois newtons, e isso é exatamente a massa do cavalo vezes a aceleração. Fecha. A corda tem a mesma tensão nas duas pontas.

### T8-5 — tela: no cavalo: seta do chão (2.800 N, para a frente) maior que a seta da corda (2.608 N, para trás); resposta em destaque: O CAVALO ANDA PORQUE O CHÃO O EMPURRA; A CORDA SÓ TRANSMITE
[emphatic] Resposta da pergunta do começo. A corda puxa o cavalo para trás com dois mil, seiscentos e oito newtons, sim. Só que o chão empurra o cavalo para a frente com dois mil e oitocentos. O cavalo não anda porque ganha a briga com a pedra: ele anda porque ganha a briga com o chão.

### T8-6 — tela: (3D) o gelo surge sob as patas; desaceleração em câmera lenta (v de ~3,5 até 0); depois as patas escorregam no lugar; na CONTA, CHÃO FIRME 2.800 N × GELO 588 N, cada uma contra os 2.352 N da pedra: ANDA / PARA
[curious] E se o chão sob as patas virasse gelo? Com um coeficiente de atrito estático de uns zero vírgula um, o chão só consegue empurrar o cavalo com uns quinhentos e oitenta e oito newtons, muito menos que os dois mil, trezentos e cinquenta e dois da pedra, que continua deslizando do mesmo jeito. O cavalo escorrega e o conjunto desacelera. O cavalo é o mesmo, a corda é a mesma. O que mudou foi a força externa.

### T8-7 — tela: ilustração leve: Cyrano sentado numa placa de ferro, jogando um ímã para cima; fronteira tracejada em volta de pessoa, placa e ímã; CORDA E ÍMÃ: SÓ FORÇAS INTERNAS
[thoughtful] Uma ideia clássica, do Cyrano de Bergerac: sentar numa placa de ferro e jogar um ímã para cima, para o ímã puxar a placa e subir até a Lua. Não funciona. Pessoa, placa e ímã formam um sistema em que as forças são todas internas, e elas não mudam o momento do conjunto.

### T8-8 — tela: pessoa andando; seta do atrito do chão no pé, para a frente; selo DICA: QUEM ACELERA O CONJUNTO É A FORÇA EXTERNA. A CORDA SÓ TRANSMITE
Até o jeito como a gente anda é isso. A gente empurra a Terra para trás, e o atrito do chão empurra a gente para a frente. É por isso que andar no gelo é tão difícil. Guarda essa ideia, que a gente volta a ela daqui a pouco.

## T9 — ESCOLHER O SISTEMA

### T9-1 — tela: PALCO: bola de 1 kg caindo 10 m em loop lento durante todo o bloco (a conta corre à direita); fronteira só em volta da bola; seta de peso (externa); P⃗ crescendo (magenta)
[thoughtful] Agora a segunda ideia: a escolha do sistema. Uma bola de um quilograma cai de dez metros e chega com catorze metros por segundo. Se o sistema é só a bola, o momento dela cresce o tempo todo. Está tudo certo: o peso é uma força externa, e a força externa muda o momento.

### T9-2 — tela: (3D opcional) a câmera abre até mostrar a Terra; a fronteira se expande e inclui a Terra; a bola segue caindo em loop; seta de momento da Terra em sentido oposto; P⃗ total = 0 em todo instante; Terra: 2,3×10⁻²⁴ m/s
[curious] Agora aumenta o sistema: bola mais Terra. A força entre elas passa a ser interna, e o momento total fica zero o tempo todo. A bola ganha momento para baixo, e a Terra ganha o mesmo tanto para cima. Só que a Terra é tão pesada que a velocidade dela é de uns dois vírgula três vezes dez elevado a menos vinte e quatro metros por segundo, impossível de perceber. A conta fecha, mesmo que ninguém note.

### T9-3 — tela: eixo x para a direita; chão com atrito; dois blocos de aço, leve (1 kg) à esquerda e pesado (2 kg) à direita, com uma mola entre eles; a mola dispara: leve vai para a esquerda a 2 m/s, pesado para a direita a 1 m/s
[thoughtful] Um exemplo mais interessante. Dois blocos num chão com atrito, com uma mola entre eles: um de um quilograma, outro de dois. Marca o eixo para a direita. A mola dispara os dois num instante tão curto que o atrito nem conta. O leve sai para a esquerda a dois metros por segundo, e o pesado para a direita a um metro por segundo. O momento total, logo depois, continua zero: menos dois quilogramas metro por segundo de um lado, mais dois do outro.

### T9-4 — tela: MASSAS IGUAIS: setas de atrito iguais e opostas; P(t) = 0 o tempo todo
[thoughtful] Primeiro, o caso de massas iguais, só para comparar. Os dois blocos têm o mesmo atrito, em sentidos opostos. A força externa resultante é zero, o momento total fica zero, e os dois param juntos.

### T9-5 — tela: o evento roda uma vez em câmera lenta 4× com os gráficos se desenhando (T9-5 a T9-7)
[curious] Mas com massas diferentes, o atrito não se cancela. O leve está indo para a esquerda, então o atrito nele aponta para a direita: um vírgula noventa e seis newtons. O pesado vai para a direita, então o atrito nele aponta para a esquerda: três vírgula noventa e dois. A força externa resultante fica menos um vírgula noventa e seis newtons, e o momento total começa a descer.

### T9-6 — tela: em T9-6 o ponto (0,51 s; −1,0) acende com o bloco pesado parado (realce, sem replay)
[thoughtful] O pesado para primeiro, depois de meio segundo. Nesse instante, só o leve ainda está se movendo, e o momento total é menos um quilograma metro por segundo, o ponto mais baixo do gráfico. Depois, o leve continua deslizando e para em pouco mais de um segundo. O momento total sobe de volta até zero.

### T9-7 — tela: em T9-7 um replay desenha P_Terra(t) embaixo, espelhado; depois tudo fica; soma dos dois gráficos = 0; selo DICA: NÃO CONSERVA? PERGUNTE QUEM FICOU DE FORA DO SISTEMA
[emphatic] E o momento que desapareceu? Foi para a Terra. Inclui a Terra no sistema e o momento total volta a ser zero a todo instante: o que os blocos perdem, o chão ganha, e depois devolve. Quando a conta do momento não fecha, a primeira pergunta é sempre: quem eu deixei de fora do sistema?

## T10 — COMO A ENERGIA SE DIVIDE

### T10-1 — tela: PALCO: os dois blocos do T9 (sem atrito agora) disparam pela mola uma vez, com as setas de momento magenta iguais e as barras de energia crescendo juntas; os blocos param em batentes nas bordas do PALCO e ficam, as barras ficam; CONTA: m₁v₁ = m₂v₂ (módulos); um replay só em T10-3
[thoughtful] Mais uma consequência. Dois corpos saem do repouso empurrados só por forças internas, como os dois blocos da mola. O momento total continua zero, então os momentos dos dois têm o mesmo módulo, em sentidos opostos. A massa do primeiro vezes a velocidade dele é igual à massa do segundo vezes a velocidade dele.

### T10-2 — tela: m₁v₁ = m₂v₂ → v₁/v₂ = m₂/m₁ → K₁/K₂ = (m₁/m₂)(v₁/v₂)² = m₂/m₁ (passo a passo, TransformMatchingTex)
[curious] E a energia cinética? Do vídeo anterior, a gente sabe que a energia cinética é o quadrado do momento dividido por duas vezes a massa. Se o momento é igual, a energia fica inversamente proporcional à massa. Passo a passo: a razão das velocidades é a razão inversa das massas, e a razão das energias é a massa do segundo dividida pela massa do primeiro.

### T10-3 — tela: barras: momentos iguais (magenta) e energias diferentes (ciano); blocos de 1 kg e 2 kg: K = 2 J e 1 J; fração do mais leve: 2/3 (67%); massas iguais: 50%
[emphatic] Ou seja, o momento se divide igualmente, mas a energia, não. Com os nossos blocos, o leve fica com dois joules e o pesado com um: dois terços da energia para o mais leve. E quanto maior a diferença entre as massas, maior a fração da energia cinética que fica com o mais leve. Guarda esse resultado para o caçador.

### T10-4 — tela: selo DICA: MESMO MOMENTO: QUANTO MAIS LEVE, MAIOR A FRAÇÃO DA ENERGIA
Com a teoria na mão, vamos aos exercícios.

## E6 — AGARRAR OU REBATER

### E6-1 — tela: selo de ligação SISTEMA: VOCÊ + A BOLA; PALCO fixo à esquerda o exercício inteiro: (3D) o manequim do yt_0015 parado no gelo; uma bola de 0,600 kg chega a 10,0 m/s; fronteira: VOCÊ + A BOLA
[thoughtful] Primeiro exercício. Você está parado no gelo, sem atrito, com setenta quilogramas. Um amigo joga uma bola de seiscentos gramas a dez metros por segundo. O sistema é você mais a bola, e na horizontal não há força externa.

### E6-2 — tela: AGARRA: V = 0,600 · 10,0 / 70,6 = 0,085 m/s; energia: 30 J → 0,25 J
Se você agarra a bola, os dois seguem juntos. O momento antes era só o da bola, seis quilogramas metro por segundo. Dividindo pela massa total, setenta vírgula seis, você sai a uns oito centímetros e meio por segundo.

### E6-3 — tela: REBATE: a bola volta a 8,0 m/s; 70,0 · V = 0,600 · (10,0 + 8,0); V = 0,154 m/s; energia total: 30 J → 20 J; miniatura do vídeo anterior (parar × rebater)
[curious] E se a bola bate no seu peito e volta a oito metros por segundo? Agora a bola perde todo o momento que tinha e ainda ganha momento para o outro lado. Tudo isso vai para você: uns quinze centímetros por segundo, quase o dobro. É o mesmo efeito da parede do vídeo anterior: rebater transfere mais momento do que agarrar.

### E6-4 — tela: o PALCO continua (replay lento das duas versões, agarrar e rebater); na CONTA à direita, o balanço de energia em barras: AGARRAR: antes 30 J, depois 0,25 J (laranja: ≈ 29,7 J viram calor); REBATER: antes 30 J, depois ≈ 20 J; MOMENTO: CONSERVADO NOS DOIS; selo DICA: NO MOMENTO O SISTEMA É VOCÊ + A BOLA. REBATER TRANSFERE MAIS QUE AGARRAR
[emphatic] E olha a energia. Antes, a bola tinha trinta joules. Agarrando, sobram uns zero vírgula vinte e cinco: quase tudo vira calor e deformação. Rebatendo, sobram uns vinte. O momento se conservou nos dois casos, e a energia, em nenhum. O momento se conserva em qualquer colisão. A energia só se conserva se a colisão for elástica.

## E7 — O CAÇADOR NO LAGO

### E7-1 — tela: selo de ligação MOMENTO POR COMPONENTE; PALCO fixo à esquerda o exercício inteiro: (3D) o manequim como caçador, com a arma, no lago congelado; 72,5 kg; bala de 4,20 g a 965 m/s; tiro horizontal
[thoughtful] Segundo exercício. Um caçador está parado num lago congelado, sem atrito. Ele e a arma têm setenta e dois vírgula cinco quilogramas. A bala tem quatro vírgula dois gramas e sai a novecentos e sessenta e cinco metros por segundo.

### E7-2 — tela: tiro horizontal: V = 0,00420 · 965 / 72,5 = 0,0559 m/s
Atirando na horizontal, o momento total era zero e continua zero. Então o recuo é o momento da bala dividido pela massa do caçador: uns cinco vírgula seis centímetros por segundo.

### E7-3 — tela: agora o tiro sai a 56° acima da horizontal; aparece a normal do gelo (azul-claro) empurrando para cima durante o disparo
[curious] Agora ele atira para cima, a cinquenta e seis graus. A bala leva momento para cima... e o caçador não afunda no gelo. Quem segurou ele?

### E7-4 — tela: P_y NÃO SE CONSERVA (a normal é externa e impulsiva); P_x SE CONSERVA; V = 0,0559 · cos 56° = 0,031 m/s
[emphatic] Foi o gelo. Durante o disparo, a normal cresce de repente e absorve o momento vertical. Então, na vertical, o sistema não está isolado. Na horizontal, está. Por isso só a parte horizontal do momento da bala volta no caçador: o recuo cai para uns três centímetros por segundo, o anterior vezes o cosseno de cinquenta e seis graus.

### E7-5 — tela: o PALCO continua (o caçador recuando devagar no gelo e a bala saindo, em loop); na CONTA à direita, duas barras de momento iguais (magenta); energias: bala ≈ 1.956 J, caçador ≈ 0,11 J (ciano); razão ≈ 17.262 = 72,5 / 0,0042; ≈ 99,994% NA BALA; selo DICA: ISOLADO NA HORIZONTAL NÃO É ISOLADO NA VERTICAL
[curious] E a energia? Volta ao nosso resultado: o momento é igual, então quem tem menos massa fica com mais energia. A bala sai com quase dois mil joules. O caçador recua com uns onze centésimos de joule. É uma razão de uns dezessete mil, que é só a massa do caçador dividida pela da bala. Praticamente toda a energia cinética fica na bala. Por isso o recuo não machuca, e a bala sim.

## E8 — OS GASES DO RIFLE

### E8-1 — tela: selo de ligação QUEM ESTÁ NO SISTEMA?; rifle de 2,80 kg; bala de 7,20 g sai a 601 m/s EM RELAÇÃO AO CANO; rifle recua a 1,85 m/s EM RELAÇÃO AO CHÃO
[curious] Mais um tiro, agora com uma pegadinha. A bala sai a seiscentos e um metros por segundo em relação ao cano, e o rifle recua a um vírgula oitenta e cinco metros por segundo em relação ao chão. A pergunta: os gases que saem junto carregam algum momento?

### E8-2 — tela: velocidade da bala em relação ao chão: 601 − 1,85 = 599,15 m/s; p da bala = 4,31 kg·m/s; p do rifle = −5,18 kg·m/s
[thoughtful] Primeiro, a velocidade da bala em relação ao chão: o cano está andando para trás, então ela é seiscentos e um menos um vírgula oitenta e cinco. O momento da bala fica em quatro vírgula trinta e um quilogramas metro por segundo, para a frente. O do rifle, cinco vírgula dezoito, para trás.

### E8-3 — tela: as setas não fecham; aparece uma nuvem de gases com p dos gases = +0,866 kg·m/s; agora a soma dá zero
Só que o momento total antes era zero, e essas duas setas não se cancelam. Falta alguém no sistema: os gases. Eles carregam cerca de zero vírgula oitenta e sete quilogramas metro por segundo para a frente.

### E8-4 — tela: SISTEMA = BALA + RIFLE + GASES; selo DICA: VELOCIDADE EM RELAÇÃO AO CANO NÃO É EM RELAÇÃO AO CHÃO. A CONTA FECHA COM OS GASES
[emphatic] A lição é a mesma dos blocos com a Terra: a conservação vale para o sistema inteiro. Se a conta não fecha, quase sempre tem alguém escondido que você deixou de fora.

## E9 — NEWTON E A LUZ

### E9-1 — tela: selo de ligação IMPULSO NORMAL; PALCO (3D): o tanque de água, com um fluxo de corpúsculos; retrato pequeno estilizado do século XVII; raio de luz desenhado como um fluxo de bolinhas (corpúsculos)
[curious] Para fechar, um problema que mistura física e história. No século dezessete, o Newton defendia que a luz era feita de corpúsculos, bolinhas muito rápidas. Será que o impulso consegue explicar a reflexão e a refração da luz nesse modelo?

### E9-2 — tela: um corpúsculo bate num espelho; o impulso aparece perpendicular à superfície; componente tangencial igual, normal invertida; θ₁′ = θ₁
[thoughtful] Comece pela reflexão. O espelho só empurra na direção perpendicular à superfície. Então o impulso é todo normal: ele inverte a parte normal da velocidade e não mexe na parte paralela ao espelho. O resultado é que o ângulo de reflexão é igual ao de incidência.

### E9-3 — tela: agora ar → água; o impulso normal acelera o corpúsculo para dentro da água; a componente tangencial se mantém; v₁ sen θ₁ = v₂ sen θ₂
Agora a passagem do ar para a água. No modelo, a superfície dá de novo um impulso só normal. Então a parte da velocidade paralela à superfície se conserva. Escrevendo isso com os ângulos medidos a partir da normal: a velocidade no ar vezes o seno do ângulo no ar é igual à velocidade na água vezes o seno do ângulo na água.

### E9-4 — tela: sen θ₁ / sen θ₂ = CONSTANTE (a forma da lei de Snell) → no modelo de Newton: = v₂/v₁
[emphatic] E aí aparece a forma da lei de Snell: o seno de um ângulo dividido pelo seno do outro é uma constante. Só que, no modelo de Newton, essa constante é a velocidade na água dividida pela velocidade no ar.

### E9-5 — tela: o raio se aproxima da normal na água (θ₂ < θ₁) → v₂/v₁ > 1 → NEWTON: LUZ MAIS RÁPIDA NA ÁGUA
[curious] Agora olha o que a gente vê de verdade: ao entrar na água, a luz se aproxima da normal. O ângulo na água é menor. Então, pelo modelo, a velocidade na água teria que ser maior que no ar. Os corpúsculos acelerariam ao entrar na água.

### E9-6 — tela: 1850 · FOUCAULT: A LUZ É MAIS LENTA NA ÁGUA; o "v₂ > v₁" é riscado; ao lado, na descrição ondulatória: sen θ₁ / sen θ₂ = v₁/v₂
[excited] Por quase dois séculos, ninguém conseguiu medir. Até que, em mil oitocentos e cinquenta, o Foucault mediu a luz na água... e ela era mais lenta. A previsão do modelo corpuscular de Newton caiu. Na descrição ondulatória, a relação entre os ângulos e as velocidades aparece invertida, e é essa que a natureza segue.

### E9-7 — tela: o PALCO continua (corpúsculos no tanque, agora apagados); na CONTA: IMPULSO CERTO + MODELO ERRADO = PREVISÃO TESTÁVEL; selo DICA: O IMPULSO É NORMAL: SÓ A COMPONENTE NORMAL DA VELOCIDADE MUDA
[thoughtful] E repara que o teorema do impulso estava certo o tempo todo. O que estava errado era o modelo de luz. Uma física correta, aplicada com cuidado, fez uma previsão que dava para medir, e a natureza decidiu.

## CODA — A LUZ TAMBÉM TEM MOMENTO

### C-1 — tela: duas raias em painéis: SUPERFÍCIE PRETA · ABSORVE e ESPELHO · REFLETE; fonte, feixe amarelo com brilho, fótons como pacotes de onda com seta p⃗ magenta; a preta engole o fóton com um flash laranja, o espelho devolve; placas penduradas, a do espelho inclina o dobro; F⃗ e 2F⃗; CONTA: p = E/c → Δp/Δt = F
[curious] Só que a história tem uma virada. O modelo do Newton errou a velocidade da luz na água, mas, em outro ponto, ele estava mais certo do que parecia: a luz realmente carrega momento. A energia que ela transporta, dividida pela velocidade da luz, é o momento dela. Quando a luz bate numa superfície, ela entrega momento a cada segundo, e momento por segundo é força.

### C-2 — tela: PALCO (3D): uma vela solar refletora no espaço, abrindo devagar, com fótons em riscos amarelos (LUZ #FFD25A) batendo e voltando e uma seta de força pequena crescendo; na CONTA: LUZ DO SOL: 4,5 μPa (ABSORVIDA) · 9,1 μPa (REFLETIDA); vela solar de 100 m² refletora: ≈ 0,9 mN; um laser de 1 W: 3,3 nN
[thoughtful] É uma força pequenininha. A luz do Sol, que chega à Terra com mil, trezentos e sessenta e um watts por metro quadrado, empurra com uns quatro vírgula cinco micropascais se for absorvida, e o dobro, uns nove micropascais, se for refletida. Uma vela solar refletora de cem metros quadrados recebe uns nove décimos de milinewton. Pouco, mas no vácuo, sem atrito, empurrando o tempo todo, é força suficiente para navegar. E um laser de um watt empurra com uns três vírgula três nanonewtons.

### C-3 — tela: o PALCO continua (a vela se afastando, o tanque apagado ao lado); O MODELO DO NEWTON CAIU. A CONSERVAÇÃO DO MOMENTO FICOU.
[emphatic] O modelo do Newton caiu. A conservação do momento ficou. Ela vale para a luz, vale na física quântica, onde o momento deixa de ser massa vezes velocidade, e vale em tudo o que a gente sabe medir.

## SÍNTESE

### S1 — tela: limpa; o cavalo e a pedra, com a fronteira tracejada, a tensão em cinza e as duas forças externas em azul-claro
[calm] Então, voltando à pergunta do começo. A corda puxa o cavalo para trás, mas ela é uma força interna, e força interna não muda o momento do sistema. Quem acelera o cavalo e a pedra é o chão, uma força externa. A pergunta inicial está respondida.

### S2 — tela: cada ideia entra com seu desenho pequeno no PALCO (as esferas com molas; os blocos e a Terra; o cavalo); as ideias-chave: dP⃗/dt = F⃗^ext (componente por componente) e MOMENTO SE DIVIDE IGUAL; ENERGIA, NÃO; NÃO CONSERVA? AUMENTE O SISTEMA
Resumindo em três ideias. A variação do momento total só depende da força externa resultante, componente por componente. Quando um sistema se separa, o momento se divide igualmente e a energia vai principalmente para o mais leve. E, quando a conta do momento não fecha, aumenta o sistema até a conta fechar.

## ENCERRAMENTO

### EN1 — tela: FadeOut geral; logo com anéis; INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS
Se esses exercícios ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos.

### EN2 — tela: granada explodindo no ar, fragmentos para todos os lados, um ponto seguindo a parábola; SE A GRANADA EXPLODE NO AR, O QUE CONTINUA NA PARÁBOLA? → PRÓXIMO VÍDEO: CENTRO DE MASSA (ciano)
[curious] E fica a pergunta para o próximo: se uma granada explode no meio do voo, os pedaços voam para todo lado... mas alguma coisa continua exatamente na mesma parábola. O quê? No próximo vídeo: centro de massa. Até a próxima!

---

## Números de conferência (briefing v1; g = 9,8 m/s²)

| Bloco | Valor falado | Exato |
|---|---|---|
| T8 | 2.352 N; 2.800 N; 448 N; 0,32 m/s²; 2.608 N; 192 N; 588 N | 2352; 2800; 448; 0,32; 2608; 192; 588 |
| T9 | 14 m/s; 2,3×10⁻²⁴ m/s; ±2 kg·m/s; 1,96 N; 3,92 N; 0,51 s; −1,0; 1,02 s | 14,0; 2,35e-24; 2; 1,96; 3,92; 0,510; −1,0; 1,020 |
| T10 | 2 J e 1 J; fração 2/3; 50% (iguais) | 2; 1; 66,7% |
| E6 | 8,5 cm/s; 15 cm/s; 30 J → 0,25 J e ≈ 20 J | 0,0850; 0,1543; 30; 0,255; 20,03 |
| E7 | 5,6 cm/s; 3 cm/s; ≈ 1.956 J e ≈ 0,11 J; ≈ 17.262; 99,994% | 0,0559; 0,0313; 1955,6 e 0,113; 17.262; 99,9942% |
| E8 | 599,15 m/s; 4,31; 5,18; 0,87 kg·m/s | 599,15; 4,314; 5,18; 0,866 |
| Coda | 4,5 e 9,1 μPa; 0,9 mN; 3,3 nN | 4,54; 9,08; 0,908; 3,34 |

**Pontos a confirmar antes da voz**
1. E9-6: Foucault, 1850, luz mais lenta na água: fato bem estabelecido, conferir fonte se for para a descrição.
2. C-1: a frase "o Newton estava mais certo do que parecia" tem um sentido brando (a luz carrega momento); se quiser evitar atribuir ao Newton, trocar por "o modelo errou a velocidade, mas a luz realmente carrega momento".
3. T7-7: a observação sobre cargas em movimento e campo é qualitativa; não há esquema com forças.
4. T9-3: o caso das massas iguais/diferentes parte do Moysés §8.3 (só na descrição do YouTube); os números e o gráfico P(t) são construção nossa.
