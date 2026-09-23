"""Monta um master limpo a partir do render Manim e da narração aprovada.

Uso: python videos/montar_master.py VISUAL.mp4 AUDIO.wav MASTER.mp4
Aceita WAV ou MP3. Copia o vídeo H.264 e codifica o áudio em AAC, sem
alterar a cena. Os dois episódios usam a mesma operação de montagem.
"""

import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

import av


def packets(container, source_stream, target_stream):
    for packet in container.demux(source_stream):
        if packet.dts is not None:
            packet.stream = target_stream
            yield packet


def encode_audio(source: Path, target: Path) -> None:
    with av.open(str(source)) as inp, av.open(str(target), "w") as out:
        audio = inp.streams.audio[0]
        layout = "mono" if audio.channels == 1 else "stereo"
        stream = out.add_stream("aac", rate=44100)
        stream.layout = layout
        resampler = av.AudioResampler(format="fltp", layout=layout, rate=44100)
        for frame in inp.decode(audio):
            for converted in resampler.resample(frame):
                for packet in stream.encode(converted):
                    out.mux(packet)
        for converted in resampler.resample(None):
            for packet in stream.encode(converted):
                out.mux(packet)
        for packet in stream.encode(None):
            out.mux(packet)


def mux(visual: Path, sound: Path, target: Path) -> None:
    with av.open(str(visual)) as video, av.open(str(sound)) as audio, av.open(str(target), "w") as out:
        vin, ain = video.streams.video[0], audio.streams.audio[0]
        vout = out.add_stream_from_template(vin)
        aout = out.add_stream_from_template(ain)
        videos, audios = packets(video, vin, vout), packets(audio, ain, aout)
        vp, ap = next(videos, None), next(audios, None)
        while vp is not None or ap is not None:
            vt = float(vp.dts * vp.time_base) if vp is not None else float("inf")
            at = float(ap.dts * ap.time_base) if ap is not None else float("inf")
            if vt <= at:
                out.mux(vp)
                vp = next(videos, None)
            else:
                out.mux(ap)
                ap = next(audios, None)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("visual", type=Path)
    parser.add_argument("audio", type=Path)
    parser.add_argument("master", type=Path)
    args = parser.parse_args()
    paths = [path.resolve() for path in (args.visual, args.audio, args.master)]
    visual, audio, master = paths
    if len(set(paths)) != 3 or not visual.is_file() or not audio.is_file():
        parser.error("Arquivos de entrada ausentes ou caminhos de entrada/saída iguais")
    master.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as directory:
        encoded = Path(directory) / "narracao.m4a"
        encode_audio(audio, encoded)
        mux(visual, encoded, master)
    with av.open(str(master)) as result:
        video, sound = result.streams.video[0], result.streams.audio[0]
        print(f"{master}: {video.width}×{video.height}, "
              f"{float(video.base_rate):.0f} fps, "
              f"{float(video.duration * video.time_base):.3f} s vídeo, "
              f"{float(sound.duration * sound.time_base):.3f} s áudio")


if __name__ == "__main__":
    main()
