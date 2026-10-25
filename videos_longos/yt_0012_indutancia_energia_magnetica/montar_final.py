"""yt_0012 — master: emenda os grupos do render (cópia do H.264, sem recompressão) e cola a voz sincronizada (AAC).

Uso: uv run --no-sync python montar_final.py [PASTA_DOS_GRUPOS]   ->  final/master - 0012.mp4
Grupos: grupo1.mp4 … grupoN.mp4 (render 1080p30 com SYNC=ritmo.json e SEG=<seções do grupo>).
Confere: quadros do vídeo = duração do ritmo × 30 (±1) e CRF gravado no stream.
"""
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

import av

P = Path(__file__).resolve().parent
PASTA = Path(sys.argv[1]) if len(sys.argv) > 1 else P / "media_final" / "videos" / "cena" / "1080p30"
GR = sorted(PASTA.glob("grupo*.mp4"), key=lambda p: int(re.search(r"\d+", p.stem).group()))
WAV = P / "audio" / "narracao_sync.wav"
OUT = P / "final" / "master - 0012.mp4"
OUT.parent.mkdir(exist_ok=True)

with av.open(str(OUT), "w") as out:
    with av.open(str(GR[0])) as g0:
        vout = out.add_stream_from_template(g0.streams.video[0])
    aout = out.add_stream("aac", rate=44100)
    aout.layout = "mono"
    aout.bit_rate = 256000
    tb = vout.time_base
    off, quadros = 0, 0
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
print(f"master: {OUT.name} · {len(GR)} grupos · {quadros} quadros ({quadros / 30:.2f} s) · ritmo {dur:.2f} s · esperado "
      f"{round(dur * 30)} quadros · CRF {crf.group(1).decode() if crf else '?'}")
