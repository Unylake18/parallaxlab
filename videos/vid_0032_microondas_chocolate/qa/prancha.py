"""Prancha de QA: junta PNGs (lado a lado, com o rótulo de cada um). Uso: uv run python qa/prancha.py saida.png a.png b.png ..."""
import sys
from PIL import Image, ImageDraw

BG = (5, 8, 22)
out, fs = sys.argv[1], sys.argv[2:]
ims = []
for f in fs:
    im = Image.open(f).convert('RGBA')
    fundo = Image.new('RGBA', im.size, BG + (255,))
    ims.append(Image.alpha_composite(fundo, im).convert('RGB').resize((270, 480)))
cols = min(6, len(ims))
rows = (len(ims) + cols - 1) // cols
P = Image.new('RGB', (cols * 274, rows * 500), (30, 30, 30))
d = ImageDraw.Draw(P)
for i, (im, f) in enumerate(zip(ims, fs)):
    x, y = (i % cols) * 274, (i // cols) * 500
    P.paste(im, (x, y))
    d.text((x + 4, y + 484), f.replace(chr(92), '/').split('/')[-1], fill=(220, 220, 220))
P.save(out)
