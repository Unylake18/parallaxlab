"""yt_0015 — kit comum: paleta, texto, setas, corpos 2D, pessoa, gráficos F(t), cabeçalho e relógio por quadro.

Copiado/adaptado dos helpers do yt_0013 (não importa entre unidades). Preview silencioso: o tempo de cada âncora vem de
ancoras.json (palavras da narração congelada ÷ 2,7 palavras/s); a cena se estica para a voz depois.
"""
import json
import math
import os
import re
import sys
from pathlib import Path

import numpy as np
from manim import *  # noqa: F401,F403

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[1]
sys.path.insert(0, str(ROOT))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import DISPLAY_FONT, official_text, screen_text  # noqa: E402

config.media_dir = os.environ.get("MEDIA_DIR", str(AQUI / "media"))

# ── paleta (padrão de Mecânica, docs/padrao_video_longo.md §4 + handoff §4) ─────────────────────────────────
WHITE_ = TEXT_COLOR          # #F5F7FF
CYAN = PRIMARY_COLOR         # #35D9FF (só o assunto do próximo vídeo)
MAG = "#EA63FF"              # momento p, P, Δp
VEL = "#9C8CFF"              # velocidade (violeta só da velocidade)
FC = "#5AA2FF"               # força (F, F_x, F_res, N, peso, F12)
STEEL = "#7A8696"
GEO = "#B8C4DA"
DIM = "#8FA3C4"
PANEL = "#0E2A52"
APAGADO = "#6B7788"          # conta errada riscada


def mix(c, w):
    return interpolate_color(ManimColor(c), ManimColor(WHITE_), w).to_hex()


JC = "#9CC7FF"               # impulso J e toda área sob F(t)
T_HL, T_MAIN, T_LAB, T_SMALL = 44, 34, 26, 22
M_MAIN, M_MID, M_REF, M_LAB = 68, 56, 46, 40
FPS = 15
FRAC = 0.02 / FPS            # folga p/ np.arange não criar um quadro extra

SECOES = [s.strip() for s in os.environ.get("SECOES", "").split(",") if s.strip()]
AUDITORIA = os.environ.get("AUDITORIA") == "1"
STILL = float(os.environ["STILL"]) if os.environ.get("STILL") else None   # still num instante (use com -s)

ANC = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]


def dur(aid):
    return ANC[aid]["dur"]


# ── texto e matemática ───────────────────────────────────────────────────────────────────────────────────
def txt(s, size=T_MAIN, color=WHITE_, op=1.0, bold=False, livre=False):
    """Texto editorial: Space Grotesk em CAIXA ALTA (sem ², ×, ≈, ° dentro: isso vai em MathTex)."""
    s = s.upper()
    if size < 20 and not livre:                 # v6 (G4): nada abaixo de 24 px de versal em 1080p
        size = 20
    if bold:
        return official_text(s, DISPLAY_FONT, BOLD, size, oversample=2, color=color).set_opacity(op)
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(op)


def Mc(*pares, size=M_MID, w=None):
    """MathTex em partes coloridas: cada par é (tex, cor|None). Cada parte precisa ser um TeX completo."""
    partes = [p[0] if isinstance(p, tuple) else p for p in pares]
    cores = [p[1] if isinstance(p, tuple) else None for p in pares]
    m = MathTex(*partes, font_size=size, color=WHITE_)
    for sub, c in zip(m.submobjects, cores):
        if c:
            sub.set_color(c)
    if w and m.width > w:
        m.scale_to_fit_width(w)
    return m


def linha(*itens, buff=0.2, size=T_MAIN, color=WHITE_):
    """Linha mista: str vira txt(); mobjects entram como estão."""
    g = VGroup(*[txt(i, size, color) if isinstance(i, str) else i for i in itens]).arrange(RIGHT, buff=buff)
    return g


def P3(x, y):
    return np.array([x, y, 0.0])


def arrow(a, b, color=WHITE_, width=5, z=8, tip=0.2, op=1.0):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    L = np.linalg.norm(b - a)
    if L < 0.03:
        return VMobject()
    if L < 3 * tip:                     # ponta sempre visível
        b = a + (b - a) / L * 3 * tip
    m = Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.45,
              max_stroke_width_to_length_ratio=50)
    return m.set_opacity(op).set_z_index(z)


HEAT = "#FF7A3D"             # explosão / energia interna (único tom quente, como no yt_0014)


def _fundo(w):
    """Cor do fundo misturada com `w` de branco (gradientes sutis dos painéis)."""
    return interpolate_color(ManimColor(BACKGROUND_COLOR), ManimColor(WHITE_), w)


def placa(w, h, centro, op=0.05):
    """Painel no padrão do yt_0014: leve gradiente vertical, borda fina e filete interno (moldura: não conta como visual)."""
    frente = RoundedRectangle(corner_radius=0.14, width=w, height=h).set_stroke(WHITE_, 1.3, opacity=0.26) \
        .set_fill([_fundo(0.09), _fundo(0.035)], opacity=1.0)
    frente.set_sheen_direction(DOWN)
    filete = RoundedRectangle(corner_radius=0.1, width=w - 0.14, height=h - 0.14).set_stroke(WHITE_, 1.0, opacity=0.09) \
        .set_fill(opacity=0)
    g = VGroup(frente, filete).move_to(centro).set_z_index(-2)
    for m in (g, frente, filete):
        m.moldura = True
    return g


def vinheta(c, r, cor, soma=0.11, n=4):
    """Foco de luz muito sutil atrás do visual principal (yt_0014): círculos concêntricos de baixa opacidade."""
    g = VGroup(*[Circle(radius=r * (1 - 0.23 * k)).set_stroke(width=0).set_fill(cor, soma / n) for k in range(n)])
    for m in [g, *g]:
        m.moldura = True
    return g.move_to(np.asarray(c, float)).set_z_index(-4)


def caixa(m, cor=WHITE_, buff=0.2, w=2.5):
    """Caixa de resultado (moldura)."""
    r = SurroundingRectangle(m, color=cor, buff=buff, stroke_width=w, corner_radius=0.1)
    r.moldura = True
    return r


def lab_at(m, a, b, lado=1, gap=0.14):
    """Rótulo ao lado de um segmento a→b (lado=+1: esquerda de a→b; −1: direita), sem encostar nele."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = (b - a) / max(np.linalg.norm(b - a), 1e-6)
    nrm = np.array([-d[1], d[0], 0.0]) * lado
    meia = 0.5 * (abs(nrm[0]) * m.width + abs(nrm[1]) * m.height)
    return m.move_to((a + b) / 2 + nrm * (gap + meia))


class Carro(VGroup):
    """Veículo visto de cima (copiado do yt_0014/vid_0026): rodas, teto, para-brisa, faróis e lanternas, em aço. Construído
    apontando para +x; `ang` gira o corpo."""

    def __init__(self, L, W, cor=GEO, borda=None, ang=0.0):
        super().__init__()
        borda = borda or mix(cor, 0.5)
        k = W / 1.85
        rodas = VGroup(*[RoundedRectangle(corner_radius=0.08 * k, width=0.75 * k, height=0.32 * k)
                         .set_fill("#060A16", 1).set_stroke(borda, 1, opacity=0.5).move_to(P3(sx * L * 0.3, sy * (W / 2 - 0.02 * k)))
                         for sx in (-1, 1) for sy in (-1, 1)])
        halo = RoundedRectangle(corner_radius=W * 0.32, width=L + 0.25 * k, height=W + 0.25 * k) \
            .set_fill(opacity=0).set_stroke(borda, 7, opacity=0.18)
        corpo = RoundedRectangle(corner_radius=W * 0.3, width=L, height=W).set_fill(cor, 0.62).set_stroke(borda, 2.4)
        brilho = Line(P3(-L * 0.36, W * 0.36), P3(L * 0.3, W * 0.36)).set_stroke(WHITE_, 1.5, opacity=0.35)
        teto = RoundedRectangle(corner_radius=W * 0.2, width=L * 0.46, height=W * 0.7).move_to(P3(-L * 0.06, 0)) \
            .set_fill(interpolate_color(ManimColor(cor), ManimColor(BACKGROUND_COLOR), 0.55), 0.95).set_stroke(borda, 1.2, opacity=0.7)
        xf = L * 0.17
        para = Polygon(P3(xf, W * 0.33), P3(xf + L * 0.13, W * 0.4), P3(xf + L * 0.13, -W * 0.4), P3(xf, -W * 0.33)) \
            .set_fill("#081022", 0.95).set_stroke(borda, 1.2, opacity=0.8)
        tras = Polygon(P3(-L * 0.29, W * 0.32), P3(-L * 0.36, W * 0.37), P3(-L * 0.36, -W * 0.37), P3(-L * 0.29, -W * 0.32)) \
            .set_fill("#081022", 0.9).set_stroke(borda, 1, opacity=0.6)
        far = VGroup(*[Ellipse(width=0.22 * k, height=0.34 * k).set_fill("#F2F8FF", 1).set_stroke(width=0)
                       .move_to(P3(L / 2 - 0.12 * k, s * W * 0.32)) for s in (-1, 1)])
        lan = VGroup(*[RoundedRectangle(corner_radius=0.04 * k, width=0.12 * k, height=0.36 * k).set_fill(DIM, 0.9).set_stroke(width=0)
                       .move_to(P3(-L / 2 + 0.08 * k, s * W * 0.32)) for s in (-1, 1)])
        self.add(rodas, halo, corpo, brilho, teto, para, tras, far, lan)
        self.rotate(ang, about_point=ORIGIN)


class Motor:
    """Fase de um movimento em loop presa ao relógio da cena: corre(ω) / para(). fase() vale em qualquer quadro (updaters)."""

    def __init__(self, cena, s0=0.0, w=0.5):
        self.cena, self.s, self.w, self.t0, self.on = cena, s0, w, 0.0, False

    def fase(self):
        if not self.on:
            return self.s
        return self.s + self.w * (self.cena.clk.get_value() - self.t0)

    def corre(self, w=None):
        self.s = self.fase()
        self.w = self.w if w is None else w
        self.t0, self.on = self.cena.clk.get_value(), True

    def para(self):
        self.s = self.fase()
        self.on = False


def risco(m, cor=APAGADO, w=4):
    """Traço reto horizontal sobre um mobject (item riscado), na altura do meio (v6)."""
    return Line(m.get_left() + 0.06 * LEFT, m.get_right() + 0.06 * RIGHT).set_stroke(cor, w).set_z_index(30)


class Corpo(VGroup):
    """Bloco 2D chato: aço, contorno claro e filete interno (sem 3D falso)."""

    def __init__(self, nome, cor, lado, alt=None, size=36):
        super().__init__()
        alt = alt or lado
        self.lado, self.alt = lado, alt
        f = RoundedRectangle(corner_radius=0.04, width=lado, height=alt).set_stroke(mix(cor, 0.5), 2).set_fill(cor, 1.0)
        ins = min(0.07, 0.12 * min(lado, alt))
        filete = RoundedRectangle(corner_radius=0.03, width=max(lado - 2 * ins, 0.02), height=max(alt - 2 * ins, 0.02)) \
            .set_stroke(WHITE_, 1, opacity=0.35).set_fill(opacity=0).move_to(f)
        self.front = f
        self.add(f, filete)
        if nome:
            esc = cor == GEO
            self.lab = MathTex(nome, font_size=size, color=BACKGROUND_COLOR if esc else WHITE_).move_to(f)
            self.add(self.lab)

    def at(self, x, yb):
        self.shift(P3(x, yb + self.alt / 2) - self.front.get_center())
        return self


def bola(r=0.28, cor=STEEL):
    c = Circle(radius=r).set_stroke(mix(cor, 0.5), 2).set_fill(cor, 1.0)
    return VGroup(c, Circle(radius=r * 0.78).set_stroke(WHITE_, 1, opacity=0.3).set_fill(opacity=0)).set_z_index(5)


# ── grade de layout (handoff v3 §2) ───────────────────────────────────────────────────────────────────────────
PALCO = dict(x0=-6.6, x1=0.6, y0=-3.0, y1=2.5, cx=-3.0, cy=-0.25)
CONTA = dict(x0=1.0, x1=6.6, y0=-3.0, y1=2.5, cx=3.8)
PAINEL_W, PAINEL_X, PAINEL_TOPO = 6.2, 3.3, 2.3
LEGENDA_Y = -3.4


def centro(m, y=None):
    """Modo CENTRO: centraliza pela tela inteira (auditado: |x| < 0,1)."""
    m.set_x(0)
    if y is not None:
        m.set_y(y)
    m.modo_centro = True
    return m


def conta(*mobs, topo=2.2, buff=0.42, x0=None):
    """Coluna da CONTA alinhada à esquerda em x = 1,0, a partir do topo."""
    g = VGroup(*mobs).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    g.move_to(P3(0, 0)).align_to(P3(CONTA["x0"] if x0 is None else x0, 0), LEFT).align_to(P3(0, topo), UP)
    return g


def legenda(s, size=T_LAB, color=GEO, x=0.0):            # v6 (G4): legenda em GEO (clara), não DIM
    return txt(s, size, color=color).move_to(P3(x, LEGENDA_Y))


def painel(lado, altura=5.2, topo=PAINEL_TOPO):
    """Quadro de DOIS PAINÉIS (lado = -1 esquerda, +1 direita), topo em y = 2,3."""
    return placa(PAINEL_W, altura, P3(lado * PAINEL_X, topo - altura / 2))


# ── selo DICA (v2) ───────────────────────────────────────────────────────────────────────────────────────────
BLUE_L = "#7FB2FF"


def dica(*linhas, size=22):
    """Cartão PANEL com borda BLUE_L no canto inferior direito: 'DICA' em ciano e a frase em maiúsculas. Cada linha é uma str
    ou uma lista de str/mobjects (símbolos matemáticos entram como MathTex, nunca dentro de txt())."""
    corpo = VGroup()
    for l in linhas:
        corpo.add(txt(l, size) if isinstance(l, str) else linha(*l, buff=0.1, size=size))
    corpo.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    rot = txt("DICA", 17, color=CYAN, bold=True)
    g = VGroup(rot, corpo).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    cx_ = RoundedRectangle(corner_radius=0.12, width=g.width + 0.6, height=g.height + 0.44).set_stroke(BLUE_L, 2) \
        .set_fill(PANEL, 0.97).move_to(g)
    cx_.moldura = True
    return VGroup(cx_, g).set_z_index(35).to_corner(DR, buff=0.32)


def faixas(*partes):
    """Índices de glifos de cada parte de um TeX (para glyph maps sobre o MathTex de string única equivalente)."""
    m = MathTex(*partes)
    out, i = [], 0
    for s in m.submobjects:
        out.append(list(range(i, i + len(s))))
        i += len(s)
    return out


# ── silhueta humana 2D preenchida (cápsulas; nunca linhas) ───────────────────────────────────────────────────
def capsula2d(a, b, r, cor=STEEL, borda=None):
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = max(np.linalg.norm(b - a), 1e-3)
    c = RoundedRectangle(corner_radius=r * 0.999, width=L + 2 * r, height=2 * r).set_stroke(borda or mix(cor, 0.45), 1.5) \
        .set_fill(cor, 1.0)
    c.rotate(math.atan2(*(b - a)[[1, 0]])).move_to((a + b) / 2)
    return c


def silhueta(altura=2.0, cor=STEEL, junta=GEO):
    """Pessoa de pé, de frente, pés em (0, 0): cápsulas para tronco, braços e pernas, cabeça oval e mãos."""
    k = altura / 1.76
    P = lambda x, y: P3(x * k, y * k)
    g = VGroup()
    for s in (1, -1):
        g.add(capsula2d(P(0.1 * s, 0.94), P(0.11 * s, 0.5), 0.07 * k, cor), capsula2d(P(0.11 * s, 0.5), P(0.12 * s, 0.09), 0.052 * k, cor))
        g.add(RoundedRectangle(corner_radius=0.03 * k, width=0.15 * k, height=0.07 * k).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1)
              .move_to(P(0.14 * s, 0.035)))
        g.add(capsula2d(P(0.2 * s, 1.42), P(0.25 * s, 1.13), 0.045 * k, cor), capsula2d(P(0.25 * s, 1.13), P(0.27 * s, 0.88), 0.036 * k, cor))
        g.add(Ellipse(width=0.07 * k, height=0.12 * k).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1).move_to(P(0.275 * s, 0.81)))
    g.add(Ellipse(width=0.32 * k, height=0.2 * k).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1).move_to(P(0, 1.02)))
    g.add(RoundedRectangle(corner_radius=0.1 * k, width=0.38 * k, height=0.42 * k).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1)
          .move_to(P(0, 1.27)))
    g.add(capsula2d(P(0, 1.47), P(0, 1.52), 0.04 * k, cor))
    g.add(Ellipse(width=0.17 * k, height=0.23 * k).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1).move_to(P(0, 1.645)))
    for s in (1, -1):
        for y, x in ((1.42, 0.2), (0.94, 0.1), (0.5, 0.11)):
            g.add(Dot(P(x * s, y), radius=0.032 * k, color=junta).set_z_index(1))
    return g


# ── pulga 2D de perfil, com o par de patas traseiras articulado ──────────────────────────────────────────────
def _ik2(q, pe, L1, L2, dobra=1):
    """IK 2D de dois segmentos: joelho do lado `dobra` (+1 = para cima/trás)."""
    d = min(max(np.linalg.norm(pe - q), 1e-4), 0.999 * (L1 + L2))
    base = math.atan2(*(pe - q)[[1, 0]])
    al = math.acos(max(-1, min(1, (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d))))
    return q + L1 * P3(math.cos(base + dobra * al), math.sin(base + dobra * al))


def pulga(ext=0.0, esc=1.0, cor=STEEL):
    """Pulga de perfil (cabeça à direita), preenchida em aço com contorno GEO; pés em y = 0. Corpo oval achatado, cabeça pequena,
    6 patas (3 do lado de cá, 3 do lado de lá, mais escuras); as traseiras longas, com fêmur grosso. ext = 0 (dobrada) → 1
    (patas traseiras esticadas: o corpo sobe 0,26·esc)."""
    k = esc
    escuro = interpolate_color(ManimColor(cor), ManimColor(BACKGROUND_COLOR), 0.45).to_hex()
    c = P3(0.0, (0.55 + 0.26 * ext) * k)
    g = VGroup()
    for lado, tom, dx in ((-1, escuro, 0.07 * k), (1, cor, 0.0)):          # lado de lá primeiro (atrás do corpo)
        borda = GEO if lado == 1 else escuro
        # traseira: fêmur grosso + tíbia longa + tarso, pé fixo
        q = c + P3(-0.28 * k + dx, -0.16 * k)
        pe = P3(-0.52 * k + dx, 0.0)
        jo = _ik2(q, pe + P3(0, 0.05 * k), 0.42 * k, 0.46 * k, dobra=-1)
        g.add(capsula2d(q, jo, 0.075 * k, tom, borda), capsula2d(jo, pe + P3(0, 0.05 * k), 0.035 * k, tom, borda),
              capsula2d(pe + P3(0, 0.05 * k), pe + P3(0.1 * k, 0.0), 0.022 * k, tom, borda))
        # meio e dianteira
        for hx, fx in ((0.02, 0.12), (0.26, 0.44)):
            qh = c + P3(hx * k + dx, -0.24 * k)
            pf = P3(fx * k + dx, 0.0)
            jm = _ik2(qh, pf, 0.22 * k, 0.3 * k, dobra=1)
            g.add(capsula2d(qh, jm, 0.04 * k, tom, borda), capsula2d(jm, pf, 0.026 * k, tom, borda))
    corpo = Ellipse(width=0.95 * k, height=0.66 * k).set_stroke(GEO, 2).set_fill(cor, 1).rotate(-0.22).move_to(c)
    segs = VGroup(*[Arc(radius=0.34 * k, start_angle=-0.7, angle=1.4, arc_center=c + P3((-0.48 + 0.17 * i) * k, 0.02 * k))
                    .set_stroke(GEO, 1.5, opacity=0.55) for i in range(4)])
    cab = Ellipse(width=0.3 * k, height=0.26 * k).set_stroke(GEO, 2).set_fill(cor, 1).move_to(c + P3(0.5 * k, -0.12 * k))
    olho = Dot(cab.get_center() + P3(0.04 * k, 0.03 * k), radius=0.025 * k, color=BACKGROUND_COLOR)
    ant = Arc(radius=0.12 * k, start_angle=PI * 0.2, angle=PI * 0.45, arc_center=cab.get_center() + P3(-0.04 * k, 0.0)).set_stroke(GEO, 2)
    bico = capsula2d(cab.get_center() + P3(0.1 * k, -0.08 * k), cab.get_center() + P3(0.14 * k, -0.22 * k), 0.015 * k, GEO, GEO)
    g.add(corpo, segs, cab, olho, ant, bico)
    return g


class Pessoa(VGroup):
    """Silhueta: pés em (x, y); `hip` = altura do quadril (u). Reta: hip = 2·COXA; agachada: joelho para a frente."""
    COXA, TRONCO, CAB = 0.60, 0.72, 0.15

    def __init__(self, cor=GEO, esc=1.0, sentido=1):
        super().__init__()
        self.cor, self.esc, self.sen = cor, esc, sentido
        self.segs = [Line(ORIGIN, RIGHT).set_stroke(cor, max(6, 12 * esc)) for _ in range(5)]
        self.cab = Circle(radius=self.CAB * esc).set_stroke(mix(cor, 0.4), 2).set_fill(cor, 1.0)
        self.add(*self.segs, self.cab)
        self.x, self.y, self.hip = 0.0, 0.0, 2 * self.COXA * esc
        self.pose(0.0, 0.0, None)

    def reta(self):
        return 2 * self.COXA * self.esc

    def pose(self, x, y, hip=None):
        e = self.esc
        hip = self.reta() if hip is None else hip
        self.x, self.y, self.hip = x, y, hip
        L = self.COXA * e
        h = min(hip, 2 * L - 1e-3)
        off = math.sqrt(max(L * L - (h / 2) ** 2, 0.0)) * self.sen
        pe, joe, q = P3(x, y), P3(x + off, y + h / 2), P3(x, y + h)
        om = q + P3(0, self.TRONCO * e)
        self.segs[0].put_start_and_end_on(pe, joe)
        self.segs[1].put_start_and_end_on(joe, q)
        self.segs[2].put_start_and_end_on(q, om)
        braco = 0.55 * e
        self.segs[3].put_start_and_end_on(om, om + P3(0.10 * e * self.sen, -braco))
        self.segs[4].put_start_and_end_on(om, om + P3(-0.10 * e * self.sen, -braco))
        self.cab.move_to(om + P3(0, self.CAB * e + 0.12 * e))
        return self


def flash(centro):
    """Flash curto de impacto: anel + raios finos (sem brilho)."""
    g = VGroup(Circle(radius=0.12).set_stroke(WHITE_, 3).move_to(centro))
    for k in range(8):
        a = k * PI / 4
        g.add(Line(centro + 0.16 * P3(math.cos(a), math.sin(a)), centro + 0.34 * P3(math.cos(a), math.sin(a)))
              .set_stroke(WHITE_, 3))
    return g


# ── gráficos F(t) ──────────────────────────────────────────────────────────────────────────────────────────
class Graf:
    """Eixos com mapeamento (t, F) → tela. Origem (x0, y0) no canto inferior esquerdo dos eixos."""

    def __init__(self, x0, y0, w, h, tmax, fmax, rot_y, rot_x=r"t", z=2):
        self.x0, self.y0, self.w, self.h, self.tmax, self.fmax = x0, y0, w, h, tmax, fmax
        eixo_x = Arrow(P3(x0 - 0.1, y0), P3(x0 + w + 0.25, y0), buff=0, color=DIM, stroke_width=3, tip_length=0.16)
        eixo_y = Arrow(P3(x0, y0 - 0.1), P3(x0, y0 + h + 0.25), buff=0, color=DIM, stroke_width=3, tip_length=0.16)
        self.ey = rot_y.next_to(P3(x0, y0 + h + 0.28), UP, buff=0.05) if rot_y is not None else VGroup()
        self.ex = MathTex(rot_x, font_size=34, color=DIM).next_to(P3(x0 + w + 0.28, y0), RIGHT, buff=0.08)
        self.eixos = VGroup(eixo_x, eixo_y, self.ex, self.ey).set_z_index(z)

    def pt(self, t, f):
        return P3(self.x0 + self.w * t / self.tmax, self.y0 + self.h * f / self.fmax)

    def curva(self, fun, t0=0.0, t1=None, n=160, cor=FC, w=5):
        t1 = self.tmax if t1 is None else t1
        ts = np.linspace(t0, t1, n)
        pts = [self.pt(t, min(fun(t), self.fmax * 1.06)) for t in ts]
        return VMobject().set_points_as_corners(pts).set_stroke(cor, w).set_z_index(6)

    def area(self, fun, t0, t1, n=160, op=0.45, cor=JC):
        ts = np.linspace(t0, t1, n)
        pts = [self.pt(t0, 0)] + [self.pt(t, min(fun(t), self.fmax * 1.06)) for t in ts] + [self.pt(t1, 0)]
        return Polygon(*pts).set_stroke(width=0).set_fill(cor, op).set_z_index(3)

    def retangulo(self, t0, t1, f, cor=FC):
        r = Rectangle(width=self.w * (t1 - t0) / self.tmax, height=self.h * f / self.fmax)
        r.move_to((self.pt(t0, 0) + self.pt(t1, f)) / 2).set_stroke(cor, 3).set_fill(opacity=0)
        return DashedVMobject(r, num_dashes=70, dashed_ratio=0.55).set_z_index(7)


def meia_senoide(J, tau, t0=0.0):
    """F(t) = A sen(π (t − t0)/τ) em [t0, t0+τ]; A = π J/(2τ) → área exatamente J."""
    A = math.pi * J / (2 * tau)
    return lambda t: A * math.sin(math.pi * (t - t0) / tau) if t0 <= t <= t0 + tau else 0.0


def area_num(fun, t0, t1, n=20001):
    ts = np.linspace(t0, t1, n)
    ys = np.array([fun(t) for t in ts])
    return float(np.sum((ys[1:] + ys[:-1]) * np.diff(ts)) / 2)


def suave(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


# ── v6: escrita e transformações sem glifo solto nem fantasma (handoff v6, G2/G3) ──────────────────────────────────
_Write = Write
TEXTO = (Text, SingleStringMathTex, MathTex, Tex)


def _texto(m):
    """Só texto/fórmula (ou grupo só de texto)?"""
    if isinstance(m, TEXTO):
        return True
    return isinstance(m, VGroup) and len(m.submobjects) > 0 and all(_texto(s) for s in m.submobjects)


class Revela(Animation):
    """Escrita do v6: os glifos acendem da esquerda para a direita, termo a termo (nunca um traço pela metade nem um glifo
    sozinho parado); o objeto entra inteiro na cena."""

    def __init__(self, m, larg=0.35, **kw):
        kw.pop("lag_ratio", None)
        super().__init__(m, **kw)
        folhas = m.family_members_with_points()
        xs = sorted({round(f.get_center()[0], 2) for f in folhas})
        n = max(1, len(xs) - 1)
        self._f = [(f, f.get_fill_opacity(), f.get_stroke_opacity(), xs.index(round(f.get_center()[0], 2)) / n) for f in folhas]
        self.larg = larg

    def interpolate_mobject(self, alpha):
        w = self.larg
        for f, fo, so, r in self._f:
            u = min(1.0, max(0.0, (alpha * (1 + w) - r) / w))
            f.set_fill(opacity=fo * u)
            f.set_stroke(opacity=so * u)


def Write(m, *a, **kw):                     # noqa: N802  (substitui o Write do Manim só para texto)
    if _texto(m):
        return Revela(m, **{k: v for k, v in kw.items() if k in ("run_time", "rate_func")})
    return _Write(m, *a, **kw)


def _norm(m):
    p = m.points - m.get_center()
    h = max(m.height, m.width, 1e-6)
    return p / h


def _igual(g1, g2):
    if len(g1.points) != len(g2.points) or len(g1.points) == 0:
        return False
    if abs(g1.width / max(g1.height, 1e-6) - g2.width / max(g2.height, 1e-6)) > 0.05:
        return False
    return float(np.max(np.abs(_norm(g1) - _norm(g2)))) < 0.03


class TrocaGlifos(AnimationGroup):
    """Troca de fórmula do v6 (G3): glifos iguais só se deslocam; os que saem apagam na primeira metade e os novos acendem na
    segunda (nunca se sobrepõem, nada se deforma). A cena tira `a` e põe `b` inteiro no fim (Base.play)."""

    def __init__(self, a, b, *mapas, copia=False, run_time=1.2, **kw):
        self.a, self.b, self.copia = a, b, copia
        A = [x.copy() for x in a.family_members_with_points()]
        B = b.family_members_with_points()

        def rel(g, tudo):
            (x0, y0, _), (x1, y1, _) = tudo.get_critical_point(DL), tudo.get_critical_point(UR)
            c = g.get_center()
            return (c[0] - x0) / max(x1 - x0, 1e-6), (c[1] - y0) / max(y1 - y0, 1e-6)
        ra, rb = [rel(g, a) for g in A], [rel(g, b) for g in B]
        cand = sorted((abs(ra[i][0] - rb[j][0]) + 0.5 * abs(ra[i][1] - rb[j][1]), i, j)
                      for i in range(len(A)) for j in range(len(B)) if _igual(A[i], B[j]))
        usados, casados, pares = set(), set(), []
        for _, i, j in cand:                             # v6: casa pela posição relativa na fórmula (o Δ de p₂ não vai para o Δt)
            if i in usados or j in casados:
                continue
            usados.add(i)
            casados.add(j)
            pares.append((i, j))
        anims = [Transform(A[i], B[j].copy(), rate_func=smooth) for i, j in pares]
        sai = [A[i] for i in range(len(A)) if i not in usados]
        entra = [B[j].copy() for j in range(len(B)) if j not in casados]
        anims += [FadeOut(x, rate_func=lambda t: smooth(min(1.0, t / 0.42))) for x in sai]
        anims += [FadeIn(x, rate_func=lambda t: smooth(max(0.0, (t - 0.5) / 0.5))) for x in entra]
        if not anims:
            anims = [Wait(run_time)]
        super().__init__(*anims, run_time=run_time)
        self.pecas = A + entra


def TransformMatchingTex(a, b, *x, **kw):     # noqa: N802
    return TrocaGlifos(a, b, run_time=kw.get("run_time", 1.2))


TransformMatchingShapes = TransformMatchingTex
TransformByGlyphMap = TransformMatchingTex


# ── cena-base: relógio por quadro, âncoras, cabeçalho ──────────────────────────────────────────────────────
class Base(Scene):
    """Todo `play` é quantizado em quadros inteiros e arrasta o relógio `self.clk` (segundos da cena), de modo que
    updaters baseados em `self.clk` ficam exatos quadro a quadro e o número de quadros é determinístico."""
    TITULO = "MECÂNICA · MOMENTO LINEAR E IMPULSO"

    def setup_base(self, cap=None, selo=None, continua=False):
        self._h2_in = []
        self._escrito = {}
        self.camera.background_color = BACKGROUND_COLOR
        self.clk = ValueTracker(0.0)
        self.nq = 0
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3).set_z_index(40)
        self.h1 = txt(self.TITULO, 17, color=DIM, op=0.5, livre=True).to_corner(UL, buff=0.32).set_z_index(40)
        self.h2 = self._sl = None
        self._pend = []
        self.add(self.wm, self.h1)
        self.alvo = 0.0
        self.log = []
        self._aid, self._q0 = None, 0
        if cap:
            self.h2 = txt(cap, 30, op=0.95).next_to(self.h1, DOWN, buff=0.14, aligned_edge=LEFT).set_z_index(40)
            self.add(self.h2)
            if selo:
                self._sl = txt(selo, 20, color=DIM, op=0.85).next_to(self.h2, DOWN, buff=0.12, aligned_edge=LEFT).set_z_index(40)
                self.add(self._sl)
            if not continua:                       # v6 (G1): o capítulo entra em 0,3 s no começo do lote (o anterior já saiu)
                self._h2_in = [(m, m.get_fill_opacity()) for m in (self.h2, self._sl) if m is not None]
                for m, _ in self._h2_in:
                    m.set_opacity(0)

    # tempo ---------------------------------------------------------------------------------------------------
    @property
    def t(self):
        return self.nq / FPS

    def play(self, *anims, run_time=None, **kw):
        if self._pend:
            anims, self._pend = (*anims, *self._pend), []
        self._v6_espera_escrita(anims)
        self._still()
        rt = run_time
        if rt is None:
            rt = max([getattr(a, "run_time", 1.0) for a in anims] or [1.0])
        n = max(1, round(rt * FPS))
        rtq = n / FPS - FRAC
        t0 = self.nq / FPS
        clk = UpdateFromAlphaFunc(self.clk, lambda m, a: m.set_value(t0 + a * n / FPS), rate_func=linear, run_time=rtq)
        if AUDITORIA:
            self._auditar()
            self._registra(n, "anim")
        antes = [m for m in self.mobjects if isinstance(m, MathTex)]
        tops_antes = list(self.mobjects)
        anims = self._v6_antes(anims, rtq)
        if STILL is not None and t0 <= STILL < t0 + n / FPS:      # v6: still no instante exato (no meio da animação)
            from manim.animation.animation import prepare_animation
            from manim.utils.exceptions import EndSceneEarlyException
            todas = [prepare_animation(an) for an in (*anims, clk)]
            for an in todas:
                an.run_time = rtq
            for an in todas:
                an._setup_scene(self)
                an.begin()
            self.add_mobjects_from_animations(todas)
            al = (STILL - t0) / (n / FPS)
            for an in todas:
                an.interpolate(al)
            self.update_mobjects(0)
            self.update_mobjects(0)                   # 2ª passada: quem lê outro updater (régua, setas) pega o valor novo
            raise EndSceneEarlyException()
        super().play(*anims, clk, run_time=rtq, **kw)
        self.nq += n
        self._v6_depois(anims, t0, rtq)
        self._reparar(antes, anims)
        self._remonta(tops_antes, anims)

    def _remonta(self, tops_antes, anims):
        """v6: animar um grupo NOVO feito de partes de um objeto já em cena (ex.: Indicate(VGroup(A.letra, B.letra))) faz o Manim
        desmontar o objeto em pedaços soltos (e o updater dele para de valer). Aqui o objeto volta inteiro."""
        ids_antes = {id(m) for m in tops_antes}
        for w in list(self.mobjects):                 # embrulho novo só de objetos que já estavam soltos na cena: desembrulha
            if type(w) is VGroup and id(w) not in ids_antes and w.submobjects and all(id(x) in ids_antes for x in w.submobjects):
                self.remove(w)
                self.add(*w.submobjects)
        tops = {id(m) for m in self.mobjects}
        sai = set()
        for a in anims:
            if getattr(a, "remover", False) and getattr(a, "mobject", None) is not None:
                sai |= {id(x) for x in a.mobject.get_family()}
        for m in tops_antes:
            if id(m) in tops or m is self.clk or id(m) in sai:
                continue
            fam = m.get_family()[1:]
            if any(id(x) in sai for x in fam):
                continue
            if any(id(x) in tops for x in fam):
                self.consolida(m)

    # v6 ----------------------------------------------------------------------------------------------------------
    def _v6_espera_escrita(self, anims):
        """G2: nada que acabou de ser escrito sai antes de 1,0 s parado na tela (espera o que falta)."""
        esc = getattr(self, "_escrito", None)
        if not esc:
            return
        fim_ = 0.0
        for a in anims:
            if isinstance(a, FadeOut) or (isinstance(a, TrocaGlifos) and not a.copia):
                m = a.a if isinstance(a, TrocaGlifos) else a.mobject
                for x in m.get_family():
                    fim_ = max(fim_, esc.get(id(x), 0.0))
        falta = fim_ + 1.0 - self.nq / FPS
        if fim_ > 0 and falta > 1e-3:
            if AUDITORIA:
                print(f"[escrita] {self.nq / FPS:7.1f}s saída adiada {falta:.2f} s (G2)")
            self.wait(falta)

    def _v6_antes(self, anims, rtq):
        out = []
        for a in anims:
            if isinstance(a, ReplacementTransform) and isinstance(a.mobject, SingleStringMathTex) \
                    and isinstance(a.target_mobject, SingleStringMathTex) and a.mobject.get_tex_string() != a.target_mobject.get_tex_string():
                a = TrocaGlifos(a.mobject, a.target_mobject, run_time=rtq)
            elif AUDITORIA and isinstance(a, Transform) and not isinstance(a, TrocaGlifos) and _texto(a.mobject) \
                    and getattr(a, "target_mobject", None) is not None and _texto(a.target_mobject):
                print(f"[morph] {self.nq / FPS:7.1f}s {type(a).__name__} entre textos")
            if isinstance(a, TrocaGlifos) and not a.copia:
                if a.a in self.mobjects:
                    self.remove(a.a)
                else:
                    opac_rel(a.a, 0.0)
            out.append(a)
        for m, op in getattr(self, "_h2_in", []):        # G1: header do capítulo entra nos primeiros 0,3 s do lote
            out.append(UpdateFromAlphaFunc(m, lambda x, al, op=op: x.set_opacity(op * min(1.0, al * rtq / 0.3))))
        self._h2_in = []
        return out

    def _v6_depois(self, anims, t0, rtq):
        for a in anims:
            if isinstance(a, TrocaGlifos):
                self.remove(*a.pecas)
                if not a.copia:
                    self.remove(a.a)
                self.consolida(a.b)
            elif isinstance(a, Revela):
                for x in a.mobject.get_family():
                    self._escrito[id(x)] = t0 + rtq

    def _legib(self):
        """G4 (AUDITORIA): texto abaixo de 24 px de versal em 1080p ou legenda parada com opacidade < 0,85."""
        t = self.nq / FPS
        fixos = self.fixos()
        vistos = getattr(self, "_legv", set())
        self._legv = vistos

        def walk(m):
            if m in fixos or getattr(m, "moldura", False) or isinstance(m, ImageMobject):
                return
            if isinstance(m, (Text, SingleStringMathTex)):
                fol = m.family_members_with_points()
                if not fol:
                    return
                op = max(f.get_fill_opacity() for f in fol)
                if op < 0.05:
                    return
                px = m.font_size * (1.31 if isinstance(m, Text) else 1.0)
                nome = m.text[:28] if isinstance(m, Text) else m.get_tex_string()[:28]
                if px < 23.5 and ("px", nome) not in vistos:
                    vistos.add(("px", nome))
                    print(f"[legib] {t:7.1f}s PEQUENO {px:4.1f} px '{nome}'")
                if op < 0.84 and ("op", nome) not in vistos:
                    vistos.add(("op", nome))
                    print(f"[legib] {t:7.1f}s APAGADO op={op:.2f} '{nome}'")
                return
            for x in m.submobjects:
                walk(x)
        for top in self.mobjects:
            if top is not self.clk:
                walk(top)

    def _reparar(self, antes, anims=()):
        """v5: animar um VGroup feito de glifos de uma equação que já está na cena (Indicate, Write ou FadeIn de um pedaço) faz o Manim
        quebrar a equação em pedaços soltos no topo da cena. Aqui ela é remontada inteira (nada em dobro, nada solto)."""
        tops = set(id(m) for m in self.mobjects)
        sai = set()                                   # v6: o que uma animação tirou de propósito (FadeOut, Replacement) não volta
        for a in anims:
            if getattr(a, "remover", False) or isinstance(a, ReplacementTransform):
                m = getattr(a, "mobject", None)
                if m is not None:
                    sai |= {id(x) for x in m.get_family()}
        for eq in antes:
            if id(eq) in tops:
                continue
            fam = {id(x) for x in eq.get_family()}
            if fam & sai:
                continue
            embrulho = any(type(m) is VGroup and m.submobjects and all(id(x) in fam for x in m.submobjects) for m in self.mobjects)
            pedaco = any(id(m) in fam for m in self.mobjects)
            if embrulho or pedaco:
                self.consolida(eq)

    def _still(self):
        if STILL is not None and self.nq / FPS >= STILL:
            from manim.utils.exceptions import EndSceneEarlyException
            raise EndSceneEarlyException()

    def wait(self, duration=1.0, *a, **kw):
        if getattr(self, "_h2_in", None):                 # v6 (G1): o capítulo entra mesmo se o lote começa esperando
            return self.play(Wait(duration), run_time=duration)
        self._still()
        n = max(1, round(duration * FPS))
        if AUDITORIA:
            self._auditar()
            self._registra(n, "pausa")
            self._legib()
        rtq = n / FPS - FRAC
        t0 = self.nq / FPS
        super().play(UpdateFromAlphaFunc(self.clk, lambda m, a_: m.set_value(t0 + a_ * n / FPS), rate_func=linear,
                                         run_time=rtq), run_time=rtq)
        self.nq += n

    def ate(self, frac):
        """Espera até a fração `frac` (0–1) da âncora corrente."""
        alvo = self._q0 + frac * (self.alvo - self._q0)
        if alvo - self.nq >= 1:
            self.wait((alvo - self.nq) / FPS)

    def orfaos(self, tag=""):
        """QA v5: mobjects soltos depois de transformações — glifo solto no topo da cena, objeto do topo que também está dentro de
        outro (dobrado) e duas fórmulas iguais no mesmo lugar. Imprime [orfao] (só com AUDITORIA=1)."""
        if not AUDITORIA:
            return
        tops = [m for m in self.mobjects if m is not self.clk]
        dentro = {}
        for m in tops:
            for x in m.get_family()[1:]:
                dentro[id(x)] = m
        t = self.nq / FPS
        for m in tops:
            nome = type(m).__name__
            if id(m) in dentro:
                print(f"[orfao] {t:7.1f}s {tag} {nome} também dentro de {type(dentro[id(m)]).__name__}")
            elif nome in ("VMobjectFromSVGPath", "SVGPathMobject"):
                print(f"[orfao] {t:7.1f}s {tag} glifo solto em ({m.get_center()[0]:+.2f}, {m.get_center()[1]:+.2f}) op={m.get_fill_opacity():.2f}"
                      f" id={id(m)} dono={getattr(m, '_dono', '?')}")
        tx = [m for m in tops if isinstance(m, SingleStringMathTex)]
        for i, a in enumerate(tx):
            for b in tx[i + 1:]:
                if a.get_tex_string() == b.get_tex_string() and np.linalg.norm(a.get_center() - b.get_center()) < 0.05:
                    print(f"[orfao] {t:7.1f}s {tag} fórmula em dobro '{a.get_tex_string()[:30]}'")

    def glifos(self, src, tgt, pares, entra=(), sai=(), extras=(), rt=1.2, mover=()):
        """Transformação glifo a glifo do v5 (sem morph entre glifos diferentes): pares (i, j) viram Transform do glifo i de src no j
        de tgt (glifos iguais → translação); `mover` = pares que só transladam (move_to); `entra` = índices de tgt com FadeIn; `sai` =
        índices de src com FadeOut. No fim, src e os pedaços saem e tgt entra inteiro (sem órfãos)."""
        # v6 (G3): os pares viram TrocaGlifos (iguais só se deslocam; os que saem apagam antes de os novos acenderem)
        self.play(TrocaGlifos(src, tgt, run_time=rt), *extras, run_time=rt)
        self.consolida(tgt)

    def consolida(self, *alvos):
        """Depois de transformações em pedaços: tira do topo da cena tudo o que é pedaço de um alvo (glifos, VGroups-embrulho de
        glifos) e põe os alvos inteiros — nada fica em dobro nem solto."""
        fam = set()
        for a in alvos:
            fam |= {id(x) for x in a.get_family()}
        for m in list(self.mobjects):
            if m in alvos:
                continue
            if id(m) in fam or (isinstance(m, VGroup) and m.submobjects and all(id(x) in fam for x in m.submobjects)):
                self.remove(m)
        self.add(*alvos)

    def an(self, aid):
        """Fecha a âncora anterior (espera o resto da fala) e abre `aid`."""
        self.orfaos(f"antes de {aid}")
        self._fecha()
        self._aid, self._q0 = aid, self.nq
        self.alvo = self.nq + dur(aid) * FPS

    def _fecha(self):
        if self._aid is not None:
            if self.alvo - self.nq >= 1:
                self.wait((self.alvo - self.nq) / FPS)
            self.log.append((self._aid, self._q0 / FPS, dur(self._aid), (self.nq - self._q0) / FPS))
            self._aid = None

    def fim(self, sai=True):
        self._fecha()
        self.orfaos("fim")
        if sai:                                     # v6 (G1): o lote sai inteiro (conteúdo e capítulo) antes do próximo entrar
            fixos = {self.wm, self.h1}
            mobs = [m for m in self.mobjects if m not in fixos and m is not self.clk]
            if mobs:
                self.play(*[FadeOut(m) for m in mobs], run_time=0.3)
                self.remove(*mobs)
        self.log.append(("FIM", self.nq / FPS, 0, 0))

    # cabeçalho -------------------------------------------------------------------------------------------------
    def fixos(self):
        return {self.wm, self.h1, *([self.h2] if self.h2 else []), *([self._sl] if getattr(self, '_sl', None) else [])}

    def secao(self, s, selo=None):
        """Linha 2 do header (e selo da fonte, linha 3): o antigo sai (0,25 s) antes de o novo entrar."""
        velhos = [m for m in (self.h2, getattr(self, "_sl", None)) if m is not None]
        if velhos:
            self.play(*[FadeOut(m) for m in velhos], run_time=0.25)
        self.h2 = self._sl = None
        if not s:
            return
        novo = txt(s, 30, op=0.95).next_to(self.h1, DOWN, buff=0.14, aligned_edge=LEFT).set_z_index(40)
        self.h2 = novo
        self._pend.append(FadeIn(novo))
        if selo:
            self._sl = txt(selo, 20, color=DIM, op=0.85).next_to(novo, DOWN, buff=0.12, aligned_edge=LEFT).set_z_index(40)
            self._pend.append(FadeIn(self._sl))

    def clear(self, *keep, rt=0.6):
        keep = self.fixos() | set(keep)
        mobs = [m for m in self.mobjects if m not in keep and m is not self.clk]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=rt)
        for m in mobs:
            m.clear_updaters()
        self.remove(*mobs)

    def logo(self, largura):
        img = ImageMobject(str(ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"))
        arr = img.get_pixel_array()
        ys, xs = np.nonzero(arr[:, :, 3] > 8)
        return ImageMobject(arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).set_width(largura)

    def hl(self, s, y=3.0, size=T_HL, color=WHITE_, x=0.0, bold=True):
        return txt(s, size, color=color, bold=bold).move_to(P3(x, y))

    def troca(self, old, new, rt=0.5):
        if old is None:
            self.play(FadeIn(new), run_time=rt)
        else:
            self.play(FadeOut(old), FadeIn(new), run_time=rt)
        return new

    # auditoria de sobreposições (AUDITORIA=1) ---------------------------------------------------------------
    def _auditar(self):
        self.update_mobjects(0)
        itens = []

        def op(m):
            vals = []
            for x in m.family_members_with_points():
                try:
                    vals.append(max(x.get_fill_opacity(), x.get_stroke_opacity()))
                except Exception:
                    vals.append(1.0)
            return max(vals) if vals else 0.0

        def walk(m):
            if isinstance(m, ImageMobject):
                return
            if isinstance(m, (Text, SingleStringMathTex)):
                if op(m) > 0.08 and m.width > 0.01:
                    itens.append(m)
                return
            for s in m.submobjects:
                walk(s)

        for top in self.mobjects:
            walk(top)

        def bb(m):
            (x0, y0, _), (x1, y1, _) = m.get_critical_point(DL), m.get_critical_point(UR)
            return x0 + 0.03, y0 + 0.03, x1 - 0.03, y1 - 0.03

        def nome(m):
            return f"'{m.text[:30]}'" if isinstance(m, Text) else f"'{m.get_tex_string()[:30]}'"

        t = self.nq / FPS
        # v6 (QA 2): menor folga entre dois textos por âncora (linhas da mesma coluna, alinhadas à esquerda, não contam)
        if not hasattr(self, "_folga"):
            self._folga = {}
        fixos = self.fixos()
        livres = [m for m in itens if not any(m in f.get_family() for f in fixos)]
        for i, a in enumerate(livres):
            (ax0, ay0, _), (ax1, ay1, _) = a.get_critical_point(DL), a.get_critical_point(UR)
            for b in livres[i + 1:]:
                if a in b.get_family() or b in a.get_family():
                    continue
                (bx0, by0, _), (bx1, by1, _) = b.get_critical_point(DL), b.get_critical_point(UR)
                if abs(ax0 - bx0) < 0.06 and (by1 < ay0 or ay1 < by0):
                    continue
                gx, gy = max(bx0 - ax1, ax0 - bx1), max(by0 - ay1, ay0 - by1)
                g = max(gx, gy)
                if g > 1.0:
                    continue
                k = self._aid or "?"
                if k not in self._folga or g < self._folga[k][0]:
                    self._folga[k] = (g, t, nome(a), nome(b))
        for i, a in enumerate(itens):
            x0, y0, x1, y1 = bb(a)
            if x0 < -7.9 or x1 > 7.9 or y0 < -4.4 or y1 > 4.4:
                print(f"[audit] {t:7.1f}s FORA DO QUADRO {nome(a)}")
            for b in itens[i + 1:]:
                if a in b.get_family() or b in a.get_family():
                    continue
                bx0, by0, bx1, by1 = bb(b)
                w, h = min(x1, bx1) - max(x0, bx0), min(y1, by1) - max(y0, by0)
                if w > 0.03 and h > 0.03:
                    print(f"[audit] {t:7.1f}s SOBREPOSICAO {nome(a)} x {nome(b)} ({w:.2f}x{h:.2f})")

    def dica_entra(self, d):
        self.dica_atual = d
        self.play(FadeIn(d, shift=0.15 * UP), run_time=0.6)

    # auditorias do v3: vazio (metade da tela sem conteúdo), centralização e pausas ------------------------------------
    def _registra(self, n, tipo):
        if not hasattr(self, "_reg"):
            self._reg = []
        self.update_mobjects(0)
        fixos = self.fixos()
        L = R = 0.0
        cent = []
        for top in self.mobjects:
            if top in fixos or top is self.clk or isinstance(top, ImageMobject) and top is self.wm:
                continue
            for m in ([top] if isinstance(top, ImageMobject) else top.family_members_with_points()):
                try:
                    o = max(m.get_fill_opacity(), m.get_stroke_opacity()) if not isinstance(m, ImageMobject) else 1.0
                except Exception:
                    o = 1.0
                if o < 0.08 or m.width < 0.01:
                    continue
                x0, x1 = m.get_left()[0], m.get_right()[0]
                L += max(0.0, min(x1, -0.3) - max(x0, -7.1))
                R += max(0.0, min(x1, 7.1) - max(x0, 0.3))
            if getattr(top, "modo_centro", False):
                cent.append(round(top.get_center()[0], 3))
        self._reg.append((self.nq / FPS, (self.nq + n) / FPS, L > 0.6, R > 0.6, tipo, cent, self._tem_visual(fixos)))

    def _tem_visual(self, fixos):
        """v4: há na tela algum objeto não textual (desenho, gráfico, imagem) além do cabeçalho, molduras e caixas?"""
        achou = [False]

        def walk(m):
            if achou[0] or getattr(m, "moldura", False):
                return
            if isinstance(m, ImageMobject):
                achou[0] = True
                return
            if isinstance(m, (Text, SingleStringMathTex, MathTex)) or isinstance(m, SurroundingRectangle):
                return
            if m.has_points() and m.width > 0.05:
                try:
                    o = max(m.get_fill_opacity(), m.get_stroke_opacity())
                except Exception:
                    o = 1.0
                if o > 0.08:
                    achou[0] = True
                    return
            for s in m.submobjects:
                walk(s)
        for top in self.mobjects:
            if top in fixos or top is self.clk or top is getattr(self, "dica_atual", None):
                continue
            walk(top)
        return achou[0]

    def _auditar_v3(self):
        reg = getattr(self, "_reg", [])
        if not reg:
            return
        for lado, k in (("ESQUERDA", 2), ("DIREITA", 3)):
            ini = None
            for t0, t1, *v in reg + [(reg[-1][1], reg[-1][1], True, True, "fim", [])]:
                vazio = not (v[0] if k == 2 else v[1])
                if vazio and ini is None:
                    ini = t0
                if not vazio and ini is not None:
                    if t0 - ini > 6:
                        print(f"[vazio] {ini:7.1f}–{t0:7.1f} s ({t0 - ini:4.1f} s) metade {lado} vazia")
                    ini = None
        ini = None
        for t0, t1, *v in reg + [(reg[-1][1], reg[-1][1], 1, 1, "anim", [], True)]:
            if not v[-1] and ini is None:
                ini = t0
            if v[-1] and ini is not None:
                if t0 - ini > 2:
                    print(f"[algebra] {ini:7.1f}–{t0:7.1f} s ({t0 - ini:4.1f} s) só texto/álgebra na tela")
                ini = None
        ini, fim_ = None, None
        for t0, t1, L, R, tipo, cent, _ in reg + [(reg[-1][1], reg[-1][1], 1, 1, "anim", [], True)]:
            if tipo == "pausa":
                ini = t0 if ini is None else ini
                fim_ = t1
            else:
                if ini is not None and fim_ - ini > 8:
                    print(f"[pausa] {ini:7.1f}–{fim_:7.1f} s ({fim_ - ini:4.1f} s) sem animação")
                ini = None
        for t0, t1, L, R, tipo, cent, _ in reg:
            for x in cent:
                if abs(x) >= 0.1:
                    print(f"[centro] {t0:7.1f} s objeto de modo CENTRO em x = {x:+.2f}")

    def relatorio(self):
        if AUDITORIA:
            self._auditar_v3()
            for aid, (g, tt, na, nb) in sorted(getattr(self, "_folga", {}).items(), key=lambda x: x[1][1]):
                print(f"[folga] {aid}: {g:+.2f} em {tt:.1f}s entre {na} e {nb}")
        for aid, t0, prev, real in self.log:
            if os.environ.get("ANCORAS") == "1":
                print(f"[an] {aid} {t0:.2f}")
            if aid != "FIM" and real > prev + 0.2:
                print(f"[tempo] {aid}: previsto {prev:.1f} s, real {real:.1f} s (cena mais longa que a fala)")
        print(f"[tempo] total {self.nq / FPS:.1f} s ({self.nq} quadros)")


class Camada(Base):
    """Camadas Manim transparentes (-t) dos trechos Three.js: tempo absoluto do trecho e o mesmo número de quadros do 3D."""

    def setup_base(self, cap=None, selo=None):
        super().setup_base(cap, selo)
        topo = [m for m in (self.h1, self.h2, self._sl) if m is not None]      # faixa escura atrás do header (legível sobre o 3D)
        g = VGroup(*topo)
        self.faixa = Rectangle(width=g.get_right()[0] + 8.0 + 0.45, height=g.height + 0.4).set_stroke(width=0) \
            .set_fill(BACKGROUND_COLOR, 0.55).move_to(g).align_to(P3(-8.0, 0), LEFT).set_z_index(39)
        self.add(self.faixa)

    def fixos(self):
        return super().fixos() | {getattr(self, "faixa", self.wm)}

    def ate_t(self, alvo):
        n = round((alvo - self.nq / FPS) * FPS)
        if n >= 1:
            self.wait(n / FPS)

    def fim_camada(self, T):
        self.ate_t(T)
        total = round(T * FPS)
        print(f"[camada] {self.nq} quadros (3D: {total})" + ("" if self.nq == total else "  <-- DIFERENTE"))


def timeline(nome):
    return json.loads((AQUI / "threejs" / f"timeline_{nome}.json").read_text(encoding="utf-8"))


def projecoes(nome):
    return json.loads((AQUI / "threejs" / f"proj_{nome}.json").read_text(encoding="utf-8"))["ref"]


def opac_rel(m, f):
    """Opacidade relativa: multiplica as opacidades originais de cada parte (preserva vidros, halos e preenchimentos parciais)."""
    if not hasattr(m, "_ops"):
        m._ops = [(x, x.get_fill_opacity(), x.get_stroke_opacity()) for x in m.family_members_with_points()]
    for x, fo, so in m._ops:
        x.set_fill(opacity=fo * f)
        x.set_stroke(opacity=so * f)
    return m


def fixa(m):
    """Cópia parada e opaca de um objeto que se move/apaga por updater (origem de um TransformFromCopy)."""
    c = m.copy()
    for x in c.get_family():
        x.clear_updaters()
    ops = [max(x.get_fill_opacity(), x.get_stroke_opacity()) for x in c.family_members_with_points()]
    if hasattr(c, "_ops"):
        del c._ops
    return opac_rel(c, 1.0 / max(1e-3, max(ops or [1.0])))


def cursor(cena, G, t0, t1, per=4.0, fun=None, cor=WHITE_):
    """Cursor de tempo que varre um gráfico em loop (o PALCO nunca fica parado); com `fun`, um ponto anda sobre a curva."""
    t_ini = cena.clk.get_value()

    def f():
        u = ((cena.clk.get_value() - t_ini) % per) / per
        t = t0 + (t1 - t0) * u
        topo = min(fun(t), G.fmax) if fun is not None else G.fmax        # v6.1: com `fun`, o tracejado só sobe até a curva (não cruza rótulos)
        g = VGroup()
        if G.pt(t, topo)[1] - G.pt(t, 0)[1] > 0.05:
            g.add(DashedLine(G.pt(t, 0), G.pt(t, topo), dash_length=0.08).set_stroke(cor, 1.6, opacity=0.45))
        if fun is not None:
            g.add(Dot(G.pt(t, min(fun(t), G.fmax)), radius=0.08, color=cor))
        return g.set_z_index(8)
    return always_redraw(f)


def rotulo(tex, cor, size=38):
    """Rótulo de vetor do v5: tamanho fixo, nunca gira, contorno de fundo (legível sobre setas e rastro), z = 4 (acima de tudo da cena)."""
    m = MathTex(tex, font_size=size, color=cor)
    m.set_stroke(BACKGROUND_COLOR, width=6, background=True)
    return m.set_z_index(4)


def vet(a, b, cor, w=4, tip=0.18, z=3, minimo=0.9):
    """Vetor do v5: haste 4, opacidade 1, ponta ≤ 35% do comprimento; abaixo de `minimo` não é desenhado."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = np.linalg.norm(b - a)
    if L < minimo or L < 1e-3:
        return VMobject()
    t = min(tip, 0.35 * L)
    m = Arrow(a, b, buff=0, color=cor, stroke_width=w, tip_length=t, max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=50)
    return m.set_z_index(z)


def caixa_de(m):
    (x0, y0, _), (x1, y1, _) = m.get_critical_point(DL), m.get_critical_point(UR)
    return (x0, y0, x1, y1)


def colide(b1, b2, folga=0.1):
    return not (b1[2] + folga <= b2[0] or b2[2] + folga <= b1[0] or b1[3] + folga <= b2[1] or b2[3] + folga <= b1[1])


def seg_caixa(a, b, cx, folga=0.1, n=24):
    """O segmento a→b passa pela caixa (com folga)?"""
    for u in np.linspace(0, 1, n):
        p = a + (b - a) * u
        if cx[0] - folga <= p[0] <= cx[2] + folga and cx[1] - folga <= p[1] <= cx[3] + folga:
            return True
    return False


def coloca(lab, ponta, direcao, ocupados, segmentos=(), gap=0.2):
    """Põe o rótulo além da ponta, no prolongamento (folga `gap`); se colidir com caixas ocupadas ou segmentos, gira ±60°, ±120°.
    Devolve a caixa usada (e a acrescenta a `ocupados`)."""
    d = np.asarray(direcao, float)
    n = np.linalg.norm(d[:2])
    d = d / n if n > 1e-6 else UP
    melhor = None
    for ang in (0, 60, -60, 120, -120, 180):
        a = math.radians(ang)
        u = np.array([d[0] * math.cos(a) - d[1] * math.sin(a), d[0] * math.sin(a) + d[1] * math.cos(a), 0.0])
        meia = 0.5 * (abs(u[0]) * lab.width + abs(u[1]) * lab.height)
        lab.move_to(np.asarray(ponta, float) + u * (gap + meia))
        cx = caixa_de(lab)
        livre = not any(colide(cx, o) for o in ocupados) and not any(seg_caixa(np.asarray(s0), np.asarray(s1), cx, 0.05) for s0, s1 in segmentos)
        if melhor is None:
            melhor = lab.get_center().copy()
        if livre:
            ocupados.append(cx)
            return cx
    lab.move_to(melhor)
    cx = caixa_de(lab)
    ocupados.append(cx)
    return cx
