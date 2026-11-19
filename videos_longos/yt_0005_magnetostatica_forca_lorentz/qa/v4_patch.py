"""v4: cortes da tabela de condensação (alvo ~23 min). Chave = início da fala da v3.1; valor = nova fala ("—" = sem fala, a animação segue)."""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
L = open(src, encoding="utf-8").read().split("\n")
S = "—"

C = {
    # B01
    "Nos extremos, a força é nula:": "Nos extremos a força é nula: com a velocidade paralela ou antiparalela ao campo, ou com a carga parada. E com a velocidade perpendicular, o seno vale um e a força é a máxima.",
    "E com a velocidade perpendicular ao campo, o seno vale um": S,
    "Dá pra organizar isso decompondo": "Dá pra decompor a velocidade em uma componente paralela e uma perpendicular ao campo. A paralela, no produto vetorial com o campo, dá zero: não contribui em nada.",
    "A paralela, no produto vetorial com o campo, dá zero": S,
    # B02
    "Agora olhamos ao longo da direção do campo": "Agora olhamos ao longo do campo: as linhas viram pontinhos saindo da tela. A perspectiva muda, a física não.",
    "Com carga negativa e as mesmas condições iniciais, a órbita": "Com carga negativa e as mesmas condições iniciais, a órbita e o vetor giram no sentido contrário, com a mesma frequência angular: o módulo da carga fixa a rapidez do giro, e o sinal, o sentido.",
    "Voltando ao círculo: a força magnética é perpendicular": S,
    "Dá pra conferir o raio por outro caminho": "Como verificação, a força magnética faz o papel de força centrípeta, e igualar o módulo dela à massa vezes a rapidez ao quadrado dividida pelo raio dá o mesmo raio.",
    "Duas partículas, mesma massa": "Duas partículas, raios diferentes, e passam juntas pelo ponto de partida a cada período.",
    # B03
    "As duas componentes não se misturam": S,
    "Comparando condições iniciais diferentes": "Comparando condições iniciais diferentes: com menos velocidade perpendicular, o raio diminui e o passo fica igual; com mais componente paralela, o passo cresce e o raio fica igual. Sem componente perpendicular, sobra um movimento retilíneo ao longo do campo.",
    "Com a componente paralela maior": S,
    "Casos limite:": S,
    "Com carga negativa, mesma massa e mesmas condições iniciais, ela gira": S,
    # B04
    "Se outra força realizasse trabalho": S,
    "Isso não quer dizer que um motor": "Isso não quer dizer que um motor não transfira energia: ela vem da fonte elétrica, e o campo magnético organiza as forças que a convertem em movimento.",
    # B05
    "E se o condutor é uma lâmina": S,
    "A densidade superficial de corrente, que na tela aparece como K": "Numa lâmina, a corrente se espalha pela largura: a densidade superficial de corrente, que na tela aparece como K, é a corrente por unidade de largura. E, com sigma, a densidade superficial de carga, ela é sigma vezes a velocidade.",
    "Do lado da carga, sigma": S,
    "Para uma espécie de portador, a densidade superficial": S,
    "Com várias espécies": "Com várias espécies, somamos as contribuições com seus sinais. Mesmo com carga líquida zero, a densidade de corrente pode não ser zero.",
    # B06
    "Num pequeno intervalo, atravessa a carga": S,
    "Entrada igual à saída": "Entrada igual à saída: a carga dentro fica constante. Saída maior, ela diminui; entrada maior, aumenta. A carga não aparece nem some.",
    "Saída maior que entrada": S,
    "Voltando a igualar": S,
    "Entrada maior que saída": S,
    "O que entra ou fica armazenado": S,
    "Usamos a normal que aponta pra fora": "Usamos a normal pra fora: na entrada, o produto escalar é negativo; na saída, positivo. A integral na fronteira é o fluxo líquido pra fora: o que sai menos o que entra.",
    "A integral na fronteira inteira": S,
    "A carga dentro é a integral da densidade volumétrica": "A carga dentro é a integral da densidade volumétrica de carga no volume, que é fixo: só a densidade pode variar no tempo.",
    "O volume é fixo, então só a densidade": S,
    "Nestas células": S,
    # B07
    "Rapidez menor que a selecionada": "O feixe desvia pra cima se a rapidez é menor que a selecionada, e pra baixo se é maior. As curvas fora da condição selecionada são esquemáticas.",
    "Rapidez maior: ganha a magnética": S,
    "Com carga negativa, as duas forças invertem": "Com carga negativa, as forças invertem, mas a rapidez selecionada é a mesma.",
    # B08
    "É a mesma ideia do círculo do B02": "A força magnética faz o papel de força centrípeta, a resultante que aponta pro centro: o módulo da carga vezes a rapidez vezes o campo, igual à massa vezes a rapidez ao quadrado dividida pelo raio.",
    "Cancelando uma rapidez": "Cancelando uma rapidez e isolando: a razão entre o módulo da carga e a massa é a rapidez dividida pelo produto do campo magnético e do raio.",
    "Isolando:": S,
    "Esse é o resultado da caixa": S,
    "A rapidez continua constante": S,
    "As unidades, na tela": S,
    # B09
    "Recapitulando:": "Recapitulando: a força magnética gera círculos e hélices; cargas organizadas formam a corrente, descrita localmente pela densidade de corrente; e, com dois campos, uma carga vira o seletor e a medida da razão entre carga e massa.",
    "Sem componente paralela, a trajetória": S,
    "Com componente paralela, o círculo": S,
    "Quando há transporte organizado": S,
    "Distribuído pelo volume": S,
    "E, numa carga individual": S,
}

feitos, usados = 0, set()
for i, ln in enumerate(L):
    if not re.match(r"\|\s*\d+:\d+", ln):
        continue
    c = ln.strip()[2:-2].split(" | ")
    assert len(c) == 3
    hits = [k for k in C if c[2].startswith(k)]
    if hits:
        assert len(hits) == 1, (hits, c[2][:50])
        usados.add(hits[0])
        c[2] = C[hits[0]]
        L[i] = "| " + " | ".join(c) + " |"
        feitos += 1
print("células alteradas:", feitos, "| chaves não usadas:", [k for k in C if k not in usados])
open(dst, "w", encoding="utf-8").write("\n".join(L))
