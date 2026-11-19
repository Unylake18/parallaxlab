"""SYNC (handoff final §5.5): para cada âncora e cada gatilho de fala, atraso entre o início da palavra (voz real) e o evento visual no render. Meta: ≤ 0,2 s (imagem pode adiantar até 0,35 s).
uso: python sync24.py → qa/sync.txt"""
import json, re
from pathlib import Path
U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8")); anc = A["ancoras"]; ordem = A["ordem"]
tok = lambda s: re.findall(r"\w+", s.lower())
out, ruins, n, atrasos, anc_n = [], 0, 0, [], 0
for L in ["PH", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PS"]:
    for ln in (U / f"log_{L}.txt").read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"\[ancora\] (\S+) (\S+)", ln)
        if m:
            aid, rel = m.group(1), float(m.group(2))
            if aid not in anc:
                continue
            anc_n += 1
            out.append(f"ANCORA {aid:5s} abre em {rel:7.2f} s do lote (voz: {anc[aid]['ini']:.2f} s absoluto)")
        m = re.match(r"\[gatilho\] (\S+) (\S+) (.*)", ln)
        if m:
            aid, rel, fr = m.group(1), float(m.group(2)), m.group(3)
            alvo = tok(fr); fala = anc[aid]["fala"].split()
            k = next((i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo), None)
            if k is None:
                continue
            dly = rel - anc[aid]["t"][k]            # >0: imagem depois da palavra
            n += 1; atrasos.append(dly)
            if dly > 0.20 or dly < -0.45:
                ruins += 1
                out.append(f"  FORA {aid:5s} {dly:+.2f} s  «{fr}»")
a = [x for x in atrasos]
res = f"SYNC: {n} gatilhos; atraso (imagem − palavra) min {min(a):+.2f} / mediana {sorted(a)[len(a)//2]:+.2f} / máx {max(a):+.2f} s; fora de [−0,45; +0,20]: {ruins}; âncoras abertas: {anc_n}/43"
(U / "qa" / "sync.txt").write_text(res + "\n" + "\n".join(out) + "\n", encoding="utf-8")
print(res)
print("\n".join(l for l in out if "FORA" in l)[:3000])
