"""Gera as 6 propostas de capa do vid_0008 (POR TRÁS DA FÓRMULA · EP. 03), com a fórmula estampada.

Uso, na raiz do repositório:
    uv run python videos/vid_0008_campo_espira/gerar_capa.py [PASTA_SAIDA]

Mesmo layout e mesma base das capas da série (base versionada
videos/vid_0002_integral_substituicao/capa_instagram.png, da qual se apagam título, linha de
série e interior do painel; fundo, símbolo, divisor, borda do painel, marca e horizonte são
preservados). A fórmula sai de MathTex com o template de cores da cena (R ciano, z azul):
    B_z(z) = mu0 I R^2 / 2 (R^2 + z^2)^{3/2}
A curva do gráfico usa b_loop, a mesma função da cena.

Propostas: A a F (headline + painel diferentes; F traz a fórmula gigante ao fundo, translúcida).
"""
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(UNIT))
from template.fonts import SPACE_GROTESK, screen_text  # noqa: E402
from comum import b_loop, mtex, tex  # noqa: E402

BASE = UNIT.parent / "vid_0002_integral_substituicao" / "capa_instagram.png"
TMP_MEDIA = ROOT / "media" / "_capa_vid0008_tmp"
BOLD, MEDIUM = str(SPACE_GROTESK["bold"]), str(SPACE_GROTESK["medium"])
BRAND = [(0x35, 0xD9, 0xFF), (0x26, 0x7B, 0xFF), (0x74, 0x5C, 0xFF), (0xEA, 0x63, 0xFF)]
CYAN, WHITE, BLUE, VIOLET, MAGENTA = "#35D9FF", "#F5F7FF", "#267BFF", "#745CFF", "#EA63FF"
SERIE = "POR TRÁS DA FÓRMULA · EP. 03"


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


# ── Peças de painel ───────────────────────────────────────────────────────────
def formula(size=60):
    return mtex(r"B_z(\vZ)", "=", r"\frac{\mu_0 I \vR^2}{2\left(\vR^2+\vZ^2\right)^{3/2}}", size=size)


def espira_icon(rs=1.25, tilt=0.30):
    """Espira pseudo-3D com o eixo, P e a seta do campo (como na cena)."""
    from manim import PI, Arrow, DashedLine, Dot, Line, VGroup, VMobject
    pt = lambda phi: np.array([rs * tilt * np.sin(phi), rs * np.cos(phi), 0.0])
    half = lambda a, op: VMobject().set_points_as_corners(
        [pt(p) for p in np.linspace(a, a + PI, 60)]).set_stroke(BLUE, 16, op)
    p = np.array([2.7, 0, 0])
    return VGroup(half(PI, 0.45), half(0, 1.0),
                  DashedLine([-0.5, 0, 0], p + [0.5, 0, 0], dash_length=0.16).set_stroke(BLUE, 6, 0.6),
                  Arrow(p, p + [1.0, 0, 0], buff=0, stroke_width=20, tip_length=0.4, color=CYAN,
                        max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=60),
                  Dot(p, 0.16, color=WHITE),
                  Line([0, 0, 0], [0, rs, 0]).set_stroke(CYAN, 10),
                  Line([0, rs, 0], p).set_stroke(VIOLET, 10))


def triangulo_icon():
    """Triângulo R (ciano) – z (azul) – r (violeta), com os rótulos."""
    from manim import VGroup, Line
    O, T, P = np.array([0, 0, 0.0]), np.array([0, 1.5, 0.0]), np.array([2.2, 0, 0.0])
    g = VGroup(Line(O, T).set_stroke(CYAN, 16), Line(O, P).set_stroke(BLUE, 16),
               Line(T, P).set_stroke(VIOLET, 16))
    g.add(tex("R", 90, CYAN).move_to([-0.42, 0.75, 0]), tex("z", 90, BLUE).move_to([1.1, -0.42, 0]),
          tex("r", 90, VIOLET).move_to([1.45, 0.98, 0]))
    return g


def grafico_icon(w=3.6, h=1.9, zmax=3.4):
    """B_z/B_z(0) contra z/R, simétrico; o pico em magenta."""
    from manim import Circle, Dot, Line, VGroup, VMobject
    gp = lambda z: np.array([w * z / zmax, h * float(b_loop(z)), 0.0])
    return VGroup(Line([-w - 0.15, 0, 0], [w + 0.15, 0, 0]).set_stroke(BLUE, 7, 0.85),
                  Line([0, -0.05, 0], [0, h + 0.3, 0]).set_stroke(BLUE, 7, 0.85),
                  VMobject().set_points_as_corners([gp(z) for z in np.linspace(-zmax, zmax, 260)]
                                                   ).set_stroke(CYAN, 16),
                  Circle(0.34).move_to(gp(0)).set_stroke(MAGENTA, 6, 0.55),
                  Dot(gp(0), 0.2, color=MAGENTA))


def chips():
    """GEOMETRIA · SIMETRIA · BIOT-SAVART."""
    from manim import RIGHT, RoundedRectangle, VGroup
    itens = VGroup()
    for t, c in (("GEOMETRIA", CYAN), ("SIMETRIA", MAGENTA), ("BIOT-SAVART", VIOLET)):
        tx = screen_text(t, 34).set_color(WHITE)
        bg = RoundedRectangle(width=tx.width + 0.5, height=tx.height + 0.38, corner_radius=0.2
                              ).set_stroke(c, 5, 1.0).set_fill(c, 0.12)
        itens.add(VGroup(bg, tx))
    return itens.arrange(RIGHT, buff=0.35)


def painel(kind):
    from manim import DOWN, RIGHT, VGroup
    if kind == "formula":
        return formula(80)
    if kind == "formula+grafico":
        return VGroup(formula(62), grafico_icon()).arrange(RIGHT, buff=0.7)
    if kind == "triangulo+formula":
        return VGroup(triangulo_icon(), formula(62)).arrange(RIGHT, buff=0.8)
    if kind == "espira+formula":
        return VGroup(espira_icon(), formula(60)).arrange(RIGHT, buff=0.8)
    if kind == "formula+chips":
        return VGroup(formula(72), chips()).arrange(DOWN, buff=0.45)
    if kind == "espira+grafico":
        return VGroup(espira_icon(), grafico_icon()).arrange(RIGHT, buff=0.9, aligned_edge=DOWN)
    raise ValueError(kind)


# ── Propostas: (headline, painel, fórmula-fantasma) ───────────────────────────
PROPOSTAS = {
    "A": ([([("DE ONDE VEM", "white")], 84), ([("O CAMPO MAGNÉTICO", "white")], 130),
           ([("DE UMA ESPIRA?", "grad")], 150)], "formula", False),
    "B": ([([("VOCÊ DECOROU", "white")], 150), ([("ESSA FÓRMULA?", "grad")], 150)], "formula+grafico", False),
    "C": ([([("ELA NÃO SURGE", "white")], 150), ([("DO NADA", "grad")], 190)], "triangulo+formula", False),
    "D": ([([("DECORAR OU", "white")], 150), ([("CONSTRUIR?", "grad")], 190)], "espira+formula", False),
    "E": ([([("3 IDEIAS.", "white")], 150), ([("1 FÓRMULA.", "grad")], 190)], "formula+chips", False),
    "F": ([([("A FÓRMULA", "white")], 124), ([("POR TRÁS DO CAMPO", "white")], 90),
           ([("DA ESPIRA", "grad")], 124)], "espira+grafico", True),
}


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
    for x0, y0, patch in (erase_vertical(64, 1016, 666, 1000),
                          erase_vertical(96, 988, 1052, 1142),
                          erase_bilinear(226, 874, 1194, 1420)):
        h, w = patch.shape[:2]
        fill[y0:y0 + h, x0:x0 + w] = patch
        mask[y0:y0 + h, x0:x0 + w] = 1
    m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(8))).astype(np.float32)[..., None] / 255
    fill += np.random.default_rng(5).normal(0, 1.6, fill.shape)
    return Image.fromarray((arr * (1 - m) + fill * m).clip(0, 255).astype(np.uint8)).convert("RGBA")


def gradient(size, stops):
    w, h = size
    seg = np.clip(np.linspace(0, 1, w) * (len(stops) - 1), 0, len(stops) - 1 - 1e-6)
    i = seg.astype(int); f = (seg - i)[:, None]
    row = (np.array(stops)[i] * (1 - f) + np.array(stops)[i + 1] * f).astype(np.uint8)
    return Image.fromarray(np.repeat(row[None], h, 0), "RGB")


def glow_paste(img, layer_mask, box, color_img, glow_color, glow_radius, glow_alpha):
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


def cover(lines, panel_art, ghost_art=None):
    img = base()
    if ghost_art is not None:      # fórmula gigante, translúcida, atrás da headline
        g = ghost_art.resize((940, round(ghost_art.height * 940 / ghost_art.width)), Image.LANCZOS)
        a = g.getchannel("A").point(lambda v: int(v * 0.09))
        g.putalpha(a)
        img.alpha_composite(g, ((img.width - g.width) // 2, 830 - g.height // 2))
    rows = [headline_line(seg, start) for seg, start in lines]
    gap = 22
    total = sum(r[0].height for r in rows) + gap * (len(rows) - 1)
    assert total <= 340, f"headline alta demais: {total}px"
    y = 832 - total / 2
    for mask, color, glow, _ in rows:
        img = glow_paste(img, mask, ((img.width - mask.width) // 2, int(y)), color, glow, 15, 0.5)
        y += mask.height + gap
    series = text_mask(SERIE, ImageFont.truetype(MEDIUM, 38), tracking=9)
    series = series.resize((min(series.width, 850), round(series.height * min(series.width, 850) / series.width)),
                           Image.LANCZOS)
    img = glow_paste(img, series, center(img, series, 1097), Image.new("RGB", series.size, (245, 247, 255)),
                     (60, 120, 255), 6, 0.32)
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
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capas"
    out.mkdir(parents=True, exist_ok=True)
    ghost = render_rgba(lambda: formula(70), 400)
    so = sys.argv[2] if len(sys.argv) > 2 else None
    for nome, (lines, kind, com_ghost) in PROPOSTAS.items():
        if so and nome != so:
            continue
        alvo = out / f"capa_{nome}.png"
        cover(lines, render_rgba(lambda k=kind: painel(k), 400), ghost if com_ghost else None).save(alvo, optimize=True)
        print(alvo)
