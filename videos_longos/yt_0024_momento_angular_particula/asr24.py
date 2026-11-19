"""yt_0024 · tempos por palavra do WAV da voz (faster-whisper small, venv isolado em C:\\Users\\Pichau\\asr_venv).

Passo 1 (venv do projeto): decodifica o WAV para 16 kHz float32 (.npy), porque o av do venv isolado quebra.
Passo 2 (venv isolado): transcreve com word_timestamps e grava audio/asr_palavras_v1.json = [{word, start, end}].
Uso:  uv run --no-sync python asr24.py audio/narracao_v1.wav
"""
import json
import subprocess
import sys
from pathlib import Path

import av
import numpy as np

AQUI = Path(__file__).resolve().parent
wav = Path(sys.argv[1]).resolve()
saida = wav.parent / "asr_palavras_v1.json"
npy = wav.parent / "_asr16k.npy"

saida_arr = []
with av.open(str(wav)) as c:
    rs = av.AudioResampler(format="flt", layout="mono", rate=16000)
    for fr in c.decode(audio=0):
        for r in rs.resample(fr):
            saida_arr.append(np.frombuffer(bytes(r.planes[0])[: r.samples * 4], dtype=np.float32))
    for r in rs.resample(None):
        saida_arr.append(np.frombuffer(bytes(r.planes[0])[: r.samples * 4], dtype=np.float32))
np.save(npy, np.concatenate(saida_arr))

codigo = r'''
import json, sys, numpy as np
from faster_whisper import WhisperModel
a = np.load(sys.argv[1])
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, language="pt", word_timestamps=True, vad_filter=False, condition_on_previous_text=False, beam_size=5)
out = []
for s in segs:
    for w in s.words:
        out.append(dict(word=w.word.strip(), start=round(w.start, 3), end=round(w.end, 3)))
open(sys.argv[2], "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False))
print(len(out), "palavras")
'''
(AQUI / "_asr_run.py").write_text(codigo, encoding="utf-8")
r = subprocess.run([r"C:\Users\Pichau\asr_venv\Scripts\python.exe", str(AQUI / "_asr_run.py"), str(npy), str(saida)], capture_output=True, text=True)
print(r.stdout[-500:], r.stderr[-800:])
npy.unlink(missing_ok=True)
