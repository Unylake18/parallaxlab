"""narracao_final_v4.md (Anexo A do handoff v5) → narracao_tags.md: texto corrido para a voz (um parágrafo por âncora, com as tags)
e a lista âncora → primeira frase (para a sincronia). Também grava ancoras_frases_v5.json."""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
t = (AQUI / "narracao_final_v4.md").read_text(encoding="utf-8")
t = t[:t.rindex("## Números de conferência")]
ancoras = []
for bloco in re.split(r"^### ", t, flags=re.M)[1:]:
    cab, *resto = bloco.split("\n")
    aid = cab.split(" — ")[0].strip()
    fala = " ".join(l.strip() for l in resto if l.strip() and not l.startswith(("---", "## ")))
    limpa = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", fala)).strip()
    frase = re.split(r"(?<=[.!?…:])\s+", limpa)[0]
    ancoras.append({"id": aid, "fala": fala, "limpa": limpa, "primeira": frase})

linhas = ["# yt_0016 — narração com tags (v4 final, handoff v5)", "",
          "Gerado por `fazer_tags.py` a partir de `narracao_final_v4.md`. Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`.", "",
          "## Texto corrido (para gravação)", ""]
for a in ancoras:
    linhas += [a["fala"], ""]
linhas += ["## Âncora → primeira frase (sincronia)", ""]
for a in ancoras:
    linhas.append(f"- **{a['id']}** — {a['primeira']}")
(AQUI / "narracao_tags.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
(AQUI / "ancoras_frases_v5.json").write_text(json.dumps(ancoras, ensure_ascii=False, indent=1), encoding="utf-8")
n = sum(len(re.findall(r"\w+", a["limpa"])) for a in ancoras)
c = sum(len(a["fala"]) + 2 for a in ancoras)
print(len(ancoras), "âncoras;", n, "palavras;", c, "caracteres;", round(n / 2.7 / 60, 1), "min a 2,7 p/s")
