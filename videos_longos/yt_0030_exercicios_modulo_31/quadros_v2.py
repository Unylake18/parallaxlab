"""yt_0030 · ferramenta de iteração: quadros (960×540) de lotes em instantes dados por gatilho. uso: python quadros_v2.py SAIDA LOTE:ANCORA:FRASE:DT ..."""
import re
import sys
from pathlib import Path

import av

U = Path(__file__).resolve().parent
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
for n, arg in enumerate(sys.argv[2:]):
    lote, aid, frase, dt = arg.split(":")
    log = (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")
    a = {m.group(1): float(m.group(2)) for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log)}
    m = re.search(r"\[gatilho\] %s +([0-9.]+)s \(alvo[^)]*\) %s" % (re.escape(aid), re.escape(frase)), log)
    t = a[aid] + float(m.group(1)) + float(dt)
    c = av.open(str(U / f"media_{lote}/videos/cena/540p15/{lote}.mp4"))
    q = round(t * 15)
    for i, fr in enumerate(c.decode(video=0)):
        if i >= q:
            break
    c.close()
    fr.to_image().save(out / f"q{n:02d}_{lote}_{aid}.png")
    print(out / f"q{n:02d}_{lote}_{aid}.png", f"t={t:.2f}")
