"""yt_0022: agrupa as linhas [audit] dos log_aud_<L>.txt por (lote, categoria, par de objetos), ignorando o instante e as coordenadas: a lista única do portão.
uso: python agrupar_portao.py → renders/portao_unico.txt"""
import re
from collections import defaultdict
from pathlib import Path

U = Path(__file__).resolve().parent
LOTES = ["PH", "PA", "PT1", "PT2", "PT3", "PT4", "PT5", "PT6", "PS"]
g = defaultdict(lambda: [0, 1e9, 0])
for l in LOTES:
    f = U / f"log_aud_{l}.txt"
    if not f.exists():
        continue
    for ln in f.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"\[audit\]\s+([0-9.]+)s (.*)", ln)
        if not m:
            continue
        t, resto = float(m.group(1)), m.group(2)
        cat = re.match(r"([A-ZÇÃÕÉÍÂÊÓÚ ]+?)(?= '|\s\(|\s[a-z0-9]|$)", resto)
        cat = cat.group(1).strip() if cat else resto[:20]
        chave = (l, cat, re.sub(r"[-+]?\d+\.\d+", "N", resto[len(cat):])[:110])
        e = g[chave]
        e[0] += 1
        e[1] = min(e[1], t)
        e[2] = max(e[2], t)
linhas = [f"{l:4s} {c:20s} x{n:<5d} {a:7.1f}–{b:7.1f}s {d}" for (l, c, d), (n, a, b) in sorted(g.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[1][1]))]
(U / "renders").mkdir(exist_ok=True)
(U / "renders" / "portao_unico.txt").write_text("\n".join(linhas) + "\n", encoding="utf-8")
print(len(linhas), "itens únicos")
