"""Gera narracao_tags.md (texto corrido com audio tags do ElevenLabs v4) a partir de narracao_sugestao.md (v1.2.1).

Cada âncora ### vira um parágrafo; linhas que começam com ">" são notas de animação e não são faladas.
A tag só é escrita quando muda (vale até a próxima). Sem tags de ritmo lento (decisão do usuário). Uso:
    uv run --no-sync python videos_longos/yt_0014_colisoes_2d/gerar_narracao_tags.py
"""
import re
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
C, T, E, X, H, K = "[curious]", "[thoughtful]", "[thoughtful, emphatic]", "[excited]", "[happy]", "[calm, satisfied]"
TAG = {
    "H1": C, "H2": C, "H3": C, "A1": H, "A2": T,
    "C01-1": T, "C01-2": T,
    "C02-1": T, "C02-2": T, "C02-3": E, "C02-4": C,
    "C03-1": T, "C03-2": T, "C03-3": E,
    "C04-1": C, "C04-2": T, "C04-3": T, "C04-4": C, "C04-5": T, "C04-6": E, "C04-7": T, "C04-8": E,
    "C05-1": C, "C05-2": T, "C05-3": T,
    "C06-1": C, "C06-2": T, "C06-3": T, "C06-4": C,
    "C07-1": T, "C07-2": E, "C07-3": T, "C07-4": E, "C07-5": T, "C07-6": T,
    "C08-1": C, "C08-2": T, "C08-3": T, "C08-4": C, "C08-5": X,
    "C09-1": C, "C09-2": T, "C09-3": T, "C09-4": T, "C09-5": E, "C09-6": X, "C09-7": C,
    "C10-1": C, "C10-2": T, "C10-3": E,
    "C11-1": C, "C11-2": T, "C11-3": T, "C11-4": T, "C11-5": E,
    "C12-1": C, "C13-1": T, "C13-2": E,
    "C14-1": T, "C14-2": C, "C14-3": T, "C14-4": C, "C14-5": T,
    "E1": K, "E2": H,
}
# pausa curta logo depois da primeira reticência (ou do trecho dado) do parágrafo
PAUSA = {"H3": "Por quê?", "C07-2": "na vida...", "C09-5": "às duas pontas..."}

src = (AQUI / "narracao_sugestao.md").read_text(encoding="utf-8")
corpo = src.split("## HOOK", 1)[1].split("## Orçamento de tempo", 1)[0]
blocos = re.findall(r"^### (\S+) (?:\(opcional\) )?— [^\n]*\n(.*?)(?=^### |^## |^---|\Z)", corpo, flags=re.M | re.S)
linhas, atual, faltam = [], None, []
for aid, txt in blocos:
    falas = [l.strip() for l in txt.strip().splitlines() if l.strip() and not l.strip().startswith(">")]
    if not falas:
        continue
    t = " ".join(falas)
    if aid in PAUSA and PAUSA[aid] in t:
        t = t.replace(PAUSA[aid], PAUSA[aid] + " [short pause]", 1)
    if aid not in TAG:
        faltam.append(aid)
    tag = TAG.get(aid, T)
    if tag != atual:
        t, atual = f"{tag} {t}", tag
    linhas.append(t)
txt = "\n\n".join(linhas)
assert "slow" not in txt.lower(), "nada de [slowly] / devagar"
cab = ("# yt_0014 — narração com audio tags (v1.2.1, para gerar a voz)\n\n"
       "Fonte: `narracao_sugestao.md` (âncoras ### = parágrafos daqui, na mesma ordem); gerado por `gerar_narracao_tags.py`. "
       "Tags em inglês, valendo até a próxima; não entram na legenda nem no SRT. **Sem tags de ritmo lento (pedido do usuário).**\n\n"
       "## Texto corrido (para gravação)\n\n")
(AQUI / "narracao_tags.md").write_text(cab + txt + "\n", encoding="utf-8")
sem_tags = re.sub(r"\[[^\]]*\]", "", txt)
pal = len(sem_tags.split())
print(f"parágrafos {len(linhas)} · palavras {pal} · {pal / 3.0 / 60:.1f}–{pal / 2.6 / 60:.1f} min · caracteres {len(txt)}")
print(dict(Counter(re.findall(r"\[[^\]]*\]", txt))))
if faltam:
    print("sem tag definida (usei thoughtful):", faltam)
suspeitos = sorted(set(re.findall(r"[0-9]|[=+×^²₁₂ᵢθλ⃗√%°/]", sem_tags)))
print("símbolos/dígitos na fala (deveria ser vazio):", suspeitos)
