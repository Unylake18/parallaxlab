"""Folha de contato: uv run python contato.py VIDEO SAIDA.png [passo_s] [t0] [t1] [colunas]"""
import sys
import av
from PIL import Image, ImageDraw

src, out = sys.argv[1], sys.argv[2]
step = float(sys.argv[3]) if len(sys.argv) > 3 else 4
t0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0
t1 = float(sys.argv[5]) if len(sys.argv) > 5 else 1e9
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 3
c = av.open(src)
s = c.streams.video[0]
fps = float(s.average_rate)
want = t0
imgs = []
for fr in c.decode(s):
    t = float(fr.pts * s.time_base)
    if t > t1:
        break
    if t >= want:
        im = fr.to_image()
        ImageDraw.Draw(im).text((8, 520), f"{t:6.1f}s", fill=(255, 255, 0))
        imgs.append(im)
        want += step
w, h = imgs[0].size
rows = (len(imgs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w, rows * h))
for i, im in enumerate(imgs):
    sheet.paste(im, ((i % cols) * w, (i // cols) * h))
sheet.save(out)
print(len(imgs), "quadros", sheet.size)
