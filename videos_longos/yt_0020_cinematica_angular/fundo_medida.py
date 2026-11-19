"""yt_0020 v7 §1.6 · medida do fundo de estrelas: correlação de fase entre quadros consecutivos em blocos sem conteúdo → deslocamento em x por quadro.
Blocos (a 960×540, escalados na resolução do arquivo): faixa de cima (y 44…94) e de baixo (y 470…520), 6 blocos de 160 px cada; só entram blocos sem conteúdo
(desvio-padrão baixo: só estrelas). Aprovado: todo bloco com estrela com dx ≤ −1 px (nunca positivo, nunca 0 por > 2 quadros) e velocidade por camada ±10%.
uso: python fundo_medida.py ARQ.mp4 [passo_s=3.0] [t_ini t_fim]  → renders/v8/fundo_medida.txt"""
import sys
from collections import Counter
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
arq = sys.argv[1]
passo = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
c = av.open(arq)
s = c.streams.video[0]
fps = float(s.average_rate)
dur = float(s.duration * s.time_base) if s.duration else float(c.duration) / 1e6
t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
t1 = float(sys.argv[4]) if len(sys.argv) > 4 else dur
esc = s.width / 960.0
BL = [(int(44 * esc), int(94 * esc), int(x * esc), int((x + 160) * esc)) for x in range(0, 960, 160)] + \
     [(int(470 * esc), int(520 * esc), int(x * esc), int((x + 160) * esc)) for x in range(0, 960, 160)]


def fase(a, b):
    a, b = a - a.mean(), b - b.mean()
    F = np.fft.fft2(a) * np.conj(np.fft.fft2(b))
    F /= np.abs(F) + 1e-9
    r = np.fft.ifft2(F).real
    iy, ix = np.unravel_index(np.argmax(r), r.shape)
    if ix > r.shape[1] // 2:
        ix -= r.shape[1]
    return ix, float(r.max())


def par(t):
    c.seek(int(t / s.time_base), stream=s)
    fr = []
    for f in c.decode(s):
        if float(f.pts * s.time_base) >= t - 1e-6:
            fr.append((float(f.pts * s.time_base), f.to_ndarray(format="gray").astype(np.float32)))
            if len(fr) == 2:
                break
    return fr


res, zeros = [], 0
t = max(t0, 1.0)
while t < t1 - 1:
    fr = par(t)
    if len(fr) == 2:
        for (y0, y1, x0, x1) in BL:
            A, B = fr[1][1][y0:y1, x0:x1], fr[0][1][y0:y1, x0:x1]
            if A.std() > 7 or B.std() > 7 or A.std() < 0.3:
                continue
            ix, pk = fase(A, B)
            if pk > 0.10:
                res.append((fr[0][0], ix / esc))              # px a 960 de largura, por quadro; < 0: andou para a esquerda
    t += passo
d = np.array([r[1] for r in res])
out = [f"# yt_0020 — fundo_medida ({Path(arq).name}, {s.width}×{s.height}, {fps:g} fps): {len(res)} medidas de bloco em {t1 - t0:.0f} s, passo {passo} s", ""]
if len(d):
    neg, pos, zer = (d <= -1).sum(), (d > 0).sum(), (d == 0).sum()
    out += [f"dx ≤ −1 px: {neg} ({100 * neg / len(d):.1f}%) · dx > 0: {pos} · dx = 0: {zer}", "histograma do dx (px/quadro a 960):"]
    for v, n in sorted(Counter(np.round(d).astype(int)).items()):
        out.append(f"  {v:+3d} px: {n:5d} {'#' * min(60, n * 60 // max(1, len(d)))}")
    # camadas esperadas (px/quadro a 960 de largura e 15 fps): 0,40/0,75/1,25 u/s × 60 px/u ÷ fps
    esp = [v * 60 / fps for v in (0.40, 0.75, 1.25)]
    out.append(f"camadas esperadas: {', '.join(f'−{e:.2f}' for e in esp)} px/quadro")
else:
    out.append("nenhuma medida válida")
(U / "renders" / "v7").mkdir(parents=True, exist_ok=True)
(U / "renders" / "v7" / "fundo_medida.txt").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
