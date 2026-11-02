"""yt_0018 v7: auditorias da VOZ no WAV final (audio/narracao_v7.wav) — VOZ CONTÍNUA, BORDA ABRUPTA e JUNÇÕES.
  VOZ CONTÍNUA: silêncio digital (< -80 dBFS em janelas de 10 ms) com 50 ms ou mais, do começo da fala ao fim da fala → 0 trechos.
  BORDA ABRUPTA: envelope RMS em janelas de 10 ms; salto >= 35 dB entre janelas vizinhas fora do começo e do fim do arquivo → 0 ocorrências.
  JUNÇÕES: uma por bloco - 1, cada uma com crossfade e silêncio natural.
uso: python auditoria_voz.py [arquivo.wav] [--lista]"""
import json
import sys
import wave
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
WAV = Path(args[0]) if args else U / "audio" / "narracao_v7.wav"
LISTA = "--lista" in sys.argv
SR, JAN = 44100, 441
with wave.open(str(WAV)) as w:
    assert w.getframerate() == SR and w.getnchannels() == 1
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64)
n = len(x) // JAN
e = np.sqrt((x[: n * JAN].reshape(n, JAN) ** 2).mean(axis=1) + 1e-12)
db = 20 * np.log10(e / 32768.0)
fala = np.nonzero(db > -45)[0]
i0, i1 = int(fala[0]), int(fala[-1])
print(f"{WAV.name}: {len(x) / SR:.2f} s; fala de {i0 * 0.01:.2f} a {(i1 + 1) * 0.01:.2f} s")

# VOZ CONTÍNUA
dig = db[i0:i1 + 1] < -80
runs, ini = [], None
for k, d in enumerate(list(dig) + [False]):
    if d and ini is None:
        ini = k
    if not d and ini is not None:
        if (k - ini) >= 5:
            runs.append(((i0 + ini) * 0.01, (k - ini) * 0.01))
        ini = None
print(f"VOZ CONTÍNUA: {len(runs)} trechos de silêncio digital >= 50 ms" + (": " + ", ".join(f"{t:.2f}s({d * 1000:.0f}ms)" for t, d in runs[:30]) if runs else ""))

# BORDA ABRUPTA
salto = np.abs(np.diff(db[i0:i1 + 1]))
idx = np.nonzero(salto >= 35)[0]
print(f"BORDA ABRUPTA: {len(idx)} ocorrências (salto >= 35 dB em 10 ms)" + (": " + ", ".join(f"{(i0 + k) * 0.01:.2f}s({salto[k]:.0f}dB)" for k in idx[:40]) if len(idx) else ""))
print(f"  maior salto: {salto.max():.1f} dB em {(i0 + int(salto.argmax())) * 0.01:.2f} s")

# piso de ruído nos silêncios (janelas entre -45 e o mínimo)
sil = db[i0:i1 + 1][db[i0:i1 + 1] < -45]
print(f"silêncios: {len(sil)} janelas < -45 dBFS; piso mediano {np.median(sil):.1f} dBFS, mínimo {sil.min():.1f}, p5 {np.percentile(sil, 5):.1f}")

# JUNÇÕES
T = json.loads((U / "audio" / "voz7_tempos.json").read_text(encoding="utf-8"))
print(f"JUNÇÕES: {len(T['juncoes'])}")
for j in T["juncoes"]:
    print(f"  {j['t']:.2f} s {j['entre'][0]}→{j['entre'][1]}: crossfade {j['xfade_ms']:.0f} ms, silêncio natural {j['silencio_s']:.2f} s")
if LISTA:
    # pausas entre âncoras (silêncio natural do próprio take)
    pass
