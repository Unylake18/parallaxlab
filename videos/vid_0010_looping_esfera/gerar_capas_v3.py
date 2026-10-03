"""Terceira leva de capas do vid_0010 (V13–V18): a composição de referência refeita em 6 variações.

Uso, na raiz do repositório:
    uv run python videos/vid_0010_looping_esfera/gerar_capas_v3.py [PASTA_SAIDA]

Layout da referência (imagem aprovada pelo usuário): título gigante "2,5R / OU ?", tela dividida (partícula em ciano
à esquerda, esfera em magenta à direita), pílulas "PARTÍCULA" / "ESFERA", valores "2,5R" e "?", rampa + looping neon
com a trajetória do CM tracejada, linha de altura com seta, chão com reflexo e marca no canto superior direito.
Mudanças em relação à referência: números e "?" em Space Grotesk Bold (a fonte aprovada); pista com a geometria da
cena (rampa suave e tangente ao fundo do looping, em vez de uma curva solta); partícula e esfera partem da mesma
altura (a incógnita é justamente se a esfera precisa de mais). Reaproveita de gerar_capas_v2.py a tela cheia e as
primitivas de desenho. Nenhuma variação é eleita aqui.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(UNIT))
import gerar_capas_v2 as v2  # noqa: E402
g = v2.g

g.M_SL, g.C_SL = 2.4, 2.5              # rampa mais íngreme que a da cena (mesma família; M/C < 1: não cruza o looping)
S, W, H = v2.S, v2.W, v2.H
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capas"
CY, BL, VI, MG, WH = g.CY, g.BL, g.VI, g.MG, g.WH
fnt = g.fnt

K = 124                                  # pixels por R
FLOOR = 1700                             # linha do chão
OY = FLOOR - round(g.A_R * K)            # ponto mais baixo da trajetória do CM
HH = 2.5                                 # altura de partida mostrada nos dois lados (a esfera é a incógnita)
OX_L, OX_R = 381, 921                    # ponto mais baixo do looping em cada lado
Y_H = OY - HH * K                        # nível de partida
Y_ROT = {"L": (CY, "#BFEFFF", BL), "R": (MG, "#F1CBFF", VI)}   # (meio, núcleo, brilho) de cada lado


BASE_SERIE = UNIT.parent / "vid_0002_integral_substituicao" / "capa_instagram.png"
_WM = {}


def wordmark_padrao():
    """O "PARALLAX LAB" padrão das capas da série (fonte da marca, "LAB" em degradê), extraído da base e
    convertido em PNG transparente: o brilho vira opacidade e a cor original é mantida."""
    if "im" not in _WM:
        a = Image.open(BASE_SERIE).convert("RGB").crop((298, 1588, 788, 1634))
        rgb_ = np.asarray(a, np.float32)
        al = np.clip((rgb_.max(2) - 45) / 130, 0, 1)
        out = np.dstack([rgb_, al[..., None] * 255]).astype(np.uint8)
        _WM["im"] = Image.fromarray(out, "RGBA")
    return _WM["im"]


def largura(texto, fonte):
    return ImageDraw.Draw(Image.new("L", (10, 10))).textlength(texto, font=fonte) / S


def ajusta(texto, max_w, ini, minimo=60):
    t = ini
    while t > minimo and largura(texto, fnt("bold", t)) > max_w:
        t -= 2
    return t


class T3(v2.Tela):
    """Tela com os acabamentos da referência: neon, esferas brilhantes, pílulas, reflexo."""

    def neon(self, pts, meio, nucleo, brilho_cor, esp=1.0, forte=False):
        self.linha(pts, brilho_cor, 22 * esp, 18, alfa=150 if forte else 105, ponta=False)
        self.linha(pts, meio, 8.5 * esp, 6, alfa=235, ponta=False)
        self.linha(pts, nucleo, 3.2 * esp, 0, alfa=255, ponta=False)

    def circ_trac(self, cx, cy, r, cor, alfa=190, n=44, larg=2.6):
        c = self.camada()
        d = ImageDraw.Draw(c)
        for i in range(n):
            a0, a1 = 2 * np.pi * i / n, 2 * np.pi * (i + 0.55) / n
            pts = [((cx + r * np.cos(a)) * S, (cy + r * np.sin(a)) * S) for a in np.linspace(a0, a1, 6)]
            d.line(pts, fill=g.rgb(cor) + (alfa,), width=round(larg * S))
        self.cola(c, 2, 0.5)

    def bola(self, cx, cy, r, c0, c1, borda, brilho=12, marca=None, cor_marca=None):
        n = round(2 * r * S) + 6
        yy, xx = np.mgrid[0:n, 0:n]
        u, v = (xx - n / 2) / (r * S), (yy - n / 2) / (r * S)
        rho = np.hypot(u, v)
        luz = np.clip(1 - np.hypot(u + 0.30, v + 0.38) / 1.30, 0, 1)
        brilhante = np.exp(-np.hypot(u + 0.36, v + 0.42) ** 2 / 0.05)
        cor = np.array(c0, float) + (np.array(c1, float) - np.array(c0, float)) * (luz ** 1.2)[..., None]
        cor = np.clip(cor + 150 * brilhante[..., None], 0, 255)
        im = np.zeros((n, n, 4))
        im[..., :3] = cor
        im[..., 3] = np.where(rho <= 1.0, 255, 0)
        camada = self.camada()
        camada.alpha_composite(Image.fromarray(im.astype("uint8"), "RGBA"),
                               (round((cx - r) * S) - 3, round((cy - r) * S) - 3))
        d = ImageDraw.Draw(camada)
        d.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), outline=g.rgb(borda) + (255,),
                  width=max(2, round(r * 0.07 * S)))
        if marca is not None:
            a = np.radians(marca)
            d.line([(cx * S, cy * S), ((cx + 0.88 * r * np.cos(a)) * S, (cy + 0.88 * r * np.sin(a)) * S)],
                   fill=g.rgb(cor_marca) + (255,), width=max(3, round(r * 0.13 * S)))
            d.ellipse(((cx - r * 0.1) * S, (cy - r * 0.1) * S, (cx + r * 0.1) * S, (cy + r * 0.1) * S),
                      fill=g.rgb(WH) + (255,))
        self.cola(camada, brilho, 0.9)

    def pilula(self, cx, cy, w, h, texto, cor, cheia=False):
        c = self.camada()
        d = ImageDraw.Draw(c)
        box = ((cx - w / 2) * S, (cy - h / 2) * S, (cx + w / 2) * S, (cy + h / 2) * S)
        if cheia:
            d.rounded_rectangle(box, radius=h / 2 * S, fill=g.rgb(cor) + (46,))
        d.rounded_rectangle(box, radius=h / 2 * S, outline=g.rgb(cor) + (255,), width=round(4 * S))
        self.cola(c, 7, 0.8)
        self.texto((cx, cy + 1), texto, fnt("interb", 41), cor, ancora="mm", trilha=0.5)

    def reflexo(self, y, alt=250, forca=0.34):
        s = self.img.crop((0, (y - alt) * S, W * S, y * S)).transpose(Image.FLIP_TOP_BOTTOM)
        rampa = np.linspace(forca, 0, alt * S)[:, None]
        mascara = Image.fromarray((np.repeat(rampa, W * S, 1) * 255).astype("uint8"), "L")
        regiao = self.img.crop((0, y * S, W * S, (y + alt) * S))
        self.img.paste(Image.composite(s, regiao, mascara), (0, y * S))

    def wordmark(self, cx, cy, larg):
        w = wordmark_padrao()
        im = w.resize((round(larg * S), round(larg * S * w.height / w.width)), Image.LANCZOS)
        self.img.alpha_composite(im, (round(cx * S - im.width / 2), round(cy * S - im.height / 2)))

    def marca_canto(self, padrao=False):
        if padrao:
            ic = Image.open(v2.ICONE).convert("RGBA")
            tam = 84
            ic = ic.resize((tam * S, round(tam * S * ic.height / ic.width)), Image.LANCZOS)
            self.img.alpha_composite(ic, (round((946 - tam / 2) * S), 90 * S))
            self.wordmark(946, 204, 168)
            return
        ic = Image.open(v2.ICONE).convert("RGBA")
        tam = 84
        ic = ic.resize((tam * S, round(tam * S * ic.height / ic.width)), Image.LANCZOS)
        cx = 946
        self.img.alpha_composite(ic, (round((cx - tam / 2) * S), 92 * S))
        self.texto((cx, 196), "PARALLAX", fnt("inter", 23), WH, ancora="mm", trilha=2)
        self.texto((cx, 222), "LAB", fnt("inter", 23), CY, ancora="mm", trilha=4)


def fundo_galaxia():
    """O fundo clássico da série (nebulosas laterais, estrelas e horizonte do planeta): a própria base das capas,
    sem logo, título, linha de série, painel nem wordmark. As áreas apagadas são refeitas a partir das bordas."""
    a = np.asarray(Image.open(BASE_SERIE).convert("RGB"), np.float32)
    img = Image.fromarray(a.astype(np.uint8))
    soft = np.asarray(img.filter(ImageFilter.MinFilter(15)).filter(ImageFilter.GaussianBlur(20)), np.float32)
    suave = lambda v: np.asarray(Image.fromarray(np.clip(v, 0, 255).astype(np.uint8)[None]).filter(
        ImageFilter.GaussianBlur(6)), np.float32)[0]
    fill, mask = a.copy(), np.zeros(a.shape[:2], np.float32)

    def coons(x0, x1, y0, y1):                           # preenche o retângulo só com os valores das quatro bordas
        topo, base_ = suave(soft[y0, x0:x1]), suave(soft[y1 - 1, x0:x1])
        esq, dir_ = suave(soft[y0:y1, x0]), suave(soft[y0:y1, x1 - 1])
        u = np.linspace(0, 1, x1 - x0)[None, :, None]
        v = np.linspace(0, 1, y1 - y0)[:, None, None]
        cantos = (1 - v) * ((1 - u) * topo[0] + u * topo[-1]) + v * ((1 - u) * base_[0] + u * base_[-1])
        fill[y0:y1, x0:x1] = (1 - v) * topo[None] + v * base_[None] + (1 - u) * esq[:, None] + u * dir_[:, None] - cantos
        mask[y0:y1, x0:x1] = 1

    def faixa(x0, x1, y0, y1, mistura=30):               # como nas outras capas: só as linhas de cima e de baixo
        topo, base_ = soft[y0, x0:x1], soft[y1, x0:x1]
        t = np.clip((np.arange(y1 - y0) - (y1 - y0 - mistura)) / mistura, 0, 1)[:, None, None]
        fill[y0:y1, x0:x1] = (1 - t) * topo[None] + t * base_[None]
        mask[y0:y1, x0:x1] = 1

    coons(290, 840, 90, 705)                            # símbolo grande
    faixa(64, 1016, 666, 1146)                          # título, divisor e linha de série
    faixa(140, 940, 1146, 1474)                         # painel
    faixa(285, 810, 1576, 1646)                         # wordmark original
    m = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9)),
                   np.float32)[..., None] / 255
    fill = fill + np.random.default_rng(5).normal(0, 1.6, fill.shape)
    out = Image.fromarray(np.clip(a * (1 - m) + fill * m, 0, 255).astype(np.uint8)).convert("RGBA")
    return out.resize((W * S, H * S), Image.LANCZOS)


def fundo_base(estilo):
    if estilo == "galaxia":
        return fundo_galaxia()
    if estilo == "premium":
        return v2.fundo(glows=[(300, 480, 520, (20, 140, 210), 0.20), (800, 480, 520, (190, 60, 220), 0.18),
                               (270, 1560, 420, (20, 70, 170), 0.16), (810, 1560, 420, (110, 40, 190), 0.18)],
                        estrelas=36, nebulosa=0.55, seed=16)
    if estilo == "limpo":
        return v2.fundo(glows=[(270, 1300, 520, (20, 70, 150), 0.07), (810, 1300, 520, (90, 40, 150), 0.07)],
                        estrelas=0, seed=17)
    return v2.fundo(glows=[(270, 1500, 520, (20, 80, 170), 0.13), (810, 1500, 520, (110, 40, 190), 0.14),
                           (300, 420, 480, (20, 120, 200), 0.08), (800, 640, 420, (180, 60, 210), 0.08)],
                    estrelas=28, seed=13)


def compor(nome, estilo="base", rotacao=False, nivel_comum=False, ponto_grande=False, pilulas="vazia",
           reflexo=True, esp=1.0, h_tags=False, circulo_cm=True, divisor="fino", titulo_degrade=False, marca_std=False):
    c = T3(fundo_base(estilo))
    forte = estilo == "premium"

    # marca e série
    c.texto((478, 150), v2.SERIE, fnt("inter", 27), WH, alfa=210, trilha=6, ancora="mm")
    c.marca_canto(padrao=marca_std)

    # título
    t1 = ajusta("2,5R", 760, 360)
    if titulo_degrade:                                   # degradê da marca: ciano → azul → violeta no "2,5R"
        c.texto_grad((540, 410), "2,5R", fnt("bold", t1), ancora="mm", brilho=16, cores=[g.BRAND[0], g.BRAND[1], g.BRAND[2]])
    else:
        c.texto((540, 410), "2,5R", fnt("bold", t1), CY, ancora="mm", brilho=16)
    t2 = 236
    f2 = fnt("bold", t2)
    wou, wq, gap = largura("OU", f2), largura("?", f2), 46
    x0 = 540 - (wou + gap + wq) / 2
    c.texto((x0, 705), "OU", f2, WH, ancora="lm", brilho=10)
    if titulo_degrade:                                   # "?": violeta → magenta (como o "2,7R?" do exemplo)
        c.texto_grad((x0 + wou + gap, 705), "?", f2, ancora="lm", brilho=16, cores=[g.BRAND[2], g.BRAND[3]])
    else:
        c.texto((x0 + wou + gap, 705), "?", f2, MG, ancora="lm", brilho=16)

    # divisor
    if divisor == "fino":
        c.linha([(540, 910), (540, FLOOR)], "#6FA8FF", 2.4, 3, alfa=120, ponta=False)
    else:
        for i, (a, cor) in enumerate(((910, CY), (1310, "#B58CFF"))):
            c.linha([(540, a), (540, a + 400)], cor, 3.2, 5, alfa=150, ponta=False)

    # pílulas e valores
    for cx, rot, cor in ((270, "PARTÍCULA", CY), (810, "ESFERA", MG)):
        if pilulas == "vazia":
            c.pilula(cx, 990, 390, 88, rot, cor)
        elif pilulas == "cheia":
            c.pilula(cx, 990, 390, 88, rot, cor, cheia=True)
        else:                                            # sem pílula: rótulo pequeno com sublinhado
            c.texto((cx, 980), rot, fnt("interb", 38), cor, ancora="mm", trilha=5)
            c.linha([(cx - 120, 1018), (cx + 120, 1018)], cor, 3, 3, alfa=200)
    sv = 132
    c.texto((270, 1140), "2,5R", fnt("bold", sv), CY, ancora="mm", brilho=10)
    c.texto((810, 1140), "?", fnt("bold", int(sv * (1.28 if ponto_grande else 1.0))), MG, ancora="mm", brilho=12)

    # pistas
    for lado, ox, (meio, nucleo, brilho_cor) in (("L", OX_L, Y_ROT["L"]), ("R", OX_R, Y_ROT["R"])):
        p = g.Pista(K, ox, OY)
        pts = p.pontos(HH, 1.18)
        c.neon(pts, meio, nucleo, brilho_cor, esp, forte)
        if circulo_cm:
            c.circ_trac(ox, OY - K, K, meio)
        # nível de partida e seta de altura
        cx0, cy0, _ = c.corpo_rampa(p, g.u_de_H(HH), 1.0)
        xs = ox - g.u_de_H(HH) * K
        x_fim = 480 if lado == "L" else 1020
        c.tra((cx0 + 4, Y_H), (x_fim, Y_H), meio, alfa=235, larg=3.6)
        xa = ox + 76
        rt = K * (1 + g.A_R)
        y_top = (OY - K) - np.sqrt(rt * rt - 76 * 76)
        c.seta((xa, y_top - 2), (xa, Y_H + 3), meio, larg=4.5, cabeca=26, brilho=8)
        if h_tags:
            c.texto((x_fim + (4 if lado == "L" else -2), Y_H - 46), "h", fnt("bold", 70), "#9B86FF", ancora="rm", brilho=7)
        # corpo
        dire = np.array([0.51, 0.86])                      # tangente da rampa na partida (tela: para a direita e para baixo)
        if lado == "L":
            rp = 22
            c.bola(xs + 3, Y_H - 8, rp, (10, 50, 120), (120, 230, 255), CY, brilho=14)
            if rotacao:
                o = np.array([xs + 3, Y_H - 8]) + dire * (rp + 12)
                c.seta(tuple(o), tuple(o + dire * 84), CY, larg=5, cabeca=22, brilho=6)
        else:
            rc = 40
            bx, by, _ = c.corpo_rampa(p, g.u_de_H(HH), rc / (g.A_R * K))
            c.bola(bx, by, rc, (50, 8, 90), (225, 120, 255), MG, brilho=16,
                   marca=-35 if rotacao else None, cor_marca="#FFD8FF")
            if rotacao:
                c.arco_seta((bx, by), rc + 20, -170, -35, MG, larg=6, cabeca=22, brilho=7)
                o = np.array([bx, by]) + dire * (rc + 12)
                c.seta(tuple(o), tuple(o + dire * 84), CY, larg=5, cabeca=22, brilho=6)
    if nivel_comum:                                      # a esfera parte da mesma altura? uma linha atravessa o divisor
        c.linha([(462, Y_H), (618, Y_H)], WH, 4, 5, alfa=190, ponta=False)
        c.texto((540, Y_H - 52), "=", fnt("bold", 84), WH, ancora="mm", alfa=235, brilho=8)

    # chão e reflexo
    if reflexo:
        c.reflexo(FLOOR)
    c.linha([(0, FLOOR), (540, FLOOR)], CY, 3.2, 8, alfa=230, ponta=False)
    c.linha([(540, FLOOR), (1080, FLOOR)], MG, 3.2, 8, alfa=230, ponta=False)
    if marca_std:                                        # a assinatura padrão da série, embaixo (como nas outras capas)
        c.wordmark(540, 1822, 470)
    v2.salvar(c, nome)


VARIACOES = [
    ("capa_v13_fiel.png", dict()),
    ("capa_v14_rotacao.png", dict(rotacao=True, pilulas="cheia")),
    ("capa_v15_mesma_altura.png", dict(nivel_comum=True, ponto_grande=True)),
    ("capa_v16_premium.png", dict(estilo="premium", divisor="grad", esp=1.15)),
    ("capa_v17_limpa.png", dict(estilo="limpo", pilulas="texto", reflexo=False, esp=0.8, circulo_cm=False)),
    ("capa_v18_tags_h.png", dict(h_tags=True, pilulas="cheia", ponto_grande=True)),
]


def contato():
    tw, th, gap, rot_h = 360, 640, 30, 46
    folha = Image.new("RGB", (3 * tw + 4 * gap, 2 * (th + rot_h) + 3 * gap), (12, 14, 28))
    d = ImageDraw.Draw(folha)
    rot = g.ImageFont.truetype(str(g.INTER["bold"]), 30)
    for i, (nome, _) in enumerate(VARIACOES):
        im = Image.open(OUT / nome).convert("RGB").resize((tw, th), Image.LANCZOS)
        x, y = gap + (i % 3) * (tw + gap), gap + (i // 3) * (th + rot_h + gap)
        folha.paste(im, (x, y))
        d.text((x + tw // 2, y + th + rot_h // 2), f"V{i + 13}", font=rot, fill=(245, 247, 255), anchor="mm")
    folha.save(OUT / "capas_contato_v3.png")


if __name__ == "__main__":
    v2.OUT = OUT
    for nome, kw in VARIACOES:
        compor(nome, **kw)
    contato()
    print("capas_contato_v3.png ->", OUT)
