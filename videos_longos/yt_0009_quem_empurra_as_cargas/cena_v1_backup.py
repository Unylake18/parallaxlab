"""yt_0009 — Quem empurra as cargas? (campo elétrico, Lei de Ohm, cargas superficiais e FEM).

Preview visual silencioso, 960×540 / 15 fps. Paleta e gramática da série Magnetostática (yt_0005/yt_0006):
E e energia ciano · J, I e ∇·J verde · carga azul · força (f, f_s) azul-claro FC · geometria violeta · matéria STEEL.

Fio condutor: UM circuito recorrente (fonte + fio + resistor) que ganha camadas: E → J → cargas superficiais → f_s.
"""
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from manim import (
    AnimationGroup, Arrow, Circle, DashedVMobject, DoubleArrow, Ellipse, FadeIn, FadeOut, ImageMobject, Indicate,
    LaggedStart, Line, MathTex, Polygon, Rectangle, ReplacementTransform, RoundedRectangle, Scene, SurroundingRectangle,
    TransformFromCopy, TransformMatchingTex, VGroup, VMobject, ValueTracker, Write, always_redraw, linear, smooth,
    there_and_back, UP, DOWN, LEFT, RIGHT, UL, UR, ORIGIN, CapStyleType,
)
from MF_Tools import TransformByGlyphMap

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import screen_text  # noqa: E402

# ── paleta (idêntica à da Magnetostática) ───────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR        # E, V, ℰ, energia/potência
BLUE = "#267BFF"            # carga positiva
BLUE_L = "#7FB2FF"          # carga negativa/elétron, ρ, painéis, volume de controle
STEEL = "#7A8696"           # matéria condutora
VIOLET = "#9C8CFF"          # geometria (L, A) e velocidade (v_d)
FC = "#5AA2FF"              # força por unidade de carga (f, f_s)
GREEN = "#3FE08B"           # corrente (I, J, ∇·J)
PANEL = "#0E2A52"
DIM = "#8FA3C4"

T_BODY, T_NOTE, T_CAP, T_HEAD = 30, 26, 24, 36
M_XL, M_L, M_M, M_S = 54, 48, 40, 32

TOKCOL = {}
for _t in ("I", "J", r"\mathbf J", r"I_{\rm entra}", r"I_{\rm sai}", r"\nabla\cdot\mathbf J"):
    TOKCOL[_t] = GREEN
for _t in ("E", "V", r"\mathbf E", r"\mathcal E", "P", "p", r"P_{\rm fonte}", r"P_{\rm dissipada}", r"\Delta V"):
    TOKCOL[_t] = CYAN
for _t in (r"\mathbf f", r"\mathbf f_s"):
    TOKCOL[_t] = FC
for _t in (r"\rho", r"\frac{\partial\rho}{\partial t}", "Q", r"\frac{dQ}{dt}"):
    TOKCOL[_t] = BLUE_L
for _t in ("A", "L", r"\mathbf v_d"):
    TOKCOL[_t] = VIOLET


def txt(s, size=T_BODY, color=WHITE, opacity=1.0):
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(opacity)


# ── equações ────────────────────────────────────────────────────────────────────────────────────────────────
def M(*parts, size=M_M, width=None):
    """MathTex por partes, cada parte na cor da grandeza (serve a TransformMatchingTex)."""
    m = MathTex(*parts, font_size=size, color=WHITE)
    for part, sub in zip(parts, m.submobjects):
        c = TOKCOL.get(part)
        if c:
            sub.set_color(c)
    if width and m.width > width:
        m.scale_to_fit_width(width)
    return m


def _build(tex, iso, size, width):
    iso = tuple(dict.fromkeys(iso))
    m = MathTex(tex, font_size=size, color=WHITE, substrings_to_isolate=list(iso))
    leaves = list(m[0].submobjects)
    pos = {id(g): i for i, g in enumerate(leaves)}
    tok = {}
    for t, sid in getattr(m, "matched_strings_and_ids", []):
        if not sid.endswith("substring") or t not in iso:
            continue
        idx = sorted(pos[id(g)] for g in m.id_to_vgroup_dict[sid].family_members_with_points() if id(g) in pos)
        if idx:
            tok.setdefault(t, []).append(idx)
    for t, occs in tok.items():
        c = TOKCOL.get(t)
        if c:
            for idx in occs:
                for i in idx:
                    leaves[i].set_color(c)
    if width and m.width > width:
        m.scale_to_fit_width(width)
    m.tok, m.tex = tok, tex
    return m


_EC = {}


def EQ(tex, *iso, size=M_M, width=None):
    """MathTex de string única com tokens isolados (para TransformByGlyphMap)."""
    key = (tex, iso, size, width)
    if key not in _EC:
        _EC[key] = _build(tex, iso, size, width)
    c = _EC[key].copy()
    c.tok, c.tex = _EC[key].tok, tex
    return c


def glyphs(m, tok, occ=None):
    lst = m.tok[tok]
    sel = lst if occ is None else [lst[occ]]
    return VGroup(*[m[0][i] for idx in sel for i in idx])


def _occ(m, tok, o):
    if tok not in m.tok:
        raise KeyError(f"token {tok!r} ausente em {m.tex!r} (tem {list(m.tok)})")
    lst = m.tok[tok]
    return lst if o is None else [lst[o]]


def _sig(g):
    w, h = g.width, g.height
    if h < 0.045 and w > 0.12:
        return ("bar",)
    return (len(g.points), round(w / max(h, 1e-3), 1))


def gmap(A, B, *pairs, **kw):
    """TransformByGlyphMap A→B por termos. pairs: (tokA, tokB[, occA[, occB]]) leva; (tokA, None[, occ]) remove.
    O restante é pareado automaticamente (mesmo token, na ordem; depois estrutura por assinatura)."""
    entries, ua, ub = [], set(), set()
    for p in pairs:
        ta, tb = p[0], p[1]
        oa = p[2] if len(p) > 2 else None
        ob = p[3] if len(p) > 3 else None
        if tb is None:
            for lst in _occ(A, ta, oa):
                entries.append((list(lst), []))
                ua.update(lst)
            continue
        la, lb = _occ(A, ta, oa), _occ(B, tb, ob)
        if len(la) != len(lb):
            raise ValueError(f"par ({ta!r},{tb!r}): {len(la)} em A e {len(lb)} em B")
        for a, b in zip(la, lb):
            entries.append((list(a), list(b)))
            ua.update(a)
            ub.update(b)
    for t, occs in A.tok.items():
        if t in B.tok:
            fa = [o for o in occs if not (set(o) & ua)]
            fb = [o for o in B.tok[t] if not (set(o) & ub)]
            for a, b in zip(fa, fb):
                entries.append((list(a), list(b)))
                ua.update(a)
                ub.update(b)
    tokA = {i for occs in A.tok.values() for o in occs for i in o}
    tokB = {i for occs in B.tok.values() for o in occs for i in o}
    ra = [i for i in range(len(A[0])) if i not in ua and i not in tokA]
    rb = [j for j in range(len(B[0])) if j not in ub and j not in tokB]
    for i in ra:
        si = _sig(A[0][i])
        for j in rb:
            if _sig(B[0][j]) == si:
                entries.append(([i], [j]))
                ua.add(i)
                ub.add(j)
                rb.remove(j)
                break
    kw.setdefault("run_time", 1.8)
    return TransformByGlyphMap(A, B, *entries, auto_fade=True, **kw)


def rich(s, size=T_CAP, color=WHITE):
    """Texto com matemática entre $...$ (símbolos saem em MathTex)."""
    g, prev = VGroup(), None
    for i, p in enumerate(s.split("$")):
        p = p.strip() if i % 2 == 0 else p
        if not p:
            continue
        m = MathTex(p, font_size=size * 1.18, color=color) if i % 2 else txt(p, size, color)
        if prev is not None:
            m.next_to(prev, RIGHT, buff=0.16)
        g.add(m)
        prev = m
    return g


# ── desenho ─────────────────────────────────────────────────────────────────────────────────────────────────
def P3(x, y):
    return np.array([x, y, 0.0])


def arrow(a, b, color=WHITE, width=5, z=8, tip=0.2):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if np.linalg.norm(b - a) < 1e-4:
        return VMobject()
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.45,
                 max_stroke_width_to_length_ratio=50).set_z_index(z)


def halo(m, w=6):
    return m.set_stroke(BACKGROUND_COLOR, width=w, background=True)


def box(m, color=WHITE, buff=0.16, width=3):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=width, corner_radius=0.1).set_z_index(22)


def panel(w, h, center, op=0.9, z=14):
    r = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_width=1.5)
    return r.set_fill(PANEL, op).set_stroke(BLUE_L, 1.5, 0.55).move_to(center).set_z_index(z)


def rect(x0, y0, x1, y1, color, op=1.0, z=1):
    return Rectangle(width=x1 - x0, height=y1 - y0).set_fill(color, op).set_stroke(width=0).move_to(
        P3((x0 + x1) / 2, (y0 + y1) / 2)).set_z_index(z)


def charge(sign, pos, r=0.115, z=7):
    """Carga superficial esquemática: azul = positiva (+), azul-claro = negativa (−)."""
    pos = np.asarray(pos, dtype=float)
    c = Circle(radius=r).set_fill(BLUE if sign > 0 else BLUE_L, 1).set_stroke(BACKGROUND_COLOR, 1.2).move_to(pos)
    sc = WHITE if sign > 0 else PANEL
    g = VGroup(c, Line(pos + LEFT * r * 0.55, pos + RIGHT * r * 0.55, stroke_width=2.2, color=sc))
    if sign > 0:
        g.add(Line(pos + DOWN * r * 0.55, pos + UP * r * 0.55, stroke_width=2.2, color=sc))
    return g.set_z_index(z)


class Loop:
    """Percurso do circuito no sentido da corrente convencional (fonte + → fio → resistor → fio → fonte −)."""

    def __init__(self, pts):
        self.p = np.array([P3(*q) for q in pts])
        self.l = np.linalg.norm(np.diff(self.p, axis=0), axis=1)
        self.cum = np.concatenate([[0.0], np.cumsum(self.l)])
        self.total = self.cum[-1]

    def at(self, s):
        s = s % self.total
        i = min(int(np.searchsorted(self.cum, s, side="right")) - 1, len(self.l) - 1)
        t = (self.p[i + 1] - self.p[i]) / self.l[i]
        return self.p[i] + t * (s - self.cum[i]), t

    def seg(self, i, frac):
        return self.at(self.cum[i] + frac * self.l[i])


TOP, BOT, LX, RX, WT = 1.55, -1.95, -5.4, 5.4, 0.5
BAT = (-0.85, 0.45)     # intervalo y da fonte, na vertical esquerda
RES = (-0.9, 0.5)       # intervalo y do resistor, na vertical direita
LOOP = Loop([(LX, BAT[1]), (LX, TOP), (RX, TOP), (RX, RES[1]), (RX, RES[0]), (RX, BOT), (LX, BOT), (LX, BAT[0]),
             (LX, BAT[1])])
# (segmento, fração, comprimento do E) — poucas setas, uma por trecho
E_SPECS = [(0, 0.5, 0.5), (1, 0.2, 0.55), (1, 0.5, 0.55), (1, 0.8, 0.55), (2, 0.5, 0.42), (3, 0.5, 1.05), (4, 0.5, 0.42),
           (5, 0.2, 0.55), (5, 0.5, 0.55), (5, 0.8, 0.55), (6, 0.5, 0.5)]
J_LEN = 0.55
COL = 3.95          # coluna de álgebra (x)
COLW = 5.9


def lane(seg, frac, off):
    p, t = LOOP.seg(seg, frac)
    n = np.array([-t[1], t[0], 0.0])
    return p + n * off, t


def loop_arrows(kind, scale_res=1.0, z=8):
    """Setas de E (ciano, faixa à esquerda do sentido) ou J (verde, faixa à direita) ao longo do circuito."""
    g = VGroup()
    for seg, frac, ln in E_SPECS:
        if kind == "E":
            c, t = lane(seg, frac, 0.115)
            L = ln * (scale_res if seg == 3 else 1.0)
            col = CYAN
        else:
            c, t = lane(seg, frac, -0.115)
            L = J_LEN
            col = GREEN
        g.add(halo(arrow(c - t * L / 2, c + t * L / 2, col, 4, z, 0.17), 5))
    return g


def global_charges():
    """(sinal, x, y): distribuição superficial estacionária conceitual — + no ramo da fonte positiva, − no outro."""
    out = []
    xs = [-4.7, -3.7, -2.6, -1.4, -0.1, 1.3, 2.8, 4.3]
    for i, x in enumerate(xs):
        out.append((+1, x, TOP + (WT / 2 if i % 2 == 0 else -WT / 2)))
        out.append((-1, x, BOT + (-WT / 2 if i % 2 == 0 else WT / 2)))
    out += [(+1, LX - WT / 2, 1.05), (+1, LX + WT / 2, 0.8), (-1, LX - WT / 2, -1.5), (-1, LX + WT / 2, -1.25),
            (+1, RX + WT / 2, 1.0), (-1, RX - WT / 2, -1.45),
            (+1, RX - WT / 2, 0.85), (-1, RX - WT / 2, -1.2)]
    return out


class QuemEmpurraCargasYT009(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.vz, self.vc = 1.0, np.zeros(3)
        self.tag = txt("ELETROMAGNETISMO · CORRENTE E FEM", 18, opacity=0.6).to_corner(UL, buff=0.38).set_z_index(40)
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3)
        self.wm.set_z_index(40)
        self.dim = Rectangle(width=16.6, height=9.6).set_fill(BACKGROUND_COLOR, 0).set_stroke(width=0).set_z_index(12)
        self.add(self.tag, self.wm, self.dim)
        self.build_circuit()
        self.abertura_local()
        self.conducao_local()
        self.ohm_macroscopica()
        self.continuidade()
        self.cargas_superficiais()
        self.regime_estacionario()
        self.fonte_e_fem()
        self.energia_e_payoff()
        self.wait(1)

    # ── utilidades ──────────────────────────────────────────────────────────────────────────────────────────
    def view(self, z, c, rt=3.0):
        z1, c1 = self.vz, self.vc
        c = np.asarray(c, dtype=float)
        self.play(self.world.animate.shift(-z1 * (c - c1)).scale(z / z1, about_point=ORIGIN), run_time=rt)
        self.vz, self.vc = z, c

    def reset_view_silent(self):
        z1, c1 = self.vz, self.vc
        self.world.shift(-z1 * (0 - c1)).scale(1 / z1, about_point=ORIGIN)
        self.vz, self.vc = 1.0, np.zeros(3)

    def set_dim(self, o, rt=1.0):
        self.play(self.dim.animate.set_fill(BACKGROUND_COLOR, o), run_time=rt)

    def chips(self, active):
        """Estágios: TRANSIENTE → REDISTRIBUIÇÃO → ESTACIONÁRIO. active: 0..2 ou None."""
        if not hasattr(self, "chip_g"):
            items = []
            for name in ("TRANSIENTE", "REDISTRIBUIÇÃO DE CARGA", "REGIME ESTACIONÁRIO"):
                t = txt(name, 18, WHITE)
                r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.5, height=0.42, stroke_width=1.5)
                r.set_fill(PANEL, 0.95).set_stroke(BLUE_L, 1.5, 0.6)
                items.append(VGroup(r, t.move_to(r)))
            self.chip_g = VGroup(*items).arrange(RIGHT, buff=0.55).move_to(P3(0, -2.68)).set_z_index(30)
            self.chip_ar = VGroup(*[MathTex(r"\rightarrow", font_size=26, color=DIM).move_to(
                (items[i].get_right() + items[i + 1].get_left()) / 2) for i in range(2)]).set_z_index(30)
        for i, it in enumerate(self.chip_g):
            on = active == i
            it[0].set_stroke(CYAN if on else BLUE_L, 2.5 if on else 1.5, 1.0 if on else 0.6)
            it[0].set_fill(PANEL, 1.0 if on else 0.7)
            it[1].set_opacity(1.0 if on else 0.45)

    # ── circuito recorrente ─────────────────────────────────────────────────────────────────────────────────
    def build_circuit(self):
        h = WT / 2
        pieces = [(LX - h, TOP - h, RX + h, TOP + h), (LX - h, BOT - h, RX + h, BOT + h),
                  (LX - h, BAT[1], LX + h, TOP), (LX - h, BOT, LX + h, BAT[0]),
                  (RX - h, RES[1], RX + h, TOP), (RX - h, BOT, RX + h, RES[0])]
        outline = VGroup(*[rect(a - .04, b - .04, c + .04, d + .04, PANEL, 1, 1) for a, b, c, d in pieces])
        wires = VGroup(*[rect(a, b, c, d, STEEL, 1, 2) for a, b, c, d in pieces])
        hi = VGroup(rect(LX - h, TOP + h - .07, RX + h, TOP + h - .02, WHITE, .22, 3),
                    rect(LX - h, BOT + h - .07, RX + h, BOT + h - .02, WHITE, .22, 3),
                    rect(LX - h + .02, BAT[1], LX - h + .07, TOP, WHITE, .2, 3),
                    rect(LX - h + .02, BOT, LX - h + .07, BAT[0], WHITE, .2, 3),
                    rect(RX - h + .02, RES[1], RX - h + .07, TOP, WHITE, .2, 3),
                    rect(RX - h + .02, BOT, RX - h + .07, RES[0], WHITE, .2, 3))
        # fonte: caixa com placas (longa = +, curta = −)
        bat = VGroup(RoundedRectangle(corner_radius=0.1, width=0.95, height=BAT[1] - BAT[0], stroke_width=2)
                     .set_fill(PANEL, 1).set_stroke(BLUE_L, 2, 0.8).move_to(P3(LX, (BAT[0] + BAT[1]) / 2)),
                     Line(P3(LX - .36, BAT[1] - .3), P3(LX + .36, BAT[1] - .3), stroke_width=5, color=WHITE),
                     Line(P3(LX - .2, BAT[1] - .62), P3(LX + .2, BAT[1] - .62), stroke_width=5, color=WHITE)).set_z_index(4)
        bat_pm = VGroup(MathTex("+", font_size=34, color=WHITE).move_to(P3(LX - .82, BAT[1] - .3)),
                        MathTex("-", font_size=34, color=WHITE).move_to(P3(LX - .82, BAT[1] - .62))).set_z_index(4)
        # resistor: corpo mais largo com zigue-zague
        zz = [P3(RX, RES[1])] + [P3(RX + (0.18 if i % 2 else -0.18), RES[1] - (i + 0.5) * (RES[1] - RES[0]) / 8)
                                 for i in range(8)] + [P3(RX, RES[0])]
        res = VGroup(RoundedRectangle(corner_radius=0.08, width=0.8, height=RES[1] - RES[0], stroke_width=2)
                     .set_fill(PANEL, 1).set_stroke(BLUE_L, 2, 0.8).move_to(P3(RX, (RES[0] + RES[1]) / 2)),
                     VMobject().set_points_as_corners(zz).set_stroke(WHITE, 3)).set_z_index(4)
        self.lbl_bat = txt("fonte", 22, DIM).move_to(P3(LX - 1.2, BAT[0] - 0.4)).set_z_index(4)
        self.lbl_res = txt("resistor", 22, DIM).move_to(P3(RX + 1.15, RES[0] - 0.4)).set_z_index(4)
        self.world = VGroup(outline, wires, hi, bat, bat_pm, res, self.lbl_bat, self.lbl_res)
        self.bat_g, self.res_g = VGroup(bat, bat_pm), res
        self.pieces = (outline, wires, hi)

    # ═══ 1. QUEM AGE LOCALMENTE ═════════════════════════════════════════════════════════════════════════════
    def abertura_local(self):
        self.next_section("B01_gancho")
        self.play(LaggedStart(FadeIn(self.world[0]), FadeIn(self.world[1]), FadeIn(self.world[2]), FadeIn(self.bat_g),
                              FadeIn(self.res_g), lag_ratio=0.25), run_time=3)
        self.play(FadeIn(self.lbl_bat), FadeIn(self.lbl_res), run_time=0.8)
        self.wait(1.5)
        ring = Circle(radius=0.95, color=CYAN, stroke_width=3).move_to(P3(LX, (BAT[0] + BAT[1]) / 2)).set_z_index(5)
        self.world.add(ring)
        self.play(FadeIn(ring, scale=1.3), run_time=0.6)
        self.play(Indicate(self.bat_g, color=WHITE, scale_factor=1.12), run_time=1.2)
        self.play(FadeOut(ring), run_time=0.5)
        self.world.remove(ring)
        carrier = VGroup(Circle(radius=0.11, color=BLUE_L, stroke_width=0).set_fill(BLUE_L, 1),
                         Line(P3(3.3 - .06, 1.55), P3(3.3 + .06, 1.55), stroke_width=2.5, color=PANEL)).set_z_index(7)
        carrier.move_to(P3(3.3, 1.55)).set_opacity(0)
        carrier_ring = Circle(radius=0.3, color=WHITE, stroke_width=3).move_to(P3(3.3, 1.55)).set_z_index(7)
        carrier_ring.set_stroke(opacity=0)
        self.world.add(carrier, carrier_ring)
        # a câmera percorre o circuito: bateria → trecho distante do fio
        self.view(1.6, P3(-4.6, 0.9), 2.5)
        self.wait(0.6)
        self.view(1.6, P3(3.3, 1.55), 6.0)
        self.play(carrier.animate.set_opacity(1), carrier_ring.animate.set_stroke(opacity=1), run_time=1.0)
        q = txt("Que força age aqui, agora?", T_HEAD).move_to(P3(0, -1.5)).set_z_index(30)
        halo(q)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=1.0)
        self.play(Indicate(carrier_ring, color=CYAN, scale_factor=1.25), run_time=1.0)
        self.wait(3.5)
        self.q_hook = q
        self.hook_extra = VGroup(carrier, carrier_ring)

    # ═══ 2. CONDUÇÃO LOCAL: E → J = σE ═════════════════════════════════════════════════════════════════════
    def conducao_local(self):
        self.next_section("B02_conducao_local")
        # zoom microscópico: o fio vira um corte com elétrons
        x0, x1, cy, hh = -7.0, 0.2, -0.2, 2.8
        body = Rectangle(width=x1 - x0, height=hh).set_fill(STEEL, 0.16).set_stroke(STEEL, 3).move_to(P3((x0 + x1) / 2, cy))
        band = rect(x0, cy + hh / 2 - 0.1, x1, cy + hh / 2, WHITE, 0.14, 1)
        ions = VGroup(*[Circle(radius=0.085, stroke_width=0).set_fill(STEEL, 0.55).move_to(P3(x, y)).set_z_index(1)
                        for x in np.arange(x0 + 0.6, x1 - 0.2, 0.95) for y in np.arange(cy - 1.05, cy + 1.2, 0.7)])
        rng = np.random.default_rng(11)
        N = 22
        pos = np.column_stack([rng.uniform(x0 + .3, x1 - .3, N), rng.uniform(cy - hh / 2 + .2, cy + hh / 2 - .2, N)])
        ang = rng.uniform(0, 2 * np.pi, N)
        vel = np.column_stack([np.cos(ang), np.sin(ang)]) * rng.uniform(0.9, 1.5, N)[:, None]
        elec = VGroup(*[Circle(radius=0.075, stroke_width=0).set_fill(BLUE_L, 1).set_z_index(5).move_to(P3(*p)) for p in pos])
        hero = VGroup(Circle(radius=0.13, stroke_width=1.5, color=WHITE).set_fill(BLUE_L, 1),
                      Line(LEFT * 0.07, RIGHT * 0.07, stroke_width=2.5, color=PANEL)).set_z_index(6)
        hero.move_to(P3(-3.4, 0.0))
        hp = np.array([-3.4, 0.0])
        hv = np.array([0.8, 0.9])
        trail = VMobject().set_stroke(BLUE_L, 2, 0.6).set_z_index(4)
        hist = [hp.copy()]
        drift = ValueTracker(0.0)
        vd = 0.3
        st = {"pos": pos, "vel": vel, "hp": hp, "hv": hv}

        def step(m, dt):
            dt = min(dt, 0.1)
            for key in ("pos", "hp"):
                pass
            p, v = st["pos"], st["vel"]
            hit = rng.random(N) < 2.2 * dt
            a = rng.uniform(0, 2 * np.pi, N)
            v[hit] = (np.column_stack([np.cos(a), np.sin(a)]) * rng.uniform(0.9, 1.5, N)[:, None])[hit]
            p += (v + np.array([-vd * drift.get_value(), 0.0]) * 1.0) * dt
            p[:, 0] = np.where(p[:, 0] < x0 + .2, x1 - .25, np.where(p[:, 0] > x1 - .2, x0 + .25, p[:, 0]))
            p[:, 1] = np.where((p[:, 1] < cy - hh / 2 + .15) | (p[:, 1] > cy + hh / 2 - .15), p[:, 1] - 2 * v[:, 1] * dt, p[:, 1])
            for i, e in enumerate(m):
                e.move_to(P3(*p[i]))
            h, hvv = st["hp"], st["hv"]
            if rng.random() < 2.2 * dt:
                aa = rng.uniform(0, 2 * np.pi)
                hvv[:] = np.array([np.cos(aa), np.sin(aa)]) * 1.1
            h += (hvv + np.array([-vd * drift.get_value(), 0.0])) * dt
            if h[0] < x0 + .3 or h[0] > x1 - .3:
                h[0] = np.clip(h[0], x0 + .3, x1 - .3)
                hvv[0] *= -1
            if h[1] < cy - hh / 2 + .2 or h[1] > cy + hh / 2 - .2:
                h[1] = np.clip(h[1], cy - hh / 2 + .2, cy + hh / 2 - .2)
                hvv[1] *= -1
            hero.move_to(P3(*h))
            hist.append(h.copy())
            del hist[:-70]
            if len(hist) > 2:
                trail.set_points_as_corners([P3(*q) for q in hist])

        elec.add_updater(step)
        micro = VGroup(body, band, ions, elec, hero, trail)
        self.micro = micro
        # corta o macro, entra o micro
        self.play(FadeOut(self.q_hook), FadeOut(self.world), run_time=1.0)
        self.world.remove(*self.hook_extra)
        self.reset_view_silent()
        note0 = txt("Dentro do fio: elétrons em movimento irregular", T_CAP, DIM).move_to(P3(-3.4, -2.4))
        self.play(FadeIn(body), FadeIn(band), FadeIn(ions), FadeIn(elec), FadeIn(hero), run_time=1.2)
        self.add(micro)
        self.play(FadeIn(note0), run_time=0.6)
        self.wait(5)
        # E aparece: resposta local
        e_arrows = VGroup(*[halo(arrow(P3(x - 0.6, cy + 1.0), P3(x + 0.6, cy + 1.0), CYAN, 5, 9, 0.22)) for x in (-5.6, -3.4, -1.2)])
        e_lab = MathTex(r"\mathbf E", font_size=44, color=CYAN).move_to(P3(-6.3, cy + 1.75))
        halo(e_lab)
        note1 = txt("campo elétrico local", T_CAP, CYAN).next_to(e_lab, RIGHT, buff=0.25)
        self.play(LaggedStart(*[FadeIn(a, shift=RIGHT * 0.2) for a in e_arrows], lag_ratio=0.25), FadeIn(e_lab), FadeIn(note1), run_time=1.6)
        self.wait(1.2)
        # a deriva média nasce (pequena)
        vd_arr = halo(arrow(P3(-1.0, 2.2), P3(-2.35, 2.2), VIOLET, 5, 9, 0.22))
        vd_lab = MathTex(r"\mathbf v_d", font_size=40, color=VIOLET).next_to(vd_arr, UP, buff=0.05)
        vd_note = txt("deriva média do elétron", T_CAP, VIOLET).next_to(vd_arr, LEFT, buff=0.2)
        self.play(drift.animate.set_value(1.0), FadeOut(note0), run_time=2.5)
        self.play(FadeIn(vd_arr, shift=LEFT * 0.2), FadeIn(vd_lab), FadeIn(vd_note), run_time=1.0)
        self.wait(5)
        j_arr = halo(arrow(P3(-5.8, -2.0), P3(-2.2, -2.0), GREEN, 7, 9, 0.28))
        j_lab = MathTex(r"\mathbf J", font_size=44, color=GREEN).next_to(j_arr, UP, buff=0.05)
        j_note = txt("corrente macroscópica", T_CAP, GREEN).next_to(j_arr, RIGHT, buff=0.25)
        self.play(FadeIn(j_arr, shift=RIGHT * 0.3), FadeIn(j_lab), FadeIn(j_note), run_time=1.4)
        self.wait(2.5)
        # fórmula local, depois do fenômeno
        eq0 = M(r"\mathbf J", "=", r"\sigma", r"\mathbf f", size=M_L).move_to(P3(COL, 1.2))
        eq1 = M(r"\mathbf J", "=", r"\sigma", r"\mathbf E", size=M_L).move_to(eq0)
        note_f = rich("no trecho resistivo: $\\mathbf f=\\mathbf E$", T_CAP).move_to(P3(COL, 0.0))
        self.play(Write(eq0), run_time=1.5)
        self.wait(1.5)
        self.play(FadeIn(note_f, shift=UP * 0.1), run_time=0.8)
        self.wait(1)
        self.play(TransformMatchingTex(eq0, eq1), run_time=1.5)
        bx = box(eq1)
        self.play(FadeIn(bx), run_time=0.6)
        self.wait(2.5)
        self.micro_ui = VGroup(note1, e_lab, vd_arr, vd_lab, vd_note, j_arr, j_lab, j_note, e_arrows)
        self.micro_eq = VGroup(eq1, bx, note_f)
        self.micro_state = (elec, hero, trail, body, band, ions, e_arrows)

    # ═══ 3-4. DA LEI LOCAL PARA V = IR ═════════════════════════════════════════════════════════════════════
    def ohm_macroscopica(self):
        self.next_section("B03_ohm_macro")
        elec, hero, trail, body, band, ions, e_arrows = self.micro_state
        # fio macroscópico: mesmo objeto, agora com L, A e I
        wx0, wx1, wy, wh = -6.0, 0.0, 0.3, 1.1
        mbody = Rectangle(width=wx1 - wx0, height=wh).set_fill(STEEL, 1).set_stroke(PANEL, 2).move_to(P3(-3.0, wy)).set_z_index(2)
        mhi = rect(wx0, wy + wh / 2 - .07, wx1, wy + wh / 2 - .02, WHITE, .22, 3)
        face = Ellipse(width=0.4, height=wh).set_fill(VIOLET, 0.55).set_stroke(VIOLET, 3).move_to(P3(wx1, wy)).set_z_index(3)
        A_lab = MathTex("A", font_size=44, color=VIOLET).move_to(P3(0.62, wy + 0.1))
        Lline = DoubleArrow(P3(wx0, -0.55), P3(wx1, -0.55), buff=0, color=VIOLET, stroke_width=4, tip_length=0.18)
        L_lab = MathTex("L", font_size=44, color=VIOLET).move_to(P3(-3.0, -0.95))
        Vline = VGroup(Line(P3(wx0, 1.25), P3(wx1, 1.25), stroke_width=4, color=CYAN),
                       Line(P3(wx0, 1.15), P3(wx0, 1.35), stroke_width=4, color=CYAN),
                       Line(P3(wx1, 1.15), P3(wx1, 1.35), stroke_width=4, color=CYAN))
        V_lab = MathTex("V", font_size=44, color=CYAN).move_to(P3(-3.0, 1.62))
        Vtxt = txt("queda de potencial", T_CAP, CYAN).next_to(V_lab, RIGHT, buff=0.2)
        I_arr = halo(arrow(P3(-7.0, wy), P3(-6.1, wy), GREEN, 8, 9, 0.26))
        I_lab = MathTex("I", font_size=44, color=GREEN).move_to(P3(-6.6, wy + 0.5))
        mE = VGroup(*[halo(arrow(P3(x - .55, wy + .3), P3(x + .55, wy + .3), CYAN, 4, 9, 0.18), 5) for x in (-5.0, -3.0, -1.0)])
        mJ = VGroup(*[halo(arrow(P3(x - .55, wy - .22), P3(x + .55, wy - .22), GREEN, 4, 9, 0.18), 5) for x in (-5.0, -3.0, -1.0)])
        mE_lab = MathTex(r"\mathbf E", font_size=36, color=CYAN).move_to(P3(-1.0 - .1, wy + 0.0 + 0.0)).set_opacity(0)
        # transição micro → macro
        for m in (elec, hero, trail):
            m.clear_updaters()
        self.play(FadeOut(VGroup(elec, hero, trail, ions, band, self.micro_ui[0], self.micro_ui[2], self.micro_ui[3],
                                 self.micro_ui[4], self.micro_ui[5], self.micro_ui[6], self.micro_ui[7]), run_time=1.0),
                  ReplacementTransform(body, mbody), ReplacementTransform(e_arrows, mE), FadeOut(self.micro_ui[1]),
                  FadeOut(self.micro_eq[2]), run_time=1.6)
        self.remove(self.micro)
        self.play(FadeIn(mhi), FadeIn(face), run_time=0.5)
        self.play(FadeIn(I_arr), FadeIn(I_lab), FadeIn(mJ), run_time=1.0)
        self.play(FadeIn(Lline), FadeIn(L_lab), FadeIn(A_lab), run_time=1.0)
        self.play(FadeIn(Vline), FadeIn(V_lab), FadeIn(Vtxt), run_time=1.0)
        self.wait(1.5)
        # relações ligadas ao mesmo objeto físico
        r1 = M("J", "=", r"\frac{I}{A}", size=M_S)
        r2 = M("E", "=", r"\frac{V}{L}", size=M_S)
        r3 = M("J", "=", r"\sigma", "E", size=M_S)
        rels = VGroup(r1, r2, r3).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(P3(COL, 1.55))
        old_eq = self.micro_eq[:2]
        self.play(FadeOut(old_eq), run_time=0.8)
        self.play(FadeIn(r1, shift=RIGHT * 0.2), Indicate(face, color=WHITE), Indicate(I_arr, color=WHITE), run_time=1.6)
        self.wait(1.0)
        self.play(FadeIn(r2, shift=RIGHT * 0.2), Indicate(Lline, color=WHITE), Indicate(V_lab, color=WHITE), run_time=1.6)
        self.wait(1.0)
        self.play(FadeIn(r3, shift=RIGHT * 0.2), Indicate(mE, color=WHITE), Indicate(mJ, color=WHITE), run_time=1.6)
        self.wait(2)
        self.macro = VGroup(mbody, mhi, face, A_lab, Lline, L_lab, Vline, V_lab, Vtxt, I_arr, I_lab, mE, mJ)
        self.macro_L = VGroup(Lline, L_lab, Vline, V_lab, Vtxt, I_arr, I_lab)

        self.next_section("B04_ohm_derivacao")
        S1 = EQ(r"\frac{I}{A}=J=\sigma E=\sigma\frac{V}{L}", "I", "A", "J", r"\sigma", "E", "V", "L", size=M_M, width=COLW)
        S2 = EQ(r"\frac{I}{A}=\sigma\frac{V}{L}", "I", "A", r"\sigma", "V", "L", size=M_L, width=COLW)
        S3f = EQ(r"V=I\frac{L}{\sigma A}", "V", "I", "L", r"\sigma", "A", size=M_L, width=COLW)
        S3c = EQ(r"V=I\frac{L}{\sigma A}", "V", "I", r"\frac{L}{\sigma A}", size=M_L, width=COLW)
        Df = EQ(r"R=\frac{L}{\sigma A}", "R", r"\frac{L}{\sigma A}", size=M_L, width=COLW)
        S4 = EQ(r"V=IR", "V", "I", "R", size=M_XL, width=COLW)
        for s in (S1, S2, S3f, S3c, S4):
            s.move_to(P3(COL, -0.6))
        self.play(rels.animate.set_opacity(0.45), run_time=0.6)
        self.play(FadeIn(S1, shift=UP * 0.15), run_time=1.4)
        self.wait(1.5)
        self.play(gmap(S1, S2, (r"\sigma", None, 0), ("J", None), ("E", None), (r"\sigma", r"\sigma", 1, 0)), run_time=2.0)
        self.add(S2)
        self.wait(1.5)
        self.play(gmap(S2, S3f), run_time=2.4)
        self.add(S3f)
        self.wait(1.2)
        # troca invisível para o token do bloco L/(σA)
        S3c.move_to(S3f)
        self.remove(S3f)
        self.add(S3c)
        blk = glyphs(S3c, r"\frac{L}{\sigma A}")
        bk = SurroundingRectangle(blk, color=VIOLET, buff=0.12, stroke_width=3, corner_radius=0.08).set_z_index(22)
        self.play(FadeIn(bk), run_time=0.8)
        blk_note = txt("depende só do material e da geometria", T_CAP, VIOLET).next_to(bk, DOWN, buff=0.35)
        self.play(FadeIn(blk_note, shift=UP * 0.1), run_time=0.8)
        self.wait(2.5)
        Df.move_to(P3(COL, -1.95))
        self.play(FadeOut(blk_note), run_time=0.4)
        self.play(TransformFromCopy(blk, glyphs(Df, r"\frac{L}{\sigma A}")), run_time=1.6)
        self.play(FadeIn(glyphs(Df, "R")), run_time=0.6)
        self.add(Df)
        bd = box(Df, WHITE)
        self.play(FadeIn(bd), run_time=0.6)
        self.wait(2)
        self.play(FadeOut(bk), FadeOut(bd), run_time=0.5)
        S4.move_to(S3c)
        self.play(gmap(S3c, S4, (r"\frac{L}{\sigma A}", "R")), FadeOut(Df), run_time=2.2)
        self.add(S4)
        bs = box(S4, WHITE)
        self.play(FadeIn(bs), run_time=0.6)
        self.wait(3)
        # consequência curta
        self.play(FadeOut(rels), run_time=0.8)
        cons = rich(r"$L\uparrow\Rightarrow R\uparrow,\qquad A\uparrow\Rightarrow R\downarrow$", T_NOTE).move_to(P3(COL, 1.5))
        self.play(FadeIn(cons, shift=UP * 0.1), run_time=0.8)
        self.wait(3)
        self.play(FadeOut(cons), FadeOut(S4), FadeOut(bs), FadeOut(self.macro), run_time=1.2)
        self.macro_rest = VGroup()

    # ═══ 5-6. QUEM ESTABELECE E? — CONTINUIDADE ═══════════════════════════════════════════════════════════════
    def continuidade(self):
        self.next_section("B05_segunda_pergunta")
        self.reset_view_silent()
        self.E_arr = loop_arrows("E", 1.0)
        self.J_arr = loop_arrows("J")
        self.play(FadeIn(self.world), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(a, shift=0.1 * RIGHT) for a in self.E_arr], lag_ratio=0.12), run_time=3.0)
        self.wait(1)
        e_tag = MathTex(r"\mathbf E", font_size=44, color=CYAN).move_to(P3(0, 0.2))
        q = VGroup(txt("Quem estabelece esse campo", T_BODY), txt("ao longo do circuito inteiro?", T_BODY)).arrange(DOWN, buff=0.15).move_to(P3(0, -0.2)).set_z_index(30)
        halo(q)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=1.0)
        self.wait(4)
        self.play(FadeOut(q), run_time=0.6)
        self.q5 = q

        self.next_section("B06_continuidade")
        # volume de controle numa região do fio: figura local grande
        self.set_dim(0.94, 1.0)
        cx0, cx1, cy, ch = -7.0, 0.2, 0.35, 1.9
        wire = Rectangle(width=cx1 - cx0, height=ch).set_fill(STEEL, 1).set_stroke(PANEL, 2).move_to(P3((cx0 + cx1) / 2, cy)).set_z_index(15)
        whi = rect(cx0, cy + ch / 2 - .08, cx1, cy + ch / 2 - .02, WHITE, .22, 16)
        CVx = -3.4
        cv = DashedVMobject(Rectangle(width=2.4, height=ch + 0.45, color=BLUE_L, stroke_width=3).move_to(P3(CVx, cy)), num_dashes=44).set_z_index(18)
        cv_lab = txt("volume de controle", 20, BLUE_L).move_to(P3(CVx, cy + ch / 2 + 0.45)).set_z_index(18)
        self.cv_all = VGroup(wire, whi, cv, cv_lab)
        self.play(FadeIn(wire), FadeIn(whi), run_time=1.0)
        self.play(FadeIn(cv), FadeIn(cv_lab), run_time=1.0)
        self.chips(0)
        self.play(FadeIn(self.chip_g), FadeIn(self.chip_ar), run_time=0.8)
        cont = M(r"\frac{\partial\rho}{\partial t}", "+", r"\nabla\cdot\mathbf J", "=", "0", size=M_L, width=COLW).move_to(P3(COL, 1.9)).set_z_index(20)
        self.play(Write(cont), run_time=2.0)
        self.wait(2)
        dq = M(r"\frac{dQ}{dt}", "=", r"I_{\rm entra}", "-", r"I_{\rm sai}", size=M_M, width=COLW).move_to(P3(COL, 0.3)).set_z_index(20)
        self.play(FadeIn(dq, shift=UP * 0.1), run_time=1.2)
        self.wait(2)
        self.cont, self.dq = cont, dq
        self.wire_cv = (cy, ch, CVx)

    # ═══ cena prioritária: I_entra > I_sai → carga superficial → E → J ═══════════════════════════════════
    def cargas_superficiais(self):
        self.next_section("B07_carga_E_J")
        cy, ch, CVx = self.wire_cv
        d, s, sE, sJ = ValueTracker(0), ValueTracker(0), ValueTracker(0), ValueTracker(0)
        op = ValueTracker(0)

        def lens():
            base = 0.95
            k = 0.35
            eL = base + d.get_value() * k - sE.get_value() * k
            eR = base - d.get_value() * k + sE.get_value() * k
            jL = base + d.get_value() * k - sJ.get_value() * k
            jR = base - d.get_value() * k + sJ.get_value() * k
            return eL, eR, jL, jR

        def arrows():
            eL, eR, jL, jR = lens()
            o = op.get_value()
            g = VGroup()
            for c, ln, y, col in ((-5.7, eL, cy + 0.42, CYAN), (-1.0, eR, cy + 0.42, CYAN),
                                  (-5.7, jL, cy - 0.38, GREEN), (-1.0, jR, cy - 0.38, GREEN)):
                g.add(halo(arrow(P3(c - ln / 2, y), P3(c + ln / 2, y), col, 6, 20, 0.22), 5).set_opacity(o))
            return g

        arr = always_redraw(arrows)
        el = MathTex(r"\mathbf E", font_size=34, color=CYAN).set_z_index(20)
        jl = MathTex(r"\mathbf J", font_size=34, color=GREEN).set_z_index(20)
        lab_in = MathTex(r"I_{\rm entra}", font_size=34, color=GREEN).move_to(P3(-5.7, cy - 1.45)).set_z_index(20)
        lab_out = MathTex(r"I_{\rm sai}", font_size=34, color=GREEN).move_to(P3(-1.0, cy - 1.45)).set_z_index(20)
        lab_E = VGroup(MathTex(r"\mathbf E", font_size=34, color=CYAN).move_to(P3(-7.0 + 0.3, cy + 0.42)),
                       MathTex(r"\mathbf J", font_size=34, color=GREEN).move_to(P3(-7.0 + 0.3, cy - 0.38))).set_z_index(20)
        # cargas superficiais do volume de controle: aparecem na superfície, nunca no volume
        spots = [(CVx - 0.9, cy + ch / 2), (CVx - 0.3, cy + ch / 2), (CVx + 0.3, cy + ch / 2), (CVx + 0.9, cy + ch / 2),
                 (CVx - 0.9, cy - ch / 2), (CVx - 0.3, cy - ch / 2), (CVx + 0.3, cy - ch / 2), (CVx + 0.9, cy - ch / 2)]
        order = [1, 5, 2, 6, 0, 4, 3, 7]
        chs = VGroup(*[charge(+1, P3(*spots[i]), r=0.14, z=19) for i in order])

        def chg_upd(m):
            for i, c in enumerate(m):
                c.set_opacity(float(np.clip(s.get_value() * len(m) - i, 0, 1)))

        chs.add_updater(chg_upd)
        chg_upd(chs)
        # lista causal
        step_t = [rich(r"$I_{\rm entra}>I_{\rm sai}$", T_NOTE), rich("acúmulo na superfície", T_NOTE),
                  rich(r"$\mathbf E$ muda", T_NOTE), rich(r"$\mathbf J=\sigma\mathbf E$ muda", T_NOTE)]
        for i, t in enumerate(step_t):
            t.move_to(P3(COL, 1.3 - 0.95 * i)).set_z_index(20)
        step_ar = VGroup(*[MathTex(r"\downarrow", font_size=30, color=DIM).move_to(P3(COL, 1.3 - 0.95 * i - 0.47)) for i in range(3)]).set_z_index(20)
        self.play(self.cont.animate.scale(0.62).move_to(P3(COL, 2.2)), FadeOut(self.dq), run_time=1.0)
        self.add(arr, chs)
        self.play(FadeIn(lab_E), op.animate.set_value(1), run_time=1.2)
        self.wait(1.5)

        def hi(i):
            return AnimationGroup(*[t.animate.set_opacity(1 if j == i else 0.35) for j, t in enumerate(step_t)])

        for t in step_t:
            t.set_opacity(0.35)
        self.play(FadeIn(step_ar), *[FadeIn(t) for t in step_t], run_time=0.8)
        # 1. entra mais corrente do que sai
        self.play(hi(0), d.animate.set_value(1), run_time=3.0)
        self.play(FadeIn(lab_in), FadeIn(lab_out), run_time=0.8)
        self.wait(2)
        # 2. carga na superfície
        self.play(hi(1), s.animate.set_value(0.5), run_time=3.5)
        self.wait(1.5)
        # 3. E muda
        self.play(hi(2), sE.animate.set_value(0.5), run_time=3.5)
        self.wait(1.5)
        # 4. J muda
        self.play(hi(3), sJ.animate.set_value(0.5), run_time=3.5)
        self.wait(1.5)
        # evolui até o estacionário
        self.chips(1)
        self.wait(0.1)
        self.play(AnimationGroup(s.animate.set_value(1), sE.animate.set_value(1), sJ.animate.set_value(1), lag_ratio=0.12),
                  run_time=6.0)
        eq_lab = MathTex(r"I_{\rm entra}", "=", r"I_{\rm sai}", font_size=34).move_to(P3(-3.4, cy - 1.7)).set_z_index(20)
        eq_lab[0].set_color(GREEN)
        eq_lab[2].set_color(GREEN)
        self.play(FadeOut(lab_in), FadeOut(lab_out), FadeIn(eq_lab), run_time=1.0)
        self.chips(2)
        self.wait(3)
        # a carga fica: guarda o estado final do trecho local
        arr.clear_updaters()
        chs.clear_updaters()
        self.local_final = VGroup(arr, chs, lab_E, eq_lab, step_t_group := VGroup(*step_t), step_ar)
        self.play(FadeOut(self.local_final[2:]), FadeOut(self.cv_all[2:]), run_time=1.0)

        # ── do ajuste local à distribuição superficial global ──
        self.next_section("B07b_distribuicao_global")
        spot = DashedVMobject(Circle(radius=0.62, color=BLUE_L, stroke_width=3).scale([1.7, 1, 1]).move_to(P3(-2.2, TOP)), num_dashes=24).set_z_index(10)
        self.play(FadeOut(self.local_final[0]), FadeOut(self.local_final[1]), FadeOut(self.cv_all[0]), FadeOut(self.cv_all[1]),
                  FadeOut(self.cont), run_time=1.0)
        self.set_dim(0.0, 1.2)
        self.chips(0)
        self.play(FadeIn(spot), run_time=0.8)
        gc = global_charges()
        center = np.array([-2.2, TOP])
        gch = [(charge(sg, P3(x, y), r=0.115, z=7), np.hypot(x - center[0], y - center[1])) for sg, x, y in gc]
        gch.sort(key=lambda t: t[1])
        self.G_charges = VGroup(*[g for g, _ in gch])
        self.play(Indicate(spot, color=WHITE, scale_factor=1.15), run_time=1.0)
        steps = [rich("o ajuste local se repete pelo circuito", T_NOTE), rich("a distribuição superficial se espalha", T_NOTE),
                 rich(r"$\mathbf E$ fica adequado em cada região", T_NOTE)]
        for i, t in enumerate(steps):
            t.move_to(P3(0, 0.55 - 0.55 * i)).set_z_index(30)
        self.chips(1)
        self.play(FadeIn(steps[0], shift=UP * 0.1), LaggedStart(*[FadeIn(g, scale=0.4) for g in self.G_charges], lag_ratio=0.06),
                  run_time=6.0)
        self.play(FadeIn(steps[1], shift=UP * 0.1), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(spot), FadeOut(self.E_arr), run_time=0.6)
        # E se adapta: curto nos fios, longo no resistor; J igual em todo lado
        self.E_arr = loop_arrows("E", 1.0)
        self.play(FadeIn(steps[2], shift=UP * 0.1), FadeIn(self.E_arr), FadeIn(self.J_arr), run_time=1.8)
        jse = M(r"\mathbf J", "=", r"\sigma", r"\mathbf E", size=M_S).move_to(P3(0, -1.2)).set_z_index(30)
        self.play(FadeIn(jse, shift=UP * 0.1), run_time=0.8)
        self.wait(3.5)
        self.play(FadeOut(steps[0]), FadeOut(steps[1]), FadeOut(steps[2]), FadeOut(jse), FadeOut(self.local_final[2:]), run_time=0.8)
        # fio de baixa resistência × resistor (curto, opcional)
        base_y = -0.2
        small = Rectangle(width=0.2, height=0.14).set_fill(CYAN, 1).set_stroke(width=0).set_z_index(30).move_to(P3(-2.2, base_y + 0.07))
        big = Rectangle(width=0.2, height=1.0).set_fill(CYAN, 1).set_stroke(width=0).set_z_index(30).move_to(P3(2.2, base_y + 0.5))
        t_s = rich(r"fio: queda $\Delta V$ pequena", T_CAP).move_to(P3(-2.2, base_y - 0.45)).set_z_index(30)
        t_b = rich(r"resistor: queda $\Delta V$ grande", T_CAP).move_to(P3(2.2, base_y - 0.45)).set_z_index(30)
        self.play(FadeIn(small), FadeIn(big), FadeIn(t_s), FadeIn(t_b), run_time=1.2)
        self.wait(3.5)
        self.play(FadeOut(VGroup(small, big, t_s, t_b)), run_time=0.8)

    # ═══ 6b. REGIME ESTACIONÁRIO ═══════════════════════════════════════════════════════════════════════════
    def regime_estacionario(self):
        self.next_section("B08_estacionario")
        self.chips(1)
        tr = M(r"\frac{\partial\rho}{\partial t}", r"\neq", "0", size=M_L).move_to(P3(0, 0.0)).set_z_index(30)
        self.play(FadeIn(tr, shift=UP * 0.1), run_time=1.0)
        # a redistribuição pulsa e para
        self.play(*[Indicate(g, color=WHITE, scale_factor=1.3) for g in self.G_charges[:8]], run_time=1.6)
        self.wait(1)
        self.chips(2)
        st1 = M(r"\frac{\partial\rho}{\partial t}", "=", "0", size=M_L).move_to(P3(-2.35, 0.3)).set_z_index(30)
        st2 = M(r"\nabla\cdot\mathbf J", "=", "0", size=M_L).move_to(P3(2.35, 0.3)).set_z_index(30)
        self.play(ReplacementTransform(tr, st1), run_time=1.2)
        self.play(FadeIn(st2, shift=UP * 0.1), run_time=1.0)
        b2 = box(st2)
        self.play(FadeIn(b2), run_time=0.6)
        self.wait(2)
        # as cargas NÃO desapareceram
        keep = SurroundingRectangle(self.G_charges, color=BLUE_L, buff=0.2, stroke_width=0)
        self.play(*[Indicate(g, color=WHITE, scale_factor=1.4) for g in self.G_charges], run_time=1.6)
        ne1 = VGroup(txt("regime estacionário", T_CAP), MathTex(r"\neq", font_size=40), txt("sem cargas superficiais", T_CAP)).arrange(RIGHT, buff=0.3)
        ne1.move_to(P3(0, -0.55)).set_z_index(30)
        self.play(FadeIn(ne1, shift=UP * 0.1), run_time=1.0)
        bn1 = box(ne1, BLUE_L)
        self.play(FadeIn(bn1), run_time=0.6)
        self.wait(3)
        self.play(FadeOut(VGroup(st1, st2, b2, ne1, bn1)), run_time=0.8)
        # E ≠ 0 no fio com corrente, e a comparação com a eletrostática
        self.set_dim(0.55, 0.8)
        pa = panel(4.5, 2.5, P3(-2.6, -0.05))
        pb = panel(4.5, 2.5, P3(2.6, -0.05))
        ta = txt("equilíbrio eletrostático", T_CAP, DIM).move_to(P3(-2.6, 0.85)).set_z_index(30)
        tb = txt("corrente estacionária", T_CAP, GREEN).move_to(P3(2.6, 0.85)).set_z_index(30)
        ea = M(r"\mathbf E", "=", "0", size=M_L).move_to(P3(-2.6, 0.0)).set_z_index(30)
        ea_n = txt("no interior do condutor", 20, DIM).move_to(P3(-2.6, -0.7)).set_z_index(30)
        eb1 = M(r"\mathbf E", r"\neq", "0", size=M_L).move_to(P3(2.6, 0.2)).set_z_index(30)
        eb2 = M(r"\mathbf J", "=", r"\sigma", r"\mathbf E", size=M_M).move_to(P3(2.6, -0.5)).set_z_index(30)
        self.play(FadeIn(pa), FadeIn(pb), FadeIn(ta), FadeIn(tb), run_time=1.0)
        self.play(FadeIn(ea, shift=UP * 0.1), FadeIn(ea_n), run_time=1.0)
        self.wait(1.5)
        self.play(FadeIn(eb1, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(eb2, shift=UP * 0.1), run_time=1.0)
        bb = box(eb1, GREEN)
        self.play(FadeIn(bb), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(VGroup(pa, pb, ta, tb, ea, ea_n, eb1, eb2, bb)), run_time=0.8)
        ne2 = VGroup(txt("estacionário", T_BODY), MathTex(r"\neq", font_size=48), txt("eletrostático", T_BODY)).arrange(RIGHT, buff=0.35)
        ne2.move_to(P3(0, -0.2)).set_z_index(30)
        bn2 = box(ne2, WHITE, 0.22)
        self.play(FadeIn(ne2, shift=UP * 0.1), FadeIn(bn2), run_time=1.2)
        self.wait(3)
        self.play(FadeOut(ne2), FadeOut(bn2), run_time=0.8)
        self.set_dim(0.0, 0.8)
        self.wait(1.5)

    # ═══ 7-8. QUEM REPÕE A ENERGIA? — FONTE E FEM ═════════════════════════════════════════════════════════
    def fonte_e_fem(self):
        self.next_section("B09_fonte")
        self.play(FadeOut(self.chip_g), FadeOut(self.chip_ar), run_time=0.5)
        self.set_dim(0.96, 1.0)
        q = txt("Se o resistor dissipa energia, quem repõe essa energia?", T_BODY).move_to(P3(0, 1.5)).set_z_index(30)
        halo(q)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=1.0)
        self.wait(3.5)
        self.play(q.animate.scale(0.62).move_to(P3(COL, 2.2)).set_color(DIM), run_time=1.0)
        # fonte esquemática: E e f_s coexistem
        bx0 = -3.3
        body = RoundedRectangle(corner_radius=0.15, width=2.8, height=3.6, stroke_width=2).set_fill(PANEL, 1).set_stroke(BLUE_L, 2, 0.8)
        body.move_to(P3(bx0, -0.15)).set_z_index(15)
        stub_t = rect(bx0 - .25, 1.65, bx0 + .25, 2.3, STEEL, 1, 15)
        stub_b = rect(bx0 - .25, -2.6, bx0 + .25, -1.95, STEEL, 1, 15)
        plate_t = Line(P3(bx0 - 1.0, 1.35), P3(bx0 + 1.0, 1.35), stroke_width=7, color=WHITE).set_z_index(16)
        plate_b = Line(P3(bx0 - 0.55, -1.65), P3(bx0 + 0.55, -1.65), stroke_width=7, color=WHITE).set_z_index(16)
        pm = VGroup(MathTex("+", font_size=40, color=WHITE).move_to(P3(bx0 + 1.75, 1.35)),
                    MathTex("-", font_size=40, color=WHITE).move_to(P3(bx0 + 1.75, -1.65))).set_z_index(16)
        cps = VGroup(*[charge(+1, P3(bx0 + dx, 1.12), z=17) for dx in (-0.6, 0.0, 0.6)],
                     *[charge(-1, P3(bx0 + dx, -1.42), z=17) for dx in (-0.35, 0.35)])
        fonte_lab = txt("fonte (esquemática)", 20, DIM).move_to(P3(bx0, 2.62)).set_z_index(16)
        self.play(FadeIn(body), FadeIn(stub_t), FadeIn(stub_b), FadeIn(plate_t), FadeIn(plate_b), FadeIn(pm), FadeIn(fonte_lab), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cps], lag_ratio=0.15), run_time=1.2)
        Ea = VGroup(*[halo(arrow(P3(bx0 - 0.65, 0.95 - dy), P3(bx0 - 0.65, 0.95 - dy - 0.7), CYAN, 6, 18, 0.22)) for dy in (0, 0.9, 1.8)][:2])
        Ea = VGroup(halo(arrow(P3(bx0 - 0.65, 0.65), P3(bx0 - 0.65, -0.15), CYAN, 6, 18, 0.22)),
                    halo(arrow(P3(bx0 - 0.65, -0.35), P3(bx0 - 0.65, -1.15), CYAN, 6, 18, 0.22)))
        Ea_l = MathTex(r"\mathbf E", font_size=40, color=CYAN).move_to(P3(bx0 - 1.15, -0.15)).set_z_index(18)
        self.play(FadeIn(Ea, shift=DOWN * 0.15), FadeIn(Ea_l), run_time=1.2)
        self.wait(1.5)
        Fs = VGroup(halo(arrow(P3(bx0 + 0.65, -1.15), P3(bx0 + 0.65, 0.35), FC, 8, 18, 0.28)),
                    halo(arrow(P3(bx0 + 0.65, 0.2), P3(bx0 + 0.65, 1.0), FC, 8, 18, 0.28)))
        Fs_l = MathTex(r"\mathbf f_s", font_size=40, color=FC).move_to(P3(bx0 + 1.2, -0.15)).set_z_index(18)
        self.play(FadeIn(Fs, shift=UP * 0.2), FadeIn(Fs_l), run_time=1.4)
        n1 = txt("E e f_s coexistem na fonte", T_CAP, WHITE).move_to(P3(COL, 0.9)).set_z_index(30)
        n1 = rich(r"$\mathbf E$ e $\mathbf f_s$ coexistem dentro da fonte", T_CAP).move_to(P3(COL, 0.95)).set_z_index(30)
        n2 = txt("f_s: força não eletrostática por unidade de carga", 20, DIM)
        n2 = rich(r"$\mathbf f_s$: força não eletrostática, por unidade de carga", 20, DIM).move_to(P3(COL, 0.45)).set_z_index(30)
        self.play(FadeIn(n1, shift=UP * 0.1), FadeIn(n2, shift=UP * 0.1), run_time=1.2)
        self.wait(3)
        feq = M(r"\mathbf f", "=", r"\mathbf E", "+", r"\mathbf f_s", size=M_L, width=COLW).move_to(P3(COL, -0.65)).set_z_index(30)
        self.play(Write(feq), run_time=1.6)
        fb = box(feq)
        self.play(FadeIn(fb), run_time=0.6)
        self.wait(4)
        self.src_fig = VGroup(body, stub_t, stub_b, plate_t, plate_b, pm, cps, Ea, Ea_l, Fs, Fs_l, fonte_lab, n1, n2, q)
        self.play(FadeOut(self.src_fig), FadeOut(feq), FadeOut(fb), run_time=1.0)

        # ── FEM ──
        self.next_section("B10_fem")
        self.set_dim(0.6, 1.0)
        u = ValueTracker(0)
        mk = always_redraw(lambda: VGroup(
            Circle(radius=0.14, stroke_width=2, color=WHITE).set_fill(WHITE, 1).move_to(LOOP.at(u.get_value() * LOOP.total)[0]),
            halo(arrow(LOOP.at(u.get_value() * LOOP.total)[0], LOOP.at(u.get_value() * LOOP.total)[0] + 0.45 * LOOP.at(u.get_value() * LOOP.total)[1], WHITE, 5, 40, 0.2), 4)).set_z_index(40))
        mk_lab = MathTex(r"d\boldsymbol\ell", font_size=30, color=WHITE).set_z_index(40)
        nf = txt("FEM não é força", T_BODY, WHITE).move_to(P3(0, 0.95)).set_z_index(30)
        halo(nf)
        d1 = M(r"\mathcal E", "=", r"\oint", r"\mathbf f", r"\cdot d\boldsymbol\ell", size=M_L).move_to(P3(0, 0.2)).set_z_index(30)
        self.add(mk)
        self.play(Write(d1), run_time=1.6)
        self.play(u.animate.set_value(1.0), FadeIn(nf, shift=UP * 0.1), run_time=8, rate_func=linear)
        self.remove(mk)
        self.wait(1)
        self.play(FadeOut(nf), run_time=0.6)
        d2 = M(r"\mathcal E", "=", r"\oint", r"\mathbf E", r"\cdot d\boldsymbol\ell", "+", r"\oint", r"\mathbf f_s", r"\cdot d\boldsymbol\ell",
               size=M_M, width=9.4).move_to(P3(0, 0.5)).set_z_index(30)
        self.play(d1.animate.move_to(P3(0, 0.5)), run_time=0.01)
        self.play(TransformMatchingTex(d1, d2), run_time=2.4)
        self.wait(2)
        hyp = txt("circuito DC estacionário, sem indução magnética nem movimento do circuito", 20, DIM).move_to(P3(0, -0.3)).set_z_index(30)
        self.play(FadeIn(hyp, shift=UP * 0.1), run_time=1.0)
        circ0 = M(r"\oint", r"\mathbf E", r"\cdot d\boldsymbol\ell", "=", "0", size=M_L).move_to(P3(0, -1.05)).set_z_index(30)
        self.play(Write(circ0), run_time=1.6)
        cb = box(circ0, CYAN)
        self.play(FadeIn(cb), run_time=0.6)
        self.wait(3)
        d3 = M(r"\mathcal E", "=", r"\oint", r"\mathbf f_s", r"\cdot d\boldsymbol\ell", size=M_XL, width=9.0).move_to(P3(0, 0.1)).set_z_index(30)
        self.play(FadeOut(hyp), FadeOut(circ0), FadeOut(cb), run_time=0.8)
        self.play(TransformMatchingTex(d2, d3), run_time=2.4)
        fb3 = box(d3, WHITE, 0.22)
        self.play(FadeIn(fb3), run_time=0.6)
        self.wait(3.5)
        self.d3, self.fb3 = d3, fb3

    # ═══ 9-10. ENERGIA E PAYOFF ══════════════════════════════════════════════════════════════════════════
    def energia_e_payoff(self):
        self.next_section("B11_energia")
        self.play(self.d3.animate.scale(0.5).move_to(P3(COL + 0.8, 2.25)).set_opacity(0.6), FadeOut(self.fb3), run_time=1.0)
        p0 = M("p", "=", r"\mathbf J", r"\cdot", r"\mathbf E", size=M_M).move_to(P3(0, 0.8)).set_z_index(30)
        p1 = M("P", "=", "V", "I", "=", "I^2", "R", size=M_M).move_to(P3(0, 0.8)).set_z_index(30)
        self.play(FadeIn(p0, shift=UP * 0.1), run_time=1.0)
        self.wait(2)
        self.play(TransformMatchingTex(p0, p1), run_time=1.6)
        self.wait(2)
        self.play(p1.animate.scale(0.75).move_to(P3(0, 0.95)).set_opacity(0.6), run_time=0.8)
        pf = M(r"P_{\rm fonte}", "=", r"\mathcal E", "I", size=M_L).move_to(P3(0, 0.3)).set_z_index(30)
        eir = M(r"\mathcal E", "=", "I", "R", size=M_M).move_to(P3(0, -0.5)).set_z_index(30)
        self.play(Write(pf), run_time=1.4)
        self.wait(1.5)
        self.play(FadeIn(eir, shift=UP * 0.1), run_time=1.0)
        rn = txt("R: resistência total do modelo ideal", 20, DIM).move_to(P3(0, -1.1)).set_z_index(30)
        self.play(FadeIn(rn), run_time=0.8)
        self.wait(3)
        self.play(FadeOut(pf), FadeOut(eir), FadeOut(rn), FadeOut(p1), run_time=0.8)
        fin = M(r"P_{\rm fonte}", "=", r"\mathcal E", "I", "=", "I^2", "R", "=", r"P_{\rm dissipada}", size=M_M, width=9.6).move_to(P3(0, 0.4)).set_z_index(30)
        self.play(Write(fin), run_time=2.4)
        fbx = box(fin, WHITE, 0.2)
        self.play(FadeIn(fbx), run_time=0.6)
        # balanço esquemático: duas barras iguais
        b_in = Rectangle(width=0.01, height=0.28).set_fill(CYAN, 1).set_stroke(width=0).move_to(P3(-3.6, -0.65)).set_z_index(30)
        b_out = Rectangle(width=0.01, height=0.28).set_fill(CYAN, 0.55).set_stroke(width=0).move_to(P3(-3.6, -1.15)).set_z_index(30)
        t_in = txt("fonte repõe", 20, CYAN).move_to(P3(-5.6, -0.65)).set_z_index(30)
        t_out = txt("resistor dissipa", 20, CYAN).move_to(P3(-5.6, -1.15)).set_z_index(30)
        for t in (t_in, t_out):
            t.set_x(-6.0 + t.width / 2)
        self.play(FadeIn(t_in), FadeIn(t_out), run_time=0.6)
        w = 6.0
        b_in.move_to(P3(-3.6 + 0.005, -0.65))
        b_out.move_to(P3(-3.6 + 0.005, -1.15))
        grow_in = Rectangle(width=w, height=0.28).set_fill(CYAN, 1).set_stroke(width=0).set_z_index(30).move_to(P3(-3.6 + w / 2, -0.65))
        grow_out = Rectangle(width=w, height=0.28).set_fill(CYAN, 0.55).set_stroke(width=0).set_z_index(30).move_to(P3(-3.6 + w / 2, -1.15))
        self.add(b_in, b_out)
        self.play(ReplacementTransform(b_in, grow_in), ReplacementTransform(b_out, grow_out), run_time=2.5)
        self.wait(4)
        self.play(FadeOut(VGroup(fin, fbx, t_in, t_out, grow_in, grow_out, self.d3)), run_time=1.0)

        # ── payoff ──
        self.next_section("B12_payoff")
        self.set_dim(0.0, 1.0)
        # fonte: f_s e E coexistem no próprio circuito
        bx, by = LX, (BAT[0] + BAT[1]) / 2
        fs_a = halo(arrow(P3(bx + 0.75, BAT[0] + 0.05), P3(bx + 0.75, BAT[1] + 0.2), FC, 7, 25, 0.24))
        e_a = halo(arrow(P3(bx - 0.62, BAT[1] - 0.3), P3(bx - 0.62, BAT[0] + 0.25), CYAN, 4, 25, 0.16))
        fs_l = MathTex(r"\mathbf f_s", font_size=36, color=FC).move_to(P3(bx + 0.75, BAT[1] + 0.6)).set_z_index(25)
        self.play(FadeIn(fs_a, shift=UP * 0.15), FadeIn(fs_l), FadeIn(e_a), run_time=1.6)
        self.wait(1.5)
        # legenda sintética no interior do circuito: fonte → campo do circuito → corrente
        n_f = VGroup(MathTex(r"\mathbf f_s", font_size=40, color=FC), txt("na fonte", 20, DIM)).arrange(DOWN, buff=0.12)
        n_e = VGroup(MathTex(r"\mathbf E", font_size=40, color=CYAN), txt("cargas superficiais", 20, BLUE_L)).arrange(DOWN, buff=0.12)
        n_j = VGroup(MathTex(r"\mathbf J", font_size=40, color=GREEN), txt("condução local", 20, DIM)).arrange(DOWN, buff=0.12)
        nodes = VGroup(n_f, n_e, n_j).arrange(RIGHT, buff=1.55).move_to(P3(0.1, -0.2)).set_z_index(30)
        a1 = VGroup(arrow(n_f.get_right() + RIGHT * 0.2, n_e.get_left() + LEFT * 0.2, WHITE, 3, 30, 0.16),
                    txt("repõe energia", 18, DIM)).set_z_index(30)
        a1[1].next_to(a1[0], UP, buff=0.06)
        a2 = VGroup(arrow(n_e.get_right() + RIGHT * 0.2, n_j.get_left() + LEFT * 0.2, WHITE, 3, 30, 0.16),
                    txt("ação local", 18, DIM)).set_z_index(30)
        a2[1].next_to(a2[0], UP, buff=0.06)
        self.play(FadeIn(n_f, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(a1), FadeIn(n_e, shift=UP * 0.1), run_time=1.4)
        self.play(FadeIn(a2), FadeIn(n_j, shift=UP * 0.1), run_time=1.4)
        self.wait(1.5)
        # tudo junto: as quatro camadas sobre o mesmo circuito
        self.play(*[Indicate(g, color=WHITE, scale_factor=1.3) for g in self.G_charges], run_time=1.8)
        self.play(Indicate(self.E_arr, color=WHITE, scale_factor=1.15), Indicate(self.J_arr, color=WHITE, scale_factor=1.15), run_time=1.8)
        self.wait(6)
