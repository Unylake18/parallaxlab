"""Segunda leva de capas do vid_0010 (V7–V12), 1080×1920, mais editoriais e centradas na física.

Uso, na raiz do repositório:
    uv run python videos/vid_0010_looping_esfera/gerar_capas_v2.py [PASTA_SAIDA]

Diferente da primeira leva (gerar_capas.py, que segue o template da série), aqui não há template: fundo
escuro próprio por capa, marca pequena num canto, linha de série discreta e a pista (rampa + looping)
desenhada direto na composição, sem card. Reaproveita de gerar_capas.py só as primitivas de desenho
(linhas, setas, esfera) e a geometria da cena: trajetória do CM de raio R, pista física R + a,
rampa y = 1,4(√(u²+1,7²) − 1,7). Fontes: Space Grotesk e Inter, versionadas. Nenhuma capa é eleita aqui.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(UNIT))
import gerar_capas as g  # noqa: E402  (só as primitivas e a geometria; o módulo não gera nada ao importar)

g.S = 2                                  # supersampling da tela cheia (1080×1920 -> 2160×3840)
S = g.S
W, H = 1080, 1920
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else UNIT / "capas"
TEMPLATE = ROOT / "assets" / "branding" / "social" / "parallax_lab_cover_template_9x16.png"
ICONE = ROOT / "assets" / "branding" / "master" / "parallax_lab_icon_transparent.png"
CY, BL, VI, MG, WH = g.CY, g.BL, g.VI, g.MG, g.WH
SERIE = g.SERIE
A_R = g.A_R
fnt = g.fnt
rgb = g.rgb


# ── Fundos ───────────────────────────────────────────────────────────────────
def fundo(glows=(), grad=None, estrelas=0, nebulosa=0.0, seed=0):
    """Base #050816 + brilhos radiais suaves; estrelas e nebulosa (só das bordas do template) opcionais."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    img = np.zeros((H, W, 3), np.float32) + np.array([5, 8, 22], np.float32)
    if grad:
        t = (yy / H)[..., None]
        img = img * 0 + (1 - t) * np.array(grad[0], np.float32) + t * np.array(grad[1], np.float32)
    for cx, cy, r, col, a in glows:
        d = np.hypot(xx - cx, yy - cy) / r
        w = (np.exp(-d * d * 1.6) * a)[..., None]
        img = img * (1 - w) + np.array(col, np.float32) * w
    if nebulosa:
        tpl = np.asarray(Image.open(TEMPLATE).convert("RGB").resize((W, H), Image.LANCZOS), np.float32)
        lado = np.clip(np.maximum(0.20 - xx / W, xx / W - 0.80) / 0.20, 0, 1) ** 1.3     # só as bordas: o miolo do
        topo = np.clip(1 - (yy - 80) / 540, 0, 1)                                         # template tem logo e título
        img = img + tpl * (lado * topo * nebulosa)[..., None]
    out = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(out)
    for _ in range(estrelas):
        x, y = int(rng.integers(30, W - 30)), int(rng.integers(30, H - 30))
        v = int(rng.integers(80, 190))
        d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(v, v, 255))
    arr = np.asarray(out, np.float32) + rng.normal(0, 1.2, (H, W, 3))
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    return out.resize((W * S, H * S), Image.LANCZOS)


class Tela(g.Cena):
    """A mesma Cena de desenho, mas na tela inteira 1080×1920."""

    def __init__(self, bg):
        self.img = bg

    def marca(self, ic_xy, ic_tam, serie_xy, ancora="lm", alfa=170):
        ic = Image.open(ICONE).convert("RGBA")
        ic = ic.resize((ic_tam * S, round(ic_tam * S * ic.height / ic.width)), Image.LANCZOS)
        self.img.alpha_composite(ic, (round(ic_xy[0] * S), round(ic_xy[1] * S)))
        self.texto(serie_xy, SERIE, fnt("inter", 24), WH, alfa=alfa, trilha=5, ancora=ancora)

    def pista(self, p, Hh, cauda, larg=11, brilho=14, alfa=255, esmaece=False):
        pts = p.pontos(Hh, cauda)
        if not esmaece:
            self.linha(pts, BL, larg, brilho, alfa)
            return
        n = 80                                         # trecho da rampa: some para a esquerda (continua fora do quadro)
        rampa, resto = pts[:n], pts[n - 1:]
        for i in range(0, n - 1, 3):
            seg = rampa[i:i + 4]
            xm = seg[len(seg) // 2][0]
            a = int(np.clip((xm - 0) / 420, 0.12, 1.0) * alfa)
            self.linha(seg, BL, larg, 0, a, ponta=False)
        self.linha(resto, BL, larg, brilho, alfa)

    def corpo_rampa(self, p, u, esc):
        """(cx, cy, r): esfera de raio esc·a·k apoiada na rampa no ponto de abscissa -u (em R)."""
        gr = g.M_SL * u / np.sqrt(u * u + g.C_SL ** 2)
        n = np.hypot(1, gr)
        lift = (esc - 1) * p.a
        cx, cy = p.p(-u + lift * gr / n, g.f_ramp(u) + lift / n)
        return cx, cy, esc * p.a * p.k

    def corpo_loop(self, p, th, esc):
        rc = 1 + p.a - esc * p.a
        cx, cy = p.p(rc * np.sin(th), 1 - rc * np.cos(th))
        return cx, cy, esc * p.a * p.k

    def tra(self, a, b, cor, alfa=215, larg=4):
        self.tracejada(a, b, cor, larg=larg, tra=24, vao=17, alfa=alfa, brilho=3)

    def dimensao(self, x, y_alto, y_baixo, cor=VI, larg=5, cab=26):
        self.seta((x, y_alto), (x, y_baixo), cor, larg=larg, cabeca=cab, brilho=5, dupla=True)

    def regua(self, x, p, y_alto, y_baixo, cor=WH, passo=0.5, lado=1):
        k, oy = p.k, p.oy
        i = 0
        while oy - i * passo * k >= y_alto - 2:
            yy = oy - i * passo * k
            if yy <= y_baixo + 2:
                self.linha([(x, yy), (x + lado * (22 if i % 2 == 0 else 13), yy)], cor, 3, 0, alfa=170, ponta=False)
            i += 1


def titulo(c, linhas, y0, x=540, ancora="mm", larg_max=960):
    """linhas = [(texto, corpo, estilo)], estilo: 'w' branco, 'g' gradiente da marca ou cor '#rrggbb'."""
    d = ImageDraw.Draw(Image.new("L", (10, 10)))
    cur = y0
    for t, size, st in linhas:
        f = fnt("bold", size)
        assert d.textlength(t, font=f) / S <= larg_max, f"linha larga demais: {t!r}"
        yc = cur + size * 0.5
        if st == "g":
            c.texto_grad((x, yc), t, f, ancora=ancora, brilho=9)
        else:
            c.texto((x, yc), t, f, WH if st == "w" else st, ancora=ancora, brilho=8)
        cur += size * 1.08
    return cur


# ── V7 — a rampa como herói ──────────────────────────────────────────────────
def v7():
    c = Tela(fundo(glows=[(760, 1500, 760, (30, 90, 170), 0.16), (140, 520, 620, (70, 50, 170), 0.10)],
                   estrelas=22, seed=7))
    c.marca((54, 52), 54, (126, 80))
    titulo(c, [("QUAL A ALTURA", 128, "w"), ("MÍNIMA?", 176, "g")], 170)
    k, ox, oy, Hh = 228, 760, 1700, 2.6
    p = g.Pista(k, ox, oy)
    c.pista(p, Hh, 1.23)
    cx, cy, r = c.corpo_rampa(p, g.u_de_H(Hh), 1.6)
    c.tra((cx, cy), (1046, cy), VI)
    c.tra((60, oy), (1046, oy), VI, alfa=110, larg=3)
    c.dimensao(1050, cy, oy)
    c.regua(1046, p, cy, oy, lado=-1)
    c.esfera(cx, cy, r, marca=-35, brilho=10)
    c.texto_grad((590, 800), "h = ?", fnt("bold", 230))
    salvar(c, "capa_v07_altura_minima.png")


# ── V8 — 2,5R ou 2,7R ────────────────────────────────────────────────────────
def v8():
    c = Tela(fundo(glows=[(760, 1480, 700, (80, 50, 190), 0.20), (200, 260, 700, (30, 70, 160), 0.12)],
                   grad=((6, 12, 40), (13, 8, 38)), estrelas=34, seed=8))
    c.marca((54, 52), 54, (126, 80))
    f = fnt("bold", 200)
    d = ImageDraw.Draw(Image.new("L", (10, 10)))
    w1, w2 = d.textlength("2,5R", font=f) / S, d.textlength(" OU", font=f) / S
    x = 540 - (w1 + w2) / 2
    c.texto((x, 300), "2,5R", f, CY, ancora="lm", brilho=12)
    c.texto((x + w1, 300), " OU", f, WH, ancora="lm", brilho=8)
    c.texto_grad((540, 300 + 214), "2,7R?", f, cores=[(0x74, 0x5C, 0xFF), (0xEA, 0x63, 0xFF)], brilho=12)
    k, ox, oy = 222, 777, 1700
    p = g.Pista(k, ox, oy)
    c.pista(p, 2.7, 1.23)
    s27 = c.corpo_rampa(p, g.u_de_H(2.7), 1.6)
    s25 = c.corpo_rampa(p, g.u_de_H(2.5), 1.0)
    y27, y25 = oy - 2.7 * k, oy - 2.5 * k
    c.tra((s27[0], y27), (1046, y27), MG, alfa=240)
    c.tra((s25[0], y25), (1046, y25), CY, alfa=240)
    c.particula(s25[0], y25, 11, CY, brilho=10)
    c.esfera(s27[0], s27[1], s27[2], marca=-35, brilho=10)
    c.texto((1040, y27 - 52), "2,7R", fnt("bold", 76), MG, ancora="rm", brilho=8)
    c.texto((1040, y25 + 54), "2,5R", fnt("bold", 76), CY, ancora="rm", brilho=8)
    c.seta((640, y27 + 3), (640, y25 - 3), WH, larg=4, cabeca=14, brilho=3, dupla=True)
    salvar(c, "capa_v08_25_ou_27.png")


# ── V9 — h = ? como protagonista ─────────────────────────────────────────────
def v9():
    c = Tela(fundo(glows=[(540, 540, 560, (30, 110, 190), 0.11), (900, 1500, 520, (80, 60, 190), 0.08)],
                   estrelas=0, seed=9))
    c.marca((54, 1818), 48, (122, 1842))
    titulo(c, [("QUAL A ALTURA?", 70, "w")], 150)
    f = fnt("bold", 330)
    c.texto_grad((540, 560), "h = ?", f, brilho=14)
    k, ox, oy, Hh = 222, 767, 1740, 2.5
    p = g.Pista(k, ox, oy)
    c.pista(p, Hh, 1.23, larg=10)
    cx, cy, r = c.corpo_rampa(p, g.u_de_H(Hh), 1.5)
    c.tra((cx, cy), (1046, cy), VI)
    c.dimensao(1050, cy, oy)
    c.regua(1046, p, cy, oy, lado=-1)
    c.linha([(1050, cy - 14), (1050, 760)], VI, 3, 3, alfa=140, ponta=False)       # liga a altura ao "h"
    c.particula(1050, 760, 7, VI, brilho=6)
    c.esfera(cx, cy, r, marca=-35, brilho=8)
    salvar(c, "capa_v09_h_interrogacao.png")


# ── V10 — chega ao topo? ─────────────────────────────────────────────────────
def v10():
    c = Tela(fundo(glows=[(682, 1040, 360, (40, 150, 220), 0.17)], estrelas=40, nebulosa=0.55, seed=10))
    c.marca((968, 52), 54, (54, 80), ancora="lm")
    titulo(c, [("A ESFERA", 118, "w"), ("CHEGA AO TOPO?", 104, "g")], 170)
    k, ox, oy, Hh = 310, 682, 1700, 2.6
    p = g.Pista(k, ox, oy)
    c.pista(p, Hh, 1.12, larg=12, brilho=16, esmaece=True)
    cx, cy, r = c.corpo_loop(p, 2.55, 1.5)
    c.dimensao(70, oy - Hh * k, oy)
    c.tra((70, oy - Hh * k), (600, oy - Hh * k), VI)
    c.texto((330, oy - Hh * k - 110), "h = ?", fnt("bold", 130), VI, brilho=8)
    # tangente no ângulo 2,55 rad: em coordenadas de tela é (cos θ, −sin θ) = esquerda e para cima
    dx, dy = np.cos(2.55), -np.sin(2.55)
    c.seta((cx + dx * (r + 8), cy + dy * (r + 8)), (cx + dx * (r + 190), cy + dy * (r + 190)), CY, larg=9,
           cabeca=36, brilho=10)
    c.texto((cx + dx * (r + 215), cy + dy * (r + 215) - 40), "v", fnt("medium", 54), CY, brilho=4)
    c.esfera(cx, cy, r, marca=-30, brilho=14)
    salvar(c, "capa_v10_chega_ao_topo.png")


# ── V11 — mesmo loop, alturas diferentes ─────────────────────────────────────
def v11():
    bg = fundo(glows=[(180, 760, 680, (20, 120, 200), 0.11), (900, 1560, 700, (160, 60, 200), 0.12)],
               estrelas=20, seed=11)
    c = Tela(bg)
    c.marca((54, 52), 54, (126, 80))
    titulo(c, [("MESMO LOOP.", 130, "w"), ("ALTURAS", 130, "g"), ("DIFERENTES.", 130, "g")], 150)
    k = 170
    pa = g.Pista(k, 567, 1090)
    pb = g.Pista(k, 836, 1760)
    c.pista(pa, 2.5, 1.0, larg=9, brilho=10)
    c.pista(pb, 2.7, 1.0, larg=9, brilho=10)
    ya, yb = 1090 - 2.5 * k, 1760 - 2.7 * k
    xa = pa.p(-g.u_de_H(2.5), 0)[0]
    xb = pb.p(-g.u_de_H(2.7), 0)[0]
    c.tra((40, ya), (1044, ya), CY)
    c.tra((40, yb), (1044, yb), MG)
    c.particula(xa, ya, 11, CY, brilho=9)
    sb = c.corpo_rampa(pb, g.u_de_H(2.7), 1.7)
    c.esfera(sb[0], sb[1], sb[2], marca=-35, brilho=9)
    c.texto((1044, ya - 34), "PARTÍCULA", fnt("inter", 27), CY, ancora="rm", alfa=230, trilha=4)
    c.texto((1044, ya + 80), "2,5R", fnt("bold", 100), CY, ancora="rm", brilho=8)
    c.texto((44, yb - 34), "ESFERA", fnt("inter", 27), MG, ancora="lm", alfa=230, trilha=4)
    c.texto((44, yb + 80), "2,7R", fnt("bold", 100), MG, ancora="lm", brilho=8)
    salvar(c, "capa_v11_alturas_diferentes.png")


# ── V12 — a rotação como causa ───────────────────────────────────────────────
def v12():
    c = Tela(fundo(glows=[(420, 1330, 560, (110, 70, 220), 0.30), (860, 600, 600, (30, 70, 160), 0.10)],
                   estrelas=26, seed=12))
    c.marca((54, 52), 54, (126, 80))
    titulo(c, [("POR QUE A ESFERA", 96, "w"), ("PRECISA DE MAIS", 96, "w"), ("ALTURA?", 140, "g")], 160)
    k, ox, oy = 235, 767, 1700
    p = g.Pista(k, ox, oy)
    c.pista(p, 2.6, 1.15, larg=10, brilho=8, alfa=125)
    for Hh, cor, lab, dy in ((2.7, MG, "2,7R", -44), (2.5, CY, "2,5R", 46)):
        y = oy - Hh * k
        c.tra((40, y), (222, y), cor, alfa=120, larg=3)           # a esfera, em primeiro plano, fica entre os trechos
        c.tra((666, y), (1046, y), cor, alfa=120, larg=3)
        c.texto((1040, y + dy), lab, fnt("bold", 54), cor, ancora="rm", alfa=210)
    cx, cy, r = c.corpo_rampa(p, 1.85, 5.6)
    for a_ in (-50, 130):                                             # duas marcas: a rotação é visível
        a = np.radians(a_)
        c.linha([(cx, cy), (cx + 0.9 * r * np.cos(a), cy + 0.9 * r * np.sin(a))], MG, 16, 0, alfa=255 if a_ < 0 else 120)
    c.esfera(cx, cy, r, marca=-50, brilho=22)
    c.linha([(cx, cy), (cx + 0.9 * r * np.cos(np.radians(130)), cy + 0.9 * r * np.sin(np.radians(130)))], MG, 14, 0, alfa=120)
    t = np.array([0.696, 0.718])
    c.seta((cx + t[0] * (r + 8), cy + t[1] * (r + 8)), (cx + t[0] * (r + 190), cy + t[1] * (r + 190)), CY, larg=11,
           cabeca=40, brilho=10)
    c.texto((cx + t[0] * (r + 215) + 40, cy + t[1] * (r + 215) - 24), "v", fnt("medium", 60), CY, brilho=4)
    c.arco_seta((cx, cy), r + 34, -160, -30, MG, larg=11, cabeca=40, brilho=10)
    c.texto((cx - 20, cy - r - 70), "ω", fnt("interb", 64), MG, brilho=4)
    f = fnt("inter", 28)
    w = c.texto((60, 1660), "TRANSLAÇÃO", f, CY, ancora="lm", alfa=235, trilha=3)
    c.texto((60 + w + 14, 1660), "+", f, WH, ancora="lm", alfa=200)
    c.texto((60 + w + 42, 1660), "ROTAÇÃO", f, MG, ancora="lm", alfa=235, trilha=3)
    salvar(c, "capa_v12_rotacao_causa.png")


def salvar(c, nome):
    OUT.mkdir(parents=True, exist_ok=True)
    c.img.convert("RGB").resize((W, H), Image.LANCZOS).save(OUT / nome, optimize=True)
    print(nome)


NOMES = ["capa_v07_altura_minima.png", "capa_v08_25_ou_27.png", "capa_v09_h_interrogacao.png",
         "capa_v10_chega_ao_topo.png", "capa_v11_alturas_diferentes.png", "capa_v12_rotacao_causa.png"]


def contato():
    tw, th, gap, rot_h = 360, 640, 30, 46
    folha = Image.new("RGB", (3 * tw + 4 * gap, 2 * (th + rot_h) + 3 * gap), (12, 14, 28))
    d = ImageDraw.Draw(folha)
    rot = g.ImageFont.truetype(str(g.INTER["bold"]), 30)
    for i, nome in enumerate(NOMES):
        im = Image.open(OUT / nome).convert("RGB").resize((tw, th), Image.LANCZOS)
        x, y = gap + (i % 3) * (tw + gap), gap + (i // 3) * (th + rot_h + gap)
        folha.paste(im, (x, y))
        d.text((x + tw // 2, y + th + rot_h // 2), f"V{i + 7}", font=rot, fill=(245, 247, 255), anchor="mm")
    folha.save(OUT / "capas_contato_v2.png")


if __name__ == "__main__":
    for fn in (v7, v8, v9, v10, v11, v12):
        fn()
    contato()
    print("capas_contato_v2.png ->", OUT)
