"""yt_0027 (final, 1080p): alinhamento Three.js × Manim (critério ≤ 2 px; versão 1080p do final: px de 1920×1080, grava threejs/timeline_1080.json). Para cada quadro das cenas do lote compara os pontos que o f27.js projetou
(pontos.json, px) com projeta3d (kit.py, a mesma câmera do b3d.js) para o mesmo estado. Junta tudo em threejs/timeline.json.
uso: python qa3d.py PB6"""
import json
import math
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
sys.path.insert(0, str(U))
import numpy as np  # noqa: E402
from kit import projeta3d  # noqa: E402

S35, C35 = math.sin(math.radians(35)), math.cos(math.radians(35))


def alvos(cena, e):
    if cena == "cubo":
        return {"o": (0, 0, 0), "face": (0.8, 0, 0)}
    r = e.get("rot", 0.0)
    return {"o": (0, 0, 0), "ponta": (S35 * 2.0 * r, 0, C35 * 2.0 * r)}


tl = {}
for lote in sys.argv[1:]:
    ped = json.loads((U / "threejs" / "pedidos3d" / f"{lote}.json").read_text(encoding="utf-8"))["cenas"]
    tl[lote] = {}
    for cena, lista in ped.items():
        pj = json.loads((U / "threejs" / "q3d" / f"{lote}_1920x1080" / cena / "pontos.json").read_text(encoding="utf-8"))
        tl[lote][cena] = pj
        pior, n = 0.0, 0
        for f, e in lista:
            js = pj.get(str(f))
            if not js:
                continue
            for k, p in alvos(cena, e).items():
                if k not in js:
                    continue
                m = projeta3d(e["cam"], p)
                px = np.array([(m[0] * 120 + 960), (4.5 - m[1]) * 120])
                pior = max(pior, float(np.linalg.norm(px - np.array(js[k]))))
                n += 1
        print(f"[qa3d] {lote}/{cena}: {n} pontos em {len(lista)} quadros; pior desvio {pior:.3f} px {'OK' if pior <= 2 else 'FALHA'}")
(U / "threejs" / "timeline_1080.json").write_text(json.dumps(tl), encoding="utf-8")
