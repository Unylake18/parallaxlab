# Narração integral — As 3 simetrias que resolvem a Lei de Gauss

Versão editorial: 2026-10-06. Português do Brasil. Formato: ensaio narrado sobre animações, com uma pergunta central e três famílias sucessivas. Não gerar voz nesta rodada.

As janelas são estimativas de montagem, não timestamps de áudio. Trechos entre colchetes orientam a futura produção e não são falados. Equações estão no storyboard; a voz desenvolve o raciocínio, sem soletrar cada símbolo. O único roteiro a narrar começa em N01; os ganchos alternativos não entram na contagem desse roteiro.

## Três opções de gancho

**G1 — Mudança de geometria, selecionado em N01.** Você tem uma linha de carga, uma esfera e duas placas. Os campos parecem pedir três receitas diferentes: um cai com a distância, outro cai ainda mais rápido, e outro nem diminui. Mas todos saem da mesma lei. O que muda: a fórmula, a superfície escolhida ou a carga que ficou dentro dela?

**G2 — Correção de expectativa.** Se você tentar decorar uma fórmula para cada problema de Gauss, vai precisar lembrar de cascas, maciços, placas e capacitores. Mas experimente guardar só três superfícies. Como a mesma superfície pode resolver fontes tão diferentes? A resposta está na simetria e no que ela permite dizer sobre o campo.

**G3 — Escolha concreta.** Você recebeu um cilindro carregado e precisa encontrar o campo dentro e fora dele. Antes de fazer uma conta, precisa decidir duas coisas: onde o campo pode apontar e quanto da carga a sua superfície envolve. Se essas escolhas estiverem certas, quase toda a integral já está resolvida. Vamos construir esse método.

## Roteiro selecionado

### N01 · 0:00–0:22 · Cold open

Você tem uma linha de carga, uma esfera e duas placas. Os campos parecem pedir três receitas diferentes: um cai com a distância, outro cai ainda mais rápido, e outro nem diminui. Mas todos saem da mesma lei. O que muda: a fórmula, a superfície escolhida ou a carga que ficou dentro dela?

[ANIMAÇÃO: três fontes e três perfis breves; sem revelar derivações ou fazer gráfico quantitativo comparativo. Ciência antes da marca.]

### N02 · 0:22–0:36 · Intro humana

Você está no Parallax Lab. No primeiro vídeo, a simetria transformou fluxo em campo. Agora você vai usar essa ideia para reconhecer e resolver os casos clássicos, sem guardar uma receita para cada desenho.

[TELA: sistema de intro de yt_0001; título LEI DE GAUSS; subtítulo Três simetrias, um método.]

### N03 · 0:36–1:17 · Recap e algoritmo

A Lei de Gauss relaciona o fluxo por uma superfície fechada à carga envolvida. Sempre vale. A carga externa não entra nessa carga envolvida, mas pode contribuir para o campo local. Fluxo zero não garante campo zero. Para encontrar o campo diretamente, precisamos de simetria que simplifique esse fluxo.

Imagine uma moldura transparente que organiza a conta. Ela não altera cargas nem cria simetria.

Reconheça a fonte, encontre a direção do campo, escolha a superfície e veja quais partes contribuem para o fluxo. Calcule a carga envolvida na região. Vamos começar com um eixo.

[ANIMAÇÃO: construir o algoritmo, destacar a fonte cilíndrica. Leitura de 3 s incorporada ao orçamento.]

### N04 · 1:17–2:03 · Linha: reconhecer a simetria

Esta linha tem a mesma quantidade de carga por unidade de comprimento em todo lugar. Essa densidade linear é lambda. E a linha é infinita: uma idealização que elimina a influência das extremidades.

Se você anda ao longo dela, a fonte continua igual. Se gira ao redor do eixo, também. O campo não pode privilegiar uma posição ao longo da linha nem uma direção ao redor dela.

Os pares de carga em posições opostas ao longo do eixo cancelam a componente axial. Resta a direção radial, perpendicular à linha. Para carga positiva, o campo aponta para fora. Seu módulo só pode depender da distância ao eixo.

[DEMO: translação e rotação da fonte; cancelar componentes axiais de um par; pausar 3 s na direção radial.]

### N05 · 2:03–2:52 · Linha: lateral e tampas

Escolha um cilindro fechado com o mesmo eixo da linha. Seu raio é a distância onde você quer calcular o campo; seu comprimento é um trecho finito escolhido para a conta.

Na lateral, todos os pontos estão à mesma distância do eixo. O campo tem o mesmo módulo e aponta na direção da normal exterior. Por isso, o fluxo lateral vira campo vezes área lateral.

Nas tampas, acontece outra coisa. O campo é radial, mas a normal aponta ao longo do eixo. Campo e normal são perpendiculares: o produto escalar é zero.

Não é o campo que desaparece nas tampas. É a contribuição dessas tampas para o fluxo.

[ANIMAÇÃO: lateral contínua violeta; tampas fechadas; normais e vetores separados; 5 s para observar o produto escalar.]

### N06 · 2:52–3:36 · Linha: carga e resultado

A área lateral é dois pi vezes o raio vezes o comprimento. E a carga envolvida é a densidade linear vezes esse mesmo comprimento.

Colocando os dois lados na Lei de Gauss, o comprimento cancela. Ele era uma escolha nossa e não pode determinar o campo da fonte infinita.

O resultado cai com o inverso da distância ao eixo. Se você dobra essa distância, o campo cai pela metade. A carga por comprimento continua a mesma; a área lateral é que cresceu.

Essa é a primeira ferramenta. Vamos conservar o cilindro gaussiano e mudar apenas onde a carga está distribuída.

[BUILD: cancelar L, depois isolar E; leitura de 4 s no resultado e teste de dobrar r.]

### N07 · 3:36–4:22 · Casca cilíndrica

Agora a carga ocupa uma casca cilíndrica de raio fixo. Ela é uniforme, infinita ao longo do eixo e muito fina. Lambda continua representando a carga total por unidade de comprimento.

Com a gaussiana por dentro da casca, não há carga envolvida. E a mesma simetria radial permite concluir que o campo interno é zero. Sem essa simetria, carga envolvida zero não bastaria.

Por fora, a gaussiana envolve toda a carga daquele comprimento. O resultado externo é exatamente o da linha.

Ao atravessar a camada carregada, o campo salta de zero para um valor não nulo. Uma casca não tem o mesmo perfil de um maciço.

[COMPARE: r<R e r>R sequenciais; dois limites laterais, sem avaliar r=R nem interpolar um salto.]

### N08 · 4:22–5:14 · Cilindro maciço: duas regiões

Preencha o interior com carga distribuída uniformemente no volume de um material isolante. Agora a densidade é rô: carga por unidade de volume.

Se a gaussiana tem raio menor que o corpo, ela envolve apenas o cilindro de carga que ficou dentro dela. O volume usa o raio pequeno, não o raio inteiro da fonte.

A carga envolvida cresce com o quadrado do raio, enquanto a área lateral cresce com o raio. Dividindo uma pela outra, o campo cresce linearmente.

Quando a gaussiana passa para fora, a carga envolvida para de crescer. O raio da fonte entra na carga; o raio gaussiano continua na área. A partir daí, o campo volta a cair com o inverso da distância.

[BUILD: atualizar Q_env mantendo a relação de fluxo; 4 s para distinguir r e R.]

### N09 · 5:14–5:41 · Cilindro: gráfico e continuidade

O gráfico começa em zero no eixo, sobe em linha reta e encontra a curva externa na borda. Os dois resultados dão o mesmo valor ali.

A inclinação muda, mas o campo não salta: não acrescentamos uma camada superficial de carga. Compare com a casca. A geometria gaussiana é a mesma; a distribuição da carga muda o perfil.

[GRÁFICO: r/R e E/E_R sincronizados; 3 s no encontro em R.]

### N10 · 5:41–6:22 · Capacitor coaxial

Troque agora o isolante por um condutor maciço e acrescente uma casca condutora externa, coaxial. No equilíbrio eletrostático, a carga do condutor interno fica na sua superfície. As cargas por comprimento são iguais e opostas.

Dentro do metal, o campo é zero. No vão, a gaussiana envolve a carga positiva do interno e o campo segue o mesmo inverso do raio.

Por fora dos dois condutores, as cargas envolvidas se cancelam. Com a simetria cilíndrica do modelo, o campo externo é zero. O campo fica confinado ao vão, apontando do positivo para o negativo.

[COMPARE/BUILD: três regiões; casca externa delgada ideal; não apresentar capacitância.]

### N11 · 6:22–6:32 · Ponte para o plano

Um único cilindro gaussiano resolveu quatro fontes. Mudaram a carga envolvida e a região. E se a fonte tiver um plano inteiro de simetria?

[TRANSIÇÃO: preservar o método, retirar o cilindro apenas na troca de família.]

### N12 · 6:32–7:19 · Chapa: direção e idealização

Esta chapa não condutora tem carga uniforme por área. Essa densidade superficial é sigma. Ela é infinita nas duas direções do plano: não existem bordas distinguindo um ponto de outro.

Andar paralelamente à chapa não muda a fonte. Girar dentro do plano também não. Por simetria, o campo não tem componente paralela à chapa: ele só pode ser normal ao plano.

Para carga positiva, aponta para fora de cada lado. Os sentidos são opostos, mas os módulos são iguais, porque os dois lados da chapa são equivalentes.

É essa igualdade que vai permitir somar o fluxo das duas tampas. Não transfira essa conclusão automaticamente para uma placa finita.

[DEMO: translação no plano, normais opostas e vetores de mesmo comprimento; 3 s de leitura.]

### N13 · 7:19–8:06 · Chapa: duas tampas ativas

Use um cilindro gaussiano curto atravessando a chapa, como uma pequena caixa fechada. Cada tampa tem área A.

Na lateral, o campo corre tangente à superfície. A normal lateral é perpendicular a ele, então essa parte não contribui para o fluxo.

Nas duas tampas, campo e normal exterior apontam no mesmo sentido. Em cima, ambos para um lado; embaixo, ambos para o outro. As duas contribuições são positivas.

Temos campo vezes A mais campo vezes A: duas vezes campo vezes A. A carga envolvida é sigma vezes a área do pedaço de chapa dentro da caixa. Essa área coincide com a área de uma tampa.

[ANIMAÇÃO: marcar separadamente as duas tampas; não cancelar setas de fluxo; 5 s na soma.]

### N14 · 8:06–8:43 · Chapa: independência da distância

Aplicando Gauss, a área cancela. O campo de cada lado vale sigma dividido por duas vezes a permissividade do vácuo.

Repare: nenhuma distância à chapa aparece no resultado. Afaste as tampas mantendo sua área. A carga envolvida continua a mesma, e a área que recebe o fluxo também.

Por isso o campo não diminui com a distância neste modelo. A chapa tem extensão infinita; não estamos descrevendo uma placa real vista de muito longe. A idealização sustenta a simetria e o resultado.

[DEMO: afastar tampas sem alterar A; manter vetores iguais; respiro de 4 s.]

### N15 · 8:43–9:32 · Slab: carga dentro da espessura

Dê espessura à distribuição. Agora temos um slab: uma placa volumétrica infinita nas direções paralelas ao plano, mas com espessura finita.

O plano médio é a origem. As faces ficam à mesma distância dele, uma de cada lado. A densidade é volumétrica, rô, e o material continua sendo isolante.

Conserve a caixa gaussiana simétrica, com uma tampa de cada lado do centro. Comece observando um ponto à direita, ainda dentro da placa.

A espessura envolvida é duas vezes a distância desse ponto ao centro. Multiplicando pela área e pela densidade, você encontra a carga envolvida. O fluxo continua tendo duas tampas. Agora o campo cresce linearmente com a distância ao plano médio.

[BUILD: mostrar a fatia realmente envolvida; 4 s para separar x de a e sigma de rô.]

### N16 · 9:32–10:11 · Slab: exterior e gráfico assinado

Quando as tampas passam das faces, a caixa envolve toda a espessura. A carga envolvida fica constante e o campo também.

À esquerda, o campo aponta no sentido negativo do eixo; à direita, no positivo. Por isso este gráfico mostra a componente assinada, não o módulo.

Ela começa num patamar negativo, cresce linearmente dentro da placa, passa por zero no centro e termina num patamar positivo. O campo é contínuo nas duas faces. Não há folhas de carga extras ali, só o fim da densidade volumétrica.

[GRÁFICO: E_x versus x, dois lados; marcador sincronizado; 4 s nas faces e no centro.]

### N17 · 10:11–10:58 · Duas chapas opostas

Troque o slab por duas chapas paralelas com densidades iguais e sinais opostos. Para cada chapa, você já conhece o campo.

Entre elas, o campo da positiva aponta para a negativa, e o campo da negativa também. Os dois têm o mesmo sentido e se somam. O resultado é uniforme e vale sigma dividido pela permissividade.

Por fora, as contribuições têm sentidos opostos e módulos iguais. Elas se cancelam.

Esse é o campo do capacitor plano ideal, desprezando bordas. Ao interpretá-lo com placas condutoras, as cargas indicadas pertencem às faces voltadas para o vão. Não vamos calcular capacitância: queremos entender o campo e onde ele existe.

[COMPARE: folha única versus duas folhas; setas auxiliares antes da resultante; 4 s para o cancelamento exterior.]

### N18 · 10:58–11:54 · Face condutora: fator dois

Há uma consequência curta que evita uma confusão comum. Junto à superfície de um condutor em equilíbrio, o campo dentro do metal é zero.

Pegue uma caixa gaussiana muito pequena atravessando uma face. A tampa que ficou dentro do metal não contribui. A lateral também não contribui no limite em que a caixa fica achatada. Só sobra a tampa no vácuo.

Agora o fluxo é campo vezes área, sem o fator dois. O campo normal logo fora vale a densidade superficial daquela face dividida pela permissividade.

Atenção à palavra face. Essa densidade é local; não é a carga total de uma lâmina inteira dividida por sua área. A folha isolante tinha dois lados ativos. Aqui, uma tampa está no metal. As hipóteses mudaram, não a Lei de Gauss.

[TELA: σ_face na face; normal saindo do metal; comparação EA/2EA; 4 s de leitura.]

### N19 · 11:54–12:03 · Ponte para a esfera

A mesma caixa atravessou chapa, slab e face condutora. Falta a geometria que distribui as direções igualmente ao redor de um centro.

[TRANSIÇÃO: plano sai; casca esférica entra sem nova intro institucional.]

### N20 · 12:03–12:50 · Casca esférica: aparato

Distribua uma carga total sobre uma casca esférica, uniformemente. A casca tem raio fixo. Sem outras fontes, todas as rotações ao redor do centro deixam a distribuição igual.

O campo só pode ser radial, e seu módulo depende apenas da distância ao centro. Escolha uma esfera gaussiana concêntrica.

Em todos os pontos dela, o campo tem o mesmo módulo e está alinhado à normal. Toda a superfície contribui: o fluxo é campo vezes quatro pi vezes o quadrado do raio.

É a mesma construção esférica do primeiro vídeo. A pergunta que decide os ramos agora é simples: a esfera gaussiana envolve a casca carregada ou ainda está dentro dela?

[BUILD: esfera fechada, normal exterior e área total; 3 s antes de escolher a região.]

### N21 · 12:50–13:31 · Casca esférica: regiões

Por dentro, a carga envolvida é zero. Junto da simetria esférica, isso dá campo interno zero. Não é uma regra para qualquer superfície vazia.

Por fora, a carga envolvida é a carga total da casca. Dividindo pela área da esfera gaussiana e pela permissividade, o campo cai com o quadrado da distância.

Externamente, ele coincide com o campo de uma carga pontual colocada no centro. Essa equivalência não vale por dentro da casca.

E aqui também há um salto na camada superficial carregada: o campo interno é zero; logo do lado externo, é não nulo.

[COMPARE: domínio em cada resultado; mini-indicação dos limites laterais; 3 s no salto.]

### N22 · 13:31–14:37 · Esfera maciça: revisão e comparação

Preencha a esfera com carga uniforme no volume de um isolante. Este é o caso que já desenvolvemos no primeiro longo, então vamos recuperar o raciocínio sem refazer toda a derivação.

Por dentro, a carga envolvida cresce com o cubo do raio. A área gaussiana cresce com o quadrado. O campo, portanto, cresce linearmente, partindo de zero no centro.

Por fora, a carga envolvida para de crescer. A área continua aumentando com o quadrado da distância, e o campo passa a cair com o inverso desse quadrado.

Os dois ramos se encontram sem salto na borda, porque não há uma camada superficial adicional.

Compare o gráfico com o do cilindro maciço. Ambos crescem linearmente por dentro, mas suas caudas externas são diferentes: inverso do raio no cilindro, inverso do raio ao quadrado na esfera. Aqui normalizamos cada gráfico pelo seu próprio valor na borda para comparar o formato, não a intensidade absoluta.

[GRÁFICO: construir esfera e reapresentar cilindro sequencialmente; 5 s de comparação; não rederivar dV.]

### N23 · 14:37–15:27 · Capacitor esférico

Troque a esfera isolante por uma esfera condutora maciça em equilíbrio. Sua carga positiva fica na superfície. Acrescente uma casca condutora concêntrica com carga igual e negativa.

Dentro do condutor central, o campo é zero. No vão, a esfera gaussiana envolve apenas a carga positiva. O campo é radial e cai com o quadrado da distância ao centro.

Depois da casca externa, a carga envolvida total é zero. Com a simetria esférica, o campo externo também é zero.

Temos de novo um campo confinado entre condutores. Mas ele não tem o mesmo perfil do cabo coaxial ou das placas paralelas. A mesma lei resolveu os três; a geometria deixou uma assinatura diferente em cada resultado.

[COMPARE/BUILD: núcleo MACIÇO rotulado; casca externa delgada; três domínios; 4 s na região do vão.]

### N24 · 15:27–16:09 · Três capacitores

Coloque os três capacitores lado a lado. Nas placas paralelas ideais, o campo no vão é constante. No coaxial, cai com o inverso da distância ao eixo. No esférico, cai com o inverso do quadrado da distância ao centro.

Essa comparação vale entre os condutores. Fora dos três sistemas, o campo é zero nos modelos que escolhemos, com cargas iguais e opostas e sem fontes externas.

Não são três leis. São três formas de simplificar a mesma Lei de Gauss. A superfície onde o fluxo contribui ajuda a entender por que os perfis são diferentes.

[COMPARE: revelar um caso por vez; somente depois manter três diagramas pequenos e uma lei em cada; 4 s de leitura.]

### N25 · 16:09–17:01 · Área, carga fixa e potências

Na esfera, a área cresce com o quadrado do raio. Se a carga envolvida já é fixa, o campo precisa cair nessa mesma proporção para conservar o fluxo.

No cilindro, para um comprimento escolhido, a área lateral cresce com o raio. Com a carga envolvida fixa naquele trecho, o campo cai com o inverso do raio.

No plano, afastar as tampas não aumenta a área delas nem a carga envolvida da chapa. O campo permanece constante.

Mas não transforme isso numa regra de espalhamento que funciona para qualquer fonte. Foi a simetria que permitiu usar um único campo nas partes relevantes. E, por dentro dos maciços, a carga envolvida também cresce. Você precisa olhar os dois lados da equação.

[BUILD/FOCUS: área e Q_env em destaque alternado; retomar crescimento interior brevemente; 4 s no vínculo entre hipóteses e potência.]

### N26 · 17:01–17:59 · Checklist aplicado

Antes da integral, faça seis perguntas. Qual é a simetria da fonte? Em que direção o campo pode apontar? De quais coordenadas seu módulo pode depender?

Depois escolha uma superfície fechada onde o campo seja constante nas partes que contribuem, ou tangente nas que não contribuem. Calcule a carga realmente envolvida. E confira se o problema precisa ser dividido em regiões.

Uma esfera concêntrica resolve a família esférica. Um cilindro coaxial resolve a família cilíndrica infinita. Uma caixa curta atravessando o plano resolve a família planar apropriada.

Vamos testar: no cilindro maciço, por dentro, você usa o raio da gaussiana para calcular o volume envolvido. Por fora, usa o raio da fonte. A superfície foi reaproveitada; a carga mudou. É isso que você precisa reconhecer, antes de procurar uma fórmula pronta.

[TELA: checklist progressivo, uma pergunta por vez; aplicar ao A3; 5 s para a decisão dentro/fora.]

### N27 · 17:59–18:17 · Payoff

Você não precisa decorar dez campos diferentes. Identifique a simetria da fonte, escolha uma superfície onde o fluxo simplifique e calcule a carga envolvida na região. Esfera, cilindro e plano são três versões do mesmo raciocínio. Agora você tem um método para começar.

[FOCUS: headline científica; retirar os detalhes do checklist.]

### N28 · 18:17–18:19 · Pausa

[PAUSA DE 2 s: sem fala, sem CTA; sustentar o payoff.]

### N29 · 18:19–18:42 · CTA / outro

Agora que você conhece os casos clássicos, no próximo vídeo vamos usar Gauss em problemas em que escolher a estratégia é a parte difícil. Se esse método te ajudou, deixa o like e se inscreve no Parallax Lab para acompanhar a sequência. A gente se vê no próximo.

[OUTRO: logo horizontal, mensagem curta e anéis discretos do yt_0001; sem promessa de data ou vídeo recomendado ainda inexistente.]
