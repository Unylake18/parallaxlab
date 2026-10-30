"""Mede trechos parados num vídeo: quadros consecutivos quase idênticos (reduzidos a 240×135 em cinza; um quadro é "parado" quando
menos de 10 pixels mudam mais de 6 níveis em relação ao anterior). Lista todo trecho ≥ LIM s (padrão 6).
uso: python parados.py video.mp4 [LIM] [capitulos.txt]"""
import sys

import av
import numpy as np

arq = sys.argv[1]
LIM = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
c = av.open(arq)
st = c.streams.video[0]
fps = float(st.average_rate)
ant, run0, runs, n = None, None, [], 0
for i, fr in enumerate(c.decode(st)):
    g = np.asarray(fr.to_image().convert("L").resize((240, 135)), dtype=np.int16)
    if ant is not None:
        parado = int((np.abs(g - ant) > 6).sum()) < 10
        if parado and run0 is None:
            run0 = i - 1
        elif not parado and run0 is not None:
            runs.append((run0 / fps, (i - 1) / fps))
            run0 = None
    ant = g
    n = i
if run0 is not None:
    runs.append((run0 / fps, n / fps))
mm = lambda t: f"{int(t // 60)}:{t % 60:04.1f}"
longos = [(a, b) for a, b in runs if b - a >= LIM]
print(f"duração {n / fps:.1f} s · trechos parados ≥ {LIM:g} s: {len(longos)} (soma {sum(b - a for a, b in longos):.1f} s)")
for a, b in longos:
    print(f"  {mm(a)}–{mm(b)}  ({b - a:.1f} s)")
q4 = [(a, b) for a, b in runs if 4.0 <= b - a < LIM]
print(f"trechos entre 4 e {LIM:g} s: {len(q4)}")
