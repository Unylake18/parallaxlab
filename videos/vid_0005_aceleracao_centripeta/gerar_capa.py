"""Gera capa_instagram.png do vid_0005 (POR TRÁS DA FÓRMULA · EP. 02).

Uso, na raiz do repositório:
    uv run python videos/vid_0005_aceleracao_centripeta/gerar_capa.py [SAIDA.png]

Mesmo layout da capa do EP. 01 (vid_0003): base versionada
videos/vid_0002_integral_substituicao/capa_instagram.png, da qual se apagam título,
linha de série e interior do painel; fundo, símbolo, divisor, borda do painel,
marca e horizonte são preservados. No painel (variante aprovada "diagrama"): círculo, v tangente, a_c para o
centro e a_c = v²/R. As variantes "semelhanca" e "delta" ficam como opção.

Fontes: Space Grotesk versionada em assets/fonts/ (tipografia oficial das capas);
matemática em MathTex, como na cena.
"""
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(ROOT))
from template.fonts import SPACE_GROTESK  # noqa: E402

BASE = UNIT.parent / "vid_0002_integral_substituicao" / "capa_instagram.png"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capa_instagram5.png"
TMP_MEDIA = ROOT / "media" / "_capa_vid0005_tmp"   # LaTeX falha em caminhos curtos (~) do Temp
BOLD, MEDIUM = str(SPACE_GROTESK["bold"]), str(SPACE_GROTESK["medium"])
BRAND = [(0x35, 0xD9, 0xFF), (0x26, 0x7B, 0xFF), (0x74, 0x5C, 0xFF), (0xEA, 0x63, 0xFF)]
PALE = [(0xC8, 0xF4, 0xFF), (0xD8, 0xDD, 0xFF), (0xE6, 0xC4, 0xFF)]


def render_rgba(build, height):
    """Renderiza mobjects do Manim em fundo transparente, recortados, com a altura pedida."""
    from manim import Scene, tempconfig

    class Quadro(Scene):
        def construct(self):
            group = build()
            group.scale_to_fit_height(6)
            if group.width > 15:
                group.scale_to_fit_width(15)
            self.add(group)

    with tempconfig({"frame_width": 16, "frame_height": 9, "pixel_width": 3200,
                     "pixel_height": 1800, "transparent": True, "format": "png",
                     "save_last_frame": True, "write_to_movie": False,
                     "media_dir": str(TMP_MEDIA), "verbosity": "WARNING",
                     "disable_caching": True, "output_file": "quadro"}):
        scene = Quadro()
        scene.render()
        image = Image.open(scene.renderer.file_writer.image_file_path).convert("RGBA")
    shutil.rmtree(TMP_MEDIA, ignore_errors=True)
    image = image.crop(image.getchannel("A").getbbox())
    return image.resize((round(image.width * height / image.height), height), Image.LANCZOS)


def tex_mask(content, height):
    """MathTex → máscara L (para receber o gradiente pálido das capas)."""
    from manim import MathTex
    alpha = render_rgba(lambda: MathTex(content, color="#FFFFFF"), height).getchannel("A")
    return alpha.filter(ImageFilter.MaxFilter(3))  # traço do LaTeX é fino para capa


def diagram():
    """Assinatura física do vídeo: círculo, v tangente, a_c para o centro, ângulo reto."""
    from manim import LEFT, RIGHT, Arrow, Circle, Dot, MathTex, VGroup, VMobject
    # Espessuras pensadas para a escala final (~50 px por unidade na capa).
    top = [0, 2, 0]
    arrow = lambda end, color, width, tip: Arrow(top, end, buff=0, color=color, stroke_width=width,
                                                 tip_length=tip, max_tip_length_to_length_ratio=0.4,
                                                 max_stroke_width_to_length_ratio=100)
    v = arrow([-2.3, 2, 0], "#35D9FF", 22, 0.55)
    a = arrow([0, 0.28, 0], "#745CFF", 30, 0.68)          # radial, para o centro (sem tocá-lo)
    a_halo = a.copy().set_stroke("#F5F7FF", 52, 0.16).set_fill("#F5F7FF", 0.12)  # contraste no painel violeta
    square = VMobject().set_points_as_corners([[-0.4, 2, 0], [-0.4, 1.6, 0], [0, 1.6, 0]])
    label = lambda tex_, color: MathTex(tex_, color=color).scale(1.9).set_stroke(color, 4)
    return VGroup(
        Circle(radius=2).set_stroke("#267BFF", 12, 0.6),  # estrutura, não protagonista
        Dot([0, 0, 0], 0.12, color="#F5F7FF"),
        square.set_stroke("#F5F7FF", 8, 0.75), v, a_halo, a,
        Dot(top, 0.36, color="#35D9FF", fill_opacity=0.25), Dot(top, 0.19, color="#F5F7FF"),
        label(r"\vec v", "#35D9FF").next_to(v.get_end(), LEFT, buff=0.15),
        label(r"\vec a_c", "#745CFF").next_to(a, RIGHT, buff=0.22),
    )


img = Image.open(BASE).convert("RGB")
W, H = img.size
arr = np.asarray(img).astype(np.float32)
# Fundo sem estrelas: mínimo local seguido de suavização.
soft = np.asarray(img.filter(ImageFilter.MinFilter(15)).filter(ImageFilter.GaussianBlur(20))).astype(np.float32)


def erase_vertical(x0, x1, y0, y1, blend=30):
    top, bot = soft[y0, x0:x1], soft[y1, x0:x1]
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
fill += np.random.default_rng(5).normal(0, 1.6, fill.shape)  # grão similar ao original
img = Image.fromarray((arr * (1 - m) + fill * m).clip(0, 255).astype(np.uint8)).convert("RGBA")


def gradient(size, stops):
    w, h = size
    seg = np.clip(np.linspace(0, 1, w) * (len(stops) - 1), 0, len(stops) - 1 - 1e-6)
    i = seg.astype(int); f = (seg - i)[:, None]
    row = (np.array(stops)[i] * (1 - f) + np.array(stops)[i + 1] * f).astype(np.uint8)
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


# 1. Headline e assunto.
head = text_mask("DE ONDE VEM?", fit("DE ONDE VEM?", BOLD, 870, 200))
glow_paste(head, place_center(head, 772), Image.new("RGB", head.size, (255, 255, 255)),
           (70, 140, 255), 16, 0.55)
subj = text_mask("ACELERAÇÃO CENTRÍPETA", fit("ACELERAÇÃO CENTRÍPETA", BOLD, 870, 120))
glow_paste(subj, place_center(subj, 920), gradient(subj.size, BRAND), (110, 90, 255), 14, 0.45)

# 2. Linha de série, no lugar e escala da capa do EP. 01.
series = text_mask("POR TRÁS DA FÓRMULA · EP. 02", ImageFont.truetype(MEDIUM, 38), tracking=9)
if series.width > 850:
    series = series.resize((850, round(series.height * 850 / series.width)), Image.LANCZOS)
glow_paste(series, place_center(series, 1097), Image.new("RGB", series.size, (236, 240, 255)),
           (60, 120, 255), 6, 0.25)

# 3. Painel (interior x 226–874, y 1194–1420).
PANEL_CY = 1307


def arrow_mask(w, h, horizontal):
    mk = Image.new("L", (w, h), 0); d = ImageDraw.Draw(mk)
    if horizontal:
        d.line((0, h // 2, w - 16, h // 2), fill=255, width=5)
        d.polygon([(w - 20, h // 2 - 13), (w - 20, h // 2 + 13), (w - 1, h // 2)], fill=255)
    else:
        d.line((w // 2, 0, w // 2, h - 16), fill=255, width=5)
        d.polygon([(w // 2 - 13, h - 20), (w // 2 + 13, h - 20), (w // 2, h - 1)], fill=255)
    return mk


def paste_row(items, cy, gap=34):
    """Coloca máscaras lado a lado, centradas no painel."""
    x = (W - sum(m.width for m, _ in items) - gap * (len(items) - 1)) // 2
    for mk, colors in items:
        glow_paste(mk, (x, int(cy - mk.height / 2)), gradient(mk.size, colors), (110, 120, 255), 10, 0.5)
        x += mk.width + gap


PAINEL = sys.argv[2] if len(sys.argv) > 2 else "diagrama"   # variante aprovada
if PAINEL == "semelhanca":      # o passo-chave do vídeo: semelhança ⇒ a_c = v²/R
    paste_row([(tex_mask(r"\frac{|\Delta\vec v|}{v}=\frac{|\Delta\vec r|}{R}", 100), PALE),
               (arrow_mask(62, 40, True), BRAND[:3]),
               (tex_mask(r"a_c=\frac{v^2}{R}", 100), PALE)], PANEL_CY)
elif PAINEL == "diagrama":      # fenômeno + fórmula: v tangente, a_c para o centro
    art = render_rgba(diagram, 216)
    formula = tex_mask(r"a_c=\frac{v^2}{R}", 116)
    x, y = (W - art.width - 64 - formula.width) // 2, PANEL_CY - art.height // 2
    full = Image.new("L", img.size, 0); full.paste(art.getchannel("A"), (x, y))
    halo = full.filter(ImageFilter.GaussianBlur(10)).point(lambda p: int(p * 0.3))
    img = Image.composite(Image.new("RGBA", img.size, (90, 110, 255, 255)), img, halo)
    img.alpha_composite(art, (x, y))
    glow_paste(formula, (x + art.width + 64, PANEL_CY - formula.height // 2),
               gradient(formula.size, PALE), (150, 110, 255), 10, 0.5)
else:                           # "delta": Δv = v₊ − v₋ ↓ a_c = v²/R
    dv = tex_mask(r"\Delta\vec v=\vec v_+-\vec v_-", 62)
    ac = tex_mask(r"a_c=\frac{v^2}{R}", 108)
    glow_paste(dv, place_center(dv, 1228), gradient(dv.size, PALE), (80, 150, 255), 10, 0.5)
    glow_paste(ac, place_center(ac, 1364), gradient(ac.size, PALE), (150, 110, 255), 10, 0.5)
    down = arrow_mask(40, 46, False)
    glow_paste(down, place_center(down, 1287), gradient(down.size, BRAND[:3]), (60, 170, 255), 8, 0.6)

img.convert("RGB").save(OUT, optimize=True)
print(OUT, img.size)
