"""10 propostas de capa do vid_0013 com composições diferentes (título fixo: "FICA PRESA DE UM LADO / OU ATRAVESSA?").

Uso, na raiz do repositório:
    uv run python videos/vid_0013_potencial_poco_duplo/gerar_capas_variacoes.py [LETRAS]     (ex.: AEG; sem argumento: todas)

Variante local do gerar_capa.py da unidade: a identidade é a mesma (fundo cósmico e horizonte da base aprovada,
símbolo e marca do branding, Space Grotesk, degradê da marca, painel com borda luminosa), mas cada proposta
recompõe as peças em posições e hierarquias próprias. O fundo limpo vem da base da série com símbolo, título,
série, painel e marca apagados (preenchimento pelas bordas + estrelas). Artes em Manim com a paleta da cena:
violeta = potencial, magenta = barreira, azul = energia, ciano = força/movimento, partícula branca.
Saída: capas/capa_<LETRA>_<nome>.png (1080×1920) e capas/contato_variacoes_A-J.png.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(UNIT))
sys.path.insert(0, str(ROOT))
import gerar_capa as gc  # noqa: E402  (peças de arte e o compositor do vid_0009 via gc.g9)
from manim import (  # noqa: E402
    DOWN, LEFT, RIGHT, UP, Arrow, ArcBetweenPoints, CurvedArrow, DashedLine, DashedVMobject, Dot, Line, Text,
    VGroup, VMobject,
)
from template.fonts import screen_text  # noqa: E402

g9 = gc.g9
BOLD, MEDIUM = g9.BOLD, g9.MEDIUM
BRAND = g9.BRAND
SERIE = "DA EQUAÇÃO AO FENÔMENO · EP. 04"
W, H = 1080, 1920
OUT = UNIT / "capas"
CYAN, WHITE, MAGENTA = gc.CYAN, gc.WHITE, gc.MAGENTA
VIOLET_L, BLUE_L, ENERGIA = gc.VIOLET_L, gc.BLUE_L, gc.ENERGIA
ICONE = ROOT / "assets" / "branding" / "master" / "parallax_lab_icon_transparent.png"
LOGO_H = ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"
u = gc.u


# ── Fundo limpo ─────────────────────────────────────────────────────────────
# máscaras justas: símbolo, título, divisor, série, painel e marca da base (as nebulosas laterais ficam intactas)
APAGAR = ((330, 140, 750, 660), (60, 668, 1020, 1002), (220, 1000, 860, 1046), (90, 1050, 990, 1146),
          (112, 1140, 968, 1480), (270, 1568, 810, 1652))
_FUNDO = None


def fundo():
    """Base da série sem as peças de texto/marca: inpainting por difusão (suave, sem faixas) + grão + estrelas."""
    global _FUNDO
    if _FUNDO is None:
        img = Image.open(g9.BASE).convert("RGB")
        arr = np.asarray(img).astype(np.float32)
        m = Image.new("L", img.size, 0)
        for r in APAGAR:
            ImageDraw.Draw(m).rectangle(r, fill=255)
        m = m.filter(ImageFilter.MaxFilter(9))
        def difunde(k, init=None, it=400):
            """Interpolação harmônica (difusão) nas áreas mascaradas, na escala 1/k; `init` vem da escala grossa."""
            sw, sh = W // k, H // k
            sm = np.asarray(img.filter(ImageFilter.MinFilter(5)).resize((sw, sh), Image.BOX)).astype(np.float32)
            ms = np.asarray(m.resize((sw, sh), Image.BOX)) > 0
            sm[ms] = 8.0 if init is None else np.asarray(Image.fromarray(init.clip(0, 255).astype(np.uint8))
                                                         .resize((sw, sh), Image.BICUBIC)).astype(np.float32)[ms]
            for _ in range(it):
                bl = (np.roll(sm, 1, 0) + np.roll(sm, -1, 0) + np.roll(sm, 1, 1) + np.roll(sm, -1, 1)) / 4
                sm[ms] = bl[ms]
            return sm

        grosso = difunde(24, it=1500)
        fino = difunde(6, grosso, it=800)
        up = np.asarray(Image.fromarray(fino.clip(0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(np.float32)
        rng = np.random.default_rng(13)
        up += rng.normal(0, 1.8, up.shape)
        ma = np.asarray(m).astype(bool)
        ys, xs = np.nonzero(ma)
        n = len(ys) // 650
        sel = rng.integers(0, len(ys), n)
        b_ = np.clip(18 + rng.exponential(42, n), 0, 255)
        for y, x, bb in zip(ys[sel], xs[sel], b_):
            up[y, x] = np.maximum(up[y, x], [bb * 0.86, bb * 0.92, bb])
        fe = np.asarray(m.filter(ImageFilter.GaussianBlur(14))).astype(np.float32)[..., None] / 255
        res = arr * (1 - fe) + up * fe
        out = Image.fromarray(res.clip(0, 255).astype(np.uint8))
        brilho = Image.new("L", img.size, 0)
        for _ in range(9):                                      # poucas estrelas maiores, espalhadas
            j = rng.integers(0, len(ys))
            y, x = int(ys[j]), int(xs[j])
            ImageDraw.Draw(brilho).ellipse((x - 2, y - 2, x + 2, y + 2), fill=255)
        out = Image.composite(Image.new("RGB", img.size, (185, 210, 255)), out,
                              brilho.filter(ImageFilter.GaussianBlur(2.0)).point(lambda q: min(255, q * 2)))
        _FUNDO = out.convert("RGBA")
    return _FUNDO.copy()


# ── Peças de marca ──────────────────────────────────────────────────────────
def _halo(img, alpha, box, cor, raio, forca):
    full = Image.new("L", img.size, 0)
    full.paste(alpha, box)
    halo = full.filter(ImageFilter.GaussianBlur(raio)).point(lambda p: int(p * forca))
    return Image.composite(Image.new("RGBA", img.size, cor + (255,)), img, halo)


def simbolo(img, cx, cy, h):
    ic = Image.open(ICONE).convert("RGBA")
    ic = ic.crop(ic.getbbox())
    ic = ic.resize((round(ic.width * h / ic.height), h), Image.LANCZOS)
    box = (int(cx - ic.width / 2), int(cy - h / 2))
    img = _halo(img, ic.getchannel("A"), box, (70, 110, 255), 28, 0.35)
    img.alpha_composite(ic, box)
    return img


def marca(img, cy, w=470):
    """Só a palavra PARALLAX LAB do logo horizontal (o símbolo já aparece no alto)."""
    lg = Image.open(LOGO_H).convert("RGBA")
    txt = lg.crop((388, 640, lg.width, 720))                # faixa da palavra (o símbolo termina na coluna 381)
    txt = txt.crop(txt.getbbox())
    txt = txt.resize((w, round(txt.height * w / txt.width)), Image.LANCZOS)
    box = (int((W - w) / 2), int(cy - txt.height / 2))
    img = _halo(img, txt.getchannel("A"), box, (80, 120, 255), 10, 0.3)
    img.alpha_composite(txt, box)
    return img


def serie(img, cy, w=820, size=38, cx=W / 2):
    m = g9.text_mask(SERIE, ImageFont.truetype(MEDIUM, size), tracking=9)
    if m.width > w:
        m = m.resize((w, round(m.height * w / m.width)), Image.LANCZOS)
    return g9.glow_paste(img, m, (int(cx - m.width / 2), int(cy - m.height / 2)),
                         Image.new("RGB", m.size, (245, 247, 255)), (60, 120, 255), 6, 0.32)


def rotulo(img, texto, cx, cy, size=34, cor=(245, 247, 255), tracking=6, glow=(60, 120, 255)):
    m = g9.text_mask(texto, ImageFont.truetype(MEDIUM, size), tracking=tracking)
    return g9.glow_paste(img, m, (int(cx - m.width / 2), int(cy - m.height / 2)), Image.new("RGB", m.size, cor),
                         glow, 6, 0.35)


def divisor(img, cy, meia=300, cx=W / 2):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for x0, x1, c0, c1 in ((cx - meia, cx - 34, (40, 210, 255), (150, 130, 255)),
                           (cx + 34, cx + meia, (150, 130, 255), (234, 99, 255))):
        for x in range(int(x0), int(x1)):
            t = (x - x0) / (x1 - x0)
            fade = min(1.0, (x - x0) / 60, (x1 - x) / 60) if x0 < cx else min(1.0, (x1 - x) / 60, (x - x0) / 60)
            c = tuple(int(c0[k] * (1 - t) + c1[k] * t) for k in range(3))
            d.line([(x, cy), (x, cy + 2)], fill=c + (int(255 * max(0.0, fade)),))
    r, s = 22, 5
    d.polygon([(cx, cy - r), (cx + s, cy - s), (cx + r, cy), (cx + s, cy + s), (cx, cy + r), (cx - s, cy + s),
               (cx - r, cy), (cx - s, cy - s)], fill=(235, 245, 255, 255))
    img = _halo(img, lay.getchannel("A"), (0, 0), (90, 140, 255), 8, 0.6)
    img.alpha_composite(lay)
    return img


KINDS = {"white": None, "grad": BRAND, "cyan": [(0x35, 0xD9, 0xFF), (0x26, 0x7B, 0xFF)],
         "mag": [(0xC9, 0x7B, 0xFF), (0xEA, 0x63, 0xFF)]}


def titulo(img, linhas, cy, largura=900, corpo=150, gap=20, align="center", x=None):
    """Linhas de título no mesmo corpo (o maior que cabe em `largura`); cada segmento: (texto, tipo)."""
    corpo = min(g9.fit("".join(t for t, _ in ln), BOLD, largura, corpo).size for ln in linhas)
    font = ImageFont.truetype(BOLD, corpo)
    rows = []
    for ln in linhas:
        full = "".join(t for t, _ in ln)
        raw = Image.new("L", (int(font.getlength(full)) + 8, sum(font.getmetrics()) + 8), 0)
        ImageDraw.Draw(raw).text((4, 4), full, font=font, fill=255)
        box = raw.getbbox()
        mask = raw.crop(box)
        color = Image.new("RGB", mask.size, (255, 255, 255))
        xx = 4
        for t, kind in ln:
            w = font.getlength(t)
            if KINDS[kind]:
                x0, x1 = max(0, int(xx - box[0])), min(mask.width, int(xx + w - box[0]) + 2)
                if x1 > x0:
                    color.paste(g9.gradient((x1 - x0, mask.height), KINDS[kind]), (x0, 0))
            xx += w
        glow = (110, 90, 255) if any(k != "white" for _, k in ln) else (70, 140, 255)
        rows.append((mask, color, glow))
    total = sum(r[0].height for r in rows) + gap * (len(rows) - 1)
    y = cy - total / 2
    for mask, color, glow in rows:
        px = (W - mask.width) // 2 if align == "center" else int(x)
        img = g9.glow_paste(img, mask, (px, int(y)), color, glow, 15, 0.5)
        y += mask.height + gap
    return img


def painel(img, box, raio=40):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    uu = np.linspace(0, 1, w)[None, :, None]
    vv = np.linspace(0, 1, h)[:, None, None]
    tl, tr, bl, br = (np.array(c, np.float32) for c in ((16, 30, 92), (34, 22, 96), (20, 36, 120), (64, 24, 120)))
    inter = ((1 - vv) * ((1 - uu) * tl + uu * tr) + vv * ((1 - uu) * bl + uu * br)).clip(0, 255).astype(np.uint8)
    forma = Image.new("L", img.size, 0)
    ImageDraw.Draw(forma).rounded_rectangle(box, raio, fill=228)
    cheio = Image.new("RGBA", img.size)
    cheio.paste(Image.fromarray(inter).convert("RGBA"), (x0, y0))
    img = Image.composite(cheio, img, forma)
    borda = Image.new("L", img.size, 0)
    ImageDraw.Draw(borda).rounded_rectangle(box, raio, outline=255, width=4)
    cores = Image.new("RGBA", img.size)
    cores.paste(g9.gradient((w, h), [(225, 242, 255), (130, 190, 255), (205, 95, 235)]).convert("RGBA"), (x0, y0))
    img = Image.composite(cores, img, borda.filter(ImageFilter.GaussianBlur(9)).point(lambda p: int(p * 0.55)))
    return Image.composite(cores, img, borda)


def arte(img, build, cx, cy, maxw, maxh, halo=0.3, resolucao=900):
    art = g9.render_rgba(lambda: build().center(), resolucao)    # o compositor escala sem recentrar
    k = min(maxw / art.width, maxh / art.height)
    art = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)
    box = (int(cx - art.width / 2), int(cy - art.height / 2))
    if halo:
        img = _halo(img, art.getchannel("A"), box, (90, 110, 255), 10, halo)
    img.alpha_composite(art, box)
    return img


# ── Peças de arte (Manim) ───────────────────────────────────────────────────
neon = gc.neon


def curva(sx, sy, x0=-1.6, x1=1.6, w=10, barreira=True, cor=VIOLET_L, op=1.0, topo=0.42):
    """U(x) em violeta; o topo da barreira (|x| < `topo` ℓ) em magenta, com brilho próprio."""
    pts = lambda a, b, n: [np.array([sx * x, sy * u(x), 0.0]) for x in np.linspace(a, b, n)]
    g = VGroup(neon(VMobject().set_points_smoothly(pts(x0, x1, 160)), cor, w))
    if barreira and x0 < -topo and x1 > topo:
        g.add(neon(VMobject().set_points_smoothly(pts(-topo, topo, 40)), MAGENTA, w * 1.15))
    if op < 1:
        g.set_opacity(op)
    return g


def particula(p, r=0.14):
    p = np.array([p[0], p[1], 0.0])
    return VGroup(Dot(p, r * 2.6, color=WHITE).set_opacity(0.12), Dot(p, r * 1.7, color=WHITE).set_opacity(0.25),
                  Dot(p, r, color=WHITE))


def seta_arco(a, b, ang, cor=CYAN, w=8, tip=0.28, tracejada=False):
    if tracejada:
        arco = DashedVMobject(ArcBetweenPoints(np.array([*a, 0]), np.array([*b, 0]), angle=ang), num_dashes=14)
        return neon(arco, cor, w)
    s = CurvedArrow(np.array([*a, 0]), np.array([*b, 0]), angle=ang, color=cor, stroke_width=w, tip_length=tip)
    return VGroup(s.copy().set_stroke(cor, w * 2.6, 0.22), s)


def seta_reta(a, b, cor=WHITE, w=8, tip=0.26, duas=False):
    s = Arrow(np.array([*a, 0]), np.array([*b, 0]), buff=0, stroke_width=w, tip_length=tip, color=cor,
              max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=60)
    g = VGroup(s.copy().set_stroke(cor, w * 2.6, 0.22), s)
    if duas:
        t = Arrow(np.array([*b, 0]), np.array([*a, 0]), buff=0, stroke_width=w, tip_length=tip, color=cor,
                  max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=60)
        g.add(t)
    return g


def interrogacao(p, escala=1.0, cor=WHITE):
    return Text("?", font="Arial", weight="BOLD", color=cor).scale(escala).move_to(np.array([*p, 0]))


def nivel(sx, sy, E, x0=-1.75, x1=1.75, cor=ENERGIA, w=6, op=1.0):
    return neon(Line([sx * x0, sy * E, 0], [sx * x1, sy * E, 0]), cor, w).set_opacity(op)


def eixo_x(sx, y, x0=-1.6, x1=1.6, marcas=True):
    g = VGroup(Arrow([sx * x0 - 0.1, y, 0], [sx * x1 + 0.35, y, 0], buff=0, stroke_width=5, tip_length=0.2,
                     color=WHITE).set_opacity(0.75))
    if marcas:
        for x in (-1, 0, 1):
            g.add(Line([sx * x, y - 0.09, 0], [sx * x, y + 0.09, 0]).set_stroke(MAGENTA if x == 0 else VIOLET_L, 5))
    return g


def regiao(sx, y, a, b):
    return neon(Line([sx * a, y, 0], [sx * b, y, 0]), ENERGIA, 9)


# ── Artes das propostas ─────────────────────────────────────────────────────
def arte_A():
    sx, sy = 2.0, 1.25
    g = VGroup(curva(sx, sy, w=12), particula((-sx, 0.2), 0.17))
    g.add(seta_arco((-sx + 0.15, 0.55), (sx - 0.15, 0.55), -np.pi * 0.75, CYAN, 9, 0.32))
    g.add(interrogacao((0, sy + 1.05), 1.35))
    return g


def arte_A2(q=1.35, yp=0.2):
    """V2 da A: barreira magenta curta, só no topo; a seta passa rente ao topo e termina logo depois dele;
    o "?" fica logo acima do topo (a pergunta é sobre aquela barreira, sem mostrar a resposta)."""
    sx, sy = 2.0, 1.25
    g = VGroup(curva(sx, sy, w=12, topo=0.22), particula((-sx, yp), 0.17))
    g.add(seta_arco((-sx + 0.15, 0.55), (0.62 * sx, sy * u(0.62) + 0.42), -np.pi * 0.62, CYAN, 9, 0.32))
    g.add(interrogacao((0.0, sy + 0.84 - (1.35 - q) * 0.25), q))
    return g


def arte_B():
    sx, sy, E = 1.7, 1.15, 0.55
    a, b = np.sqrt(1 - np.sqrt(E)), np.sqrt(1 + np.sqrt(E))
    ub = DashedLine([-sx * 1.75, sy, 0], [sx * 1.75, sy, 0], dash_length=0.14).set_stroke(MAGENTA, 6)
    y = -0.85
    g = VGroup(nivel(sx, sy, E), ub, curva(sx, sy, w=11), eixo_x(sx, y), regiao(sx, y, -b, -a), regiao(sx, y, a, b),
               particula((-sx * 1.05, y), 0.15))
    return g


def arte_heroi_B():
    f = gc.tx(r"E\ ?\ U_b", 150)
    f[0][0].set_color(BLUE_L)
    f[0][2:].set_color(MAGENTA)
    return f


def arte_C(acima):
    sx, sy = 1.35, 1.0
    y = -0.8
    if not acima:
        E = 0.5
        a, b = np.sqrt(1 - np.sqrt(E)), np.sqrt(1 + np.sqrt(E))
        g = VGroup(nivel(sx, sy, E), curva(sx, sy, w=10), eixo_x(sx, y), regiao(sx, y, -b, -a),
                   regiao(sx, y, a, b).set_opacity(0.3), particula((-sx * 1.0, y), 0.14))
        g.add(seta_reta((-sx * b + 0.1, y - 0.45), (-sx * a - 0.1, y - 0.45), WHITE, 7, 0.22, duas=True))
    else:
        E = 1.5
        b = np.sqrt(1 + np.sqrt(E))
        g = VGroup(nivel(sx, sy, E), curva(sx, sy, w=10), eixo_x(sx, y), regiao(sx, y, -b, b),
                   particula((-sx * 0.75, y), 0.14))
        g.add(seta_reta((-sx * 0.75, y - 0.45), (sx * 1.0, y - 0.45), CYAN, 8, 0.26))
    return g


def arte_D():
    """Paisagem de energia estilizada (relevo em linhas de grade): analogia visual, não terreno real."""
    sx, sy = 2.7, 1.45
    xs = np.linspace(-1.62, 1.62, 160)
    base_y = -1.25
    g = VGroup()
    for k in range(1, 8):                                    # curvas de nível do "relevo"
        f = 1 - k / 8
        pts = [np.array([sx * x, base_y + (sy * u(x) - base_y) * f, 0.0]) for x in xs]
        g.add(VMobject().set_points_smoothly(pts).set_stroke(VIOLET_L, 3, 0.55 * f + 0.08))
    for x in np.linspace(-1.6, 1.6, 23):                    # meridianos
        g.add(Line([sx * x, base_y, 0], [sx * x, sy * u(x), 0]).set_stroke(BLUE_L, 2, 0.22))
    g.add(curva(sx, sy, -1.62, 1.62, w=13))
    g.add(particula((-sx, 0.27), 0.24))
    g.add(seta_arco((-sx + 0.1, 0.75), (sx - 0.25, 0.75), -np.pi * 0.72, CYAN, 10, 0.36))
    return g


def arte_E():
    """Close: mínimo esquerdo, topo e começo do vale direito; tentativa tracejada que não chega ao topo."""
    sx, sy = 3.0, 2.1
    g = VGroup(curva(sx, sy, -1.32, 0.62, w=16))
    g.add(particula((-sx, 0.36), 0.3))
    tent = DashedVMobject(ArcBetweenPoints(np.array([-sx + 0.45, 0.85, 0]), np.array([-0.55, sy + 0.25, 0]),
                                           angle=-np.pi * 0.32), num_dashes=11)
    g.add(neon(tent, CYAN, 9))
    g.add(interrogacao((0.0, sy + 1.05), 1.9, WHITE))
    return g


def arte_F():
    sx, sy, E = 1.9, 1.15, 0.5
    a, b = np.sqrt(1 - np.sqrt(E)), np.sqrt(1 + np.sqrt(E))
    y, xp = -1.0, 1.15
    g = VGroup(nivel(sx, sy, E), curva(sx, sy, w=11), eixo_x(sx, y), regiao(sx, y, -b, -a), regiao(sx, y, a, b))
    for xr in (-b, -a, a, b):
        g.add(DashedLine([sx * xr, sy * E, 0], [sx * xr, y + 0.08, 0], dash_length=0.08).set_stroke(BLUE_L, 3, 0.5))
        g.add(Dot([sx * xr, sy * E, 0], 0.09, color=BLUE_L))
    g.add(DashedLine([sx * xp, y + 0.2, 0], [sx * xp, sy * u(xp), 0], dash_length=0.1).set_stroke(WHITE, 4, 0.8))
    g.add(Dot([sx * xp, sy * u(xp), 0], 0.12, color=VIOLET_L).set_stroke(WHITE, 3),
          particula((sx * xp, y), 0.17))
    return g


def arte_G():
    sx, sy = 2.0, 1.25
    g = VGroup(curva(sx, sy, w=14), particula((-sx, 0.22), 0.2))
    g.add(seta_arco((-sx + 0.2, 0.6), (sx - 0.2, 0.6), -np.pi * 0.72, CYAN, 10, 0.34))
    return g


def arte_H_fundo():
    sx, sy, E = 2.0, 1.2, 0.55
    return VGroup(nivel(sx, sy, E, w=7, op=0.85), curva(sx, sy, w=11))


def arte_H_heroi():
    return gc.ule(170)


def arte_I():
    fx = VMobject().set_points_smoothly([[1.2 * x, 1.05 * (x - x ** 3), 0] for x in np.linspace(-1.45, 1.45, 100)])
    fg = VGroup(Line([-1.95, 0, 0], [1.95, 0, 0]).set_stroke(WHITE, 4, 0.35), neon(fx, CYAN, 11))
    fl = gc.tx(r"F(x)", 96, CYAN).next_to(fg, DOWN, buff=0.4)
    sx, sy = 1.2, 0.95
    ug = VGroup(curva(sx, sy, w=11), eixo_x(sx, -0.6, marcas=False), particula((-sx * 1.05, -0.6), 0.13))
    ul = gc.tx(r"U(x)", 96, VIOLET_L).next_to(ug, DOWN, buff=0.3)
    seta = seta_reta((0, 0), (1.5, 0), WHITE, 10, 0.34)
    return VGroup(VGroup(fg, fl), seta, VGroup(ug, ul)).arrange(RIGHT, buff=0.55)


def arte_J():
    sx, sy = 1.85, 1.15
    g = VGroup(*(nivel(sx, sy, E, w=5, op=0.9) for E in (0.5, 1.0, 1.5)), curva(sx, sy, w=11))
    a, b = np.sqrt(1 - np.sqrt(0.5)), np.sqrt(1 + np.sqrt(0.5))
    g.add(seta_reta((sx * a + 0.12, sy * 0.5 + 0.3), (sx * b - 0.12, sy * 0.5 + 0.3), WHITE, 6, 0.18, duas=True))
    for k, x in enumerate((1.0, 0.62, 0.38, 0.22)):          # separatriz: passos cada vez menores rumo ao topo
        g.add(Dot([sx * x, sy * 1.0 + 0.28, 0], 0.09 - 0.012 * k, color=WHITE).set_opacity(1 - 0.18 * k))
    g.add(seta_reta((-sx * 1.4, sy * 1.5 + 0.3), (sx * 1.4, sy * 1.5 + 0.3), CYAN, 8, 0.26))
    for E, s in ((0.5, "preso"), (1.0, "separatriz"), (1.5, "atravessa")):
        t = screen_text(s, 44).set_color(BLUE_L if E != 1.5 else CYAN)
        g.add(t.next_to([sx * 1.75, sy * E, 0], RIGHT, buff=0.22))
    return g


# ── Composições ─────────────────────────────────────────────────────────────
T2 = [[("FICA PRESA DE UM LADO", "white")], [("OU ATRAVESSA?", "grad")]]
T3 = [[("FICA PRESA", "white")], [("DE UM LADO", "white")], [("OU ATRAVESSA?", "grad")]]


def capa_A():                       # título na metade superior; arte grande sem painel
    img = simbolo(fundo(), W / 2, 215, 230)
    img = titulo(img, T3, 560, 900, 150)
    img = divisor(img, 790)
    img = serie(img, 845)
    img = arte(img, arte_A, W / 2, 1230, 1000, 600)
    return marca(img, 1610)


def capa_A2(q=1.35, yp=0.2):        # V2 da A (mesma composição; barreira, seta e "?" refinados)
    img = simbolo(fundo(), W / 2, 215, 230)
    img = titulo(img, T3, 560, 900, 150)
    img = divisor(img, 790)
    img = serie(img, 845)
    img = arte(img, lambda: arte_A2(q, yp), W / 2, 1230, 1000, 600)
    return marca(img, 1610)


def capa_B():                       # painel grande: gráfico + E ? U_b como comparação
    img = simbolo(fundo(), W / 2, 200, 200)
    img = titulo(img, T2, 470, 940, 130)
    img = divisor(img, 625)
    img = serie(img, 680)
    img = painel(img, (50, 770, 1030, 1470))
    img = arte(img, arte_heroi_B, W / 2, 900, 470, 170, halo=0.3)     # a comparação em cima, grande
    img = arte(img, arte_B, W / 2, 1230, 820, 380, halo=0.2)
    return marca(img, 1600)


def capa_C():                       # split: PRESA × ATRAVESSA em dois painéis
    img = simbolo(fundo(), W / 2, 190, 190)
    t = [[("FICA ", "white"), ("PRESA", "mag"), (" DE UM LADO", "white")], [("OU ", "white"), ("ATRAVESSA?", "cyan")]]
    img = titulo(img, t, 440, 940, 130)
    img = serie(img, 600)
    img = painel(img, (40, 690, 530, 1470), 34)
    img = painel(img, (550, 690, 1040, 1470), 34)
    img = titulo_curto(img, "PRESA", 285, 785, KINDS["mag"])
    img = titulo_curto(img, "ATRAVESSA", 795, 785, KINDS["cyan"])
    img = arte(img, lambda: arte_C(False), 285, 1130, 430, 560, halo=0.2)
    img = arte(img, lambda: arte_C(True), 795, 1130, 430, 560, halo=0.2)
    return marca(img, 1600)


def titulo_curto(img, texto, cx, cy, stops, corpo=62):
    font = ImageFont.truetype(BOLD, corpo)
    raw = Image.new("L", (int(font.getlength(texto)) + 8, sum(font.getmetrics()) + 8), 0)
    ImageDraw.Draw(raw).text((4, 4), texto, font=font, fill=255)
    mask = raw.crop(raw.getbbox())
    return g9.glow_paste(img, mask, (int(cx - mask.width / 2), int(cy - mask.height / 2)),
                         g9.gradient(mask.size, stops), (110, 90, 255), 12, 0.45)


def capa_D():                       # paisagem estilizada ocupando a largura toda; sem fórmulas
    img = simbolo(fundo(), 150, 170, 150)
    img = serie(img, 172, w=560, size=30, cx=630)
    t = [[("FICA PRESA DE UM LADO", "white")], [("OU ATRAVESSA?", "grad")]]
    img = titulo(img, t, 430, 960, 140)
    img = arte(img, arte_D, W / 2, 1060, 1080, 720, halo=0.25)
    img = rotulo(img, "PAISAGEM DE ENERGIA · ANALOGIA", W / 2, 1470, 26, (190, 205, 255), 7)
    return marca(img, 1605)


def capa_E():                       # close na barreira; título embaixo
    img = simbolo(fundo(), W / 2, 185, 180)
    img = arte(img, arte_E, W / 2, 720, 1040, 760, halo=0.3)
    img = titulo(img, T3, 1265, 880, 140)
    img = divisor(img, 1475)
    img = serie(img, 1525)
    return marca(img, 1620)


def capa_F():                       # eixo espacial + U(x) acima: o gráfico decide onde a partícula pode ir
    img = simbolo(fundo(), W / 2, 200, 200)
    img = titulo(img, T2, 470, 940, 130)
    img = divisor(img, 620)
    img = serie(img, 675)
    img = arte(img, arte_F, W / 2, 1120, 980, 680)
    return marca(img, 1610)


def capa_G():                       # minimalista: título muito grande + silhueta
    img = simbolo(fundo(), W / 2, 180, 170)
    t = [[("FICA PRESA", "white")], [("DE UM LADO", "white")], [("OU", "white")], [("ATRAVESSA?", "grad")]]
    img = titulo(img, t, 680, 990, 220, gap=18)
    img = arte(img, arte_G, W / 2, 1290, 860, 380, halo=0.3)
    return marca(img, 1610)


def capa_H():                       # U(x) ≤ E como herói
    img = simbolo(fundo(), W / 2, 185, 170)
    img = titulo(img, T2, 430, 900, 115)
    img = serie(img, 575)
    img = arte(img, arte_H_fundo, W / 2, 1245, 960, 440, halo=0.15)
    img = painel(img, (130, 690, 950, 1000), 40)
    img = arte(img, arte_H_heroi, W / 2, 845, 700, 230, halo=0.35)
    return marca(img, 1610)


def capa_I():                       # força virando potencial, painel largo
    img = simbolo(fundo(), W / 2, 200, 200)
    img = titulo(img, T2, 470, 940, 130)
    img = divisor(img, 620)
    img = serie(img, 675)
    img = painel(img, (40, 790, 1040, 1420))
    img = arte(img, arte_I, W / 2, 1105, 920, 540, halo=0.2)
    return marca(img, 1600)


def capa_J():                       # três energias, um mesmo potencial
    img = simbolo(fundo(), W / 2, 190, 180)
    t = [[("FICA PRESA", "white")], [("DE UM LADO OU", "white")], [("ATRAVESSA?", "grad")]]
    img = titulo(img, t, 520, 860, 140)
    img = serie(img, 770)
    img = arte(img, arte_J, W / 2, 1160, 930, 620)
    return marca(img, 1610)


CAPAS = {"A": ("barreira", capa_A), "B": ("energia_barreira", capa_B), "C": ("presa_atravessa", capa_C),
         "D": ("paisagem", capa_D), "E": ("close_barreira", capa_E), "F": ("eixo_potencial", capa_F),
         "G": ("minimalista", capa_G), "H": ("U_menor_E", capa_H), "I": ("forca_potencial", capa_I),
         "J": ("tres_energias", capa_J)}


def contato(arqs, saida):
    ims = [Image.open(a).convert("RGB") for a in arqs]
    tw, th = 432, 768
    folha = Image.new("RGB", (tw * 5 + 6 * 12, th * 2 + 3 * 12 + 2 * 40), (12, 14, 24))
    d = ImageDraw.Draw(folha)
    f = ImageFont.truetype(BOLD, 30)
    for i, (im, a) in enumerate(zip(ims, arqs)):
        x, y = 12 + (i % 5) * (tw + 12), 12 + (i // 5) * (th + 52)
        d.text((x, y), Path(a).stem.replace("capa_", ""), font=f, fill=(220, 230, 255))
        folha.paste(im.resize((tw, th), Image.LANCZOS), (x, y + 40))
    folha.save(saida, optimize=True)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] in ("A2", "A3"):
        # A3: microajustes opcionais sobre a V2 aprovada ("?" ~13% menor; partícula mais apoiada na curva)
        alvo = OUT / ("capa_A_barreira_v2.png" if sys.argv[1] == "A2" else "capa_A_barreira_v2b.png")
        (capa_A2() if sys.argv[1] == "A2" else capa_A2(q=1.17, yp=0.3)).convert("RGB").save(alvo, optimize=True)
        print(alvo)
        sys.exit()
    letras = sys.argv[1] if len(sys.argv) > 1 else "ABCDEFGHIJ"
    if letras == "fundo":
        fundo().convert("RGB").save(OUT / "_fundo_limpo.png")
        sys.exit()
    for L in letras:
        nome, fn = CAPAS[L]
        alvo = OUT / f"capa_{L}_{nome}.png"
        img = fn().convert("RGB")
        assert img.size == (W, H)
        img.save(alvo, optimize=True)
        print(alvo)
    arqs = [OUT / f"capa_{L}_{n}.png" for L, (n, _) in CAPAS.items()]
    if all(a.exists() for a in arqs):
        contato(arqs, OUT / "contato_variacoes_A-J.png")
        print(OUT / "contato_variacoes_A-J.png")
