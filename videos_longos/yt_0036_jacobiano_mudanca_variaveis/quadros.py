"""yt_0036 · quadros de um lote em instantes dados (960×540, resolução cheia do preview), 2 por linha. uso: python quadros.py LOTE t1 t2 ... [--saida nome]"""
import sys
from pathlib import Path
import av
from PIL import Image, ImageDraw, ImageFont
U = Path(__file__).resolve().parent
a = sys.argv[1:]
saida = a[a.index("--saida") + 1] if "--saida" in a else None
a = [x for i, x in enumerate(a) if x != "--saida" and (i == 0 or a[i - 1] != "--saida")]
lote, ts = a[0], [float(x) for x in a[1:]]
mp4 = U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"
c = av.open(str(mp4))
fr = {}
alvo = {round(t * 15): t for t in ts}
for i, f in enumerate(c.decode(video=0)):
    if i in alvo:
        fr[i] = f.to_image()
    if i > max(alvo):
        break
F = ImageFont.truetype(str(U.parents[1] / "assets/fonts/space_grotesk/SpaceGrotesk-Bold.ttf"), 22)
n = len(ts)
img = Image.new("RGB", (1930, ((n + 1) // 2) * 574), (12, 10, 30))
d = ImageDraw.Draw(img)
for k, i in enumerate(sorted(fr)):
    x, y = (k % 2) * 970, (k // 2) * 574
    d.text((x + 6, y + 2), f"{lote} t = {alvo[i]:.2f} s", font=F, fill=(240, 240, 255))
    img.paste(fr[i], (x, y + 32))
out = U / "renders/v1/qa" / (saida or f"q_{lote}.jpg")
img.save(out, quality=90)
print(out)
