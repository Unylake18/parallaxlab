"""v7 FINAL 1920×1080 / 30 fps: emenda os lotes do preview na ordem do vídeo → renders/preview_yt0018_<rodada>_960x540.mp4 (H.264 CRF 14, sem áudio).
Copiado do yt_0017. Rodada "v3" (padrão): PH hook+abertura · PX0 X0, X1 · PX2 · PX3 · PX4 · PX5 · PEP epílogo, síntese, encerramento.
Transição entre lotes (= capítulos), G13: o lote anterior apaga até o fundo em 5 quadros e o novo acende em 5, sem mudar a duração total.
v3 §9: entre PH e PX0 não apaga (o disco do X0-1 já nasceu no fim do A4): os 5 primeiros quadros do PX0 fundem com o último do PH (troca de céu).
Grava também renders/capitulos_<rodada>.txt (início de cada capítulo, formato do YouTube).
uso: python montar_preview.py [lote1]"""
import json
import sys
from fractions import Fraction
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
M = lambda c: U / f"media_F_{c}/videos/cena/1080p30/{c}.mp4"
RODADA = "final"
CONTINUA = {("PH", "PX0")}                    # sem apagar até o fundo nesta emenda
partes = [("PH", None), ("PX0", "PROBLEMA 1 · O DISCO FURADO"), ("PX2", "PROBLEMA 3 · O FIO NO CUBO"), ("PX3", "PROBLEMA 4 · O GAFANHOTO"),
          ("PX4", "PROBLEMA 5 · AS NAVES"), ("PX5", "PROBLEMA 6 · A BALANÇA"), ("PEP", "EPÍLOGO · A LUZ TAMBÉM EMPURRA")]
DENTRO = {"PH": {"A1": "ABERTURA"}, "PX0": {"X1-1": "PROBLEMA 2 · A PLACA COM FURO"}, "PEP": {"S2": "RESUMO", "EN1": "ENCERRAMENTO"}}   # capítulos dentro de um lote
SAI = 10                                      # 5 quadros a 15 fps = 10 quadros a 30 fps (0,33 s)
from PIL import Image
FUNDO = np.asarray(Image.open(U / "fundo_lab.png").convert("RGB").resize((1920, 1080)), dtype=np.float32)   # v4: apaga até o céu do laboratório
saida = U / "renders" / "master_mudo_yt0018_1920x1080.mp4"
out = av.open(str(saida), "w")
s = out.add_stream("libx264", rate=Fraction(30))
s.width, s.height, s.pix_fmt = 1920, 1080, "yuv420p"
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
    marcas.append((nome, cap, round(t / 30, 1), round(n / 30, 1)))
    import re
    log = (U / f"log_F_{nome}.txt").read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", log):
        if m.group(1) in DENTRO.get(nome, {}):
            marcas.append((nome, DENTRO[nome][m.group(1)], round(t / 30 + float(m.group(2)), 1), 0))
    t += n
    c.close()
for p in s.encode():
    out.mux(p)
out.close()
caps = []
for nome, cap, t0, _ in marcas:
    mm, ss = divmod(int(t0), 60)
    caps.append(f"{mm}:{ss:02d} {cap or 'O GAFANHOTO NA FOLHA'}")
(U / "renders" / f"capitulos_{RODADA}.txt").write_text("\n".join(caps) + "\n", encoding="utf-8")
print(json.dumps({"saida": str(saida), "quadros": t, "duracao_s": round(t / 30, 2), "partes": marcas}, ensure_ascii=False))
