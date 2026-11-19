import re, sys
from collections import Counter
from pathlib import Path
U = Path(__file__).resolve().parent
def cont(f):
    c = Counter()
    if not f.exists(): return c
    for ln in f.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.search(r"\[audit\]\s+(?:[0-9.]+s\s+)?([A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9 ]+?)(?:\s{1,}|$)['(a-z0-9]", ln + " x")
        if m: c[m.group(1).strip()] += 1
    return c
out = ["TABELA ANTES (v4) × DEPOIS (v8): linhas [audit] da passada de auditoria, por classe e lote", ""]
for l in ("PB3", "PB4", "PB6"):
    a, d = cont(U / "renders/antes_v4" / f"log_aud_{l}.txt"), cont(U / f"log_aud_{l}.txt")
    out.append(f"{l}: total antes {sum(a.values())} → depois {sum(d.values())}")
    for k in sorted(set(a) | set(d), key=lambda k: -(a[k] + d[k])):
        out.append(f"   {k:28s} {a[k]:6d} → {d[k]:6d}")
    out.append("")
t = "\n".join(out); print(t); (U / "renders/antes_depois.txt").write_text(t, encoding="utf-8")
