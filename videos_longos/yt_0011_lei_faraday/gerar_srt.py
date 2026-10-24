"""yt_0011 — legenda .srt a partir dos tempos exatos do alinhamento forçado (audio/alinhamento_forcado.json).
Cada legenda: até 2 linhas de ≤ 42 caracteres, quebrando em pontuação."""
import json
import textwrap
from pathlib import Path

P = Path(__file__).resolve().parent
cel = json.loads((P / "audio" / "alinhamento_forcado.json").read_text(encoding="utf-8"))["celulas"]
pal = [(w, a, b) for c in cel for w, a, b in c["palavras"]]


def fmt(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


blocos, cur = [], []
for w in pal:
    cur.append(w)
    txt = " ".join(x[0] for x in cur)
    fim = w[0][-1] in ".?!:" or (w[0][-1] in ",;" and len(txt) > 45) or len(txt) > 64
    if fim:
        blocos.append(cur)
        cur = []
if cur:
    blocos.append(cur)
out = []
for i, b in enumerate(blocos, 1):
    ini, fim = b[0][1], b[-1][2] + 0.25
    if i < len(blocos):
        fim = min(fim, blocos[i][0][1] - 0.02)
    linhas = textwrap.wrap(" ".join(x[0] for x in b), 42)
    out.append(f"{i}\n{fmt(ini)} --> {fmt(fim)}\n" + "\n".join(linhas))
(P / "final" / "legenda - 0011.srt").write_text("\n\n".join(out) + "\n", encoding="utf-8")
print(len(blocos), "legendas;", max(len(textwrap.wrap(" ".join(x[0] for x in b), 42)) for b in blocos), "linhas máx")
