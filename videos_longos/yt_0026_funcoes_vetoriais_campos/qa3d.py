"""yt_0026: alinhamento Three.js × Manim (critério ≤ 2 px). Para cada quadro renderizado, compara os pontos que o b3d.js projetou (pontos.json)
com a projeção do Python (kit.projeta3d, a mesma câmera) para o mesmo estado. Também junta tudo em threejs/timeline.json (coordenadas de tela
dos pontos que o Manim prende, por lote, cena e quadro). uso: python qa3d.py PT PB4 PB7"""
import json
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
sys.path.insert(0, str(U))
import numpy as np  # noqa: E402
from kit import projeta3d  # noqa: E402

PTS = {   # nome do ponto → ponto 3D em função do estado
    "o": lambda e: (0, 0, 0), "cx": lambda e: (0, 0, 1.05), "c": lambda e: (3, 2, 0), "p1": lambda e: (1, 0, 0),
    "a1": lambda e: (1, 0, e.get("s", 0)), "a4": lambda e: (2, 0, 4 * e.get("s", 0)),
}
W, H = 960, 540
tl = json.loads((U / "threejs" / "timeline.json").read_text(encoding="utf-8")) if (U / "threejs" / "timeline.json").exists() else {}
for lote in sys.argv[1:]:
    ped = json.loads((U / "threejs" / "pedidos3d" / f"{lote}.json").read_text(encoding="utf-8"))["cenas"]
    tl[lote] = {}
    for cena, lista in ped.items():
        pj = json.loads((U / "threejs" / "q3d" / f"{lote}_{W}x{H}" / cena / "pontos.json").read_text(encoding="utf-8"))
        tl[lote][cena] = pj
        pior, n = 0.0, 0
        for f, e in lista:
            js = pj.get(str(f))
            if not js:
                continue
            for k, pt in js.items():
                m = projeta3d(e["cam"], (0, 0, 0.625) if (cena == 'gauss' and k == 'cx') else PTS[k](e))
                px = np.array([(m[0] + 8) / 16 * W, (4.5 - m[1]) / 9 * H])
                pior = max(pior, float(np.linalg.norm(px - np.array(pt))))
                n += 1
        print(f"[qa3d] {lote}/{cena}: {n} pontos em {len(lista)} quadros; pior desvio {pior:.3f} px {'OK' if pior <= 2 else 'FALHA'}")
(U / "threejs" / "timeline.json").write_text(json.dumps(tl), encoding="utf-8")
