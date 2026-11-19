"""yt_0020 · ASR só para os tempos por palavra: etapa 1 (.venv do projeto) decodifica o WAV para 16 kHz float32 (.npy); etapa 2 (~/asr_venv, faster-whisper small) transcreve.
uso: .venv/Scripts/python.exe asr_voz.py 1   e   ~/asr_venv/Scripts/python.exe asr_voz.py 2"""
import json
import sys
from pathlib import Path

import numpy as np

A = Path(__file__).resolve().parent / "audio"
if sys.argv[1] == "1":
    import av
    out = []
    with av.open(str(A / "narracao_v6.wav")) as c:
        rs = av.AudioResampler(format="flt", layout="mono", rate=16000)
        for fr in c.decode(audio=0):
            for r in rs.resample(fr):
                out.append(r.to_ndarray().reshape(-1))
        for r in rs.resample(None):
            out.append(r.to_ndarray().reshape(-1))
    np.save(A / "_v6_16k.npy", np.concatenate(out).astype(np.float32))
    print("ok", sum(len(x) for x in out) / 16000, "s")
else:
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cpu", compute_type="int8")
    seg, info = m.transcribe(np.load(A / "_v6_16k.npy"), language="pt", beam_size=5, word_timestamps=True, vad_filter=False, condition_on_previous_text=False)
    pal = [dict(word=w.word.strip(), start=round(w.start, 3), end=round(w.end, 3)) for s in seg for w in s.words]
    (A / "asr_palavras_v6.json").write_text(json.dumps(pal, ensure_ascii=False), encoding="utf-8")
    print(len(pal), "palavras")
