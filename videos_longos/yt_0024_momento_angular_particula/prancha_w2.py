"""prancha_w2.py LOTE ANC+seg ... → renders/_w2_<LOTE>.png (2 colunas, 960×540 por quadro). Ex.: python prancha_w2.py PB1 B1-1+6 B1-3+10 40.5"""
import re, sys
from pathlib import Path
import av
from PIL import Image, ImageDraw
U = Path(__file__).resolve().parent
L = sys.argv[1]
s = (U / f"log_{L}.txt").read_text(encoding="utf-8", errors="replace")
an = {m.group(1): float(m.group(2)) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", s)}
fr = [f.to_image() for f in av.open(str(U / f"media_{L}/videos/cena/540p15/{L}.mp4")).decode(video=0)]
ts = []
for a in sys.argv[2:]:
    if "+" in a:
        k, d = a.split("+")
        ts.append(an[k] + float(d))
    else:
        ts.append(float(a))
W = Image.new("RGB", (1920, 540 * ((len(ts) + 1) // 2)))
for k, t in enumerate(ts):
    im = fr[min(len(fr) - 1, int(t * 15))].copy()
    ImageDraw.Draw(im).text((8, 520), f"{L} t={t:.1f}", fill=(255, 230, 0))
    W.paste(im, ((k % 2) * 960, (k // 2) * 540))
W.save(U / "renders" / f"_w2_{L}.png")
print(len(fr), an)
