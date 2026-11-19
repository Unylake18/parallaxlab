import sys, av
from PIL import Image
V = sys.argv[1]; out = sys.argv[2]; ts = [float(x) for x in sys.argv[3:]]
c = av.open(V); fps = float(c.streams.video[0].average_rate)
want = {int(round(t * fps)): t for t in ts}; got = {}
for k, f in enumerate(c.decode(video=0)):
    if k in want: got[want[int(k)]] = f.to_image().resize((960, 540), Image.LANCZOS)
    if k >= max(want): break
P = Image.new("RGB", (960 * len(ts), 540))
for i, t in enumerate(ts): P.paste(got[t], (960 * i, 0))
P.save(out)
