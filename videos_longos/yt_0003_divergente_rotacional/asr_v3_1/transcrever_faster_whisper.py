"""Transcrição local (faster-whisper) do áudio do preview com voz — roda em venv ISOLADO fora do repositório.
Uso: <venv>/Scripts/python.exe transcrever_faster_whisper.py <audio.wav> <saida_dir> [modelo]
Não usa o texto da narração: reconhece o que foi efetivamente pronunciado."""
import json, os, sys, time
from pathlib import Path
site = Path(sys.prefix) / "Lib" / "site-packages" / "nvidia"
for d in site.glob("*/bin"):
    os.add_dll_directory(str(d)); os.environ["PATH"] = str(d) + os.pathsep + os.environ["PATH"]
from faster_whisper import WhisperModel
audio, out = Path(sys.argv[1]), Path(sys.argv[2])
modelo = sys.argv[3] if len(sys.argv) > 3 else "large-v3"
CFG = dict(language="pt", beam_size=5, word_timestamps=True, vad_filter=False, condition_on_previous_text=False,
           temperature=0.0, no_speech_threshold=0.6, compression_ratio_threshold=2.4)
m = WhisperModel(modelo, device="cuda", compute_type="float16", download_root=os.environ.get("HF_HOME"))
t0 = time.time()
segs, info = m.transcribe(str(audio), **CFG)
saida = []
for s in segs:
    saida.append({"id": s.id, "start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(),
                  "avg_logprob": round(s.avg_logprob, 3), "no_speech_prob": round(s.no_speech_prob, 3),
                  "words": [{"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3), "prob": round(w.probability, 3)} for w in (s.words or [])]})
    if len(saida) % 20 == 0:
        print(f"{len(saida)} segmentos até {s.end:.0f}s ({time.time() - t0:.0f}s)", flush=True)
meta = {"modelo": modelo, "biblioteca": "faster-whisper 1.2.1 / ctranslate2 4.8.3", "dispositivo": "cuda (RTX 2060 6GB)", "compute_type": "float16",
        "config": CFG, "idioma_detectado": info.language, "prob_idioma": round(info.language_probability, 4), "duracao_audio_s": round(info.duration, 2),
        "audio": audio.name, "tempo_processamento_s": round(time.time() - t0, 1), "initial_prompt": None}
(out / "transcricao_asr.json").write_text(json.dumps({"meta": meta, "segmentos": saida}, ensure_ascii=False, indent=1), encoding="utf-8")
def ts(t):
    return f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{t % 60:06.3f}".replace(".", ",")
(out / "transcricao_asr.srt").write_text("\n".join(f"{i}\n{ts(s['start'])} --> {ts(s['end'])}\n{s['text']}\n" for i, s in enumerate(saida, 1)), encoding="utf-8")
print("fim", len(saida), "segmentos;", meta["tempo_processamento_s"], "s")
