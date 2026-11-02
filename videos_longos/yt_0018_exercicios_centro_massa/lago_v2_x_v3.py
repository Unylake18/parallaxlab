"""v3 §5: 3 quadros do hook + 3 do X3, v2 × v3 lado a lado, no mesmo ponto da fala (âncora + fração; âncoras do v2 nos logs da auditoria do
v2). uso: python lago_v2_x_v3.py → renders/v3/lago_v2_x_v3.png"""
import json
import re
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
INI2 = {"PH": 0.0, "PX3": 316.6}
ini3 = json.loads((U / "renders" / "v3" / "inicio_lotes.json").read_text(encoding="utf-8"))
EST = [("PH", "H1", 0.75, "H1 close"), ("PH", "H2", 0.3, "H2 salto"), ("PH", "H2", 0.8, "H2 replay de lado"),
       ("PX3", "X3-1", 0.85, "X3-1 dados"), ("PX3", "X3-5", 0.55, "X3-5 voo (câmera recuada)"), ("PX3", "X3-7", 0.3, "X3-7 rasante")]


def anc(f):
    a = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", f.read_text(encoding="utf-8", errors="replace"))]
    return {x: (t, a[i + 1][1] if i + 1 < len(a) else t + 10) for i, (x, t) in enumerate(a)}


def q(arq, qs):
    c = av.open(str(arq))
    out = {}
    for i, f in enumerate(c.decode(video=0)):
        if i in qs:
            out[i] = f.to_image()
        if i > max(qs):
            break
    return out


par = []
for l, aid, fr, nome in EST:
    s2, e2 = anc(U / f"log_aud_{l}__teste_v2.txt")[aid]
    s3, e3 = anc(U / f"log_{l}.txt")[aid]
    par.append((int(round((INI2[l] + s2 + fr * (e2 - s2)) * 15)), int(round((ini3[l] + s3 + fr * (e3 - s3)) * 15)), nome))
a = q(U / "renders" / "preview_yt0018_v2_960x540.mp4", {p[0] for p in par})
b = q(U / "renders" / "preview_yt0018_v3_960x540.mp4", {p[1] for p in par})
W, H = 640, 360
pr = Image.new("RGB", (2 * W + 10, len(par) * (H + 22)), "black")
d = ImageDraw.Draw(pr)
for k, (q2, q3, nome) in enumerate(par):
    y = k * (H + 22)
    pr.paste(a[q2].resize((W, H)), (0, y + 22))
    pr.paste(b[q3].resize((W, H)), (W + 10, y + 22))
    d.text((4, y + 5), f"v2 · {nome}", fill="yellow")
    d.text((W + 14, y + 5), f"v3 · {nome}", fill="yellow")
pr.save(U / "renders" / "v3" / "lago_v2_x_v3.png")
print("ok")
