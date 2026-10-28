"""Emenda os lotes do preview v4 na ordem do vídeo → renders/preview_yt0015_v4_960x540.mp4 (H.264 CRF 14, sem áudio).
Ordem: hook (3D) · PA abertura · PT1 T1 · PB T2 · PT3 T3 (2D) · PC T4 · PD T5 · PE E1–E3 · PF T6 · E4-1 (3D) · PG E4-2..E5 · PS · F2 (3D).
Transição entre lotes: dissolve de 0,4 s (6 quadros) do último quadro do lote anterior para o novo, sem mudar a duração total."""
import json
from fractions import Fraction
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
M = lambda c: U / f"media_{c}/videos/cena/540p15/{c}.mp4"
partes = [("hook", U / "renders/hook_960x540.mp4"), ("PA", M("PA")), ("PT1", M("PT1")), ("PB", M("PB")), ("PT3", M("PT3")),
          ("PC", M("PC")), ("PD", M("PD")), ("PE", M("PE")), ("PF", M("PF")), ("E4-1", U / "renders/e4_960x540.mp4"),
          ("PG", M("PG")), ("PS", M("PS")), ("F2", U / "renders/cavalo_960x540.mp4")]
DISS = 6
saida = U / "renders" / "preview_yt0015_v4_960x540.mp4"
out = av.open(str(saida), "w")
s = out.add_stream("libx264", rate=Fraction(15))
s.width, s.height, s.pix_fmt = 960, 540, "yuv420p"
s.options = {"crf": "14", "preset": "medium"}
t, marcas, ultimo = 0, [], None
for nome, arq in partes:
    c = av.open(str(arq))
    n = 0
    for fr in c.decode(video=0):
        img = fr.to_ndarray(format="rgb24")
        if ultimo is not None and n < DISS:
            w = 1 - (n + 1) / (DISS + 1)
            img = (img.astype(np.float32) * (1 - w) + ultimo.astype(np.float32) * w + 0.5).astype(np.uint8)
        for p in s.encode(av.VideoFrame.from_ndarray(img, format="rgb24")):
            out.mux(p)
        n += 1
        last = img
    ultimo = last
    marcas.append((nome, round(t / 15, 1), round(n / 15, 1)))
    t += n
    c.close()
for p in s.encode():
    out.mux(p)
out.close()
print(json.dumps({"saida": str(saida), "quadros": t, "duracao_s": round(t / 15, 1), "partes": marcas}, ensure_ascii=False))
