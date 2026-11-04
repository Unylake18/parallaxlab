"""Cola a voz (audio/narracao_sync.wav) no preview composto, sem recomprimir o vídeo (cópia do fluxo H.264; áudio AAC 192 kb/s).
Uso (na raiz): uv run python videos/vid_0031_halo_22/qa/muxar_voz.py  ->  renders/preview_voz_540x960.mp4"""
from pathlib import Path

import av

UNIT = Path(__file__).resolve().parents[1]
import sys
ORIG = UNIT / 'renders' / (sys.argv[1] if len(sys.argv) > 1 else 'preview_540x960.mp4')
WAV = UNIT / 'audio' / 'narracao_sync.wav'
DEST = UNIT / 'renders' / (sys.argv[2] if len(sys.argv) > 2 else 'preview_voz_540x960.mp4')

with av.open(str(ORIG)) as vin, av.open(str(WAV)) as ain, av.open(str(DEST), 'w') as out:
    vs = out.add_stream_from_template(vin.streams.video[0])
    sr = ain.streams.audio[0].rate
    ast = out.add_stream('aac', rate=sr)
    ast.layout = 'mono'
    ast.bit_rate = 192000
    for pkt in vin.demux(vin.streams.video[0]):
        if pkt.dts is None:
            continue
        pkt.stream = vs
        out.mux(pkt)
    rs = av.AudioResampler(format='fltp', layout='mono', rate=sr)
    for fr in ain.decode(audio=0):
        for r in rs.resample(fr):
            for p in ast.encode(r):
                out.mux(p)
    for p in ast.encode(None):
        out.mux(p)
with av.open(str(DEST)) as c:
    v, a = c.streams.video[0], c.streams.audio[0]
    print('vídeo %.2f s · áudio %.2f s' % (float(v.duration * v.time_base), float(a.duration * a.time_base)))
