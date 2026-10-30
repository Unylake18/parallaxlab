"""QA de alinhamento 3D × Manim do v4 (960×540): erro em px entre a projeção real do Three.js (pontos.json do r3d.js) e o mapa analítico
da vista 'frente' / FK do manequim, ponto a ponto, em todos os quadros (passo 3). Aceitação: ≤ 2 px.
As setas da corda (balancim e amarração da pedra), o clarão, o arco de 56° e a seta p_bala usam o ponto REAL (Fundo3D.real), então o erro na
tela delas é 0 por construção; a coluna "mapa" mostra quanto o mapa analítico erraria.
uso: python qa_alinhamento_v4.py PH P8 Q6 Q7 PS"""
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
        piores = {}

        def reg(nome, v):
            a, n = piores.get(nome, (0.0, 0))
            piores[nome] = (max(a, v), n + 1)
        for f, e in lista[::3]:
            p = pts.get(str(f))
            if not p or e.get("cam", {}).get("modo") not in (None, "frente"):
                continue
            c = e["cam"]
            base = cena.split("@")[0]
            if base == "cavalo":
                from sec_cavalo import BAL_DX, BAL_Z, CORDA_Z0, PEITO_Z, Y_CORDA
                reg("arreio", erro(mapa(c, e["xp"], PEITO_Z, Y_CORDA), p["corda_peito"]))
                reg("balancim", erro(mapa(c, e["xp"] - BAL_DX, BAL_Z), p["balancim"]))
                reg("amarração na pedra", erro(mapa(c, e["xp"] - e["L"], CORDA_Z0), p["corda_pedra"]))
            elif base == "esferas":
                for (x, z, vis, _), q in zip(e["esf"], p["esf"]):
                    if vis:
                        reg("esferas", erro(mapa(c, x, z), q))
            elif base == "manequim":
                from sec_manequim import boca, mao
                for i in (0, 1):
                    reg("mãos", erro(mapa(c, *mao(e, i)), p[f"mao{i}"]))
                b = e.get("bola")
                if isinstance(b, list):
                    reg("bola", erro(mapa(c, b[0], b[1]), p["bola"]))
                if e.get("rifle") and e["rifle"].get("on"):
                    bx, bz, _ = boca(e, e["rifle"]["ang"])
                    reg("ponta do cano", erro(mapa(c, bx, bz), p["pb"]))
        out[cena] = {k: (round(v, 2), n) for k, (v, n) in piores.items()}
    return out


if __name__ == "__main__":
    for L in sys.argv[1:]:
        try:
            print(L, json.dumps(lote(L), ensure_ascii=False))
        except FileNotFoundError as x:
            print(L, "sem dados:", x.filename)
