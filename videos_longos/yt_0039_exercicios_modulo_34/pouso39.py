"""yt_0039 · QA do pouso (handoff §8.2, item 2): no quadro da troca 2D ↔ 3D (linhas [pouso3d] do log), o contorno da região no quadro 3D × o
contorno no quadro 2D vizinho. Máscara = pixels com a cor do preenchimento da região (quarto de disco GEO 30 % no E3; chapa #9AA6C4 no E6), no MP4 do
lote (960×540); mede o deslocamento das bordas (esquerda, direita, topo, base da máscara) e a distância média entre os contornos, em px de 1080p.
Grava renders/v1/qa/pouso3d.txt."""
import re
from pathlib import Path

import av
import numpy as np

import os as _os
RV = _os.environ.get("RODADA", "v2")
AQUI = Path(__file__).resolve().parent
COR = {"PE3": np.array([0x45, 0x42, 0x66]), "PE6": np.array([0x9A, 0xA6, 0xC4])}


def quadros(arq, alvos):
    out = {}
    with av.open(str(arq)) as c:
        for i, f in enumerate(c.decode(video=0)):
            if i in alvos:
                out[i] = f.to_ndarray(format="rgb24").astype(int)
            if i > max(alvos):
                break
    return out


def mascara(a, cor, tol=26):
    m = np.abs(a - cor).max(2) < tol
    m[:60, :] = False
    m[:, 545:] = False
    return m


def contorno(m):
    e = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
    return np.argwhere(e)


def dist(c1, c2):
    if not len(c1) or not len(c2):
        return float("nan")
    from scipy.spatial import cKDTree
    t = cKDTree(c2)
    d, _ = t.query(c1)
    return float(np.median(d))


L = []
for lote in ("PE3", "PE6"):
    log = (AQUI / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")
    ev = re.findall(r"\[pouso3d\] \S+ (\S+) (\S+) quadro (\d+) \((.*?)\)", log)
    arq = AQUI / f"media_{lote}" / "videos" / "cena" / "540p15" / f"{lote}.mp4"
    for aid, tipo, q, desc in ev:
        q = int(q)
        Q = quadros(arq, {q - 2, q - 1, q, q + 1})
        a3, a2 = (Q[q + 1], Q[q - 2]) if "2D → 3D" in desc else (Q[q - 2], Q[q + 1])
        cor = COR[lote]
        if lote == "PE3":
            cor = np.median(a2[mascara(a2, cor, 40)], axis=0) if mascara(a2, cor, 40).any() else cor
        m2, m3 = mascara(a2, cor), mascara(a3, cor)
        if m2.sum() < 50 or m3.sum() < 50:
            L.append(f"{lote} {aid} {desc}: máscara vazia (2D {m2.sum()} px, 3D {m3.sum()} px)")
            continue
        b2 = [np.argwhere(m2)[:, k] for k in (0, 1)]
        b3 = [np.argwhere(m3)[:, k] for k in (0, 1)]
        dif = {"topo": (b3[0].min() - b2[0].min()), "base": (b3[0].max() - b2[0].max()), "esq": (b3[1].min() - b2[1].min()), "dir": (b3[1].max() - b2[1].max())}
        dc = dist(contorno(m3), contorno(m2))
        iou = (m2 & m3).sum() / max(1, (m2 | m3).sum())
        L.append(f"{lote} {aid} {desc}, quadros {q - 2} × {q + 1}: bordas (3D − 2D, px de 1080p) " +
                 ", ".join(f"{k} {2 * v:+d}" for k, v in dif.items()) + f"; distância mediana entre contornos {2 * dc:.1f} px; IoU {iou:.3f}")
(AQUI / "renders" / RV / "qa" / "pouso3d.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
