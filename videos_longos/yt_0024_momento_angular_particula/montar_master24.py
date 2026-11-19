"""yt_0024: cola a voz (audio/narracao_v1.wav) no vídeo mudo 1080p (renders/video_mudo_yt0024_1920x1080.mp4) SEM recodificar o vídeo (cópia do fluxo),
áudio AAC 192k → renders/yt_0024_final_master_limpo_1920x1080.mp4. Confere duração do vídeo × WAV."""
import re
import wave
from pathlib import Path
import av

U = Path(__file__).resolve().parent
vin = av.open(str(U / "renders" / "video_mudo_yt0024_1920x1080.mp4"))
ain = av.open(str(U / "audio" / "narracao_v1.wav"))
saida = U / "renders" / "yt_0024_final_master_limpo_1920x1080.mp4"
out = av.open(str(saida), "w")
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
w = wave.open(str(U / "audio" / "narracao_v1.wav"))
dwav = w.getnframes() / w.getframerate()
c = av.open(str(saida))
v = c.streams.video[0]
dv = float(v.duration * v.time_base) if v.duration else float(c.duration) / 1e6
dados = b"".join(bytes(p) for _, p in zip(range(4), av.open(str(saida)).demux(av.open(str(saida)).streams.video[0])))
c2 = av.open(str(saida)); d = b"".join(bytes(p) for _, p in zip(range(4), c2.demux(c2.streams.video[0])))
crf = re.search(rb"crf=([0-9.]+)", d)
print(f"master {v.width}x{v.height} fps {float(v.average_rate):.3f}; vídeo {dv:.2f} s; WAV {dwav:.2f} s; dif {dv - dwav:+.2f} s; crf={crf.group(1).decode() if crf else '?'}")
