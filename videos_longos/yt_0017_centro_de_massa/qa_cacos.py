"""QA dos cacos da granada (handoff v3 do lote 1, §6.2):
VOLUME DOS CACOS — volume de cada malha ÷ volume do corpo (quadratura independente) contra 2/4,5 · 1/4,5 · 1,5/4,5 (±3%) e a soma (1,00 ± 3%).
CENTROIDE × FÍSICA — em cada quadro renderizado, distância (px) entre o centroide projetado de cada caco (pontos.json: cen) e o ponto físico
do mesmo quadro (pedidos3d: estado → projeta3d). No campo de provas o ponto físico é o da física pontual (os números do roteiro); o caco
sai do encaixe no corpo em T_SEP e apoia na linha de contato (G4): esses quadros saem separados. No espaço (exp) o encaixe é físico.
uso: python qa_cacos.py PH P2"""
import json
import sys

import numpy as np

from kit import AQUI, projeta3d
from pecas3d import CEN, MED, MS, MT

W, H = 960, 540
px = lambda p: np.array([(p[0] + 8) / 16 * W, (4.5 - p[1]) / 9 * H])
alvo = [m / MT for m in MS]
fr = [v / MED["vol_corpo"] for v in MED["vol"]]
soma = MED["soma"] / MED["vol_corpo"]
print("[cacos] VOLUME DOS CACOS: " + " · ".join(f"{m:g} kg {f:.4f} (alvo {a:.4f}; {100 * (f / a - 1):+.2f}%)" for m, f, a in zip(MS, fr, alvo))
      + f" · soma {soma:.4f}")
ok = all(abs(f / a - 1) <= 0.03 for f, a in zip(fr, alvo)) and abs(soma - 1) <= 0.03
print(f"[cacos] VOLUME DOS CACOS: {'dentro' if ok else 'FORA'} da tolerância de ±3%")
for lote in sys.argv[1:]:
    ped = json.loads((AQUI / "threejs" / "pedidos3d" / f"{lote}.json").read_text(encoding="utf-8"))["cenas"]
    for cena in ("gra", "exp"):
        arq = AQUI / "threejs" / "q3d" / f"{lote}_{W}x{H}" / cena / "pontos.json"
        if cena not in ped or not arq.exists():
            continue
        pts = json.loads(arq.read_text(encoding="utf-8"))
        cat = {"voo": [0.0, 0], "encaixe": [0.0, 0], "apoio": [0.0, 0]}
        for f, e in ped[cena]:
            q, g = pts.get(str(f)), e["gr"]
            if q is None or q.get("modo") != "cacos" or "frags" not in g:
                continue
            for k, fk in enumerate(g["frags"]):
                if cena == "exp":
                    p3 = (fk[0] + g["esc"] * CEN[k][0], g["esc"] * CEN[k][1], fk[1] + g["esc"] * CEN[k][2])
                else:
                    p3 = (fk[0], 0.0, fk[1])
                d = float(np.linalg.norm(px(projeta3d(e["cam"], p3)) - np.asarray(q["cen"][k])))
                lift = (q.get("lift") or [0, 0, 0])[k]
                c_ = "apoio" if lift > 1e-4 else ("encaixe" if cena == "gra" and fk[3] < 0.999 else "voo")
                cat[c_][0] = max(cat[c_][0], d)
                cat[c_][1] += 1
        for c_, (dm, n) in cat.items():
            if n:
                print(f"[cacos] CENTROIDE × FÍSICA {lote}/{cena} {c_}: {n} amostras (caco × quadro), pior {dm:.2f} px")
