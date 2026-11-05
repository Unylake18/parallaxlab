"""Emenda os lotes do preview na ordem do vídeo → renders/preview_yt0020_<rodada>_960x540.mp4 (H.264 CRF 14, sem áudio). Copiado do yt_0019.
Transição entre lotes (= capítulos), G13: o lote anterior apaga até o fundo em 5 quadros e o novo acende em 5, sem mudar a duração total.
Grava também renders/capitulos_<rodada>.txt (início de cada capítulo, formato do YouTube).
uso: python montar_preview.py [rodada]"""
import json
import sys
from fractions import Fraction
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
M = lambda c: U / f"media_{c}/videos/cena/540p15/{c}.mp4"
RODADA = sys.argv[1] if len(sys.argv) > 1 else "v1"
CONTINUA = set()                              # v4 G39: o lote velho sai inteiro (0,4 s) e o novo entra depois (0,4 s); nunca cruzados
partes = [("PH", None), ("PT1", "COMO MEDIR UM GIRO?"), ("PT2", "QUÃO RÁPIDO GIRA?"), ("PT3", "E QUANDO O GIRO ACELERA?"),
          ("PT4", "E CADA PONTO DO CORPO?"), ("PT5", "PARA ONDE APONTA UM GIRO?"), ("PE1", "EXERCÍCIO 1 · O VENTILADOR QUE DESLIGA"),
          ("PE2", "EXERCÍCIO 2 · A CORRENTE DA BICICLETA"), ("PE3", "EXERCÍCIO 3 · QUANTO GIRA A TERRA?"), ("PS", "RESUMO")]
DENTRO = {"PH": {"A1": "ABERTURA"}, "PS": {"EN1": "ENCERRAMENTO E DESAFIO"}}   # capítulos dentro de um lote
SAI = 5                                       # 0,4 s de saída e 0,4 s de entrada entre lotes
from PIL import Image
FUNDO = np.asarray(Image.open(U / "fundo_lab.png").convert("RGB").resize((960, 540)), dtype=np.float32)   # v4: apaga até o céu do laboratório
saida = U / "renders" / f"preview_yt0020_{RODADA}_960x540.mp4"
out = av.open(str(saida), "w")
s = out.add_stream("libx264", rate=Fraction(15))
s.width, s.height, s.pix_fmt = 960, 540, "yuv420p"
s.options = {"crf": "14", "preset": "medium"}
t, marcas, ultimo, anterior = 0, [], None, None
for nome, cap in partes:
    c = av.open(str(M(nome)))
    total = c.streams.video[0].frames
    n = 0
    for fr in c.decode(video=0):
        img = fr.to_ndarray(format="rgb24")
        # G13: entre dois lotes (cenas cheias) o anterior apaga até o fundo em 5 quadros e o novo acende em 5, sem os dois a 50%
        if ultimo is not None and n < SAI:
            w = (n + 1) / (SAI + 1)
            base = ultimo.astype(np.float32) if (anterior, nome) in CONTINUA else FUNDO
            img = (img.astype(np.float32) * w + base * (1 - w) + 0.5).astype(np.uint8)
        prox = partes[[q[0] for q in partes].index(nome) + 1][0] if nome != partes[-1][0] else None
        if prox is not None and (nome, prox) not in CONTINUA and n >= total - SAI:
            w = (total - n) / (SAI + 1)
            img = (img.astype(np.float32) * w + FUNDO * (1 - w) + 0.5).astype(np.uint8)
        for p in s.encode(av.VideoFrame.from_ndarray(img, format="rgb24")):
            out.mux(p)
        n += 1
        last = img
    ultimo, anterior = last, nome
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
    caps.append(f"{mm}:{ss:02d} {cap or 'POR QUE A PONTA DA HÉLICE CHEGA A QUASE 1.000 km/h?'}")
(U / "renders" / f"capitulos_{RODADA}.txt").write_text("\n".join(caps) + "\n", encoding="utf-8")
print(json.dumps({"saida": str(saida), "quadros": t, "duracao_s": round(t / 15, 1), "partes": marcas}, ensure_ascii=False))
