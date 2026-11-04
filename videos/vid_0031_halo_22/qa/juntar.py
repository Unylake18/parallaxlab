"""Junta renders/seg_0..5.mp4 (cópia do fluxo H.264, sem recomprimir) e cola a voz (audio/narracao_sync.wav, AAC 192 kb/s).
Uso (na raiz): uv run --no-sync python videos/vid_0031_halo_22/qa/juntar.py  ->  renders/vid_0031_halo_22_final_master_limpo.mp4"""
from fractions import Fraction
from pathlib import Path

import av

UNIT = Path(__file__).resolve().parents[1]
SEGS = [UNIT / 'renders' / f'seg_{i}.mp4' for i in range(7)]
WAV = UNIT / 'audio' / 'narracao_sync.wav'
DEST = UNIT / 'renders' / 'vid_0031_halo_22_final_master_limpo.mp4'

with av.open(str(DEST), 'w') as out, av.open(str(WAV)) as ain:
    with av.open(str(SEGS[0])) as c0:
        vs = out.add_stream_from_template(c0.streams.video[0])
    sr = ain.streams.audio[0].rate
    ast = out.add_stream('aac', rate=sr)
    ast.layout = 'mono'
    ast.bit_rate = 192000
    off = 0                                              # deslocamento (em ticks do time_base do vídeo) de cada segmento
    tb = vs.time_base
    quadro = int(round(1 / (30 * tb)))                   # 1 quadro a 30 fps em ticks
    total = 0
    for seg in SEGS:
        with av.open(str(seg)) as c:
            v = c.streams.video[0]
            pkts = [p for p in c.demux(v) if p.dts is not None]
            dts0 = min(p.dts for p in pkts)
            for p in pkts:
                p.stream = vs
                p.pts = p.pts - dts0 + off
                p.dts = p.dts - dts0 + off
                out.mux(p)
            n = len(pkts)
        off += n * quadro
        total += n
    rs = av.AudioResampler(format='fltp', layout='mono', rate=sr)
    for fr in ain.decode(audio=0):
        for r in rs.resample(fr):
            for p in ast.encode(r):
                out.mux(p)
    for p in ast.encode(None):
        out.mux(p)
print('quadros', total)
with av.open(str(DEST)) as c:
    v, a = c.streams.video[0], c.streams.audio[0]
    print('vídeo %.2f s · áudio %.2f s · %dx%d' % (float(v.duration * v.time_base), float(a.duration * a.time_base), v.width, v.height))
