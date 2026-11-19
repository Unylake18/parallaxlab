"""yt_0020 v7 §5 · teste FLASH: picos de "tinta" que sobem em ≤ 3 quadros e caem ≥ 75% em ≤ 10 quadros (algo que aparece e some sem se desenvolver).
Tinta = nº de pixels claros (luma > 90, 480×270) fora do cabeçalho; as estrelas (≤ 3 px, opacidade ≤ 50%) ficam abaixo do limiar.
uso: python flash20.py renders/preview_....mp4  → renders/v8/flash.txt (candidatos com tempo, base, pico, final, âncora) e json."""
import json
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
arq = Path(sys.argv[1])
FPS = 15.0
c = av.open(str(arq))
s = c.streams.video[0]
s.thread_type = "AUTO"
ink = []
for f in c.decode(s):
    g = f.to_ndarray(format="gray")                         # 540×960
    g = g[::2, ::2]                                          # 270×480
    ink.append(int((g[22:] > 90).sum()))                     # sem o cabeçalho (≈ 4% superior)
ink = np.array(ink, float)
anc = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
lim = [(k, v["ini"], v["fim"]) for k, v in anc.items()]


def aid(t):
    for k, a, b in lim:
        if a <= t < b:
            return k
    return "-"


cand = []
i = 3
n = len(ink)
while i < n - 12:
    base = ink[i - 1]
    j = i + int(np.argmax(ink[i:i + 3]))
    amp = ink[j] - base
    if amp >= 350:                                           # ≈ uma palavra/um traço longo
        # cai ≥ 75% do ganho em ≤ 10 quadros depois do pico, e termina perto da base
        fim = ink[j + 1:j + 11]
        if len(fim) and fim.min() <= base + 0.25 * amp:
            k = j + 1 + int(np.argmax(fim <= base + 0.25 * amp))
            cand.append((j / FPS, base, ink[j], ink[k], (k - j) / FPS))
            i = k
            continue
    i += 1
out = [f"# yt_0020 — FLASH ({arq.name}): {len(cand)} candidatos (sobe ≥ 350 px em ≤ 3 quadros e cai ≥ 75% em ≤ 10 quadros)", "",
       "t_s    âncora   base→pico→fim (px claros)   queda_em_s"]
for t, b, p, fi, dt in cand:
    out.append(f"{t:7.2f}  {aid(t):7s}  {b:6.0f} → {p:6.0f} → {fi:6.0f}   {dt:.2f}")
(U / "renders" / "v7").mkdir(parents=True, exist_ok=True)
(U / "renders" / "v7" / "flash.txt").write_text("\n".join(out), encoding="utf-8")
np.save(U / "renders" / "v7" / "tinta.npy", ink)
print("\n".join(out[:40]))
