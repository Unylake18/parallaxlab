"""yt_0018 v7: uma prancha por lote (20 quadros igualmente espaçados do preview com voz) → renders/v7/prancha_<LOTE>.png. uso: python pranchas_v7.py"""
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
LOTES = {"PH": ("H1", "A4"), "PX0": ("X0-1", "X1-4"), "PX2": ("X2-1", "X2-4"), "PX3": ("X3-1", "X3-10"), "PX4": ("X4-1", "X4-5"), "PX5": ("X5-1", "X5-8"), "PEP": ("EP1", "EN2")}
c = av.open(str(U / "renders" / "preview_yt0018_v7_960x540.mp4"))
quadros = {}
alvos = {}
for l, (a0, a1) in LOTES.items():
    t0, t1 = A[a0]["ini"], A[a1]["fim"]
    alvos[l] = [t0 + (t1 - t0) * (k + 0.5) / 20 for k in range(20)]
quer = {int(round(t * 15)) for ts in alvos.values() for t in ts}
for i, fr in enumerate(c.decode(video=0)):
    if i in quer:
        quadros[i] = fr.to_image()
    if i > max(quer):
        break
for l, ts in alvos.items():
    W, H = 480, 270
    pr = Image.new("RGB", (4 * W, 5 * (H + 16)), "black")
    d = ImageDraw.Draw(pr)
    for k, t in enumerate(ts):
        x, y = (k % 4) * W, (k // 4) * (H + 16)
        pr.paste(quadros[int(round(t * 15))].resize((W, H)), (x, y + 16))
        d.text((x + 4, y + 2), f"{l} {int(t // 60)}:{t % 60:05.2f}", fill="yellow")
    pr.save(U / "renders" / "v7" / f"prancha_{l}.png")
print("ok")
