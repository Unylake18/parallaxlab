"""yt_0039 · v2 B3 (massa como volume): stills de APROVAÇÃO, 960×540, da cena Three.js `massa` nos ângulos de entrada (vista de cima
ortográfica = o 2D, alt = 0) e de chegada (elevação 32°, azimute −35°, fov 22°, alt = 1), para E4-3 (meia elipse, ρ = k y) e E5-4 (meia arruela,
ρ = k r). Grava renders/<RODADA>/qa/b3/*.png (o 3D sobre o fundo do vídeo) e a prancha b3_aprovacao.jpg. Nada vai para o render do vídeo."""
import json
import math
import os
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
RV = os.environ.get("RODADA", "v2")
OUT = AQUI / "renders" / RV / "qa" / "b3"
OUT.mkdir(parents=True, exist_ok=True)
ENV = dict(os.environ, CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe",
           NODE_PATH="K:/PycharmProjects/manim-fisica/videos_longos/yt_0020_cinematica_angular/threejs/node_modules")


def cam_topo(k, cx, cy):
    return {"orto": True, "k": k, "cx": cx, "cy": cy, "pos": [0, 0, 50], "tgt": [0, 0, 0], "up": [0, 1, 0]}


def cam_incl(tgt, d, el=32, az=-35, cx=960, cy=560, fov=22):
    e, a = math.radians(el), math.radians(az)
    pos = [tgt[0] + d * math.cos(e) * math.sin(a), tgt[1] - d * math.cos(e) * math.cos(a), tgt[2] + d * math.sin(e)]
    return {"pos": pos, "tgt": list(tgt), "up": [0, 0, 1], "cx": cx, "cy": cy, "fov": fov}


CASOS = [("E4-3_meia_elipse_entrada", {"forma": "elipse", "alt": 0.0, "cam": cam_topo(470, 545, 900)}),
         ("E4-3_meia_elipse_inclinada", {"forma": "elipse", "alt": 1.0, "H": .8, "cam": cam_incl((0, .25, .3), 6.6, cx=560, cy=620)}),
         ("E5-4_meia_arruela_entrada", {"forma": "arruela", "alt": 0.0, "cam": cam_topo(210, 520, 860)}),
         ("E5-4_meia_arruela_inclinada", {"forma": "arruela", "alt": 1.0, "cam": cam_incl((0, .9, .35), 13.5, cx=540, cy=620)})]

# fundo: a cor mediana do violeta do próprio preview (quadro do E4-3 no v1, faixa sem desenho)
fundo = np.array([0x13, 0x10, 0x30], dtype=np.uint8)
v1 = AQUI / "renders" / "v1" / "qa" / "still_09_E4-3.png"
if v1.exists():
    a = np.asarray(Image.open(v1).convert("RGB"))
    fundo = np.median(a[140:200, 20:60].reshape(-1, 3), axis=0).astype(np.uint8)
saidas = []
for nome, est in CASOS:
    png = OUT / f"_{nome}_alfa.png"
    r = subprocess.run(["node", "r3d.js", "--w", "960", "--h", "540", "--sonda", "massa", "--estado", json.dumps(est), "--png", str(png)],
                       cwd=AQUI / "threejs", env=ENV, capture_output=True, text=True, timeout=180)
    assert png.exists(), r.stderr[-800:]
    im = Image.open(png).convert("RGBA")
    bg = Image.new("RGBA", im.size, tuple(int(c) for c in fundo) + (255,))
    bg.alpha_composite(im)
    f = OUT / f"b3_{nome}.png"
    bg.convert("RGB").save(f)
    png.unlink()
    saidas.append((nome, f))
    print(f, r.stdout.strip()[-160:])
# prancha 2 × 2 (resolução cheia de cada still)
W, H = 960, 540
pr = Image.new("RGB", (2 * W + 30, 2 * H + 90), (24, 22, 46))
d = ImageDraw.Draw(pr)
try:
    fn = ImageFont.truetype("arial.ttf", 22)
except Exception:
    fn = None
for i, (nome, f) in enumerate(saidas):
    x, y = (i % 2) * (W + 30), (i // 2) * (H + 45) + 40
    pr.paste(Image.open(f), (x, y))
    d.text((x + 8, y - 32), nome.replace("_", " "), fill=(230, 230, 245), font=fn)
pr.save(OUT / "b3_aprovacao.jpg", quality=92)
print(OUT / "b3_aprovacao.jpg")
