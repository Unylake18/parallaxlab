"""yt_0024 FINAL 1920×1080 / 30 fps: emenda os 8 lotes (media_F_<lote>/videos/cena/1080p30/<lote>.mp4) → renders/video_mudo_yt0024_1920x1080.mp4 (H.264 yuv420p CRF 14, sem áudio)
e renders/capitulos_final.txt. Mesma regra do preview: entre lotes o anterior apaga até o fundo em 10 quadros e o novo acende em 10, sem mudar a duração total.
uso: python montar_final24.py"""
import json
import re
from fractions import Fraction
from pathlib import Path

import av
import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
M = lambda c: U / f"media_F_{c}/videos/cena/1080p30/{c}.mp4"
partes = [("PH", "O DISCO NA MESA COM FURO"), ("PB1", "DE p PARA L"), ("PB2", "UMA RETA TAMBÉM GIRA"), ("PB3", "O QUE MUDA L"), ("PB4", "O CÍRCULO"),
          ("PB5", "FORÇA CENTRAL"), ("PB6", "DE VOLTA À MESA"), ("PS", "RESUMO")]
DENTRO = {"PH": {"A1": "ABERTURA"}, "PS": {"EN": "ENCERRAMENTO"}}
FPS, SAI = 30, 10
FUNDO = np.asarray(Image.open(U / "fundo_lab.png").convert("RGB").resize((1920, 1080)), dtype=np.float32)
saida = U / "renders" / "video_mudo_yt0024_1920x1080.mp4"
out = av.open(str(saida), "w")
s = out.add_stream("libx264", rate=Fraction(FPS))
s.width, s.height, s.pix_fmt = 1920, 1080, "yuv420p"
s.options = {"crf": "14", "preset": "medium"}
t, marcas = 0, []
for k, (nome, cap) in enumerate(partes):
    c = av.open(str(M(nome)))
    total = c.streams.video[0].frames
    n = 0
    for fr in c.decode(video=0):
        img = fr.to_ndarray(format="rgb24")
        if k > 0 and n < SAI:
            w = (n + 1) / (SAI + 1)
            img = (img.astype(np.float32) * w + FUNDO * (1 - w) + 0.5).astype(np.uint8)
        if k < len(partes) - 1 and n >= total - SAI:
            w = (total - n) / (SAI + 1)
            img = (img.astype(np.float32) * w + FUNDO * (1 - w) + 0.5).astype(np.uint8)
        for pk in s.encode(av.VideoFrame.from_ndarray(img, format="rgb24")):
            out.mux(pk)
        n += 1
    c.close()
    marcas.append((cap, round(t / FPS, 1)))
    log = (U / f"log_F_{nome}.txt").read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log):
        if m.group(1) in DENTRO.get(nome, {}):
            marcas.append((DENTRO[nome][m.group(1)], round(t / FPS + float(m.group(2)), 1)))
    t += n
for pk in s.encode():
    out.mux(pk)
out.close()
caps = [f"{int(t0) // 60}:{int(t0) % 60:02d} {cap}" for cap, t0 in marcas]
(U / "renders" / "capitulos_final.txt").write_text("\n".join(caps) + "\n", encoding="utf-8")
print(json.dumps({"saida": str(saida), "quadros": t, "duracao_s": round(t / FPS, 2), "capitulos": caps}, ensure_ascii=False))
