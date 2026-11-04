"""yt_0022 — auditoria PARADO: lê o preview e acusa intervalos ≥ 3 s (ou 5 s se passado 2º arg) com diferença média de quadro (cinza, 0–255, a 1/4 da resolução) < 0,35.
uso: python parado22.py [rodada] → renders/parado.txt"""
import sys
from pathlib import Path

import av
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v1"
c = av.open(str(U / "renders" / f"preview_yt0022_{R}_960x540.mp4"))
ant, d = None, []
for fr in c.decode(video=0):
    g = fr.to_ndarray(format="gray")[::4, ::4].astype(np.int16)
    d.append(0.0 if ant is None else float(np.abs(g - ant).mean()))
    ant = g
d = np.array(d)
LIM, MIN = 0.35, int(float(sys.argv[2]) * 15) if len(sys.argv) > 2 else 3 * 15
runs, i = [], 0
while i < len(d):
    if d[i] < LIM:
        j = i
        while j < len(d) and d[j] < LIM:
            j += 1
        if j - i >= MIN:
            runs.append((i, j))
        i = j
    else:
        i += 1
lin = [f"{a / 15 // 60:.0f}:{a / 15 % 60:04.1f} → {b / 15 // 60:.0f}:{b / 15 % 60:04.1f} ({(b - a) / 15:.1f} s)" for a, b in runs]
txt = f"PARADO (diferença média < {LIM} por ≥ {MIN / 15:.0f} s): {len(runs)} intervalos\n" + "\n".join(lin) + "\n"
(U / "renders" / "parado.txt").write_text(txt, encoding="utf-8")
print(txt)
