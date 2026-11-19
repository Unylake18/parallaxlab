"""yt_0030 · handoff final §6: prancha com um quadro de cada âncora no instante da 1ª palavra (69 quadros) → qa/prancha_ancoras.jpg.
Quadros tirados do vídeo emendado (preview 540p com voz), em resolução cheia (960×540), em 6 colunas, com o id e a 1ª frase.
uso: python prancha_ancoras.py VIDEO.mp4 [fps]"""
import json
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
V = Path(sys.argv[1])
FPS = int(sys.argv[2]) if len(sys.argv) > 2 else 15
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
alvo = {round((A["ancoras"][a]["ini"] + A["ancoras"][a]["t"][0]) * FPS): a for a in A["ordem"]}
ims = {}
c = av.open(str(V))
for i, fr in enumerate(c.decode(video=0)):
    if i in alvo:
        ims[alvo[i]] = fr.to_image()
    if len(ims) == len(alvo):
        break
c.close()
try:
    FT = ImageFont.truetype("arial.ttf", 18)
except OSError:
    FT = ImageFont.load_default()
w, h = ims[A["ordem"][0]].size
COL = 6
lin = (len(A["ordem"]) + COL - 1) // COL
pr = Image.new("RGB", (COL * w, lin * (h + 28)), (5, 11, 24))
d = ImageDraw.Draw(pr)
for k, a in enumerate(A["ordem"]):
    x, y = k % COL * w, k // COL * (h + 28)
    pr.paste(ims[a], (x, y + 28))
    t = A["ancoras"][a]["ini"] + A["ancoras"][a]["t"][0]
    d.text((x + 6, y + 4), f"{a} · {int(t) // 60}:{t % 60:04.1f} · «{' '.join(A['ancoras'][a]['fala'].split()[:7])}…»", fill=(255, 220, 90), font=FT)
(U / "qa").mkdir(exist_ok=True)
pr.save(U / "qa" / "prancha_ancoras.jpg", quality=90)
print(U / "qa" / "prancha_ancoras.jpg", pr.size, len(ims), "quadros")
