"""yt_0025: emenda os 8 lotes na ordem do vídeo (H.264 yuv420p CRF 14, sem áudio) e grava os capítulos (formato do YouTube).
Mesma regra do yt_0021/yt_0022: entre lotes (= capítulos) o anterior apaga até o fundo nos últimos quadros e o novo acende nos primeiros, sem mudar a duração total.
uso: python montar_final25.py preview   -> renders/preview_yt0025_v6_completo_960x540.mp4  (media_<lote>/videos/cena/540p15, 15 fps)
     python montar_final25.py final     -> renders/visual_mudo_yt0025_1920x1080.mp4        (media_F_<lote>/videos/cena/1080p30, 30 fps)
Depois, a voz: python montar_final25.py voz ARQ_VIDEO.mp4 ARQ_SAIDA.mp4  (vídeo copiado sem recompressão, áudio AAC 192k do WAV)."""
import json
import sys
from fractions import Fraction
from pathlib import Path

import av
import numpy as np
from PIL import Image

U = Path(__file__).resolve().parent
partes = [("PH", "COMO EXISTE TORQUE SEM AUMENTAR O GIRO?"), ("PB1", "UM L QUE SÓ VIRA"), ("PB2", "UM CORPO INTEIRO"), ("PB3", "O HALTERE TORTO"),
          ("PB4", "EIXO PRINCIPAL"), ("PB5", "O QUE OS MANCAIS FAZEM"), ("PB6", "A RODA"), ("PS", "RESUMO")]
modo = sys.argv[1] if len(sys.argv) > 1 else "preview"
if modo == "voz":
    vin, sai = av.open(sys.argv[2]), Path(sys.argv[3])
    ain = av.open(str(U / "audio" / "narracao_v2.wav"))
    out = av.open(str(sai), "w")
    sv = out.add_stream_from_template(vin.streams.video[0])
    sa = out.add_stream("aac", rate=44100)
    sa.bit_rate = 192000
    for pk in vin.demux(vin.streams.video[0]):
        if pk.dts is None:
            continue
        pk.stream = sv
        out.mux(pk)
    for fr in ain.decode(audio=0):
        fr.pts = None
        for pk in sa.encode(fr):
            out.mux(pk)
    for pk in sa.encode():
        out.mux(pk)
    out.close()
    print("ok", sai)
    sys.exit()
FINAL = modo == "final"
FPS, W, H, SAI = (30, 1920, 1080, 10) if FINAL else (15, 960, 540, 5)
M = (lambda c: U / f"media_F_{c}/videos/cena/1080p30/{c}.mp4") if FINAL else (lambda c: U / f"media_{c}/videos/cena/540p15/{c}.mp4")
FUNDO = np.asarray(Image.open(U / "fundo_lab.png").convert("RGB").resize((W, H)), dtype=np.float32)
saida = U / "renders" / ("visual_mudo_yt0025_1920x1080.mp4" if FINAL else "preview_yt0025_v6_completo_960x540.mp4")
out = av.open(str(saida), "w")
s = out.add_stream("libx264", rate=Fraction(FPS))
s.width, s.height, s.pix_fmt = W, H, "yuv420p"
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
    t += n
for pk in s.encode():
    out.mux(pk)
out.close()
caps = [f"{int(t0) // 60}:{int(t0) % 60:02d} {cap}" for cap, t0 in marcas]
(U / "renders" / ("capitulos_final.txt" if FINAL else "capitulos_v6.txt")).write_text("\n".join(caps) + "\n", encoding="utf-8")
print(json.dumps({"saida": str(saida), "quadros": t, "duracao_s": round(t / FPS, 2), "capitulos": caps}, ensure_ascii=False))
