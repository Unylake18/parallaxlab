"""uso: python frames.py video.mp4 saida_prefixo t1 t2 ... -> PNGs; e prancha: se prefixo termina com .png, junta os quadros numa grade 2 colunas."""
import sys, av
from PIL import Image
v, out, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3:]]
c = av.open(v); s = c.streams.video[0]
ims = []
for t in ts:
    c.seek(int(t / s.time_base), stream=s)
    for f in c.decode(s):
        if f.time >= t - 0.001:
            ims.append(f.to_image()); break
W, H = ims[0].size
cols = 2
rows = (len(ims) + 1) // 2
P = Image.new('RGB', (W * cols, H * rows))
for k, im in enumerate(ims):
    P.paste(im, ((k % cols) * W, (k // cols) * H))
P.save(out)
