"""yt_0013 — um quadro por âncora (a 60 % do trecho, antes das limpezas de fim de trecho) + pranchas 4×3 com id, frase e tempo."""
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

P = Path(__file__).resolve().parent
OUT = P / "renders" / "final_sync"
(OUT / "quadros").mkdir(parents=True, exist_ok=True)
(OUT / "pranchas").mkdir(parents=True, exist_ok=True)
tr = json.loads((P / "ritmo.json").read_text(encoding="utf-8"))["trechos"]
alvos = [(r["id"], r["frase"], r["alvo"], tr[i + 1]["alvo"]) for i, r in enumerate(tr[:-1])]
pontos = sorted((a + max(0.5, 0.6 * (b - a)) if b - a > 0.8 else a + 0.5 * (b - a), i) for i, (_, _, a, b) in enumerate(alvos))
c = av.open(str(P / "final" / "master - 0013.mp4"))
s = c.streams.video[0]
s.thread_type = "AUTO"
quadros, j = {}, 0
for f in c.decode(s):
    t = float(f.pts * s.time_base)
    while j < len(pontos) and t >= pontos[j][0]:
        i = pontos[j][1]
        im = f.to_image().resize((640, 360))
        nome = f"{i + 1:03d}_{alvos[i][0]}.jpg"
        im.save(OUT / "quadros" / nome, quality=88)
        quadros[i] = (im, nome)
        j += 1
fonte = ImageFont.truetype("arial.ttf", 18)
for p in range(0, len(alvos), 12):
    folha = Image.new("RGB", (4 * 640 + 5 * 10, 3 * (360 + 46) + 10), (12, 14, 20))
    d = ImageDraw.Draw(folha)
    for k, i in enumerate(range(p, min(p + 12, len(alvos)))):
        x, y = 10 + (k % 4) * 650, 10 + (k // 4) * 406
        im, _ = quadros[i]
        folha.paste(im, (x, y))
        aid, fr, a, _ = alvos[i]
        d.text((x, y + 364), f"{i + 1:03d} {aid} · {int(a) // 60:02d}:{a % 60:05.2f} · {fr or '(início)'}"[:70], fill=(220, 225, 240),
               font=fonte)
    folha.save(OUT / "pranchas" / f"prancha_{p // 12 + 1:02d}.jpg", quality=85)
print(len(quadros), "quadros;", (len(alvos) + 11) // 12, "pranchas em", OUT)
