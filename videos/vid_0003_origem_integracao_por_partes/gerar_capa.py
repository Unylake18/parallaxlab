"""Gera capa_instagram.png do vid_0003 sobre a capa do vid_0002 (mesma base visual).

Uso, na raiz do repositório:
    uv run python videos/vid_0003_origem_integracao_por_partes/gerar_capa.py [SAIDA.png]

Base: videos/vid_0002_integral_substituicao/capa_instagram.png (versionada). Dela
se apagam título, linha de série e fórmula; fundo, símbolo, divisor, painel,
marca e horizonte são preservados.

Fontes: Century Gothic (GOTHIC.TTF, GOTHICB.TTF) e Times New Roman (times.ttf,
timesi.ttf), fontes do sistema Windows, não versionadas. A tipografia oficial
do Parallax Lab ainda não foi definida.
"""
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

UNIT = Path(__file__).resolve().parent
BASE = UNIT.parent / "vid_0002_integral_substituicao" / "capa_instagram.png"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capa_instagram.png"
FONT_DIRS = [Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts",
             Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Windows" / "Fonts"]


def system_font(name):
    for folder in FONT_DIRS:
        if (folder / name).is_file():
            return str(folder / name)
    sys.exit(f"Fonte do sistema ausente: {name} (esperada em {FONT_DIRS[0]})")


GOTHIC_B, GOTHIC = system_font("GOTHICB.TTF"), system_font("GOTHIC.TTF")
TIMES, TIMES_I = system_font("times.ttf"), system_font("timesi.ttf")
BRAND = [(0x35, 0xD9, 0xFF), (0x26, 0x7B, 0xFF), (0x74, 0x5C, 0xFF), (0xEA, 0x63, 0xFF)]
PALE = [(0xC8, 0xF4, 0xFF), (0xD8, 0xDD, 0xFF), (0xE6, 0xC4, 0xFF)]

img = Image.open(BASE).convert("RGB")
W, H = img.size
arr = np.asarray(img).astype(np.float32)
# Fundo sem estrelas: mínimo local seguido de suavização.
soft = np.asarray(img.filter(ImageFilter.MinFilter(15)).filter(ImageFilter.GaussianBlur(20))).astype(np.float32)


def erase_vertical(x0, x1, y0, y1, blend=30):
    top, bot = soft[y0, x0:x1], soft[y1, x0:x1]
    # Estende a linha superior; só as últimas linhas convergem para a inferior.
    t = np.clip((np.arange(y1 - y0) - (y1 - y0 - blend)) / blend, 0, 1)[:, None, None]
    return (x0, y0, (1 - t) * top[None] + t * bot[None])


def erase_bilinear(x0, x1, y0, y1, r=6):
    """Interior do painel: interpolação entre os quatro cantos, fora da fórmula antiga."""
    c = lambda x, y: arr[y - r:y + r, x - r:x + r].reshape(-1, 3).mean(0)
    tl, tr, bl, br = c(x0, y0), c(x1, y0), c(x0, y1), c(x1, y1)
    u = np.linspace(0, 1, x1 - x0)[None, :, None]; v = np.linspace(0, 1, y1 - y0)[:, None, None]
    return (x0, y0, (1 - v) * ((1 - u) * tl + u * tr) + v * ((1 - u) * bl + u * br))


fill = arr.copy()
mask = np.zeros((H, W), np.float32)
for x0, y0, patch in (erase_vertical(64, 1016, 666, 1000),     # título
                      erase_vertical(96, 988, 1052, 1142),    # linha de série
                      erase_bilinear(226, 874, 1194, 1420)):  # interior do painel
    h, w = patch.shape[:2]
    fill[y0:y0 + h, x0:x0 + w] = patch
    mask[y0:y0 + h, x0:x0 + w] = 1
m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(
    ImageFilter.GaussianBlur(8))).astype(np.float32)[..., None] / 255
fill += np.random.default_rng(3).normal(0, 1.6, fill.shape)  # grão similar ao original
# Mantém o erro de interpolação dentro das zonas: fora delas, a imagem original.
out = arr * (1 - m) + fill * m
img = Image.fromarray(out.clip(0, 255).astype(np.uint8)).convert("RGBA")


def gradient(size, stops):
    w, h = size
    xs = np.linspace(0, 1, w)
    seg = np.clip((xs * (len(stops) - 1)), 0, len(stops) - 1 - 1e-6)
    i = seg.astype(int); f = (seg - i)[:, None]
    a, b = np.array(stops)[i], np.array(stops)[i + 1]
    row = (a * (1 - f) + b * f).astype(np.uint8)
    return Image.fromarray(np.repeat(row[None], h, 0), "RGB")


def glow_paste(layer_mask, box, color_img, glow_color, glow_radius, glow_alpha):
    """Aplica texto (máscara L em box) com preenchimento e brilho."""
    global img
    full = Image.new("L", img.size, 0); full.paste(layer_mask, box[:2])
    halo = full.filter(ImageFilter.GaussianBlur(glow_radius)).point(lambda v: int(v * glow_alpha))
    img = Image.composite(Image.new("RGBA", img.size, glow_color + (255,)), img, halo)
    fill_full = Image.new("RGBA", img.size); fill_full.paste(color_img.convert("RGBA"), box[:2])
    img = Image.composite(fill_full, img, full)


def text_mask(text, font, tracking=0):
    widths = [font.getlength(c) + tracking for c in text]
    asc, desc = font.getmetrics()
    m = Image.new("L", (int(sum(widths) - tracking) + 4, asc + desc + 4), 0)
    d = ImageDraw.Draw(m); x = 2
    for c, w in zip(text, widths):
        d.text((x, 2), c, font=font, fill=255); x += w
    return m.crop(m.getbbox())


def fit(text, path, width, start):
    size = start
    while ImageFont.truetype(path, size).getlength(text) > width:
        size -= 1
    return ImageFont.truetype(path, size)


def place_center(mask_img, cy):
    return ((W - mask_img.width) // 2, int(cy - mask_img.height / 2))


# 1. Headline e assunto.
head = text_mask("DE ONDE VEM?", fit("DE ONDE VEM?", GOTHIC_B, 870, 200))
box = place_center(head, 772)
glow_paste(head, box, Image.new("RGB", head.size, (255, 255, 255)), (70, 140, 255), 16, 0.55)
subj_font = fit("INTEGRAÇÃO POR PARTES", GOTHIC_B, 870, 120)
subj = text_mask("INTEGRAÇÃO POR PARTES", subj_font)
box = place_center(subj, 920)
glow_paste(subj, box, gradient(subj.size, BRAND), (110, 90, 255), 14, 0.45)

# 2. Linha de série, no lugar e escala da linha de série da capa do vid_0002.
series = text_mask("POR TRÁS DA FÓRMULA · EP. 01", ImageFont.truetype(GOTHIC, 38), tracking=9)
if series.width > 850:
    series = series.resize((850, round(series.height * 850 / series.width)), Image.LANCZOS)
glow_paste(series, place_center(series, 1097), Image.new("RGB", series.size, (236, 240, 255)),
           (60, 120, 255), 6, 0.25)


# 3. Painel: (uv)' = u'v + uv'  ↓  ∫ u dv = uv − ∫ v du
def math_mask(tokens, size):
    """tokens: (texto, itálico?, escala, dy_em, espaço_depois_em)."""
    pieces, x = [], 0
    for text, italic, scale, dy, gap in tokens:
        f = ImageFont.truetype(TIMES_I if italic else TIMES, round(size * scale))
        pieces.append((x, dy * size, text, f)); x += f.getlength(text) + gap * size
    m = Image.new("L", (int(x) + 40, size * 3), 0); d = ImageDraw.Draw(m)
    base = size * 1.9
    for px, dy, text, f in pieces:
        d.text((px + 10, base + dy), text, font=f, fill=255, anchor="ls")
    return m.crop(m.getbbox())


S = 0.3  # espaço médio (em)
product = math_mask([("(", 0, 1, 0, 0), ("uv", 1, 1, 0, 0.02), (")", 0, 1, 0, 0),
                     ("′", 0, 1, 0, S), ("=", 0, 1, 0, S), ("u", 1, 1, 0, 0.02),
                     ("′", 0, 1, 0, 0), ("v", 1, 1, 0, S), ("+", 0, 1, 0, S),
                     ("uv", 1, 1, 0, 0.02), ("′", 0, 1, 0, 0)], 68)
parts = math_mask([("∫", 0, 1.55, 0.2, 0.08), ("u", 1, 1, 0, 0.22), ("dv", 1, 1, 0, S),
                   ("=", 0, 1, 0, S), ("uv", 1, 1, 0, S), ("−", 0, 1, 0, S),
                   ("∫", 0, 1.55, 0.2, 0.08), ("v", 1, 1, 0, 0.22), ("du", 1, 1, 0, 0)], 70)
glow_paste(product, place_center(product, 1232), gradient(product.size, PALE), (80, 150, 255), 10, 0.5)
glow_paste(parts, place_center(parts, 1368), gradient(parts.size, PALE), (150, 110, 255), 10, 0.5)

arrow = Image.new("L", (44, 56), 0); d = ImageDraw.Draw(arrow)
d.line((22, 0, 22, 38), fill=255, width=5); d.polygon([(8, 34), (36, 34), (22, 55)], fill=255)
glow_paste(arrow, place_center(arrow, 1296), gradient(arrow.size, BRAND[:3]), (60, 170, 255), 8, 0.6)

img.convert("RGB").save(OUT, optimize=True)
print(OUT, img.size)
