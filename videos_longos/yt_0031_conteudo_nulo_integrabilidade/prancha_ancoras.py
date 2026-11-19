"""yt_0031 final §7: um quadro de cada âncora no instante da primeira palavra dela (tempo do WAV = tempo do vídeo), do preview com voz.
uso: python prancha_ancoras.py [rodada]  → renders/<rodada>/ancoras_primeira_palavra.jpg"""
import json
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "final"
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
alvo = {aid: A["ancoras"][aid]["ini"] + A["ancoras"][aid]["t"][0] for aid in A["ordem"]}
fq = {round(t * 15): aid for aid, t in alvo.items()}
c = av.open(str(U / "renders" / R / f"yt_0031_preview_{R}_540p15.mp4"))
im = {}
for k, fr in enumerate(c.decode(video=0)):
    if k in fq:
        im[fq[k]] = fr.to_image()
    if len(im) == len(fq):
        break
try:
    F = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
except OSError:
    F = ImageFont.load_default()
W, H, COLS = 480, 270, 4
rows = (len(A["ordem"]) + COLS - 1) // COLS
P = Image.new("RGB", (COLS * (W + 12) + 12, rows * (H + 40) + 12), (22, 18, 34))
d = ImageDraw.Draw(P)
for i, aid in enumerate(A["ordem"]):
    x, y = 12 + (i % COLS) * (W + 12), 12 + (i // COLS) * (H + 40)
    fala = " ".join(A["ancoras"][aid]["fala"].split()[:5])
    d.text((x, y + 4), f"{aid} · {alvo[aid]:7.2f} s · «{fala}…»", font=F, fill=(255, 196, 92))
    P.paste(im[aid].resize((W, H)), (x, y + 32))
P.save(U / "renders" / R / "ancoras_primeira_palavra.jpg", quality=88)
print("ok", len(im), "quadros", P.size)
