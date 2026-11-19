"""yt_0031 final: extrai quadros de um lote (s do lote) em resolução cheia e monta uma prancha.
uso: python quadros.py SAIDA.jpg LOTE:t LOTE:t ... [--res 540p15|1080p30] [--cols 3]"""
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
res = sys.argv[sys.argv.index("--res") + 1] if "--res" in sys.argv else "540p15"
cols = int(sys.argv[sys.argv.index("--cols") + 1]) if "--cols" in sys.argv else 3
args = [a for a in args if a not in (res, str(cols))]
saida, pedidos = args[0], args[1:]
fps = 30 if res.startswith("1080") else 15
pref = "media1080_" if res.startswith("1080") else "media_"
ims = []
for p in pedidos:
    lote, t = p.split(":")
    t = float(t)
    with av.open(str(U / f"{pref}{lote}/videos/cena/{res}/{lote}.mp4")) as c:
        alvo = round(t * fps)
        for k, fr in enumerate(c.decode(video=0)):
            if k == alvo:
                im = fr.to_image()
                break
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 200, 22], fill=(0, 0, 0))
    d.text((4, 4), f"{lote} {t:.2f}s q{alvo}", fill=(255, 255, 0))
    ims.append(im)
w, h = ims[0].size
rows = (len(ims) + cols - 1) // cols
P = Image.new("RGB", (w * min(cols, len(ims)), h * rows), (40, 40, 40))
for i, im in enumerate(ims):
    P.paste(im, ((i % cols) * w, (i // cols) * h))
P.save(saida, quality=92)
print(saida, P.size)
