"""Lê narracao_sugestao.md (congelada) e grava ancoras.json: palavras e duração nominal (2,7 palavras/s) de cada âncora."""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
t = (AQUI / "narracao_sugestao.md").read_text(encoding="utf-8")
t = t[:t.rindex("## Números de conferência")]
VEL = 2.7
out, ordem = {}, []
for bloco in re.split(r"^### ", t, flags=re.M)[1:]:
    cab, *resto = bloco.split("\n")
    aid = cab.split(" — ")[0].strip()
    fala = " ".join(l for l in resto if l.strip() and not l.startswith(("---", "## ")))
    fala = re.sub(r"\[[^\]]*\]", "", fala)
    n = len(re.findall(r"\w+", fala))
    out[aid] = {"palavras": n, "dur": round(n / VEL, 2)}
    ordem.append(aid)
(AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "ancoras": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(sum(v["palavras"] for v in out.values()), "palavras;", round(sum(v["dur"] for v in out.values()) / 60, 1), "min")
for a in ordem:
    print(a, out[a]["palavras"], out[a]["dur"])
