import sys, json, numpy as np
from faster_whisper import WhisperModel
a = np.load(sys.argv[1]); m = WhisperModel("small", device="cpu", compute_type="int8")
seg, _ = m.transcribe(a, language="pt", word_timestamps=True, vad_filter=False, beam_size=5)
out = [{"word": w.word.strip(), "start": w.start, "end": w.end} for s in seg for w in s.words]
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False); print(len(out), "palavras")
