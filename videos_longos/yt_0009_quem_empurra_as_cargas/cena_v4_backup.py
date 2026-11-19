"""yt_0009 — Quem empurra as cargas? (campo elétrico, Lei de Ohm, cargas superficiais e FEM). V2.

Preview visual silencioso, 960×540 / 15 fps. Paleta e gramática da série Magnetostática (yt_0005/yt_0006):
E, V, ℰ e energia ciano · J, I e ∇·J verde · carga azul · f e f_s azul-claro FC · geometria violeta · matéria STEEL.

Fio condutor: UM circuito recorrente (fonte + fio + resistor) que ganha camadas: E → J → camada de carga superficial →
potencial V(s) → f_s. Preserva os blocos da V1; reconstrói Ohm, continuidade, cena causal, fonte/FEM, energia e payoff.
"""
import os
import sys
from pathlib import Path

import numpy as np
from manim import (
    AnimationGroup, Arrow, Circle, Create, DashedLine, DashedVMobject, DoubleArrow, Ellipse, FadeIn, FadeOut, ImageMobject, Indicate,
    LaggedStart, Line, MathTex, Mobject, MovingCameraScene, Polygon, Rectangle, ReplacementTransform, RoundedRectangle,
    Cross, SingleStringMathTex, SurroundingRectangle, Text, TransformFromCopy, TransformMatchingTex, VGroup, VMobject, ValueTracker, Write, always_redraw,
    linear, smooth, there_and_back, UP, DOWN, LEFT, RIGHT, UL, UR, ORIGIN,
)
from MF_Tools import TransformByGlyphMap

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import screen_text  # noqa: E402

# ── paleta (idêntica à da Magnetostática) ───────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR
BLUE = "#267BFF"
BLUE_L = "#7FB2FF"
STEEL = "#7A8696"
VIOLET = "#9C8CFF"
FC = "#5AA2FF"
GREEN = "#3FE08B"
PANEL = "#0E2A52"
DIM = "#8FA3C4"

T_BODY, T_NOTE, T_CAP, T_HEAD = 30, 26, 24, 36
M_XL, M_L, M_M, M_S = 54, 48, 40, 32

TOKCOL = {}
for _t in ("I", "J", r"\mathbf J", r"I_{\rm entra}", r"I_{\rm sai}", r"\nabla\cdot\mathbf J", r"\nabla\cdot"):
    TOKCOL[_t] = GREEN
for _t in ("E", "V", r"\mathbf E", r"\mathcal E", "P", "p", r"P_{\rm fonte}", r"P_{\rm dissipada}", r"\Delta V"):
    TOKCOL[_t] = CYAN
for _t in (r"\mathbf f", r"\mathbf f_s"):
    TOKCOL[_t] = FC
for _t in (r"\rho", r"\frac{\partial\rho}{\partial t}", "Q", r"\frac{dQ}{dt}"):
    TOKCOL[_t] = BLUE_L
for _t in ("A", "L", r"\mathbf v_d", r"d\mathbf a", r"d\tau"):
    TOKCOL[_t] = VIOLET


def txt(s, size=T_BODY, color=WHITE, opacity=1.0):
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(opacity)


# ── equações ────────────────────────────────────────────────────────────────────────────────────────────────
def M(*parts, size=M_M, width=None):
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
    """TransformByGlyphMap A→B por termos. pairs: (tokA, tokB[, occA[, occB]]) leva; (tokA, None[, occ]) remove;
    ([(tok, occ), ...], tokB[, occB]) funde vários termos de A num de B. O restante é pareado automaticamente."""
    entries, ua, ub = [], set(), set()
    for p in pairs:
        ta, tb = p[0], p[1]
        if isinstance(ta, list):
            src = [i for (t, o) in ta for lst in _occ(A, t, o) for i in lst]
            ob = p[2] if len(p) > 2 else None
            dst = [i for lst in _occ(B, tb, ob) for i in lst]
            entries.append((src, dst))
            ua.update(src)
            ub.update(dst)
            continue
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
    kw.setdefault("run_time", 2.0)
    if not entries:
        return AnimationGroup(FadeOut(A), FadeIn(B))
    return TransformByGlyphMap(A, B, *entries, auto_fade=True, **kw)


def rich(s, size=T_CAP, color=WHITE):
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


def gi(sym, color, desc, size=21):
    """Item de glossário: símbolo na cor da grandeza + descrição curta."""
    return VGroup(MathTex(sym, font_size=size * 1.25, color=color), txt(": " + desc, size, DIM)).arrange(RIGHT, buff=0.06)


def gloss_line(items, y=-2.78, maxw=13.4):
    g = VGroup(*items).arrange(RIGHT, buff=0.5)
    if g.width > maxw:
        g.scale_to_fit_width(maxw)
    return g.move_to(np.array([0.0, y, 0.0])).set_z_index(30)


def gloss_rows(items, pos):
    return VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(pos).set_z_index(30)


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


def poly(pts, color, op=1.0, z=1, stroke=None):
    p = Polygon(*[P3(*q) for q in pts]).set_fill(color, op).set_z_index(z)
    return p.set_stroke(stroke[0], stroke[1], stroke[2]) if stroke else p.set_stroke(width=0)


def charge(sign, pos, r=0.115, z=7):
    pos = np.asarray(pos, dtype=float)
    c = Circle(radius=r).set_fill(BLUE if sign > 0 else BLUE_L, 1).set_stroke(BACKGROUND_COLOR, 1.2).move_to(pos)
    sc = WHITE if sign > 0 else PANEL
    g = VGroup(c, Line(pos + LEFT * r * 0.55, pos + RIGHT * r * 0.55, stroke_width=2.2, color=sc))
    if sign > 0:
        g.add(Line(pos + DOWN * r * 0.55, pos + UP * r * 0.55, stroke_width=2.2, color=sc))
    return g.set_z_index(z)


def sstep(x):
    x = float(np.clip(x, 0, 1))
    return x * x * (3 - 2 * x)


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

    def seg_of(self, s):
        s = min(max(s, 0.0), self.total - 1e-9)
        i = min(int(np.searchsorted(self.cum, s, side="right")) - 1, len(self.l) - 1)
        return i, (s - self.cum[i]) / self.l[i]

    def seg(self, i, frac):
        return self.at(self.cum[i] + frac * self.l[i])


TOP, BOT, LX, RX, WT = 1.55, -1.95, -5.4, 5.4, 0.5
BAT = (-0.85, 0.45)
RES = (-0.9, 0.5)
LOOP = Loop([(LX, BAT[1]), (LX, TOP), (RX, TOP), (RX, RES[1]), (RX, RES[0]), (RX, BOT), (LX, BOT), (LX, BAT[0]),
             (LX, BAT[1])])
# potencial (conceitual) nos vértices do percurso: cai pouco nos fios, muito no resistor e sobe na fonte
VPTS = [1.0, 0.98, 0.62, 0.60, -0.60, -0.62, -0.98, -1.0, 1.0]


def Vat(s):
    i, f = LOOP.seg_of(s)
    return VPTS[i] + (VPTS[i + 1] - VPTS[i]) * f


E_SPECS = [(0, 0.5, 0.5), (1, 0.2, 0.55), (1, 0.5, 0.55), (1, 0.8, 0.55), (2, 0.5, 0.42), (3, 0.5, 1.05), (4, 0.5, 0.42),
           (5, 0.2, 0.55), (5, 0.5, 0.55), (5, 0.8, 0.55), (6, 0.5, 0.5)]
J_LEN = 0.55
COL = 3.95
COLW = 5.9


def j_phases():
    return [(LOOP.cum[sg] + fr_ * LOOP.l[sg]) / LOOP.total for sg, fr_, _ in E_SPECS]


def lane(seg, frac, off):
    p, t = LOOP.seg(seg, frac)
    n = np.array([-t[1], t[0], 0.0])
    return p + n * off, t


def loop_arrows(kind, z=8):
    g = VGroup()
    for seg, frac, ln in E_SPECS:
        if kind == "E":
            c, t = lane(seg, frac, 0.115)
            L, col = ln, CYAN
        else:
            c, t = lane(seg, frac, -0.115)
            L, col = J_LEN, GREEN
        g.add(halo(arrow(c - t * L / 2, c + t * L / 2, col, 4, z, 0.17), 5))
    return g


def surface_layer(z=7, gain=1.0):
    """Camada de carga superficial contínua: faixa fina na casca do condutor, sinal e intensidade ∝ V(s)."""
    g = VGroup()
    for i in (0, 1, 2, 3, 4, 5, 6):
        half = 0.42 if i == 3 else WT / 2 + 0.02
        n = max(2, int(LOOP.l[i] / 0.2))
        for k in range(n):
            f0, f1 = k / n, (k + 1) / n
            a = LOOP.p[i] + (LOOP.p[i + 1] - LOOP.p[i]) * f0
            b = LOOP.p[i] + (LOOP.p[i + 1] - LOOP.p[i]) * f1
            v = VPTS[i] + (VPTS[i + 1] - VPTS[i]) * (f0 + f1) / 2
            t = (b - a) / np.linalg.norm(b - a)
            nr = np.array([-t[1], t[0], 0.0])
            col = BLUE if v > 0 else BLUE_L
            w = min(1.0, abs(v) * gain)
            for sg in (1, -1):
                off = nr * sg * half
                g.add(Line(a + off, b + off, stroke_width=12, color=col).set_stroke(opacity=0.22 * w))
                g.add(Line(a + off, b + off, stroke_width=4.5, color=col).set_stroke(opacity=0.95 * w))
    return g.set_z_index(z)


def ribbon(z=9):
    """Fita de potencial V(s) acompanhando o circuito, voltada para dentro: fina onde V é baixo, espessa onde é alto."""
    g = VGroup()
    for i in range(8):
        n = max(2, int(LOOP.l[i] / 0.2))
        for k in range(n):
            f0, f1 = k / n, (k + 1) / n
            a = LOOP.p[i] + (LOOP.p[i + 1] - LOOP.p[i]) * f0
            b = LOOP.p[i] + (LOOP.p[i + 1] - LOOP.p[i]) * f1
            t = (b - a) / np.linalg.norm(b - a)
            inw = np.array([t[1], -t[0], 0.0])
            va = VPTS[i] + (VPTS[i + 1] - VPTS[i]) * f0
            vb = VPTS[i] + (VPTS[i + 1] - VPTS[i]) * f1
            ha, hb = 0.1 + 0.46 * (va + 1) / 2, 0.1 + 0.46 * (vb + 1) / 2
            base = 0.4
            q = [a + inw * base, b + inw * base, b + inw * (base + hb), a + inw * (base + ha)]
            g.add(Polygon(*q).set_fill(CYAN, 0.32).set_stroke(width=0))
            g.add(Line(q[3], q[2], stroke_width=3, color=CYAN))
    return g.set_z_index(z)


def pipe(x0, y0, x1, y1, horiz, z=2):
    g = VGroup(rect(x0, y0, x1, y1, STEEL, 1, z))
    if horiz:
        g.add(rect(x0, y1 - 0.1, x1, y1 - 0.03, WHITE, 0.3, z + 1), rect(x0, y1 - 0.22, x1, y1 - 0.12, WHITE, 0.09, z + 1),
              rect(x0, y0, x1, y0 + 0.13, PANEL, 0.45, z + 1))
    else:
        g.add(rect(x0 + 0.03, y0, x0 + 0.1, y1, WHITE, 0.3, z + 1), rect(x0 + 0.12, y0, x0 + 0.22, y1, WHITE, 0.09, z + 1),
              rect(x1 - 0.13, y0, x1, y1, PANEL, 0.45, z + 1))
    return g


AUDIT = os.environ.get("AUDIT") == "1"
_TXT = (Text, MathTex, SingleStringMathTex)


def _units(m, out):
    if isinstance(m, _TXT):
        out.append(m)
        return
    for sm in m.submobjects:
        _units(sm, out)


def _opac(m):
    fam = m.family_members_with_points()
    return max([sm.get_fill_opacity() for sm in fam] + [sm.get_stroke_opacity() for sm in fam] + [0.0])


class QuemEmpurraCargasYT009(MovingCameraScene):
    # ── auditoria de layout (AUDIT=1): texto/fórmula sobreposto ou fora da área segura ─────────────────────
    def _audit(self, tag=""):
        if not AUDIT or abs(self.fr.width - self.fw0) > 0.05:
            return
        us = []
        for m in self.mobjects:
            _units(m, us)
        dim_o = self.dim.get_fill_opacity()
        vis = []
        for u in us:
            if u is self.tag or _opac(u) < 0.25 or u.width < 1e-3:
                continue
            if dim_o > 0.5 and u.z_index < 12:
                continue
            vis.append(u)
        t = round(self.renderer.time, 1)
        names = lambda u: (getattr(u, "text", None) or getattr(u, "tex_string", "") or "?")[:34]
        for i, a in enumerate(vis):
            if abs(a.get_center()[0]) > 7.45 or abs(a.get_center()[1]) > 4.1 or a.get_right()[0] > 7.75 or a.get_left()[0] < -7.75:
                self._issues.setdefault(("borda", names(a)), t)
            for b in vis[i + 1:]:
                ox = min(a.get_right()[0], b.get_right()[0]) - max(a.get_left()[0], b.get_left()[0])
                oy = min(a.get_top()[1], b.get_top()[1]) - max(a.get_bottom()[1], b.get_bottom()[1])
                if ox > 0.05 and oy > 0.05:
                    self._issues.setdefault((names(a), names(b)), t)

    def wait(self, *a, **k):
        self._audit()
        super().wait(*a, **k)

    def play(self, *a, **k):
        super().play(*a, **k)
        self._audit()

    def tear_down(self):
        if AUDIT:
            print("[AUDIT] sobreposições:", len(self._issues))
            for (a, b), t in sorted(self._issues.items(), key=lambda kv: kv[1]):
                print(f"[AUDIT] t={t:6.1f}  {a!r}  x  {b!r}")
        super().tear_down()

    def add_shimmer(self, g, phases, base=0.5):
        def upd(m):
            t = self.clk.get_value()
            for arr, ph in zip(m, phases):
                arr.set_opacity(base + (1 - base) * np.sin(np.pi * (t * 0.45 - ph)) ** 2)
        g.add_updater(upd)

    def construct(self):
        self._issues = {}
        self.clk = ValueTracker(0)
        self.clk.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(self.clk)
        self.camera.background_color = BACKGROUND_COLOR
        fr = self.camera.frame
        self.fr = fr
        self.fw0 = fr.width
        self.tag = txt("LEI DE OHM E FORÇA ELETROMOTRIZ", 18, opacity=0.6).to_corner(UL, buff=0.38).set_z_index(40)
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3)
        self.wm.set_z_index(40)
        tag_h, wm_w = self.tag.height, self.wm.width
        tag_off = self.tag.get_center() - fr.get_corner(UL)
        wm_off = self.wm.get_center() - fr.get_corner(UR)
        self.dim = Rectangle(width=16.8, height=9.6).set_fill(BACKGROUND_COLOR, 0).set_stroke(width=0).set_z_index(12)

        def hud(_m):
            r = fr.width / self.fw0
            self.tag.set_height(tag_h * r).move_to(fr.get_corner(UL) + tag_off * r)
            self.wm.set_width(wm_w * r).move_to(fr.get_corner(UR) + wm_off * r)
            self.dim.set_width(16.8 * r).move_to(fr.get_center())

        self.hud_dummy = Mobject()
        self.hud_dummy.add_updater(hud)
        self.add(self.tag, self.wm, self.dim, self.hud_dummy)
        self.build_circuit()
        self.introducao()
        self.abertura_local()
        self.conducao_local()
        self.ohm_macroscopica()
        self.continuidade()
        self.cargas_superficiais()
        self.regime_estacionario()
        self.fonte_e_fem()
        self.energia_e_payoff()
        self.encerramento()
        self.wait(1)

    # ── utilidades ──────────────────────────────────────────────────────────────────────────────────────────
    def set_dim(self, o, rt=1.0):
        self.play(self.dim.animate.set_fill(BACKGROUND_COLOR, o), run_time=rt)

    def chips(self, active):
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

    # ── circuito recorrente (2.5D) ──────────────────────────────────────────────────────────────────────────
    def build_circuit(self):
        h = WT / 2
        pcs = [(LX - h, TOP - h, RX + h, TOP + h, True), (LX - h, BOT - h, RX + h, BOT + h, True),
               (LX - h, BAT[1], LX + h, TOP - h, False), (LX - h, BOT + h, LX + h, BAT[0], False),
               (RX - h, RES[1], RX + h, TOP - h, False), (RX - h, BOT + h, RX + h, RES[0], False)]
        shadow = VGroup(*[rect(a + 0.1, b - 0.12, c + 0.1, d - 0.12, "#000000", 0.45, 0) for a, b, c, d, _ in pcs])
        outline = VGroup(*[rect(a - .04, b - .04, c + .04, d + .04, PANEL, 1, 1) for a, b, c, d, _ in pcs])
        wires = VGroup(*[pipe(a, b, c, d, hz) for a, b, c, d, hz in pcs])
        bw, bh = 0.95, BAT[1] - BAT[0]
        bx, by = LX, (BAT[0] + BAT[1]) / 2
        dx, dy = 0.2, 0.15
        body = VGroup(
            poly([(bx + bw / 2, by + bh / 2), (bx + bw / 2 + dx, by + bh / 2 + dy), (bx + bw / 2 + dx, by - bh / 2 + dy), (bx + bw / 2, by - bh / 2)], PANEL, 0.7, 4),
            poly([(bx - bw / 2, by + bh / 2), (bx + bw / 2, by + bh / 2), (bx + bw / 2 + dx, by + bh / 2 + dy), (bx - bw / 2 + dx, by + bh / 2 + dy)], BLUE_L, 0.4, 4),
            RoundedRectangle(corner_radius=0.08, width=bw, height=bh, stroke_width=2).set_fill(PANEL, 1).set_stroke(BLUE_L, 2, 0.9)
            .move_to(P3(bx, by)).set_z_index(5),
            Line(P3(bx - .36, BAT[1] - .3), P3(bx + .36, BAT[1] - .3), stroke_width=5, color=WHITE).set_z_index(6),
            Line(P3(bx - .2, BAT[1] - .62), P3(bx + .2, BAT[1] - .62), stroke_width=5, color=WHITE).set_z_index(6))
        bat_pm = VGroup(MathTex("+", font_size=34, color=WHITE).move_to(P3(LX - .82, BAT[1] - .3)),
                        MathTex("-", font_size=34, color=WHITE).move_to(P3(LX - .82, BAT[1] - .62))).set_z_index(6)
        rw, rh = 0.8, RES[1] - RES[0]
        zz = [P3(RX, RES[1])] + [P3(RX + (0.18 if i % 2 else -0.18), RES[1] - (i + 0.5) * rh / 8) for i in range(8)] + [P3(RX, RES[0])]
        res = VGroup(
            RoundedRectangle(corner_radius=0.08, width=rw, height=rh, stroke_width=2).set_fill(PANEL, 1).set_stroke(BLUE_L, 2, 0.9)
            .move_to(P3(RX, (RES[0] + RES[1]) / 2)).set_z_index(5),
            rect(RX - rw / 2 + 0.04, RES[0] + 0.05, RX - rw / 2 + 0.1, RES[1] - 0.05, WHITE, 0.25, 6),
            VMobject().set_points_as_corners(zz).set_stroke(WHITE, 3).set_z_index(6))
        self.lbl_bat = txt("fonte", 22, DIM).move_to(P3(LX - 1.2, BAT[0] - 0.4)).set_z_index(5)
        self.lbl_res = txt("resistor", 22, DIM).move_to(P3(RX + 1.15, RES[0] - 0.4)).set_z_index(5)
        self.bat_g, self.res_g = VGroup(body, bat_pm), res
        self.base = VGroup(shadow, outline, wires)
        self.world = VGroup(self.base, self.bat_g, self.res_g, self.lbl_bat, self.lbl_res)

    # ═══ 0. INTRODUÇÃO: gancho de curiosidade (o que você vai entender) ═══════════════════════════════════════
    def make_backdrop(self, op=0.35, z=-1, sc=1.5):
        """Circuito esquemático ao fundo com pulsos de corrente: mantém a tela viva sem competir com o conteúdo."""
        outline = VMobject().set_points_as_corners([*(LOOP.p * sc)]).set_stroke(STEEL, 7, opacity=op * 0.7).set_z_index(z - 1)
        pul = VGroup(*[Line(ORIGIN, RIGHT * 0.3, stroke_width=8, color=GREEN).set_z_index(z) for _ in range(16)])

        def upd(m):
            t = self.clk.get_value()
            for i, ln in enumerate(m):
                p, tg = LOOP.at((i / 16 + t * 0.05) * LOOP.total)
                ln.put_start_and_end_on(p * sc, p * sc + tg * 0.3)
                ln.set_stroke(opacity=op)

        pul.add_updater(upd)
        return VGroup(outline, pul)

    def introducao(self):
        self.next_section("B00_introducao")
        back = self.make_backdrop(0.4)
        self.add(back)
        logo0 = ImageMobject(str(WATERMARK_PATH)).set_width(3.8).move_to(P3(0, 1.05)).set_z_index(30)
        welcome = txt("Bem-vindos ao Parallax Lab", 40, WHITE).move_to(P3(0, -0.35)).set_z_index(30)
        self.play(FadeIn(logo0, shift=UP * 0.1), FadeIn(welcome, shift=UP * 0.1), run_time=1.6)
        self.wait(2.2)
        self.play(FadeOut(logo0), FadeOut(welcome), run_time=0.8)
        title = txt("Quem empurra as cargas?", 56, WHITE).move_to(P3(0, 0.9)).set_z_index(30)
        halo(title, 8)
        sub = txt("Campo elétrico, Lei de Ohm e força eletromotriz", 28, DIM).move_to(P3(0, -0.2)).set_z_index(30)
        hook = txt("A bateria está de um lado. O resistor, do outro. O que age sobre uma carga no meio do fio?", T_CAP, CYAN).move_to(P3(0, -1.5)).set_z_index(30)
        self.play(FadeIn(title, shift=UP * 0.15), run_time=1.6)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=1.0)
        self.wait(1.2)
        self.play(FadeIn(hook, shift=UP * 0.1), run_time=1.0)
        self.wait(3.2)
        self.play(FadeOut(hook), FadeOut(back), title.animate.scale(0.72).move_to(P3(0, 2.5)), sub.animate.scale(0.8).move_to(P3(0, 1.75)), run_time=1.4)
        lead = txt("Neste vídeo vamos aprender:", T_CAP, CYAN).move_to(P3(0, 1.2)).set_z_index(30)
        self.play(FadeIn(lead), run_time=0.6)
        cards = [
            ("Quem age sobre uma carga num fio distante?", r"\mathbf J=\sigma\mathbf E", GREEN),
            ("De onde nasce a Lei de Ohm?", r"V=IR", CYAN),
            ("Quem cria o campo ao longo do circuito?", r"\nabla\cdot\mathbf J=0", GREEN),
            ("O que a fonte realmente faz?", r"\mathcal E=\oint\mathbf f_s\cdot d\boldsymbol\ell", FC),
        ]
        grid = [P3(-3.7, 0.0), P3(3.7, 0.0), P3(-3.7, -1.85), P3(3.7, -1.85)]
        made = []
        for (q, tex, col), pos in zip(cards, grid):
            pn = panel(6.9, 1.6, pos, op=0.9, z=20)
            qt = txt(q, 22, WHITE).move_to(pos + UP * 0.45).set_z_index(30)
            eq = MathTex(tex, font_size=44, color=col).move_to(pos + DOWN * 0.3).set_z_index(30)
            made.append(VGroup(pn, qt, eq))
            self.play(FadeIn(pn, shift=UP * 0.15), FadeIn(qt, shift=UP * 0.1), run_time=0.9)
            self.play(Write(eq), run_time=1.1)
            self.wait(1.2)
        self.wait(1.5)
        self.play(FadeOut(VGroup(*made)), FadeOut(lead), FadeOut(title), FadeOut(sub), run_time=1.2)
        back.clear_updaters()

    # ═══ 13. ENCERRAMENTO: chamada para ação ═══════════════════════════════════════════════════════════════
    def encerramento(self):
        self.next_section("B13_encerramento")
        back = self.make_backdrop(0.4, z=13, sc=1.7)
        self.add(back)
        logo = ImageMobject(str(WATERMARK_PATH)).set_width(4.4).move_to(P3(0, 1.75)).set_z_index(30)
        self.play(FadeIn(logo, shift=UP * 0.1), run_time=1.2)
        head = txt("Gostou? Então não deixe de acompanhar.", 34, WHITE).move_to(P3(0, 0.45)).set_z_index(30)
        self.play(FadeIn(head, shift=UP * 0.1), run_time=1.0)
        pills = VGroup()
        for label, col in (("CURTIR", BLUE_L), ("INSCREVER-SE", CYAN), ("COMENTAR", GREEN)):
            t = txt(label, 24, WHITE)
            r = RoundedRectangle(corner_radius=0.3, width=t.width + 0.9, height=0.7, stroke_width=2.5)
            r.set_fill(PANEL, 0.95).set_stroke(col, 2.5, 1.0)
            pills.add(VGroup(r, t.move_to(r)))
        pills.arrange(RIGHT, buff=0.55).move_to(P3(0, -0.7)).set_z_index(30)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in pills], lag_ratio=0.25), run_time=1.6)
        ask = txt("Qual parte te surpreendeu mais? Conta nos comentários.", 24, DIM).move_to(P3(0, -1.75)).set_z_index(30)
        self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.9)
        for p in pills:
            self.play(Indicate(p, color=WHITE, scale_factor=1.12), run_time=1.0)
        self.wait(1.5)
        sig = txt("Parallax Lab", 22, DIM).move_to(P3(0, -2.65)).set_z_index(30)
        self.play(FadeIn(sig), run_time=0.8)
        self.wait(5.0)

    # ═══ 1. QUEM AGE LOCALMENTE ═════════════════════════════════════════════════════════════════════════════
    def abertura_local(self):
        self.next_section("B01_gancho")
        fr = self.fr
        self.play(LaggedStart(FadeIn(self.base[0]), FadeIn(self.base[1]), FadeIn(self.base[2]), FadeIn(self.bat_g),
                              FadeIn(self.res_g), lag_ratio=0.25), run_time=3)
        self.play(FadeIn(self.lbl_bat), FadeIn(self.lbl_res), run_time=0.8)
        ring = Circle(radius=0.95, color=CYAN, stroke_width=3).move_to(P3(LX, (BAT[0] + BAT[1]) / 2)).set_z_index(9)
        self.play(FadeIn(ring, scale=1.3), Indicate(self.bat_g, color=WHITE, scale_factor=1.1), run_time=1.6)
        self.play(FadeOut(ring), run_time=0.4)
        # câmera de verdade: acompanha o fio da fonte até um trecho distante
        self.play(fr.animate.scale(0.45).move_to(P3(-4.2, 0.4)), run_time=3.0)
        self.wait(0.8)
        self.play(fr.animate.move_to(P3(3.4, 1.0)), run_time=7.0)
        cpos = P3(3.3, TOP)
        carrier = VGroup(Circle(radius=0.11, stroke_width=0).set_fill(BLUE_L, 1).move_to(cpos),
                         Line(cpos + LEFT * .06, cpos + RIGHT * .06, stroke_width=2.5, color=PANEL)).set_z_index(9)
        carrier.move_to(cpos)
        cring = Circle(radius=0.3, color=WHITE, stroke_width=3).move_to(cpos).set_z_index(9)
        self.play(FadeIn(carrier, scale=0.4), FadeIn(cring, scale=1.8), run_time=1.0)
        cring.add_updater(lambda m: m.set_stroke(opacity=0.45 + 0.55 * np.sin(np.pi * self.clk.get_value() * 0.9) ** 2))
        r = fr.width / self.fw0
        q = txt("Que força age aqui, agora?", T_HEAD).scale(r).move_to(fr.get_center() + DOWN * 1.65 * r).set_z_index(30)
        halo(q)
        self.play(FadeIn(q, shift=UP * 0.1), Indicate(cring, color=CYAN, scale_factor=1.3), run_time=1.4)
        self.wait(2.5)
        # mergulho no fio
        self.play(fr.animate.scale(0.42).move_to(cpos), FadeOut(q), run_time=3.2)
        cring.clear_updaters()
        self.hook_extra = VGroup(carrier, cring)

    # ═══ 2. CONDUÇÃO LOCAL: E → J = σE ═════════════════════════════════════════════════════════════════════
    def conducao_local(self):
        self.next_section("B02_conducao_local")
        # corte microscópico 2.5D: planos de rede em profundidade, elétrons em camadas, leve parallax
        x0, x1, cy, hh = -7.0, 0.1, -0.15, 2.6
        dx, dy = 0.42, 0.3
        front = Rectangle(width=x1 - x0, height=hh).set_fill(STEEL, 0.15).set_stroke(STEEL, 3).move_to(P3((x0 + x1) / 2, cy)).set_z_index(1)
        back = Rectangle(width=x1 - x0, height=hh).set_fill(STEEL, 0.06).set_stroke(STEEL, 1.5, 0.5).move_to(P3((x0 + x1) / 2 + dx, cy + dy)).set_z_index(0)
        edges = VGroup(*[Line(P3(x, y), P3(x + dx, y + dy), stroke_width=1.5, color=STEEL).set_stroke(opacity=0.5)
                         for x, y in ((x0, cy - hh / 2), (x1, cy - hh / 2), (x0, cy + hh / 2), (x1, cy + hh / 2))]).set_z_index(0)
        topf = poly([(x0, cy + hh / 2), (x1, cy + hh / 2), (x1 + dx, cy + hh / 2 + dy), (x0 + dx, cy + hh / 2 + dy)], WHITE, 0.07, 0)
        ions_f = VGroup(*[Circle(radius=0.085, stroke_width=0).set_fill(STEEL, 0.55).move_to(P3(x, y)).set_z_index(1)
                          for x in np.arange(x0 + 0.6, x1 - 0.2, 0.95) for y in np.arange(cy - 0.95, cy + 1.15, 0.7)])
        ions_b = VGroup(*[Circle(radius=0.06, stroke_width=0).set_fill(STEEL, 0.3).move_to(P3(x + 0.45 + dx, y + dy)).set_z_index(0)
                          for x in np.arange(x0 + 0.6, x1 - 0.5, 0.95) for y in np.arange(cy - 0.6, cy + 1.0, 0.7)])
        rng = np.random.default_rng(11)
        N = 26
        pos = np.column_stack([rng.uniform(x0 + .3, x1 - .3, N), rng.uniform(cy - hh / 2 + .2, cy + hh / 2 - .2, N)])
        depth = np.array([i % 3 / 2 for i in range(N)])        # 0 (frente), 0.5, 1 (fundo)
        ang = rng.uniform(0, 2 * np.pi, N)
        vel = np.column_stack([np.cos(ang), np.sin(ang)]) * rng.uniform(0.9, 1.5, N)[:, None]
        elec = VGroup(*[Circle(radius=0.085 - 0.022 * d, stroke_width=0).set_fill(BLUE_L, 1.0 - 0.5 * d).set_z_index(5 - int(2 * d))
                        for d in depth])
        drift, clock, Dd = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        vd = 0.32
        st = {"p": pos, "v": vel}

        def step(m, dt):
            dt = min(dt, 0.1)
            p, v = st["p"], st["v"]
            hit = rng.random(N) < 2.2 * dt
            a = rng.uniform(0, 2 * np.pi, N)
            v[hit] = (np.column_stack([np.cos(a), np.sin(a)]) * rng.uniform(0.9, 1.5, N)[:, None])[hit]
            p += (v + np.array([-vd * drift.get_value(), 0.0])) * dt
            p[:, 0] = np.where(p[:, 0] < x0 + .2, x1 - .25, np.where(p[:, 0] > x1 - .2, x0 + .25, p[:, 0]))
            bad = (p[:, 1] < cy - hh / 2 + .15) | (p[:, 1] > cy + hh / 2 - .15)
            v[bad, 1] *= -1
            p[:, 1] = np.clip(p[:, 1], cy - hh / 2 + .15, cy + hh / 2 - .15)
            clock.increment_value(dt)
            Dd.set_value(min(3.4, Dd.get_value() + vd * drift.get_value() * dt))
            sw = np.array([0.07 * np.sin(0.7 * clock.get_value()), 0.035 * np.cos(0.5 * clock.get_value())])
            for i, e in enumerate(m):
                e.move_to(P3(*(p[i] + depth[i] * np.array([dx, dy]) + depth[i] * sw)))

        elec.add_updater(step)
        micro = VGroup(front, back, edges, topf, ions_f, ions_b, elec)
        self.micro = micro
        # corta o macro sob um escurecimento rápido e entra no corte
        self.play(self.dim.animate.set_fill(BACKGROUND_COLOR, 1.0), run_time=0.7)
        self.remove(*self.hook_extra)
        self.fr.move_to(ORIGIN)
        self.fr.scale(self.fw0 / self.fr.width)
        self.remove(self.base[0], self.base[1], self.base[2], self.bat_g, self.res_g, self.lbl_bat, self.lbl_res)
        self.add(micro)
        note0 = txt("dentro do fio: elétrons em movimento irregular", T_CAP, DIM).move_to(P3(-3.2, -2.35))
        self.play(self.dim.animate.set_fill(BACKGROUND_COLOR, 0.0), FadeIn(note0), run_time=1.2)
        self.wait(3.5)
        # E aparece: resposta local
        e_arrows = VGroup(*[halo(arrow(P3(x - 0.6, cy + 0.95), P3(x + 0.6, cy + 0.95), CYAN, 5, 9, 0.22)) for x in (-5.6, -3.4, -1.2)])
        e_lab = MathTex(r"\mathbf E", font_size=44, color=CYAN).move_to(P3(-6.3, cy + 1.7))
        halo(e_lab)
        note1 = txt("campo elétrico local", T_CAP, CYAN).next_to(e_lab, RIGHT, buff=0.25)
        self.play(LaggedStart(*[FadeIn(a, shift=RIGHT * 0.2) for a in e_arrows], lag_ratio=0.25), FadeIn(e_lab), FadeIn(note1), run_time=1.6)
        self.wait(1.0)
        # a deriva média nasce: o conjunto desliza, pouco; o centro do conjunto marca o deslocamento médio
        xc0 = -1.0
        ghost = DashedLine(P3(xc0, cy - hh / 2 - 0.15), P3(xc0, cy + hh / 2 + 0.15), color=WHITE, stroke_width=2).set_stroke(opacity=0.6).set_z_index(6)
        cur = always_redraw(lambda: Line(P3(xc0 - Dd.get_value(), cy - hh / 2 - 0.15), P3(xc0 - Dd.get_value(), cy + hh / 2 + 0.15),
                                         color=VIOLET, stroke_width=4).set_z_index(6))
        d_arr = always_redraw(lambda: halo(arrow(P3(xc0, cy - hh / 2 - 0.4), P3(xc0 - max(Dd.get_value(), 0.02), cy - hh / 2 - 0.4), VIOLET, 5, 9, 0.2)))
        d_lab = MathTex(r"\mathbf v_d", font_size=40, color=VIOLET).move_to(P3(-2.6, cy - hh / 2 - 0.72))
        d_note = txt("deslocamento médio do conjunto", T_CAP, VIOLET).next_to(d_lab, RIGHT, buff=0.25)
        d_lab.set_opacity(0)
        d_note.set_opacity(0)
        self.add(cur, d_arr, d_lab, d_note)
        self.play(drift.animate.set_value(1.0), FadeOut(note0), FadeIn(ghost), run_time=2.0)
        self.play(d_lab.animate.set_opacity(1), d_note.animate.set_opacity(1), run_time=0.8)
        self.wait(5.5)
        j_arr = halo(arrow(P3(-5.6, -2.55), P3(-2.2, -2.55), GREEN, 7, 9, 0.28))
        j_lab = MathTex(r"\mathbf J", font_size=44, color=GREEN).next_to(j_arr, LEFT, buff=0.2)
        j_note = txt("corrente macroscópica", T_CAP, GREEN).next_to(j_arr, RIGHT, buff=0.25)
        self.play(FadeOut(d_note), FadeOut(d_lab), run_time=0.4)
        self.play(FadeIn(j_arr, shift=RIGHT * 0.3), FadeIn(j_lab), FadeIn(j_note), run_time=1.4)
        self.wait(1.0)
        # checagem de sinal: elétrons derivam contra E, mas J ∥ E
        k0 = M(r"\mathbf J", "=", "nq", r"\mathbf v_d", size=M_L).move_to(P3(COL, 1.55))
        k1 = M(r"\mathbf J", "=", "-ne", r"\mathbf v_d", size=M_L).move_to(P3(COL, 1.55))
        k_note0 = rich("portadores: elétrons, $q=-e$", T_CAP).move_to(P3(COL, 0.7))
        k_par = M(r"\mathbf J", r"\parallel", r"\mathbf E", size=M_L).move_to(P3(COL, -0.7))
        self.play(Write(k0), run_time=1.5)
        self.wait(1.0)
        self.play(FadeIn(k_note0, shift=UP * 0.1), TransformMatchingTex(k0, k1), run_time=1.6)
        self.wait(1.0)
        k_note1 = rich("$\\mathbf v_d$ oposta a $\\mathbf E$ : $\\mathbf J$ no sentido de $\\mathbf E$", 22, DIM).move_to(P3(COL, 0.1))
        self.play(FadeOut(k_note0), FadeIn(k_note1, shift=UP * 0.1), run_time=1.0)
        self.wait(2.0)
        self.play(FadeIn(k_par, shift=UP * 0.1), run_time=1.0)
        kb = box(k_par, GREEN)
        self.play(FadeIn(kb), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(VGroup(k1, k_note1, k_par, kb)), run_time=0.8)
        # fórmula local, depois do fenômeno
        eq0 = M(r"\mathbf J", "=", r"\sigma", r"\mathbf f", size=M_L).move_to(P3(COL, 1.2))
        eq1 = M(r"\mathbf J", "=", r"\sigma", r"\mathbf E", size=M_L).move_to(eq0)
        note_f = rich("no trecho resistivo: $\\mathbf f=\\mathbf E$", T_CAP).move_to(P3(COL, 0.1))
        self.play(Write(eq0), run_time=1.5)
        self.play(FadeIn(note_f, shift=UP * 0.1), run_time=0.8)
        self.wait(1.0)
        self.play(TransformMatchingTex(eq0, eq1), run_time=1.5)
        bx = box(eq1)
        self.play(FadeIn(bx), run_time=0.6)
        self.wait(2.0)
        elec.clear_updaters()
        cur.clear_updaters()
        d_arr.clear_updaters()
        self.micro_ui = VGroup(note1, e_lab, e_arrows, ghost, cur, d_arr, j_arr, j_lab, j_note)
        self.micro_eq = VGroup(eq1, bx, note_f)

    # ═══ 3-4. DA LEI LOCAL PARA V = IR ═════════════════════════════════════════════════════════════════════
    def ohm_macroscopica(self):
        self.next_section("B03_ohm_macro")
        # fio macroscópico 2.5D: mesmo objeto, agora com seção A, comprimento L e queda V
        wx0, wx1, wy, wh = -6.0, 0.0, 0.3, 1.1
        mbody = pipe(wx0, wy - wh / 2, wx1, wy + wh / 2, True, 2)
        face = Ellipse(width=0.42, height=wh).set_fill(VIOLET, 0.35).set_stroke(VIOLET, 3).move_to(P3(wx1, wy)).set_z_index(4)
        rim = Ellipse(width=0.42, height=wh).set_fill(STEEL, 1).set_stroke(PANEL, 1).move_to(P3(wx0, wy)).set_z_index(2)
        A_lab = MathTex("A", font_size=44, color=VIOLET).move_to(P3(0.65, wy + 0.15))
        Lline = DoubleArrow(P3(wx0, -0.55), P3(wx1, -0.55), buff=0, color=VIOLET, stroke_width=4, tip_length=0.18)
        L_lab = MathTex("L", font_size=44, color=VIOLET).move_to(P3(-3.0, -0.95))
        Vline = VGroup(Line(P3(wx0, 1.25), P3(wx1, 1.25), stroke_width=4, color=CYAN),
                       Line(P3(wx0, 1.15), P3(wx0, 1.35), stroke_width=4, color=CYAN),
                       Line(P3(wx1, 1.15), P3(wx1, 1.35), stroke_width=4, color=CYAN))
        V_lab = MathTex("V", font_size=44, color=CYAN).move_to(P3(-3.0, 1.62))
        Vtxt = txt("queda de potencial", T_CAP, CYAN).next_to(V_lab, RIGHT, buff=0.2)
        I_arr = halo(arrow(P3(-7.0, wy), P3(-6.1, wy), GREEN, 8, 9, 0.26))
        I_lab = MathTex("I", font_size=44, color=GREEN).move_to(P3(-6.6, wy + 0.5))
        mE = VGroup(*[halo(arrow(P3(x - .55, wy + .24), P3(x + .55, wy + .24), CYAN, 4, 9, 0.18), 5) for x in (-5.0, -3.0, -1.0)])
        mJ = VGroup(*[halo(arrow(P3(x - .55, wy - .2), P3(x + .55, wy - .2), GREEN, 4, 9, 0.18), 5) for x in (-5.0, -3.0, -1.0)])
        j_face = VGroup(*[halo(arrow(P3(wx1 - 0.3, wy + dy), P3(wx1 + 0.45, wy + dy), GREEN, 4, 10, 0.16), 4) for dy in (-0.3, 0.0, 0.3)])
        self.play(FadeOut(self.micro), FadeOut(self.micro_ui), FadeOut(self.micro_eq), run_time=1.2)
        self.remove(self.micro)
        self.play(FadeIn(mbody), FadeIn(rim), run_time=1.0)
        self.play(FadeIn(I_arr), FadeIn(I_lab), FadeIn(mJ), FadeIn(mE), run_time=1.0)
        self.add_shimmer(mJ, [0.0, 0.33, 0.66])
        self.gl_ohm = gloss_line([gi("J", GREEN, "densidade de corrente"), gi("I", GREEN, "corrente"), gi("A", VIOLET, "área da seção"),
                                  gi("L", VIOLET, "comprimento do trecho"), gi("V", CYAN, "queda de potencial")])
        self.play(FadeIn(self.gl_ohm), run_time=0.8)
        # origem de I = JA: a seção A acende e J a atravessa
        self.play(FadeIn(face), FadeIn(A_lab), run_time=0.8)
        self.play(FadeIn(j_face, shift=RIGHT * 0.15), face.animate.set_fill(VIOLET, 0.6), run_time=1.0)
        i0 = EQ(r"I=\int_{A}\mathbf J\cdot d\mathbf a", "I", r"\mathbf J", "A", r"d\mathbf a", size=M_M, width=COLW).move_to(P3(COL, 0.2))
        i1 = EQ(r"I=JA", "I", "J", "A", size=M_L, width=COLW).move_to(P3(COL, 0.2))
        i2 = EQ(r"J=\frac{I}{A}", "J", "I", "A", size=M_L, width=COLW).move_to(P3(COL, 0.2))
        n_u = txt("J uniforme na seção", T_CAP, DIM).move_to(P3(COL, -0.65))
        self.play(Write(i0), run_time=1.8)
        self.play(Indicate(face, color=WHITE), run_time=1.2)
        self.play(FadeIn(n_u, shift=UP * 0.1), run_time=0.8)
        self.wait(0.8)
        self.play(gmap(i0, i1, ("I", "I"), (r"\mathbf J", "J"), ("A", "A")), FadeOut(n_u), run_time=2.0)
        self.add(i1)
        self.wait(0.8)
        self.play(gmap(i1, i2, ("I", "I"), ("J", "J"), ("A", "A")), run_time=1.8)
        self.add(i2)
        self.play(i2.animate.scale(0.75).move_to(P3(COL, 2.35)), FadeOut(j_face), face.animate.set_fill(VIOLET, 0.35), run_time=1.0)
        # origem de V = EL: o caminho L acende e E o percorre
        self.play(FadeIn(Lline), FadeIn(L_lab), FadeIn(Vline), FadeIn(V_lab), FadeIn(Vtxt), run_time=1.0)
        path = Line(P3(wx0, wy), P3(wx1, wy), stroke_width=5, color=CYAN).set_z_index(8).set_stroke(opacity=0.0)
        self.add(path)
        self.play(path.animate.set_stroke(opacity=0.9), Indicate(mE, color=WHITE), run_time=1.4)
        v0 = EQ(r"V=\left|\int_0^{L}\mathbf E\cdot d\boldsymbol\ell\right|", "V", "L", r"\mathbf E", size=M_M, width=COLW).move_to(P3(COL, 0.2))
        v1 = EQ(r"V=EL", "V", "E", "L", size=M_L, width=COLW).move_to(P3(COL, 0.2))
        v2 = EQ(r"E=\frac{V}{L}", "E", "V", "L", size=M_L, width=COLW).move_to(P3(COL, 0.2))
        n_e = txt("E uniforme, paralelo ao caminho", T_CAP, DIM).move_to(P3(COL, -0.65))
        self.play(Write(v0), run_time=1.8)
        self.play(FadeIn(n_e, shift=UP * 0.1), run_time=0.8)
        self.wait(0.8)
        self.play(gmap(v0, v1, ("V", "V"), (r"\mathbf E", "E"), ("L", "L")), FadeOut(n_e), run_time=2.0)
        self.add(v1)
        self.wait(0.8)
        self.play(gmap(v1, v2, ("V", "V"), ("E", "E"), ("L", "L")), run_time=1.8)
        self.add(v2)
        self.play(v2.animate.scale(0.75).move_to(P3(COL, 1.45)), FadeOut(path), run_time=1.0)
        r3 = M("J", "=", r"\sigma", "E", size=M_S).scale(0.75).move_to(P3(COL, 0.65))
        self.play(FadeIn(r3, shift=RIGHT * 0.2), Indicate(mE, color=WHITE), Indicate(mJ, color=WHITE), run_time=1.6)
        rels = VGroup(i2, v2, r3)
        self.macro = VGroup(mbody, rim, face, A_lab, Lline, L_lab, Vline, V_lab, Vtxt, I_arr, I_lab, mE, mJ)

        self.next_section("B04_ohm_derivacao")
        C0 = EQ(r"J=\sigma E", "J", r"\sigma", "E", size=M_L, width=COLW)
        C1 = EQ(r"\frac{I}{A}=\sigma E", "I", "A", r"\sigma", "E", size=M_L, width=COLW)
        C2 = EQ(r"\frac{I}{A}=\sigma\frac{V}{L}", "I", "A", r"\sigma", "V", "L", size=M_L, width=COLW)
        C3 = EQ(r"IL=\sigma AV", "I", "L", r"\sigma", "A", "V", size=M_L, width=COLW)
        S3f = EQ(r"V=I\frac{L}{\sigma A}", "V", "I", "L", r"\sigma", "A", size=M_L, width=COLW)
        S3c = EQ(r"V=I\frac{L}{\sigma A}", "V", "I", r"\frac{L}{\sigma A}", size=M_L, width=COLW)
        Df = EQ(r"R=\frac{L}{\sigma A}", "R", r"\frac{L}{\sigma A}", size=M_L, width=COLW)
        S4 = EQ(r"V=IR", "V", "I", "R", size=M_XL, width=COLW)
        for s in (C0, C1, C2, C3, S3f, S3c, S4):
            s.move_to(P3(COL, -0.45))
        self.play(rels.animate.set_opacity(0.5), run_time=0.6)
        self.play(FadeIn(C0, shift=UP * 0.15), run_time=1.2)
        self.wait(1.0)
        self.play(gmap(C0, C1, ("J", None)), run_time=2.0)
        self.add(C1)
        self.wait(1.0)
        self.play(gmap(C1, C2, ("E", None)), run_time=2.0)
        self.add(C2)
        self.wait(1.0)
        self.play(gmap(C2, C3), run_time=2.4)
        self.add(C3)
        self.wait(1.0)
        self.play(gmap(C3, S3f), run_time=2.4)
        self.add(S3f)
        self.wait(0.8)
        S3c.move_to(S3f)
        self.remove(S3f)
        self.add(S3c)
        blk = glyphs(S3c, r"\frac{L}{\sigma A}")
        bk = SurroundingRectangle(blk, color=VIOLET, buff=0.12, stroke_width=3, corner_radius=0.08).set_z_index(22)
        self.play(FadeIn(bk), run_time=0.8)
        blk_note = txt("depende só do material e da geometria", T_CAP, VIOLET).next_to(bk, DOWN, buff=0.35)
        self.play(FadeIn(blk_note, shift=UP * 0.1), run_time=0.8)
        self.wait(2.0)
        Df.move_to(P3(COL, -1.7))
        self.play(FadeOut(blk_note), run_time=0.4)
        self.play(TransformFromCopy(blk, glyphs(Df, r"\frac{L}{\sigma A}")), run_time=1.6)
        self.play(FadeIn(glyphs(Df, "R")), run_time=0.6)
        self.add(Df)
        bd = box(Df, WHITE)
        self.play(FadeIn(bd), run_time=0.6)
        self.wait(1.6)
        self.play(FadeOut(bk), FadeOut(bd), run_time=0.5)
        S4.move_to(S3c)
        self.play(gmap(S3c, S4, (r"\frac{L}{\sigma A}", "R")), FadeOut(Df), run_time=2.2)
        self.add(S4)
        bs = box(S4, WHITE)
        self.play(FadeIn(bs), run_time=0.6)
        self.wait(2.0)
        self.play(FadeOut(rels), run_time=0.8)
        cons = rich(r"$L\uparrow\Rightarrow R\uparrow,\qquad A\uparrow\Rightarrow R\downarrow$", T_NOTE).move_to(P3(COL, 1.5))
        self.play(FadeIn(cons, shift=UP * 0.1), run_time=0.8)
        self.wait(2.5)
        mJ.clear_updaters()
        self.play(FadeOut(cons), FadeOut(S4), FadeOut(bs), FadeOut(self.macro), FadeOut(self.gl_ohm), run_time=1.2)

    # ═══ 5-6. QUEM ESTABELECE E? — CONTINUIDADE ═══════════════════════════════════════════════════════════════
    def continuidade(self):
        self.next_section("B05_segunda_pergunta")
        self.E_arr = loop_arrows("E")
        self.J_arr = loop_arrows("J")
        self.ribbon = ribbon()
        self.play(FadeIn(self.world), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(a, shift=0.1 * RIGHT) for a in self.E_arr], lag_ratio=0.12), run_time=2.6)
        pot = txt("potencial ao longo do circuito", T_CAP, CYAN).move_to(P3(0, -0.25)).set_z_index(30)
        self.play(FadeIn(self.ribbon), FadeIn(pot), run_time=1.6)
        self.wait(1.0)
        self.play(FadeOut(pot), run_time=0.5)
        q = VGroup(txt("Quem estabelece esse campo", T_BODY), txt("ao longo do circuito inteiro?", T_BODY)).arrange(DOWN, buff=0.15)
        q.move_to(P3(0, -0.45)).set_z_index(30)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=1.0)
        self.wait(3.5)
        self.play(FadeOut(q), run_time=0.6)

        self.next_section("B06_continuidade")
        self.set_dim(0.94, 1.0)
        cx0, cx1, cy, ch = -7.0, 0.2, 0.35, 1.9
        wire = pipe(cx0, cy - ch / 2, cx1, cy + ch / 2, True, 15)
        for m in wire:
            m.set_z_index(15)
        CVx = -3.4
        cvbox = Rectangle(width=2.4, height=ch + 0.45).set_fill(BLUE_L, 0.0).set_stroke(width=0).move_to(P3(CVx, cy)).set_z_index(18)
        cv = DashedVMobject(Rectangle(width=2.4, height=ch + 0.45, color=BLUE_L, stroke_width=3).move_to(P3(CVx, cy)), num_dashes=44).set_z_index(18)
        cv_lab = txt("volume de controle", 20, BLUE_L).move_to(P3(CVx, cy - ch / 2 - 0.55)).set_z_index(18)
        face_l = rect(CVx - 1.2 - 0.05, cy - ch / 2, CVx - 1.2 + 0.05, cy + ch / 2, GREEN, 1.0, 19).set_fill(GREEN, 0.0)
        face_r = rect(CVx + 1.2 - 0.05, cy - ch / 2, CVx + 1.2 + 0.05, cy + ch / 2, GREEN, 1.0, 19).set_fill(GREEN, 0.0)
        self.cv_all = VGroup(wire, cvbox, cv, cv_lab, face_l, face_r)
        self.play(FadeIn(wire), run_time=1.0)
        self.pul = VGroup(*[Line(P3(0, cy), P3(0.3, cy), stroke_width=6, color=GREEN).set_z_index(16) for _ in range(7)])

        def pul_upd(m):
            t = self.clk.get_value()
            for i, ln in enumerate(m):
                x = cx0 + ((i / 7 + t * 0.1) % 1.0) * (cx1 - cx0 - 0.3)
                ln.put_start_and_end_on(P3(x, cy), P3(x + 0.3, cy))

        self.pul.add_updater(pul_upd)
        self.add(self.pul)
        self.play(FadeIn(cv), FadeIn(cv_lab), run_time=1.0)
        self.chips(0)
        self.play(FadeIn(self.chip_g), FadeIn(self.chip_ar), run_time=0.8)
        K0 = EQ(r"\frac{\partial\rho}{\partial t}+\nabla\cdot\mathbf J=0", r"\frac{\partial\rho}{\partial t}", r"\nabla\cdot", r"\mathbf J", size=M_M, width=COLW)
        K1 = EQ(r"\int_V\frac{\partial\rho}{\partial t}\,d\tau+\int_V\nabla\cdot\mathbf J\,d\tau=0", r"\frac{\partial\rho}{\partial t}", r"\nabla\cdot", r"\mathbf J", r"d\tau", size=M_S, width=COLW)
        K2 = EQ(r"\frac{d}{dt}\int_V\rho\,d\tau+\oint_S\mathbf J\cdot d\mathbf a=0", r"\rho", r"\mathbf J", r"d\tau", r"d\mathbf a", size=M_S, width=COLW)
        K3 = EQ(r"\frac{dQ}{dt}=I_{\rm entra}-I_{\rm sai}", r"\frac{dQ}{dt}", r"I_{\rm entra}", r"I_{\rm sai}", size=M_L, width=COLW)
        for k in (K0, K1, K2):
            k.move_to(P3(COL, 1.2)).set_z_index(30)
        K3.move_to(P3(COL, 0.0)).set_z_index(30)
        self.play(Write(K0), run_time=2.0)
        self.wait(1.2)
        self.play(cvbox.animate.set_fill(BLUE_L, 0.18), run_time=0.8)
        self.play(gmap(K0, K1, (r"\nabla\cdot", r"\nabla\cdot"), (r"\mathbf J", r"\mathbf J")), run_time=2.4)
        self.add(K1)
        self.wait(1.4)
        self.play(gmap(K1, K2, (r"\mathbf J", r"\mathbf J"), (r"d\tau", r"d\tau", 0, 0), (r"d\tau", None, 1),
                       (r"\nabla\cdot", None), (r"\frac{\partial\rho}{\partial t}", None)), run_time=2.6)
        self.add(K2)
        self.play(face_l.animate.set_fill(GREEN, 0.55), face_r.animate.set_fill(GREEN, 0.55), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(K2), FadeIn(K3, shift=UP * 0.1), run_time=1.6)
        kb = box(K3, WHITE)
        self.play(FadeIn(kb), run_time=0.6)
        self.wait(1.6)
        self.lab_in = MathTex(r"I_{\rm entra}", font_size=34, color=GREEN).move_to(P3(-5.4, cy - 1.5)).set_z_index(20)
        self.lab_out = MathTex(r"I_{\rm sai}", font_size=34, color=GREEN).move_to(P3(-1.4, cy - 1.5)).set_z_index(20)
        self.gl_cont = gloss_rows([gi("Q", BLUE_L, "carga dentro do volume"), gi(r"I_{\rm entra},\,I_{\rm sai}", GREEN, "correntes pelas faces")], P3(4.0, -1.7))
        self.play(FadeIn(self.lab_in), FadeIn(self.lab_out), FadeIn(self.gl_cont), run_time=1.0)
        self.K3, self.kb = K3, kb

    # ═══ cena prioritária: I_entra > I_sai → carga superficial → V(x) → E → J, em etapas ═════════════════
    def cargas_superficiais(self):
        self.next_section("B07_carga_E_J")
        cy, ch, CVx = 0.35, 1.9, -3.4
        d, s, sV, sE, sJ = (ValueTracker(0) for _ in range(5))
        opJ, opE, opV, opG = (ValueTracker(0) for _ in range(4))
        k = 0.35

        def L4():
            dd = d.get_value()
            return dict(eLv=0.95 + dd * k - k * sV.get_value(), eRv=0.95 - dd * k + k * sV.get_value(),
                        eL=0.95 + dd * k - k * sE.get_value(), eR=0.95 - dd * k + k * sE.get_value(),
                        jL=0.95 + dd * k - k * sJ.get_value(), jR=0.95 - dd * k + k * sJ.get_value())

        def arrows():
            L = L4()
            g = VGroup()
            for c, ln, y, col, o in ((-5.7, L["eL"], cy + 0.4, CYAN, opE), (-1.0, L["eR"], cy + 0.4, CYAN, opE),
                                     (-5.7, L["jL"], cy - 0.38, GREEN, opJ), (-1.0, L["jR"], cy - 0.38, GREEN, opJ)):
                g.add(halo(arrow(P3(c - ln / 2, y), P3(c + ln / 2, y), col, 6, 20, 0.22), 5).set_opacity(o.get_value()))
            return g

        def profile():
            L = L4()
            kk, y0 = 0.36, cy + ch / 2 + 1.2
            xs = [-7.0, -4.6, -2.2, 0.2]
            sl = [L["eLv"], (L["eLv"] + L["eRv"]) / 2, L["eRv"]]
            ys = [y0]
            for i in range(3):
                ys.append(ys[-1] - kk * sl[i])
            o = opV.get_value()
            g = VGroup(VMobject().set_points_as_corners([P3(x, y) for x, y in zip(xs, ys)]).set_stroke(CYAN, 5, opacity=o))
            for x, y in ((xs[1], ys[1]), (xs[2], ys[2])):
                g.add(DashedLine(P3(x, cy + ch / 2 + 0.05), P3(x, y), stroke_width=2, color=CYAN, dash_length=0.1).set_stroke(opacity=0.4 * o))
            return g.set_z_index(20)

        def gauge():
            L = L4()
            val = L["jL"] - L["jR"]
            w = max(abs(val) * 2.2, 0.001)
            r = Rectangle(width=w, height=0.2).set_fill(BLUE_L, 0.9).set_stroke(width=0).set_z_index(20)
            r.move_to(P3(-3.4 + w / 2, -2.05))
            return r.set_opacity(opG.get_value() * 0.9)

        arr = always_redraw(arrows)
        prof = always_redraw(profile)
        gau = always_redraw(gauge)
        g_axis = Line(P3(-3.4, -2.25), P3(-3.4, -1.85), stroke_width=2, color=DIM).set_z_index(20)
        g_lab = rich("$\\frac{dQ}{dt}$", 20, BLUE_L).move_to(P3(-4.35, -2.05)).set_z_index(20)
        v_lab = MathTex("V(x)", font_size=30, color=CYAN).move_to(P3(-6.55, cy + ch / 2 + 1.35)).set_z_index(20)
        spots = [(CVx - 0.9, cy + ch / 2), (CVx - 0.3, cy + ch / 2), (CVx + 0.3, cy + ch / 2), (CVx + 0.9, cy + ch / 2),
                 (CVx - 0.9, cy - ch / 2), (CVx - 0.3, cy - ch / 2), (CVx + 0.3, cy - ch / 2), (CVx + 0.9, cy - ch / 2)]
        order = [1, 5, 2, 6, 0, 4, 3, 7]
        chs = VGroup(*[charge(+1, P3(*spots[i]), r=0.14, z=19) for i in order])

        def chg_upd(m):
            for i, c in enumerate(m):
                c.set_opacity(float(np.clip(s.get_value() * len(m) - i, 0, 1)))

        chs.add_updater(chg_upd)
        chg_upd(chs)
        # uma legenda dominante por etapa (no máximo: representação + equação), com trilho de progresso
        st = {"cap": None, "sub": None}
        dots = VGroup(*[Circle(radius=0.07, stroke_width=1.5, color=BLUE_L).set_fill(BLUE_L, 0.0).move_to(P3(COL - 1.25 + 0.5 * i, -0.15))
                        for i in range(6)]).set_z_index(20)

        def stage(i, cap_new, sub_text, run=0.8):
            cap_new.move_to(P3(COL, 1.25)).set_z_index(20)
            sub_new = txt(sub_text, T_CAP, DIM).move_to(P3(COL, 0.5)).set_z_index(20)
            outs = [m for m in (st["cap"], st["sub"]) if m is not None]
            fills = [dd.animate.set_fill(BLUE_L, 1.0 if j <= i else 0.0) for j, dd in enumerate(dots)]
            self.play(*[FadeOut(m) for m in outs], FadeIn(cap_new, shift=UP * 0.1), FadeIn(sub_new, shift=UP * 0.1), *fills, run_time=run)
            st["cap"], st["sub"] = cap_new, sub_new

        self.play(FadeOut(self.K3), FadeOut(self.kb), FadeIn(dots), run_time=0.8)
        self.add(arr, prof, chs, gau)
        # A — só I_entra > I_sai
        stage(0, M(r"I_{\rm entra}", ">", r"I_{\rm sai}", size=M_L, width=COLW), "entra mais corrente do que sai")
        self.play(opJ.animate.set_value(1), run_time=1.0)
        self.play(d.animate.set_value(1), run_time=2.8)
        self.wait(1.2)
        # B — dQ/dt > 0
        stage(1, M(r"\frac{dQ}{dt}", ">", "0", size=M_L, width=COLW), "a carga dentro do volume cresce")
        self.play(opG.animate.set_value(1), FadeIn(g_axis), FadeIn(g_lab), run_time=1.2)
        self.wait(1.4)
        # C — acúmulo superficial
        self.chips(1)
        stage(2, txt("acúmulo na superfície", T_HEAD), "só na casca do condutor, não no volume")
        self.play(s.animate.set_value(1), run_time=4.0, rate_func=linear)
        self.wait(1.2)
        # D — o potencial local se deforma
        stage(3, txt("o potencial se deforma", T_HEAD), "V(x) muda junto do acúmulo")
        self.play(opV.animate.set_value(1), FadeIn(v_lab), run_time=1.0)
        self.play(sV.animate.set_value(1), run_time=4.0, rate_func=linear)
        self.wait(1.2)
        # E — o campo muda porque a inclinação de V muda
        stage(4, M("E", "=", r"-\frac{dV}{dx}", size=M_L, width=COLW), "E muda onde a inclinação de V muda")
        self.play(opE.animate.set_value(1), run_time=1.0)
        self.play(sE.animate.set_value(1), run_time=4.0, rate_func=linear)
        self.wait(1.2)
        # F — J acompanha E
        stage(5, M(r"\mathbf J", "=", r"\sigma", r"\mathbf E", size=M_L, width=COLW), "J acompanha E")
        self.play(sJ.animate.set_value(1), run_time=4.0, rate_func=linear)
        self.wait(1.0)
        self.chips(2)
        stage(5, M(r"I_{\rm entra}", "=", r"I_{\rm sai}", size=M_L, width=COLW), "a acumulação para; a carga permanece")
        self.wait(2.0)
        for m in (arr, prof, gau):
            m.clear_updaters()
        chs.clear_updaters()
        extras = VGroup(st["cap"], st["sub"], dots, self.lab_in, self.lab_out, g_axis, g_lab, v_lab, self.gl_cont)

        # ── do caso local para uma distribuição global já estabelecida ──
        self.next_section("B07b_distribuicao_global")
        self.layer = surface_layer()
        self.play(FadeOut(extras), run_time=1.0)
        self.pul.clear_updaters()
        figure = VGroup(arr, prof, gau, chs, self.cv_all, self.pul)
        spot_c = P3(-2.2, TOP)
        self.chips(1)
        self.set_dim(0.0, 0.01)
        self.play(figure.animate.scale(0.13).move_to(spot_c), FadeOut(self.ribbon), run_time=1.6)
        self.remove(figure)
        spot = DashedVMobject(Circle(radius=0.55, color=BLUE_L, stroke_width=3).scale([1.7, 1, 1]).move_to(spot_c), num_dashes=24).set_z_index(10)
        self.play(FadeIn(spot), FadeIn(self.layer), run_time=2.4)
        sprites = VGroup(charge(+1, P3(-3.7, TOP + WT / 2 + 0.1), r=0.09, z=9), charge(+1, P3(1.2, TOP + WT / 2 + 0.1), r=0.09, z=9),
                         charge(-1, P3(-3.7, BOT - WT / 2 - 0.1), r=0.09, z=9), charge(-1, P3(1.2, BOT - WT / 2 - 0.1), r=0.09, z=9))
        sprites.set_opacity(0.75)
        self.play(FadeIn(sprites, scale=0.5), run_time=0.8)
        steps = [rich("o mesmo ajuste vale em todo o circuito", T_NOTE), rich("a camada de carga já está estabelecida", T_NOTE),
                 rich(r"$\mathbf E$ adequado em cada região", T_NOTE)]
        for i, tt in enumerate(steps):
            tt.move_to(P3(0, 0.55 - 0.55 * i)).set_z_index(30)
        self.play(FadeIn(steps[0], shift=UP * 0.1), run_time=1.0)
        self.wait(2.0)
        self.play(FadeIn(steps[1], shift=UP * 0.1), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(spot), FadeOut(self.E_arr), run_time=0.6)
        self.E_arr = loop_arrows("E")
        self.play(FadeIn(steps[2], shift=UP * 0.1), FadeIn(self.E_arr), FadeIn(self.J_arr), run_time=1.8)
        self.add_shimmer(self.J_arr, j_phases())
        jse = M(r"\mathbf J", "=", r"\sigma", r"\mathbf E", size=M_S).move_to(P3(0, -1.2)).set_z_index(30)
        self.play(FadeIn(jse, shift=UP * 0.1), run_time=0.8)
        self.wait(3.0)
        self.play(FadeOut(steps[0]), FadeOut(steps[1]), FadeOut(steps[2]), FadeOut(jse), run_time=0.8)
        # a fita de potencial reúne as ideias: fio (queda pequena), resistor (queda grande), fonte (sobe)
        self.ribbon = ribbon()
        rib_notes = [rich("fio: queda pequena", T_CAP).move_to(P3(-1.8, 0.0)), rich("resistor: queda grande", T_CAP).move_to(P3(2.0, -0.5)),
                     rich("fonte: potencial sobe", T_CAP).move_to(P3(-2.6, -0.95))]
        for rn in rib_notes:
            rn.set_z_index(30)
        self.play(FadeIn(self.ribbon), run_time=1.4)
        for rn in rib_notes:
            self.play(FadeIn(rn, shift=UP * 0.1), run_time=0.8)
            self.wait(1.4)
        efd = rich("$E_t=-\\frac{dV}{ds}$", T_NOTE, CYAN).move_to(P3(2.9, 0.1)).set_z_index(30)
        self.play(FadeIn(efd), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(VGroup(self.ribbon, efd, *rib_notes)), run_time=1.0)
        self.sprites = sprites

    # ═══ 6b. REGIME ESTACIONÁRIO ═══════════════════════════════════════════════════════════════════════════
    def regime_estacionario(self):
        self.next_section("B08_estacionario")
        self.chips(1)
        tr = M(r"\frac{\partial\rho}{\partial t}", r"\neq", "0", size=M_L).move_to(P3(0, 0.0)).set_z_index(30)
        self.play(FadeIn(tr, shift=UP * 0.1), run_time=1.0)
        self.play(Indicate(self.layer, color=WHITE, scale_factor=1.0, rate_func=there_and_back), run_time=2.0)
        self.chips(2)
        st1 = M(r"\frac{\partial\rho}{\partial t}", "=", "0", size=M_L).move_to(P3(-2.35, 0.45)).set_z_index(30)
        st2 = M(r"\nabla\cdot\mathbf J", "=", "0", size=M_L).move_to(P3(2.35, 0.45)).set_z_index(30)
        self.play(ReplacementTransform(tr, st1), run_time=1.2)
        self.play(FadeIn(st2, shift=UP * 0.1), run_time=1.0)
        b2 = box(st2)
        self.play(FadeIn(b2), run_time=0.6)
        self.wait(1.5)
        self.play(Indicate(self.layer, color=WHITE, scale_factor=1.0, rate_func=there_and_back), run_time=2.0)
        ne1 = VGroup(txt("regime estacionário", T_CAP), MathTex(r"\neq", font_size=40), txt("sem cargas superficiais", T_CAP)).arrange(RIGHT, buff=0.3)
        ne1.move_to(P3(0, -0.75)).set_z_index(30)
        self.play(FadeIn(ne1, shift=UP * 0.1), run_time=1.0)
        bn1 = box(ne1, BLUE_L)
        self.play(FadeIn(bn1), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(VGroup(st1, st2, b2, ne1, bn1)), run_time=0.8)
        self.set_dim(0.55, 0.8)
        pa = panel(4.5, 2.5, P3(-2.6, -0.05))
        pb = panel(4.5, 2.5, P3(2.6, -0.05))
        ta = txt("equilíbrio eletrostático", T_CAP, DIM).move_to(P3(-2.6, 0.85)).set_z_index(30)
        tb = txt("corrente estacionária", T_CAP, GREEN).move_to(P3(2.6, 0.85)).set_z_index(30)
        ea = M(r"\mathbf E", "=", "0", size=M_L).move_to(P3(-2.6, 0.0)).set_z_index(30)
        ea_n = txt("no interior do condutor", 20, DIM).move_to(P3(-2.6, -0.55)).set_z_index(30)
        eb1 = M(r"\mathbf E", r"\neq", "0", size=M_L).move_to(P3(2.6, 0.2)).set_z_index(30)
        eb2 = M(r"\mathbf J", "=", r"\sigma", r"\mathbf E", size=M_M).move_to(P3(2.6, -0.5)).set_z_index(30)
        self.play(FadeIn(pa), FadeIn(pb), FadeIn(ta), FadeIn(tb), run_time=1.0)
        self.play(FadeIn(ea, shift=UP * 0.1), FadeIn(ea_n), run_time=1.0)
        self.wait(1.2)
        self.play(FadeIn(eb1, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(eb2, shift=UP * 0.1), run_time=1.0)
        bb = box(eb1, GREEN)
        self.play(FadeIn(bb), run_time=0.6)
        self.wait(2.0)
        self.play(FadeOut(VGroup(pa, pb, ta, tb, ea, ea_n, eb1, eb2, bb)), run_time=0.8)
        ne2 = VGroup(txt("estacionário", T_BODY), MathTex(r"\neq", font_size=48), txt("eletrostático", T_BODY)).arrange(RIGHT, buff=0.35)
        ne2.move_to(P3(0, -0.2)).set_z_index(30)
        bn2 = box(ne2, WHITE, 0.22)
        self.play(FadeIn(ne2, shift=UP * 0.1), FadeIn(bn2), run_time=1.2)
        self.wait(2.5)
        self.play(FadeOut(ne2), FadeOut(bn2), run_time=0.8)
        self.set_dim(0.0, 0.8)

    # ═══ 7-8. QUEM REPÕE A ENERGIA? — FONTE E FEM ═════════════════════════════════════════════════════════
    def fonte_e_fem(self):
        self.next_section("B09_fonte")
        self.play(FadeOut(self.chip_g), FadeOut(self.chip_ar), run_time=0.5)
        self.set_dim(0.96, 1.0)
        q = txt("Se o resistor dissipa energia, quem repõe essa energia?", T_BODY).move_to(P3(0, 1.5)).set_z_index(30)
        halo(q)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=1.0)
        self.wait(3.0)
        self.play(q.animate.scale(0.62).move_to(P3(COL, 2.3)).set_color(DIM), run_time=1.0)
        # corte pseudo-3D da fonte: dois terminais em profundidade; E atravessa, f_s atua no sentido oposto
        bx0, by0 = -3.4, -0.1
        w, hgt, dx, dy = 2.8, 3.2, 0.5, 0.35
        fl, fr_, ft, fb = bx0 - w / 2, bx0 + w / 2, by0 + hgt / 2, by0 - hgt / 2
        back = poly([(fl + dx, fb + dy), (fr_ + dx, fb + dy), (fr_ + dx, ft + dy), (fl + dx, ft + dy)], PANEL, 0.45, 15, (BLUE_L, 1.5, 0.5))
        side = poly([(fr_, fb), (fr_ + dx, fb + dy), (fr_ + dx, ft + dy), (fr_, ft)], PANEL, 0.75, 15)
        top = poly([(fl, ft), (fr_, ft), (fr_ + dx, ft + dy), (fl + dx, ft + dy)], BLUE_L, 0.35, 15)
        front = RoundedRectangle(corner_radius=0.1, width=w, height=hgt, stroke_width=2).set_fill(PANEL, 0.8).set_stroke(BLUE_L, 2, 0.9)
        front.move_to(P3(bx0, by0)).set_z_index(16)
        py_t, py_b = ft - 0.5, fb + 0.5
        plate_t = VGroup(poly([(fl + 0.2, py_t), (fr_ - 0.2, py_t), (fr_ - 0.2 + dx, py_t + dy), (fl + 0.2 + dx, py_t + dy)], WHITE, 0.55, 17),
                         Line(P3(fl + 0.2, py_t), P3(fr_ - 0.2, py_t), stroke_width=6, color=WHITE).set_z_index(18))
        plate_b = VGroup(poly([(fl + 0.7, py_b), (fr_ - 0.7, py_b), (fr_ - 0.7 + dx, py_b + dy), (fl + 0.7 + dx, py_b + dy)], WHITE, 0.4, 17),
                         Line(P3(fl + 0.7, py_b), P3(fr_ - 0.7, py_b), stroke_width=6, color=WHITE).set_z_index(18))
        stub_t = rect(bx0 - .25, ft, bx0 + .25, ft + 0.6, STEEL, 1, 14)
        stub_b = rect(bx0 - .25, fb - 0.6, bx0 + .25, fb, STEEL, 1, 14)
        pm = VGroup(MathTex("+", font_size=40, color=WHITE).move_to(P3(fr_ + dx + 0.3, py_t + dy)),
                    MathTex("-", font_size=40, color=WHITE).move_to(P3(fr_ + dx + 0.3, py_b + dy))).set_z_index(18)
        cps = VGroup(*[charge(+1, P3(bx0 + dxx, py_t - 0.22), z=19) for dxx in (-0.7, 0.0, 0.7)],
                     *[charge(-1, P3(bx0 + dxx, py_b + 0.22), z=19) for dxx in (-0.4, 0.4)])
        fonte_lab = txt("fonte (esquemática)", 20, DIM).move_to(P3(bx0, ft + 0.9)).set_z_index(18)
        shell = VGroup(back, side, top, front, plate_t, plate_b, stub_t, stub_b, pm, fonte_lab)
        self.play(FadeIn(shell), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in cps], lag_ratio=0.15), run_time=1.2)
        Ea = VGroup(halo(arrow(P3(bx0 - 0.7, py_t - 0.55), P3(bx0 - 0.7, by0 + 0.1), CYAN, 6, 20, 0.22)),
                    halo(arrow(P3(bx0 - 0.7, by0 - 0.05), P3(bx0 - 0.7, py_b + 0.45), CYAN, 6, 20, 0.22)))
        Ea_l = MathTex(r"\mathbf E", font_size=40, color=CYAN).move_to(P3(bx0 - 1.15, by0)).set_z_index(20)
        self.play(FadeIn(Ea, shift=DOWN * 0.15), FadeIn(Ea_l), run_time=1.2)
        self.wait(1.0)
        Fs = VGroup(halo(arrow(P3(bx0 + 0.7, py_b + 0.35), P3(bx0 + 0.7, by0 + 0.15), FC, 8, 20, 0.28)),
                    halo(arrow(P3(bx0 + 0.7, by0), P3(bx0 + 0.7, py_t - 0.35), FC, 8, 20, 0.28)))
        Fs_l = MathTex(r"\mathbf f_s", font_size=40, color=FC).move_to(P3(bx0 + 1.2, by0 + 0.3)).set_z_index(20)
        self.play(FadeIn(Fs, shift=UP * 0.2), FadeIn(Fs_l), run_time=1.4)
        # um portador sobe contra a tendência eletrostática; a régua mostra energia por carga aumentando
        cu = ValueTracker(0.0)
        cu.add_updater(lambda m, dt: m.set_value((m.get_value() + dt / 4.0) % 1.0))
        y_lo, y_hi = py_b + 0.3, py_t - 0.3
        car = Circle(radius=0.12, stroke_width=1.5, color=WHITE).set_fill(BLUE, 1).set_z_index(21)
        car.add_updater(lambda m: m.move_to(P3(bx0 + 0.0, y_lo + (y_hi - y_lo) * cu.get_value())))
        rx = fr_ + dx + 0.95
        rule = Line(P3(rx, y_lo), P3(rx, y_hi), stroke_width=2, color=DIM).set_z_index(20)
        bar = Rectangle(width=0.2, height=0.05).set_fill(CYAN, 0.9).set_stroke(width=0).set_z_index(20)

        def bar_upd(m):
            hh_ = max(0.02, (y_hi - y_lo) * cu.get_value())
            m.become(Rectangle(width=0.2, height=hh_).set_fill(CYAN, 0.9).set_stroke(width=0).set_z_index(20).move_to(P3(rx, y_lo + hh_ / 2)))

        bar.add_updater(bar_upd)
        rule_l = txt("energia por carga", 18, CYAN).move_to(P3(rx, py_b - 0.55)).set_z_index(20)
        self.add(cu, car, bar)
        self.play(FadeIn(rule), FadeIn(rule_l), run_time=0.8)
        n1 = rich(r"$\mathbf E$ e $\mathbf f_s$ coexistem dentro da fonte", T_CAP).move_to(P3(COL, 1.1)).set_z_index(30)
        n2 = gloss_line([gi(r"\mathbf f_s", FC, "força não eletrostática, por unidade de carga")])
        self.play(FadeIn(n1, shift=UP * 0.1), FadeIn(n2, shift=UP * 0.1), run_time=1.2)
        self.wait(4.0)
        feq = M(r"\mathbf f", "=", r"\mathbf E", "+", r"\mathbf f_s", size=M_L, width=COLW).move_to(P3(COL, -0.65)).set_z_index(30)
        self.play(Write(feq), run_time=1.6)
        fb_ = box(feq)
        self.play(FadeIn(fb_), run_time=0.6)
        self.wait(4.0)
        for m in (cu, car, bar):
            m.clear_updaters()
        self.remove(cu)
        self.src_fig = VGroup(shell, cps, Ea, Ea_l, Fs, Fs_l, car, rule, bar, rule_l, n1, n2, q)
        self.play(FadeOut(self.src_fig), FadeOut(feq), FadeOut(fb_), run_time=1.0)

        # ── FEM: o marcador realmente calcula a circulação ──
        self.next_section("B10_fem")
        self.set_dim(0.6, 1.0)
        u = ValueTracker(0)
        nf = txt("FEM não é força", T_BODY, WHITE).move_to(P3(0, 2.3)).set_z_index(30)
        halo(nf)
        d1 = M(r"\mathcal E", "=", r"\oint", r"\mathbf f", r"\cdot d\boldsymbol\ell", size=M_L).move_to(P3(0, 0.5)).set_z_index(30)

        def mk_pos():
            return LOOP.at(u.get_value() * LOOP.total * 0.99999)

        mk = always_redraw(lambda: VGroup(
            Circle(radius=0.14, stroke_width=2, color=WHITE).set_fill(WHITE, 1).move_to(mk_pos()[0]),
            halo(arrow(mk_pos()[0], mk_pos()[0] + 0.45 * mk_pos()[1], WHITE, 5, 40, 0.2), 4)).set_z_index(40))

        def trail():
            n = max(2, int(u.get_value() * 80))
            pts = [LOOP.at(u.get_value() * LOOP.total * 0.99999 * j / (n - 1))[0] for j in range(n)]
            return VMobject().set_points_as_corners(pts).set_stroke(WHITE, 3, 0.55).set_z_index(39)

        tr = always_redraw(trail)

        def cE():
            return (1.0 - Vat(u.get_value() * LOOP.total * 0.99999)) / 2

        def cF():
            if u.get_value() >= 0.99999:
                return 1.0
            i, f = LOOP.seg_of(u.get_value() * LOOP.total)
            return f if i == 7 else 0.0

        BL = 3.4
        bE = always_redraw(lambda: Rectangle(width=max(0.001, BL * cE()), height=0.22).set_fill(CYAN, 0.9).set_stroke(width=0)
                           .move_to(P3(-0.6 + max(0.001, BL * cE()) / 2, -0.55)).set_z_index(30))
        bF = always_redraw(lambda: Rectangle(width=max(0.001, BL * cF()), height=0.22).set_fill(FC, 0.9).set_stroke(width=0)
                           .move_to(P3(-0.6 + max(0.001, BL * cF()) / 2, -1.45)).set_z_index(30))
        lE = MathTex(r"\oint\mathbf E\cdot d\boldsymbol\ell", font_size=30, color=CYAN).move_to(P3(-2.2, -0.55)).set_z_index(30)
        lF = MathTex(r"\oint\mathbf f_s\cdot d\boldsymbol\ell", font_size=30, color=FC).move_to(P3(-2.2, -1.45)).set_z_index(30)
        self.gl_fem = gloss_line([gi(r"\mathcal E", CYAN, "força eletromotriz (fem)"), gi(r"\mathbf f_s", FC, "força não eletrostática por unidade de carga")])
        self.add(mk, tr)
        self.play(FadeIn(self.gl_fem), Write(d1), FadeIn(nf, shift=UP * 0.1), run_time=1.6)
        self.wait(1.0)
        self.add(bE, bF)
        self.play(FadeIn(lE), FadeIn(lF), run_time=0.8)
        self.play(u.animate.set_value(1.0), run_time=12, rate_func=linear)
        for m in (mk, tr, bE, bF):
            m.clear_updaters()
        self.remove(mk, tr)
        self.wait(1.0)
        hyp = txt("circuito DC estacionário, sem indução magnética nem movimento do circuito", 22, DIM).move_to(P3(0, 2.3)).set_z_index(30)
        self.play(FadeOut(nf), FadeIn(hyp, shift=UP * 0.1), run_time=1.0)
        e0 = MathTex(r"\oint\mathbf E\cdot d\boldsymbol\ell=0", font_size=30, color=CYAN).move_to(P3(-2.6, -0.55)).set_z_index(30)
        self.play(ReplacementTransform(lE, e0), run_time=1.2)
        cb = box(e0, CYAN)
        self.play(FadeIn(cb), run_time=0.6)
        self.wait(2.5)
        d2 = EQ(r"\mathcal E=\oint\mathbf E\cdot d\boldsymbol\ell+\oint\mathbf f_s\cdot d\boldsymbol\ell", r"\mathcal E", r"\oint", r"\mathbf E",
                r"\mathbf f_s", r"\cdot d\boldsymbol\ell", size=M_M, width=9.0).move_to(P3(0, 0.5)).set_z_index(30)
        d2z = EQ(r"\mathcal E=0+\oint\mathbf f_s\cdot d\boldsymbol\ell", r"\mathcal E", "0", r"\oint", r"\mathbf f_s", r"\cdot d\boldsymbol\ell",
                 size=M_M, width=9.0).move_to(P3(0, 0.5)).set_z_index(30)
        d3 = EQ(r"\mathcal E=\oint\mathbf f_s\cdot d\boldsymbol\ell", r"\mathcal E", r"\oint", r"\mathbf f_s", r"\cdot d\boldsymbol\ell",
                size=M_L, width=9.0).move_to(P3(0, 0.5)).set_z_index(30)
        self.play(FadeOut(hyp), run_time=0.5)
        self.play(FadeOut(d1), FadeIn(d2), run_time=1.6)
        self.wait(2.0)
        eterm = VGroup(glyphs(d2, r"\oint", 0), glyphs(d2, r"\mathbf E"), glyphs(d2, r"\cdot d\boldsymbol\ell", 0))
        cr = Cross(eterm, stroke_color=WHITE, stroke_width=4).set_z_index(35)
        self.play(Create(cr), run_time=0.9)
        self.wait(0.7)
        self.play(FadeOut(cr), gmap(d2, d2z, (r"\oint", None, 0), (r"\mathbf E", None), (r"\cdot d\boldsymbol\ell", None, 0)), run_time=2.0)
        self.add(d2z)
        self.wait(1.2)
        self.play(gmap(d2z, d3, ("0", None)), run_time=2.0)
        self.add(d3)
        fb3 = box(d3, WHITE, 0.22)
        self.play(FadeIn(fb3), run_time=0.6)
        self.wait(3.0)
        self.d3, self.fb3 = d3, fb3
        self.fem_bits = VGroup(bE, bF, lF, e0, cb)

    # ═══ 9-10. ENERGIA E PAYOFF ══════════════════════════════════════════════════════════════════════════
    def energia_e_payoff(self):
        self.next_section("B11_energia")
        self.play(FadeOut(self.fem_bits), self.d3.animate.scale(0.5).move_to(P3(COL + 0.8, 2.3)).set_opacity(0.6), FadeOut(self.fb3), run_time=1.0)
        self.set_dim(0.75, 0.6)
        Q0 = EQ(r"p=\mathbf J\cdot\mathbf E", "p", r"\mathbf J", r"\mathbf E", size=M_L)
        Q1 = EQ(r"P=\int p\,d\tau=\int\mathbf J\cdot\mathbf E\,d\tau", "P", "p", r"\mathbf J", r"\mathbf E", size=M_M, width=8.6)
        Q2 = EQ(r"P=JE\,AL", "P", "J", "E", "A", "L", size=M_L)
        Q3 = EQ(r"P=(JA)(EL)", "P", "J", "E", "A", "L", size=M_L)
        Q4 = EQ(r"P=VI", "P", "V", "I", size=M_L)
        Q5 = EQ(r"P=I^2R", "P", "I", size=M_L)
        for q in (Q0, Q1, Q2, Q3, Q4, Q5):
            q.move_to(P3(0, 0.3)).set_z_index(30)
        pv = txt("potência por volume", T_CAP, DIM).move_to(P3(0, -0.55)).set_z_index(30)
        self.gl_en = gloss_line([gi("p", CYAN, "potência por volume"), gi("P", CYAN, "potência total"), gi("R", WHITE, "resistência total do modelo ideal")])
        self.play(FadeOut(self.gl_fem), run_time=0.4)
        self.play(Indicate(self.res_g, color=CYAN, scale_factor=1.1), Write(Q0), FadeIn(pv), FadeIn(self.gl_en), run_time=1.6)
        self.wait(1.5)
        self.play(FadeOut(pv), gmap(Q0, Q1, ("p", "p"), (r"\mathbf J", r"\mathbf J"), (r"\mathbf E", r"\mathbf E")), run_time=2.4)
        self.add(Q1)
        pt = txt("potência total no resistor", T_CAP, DIM).move_to(P3(0, -0.55)).set_z_index(30)
        self.play(FadeIn(pt), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(pt), gmap(Q1, Q2, (r"\mathbf J", "J"), (r"\mathbf E", "E"), ("p", None)), run_time=2.4)
        self.add(Q2)
        un = txt("resistor uniforme: J e E constantes, volume AL", T_CAP, DIM).move_to(P3(0, -0.55)).set_z_index(30)
        self.play(FadeIn(un), run_time=0.6)
        self.wait(1.4)
        self.play(FadeOut(un), gmap(Q2, Q3), run_time=2.0)
        self.add(Q3)
        self.wait(1.0)
        ji = rich(r"$JA=I,\qquad EL=V$", T_NOTE).move_to(P3(0, -0.6)).set_z_index(30)
        self.play(FadeIn(ji, shift=UP * 0.1), run_time=0.8)
        self.wait(1.0)
        self.play(gmap(Q3, Q4, ([("J", 0), ("A", 0)], "I"), ([("E", 0), ("L", 0)], "V")), run_time=2.6)
        self.add(Q4)
        bq = box(Q4, CYAN)
        self.play(FadeIn(bq), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(bq), FadeOut(ji), run_time=0.5)
        vir = M("V", "=", "I", "R", size=M_M).move_to(P3(0, -0.6)).set_z_index(30)
        self.play(FadeIn(vir, shift=UP * 0.1), run_time=0.8)
        self.play(gmap(Q4, Q5, ("I", "I"), ("V", None)), run_time=2.2)
        self.add(Q5)
        bq5 = box(Q5, CYAN)
        self.play(FadeIn(bq5), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(Q5), FadeOut(bq5), FadeOut(vir), run_time=0.8)
        pf = M(r"P_{\rm fonte}", "=", r"\mathcal E", "I", size=M_L).move_to(P3(0, 0.45)).set_z_index(30)
        eir = M(r"\mathcal E", "=", "I", "R", size=M_M).move_to(P3(0, -0.4)).set_z_index(30)
        self.play(Write(pf), run_time=1.4)
        self.wait(1.2)
        self.play(FadeIn(eir, shift=UP * 0.1), run_time=1.0)
        rn = txt("R: resistência total do modelo ideal", 20, DIM).move_to(P3(0, -1.0)).set_z_index(30)
        self.play(FadeIn(rn), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(pf), FadeOut(eir), FadeOut(rn), run_time=0.8)
        fin = M(r"P_{\rm fonte}", "=", r"\mathcal E", "I", "=", "I^2", "R", "=", r"P_{\rm dissipada}", size=M_M, width=9.6).move_to(P3(0, 0.5)).set_z_index(30)
        self.play(Write(fin), run_time=2.4)
        fbx = box(fin, WHITE, 0.2)
        self.play(FadeIn(fbx), run_time=0.6)
        t_in = txt("fonte repõe", 20, CYAN).set_z_index(30)
        t_out = txt("resistor dissipa", 20, CYAN).set_z_index(30)
        t_in.move_to(P3(-4.4 + t_in.width / 2, -0.65))
        t_out.move_to(P3(-4.4 + t_out.width / 2, -1.15))
        b_in = Rectangle(width=0.01, height=0.28).set_fill(CYAN, 1).set_stroke(width=0).set_z_index(30).move_to(P3(-1.795, -0.65))
        b_out = Rectangle(width=0.01, height=0.28).set_fill(CYAN, 0.55).set_stroke(width=0).set_z_index(30).move_to(P3(-1.795, -1.15))
        wbar = 5.0
        g_in = Rectangle(width=wbar, height=0.28).set_fill(CYAN, 1).set_stroke(width=0).set_z_index(30).move_to(P3(-1.8 + wbar / 2, -0.65))
        g_out = Rectangle(width=wbar, height=0.28).set_fill(CYAN, 0.55).set_stroke(width=0).set_z_index(30).move_to(P3(-1.8 + wbar / 2, -1.15))
        self.play(FadeIn(t_in), FadeIn(t_out), run_time=0.6)
        self.add(b_in, b_out)
        self.play(ReplacementTransform(b_in, g_in), ReplacementTransform(b_out, g_out), run_time=2.5)
        self.wait(3.0)
        self.play(FadeOut(VGroup(fin, fbx, t_in, t_out, g_in, g_out, self.d3, self.gl_en)), run_time=1.0)

        # ── payoff: o próprio circuito é a síntese; holofote camada a camada ──
        self.next_section("B12_payoff")
        self.set_dim(0.78, 1.0)
        # as camadas ficam acima do escurecimento: o holofote acende uma por vez sobre o circuito apagado
        self.J_arr.clear_updaters()
        self.remove(self.layer, self.E_arr, self.J_arr, self.sprites)
        self.layer = surface_layer(z=14)
        self.E_arr, self.J_arr = loop_arrows("E", z=14), loop_arrows("J", z=14)
        self.sprites = VGroup(charge(+1, P3(-3.7, TOP + WT / 2 + 0.1), z=15), charge(+1, P3(1.2, TOP + WT / 2 + 0.1), z=15),
                              charge(-1, P3(-3.7, BOT - WT / 2 - 0.1), z=15), charge(-1, P3(1.2, BOT - WT / 2 - 0.1), z=15))
        bx, by = LX, (BAT[0] + BAT[1]) / 2
        fs_a = halo(arrow(P3(bx + 0.78, BAT[0] - 0.1), P3(bx + 0.78, BAT[1] + 0.35), FC, 8, 25, 0.26))
        fs_l = MathTex(r"\mathbf f_s", font_size=44, color=FC).move_to(P3(bx + 0.78, BAT[1] + 0.8)).set_z_index(25)
        fs_ring = Circle(radius=0.95, color=FC, stroke_width=3).move_to(P3(bx, by)).set_z_index(25)
        self.play(FadeIn(fs_a, shift=UP * 0.15), FadeIn(fs_l), FadeIn(fs_ring, scale=1.3), run_time=1.6)
        self.wait(2.0)
        self.play(FadeOut(fs_ring), run_time=0.5)
        lab_q = txt("carga superficial", T_CAP, BLUE_L).move_to(P3(-2.6, 2.3)).set_z_index(30)
        self.play(FadeIn(self.layer), FadeIn(self.sprites), FadeIn(lab_q, shift=UP * 0.1), run_time=2.0)
        self.wait(2.4)
        lab_E = MathTex(r"\mathbf E", font_size=44, color=CYAN).move_to(P3(3.9, 0.35)).set_z_index(30)
        self.play(FadeIn(self.E_arr), FadeIn(lab_E), run_time=1.4)
        self.wait(2.4)
        lab_J = MathTex(r"\mathbf J", font_size=44, color=GREEN).move_to(P3(3.9, -0.45)).set_z_index(30)
        self.play(FadeIn(self.J_arr), FadeIn(lab_J), run_time=1.4)
        self.add_shimmer(self.J_arr, j_phases())
        self.wait(2.0)
        self.play(self.dim.animate.set_fill(BACKGROUND_COLOR, 0.0), run_time=1.6)
        fin_t = txt("A fonte repõe energia · as cargas superficiais estabelecem E · E atua localmente", 22, WHITE).move_to(P3(0, -2.85)).set_z_index(30)
        self.play(FadeIn(fin_t, shift=UP * 0.1), Indicate(self.E_arr, color=WHITE, scale_factor=1.12), run_time=2.0)
        self.wait(6.0)
        self.J_arr.clear_updaters()
        self.play(FadeOut(VGroup(self.layer, self.E_arr, self.J_arr, self.sprites, fs_a, fs_l, lab_q, lab_E, lab_J, fin_t)),
                  self.dim.animate.set_fill(BACKGROUND_COLOR, 1.0), run_time=1.5)
