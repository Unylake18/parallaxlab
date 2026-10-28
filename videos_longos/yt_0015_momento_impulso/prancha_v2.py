"""python prancha_v2.py video.mp4 saida.png t1 t2 ... → prancha 3 colunas com os quadros nos instantes (s), com o tempo no canto."""
import sys

import av
from PIL import Image, ImageDraw

vid, saida, ts = sys.argv[1], sys.argv[2], sorted(float(x) for x in sys.argv[3:])
c = av.open(vid)
ims, i = [], 0
for fr in c.decode(video=0):
    t = float(fr.pts * fr.time_base)
    while i < len(ts) and t >= ts[i] - 1e-6:
        im = fr.to_image()
        ImageDraw.Draw(im).text((6, im.height - 16), f"{ts[i]:.1f}s", fill=(255, 230, 0))
        ims.append(im)
        i += 1
    if i >= len(ts):
        break
w, h = ims[0].size
sh = Image.new("RGB", (3 * w, ((len(ims) + 2) // 3) * h))
for k, im in enumerate(ims):
    sh.paste(im, ((k % 3) * w, (k // 3) * h))
sh.save(saida)
