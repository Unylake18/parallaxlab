"""yt_0019 v7 — varredura de amarelo (a aceleração agora é verde): conta pixels com matiz 44–62°, S > 0,55, V > 0,75 a cada 10º quadro.
uso: python qa_amarelo.py [renders/preview_yt0019_v7_960x540.mp4] → renders/amarelo.txt"""
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
STEP = int(sys.argv[2]) if len(sys.argv) > 2 else 10
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else U / "renders" / "preview_yt0019_v7_960x540.mp4"
c = av.open(str(SRC))
ach = []
for i, fr in enumerate(c.decode(c.streams.video[0])):
    if i % STEP:
        continue
    x = np.asarray(fr.to_image().resize((480, 270)), dtype=np.float32) / 255.0
    mx, mn = x.max(2), x.min(2)
    d = mx - mn
    r, g, b = x[..., 0], x[..., 1], x[..., 2]
    h = np.where(mx == r, ((g - b) / np.maximum(d, 1e-6)) % 6, np.where(mx == g, (b - r) / np.maximum(d, 1e-6) + 2, (r - g) / np.maximum(d, 1e-6) + 4)) * 60.0
    m = (h >= 44) & (h <= 62) & (d / np.maximum(mx, 1e-6) > 0.55) & (mx > 0.75)
    ach.append((i / 15.0, int(m.sum())))
ruins = [(t, n) for t, n in ach if n > 12]
L = [f"# amarelo (matiz 44–62°) — {len(ach)} quadros amostrados; com mais de 12 pixels: {len(ruins)}"]
for t, n in sorted(ruins, key=lambda z: -z[1])[:400]:
    L.append(f"- {int(t // 60)}:{t % 60:04.1f} — {n} px")
(U / "renders" / "amarelo.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
