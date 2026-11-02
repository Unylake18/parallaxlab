"""Compõe PNGs do Three.js (fundo transparente) sobre o céu do laboratório em uma prancha. uso: python turntable.py saida.png a.png b.png ..."""
import sys
from PIL import Image, ImageDraw
fundo = Image.open("fundo_lab.png").convert("RGBA").resize((960, 540))
ims = []
for f in sys.argv[2:]:
    im = Image.open(f).convert("RGBA")
    b = fundo.copy(); b.alpha_composite(im); ims.append((f, b.convert("RGB")))
C = 2 if len(ims) > 1 else 1
W, H = 640, 360
L = (len(ims) + C - 1) // C
pr = Image.new("RGB", (W * C, (H + 18) * L), "black")
d = ImageDraw.Draw(pr)
for k, (f, im) in enumerate(ims):
    x, y = (k % C) * W, (k // C) * (H + 18)
    pr.paste(im.resize((W, H)), (x, y + 18)); d.text((x + 4, y + 3), f.split("/")[-1], fill="yellow")
pr.save(sys.argv[1])
