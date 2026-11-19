"""fqs.py LOTE t1 t2 ... [--out ARQ]  → prancha dos instantes (s) em resolução cheia (2 colunas)."""
import sys, av
from pathlib import Path
from PIL import Image, ImageDraw
U = Path(__file__).resolve().parent
a = sys.argv[1:]
out = U / "renders/v6/_fq.png"
if "--out" in a:
    i = a.index("--out"); out = Path(a[i + 1]); a = a[:i] + a[i + 2:]
L, ts = a[0], [float(x) for x in a[1:]]
out.parent.mkdir(parents=True, exist_ok=True)
c = av.open(str(U / f"media_{L}/videos/cena/540p15/{L}.mp4"))
fps = float(c.streams.video[0].average_rate)
want = {int(round(t * fps)): t for t in ts}
got = {}
for i, f in enumerate(c.decode(video=0)):
    if i in want: got[want[i]] = f.to_image()
    if i > max(want): break
cols = 1 if len(ts) == 1 else 2
rows = (len(ts) + cols - 1) // cols
P = Image.new("RGB", (960 * cols, 540 * rows))
for k, t in enumerate(ts):
    if t in got:
        d = got[t].copy(); ImageDraw.Draw(d).text((6, 4), f"{L} {t:.2f}s", fill=(255, 255, 0))
        P.paste(d, ((k % cols) * 960, (k // cols) * 540))
P.save(out); print(out)
