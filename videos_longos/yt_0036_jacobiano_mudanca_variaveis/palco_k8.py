"""yt_0036 final §7 / K8: palco vazio = METADE da tela (esquerda ou direita, abaixo do canto) sem nada além do papel por mais de 0,5 s.
Tinta: traço/texto (pixel > 70 de 255) ou preenchimento (pixel > 46 em blocos ≥ 30 % cheios); a linha da grade fica ≤ 43. O CTA fica de fora.
Saída: renders/final/qa/palco_vazio_k8_final.txt"""
import json
import re
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
R = "final"
MP4 = U / "renders" / R / f"yt_0036_preview_{R}_540p15.mp4"
ini = json.loads((U / "renders" / R / f"lotes_{R}.json").read_text())["inicio"]
m = re.search(r"\[cta\] ([\d.]+)", (U / "log_PS.txt").read_text(encoding="utf-8", errors="ignore"))
cta = ini["PS"] / 15 + float(m.group(1)) if m else 1e9
vaz = []
c = av.open(str(MP4))
for t, f_ in enumerate(c.decode(video=0)):
    f = f_.to_ndarray(format="gray").astype(np.int16)[66:, :]
    estado = []
    for h in (f[:, :480], f[:, 480:]):
        tinta = int(np.count_nonzero(h > 70))
        cheio = h > 46
        bl = cheio[: cheio.shape[0] // 30 * 30, :].reshape(-1, 30, 16, 30).sum(axis=(1, 3)) >= 270
        estado.append(tinta < 60 and not bl.any())
    vaz.append(any(estado) and t / 15 < cta)
c.close()
runs, i = [], 0
while i < len(vaz):
    if vaz[i]:
        j = i
        while j + 1 < len(vaz) and vaz[j + 1]:
            j += 1
        if (j - i + 1) / 15 > 0.5:
            runs.append((i, j))
        i = j + 1
    else:
        i += 1
txt = (f"PALCO VAZIO (K8 / §7): metade da tela (esquerda ou direita) sem nada além do papel por mais de 0,5 s (o CTA fica de fora): {len(runs)}\n"
       + "".join(f"  {a / 15:7.2f}–{b / 15:7.2f} s ({(b - a + 1) / 15:.2f} s)\n" for a, b in runs))
(U / "renders" / R / "qa" / f"palco_vazio_k8_{R}.txt").write_text(txt, encoding="utf-8")
print(txt)
