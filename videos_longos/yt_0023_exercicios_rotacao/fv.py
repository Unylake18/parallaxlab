"""fv.py VIDEO t1 t2 ... -o saida.png : prancha 1-2 colunas com quadros cheios do vídeo nos tempos (s)."""
import sys, av
from PIL import Image
a = sys.argv[1:]; out = "renders/v9/q.png"
if "-o" in a:
    i = a.index("-o"); out = a[i+1]; a = a[:i] + a[i+2:]
V = a[0]; ts = [float(x) for x in a[1:]]
c = av.open(V); fps = float(c.streams.video[0].average_rate)
want = {int(round(t*fps)): t for t in ts}; got = {}
for k, f in enumerate(c.decode(video=0)):
    if k in want: got[k] = f.to_image()
    if k >= max(want): break
ims = [got[k] for k in sorted(got)]
W, H = ims[0].size; cols = 2 if len(ims) > 1 else 1; rows = (len(ims)+cols-1)//cols
P = Image.new("RGB", (W*cols, H*rows))
for i, im in enumerate(ims): P.paste(im, ((i % cols)*W, (i//cols)*H))
import os; os.makedirs(os.path.dirname(out), exist_ok=True); P.save(out); print(out, P.size)
