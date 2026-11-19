"""Sonda 3D: cada cena do c41.js no estado final do alvo, com a câmera do c3d41.html (sem deslocamento) em 1920×1080, para comparar com os r3d_*.png."""
import json, os, subprocess, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
os.environ.setdefault("PEDIDOS3D", "0")
import math
import numpy as np
VER = {"bola": ((9.2, -6.2, 4.3), (0, 0, 0), 600, 560, 1.4), "grade": ((9.0, -6.8, 4.0), (0, 0, .05), 600, 560, 1.4),
       "ponto": ((8.6, -5.4, 4.4), (0, .6, .95), 620, 560, 1.3), "caixa": ((8.2, -5.6, 5.6), (1.15, 1.45, 1.0), 600, 520, 1.15),
       "bolagrade": ((9.0, -6.8, 4.0), (0, 0, .05), 600, 560, 1.4), "caixinha": ((7.2, -6.4, 4.9), (.95, .45, .35), 620, 560, 1.15),
       "cebola": ((9.2, -6.2, 4.3), (0, 0, 0), 600, 560, 1.4), "casquinha": ((8.6, -6.4, 4.6), (0, 0, 1.2), 600, 560, 1.4),
       "lata": ((8.4, -6.3, 4.4), (0, 0, .6), 600, 560, 1.4)}
EST = {"bola": {"cunha": 1}, "grade": {"celulas": 1}, "ponto": {"rho": 1, "fi": 1, "teta": 1, "pagina": 1, "sombra": 1, "altura": 1, "xy": 1},
       "caixa": {"celula": 1, "bordas": 1}, "bolagrade": {"bordas": 3, "celula": 1}, "caixinha": {"aresta": 3, "raioPar": 1}, "cebola": {"casca": 1},
       "casquinha": {"sonda": 1, "arcofi": 1}, "lata": {"sonda1": 1, "sonda2": 1, "quina": 1}}
def cam(c):
    p, t, cx, cy, DF = VER[c]; p, t = np.array(p, float), np.array(t, float)
    return {"pos": list(t + (p - t) * DF), "tgt": list(t), "up": [0, 0, 1], "cx": cx, "cy": cy, "fov": 22.0}
so = sys.argv[1:] or list(VER)
env = dict(os.environ, NODE_PATH="K:/PycharmProjects/manim-fisica/videos_longos/yt_0020_cinematica_angular/threejs/node_modules",
           CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe")
for c in so:
    e = dict(EST[c]); e["cam"] = cam(c)
    r = subprocess.run(["node", "r3d.js", "--sonda", c, "--estado", json.dumps(e), "--png", f"sonda/{c}.png", "--w", "1920", "--h", "1080"],
                       cwd=AQUI, env=env, capture_output=True, text=True)
    print(c, r.stdout.strip()[:300], r.stderr.strip()[-300:])
