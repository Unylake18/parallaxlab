"""yt_0010 — põe a narração (audio/narracao_v4.wav) no render mudo, sem recomprimir o vídeo, e gera legenda.srt.

Uso: uv run --no-sync python videos_longos/yt_0010_fem_movimento/montar_final.py VIDEO_MUDO.mp4 SAIDA.mp4
O vídeo nasce com o relógio da voz (t da cena = t do áudio), então o áudio entra em t = 0, sem deslocamento.
"""
import json
import sys
from pathlib import Path

import av

PASTA = Path(__file__).resolve().parent
AUDIO = PASTA / "audio" / "narracao_v4.wav"


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



def srt(destino):
    """Legenda por frase (texto sem tags), tempo do vídeo final."""
    fr = json.load(open(PASTA / "frases.json", encoding="utf-8"))

    def t(x):
        h, r = divmod(int(round(x * 1000)), 3600000)
        m, r = divmod(r, 60000)
        s, ms = divmod(r, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    cues = [f for k in sorted(fr) for f in fr[k]]
    linhas = []
    for i, f in enumerate(cues, 1):
        fim = min(f["t1"] + 0.15, cues[i]["t0"] - 0.02 if i < len(cues) else f["t1"] + 0.5)
        linhas += [str(i), f"{t(f['t0'])} --> {t(max(fim, f['t0'] + 0.4))}", f["texto"], ""]
    Path(destino).write_text("\n".join(linhas), encoding="utf-8")
    return len(cues)


def main():
    video, destino = Path(sys.argv[1]), Path(sys.argv[2])
    destino.parent.mkdir(parents=True, exist_ok=True)
    mux(video, AUDIO, destino)
    n = srt(destino.with_suffix(".srt"))
    with av.open(str(destino)) as r:
        v, a = r.streams.video[0], r.streams.audio[0]
        print(f"{destino.name}: {v.width}×{v.height} {float(v.average_rate):.0f} fps, vídeo {float(v.duration * v.time_base):.3f} s, "
              f"áudio {float(a.duration * a.time_base):.3f} s, {destino.stat().st_size / 1e6:.0f} MB; {n} legendas")


if __name__ == "__main__":
    main()
