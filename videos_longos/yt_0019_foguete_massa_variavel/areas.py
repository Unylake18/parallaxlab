"""yt_0019 v5 — G30 ÁREA MORTA e G31 QUADRO VAZIO sobre o preview (1 quadro por segundo, 240×135).
Fundo estimado = mediana temporal dos quadros amostrados (estrelas, grade e cantos fixos); ocupado = pixel que difere do fundo.
Grade 4 × 3 (12 células) sobre a área útil (abaixo do canto); célula ocupada = ≥ 1,5% de pixels diferentes (v3 §2).
ÁREA MORTA: trecho > 4 s em que mais de 6 das 12 células estão vazias. QUADRO VAZIO: quadro com menos de 0,8% da área útil ocupada.
uso: python areas.py [renders/preview_yt0019_v9_960x540.mp4] → renders/area_morta.txt"""
import sys
from pathlib import Path

import av
import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else U / "renders" / "preview_yt0019_v9_960x540.mp4"
c = av.open(str(SRC))
fps = float(c.streams.video[0].average_rate)
passo = int(round(fps))
quadros, idx = [], []
for i, fr in enumerate(c.decode(c.streams.video[0])):
    if i % passo:
        continue
    quadros.append(np.asarray(fr.to_image().resize((240, 135), Image.BILINEAR), dtype=np.int16))
    idx.append(i)
Q = np.stack(quadros)
fundo = np.median(Q, axis=0)
y0 = int(135 * 0.14)                                         # abaixo do canto/título
dif = (np.abs(Q - fundo).max(axis=3) > 60)[:, y0:, :]
H, W = dif.shape[1], dif.shape[2]
ch, cw = H // 3, W // 4
vazio_cel = np.zeros((len(Q), 3, 4), bool)
for r in range(3):
    for k in range(4):
        bloco = dif[:, r * ch:(r + 1) * ch, k * cw:(k + 1) * cw]
        vazio_cel[:, r, k] = bloco.mean(axis=(1, 2)) < 0.015
frac_vazia = vazio_cel.mean(axis=(1, 2))
ocup = dif.mean(axis=(1, 2))
fmt = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
linhas = []
runs, ini = [], None
for k, f in enumerate(vazio_cel.sum(axis=(1, 2)) > 6):
    if f and ini is None:
        ini = k
    if (not f or k == len(frac_vazia) - 1) and ini is not None:
        fim = k if not f else k + 1
        if fim - ini > 4:
            runs.append((ini, fim))
        ini = None
vazios = [k for k in range(len(Q)) if ocup[k] < 0.008]
linhas.append(f"{len(runs)} trechos de ÁREA MORTA (> 4 s com mais de 6 das 12 células vazias) e {len(vazios)} QUADROS VAZIOS em {len(Q)} amostras (1 por segundo)")
for a, b in runs:
    linhas.append(f"  ÁREA MORTA {fmt(a)}–{fmt(b)} ({b - a} s): células vazias em média {12 * frac_vazia[a:b].mean():.1f}/12")
for k in vazios:
    linhas.append(f"  QUADRO VAZIO {fmt(k)} (ocupação {100 * ocup[k]:.2f}%)")
(U / "renders" / "area_morta.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print("\n".join(linhas))
