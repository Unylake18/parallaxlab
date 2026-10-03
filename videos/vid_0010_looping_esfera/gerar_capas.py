"""Seis propostas de capa vertical do vid_0010 (EXERCÍCIO RESOLVIDO · EP. 04), 1080×1920.

Uso, na raiz do repositório:
    uv run python videos/vid_0010_looping_esfera/gerar_capas.py [PASTA_SAIDA]

Mesmo layout do último Exercício Resolvido (vid_0007, EP. 03): base versionada
videos/vid_0002_integral_substituicao/capa_instagram.png, da qual se apagam título, linha de série e
interior do painel; fundo, símbolo, divisor, borda do painel, marca e horizonte são preservados.
Headline em 2–3 linhas (a última em gradiente), linha de série abaixo do divisor e a ilustração dentro
do painel original (600×215).

As ilustrações são desenhadas em Pillow (supersampling) com a geometria da cena: trajetória do CM de raio
R, pista física R + a, rampa y = 1,4(√(u²+1,7²) − 1,7). Fontes: Space Grotesk e Inter, versionadas.
Cada proposta testa uma ideia editorial diferente; nenhuma é eleita aqui.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(ROOT))
from template.fonts import INTER, SPACE_GROTESK  # noqa: E402

BASE = UNIT.parent / "vid_0002_integral_substituicao" / "capa_instagram.png"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capas"
BOLD, MEDIUM = str(SPACE_GROTESK["bold"]), str(SPACE_GROTESK["medium"])
BRAND = [(0x35, 0xD9, 0xFF), (0x26, 0x7B, 0xFF), (0x74, 0x5C, 0xFF), (0xEA, 0x63, 0xFF)]
CY, BL, VI, MG, WH = "#35D9FF", "#267BFF", "#745CFF", "#EA63FF", "#F5F7FF"
SERIE = "EXERCÍCIO RESOLVIDO · EP. 04"

S = 3                                  # supersampling das ilustrações
PW, PH = 780, 275                      # área útil do painel (px finais)
A_R = 0.14                             # a/R nas capas (esfera um pouco maior que no vídeo, para leitura)
M_SL, C_SL = 1.4, 1.7                  # mesma rampa da cena


def rgb(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def fnt(kind, size):
    path = {"bold": SPACE_GROTESK["bold"], "medium": SPACE_GROTESK["medium"],
            "inter": INTER["semibold"], "interb": INTER["bold"]}[kind]
    return ImageFont.truetype(str(path), round(size * S))


# ── Ilustração do painel ─────────────────────────────────────────────────────
class Cena:
    """Tela transparente PW×PH (coordenadas lógicas), desenhada com supersampling S."""

    def __init__(self):
        self.img = Image.new("RGBA", (PW * S, PH * S), (0, 0, 0, 0))

    def camada(self):
        return Image.new("RGBA", self.img.size, (0, 0, 0, 0))

    def cola(self, camada, brilho=0, ganho=0.9):
        if brilho:
            g = camada.filter(ImageFilter.GaussianBlur(brilho * S))
            g.putalpha(g.getchannel("A").point(lambda v: min(255, int(v * ganho))))
            self.img.alpha_composite(g)
        self.img.alpha_composite(camada)

    def linha(self, pts, cor, larg, brilho=5, alfa=255, ponta=True):
        c = self.camada()
        d = ImageDraw.Draw(c)
        p = [(x * S, y * S) for x, y in pts]
        col = rgb(cor) + (alfa,)
        d.line(p, fill=col, width=round(larg * S), joint="curve")
        if ponta:
            r = larg * S / 2
            for x, y in (p[0], p[-1]):
                d.ellipse((x - r, y - r, x + r, y + r), fill=col)
        self.cola(c, brilho)

    def tracejada(self, a, b, cor, larg=2.5, tra=11, vao=8, alfa=210, brilho=2):
        (x0, y0), (x1, y1) = a, b
        L = float(np.hypot(x1 - x0, y1 - y0))
        n = max(1, int(L // (tra + vao)))
        c = self.camada()
        d = ImageDraw.Draw(c)
        for i in range(n + 1):
            t0 = i * (tra + vao) / L
            t1 = min(1.0, t0 + tra / L)
            if t0 >= 1:
                break
            d.line([((x0 + (x1 - x0) * t0) * S, (y0 + (y1 - y0) * t0) * S),
                    ((x0 + (x1 - x0) * t1) * S, (y0 + (y1 - y0) * t1) * S)],
                   fill=rgb(cor) + (alfa,), width=round(larg * S))
        self.cola(c, brilho, 0.6)

    def seta(self, a, b, cor, larg=5, cabeca=16, brilho=5, dupla=False):
        (x0, y0), (x1, y1) = a, b
        ang = np.arctan2(y1 - y0, x1 - x0)

        def ponta(x, y, ang_):
            return [(x, y), (x - cabeca * np.cos(ang_ - 0.45), y - cabeca * np.sin(ang_ - 0.45)),
                    (x - cabeca * np.cos(ang_ + 0.45), y - cabeca * np.sin(ang_ + 0.45))]

        rec = cabeca * 0.7
        ini = (x0 + (rec * np.cos(ang) if dupla else 0), y0 + (rec * np.sin(ang) if dupla else 0))
        fim = (x1 - rec * np.cos(ang), y1 - rec * np.sin(ang))
        c = self.camada()
        d = ImageDraw.Draw(c)
        col = rgb(cor) + (255,)
        d.line([(ini[0] * S, ini[1] * S), (fim[0] * S, fim[1] * S)], fill=col, width=round(larg * S))
        d.polygon([(x * S, y * S) for x, y in ponta(x1, y1, ang)], fill=col)
        if dupla:
            d.polygon([(x * S, y * S) for x, y in ponta(x0, y0, ang + np.pi)], fill=col)
        self.cola(c, brilho)

    def arco_seta(self, centro, r, ang0, ang1, cor, larg=5, cabeca=16, brilho=5):
        t = np.radians(np.linspace(ang0, ang1, 60))
        pts = [(centro[0] + r * np.cos(a), centro[1] + r * np.sin(a)) for a in t]
        self.linha(pts, cor, larg, brilho)
        (xa, ya), (xb, yb) = pts[-2], pts[-1]
        ang = np.arctan2(yb - ya, xb - xa)
        c = self.camada()
        d = ImageDraw.Draw(c)
        pt = [(xb, yb), (xb - cabeca * np.cos(ang - 0.5), yb - cabeca * np.sin(ang - 0.5)),
              (xb - cabeca * np.cos(ang + 0.5), yb - cabeca * np.sin(ang + 0.5))]
        d.polygon([(x * S, y * S) for x, y in pt], fill=rgb(cor) + (255,))
        self.cola(c, brilho)

    def esfera(self, cx, cy, r, marca=-40, cor_marca=MG, brilho=7):
        n = round(2 * r * S) + 4
        yy, xx = np.mgrid[0:n, 0:n]
        u = (xx - n / 2) / (r * S)
        v = (yy - n / 2) / (r * S)
        rho = np.hypot(u, v)
        luz = np.clip(1 - np.hypot(u + 0.35, v + 0.40) / 1.35, 0, 1)
        interior = np.zeros((n, n, 4), float)
        c0, c1 = np.array([8, 18, 70]), np.array([88, 168, 255])
        interior[..., :3] = c0 + (c1 - c0) * luz[..., None] ** 1.3
        interior[..., 3] = np.where(rho <= 1.0, 255, 0)
        im = Image.fromarray(interior.astype("uint8"), "RGBA")
        c = self.camada()
        c.alpha_composite(im, (round((cx - r) * S) - 2, round((cy - r) * S) - 2))
        d = ImageDraw.Draw(c)
        d.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), outline=rgb(CY) + (255,),
                  width=max(2, round(r * 0.08 * S)))
        a = np.radians(marca)
        d.line([(cx * S, cy * S), ((cx + 0.93 * r * np.cos(a)) * S, (cy + 0.93 * r * np.sin(a)) * S)],
               fill=rgb(cor_marca) + (255,), width=max(3, round(r * 0.14 * S)))
        d.ellipse(((cx - r * 0.1) * S, (cy - r * 0.1) * S, (cx + r * 0.1) * S, (cy + r * 0.1) * S),
                  fill=rgb(WH) + (255,))
        self.cola(c, brilho, 0.8)

    def particula(self, cx, cy, r=6, cor=WH, brilho=7):
        c = self.camada()
        d = ImageDraw.Draw(c)
        d.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), fill=rgb(cor) + (255,))
        self.cola(c, brilho, 1.0)

    def texto(self, xy, s, fonte, cor=WH, alfa=255, trilha=0, ancora="mm", brilho=0):
        c = self.camada()
        d = ImageDraw.Draw(c)
        larg = (sum(d.textlength(ch, font=fonte) + trilha * S for ch in s) - trilha * S) if trilha \
            else d.textlength(s, font=fonte)
        x = xy[0] * S - (larg / 2 if ancora[0] == "m" else (larg if ancora[0] == "r" else 0))
        y = xy[1] * S
        if trilha:
            for ch in s:
                d.text((x, y), ch, font=fonte, fill=rgb(cor) + (alfa,), anchor="lm")
                x += d.textlength(ch, font=fonte) + trilha * S
        else:
            d.text((x, y), s, font=fonte, fill=rgb(cor) + (alfa,), anchor="lm")
        self.cola(c, brilho, 0.7)
        return larg / S

    def texto_grad(self, xy, s, fonte, ancora="mm", brilho=7, cores=BRAND):
        mask = Image.new("L", self.img.size, 0)
        d = ImageDraw.Draw(mask)
        larg = d.textlength(s, font=fonte)
        x = xy[0] * S - (larg / 2 if ancora[0] == "m" else (larg if ancora[0] == "r" else 0))
        d.text((x, xy[1] * S), s, font=fonte, fill=255, anchor="lm")
        gx = np.linspace(0, 1, self.img.size[0])
        t = np.clip((gx - x / self.img.size[0]) / max(1e-6, larg / self.img.size[0]), 0, 1)
        stops = np.linspace(0, 1, len(cores))
        linha = np.stack([np.interp(t, stops, [c[i] for c in cores]) for i in range(3)], -1)
        grad = np.broadcast_to(linha[None], (self.img.size[1], self.img.size[0], 3)).astype("uint8")
        c = Image.fromarray(grad, "RGB").convert("RGBA")
        c.putalpha(mask)
        self.cola(c, brilho, 0.55)
        return larg / S

    def arte(self):
        return self.img.resize((PW, PH), Image.LANCZOS)


# ── Geometria da cena ────────────────────────────────────────────────────────
def f_ramp(u):
    return M_SL * (np.sqrt(u * u + C_SL ** 2) - C_SL)


def u_de_H(Hh):
    return float(np.sqrt((Hh / M_SL + C_SL) ** 2 - C_SL ** 2))


class Pista:
    """Trajetória do CM de raio 1 (R) e pista física R + a; k = pixels por R; (ox, oy) = ponto mais baixo do CM."""

    def __init__(self, k, ox, oy, a=A_R):
        self.k, self.ox, self.oy, self.a = k, ox, oy, a

    def p(self, x, y):
        return (self.ox + self.k * x, self.oy - self.k * y)

    def pontos(self, Hh=None, cauda=1.4):
        d = self.a
        pts = []
        if Hh:
            for uu in np.linspace(u_de_H(Hh), 0, 80):
                x, y = -uu, f_ramp(uu)
                g = M_SL * uu / np.sqrt(uu * uu + C_SL ** 2)
                n = np.hypot(1, g)
                pts.append(self.p(x + d * (-g / n), y - d * (1 / n)))
        pts += [self.p((1 + d) * np.sin(t), 1 - (1 + d) * np.cos(t)) for t in np.linspace(0, 2 * np.pi, 120)]
        pts += [self.p(cauda, -d)]
        return pts

    def pos_rampa(self, Hh):
        return self.p(-u_de_H(Hh), Hh)

    def pos_loop(self, th):
        return self.p(np.sin(th), 1 - np.cos(th))


def pista_desenho(c, pista, Hh=None, cauda=1.4, larg=5, alfa=255, brilho=7):
    c.linha(pista.pontos(Hh, cauda), BL, larg, brilho, alfa)


def dimensao_v(c, x, y_alto, y_baixo, cor=VI, larg=3):
    c.seta((x, y_alto), (x, y_baixo), cor, larg=larg, cabeca=12, brilho=3, dupla=True)


# ── Painéis (uma ideia editorial por proposta) ───────────────────────────────
def painel_v1():      # pergunta: rampa + looping, altura desconhecida
    c = Cena()
    pista = Pista(84, 292, 252)
    Hh = 2.6
    pista_desenho(c, pista, Hh)
    sx, sy = pista.pos_rampa(Hh)
    c.tracejada((sx, sy), (452, sy), VI)
    c.tracejada((60, 252), (452, 252), VI, alfa=110)
    dimensao_v(c, 452, sy, 252)
    c.esfera(sx + 3, sy - A_R * pista.k * 1.05, A_R * pista.k * 1.35, marca=-35)
    c.texto_grad((626, 137), "h = ?", fnt("bold", 132))
    return c.arte()


def painel_v2():      # duelo: duas alturas na mesma rampa
    c = Cena()
    pista = Pista(84, 300, 252)
    pista_desenho(c, pista, 2.7)
    s25, s27 = pista.pos_rampa(2.5), pista.pos_rampa(2.7)
    c.tracejada((s25[0], s25[1]), (486, s25[1]), CY, alfa=235)
    c.tracejada((s27[0], s27[1]), (486, s27[1]), MG, alfa=235)
    c.particula(s25[0] + 1, s25[1], 6.5, CY)
    c.esfera(s27[0] + 2, s27[1] - A_R * pista.k * 1.05, A_R * pista.k * 1.35, marca=-35)
    c.linha([(486, s27[1]), (514, 42), (540, 42)], MG, 2.5, 2, alfa=230)
    c.linha([(486, s25[1]), (514, 128), (540, 128)], CY, 2.5, 2, alfa=230)
    c.texto((548, 42), "2,7R", fnt("bold", 70), MG, ancora="lm", brilho=6)
    c.texto((548, 128), "2,5R", fnt("bold", 70), CY, ancora="lm", brilho=6)
    c.texto((548, 214), "+0,2R", fnt("medium", 44), WH, ancora="lm", alfa=205)
    return c.arte()


def painel_v3():      # contraste: duas colunas, partícula × esfera
    c = Cena()
    k = 62
    pe, pd = Pista(k, 214, 244), Pista(k, 604, 244)
    c.linha([(390, 20), (390, 262)], WH, 2, 3, alfa=75)
    pista_desenho(c, pe, 2.5, cauda=1.0, larg=4, brilho=5)
    pista_desenho(c, pd, 2.7, cauda=1.0, larg=4, brilho=5)
    y25 = pe.p(0, 2.5)[1]
    c.tracejada((8, y25), (772, y25), VI, 2, alfa=150)
    sx, sy = pe.pos_rampa(2.5)
    c.particula(sx, sy, 6.5, CY)
    sx2, sy2 = pd.pos_rampa(2.7)
    c.esfera(sx2 + 2, sy2 - A_R * k * 1.05, A_R * k * 1.7, marca=-35)
    c.texto((214, 40), "2,5R", fnt("bold", 56), CY, brilho=5)
    c.texto((604, 40), "2,7R", fnt("bold", 56), MG, brilho=5)
    return c.arte()


def painel_v4():      # causa: a esfera gira (v e ω) e a energia se divide
    c = Cena()
    cx, cy, r = 128, 140, 70
    c.esfera(cx, cy, r, marca=-50, brilho=12)
    c.seta((cx + r + 12, cy), (cx + r + 112, cy), CY, larg=7, cabeca=22, brilho=6)
    c.texto((cx + r + 62, cy - 24), "v", fnt("medium", 34), CY, brilho=3)
    c.arco_seta((cx, cy), r + 22, -150, -25, MG, larg=6, cabeca=22, brilho=6)
    c.texto((cx - 8, cy - r - 44), "ω", fnt("interb", 36), MG, brilho=3)
    x0, x1, y = 330, 765, 150
    cut = x0 + (x1 - x0) * 5 / 7
    c.linha([(x0, y), (cut - 4, y)], CY, 22, 7, ponta=False)
    c.linha([(cut + 4, y), (x1, y)], MG, 22, 7, ponta=False)
    c.texto((x0, y + 38), "TRANSLAÇÃO", fnt("inter", 21), CY, ancora="lm", alfa=235, trilha=1.5)
    c.texto((x1, y + 38), "ROTAÇÃO", fnt("inter", 21), MG, ancora="rm", alfa=235, trilha=1.5)
    c.texto((x1, y - 50), "2,5R → 2,7R", fnt("medium", 40), WH, ancora="rm", alfa=215)
    return c.arte()


def painel_v5():      # altura física: rampa dominante com régua
    c = Cena()
    pista = Pista(78, 262, 250)
    Hh = 2.6
    pista_desenho(c, pista, Hh, larg=7, brilho=9)
    sx, sy = pista.pos_rampa(Hh)
    xr = 38
    c.linha([(xr, 250 + 16), (xr, sy)], WH, 2.5, 3, alfa=210)
    for i in range(6):
        yy = 250 - i * 0.5 * 78
        if yy >= sy - 3:
            c.linha([(xr, yy), (xr + (16 if i % 2 == 0 else 9), yy)], WH, 2.5, 0, alfa=210, ponta=False)
    c.linha([(xr - 6, 250 + 16), (730, 250 + 16)], WH, 2, 2, alfa=70)
    c.tracejada((xr, sy), (sx - 6, sy), VI)
    dimensao_v(c, xr + 26, sy, 250 + 16, cor=VI, larg=3)
    c.esfera(sx + 3, sy - A_R * pista.k * 1.05, A_R * pista.k * 1.35, marca=-35)
    c.texto_grad((612, 118), "h = ?", fnt("bold", 128))
    return c.arte()


def painel_v6():      # minimal: um looping, uma esfera, uma altura
    c = Cena()
    pista = Pista(96, 400, 256)
    c.linha(pista.pontos(None, 1.9)[:-1] + [pista.p(1.9, -A_R)], BL, 5, 9)
    c.linha([pista.p(-1.9, -A_R), pista.p(0, -A_R)], BL, 5, 5, alfa=200)
    sx, sy = pista.pos_loop(2.5)
    c.esfera(sx, sy, A_R * pista.k * 1.5, marca=-20, brilho=8)
    xl = 168
    c.tracejada((xl, 256 + 4), (xl, 40), VI, 2.5)
    c.linha([(xl - 10, 40), (xl + 10, 40)], VI, 2.5, 2)
    f = fnt("medium", 52)
    c.texto((xl - 18, 66), "h", f, VI, ancora="rm")
    c.texto((xl - 14, 98), "min", fnt("medium", 30), VI, ancora="rm")
    c.texto((xl - 18, 138), "= ?", f, VI, ancora="rm")
    return c.arte()


# ── Base da série (igual ao vid_0007, EP. 03): apaga título, série e interior do painel ──
def gradient(size, stops):
    w, h = size
    seg = np.clip(np.linspace(0, 1, w) * (len(stops) - 1), 0, len(stops) - 1 - 1e-6)
    i = seg.astype(int)
    f = (seg - i)[:, None]
    row = (np.array(stops)[i] * (1 - f) + np.array(stops)[i + 1] * f).astype(np.uint8)
    return Image.fromarray(np.repeat(row[None], h, 0), "RGB")


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
        u = np.linspace(0, 1, x1 - x0)[None, :, None]
        v = np.linspace(0, 1, y1 - y0)[:, None, None]
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


def glow_paste(img, layer_mask, box, color_img, glow_color, glow_radius, glow_alpha):
    full = Image.new("L", img.size, 0)
    full.paste(layer_mask, box[:2])
    halo = full.filter(ImageFilter.GaussianBlur(glow_radius)).point(lambda v: int(v * glow_alpha))
    img = Image.composite(Image.new("RGBA", img.size, glow_color + (255,)), img, halo)
    fill_full = Image.new("RGBA", img.size)
    fill_full.paste(color_img.convert("RGBA"), box[:2])
    return Image.composite(fill_full, img, full)


def text_mask(text, font, tracking=0):
    widths = [font.getlength(ch) + tracking for ch in text]
    asc, desc = font.getmetrics()
    mk = Image.new("L", (int(sum(widths) - tracking) + 4, asc + desc + 4), 0)
    d = ImageDraw.Draw(mk)
    x = 2
    for ch, w in zip(text, widths):
        d.text((x, 2), ch, font=font, fill=255)
        x += w
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


def cover(lines, panel_art):
    img = base()
    rows = [headline_line(seg, start) for seg, start in lines]
    gap = 22
    total = sum(r[0].height for r in rows) + gap * (len(rows) - 1)
    assert total <= 320, f"headline alta demais: {total}px"
    y = 822 - total / 2                                    # bloco do título: y 666–1000
    for mask, color, glow, _ in rows:
        img = glow_paste(img, mask, ((img.width - mask.width) // 2, int(y)), color, glow, 15, 0.5)
        y += mask.height + gap
    series = text_mask(SERIE, ImageFont.truetype(MEDIUM, 38), tracking=9)
    series = series.resize((min(series.width, 850), round(series.height * min(series.width, 850) / series.width)),
                           Image.LANCZOS)
    img = glow_paste(img, series, center(img, series, 1097), Image.new("RGB", series.size, (245, 247, 255)),
                     (60, 120, 255), 6, 0.32)
    art = panel_art                                        # painel original: interior x 226–874, y 1194–1420
    k = min(600 / art.width, 215 / art.height)
    art = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)
    x, y = (img.width - art.width) // 2, 1307 - art.height // 2
    full = Image.new("L", img.size, 0)
    full.paste(art.getchannel("A"), (x, y))
    halo = full.filter(ImageFilter.GaussianBlur(10)).point(lambda p: int(p * 0.3))
    img = Image.composite(Image.new("RGBA", img.size, (90, 110, 255, 255)), img, halo)
    img.alpha_composite(art, (x, y))
    return img.convert("RGB")


# ── As seis propostas: (arquivo, headline, painel) ───────────────────────────
PROPOSTAS = [
    ("capa_v01_pergunta.png", [([("QUAL A ALTURA", "white")], 118), ([("MÍNIMA?", "grad")], 170)], painel_v1),
    ("capa_v02_25_vs_27.png", [([("2,5R OU", "white")], 170), ([("2,7R?", "grad")], 170)], painel_v2),
    ("capa_v03_particula_vs_esfera.png", [([("PARTÍCULA", "white")], 150), ([("≠ ESFERA", "grad")], 160)], painel_v3),
    ("capa_v04_rotacao.png", [([("A ROTAÇÃO", "white")], 150), ([("MUDA TUDO", "grad")], 160)], painel_v4),
    ("capa_v05_altura_h.png", [([("DE QUÃO ALTO", "white")], 90), ([("ELA PRECISA", "white")], 112), ([("PARTIR?", "grad")], 124)], painel_v5),
    ("capa_v06_minimal.png", [([("ESFERA NO", "white")], 96), ([("LOOPING", "grad")], 170)], painel_v6),
]


def contato():
    tw, th, gap = 360, 640, 30
    folha = Image.new("RGB", (3 * tw + 4 * gap, 2 * th + 3 * gap), (12, 14, 28))
    d = ImageDraw.Draw(folha)
    rot = ImageFont.truetype(str(INTER["bold"]), 34)
    for i, (nome, _, _) in enumerate(PROPOSTAS):
        im = Image.open(OUT / nome).convert("RGB").resize((tw, th), Image.LANCZOS)
        x, y = gap + (i % 3) * (tw + gap), gap + (i // 3) * (th + gap)
        folha.paste(im, (x, y))
        d.rounded_rectangle((x + 12, y + 12, x + 84, y + 58), 10, fill=(5, 8, 22))
        d.text((x + 48, y + 36), f"V{i + 1}", font=rot, fill=(245, 247, 255), anchor="mm")
    folha.save(OUT / "capas_contato.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for nome, lines, painel in PROPOSTAS:
        cover(lines, painel()).save(OUT / nome, optimize=True)
        print(nome)
    contato()
    print("capas_contato.png ->", OUT)
