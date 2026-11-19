"""yt_0045 final R2/item 23: distância (px, 1080p) do eixo z (azul) ao traço CONTÍNUO da frente (hélice, tampa), medida nos stills nativos
1920x1080 de renders/<R>/qa/comparacao/stills (H1: CX 480; B7: CX 300). Saída: renders/<R>/qa/eixo_z.txt"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "final"
D = U / "renders" / R / "qa" / "comparacao" / "stills"
CASOS = [("01_H1_helice_lata.png", 480, (727.5, 577.5, 540)), ("14_B7-1_helice_montando.png", 300, (750, 600)), ("15_B7-2_helice_conta.png", 300, (750, 600)), ("16_B7-3_lendo_resposta.png", 300, (750, 600, 630))]
L = [f"yt_0045 · eixo z × traço da frente (rodada {R}): menor distância de um pixel do eixo (azul) a um pixel de traço contínuo da frente"]
for nome, cx, cruz in CASOS:
    a = np.asarray(Image.open(D / nome).convert("RGB")).astype(int)
    azul = (abs(a[..., 0] - 90) < 40) & (abs(a[..., 1] - 162) < 40) & (a[..., 2] > 200)
    strip = np.zeros_like(azul)
    strip[:, cx - 3:cx + 4] = True
    eixo = azul & strip
    ys = np.where(eixo.any(1))[0]
    # traço contínuo da frente: laranja/lima/GEO claro fora do eixo, na janela do eixo ± 40 px
    laranja = (a[..., 0] > 200) & (a[..., 1] > 110) & (a[..., 1] < 215) & (a[..., 2] < 160)
    geo = (abs(a[..., 0] - 184) < 28) & (abs(a[..., 1] - 196) < 28) & (abs(a[..., 2] - 218) < 28)
    outro = (abs(a[..., 0] - 0xA8) < 20) & (abs(a[..., 1] - 0x79) < 20) & (abs(a[..., 2] - 0x4F) < 25)
    traco = laranja | geo | outro
    win = np.zeros_like(traco)
    win[:, cx - 45:cx + 46] = True
    dist = ndimage.distance_transform_edt(~(traco & win))
    pcs = []
    for yc in cruz:                                   # só nos cruzamentos da frente com o eixo (±24 px de cada um)
        w = np.zeros_like(eixo)
        w[int(yc) - 24:int(yc) + 25, :] = True
        d = dist[eixo & w]
        pcs.append(f"y={yc}: {d.min():.1f} px")
    L.append(f"  {nome}: pixels do eixo {int(eixo.sum())}; menor distância ao traço contínuo da frente por cruzamento: " + "; ".join(pcs))
(U / "renders" / R / "qa" / "eixo_z.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
