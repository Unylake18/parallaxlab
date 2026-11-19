"""yt_0032 · QA: cada trecho de renders/v1/qa/parado_v1.txt → lote, âncora, instante no lote e o gatilho seguinte (para decidir o passo que falta)."""
import json
import re
from pathlib import Path

U = Path(__file__).resolve().parent
ini = json.loads((U / "renders/v1/lotes_v1.json").read_text())["inicio"]
L = sorted(ini.items(), key=lambda x: x[1])
for ln in (U / "renders/v1/qa/parado_v1.txt").read_text(encoding="utf-8").splitlines()[1:]:
    a, b = [float(x) for x in re.findall(r"([\d.]+)–\s*([\d.]+)", ln)[0]]
    lote, q0 = [x for x in L if x[1] / 15 <= a][-1]
    ta, tb = a - q0 / 15, b - q0 / 15
    log = (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="ignore")
    an = [(m.group(1), float(m.group(2))) for m in re.finditer(r"\[ancora\] (\S+) ([\d.]+)", log)]
    aid, a0 = [x for x in an if x[1] <= ta + 0.01][-1]
    g = [(float(m.group(1)), m.group(2)) for m in re.finditer(r"\[gatilho\] " + re.escape(aid) + r"\s+([\d.]+)s .*?\) (.*)", log)]
    prox = [x for x in g if x[0] + a0 >= tb - 0.5]
    print(f"{lote:4s} {aid:5s} {ta:6.1f}-{tb:6.1f} ({tb - ta:4.1f}s) próximo: {prox[0][1] if prox else '(fim da âncora)'}")
