"""Âncoras da voz do vid_0027: instante (s) em que começa cada unidade da fala, a partir de alinhamento_palavras.json.
Cada unidade abre o passo da cena de mesmo nome (self.an(nome) em cena.py). Saída: voz_ancoras.json."""
import json
import re
from pathlib import Path

PASTA = Path(__file__).absolute().parent
UNIDADES = [
    ("hook", "Todo indutor guarda energia. Mas onde ela fica?"),
    ("fio", "No fio..."),
    ("espaco", "ou no espaço aí dentro, onde só tem ar?"),
    ("palpite", "Guarda o seu palpite."),
    ("cenario", "Vamos descobrir com um solenoide longo, de núcleo de ar."),
    ("sentidos", "Em cima, a corrente sai da tela; embaixo, entra."),
    ("raio", "Ele tem raio"),
    ("espiras", "e espiras por metro,"),
    ("trecho", "e olhamos um trecho longe das pontas."),
    ("campo_q", "Primeiro: quanto vale o campo magnético aí dentro?"),
    ("ampere", "Lei de Ampère: a soma do campo ao longo de um caminho fechado é a permeabilidade do vácuo,"),
    ("mi0", "que na tela é mi zero,"),
    ("iint", "vezes a corrente total que atravessa esse caminho."),
    ("retangulo", "No retângulo,"),
    ("dentro", "só o lado de dentro conta, porque lá o campo acompanha o caminho."),
    ("verticais", "Nos lados verticais ele é perpendicular;"),
    ("fora", "fora, praticamente zero."),
    ("bl", "A soma vira campo vezes o comprimento do lado."),
    ("corrente_q", "E a corrente?"),
    ("cada_espira", "Cada espira dentro do retângulo."),
    ("comprimento", "O comprimento aparece dos dois lados..."),
    ("corta", "e corta!"),
    ("campo_res", "O campo é a permeabilidade do vácuo, vezes espiras por metro, vezes corrente."),
    ("fluxo", "Agora, o fluxo numa espira:"),
    ("soma_disco", "a soma do campo que atravessa o disco."),
    ("uniforme", "Como o campo é uniforme e entra de frente,"),
    ("sai_integral", "ele sai da integral:"),
    ("sobra_area", "sobra a área."),
    ("fluxo_ba", "Fluxo é campo vezes área."),
    ("muitas", "Só que são muitas espiras, todas com o mesmo fluxo."),
    ("concat", "O fluxo concatenado, que na tela é a letra grega lambda, é a soma de todos:"),
    ("nphi", "número de espiras vezes o fluxo de uma."),
    ("numero", "Esse número é espiras por metro vezes o comprimento."),
    ("indutancia", "A indutância é o fluxo concatenado dividido pela corrente, medida em henry."),
    ("cancela", "A corrente cancela,"),
    ("geometria", "e sobra só geometria."),
    ("repara", "Repara nas espiras por metro ao quadrado:"),
    ("fator_campo", "um fator vem do campo;"),
    ("fator_contagem", "o outro, da contagem."),
    ("energia", "Agora, a energia. Primeiro jeito: pelo circuito."),
    ("fem", "Enquanto a corrente sobe, o indutor reage com uma força eletromotriz,"),
    ("potencia", "e a fonte entrega potência para vencê-la."),
    ("du", "A cada pedacinho de tempo, a energia cresce indutância vezes corrente vezes um pedacinho de corrente."),
    ("somando", "Somando de zero até o valor final:"),
    ("meio", "meio vezes indutância vezes corrente ao quadrado."),
    ("guardada", "É a energia guardada quando a corrente chega a esse valor; ela entrou enquanto a corrente subia."),
    ("com_L", "Com a indutância do solenoide,"),
    ("topo", "essa expressão vai para o topo."),
    ("segundo", "Segundo jeito: pelo campo."),
    ("densidade", "A densidade de energia é a energia por volume,"),
    ("geral", "e tem um resultado geral: campo ao quadrado, dividido por duas vezes a permeabilidade do vácuo."),
    ("brilho", "Dentro, brilho uniforme; fora, escuro."),
    ("somando_vol", "Somando no volume:"),
    ("uv", "densidade vezes volume,"),
    ("arrastada", "que é a área do disco arrastada ao longo do trecho."),
    ("trocando", "Trocando o campo pelo que achamos"),
    ("elevando", "e elevando ao quadrado..."),
    ("cancela_mu", "uma permeabilidade do vácuo de cima cancela com a de baixo."),
    ("mesma", "Sobrou a mesma expressão lá de cima!"),
    ("conferem", "As duas contas conferem:"),
    ("dois_jeitos", "é a mesma energia, contada de dois jeitos."),
    ("pergunta", "E a pergunta do começo?"),
    ("fio_conduz", "O fio só conduz a corrente."),
    ("campo_final", "A energia está guardada no campo magnético, dentro do solenoide."),
    ("chutou", "Chutou \"no fio\"? Relaxa, é um palpite natural."),
    ("cta", "Se curtiu, siga o Parallax Lab."),
]


def norm(w):
    return re.sub(r"[^\wà-ú]", "", w.lower())


pal = json.loads((PASTA / "alinhamento_palavras.json").read_text(encoding="utf-8"))
texto = (PASTA / "texto_narracao.txt").read_text(encoding="utf-8")
assert " ".join(u[1] for u in UNIDADES).split() == texto.split(), "as unidades não reproduzem o texto da narração"
assert len(pal) == len(texto.split()), (len(pal), len(texto.split()))
out, i = {}, 0
for nome, frase in UNIDADES:
    ws = frase.split()
    assert norm(pal[i]["word"]) == norm(ws[0]), (nome, pal[i]["word"], ws[0])
    out[nome] = {"ini": pal[i]["start"], "fim": pal[i + len(ws) - 1]["end"], "texto": frase}
    i += len(ws)
out["_fim_voz"] = pal[-1]["end"]
(PASTA / "voz_ancoras.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for nome, _ in UNIDADES:
    print(f"{nome:15s} {out[nome]['ini']:7.2f} – {out[nome]['fim']:7.2f}")
