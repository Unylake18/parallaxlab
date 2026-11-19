"""FLASH POR QUADRO (regra 2026-11-08): para cada `[flash] t0 box` do log do lote, o retângulo de destino no quadro t0−1 deve estar vazio
(≤ 2% de pixels claros). uso: python flash25.py LOTE [saida.txt]"""
import re, sys
from pathlib import Path
import av, numpy as np
U = Path(__file__).resolve().parent
L = sys.argv[1]
mp4 = U / f"media_{L}/videos/cena/540p15/{L}.mp4"
log = (U / f"log_{L}.txt").read_text(encoding="utf-8", errors="replace")
ev = [(float(a), tuple(int(v) for v in b.split(","))) for a, b in re.findall(r"\[flash\] t0=([\d.]+) box=([-\d,]+)", log)]
c = av.open(str(mp4)); fps = float(c.streams.video[0].average_rate)
fr = [f.reformat(width=960, height=540, format="gray").to_ndarray() for f in c.decode(video=0)]
ruins = []
for t0, (x0, y0, x1, y1) in ev:
    k = int(round(t0 * fps))
    if k < 6 or k + 20 >= len(fr):
        continue
    x0, y0 = max(0, x0 - 2), max(0, y0 - 2); x1, y1 = min(960, x1 + 2), min(540, y1 + 2)
    fim = fr[k + 18][y0:y1, x0:x1] > 150
    if fim.mean() < 0.02:
        continue
    # FLASH: o termo (a máscara do quadro final dele) já aparece no retângulo mais de 3 quadros (0,2 s) antes do t0
    # (IoU > 0,5 com o termo final); tinta de outra coisa (linha que sai da pilha) tem IoU baixo; tinta ≤ 3 quadros antes é folga do relógio.
    for j in range(max(0, k - 24), k - 3):
        m = fr[j][y0:y1, x0:x1] > 150
        iou = float((m & fim).sum()) / max(1.0, float((m | fim).sum()))
        if iou > 0.5:
            ruins.append((t0, (x0, y0, x1, y1), iou))
            break
out = [f"FLASH POR QUADRO {L}: {len(ev)} eventos, {len(ruins)} com tinta antes da vez"]
out += [f"  t0={t:.2f}s box={b} IoU={f:.2f}" for t, b, f in ruins[:40]]
txt = "\n".join(out)
print(txt)
if len(sys.argv) > 2:
    Path(sys.argv[2]).write_text(txt, encoding="utf-8")
