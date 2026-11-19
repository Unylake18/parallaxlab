import re, glob
R = {
'H1': {'tira do meio dele': 'arrancado do meio', 'ficou uma meia arruela': 'Sobrou uma meia arruela', 'a pergunta é': 'Será que cai', 'abaixo de um': 'menos de um', 'a borda de fora pesar mais': 'a borda de fora fosse mais pesada'},
'E1-1': {'fatia em pé': 'em pé', 'a integral de dentro em ípsilon': 'A integral de dentro', 'que não se escreve': 'isso não existe', 'trava fatia deitada': 'Trava', 'ípsilon menos xis ao quadrado e': 'enxerga'},
'E1-2': {'a primeira linha é um': 'A primeira linha na tela', 'a segunda linha é dois': 'A segunda é a das derivadas de y', 'um vezes um menos': 'Agora o determinante', 'com xis parado ípsilon só perde': 'com x parado', 'cada fatia em pé só escorrega': 'cada carta escorrega', 'e a área não muda': 'a área não', 'a região é um trapézio': 'virou um trapézio'},
'E1-3': {'vezes o módulo do jacobiano': 'entra o módulo do jacobiano', 'cancela o vê de baixo': 'cancela o v que estava embaixo', 'sobra é elevado a vê': 'Sobra só é elevado a v', 'de um a dois é ao quadrado': 'aplica de um a dois', 'a resposta é': 'Dá mais ou menos'},
'E1-4': {'e como conferir': 'Mas será que está certo', 'a área de bê u vê': 'No plano u v a região', 'base média vezes altura': 'média das bases vezes a altura', 'comprimento dois menos xis': 'o comprimento é dois menos x', 'a primeira xis de zero': 'A primeira é fácil', 'em dois quatro menos dois': 'a gente aplica os limites'},
'E2-1': {'calcule a área dela': 'Calcule a área', 'mas olha as bordas': 'olha as bordas de novo'},
'E2-2': {'as bordas viram': 'Olha como as bordas', 'passo dois multiplicando': 'Passo dois', 'então vai o atalho': 'Vai o atalho', 'o determinante ípsilon vezes': 'A matriz está na tela', 'que é dois vê': 'dá dois v', 'agora ir e voltar': 'ir e voltar'},
'E2-3': {'o quadrado de um a dois': 'virou um quadrado', 'dois menos um um': 'comprimento do quadrado', 'sobra um sobre dois': 'Fica só um sobre dois v', 'a de fora um meio': 'A de fora é um meio', 'a vertical mede um': 'uma mede um', 'e a horizontal raiz': 'a outra um sobre raiz de dois'},
'E2-4': {'é u então': 'é o nosso u', 'a de dentro um sobre': 'A de dentro é em u', 'quatro meios menos um': 'subtração de frações', 'três meios vezes um': 'sobram três meios', 'a de fora três quartos': 'A de fora é três quartos', 'a densidade média é': 'a densidade média', 'sobre um meio de': 'dividida pela área'},
'E3-1': {'ípsilon ao quadrado mais xis': 'Elevando ao quadrado'},
'E3-2': {'em polares xis ao quadrado': 'x ao quadrado mais y ao quadrado é r ao quadrado', 'então o integrando vira': 'e o integrando fica', 'então erre dê erre': 'então r d r é menos', 'a de fora multiplica': 'A de fora só multiplica'},
'E4-1': {'substituindo á ao quadrado': 'joga na desigualdade', 'o á ao quadrado cancela': 'embaixo cancelam', 'o bê ao quadrado cancela': 'b ao quadrado com b', 'o determinante de á': 'Olha a matriz na tela', 'seno ao quadrado á bê erre': 'põe a b r em evidência', 'duas vezes á bê vezes erre': 'faz a metade de cima', 'vezes um meio vezes pi': 'A integral de r d r dá um meio'},
'E4-2': {'pela simetria em torno': 'Aproveita a simetria', 'o módulo do jacobiano é á': 'a b r ou seja', 'a massa a integral': 'A massa é a integral', 'a primeira menos cosseno': 'A de téta é a integral do seno', 'a segunda erre ao cubo': 'A de r é r ao quadrado', 'a massa é cá sobre quatro': 'Junta tudo com o k sobre quatro'},
'E4-3': {'ípsilon vezes rô ípsilon': 'a integral de y vezes rô', 'um oitavo fica': 'os números viram um oitavo', 'para o seno ao quadrado': 'seno ao quadrado a gente não integra', 'a primitiva é téta': 'Integra termo a termo', 'em pi pi sobre dois': 'Aplica de zero a pi', 'dá pi sobre dois': 'sobra pi sobre dois', 'a de erre erre à quarta': 'A de r ao cubo', 'o momento é cá sobre oito': 'Junta o momento', 'sobre sessenta e quatro e ípsilon': 'k pi sobre sessenta e quatro', 'ípsilon barra é momento sobre massa': 'é momento sobre massa'},
'E4-4': {'a de dentro cá vezes': 'A de dentro é k vezes', 'cá vezes um meio vezes': 'o quadrado da raiz', 'a de fora cá sobre oito': 'A de fora integra'},
'E5-1': {'o erre é o jacobiano': 'aquele r é o jacobiano', 'a de fora três meios': 'A de fora é só multiplicar', 'a diferença três pi': 'a diferença é três pi sobre dois'},
'E5-2': {'a de dentro seno de téta': 'A de dentro integra', 'a de fora sete terços': 'A de fora é a integral do seno', 'menos cosseno de pi é um': 'menos cosseno de zero a pi', 'mais cosseno de zero um': 'aquele dois de sempre', 'ípsilon barra é momento sobre área': 'é momento sobre área'},
'E5-4': {'a massa é a integral': 'Resolve a massa de dentro para fora', 'a de dentro cá vezes': 'integra em r ao cubo', 'no momento entram três': 'Agora o momento', 'a de dentro cá seno': 'A de dentro é r à quarta', 'quinze quartos a de fora': 'quinze quartos', 'ípsilon barra é quinze': 'Dividindo momento por massa', 'o cá cancela quarenta': 'o k cancela'},
'E6-1': {'o caminho que o centroide': 'o caminho do centroide'},
'E6-2': {'testa no meio disco': 'Vamos testar com o meio disco', 'pappus diz dois pi': 'Pappus diz o volume', 'oito pi á ao cubo sobre seis': 'que dá quatro terços', 'o volume da bola': 'É a bola'},
'E6-3': {'usa pappus ao contrário': 'Pappus ao contrário', 'a área é três pi sobre dois': 'A área a gente já tem', 'dividido por três pi ao': 'Vamos dividir'},
'E6-4': {'e a mesma conta vale': 'a mesma conta', 'fatora as duas diferenças': 'fatora essas duas diferenças', 'bê ao quadrado menos á ao quadrado é': 'diferença de quadrados', 'o meio disco com': 'é o meio disco', 'a chapa vira um arame': 'A chapa afina até virar um arame'},
'E6-5': {'o centroide do disco é o próprio': 'o centro do disco é o centroide'},
}
n = 0
for f in sorted(glob.glob('sec_*.py')):
    src = open(f, encoding='utf-8').read().split('\n')
    cur = None
    ch = False
    for i, l in enumerate(src):
        m = re.search(r'\.an\("([^"]+)"', l)
        if m:
            cur = m.group(1)
        m = re.search(r'\.gat\(\s*"([^"]*)"', l)
        if m and cur in R and m.group(1) in R[cur]:
            src[i] = l.replace('"' + m.group(1) + '"', '"' + R[cur][m.group(1)] + '"', 1)
            n += 1
            ch = True
    if ch:
        open(f, 'w', encoding='utf-8').write('\n'.join(src))
print('trocados', n)
