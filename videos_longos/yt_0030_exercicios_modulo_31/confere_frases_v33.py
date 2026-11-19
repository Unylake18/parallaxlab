"""yt_0030 · conferência estática da narração v3.3 (HANDOFF FINAL §3.2). Rodar na unidade, depois de instalar o narracao.md v3.3:
    uv run --no-sync python confere_frases_v33.py
Usa a MESMA tokenização da cena (tempos.py + kit._k_frase: \\w+ em minúsculas, COM acento) e confere as 482 frases de sincronia
(459 gatilhos self.gat + 23 fins de sublinhado le(..., ate=...)). Saída esperada: 69 âncoras, 482/482, 0 faltando, 5414 palavras."""
import json, re, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from tempos import ANC_DADOS as D

F = json.loads((AQUI / "frases_sincronia_v33.json").read_text(encoding="utf-8"))
falta, n = [], 0
for aid, grupos in F.items():
    fala = D["ancoras"][aid]["fala"].split()
    for tipo, lista in grupos.items():
        for fr in lista:
            n += 1
            alvo = re.findall(r"\w+", fr.lower())
            if next((i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo), None) is None:
                falta.append(f"{aid} [{tipo}] {fr!r}")
pal = sum(D["ancoras"][a]["palavras"] for a in D["ordem"])
print(f"âncoras {len(D['ordem'])} · frases {n - len(falta)}/{n} · faltando {len(falta)} · palavras {pal}")
for f in falta:
    print("  FALTA", f)
sys.exit(1 if falta or len(D["ordem"]) != 69 else 0)
