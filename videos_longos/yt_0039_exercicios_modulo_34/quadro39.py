"""yt_0039 · quadros para conferência: python quadro39.py LOTE "frase do gatilho" [+dt] [saida.png] → o quadro do media_<LOTE> no instante
do gatilho (log_<LOTE>.txt) + dt s, em resolução cheia do preview (960×540), em renders/<RODADA>/qa/q/."""
import os
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RV = os.environ.get("RODADA", "v2")
lote, frase = sys.argv[1], sys.argv[2]
dt = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
log = (AQUI / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")
anc, t = {}, None
cur = None
for ln in log.splitlines():
    m = re.match(r"\[ancora\] (\S+) ([\d.]+)", ln)
    if m:
        anc[m.group(1)] = float(m.group(2))
        continue
    m = re.match(r"\[gatilho\] (\S+)\s+([\d.]+)s .*\) (.*)$", ln)
    if m and frase in m.group(3):
        t = anc.get(m.group(1), 0.0) + float(m.group(2))
        break
    m = re.match(r"\[marca\] (\S+) ([\d.]+)", ln)
    if m and frase == m.group(1):
        t = float(m.group(2))
        break
assert t is not None, f"gatilho/marca não achado: {frase}"
t += dt
out = AQUI / "renders" / RV / "qa" / "q"
out.mkdir(parents=True, exist_ok=True)
nome = sys.argv[4] if len(sys.argv) > 4 else f"{lote}_{re.sub(r'[^a-z0-9]+', '_', frase.lower())[:30]}_{t:07.2f}.png"
src = AQUI / f"media_{lote}" / "videos" / "cena" / "540p15" / f"{lote}.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1", str(out / nome)], check=True)
print(out / nome)
