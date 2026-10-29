"""Gera narracao_tags.md (texto corrido com audio tags do ElevenLabs v4) a partir de narracao_sugestao.md (v5.3).

Cada âncora ### vira um parágrafo, na mesma ordem. As tags já vêm no texto da v5.3; um parágrafo sem tag herda a anterior, e a tag
é escrita em todo parágrafo (cada bloco da API é uma chamada separada e não herda o tom do bloco anterior). Sem tags de ritmo lento. Uso (na raiz do repositório):
    uv run --no-sync python videos_longos/yt_0015_momento_impulso/gerar_narracao_tags.py
"""
import re
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
src = (AQUI / "narracao_sugestao.md").read_text(encoding="utf-8")
corpo = src.split("## HOOK", 1)[1].split("## Números de conferência", 1)[0]
blocos = re.findall(r"^### (\S+) — [^\n]*\n(.*?)(?=^### |^## |^---|\Z)", corpo, flags=re.M | re.S)
linhas, atual = [], None
for aid, txt in blocos:
    falas = [l.strip() for l in txt.strip().splitlines() if l.strip() and not l.strip().startswith(">")]
    if not falas:
        continue
    t = " ".join(falas)
    m = re.match(r"^(\[[^\]]+\])\s*", t)
    tag = m.group(1) if m else atual
    t = t[m.end():] if m else t
    if tag:                                  # tag em todo parágrafo: cada bloco da API começa com o tom certo
        t, atual = f"{tag} {t}", tag
    linhas.append(t)
txt = "\n\n".join(linhas)
assert "slow" not in txt.lower(), "nada de [slowly] / devagar"
cab = ("# yt_0015 — narração com audio tags (v5.3, para gerar a voz)\n\n"
       "Fonte: `narracao_sugestao.md` (âncoras ### = parágrafos daqui, na mesma ordem); gerado por `gerar_narracao_tags.py`. "
       "Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`. Tags em inglês, valendo até a próxima; não entram na legenda nem no SRT.\n\n"
       "## Texto corrido (para gravação)\n\n")
(AQUI / "narracao_tags.md").write_text(cab + txt + "\n", encoding="utf-8")
sem_tags = re.sub(r"\[[^\]]*\]", "", txt)
pal = len(sem_tags.split())
print(f"parágrafos {len(linhas)} · palavras {pal} · {pal / 3.0 / 60:.1f}–{pal / 2.6 / 60:.1f} min · caracteres {len(txt)}")
print(dict(Counter(re.findall(r"\[[^\]]*\]", txt))))
