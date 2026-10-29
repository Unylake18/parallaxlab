"""Composição 3D (PNGs opacos do Three.js, fundo) + camada Manim (.mov com alfa, por cima) → H.264 CRF 14 (16:9).
Uso (na raiz do worktree/repositório): python compor.py --trecho c01 --classe PT1 [--res 960x540] [--fps 15]
Gera renders/<TRECHO>_<WxH>.mp4 (composto) e renders/<TRECHO>_parte3d_<WxH>.mp4 (só o 3D). Usa o PyAV da .venv."""
import argparse
import json
import time
from fractions import Fraction
from pathlib import Path

import av
import numpy as np
from PIL import Image

UNIT = Path(__file__).resolve().parent


def enc(path, w, h, fps):
    out = av.open(str(path), "w")
    s = out.add_stream("libx264", rate=Fraction(fps))
    s.width, s.height, s.pix_fmt = w, h, "yuv420p"
    s.options = {"crf": "14", "preset": "medium"}
    return out, s


def put(out, s, rgb):
    for p in s.encode(av.VideoFrame.from_ndarray(rgb, format="rgb24")):
        out.mux(p)


ap = argparse.ArgumentParser()
ap.add_argument("--trecho", required=True)
ap.add_argument("--classe", required=True)
ap.add_argument("--res", default="960x540")
ap.add_argument("--fps", type=int, default=15)
a = ap.parse_args()
w, h = map(int, a.res.split("x"))
total = round(json.loads((UNIT / "threejs" / f"timeline_{a.trecho}.json").read_text(encoding="utf-8"))["duracao_s"] * a.fps)
f3d = UNIT / "threejs" / f"frames3d_{a.trecho}_{w}x{h}"
mov = UNIT / f"media_{a.classe}" / "videos" / "cena" / f"{h}p{a.fps}" / f"{a.classe}.mov"
(UNIT / "renders").mkdir(exist_ok=True)
o3, s3 = enc(UNIT / "renders" / f"{a.trecho}_parte3d_{w}x{h}.mp4", w, h, a.fps)
oc, sc = enc(UNIT / "renders" / f"{a.trecho}_{w}x{h}.mp4", w, h, a.fps)
t0 = time.time()
man = av.open(str(mov))
cam = (f.to_ndarray(format="rgba") for f in man.decode(video=0))
last, n_m = np.zeros((h, w, 4), np.uint8), 0
for i in range(total):
    bg = np.asarray(Image.open(f3d / f"f{i:05d}.png").convert("RGB"))
    fg = next(cam, None)
    if fg is None:
        fg = last
    else:
        n_m += 1
        last = fg
    al = fg[..., 3:4].astype(np.float32) / 255
    put(o3, s3, bg)
    put(oc, sc, (fg[..., :3] * al + bg * (1 - al) + .5).astype(np.uint8))
for o, s in ((o3, s3), (oc, sc)):
    for p in s.encode():
        o.mux(p)
    o.close()
extra = sum(1 for _ in cam)
print(json.dumps({"quadros_3d": total, "quadros_manim": n_m + extra, "segundos": round(time.time() - t0, 1)}))
if n_m != total or extra:
    print("AVISO: número de quadros diferente entre as camadas")
