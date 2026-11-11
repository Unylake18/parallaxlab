"""yt_0026 v9: [parado] trechos com a tela congelada (nenhum pixel muda acima do limiar) por mais de LIM s, por âncora.
uso: python qa_parado.py VIDEO.mp4 QUADROS.json [LIM=2.0]   (QUADROS = quadro de início de cada âncora, do montar_preview.py)"""
import json
import sys

import av
import numpy as np

vid, qj = sys.argv[1], sys.argv[2]
LIM = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
ini = sorted(json.load(open(qj, encoding="utf-8")).items(), key=lambda kv: kv[1])
c = av.open(vid)
fps = float(c.streams.video[0].average_rate)
ant, run0, runs, i = None, 0, [], 0
for fr in c.decode(video=0):
    a = fr.to_ndarray(format="gray").astype(np.int16)
    if ant is not None and (np.abs(a - ant) > 12).sum() >= 4:          # algo mudou: >= 4 pixels com diferença > 12 (acima do ruído do codec)
        if (i - run0) / fps > LIM:
            runs.append((run0, i))
        run0 = i
    ant, i = a, i + 1
if (i - run0) / fps > LIM:
    runs.append((run0, i))
aid = lambda q: [k for k, v in ini if v <= q][-1]
for a, b in runs:
    print(f"[parado] {aid(a)} {a / fps:7.2f}s–{b / fps:7.2f}s ({(b - a) / fps:.1f} s)")
print(f"[parado] total: {len(runs)} trechos > {LIM} s")
