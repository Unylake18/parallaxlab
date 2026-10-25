"""yt_0013 — master: emenda os grupos do render (cópia do H.264, sem recompressão) e cola a voz sincronizada (AAC).

Uso: uv run --no-sync python montar_final.py   ->  final/master - 0013.mp4
Confere: quadros do vídeo = duração do ritmo × 30 (±1) e CRF gravado no stream.
"""
import json
import re
from fractions import Fraction
from pathlib import Path

import av

P = Path(__file__).resolve().parent
GR = [P / "media_final" / "videos" / "cena" / "1080p30" / f"grupo{i}.mp4" for i in range(1, 6)]
WAV = P / "audio" / "narracao_sync.wav"
OUT = P / "final" / "master - 0013.mp4"

with av.open(str(OUT), "w") as out:
    with av.open(str(GR[0])) as g0:
        vout = out.add_stream_from_template(g0.streams.video[0])
    aout = out.add_stream("aac", rate=44100)
    aout.layout = "mono"
    aout.bit_rate = 192000
    tb = vout.time_base
    off, quadros, pkts = 0, 0, []
    for g in GR:
        with av.open(str(g)) as c:
            s = c.streams.video[0]
            ult = 0
            for pk in c.demux(s):
                if pk.dts is None:
                    continue
                k = Fraction(s.time_base) / Fraction(tb)
                pk.pts = int(pk.pts * k) + off
                pk.dts = int(pk.dts * k) + off
                ult = max(ult, pk.pts)
                pk.stream = vout
                out.mux(pk)
                quadros += 1
            off = ult + int(Fraction(1, 30) / Fraction(tb))
    with av.open(str(WAV)) as a:
        rs = av.AudioResampler(format="fltp", layout="mono", rate=44100)
        for fr in a.decode(a.streams.audio[0]):
            for f2 in rs.resample(fr):
                for pk in aout.encode(f2):
                    out.mux(pk)
        for pk in aout.encode(None):
            out.mux(pk)

dur = json.loads((P / "ritmo.json").read_text(encoding="utf-8"))["dur"]
with av.open(str(OUT)) as c:
    d = b"".join(bytes(p) for _, p in zip(range(4), c.demux(c.streams.video[0])))
    crf = re.search(rb"crf=([0-9.]+)", d)
print(f"master: {OUT.name} · {quadros} quadros ({quadros / 30:.2f} s) · voz {dur:.2f} s · esperado {round(dur * 30)} quadros "
      f"· CRF {crf.group(1).decode() if crf else '?'}")
