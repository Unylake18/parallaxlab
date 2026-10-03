"""Gera as 6 propostas de capa do vid_0009 (DA EQUAÇÃO AO FENÔMENO · EP. 03).

Uso, na raiz do repositório:
    uv run python videos/vid_0009_campo_solenoide/gerar_capa.py [PASTA_SAIDA [LETRA]]

Mesmo layout e mesma base das capas da série (base versionada
videos/vid_0002_integral_substituicao/capa_instagram.png, da qual se apagam título, linha de
série e interior do painel; fundo, símbolo, divisor, borda do painel, marca e horizonte são
preservados). Painéis em Manim com a paleta da cena: bobina azul, campo B ciano, corrente verde,
contorno de Ampère magenta. O gráfico usa a mesma B(z) da cena (bobina finita, fórmula fechada).

Propostas: A, B, C (C2 = variante de headline), D, E, F; sem fórmula-fantasma.
"""
import os
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
from comum import mtex, tex  # noqa: E402

BASE = UNIT.parent / "vid_0002_integral_substituicao" / "capa_instagram.png"
TMP_MEDIA = ROOT / "media" / "_capa_vid0009_tmp"
BOLD, MEDIUM = str(SPACE_GROTESK["bold"]), str(SPACE_GROTESK["medium"])
BRAND = [(0x35, 0xD9, 0xFF), (0x26, 0x7B, 0xFF), (0x74, 0x5C, 0xFF), (0xEA, 0x63, 0xFF)]
CYAN, WHITE, BLUE, VIOLET, MAGENTA = "#35D9FF", "#F5F7FF", "#267BFF", "#745CFF", "#EA63FF"
GREEN = "#3FE08B"                  # corrente (a mesma cor da cena)
SERIE = "DA EQUAÇÃO AO FENÔMENO · EP. 03"


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
def formula(size=64):
    f = mtex("B", "=", r"\mu_0", "n", "I", size=size)
    f[0].set_color(CYAN)
    f[3].set_color(GREEN)
    f[4].set_color(GREEN)
    return f


def leitura(size=46):
    """I sobe => B sobe; n sobe => B sobe (corrente verde, campo ciano)."""
    from manim import DOWN, VGroup
    a = mtex("I", r"\uparrow", r"\Rightarrow", "B", r"\uparrow", size=size)
    b = mtex("n", r"\uparrow", r"\Rightarrow", "B", r"\uparrow", size=size)
    for m, c in ((a, GREEN), (b, GREEN)):
        m[0].set_color(c)
        m[1].set_color(c)
        m[3].set_color(CYAN)
        m[4].set_color(CYAN)
    return VGroup(a, b).arrange(DOWN, buff=0.35)


def aneis(n, w, rs=1.0, tilt=0.30, destaque=None):
    """n espiras pseudo-3D ao longo do eixo x (metade de trás apagada), como na cena."""
    from manim import PI, Line, VGroup, VMobject
    g = VGroup()
    xs = [0.0] if n == 1 else list(np.linspace(-w / 2, w / 2, n))
    for i, x in enumerate(xs):
        pt = lambda phi, x=x: np.array([x + rs * tilt * np.sin(phi), rs * np.cos(phi), 0.0])
        cor = GREEN if i == destaque else BLUE
        for a, op in ((PI, 0.40), (0, 1.0)):
            g.add(VMobject().set_points_as_corners([pt(p) for p in np.linspace(a, a + PI, 40)])
                  .set_stroke(cor, 9 if n > 4 else 14, op))
    if n > 1:
        for s in (-1, 1):
            g.add(Line([xs[0], s * rs, 0], [xs[-1], s * rs, 0]).set_stroke(BLUE, 5, 0.55))
    return g


def setas(w, ys=(-0.4, 0.0, 0.4), color=CYAN, width=14):
    from manim import Arrow, VGroup
    return VGroup(*(Arrow([-w / 2, y, 0], [w / 2, y, 0], buff=0, stroke_width=width, tip_length=0.3,
                          color=color, max_tip_length_to_length_ratio=0.5,
                          max_stroke_width_to_length_ratio=60) for y in ys))


def solenoide(n=9, w=4.2, rs=1.0, destaque=None):
    from manim import VGroup
    return VGroup(aneis(n, w, rs, destaque=destaque), setas(w * 0.85, (-0.35, 0.0, 0.35)))


def seta_branca(w=0.9):
    from manim import Arrow
    return Arrow([0, 0, 0], [w, 0, 0], buff=0, stroke_width=10, tip_length=0.3, color=WHITE,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=60)


def b_fin(z, L=8.0):
    a, b = z + L / 2, z - L / 2
    return 0.5 * (a / np.sqrt(1 + a * a) - b / np.sqrt(1 + b * b))


def grafico(w=3.4, h=1.7, zmax=9.0):
    """B(z) de uma bobina longa: platô no centro (faixa violeta), quedas nas pontas."""
    from manim import Line, Rectangle, VGroup, VMobject
    gp = lambda z: np.array([w * z / zmax, h * float(b_fin(z) / b_fin(0.0)), 0.0])
    banda = Rectangle(width=2 * w * 3.0 / zmax, height=h).set_stroke(width=0).set_fill(VIOLET, 0.28)
    banda.move_to([0, h / 2, 0])
    return VGroup(banda, Line([-w - 0.15, 0, 0], [w + 0.15, 0, 0]).set_stroke(BLUE, 7, 0.85),
                  Line([0, -0.05, 0], [0, h + 0.3, 0]).set_stroke(BLUE, 7, 0.85),
                  VMobject().set_points_as_corners([gp(z) for z in np.linspace(-zmax, zmax, 260)]
                                                   ).set_stroke(CYAN, 16))


def atuador(w=2.3, n=6):
    """Bobina + núcleo (branco) entrando pela entrada + haste e comporta de uma válvula."""
    from manim import Line, Rectangle, RoundedRectangle, VGroup
    bob = aneis(n, w, 0.9)
    xe = w / 2
    nuc = RoundedRectangle(width=1.5, height=0.62, corner_radius=0.14).set_stroke(WHITE, 5, 0.95)
    nuc.set_fill(WHITE, 0.25).move_to([xe + 0.1, 0, 0])
    haste = Line([nuc.get_right()[0], 0, 0], [xe + 1.9, 0, 0]).set_stroke(WHITE, 6, 0.9)
    gate = Rectangle(width=0.5, height=0.3).set_stroke(WHITE, 5, 0.95).set_fill(WHITE, 0.3).move_to([xe + 2.15, 0, 0])
    tubo = VGroup(Line([xe + 2.15, -1.0, 0], [xe + 2.15, -0.3, 0]), Line([xe + 2.15, 0.3, 0], [xe + 2.15, 1.0, 0])
                  ).set_stroke(BLUE, 6, 0.85)
    return VGroup(bob, setas(w * 0.8, (-0.3, 0.3)), nuc, haste, gate, tubo)


def ampere(w=3.6):
    """Corte da bobina (⊙ em cima, ⊗ embaixo), campo B ciano e o retângulo de Ampère magenta
    atravessando a parede de cima."""
    from manim import Circle, Dot, Line, Rectangle, VGroup
    xs = np.linspace(-w / 2, w / 2, 7)
    cima = VGroup(*(VGroup(Circle(0.17).set_stroke(BLUE, 5), Dot(radius=0.06, color=BLUE)).move_to([x, 0.7, 0])
                    for x in xs))
    baixo = VGroup()
    for x in xs:
        c = Circle(0.17).set_stroke(BLUE, 5).move_to([x, -0.7, 0])
        k = 0.17 * 0.7071
        baixo.add(VGroup(c, Line([x - k, -0.7 - k, 0], [x + k, -0.7 + k, 0]).set_stroke(BLUE, 5),
                         Line([x - k, -0.7 + k, 0], [x + k, -0.7 - k, 0]).set_stroke(BLUE, 5)))
    ret = Rectangle(width=w * 0.55, height=1.0).set_stroke(MAGENTA, 9).move_to([0.3, 0.7, 0])
    return VGroup(cima, baixo, setas(w * 0.8, (-0.15, 0.2), width=12), ret)


def seta(x0, x1, y=0.0, color=CYAN, width=16, op=1.0, tip=0.34):
    from manim import Arrow
    return Arrow([x0, y, 0], [x1, y, 0], buff=0, stroke_width=width, tip_length=tip, color=color,
                 max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=60).set_opacity(op)


def seta_c(comprimento, y=0.0, cx=0.0, **kw):
    """Seta de B centrada em cx."""
    return seta(cx - comprimento / 2, cx + comprimento / 2, y, **kw)


def espira_ep8(rs=1.6, tilt=0.30):
    """A espira do episódio 8: anel, eixo tracejado, ponto P e a seta de B_esp."""
    from manim import DashedLine, Dot, VGroup
    p = 1.6
    return VGroup(aneis(1, 0, rs, tilt), DashedLine([-0.4, 0, 0], [p + 0.3, 0, 0], dash_length=0.16).set_stroke(BLUE, 6, 0.6),
                  seta(p, p + 0.9, 0, CYAN, 16), Dot([p, 0, 0], 0.15, color=WHITE))


def bobina_seta(n, w, comp, larg, rs=1.5):
    """Bobina de n espiras (comprimento w) com UMA seta de B centrada: comprimento e espessura contam a história."""
    from manim import VGroup
    return VGroup(aneis(n, w, rs), seta_c(comp, width=larg))


def painel_prog():       # A: 1 espira -> várias -> B bem maior
    from manim import RIGHT, VGroup
    s1 = bobina_seta(1, 0, 0.8, 11)
    s2 = bobina_seta(4, 1.2, 1.9, 16)
    s3 = bobina_seta(7, 2.4, 3.5, 24)
    return VGroup(s1, seta_branca(0.55), s2, seta_branca(0.55), s3).arrange(RIGHT, buff=0.3)


def painel_proximo():    # B: espira do ep. 8 -> poucas espiras (cada uma com a sua) -> solenoide com B resultante
    from manim import RIGHT, VGroup
    s2 = VGroup(aneis(3, 1.7, 1.5), *(seta_c(0.8, cx=x, width=12, op=0.8) for x in np.linspace(-0.85, 0.85, 3)))
    s3 = bobina_seta(8, 2.4, 3.6, 24)
    return VGroup(espira_ep8(), seta_branca(0.55), s2, seta_branca(0.55), s3).arrange(RIGHT, buff=0.3)


def painel_mesmo_espaco():   # C: mesmo comprimento, poucas e depois muitas espiras, B cresce
    from manim import DOWN, Line, RIGHT, VGroup
    def lado(n, comp, larg):
        L = Line([-1.55, 1.8, 0], [1.55, 1.8, 0]).set_stroke(VIOLET, 5, 0.9)
        tk = VGroup(*(Line([x, 1.68, 0], [x, 1.92, 0]).set_stroke(VIOLET, 5, 0.9) for x in (-1.55, 1.55)))
        return VGroup(aneis(n, 3.0, 1.3), seta_c(comp, width=larg), L, tk)
    return VGroup(lado(3, 1.0, 11), seta_branca(0.7), lado(11, 3.0, 24)).arrange(RIGHT, buff=0.45)


def painel_soma():       # D: contribuições de várias espiras somam num B resultante maior
    from manim import RIGHT, VGroup
    def uma():
        from manim import Dot
        return VGroup(aneis(1, 0, 1.45), seta_c(0.85, width=12, op=0.85), Dot([-0.425, 0, 0], 0.11, color=WHITE))
    def op(s):
        return mtex(s, size=80, color=WHITE)
    return VGroup(uma(), op("+"), uma(), op("+"), uma(), op("="), seta_c(2.5, width=26)).arrange(RIGHT, buff=0.3)


def painel_transforma(): # E: espira -> cópias -> solenoide
    from manim import RIGHT, VGroup
    s1 = aneis(1, 0, 1.7)
    s2 = aneis(4, 2.2, 1.7)
    s3 = bobina_seta(10, 3.0, 3.4, 20, 1.7)
    return VGroup(s1, seta_branca(0.7), s2, seta_branca(0.7), s3).arrange(RIGHT, buff=0.35)


def painel_plano():      # F: solenoide em cima, B(z) embaixo com o platô central destacado
    from manim import DOWN, DashedLine, VGroup
    z_ext = 3.4 * 4.0 / 9.0
    topo = VGroup(aneis(9, 2 * z_ext, 0.8, 0.22), seta_c(2.5, width=12))
    graf = grafico(3.4, 1.15)
    guias = VGroup(*(DashedLine([s * z_ext, -0.85, 0], [s * z_ext, -1.55, 0], dash_length=0.12).set_stroke(VIOLET, 4, 0.7)
                     for s in (-1, 1)))
    graf.move_to([0, -2.3, 0])
    return VGroup(topo, guias, graf)


PAINEIS = {"prog": painel_prog, "proximo": painel_proximo, "espaco": painel_mesmo_espaco,
           "soma": painel_soma, "transforma": painel_transforma, "plano": painel_plano}


def painel_minimo():     # solenoide cheio de espiras e setas internas fortes
    from manim import VGroup
    return VGroup(aneis(12, 4.4, 1.5), setas(4.0, (-0.6, 0.0, 0.6), width=24))


PAINEIS["minimo"] = painel_minimo


def painel_final(forte=False):
    """Opção 4 refinada: espira reconhecível -> poucas -> solenoide dominante; B cresce nas três etapas."""
    from manim import RIGHT, VGroup
    s1 = VGroup(aneis(1, 0, 1.7), seta_c(0.9, width=12))
    s2 = VGroup(aneis(4, 2.0, 1.7), seta_c(1.9, width=17))
    s3 = VGroup(aneis(11, 3.6, 1.9), seta_c(5.0 if forte else 3.5, width=30 if forte else 24))
    return VGroup(s1, seta_branca(0.7), s2, seta_branca(0.7), s3).arrange(RIGHT, buff=0.4)


PAINEIS["final"] = lambda: painel_final(False)
PAINEIS["final_forte"] = lambda: painel_final(True)


def painel(kind):
    return PAINEIS[kind]()


# ── Base: título, série, logo menor e moldura maior ───────────────────────────
def gradient(size, stops):
    w, h = size
    seg = np.clip(np.linspace(0, 1, w) * (len(stops) - 1), 0, len(stops) - 1 - 1e-6)
    i = seg.astype(int); f = (seg - i)[:, None]
    row = (np.array(stops)[i] * (1 - f) + np.array(stops)[i + 1] * f).astype(np.uint8)
    return Image.fromarray(np.repeat(row[None], h, 0), "RGB")


LOGO_K = 0.78                       # reduz o símbolo do topo (a marca já aparece embaixo)
MOLDURA = (120, 1146, 960, 1474)    # painel: +16% de largura e +17% de altura em relação à base
ART_MAX = (780, 275)                # área útil do diagrama dentro da moldura


def encolher_logo(res, soft, k=LOGO_K, centro=(560, 400)):
    """Reduz o símbolo. O fundo da região vem só das bordas (patch de Coons), sem herdar brilho do logo antigo."""
    x0, x1, y0, y1 = 320, 810, 110, 690
    fg = res[y0:y1, x0:x1].copy()
    h, w = fg.shape[:2]
    suave = lambda v: np.asarray(Image.fromarray(np.clip(v, 0, 255).astype(np.uint8)[None]).filter(
        ImageFilter.GaussianBlur(6))).astype(np.float32)[0]
    topo, base_ = suave(soft[y0, x0:x1]), suave(soft[y1 - 1, x0:x1])
    esq, dir_ = suave(soft[y0:y1, x0]), suave(soft[y0:y1, x1 - 1])
    u = np.linspace(0, 1, w)[None, :, None]
    v = np.linspace(0, 1, h)[:, None, None]
    cantos = (1 - v) * ((1 - u) * topo[0] + u * topo[-1]) + v * ((1 - u) * base_[0] + u * base_[-1])
    bg = (1 - v) * topo[None] + v * base_[None] + (1 - u) * esq[:, None] + u * dir_[:, None] - cantos
    bg = bg.clip(0, 255) + np.random.default_rng(7).normal(0, 1.6, bg.shape)
    alfa = np.clip((fg.max(2) - bg.max(2)) / 70.0, 0, 1)
    jan = lambda n, f: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / f, 0, 1)
    feather = np.outer(jan(h, 45), jan(w, 45))
    res[y0:y1, x0:x1] = fg * (1 - feather[..., None]) + bg * feather[..., None]
    nw, nh = round(w * k), round(h * k)
    fgs = np.asarray(Image.fromarray(fg.clip(0, 255).astype(np.uint8)).resize((nw, nh), Image.LANCZOS)).astype(np.float32)
    als = np.asarray(Image.fromarray((alfa * feather * 255).astype(np.uint8)).resize((nw, nh), Image.LANCZOS)).astype(np.float32) / 255
    px, py = int(centro[0] - nw / 2), int(centro[1] - nh / 2)
    reg = res[py:py + nh, px:px + nw]
    res[py:py + nh, px:px + nw] = reg * (1 - als[..., None]) + fgs * als[..., None]
    return res


def desenhar_moldura(img, cantos):
    """Moldura do painel maior: interior em gradiente bilinear dos cantos originais e borda branca→magenta."""
    x0, y0, x1, y1 = MOLDURA
    w, h = x1 - x0, y1 - y0
    tl, tr, bl, br = cantos
    u = np.linspace(0, 1, w)[None, :, None]
    v = np.linspace(0, 1, h)[:, None, None]
    interior = ((1 - v) * ((1 - u) * tl + u * tr) + v * ((1 - u) * bl + u * br)).clip(0, 255).astype(np.uint8)
    forma = Image.new("L", img.size, 0)
    ImageDraw.Draw(forma).rounded_rectangle(MOLDURA, 40, fill=255)
    cheio = Image.new("RGBA", img.size)
    cheio.paste(Image.fromarray(interior).convert("RGBA"), (x0, y0))
    img = Image.composite(cheio, img, forma)
    borda = Image.new("L", img.size, 0)
    ImageDraw.Draw(borda).rounded_rectangle(MOLDURA, 40, outline=255, width=4)
    cores = Image.new("RGBA", img.size)
    cores.paste(gradient((w, h), [(225, 242, 255), (130, 190, 255), (205, 95, 235)]).convert("RGBA"), (x0, y0))
    halo = borda.filter(ImageFilter.GaussianBlur(9)).point(lambda p: int(p * 0.55))
    img = Image.composite(cores, img, halo)
    return Image.composite(cores, img, borda)


def base():
    img = Image.open(BASE).convert("RGB")
    W, H = img.size
    arr = np.asarray(img).astype(np.float32)
    soft = np.asarray(img.filter(ImageFilter.MinFilter(15)).filter(ImageFilter.GaussianBlur(20))).astype(np.float32)
    r = 6
    c = lambda x, y: arr[y - r:y + r, x - r:x + r].reshape(-1, 3).mean(0)
    cantos = (c(226, 1194), c(874, 1194), c(226, 1420), c(874, 1420))     # cores do interior original

    def erase_vertical(x0, x1, y0, y1, blend=30):
        top, bot = soft[y0, x0:x1], soft[y1, x0:x1]
        t = np.clip((np.arange(y1 - y0) - (y1 - y0 - blend)) / blend, 0, 1)[:, None, None]
        return (x0, y0, (1 - t) * top[None] + t * bot[None])

    fill = arr.copy()
    mask = np.zeros((H, W), np.float32)
    for x0, y0, patch in (erase_vertical(64, 1016, 666, 1000),     # título
                          erase_vertical(96, 988, 1052, 1142),    # linha de série
                          erase_vertical(140, 940, 1150, 1470)):  # moldura e interior originais
        h, w = patch.shape[:2]
        fill[y0:y0 + h, x0:x0 + w] = patch
        mask[y0:y0 + h, x0:x0 + w] = 1
    m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(8))).astype(np.float32)[..., None] / 255
    fill += np.random.default_rng(5).normal(0, 1.6, fill.shape)
    res = arr * (1 - m) + fill * m
    res = encolher_logo(res, soft)
    img = Image.fromarray(res.clip(0, 255).astype(np.uint8)).convert("RGBA")
    return desenhar_moldura(img, cantos)


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
    k = min(ART_MAX[0] / art.width, ART_MAX[1] / art.height)
    art = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)
    x, y = (img.width - art.width) // 2, 1310 - art.height // 2
    full = Image.new("L", img.size, 0); full.paste(art.getchannel("A"), (x, y))
    halo = full.filter(ImageFilter.GaussianBlur(10)).point(lambda p: int(p * 0.3))
    img = Image.composite(Image.new("RGBA", img.size, (90, 110, 255, 255)), img, halo)
    img.alpha_composite(art, (x, y))
    return img.convert("RGB")




# ── Propostas: (headline, painel, fórmula-fantasma) ───────────────────────────
PROPOSTAS = {
    "A": ([([("ENROLAR O FIO", "white")], 130), ([("REFORÇA O CAMPO?", "grad")], 130)], "prog", False),
    "B": ([([("E SE FOREM", "white")], 150), ([("MUITAS ESPIRAS?", "grad")], 150)], "proximo", False),
    "C": ([([("MAIS ESPIRAS,", "white")], 140), ([("CAMPO MAIS FORTE", "grad")], 140)], "espaco", False),
    "C2": ([([("MAIS ESPIRAS", "white")], 100), ([("NO MESMO ESPAÇO,", "white")], 100),
            ([("CAMPO MAIS FORTE", "grad")], 100)], "espaco", False),
    "D": ([([("COMO VÁRIAS ESPIRAS", "white")], 120), ([("SOMAM SEUS CAMPOS?", "grad")], 120)], "soma", False),
    "E": ([([("DA ESPIRA", "white")], 150), ([("AO SOLENOIDE", "grad")], 150)], "transforma", False),
    "F": ([([("POR QUE O CAMPO", "white")], 120), ([("FICA QUASE PLANO?", "grad")], 120)], "plano", False),
}


# Série "headline B": mesmo título nas seis capas; só o painel muda (CAPA_SET=b6).
_HB = [([("E SE FOREM", "white")], 150), ([("MUITAS ESPIRAS?", "grad")], 150)]
PROPOSTAS_B6 = {str(i): (_HB, k, False) for i, k in
                enumerate(("prog", "soma", "espaco", "transforma", "plano", "minimo"), 1)}
if os.environ.get("CAPA_SET") == "b6":
    PROPOSTAS = PROPOSTAS_B6
if os.environ.get("CAPA_SET") == "final":
    PROPOSTAS = {"final": (_HB, "final", False), "final_vetor_forte": (_HB, "final_forte", False)}


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capas"
    out.mkdir(parents=True, exist_ok=True)
    ghost = None
    so = sys.argv[2] if len(sys.argv) > 2 else None
    for nome, (lines, kind, com_ghost) in PROPOSTAS.items():
        if so and nome != so:
            continue
        alvo = out / (f"capa_B{nome}.png" if os.environ.get("CAPA_SET") == "b6" else f"capa_{nome}.png")
        cover(lines, render_rgba(lambda k=kind: painel(k), 400), ghost if com_ghost else None).save(alvo, optimize=True)
        print(alvo)
