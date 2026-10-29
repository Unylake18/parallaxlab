"""QA do alinhamento Manim × Three.js de um lote: o que a camada Manim desenhou em cada quadro (qa_overlay_<lote>.json) contra os pontos
que o r3d.js mediu na câmera do Three.js no mesmo quadro (pontos.json); e, no haltere, a escala/folga do último quadro frontal; na
explosão, o comprimento das setas de momento relativo (devem ser iguais).
Uso: python qa_3d.py X1"""
import json
import sys

import numpy as np

from kit import AQUI

LOTE = sys.argv[1] if len(sys.argv) > 1 else "X1"
W, H = 960, 540
q3d = AQUI / "threejs" / "q3d" / f"{LOTE}_{W}x{H}"
ov = json.loads((AQUI / f"qa_overlay_{LOTE}.json").read_text(encoding="utf-8"))


def px(p):
    return np.array([(p[0] + 8) / 16 * W, (4.5 - p[1]) / 9 * H])


for cena, d in ov.items():
    if not (q3d / cena / "pontos.json").exists():
        print(f"[qa] {cena}: camada 2D (sem fundo 3D), {len(d)} quadros registrados")
        continue
    pts = json.loads((q3d / cena / "pontos.json").read_text(encoding="utf-8"))
    pior, n = 0.0, 0
    for f, o in d.items():
        if f not in pts:
            continue
        q = pts[f]
        for k, v in o.items():
            if k not in q:
                continue
            lista = isinstance(v[0], list)                          # frags / fis: um ponto por caco
            a, b = (v, q[k][:len(v)]) if lista else (v, q[k])
            pares = zip(a, b) if lista else [(a, b)]
            for x, y in pares:
                pior = max(pior, float(np.linalg.norm(px(x) - np.asarray(y))))
        n += 1
    print(f"[qa] {cena}: camada Manim × Three.js no mesmo quadro: {n} quadros, pior {pior:.3f} px")

if "hal" in ov:
    f = max(ov["hal"], key=int)
    o = ov["hal"][f]
    b1, b2 = px(o["b1"]), px(o["b2"])
    r1, r2 = 0.8 * (1 / 3) ** (1 / 3) * 0.95 / 16 * W, 0.8 * 0.95 / 16 * W      # haltere 2D (K = 0,95)
    esq, dir_ = b1[0] - r1, b2[0] + r2
    pal = ((-7.4 + 8) / 16 * W, (0.7 + 8) / 16 * W)
    print(f"[qa] haltere (último quadro): ocupa {100 * (dir_ - esq) / (pal[1] - pal[0]):.0f}% da largura do PALCO; folga esquerda "
          f"{esq - pal[0]:.0f} px, direita {pal[1] - dir_:.0f} px; ⊕ a {(px(o['cm'])[0] - b1[0]) / (b2[0] - b1[0]):.4f} da haste a partir da leve")
