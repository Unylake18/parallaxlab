"""yt_0013 — ritmo da sincronia: ritmo_bruto.json (passe GRAVAR=1) + alinhamento da voz -> ritmo.json.

Trecho k = conteúdo da cena entre a âncora k−1 e a âncora k (P = plays, W = esperas, F = resto fixo).
Cada trecho recebe fatores fp (plays) e fw (esperas) para durar exatamente o tempo da voz até a âncora k:
- sobra tempo: os plays esticam até SMAX e as esperas absorvem o resto (sem esperas, os plays esticam até SMAX_SO);
- falta tempo: as esperas encolhem até FWMIN, depois os plays até FPMIN; se ainda faltar, entra uma pausa na voz
  (silêncio inserido antes da fala da âncora k), nunca uma animação apressada demais.
Uso: uv run --no-sync python ritmo.py   (depois: render normal; montar_sync.py monta a voz com as pausas)
"""
import json
import re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LEAD, FIM_EXTRA, FOLGA = 0.15, 1.8, 0.08
SMAX, SMAX_SO, FPMIN, FWMIN = 1.6, 2.2, 0.75, 0.35


def _n(w):
    return re.sub(r"[^\w]", "", w.lower())


cel = json.loads((AQUI / "audio" / "alinhamento_forcado.json").read_text(encoding="utf-8"))["celulas"]
VOZ = {c["chave"]: c["palavras"] for c in cel}
TODAS = [p for c in cel for p in c["palavras"]]
VOZ_FIM = TODAS[-1][2]


def palavra(aid, frase):
    ws = VOZ[aid]
    if not frase:
        return ws[0]
    toks = [_n(x) for x in frase.split()]
    seq = [_n(w[0]) for w in ws]
    for i in range(len(seq) - len(toks) + 1):
        if seq[i:i + len(toks)] == toks:
            return ws[i]
    raise KeyError((aid, frase))


def corte(w):
    """Instante (voz original) para inserir silêncio antes da palavra w: meio da pausa que a antecede."""
    i = next(j for j, x in enumerate(TODAS) if x is w)
    return (TODAS[i - 1][2] + w[1]) / 2 if i else max(0.0, w[1] - 0.05)


bruto = json.loads((AQUI / "ritmo_bruto.json").read_text(encoding="utf-8"))
trechos, pads, soma, t_ant = [], [], 0.0, 0.0
rel = []
for r in bruto:
    if r["id"] == "FIM":
        v, w = VOZ_FIM + FIM_EXTRA, None
    else:
        w = palavra(r["id"], r["frase"])
        v = max(0.0, w[1] - LEAD)
    P, W, D = r["P"], r["W"], r["D"]
    F = max(0.0, D - P - W)
    A = v + soma - t_ant - FOLGA
    pad = 0.0
    if A >= D - 0.1:
        extra = max(0.0, A - D)
        if W > 0.05:
            fp = min(1 + extra / P, SMAX) if P > 0 else 1.0
            fw = (W + extra - P * (fp - 1)) / W
        else:
            fp = min(1 + extra / P, SMAX_SO) if P > 0 else 1.0
            fw = 1.0
    else:
        falta = D - A
        if W * (1 - FWMIN) >= falta:
            fp, fw = 1.0, 1 - falta / W
        else:
            fw = FWMIN if W > 0 else 1.0
            falta -= W * (1 - FWMIN)
            if P * (1 - FPMIN) >= falta:
                fp = 1 - falta / P
            else:
                fp = FPMIN
                pad = falta - P * (1 - FPMIN) + 0.15
                if w is not None:
                    pads.append([round(corte(w), 3), round(pad, 3), r["id"], r["frase"]])
                soma += pad
    alvo = v + soma
    dur_real = F + P * fp + W * fw
    trechos.append({"id": r["id"], "frase": r["frase"], "alvo": round(alvo, 4), "fp": round(fp, 4), "fw": round(fw, 4)})
    rel.append((r["id"], r["frase"], round(alvo - t_ant, 2), round(D, 2), fp, fw, round(pad, 2),
                round(max(0.0, alvo - t_ant - dur_real), 2)))
    t_ant = alvo
(AQUI / "ritmo.json").write_text(json.dumps({"trechos": trechos, "pads": pads, "dur": round(t_ant, 3)},
                                            ensure_ascii=False, indent=0), encoding="utf-8")
print(f"{len(trechos)} trechos; {len(pads)} pausas na voz (soma {soma:.1f} s); duração {t_ant:.1f} s")
print("trecho                                        voz(s) cena(s)  fp    fw    pausa  sobra")
for x in rel:
    print(f"{x[0]:7s} {x[1][:34]:34s} {x[2]:6.2f} {x[3]:6.2f} {x[4]:5.2f} {x[5]:5.2f} {x[6]:5.2f} {x[7]:5.2f}")
