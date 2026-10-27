"""yt_0013 — confere no master se cada evento visual começa no instante da âncora (alvo = palavra − 0,15 s).
Para cada âncora: o primeiro quadro, a partir de alvo − 0,3 s, em que a imagem muda; desvio = início − alvo.
Âncoras em que a tela já estava em movimento antes do alvo ficam como 'em movimento' (sem início detectável)."""
import json
from pathlib import Path

import av
import numpy as np

P = Path(__file__).resolve().parent
CACHE = P / "final" / "_dif.npy"
if CACHE.exists() and CACHE.stat().st_mtime > (P / "final" / "master - 0013.mp4").stat().st_mtime:
    dif = np.load(CACHE)
else:
    c = av.open(str(P / "final" / "master - 0013.mp4"))
    s = c.streams.video[0]
    s.thread_type = "AUTO"
    prev, dif = None, []
    for f in c.decode(s):
        g = f.reformat(width=240, height=135, format="gray").to_ndarray().astype(np.int16)
        dif.append(0.0 if prev is None else float(np.abs(g - prev).mean()))
        prev = g
    dif = np.array(dif)
    np.save(CACHE, dif)
tr = json.loads((P / "ritmo.json").read_text(encoding="utf-8"))["trechos"]
LIM = 0.0                      # quadro parado decodifica idêntico (diferença exatamente 0)
res = []
for r in tr[:-1]:
    a = r["alvo"]
    k0 = int(round(a * 30))
    antes = dif[max(0, k0 - 9):k0 - 1]               # 0,3 s antes do alvo
    if len(antes) and antes.max() > LIM:
        res.append((r, None))
        continue
    janela = np.nonzero(dif[k0 - 1:k0 + 30] > LIM)[0]
    res.append((r, (k0 - 1 + janela[0]) / 30 - a if len(janela) else float("inf")))
med = [d for _, d in res if d is not None and d != float("inf")]
ruins = [(r, d) for r, d in res if d is not None and abs(d) > 0.2]
print(f"{len(res)} âncoras · início detectável em {len(med)} · em movimento antes: {sum(d is None for _, d in res)}")
print(f"desvio (início − alvo): mediana {np.median(med):+.3f} s · máx {max(med):+.3f} s · mín {min(med):+.3f} s")
print(f"fora de ±0,2 s: {len(ruins)}")
for r, d in ruins:
    print(f"  {r['id']:7s} {r['frase'][:36]:36s} alvo {r['alvo']:7.2f}  desvio {d:+.2f}")
