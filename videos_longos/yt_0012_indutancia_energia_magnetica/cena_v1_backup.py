"""yt_0012 — Por que a corrente resiste a mudar? (indutância e energia magnética).

Preview visual silencioso, 960×540 / 15 fps. Storyboard C01–C20 (ver ficha.md).

Um aparato só (bateria + chave + solenoide + resistor), desenhado a cada quadro a partir de trackers:
  tc = t/τ da carga     → I = 1 − e^{−tc}, dI/dt = e^{−tc}, B = I, ℰ_L = −e^{−tc}, U_B = I², P_J = I², ...
  td = t/τ da descarga  → I = e^{−td}, dI/dt = −e^{−td}, ℰ_L = +e^{−td}, U_B = P_R = e^{−2td}, Q_R = 1 − e^{−2td}
  sp (só C06)           → corrente imposta (sobe, constante, desce) e sua derivada analítica
(unidades: I_∞ ou I₀ = 1, I_∞/τ = 1, ℰ₀ = 1, U_B,∞ ou U_B,0 = 1). Gráficos, campo, cargas, fem e brilho leem o mesmo estado.
Cores: corrente azul elétrico · E induzido / ℰ_L ciano · B, Λ, U_B magenta · τ, t violeta · calor laranja · resto branco.
Convenção: corrente horária (sobe pela bateria, solenoide da esquerda para a direita); B dentro do solenoide = +x.
`SO=3,5-7` renderiza só essas cenas (as outras são puladas, o estado é construído).
"""
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from manim import (
    AnimationGroup, Arrow, Axes, Brace, Circle, Create, DashedLine, DashedVMobject, DoubleArrow, Dot, Ellipse,
    FadeIn, FadeOut, ImageMobject, LaggedStart, Line, ManimColor, MathTex, Mobject, Rectangle,
    ReplacementTransform, RoundedRectangle, Scene, Square, SurroundingRectangle, TransformFromCopy, TransformMatchingTex,
    VGroup, VMobject, ValueTracker, always_redraw, interpolate_color, linear, DOWN, LEFT, RIGHT, UP, UL, UR, PI,
)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import screen_text  # noqa: E402

PASTA = Path(__file__).resolve().parent
LOGO_H = ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"

# ── paleta ───────────────────────────────────────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR        # campo elétrico induzido, ℰ_L, ℰ₂, E_φ
BLUE = "#267BFF"            # corrente: cargas, setas
IC = "#4F94FF"              # corrente nos símbolos (azul elétrico clareado para leitura)
MAGENTA = "#EA63FF"         # B, Λ, U_B, u_B
VIOLET = "#9C8CFF"          # tempo, τ (violeta #745CFF clareado, como no vid_0011)
HEAT = "#FF7A3D"            # calor: P_R, P_Joule, E_calor, Q_R (único tom quente, como no yt_0010)
STEEL = "#7A8696"           # fios
COIL = "#B9C4D8"            # espiras da frente
COIL_B = "#5C6678"          # espiras de trás
GEO = "#B8C4DA"
DIM = "#8FA3C4"

T_BODY, T_NOTE, T_CAP = 30, 26, 22
M_XL, M_L, M_M, M_S = 54, 46, 38, 30

# ── tempos provisórios (a voz será escrita depois sobre estes tempos; retimar aqui) ───────────────────────────
T_FADE = 0.8     # entrada/saída de texto
T_MOVE = 1.6     # mudança de composição
T_EQ = 1.2       # entrada de equação
T_MORPH = 1.8    # transformação de equação
T_BEAT = 1.0     # respiro curto
T_READ = 3.0     # pausa de leitura
T_HOLD = 5.0     # pausa longa (payoff)
T_RUN = 9.0      # transitório completo (0 → 5τ)
T_SW = 0.8       # movimento da chave

TOK = {
    "I": IC, "I_1": IC, "I_2": IC, "I(t)": IC, "I_0": IC, r"I_\infty": IC, "I^2": IC, "I_0^2": IC, "I(0)": IC,
    r"\frac{dI}{dt}": IC, r"\frac{dI_1}{dt}": IC, r"\frac{dI_2}{dt}": IC, r"I\to I_\infty": IC,
    r"\mathbf B_1": MAGENTA, r"\mathbf B": MAGENTA, "B(t)": MAGENTA, r"\frac{dB}{dt}": MAGENTA, r"B\neq0": MAGENTA,
    r"\Lambda": MAGENTA, r"\Lambda_1": MAGENTA, r"\Lambda_2": MAGENTA,
    "U_B": MAGENTA, "U_B(t)": MAGENTA, "U_{B,0}": MAGENTA, "u_B": MAGENTA, r"\frac{dU_B}{dt}": MAGENTA,
    r"\mathcal E_L": CYAN, r"\mathcal E_2": CYAN, r"\mathcal E_1": CYAN, r"E_\phi": CYAN, r"E_{\rm ind}": CYAN,
    r"\mathcal E_L=0": CYAN, r"\mathcal E_L\to0": CYAN, r"E_{\rm ind}=0": CYAN, r"|\mathcal E_L|=\mathcal E_0": CYAN,
    "P_R": HEAT, "P_R(t)": HEAT, r"P_{\rm Joule}": HEAT, r"E_{\rm calor}": HEAT, "Q_R(t)": HEAT, "I^2R": HEAT,
    r"\tau": VIOLET, r"\frac{t}{\tau}": VIOLET, r"\frac{dt}{\tau}": VIOLET,
}

# ── geometria local do aparato (tela = C + s·(p − F)) ────────────────────────────────────────────────────────
XL, XA, XB = -4.2, -3.4, -2.6        # bateria, contato a, pivô da chave / ramo de desvio
XS0, XS1, XR = -1.3, 1.9, 3.6        # solenoide (início, fim), resistor
YT, YB = 1.3, -1.3                   # fio de cima (eixo do solenoide), fio de baixo
A_R, NT, KX = 0.5, 9, 0.13           # raio do solenoide, espiras desenhadas, inclinação de perspectiva
XC = 0.5 * (XS0 + XS1)
HX0, HX1 = XS0 - KX, XS1 - KX        # pontas da hélice
LBL = 0.8                            # comprimento da lâmina da chave
SW_OPEN, SW_A, SW_B = 145.0, 180.0, 270.0
XM0, XM1, A2, NT2, KX2 = -0.15, 0.75, 0.8, 3, 0.2   # bobina secundária coaxial
YMET, MR = YT + 1.75, 0.3            # medidor da secundária
XP0, XP1, PH = XC - 0.22, XC + 0.22, 0.5            # capacitor (C20)
XAMP = -0.75                         # anel amperiano (C20)
XIA = 0.9                            # centro da seta de corrente no fio de baixo

LAYOUTS = {                          # (s, cx, cy, fx, fy)
    "full": (1.1, 0.0, -0.4, -0.3, 0.1),
    "left": (0.9, -3.75, -0.45, -0.3, 0.1),
    "mut": (0.8, -3.55, -0.95, -0.3, 0.1),
    "solo": (1.7, -2.6, 0.1, XC, YT),
    "soloc": (1.9, 0.0, 0.7, XC, YT),
    "cells": (1.2, -2.6, -0.1, XC, YT),
    "thumb": (0.55, -4.4, 1.3, -0.3, 0.1),
}
EQX = 3.95                           # centro da coluna da direita
GC = (3.95, -0.65)                   # centro do gráfico padrão


def _sel(s):
    out = set()
    for p in s.split(","):
        p = p.strip()
        if "-" in p:
            a, b = p.split("-")
            out.update(range(int(a), int(b) + 1))
        elif p:
            out.add(int(p))
    return out


SEL = _sel(os.environ.get("SO", ""))


def P3(x, y):
    return np.array([x, y, 0.0])


def txt(s, size=T_BODY, color=WHITE, opacity=1.0):
    if size <= 28:                   # anotações em MAIÚSCULA (como no yt_0010)
        s = s.upper()
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(opacity)


def fitw(m, w=6.6):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def M(*parts, size=M_L, w=6.6, col=None):
    """MathTex por partes; cada parte na cor da grandeza (serve ao morph parte a parte)."""
    m = MathTex(*parts, font_size=size, color=WHITE)
    for i, (part, sub) in enumerate(zip(parts, m.submobjects)):
        c = (col or {}).get(i, TOK.get(part))
        if c:
            sub.set_color(c)
    return fitw(m, w) if w else m


def arrow(a, b, color=WHITE, width=5, z=8, tip=0.2, op=1.0):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if np.linalg.norm(b - a) < 0.03:
        return VMobject()
    m = Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.45,
              max_stroke_width_to_length_ratio=50)
    return m.set_opacity(op).set_z_index(z)


def boxed(m, color=WHITE, buff=0.16, width=3):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=width, corner_radius=0.1)


def multi(paths):
    """Um VMobject com vários subcaminhos poligonais (pontos já em coordenadas de tela)."""
    m = VMobject()
    for p in paths:
        if len(p) < 2:
            continue
        m.start_new_path(p[0])
        m.add_points_as_corners(p[1:])
    return m


def helix(x0, x1, yc, r, nt, kx, th0=-PI / 2, n_per=36):
    """Hélice vista de lado: corrente avançando em θ ⇒ espiras da frente (sen θ > 0) descem ⇒ B em +x."""
    th = np.linspace(th0, th0 + 2 * PI * nt, nt * n_per + 1)
    x = x0 + (x1 - x0) * (th - th[0]) / (th[-1] - th[0]) + kx * np.sin(th)
    return np.stack([x, yc + r * np.cos(th)], 1), np.sin(th)


def split_depth(pts, z):
    """Fatia a hélice em trechos da frente (z ≥ 0) e de trás (z < 0)."""
    front, back, cur, sign = [], [], [pts[0]], z[0] >= 0
    for p, zz in zip(pts[1:], z[1:]):
        cur.append(p)
        if (zz >= 0) != sign:
            (front if sign else back).append(np.array(cur))
            cur, sign = [p], zz >= 0
    (front if sign else back).append(np.array(cur))
    return front, back


def probe(s):
    """C06: corrente imposta (sobe, constante, desce). Retorna (I, dI/dt normalizado, máx. 1)."""
    if s <= 0:
        return 0.0, 0.0
    if s < 1:
        return 0.5 * (1 - math.cos(PI * s)), math.sin(PI * s)
    if s < 2:
        return 1.0, 0.0
    if s < 3:
        return 0.5 * (1 + math.cos(PI * (s - 2))), -math.sin(PI * (s - 2))
    return 0.0, 0.0


class Trilha:
    """Percurso das cargas (coordenadas locais). z ∈ [−1, 1] na hélice (profundidade); z = 2 nos fios."""

    def __init__(self, pts, z):
        self.p, self.z = np.asarray(pts, float), np.asarray(z, float)
        d = np.linalg.norm(np.diff(self.p, axis=0), axis=1)
        self.c = np.concatenate([[0.0], np.cumsum(d)])
        self.L = self.c[-1]

    def at(self, u):
        s = (np.asarray(u) % 1.0) * self.L
        return (np.interp(s, self.c, self.p[:, 0]), np.interp(s, self.c, self.p[:, 1]),
                np.interp(s, self.c, self.z))


def trilha(*parts):
    pts, zs = [], []
    for p in parts:
        if isinstance(p, tuple) and len(p) == 2 and isinstance(p[0], np.ndarray):
            a, z = p                                     # sentinelas: o trecho fio ↔ hélice não herda profundidade
            pts += [a[0] - np.array([1e-4, 0])] + list(a) + [a[-1] + np.array([1e-4, 0])]
            zs += [2.0] + list(z) + [2.0]
        else:
            pts += [p]
            zs += [2.0]
    return Trilha(pts, zs)


class Ap:
    """Estado do aparato (trackers visuais e físicos) e o desenho de cada quadro."""
    OPS0 = ("oAll", "oDots", "oEL", "oEB", "oIA", "oSec", "oSrc", "oByp", "oVol", "oAe", "oCap", "oIS", "oHL",
            "oAmp", "oS1", "oS2")
    OPS1 = ("oCirc", "oSol", "oBat", "oB", "oHeat")

    def __init__(self):
        T = ValueTracker
        s, cx, cy, fx, fy = LAYOUTS["full"]
        self.s, self.cx, self.cy, self.fx, self.fy = T(s), T(cx), T(cy), T(fx), T(fy)
        for n in self.OPS0:
            setattr(self, n, T(0.0))
        for n in self.OPS1:
            setattr(self, n, T(1.0))
        self.sw = T(SW_OPEN)
        self.tc, self.td, self.sp = T(0.0), T(0.0), T(0.0)
        self.mode, self.role, self.ph, self.auto_tc = "charge", 1, 0.0, 0.0
        hp, hz = helix(XS0, XS1, YT, A_R, NT, KX)
        self.hfront, self.hback = split_depth(hp, hz)
        sp_, sz = helix(XM0, XM1, YT, A2, NT2, KX2, th0=0.0)
        self.sfront, self.sback = split_depth(sp_, sz)
        H = (hp, hz)
        self.paths = {
            "charge": trilha((XL, YB), (XL, YT), (XA, YT), (XB, YT), (HX0, YT), H, (XR, YT), (XR, YB), (XL, YB)),
            "discharge": trilha((XB, YT), (HX0, YT), H, (XR, YT), (XR, YB), (XB, YB), (XB, YT - LBL), (XB, YT)),
            "cap": trilha((XL, YB), (XL, YT), (XA, YT), (XB, YT), (HX0, YT), (HX1, YT), (XR, YT), (XR, YB),
                          (XL, YB)),
            "probe": Trilha(hp, hz),
            "sec": trilha((sp_, sz), (XM1, YMET), (XC + MR, YMET), (XC - MR, YMET), (XM0, YMET), (XM0, YT + A2)),
        }

    # ── estado físico: tudo sai daqui ─────────────────────────────────────────────────────────────────────────
    def st(self):
        m = self.mode
        if m == "charge":
            e = math.exp(-self.tc.get_value())
            I, dI, q = 1 - e, e, 0.0
            if self.role == 1 and self.tc.get_value() < 1e-6 and abs(self.sw.get_value() - SW_A) > 2:
                dI = 0.0                                 # chave aberta: nada muda ainda
        elif m == "discharge":
            e = math.exp(-self.td.get_value())
            I, dI, q = e, -e, 0.0
        elif m == "probe":
            (I, dI), q = probe(self.sp.get_value()), 0.0
        else:                                            # "cap": carga RC do capacitor (C20)
            e = math.exp(-self.tc.get_value())
            I, dI, q = e, -e, 1 - e
        return {"I": I, "dI": dI, "B": I, "EL": -dI, "UB": I * I, "PR": I * I, "q": q,
                "QR": 1 - math.exp(-2 * self.td.get_value())}

    def path_key(self):
        if self.role == 2:
            return "sec"
        return self.mode

    # ── transformação local → tela ──────────────────────────────────────────────────────────────────────────
    def W(self, x, y=0.0):
        s = self.s.get_value()
        return P3(self.cx.get_value() + s * (x - self.fx.get_value()), self.cy.get_value() + s * (y - self.fy.get_value()))

    def Wv(self, a):
        a = np.asarray(a, float)
        s = self.s.get_value()
        out = np.zeros((len(a), 3))
        out[:, 0] = self.cx.get_value() + s * (a[:, 0] - self.fx.get_value())
        out[:, 1] = self.cy.get_value() + s * (a[:, 1] - self.fy.get_value())
        return out

    # ── relógio ───────────────────────────────────────────────────────────────────────────────────────────
    def tick(self, dt):
        if self.auto_tc > 0:
            self.tc.increment_value(self.auto_tc * dt)
        S = self.st()
        k = self.paths[self.path_key()]
        self.ph = (self.ph + dt * 0.9 * abs(S["I"]) / k.L) % 1.0      # velocidade das cargas ∝ I

    # ── desenho ─────────────────────────────────────────────────────────────────────────────────────────────
    def build(self):
        g = VGroup()
        A = self.oAll.get_value()
        if A < 0.01:
            return g.add(Dot(radius=0.001).set_opacity(0))
        S = self.st()
        s, W, Wv = self.s.get_value(), self.W, self.Wv
        lw = 2.2 + 1.6 * min(s, 1.7)
        cap = self.oCap.get_value()
        oc = A * self.oCirc.get_value()
        ob_ = oc * self.oBat.get_value()
        osl = A * self.oSol.get_value() * (1 - cap)
        ocap = A * cap
        role2 = self.role == 2
        Bv = S["B"]

        # campo B dentro do solenoide (preenchimento + linhas), intensidade ∝ B
        ob = osl * self.oB.get_value()
        if ob > 0.01 and Bv > 0.01:
            g.add(Rectangle(width=(XS1 - XS0) * s, height=2 * A_R * s * 0.9).move_to(W(XC - KX, YT))
                  .set_fill(MAGENTA, ob * (0.05 + 0.2 * min(Bv, 1))).set_stroke(width=0).set_z_index(1))
            for yy in (-0.55 * A_R, 0.0, 0.55 * A_R):
                g.add(arrow(W(XS0 + 0.15, YT + yy), W(XS1 - 0.35, YT + yy), MAGENTA, 3.5, 3, 0.16 * min(s, 1.5),
                            ob * min(1.0, Bv) * 0.9))
        # volume interno (C14) e seção A (C03, C14)
        ov = osl * self.oVol.get_value()
        if ov > 0.01:
            g.add(Rectangle(width=(XS1 - XS0) * s, height=2 * A_R * s).move_to(W(XC - KX, YT))
                  .set_fill(MAGENTA, 0.16 * ov).set_stroke(MAGENTA, 3, ov).set_z_index(2))
            y0 = YT - A_R - 0.32
            g.add(DoubleArrow(W(HX0, y0), W(HX1, y0), buff=0, color=GEO, stroke_width=3, tip_length=0.14,
                              max_tip_length_to_length_ratio=0.2).set_opacity(ov).set_z_index(9))
        oae = osl * max(self.oAe.get_value(), self.oVol.get_value())
        if oae > 0.01:
            g.add(Ellipse(width=2 * KX * s + 0.08, height=2 * A_R * s).move_to(W(HX0 + 0.02, YT))
                  .set_fill(MAGENTA, 0.45 * oae).set_stroke(MAGENTA, 3, oae).set_z_index(6))

        # secundária: trechos de trás
        osc = A * self.oSec.get_value()
        if osc > 0.01:
            g.add(multi([Wv(p) for p in self.sback]).set_stroke(COIL_B, lw * 0.8, 0.6 * osc).set_z_index(0))
        # espiras de trás do solenoide
        if osl > 0.01:
            g.add(multi([Wv(p) for p in self.hback]).set_stroke(COIL_B, lw * 0.7, 0.75 * osl).set_z_index(2))

        # fios
        bat = [[(XL, YB), (XL, -0.1)], [(XL, 0.1), (XL, YT), (XA, YT)], [(XL, YB), (XB, YB)]]
        main = [[(XB, YT), (HX0, YT)], [(HX1, YT), (XR, YT), (XR, 0.65)], [(XR, -0.65), (XR, YB), (XB, YB)]]
        if ob_ > 0.01:
            g.add(multi([Wv(p) for p in bat]).set_stroke(STEEL, lw, ob_).set_z_index(3))
        if oc > 0.01:
            g.add(multi([Wv(p) for p in main]).set_stroke(STEEL, lw, oc).set_z_index(3))
        if ocap > 0.01 and oc > 0.01:
            g.add(multi([Wv([(HX0, YT), (XP0, YT)]), Wv([(XP1, YT), (HX1, YT)])]).set_stroke(STEEL, lw, oc * cap)
                  .set_z_index(3))
        oby = oc * self.oByp.get_value()
        if oby > 0.01:
            g.add(Line(W(XB, YT - LBL), W(XB, YB)).set_stroke(STEEL, lw, oby).set_z_index(3))
            g.add(Dot(W(XB, YB), radius=0.05 * s).set_fill(STEEL, oby).set_z_index(4))
            g.add(Circle(radius=0.06 * s).move_to(W(XB, YT - LBL)).set_fill(BACKGROUND_COLOR, oby)
                  .set_stroke(WHITE, 2, oby).set_z_index(5))

        # bateria (placa longa = +)
        if ob_ > 0.01:
            g.add(Line(W(XL - 0.38, 0.1), W(XL + 0.38, 0.1)).set_stroke(WHITE, lw * 1.1, ob_).set_z_index(4))
            g.add(Line(W(XL - 0.2, -0.1), W(XL + 0.2, -0.1)).set_stroke(WHITE, lw * 2.6, ob_).set_z_index(4))
            pc, a = W(XL + 0.52, 0.34), 0.07 * s
            g.add(multi([[pc + P3(-a, 0), pc + P3(a, 0)], [pc + P3(0, -a), pc + P3(0, a)]])
                  .set_stroke(WHITE, 2.5, ob_).set_z_index(4))
        # resistor (cor e brilho ∝ P_R)
        if oc > 0.01:
            h = min(1.0, S["PR"]) * self.oHeat.get_value() * (0 if role2 or self.mode in ("probe", "cap") else 1)
            if h > 0.03:
                for sc, op in ((2.6, 0.10), (1.9, 0.16), (1.35, 0.26)):
                    g.add(RoundedRectangle(corner_radius=0.12 * s, width=0.45 * s * sc, height=1.3 * s * (0.6 + 0.4 * sc))
                          .set_fill(HEAT, op * h * oc).set_stroke(width=0).move_to(W(XR, 0)).set_z_index(2))
            zz = [(XR, 0.65)] + [(XR + (0.2 if i % 2 == 0 else -0.2), 0.65 - 1.3 * (i + 0.5) / 7) for i in range(7)] + \
                 [(XR, -0.65)]
            col = interpolate_color(ManimColor(STEEL), ManimColor(HEAT), h)
            g.add(VMobject().set_points_as_corners(Wv(zz)).set_stroke(col, lw * 1.05, oc).set_z_index(4))
            # chave: pivô, contato a, lâmina
            ang = math.radians(self.sw.get_value())
            pv = W(XB, YT)
            g.add(Circle(radius=0.06 * s).move_to(W(XA, YT)).set_fill(BACKGROUND_COLOR, ob_)
                  .set_stroke(WHITE, 2, ob_).set_z_index(5))
            g.add(Line(pv, W(XB + LBL * math.cos(ang), YT + LBL * math.sin(ang)))
                  .set_stroke("#DCE4F2", lw * 1.15, oc).set_z_index(6))
            g.add(Dot(pv, radius=0.07 * s).set_fill("#DCE4F2", oc).set_z_index(6))

        # espiras da frente do solenoide
        if osl > 0.01:
            col = interpolate_color(ManimColor(COIL), ManimColor("#F3B6FF"), self.oHL.get_value())
            g.add(multi([Wv(p) for p in self.hfront]).set_stroke(col, lw * 0.95, osl).set_z_index(5))

        # secundária: frente, terminais e medidor/fonte
        if osc > 0.01:
            g.add(multi([Wv(p) for p in self.sfront]).set_stroke("#DCE4F2", lw * 0.9, osc).set_z_index(6))
            g.add(multi([Wv([(XM0, YT + A2), (XM0, YMET), (XC - MR, YMET)]),
                         Wv([(XM1, YT + A2), (XM1, YMET), (XC + MR, YMET)])]).set_stroke(STEEL, lw, osc).set_z_index(5))
            mc = W(XC, YMET)
            g.add(Circle(radius=MR * s).move_to(mc).set_fill(BACKGROUND_COLOR, osc).set_stroke(WHITE, 2.5, osc)
                  .set_z_index(6))
            osr = self.oSrc.get_value()
            if osr < 0.99:
                e2 = 0.0 if role2 else max(-1.0, min(1.0, -S["dI"]))
                ph = math.radians(65 * e2)
                p0 = mc + P3(0, -0.14 * s)
                g.add(Line(p0, p0 + 0.36 * s * P3(math.sin(ph), math.cos(ph))).set_stroke(CYAN, 3, osc * (1 - osr))
                      .set_z_index(7))
            if osr > 0.01:
                xs = np.linspace(-0.18, 0.18, 30)
                g.add(VMobject().set_points_smoothly([mc + s * P3(x, 0.08 * math.sin(x / 0.18 * PI * 2)) for x in xs])
                      .set_stroke(WHITE, 3, osc * osr).set_z_index(7))

        # capacitor (C20)
        if ocap > 0.01:
            for xp in (XP0, XP1):
                g.add(Line(W(xp, YT - PH), W(xp, YT + PH)).set_stroke("#DCE4F2", lw * 1.7, ocap).set_z_index(5))
            nq = int(round(6 * S["q"]))
            a = 0.06 * s
            for i in range(nq):
                y = YT - PH + 0.08 + (2 * PH - 0.16) * (i + 0.5) / 6
                c1, c2 = W(XP0 + 0.11, y), W(XP1 - 0.11, y)
                g.add(multi([[c1 + P3(-a, 0), c1 + P3(a, 0)], [c1 + P3(0, -a), c1 + P3(0, a)],
                             [c2 + P3(-a, 0), c2 + P3(a, 0)]]).set_stroke(IC, 2.5, ocap).set_z_index(6))

        # anel amperiano e superfícies (C20)
        oam = A * self.oAmp.get_value()
        if oam > 0.01:
            ring = Ellipse(width=0.32 * s, height=1.5 * s).move_to(W(XAMP, YT))
            g.add(ring.copy().set_fill(GEO, 0.22 * self.oS1.get_value() * oam).set_stroke(width=0).set_z_index(4))
            bag = VMobject().set_points_as_corners(Wv([(XAMP, YT + 0.75), (XC - 0.15, YT + 0.75), (XC, YT + 0.6),
                                                        (XC, YT - 0.6), (XC - 0.15, YT - 0.75), (XAMP, YT - 0.75)]))
            o2 = self.oS2.get_value() * oam
            if o2 > 0.01:
                g.add(DashedVMobject(bag, num_dashes=28, dashed_ratio=0.6).set_stroke(VIOLET, 3, o2).set_z_index(4))
            g.add(ring.set_fill(opacity=0).set_stroke(WHITE, 3, oam).set_z_index(7))
            ib = min(1.0, abs(S["I"]) * 2.5)
            if ib > 0.02:                                  # B em volta do fio: ⊙ em cima, ⊗ embaixo
                for k in (-1.3, -0.35):
                    pu, pd, r = W(k, YT + 0.42), W(k, YT - 0.42), 0.09 * s
                    g.add(Circle(radius=r).move_to(pu).set_stroke(MAGENTA, 2.5, oam * ib).set_z_index(6))
                    g.add(Dot(pu, radius=0.03 * s).set_fill(MAGENTA, oam * ib).set_z_index(6))
                    g.add(Circle(radius=r).move_to(pd).set_stroke(MAGENTA, 2.5, oam * ib).set_z_index(6))
                    g.add(multi([[pd + P3(-0.6 * r, -0.6 * r), pd + P3(0.6 * r, 0.6 * r)],
                                 [pd + P3(-0.6 * r, 0.6 * r), pd + P3(0.6 * r, -0.6 * r)]])
                          .set_stroke(MAGENTA, 2.5, oam * ib).set_z_index(6))

        # cargas em movimento (corrente convencional), velocidade ∝ I (fase em tick)
        od = A * self.oDots.get_value()
        I = S["I"]
        if od > 0.01:
            k = self.paths[self.path_key()]
            n = max(8, int(k.L / 0.55))
            xs, ys, zs = k.at(np.arange(n) / n + self.ph)
            base = od * (0.3 + 0.7 * min(1.0, abs(I)))
            for x, y, z in zip(xs, ys, zs):
                if self.mode == "cap" and XP0 - 0.03 < x < XP1 + 0.03 and abs(y - YT) < 0.1:
                    continue
                if z > 1.5:
                    f = osc if self.role == 2 and abs(y - YMET) < 0.01 or (self.role == 2 and abs(x - XM0) < 1e-6) \
                        else (osc if self.role == 2 else (oc if self.mode != "probe" else osl))
                    op, rr = base * f / max(A, 1e-6), 0.065
                else:
                    f = osc if self.role == 2 else osl
                    op, rr = base * f / max(A, 1e-6) * (1.0 if z >= 0 else 0.35), (0.065 if z >= 0 else 0.05)
                if op > 0.01:
                    g.add(Dot(W(x, y), radius=rr * min(s, 1.15)).set_fill(BLUE, op).set_stroke(BACKGROUND_COLOR, 1, op)
                          .set_z_index(7 if z >= 0 else 2))

        # fem autoinduzida ℰ_L (seta = sentido em que empurra a corrente; + na ponta)
        oe = osl * self.oEL.get_value()
        el = S["EL"]
        if oe > 0.01 and abs(el) > 0.02:
            y = YT + A_R + 0.45
            g.add(arrow(W(XC - 0.8 * el, y), W(XC + 0.8 * el, y), CYAN, 6, 9, 0.22 * min(s, 1.4), oe))
            sg, a, opm = (1 if el > 0 else -1), 0.08 * s, oe * min(1.0, 3 * abs(el))
            pp, pm = W(XC + sg * 1.95, y), W(XC - sg * 1.95, y)
            g.add(multi([[pp + P3(-a, 0), pp + P3(a, 0)], [pp + P3(0, -a), pp + P3(0, a)], [pm + P3(-a, 0), pm + P3(a, 0)]])
                  .set_stroke(CYAN, 3, opm).set_z_index(9))
        # fem da bateria (comparação em C09): mesma escala da seta de ℰ_L
        oeb = ob_ * self.oEB.get_value()
        if oeb > 0.01:
            g.add(arrow(W(XL + 0.62, -0.8), W(XL + 0.62, 0.8), WHITE, 6, 9, 0.22 * min(s, 1.4), oeb))
        # seta de corrente no fio de baixo (aponta para a esquerda), comprimento ∝ I
        oia = oc * self.oIA.get_value() * (0 if role2 else 1)
        if oia > 0.01 and abs(I) > 0.02:
            y = YB - 0.3
            g.add(arrow(W(XIA + 0.75 * I, y), W(XIA - 0.75 * I, y), BLUE, 6, 9, 0.2 * min(s, 1.4), oia))
        ois = osl * self.oIS.get_value()
        if ois > 0.01 and abs(I) > 0.02:
            y = YT - A_R - 0.62
            g.add(arrow(W(XC - 0.7 * I, y), W(XC + 0.7 * I, y), BLUE, 6, 9, 0.2 * min(s, 1.4), ois))
        return g


class Graf:
    """Eixos t × grandeza; curvas e marcador lidos de um tracker (unidades de τ)."""

    def __init__(self, sc, center=GC, w=5.5, h=2.8, xmax=5.0, ymax=1.15, one=None, ylab=None, ycol=WHITE,
                 ticks=True, tlab=True):
        self.sc, self.op, self.xmax, self.dyn = sc, ValueTracker(0.0), xmax, []
        ax = Axes(x_range=[0, xmax, 1], y_range=[0, ymax, 0.5], x_length=w, y_length=h, tips=False,
                  axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False}).move_to(P3(*center))
        self.ax = ax
        deco = VGroup()
        if ticks:
            for k in range(1, int(xmax) + 1):
                deco.add(Line(ax.c2p(k, 0), ax.c2p(k, 0.06), color=DIM, stroke_width=2))
                if tlab:
                    deco.add(MathTex(r"\tau" if k == 1 else rf"{k}\tau", font_size=24, color=DIM)
                             .move_to(ax.c2p(k, 0) + P3(0, -0.27)))
        deco.add(MathTex("0", font_size=24, color=DIM).move_to(ax.c2p(0, 0) + P3(-0.22, -0.18)))
        if one:
            deco.add(Line(ax.c2p(0, 1), ax.c2p(0.1 * xmax / 5, 1), color=DIM, stroke_width=2))
            deco.add(MathTex(one, font_size=26, color=DIM).next_to(ax.c2p(0, 1), LEFT, buff=0.12))
        if tlab:
            deco.add(MathTex("t", font_size=28, color=VIOLET).move_to(ax.c2p(xmax, 0) + P3(0.28, 0.0)))
        if ylab:
            deco.add(MathTex(ylab, font_size=28, color=ycol).next_to(ax.c2p(0, ymax), UP, buff=0.06))
        self.static = VGroup(ax, deco).set_z_index(4)

    def c2p(self, x, y):
        return self.ax.c2p(x, y)

    def curve(self, fn, tr, color, width=5, z=6):
        ax, op = self.ax, self.op

        def mk():
            x1 = min(tr.get_value(), self.xmax)
            o = op.get_value()
            if x1 < 0.02 or o < 0.01:
                return VMobject()
            return ax.plot(fn, x_range=[0, x1, max(0.02, x1 / 120)], color=color, stroke_width=width,
                           use_smoothing=False).set_stroke(opacity=o).set_z_index(z)
        m = always_redraw(mk)
        self.sc.add(m)
        self.dyn.append(m)
        return m

    def marker(self, fn, tr, color=WHITE, slope=None):
        ax, op = self.ax, self.op

        def mk():
            x = min(tr.get_value(), self.xmax)
            o = op.get_value()
            if o < 0.01:
                return VMobject()
            y = fn(x)
            g = VGroup(DashedLine(ax.c2p(x, 0), ax.c2p(x, y), dash_length=0.07, color=WHITE, stroke_width=2)
                       .set_opacity(0.45 * o),
                       Dot(ax.c2p(x, y), radius=0.08).set_fill(color, o).set_stroke(WHITE, 1.5, o))
            if slope is not None:                          # reta tangente (C06): sinal de dI/dt à vista
                d = slope(x)
                hw = 0.4 / max(1.0, abs(d) * 1.6)
                g.add(Line(ax.c2p(x - hw, y - hw * d), ax.c2p(x + hw, y + hw * d)).set_stroke(CYAN, 3, o))
            return g.set_z_index(9)
        m = always_redraw(mk)
        self.sc.add(m)
        self.dyn.append(m)
        return m

    def show(self):
        return [FadeIn(self.static), self.op.animate.set_value(1)]

    def hide(self):
        return [FadeOut(self.static), self.op.animate.set_value(0)]

    def drop(self):
        self.sc.remove(*self.dyn)
        self.dyn = []


class IndutanciaYT012(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        ap = self.ap = Ap()
        tickm = Mobject()
        tickm.add_updater(lambda m, dt: ap.tick(dt))
        self.add(tickm)
        self.tag = txt("ELETROMAGNETISMO · INDUTÂNCIA E ENERGIA MAGNÉTICA", 24, opacity=0.58) \
            .scale(0.84).to_corner(UL, buff=0.32).set_z_index(40)
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3)
        self.wm.set_z_index(40)
        self.add(self.tag, self.wm)
        self.body = always_redraw(ap.build)
        self.add(self.body)
        self.hd, self.E, self.marks = None, VGroup(), []
        self.mk_labels()
        for k in range(1, 21):
            getattr(self, f"c{k:02d}")()
        if not SEL:
            json.dump({"cenas": self.marks, "total": round(self.renderer.time, 2)},
                      open(PASTA / "tempos.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # ── utilidades ──────────────────────────────────────────────────────────────────────────────────────────
    def sec(self, k, nome):
        self.marks.append({"cena": f"C{k:02d}", "nome": nome, "t": round(self.renderer.time, 2)})
        if SEL:
            self.next_section(f"C{k:02d}", skip_animations=k not in SEL)

    def H(self, text):
        new = fitw(txt(text.upper(), T_BODY, opacity=0.9), 11.5).move_to(P3(0, 3.42)).set_z_index(30)
        old, self.hd = self.hd, new
        return ([FadeOut(old)] if old is not None else []) + [FadeIn(new)]

    def lay(self, name):
        ap = self.ap
        return [tr.animate.set_value(v) for tr, v in zip((ap.s, ap.cx, ap.cy, ap.fx, ap.fy), LAYOUTS[name])]

    def setlay(self, name):
        ap = self.ap
        for tr, v in zip((ap.s, ap.cx, ap.cy, ap.fx, ap.fy), LAYOUTS[name]):
            tr.set_value(v)

    def Wl(self, name, x, y):
        s, cx, cy, fx, fy = LAYOUTS[name]
        return P3(cx + s * (x - fx), cy + s * (y - fy))

    def lab(self, mob, anchor, off=(0, 0), color=WHITE, size=M_S, dep=None):
        """Rótulo preso ao aparato; dep = tracker extra de opacidade (circuito, solenoide, secundária…)."""
        ap = self.ap
        m = MathTex(mob, font_size=size, color=color) if isinstance(mob, str) else mob
        m.v = ValueTracker(0)
        deps = [getattr(ap, d) for d in (dep or [])]

        def upd(x):
            o = off() if callable(off) else off
            x.move_to(ap.W(*anchor()) + P3(*o) * ap.s.get_value())
            ov = m.v.get_value() * ap.oAll.get_value()
            for d in deps:
                ov *= d.get_value()
            x.set_opacity(ov)
            if isinstance(x, MathTex):
                x.set_stroke(BACKGROUND_COLOR, 8, ov, background=True)
        m.add_updater(upd)
        upd(m)
        m.set_z_index(20)
        self.add(m)
        return m

    def mk_labels(self):
        ap = self.ap
        L = self.L = {}
        cap1 = ["oCap"]
        L["E0"] = self.lab(r"\mathcal E_0", lambda: (XL, 0), (-0.55, 0), dep=["oCirc", "oBat"])
        L["R"] = self.lab("R", lambda: (XR, 0), (0.55, 0), dep=["oCirc"])
        L["sol"] = self.lab(txt("solenoide", 22, DIM), lambda: (XC, YT - A_R), (0, -0.36), dep=["oSol"])
        L["L"] = self.lab("L", lambda: (XC, YT - A_R), (0, -0.38), dep=["oSol"])
        L["B"] = self.lab(r"\mathbf B", lambda: (XS0 + 0.3, YT - A_R), (0, -0.38), MAGENTA, dep=["oSol", "oB"])
        L["I"] = self.lab("I", lambda: (XIA, YB - 0.3), (0, -0.34), IC, dep=["oCirc", "oIA"])
        L["I1"] = self.lab("I_1", lambda: (XIA, YB - 0.3), (0, -0.34), IC, dep=["oCirc", "oIA"])
        L["EL"] = self.lab(r"\mathcal E_L", lambda: (XC, YT + A_R + 0.45), (0, 0.38), CYAN, dep=["oSol", "oEL"])
        L["E1"] = self.lab(r"\mathcal E_1", lambda: (XC, YT + A_R + 0.45), (-1.3, 0.3), CYAN, dep=["oSol", "oEL"])
        L["E2"] = self.lab(r"\mathcal E_2", lambda: (XC + MR, YMET), (0.42, 0.05), CYAN, dep=["oSec"])
        L["N2"] = self.lab("N_2", lambda: (XM1, YT + A2), (0.45, 0.2), dep=["oSec"])
        L["I2"] = self.lab("I_2", lambda: (XM1, 0.5 * (YT + A2 + YMET)), (0.36, 0), IC, dep=["oSec"])
        L["med"] = self.lab(txt("medidor", 22, DIM), lambda: (XC, YMET), (0, 0.6), dep=["oSec"])
        L["fonte"] = self.lab(txt("fonte", 22, DIM), lambda: (XC, YMET), (0, 0.6), dep=["oSec"])
        L["A"] = self.lab("A", lambda: (HX0, YT), (-0.42, 0.0), MAGENTA, dep=["oSol"])
        L["ell"] = self.lab(r"\ell", lambda: (XC - KX, YT - A_R - 0.32), (0, -0.3), GEO, dep=["oSol"])
        L["C"] = self.lab("C", lambda: (XC, YT - PH), (0, -0.32), dep=cap1)
        L["S1"] = self.lab("S_1", lambda: (XAMP, YT - 0.75), (0, -0.3), GEO, size=26, dep=["oAmp", "oS1"])
        L["S2"] = self.lab("S_2", lambda: (XC, YT + 0.75), (0.1, 0.28), VIOLET, size=26, dep=["oAmp", "oS2"])
        L["I0gap"] = self.lab(r"I=0", lambda: (XC, YT), (0, 0), WHITE, size=24, dep=cap1)

    def show(self, *labs):
        return [m.v.animate.set_value(1) for m in labs]

    def hide(self, *labs):
        return [m.v.animate.set_value(0) for m in labs]

    def clrE(self):
        old, self.E = self.E, VGroup()
        return [FadeOut(old)] if len(old) else []

    def morph(self, a, b, pairs=None, t=T_MORPH, arcs=None, extra=()):
        """a → b por partes: pares (i, j) ou ((i1, i2, …), j); o que sobra some, o que falta aparece."""
        ta, tb = a.tex_strings, b.tex_strings
        if pairs is None:
            pairs, used = [], set()
            for i, x in enumerate(ta):
                for j, y in enumerate(tb):
                    if j not in used and x == y:
                        pairs.append((i, j))
                        used.add(j)
                        break
        anims, ia, ib = [], set(), set()
        for src, j in pairs:
            src = src if isinstance(src, (tuple, list)) else (src,)
            ia.update(src)
            ib.add(j)
            mob = a[src[0]] if len(src) == 1 else VGroup(*[a[i] for i in src])
            kw = {"path_arc": arcs[j]} if arcs and j in arcs else {}
            anims.append(ReplacementTransform(mob, b[j], **kw))
        gone = [a[i] for i in range(len(ta)) if i not in ia]
        came = [b[j] for j in range(len(tb)) if j not in ib]
        if gone and came:
            anims.append(ReplacementTransform(VGroup(*gone), VGroup(*came)))
        else:
            anims += [FadeOut(m) for m in gone] + [FadeIn(m) for m in came]
        self.play(*anims, *extra, run_time=t)
        self.remove(a, *a.submobjects, *b.submobjects, b)
        self.add(b)
        return b

    def restart(self, tr, label, x=EQX, y=-3.0):
        """Recomeça o mesmo processo em t = 0 (aviso visível: é a mesma experiência, não outra)."""
        ap = self.ap
        m = MathTex(label, font_size=26, color=WHITE)
        bx = VGroup(m, boxed(m, color=VIOLET, buff=0.12, width=2)).move_to(P3(x, y)).set_z_index(30)
        self.play(FadeIn(bx), ap.oDots.animate.set_value(0), run_time=0.5)
        tr.set_value(0.0)
        self.play(ap.oDots.animate.set_value(1), run_time=0.5)
        return bx

    def ring(self, p, w=1.0, h=1.0, color=WHITE):
        r = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(color, 4).move_to(p)
        self.play(Create(r), run_time=0.6)
        self.play(r.animate.set_stroke(opacity=0), run_time=0.6)
        self.remove(r)

    # ═══ C01 — a previsão que falha ═══════════════════════════════════════════════════════════════════════
    def c01(self):
        ap, L = self.ap, self.L
        self.sec(1, "previsao_que_falha")
        self.setlay("left")
        self.play(ap.oAll.animate.set_value(1), *self.H("Bateria, chave, solenoide e resistor"),
                  *self.show(L["E0"], L["R"], L["sol"]), run_time=T_MOVE)
        self.wait(T_READ)
        g = self.g = Graf(self, one=r"I_\infty", ylab="I", ycol=IC)
        i0 = M("I", "=", "0", size=M_L).move_to(P3(EQX, 2.05))
        ca = txt("chave aberta", T_NOTE, DIM).next_to(i0, DOWN, buff=0.22)
        self.play(*g.show(), FadeIn(i0), FadeIn(ca), run_time=T_EQ)
        self.wait(T_BEAT)
        pred = M("I", "=", r"\frac{\mathcal E_0}{R}", size=M_L).move_to(P3(EQX, 2.05))
        pn = txt("previsão: salto instantâneo", T_NOTE, DIM).next_to(pred, DOWN, buff=0.18)
        jump = DashedVMobject(VMobject().set_points_as_corners([g.c2p(0, 0), g.c2p(0, 1), g.c2p(5, 1)]),
                              num_dashes=48, dashed_ratio=0.55).set_stroke(WHITE, 3, 0.8).set_z_index(5)
        self.play(*self.H("O que esperamos ao fechar a chave?"), FadeOut(ca), run_time=T_FADE)
        self.play(TransformMatchingTex(i0, pred), run_time=T_EQ)
        self.play(FadeIn(pn), Create(jump), run_time=1.6)
        self.wait(T_READ)
        self.play(*self.H("Fechamos a chave"), FadeOut(pn), run_time=T_FADE)
        self.play(ap.sw.animate.set_value(SW_A), run_time=T_SW)
        g.curve(lambda x: 1 - math.exp(-x), ap.tc, BLUE, 5)
        g.marker(lambda x: 1 - math.exp(-x), ap.tc, BLUE)
        self.play(ap.oDots.animate.set_value(1), ap.oIA.animate.set_value(1), *self.show(L["I"], L["B"]),
                  run_time=0.6)
        self.play(ap.tc.animate.set_value(5), jump.animate.set_stroke(opacity=0.35), run_time=T_RUN, rate_func=linear)
        real = M("I(t)", "=", r"I_\infty", r"\left(1-e^{-t/\tau}\right)", size=M_L).move_to(P3(EQX, 2.05))
        self.play(FadeOut(pred), FadeIn(real), run_time=T_EQ)
        self.play(*self.H("A corrente deveria saltar."), run_time=T_FADE)
        self.wait(T_READ)
        self.play(*self.H("Mas não salta."), run_time=T_FADE)
        self.ring(self.Wl("left", XC - KX, YT), 3.0, 1.1, MAGENTA)
        self.E = VGroup(real, jump)
        self.wait(T_HOLD)

    # ═══ C02 — promessa ═════════════════════════════════════════════════════════════════════════════════════
    def c02(self):
        ap, L, g = self.ap, self.L, self.g
        self.sec(2, "promessa")
        logo = ImageMobject(str(LOGO_H)).set_width(3.0).move_to(P3(0, 1.6)).set_opacity(0.9)
        t1 = fitw(txt("POR QUE A CORRENTE RESISTE A MUDAR?", 44, CYAN), 13.0).move_to(P3(0, 0.25))
        t2 = txt("Indutância e energia magnética", 32, WHITE, 0.85).move_to(P3(0, -0.7))
        self.play(FadeOut(self.hd), *self.clrE(), *g.hide(), ap.oAll.animate.set_value(0.16), run_time=T_MOVE)
        self.hd = None
        g.drop()
        # reinício oculto pela atenuação: chave aberta, I = 0
        ap.tc.set_value(0)
        ap.sw.set_value(SW_OPEN)
        ap.oDots.set_value(0)
        ap.oIA.set_value(0)
        self.play(FadeIn(logo, scale=0.95), FadeIn(t1, shift=0.1 * UP), *self.hide(L["I"], L["B"]), run_time=1.2)
        self.play(FadeIn(t2), run_time=T_FADE)
        self.wait(T_HOLD)
        self.play(FadeOut(logo), FadeOut(t1), FadeOut(t2), ap.oAll.animate.set_value(1), run_time=T_MOVE)

    # ═══ C03 — indução mútua ════════════════════════════════════════════════════════════════════════════════
    def c03(self):
        ap, L = self.ap, self.L
        self.sec(3, "inducao_mutua")
        self.play(*self.H("Uma segunda bobina, em volta do solenoide"), *self.lay("mut"),
                  ap.oSec.animate.set_value(1), *self.show(L["N2"], L["E2"], L["med"]), *self.hide(L["sol"]),
                  run_time=T_MOVE)
        self.wait(T_READ)
        ch = M(r"I_1", r"\ \longrightarrow\ ", r"\mathbf B_1", r"\ \longrightarrow\ ", r"\Lambda_2",
               r"\ \longrightarrow\ ", r"\mathcal E_2", size=M_L).move_to(P3(EQX, 2.05))
        cps = [txt(t, T_CAP, DIM) for t in ("corrente", "campo", "fluxo", "fem")]
        for c, i in zip(cps, (0, 2, 4, 6)):
            c.next_to(ch[i], DOWN, buff=0.2)
        self.play(ap.sw.animate.set_value(SW_A), run_time=T_SW)
        # o transitório anda o tempo todo enquanto a cadeia se monta (tc linear, sem congelar)
        self.play(ap.oDots.animate.set_value(1), ap.oIA.animate.set_value(1), *self.show(L["I1"]),
                  FadeIn(ch[0]), FadeIn(cps[0]), ap.tc.animate.set_value(0.3), run_time=2.2, rate_func=linear)
        self.play(FadeIn(ch[1]), FadeIn(ch[2]), FadeIn(cps[1]), *self.show(L["B"]), ap.tc.animate.set_value(0.6),
                  run_time=2.2, rate_func=linear)
        self.play(FadeIn(ch[3]), FadeIn(ch[4]), FadeIn(cps[2]), ap.tc.animate.set_value(0.9), run_time=2.2,
                  rate_func=linear)
        self.play(FadeIn(ch[5]), FadeIn(ch[6]), FadeIn(cps[3]), ap.tc.animate.set_value(1.2), run_time=2.2,
                  rate_func=linear)
        e1 = M(r"\Lambda_2", "=", "M", "I_1", size=M_L).move_to(P3(EQX - 1.6, 0.75))
        e2 = M(r"\mathcal E_2", "=", "-M", r"\frac{dI_1}{dt}", size=M_L).move_to(P3(EQX + 1.5, 0.75))
        self.play(FadeIn(e1), ap.tc.animate.set_value(1.5), run_time=1.5, rate_func=linear)
        self.play(FadeIn(e2), ap.tc.animate.set_value(1.8), run_time=1.5, rate_func=linear)
        self.play(*self.H("Só há fem enquanto a corrente muda"), ap.tc.animate.set_value(5), run_time=6.0, rate_func=linear)
        self.wait(T_READ)
        # geometria: M = μ0 n N2 A
        self.play(*self.H("O coeficiente M vem da geometria"), run_time=T_FADE)
        br = Brace(VGroup(*[Dot(self.Wl("mut", x, YT + A_R + 0.05)) for x in (XS0, XS0 + 1.0)]), UP, buff=0.06,
                   color=GEO)
        bn = MathTex(r"n=\frac{N_1}{\ell}", font_size=26, color=GEO).next_to(br, UP, buff=0.06)
        g1 = M(r"\Lambda_2", "=", "N_2", r"\mathbf B_1", "A", size=M_M).move_to(P3(EQX, -0.45))
        g2 = M(r"\Lambda_2", "=", "N_2", r"(\mu_0 n I_1)", "A", size=M_M).move_to(P3(EQX, -0.45))
        g3 = M("M", "=", r"\mu_0 n N_2 A", size=M_L).move_to(P3(EQX, -1.75))
        nA = fitw(txt("A: seção do solenoide; fora dele o campo é quase nulo", T_CAP, DIM), 6.4).move_to(P3(EQX, -2.65))
        self.play(FadeIn(g1), ap.oAe.animate.set_value(1), *self.show(L["A"]), run_time=T_EQ)
        self.play(FadeIn(nA), run_time=T_FADE)
        self.wait(T_READ)
        self.play(FadeIn(br), FadeIn(bn), run_time=T_FADE)
        g2[3].set_color(MAGENTA)
        self.morph(g1, g2, pairs=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])
        self.wait(T_BEAT)
        self.play(TransformFromCopy(g2, g3), run_time=T_MORPH)
        b3 = boxed(g3)
        self.play(Create(b3), run_time=T_FADE)
        self.E = VGroup(ch, *cps, e1, e2, g2, g3, b3, nA, br, bn)
        self.wait(T_HOLD)

    # ═══ C04 — reciprocidade ════════════════════════════════════════════════════════════════════════════════
    def c04(self):
        ap, L = self.ap, self.L
        self.sec(4, "reciprocidade")
        ch, c0, c1, c2, c3, e1, e2, g2, g3, b3, nA, br, bn = self.E
        self.play(*self.H("Reciprocidade: trocamos os papéis"), FadeOut(VGroup(ch, c0, c1, c2, c3, e2, g2, nA, br, bn)),
                  VGroup(g3, b3).animate.move_to(P3(EQX, 2.05)), ap.oAe.animate.set_value(0), *self.hide(L["A"]),
                  ap.oDots.animate.set_value(0), ap.oIA.animate.set_value(0), ap.sw.animate.set_value(SW_OPEN),
                  ap.oBat.animate.set_value(0.35), run_time=T_MOVE)
        ap.tc.set_value(0)
        ap.role = 2
        f1 = M(r"\Lambda_2", "=", "M_{21}", "I_1", size=M_M).move_to(P3(EQX - 1.6, 0.8))
        self.play(ReplacementTransform(e1, f1), *self.hide(L["med"], L["E2"], L["I1"]), *self.show(L["fonte"], L["I2"]),
                  ap.oSrc.animate.set_value(1), run_time=T_EQ)
        self.play(*self.show(L["E1"]), ap.oEL.animate.set_value(1), ap.oDots.animate.set_value(1),
                  ap.tc.animate.set_value(0.4), run_time=1.6, rate_func=linear)
        f2 = M(r"\Lambda_1", "=", "M_{12}", "I_2", size=M_M).move_to(P3(EQX + 1.6, 0.8))
        f3 = M(r"\mathcal E_1", "=", "-M_{12}", r"\frac{dI_2}{dt}", size=M_M).move_to(P3(EQX + 1.6, -0.3))
        self.play(FadeIn(f2), ap.tc.animate.set_value(0.8), run_time=1.6, rate_func=linear)
        self.play(FadeIn(f3), ap.tc.animate.set_value(1.2), run_time=1.6, rate_func=linear)
        self.play(ap.tc.animate.set_value(4), run_time=4.0, rate_func=linear)
        r = M("M_{12}", "=", "M_{21}", size=M_XL).move_to(P3(EQX, -1.45))
        rb = boxed(r)
        rc = txt("mesma geometria, mesmo coeficiente", T_CAP, DIM).next_to(rb, DOWN, buff=0.2)
        self.play(FadeIn(r), Create(rb), FadeIn(rc), run_time=T_EQ)
        self.wait(T_HOLD)
        q = fitw(txt("E se o segundo circuito desaparecer?", 36, CYAN), 7.0).move_to(P3(EQX, -2.85))
        self.play(*self.H("E se o segundo circuito desaparecer?"), FadeIn(q), run_time=T_FADE)
        self.E = VGroup(g3, b3, f1, f2, f3, r, rb, rc, q)
        self.wait(T_READ)

    # ═══ C05 — mútua vira autoindução ═══════════════════════════════════════════════════════════════════════
    def c05(self):
        ap, L = self.ap, self.L
        self.sec(5, "mutua_vira_autoinducao")
        g3, b3, f1, f2, f3, r, rb, rc, q = self.E
        e1 = M(r"\Lambda_2", "=", "M", "I_1", size=M_L).move_to(P3(EQX, 1.45))
        e2 = M(r"\mathcal E_2", "=", "-M", r"\frac{dI_1}{dt}", size=M_L).move_to(P3(EQX, 0.1))
        self.play(FadeOut(VGroup(g3, b3, f2, f3, r, rb, rc, q)), ReplacementTransform(f1, e1),
                  *self.hide(L["E1"], L["I2"], L["fonte"]), ap.oEL.animate.set_value(0), ap.oDots.animate.set_value(0),
                  ap.oBat.animate.set_value(1), run_time=T_MOVE)
        ap.role = 1
        ap.tc.set_value(0)
        ap.oSrc.set_value(0)
        self.play(FadeIn(e2), *self.lay("left"), ap.sw.animate.set_value(SW_A), run_time=T_MOVE)
        self.play(*self.H("A bobina 2 sai; o campo continua"), ap.oSec.animate.set_value(0),
                  *self.hide(L["N2"]), run_time=T_MOVE)
        self.play(ap.oDots.animate.set_value(1), ap.oIA.animate.set_value(1), *self.show(L["I"]),
                  ap.tc.animate.set_value(0.4), run_time=2.0, rate_func=linear)
        self.play(*self.H("O campo atravessa as próprias espiras"), ap.oHL.animate.set_value(1),
                  ap.tc.animate.set_value(0.8), run_time=2.0, rate_func=linear)
        self.play(ap.oHL.animate.set_value(0.25), ap.tc.animate.set_value(1.0), run_time=1.2, rate_func=linear)
        n1 = M(r"\Lambda", "=", "L", "I", size=M_XL).move_to(P3(EQX, 1.45))
        self.morph(e1, n1, pairs=[(0, 0), (1, 1), (2, 2), (3, 3)],
                   extra=[ap.tc.animate.set_value(1.25)])
        nc = txt("L: autoindutância (só geometria)", T_CAP, DIM).next_to(n1, DOWN, buff=0.2)
        self.play(FadeIn(nc), *self.hide(L["sol"]), *self.show(L["L"]), run_time=T_FADE)
        self.wait(T_BEAT)
        n2 = M(r"\mathcal E_L", "=", "-L", r"\frac{dI}{dt}", size=M_XL).move_to(P3(EQX, -0.3))
        self.morph(e2, n2, pairs=[(0, 0), (1, 1), (2, 2), (3, 3)], extra=[ap.tc.animate.set_value(1.5)])
        b2 = boxed(n2, buff=0.2)
        un = MathTex(r"[L]=\mathrm{H}=\frac{\mathrm{V\,s}}{\mathrm{A}}", font_size=30, color=DIM).move_to(P3(EQX, -1.75))
        self.play(Create(b2), *self.show(L["EL"]), ap.oEL.animate.set_value(1), ap.oHL.animate.set_value(0),
                  ap.tc.animate.set_value(1.8), run_time=T_EQ, rate_func=linear)
        self.play(FadeIn(un), ap.tc.animate.set_value(2.3), run_time=T_EQ, rate_func=linear)
        self.E = VGroup(n1, nc, n2, b2, un)
        self.play(ap.tc.animate.set_value(3.2), run_time=T_READ, rate_func=linear)

    # ═══ C06 — o que o indutor combate ══════════════════════════════════════════════════════════════════════
    def c06(self):
        ap, L = self.ap, self.L
        self.sec(6, "o_que_o_indutor_combate")
        self.play(*self.H("O que o indutor realmente combate"), *self.clrE(), *self.lay("solo"),
                  ap.oCirc.animate.set_value(0), ap.oDots.animate.set_value(0), *self.hide(L["I"]),
                  run_time=T_MOVE)
        ap.mode = "probe"
        ap.sp.set_value(0)
        gp = Graf(self, center=(EQX, -1.55), w=5.4, h=1.9, xmax=3.2, ticks=False, ylab="I", ycol=IC)
        gp.curve(lambda x: probe(x)[0], ap.sp, BLUE, 5)
        gp.marker(lambda x: probe(x)[0], ap.sp, BLUE, slope=lambda x: probe(x)[1] * PI / 2)
        nt = txt("corrente imposta por uma fonte ajustável", T_CAP, DIM).move_to(P3(EQX, 2.25))
        self.play(*gp.show(), FadeIn(nt), ap.oIS.animate.set_value(1), ap.oDots.animate.set_value(1),
                  run_time=T_EQ)
        self.play(ap.sp.animate.set_value(0.5), run_time=2.5, rate_func=linear)
        k1 = M(r"\frac{dI}{dt}>0", r"\Rightarrow", r"\mathcal E_L", r"\text{ contra } I", size=M_M, col={3: IC}) \
            .move_to(P3(EQX, 1.35))
        self.play(FadeIn(k1), run_time=T_EQ)
        self.wait(T_READ)
        self.play(ap.sp.animate.set_value(2.5), run_time=6.0, rate_func=linear)
        k2 = M(r"\frac{dI}{dt}<0", r"\Rightarrow", r"\mathcal E_L", r"\text{ a favor de } I", size=M_M, col={3: IC}) \
            .move_to(P3(EQX, 0.35))
        self.play(FadeIn(k2), run_time=T_EQ)
        self.wait(T_READ)
        self.play(ap.sp.animate.set_value(3.0), run_time=1.5, rate_func=linear)
        # payoff
        p1 = fitw(txt("O indutor não se opõe à corrente", 36, WHITE), 12.5).move_to(P3(0, 0.55))
        p2 = fitw(txt("Ele se opõe à MUDANÇA da corrente", 42, CYAN), 12.5).move_to(P3(0, -0.55))
        dim = Rectangle(width=16, height=6.2).set_fill(BACKGROUND_COLOR, 0.86).set_stroke(width=0).move_to(P3(0, -0.4)) \
            .set_z_index(25)
        p1.set_z_index(26)
        p2.set_z_index(26)
        self.play(FadeIn(dim), FadeIn(p1), run_time=T_EQ)
        self.wait(T_BEAT)
        self.play(FadeIn(p2, shift=0.1 * UP), run_time=T_EQ)
        self.wait(T_HOLD)
        # corrente constante: I ≠ 0, dI/dt = 0, ℰ_L = 0
        self.play(FadeOut(p1), FadeOut(p2), FadeOut(dim), FadeOut(k1), FadeOut(k2), ap.oDots.animate.set_value(0),
                  run_time=T_FADE)
        ap.sp.set_value(0)
        self.play(*self.H("E com corrente constante?"), ap.oDots.animate.set_value(1), run_time=T_FADE)
        self.play(ap.sp.animate.set_value(1.5), run_time=4.0, rate_func=linear)
        z = VGroup(M(r"I\neq0", size=M_M, col={0: IC}), M(r"B\neq0", size=M_M),
                   M(r"\frac{dI}{dt}=0", size=M_M, col={0: IC}), M(r"\mathcal E_L=0", size=M_M)) \
            .arrange_in_grid(2, 2, buff=(1.2, 0.35)).move_to(P3(EQX, 0.95))
        self.play(LaggedStart(*[FadeIn(m) for m in z], lag_ratio=0.5), run_time=2.4)
        self.ring(z[3].get_center(), z[3].width + 0.4, z[3].height + 0.3, CYAN)
        self.E = VGroup(nt, z)
        self.gp = gp
        self.wait(T_HOLD)

    # ═══ C07 — equação RL ═══════════════════════════════════════════════════════════════════════════════════
    def c07(self):
        ap, L, gp = self.ap, self.L, self.gp
        self.sec(7, "equacao_rl")
        self.play(*self.H("De volta ao circuito: a lei das malhas"), *self.clrE(), *gp.hide(), *self.lay("left"),
                  ap.oCirc.animate.set_value(1), ap.oIS.animate.set_value(0), ap.oDots.animate.set_value(0),
                  run_time=T_MOVE)
        gp.drop()
        ap.mode = "charge"
        ap.tc.set_value(0.9)
        self.play(ap.oDots.animate.set_value(1), ap.oIA.animate.set_value(1), *self.show(L["I"]), run_time=T_FADE)
        eq = M(r"\mathcal E_0", "-", r"L\frac{dI}{dt}", "=", "R", "I", size=M_XL, col={2: CYAN})
        eq.move_to(P3(EQX, 1.0))
        self.play(*self.H("A fonte empurra"), run_time=T_FADE)
        self.ring(self.Wl("left", XL, 0), 1.0, 1.0)
        self.play(TransformFromCopy(L["E0"], eq[0]), run_time=T_EQ)
        self.wait(T_BEAT)
        self.play(*self.H("O indutor reage"), run_time=T_FADE)
        self.ring(self.Wl("left", XC - KX, YT), 2.9, 1.0, CYAN)
        self.play(FadeIn(eq[1]), TransformFromCopy(L["EL"], eq[2]), run_time=T_EQ)
        self.wait(T_BEAT)
        self.play(*self.H("O resistor consome"), run_time=T_FADE)
        self.ring(self.Wl("left", XR, 0), 0.9, 1.4, HEAT)
        self.play(FadeIn(eq[3]), TransformFromCopy(L["R"], eq[4]), TransformFromCopy(L["I"], eq[5]), run_time=T_EQ)
        self.remove(*eq.submobjects)
        self.add(eq)
        self.wait(T_READ)
        eq2 = M(r"L\frac{dI}{dt}", "+", "R", "I", "=", r"\mathcal E_0", size=M_XL, col={0: CYAN}).move_to(P3(EQX, 1.0))
        self.play(*self.H("Organizando"), run_time=T_FADE)
        self.morph(eq, eq2, pairs=[(2, 0), (4, 2), (5, 3), (3, 4), (0, 5)], arcs={0: PI / 2, 5: -PI / 2})
        self.E = VGroup(eq2)
        self.wait(T_HOLD)

    # ═══ C08 — resolver a dinâmica ══════════════════════════════════════════════════════════════════════════
    def c08(self):
        ap = self.ap
        self.sec(8, "resolver_dinamica")
        (e1,) = self.E
        self.play(*self.H("Resolvendo a dinâmica"), e1.animate.move_to(P3(EQX, 0.4)), run_time=T_MOVE)
        e2 = M(r"\frac{dI}{dt}", "=", r"\frac{\mathcal E_0-RI}{L}", size=M_XL).move_to(P3(EQX, 0.4))
        self.morph(e1, e2, pairs=[(0, 0), (4, 1)])
        self.wait(T_READ)
        e3 = M(r"\frac{dI}{dt}", "=", r"\frac{R}{L}", r"\Big(", r"\frac{\mathcal E_0}{R}", "-", "I", r"\Big)",
               size=M_XL).move_to(P3(EQX, 0.4))
        self.morph(e2, e3, pairs=[(0, 0), (1, 1)])
        self.wait(T_BEAT)
        d1 = M(r"I_\infty", "=", r"\frac{\mathcal E_0}{R}", size=M_M).move_to(P3(EQX - 1.6, 2.05))
        d2 = M(r"\tau", "=", r"\frac{L}{R}", size=M_M).move_to(P3(EQX + 1.6, 2.05))
        c1 = txt("corrente final", T_CAP, DIM).next_to(d1, DOWN, buff=0.12)
        c2 = txt("constante de tempo", T_CAP, DIM).next_to(d2, DOWN, buff=0.12)
        self.play(FadeIn(d1), FadeIn(c1), run_time=T_EQ)
        self.play(FadeIn(d2), FadeIn(c2), run_time=T_EQ)
        self.wait(T_BEAT)
        e4 = M(r"\frac{dI}{dt}", "=", r"\frac{I_\infty-I}{\tau}", size=M_XL).move_to(P3(EQX, 0.4))
        self.morph(e3, e4, pairs=[(0, 0), (1, 1), ((2, 3, 4, 5, 6, 7), 2)])
        cm = txt("longe do valor final, I muda depressa", T_CAP, DIM).move_to(P3(EQX, -0.75))
        self.play(FadeIn(cm), run_time=T_FADE)
        self.wait(T_READ)
        e5 = M(r"\frac{dI}{I_\infty-I}", "=", r"\frac{dt}{\tau}", size=M_XL).move_to(P3(EQX, 0.4))
        self.play(FadeOut(cm), run_time=0.4)
        self.morph(e4, e5, pairs=[(0, 0), (1, 1), (2, 2)])
        ci = M("I(0)", "=", "0", size=M_M).move_to(P3(EQX, -1.0))
        self.play(FadeIn(ci), run_time=T_FADE)
        self.wait(T_BEAT)
        e6 = M(r"-\ln\frac{I_\infty-I}{I_\infty}", "=", r"\frac{t}{\tau}", size=M_XL).move_to(P3(EQX, 0.4))
        self.morph(e5, e6, pairs=[(0, 0), (1, 1), (2, 2)])
        self.wait(T_BEAT)
        e7 = M("I(t)", "=", r"I_\infty", r"\left(1-e^{-t/\tau}\right)", size=M_XL).move_to(P3(EQX, 0.4))
        self.morph(e6, e7, pairs=[(1, 1)])
        b7 = boxed(e7, buff=0.2)
        ck = M(r"I(0)=0", r"\qquad", r"I(\infty)=I_\infty", size=M_S, col={0: IC, 2: IC}).move_to(P3(EQX, -1.0))
        self.play(Create(b7), ReplacementTransform(ci, ck), run_time=T_EQ)
        self.E = VGroup(d1, d2, c1, c2, e7, b7, ck)
        self.wait(T_HOLD)

    # ═══ C09 — uma escala controla tudo ═════════════════════════════════════════════════════════════════════
    def c09(self):
        ap, L = self.ap, self.L
        self.sec(9, "escala_tau")
        d1, d2, c1, c2, e7, b7, ck = self.E
        top = VGroup(e7, b7)
        g = self.g = Graf(self, one=r"I_\infty", ylab="I", ycol=IC)
        self.play(*self.H("Uma única escala de tempo controla tudo"), FadeOut(VGroup(d1, d2, c1, c2, ck)),
                  top.animate.scale(0.7).move_to(P3(EQX, 2.2)), *g.show(), ap.oEB.animate.set_value(1),
                  ap.oEL.animate.set_value(1), *self.show(L["EL"]), run_time=T_MOVE)
        bx = self.restart(ap.tc, r"\text{repetindo a carga desde }t=0")
        g.curve(lambda x: 1 - math.exp(-x), ap.tc, BLUE, 5)
        g.marker(lambda x: 1 - math.exp(-x), ap.tc, BLUE)
        tg = DashedLine(g.c2p(0, 0), g.c2p(1, 1), dash_length=0.08, color=VIOLET, stroke_width=3).set_z_index(5)
        tl = MathTex(r"\text{inclinação }\frac{\mathcal E_0}{L}", font_size=26, color=VIOLET) \
            .next_to(g.c2p(1, 1), RIGHT, buff=0.15).shift(0.12 * DOWN)
        p0 = M(r"t=0:", "I=0", r"\frac{dI}{dt}=\frac{\mathcal E_0}{L}", r"|\mathcal E_L|=\mathcal E_0", size=M_S,
               col={1: IC, 2: IC}).arrange(RIGHT, buff=0.45).move_to(P3(EQX, 1.35))
        self.play(FadeOut(bx), FadeIn(p0), run_time=T_EQ)
        self.play(Create(tg), FadeIn(tl), run_time=T_EQ)
        self.wait(T_READ)
        self.play(ap.tc.animate.set_value(1.0), run_time=4.0, rate_func=linear)
        y1 = 1 - math.exp(-1)
        mk = VGroup(DashedLine(g.c2p(1, 0), g.c2p(1, y1), dash_length=0.06, color=WHITE, stroke_width=2.5),
                    DashedLine(g.c2p(0, y1), g.c2p(1, y1), dash_length=0.06, color=WHITE, stroke_width=2.5),
                    MathTex(r"I(\tau)\approx0{,}632\,I_\infty", font_size=28, color=IC)
                    .next_to(g.c2p(1, y1), RIGHT, buff=0.2).shift(0.25 * DOWN)).set_z_index(8)
        self.play(FadeIn(mk), run_time=T_EQ)
        self.wait(T_READ)
        self.play(ap.tc.animate.set_value(5.0), FadeOut(tl), run_time=6.0, rate_func=linear)
        p1 = M(r"t\gg\tau:", r"I\to I_\infty", r"\frac{dI}{dt}\to0", r"\mathcal E_L\to0", size=M_S,
               col={2: IC}).arrange(RIGHT, buff=0.45).move_to(P3(EQX, 1.35))
        self.play(ReplacementTransform(p0, p1), run_time=T_EQ)
        self.E = VGroup(top, tg, mk, p1)
        self.wait(T_HOLD)

    # ═══ C10 — B cresce, E induzido some ════════════════════════════════════════════════════════════════════
    XS_C, XS_A = P3(-4.4, -1.55), 0.72

    def xsec(self):
        """Corte transversal do solenoide (B saindo da tela) com E_φ(r) induzido, lido do mesmo estado."""
        ap = self.ap
        o = self.oXs.get_value()
        g = VGroup()
        if o < 0.01:
            return g
        S = ap.st()
        c, a, B, dI = self.XS_C, self.XS_A, S["B"], S["dI"]
        g.add(Circle(radius=a, arc_center=c).set_stroke(COIL, 3, o).set_z_index(3))
        if B > 0.01:
            g.add(Circle(radius=a, arc_center=c).set_fill(MAGENTA, o * (0.05 + 0.2 * B)).set_stroke(width=0)
                  .set_z_index(1))
            for i in range(-2, 3):
                for j in range(-2, 3):
                    p = c + P3(0.26 * i + 0.13 * (j % 2), 0.24 * j)
                    if np.linalg.norm(p - c) < 0.84 * a:
                        g.add(Circle(radius=0.055, arc_center=p).set_stroke(MAGENTA, 2, o * min(1, B)).set_z_index(2))
                        g.add(Dot(p, radius=0.018).set_fill(MAGENTA, o * min(1, B)).set_z_index(2))
        for rr in (0.35, 0.7, 1.3, 1.75):
            e = (rr if rr < 1 else 1 / rr) * dI             # |E_φ| ∝ r dentro, ∝ a²/r fora
            m = abs(e)
            if m < 0.03:
                continue
            r = rr * a
            g.add(DashedVMobject(Circle(radius=r, arc_center=c), num_dashes=int(14 + 10 * r), dashed_ratio=0.55)
                  .set_stroke(CYAN, 2.5, o * min(1.0, 0.25 + m)).set_z_index(4))
            for k in range(4):
                th = PI / 4 + k * PI / 2 + 0.3 * rr
                p = c + r * P3(math.cos(th), math.sin(th))
                t = P3(math.sin(th), -math.cos(th)) * (1 if dI > 0 else -1)   # E_φ < 0 ⇒ horário (Lenz)
                L = 0.12 + 0.3 * m
                g.add(arrow(p - t * L / 2, p + t * L / 2, CYAN, 4, 5, 0.13, o * min(1.0, 0.3 + m)))
        return g

    def c10(self):
        ap, L = self.ap, self.L
        self.sec(10, "b_cresce_e_some")
        top, tg, mk, p1 = self.E
        g = self.g
        self.oXs = ValueTracker(0)
        xs = always_redraw(self.xsec)
        self.add(xs)
        c, a = self.XS_C, self.XS_A
        link = DashedLine(self.Wl("thumb", HX1, YT - A_R), c + P3(0.55, 0.85), dash_length=0.08, color=DIM,
                          stroke_width=2)
        cl = txt("corte: B saindo da tela", T_CAP, DIM).move_to(c + P3(0, -1.55))
        ra = VGroup(Line(c, c + P3(a, 0), color=GEO, stroke_width=2.5),
                    MathTex("a", font_size=26, color=GEO).move_to(c + P3(a / 2, 0.18))).set_z_index(6)
        self.play(*self.H("B cresce enquanto o campo elétrico induzido some"), FadeOut(VGroup(top, tg, mk, p1)),
                  *g.hide(), *self.lay("thumb"), *self.hide(L["E0"], L["R"], L["I"], L["L"], L["B"], L["EL"]),
                  ap.oEB.animate.set_value(0), run_time=T_MOVE)
        g.drop()
        self.play(self.oXs.animate.set_value(1), Create(link), FadeIn(cl), FadeIn(ra), run_time=T_EQ)
        b1 = M("B(t)", "=", r"\mu_0 n", "I(t)", size=M_M).move_to(P3(2.9, 2.05))
        b2 = M(r"\frac{dB}{dt}", "=", r"\mu_0 n", r"\frac{dI}{dt}", size=M_M).move_to(P3(2.9, 1.05))
        self.play(FadeIn(b1), FadeIn(b2), run_time=T_EQ)
        bx = self.restart(ap.tc, r"\text{repetindo a carga desde }t=0", x=2.9)
        r1 = M(r"r<a:", r"E_\phi", "=", r"-\frac{\mu_0 n r}{2}", r"\frac{dI}{dt}", size=M_M).move_to(P3(2.9, -0.15))
        r2 = M(r"r>a:", r"E_\phi", "=", r"-\frac{\mu_0 n a^2}{2r}", r"\frac{dI}{dt}", size=M_M).move_to(P3(2.9, -1.45))
        self.play(FadeOut(bx), FadeIn(r1), ap.tc.animate.set_value(0.25), run_time=T_EQ, rate_func=linear)
        self.play(FadeIn(r2), ap.tc.animate.set_value(0.5), run_time=T_EQ, rate_func=linear)
        self.play(ap.tc.animate.set_value(5.0), run_time=T_RUN, rate_func=linear)
        pf = M(r"\text{regime:}\quad", r"B\neq0", r",\quad", r"E_{\rm ind}=0", size=M_L).move_to(P3(2.9, -2.65))
        pb = boxed(pf, buff=0.18)
        self.play(FadeIn(pf), Create(pb), run_time=T_EQ)
        self.xs, self.E = xs, VGroup(b1, b2, r1, r2, pf, pb, link, cl, ra)
        self.wait(T_HOLD)

    # ═══ C11 — construir o campo custa energia ══════════════════════════════════════════════════════════════
    def c11(self):
        ap, L = self.ap, self.L
        self.sec(11, "custo_energia")
        self.play(*self.H("Construir o campo custa energia"), *self.clrE(), self.oXs.animate.set_value(0),
                  *self.lay("left"), *self.show(L["E0"], L["R"], L["I"], L["L"], L["B"], L["EL"]), run_time=T_MOVE)
        self.remove(self.xs)
        bx = self.restart(ap.tc, r"\text{repetindo a carga desde }t=0")
        self.play(FadeOut(bx), ap.tc.animate.set_value(0.6), run_time=2.0, rate_func=linear)
        eq = M(r"\mathcal E_0", "-", r"L\frac{dI}{dt}", "=", "R", "I", size=M_XL, col={2: CYAN}).move_to(P3(EQX, 1.3))
        self.play(FadeIn(eq), ap.tc.animate.set_value(0.8), run_time=T_EQ, rate_func=linear)
        xI = M(r"\times", "I", size=M_XL).next_to(eq, RIGHT, buff=0.35)
        self.play(FadeIn(xI, shift=0.2 * LEFT), ap.tc.animate.set_value(1.0), run_time=T_EQ, rate_func=linear)
        eqI = M(r"\mathcal E_0", "I", "-", r"LI\frac{dI}{dt}", "=", "R", "I^2", size=M_XL, col={3: MAGENTA}) \
            .move_to(P3(EQX, 1.3))
        self.play(ReplacementTransform(eq[0], eqI[0]), ReplacementTransform(eq[1], eqI[2]),
                  ReplacementTransform(eq[2], eqI[3]), ReplacementTransform(eq[3], eqI[4]),
                  ReplacementTransform(eq[4], eqI[5]), ReplacementTransform(eq[5], eqI[6]),
                  ReplacementTransform(xI[1], eqI[1]), FadeOut(xI[0]), ap.tc.animate.set_value(1.3),
                  run_time=T_MORPH, rate_func=linear)
        self.remove(eq, *eqI.submobjects)
        self.add(eqI)
        bs = [Brace(VGroup(eqI[0], eqI[1]), DOWN, buff=0.12, color=DIM), Brace(eqI[3], DOWN, buff=0.12, color=MAGENTA),
              Brace(VGroup(eqI[5], eqI[6]), DOWN, buff=0.12, color=HEAT)]
        ls = [txt("potência da fonte", T_CAP, DIM), MathTex("?", font_size=40, color=MAGENTA),
              txt("potência no resistor", T_CAP, HEAT)]
        for b, l in zip(bs, ls):
            l.next_to(b, DOWN, buff=0.1)
        ls[0].align_to(bs[0], LEFT).shift(0.3 * LEFT)
        ls[2].align_to(bs[2], RIGHT).shift(0.3 * DOWN)
        self.play(FadeIn(bs[0]), FadeIn(ls[0]), ap.tc.animate.set_value(1.6), run_time=T_EQ, rate_func=linear)
        self.play(FadeIn(bs[2]), FadeIn(ls[2]), ap.tc.animate.set_value(1.9), run_time=T_EQ, rate_func=linear)
        self.play(FadeIn(bs[1]), FadeIn(ls[1]), ap.tc.animate.set_value(2.2), run_time=T_EQ, rate_func=linear)
        self.E = VGroup(eqI, *bs, *ls)
        self.play(ap.tc.animate.set_value(2.8), run_time=T_READ, rate_func=linear)

    # ═══ C12 — a potência se divide ═════════════════════════════════════════════════════════════════════════
    def pbars(self):
        """Potências (unidade ℰ₀ I_∞) e U_B (unidade ½ L I_∞²) a cada quadro, do mesmo tc."""
        ap = self.ap
        o = self.oBars.get_value()
        g = VGroup()
        if o < 0.01:
            return g
        S = ap.st()
        I, dI = S["I"], S["dI"]
        Pf, PJ, PL = I, I * I, I * dI                     # PJ + PL = Pf (balanço exato)
        Hh, base, x0, x1, w = 2.0, -2.75, 2.9, 5.6, 0.8
        g.add(Rectangle(width=w, height=Hh).move_to(P3(x0, base + Hh / 2)).set_stroke(DIM, 2, o).set_fill(opacity=0))
        if PJ > 0.004:
            g.add(Rectangle(width=w, height=Hh * PJ).move_to(P3(x0, base + Hh * PJ / 2)).set_fill(HEAT, 0.85 * o)
                  .set_stroke(width=0))
        if PL > 0.004:
            g.add(Rectangle(width=w, height=Hh * PL).move_to(P3(x0, base + Hh * (PJ + PL / 2))).set_fill(MAGENTA, 0.85 * o)
                  .set_stroke(width=0))
        g.add(Line(P3(x0 - w / 2 - 0.1, base + Hh * Pf), P3(x0 + w / 2 + 0.1, base + Hh * Pf)).set_stroke(WHITE, 3, o))
        g.add(Rectangle(width=w, height=Hh).move_to(P3(x1, base + Hh / 2)).set_stroke(DIM, 2, o).set_fill(opacity=0))
        if S["UB"] > 0.004:
            g.add(Rectangle(width=w, height=Hh * S["UB"]).move_to(P3(x1, base + Hh * S["UB"] / 2))
                  .set_fill(MAGENTA, 0.6 * o).set_stroke(MAGENTA, 2, o))
        return g.set_z_index(6)

    def c12(self):
        ap = self.ap
        self.sec(12, "potencia_se_divide")
        eqI, b0, b1, b2, l0, l1, l2 = self.E
        self.play(*self.H("A potência se divide"), FadeOut(VGroup(b0, b1, b2, l0, l1, l2)), run_time=T_FADE)
        e1 = M(r"\mathcal E_0", "I", "=", "I^2R", "+", r"LI\frac{dI}{dt}", size=M_XL, col={5: MAGENTA}) \
            .move_to(P3(EQX, 1.3))
        self.morph(eqI, e1, pairs=[(0, 0), (1, 1), (3, 5), (4, 2), ((5, 6), 3)], arcs={5: PI / 2, 3: -PI / 2})
        self.wait(T_READ)
        side = M(r"LI\frac{dI}{dt}", "=", r"\frac{d}{dt}\Big(\tfrac12 LI^2\Big)", size=M_L, col={0: MAGENTA, 2: MAGENTA}) \
            .move_to(P3(EQX, -0.45))
        sc = MathTex(r"\text{regra da cadeia: }\frac{d(I^2)}{dt}=2I\frac{dI}{dt}", font_size=28, color=DIM) \
            .next_to(side, DOWN, buff=0.22)
        self.play(TransformFromCopy(e1[5], side[0]), FadeIn(side[1]), FadeIn(side[2]), FadeIn(sc), run_time=T_EQ)
        self.remove(*side.submobjects)
        self.add(side)
        self.wait(T_READ)
        e2 = M(r"\mathcal E_0", "I", "=", "I^2R", "+", r"\frac{d}{dt}\Big(\tfrac12 LI^2\Big)", size=M_XL,
               col={5: MAGENTA}).move_to(P3(EQX, 1.3))
        self.play(ReplacementTransform(e1[5], e2[5]), FadeOut(side), FadeOut(sc),
                  *[ReplacementTransform(e1[i], e2[i]) for i in range(5)], run_time=T_MORPH)
        self.remove(e1, *e2.submobjects)
        self.add(e2)
        self.wait(T_BEAT)
        f = M(r"P_{\rm fonte}", "=", r"P_{\rm Joule}", "+", r"\frac{dU_B}{dt}", size=64).move_to(P3(EQX, 1.3))
        self.play(*self.H("O balanço de potência"), run_time=T_FADE)
        self.morph(e2, f, pairs=[((0, 1), 0), (2, 1), (3, 2), (4, 3), (5, 4)], t=2.2)
        fb = boxed(f, buff=0.22)
        u = M("U_B", "=", r"\tfrac12", "L", "I^2", size=M_XL).move_to(P3(EQX, -0.5))
        ub = boxed(u, color=MAGENTA, buff=0.2)
        self.play(Create(fb), run_time=T_FADE)
        self.wait(T_READ)
        self.play(FadeIn(u), Create(ub), run_time=T_EQ)
        self.wait(T_HOLD)
        # o mesmo transitório, agora como divisão de potência
        self.oBars = ValueTracker(0)
        bars = always_redraw(self.pbars)
        self.add(bars)
        lb = VGroup(MathTex(r"P_{\rm fonte}", font_size=30).move_to(P3(2.9, -0.45)),
                    MathTex("U_B", font_size=30, color=MAGENTA).move_to(P3(5.6, -0.45)),
                    txt("campo", T_CAP, MAGENTA).move_to(P3(4.0, -1.0)),
                    txt("joule", T_CAP, HEAT).move_to(P3(4.0, -2.3)))
        self.play(VGroup(f, fb).animate.scale(0.82).move_to(P3(EQX, 2.05)),
                  VGroup(u, ub).animate.scale(0.82).move_to(P3(EQX, 0.95)), run_time=T_MOVE)
        bx = self.restart(ap.tc, r"\text{repetindo a carga desde }t=0", x=EQX, y=-3.25)
        self.play(FadeOut(bx), self.oBars.animate.set_value(1), FadeIn(lb), run_time=T_FADE)
        self.play(ap.tc.animate.set_value(5.0), run_time=T_RUN * 1.3, rate_func=linear)
        self.bars, self.E = bars, VGroup(f, fb, u, ub, lb)
        self.wait(T_HOLD)

    # ═══ C13 — onde está a energia? ═════════════════════════════════════════════════════════════════════════
    def c13(self):
        ap, L = self.ap, self.L
        self.sec(13, "onde_esta_energia")
        f, fb, u, ub, lb = self.E
        self.play(*self.H("Onde está essa energia?"), FadeOut(VGroup(f, fb, lb)), self.oBars.animate.set_value(0),
                  *self.lay("soloc"), ap.oCirc.animate.set_value(0), ap.oEL.animate.set_value(0),
                  *self.hide(L["EL"], L["L"], L["B"]), ap.tc.animate.set_value(6.0), VGroup(u, ub).animate.scale(1 / 0.82)
                  .move_to(P3(0, -1.35)), run_time=T_MOVE)
        self.remove(self.bars)
        q = fitw(txt("Onde está essa energia?", 44, CYAN), 12.0).move_to(P3(0, -2.55))
        self.play(FadeIn(q, shift=0.1 * UP), run_time=T_EQ)
        self.E = VGroup(u, ub, q)
        self.wait(T_HOLD)

    # ═══ C14 — densidade de energia ═════════════════════════════════════════════════════════════════════════
    def c14(self):
        ap, L = self.ap, self.L
        self.sec(14, "densidade_energia")
        u, ub, q = self.E
        self.play(*self.H("Densidade de energia magnética"), FadeOut(q), FadeOut(ub), *self.lay("solo"),
                  u.animate.move_to(P3(EQX, 0.8)), run_time=T_MOVE)
        g1 = M(r"\mathbf B", "=", r"\mu_0 n", "I", size=M_M).move_to(P3(EQX - 1.7, 2.05))
        g2 = M("L", "=", r"\mu_0 n^2", r"A\ell", size=M_M).move_to(P3(EQX + 1.6, 2.05))
        self.play(FadeIn(g1), FadeIn(g2), run_time=T_EQ)
        self.play(ap.oVol.animate.set_value(1), *self.show(L["A"], L["ell"]), *self.hide(L["L"], L["B"]),
                  run_time=T_EQ)
        self.wait(T_READ)
        s1 = M("U_B", "=", r"\tfrac12", r"\mu_0 n^2", r"A\ell", "I^2", size=M_XL).move_to(P3(EQX, 0.8))
        self.morph(u, s1, pairs=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 5)])
        self.wait(T_BEAT)
        s2 = M("U_B", "=", r"\frac{(\mu_0 n I)^2}{2\mu_0}", r"A\ell", size=M_XL).move_to(P3(EQX, 0.8))
        self.morph(s1, s2, pairs=[(0, 0), (1, 1), ((2, 3, 5), 2), (4, 3)])
        self.wait(T_BEAT)
        s3 = M("U_B", "=", r"\frac{B^2}{2\mu_0}", r"A\ell", size=M_XL, col={2: MAGENTA}).move_to(P3(EQX, 0.8))
        self.morph(s2, s3, pairs=[(0, 0), (1, 1), (2, 2), (3, 3)])
        self.wait(T_READ)
        vl = M("V", "=", r"A\ell", size=M_M).move_to(self.Wl("solo", XC - KX, YT - A_R - 1.2))
        self.play(*self.H("Aℓ é o volume dentro do solenoide"), TransformFromCopy(s3[3], vl[2]), FadeIn(vl[0]),
                  FadeIn(vl[1]), ap.oVol.animate.set_value(1.4), run_time=T_MORPH)
        self.remove(*vl.submobjects)
        self.add(vl)
        self.wait(T_READ)
        s4 = M("u_B", "=", r"\frac{U_B}{A\ell}", "=", r"\frac{B^2}{2\mu_0}", size=M_XL, col={2: MAGENTA, 4: MAGENTA}) \
            .move_to(P3(EQX, -1.05))
        self.play(FadeIn(s4[0]), FadeIn(s4[1]), FadeIn(s4[2]), FadeIn(s4[3]), TransformFromCopy(s3[2], s4[4]),
                  run_time=T_MORPH)
        self.remove(*s4.submobjects)
        self.add(s4)
        self.wait(T_READ)
        fin = M("u_B", "=", r"\frac{B^2}{2\mu_0}", size=64, col={2: MAGENTA}).move_to(P3(EQX, 0.25))
        self.play(*self.H("A energia mora no campo"), FadeOut(s3), FadeOut(s4[2]), FadeOut(s4[3]), ReplacementTransform(s4[0], fin[0]),
                  ReplacementTransform(s4[1], fin[1]), ReplacementTransform(s4[4], fin[2]), run_time=T_MORPH)
        self.remove(s4, *fin.submobjects)
        self.add(fin)
        fb = boxed(fin, color=MAGENTA, buff=0.22)
        un = MathTex(r"\left[\frac{B^2}{2\mu_0}\right]=\frac{\mathrm T^2}{\mathrm{T\,m/A}}=\frac{\mathrm J}{\mathrm m^3}",
                     font_size=30, color=DIM).move_to(P3(EQX, -1.55))
        self.play(Create(fb), FadeIn(un), run_time=T_EQ)
        self.E = VGroup(g1, g2, vl, fin, fb, un)
        self.wait(T_HOLD)

    # ═══ C15 — generalização ════════════════════════════════════════════════════════════════════════════════
    def cells(self):
        """|B|² de um solenoide finito (cilindro uniformemente magnetizado: cargas ±σ nas tampas), em células."""
        xs = np.arange(XS0 - 1.6, XS1 + 1.61, 0.3)
        ys = np.arange(YT - 1.5, YT + 1.51, 0.3)
        rr, pp = np.meshgrid(np.linspace(0.04, A_R, 9), np.linspace(0, 2 * PI, 28, endpoint=False))
        dA = (A_R / 9) * (2 * PI / 28) * rr.ravel()
        qy, qz = (rr * np.cos(pp)).ravel(), (rr * np.sin(pp)).ravel()

        def Hfield(x, y):
            h = np.zeros(2)
            for xe, sg in ((HX1, 1.0), (HX0, -1.0)):
                d = np.stack([x - xe + 0 * qy, (y - YT) - qy, -qz], 1)
                r3 = np.linalg.norm(d, axis=1) ** 3 + 1e-9
                h += sg * np.sum((d[:, :2].T * dA / r3), axis=1) / (4 * PI)
            return h
        b0 = Hfield(XC - KX, YT) + np.array([1.0, 0.0])
        vals = []
        for x in xs:
            for y in ys:
                h = Hfield(x, y)
                inside = HX0 < x < HX1 and abs(y - YT) < A_R
                b = h + (np.array([1.0, 0.0]) if inside else 0)
                vals.append((x, y, float(np.dot(b, b) / np.dot(b0, b0))))
        g = VGroup()
        s = LAYOUTS["cells"][0]
        for x, y, v in vals:
            if v < 0.004:
                continue
            g.add(Square(0.27 * s).move_to(self.Wl("cells", x, y)).set_fill(MAGENTA, min(0.8, 0.8 * v ** 0.75))
                  .set_stroke(width=0))
        return g.set_z_index(0)

    def c15(self):
        ap, L = self.ap, self.L
        self.sec(15, "generalizacao")
        g1, g2, vl, fin, fb, un = self.E
        self.play(*self.H("Vale para qualquer campo"), FadeOut(VGroup(g1, g2, vl, un)), *self.lay("cells"),
                  ap.oVol.animate.set_value(0), *self.hide(L["A"], L["ell"]), VGroup(fin, fb).animate.move_to(P3(EQX, 1.7)),
                  run_time=T_MOVE)
        cg = self.cells()
        self.play(LaggedStart(*[FadeIn(c) for c in cg], lag_ratio=0.004), ap.oB.animate.set_value(0.5),
                  run_time=2.5)
        cn = txt("campo real: não uniforme, vaza pelas pontas", T_CAP, DIM).move_to(self.Wl("cells", XC - KX, YT - 1.85))
        self.play(FadeIn(cn), run_time=T_FADE)
        self.wait(T_READ)
        pk = self.Wl("cells", HX1 + 0.45, YT + 0.6)
        dt_ = Square(0.27 * LAYOUTS["cells"][0]).move_to(pk).set_stroke(WHITE, 3).set_fill(opacity=0).set_z_index(8)
        dl = MathTex(r"d\tau", font_size=30).next_to(dt_, UR, buff=0.06).set_z_index(8)
        self.play(Create(dt_), FadeIn(dl), run_time=T_EQ)
        d1 = M(r"dU_B", "=", r"\frac{B^2}{2\mu_0}", r"d\tau", size=M_L, col={0: MAGENTA, 2: MAGENTA}).move_to(P3(EQX, -0.05))
        self.play(FadeIn(d1), run_time=T_EQ)
        self.wait(T_READ)
        d2 = M("U_B", "=", r"\frac{1}{2\mu_0}", r"\int", r"B^2", r"d\tau", size=60, col={4: MAGENTA}).move_to(P3(EQX, -1.75))
        self.play(LaggedStart(*[c.animate.set_stroke(WHITE, 1.2, 0.6) for c in cg], lag_ratio=0.003), run_time=2.0)
        self.play(TransformFromCopy(d1, d2), run_time=T_MORPH)
        self.remove(*d2.submobjects)
        self.add(d2)
        b2 = boxed(d2, color=MAGENTA, buff=0.22)
        self.play(Create(b2), cg.animate.set_stroke(width=0), run_time=T_EQ)
        self.E = VGroup(fin, fb, d1, d2, b2, cn, dt_, dl, cg)
        self.wait(T_HOLD)

    # ═══ C16 — comutação para descarga ══════════════════════════════════════════════════════════════════════
    def c16(self):
        ap, L = self.ap, self.L
        self.sec(16, "comutacao_descarga")
        self.play(*self.H("Agora: tirar a bateria sem abrir o circuito"), *self.clrE(), *self.lay("left"),
                  ap.oCirc.animate.set_value(1), ap.oB.animate.set_value(1), *self.show(L["L"], L["B"], L["I"], L["E0"],
                                                                                         L["R"]),
                  run_time=T_MOVE)
        i0 = M("I(0)", "=", "I_0", size=M_L).move_to(P3(EQX, 2.05))
        u0 = M("U_{B,0}", "=", r"\tfrac12", "L", "I_0^2", size=M_L).move_to(P3(EQX, 0.95))
        ub = boxed(u0, color=MAGENTA)
        self.play(FadeIn(i0), run_time=T_EQ)
        self.play(FadeIn(u0), Create(ub), run_time=T_EQ)
        self.wait(T_READ)
        n1 = txt("abrir a chave exigiria I → 0 de repente", T_CAP, DIM).move_to(P3(EQX, -0.35))
        n2 = txt("um caminho alternativo: só o resistor", T_CAP, WHITE).move_to(P3(EQX, -0.85))
        self.play(FadeIn(n1), run_time=T_FADE)
        self.wait(T_BEAT)
        self.play(FadeIn(n2), ap.oByp.animate.set_value(1), run_time=T_EQ)
        self.wait(T_BEAT)
        # comutação a → b: a corrente é contínua (td = 0 ⇔ I = I₀)
        self.play(ap.sw.animate.set_value(SW_B), ap.oDots.animate.set_value(0.4), run_time=T_SW)
        ap.mode = "discharge"
        ap.td.set_value(0)
        self.play(ap.oDots.animate.set_value(1), ap.oBat.animate.set_value(0.18), run_time=T_EQ)
        n3 = txt("o caminho continua fechado pelo resistor", T_CAP, CYAN).move_to(P3(EQX, -1.55))
        self.play(FadeIn(n3), run_time=T_FADE)
        self.E = VGroup(i0, u0, ub, n1, n2, n3)
        self.wait(T_READ)

    # ═══ C17 — o indutor sustenta a corrente ════════════════════════════════════════════════════════════════
    def c17(self):
        ap, L = self.ap, self.L
        self.sec(17, "indutor_sustenta")
        i0, u0, ub, n1, n2, n3 = self.E
        self.play(*self.H("O indutor sustenta a corrente"), FadeOut(VGroup(i0, n1, n2, n3)),
                  VGroup(u0, ub).animate.scale(0.75).move_to(P3(EQX + 1.9, 2.35)), run_time=T_MOVE)
        e1 = M(r"L\frac{dI}{dt}", "+", "R", "I", "=", "0", size=M_L, col={0: CYAN}).move_to(P3(EQX - 1.0, 1.35))
        self.play(FadeIn(e1), run_time=T_EQ)
        self.wait(T_BEAT)
        e2 = M("I(t)", "=", "I_0", r"e^{-t/\tau}", size=M_L).move_to(P3(EQX - 1.0, 1.35))
        self.morph(e1, e2, pairs=[(4, 1)])
        b2 = boxed(e2)
        self.play(Create(b2), run_time=T_FADE)
        g = self.g = Graf(self, center=(EQX, -1.0), h=2.4, one="I_0", ylab="I", ycol=IC)
        self.play(*g.show(), ap.oEL.animate.set_value(1), *self.show(L["EL"]), run_time=T_EQ)
        g.curve(lambda x: math.exp(-x), ap.td, BLUE, 5)
        g.marker(lambda x: math.exp(-x), ap.td, BLUE)
        nn = fitw(txt("mesmo sentido: a fem do indutor agora empurra a corrente", T_CAP, CYAN), 6.4).move_to(P3(EQX, 0.45))
        self.play(FadeIn(nn), ap.td.animate.set_value(0.5), run_time=2.0, rate_func=linear)
        self.play(ap.td.animate.set_value(5.0), run_time=T_RUN, rate_func=linear)
        self.E = VGroup(u0, ub, e2, b2, nn)
        self.wait(T_HOLD)

    # ═══ C18 — campo vira calor ═════════════════════════════════════════════════════════════════════════════
    def c18(self):
        ap, L = self.ap, self.L
        self.sec(18, "campo_vira_calor")
        u0, ub, e2, b2, nn = self.E
        g = self.g
        self.play(*self.H("O campo vira calor"), FadeOut(VGroup(e2, b2, nn)), *g.hide(), run_time=T_FADE)
        g.drop()
        gU = Graf(self, center=(EQX, 0.5), h=1.35, one="U_{B,0}", tlab=False)
        gP = Graf(self, center=(EQX, -1.95), h=1.35, one=r"RI_0^2")
        eU = M("U_B(t)", "=", r"\tfrac12 L I_0^2", r"e^{-2t/\tau}", size=M_M).move_to(P3(EQX, 1.65))
        eP = M("P_R(t)", "=", r"R I_0^2", r"e^{-2t/\tau}", size=M_M).move_to(P3(EQX, -0.75))
        self.play(*gU.show(), *gP.show(), FadeIn(eU), FadeIn(eP), FadeOut(VGroup(u0, ub)), run_time=T_EQ)
        for gg, col in ((gU, MAGENTA), (gP, HEAT)):
            gg.curve(lambda x: math.exp(-2 * x), ap.td, col, 5)
            gg.marker(lambda x: math.exp(-2 * x), ap.td, col)
        bx = self.restart(ap.td, r"\text{repetindo a descarga desde }t=0", y=-3.35)
        self.play(FadeOut(bx), ap.td.animate.set_value(0.3), run_time=1.0, rate_func=linear)
        self.play(ap.td.animate.set_value(5.0), run_time=T_RUN * 1.2, rate_func=linear)
        ck = M("P_R", "=", r"-\frac{dU_B}{dt}", size=M_M, col={2: MAGENTA}).move_to(P3(0.9, 2.15))
        self.play(FadeIn(ck), run_time=T_EQ)
        self.gU, self.gP, self.E = gU, gP, VGroup(eU, eP, ck)
        self.wait(T_HOLD)

    # ═══ C19 — a conservação fecha ══════════════════════════════════════════════════════════════════════════
    def c19(self):
        ap, L = self.ap, self.L
        self.sec(19, "conservacao_fecha")
        gU, gP = self.gU, self.gP
        self.play(*self.H("A conservação fecha"), *self.clrE(), *gU.hide(), *gP.hide(), run_time=T_FADE)
        gU.drop()
        gP.drop()
        y0 = 0.6
        e1 = M(r"E_{\rm calor}", "=", r"\int_0^\infty", "I^2R", r"\,dt", size=M_XL).move_to(P3(EQX, y0))
        self.play(FadeIn(e1), run_time=T_EQ)
        self.wait(T_READ)
        e2 = M(r"E_{\rm calor}", "=", r"\int_0^\infty", r"R I_0^2", r"e^{-2t/\tau}", r"\,dt", size=M_XL).move_to(P3(EQX, y0))
        self.morph(e1, e2, pairs=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 5)])
        self.wait(T_BEAT)
        e3 = M(r"E_{\rm calor}", "=", "R", r"I_0^2", r"\frac{\tau}{2}", size=M_XL).move_to(P3(EQX, y0))
        self.morph(e2, e3, pairs=[(0, 0), (1, 1), ((2, 4, 5), 4)])
        self.wait(T_BEAT)
        tl = M(r"\tau", "=", r"\frac{L}{R}", size=M_M).move_to(P3(EQX, 2.1))
        self.play(FadeIn(tl), run_time=T_EQ)
        e4 = M(r"E_{\rm calor}", "=", "R", r"I_0^2", r"\frac{L}{2R}", size=M_XL).move_to(P3(EQX, y0))
        self.morph(e3, e4, pairs=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])
        # cancela R: o R da frente e o R do denominador
        den = sorted(e4[4], key=lambda m: (m.get_center()[1], -m.get_center()[0]))[0]

        def strike(m):
            return Line(m.get_corner(DOWN + LEFT) + P3(-0.05, -0.05), m.get_corner(UP + RIGHT) + P3(0.05, 0.05),
                        color=HEAT, stroke_width=5).set_z_index(30)
        s1, s2 = strike(e4[2]), strike(den)
        self.play(Create(s1), Create(s2), run_time=T_EQ)
        self.wait(T_BEAT)
        e5 = M(r"E_{\rm calor}", "=", r"\tfrac12", "L", r"I_0^2", size=M_XL).move_to(P3(EQX, y0))
        self.play(FadeOut(s1), FadeOut(s2), run_time=0.4)
        self.morph(e4, e5, pairs=[(0, 0), (1, 1), (3, 4), (4, 3)])
        e6 = M(r"E_{\rm calor}", "=", r"\tfrac12 L I_0^2", "=", "U_{B,0}", size=60).move_to(P3(EQX, y0))
        self.morph(e5, e6, pairs=[(0, 0), (1, 1), ((2, 3, 4), 2)])
        b6 = boxed(e6, buff=0.22)
        self.play(Create(b6), run_time=T_EQ)
        cR = txt("R cancela: a resistência só decide o ritmo", T_CAP, DIM).move_to(P3(EQX, -0.45))
        self.play(FadeIn(cR), run_time=T_FADE)
        self.wait(T_HOLD)
        # Q_R(t) e U_B(t): uma cai, a outra sobe, a soma fica
        self.play(FadeOut(tl), FadeOut(cR), VGroup(e6, b6).animate.scale(0.75).move_to(P3(EQX, 2.1)), run_time=T_MOVE)
        q1 = M("Q_R(t)", "=", "U_{B,0}", r"\left(1-e^{-2t/\tau}\right)", size=M_M).move_to(P3(EQX, 1.15))
        q2 = M("U_B(t)", "+", "Q_R(t)", "=", "U_{B,0}", size=M_L).move_to(P3(EQX, 0.3))
        g = self.g = Graf(self, center=(EQX, -1.75), h=2.0, one="U_{B,0}")
        self.play(FadeIn(q1), *g.show(), run_time=T_EQ)
        g.curve(lambda x: math.exp(-2 * x), ap.td, MAGENTA, 5)
        g.curve(lambda x: 1 - math.exp(-2 * x), ap.td, HEAT, 5)
        g.curve(lambda x: 1.0, ap.td, WHITE, 3)
        g.marker(lambda x: math.exp(-2 * x), ap.td, MAGENTA)
        g.marker(lambda x: 1 - math.exp(-2 * x), ap.td, HEAT)
        bx = self.restart(ap.td, r"\text{repetindo a descarga desde }t=0", y=-3.4)
        self.play(FadeOut(bx), FadeIn(q2), ap.td.animate.set_value(0.3), run_time=T_EQ, rate_func=linear)
        self.play(ap.td.animate.set_value(5.0), run_time=T_RUN * 1.2, rate_func=linear)
        b2 = boxed(q2)
        self.play(Create(b2), run_time=T_EQ)
        self.E = VGroup(e6, b6, q1, q2, b2)
        self.wait(T_HOLD)

    # ═══ C20 — síntese e Maxwell ════════════════════════════════════════════════════════════════════════════
    def c20(self):
        ap, L = self.ap, self.L
        self.sec(20, "sintese_maxwell")
        g = self.g
        self.play(*self.H("Síntese"), *self.clrE(), *g.hide(), ap.oAll.animate.set_value(0.14), run_time=T_MOVE)
        g.drop()
        items = [(M(r"\mathcal E_L", "=", "-L", r"\frac{dI}{dt}", size=M_L), "o indutor reage à mudança", CYAN),
                 (M("U_B", "=", r"\tfrac12", "L", "I^2", size=M_L), "energia armazenada", MAGENTA),
                 (M("u_B", "=", r"\frac{B^2}{2\mu_0}", size=M_L, col={2: MAGENTA}), "a energia está no campo", MAGENTA),
                 (M(r"E_{\rm calor}", "=", "U_{B,0}", size=M_L), "toda ela vira calor", HEAT)]
        pos = [P3(-3.4, 1.35), P3(3.4, 1.35), P3(-3.4, -1.15), P3(3.4, -1.15)]
        grid = VGroup()
        for (m, c, col), p in zip(items, pos):
            m.move_to(p)
            b = boxed(m, color=col, buff=0.22)
            t = txt(c, T_CAP, DIM).next_to(b, UP, buff=0.18)
            self.play(FadeIn(t), FadeIn(m), Create(b), run_time=T_EQ)
            self.wait(T_BEAT)
            grid.add(m, b, t)
        self.wait(T_HOLD)
        # o mesmo circuito, com um capacitor no lugar do solenoide
        self.play(*self.H("E se, no lugar do solenoide, houver um capacitor?"), FadeOut(grid), run_time=T_MOVE)
        ap.oDots.set_value(0)
        self.play(ap.oAll.animate.set_value(1), ap.oCap.animate.set_value(1), ap.oByp.animate.set_value(0),
                  ap.oBat.animate.set_value(1), ap.oEL.animate.set_value(0), ap.sw.animate.set_value(SW_OPEN),
                  *self.hide(L["L"], L["B"], L["EL"]), *self.show(L["C"]), run_time=T_MOVE)
        ap.mode = "cap"
        ap.tc.set_value(0)
        self.play(ap.sw.animate.set_value(SW_A), run_time=T_SW)
        self.play(ap.oDots.animate.set_value(1), ap.tc.animate.set_value(0.5), run_time=2.5, rate_func=linear)
        ap.auto_tc = 0.05                                    # a carga continua devagar até o fim (tempo não congela)
        n1 = txt("a corrente chega às placas…", T_CAP, IC).move_to(P3(EQX, 2.1))
        n2 = txt("…mas não atravessa o espaço entre elas", T_CAP, WHITE).move_to(P3(EQX, 1.6))
        self.play(FadeIn(n1), run_time=T_FADE)
        self.wait(T_BEAT)
        self.play(FadeIn(n2), *self.show(L["I0gap"]), run_time=T_FADE)
        self.wait(T_READ)
        self.play(*self.H("A lei de Ampère em volta do fio"), FadeOut(n1), FadeOut(n2), *self.hide(L["I0gap"]),
                  ap.oAmp.animate.set_value(1), run_time=T_EQ)
        a1 = M(r"\oint", r"\mathbf B\cdot d\boldsymbol\ell", "=", r"\mu_0", r"I_{\rm enc}", size=M_L,
               col={1: MAGENTA, 4: IC}).move_to(P3(EQX, 1.85))
        self.play(FadeIn(a1), run_time=T_EQ)
        self.wait(T_READ)
        s1 = M("S_1:", r"I_{\rm enc}", "=", "I", size=M_M, col={1: IC}).move_to(P3(EQX - 1.6, 0.75))
        s2 = M("S_2:", r"I_{\rm enc}", "=", "0", size=M_M, col={1: IC}).move_to(P3(EQX + 1.6, 0.75))
        self.play(ap.oS1.animate.set_value(1), *self.show(L["S1"]), FadeIn(s1), run_time=T_EQ)
        self.wait(T_BEAT)
        self.play(ap.oS2.animate.set_value(1), *self.show(L["S2"]), FadeIn(s2), run_time=T_EQ)
        self.wait(T_BEAT)
        qm = MathTex("?", font_size=80, color=CYAN).move_to(P3(EQX, 0.75))
        self.play(FadeIn(qm, scale=0.7), run_time=T_EQ)
        self.wait(T_READ)
        q = VGroup(txt("Como o campo magnético sabe", 34, WHITE), txt("que o circuito continua?", 34, WHITE)) \
            .arrange(DOWN, buff=0.18).scale(0.9).move_to(P3(EQX + 0.3, -0.75))
        self.play(*self.H("Como o campo magnético sabe que o circuito continua?"), FadeIn(q, shift=0.1 * UP),
                  run_time=T_EQ)
        self.wait(T_HOLD)
        nx = txt("Próximo: Maxwell", 36, CYAN).move_to(P3(EQX, -2.05))
        self.play(FadeIn(nx, shift=0.1 * UP), run_time=T_EQ)
        cta = txt("Inscreva-se para acompanhar a série · Parallax Lab", 22, DIM, 0.8).move_to(P3(0, -3.45))
        self.play(FadeIn(cta), run_time=T_FADE)
        self.wait(T_HOLD * 1.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.body], ap.oAll.animate.set_value(0),
                  run_time=T_MOVE)
        ap.auto_tc = 0.0
        self.wait(0.5)
