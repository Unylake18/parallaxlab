"""GLIFO SOLTO (handoff final §2.1.4): componente pequeno (ponto, vírgula, traço) isolado por mais de 2 quadros que NÃO pertence à expressão final.
Para cada jogada de caneta (um `[ordem]` no log_<L>.txt com seus `[glifo]`) toma a caixa da linha e compara cada quadro da janela com o quadro final da
jogada (0,4 s depois da última tinta): tudo o que for claro fora do quadro final (dilatado 6 px) e ficar parado ≥ 3 quadros (±3 px) é solto.
A ponta da caneta anda a cada quadro e o que está no quadro final (estrelas, glifos parciais) não conta.
uso: python solto24.py PB1 PB3 ...   → imprime tempo e posição de cada glifo solto; resumo `GLIFO SOLTO n=N`."""
import re
import sys
from pathlib import Path

import av
import numpy as np
from scipy import ndimage

U = Path(__file__).resolve().parent
FPS = 15
px = lambda x: (x / 16.0 + 0.5) * 960
py = lambda y: (0.5 - y / 9.0) * 540
total = 0
for L in sys.argv[1:]:
    log = (U / f"log_{L}.txt").read_text(encoding="utf-8", errors="replace").splitlines()
    plays, cur = [], None
    for ln in log:
        if ln.startswith("[ordem]"):
            cur = []
            if " voa " in ln:                  # só escrita por caneta/voo de linha; o glyph map (passo) move glifos da origem e geraria falsos positivos
                plays.append(cur)
        m = re.match(r"\[glifo\] (\S+) (\S+) (\S+) (\S+)", ln)
        if m and cur is not None:
            cur.append(tuple(map(float, m.groups())))
    jan = []
    for p in plays:
        if not p:
            continue
        t0 = min(g[0] for g in p)
        t1 = max(g[0] for g in p) + 1.0
        x0, x1 = min(g[1] for g in p) - 0.25, max(g[2] for g in p) + 0.25
        yc = np.mean([g[3] for g in p])
        jan.append((t0, t1, int(px(x0)), int(px(x1)), int(py(yc + 1.0)), int(py(yc - 1.0))))
    frames = {}
    need = set()
    for t0, t1, *_ in jan:
        for k in range(int(t0 * FPS) - 1, int((t1 + 0.4) * FPS) + 2):
            need.add(k)
    c = av.open(str(U / f"media_{L}/videos/cena/540p15/{L}.mp4"))
    for k, fr in enumerate(c.decode(video=0)):
        if k in need:
            frames[k] = fr.to_ndarray(format="gray").astype(np.int16)
    c.close()
    n_l = 0
    for t0, t1, xa, xb, ya, yb in jan:
        xa, ya = max(0, xa), max(0, ya)
        xb, yb = min(960, xb), min(540, yb)
        kf = int((t1 + 0.3) * FPS)
        if kf not in frames or kf <= int(t0 * FPS):
            continue
        fin = frames[kf][ya:yb, xa:xb] > 70
        proib = ndimage.binary_dilation(fin, iterations=6)
        prev = []
        for k in range(int(t0 * FPS), int(t1 * FPS) + 1):
            if k not in frames:
                continue
            m = (frames[k][ya:yb, xa:xb] > 70) & ~proib
            lab, n = ndimage.label(m)
            cur = []
            for i in range(1, n + 1):
                a = int((lab == i).sum())
                if 6 <= a <= 40:
                    cy, cx = ndimage.center_of_mass(lab == i)
                    cur.append((cx + xa, cy + ya, a))
            for cx, cy, a in cur:
                ach = [q for q in prev if abs(q[0] - cx) <= 3 and abs(q[1] - cy) <= 3]
                dur = 1 + max([q[3] for q in ach] + [0])
                prev_new = (cx, cy, a, dur)
                if dur >= 3 and dur == 3:
                    n_l += 1
                    print(f"[{L}] GLIFO SOLTO t={k / FPS:.2f}s em ({cx:.0f},{cy:.0f}) px, área {a}")
                cur[cur.index((cx, cy, a))] = prev_new
            prev = [(c_[0], c_[1], c_[2], c_[3]) if len(c_) > 3 else (c_[0], c_[1], c_[2], 1) for c_ in cur]
    print(f"[{L}] {len(jan)} jogadas de caneta; GLIFO SOLTO n={n_l}")
    total += n_l
print(f"GLIFO SOLTO n={total}")
