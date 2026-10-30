"""v7 (handoff §3): alinhamento 3D × Manim nas cenas 3D novas. O Manim prende setas e rótulos pela projeção exata da câmera do b3d.js
(kit.proj3d); aqui ela é comparada, quadro a quadro, com o ponto que o Three.js projetou (pontos.json do r3d.js). Meta ≤ 2 px.
uso: python qa_alinhamento_v7.py → log_alinh_v7.txt"""
import json
import math
import sys
from pathlib import Path

sys.argv = sys.argv[:1]
U = Path(__file__).resolve().parent
sys.path.insert(0, str(U))
from kit import proj3d  # noqa: E402

T = U / "threejs"
W, H = 960, 540


def px(p):
    return ((p[0] + 8) / 16 * W, (4.5 - p[1]) / 9 * H)


def pontos_esperados(cena, e):
    r = {}
    c = e["cam"]
    if cena == "esferas":
        if e.get("disco"):
            r["dc"] = (e["disco"]["x"], e["disco"]["y"], 0.62)
        if e.get("bola"):
            r["bola"] = (e["bola"]["x"], 0, e["bola"]["z"])
    elif cena == "blocos":
        for i, b in enumerate(e.get("blocos", [])):
            r[f"b{i}"] = (b["x"], -b["d"] / 2, b["h"] / 2)
            r[f"t{i}"] = (b["x"], b["d"] / 2, b["h"])
    elif cena == "terra":
        r["bola"] = (e["bx"], 0, e["bz"])
    elif cena == "rifle":
        r["boca"] = (e["xr"], 0, e["zb"])
    elif cena == "placas":
        for i, w in enumerate(e["rows"]):
            tx, tz = w["piv"][0] + math.sin(w["th"]), w["piv"][1] - math.cos(w["th"])
            r[f"pl{i}"] = (tx, 0, tz - 0.5)
    return {k: px(proj3d(c, v)) for k, v in r.items()}


out = []
for lote in ("PH", "P7", "P9", "P10", "Q8", "PC"):
    arq = T / "pedidos3d" / f"{lote}.json"
    if not arq.exists():
        continue
    ped = json.loads(arq.read_text(encoding="utf-8"))["cenas"]
    for cena, lista in ped.items():
        base = cena.split("@")[0]
        pj = T / "q3d" / f"{lote}_{W}x{H}" / cena / "pontos.json"
        if base not in ("esferas", "blocos", "terra", "rifle", "placas") or not pj.exists():
            continue
        pts = json.loads(pj.read_text(encoding="utf-8"))
        pior, n = (0.0, None, None), 0
        for f, e in lista:
            q = pts.get(str(f))
            if not q:
                continue
            for k, (x, y) in pontos_esperados(base, e).items():
                if k in q and isinstance(q[k], list) and len(q[k]) == 2 and isinstance(q[k][0], (int, float)):
                    d = math.hypot(q[k][0] - x, q[k][1] - y)
                    n += 1
                    if d > pior[0]:
                        pior = (d, f, k)
        out.append(f"{lote} {cena:10s} {n:6d} pontos · desvio máximo {pior[0]:.3f} px (quadro {pior[1]}, {pior[2]})")
(U / "log_alinh_v7.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
