"""yt_0030 · QA das 22 emendas da voz v3.4 (HANDOFF v4 §4.5), DEPOIS do alinhamento novo (alinhar_voz.py --stt no WAV v3.4).
Para cada trecho: a pausa real entre a última palavra antes e a primeira do trecho (e no fim), o nível 2 s antes × 2 s depois de cada emenda
e o maior salto entre amostras dentro da pausa. Critérios: pausa 0,12–0,60 s · |Δ nível| ≤ 3 dB · salto ≤ 0,2 (sem clique).
uso: uv run --no-sync python qa_emendas_v34.py   → qa/emendas_v34.txt; saída 1 se alguma emenda falhar."""
import json
import re
import sys
import wave
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
sys.path.insert(0, str(U))
from tempos import ancoras  # noqa: E402

with wave.open(str(U / "audio" / "narracao_final.wav")) as w:
    sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
P = json.loads((U / "alinhamento_palavras.json").read_text(encoding="utf-8"))
d = ancoras()
toks = [(i, t) for i, p in enumerate(P) for t in re.findall(r"\w+", p["word"].lower())]
lim, k = {}, 0
for aid in d["ordem"]:
    n = len(d["ancoras"][aid]["fala"].split())
    lim[aid] = (toks[k][0], toks[k + n - 1][0])
    k += n
assert k == len(toks)
rms = lambda t0, t1: 20 * np.log10(np.sqrt(np.mean(a[int(max(0, t0) * sr):int(t1 * sr)] ** 2)) + 1e-9)
plano = json.loads((U / "trechos_v34" / "plano_trechos.json").read_text(encoding="utf-8"))
L, falha = ["yt_0030 · QA das emendas v3.4 (pausa real, nível e clique em cada emenda)"], False
for p in plano:
    for lado, (wa, wb) in (("início", (lim[p["antes"]][1], lim[p["ancoras"][0]][0])), ("fim", (lim[p["ancoras"][-1]][1], lim[p["depois"]][0]))):
        x, y = P[wa]["end"], P[wb]["start"]
        seg = a[int(x * sr):int(y * sr)]
        salto = float(np.abs(np.diff(seg)).max()) if len(seg) > 1 else 0.0
        dn = rms(y, y + 2) - rms(x - 2, x)
        ok = 0.12 <= y - x <= 0.60 and abs(dn) <= 3.0 and salto <= 0.2
        falha |= not ok
        L.append(f"{'OK   ' if ok else 'FALHA'} {p['trecho']} ({lado}): «{P[wa]['word']}» → «{P[wb]['word']}» pausa {y - x:.2f} s "
                 f"({x:.2f}–{y:.2f}) · nível {dn:+.1f} dB · salto {salto:.4f}")
(U / "qa").mkdir(exist_ok=True)
(U / "qa" / "emendas_v34.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
sys.exit(1 if falha else 0)
