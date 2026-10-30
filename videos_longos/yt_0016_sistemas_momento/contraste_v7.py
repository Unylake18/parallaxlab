"""v7 (handoff §3): contraste entre cada rótulo e o fundo ATRÁS dele (WCAG, meta ≥ 4,5:1).
Lê contr_<LOTE>.txt (aud_v7.sh: caixa, cor e opacidade de cada texto a cada 0,5 s). O fundo é o quadro 3D puro do mesmo instante
(threejs/q3d/<LOTE>_960x540/<cena>/fNNNNN.png, sem nenhuma camada do Manim), com o véu do céu da CONTA por cima (como o kit faz),
ou o céu da unidade (fundo_lab) onde não há 3D. Fundo = percentil 95 da luminância dentro da caixa (o pior caso: brilho, névoa,
gelo atrás); texto = o pixel mais claro do texto no preview v7 (percentil 99 na caixa; a cor registrada pelo Manim
não serve: Text guarda a cor nas letras). Também mede onde há fog/glow atrás de texto (fundo claro).
Saída: log_contraste_v7.txt. uso: python contraste_v7.py"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
PRIMEIRA = {"PH": "H1", "P7": "T7-1", "P8": "T8-1", "P9": "T9-1", "P10": "T10-1", "Q6": "E6-1", "Q7": "E7-1", "Q8": "E8-1", "Q9": "E9-1",
            "PC": "C-1", "PS": "S1"}
t0s = [(ANC["ancoras"][a]["t0"], a) for a in ANC["ordem"]]
CEU = np.asarray(Image.open(U / "assets_unidade" / "fundo_lab_960x540.png").convert("RGB"), dtype=np.float64)
xm = (np.arange(960) + 0.5) / 960 * 16 - 8
u = np.clip((xm + 0.6) / 3.0, 0, 1)
VEU = (0.9 * u * u * (3 - 2 * u))[None, :, None]


def ancora(t):
    return [a for t0, a in t0s if t0 <= t + 1e-6][-1]


def lum(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


cache = {}


def fundo(lote, f):
    d = U / "threejs" / "q3d" / f"{lote}_960x540"
    arqs = [p / f"f{f:05d}.png" for p in d.iterdir() if p.is_dir()] if d.exists() else []
    arqs = [a for a in arqs if a.exists()]
    if not arqs:
        return CEU, False
    k = tuple(arqs)
    if k not in cache:
        ims = [np.asarray(Image.open(a).convert("RGB"), dtype=np.float64) for a in arqs]
        im = np.maximum.reduce(ims)                         # duas tomadas em crossfade: o pior caso
        cache.clear()
        cache[k] = im * (1 - VEU) + CEU * VEU
    return cache[k], True


import av
_c = av.open(str(U / "renders" / "preview_yt0016_v7_960x540.mp4"))
VID = _c.decode(video=0)
_atual = [-1, None]


def quadro_video(k):
    while _atual[0] < k:
        _atual[1] = next(VID).to_ndarray(format="rgb24").astype(np.float64)
        _atual[0] += 1
    return _atual[1]


linhas = []
for lote, aid in PRIMEIRA.items():
    arq = U / f"contr_{lote}.txt"
    if arq.exists():
        base = ANC["ancoras"][aid]["t0"]
        linhas += [(base + float(ln.split(" ", 3)[2]), lote, base, ln) for ln in arq.read_text(encoding="utf-8").splitlines()]
linhas.sort()
res = []
for _, lote, base, ln in linhas:
    if True:
        p = ln.split(" ", 9)
        t, x0, y0, x1, y1, cor, op = float(p[2]), *map(float, p[3:7]), p[7], float(p[8])
        if op < 0.6 or y0 > 2.7:                            # o header fica fora (é o mesmo de sempre)
            continue
        im, tem3d = fundo(lote, int(round(t * 15)))
        px0, px1 = max(0, int((x0 + 8) / 16 * 960)), min(960, int((x1 + 8) / 16 * 960))
        py0, py1 = max(0, int((4.5 - y1) / 9 * 540)), min(540, int((4.5 - y0) / 9 * 540))
        if px1 - px0 < 9 or py1 - py0 < 9:                   # glifo isolado pequeno (=, 0, +): o antisserrilhado em 540p mede errado
            continue
        b = im[py0:py1, px0:px1].reshape(-1, 3)
        lb = lum(b)
        i95 = int(np.argsort(lb)[int(0.95 * (len(lb) - 1))])
        bg = b[i95]
        v = quadro_video(int(round((base + t) * 15)))[py0:py1, px0:px1].reshape(-1, 3)
        lt, l_b = float(np.percentile(lum(v), 99)), float(lb[i95])
        r = (max(lt, l_b) + 0.05) / (min(lt, l_b) + 0.05)
        res.append((r, base + t, ancora(base + t), p[9] if len(p) > 9 else "", tem3d, l_b))
por = {}
for it in res:
    por.setdefault(it[2], []).append(it)
n3 = [x for x in res if x[4]]
out = [f"contraste rótulo × fundo atrás dele (WCAG; fundo = quadro 3D puro + véu da CONTA, ou o céu): {len(res)} medições "
       f"({len(n3)} sobre 3D); abaixo de 4,5: {sum(1 for x in res if x[0] < 4.5)} ({sum(1 for x in n3 if x[0] < 4.5)} sobre 3D)", "",
       "mínimo por âncora:"]
for a in ANC["ordem"]:
    if a in por:
        r, t, _, nome, t3, l_b = min(por[a])
        out.append(f"{a:7s} {r:5.2f}:1  {'3D ' if t3 else 'céu'} ({int(t // 60)}:{t % 60:05.2f} {nome[:40]})")
out += ["", "abaixo de 4,5 (pior primeiro):"] + [f"{r:5.2f}:1  {int(t // 60)}:{t % 60:05.2f}  {a:6s} {'3D ' if t3 else 'céu'} fundo L={l_b:.3f}  {nome[:44]}"
                                               for r, t, a, nome, t3, l_b in sorted(res) if r < 4.5][:120]
(U / "log_contraste_v7.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out[:80]))
