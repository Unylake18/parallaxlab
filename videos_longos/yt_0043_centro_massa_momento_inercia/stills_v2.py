"""yt_0043 · lista de stills do preview v2: os 23 alvos (marcas) + um still logo depois de cada degrau novo (D1–D9). Saída: stills_v2.txt (LOTE T)."""
import re
from pathlib import Path
A = Path(__file__).resolve().parent
NOVOS = ["C2.6b", "C2.7b", "C2.7c", "C2.8a", "C2.8b", "C2.8c", "C2.8d", "C6.2b", "C7.9b", "C7.12a", "C7.12b", "C9.5b", "C9.6a", "C9.13b", "C9.14a",
         "C10.4b", "C10.5a", "C10.19b", "C10.20a"]
out, marc = [], []
for l in ["PH", "PA", "PB1", "PB2", "PB3", "PB4", "PS"]:
    L = (A / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace").splitlines()
    for i, x in enumerate(L):
        m = re.match(r"\[marca\] (\S+) ([\d.]+)", x)
        if m:
            marc.append((l, float(m.group(2)), "marca:" + m.group(1)))
        m = re.match(r"\[degrau\] (\S+) (\S+)\s+([\d.]+)\s+([\d.]+) (\S+) ::", x)
        if m and m.group(5) in NOVOS:
            ta, tl = float(m.group(3)), float(m.group(4))
            off = tl - ta
            for y in L[i + 1:i + 12]:
                p = re.match(r"\[pena\] \S+ \S+\s+([\d.]+)s", y)
                if p:
                    out.append((l, round(float(p.group(1)) + off + 0.1, 2), "degrau:" + m.group(5)))
                    break
            else:
                out.append((l, round(tl + 1.5, 2), "degrau:" + m.group(5)))
todos = marc + out
(A / "stills_v2.txt").write_text("\n".join(f"{l} {t} {n}" for l, t, n in todos), encoding="utf-8")
print(len(marc), "marcas;", len(out), "degraus novos")
