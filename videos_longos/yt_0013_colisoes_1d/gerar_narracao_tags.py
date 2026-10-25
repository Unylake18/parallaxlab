"""Gera narracao_tags.md (texto corrido com audio tags do ElevenLabs v4) a partir de narracao_sugestao.md.

Cada âncora ### vira um parágrafo; linhas que começam com "(" são notas de direção e não são faladas.
A tag só é escrita quando muda (vale até a próxima). Uso: uv run --no-sync python gerar_narracao_tags.py
"""
import re
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
TAG = {
    "H1": "[curious]", "H2": "[curious]", "H4": "[curious]", "A1": "[happy]", "A2": "[thoughtful]",
    "C01-5": "[thoughtful, emphatic]", "C01-9": "[thoughtful, emphatic]", "C01-10": "[curious]",
    "C02-1": "[curious]", "C02-3": "[curious]", "C02-5": "[thoughtful, emphatic]", "C02-7": "[curious]",
    "C03-1": "[curious]", "C03-3": "[curious]", "C03-6": "[thoughtful, emphatic]", "C03-7": "[thoughtful, emphatic]",
    "C04-1": "[curious]", "C04-5": "[curious]", "C05-1": "[curious]", "C05-5": "[curious]", "C05-7": "[thoughtful, emphatic]",
    "C06-1": "[curious]", "C06-4": "[curious]", "C06-8": "[curious]", "C06-10": "[thoughtful, emphatic]",
    "C06b-1": "[curious]", "C06b-5": "[excited]", "C07-6": "[thoughtful, emphatic]", "C08-1": "[curious]",
    "C08-2": "[curious]", "C08-4": "[curious]", "C08-6": "[curious]", "C08-7": "[excited]",
    "C08-8": "[thoughtful, emphatic]", "C09-1": "[curious]", "C09-3": "[curious]", "C10-1": "[thoughtful]",
    "C10-6": "[curious]", "C11-1": "[curious]", "C11-5": "[thoughtful, emphatic]", "C11-6": "[thoughtful, emphatic]",
    "C12-1": "[thoughtful]", "C12-6": "[thoughtful, emphatic]", "C12-7": "[thoughtful, emphatic]", "P1": "[curious]",
    "E1": "[calm, satisfied]", "E2": "[curious]", "E3": "[happy]",
}
PAUSA = {"C01-10"}                       # "Então... [short pause] o que está faltando?"

src = (AQUI / "narracao_sugestao.md").read_text(encoding="utf-8")
corpo = src.split("## Notas para a sincronização")[0]
blocos = re.findall(r"^### (\S+) — [^\n]*\n(.*?)(?=^### |^## |^---|\Z)", corpo, flags=re.M | re.S)
linhas, atual = [], None
for aid, txt in blocos:
    falas = [l.strip() for l in txt.strip().splitlines() if l.strip() and not l.strip().startswith("(")]
    if not falas:
        continue
    t = " ".join(falas)
    if aid in PAUSA and "..." in t:
        t = t.replace("... ", "... [short pause] ", 1)
    tag = TAG.get(aid, "[thoughtful]")
    if tag != atual:
        t, atual = f"{tag} {t}", tag
    linhas.append(t)
txt = "\n\n".join(linhas)
(AQUI / "narracao_tags.md").write_text(
    "# yt_0013 — narração com audio tags (sugestão v2.1, para gerar a voz)\n\n"
    "Fonte: `narracao_sugestao.md` (âncoras ### = parágrafos daqui, na mesma ordem); gerado por `gerar_narracao_tags.py`. "
    "Tags em inglês, uma por trecho, valendo até a próxima; não entram na legenda nem no SRT. Gerar só depois da confirmação do usuário.\n\n"
    "## Texto corrido (para gravação)\n\n" + txt + "\n", encoding="utf-8")
pal = len(re.sub(r"\[[^\]]*\]", "", txt).split())
print(f"parágrafos {len(linhas)} · palavras {pal} · {pal / 3.0 / 60:.1f}–{pal / 2.7 / 60:.1f} min")
print(dict(Counter(re.findall(r"\[[^\]]*\]", txt))))
