"""yt_0020 (copiado do yt_0019). Lê narracao_sugestao.md (v1.1 congelada) e grava ancoras.json com a régua NOMINAL do preview silencioso:
2,7 palavras/s, a fala começa 0,15 s depois da âncora; ini/fim acumulados e o instante de cada palavra (t), no mesmo formato que a voz gerará depois."""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
t = (AQUI / "narracao_sugestao.md").read_text(encoding="utf-8")
t = t[:t.rindex("## Números de conferência")]
VEL, INI, RESPIRO = 2.7, 0.15, 0.6
out, ordem, rel = {}, [], 0.0
for bloco in re.split(r"^### ", t, flags=re.M)[1:]:
    cab, *resto = bloco.split("\n")
    aid = cab.split(" — ")[0].strip()
    fala = " ".join(l for l in resto if l.strip() and not l.startswith(("---", "## ", "**")))
    fala = re.sub(r"\[[^\]]*\]", "", fala)
    pal = re.findall(r"\w+", fala.lower())
    n = len(pal)
    d = round(INI + n / VEL + RESPIRO, 2)
    out[aid] = {"palavras": n, "ini": round(rel, 4), "fim": round(rel + d, 4), "dur": d, "fala": " ".join(pal),
                "t": [round(INI + k / VEL, 3) for k in range(n)], "nominal": d}
    rel += d
    ordem.append(aid)
(AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "ancoras": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(sum(v["palavras"] for v in out.values()), "palavras;", round(rel / 60, 1), "min")
for a in ordem:
    print(a, out[a]["palavras"], out[a]["dur"])
