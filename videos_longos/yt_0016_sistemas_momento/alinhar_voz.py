"""Alinhamento forçado (ElevenLabs /v1/forced-alignment) da voz v4 do yt_0016: instante de cada palavra, e transcrição (ASR,
/v1/speech-to-text) de cada bloco para conferir a pronúncia (handoff v5 §2–§3). Chave só em ELEVENLABS_API_KEY.
Entrada: narracao_tags.md + audio/narracao_v4.wav (+ audio/blocos_v4/bNN.mp3). Saída: alinhamento_palavras.json, texto_narracao.txt,
audio/asr_v4.json. Uso: uv run --no-sync python alinhar_voz.py [--asr]"""
import io
import json
import os
import re
import sys
import uuid
import urllib.request
import wave
from pathlib import Path

import numpy as np

PASTA = Path(__file__).absolute().parent
CH = os.environ["ELEVENLABS_API_KEY"]


def multipart(campos, arquivo, nome, tipo):
    b = uuid.uuid4().hex
    partes = [f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n'.encode() + v.encode("utf-8") + b"\r\n"
              for k, v in campos.items()]
    partes.append(f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{nome}"\r\nContent-Type: {tipo}\r\n\r\n'.encode()
                  + arquivo + b"\r\n")
    partes.append(f"--{b}--\r\n".encode())
    return b"".join(partes), b


def post(url, corpo, b):
    req = urllib.request.Request(url, data=corpo, method="POST",
                                 headers={"xi-api-key": CH, "Content-Type": f"multipart/form-data; boundary={b}"})
    return json.loads(urllib.request.urlopen(req, timeout=900).read())


def wav16k():
    """A voz em 16 kHz mono (mesma linha do tempo) para o upload ficar leve."""
    with wave.open(str(PASTA / "audio" / os.environ.get("WAV", "narracao_v4.wav"))) as w:
        sr, x = w.getframerate(), np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)
    n = int(len(x) * 16000 / sr)
    y = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.int16)
    bio = io.BytesIO()
    with wave.open(bio, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000); w.writeframes(y.tobytes())
    return bio.getvalue()


def main():
    md = (PASTA / "narracao_tags.md").read_text(encoding="utf-8").split("## Texto corrido (para gravação)")[1].split("\n## ")[0]
    texto = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", md)).strip()
    (PASTA / "texto_narracao.txt").write_text(texto, encoding="utf-8")
    if "--asr" in sys.argv:
        out = []
        for mp3 in sorted((PASTA / "audio" / "blocos_v4").glob("b??.mp3")):
            corpo, b = multipart({"model_id": "scribe_v1", "language_code": "por"}, mp3.read_bytes(), mp3.name, "audio/mpeg")
            r = post("https://api.elevenlabs.io/v1/speech-to-text", corpo, b)
            out.append({"bloco": mp3.stem, "texto": r.get("text", "")})
            print(mp3.stem, len(r.get("text", "")), "caracteres", flush=True)
        (PASTA / "audio" / "asr_v4.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        return
    corpo, b = multipart({"text": texto}, wav16k(), "narracao.wav", "audio/wav")
    r = post("https://api.elevenlabs.io/v1/forced-alignment", corpo, b)
    pal = [dict(word=w["text"].strip(), start=round(w["start"], 3), end=round(w["end"], 3), loss=round(w.get("loss", 0), 3))
           for w in r["words"] if w["text"].strip()]
    (PASTA / os.environ.get("SAIDA", "alinhamento_palavras.json")).write_text(json.dumps(pal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(pal), "palavras; perda média", round(r.get("loss", 0), 3), "; fim", pal[-1]["end"])


if __name__ == "__main__":
    main()
