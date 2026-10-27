"""Legendas Inter, em faixa livre abaixo do conteúdo; sem redimensionar a cena."""
from functools import lru_cache
from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parent
COLORS = {"energia interna": "#745CFF", "calor": "#EA63FF", "trabalho": "#35D9FF"}
PATTERN = re.compile(r"(?<!\w)(" + "|".join(COLORS) + r")(?!\w)", re.I)


class Captions:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.scale = width / 540
        self.y = round(840 * self.scale)
        self.font = ImageFont.truetype(
            str(UNIT.parents[1] / "assets/fonts/inter/Inter-SemiBold.ttf"),
            round(27 * self.scale))

    @lru_cache(maxsize=64)
    def overlay(self, lines):
        scale, font = self.scale, self.font
        layer = Image.new("RGBA", (self.width, round(100 * scale)))
        if not lines:
            return layer
        draw = ImageDraw.Draw(layer)
        widths = [font.getlength(line) for line in lines]
        if max(widths) > 448 * scale:
            raise ValueError(f"Legenda fora da largura segura: {lines}")
        bottom = round(927 * scale) - self.y
        top = bottom - round(35 * scale) * len(lines)
        left = (self.width - max(widths)) / 2 - 14 * scale
        draw.rounded_rectangle((left, top - 8 * scale, self.width - left, bottom + 5 * scale),
                               radius=round(12 * scale), fill=(5, 8, 22, 225))
        stroke = round(2 * scale)
        for index, line in enumerate(lines):
            x = (self.width - widths[index]) / 2
            y = top + index * round(35 * scale) - draw.textbbox(
                (0, 0), line, font=font, stroke_width=stroke)[1]
            cursor = 0
            for match in list(PATTERN.finditer(line)) + [None]:
                end = match.start() if match else len(line)
                chunk = line[cursor:end]
                draw.text((x, y), chunk, font=font, fill="white", stroke_width=stroke,
                          stroke_fill="#050816")
                x += font.getlength(chunk)
                if match:
                    chunk = match.group()
                    draw.text((x, y), chunk, font=font, fill=COLORS[chunk.lower()],
                              stroke_width=stroke, stroke_fill="#050816")
                    x += font.getlength(chunk)
                    cursor = match.end()
        return layer

    def apply(self, frame, lines):
        base = frame.to_image()
        if lines:
            overlay = self.overlay(tuple(lines))
            base.paste(overlay, (0, self.y), overlay)
        return base
