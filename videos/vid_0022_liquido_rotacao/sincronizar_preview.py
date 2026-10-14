"""Sincroniza o preview V3.1 ao WAV aprovado; legenda local, sem mudar o template."""
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import sys

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(ROOT / "videos"))
from montar_legendado import read_cues
from montar_master import encode_audio, mux

OUT = UNIT / "media_sync_confirmado"
SOURCE = UNIT / "media/videos/cena_v3_1/960p15/preview_silencioso_v3_1.mp4"
WAV = UNIT / "audio/narracao_final.wav"
FPS = 15
FONT = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 27)
COLORS = {}
for color, terms in [
    ("#35D9FF", ["distância", "distâncias", "eixo", "raio", "espessura", "horizontal", "velocidade angular", "velocidade", "tangencial", "angular", "inclinação", "inclinada"]),
    ("#D77CFF", ["pressão", "pressões", "gradiente", "atmosférica"]),
    ("#75BDFF", ["líquido", "superfície", "altura", "alturas", "vertical", "parábola", "paraboloide", "seção", "desnível"]),
]:
    COLORS.update({term: color for term in terms})
PATTERN = re.compile(r"(?<!\w)(" + "|".join(re.escape(t) for t in sorted(COLORS, key=len, reverse=True)) + r")(?!\w)", re.I)


def caption(image, lines):
    base = image.copy()
    if not lines:
        return base
    overlay = Image.new("RGBA", base.size)
    draw = ImageDraw.Draw(overlay)
    widths = [FONT.getlength(line) for line in lines]
    assert max(widths) <= 448, lines
    top, bottom = 927 - 35 * len(lines), 927
    left = (540 - max(widths)) / 2 - 14
    draw.rounded_rectangle((left, top - 8, 540 - left, bottom + 5), radius=12, fill=(4, 6, 16, 225))
    for i, line in enumerate(lines):
        x = (540 - widths[i]) / 2
        y = top + i * 35 - draw.textbbox((0, 0), line, font=FONT, stroke_width=2)[1]
        cursor = 0
        for match in list(PATTERN.finditer(line)) + [None]:
            end = match.start() if match else len(line)
            chunk = line[cursor:end]
            draw.text((x, y), chunk, font=FONT, fill="white", stroke_width=2, stroke_fill="#040610")
            x += FONT.getlength(chunk)
            if match:
                chunk = match.group()
                draw.text((x, y), chunk, font=FONT, fill=COLORS[chunk.lower()], stroke_width=2, stroke_fill="#040610")
                x += FONT.getlength(chunk)
                cursor = match.end()
    return Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")


def main():
    OUT.mkdir(exist_ok=True, parents=True)
    sync = json.loads((UNIT / "sync.json").read_text(encoding="utf-8"))
    anchors = sync["anchors"]
    segments = sync["segments"]
    starts = [g[0]["audio"] for g in segments]
    target_times = np.array([item["audio"] for item in anchors])
    source_times = np.array([item["visual"] for item in anchors])
    assert all(np.all(np.diff([p["audio"] for p in group]) > 0) for group in segments)
    cues = read_cues(UNIT / "legenda.srt")
    spoken = (UNIT / "texto_narracao.txt").read_text(encoding="utf-8").split()
    subtitled = " ".join(line for _, _, lines in cues for line in lines).split()
    assert spoken == subtitled, "Legenda difere da narração aprovada"
    assert all(len(lines) <= 2 and max(FONT.getlength(line) for line in lines) <= 448 for _, _, lines in cues)
    with av.open(str(WAV)) as audio:
        duration = float(audio.streams.audio[0].duration * audio.streams.audio[0].time_base)
    frames = math.ceil(target_times[-1] * FPS)
    timeline = anchors
    (OUT / "mapa_sincronizacao.json").write_text(json.dumps(timeline, indent=2, ensure_ascii=False), encoding="utf-8")
    stills = [1, 9, 15, 21, 24, 29, 33, 38, 44, 49, 55, 62, 70, 78, 84, 91, 98, 104, 112, 123, 130, 138, 146, 156, 161, 165, 169]
    snapshots = []
    silent_clean, silent_caption = OUT / "visual_sincronizado.mp4", OUT / "visual_legendado.mp4"
    with av.open(str(SOURCE)) as src, av.open(str(silent_clean), "w") as clean, av.open(str(silent_caption), "w") as sub:
        streams = []
        for container in (clean, sub):
            stream = container.add_stream("libx264", rate=FPS)
            stream.width, stream.height, stream.pix_fmt = 540, 960, "yuv420p"
            stream.options = {"crf": "14", "preset": "medium"}
            streams.append(stream)
        decoder = iter(src.decode(video=0))
        current = next(decoder)
        following = next(decoder, None)
        cue_index = 0
        for n in range(frames):
            at = n / FPS
            group = segments[max(0, int(np.searchsorted(starts, at, side="right")) - 1)]
            desired = float(np.interp(at, [p["audio"] for p in group], [p["visual"] for p in group]))
            if desired + 0.001 < float(current.time):
                src.seek(int(desired / src.streams.video[0].time_base), stream=src.streams.video[0], backward=True)
                decoder = iter(src.decode(video=0))
                current = next(decoder)
                following = next(decoder, None)
            while following is not None and float(following.time) <= desired:
                current, following = following, next(decoder, None)
            selected = following if following is not None and abs(float(following.time) - desired) < abs(float(current.time) - desired) else current
            original = selected.to_image()
            while cue_index < len(cues) and cues[cue_index][1] <= at:
                cue_index += 1
            lines = cues[cue_index][2] if cue_index < len(cues) and cues[cue_index][0] <= at else None
            decorated = caption(original, lines)
            for container, stream, image in zip((clean, sub), streams, (original, decorated)):
                encoded = av.VideoFrame.from_image(image)
                encoded.pts, encoded.time_base = n, Fraction(1, FPS)
                for packet in stream.encode(encoded):
                    container.mux(packet)
            if snapshots.__len__() < len(stills) and at >= stills[len(snapshots)]:
                path = OUT / f"frame_{len(snapshots) + 1:02d}.jpg"
                decorated.save(path, quality=94)
                snapshots.append({"tempo": at, "origem": float(selected.time), "arquivo": str(path), "legenda": lines})
            if n % 450 == 0:
                print(f"{at:.1f}/{frames / FPS:.1f}s", flush=True)
        for container, stream in zip((clean, sub), streams):
            for packet in stream.encode(None):
                container.mux(packet)
    aac = OUT / "narracao.m4a"
    encode_audio(WAV, aac)
    outputs = [UNIT / "preview_sincronizado.mp4", UNIT / "preview_legendado.mp4"]
    for visual, output in zip((silent_clean, silent_caption), outputs):
        mux(visual, aac, output)
    report = {"audio_segundos": duration, "video_segundos": frames / FPS, "resolucao": [540, 960], "fps": FPS,
              "legendas": len(cues), "ancoras": len(anchors), "wav_sha256": hashlib.sha256(WAV.read_bytes()).hexdigest(),
              "metodo": "Texto aprovado alinhado a pausas medidas; interpolação silábica dentro das frases. Texto confirmado de 458 palavras; vídeo montado na ordem da fala por quatro blocos; sem alinhamento fonético.",
              "cores": COLORS, "amostras": snapshots, "arquivos": [str(p) for p in outputs]}
    (OUT / "validacao.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ("amostras", "cores")}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
