"""yt_0030 · ferramenta de iteração: para cada hold > 6 s do holds_<rodada>.txt, a fala dentro do hold (palavras com o tempo na âncora)
e os gatilhos do lote vizinhos. uso: python holds_fala.py [rodada]"""
import json
import re
import sys
from pathlib import Path

from tempos import ANC_DADOS

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v2"
INFO = json.loads((U / "renders" / R / f"lotes_{R}.json").read_text(encoding="utf-8"))
INI = {k: v / 15 for k, v in INFO["inicio"].items()}
ORD = sorted(INI, key=INI.get)
txt = (U / "renders" / R / "qa" / f"holds_{R}.txt").read_text(encoding="utf-8")
for m in re.finditer(r"(\d+):(\d+\.\d+) · +(\d+\.\d+) s · (\S+) .*> 6 s", txt):
    t0 = int(m.group(1)) * 60 + float(m.group(2))
    d = float(m.group(3))
    lote = [l for l in ORD if INI[l] <= t0][-1]
    lt0 = t0 - INI[lote]
    log = (U / f"log_{lote}.txt").read_text(encoding="utf-8", errors="replace")
    anc = {a.group(1): float(a.group(2)) for a in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log)}
    print(f"\n== {m.group(1)}:{m.group(2)} · {d:.2f} s · {lote} t = {lt0:.2f}–{lt0 + d:.2f}")
    for aid, ta in anc.items():
        A = ANC_DADOS["ancoras"].get(aid)
        if not A:
            continue
        ws = [(ta + t, w) for t, w in zip(A["t"], A["fala"].split()) if lt0 - 0.5 <= ta + t <= lt0 + d + 0.3]
        if ws:
            print(f"   {aid}: " + " ".join(f"{w}" + (f"[{t:.1f}]" if i % 6 == 0 else "") for i, (t, w) in enumerate(ws)))
    for g in re.finditer(r"\[gatilho\] (\S+) +([0-9.]+)s \(alvo[^)]*\) (.+)", log):
        tg = anc.get(g.group(1), 0) + float(g.group(2))
        if lt0 - 4 <= tg <= lt0 + d + 2:
            print(f"   gat {tg:7.2f} {g.group(1)} «{g.group(3)}»")
