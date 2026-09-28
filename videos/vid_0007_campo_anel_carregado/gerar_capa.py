"""Gera capa_instagram.png do vid_0007 (EXERCÍCIO RESOLVIDO · EP. 03).

Uso, na raiz do repositório:
    uv run python videos/vid_0007_campo_anel_carregado/gerar_capa.py [SAIDA.png]

Headline “ONDE O / CAMPO ELÉTRICO / É MAIS FORTE?”; painel: anel carregado com P no
máximo e a seta do campo, rótulo “anel” (fonte das fórmulas, claro e translúcido, com
linha-guia fina) e o gráfico E(z) com o pico destacado em magenta.

Mesmo layout das capas da série (base versionada
videos/vid_0002_integral_substituicao/capa_instagram.png, da qual se apagam título,
linha de série e interior do painel; fundo, símbolo, divisor, borda do painel, marca e
horizonte são preservados). O painel usa as funções da cena: comprimento das setas e
curva E(z) saem de e(u), com o pico em u = 1/√2.

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
from cena import E_MAX, U_STAR, e  # noqa: E402  mesmas funções da cena (importar antes do tempconfig)
from cena import text as scene_text  # noqa: E402  Space Grotesk Medium, como na animação

BASE = UNIT.parent / "vid_0002_integral_substituicao" / "capa_instagram.png"
TMP_MEDIA = ROOT / "media" / "_capa_vid0007_tmp"   # saída temporária do Manim, apagada após o quadro
BOLD, MEDIUM = str(SPACE_GROTESK["bold"]), str(SPACE_GROTESK["medium"])
BRAND = [(0x35, 0xD9, 0xFF), (0x26, 0x7B, 0xFF), (0x74, 0x5C, 0xFF), (0xEA, 0x63, 0xFF)]
CYAN, WHITE, BLUE, VIOLET, MAGENTA = "#35D9FF", "#F5F7FF", "#267BFF", "#745CFF", "#EA63FF"
LABEL = "#CDEFFF"   # rótulo do anel: ciano bem claro, translúcido


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


# ── Painéis ───────────────────────────────────────────────────────────────────
def ring(u, rs=2.3, tilt=0.25, lmax=1.65):
    """Anel carregado pseudo-3D (com +) e o eixo; P em u, seta de comprimento lmax·e(u)/E_max."""
    from manim import PI, Arrow, Dot, Line, VGroup, VMobject
    pt = lambda phi: np.array([rs * np.cos(phi), rs * tilt * np.sin(phi), 0.0])
    half = lambda a, op: VMobject().set_points_as_corners([pt(p) for p in np.linspace(a, a + PI, 60)]
                                                          ).set_stroke(BLUE, 16, op)
    p = np.array([0, rs * u, 0])
    L = lmax * float(e(u)) / E_MAX
    g = VGroup(half(0, 0.7), Line([0, -0.2, 0], p + [0, L + 0.15, 0]).set_stroke(BLUE, 7, 0.8), half(PI, 1.0))
    for phi in np.arange(10) * 2 * PI / 10 + PI / 10:
        c, op = pt(phi), 0.6 if np.sin(phi) > 0 else 1.0
        g.add(Line(c - [0.13, 0, 0], c + [0.13, 0, 0]).set_stroke(WHITE, 7, op),
              Line(c - [0, 0.13, 0], c + [0, 0.13, 0]).set_stroke(WHITE, 7, op))
    g.add(Arrow(p, p + [0, L, 0], buff=0, stroke_width=20, tip_length=0.46, color=WHITE,
                max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=60),
          Dot(p, 0.16, color=WHITE))
    return g, pt


def graph(w=3.4, h=2.3, umax=3.0):
    """Curva E(z) (ciano) com o pico destacado em magenta e guia violeta até o eixo."""
    from manim import Circle, DashedLine, Dot, Line, VGroup, VMobject
    gp = lambda u: np.array([w * u / umax, h * float(e(u)) / E_MAX, 0.0])
    peak = gp(U_STAR)
    return VGroup(Line([0, 0, 0], [w + 0.15, 0, 0]).set_stroke(BLUE, 7, 0.85),
                  Line([0, 0, 0], [0, h + 0.3, 0]).set_stroke(BLUE, 7, 0.85),
                  VMobject().set_points_as_corners([gp(u) for u in np.linspace(0, umax, 200)]).set_stroke(CYAN, 16),
                  DashedLine(peak * [1, 0, 0], peak, dash_length=0.14).set_stroke(VIOLET, 9),
                  Circle(0.36).move_to(peak).set_stroke(MAGENTA, 6, 0.55),
                  Dot(peak, 0.21, color=MAGENTA))


def panel():
    """Anel (protagonista, à esquerda, com o rótulo “anel”) + gráfico com o pico (à direita).

    Um “fantasma” quase transparente no lugar do rótulo da primeira versão fixa o
    recorte e o arranjo do painel aprovados (anel, seta, gráfico e pico).
    """
    from manim import DOWN, LEFT, PI, RIGHT, Line, MathTex, VGroup
    obj, pt = ring(U_STAR)
    ghost = scene_text("anel", 50, color=WHITE, opacity=0.012).move_to(pt(1.1 * PI) + np.array([-1.15, 0.95, 0]))
    tag = MathTex(r"\text{anel}", font_size=40, color=LABEL).set_opacity(0.7).move_to(ghost).align_to(ghost, LEFT)
    end = pt(1.1 * PI) + [-0.12, 0.08, 0]
    obj.add(ghost, tag, Line(tag.get_corner(DOWN + RIGHT) + [0.06, -0.04, 0], end).set_stroke(LABEL, 3, 0.5))
    return VGroup(obj, graph()).arrange(RIGHT, buff=0.8, aligned_edge=DOWN)


HEADLINE = [([("ONDE O", "white")], 84), ([("CAMPO ELÉTRICO", "white")], 170), ([("É MAIS FORTE?", "grad")], 150)]


# ── Base: apaga título, série e interior do painel ────────────────────────────
def base():
    img = Image.open(BASE).convert("RGB")
    W, H = img.size
    arr = np.asarray(img).astype(np.float32)
    soft = np.asarray(img.filter(ImageFilter.MinFilter(15)).filter(ImageFilter.GaussianBlur(20))).astype(np.float32)

    def erase_vertical(x0, x1, y0, y1, blend=30):
        top, bot = soft[y0, x0:x1], soft[y1, x0:x1]
        t = np.clip((np.arange(y1 - y0) - (y1 - y0 - blend)) / blend, 0, 1)[:, None, None]
        return (x0, y0, (1 - t) * top[None] + t * bot[None])

    def erase_bilinear(x0, x1, y0, y1, r=6):
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
    return Image.fromarray((arr * (1 - m) + fill * m).clip(0, 255).astype(np.uint8)).convert("RGBA")


def gradient(size, stops):
    w, h = size
    seg = np.clip(np.linspace(0, 1, w) * (len(stops) - 1), 0, len(stops) - 1 - 1e-6)
    i = seg.astype(int); f = (seg - i)[:, None]
    row = (np.array(stops)[i] * (1 - f) + np.array(stops)[i + 1] * f).astype(np.uint8)
    return Image.fromarray(np.repeat(row[None], h, 0), "RGB")


def glow_paste(img, layer_mask, box, color_img, glow_color, glow_radius, glow_alpha):
    """Aplica uma máscara L em box com preenchimento e brilho."""
    full = Image.new("L", img.size, 0); full.paste(layer_mask, box[:2])
    halo = full.filter(ImageFilter.GaussianBlur(glow_radius)).point(lambda v: int(v * glow_alpha))
    img = Image.composite(Image.new("RGBA", img.size, glow_color + (255,)), img, halo)
    fill_full = Image.new("RGBA", img.size); fill_full.paste(color_img.convert("RGBA"), box[:2])
    return Image.composite(fill_full, img, full)


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


def center(img, mask_img, cy):
    return ((img.width - mask_img.width) // 2, int(cy - mask_img.height / 2))


def headline_line(segments, start):
    """Uma linha da headline: máscara única; branco ou gradiente da marca por segmento."""
    full = "".join(t for t, _ in segments)
    font = fit(full, BOLD, 870, start)
    raw = Image.new("L", (int(font.getlength(full)) + 8, sum(font.getmetrics()) + 8), 0)
    ImageDraw.Draw(raw).text((4, 4), full, font=font, fill=255)
    box = raw.getbbox()
    mask = raw.crop(box)
    color = Image.new("RGB", mask.size, (255, 255, 255))
    x = 4
    for t, kind in segments:
        w = font.getlength(t)
        if kind == "grad":
            x0, x1 = max(0, int(x - box[0])), min(mask.width, int(x + w - box[0]) + 2)
            color.paste(gradient((x1 - x0, mask.height), BRAND), (x0, 0))
        x += w
    glow = (110, 90, 255) if any(k == "grad" for _, k in segments) else (70, 140, 255)
    return mask, color, glow, font.size


def cover(lines, panel_art):
    img = base()
    # 1. Headline (título: y 666–1000), linhas empilhadas e centradas no bloco.
    rows = [headline_line(seg, start) for seg, start in lines]
    gap = 22
    total = sum(r[0].height for r in rows) + gap * (len(rows) - 1)
    assert total <= 320, f"headline alta demais: {total}px"
    y = 822 - total / 2
    for mask, color, glow, _ in rows:
        img = glow_paste(img, mask, ((img.width - mask.width) // 2, int(y)), color, glow, 15, 0.5)
        y += mask.height + gap
    print("  corpos da headline:", [r[3] for r in rows], "altura", total)
    # 2. Linha de série, no lugar e escala das capas anteriores.
    series = text_mask("EXERCÍCIO RESOLVIDO · EP. 03", ImageFont.truetype(MEDIUM, 38), tracking=9)
    series = series.resize((min(series.width, 850), round(series.height * min(series.width, 850) / series.width)),
                           Image.LANCZOS)
    img = glow_paste(img, series, center(img, series, 1097), Image.new("RGB", series.size, (245, 247, 255)),
                     (60, 120, 255), 6, 0.32)
    # 3. Painel (interior x 226–874, y 1194–1420), centrado, com halo suave.
    art = panel_art
    k = min(600 / art.width, 215 / art.height)
    art = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)
    x, y = (img.width - art.width) // 2, 1307 - art.height // 2
    full = Image.new("L", img.size, 0); full.paste(art.getchannel("A"), (x, y))
    halo = full.filter(ImageFilter.GaussianBlur(10)).point(lambda p: int(p * 0.3))
    img = Image.composite(Image.new("RGBA", img.size, (90, 110, 255, 255)), img, halo)
    img.alpha_composite(art, (x, y))
    return img.convert("RGB")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capa_instagram.png"
    cover(HEADLINE, render_rgba(panel, 400)).save(out, optimize=True)
    print(out)
