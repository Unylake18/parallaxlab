"""v4 (v3 §5): percentil 99 do canal mais claro nos pixels da folha e do gafanhoto (máscaras do threejs/p99.js), quadro 3D composto sobre o céu do
laboratório como no vídeo. Meta: < 235 (sem branco estourado). uso: python p99.py → renders/v7/p99.json"""
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
D = U / "renders" / "v7" / "p99"
fundo = Image.open(U / "fundo_lab.png").convert("RGBA").resize((960, 540))
out = {}
for f in sorted(D.glob("*_full.png")):
    lote, q = re.match(r"(\w+?)_(\d+)_full", f.stem).groups()
    comp = fundo.copy()
    comp.alpha_composite(Image.open(f).convert("RGBA"))
    rgb = np.asarray(comp.convert("RGB"), float)
    r = {}
    for nome in ("folha", "gaf"):
        m = np.asarray(Image.open(D / f"{lote}_{q}_{nome}.png").convert("RGBA"))[..., 3] > 200
        r[nome] = float(np.percentile(rgb[m].max(axis=1), 99)) if m.any() else 0.0
        r[nome + "_lum"] = float((rgb[m] @ np.array([0.2126, 0.7152, 0.0722])).mean() / 255) if m.any() else 0.0   # v4: contraste gafanhoto × folha
        r[nome + "_px"] = int(m.sum())
    out[f"{lote} q{q}"] = r
(U / "renders" / "v7" / "p99.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
