"""python medir_parado.py video.mp4 [limite_s] → trechos em que a imagem fica parada.

Duas medidas (480×270, cinza):
- v4/v5 · quadro a quadro: "parado" = diferença máxima < 10/255 em 99,95% dos pixels em relação ao quadro anterior;
- v6 (a do handoff) · por segundo: "parado" = diferença MÉDIA < 0,3 (escala 0–255) entre o quadro e o de 1 s antes.
Lista os trechos mais longos que o limite (padrão 4 s) e as contagens > 6 s e > 8 s (meta v6: zero > 8 s; no máximo 4 entre 6 e 8 s)."""
import sys

import av
import numpy as np

vid = sys.argv[1]
lim = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
c = av.open(vid)
fps = float(c.streams.video[0].average_rate)
janela = round(fps)
hist, parado, parado6, i = [], [], [], 0
for fr in c.decode(video=0):
    g = np.asarray(fr.to_image().convert("L").resize((480, 270)), dtype=np.int16)
    if hist:
        d = np.abs(g - hist[-1])
        parado.append(np.mean(d > 10) < 0.0005)
    if len(hist) >= janela:
        parado6.append(float(np.mean(np.abs(g - hist[-janela]))) < 0.3)
    else:
        parado6.append(False)
    hist.append(g)
    if len(hist) > janela:
        hist.pop(0)
    i += 1


def trechos(flags, desloc):
    runs, ini = [], None
    for k, p in enumerate(flags + [False]):
        if p and ini is None:
            ini = k
        if not p and ini is not None:
            runs.append(((ini + desloc) / fps, (k + desloc) / fps))
            ini = None
    return runs


r5 = trechos(parado, 1)
# v6: um quadro "parado" diz que o último 1 s não mudou → o trecho começa 1 s antes do primeiro quadro marcado
r6 = [(max(0.0, a - 1.0), b) for a, b in trechos(parado6, 0)]
for nome, runs in (("v5", r5), ("v6", r6)):
    longos = [(a, b) for a, b in runs if b - a > lim]
    for a, b in longos:
        print(f"[parado {nome}] {a:7.1f}–{b:7.1f} s ({b - a:4.1f} s)  {int(a // 60)}:{a % 60:04.1f}" + ("  > 8 s" if b - a > 8 else "  > 6 s" if b - a > 6 else ""))
    print(f"[parado {nome}] {len(longos)} trechos > {lim:g} s; {sum(1 for a, b in runs if 6 < b - a <= 8)} entre 6 e 8 s; "
          f"{sum(1 for a, b in runs if b - a > 8)} > 8 s; duração {i / fps:.1f} s")
