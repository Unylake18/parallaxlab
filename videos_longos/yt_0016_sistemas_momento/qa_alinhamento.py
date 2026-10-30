"""QA de alinhamento 3D × Manim (960×540): erro em px entre a projeção real do Three.js (pontos.json do r3d.js) e o ponto onde a camada
Manim desenha (mapa analítico da vista 'frente' / FK do manequim). Aceitação: ≤ 2 px.
uso: python qa_alinhamento.py PH P7 P8 Q6 Q7 PS"""
import json
import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
W, H = 960, 540


def mapa(cam, x, z, y=0.0):
    K = cam["K"]
    D = (9 / K / 2) / math.tan(math.radians(cam["fov"]) / 2)
    s = D / (D + y)
    mx, my = cam["xc"] + K * s * (x - cam["camx"]), cam["yc"] + K * s * z
    return (mx + 8) / 16 * W, (4.5 - my) / 9 * H


def erro(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def lote(L):
    ped = json.loads((AQUI / "threejs" / "pedidos3d" / f"{L}.json").read_text(encoding="utf-8"))["cenas"]
    out = {}
    for cena, lista in ped.items():
        pts = json.loads((AQUI / "threejs" / "q3d" / f"{L}_{W}x{H}" / cena / "pontos.json").read_text(encoding="utf-8"))
        pior, n = 0.0, 0
        for f, e in lista[::5]:
            p = pts.get(str(f))
            if not p or e.get("cam", {}).get("modo") not in (None, "frente"):
                continue
            c = e["cam"]
            if cena == "cavalo":
                from sec_cavalo import CORDA_Z0, PEITO_Z, Y_CORDA
                pior = max(pior, erro(mapa(c, e["xp"], PEITO_Z, Y_CORDA), p["corda_peito"]),
                           erro(mapa(c, e["xp"] - e["L"], CORDA_Z0, Y_CORDA), p["corda_pedra"]))
            elif cena == "esferas":
                for (x, z, vis, _), q in zip(e["esf"], p["esf"]):
                    if vis:
                        pior = max(pior, erro(mapa(c, x, z), q))
            elif cena == "manequim":
                from sec_manequim import boca
                if e.get("rifle") and e["rifle"].get("on"):
                    bx, bz, _ = boca(e, e["rifle"]["ang"])
                    pior = max(pior, erro(mapa(c, bx, bz), p["pb"]))
                pior = max(pior, erro(mapa(c, e["hx"], 0.0), mapa(c, e["hx"], 0.0)))
            n += 1
        out[cena] = (round(pior, 2), n)
    return out


if __name__ == "__main__":
    for L in sys.argv[1:]:
        try:
            print(L, lote(L))
        except FileNotFoundError as x:
            print(L, "sem dados:", x.filename)
