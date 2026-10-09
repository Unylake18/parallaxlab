"""yt_0002 — junta os trechos do render final (sem recompressão) e põe a narração de montagem (AAC).

Uso: uv run --no-sync python videos_longos/yt_0002_lei_gauss/montar_final.py SAIDA.mp4 TRECHO1.mp4 TRECHO2.mp4 ...
Os trechos vêm de renders paralelos com SO=grupos de blocos em ordem; todos têm o mesmo encoder (libx264, crf 14,
1920×1080, 30 fps, yuv420p). Se os parâmetros do H.264 (extradata) diferirem, o script para em vez de colar.
"""

import sys
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory

import av

PASTA = Path(__file__).resolve().parent
AUDIO = PASTA / "audio" / "narracao_montagem.wav"


def colar(trechos, destino):
    ins = [av.open(str(t)) for t in trechos]
    vs = [c.streams.video[0] for c in ins]
    ref = vs[0].codec_context.extradata
    for t, v in zip(trechos, vs):
        assert (v.width, v.height, round(float(v.base_rate)), v.codec_context.name) == (1920, 1080, 30, "h264"), t
        assert v.codec_context.extradata == ref, f"parâmetros H.264 diferentes em {t}"
    out = av.open(str(destino), "w")
    vo = out.add_stream_from_template(vs[0])
    quadros, off = 0, 0
    for c, v in zip(ins, vs):
        n_pk, base = 0, None
        for pk in c.demux(v):
            if pk.dts is None:
                continue
            if base is None:
                base = pk.dts
            pk.pts = pk.pts - base + off if pk.pts is not None else None
            pk.dts = pk.dts - base + off
            pk.stream = vo
            out.mux(pk)
            n_pk += 1
        frames = v.frames or n_pk
        quadros += frames
        off += int(round(frames / 30 / v.time_base))          # avança o relógio do trecho em unidades do time_base
        assert all(x.time_base == v.time_base for x in vs), "time_base diferente entre trechos"
        print(f"  {Path(c.name).parent.parent.parent.parent.name}: {frames} quadros")
    out.close()
    for c in ins:
        c.close()
    return quadros


def mux(video, audio, destino):
    with av.open(str(video)) as vi, av.open(str(audio)) as ai, \
            av.open(str(destino), "w", options={"movflags": "+faststart"}) as out:
        vin = vi.streams.video[0]
        vout = out.add_stream_from_template(vin)
        ain = ai.streams.audio[0]
        aout = out.add_stream("aac", rate=48000)
        aout.layout = "stereo"
        aout.bit_rate = 320_000
        rs = av.AudioResampler(format="fltp", layout="stereo", rate=48000)

        def apk():
            for fr in ai.decode(ain):
                for f2 in rs.resample(fr):
                    yield from aout.encode(f2)
            for f2 in rs.resample(None):
                yield from aout.encode(f2)
            yield from aout.encode(None)

        def vpk():
            for pk in vi.demux(vin):
                if pk.dts is not None:
                    pk.stream = vout
                    yield pk
        A, V = apk(), vpk()
        a, v = next(A, None), next(V, None)
        while a is not None or v is not None:
            ta = float(a.dts * a.time_base) if a is not None and a.dts is not None else float("inf")
            tv = float(v.dts * v.time_base) if v is not None else float("inf")
            if tv <= ta:
                out.mux(v)
                v = next(V, None)
            else:
                out.mux(a)
                a = next(A, None)


def main():
    destino, trechos = Path(sys.argv[1]), [Path(t) for t in sys.argv[2:]]
    destino.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as d:
        mudo = Path(d) / "video.mp4"
        q = colar(trechos, mudo)
        print(f"vídeo: {q} quadros = {q / 30:.3f} s")
        mux(mudo, AUDIO, destino)
    with av.open(str(destino)) as r:
        v, a = r.streams.video[0], r.streams.audio[0]
        print(f"{destino.name}: {v.width}×{v.height} {float(v.average_rate):.0f} fps, vídeo {float(v.duration * v.time_base):.3f} s, "
              f"áudio {float(a.duration * a.time_base):.3f} s ({a.codec_context.name} {a.rate} Hz), "
              f"{destino.stat().st_size / 1e6:.0f} MB")


if __name__ == "__main__":
    main()
