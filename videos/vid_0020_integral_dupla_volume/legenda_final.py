"""Legendas do VID20 compostas nos quadros nativos, antes da única codificação."""
from bisect import bisect_right
from functools import lru_cache
from pathlib import Path
import re
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(UNIT.parents[1] / "videos"))
from montar_legendado import read_cues

COLORS = {}
for color, terms in [
    ("#35D9FF", ["base", "bases", "área", "áreas", "célula", "células", "comprimento", "largura", "espessura", "superfície"]),
    ("#EA63FF", ["função", "altura", "alturas"]),
    ("#9C8CFF", ["volume", "volumes", "coluna", "colunas", "contribuição", "contribuições", "integral dupla"]),
    ("#8CEBFF", ["seção", "seções", "primeira integração"]),
    ("#C4B5FF", ["segunda integração", "segunda integral"]),
]:
    COLORS.update({term: color for term in terms})
PATTERN = re.compile(r"(?<!\w)(" + "|".join(re.escape(t) for t in sorted(COLORS, key=len, reverse=True)) + r")(?!\w)", re.I)


class NativeCaptions:
    def __init__(self, width, height, fps):
        self.width, self.height, self.fps = width, height, fps
        self.scale = width / 540
        self.font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", round(27 * self.scale))
        self.cues = read_cues(UNIT / "legenda.srt")
        self.starts = [int(np.ceil(start * fps - 1e-8)) for start, _, _ in self.cues]
        self.ends = [int(np.ceil(end * fps - 1e-8)) for _, end, _ in self.cues]

    def body(self, frame):
        image = Image.fromarray(frame).convert("RGBA")
        top = round(190 * self.scale)
        base = Image.new("RGBA", image.size, "#050816")
        base.paste(image.crop((0, 0, self.width, top)), (0, 0))
        body = image.crop((0, top, self.width, self.height)).resize(
            (round(464 * self.scale), round(662 * self.scale)), Image.Resampling.LANCZOS)
        base.paste(body, (round(38 * self.scale), top))
        return base

    @lru_cache(maxsize=80)
    def overlay(self, lines):
        layer = Image.new("RGBA", (self.width, self.height))
        if not lines:
            return layer
        draw, scale, font = ImageDraw.Draw(layer), self.scale, self.font
        widths = [font.getlength(line) for line in lines]
        assert max(widths) <= 448 * scale
        bottom = round(927 * scale)
        top = bottom - round(35 * scale) * len(lines)
        left = (self.width - max(widths)) / 2 - 14 * scale
        draw.rounded_rectangle((left, top - 8 * scale, self.width - left, bottom + 5 * scale),
                               radius=round(12 * scale), fill=(5, 8, 22, 225))
        stroke = round(2 * scale)
        for i, line in enumerate(lines):
            x = (self.width - widths[i]) / 2
            y = top + i * round(35 * scale) - draw.textbbox((0, 0), line, font=font, stroke_width=stroke)[1]
            cursor = 0
            for match in list(PATTERN.finditer(line)) + [None]:
                end = match.start() if match else len(line)
                chunk = line[cursor:end]
                draw.text((x, y), chunk, font=font, fill="white", stroke_width=stroke, stroke_fill="#050816")
                x += font.getlength(chunk)
                if match:
                    chunk = match.group()
                    draw.text((x, y), chunk, font=font, fill=COLORS[chunk.lower()], stroke_width=stroke, stroke_fill="#050816")
                    x += font.getlength(chunk)
                    cursor = match.end()
        return layer

    def batches(self, frame, start_frame, count):
        base = self.body(frame)
        cursor, stop = start_frame, start_frame + count
        while cursor < stop:
            index = bisect_right(self.starts, cursor) - 1
            if index >= 0 and cursor < self.ends[index]:
                lines = tuple(self.cues[index][2])
                end = min(stop, self.ends[index])
            else:
                lines = ()
                end = min(stop, self.starts[index + 1] if index + 1 < len(self.starts) else stop)
            assert end > cursor
            yield np.array(Image.alpha_composite(base, self.overlay(lines))), end - cursor
            cursor = end
