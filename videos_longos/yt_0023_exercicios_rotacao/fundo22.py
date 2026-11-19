"""yt_0022 v6 — QA do fundo de estrelas: deslocamento horizontal por quadro (correlação de fase por blocos) em todo o vídeo.
Aprovado: nenhum quadro com deslocamento ≥ −0,3 px (parado/para a direita) em sequência > 2 quadros, e nenhum salto > 1,5× a mediana local,
inclusive nas fronteiras de lote. Medida em px de 960 de largura (o master 1080p é reduzido a 960).
uso: python fundo22.py ARQUIVO.mp4 [saida.txt]"""
import sys
from pathlib import Path

import av
import numpy as np
from scipy.ndimage import gaussian_filter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

U = Path(__file__).resolve().parent
arq = Path(sys.argv[1])
saida = Path(sys.argv[2]) if len(sys.argv) > 2 else U / "renders" / "fundo.txt"
c = av.open(str(arq))
s = c.streams.video[0]
s.thread_type = "AUTO"
fps = float(s.average_rate)
# blocos de estrelas puras: faixas laterais e inferior (sem conteúdo): 4 blocos de 160×90 (em 480×270) nos cantos/rodapé
BL = [(y, y + 90, x, x + 120) for y in (0, 90, 180) for x in (0, 120, 240, 360)]   # (y0, y1, x0, x1) em 480×270; rodapé e meio inferior
ant, dx = None, []
han = np.outer(np.hanning(1), np.hanning(1))


def desloca(a, b, vmax=14):
    """Melhor deslocamento em x com |dx| ≥ 0,8 px (o conteúdo estático, dx = 0, é ignorado); devolve (dx, força)."""
    a = a - a.mean()
    b = b - b.mean()
    F = np.fft.rfft2(a) * np.conj(np.fft.rfft2(b))
    F /= np.abs(F) + 1e-9
    r = np.fft.irfft2(F, s=a.shape)
    n = a.shape[1]
    perfil = r.max(axis=0)                                  # melhor linha para cada dx (y livre: parallax vertical nulo, mas tolera)
    best, pico = 0.0, 0.0
    for k in list(range(-vmax, -0) ) + list(range(1, vmax + 1)):
        for fr_ in (0.0,):
            p = perfil[k % n]
            if p > pico:
                r0, r1, r2 = perfil[(k - 1) % n], perfil[k % n], perfil[(k + 1) % n]
                den = r0 - 2 * r1 + r2
                best, pico = k + (0.5 * (r0 - r2) / den if abs(den) > 1e-9 else 0.0), p
    return best, float(pico)


for fr in c.decode(video=0):
    g = fr.reformat(width=480, height=270, format="gray").to_ndarray().astype(np.float32)
    g = np.clip(g - gaussian_filter(g, 2.0), 0, None)        # top-hat: só pontos pequenos (estrelas); realça contra texto/formas grandes
    if ant is not None:
        v = []
        for (y0, y1, x0, x1) in BL:
            bl = g[y0:min(y1, 270), x0:x1]
            bl0 = ant[y0:min(y1, 270), x0:x1]
            if bl.shape[0] < 20:
                continue
            d, p = desloca(bl, bl0)
            if p > 0.10 and abs(d) >= 1.0:
                v.append(d * 2.0)           # 480 → 960 px
        dx.append(float(np.median(v)) if v else np.nan)
    else:
        dx.append(np.nan)
    ant = g
dx = np.array(dx)
VMAX_ESTRELA = 6.0 * 15 / fps * (960 / 960)   # px/quadro a 960: a camada mais rápida anda ≈5; > 6 é conteúdo em movimento rápido (câmera/zoom), não estrela
dx[np.abs(dx) > VMAX_ESTRELA * 1.0] = np.nan
ok = ~np.isnan(dx)
med = float(np.nanmedian(dx))
lin = [f"arquivo {arq.name}: {len(dx)} quadros a {fps:g} fps; deslocamento mediano {med:.2f} px/quadro (a 960 px; negativo = esquerda)"]
# paradas/inversões
bad, i = [], 0
ruim = lambda k: (not ok[k]) or dx[k] > -0.3
lim_nan = int(1.0 * fps)          # sem deslocamento medido (estrelas paradas) ou para a direita
while i < len(dx):
    if i > 0 and ruim(i):
        j = i
        while j < len(dx) and ruim(j):
            j += 1
        if (j - i > 3 and np.isfinite(dx[i:j]).any()) or j - i > lim_nan:
            bad.append((i, j))
        i = j
    else:
        i += 1
# saltos
pulos = []
w = max(5, int(fps))
for i in range(w, len(dx) - w):
    if not ok[i]:
        continue
    loc = np.nanmedian(dx[i - w:i + w])
    if loc < -0.3 and abs(dx[i]) > 1.5 * abs(loc) + 0.8:
        pulos.append(i)
lin.append(f"trechos sem deslocamento à esquerda por > 3 quadros (parado/para a direita/não medido): {len(bad)}")
for i, j in bad[:40]:
    lin.append(f"  parado/volta  {i / fps:8.2f}s – {j / fps:8.2f}s  ({j - i} quadros, dx médio {np.nanmean(dx[i:j]) if np.isfinite(dx[i:j]).any() else float('nan'):.2f})")
lin.append(f"saltos > 1,5× a mediana local: {len(pulos)} quadros")
for i in pulos[:40]:
    lin.append(f"  salto  {i / fps:8.2f}s  dx {dx[i]:.2f} (local {np.nanmedian(dx[i - w:i + w]):.2f})")
lin.append(f"NaN (sem estrela medida: conteúdo em movimento rápido ou 3D opaco cobrindo o fundo): {int((~ok).sum())} quadros")
import json
anc = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
fr_ok = 0
for k in ("A1", "T1-1", "T2-1", "T3-1", "T4-1", "T5-1", "T6-1", "S1"):
    i = int(round(anc[k]["ini"] * fps))
    jan = dx[max(0, i - 8):i + 9]
    jan = jan[np.isfinite(jan)]
    ant_ = dx[max(0, i - 8):i]
    dep_ = dx[i:i + 9]
    ant_, dep_ = ant_[np.isfinite(ant_)], dep_[np.isfinite(dep_)]
    cont = len(ant_) >= 3 and len(dep_) >= 3 and np.median(ant_) < -0.3 and abs(np.median(ant_) - np.median(dep_)) <= 0.4
    fr_ok += int(cont)
    lin.append(f"  fronteira {k:5s} {anc[k]['ini']:7.2f}s: dx {jan.min() if len(jan) else float('nan'):.2f}…{jan.max() if len(jan) else float('nan'):.2f} ({len(jan)} medidas) {'contínua' if cont else 'FALHA'}")
lin.append(f"fronteiras de lote contínuas: {fr_ok} de 8")
saida.write_text("\n".join(lin) + "\n", encoding="utf-8")
print("\n".join(lin[:12]))
np.save(saida.with_suffix(".npy"), dx)
