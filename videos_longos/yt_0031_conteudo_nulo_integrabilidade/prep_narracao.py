"""yt_0031 final §4: a partir de narracao.md (narração v2.3 fechada) grava narracao_tags.md (seção 2, com tags) e narracao_limpa.md (sem tags),
e confere que o texto corrido = a fala das 31 âncoras da seção 1 (mesmas palavras, na ordem)."""
import re
from pathlib import Path

U = Path(__file__).resolve().parent
t = (U / "narracao.md").read_text(encoding="utf-8")
corrido = t.split("## 2. Texto corrido (para gravação)")[1].strip()
pars = [p.strip() for p in corrido.split("\n\n") if p.strip()]
(U / "narracao_tags.md").write_text(
    "# yt_0031 · narração v2.3 com tags (ElevenLabs v4)\n\n"
    "Tags permitidas: [curious] [thoughtful] [surprised] [happy] [excited] [serious]; uma por parágrafo (o S2 tem duas).\n\n"
    "## Texto corrido (para gravação)\n\n" + "\n\n".join(pars) + "\n", encoding="utf-8")
limpos = [re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", p)).strip() for p in pars]
(U / "narracao_limpa.md").write_text("# yt_0031 · narração v2.3 sem tags (alinhamento e .srt)\n\n" + "\n\n".join(limpos) + "\n", encoding="utf-8")
sec1 = t.split("## 1. Narração por âncora")[1].split("## 2. Texto corrido")[0]
falas = []
for bloco in re.split(r"^### ", sec1, flags=re.M)[1:]:
    falas.append(" ".join(l.lstrip("> ") for l in bloco.split("\n") if l.startswith(">")))
w1 = re.findall(r"\w+", re.sub(r"\[[^\]]*\]", "", " ".join(falas)).lower())
w2 = re.findall(r"\w+", " ".join(limpos).lower())
tags = re.findall(r"\[([a-z ]+)\]", corrido)
print(f"{len(pars)} parágrafos; {len(falas)} âncoras; palavras seção1={len(w1)} corrido={len(w2)} iguais={w1 == w2}")
print("tags:", {x: tags.count(x) for x in sorted(set(tags))})
proib = [x for x in tags if x in ("slowly", "pause")]
print("tags proibidas:", proib or "nenhuma")
