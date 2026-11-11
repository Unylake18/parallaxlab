"""yt_0026: legenda.srt (pt-BR) a partir do alinhamento forçado da voz real (alinhamento_palavras.json; sem as tags [ ]).
Blocos de até 2 linhas × 42 caracteres, 2 a 5 s, quebra preferida em fim de frase e depois em vírgula. Tempo do WAV = tempo do vídeo (a voz começa no quadro 0).
uso: python gerar_srt.py  → legenda.srt e o resumo (blocos, faixa de duração, maior linha)."""
import json
import re
from pathlib import Path

U = Path(__file__).resolve().parent
W = json.loads((U / "alinhamento_palavras.json").read_text(encoding="utf-8"))
L, MAXC, DMIN, DMAX = 42, 84, 2.0, 5.0
# "Cálculo três" é falado; na legenda vira "Cálculo III"
for a, b in zip(W, W[1:]):
    if a["word"] == "Cálculo" and re.fullmatch(r"três\W*", b["word"]):
        b["word"] = "III" + b["word"][4:]


def duas_linhas(t):
    if len(t) <= L:
        return [t]
    p = t.split()
    melhor = None
    for i in range(1, len(p)):
        a, b = " ".join(p[:i]), " ".join(p[i:])
        if len(a) <= L and len(b) <= L:
            c = abs(len(a) - len(b)) - (6 if a[-1] in ",.:;?!…" else 0)
            if melhor is None or c < melhor[0]:
                melhor = (c, [a, b])
    return melhor[1] if melhor else None


blocos, cur = [], []
for i, w in enumerate(W):
    if cur:
        txt = " ".join(x["word"] for x in cur + [w])
        dur = w["end"] - cur[0]["start"]
        ultimo = cur[-1]["word"]
        d0 = cur[-1]["end"] - cur[0]["start"]
        fecha = (len(txt) > MAXC or duas_linhas(txt) is None or dur > DMAX
                 or (ultimo[-1] in ".?!…" and d0 >= DMIN)
                 or (ultimo[-1] in ",:;" and d0 >= DMIN and len(" ".join(x["word"] for x in cur)) > 45))
        if fecha:
            blocos.append(cur)
            cur = []
    cur.append(w)
blocos.append(cur)

srt, durs, maior = [], [], 0
for k, b in enumerate(blocos):
    ini = b[0]["start"]
    prox = blocos[k + 1][0]["start"] if k + 1 < len(blocos) else max(b[-1]["end"] + 1.0, ini + DMIN + 0.1)
    fim = min(prox - 0.04, max(b[-1]["end"] + 0.25, ini + DMIN))
    linhas = duas_linhas(" ".join(x["word"] for x in b))
    maior = max(maior, *map(len, linhas))
    durs.append(fim - ini)
    ts = lambda s: (lambda m: f"{m // 3600000:02d}:{m // 60000 % 60:02d}:{m // 1000 % 60:02d},{m % 1000:03d}")(int(round(s * 1000)))
    srt.append(f"{k + 1}\n{ts(ini)} --> {ts(fim)}\n" + "\n".join(linhas) + "\n")
(U / "legenda.srt").write_text("\n".join(srt), encoding="utf-8")
fora = [i + 1 for i, d in enumerate(durs) if d < DMIN - 0.01 or d > DMAX + 0.3]
print(f"{len(blocos)} blocos; duração {min(durs):.2f}–{max(durs):.2f} s; maior linha {maior}; fora de 2–5 s: {fora}")
