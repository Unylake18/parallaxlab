"""yt_0045 final itens 23 e 27 (lata na grade ≤ 1 px; 2 verticais, sem piso, dentro de x ∈ [60,900] no H1 e [60,740] no B7), medidos nos stills 1080p.
Saída: renders/final/qa/lata_campo_final.txt (+ as linhas [lata] dos logs: itens 24/25 da seta da lata)."""
from pathlib import Path

import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
D = U / "renders" / "final" / "qa" / "comparacao" / "stills"
L = ["yt_0045 final · itens 23 e 27 (lata) nos stills nativos 1920x1080"]
for nome, lim, esperado in (("01_H1_helice_lata.png", (60, 900), (180, 780)), ("14_B7-1_helice_montando.png", (60, 740), (60, 540)), ("16_B7-3_lendo_resposta.png", (60, 740), (60, 540))):
    a = np.asarray(Image.open(D / nome).convert("RGB")).astype(int)
    geo = (abs(a[..., 0] - 184) < 30) & (abs(a[..., 1] - 196) < 30) & (abs(a[..., 2] - 218) < 30)
    verde = (a[..., 1] > 200) & (a[..., 0] < 215) & (a[..., 2] < 160) & (a[..., 0] > 150)           # base recolorida (lima) no B7-3
    cor = geo | (verde if "16_" in nome else False)
    col = cor[:, :1000].sum(0)
    # verticais: colunas com ≥ 150 px de traço (as paredes têm 240–300 px)
    xs = [x for x in range(1000) if col[x] >= 150]
    grupos = []
    for x in xs:
        if grupos and x - grupos[-1][-1] <= 1:
            grupos[-1].append(x)
        else:
            grupos.append([x])
    centros = [float(np.mean(g)) for g in grupos]
    erro = max(abs(c - e) for c, e in zip(centros, esperado)) if len(centros) == 2 else float("nan")
    xmax = int(round(max(centros))) if centros else -1                 # a parede da direita é o ponto mais à direita da lata (elipses: CX ± U)
    ymax = int(np.where(cor[:900, :1000].any(1))[0].max())
    L.append(f"  {nome}: verticais encontradas {len(centros)} em x = {', '.join(f'{c:.1f}' for c in centros)} (esperado {esperado}; erro máx {erro:.1f} px na grade de 60 px) · "
             f"traço da lata até x = {xmax} (limite {lim[1]}) e até y = {ymax} (a base fecha em CY = 780, sem piso abaixo)")
for f in sorted(U.glob("log_P[HB]*.txt")):
    for ln in f.read_text(encoding="utf-8", errors="replace").splitlines():
        if ln.startswith("[lata]"):
            L.append("  " + ln)
(U / "renders" / "final" / "qa" / "lata_campo_final.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
