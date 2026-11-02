"""yt_0018 v7: estimativa (sem render) de quanta tela fica sem animação depois do plano(): para cada trecho entre marcas, sobra = D − (esc·A + esperas).
Lista os trechos com sobra >= LIM s (esses vão parar a tela se nada anima dentro deles).
uso: python idle_plano.py [lote ...] [--lim 1.5]"""
import json
import re
import sys
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
LEAD, FPS = 0.08, 15
args = [a for a in sys.argv[1:] if not a.startswith("--")]
LIM = float(sys.argv[sys.argv.index("--lim") + 1]) if "--lim" in sys.argv else 1.5
if "--lim" in sys.argv:
    args = [a for a in args if a != sys.argv[sys.argv.index("--lim") + 1]]
LOTES = args or ["PH", "PX0", "PX2", "PX3", "PX4", "PX5", "PEP"]


def plano(A, W, D):
    if A + W < 1e-6:
        return 1.0, 1.0
    if D >= A + W:
        s_ = min(1.8, max(1.0, (D / (A + W)) ** 0.5))
        return s_, (max(1.0, (D - s_ * A) / W) if W > 1e-6 else 1.0)
    wp = max(0.15 * W, D - A)
    if A + wp <= D + 1e-6:
        return 1.0, wp / W if W > 1e-6 else 1.0
    return max(0.5, (D - wp) / A), (wp / W if W > 1e-6 else 1.0)


def t_ate(aid, frac):
    a = ANC[aid]
    tw, nom = a["t"], a["nominal"]
    xs = [0.0] + [0.15 + k / 2.7 for k in range(len(tw))] + [max(nom, 0.15 + len(tw) / 2.7)]
    ys = [0.0] + list(tw) + [a["dur"]]
    return float(np.interp(frac * nom, xs, ys))


def alvo(mid):
    parts = mid.split(":", 2)
    kind, aid, arg = parts[0], parts[1], (parts[2] if len(parts) > 2 else None)
    a = ANC.get(aid)
    if kind == "an":
        return a["ini"]
    if kind == "gat":
        fala = a["fala"].split()
        al = re.findall(r"\w+", arg.lower())
        k = next((i for i in range(len(fala)) if fala[i:i + len(al)] == al), None)
        return None if k is None else a["ini"] + max(0.0, a["t"][k] - LEAD)
    return a["ini"] + max(0.0, t_ate(aid, float(arg)) - LEAD)


tot_idle = 0.0
linhas = []
for lote in LOTES:
    f = U / f"medicao_{lote}.json"
    if not f.exists():
        print(f"{lote}: sem medição")
        continue
    marcas = json.loads(f.read_text(encoding="utf-8"))["marcas"]
    aid_atual, fim_anc = None, None
    ini_seg = None
    for i, m in enumerate(marcas):
        kind = m["id"].split(":")[0]
        if kind == "fim":
            continue
        t0 = alvo(m["id"])
        if t0 is None:
            continue
        if kind == "an":
            aid_atual = m["id"].split(":")[1]
            fim_anc = ANC[aid_atual]["fim"]
        A, W, j, tgt = 0.0, 0.0, i, fim_anc
        while j < len(marcas):
            A += marcas[j]["A"]
            W += marcas[j]["W"]
            j += 1
            if j >= len(marcas):
                break
            nid = marcas[j]["id"]
            if nid.startswith("an:") or nid == "fim":
                break
            t_ = alvo(nid)
            if t_ is not None and t_ - t0 >= 0.25:
                tgt = t_
                break
        D = max(0.3, tgt - t0)
        sa, sw = plano(A, W, D)
        sobra = D - (sa * A + sw * W)
        if sobra >= LIM:
            linhas.append((lote, aid_atual, m["id"], t0, D, A, W, sa, sobra))
        tot_idle += max(0.0, sobra)
for l in linhas:
    print(f"{l[0]:4s} {l[1]:6s} {l[2]:38s} abs {l[3]:7.1f}  D {l[4]:5.1f}  A {l[5]:4.1f}  W {l[6]:4.1f}  esc {l[7]:.2f}  SOBRA {l[8]:5.1f} s")
print(f"{len(linhas)} trechos com sobra >= {LIM} s; sobra total estimada {tot_idle:.0f} s")
