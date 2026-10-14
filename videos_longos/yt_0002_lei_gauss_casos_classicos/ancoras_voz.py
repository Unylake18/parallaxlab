"""yt_0002 — âncoras entre a cena e a voz: (instante editorial t de um `at(t)` da cena, trecho da fala que deve COMEÇAR nesse instante).

Os t são os marcos reais de `cena.py` (cada `self.at(t)` marca o início de um evento visual: vetor, passo de equação, gráfico, etc.);
os trechos são sequências de palavras de `texto_narracao.txt`, procuradas em ordem. `gerar_sync.py alinhar` converte cada par em um
nó [t_editorial, t_voz]; a cena converte todos os outros marcos por interpolação entre os nós.

Regras: ordem estritamente crescente nos dois eixos; o trecho aponta o início da cláusula que descreve o evento. A fala começa LEAD segundos
antes do evento na tela (ver gerar_sync.py).
"""

ANCORAS = [
    # N01 cold open (os perfis entram um a um: linha 7,4 · esfera 10,2 · placas 13,0 · traço 14,9 · pergunta 17,0)
    (0.0, "Uma linha de carga"), (7.4, "Na linha, o campo cai"), (10.2, "Na esfera, como um sobre"), (13.0, "Entre placas ideais"),
    (14.9, "Três perfis diferentes"), (17.0, "Então, o que muda de verdade"),
    # N02 intro
    (22.0, "Fala, pessoal"), (29.5, "Hoje a gente pega"),
    # N03 recap: P0 · sempre vale · carga externa · vetores entram/saem · Φ = 0 · Φ = 0 ⇏ E = 0 · simetria · moldura · algoritmo
    (36.0, "A Lei de Gauss vale pra qualquer"), (42.6, "Uma carga que ficou fora"), (44.6, "O campo dela entra de um lado"),
    (47.0, "e o fluxo líquido dá zero"), (48.6, "Por isso, fluxo zero"), (51.8, "Pra achar o campo direto"), (53.0, "É ela que diz a direção"),
    (55.6, "A superfície é só uma moldura"), (62.3, "Daí vem o método"), (62.9, "identifica a fonte"), (64.1, "reconhece a simetria"),
    (65.5, "descobre a direção"), (67.2, "escolhe a gaussiana"), (68.8, "simplifica o fluxo"), (70.2, "e calcula a carga envolvida"),
    (71.6, "dividindo em regiões"), (72.6, "quando precisar"), (75.5, "Vamos começar pela simetria"),
    # N04 linha: reconhecer a simetria
    (77.0, "Essa linha tem a mesma carga"), (79.0, "a densidade linear de carga"), (81.5, "E ela é infinita"), (88.0, "Imagina que você anda"),
    (95.0, "ou gira em volta dela"), (103.0, "Agora pega um ponto"), (106.6, "As componentes ao longo da linha"),
    (113.4, "e o mesmo vale pra todos"), (116.5, "Sobra só a direção radial"),
    # N05 lateral e tampas
    (123.0, "Agora escolhe um cilindro fechado"), (127.5, "O raio dele é a distância"), (131.0, "O comprimento é um trecho"),
    (134.6, "Na lateral, todos os pontos"), (138.0, "aponta na direção da normal"), (143.0, "O fluxo lateral vira"),
    (147.8, "Nas tampas é diferente"), (150.3, "mas a normal da tampa"), (154.0, "O campo ali não é nulo"), (158.6, "Repara nisso"),
    (168.0, "E é isso que deixa só a lateral"),
    # N06 carga envolvida e resultado
    (172.0, "O fluxo é o campo vezes dois pi"), (177.8, "E a carga envolvida é a densidade linear"), (181.0, "Na Lei de Gauss, o comprimento"),
    (185.2, "e cancela"), (187.4, "Faz sentido"), (188.8, "O campo vale lambda sobre"), (193.0, "cai como um sobre a distância"),
    (195.6, "Testa: dobra a distância"), (199.8, "A área lateral dobra"), (207.0, "Essa é a nossa primeira ferramenta"),
    # N07 casca cilíndrica
    (216.0, "Agora a carga deixa de estar num fio"), (221.0, "Lambda continua sendo"), (227.6, "Com a gaussiana por dentro da casca"),
    (231.4, "E, pela simetria cilíndrica"), (239.6, "Por fora, a gaussiana envolve"), (243.0, "e o resultado é exatamente o da linha"),
    (246.8, "Mas olha: ao atravessar"), (256.0, "Uma casca não tem o perfil"),
    # N08 cilindro maciço (cada passo de equação: 279,5 Gauss · 281,4 πL · 284 cancela · 287,4 r · 291 r²÷r · 292 resultado)
    (262.0, "Agora preenche o interior"), (271.6, "Com a gaussiana menor que"), (279.5, "A carga envolvida cresce com o raio ao quadrado"),
    (281.4, "a área lateral cresce"), (291.0, "e sobra o raio"), (292.0, "o campo cresce em linha reta"),
    (294.4, "Quando a gaussiana passa pra fora"), (298.0, "Aí o raio da fonte"), (304.6, "e o raio da gaussiana continua"),
    (306.2, "Dois raios diferentes"),
    # N09 gráfico
    (314.0, "Juntando tudo num gráfico"), (316.4, "Ele sobe em linha reta"), (320.0, "e encontra a curva de fora"),
    (321.8, "A inclinação muda ali"), (329.6, "A gente não colocou nenhuma camada"), (335.8, "Compara com a casca"),
    # N10 coaxial
    (341.0, "Agora troca o isolante"), (346.0, "com uma casca condutora em volta"), (355.4, "Dentro de um condutor em equilíbrio"),
    (359.8, "No vão, entre os dois condutores"), (365.4, "Por fora das duas camadas"), (371.5, "O campo fica preso no vão"),
    # N11 ponte
    (382.0, "Um único cilindro gaussiano"), (385.5, "Mudou só a carga envolvida"), (388.2, "E se a fonte for um plano inteiro"),
    # N12 folha
    (392.0, "Essa chapa não condutora"), (395.0, "a densidade superficial de carga"), (399.0, "Anda paralelo à chapa"),
    (412.0, "Por simetria, as componentes paralelas"), (418.4, "se cancelam, por pares"), (422.0, "Sobra só a componente perpendicular"),
    (427.0, "Pra carga positiva, ele aponta pra fora"), (439.0, "Como superfície, um cilindro curto"),
    (450.0, "Na lateral, o campo é tangente"), (454.0, "Nas duas tampas, o campo"), (458.0, "O fluxo é o campo vezes a área da tampa"),
    (464.0, "duas vezes o campo vezes a área"), (468.0, "A carga envolvida é sigma vezes"), (474.0, "Na Lei de Gauss, a área cancela"),
    (484.6, "e o campo vale sigma sobre"), (489.0, "Repara: não aparece distância"), (500.0, "Isso vale pra chapa infinita"),
    # N13 slab (gráfico: 525 · +a 528 · >a 534 · centro 541 · −a 550 · <−a 556 · contínuo 562)
    (504.0, "Agora a folha ganha espessura"), (507.0, "A carga não está mais sobre"), (512.0, "Começa com um ponto à direita"),
    (517.0, "Então a espessura que ela envolve"), (519.0, "A carga envolvida cresce com essa distância"),
    (525.0, "No centro, por simetria"), (528.0, "Do outro lado, o sentido"), (534.0, "Quando a gaussiana passa das faces"),
    (550.0, "Na passagem pelas faces"), (562.0, "Por isso o campo é contínuo"),
    # N14 duas folhas
    (574.0, "Agora troca a placa por duas chapas"), (577.5, "Cada uma, sozinha"), (588.0, "Por fora das duas chapas"),
    (594.5, "Entre as chapas, o campo da positiva"), (599.0, "Os dois se somam"), (606.5, "Esse é o campo do capacitor plano ideal"),
    (611.4, "A gente não vai calcular capacitância"),
    # N15 face de condutor e síntese planar
    (616.0, "Tem uma consequência curta"), (619.0, "Junto à superfície de um condutor"), (624.5, "Metal de um lado, vácuo do outro"),
    (628.0, "Pega uma caixa gaussiana pequena"), (638.0, "Então o fluxo é só o campo vezes a área"),
    (651.0, "Repara na diferença pra folha isolante"), (655.0, "Cuidado com a palavra face"), (657.5, "Mudaram as hipóteses"),
    (664.0, "A mesma caixa atravessou"), (672.5, "Falta a geometria que trata"),
    # N20 casca esférica
    (681.0, "Agora distribui uma carga total"), (688.0, "Gira a esfera em torno do centro"), (695.5, "Então o campo só pode ser radial"),
    (702.0, "A gaussiana é uma esfera com o mesmo centro"), (707.0, "Em todos os pontos dela, o campo"),
    (712.0, "Então o fluxo é o campo vezes a área da esfera"), (718.0, "A pergunta que decide tudo"),
    # N21 regiões
    (731.0, "Por dentro, a carga envolvida é zero"), (735.0, "o campo também é zero"), (740.0, "Por fora, a carga envolvida é a carga total"),
    (744.0, "O campo vale a carga total sobre"), (747.5, "cai com um sobre o raio ao quadrado"),
    (752.0, "É igual ao campo de uma carga pontual"), (757.0, "Por dentro, essa equivalência"), (760.5, "E aqui também tem um salto"),
    (766.0, "É a camada de carga na superfície"),
    # N22 esfera maciça (equação: 784 Gauss · 787,3 cancela 4π · 791,6 r³÷r² · 792,6 resultado · 795,5 fora · 799,5 · 805,6 resultado)
    (776.0, "Agora preenche a esfera"), (779.0, "Por dentro, a carga envolvida cresce com o cubo"), (784.0, "e a área da gaussiana cresce"),
    (791.6, "Divide uma pela outra"), (792.6, "o campo cresce em linha reta, a partir"), (795.5, "Por fora, a carga envolvida para de crescer"),
    (799.5, "A área continua crescendo"), (805.6, "Então o campo passa a cair"), (812.0, "No gráfico, os dois ramos"),
    (825.0, "Comparando com o cilindro maciço"), (831.0, "Cada gráfico está normalizado"),
    # N23 capacitor esférico
    (840.0, "Agora troca a esfera isolante"), (845.0, "Em volta, uma casca condutora"), (850.0, "Dentro do condutor central"),
    (856.0, "No vão, entre os dois condutores, ela"), (864.5, "Depois da casca externa"), (873.0, "De novo, o campo fica preso"),
    (878.0, "Mas o perfil não é o do coaxial"),
    # N24 três capacitores
    (886.0, "Os três capacitores, lado a lado"), (894.0, "No coaxial, ele cai"), (902.0, "No esférico, cai"),
    (910.0, "Por fora, o campo é zero nesses modelos"), (917.0, "Não são três leis"),
    # N25 áreas e potências
    (928.0, "Olha de novo essas potências"), (932.0, "Na esfera, a área da gaussiana"), (943.0, "No cilindro, pra um comprimento"),
    (946.0, "Então, com a carga envolvida fixa naquele"), (957.0, "No plano, afastar as tampas"), (960.0, "Então o campo fica constante"),
    (969.0, "Mas isso não é regra"), (973.0, "E, por dentro dos maciços"),
    # N26 checklist
    (980.0, "Antes de integrar, faz seis perguntas"), (989.0, "Segunda: em que direção"), (997.0, "Terceira: de quais coordenadas"),
    (1005.0, "Quarta: qual superfície fechada"), (1013.0, "Quinta: quanta carga"), (1020.0, "Sexta: o problema precisa"),
    (1026.0, "Por fora, entra o raio da fonte"), (1033.0, "A superfície foi a mesma"),
    # N27 payoff e CTA
    (1038.0, "Você não precisa decorar um campo diferente"), (1043.0, "escolhe uma superfície onde o fluxo simplifica"),
    (1058.0, "No próximo vídeo de Gauss"), (1066.0, "Se esse vídeo te ajudou"), (1072.0, "A gente se vê no próximo"),
]
