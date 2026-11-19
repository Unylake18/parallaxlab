"""yt_0021 — auditoria COLUNA VAZIA: no preview, a região da coluna da direita (x > 0,6 u, abaixo do canto) sem nenhum objeto claro por mais de 5 s.
uso: python coluna21.py [rodada] → renders/coluna.txt"""
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v7"
c = av.open(str(U / "renders" / f"preview_yt0021_{R}_960x540.mp4"))
X0, Y0, Y1 = int((0.6 + 8) / 16 * 960), 85, 520
vaz, fps = [], 15
for i, fr in enumerate(c.decode(video=0)):
    if i % 3:
        continue
    g = fr.to_ndarray(format="gray")[Y0:Y1, X0:945].astype(np.int16)
    vaz.append(int((g > 105).sum()) < 150)            # estrelas e poeira ficam abaixo disso
runs, i = [], 0
dt = 3 / fps
while i < len(vaz):
    if vaz[i]:
        j = i
        while j < len(vaz) and vaz[j]:
            j += 1
        if (j - i) * dt >= 5.0:
            runs.append((i * dt, j * dt))
        i = j
    else:
        i += 1
lin = [f"{a // 60:.0f}:{a % 60:04.1f} → {b // 60:.0f}:{b % 60:04.1f} ({b - a:.1f} s)" for a, b in runs]
(U / "renders" / "coluna.txt").write_text(f"COLUNA VAZIA (x > 0,6 u sem objeto claro por ≥ 5 s): {len(runs)} intervalos\n" + "\n".join(lin) + "\n", encoding="utf-8")
print(len(runs), "intervalos")
