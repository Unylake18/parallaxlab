"""yt_0014 — acha os trechos em que a imagem fica parada (quadros idênticos) por mais de LIM s num vídeo (preview ou master).
Uso: uv run --no-sync python parados.py ARQ.mp4 [LIM=0.6]
Mostra cada trecho parado (início, duração) e, se existir ritmo.json, a âncora da fala mais próxima."""
import json
import sys
from pathlib import Path

import av
import numpy as np

P = Path(__file__).resolve().parent
arq = Path(sys.argv[1])
lim = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6
c = av.open(str(arq))
s = c.streams.video[0]
s.thread_type = "AUTO"
fps = float(s.average_rate)
prev, dif = None, []
for f in c.decode(s):
    g = f.reformat(width=240, height=135, format="gray").to_ndarray().astype(np.int16)
    dif.append(0.0 if prev is None else float(np.abs(g - prev).mean()))
    prev = g
dif = np.array(dif)
par = dif <= 0.0
tr = json.loads((P / "ritmo.json").read_text(encoding="utf-8"))["trechos"] if (P / "ritmo.json").exists() else []
tot, n, i = 0.0, 0, 0
while i < len(par):
    if par[i]:
        j = i
        while j < len(par) and par[j]:
            j += 1
        d = (j - i) / fps
        if d >= lim:
            t = i / fps
            ref = next((r for r in reversed(tr) if r["alvo"] <= t + 0.05), None)
            print(f"{t:8.2f} s  parado {d:5.2f} s  após {ref['id']} {ref['frase'][:30]!r}" if ref else f"{t:8.2f} s  parado {d:5.2f} s")
            tot += d
            n += 1
        i = j
    else:
        i += 1
print(f"{n} trechos parados ≥ {lim} s, soma {tot:.1f} s de {len(dif) / fps:.1f} s ({100 * tot / (len(dif) / fps):.1f} %)")
