"""yt_0023 v4 — portões novos medidos nos quadros do preview de um lote (960×540 / 15 fps):
  CONTRASTE      : agrupamentos de pixels lima (#C8FF2E) ou magenta-neon (#E040FB) com contraste WCAG < 3,0 contra o anel de pixels em volta
  OBJETO CORTADO : faixa clara contínua (≥ 24 px) colada à borda do quadro (peça cortada pela margem)
  EMENDA         : salto entre o último quadro de um trecho e o primeiro do seguinte (passada dos lotes) muito acima do salto típico
uso: python gates_v4.py LOTE [saida.txt]"""
import sys
from pathlib import Path

import av
import numpy as np
from scipy import ndimage as ndi

U = Path(__file__).resolve().parent
L = sys.argv[1]
mp4 = U / f"media_{L}/videos/cena/540p15/{L}.mp4"
c = av.open(str(mp4))
fr = [f.to_ndarray(format="rgb24") for f in c.decode(video=0)]
N = len(fr)
H, W = fr[0].shape[:2]
out = []


def lum(a):
    a = a.astype(float) / 255.0
    a = np.where(a <= 0.03928, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


# ── CONTRASTE ──
ALVOS = {"lima": np.array([200, 255, 46]), "magenta": np.array([224, 64, 251])}
ev_c = []
ev_c_ant = []
for k in range(0, N, 15):
    f = fr[k]
    for nome, rgb in ALVOS.items():
        m = (np.abs(f.astype(int) - rgb).sum(axis=2) < 70)
        lab, n = ndi.label(ndi.binary_dilation(m, iterations=2))
        for i in range(1, n + 1):
            reg = lab == i
            area = int((reg & m).sum())
            if area < 40:
                continue
            for ini, fim_, lista in ((2, 4, ev_c), (3, 7, ev_c_ant)):             # v5: anel colado ao halo (2–4 px depois do agrupamento); a definição antiga (3–7 px) fica só como contagem
                anel = ndi.binary_dilation(reg, iterations=fim_) & ~ndi.binary_dilation(reg, iterations=ini)
                if anel.sum() < 20:
                    continue
                viz = np.median(f[anel], axis=0)
                l1, l2 = float(lum(rgb[None, :])[0]), float(lum(viz[None, :])[0])
                cr = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
                if cr < 3.0:
                    lista.append((k / 15, nome, area, round(cr, 2), tuple(int(v) for v in ndi.center_of_mass(reg))))
out.append(f"CONTRASTE {L}: {len(ev_c)} agrupamentos lima/magenta com contraste < 3,0 (anel colado ao halo; definição antiga 3–7 px: {len(ev_c_ant)})")
out += [f"  t={t:.1f}s {n} area={a}px contraste={cr} yx={cg}" for t, n, a, cr, cg in ev_c[:25]]

# ── OBJETO CORTADO ──
ev_o = []
for k in range(0, N, 15):
    g = fr[k].mean(axis=2)
    for nome, faixa in (("topo", g[0:2, :].max(axis=0)), ("base", g[-2:, :].max(axis=0)), ("esq", g[:, 0:2].max(axis=1)), ("dir", g[:, -2:].max(axis=1))):
        clara = faixa > 150
        lab, n = ndi.label(clara)
        for i in range(1, n + 1):
            tam = int((lab == i).sum())
            if tam >= 24:
                ev_o.append((k / 15, nome, tam))
out.append(f"OBJETO CORTADO {L}: {len(ev_o)} faixas claras coladas à borda do quadro")
out += [f"  t={t:.1f}s borda={b} comprimento={s}px" for t, b, s in ev_o[:25]]

# ── EMENDA ──
d = [float(np.abs(fr[i + 1].astype(int) - fr[i].astype(int)).mean()) for i in range(N - 1)]
med = float(np.median(d)) + 1e-6
ev_e = [(i / 15, round(x, 2), round(x / med, 1)) for i, x in enumerate(d) if x > max(6 * med, 4.0)]
out.append(f"EMENDA {L}: {len(ev_e)} saltos entre quadros consecutivos > 6× a mediana ({med:.2f})")
out += [f"  t={t:.2f}s salto={x} ({r}×)" for t, x, r in ev_e[:25]]
txt = "\n".join(out)
print(txt)
if len(sys.argv) > 2:
    Path(sys.argv[2]).write_text(txt, encoding="utf-8")
