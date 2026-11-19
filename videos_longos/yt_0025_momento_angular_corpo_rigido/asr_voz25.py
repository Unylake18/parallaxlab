"""yt_0025 · ASR só para os tempos por palavra (e para achar tag lida em voz alta).
Etapa 1 (.venv do projeto): decodifica audio/narracao_v2.wav para 16 kHz float32 (.npy).
Etapa 2 (~/asr_venv, faster-whisper small): transcreve com tempo por palavra -> audio/asr_palavras_v2.json.
uso: ../../.venv/Scripts/python.exe asr_voz25.py 1   e   ~/asr_venv/Scripts/python.exe asr_voz25.py 2"""
import json
import sys
from pathlib import Path

import numpy as np

A = Path(__file__).resolve().parent / "audio"
WAV = A / "narracao_v2.wav"
if sys.argv[1] == "1":
    import av
    out = []
    with av.open(str(WAV)) as c:
        rs = av.AudioResampler(format="flt", layout="mono", rate=16000)
        for fr in c.decode(audio=0):
            for r in rs.resample(fr):
                out.append(r.to_ndarray().reshape(-1))
        for r in rs.resample(None):
            out.append(r.to_ndarray().reshape(-1))
    np.save(A / "_v2_16k.npy", np.concatenate(out).astype(np.float32))
    print("ok", sum(len(x) for x in out) / 16000, "s")
else:
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    seg, info = m.transcribe(np.load(A / "_v2_16k.npy"), language="pt", beam_size=5, word_timestamps=True, vad_filter=False,
                             condition_on_previous_text=False)
    pal = [dict(word=w.word.strip(), start=round(w.start, 3), end=round(w.end, 3)) for s in seg for w in s.words]
    (A / "asr_palavras_v2.json").write_text(json.dumps(pal, ensure_ascii=False), encoding="utf-8")
    print(len(pal), "palavras")
