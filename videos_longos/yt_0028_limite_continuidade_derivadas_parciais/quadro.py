"""yt_0028: um quadro do preview de um lote no instante t (s do lote), lado a lado com um quadro-alvo (960×540 cada).
uso: python quadro.py LOTE t [NN]  → renders/still/q_LOTE_t.png"""
import sys
from pathlib import Path

import av
from PIL import Image

U = Path(__file__).resolve().parent
lote, t = sys.argv[1], float(sys.argv[2])
nn = sys.argv[3] if len(sys.argv) > 3 else None
c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
alvo_q = round(t * 15)
im = None
for i, fr in enumerate(c.decode(video=0)):
    if i == alvo_q:
        im = fr.to_image()
        break
if im is None:
    im = fr.to_image()
out = Image.new("RGB", (1920 if nn else 960, 540))
out.paste(im, (0, 0))
if nn:
    a = next((U / "referencia_v3").glob(f"{int(nn):02d}_*.jpg"))
    out.paste(Image.open(a).convert("RGB").resize((960, 540), Image.LANCZOS), (960, 0))
(U / "renders" / "still").mkdir(parents=True, exist_ok=True)
p = U / "renders" / "still" / f"q_{lote}_{t:.1f}.png"
out.save(p)
print(p)
