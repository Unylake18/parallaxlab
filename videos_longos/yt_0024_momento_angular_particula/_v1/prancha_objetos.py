"""Prancha de objetos (handoff §7.3): mesa em C_34, C_TOPO e C_L a 1920×1080, disco em r = 0,60 e 0,30, fio esticado, puxador nas duas alturas.
Mede: fio (px de largura na vista de cima), contraste aro × disco e aresta do tampo × fundo, luminância do tampo, sombra de contato.
uso: python prancha_objetos.py → renders/objetos/*.png, renders/prancha_objetos.png, renders/objetos/medidas.txt"""
import json, math, subprocess, sys
sys.argv = ['x']
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
from pecas24 import C34, CTOPO, CL, C34H, proj, px_de
import fisica24 as F
U = Path(__file__).resolve().parent
O = U / "renders" / "objetos"
casos = []
for nome, c in (("C34", C34H), ("CTOPO", CTOPO), ("CL", CL)):
    for r, zp in ((0.60, 0.0), (0.30, -0.30)):
        th = 0.9
        casos.append((f"{nome}_r{int(r*100)}", c, [r * math.cos(th), r * math.sin(th)], zp))
fundo = Image.open(U / "fundo_lab.png").convert("RGBA").resize((1920, 1080))
lin = []
ims = []
for nome, c, d, zp in casos:
    e = dict(cam=c, disco=d, zp=zp, rastro=[[F.R0 * math.cos(a), F.R0 * math.sin(a)] for a in np.linspace(0.9 - 2.2, 0.9, 150)] if zp == 0 else [])
    arq = O / f"{nome}.png"
    t = subprocess.run(["bash", "threejs/sonda.sh", json.dumps(e), str(arq), "1920", "1080"], capture_output=True, text=True).stdout
    im = Image.alpha_composite(fundo, Image.open(arq).convert("RGBA")).convert("RGB")
    a = np.asarray(im, float) / 255
    lum = lambda p: float(0.2126 * p[..., 0] + 0.7152 * p[..., 1] + 0.0722 * p[..., 2]) if np.ndim(p) == 1 else (0.2126 * p[..., 0] + 0.7152 * p[..., 1] + 0.0722 * p[..., 2])
    L = lum(a)
    px = lambda p: [int(round(v * 2)) for v in px_de(proj(c, p))]
    cx, cy = px([d[0], d[1], 0.0195])
    # aro (anel rosa na borda do topo) × corpo do disco; tampo ao lado do disco; sombra a 4 cm na direção oposta à câmera
    k = 2 * c["K"] * 60 * 0.035
    def amostra(p, r=2):
        x, y = p
        return float(L[max(0, y - r):y + r + 1, max(0, x - r):x + r + 1].mean())
    aro = max(amostra(px([d[0] + 0.0325 * math.cos(q), d[1] + 0.0325 * math.sin(q), 0.0196])) for q in np.linspace(0, 6.28, 16))
    corpo = amostra(px([d[0], d[1] + 0.012, 0.0196]))
    tampo = amostra(px([d[0] + 0.12, d[1] - 0.10, 0.0]), 4)
    sombra = amostra(px([d[0] + 0.03, d[1] - 0.03, 0.0]))
    fio_mid = px([d[0] / 2, d[1] / 2, 0.009])
    col = L[fio_mid[1] - 8:fio_mid[1] + 9, fio_mid[0]]
    larg = int((col > (col.min() + 0.5 * (col.max() - col.min()))).sum()) if col.max() - col.min() > 0.08 else 0
    lin.append(f"{nome}: tampo lum {tampo:.2f} (≤ 0,85) · aro/corpo {aro:.2f}/{corpo:.2f} = {aro / max(corpo, 1e-3):.2f}× (≥ 1,6) · "
               f"sombra/tampo {sombra / max(tampo, 1e-3):.2f} · fio ~{larg} px (≥ 2 a 1080p) · {t.strip()[-60:] if 'Error' in t else ''}")
    ims.append(im.resize((960, 540)))
    dr = ImageDraw.Draw(ims[-1]); dr.text((12, 12), nome, fill=(255, 255, 255))
P = Image.new("RGB", (1920, 540 * 3))
for i, im in enumerate(ims):
    P.paste(im, ((i % 2) * 960, (i // 2) * 540))
P.save(U / "renders" / "prancha_objetos.png")
(O / "medidas.txt").write_text("\n".join(lin) + "\n", encoding="utf-8")
print("\n".join(lin))
