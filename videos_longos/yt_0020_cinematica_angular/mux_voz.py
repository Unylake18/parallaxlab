"""yt_0020 v6 · cola a voz (audio/narracao_v6.wav) no preview silencioso, sem recodificar o vídeo (só conferência). uso: python mux_voz.py ENTRADA.mp4 SAIDA.mp4"""
import sys
from pathlib import Path

import av

U = Path(__file__).resolve().parent
ent, sai = sys.argv[1], sys.argv[2]
iv, ia = av.open(ent), av.open(str(U / "audio" / "narracao_v6.wav"))
o = av.open(sai, "w")
sv = o.add_stream_from_template(iv.streams.video[0])
sa = o.add_stream("aac", rate=44100, layout="mono")
sa.bit_rate = 192000
for p in iv.demux(iv.streams.video[0]):
    if p.dts is None:
        continue
    p.stream = sv
    o.mux(p)
for fr in ia.decode(audio=0):
    fr.pts = None
    for p in sa.encode(fr):
        o.mux(p)
for p in sa.encode(None):
    o.mux(p)
o.close()
print("ok", sai)
