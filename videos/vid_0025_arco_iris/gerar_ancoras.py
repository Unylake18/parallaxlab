"""Âncoras do vid_0025: nome -> instante real (s) da voz, a partir de alinhamento_palavras.json.
Cada âncora marca o início de uma frase/cláusula falada que dispara um evento visual. Ordem crescente obrigatória.
Saída: ancoras.json  {"A": {nome: t}, "order": [...], "audio_end": s, "fim": s}"""
import json
import re
import wave
from pathlib import Path

PASTA = Path(__file__).resolve().parent
PAL = json.loads((PASTA / "alinhamento_palavras.json").read_text(encoding="utf-8"))
norm = lambda s: re.sub(r"[^\wáéíóúâêôãõàçü]", "", s.lower())
W = [norm(p["word"]) for p in PAL]


def acha(frase, apos=0):
    seq = [norm(x) for x in frase.split()]
    for i in range(apos, len(W) - len(seq) + 1):
        if W[i:i + len(seq)] == seq:
            return i
    raise KeyError(frase)


# nome: frase falada (início)
F = [
    # C01 — hook: arco preso a um ângulo, "de quê?", direção antissolar
    ("h1", "o arco-íris não aparece"), ("h1b", "em qualquer lugar do céu"),
    ("h2", "ele fica preso"), ("h2b", "cerca de quarenta e dois graus"),
    ("h3", "mas quarenta e dois graus"), ("h3b", "de quê"),
    ("h4", "com o sol nas costas"), ("h4b", "trace uma linha"), ("h4c", "até a sombra dela"),
    ("h5", "essa é a direção antissolar"), ("h5b", "e é dela que medimos o arco"),
    # C02 — a gota
    ("c02", "tudo começa numa gota esférica"), ("c02b", "atingida por raios de luz paralelos"),
    # C03 — entrada e Snell
    ("c03", "ao entrar na água"), ("c03b", "é a refração"), ("c03c", "pela lei de snell"),
    ("c03d", "o seno do ângulo de incidência"), ("c03e", "é o índice de refração da água"),
    ("c03f", "vezes o seno do ângulo de refração"),
    # C04 — reflexão e saída
    ("c04", "depois o raio reflete no fundo"), ("c04b", "como dois lados do triângulo"),
    ("c04c", "o ângulo ali volta a ser o de refração"), ("c04d", "na saída volta ao ângulo de incidência"),
    # C05 — as três viradas
    ("c05", "agora somamos as três viradas"), ("c05a", "na entrada e na saída"), ("c05b", "na reflexão"),
    ("c05c", "o desvio total é"), ("c05d", "medindo da direção antissolar"), ("c05e", "o ângulo do arco é quatro vezes"),
    # C06 — família de raios e o gráfico
    ("c06", "só que há raios entrando"), ("c06b", "o do centro volta pelo mesmo caminho"),
    ("c06c", "subindo a altura"), ("c06d", "cresce menos"), ("c06e", "chega a um máximo"), ("c06f", "e cai"),
    # C07 — o amontoado
    ("c07", "e esse máximo é o segredo"), ("c07b", "perto dele raios que entram"), ("c07c", "eles se amontoam"),
    ("c07d", "no modelo geométrico"), ("c07e", "cerca de um em cada cinco"), ("c07f", "a menos de um grau do máximo"),
    ("c07g", "e nenhum passa dele"),
    # C08 — quanto vale o máximo
    ("c08", "quanto vale esse máximo"), ("c08b", "no topo da curva a inclinação é zero"),
    ("c08c", "uma pequena mudança na incidência"), ("c08d", "derivando snell"), ("c08e", "chegamos a três vezes"),
    ("c08f", "igual ao índice"), ("c08g", "para a água"), ("c08h", "incidência de cinquenta e nove graus"),
    ("c08i", "refração de quarenta"), ("c08j", "e o máximo aparece em quarenta e dois graus"),
    # C09 — as cores
    ("c09", "e as cores"), ("c09b", "o índice muda um pouco com a cor"), ("c09c", "vermelho"), ("c09d", "violeta"),
    ("c09e", "por isso vermelho por fora"),
    # C10 — cone, círculo, semicírculo, Sol
    ("c10", "todas as direções a quarenta e dois graus"), ("c10b", "formam um cone"),
    ("c10c", "e sua borda aparece como um círculo"), ("c10d", "em torno do ponto antissolar"),
    ("c10e", "o horizonte esconde"), ("c10f", "com o sol no horizonte"),
    ("c10g", "se o sol sobe acima de quarenta e dois graus"), ("c10h", "o círculo fica abaixo do horizonte"),
    # C11 — fechamento
    ("c11", "resumindo"), ("c11b", "o arco-íris aparece onde"), ("c11c", "a cerca de quarenta e dois graus"),
    ("c11d", "siga o parallax lab"),
]

out, pos = [], 0
for nome, frase in F:
    k = acha(frase, pos)
    out.append((nome, round(PAL[k]["start"], 3)))
    pos = k + 1
assert all(b[1] > a[1] for a, b in zip(out, out[1:])), [(a, b) for a, b in zip(out, out[1:]) if b[1] <= a[1]]
with wave.open(str(PASTA / "audio" / "narracao_v5.wav")) as w:
    audio_end = w.getnframes() / w.getframerate()
fim = round(audio_end + 1.2, 3)       # cartão final segura ~1,2 s depois da voz
A = dict(out)
A["fim"] = fim
(PASTA / "ancoras.json").write_text(json.dumps(dict(A=A, order=[n for n, _ in out] + ["fim"], audio_end=round(audio_end, 3),
                                                     fim_fala=PAL[-1]["end"]), indent=1), encoding="utf-8")
print(len(A), "âncoras; fala termina", PAL[-1]["end"], "áudio", round(audio_end, 3), "fim do vídeo (voz)", fim)
