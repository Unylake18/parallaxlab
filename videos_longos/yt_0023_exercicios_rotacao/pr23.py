"""Prancha de quadros de um lote: python pr23.py LOTE [n] [t0 t1] → renders/prancha_<LOTE>.png (quadros com o tempo)."""
import sys, av
from pathlib import Path
from PIL import Image, ImageDraw
U = Path(__file__).resolve().parent
L = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 24
v = U / f"media_{L}/videos/cena/540p15/{L}.mp4"
c = av.open(str(v)); s = c.streams.video[0]; tot = s.frames
t0 = float(sys.argv[3]) * 15 if len(sys.argv) > 3 else 0; t1 = float(sys.argv[4]) * 15 if len(sys.argv) > 4 else tot - 1
alvo = sorted(set(int(t0 + (t1 - t0) * k / max(1, n - 1)) for k in range(n)))
ims = []
for i, fr in enumerate(c.decode(video=0)):
    if i in alvo:
        im = fr.to_image().resize((480, 270)); d = ImageDraw.Draw(im); d.text((6, 4), f"{i/15:.1f}s", fill=(255, 255, 0)); ims.append(im)
    if i > max(alvo): break
cols = 4; rows = (len(ims) + cols - 1) // cols
out = Image.new("RGB", (480 * cols, 270 * rows))
for k, im in enumerate(ims): out.paste(im, ((k % cols) * 480, (k // cols) * 270))
(U / "renders").mkdir(exist_ok=True); out.save(U / f"renders/prancha_{L}{'_'+sys.argv[3] if len(sys.argv)>3 else ''}.png"); print(len(ims), tot)
