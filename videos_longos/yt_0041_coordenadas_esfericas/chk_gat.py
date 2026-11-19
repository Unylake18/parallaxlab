"""Confere cada self.gat("frase") das seções com a fala da âncora corrente (ancoras.json): frases ausentes e fora de ordem."""
import json, re, sys
from pathlib import Path
A = json.loads(Path("ancoras.json").read_text(encoding="utf-8"))["ancoras"]
w = lambda s: re.findall(r"\w+", s.lower())
for arq in sorted(Path(".").glob("sec_*.py")):
    aid, pos = None, 0
    for n, l in enumerate(arq.read_text(encoding="utf-8").splitlines(), 1):
        m = re.search(r'self\.an\("([^"]+)"\)', l)
        if m:
            aid, pos = m.group(1), 0
            continue
        m = re.search(r'self\.gat\("([^"]+)"\)', l)
        if m and aid:
            fala = w(A[aid]["fala"]); al = w(m.group(1))
            ks = [i for i in range(len(fala)) if fala[i:i + len(al)] == al]
            if not ks:
                print(f"{arq}:{n} {aid} AUSENTE: {m.group(1)!r}")
            else:
                k = next((k for k in ks if k >= pos), None)
                if k is None:
                    print(f"{arq}:{n} {aid} ANTES do ponto atual: {m.group(1)!r}")
                else:
                    pos = k
