"""PAUSAS: trechos parados de cada lote (quadros consecutivos quase idênticos, reduzidos a 240×135 em cinza; um quadro é "parado" quando
menos de 10 pixels mudam mais de 6 níveis em relação ao anterior). Lista todo trecho ≥ LIM s (padrão 4) com a âncora em que ele cai
(log_<lote>.txt: linhas [ancora]).
uso: python parados.py PH P1 P2 ... [--lim 4]"""
import re
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
args = sys.argv[1:]
LIM = float(args[args.index("--lim") + 1]) if "--lim" in args else 4.0
lotes = [a for a in args if not a.startswith("--") and not re.fullmatch(r"[0-9.]+", a)]


def trechos(arq):
    c = av.open(str(arq))
    st = c.streams.video[0]
    fps = float(st.average_rate)
    ant, run0, runs, n = None, None, [], 0
    for i, fr in enumerate(c.decode(st)):
        g = np.asarray(fr.to_image().convert("L").resize((240, 135)), dtype=np.int16)
        if ant is not None:
            parado = int((np.abs(g - ant) > 6).sum()) < 10
            if parado and run0 is None:
                run0 = i - 1
            elif not parado and run0 is not None:
                runs.append((run0 / fps, (i - 1) / fps))
                run0 = None
        ant = g
        n = i
    if run0 is not None:
        runs.append((run0 / fps, n / fps))
    return runs


total = 0
for lote in lotes:
    anc = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace"))]
    longos = [(a, b) for a, b in trechos(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4") if b - a >= LIM]
    total += len(longos)
    for a, b in longos:
        aid = [k for k, t in anc if t <= a + 1e-6][-1] if anc else "?"
        print(f"[pausa] {lote} {aid} {a:6.1f}–{b:6.1f} s ({b - a:.1f} s)")
print(f"[pausa] total de trechos parados ≥ {LIM:g} s: {total}")
