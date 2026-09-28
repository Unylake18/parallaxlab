"""Gera capa_instagram.png do vid_0006 (DA EQUAÇÃO AO FENÔMENO · EP. 02).

Uso, na raiz do repositório:
    uv run python videos/vid_0006_cancelamento_ruido/gerar_capa.py [SAIDA.png]

Mesmo layout das capas do vid_0005/vid_0003: base versionada
videos/vid_0002_integral_substituicao/capa_instagram.png, da qual se apagam título,
linha de série e interior do painel; fundo, símbolo, divisor, borda do painel,
marca e horizonte são preservados. Headline “O SOM PODE / CANCELAR O SOM?”.
Painel: INTERFERÊNCIA (ciano + magenta quase opostos → resultante branca pequena)
→ CANCELAMENTO DE RUÍDO (fone com o ruído chegando, a contribuição magenta saindo
e o resíduo branco entre as conchas), com as mesmas funções da cena: resíduo
pequeno, nunca zero.

Fontes: Space Grotesk versionada em assets/fonts/.
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
sys.path.insert(0, str(UNIT))
from cena import fone, noise, residual  # noqa: E402  mesmas funções da cena
from cena import text as scene_text  # noqa: E402  (importar antes do tempconfig)

BASE = UNIT.parent / "vid_0002_integral_substituicao" / "capa_instagram.png"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capa_instagram.png"
TMP_MEDIA = ROOT / "media" / "_capa_vid0006_tmp"   # saída temporária do Manim, apagada após o quadro
BOLD, MEDIUM = str(SPACE_GROTESK["bold"]), str(SPACE_GROTESK["medium"])
BRAND = [(0x35, 0xD9, 0xFF), (0x26, 0x7B, 0xFF), (0x74, 0x5C, 0xFF), (0xEA, 0x63, 0xFF)]
G, WTAU = 0.95, 0.03 * np.pi                        # melhor ajuste da cena (resíduo ≈ 0,105A)
CYAN, MAGENTA, WHITE, BLUE = "#35D9FF", "#EA63FF", "#F5F7FF", "#267BFF"


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


# ── Painel: física → aplicação ────────────────────────────────────────────────
def curve(x0, x1, y, amp, f, color, width, periods=2):
    """Curva y = amp·f(ωt) em [x0, x1], com as funções da cena (f recebe ωt)."""
    from manim import VMobject
    xs = np.linspace(x0, x1, 300)
    wt = 2 * np.pi * periods * (xs - x0) / (x1 - x0)
    return VMobject().set_points_smoothly(np.column_stack([xs, y + amp * f(wt), 0 * xs])).set_stroke(color, width)


def headphone_icon():
    """Fone de ouvido visto de frente (haste, conchas e almofadas), centrado em x = 0."""
    from manim import PI, Arc, Line, RoundedRectangle, VGroup
    band = Arc(radius=2.3, start_angle=0.15, angle=PI - 0.3).shift([0, 0.2, 0]).set_stroke(BLUE, 16)
    sliders = VGroup(*(Line([s * 2.27, 0.54, 0], [s * 2.3, 0.2, 0]) for s in (-1, 1))).set_stroke(BLUE, 14)
    cups = VGroup(*(RoundedRectangle(width=0.95, height=1.9, corner_radius=0.4).move_to([s * 2.3, -0.7, 0])
                    for s in (-1, 1))).set_stroke(BLUE, 10).set_fill(BLUE, 0.35)
    pads = VGroup(*(RoundedRectangle(width=0.28, height=1.5, corner_radius=0.14).move_to([s * 1.7, -0.7, 0])
                    for s in (-1, 1))).set_stroke(BLUE, 6).set_fill(BLUE, 0.6)
    return VGroup(band, sliders, cups, pads)


def interference(x0, x1, y, amp):
    """Ruído (ciano) e fone (magenta) quase opostos no mesmo eixo; a soma branca fica pequena, não nula."""
    from manim import VGroup
    return VGroup(curve(x0, x1, y, amp, lambda w: noise(w, 0), CYAN, 12),
                  curve(x0, x1, y, amp, lambda w: fone(w, G, WTAU, 0), MAGENTA, 12),
                  curve(x0, x1, y, amp, lambda w: residual(w, G, WTAU, 0), WHITE, 20))


def fone_applied(cx, cy, k):
    """Fone (escala k): ruído ciano chegando, contribuição magenta saindo do próprio fone
    (ele adiciona, não só bloqueia) e o resíduo branco entre as conchas."""
    from manim import PI, Arc, VGroup
    icon = headphone_icon().scale(k).move_to([cx, cy, 0])
    cup_l = icon[2][0]
    pad_l, pad_r = icon[3]
    y, amp = cup_l.get_center()[1], 0.62 * k / 0.75
    group = VGroup(icon,
                   curve(pad_l.get_right()[0] + 0.12, pad_r.get_left()[0] - 0.12, y, amp,
                         lambda w: residual(w, G, WTAU, 0), WHITE, 16, periods=1.5),
                   curve(cup_l.get_left()[0] - 1.42, cup_l.get_left()[0] - 0.12, y, amp,
                         lambda w: noise(w, 0), CYAN, 12, periods=1))
    for center, start in (([pad_l.get_right()[0], y, 0], -0.55), ([pad_r.get_left()[0], y, 0], PI - 0.55)):
        for j, r in enumerate((0.4, 0.72)):
            group.add(Arc(radius=r * k / 0.85, start_angle=start, angle=1.1, arc_center=center)
                      .set_stroke(MAGENTA, 12, 1.0 - 0.25 * j))
    return group


def panel():
    """INTERFERÊNCIA → CANCELAMENTO DE RUÍDO: ciano + magenta → branco pequeno, nos dois lados."""
    from manim import Arrow, VGroup
    right = fone_applied(3.9, 0.6, 0.85)
    y = right[0][2][0].get_center()[1]               # altura do centro das conchas
    bottom = y - 1.75                                 # rótulos abaixo do vale das ondas
    labels = VGroup(scene_text("INTERFERÊNCIA", 48, color=WHITE).move_to([-4.35, bottom, 0]),
                    scene_text("CANCELAMENTO DE RUÍDO", 48, color=WHITE).move_to([3.45, bottom, 0]))
    arrow = Arrow([-2.0, y, 0], [-0.9, y, 0], buff=0, color=WHITE, stroke_width=9, tip_length=0.3)
    return VGroup(interference(-6.4, -2.3, y, 1.1), arrow, right, labels)


# ── Base: apaga título, série e interior do painel ────────────────────────────
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


# 1. Headline em duas linhas (branco + gradiente da marca), como no EP. 01 da série.
head = text_mask("O SOM PODE", fit("O SOM PODE", BOLD, 870, 170))
glow_paste(head, place_center(head, 772), Image.new("RGB", head.size, (255, 255, 255)),
           (70, 140, 255), 16, 0.55)
subj = text_mask("CANCELAR O SOM?", fit("CANCELAR O SOM?", BOLD, 870, 130))
glow_paste(subj, place_center(subj, 920), gradient(subj.size, BRAND), (110, 90, 255), 14, 0.45)

# 2. Linha de série, no lugar e escala das capas anteriores.
series = text_mask("DA EQUAÇÃO AO FENÔMENO · EP. 02", ImageFont.truetype(MEDIUM, 38), tracking=9)
if series.width > 850:
    series = series.resize((850, round(series.height * 850 / series.width)), Image.LANCZOS)
glow_paste(series, place_center(series, 1097), Image.new("RGB", series.size, (245, 247, 255)),
           (60, 120, 255), 6, 0.32)

# 3. Painel (interior x 226–874, y 1194–1420), centrado, com halo suave.
art = render_rgba(panel, 400)
k = min(600 / art.width, 205 / art.height)
art = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)
x, y = (W - art.width) // 2, 1307 - art.height // 2
full = Image.new("L", img.size, 0); full.paste(art.getchannel("A"), (x, y))
halo = full.filter(ImageFilter.GaussianBlur(10)).point(lambda p: int(p * 0.3))
img = Image.composite(Image.new("RGBA", img.size, (90, 110, 255, 255)), img, halo)
img.alpha_composite(art, (x, y))

img.convert("RGB").save(OUT, optimize=True)
print(OUT, img.size)
