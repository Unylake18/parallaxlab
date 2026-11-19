"""Sonda v3: cenas 3D nos estados finais com a câmera de cada alvo (ENQ), 960x540 → threejs/sonda/v3_<chave>.png + folha v3_folha.jpg"""
import json, os, subprocess, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent)); sys.argv = ["x"]
from k41 import cam_alvo, ENQ
from PIL import Image
EST = {"h1": {"cunha": 1}, "b1": {"rho": 1, "fi": 1, "teta": 1, "pagina": 1, "sombra": 1, "altura": 1, "xy": 1}, "b32": {"sonda": 1},
       "b4": {"casca": 1}, "b5": {"cunha": 1, "casca084": 1}, "b6": {"sonda": 1, "arcofi": 1}, "s2": {"sonda1": 1, "sonda2": 1, "quina": 1}, "h2": {"celulas": 1},
       "b21": {"aresta": 3, "raioPar": 1}, "b24": {"raio": 1, "meridiano": 1, "volta": 1, "piso": 1}}
env = dict(os.environ, NODE_PATH="K:/PycharmProjects/manim-fisica/videos_longos/yt_0020_cinematica_angular/threejs/node_modules", CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe")
ks = sys.argv[1:] or list(EST)
ims = []
for k in (os.environ.get("K3") or ",".join(EST)).split(","):
    e = dict(EST[k]); e["cam"] = cam_alvo(k)
    r = subprocess.run(["node", "r3d.js", "--sonda", ENQ[k][0], "--estado", json.dumps(e), "--png", f"sonda/v3_{k}.png", "--w", "960", "--h", "540"], cwd=AQUI, env=env, capture_output=True, text=True)
    print(k, r.stderr.strip()[-200:])
    ims.append(Image.open(AQUI / "sonda" / f"v3_{k}.png"))
bg = Image.new("RGB", (960 * 2, 540 * ((len(ims) + 1) // 2)), (19, 16, 48))
for i, im in enumerate(ims):
    bg.paste(im, ((i % 2) * 960, (i // 2) * 540), im)
bg.save(AQUI / "sonda" / "v3_folha.jpg", quality=90)
