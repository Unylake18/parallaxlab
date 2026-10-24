"""yt_0010 — Como movimento vira corrente? (fem de movimento; barra livre = Griffiths 7.7).

Preview visual silencioso, 960×540 / 15 fps. Storyboard congelado N01–N48 (ver ficha.md).

Um aparato só (trilhos + resistor + barra + B entrando na tela), controlado por trackers:
barra puxada com u constante → fluxo → faixa varrida → mesma barra sem força externa → energia dissipada.
Cores: u violeta · B magenta · corrente/I/v_d verde · F_mag azul-claro · agente externo e energia mecânica ciano ·
calor/P_R/E_diss laranja (único tom quente) · aparato em aço.
Convenção: +x direita, +y cima, +z para fora da tela; B = −B ẑ; u = u x̂; circuito anti-horário, n̂ = +ẑ.
"""
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from manim import (
    config,
    Succession, Wait, AnimationGroup, DashedLine,
    Arc, Arrow, Axes, Circle, DashedVMobject, DoubleArrow, Dot, FadeIn, FadeOut, ImageMobject, Indicate, LaggedStart,
    Line, ManimColor, MathTex, Mobject, Polygon, Rectangle, ReplacementTransform, RoundedRectangle, Scene,
    SurroundingRectangle, Transform, TransformFromCopy, TransformMatchingTex, VGroup, VMobject, ValueTracker, Create,
    Write, always_redraw, interpolate_color, linear, smooth, UP, DOWN, LEFT, RIGHT, UL, UR, PI,
)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import screen_text  # noqa: E402

# ── paleta ───────────────────────────────────────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR        # agente externo, energia mecânica, ℰ
BLUE = "#267BFF"            # carga positiva de prova
VIOLET = "#9C8CFF"          # u
MAGENTA = "#EA63FF"         # B, Φ_B
GREEN = "#3FE08B"           # corrente, v_d
FC = "#5AA2FF"              # força magnética
HEAT = "#FF7A3D"            # calor / P_R / E_diss
STEEL = "#7A8696"           # trilhos
GEO = "#B8C4DA"             # geometria (l, x, área)
DIM = "#8FA3C4"
PANEL = "#0E2A52"

T_BODY, T_NOTE, T_CAP = 30, 26, 22
M_XL, M_L, M_M, M_S = 54, 46, 38, 30

TOK = {
    r"\mathbf u": VIOLET, "u": VIOLET, r"\mathbf B": MAGENTA, "B": MAGENTA, "I": GREEN, r"\mathcal E": CYAN,
    r"\mathbf v_d": GREEN, r"\mathbf F_{B,u}": FC, r"\mathbf F_B": FC, r"\mathbf F_{\rm mag}": FC, r"F_{\rm mag}": FC,
    r"\mathbf F_{\rm ext}": CYAN, r"F_{\rm ext}": CYAN, r"P_{\rm ext}": CYAN, r"P_R": HEAT, r"E_{\rm diss}": HEAT,
    r"K_0": CYAN, r"K(t)": CYAN, r"E_{\rm diss}(t)": HEAT, r"F_x": FC, r"\Phi_B": MAGENTA, r"\tau": VIOLET, r"\frac{d\Phi_B}{dt}": MAGENTA,
}

# ── geometria local do aparato (unidades locais; a tela é W(p) = C + s·(p − F)) ────────────────────────────────
XL, XR, YT, YB = -3.0, 4.6, 1.0, -1.0     # fio esquerdo, fim dos trilhos, trilho de cima, trilho de baixo
XB0, XB_MAX = 0.0, 4.2                    # barra: início e fim do percurso forçado (3.6 = 6 passos da grade de B)
F0X = 0.8                                 # centro de enquadramento do aparato inteiro
D_DEC = 3.4                               # distância total (assintótica) percorrida na barra livre, em unidades locais
TAU = 2.0                                 # τ em unidades do eixo t (tempo físico do gráfico)
TT_END = 4.5                              # fim do trecho sincronizado, em t/τ
BX = [-3.3 + 0.6 * k for k in range(15)]
BY = [-1.5 + 0.6 * j for j in range(6)]
QY = [-0.72, -0.36, 0.0, 0.36, 0.72]
TC = 3                                    # índice da carga de prova
NDOT = 26

LAYOUTS = {                               # (s, cx, cy, fol)
    "full": (1.45, 0.0, -0.3, 0.0),
    "left": (0.95, -3.0, 0.0, 0.0),
    "top": (0.80, 0.0, 1.45, 0.0),
    "bar": (1.9, -3.0, 0.0, 1.0),
    "hook": (1.2, 0.0, 0.7, 0.0),
}
CLIPX = {"full": 9.0, "left": 0.9, "top": 9.0, "bar": 0.5, "hook": 9.0}   # o campo B não invade a matemática
EQX = 4.3                                 # centro da coluna de equações à direita


def txt(s, size=T_BODY, color=WHITE, opacity=1.0):
    if size <= 28:                       # anotações em Space Grotesk MAIÚSCULA (manchetes e frases de corpo ficam normais)
        s = s.upper()
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(opacity)


def fitw(m, w=6.2):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def M(*parts, size=M_L, w=None):
    """MathTex por partes; cada parte na cor da grandeza (serve a TransformMatchingTex)."""
    m = MathTex(*parts, font_size=size, color=WHITE)
    for part, sub in zip(parts, m.submobjects):
        c = TOK.get(part)
        if c:
            sub.set_color(c)
    if w and m.width > w:
        m.scale_to_fit_width(w)
    return m


def arrow(a, b, color=WHITE, width=5, z=8, tip=0.2, op=1.0):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if np.linalg.norm(b - a) < 0.03:
        return VMobject()
    m = Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.45,
              max_stroke_width_to_length_ratio=50)
    return m.set_opacity(op).set_z_index(z)


def P3(x, y):
    return np.array([x, y, 0.0])


def boxed(m, color=WHITE, buff=0.16, width=3):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=width, corner_radius=0.1)


class Ap:
    """Estado do aparato: trackers (visuais e físicos) + construção do desenho a cada quadro."""
    NAMES = ("oAll", "oB", "oBar", "oU", "oI", "oF", "oA", "oO", "oQ", "oQF", "oP", "oHB", "oL", "oX", "oTC")

    def __init__(self):
        T = ValueTracker
        self.s, self.cx, self.cy, self.fol = T(1.45), T(0.0), T(-0.3), T(0.0)
        self.xb = T(XB0)
        for n in self.NAMES:
            setattr(self, n, T(0.0))
        self.ua, self.cur, self.heat, self.fm, self.fe = T(1.0), T(0.0), T(0.0), T(0.0), T(0.0)
        self.drift, self.barf, self.tt = T(0.0), T(1.0), T(0.0)
        self.clx, self.frozen, self.auto = T(9.0), False, 0.0
        self.autoloop, self.lp, self.lt = False, "run", 0.0
        self.mode, self.moving, self.vsp = "forced", True, 0.55
        self.rph, self.rt, self.ph, self.qph = "run", 0.0, 0.0, 0.0

    # ── transformação local → tela ──────────────────────────────────────────────────────────────────────────
    def W(self, x, y=0.0):
        s, f = self.s.get_value(), self.fol.get_value()
        fx = (1 - f) * F0X + f * self.xb.get_value()
        return P3(self.cx.get_value() + s * (x - fx), self.cy.get_value() + s * y)

    def qy(self, i):
        y = ((QY[i] + self.qph + 0.9) % 1.8) - 0.9
        return y

    def qpos(self, i):
        return (self.xb.get_value(), self.qy(i))

    def loop_pt(self, u):
        """Percurso anti-horário: sobe pela barra, volta pelo trilho de cima, desce pela esquerda, volta por baixo."""
        xb = self.xb.get_value()
        lb, lh = YT - YB, max(xb - XL, 0.01)
        d = (u % 1.0) * (2 * lb + 2 * lh)
        if d < lb:
            return xb, YB + d
        d -= lb
        if d < lh:
            return xb - d, YT
        d -= lh
        if d < lb:
            return XL, YT - d
        d -= lb
        return XL + d, YB

    # ── dinâmica ────────────────────────────────────────────────────────────────────────────────────────────
    def tick(self, dt):
        if self.mode == "decay" and self.autoloop:      # soltura em laço: a barra freia, some, e recomeça em t = 0
            if self.lp == "run":
                self.tt.increment_value(dt * TT_END / 12.0)
                if self.tt.get_value() >= TT_END:
                    self.lp, self.lt = "hold", 0.0
            elif self.lp == "hold":
                self.lt += dt
                if self.lt >= 1.0:
                    self.lp, self.lt = "out", 0.0
            elif self.lp == "out":
                self.lt += dt
                self.barf.set_value(max(0.0, 1 - self.lt / 0.4))
                if self.lt >= 0.4:
                    self.tt.set_value(0.0)
                    self.lp, self.lt = "in", 0.0
            else:
                self.lt += dt
                self.barf.set_value(min(1.0, self.lt / 0.4))
                if self.lt >= 0.4:
                    self.lp = "run"
        if self.auto > 0:                                # relógio da soltura: tt avança sozinho, encaixado na voz
            self.tt.increment_value(self.auto * dt)
            if self.tt.get_value() >= TT_END:
                self.tt.set_value(TT_END)
                self.auto = 0.0
        if self.mode == "decay":
            e = math.exp(-self.tt.get_value())
            self.xb.set_value(XB0 + D_DEC * (1 - e))
            self.ua.set_value(e)
            self.cur.set_value(e)
            self.fm.set_value(e)
            self.heat.set_value(e * e)
        elif self.mode == "forced" and self.moving:
            if self.rph == "run":
                self.xb.increment_value(self.vsp * dt)
                if self.xb.get_value() > XB_MAX:
                    if self.fol.get_value() > 0.5:      # câmera seguindo a barra: o fundo (grade de B) é periódico
                        self.xb.increment_value(-XB_MAX)
                    else:
                        self.rph, self.rt = "out", 0.0
            elif self.rph == "out":
                self.rt += dt
                self.barf.set_value(max(0.0, 1 - self.rt / 0.3))
                if self.rt >= 0.3:
                    self.xb.set_value(XB0)
                    self.rph, self.rt = "in", 0.0
            else:
                self.rt += dt
                self.barf.set_value(min(1.0, self.rt / 0.3))
                if self.rt >= 0.3:
                    self.rph = "run"
        if not self.frozen:
            self.ph = (self.ph + dt * 0.25 * self.cur.get_value()) % 1.0
            self.qph += dt * 0.35 * self.drift.get_value()

    # ── desenho ─────────────────────────────────────────────────────────────────────────────────────────────
    def build(self):
        g = VGroup()
        A = self.oAll.get_value()
        if A < 0.01:
            return g.add(Dot(radius=0.001, fill_opacity=0, stroke_opacity=0))
        s, W = self.s.get_value(), self.W
        xb, bf = self.xb.get_value(), self.barf.get_value()
        lw = 2.5 + 2.0 * min(s, 2.0)
        h, cur = self.heat.get_value(), self.cur.get_value()

        clx = self.clx.get_value()
        fx = (1 - self.fol.get_value()) * F0X + self.fol.get_value() * xb
        xe = min(XR, fx + (clx - self.cx.get_value()) / s)
        ob = self.oB.get_value() * A
        if ob > 0.01:                                          # campo B entrando na tela: cruzes
            mk, a = VMobject(), 0.07 * s
            for xi in BX:
                for yj in BY:
                    c = W(xi, yj)
                    if abs(c[0]) > 7.7 or abs(c[1]) > 4.7 or c[0] > clx or c[1] > 2.6 or c[1] < -2.45:
                        continue
                    mk.start_new_path(c + P3(-a, -a))
                    mk.add_line_to(c + P3(a, a))
                    mk.start_new_path(c + P3(-a, a))
                    mk.add_line_to(c + P3(a, -a))
            if mk.has_points():
                g.add(mk.set_stroke(MAGENTA, 1.6 + 0.8 * s, 0.38 * ob).set_fill(opacity=0).set_z_index(0))

        oa = self.oA.get_value() * A
        if oa > 0.01:                                          # área do circuito A = l·x
            g.add(Polygon(W(XL, YB), W(xb, YB), W(xb, YT), W(XL, YT)).set_fill(GEO, 0.2 * oa)
                  .set_stroke(width=0).set_z_index(1))

        for y in (YT, YB):                                     # trilhos e fio esquerdo
            g.add(Line(W(XL, y), W(max(xe, XL + 0.1), y), color=STEEL, stroke_width=lw, stroke_opacity=A).set_z_index(3))
        g.add(Line(W(XL, YT), W(XL, YB), color=STEEL, stroke_width=lw, stroke_opacity=A).set_z_index(3))

        if h > 0.03:                                           # brilho do resistor ∝ P_R
            for sc, op in ((2.5, 0.10), (1.9, 0.16), (1.4, 0.25)):
                g.add(RoundedRectangle(corner_radius=0.12 * s, width=0.5 * s * sc, height=1.0 * s * (0.6 + 0.4 * sc))
                      .set_fill(HEAT, op * min(h, 1.0) * A).set_stroke(width=0).move_to(W(XL, 0)).set_z_index(2))
        col = interpolate_color(ManimColor("#16233F"), ManimColor(HEAT), min(1.0, h))
        g.add(Rectangle(width=0.5 * s, height=1.0 * s).set_fill(col, A).set_stroke(STEEL, lw * 0.9, A)
              .move_to(W(XL, 0)).set_z_index(4))

        op_ = self.oP.get_value() * A
        if op_ > 0.01:                                         # medidor de P_R
            xm = XL - 0.66
            g.add(Rectangle(width=0.16 * s, height=1.0 * s).set_fill(opacity=0).set_stroke(STEEL, 2, op_)
                  .move_to(W(xm, 0)).set_z_index(4))
            fh = max(min(h, 1.0), 0.001) * s
            g.add(Rectangle(width=0.16 * s, height=fh).set_fill(HEAT, 0.9 * op_).set_stroke(width=0)
                  .move_to(W(xm, -0.5) + P3(0, fh / 2)).set_z_index(4))

        bo = self.oBar.get_value() * A * bf
        if bo > 0.01:                                          # barra
            hb = self.oHB.get_value() * A * bf
            if hb > 0.01:
                g.add(Rectangle(width=0.66 * s, height=2.6 * s).set_fill(CYAN, 0.16 * hb)
                      .set_stroke(CYAN, 3, hb).move_to(W(xb, 0)).set_z_index(4))
            g.add(Rectangle(width=0.30 * s, height=2.24 * s).set_fill("#9AA7BC", bo)
                  .set_stroke("#DCE4F2", lw * 0.7, bo).move_to(W(xb, 0)).set_z_index(5))

        oi = self.oI.get_value() * A
        if oi > 0.01 and cur > 0.02:                           # cargas positivas circulando (corrente convencional)
            op = oi * min(1.0, 1.1 * math.sqrt(cur))
            for i in range(NDOT):
                x, y = self.loop_pt(i / NDOT + self.ph)
                g.add(Dot(W(x, y), radius=0.07 * s).set_fill(BLUE, op).set_stroke(BACKGROUND_COLOR, 1, op)
                      .set_z_index(6))
            c = max(cur, 0.12)
            g.add(arrow(W(xb, -0.85 * c), W(xb, 0.85 * c), GREEN, 6, 9, 0.22, oi * bf))

        oq = self.oQ.get_value() * A * bf
        oqf = self.oQF.get_value() * A * bf
        otc = self.oTC.get_value() * A * bf
        if oq > 0.01 or oqf > 0.01 or otc > 0.01:              # cargas dentro da barra
            for i in range(len(QY)):
                y = self.qy(i)
                edge = min(1.0, max(0.0, (0.92 - abs(y)) / 0.12))
                c0, r = W(xb, y), 0.085 * s
                if oq > 0.01:
                    g.add(Circle(radius=r).set_fill(BLUE, oq * edge).set_stroke(WHITE, 1.2, oq * edge)
                          .move_to(c0).set_z_index(7))
                    g.add(Line(c0 + P3(-0.55 * r, 0), c0 + P3(0.55 * r, 0), stroke_width=1.6, color=WHITE,
                               stroke_opacity=oq * edge).set_z_index(8))
                    g.add(Line(c0 + P3(0, -0.55 * r), c0 + P3(0, 0.55 * r), stroke_width=1.6, color=WHITE,
                               stroke_opacity=oq * edge).set_z_index(8))
                if oqf > 0.01:
                    g.add(arrow(c0, W(xb, y + 0.36), FC, 4, 9, 0.12, oqf * edge))
                if i == TC and otc > 0.01:
                    g.add(Circle(radius=0.17 * s).set_fill(opacity=0).set_stroke(WHITE, 2.5, otc)
                          .move_to(c0).set_z_index(8))

        ou = self.oU.get_value() * A * bf
        if ou > 0.01:                                          # u: seta rígida da barra
            ua = max(self.ua.get_value(), 0.04)
            g.add(arrow(W(xb, 1.4), W(xb + 1.5 * ua, 1.4), VIOLET, 6, 9, 0.22, ou))

        of = self.oF.get_value() * A * bf
        if of > 0.01:
            g.add(arrow(W(xb - 0.2, 0), W(xb - 0.2 - 1.35 * self.fm.get_value(), 0), FC, 7, 10, 0.24, of))
            g.add(arrow(W(xb + 0.2, 0), W(xb + 0.2 + 1.35 * self.fe.get_value(), 0), CYAN, 7, 10, 0.24, of))

        ol = self.oL.get_value() * A
        if ol > 0.01:
            g.add(DoubleArrow(W(xb + 0.62, YB), W(xb + 0.62, YT), buff=0, color=GEO, stroke_width=3, tip_length=0.14,
                              max_tip_length_to_length_ratio=0.2).set_opacity(ol).set_z_index(9))
        ox = self.oX.get_value() * A
        if ox > 0.01:
            g.add(DoubleArrow(W(XL, -1.4), W(xb, -1.4), buff=0, color=GEO, stroke_width=3, tip_length=0.14,
                              max_tip_length_to_length_ratio=0.2).set_opacity(ox).set_z_index(9))

        oo = self.oO.get_value() * A
        if oo > 0.01:                                          # orientação anti-horária, n̂ = +ẑ (⊙), dℓ
            ctr = W((XL + xb) / 2, 0)
            arc = Arc(radius=0.38 * s, start_angle=-0.15 * PI, angle=1.6 * PI, arc_center=ctr, color=WHITE,
                      stroke_width=3.5)
            arc.add_tip(tip_length=0.17, tip_width=0.17)
            arc.set_fill(opacity=0).set_stroke(WHITE, 3.5, oo)
            arc.tip.set_fill(WHITE, oo).set_stroke(WHITE, 1, oo)
            g.add(arc.set_z_index(9))
            g.add(Circle(radius=0.14 * s).set_fill(opacity=0).set_stroke(WHITE, 2.5, oo).move_to(ctr).set_z_index(9))
            g.add(Dot(ctr, radius=0.04 * s).set_fill(WHITE, oo).set_z_index(9))
            g.add(arrow(W(xb - 0.42, -0.3), W(xb - 0.42, 0.3), WHITE, 5, 11, 0.16, oo * bf))
        return g


AUDIT = os.environ.get("AUDIT") == "1"
SYNC = os.environ.get("SYNC", "")        # "medir" (passe a seco) | "final" (encaixa cada trecho na voz) | "" (preview livre)
PASTA = Path(__file__).resolve().parent
config.max_files_cached = 4000            # permite retomar o render final sem refazer animações já escritas
LEAD = 0.15                              # a imagem começa 0,15 s antes da frase correspondente


def plano(A, W, D):
    """(escala das animações, escala das esperas) para encaixar um trecho (A s de animação + W s de espera) em D s."""
    if A + W < 1e-6:
        return 1.0, 1.0
    if D >= A + W:
        s_ = min(1.8, max(1.0, (D / (A + W)) ** 0.5))
        return s_, (max(1.0, (D - s_ * A) / W) if W > 1e-6 else 1.0)
    wp = max(0.15 * W, D - A)
    if A + wp <= D + 1e-6:
        return 1.0, wp / W if W > 1e-6 else 1.0
    return max(0.5, (D - wp) / A), (wp / W if W > 1e-6 else 1.0)


class FemMovimentoYT010(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        ap = self.ap = Ap()
        tickm = Mobject()
        tickm.add_updater(lambda m, dt: ap.tick(dt))
        self.add(tickm)
        self.tag = txt("ELETROMAGNETISMO · FEM DE MOVIMENTO E REGRA DO FLUXO MAGNÉTICO", 24, opacity=0.78) \
            .to_corner(UL, buff=0.32).set_z_index(40)
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3)
        self.wm.set_z_index(40)
        self.add(self.tag, self.wm)
        self.body = always_redraw(ap.build)
        self.add(self.body)
        self.hd, self.E = None, VGroup()
        self.Tu, self.Tvd, self.Tw, self.Tf, self.Tfb = (ValueTracker(0) for _ in range(5))
        self.mk_labels()
        self.mk_legend()
        self.sync_init()

        self.n00()
        if AUDIT:
            self.audit('n00')
        self.n01()
        if AUDIT:
            self.audit('n01')
        self.n02()
        if AUDIT:
            self.audit('n02')
        self.n03()
        if AUDIT:
            self.audit('n03')
        self.n04()
        if AUDIT:
            self.audit('n04')
        self.n05()
        if AUDIT:
            self.audit('n05')
        self.n06()
        if AUDIT:
            self.audit('n06')
        self.n07()
        if AUDIT:
            self.audit('n07')
        self.n08()
        if AUDIT:
            self.audit('n08')
        self.n09()
        if AUDIT:
            self.audit('n09')
        self.n10()
        if AUDIT:
            self.audit('n10')
        self.n11()
        if AUDIT:
            self.audit('n11')
        self.n12()
        if AUDIT:
            self.audit('n12')
        self.n13()
        if AUDIT:
            self.audit('n13')
        self.n14()
        if AUDIT:
            self.audit('n14')
        self.n15()
        if AUDIT:
            self.audit('n15')
        self.n16()
        if AUDIT:
            self.audit('n16')
        self.n17()
        if AUDIT:
            self.audit('n17')
        self.n18()
        if AUDIT:
            self.audit('n18')
        self.n19()
        if AUDIT:
            self.audit('n19')
        self.n20()
        if AUDIT:
            self.audit('n20')
        self.n21()
        if AUDIT:
            self.audit('n21')
        self.n22()
        if AUDIT:
            self.audit('n22')
        self.n23()
        if AUDIT:
            self.audit('n23')
        self.n24()
        if AUDIT:
            self.audit('n24')
        self.n25()
        if AUDIT:
            self.audit('n25')
        self.n26()
        if AUDIT:
            self.audit('n26')
        self.n27()
        if AUDIT:
            self.audit('n27')
        self.n28()
        if AUDIT:
            self.audit('n28')
        self.n29()
        if AUDIT:
            self.audit('n29')
        self.n30()
        if AUDIT:
            self.audit('n30')
        self.n31()
        if AUDIT:
            self.audit('n31')
        self.n32()
        if AUDIT:
            self.audit('n32')
        self.n33()
        if AUDIT:
            self.audit('n33')
        self.n34()
        if AUDIT:
            self.audit('n34')
        self.n35()
        if AUDIT:
            self.audit('n35')
        self.n36()
        if AUDIT:
            self.audit('n36')
        self.n37()
        if AUDIT:
            self.audit('n37')
        self.n38()
        if AUDIT:
            self.audit('n38')
        self.n39()
        if AUDIT:
            self.audit('n39')
        self.n40()
        if AUDIT:
            self.audit('n40')
        self.n41()
        if AUDIT:
            self.audit('n41')
        self.n42()
        if AUDIT:
            self.audit('n42')
        self.n43()
        if AUDIT:
            self.audit('n43')
        self.n44()
        if AUDIT:
            self.audit('n44')
        self.n45()
        if AUDIT:
            self.audit('n45')
        self.n46()
        if AUDIT:
            self.audit('n46')
        self.n47()
        if AUDIT:
            self.audit('n47')
        self.n48()
        if AUDIT:
            self.audit('n48')
        self.n49()
        if AUDIT:
            self.audit('n49')
        self.fim_sync()

    # ── sincronização com a voz ───────────────────────────────────────────────────────────────────────────────
    def sync_init(self):
        self._marks, self._calls, self._plan, self._mi, self._ci = [], [], {}, 0, 0
        self._hold, self._med, self._late = False, None, []
        self.fr = json.load(open(PASTA / "frases.json", encoding="utf-8"))
        self.vdur = json.load(open(PASTA / "sync.json", encoding="utf-8"))["dur"]
        if SYNC == "medir":
            self.next_section(skip_animations=True)
        elif SYNC == "final":
            self._med = json.load(open(PASTA / "medicao.json", encoding="utf-8"))

    def fr_t(self, n, k):
        return self.fr[f"N{n:02d}"][k]["t0"]

    def alvo(self, n, k):
        return max(0.0, self.fr_t(n, k) - LEAD)

    def unit_end(self, n):
        return self.fr_t(n + 1, 0) if f"N{n + 1:02d}" in self.fr else self.vdur

    def an(self, n, k=0):
        """Âncora: daqui em diante a cena corresponde à frase k da unidade n (início da frase − LEAD)."""
        sid = f"N{n:02d}.{k}"
        if SYNC == "medir":
            self._marks.append({"id": sid, "t": round(self.renderer.time, 4)})
            return
        if SYNC != "final":
            return
        i = self._mi
        self._mi += 1
        marks = self._med["marks"]
        assert marks[i]["id"] == sid, (marks[i]["id"], sid)
        tgt = self.alvo(n, k)
        now = self.renderer.time
        if now < tgt - 0.02:
            self._hold = True
            self.play(Wait(run_time=tgt - now))
            self._hold = False
            now = self.renderer.time
        self._late.append((sid, round(now - tgt, 3)))
        if i + 1 < len(marks):
            nn, kk = int(marks[i + 1]["id"][1:3]), int(marks[i + 1]["id"].split(".")[1])
            fim = self.alvo(nn, kk)
        else:
            fim = self.vdur + 2.0
        A = sum(c["d"] for c in self._med["calls"] if c["seg"] == i and c["k"] == "play")
        W = sum(c["d"] for c in self._med["calls"] if c["seg"] == i and c["k"] == "wait")
        self._plan[i] = plano(A, W, max(0.3, fim - now))

    def play(self, *args, **kwargs):
        if SYNC == "medir":
            t0 = self.renderer.time
            super().play(*args, **kwargs)
            k = "wait" if (len(args) == 1 and isinstance(args[0], Wait)) else "play"
            self._calls.append({"seg": len(self._marks) - 1, "k": k, "d": round(self.renderer.time - t0, 4)})
            return
        if SYNC == "final" and self._med is not None and not self._hold:
            c = self._med["calls"][self._ci]
            self._ci += 1
            sa, sw = self._plan.get(c["seg"], (1.0, 1.0))
            if c["k"] == "wait":
                d = c["d"] * sw
                if d < 1e-3:
                    return
                args[0].run_time = d
            else:
                kwargs["run_time"] = max(1 / 30, c["d"] * sa)
        super().play(*args, **kwargs)

    def decay_until(self, t_fim):
        """A soltura (tt) avança sozinha com o relógio da cena e chega a TT_END em t_fim (tempo de vídeo)."""
        ap = self.ap
        if SYNC == "final":
            ap.auto = (TT_END - ap.tt.get_value()) / max(1.0, t_fim - self.renderer.time)
        elif SYNC == "":
            ap.auto = (TT_END - ap.tt.get_value()) / 12.0

    def fim_sync(self):
        if SYNC == "medir":
            json.dump({"marks": self._marks, "calls": self._calls, "t_total": round(self.renderer.time, 3)},
                      open(PASTA / "medicao.json", "w", encoding="utf-8"), indent=0)
        elif SYNC == "final":
            json.dump({"atrasos": self._late, "t_total": round(self.renderer.time, 3)},
                      open(PASTA / "atrasos.json", "w", encoding="utf-8"), indent=0)

    # ── auditoria de layout ─────────────────────────────────────────────────────────────────────────────────
    def audit(self, name):
        from manim import Text
        items = []
        for m in self.mobjects:
            for f in m.get_family():
                if isinstance(f, (Text, MathTex)) and f is not self.tag and f.has_points() is not None:
                    try:
                        if f.get_fill_opacity() < 0.25 and f.get_stroke_opacity() < 0.25:
                            continue
                    except Exception:
                        pass
                    if f.width > 0.01:
                        items.append(f)
        tops = [f for f in items if f is not self.hd]
        out = []

        def box(f):
            return (f.get_left()[0], f.get_right()[0], f.get_bottom()[1], f.get_top()[1])
        for i, a in enumerate(items):
            x0, x1, y0, y1 = box(a)
            if x0 < -7.75 or x1 > 7.75 or y0 < -4.3 or y1 > 4.3:
                out.append(f"FORA DO QUADRO: {a.get_tex_string() if hasattr(a, 'get_tex_string') else a.text[:30]}")
            for b in items[i + 1:]:
                if a is b or a in b.get_family() or b in a.get_family():
                    continue
                u0, u1, v0, v1 = box(b)
                ox, oy = min(x1, u1) - max(x0, u0), min(y1, v1) - max(y0, v0)
                if ox > 0.05 and oy > 0.05:
                    na = a.get_tex_string() if hasattr(a, "get_tex_string") else a.text[:28]
                    nb = b.get_tex_string() if hasattr(b, "get_tex_string") else b.text[:28]
                    out.append(f"SOBREPÕE: [{na[:34]}] x [{nb[:34]}] ({ox:.2f}x{oy:.2f})")
        if self.hd is not None:
            top = self.hd.get_top()[1]
            if top > 3.8 or self.hd.get_bottom()[1] < 2.9:
                out.append(f"TÍTULO fora da faixa y: top={top:.2f}")
        with open(os.path.join(os.path.dirname(__file__), "audit.log"), "a", encoding="utf-8") as fh:
            fh.write(f"{name}: {'OK' if not out else ''}\n" + "".join(f"   {o}\n" for o in out))

    # ── utilidades ──────────────────────────────────────────────────────────────────────────────────────────
    def H(self, text):
        new = txt(text.upper(), T_BODY, opacity=0.9)
        if new.width > 11.5:
            new.scale_to_fit_width(11.5)
        new.move_to(P3(0, 3.42)).set_z_index(30)
        if self.hd is not None:
            self.play(FadeOut(self.hd), run_time=0.35)
        self.hd = new
        return [FadeIn(new)]

    def lay(self, name):
        s, cx, cy, f = LAYOUTS[name]
        ap = self.ap
        return [ap.s.animate.set_value(s), ap.cx.animate.set_value(cx), ap.cy.animate.set_value(cy),
                ap.fol.animate.set_value(f), ap.clx.animate.set_value(CLIPX[name])]

    def Wl(self, name, x, y=0.0):
        s, cx, cy, f = LAYOUTS[name]
        fx = (1 - f) * F0X + f * self.ap.xb.get_value()
        return P3(cx + s * (x - fx), cy + s * y)

    def swap(self, *new):
        """Troca o conjunto de equações atual (FadeOut do velho + FadeIn do novo); retorna as animações."""
        old, self.E = self.E, VGroup(*new)
        return ([FadeOut(old)] if len(old) else []) + [FadeIn(m) for m in new]

    def lab(self, tex, anchor, off=(0, 0), color=WHITE, size=M_S, bar=False):
        ap = self.ap
        m = MathTex(tex, font_size=size, color=color)
        m.v = ValueTracker(0)

        def upd(mob):
            o = off() if callable(off) else off
            mob.move_to(ap.W(*anchor()) + P3(*o))
            ov = m.v.get_value() * ap.oAll.get_value() * (ap.barf.get_value() if bar else 1.0)
            mob.set_opacity(ov)
            mob.set_stroke(BACKGROUND_COLOR, 9, ov, background=True)
        m.add_updater(upd)
        upd(m)
        m.set_z_index(20)
        self.add(m)
        return m

    def vec(self, anchor, dvec, color, T, width=7, tip=0.22):
        ap = self.ap

        def mk():
            L = T.get_value()
            if L < 0.02:
                return VMobject()
            a = ap.W(*anchor())
            d = dvec()
            return arrow(a, a + P3(d[0], d[1]) * ap.s.get_value() * L, color, width, 12, tip)
        m = always_redraw(mk)
        self.add(m)
        return m

    def mk_labels(self):
        ap, xb = self.ap, self.ap.xb.get_value
        L = self.L = {}
        L["u"] = self.lab(r"\mathbf u=u\,\hat x", lambda: (xb() + 0.75 * ap.ua.get_value(), 1.4), (0, 0.36), VIOLET,
                          bar=True)
        L["B"] = self.lab(r"\mathbf B=-B\,\hat z", lambda: (-1.9, 1.62), (0, 0.1), MAGENTA)
        L["l"] = self.lab("l", lambda: (xb() + 0.62, 0), (0.28, 0), GEO, bar=True)
        L["x"] = self.lab("x", lambda: ((XL + xb()) / 2, -1.4), (0, -0.3), GEO)
        L["R"] = self.lab("R", lambda: (XL, 0), (0.55, 0), WHITE)
        L["I"] = self.lab("I", lambda: (xb(), 0.55), (0.32, 0), GREEN, bar=True)
        L["Fm"] = self.lab(r"\mathbf F_{\rm mag}", lambda: (xb() - 0.2 - 0.675 * ap.fm.get_value(), 0), (0, 0.36), FC,
                           bar=True)
        L["Fe"] = self.lab(r"\mathbf F_{\rm ext}", lambda: (xb() + 0.2 + 0.675 * ap.fe.get_value(), 0), (0, 0.36),
                           CYAN, bar=True)
        L["Pm"] = self.lab(r"P_R", lambda: (XL - 0.66, -0.5), (0, -0.3), HEAT)
        L["n"] = self.lab(r"\hat{\mathbf n}=+\hat z", lambda: ((XL + xb()) / 2, 0),
                          lambda: (0, -0.40 * ap.s.get_value() - 0.2), WHITE, size=22)
        L["C"] = self.lab("C", lambda: (XL + 0.3, YT - 0.32), (0, 0), WHITE, size=28)
        L["dl"] = self.lab(r"d\boldsymbol\ell", lambda: (xb() - 0.42, 0), (-0.42, 0), WHITE, size=26, bar=True)
        # rótulos dos vetores da carga de prova (N04, N08, N09)
        L["uq"] = self.lab(r"\mathbf u", lambda: (xb() + 0.5, ap.qy(TC)), (0, -0.3), VIOLET)
        L["vd"] = self.lab(r"\mathbf v_d", lambda: (xb() + 1.0, ap.qy(TC) + 0.2), (0.42, 0), GREEN)
        L["w"] = self.lab(r"\mathbf w", lambda: (xb() + 0.5, ap.qy(TC) + 0.2), (-0.3, 0.3), WHITE)
        L["Fb"] = self.lab(r"\mathbf F_B", lambda: (xb() - 0.18, ap.qy(TC) + 0.45), (-0.4, 0.1), FC)
        L["Fq"] = self.lab(r"\mathbf F_{B,u}", lambda: (xb(), ap.qy(TC) + 0.9), (0.5, 0.1), FC)

    def mk_legend(self):
        o = P3(-7.0, -3.75)
        gx, gy = arrow(o, o + P3(0.6, 0), DIM, 3.5, 3, 0.14), arrow(o, o + P3(0, 0.6), DIM, 3.5, 3, 0.14)
        lx = MathTex(r"\hat x", font_size=26, color=DIM).next_to(gx, RIGHT, buff=0.06)
        ly = MathTex(r"\hat y", font_size=26, color=DIM).next_to(gy, UP, buff=0.04)
        zc = o + P3(1.5, 0.2)
        gz = VGroup(Circle(radius=0.14).set_stroke(DIM, 2.5).move_to(zc), Dot(zc, radius=0.04).set_fill(DIM, 1))
        lz = MathTex(r"\hat z", font_size=26, color=DIM).next_to(gz, RIGHT, buff=0.1)
        self.legend = VGroup(gx, gy, lx, ly, gz, lz).set_z_index(3)

    def run_decay(self, dur):
        self.play(self.ap.tt.animate.set_value(TT_END), run_time=dur, rate_func=linear)

    def restart_decay(self, label=r"\text{repetindo a mesma soltura}\ \cdot\ t=0"):
        """Reinicia a evolução livre; antes avisa que é a mesma soltura (não um experimento novo)."""
        ap = self.ap
        if label:
            m = MathTex(label, font_size=28, color=WHITE)
            g = VGroup(m, boxed(m, color=CYAN, buff=0.14, width=2)).move_to(P3(-3.4, 2.35)).set_z_index(30)
            self.play(FadeIn(g), run_time=0.6)
            self.wait(0.8)
        self.play(ap.barf.animate.set_value(0), run_time=0.35)
        ap.mode, ap.moving, ap.rph, ap.frozen, ap.autoloop, ap.auto = "decay", False, "run", False, False, 0.0
        ap.tt.set_value(0.0)
        ap.tick(0.0)
        self.play(ap.barf.animate.set_value(1), run_time=0.35)
        if label:
            self.play(FadeOut(g), run_time=0.5)

    def pulse(self, mobs, lo=0.25, hi=0.55, period=2.4):
        """Pulsação suave de opacidade (cenas sem aparato em movimento)."""
        for m in (mobs if isinstance(mobs, (list, tuple)) else [mobs]):
            m._pt = 0.0

            def upd(mob, dt, lo=lo, hi=hi, period=period):
                mob._pt += dt
                v = lo + (hi - lo) * (0.5 + 0.5 * math.sin(2 * PI * mob._pt / period))
                mob.set_fill(opacity=v)
                mob.set_stroke(opacity=min(1.0, v + 0.2))
            m.add_updater(upd)

    def put(self, eq, rt=1.5):
        """FadeIn da equação e libera as partes como objetos de cena (para o morph parte a parte)."""
        self.play(FadeIn(eq), run_time=rt)
        self.remove(eq)
        self.add(*eq.submobjects)
        return eq

    def morph(self, a, b, pairs=None, t=2.0):
        """a → b: partes iguais se movem; o que sai vira o que entra, tudo ao mesmo tempo (a igualdade nunca fica pela metade)."""
        ta, tb = a.tex_strings, b.tex_strings
        if pairs is None:
            pairs, used = [], set()
            for i, x in enumerate(ta):
                for j, y in enumerate(tb):
                    if j not in used and x == y:
                        pairs.append((i, j))
                        used.add(j)
                        break
        ia, ib = {i for i, _ in pairs}, {j for _, j in pairs}
        gone = [a[i] for i in range(len(ta)) if i not in ia]
        came = [b[j] for j in range(len(tb)) if j not in ib]
        anims = [ReplacementTransform(a[i], b[j]) for i, j in pairs]
        wrapper = None
        if gone and came:
            wrapper = VGroup(*came)
            anims.append(ReplacementTransform(VGroup(*gone), wrapper))
        elif gone:
            anims += [FadeOut(m) for m in gone]
        elif came:
            anims += [FadeIn(m) for m in came]
        self.play(*anims, run_time=t)
        if wrapper is not None:
            self.remove(wrapper)
            self.add(*came)
        return b

    GL = {"m": r"m:\ \text{massa da barra}", "R": r"R:\ \text{resistência total}",
          "u": r"u(t):\ \text{velocidade da barra}", "I0": r"I_0:\ \text{corrente inicial}",
          "P0": r"P_0:\ \text{potência inicial}", "tau": r"\tau:\ \text{constante de tempo}"}

    def glossary(self, keys):
        return VGroup(*[MathTex(self.GL[k], font_size=26, color=DIM) for k in keys]) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(P3(-2.8, -2.8))

    def setgl(self, keys):
        new = self.glossary(keys)
        old, self.gl35 = getattr(self, "gl35", None), new
        return ([FadeOut(old)] if old is not None else []) + [FadeIn(new)]

    def show(self, *labs, rt=1.0):
        return [m.v.animate.set_value(1) for m in labs]

    def hide(self, *labs):
        return [m.v.animate.set_value(0) for m in labs]

    # ── abertura (estilo da narração) e encerramento (CTA) ─────────────────────────────────────────────────
    def n00(self):
        # logo → apresentação curta → título → aparato em cena (barra, corrente, resistor) → pergunta energética
        ap = self.ap
        ap.s.set_value(LAYOUTS["hook"][0])
        ap.cx.set_value(LAYOUTS["hook"][1])
        ap.cy.set_value(LAYOUTS["hook"][2])
        logo = ImageMobject(str(ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png")) \
            .set_width(4.6).move_to(P3(0, 0.8))
        wel = txt("Bem-vindos ao Parallax Lab", 38, WHITE).move_to(P3(0, -1.4))
        title = fitw(txt("FEM DE MOVIMENTO E REGRA DO FLUXO MAGNÉTICO", 42, CYAN), 12.5).move_to(P3(0, 0.5))
        sub = fitw(txt("Neste vídeo: como o movimento vira corrente, e de onde vem a energia", 28, DIM), 12.0) \
            .move_to(P3(0, -0.5))
        l3 = fitw(txt("A força magnética nunca realiza trabalho.", 34, FC), 12.0).move_to(P3(0, -1.9))
        l4 = fitw(txt("Então, de onde vem essa energia?", 44, WHITE), 12.0).move_to(P3(0, -2.8))
        self.an(0, 0)
        self.play(FadeIn(logo, scale=0.94), FadeIn(wel, shift=0.1 * UP), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(logo), FadeOut(wel), run_time=0.5)
        self.an(0, 2)
        self.play(FadeIn(title, shift=0.1 * UP), FadeIn(sub), run_time=1.2)
        self.wait(2.0)
        self.play(FadeOut(title), FadeOut(sub), run_time=0.6)
        self.an(0, 3)
        self.play(ap.oAll.animate.set_value(1), ap.oB.animate.set_value(1), ap.oBar.animate.set_value(1),
                  ap.oI.animate.set_value(1), ap.cur.animate.set_value(1), run_time=1.5)
        self.play(ap.heat.animate.set_value(1), run_time=4.0)
        self.an(0, 5)
        self.wait(2.0)

    def n49(self):
        oc = P3(0, 0.7)
        rings = VGroup(*[DashedVMobject(Circle(radius=r, arc_center=oc), num_dashes=max(12, int(14 * r)),
                                        dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.16) for r in (2.0, 3.0, 4.0)])
        for i, r_ in enumerate(rings):
            r_.add_updater(lambda m, dt, sg=(1 if i % 2 == 0 else -1) * (0.06 - 0.01 * i):
                           m.rotate(sg * dt, about_point=oc))
        logo = ImageMobject(str(ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png")) \
            .set_width(6.0).move_to(oc + P3(0, 0.4))
        msg = txt("Inscreva-se para acompanhar os próximos vídeos", 28, opacity=0.9).move_to(oc + P3(0, -1.0))
        nxt1 = txt("Próximo vídeo: campo magnético variável", 26, opacity=0.95).move_to(oc + P3(0, -1.85))
        nxt2 = txt("Lei de Faraday e campo elétrico induzido", 26, CYAN).move_to(oc + P3(0, -2.4))
        hook = fitw(txt("E se, em vez de mover o circuito, for o campo que muda?", 28, WHITE), 12.0) \
            .move_to(oc + P3(0, -1.85))

        def ripple():
            w = DashedVMobject(Circle(radius=1.6, arc_center=oc), num_dashes=24, dashed_ratio=0.6) \
                .set_stroke(VIOLET, 3.5, 0.35)
            self.play(w.animate.scale(2.6, about_point=oc).set_stroke(opacity=0.0), run_time=2.6)
            self.remove(w)
        self.an(49, 0)
        self.play(FadeOut(self.E), FadeOut(self.hd), FadeOut(self.legend), FadeOut(self.wm), FadeOut(self.tag),
                  self.ap.oAll.animate.set_value(0), run_time=1.2)
        self.ap.moving, self.ap.mode, self.ap.autoloop = False, "forced", False
        self.clear()                       # remove aparato, rótulos, vetores, updaters: nada fica atrás da logo
        self.hd = None
        self.play(LaggedStart(*[FadeIn(r_, scale=0.85) for r_ in rings], lag_ratio=0.3), FadeIn(logo, scale=0.92),
                  run_time=1.8)
        self.an(49, 1)
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=1.0)
        self.an(49, 2)
        self.play(FadeIn(hook, shift=0.1 * UP), run_time=1.0)
        self.wait(1.5)
        self.an(49, 4)
        self.play(FadeOut(hook), run_time=0.6)
        self.play(FadeIn(nxt1, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(nxt2, shift=0.1 * UP), run_time=0.8)
        self.an(49, 5)
        ripple()
        self.wait(1.0)

    # ── N01–N07: fenômeno, convenções, Lorentz, fem, corrente, dissipação ──────────────────────────────────────
    def n01(self):
        ap = self.ap
        self.an(1, 0)
        self.play(*self.H("Puxe a barra: o resistor esquenta"), *self.lay("full"), ap.oI.animate.set_value(0),
                  self.tag.animate.scale(0.84, about_point=self.tag.get_corner(UL)).set_opacity(0.58), run_time=2.5)
        self.wait(0.5)
        self.an(1, 1)
        ring = Rectangle(width=1.2, height=2.0).set_stroke(HEAT, 4).move_to(self.Wl("full", XL, 0))
        self.play(Create(ring), run_time=0.8)
        self.play(ring.animate.set_stroke(opacity=0), run_time=0.8)
        self.remove(ring)
        self.an(1, 2)
        self.wait(2.0)

    def n02(self):
        ap, L = self.ap, self.L
        self.an(2, 0)
        self.play(*self.H("Convenções do aparato"), ap.oU.animate.set_value(1), *self.show(L["u"]),
                  FadeIn(self.legend), run_time=2.0)
        self.an(2, 1)
        self.play(*self.show(L["B"]), ap.oB.animate.set_value(1.9), run_time=0.8)
        self.play(ap.oB.animate.set_value(1.0), run_time=0.8)
        self.an(2, 3)
        self.play(ap.oL.animate.set_value(1), *self.show(L["l"]), run_time=1.2)
        self.an(2, 4)
        ring = Rectangle(width=1.2, height=2.0).set_stroke(HEAT, 4).move_to(self.Wl("full", XL, 0))
        self.play(*self.show(L["R"]), Create(ring), run_time=1.0)
        self.play(ring.animate.set_stroke(opacity=0), run_time=0.8)
        self.remove(ring)
        self.an(2, 5)
        self.wait(1.5)

    def n03(self):
        ap, L = self.ap, self.L
        self.an(3, 0)
        self.play(*self.H("A barra inteira se move, levando as cargas junto"), *self.lay("bar"),
                  *self.hide(L["u"], L["B"], L["l"], L["R"]), ap.oL.animate.set_value(0), run_time=1.2)
        self.an(3, 1)
        self.play(ap.oQ.animate.set_value(1), run_time=1.5)
        self.an(3, 3)
        self.wait(2.0)

    def n04(self):
        ap, L = self.ap, self.L
        self.vu = self.vec(lambda: ap.qpos(TC), lambda: (1.0, 0.0), VIOLET, self.Tu)
        self.vF = self.vec(lambda: ap.qpos(TC), lambda: (0.0, 0.9), FC, self.Tf)
        e1 = M(r"\mathbf F_{B,u}", "=", "q", r"\mathbf u", r"\times", r"\mathbf B", w=6.3).move_to(P3(EQX, 1.3))
        e2 = M(r"\mathbf u", r"\times", r"\mathbf B", "=", r"+uB\,\hat y", w=6.3).move_to(P3(EQX, -0.2))
        self.an(4, 0)
        self.play(*self.H("Força de Lorentz sobre uma carga de prova"), ap.oTC.animate.set_value(1), run_time=1.0)
        self.an(4, 1)
        self.play(self.Tu.animate.set_value(1), *self.show(L["uq"]), run_time=1.2)
        self.an(4, 2)
        self.play(FadeIn(e1), run_time=1.2)
        self.an(4, 3)
        self.play(ap.oB.animate.set_value(1.9), run_time=0.8)
        self.play(ap.oB.animate.set_value(1.0), run_time=0.8)
        self.play(self.Tf.animate.set_value(1), *self.show(L["Fq"]), FadeIn(e2), run_time=1.5)
        self.E = VGroup(e1, e2)
        self.wait(1.5)

    def n05(self):
        ap, L = self.ap, self.L
        e1 = M(r"\mathcal E", "=", r"\oint", "(", r"\mathbf u", r"\times", r"\mathbf B", ")", r"\cdot",
               r"d\boldsymbol\ell", w=6.3).move_to(P3(EQX, 1.5))
        e2 = M(r"\mathcal E", "=", "Blu", w=6.0).move_to(P3(EQX, 0.0))
        b2 = boxed(e2)
        volt = MathTex(r"\text{unidade: volt}=\mathrm{J/C}", font_size=30, color=DIM).move_to(P3(EQX, -0.9))
        self.an(5, 0)
        self.play(self.Tu.animate.set_value(0), self.Tf.animate.set_value(0), ap.oTC.animate.set_value(0),
                  *self.hide(L["uq"], L["Fq"]), FadeOut(self.E), *self.H("Fem de movimento"), *self.lay("left"),
                  FadeIn(e1), run_time=2.5)
        self.an(5, 2)
        self.play(FadeIn(volt), run_time=1.0)
        self.an(5, 4)
        self.play(ap.oHB.animate.set_value(1), ap.oQF.animate.set_value(1), ap.drift.animate.set_value(1),
                  run_time=1.5)
        self.an(5, 6)
        self.play(FadeIn(e2), Create(b2), run_time=1.5)
        self.E = VGroup(e1, volt, e2, b2)
        self.wait(1.5)

    def n06(self):
        ap, L = self.ap, self.L
        e = M("I", "=", r"\frac{\mathcal E}{R}", "=", r"\frac{Blu}{R}", w=6.3).move_to(P3(EQX, 0.4))
        self.an(6, 0)
        self.play(*self.H("A corrente fecha o percurso"), ap.oHB.animate.set_value(0), ap.oQ.animate.set_value(0),
                  ap.oQF.animate.set_value(0), ap.drift.animate.set_value(0), FadeOut(self.E), run_time=1.5)
        self.an(6, 2)
        self.play(FadeIn(e), run_time=1.2)
        self.an(6, 3)
        self.play(ap.oI.animate.set_value(1), ap.cur.animate.set_value(1), *self.show(L["I"], L["R"]), run_time=2.0)
        self.E = VGroup(e)
        self.wait(2.0)

    def n07(self):
        ap, L = self.ap, self.L
        e = M(r"P_R", "=", "I^2R", ">0", size=M_XL, w=6.0).move_to(P3(EQX, 0.4))
        b = boxed(e)
        ring = Rectangle(width=1.0, height=1.5).set_stroke(HEAT, 4).move_to(self.Wl("left", XL, 0))
        self.an(7, 0)
        self.play(*self.H("O resistor dissipa potência"), FadeOut(self.E), FadeIn(e), run_time=1.5)
        self.an(7, 1)
        self.play(Create(b), run_time=0.8)
        self.an(7, 2)
        self.play(ap.oP.animate.set_value(1), *self.show(L["Pm"]), Create(ring), run_time=1.2)
        self.play(ring.animate.set_stroke(opacity=0), run_time=0.8)
        self.E = VGroup(e, b)
        self.remove(ring)
        self.an(7, 3)
        self.wait(2.0)

    # ── N08–N10: duas velocidades, F_B·w = 0, conflito ─────────────────────────────────────────────────────────
    def n08(self):
        ap, L = self.ap, self.L
        self.vvd = self.vec(lambda: (ap.xb.get_value() + 1.0, ap.qy(TC)), lambda: (0.0, 0.4), GREEN, self.Tvd)
        self.vw = self.vec(lambda: ap.qpos(TC), lambda: (1.0, 0.4), WHITE, self.Tw)
        e = M(r"\mathbf w", "=", r"\mathbf u", "+", r"\mathbf v_d", size=M_XL, w=6.0).move_to(P3(EQX, 1.2))
        c1 = fitw(MathTex(r"\mathbf u:\ \text{velocidade do material (a barra inteira)}", font_size=26,
                          color=VIOLET), 6.2).move_to(P3(EQX, -0.4))
        c2 = fitw(MathTex(r"\mathbf v_d:\ \text{velocidade do portador relativa ao material}", font_size=26,
                          color=GREEN), 6.2).move_to(P3(EQX, -0.95))
        self.an(8, 0)
        self.play(*self.H("Duas velocidades para a mesma carga"), *self.lay("bar"), ap.oI.animate.set_value(0),
                  ap.oQ.animate.set_value(1), ap.drift.animate.set_value(0.3), ap.oTC.animate.set_value(1),
                  *self.hide(L["I"], L["R"], L["Pm"]), ap.oP.animate.set_value(0), FadeOut(self.E),
                  run_time=2.2)
        self.an(8, 1)
        self.play(self.Tu.animate.set_value(1), *self.show(L["uq"]), FadeIn(c1), run_time=1.2)
        self.an(8, 2)
        self.play(self.Tvd.animate.set_value(1), *self.show(L["vd"]), FadeIn(c2), run_time=1.2)
        self.an(8, 3)
        self.play(self.Tw.animate.set_value(1), *self.show(L["w"]), FadeIn(e), run_time=1.2)
        self.E = VGroup(e, c1, c2)
        self.wait(1.5)

    def n09(self):
        ap, L = self.ap, self.L
        self.vFb = self.vec(lambda: ap.qpos(TC), lambda: (-0.36, 0.9), FC, self.Tfb)

        def rmark():
            if self.Tfb.get_value() < 0.5:
                return VMobject()
            o = ap.W(*ap.qpos(TC))
            s = ap.s.get_value()
            uw, uf = P3(1.0, 0.4) / np.linalg.norm([1.0, 0.4]), P3(-0.4, 1.0) / np.linalg.norm([-0.4, 1.0])
            k = 0.2 * s
            return VMobject().set_points_as_corners([o + k * uw, o + k * (uw + uf), o + k * uf]).set_stroke(WHITE, 2.5) \
                .set_z_index(13)
        self.rm = always_redraw(rmark)
        self.add(self.rm)
        e1 = M(r"\mathbf F_B", "=", "q", r"\mathbf w", r"\times", r"\mathbf B", w=6.3).move_to(P3(EQX, 1.5))
        e2 = M(r"\mathbf F_B", r"\cdot", r"\mathbf w", "=", "0", size=M_XL, w=6.0).move_to(P3(EQX, 0.0))
        b2 = boxed(e2)
        self.an(9, 0)
        self.play(*self.H("A força magnética é perpendicular à velocidade total"), FadeOut(self.E), run_time=1.0)
        self.an(9, 1)
        self.play(FadeIn(e1), run_time=1.2)
        self.an(9, 2)
        self.play(self.Tfb.animate.set_value(1), *self.show(L["Fb"]), run_time=1.5)
        self.an(9, 3)
        self.play(FadeIn(e2), Create(b2), run_time=1.5)
        self.E = VGroup(e1, e2, b2)
        self.wait(2.0)

    def n10(self):
        ap, L = self.ap, self.L
        self.an(10, 0)
        self.play(*self.H("O conflito central"), self.Tu.animate.set_value(0), self.Tvd.animate.set_value(0),
                  self.Tw.animate.set_value(0), self.Tfb.animate.set_value(0), ap.oTC.animate.set_value(0),
                  ap.oQ.animate.set_value(0), ap.drift.animate.set_value(0),
                  *self.hide(L["uq"], L["vd"], L["w"], L["Fb"]), *self.lay("top"), ap.oAll.animate.set_value(0.35),
                  FadeOut(self.E), run_time=1.5)
        self.remove(self.vvd, self.vw, self.vFb, self.rm)
        a = M(r"P_R", ">", "0", size=60).move_to(P3(-3.6, -1.2))
        b = M(r"\mathbf F_B", r"\cdot", r"\mathbf w", "=", "0", size=60).move_to(P3(3.6, -1.2))
        ba, bb = boxed(a, buff=0.25), boxed(b, buff=0.25)
        self.play(FadeIn(a), Create(ba), run_time=1.0)
        self.play(FadeIn(b), Create(bb), run_time=1.0)
        self.an(10, 1)
        q = txt("QUEM FORNECE A ENERGIA?", 44, WHITE).move_to(P3(0, -2.9))
        self.play(FadeIn(q, shift=0.1 * UP), run_time=1.2)
        self.E = VGroup(a, b, ba, bb, q)
        self.wait(1.5)

    # ── N11–N13: arrasto, força externa, potência mecânica ──────────────────────────────────────────────────
    def n11(self):
        ap, L = self.ap, self.L
        e1 = M(r"\mathbf F_{\rm mag}", "=", "I", r"\mathbf l", r"\times", r"\mathbf B", w=6.2).move_to(P3(EQX, 1.7))
        e2 = M(r"\mathbf l", r"\times", r"\mathbf B", "=", r"-lB\,\hat x", w=6.2).move_to(P3(EQX, 0.4))
        e3 = M(r"F_{\rm mag}", "=", "IlB", w=5.0).move_to(P3(EQX, -0.9))
        b3 = boxed(e3)
        self.an(11, 0)
        self.play(*self.H("A corrente sente força: arrasto"), FadeOut(self.E), ap.oAll.animate.set_value(1),
                  *self.lay("left"), ap.oI.animate.set_value(1), ap.oF.animate.set_value(1),
                  *self.show(L["I"], L["u"], L["R"]), run_time=2.5)
        self.an(11, 1)
        self.play(FadeIn(e1), run_time=1.2)
        self.an(11, 4)
        self.play(ap.fm.animate.set_value(1), *self.show(L["Fm"]), FadeIn(e2), run_time=1.5)
        self.an(11, 5)
        self.play(FadeIn(e3), Create(b3), run_time=1.2)
        self.E = VGroup(e1, e2, e3, b3)
        self.wait(1.5)

    def n12(self):
        ap, L = self.ap, self.L
        e1 = M("u", r"=\text{constante}", r"\Rightarrow", r"\mathbf F_{\rm ext}", "=", "-", r"\mathbf F_{\rm mag}",
               w=6.4).move_to(P3(EQX, 1.0))
        e2 = M(r"F_{\rm ext}", "=", "IlB", w=5.0).move_to(P3(EQX, -0.4))
        b2 = boxed(e2)
        self.an(12, 0)
        self.play(*self.H("Para manter a velocidade constante, alguém puxa"), FadeOut(self.E), ap.fe.animate.set_value(1),
                  *self.show(L["Fe"]), run_time=1.5)
        self.play(FadeIn(e1), run_time=1.0)
        self.an(12, 1)
        self.play(FadeIn(e2), Create(b2), run_time=1.0)
        self.E = VGroup(e1, e2, b2)
        self.an(12, 2)
        self.wait(1.5)

    def n13(self):
        ap = self.ap
        steps = [
            [r"P_{\rm ext}", "=", r"F_{\rm ext}", "u"],
            [r"P_{\rm ext}", "=", "I", "l", "B", "u"],
            [r"P_{\rm ext}", "=", "I", "(", "B", "l", "u", ")"],
            [r"P_{\rm ext}", "=", "I", r"\mathcal E"],
            [r"P_{\rm ext}", "=", "I^2R"],
            [r"P_{\rm ext}", "=", "I^2R", "=", r"P_R"],
        ]
        eqs = [M(*p, size=M_XL).move_to(P3(0, -0.85)) for p in steps]
        fin = M(r"P_{\rm ext}", "=", r"P_R", size=60).move_to(P3(0, -0.85))
        bf = boxed(fin, buff=0.25)
        self.an(13, 0)
        self.play(*self.H("Potência mecânica = potência dissipada"), FadeOut(self.E), *self.lay("top"), run_time=2.0)
        self.play(FadeIn(eqs[0]), run_time=1.0)
        self.an(13, 1)
        self.play(TransformMatchingTex(eqs[0], eqs[1]), run_time=1.5)
        self.an(13, 2)
        self.play(TransformMatchingTex(eqs[1], eqs[2]), run_time=1.5)
        self.wait(1.0)
        self.play(TransformMatchingTex(eqs[2], eqs[3]), run_time=1.5)
        self.an(13, 3)
        self.play(TransformMatchingTex(eqs[3], eqs[4]), run_time=1.5)
        self.wait(0.8)
        self.play(TransformMatchingTex(eqs[4], eqs[5]), run_time=1.5)
        self.an(13, 4)
        self.play(TransformMatchingTex(eqs[5], fin), run_time=1.5)
        self.play(Create(bf), run_time=0.8)
        self.E = VGroup(fin, bf)
        self.an(13, 5)
        self.wait(2.0)

    # ── N14–N18: fluxo magnético ──────────────────────────────────────────────────────────────────────────────
    def n14(self):
        ap, L = self.ap, self.L
        e = M("A", "=", "l", "x", size=M_XL).move_to(P3(-2.6, -1.2))
        cap = MathTex(r"x:\ \text{distância até a barra}", font_size=28, color=DIM).move_to(P3(-2.6, -2.3))
        ap.moving, ap.vsp, ap.rph = True, 0.02, "run"
        self.an(14, 0)
        note = txt("voltando ao instante inicial", T_CAP, DIM).move_to(P3(0, -2.5))
        self.play(ap.barf.animate.set_value(0), FadeIn(note), run_time=0.4)
        ap.xb.set_value(0.3)
        self.play(*self.H("A mesma geometria, agora vista como fluxo"), FadeOut(self.E), FadeOut(note),
                  ap.barf.animate.set_value(1), ap.oI.animate.set_value(0.5), ap.oF.animate.set_value(0),
                  ap.oU.animate.set_value(0.3), ap.oP.animate.set_value(0),
                  *self.hide(L["I"], L["Fm"], L["Fe"], L["Pm"], L["u"]), run_time=1.8)
        self.an(14, 1)
        self.play(ap.oA.animate.set_value(1), ap.oX.animate.set_value(1), ap.oL.animate.set_value(1),
                  *self.show(L["x"], L["l"]), FadeIn(e), FadeIn(cap), run_time=1.8)
        self.E = VGroup(e, cap)
        self.an(14, 2)
        ap.vsp = 0.2
        self.wait(2.0)

    def n15(self):
        ap, L = self.ap, self.L
        e1 = M(r"\Phi_B", "=", r"\int_S", r"\mathbf B", r"\cdot", r"d\mathbf a", size=M_L).move_to(P3(-2.8, -0.9))
        e2 = M(r"\Phi_B", "=", r"\int_S", r"(-B\,\hat z)", r"\cdot", r"(\hat z\,da)", size=M_L).move_to(P3(-2.8, -0.9))
        e3 = M(r"\Phi_B", "=", r"-Blx", size=M_XL).move_to(P3(-2.8, -0.9))
        b3 = boxed(e3)
        # visão lateral: B antiparalelo a n̂
        o = P3(4.6, -1.7)
        an = arrow(o, o + P3(0, 1.1), WHITE, 6, 9, 0.22)
        ab = arrow(o, o + P3(0, -1.1), MAGENTA, 6, 9, 0.22)
        ln = MathTex(r"\hat{\mathbf n}", font_size=M_M, color=WHITE).next_to(an, RIGHT, buff=0.15)
        lb = MathTex(r"\mathbf B", font_size=M_M, color=MAGENTA).next_to(ab, RIGHT, buff=0.15)
        res = MathTex(r"\mathbf B\cdot\hat{\mathbf n}=-B<0", font_size=M_M, color=WHITE).move_to(P3(4.6, -3.0))
        side = VGroup(an, ab, ln, lb, res)
        ap.vsp = 0.02
        self.an(15, 0)
        self.play(*self.H("Orientação do circuito e sinal do fluxo"), FadeOut(self.E), FadeIn(e1), run_time=1.5)
        self.an(15, 1)
        self.play(ap.oO.animate.set_value(1), *self.show(L["n"], L["C"], L["dl"]), run_time=1.5)
        self.an(15, 2)
        self.play(FadeIn(VGroup(an, ln)), run_time=1.2)
        self.an(15, 3)
        self.play(FadeIn(VGroup(ab, lb, res)), run_time=1.2)
        self.an(15, 4)
        self.play(TransformMatchingTex(e1, e2), run_time=1.5)
        self.wait(0.8)
        self.play(TransformMatchingTex(e2, e3), Create(b3), run_time=1.5)
        self.side = side
        self.E = VGroup(e3, b3)
        self.wait(1.5)

    def n16(self):
        ap, L = self.ap, self.L
        self.gx0 = P3(5.0, -0.3)

        def gauge():
            g = (ap.xb.get_value() - XL) / (XB_MAX - XL)
            ln = 2.4 * g
            r = Rectangle(width=0.55, height=ln).set_fill(MAGENTA, 0.8).set_stroke(width=0)
            r.move_to(self.gx0 + P3(0, -ln / 2))
            z = Line(self.gx0 + P3(-0.55, 0), self.gx0 + P3(0.55, 0), color=DIM, stroke_width=3)
            return VGroup(r, z)
        self.gauge = always_redraw(gauge)
        gl = MathTex(r"\Phi_B", font_size=M_M, color=MAGENTA).move_to(self.gx0 + P3(0, 0.5))
        g0 = MathTex("0", font_size=26, color=DIM).move_to(self.gx0 + P3(-0.9, 0))
        self.gl = VGroup(gl, g0)
        e1 = M(r"\frac{dx}{dt}", "=", "u", size=M_L).move_to(P3(-2.8, -1.0))
        e2 = M(r"\frac{d\Phi_B}{dt}", "=", "-Bl", r"\frac{dx}{dt}", size=M_L).move_to(P3(-2.8, -2.3))
        e3 = M(r"\frac{d\Phi_B}{dt}", "=", "-Blu", size=M_XL).move_to(P3(-2.8, -2.3))
        b3 = boxed(e3)
        self.an(16, 0)
        ap.vsp = 0.2                          # x cresce de forma monótona, sem reinício
        self.play(*self.H("A barra anda: o fluxo varia"), FadeOut(self.side),
                  FadeIn(self.gauge), FadeIn(self.gl), ap.oU.animate.set_value(0.6), FadeOut(self.E),
                  run_time=1.5)
        self.play(FadeIn(e1), run_time=1.0)
        self.an(16, 1)
        self.play(FadeIn(e2), run_time=1.2)
        self.wait(1.5)
        self.play(TransformMatchingTex(e2, e3), Create(b3), run_time=1.5)
        self.E = VGroup(e1, e3, b3)
        self.an(16, 2)
        self.wait(2.0)

    def n17(self):
        ap, L = self.ap, self.L
        a = M(r"\mathcal E", "=", "Blu", size=M_XL).move_to(P3(-3.6, -1.6))
        b = M(r"\frac{d\Phi_B}{dt}", "=", "-Blu", size=M_XL).move_to(P3(3.6, -1.6))
        ba, bb = boxed(a), boxed(b)
        ap.vsp = 0.02
        self.an(17, 0)
        self.play(*self.H("Reconhecimento"), FadeOut(self.E), FadeOut(self.gauge), FadeOut(self.gl), run_time=1.2)
        self.play(FadeIn(a), Create(ba), run_time=1.2)
        self.an(17, 1)
        self.play(FadeIn(b), Create(bb), run_time=1.2)
        self.a17, self.b17, self.x17 = a, b, VGroup(ba, bb)
        self.an(17, 2)
        self.wait(1.5)

    def n18(self):
        ap, L = self.ap, self.L
        a = self.a17
        mid = M(r"\mathcal E", "=", "Blu", "=", "-", r"\frac{d\Phi_B}{dt}", size=M_XL).move_to(P3(0, -1.6))
        fin = M(r"\mathcal E", "=", "-", r"\frac{d\Phi_B}{dt}", size=60).move_to(P3(0, -1.6))
        bf = boxed(fin, buff=0.25)
        self.an(18, 0)
        self.play(*self.H("Fem = menos a taxa de variação do fluxo"), FadeOut(self.x17), run_time=1.0)
        self.play(FadeOut(self.b17), run_time=0.8)
        self.wait(0.4)
        self.play(TransformMatchingTex(a, mid), run_time=2.0)
        self.wait(1.0)
        self.play(TransformMatchingTex(mid, fin), run_time=1.5)
        self.play(Create(bf), run_time=1.0)
        self.E = VGroup(fin, bf)
        self.an(18, 1)
        self.wait(2.0)

    # ── N19–N25: contorno geral e faixa varrida ──────────────────────────────────────────────────────────────
    def blob_pts(self, n=60):
        c, ax, ay = P3(-3.2, -0.1), 2.5, 1.55
        pts = []
        for k in range(n):
            th = 2 * PI * k / n
            r = 1 + 0.10 * math.cos(2 * th + 0.6) + 0.06 * math.sin(3 * th)
            pts.append(c + P3(ax * r * math.cos(th), ay * r * math.sin(th)))
        return pts

    def disp(self, p):
        x0, ax = -3.2 + 0.1, 2.5
        t = min(1.0, max(0.0, (p[0] - x0) / (1.3 * ax)))
        return P3(0.75 * t * t * (3 - 2 * t), 0)

    def n19(self):
        ap, L = self.ap, self.L
        ap.moving = False
        ap.barf.set_value(1.0)
        rect_pts = [self.Wl("top", XL, YB), self.Wl("top", ap.xb.get_value(), YB), self.Wl("top", ap.xb.get_value(), YT),
                    self.Wl("top", XL, YT)]
        contour = Polygon(*rect_pts, color=WHITE, stroke_width=4).set_z_index(10)
        pts = self.blob_pts()
        self.pts = pts
        blob = Polygon(*pts, color=WHITE, stroke_width=4).set_z_index(10)
        # fundo de B (estático) atrás do contorno
        mk, a = VMobject(), 0.1
        for x in np.arange(-6.6, 0.3, 0.6):
            for y in np.arange(-2.3, 2.3, 0.6):
                c = P3(x, y)
                mk.start_new_path(c + P3(-a, -a)); mk.add_line_to(c + P3(a, a))
                mk.start_new_path(c + P3(-a, a)); mk.add_line_to(c + P3(a, -a))
        self.bg = mk.set_stroke(MAGENTA, 2.0, 0.35).set_fill(opacity=0).set_z_index(0)
        tan = VGroup(*[arrow(pts[i], pts[i] + 0.45 * (pts[(i + 1) % 60] - pts[i]) / np.linalg.norm(pts[(i + 1) % 60] - pts[i]),
                             WHITE, 5, 11, 0.16) for i in (3, 18, 33, 48)])
        ctr = P3(-3.2, -0.1)
        sym = VGroup(Circle(radius=0.14).set_stroke(WHITE, 2.5).move_to(ctr), Dot(ctr, radius=0.04).set_fill(WHITE, 1))
        ln = MathTex(r"\hat{\mathbf n}=+\hat z", font_size=26, color=WHITE).move_to(ctr + P3(0, -0.5))
        lc = MathTex(r"C(t)", font_size=M_M, color=WHITE).move_to(P3(-6.2, 1.5))
        self.cg = VGroup(blob, tan, sym, ln, lc)
        self.an(19, 0)
        self.play(*self.H("Um contorno qualquer"), FadeOut(self.E), run_time=1.2)
        self.add(contour)
        self.play(FadeIn(self.bg), ap.oAll.animate.set_value(0), run_time=1.0)
        self.an(19, 1)
        self.play(Transform(contour, blob), run_time=2.5)
        self.remove(contour)
        self.add(blob)
        self.an(19, 2)
        self.play(FadeIn(VGroup(tan, sym, ln, lc)), run_time=1.5)
        self.E = VGroup()
        self.an(19, 3)
        self.wait(1.5)

    def n20(self):
        pts = self.pts
        n = len(pts)
        d = [self.disp(p) for p in pts]
        strips = VGroup(*[Polygon(pts[i], pts[(i + 1) % n], pts[(i + 1) % n] + d[(i + 1) % n], pts[i] + d[i])
                          .set_fill(CYAN, 0.38).set_stroke(width=0).set_z_index(2)
                          for i in range(n) if np.linalg.norm(d[i]) > 0.01 or np.linalg.norm(d[(i + 1) % n]) > 0.01])
        c2 = DashedVMobject(Polygon(*[p + dd for p, dd in zip(pts, d)], color=CYAN, stroke_width=3.5), num_dashes=120)
        c2.set_z_index(10)
        ua = VGroup(*[arrow(pts[i], pts[i] + d[i], VIOLET, 5, 12, 0.16) for i in range(0, n, 4)
                      if np.linalg.norm(d[i]) > 0.15])
        lc2 = MathTex(r"C(t+dt)", font_size=M_M, color=CYAN).move_to(P3(0.2, 1.7))
        lb = MathTex(r"\text{faixa varrida}", font_size=M_S, color=CYAN).move_to(P3(0.6, -2.3))
        self.strips, self.c2, self.ua, self.lc2, self.lb = strips, c2, ua, lc2, lb
        self.pulse(list(strips), 0.22, 0.5, 2.6)
        self.pulse(list(ua), 0.55, 1.0, 1.8)
        self.an(20, 0)
        self.play(*self.H("Dois instantes do contorno"), run_time=1.0)
        self.play(FadeIn(ua), run_time=1.0)
        self.play(Create(c2), run_time=1.5)
        self.an(20, 1)
        self.play(FadeIn(strips), FadeIn(lc2), FadeIn(lb), run_time=1.5)
        self.E = VGroup()
        self.an(20, 2)
        self.wait(2.0)

    def n21(self):
        pts = self.pts
        i = 51
        t_hat = (pts[(i + 1) % 60] - pts[i]) / np.linalg.norm(pts[(i + 1) % 60] - pts[i])
        o = P3(2.9, -0.5)
        dl, udt = t_hat * 1.6, P3(1.5, 0)
        ring = Circle(radius=2.0).set_stroke(DIM, 2.5).move_to(P3(3.9, 0.5))
        link = Line(pts[i] + P3(0.05, 0), ring.get_left() + P3(0.02, 0), color=DIM, stroke_width=2)
        mark = Circle(radius=0.2).set_stroke(DIM, 2.5).move_to(pts[i])
        a_dl = arrow(o, o + dl, WHITE, 6, 12, 0.2)
        a_ud = arrow(o, o + udt, VIOLET, 6, 12, 0.2)
        para = Polygon(o, o + dl, o + dl + udt, o + udt).set_fill(CYAN, 0.35).set_stroke(CYAN, 2).set_z_index(2)
        a_dl2 = arrow(o + udt, o + udt + dl, WHITE, 3, 12, 0.14, 0.5)
        a_ud2 = arrow(o + dl, o + dl + udt, VIOLET, 3, 12, 0.14, 0.5)
        cen = o + 0.5 * (dl + udt)
        sym = VGroup(Circle(radius=0.15).set_stroke(WHITE, 2.5).move_to(cen), Dot(cen, radius=0.045).set_fill(WHITE, 1))
        l_dl = MathTex(r"d\boldsymbol\ell", font_size=M_S, color=WHITE).move_to(o + dl * 0.5 + P3(-0.55, 0.15))
        l_ud = MathTex(r"\mathbf u\,dt", font_size=M_S, color=VIOLET).move_to(o + udt * 0.5 + P3(0, -0.35))
        l_da = MathTex(r"d\mathbf a", font_size=M_S, color=CYAN).move_to(cen + P3(0.55, 0.0))
        eq = M(r"d\mathbf a", "=", "(", r"\mathbf u", r"\times", r"d\boldsymbol\ell", ")", "dt", size=M_L, w=6.0) \
            .move_to(P3(3.9, -2.2))
        eq[0].set_color(CYAN)
        self.lg = VGroup(ring, link, mark, a_dl, a_ud, para, a_dl2, a_ud2, sym, l_dl, l_ud, l_da, eq)
        self.pulse(para, 0.2, 0.5, 2.4)
        self.an(21, 0)
        self.play(*self.H("Um elemento da faixa"), Create(mark), Create(link), Create(ring), run_time=1.5)
        self.an(21, 1)
        self.play(Create(a_dl), FadeIn(l_dl), run_time=1.2)
        self.an(21, 2)
        self.play(Create(a_ud), FadeIn(l_ud), run_time=1.2)
        self.an(21, 3)
        self.play(FadeIn(a_dl2), FadeIn(a_ud2), FadeIn(para), run_time=1.5)
        self.an(21, 4)
        self.play(FadeIn(sym), FadeIn(l_da), run_time=1.2)
        self.an(21, 5)
        self.play(FadeIn(eq), run_time=1.5)
        self.wait(2.0)

    def n22(self):
        ap, L = self.ap, self.L
        self.an(22, 0)
        self.play(*self.H("Teste na barra: o sinal antes da álgebra"),
                  FadeOut(self.lg), FadeOut(self.cg), FadeOut(self.bg), FadeOut(self.strips), FadeOut(self.c2),
                  FadeOut(self.ua), FadeOut(self.lc2), FadeOut(self.lb), run_time=1.0)
        ap.oHB.set_value(1.0)
        ap.moving, ap.vsp = True, 0.02
        ap.oA.set_value(0.0)
        ap.oX.set_value(0.0)
        ap.oL.set_value(0.0)
        ap.oO.set_value(0.0)
        ap.oI.set_value(0.5)
        ap.oU.set_value(0.0)
        for m in (L["x"], L["l"], L["n"], L["C"], L["dl"]):
            m.v.set_value(0)
        self.play(*self.lay("top"), ap.oAll.animate.set_value(1), run_time=1.5)
        o = P3(-5.4, -2.1)
        dl, udt = P3(0, 1.5), P3(1.5, 0)
        a_dl, a_ud = arrow(o, o + dl, WHITE, 6, 12, 0.2), arrow(o, o + udt, VIOLET, 6, 12, 0.2)
        para = Polygon(o, o + dl, o + dl + udt, o + udt).set_fill(CYAN, 0.3).set_stroke(CYAN, 2).set_z_index(2)
        cen = o + 0.5 * (dl + udt)
        sym = VGroup(Circle(radius=0.15).set_stroke(WHITE, 2.5).move_to(cen), Dot(cen, radius=0.045).set_fill(WHITE, 1))
        l_dl = MathTex(r"d\boldsymbol\ell", font_size=M_S, color=WHITE).move_to(o + dl * 0.5 + P3(-0.6, 0))
        l_ud = MathTex(r"\mathbf u\,dt", font_size=M_S, color=VIOLET).move_to(o + udt * 0.5 + P3(0, -0.35))
        l_da = MathTex(r"d\mathbf a", font_size=M_S, color=CYAN).move_to(cen + P3(0.55, 0))
        self.ins = VGroup(a_dl, a_ud, para, sym, l_dl, l_ud, l_da)
        self.pulse(para, 0.2, 0.5, 2.4)
        e1 = M(r"d\boldsymbol\ell", "=", r"+d\ell\,\hat y", ",", r"\quad", r"\mathbf u", "=", r"+u\,\hat x", size=M_M) \
            .move_to(P3(1.9, -1.0))
        e2 = M(r"\mathbf u", r"\times", r"d\boldsymbol\ell", "=", r"+u\,d\ell\,\hat z", size=M_M).move_to(P3(1.9, -1.9))
        e3 = M(r"\mathbf B", r"\cdot", r"d\mathbf a", "<", "0", size=M_L).move_to(P3(1.9, -2.9))
        b3 = boxed(e3)
        self.play(Create(a_dl), FadeIn(l_dl), Create(a_ud), FadeIn(l_ud), run_time=1.2)
        self.play(FadeIn(e1), run_time=1.0)
        self.an(22, 1)
        self.play(FadeIn(para), FadeIn(sym), FadeIn(l_da), FadeIn(e2), run_time=1.5)
        self.an(22, 3)
        self.play(FadeIn(e3), Create(b3), run_time=1.5)
        self.e22 = VGroup(e1, e2, e3, b3)
        self.an(22, 4)
        self.wait(1.5)

    def n23(self):
        ap, L = self.ap, self.L
        ap.oHB.set_value(0.0)
        e = M(r"\frac{d\Phi_B}{dt}", "=", r"\oint", r"\mathbf B", r"\cdot", "(", r"\mathbf u", r"\times",
              r"d\boldsymbol\ell", ")", size=M_L, w=6.4).move_to(P3(EQX, 0.9))
        self.an(23, 0)
        self.play(*self.H("A faixa inteira"), FadeOut(self.ins), FadeOut(self.e22), ap.oAll.animate.set_value(0),
                  run_time=1.2)
        self.play(FadeIn(self.bg), FadeIn(self.cg), FadeIn(self.strips), FadeIn(self.c2), FadeIn(self.ua), run_time=1.2)
        self.an(23, 1)
        self.play(FadeIn(e), run_time=1.5)
        self.E = VGroup(e)
        self.e23 = e
        self.an(23, 2)
        self.wait(2.0)

    def n24(self):
        a = self.e23
        parts = [
            [r"\frac{d\Phi_B}{dt}", "=", r"\oint", "(", r"\mathbf B", r"\times", r"\mathbf u", ")", r"\cdot",
             r"d\boldsymbol\ell"],
            [r"\frac{d\Phi_B}{dt}", "=", "-", r"\oint", "(", r"\mathbf u", r"\times", r"\mathbf B", ")", r"\cdot",
             r"d\boldsymbol\ell"],
        ]
        b = M(*parts[0], size=M_L, w=6.4).move_to(P3(EQX, 0.9))
        c = M(*parts[1], size=M_L, w=6.4).move_to(P3(EQX, 0.9))
        cap1 = MathTex(r"\mathbf B\cdot(\mathbf u\times d\boldsymbol\ell)=(\mathbf B\times\mathbf u)\cdot d\boldsymbol\ell", font_size=26, color=DIM).move_to(P3(EQX, -0.4))
        cap2 = MathTex(r"\mathbf B\times\mathbf u=-\,\mathbf u\times\mathbf B", font_size=26, color=DIM).move_to(P3(EQX, -1.1))
        self.an(24, 0)
        self.play(*self.H("Produto escalar triplo"), run_time=1.0)
        self.an(24, 1)
        self.play(TransformMatchingTex(a, b), FadeIn(cap1), run_time=2.0)
        self.an(24, 3)
        self.play(TransformMatchingTex(b, c), FadeIn(cap2), run_time=2.0)
        self.e24 = c
        self.E = VGroup(c, cap1, cap2)
        self.an(24, 4)
        self.wait(1.5)

    def n25(self):
        c = self.e24
        fin1 = M(r"\frac{d\Phi_B}{dt}", "=", "-", r"\mathcal E", size=M_XL).move_to(P3(EQX, 0.9))
        fin2 = M(r"\mathcal E", "=", "-", r"\frac{d\Phi_B}{dt}", size=M_XL).move_to(P3(EQX, 0.9))
        bf = boxed(fin2, buff=0.2)
        cap = MathTex(r"\mathcal E=\oint(\mathbf u\times\mathbf B)\cdot d\boldsymbol\ell", font_size=30, color=CYAN).move_to(P3(EQX, -0.4))
        note = txt("Campo magnético estacionário; circuito em movimento.", T_NOTE, DIM).move_to(P3(1.2, -3.1))
        self.an(25, 0)
        self.play(*self.H("A regra do fluxo, provada"), FadeOut(self.E[1]), FadeOut(self.E[2]), FadeIn(cap), run_time=1.2)
        self.an(25, 1)
        self.play(TransformMatchingTex(c, fin1), run_time=2.0)
        self.an(25, 2)
        self.play(TransformMatchingTex(fin1, fin2), FadeOut(cap), run_time=1.5)
        self.play(Create(bf), run_time=0.8)
        self.an(25, 3)
        self.play(FadeIn(note), run_time=1.0)
        self.E = VGroup(fin2, bf, note)
        self.wait(1.5)

    # ── N26–N34: volta aos trilhos, barra livre, exponencial ─────────────────────────────────────────────────
    def n26(self):
        ap, L = self.ap, self.L
        ap.mode, ap.moving, ap.rph, ap.frozen, ap.vsp = "forced", True, "run", False, 0.55
        ap.xb.set_value(1.2)
        ap.barf.set_value(1.0)
        for tr, v in ((ap.oU, 1), (ap.oI, 1), (ap.oF, 1), (ap.oA, 0), (ap.oX, 0), (ap.oL, 0), (ap.oO, 0), (ap.oP, 0),
                      (ap.oHB, 0), (ap.cur, 1), (ap.heat, 1), (ap.fm, 1), (ap.fe, 1), (ap.ua, 1), (ap.fol, 0),
                      (ap.s, LAYOUTS["full"][0]), (ap.cx, LAYOUTS["full"][1]), (ap.cy, LAYOUTS["full"][2])):
            tr.set_value(v)
        xb = ap.xb.get_value()
        tgt = Polygon(self.Wl("full", XL, YB), self.Wl("full", xb, YB), self.Wl("full", xb, YT), self.Wl("full", XL, YT),
                      color=WHITE, stroke_width=4).set_z_index(10)
        big = self.cg[0]
        self.an(26, 0)
        self.play(*self.H("De volta ao mesmo aparato"), FadeOut(self.E), FadeOut(self.strips), FadeOut(self.c2),
                  FadeOut(self.ua), FadeOut(VGroup(*self.cg[1:])), run_time=1.0)
        self.play(Transform(big, tgt), FadeOut(self.bg), run_time=2.0)
        ap.oAll.set_value(0.0)
        self.remove(big)
        self.play(ap.oAll.animate.set_value(1), *self.show(L["u"], L["I"], L["Fm"], L["Fe"], L["R"]), run_time=1.5)
        self.an(26, 1)
        self.wait(1.5)

    def n27(self):
        ap, L = self.ap, self.L
        ap.mode, ap.moving, ap.rph, ap.frozen, ap.autoloop = "forced", False, "run", True, False
        ap.barf.set_value(1.0)                 # instante t = 0: nada evolui até o N35
        e = M("t", "=", "0", ":", r"\quad", "u(0)", "=", "u_0", size=M_XL, w=6.2).move_to(P3(EQX, 0.4))
        b = boxed(e)
        bt = MathTex(r"t=0\ \cdot\ \text{imagem congelada}", font_size=34, color=WHITE)
        self.badge = VGroup(bt, boxed(bt, color=CYAN, buff=0.16, width=3)).move_to(P3(-3.4, -1.75)).set_z_index(30)
        self.an(27, 0)
        self.play(*self.H("Sem ninguém puxando"), *self.lay("left"), ap.fe.animate.set_value(0),
                  *self.hide(L["Fe"]), run_time=2.0)
        self.play(FadeIn(e), Create(b), run_time=1.0)
        self.E = VGroup(e, b)
        self.an(27, 1)
        self.play(FadeIn(self.badge), run_time=0.8)
        self.an(27, 2)
        self.wait(2.0)

    def n28(self):
        e1 = M("u", ">", "0", r"\Rightarrow", r"\mathcal E", "=", "Blu", w=6.3).move_to(P3(EQX, 1.3))
        e2 = M("I", "=", r"\frac{Blu}{R}", w=5.0).move_to(P3(EQX, -0.1))
        self.an(28, 0)
        self.play(*self.H("Enquanto a barra se move, há corrente"), FadeOut(self.E), FadeIn(e1), run_time=1.5)
        self.an(28, 1)
        self.play(FadeIn(e2), run_time=1.2)
        self.E = VGroup(e1, e2)
        self.an(28, 2)
        self.wait(1.5)

    def n29(self):
        a = M(r"F_x", "=", "-", r"F_{\rm mag}").move_to(P3(EQX, 1.4))
        b = M(r"F_x", "=", "-", "I", "lB").move_to(P3(EQX, 1.4))
        c = M(r"F_x", "=", "-", r"\left(\frac{Blu}{R}\right)", "lB").move_to(P3(EQX, 1.4))
        d = M(r"F_x", "=", r"-\frac{B^2l^2}{R}", "u").move_to(P3(EQX, 1.4))
        s1 = MathTex(r"F_{\rm mag}=IlB", font_size=30, color=FC).move_to(P3(EQX, 0.1))
        s2 = MathTex(r"I=\frac{Blu}{R}", font_size=30, color=GREEN).move_to(P3(EQX, -0.9))
        self.an(29, 0)
        self.play(*self.H("A força em função da velocidade"), FadeOut(self.E), run_time=1.0)
        self.put(a, 1.2)
        self.an(29, 1)
        self.play(FadeIn(s1), run_time=0.8)
        self.morph(a, b)
        self.an(29, 2)
        self.play(FadeIn(s2), run_time=0.8)
        self.morph(b, c)
        self.an(29, 3)
        self.morph(c, d)
        self.play(FadeOut(s1), FadeOut(s2), run_time=0.8)
        self.an(29, 4)
        bd = boxed(d)
        self.play(Create(bd), run_time=1.0)
        self.E = VGroup(d, bd)
        self.wait(1.5)

    def n30(self):
        d, bd = self.E
        f1 = M("m", r"\frac{du}{dt}", "=", r"F_x").move_to(P3(EQX, 2.0))
        f2 = M("m", r"\frac{du}{dt}", "=", r"-\frac{B^2l^2}{R}", "u").move_to(P3(EQX, 2.0))
        cap = MathTex(r"m:\ \text{massa da barra}", font_size=26, color=DIM).move_to(P3(EQX, 0.9))
        self.an(30, 0)
        self.play(*self.H("Segunda lei de Newton"), FadeOut(bd), d.animate.move_to(P3(EQX, -0.2)), run_time=1.2)
        self.put(f1, 1.2)
        self.play(FadeIn(cap), run_time=0.8)
        self.an(30, 1)
        self.morph(f1, f2)
        self.play(FadeOut(d), run_time=0.8)
        self.an(30, 2)
        bf2 = boxed(f2)
        self.play(Create(bf2), run_time=1.0)
        self.E = VGroup(f2, bf2, cap)
        self.an(30, 3)
        self.wait(1.5)

    def n31(self):
        f2, bf2, cap = self.E
        s1 = M(r"\frac{1}{u}", r"\frac{du}{dt}", "=", r"-\frac{B^2l^2}{mR}").move_to(P3(EQX, 1.6))
        s2 = M(r"\frac{du}{u}", "=", r"-\frac{B^2l^2}{mR}", "dt").move_to(P3(EQX, 1.6))
        a1 = MathTex(r"\text{dividindo por }mu", font_size=28, color=DIM).move_to(P3(EQX, 0.4))
        a2 = MathTex(r"\text{multiplicando por }dt", font_size=28, color=DIM).move_to(P3(EQX, 0.4))
        self.an(31, 0)
        self.play(*self.H("Separando as variáveis"), FadeOut(bf2), FadeOut(cap),
                  f2.animate.move_to(P3(EQX, 1.6)), run_time=1.2)
        self.an(31, 1)
        self.play(FadeIn(a1), run_time=0.8)
        self.morph(f2, s1)
        self.an(31, 2)
        self.play(FadeOut(a1), FadeIn(a2), run_time=0.8)
        self.morph(s1, s2)
        self.an(31, 5)
        self.E = VGroup(s2, a2)
        self.wait(1.5)

    def n32(self):
        s2, a2 = self.E
        i1 = M(r"\int_{u_0}^{u}", r"\frac{du'}{u'}", "=", r"-\frac{B^2l^2}{mR}", r"\int_0^t", "dt'", w=6.4) \
            .move_to(P3(EQX, 1.6))
        i2 = M(r"\ln\frac{u}{u_0}", "=", r"-\frac{B^2l^2}{mR}", "t").move_to(P3(EQX, 1.6))
        a3 = MathTex(r"\text{integrando, com }u(0)=u_0", font_size=28, color=DIM).move_to(P3(EQX, 0.4))
        self.an(32, 0)
        self.play(*self.H("Integrando com a condição inicial"), FadeOut(a2), FadeIn(a3), run_time=1.0)
        self.morph(s2, i1)
        self.an(32, 1)
        self.wait(1.0)
        self.morph(i1, i2)
        self.an(32, 3)
        self.E = VGroup(i2, a3)
        self.wait(1.5)

    def n33(self):
        i2, a3 = self.E
        tau = M(r"\tau", "=", r"\frac{mR}{B^2l^2}", size=M_L).move_to(P3(EQX - 1.0, -0.9))
        tb = boxed(tau)
        tn = MathTex(r"\frac{B^2l^2}{mR}\ \to\ \frac{1}{\tau}", font_size=30, color=DIM).move_to(P3(EQX + 2.1, -0.9))
        i2b = M(r"\ln\frac{u}{u_0}", "=", "-", r"\frac{1}{\tau}", "t").move_to(P3(EQX, 1.6))
        i3 = M(r"\ln\frac{u}{u_0}", "=", "-", r"\frac{t}{\tau}").move_to(P3(EQX, 1.6))
        i4 = M(r"\frac{u}{u_0}", "=", r"e^{-t/\tau}").move_to(P3(EQX, 1.6))
        i5 = M("u(t)", "=", "u_0", r"e^{-t/\tau}", size=M_XL).move_to(P3(EQX, 1.6))
        ea = MathTex(r"\text{exponenciando os dois lados}", font_size=28, color=DIM).move_to(P3(EQX, 0.4))
        self.an(33, 0)
        self.play(*self.H("Decaimento exponencial"), FadeOut(a3), run_time=1.0)
        self.an(33, 1)
        self.play(FadeIn(tau), Create(tb), FadeIn(tn), run_time=1.5)
        self.an(33, 2)
        self.morph(i2, i2b)
        self.wait(0.8)
        self.morph(i2b, i3)
        self.an(33, 3)
        self.play(FadeIn(ea), run_time=0.8)
        self.morph(i3, i4)
        self.an(33, 4)
        self.play(FadeOut(ea), run_time=0.6)
        self.morph(i4, i5)
        self.an(33, 5)
        b5 = boxed(i5)
        self.play(Create(b5), run_time=1.0)
        self.E = VGroup(i5, b5, tau, tb, tn)
        self.wait(1.5)

    def mk_axes(self):
        ax = Axes(x_range=[0, TT_END * TAU, TAU], y_range=[0, 1.1, 0.5], x_length=5.6, y_length=2.9, tips=False,
                  axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False}).move_to(P3(4.2, -1.0))
        self.ax = ax
        ticks = VGroup()
        for k in (1, 2, 3, 4):
            ticks.add(Line(ax.c2p(k * TAU, 0), ax.c2p(k * TAU, 0.06), color=DIM, stroke_width=2))
            ticks.add(MathTex(r"\tau" if k == 1 else rf"{k}\tau", font_size=24, color=DIM)
                      .move_to(ax.c2p(k * TAU, 0) + P3(0, -0.28)))
        ticks.add(MathTex("1", font_size=24, color=DIM).move_to(ax.c2p(0, 1.0) + P3(-0.25, 0)))
        ticks.add(MathTex("0", font_size=24, color=DIM).move_to(ax.c2p(0, 0) + P3(-0.25, 0)))
        ticks.add(Line(ax.c2p(0, 1.0), ax.c2p(0.08 * TAU, 1.0), color=DIM, stroke_width=2))
        xl = MathTex(r"t", font_size=26, color=DIM).move_to(ax.c2p(TT_END * TAU, 0) + P3(0.1, -0.3))
        self.axg = VGroup(ax, ticks, xl)
        return self.axg

    def curve(self, fn, color, width=5, z=6, tr=None):
        """fn(s) com s = t/τ; o gráfico usa o tempo físico t = τ·s."""
        ax, ap = self.ax, self.ap
        tr = tr if tr is not None else ap.tt
        op = ValueTracker(1)

        def mk():
            t = tr.get_value() * TAU
            if t < 0.1 * TAU:
                return VMobject()
            return ax.plot(lambda x: fn(x / TAU), x_range=[0, t, 0.05 * TAU], color=color, stroke_width=width,
                           use_smoothing=False).set_stroke(opacity=op.get_value()).set_z_index(z)
        m = always_redraw(mk)
        m.op = op
        self.add(m)
        return m

    def mk_marker(self):
        """Indicador de t sobre o gráfico: o mesmo tracker do aparato."""
        ax, ap = self.ax, self.ap

        def mk():
            s_ = ap.tt.get_value()
            if s_ < 0.02 or s_ > TT_END - 0.03 or self.mop.get_value() < 0.5:
                return VMobject()
            t = s_ * TAU
            ln = DashedLine(ax.c2p(t, 0), ax.c2p(t, 1.05), dash_length=0.08, color=WHITE, stroke_width=2) \
                .set_opacity(0.55)
            return VGroup(ln, Dot(ax.c2p(t, self.mfn(s_)), radius=0.08).set_fill(WHITE, 1)).set_z_index(9)
        self.mop, self.mfn = ValueTracker(1), (lambda s_: math.exp(-s_))
        self.marker = always_redraw(mk)
        self.add(self.marker)

    def n34(self):
        ap = self.ap
        e = M(r"\tau", "=", r"\frac{mR}{B^2l^2}", size=M_XL, w=5.0).move_to(P3(EQX, 2.0))
        eb = boxed(e)
        axg = self.mk_axes()
        ax = self.ax
        self.tg = ValueTracker(0)
        self.cu = self.curve(lambda t: math.exp(-t), VIOLET, 5, tr=self.tg)
        ylab = MathTex(r"u/u_0", font_size=26, color=VIOLET).move_to(ax.c2p(0, 1.1) + P3(0.55, 0.12))
        self.ylab = ylab
        mk1 = VGroup(Line(ax.c2p(TAU, 0), ax.c2p(TAU, math.exp(-1)), color=WHITE, stroke_width=2),
                     Dot(ax.c2p(TAU, math.exp(-1)), radius=0.07).set_fill(WHITE, 1),
                     MathTex(r"1/e", font_size=24, color=WHITE).move_to(ax.c2p(TAU, math.exp(-1)) + P3(0.55, 0.15)))
        self.mk1 = mk1
        self.an(34, 0)
        self.play(*self.H("A escala de tempo da desaceleração"), FadeOut(self.E), FadeIn(e), Create(eb), FadeIn(axg),
                  FadeIn(ylab), run_time=2.0)
        self.play(self.tg.animate.set_value(TT_END), run_time=3.5, rate_func=linear)
        self.play(FadeIn(mk1), run_time=1.0)
        self.E = VGroup(e, eb)
        self.an(34, 1)
        self.wait(1.5)

    def n35(self):
        ap, L = self.ap, self.L
        e = M("u(t)", "=", "u_0", r"e^{-t/\tau}", size=M_L, w=5.4).move_to(P3(EQX, 1.9))
        self.an(35, 0)
        self.play(*self.H("A barra freia: o mesmo tempo move tudo"), FadeOut(self.E), FadeOut(self.mk1), FadeIn(e),
                  FadeOut(self.badge), *self.setgl(["m", "R", "u", "tau"]), ap.oAll.animate.set_value(1),
                  run_time=1.2)
        self.remove(self.cu)
        self.cu = self.curve(lambda t: math.exp(-t), VIOLET, 5)
        self.mk_marker()
        self.restart_decay(r"\text{soltura}\ \cdot\ t=0")
        self.an(35, 1)
        self.decay_until(self.unit_end(35) - 0.5)
        self.E = VGroup(e)
        self.wait(2.0)

    def n36(self):
        ap, L = self.ap, self.L
        e0 = M("I_0", "=", r"\frac{Blu_0}{R}", size=M_M, w=3.0).move_to(P3(EQX - 0.9, 2.3))
        b0 = boxed(e0, buff=0.1, width=2)
        c0 = txt("corrente inicial", T_CAP, DIM).next_to(b0, RIGHT, buff=0.25)
        e1 = M("I(t)", "=", r"\frac{Bl}{R}", "u(t)", size=M_L, w=4.6).move_to(P3(EQX, 1.25))
        e2 = M("I(t)", "=", "I_0", r"e^{-t/\tau}", size=M_L, w=4.8).move_to(P3(EQX, 1.25))
        self.an(36, 0)
        self.play(*self.H("A corrente acompanha a velocidade"), FadeOut(self.E), *self.setgl(["R", "u", "I0", "tau"]),
                  run_time=1.0)
        self.restart_decay()
        self.decay_until(self.unit_end(36) - 0.5)
        self.an(36, 1)
        self.play(FadeIn(e0), Create(b0), FadeIn(c0), FadeIn(e1), run_time=1.5)
        self.remove(e1)
        self.add(*e1.submobjects)
        self.an(36, 3)
        self.morph(e1, e2)
        b2 = boxed(e2)
        self.play(Create(b2), run_time=0.8)
        self.E = VGroup(e0, b0, c0, e2, b2)
        self.wait(2.0)

    def n37(self):
        ap = self.ap
        self.ci = self.curve(lambda t: math.exp(-t), GREEN, 3, 7)
        e = M(r"\frac{I}{I_0}", "=", r"\frac{u}{u_0}", "=", r"e^{-t/\tau}", size=M_L, w=5.6).move_to(P3(EQX, 2.05))
        eb = boxed(e)
        lg = VGroup(MathTex(r"u/u_0", font_size=26, color=VIOLET), MathTex(r"I/I_0", font_size=26, color=GREEN)) \
            .arrange(RIGHT, buff=0.45).move_to(P3(EQX, 1.0))
        yl = MathTex(r"\text{razões adimensionais}", font_size=24, color=DIM).move_to(self.ax.c2p(0, 1.1) + P3(1.2, 0.12))
        self.an(37, 0)
        self.play(*self.H("Mesmos eixos, curvas que coincidem"), FadeOut(self.E), FadeOut(self.ylab), FadeIn(yl),
                  FadeIn(e), Create(eb), FadeIn(lg), run_time=1.5)
        self.ylab = yl
        self.E = VGroup(e, eb, lg)
        self.restart_decay()
        self.decay_until(self.unit_end(37) - 0.5)
        self.an(37, 1)
        self.wait(2.0)

    def n38(self):
        ap, L = self.ap, self.L
        self.cp = self.curve(lambda t: math.exp(-2 * t), HEAT, 5, 8)
        self.mfn = lambda s_: math.exp(-2 * s_)       # o marcador passa a seguir P_R/P_0
        lg2 = VGroup(MathTex(r"u/u_0", font_size=24, color=VIOLET), MathTex(r"I/I_0", font_size=24, color=GREEN),
                     MathTex(r"P_R/P_0", font_size=24, color=HEAT)).arrange(RIGHT, buff=0.4).move_to(P3(EQX, 0.66))
        p0 = M("P_0", "=", "I_0^2R", size=M_M, w=3.0).move_to(P3(EQX - 0.9, 2.55))
        b0 = boxed(p0, buff=0.1, width=2)
        c0 = txt("potência inicial", T_CAP, DIM).next_to(b0, RIGHT, buff=0.25)
        e2 = M(r"\frac{P_R}{P_0}", "=", r"e^{-2t/\tau}", size=M_L, w=4.6).move_to(P3(EQX, 1.45))
        b2 = boxed(e2)
        self.an(38, 0)
        self.play(*self.H("A potência cai com o quadrado"), FadeOut(self.E), FadeOut(self.ylab), FadeIn(p0), Create(b0),
                  FadeIn(c0), FadeIn(lg2), ap.oP.animate.set_value(1), *self.show(L["Pm"]),
                  *self.setgl(["R", "u", "I0", "P0"]), run_time=1.5)
        self.restart_decay()
        self.decay_until(self.unit_end(38) - 0.5)
        self.an(38, 1)
        self.play(FadeIn(e2), Create(b2), run_time=1.2)
        self.E = VGroup(p0, b0, c0, e2, b2, lg2)
        self.an(38, 3)
        self.wait(2.0)

    def n39(self):
        ap, L = self.ap, self.L
        ax = self.ax
        a = M(r"\frac{I}{I_0}", "=", r"e^{-t/\tau}", size=M_M, w=2.8).move_to(P3(2.6, 2.0))
        b = M(r"\frac{P_R}{P_0}", "=", r"e^{-2t/\tau}", size=M_M, w=2.9).move_to(P3(5.5, 2.0))
        a[0].set_color(GREEN)
        mk = VGroup(Line(ax.c2p(TAU, 0), ax.c2p(TAU, 1.0), color=DIM, stroke_width=2),
                    Dot(ax.c2p(TAU, math.exp(-1)), radius=0.08).set_fill(GREEN, 1),
                    Dot(ax.c2p(TAU, math.exp(-2)), radius=0.08).set_fill(HEAT, 1),
                    MathTex(r"e^{-1}", font_size=24, color=GREEN).move_to(ax.c2p(TAU, math.exp(-1)) + P3(0.6, 0.12)),
                    MathTex(r"e^{-2}", font_size=24, color=HEAT).move_to(ax.c2p(TAU, math.exp(-2)) + P3(0.6, 0.12)))
        cap = MathTex(r"t=\tau:\; I/I_0\approx 37\%,\;\; P_R/P_0\approx 14\%", font_size=28, color=DIM) \
            .move_to(P3(EQX, 1.05))
        self.mop.set_value(0)
        self.an(39, 0)
        self.play(*self.H("Comparação: corrente e potência"), FadeOut(self.E), self.cu.op.animate.set_value(0),
                  FadeOut(self.ylab), ap.oAll.animate.set_value(0.35), run_time=1.2)
        self.play(FadeIn(a), FadeIn(b), FadeIn(VGroup(mk[0], mk[1], mk[3])), run_time=1.2)
        self.an(39, 1)
        self.play(FadeIn(VGroup(mk[2], mk[4])), FadeIn(cap), run_time=1.2)
        self.E = VGroup(a, b, mk, cap)
        self.wait(1.5)

    # ── N40–N44: energia dissipada ─────────────────────────────────────────────────────────────────────────────
    def n40(self):
        ap, L = self.ap, self.L
        ax = self.ax
        l1 = M(r"E_{\rm diss}", "=", r"\int_0^\infty", "P_R", "dt", size=M_M, w=5.8).move_to(P3(EQX, 2.3))
        l2 = M("=", "P_0", r"\int_0^\infty", r"\frac{P_R}{P_0}", "dt", size=M_M, w=5.8).move_to(P3(EQX, 1.45))
        l2.align_to(l1[1], LEFT)
        ylab = MathTex(r"P_R/P_0", font_size=26, color=HEAT).move_to(ax.c2p(0, 1.1) + P3(0.55, 0.12))
        cap1 = MathTex(r"\text{área sob }P_R/P_0\ =\ \text{tempo efetivo}", font_size=26, color=HEAT) \
            .move_to(P3(EQX, 0.85))
        cap2 = MathTex(r"E_{\rm diss}=P_0\times\text{área}", font_size=30, color=WHITE).move_to(P3(EQX, 0.85))
        self.cpfull = ax.plot(lambda x: math.exp(-2 * x / TAU), x_range=[0, TT_END * TAU, 0.05 * TAU], color=HEAT,
                              stroke_width=5).set_z_index(8)
        # curva completa já existe; a área começa vazia
        self.an(40, 0)
        self.play(*self.H("A energia dissipada: potência inicial × área"), FadeOut(self.E),
                  self.ci.op.animate.set_value(0), self.cp.op.animate.set_value(0), FadeIn(self.cpfull),
                  ap.oAll.animate.set_value(1), *self.setgl(["P0", "tau"]), FadeIn(l1), run_time=1.5)
        self.ylab40 = ylab
        self.mfn = lambda s_: math.exp(-2 * s_)
        aop = ValueTracker(0)

        def area():
            t = ap.tt.get_value() * TAU
            if t < 0.1 * TAU:
                return VMobject()
            gr = ax.plot(lambda x: math.exp(-2 * x / TAU), x_range=[0, TT_END * TAU, 0.05 * TAU])
            return ax.get_area(gr, x_range=(0, t), color=HEAT, opacity=0.4 * aop.get_value()).set_z_index(3)
        self.area = always_redraw(area)
        self.area.op = aop
        self.add(self.area)
        self.mop.set_value(0)
        self.an(40, 1)
        self.play(FadeIn(ylab), FadeIn(l2), run_time=1.2)
        self.an(40, 2)
        self.play(FadeIn(cap1), run_time=1.0)
        self.an(40, 3)
        self.play(FadeOut(cap1), FadeIn(cap2), run_time=1.0)
        self.an(40, 4)
        self.restart_decay()
        self.mop.set_value(1)
        self.area.op.set_value(1)
        self.decay_until(self.unit_end(40) - 0.8)
        self.wait(1.0)
        self.an(40, 5)
        self.E = VGroup(l1, l2, cap2)
        self.wait(2.0)

    def n41(self):
        ap, L = self.ap, self.L
        a = M(r"E_{\rm diss}", "=", r"\int_0^\infty", "P_R", "dt", size=M_XL).move_to(P3(0, -0.45))
        e1 = M(r"E_{\rm diss}", "=", r"\int_0^\infty", "P_0", r"e^{-2t/\tau}", "dt", size=M_XL).move_to(P3(0, -0.45))
        e2 = M(r"E_{\rm diss}", "=", "P_0", r"\int_0^\infty", r"e^{-2t/\tau}", "dt", size=M_XL).move_to(P3(0, -0.45))
        p0 = M("P_0", "=", "I_0^2R", "=", r"\frac{B^2l^2u_0^2}{R}", size=M_L).move_to(P3(0, -1.7))
        pc = txt("potência inicial", T_CAP, DIM).move_to(P3(0, -2.5))
        self.an(41, 0)
        self.play(*self.H("Substituindo a potência"), FadeOut(self.axg), FadeOut(self.E), FadeOut(self.ylab40),
                  FadeOut(self.cpfull), self.area.op.animate.set_value(0), self.cp.op.animate.set_value(0),
                  FadeOut(self.gl35), *self.lay("top"), *self.hide(L["u"], L["I"], L["Fm"], L["Fe"]), run_time=1.8)
        self.remove(self.cp, self.area, self.cu, self.ci, self.marker)
        self.play(ap.barf.animate.set_value(0), run_time=0.3)
        ap.mode, ap.autoloop, ap.lp, ap.frozen = "decay", True, "run", False
        ap.tt.set_value(0.0)
        self.play(ap.barf.animate.set_value(1), run_time=0.3)
        self.put(a, 1.2)
        self.morph(a, e1)
        self.an(41, 1)
        self.morph(e1, e2)
        self.an(41, 2)
        self.play(FadeIn(p0), FadeIn(pc), run_time=1.2)
        self.E = VGroup(e2, p0, pc)
        self.an(41, 3)
        self.wait(1.5)

    def n42(self):
        e2, p0, pc = self.E
        mid = M(r"\int_0^\infty", r"e^{-2t/\tau}", "dt").move_to(P3(0, -1.6))
        j1 = M(r"\int_0^\infty", r"e^{-2t/\tau}", "dt", "=", r"\left[-\frac{\tau}{2}e^{-2t/\tau}\right]_0^\infty") \
            .move_to(P3(0, -1.6))
        j2 = M(r"\int_0^\infty", r"e^{-2t/\tau}", "dt", "=", r"-\frac{\tau}{2}", r"\left(e^{-\infty}-e^{0}\right)") \
            .move_to(P3(0, -1.6))
        j3 = M(r"\int_0^\infty", r"e^{-2t/\tau}", "dt", "=", r"\frac{\tau}{2}").move_to(P3(0, -1.6))
        an = MathTex(r"e^{-\infty}=0,\qquad e^{0}=1", font_size=32, color=DIM).move_to(P3(0, -2.6))
        e3 = M(r"E_{\rm diss}", "=", "P_0", r"\frac{\tau}{2}", size=M_XL).move_to(P3(0, -0.6))
        self.an(42, 0)
        self.play(*self.H("A integral"), FadeOut(p0), FadeOut(pc), run_time=1.0)
        self.put(mid, 1.0)
        self.morph(mid, j1)
        self.an(42, 1)
        self.wait(1.0)
        self.an(42, 2)
        self.morph(j1, j2)
        self.play(FadeIn(an), run_time=0.8)
        self.an(42, 5)
        self.morph(j2, j3)
        self.play(FadeOut(an), run_time=0.5)
        b3 = boxed(j3[4], buff=0.14)
        self.play(Create(b3), run_time=0.8)
        self.an(42, 6)
        self.play(FadeOut(VGroup(j3, b3)), run_time=0.8)
        self.morph(e2, e3)
        b4 = boxed(e3)
        self.play(Create(b4), run_time=0.8)
        self.E = VGroup(e3, b4)
        self.wait(1.5)

    def n43(self):
        e3, b4 = self.E

        def frac(nums, dens, size=M_XL):
            nm = [MathTex(t, font_size=size, color=c) for t, c in nums]
            dn = [MathTex(t, font_size=size, color=c) for t, c in dens]
            ng, dg = VGroup(*nm).arrange(RIGHT, buff=0.14), VGroup(*dn).arrange(RIGHT, buff=0.14)
            wd = max(ng.width, dg.width) + 0.2
            bar = Line(LEFT * wd / 2, RIGHT * wd / 2, color=WHITE, stroke_width=3)
            ng.next_to(bar, UP, buff=0.12)
            dg.next_to(bar, DOWN, buff=0.12)
            return VGroup(ng, bar, dg), nm, dn
        cB, cl, cR = MAGENTA, "#7FB2FF", HEAT
        f1, n1, d1 = frac([("B^2", cB), ("l^2", cl), ("u_0^2", VIOLET)], [("R", cR)])
        f2, n2, d2 = frac([("m", WHITE), ("R", cR)], [("B^2", cB), ("l^2", cl)])
        lead = M(r"E_{\rm diss}", "=", size=M_XL)
        c1, half, c2 = (MathTex(r"\cdot", font_size=M_XL), MathTex(r"\frac12", font_size=M_XL),
                        MathTex(r"\cdot", font_size=M_XL))
        row = VGroup(lead, f1, c1, half, c2, f2).arrange(RIGHT, buff=0.22).move_to(P3(0, -0.8))
        # resultado em formação (embaixo): ½ · m · u₀²
        lead_b = M(r"E_{\rm diss}", "=", size=M_XL)
        half_b, m_b, u_b = (MathTex(r"\frac12", font_size=M_XL), MathTex("m", font_size=M_XL),
                            MathTex("u_0^2", font_size=M_XL, color=VIOLET))
        res = VGroup(lead_b, half_b, m_b, u_b).arrange(RIGHT, buff=0.2).move_to(P3(0, -2.5))
        # pares canceláveis (em cima)
        rB, rBn, rBd = frac([("B^2", cB)], [("B^2", cB)])
        rl, rln, rld = frac([("l^2", cl)], [("l^2", cl)])
        rR, rRn, rRd = frac([("R", cR)], [("R", cR)])
        rowt = VGroup(rR, rB, rl).arrange(RIGHT, buff=0.4).move_to(P3(0, -0.8))
        lead_tgt = rowt.get_left() + LEFT * (lead.width / 2 + 0.25)
        tf, tn_, td_ = frac([("m", WHITE), ("R", cR)], [("B^2", cB), ("l^2", cl)], size=M_L)
        tau = VGroup(MathTex(r"\tau=", font_size=M_L, color=VIOLET), tf).arrange(RIGHT, buff=0.2).move_to(P3(-3.0, -2.35))

        def strike(t):
            return Line(t.get_corner(UP + RIGHT) + P3(0.06, 0.08), t.get_corner(DOWN + LEFT) + P3(-0.06, -0.08),
                        color=WHITE, stroke_width=5).set_z_index(30)
        self.an(43, 0)
        self.play(*self.H("Os cancelamentos"), FadeOut(b4), run_time=0.8)
        self.play(FadeOut(e3), FadeIn(row), run_time=1.2)
        self.an(43, 1)
        # etapa A: os fatores que sobrevivem (½, m, u₀²) vão formar o resultado
        self.play(ReplacementTransform(half, half_b), ReplacementTransform(n2[0], m_b),
                  ReplacementTransform(n1[2], u_b), FadeIn(lead_b), FadeOut(VGroup(lead, c1, c2)), run_time=2.2)
        self.an(43, 2)
        # etapa B: o resto vira pares R/R, B²/B², l²/l²
        self.play(ReplacementTransform(n1[0], rBn[0]), ReplacementTransform(d2[0], rBd[0]),
                  ReplacementTransform(n1[1], rln[0]), ReplacementTransform(d2[1], rld[0]),
                  ReplacementTransform(n2[1], rRn[0]), ReplacementTransform(d1[0], rRd[0]),
                  FadeOut(VGroup(f1[1], f2[1])), FadeIn(VGroup(rB[1], rl[1], rR[1])), run_time=1.8)
        ones = []
        for idx, (r_, num, den) in enumerate(((rR, rRn[0], rRd[0]), (rB, rBn[0], rBd[0]), (rl, rln[0], rld[0]))):
            self.an(43, 3 + idx)                      # R/R, B²/B², l²/l²: um par por frase
            s1, s2 = strike(num), strike(den)
            self.play(Create(s1), Create(s2), run_time=1.0)
            one = MathTex("1", font_size=M_XL).move_to(VGroup(num, den, r_[1]).get_center())
            self.play(FadeOut(VGroup(s1, s2)), ReplacementTransform(VGroup(num, den, r_[1]), one), run_time=0.8)
            ones.append(one)
        self.an(43, 6)
        self.play(FadeOut(VGroup(*ones)), res.animate.move_to(P3(0, -0.8)), run_time=1.5)
        bf = boxed(res, buff=0.25)
        self.play(Create(bf), run_time=0.8)
        l1 = MathTex(r"\text{depende de }B,\,l,\,R", font_size=30, color=DIM).move_to(P3(-3.0, -3.35))
        l2 = MathTex(r"\text{não depende de }B,\,l,\,R", font_size=30, color=DIM).move_to(P3(1.8, -1.95))
        self.an(43, 7)
        self.play(FadeIn(tau), FadeIn(l1), FadeIn(l2), run_time=1.5)
        self.E = VGroup(res, bf, tau, l1, l2)
        self.wait(2.0)

    def n44(self):
        keep, bf, tau, l1, l2 = self.E
        k0 = M("K_0", "=", r"\frac12mu_0^2", size=M_XL).move_to(P3(0, -2.2))
        fin = M(r"E_{\rm diss}", r"(\infty)", "=", "K_0", size=64).move_to(P3(0, -1.3))
        bfin = boxed(fin, buff=0.3)
        self.an(44, 0)
        self.play(*self.H("Energia dissipada total = energia cinética inicial"), FadeOut(bf), FadeOut(tau),
                  FadeOut(l1), FadeOut(l2), keep.animate.move_to(P3(0, -0.5)), run_time=1.2)
        self.an(44, 1)
        self.play(FadeIn(k0), run_time=1.2)
        self.an(44, 2)
        self.play(FadeOut(keep), FadeOut(k0), FadeIn(fin), run_time=1.5)
        self.play(Create(bfin), run_time=1.0)
        self.E = VGroup(fin, bfin)
        self.an(44, 3)
        self.wait(2.0)

    # ── N45–N46: síntese ───────────────────────────────────────────────────────────────────────────────────────
    def n45(self):
        ap, L = self.ap, self.L
        ap.mode, ap.moving, ap.rph, ap.frozen = "forced", True, "run", False
        ap.xb.set_value(XB0)
        for tr, v in ((ap.cur, 1), (ap.heat, 1), (ap.fm, 1), (ap.fe, 1), (ap.ua, 1), (ap.oA, 0), (ap.oX, 0), (ap.oL, 0),
                      (ap.oI, 1), (ap.oU, 1), (ap.oF, 1), (ap.oP, 1)):
            tr.set_value(v)
        ap.barf.set_value(1.0)
        e = M(r"P_{\rm ext}", "=", r"P_R", size=60).move_to(P3(0, -1.0))
        b = boxed(e, buff=0.25)
        ap.auto = 0.0
        self.an(45, 0)
        self.play(*self.H("Barra com velocidade imposta"), FadeOut(self.E), *self.lay("top"),
                  ap.oAll.animate.set_value(1), *self.show(L["Fm"], L["Fe"], L["I"], L["Pm"]), run_time=2.0)
        self.an(45, 2)
        self.play(FadeIn(e), Create(b), run_time=1.2)
        self.E = VGroup(e, b)
        self.an(45, 3)
        self.wait(1.5)

    def n46(self):
        ap, L = self.ap, self.L
        # K (ciano, em cima) diminui; E_diss (laranja, embaixo) aumenta; a soma permanece K₀
        H, base = 2.6, P3(1.7, -1.4)

        def bars():
            e2 = math.exp(-2 * ap.tt.get_value())
            kd = VGroup(Rectangle(width=0.8, height=H).set_fill(opacity=0).set_stroke(DIM, 2)
                        .move_to(base + P3(0, H / 2)))
            if e2 > 0.003:
                kd.add(Rectangle(width=0.8, height=H * e2).set_fill(CYAN, 0.85).set_stroke(width=0)
                       .move_to(base + P3(0, H * (1 - e2) + H * e2 / 2)))
            if 1 - e2 > 0.003:
                kd.add(Rectangle(width=0.8, height=H * (1 - e2)).set_fill(HEAT, 0.85).set_stroke(width=0)
                       .move_to(base + P3(0, H * (1 - e2) / 2)))
            return kd
        lk = MathTex("K", font_size=M_S, color=CYAN).move_to(base + P3(0.8, H - 0.35))
        ld = MathTex(r"E_{\rm diss}", font_size=M_S, color=HEAT).move_to(base + P3(1.0, 0.35))
        lt = MathTex(r"K_0", font_size=M_S, color=DIM).move_to(base + P3(0.8, H + 0.3))
        e = M(r"K(t)", "+", r"E_{\rm diss}(t)", "=", "K_0", size=M_L, w=4.6).move_to(P3(5.1, 2.0))
        k = M(r"K(t)", "=", "K_0", r"e^{-2t/\tau}", size=M_M, w=4.4).move_to(P3(5.1, 1.0))
        d = M(r"E_{\rm diss}(t)", "=", "K_0", r"\left(1-e^{-2t/\tau}\right)", size=M_M, w=4.6).move_to(P3(5.1, 0.1))
        init = MathTex(r"t=0:\ K(0)=K_0,\ \ E_{\rm diss}(0)=0", font_size=26, color=DIM).move_to(P3(5.1, -0.9))
        self.an(46, 0)
        self.play(*self.H("Barra livre: a energia se conserva no tempo"), FadeOut(self.E), *self.hide(L["Fe"]),
                  ap.fe.animate.set_value(0), *self.lay("left"), run_time=1.5)
        self.restart_decay()                       # t = 0 ANTES de criar a coluna: primeiro quadro K = K₀, E_diss = 0
        self.bars = always_redraw(bars)
        self.an(46, 1)
        self.play(FadeIn(self.bars), FadeIn(VGroup(lk, ld, lt)), run_time=1.0)
        self.an(46, 2)
        self.decay_until(self.fr_t(46, 5) + 2.5)
        self.wait(0.5)
        self.an(46, 3)
        self.play(FadeIn(e), FadeIn(k), FadeIn(d), FadeIn(init), run_time=1.5)
        tinf = MathTex(r"t\to\infty", font_size=M_M, color=WHITE).move_to(P3(5.1, -1.0))
        kinf = M(r"K(\infty)", "=", "0", size=M_M).move_to(P3(5.1, -1.8))
        fin = M(r"E_{\rm diss}", r"(\infty)", "=", "K_0", size=M_L, w=4.6).move_to(P3(5.1, -2.7))
        bf = boxed(fin)
        self.an(46, 5)
        self.play(FadeOut(init), FadeIn(tinf), run_time=0.8)
        self.play(FadeIn(kinf), run_time=0.8)
        self.play(FadeIn(fin), Create(bf), run_time=1.2)
        self.E = VGroup(e, k, d, tinf, kinf, fin, bf, lk, ld, lt)
        self.wait(2.0)

    def n47(self):
        ap, L = self.ap, self.L
        self.an(47, 0)
        self.play(*self.H("A resposta"), FadeOut(self.E), FadeOut(self.bars), *self.hide(L["Pm"]),
                  ap.barf.animate.set_value(0), run_time=1.2)
        ap.mode, ap.moving, ap.rph, ap.frozen, ap.auto = "forced", True, "run", False, 0.0
        ap.xb.set_value(XB0)
        for tr, v in ((ap.cur, 1), (ap.heat, 1), (ap.fm, 1), (ap.fe, 1), (ap.ua, 1), (ap.oP, 0), (ap.oF, 1)):
            tr.set_value(v)
        e47 = M(r"P_{\rm ext}", "=", r"P_R", size=60).move_to(P3(0, -1.2))
        b47 = boxed(e47, buff=0.25)
        self.play(*self.lay("top"), ap.barf.animate.set_value(1), *self.show(L["Fm"], L["Fe"]), run_time=2.0)
        cv = txt("velocidade imposta", T_CAP, DIM).move_to(P3(0, -0.45))
        self.an(47, 1)
        self.play(FadeIn(e47), Create(b47), FadeIn(cv), run_time=1.2)
        self.E = VGroup(e47, b47, cv)
        self.wait(1.5)

    def n48(self):
        ap = self.ap
        a = M(r"\text{trabalho externo}", r"\rightarrow", r"E_{\rm diss}", size=M_XL).move_to(P3(0, -0.95))
        a[0].set_color(CYAN)
        b = M(r"K_0", "=", r"E_{\rm diss}", r"(\infty)", size=M_XL).move_to(P3(0, -2.5))
        ba, bb = boxed(a, buff=0.25), boxed(b, buff=0.25)
        ca = txt("barra com velocidade imposta", T_CAP, DIM).move_to(P3(0, -0.2))
        cb = txt("barra livre", T_CAP, DIM).move_to(P3(0, -1.75))
        self.an(48, 0)
        self.play(*self.H("Síntese"), FadeOut(self.E), ap.oAll.animate.set_value(0.4), run_time=1.5)
        self.an(48, 2)
        self.play(FadeIn(a), Create(ba), FadeIn(ca), run_time=1.5)
        self.play(FadeIn(b), Create(bb), FadeIn(cb), run_time=1.5)
        self.E = VGroup(a, b, ba, bb, ca, cb)
        self.an(48, 3)
        self.wait(1.5)
