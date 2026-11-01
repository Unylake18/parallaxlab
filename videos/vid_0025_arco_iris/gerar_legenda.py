"""Legenda do vid_0025: legenda.srt a partir do alinhamento forçado (tempo exato de cada palavra) já convertido para o tempo do VÍDEO
(voz + pausas inseridas por plan_sync.py, lidas de sync.json). Até 2 linhas por bloco, sem sobreposição; nenhum bloco atravessa uma pausa.
Uso: python gerar_legenda.py [LARGURA_MAX_LINHA]    Saída: legenda.srt (texto sem tags de áudio)."""
import json
import re
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
MAXL = int(sys.argv[1]) if len(sys.argv) > 1 else 30      # caracteres por linha
pal = json.loads((PASTA / "alinhamento_palavras.json").read_text(encoding="utf-8"))
sy = json.loads((PASTA / "sync.json").read_text(encoding="utf-8"))
pads = sorted((p, d) for p, d in sy["pads"])
FIM_VIDEO = sy["end"]
FIM = (".", "?", "!", ":")

# expressões coloridas (cores_legenda.py) com mais de uma palavra não podem ser quebradas entre linhas
sys.path.insert(0, str(PASTA))
from cores_legenda import SUBTITLE_TERM_COLORS  # noqa: E402
FRASES = sorted({t for t in SUBTITLE_TERM_COLORS if " " in t and len(t) <= MAXL}, key=lambda t: -len(t.split()))
norm = lambda w: re.sub(r"[^\wáéíóúâêôãõàçü]", "", w.lower())


def vt(t):
    """tempo da voz -> tempo do vídeo (soma as pausas inseridas antes de t)"""
    return t + sum(d for p, d in pads if p < t)


W = [dict(word=w["word"], start=vt(w["start"]), end=vt(w["end"]), vstart=w["start"], vend=w["end"]) for w in pal]


def pausa_entre(a, b):
    return any(a["vend"] <= p <= b["vstart"] for p, _ in pads)


def agrupa(tokens):
    """junta as palavras que formam uma frase colorida num único token (nunca quebra no meio)"""
    saida, i = [], 0
    while i < len(tokens):
        for f in FRASES:
            n = len(f.split())
            if [norm(x) for x in tokens[i:i + n]] == [norm(x) for x in f.split()]:
                saida.append(" ".join(tokens[i:i + n]))
                i += n
                break
        else:
            saida.append(tokens[i])
            i += 1
    return saida


def quebra_linhas(tokens):
    linhas, atual = [], ""
    for t in agrupa(tokens):
        cand = (atual + " " + t).strip()
        if len(cand) <= MAXL or not atual:
            atual = cand
        else:
            linhas.append(atual)
            atual = t
    linhas.append(atual)
    return linhas


cues, cur = [], []


def fecha():
    global cur
    if cur:
        cues.append(cur)
        cur = []


for w in W:
    if cur and pausa_entre(cur[-1], w):
        fecha()
    prova = quebra_linhas([x["word"] for x in cur] + [w["word"]])
    if len(prova) > 2:
        fecha()
    cur.append(w)
    txt = " ".join(x["word"] for x in cur)
    if w["word"].endswith(FIM) or (w["word"].endswith(",") and len(txt) >= 24):
        fecha()
fecha()

# junta blocos muito curtos (< 0,7 s ou < 10 caracteres) ao vizinho quando cabe em 2 linhas e não há pausa entre eles
i = 0
while i < len(cues) - 1:
    dur = cues[i][-1]["end"] - cues[i][0]["start"]
    txt = " ".join(x["word"] for x in cues[i])
    if (dur < 0.7 or len(txt) < 10) and len(quebra_linhas([x["word"] for x in cues[i] + cues[i + 1]])) <= 2 \
            and cues[i + 1][0]["start"] - cues[i][-1]["end"] < 0.6 and not pausa_entre(cues[i][-1], cues[i + 1][0]):
        cues[i] = cues[i] + cues.pop(i + 1)
    else:
        i += 1


def ts(t):
    ms = round(t * 1000)
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


saida, prev_fim = [], 0.0
for k, c in enumerate(cues):
    ini = max(c[0]["start"], prev_fim + 0.02)
    prox = cues[k + 1][0]["start"] if k + 1 < len(cues) else FIM_VIDEO
    fim = min(c[-1]["end"] + 0.25, prox - 0.03)
    fim = max(fim, min(ini + 0.9, prox - 0.03))
    if fim <= ini:
        fim = ini + 0.2
    linhas = quebra_linhas([x["word"] for x in c])
    saida.append(f"{k + 1}\n{ts(ini)} --> {ts(fim)}\n" + "\n".join(linhas))
    prev_fim = fim
(PASTA / "legenda.srt").write_text("\n\n".join(saida) + "\n", encoding="utf-8")
print(len(cues), "blocos; maior linha", max(len(l) for c in cues for l in quebra_linhas([x["word"] for x in c])), "caracteres")
