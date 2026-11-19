# yt_0032 · CÁLCULO III · EP. 07 · Propriedades da integral dupla
## Narração v3: v2 enxuta (~18 min)

2026-11-12 · thread "Planejar propriedades da integral dupla" · substitui o Anexo A da proposta v1 (`pautas/calculo3_32t3_propriedades_integral_dupla_proposta_v1.md`). A estrutura, as figuras D1–D19 e os números da proposta continuam valendo, com as mudanças de tela do §2. Todos os números estão conferidos em `pautas/verificacao/verifica_calc3_32t3_sympy.py` (19 checagens, todas `True`).

**Tamanho:** 3.160 palavras ≈ **17:46** (0,15 s + palavras/3 + 0,35 s por âncora). A v2 tinha 3.901 palavras ≈ 21:53; o Kaio escolheu enxugar para ~18 min (2026-11-12). **Esta é a narração vigente.** O corte tirou só repetições e transições ("agora olha", "parece óbvio", frases que repetiam a anterior): nenhum exemplo, número, leitura de símbolo, hipótese ou passo da prova saiu, e as seis correções do filtro (§1) continuam. A v2 (`yt_0032_narracao_v2_refino_gpt_filtrado.md`) fica como registro.

### Tempo por âncora

| Âncora | Trecho | Palavras | Voz (s) | Início estimado |
|---|---|---:|---:|---:|
| H1 | a balança e as três perguntas | 166 | 55.8 | 0:00 |
| H2 | o que vamos descobrir | 81 | 27.5 | 0:55 |
| A1 | apresentação | 75 | 25.5 | 1:23 |
| B1-1 | as regras do jogo | 96 | 32.5 | 1:48 |
| B1-2 | somar funções | 130 | 43.8 | 2:21 |
| B1-3 | uma conta de graça | 98 | 33.2 | 3:05 |
| B1-4 | multiplicar por uma constante | 148 | 49.8 | 3:38 |
| B2-1 | uma função acima da outra | 130 | 43.8 | 4:28 |
| B2-2 | estimar sem resolver | 122 | 41.2 | 5:12 |
| B3-1 | uma linha pode ter massa? | 130 | 43.8 | 5:53 |
| B3-2 | um muro de cem | 119 | 40.2 | 6:37 |
| B3-3 | mas uma solda real pesa | 125 | 42.2 | 7:17 |
| B4-1 | cem, dois ou três? | 117 | 39.5 | 7:59 |
| B4-2 | o motivo e a função com furo | 121 | 40.8 | 8:38 |
| B5-1 | a propriedade da balança | 137 | 46.2 | 9:19 |
| B5-2 | e se houver sobreposição? | 116 | 39.2 | 10:05 |
| B5-3 | por que dividir ajuda? | 68 | 23.2 | 10:45 |
| B6-1 | a terraplanagem | 146 | 49.2 | 11:08 |
| B6-2 | o teorema aparece | 134 | 45.2 | 11:57 |
| B6-3 | por que isso é verdade? | 151 | 50.8 | 12:42 |
| B6-4 | quando a média não aparece | 176 | 59.2 | 13:33 |
| B6-5 | onde encontramos essa média? | 80 | 27.2 | 14:32 |
| B7-1 | a função com um furo | 111 | 37.5 | 14:59 |
| B7-2 | pi sobre dois, sem fazer conta | 121 | 40.8 | 15:37 |
| S1 | voltando à balança | 115 | 38.8 | 16:17 |
| S2 | o próximo vídeo e CTA | 147 | 49.5 | 16:56 |
| **Total** | | **3160** | **17:46** | |

## 1. Filtro do refino do GPT

**Entrou (correto e melhora):**
- **A soma da balança.** O GPT tem razão: 2,47 + 4,58 dá 7,05. O total certo vem de 2,4721 + 4,5836 = 7,0557 ≈ 7,06. A fala fica como o GPT escreveu ("usando os valores sem arredondar"), e a tela muda (§2, item 1).
- **Valor médio: as hipóteses são suficientes, não necessárias.** Correto. O "Sem continuidade, ou sem caminho, o teorema não vale" da v1 dava a entender que a média nunca aparece sem elas. O B6-4 agora diz que "o teorema já não assegura", e o cartão final troca `MÉDIA: SÓ SEM SALTO` por `MÉDIA: CONTINUIDADE + CAMINHO`.
- **Cotas, não massas, no muro de 100.** O 9,3 → 0,6 kg é uma cota superior da contribuição possível, não a massa da solda. Fala e tela dizem isso.
- **Cada propriedade responde a uma pergunta da anterior**, com as transições que o GPT escreveu (B1-1 → B1-2, B2-1, B3-1, B4-1, B6-2).
- O caso α = 0 com "e não for vazia" (B6-3); "independentemente dos pontos escolhidos" na definição de integrável (B1-1); o k negativo e o k = ½ (B1-4); "desde que a região tenha área positiva" para falar de média (B6-2).

**Corrigi no texto do GPT (6 pontos):**
1. **Numeração das propriedades (B2-1).** O sinal e a comparação são as propriedades **II e III** do livro; o texto do GPT dizia "uma segunda propriedade" para a comparação, e a minha v1 dizia "terceira" e "quarta", o que também estava errado e batia de frente com a "quarta" do B3-1. Agora: "propriedade dois, a do sinal" e "propriedade três".
2. **"Infinitamente fino" (B3-1)** virou "tão fino quanto se queira". Em nenhuma grade o muro tem largura zero: a largura vai a zero no limite.
3. **"Hipóteses necessárias" (B6-5)** virou "as hipóteses do teorema". "Necessárias" contradizia a correção que o próprio GPT pediu no B6-4.
4. **Um exemplo concreto para "suficiente, não necessária" (B6-4).** Entrou uma frase: pela propriedade cinco, dá para pôr 1,76 exatamente na solda sem mudar a massa, e aí a média aparece num ponto mesmo com o salto. É a prova, dentro do próprio vídeo, de que a média pode aparecer sem as hipóteses.
5. **"Propriedade seis" dito em voz alta (B5-1)**, como as outras seis.
6. **"Formato de ele" (B5-3)** virou "formato de éle", para a voz não ler o pronome.

**Não mudou:** os exemplos, as seis tags, as leituras dos símbolos, a terraplanagem e a prova completa do B6 como clímax, o gancho de Fubini.

## 2. Mudanças de tela que a v2 pede

1. **H1 e B5-1:** a soma da balança fica `2,472 kg + 4,584 kg ≈ 7,06 kg` (três casas, com o ≈). Nada de `2,47 + 4,58 = 7,06` na tela.
2. **B3-2:** a tabela ganha o título `COTA SUPERIOR` e, ao lado do muro, `COTA, NÃO MASSA`.
3. **B6-4:** depois das duas miniaturas, a solda da chapa de dois metais acende em `ρ = 1,76` e um ponto laranja pousa nela com `MÉDIA ATINGIDA` (beat novo, um movimento só).
4. **S1:** o terceiro ✓ da balança vira `MÉDIA: CONTINUIDADE + CAMINHO`.
5. **H1:** entra `MÉDIA ≈ 1,76 kg/m²` junto da terceira pergunta, porque a fala agora diz o número.

## 3. Narração v3 por âncora

Tags permitidas: [curious], [thoughtful], [surprised], [happy], [excited], [serious]. Uma por parágrafo (o S2 tem duas, como nos EP. 05 e 06). Sem [slowly] e sem [pause]. Letras escritas como a voz deve ler: éfe, gê, cá, xis, ípsilon, érre, ésse, éle, eme.

### H1 · a balança e as três perguntas
**Tela:** a chapa inteira com `7,06 kg`; ela se parte na solda; os pedaços nos pratos; `2,472 kg + 4,584 kg ≈ 7,06 kg`; a solda acende nos dois pedaços (`CONTOU DUAS VEZES?`); `E SE ρ = 100 NA SOLDA?`; `MÉDIA ≈ 1,76 kg/m²` + `ALGUM PONTO TEM A MÉDIA?`.
> [curious] Lembra da chapa de dois metais? Embaixo da solda, um quilo por metro quadrado; em cima, três. No episódio passado, descobrimos que a massa total existe e vale aproximadamente sete vírgula zero seis quilos. Agora imagina cortar a chapa exatamente na linha da solda e colocar os dois pedaços numa balança. O pedaço leve tem aproximadamente dois vírgula quarenta e sete quilos. O pesado, quatro vírgula cinquenta e oito. Usando os valores sem arredondar, a soma dá os mesmos sete vírgula zero seis. Até aqui, tudo bem. Mas olha a linha branca entre os dois metais: ela é a fronteira dos dois pedaços. Será que a gente contou a solda duas vezes? E quanto ela pesa? Agora piora: e se a densidade exatamente sobre a solda fosse de cem quilos por metro quadrado? A massa mudaria? E uma última pergunta: a densidade média da chapa é aproximadamente um vírgula setenta e seis quilo por metro quadrado. Existe algum ponto onde a densidade tem exatamente esse valor?

### H2 · o que vamos descobrir
**Tela:** a balança encolhe para o canto; `O QUE VALE NA SOMA` / `VALE NA INTEGRAL`; embaixo, `CONTEÚDO NULO NÃO PESA`.
> [serious] Parecem três perguntas diferentes, mas as propriedades da integral dupla respondem todas. E a ideia principal é simples: a integral nasce de uma soma. Então as regras que funcionam nas somas continuam funcionando quando passamos ao limite: somar, multiplicar, comparar e dividir regiões. E tem um ingrediente a mais, que veio do episódio passado: um conjunto de conteúdo nulo pode estar no desenho sem contribuir para a integral de uma função limitada. É isso que vai resolver o mistério da solda.

### A1 · apresentação
**Tela:** logo; `INTEGRAIS DUPLAS`; `NESTE VÍDEO: SOMAR · COMPARAR · DIVIDIR · MÉDIA`.
> [happy] Fala, pessoal! Bem-vindos ao Parallax Lab! Esse é o sétimo episódio da nossa série de Cálculo três e o terceiro do módulo de integrais duplas. A gente já sabe de onde a integral vem e como garantir que ela existe. Agora vamos aprender a trabalhar com ela: sete propriedades para somar, comparar, estimar e dividir integrais sem refazer a conta. E, no final, o teorema do valor médio. Cada propriedade vai sair de um desenho.

### B1-1 · as regras do jogo
**Tela:** D1; `f, g INTEGRÁVEIS EM B` · `k CONSTANTE`; `∬_B f(x, y) dx dy` a caneta, sublinhado em ∬, B e dx dy no gatilho.
> [thoughtful] Primeiro, as regras do jogo. Temos duas funções, éfe e gê, integráveis numa mesma região B, e uma constante cá, que é simplesmente um número fixo. Lembrando: uma função é integrável quando suas somas de Riemann convergem para um único valor à medida que a partição fica fina, independentemente dos pontos escolhidos. Esse valor é escrito com o símbolo de integral dupla. Lê-se: integral dupla sobre B de éfe de xis, ípsilon, dê xis, dê ípsilon. A letra B indica a região onde estamos somando, e o dê xis, dê ípsilon representa o elemento de área.

### B1-2 · somar funções
**Tela:** D2 em Three.js (rampa x² âmbar + rampa y² magenta → prédio ciano); na coluna, `Σ (f + g) ΔA = Σ f ΔA + Σ g ΔA` e depois `∬(f + g) = ∬f + ∬g`.
> [curious] Pega a nossa chapa quadrada de dois metros de lado e duas funções: xis ao quadrado, uma rampa que cresce na direção horizontal, e ípsilon ao quadrado, uma rampa que cresce na direção vertical. Mesma grade para as duas, mesmos pontos em cada célula. Primeiro, levantamos as caixinhas da rampa horizontal. Depois, colocamos em cima delas as caixinhas da outra rampa. Em cada célula, a altura total é a soma das duas alturas. Então a soma de Riemann de éfe mais gê é exatamente a soma de Riemann de éfe mais a de gê. Isso vale antes mesmo de refinar a grade! E, passando ao limite, a igualdade continua valendo. Portanto, a soma de duas funções integráveis também é integrável, e a integral da soma é a soma das integrais.

### B1-3 · uma conta de graça
**Tela:** D3: espelho na diagonal; `32/3` voa da régua da massa e vira `16/3 + 16/3`.
> [excited] E olha o que isso dá de graça! Quando construímos a integral dupla, a chapa com densidade xis ao quadrado mais ípsilon ao quadrado deu trinta e dois terços de quilo. Agora espelha a rampa de xis ao quadrado pela diagonal da chapa: ela se transforma exatamente na rampa de ípsilon ao quadrado. A região continua a mesma, e as caixinhas correspondentes têm os mesmos volumes. Então as duas integrais são iguais. Como somam trinta e dois terços, cada uma vale dezesseis terços. Nenhuma soma nova: só a propriedade que acabamos de ver e a simetria do desenho.

### B1-4 · multiplicar por uma constante
**Tela:** D4: caixas esticam ×2; `∬ k f = k ∬ f`; as duas camadas da chapa de dois metais; `1 · 4 = 4` e `2 · 1,53 ≈ 3,06`; `4 + 3,06 ≈ 7,06`.
> [thoughtful] A segunda parte da primeira propriedade é a constante. Multiplicando a função por cá, todas as caixinhas têm a altura multiplicada por cá. Se cá vale dois, as alturas dobram; se vale meio, caem pela metade; se é negativo, a contribuição troca de sinal. Em todos os casos, cada parcela da soma de Riemann é multiplicada por cá, e a constante sai da soma e, depois, da integral. Lê-se: a integral de cá vezes éfe é cá vezes a integral de éfe. Agora junta com a regra da soma. A chapa de dois metais pode ser vista como uma camada de um quilo por metro quadrado sobre os quatro metros quadrados, mais um reforço de dois quilos por metro quadrado só na região do metal pesado. A camada dá quatro quilos; o reforço, aproximadamente três vírgula zero seis. Total: sete vírgula zero seis quilos, agora montado em camadas.

### B2-1 · uma função acima da outra
**Tela:** D5 (caixas no chão; somas sempre à direita do zero); D6 (prédio de f dentro do de g); `f ≥ 0 em B ⇒ ∬f ≥ 0`; `f ≤ g em B ⇒ ∬f ≤ ∬g`; `g − f ≥ 0` nasce da folga.
> [curious] Agora uma propriedade que parece óbvia no desenho, mas é muito útil nas contas. Se uma função é maior ou igual a zero em toda a região, cada parcela da soma de Riemann também é, e a integral não pode ser negativa. Essa é a propriedade dois, a do sinal. Aquela seta na fórmula se lê "implica". Daí vem a propriedade três: se éfe é menor ou igual a gê em todos os pontos, a integral de éfe é menor ou igual à de gê. Por quê? A diferença gê menos éfe nunca é negativa, então sua integral também não é. E, pela propriedade da soma, essa integral é a integral de gê menos a integral de éfe. Reorganizando, aparece a comparação. Percebe? Uma propriedade ajuda a demonstrar a seguinte.

### B2-2 · estimar sem resolver
**Tela:** D7: as lajes de 1 e 3; régua da massa com a faixa [4, 12] e o 7,06 dentro; `m · α ≤ ∬ f ≤ M · α`; `13 kg? ERRO`.
> [thoughtful] E a comparação permite descobrir se uma resposta é possível antes de calcular a integral. Na chapa de dois metais, a densidade fica entre um e três quilos por metro quadrado. Compara com duas chapas uniformes: com a menor densidade, a massa seria quatro quilos; com a maior, doze. Então a massa verdadeira está entre quatro e doze, e o sete vírgula zero seis passa no teste. Em geral, se uma função fica entre um valor eme minúsculo e um eme maiúsculo, sua integral fica entre esses valores multiplicados pela área da região, que chamamos de alfa. Parece simples, mas é extremamente útil: se um programa calculasse treze quilos para essa chapa, já saberíamos que tem erro, sem resolver a integral inteira.

### B3-1 · uma linha pode ter massa?
**Tela:** D8: só a solda com a cobertura menta; o muro coral (Three.js); `B COM CONTEÚDO NULO ⇒ ∬_B f = 0`; `∬ ≤ M · ÁREA DA COBERTURA`.
> [serious] Agora, a primeira pergunta da abertura: quanto pesa a solda? Começa pela solda matemática: uma curva, sem espessura. No episódio passado, vimos que essa linha tem conteúdo nulo: dá para cobri-la com retângulos de área total tão pequena quanto quisermos. Agora põe sobre ela uma densidade limitada: existe um número eme maior que o módulo de todos os seus valores. A contribuição das células que cobrem a solda fica limitada por eme vezes a área da cobertura. A altura pode ser grande, mas a área vai ficando cada vez menor, e a contribuição tende a zero. Essa é a quarta propriedade: a integral de uma função limitada sobre um conjunto de conteúdo nulo é zero. No desenho, um muro que pode ser alto, mas fica tão fino quanto se queira.

### B3-2 · um muro de cem
**Tela:** D9: o muro de altura 100 afinando; tabela `COTA SUPERIOR` com `n · ÁREA · COTA`: 64 · 0,093 · 9,3 kg → 1024 · 0,006 · 0,6 kg; ao lado do muro, `COTA, NÃO MASSA`.
> [surprised] Vamos exagerar: densidade de cem quilos por metro quadrado exatamente sobre a solda. O muro coral fica altíssimo. Com sessenta e quatro divisões por lado, a cota superior desse muro chega a nove vírgula três quilos. Atenção: é uma cota grosseira, não a massa real da linha. Dobra a resolução: a cota cai para quatro vírgula seis. Depois, dois vírgula três. Depois, um vírgula dois. E, continuando, seis décimos de quilo. A altura continua cem; o que desaparece é a área da cobertura. Repetindo, a contribuição fica menor que qualquer tolerância positiva. Então a solda matemática não acrescenta massa à integral dupla, por maior que seja a densidade, desde que limitada. E contar zero duas vezes não muda nada.

### B3-3 · mas uma solda real pesa
**Tela:** D10: zoom na solda; o cordão de 1 cm com `≈ 135 g`; afina para 1 mm, `≈ 13 g`; vira a curva branca; `kg/m` quando a voz fala de densidade linear.
> [thoughtful] Só que aqui precisamos separar o modelo da realidade. Uma solda de verdade é um cordão de metal: ocupa espaço e acrescenta massa à peça. Vamos representá-lo como uma faixa de largura constante, com seis quilos por metro quadrado. A linha da solda tem uns dois vírgula vinte e cinco metros. Com um centímetro de largura, a faixa teria uns cento e trinta e cinco gramas. Com um milímetro, uns treze gramas. E, conforme a largura tende a zero, a massa desse modelo também tende a zero. E se quisermos uma massa realmente concentrada numa linha? Aí usamos uma densidade linear, em quilos por metro, que leva às integrais de linha. A integral dupla com densidade superficial limitada não representa uma massa concentrada dessa maneira.

### B4-1 · cem, dois ou três?
**Tela:** D11: a solda troca de cor e rótulo (`ρ = 1`, `3`, `2`, `100`), contador parado em `≈ 7,06 kg`; `{(x, y) ∈ B | f ≠ g}` a caneta, sublinhado no "|".
> [curious] Agora, uma consequência surpreendente. Qual densidade devemos colocar exatamente sobre a solda? A do metal leve, um? A do pesado, três? A média, dois? Ou aquele exagero de cem? Para a massa total, tanto faz. Essa é a quinta propriedade: se duas funções integráveis só diferem num conjunto de conteúdo nulo, suas integrais são iguais. Na fórmula, aparece o conjunto dos pontos xis, ípsilon de B tais que éfe é diferente de gê. O tracinho em pé, dentro das chaves, se lê "tais que". Se esse conjunto tem conteúdo nulo, a integral de éfe é igual à de gê. Então podemos mudar a densidade sobre a solda, e o contador continua marcando sete vírgula zero seis quilos.

### B4-2 · o motivo e a função com furo
**Tela:** D12: caixas de f − g (zero fora, muro fino na solda); um furo tracejado preenchido por valores diferentes, a integral parada.
> [thoughtful] E essa propriedade nasce das anteriores. Se duas funções são iguais fora da solda, a diferença entre elas vale zero fora dessa linha. Então, nas somas da diferença, só contam as células que encostam na solda, e a área delas pode ser tornada arbitrariamente pequena. A integral da diferença é zero, e, pela propriedade da soma, as integrais das duas funções são iguais. Isso também resolve uma situação comum: uma função que não está definida em alguns pontos, como um furo na origem ou uma borda onde a fórmula falha. Se esses pontos formam um conjunto de conteúdo nulo, podemos preenchê-los com valores limitados e trabalhar com uma extensão integrável. O valor da integral não depende de como preenchemos o furo.

### B5-1 · a propriedade da balança
**Tela:** D13: os dois pedaços se afastam e voltam; `B ∩ B₁ COM CONTEÚDO NULO ⇒ ∬_{B∪B₁} f = ∬_B f + ∬_{B₁} f`; `2,472 + 4,584 ≈ 7,06`.
> [serious] Agora voltamos à balança, com a propriedade seis. A chapa foi dividida em duas partes: o metal leve, que vamos chamar de B, e o metal pesado, B um. Se a função é integrável nelas e a parte comum tem conteúdo nulo, a integral sobre a união é a soma das duas integrais. O U normal é a união: os dois conjuntos juntos. O U de cabeça para baixo é a interseção: a parte em comum. Lê-se: a integral sobre B união B um é igual à integral sobre B mais a integral sobre B um. A solda está na fronteira dos dois pedaços, então aparece nas duas regiões. Mas ela tem conteúdo nulo, e sua contribuição é zero. Por isso a balança não precisa de correção: sem arredondar, o total é sete vírgula zero seis quilos.

### B5-2 · e se houver sobreposição?
**Tela:** a solda acende duas vezes; `∬_B + ∬_{B₁} − ∬_{B∩B₁}`; o último termo vira `0` e sai; D14: faixa de 0,2 m hachurada duas vezes, `4 + 0,4 = 4,4 m²`.
> [thoughtful] E se a parte comum tiver área positiva? Aí somar as integrais conta essa parte duas vezes. A conta correta é a integral sobre B, mais a integral sobre B um, menos a integral sobre a interseção. É como contar os alunos de duas turmas: quem está nas duas não pode entrar duas vezes no total. Na chapa: faz os dois pedaços se sobreporem numa faixa de vinte centímetros de altura. A chapa tem quatro metros quadrados, mas a soma das áreas dos dois pedaços dá quatro vírgula quatro. Os quatro décimos extras são a faixa contada duas vezes. Quando a interseção tem conteúdo nulo, esse desconto vale zero e desaparece. Com área positiva, precisamos descontá-la.

### B5-3 · por que dividir ajuda?
**Tela:** quatro miniaturas: peças montadas que se tocam numa face; região em L partida em dois retângulos; a chapa partida na solda; "várias integrais simples".
> [curious] E dividir é uma das estratégias mais úteis na prática. A massa de uma peça montada sai das massas de cada componente, sem sobreposições. Uma região em formato de éle vira dois retângulos. Uma chapa de materiais diferentes se divide justamente onde a densidade muda. Em vez de uma integral complicada, várias integrais simples. Quando começarmos a trabalhar com integrais iteradas, essa estratégia vai aparecer o tempo todo.

### B6-1 · a terraplanagem
**Tela:** D16 em Three.js: a superfície x² + y² vira morro; terraplanagem até a altura 8/3; `ACIMA: 8π/9` · `ABAIXO: 8π/9`; o arco de raio 1,63 acende na chapa.
> [curious] Agora, a terceira pergunta: a média. Volta à chapa com densidade xis ao quadrado mais ípsilon ao quadrado. A massa é trinta e dois terços de quilo, e a área é quatro metros quadrados. Dividindo, a densidade média é oito terços, aproximadamente dois vírgula sessenta e sete quilos por metro quadrado. Agora transforma a densidade num relevo, como quando construímos a integral: o gráfico vira um morro. A média é a altura que dá o mesmo volume se nivelarmos tudo. Olha a terraplanagem: o material acima dessa altura vai preencher o espaço que falta abaixo. O volume retirado e o preenchido são iguais: oito pi sobre nove, aproximadamente dois vírgula setenta e nove. E existe algum ponto da chapa que já tem exatamente a altura média? Existe! Todos os pontos deste arco, a um vírgula sessenta e três da origem, têm densidade igual a oito terços.

### B6-2 · o teorema aparece
**Tela:** D15 (ícones fechado/limitado); o enunciado a caneta: `B COMPACTO · FRONTEIRA DE CONTEÚDO NULO`, `CAMINHO DENTRO DE B · f CONTÍNUA`, `⇒ ∃ (r, s) ∈ B : ∬_B f = α f(r, s)`; `α = ÁREA DE B`.
> [serious] Mas isso acontece com qualquer função? Aqui entra a sétima propriedade: o teorema do valor médio para integrais duplas. As hipóteses: a região B é compacta, ou seja, fechada e limitada. Fechada quer dizer que contém seus pontos de fronteira; limitada, que cabe dentro de algum retângulo. A fronteira tem conteúdo nulo. Dois pontos quaisquer da região podem ser ligados por um caminho contínuo que não sai dela. E a função é contínua. Com essas condições, existe pelo menos um ponto érre, ésse da região onde a função vale exatamente a média. Na fórmula, a integral sobre B de éfe é igual a alfa vezes éfe de érre, ésse, sendo alfa a área de B. Em outras palavras: desde que a região tenha área positiva, a função assume em algum lugar o valor médio.

### B6-3 · por que isso é verdade?
**Tela:** D17: mínimo em (0, 0), máximo em (2, 2); `m · α ≤ ∬ f ≤ M · α` volta do B2-2 e se divide por α; o caminho laranja; o gráfico ao longo do caminho cruzando 8/3.
> [thoughtful] E a demonstração é muito bonita, porque junta duas ideias conhecidas. Como B é compacto e a função é contínua, ela atinge um mínimo e um máximo na região. Na nossa chapa, o mínimo é zero, na origem, e o máximo é oito, no canto oposto. Pela comparação, a integral fica entre o mínimo vezes a área e o máximo vezes a área. Dividindo pela área, a média está entre o mínimo e o máximo. Agora escolhe um caminho dentro da região ligando um ponto de mínimo a um ponto de máximo. Ao longo dele, a função muda continuamente. E, pelo teorema do valor intermediário, uma função contínua não passa de um valor abaixo da média para outro acima sem assumir a própria média. Esse é o ponto érre, ésse. E, se a região tiver área zero e não for vazia, a integral é zero, e qualquer ponto satisfaz a igualdade.

### B6-4 · quando a média não aparece
**Tela:** D18: (a) degraus 1 e 3 com a linha da média 1,76 passando entre eles; (b) dois quadrados separados, 1 e 3, média 2; (c) beat novo: a solda acende em `ρ = 1,76`, ponto laranja nela, `MÉDIA ATINGIDA`.
> [curious] Agora a parte interessante: o que acontece sem alguma dessas hipóteses? Volta à chapa de dois metais. A densidade média é aproximadamente um vírgula setenta e seis, mas, no modelo original, a função só assume dois valores: um e três. Nenhum ponto tem densidade um vírgula setenta e seis: a função salta de um valor para o outro, passando por cima da média. Outro exemplo: dois quadrados separados, um com densidade um e o outro com densidade três. A função é contínua na região formada pelos dois, mas não existe caminho dentro dela ligando os quadrados. A média é dois, e a função não vale dois em nenhum ponto. Só que repara no outro lado da moeda: pela quinta propriedade, dá para colocar um vírgula setenta e seis exatamente sobre a solda sem mudar a massa. Aí a média aparece num ponto, mesmo com o salto. Então continuidade e caminho garantem o resultado, mas não são a única forma de ele acontecer. Sem essas hipóteses, a média pode até ser atingida, mas o teorema não assegura.

### B6-5 · onde encontramos essa média?
**Tela:** quatro miniaturas: placa aquecida, bacia de rio com chuva, terraplanagem, imagem; `MÉDIA = ∬ f / α`.
> [happy] E essa média aparece em muito lugar. A temperatura média de uma placa aquecida. A altura média de chuva numa bacia hidrográfica. A altura de uma terraplanagem, que equilibra corte e aterro. O brilho médio de uma região numa imagem digital. A integral dupla dá a média mesmo quando a grandeza varia de ponto para ponto. E o teorema acrescenta: se a função é contínua e a região satisfaz as hipóteses do teorema, algum lugar assume exatamente esse valor médio.

### B7-1 · a função com um furo
**Tela:** D19: mapa de x²/(x² + y²) no disco, origem tracejada; `1` no eixo x, `0` no eixo y; o furo preenchido.
> [curious] Para fechar, um exemplo que junta várias propriedades. No disco de raio um, considera a função xis ao quadrado dividido por xis ao quadrado mais ípsilon ao quadrado. Na origem, a fórmula vira zero dividido por zero: a função não está definida ali. E o limite na origem nem existe: pelo eixo horizontal, o valor é um; pelo vertical, zero. Mas a origem é um único ponto, e um ponto tem conteúdo nulo. Fora dele, a função é contínua e fica entre zero e um. Então podemos preencher o furo com qualquer valor finito: a função fica integrável, e a integral não depende do valor escolhido. É a quinta propriedade funcionando.

### B7-2 · pi sobre dois, sem fazer conta
**Tela:** os dois mapas somados viram o disco todo em `1`; `= ÁREA = π`; espelho na diagonal; `π/2 + π/2`.
> [excited] E agora o valor, sem calcular nenhuma primitiva. Cria uma segunda função, parecida, mas com ípsilon ao quadrado no numerador. Somando as duas, fora da origem, o numerador fica igual ao denominador. Resultado: um! Então a soma das duas funções vale um em todo o disco, exceto talvez naquele ponto que não altera a integral. Pela propriedade da soma, as duas integrais juntas valem a integral de um sobre o disco, que é a área: pi. Agora a simetria: espelhando o disco pela diagonal, a primeira função vira a segunda, e a região continua a mesma. Então as integrais são iguais. Dois números iguais que somam pi: cada um vale pi sobre dois. Soma, conteúdo nulo e simetria. Nenhuma integração complicada.

### S1 · voltando à balança
**Tela:** a balança volta com os três ✓: `SOLDA: 0 kg` · `DENSIDADE NA SOLDA: TANTO FAZ` · `MÉDIA: CONTINUIDADE + CAMINHO`; embaixo, a lista curta das sete.
> [thoughtful] Então olha o que aprendemos. A integral dupla nasce de uma soma, por isso podemos somar funções, multiplicar por constantes e comparar resultados. Um conjunto de conteúdo nulo não contribui para a integral de uma função limitada, e mudar a função só nele não altera o resultado. Dividir a região funciona quando a sobreposição não traz contribuição extra. E o teorema do valor médio garante que uma função contínua, numa região adequada, atinge sua média em algum ponto. As três perguntas da abertura: a solda matemática não acrescenta massa; o valor limitado que pomos nela não altera o total; e, para garantir um ponto com a média, olhamos a continuidade e a geometria da região.

### S2 · o próximo vídeo e CTA
**Tela:** cartão `NO PRÓXIMO VÍDEO: TEOREMA DE FUBINI`; a chapa de dois metais fatiada em tiras verticais; `COMO CALCULAR O 7,06 EXATO?`; depois o CTA padrão.
> [curious] Mas repara numa coisa. Até aqui, as integrais apareceram como limites de somas de Riemann, com grades cada vez mais finas, propriedades e simetrias. Falta uma pergunta bem prática: como calcular uma integral dupla diretamente, com as ferramentas do Cálculo um? Por exemplo: dá para achar a massa exata da chapa de dois metais numa conta no papel, sem refinar milhares de caixinhas? Dá. A ideia é fatiar a região: primeiro, somamos dentro de cada fatia; depois, somamos as fatias. Duas integrais simples trabalhando juntas. É isso que vamos ver no próximo episódio, com o teorema de Fubini. [happy] Se essa aula te ajudou, deixa o like e se inscreve no Parallax Lab para acompanhar a série. E conta nos comentários: qual propriedade te surpreendeu mais? A solda sem massa, mudar a função num conjunto de conteúdo nulo ou o ponto com o valor médio? Até a próxima!
