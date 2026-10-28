"""python medir_parado.py video.mp4 [limite_s] → trechos em que a imagem fica parada (sem mudança visível entre quadros).
Quadro "parado": diferença máxima < 10/255 em 99,95% dos pixels (480×270, cinza) em relação ao quadro anterior. Lista os trechos
parados mais longos que o limite (padrão 4 s) e o total acima de 6 s (QA do handoff v4 §3.3)."""
import sys

import av
import numpy as np

vid = sys.argv[1]
lim = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
c = av.open(vid)
fps = float(c.streams.video[0].average_rate)
ant, parado, i = None, [], 0
for fr in c.decode(video=0):
    g = np.asarray(fr.to_image().convert("L").resize((480, 270)), dtype=np.int16)
    if ant is not None:
        d = np.abs(g - ant)
        parado.append(np.mean(d > 10) < 0.0005)
    ant = g
    i += 1
runs, ini = [], None
for k, p in enumerate(parado + [False]):
    if p and ini is None:
        ini = k
    if not p and ini is not None:
        runs.append(((ini + 1) / fps, (k + 1) / fps))
        ini = None
longos = [(a, b) for a, b in runs if b - a > lim]
for a, b in longos:
    print(f"[parado] {a:7.1f}–{b:7.1f} s ({b - a:4.1f} s)" + ("  > 6 s" if b - a > 6 else ""))
print(f"[parado] {len(longos)} trechos > {lim:g} s; {sum(1 for a, b in runs if b - a > 6)} trechos > 6 s; duração {i / fps:.1f} s")
