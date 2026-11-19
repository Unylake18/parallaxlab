"""Quadros de conferência (v2 §7.4): os 21 do v1 (a 70% da âncora), os 7 novos de 3D e um quadro de cada uma das 21 sobreposições do §5
(no mesmo ponto da âncora). uso: python conf23.py [rodada] → renders/conferencia_<rodada>/*.png + renders/prancha_conferencia_<rodada>.png"""
import json
import sys
from pathlib import Path

import av
from PIL import Image, ImageDraw

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v2"
Q = json.loads((U / f"renders/quadros_{R}.json").read_text(encoding="utf-8"))
BASE = [(a, a, 0.7) for a in "H2 A3 D3 E1-3 E1-5 E1-9 E1-12 E1-13 E1-16 E1-17 E2-8 E2-9 E2-10 E3-1 E3-3 E3-7 E4-3 E4-7 E4-8 E4-9 S1".split()]
NOVOS = [("3D_H1", "H1", 0.5), ("3D_E1-1", "E1-1", 0.3), ("3D_E3-3", "E3-3", 0.6), ("3D_E1-6", "E1-6", 0.5), ("3D_E2-1", "E2-1", 0.5),
         ("3D_E4-1", "E4-1", 0.15), ("3D_D1", "D1", 0.6)]
SOBRE = [("S01_H2", "H2", 0.75), ("S02_D1", "D1", 0.8), ("S03_D2", "D2", 0.85), ("S04_E1-3", "E1-3", 0.5), ("S05_E1-4", "E1-4", 0.35),
         ("S06_E1-4", "E1-4", 0.8), ("S07_E1-6", "E1-6", 0.85), ("S08_E1-8", "E1-8", 0.6), ("S09_E1-10", "E1-10", 0.92), ("S10_E1-12", "E1-12", 0.8),
         ("S11_E1-13", "E1-13", 0.8), ("S12_E1-17", "E1-17", 0.5), ("S13_E1-15", "E1-15", 0.9), ("S14_E1-17", "E1-17", 0.9), ("S15_E2-3", "E2-3", 0.85),
         ("S16_E2-4", "E2-4", 0.5), ("S17_E2-7", "E2-7", 0.7), ("S18_E3-3", "E3-3", 0.9), ("S19_E3-5", "E3-5", 0.7), ("S20_E3-8", "E3-8", 0.8),
         ("S21_E4-9", "E4-9", 0.6)]
ini = sorted(Q.values())


def quadro(a, fr):
    i0 = Q[a]
    i1 = min(v for v in ini if v > i0)
    return int(i0 + fr * (i1 - i0))


alvo = {}
for nome, a, fr in BASE + NOVOS + SOBRE:
    alvo.setdefault(quadro(a, fr), []).append(nome)
od = U / f"renders/conferencia_{R}"
od.mkdir(parents=True, exist_ok=True)
c = av.open(str(U / f"renders/preview_yt0023_{R}_960x540.mp4"))
ims = {}
for i, f in enumerate(c.decode(video=0)):
    if i in alvo:
        im = f.to_image()
        for nome in alvo[i]:
            im.save(od / f"{nome}.png")
            t = im.resize((480, 270))
            ImageDraw.Draw(t).text((6, 4), f"{nome}  {i / 15:.1f}s", fill=(255, 255, 0))
            ims[nome] = t
    if i > max(alvo):
        break
for grupo, lista in (("base", BASE), ("3d", NOVOS), ("sobreposicoes", SOBRE)):
    tl = [ims[n] for n, _, _ in lista if n in ims]
    cols = 4
    rows = (len(tl) + cols - 1) // cols
    out = Image.new("RGB", (480 * cols, 270 * rows))
    for k, im in enumerate(tl):
        out.paste(im, ((k % cols) * 480, (k // cols) * 270))
    out.save(U / f"renders/prancha_conferencia_{grupo}_{R}.png")
print(len(ims))
