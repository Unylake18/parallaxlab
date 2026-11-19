"""bbox do 3D (alfa > 12) por alvo, em px de 1080p, com a câmera do ENQ (dx, dy, esc) e os estados do final do bloco.
uso: python bbox3.py b21 b6 ...   [env DX/DY/ESC para testar outro enquadramento da 1ª chave]"""
import json, os, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
AQUI = Path(__file__).resolve().parent
ks = sys.argv[1:]
sys.path.insert(0, str(AQUI.parent)); sys.argv = ["x"]
import k41
EST = {"h1": {"cunha": 1}, "b21": {"aresta": 3, "raioPar": 1}, "b6": {"sonda": 1, "arcofi": 1, "encontro": 1}, "s2": {"sonda1": 1, "sonda2": 1, "quina": 1},
       "b4": {"casca": 1}, "b5": {"cunha": 1, "casca084": 1}, "b32": {"sonda": 1}, "b1": {"rho": 1, "fi": 1, "teta": 1, "pagina": 1, "sombra": 1, "altura": 1, "xy": 1},
       "h2": {"celulas": 1}, "b24": {"raio": 1, "meridiano": 1, "volta": 1, "piso": 1}}
env = dict(os.environ, NODE_PATH="K:/PycharmProjects/manim-fisica/videos_longos/yt_0020_cinematica_angular/threejs/node_modules", CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe")
for k in ks:
    c, dx, dy, esc = k41.ENQ[k]
    if os.environ.get("DX"):
        dx, dy, esc = float(os.environ["DX"]), float(os.environ["DY"]), float(os.environ["ESC"])
    cam = k41.cam41(c, dx, dy, esc)
    e = dict(EST[k]); e["cam"] = cam
    r = subprocess.run(["node", "r3d.js", "--sonda", c, "--estado", json.dumps(e), "--png", f"sonda/_bb_{k}.png", "--w", "960", "--h", "540"], cwd=AQUI, env=env, capture_output=True, text=True)
    a = np.array(Image.open(AQUI / "sonda" / f"_bb_{k}.png").convert("RGBA"))
    ys, xs = np.nonzero(a[..., 3] > 12)
    print(k, (dx, dy, esc), "bbox 1080p: x", int(xs.min() * 2), int(xs.max() * 2), "y", int(ys.min() * 2), int(ys.max() * 2))
