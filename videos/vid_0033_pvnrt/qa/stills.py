"""Prancha: 3D (frames3d_540x960) + camada Manim (media_preview/stills/N.png) para os quadros pedidos. Uso: stills.py q1,q2,... [saida.png]"""
import sys
from pathlib import Path
from PIL import Image
U = Path(__file__).resolve().parents[1]
qs = [int(x) for x in sys.argv[1].split(',')]
ims = []
for q in qs:
    bg = Image.open(U / 'frames3d_540x960' / f'f{q:05d}.png').convert('RGBA')
    fg = Image.open(U / 'media_preview' / 'stills' / f'{q}.png').convert('RGBA')
    if fg.size != bg.size:
        fg = fg.resize(bg.size)
    ims.append(Image.alpha_composite(bg, fg).convert('RGB'))
c = Image.new('RGB', (540 * len(ims), 960))
for i, im in enumerate(ims):
    c.paste(im, (540 * i, 0))
c.save(sys.argv[2] if len(sys.argv) > 2 else U / 'qa' / 'prancha.png')
