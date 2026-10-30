"""QA de palco congelado (handoff v6 §4): quadros a 5 fps, 240×135 em cinza; um pixel muda se muda > 18 níveis entre quadros seguidos;
um trecho é congelado se < 0,4 % dos pixels mudam. Lista os trechos ≥ LIM s (padrão 6) com a âncora em que começam.
uso: python congelado_v6.py video.mp4 [LIM] → log_congelado_v6.txt"""
import json
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
arq = sys.argv[1]
LIM = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
t0s = [(A["ancoras"][a]["t0"], a) for a in A["ordem"]]


def ancora(t):
    return [a for t0, a in t0s if t0 <= t + 1e-6][-1]


c = av.open(arq)
st = c.streams.video[0]
fps = float(st.average_rate)
passo = int(round(fps / 5))
ant, frac, ts = None, [], []
for i, fr in enumerate(c.decode(st)):
    if i % passo:
        continue
    g = np.asarray(fr.to_image().convert("L").resize((240, 135)), dtype=np.int16)
    if ant is not None:
        frac.append(float((np.abs(g - ant) > 18).mean()))
        ts.append(i / fps)
    ant = g
frac = np.array(frac)
cong = frac < 0.004
trechos, i = [], 0
while i < len(cong):
    if cong[i]:
        j = i
        while j + 1 < len(cong) and cong[j + 1]:
            j += 1
        d = ts[j] - ts[i] + 0.2
        if d >= 3.0:
            trechos.append((ts[i] - 0.2, d))
        i = j + 1
    else:
        i += 1
out = [f"palco congelado (< 0,4 % dos pixels mudando, quadros a 5 fps): {len(trechos)} trechos ≥ 3 s, soma {sum(d for _, d in trechos):.1f} s; "
       f"≥ {LIM:.0f} s: {sum(1 for _, d in trechos if d >= LIM)}; ≥ 8 s: {sum(1 for _, d in trechos if d >= 8)}", ""]
for t, d in sorted(trechos, key=lambda x: -x[1]):
    if d >= LIM:
        out.append(f"{int(t // 60)}:{t % 60:05.2f}  {d:5.1f} s  {ancora(t + 0.01)}")
out += ["", "todos os ≥ 3 s:"] + [f"{int(t // 60)}:{t % 60:05.2f}  {d:5.1f} s  {ancora(t + 0.01)}" for t, d in trechos]
(U / "log_congelado_v6.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out[:40]))
