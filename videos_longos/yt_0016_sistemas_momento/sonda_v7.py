"""v7: sonda 3D — tira um print de uma cena 3D num estado gravado pela passagem seca (pedidos3d/<LOTE>.json), sem render do lote.
uso: python sonda_v7.py LOTE CENA QUADRO saida.png [--w 960 --h 540]   (QUADRO = quadro do lote; pega o pedido mais próximo)
     python sonda_v7.py - CENA '{"json": "do estado"}' saida.png"""
import json
import os
import subprocess
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
T = U / "threejs"
lote, cena, q, out = sys.argv[1:5]
extra = sys.argv[5:]
if lote == "-":
    e = json.loads(q)
else:
    ped = json.loads((T / "pedidos3d" / f"{lote}.json").read_text(encoding="utf-8"))["cenas"][cena]
    f, e = min(ped, key=lambda x: abs(x[0] - int(q)))
env = dict(os.environ, NODE_PATH=str(U.parent / "yt_0015_momento_impulso" / "threejs" / "node_modules"),
           CHROMIUM_PATH="C:/Program Files/Google/Chrome/Application/chrome.exe")
r = subprocess.run(["node", "r3d.js", "--sonda", cena.split("@")[0], "--estado", json.dumps(e), "--png", str(Path(out).resolve()), *extra],
                   cwd=T, env=env, capture_output=True, text=True, encoding="utf-8")
print(r.stdout[-1500:], r.stderr[-1500:])
