"""yt_0031 · parado ≤ 3 s: lê `[play] k t0 dur +extra` e `[espera] k dur_play W t` dos logs e acumula em ritmo31.json quanto esticar a animação
anterior a cada espera longa: extra += min(W − 2,2 s; 2 × duração; 4 s), só para animações de ≥ 0,4 s. uso: python ritmo31.py [LOTE ...]"""
import json
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
ARQ = U / "ritmo31.json"
rit = json.loads(ARQ.read_text(encoding="utf-8")) if ARQ.exists() else {}
LOTES = sys.argv[1:] or ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PB7", "PB8", "PB9", "PS"]
for L in LOTES:
    t = (U / f"log_seco_{L}.txt").read_text(encoding="utf-8", errors="ignore")
    plays = {int(k): float(d) for k, _, d, _ in re.findall(r"\[play\] (\d+) ([\d.]+) ([\d.]+) \+([\d.]+)", t)}
    base = {int(k): float(d) - float(x) for k, _, d, x in re.findall(r"\[play\] (\d+) ([\d.]+) ([\d.]+) \+([\d.]+)", t)}
    r = rit.setdefault(L, {})
    n = 0
    for k, dur, W, _ in re.findall(r"\[espera\] (\d+) ([\d.]+) ([\d.]+) ([\d.]+)", t):
        k, W = int(k), float(W)
        b = base.get(k, 0.0)
        if b < 0.4 or W < 2.9:
            continue
        ja = r.get(str(k), 0.0)
        add = min(W - 2.2, max(0.0, 2 * b - ja), 4.0 - ja)
        if add > 0.05:
            r[str(k)] = round(ja + add, 3)
            n += 1
    print(L, "ajustes:", n, "total esticado:", round(sum(r.values()), 1), "s")
ARQ.write_text(json.dumps(rit, indent=1), encoding="utf-8")
