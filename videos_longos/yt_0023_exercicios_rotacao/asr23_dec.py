import sys, wave, numpy as np
w = wave.open(sys.argv[1]); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
# reamostra para 16 kHz (interp linear; suficiente para ASR de tempos)
n = int(len(x) * 16000 / sr); y = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
np.save(sys.argv[2], y); print(len(y) / 16000, 's')
