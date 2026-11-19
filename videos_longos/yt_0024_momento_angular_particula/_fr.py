import sys, av
from PIL import Image
# uso: python _fr.py video.mp4 saida_prefixo t1 t2 ...  (segundos)
mp4, pre = sys.argv[1], sys.argv[2]
ts = [float(x) for x in sys.argv[3:]]
c = av.open(mp4); fps = float(c.streams.video[0].average_rate)
alvo = {int(round(t*fps)): t for t in ts}
for k, f in enumerate(c.decode(video=0)):
    if k in alvo:
        f.to_image().save(f"{pre}_{alvo[k]:g}.png")
