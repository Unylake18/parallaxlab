"""Prancha de objetos v2 (handoff v2 §8.1): renders reais a 1920×1080 da mesa v2 (C_34 do hook e da teoria, C_TOPO, C_L), do painel_queda
(esfera no alto e em 0,6 s), da orbita (35° e de cima) e da nuvem. Mede ESTOURO (luminância máxima do tampo nu ≤ 0,55), TAMANHO 3D
(disco ≥ 3 % da largura na C_34 do hook; mesa ≥ 75 % da largura no hook; mesa na coluna esquerda nos blocos), fio, anel rosa e furo.
uso: python prancha_objetos.py → renders/objetos/*.png, renders/prancha_objetos.png, renders/objetos/medidas.txt"""
import json, math, subprocess, sys
sys.argv = ['x']
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
from pecas24 import C34, C34H, CTOPO, CL, proj
import fisica24 as F
U = Path(__file__).resolve().parent
O = U / "renders" / "objetos"
O.mkdir(parents=True, exist_ok=True)
fundo = Image.open(U / "fundo_lab.png").convert("RGBA").resize((1920, 1080))
lum = lambda a: 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
px = lambda c, p: [(proj(c, p)[0] + 8) / 16 * 1920, (4.5 - proj(c, p)[1]) / 9 * 1080]


def sonda(nome, e, cena="mesa_furo"):
    arq = O / f"{nome}.png"
    t = subprocess.run(["bash", "threejs/sonda.sh", json.dumps(e), str(arq), "1920", "1080", cena], capture_output=True, text=True).stdout
    pts = json.loads(t.strip().splitlines()[-1])["pts"] if t.strip() else {}
    im = Image.alpha_composite(fundo, Image.open(arq).convert("RGBA")).convert("RGB")
    return im, pts


lin, ims = [], []
th = 0.9
for nome, c in (("C34_hook", C34H), ("C34_teoria", C34), ("CTOPO", CTOPO), ("CL", CL)):
    for r, zp in ((0.60, 0.0), (0.30, -0.30)):
        d = [r * math.cos(th), r * math.sin(th)]
        e = dict(cam=c, disco=d, zp=zp, rastro=[[r * math.cos(a), r * math.sin(a)] for a in np.linspace(th - 2.2, th, 150)])
        im, pts = sonda(f"{nome}_r{int(r * 100)}", e)
        a = np.asarray(im, float) / 255
        L = lum(a)
        # disco: diâmetro em px (largura projetada do topo)
        xs = [px(c, (d[0] + 0.045 * math.cos(q), d[1] + 0.045 * math.sin(q), 0.021))[0] for q in np.linspace(0, 2 * math.pi, 64)]
        dd = max(xs) - min(xs)
        cs = [px(c, (x, y, 0)) for x, y in ((-.8, -.8), (.8, -.8), (.8, .8), (-.8, .8))]
        mesa_x = (min(p[0] for p in cs), max(p[0] for p in cs))
        aro = max(float(L[int(p[1]) - 1:int(p[1]) + 2, int(p[0]) - 1:int(p[0]) + 2].mean()) for p in
                  [px(c, (d[0] + 0.0375 * math.cos(q), d[1] + 0.0375 * math.sin(q), 0.0215)) for q in np.linspace(0, 6.28, 24)])
        corpo = float(L[int(px(c, (d[0], d[1] + 0.02, 0.0215))[1]), int(px(c, (d[0], d[1] + 0.02, 0.0215))[0])])
        fm = px(c, (d[0] / 2, d[1] / 2, 0.010))
        col = L[int(fm[1]) - 10:int(fm[1]) + 11, int(fm[0])]
        larg = int((col > col.min() + 0.5 * (col.max() - col.min())).sum()) if col.max() - col.min() > 0.06 else 0
        # ESTOURO: tampo nu (sem disco, fio, rastro), fora de 3 cm do furo
        if r == 0.60:
            im2, _ = sonda(f"{nome}_nu", dict(cam=c, fio=False))
            L2 = lum(np.asarray(im2, float) / 255)
            mk = Image.new("L", (1920, 1080), 0)
            ImageDraw.Draw(mk).polygon([tuple(p) for p in [px(c, (x, y, 0)) for x, y in ((-.79, -.79), (.79, -.79), (.79, .79), (-.79, .79))]], fill=255)
            o_ = px(c, (0, 0, 0)); rr = abs(px(c, (0.03, 0, 0))[0] - o_[0]) + abs(px(c, (0, 0.03, 0))[1] - o_[1]) + 4
            ImageDraw.Draw(mk).ellipse([o_[0] - rr, o_[1] - rr, o_[0] + rr, o_[1] + rr], fill=0)
            m_ = np.asarray(mk) > 0
            est = float(L2[m_].max())
            lin.append(f"{nome}: ESTOURO tampo nu lum máx {est:.3f} (≤ 0,55) {'OK' if est <= 0.55 else 'FALHA'} · mesa x {mesa_x[0]:.0f}…{mesa_x[1]:.0f} px "
                       f"({(mesa_x[1] - mesa_x[0]) / 1920 * 100:.0f} % da largura)")
        lin.append(f"{nome}_r{int(r * 100)}: disco {dd:.0f} px = {dd / 1920 * 100:.1f} % da largura · aro/corpo {aro:.2f}/{corpo:.2f} = {aro / max(corpo, 1e-3):.1f}× · fio ~{larg} px")
        ims.append((f"{nome}_r{int(r * 100)}", im))
# painel_queda: esfera no alto (t = 0) e em t = 0,6 s; câmera ortográfica frontal
CQ = dict(az=-90.0, el=0.0, alvo=[0.4, 0.0, -0.9], K=2.4, fov=0.0, xc=-5.04, yc=-0.45)
for nome, t in (("queda_t0", 0.0), ("queda_t06", 0.6)):
    z = -0.5 * 9.8 * t * t
    est = [[0.4, -0.5 * 9.8 * (k * 0.1) ** 2] for k in range(int(t / 0.1 + 1e-6) + 1)][:-1]
    im, pts = sonda(nome, dict(cam=CQ, esfera=[0.4, z], estrobo=est, ima=1.0 if t == 0 else 0.0), "painel_queda")
    ims.append((nome, im))
for nome, cam in (("orbita_35", dict(az=-90.0, el=35.0, alvo=[-1.56, 0, 0], K=1.0, fov=43.6, xc=-3.9, yc=-0.45)),
                  ("orbita_topo", dict(az=-90.0, el=90.0, alvo=[-1.56, 0, 0], K=0.95, fov=0.0, xc=-3.9, yc=-0.65))):
    im, pts = sonda(nome, dict(cam=cam, planeta=[-2.0, 1.4]), "orbita")
    ims.append((nome, im))
im, pts = sonda("nuvem", dict(cam=dict(az=-90.0, el=22.0, alvo=[0, 0, 0.35], K=1.45, fov=43.6, xc=3.7, yc=-0.9), ang=0.3, acesas=[3, 40, 77, 120, 200, 300]), "nuvem")
ims.append(("nuvem", im))
col = 3
P = Image.new("RGB", (640 * col, 360 * ((len(ims) + col - 1) // col)))
for i, (n, im) in enumerate(ims):
    t = im.resize((640, 360))
    ImageDraw.Draw(t).text((10, 8), n, fill=(255, 230, 0))
    P.paste(t, ((i % col) * 640, (i // col) * 360))
P.save(U / "renders" / "prancha_objetos.png")
(O / "medidas.txt").write_text("\n".join(lin) + "\n", encoding="utf-8")
print("\n".join(lin))
