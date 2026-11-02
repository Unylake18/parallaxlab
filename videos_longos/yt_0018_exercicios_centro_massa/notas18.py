"""yt_0018 v7b: anotações curtas que entram NA PALAVRA da fala (presas ao relógio da cena, sem tween e sem piscar), no lugar dos realces.
Cada anotação nasce 0,4 s antes da palavra (fade de entrada de 0,35 s), fica até a próxima anotação da âncora (ou o fim da âncora) e sai em fade.
É escrita nova, só reforça o que a voz acabou de dizer: nenhuma anotação traz número ou ideia que a voz não tenha dito.

NOTAS = {âncora: [(índice da palavra na fala da âncora, texto), ...]}   (o índice vem de renders/v7/_notas_pontos.json)
SLOTS = {âncora: (x, y) ou [candidatos]}  centro da anotação; SLOTS_ESQ_CONTA vale para o ESQUEMA × CONTA (parte de baixo da CONTA primeiro).
"""
_PONTOS = [
    # A2
    ("A2", 20, "SEIS PROBLEMAS DIFERENTES"), ("A2", 27, "AS MESMAS POUCAS IDEIAS"),
    # A3
    ("A3", 15, "COMO UMA PARTÍCULA"), ("A3", 29, "SÓ AS FORÇAS DE FORA"),
    # A4
    ("A4", 5, "TRÊS PERGUNTAS"), ("A4", 10, "O SISTEMA"), ("A4", 19, "O REFERENCIAL"), ("A4", 27, "TODO PROBLEMA DIFÍCIL"), ("A4", 39, "RESPONDA AS TRÊS"),
    # X1-1
    ("X1-1", 14, "FURO FORA DO CENTRO"), ("X1-1", 18, "ESPESSURA UNIFORME"),
    # X1-2
    ("X1-2", 0, "ANTES DA CONTA"), ("X1-2", 4, "PROCURE A SIMETRIA"), ("X1-2", 9, "A DIAGONAL"), ("X1-2", 15, "CENTRO DA PLACA E DO FURO"), ("X1-2", 38, "X = Y"),
    # X1-3
    ("X1-3", 12, "PLACA CHEIA: 1.600 CM QUADRADOS"),
    # X1-4
    ("X1-4", 30, "O FURO TIRA CERCA DE 1/5"), ("X1-4", 48, "A DICA CORTA A CONTA"),
    # X2-2
    ("X2-2", 8, "MONTAR POR PARTES"), ("X2-2", 14, "ARESTA RETA E UNIFORME"), ("X2-2", 33, "CADA PEDAÇO: UM TERÇO"), ("X2-2", 39, "O FIO VIRA PARTÍCULAS"),
    ("X2-2", 47, "UMA NO MEIO DE CADA ARESTA"),
    # X2-3
    ("X2-3", 8, "MÉDIA SIMPLES"), ("X2-3", 25, "UMA DIMENSÃO POR VEZ"), ("X2-3", 40, "NA LARGURA: MÉDIA MEIO METRO"),
    # X2-3b
    ("X2-3b", 33, "A MASSA NÃO ESTÁ NOS CANTOS"), ("X2-3b", 38, "ESTÁ NAS ARESTAS"),
    # X2-4
    ("X2-4", 13, "A UNS 24 CENTÍMETROS DO FIO"), ("X2-4", 24, "O CM PODE FICAR NO AR"), ("X2-4", 33, "FORA DO MATERIAL"), ("X2-4", 37, "COORDENADAS ENTRE 0 E 1"),
    ("X2-4", 43, "DENTRO DO CUBO"), ("X2-4", 51, "A DICA: EM 3D"), ("X2-4", 55, "SEPARE AS COORDENADAS"), ("X2-4", 60, "CADA UMA É UM PROBLEMA 1D"),
    # X3-5
    ("X3-5", 10, "A FOLHA ESTÁ ANDANDO"), ("X3-5", 14, "TROCA DE RÉGUA"),
    # X3-5b
    ("X3-5b", 10, "SISTEMA: GAFANHOTO + FOLHA"),
    # X3-9
    ("X3-9", 47, "PRIMEIRO: EM RELAÇÃO A QUÊ?"),
    # X3-10
    ("X3-10", 6, "PERGUNTA RESPONDIDA"), ("X3-10", 10, "CONTINUA NA FOLHA DE 2 JEITOS"), ("X3-10", 28, "CHEGA À PONTA OPOSTA"), ("X3-10", 36, "NO MEIO A FOLHA FOGE"),
    # X4-1
    ("X4-1", 2, "NO ESPAÇO"), ("X4-1", 18, "NAVE DE 2.000 QUILOS"), ("X4-1", 23, "PARADAS NO REFERENCIAL DO CM"), ("X4-1", 27, "UMA CARGA ENTRE ELAS"),
    # X4-2
    ("X4-2", 22, "MOMENTOS IGUAIS E OPOSTOS"), ("X4-2", 26, "MESMO TAMANHO"),
    # X4-3
    ("X4-3", 13, "MOMENTOS IGUAIS, ENERGIAS NÃO"),
    # X4-4
    ("X4-4", 18, "COM O MESMO MOMENTO"), ("X4-4", 24, "MENOS MASSA, MAIS ENERGIA"), ("X4-4", 76, "ENERGIA DIVIDIDA"),
    # X4-5
    ("X4-5", 7, "MASSAS IGUAIS: MEIO A MEIO"), ("X4-5", 16, "A OUTRA LEVA QUASE TUDO"), ("X4-5", 28, "ENERGIA NA RAZÃO INVERSA"), ("X4-5", 33, "DAS MASSAS"),
    ("X4-5", 39, "O TOTAL NÃO MUDA"), ("X4-5", 55, "JUNTAS, A DEZ METROS POR SEGUNDO"), ("X4-5", 61, "ANTES: 150.000 J"), ("X4-5", 98, "A PARTE RELATIVA"), ("X4-5", 102, "NENHUM REFERENCIAL MUDA"),
    # X5-1
    ("X5-1", 14, "BLOCOS DE 3 E 1 QUILOS"), ("X5-1", 21, "PENDURADOS NO FIO"), ("X5-1", 25, "TRAVADOS"), ("X5-1", 30, "A BALANÇA SOMA TUDO"),
    # X5-2
    ("X5-2", 15, "SOLTOU: MARCA 5 QUILOS"),
    # X5-3
    ("X5-3", 1, "PRIMEIRO: O SISTEMA"), ("X5-3", 12, "SUPORTE, POLIA E FIO"), ("X5-3", 15, "E OS DOIS BLOCOS"), ("X5-3", 21, "O FIO PUXA BLOCOS E POLIA"), ("X5-3", 27, "ISSO É FORÇA INTERNA"),
    ("X5-3", 36, "DE FORA: SÓ DUAS"), ("X5-3", 41, "O PESO DE TUDO, PARA BAIXO"), ("X5-3", 60, "MASSA TOTAL × A DO CM"),
    # X5-4
    ("X5-4", 13, "BLOCO PESADO: PESO − TRAÇÃO"), ("X5-4", 22, "BLOCO LEVE: TRAÇÃO − PESO"), ("X5-4", 31, "SOMANDO, A TRAÇÃO SOME"), ("X5-4", 35, "FORÇA INTERNA CANCELA"),
    ("X5-4", 41, "SOBRA A DIFERENÇA DOS PESOS"), ("X5-4", 46, "ACELERANDO AS DUAS JUNTAS"),
    # X5-5
    ("X5-5", 33, "O CM DESCE ACELERANDO"),
    # X5-6
    ("X5-6", 14, "PESO TOTAL − M × A"), ("X5-6", 39, "NENHUMA MASSA FOI EMBORA"), ("X5-6", 45, "É O CM QUE ACELERA"),
    # X5-7
    ("X5-7", 9, "TRAÇÃO: 14,7 N"), ("X5-7", 13, "A POLIA É PUXADA PARA BAIXO"), ("X5-7", 20, "PELOS DOIS LADOS DO FIO"), ("X5-7", 29, "A BALANÇA SEGURA O SUPORTE"),
    ("X5-7", 34, "MAIS AS DUAS TRAÇÕES"), ("X5-7", 39, "49 N DE NOVO"), ("X5-7", 45, "CASOS-LIMITE"),
    # X5-8
    ("X5-8", 34, "O CAVALO PUXANDO A PEDRA"), ("X5-8", 40, "A FORÇA EXTERNA"), ("X5-8", 44, "SAI DA ACELERAÇÃO DO CM"),
    # EP1
    ("EP1", 11, "CAIXA PARADA NO ESPAÇO"), ("EP1", 28, "ABSORVIDO NA OUTRA PAREDE"), ("EP1", 34, "A LUZ CARREGA MOMENTO"),
    # EP2
    ("EP2", 0, "SÓ FORÇAS INTERNAS"), ("EP2", 4, "O CM NÃO ANDA"), ("EP2", 14, "A CAIXA FOI PARA A ESQUERDA"), ("EP2", 27, "EINSTEIN, 1906"), ("EP2", 31, "A MESMA PERGUNTA"),
    ("EP2", 38, "A RESPOSTA"), ("EP2", 45, "ENERGIA CARREGA INÉRCIA"), ("EP2", 50, "NÃO É DEMONSTRAÇÃO"), ("EP2", 58, "PORTA DA RELATIVIDADE"),
    # S2
    ("S2", 12, "CORPO COMPLICADO"), ("S2", 16, "PARTÍCULAS NO CM DE CADA PEDAÇO"), ("S2", 27, "SEM FORÇA EXTERNA: CM PARADO"), ("S2", 38, "TROCA DE RÉGUA"),
    ("S2", 44, "OS MOMENTOS SE CANCELAM"), ("S2", 50, "SOBRA A ENERGIA RELATIVA"), ("S2", 61, "CM ACELERA: FORÇA EXTERNA"), ("S2", 75, "AS TRÊS PERGUNTAS VALEM SEMPRE"),
    ("S2", 81, "TEM FORÇA EXTERNA?"), ("S2", 87, "EM QUE DIREÇÃO?"), ("S2", 92, "DE QUAL REFERENCIAL?"),
    ("S2", 101, "O MAIS DIFÍCIL SUMIU"), ("S2", 105, "ESCOLHEU BEM O SISTEMA"),
    # EN1
    ("EN1", 6, "SE ISSO MUDOU SEU OLHAR"), ("EN1", 30, "FÍSICA QUE PARECE DIFÍCIL"), ("EN1", 34, "COM ANIMAÇÃO"), ("EN1", 39, "E CONTA PASSO A PASSO"), ("EN1", 45, "DE ONDE CADA RESULTADO VEM"),
]
NOTAS = {}
for _aid, _i, _txt in _PONTOS:
    NOTAS.setdefault(_aid, []).append((_i, _txt))

# ESQUEMA × CONTA (PX0…PX5): candidatos em ordem; vale o primeiro que não encosta em nada (CONTA de baixo para cima, depois o ESQUEMA)
SLOTS_ESQ_CONTA = [(4.0, -3.3), (4.0, -2.75), (4.0, -2.2), (4.0, -1.65), (4.0, -1.1), (4.0, -0.55), (-3.8, -3.75), (-3.8, 2.65), (4.0, -3.64), (5.2, -3.64), (-4.4, -3.64)]
# demais âncoras: centro preferido (uma lista vale como candidatos em ordem; um ponto só, o código tenta também 0,6 acima, 0,6 abaixo e 1,2 acima)
SLOTS = {
    "A2": (0.0, -3.1), "A3": (4.0, -2.75), "A4": (0.0, -3.1),
    "EP1": [(0.0, -2.35), (0.0, 1.2), (0.0, -3.2)],
    "EP2": [(-3.4, 1.0), (3.4, 1.0), (0.0, -2.35), (0.0, -3.5), (0.0, -3.62), (-5.4, 0.2), (-5.4, -0.9)], "S2": [(0.0, 0.6), (0.0, -3.55), (0.0, 3.2)],
    "EN1": [(-4.9, 0.4), (4.9, 0.4), (-4.9, -0.6), (4.9, -0.6), (-4.9, 2.0), (4.9, 2.0), (-4.9, 3.0), (4.9, 3.0), (0.0, -1.75), (0.0, -2.45), (0.0, -3.1), (0.0, -3.62)],
}
