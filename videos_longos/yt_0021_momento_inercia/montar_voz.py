"""yt_0021 v9: muxa a voz (audio/narracao_v4.wav) no preview silencioso: vídeo copiado (sem recodificar), áudio AAC 192k. uso: python montar_voz.py v9"""
import sys
from pathlib import Path
import av

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v9"
vin = av.open(str(U / "renders" / f"preview_yt0021_{R}_960x540.mp4"))
ain = av.open(str(U / "audio" / "narracao_v4.wav"))
out = av.open(str(U / "renders" / f"preview_yt0021_{R}_960x540_voz.mp4"), "w")
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
print("ok", out.name if hasattr(out, "name") else "")
