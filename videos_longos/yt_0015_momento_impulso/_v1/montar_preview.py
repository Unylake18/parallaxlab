"""Emenda os lotes do preview na ordem do vídeo → renders/preview_yt0015_960x540.mp4 (H.264 CRF 14, sem áudio).
Ordem: P1 (hook+abertura) · T1 (C01-1..5, 3D) · PA (C01-6..C03) · PB (C04..C06) · PC (C07, C08) · PD (C09..C13-1) · T2 (C13-2..5, 3D) · PE (C13-6..fim)."""
import json
import sys
from fractions import Fraction
from pathlib import Path

import av

U = Path(__file__).resolve().parent
partes = [("P1", U / "media_P1/videos/cena/540p15/P1.mp4"), ("T1", U / "renders/c01_960x540.mp4"),
          ("PA", U / "media_PA/videos/cena/540p15/PA.mp4"), ("PB", U / "media_PB/videos/cena/540p15/PB.mp4"),
          ("PC", U / "media_PC/videos/cena/540p15/PC.mp4"), ("PD", U / "media_PD/videos/cena/540p15/PD.mp4"),
          ("T2", U / "renders/c13_960x540.mp4"), ("PE", U / "media_PE/videos/cena/540p15/PE.mp4")]
saida = U / "renders" / "preview_yt0015_960x540.mp4"
out = av.open(str(saida), "w")
s = out.add_stream("libx264", rate=Fraction(15))
s.width, s.height, s.pix_fmt = 960, 540, "yuv420p"
s.options = {"crf": "14", "preset": "medium"}
t, marcas = 0, []
for nome, arq in partes:
    c = av.open(str(arq))
    n = 0
    for fr in c.decode(video=0):
        img = fr.to_ndarray(format="rgb24")
        for p in s.encode(av.VideoFrame.from_ndarray(img, format="rgb24")):
            out.mux(p)
        n += 1
    marcas.append((nome, round(t / 15, 1), round(n / 15, 1)))
    t += n
    c.close()
for p in s.encode():
    out.mux(p)
out.close()
print(json.dumps({"saida": str(saida), "quadros": t, "duracao_s": round(t / 15, 1), "partes": marcas}, ensure_ascii=False))
