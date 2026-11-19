"""Auditoria CONCÊNTRICO (v2 §1.3) sobre os pontos3d do f23.js (px de tela, 960×540).
Para cada quadro: (1) centro de cada peça coaxial sobre o eixo projetado; (2) pivô (ponto médio 3D de dois pontos opostos da borda) no eixo;
(3) topo do fio = ponto tangente do tambor (±raio, y, 0) e fio vertical; (4) mancais no eixo. Limites: 1 px; fio ≤ 0,5°."""
import math


def _d(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _dist_reta(p, a, b):
    vx, vy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(vx, vy) or 1.0
    return abs((p[0] - a[0]) * vy - (p[1] - a[1]) * vx) / n


def medir(pt):
    """pt: pontos3d de um quadro → dict de máximos {centro, pivo, mancal, fio_px, fio_graus}."""
    r = {"centro": 0.0, "pivo": 0.0, "mancal": 0.0, "fio_px": 0.0, "fio_graus": 0.0, "colinear": 0.0}
    blocos = []
    if pt.get("conc"):
        blocos.append(pt["conc"])
    for q in pt.get("pend", []):
        for a, b in q["conc"]:
            r["centro"] = max(r["centro"], _d(a, b))
    for c in blocos:
        for a, b in c["c"]:
            r["centro"] = max(r["centro"], _d(a, b))
        for a, b in c["p"]:
            r["pivo"] = max(r["pivo"], _d(a, b))
        for a, b in c["m"]:
            r["mancal"] = max(r["mancal"], _d(a, b))
        e0, e1 = c["eixo"]
        if _d(e0, e1) > 2:                                   # 3/4: todos os centros sobre a reta do eixo projetado
            for a, _ in c["c"] + c["m"]:
                r["colinear"] = max(r["colinear"], _dist_reta(a, e0, e1))
    for topo, baixo, tang in pt.get("fios", []):
        r["fio_px"] = max(r["fio_px"], _d(topo, tang))
        ang = math.degrees(math.atan2(abs(baixo[0] - topo[0]), abs(baixo[1] - topo[1]) or 1e-9))
        r["fio_graus"] = max(r["fio_graus"], ang)
    return r


LIM = {"centro": 1.0, "pivo": 1.0, "mancal": 1.0, "fio_px": 1.0, "fio_graus": 0.5, "colinear": 1.0}


def falhas(r):
    return [k for k, v in r.items() if v > LIM[k]]
