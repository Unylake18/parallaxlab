"""Queima um SRT no master limpo, preservando seus pacotes AAC.

Uso: python videos/montar_legendado.py MASTER.mp4 LEGENDA.srt SAIDA.mp4
O estilo padrão reproduz o vid_0002; --style piloto usa o posicionamento e a
tipografia observados no master aprovado do vid_0001.
"""

import argparse
from fractions import Fraction
import re
from pathlib import Path
from tempfile import TemporaryDirectory

import av
from PIL import Image, ImageDraw, ImageFont


def seconds(stamp: str) -> float:
    h, m, s, ms = map(int, re.split(r"[:,]", stamp))
    return h * 3600 + m * 60 + s + ms / 1000


def read_cues(path: Path) -> list[tuple[float, float, list[str]]]:
    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = block.splitlines()
        if len(lines) not in (3, 4) or int(lines[0]) != len(cues) + 1:
            raise ValueError(f"Entrada SRT inválida: {lines!r}")
        start, end = (seconds(stamp) for stamp in lines[1].split(" --> "))
        if start >= end or (cues and start < cues[-1][1]):
            raise ValueError(f"Tempo SRT inválido: {lines[1]}")
        cues.append((start, end, lines[2:]))
    if not cues:
        raise ValueError("SRT vazio")
    return cues


def draw_caption(frame, lines, font, width, height, style):
    base = frame.to_image()
    if not lines:
        return base
    scale = width / 540
    base = base.convert("RGBA")
    overlay = Image.new("RGBA", (width, height))
    painter = ImageDraw.Draw(overlay)
    pilot = style == "piloto"
    stroke = round((1 if pilot else 2) * scale)
    boxes = [painter.textbbox((0, 0), line, font=font, stroke_width=stroke)
             for line in lines]
    widest = max(box[2] - box[0] for box in boxes)
    if widest > 468 * scale:
        raise ValueError(f"Legenda excede a largura segura: {lines!r}")
    line_height = round((31 if pilot else 38) * scale)
    bottom = round((821 if pilot else 855) * scale)
    top = bottom - len(lines) * line_height
    left = (width - widest) / 2 - 15 * scale
    painter.rounded_rectangle(
        (left, top - 7 * scale, width - left, bottom + 5 * scale),
        radius=round(12 * scale), fill=(4, 6, 16, 90 if pilot else 160),
    )
    for index, line in enumerate(lines):
        box = boxes[index]
        x = width / 2 - (box[2] - box[0]) / 2
        y = top + index * line_height - box[1]
        painter.text((x, y), line, font=font, fill="white",
                     stroke_width=stroke, stroke_fill="#040610")
    base.alpha_composite(overlay)
    return base.convert("RGB")


def packets(container, source_stream, target_stream):
    for packet in container.demux(source_stream):
        if packet.dts is not None:
            packet.stream = target_stream
            yield packet


def mux_audio(visual: Path, master: Path, target: Path) -> None:
    with av.open(str(visual)) as video, av.open(str(master)) as audio, av.open(str(target), "w") as out:
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
    parser.add_argument("master", type=Path)
    parser.add_argument("srt", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--style", choices=("standard", "piloto"), default="standard")
    args = parser.parse_args()
    master, srt, output = (path.resolve() for path in (args.master, args.srt, args.output))
    if len({master, srt, output}) != 3 or not master.is_file() or not srt.is_file():
        parser.error("Arquivos de entrada ausentes ou caminhos de entrada/saída iguais")
    cues = read_cues(srt)
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as directory:
        silent = Path(directory) / "legendado_sem_audio.mp4"
        with av.open(str(master)) as clean:
            video = clean.streams.video[0]
            width, height = video.width, video.height
            fps = round(float(video.base_rate))
            if (width, height, fps) not in ((540, 960, 15), (1080, 1920, 30)):
                raise ValueError("Formato esperado: 540×960/15 ou 1080×1920/30")
            font_name = "arial.ttf" if args.style == "piloto" else "arialbd.ttf"
            font_size = 24.5 if args.style == "piloto" else 29
            font = ImageFont.truetype(
                str(Path(r"C:\Windows\Fonts") / font_name), round(font_size * width / 540))
            with av.open(str(silent), "w") as out:
                stream = out.add_stream("libx264", rate=fps)
                stream.width, stream.height, stream.pix_fmt = width, height, "yuv420p"
                stream.options = {"crf": "18" if width == 1080 else "19", "preset": "veryfast"}
                cue_index = 0
                for count, frame in enumerate(clean.decode(video)):
                    at = float(frame.pts * frame.time_base)
                    while cue_index < len(cues) and cues[cue_index][1] <= at:
                        cue_index += 1
                    lines = (cues[cue_index][2] if cue_index < len(cues)
                             and cues[cue_index][0] <= at else None)
                    encoded = av.VideoFrame.from_image(
                        draw_caption(frame, lines, font, width, height, args.style))
                    encoded.pts, encoded.time_base = count, Fraction(1, fps)
                    for packet in stream.encode(encoded):
                        out.mux(packet)
                for packet in stream.encode(None):
                    out.mux(packet)
        mux_audio(silent, master, output)
    print(f"{output}: {len(cues)} legendas")


if __name__ == "__main__":
    main()
