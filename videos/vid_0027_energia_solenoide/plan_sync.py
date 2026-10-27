"""Plano de sincronização do vid_0027: une nat.json (instante natural de cada âncora na cena, MEDIR=1) e voz_ancoras.json
(instante de cada frase na voz). Cada âncora começa em T = início da frase − LEAD (a imagem antecipa a voz). Em cada trecho,
o ritmo f = (voz − FOLGA) / cena, limitado a [FMIN, FMAX]; o que sobra vira espera que "respira" (idle) na âncora seguinte.
A voz não é editada: se algum trecho não couber nem em FMIN, ele é listado como atrasado (corrigir a cena, não a voz).
Saída: sync.json (T e f por âncora, para SYNC=sync.json)."""
import json
from pathlib import Path

PASTA = Path(__file__).absolute().parent
FMIN, FMAX, LEAD, FOLGA = 0.4, 1.8, 0.10, 0.20
nat = json.loads((PASTA / "nat.json").read_text(encoding="utf-8"))
voz = json.loads((PASTA / "voz_ancoras.json").read_text(encoding="utf-8"))
nomes = [k for k in nat if not k.startswith("_")]
assert nomes == [k for k in voz if not k.startswith("_")], "âncoras da cena e da voz em ordens diferentes"
V = [voz[n]["ini"] for n in nomes] + [voz["_fim_voz"]]
N = [nat[n] for n in nomes] + [nat["_fim"]]
T = [max(v - LEAD, 0.0) for v in V[:-1]]
f, atrasados = [], []
for i, n in enumerate(nomes):
    Ds = N[i + 1] - N[i]
    if i == len(nomes) - 1:                     # cartão final: ritmo natural; a voz termina dentro dele
        f.append(1.0)
        break
    Dv = T[i + 1] - T[i]
    fi = min(max((Dv - FOLGA) / Ds, FMIN), FMAX) if Ds > 1e-6 else 1.0
    f.append(round(fi, 4))
    if Ds * fi + FOLGA > Dv + 1e-6:
        atrasados.append((n, round(Ds * fi + FOLGA - Dv, 2)))
fim_video = T[-1] + (N[-1] - N[-2]) * f[-1]
sync = {"ancoras": {n: {"T": round(T[i], 4), "f": f[i]} for i, n in enumerate(nomes)}, "lead": LEAD,
        "fim_video": round(fim_video, 3)}
(PASTA / "sync.json").write_text(json.dumps(sync, indent=1), encoding="utf-8")
print(f"vídeo {fim_video:.1f} s (voz {V[-1]:.1f} s)")
for i, n in enumerate(nomes[:-1]):
    Ds, Dv = N[i + 1] - N[i], T[i + 1] - T[i]
    sobra = Dv - Ds * f[i]
    print(f"{n:15s} T={T[i]:6.2f}  cena {Ds:5.2f}  voz {Dv:5.2f}  f={f[i]:4.2f}  espera {sobra:5.2f}")
print("atrasados:", atrasados or "nenhum")
