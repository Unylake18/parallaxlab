"""Prancha de quadros: python prancha.py video.mp4 saida.png t1 t2 ... (segundos). Sem ffmpeg: usa o PyAV da .venv."""
import sys
import av
from PIL import Image, ImageDraw

v, saida, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]]
c = av.open(v)
s = c.streams.video[0]
fps = float(s.average_rate)
alvo = sorted(round(t * fps) for t in ts)
imgs, i = [], 0
for fr in c.decode(video=0):
    if i in alvo:
        imgs.append((i / fps, fr.to_image()))
    i += 1
    if i > alvo[-1]:
        break
w, h = imgs[0][1].size
cols = 3
rows = (len(imgs) + cols - 1) // cols
sh = Image.new("RGB", (cols * w, rows * h))
for k, (t, im) in enumerate(imgs):
    d = ImageDraw.Draw(im)
    d.text((6, h - 16), f"{t:.1f}s", fill=(255, 255, 0))
    sh.paste(im, ((k % cols) * w, (k // cols) * h))
sh.save(saida)
print(saida, len(imgs), "quadros")
