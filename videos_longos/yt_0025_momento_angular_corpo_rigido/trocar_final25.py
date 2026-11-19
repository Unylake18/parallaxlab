"""yt_0025 · voz v2 (revisão do encerramento): regera SÓ o último parágrafo (a pergunta final foi reescrita: «massa a mais só de um lado»)
e cola no WAV atual (audio/narracao_v2.wav). Backup do WAV anterior em audio/narracao_v2_antes_final.wav.
A chave só vem do ambiente (ELEVENLABS_API_KEY); nunca é gravada.
uso: python trocar_final25.py [--seco]"""
import importlib.util
import json
import os
import re
import shutil
import sys
import unicodedata
import wave
from pathlib import Path

import numpy as np

U = Path(__file__).resolve().parent
ROOT = U.parents[1]
spec = importlib.util.spec_from_file_location("gv", ROOT / "videos" / "gerar_voz_elevenlabs.py")
gv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gv)
VOZ, MODELO, FMT = "qw7jgPZWOKrl10GsjQ82", "eleven_v4", "mp3_44100_192"
NOVO = ("[happy] Se essas conexões ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos. "
        "E deixa nos comentários: se a roda tivesse massa a mais só de um lado, os apoios sentiriam apenas um binário, "
        "ou apareceria também uma força que gira junto com a roda? Até a próxima!")
sem_acento = lambda s: "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
al = json.loads((U / "alinhamento_palavras.json").read_text(encoding="utf-8"))
palavras = [sem_acento(a["word"]).lower() for a in al]
k = next(i for i in range(len(palavras) - 2) if palavras[i:i + 3] == ["se", "essas", "conexoes"])
t0 = al[k]["start"]
wav = U / "audio" / "narracao_v2.wav"
with wave.open(str(wav)) as w:
    fr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
print(f"início do último parágrafo: {t0:.2f} s; WAV atual {len(x) / fr:.2f} s; trecho antigo {len(x) / fr - t0:.2f} s")
if "--seco" in sys.argv:
    sys.exit()
chave = os.environ.get("ELEVENLABS_API_KEY")
if not chave:
    sys.exit("ELEVENLABS_API_KEY ausente")
jan = int(0.005 * fr)
i0, i1 = int(max(0, t0 - 0.05) * fr), int((t0 + 0.05) * fr)
e = np.convolve(np.abs(x[i0:i1]), np.ones(jan) / jan, mode="same")
corte = i0 + int(np.argmin(e))
mp3 = gv.sintetizar(chave, VOZ, MODELO, FMT, NOVO, None, None, None)
pcm = np.frombuffer(gv.decodificar_mp3(mp3), dtype=np.int16).astype(np.float32)
ativo = np.where(np.abs(pcm) > 600)[0]
pcm = pcm[: min(len(pcm), ativo[-1] + int(0.30 * fr))] if len(ativo) else pcm
orig = x[corte:]
ganho = float(np.sqrt((orig ** 2).mean()) / max(1.0, np.sqrt((pcm[pcm != 0] ** 2).mean())))
pcm = np.clip(pcm * ganho, -32768, 32767)
print(f"antigo {len(orig) / fr:.2f} s -> novo {len(pcm) / fr:.2f} s (ganho {ganho:.2f}); {(len(pcm) - len(orig)) / fr:+.2f} s")
shutil.copy2(wav, U / "audio" / "narracao_v2_antes_final.wav")
y = np.concatenate([x[:corte], pcm])
with wave.open(str(wav), "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(fr)
    w.writeframes(np.clip(y, -32768, 32767).astype(np.int16).tobytes())
print(f"{wav.name}: {len(y) / fr:.2f} s")
