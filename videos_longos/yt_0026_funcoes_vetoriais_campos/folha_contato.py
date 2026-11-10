"""yt_0026: folha de contato do preview completo (com B7): um quadro por âncora, tirado a 70% da âncora (a construção já em cena).
uso: python folha_contato.py [rodada] → renders/folha_contato_<rodada>.png"""
import json
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v1"
q = json.loads((U / "renders" / f"quadros_{R}_com_b7.json").read_text(encoding="utf-8"))
ordem = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ordem"]
c = av.open(str(U / "renders" / f"preview_yt0026_{R}_com_b7_960x540.mp4"))
n = c.streams.video[0].frames
ini = [q[a] for a in ordem]
alvo = {int(i0 + 0.7 * (i1 - i0)): a for a, i0, i1 in zip(ordem, ini, ini[1:] + [n])}
ims = {}
for i, fr in enumerate(c.decode(video=0)):
    if i in alvo:
        ims[alvo[i]] = (i, fr.to_image())
W, H, C = 480, 270, 4
L = (len(ordem) + C - 1) // C
pr = Image.new("RGB", (W * C, (H + 18) * L), "black")
d = ImageDraw.Draw(pr)
for k, a in enumerate(ordem):
    x, y = (k % C) * W, (k // C) * (H + 18)
    if a in ims:
        i, im = ims[a]
        pr.paste(im.resize((W, H)), (x, y + 18))
        d.text((x + 4, y + 3), f"{a}  q{i}  {i // 15 // 60}:{i / 15 % 60:04.1f}", fill="yellow")
pr.save(U / "renders" / f"folha_contato_{R}.png")
print(len(ims), "âncoras;", n, "quadros")
