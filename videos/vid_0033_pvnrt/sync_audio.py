"""audio/narracao_sync.wav = narracao_v4.wav sem nenhum recorte, com silêncio só no FIM até a duração do vídeo (NQ/FPS). Sem pausas inseridas na voz."""
import wave
from pathlib import Path
import numpy as np
import roteiro as RT
U = Path(__file__).resolve().parent
with wave.open(str(U / 'audio' / 'narracao_v4.wav')) as w:
    sr, pcm = w.getframerate(), np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
falta = int(round(RT.DURACAO * sr)) - len(pcm)
assert falta >= 0, 'a voz é mais longa que o vídeo'
out = np.concatenate([pcm, np.zeros(falta, dtype=np.int16)])
with wave.open(str(U / 'audio' / 'narracao_sync.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(out.tobytes())
# QA: sem silêncio digital > 0,35 s dentro da fala; sem descontinuidade abrupta
fala = pcm[:int(170.9 * sr)]
z = (np.abs(fala) < 8).astype(np.int8)
d = np.diff(np.concatenate([[0], z, [0]]))
ini, fim = np.where(d == 1)[0], np.where(d == -1)[0]
runs = [(a / sr, (b - a) / sr) for a, b in zip(ini, fim) if (b - a) / sr > .35]
salto = np.abs(np.diff(fala.astype(np.int32))).max() / 32768
print(f'duração da voz {len(pcm)/sr:.2f} s; vídeo {RT.DURACAO:.2f} s; silêncios digitais > 0,35 s dentro da fala: {runs}; maior salto amostra a amostra {salto:.3f} (fração do fundo de escala)')
