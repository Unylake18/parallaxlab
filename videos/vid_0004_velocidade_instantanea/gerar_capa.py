"""Gera capa_instagram.png do vid_0004 (DA EQUAÇÃO AO FENÔMENO · EP. 01).

Uso, na raiz do repositório:
    uv run python videos/vid_0004_velocidade_instantanea/gerar_capa.py [SAIDA.png]

Base: videos/vid_0002_integral_substituicao/capa_instagram.png (versionada), como
nas capas 1–3; dela se apagam título, linha de série e painel. No lugar do painel
entra a assinatura da série: fenômeno (partícula em movimento) + gráfico x × t com
secantes, tangente e v = dx/dt, desenhados pelo Manim no estilo da cena.

Fontes: Century Gothic (GOTHIC.TTF, GOTHICB.TTF) do sistema, como na capa do
vid_0003; não versionadas. Matemática em MathTex.
"""
import os
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
BASE = UNIT.parent / "vid_0002_integral_substituicao" / "capa_instagram.png"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capa_instagram.png"
TMP_MEDIA = ROOT / "media" / "_capa_vid0004_tmp"   # LaTeX falha em caminhos curtos (~) do Temp
FONT_DIRS = [Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts",
             Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts"]

CYAN, BLUE, MAGENTA, VIOLET, WHITE = "#35D9FF", "#267BFF", "#EA63FF", "#745CFF", "#F5F7FF"
BRAND = [(0x35, 0xD9, 0xFF), (0x26, 0x7B, 0xFF), (0x74, 0x5C, 0xFF), (0xEA, 0x63, 0xFF)]


def system_font(name):
    for folder in FONT_DIRS:
        if (folder / name).is_file():
            return str(folder / name)
    sys.exit(f"Fonte do sistema ausente: {name}")


# ---------------------------------------------------------------- ilustração (Manim)
def render_illustration():
    from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Axes, Circle, Dot, Line, MathTex,
                       Scene, VGroup, tempconfig)

    def glow(mob, color, width, opacity):
        return VGroup(mob.copy().set_stroke(color=color, width=width, opacity=opacity), mob)

    class Ilustracao(Scene):
        def construct(self):
            # Fenômeno: pista, rastro do movimento acelerado e partícula com seta.
            to_x = lambda m: -3.4 + 6.8 * m / 18
            track = Line([to_x(0), 1.6, 0], [to_x(18), 1.6, 0], stroke_width=7)
            track.set_color([CYAN, VIOLET])
            self.add(glow(track, VIOLET, 26, 0.16))
            for m, op in ((0.25, 0.14), (1.0, 0.24), (2.25, 0.40)):   # x(t) em t = 0,5; 1; 1,5 s
                self.add(Dot([to_x(m), 1.6, 0], radius=0.15, color=CYAN, fill_opacity=op))
            orb_c = [to_x(4), 1.6, 0]
            arrow = Arrow(orb_c, [orb_c[0] + 2.0, 1.6, 0], buff=0.3, color=CYAN,
                          stroke_width=12, max_tip_length_to_length_ratio=0.3)
            self.add(arrow.copy().set_stroke(width=28, opacity=0.2).set_fill(opacity=0.2), arrow)
            self.add(Dot(orb_c, radius=0.5, color=VIOLET, fill_opacity=0.12),
                     Dot(orb_c, radius=0.37, color=CYAN, fill_opacity=0.2),
                     Dot(orb_c, radius=0.27, color=CYAN, fill_opacity=0.38),
                     Dot(orb_c, radius=0.18, color=WHITE))

            # Gráfico x × t: parábola, aproximação por secantes e tangente em P.
            # Domínio recortado (t ≤ 3,4 s, x ≤ 12 m) para a curvatura e o leque aparecerem.
            axes = Axes(x_range=[0, 3.4, 1], y_range=[0, 12, 4], x_length=6.8, y_length=3.6,
                        tips=True, axis_config={"color": "#9AA1C7", "stroke_width": 3,
                                                "include_ticks": False}).move_to([0, -1.05, 0])
            self.add(axes,
                     MathTex("t", font_size=40, color="#9AA1C7").next_to(axes.x_axis.get_end(), RIGHT, buff=0.12),
                     MathTex("x", font_size=40, color="#9AA1C7").next_to(axes.y_axis.get_end(), RIGHT, buff=0.12))
            x = lambda t: t ** 2
            curve = axes.plot(x, x_range=[0, 3.4], stroke_width=5).set_stroke(color=WHITE)
            halo = curve.copy().set_stroke(width=20, opacity=0.22)
            halo.set_color([CYAN, VIOLET])
            self.add(halo, curve)

            def line(slope, color, width, op):
                t0, t1 = max(0, 2 - 4 / slope), min(3.4, 2 + 8 / slope)
                pt = lambda t: axes.c2p(t, 4 + slope * (t - 2))
                return glow(Line(pt(t0), pt(t1), color=color, stroke_width=width,
                                 stroke_opacity=op), color, width * 3, 0.18 * op)

            P = axes.c2p(2, 4)
            for dt, op in ((1.4, 0.6), (0.7, 0.9)):                  # secantes se aproximando
                self.add(line(4 + dt, BLUE, 5, op))
                self.add(Circle(radius=0.13, color=BLUE, stroke_width=4, stroke_opacity=op)
                         .move_to(axes.c2p(2 + dt, x(2 + dt))))
            corner, Q = axes.c2p(3.4, 4), axes.c2p(3.4, x(3.4))
            self.add(Line(P, corner, color=VIOLET, stroke_width=6),
                     Line(corner, Q, color=MAGENTA, stroke_width=6))
            self.add(line(4, CYAN, 9, 1.0))                           # tangente: elemento forte
            self.add(Dot(P, radius=0.36, color=CYAN, fill_opacity=0.15),
                     Dot(P, radius=0.22, color=CYAN, fill_opacity=0.3),
                     Dot(P, radius=0.12, color=WHITE))

            formula = MathTex("v", "=", r"\frac{dx}{dt}", font_size=60, color=WHITE)
            formula[0].set_color(CYAN)
            formula[2].set_color(CYAN)
            self.add(formula.move_to(axes.c2p(0.75, 8.6)))

    with tempconfig({"frame_width": 9, "frame_height": 16, "pixel_width": 2160,
                     "pixel_height": 3840, "transparent": True, "format": "png",
                     "save_last_frame": True, "write_to_movie": False,
                     "media_dir": str(TMP_MEDIA), "verbosity": "WARNING",
                     "disable_caching": True, "output_file": "ilustracao"}):
        scene = Ilustracao()
        scene.render()
        image = Image.open(scene.renderer.file_writer.image_file_path).convert("RGBA")
    shutil.rmtree(TMP_MEDIA, ignore_errors=True)
    return image.crop(image.getchannel("A").getbbox())


# ---------------------------------------------------------------- base e composição
img = Image.open(BASE).convert("RGB")
W, H = img.size
arr = np.asarray(img).astype(np.float32)
soft = np.asarray(img.filter(ImageFilter.MinFilter(15)).filter(ImageFilter.GaussianBlur(20))).astype(np.float32)


def erase_vertical(x0, x1, y0, y1, blend=30):
    top, bot = soft[y0, x0:x1], soft[y1, x0:x1]
    t = np.clip((np.arange(y1 - y0) - (y1 - y0 - blend)) / blend, 0, 1)[:, None, None]
    return (x0, y0, (1 - t) * top[None] + t * bot[None])


fill, mask = arr.copy(), np.zeros((H, W), np.float32)
for x0, y0, patch in (erase_vertical(64, 1016, 666, 1000),     # título
                      erase_vertical(96, 988, 1052, 1142),    # linha de série
                      erase_vertical(150, 935, 1142, 1478)):  # painel inteiro (borda incluída)
    h, w = patch.shape[:2]
    fill[y0:y0 + h, x0:x0 + w] = patch
    mask[y0:y0 + h, x0:x0 + w] = 1
m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(
    ImageFilter.GaussianBlur(8))).astype(np.float32)[..., None] / 255
fill += np.random.default_rng(4).normal(0, 1.6, fill.shape)   # grão similar ao original
img = Image.fromarray((arr * (1 - m) + fill * m).clip(0, 255).astype(np.uint8)).convert("RGBA")


def gradient(size, stops):
    w, h = size
    seg = np.clip(np.linspace(0, 1, w) * (len(stops) - 1), 0, len(stops) - 1 - 1e-6)
    i = seg.astype(int); f = (seg - i)[:, None]
    row = (np.array(stops)[i] * (1 - f) + np.array(stops)[i + 1] * f).astype(np.uint8)
    return Image.fromarray(np.repeat(row[None], h, 0), "RGB")


def glow_paste(layer_mask, box, color_img, glow_color, glow_radius, glow_alpha):
    global img
    full = Image.new("L", img.size, 0); full.paste(layer_mask, box[:2])
    halo = full.filter(ImageFilter.GaussianBlur(glow_radius)).point(lambda v: int(v * glow_alpha))
    img = Image.composite(Image.new("RGBA", img.size, glow_color + (255,)), img, halo)
    fill_full = Image.new("RGBA", img.size); fill_full.paste(color_img.convert("RGBA"), box[:2])
    img = Image.composite(fill_full, img, full)


def text_mask(text, font, tracking=0):
    widths = [font.getlength(c) + tracking for c in text]
    asc, desc = font.getmetrics()
    mk = Image.new("L", (int(sum(widths) - tracking) + 4, asc + desc + 4), 0)
    d = ImageDraw.Draw(mk); x = 2
    for c, w in zip(text, widths):
        d.text((x, 2), c, font=font, fill=255); x += w
    return mk.crop(mk.getbbox())


def fit(text, path, width, start):
    size = start
    while ImageFont.truetype(path, size).getlength(text) > width:
        size -= 1
    return ImageFont.truetype(path, size)


def place_center(mask_img, cy):
    return ((W - mask_img.width) // 2, int(cy - mask_img.height / 2))


GOTHIC_B, GOTHIC = system_font("GOTHICB.TTF"), system_font("GOTHIC.TTF")

# 1. Headline em duas linhas: branco, depois gradiente da marca.
line1 = text_mask("VELOCIDADE", fit("VELOCIDADE", GOTHIC_B, 860, 200))
glow_paste(line1, place_center(line1, 768), Image.new("RGB", line1.size, (255, 255, 255)),
           (70, 140, 255), 16, 0.55)
line2 = text_mask("EM UM INSTANTE?", fit("EM UM INSTANTE?", GOTHIC_B, 860, 160))
glow_paste(line2, place_center(line2, 905), gradient(line2.size, BRAND), (110, 90, 255), 14, 0.45)

# 2. Linha de série, no lugar e escala das capas anteriores.
series = text_mask("DA EQUAÇÃO AO FENÔMENO · EP. 01", ImageFont.truetype(GOTHIC, 36), tracking=8)
if series.width > 860:
    series = series.resize((860, round(series.height * 860 / series.width)), Image.LANCZOS)
glow_paste(series, place_center(series, 1097), Image.new("RGB", series.size, (236, 240, 255)),
           (60, 120, 255), 6, 0.25)

# 3. Assinatura da série: fenômeno + gráfico, no espaço do antigo painel.
art = render_illustration()
k = min(880 / art.width, 425 / art.height)
art = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)
img.alpha_composite(art, ((W - art.width) // 2, 1146))

img.convert("RGB").save(OUT, optimize=True)
print(OUT, img.size, "ilustração", art.size)
