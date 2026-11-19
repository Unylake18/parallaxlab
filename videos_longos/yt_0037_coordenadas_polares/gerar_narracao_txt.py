"""yt_0037 final: gera narracao_tags.md (texto corrido com tags [ ] do ElevenLabs v4, um parágrafo por âncora) e narracao_limpa.md (sem tags)
a partir de narracao_final_v3.md (Anexo A: as linhas '> ...' de cada '### ÂNCORA')."""
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
t = (AQUI / "narracao_final_v3.md").read_text(encoding="utf-8")
t = t[t.index("## Anexo A"):t.index("## Anexo B")]
pars = []
for bloco in re.split(r"^### ", t, flags=re.M)[1:]:
    cab, *resto = bloco.split("\n")
    if cab.startswith("Tempo por"):
        continue
    fala = " ".join(l[1:].strip() for l in resto if l.startswith(">"))
    pars.append(re.sub(r"\s+", " ", fala).strip())
(AQUI / "narracao_tags.md").write_text(
    "# yt_0037 · narração final v3.1 com tags (ElevenLabs v4)\n\nUma tag por parágrafo (S2 tem duas), sem [slowly] e sem [pause]. Fonte: narracao_final_v3.md (Anexo A).\n\n"
    "## Texto corrido (para gravação)\n\n" + "\n\n".join(pars) + "\n", encoding="utf-8")
(AQUI / "narracao_limpa.md").write_text(
    "# yt_0037 · narração final v3.1 limpa (sem tags; alinhamento e .srt)\n\n" + "\n\n".join(re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", p)).strip() for p in pars) + "\n",
    encoding="utf-8")
n = sum(len(re.findall(r"\w+", re.sub(r"\[[^\]]*\]", "", p))) for p in pars)
print(len(pars), "parágrafos;", n, "palavras (tokens \w+);", "teta sem acento:", len(re.findall(r"\bteta\b", " ".join(pars), flags=re.I)))
