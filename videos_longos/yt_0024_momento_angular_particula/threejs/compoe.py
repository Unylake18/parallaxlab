"""Compõe PNG(s) do 3D (com alfa) sobre o fundo_lab.png: python compoe.py saida.png a.png [b.png ...] (lado a lado em grade de 2)."""
import sys
from pathlib import Path
from PIL import Image
U = Path(__file__).resolve().parents[1]
saida, ents = sys.argv[1], sys.argv[2:]
ims = []
for e in ents:
    a = Image.open(e).convert("RGBA")
    f = Image.open(U / "fundo_lab.png").convert("RGBA").resize(a.size)
    ims.append(Image.alpha_composite(f, a).convert("RGB"))
w, h = ims[0].size
col = 1 if len(ims) == 1 else 2
lin = (len(ims) + col - 1) // col
P = Image.new("RGB", (w * col, h * lin))
for k, im in enumerate(ims):
    P.paste(im, ((k % col) * w, (k // col) * h))
P.save(saida)
