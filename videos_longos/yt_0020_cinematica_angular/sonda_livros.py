"""sonda do 3D dos livros (v7): python sonda_livros.py saida.png [W H] [u1 u2]"""
import json, math, subprocess, sys
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from kit import cam_obl
from sec_t5 import Rx, Ry, fl
out = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 960; H = int(sys.argv[3]) if len(sys.argv) > 3 else 540
u1 = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0; u2 = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
g = math.radians(90)
a1, a2 = u1 * g, u2 * g
L = Ry(a2) @ Rx(a1); R = Rx(a2) @ Ry(a1)
cam = cam_obl(-62.0, -26.0, (0, 0, 0), K=12.5, xc=0.0, yc=-1.9, fov=16)
e = {"c": [[-0.3, 0, 0], [0.3, 0, 0]], "L": fl(L), "R": fl(R), "G": fl(R), "oG": 0, "sx": 0.3, "oe": 1, "oz": 1, "on": 1, "ln": 0.11, "cam": cam,
     "arcs": [{"k": 0, "ax": "x", "a0": 0.5, "a": a1, "op": 1 if u1 > 0 else 0}, {"k": 0, "ax": "y", "a0": 0.5, "a": a2, "op": 1 if u2 > 0 else 0},
              {"k": 1, "ax": "y", "a0": 0.5, "a": a1, "op": 1 if u1 > 0 else 0}, {"k": 1, "ax": "x", "a0": 0.5, "a": a2, "op": 1 if u2 > 0 else 0}]}
r = subprocess.run(["node", "r3d.js", "--sonda", "livros", "--estado", json.dumps(e), "--png", out, "--w", str(W), "--h", str(H)], cwd=Path(__file__).parent / "threejs",
                   env={**__import__("os").environ, "CHROMIUM_PATH": "C:/Program Files/Google/Chrome/Application/chrome.exe"}, capture_output=True, text=True)
print(r.stdout[-400:], r.stderr[-600:])
