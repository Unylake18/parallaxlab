"""yt_0012 — ritmo da sincronia: sync_log.jsonl (passe a seco) + alinhamento forçado da voz -> ritmo.json.

Cada âncora `an(frase)` prende o play() seguinte a LEAD s antes da primeira palavra de `frase` na voz.
Trecho k = plays entre a âncora k−1 e a âncora k: animações (A), esperas (W) e a folga mínima da âncora (S, logo antes dela).
- sobra tempo: animações esticam até SMAX (em proporção), as esperas absorvem o resto; sem esperas, a folga S segura a tela;
- falta tempo: esperas encolhem até FWMIN, animações até FPMIN; se ainda faltar, entra uma pausa na voz (silêncio antes da
  palavra da âncora), nunca uma animação apressada demais.
Saída: ritmo.json {"t": início de cada play (s), "pads": [[corte_s, dur_s, frase]], "anchors": [...], "dur": s}.
Uso: uv run --no-sync python ritmo.py
"""
import json
import re
from pathlib import Path

P = Path(__file__).resolve().parent
LEAD, TAIL = 0.15, 2.5
SMAX, SMAX_SO, FPMIN, FWMIN, MINF = 1.35, 1.6, 0.72, 0.3, 2 / 30


def norm(w):
    return re.sub(r"[^\w]", "", w.lower())


bruto = json.loads((P / "audio" / "alinhamento_forcado_bruto.json").read_text(encoding="utf-8"))
WS = [(w["text"], w["start"], w["end"]) for w in bruto["words"] if w["text"].strip()]
SEQ = [norm(w[0]) for w in WS]
VOZ_FIM = WS[-1][2]

plays, anchors = [], []
for ln in (P / "sync_log.jsonl").read_text(encoding="utf-8").splitlines():
    r = json.loads(ln)
    if "anchor" in r:
        anchors.append(r)
    else:
        plays.append(r)
assert all(p["i"] == k for k, p in enumerate(plays)), "log fora de ordem"
N = len(plays)

# palavra de cada âncora: busca sequencial a partir da anterior
pos, alvo = 0, []
for a in anchors:
    toks = [norm(x) for x in a["anchor"].split() if norm(x)]
    for j in range(pos, len(SEQ) - len(toks) + 1):
        if SEQ[j:j + len(toks)] == toks:
            break
    else:
        raise SystemExit(f"âncora não encontrada na voz (depois da palavra {pos}): {a['anchor']!r}")
    alvo.append(j)
    pos = j + 1


def corte(j):
    return (WS[j - 1][2] + WS[j][1]) / 2 if j else max(0.0, WS[j][1] - 0.05)


dur = [0.0] * N
pads, soma, rel = [], 0.0, []
fronteiras = [(0, None, "")] + [(a["i"], j, a["anchor"]) for a, j in zip(anchors, alvo)] + [(N, -1, "FIM")]
t_ant = 0.0
for (i0, _, _n), (i1, j, nome) in zip(fronteiras[:-1], fronteiras[1:]):
    idx = list(range(i0, i1))
    if j is None:
        continue
    v = (VOZ_FIM + TAIL) if j == -1 else max(0.0, WS[j][1] - LEAD)
    T = v + soma - t_ant
    folga = [k for k in idx if plays[k]["kind"] == "hold" and plays[k]["nom"] < 0.1]
    A = [k for k in idx if plays[k]["kind"] == "anim" and plays[k]["nom"] > 0]
    W = [k for k in idx if plays[k]["kind"] == "hold" and plays[k]["nom"] >= 0.1]
    PA, PW = sum(plays[k]["nom"] for k in A), sum(plays[k]["nom"] for k in W)
    fp = fw = 1.0
    sobra = 0.0
    pad = 0.0
    if T >= PA + PW:
        extra = T - PA - PW
        if PW >= 0.3:
            fp = min(1 + extra / max(PA + PW, 1e-9), SMAX) if PA > 0 else 1.0
            fw = (PW + extra - PA * (fp - 1)) / PW
        else:
            fp = min(1 + extra / PA, SMAX_SO) if PA > 0 else 1.0
            sobra = extra - PA * (fp - 1)
            if PW > 0:
                fw, sobra = (PW + sobra) / PW, 0.0
    else:
        falta = PA + PW - T
        if PW * (1 - FWMIN) >= falta:
            fw = 1 - falta / PW
        else:
            fw = FWMIN if PW > 0 else 1.0
            falta -= PW * (1 - FWMIN)
            if PA * (1 - FPMIN) >= falta:
                fp = 1 - falta / PA
            else:
                fp = FPMIN
                pad = falta - PA * (1 - FPMIN) + 0.12
                if j != -1:
                    pads.append([round(corte(j), 3), round(pad, 3), nome])
                soma += pad
    for k in A:
        dur[k] = max(MINF, plays[k]["nom"] * fp)
    for k in W:
        dur[k] = plays[k]["nom"] * fw
    if folga:
        dur[folga[-1]] = max(0.0, sobra)
    real = sum(dur[k] for k in idx)
    alvo_t = v + soma
    rel.append((nome[:38], i0, i1, round(T, 2), round(PA, 2), round(PW, 2), round(fp, 2), round(fw, 2), round(pad, 2), round(sobra, 2),
                round(alvo_t - t_ant - real, 3)))
    # corrige o arredondamento (MINF) jogando a diferença na última espera do trecho, se houver
    diff = alvo_t - t_ant - real
    if abs(diff) > 1e-6:
        alvo_hold = (folga + W)[-1:] if (folga + W) else A[-1:]
        dur[alvo_hold[0]] = max(0.0, dur[alvo_hold[0]] + diff)
    t_ant = alvo_t

t = [0.0]
for d in dur:
    t.append(round(t[-1] + d, 5))
(P / "ritmo.json").write_text(json.dumps({"t": t, "pads": pads, "anchors": [[a["anchor"], a["i"], round(WS[j][1], 3)]
                                                                             for a, j in zip(anchors, alvo)],
                                          "dur": round(t[-1], 3)}, ensure_ascii=False, indent=0), encoding="utf-8")
print(f"{N} plays · {len(anchors)} âncoras · {len(pads)} pausas na voz (soma {soma:.1f} s) · duração {t[-1]:.1f} s "
      f"(voz {VOZ_FIM:.1f} s)")
ruins = [r for r in rel if r[6] > SMAX_SO - 0.01 or r[8] > 0 or r[9] > 4.0 or r[6] < 0.8]
print("trechos a olhar (âncora i0 i1 voz anim espera fp fw pausa folga resto):")
for r in ruins:
    print("  ", r)
(P / "ritmo.log").write_text(chr(10).join(str(r) for r in rel), encoding="utf-8")
