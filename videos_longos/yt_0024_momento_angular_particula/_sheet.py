import sys, av
from PIL import Image, ImageDraw
# uso: python _sheet.py video.mp4 saida.png t0 t1 passo [x0 y0 x1 y1] [cols]
mp4, out = sys.argv[1], sys.argv[2]
t0, t1, dt = map(float, sys.argv[3:6])
box = tuple(int(v) for v in sys.argv[6:10]) if len(sys.argv) > 9 else (480, 80, 960, 340)
cols = int(sys.argv[10]) if len(sys.argv) > 10 else 3
c = av.open(mp4); fps = float(c.streams.video[0].average_rate)
ks = []; t = t0
while t <= t1 + 1e-6:
    ks.append((int(round(t * fps)), t)); t += dt
alvo = dict(ks); imgs = []
for k, f in enumerate(c.decode(video=0)):
    if k in alvo:
        im = f.to_image().crop(box); d = ImageDraw.Draw(im); d.text((4, 2), f"{alvo[k]:.2f}s", fill=(255, 255, 0)); imgs.append(im)
    if k > ks[-1][0]: break
w, h = imgs[0].size; rows = (len(imgs) + cols - 1) // cols
S = Image.new("RGB", (w * cols, h * rows))
for i, im in enumerate(imgs): S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(out)
