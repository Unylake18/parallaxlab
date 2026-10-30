"""MASTER final (1920×1080, 30 fps, H.264 CRF 14 + AAC 192 kb/s) a partir dos lotes do render final; mesma montagem do preview v7: emenda os lotes na ordem do vídeo (transição em sequência do v4, sem mudar a duração) e cola a voz
audio/narracao_v4_pausas.wav deslocada de PAD (ancoras.json) → renders/master_yt0016_1920x1080_30fps.mp4 (H.264 CRF 14 + AAC 192k).
Grava também renders/capitulos_final.txt (início de cada capítulo, formato do YouTube) e confere a duração de cada lote contra as âncoras."""
import json
import wave
from fractions import Fraction
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
M = lambda c: U / f"media_{c}/videos/cena/1080p30/{c}.mp4"
partes = [("PH", None, "H1"), ("P7", "SISTEMAS DE PARTÍCULAS", "T7-1"), ("P8", "FORÇA INTERNA NÃO MOVE O SISTEMA", "T8-1"),
          ("P9", "ESCOLHER O SISTEMA", "T9-1"), ("P10", "COMO A ENERGIA SE DIVIDE", "T10-1"),
          ("Q6", "EXERCÍCIO 6 · AGARRAR OU REBATER", "E6-1"), ("Q7", "EXERCÍCIO 7 · O CAÇADOR NO LAGO", "E7-1"),
          ("Q8", "EXERCÍCIO 8 · OS GASES DO RIFLE", "E8-1"), ("Q9", "EXERCÍCIO 9 · NEWTON E A LUZ", "E9-1"),
          ("PC", "A LUZ TAMBÉM TEM MOMENTO", "C-1"), ("PS", "RESUMO", "S1")]
ANC = json.loads((U / "ancoras.json").read_text(encoding="utf-8"))
PAD = ANC["pad"]
DISS = 12
from PIL import Image
FUNDO = np.asarray(Image.open(U / "assets_unidade" / "fundo_lab_1920x1080.png").convert("RGB"))
saida = U / "renders" / "master_yt0016_1920x1080_30fps.mp4"
out = av.open(str(saida), "w")
s = out.add_stream("libx264", rate=Fraction(30))
s.width, s.height, s.pix_fmt = 1920, 1080, "yuv420p"
s.options = {"crf": "14", "preset": "medium"}
sa = out.add_stream("aac", rate=44100)
sa.layout = "mono"
sa.bit_rate = 192000
t, marcas, ultimo = 0, [], None
for nome, cap, aid in partes:
    c = av.open(str(M(nome)))
    n = 0
    for fr in c.decode(video=0):
        img = fr.to_ndarray(format="rgb24")
        if ultimo is not None and n < DISS:
            fundo = FUNDO                         # v7: a transição passa pelo céu da unidade (não pelo preto antigo)
            if n < 6:
                u = (n + 1) / 6
                q = ultimo.astype(np.float32) * (1 - u) + fundo * u
            else:
                u = (n - 5) / (DISS - 5)
                q = fundo.astype(np.float32) * (1 - u) + img.astype(np.float32) * u
            q = (q + 0.5).astype(np.uint8)
            q[:68, :] = img[:68, :]
            q[:, 1600:][:220] = img[:220, 1600:]
            img = q
        for p in s.encode(av.VideoFrame.from_ndarray(img, format="rgb24")):
            out.mux(p)
        n += 1
        last = img
    ultimo = last
    esperado = round(ANC["ancoras"][aid]["t0"] * 30)
    marcas.append((nome, cap, round(t / 30, 2), round(n / 30, 2), t - esperado))
    t += n
    c.close()
for p in s.encode():
    out.mux(p)
# a voz, deslocada de PAD, cortada/estendida até o fim do vídeo
with wave.open(str(U / "audio" / "narracao_v4_pausas.wav")) as w:
    sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
n_tot = int(round(t / 30 * sr))
pad = int(round(PAD * sr))
y = np.zeros(n_tot, np.int16)
seg = x[max(0, -pad):][: n_tot - max(0, pad)]
y[max(0, pad):max(0, pad) + len(seg)] = seg
pts = 0
for i in range(0, n_tot, 1024):
    bloco = y[i:i + 1024].reshape(1, -1)
    fr = av.AudioFrame.from_ndarray(bloco, format="s16", layout="mono")
    fr.sample_rate = sr
    fr.pts = pts
    pts += bloco.shape[1]
    for p in sa.encode(fr):
        out.mux(p)
for p in sa.encode():
    out.mux(p)
out.close()
caps = []
for nome, cap, t0, _, _ in marcas:
    mm, ss = divmod(int(t0), 60)
    caps.append(f"{mm}:{ss:02d} {cap or 'ABERTURA'}")
(U / "renders" / "capitulos_final.txt").write_text("\n".join(caps) + "\n", encoding="utf-8")
print(json.dumps({"saida": str(saida), "quadros": t, "duracao_s": round(t / 30, 2), "esperado_s": ANC["total"],
                  "partes": marcas}, ensure_ascii=False))
