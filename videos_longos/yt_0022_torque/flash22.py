"""yt_0022 v6 — QA FLASH por vídeo: curva de "tinta" (pixels com luma > 185 na metade direita, y 70–490, em 960×540) por quadro.
Reporta subidas ≥ 60 px em ≤ 3 quadros seguidas de queda ≥ 75% em ≤ 10 quadros (elemento que aparece e some antes de ser escrito).
Cada ocorrência gera quadros em renders/chk/flash/ para conferência.
uso: python flash22.py ARQUIVO.mp4 [saida.txt]"""
import sys
from pathlib import Path

import av
import numpy as np
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

U = Path(__file__).resolve().parent
arq = Path(sys.argv[1])
saida = Path(sys.argv[2]) if len(sys.argv) > 2 else U / "renders" / "flash.txt"
c = av.open(str(arq))
s = c.streams.video[0]
s.thread_type = "AUTO"
fps = float(s.average_rate)
tinta = []
for fr in c.decode(video=0):
    g = fr.reformat(width=960, height=540, format="gray").to_ndarray()
    tinta.append(int((g[70:490, 480:] > 185).sum()))
t = np.array(tinta, float)
ev, i, n = [], 1, len(t)
sub, qd = 3, 10
MINSUB = 300      # px de tinta (um bloco de texto/fórmula tem centenas a milhares; variações < 300 são estrelas e fades de cena)
while i < n - 1:
    j = min(n - 1, i + sub)
    pico_i = i + int(np.argmax(t[i:j + 1]))
    if t[pico_i] - t[i - 1] >= MINSUB:
        base = t[i - 1]
        k = pico_i
        alt = t[pico_i] - base
        fim = None
        for q in range(pico_i + 1, min(n, pico_i + qd * int(max(1, round(fps / 15))) + 1)):
            if t[q] - base <= 0.25 * alt:
                fim = q
                break
        if fim is not None:
            ev.append((i, pico_i, fim, base, t[pico_i]))
            i = fim + 1
            continue
    i += 1
lin = [f"arquivo {arq.name}: {n} quadros a {fps:g} fps; picos de tinta que sobem em ≤ 3 quadros e voltam em ≤ 10: {len(ev)}"]
for (i0, ip, f1, b, p) in ev:
    lin.append(f"  {i0 / fps:8.2f}s  sobe {int(b)}→{int(p)} px em {ip - i0 + 1} q; volta em {f1 - ip} q  (duração visível {(f1 - i0) / fps:.2f}s)")
saida.write_text("\n".join(lin) + "\n", encoding="utf-8")
np.save(saida.with_suffix(".npy"), t)
print("\n".join(lin[:60]))
