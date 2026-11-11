"""final: simula a sincronia a partir de qa/plano/<lote>.json e do ancoras.json (sem render): atraso previsto de cada gatilho e estouro de âncora,
com a caneta encolhida até o piso (f ≥ 0,667). uso: python qa_simula_sync.py [LIM=0.2]"""
import json, re, sys
from pathlib import Path
U = Path(__file__).resolve().parent
A = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
LEAD, FMIN = 0.09, 0.667
LIM = float(sys.argv[1]) if len(sys.argv) > 1 else 0.2
def kf(aid, fr):
    fala, alvo = A[aid]["fala"].split(), re.findall(r"\w+", fr.lower())
    return next((i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo), None)
tot = 0
for lote in ["PHA", "PB1", "PB2", "PB3", "PB4", "PB5", "PB6", "PF", "PB7", "PS"]:
    segs = json.loads((U / "qa" / "plano" / f"{lote}.json").read_text(encoding="utf-8"))
    T, off, aid = None, 0.0, None
    for i, g in enumerate(segs):
        if g["aid"] and g["aid"] != aid:
            na = g["aid"]
            ini = A[na]["ini"] + off
            if T is None:
                T = ini
            elif T > ini + 1e-6:
                print(f"  [estouro] {lote} {na} +{T - ini:.2f}s")
                off += T - ini
            else:
                T = ini
            aid = na
        if g["fim"] == "fim":
            continue
        q0 = A[aid]["ini"] + off
        if g["fim"] == "gat":
            k = kf(aid, g["frase"])
            alvo = q0 + max(0, A[aid]["t"][k] - LEAD)
        else:
            alvo = A[aid]["fim"] + off - g["antes"]
        disp = alvo - T - 0.05
        f = 1.0
        if g["c"] > 0 and g["c"] + g["o"] > disp:
            f = max(FMIN, (disp - g["o"]) / g["c"])
        fim = T + g["c"] * f + g["o"]
        atraso = fim - alvo
        if atraso > LIM and g["fim"] == "gat":
            tot += 1
            print(f"{lote} {aid:6s} trecho {i:2d} → «{g['frase']}»: pede c={g['c']:.1f} o={g['o']:.1f}, cabe {disp:.1f} → atraso {atraso:+.2f}s")
        T = max(fim, alvo)
print(tot, "gatilhos previstos acima de", LIM)
