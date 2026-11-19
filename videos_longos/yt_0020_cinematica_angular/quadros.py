"""quadros.py ARQ.mp4 saida.png t1 t2 ...  → prancha 2 colunas (960×540 cada, reduzida a 640×360) com os quadros nos tempos globais dados"""
import sys
import av
from PIL import Image, ImageDraw
arq, out, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]]
c = av.open(arq); s = c.streams.video[0]
ims = []
for t in ts:
    c.seek(int(t / s.time_base), stream=s)
    for f in c.decode(s):
        if float(f.pts * s.time_base) >= t - 1e-6:
            im = f.to_image().resize((640, 360)); ImageDraw.Draw(im).text((6, 340), f"t={t:.2f}", fill=(255, 255, 0)); ims.append(im); break
n = len(ims); cols = 2; rows = (n + 1) // 2
W = Image.new("RGB", (640 * cols, 360 * rows))
for i, im in enumerate(ims):
    W.paste(im, ((i % cols) * 640, (i // cols) * 360))
W.save(out)
