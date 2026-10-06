"""yt_0001 — 10 propostas de thumbnail para o YouTube (1280×720, 16:9).

Uso, na raiz do repositório:
    uv run --no-sync python videos_longos/yt_0001_lei_gauss/gerar_thumbs.py [NUMEROS...]

Composição em 2560×1440 e redução para 1280×720 (PNG < 2 MB, limite do YouTube). Fundo: banner 16:9 oficial
com o símbolo central apagado (patch de Coons a partir das bordas, como nas capas verticais). Marca: logo
horizontal oficial pequeno no canto superior esquerdo (o canto inferior direito fica livre para a duração do
vídeo e o superior direito para os ícones do YouTube). Títulos em Space Grotesk Bold; desenhos em Manim com a
gramática visual do vídeo: ciano = campo E, azul = distribuição física, violeta tracejado = gaussiana,
âmbar = ângulos, magenta = passo inválido.
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

from manim import (  # noqa: E402
    DOWN, LEFT, ORIGIN, RIGHT, UP, Arc, Arrow, Circle, DashedVMobject, Dot, Ellipse, Line, MathTex, Polygon,
    Scene, VGroup, tempconfig,
)

SAIDA = UNIT / "thumbs"
TMP = ROOT / "media" / "_thumbs_yt0001_tmp"
BANNER = ROOT / "assets" / "branding" / "social" / "parallax_lab_banner_16x9.png"
LOGO_H = ROOT / "assets" / "branding" / "overlays" / "parallax_lab_watermark.png"
BOLD, MEDIUM = str(SPACE_GROTESK["bold"]), str(SPACE_GROTESK["medium"])
W, H = 2560, 1440

CYAN, BLUE, VIOLET, MAGENTA, WHITE = "#35D9FF", "#267BFF", "#745CFF", "#EA63FF", "#F5F7FF"
VIOLET_L, BLUE_L, AMBER = "#A898FF", "#7FB2FF", "#FFC24D"
BRAND = [(0x35, 0xD9, 0xFF), (0x26, 0x7B, 0xFF), (0x74, 0x5C, 0xFF), (0xEA, 0x63, 0xFF)]
CAIXA = {"M": (0xD9, 0x3F, 0xF0), "C": (0x35, 0xD9, 0xFF)}
COR = {"e": (5, 8, 22), "w": (245, 247, 255), "c": (0x35, 0xD9, 0xFF), "m": (0xEA, 0x63, 0xFF), "a": (0xFF, 0xC2, 0x4D),
       "v": (0xA8, 0x98, 0xFF)}


# ── Fundo e marca ─────────────────────────────────────────────────────────────
def fundo():
    img = Image.open(BANNER).convert("RGB")
    arr = np.asarray(img).astype(np.float32)
    soft = np.asarray(img.filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(12))).astype(np.float32)
    x0, x1, y0, y1 = 495, 1195, 150, 740                     # símbolo + PARALLAX LAB do banner
    h, w = y1 - y0, x1 - x0
    topo, base, esq, dir_ = soft[y0, x0:x1], soft[y1 - 1, x0:x1], soft[y0:y1, x0], soft[y0:y1, x1 - 1]
    u = np.linspace(0, 1, w)[None, :, None]
    v = np.linspace(0, 1, h)[:, None, None]
    cantos = (1 - v) * ((1 - u) * topo[0] + u * topo[-1]) + v * ((1 - u) * base[0] + u * base[-1])
    bg = (1 - v) * topo[None] + v * base[None] + (1 - u) * esq[:, None] + u * dir_[:, None] - cantos
    rng = np.random.default_rng(3)
    st = np.zeros((h, w), np.float32)
    idx = rng.random(st.shape) < 0.0015
    st[idx] = rng.uniform(50, 220, idx.sum())
    st = np.asarray(Image.fromarray(st.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32)
    bg = bg + 2.5 * st[..., None] * np.array([0.75, 0.85, 1.0])
    jan = lambda n, f: np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / f, 0, 1)
    fe = np.outer(jan(h, 40), jan(w, 40))[..., None]
    arr[y0:y1, x0:x1] = arr[y0:y1, x0:x1] * (1 - fe) + bg * fe
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8)).resize((W, H), Image.LANCZOS).convert("RGBA")


def escurecer(img, lado="esq", forca=0.62, ate=0.62):
    """Véu escuro para leitura do título: horizontal (esq) ou vertical (topo)."""
    if lado == "esq":
        t = np.clip(1 - np.linspace(0, 1, W) / ate, 0, 1) ** 1.3
        a = np.repeat(t[None], H, 0)
    else:
        t = np.clip(1 - np.linspace(0, 1, H) / ate, 0, 1) ** 1.3
        a = np.repeat(t[:, None], W, 1)
    vinheta = np.hypot(*np.meshgrid(np.linspace(-1, 1, W), np.linspace(-1, 1, H))) / np.sqrt(2)
    a = np.clip(a * forca + 0.35 * vinheta ** 2, 0, 0.85)
    veu = Image.new("RGBA", (W, H), (3, 5, 14, 255))
    return Image.composite(veu, img, Image.fromarray((a * 255).astype(np.uint8)))


def marca(img, altura=112, xy=(64, 50)):
    logo = Image.open(LOGO_H).convert("RGBA")
    logo = logo.crop(logo.getchannel("A").getbbox())
    logo = logo.resize((round(logo.width * altura / logo.height), altura), Image.LANCZOS)
    img.alpha_composite(logo, xy)
    return img


# ── Texto ─────────────────────────────────────────────────────────────────────
def gradiente(size, stops):
    w, h = size
    seg = np.clip(np.linspace(0, 1, w) * (len(stops) - 1), 0, len(stops) - 1 - 1e-6)
    i = seg.astype(int)
    f = (seg - i)[:, None]
    row = (np.array(stops)[i] * (1 - f) + np.array(stops)[i + 1] * f).astype(np.uint8)
    return Image.fromarray(np.repeat(row[None], h, 0), "RGB")


def linha(segs, size, fonte=BOLD, track=0):
    """Uma linha de título: [(texto, cor)] com cor em COR ou 'g' (gradiente da marca). Devolve máscara, cores,
    deslocamento do topo das maiúsculas e altura das maiúsculas."""
    font = ImageFont.truetype(fonte, size)
    full = "".join(t for t, _ in segs)
    grande = ImageFont.truetype(fonte, int(size * 1.45))           # ≠ da fonte é pequeno: desenhado maior
    lc = lambda ch: (grande if ch == "≠" else font).getlength(ch) + track
    larg = lambda s: sum(lc(ch) for ch in s)
    hb = font.getbbox("H")
    folga = 0.42 * (hb[3] - hb[1])                                   # espaço extra em volta de palavra em caixa
    raw = Image.new("L", (int(larg(full) + 2 * folga * len(segs)) + 40, int(size * 1.6)), 0)
    d = ImageDraw.Draw(raw)
    x = 20
    for t, k in segs:
        x += folga if k in CAIXA else 0
        for ch in t:
            if ch == "≠":
                nb = grande.getbbox("≠")
                d.text((x, 20 + (hb[1] + hb[3]) / 2 - (nb[1] + nb[3]) / 2), ch, font=grande, fill=255)
            else:
                d.text((x, 20), ch, font=font, fill=255)
            x += lc(ch)
        x += folga if k in CAIXA else 0
    cap_top, base = 20 + hb[1], 20 + hb[3]
    bb = raw.getbbox()
    top, bot = min(bb[1], cap_top), max(bb[3], base)
    mask = raw.crop((bb[0], top, bb[2], bot))
    cor = Image.new("RGB", mask.size, COR["w"])
    caixas = []
    x = 20
    for t, k in segs:
        f = folga if k in CAIXA else 0
        x += f
        a, b = max(0, int(x - bb[0])), min(mask.width, int(x + larg(t) - bb[0]) + 2)
        if k in CAIXA:                      # palavra dentro de caixa sólida: texto branco (M) ou escuro (C)
            caixas.append((a, b, k))
            k = "w" if k == "M" else "e"
        if b > a:
            cor.paste(gradiente((b - a, mask.height), BRAND) if k == "g" else Image.new("RGB", (b - a, mask.height), COR[k]),
                      (a, 0))
        x += larg(t) + f
    return mask, cor, cap_top - top, base - cap_top, caixas


def colar(img, mask, cor, xy, brilho=(80, 100, 255), raio=20, alfa=0.5, sombra=True):
    cheio = Image.new("L", img.size, 0)
    cheio.paste(mask, xy)
    if sombra:
        sb = cheio.filter(ImageFilter.GaussianBlur(26)).point(lambda p: int(min(255, p * 1.6)))
        img = Image.composite(Image.new("RGBA", img.size, (2, 3, 10, 255)), img, sb)
    halo = cheio.filter(ImageFilter.GaussianBlur(raio)).point(lambda p: int(p * alfa))
    img = Image.composite(Image.new("RGBA", img.size, brilho + (255,)), img, halo)
    tinta = Image.new("RGBA", img.size)
    tinta.paste(cor.convert("RGBA"), xy)
    return Image.composite(tinta, img, cheio)


def titulo(img, linhas, x, y, gap=0.36, alinhar="esq", larg_max=None):
    """linhas: [(segs, size)] ou [(segs, size, fonte, track)]. y = topo das maiúsculas da primeira linha."""
    for spec in linhas:
        segs, size = spec[0], spec[1]
        fonte = spec[2] if len(spec) > 2 else BOLD
        track = spec[3] if len(spec) > 3 else 0
        mask, cor, off, cap, caixas = linha(segs, size, fonte, track)
        if larg_max and mask.width > larg_max:
            k = larg_max / mask.width
            mask = mask.resize((larg_max, round(mask.height * k)), Image.LANCZOS)
            cor = cor.resize(mask.size, Image.LANCZOS)
            off, cap = off * k, cap * k
            caixas = [(a * k, b * k, c) for a, b, c in caixas]
        px = x if alinhar == "esq" else int(x - mask.width / 2)
        brilho = (110, 90, 255) if any(k == "g" for _, k in segs) else (70, 120, 255)
        if any(k == "m" for _, k in segs):
            brilho = (200, 60, 230)
        for a, b, c in caixas:
            pad = cap * 0.32
            forma = Image.new("L", img.size, 0)
            ImageDraw.Draw(forma).rounded_rectangle((px + a - pad, y - pad, px + b + pad, y + cap + pad),
                                                    radius=int(cap * 0.22), fill=255)
            tinta = Image.new("RGBA", img.size, CAIXA[c] + (255,))
            img = Image.composite(tinta, img, forma.filter(ImageFilter.GaussianBlur(38)).point(lambda v: int(v * 0.55)))
            img = Image.composite(tinta, img, forma)
        img = colar(img, mask, cor, (px, int(y - off)), brilho, alfa=0.2 if caixas else 0.5, sombra=not caixas)
        y += cap * (1 + gap)
    return img, y


def rotulo(img, texto, x, y, cor="c", size=44, track=10, alinhar="esq"):
    """Rótulo pequeno espaçado (como a linha de série das capas)."""
    mask, c, off, *_ = linha([(texto, cor)], size, MEDIUM, track)
    px = x if alinhar == "esq" else int(x - mask.width / 2)
    return colar(img, mask, c, (px, int(y - off)), (40, 110, 255), 8, 0.35)


# ── Desenhos (Manim) ──────────────────────────────────────────────────────────
def desenho(build, altura):
    """Renderiza mobjects em fundo transparente, recortados, com a altura pedida (px na tela 2560×1440)."""
    class Quadro(Scene):
        def construct(self):
            g = build()
            g.scale_to_fit_height(8.2)
            if g.width > 15.4:
                g.scale_to_fit_width(15.4)
            self.add(g)

    with tempconfig({"frame_width": 16, "frame_height": 9, "pixel_width": 4000, "pixel_height": 2250,
                     "transparent": True, "format": "png", "save_last_frame": True, "write_to_movie": False,
                     "media_dir": str(TMP), "verbosity": "WARNING", "disable_caching": True,
                     "output_file": "quadro"}):
        cena = Quadro()
        cena.render()
        im = Image.open(cena.renderer.file_writer.image_file_path).convert("RGBA")
    shutil.rmtree(TMP, ignore_errors=True)
    im = im.crop(im.getchannel("A").getbbox())
    return im.resize((round(im.width * altura / im.height), altura), Image.LANCZOS)


def colar_desenho(img, art, cx, cy, brilho=(70, 110, 255), alfa=0.35):
    x, y = int(cx - art.width / 2), int(cy - art.height / 2)
    cheio = Image.new("L", img.size, 0)
    cheio.paste(art.getchannel("A"), (x, y))
    halo = cheio.filter(ImageFilter.GaussianBlur(18)).point(lambda p: int(p * alfa))
    img = Image.composite(Image.new("RGBA", img.size, brilho + (255,)), img, halo)
    img.alpha_composite(art, (x, y))
    return img


def neon(m, cor, w):
    a = m.copy().set_stroke(cor, w * 3.4, 0.10)
    b = m.copy().set_stroke(cor, w * 2.0, 0.24)
    m.set_stroke(cor, w, 1)
    return VGroup(a, b, m)


def seta(p0, p1, cor=CYAN, w=11):
    p0, p1 = np.array([*p0, 0])[:3], np.array([*p1, 0])[:3]
    a = Arrow(p0, p1, buff=0, stroke_width=w, max_tip_length_to_length_ratio=0.42,
              max_stroke_width_to_length_ratio=100).set_color(cor)
    halo = a.copy().set_stroke(cor, w * 3, 0.16).set_fill(cor, 0.16)
    return VGroup(halo, a)


def carga(p=ORIGIN, r=0.14):
    p = np.array([*p, 0])[:3] if len(p) == 2 else p
    halos = [Circle(r * k).set_fill("#CFEFFF", o).set_stroke(width=0).move_to(p) for k, o in ((3.2, 0.08), (2.2, 0.16))]
    return VGroup(*halos, Dot(p, radius=r, color=WHITE))


def esfera(r=1.5, cor=BLUE):
    nucleo = [Circle(r * (1 - k / 14)).set_fill("#3D6BFF", 0.045).set_stroke(width=0) for k in range(12)]
    borda = neon(Circle(r).set_fill(cor, 0.20), BLUE_L, 6)
    equador = DashedVMobject(Ellipse(width=2 * r, height=0.5 * r), num_dashes=26).set_stroke(BLUE_L, 3, 0.55)
    return VGroup(*nucleo, borda, equador)


def tracejada(r, cor=VIOLET_L, w=7, n=30):
    return neon(DashedVMobject(Circle(r), num_dashes=n), cor, w)


def v_simetrica():
    g = VGroup(esfera(1.5), carga(), tracejada(2.25))
    for a in np.linspace(0, 2 * np.pi, 16, endpoint=False):
        u = np.array([np.cos(a), np.sin(a)])
        g.add(seta(2.45 * u, 3.55 * u))
    return g


def v_deslocada(rotulo_e=True):
    q = np.array([0.95, 0.55])
    g = VGroup(tracejada(2.3), carga(q))
    for a in np.linspace(0, 2 * np.pi, 16, endpoint=False):
        p = 2.3 * np.array([np.cos(a), np.sin(a)])
        d = p - q
        n = np.linalg.norm(d)
        comp = float(np.clip(0.35 + 1.5 * (1.0 / n) ** 2, 0.42, 2.1))
        g.add(seta(p + 0.08 * d / n, p + (0.08 + comp) * d / n, w=10))
    if rotulo_e:
        e = MathTex(r"\vec E", "=", "?", font_size=150).set_color(MAGENTA).move_to([-3.4, -2.9, 0])
        g.add(e)
    return g


def eq_gauss(size=120):
    t = MathTex(r"\oint", r"\vec E", r"\cdot d\vec A", "=", r"\frac{Q_{\mathrm{env}}}{\varepsilon_0}", font_size=size)
    t.set_color(WHITE)
    t[1].set_color(CYAN)
    return t


def v_proibido():
    t = MathTex(r"\oint \vec E\cdot d\vec A", r"\neq", r"E\oint dA", font_size=130).set_color(WHITE)
    t[0][1:3].set_color(CYAN)
    t[2][0].set_color(CYAN)
    t[1].set_color(MAGENTA)
    risco = neon(Line(t[2].get_corner(DOWN + LEFT) + [-0.15, -0.1, 0], t[2].get_corner(UP + RIGHT) + [0.15, 0.1, 0]),
                 MAGENTA, 12)
    return VGroup(t, risco)


def v_tres(vertical=False):
    # esfera concêntrica
    s = VGroup(esfera(0.85), carga(r=0.1), tracejada(1.3, w=6, n=22))
    for a in np.linspace(0, 2 * np.pi, 10, endpoint=False):
        u = np.array([np.cos(a), np.sin(a)])
        s.add(seta(1.42 * u, 2.05 * u, w=9))
    # linha infinita + cilindro coaxial
    fio = neon(Line(DOWN * 2.1, UP * 2.1), BLUE_L, 10)
    cil = VGroup(*(DashedVMobject(Ellipse(width=1.5, height=0.42), num_dashes=16).shift(UP * y) for y in (1.1, -1.1)),
                 *(DashedVMobject(Line([x, -1.1, 0], [x, 1.1, 0]), num_dashes=8) for x in (-0.75, 0.75)))
    cil = neon(cil, VIOLET_L, 6)
    li = VGroup(fio, cil)
    for y in (-0.6, 0.0, 0.6):
        for sx in (-1, 1):
            li.add(seta([sx * 0.85, y], [sx * 1.6, y], w=9))
    # plano infinito + cilindro curto
    pl = Polygon([-1.9, -0.4, 0], [1.1, -0.4, 0], [1.9, 0.4, 0], [-1.1, 0.4, 0]).set_fill(BLUE, 0.28)
    pl = neon(pl, BLUE_L, 5)
    cx = VGroup(*(DashedVMobject(Ellipse(width=0.9, height=0.26), num_dashes=12).shift(UP * y) for y in (0.75, -0.75)),
                *(DashedVMobject(Line([x, -0.75, 0], [x, 0.75, 0]), num_dashes=6) for x in (-0.45, 0.45)))
    pla = VGroup(pl, neon(cx, VIOLET_L, 6))
    for x in (-0.25, 0.25):
        pla.add(seta([x, 0.9], [x, 1.85], w=9), seta([x, -0.9], [x, -1.85], w=9))
    return VGroup(s, li, pla).arrange(DOWN if vertical else RIGHT, buff=0.7 if vertical else 1.3)


def v_cone():
    q = np.array([-3.2, -0.3, 0])
    g = VGroup()
    g.add(DashedVMobject(Circle(0.95).move_to(q), num_dashes=22).set_stroke(WHITE, 3, 0.45))
    a0, a1 = np.radians(8), np.radians(30)
    r1 = 5.2
    dirs = [np.array([np.cos(a), np.sin(a), 0]) for a in (a0, a1)]
    cone = Polygon(q, q + r1 * dirs[0], q + r1 * dirs[1]).set_fill("#B9C6FF", 0.10).set_stroke(width=0)
    g.add(cone)
    for d in dirs:
        g.add(Line(q, q + r1 * d).set_stroke(WHITE, 3, 0.7))
    patch = Line(q + 4.9 * dirs[0], q + 5.4 * dirs[1])
    g.add(neon(patch, VIOLET, 14))
    g.add(neon(Arc(radius=1.35, start_angle=a0, angle=a1 - a0, arc_center=q), AMBER, 8))
    g.add(MathTex(r"d\Omega", font_size=90, color=AMBER).move_to(q + 2.05 * np.array([np.cos(0.33), np.sin(0.33), 0])))
    g.add(carga(q, 0.13))
    g.add(MathTex(r"\oint d\Omega = 4\pi", font_size=150, color=WHITE).move_to([0.2, -2.6, 0]))
    big = g[-1]
    big[0][-2:].set_color(AMBER)
    return g


def v_bolas():
    uni = VGroup(esfera(1.5), carga(r=0.1))
    R = 1.5
    tort = VGroup(*(Circle(R * (1 - k / 11)).shift(RIGHT * R * (k / 11) * 0.95).set_fill("#5A8BFF", 0.17).set_stroke(width=0)
                    for k in range(10)))
    tort.add(neon(Circle(R).set_fill(BLUE, 0.12), BLUE_L, 6))
    return VGroup(uni, tort).arrange(RIGHT, buff=4.2)


# ── Propostas ─────────────────────────────────────────────────────────────────
def t01():
    img = escurecer(fundo())
    img = colar_desenho(img, desenho(v_simetrica, 1080), 1900, 760)
    img, _ = titulo(img, [([("NÃO É A", "w")], 190), ([("INTEGRAL.", "m")], 190), ([("É A SIMETRIA.", "g")], 190)],
                    110, 330, gap=0.42, larg_max=1340)
    return img


def t02():
    img = escurecer(fundo(), "topo", 0.55, 0.5)
    img = colar_desenho(img, desenho(v_simetrica, 800), 700, 900)
    img = colar_desenho(img, desenho(lambda: v_deslocada(False), 800), 1860, 900, (200, 70, 230), 0.25)
    img, _ = titulo(img, [([("MESMA LEI.", "w")], 170)], 1280, 210, alinhar="centro")
    img = rotulo(img, "O CAMPO SAI", 700, 1310, "c", 66, 8, "centro")
    img = rotulo(img, "O CAMPO TRAVA", 1860, 1310, "m", 66, 8, "centro")
    vs, cor, off, *_ = linha([("VS", "w")], 120)
    img = colar(img, vs, cor, (1280 - vs.width // 2, 860), (110, 90, 255))
    return img


def t03():
    img = escurecer(fundo())
    img = colar_desenho(img, desenho(v_deslocada, 1060), 1880, 780, (200, 70, 230), 0.25)
    img, _ = titulo(img, [([("A LEI DE GAUSS", "w")], 150), ([("NÃO TE DÁ", "w")], 190), ([("O CAMPO?!", "m")], 210)],
                    110, 360, gap=0.45, larg_max=1250)
    return img


def t04():
    img = escurecer(fundo(), "topo", 0.6, 0.55)
    img, y = titulo(img, [([("PARE DE ", "w"), ("DECORAR", "m")], 175), ([("GAUSSIANAS.", "g")], 210)],
                    1280, 230, gap=0.38, alinhar="centro", larg_max=2200)
    img = colar_desenho(img, desenho(v_tres, 660), 1280, 1040)
    return img


def t05():
    img = escurecer(fundo())
    img, _ = titulo(img, [([("FLUXO", "w")], 270), ([("≠ ", "m"), ("CAMPO", "c")], 270)], 110, 400, gap=0.4)
    img = colar_desenho(img, desenho(lambda: eq_gauss(130), 330), 1890, 560)
    img = colar_desenho(img, desenho(lambda: MathTex(r"\vec E", "=", "?", font_size=150).set_color(MAGENTA), 270),
                        1890, 1000, (200, 70, 230), 0.3)
    return img


def t06():
    img = escurecer(fundo())
    img = colar_desenho(img, desenho(v_cone, 1000), 1820, 760, (110, 90, 255), 0.3)
    img, _ = titulo(img, [([("DE ONDE", "w")], 200), ([("VEM O ", "w"), ("4π", "a"), ("?", "w")], 200)], 110, 430, gap=0.45)
    img = rotulo(img, "O ÂNGULO SÓLIDO EXPLICA", 116, 1010, "c", 52, 8)
    return img


def t07():
    img = escurecer(fundo())
    img = colar_desenho(img, desenho(v_simetrica, 1000), 1930, 760)
    img, _ = titulo(img, [([("SIMETRIA", "g")], 250), ([("> ", "c"), ("INTEGRAL", "w")], 250)], 110, 450, gap=0.42,
                    larg_max=1350)
    return img


def t08():
    img = escurecer(fundo())
    img = colar_desenho(img, desenho(v_simetrica, 960), 1930, 700)
    img = rotulo(img, "ELETROMAGNETISMO", 116, 330, "c", 50, 12)
    img, y = titulo(img, [([("LEI DE", "w")], 230), ([("GAUSS", "g")], 300)], 110, 450, gap=0.38)
    img, y = titulo(img, [([("O SEGREDO É A SIMETRIA", "w")], 84, MEDIUM, 4)], 116, y + 30)
    eq = desenho(lambda: eq_gauss(120), 170)
    img = colar_desenho(img, eq, 116 + eq.width // 2, int(y + 150))
    return img


def t09():
    img = escurecer(fundo(), "topo", 0.6, 0.55)
    img, _ = titulo(img, [([("ESFERA ", "w"), ("≠", "m")], 170), ([("SIMETRIA ESFÉRICA", "g")], 170)], 1280, 210,
                    gap=0.38, alinhar="centro", larg_max=2200)
    img = colar_desenho(img, desenho(v_bolas, 640), 1280, 1010)
    img = rotulo(img, "SIMETRIA ESFÉRICA", 740, 1330, "c", 56, 8, "centro")
    img = rotulo(img, "SÓ O FORMATO", 1820, 1330, "m", 56, 8, "centro")
    return img


def t10():
    img = escurecer(fundo())
    img = colar_desenho(img, desenho(lambda: v_deslocada(False), 780), 1880, 520, (200, 70, 230), 0.22)
    img = colar_desenho(img, desenho(v_proibido, 300), 1800, 1090, (200, 70, 230), 0.35)
    img, _ = titulo(img, [([("O PASSO", "w")], 210), ([("PROIBIDO", "m")], 230)], 110, 440, gap=0.42)
    img = rotulo(img, "DA LEI DE GAUSS", 116, 940, "w", 64, 10)
    return img


# ── Rodada 2: 4 hooks × (limpa, agressiva), base visual da 08 ───────────────────
def fundo_calmo(k=0.62):
    """Fundo da 08 com a galáxia e o planeta recolhidos (menos disputa com o título)."""
    a = np.asarray(fundo()).astype(np.float32)
    rgb = a[..., :3]
    rgb = (0.8 * rgb + 0.2 * rgb.mean(2, keepdims=True)) * k
    return Image.fromarray(np.dstack([rgb, a[..., 3:]]).clip(0, 255).astype(np.uint8), "RGBA")


def interrogacao(img, cx, cy, size=330):
    mask, cor, off, cap, _ = linha([("?", "m")], size)
    return colar(img, mask, cor, (int(cx - mask.width / 2), int(cy - off - cap / 2)), (200, 60, 230), 30, 0.7)


def r01():   # hook 1 · limpa
    img = escurecer(fundo_calmo())
    img = colar_desenho(img, desenho(lambda: v_deslocada(False), 960), 1900, 740, (200, 70, 230), 0.2)
    img = rotulo(img, "ELETROMAGNETISMO", 116, 330, "c", 50, 12)
    img, _ = titulo(img, [([("A LEI DE GAUSS", "w")], 150), ([("NÃO TE DÁ", "w")], 200), ([("O ", "w"), ("CAMPO?!", "m")], 230)],
                    110, 450, gap=0.42, larg_max=1300)
    return img


def r02():   # hook 1 · agressiva: funciona × trava
    img = escurecer(fundo_calmo(0.5), "topo", 0.6, 0.45)
    img, y = titulo(img, [([("A LEI DE GAUSS", "w")], 110), ([("NÃO TE DÁ O ", "w"), ("CAMPO?!", "M")], 180)],
                    1280, 150, gap=0.62, alinhar="centro", larg_max=2300)
    img = colar_desenho(img, desenho(v_simetrica, 760), 760, 1010)
    img = colar_desenho(img, desenho(lambda: v_deslocada(False), 760), 1800, 1010, (200, 70, 230), 0.22)
    img = colar_desenho(img, desenho(lambda: MathTex(r"\checkmark", color=CYAN, font_size=200), 200), 300, 700,
                        (40, 160, 255), 0.5)
    img = interrogacao(img, 2330, 760, 300)
    return img


def r03():   # hook 2 · limpa
    img = escurecer(fundo_calmo())
    img = colar_desenho(img, desenho(lambda: v_deslocada(False), 960), 1900, 740, (200, 70, 230), 0.2)
    img = rotulo(img, "LEI DE GAUSS", 116, 400, "c", 50, 12)
    img, _ = titulo(img, [([("FLUXO", "w")], 290), ([("≠ ", "m"), ("CAMPO", "w")], 290)], 110, 530, gap=0.4)
    return img


def r04():   # hook 2 · agressiva: tipografia gigante + a conta que trava
    img = escurecer(fundo_calmo(0.5), "topo", 0.5, 0.6)
    img, _ = titulo(img, [([("FLUXO ", "w"), ("≠", "m"), (" CAMPO", "w")], 330)], 1280, 300, alinhar="centro",
                    larg_max=2300)
    eq = desenho(lambda: VGroup(eq_gauss(130), MathTex(r"\Rightarrow", font_size=130, color=WHITE),
                                MathTex(r"\vec E", "=", "?", font_size=150).set_color(MAGENTA)).arrange(RIGHT, buff=0.7), 300)
    img = colar_desenho(img, eq, 1280, 1020, (150, 80, 240), 0.3)
    return img


def r05():   # hook 3 · limpa
    img = escurecer(fundo_calmo())
    img = colar_desenho(img, desenho(v_simetrica, 980), 1930, 740)
    img = rotulo(img, "LEI DE GAUSS", 116, 330, "c", 50, 12)
    img, _ = titulo(img, [([("NÃO É A INTEGRAL.", "w")], 120), ([("É A", "w")], 210), ([("SIMETRIA.", "g")], 250)],
                    110, 450, gap=0.42, larg_max=1350)
    return img


def r06():   # hook 3 · agressiva: a integral riscada é o desenho
    img = escurecer(fundo_calmo(0.5), "esq", 0.4, 0.5)

    def riscada():
        t = MathTex(r"\oint", font_size=400, color=WHITE)
        return VGroup(t, neon(Line(t.get_corner(DOWN + LEFT) + [-0.3, 0.2, 0], t.get_corner(UP + RIGHT) + [0.3, -0.2, 0]),
                              MAGENTA, 22))
    img = colar_desenho(img, desenho(riscada, 1080), 540, 760, (200, 70, 230), 0.3)
    img, _ = titulo(img, [([("NÃO É A INTEGRAL.", "w")], 120), ([("É A", "w")], 230), ([("SIMETRIA.", "g")], 300)],
                    1050, 400, gap=0.42, larg_max=1420)
    return img


def r07():   # hook 4 · limpa
    img = escurecer(fundo_calmo(), "topo", 0.6, 0.55)
    img, _ = titulo(img, [([("PARE DE ", "w"), ("DECORAR", "m")], 185), ([("GAUSSIANAS.", "w")], 185)],
                    1280, 230, gap=0.38, alinhar="centro", larg_max=2200)
    img = colar_desenho(img, desenho(v_tres, 660), 1280, 1040)
    return img


def r08():   # hook 4 · agressiva: palavra em caixa + coluna das três gaussianas
    img = escurecer(fundo_calmo(0.5))
    img = colar_desenho(img, desenho(lambda: v_tres(True), 1340), 2070, 735)
    img, _ = titulo(img, [([("PARE DE", "w")], 210), ([("DECORAR", "M")], 250), ([("GAUSSIANAS.", "w")], 170)],
                    150, 380, gap=0.62, larg_max=1400)
    return img


PROPOSTAS2 = {1: r01, 2: r02, 3: r03, 4: r04, 5: r05, 6: r06, 7: r07, 8: r08}
NOMES2 = {1: "GAUSS NÃO DÁ O CAMPO · LIMPA", 2: "GAUSS NÃO DÁ O CAMPO · AGRESSIVA", 3: "FLUXO ≠ CAMPO · LIMPA",
          4: "FLUXO ≠ CAMPO · AGRESSIVA", 5: "NÃO É A INTEGRAL · LIMPA", 6: "NÃO É A INTEGRAL · AGRESSIVA",
          7: "PARE DE DECORAR · LIMPA", 8: "PARE DE DECORAR · AGRESSIVA"}

PROPOSTAS = {1: t01, 2: t02, 3: t03, 4: t04, 5: t05, 6: t06, 7: t07, 8: t08, 9: t09, 10: t10}


def grade(arquivos, destino, nomes=None):
    """Folha de contato 2×5 com o tamanho real em que a thumb aparece na página inicial (~360 px)."""
    c, tw, th, m = 2, 760, 428, 30
    l = (len(arquivos) + c - 1) // c
    folha = Image.new("RGB", (c * tw + (c + 1) * m, l * (th + 56) + m), (14, 14, 18))
    d = ImageDraw.Draw(folha)
    f = ImageFont.truetype(MEDIUM, 30)
    for i, a in enumerate(arquivos):
        r, k = divmod(i, c)
        x, y = m + k * (tw + m), m + r * (th + 56)
        folha.paste(Image.open(a).convert("RGB").resize((tw, th), Image.LANCZOS), (x, y + 44))
        n = int(a.stem[-2:])
        d.text((x, y + 4), f"PROPOSTA {n:02d}" + (f" · {nomes[n]}" if nomes else ""), font=f, fill=(230, 232, 240))
    folha.save(destino)


def main():
    """Sem argumentos: rodada 1. `r2 [NUMEROS...]`: rodada 2 (4 hooks × limpa/agressiva)."""
    SAIDA.mkdir(exist_ok=True)
    args = sys.argv[1:]
    r2 = bool(args) and args[0] == "r2"
    props, prefixo = (PROPOSTAS2, "thumb_r2_") if r2 else (PROPOSTAS, "thumb_")
    nums = [int(a) for a in args[r2:]] or list(props)
    for n in nums:
        img = marca(props[n]())
        out = SAIDA / f"{prefixo}{n:02d}.png"
        img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(out, optimize=True)
        print(f"{out.name}: {out.stat().st_size / 1e6:.2f} MB")
    if r2:
        grade(sorted(SAIDA.glob("thumb_r2_??.png")), SAIDA / "thumbs_r2_contato.png", NOMES2)
    else:
        grade(sorted(SAIDA.glob("thumb_??.png")), SAIDA / "thumbs_contato.png")


if __name__ == "__main__":
    main()
