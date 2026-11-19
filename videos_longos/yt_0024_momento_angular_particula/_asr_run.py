
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
