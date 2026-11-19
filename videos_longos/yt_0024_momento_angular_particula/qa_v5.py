"""yt_0024 — auditorias novas do handoff v5 (rodam sobre os logs e os mp4 dos lotes; não alteram nada).

  VETOR   : conta as linhas `[audit] VETOR` de log_aud_<L>.txt (r⃗ da referência à partícula; T⃗/F⃗ para o furo/centro; p⃗ ∥ v⃗) → renders/vetor.txt
  BARRA   : coluna estreita de luminância alta que corre pelo quadro (a "varredura de luz" removida): em cada lote, compara a coluna de cada quadro com a
            mesma coluna 4 quadros antes e depois; um excesso estreito (≤ 14 colunas) e alto (> 14 níveis) que só existe naquele instante é falha → renders/barra.txt
  FLASH   : flash24.py (MathTex e, desde o v5, txt/selos) → renders/flash.txt

uso: python qa_v5.py [LOTE ...]   (sem argumentos: todos os lotes com mp4 em media_<L>/)"""
import re
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
ARQ = sys.argv[sys.argv.index("--arquivo") + 1] if "--arquivo" in sys.argv else None
if ARQ:
    sys.argv = sys.argv[:sys.argv.index("--arquivo")]
LOTES = [a for a in sys.argv[1:]] or ["PH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PS"]
R = U / "renders"
R.mkdir(exist_ok=True)


def mp4(l):
    if ARQ:
        return Path(ARQ)
    return U / f"media_{l}/videos/cena/540p15/{l}.mp4"


# ── VETOR ──
linhas, total = [], 0
for l in LOTES:
    f = U / f"log_aud_{l}.txt"
    if not f.exists():
        linhas.append(f"{l}: auditoria não rodada")
        continue
    ev = [x for x in f.read_text(encoding="utf-8", errors="replace").splitlines() if "VETOR" in x]
    total += len(ev)
    linhas.append(f"{l}: {len(ev)} eventos VETOR")
    linhas += [f"   {x.strip()[:150]}" for x in ev[:12]]
(R / "vetor.txt").write_text(f"AUDITORIA VETOR (handoff v5 §1.6): {total} eventos\n" + "\n".join(linhas) + "\n", encoding="utf-8")
print(f"VETOR: {total} eventos")

# ── BARRA ──
saida, n_bar = [], 0
for l in LOTES:
    f = mp4(l)
    if not f.exists():
        saida.append(f"{l}: sem mp4")
        continue
    c = av.open(str(f))
    fps = float(c.streams.video[0].average_rate)
    col = []                                           # luminância média de cada coluna (959) por quadro, descontada a mediana local (borda da mesa, texto fixo etc.)
    for fr in c.decode(video=0):
        g = fr.reformat(width=960, height=540, format="gray").to_ndarray().astype(np.float32)
        m = g.mean(axis=0)
        k = 41
        pad = np.pad(m, k // 2, mode="edge")
        med = np.array([np.median(pad[i:i + k]) for i in range(960)])
        col.append(m - med)
    col = np.array(col)
    ev = []
    for t in range(4, len(col) - 4):
        ref = np.maximum(col[t - 4], col[t + 4])
        ex = col[t] - ref                                 # só o que existe neste quadro e não 4 quadros antes/depois
        if ex.max() > 14:
            xs = np.nonzero(ex > 14)[0]
            if xs.max() - xs.min() <= 14:
                ev.append((t / fps, int(xs.mean()), float(ex.max())))
    # agrupa quadros consecutivos (a barra passa por ~6 quadros)
    grupos = []
    for e in ev:
        if grupos and e[0] - grupos[-1][-1][0] <= 0.2:
            grupos[-1].append(e)
        else:
            grupos.append([e])
    # a varredura removida andava ~128 px por quadro (960 px em 0,5 s): só conta como BARRA o que se MOVE (≥ 3 quadros, ≥ 150 px de percurso)
    grupos = [g for g in grupos if len(g) >= 3 and abs(g[-1][1] - g[0][1]) >= 150 and max(x[2] for x in g) >= 30]      # a faixa suave de fundo (_varre, ~18 níveis, atrás de tudo) não conta; a barra removida tinha ~180
    n_bar += len(grupos)
    saida.append(f"{l}: {len(grupos)} barras")
    saida += [f"   t={g[0][0]:.2f}–{g[-1][0]:.2f} s x≈{g[0][1]}→{g[-1][1]} px excesso máx {max(x[2] for x in g):.0f}" for g in grupos[:20]]
(R / "barra.txt").write_text(f"BARRA (coluna estreita de luminância alta): {n_bar} eventos\n" + "\n".join(saida) + "\n", encoding="utf-8")
print(f"BARRA: {n_bar} eventos")
