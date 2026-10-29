"""yt_0015 — alinhamento forçado (ElevenLabs /v1/forced-alignment) da narracao_v4.wav com o texto sem tags (cópia do yt_0014).

Uso: uv run --no-sync python audio/alinhar.py  ->  audio/alinhamento_forcado_bruto.json (palavras com início/fim)
A chave vem só de ELEVENLABS_API_KEY (ambiente).
"""
import json
import os
import re
import sys
import uuid
import urllib.error
import urllib.request
from pathlib import Path

P = Path(__file__).resolve().parent
txt = (P.parent / "narracao_tags.md").read_text(encoding="utf-8").split("## Texto corrido (para gravação)", 1)[1]
txt = re.sub(r"\[[^\]]*\]\s*", "", txt)
txt = " ".join(txt.split())
(P / "texto_voz_v4.txt").write_text(txt + "\n", encoding="utf-8")
chave = os.environ["ELEVENLABS_API_KEY"]
wav = (P / "narracao_v4.wav").read_bytes()
b = uuid.uuid4().hex
corpo = (f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"narracao_v4.wav\"\r\n"
         f"Content-Type: audio/wav\r\n\r\n").encode() + wav + \
        (f"\r\n--{b}\r\nContent-Disposition: form-data; name=\"text\"\r\n\r\n{txt}\r\n--{b}--\r\n").encode("utf-8")
req = urllib.request.Request("https://api.elevenlabs.io/v1/forced-alignment", corpo,
                             {"xi-api-key": chave, "Content-Type": f"multipart/form-data; boundary={b}",
                              "User-Agent": "parallax-lab/1.0"})
try:
    with urllib.request.urlopen(req, timeout=900) as r:
        dados = json.loads(r.read())
except urllib.error.HTTPError as e:
    sys.exit(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}")
(P / "alinhamento_forcado_bruto.json").write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
ws = [w for w in dados["words"] if w["text"].strip()]
print(len(ws), "palavras; texto", len(txt.split()), "; loss", dados.get("loss"), "; fim", ws[-1]["end"])
