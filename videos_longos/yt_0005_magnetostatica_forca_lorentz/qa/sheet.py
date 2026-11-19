"""Prancha de quadros: python sheet.py VIDEO SAIDA.png t1 t2 ... (segundos; 3 colunas)."""
import sys, av
from PIL import Image, ImageDraw

v, out = sys.argv[1], sys.argv[2]
ts = [float(x) for x in sys.argv[3:]]
fps_want = {}
c = av.open(v)
fr = float(c.streams.video[0].average_rate)
want = {int(round(t * fr)): t for t in ts}
got = {}
for i, f in enumerate(c.decode(c.streams.video[0])):
    if i in want:
        got[i] = f.to_image()
    if i > max(want):
        break
tiles = sorted(got.items())
w, h = tiles[0][1].size
cols = 3
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h))
d = ImageDraw.Draw(sheet)
for n, (k, im) in enumerate(tiles):
    x, y = (n % cols) * w, (n // cols) * h
    sheet.paste(im, (x, y))
    d.text((x + w - 70, y + h - 16), "%d:%05.2f" % (int(k / fr) // 60, (k / fr) % 60), fill=(255, 255, 0))
sheet.save(out)
print(len(tiles))
