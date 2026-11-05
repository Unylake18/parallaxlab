"""Compõe PNGs 3D (com transparência) sobre o fundo do laboratório e junta numa grade: python _comp3d.py saida.png a.png b.png ..."""
import sys
from pathlib import Path
from PIL import Image

U = Path(__file__).resolve().parent
saida, arqs = sys.argv[1], sys.argv[2:]
fundo = Image.open(U / "fundo_lab.png").convert("RGBA").resize((960, 540))
ims = []
for a in arqs:
    im = Image.open(a).convert("RGBA")
    f = fundo.copy()
    f.alpha_composite(im)
    ims.append(f.convert("RGB"))
cols = 2 if len(ims) > 1 else 1
lin = (len(ims) + cols - 1) // cols
pr = Image.new("RGB", (960 * cols, 540 * lin))
for i, im in enumerate(ims):
    pr.paste(im, ((i % cols) * 960, (i // cols) * 540))
pr.save(saida)
print(saida)
