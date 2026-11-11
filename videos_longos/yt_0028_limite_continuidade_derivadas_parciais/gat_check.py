"""yt_0028 final: confere estaticamente se cada gat("frase")/falta("frase") dos sec_*.py existe na fala da âncora corrente (ancoras.json)."""
import json, re
from pathlib import Path
U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
ruins = 0
for f in sorted(U.glob("sec_*.py")):
    aid = None
    for n, l in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        m = re.search(r'\ban\("([^"]+)"\)', l)
        if m:
            aid = m.group(1)
        for g in re.findall(r'(?:gat|falta|caneta_ate\([^,]+,)\s*\(?\s*"([^"]+)"', l):
            fala = A.get(aid, {}).get("fala", "").split()
            alvo = re.findall(r"\w+", g.lower())
            ok = any(fala[i:i + len(alvo)] == alvo for i in range(len(fala)))
            if not ok:
                ruins += 1
                print(f"{f.name}:{n} {aid}: {g!r}")
print("sem frase:", ruins)
