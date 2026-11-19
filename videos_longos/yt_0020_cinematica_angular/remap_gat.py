# yt_0020 v6: remapeia gat("frase v1.1") -> gat("frase da fala v1.2") (mesma âncora). Valida que a nova existe consecutiva na fala da âncora.
import glob
import json
import re

M = {
    "E1-1": {"desligado ele para em trinta segundos": "desliga ele para em trinta segundos"},
    "E3-2": {"vamos marcar também a direção de uma estrela": "vamos marcar também uma estrela muito distante",
             "depois de uma volta completa em relação às estrelas": "quando completa uma volta em relação às estrelas",
             "só que nesse tempo a terra também andou": "ao mesmo tempo avança um pouco em sua órbita",
             "então o sol ainda não voltou ao meridiano": "mas o sol ainda não voltou ao meridiano",
             "quase um grau": "um pouquinho mais",
             "o dia de vinte e quatro horas é o dia solar médio": "o dia solar médio dura vinte e quatro horas",
             "a volta de verdade em relação às estrelas": "uma volta em relação às estrelas o dia sideral"},
    "E3-3": {"conta as voltas num ano inteiro": "contando voltas durante um ano",
             "em relação às estrelas uma volta a mais": "em relação às estrelas a terra completa uma volta a mais",
             "porque a órbita inteira acrescenta um giro": "essa volta extra aparece",
             "dividindo tudo pelo tempo de um ano": "dividindo pelo tempo de um ano",
             "dá oitenta e seis mil": "dá aproximadamente oitenta e seis mil",
             "sete vírgula duzentos": "sete vírgula dois nove dois"},
    "E3-6": {"e a aceleração centrípeta de são paulo": "e são paulo também tem aceleração centrípeta",
             "uns três centésimos": "zero vírgula zero três um",
             "para o eixo da terra não para o centro": "para o eixo de rotação não exatamente para o centro",
             "um ângulo igual à latitude": "um ângulo igual ao módulo da latitude",
             "conferindo no polo": "nos polos a distância ao eixo é zero",
             "e ficam duas dicas": "guarda duas perguntas para qualquer problema"},
    "H1": {"só que não tem": "só que não anda"},
    "T1-2": {"na tela ele aparece como teta": "o ângulo entre essa linha pintada no disco"},
    "T1-3": {"a gente mede em radianos": "a gente usa o radiano", "esse número é o ângulo em radianos": "é o ângulo da fatia em radianos"},
    "T1-4": {"é por isso que toda a rotação": "por isso em rotação é sempre radiano"},
    "T1-5": {"o ângulo que a gente usa não volta a zero": "o ângulo não precisa voltar a zero", "se o disco deu três voltas": "três voltas no mesmo sentido",
             "o ângulo acumulado diz quanto": "já o deslocamento angular acompanha o giro com sinal"},
    "T2-1": {"a ideia é a mesma da velocidade": "é a mesma ideia do velocímetro"},
    "T2-5": {"quando o giro é uniforme": "quando o disco gira sempre no mesmo ritmo", "a frequência que é o número de voltas": "a frequência que diz quantas voltas",
             "o tamanho da velocidade angular é dois pi": "o módulo da velocidade angular é dois pi", "repara nas duas ressalvas": "duas observações",
             "é o tamanho porque a frequência": "a frequência é positiva mesmo quando o giro é horário", "e só vale com giro uniforme": "e aqui estamos falando de giro uniforme",
             "e não existe um período só": "cada volta pode levar um tempo diferente"},
    "T3-4": {"olha a área embaixo dessa reta": "olha o gráfico da velocidade angular", "que é uma tirinha fina de área": "uma tirinha de área",
             "somando todas as tirinhas": "somamos todas as tirinhas", "o retângulo é a velocidade angular inicial vezes o tempo": "o retângulo representa o giro",
             "e o triângulo": "o triângulo representa a contribuição da aceleração", "vale meio vezes a aceleração angular": "metade da aceleração angular vezes o tempo ao quadrado",
             "é o giro a mais que a aceleração deu": "somando temos o deslocamento angular", "só um cuidado": "mas cuidado", "se o disco inverter o sentido": "se o disco der uma volta num sentido",
             "a parte abaixo do eixo conta negativo": "abaixo negativo", "tem deslocamento angular zero": "deslocamento angular será zero",
             "mas girou quatro pi radianos no total": "terá girado quatro pi radianos no total"},
    "T3-6": {"e não é coincidência": "não é coincidência"},
    "T4-2": {"tem uma velocidade angular só": "tem a mesma velocidade angular", "uns duzentos e oitenta e três": "cerca de duzentos e oitenta e três",
             "mas cada ponto multiplica": "a velocidade de cada ponto depende", "uns cem quilômetros": "perto de cem quilômetros por hora",
             "ele gira junto": "ele completa cada volta junto com a ponta", "e essa rapidez na ponta": "e tem um detalhe importante",
             "ela é medida em relação ao eixo": "essas são velocidades em relação ao eixo", "perto da velocidade do som": "se aproxima da velocidade do som"},
    "T4-6": {"cada ponto tem duas acelerações": "um ponto do disco pode ter duas acelerações", "a tangencial que muda o tamanho": "a tangencial muda o tamanho da velocidade",
             "e a centrípeta que muda": "a centrípeta muda sua direção", "a aceleração total é a soma": "o tamanho da aceleração total", "o tamanho vem do pitágoras": "vem de pitágoras",
             "e o ângulo dela medido a partir": "se medirmos o ângulo a partir", "tem tangente igual": "sua tangente é o módulo",
             "para a frente se o giro acelera": "para qual lado a resultante se inclina", "repara também que a centrípeta cresce": "e olha a consequência",
             "com o quadrado da velocidade angular": "do quadrado da velocidade angular", "na ponta da hélice": "na ponta daquela hélice",
             "dá uns setenta": "aproximadamente setenta e seis mil", "perto de sete mil e setecentas": "mais de sete mil e setecentas"},
    "T5-4": {"com o produto dos dois ângulos": "depende do produto dos dois ângulos", "se os dois giros caem pela metade": "se os dois caem pela metade",
             "a diferença cai para um quarto": "aproximadamente quatro vezes menor", "para giros infinitesimais": "de giros infinitesimais",
             "e os giros pequenininhos se somam": "os pequenos giros podem ser somados como vetores"},
    "T5-5": {"com tamanho igual ao tamanho": "com tamanho igual ao módulo"},
    "T5-6": {"ganha uma fórmula completa": "ganha uma descrição completa", "dá um terceiro": "dá a velocidade do ponto", "com tamanho igual à área desse paralelogramo": "olha o paralelogramo",
             "vezes o seno do ângulo entre eles": "vezes o seno do ângulo entre os dois", "é exatamente a distância do ponto ao eixo": "é justamente a distância perpendicular ao eixo",
             "por isso o vetor posição pode começar em qualquer ponto do eixo": "qualquer ponto desse eixo como origem", "o tamanho volta a ser": "recuperamos a relação que já conhecemos",
             "tangente ao círculo do ponto": "tangente à trajetória circular"},
    "T5-8": {"a aceleração angular também vira vetor": "e a aceleração angular também pode ser um vetor", "com eixo fixo ela fica em cima do eixo": "com o eixo fixo ela aponta ao longo desse eixo",
             "quando o giro acelera": "o giro acelera", "no sentido oposto quando freia": "no sentido oposto o giro desacelera",
             "e agora dá para juntar tudo numa linha": "agora deriva a expressão vetorial da velocidade de um ponto", "derivando a velocidade do ponto": "aparecem dois termos",
             "o primeiro é a aceleração angular": "o primeiro combina a aceleração angular", "o segundo é a velocidade angular": "o segundo combina a velocidade angular",
             "com a velocidade do próprio ponto": "com a velocidade do ponto", "ele aponta para o eixo": "esse aponta para o eixo",
             "e tem tamanho velocidade angular": "e tem módulo igual ao quadrado da velocidade angular",
             "as duas acelerações do disco estavam escondidas": "aquelas duas acelerações que desenhamos no disco", "e quando o próprio eixo muda de direção": "se a própria direção do eixo começar a mudar"},
}
anc = json.load(open("ancoras.json", encoding="utf-8"))["ancoras"]
tok = lambda s: re.findall(r"\w+", s.lower())
ruim = []
for aid, d in M.items():
    ft = tok(anc[aid]["fala"])
    for old, new in d.items():
        ps = tok(new)
        if not any(ft[i:i + len(ps)] == ps for i in range(len(ft) - len(ps) + 1)):
            ruim.append((aid, new))
print("não achadas na fala:", ruim)
n = 0
for f in glob.glob("sec_*.py"):
    s = open(f, encoding="utf-8").read()
    o = s
    for aid, d in M.items():
        for old, new in d.items():
            s = s.replace(f'gat("{old}")', f'gat("{new}")')
    if s != o:
        open(f, "w", encoding="utf-8").write(s)
        n += 1
print("arquivos alterados:", n)
