"""Decodifica o master inteiro (integridade) e salva o quadro de cada âncora (T + 0,6 s) em qa/final_frames/NNN.jpg."""
import json, sys
from pathlib import Path
import av
P = Path(__file__).resolve().parent.parent
log = json.load(open(P / "ancoras_log.json"))
sj = json.load(open(P / "sync.json"))["celulas"]
want = {}
for l in log:
    if str(l[0]).isdigit():
        want[int(round((l[1] + 0.6) * 30))] = int(l[0])
out = P / "qa" / "final_frames"; out.mkdir(exist_ok=True)
c = av.open(sys.argv[1]); n = 0
for i, f in enumerate(c.decode(c.streams.video[0])):
    n += 1
    if i in want:
        f.to_image().resize((960, 540)).save(out / ("%03d.jpg" % want[i]), quality=88)
print("quadros decodificados:", n, "| salvos:", len(list(out.glob('*.jpg'))))
