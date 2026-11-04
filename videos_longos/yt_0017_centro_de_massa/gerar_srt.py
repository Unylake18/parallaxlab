"""yt_0017 — legenda .srt: alinhamento forçado (ElevenLabs /v1/forced-alignment) da audio/narracao_v42_montada.wav (a pista do master)
com o texto de narracao_tags_v4_2.md ("## Por âncora", sem as tags [ ]); guarda o bruto em audio/alinhamento_forcado_bruto.json (não
realinha se ele existir). Cada legenda: até 2 linhas de ≤ 42 caracteres, quebrando em pontuação (mesma regra do yt_0011).
Saída: renders/legenda - yt0017.srt. A chave vem só de ELEVENLABS_API_KEY.
uso: python gerar_srt.py"""
import json
import os
import re
import sys
import textwrap
import urllib.request
import uuid
from pathlib import Path

U = Path(__file__).resolve().parent
BRUTO = U / "audio" / "alinhamento_forcado_bruto.json"
t = (U / "narracao_tags_v4_2.md").read_text(encoding="utf-8")
t = t[t.index("## Por âncora"):t.index("## Texto corrido")]
txt = " ".join(" ".join(re.sub(r"\[[^\]]*\]", " ", b.split("\n", 1)[1]).split()) for b in re.split(r"^### ", t, flags=re.M)[1:])

if not BRUTO.exists():
    wav = (U / "audio" / "narracao_v42_montada.wav").read_bytes()
    b = uuid.uuid4().hex
    corpo = (f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"narracao.wav\"\r\nContent-Type: audio/wav\r\n\r\n").encode() \
        + wav + (f"\r\n--{b}\r\nContent-Disposition: form-data; name=\"text\"\r\n\r\n{txt}\r\n--{b}--\r\n").encode("utf-8")
    req = urllib.request.Request("https://api.elevenlabs.io/v1/forced-alignment", corpo,
                                 {"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "User-Agent": "parallax-lab/1.0",
                                  "Content-Type": f"multipart/form-data; boundary={b}"})
    try:
        with urllib.request.urlopen(req, timeout=1200) as r:
            BRUTO.write_bytes(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}")

dados = json.loads(BRUTO.read_text(encoding="utf-8"))
ws = [w for w in dados["words"] if w["text"].strip()]
pal = txt.split()
assert len(ws) == len(pal), (len(ws), len(pal))
pal = [(p, w["start"], w["end"]) for p, w in zip(pal, ws)]


def fmt(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


blocos, cur = [], []
for w in pal:
    cur.append(w)
    n = len(" ".join(x[0] for x in cur))
    if w[0][-1] in ".?!:" or (w[0][-1] in ",;" and n > 45) or n > 64:
        blocos.append(cur)
        cur = []
if cur:
    blocos.append(cur)
out = []
for i, b in enumerate(blocos, 1):
    ini, fim = b[0][1], b[-1][2] + 0.25
    if i < len(blocos):
        fim = min(fim, blocos[i][0][1] - 0.02)
    out.append(f"{i}\n{fmt(ini)} --> {fmt(fim)}\n" + "\n".join(textwrap.wrap(" ".join(x[0] for x in b), 42)))
(U / "renders" / "legenda - yt0017.srt").write_text("\n\n".join(out) + "\n", encoding="utf-8")
print(len(blocos), "legendas;", max(len(textwrap.wrap(" ".join(x[0] for x in b), 42)) for b in blocos), "linhas máx;",
      "loss", dados.get("loss"), "; última palavra", round(ws[-1]["end"], 2), "s")
