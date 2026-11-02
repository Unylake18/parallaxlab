"""v9: confere cada self.gat("frase") / self.an("ID") das seções contra a fala real (ancoras.json)."""
import json, re, glob
A = json.load(open("ancoras.json", encoding="utf-8"))["ancoras"]
falta = []
for f in sorted(glob.glob("sec_*.py")):
    aid = None
    for n, l in enumerate(open(f, encoding="utf-8"), 1):
        m = re.search(r'self\.an\("([^"]+)"\)', l)
        if m:
            aid = m.group(1)
            if aid not in A:
                falta.append((f, n, "ÂNCORA INEXISTENTE", aid))
        for g in re.finditer(r'self\.gat\("([^"]+)"\)', l):
            fr = re.findall(r"\w+", g.group(1).lower())
            fala = A.get(aid, {}).get("fala", "").split()
            ok = any(fala[i:i + len(fr)] == fr for i in range(len(fala)))
            if not ok:
                falta.append((f, n, aid, g.group(1)))
print(len(falta), "gatilhos sem frase na fala real")
for x in falta:
    print(x)
