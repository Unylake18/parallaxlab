"""Cola o WAV (sem recompressão do vídeo) no preview: uso: python mux_audio.py VIDEO.mp4 AUDIO.wav SAIDA.mp4"""
import sys, av
v, a, s = sys.argv[1:4]
iv, ia = av.open(v), av.open(a)
o = av.open(s, "w")
sv = o.add_stream_from_template(iv.streams.video[0])
sa = o.add_stream("aac", rate=44100); sa.layout = "mono"; sa.bit_rate = 192000
for p in iv.demux(iv.streams.video[0]):
    if p.dts is None: continue
    p.stream = sv; o.mux(p)
rs = av.AudioResampler(format="fltp", layout="mono", rate=44100)
for fr in ia.decode(audio=0):
    for r in rs.resample(fr):
        for p in sa.encode(r): o.mux(p)
for p in sa.encode(): o.mux(p)
o.close()
