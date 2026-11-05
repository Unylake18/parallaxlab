"""Extrai quadros de um lote numa prancha: python _quadros.py LOTE t1 t2 ... → renders/_q_LOTE.png"""
import sys
from pathlib import Path
import av
from PIL import Image, ImageDraw
U = Path(__file__).resolve().parent
L, ts = sys.argv[1], [float(x) for x in sys.argv[2:]]
c = av.open(str(U / f"media_{L}/videos/cena/540p15/{L}.mp4"))
alvo = sorted(round(t * 15) for t in ts)
out, f = [], 0
for fr in c.decode(video=0):
    if f in alvo:
        im = fr.to_image()
        ImageDraw.Draw(im).text((8, 520), f"{L} {f/15:.1f}s", fill=(255, 255, 0))
        out.append(im)
    f += 1
cols = 2
W, H = 960, 540
pr = Image.new("RGB", (W * cols, H * ((len(out) + cols - 1) // cols)))
for i, im in enumerate(out):
    pr.paste(im, ((i % cols) * W, (i // cols) * H))
pr.save(U / "renders" / f"_q_{L}.png")
