"""yt_0004 — Lei de Gauss + superposição. Blocos N01–N16, preview sem voz — versão 4 (composição, textos de tela, glyph maps).

Fonte de verdade: narracao.md (V3 + correções pontuais), storyboard.md (direção V3/V4), producao.md e ficha.md desta pasta;
continuidade visual com yt_0001/yt_0002 (paleta, header, watermark, tipografia, helpers de texto).

Problema principal: Griffiths 2.18 (duas esferas +ρ e −ρ). A cavidade deslocada é generalização do Parallax Lab.
Sem Blender (solido_3d: nenhum): toda a geometria é 2D/2.5D em Manim.

Áreas da tela (V4): título/pergunta na faixa superior (abaixo da marca); geometria à esquerda (≈55%); legenda compacta no canto
superior direito; álgebra no centro da coluna direita (um "slot": o resultado substitui o desenvolvimento); observação curta
abaixo da equação. Rótulos em tipografia matemática normal (sem contorno).

Gramática visual: azul = distribuição +ρ · magenta = −ρ / esfera fictícia · ciano = E⃗ (finos = parciais, grosso = total) ·
violeta tracejado = superfície gaussiana · vetores posição na cor da esfera de origem · branco = d⃗ e P · anel branco = marcador
de percurso (NÃO é P). Escala: uma para distâncias (vetores posição) e outra, comum a parciais e total, para a intensidade do
campo (E⃗ = K·C·r⃗ na tela). O zoom (View) multiplica as duas.

Preview:  uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_0004_gauss_superposicao/cena.py GaussSuperposicao004
SO=5 (ou SO=5,6) renderiza só esses blocos (os outros rodam sem gerar quadros). GUIAS=1 mostra a safe area.
"""

import math
import os
import sys
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from manim import (
    BOLD, DOWN, LEFT, PI, RIGHT, UP, Arrow, Circle, Create, DashedLine, DashedVMobject, Dot, Ellipse, FadeIn,
    FadeOut, ImageMobject, Indicate, LaggedStart, Line, MathTex, Polygon, ReplacementTransform, Rotate, Scene,
    SurroundingRectangle, TexTemplate, Transform, TransformMatchingTex, ValueTracker, VGroup, VMobject, always_redraw, config,
    linear,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import DISPLAY_FONT, official_text, screen_text  # noqa: E402
from template.layout_horizontal import GUIAS, safe_guides  # noqa: E402
from MF_Tools import TransformByGlyphMap  # noqa: E402

SO = {int(s) for s in os.environ.get("SO", "").split(",") if s.strip()}
SLACK = 6.0     # folga máxima de espera por marco editorial (s): evita tela parada; a voz fixa o ritmo depois

# ── Paleta ──────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # E⃗
BLUE = "#267BFF"          # distribuição +ρ (preenchimento)
BLUE_L = "#7FB2FF"        # contorno +ρ, r⃗₊
MAG = "#EA63FF"           # distribuição −ρ / esfera fictícia
MAG_L = "#F3A4FF"         # contorno −ρ, r⃗₋
VIOLET = "#9C8CFF"        # superfície gaussiana
NHAT = "#267BFF"          # normal unitária n̂
AUX_OP = 0.85
HEADER = "ELETROMAGNETISMO · LEI DE GAUSS"
WM_W, WM_OP = 1.92, 0.45

# ── Áreas da tela (frame lógico 16 × 9; safe |x| ≤ 7,2) ─────────────────────
GEO_L, GEO_R = -7.0, 0.7            # geometria: ≈ 55% da largura útil
RL, COLW = 1.5, 5.7                 # coluna de análise: ≈ 40% (início, largura)
AX = RL + COLW / 2                  # centro horizontal da coluna de análise
TITLE_Y = 3.2                       # faixa superior, abaixo da marca
LEG_Y0, LEG_DY = 2.55, 0.4          # legenda compacta (canto superior direito)
EQ_Y = -0.3                         # slot da álgebra (centro da coluna)
OBS_Y = -1.7                        # observação abaixo da equação

T_TITLE, T_BODY, T_NOTE, T_LEG = 36, 28, 24, 20
M_L, M_M, M_S, M_LEG = 50, 40, 30, 26
LX = -3.75                          # centro da geometria (par de esferas)
MY = -0.2

CANCEL = TexTemplate()
CANCEL.add_to_preamble(r"\usepackage{cancel}")

# ── Geometria do problema (Griffiths 2.18) ──────────────────────────────────
R = 2.0                             # raio das duas esferas
DV = np.array([1.3, 0.4, 0.0])      # d⃗: de O₊ para O₋
K = 0.55                            # tela: comprimento de E⃗ por unidade de r⃗ (C = 1); comum a parciais e total
GC = np.array([LX, MY, 0.0])        # centro do par de esferas
OP_ = GC - DV / 2                   # O₊
OM_ = GC + DV / 2                   # O₋
P0 = GC + np.array([0.2, 1.0, 0.0])
# trajetória de P dentro da região comum (relativa a GC)
WAY = [np.array(v) for v in ((0.2, 1.0, 0), (-0.46, -0.66, 0), (0.73, -0.6, 0), (-0.13, 0.13, 0), (0.2, 1.0, 0))]
# pontos esparsos dentro da região comum (para mostrar o campo uniforme)
LENS_PTS = [np.array(v) for v in ((0.0, 0.0, 0), (0.25, 1.0, 0), (-0.5, -0.7, 0), (0.7, -0.55, 0), (-0.45, 0.55, 0), (0.55, 0.5, 0), (0.05, -0.9, 0))]
ZS, ZC = 1.6, np.array([-3.3, -0.55, 0.0])   # zoom da figura do primeiro problema (escala, centro na tela)

# ── Cavidade (generalização do Parallax Lab) ────────────────────────────────
RB, RA = 2.45, 1.3                  # raio externo R e raio da cavidade a
CB = np.array([LX, MY - 0.2, 0.0])  # centro da esfera grande
DM0, DA0 = 0.9, 20.0                # |d⃗| e ângulo (graus) iniciais
KC = 0.65                           # escala de campo da figura da cavidade (comum a parciais e total)
CZS, CZC = 1.35, np.array([-3.2, -0.45, 0.0])  # zoom da cavidade


def U(deg):
    a = math.radians(deg)
    return np.array([math.cos(a), math.sin(a), 0.0])


def cc_of(dm, da):
    return CB + dm * U(da)


def e_sph(x, c, sgn):
    """Campo (C = 1) de uma esfera uniforme de raio R: linear dentro, 1/r² fora."""
    r = x - c
    rr = float(np.linalg.norm(r))
    if rr < 1e-9:
        return np.zeros(3)
    return sgn * (r if rr <= R else R ** 3 * r / rr ** 3)


def e_tot(x):
    return e_sph(x, OP_, 1) + e_sph(x, OM_, -1)


CUP_PTS = [np.array(v) for v in ((-0.5, 0.2, 0), (0.3, 0.55, 0), (0.2, -0.45, 0), (-0.35, -0.5, 0))]
WAYC = [np.array(v) for v in ((-0.3, 0.45, 0), (0.45, -0.35, 0), (-0.55, -0.45, 0), (0.4, 0.55, 0), (-0.3, 0.45, 0))]  # relativos a CC


def _checagem_numerica():
    """Domínios, sinais, soma vetorial, invariância da resultante e estrita internalidade da cavidade (C = 1)."""
    rng = np.random.default_rng(1)
    n = 0
    for _ in range(6000):
        p = GC + np.append(rng.uniform(-3, 3, 2), 0.0)
        if np.linalg.norm(p - OP_) < R and np.linalg.norm(p - OM_) < R:
            rp, rm = p - OP_, p - OM_
            assert np.allclose(rp, DV + rm)                    # r₊ = d + r₋
            assert np.allclose(rp - rm, DV)                    # r₊ − r₋ = d
            assert np.allclose(rp + (-rm), DV)                 # somar o oposto de r₋ na ponta de r₊ leva a O₋
            assert np.allclose(e_tot(p), DV)                   # E = C r₊ − C r₋ = C d
            n += 1
    assert n > 500
    for w in WAY:
        p = GC + w
        assert np.linalg.norm(p - OP_) < R - 0.12 and np.linalg.norm(p - OM_) < R - 0.12
    for w in LENS_PTS:
        p = GC + w
        assert np.linalg.norm(p - OP_) < R - 0.3 and np.linalg.norm(p - OM_) < R - 0.3
        assert np.allclose(e_tot(p), DV)
    p1 = P0 + P(0.6, -0.45)
    assert np.linalg.norm(p1 - OP_) < R - 0.12 and np.linalg.norm(p1 - OM_) < R - 0.12
    p, q = GC + WAY[0], GC + WAY[2]
    assert np.allclose(e_tot(q) - e_tot(p), 0.0)               # Δr₊ = Δr₋ ⇒ ΔE = 0
    assert np.allclose(-e_tot(p), -DV)                         # troca de sinais inverte o campo
    assert RA + DM0 < RB
    for dm, ta in ((DM0, RA), (0.0, RA), (1.1, RA), (DM0, 0.8), (DM0, 1.45)):
        assert ta + dm < RB, (dm, ta)                          # a + |d| < R, estritamente
    for da in (DA0, 100.0, 200.0):
        cc = cc_of(DM0, da)
        for o in WAYC + CUP_PTS:
            w = cc + o
            assert np.linalg.norm(w - cc) < RA - 0.25 and np.linalg.norm(w - CB) < RB
            assert np.allclose((w - CB) - (w - cc), cc - CB)   # E1 + E2 = C d (r = d + r')
            assert np.allclose(w - CB, (cc - CB) + (w - cc))
    print(f"checagem numérica ok ({n} pontos aleatórios na região comum)")


# ── Texto e matemática ──────────────────────────────────────────────────────
@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def text(content, size=24, color=WHITE, opacity=1.0):
    with wide_pango():
        t = screen_text(content, size)
    return t.set_color(color).set_opacity(opacity)


def display(content, size=36, color=WHITE, bold=False):
    with wide_pango():
        t = official_text(content, DISPLAY_FONT, BOLD, size, oversample=2) if bold else screen_text(content, size, oversample=2)
    return t.set_color(color)


def eq(*parts, size=44, color=WHITE, colors=None, cancel=False):
    kw = {"tex_template": CANCEL} if cancel else {}
    m = MathTex(*parts, font_size=size, color=color, **kw)
    for i, c in (colors or {}).items():
        m[i].set_color(c)
    return m


def body(content, color=WHITE, op=1.0):
    return text(content, T_BODY, color, op)


def note(content, color=WHITE, op=0.92):
    return text(content, T_NOTE, color, op)


def small(content, color=WHITE, op=0.92):
    return text(content, T_LEG, color, op)


def lines(*strs, size=T_BODY, color=WHITE, op=1.0, gap=0.14):
    return VGroup(*[text(s, size, color, op) for s in strs]).arrange(DOWN, buff=gap, aligned_edge=LEFT)


def hchain(*items, buff=0.18):
    return VGroup(*items).arrange(RIGHT, buff=buff)


def mix(*parts, size=T_NOTE, color=WHITE, op=0.92, buff=0.12):
    """Linha de texto e símbolos: str vira texto da série; MathTex entra como está."""
    return hchain(*[text(p, size, color, op) if isinstance(p, str) else p for p in parts], buff=buff)


def stack(*rows, gap=0.16, align=LEFT):
    return VGroup(*rows).arrange(DOWN, buff=gap, aligned_edge=align)


def P(x, y):
    return np.array([x, y, 0.0])


def unit(v):
    n = float(np.linalg.norm(v))
    return v / n if n > 1e-9 else np.array([1.0, 0.0, 0.0])


def perp(v, s=1.0):
    u = unit(v)
    return s * np.array([-u[1], u[0], 0.0])


def fit(m, w=COLW):
    """Reduz m se passar da largura w (nunca amplia)."""
    if m.width > w:
        m.scale(w / m.width)
    return m


def in_ana(m, y, left=False):
    """Coloca m na coluna de análise (centralizado, ou alinhado à esquerda), reduzindo se passar da largura."""
    fit(m)
    m.move_to(P(AX, y))
    if left:
        m.align_to(P(RL, 0), LEFT)
    return m


def box(m, color=WHITE, buff=0.24):
    return SurroundingRectangle(m, color=color, buff=buff, corner_radius=0.1, stroke_width=2.0)


def vec(p0, p1, color=CYAN, w=5, op=1.0, z=3):
    d = float(np.linalg.norm(p1 - p0))
    if d < 0.04 or op < 0.01:
        return Arrow(p0, p0 + 0.06 * RIGHT, buff=0, stroke_width=1, tip_length=0.03, color=color).set_opacity(0).set_z_index(z)
    return Arrow(p0, p1, buff=0, stroke_width=w, tip_length=min(0.2, 0.42 * d), max_tip_length_to_length_ratio=0.5,
                 max_stroke_width_to_length_ratio=40, color=color).set_opacity(op).set_z_index(z)


def sign(p, minus=False, s=0.075, color=WHITE, w=2.2):
    g = VGroup(Line(p - s * RIGHT, p + s * RIGHT))
    if not minus:
        g.add(Line(p - s * UP, p + s * UP))
    return g.set_stroke(color, w)


def gauss_circle(c, r, w=3.5, op=1.0):
    return DashedVMobject(Circle(radius=r, arc_center=c), num_dashes=max(24, int(16 * r)), dashed_ratio=0.6).set_stroke(VIOLET, w, op)


def equator(c, r, color=BLUE_L, op=0.3):
    """Elipse do equador: sugere o volume da esfera (2.5D) sem mudar a representação."""
    return Ellipse(width=2 * r, height=0.5 * r).move_to(c).set_stroke(color, 2, op).set_fill(opacity=0)


def follow(m, fn):
    m.add_updater(lambda x: x.move_to(fn()))
    return m


def ring():
    """Marcador de percurso: anel branco vazado, distinto de P (ponto cheio)."""
    return Circle(radius=0.15).set_stroke(WHITE, 3.5).set_fill(opacity=0).set_z_index(12)


def leader(p_text, p_obj, op=0.55):
    """Chamada curta: linha fina do rótulo ao objeto."""
    return Line(p_text, p_obj, color=WHITE, stroke_width=1.5, stroke_opacity=op).set_z_index(9)


# ── Distribuições (estáticas, usadas nos blocos de abertura) ────────────────
def marks(c, r, minus):
    """Sinais esquemáticos (não quantitativos) sobre a distribuição."""
    g = VGroup()
    s = 0.62 * r
    for j in range(-4, 5):
        for i in range(-4, 5):
            x, y = s * (i + 0.5 * (j % 2)), s * j * 0.866
            if x * x + y * y < (0.76 * r) ** 2:
                g.add(sign(c + P(x, y), minus))
    return g.set_opacity(0.4).set_z_index(2)


def sph(c, r, minus=False):
    col, col_l = (MAG, MAG_L) if minus else (BLUE, BLUE_L)
    disk = Circle(radius=r, arc_center=c).set_stroke(col_l, 4).set_fill(col, 0.30)
    return VGroup(disk, marks(c, r, minus))


def lens_poly(a, b, r, n=40):
    d = b - a
    dist = float(np.linalg.norm(d))
    phi = math.atan2(d[1], d[0])
    al = math.acos(min(1.0, dist / (2 * r)))
    A = [a + r * P(math.cos(phi + t), math.sin(phi + t)) for t in np.linspace(-al, al, n)]
    B = [b + r * P(math.cos(phi + math.pi + t), math.sin(phi + math.pi + t)) for t in np.linspace(-al, al, n)]
    return Polygon(*A, *B).set_stroke(WHITE, 2.5, 0.6).set_fill(WHITE, 0.10).set_z_index(1)


def make_pair(c0, s=1.0):
    oa, ob, r = c0 - s * DV / 2, c0 + s * DV / 2, s * R
    pos, neg, lens = sph(oa, r, False), sph(ob, r, True), lens_poly(oa, ob, r)
    return SimpleNamespace(pos=pos, neg=neg, lens=lens, all=VGroup(pos, neg, lens))


def field_arrows(c, g, op=1.0, extra=(), off=None, base=22.5):
    """Campo total (real) em 8 pontos da gaussiana de centro c (física) e raio g; escala comum à superfície; desenho deslocado por off."""
    off = np.zeros(3) if off is None else off
    pts = [c + g * U(a) for a in [base + 45 * i for i in range(8)]]
    es = [e_tot(p) for p in pts]
    mx = max(max(float(np.linalg.norm(e)) for e in es), 1e-9)
    out = VGroup(*[vec(p + off, p + off + 0.8 * e / mx, CYAN, 3.5, op=op * 0.95, z=6) for p, e in zip(pts, es)])
    for a in extra:
        p = c + g * U(a)
        e = e_tot(p)
        out.add(vec(p + off, p + off + 0.8 * e / mx, CYAN, 5, op=op, z=7))
        out.add(vec(p + off, p + off + 0.55 * U(a), NHAT, 4, op=op, z=8))
    return out


# ── Vista com zoom e figura dinâmica ────────────────────────────────────────
class View:
    """Mapa física → tela com escala e centro animáveis (zoom da figura inteira)."""

    def __init__(self, o, c, s=1.0):
        self.o = np.asarray(o)
        self.vs, self.vx, self.vy = ValueTracker(s), ValueTracker(c[0]), ValueTracker(c[1])

    def s(self):
        return self.vs.get_value()

    def m(self, p):
        return P(self.vx.get_value(), self.vy.get_value()) + self.s() * (np.asarray(p) - self.o)

    def go(self, s, c):
        return [self.vs.animate.set_value(s), self.vx.animate.set_value(c[0]), self.vy.animate.set_value(c[1])]


def pair_dyn(V, op, lop):
    """As duas distribuições e a região comum, seguindo a vista V. op: intensidade (0–1); lop: intensidade da lente."""
    def disk(Oc, minus):
        col, col_l = (MAG, MAG_L) if minus else (BLUE, BLUE_L)
        return always_redraw(lambda: Circle(radius=R * V.s(), arc_center=V.m(Oc)).set_stroke(col_l, 4, 0.3 * op.get_value() + 0.7 * op.get_value() ** 2)
                             .set_fill(col, 0.30 * op.get_value()))

    ln = always_redraw(lambda: lens_poly(V.m(OP_), V.m(OM_), R * V.s()).set_stroke(WHITE, 2.5, 0.6 * lop.get_value())
                       .set_fill(WHITE, 0.10 * lop.get_value()))
    return [disk(OP_, False), disk(OM_, True), ln]


class Rig:
    """P (trackers, coordenadas físicas) com vetores posição e campos desenhados na vista V.
    Oa, Ob: funções que devolvem os centros (+ e −). E_a = k(P−Oa); E_b = −k(P−Ob); escala de campo k·V.s, comum a todas as setas."""

    def __init__(self, V, Oa, Ob, p0, k=K):
        self.V, self.Oa, self.Ob, self.k = V, Oa, Ob, k
        self.tx, self.ty = ValueTracker(p0[0]), ValueTracker(p0[1])
        self.rv = ValueTracker(1.0)    # visibilidade dos vetores posição
        self.ev = ValueTracker(1.0)    # visibilidade dos campos parciais
        self.tv = ValueTracker(1.0)    # visibilidade do campo total

    def p(self):
        return P(self.tx.get_value(), self.ty.get_value())

    def sp(self):
        return self.V.m(self.p())

    def to(self, p):
        """Animações de P até p (passe run_time ao play)."""
        return [self.tx.animate.set_value(p[0]), self.ty.animate.set_value(p[1])]

    def dEa(self):
        return self.V.s() * self.k * (self.p() - self.Oa())

    def dEb(self):
        return -self.V.s() * self.k * (self.p() - self.Ob())

    def dot(self):
        return follow(Dot(radius=0.08, color=WHITE).set_z_index(10), self.sp)

    def ra(self, w=4.5):
        return always_redraw(lambda: vec(self.V.m(self.Oa()), self.sp(), BLUE_L, w, op=self.rv.get_value(), z=5))

    def rb(self, w=4.5):
        return always_redraw(lambda: vec(self.V.m(self.Ob()), self.sp(), MAG_L, w, op=self.rv.get_value(), z=5))

    def Ea_v(self):
        return always_redraw(lambda: vec(self.sp(), self.sp() + self.dEa(), CYAN, 4, op=0.85 * self.ev.get_value(), z=6))

    def Eb_v(self):
        return always_redraw(lambda: vec(self.sp(), self.sp() + self.dEb(), CYAN, 4, op=0.85 * self.ev.get_value(), z=6))

    def Et_v(self, w=7):
        return always_redraw(lambda: vec(self.sp(), self.sp() + self.dEa() + self.dEb(), CYAN, w, op=self.tv.get_value(), z=7))

    def lab(self, m, kind):
        """Rótulo sem contorno, afastado das linhas e das pontas das setas."""
        def pos():
            p = self.sp()
            if kind == "ra":
                o = self.V.m(self.Oa())
                return (o + p) / 2 + 0.42 * perp(p - o, 1)
            if kind == "rb":
                o = self.V.m(self.Ob())
                return (o + p) / 2 + 0.42 * perp(p - o, -1)
            if kind == "Ea":
                return p + self.dEa() + 0.42 * unit(self.dEa())
            if kind == "Eb":
                return p + self.dEb() + 0.4 * unit(self.dEb()) + 0.35 * perp(self.dEb(), 1)
            if kind == "Et":
                et = self.dEa() + self.dEb()
                return p + et + 0.38 * unit(et) + 0.42 * perp(et, -1)
            return p + P(0.3, 0.32)

        return follow(m.set_z_index(10), pos)


def _texty(m):
    """True se m é só texto/matemática (sem figuras)."""
    from manim import Text
    if isinstance(m, (Text, MathTex)):
        return True
    return isinstance(m, VGroup) and len(m.submobjects) > 0 and all(_texty(x) for x in m.submobjects)


def _overlap(a, b):
    """Caixas envolventes se cruzam."""
    return not (a.get_right()[0] < b.get_left()[0] or b.get_right()[0] < a.get_left()[0]
                or a.get_top()[1] < b.get_bottom()[1] or b.get_top()[1] < a.get_bottom()[1])


class GaussSuperposicao004(Scene):
    def setup(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.T = 0.0
        self.wm = self.tag = None
        self.fase = 1
        self.leg = []           # linhas da legenda compacta

    # ── relógio e seções ────────────────────────────────────────────────────
    def play(self, *anims, **kw):
        """Relógio do preview. Texto que sai e texto que entra no mesmo lugar não se sobrepõem: a saída vem antes da entrada."""
        t0 = self.renderer.time
        fo = [a for a in anims if isinstance(a, FadeOut) and _texty(a.mobject)]
        fi = [a for a in anims if isinstance(a, FadeIn) and _texty(a.mobject)]
        if fo and fi and any(_overlap(o.mobject, i.mobject) for o in fo for i in fi):
            rt = kw.get("run_time", 1.0)
            resto = [a for a in anims if all(a is not i for i in fi)]
            kw1 = {**kw, "run_time": rt * 0.45}
            kw2 = {**kw, "run_time": rt * 0.55}
            super().play(*resto, **kw1)
            super().play(*fi, **kw2)
        else:
            super().play(*anims, **kw)
        self.T += self.renderer.time - t0

    def at(self, t):
        """Marco editorial t (s): espera até ele, no máximo SLACK s por chamada (sem esperas artificiais)."""
        d = min(t - self.T, SLACK)
        if d > 0.03:
            self.wait(d)

    def begin(self, k, name):
        self.next_section(f"{k:02d}_{name}", skip_animations=bool(SO) and k not in SO)

    def fadable(self, keep=()):
        """Mobjects da cena que podem receber FadeOut (com pontos; setas vazias de always_redraw são descartadas)."""
        ms = [m for m in self.mobjects if m is not self.wm and m is not self.tag and all(m is not k for k in keep)]
        vazios = [m for m in ms if not m.family_members_with_points() or any(isinstance(f, Arrow) and not f.has_points() for f in m.get_family())]
        self.remove(*vazios)
        return [m for m in ms if all(m is not v for v in vazios)]

    def wipe(self, rt=0.8, keep=()):
        ms = self.fadable(keep)
        if ms:
            self.play(FadeOut(*ms), run_time=rt)
        self.remove(*ms)

    # ── legenda compacta (canto superior direito): uma definição por vez, a ativa em destaque ──
    def leg_row(self, sym, *desc, x=RL):
        r = hchain(sym, text("—", T_LEG, opacity=0.7), mix(*desc, size=T_LEG, buff=0.1), buff=0.16)
        n = len(self.leg)
        r.move_to(P(0, LEG_Y0 - LEG_DY * n)).align_to(P(x, 0), LEFT)
        return r

    def leg_add(self, sym, *desc, x=RL, extra=()):
        r = self.leg_row(sym, *desc, x=x)
        self.play(*[m.animate.set_opacity(0.55) for m in self.leg], FadeIn(r), *extra, run_time=0.9)
        self.leg.append(r)
        return r

    def leg_clear(self):
        if self.leg:
            self.play(FadeOut(VGroup(*self.leg)), run_time=0.6)
        self.leg = []

    # ── título e observação ─────────────────────────────────────────────────
    def title(self, content, color=WHITE):
        t = body(content, color) if isinstance(content, str) else content
        return t.move_to(P(0, TITLE_Y))

    def obs(self, *rows, dy=0.0):
        g = stack(*rows, gap=0.12) if len(rows) > 1 else rows[0]
        return in_ana(g, OBS_Y + dy)

    def gm(self, A, B, pairs, rt=1.8):
        """Transformação de glifos (MF-Tools): mapa explícito + auto_fade para o restante. A e B: MathTex de string única."""
        self.play(TransformByGlyphMap(A, B, *[(list(a), list(b)) for a, b in pairs], auto_fade=True, run_time=rt))

    def construct(self):
        _checagem_numerica()
        if GUIAS:
            self.add(safe_guides())
        for f in (self.n01, self.n02, self.n03, self.n04, self.n05, self.n06, self.n07, self.n08, self.n09, self.n10,
                  self.n11, self.n12, self.n13, self.n14, self.n15, self.n16):
            f()
        print(f"duração do preview: {self.T:.2f}s")

    def swap(self, old, new, rt=0.8, **kw):
        """Troca um item da área de leitura (slot ou observação): o novo ocupa o lugar do anterior."""
        anims = []
        if old is not None:
            anims.append(FadeOut(old))
        if new is not None:
            anims.append(FadeIn(new, shift=0.08 * DOWN))
        if anims:
            self.play(*anims, run_time=rt, **kw)
        return new

    # ═══ N01 · 0:00–0:35 · pergunta · FOCUS · sem marca/header/watermark ═══
    def n01(self):
        self.begin(1, "pergunta")
        s, c0 = 1.1, P(0, -0.45)
        pair = self.pair = make_pair(c0, s)
        oa, ob = c0 - s * DV / 2, c0 + s * DV / 2
        q1 = self.title("Qual é o campo elétrico na região em comum?")
        lp = eq(r"+\rho", size=M_L, color=BLUE_L).move_to(oa + P(-s * R - 0.6, 0.0))
        ln = eq(r"-\rho", size=M_L, color=MAG_L).move_to(ob + P(s * R + 0.6, 0.0))
        cut = note("Corte de duas distribuições esféricas", op=0.75).move_to(P(0, -3.1))
        pair.pos.shift(3.2 * LEFT)
        pair.neg.shift(3.2 * RIGHT)
        self.add(pair.pos, pair.neg)
        self.play(pair.pos.animate.shift(3.2 * RIGHT), pair.neg.animate.shift(3.2 * LEFT), FadeIn(lp), FadeIn(ln), run_time=2.0)
        self.play(FadeIn(pair.lens), FadeIn(cut), run_time=0.9)
        self.at(4.0)
        self.play(FadeIn(q1, shift=0.1 * DOWN), run_time=1.0)
        self.at(9.0)
        # P: o lugar onde calculamos o campo; as distribuições ficam fixas
        path = [c0 + s * w for w in WAY]
        tp = ValueTracker(0.0)

        def on_path():
            t = min(max(tp.get_value(), 0.0), len(path) - 1 - 1e-9)
            i = int(t)
            f = t - i
            return path[i] * (1 - f) + path[i + 1] * f

        pt = Dot(radius=0.09, color=WHITE).move_to(path[0]).set_z_index(10)
        pl = eq("P", size=M_M).set_z_index(10).move_to(path[0] + P(0.0, 0.42))
        ql = eq(r"\vec E=\,?", size=M_M).set_z_index(10).move_to(path[0] + P(0.8, -0.05))
        self.leg = []
        self.play(FadeIn(pt, scale=1.5), FadeIn(pl), run_time=0.8)
        self.leg_add(eq("P", size=M_LEG), "Ponto de observação", x=4.1, extra=[FadeIn(ql)])
        pt.add_updater(lambda m: m.move_to(on_path()))
        pl.add_updater(lambda m: m.move_to(on_path() + P(0.0, 0.42)))
        ql.add_updater(lambda m: m.move_to(on_path() + P(0.85, -0.05)))
        self.play(tp.animate.set_value(len(path) - 1), run_time=9.0, rate_func=linear)
        self.at(23.0)
        q2 = self.title("Se P mudar, o campo muda?")
        self.play(FadeOut(q1, shift=0.1 * UP), FadeIn(q2, shift=0.1 * DOWN), run_time=0.9)
        self.play(tp.animate.set_value(0.0), run_time=9.0, rate_func=linear)
        pt.clear_updaters()
        pl.clear_updaters()
        ql.clear_updaters()
        self.remove(pair.pos, pair.neg, pair.lens)
        self.add(pair.all)
        self.ex = [lp, ln, pt, ql, pl, q2, cut] + list(self.leg)
        self.leg = []
        self.at(35.0)

    # ═══ N02 · 0:35–0:45 · intro humana ═══
    def n02(self):
        self.begin(2, "intro")
        pair = self.pair
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(WM_W).set_opacity(WM_OP).to_corner(UP + RIGHT, buff=0.3)
        self.tag = text(HEADER, 18, opacity=0.6).to_corner(UP + LEFT, buff=0.38)
        brand = text("PARALLAX LAB", 22, opacity=0.8).move_to(P(0, 2.05))
        bt = display("LEI DE GAUSS", 58, bold=True).move_to(P(0, 1.25))
        sub = text("Superposição", 26, opacity=0.85).move_to(P(0, 0.45))
        self.play(*[FadeOut(m) for m in self.ex], pair.all.animate.scale(0.45).move_to(P(0, -1.8)).set_opacity(0.3), run_time=1.1)
        self.play(FadeIn(brand, shift=0.1 * DOWN), FadeIn(bt, shift=0.15 * DOWN), FadeIn(sub), FadeIn(self.wm), run_time=1.0)
        self.at(42.0)
        alvo = make_pair(GC, 1.0).all
        self.play(FadeOut(VGroup(brand, bt, sub)), FadeIn(self.tag), Transform(pair.all, alvo), run_time=1.3)
        self.at(45.0)

    # ═══ N03 · 0:45–1:50 · Gauss válida, E direto não ═══
    def n03(self):
        self.begin(3, "conflito")
        pair = self.pair
        SH = P(0.9, 0.0)                    # a figura desloca-se à direita para os rótulos A e B caberem
        p0 = eq(r"\oint_S\vec E\cdot d\vec A=\frac{Q_{\mathrm{env}}}{\varepsilon_0}", size=M_M)
        in_ana(p0, 1.35)
        b0 = box(p0)
        c1 = stack(mix("Para escrever", eq(r"\Phi=E\cdot", size=M_S), "Área(S)"), note("nesta superfície, E precisa ser"),
                   note("perpendicular a S e ter o mesmo"), note("módulo em todos os seus pontos."))
        in_ana(c1, -0.4)
        self.at(46.0)
        self.play(pair.all.animate.shift(SH), FadeIn(p0, shift=0.1 * DOWN), Create(b0), run_time=1.4)
        self.play(FadeIn(c1), run_time=1.0)
        self.at(58.0)
        self.play(FadeOut(VGroup(p0, b0, c1)), run_time=0.7)
        tcx, tcy, tr, ta = ValueTracker(OP_[0]), ValueTracker(OP_[1]), ValueTracker(2.5), ValueTracker(0.0)

        def cen():
            return P(tcx.get_value(), tcy.get_value())

        self.fase = 1
        surf = always_redraw(lambda: gauss_circle(cen() + SH, tr.get_value()))
        arr = always_redraw(lambda: field_arrows(cen(), tr.get_value(), ta.get_value(), extra=(0, 180) if self.fase == 1 else (), off=SH))
        # 1 · centrada em O₊
        s0 = gauss_circle(OP_ + SH, 2.5)
        self.play(Create(s0), run_time=1.6)
        self.remove(s0)
        self.add(surf, arr)
        t1 = mix("Gaussiana centrada em", eq("O_+", size=M_S), size=T_NOTE)
        in_ana(t1, 1.6)
        w1 = note("A esfera negativa quebra a simetria")
        in_ana(w1, 0.9)
        dA = Dot(OP_ + SH + 2.5 * U(0), radius=0.07, color=CYAN).set_z_index(9)
        dB = Dot(OP_ + SH + 2.5 * U(180), radius=0.07, color=CYAN).set_z_index(9)
        lA = eq("A", size=M_M, color=CYAN).move_to(OP_ + SH + 3.55 * U(0))
        lB = eq("B", size=M_M, color=CYAN).move_to(OP_ + SH + 3.55 * U(180))
        self.play(ta.animate.set_value(1.0), FadeIn(t1), FadeIn(w1), FadeIn(dA), FadeIn(dB), FadeIn(lA), FadeIn(lB), run_time=1.4)
        self.at(66.0)
        n1 = stack(note("Em A e B, o campo tem", CYAN, 0.95), note("valor e ângulo diferentes", CYAN, 0.95))
        in_ana(n1, 0.0)
        ineq = eq(r"\oint_S\vec E\cdot d\vec A\neq E\cdot\text{Área}(S)", size=M_M)
        in_ana(ineq, -1.1)
        self.play(FadeIn(n1), run_time=0.8)
        self.at(70.0)
        self.play(FadeIn(ineq, shift=0.1 * DOWN), run_time=0.9)
        self.at(74.0)
        # 2 · centrada em O₋
        self.fase = 2
        t2 = mix("Gaussiana centrada em", eq("O_-", size=M_S), size=T_NOTE)
        in_ana(t2, 1.6)
        w2 = note("A esfera positiva quebra a simetria")
        in_ana(w2, 0.9)
        self.play(FadeOut(VGroup(t1, w1, n1, ineq, dA, dB, lA, lB)), tcx.animate.set_value(OM_[0]), tcy.animate.set_value(OM_[1]), run_time=3.0)
        self.play(FadeIn(t2), FadeIn(w2), run_time=0.8)
        self.at(86.0)
        # 3 · envolvendo tudo
        t3 = note("Gaussiana envolvendo tudo")
        in_ana(t3, 1.6)
        w3 = stack(note("E não tem módulo constante"), note("nem é normal à superfície"))
        in_ana(w3, 0.8)
        self.play(FadeOut(VGroup(t2, w2)), tcx.animate.set_value(GC[0]), tcy.animate.set_value(GC[1]), tr.animate.set_value(2.85), run_time=3.0)
        self.play(FadeIn(t3), FadeIn(w3), run_time=0.8)
        self.at(98.0)
        self.play(FadeOut(VGroup(t3, w3)), ta.animate.set_value(0.0), pair.all.animate.shift(-SH), run_time=0.9)
        self.remove(surf, arr)
        p0b = eq(r"\oint_S\vec E\cdot d\vec A=\frac{Q_{\mathrm{env}}}{\varepsilon_0}", size=M_M)
        in_ana(p0b, 1.0)
        b0b = box(p0b)
        ok = body("A Lei de Gauss continua verdadeira", CYAN)
        in_ana(ok, -0.3)
        self.play(FadeIn(p0b, shift=0.1 * DOWN), Create(b0b), run_time=1.0)
        self.play(FadeIn(ok), run_time=0.8)
        self.at(103.0)
        nok = stack(note("Falta a simetria esférica necessária", op=0.95), note("para obter o campo diretamente.", op=0.95))
        in_ana(nok, -1.4)
        self.play(FadeIn(nok, shift=0.1 * UP), run_time=1.0)
        self.at(108.0)
        self.play(FadeOut(VGroup(p0b, b0b, ok, nok)), run_time=0.7)
        self.at(110.0)

    # ═══ N04 · 1:50–2:35 · superposição ═══
    def n04(self):
        self.begin(4, "superposicao")
        pair = self.pair
        xs = [-3.0, -1.2, 0.3, 1.9, 3.4]       # slots: par = + + −
        y = 0.9
        pc, nc = pair.pos.copy(), pair.neg.copy()
        self.add(pc, nc)
        tit = self.title("Decomposição matemática")
        self.play(pair.all.animate.scale(0.45).move_to(P(xs[0], y)), FadeIn(tit),
                  pc.animate.scale(0.45).move_to(P(xs[2], y)), nc.animate.scale(0.45).move_to(P(xs[4], y)), run_time=2.0)
        eqs, plus = eq("=", size=M_M).move_to(P(xs[1], y)), eq("+", size=M_M).move_to(P(xs[3], y))
        self.play(FadeIn(eqs), FadeIn(plus), run_time=0.6)
        self.at(118.0)
        rho = eq(r"\rho_{\mathrm{tot}}", "=", r"\rho_1", "+", r"\rho_2", size=M_M, colors={2: BLUE_L, 4: MAG_L}).move_to(P(-3.0, -1.0))
        imp = eq(r"\Rightarrow", size=M_M).move_to(P(0.2, -1.0))
        ee = eq(r"\vec E_{\mathrm{tot}}", "=", r"\vec E_1", "+", r"\vec E_2", size=M_M, colors={2: BLUE_L, 4: MAG_L}).move_to(P(3.3, -1.0))
        self.play(FadeIn(rho, shift=0.1 * UP), run_time=0.9)
        self.play(Indicate(pc, color=BLUE_L, scale_factor=1.1), Indicate(rho[2], color=BLUE_L), run_time=1.0)
        self.play(Indicate(nc, color=MAG_L, scale_factor=1.1), Indicate(rho[4], color=MAG_L), run_time=1.0)
        self.at(126.0)
        self.play(FadeIn(imp), FadeIn(ee, shift=0.1 * UP), run_time=0.9)
        self.play(Indicate(ee[2], color=BLUE_L), Indicate(ee[4], color=MAG_L), run_time=1.0)
        self.at(136.0)
        seal = hchain(body("Sempre válido"), eq(r"\neq", size=M_M), body("sempre útil")).move_to(P(0, -2.3))
        sbox = box(seal, VIOLET, 0.22)
        self.play(FadeIn(seal), Create(sbox), run_time=1.0)
        self.at(144.0)
        tit2 = self.title("Só ajuda se soubermos o campo de cada parte", CYAN)
        self.play(FadeOut(tit), FadeIn(tit2), Indicate(pc, color=CYAN, scale_factor=1.15), run_time=0.9)
        self.cur_title = tit2
        self.at(151.0)
        # a esfera +ρ conserva identidade e vira o objeto da próxima etapa
        self.S = pc
        self.play(FadeOut(VGroup(pair.all, eqs, plus, nc, rho, imp, ee, seal, sbox)), run_time=0.8)
        self.at(155.0)

    # ═══ N05 · 2:35–4:45 · ferramenta: E⃗ = C r⃗ dentro de uma esfera uniforme ═══
    def n05(self):
        self.begin(5, "campo_esfera")
        S = self.S
        ttl = self.title("Campo dentro de uma esfera com carga uniforme")
        self.play(S.animate.scale(1 / 0.45).move_to(GC), FadeOut(self.cur_title), FadeIn(ttl), run_time=1.4)
        eqt = equator(GC, R)
        self.play(FadeIn(eqt), run_time=0.5)
        # 1 · esfera, raio R, densidade uniforme
        o_dot = Dot(GC, radius=0.06, color=WHITE).set_z_index(8)
        o_lab = eq("O", size=M_S).next_to(o_dot, DOWN, buff=0.15)
        rR = Line(GC, GC + R * U(205), color=BLUE_L, stroke_width=3).set_z_index(7)
        tR = eq("R", size=M_S, color=BLUE_L).move_to(GC + 0.55 * R * U(205) + 0.3 * perp(U(205), 1))
        self.at(160.0)
        self.leg = []
        self.leg_add(eq("R", size=M_LEG, color=BLUE_L), "Raio da esfera", extra=[FadeIn(o_dot), FadeIn(o_lab), Create(rR), FadeIn(tR)])
        e0 = eq(r"\rho=\frac{Q}{V_{\mathrm{esf}}}", size=M_M)
        in_ana(e0, EQ_Y)
        n0 = stack(note("Uniforme: a mesma em todos os pontos"), mix("Unidade:", eq(r"[\rho]=\mathrm{C/m^3}", size=M_S)))
        in_ana(n0, OBS_Y)
        self.play(FadeIn(e0, shift=0.1 * DOWN), run_time=1.0)
        self.play(FadeIn(n0), run_time=0.7)
        self.at(174.0)
        # 2 · P interno, gaussiana (imaginária) e volume envolvido
        rg = ValueTracker(1.1)
        env = always_redraw(lambda: Circle(radius=rg.get_value(), arc_center=GC).set_stroke(width=0).set_fill(VIOLET, 0.2).set_z_index(1))
        gs = always_redraw(lambda: gauss_circle(GC, rg.get_value()).set_z_index(6))
        gse = always_redraw(lambda: equator(GC, rg.get_value(), VIOLET, 0.35).set_z_index(6))
        rl = always_redraw(lambda: Line(GC, GC + rg.get_value() * U(35), color=WHITE, stroke_width=2.5).set_z_index(7))
        pdot = Dot(radius=0.07, color=WHITE).set_z_index(9)
        pdot.add_updater(lambda m: m.move_to(GC + rg.get_value() * U(35)))
        pdot.move_to(GC + rg.get_value() * U(35))
        rtx = eq("r", size=M_S).add_updater(lambda m: m.move_to(GC + rg.get_value() * 0.5 * U(35) + 0.32 * perp(U(35), 1)))
        rtx.move_to(GC + rg.get_value() * 0.5 * U(35) + 0.32 * perp(U(35), 1))
        plb = eq("P", size=M_S).add_updater(lambda m: m.move_to(GC + rg.get_value() * U(35) + P(0.3, 0.28)))
        plb.move_to(GC + rg.get_value() * U(35) + P(0.3, 0.28))
        cond = stack(note("Superfície gaussiana: esfera imaginária,"), note("concêntrica, que passa por P (r < R)"))
        in_ana(cond, OBS_Y)
        self.leg_add(eq("r", size=M_LEG), "Distância de P ao centro", extra=[FadeOut(rR), FadeOut(tR), FadeIn(env), Create(gs), FadeIn(gse), FadeIn(rl), FadeIn(pdot), FadeIn(rtx), FadeIn(plb), FadeOut(n0), FadeIn(cond)])
        self.leg_add(eq("P", size=M_LEG), "Ponto de observação")
        self.at(186.0)
        v1 = eq(r"V_{\mathrm{env}}=\tfrac{4}{3}\pi r^{3}", size=M_M)
        in_ana(v1, EQ_Y)
        nv = note("Só o volume de raio r — não o da esfera inteira")
        in_ana(nv, OBS_Y)
        self.play(FadeOut(e0), FadeIn(v1, shift=0.1 * DOWN), FadeOut(cond), FadeIn(nv), rg.animate.set_value(1.4), run_time=1.5)
        self.play(rg.animate.set_value(1.1), run_time=1.0)
        self.at(198.0)
        q1 = eq(r"Q_{\mathrm{env}}", "=", r"\rho", r"V_{\mathrm{env}}", size=M_M, colors={0: VIOLET, 2: BLUE_L, 3: VIOLET})
        in_ana(q1, EQ_Y)
        self.play(FadeOut(v1), FadeOut(nv), FadeIn(q1, shift=0.1 * DOWN), run_time=1.0)
        q2 = eq(r"Q_{\mathrm{env}}", "=", r"\rho", r"\tfrac{4}{3}\pi r^{3}", size=M_M, colors={0: VIOLET, 2: BLUE_L})
        in_ana(q2, EQ_Y)
        self.at(204.0)
        self.play(TransformMatchingTex(q1, q2), run_time=1.3)
        self.at(210.0)
        # 3 · fluxo: E radial, mesmo módulo, paralelo à normal (a carga envolvida sobe como referência)
        ref = eq(r"Q_{\mathrm{env}}=\rho\,\tfrac{4}{3}\pi r^{3}", size=M_S, color=VIOLET)
        in_ana(ref, 1.0)
        arrs = always_redraw(lambda: VGroup(*[vec(GC + rg.get_value() * U(a), GC + 1.5 * rg.get_value() * U(a), CYAN, 3.5, z=6)
                                              for a in range(35, 395, 72)]))
        nh = always_redraw(lambda: vec(GC + rg.get_value() * U(35) + 0.12 * perp(U(35), 1), GC + (rg.get_value() + 0.45) * U(35) + 0.12 * perp(U(35), 1), NHAT, 4, z=8))
        nhl = eq(r"\hat n", size=M_S, color=NHAT).add_updater(lambda m: m.move_to(GC + (rg.get_value() + 0.8) * U(35) + 0.38 * perp(U(35), 1)))
        nhl.move_to(GC + (rg.get_value() + 0.8) * U(35) + 0.38 * perp(U(35), 1))
        f1 = eq(r"\oint_S\vec E\cdot d\vec A=E\oint_S dA=E\,(4\pi r^{2})", size=M_M)
        in_ana(f1, EQ_Y)
        fn = stack(note("E radial, com o mesmo módulo na gaussiana,"), note("paralelo à normal: E sai da integral"))
        in_ana(fn, OBS_Y)
        self.play(FadeOut(q2), FadeIn(ref), FadeIn(f1, shift=0.1 * DOWN), FadeIn(arrs), FadeIn(nh), FadeIn(nhl), FadeIn(fn), run_time=1.4)
        self.at(224.0)
        # 4 · Gauss, substituição e cancelamento (glyph map)
        g1 = eq(r"E\,(4\pi r^{2})=\frac{Q_{\mathrm{env}}}{\varepsilon_0}", size=M_M)
        in_ana(g1, EQ_Y)
        self.play(FadeOut(f1), FadeOut(fn), FadeIn(g1, shift=0.1 * DOWN), run_time=1.0)
        self.at(230.0)
        g2 = eq(r"E\,(4\pi r^{2})=\frac{4\pi\rho\,r^{3}}{3\varepsilon_0}", size=M_M)
        in_ana(g2, EQ_Y)
        self.play(FadeOut(g1), FadeIn(g2), run_time=1.0)
        self.at(236.0)
        g3 = eq(r"E=\frac{\rho\cdot4\pi r^{2}\cdot r}{3\,\varepsilon_0\cdot4\pi r^{2}}", size=M_M)
        in_ana(g3, EQ_Y)
        self.play(FadeOut(g2), FadeOut(ref), FadeIn(g3, shift=0.1 * DOWN), run_time=1.0)
        self.at(242.0)
        cn = mix("Fatores comuns:", eq(r"4\pi r^{2}", size=M_S, color=VIOLET), "no numerador e no denominador")
        in_ana(cn, OBS_Y)
        for i in (4, 5, 6, 7, 15, 16, 17, 18):
            g3[0][i].set_color(VIOLET)
        self.play(FadeIn(cn), Indicate(VGroup(*[g3[0][i] for i in (4, 5, 6, 7, 15, 16, 17, 18)]), color=VIOLET, scale_factor=1.15), run_time=1.6)
        g4 = eq(r"E=\frac{\rho\,r}{3\,\varepsilon_0}", size=M_M)
        in_ana(g4, EQ_Y)
        self.gm(g3, g4, [([0], [0]), ([1], [1]), ([2], [2]), ([9], [3]), ([10], [4]), ([11], [5]), ([12], [6]), ([13], [7])], rt=2.2)
        cn2 = mix("O", eq(r"r^{3}/r^{2}", size=M_S), "deixa um fator r")
        in_ana(cn2, OBS_Y)
        self.play(FadeOut(cn), FadeIn(cn2), run_time=0.8)
        self.at(254.0)
        # r → 2r: carga envolvida ×8, área ×4, campo ×2
        dbl = eq(r"r\to2r:\;Q_{\mathrm{env}}\times8,\;A\times4,\;E\times2", size=M_S)
        in_ana(dbl, OBS_Y)
        self.play(FadeOut(cn2), run_time=0.4)
        self.play(rg.animate.set_value(0.65), run_time=1.2)
        self.play(FadeIn(dbl), rg.animate.set_value(1.3), run_time=2.4)
        self.play(Indicate(env, color=WHITE), run_time=0.8)
        self.play(rg.animate.set_value(1.1), run_time=1.0)
        self.at(264.0)
        # 5 · forma vetorial
        rhat = vec(GC + 1.1 * U(35), GC + 1.65 * U(35), WHITE, 4, z=8)
        rhl = eq(r"\hat r", size=M_S).move_to(GC + 1.95 * U(35) + 0.38 * perp(U(35), -1))
        rvec = vec(GC, GC + 1.1 * U(35), WHITE, 5, z=8)
        rvl = eq(r"\vec r", size=M_S).move_to(GC + 0.55 * U(35) + 0.34 * perp(U(35), -1))
        ref2 = eq(r"E=\frac{\rho\,r}{3\,\varepsilon_0}", size=M_S)
        in_ana(ref2, 1.0)
        s0 = stack(mix(eq(r"\hat r", size=M_S), "tem tamanho 1 e aponta"), note("do centro para fora"))
        in_ana(s0, OBS_Y)
        s1 = eq(r"\vec E=E\,\hat r", size=M_M)
        in_ana(s1, EQ_Y)
        self.play(FadeOut(VGroup(arrs, nh, nhl, dbl, rl, rtx)), FadeOut(g4), FadeIn(ref2), FadeIn(s1, shift=0.1 * DOWN),
                  FadeIn(rvec), FadeIn(rvl), FadeIn(rhat), FadeIn(rhl), FadeIn(s0), run_time=1.4)
        self.play(Indicate(rhat, color=WHITE), run_time=0.9)
        self.at(272.0)
        s2 = eq(r"\vec E=\frac{\rho}{3\varepsilon_0}\,r\,\hat r", size=M_M)
        in_ana(s2, EQ_Y)
        s2n = note("Substituindo E pelo resultado anterior")
        in_ana(s2n, OBS_Y)
        self.play(FadeOut(s1), FadeOut(ref2), FadeOut(s0), FadeIn(s2, shift=0.1 * DOWN), FadeIn(s2n), run_time=1.2)
        self.at(276.0)
        s3 = eq(r"\vec E=\frac{\rho}{3\varepsilon_0}\,\vec r", size=M_M)
        in_ana(s3, EQ_Y)
        pn = mix(eq(r"r\,\hat r=\vec r", size=M_S), "é o vetor posição de P")
        in_ana(pn, OBS_Y)
        self.play(FadeOut(s2n), FadeIn(pn), Indicate(rvec, color=WHITE), run_time=0.9)
        self.gm(s2, s3, [([0], [0]), ([1], [1]), ([2], [2]), ([3], [3]), ([4], [4]), ([5], [5]), ([6], [6]), ([7], [7]), ([8, 10], [9]), ([9], [8])], rt=2.0)
        self.at(281.0)
        cdef = mix(eq(r"C=\frac{\rho}{3\varepsilon_0}", size=M_S), "(abreviação; não é uma nova carga)")
        in_ana(cdef, OBS_Y)
        self.play(FadeOut(pn), FadeIn(cdef), run_time=0.8)
        s4 = eq(r"\vec E=C\,\vec r", size=M_L)
        in_ana(s4, EQ_Y)
        self.gm(s3, s4, [([0], [0]), ([1], [1]), ([2], [2]), ([3, 4, 5, 6, 7], [3]), ([8], [4]), ([9], [5])], rt=2.0)
        b4 = box(s4)
        self.play(Create(b4), run_time=0.7)
        self.keep5 = [S, eqt, o_dot, o_lab, env, gs, gse, pdot, plb, rvec, rvl, rhat, rhl, ttl]
        self.fin5 = VGroup(s4, b4, cdef)
        self.at(285.0)

    # ═══ N06 · 4:45–5:40 · mapa de centros, P e vetores posição ═══
    def n06(self):
        self.begin(6, "vetores_posicao")
        k = self.keep5
        V = self.V = View(GC, GC, 1.0)
        op, lop = self.op, self.lop = ValueTracker(0.0), ValueTracker(0.0)
        self.dyn = pair_dyn(V, op, lop)
        self.add(*self.dyn)
        ttl = self.title("Centros, ponto de observação e vetores posição")
        self.play(FadeOut(VGroup(*k)), FadeOut(self.fin5), FadeOut(VGroup(*self.leg)), op.animate.set_value(1.0), lop.animate.set_value(1.0),
                  FadeIn(ttl), run_time=1.8)
        self.leg = []
        self.ttl6 = ttl
        # 1 · O₊
        self.at(293.0)
        dop = follow(Dot(radius=0.08, color=WHITE).set_z_index(8), lambda: V.m(OP_))
        lop_ = follow(eq("O_+", size=M_M, color=BLUE_L), lambda: V.m(OP_) + P(-0.5, -0.45))
        self.leg_add(eq("O_+", size=M_LEG, color=BLUE_L), "Centro da distribuição positiva", extra=[FadeIn(dop, scale=1.6), FadeIn(lop_)])
        # 2 · O₋
        self.at(298.0)
        dom = follow(Dot(radius=0.08, color=WHITE).set_z_index(8), lambda: V.m(OM_))
        lom = follow(eq("O_-", size=M_M, color=MAG_L), lambda: V.m(OM_) + P(0.5, -0.45))
        self.leg_add(eq("O_-", size=M_LEG, color=MAG_L), "Centro da distribuição negativa", extra=[FadeIn(dom, scale=1.6), FadeIn(lom)])
        # 3 · d⃗
        self.at(304.0)
        self.dvec = always_redraw(lambda: vec(V.m(OP_), V.m(OM_), WHITE, 4.5, z=6))
        self.dlab = follow(eq(r"\vec d", size=M_M), lambda: (V.m(OP_) + V.m(OM_)) / 2 + 0.48 * perp(DV, -1))
        self.leg_add(eq(r"\vec d", size=M_LEG), "Deslocamento fixo entre os centros", extra=[Create(self.dvec), FadeIn(self.dlab)])
        # 4 · P
        self.at(311.0)
        rig = self.rig = Rig(V, lambda: OP_, lambda: OM_, P0)
        self.pdot = rig.dot()
        self.plab = rig.lab(eq("P", size=M_M), "P")
        self.leg_add(eq("P", size=M_LEG), "Ponto de observação", extra=[FadeIn(self.pdot, scale=1.6), FadeIn(self.plab)])
        self.play(Indicate(self.pdot, color=WHITE, scale_factor=2.5), run_time=0.8)
        # 5 · r⃗₊ e a anatomia da seta
        self.at(319.0)
        self.ra = rig.ra()
        self.lra = rig.lab(eq(r"\vec r_+", size=M_M, color=BLUE_L), "ra")
        sOP = V.m(OP_)
        t_ini = small("Início", op=0.95).move_to(sOP + P(-1.15, -1.0))
        t_fim = small("Ponta", op=0.95).move_to(rig.sp() + P(-1.4, 0.75))
        l_ini, l_fim = leader(sOP + P(-1.15, -0.8), sOP + P(-0.08, -0.06)), leader(rig.sp() + P(-1.0, 0.65), rig.sp() + P(-0.1, 0.05))
        self.leg_add(eq(r"\vec r_+", size=M_LEG, color=BLUE_L), "Posição de P a partir de", eq("O_+", size=M_LEG),
                     extra=[Create(self.ra), FadeIn(self.lra), FadeIn(VGroup(t_ini, t_fim, l_ini, l_fim))])
        self.wait(1.6)
        self.play(FadeOut(VGroup(t_ini, t_fim, l_ini, l_fim)), run_time=0.5)
        # 6 · r⃗₋
        self.at(327.0)
        self.rb = rig.rb()
        self.lrb = rig.lab(eq(r"\vec r_-", size=M_M, color=MAG_L), "rb")
        self.leg_add(eq(r"\vec r_-", size=M_LEG, color=MAG_L), "Posição do mesmo P a partir de", eq("O_-", size=M_LEG),
                     extra=[Create(self.rb), FadeIn(self.lrb)])
        n6 = stack(note("O comprimento é a distância;", CYAN, 0.95), note("a ponta mostra direção e sentido.", CYAN, 0.95))
        in_ana(n6, -0.6)
        self.play(FadeIn(n6), run_time=0.7)
        self.at(331.0)
        self.play(Indicate(self.ra, color=WHITE, scale_factor=1.0), run_time=1.2)
        self.play(Indicate(self.rb, color=WHITE, scale_factor=1.0), run_time=1.2)
        self.play(Indicate(self.pdot, color=WHITE, scale_factor=2.5), run_time=1.0)
        self.at(337.0)
        self.play(FadeOut(n6), run_time=0.4)
        self.dots6 = VGroup(dop, dom, lop_, lom)
        self.at(340.0)

    # ═══ N07 · 5:40–6:55 · soma, vetor oposto e relação central (figura ampliada, contornos recuados) ═══
    def n07(self):
        self.begin(7, "relacao_vetorial")
        V, rig = self.V, self.rig
        mini = make_pair(P(-6.25, 2.3), 0.16).all
        self.play(FadeOut(self.ttl6), *V.go(ZS, ZC), self.op.animate.set_value(0.0), self.lop.animate.set_value(0.0), FadeIn(mini),
                  run_time=3.0)
        sOP, sOM, sP = V.m(OP_), V.m(OM_), rig.sp()
        trav = ring().move_to(sOP)
        ttl = self.title("Soma de vetores")
        n0 = mix("O anel é só um marcador de percurso: não é", eq("P", size=M_S))
        in_ana(n0, OBS_Y)
        e1 = MathTex(r"\vec r_+", "=", r"\vec d", "+", r"\vec r_-", font_size=M_L)
        e1[0].set_color(BLUE_L)
        e1[4].set_color(MAG_L)
        in_ana(e1, EQ_Y)
        self.at(346.0)
        self.play(FadeIn(trav), FadeIn(n0), FadeIn(ttl), run_time=0.7)
        # caminho 1: direto O₊ → P
        hp = vec(sOP, sP, WHITE, 9, op=0.9, z=9)
        self.at(350.0)
        self.play(FadeIn(hp), trav.animate.move_to(sP), FadeIn(e1[0]), run_time=1.8, rate_func=linear)
        self.wait(1.2)
        self.play(FadeOut(hp), trav.animate.move_to(sOP), run_time=1.0)
        # caminho 2: O₊ → O₋ (d⃗) e depois O₋ → P (r⃗₋)
        self.at(358.0)
        hd = vec(sOP, sOM, WHITE, 9, op=0.9, z=9)
        hm = vec(sOM, sP, WHITE, 9, op=0.9, z=9)
        self.play(FadeIn(hd), trav.animate.move_to(sOM), FadeIn(e1[2]), run_time=1.8, rate_func=linear)
        self.wait(0.6)
        self.play(FadeIn(hm), trav.animate.move_to(sP), FadeIn(e1[3]), FadeIn(e1[4]), run_time=1.8, rate_func=linear)
        self.at(368.0)
        # os dois caminhos começam e terminam nos mesmos pontos
        hp2 = vec(sOP, sP, WHITE, 9, op=0.9, z=8)
        sm = note("Somar vetores: o início de um na ponta do outro", CYAN, 0.95)
        in_ana(sm, OBS_Y)
        self.play(FadeIn(hp2), FadeIn(e1[1]), Indicate(self.pdot, color=WHITE, scale_factor=2.2), FadeOut(n0), FadeIn(sm), run_time=1.4)
        self.at(378.0)
        self.play(FadeOut(VGroup(hp2, hd, hm)), run_time=0.6)
        # isolar d⃗ e vetor oposto
        e2 = MathTex(r"\vec r_+", "-", r"\vec r_-", "=", r"\vec d", font_size=M_L)
        e2[0].set_color(BLUE_L)
        e2[2].set_color(MAG_L)
        in_ana(e2, EQ_Y)
        self.play(FadeOut(sm), TransformMatchingTex(e1, e2), run_time=1.8)
        self.at(388.0)
        # −r⃗₋: mesma seta, mesmo comprimento, sentido invertido
        cp = vec(sOM, sP, MAG_L, 5, z=9)
        on = stack(note("Vetor oposto: mesmo comprimento,", op=0.95), note("sentido invertido", op=0.95))
        in_ana(on, OBS_Y)
        self.play(FadeIn(cp), FadeIn(on), run_time=0.6)
        self.play(Rotate(cp, angle=PI, about_point=(sOM + sP) / 2), run_time=2.0)
        self.play(cp.animate.shift(0.3 * perp(sP - sOM, -1)), run_time=0.8)
        lneg = eq(r"-\vec r_-", size=M_M, color=MAG_L).move_to((sOM + sP) / 2 + 1.35 * perp(sP - sOM, -1))
        self.play(FadeIn(lneg), run_time=0.6)
        self.at(398.0)
        # na ponta de r⃗₊: chegamos a O₋
        hp3 = vec(sOP, sP, BLUE_L, 6, z=8)
        d3 = mix("O deslocamento total, de", eq("O_+", size=M_S), "a", eq("O_-", size=M_S), "é", eq(r"\vec d", size=M_S), color=CYAN, op=0.95)
        self.play(FadeIn(hp3), trav.animate.move_to(sOP), run_time=0.4)
        self.play(trav.animate.move_to(sP), run_time=1.4, rate_func=linear)
        self.play(trav.animate.move_to(sOM), FadeOut(on), FadeIn(in_ana(d3, OBS_Y)), run_time=1.4, rate_func=linear)
        b2 = box(e2)
        self.play(Create(b2), Indicate(self.dvec, color=WHITE, scale_factor=1.0), run_time=1.2)
        self.at(410.0)
        self.play(FadeOut(VGroup(trav, cp, lneg, hp3, d3, ttl)), run_time=0.7)
        self.e2, self.b2, self.mini = e2, b2, mini
        self.at(415.0)

    # ═══ N08 · 6:55–7:45 · campos parciais, sentidos e a constante C ═══
    def n08(self):
        self.begin(8, "campos_sinais")
        V, rig = self.V, self.rig
        rel = self.rel = VGroup(self.e2, self.b2)
        ttl = self.title("Contribuições de cada distribuição")
        self.play(rel.animate.scale(0.55).move_to(P(AX, -3.05)), rig.rv.animate.set_value(0.0), FadeOut(VGroup(self.lra, self.lrb)),
                  FadeOut(VGroup(*self.leg)), FadeIn(ttl), run_time=1.2)
        self.leg = []
        self.leg_add(eq(r"\vec r", size=M_LEG, color=BLUE_L), "Comprimento = distância")
        self.leg_add(eq(r"\vec E", size=M_LEG, color=CYAN), "Comprimento = intensidade do campo")
        self.Ea, self.Eb = rig.Ea_v(), rig.Eb_v()
        self.lEa = rig.lab(eq(r"\vec E_+", size=M_M, color=CYAN), "Ea")
        self.lEb = rig.lab(eq(r"\vec E_-", size=M_M, color=CYAN), "Eb")
        sOP, sOM, sP = V.m(OP_), V.m(OM_), rig.sp()
        gd = DashedLine(sOP, sOP + 1.7 * (sP - sOP), color=WHITE, stroke_width=2, stroke_opacity=0.45, dash_length=0.12).set_z_index(2)
        gd2 = DashedLine(sP, sOM, color=WHITE, stroke_width=2, stroke_opacity=0.45, dash_length=0.12).set_z_index(2)
        ea = MathTex(r"\vec E_+", "=", "C", r"\vec r_+", font_size=M_M)
        ea[0].set_color(CYAN)
        ea[3].set_color(BLUE_L)
        in_ana(ea, 0.3)
        eb = MathTex(r"\vec E_-", "=", "-", "C", r"\vec r_-", font_size=M_M)
        eb[0].set_color(CYAN)
        eb[4].set_color(MAG_L)
        in_ana(eb, -0.6)
        self.at(421.0)
        self.play(Create(gd), run_time=1.0)
        self.play(Create(self.Ea), FadeIn(self.lEa), run_time=1.3)
        nea = stack(note("Afasta-se do centro", op=0.95), note("da distribuição positiva", op=0.95))
        in_ana(nea, OBS_Y)
        self.play(FadeIn(ea, shift=0.1 * DOWN), FadeIn(nea), run_time=0.9)
        self.at(432.0)
        cdef = mix(eq(r"C=\frac{\rho}{3\varepsilon_0}", size=M_S), "(abreviação; não é uma nova carga)")
        in_ana(cdef, OBS_Y)
        self.play(FadeOut(nea), FadeIn(cdef), run_time=0.8)
        self.at(438.0)
        neb = stack(note("A carga negativa puxa: o campo aponta", op=0.95), note("para o centro da distribuição negativa", op=0.95))
        in_ana(neb, OBS_Y)
        self.play(Create(gd2), Create(self.Eb), FadeIn(self.lEb), run_time=1.3)
        self.play(FadeOut(cdef), FadeIn(eb, shift=0.1 * DOWN), FadeIn(neb), run_time=0.9)
        self.at(452.0)
        self.play(Indicate(self.Ea, color=WHITE), run_time=0.9)
        self.play(Indicate(self.Eb, color=WHITE), run_time=0.9)
        self.eab4 = VGroup(ea, eb, neb)
        self.gds = VGroup(gd, gd2)
        self.ttl8 = ttl
        self.at(465.0)

    # ═══ N09 · 7:45–8:35 · soma geométrica e resultado ═══
    def n09(self):
        self.begin(9, "soma")
        V, rig = self.V, self.rig
        ttl = self.title("Soma dos campos")
        self.play(FadeOut(self.ttl8), FadeOut(self.gds), FadeOut(VGroup(self.lEa, self.lEb)), FadeOut(VGroup(*self.leg)), FadeIn(ttl),
                  self.rel.animate.scale(1.0 / 0.55 * 0.7).move_to(P(AX, 1.15)), run_time=1.0)
        self.leg = []
        lEt = rig.lab(eq(r"\vec E", size=M_M, color=CYAN), "Et")
        sP = rig.sp()
        cp = vec(sP, sP + rig.dEb(), CYAN, 4, op=0.6, z=5)
        self.add(cp)
        s1 = eq(r"\vec E=\vec E_++\vec E_-", size=M_M, colors={})
        in_ana(s1, EQ_Y)
        nsum = note("Na ponta do primeiro, o início do segundo")
        in_ana(nsum, OBS_Y)
        self.at(470.0)
        self.play(FadeOut(self.eab4), FadeIn(s1, shift=0.1 * DOWN), FadeIn(nsum), run_time=0.9)
        self.play(cp.animate.shift(rig.dEa()), run_time=2.2)
        Et = rig.Et_v()
        self.play(Create(Et), FadeIn(lEt), run_time=1.3)
        self.at(480.0)
        s2 = eq(r"\vec E=C\,\vec r_+-C\,\vec r_-", size=M_M)
        in_ana(s2, EQ_Y)
        self.play(FadeOut(nsum), FadeOut(s1), FadeOut(cp), FadeIn(s2, shift=0.1 * DOWN), run_time=1.3)
        s3 = eq(r"\vec E=C\,(\vec r_+-\vec r_-)", size=M_M)
        in_ana(s3, EQ_Y)
        nf = note("Fator comum C em evidência")
        in_ana(nf, OBS_Y)
        self.at(488.0)
        self.play(FadeIn(nf), run_time=0.6)
        # N09 — fatoração: o segundo C junta-se ao primeiro e o sinal negativo permanece
        self.gm(s2, s3, [([0], [0]), ([1], [1]), ([2], [2]), ([3, 8], [3]), ([4], [5]), ([5], [6]), ([6], [7]), ([7], [8]), ([9], [9]), ([10], [10]), ([11], [11])], rt=2.2)
        s4 = eq(r"\vec E=C\,\vec d", size=M_M)
        in_ana(s4, EQ_Y)
        nr = note("Substituímos o grupo pela relação do quadro acima")
        in_ana(nr, OBS_Y)
        self.at(494.0)
        self.play(FadeOut(nf), FadeIn(nr), Indicate(self.rel, color=WHITE, scale_factor=1.1), Indicate(self.dvec, color=WHITE, scale_factor=1.0), run_time=1.6)
        # N09 — substituição geométrica: o grupo (r₊ − r₋) vira d⃗
        self.gm(s3, s4, [([0], [0]), ([1], [1]), ([2], [2]), ([3], [3]), ([4, 5, 6, 7, 8, 9, 10, 11, 12], [4, 5])], rt=2.2)
        s5 = eq(r"\vec E=\frac{\rho}{3\varepsilon_0}\,\vec d", size=M_M)
        in_ana(s5, EQ_Y)
        self.at(500.0)
        self.gm(s4, s5, [([0], [0]), ([1], [1]), ([2], [2]), ([3], [3, 4, 5, 6, 7]), ([4], [8]), ([5], [9])], rt=1.8)
        b5 = box(s5)
        dref = vec(sP, sP + V.s() * unit(DV), WHITE, 3, op=0.7, z=4)
        nd = stack(note("E tem a direção e o sentido de d", op=0.95), note("(com escalas diferentes)", op=0.95))
        in_ana(nd, OBS_Y)
        self.play(Create(b5), FadeOut(nr), FadeIn(nd), FadeIn(dref), run_time=1.0)
        self.at(506.0)
        nt = stack(mix("Nesta lente", eq(r"\rho_{\mathrm{tot}}=0", size=M_S), "e mesmo assim", eq(r"\vec E\neq0", size=M_S, color=CYAN), color=WHITE))
        in_ana(nt, OBS_Y - 0.0)
        self.play(FadeOut(nd), FadeIn(nt), self.lop.animate.set_value(0.0), run_time=0.9)
        self.play(self.lop.animate.set_value(0.0), run_time=1.0)
        self.Et, self.lEt, self.s5, self.b5, self.nt, self.dref, self.ttl9 = Et, lEt, s5, b5, nt, dref, ttl
        self.at(515.0)

    # ═══ N10 · 8:35–9:30 · mover P (posições, contribuições e resultante em passagens distintas) ═══
    def n10(self):
        self.begin(10, "mover_P")
        V, rig = self.V, self.rig
        res = VGroup(self.s5, self.b5)
        ttl = self.title("Onde está P nesta resposta?")
        self.play(FadeOut(self.ttl9), FadeOut(self.nt), FadeOut(self.rel), FadeOut(self.dref), FadeOut(self.lEt), FadeOut(self.Et), FadeOut(self.dlab),
                  res.animate.move_to(P(AX, 1.0)).scale(0.8), FadeIn(ttl), run_time=1.2)
        gone = stack(note("Sumiu. Vamos conferir movendo P.", CYAN, 0.95), note("As esferas ficam paradas: P é só o lugar", op=0.95), note("onde calculamos o campo.", op=0.95))
        in_ana(gone, -0.7)
        self.at(522.0)
        self.play(FadeIn(gone), run_time=0.8)
        # referência fixa do campo total
        rp = P(AX - 0.8, -2.9)
        rlen = V.s() * K * np.linalg.norm(DV)
        refv = vec(rp, rp + rlen * unit(DV), CYAN, 4, op=0.6, z=2)
        refl = eq(r"\vec E", size=M_S, color=CYAN).move_to(rp + rlen * unit(DV) + 0.45 * unit(DV) + P(0.0, 0.1))
        refn = small("Referência fixa", op=0.8).move_to(rp + P(-1.1, 0.1))
        self.play(FadeIn(refv), FadeIn(refl), FadeIn(refn), run_time=0.8)
        # 1ª passagem: posições (P e vetores posição); campos recolhidos
        self.leg = []
        rig.ev.set_value(0.0)
        rig.tv.set_value(0.0)
        self.at(530.0)
        self.leg_add(eq(r"\vec r_+", size=M_LEG, color=BLUE_L), "Posição de P a partir de", eq("O_+", size=M_LEG),
                     extra=[FadeOut(VGroup(self.Ea, self.Eb)), rig.rv.animate.set_value(1.0)])
        self.leg_add(eq(r"\vec r_-", size=M_LEG, color=MAG_L), "Posição de P a partir de", eq("O_-", size=M_LEG))
        for w in WAY[1:3]:
            self.play(*rig.to(GC + w), run_time=3.0)
            self.wait(0.8)
        self.play(*rig.to(GC + WAY[3]), run_time=3.0)
        self.at(546.0)
        # 2ª passagem: contribuições (campos parciais); posições recolhidas
        self.Ea, self.Eb = rig.Ea_v(), rig.Eb_v()
        self.add(self.Ea, self.Eb)
        self.leg_clear()
        self.leg_add(eq(r"\vec E_+", size=M_LEG, color=CYAN), "Campo da distribuição positiva", extra=[rig.rv.animate.set_value(0.0), rig.ev.animate.set_value(1.0)])
        self.leg_add(eq(r"\vec E_-", size=M_LEG, color=CYAN), "Campo da distribuição negativa")
        for w in (WAY[1], WAY[2]):
            self.play(*rig.to(GC + w), run_time=3.0)
            self.wait(0.6)
        self.at(558.0)
        # 3ª passagem: só a resultante
        self.Et = rig.Et_v()
        self.add(self.Et)
        self.leg_clear()
        self.leg_add(eq(r"\vec E", size=M_LEG, color=CYAN), "Campo total: sempre a mesma seta", extra=[rig.ev.animate.set_value(0.0), rig.tv.animate.set_value(1.0)])
        for w in (WAY[3], WAY[1], WAY[0]):
            self.play(*rig.to(GC + w), run_time=2.4)
            self.wait(0.5)
        self.at(564.0)
        ups = VGroup(*[vec(V.m(GC + w), V.m(GC + w) + rlen * unit(DV), CYAN, 5, op=0.9, z=6) for w in LENS_PTS])
        tx3 = note("Em vários pontos da lente, o mesmo campo", CYAN, 0.95)
        in_ana(tx3, -0.7)
        self.play(FadeOut(gone), FadeOut(VGroup(self.Ea, self.Eb)), FadeOut(self.pdot), FadeOut(self.plab), FadeOut(self.Et), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(a) for a in ups], lag_ratio=0.25), FadeIn(tx3), run_time=3.0)
        self.n10x = VGroup(res, ttl, refv, refl, refn, ups, tx3)
        self.at(570.0)

    # ═══ N11 · 9:30–10:15 · Δ: por que as variações se cancelam ═══
    def n11(self):
        self.begin(11, "delta_E")
        V, rig = self.V, self.rig
        self.leg_clear()
        self.play(FadeOut(self.n10x), run_time=0.7)
        rig.tx.set_value(P0[0])
        rig.ty.set_value(P0[1])
        rig.rv.set_value(1.0)
        rig.ev.set_value(0.0)
        rig.tv.set_value(0.0)
        self.ra, self.rb = rig.ra(), rig.rb()
        self.pdot, self.plab = rig.dot(), rig.lab(eq("P", size=M_M), "P")
        self.add(self.ra, self.rb, self.pdot, self.plab)
        sP0 = V.m(P0)
        sOP, sOM = V.m(OP_), V.m(OM_)
        ghosts = VGroup(vec(sOP, sP0, BLUE_L, 3, op=0.3), vec(sOM, sP0, MAG_L, 3, op=0.3))
        gp = Dot(sP0, radius=0.06, color=WHITE).set_opacity(0.4).set_z_index(9)
        self.add(ghosts, gp)
        ttl = self.title("Variações")
        dd = note("Δ = valor depois menos valor antes", CYAN, 0.95)
        in_ana(dd, 2.0)
        self.play(FadeIn(ttl), FadeIn(dd), run_time=0.8)
        p1 = P0 + P(0.6, -0.45)
        sP1 = V.m(p1)
        self.at(578.0)
        dl = vec(sP0, sP1, WHITE, 6, z=9)
        lP = eq(r"\Delta\vec P", size=M_M).move_to((sP0 + sP1) / 2 + 0.6 * perp(sP1 - sP0, -1))
        self.play(*rig.to(p1), Create(dl), FadeIn(lP), run_time=2.0)
        l1 = eq(r"\Delta\vec r_+=\Delta\vec r_-", size=M_M)
        in_ana(l1, EQ_Y)
        n1 = stack(note("Os dois vetores terminam no novo P;", op=0.95), note("os centros não se mexem.", op=0.95))
        in_ana(n1, OBS_Y)
        self.at(586.0)
        self.play(FadeIn(l1, shift=0.1 * DOWN), FadeIn(n1), run_time=1.2)
        # espaço de comparação: Δr⃗₊ e Δr⃗₋ são o mesmo deslocamento
        ddv = sP1 - sP0
        cx = P(AX, 1.1)
        d1 = vec(sP0, sP1, BLUE_L, 6, z=9)
        d2 = vec(sP0, sP1, MAG_L, 6, z=9)
        lab1 = eq(r"\Delta\vec r_+", size=M_S, color=BLUE_L).move_to(cx + P(-1.9, 0.38))
        lab2 = eq(r"\Delta\vec r_-", size=M_S, color=MAG_L).move_to(cx + P(-1.9, -0.38))
        self.play(d1.animate.shift(cx + P(-0.6, 0.38) - ddv / 2 - sP0), d2.animate.shift(cx + P(-0.6, -0.38) - ddv / 2 - sP0), FadeIn(lab1), FadeIn(lab2), run_time=1.8)
        self.at(596.0)
        # contribuições: C Δr⃗₊ e −C Δr⃗₋ se cancelam
        l2 = eq(r"\Delta\vec E=C\,\Delta\vec r_+-C\,\Delta\vec r_-=0", size=M_M)
        in_ana(l2, EQ_Y)
        n2 = note("As duas parcelas são iguais e de sentidos opostos", op=0.95)
        in_ana(n2, OBS_Y)
        self.play(FadeOut(l1), FadeOut(n1), FadeIn(l2, shift=0.1 * DOWN), FadeIn(n2), run_time=1.1)
        cl = eq(r"C\,\Delta\vec r_+", size=M_S, color=BLUE_L).move_to(cx + P(-1.9, 0.38))
        cl2 = eq(r"-C\,\Delta\vec r_-", size=M_S, color=MAG_L).move_to(cx + P(-1.9, -0.38))
        a1 = vec(cx + P(-0.9, 0.38), cx + P(0.4, 0.38), BLUE_L, 5, z=9)
        a2 = vec(cx + P(0.4, -0.38), cx + P(-0.9, -0.38), MAG_L, 5, z=9)
        self.play(FadeOut(VGroup(d1, d2, lab1, lab2)), FadeIn(VGroup(a1, a2, cl, cl2)), Indicate(l2[0], color=CYAN), run_time=1.6)
        self.wait(1.2)
        fin = body("Cada campo muda. A soma não.", CYAN)
        in_ana(fin, OBS_Y)
        self.at(608.0)
        self.play(FadeOut(n2), FadeIn(fin, shift=0.1 * UP), run_time=0.9)
        self.n11x = VGroup(dl, lP, l2, fin, a1, a2, cl, cl2, dd, ttl, ghosts, gp)
        self.at(615.0)

    # ═══ cavidade: trackers e figura dinâmica ═══
    def cav_setup(self):
        Vc = self.Vc = View(CB, CB, 1.0)
        t = self.ct = SimpleNamespace(dm=ValueTracker(DM0), da=ValueTracker(DA0), ta=ValueTracker(RA), rho=ValueTracker(1.0),
                                      hole=ValueTracker(1.0), fo=ValueTracker(0.0), dv=ValueTracker(0.0), ev=ValueTracker(0.0),
                                      bo=ValueTracker(0.0))

        def cc():
            return cc_of(t.dm.get_value(), t.da.get_value())

        self.cc = cc
        big = always_redraw(lambda: Circle(radius=RB * Vc.s(), arc_center=Vc.m(CB))
                            .set_stroke(MAG_L if t.rho.get_value() < 0 else BLUE_L, 4, t.bo.get_value())
                            .set_fill(MAG if t.rho.get_value() < 0 else BLUE, (0.3 * abs(t.rho.get_value()) + 0.001) * t.bo.get_value()))
        hole = always_redraw(lambda: Circle(radius=t.ta.get_value() * Vc.s(), arc_center=Vc.m(cc()))
                             .set_stroke(WHITE, 3.5, (0.15 + 0.85 * t.hole.get_value()) * t.bo.get_value())
                             .set_fill(BACKGROUND_COLOR, t.hole.get_value() * t.bo.get_value()).set_z_index(4))
        ficf = always_redraw(lambda: Circle(radius=t.ta.get_value() * Vc.s(), arc_center=Vc.m(cc()))
                             .set_stroke(width=0).set_fill(MAG, 0.45 * t.fo.get_value()).set_z_index(3))
        ficd = always_redraw(lambda: gauss_circle(Vc.m(cc()), t.ta.get_value() * Vc.s(), 3.5, t.fo.get_value()).set_color(MAG_L).set_z_index(5))
        dar = always_redraw(lambda: vec(Vc.m(CB), Vc.m(cc()), WHITE, 4.5, op=t.dv.get_value(), z=8))
        ear = always_redraw(lambda: vec(Vc.m(cc()), Vc.m(cc()) + Vc.s() * KC * t.rho.get_value() * (cc() - CB), CYAN, 7,
                                        op=t.ev.get_value(), z=9))
        self.cav_objs = [big, ficf, hole, ficd, dar, ear]
        self.add(*self.cav_objs)

    # ═══ N12 · 10:15–11:20 · segundo problema: a cavidade ═══
    def n12(self):
        self.begin(12, "carga_removida")
        self.leg = []
        self.wipe(1.0)
        self.cav_setup()
        t, Vc = self.ct, self.Vc
        tit = self.title("Segundo problema: uma cavidade", MAG_L)
        self.play(FadeIn(tit, shift=0.1 * DOWN), t.bo.animate.set_value(1.0), run_time=1.6)
        d1 = stack(note("Esfera isolante com densidade"), mix("volumétrica uniforme", eq(r"+\rho", size=M_S, color=BLUE_L), "e uma"),
                   note("cavidade esférica deslocada."))
        in_ana(d1, 1.3)
        q = body("Qual é o campo dentro do buraco?", CYAN)
        in_ana(q, -0.2)
        gn = stack(note("Generalização do Parallax Lab: sem a simetria", MAG_L, 0.95),
                   note("esférica necessária para obter E diretamente", MAG_L, 0.95))
        in_ana(gn, -1.3)
        self.at(623.0)
        self.play(FadeIn(d1), run_time=1.0)
        self.play(FadeIn(q), FadeIn(gn), run_time=1.0)
        self.at(636.0)
        # como reconstruir? esfera cheia + esfera fictícia
        self.play(FadeOut(VGroup(d1, q, gn)), t.hole.animate.set_value(0.0), run_time=1.6)
        self.play(t.fo.animate.set_value(1.0), run_time=1.4)
        lp = eq(r"+\rho", size=M_L, color=BLUE_L).move_to(Vc.m(CB) + P(-RB - 0.55, 0.5))
        lf = eq(r"-\rho", size=M_L, color=MAG_L).move_to(Vc.m(self.cc()) + P(RA + 0.7, 0.9))
        nf = small("Esfera fictícia", MAG_L, 0.95).move_to(P(-0.1, Vc.m(self.cc())[1] - 0.2))
        ninf = note("Esfera cheia", BLUE_L, 0.95)
        in_ana(ninf, 1.5)
        self.play(FadeIn(lp), FadeIn(lf), FadeIn(nf), FadeIn(ninf), run_time=1.0)
        self.at(646.0)
        # densidades: fora e dentro da cavidade
        dens = stack(mix("Fora da cavidade:", eq(r"+\rho", size=M_M, color=BLUE_L), size=T_NOTE),
                     mix("Dentro:", eq(r"+\rho+(-\rho)=0", size=M_M), size=T_NOTE), gap=0.3)
        in_ana(dens, 0.1)
        self.play(FadeOut(ninf), FadeIn(dens, shift=0.1 * DOWN), run_time=1.0)
        self.at(656.0)
        # pares +ρ / −ρ se cancelam, deixando a cavidade
        ccs = Vc.m(self.cc())
        pts = [ccs + 0.6 * RA * Vc.s() * np.array([math.cos(math.radians(a)), math.sin(math.radians(a)), 0]) * (1 if i % 2 else 0.4)
               for i, a in enumerate(range(0, 360, 60))]
        pl_, mn_ = VGroup(), VGroup()
        for p in pts:
            pl_.add(sign(p + 0.14 * LEFT, False, s=0.1, color=BLUE_L, w=3))
            mn_.add(sign(p + 0.14 * RIGHT, True, s=0.1, color=MAG_L, w=3))
        self.play(FadeIn(pl_), FadeIn(mn_), run_time=0.8)
        self.play(*[a.animate.shift(0.14 * RIGHT) for a in pl_], *[b.animate.shift(0.14 * LEFT) for b in mn_], run_time=1.2)
        a_ = stack(note("Remover carga = somar a distribuição oposta"), note("(decomposição matemática: não há carga", op=0.9),
                   note("negativa de verdade no buraco)", op=0.9))
        in_ana(a_, 0.9)
        self.play(FadeOut(pl_), FadeOut(mn_), t.hole.animate.set_value(1.0), t.fo.animate.set_value(0.0), FadeOut(lf), FadeOut(nf), FadeOut(dens),
                  FadeIn(a_), run_time=1.5)
        # esfera com cavidade = cheia + fictícia
        y, sc = -1.2, 0.3
        xs = [RL + 0.7, RL + 1.9, RL + 3.1, RL + 4.3, RL + 5.2]

        def mini(x, cavity=False, fic_=False):
            c0 = P(x, y)
            g = VGroup()
            if not fic_:
                g.add(Circle(radius=RB * sc, arc_center=c0).set_stroke(BLUE_L, 3).set_fill(BLUE, 0.3))
            if cavity:
                g.add(Circle(radius=RA * sc, arc_center=c0 + DM0 * sc * U(DA0)).set_stroke(WHITE, 2.5).set_fill(BACKGROUND_COLOR, 1))
            if fic_:
                g.add(Circle(radius=RA * sc, arc_center=c0 + DM0 * sc * U(DA0)).set_stroke(MAG_L, 3).set_fill(MAG, 0.45))
            return g

        row = VGroup(mini(xs[0], cavity=True), eq("=", size=M_M).move_to(P(xs[1], y)), mini(xs[2]),
                     eq("+", size=M_M).move_to(P(xs[3], y)), mini(xs[4], fic_=True))
        self.at(668.0)
        self.play(FadeIn(row, shift=0.1 * UP), run_time=1.2)
        nk = mix("E já sabemos o campo interno de cada esfera:", eq(r"\vec E=C\,\vec r", size=M_S, color=CYAN), color=CYAN, op=0.95)
        in_ana(nk, -2.3)
        self.play(FadeIn(nk), run_time=0.8)
        self.n12x = VGroup(tit, lp, a_, row, nk)
        self.at(680.0)

    # ═══ N13 · 11:20–12:05 · mapa de variáveis da cavidade ═══
    def n13(self):
        self.begin(13, "cavidade_deslocada")
        t, Vc = self.ct, self.Vc
        ttl = self.title("Mapa de variáveis da cavidade")
        self.play(FadeOut(VGroup(self.n12x[0], self.n12x[2], self.n12x[3], self.n12x[4])), FadeIn(ttl), run_time=0.9)
        cc = self.cc
        self.leg = []
        u_ = lambda: unit(cc() - CB)
        dob = Dot(Vc.m(CB), radius=0.07, color=WHITE).set_z_index(8)
        doc = follow(Dot(radius=0.07, color=WHITE).set_z_index(8), lambda: Vc.m(cc()))
        # R
        segR = Line(Vc.m(CB), Vc.m(CB) + RB * Vc.s() * U(205), color=BLUE_L, stroke_width=3).set_z_index(7)
        tR = eq("R", size=M_M, color=BLUE_L).set_z_index(10).move_to(Vc.m(CB) + 0.5 * RB * Vc.s() * U(205) + 0.42 * perp(U(205), 1))
        self.at(687.0)
        self.leg_add(eq("R", size=M_LEG, color=BLUE_L), "Raio da esfera grande", extra=[FadeIn(dob), Create(segR), FadeIn(tR)])
        # a
        sega = always_redraw(lambda: Line(Vc.m(cc()), Vc.m(cc()) + t.ta.get_value() * Vc.s() * U(115), color=MAG_L, stroke_width=4).set_z_index(8))
        ta_l = follow(eq("a", size=M_M, color=MAG_L).set_z_index(10), lambda: Vc.m(cc()) + 0.5 * t.ta.get_value() * Vc.s() * U(115) + 0.42 * perp(U(115), 1))
        self.at(693.0)
        self.leg_add(eq("a", size=M_LEG, color=MAG_L), "Raio da cavidade", extra=[FadeIn(doc), Create(sega), FadeIn(ta_l)])
        # d⃗
        td = follow(eq(r"\vec d", size=M_M).set_z_index(10), lambda: (Vc.m(CB) + Vc.m(cc())) / 2 + 0.5 * perp(cc() - CB, -1))
        self.at(699.0)
        self.leg_add(eq(r"\vec d", size=M_LEG), "Do centro grande ao da cavidade", extra=[t.dv.animate.set_value(1.0), FadeIn(td)])
        # condição: |d| + a < R, na mesma direção; rótulos fora do desenho, com chamadas
        self.at(705.0)
        far = follow(Dot(radius=0.08, color=MAG_L).set_z_index(9), lambda: Vc.m(CB + (t.dm.get_value() + t.ta.get_value()) * u_()))
        surf = Dot(Vc.m(CB + RB * u_()), radius=0.08, color=BLUE_L).set_z_index(9)
        gap = always_redraw(lambda: Line(Vc.m(CB + (t.dm.get_value() + t.ta.get_value()) * u_()), Vc.m(CB + RB * u_()), color=CYAN, stroke_width=5).set_z_index(9))
        fy = lambda: Vc.m(CB + (t.dm.get_value() + t.ta.get_value()) * u_())[1]
        lfar = follow(eq(r"|\vec d|+a", size=M_S, color=MAG_L).set_z_index(10), lambda: P(0.15, fy() - 0.75))
        lfar_l = always_redraw(lambda: Line(P(-0.3, fy() - 0.75), Vc.m(CB + (t.dm.get_value() + t.ta.get_value()) * u_()) + P(0.06, -0.05), color=WHITE,
                                            stroke_width=1.5, stroke_opacity=0.6).set_z_index(9))
        sy = Vc.m(CB + RB * u_())
        lsurf = eq("R", size=M_S, color=BLUE_L).set_z_index(10).move_to(P(0.15, sy[1] + 0.85))
        lsurf_l = Line(P(-0.3, sy[1] + 0.85), sy + P(0.06, 0.05), color=WHITE, stroke_width=1.5, stroke_opacity=0.6).set_z_index(9)
        cond = eq(r"a+|\vec d|<R", size=M_L)
        in_ana(cond, EQ_Y)
        cb = box(cond, VIOLET)
        t2 = stack(note("O ponto mais distante da cavidade fica", op=0.95), note("antes da superfície externa, logo é interna", op=0.95))
        in_ana(t2, OBS_Y)
        self.play(FadeIn(far), FadeIn(surf), Create(gap), FadeIn(VGroup(lfar, lfar_l, lsurf, lsurf_l)), run_time=1.4)
        self.play(FadeIn(cond, shift=0.1 * DOWN), Create(cb), FadeIn(t2), run_time=1.2)
        self.at(714.0)
        # variar a, com a densidade e d⃗ fixos: a condição continua valendo
        va = stack(note("Mudando o raio a, com a densidade e d fixos,", CYAN, 0.95), note("a condição continua valendo", CYAN, 0.95))
        in_ana(va, OBS_Y)
        self.play(FadeOut(t2), FadeIn(va), t.ta.animate.set_value(0.8), run_time=2.0)
        self.play(t.ta.animate.set_value(1.45), run_time=2.2)
        self.play(t.ta.animate.set_value(RA), run_time=1.6)
        self.n13x = VGroup(segR, tR, sega, ta_l, td, far, surf, gap, lfar, lfar_l, lsurf, lsurf_l, cond, cb, va, dob, ttl)
        self.at(725.0)

    # ═══ N14 · 12:05–13:10 · campo dentro da cavidade ═══
    def n14(self):
        self.begin(14, "campo_cavidade")
        t, Vc, cc = self.ct, self.Vc, self.cc
        ttl = self.title("Campo dentro da cavidade")
        self.play(FadeOut(self.n13x), FadeOut(self.n12x[1]), FadeOut(VGroup(*self.leg)), *Vc.go(CZS, CZC), FadeIn(ttl), run_time=2.4)
        self.leg = []
        self.play(t.dv.animate.set_value(1.0), run_time=0.5)
        p0 = cc_of(DM0, DA0) + WAYC[0]
        rig = self.rigc = Rig(Vc, lambda: CB, cc, p0, k=KC)
        pd, pl = rig.dot(), rig.lab(eq("P", size=M_M), "P")
        ra, rb = rig.ra(), rig.rb()
        lra = rig.lab(eq(r"\vec r", size=M_M, color=BLUE_L), "ra")
        lrb = rig.lab(eq(r"\vec r\,'", size=M_M, color=MAG_L), "rb")
        td = follow(eq(r"\vec d", size=M_M), lambda: (Vc.m(CB) + Vc.m(cc())) / 2 + 0.55 * perp(cc() - CB, -1))
        self.at(732.0)
        self.leg_add(eq("P", size=M_LEG), "Ponto de observação", extra=[FadeIn(pd, scale=1.6), FadeIn(pl), FadeIn(td)])
        self.leg_add(eq(r"\vec r", size=M_LEG, color=BLUE_L), "Do centro grande até P", extra=[Create(ra), FadeIn(lra)])
        self.leg_add(eq(r"\vec r\,'", size=M_LEG, color=MAG_L), "Do centro da cavidade até P", extra=[Create(rb), FadeIn(lrb)])
        r4 = mix("O apóstrofo indica outra origem; não é derivada", size=T_LEG, color=MAG_L, op=0.95)
        in_ana(r4, OBS_Y)
        self.play(FadeIn(r4), run_time=0.6)
        # mesma gramática de N07: caminho direto e caminho em dois trechos
        self.at(740.0)
        sCB, sCC, sP = Vc.m(CB), Vc.m(cc()), rig.sp()
        trav = ring().move_to(sCB)
        e1 = MathTex(r"\vec r", "=", r"\vec d", "+", r"\vec r\,'", font_size=M_L)
        e1[0].set_color(BLUE_L)
        e1[4].set_color(MAG_L)
        in_ana(e1, EQ_Y)
        hp = vec(sCB, sP, WHITE, 9, op=0.9, z=9)
        hd = vec(sCB, sCC, WHITE, 9, op=0.9, z=9)
        hm = vec(sCC, sP, WHITE, 9, op=0.9, z=9)
        self.play(FadeIn(trav), FadeIn(hp), trav.animate.move_to(sP), FadeIn(e1[0]), run_time=1.5, rate_func=linear)
        self.play(FadeOut(hp), trav.animate.move_to(sCB), run_time=0.8)
        self.play(FadeIn(hd), trav.animate.move_to(sCC), FadeIn(e1[2]), run_time=1.3, rate_func=linear)
        self.play(FadeIn(hm), trav.animate.move_to(sP), FadeIn(e1[3]), FadeIn(e1[4]), FadeIn(e1[1]), run_time=1.3, rate_func=linear)
        self.play(FadeOut(VGroup(hd, hm, trav, r4)), run_time=0.6)
        self.at(750.0)
        # contribuições: campos parciais; posições recolhidas
        ref = e1
        self.play(FadeOut(VGroup(lra, lrb)), FadeOut(VGroup(*self.leg)), rig.rv.animate.set_value(0.0),
                  ref.animate.scale(0.6).move_to(P(AX, 0.95)), run_time=0.9)
        self.leg = []
        E1, E2 = rig.Ea_v(), rig.Eb_v()
        self.leg_add(eq("P", size=M_LEG), "Ponto de observação")
        self.leg_add(eq(r"\vec E_1", size=M_LEG, color=CYAN), "Campo da esfera cheia")
        self.leg_add(eq(r"\vec E_2", size=M_LEG, color=CYAN), "Campo da esfera fictícia")
        e2 = MathTex(r"\vec E_1", "=", "C", r"\vec r", font_size=M_M)
        e2b = MathTex(r"\vec E_2", "=", "-", "C", r"\vec r\,'", font_size=M_M)
        e2[0].set_color(CYAN)
        e2b[0].set_color(CYAN)
        in_ana(e2, 0.1)
        in_ana(e2b, -0.7)
        self.play(Create(E1), FadeIn(e2), run_time=1.3)
        self.play(Create(E2), FadeIn(e2b), run_time=1.3)
        self.at(758.0)
        Et = rig.Et_v()
        s1 = eq(r"\vec E=C\,\vec r-C\,\vec r\,'", size=M_M)
        in_ana(s1, EQ_Y)
        s1b = eq(r"\vec E=C\,(\vec r-\vec r\,')", size=M_M)
        in_ana(s1b, EQ_Y)
        s1c = eq(r"\vec E=C\,\vec d", size=M_M)
        in_ana(s1c, EQ_Y)
        self.play(Create(Et), FadeOut(e2), FadeOut(e2b), FadeIn(s1, shift=0.1 * DOWN), run_time=1.3)
        self.at(764.0)
        # N14 — fatoração e substituição equivalentes às de N09
        self.gm(s1, s1b, [([0], [0]), ([1], [1]), ([2], [2]), ([3, 7], [3]), ([4], [5]), ([5], [6]), ([6], [7]), ([8], [8]), ([9], [9]), ([10], [10])], rt=2.2)
        nrr = mix("Como em N07:", eq(r"\vec r-\vec r\,'=\vec d", size=M_S), size=T_NOTE)
        in_ana(nrr, OBS_Y)
        self.play(FadeIn(nrr), run_time=0.7)
        self.at(768.0)
        self.gm(s1b, s1c, [([0], [0]), ([1], [1]), ([2], [2]), ([3], [3]), ([4, 5, 6, 7, 8, 9, 10, 11], [4, 5])], rt=2.2)
        s2 = eq(r"\vec E_{\mathrm{cav}}=\frac{\rho}{3\varepsilon_0}\,\vec d", size=M_L)
        in_ana(s2, EQ_Y)
        self.play(FadeOut(s1c), FadeOut(ref), FadeIn(s2, shift=0.1 * DOWN), run_time=1.1)
        b2 = box(s2)
        self.play(Create(b2), FadeOut(nrr), run_time=0.8)
        self.at(772.0)
        # P percorre a cavidade: parciais mudam, o total fica
        nm = note("Mova P: as parcelas mudam; o total, não", CYAN, 0.95)
        in_ana(nm, OBS_Y)
        self.play(FadeIn(nm), run_time=0.6)
        for w in WAYC[1:]:
            self.play(*rig.to(cc_of(DM0, DA0) + w), run_time=1.6)
            self.wait(0.4)
        # outra direção de d⃗: o campo gira junto
        self.at(782.0)
        nd = note("Em outra direção de d, o campo gira junto", op=0.95)
        in_ana(nd, OBS_Y)
        self.play(FadeOut(VGroup(E1, E2, pd, pl, Et)), FadeOut(VGroup(*self.leg)), t.ev.animate.set_value(1.0), FadeOut(nm), FadeIn(nd), run_time=0.9)
        self.leg = []
        self.play(t.da.animate.set_value(100.0), run_time=2.4)
        self.wait(0.8)
        self.play(t.da.animate.set_value(200.0), run_time=2.4)
        self.wait(0.8)
        self.play(t.da.animate.set_value(DA0), run_time=2.2)
        self.n14x = VGroup(s2, b2, nd, td, ttl)
        self.at(790.0)

    # ═══ N15 · 13:10–13:40 · alcance e limites ═══
    def n15(self):
        self.begin(15, "limites")
        t = self.ct
        self.play(FadeOut(self.n14x), run_time=0.8)
        ttl = self.title("Alcance do resultado")
        a1 = stack(note("Quanto mais deslocada a cavidade,", CYAN), note("maior o campo: E é proporcional a d", CYAN))
        in_ana(a1, EQ_Y)
        self.play(FadeIn(ttl), FadeIn(a1), t.dm.animate.set_value(1.1), run_time=2.4)
        self.wait(0.8)
        self.play(t.dm.animate.set_value(0.4), run_time=2.0)
        self.play(t.dm.animate.set_value(DM0), run_time=1.4)
        self.at(800.0)
        sup = note("Superposição: sempre válida na eletrostática", CYAN, 0.95)
        un = note("Campo uniforme: só com esta estrutura", MAG_L, 0.95)
        conds = [note("Densidade uniforme"), note("Cavidade esférica"),
                 mix("Campos lineares com o mesmo", eq("|C|", size=M_S), size=T_NOTE), note("Centros fixos")]
        rows = VGroup(*[hchain(Dot(radius=0.05, color=VIOLET), c, buff=0.2) for c in conds]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        lst = stack(sup, un, rows, gap=0.3)
        in_ana(lst, EQ_Y)
        self.play(FadeOut(a1), FadeIn(sup), FadeIn(un), run_time=1.0)
        self.play(FadeIn(rows, lag_ratio=0.3), run_time=3.0)
        self.at(808.0)
        # outro formato: o resultado não é herdado
        ox = Ellipse(width=0.9, height=0.45).rotate(0.4).set_stroke(WHITE, 3).set_fill(BACKGROUND_COLOR, 1)
        os_ = Circle(radius=0.55).set_stroke(BLUE_L, 3).set_fill(BLUE, 0.3)
        icon = VGroup(os_, ox)
        qm = eq(r"\vec E=\text{?}", size=M_M, color=MAG_L)
        nf = note("Outro formato: sem garantia", MAG_L, 0.95)
        fm = VGroup(hchain(icon, qm, buff=0.5), nf).arrange(DOWN, buff=0.35)
        in_ana(fm, EQ_Y)
        self.play(FadeOut(lst), FadeIn(fm), run_time=1.2)
        self.n15x = VGroup(fm, ttl)
        self.at(820.0)

    # ═══ N16 · 13:40–14:15 · checagens e estratégia ═══
    def n16(self):
        self.begin(16, "checagens")
        t = self.ct
        self.play(FadeOut(self.n15x), run_time=0.8)
        ttl = self.title("Checagens")
        self.play(FadeIn(ttl), run_time=0.5)
        items = [
            VGroup(eq(r"\vec d=0\Rightarrow\vec E=0", size=M_L), note("Centros coincidentes: cavidade concêntrica", op=0.95)).arrange(DOWN, buff=0.35),
            mix("Trocar", eq(r"+\rho\leftrightarrow-\rho", size=M_L), "inverte E", size=T_NOTE),
            eq(r"\left[\frac{\rho\,d}{\varepsilon_0}\right]=\frac{(\mathrm{C/m^3})\,\mathrm{m}}{\mathrm{C^2/(N\,m^2)}}=\mathrm{N/C}", size=M_M),
        ]
        for it in items:
            in_ana(it, EQ_Y)
        # uma checagem ativa por vez; o estado é sustentado antes de restaurar
        self.at(824.0)
        self.play(FadeIn(items[0], shift=0.1 * DOWN), t.dm.animate.set_value(0.0), run_time=2.2)
        self.wait(2.2)
        self.play(t.dm.animate.set_value(DM0), run_time=1.2)
        self.at(833.0)
        self.play(FadeOut(items[0]), FadeIn(items[1], shift=0.1 * DOWN), t.rho.animate.set_value(-1.0), run_time=2.2)
        self.wait(2.0)
        self.play(t.rho.animate.set_value(1.0), run_time=1.2)
        self.at(842.0)
        self.play(FadeOut(items[1]), FadeIn(items[2], shift=0.1 * DOWN), run_time=0.9)
        self.wait(2.6)
        # estratégia: os próprios objetos, em sequência
        self.at(848.0)
        self.wipe(0.9)
        y = 0.6
        c_pair = make_pair(P(-5.3, y), 0.28).all
        c_dec = VGroup(sph(P(-2.88, y), 0.55, False), sph(P(-1.72, y), 0.55, True))
        c_sph = VGroup(Circle(radius=0.62, arc_center=P(1.1, y)).set_stroke(BLUE_L, 3).set_fill(BLUE, 0.3),
                       *[vec(P(1.1, y) + 0.62 * U(a), P(1.1, y) + 1.05 * U(a), CYAN, 3, z=6) for a in range(30, 390, 60)])
        o_ = P(4.9, y)
        c_sum = VGroup(vec(o_ + P(-0.5, -0.35), o_ + P(0.1, 0.3), BLUE_L, 4), vec(o_ + P(0.1, 0.3), o_ + P(0.55, 0.0), MAG_L, 4),
                       vec(o_ + P(-0.5, -0.35), o_ + P(0.55, 0.0), CYAN, 6))
        words = ["Geometria difícil", "Decomposição", "Problemas simétricos", "Superposição"]
        centers = [-5.3, -2.3, 1.1, 4.9]
        icons = [c_pair, c_dec, c_sph, c_sum]
        lbl = [note(w, op=0.95).move_to(P(cx, y - 1.4)) for w, cx in zip(words, centers)]
        arrows = [eq(r"\rightarrow", size=M_M).move_to(P(x, y)) for x in (-4.0, -0.5, 3.2)]
        for i in range(4):
            self.play(FadeIn(icons[i]), FadeIn(lbl[i]), *([FadeIn(arrows[i - 1])] if i else []), run_time=1.1)
            self.wait(0.8)
        self.wait(3.0)
        self.at(855.0)
