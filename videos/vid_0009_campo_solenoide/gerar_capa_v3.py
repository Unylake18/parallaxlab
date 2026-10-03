"""Recria as seis capas de título B usando a arte-base atual do episódio 03.

O quadro neon é a única região variável. Não requer Manim.
"""

from pathlib import Path
from math import exp

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "capa_instagramvd9.png"
OUT = HERE / "capas_v3"
CYAN = (53, 217, 255)
BLUE = (38, 123, 255)
LIGHT = (138, 233, 255)
WHITE = (245, 247, 255)
VIOLET = (116, 92, 255)
MAGENTA = (234, 99, 255)
PANEL = (151, 1178, 929, 1443)


def clean_panel(source):
    """Mantém a borda e substitui o miolo por um único fundo compartilhado."""
    img = source.copy().convert("RGBA")
    x0, y0, x1, y1 = PANEL
    width, height = x1-x0, y1-y0
    left = np.array((4, 31, 92), dtype=float)
    middle = np.array((16, 29, 111), dtype=float)
    right = np.array((54, 13, 91), dtype=float)
    u = np.linspace(0, 1, width)
    row = np.empty((width, 3), dtype=np.uint8)
    for i, t in enumerate(u):
        color = (1-2*t)*left+2*t*middle if t < .5 else (2-2*t)*middle+(2*t-1)*right
        row[i] = np.clip(color, 0, 255).astype(np.uint8)
    fill = Image.fromarray(np.repeat(row[None], height, axis=0), "RGB").convert("RGBA")
    img.alpha_composite(fill, (x0, y0))
    return img


def glow_path(layer, points, color, width=7, glow=10, alpha=.57):
    local = Image.new("RGBA", layer.size)
    ImageDraw.Draw(local).line(points, fill=color+(255,), width=width, joint="curve")
    halo = local.filter(ImageFilter.GaussianBlur(glow))
    halo.putalpha(halo.getchannel("A").point(lambda x: round(x*alpha)))
    layer.alpha_composite(halo)
    layer.alpha_composite(local)


def arrow(layer, x0, y0, x1, y1, color=CYAN, width=9, tip=18):
    from math import atan2, cos, sin
    glow_path(layer, [(x0, y0), (x1, y1)], color, width)
    a = atan2(y1-y0, x1-x0)
    points = [(x1, y1),
              (x1-tip*cos(a-.48), y1-tip*sin(a-.48)),
              (x1-tip*cos(a+.48), y1-tip*sin(a+.48))]
    local = Image.new("RGBA", layer.size)
    ImageDraw.Draw(local).polygon(points, fill=color+(255,))
    halo = local.filter(ImageFilter.GaussianBlur(9))
    halo.putalpha(halo.getchannel("A").point(lambda x: round(x*.6)))
    layer.alpha_composite(halo)
    layer.alpha_composite(local)


def loop(layer, x, y=1311, rx=26, ry=95):
    box = (x-rx, y-ry, x+rx, y+ry)
    local = Image.new("RGBA", layer.size)
    draw = ImageDraw.Draw(local)
    draw.arc(box, 90, 270, fill=BLUE+(120,), width=7)
    draw.arc(box, 270, 450, fill=(50, 160, 255, 255), width=9)
    halo = local.filter(ImageFilter.GaussianBlur(8))
    halo.putalpha(halo.getchannel("A").point(lambda p: round(p*.5)))
    layer.alpha_composite(halo)
    layer.alpha_composite(local)


def coil(layer, first, last, n, y=1311, ry=92):
    for x in np.linspace(first, last, n):
        loop(layer, round(x), y, ry=ry)
    glow_path(layer, [(first, y-ry), (last, y-ry)], BLUE, 3, alpha=.25)
    glow_path(layer, [(first, y+ry), (last, y+ry)], BLUE, 3, alpha=.25)


def version_1(layer):
    loop(layer, 230)
    arrow(layer, 246, 1311, 293, 1311, LIGHT, 5, 13)
    arrow(layer, 320, 1311, 369, 1311, WHITE, 5, 15)
    coil(layer, 430, 542, 4)
    arrow(layer, 446, 1311, 542, 1311, LIGHT, 7, 18)
    arrow(layer, 563, 1311, 612, 1311, WHITE, 5, 15)
    coil(layer, 669, 860, 9)
    arrow(layer, 681, 1311, 888, 1311, CYAN, 14, 29)


def version_2(layer):
    for x in (230, 350, 470, 590):
        loop(layer, x, ry=86)
        arrow(layer, x+12, 1263, x+54, 1263, LIGHT, 5, 12)
        glow_path(layer, [(x+54, 1263), (698, 1311)], LIGHT, 2, alpha=.2)
    dot = Image.new("RGBA", layer.size)
    ImageDraw.Draw(dot).ellipse((691, 1304, 705, 1318), fill=MAGENTA+(255,))
    halo = dot.filter(ImageFilter.GaussianBlur(10))
    layer.alpha_composite(halo)
    layer.alpha_composite(dot)
    arrow(layer, 705, 1311, 875, 1311, CYAN, 15, 30)


def version_3(layer):
    coil(layer, 210, 474, 3)
    arrow(layer, 265, 1311, 382, 1311, LIGHT, 6, 18)
    arrow(layer, 498, 1311, 552, 1311, WHITE, 5, 16)
    coil(layer, 589, 853, 10)
    arrow(layer, 611, 1311, 883, 1311, CYAN, 15, 29)


def version_4(layer):
    loop(layer, 212)
    arrow(layer, 277, 1311, 344, 1311, WHITE, 6, 19)
    coil(layer, 399, 511, 4)
    arrow(layer, 547, 1311, 613, 1311, WHITE, 6, 19)
    coil(layer, 677, 863, 10)
    arrow(layer, 693, 1311, 886, 1311, CYAN, 10, 23)


def version_5(layer):
    coil(layer, 370, 716, 11, y=1260, ry=57)
    arrow(layer, 395, 1260, 741, 1260, CYAN, 8, 20)
    glow_path(layer, [(239, 1401), (858, 1401)], BLUE, 4, alpha=.3)
    glow_path(layer, [(239, 1401), (239, 1321)], BLUE, 4, alpha=.3)
    points = []
    for x in np.linspace(250, 847, 240):
        t = (x-250)/(847-250)
        b = 1/(1+exp(-35*(t-.22)))/(1+exp(35*(t-.78)))
        points.append((round(x), round(1400-72*b)))
    glow_path(layer, points, CYAN, 8, alpha=.75)
    glow_path(layer, [(431, 1329), (665, 1329)], MAGENTA, 3, alpha=.4)


def version_6(layer):
    coil(layer, 252, 822, 13)
    for y in (1264, 1311, 1358):
        arrow(layer, 283, y, 872, y, CYAN, 11 if y != 1311 else 15, 27)


VERSIONS = (version_1, version_2, version_3, version_4, version_5, version_6)


def make():
    OUT.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGBA")
    shared = clean_panel(source)
    paths = []
    for number, draw_panel in enumerate(VERSIONS, 1):
        panel = Image.new("RGBA", source.size)
        draw_panel(panel)
        image = shared.copy()
        image.alpha_composite(panel)
        path = OUT / f"capa_{number:02}.png"
        image.convert("RGB").save(path)
        paths.append(path)
    reference = np.asarray(Image.open(paths[0]))
    outside = np.ones(reference.shape[:2], dtype=bool)
    outside[PANEL[1]:PANEL[3], PANEL[0]:PANEL[2]] = False
    for path in paths[1:]:
        assert np.array_equal(reference[outside], np.asarray(Image.open(path))[outside]), path
    grid = Image.new("RGB", (720, 1920), (3, 7, 21))
    for i, path in enumerate(paths):
        thumb = Image.open(path).resize((360, 640), Image.Resampling.LANCZOS)
        grid.paste(thumb, ((i%2)*360, (i//2)*640))
    grid.save(OUT / "grade_2x3.png")
    print("Capas recriadas:", *paths, "QA: pixels fora do painel idênticos", sep="\n")


if __name__ == "__main__":
    make()
