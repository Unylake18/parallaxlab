import av
src='renders/preview_yt0022_v6_960x540.mp4'; wav='audio/narracao_v3.wav'; out='renders/preview_yt0022_v6_960x540_voz.mp4'
iv=av.open(src); ia=av.open(wav); oc=av.open(out,'w')
vs=iv.streams.video[0]; ov=oc.add_stream_from_template(vs)
a=ia.streams.audio[0]; oa=oc.add_stream('aac',rate=a.rate); oa.layout='mono' if a.channels==1 else 'stereo'; oa.bit_rate=192000
for p in iv.demux(vs):
    if p.dts is None: continue
    p.stream=ov; oc.mux(p)
for f in ia.decode(a):
    f.pts=None
    for p in oa.encode(f): oc.mux(p)
for p in oa.encode(None): oc.mux(p)
oc.close(); print('ok')
