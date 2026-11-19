"""yt_0044 · sonda das cenas 3D (v2): renderiza cada cena do c44.js no deslocamento do alvo (com o SNAP do G8) em 1920×1080, compõe sobre o papel e grava a prancha
renders/teste/sonda3d.jpg + a lista dos pontos projetados.   uso: python sonda3d.py [cena ...]"""
import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.argv_orig = sys.argv[:]
sys.argv = sys.argv[:1]
import k44  # noqa: E402

U = Path(__file__).resolve().parent
OUT = U / "renders" / "teste" / "sonda"
OUT.mkdir(parents=True, exist_ok=True)
ESTADOS = {
    "lataParede": (k44.OL, {}), "lataDobradica": (k44.OL, {}), "lataDob3": (k44.OC, {"p1": 1, "p2": 1, "p3": 1}), "helice": (k44.OL, {}),
    "cubo": (k44.OL, {"grade": 1}), "cuboCaixas": (k44.OL, {}), "cuboSonda": (k44.OC, {}), "cuboDiag": (k44.OC, {}), "cuboFolha": (k44.OL, {"folha": 1, "caixas": 1}),
    "tetraSonda": (k44.OT, {}), "tetraCent": (k44.OT, {}), "tetraPlano": (k44.OC, {"plano": 1}),
    "cone": (k44.OM, {}), "coneCm": (k44.OM, {}), "coneCasca": (k44.OM, {}), "semi": (k44.OM, {}), "semiFatia": (k44.OM, {}),
}
cenas = [a for a in sys.argv_orig[1:]] or list(ESTADOS)
env = dict(os.environ, NODE_PATH="K:/PycharmProjects/manim-fisica/videos_longos/yt_0020_cinematica_angular/threejs/node_modules",
           CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe")
papel = None
try:
    from assets.calculo.papel import papel  # noqa: F401
except Exception:
    pass
pts = {}
ims = []
for c in cenas:
    o, est = ESTADOS[c]
    e = {"cam": k44.cam44(c, o), "clip": o["clip"], **est}
    png = OUT / f"{c}.png"
    r = subprocess.run(["node", "r3d.js", "--sonda", c, "--estado", json.dumps(e), "--png", str(png), "--w", "1920", "--h", "1080"], cwd=U / "threejs", env=env,
                       capture_output=True, text=True)
    if r.returncode:
        print(c, "ERRO", r.stderr[-400:])
        continue
    j = json.loads(r.stdout.strip().splitlines()[-1])
    pts[c] = j["pts"]
    subprocess.run(["node", "r3d.js", "--sonda", c, "--estado", json.dumps({**e, "semPiso": True}), "--png", str(OUT / f"{c}_sempiso.png"), "--w", "1920", "--h", "1080"],
                   cwd=U / "threejs", env=env, capture_output=True, text=True)
    bg = Image.new("RGBA", (1920, 1080), (24, 20, 58, 255))
    d = ImageDraw.Draw(bg)
    for x in range(0, 1920, 60):
        d.line([(x, 0), (x, 1080)], fill=(60, 54, 110, 255))
    for y in range(0, 1080, 60):
        d.line([(0, y), (1920, y)], fill=(60, 54, 110, 255))
    bg.alpha_composite(Image.open(png).convert("RGBA"))
    for n, (x, y) in j["pts"].items():
        d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=(255, 90, 90, 255))
    ims.append((c, bg.convert("RGB")))
    ox, oy = j["pts"]["O"]
    print(f"{c:14s} O=({ox:7.2f},{oy:7.2f})  snap: {'OK' if abs(ox / 60 - round(ox / 60)) < .01 * 1 and abs(oy / 60 - round(oy / 60)) < .01 * 1 else 'FORA'}")
(U / "renders" / "teste" / "sonda3d_pts.json").write_text(json.dumps(pts, indent=0), encoding="utf-8")
cols = 3
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (960 * cols, 540 * rows))
for i, (c, im) in enumerate(ims):
    sheet.paste(im.resize((960, 540)), ((i % cols) * 960, (i // cols) * 540))
sheet.save(U / "renders" / "teste" / "sonda3d.jpg", quality=88)
