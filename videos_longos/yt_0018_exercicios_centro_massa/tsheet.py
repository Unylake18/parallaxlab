"""Prancha de quadros do preview nos tempos pedidos (s). uso: python tsheet.py VIDEO saida.png t1 t2 ... [--cols N] [--w 640]"""
import sys
import av
from PIL import Image, ImageDraw

a = sys.argv[1:]
cols, W = 3, 640
if "--cols" in a:
    i = a.index("--cols"); cols = int(a[i + 1]); del a[i:i + 2]
if "--w" in a:
    i = a.index("--w"); W = int(a[i + 1]); del a[i:i + 2]
video, saida, ts = a[0], a[1], [float(x) for x in a[2:]]
H = W * 9 // 16
c = av.open(video)
fps = float(c.streams.video[0].average_rate)
alvo = {int(round(t * fps)): t for t in ts}
ims = {}
for i, fr in enumerate(c.decode(video=0)):
    if i in alvo:
        ims[i] = fr.to_image()
    if i > max(alvo):
        break
L = (len(alvo) + cols - 1) // cols
pr = Image.new("RGB", (W * cols, (H + 18) * L), "black")
d = ImageDraw.Draw(pr)
for k, q in enumerate(sorted(alvo)):
    x, y = (k % cols) * W, (k // cols) * (H + 18)
    if q in ims:
        pr.paste(ims[q].resize((W, H)), (x, y + 18))
    d.text((x + 4, y + 3), f"{int(alvo[q] // 60)}:{alvo[q] % 60:05.2f}  q{q}", fill="yellow")
pr.save(saida)
print(len(ims), "quadros ->", saida)
