"""yt_0030 · handoff final §6: fundo violeta + grade em todos os lotes → qa/fundo.txt. Para cada lote, um quadro a cada 10 s:
  · violeta: fração do quadro igual ao fundo violeta liso (|Δ| ≤ 10 por canal) e cor mediana × cor do PNG liso;
  · grade: fração de pixels levemente acima do fundo (Δ de 4 a 60, sem saturar): as linhas finas da grade que nasce dos eixos.
uso: python qa_fundo.py [540|1080]"""
import sys
from pathlib import Path

import av
import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
ROOT = U.parents[1]
RES = sys.argv[1] if len(sys.argv) > 1 else "540"
LOTES = ["PH", "PD1", "PD2", "PD3", "PD3B", "PD4", "PD5", "PA1", "PA2", "PA4", "PA3", "PS"]
W, H, PASTA, FPS = (960, 540, "540p15", 15) if RES == "540" else (1920, 1080, "1080p30", 30)
F = np.asarray(Image.open(ROOT / f"assets/calculo/fundo_calculo_violeta_liso_{W}x{H}.png").convert("RGB"), np.int16)
cor_f = np.median(F.reshape(-1, 3), axis=0)
L = [f"yt_0030 · fundo ({RES}p): violeta liso (mediana do PNG {cor_f.astype(int).tolist()}) + grade", ""]
ruins = 0
for lote in LOTES:
    arq = U / (f"media_{lote}" if RES == "540" else f"media1080_{lote}") / "videos" / "cena" / PASTA / f"{lote}.mp4"
    c = av.open(str(arq))
    vio, gra, med, n = [], [], [], 0
    for i, fr in enumerate(c.decode(video=0)):
        if i % (10 * FPS):
            continue
        a = fr.to_ndarray(format="rgb24").astype(np.int16)
        d = a - F
        igual = (np.abs(d).max(axis=2) <= 10)
        leve = (d.min(axis=2) >= 4) & (d.max(axis=2) <= 60)
        vio.append(igual.mean())
        gra.append(leve.mean())
        med.append(np.median(a.reshape(-1, 3), axis=0))
        n += 1
    c.close()
    m = np.median(np.array(med), axis=0)
    ok = min(vio) >= 0.35 and np.abs(m - cor_f).max() <= 12 and max(gra) > 0.002
    ruins += not ok
    L.append(f"  {lote:5s} {n:3d} quadros · igual ao violeta liso {min(vio):.0%}–{max(vio):.0%} · mediana {m.astype(int).tolist()} · "
             f"grade em {sum(g > 0.002 for g in gra)}/{n} quadros (até {max(gra):.1%}) → {'OK' if ok else 'VER'}")
L += ["", f"resumo: {len(LOTES) - ruins}/{len(LOTES)} lotes com violeta + grade"]
(U / "qa").mkdir(exist_ok=True)
(U / "qa" / f"fundo_{RES}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
