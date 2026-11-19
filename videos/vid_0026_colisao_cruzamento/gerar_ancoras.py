"""Âncoras da voz do vid_0026: instante (s) em que começa cada unidade da fala, a partir de alinhamento_palavras.json.
Cada unidade abre com o passo da cena de mesmo nome (self.ancora(nome) em cena.py). Saída: voz_ancoras.json."""
import json
import re
from pathlib import Path

PASTA = Path(__file__).absolute().parent
UNIDADES = [
    ("acidente", "Dois carros batem num cruzamento. O azul vinha do oeste; o violeta, do sul. Grudados, eles ainda deslizam até parar."),
    ("depois", "Só que a gente chegou depois: sobrou só a marca no asfalto."),
    ("cotas", "Oito metros para leste, seis para norte."),
    ("pergunta", "O que uma marca no asfalto consegue contar sobre uma batida?"),
    ("volta", "Vamos voltar no tempo!"),
    ("dados", "Os dados: o carro azul tem dois mil quilos; o violeta, mil. O coeficiente de atrito é zero vírgula cinco; a gravidade, dez."),
    ("hipoteses", "Modelo idealizado, não perícia: impacto curtíssimo, atrito constante, marca reta."),
    ("fim", "E todo bom detetive começa pelo fim!"),
    ("conjunto", "Grudados, os carros viram um conjunto de três mil quilos."),
    ("forcas", "O chão empurra com a força normal, igual ao peso: massa total vezes gravidade."),
    ("atrito", "O atrito, contra o movimento, vale o coeficiente de atrito vezes a normal."),
    ("trabalho", "E nos dez metros da marca ele tira energia: o trabalho é menos o atrito vezes o comprimento da marca."),
    ("teorema", "Pelo teorema do trabalho e energia: zero, menos meio da massa total vezes a velocidade logo depois da batida ao quadrado, é igual a esse trabalho."),
    ("sinais", "Os sinais de menos cancelam."),
    ("corta", "A massa total está dos dois lados... então corta!"),
    ("meio", "O meio passa para o outro lado como dois,"),
    ("raiz", "e tirando a raiz, a velocidade é a raiz de duas vezes o coeficiente de atrito vezes a gravidade vezes o comprimento da marca."),
    ("numeros", "Com os números, a raiz de cem dá dez metros por segundo,"),
    ("direcao", "na direção da marca: oito para leste, seis para norte."),
    ("impacto", "Agora, o impacto: tão curto que o impulso externo fica desprezível."),
    ("conserva", "Aqui, o momento se conserva."),
    ("momento", "Momento é massa vezes velocidade."),
    ("total", "O total antes é igual ao total depois,"),
    ("direcoes", "e vale em cada direção: massa do carro vezes a velocidade dele, igual à massa total vezes aquela parte da velocidade final."),
    ("isolar", "Passando a massa do carro dividindo:"),
    ("azul", "três mil sobre dois mil, vezes oito... doze metros por segundo para o azul."),
    ("violeta", "Três mil sobre mil, vezes seis... dezoito para o violeta."),
    ("pegadinha", "E a pegadinha: o mesmo triângulo aparece três vezes."),
    ("tangente", "A tangente do ângulo é dezoito mil sobre vinte e quatro mil, três quartos: razão dos momentos, não das velocidades."),
    ("barras", "O violeta era mais rápido, mas o azul tinha mais momento... e foi ele que mandou na direção."),
    ("ida", "Na ida, com doze e dezoito, o conjunto para exatamente no fim da marca!"),
    ("energia", "E a energia cinética?"),
    ("kantes", "Antes, trezentos e seis quilojoules;"),
    ("kdepois", "depois, cento e cinquenta."),
    ("metade", "Pouco mais da metade virou deformação, calor, som e vibração."),
    ("frase", "Momento se conserva; energia cinética, não."),
    ("licao", "A lição: cada intervalo tem a sua lei. No impacto, momento; no deslizamento, trabalho e energia."),
    ("ponte", "E numa colisão elástica, com a energia também conservada, os momentos até limitam os ângulos possíveis... assunto para outro vídeo."),
    ("cta", "Segue o Parallax Lab. Até a próxima!"),
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
    print(f"{nome:10s} {out[nome]['ini']:7.2f} – {out[nome]['fim']:7.2f}")
