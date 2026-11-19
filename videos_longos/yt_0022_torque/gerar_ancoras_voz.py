"""yt_0022 · fase de voz: grava ancoras.json com os tempos REAIS da voz (audio/narracao_v3.wav).

Entrada: narracao_tags.md (texto da fala, uma âncora por parágrafo, na ordem de ancoras.json) e audio/asr_palavras_v3.json (faster-whisper small, só para os tempos;
o texto de referência é o da narração, não o reconhecido). Alinha por difflib; palavras sem par (números falados que o ASR escreveu em dígitos etc.) são
interpoladas por sílabas entre as vizinhas casadas.
Saída: ancoras.json (mesmas chaves do nominal: palavras, ini, fim, dur, nominal, fala, t) com ini/fim contínuos (sem silêncio inserido; soma = duração do WAV)
e alinhamento_palavras.json. Faz backup do nominal em ancoras_v3_nominal.json na primeira execução.
"""
import difflib
import json
import re
import wave
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
ANTES = 0.45
ANC_ANTIGO = AQUI / "ancoras_v3_nominal.json"
if not ANC_ANTIGO.exists():
    ANC_ANTIGO.write_bytes((AQUI / "ancoras.json").read_bytes())
ordem = json.loads(ANC_ANTIGO.read_text(encoding="utf-8"))["ordem"]

txt = (AQUI / "narracao_tags.md").read_text(encoding="utf-8").split("## Texto corrido (para gravação)")[1]
paras = [p.strip() for p in re.split(r"\n\s*\n", txt) if p.strip()]
assert len(paras) == len(ordem), (len(paras), len(ordem))
tok = lambda s: re.findall(r"\w+", re.sub(r"\[[^\]]*\]", "", s).lower())
palavras, dono = [], []
for aid, p in zip(ordem, paras):
    w = tok(p)
    palavras += w
    dono += [aid] * len(w)

with wave.open(str(AQUI / "audio" / "narracao_v3.wav")) as w:
    DUR = w.getnframes() / w.getframerate()

asr = json.loads((AQUI / "audio" / "asr_palavras_v3.json").read_text(encoding="utf-8"))
B, Bi = [], []                       # ASR quebrado em tokens \w+ (cada pedaço herda o tempo da palavra; "9,8" vira dois)
for a in asr:
    ps = re.findall(r"\w+", a["word"].lower())
    for k, q in enumerate(ps):
        d = (a["end"] - a["start"]) / len(ps)
        B.append(q)
        Bi.append((a["start"] + k * d, a["start"] + (k + 1) * d))


def silabas(p):
    return max(1, len(re.findall(r"[aeiouáéíóúâêôãõàü]+", p)))


ini_w = np.full(len(palavras), np.nan)
fim_w = np.full(len(palavras), np.nan)
casados = 0
for blk in difflib.SequenceMatcher(None, palavras, B, autojunk=False).get_matching_blocks():
    for k in range(blk.size):
        ini_w[blk.a + k], fim_w[blk.a + k] = Bi[blk.b + k]
        casados += 1
print(f"ASR: {len(B)} tokens; {casados}/{len(palavras)} palavras do texto casadas ({100 * casados / len(palavras):.1f}%)")
peso = np.array([silabas(p) + 0.3 for p in palavras])
i = 0
while i < len(palavras):
    if np.isnan(ini_w[i]):
        j = i
        while j < len(palavras) and np.isnan(ini_w[j]):
            j += 1
        a_t = fim_w[i - 1] if i > 0 else 0.0
        b_t = ini_w[j] if j < len(palavras) else DUR
        seg = peso[i:j]
        e = a_t + np.concatenate([[0], np.cumsum(seg)]) / seg.sum() * max(0.05, b_t - a_t)
        ini_w[i:j], fim_w[i:j] = e[:-1], e[1:]
        i = j
    else:
        i += 1
for k in range(len(palavras) - 1):          # monotonia
    ini_w[k + 1] = max(ini_w[k + 1], ini_w[k] + 0.01)
    fim_w[k] = min(max(fim_w[k], ini_w[k] + 0.01), ini_w[k + 1])

out, ini = {}, 0.0
idx = {aid: [k for k, d in enumerate(dono) if d == aid] for aid in ordem}
for n_, aid in enumerate(ordem):
    ks = idx[aid]
    if n_ + 1 < len(ordem):
        prox = idx[ordem[n_ + 1]][0]
        fim = max(fim_w[ks[-1]] + 0.02, ini_w[prox] - ANTES)   # v9: a âncora seguinte abre ANTES s antes da 1ª palavra (dá tempo à preparação da cena)
    else:
        fim = DUR
    n = len(ks)
    out[aid] = {"palavras": n, "ini": round(ini, 4), "fim": round(fim, 4), "dur": round(fim - ini, 4),
                "nominal": round(0.15 + n / 2.7 + 0.35, 2), "fala": " ".join(palavras[k] for k in ks),
                "t": [round(float(ini_w[k]) - ini, 3) for k in ks]}
    ini = fim
(AQUI / "ancoras.json").write_text(json.dumps({"ordem": ordem, "ancoras": out}, ensure_ascii=False, indent=1), encoding="utf-8")
(AQUI / "alinhamento_palavras.json").write_text(json.dumps(
    [dict(word=p, aid=d, start=round(float(a), 3), end=round(float(b), 3)) for p, d, a, b in zip(palavras, dono, ini_w, fim_w)],
    ensure_ascii=False), encoding="utf-8")
print(f"voz {DUR:.2f} s = {DUR / 60:.2f} min; soma das âncoras {ini:.2f} s; {len(palavras)} palavras")
ritmo = [(a, v["palavras"] / v["dur"]) for a, v in out.items()]
print("ritmo (palavras/s) min/med/max:", round(min(r for _, r in ritmo), 2), round(float(np.mean([r for _, r in ritmo])), 2), round(max(r for _, r in ritmo), 2))
for a, v in out.items():
    print(f"{a:6s} {v['ini']:8.2f} {v['fim']:8.2f} {v['dur']:6.2f}s {v['palavras']:3d}p  nominal {v['nominal']:5.2f}")
