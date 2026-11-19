"""Lista, por âncora, os gat("frase") do código que NÃO existem na fala nova (ancoras.json) — a frase precisa ser achada em palavras consecutivas."""
import json
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
tok = lambda s: re.findall(r"\w+", s.lower())
tot = ruins = 0
for arq in sorted(U.glob("sec_*.py")):
    aid = None
    for n, ln in enumerate(arq.read_text(encoding="utf-8").splitlines(), 1):
        m = re.search(r'self\.an\("([^"]+)"\)', ln)
        if m:
            aid = m.group(1)
            continue
        for g in re.finditer(r'self\.gat\((?:"([^"]*)"|\'([^\']*)\')\)', ln):
            fr = g.group(1) or g.group(2)
            tot += 1
            fala = tok(ANC.get(aid, {}).get("fala", ""))
            alvo = tok(fr)
            ok = any(fala[i:i + len(alvo)] == alvo for i in range(len(fala)))
            if not ok:
                ruins += 1
                print(f"{arq.name}:{n} [{aid}] {fr!r}")
                if "-v" in sys.argv:
                    print("    fala:", " ".join(fala))
print(f"{ruins} de {tot} gatilhos sem frase na fala nova")
