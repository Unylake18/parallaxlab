"""fq.py LOTE t1 t2 ... [-o saida.png] : monta uma prancha com os quadros (cheios) nos tempos dados."""
import sys, av, numpy as np
from PIL import Image
a = sys.argv[1:]
out = "renders/v5/q.png"
if "-o" in a:
    i = a.index("-o"); out = a[i+1]; a = a[:i] + a[i+2:]
L = a[0]; ts = [float(x) for x in a[1:]]
c = av.open(f"media_{L}/videos/cena/540p15/{L}.mp4"); fps = float(c.streams.video[0].average_rate)
want = {int(round(t*fps)): t for t in ts}
got = {}
for k, f in enumerate(c.decode(video=0)):
    if k in want: got[k] = f.to_ndarray(format="rgb24")
    if k > max(want): break
ims = [got[k] for k in sorted(got) if k in got]
cols = 2 if len(ims) > 1 else 1
rows = (len(ims)+cols-1)//cols
H, W = ims[0].shape[:2]
P = Image.new("RGB", (W*cols, H*rows))
for i, im in enumerate(ims): P.paste(Image.fromarray(im), ((i % cols)*W, (i//cols)*H))
import os; os.makedirs(os.path.dirname(out), exist_ok=True)
P.save(out); print(out, len(ims))
