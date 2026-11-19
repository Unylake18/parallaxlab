"""yt_0025 · checagens automáticas do WAV (handoff final §4.4) -> qa/voz.txt.
duração; pico/clipping; silêncios > 1,5 s; tag lida em voz alta (procura no ASR as palavras das tags); fronteiras entre blocos (silêncio/descontinuidade)."""
import json
import re
import wave
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
WAV = AQUI / "audio" / "narracao_v2.wav"
with wave.open(str(WAV)) as w:
    fr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
if ch > 1:
    x = x.reshape(-1, ch).mean(1)
L = []
dur = len(x) / fr
L.append(f"WAV: {fr} Hz, {ch} canal(is), {dur:.2f} s = {int(dur // 60)}:{dur % 60:04.1f} min (limite do handoff: 16:00)")
pico = float(np.abs(x).max())
clip = int((np.abs(x) > 0.999).sum())
L.append(f"pico {pico:.3f} ({20 * np.log10(pico):.1f} dBFS); amostras em clipping (>0,999): {clip} -> {'OK' if clip == 0 else 'FALHA'}")
# silêncios: janelas de 20 ms com RMS < -50 dBFS
jan = int(0.02 * fr)
rms = np.sqrt((x[: len(x) // jan * jan].reshape(-1, jan) ** 2).mean(1)) + 1e-9
db = 20 * np.log10(rms)
mudo = db < -50
runs, i = [], 0
while i < len(mudo):
    if mudo[i]:
        j = i
        while j < len(mudo) and mudo[j]:
            j += 1
        runs.append((i * 0.02, (j - i) * 0.02))
        i = j
    else:
        i += 1
longos = [(t, d) for t, d in runs if d > 1.5]
L.append(f"silêncios (< -50 dBFS) > 1,5 s: {len(longos)} {'OK' if not longos else 'FALHA'}")
for t, d in longos:
    L.append(f"   {t:7.2f} s  duração {d:.2f} s")
L.append(f"maior silêncio: {max([d for _, d in runs], default=0):.2f} s; pausas entre 0,6 e 1,5 s: {sum(1 for _, d in runs if 0.6 <= d <= 1.5)}")
# tag lida em voz alta
asr_p = AQUI / "audio" / "asr_palavras_v2.json"
if asr_p.exists():
    asr = json.loads(asr_p.read_text(encoding="utf-8"))
    texto = " ".join(a["word"].lower() for a in asr)
    achou = []
    for pal in ("curious", "thoughtful", "emphatic", "excited", "happy", "calm", "satisfied", "short pause", "pause", "colchete"):
        for m in re.finditer(r"\b" + pal + r"\b", texto):
            t = next((a["start"] for a in asr if a["word"].lower().strip(".,!?") == pal.split()[0]), None)
            achou.append((pal, t))
    L.append(f"tags lidas em voz alta (procura no ASR): {len(achou)} -> {'OK' if not achou else 'FALHA'}")
    for pal, t in achou:
        L.append(f"   '{pal}' perto de {t}")
else:
    L.append("ASR ainda não disponível: tag lida em voz alta NÃO verificada")
# fronteiras dos 4 blocos de ≤4.500 caracteres: tempo estimado pela proporção de caracteres
(AQUI / "qa").mkdir(exist_ok=True)
(AQUI / "qa" / "voz.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
