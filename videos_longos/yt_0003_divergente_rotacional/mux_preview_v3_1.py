"""Junta o vídeo silencioso do preview à voz (narracao_montagem.wav) sem recodificar o vídeo (preview de avaliação, não é o master)."""
import av
from pathlib import Path
P = Path(__file__).resolve().parent
src = P / "renders/m_full/videos/cena/540p15/preview_v3_1.mp4"
wav = P / "audio/narracao_montagem.wav"
out = P / "renders/videos/cena/540p15/preview_v3_1_com_voz.mp4"
with av.open(str(src)) as iv, av.open(str(wav)) as ia, av.open(str(out), "w") as o:
    sv = iv.streams.video[0]; ov = o.add_stream_from_template(sv)
    oa = o.add_stream("aac", rate=44100); oa.layout = "stereo"; oa.bit_rate = 192000
    rs = av.AudioResampler(format="fltp", layout="stereo", rate=44100)
    for p in iv.demux(sv):
        if p.dts is None: continue
        p.stream = ov; o.mux(p)
    for fr in ia.decode(audio=0):
        for f in rs.resample(fr):
            for p in oa.encode(f): o.mux(p)
    for f in rs.resample(None):
        for p in oa.encode(f): o.mux(p)
    for p in oa.encode(None): o.mux(p)
with av.open(str(out)) as c:
    print("video", round(float(c.streams.video[0].duration*c.streams.video[0].time_base),2), "audio", round(float(c.streams.audio[0].duration*c.streams.audio[0].time_base),2), "MB", round(out.stat().st_size/1e6,1))
