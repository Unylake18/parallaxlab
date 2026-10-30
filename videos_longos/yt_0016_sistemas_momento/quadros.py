"""Prancha rápida de quadros de um lote (conferência visual): python quadros.py LOTE saida.png t1 t2 ... (segundos do lote)."""
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
L, saida, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]]
c = av.open(str(U / f"media_{L}/videos/cena/540p15/{L}.mp4"))
alvo = {int(round(t * 15)): t for t in ts}
imgs = {}
for i, fr in enumerate(c.decode(video=0)):
    if i in alvo:
        imgs[i] = fr.to_image()
    if i > max(alvo):
        break
cols = 2 if len(ts) > 1 else 1
rows = (len(ts) + cols - 1) // cols
W, H = 960, 540
P = Image.new("RGB", (cols * W, rows * (H + 24)), (20, 20, 20))
d = ImageDraw.Draw(P)
for k, i in enumerate(sorted(imgs)):
    x, y = (k % cols) * W, (k // cols) * (H + 24)
    P.paste(imgs[i], (x, y + 24))
    d.text((x + 8, y + 5), f"{L} t={alvo[i]:.1f}s", fill=(255, 255, 0))
P.save(saida)
