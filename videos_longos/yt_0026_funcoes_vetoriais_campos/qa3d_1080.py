"""v9: cópia do qa3d.py para o render final 1920×1080 (pontos em px de 1080p; grava threejs/timeline_1080.json). yt_0026 v7: alinhamento Three.js × Manim (critério ≤ 2 px). Para cada quadro renderizado das cenas c7_* compara o ponto-origem que o c7.js projetou (pontos.json, em px de 960×540) com a
projeção do Python (v7.proj_c7: mesma câmera e mesmo encaixe na caixa) para o mesmo estado. Junta tudo em threejs/timeline.json. uso: python qa3d.py PT PB1 PB4 PB7 PS"""
import json
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
sys.path.insert(0, str(U))
import numpy as np  # noqa: E402
from v7 import proj_c7  # noqa: E402

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
            if not js or "o" not in js:
                continue
            m = proj_c7(cena[3:], e["box"], (0, 0, 0), e.get("az", 0.0))
            px = np.array([(m[0] * 120 + 960), (4.5 - m[1]) * 120])
            pior = max(pior, float(np.linalg.norm(px - np.array(js["o"]))))
            n += 1
        print(f"[qa3d] {lote}/{cena}: {n} pontos em {len(lista)} quadros; pior desvio {pior:.3f} px {'OK' if pior <= 2 else 'FALHA'}")
(U / "threejs" / "timeline_1080.json").write_text(json.dumps(tl), encoding="utf-8")
