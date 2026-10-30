"""v7 (A6): miniaturas dos objetos 3D reais (o disco, os dois discos e as três esferas) como sprites com sombra: recorte do render 3D
(sonda_v7.py, 1920×1080) com borda que some (alfa radial), para colar no mapa do A6. uso: python sprites_v7.py"""
from pathlib import Path

import numpy as np
from PIL import Image

D = Path(__file__).resolve().parent / "assets_unidade" / "sprites"
for nome, (cx, cy, w, h) in {"disco": (960, 560, 900, 560), "dois": (960, 560, 1000, 560), "esferas": (960, 470, 900, 760)}.items():
    a = np.asarray(Image.open(D / f"raw_{nome}.png").convert("RGB"), dtype=np.float64)[cy - h // 2:cy + h // 2, cx - w // 2:cx + w // 2]
    Y, X = np.mgrid[0:h, 0:w]
    r = np.sqrt(((X - w / 2) / (w / 2)) ** 2 + ((Y - h / 2) / (h / 2)) ** 2)
    al = np.clip((1.0 - r) / 0.35, 0, 1)
    al = al * al * (3 - 2 * al)
    out = np.dstack([a, 255 * al]).astype(np.uint8)
    Image.fromarray(out, "RGBA").save(D / f"{nome}.png")
    print(nome, out.shape)
