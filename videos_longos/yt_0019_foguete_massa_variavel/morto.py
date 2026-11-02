"""yt_0019 v10: trechos mortos (handoff v10 R-M): diferença média de quadro < 0,15 em cinza 320x180, amostrando a cada 0,2 s, janelas >= 3 s.
uso: python morto.py ARQ.mp4 [saida.txt]"""
import sys
import av
import numpy as np
arq = sys.argv[1]
c = av.open(arq)
v = c.streams.video[0]
fps = float(v.average_rate)
passo = max(1, round(fps * 0.2))
prev, d = None, []
for i, fr in enumerate(c.decode(v)):
    if i % passo:
        continue
    g = np.asarray(fr.to_image().convert("L").resize((320, 180)), dtype=np.float32)
    d.append(0.0 if prev is None else float(np.abs(g - prev).mean()))
    prev = g
d = np.array(d)
runs, ini = [], None
for k, x in enumerate(d):
    if x < 0.15 and ini is None:
        ini = k
    if (x >= 0.15 or k == len(d) - 1) and ini is not None:
        fim = k if x >= 0.15 else k + 1
        if (fim - ini) * 0.2 >= 3.0:
            runs.append((ini * 0.2, (fim - ini) * 0.2))
        ini = None
out = [f"{int(t // 60)}:{t % 60:04.1f}  {dur:4.1f} s" for t, dur in runs]
txt = f"{len(runs)} trechos >= 3 s; >= 8 s: {sum(1 for _, x in runs if x >= 8)}; total parado {sum(x for _, x in runs):.0f} s\n" + "\n".join(out)
print(txt)
if len(sys.argv) > 2:
    open(sys.argv[2], "w", encoding="utf-8").write(txt)
