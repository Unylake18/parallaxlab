"""v9: atraso imagem × fala de cada gatilho [gatilho] (log_ped_<lote>.txt ou log_<lote>.txt): instante da cena − (início da palavra − LEAD). Positivo = imagem atrasada."""
import json, re, sys
from pathlib import Path
U = Path(__file__).resolve().parent
A = json.load(open(U / "ancoras.json", encoding="utf-8"))["ancoras"]
LEAD = 0.12
pref = sys.argv[1] if len(sys.argv) > 1 else "log_ped_"
res = []
for lote in "PH PT1 PT2 PT3 PT4 PE1 PE2 PE3 PS".split():
    for l in (U / f"{pref}{lote}.txt").read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"\[gatilho\] (\S+) ([0-9.]+) (.*)", l)
        if not m:
            continue
        aid, t, fr = m.group(1), float(m.group(2)), m.group(3)
        a = A[aid]; fala = a["fala"].split(); alvo = re.findall(r"\w+", fr.lower())
        k = next((i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo), None)
        if k is None:
            continue
        res.append((t - (a["t"][k] - LEAD), lote, aid, fr, t))
res.sort(reverse=True)
d = [r[0] for r in res]
print(f"{len(res)} gatilhos; atraso máx {max(d):+.2f} s; adiantado máx {min(d):+.2f} s; > +0,20: {sum(x > 0.2 for x in d)}; < -0,15: {sum(x < -0.15 for x in d)}")
for r in res[:14]:
    print(f"  {r[0]:+.2f} s  {r[1]} {r[2]}  «{r[3]}»")
print("adiantados:")
for r in res[-6:]:
    print(f"  {r[0]:+.2f} s  {r[1]} {r[2]}  «{r[3]}»")
