"""QA de travadas (handoff v4 §4): nas tomadas 3D de cada lote (quadros com fundo 3D, lidos dos pedidos3d), diferença média entre
quadros consecutivos (cinza, 240×135). Lista (a) quadros quase iguais ao anterior (< 15% da mediana da janela de 2 s) durante movimento
e (b) saltos isolados > 3× a mediana da janela (vizinhos normais). Viradas e cortes de câmera aparecem como saltos e são anotados à parte (lista `cortes`).
uso: python qa_travadas.py PH P8 PS ..."""
import json
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent


def quadros3d(L):
    arq = U / "threejs" / "pedidos3d" / f"{L}.json"
    if not arq.exists():
        return set()
    ped = json.loads(arq.read_text(encoding="utf-8"))["cenas"]
    return {f for lista in ped.values() for f, _ in lista}


def lote(L, cortes=()):
    q3 = quadros3d(L)
    c = av.open(str(U / f"media_{L}/videos/cena/540p15/{L}.mp4"))
    ant, d = None, []
    for i, fr in enumerate(c.decode(video=0)):
        g = np.asarray(fr.to_image().convert("L").resize((240, 135)), dtype=np.float32)
        if ant is not None:
            d.append((i, float(np.abs(g - ant).mean())))
        ant = g
    dd = dict(d)
    rep, salto = [], []
    for i, x in d:
        if i not in q3 or i - 1 not in q3:
            continue
        jan = [dd[k] for k in range(i - 15, i + 16) if k in dd and k in q3]
        med = float(np.median(jan))
        if med < 0.05:                      # cena parada: não é travada
            continue
        viz = [dd.get(i - 1), dd.get(i + 1)]
        if None in viz:
            continue
        # repetido: quase igual ao anterior com os vizinhos em movimento (um fim de ease, com vizinhos lentos, não conta)
        if x < 0.15 * med and min(viz) > 0.5 * med:
            rep.append((round(i / 15, 2), round(x, 3), round(med, 3)))
        # salto: um pulo isolado, com os vizinhos normais (movimento de câmera e viradas são vários quadros grandes seguidos)
        elif x > 3 * med and max(viz) < 1.5 * med:
            salto.append((round(i / 15, 2), round(x, 3), round(med, 3)))
    return rep, salto


if __name__ == "__main__":
    for L in sys.argv[1:]:
        rep, salto = lote(L)
        print(f"{L}: quadros quase repetidos {len(rep)} {rep[:12]}")
        print(f"{L}: saltos {len(salto)} {salto[:20]}")
