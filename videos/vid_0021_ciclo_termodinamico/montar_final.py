"""Monta voz e legendas do VID21. Uso: uv run python .../montar_final.py --preview|--final."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys

import av

UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(UNIT.parents[1] / "videos"))
from montar_legendado import read_cues
from legenda_final import Captions


def audio_aac(target):
    with av.open(str(UNIT / "audio/narracao_final.wav")) as inp, av.open(str(target), "w") as out:
        source = inp.streams.audio[0]
        stream = out.add_stream("aac", rate=44100)
        stream.layout = "stereo" if source.channels == 2 else "mono"
        stream.bit_rate = 320000
        resampler = av.AudioResampler(format="fltp", layout=stream.layout.name, rate=44100)
        for frame in inp.decode(source):
            for converted in resampler.resample(frame):
                for packet in stream.encode(converted):
                    out.mux(packet)
        for converted in resampler.resample(None):
            for packet in stream.encode(converted):
                out.mux(packet)
        for packet in stream.encode(None):
            out.mux(packet)


def packets(container, source, target, fps=None):
    for packet in container.demux(source):
        if packet.dts is None:
            continue
        if fps:
            packet.pts = round(packet.pts * packet.time_base * fps)
            packet.dts = round(packet.dts * packet.time_base * fps)
            packet.duration = 1
            packet.time_base = Fraction(1, fps)
        packet.stream = target
        yield packet


def mux(visual, audio, target, fps):
    with av.open(str(visual)) as video, av.open(str(audio)) as sound, av.open(
            str(target), "w", options={"movflags": "+faststart"}) as out:
        vin, ain = video.streams.video[0], sound.streams.audio[0]
        vout, aout = out.add_stream_from_template(vin), out.add_stream_from_template(ain)
        vout.time_base = Fraction(1, fps)
        vs, ats = packets(video, vin, vout, fps), packets(sound, ain, aout)
        vp, ap = next(vs, None), next(ats, None)
        while vp is not None or ap is not None:
            vt = float(vp.dts * vp.time_base) if vp is not None else float("inf")
            at = float(ap.dts * ap.time_base) if ap is not None else float("inf")
            if vt <= at:
                out.mux(vp)
                vp = next(vs, None)
            else:
                out.mux(ap)
                ap = next(ats, None)


def burn(master, silent, fps, crf):
    cues = read_cues(UNIT / "legenda.srt")
    with av.open(str(master)) as inp, av.open(str(silent), "w") as out:
        video = inp.streams.video[0]
        stream = out.add_stream("libx264", rate=fps)
        stream.width, stream.height, stream.pix_fmt = video.width, video.height, "yuv420p"
        stream.options = {"crf": str(crf), "preset": "medium"}
        captions = Captions(video.width, video.height)
        index = 0
        for count, frame in enumerate(inp.decode(video)):
            at = count / fps
            while index < len(cues) and cues[index][1] <= at:
                index += 1
            lines = cues[index][2] if index < len(cues) and cues[index][0] <= at else ()
            encoded = av.VideoFrame.from_image(captions.apply(frame, lines))
            encoded.pts, encoded.time_base = count, Fraction(1, fps)
            for packet in stream.encode(encoded):
                out.mux(packet)
            if count % (fps * 20) == 0:
                print(f"Legendas: {at:.0f}s", flush=True)
        for packet in stream.encode(None):
            out.mux(packet)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preview", action="store_true")
    group.add_argument("--final", action="store_true")
    parser.add_argument("--particulas", action="store_true",
                        help="Monta a variante com movimento molecular, preservando a entrega anterior")
    args = parser.parse_args()
    fps, height = (15, 960) if args.preview else (30, 1920)
    if args.particulas:
        root = UNIT / ("media_particulas_preview" if args.preview else "media_particulas_final")
    else:
        root = UNIT / ("media_sincronizado" if args.preview else "media_final")
    visual = root / f"videos/cena/{height}p{fps}/CicloTermodinamico021.mp4"
    renders = UNIT / "renders"
    renders.mkdir(exist_ok=True)
    prefix = "vid_0021_preview" if args.preview else "vid_0021"
    if args.particulas:
        prefix = "vid_0021_particulas_preview" if args.preview else "vid_0021_particulas"
    master, legendado = renders / f"{prefix}_master.mp4", renders / f"{prefix}_legendado.mp4"
    aac, silent = root / "narracao_320k.m4a", root / "legendado_sem_audio.mp4"
    audio_aac(aac)
    mux(visual, aac, master, fps)
    burn(master, silent, fps, 23 if args.preview else 14)
    mux(silent, aac, legendado, fps)
    with av.open(str(legendado)) as out:
        v, a = out.streams.video[0], out.streams.audio[0]
        result = dict(file=str(legendado), master=str(master), width=v.width, height=v.height,
                      fps=float(v.average_rate), video_duration=float(v.duration*v.time_base),
                      audio_duration=float(a.duration*a.time_base), audio_bitrate=a.bit_rate)
    variant = "particulas_" if args.particulas else ""
    (UNIT / f"montagem_{variant}{height}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
