"""yt_0022: emenda os lotes do preview na ordem do vídeo → renders/preview_yt0022_<rodada>_960x540.mp4 (H.264 CRF 14, sem áudio).
Entre lotes (= capítulos) o anterior apaga até o fundo em 5 quadros e o novo acende em 5, sem mudar a duração total.
Grava também renders/capitulos_<rodada>.txt (início de cada capítulo, formato do YouTube) e renders/quadros_<rodada>.json (quadro absoluto de cada âncora).
uso: python montar_preview.py [rodada]"""
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

import av
import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
M = lambda c: U / f"media_{c}/videos/cena/540p15/{c}.mp4"
RODADA = sys.argv[1] if len(sys.argv) > 1 else "v1"
partes = [
    ("PH", "A RÉGUA E AS DUAS MOEDAS"),
    ("PA", "ABERTURA"),
    ("PT1", "TORQUE E BRAÇO DE ALAVANCA"),
    ("PT2", "TORQUE COMO VETOR"),
    ("PT3", "2ª LEI DE NEWTON DA ROTAÇÃO"),
    ("PT4", "DE VOLTA À RÉGUA"),
    ("PT5", "TRABALHO E POTÊNCIA NO GIRO"),
    ("PT6", "QUANDO NADA ACELERA: EQUILÍBRIO"),
    ("PS", "SÍNTESE"),
]
DENTRO = {"PS": {"S2": "A RESPOSTA DA RÉGUA", "EN2": "DESAFIO"}}
SAI = 5
FUNDO = np.asarray(Image.open(U / "fundo_lab.png").convert("RGB").resize((960, 540)), dtype=np.float32)
saida = U / "renders" / f"preview_yt0022_{RODADA}_960x540.mp4"
(U / "renders").mkdir(exist_ok=True)
out = av.open(str(saida), "w")
s = out.add_stream("libx264", rate=Fraction(15))
s.width, s.height, s.pix_fmt = 960, 540, "yuv420p"
s.options = {"crf": "14", "preset": "medium"}
t, marcas, quadros = 0, [], {}
nomes = [q[0] for q in partes]
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
    marcas.append((cap, round(t / 15, 1)))
    log = (U / f"log_{nome}.txt").read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log):
        quadros[m.group(1)] = t + round(float(m.group(2)) * 15)
        if m.group(1) in DENTRO.get(nome, {}):
            marcas.append((DENTRO[nome][m.group(1)], round(t / 15 + float(m.group(2)), 1)))
    t += n
for pk in s.encode():
    out.mux(pk)
out.close()
caps = [f"{int(t0) // 60}:{int(t0) % 60:02d} {cap}" for cap, t0 in marcas]
(U / "renders" / f"capitulos_{RODADA}.txt").write_text("\n".join(caps) + "\n", encoding="utf-8")
(U / "renders" / f"quadros_{RODADA}.json").write_text(json.dumps(quadros, indent=0), encoding="utf-8")
print(json.dumps({"saida": str(saida), "quadros": t, "duracao_s": round(t / 15, 1), "capitulos": caps}, ensure_ascii=False))
