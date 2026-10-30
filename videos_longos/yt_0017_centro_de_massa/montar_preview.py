"""Emenda os lotes do preview na ordem do vídeo → renders/preview_yt0017_<rodada>_960x540.mp4 (H.264 CRF 14, sem áudio).
Copiado do yt_0016. Rodada "completo" (padrão): PH hook+abertura · P1 T1 · P2 T2 · P3 T3 · P4 T4 · P5 E1, E2, síntese, encerramento; "lote1": PH–P2.
Transição entre lotes (= capítulos), G13: o lote anterior apaga até o fundo em 5 quadros e o novo acende em 5, sem mudar a duração total.
Grava também renders/capitulos_<rodada>.txt (início de cada capítulo, formato do YouTube).
uso: python montar_preview.py [lote1]"""
import json
import sys
from fractions import Fraction
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
M = lambda c: U / f"media_{c}/videos/cena/540p15/{c}.mp4"
RODADA = sys.argv[1] if len(sys.argv) > 1 else "completo"
partes = [("PH", None), ("P1", "ONDE ESTÁ O CENTRO DE MASSA?"), ("P2", "COMO ELE SE MOVE?"), ("P3", "QUE ENERGIA É DO MOVIMENTO RELATIVO?"),
          ("P4", "COMO ACHAR O CENTRO DE MASSA DE UM CORPO INTEIRO?"), ("P5", "EXERCÍCIO 1 · PLACA COM ENTALHE")]
if RODADA == "lote1":
    partes = partes[:3]
DENTRO = {"P5": {"E2-1": "EXERCÍCIO 2 · REMADOR E ESTACA", "S1": "RESUMO", "EN1": "ENCERRAMENTO"}}   # capítulos dentro de um lote
SAI = 5
from PIL import Image
FUNDO = np.asarray(Image.open(U / "fundo_lab.png").convert("RGB").resize((960, 540)), dtype=np.float32)   # v4: apaga até o céu do laboratório
saida = U / "renders" / f"preview_yt0017_{RODADA}_960x540.mp4"
out = av.open(str(saida), "w")
s = out.add_stream("libx264", rate=Fraction(15))
s.width, s.height, s.pix_fmt = 960, 540, "yuv420p"
s.options = {"crf": "14", "preset": "medium"}
t, marcas, ultimo = 0, [], None
for nome, cap in partes:
    c = av.open(str(M(nome)))
    total = c.streams.video[0].frames
    n = 0
    for fr in c.decode(video=0):
        img = fr.to_ndarray(format="rgb24")
        # G13: entre dois lotes (cenas cheias) o anterior apaga até o fundo em 5 quadros e o novo acende em 5, sem os dois a 50%
        if ultimo is not None and n < SAI:
            w = (n + 1) / (SAI + 1)
            img = (img.astype(np.float32) * w + FUNDO * (1 - w) + 0.5).astype(np.uint8)
        if nome != partes[-1][0] and n >= total - SAI:
            w = (total - n) / (SAI + 1)
            img = (img.astype(np.float32) * w + FUNDO * (1 - w) + 0.5).astype(np.uint8)
        for p in s.encode(av.VideoFrame.from_ndarray(img, format="rgb24")):
            out.mux(p)
        n += 1
        last = img
    ultimo = last
    marcas.append((nome, cap, round(t / 15, 1), round(n / 15, 1)))
    import re
    log = (U / f"log_{nome}.txt").read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log):
        if m.group(1) in DENTRO.get(nome, {}):
            marcas.append((nome, DENTRO[nome][m.group(1)], round(t / 15 + float(m.group(2)), 1), 0))
    t += n
    c.close()
for p in s.encode():
    out.mux(p)
out.close()
caps = []
for nome, cap, t0, _ in marcas:
    mm, ss = divmod(int(t0), 60)
    caps.append(f"{mm}:{ss:02d} {cap or 'ABERTURA'}")
(U / "renders" / f"capitulos_{RODADA}.txt").write_text("\n".join(caps) + "\n", encoding="utf-8")
print(json.dumps({"saida": str(saida), "quadros": t, "duracao_s": round(t / 15, 1), "partes": marcas}, ensure_ascii=False))
