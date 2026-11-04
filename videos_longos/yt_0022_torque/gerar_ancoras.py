"""yt_0021 (copiado do yt_0019). Lê narracao_sugestao.md (narração v1 congelada = Anexo A do handoff) e grava ancoras.json com o tempo NOMINAL de cada
âncora: a fala começa 0,15 s depois da tela, 2,7 palavras/s, e 0,35 s de respiro no fim. `t` = início de cada palavra (relativo à âncora), para os gatilhos."""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
t = (AQUI / "narracao_sugestao.md").read_text(encoding="utf-8")
t = t[:t.rindex("## Conferência numérica")]
VEL, LEAD0, RESP = 2.7, 0.15, 0.35
out, ordem, ini = {}, [], 0.0
for bloco in re.split(r"^### ", t, flags=re.M)[1:]:
    cab, *resto = bloco.split("\n")
    aid = cab.split(" — ")[0].strip()
    fala = " ".join(l for l in resto if l.strip() and not l.startswith(("---", "## ", "**")))
    fala = re.sub(r"\[[^\]]*\]", "", fala)
    pal = re.findall(r"\w+", fala.lower())
    n = len(pal)
    d = round(LEAD0 + n / VEL + RESP, 2)
    out[aid] = {"palavras": n, "ini": round(ini, 4), "fim": round(ini + d, 4), "dur": d, "nominal": d, "fala": " ".join(pal),
                "t": [round(LEAD0 + k / VEL, 3) for k in range(n)]}
    ordem.append(aid)
    ini += d
(AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "ancoras": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(sum(v["palavras"] for v in out.values()), "palavras;", round(ini / 60, 2), "min")
for a in ordem:
    print(a, out[a]["palavras"], out[a]["dur"])
