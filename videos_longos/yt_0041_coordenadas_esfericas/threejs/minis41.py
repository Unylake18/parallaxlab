"""Miniaturas desta unidade (recortes de PNGs 3D do c41.js em 1920×1080): células do H2 (painel do B2-1), bola/cebola/casquinha/lata (B7),
ponto (S1). Renderiza pelo modo sonda do r3d.js com a câmera do alvo e recorta em volta dos pontos."""
import json, os, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
AQUI = Path(__file__).resolve().parent
sys.argv = [sys.argv[0]]
sys.path.insert(0, str(AQUI.parent))
import k41
env = dict(os.environ, NODE_PATH="K:/PycharmProjects/manim-fisica/videos_longos/yt_0020_cinematica_angular/threejs/node_modules",
           CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe")
def sonda(cena, cam, est, png):
    e = dict(est); e["cam"] = cam
    r = subprocess.run(["node", "r3d.js", "--sonda", cena, "--estado", json.dumps(e), "--png", png, "--w", "1920", "--h", "1080"], cwd=AQUI, env=env,
                       capture_output=True, text=True)
    return json.loads(r.stdout.strip().splitlines()[-1])["pts"]
def corta(png, cx, cy, w, h, saida):
    a = Image.open(png).convert("RGBA")
    a.crop((int(cx - w / 2), int(cy - h / 2), int(cx + w / 2), int(cy + h / 2))).save(saida)
cam = k41.cam_alvo("h2")
pts = sonda("grade", cam, {"celulas": 1, "semPiso": 1}, "sonda/_grade_h2.png")
p, q = k41.proj3d(cam, k41.P41["grade"]["celPoloIn"]), k41.proj3d(cam, k41.P41["grade"]["celEqIn"])
corta("sonda/_grade_h2.png", p[0], p[1], 200, 150, "sonda/mini_polo.png")
corta("sonda/_grade_h2.png", q[0] - 20, q[1], 220, 165, "sonda/mini_eq.png")
for k, cena, est in (("bola", "bola", {"cunha": 1, "semPiso": 1}), ("cebola", "cebola", {"casca": 1, "semPiso": 1}), ("casquinha", "casquinha", {"sonda": 1, "semPiso": 1}),
                     ("lata", "lata", {"sonda1": 1, "sonda2": 1, "quina": 1, "semPiso": 1}), ("ponto", "ponto", {"rho": 1, "fi": 1, "teta": 1, "pagina": 1, "sombra": 1, "altura": 1})):
    c = k41.cam41(cena)
    sonda(cena, c, est, f"sonda/_{k}.png")
    a = np.array(Image.open(f"sonda/_{k}.png").convert("RGBA"))
    ys, xs = np.nonzero(a[..., 3] > 12)
    Image.fromarray(a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).save(f"sonda/mini_{k}.png")
print("ok")
