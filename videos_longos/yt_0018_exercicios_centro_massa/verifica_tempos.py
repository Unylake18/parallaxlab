"""yt_0018 v7: confere os tempos do /with-timestamps contra a forma de onda do WAV final. Para cada palavra precedida de pausa (>= 0,12 s entre o fim da
anterior e o início dela), acha o instante em que o envelope RMS (10 ms) sobe acima de max(-42 dBFS, piso + 12 dB) perto do início alinhado.
uso: python verifica_tempos.py"""
import json
import wave
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
SR, JAN = 44100, 441
with wave.open(str(U / "audio" / "narracao_v7.wav")) as w:
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)
n = len(x) // JAN
db = 20 * np.log10(np.sqrt((x[: n * JAN].reshape(n, JAN) ** 2).mean(axis=1) + 1e-12) / 32768.0)
T = json.loads((U / "audio" / "voz7_tempos.json").read_text(encoding="utf-8"))
ordem = json.loads((U / "ancoras_nominal.json").read_text(encoding="utf-8"))["ordem"]
palavras = [(aid, dict(p, t=p.get("ta", p["t"]))) for aid in ordem for p in T["ancoras"][aid]]
dif = []
for k, (aid, p) in enumerate(palavras):
    if k == 0:
        continue
    ant = palavras[k - 1][1]
    if p["t"] - ant["e"] < 0.20:
        continue
    i, i0 = int(round(p["t"] / 0.01)), int(round(ant["e"] / 0.01))
    lo, hi = max(1, i0 + 2), min(n - 1, i + 30)
    piso = np.percentile(db[lo:max(lo + 1, i - 5)], 20)
    lim = max(-42.0, piso + 12.0)
    for j in range(lo, hi):
        if db[j] >= lim and db[j - 1] < lim:
            dif.append((aid, p["w"], p["t"], j * 0.01 - p["t"]))
            break
d = np.array([q[3] for q in dif])
print(f"{len(dif)} palavras após pausa conferidas; deslocamento (onda − alinhamento): mediana {np.median(d):+.3f} s, p95 {np.percentile(np.abs(d), 95):.3f} s, "
      f"máx |{np.abs(d).max():.3f}| s, desvio {d.std():.3f} s")
for q in sorted(dif, key=lambda q: -abs(q[3]))[:5]:
    print(f"  pior: {q[0]} '{q[1]}' em {q[2]:.2f} s: {q[3]:+.3f} s")
print("primeiras palavras de âncora (10 amostras):")
for aid in ordem[::5][:10]:
    q = [r for r in dif if r[0] == aid and r[2] == T["ancoras"][aid][0]["t"]]
    print(f"  {aid:6s} {T['ancoras'][aid][0]['w']!r} t={T['ancoras'][aid][0]['t']:.3f}" + (f" onda {q[0][3]:+.3f} s" if q else " (sem pausa antes)"))
(U / "audio" / "voz7_deslocamento.json").write_text(json.dumps({"n": len(dif), "mediana": float(np.median(d)), "p95": float(np.percentile(np.abs(d), 95)), "max": float(np.abs(d).max())}), encoding="utf-8")
