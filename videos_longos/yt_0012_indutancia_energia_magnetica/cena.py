"""yt_0012 — Por que a corrente resiste a mudar? (indutância e energia magnética). V3.

Preview visual silencioso, 960×540 / 15 fps. Storyboard C01–C20 (ver ficha.md). V1 e V2 em cena_v1_backup.py / cena_v2_backup.py.

V3 segue a gramática dos longos de magnetostática (yt_0005/yt_0006) com cópias LOCAIS de base.py e kit.py:
  · título de seção no topo, legenda inferior com matemática embutida, equações em cartões (slots H e A);
  · equações por tokens (E) e TransformByGlyphMap (gmap/show): cada termo é transportado pelo nome, o que é novo voa do
    desenho (src) ou entra por fade; o que sai termina antes de o que entra começar;
  · índice de variáveis (símbolo colorido + descrição em minúsculas) num cartão próprio;
  · corrente como traços verdes que correm pelo fio (como o flow do yt_0006), com velocidade ∝ I; nas espiras, setinhas;
  · condutores em aço com brilho fino (tube); solenoide em anéis com frente e fundo (como o vid_0009), sem corpo de vidro.

Um aparato só (bateria + chave + solenoide + resistor), desenhado a partir de trackers:
  tc = t/τ da carga     → I = 1 − e^{−tc}, dI/dt = e^{−tc}, B = I, ℰ_L = −e^{−tc}, U_B = I², P_J = I², P_L = I·dI/dt
  td = t/τ da descarga  → I = e^{−td}, dI/dt = −e^{−td}, ℰ_L = +e^{−td}, U_B = P_R = e^{−2td}, Q_R = 1 − e^{−2td}
  sp (só C06)           → corrente imposta (sobe, constante, desce)
Cores: corrente verde · fem e campo elétrico induzido ciano · B, Λ, U_B magenta · R e calor laranja · geometria e tempo violeta.
SEG=<seção>[,<seção>] renderiza só essas seções (as outras são puladas, o estado é construído).
"""
import json
import math
from pathlib import Path

import numpy as np
from manim import (
    Axes, Brace, DashedVMobject, ManimColor, Rectangle, RoundedRectangle, Square, interpolate_color, PI, DL, DR,
)

from base import *  # noqa: F401,F403
from kit import HEAT, TOKCOL, GEO, defn  # noqa: E402

LOGO_H = ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"


def box(*_a, **_k):
    """Padrão dos longos: o cartão já destaca; sem caixa branca extra."""
    return VGroup()

# ── tempos provisórios (a voz será escrita depois; retimar aqui) ───────────────────────────────────────────────
T_IN, T_EQ, T_MOVE, T_READ, T_HOLD, T_RUN, T_SW = 0.8, 2.0, 1.8, 3.0, 4.5, 9.0, 0.9

# ── geometria local do aparato (tela = C + s·(p − F)); z para fora da tela ─────────────────────────────────────
XL, XA, XB = -4.2, -3.4, -2.6        # bateria, contato a, pivô da chave / ramo de desvio
XS0, XS1, XR = -1.3, 1.9, 3.6        # solenoide (início, fim), resistor
YT, YB = 1.3, -1.3                   # fio de cima (eixo do solenoide), fio de baixo
A_R, NT = 0.5, 10                    # raio do solenoide, anéis desenhados
XC = 0.5 * (XS0 + XS1)
ANG0 = -0.5                          # vista lateral (giro em torno do eixo vertical); −π/2 = vista axial (B ⊙)
ELEV = 0.15                          # leve elevação da câmera
LBL = 0.8                            # lâmina da chave
SW_OPEN, SW_A, SW_B = 145.0, 180.0, 270.0
XM0, XM1, A2, NT2 = -0.1, 0.7, 0.82, 3            # bobina 2 coaxial
YMET, MR = YT + 1.75, 0.3            # medidor / fonte da bobina 2
XP0, XP1, PH = XC - 0.24, XC + 0.24, 0.55           # capacitor (C20)
XAMP, RAMP = -0.75, 0.78             # anel amperiano (C20)
XIA = 0.9                            # seta de corrente no fio de baixo
SPC, DASH, VFLOW = 0.62, 0.16, 0.55  # espaçamento e meio-comprimento dos traços; velocidade (I = 1)

VIEW = {                             # (s, cx, cy, fx, fy)
    "left": (0.83, -3.6, -0.05, -0.3, 0.2),
    "mut": (0.78, -3.65, -0.6, -0.3, 0.2),
    "solo": (1.45, -3.6, 0.15, XC, YT),
    "soloc": (1.6, -0.6, 1.15, XC, YT),
    "cells": (1.15, -3.5, 0.0, XC, YT),
    "axial": (1.9, -3.6, -0.1, XC, YT),
}
GPOS = (3.95, -1.45)                 # gráfico na região do slot A


def probe(s):
    """C06: corrente imposta (sobe, constante, desce). (I, dI/dt normalizado, máx. 1)."""
    if s <= 0:
        return 0.0, 0.0
    if s < 1:
        return 0.5 * (1 - math.cos(PI * s)), math.sin(PI * s)
    if s < 2:
        return 1.0, 0.0
    if s < 3:
        return 0.5 * (1 + math.cos(PI * (s - 2))), -math.sin(PI * (s - 2))
    return 0.0, 0.0


def hull(pts):
    p = sorted(set(map(tuple, np.round(np.asarray(pts)[:, :2], 5))))
    if len(p) < 3:
        return np.array(p)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for q in p:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(p):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    return np.array(lo[:-1] + up[:-1])


def multi(paths):
    m = VMobject()
    for p in paths:
        if len(p) >= 2:
            m.start_new_path(p[0])
            m.add_points_as_corners(p[1:])
    return m


def redraw(func):
    """Redesenha trocando os submobjetos (o become() do always_redraw engordaria o objeto quadro a quadro)."""
    m = VGroup()

    def upd(x):
        x.submobjects = [func()]
    m.add_updater(upd)
    upd(m)
    return m


def ring3(x, r, n=48, yc=YT):
    th = np.linspace(0, 2 * PI, n + 1)
    return np.stack([np.full_like(th, x), yc + r * np.cos(th), r * np.sin(th)], 1)


class Ap:
    """Estado do aparato (trackers) e o desenho correspondente."""
    OPS0 = ("oAll", "oFlow", "oEL", "oEB", "oIA", "oSec", "oSrc", "oByp", "oVol", "oAe", "oCap", "oHL", "oAmp", "oS1",
            "oS2", "oFlux", "oGauge", "oGb", "oGr", "oGs", "oEr", "oSweep", "oCoilI")
    OPS1 = ("oCirc", "oSol", "oBat", "oB", "oHeat")

    def __init__(self):
        T = ValueTracker
        s, cx, cy, fx, fy = VIEW["left"]
        self.s, self.cx, self.cy, self.fx, self.fy = T(s), T(cx), T(cy), T(fx), T(fy)
        for n in self.OPS0:
            setattr(self, n, T(0.0))
        for n in self.OPS1:
            setattr(self, n, T(1.0))
        self.ang, self.sw = T(ANG0), T(SW_OPEN)
        self.tc, self.td, self.sp = T(0.0), T(0.0), T(0.0)
        self.mode, self.role = "charge", 1
        self.xk = [XS0 + (k + 0.5) * (XS1 - XS0) / NT for k in range(NT)]
        self.HA = self.proj(XS0, YT, 0.0, ANG0)[:2]
        self.HB = self.proj(XS1, YT, 0.0, ANG0)[:2]

    def trackers(self):
        return [getattr(self, n) for n in ("s", "cx", "cy", "fx", "fy", *self.OPS0, *self.OPS1, "ang", "sw", "tc", "td", "sp")]

    def key(self):
        return (self.mode, self.role, *[round(t.get_value(), 5) for t in self.trackers()])

    def proj(self, x, y, z, ang=None):
        a = self.ang.get_value() if ang is None else ang
        ca, sa = math.cos(a), math.sin(a)
        return (XC + (x - XC) * ca + z * sa, y + ELEV * z * ca, -(x - XC) * sa + z * ca)

    def projv(self, P, ang=None):
        a = self.ang.get_value() if ang is None else ang
        ca, sa = math.cos(a), math.sin(a)
        return (XC + (P[:, 0] - XC) * ca + P[:, 2] * sa, P[:, 1] + ELEV * P[:, 2] * ca, -(P[:, 0] - XC) * sa + P[:, 2] * ca)

    def st(self):
        m = self.mode
        if m == "charge":
            e = math.exp(-self.tc.get_value())
            I, dI, q = 1 - e, e, 0.0
            if self.role == 1 and self.tc.get_value() < 1e-6 and abs(self.sw.get_value() - SW_A) > 2:
                dI = 0.0
        elif m == "discharge":
            e = math.exp(-self.td.get_value())
            I, dI, q = e, -e, 0.0
        elif m == "probe":
            (I, dI), q = probe(self.sp.get_value()), 0.0
        else:
            e = math.exp(-self.tc.get_value())
            I, dI, q = e, -e, 1 - e
        return {"I": I, "dI": dI, "B": I, "EL": -dI, "PR": I * I, "PL": I * dI, "q": q}

    def W(self, x, y=0.0):
        s = self.s.get_value()
        return np.array([self.cx.get_value() + s * (x - self.fx.get_value()), self.cy.get_value() + s * (y - self.fy.get_value()), 0.0])

    def Wv(self, a):
        a = np.asarray(a, float)
        s = self.s.get_value()
        out = np.zeros((len(a), 3))
        out[:, 0] = self.cx.get_value() + s * (a[:, 0] - self.fx.get_value())
        out[:, 1] = self.cy.get_value() + s * (a[:, 1] - self.fy.get_value())
        return out

    def W3(self, x, y, z, ang=None):
        X, Y, _ = self.proj(x, y, z, ang)
        return self.W(X, Y)

    def flat(self, P, ang=None):
        X, Y, _ = self.projv(P, ang)
        return self.Wv(np.stack([X, Y], 1))

    def lat(self):
        return max(0.0, 1 - abs(self.ang.get_value() - ANG0) / 0.3)

    # ── condutor: aço com brilho fino (tube do yt_0006) ──────────────────────────────────────────────────────
    def tube(self, paths, w, op, z=3):
        if op < 0.01:
            return VGroup()
        base = multi(paths)
        return VGroup(base.copy().set_stroke(STEEL, w + 3, 0.5 * op), base.copy().set_stroke(STEEL, w, op),
                      base.copy().shift(0.018 * UP).set_stroke(WHITE, 1.4, 0.4 * op)).set_z_index(z)

    def ring(self, x, r, w, op, zf=5, zb=1, uniforme=False):
        """Anel 3D: metade da frente forte, metade de trás apagada (como as espiras do vid_0009).
        uniforme=True: o anel inteiro no mesmo cinza (espiras do solenoide)."""
        P = ring3(x, r, 72)
        X, Y, D = self.projv(P)
        S = self.Wv(np.stack([X, Y], 1))
        if uniforme:
            return self.tube([np.vstack([S, S[:1]])], w, op, zf)
        front, back, cur, sg = [], [], [S[0]], D[0] >= 0
        for k in range(1, len(S)):
            cur.append(S[k])
            if (D[k] >= 0) != sg:
                (front if sg else back).append(np.array(cur))
                cur, sg = [S[k]], D[k] >= 0
        (front if sg else back).append(np.array(cur))
        g = VGroup()
        if back:
            g.add(multi(back).set_stroke(STEEL, w * 0.6, 0.38 * op).set_z_index(zb))
        if front:
            g.add(self.tube(front, w, op, zf))
        return g

    def body(self, x0, x1, r, n=40):
        P = np.vstack([ring3(x0, r, n), ring3(x1, r, n)])
        X, Y, _ = self.projv(P)
        return self.Wv(hull(np.stack([X, Y], 1)))

    def build(self):
        g = VGroup()
        A = self.oAll.get_value()
        if A < 0.01:
            return g
        S = self.st()
        s, W, Wv = self.s.get_value(), self.W, self.Wv
        lw = 2.0 + 1.6 * min(s, 1.8)
        cap = self.oCap.get_value()
        oc = A * self.oCirc.get_value()
        osl = A * self.oSol.get_value() * (1 - cap)
        lat = self.lat()
        oc2, role2 = oc * lat, self.role == 2
        obt = oc2 * self.oBat.get_value()
        Bv, I = S["B"], S["I"]
        ca = abs(math.cos(self.ang.get_value()))

        # campo B dentro do solenoide (magenta, ∝ B): preenchimento suave + linhas ao longo do eixo
        if osl > 0.01:
            ob = osl * self.oB.get_value()
            if ob > 0.01 and Bv > 0.01:
                g.add(Polygon(*self.body(XS0, XS1, 0.92 * A_R)).set_fill(MAG, ob * (0.05 + 0.17 * min(Bv, 1.3)))
                      .set_stroke(width=0).set_z_index(2))
                if ca > 0.3:
                    for yy in (0.5 * A_R, 0.0, -0.5 * A_R):
                        g.add(arrow(self.W3(XS0 + 0.1, YT + yy, 0), self.W3(XS1 - 0.25, YT + yy, 0), MAG, 3, z=3,
                                    tip=0.15 * min(s, 1.5)).set_opacity(ob * min(1.0, Bv) * min(1, (ca - 0.3) / 0.4)))
                obd = ob * max(0.0, 1 - ca / 0.35) * min(1.0, Bv)
                if obd > 0.01:                              # vista axial: B ⊙ saindo da tela
                    c0 = np.array(self.proj(XC, YT, 0)[:2])
                    for i in range(-3, 4):
                        for j in range(-3, 4):
                            p = c0 + np.array([0.15 * i + 0.075 * (j % 2), 0.14 * j])
                            if np.linalg.norm(p - c0) < 0.8 * A_R:
                                q = W(*p)
                                g.add(Circle(radius=0.035 * s).move_to(q).set_stroke(MAG, 2, obd).set_z_index(7))
                                g.add(Dot(q, radius=0.012 * s).set_fill(MAG, obd).set_z_index(7))
            # seção A (tampa da frente) e volume varrido (C14)
            oae = osl * self.oAe.get_value()
            if oae > 0.01:
                g.add(Polygon(*self.flat(ring3(XS1, A_R))).set_fill(VIOLET, 0.45 * oae).set_stroke(VIOLET, 3, oae)
                      .set_z_index(6))
            sw_ = self.oSweep.get_value()
            if sw_ > 0.01:
                xr = XS1 - (XS1 - XS0) * min(1.0, sw_)
                g.add(Polygon(*self.body(xr, XS1, A_R)).set_fill(VIOLET, 0.32 * osl).set_stroke(VIOLET, 2.5, osl)
                      .set_z_index(4))
            ov = osl * self.oVol.get_value()
            if ov > 0.01:                                   # cota de ℓ
                y0 = YT - A_R - 0.45
                p0, p1 = self.W3(XS0, y0, 0), self.W3(XS1, y0, 0)
                g.add(Line(p0, p1).set_stroke(VIOLET, 3, ov).set_z_index(9))
                for p in (p0, p1):
                    g.add(Line(p + 0.1 * DOWN, p + 0.1 * UP).set_stroke(VIOLET, 3, ov).set_z_index(9))
            ohl = osl * self.oHL.get_value() * min(1.0, Bv * 1.5)
            if ohl > 0.01:                                  # cada espira concatena o fluxo (C05)
                for xk in self.xk:
                    g.add(Polygon(*self.flat(ring3(xk, A_R, 36))).set_fill(MAG, 0.14 * ohl).set_stroke(width=0)
                          .set_z_index(2))
            # anéis do solenoide
            for xk in self.xk:
                g.add(self.ring(xk, A_R, lw, osl, uniforme=True))
            # corrente nas espiras: setinhas verdes na frente de cada anel (descem: B em +x)
            oci = osl * self.oCoilI.get_value() * min(1.0, 3 * abs(I)) * (ca > 0.3)
            if oci > 0.01:
                for xk in self.xk:
                    p = self.W3(xk, YT + 0.17, A_R)
                    q = self.W3(xk, YT - 0.17, A_R)
                    g.add(arrow(p, q, GREEN, 4, z=8, tip=0.11 * min(s, 1.5)).set_opacity(oci))
            # E_φ induzido (vista axial): |E| ∝ r dentro, ∝ a²/r fora; dI/dt > 0 ⇒ horário (Lenz)
            oer = osl * self.oEr.get_value()
            if oer > 0.01:
                c0 = W(*self.proj(XC, YT, 0)[:2])
                dI = S["dI"]
                for rr in (0.4, 0.75, 1.3, 1.8):
                    e = (rr if rr < 1 else 1 / rr) * dI
                    m = abs(e)
                    if m < 0.03:
                        continue
                    r = rr * A_R * s
                    g.add(DashedVMobject(Circle(radius=r, arc_center=c0), num_dashes=int(14 + 8 * r), dashed_ratio=0.55)
                          .set_stroke(CYAN, 2.5, oer * min(1.0, 0.2 + m)).set_z_index(8))
                    for k in range(4):
                        th = PI / 4 + k * PI / 2 + 0.3 * rr
                        p = c0 + r * np.array([math.cos(th), math.sin(th), 0])
                        t = np.array([math.sin(th), -math.cos(th), 0]) * (1 if dI > 0 else -1)
                        Lr = (0.12 + 0.28 * m) * s / 1.5
                        g.add(arrow(p - t * Lr / 2, p + t * Lr / 2, CYAN, 4, z=8, tip=0.12 * s / 1.5)
                              .set_opacity(oer * min(1.0, 0.3 + m)))

        # bobina 2 e o fluxo que ela concatena
        osc = A * self.oSec.get_value()
        if osc > 0.01:
            for k in range(NT2):
                g.add(self.ring(XM0 + (k + 0.5) * (XM1 - XM0) / NT2, A2, lw, osc, zf=6, zb=0))
            g.add(self.tube([Wv([(XM0, YT + A2), (XM0, YMET), (XC - MR, YMET)]), Wv([(XM1, YT + A2), (XM1, YMET), (XC + MR, YMET)])],
                            lw * 0.8, osc, 5))
            mc = W(XC, YMET)
            g.add(Circle(radius=MR * s).move_to(mc).set_fill(BACKGROUND_COLOR, osc).set_stroke(WHITE, 2.5, osc).set_z_index(6))
            osr = self.oSrc.get_value()
            if osr < 0.99:
                e2 = 0.0 if role2 else max(-1.0, min(1.0, -S["dI"]))
                ph = math.radians(65 * e2)
                p0 = mc + 0.14 * s * DOWN
                g.add(Line(p0, p0 + 0.36 * s * np.array([math.sin(ph), math.cos(ph), 0])).set_stroke(CYAN, 3, osc * (1 - osr))
                      .set_z_index(7))
            if osr > 0.01:
                xs = np.linspace(-0.18, 0.18, 30)
                g.add(VMobject().set_points_smoothly([mc + s * np.array([x, 0.08 * math.sin(x / 0.18 * 2 * PI), 0]) for x in xs])
                      .set_stroke(WHITE, 3, osc * osr).set_z_index(7))
            ofl = osc * self.oFlux.get_value() * min(1.0, Bv * 1.5)
            if ofl > 0.01:
                xm = 0.5 * (XM0 + XM1)
                g.add(DashedVMobject(Polygon(*self.flat(ring3(xm, A2))), num_dashes=30).set_stroke(WHITE, 2, 0.8 * ofl).set_z_index(6))
                g.add(Polygon(*self.flat(ring3(xm, A_R))).set_fill(MAG, 0.5 * ofl).set_stroke(MAG, 2.5, ofl).set_z_index(6))

        # fios (ligados às pontas do solenoide só na vista lateral)
        bat = [[(XL, YB), (XL, -0.12)], [(XL, 0.12), (XL, YT), (XA, YT)], [(XL, YB), (XB, YB)]]
        main = [[(XB, YT), self.HA], [self.HB, (XR, YT), (XR, 0.65)], [(XR, -0.65), (XR, YB), (XB, YB)]]
        if ca > 0 and osl > 0.01 and lat > 0.01:
            main[0] = [(XB, YT), self.HA]
        g.add(self.tube([Wv(p) for p in bat], lw, obt))
        g.add(self.tube([Wv(p) for p in main], lw, oc2 * (1 - cap) + oc2 * cap))
        if cap > 0.01:
            g.add(self.tube([Wv([self.HA, (XP0, YT)]), Wv([(XP1, YT), self.HB])], lw, oc * cap))
        oby = oc2 * self.oByp.get_value()
        if oby > 0.01:
            g.add(self.tube([Wv([(XB, YT - LBL), (XB, YB)])], lw, oby))
            g.add(Dot(W(XB, YB), radius=0.05 * s).set_fill(STEEL, oby).set_z_index(4))
            g.add(Circle(radius=0.06 * s).move_to(W(XB, YT - LBL)).set_fill(BACKGROUND_COLOR, oby).set_stroke(WHITE, 2, oby)
                  .set_z_index(5))
        # bateria (placa longa = +)
        if obt > 0.01:
            g.add(Line(W(XL - 0.38, 0.12), W(XL + 0.38, 0.12)).set_stroke(WHITE, lw * 1.1, obt).set_z_index(4))
            g.add(Line(W(XL - 0.2, -0.12), W(XL + 0.2, -0.12)).set_stroke(WHITE, lw * 2.6, obt).set_z_index(4))
            pc, aa = W(XL + 0.52, 0.36), 0.07 * s
            g.add(multi([[pc + aa * LEFT, pc + aa * RIGHT], [pc + aa * DOWN, pc + aa * UP]]).set_stroke(WHITE, 2.5, obt).set_z_index(4))
        # medidores de potência (escala ℰ₀ I_∞): fonte = resistor + campo
        og = oc2 * self.oGauge.get_value()
        if og > 0.01 and self.mode == "charge":
            Hg, wg = 1.0, 0.22
            PJ, PL = S["PR"], max(0.0, S["PL"])

            def gauge(x, y0, parts, o):
                gg = VGroup(Rectangle(width=wg * s, height=Hg * s).move_to(W(x, y0 + Hg / 2)).set_fill(opacity=0)
                            .set_stroke(DIM, 1.5, o))
                acc = 0.0
                for v, colr in parts:
                    if v > 0.004:
                        gg.add(Rectangle(width=wg * s, height=Hg * v * s).move_to(W(x, y0 + Hg * (acc + v / 2)))
                               .set_fill(colr, 0.9 * o).set_stroke(width=0))
                    acc += v
                return gg.set_z_index(9)
            if self.oGb.get_value() > 0.01:
                g.add(gauge(XL + 0.85, -1.05, [(PJ, HEAT), (PL, MAG)], og * self.oGb.get_value()))
            if self.oGr.get_value() > 0.01:
                g.add(gauge(XR - 0.85, -1.05, [(PJ, HEAT)], og * self.oGr.get_value()))
            if self.oGs.get_value() > 0.01:
                g.add(gauge(XC + 1.0, -1.05, [(PL, MAG)], og * self.oGs.get_value()))
        # resistor (cor e brilho ∝ P_R) e chave
        if oc2 > 0.01:
            h = min(1.0, S["PR"]) * self.oHeat.get_value() * (0 if role2 or self.mode in ("probe", "cap") else 1)
            if h > 0.03:
                for sc, op in ((2.6, 0.10), (1.9, 0.16), (1.35, 0.26)):
                    g.add(RoundedRectangle(corner_radius=0.12 * s, width=0.45 * s * sc, height=1.3 * s * (0.6 + 0.4 * sc))
                          .set_fill(HEAT, op * h * oc2).set_stroke(width=0).move_to(W(XR, 0)).set_z_index(2))
            zz = [(XR, 0.65)] + [(XR + (0.2 if i % 2 == 0 else -0.2), 0.65 - 1.3 * (i + 0.5) / 7) for i in range(7)] + [(XR, -0.65)]
            col = interpolate_color(ManimColor(STEEL), ManimColor(HEAT), h)
            g.add(VMobject().set_points_as_corners(Wv(zz)).set_stroke(col, lw * 1.05, oc2).set_z_index(4))
            ang = math.radians(self.sw.get_value())
            pv = W(XB, YT)
            g.add(Circle(radius=0.06 * s).move_to(W(XA, YT)).set_fill(BACKGROUND_COLOR, obt).set_stroke(WHITE, 2, obt).set_z_index(5))
            g.add(Line(pv, W(XB + LBL * math.cos(ang), YT + LBL * math.sin(ang))).set_stroke("#DCE4F2", lw * 1.15, oc2).set_z_index(6))
            g.add(Dot(pv, radius=0.07 * s).set_fill("#DCE4F2", oc2).set_z_index(6))

        # capacitor 2.5D (C20)
        ocap = A * cap
        if ocap > 0.01:
            for xp in (XP0, XP1):
                q = [self.proj(xp, YT + u * PH, v * PH, ANG0)[:2] for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
                g.add(Polygon(*Wv(q)).set_fill("#B8C8E8", 0.16 * ocap).set_stroke("#DCE4F2", 2.2, ocap).set_z_index(5))
            nq = int(round(9 * S["q"]))
            aa = 0.055 * s
            for i in range(nq):
                u, v = -0.6 + 0.6 * (i % 3), -0.6 + 0.6 * (i // 3)
                c1 = W(*self.proj(XP0 + 0.03, YT + u * PH, v * PH, ANG0)[:2])
                c2 = W(*self.proj(XP1 - 0.03, YT + u * PH, v * PH, ANG0)[:2])
                g.add(multi([[c1 + aa * LEFT, c1 + aa * RIGHT], [c1 + aa * DOWN, c1 + aa * UP], [c2 + aa * LEFT, c2 + aa * RIGHT]])
                      .set_stroke(GREEN, 2.5, ocap).set_z_index(6))
        # anel amperiano e superfícies (C20)
        oam = A * self.oAmp.get_value()
        if oam > 0.01:
            rg = self.flat(ring3(XAMP, RAMP, 60), ANG0)
            o1, o2 = self.oS1.get_value() * oam, self.oS2.get_value() * oam
            if o1 > 0.01:
                g.add(Polygon(*rg).set_fill(VIOLET, 0.22 * o1).set_stroke(width=0).set_z_index(4))
            if o2 > 0.01:
                xg = 0.5 * (XP0 + XP1)
                P = np.vstack([ring3(XAMP, RAMP, 40), ring3(xg, RAMP, 40)])
                X, Y, _ = self.projv(P, ANG0)
                g.add(Polygon(*Wv(hull(np.stack([X, Y], 1)))).set_fill(CYAN, 0.10 * o2).set_stroke(CYAN, 2, 0.8 * o2).set_z_index(4))
                g.add(DashedVMobject(Polygon(*self.flat(ring3(xg, RAMP, 48), ANG0)), num_dashes=26).set_stroke(CYAN, 2.5, o2)
                      .set_z_index(7))
            g.add(VMobject().set_points_as_corners(rg).set_stroke(WHITE, 3, oam).set_z_index(7))
            ib = min(1.0, abs(I) * 2.5)
            if ib > 0.02:
                for k in (-1.4, -0.3):
                    pu, pd, r = W(k, YT + 0.45), W(k, YT - 0.45), 0.09 * s
                    g.add(Circle(radius=r).move_to(pu).set_stroke(MAG, 2.5, oam * ib).set_z_index(6))
                    g.add(Dot(pu, radius=0.03 * s).set_fill(MAG, oam * ib).set_z_index(6))
                    g.add(Circle(radius=r).move_to(pd).set_stroke(MAG, 2.5, oam * ib).set_z_index(6))
                    g.add(multi([[pd + 0.6 * r * (DL), pd + 0.6 * r * UR], [pd + 0.6 * r * UL, pd + 0.6 * r * DR]])
                          .set_stroke(MAG, 2.5, oam * ib).set_z_index(6))

        # fem autoinduzida ℰ_L (seta = sentido em que empurra a corrente; + na ponta)
        oe = osl * self.oEL.get_value() * lat
        el = S["EL"]
        if oe > 0.01 and abs(el) > 0.02:
            y = YT + A_R + 0.55
            g.add(arrow(W(XC - 0.8 * el, y), W(XC + 0.8 * el, y), CYAN, 6, z=9, tip=0.22 * min(s, 1.4)).set_opacity(oe))
            sg, aa, opm = (1 if el > 0 else -1), 0.08 * s, oe * min(1.0, 3 * abs(el))
            pp, pm = W(XC + sg * 1.85, y), W(XC - sg * 1.85, y)
            g.add(multi([[pp + aa * LEFT, pp + aa * RIGHT], [pp + aa * DOWN, pp + aa * UP], [pm + aa * LEFT, pm + aa * RIGHT]])
                  .set_stroke(CYAN, 3, opm).set_z_index(9))
        oeb = obt * self.oEB.get_value()
        if oeb > 0.01:
            g.add(arrow(W(XL + 0.62, -0.8), W(XL + 0.62, 0.8), CYAN, 6, z=9, tip=0.22 * min(s, 1.4)).set_opacity(oeb))
        oia = oc2 * self.oIA.get_value() * (0 if role2 else 1)
        if oia > 0.01 and abs(I) > 0.02:
            y = YB - 0.32
            g.add(arrow(W(XIA + 0.7 * I, y), W(XIA - 0.7 * I, y), GREEN, 6, z=9, tip=0.2 * min(s, 1.4)).set_opacity(oia))
        return g

    # ── percursos da corrente (local) para os traços verdes ───────────────────────────────────────────────────
    def path(self):
        if self.role == 2:
            return [(XM0, YT + A2), (XM0, YMET), (XC - MR, YMET), (XC + MR, YMET), (XM1, YMET), (XM1, YT + A2), (XM0, YT + A2)]
        if self.mode == "discharge":
            return [(XB, YT), self.HA, self.HB, (XR, YT), (XR, YB), (XB, YB), (XB, YT - LBL), (XB, YT)]
        if self.mode in ("charge", "cap"):
            return [(XB, YT), self.HA, self.HB, (XR, YT), (XR, YB), (XB, YB), (XL, YB), (XL, YT), (XA, YT), (XB, YT)]
        return []

    def hidden(self, x, y):
        """Trechos onde o traço não aparece: dentro do solenoide/capacitor, na bateria, no resistor, no medidor."""
        if self.role == 2:
            return (abs(y - YMET) < 0.05 and abs(x - XC) < MR + 0.05) or (abs(y - (YT + A2)) < 0.05 and XM0 - 0.05 < x < XM1 + 0.05)
        if abs(y - YT) < 0.05 and self.HA[0] - 0.05 < x < self.HB[0] + 0.05:
            return True
        if abs(x - XL) < 0.05 and -0.25 < y < 0.25:
            return True
        if abs(x - XR) < 0.05 and -0.72 < y < 0.72:
            return True
        return False


class Graf:
    """Eixos t × grandeza; curvas, área e marcador lidos de um tracker (unidades de τ)."""

    def __init__(self, sc, center=GPOS, w=5.6, h=2.1, xmax=5.0, ymax=1.15, one=None, ylab=None, ycol=WHITE, ticks=True, tlab=True):
        self.sc, self.op, self.xmax, self.dyn = sc, ValueTracker(0.0), xmax, []
        ax = Axes(x_range=[0, xmax, 1], y_range=[0, ymax, 0.5], x_length=w, y_length=h, tips=False,
                  axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False}).move_to(np.array([*center, 0]))
        self.ax = ax
        deco = VGroup()
        if ticks:
            for k in range(1, int(xmax) + 1):
                deco.add(Line(ax.c2p(k, 0), ax.c2p(k, 0.06), color=DIM, stroke_width=2))
                if tlab:
                    deco.add(MathTex(r"\tau" if k == 1 else rf"{k}\tau", font_size=24, color=VIOLET).move_to(ax.c2p(k, 0) + 0.27 * DOWN))
        deco.add(MathTex("0", font_size=24, color=DIM).move_to(ax.c2p(0, 0) + np.array([-0.22, -0.18, 0])))
        if one:
            deco.add(Line(ax.c2p(0, 1), ax.c2p(0.1 * xmax / 5, 1), color=DIM, stroke_width=2))
            deco.add(E(one, one, size=26).next_to(ax.c2p(0, 1), LEFT, buff=0.12))
        if tlab:
            deco.add(MathTex("t", font_size=28, color=VIOLET).move_to(ax.c2p(xmax, 0) + 0.28 * RIGHT))
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
        return self._keep(redraw(mk))

    def area(self, fn, tr, color, op_=0.35):
        ax, op = self.ax, self.op

        def mk():
            x1 = min(tr.get_value(), self.xmax)
            o = op.get_value()
            if x1 < 0.02 or o < 0.01:
                return VMobject()
            xs = np.linspace(0, x1, 80)
            return Polygon(ax.c2p(0, 0), *[ax.c2p(x, fn(x)) for x in xs], ax.c2p(x1, 0)).set_fill(color, op_ * o) \
                .set_stroke(width=0).set_z_index(5)
        return self._keep(redraw(mk))

    def marker(self, fn, tr, color=WHITE, slope=None):
        ax, op = self.ax, self.op

        def mk():
            x = min(tr.get_value(), self.xmax)
            o = op.get_value()
            if o < 0.01:
                return VMobject()
            y = fn(x)
            g = VGroup(DashedLine(ax.c2p(x, 0), ax.c2p(x, y), dash_length=0.07, color=WHITE, stroke_width=2).set_opacity(0.45 * o),
                       Dot(ax.c2p(x, y), radius=0.08).set_fill(color, o).set_stroke(WHITE, 1.5, o))
            if slope is not None:
                d = slope(x)
                hw = 0.4 / max(1.0, abs(d) * 1.6)
                g.add(Line(ax.c2p(x - hw, y - hw * d), ax.c2p(x + hw, y + hw * d)).set_stroke(CYAN, 3, o))
            return g.set_z_index(9)
        return self._keep(redraw(mk))

    def _keep(self, m):
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


SECOES = ["c01", "c02", "c03", "c04", "c05", "c06", "c07", "c08", "c09", "c10",
          "c11", "c12", "c13", "c14", "c15", "c16", "c17", "c18", "c19", "c20"]


class IndutanciaYT012(Base):
    def construct(self):
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(WM_W).set_opacity(WM_OP).to_corner(UR, buff=0.3)
        self.tag = txt("ELETROMAGNETISMO · INDUTÂNCIA E ENERGIA MAGNÉTICA", 24, opacity=0.78).to_corner(UL, buff=0.32).set_z_index(40)
        self.add(self.wm, self.tag)
        ap = self.ap = Ap()
        self.idx = {}
        self.body = self.cached(ap.key, ap.build)
        self.body.state_geometry = False                    # o aparato muda nas esperas também (relógio, chave)
        self.flowm = self.mk_flow()
        self.add(self.body, self.flowm)
        self.mk_labels()
        for nome in SECOES:
            getattr(self, nome)()
        out = PASTA / "tempos.json"
        json.dump({"sections": self.sections, "checkpoints": self.checkpoints, "layout_issues": self.layout_issues,
                   "duration": round(float(self.time), 2)}, open(out if not SEG else PASTA / f"tempos_SEG_{SEG}.json", "w",
                                                                 encoding="utf-8"), indent=1, ensure_ascii=False)

    # ── corrente: traços verdes correndo pelo fio (velocidade ∝ I; cabeça clara, cauda translúcida) ───────────
    def mk_flow(self):
        ap = self
        g = VGroup()
        g.ph = 0.0

        def upd(m, dt):
            a = ap.ap
            S = a.st()
            I = S["I"]
            m.ph = (m.ph + dt * VFLOW * abs(I)) % SPC
            o = a.oAll.get_value() * a.oFlow.get_value() * min(1.0, 4 * abs(I)) * a.lat()
            o *= a.oSec.get_value() if a.role == 2 else a.oCirc.get_value()
            marks = []
            P = a.path()
            if o > 0.01 and P:
                P = np.array(P, float)
                seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
                c = np.concatenate([[0.0], np.cumsum(seg)])
                L = c[-1]

                def at(s):
                    s = s % L
                    return np.interp(s, c, P[:, 0]), np.interp(s, c, P[:, 1])
                for s0 in np.arange(m.ph, L, SPC):
                    pts = [at(s0 + d) for d in (-DASH, 0.0, DASH)]
                    if any(a.hidden(x, y) for x, y in pts):
                        continue
                    b, mid, f = [a.W(x, y) for x, y in pts]
                    tail = Line(b, mid).set_stroke(GREEN, 7, 0.5 * o)
                    head = Line(mid, f).set_stroke(GREEN, 7, o)
                    for ln in (tail, head):
                        ln.set_stroke(BACKGROUND_COLOR, 10, o, background=True)
                    marks.append(VGroup(tail, head).set_z_index(8))
            m.submobjects = marks
        g.add_updater(upd)
        return g

    # ── rótulos presos ao aparato ─────────────────────────────────────────────────────────────────────────────
    def plab(self, mob, anchor, off=(0, 0), size=M_S, dep=None, color=None):
        ap = self.ap
        m = (E(mob, mob, size=size) if isinstance(mob, str) else mob)
        if color is not None:
            m.set_color(color)
        m.v = ValueTracker(0)
        deps = [getattr(ap, d) for d in (dep or [])]

        def upd(x):
            o = off() if callable(off) else off
            x.move_to(ap.W(*anchor()) + np.array([*o, 0]) * ap.s.get_value())
            ov = m.v.get_value() * ap.oAll.get_value()
            for d in deps:
                ov *= d.get_value() if not callable(d) else d()
            x.set_opacity(ov)
            if isinstance(x, MathTex):
                x.set_stroke(BACKGROUND_COLOR, 8, ov, background=True)
        m.add_updater(upd)
        upd(m)
        m.set_z_index(20)
        self.add(m)
        return m

    def mk_labels(self):
        L = self.L = {}
        lat = type("Lat", (), {"get_value": lambda _: self.ap.lat()})()
        self.ap.oLat = lat
        L["E0"] = self.plab(r"\mathcal E_0", lambda: (XL, 0), (-0.6, 0), dep=["oCirc", "oBat", "oLat"])
        L["R"] = self.plab("R", lambda: (XR, 0), (0.6, 0), dep=["oCirc", "oLat"])
        L["sol"] = self.plab(txt("solenoide", 20, DIM), lambda: (XC, YT - A_R), (0, -0.45), dep=["oSol", "oLat"])
        L["L"] = self.plab("L", lambda: (XC, YT - A_R), (0, -0.48), dep=["oSol", "oLat"])
        L["B"] = self.plab(r"\mathbf B", lambda: (XS0 + 0.15, YT - A_R), (0, -0.48), dep=["oSol", "oB", "oLat"])
        L["I"] = self.plab("I", lambda: (XIA, YB - 0.32), (0, -0.38), dep=["oCirc", "oIA", "oLat"])
        L["I1"] = self.plab("I_1", lambda: (XIA, YB - 0.32), (0, -0.38), dep=["oCirc", "oIA", "oLat"])
        L["EL"] = self.plab(r"\mathcal E_L", lambda: (XC, YT + A_R + 0.55), (0, 0.42), dep=["oSol", "oEL", "oLat"])
        L["E1"] = self.plab(r"\mathcal E_1", lambda: (XC, YT + A_R + 0.55), (-1.6, 0.0), dep=["oSol", "oEL", "oLat"])
        L["E2"] = self.plab(r"\mathcal E_2", lambda: (XC + MR, YMET), (0.48, 0.05), dep=["oSec"])
        L["N2"] = self.plab("N_2", lambda: (XM1, YT + A2), (0.62, -0.05), dep=["oSec"])
        L["I2"] = self.plab("I_2", lambda: (XM0, 0.5 * (YT + A2 + YMET)), (-0.42, 0), dep=["oSec"])
        L["med"] = self.plab(txt("medidor", 20, DIM), lambda: (XC, YMET), (0, 0.62), dep=["oSec"])
        L["fonte"] = self.plab(txt("fonte", 20, DIM), lambda: (XC, YMET), (0, 0.62), dep=["oSec"])
        L["A"] = self.plab("A", lambda: (XS1, YT), (0.75, 0.1), dep=["oSol"])
        L["ell"] = self.plab(r"\ell", lambda: (XC, YT - A_R - 0.45), (0, -0.32), dep=["oSol"])
        L["a"] = self.plab("a", lambda: (XC, YT), (0.22, 0.12), size=28, dep=["oSol"])
        L["C"] = self.plab("C", lambda: (XC, YT - PH), (0, -0.5), dep=["oCap"])
        L["S1"] = self.plab("S_1", lambda: (XAMP, YT - RAMP), (-0.25, -0.3), size=28, dep=["oAmp", "oS1"], color=VIOLET)
        L["S2"] = self.plab("S_2", lambda: (XC, YT + RAMP), (0.35, 0.32), size=28, dep=["oAmp", "oS2"], color=CYAN)
        L["gap"] = self.plab(r"I=0", lambda: (XC, YT + PH), (0.0, 0.42), size=26, dep=["oCap"], color=GREEN)
        L["Gb"] = self.plab(r"P_{\rm fonte}", lambda: (XL + 0.85, -0.05), (0, 0.38), size=32, dep=["oGauge", "oGb"])
        L["Gr"] = self.plab(r"P_{\rm Joule}", lambda: (XR - 0.85, -0.05), (0, 0.38), size=32, dep=["oGauge", "oGr"])
        L["Gs"] = self.plab(r"\frac{dU_B}{dt}", lambda: (XC + 1.0, -0.05), (0, 0.55), size=32, dep=["oGauge", "oGs"])

    def show_l(self, *ks):
        return [self.L[k].v.animate.set_value(1) for k in ks]

    def hide_l(self, *ks):
        return [self.L[k].v.animate.set_value(0) for k in ks]

    def view(self, name):
        ap = self.ap
        return [tr.animate.set_value(v) for tr, v in zip((ap.s, ap.cx, ap.cy, ap.fx, ap.fy), VIEW[name])]

    def setview(self, name):
        for tr, v in zip((self.ap.s, self.ap.cx, self.ap.cy, self.ap.fx, self.ap.fy), VIEW[name]):
            tr.set_value(v)

    def Wv_(self, name, x, y):
        s, cx, cy, fx, fy = VIEW[name]
        return np.array([cx + s * (x - fx), cy + s * (y - fy), 0.0])

    def run(self, tr, v, t, *extra):
        self.play(tr.animate.set_value(v), *extra, run_time=t, rate_func=linear)

    def rewind(self, tr, gx=None):
        """Recomeça o mesmo processo em t = 0 (marca violeta t = 0 no gráfico; nenhum texto de depuração)."""
        ap = self.ap
        self.play(ap.oFlow.animate.set_value(0), run_time=0.5)      # o circuito não apaga no recomeço
        tr.set_value(0.0)
        mk = None
        if gx is not None:
            mk = MathTex("t=0", font_size=28, color=VIOLET).next_to(gx.c2p(0, 0), DOWN, buff=0.4).set_z_index(30)
        self.play(ap.oAll.animate.set_value(1), ap.oFlow.animate.set_value(1), *([FadeIn(mk)] if mk else []), run_time=0.6)
        if mk:
            self.play(FadeOut(mk), run_time=0.5)

    def ring_hl(self, p, w=1.0, h=1.0, color=WHITE):
        r = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(color, 4).move_to(p).set_z_index(25)
        self.play(Create(r), run_time=0.6)
        self.play(r.animate.set_stroke(opacity=0), run_time=0.5)
        self.remove(r)

    # ── manchete (docs/padrao_video_longo.md): uma linha em MAIÚSCULAS no topo, troca sequencial ─────────────
    def caption(self, s, color=WHITE, rt=0.45):
        self._ev("caption", s)
        new = rich(s, T_BODY, WHITE)
        if new.width > 11.5:
            new.scale_to_fit_width(11.5)
        new.set_opacity(0.92).move_to([0, 3.42, 0]).set_z_index(30)
        if self.head is not None:
            self.play(FadeOut(self.head, shift=0.08 * UP), run_time=0.3)
        self.play(FadeIn(new, shift=0.08 * UP), run_time=rt)
        self.head = new

    def section(self, name, title=None):
        super().section(name)
        if title:
            self.caption(title)

    def delcap(self):
        if self.head is not None:
            self.play(FadeOut(self.head), run_time=0.35)
            self.head = None

    # ── índice de variáveis: definições "símbolo: significado" em minúsculas (MathTex), num cartão ───────────
    def indice(self, rows, slot="A", rt=0.9):
        s = self.slots[slot]
        self.sem_indice(slot)
        if s["eq"] is not None or s["card"] is not None:
            self.drop(slot, keep_card=False)
        items = VGroup()
        for sym, d in rows:
            tok = "{" + sym + "}"
            items.add(defn(tok + r":\ \text{" + d + "}", tok, size=36, colors={tok: TOKCOL.get(sym, WHITE)}))
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        g = items
        if g.width > s["w"] - 0.7:
            g.scale_to_fit_width(s["w"] - 0.7)
        if g.height > s["h"] - 0.3:
            g.scale_to_fit_height(s["h"] - 0.3)
        card = panel(g.width + 0.7, g.height + 0.45, s["pos"])
        g.move_to(s["pos"])
        self.play(FadeIn(card), FadeIn(g), run_time=rt)
        self.idx[slot] = VGroup(card, g)
        return g

    def sem_indice(self, slot="A", rt=0.5):
        m = self.idx.pop(slot, None)
        if m is not None:
            self.play(FadeOut(m), run_time=rt)

    def limpa_slots(self):
        for k in ("H", "A"):
            self.sem_indice(k)
            self.drop(k, keep_card=False)

    # ── auditoria: texto sobre texto, texto cortando cartão (registrada em tempos.json → layout_issues) ───────
    def audit(self, name):
        boxes = []
        for root in self.mobjects:
            if root is self.tag or root is self.wm:
                continue
            for m in root.get_family():
                if isinstance(m, MathTex) or m.__class__.__name__ == "Text":
                    fam = m.family_members_with_points()
                    if not fam or max(max(f.get_fill_opacity(), f.get_stroke_opacity()) for f in fam) < 0.3 or m.width < 0.05:
                        continue
                    boxes.append((m, m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1]))
        for i, (a, x0, x1, y0, y1) in enumerate(boxes):
            for b, u0, u1, v0, v1 in boxes[i + 1:]:
                if a in b.get_family() or b in a.get_family():
                    continue
                ox, oy = min(x1, u1) - max(x0, u0), min(y1, v1) - max(y0, v0)
                if ox > 0.04 and oy > 0.04:
                    na = getattr(a, "tex_string", getattr(a, "text", ""))[:30]
                    nb = getattr(b, "tex_string", getattr(b, "text", ""))[:30]
                    self.layout_issues.append({"estado": name, "t": round(float(self.time), 2), "sobrepoe": [na, nb]})

    def mark(self, name):
        super().mark(name)
        self.audit(name)

    # ═══ C01 — a previsão que falha ═══════════════════════════════════════════════════════════════════════
    def c01(self):
        ap, L = self.ap, self.L
        self.section("c01")
        self.setview("left")
        self.an("Olha esse circuito")
        self.play(ap.oAll.animate.set_value(1), *self.show_l("E0", "R", "sol"), run_time=T_MOVE)
        self.caption("Um circuito em série")
        self.indice([(r"\mathcal E_0", "fem da bateria"), ("R", "resistência do resistor"), ("I", "corrente no circuito")])
        self.hold(T_HOLD)
        self.mark("c01_aparato")
        self.sem_indice("A")
        g = self.g = Graf(self, one=r"I_\infty", ylab="I", ycol=GREEN)
        self.an("Com a chave aberta")
        self.caption("Chave aberta: nenhuma corrente")
        self.show(E(r"I=0", "I", size=M_XL), rt=1.2, wait=0)
        self.play(*g.show(), run_time=T_IN)
        self.hold(T_READ)
        self.an("Agora eu fecho a chave")
        self.caption("A previsão ingênua: um salto")
        jump = DashedVMobject(VMobject().set_points_as_corners([g.c2p(0, 0), g.c2p(0, 1), g.c2p(5, 1)]),
                              num_dashes=48, dashed_ratio=0.55).set_stroke(WHITE, 3, 0.85).set_z_index(5)
        self.an("A corrente iria direto")
        self.show(E(r"I=\frac{\mathcal E_0}{R}", "I", r"\mathcal E_0", "R", size=M_XL), src={(r"\mathcal E_0", 0): L["E0"],
                  ("R", 0): L["R"]}, rt=T_EQ, wait=0)
        self.an("No gráfico, seria um degrau")
        self.play(Create(jump), run_time=1.6)
        self.hold(T_READ)
        self.mark("c01_previsao")
        self.an("Vamos testar")
        self.caption("Fechamos a chave")
        self.play(ap.sw.animate.set_value(SW_A), run_time=T_SW)
        g.curve(lambda x: 1 - math.exp(-x), ap.tc, GREEN, 5)
        g.marker(lambda x: 1 - math.exp(-x), ap.tc, GREEN)
        self.an("Só que não acontece isso")
        self.play(ap.oFlow.animate.set_value(1), ap.oIA.animate.set_value(1), ap.oCoilI.animate.set_value(1),
                  *self.show_l("I", "B"), run_time=0.6)
        self.run(ap.tc, 0.6, 0.2 * T_RUN, jump.animate.set_stroke(opacity=0))
        self.remove(jump)
        self.an("A corrente começa em zero")
        self.caption("A corrente cresce aos poucos")
        self.run(ap.tc, 2.0, 0.4 * T_RUN)
        self.an("Ela vai se aproximando")
        self.show(E(r"I(t)=I_\infty\left(1-e^{-t/\tau}\right)", "I(t)", r"I_\infty", r"-t/\tau", size=M_L),
                  rt=T_EQ, wait=0, note=(r"I_\infty:\ \text{corrente final}", r"I_\infty"))
        self.run(ap.tc, 3.2, 0.3 * T_RUN)
        self.an("E olha o solenoide")
        self.caption("O campo $\\mathbf B$ cresce junto")
        self.ring_hl(self.Wv_("left", XC, YT), 3.2, 1.2, MAG)
        self.run(ap.tc, 5.0, 0.4 * T_RUN)
        self.an("Então temos um problema")
        self.caption("Deveria saltar. Mas não salta.")
        self.mark("c01_curva")
        self.hold(T_HOLD)

    # ═══ C02 — promessa ═════════════════════════════════════════════════════════════════════════════════════
    def c02(self):
        ap, L, g = self.ap, self.L, self.g
        self.section("c02")
        self.delcap()
        self.limpa_slots()
        self.play(*g.hide(), ap.oAll.animate.set_value(0.0), run_time=T_MOVE)
        g.drop()
        ap.tc.set_value(0)
        ap.sw.set_value(SW_OPEN)
        ap.oFlow.set_value(0)
        ap.oIA.set_value(0)
        # bem-vindos (logo) → título + "neste vídeo" → de volta ao aparato (docs/padrao_video_longo.md)
        logo = ImageMobject(str(LOGO_H)).set_width(4.6).move_to([0, 0.8, 0])
        wel = txt("Bem-vindos ao Parallax Lab", 34, WHITE).move_to([0, -1.3, 0])
        self.an("Fala, pessoal")
        self.play(FadeIn(logo, scale=0.94), FadeIn(wel, shift=0.1 * UP), *self.hide_l("I", "B"), run_time=1.2)
        self.hold(2.0)
        self.play(FadeOut(logo), FadeOut(wel), run_time=0.6)
        t1 = txt("Por que a corrente resiste a mudar?", 44, CYAN).move_to([0, 0.45, 0])
        t2 = txt("Neste vídeo: indutância, energia magnética e onde ela fica", 26, DIM).move_to([0, -0.5, 0])
        for t in (t1, t2):
            if t.width > 12.5:
                t.scale_to_fit_width(12.5)
        self.an("No vídeo passado")
        self.play(FadeIn(t1, shift=0.1 * UP), FadeIn(t2), run_time=1.2)
        self.mark("c02_titulo")
        self.hold(3.0)
        # roteiro do vídeo: quatro etapas que entram junto com a fala
        etapas = [("por que a corrente resiste", "1 · autoindução"), ("resolver o circuito", "2 · o circuito RL"),
                  ("descobrir onde fica a energia", "3 · a energia no campo"), ("desligar a bateria", "4 · a descarga")]
        itens = VGroup(*[txt(r, 24, WHITE, 0.9) for _, r in etapas]).arrange(RIGHT, buff=0.6).move_to([0, -1.5, 0])
        if itens.width > 13.0:
            itens.scale_to_fit_width(13.0)
        for (fala, _), it in zip(etapas, itens):
            self.an(fala)
            self.play(FadeIn(it, shift=0.08 * UP), run_time=0.6)
        self.an("Spoiler")
        self.play(FadeOut(t1, shift=0.1 * UP), FadeOut(t2, shift=0.1 * UP), FadeOut(itens, shift=0.1 * UP),
                  self.tag.animate.scale(0.84, about_point=self.tag.get_corner(UL)).set_opacity(0.58), run_time=0.7)
        self.play(ap.oAll.animate.set_value(1), run_time=1.0)

    # ═══ C03 — indução mútua ════════════════════════════════════════════════════════════════════════════════
    def c03(self):
        ap, L = self.ap, self.L
        self.an("Antes de fazer uma bobina")
        self.section("c03", "Duas bobinas")
        self.an("Em volta do solenoide eu coloco")
        self.play(*self.view("mut"), ap.oSec.animate.set_value(1), *self.show_l("N2", "E2", "med"), *self.hide_l("sol"),
                  run_time=T_MOVE)
        self.an("Ela não tem contato elétrico")
        self.caption("Uma segunda bobina, com um medidor")
        self.indice([("I_1", "corrente no solenoide"), ("N_2", "número de espiras da bobina 2"),
                     (r"\mathcal E_2", "fem induzida na bobina 2")])
        self.hold(T_HOLD)
        self.mark("c03_aparato")
        self.an("Agora olha a sequência")
        self.sem_indice("A")
        self.play(ap.sw.animate.set_value(SW_A), run_time=T_SW)
        self.an("A corrente no solenoide começa")
        self.caption("A corrente $I_1$ muda...")
        self.play(ap.oFlow.animate.set_value(1), ap.oIA.animate.set_value(1), ap.oCoilI.animate.set_value(1),
                  *self.show_l("I1"), ap.tc.animate.set_value(0.25), run_time=2.6, rate_func=linear)
        self.an("O campo magnético produzido por ela")
        self.caption("...o campo $\\mathbf B_1$ cresce...")
        self.play(*self.show_l("B"), ap.tc.animate.set_value(0.5), run_time=2.6, rate_func=linear)
        self.an("Esse campo atravessa as espiras")
        self.caption("...atravessa a bobina 2...")
        self.play(ap.oFlux.animate.set_value(1), ap.tc.animate.set_value(0.75), run_time=2.6, rate_func=linear)
        self.an("E o medidor acusa")
        self.caption("...e surge uma fem $\\mathcal E_2$")
        self.run(ap.tc, 1.0, 2.6)
        self.an("Corrente muda")
        self.show(E(r"I_1\ \longrightarrow\ \mathbf B_1\ \longrightarrow\ \Lambda_2\ \longrightarrow\ \mathcal E_2", "I_1",
                    r"\mathbf B_1", r"\Lambda_2", r"\mathcal E_2", size=M_L),
                  src={("I_1", 0): L["I1"], (r"\mathcal E_2", 0): L["E2"]}, rt=T_EQ, wait=0)
        self.run(ap.tc, 1.4, 2.0)
        self.an("Para contar o efeito em todas")
        self.show(E(r"I_1\ \longrightarrow\ \mathbf B_1\ \longrightarrow\ \Lambda_2\ \longrightarrow\ \mathcal E_2", "I_1",
                    r"\mathbf B_1", r"\Lambda_2", r"\mathcal E_2", size=M_L), rt=1.0, wait=0,
                  note=(r"\Lambda_2:\ \text{fluxo concatenado pela bobina 2}", r"\Lambda_2"))
        self.run(ap.tc, 1.8, 3.0)
        self.an("Agora segura a corrente")
        self.caption("Corrente constante: ponteiro no zero")
        self.run(ap.tc, 5.0, T_RUN)
        self.mark("c03_cadeia")
        self.an("A segunda bobina não responde")
        self.caption("Só há fem enquanto $I_1$ muda")
        self.hold(T_READ)
        self.an("Para esta geometria fixa")
        self.show(E(r"\Lambda_2=M\,I_1", r"\Lambda_2", "M", "I_1", size=M_XL), slot="A", rt=T_EQ, wait=0, note=(r"M:\ \text{indutância mútua}", "M"))
        self.hold(T_READ)
        self.an("E quando derivamos isso")
        self.show(E(r"\mathcal E_2=-M\,\frac{dI_1}{dt}", r"\mathcal E_2", "M", r"\frac{dI_1}{dt}", size=M_XL), slot="H",
                  src={("M", 0): glyphs(self.slots["A"]["eq"], "M", 0)}, rt=T_EQ, wait=0)
        self.caption("Indução mútua")
        self.hold(T_HOLD)
        self.mark("c03_leis")
        # de onde vem M: geometria
        self.an("E de onde vem a indutância mútua")
        self.caption("De onde vem $M$?")
        self.play(ap.oAe.animate.set_value(1), *self.show_l("A"), run_time=T_IN)
        self.an("O fluxo concatenado é o número")
        self.show(E(r"\Lambda_2=N_2\,\mathbf B_1\,A", r"\Lambda_2", "N_2", r"\mathbf B_1", "A", size=M_XL), slot="A",
                  src={("N_2", 0): L["N2"], ("A", 0): L["A"]}, rt=T_EQ, wait=0, note=(r"\mathbf B_1 A:\ \text{fluxo em cada espira}", r"\mathbf B_1", "A"))
        self.hold(T_READ)
        self.an("E aqui existe uma pegadinha")
        self.caption("Só a área do solenoide conta")
        self.hold(T_READ)
        self.an("Substituindo o campo do solenoide")
        self.show(E(r"\Lambda_2=N_2\,\mu_0\,n\,I_1\,A", r"\Lambda_2", "N_2", "n", "I_1", "A", size=M_XL),
                  (r"\mathbf B_1", None), slot="A", rt=T_EQ, wait=0, note=defn(r"B_1=\mu_0\,{n}\,I_1", "B_1", "{n}", "I_1", colors={"{n}": GEO}))
        self.hold(T_READ)
        self.an("Tudo o que sobra multiplicando")
        self.show(E(r"M=\mu_0\,n\,N_2\,A", "M", "n", "N_2", "A", size=M_XL), slot="H", rt=T_EQ, wait=0,
                  name="indutância mútua", note=defn(r"{n}:\ \text{espiras por metro}", "{n}", colors={"{n}": GEO}))
        self.hold(T_READ)
        self.an("Aqui, como estamos no vácuo")
        self.caption("$M$ só depende da geometria")
        self.mark("c03_M")
        self.hold(T_HOLD)

    # ═══ C04 — reciprocidade ════════════════════════════════════════════════════════════════════════════════
    def c04(self):
        ap, L = self.ap, self.L
        self.an("Agora vamos inverter o experimento")
        self.section("c04", "Trocando os papéis das bobinas")
        self.limpa_slots()
        self.play(ap.oAe.animate.set_value(0), *self.hide_l("A", "I1", "med", "E2", "B"), ap.oFlow.animate.set_value(0),
                  ap.oIA.animate.set_value(0), ap.oCoilI.animate.set_value(0), ap.sw.animate.set_value(SW_OPEN),
                  ap.oBat.animate.set_value(1.0), ap.oFlux.animate.set_value(0), run_time=1.2)
        ap.tc.set_value(0)
        ap.role = 2
        self.an("A segunda bobina recebe a fonte")
        self.caption("A bobina 2 vira a fonte")
        self.play(*self.show_l("fonte", "I2"), ap.oSrc.animate.set_value(1), run_time=T_EQ)
        self.an("A corrente nela começa a mudar")
        self.play(ap.oFlow.animate.set_value(1), *self.show_l("B"), ap.tc.animate.set_value(0.5), run_time=2.6, rate_func=linear)
        self.an("E agora quem sente")
        self.caption("A fem aparece no solenoide")
        self.play(*self.show_l("E1"), ap.oEL.animate.set_value(1), ap.tc.animate.set_value(0.9), run_time=1.6, rate_func=linear)
        self.run(ap.tc, 4.0, 2.6)
        self.an("No nosso modelo linear")
        self.show(E(r"M_{12}=M_{21}", "M_{12}", "M_{21}", size=M_XL), rt=T_EQ, wait=0, name="reciprocidade")
        self.caption("O mesmo $M$ nos dois sentidos")
        self.mark("c04_reciproca")
        self.hold(T_HOLD)
        self.an("Só que agora vem a pergunta")
        self.caption("E se o segundo circuito desaparecer?")
        self.hold(T_READ)

    # ═══ C05 — mútua vira autoindução ═══════════════════════════════════════════════════════════════════════
    def c05(self):
        ap, L = self.ap, self.L
        self.section("c05")
        self.limpa_slots()
        self.play(*self.hide_l("E1", "I2", "fonte"), ap.oEL.animate.set_value(0), ap.oFlow.animate.set_value(0),
                  ap.oBat.animate.set_value(1), ap.oSrc.animate.set_value(0), run_time=T_MOVE)
        ap.role = 1
        ap.tc.set_value(0)
        self.play(*self.view("left"), ap.sw.animate.set_value(SW_A), *self.show_l("med", "E2"), run_time=T_MOVE)
        self.show(E(r"\Lambda_2=M\,I_1", r"\Lambda_2", "M", "I_1", size=M_XL), rt=T_EQ, wait=0)
        self.play(ap.oFlow.animate.set_value(1), ap.oIA.animate.set_value(1), ap.oCoilI.animate.set_value(1), *self.show_l("I1", "B"),
                  ap.oFlux.animate.set_value(1), ap.tc.animate.set_value(0.3), run_time=2.0, rate_func=linear)
        self.an("Tiramos a segunda bobina")
        self.caption("Sem a bobina 2, o campo continua")
        self.play(ap.oSec.animate.set_value(0), *self.hide_l("N2", "med", "E2"), ap.tc.animate.set_value(0.6), run_time=2.6,
                  rate_func=linear)
        ap.oFlux.set_value(0)
        self.an("E esse campo atravessa as próprias")
        self.caption("O fluxo atravessa as próprias espiras")
        self.play(ap.oHL.animate.set_value(1), ap.tc.animate.set_value(0.95), run_time=2.6, rate_func=linear)
        self.an("Então a mesma lógica vale")
        self.show(E(r"\Lambda=L\,I", r"\Lambda", "L", "I", size=M_XL), (r"\Lambda_2", r"\Lambda"), ("I_1", "I"), ("M", None),
                  rt=T_EQ, wait=0, name="autoindutância", note=(r"L:\ \text{autoindutância, em henry}", "L"))
        self.an("Na tela, ela aparece como")
        self.play(*self.hide_l("sol", "I1"), *self.show_l("L", "I"), ap.tc.animate.set_value(1.3), run_time=T_IN, rate_func=linear)
        self.hold(T_READ)
        self.an("E se a corrente muda, o fluxo próprio")
        self.caption("Fem autoinduzida")
        self.play(ap.oHL.animate.set_value(0), ap.tc.animate.set_value(1.6), run_time=T_IN, rate_func=linear)
        self.an("A força eletromotriz autoinduzida é menos")
        self.show(E(r"\mathcal E_L=-L\,\frac{dI}{dt}", r"\mathcal E_L", "L", r"\frac{dI}{dt}", size=M_XL), slot="A",
                  src={("L", 0): glyphs(self.slots["H"]["eq"], "L", 0)}, rt=T_EQ, wait=0, name="fem autoinduzida", note=(r"\mathcal E_L:\ \text{fem autoinduzida}", r"\mathcal E_L"))
        self.mark("c05_EL")
        self.run(ap.tc, 2.2, T_READ)
        self.an("A seta ciano mostra")
        self.caption("Seta ciano: o sentido da fem")
        self.play(*self.show_l("EL"), ap.oEL.animate.set_value(1), ap.tc.animate.set_value(2.6), run_time=T_EQ, rate_func=linear)
        self.run(ap.tc, 4.0, T_READ)

    # ═══ C06 — o que o indutor combate ══════════════════════════════════════════════════════════════════════
    def c06(self):
        ap, L = self.ap, self.L
        self.an("Para enxergar o sinal negativo")
        self.section("c06", "O que o indutor realmente combate")
        self.limpa_slots()
        self.play(*self.view("solo"), ap.oCirc.animate.set_value(0), ap.oFlow.animate.set_value(0), *self.hide_l("I"),
                  run_time=T_MOVE)
        ap.mode = "probe"
        ap.sp.set_value(0)
        gp = self.gp = Graf(self, w=5.4, h=1.9, xmax=3.2, ticks=False, ylab="I", ycol=GREEN)
        gp.curve(lambda x: probe(x)[0], ap.sp, GREEN, 5)
        gp.marker(lambda x: probe(x)[0], ap.sp, GREEN, slope=lambda x: probe(x)[1] * PI / 2)
        self.an("Primeiro ela aumenta")
        self.caption("Corrente imposta: sobe, para, desce")
        self.an("E ao lado, o gráfico")
        self.play(*gp.show(), run_time=T_IN)
        self.hold(1.0)
        self.an("Quando a corrente aumenta")
        self.run(ap.sp, 0.5, 3.0)
        self.an("A força eletromotriz induzida aponta contra")
        self.show(E(r"\frac{dI}{dt}>0\ \Rightarrow\ \mathcal E_L\ \text{contra}\ I", r"\frac{dI}{dt}", r"\mathcal E_L", "I",
                    size=M_M), rt=1.4, wait=0)
        self.caption("Corrente aumentando: fem contra")
        self.run(ap.sp, 0.8, T_READ)
        self.mark("c06_sobe")
        self.an("Agora a corrente fica constante")
        self.run(ap.sp, 1.5, 4.0)
        self.an("Depois a corrente começa a cair")
        self.run(ap.sp, 2.3, 3.0)
        self.an("e a força eletromotriz troca de sentido")
        self.show(E(r"\frac{dI}{dt}<0\ \Rightarrow\ \mathcal E_L\ \text{a favor de}\ I", r"\frac{dI}{dt}", r"\mathcal E_L", "I",
                    size=M_M), rt=1.4, wait=0)
        self.caption("Corrente diminuindo: fem a favor")
        self.run(ap.sp, 2.6, T_READ)
        self.mark("c06_desce")
        self.an("O indutor é aquele amigo")
        self.run(ap.sp, 3.0, 2.4)
        self.an("Então guarda esta frase")
        self.delcap()
        self.limpa_slots()
        self.play(*self.hide_l("I", "L", "B", "EL"), run_time=0.4)
        dim = Rectangle(width=16, height=6.2).set_fill(BACKGROUND_COLOR, 0.9).set_stroke(width=0).move_to([0, -0.3, 0]).set_z_index(25)
        p1 = txt("O indutor não se opõe à corrente.", 40, WHITE).move_to([0, 0, 0]).set_z_index(26)
        p2 = VGroup(txt("Ele se opõe à", 40, WHITE), txt("mudança", 46, CYAN), txt("da corrente.", 40, WHITE)) \
            .arrange(RIGHT, buff=0.24).move_to([0, 0, 0]).set_z_index(26)
        self.an("O indutor não se opõe")
        self.play(FadeIn(dim), FadeIn(p1, shift=0.1 * UP), run_time=1.0)
        self.hold(T_READ)
        self.play(FadeOut(p1, shift=0.1 * UP), run_time=0.6)
        self.an("Ele se opõe à mudança")
        self.play(FadeIn(p2, shift=0.1 * UP), run_time=0.8)
        self.play(p2[1].animate.scale(1.12), run_time=0.45)
        self.play(p2[1].animate.scale(1 / 1.12), run_time=0.45)
        self.mark("c06_payoff")
        self.hold(T_HOLD)
        self.an("E isso resolve uma confusão")
        self.play(FadeOut(p2), FadeOut(dim), run_time=0.8)
        ap.sp.set_value(0)
        self.caption("E com corrente constante?")
        self.an("Podemos ter corrente constante")
        self.run(ap.sp, 1.5, 4.5, *self.show_l("L", "B", "EL"))
        self.an("E mesmo assim a força eletromotriz")
        self.show(E(r"I\neq0,\quad \frac{dI}{dt}=0\ \Rightarrow\ \mathcal E_L=0", "I", r"\frac{dI}{dt}", r"\mathcal E_L", size=M_M),
                  rt=1.4, wait=0)
        self.mark("c06_constante")
        self.hold(T_HOLD)

    # ═══ C07 — equação RL ═══════════════════════════════════════════════════════════════════════════════════
    def c07(self):
        ap, L, gp = self.ap, self.L, self.gp
        self.an("Agora voltamos ao circuito do começo")
        self.section("c07", "De volta ao circuito: a lei das malhas")
        self.limpa_slots()
        self.play(*gp.hide(), run_time=0.7)                 # o gráfico sai antes de o solenoide voltar ao tamanho do circuito
        self.play(*self.view("left"), ap.oCirc.animate.set_value(1), run_time=T_MOVE)
        gp.drop()
        ap.mode = "charge"
        ap.tc.set_value(0.9)
        self.an("Fonte, resistor e indutor")
        self.play(ap.oFlow.animate.set_value(1), ap.oIA.animate.set_value(1), *self.show_l("I"), run_time=T_IN)
        self.an("Vamos escolher o sentido da corrente")
        self.caption("Uma volta na malha")
        tE = self.lab(r"+\mathcal E_0", self.Wv_("left", XL, YT) + np.array([0.0, 0.5, 0]), r"\mathcal E_0", size=M_S)
        tL = self.lab(r"-L\frac{dI}{dt}", self.Wv_("left", XS1 + 1.0, YT + 0.65), "L", "dI", "dt", size=M_S)
        tR = self.lab(r"-R\,I", self.Wv_("left", XR, YB) + np.array([0.0, -0.5, 0]), "R", "I", size=M_S)
        self.hold(2.0)
        self.an("A bateria fornece uma força eletromotriz positiva")
        self.caption("A bateria: $+\\mathcal E_0$")
        self.ring_hl(self.Wv_("left", XL, 0), 1.0, 1.0, CYAN)
        self.play(FadeIn(tE, shift=0.1 * UP), run_time=T_IN)
        self.hold(1.5)
        self.an("A força eletromotriz autoinduzida vale menos")
        self.caption("O indutor: $-L\\,dI/dt$")
        self.ring_hl(self.Wv_("left", XC, YT), 3.0, 1.2, CYAN)
        self.play(FadeIn(tL, shift=0.1 * UP), run_time=T_IN)
        self.hold(1.5)
        self.an("E o resistor produz a queda")
        self.caption("O resistor: $-RI$")
        self.ring_hl(self.Wv_("left", XR, 0), 0.9, 1.4, HEAT)
        self.play(FadeIn(tR, shift=0.1 * UP), run_time=T_IN)
        self.hold(1.5)
        # a soma com a fem do indutor pelo nome; depois a substituição ℰ_L = −L dI/dt
        self.an("A soma na malha precisa fechar")
        self.caption("A soma fecha em zero")
        self.show(E(r"\mathcal E_0+\mathcal E_L-R\,I=0", r"\mathcal E_0", r"\mathcal E_L", "R", "I", size=M_XL),
                  src={(r"\mathcal E_0", 0): glyphs(tE, r"\mathcal E_0"), (r"\mathcal E_L", 0): L["EL"],
                       ("R", 0): glyphs(tR, "R"), ("I", 0): glyphs(tR, "I")},
                  rt=2.4, wait=0, name="lei das malhas")
        self.hold(T_READ)
        self.an("Substituindo a expressão do indutor")
        self.show(E(r"\mathcal E_0-L\frac{dI}{dt}-R\,I=0", r"\mathcal E_0", "L", "dI", "dt", "R", "I", size=M_XL),
                  (r"\mathcal E_L", None), src={("L", 0): glyphs(tL, "L"), ("dI", 0): glyphs(tL, "dI"), ("dt", 0): glyphs(tL, "dt")},
                  rt=2.2, wait=0, name="lei das malhas")
        self.mark("c07_malha")
        self.hold(1.2)
        self.play(FadeOut(VGroup(tE, tL, tR)), run_time=0.6)
        self.caption("Organizando")
        self.show(E(r"L\frac{dI}{dt}+R\,I=\mathcal E_0", "L", "dI", "dt", "R", "I", r"\mathcal E_0", size=M_XL),
                  rt=T_EQ, wait=0, name="equação do circuito RL")
        self.mark("c07_rl")
        self.an("E aqui aparece o motivo matemático")
        self.play(Indicate(glyphs(self.slots["H"]["eq"], "dI"), color=CYAN, scale_factor=1.15), run_time=1.2)
        self.hold(T_HOLD)

    # ═══ C08 — resolver a dinâmica ══════════════════════════════════════════════════════════════════════════
    def c08(self):
        self.an("Vamos resolver")
        self.section("c08", "Resolvendo a equação do circuito")
        self.hold(2.0)
        self.an("Primeiro isolamos a taxa")
        self.caption("Dividindo por $L$")
        self.show(E(r"\frac{dI}{dt}=\frac{\mathcal E_0-R\,I}{L}", "dI", "dt", r"\mathcal E_0", "R", "I", "L", size=M_XL),
                  rt=T_EQ, wait=1.0, name="equação do circuito RL")
        # R/L em evidência: a fala não cita o passo, ele só prepara as duas combinações (passa rápido)
        self.an("Agora aparecem duas combinações")
        self.caption("Duas combinações ganham nome")
        self.show(E(r"\frac{dI}{dt}=\frac{R}{L}\left(\frac{\mathcal E_0}{R}-I\right)", "dI", "dt", "R", "L", r"\mathcal E_0", "I",
                    size=M_XL), rt=1.6, wait=0.6)
        self.an("A força eletromotriz da bateria dividida pela resistência é a corrente final")
        self.show(E(r"I_\infty=\frac{\mathcal E_0}{R}\qquad \tau=\frac{L}{R}", r"I_\infty", r"\mathcal E_0", "R", r"\tau", "L",
                    size=M_L), slot="A", rt=T_EQ, wait=0, note=(r"I_\infty:\ \text{corrente final}\qquad \tau:\ \text{constante de tempo}", r"I_\infty", r"\tau"))
        self.hold(T_READ)
        self.an("Já a autoindutância dividida")
        self.play(Indicate(glyphs(self.slots["A"]["eq"], r"\tau"), color=VIOLET, scale_factor=1.2), run_time=1.2)
        self.hold(T_READ)
        self.mark("c08_definicoes")
        A_ = self.slots["A"]["eq"]
        self.an("Com esses nomes")
        self.show(E(r"\frac{dI}{dt}=\frac{I_\infty-I}{\tau}", "dI", "dt", r"I_\infty", "I", r"\tau", size=M_XL),
                  src={(r"I_\infty", 0): glyphs(A_, r"I_\infty"), (r"\tau", 0): glyphs(A_, r"\tau")}, rt=T_EQ, wait=0)
        self.hold(T_READ)
        self.an("Longe do final")
        self.caption("Longe do final, muda depressa")
        self.hold(T_READ)
        self.an("Agora separamos as variáveis")
        self.caption("Separando as variáveis")
        self.show(E(r"\frac{dI}{I_\infty-I}=\frac{dt}{\tau}", "dI", "dt", r"I_\infty", "I", r"\tau", size=M_XL), rt=T_EQ, wait=T_READ)
        self.an("Integramos desde o instante")
        self.caption("Integrando desde $I(0)=0$")
        self.show(E(r"\int_0^{I}\frac{dI}{I_\infty-I}=\int_0^{t}\frac{dt}{\tau}", "dI", "dt", r"I_\infty", "I", r"\tau", size=M_XL),
                  rt=T_EQ, wait=T_READ)
        self.an("A integral do lado da corrente")
        self.caption("As duas integrais")
        self.show(E(r"-\ln\frac{I_\infty-I}{I_\infty}=\frac{t}{\tau}", r"I_\infty", "I", r"\frac{t}{\tau}", size=M_XL),
                  (r"\tau", r"\frac{t}{\tau}"), rt=T_EQ, wait=T_READ)
        self.an("Exponenciando, eliminamos")
        self.caption("Exponenciando")
        self.show(E(r"\frac{I_\infty-I}{I_\infty}=e^{-t/\tau}", r"I_\infty", "I", r"-t/\tau", size=M_XL), (r"\frac{t}{\tau}", r"-t/\tau"),
                  rt=T_EQ, wait=T_READ)
        self.an("E isolando a corrente")
        self.caption("Isolando a corrente")
        self.show(E(r"I(t)=I_\infty\left(1-e^{-t/\tau}\right)", "I(t)", r"I_\infty", r"-t/\tau", size=M_XL), ("I", "I(t)", 0, 0),
                  rt=T_EQ, wait=0, name="corrente na carga")
        self.hold(T_READ)
        self.an("Confere os extremos")
        self.show(E(r"I(t)=I_\infty\left(1-e^{-t/\tau}\right)", "I(t)", r"I_\infty", r"-t/\tau", size=M_XL), rt=1.0, wait=0,
                  name="corrente na carga", note=(r"I(0)=0,\qquad I\to I_\infty", "I(0)", r"I_\infty", "I"))
        self.mark("c08_solucao")
        self.hold(T_HOLD)

    # ═══ C09 — uma escala controla tudo ═════════════════════════════════════════════════════════════════════
    def c09(self):
        ap, L = self.ap, self.L
        self.an("Agora vamos rodar essa carga")
        self.section("c09", "Uma única escala de tempo controla tudo")
        self.sem_indice("A")
        self.drop("A", keep_card=False)
        g = self.g = Graf(self, one=r"I_\infty", ylab="I", ycol=GREEN)
        self.play(*g.show(), ap.oEB.animate.set_value(1), ap.oEL.animate.set_value(1), *self.show_l("EL"), run_time=T_MOVE)
        g.curve(lambda x: 1 - math.exp(-x), ap.tc, GREEN, 5)
        g.marker(lambda x: 1 - math.exp(-x), ap.tc, GREEN)
        self.an("Circuito, gráfico, campo magnético")
        self.rewind(ap.tc, g)
        tg = DashedLine(g.c2p(0, 0), g.c2p(1, 1), dash_length=0.08, color=VIOLET, stroke_width=3).set_z_index(5)
        self.an("No instante zero, a corrente ainda")
        self.caption("No início, $|\\mathcal E_L|=\\mathcal E_0$")
        self.show(E(r"t=0:\quad I=0,\quad \frac{dI}{dt}=\frac{\mathcal E_0}{L}", "I", r"\frac{dI}{dt}", r"\mathcal E_0", "L",
                    size=M_M), rt=1.4, wait=0)
        self.an("A taxa inicial de crescimento")
        self.play(Create(tg), run_time=T_IN)
        self.hold(T_READ)
        self.mark("c09_inicio")
        self.an("Agora anda exatamente uma constante")
        self.run(ap.tc, 1.0, 4.5)
        y1 = 1 - math.exp(-1)
        vl = Line(g.c2p(1, 0), g.c2p(1, 1.1)).set_stroke(VIOLET, 4).set_z_index(8)
        hl_ = DashedLine(g.c2p(0, y1), g.c2p(1, y1), dash_length=0.06, color=WHITE, stroke_width=2.5).set_z_index(8)
        self.an("Substituindo na solução")
        self.play(Create(vl), Create(hl_), run_time=0.8)
        self.caption("Em $t=\\tau$: 63% do valor final")
        self.show(E(r"I(\tau)=\left(1-e^{-1}\right)I_\infty\approx0{,}632\,I_\infty", r"I_\infty", size=M_M), rt=1.4, wait=0)
        self.mark("c09_tau")
        self.hold(T_READ)
        self.an("Depois de umas cinco constantes")
        self.play(vl.animate.set_stroke(opacity=0.35), run_time=0.4)
        self.run(ap.tc, 5.0, 5.0)
        v5 = Line(g.c2p(5, 0), g.c2p(5, 1.1)).set_stroke(VIOLET, 4).set_z_index(8)
        self.play(Create(v5), run_time=0.6)
        self.an("Na prática, o transiente acabou")
        self.caption("Regime: a fem some")
        self.show(E(r"t\approx5\tau:\quad I\approx0{,}99\,I_\infty,\quad \frac{dI}{dt}\to0,\quad \mathcal E_L\to0", "I", r"I_\infty",
                    r"\frac{dI}{dt}", r"\mathcal E_L", r"\tau", size=M_M), rt=1.4, wait=0)
        self.mark("c09_regime")
        self.an("Mas o campo magnético continua aceso")
        self.ring_hl(self.Wv_("left", XC, YT), 3.2, 1.2, MAG)
        self.hold(T_HOLD)
        self.play(FadeOut(VGroup(tg, vl, hl_, v5)), run_time=0.5)

    # ═══ C10 — B cresce, E induzido some (lateral → axial do mesmo solenoide) ══════════════════════════════
    def c10(self):
        ap, L = self.ap, self.L
        g = self.g
        self.an("Agora vamos olhar fisicamente")
        self.section("c10", "Olhando o solenoide de frente")
        self.limpa_slots()
        self.play(*g.hide(), ap.oEB.animate.set_value(0), ap.oEL.animate.set_value(0),
                  *self.hide_l("E0", "R", "I", "L", "B", "EL"), run_time=T_MOVE)
        g.drop()
        self.an("Giramos o solenoide")
        self.caption("Girando o solenoide")
        self.play(*self.view("axial"), ap.ang.animate.set_value(-PI / 2), run_time=3.2, rate_func=smooth)
        self.an("Os pontos magenta")
        self.play(*self.show_l("a"), run_time=T_IN)
        self.indice([(r"\mathbf B", "campo magnético: aqui, saindo da tela"), ("a", "raio do solenoide"),
                     ("r", "distância ao eixo"), (r"E_\phi", "campo elétrico induzido, em anéis")])
        self.hold(T_HOLD)
        self.mark("c10_axial")
        self.an("Dentro do solenoide ideal")
        self.sem_indice("A")
        self.show(E(r"B(t)=\mu_0\,n\,I(t)", "B(t)", "n", "I(t)", size=M_XL), rt=T_EQ, wait=0, note=defn(r"{n}:\ \text{espiras por metro}", "{n}", colors={"{n}": GEO}))
        self.an("Então, enquanto a corrente cresce")
        self.rewind(ap.tc)
        self.an("Só que, enquanto esse campo está mudando")
        self.caption("Surge um campo elétrico em anéis")
        self.play(ap.oEr.animate.set_value(1), ap.tc.animate.set_value(0.12), run_time=1.6, rate_func=linear)
        geo = {"{r}": GEO, "{a}": GEO, "{n}": GEO, "{a^2}": GEO}
        self.an("Dentro do solenoide, a intensidade")
        self.show(E(r"{r}<{a}:\quad E_\phi=-\frac{\mu_0\,{n}\,{r}}{2}\,\frac{dI}{dt}", "{r}", "{a}", r"E_\phi", "{n}", r"\frac{dI}{dt}",
                    size=M_M, colors=geo), slot="A", rt=1.4, wait=0)
        self.run(ap.tc, 0.3, 2.0)
        self.an("Fora, ela diminui")
        self.show(E(r"{r}>{a}:\quad E_\phi=-\frac{\mu_0\,{n}\,{a^2}}{2{r}}\,\frac{dI}{dt}", "{r}", "{a}", "{a^2}", r"E_\phi", "{n}",
                    r"\frac{dI}{dt}", size=M_M, colors=geo), slot="A", rt=1.4, wait=0)
        self.mark("c10_Ephi")
        self.run(ap.tc, 0.4, 1.5)
        self.an("E o sentido dos anéis")
        self.caption("Lenz: os anéis se opõem ao aumento de $\\mathbf B$")
        self.run(ap.tc, 0.6, 3.0)
        self.an("Agora olha o que acontece no final")
        self.caption("$\\mathbf B$ constante: os anéis somem")
        self.run(ap.tc, 5.0, T_RUN)
        self.an("Esse é um ponto importante")
        self.show(E(r"\text{regime:}\quad B\neq0,\quad E_{\rm ind}=0", "B", r"E_{\rm ind}", size=M_L), rt=1.4, wait=0)
        self.mark("c10_regime")
        self.hold(T_HOLD)

    # ═══ C11 — construir o campo custa energia ══════════════════════════════════════════════════════════════
    def c11(self):
        ap, L = self.ap, self.L
        self.an("Agora entra a segunda pergunta")
        self.section("c11", "Construir o campo custa energia")
        self.limpa_slots()
        self.play(ap.oEr.animate.set_value(0), *self.hide_l("a"), run_time=0.6)
        self.play(*self.view("left"), ap.ang.animate.set_value(ANG0), run_time=3.0, rate_func=smooth)
        self.play(*self.show_l("E0", "R", "I", "L", "B"), run_time=T_IN)
        self.an("Enquanto a corrente cresce, a fonte")
        self.rewind(ap.tc)
        self.run(ap.tc, 0.15, 1.5)
        self.an("A bateria fornece potência")
        self.caption("A bateria entrega potência")
        self.play(ap.oGauge.animate.set_value(1), ap.oGb.animate.set_value(1), *self.show_l("Gb"),
                  ap.tc.animate.set_value(0.4), run_time=2.4, rate_func=linear)
        self.an("Uma parte é dissipada")
        self.caption("Parte esquenta o resistor...")
        self.play(ap.oGr.animate.set_value(1), *self.show_l("Gr"), ap.tc.animate.set_value(0.8), run_time=2.4, rate_func=linear)
        self.an("E outra parte está associada")
        self.caption("...parte vai para o campo")
        self.play(ap.oGs.animate.set_value(1), *self.show_l("Gs"), ap.tc.animate.set_value(1.2), run_time=2.4, rate_func=linear)
        self.indice([(r"P_{\rm fonte}", "potência entregue pela bateria"), (r"P_{\rm Joule}", "potência dissipada no resistor"),
                     (r"\frac{dU_B}{dt}", "potência que vai para o campo")])
        self.run(ap.tc, 2.0, 2.5)
        self.mark("c11_medidores")
        self.an("Pegamos a equação da malha")
        self.sem_indice("A")
        self.caption("Multiplicando a malha por $I$")
        self.show(E(r"\mathcal E_0-L\frac{dI}{dt}=R\,I", r"\mathcal E_0", "L", r"\frac{dI}{dt}", "R", "I", size=M_XL), rt=1.6, wait=0)
        self.run(ap.tc, 2.6, 1.0)
        self.an("Porque tensão vezes corrente")
        self.show(E(r"\mathcal E_0\,I-L\,I\,\frac{dI}{dt}=R\,I^2", r"\mathcal E_0", "L", r"\frac{dI}{dt}", "R", "I", "I^2", size=M_XL),
                  ("I", "I^2"), rt=2.0, wait=0)
        self.mark("c11_vezesI")
        self.run(ap.tc, 3.0, 1.0)

    # ═══ C12 — a potência se divide ═════════════════════════════════════════════════════════════════════════
    def c12(self):
        ap, L = self.ap, self.L
        self.an("O primeiro termo é a potência")
        self.section("c12", "A potência se divide")
        self.show(E(r"\mathcal E_0\,I=I^2R+L\,I\,\frac{dI}{dt}", r"\mathcal E_0", "I", "I^2", "R", "L", r"\frac{dI}{dt}", size=M_XL),
                  rt=2.2, wait=0)
        H_ = self.slots["H"]["eq"]
        self.play(Indicate(glyphs(H_, r"\mathcal E_0"), color=CYAN, scale_factor=1.15), run_time=1.0)
        self.an("O segundo é corrente ao quadrado")
        self.play(Indicate(VGroup(glyphs(H_, "I^2"), glyphs(H_, "R")), color=HEAT, scale_factor=1.15), run_time=1.0)
        self.hold(1.5)
        self.an("E sobra o termo do indutor")
        self.play(Indicate(VGroup(glyphs(H_, "L"), glyphs(H_, r"\frac{dI}{dt}")), color=MAG, scale_factor=1.15), run_time=1.0)
        self.an("E esse termo esconde uma derivada")
        self.caption("Regra da cadeia")
        self.show(E(r"L\,I\,\frac{dI}{dt}=\frac{d}{dt}\left(\tfrac12\,L\,I^2\right)", "L", "I", r"\frac{dI}{dt}", "I^2", size=M_L),
                  slot="A", rt=T_EQ, wait=T_READ, note=(r"\frac{d}{dt}\left(I^2\right)=2I\,\frac{dI}{dt}", "I^2", r"\frac{dI}{dt}", "I"))
        self.an("Então o termo do indutor pode")
        self.show(E(r"\mathcal E_0\,I=I^2R+\frac{d}{dt}\left(\tfrac12\,L\,I^2\right)", r"\mathcal E_0", "I", "I^2", "R", "L",
                    size=M_XL), (r"\frac{dI}{dt}", None), src={("I^2", 1): glyphs(self.slots["A"]["eq"], "I^2")}, rt=2.2, wait=0)
        self.hold(1.5)
        self.an("Agora a conta ganha significado")
        self.drop("A", keep_card=False)
        self.caption("Cada termo é uma potência")
        self.show(E(r"P_{\rm fonte}=P_{\rm Joule}+\frac{dU_B}{dt}", r"P_{\rm fonte}", r"P_{\rm Joule}", r"\frac{dU_B}{dt}", size=64),
                  rt=2.2, wait=0, name="balanço de potência")
        self.mark("c12_balanco")
        self.hold(T_READ)
        self.an("E aí aparece uma das fórmulas")
        self.caption("A energia guardada no campo")
        self.show(E(r"U_B=\tfrac12\,L\,I^2", "U_B", "L", "I^2", size=M_XL), slot="A", rt=T_EQ, wait=0, name="energia magnética", note=(r"U_B:\ \text{energia guardada no campo}", "U_B"))
        self.mark("c12_UB")
        self.hold(T_HOLD)
        self.an("Vamos conferir durante a carga")
        self.caption("No início, campo; no fim, calor")
        self.rewind(ap.tc)
        self.an("Mas imediatamente depois")
        self.run(ap.tc, 0.6, 3.0)
        self.an("À medida que a corrente cresce")
        self.run(ap.tc, 2.5, 3.5)
        self.an("E no regime estacionário")
        self.run(ap.tc, 5.0, 0.6 * T_RUN)
        self.mark("c12_medidores")
        self.hold(T_READ)

    # ═══ C13 — onde está a energia? ═════════════════════════════════════════════════════════════════════════
    def c13(self):
        ap, L = self.ap, self.L
        self.an("Beleza")
        self.section("c13", "Onde está essa energia?")
        self.drop("H", keep_card=False)
        self.delcap()
        UB = self.slots["A"]["eq"]
        self.play(ap.oGauge.animate.set_value(0), *self.hide_l("Gb", "Gr", "Gs"), ap.tc.animate.set_value(6.0), run_time=T_IN)
        # o circuito apaga por inteiro ANTES do zoom (nada do circuito passa por trás do cartão de U_B)
        self.play(ap.oCirc.animate.set_value(0), ap.oFlow.animate.set_value(0), *self.hide_l("L", "B", "E0", "R", "I"), run_time=1.0)
        self.an("No fio")
        self.caption("No fio? No indutor? Ou no campo?")
        self.play(*self.view("soloc"), run_time=2.2)
        self.an("Ou no campo magnético espalhado")
        self.play(ap.oB.animate.set_value(1.35), run_time=1.5)
        self.mark("c13_pergunta")
        self.an("A fórmula que encontramos mistura")
        self.play(Indicate(UB, color=MAG, scale_factor=1.08), run_time=1.2)
        self.hold(T_HOLD)

    # ═══ C14 — densidade de energia ═════════════════════════════════════════════════════════════════════════
    def c14(self):
        ap, L = self.ap, self.L
        self.an("Mas dá para reescrever")
        self.section("c14", "O volume dentro do solenoide")
        self.limpa_slots()
        self.an("Vamos usar o solenoide justamente")
        self.play(*self.view("solo"), ap.oB.animate.set_value(0.6), run_time=T_MOVE)
        self.an("Temos uma área de seção")
        self.caption("A seção: área $A$")
        self.play(ap.oAe.animate.set_value(1), *self.show_l("A"), run_time=1.2)
        self.an("Temos um comprimento")
        self.caption("O comprimento: $\\ell$")
        self.play(ap.oVol.animate.set_value(1), *self.show_l("ell"), run_time=1.2)
        self.an("Quando essa área varre")
        self.caption("A seção varre o volume")
        self.play(ap.oSweep.animate.set_value(1), run_time=3.5, rate_func=linear)
        self.an("Área vezes comprimento")
        self.show(E(r"V=A\,\ell", "V", "A", r"\ell", size=M_XL), slot="A", src={("A", 0): L["A"], (r"\ell", 0): L["ell"]},
                  rt=1.4, wait=0, name="volume interno")
        self.mark("c14_volume")
        self.hold(T_READ)
        self.an("Para o solenoide ideal")
        self.play(ap.oSweep.animate.set_value(0), ap.oB.animate.set_value(1.0), run_time=1.0)
        self.indice([("n", "espiras por metro"), (r"\mu_0", "permeabilidade do vácuo"), ("A", "área da seção"),
                     (r"\ell", "comprimento do solenoide")])
        self.caption("No solenoide: $B=\\mu_0 n I$ e $L=\\mu_0 n^2 A\\ell$")
        self.show(E(r"U_B=\tfrac12\,L\,I^2", "U_B", "L", "I^2", size=M_XL), rt=T_EQ, wait=T_READ)
        self.an("Substituímos a autoindutância")
        self.caption("Trocando $L$")
        self.show(E(r"U_B=\tfrac12\,\mu_0\,n^2A\ell\,I^2", "U_B", "n^2", r"A\ell", "I^2", size=M_XL), ("L", None), rt=T_EQ, wait=1.0)
        self.an("E agora olha o agrupamento")
        self.caption("Aparece o campo $B=\\mu_0 n I$")
        self.show(E(r"U_B=\frac{\left(\mu_0\,n\,I\right)^2}{2\mu_0}\,A\ell", "U_B", "n", "I", r"A\ell", size=M_XL),
                  ("n^2", "n"), ("I^2", "I"), rt=T_EQ, wait=0)
        self.an("é exatamente o campo magnético")
        self.play(Indicate(VGroup(glyphs(self.slots["H"]["eq"], "n"), glyphs(self.slots["H"]["eq"], "I")), color=MAG, scale_factor=1.15), run_time=1.0)
        self.an("Então toda aquela expressão")
        self.show(E(r"U_B=\frac{B^2}{2\mu_0}\,A\ell", "U_B", "B^2", r"A\ell", size=M_XL), ("n", None), ("I", None), rt=T_EQ, wait=0)
        self.an("dividido por duas vezes")
        self.sem_indice("A")
        self.an("multiplicado pelo volume")
        self.caption("$A\\ell$ é o volume")
        self.play(ap.oSweep.animate.set_value(1), run_time=0.7)
        self.show(E(r"U_B=\frac{B^2}{2\mu_0}\,V", "U_B", "B^2", "V", size=M_XL), (r"A\ell", "V"), rt=1.3, wait=0)
        self.an("Então, no vácuo, a energia por unidade")
        self.play(ap.oSweep.animate.set_value(0), run_time=0.6)
        self.caption("Energia por volume")
        self.show(E(r"u_B=\frac{U_B}{V}=\frac{B^2}{2\mu_0}", "u_B", "U_B", "V", "B^2", size=M_XL), rt=T_EQ, wait=0,
                  name="densidade de energia magnética", note=(r"u_B:\ \text{energia por unidade de volume}", "u_B"))
        self.an("E agora olha o que aconteceu")
        self.play(Indicate(glyphs(self.slots["H"]["eq"], "B^2"), color=MAG, scale_factor=1.15), run_time=1.2)
        self.an("É nesse sentido que a energia")
        self.caption("A energia mora no campo")
        self.mark("c14_uB")
        self.hold(T_HOLD)

    # ═══ C15 — generalização ════════════════════════════════════════════════════════════════════════════════
    def cells(self):
        xs = np.arange(XS0 - 1.6, XS1 + 1.61, 0.3)
        ys = np.arange(YT - 1.5, YT + 1.51, 0.3)
        rr, pp = np.meshgrid(np.linspace(0.04, A_R, 9), np.linspace(0, 2 * PI, 28, endpoint=False))
        dA = (A_R / 9) * (2 * PI / 28) * rr.ravel()
        qy, qz = (rr * np.cos(pp)).ravel(), (rr * np.sin(pp)).ravel()

        def Hf(x, y):
            h = np.zeros(2)
            for xe, sg in ((XS1, 1.0), (XS0, -1.0)):
                d = np.stack([x - xe + 0 * qy, (y - YT) - qy, -qz], 1)
                r3 = np.linalg.norm(d, axis=1) ** 3 + 1e-9
                h += sg * np.sum((d[:, :2].T * dA / r3), axis=1) / (4 * PI)
            return h
        b0 = Hf(XC, YT) + np.array([1.0, 0.0])
        g = VGroup()
        s = VIEW["cells"][0]
        for x in xs:
            for y in ys:
                inside = XS0 < x < XS1 and abs(y - YT) < A_R
                b = Hf(x, y) + (np.array([1.0, 0.0]) if inside else 0)
                v = float(np.dot(b, b) / np.dot(b0, b0))
                if v < 0.004:
                    continue
                X, Y, _ = self.ap.proj(x, y, 0.0, ANG0)
                g.add(Square(0.27 * s).move_to(self.Wv_("cells", X, Y)).set_fill(MAG, min(0.7, 0.7 * v ** 0.75)).set_stroke(width=0))
        return g.set_z_index(0)

    def c15(self):
        ap, L = self.ap, self.L
        self.an("E no vácuo essa ideia")
        self.section("c15", "Vale para qualquer campo")
        self.drop("A", keep_card=False)
        self.play(*self.view("cells"), ap.oVol.animate.set_value(0), ap.oAe.animate.set_value(0), *self.hide_l("A", "ell"),
                  run_time=T_MOVE)
        cg = self.cells()
        self.an("Num solenoide real")
        self.caption("Campo real: não uniforme")
        self.play(LaggedStart(*[FadeIn(c) for c in cg], lag_ratio=0.004), ap.oB.animate.set_value(0.4), run_time=2.5)
        self.hold(T_READ)
        pk = self.Wv_("cells", XS1 + 0.6, YT + 0.6)
        dt_ = Square(0.27 * VIEW["cells"][0]).move_to(pk).set_stroke(WHITE, 3).set_fill(opacity=0).set_z_index(8)
        dl = self.lab(r"d\tau", pk + np.array([0.35, 0.3, 0]), r"d\tau", size=M_S)
        self.an("Pegamos um pedacinho pequeno")
        self.play(Create(dt_), FadeIn(dl), run_time=T_IN)
        self.an("Calculamos a energia naquele")
        self.caption("Cada $d\\tau$ guarda sua parte")
        self.show(E(r"dU_B=\frac{B^2}{2\mu_0}\,d\tau", "dU_B", "B^2", r"d\tau", size=M_XL), slot="A",
                  src={(r"d\tau", 0): dl}, rt=T_EQ, wait=T_READ, note=(r"d\tau:\ \text{elemento de volume}", r"d\tau"))
        self.an("E somamos todos os pedacinhos")
        self.caption("Somando todos os pedaços")
        self.play(LaggedStart(*[c.animate.set_stroke(WHITE, 1.2, 0.6) for c in cg], lag_ratio=0.003), run_time=2.4)
        self.an("No limite contínuo")
        self.show(E(r"U_B=\frac{1}{2\mu_0}\int B^2\,d\tau", "U_B", "B^2", r"d\tau", size=M_XL), slot="H",
                  src={("B^2", 0): glyphs(self.slots["A"]["eq"], "B^2"), (r"d\tau", 0): glyphs(self.slots["A"]["eq"], r"d\tau")},
                  rt=2.2, wait=0, name="energia do campo magnético")
        self.play(cg.animate.set_stroke(width=0), run_time=0.6)
        self.mark("c15_integral")
        self.hold(T_HOLD)
        self.an("Agora temos uma descrição espacial")
        self.play(FadeOut(VGroup(cg, dt_, dl)), run_time=0.8)
        self.hold(1.0)

    # ═══ C16 — comutação para descarga ══════════════════════════════════════════════════════════════════════
    def c16(self):
        ap, L = self.ap, self.L
        self.an("Vamos fazer o teste")
        self.section("c16", "Agora: tirar a bateria sem abrir o circuito")
        self.limpa_slots()
        ap.tc.set_value(6.0)
        self.an("A corrente já chegou ao regime")
        self.play(*self.view("left"), ap.oCirc.animate.set_value(1), ap.oB.animate.set_value(1), ap.oFlow.animate.set_value(1),
                  *self.show_l("L", "B", "I", "E0", "R"), run_time=T_MOVE)
        self.an("Existe energia armazenada")
        self.caption("O campo guarda $U_{B,0}$")
        self.show(E(r"U_{B,0}=\tfrac12\,L\,I_0^2", "U_{B,0}", "L", "I_0^2", size=M_XL), rt=T_EQ, wait=0, note=(r"I_0:\ \text{corrente no instante da troca}", "I_0"))
        self.hold(T_READ)
        self.an("Mas não vamos simplesmente abrir")
        self.caption("Abrir a chave? A corrente não pode saltar")
        self.hold(1.5)
        self.an("o modelo exigiria uma variação enorme")
        self.ring_hl(self.Wv_("left", XB, YT), 1.0, 1.0, HEAT)
        self.show(E(r"\frac{dI}{dt}\to\infty\ \Rightarrow\ |\mathcal E_L|\to\infty", r"\frac{dI}{dt}", r"\mathcal E_L", size=M_M),
                  slot="A", rt=1.4, wait=0)
        self.hold(T_READ)
        self.an("Em vez disso, a chave comuta")
        self.drop("A", keep_card=False)
        self.caption("Um caminho só pelo resistor")
        self.play(ap.oByp.animate.set_value(1), run_time=T_EQ)
        self.ring_hl(self.Wv_("left", XB, 0), 0.7, 2.4)
        self.an("A bateria sai")
        self.caption("A chave vai de a para b")
        self.play(ap.sw.animate.set_value(SW_B), run_time=1.4)
        ap.mode = "discharge"
        ap.td.set_value(0)
        self.play(ap.oBat.animate.set_value(0.15), *self.hide_l("E0"), run_time=T_EQ)
        self.an("E olha a corrente no instante")
        self.caption("A corrente continua, sem salto")
        self.mark("c16_troca")
        self.hold(T_READ)

    # ═══ C17 — o indutor sustenta a corrente ════════════════════════════════════════════════════════════════
    def c17(self):
        ap, L = self.ap, self.L
        self.an("Agora a equação da malha não tem")
        self.section("c17", "O indutor sustenta a corrente")
        self.caption("A mesma malha, sem bateria")
        self.limpa_slots()
        self.an("Sobra autoindutância vezes")
        self.show(E(r"L\frac{dI}{dt}+R\,I=0", "L", r"\frac{dI}{dt}", "R", "I", size=M_XL), rt=T_EQ, wait=1.0)
        self.an("A solução é um decaimento")
        self.show(E(r"I(t)=I_0\,e^{-t/\tau}", "I(t)", "I_0", r"-t/\tau", size=M_XL), ("I", "I(t)"), rt=T_EQ, wait=0,
                  name="corrente na descarga", note=(r"\tau=\frac{L}{R}", r"\tau", "L", "R"))
        g = self.g = Graf(self, one="I_0", ylab="I", ycol=GREEN)
        self.an("A corrente começa no valor inicial")
        self.play(*g.show(), run_time=T_IN)
        g.curve(lambda x: math.exp(-x), ap.td, GREEN, 5)
        g.marker(lambda x: math.exp(-x), ap.td, GREEN)
        self.run(ap.td, 0.3, 2.0)
        self.an("E olha a força eletromotriz do indutor")
        self.caption("A fem inverte e sustenta a corrente")
        self.play(ap.oEL.animate.set_value(1), *self.show_l("EL"), ap.td.animate.set_value(0.45), run_time=T_IN, rate_func=linear)
        self.mark("c17_fem")
        self.an("Então a força eletromotriz muda de sentido")
        self.caption("Corrente caindo: fem a favor")
        self.run(ap.td, 0.9, 3.0)
        self.an("Lembra do amigo do contra")
        self.run(ap.td, 1.4, 3.0)
        self.an("Só que agora não existe bateria")
        self.run(ap.td, 5.0, T_RUN)
        self.mark("c17_fim")
        self.hold(T_READ)

    # ═══ C18 — campo vira calor ═════════════════════════════════════════════════════════════════════════════
    def c18(self):
        ap, L = self.ap, self.L
        self.an("A corrente cai como uma exponencial")
        self.section("c18", "O campo vira calor")
        g = self.g
        self.limpa_slots()
        self.play(*g.hide(), run_time=T_IN)
        g.drop()
        gU = self.gU = Graf(self, center=(3.95, 1.15), h=1.25, one="U_{B,0}", tlab=False)
        gP = self.gP = Graf(self, center=(3.95, -1.35), h=1.25, one=r"R I_0^2")
        eU = E(r"U_B(t)=U_{B,0}\,e^{-2t/\tau}", "U_B(t)", "U_{B,0}", r"-2t/\tau", size=M_M).move_to([3.95, 2.25, 0])
        eP = E(r"P_R(t)=R\,I_0^2\,e^{-2t/\tau}", "P_R(t)", "R", "I_0^2", r"-2t/\tau", size=M_M).move_to([3.95, -0.22, 0])
        self.an("Como a energia magnética depende")
        self.play(*gU.show(), FadeIn(eU), run_time=T_EQ)
        self.an("A potência dissipada no resistor também")
        self.play(*gP.show(), FadeIn(eP), run_time=T_EQ)
        for gg, col in ((gU, MAG), (gP, HEAT)):
            gg.curve(lambda x: math.exp(-2 * x), ap.td, col, 5)
            gg.marker(lambda x: math.exp(-2 * x), ap.td, col)
        self.hold(1.0)
        self.an("O campo enfraquece")
        self.rewind(ap.td, gP)
        self.caption("O campo perde, o resistor recebe")
        self.run(ap.td, 5.0, 4.5)
        self.mark("c18_curvas")
        self.hold(1.0)
        gP.area(lambda x: math.exp(-2 * x), ap.td, HEAT, 0.45)
        self.an("E potência é energia por unidade")
        self.caption("A área sob $P_R$ é o calor")
        self.rewind(ap.td, gP)
        self.an("Então a energia total transformada")
        self.run(ap.td, 5.0, 5.0)
        qq = E(r"Q_R(t)=\int_0^t P_R\,dt'", "Q_R(t)", "P_R", size=M_M).move_to([3.95, -2.95, 0])
        self.an("Essa área é a integral")
        self.play(FadeIn(qq), run_time=T_IN)
        self.mark("c18_area")
        self.hold(T_READ)
        self.an("Agora podemos fazer a conta final")
        self.play(FadeOut(VGroup(eU, eP, qq)), *gU.hide(), *gP.hide(), run_time=T_IN)
        gU.drop()
        gP.drop()

    # ═══ C19 — a conservação fecha ══════════════════════════════════════════════════════════════════════════
    def c19(self):
        ap, L = self.ap, self.L
        self.an("Quanto de calor aparece")
        self.section("c19", "Quanto calor no total?")
        self.relayout("alg", rt=0.6)
        self.an("Integramos a potência dissipada")
        self.caption("O calor total")
        self.show(E(r"E_{\rm calor}=\int_0^\infty I^2R\,dt", r"E_{\rm calor}", "I^2", "R", "dt", size=M_XL), rt=T_EQ, wait=1.0)
        self.an("Substituímos a corrente exponencial")
        self.show(E(r"I=I_0\,e^{-t/\tau}", "I", "I_0", r"-t/\tau", size=M_M), slot="A", rt=1.2, wait=0)
        self.caption("Substituindo a corrente")
        self.show(E(r"E_{\rm calor}=\int_0^\infty R\,I_0^2\,e^{-2t/\tau}\,dt", r"E_{\rm calor}", "R", "I_0^2", r"-2t/\tau", "dt",
                    size=M_XL), ("I^2", "I_0^2"), rt=2.2, wait=0)
        self.an("A integral que sobra vale")
        self.caption("A integral vale $\\tau/2$")
        self.show(E(r"E_{\rm calor}=R\,I_0^2\,\frac{\tau}{2}", r"E_{\rm calor}", "R", "I_0^2", r"\frac{\tau}{2}", size=M_XL),
                  (r"-2t/\tau", None), ("dt", None), rt=2.2, wait=T_READ)
        self.an("Agora substituímos a constante de tempo")
        self.show(E(r"\tau=\frac{L}{R}", r"\tau", "L", "R", size=M_M), slot="A", rt=1.2, wait=0)
        self.caption("Usando $\\tau=L/R$")
        self.show(E(r"E_{\rm calor}=R\,I_0^2\,\frac{L}{2R}", r"E_{\rm calor}", "R", "I_0^2", "L", size=M_XL),
                  (r"\frac{\tau}{2}", None), src={("L", 0): glyphs(self.slots["A"]["eq"], "L"),
                                                  ("R", 1): glyphs(self.slots["A"]["eq"], "R")}, rt=2.2, wait=0)
        H_ = self.slots["H"]["eq"]
        st = VGroup(*[Line(gl.get_corner(DL) + np.array([-0.04, -0.04, 0]), gl.get_corner(UR) + np.array([0.04, 0.04, 0]),
                           color=HEAT, stroke_width=5) for gl in (glyphs(H_, "R", 0), glyphs(H_, "R", 1))]).set_z_index(30)
        self.an("A resistência cancela")
        self.caption("O $R$ cancela")
        self.play(Create(st), run_time=0.8)
        self.hold(0.6)
        self.an("E sobra meio vezes")
        self.play(FadeOut(st), glyphs(H_, "R").animate.set_opacity(0), run_time=0.7)
        self.show(E(r"E_{\rm calor}=\tfrac12\,L\,I_0^2=U_{B,0}", r"E_{\rm calor}", "L", "I_0^2", "U_{B,0}", size=M_XL),
                  ("R", None, 0), ("R", None, 1), rt=2.2, wait=0, name="toda a energia do campo vira calor")
        self.drop("A", keep_card=False)
        self.mark("c19_total")
        self.hold(T_READ)
        self.an("E a resistência desapareceu")
        self.caption("$R$ só decide o ritmo")
        self.hold(1.5)
        self.an("Resistência maior significa")
        self.show(E(r"\tau=\frac{L}{R}", r"\tau", "L", "R", size=M_L), slot="A", rt=1.2, wait=0, note=defn(r"{R}\uparrow\ \Longrightarrow\ \tau\downarrow", "{R}", r"\tau", colors={"{R}": WHITE}))
        self.hold(T_READ)
        # U_B(t) e Q_R(t): uma cai, a outra sobe, a soma fica
        self.an("E dá para ver a conservação")
        self.drop("A", keep_card=False)
        self.relayout("split", rt=0.8)
        self.caption("A soma fica constante")
        self.show(E(r"U_B(t)+Q_R(t)=U_{B,0}", "U_B(t)", "Q_R(t)", "U_{B,0}", size=M_XL), rt=2.0, wait=0,
                  name="conservação", note=(r"Q_R:\ \text{calor acumulado no resistor}", "Q_R"))
        g = self.g = Graf(self, one="U_{B,0}")
        self.an("A energia magnética diminui")
        self.play(*g.show(), run_time=T_IN)
        g.curve(lambda x: math.exp(-2 * x), ap.td, MAG, 5)
        g.curve(lambda x: 1 - math.exp(-2 * x), ap.td, HEAT, 5)
        g.curve(lambda x: 1.0, ap.td, WHITE, 3)
        g.marker(lambda x: math.exp(-2 * x), ap.td, MAG)
        g.marker(lambda x: 1 - math.exp(-2 * x), ap.td, HEAT)
        self.rewind(ap.td, g)
        self.run(ap.td, 5.0, 1.2 * T_RUN)
        self.mark("c19_conservacao")
        self.hold(T_HOLD)

    # ═══ C20 — síntese e Maxwell ════════════════════════════════════════════════════════════════════════════
    def c20(self):
        ap, L = self.ap, self.L
        g = self.g
        self.an("Então agora dá para responder")
        self.section("c20", "Síntese")
        self.limpa_slots()
        self.play(*g.hide(), ap.oFlow.animate.set_value(0), run_time=T_IN)
        g.drop()
        ap.mode = "charge"
        ap.tc.set_value(0)
        self.play(ap.sw.animate.set_value(SW_A), ap.oBat.animate.set_value(1), ap.oByp.animate.set_value(0), *self.show_l("E0"),
                  run_time=T_SW)
        self.an("Porque mudar a corrente")
        self.play(ap.oFlow.animate.set_value(1), run_time=0.4)
        self.caption("O indutor reage à mudança")
        self.an("E, pela lei de Faraday")
        self.show(E(r"\mathcal E_L=-L\,\frac{dI}{dt}", r"\mathcal E_L", "L", r"\frac{dI}{dt}", size=M_L), rt=1.4, wait=0)
        self.an("Com uma fonte de tensão finita")
        self.run(ap.tc, 1.5, 3.0)
        self.an("E, ao mesmo tempo, construir")
        self.caption("A energia fica no campo")
        self.an("Essa energia pode ser escrita")
        self.show(E(r"U_B=\tfrac12\,L\,I^2", "U_B", "L", "I^2", size=M_L), slot="A", rt=1.4, wait=0)
        self.run(ap.tc, 4.0, 3.0)
        self.an("No vácuo, ela pode ser vista")
        self.caption("Densidade $B^2/2\\mu_0$")
        self.show(E(r"u_B=\frac{B^2}{2\mu_0}", "u_B", "B^2", size=M_L), rt=1.4, wait=0)
        self.play(ap.oB.animate.set_value(1.4), run_time=0.8)
        self.play(ap.oB.animate.set_value(1.0), run_time=0.8)
        self.an("E quando retiramos a bateria")
        self.caption("E volta inteira como calor")
        self.play(ap.oByp.animate.set_value(1), run_time=0.5)
        self.play(ap.sw.animate.set_value(SW_B), run_time=T_SW)
        ap.mode = "discharge"
        ap.td.set_value(0)
        self.an("O campo diminui")
        self.play(ap.oBat.animate.set_value(0.15), ap.td.animate.set_value(1.5), run_time=3.0, rate_func=linear)
        self.an("E a energia magnética reaparece")
        self.show(E(r"E_{\rm calor}=U_{B,0}", r"E_{\rm calor}", "U_{B,0}", size=M_L), slot="A", rt=1.4, wait=0)
        self.run(ap.td, 5.0, 4.0)
        self.mark("c20_sintese")
        self.hold(T_READ)
        # o mesmo circuito, com um capacitor no lugar do solenoide
        self.an("Só que a eletrodinâmica")
        self.section("c20b", "Uma conta pendente")
        self.limpa_slots()
        self.play(ap.oFlow.animate.set_value(0), run_time=0.4)
        self.an("Troca agora o indutor")
        self.caption("E se, no lugar do solenoide, houver um capacitor?")
        self.play(ap.oCap.animate.set_value(1), ap.oByp.animate.set_value(0), ap.oBat.animate.set_value(1), ap.oEL.animate.set_value(0),
                  ap.oCoilI.animate.set_value(0), ap.sw.animate.set_value(SW_OPEN), *self.show_l("E0", "C"),
                  *self.hide_l("L", "B", "EL"), run_time=T_MOVE)
        ap.mode = "cap"
        ap.tc.set_value(0)
        self.an("A corrente percorre os fios")
        self.play(ap.sw.animate.set_value(SW_A), run_time=T_SW)
        self.caption("A corrente chega às placas...")
        self.play(ap.oFlow.animate.set_value(1), ap.tc.animate.set_value(0.4), run_time=2.8, rate_func=linear)
        self.an("Mas carga nenhuma atravessa")
        self.caption("...mas não atravessa")
        self.play(*self.show_l("gap"), ap.tc.animate.set_value(0.6), run_time=T_IN, rate_func=linear)
        self.run(ap.tc, 0.8, T_READ)
        self.an("Agora desenha um mesmo contorno")
        self.caption("Lei de Ampère em volta do fio")
        self.play(*self.hide_l("gap"), ap.oAmp.animate.set_value(1), ap.tc.animate.set_value(0.95), run_time=T_EQ, rate_func=linear)
        self.an("Pela lei de Ampère original")
        self.show(E(r"\oint\mathbf B\cdot d\boldsymbol\ell=\mu_0\,I_{\rm enc}", r"\mathbf B\cdot d\boldsymbol\ell", r"I_{\rm enc}",
                    size=M_L), rt=1.6, wait=0, name="lei de Ampère", note=(r"I_{\rm enc}:\ \text{corrente que atravessa a superfície}", r"I_{\rm enc}"))
        self.run(ap.tc, 1.1, T_READ)
        self.an("Se escolhemos uma superfície")
        self.caption("Disco $S_1$: o fio atravessa")
        self.play(ap.oS1.animate.set_value(1), *self.show_l("S1"), ap.tc.animate.set_value(1.25), run_time=T_EQ, rate_func=linear)
        self.show(E(r"S_1:\ I_{\rm enc}=I", r"I_{\rm enc}", "I", size=M_L, colors={"S_1": VIOLET}), slot="A", rt=1.4, wait=0)
        self.an("Mas eu posso escolher outra")
        self.caption("Bolsa $S_2$: nada atravessa")
        self.play(ap.oS2.animate.set_value(1), *self.show_l("S2"), ap.tc.animate.set_value(1.5), run_time=T_EQ, rate_func=linear)
        self.an("Ali não existe corrente")
        self.show(E(r"S_1:\ I_{\rm enc}=I\qquad S_2:\ I_{\rm enc}=0", r"I_{\rm enc}", "I", size=M_L,
                    colors={"S_1": VIOLET}), slot="A", rt=1.4, wait=0)
        self.mark("c20_ampere")
        self.run(ap.tc, 1.8, T_READ)
        self.an("Mesmo contorno")
        self.caption("O mesmo contorno, duas respostas")
        self.run(ap.tc, 2.1, T_READ)
        self.an("Então fica a pergunta")
        self.delcap()
        self.limpa_slots()
        q = VGroup(txt("Como o campo magnético sabe", 34, WHITE), txt("que o circuito continua?", 34, WHITE)).arrange(DOWN, buff=0.16)
        q.move_to([3.95, 0.5, 0])
        self.an("como o campo magnético sabe")
        self.play(FadeIn(q, shift=0.1 * UP), ap.tc.animate.set_value(2.4), run_time=1.2, rate_func=linear)
        self.mark("c20_pergunta")
        self.run(ap.tc, 3.0, T_HOLD)
        # encerramento (docs/padrao_video_longo.md): tela limpa, logo com anéis, inscreva-se, prévia do próximo vídeo
        self.an("Se essas conexões ajudaram")
        self.play(*[FadeOut(m) for m in self.mobjects if not isinstance(m, ValueTracker) and not m.get_family_updaters()],
                  ap.oAll.animate.set_value(0), *self.hide_l("C", "S1", "S2", "E0", "R", "I"), run_time=T_MOVE)
        for m in list(self.mobjects):
            m.clear_updaters()
        self.clear()
        oc = np.array([0, 0.7, 0])
        rings = VGroup(*[DashedVMobject(Circle(radius=r, arc_center=oc), num_dashes=max(12, int(14 * r)), dashed_ratio=0.6)
                         .set_stroke(VIOLET, 3.5, 0.16) for r in (2.0, 3.0, 4.0)])
        for i, r_ in enumerate(rings):
            r_.add_updater(lambda m, dt, sg=(1 if i % 2 == 0 else -1) * (0.06 - 0.01 * i): m.rotate(sg * dt, about_point=oc))
        logo = ImageMobject(str(LOGO_H)).set_width(6.0).move_to(oc + np.array([0, 0.4, 0]))
        msg = txt("Inscreva-se para acompanhar os próximos vídeos", 28, WHITE, 0.9).move_to(oc + np.array([0, -1.0, 0]))
        hook = txt("Como o campo magnético sabe que o circuito continua?", 28, WHITE).move_to(oc + np.array([0, -1.85, 0]))
        nx1 = txt("Próximo vídeo: corrente de deslocamento", 26, WHITE, 0.95).move_to(oc + np.array([0, -1.85, 0]))
        nx2 = txt("Maxwell completa a lei de Ampère", 26, CYAN).move_to(oc + np.array([0, -2.4, 0]))
        for t in (msg, hook, nx1, nx2):
            if t.width > 12.0:
                t.scale_to_fit_width(12.0)
        self.play(LaggedStart(*[FadeIn(r_, scale=0.85) for r_ in rings], lag_ratio=0.3), FadeIn(logo, scale=0.92), run_time=1.8)
        self.an("se inscreve no Parallax Lab")
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=1.0)
        self.play(FadeIn(hook, shift=0.1 * UP), run_time=1.0)
        self.hold(2.0)
        self.play(FadeOut(hook), run_time=0.6)
        self.an("No próximo, a gente vai descobrir")
        self.play(FadeIn(nx1, shift=0.1 * UP), run_time=0.8)
        self.an("e por que essa correção")
        self.play(FadeIn(nx2, shift=0.1 * UP), run_time=0.8)
        w = DashedVMobject(Circle(radius=1.6, arc_center=oc), num_dashes=24, dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.35)
        self.an("Valeu, pessoal")
        self.play(w.animate.scale(2.6, about_point=oc).set_stroke(opacity=0.0), run_time=2.6)
        self.remove(w)
        self.mark("c20_cta")
        self.hold(1.0)


PASTA = Path(__file__).resolve().parent
