"""uso: python folha.py ARQ.mp4 SAIDA.png t1 t2 ... (segundos) -> prancha 3 colunas, 480x270 por quadro"""
import sys
import av
from PIL import Image, ImageDraw
arq, saida, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]]
c = av.open(arq)
v = c.streams.video[0]
fps = float(v.average_rate)
alvo = {int(round(t * fps)): t for t in ts}
got = {}
for i, fr in enumerate(c.decode(v)):
    if i in alvo:
        got[alvo[i]] = fr.to_image().resize((640, 360))
    if i >= max(alvo):
        break
cols = 3
rows = (len(ts) + cols - 1) // cols
fo = Image.new("RGB", (640 * cols, 380 * rows), "black")
d = ImageDraw.Draw(fo)
for k, t in enumerate(ts):
    x, y = (k % cols) * 640, (k // cols) * 380
    if t in got:
        fo.paste(got[t], (x, y + 20))
    d.text((x + 4, y + 4), f"{t:.1f}s", fill="white")
fo.save(saida)
