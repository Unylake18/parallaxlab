"""yt_0028 (copiado do yt_0027; equivale ao qa_parado.py do handoff): [holds] trechos do preview sem evento visual por mais de 1,5 s (handoff v1 §5.6). Um quadro conta como "parado" quando menos de
40 pixels (de 960×540, em cinza) mudam mais de 6 níveis em relação ao quadro de 0,2 s antes (3 quadros: pega movimento lento). Lista cada trecho com a âncora em que começa.
uso: python qa_holds.py v1 → renders/<rodada>/qa/holds.txt"""
import json
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v1"
LIM = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0          # handoff v2 §2.1.7: parado no máximo 3 s
q = json.loads((U / "renders" / R / f"quadros_{R}.json").read_text(encoding="utf-8"))
ini = sorted((v, k) for k, v in q.items())
c = av.open(str(U / "renders" / R / f"yt_0028_preview_{R}_540p15.mp4"))
hist, parado = [], []
for fr in c.decode(video=0):
    g = np.asarray(fr.to_image().convert("L"), np.int16)
    parado.append(len(hist) >= 3 and int((np.abs(g - hist[-3]) > 6).sum()) < 40)
    hist = (hist + [g])[-3:]
runs, i = [], 0
while i < len(parado):
    if parado[i]:
        j = i
        while j < len(parado) and parado[j]:
            j += 1
        if (j - i) / 15 > LIM:
            anc = [k for v, k in ini if v <= i][-1]
            runs.append((i, j, anc))
        i = j
    else:
        i += 1
out = [f"[holds] {len(runs)} trechos > {LIM:.1f} s sem evento visual em {len(parado) / 15 / 60:.2f} min (limiar: < 40 px mudando > 6 níveis)"]
out += [f"  {a // 15 // 60}:{a / 15 % 60:04.1f}–{b // 15 // 60}:{b / 15 % 60:04.1f}  {(b - a) / 15:4.1f} s  âncora {k}" for a, b, k in runs]
d = U / "renders" / R / "qa"
d.mkdir(parents=True, exist_ok=True)
(d / f"holds_{R}.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
