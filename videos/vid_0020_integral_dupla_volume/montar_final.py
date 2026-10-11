"""Entrega o render nativo com AAC 320 kb/s e relógio CFR, sem recodificar imagens."""
from fractions import Fraction
import json
from pathlib import Path
import av

UNIT = Path(__file__).resolve().parent
OUT = UNIT.parents[1] / "media/vid_0020_final"
VISUAL = OUT / "videos/cena_final/1920p30/IntegralDuplaVolume020Final.mp4"
AUDIO = UNIT / "audio/narracao_final.wav"
TARGET = UNIT / "final_legendado.mp4"
FPS = 30


def encode_audio():
    target = OUT / "narracao_320k.m4a"
    with av.open(str(AUDIO)) as inp, av.open(str(target), "w") as out:
        audio = inp.streams.audio[0]
        stream = out.add_stream("aac", rate=44100)
        stream.layout = "stereo" if audio.channels == 2 else "mono"
        stream.bit_rate = 320000
        resampler = av.AudioResampler(format="fltp", layout=stream.layout.name, rate=44100)
        for frame in inp.decode(audio):
            for converted in resampler.resample(frame):
                for packet in stream.encode(converted):
                    out.mux(packet)
        for converted in resampler.resample(None):
            for packet in stream.encode(converted):
                out.mux(packet)
        for packet in stream.encode(None):
            out.mux(packet)
    return target


def packets(container, source, target, normalize=False):
    for packet in container.demux(source):
        if packet.dts is None:
            continue
        if normalize:
            # Corrige apenas a quantização do concat de clipes; nenhum quadro é criado ou removido.
            base = packet.time_base
            packet.pts = round(packet.pts * base * FPS)
            packet.dts = round(packet.dts * base * FPS)
            packet.duration = 1
            packet.time_base = Fraction(1, FPS)
        packet.stream = target
        yield packet


def main():
    sound = encode_audio()
    with av.open(str(VISUAL)) as video, av.open(str(sound)) as audio, av.open(str(TARGET), "w", options={"movflags": "+faststart"}) as out:
        vin, ain = video.streams.video[0], audio.streams.audio[0]
        assert (vin.width, vin.height, round(float(vin.average_rate))) == (1080, 1920, FPS)
        vout, aout = out.add_stream_from_template(vin), out.add_stream_from_template(ain)
        vout.time_base = Fraction(1, FPS)
        vs, ats = packets(video, vin, vout, True), packets(audio, ain, aout)
        vp, ap = next(vs, None), next(ats, None)
        while vp is not None or ap is not None:
            vt = float(vp.dts * vp.time_base) if vp else float("inf")
            at = float(ap.dts * ap.time_base) if ap else float("inf")
            if vt <= at:
                out.mux(vp)
                vp = next(vs, None)
            else:
                out.mux(ap)
                ap = next(ats, None)
    with av.open(str(TARGET)) as final:
        v, a = final.streams.video[0], final.streams.audio[0]
        result = dict(file=str(TARGET), width=v.width, height=v.height, fps=float(v.average_rate),
                      video_seconds=float(v.duration * v.time_base), audio_seconds=float(a.duration * a.time_base),
                      video_codec=v.codec_context.name, audio_codec=a.codec_context.name, audio_bit_rate=a.bit_rate)
        (OUT / "entrega.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
