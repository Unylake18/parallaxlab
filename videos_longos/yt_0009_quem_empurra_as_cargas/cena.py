"""yt_0009 — Quem empurra as cargas? (campo elétrico, Lei de Ohm, cargas superficiais e FEM). V2.

Preview visual silencioso, 960×540 / 15 fps. Paleta e gramática da série Magnetostática (yt_0005/yt_0006):
E, V, ℰ e energia ciano · J, I e ∇·J verde · carga azul · f e f_s azul-claro FC · geometria violeta · matéria STEEL.

Fio condutor: UM circuito recorrente (fonte + fio + resistor) que ganha camadas: E → J → camada de carga superficial →
potencial V(s) → f_s. Preserva os blocos da V1; reconstrói Ohm, continuidade, cena causal, fonte/FEM, energia e payoff.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
from manim import (
    AnimationGroup, Arrow, Circle, Create, Dot, MoveAlongPath, MoveToTarget, config, DashedLine, DashedVMobject, DoubleArrow, Ellipse, FadeIn, FadeOut, ImageMobject, Indicate,
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
for _t in ("E", "E_x", "V", r"\mathbf E", r"\mathcal E", "P", "p", r"P_{\rm fonte}", r"P_{\rm dissipada}", r"\Delta V"):
    TOKCOL[_t] = CYAN
for _t in (r"\mathbf f", r"\mathbf f_s", r"\mathbf F"):
    TOKCOL[_t] = FC
for _t in (r"\rho", r"\frac{\partial\rho}{\partial t}", "Q", r"\frac{dQ}{dt}"):
    TOKCOL[_t] = BLUE_L
for _t in ("A", "L", r"\mathbf v_d", r"d\mathbf a", r"d\tau"):
    TOKCOL[_t] = VIOLET


CAPS = os.environ.get("CAPS", "1") == "1"      # teste: todo texto de tela (fora MathTex) em Space Grotesk MAIÚSCULA


def txt(s, size=T_BODY, color=WHITE, opacity=1.0, caps=True):
    if CAPS and caps:
        s = s.upper()
    # o Pango quebra a linha quando corpo×oversample é grande: reduz o oversample até sair numa linha só
    for ov in ((4, 2, 1) if (len(s) < 34 and size < 38) else (2, 1)):
        t = screen_text(s, size, color=color, oversample=ov)
        if "\n" in s or t.height < 2.0 * screen_text("H", size, color=color, oversample=ov).height:
            break
    return t.set_opacity(opacity)


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


def NT(*a, **k):
    """Texto removido (a narração diz): objeto invisível, para não quebrar as animações que o referenciam."""
    return Dot(radius=0.001).set_opacity(0)


def rich(s, size=T_CAP, color=WHITE, caps=True):
    g, prev = VGroup(), None
    for i, p in enumerate(s.split("$")):
        p = p.strip() if i % 2 == 0 else p
        if not p:
            continue
        m = MathTex(p, font_size=size * 1.18, color=color) if i % 2 else txt(p, size, color, caps=caps)
        if prev is not None:
            m.next_to(prev, RIGHT, buff=0.16)
        g.add(m)
        prev = m
    return g


def gi(sym, color, desc, size=24):
    """Item de glossário: símbolo na cor da grandeza + descrição curta."""
    return VGroup(MathTex(sym, font_size=size * 1.25, color=color), txt(": " + desc, size, DIM, caps=False)).arrange(RIGHT, buff=0.06)


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


def pt(x, y):
    """alvo invisível para ancorar um rótulo num ponto da cena."""
    return Dot(P3(x, y), radius=0.01).set_opacity(0)


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
    """Percurso do circuito (polilinha densa) no sentido da corrente convencional: fonte + → fio → resistor → fio → fonte −."""

    def __init__(self, pts, marks):
        self.p = np.array([P3(*q) for q in pts])
        self.l = np.linalg.norm(np.diff(self.p, axis=0), axis=1)
        self.cum = np.concatenate([[0.0], np.cumsum(self.l)])
        self.total = self.cum[-1]
        self.S = {k: float(self.cum[i]) for k, i in marks.items()}

    def at(self, s):
        s = s % self.total
        i = min(int(np.searchsorted(self.cum, s, side="right")) - 1, len(self.l) - 1)
        t = (self.p[i + 1] - self.p[i]) / self.l[i]
        return self.p[i] + t * (s - self.cum[i]), t


TOP, BOT, LX, RX, WT = 1.55, -1.95, -5.4, 5.4, 0.5
BAT = (-0.85, 0.45)
RES = (-0.9, 0.5)
RC = 0.9        # raio dos cantos


def _make_loop():
    pts, marks = [], {}

    def add(x, y):
        pts.append((float(x), float(y)))

    def mark(k):
        marks[k] = len(pts) - 1

    def arc(cx, cy, a0, a1, name, n=14):
        i0 = len(pts) - 1
        for k in range(1, n + 1):
            a = a0 + (a1 - a0) * k / n
            add(cx + RC * np.cos(a), cy + RC * np.sin(a))
        marks[name] = i0 + n // 2

    add(LX, BAT[1])
    mark("b1")
    add(LX, TOP - RC)
    mark("lu_end")
    arc(LX + RC, TOP - RC, np.pi, np.pi / 2, "tl_mid")
    mark("top_start")
    add(RX - RC, TOP)
    mark("top_end")
    arc(RX - RC, TOP - RC, np.pi / 2, 0, "tr_mid")
    add(RX, RES[1])
    mark("res0")
    add(RX, RES[0])
    mark("res1")
    add(RX, BOT + RC)
    mark("rd_end")
    arc(RX - RC, BOT + RC, 0, -np.pi / 2, "br_mid")
    mark("bot_start")
    add(LX + RC, BOT)
    mark("bot_end")
    arc(LX + RC, BOT + RC, -np.pi / 2, -np.pi, "bl_mid")
    add(LX, BAT[0])
    mark("b0")
    add(LX, BAT[1])
    mark("end")
    return pts, marks


LOOP = Loop(*_make_loop())
S = LOOP.S
# potencial (conceitual) ao longo do percurso: cai pouco nos fios, muito no resistor e sobe na fonte
_VS = [0.0, S["top_start"], S["top_end"], S["res0"], S["res1"], S["bot_start"], S["bot_end"], S["b0"], LOOP.total]
_VV = [1.0, 0.98, 0.64, 0.60, -0.60, -0.64, -0.98, -1.0, 1.0]


def Vat(s):
    return float(np.interp(s, _VS, _VV))


def _specs():
    t0, t1, b0_, b1_ = S["top_start"], S["top_end"], S["bot_start"], S["bot_end"]
    return ([(S["tl_mid"], 0.5)] + [(t0 + f * (t1 - t0), 0.55) for f in (0.2, 0.5, 0.8)] + [(S["tr_mid"], 0.5)]
            + [((S["res0"] + S["res1"]) / 2, 1.05), (S["br_mid"], 0.5)]
            + [(b0_ + f * (b1_ - b0_), 0.55) for f in (0.2, 0.5, 0.8)] + [(S["bl_mid"], 0.5)])


E_SPECS = _specs()
J_LEN = 0.55
COL = 3.95
COLW = 5.9


def j_phases():
    return [s_ / LOOP.total for s_, _ in E_SPECS]


def lane(s_, off):
    p, t = LOOP.at(s_)
    n = np.array([-t[1], t[0], 0.0])
    return p + n * off, t


def loop_arrows(kind, z=8):
    g = VGroup()
    for s_, ln in E_SPECS:
        if kind == "E":
            c, t = lane(s_, 0.115)
            L, col = ln, CYAN
        else:
            c, t = lane(s_, -0.115)
            L, col = J_LEN, GREEN
        g.add(halo(arrow(c - t * L / 2, c + t * L / 2, col, 4, z, 0.17), 5))
    return g


def _dens(s_):
    """Densidade superficial ESQUEMÁTICA (módulo): mais carga nos cantos, nos terminais e nas pontas do resistor.
    Não deriva o sinal de V(s): o potencial de referência é arbitrário."""
    cs = [(0.0, 0.8), (S["tl_mid"], 0.9), (S["tr_mid"], 0.9), (S["res0"], 0.35), (S["res1"], 0.35), (S["br_mid"], 0.9),
          (S["bl_mid"], 0.9), (S["b0"], 0.8)]
    return min(1.0, 0.4 + sum(0.5 * np.exp(-((s_ - c) / w) ** 2) for c, w in cs))


def surface_layer(z=7):
    """Camada de carga superficial contínua e esquemática ao longo das duas bordas do condutor."""
    g = VGroup()
    step = 0.15
    s_ = 0.0
    while s_ < S["b0"] - 1e-6:
        s1 = min(s_ + step, S["b0"] - 1e-6)
        a, _ = LOOP.at(s_ + 1e-6)
        b, _ = LOOP.at(s1)
        _, t = LOOP.at((s_ + s1) / 2)
        nr = np.array([-t[1], t[0], 0.0])
        half = 0.42 if S["res0"] <= s_ <= S["res1"] else WT / 2 + 0.02
        w = _dens((s_ + s1) / 2)
        for sg in (1, -1):
            off = nr * sg * half
            g.add(Line(a + off, b + off, stroke_width=12, color=BLUE).set_stroke(opacity=0.22 * w))
            g.add(Line(a + off, b + off, stroke_width=4.5, color=BLUE).set_stroke(opacity=0.95 * w))
        s_ = s1
    return g.set_z_index(z)


def ribbon(z=9):
    """Fita de potencial V(s) acompanhando o circuito, voltada para dentro: fina onde V é baixo, espessa onde é alto."""
    g = VGroup()
    step = 0.15
    s_ = 0.0
    while s_ < LOOP.total - 1e-6:
        s1 = min(s_ + step, LOOP.total - 1e-6)
        a, _ = LOOP.at(s_ + 1e-6)
        b, _ = LOOP.at(s1)
        _, t = LOOP.at((s_ + s1) / 2)
        inw = np.array([t[1], -t[0], 0.0])
        ha, hb = 0.1 + 0.36 * (Vat(s_) + 1) / 2, 0.1 + 0.36 * (Vat(s1) + 1) / 2
        base = 0.36
        q = [a + inw * base, b + inw * base, b + inw * (base + hb), a + inw * (base + ha)]
        g.add(Polygon(*q).set_fill(CYAN, 0.32).set_stroke(width=0))
        g.add(Line(q[3], q[2], stroke_width=3, color=CYAN))
        s_ = s1
    return g.set_z_index(z)


def _sub_path(s0, s1, step=0.1):
    n = max(2, int((s1 - s0) / step) + 1)
    return [LOOP.at(float(x))[0] for x in np.linspace(s0 + 1e-6, s1 - 1e-6, n)]


def _tangents(pts):
    ts = []
    for i in range(len(pts)):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        d = b - a
        ts.append(d / max(np.linalg.norm(d), 1e-9))
    return ts


def conductor_body():
    """Condutor contínuo 2.5D: sombra, contorno com rim light azul, corpo de aço, brilho e sombreado seguindo a curva."""
    shadow, under, body = VGroup(), VGroup(), VGroup()
    light = np.array([-0.35, 0.9, 0.0])
    light = light / np.linalg.norm(light)
    for s0, s1 in ((0.0, S["res0"]), (S["res1"], S["b0"])):
        pts = _sub_path(s0, s1)
        ts = _tangents(pts)
        shadow.add(VMobject().set_points_as_corners([p + np.array([0.1, -0.12, 0.0]) for p in pts]).set_stroke("#000000", 54, 0.45).set_z_index(0))
        under.add(VMobject().set_points_as_corners(pts).set_stroke(BLUE_L, 58, 0.28).set_z_index(1))
        under.add(VMobject().set_points_as_corners(pts).set_stroke(PANEL, 54, 1.0).set_z_index(1))
        body.add(VMobject().set_points_as_corners(pts).set_stroke(STEEL, 46, 1.0).set_z_index(2))
        hi, sh = [], []
        for p, t in zip(pts, ts):
            n = np.array([-t[1], t[0], 0.0])
            k = float(np.dot(n, light))
            hi.append(p + n * k * 0.14)
            sh.append(p - n * k * 0.15)
        body.add(VMobject().set_points_as_corners(sh).set_stroke(PANEL, 7, 0.5).set_z_index(3))
        body.add(VMobject().set_points_as_corners(hi).set_stroke(WHITE, 4, 0.32).set_z_index(3))
    return shadow, under, body


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
PLAN = os.environ.get("PLAN") == "1"
SYNC = os.environ.get("SYNC", "")
UNIT = Path(__file__).resolve().parent
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


def Scene_play(scene, *a, **k):
    return MovingCameraScene.play(scene, *a, **k)


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

    # ── sincronia com a voz ───────────────────────────────────────────────────────────────────────────────────
    #  PLAN=1  : passada a seco (--dry_run) que mede, entre âncoras, a duração nominal de animações e esperas → plan.json
    #  SYNC=ritmo.json : cada intervalo entre âncoras (unidade da narração) recebe fatores de escala para durar exatamente
    #                    o que a voz dura; os tempos são quantizados em quadros pela soma acumulada (sem deriva).
    def _setup_sync(self):
        self._cur = None
        self._lastreq = 0.0
        self._plan = {}
        self._fa, self._fw, self._pad = 1.0, 1.0, 0.0
        self._tgt, self._emit = 0.0, 0
        self._table = json.load(open(SYNC, encoding="utf-8")) if SYNC else {}
        self._raw = False

    def anchor(self, name):
        if self._cur is not None and SYNC and self._pad > 0.02:
            self._idle(self._pad)
        if os.environ.get("DBG") == "1":
            print(f"[ANC] {name} t_cena={self.renderer.time:8.2f} tgt={self._tgt:8.2f} emit_s={self._emit / config.frame_rate:8.2f}", flush=True)
        if os.environ.get("DBG") == "3":
            seen = []
            for m in self.mobjects:
                for f in m.get_family():
                    if isinstance(f, (MathTex, Text)) and f.get_fill_opacity() + f.get_stroke_opacity() > 0.05:
                        seen.append((getattr(f, "tex_string", None) or getattr(f, "text", "") or "").strip()[:28])
            print("[SCN]", name, "|".join(sorted(set(seen))), flush=True)
        self._cur = name
        self._plan.setdefault(name, {"na": 0.0, "nw": 0.0})
        if SYNC:
            r = self._table[name]
            self._fa, self._fw, self._pad = r["fa"], r["fw"], r["pad"]

    def _focus_candidates(self):
        """Objetos recém-chegados à cena (o que a fala está citando): servem de alvo para destaques no lugar de esperas paradas."""
        skip = {id(x) for x in (self.tag, self.wm, self.dim, self.hud_dummy, self.clk, getattr(self, "flow", None),
                                getattr(self, "chip_g", None), getattr(self, "chip_ar", None)) if x is not None}
        out = []
        for m in reversed(self.mobjects):
            if id(m) in skip or m.width < 0.15 or m.width > 12.5:
                continue
            if m.get_family_updaters() or m.z_index < 1:
                continue
            fam = m.family_members_with_points()
            if not fam or max(x.get_fill_opacity() + x.get_stroke_opacity() for x in fam) < 0.5:
                continue
            out.append(m)
            if len(out) >= 4:
                break
        return out[::-1]

    def _idle(self, d):
        """d segundos de 'espera': nada fica parado mais de ~2 s; o excedente vira destaques sobre o que acabou de entrar."""
        rem = d
        cands = self._focus_candidates() if SYNC else []
        i = 0
        while rem > 2.0 and cands:
            seg = 1.3 if rem > 3.3 else max(0.6, rem - 1.0)
            Scene_play(self, Indicate(cands[i % len(cands)], color=WHITE, scale_factor=1.07), run_time=self._q(seg))
            i += 1
            rem -= seg
        if rem > 0.02:
            super().wait(self._q(rem))

    def fill(self, beats):
        """Ocupa o tempo que sobra nesta unidade com estímulos novos (rótulos que surgem e somem, destaques) em vez de esticar
        as animações: cada beat é (duração, função) e só roda se ainda couber na folga (pad) calculada pelo ritmo."""
        if not SYNC:
            return
        self._raw = True
        try:
            for dur, fn in beats:
                if self._pad - dur < -0.15:
                    continue
                fn()
        finally:
            self._raw = False

    def bt(self, target, label, color=CYAN, d=2.6, side=UP, math=False, indicate=True, dx=0.0, dy=0.0, size=26, sc=1.0):
        """Beat: rótulo curto com guia que aparece ao lado de `target`, destaca o alvo e some. Retorna (duração, função)."""
        def fn():
            lab = MathTex(label, font_size=size + 12, color=color) if math else txt(label, size, color)
            lab.scale(sc).set_z_index(30)
            lab.next_to(target, side, buff=0.4 * sc).shift(RIGHT * dx + UP * dy)
            halo(lab)
            gd = Line(lab.get_edge_center(-side), target.get_edge_center(side), stroke_width=2.5 * sc, color=color).set_stroke(opacity=0.8).set_z_index(29)
            self.play(FadeIn(lab, shift=-side * 0.15), Create(gd), run_time=0.5)
            if indicate:
                self.play(Indicate(target, color=color, scale_factor=1.12), run_time=max(0.6, d - 1.0))
            else:
                self.wait(max(0.6, d - 1.0))
            self.play(FadeOut(lab), FadeOut(gd), run_time=0.5)
        return d, fn

    def lk(self, a, b, color=WHITE, d=2.4):
        """Beat: seta que liga a relação (a) ao elemento da figura (b) que ela descreve; ambos destacam, a seta some."""
        def fn():
            ar = Arrow(a.get_center(), b.get_center(), buff=0.55, stroke_width=3, color=color, max_tip_length_to_length_ratio=0.2).set_z_index(29)
            self.play(Create(ar), run_time=0.6)
            self.play(Indicate(a, color=color, scale_factor=1.15), Indicate(b, color=color, scale_factor=1.15), run_time=max(0.6, d - 1.1))
            self.play(FadeOut(ar), run_time=0.5)
        return d, fn

    def pp(self, targets, d=1.6, color=WHITE, scale=1.25):
        """Beat: destaca juntos os elementos que a fala cita (termo da equação + parte da figura)."""
        def fn():
            self.play(*[Indicate(t, color=color, scale_factor=scale) for t in targets], run_time=d)
        return d, fn

    def sweep(self, items, dt=0.45, color=WHITE, scale=1.3):
        """Beat: percorre os itens um a um (trilho do roteiro, passos de uma cadeia)."""
        def fn():
            for it in items:
                self.play(Indicate(it, color=color, scale_factor=scale), run_time=dt)
        return dt * len(items), fn

    def _q(self, rt):
        """quantiza em quadros pela soma acumulada: o instante final de cada trecho cai no quadro certo."""
        fps = config.frame_rate
        self._tgt += rt
        n = max(1, round(self._tgt * fps) - self._emit)
        self._emit += n
        return (n - 0.5) / fps

    def _emit_wait(self, d):
        super().wait(self._q(d))

    def _dbg(self, kind, req, t0):
        if os.environ.get("DBG") == "2":
            import traceback
            d = self.renderer.time - t0
            if abs(d - req) > 0.05:
                ln = [f.lineno for f in traceback.extract_stack() if f.filename.endswith("cena.py")][-1]
                print(f"[LOSS] {kind} pedido={req:.2f} obtido={d:.2f} linha={ln}", flush=True)

    def wait(self, duration=1.0, *a, **k):
        _t0 = self.renderer.time
        self._wait_inner(duration, *a, **k)
        self._dbg("wait", self._lastreq, _t0)

    def _wait_inner(self, duration=1.0, *a, **k):
        self._audit()
        if self._cur is not None:
            self._plan[self._cur]["nw"] += duration
        if SYNC and self._raw:
            self._lastreq = duration
            self._pad -= duration
            super().wait(self._q(duration))
        elif SYNC:
            self._lastreq = duration * self._fw
            self._idle(self._lastreq)
        elif PLAN:
            super().wait(1.0 / config.frame_rate, *a, **k)
        else:
            super().wait(duration, *a, **k)

    def play(self, *a, **k):
        if len(a) == 1 and type(a[0]).__name__ == "Wait":      # Scene.wait chama play(Wait): já foi escalado em wait(); não contar duas vezes
            return super().play(*a, **k)
        _t0 = self.renderer.time
        self._play_inner(*a, **k)
        self._dbg("play", self._lastreq, _t0)

    def _play_inner(self, *a, **k):
        rt = float(k.get("run_time", 1.0))
        if self._cur is not None:
            self._plan[self._cur]["na"] += rt
        if SYNC:
            if self._raw:
                self._pad -= rt
            k["run_time"] = self._q(rt if self._raw else rt * self._fa)
            self._lastreq = k["run_time"]
        elif PLAN:
            k["run_time"] = 1.0 / config.frame_rate
        super().play(*a, **k)
        self._audit()

    def tear_down(self):
        if PLAN:
            json.dump(self._plan, open(UNIT / "plan.json", "w", encoding="utf-8"), indent=1)
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
        config.max_files_cached = 2000     # o padrão (100) apaga os primeiros trechos antes da concatenação final
        config.disable_caching = True      # com tempos escalados pela voz, o cache de partial_movie_files reaproveitaria trechos de duração errada
        self._issues = {}
        self._setup_sync()
        self.clk = ValueTracker(0)
        self.clk.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(self.clk)
        self.camera.background_color = BACKGROUND_COLOR
        fr = self.camera.frame
        self.fr = fr
        self.fw0 = fr.width
        self.tag = txt("ELETROMAGNETISMO · LEI DE OHM E FORÇA ELETROMOTRIZ", 18, opacity=0.6).to_corner(UL, buff=0.38).set_z_index(40)
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
    def make_minimap(self, sc=0.2, c=None):
        """Mini-mapa do circuito (canto superior esquerdo): a corrente segue circulando e o anel mostra de que parte a fala trata,
        enquanto o circuito grande está fora de cena. Retorna (grupo, anel, trackers do anel)."""
        c = P3(-5.7, 3.05) if c is None else c
        outline = VMobject().set_points_as_corners([q * sc + c for q in LOOP.p]).set_stroke(STEEL, 3, 0.9).set_z_index(41)
        bat = Rectangle(width=0.1, height=0.24).set_fill(CYAN, 1).set_stroke(width=0).move_to(P3(LX, (BAT[0] + BAT[1]) / 2) * sc + c).set_z_index(42)
        res = Rectangle(width=0.1, height=0.24).set_fill(WHITE, 1).set_stroke(width=0).move_to(P3(RX, (RES[0] + RES[1]) / 2) * sc + c).set_z_index(42)
        n = 12
        flow = VGroup(*[Line(ORIGIN, RIGHT * 0.05, stroke_width=3, color=GREEN).set_z_index(42) for _ in range(n)])

        def upd(m):
            t = self.clk.get_value()
            for i, ln in enumerate(m):
                p_, tg = LOOP.at((i / n + t * 0.03) * LOOP.total)
                ln.put_start_and_end_on(p_ * sc + c, p_ * sc + c + tg * 0.07)

        flow.add_updater(upd)
        rx, ry = ValueTracker(float(bat.get_center()[0])), ValueTracker(float(bat.get_center()[1]))
        ring = always_redraw(lambda: Circle(radius=0.2 + 0.03 * np.sin(2.4 * self.clk.get_value()), stroke_width=2.5, color=WHITE)
                             .move_to(P3(rx.get_value(), ry.get_value())).set_z_index(43))
        self.mm_pos = {"bat": bat.get_center().copy(), "res": res.get_center().copy()}
        return VGroup(outline, bat, res, flow), ring, (rx, ry)

    def hide_circ(self, rt=0.6):
        """Tira de cena as camadas vivas do circuito (carga de superfície, E, J, cargas) quando o foco é uma equação/cartão."""
        self.J_arr.clear_updaters()
        self.play(FadeOut(self.layer), FadeOut(self.E_arr), FadeOut(self.J_arr), FadeOut(self.sprites), run_time=rt)

    def show_circ(self, rt=0.8):
        self.play(FadeIn(self.layer), FadeIn(self.E_arr), FadeIn(self.J_arr), FadeIn(self.sprites), run_time=rt)
        self.add_shimmer(self.J_arr, j_phases())

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
        shadow, under, wires = conductor_body()
        bw, bh = 0.95, BAT[1] - BAT[0]
        bx, by = LX, (BAT[0] + BAT[1]) / 2
        dx, dy = 0.2, 0.15
        body = VGroup(
            poly([(bx + bw / 2, by + bh / 2), (bx + bw / 2 + dx, by + bh / 2 + dy), (bx + bw / 2 + dx, by - bh / 2 + dy), (bx + bw / 2, by - bh / 2)], PANEL, 0.7, 4),
            poly([(bx - bw / 2, by + bh / 2), (bx + bw / 2, by + bh / 2), (bx + bw / 2 + dx, by + bh / 2 + dy), (bx - bw / 2 + dx, by + bh / 2 + dy)], BLUE_L, 0.4, 4),
            RoundedRectangle(corner_radius=0.2, width=bw, height=bh, stroke_width=2).set_fill(PANEL, 1).set_stroke(BLUE_L, 2, 0.9)
            .move_to(P3(bx, by)).set_z_index(5),
            Line(P3(bx - .36, BAT[1] - .3), P3(bx + .36, BAT[1] - .3), stroke_width=5, color=WHITE).set_z_index(6),
            Line(P3(bx - .2, BAT[1] - .62), P3(bx + .2, BAT[1] - .62), stroke_width=5, color=WHITE).set_z_index(6))
        bat_pm = VGroup(MathTex("+", font_size=34, color=WHITE).move_to(P3(LX - .82, BAT[1] - .3)),
                        MathTex("-", font_size=34, color=WHITE).move_to(P3(LX - .82, BAT[1] - .62))).set_z_index(6)
        rw, rh = 0.8, RES[1] - RES[0]
        zz = [P3(RX, RES[1] - 0.12)] + [P3(RX + (0.17 if i % 2 else -0.17), RES[1] - 0.12 - (i + 0.5) * (rh - 0.24) / 8) for i in range(8)] + [P3(RX, RES[0] + 0.12)]
        res = VGroup(
            RoundedRectangle(corner_radius=0.36, width=rw, height=rh, stroke_width=2).set_fill(PANEL, 1).set_stroke(BLUE_L, 2, 0.9)
            .move_to(P3(RX, (RES[0] + RES[1]) / 2)).set_z_index(5),
            rect(RX - rw / 2 + 0.05, RES[0] + 0.25, RX - rw / 2 + 0.11, RES[1] - 0.25, WHITE, 0.25, 6),
            VMobject().set_points_as_corners(zz).set_stroke(CYAN, 9, 0.22).set_z_index(6),
            VMobject().set_points_as_corners(zz).set_stroke(WHITE, 2.5).set_z_index(6))
        self.lbl_bat = txt("fonte", 22, DIM).move_to(P3(LX - 1.2, BAT[0] - 0.4)).set_z_index(5)
        self.lbl_res = txt("resistor", 22, DIM).move_to(P3(RX + 1.15, RES[0] - 0.4)).set_z_index(5)
        self.bat_g, self.res_g = VGroup(body, bat_pm), res
        self.base = VGroup(shadow, under, wires)
        self.world = VGroup(self.base, self.bat_g, self.res_g, self.lbl_bat, self.lbl_res)

    # ═══ 0. INTRODUÇÃO: gancho de curiosidade (o que você vai entender) ═══════════════════════════════════════
    def pulse(self, items, rt=1.0, color=WHITE, scale=1.15, rounds=1):
        """Destaca, um a um, os elementos que a fala está citando (movimento com significado, não espera parada)."""
        for _ in range(rounds):
            for it in items:
                self.play(Indicate(it, color=color, scale_factor=scale), run_time=rt)

    def make_flow(self, n=26):
        """Pulsos de corrente correndo pelo condutor (sob a fonte e o resistor): o circuito nunca fica parado."""
        g = VGroup(*[Line(ORIGIN, RIGHT * 0.2, stroke_width=5, color=GREEN).set_z_index(3.5) for _ in range(n)])

        def upd(m):
            t = self.clk.get_value()
            for i, ln in enumerate(m):
                p_, tg = LOOP.at((i / n + t * 0.035) * LOOP.total)
                ln.put_start_and_end_on(p_, p_ + tg * 0.2)
                ln.set_stroke(opacity=0.5)

        g.add_updater(upd)
        return g

    def res_glow(self):
        g = RoundedRectangle(corner_radius=0.42, width=1.05, height=RES[1] - RES[0] + 0.25, stroke_width=6, color=CYAN)
        g.move_to(P3(RX, (RES[0] + RES[1]) / 2)).set_z_index(14).set_fill(CYAN, 0.0)
        g.set_stroke(opacity=0.55)        # fixo: o circuito ao fundo não pisca
        return g

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

    # ═══ 13. ENCERRAMENTO: chamada para ação, ligada ao conteúdo ════════════════════════════════════════════
    def encerramento(self):
        self.next_section("B13_encerramento")
        self.anchor("N058")
        self.flow.clear_updaters()
        self.remove(self.flow)
        back = self.make_backdrop(0.4, z=13, sc=1.7)
        self.add(back)
        logo = ImageMobject(str(WATERMARK_PATH)).set_width(4.2).move_to(P3(0, 0.6)).set_z_index(30)
        self.play(FadeIn(logo, shift=UP * 0.1), run_time=1.2)
        self.wait(2.0)
        q = txt("Você já conhecia o papel das cargas superficiais?", 28, WHITE).move_to(P3(0, -1.3)).set_z_index(30)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=1.0)
        self.wait(2.0)

        # ── N059: gancho para o próximo vídeo — aparato pronto do yt_0010 (barra, trilhos, B entrando, corrente) ──
        self.anchor("N059")
        self.play(FadeOut(logo), FadeOut(VGroup(q, back)), run_time=0.8)
        self.remove(back)
        self.remove(self.world)
        self.set_dim(0.0, 0.3)
        import importlib.util
        spec = importlib.util.spec_from_file_location("yt0010_cena", Path(__file__).resolve().parents[1] / "yt_0010_fem_movimento" / "cena.py")
        y10 = importlib.util.module_from_spec(spec)
        sys.modules["yt0010_cena"] = y10
        spec.loader.exec_module(y10)
        ap = y10.Ap()
        ap.s.set_value(y10.LAYOUTS["hook"][0])
        ap.cx.set_value(y10.LAYOUTS["hook"][1])
        ap.cy.set_value(y10.LAYOUTS["hook"][2])
        tickm = Mobject()
        tickm.add_updater(lambda m, dt: ap.tick(dt))
        body = always_redraw(ap.build)
        self.add(tickm, body)
        self.play(ap.oAll.animate.set_value(1), ap.oB.animate.set_value(1), run_time=1.4)
        self.play(ap.oBar.animate.set_value(1), run_time=1.0)
        self.play(ap.oI.animate.set_value(1), ap.cur.animate.set_value(1), run_time=1.4)
        fb = M(r"\mathbf F_B", r"\perp", r"\mathbf v", size=M_L).move_to(P3(0, -1.85)).set_z_index(34)
        self.play(FadeIn(fb, shift=UP * 0.1), run_time=1.0)
        self.wait(1.6)
        self.play(FadeOut(fb), run_time=0.5)
        qn = txt("de onde vem a energia?", T_HEAD, WHITE).move_to(P3(0, -1.85)).set_z_index(34)
        self.play(FadeIn(qn, shift=UP * 0.1), ap.heat.animate.set_value(1), run_time=1.6)
        self.fill([self.pp([qn], 1.6, WHITE, 1.08), self.pp([qn], 1.4, CYAN, 1.08)])
        self.play(FadeOut(qn), run_time=0.5)
        nx = txt("próximo vídeo", 22, DIM).move_to(P3(0, -1.7)).set_z_index(34)
        nt = txt("fem de movimento", 40, WHITE).move_to(P3(0, -2.4)).set_z_index(34)
        self.play(FadeIn(nx, shift=UP * 0.1), FadeIn(nt, shift=UP * 0.1), run_time=1.2)
        self.wait(2.5)

    # ═══ 1. QUEM AGE LOCALMENTE ═════════════════════════════════════════════════════════════════════════════
    def abertura_local(self):
        self.next_section("B01_gancho")
        self.anchor("N001")
        fr = self.fr
        self.play(LaggedStart(FadeIn(self.base[0]), FadeIn(self.base[1]), FadeIn(self.base[2]), FadeIn(self.bat_g),
                              FadeIn(self.res_g), lag_ratio=0.25), run_time=2.4)
        self.play(FadeIn(self.lbl_bat), FadeIn(self.lbl_res), run_time=0.6)
        self.flow = self.make_flow()
        self.add(self.flow)
        ring = Circle(radius=0.95, color=CYAN, stroke_width=3).move_to(P3(LX, (BAT[0] + BAT[1]) / 2)).set_z_index(9)
        self.play(FadeIn(ring, scale=1.3), Indicate(self.bat_g, color=WHITE, scale_factor=1.1), run_time=1.2)
        self.play(FadeOut(ring), run_time=0.3)
        # câmera de verdade: acompanha o fio da fonte até um trecho distante
        self.play(fr.animate.scale(0.45).move_to(P3(-4.2, 0.4)), run_time=2.2)
        self.play(fr.animate.move_to(P3(3.4, 1.0)), run_time=5.0)
        self.anchor("N002")
        cpos = P3(3.3, TOP)
        carrier = VGroup(Circle(radius=0.11, stroke_width=0).set_fill(BLUE_L, 1).move_to(cpos),
                         Line(cpos + LEFT * .06, cpos + RIGHT * .06, stroke_width=2.5, color=PANEL)).set_z_index(9)
        carrier.move_to(cpos)
        cring = Circle(radius=0.3, color=WHITE, stroke_width=3).move_to(cpos).set_z_index(9)
        self.play(FadeIn(carrier, scale=0.4), FadeIn(cring, scale=1.8), run_time=0.8)
        cring.add_updater(lambda m: m.set_stroke(opacity=0.45 + 0.55 * np.sin(np.pi * self.clk.get_value() * 0.9) ** 2))
        r = fr.width / self.fw0
        q = VGroup(NT(), txt("Que força age sobre", T_HEAD, WHITE),
                   txt("uma carga aqui, agora?", T_HEAD, WHITE)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        q.scale(r).move_to(fr.get_center() + P3(-3.4, -1.35) * r).set_z_index(30)
        halo(q)
        self.play(FadeIn(q, shift=UP * 0.1), Indicate(cring, color=CYAN, scale_factor=1.3), run_time=1.2)
        far = DashedLine(P3(LX + 0.4, TOP), cpos + LEFT * 0.4, color=CYAN, stroke_width=4).set_z_index(9)
        far.set_stroke(opacity=0.0)
        xmid = P3(0.9, TOP)
        xcross = Cross(Circle(radius=0.28).move_to(xmid), stroke_color=WHITE, stroke_width=5).set_z_index(10)
        self.play(far.animate.set_stroke(opacity=0.85), run_time=0.9)
        self.play(Create(xcross), run_time=0.7)
        self.wait(0.6)
        self.play(FadeOut(far), FadeOut(xcross), run_time=0.7)
        self.wait(0.8)

        # marca + título + mapa conceitual (sem fórmulas), sobre o enquadramento atual da câmera
        def fx(m, x, y):
            m.scale(r)
            return m.move_to(fr.get_center() + P3(x, y) * r).set_z_index(30)

        self.fill([self.bt(carrier, "uma carga", BLUE_L, 2.4, UP, indicate=False, sc=r),
                   self.bt(pt(2.2, TOP), "corrente passando", GREEN, 2.6, UP, indicate=False, sc=r),
                   self.bt(pt(0.9, TOP), "fonte longe", DIM, 2.4, UP, indicate=False, sc=r)])
        self.anchor("N003")
        self.play(FadeOut(q), self.dim.animate.set_fill(BACKGROUND_COLOR, 1.0), run_time=1.0)
        logo = ImageMobject(str(WATERMARK_PATH)).set_width(2.6)
        logo.scale(r).move_to(fr.get_center() + P3(0, 1.55) * r).set_z_index(30)
        welcome = fx(txt("Bem-vindos ao Parallax Lab", 30, DIM), 0, 0.55)
        title = fx(txt("Quem empurra as cargas?", 52, WHITE), 0, -0.3)
        sub = fx(txt("Campo elétrico, Lei de Ohm e força eletromotriz", 26, DIM), 0, -1.05)
        self.play(FadeIn(logo, shift=UP * 0.1 * r), FadeIn(welcome, shift=UP * 0.1 * r), run_time=1.2)
        self.play(FadeIn(title, shift=UP * 0.15 * r), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.1 * r), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(logo), FadeOut(welcome), FadeOut(title), FadeOut(sub), run_time=0.8)
        self.anchor("N004")
        nodes = VGroup()
        for label, col in (("força local", FC), ("campo no circuito", CYAN), ("fonte e energia", GREEN)):
            t = txt(label, 28, WHITE)
            rr = RoundedRectangle(corner_radius=0.25, width=t.width + 0.8, height=0.95, stroke_width=2.5)
            rr.set_fill(PANEL, 0.95).set_stroke(col, 2.5, 1.0)
            nodes.add(VGroup(rr, t.move_to(rr)))
        nodes.arrange(RIGHT, buff=1.3)
        arrs = VGroup(*[MathTex(r"\rightarrow", font_size=54, color=DIM).move_to((nodes[i].get_right() + nodes[i + 1].get_left()) / 2) for i in range(2)])
        mapa = VGroup(nodes, arrs)
        mapa.scale(r, scale_stroke=True).move_to(fr.get_center() + P3(0, 0.1) * r).set_z_index(30)
        for i in range(3):
            self.play(FadeIn(nodes[i], shift=UP * 0.1 * r), *([FadeIn(arrs[i - 1])] if i else []), run_time=0.9)
            self.wait(0.9)
        self.wait(1.0)
        self.pulse(list(nodes), rt=1.0, rounds=2, scale=1.1)
        self.anchor("N005")
        self.play(FadeOut(mapa), self.dim.animate.set_fill(BACKGROUND_COLOR, 0.0), run_time=1.0)
        # mergulho no fio
        self.play(fr.animate.scale(0.42).move_to(cpos), run_time=4.5)
        self.wait(1.5)
        cring.clear_updaters()
        self.hook_extra = VGroup(carrier, cring)

    # ═══ 2. CONDUÇÃO LOCAL: E → J = σE ═════════════════════════════════════════════════════════════════════
    def conducao_local(self):
        self.next_section("B02_conducao_local")
        self.anchor("N006")
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
        self.flow.clear_updaters()
        self.remove(self.flow)
        self.fr.move_to(ORIGIN)
        self.fr.scale(self.fw0 / self.fr.width)
        self.remove(self.base[0], self.base[1], self.base[2], self.bat_g, self.res_g, self.lbl_bat, self.lbl_res)
        self.add(micro)
        note0 = NT().move_to(P3(-3.2, -2.35))
        self.play(self.dim.animate.set_fill(BACKGROUND_COLOR, 0.0), FadeIn(note0), run_time=1.2)
        self.wait(3.5)
        self.pulse([ions_f, elec, ions_f, elec], rt=1.1, scale=1.04)
        self.anchor("N007")
        # E aparece: resposta local
        e_arrows = VGroup(*[halo(arrow(P3(x - 0.6, cy + 0.95), P3(x + 0.6, cy + 0.95), CYAN, 5, 9, 0.22)) for x in (-5.6, -3.4, -1.2)])
        e_lab = MathTex(r"\mathbf E", font_size=44, color=CYAN).move_to(P3(-6.3, cy + 1.7))
        halo(e_lab)
        note1 = NT().next_to(e_lab, RIGHT, buff=0.25)
        self.play(LaggedStart(*[FadeIn(a, shift=RIGHT * 0.2) for a in e_arrows], lag_ratio=0.25), FadeIn(e_lab), FadeIn(note1), run_time=1.6)
        self.wait(1.0)
        probe = Circle(radius=0.55, color=WHITE, stroke_width=3).move_to(P3(-5.6, cy + 0.95)).set_z_index(9)
        probe.set_stroke(opacity=0.0)
        self.play(probe.animate.set_stroke(opacity=0.9), run_time=0.5)
        for k_, x_ in enumerate((-3.4, -1.2)):
            self.play(probe.animate.move_to(P3(x_, cy + 0.95)), Indicate(e_arrows[k_], color=WHITE, scale_factor=1.3), run_time=1.1)
        self.play(Indicate(e_arrows[2], color=WHITE, scale_factor=1.3), FadeOut(probe), run_time=0.8)
        self.fill([self.bt(e_lab, "campo elétrico", CYAN, 2.4, RIGHT),
                   self.bt(pt(-3.6, cy - 0.35), "elétrons livres", BLUE_L, 2.6, DOWN, indicate=False),
                   self.bt(pt(-4.6, cy + 0.35), "íons fixos", STEEL, 2.4, UP, indicate=False)])
        self.anchor("N008")
        # quem empurra? a força elétrica sobre um portador
        f0 = M(r"\mathbf F", "=", "q", r"\mathbf E", size=M_L).move_to(P3(COL, 1.55))
        f1 = M(r"\mathbf F", "=", "-e", r"\mathbf E", size=M_L).move_to(P3(COL, 1.55))
        fnote0 = rich("$q$: carga do portador", T_NOTE, caps=False).move_to(P3(COL, 0.7))
        fnote1 = NT().move_to(P3(COL, 0.7))
        self.play(Write(f0), FadeIn(fnote0, shift=UP * 0.1), run_time=1.6)
        self.wait(2.0)
        self.play(TransformMatchingTex(f0, f1), FadeOut(fnote0), FadeIn(fnote1, shift=UP * 0.1), drift.animate.set_value(1.0), run_time=1.8)
        self.wait(2.2)
        self.play(FadeOut(f1), FadeOut(fnote1), run_time=0.7)
        self.anchor("N009")
        # a deriva média nasce: o conjunto desliza, pouco; o centro do conjunto marca o deslocamento médio
        xc0 = -1.0
        ghost = DashedLine(P3(xc0, cy - hh / 2 - 0.15), P3(xc0, cy + hh / 2 + 0.15), color=WHITE, stroke_width=2).set_stroke(opacity=0.6).set_z_index(6)
        cur = always_redraw(lambda: Line(P3(xc0 - Dd.get_value(), cy - hh / 2 - 0.15), P3(xc0 - Dd.get_value(), cy + hh / 2 + 0.15),
                                         color=VIOLET, stroke_width=4).set_z_index(6))
        d_arr = always_redraw(lambda: halo(arrow(P3(xc0, cy - hh / 2 - 0.4), P3(xc0 - max(Dd.get_value(), 0.02), cy - hh / 2 - 0.4), VIOLET, 5, 9, 0.2)))
        d_lab = MathTex(r"\mathbf v_d", font_size=40, color=VIOLET).move_to(P3(-2.6, cy - hh / 2 - 0.72))
        d_note = NT().next_to(d_lab, RIGHT, buff=0.25)
        d_lab.set_opacity(0)
        d_note.set_opacity(0)
        self.add(cur, d_arr, d_lab, d_note)
        self.play(drift.animate.set_value(1.0), FadeOut(note0), FadeIn(ghost), run_time=2.0)
        self.play(d_lab.animate.set_opacity(1), d_note.animate.set_opacity(1), run_time=0.8)
        self.wait(5.5)
        self.pulse([cur, d_arr, ghost, d_arr], rt=1.1, color=VIOLET, scale=1.12)
        self.anchor("N010")
        j_arr = halo(arrow(P3(-5.6, -2.55), P3(-2.2, -2.55), GREEN, 7, 9, 0.28))
        j_lab = MathTex(r"\mathbf J", font_size=44, color=GREEN).next_to(j_arr, LEFT, buff=0.2)
        j_note = NT().next_to(j_arr, RIGHT, buff=0.25)
        self.play(FadeOut(d_note), FadeOut(d_lab), run_time=0.4)
        self.play(FadeIn(j_arr, shift=RIGHT * 0.3), FadeIn(j_lab), FadeIn(j_note), run_time=1.4)
        self.wait(1.0)
        # checagem de sinal: elétrons derivam contra E, mas J ∥ E
        k0 = M(r"\mathbf J", "=", "nq", r"\mathbf v_d", size=M_L).move_to(P3(COL, 1.55))
        k1 = M(r"\mathbf J", "=", "-ne", r"\mathbf v_d", size=M_L).move_to(P3(COL, 1.55))
        k_note0 = NT().move_to(P3(COL, 0.7))
        k_par = M(r"\mathbf J", r"\parallel", r"\mathbf E", size=M_L).move_to(P3(COL, -0.7))
        defs = gloss_rows([gi("n", WHITE, "portadores por volume"), gi("q", WHITE, "carga do portador"), gi(r"\mathbf v_d", VIOLET, "velocidade de deriva")], P3(4.2, -1.9))
        self.play(Write(k0), FadeIn(defs), run_time=1.5)
        self.wait(1.0)
        self.play(FadeIn(k_note0, shift=UP * 0.1), TransformMatchingTex(k0, k1), run_time=1.6)
        self.wait(1.0)
        k_note1 = NT().move_to(P3(COL, 0.1))
        self.play(FadeOut(k_note0), FadeIn(k_note1, shift=UP * 0.1), run_time=1.0)
        self.wait(2.0)
        self.play(FadeIn(k_par, shift=UP * 0.1), run_time=1.0)
        kb = box(k_par, GREEN)
        self.play(FadeIn(kb), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(VGroup(k1, k_note1, k_par, kb, defs)), run_time=0.8)
        self.pulse([d_arr, j_arr, e_arrows, j_arr], rt=1.1, scale=1.12)
        self.anchor("N011")
        fd = M(r"\mathbf f", r"\equiv", r"\frac{\mathbf F}{q}", size=M_L).move_to(P3(COL, 1.55))
        fdn = txt("força por unidade de carga", T_CAP, DIM, caps=False).move_to(P3(COL, 0.7))
        self.play(Write(fd), FadeIn(fdn, shift=UP * 0.1), run_time=1.6)
        self.wait(1.8)
        self.pulse([fd, fdn, fd], rt=1.0, scale=1.12)
        self.play(FadeOut(fd), FadeOut(fdn), run_time=0.6)
        self.anchor("N012")
        # fórmula local, depois do fenômeno
        eq0 = M(r"\mathbf J", "=", r"\sigma", r"\mathbf f", size=M_L).move_to(P3(COL, 1.2))
        eq1 = M(r"\mathbf J", "=", r"\sigma", r"\mathbf E", size=M_L).move_to(eq0)
        note_f = M(r"\mathbf f", "=", r"\mathbf E", size=M_M).move_to(P3(COL, 0.1))
        self.play(Write(eq0), run_time=1.5)
        self.play(FadeIn(note_f, shift=UP * 0.1), run_time=0.8)
        self.wait(1.0)
        self.play(TransformMatchingTex(eq0, eq1), run_time=1.5)
        bx = box(eq1)
        self.play(FadeIn(bx), run_time=0.6)
        self.wait(2.0)
        self.pulse([bx, eq1, e_arrows, j_arr], rt=1.1, scale=1.1)
        elec.clear_updaters()
        cur.clear_updaters()
        d_arr.clear_updaters()
        self.micro_ui = VGroup(note1, e_lab, e_arrows, ghost, cur, d_arr, j_arr, j_lab, j_note)
        self.micro_eq = VGroup(eq1, bx, note_f)

    # ═══ 3-4. DA LEI LOCAL PARA V = IR ═════════════════════════════════════════════════════════════════════
    def ohm_macroscopica(self):
        self.next_section("B03_ohm_macro")
        self.anchor("N013")
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
        Vtxt = NT().next_to(V_lab, RIGHT, buff=0.2)
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
        self.gl_ohm = VGroup(gloss_rows([gi("J", GREEN, "densidade de corrente", 20), gi("I", GREEN, "corrente", 20), gi("A", VIOLET, "área da seção", 20)], P3(-5.0, -2.0)),
                             gloss_rows([gi("L", VIOLET, "comprimento do trecho", 20), gi("V", CYAN, "queda de potencial", 20), gi(r"\sigma", WHITE, "condutividade", 20)], P3(-1.3, -2.0)))
        self.play(FadeIn(self.gl_ohm), run_time=0.8)
        self.fill([self.bt(mbody, "o fio como cilindro", WHITE, 2.6, DOWN, indicate=False)])
        self.anchor("N014")
        # origem de I = JA: a seção A acende e J a atravessa
        self.play(FadeIn(face), FadeIn(A_lab), run_time=0.8)
        self.play(FadeIn(j_face, shift=RIGHT * 0.15), face.animate.set_fill(VIOLET, 0.6), run_time=1.0)
        i0 = EQ(r"I=\int_{A}\mathbf J\cdot d\mathbf a", "I", r"\mathbf J", "A", r"d\mathbf a", size=M_M, width=COLW).move_to(P3(COL, 0.2))
        i1 = EQ(r"I=JA", "I", "J", "A", size=M_L, width=COLW).move_to(P3(COL, 0.2))
        i2 = EQ(r"J=\frac{I}{A}", "J", "I", "A", size=M_L, width=COLW).move_to(P3(COL, 0.2))
        n_u = NT().move_to(P3(COL, -0.65))
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
        self.anchor("N015")
        # origem de V = EL: o caminho L acende e E o percorre
        self.play(FadeIn(Lline), FadeIn(L_lab), FadeIn(Vline), FadeIn(V_lab), FadeIn(Vtxt), run_time=1.0)
        path = Line(P3(wx0, wy), P3(wx1, wy), stroke_width=5, color=CYAN).set_z_index(8).set_stroke(opacity=0.0)
        self.add(path)
        self.play(path.animate.set_stroke(opacity=0.9), Indicate(mE, color=WHITE), run_time=1.4)
        v0 = EQ(r"V=\left|\int_0^{L}\mathbf E\cdot d\boldsymbol\ell\right|", "V", "L", r"\mathbf E", size=M_M, width=COLW).move_to(P3(COL, 0.2))
        v1 = EQ(r"V=EL", "V", "E", "L", size=M_L, width=COLW).move_to(P3(COL, 0.2))
        v2 = EQ(r"E=\frac{V}{L}", "E", "V", "L", size=M_L, width=COLW).move_to(P3(COL, 0.2))
        n_e = NT().move_to(P3(COL, -0.65))
        self.play(Write(v0), run_time=1.8)
        self.play(FadeIn(n_e, shift=UP * 0.1), run_time=0.8)
        self.wait(0.8)
        self.play(gmap(v0, v1, ("V", "V"), (r"\mathbf E", "E"), ("L", "L")), FadeOut(n_e), run_time=2.0)
        self.add(v1)
        self.wait(0.8)
        self.play(gmap(v1, v2, ("V", "V"), ("E", "E"), ("L", "L")), run_time=1.8)
        self.add(v2)
        self.play(v2.animate.scale(0.75).move_to(P3(COL, 1.45)), FadeOut(path), run_time=1.0)
        self.anchor("N016")
        r3 = M("J", "=", r"\sigma", "E", size=M_S).scale(0.75).move_to(P3(COL, 0.65))
        self.play(FadeIn(r3, shift=RIGHT * 0.2), Indicate(mE, color=WHITE), Indicate(mJ, color=WHITE), run_time=1.6)
        for rel_, figs_ in ((i2, (face, I_arr)), (v2, (Lline, V_lab)), (r3, (mE, mJ))):
            self.play(Indicate(rel_, color=WHITE, scale_factor=1.3), *[Indicate(f_, color=WHITE) for f_ in figs_], run_time=1.8)
            self.wait(0.8)
        self.fill([self.lk(i2, face, GREEN, 2.4), self.lk(v2, Vline, CYAN, 2.4), self.lk(r3, mE, CYAN, 2.4)])
        rels = VGroup(i2, v2, r3)
        self.macro = VGroup(mbody, rim, face, A_lab, Lline, L_lab, Vline, V_lab, Vtxt, I_arr, I_lab, mE, mJ)

        self.next_section("B04_ohm_derivacao")
        self.anchor("N017")
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
        self.play(rels.animate.set_opacity(0.6), run_time=0.6)
        self.play(FadeIn(C0, shift=UP * 0.15), run_time=1.2)
        self.wait(0.8)
        self.anchor("N018")
        # J e E recebem, de fato, as expressões que já deduzimos: J ← I/A e E ← V/L
        jg, eg = glyphs(C0, "J"), glyphs(C0, "E")
        k_ = 1 / 0.75
        t1 = VGroup(*i2[0][2:]).copy().scale(k_).move_to(jg.get_center())
        t2 = VGroup(*v2[0][2:]).copy().scale(k_).move_to(eg.get_center())
        self.play(jg.animate.set_opacity(0), eg.animate.set_opacity(0), TransformFromCopy(VGroup(*i2[0][2:]), t1),
                  TransformFromCopy(VGroup(*v2[0][2:]), t2), run_time=2.2)
        self.add(t1, t2)
        self.play(Indicate(t1, color=GREEN, scale_factor=1.25), Indicate(t2, color=CYAN, scale_factor=1.25), run_time=1.8)
        self.wait(0.8)
        self.play(FadeOut(VGroup(C0, t1, t2)), FadeIn(C2), run_time=0.9)
        self.add(C2)
        self.wait(1.0)
        for _, fn_ in (self.lk(C2, face, GREEN, 2.4), self.lk(C2, Vline, CYAN, 2.4)):
            fn_()
        self.pulse([glyphs(C2, "I"), i2, glyphs(C2, "V"), v2], rt=1.0, scale=1.18, rounds=1)
        self.anchor("N019")
        mulL = MathTex(r"\times\,A\,L", font_size=44, color=VIOLET).next_to(C2, UP, buff=0.35).shift(LEFT * 1.4).set_z_index(30)
        mulR = MathTex(r"\times\,A\,L", font_size=44, color=VIOLET).next_to(C2, UP, buff=0.35).shift(RIGHT * 1.4).set_z_index(30)
        self.play(FadeIn(mulL, shift=DOWN * 0.2), FadeIn(mulR, shift=DOWN * 0.2), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(mulL), FadeOut(mulR), run_time=0.6)
        self.play(gmap(C2, C3), run_time=2.4)
        self.add(C3)
        self.wait(1.0)
        self.fill([self.lk(C3, face, VIOLET, 2.5), self.lk(C3, Lline, VIOLET, 2.5)])
        self.anchor("N020")
        self.play(gmap(C3, S3f), run_time=2.4)
        self.add(S3f)
        self.wait(0.8)
        self.fill([self.lk(S3f, Vline, CYAN, 2.5), self.lk(S3f, Lline, VIOLET, 2.5)])
        self.anchor("N021")
        S3c.move_to(S3f)
        self.remove(S3f)
        self.add(S3c)
        blk = glyphs(S3c, r"\frac{L}{\sigma A}")
        bk = SurroundingRectangle(blk, color=VIOLET, buff=0.12, stroke_width=3, corner_radius=0.08).set_z_index(22)
        self.play(FadeIn(bk), Indicate(Lline, color=WHITE), Indicate(face, color=WHITE), run_time=1.2)
        for col_ in (CYAN, GREEN, VIOLET):
            self.play(bk.animate.set_color(col_), Indicate(self.gl_ohm, color=WHITE, scale_factor=1.05), run_time=1.0)
        blk_note = NT().next_to(bk, DOWN, buff=0.35)
        self.play(FadeIn(blk_note, shift=UP * 0.1), run_time=0.8)
        self.wait(2.0)
        self.fill([self.lk(bk, Lline, VIOLET, 2.6), self.lk(bk, face, VIOLET, 2.6),
                   self.bt(bk, "só geometria e material", WHITE, 2.8, DOWN)])
        self.anchor("N022")
        Df.move_to(P3(COL, -2.05))
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
        self.anchor("N023")
        cons = rich(r"$L\uparrow\Rightarrow R\uparrow,\qquad A\uparrow\Rightarrow R\downarrow$", T_NOTE).move_to(P3(COL, 1.5))
        self.play(FadeIn(cons, shift=UP * 0.1), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(self.macro), run_time=0.8)
        Lt, At = ValueTracker(1.0), ValueTracker(1.0)

        def cyl():
            Lc = 4.2 * Lt.get_value()
            Hc = 0.95 * At.get_value() ** 0.5
            return VGroup(pipe(-6.0, 0.4 - Hc / 2, -6.0 + Lc, 0.4 + Hc / 2, True, 2),
                          Ellipse(width=0.4, height=Hc).set_fill(VIOLET, 0.4).set_stroke(VIOLET, 3).move_to(P3(-6.0 + Lc, 0.4)).set_z_index(4))

        demo = always_redraw(cyl)
        rbar = always_redraw(lambda: Rectangle(width=1.5 * Lt.get_value() / At.get_value(), height=0.3).set_fill(WHITE, 0.9)
                             .set_stroke(width=0).move_to(P3(-5.0 + 0.75 * Lt.get_value() / At.get_value(), -1.0)).set_z_index(30))
        rlab = MathTex("R", font_size=44, color=WHITE).move_to(P3(-6.3, -1.0)).set_z_index(30)
        Llab = MathTex("L", font_size=40, color=VIOLET).move_to(P3(-3.9, 1.5)).set_z_index(30)
        Alab = MathTex("A", font_size=40, color=VIOLET).move_to(P3(-1.2, 1.5)).set_z_index(30)
        self.add(demo, rbar)
        self.play(FadeIn(rlab), FadeIn(Llab), FadeIn(Alab), run_time=0.8)
        self.play(Lt.animate.set_value(1.5), run_time=1.6)
        self.play(Lt.animate.set_value(1.0), run_time=1.2)
        self.play(At.animate.set_value(2.0), run_time=1.6)
        self.play(At.animate.set_value(1.0), run_time=1.2)
        demo.clear_updaters()
        rbar.clear_updaters()
        self.play(FadeOut(VGroup(demo, rbar, rlab, Llab, Alab)), run_time=0.8)
        self.remove(demo, rbar)
        self.anchor("N024")
        mJ.clear_updaters()
        self.play(FadeOut(cons), FadeOut(S4), FadeOut(bs), FadeOut(self.gl_ohm), FadeIn(self.world), run_time=1.2)
        # N024: no circuito, a mesma corrente em série; nos fios a queda é pequena, no resistor é grande
        self.flow = self.make_flow()
        self.add(self.flow)
        gy = -0.95
        g_small = Rectangle(width=0.3, height=0.001).set_fill(CYAN, 1).set_stroke(width=0).move_to(P3(-1.8, gy)).align_to(P3(0, gy), DOWN).set_z_index(30)
        g_big = Rectangle(width=0.3, height=0.001).set_fill(CYAN, 1).set_stroke(width=0).move_to(P3(2.6, gy)).align_to(P3(0, gy), DOWN).set_z_index(30)
        l_small = MathTex(r"\Delta V", font_size=34, color=CYAN).move_to(P3(-1.8, gy - 0.35)).set_z_index(30)
        l_big = MathTex(r"\Delta V", font_size=34, color=CYAN).move_to(P3(2.6, gy - 0.35)).set_z_index(30)
        top_hi = Rectangle(width=2.6, height=0.55).set_fill(CYAN, 0.0).set_stroke(CYAN, 3, 1.0).move_to(P3(0, TOP)).set_z_index(30)
        res_hi = Rectangle(width=0.9, height=1.6).set_fill(CYAN, 0.0).set_stroke(CYAN, 3, 1.0).move_to(P3(RX, (RES[0] + RES[1]) / 2)).set_z_index(30)
        self.wait(1.0)
        self.add(g_small, g_big)
        self.play(FadeIn(top_hi), FadeIn(l_small), run_time=0.8)
        g_small.generate_target()
        g_small.target = Rectangle(width=0.3, height=0.14).set_fill(CYAN, 1).set_stroke(width=0).move_to(P3(-1.8, gy + 0.07)).set_z_index(30)
        self.play(MoveToTarget(g_small), run_time=1.0)
        self.wait(0.8)
        self.play(FadeIn(res_hi), FadeIn(l_big), run_time=0.8)
        g_big.generate_target()
        g_big.target = Rectangle(width=0.3, height=1.5).set_fill(CYAN, 1).set_stroke(width=0).move_to(P3(2.6, gy + 0.75)).set_z_index(30)
        self.play(MoveToTarget(g_big), run_time=1.6)
        self.wait(1.2)
        self.fill([self.bt(top_hi, "fio: queda pequena", CYAN, 2.4, DOWN, indicate=False)])
        self.play(FadeOut(VGroup(g_small, g_big, l_small, l_big, top_hi, res_hi)), run_time=0.8)

    # ═══ 5-6. QUEM ESTABELECE E? — CONTINUIDADE ═══════════════════════════════════════════════════════════════
    def continuidade(self):
        self.next_section("B05_segunda_pergunta")
        self.anchor("N025")
        self.E_arr = loop_arrows("E")
        self.J_arr = loop_arrows("J")
        self.ribbon = ribbon()
        self.play(LaggedStart(*[FadeIn(a, shift=0.1 * RIGHT) for a in self.E_arr], lag_ratio=0.12), run_time=2.6)
        pot = NT().move_to(P3(0, -0.25)).set_z_index(30)
        self.play(FadeIn(self.ribbon), FadeIn(pot), run_time=1.6)
        self.wait(1.0)
        self.play(FadeOut(pot), run_time=0.5)
        q = txt("Quem estabelece o campo?", T_BODY)
        q.move_to(P3(0, -0.45)).set_z_index(30)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=1.0)
        self.wait(3.5)
        self.play(FadeOut(q), run_time=0.6)

        self.next_section("B06_continuidade")
        rd0 = Dot(radius=0.1, color=WHITE).set_z_index(30)

        def rd0_upd(m):
            s_ = (self.clk.get_value() * 1.1) % LOOP.total
            p_, tg = LOOP.at(s_)
            m.move_to(p_ + np.array([tg[1], -tg[0], 0.0]) * (0.36 + 0.1 + 0.36 * (Vat(s_) + 1) / 2))

        rd0.add_updater(rd0_upd)
        self.add(rd0)
        self.pulse([self.E_arr, self.ribbon, self.E_arr], rt=1.4, scale=1.06)
        rd0.clear_updaters()
        self.remove(rd0)
        self.anchor("N026")
        self.set_dim(1.0, 1.0)
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
        self.play(Indicate(cv, color=WHITE, scale_factor=1.05), run_time=1.2)
        self.chips(0)
        self.play(FadeIn(self.chip_g), FadeIn(self.chip_ar), run_time=0.8)
        K0 = EQ(r"\frac{\partial\rho}{\partial t}+\nabla\cdot\mathbf J=0", r"\frac{\partial\rho}{\partial t}", r"\nabla\cdot", r"\mathbf J", size=M_M, width=COLW)
        K1 = EQ(r"\int_V\frac{\partial\rho}{\partial t}\,d\tau+\int_V\nabla\cdot\mathbf J\,d\tau=0", r"\frac{\partial\rho}{\partial t}", r"\nabla\cdot", r"\mathbf J", r"d\tau", size=M_S, width=COLW)
        K2 = EQ(r"\frac{d}{dt}\int_V\rho\,d\tau+\oint_S\mathbf J\cdot d\mathbf a=0", r"\rho", r"\mathbf J", r"d\tau", r"d\mathbf a", size=M_S, width=COLW)
        K3 = EQ(r"\frac{dQ}{dt}=I_{\rm entra}-I_{\rm sai}", r"\frac{dQ}{dt}", r"I_{\rm entra}", r"I_{\rm sai}", size=M_L, width=COLW)
        for k in (K0, K1, K2):
            k.move_to(P3(COL, 1.2)).set_z_index(30)
        K3.move_to(P3(COL, 0.0)).set_z_index(30)
        self.fill([self.bt(cv, "volume imaginário", BLUE_L, 2.1, UP), self.bt(face_l, r"I_{\rm entra}", GREEN, 1.7, LEFT, math=True)])
        self.anchor("N027")
        self.play(Write(K0), run_time=2.0)
        self.play(Indicate(glyphs(K0, r"\frac{\partial\rho}{\partial t}"), color=WHITE, scale_factor=1.3), run_time=1.5)
        self.play(Indicate(glyphs(K0, r"\nabla\cdot"), color=WHITE, scale_factor=1.3), Indicate(glyphs(K0, r"\mathbf J"), color=WHITE, scale_factor=1.3), run_time=1.5)
        self.wait(0.8)
        self.fill([self.bt(glyphs(K0, r"\frac{\partial\rho}{\partial t}"), "carga acumulando", BLUE_L, 2.4, DOWN),
                   self.bt(glyphs(K0, r"\mathbf J"), "saindo pelas faces", GREEN, 2.4, UP),
                   self.lk(K0, cv, BLUE_L, 2.4)])
        self.anchor("N028")
        self.play(cvbox.animate.set_fill(BLUE_L, 0.18), run_time=0.8)
        self.play(gmap(K0, K1, (r"\nabla\cdot", r"\nabla\cdot"), (r"\mathbf J", r"\mathbf J")), run_time=2.4)
        self.add(K1)
        self.wait(1.4)
        tdiv = txt("teorema da divergência", T_CAP, VIOLET).move_to(P3(COL, 0.55)).set_z_index(30)
        self.play(FadeIn(tdiv, shift=UP * 0.1), run_time=0.6)
        self.play(gmap(K1, K2, (r"\mathbf J", r"\mathbf J"), (r"d\tau", r"d\tau", 0, 0), (r"d\tau", None, 1),
                       (r"\nabla\cdot", None), (r"\frac{\partial\rho}{\partial t}", None)), run_time=2.6)
        self.add(K2)
        self.anchor("N029")
        self.play(face_l.animate.set_fill(GREEN, 0.55), face_r.animate.set_fill(GREEN, 0.55), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(K2), FadeOut(tdiv), FadeIn(K3, shift=UP * 0.1), run_time=1.6)
        kb = box(K3, WHITE)
        self.play(FadeIn(kb), run_time=0.6)
        self.wait(1.6)
        self.lab_in = MathTex(r"I_{\rm entra}", font_size=34, color=GREEN).move_to(P3(-5.4, cy - 1.5)).set_z_index(20)
        self.lab_out = MathTex(r"I_{\rm sai}", font_size=34, color=GREEN).move_to(P3(-1.4, cy - 1.5)).set_z_index(20)
        self.gl_cont = gloss_rows([gi(r"\rho", BLUE_L, "densidade de carga"), gi("Q", BLUE_L, "carga dentro do volume"), gi(r"I_{\rm entra},\,I_{\rm sai}", GREEN, "correntes pelas faces")], P3(4.2, -1.75))
        self.play(FadeIn(self.lab_in), FadeIn(self.lab_out), FadeIn(self.gl_cont), run_time=1.0)
        self.fill([self.pp([glyphs(K3, r"I_{\rm entra}"), self.lab_in], 1.6, GREEN), self.pp([glyphs(K3, r"I_{\rm sai}"), self.lab_out], 1.6, GREEN),
                   self.pp([glyphs(K3, r"\frac{dQ}{dt}"), cv], 1.6, BLUE_L)])
        self.K3, self.kb = K3, kb

    # ═══ cena prioritária: I_entra > I_sai → carga superficial → V(x) → E → J, em etapas ═════════════════
    def cargas_superficiais(self):
        self.next_section("B07_carga_E_J")
        self.anchor("N030")
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
        _it = [MathTex(r"\Delta I", font_size=44, color=GREEN), MathTex(r"\frac{dQ}{dt}", font_size=44, color=BLUE_L),
               MathTex(r"Q_s", font_size=44, color=BLUE_L), MathTex(r"V", font_size=44, color=CYAN),
               MathTex(r"E", font_size=44, color=CYAN), MathTex(r"J", font_size=44, color=GREEN)]
        dots = VGroup(*_it).arrange(RIGHT, buff=0.55).move_to(P3(COL, -0.15)).set_z_index(20)
        road_ar = VGroup(*[MathTex(r"\rightarrow", font_size=30, color=DIM).move_to((dots[i].get_right() + dots[i + 1].get_left()) / 2)
                           for i in range(5)]).set_z_index(20)

        def stage(i, cap_new, sub_text, run=0.8):
            cap_new.move_to(P3(COL, 1.25)).set_z_index(20)
            sub_new = NT()
            outs = [m for m in (st["cap"], st["sub"]) if m is not None]
            fills = [dd.animate.set_opacity(1.0 if j == i else 0.35) for j, dd in enumerate(dots)]
            self.play(*[FadeOut(m) for m in outs], FadeIn(cap_new, shift=UP * 0.1), FadeIn(sub_new, shift=UP * 0.1), *fills, run_time=run)
            st["cap"], st["sub"] = cap_new, sub_new

        self.play(FadeOut(self.K3), FadeOut(self.kb), run_time=0.8)
        dots.set_opacity(0.35)
        for k_ in range(6):
            self.play(FadeIn(dots[k_], shift=UP * 0.1), *([FadeIn(road_ar[k_ - 1])] if k_ else []), run_time=0.5)
            self.wait(0.15)
        self.wait(0.3)
        self.add(arr, prof, chs, gau)
        self.fill([self.sweep(list(dots), 0.45, WHITE, 1.3)])
        self.anchor("N031")
        # A — só I_entra > I_sai
        stage(0, M(r"I_{\rm entra}", ">", r"I_{\rm sai}", size=M_L, width=COLW), "entra mais corrente do que sai")
        self.play(opJ.animate.set_value(1), run_time=1.0)
        self.play(d.animate.set_value(1), run_time=2.8)
        self.wait(1.2)
        self.fill([self.pp([self.lab_in], 1.3, GREEN, 1.3), self.pp([self.lab_out], 1.3, GREEN, 1.3)])
        # B — dQ/dt > 0
        stage(1, M(r"\frac{dQ}{dt}", ">", "0", size=M_L, width=COLW), "a carga dentro do volume cresce")
        self.play(opG.animate.set_value(1), FadeIn(g_axis), FadeIn(g_lab), run_time=1.2)
        self.wait(1.4)
        self.anchor("N032")
        # C — acúmulo superficial
        self.chips(1)
        stage(2, txt("acúmulo na superfície", T_HEAD), "só na casca do condutor, não no volume")
        self.play(s.animate.set_value(1), run_time=4.0, rate_func=linear)
        self.wait(1.2)
        self.fill([self.bt(chs, "cargas na superfície", BLUE_L, 2.6, UP, indicate=False)])
        self.anchor("N033")
        # D — o potencial local se deforma
        stage(3, MathTex("V(x)", font_size=60, color=CYAN), "V(x) muda junto do acúmulo")
        self.play(opV.animate.set_value(1), FadeIn(v_lab), run_time=1.0)
        self.play(sV.animate.set_value(1), run_time=4.0, rate_func=linear)
        self.wait(1.2)
        self.fill([self.bt(pt(-3.4, 2.1), "curva do potencial", CYAN, 2.6, UP, indicate=False)])
        # E — o campo muda porque a inclinação de V muda
        stage(4, M("E_x", "=", r"-\frac{dV}{dx}", size=M_L, width=COLW), "E muda onde a inclinação de V muda")
        self.play(opE.animate.set_value(1), run_time=1.0)
        self.play(sE.animate.set_value(1), run_time=4.0, rate_func=linear)
        self.wait(1.2)
        self.anchor("N034")
        # F — J acompanha E
        stage(5, M(r"\mathbf J", "=", r"\sigma", r"\mathbf E", size=M_L, width=COLW), "J acompanha E")
        self.play(sJ.animate.set_value(1), run_time=4.0, rate_func=linear)
        self.wait(1.0)
        self.fill([self.bt(g_lab, "acúmulo cai", BLUE_L, 2.6, LEFT, indicate=False, size=22)])
        self.pulse([arr, prof, arr], rt=1.2, scale=1.05)
        self.anchor("N035")
        self.chips(2)
        stage(5, M(r"I_{\rm entra}", "=", r"I_{\rm sai}", size=M_L, width=COLW), "a acumulação para; a carga permanece")
        self.play(FadeOut(self.gl_cont), run_time=0.6)
        ring_c = P3(COL, -1.45)
        names = [MathTex(r"Q_s", font_size=36, color=BLUE_L), MathTex(r"E", font_size=36, color=CYAN),
                 MathTex(r"J", font_size=36, color=GREEN), MathTex(r"\Delta I", font_size=36, color=GREEN)]
        pos_ = [ring_c + P3(-1.3, 0.45), ring_c + P3(0.0, 0.8), ring_c + P3(1.3, 0.45), ring_c + P3(0.0, -0.1)]
        ring = VGroup(*[n_.move_to(p_) for n_, p_ in zip(names, pos_)]).set_z_index(30)
        rarr = VGroup(*[arrow(pos_[i] + (pos_[(i + 1) % 4] - pos_[i]) * 0.3, pos_[i] + (pos_[(i + 1) % 4] - pos_[i]) * 0.7, DIM, 3, 30, 0.14)
                        for i in range(4)])
        self.play(FadeIn(ring), FadeIn(rarr), run_time=1.0)
        for amp_ in (1.0, 0.6, 0.3, 0.0):
            for n_ in names:
                self.play(Indicate(n_, color=WHITE, scale_factor=1.0 + 0.4 * max(amp_, 0.2)), run_time=0.5)
            self.play(names[3].animate.set_opacity(max(amp_ - 0.3, 0.1)), run_time=0.3)
        self.wait(0.6)
        self.play(FadeOut(VGroup(ring, rarr)), run_time=0.6)
        for m in (arr, prof, gau):
            m.clear_updaters()
        chs.clear_updaters()
        extras = VGroup(st["cap"], st["sub"], dots, road_ar, self.lab_in, self.lab_out, g_axis, g_lab, v_lab)

        # ── do caso local para uma distribuição global já estabelecida ──
        self.next_section("B07b_distribuicao_global")
        self.anchor("N036")
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
        self.sprites = sprites
        self.play(FadeIn(sprites, scale=0.5), run_time=0.8)
        steps = [NT(), NT(),
                 NT()]
        for i, tt in enumerate(steps):
            tt.move_to(P3(0, 0.55 - 0.55 * i)).set_z_index(30)
        self.play(FadeIn(steps[0], shift=UP * 0.1), run_time=1.0)
        self.wait(2.0)
        self.play(FadeIn(steps[1], shift=UP * 0.1), run_time=1.0)
        self.wait(2.0)
        self.fill([self.bt(spot, "o trecho que estudamos", BLUE_L, 2.8, DOWN), self.pp([sprites], 1.8, WHITE, 1.3),
                   self.pp([self.layer], 2.0, BLUE_L, 1.02)])
        self.anchor("N037")
        self.play(FadeOut(spot), FadeOut(self.E_arr), run_time=0.6)
        self.E_arr = loop_arrows("E")
        self.play(FadeIn(steps[2], shift=UP * 0.1), FadeIn(self.E_arr), FadeIn(self.J_arr), run_time=1.8)
        self.add_shimmer(self.J_arr, j_phases())
        jse = M(r"\mathbf J", "=", r"\sigma", r"\mathbf E", size=M_S).move_to(P3(0, -1.2)).set_z_index(30)
        self.play(FadeIn(jse, shift=UP * 0.1), run_time=0.8)
        self.wait(3.0)
        self.play(FadeOut(steps[0]), FadeOut(steps[1]), FadeOut(steps[2]), FadeOut(jse), run_time=0.8)
        self.hide_circ(0.6)
        self.set_dim(1.0, 0.8)
        ys = -0.1
        sections = [(-4.2, 0.9), (-1.0, 0.45), (2.2, 0.9)]            # (x inicial, altura): fio, resistor, fio
        cyls = VGroup(*[pipe(x_, ys - h_ / 2, x_ + 2.4, ys + h_ / 2, True, 15) for x_, h_ in sections])
        for c_ in cyls:
            for mm_ in c_:
                mm_.set_z_index(15)
        self.play(FadeIn(cyls), run_time=1.2)
        i_arrs = VGroup(*[halo(arrow(P3(x_ - 0.1, ys + 0.85), P3(x_ + 2.5, ys + 0.85), GREEN, 8, 30, 0.26)) for x_, _ in sections])
        i_lab = MathTex("I", font_size=40, color=GREEN).move_to(P3(-4.6, ys + 0.85)).set_z_index(30)
        self.play(FadeIn(i_arrs), FadeIn(i_lab), run_time=1.2)
        self.wait(0.8)
        j_grp = VGroup()
        for (x_, h_), n_ in zip(sections, (2, 4, 2)):
            for k_ in range(n_):
                y_ = ys - h_ / 2 + (k_ + 0.5) * h_ / n_
                j_grp.add(halo(arrow(P3(x_ + 0.4, y_), P3(x_ + 2.0, y_), GREEN, 3, 30, 0.14), 4))
        j_lab = MathTex(r"J", font_size=40, color=GREEN).move_to(P3(-4.6, ys)).set_z_index(30)
        self.play(FadeIn(j_grp, lag_ratio=0.1), FadeIn(j_lab), run_time=1.6)
        self.wait(0.8)
        e_grp = VGroup()
        for (x_, h_), L_ in zip(sections, (0.55, 1.2, 0.55)):
            e_grp.add(halo(arrow(P3(x_ + 1.2 - L_ / 2, ys - h_ / 2 - 0.45), P3(x_ + 1.2 + L_ / 2, ys - h_ / 2 - 0.45), CYAN, 6, 30, 0.2)))
        e_lab = MathTex("E", font_size=40, color=CYAN).move_to(P3(-4.6, ys - 0.9)).set_z_index(30)
        self.play(FadeIn(e_grp), FadeIn(e_lab), run_time=1.4)
        eqs = M(r"E", "=", r"\frac{I}{\sigma A}", size=M_L).move_to(P3(0, 1.45)).set_z_index(30)
        self.play(Write(eqs), run_time=1.4)
        self.wait(1.6)
        self.pulse([i_arrs, j_grp, e_grp, eqs], rt=1.2, scale=1.1, rounds=1)
        self.play(FadeOut(VGroup(cyls, i_arrs, i_lab, j_grp, j_lab, e_grp, e_lab, eqs)), run_time=0.8)
        self.set_dim(0.0, 0.8)
        self.show_circ(0.8)
        self.anchor("N038")
        # a fita de potencial reúne as ideias: fio (queda pequena), resistor (queda grande), fonte (sobe)
        self.ribbon = ribbon()
        rib_notes = [NT().move_to(P3(-1.8, 0.0)), NT().move_to(P3(2.0, -0.5)),
                     NT().move_to(P3(-2.6, -0.95))]
        for rn in rib_notes:
            rn.set_z_index(30)
        self.play(FadeIn(self.ribbon), run_time=1.4)
        rdot = Dot(radius=0.1, color=WHITE).set_z_index(30)

        def rdot_upd(m):
            s_ = (self.clk.get_value() * 1.1) % LOOP.total
            p_, tg = LOOP.at(s_)
            m.move_to(p_ + np.array([tg[1], -tg[0], 0.0]) * (0.36 + 0.1 + 0.36 * (Vat(s_) + 1) / 2))

        rdot.add_updater(rdot_upd)
        self.add(rdot)
        for rn in rib_notes:
            self.play(FadeIn(rn, shift=UP * 0.1), run_time=0.8)
            self.wait(1.4)
        efd = rich("$E_t=-\\frac{dV}{ds}$", T_NOTE, CYAN).move_to(P3(2.9, 0.1)).set_z_index(30)
        self.play(FadeIn(efd), run_time=0.8)
        self.wait(2.0)
        rdot.clear_updaters()
        self.play(FadeOut(VGroup(self.ribbon, efd, rdot, *rib_notes)), run_time=1.0)
        self.sprites = sprites

    # ═══ 6b. REGIME ESTACIONÁRIO ═══════════════════════════════════════════════════════════════════════════
    def regime_estacionario(self):
        self.next_section("B08_estacionario")
        self.anchor("N039")
        self.chips(1)
        tr = M(r"\frac{\partial\rho}{\partial t}", r"\neq", "0", size=M_L).move_to(P3(0, 0.55)).set_z_index(30)
        self.play(FadeIn(tr, shift=UP * 0.1), run_time=1.0)
        self.play(Indicate(self.layer, color=WHITE, scale_factor=1.0, rate_func=there_and_back), run_time=2.0)
        gx0, gy0 = -1.6, -1.35
        gax = VGroup(Line(P3(gx0, gy0), P3(gx0 + 3.6, gy0), stroke_width=2, color=DIM), Line(P3(gx0, gy0), P3(gx0, gy0 + 0.95), stroke_width=2, color=DIM)).set_z_index(30)
        curve = VMobject().set_points_as_corners([P3(gx0 + 3.6 * t_, gy0 + 0.9 * float(np.exp(-4.0 * t_))) for t_ in np.linspace(0, 1, 40)])
        curve.set_stroke(BLUE_L, 4).set_z_index(30)
        gdot = Dot(radius=0.07, color=WHITE).move_to(curve.get_start()).set_z_index(31)
        self.play(FadeIn(gax), run_time=0.6)
        self.play(Create(curve), MoveAlongPath(gdot, curve), run_time=2.6, rate_func=linear)
        self.play(FadeOut(VGroup(gax, curve, gdot)), run_time=0.6)
        self.chips(2)
        st1 = M(r"\frac{\partial\rho}{\partial t}", "=", "0", size=M_L).move_to(P3(-2.35, 0.2)).set_z_index(30)
        st2 = M(r"\nabla\cdot\mathbf J", "=", "0", size=M_L).move_to(P3(2.35, 0.2)).set_z_index(30)
        self.play(ReplacementTransform(tr, st1), run_time=1.2)
        self.play(FadeIn(st2, shift=UP * 0.1), run_time=1.0)
        b2 = box(st2)
        self.play(FadeIn(b2), run_time=0.6)
        self.anchor("N040")
        self.play(Indicate(self.layer, color=WHITE, scale_factor=1.0, rate_func=there_and_back), run_time=2.0)
        self.play(Indicate(self.layer, color=WHITE, scale_factor=1.0, rate_func=there_and_back), run_time=2.0)
        self.play(Indicate(self.layer, color=WHITE, scale_factor=1.0, rate_func=there_and_back), run_time=2.0)
        self.fill([self.bt(pt(0.0, -0.9), "a carga de superfície continua lá", BLUE_L, 2.8, DOWN, indicate=False)])
        self.play(FadeOut(VGroup(st1, st2, b2)), run_time=0.8)
        self.anchor("N041")
        self.hide_circ(0.6)
        self.set_dim(1.0, 0.8)
        pa = panel(4.5, 2.5, P3(-2.6, -0.05))
        pb = panel(4.5, 2.5, P3(2.6, -0.05))
        ta = txt("equilíbrio eletrostático", T_CAP, DIM).move_to(P3(-2.6, 0.85)).set_z_index(30)
        tb = txt("corrente estacionária", T_CAP, GREEN).move_to(P3(2.6, 0.85)).set_z_index(30)
        ea = M(r"\mathbf E", "=", "0", size=M_L).move_to(P3(-2.6, -0.1)).set_z_index(30)
        eb1 = M(r"\mathbf E", r"\neq", "0", size=M_L).move_to(P3(2.6, 0.2)).set_z_index(30)
        eb2 = M(r"\mathbf J", "=", r"\sigma", r"\mathbf E", size=M_M).move_to(P3(2.6, -0.5)).set_z_index(30)
        self.play(FadeIn(pa), FadeIn(pb), FadeIn(ta), FadeIn(tb), run_time=1.0)
        self.play(FadeIn(ea, shift=UP * 0.1), run_time=1.0)
        self.wait(1.6)
        self.play(FadeIn(eb1, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(eb2, shift=UP * 0.1), run_time=1.0)
        bb = box(eb1, GREEN)
        self.play(FadeIn(bb), run_time=0.6)
        self.wait(2.4)
        self.pulse([ea, eb1, eb2, ea, eb1], rt=1.2, scale=1.12)
        self.play(FadeOut(VGroup(pa, pb, ta, tb, ea, eb1, eb2, bb)), run_time=0.8)
        self.set_dim(0.0, 0.8)
        self.show_circ(0.8)

    # ═══ 7-8. QUEM REPÕE A ENERGIA? — FONTE E FEM ═════════════════════════════════════════════════════════
    def make_circ(self):
        """Marcador que percorre o circuito + barras que acumulam ∮E·dℓ e ∮f_s·dℓ (o cálculo da circulação, em movimento)."""
        u = ValueTracker(0)

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
            s_ = u.get_value() * LOOP.total
            return 0.0 if s_ < S["b0"] else min(1.0, (s_ - S["b0"]) / (LOOP.total - S["b0"]))

        BL = 3.4
        bE = always_redraw(lambda: Rectangle(width=max(0.001, BL * cE()), height=0.22).set_fill(CYAN, 0.9).set_stroke(width=0)
                           .move_to(P3(-0.6 + max(0.001, BL * cE()) / 2, -0.55)).set_z_index(30))
        bF = always_redraw(lambda: Rectangle(width=max(0.001, BL * cF()), height=0.22).set_fill(FC, 0.9).set_stroke(width=0)
                           .move_to(P3(-0.6 + max(0.001, BL * cF()) / 2, -1.3)).set_z_index(30))
        lE = MathTex(r"\oint\mathbf E\cdot d\boldsymbol\ell", font_size=30, color=CYAN).move_to(P3(-2.2, -0.55)).set_z_index(30)
        lF = MathTex(r"\oint\mathbf f_s\cdot d\boldsymbol\ell", font_size=30, color=FC).move_to(P3(-2.2, -1.3)).set_z_index(30)
        return u, mk, tr, bE, bF, lE, lF

    def fonte_e_fem(self):
        self.next_section("B09_fonte")
        self.anchor("N042")
        self.play(FadeOut(self.chip_g), FadeOut(self.chip_ar), run_time=0.5)
        glow = self.res_glow()
        self.add(glow)
        self.wait(2.6)
        glow.clear_updaters()
        self.play(FadeOut(glow), run_time=0.3)
        # ── N043: o campo conservativo, sozinho, devolve tudo numa volta completa ──
        self.anchor("N043")
        self.set_dim(0.6, 1.0)
        u0, mk0, tr0, bE0, bF0, lE0, lF0 = self.make_circ()
        self.add(mk0, tr0, bE0)
        self.play(FadeIn(lE0), run_time=0.6)
        self.play(u0.animate.set_value(1.0), run_time=6.0, rate_func=linear)
        self.wait(1.5)
        for m in (mk0, tr0, bE0):
            m.clear_updaters()
        self.play(FadeOut(VGroup(mk0, tr0, bE0, lE0)), run_time=0.8)
        self.remove(mk0, tr0, bE0)
        # ── N044: dentro da fonte, E e a força não eletrostática ──
        self.anchor("N044")
        self.hide_circ(0.6)
        self.set_dim(1.0, 1.0)
        self.mm, self.mm_ring, self.mm_t = self.make_minimap()
        self.play(FadeIn(self.mm), FadeIn(self.mm_ring), run_time=0.6)
        q = NT()
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
        self.add_shimmer(Ea, [0.0, 0.5])
        self.add_shimmer(Fs, [0.25, 0.75])
        n1 = NT().move_to(P3(COL, 1.1)).set_z_index(30)
        n2 = gloss_line([gi(r"\mathbf f_s", FC, "força não eletrostática, por unidade de carga")])
        self.play(FadeIn(n2, shift=UP * 0.1), run_time=0.8)
        # ── N045: os dois coexistem; a força total é a soma ──
        self.anchor("N045")
        feq = M(r"\mathbf f", "=", r"\mathbf E", "+", r"\mathbf f_s", size=M_L, width=COLW).move_to(P3(COL, -0.65)).set_z_index(30)
        self.play(Write(feq), run_time=1.6)
        fb_ = box(feq)
        self.play(FadeIn(fb_), run_time=0.6)
        self.wait(2.0)
        self.fill([self.pp([feq[2], Ea, Ea_l], 1.7, CYAN), self.pp([feq[4], Fs, Fs_l], 1.7, FC), self.pp([feq[0], feq[2], feq[4]], 1.6, WHITE)])
        # ── N046: uma carga de prova positiva sobe; a régua de energia por carga cresce ──
        p0 = P3(COL - 1.6, 1.0)
        v_e = halo(arrow(p0, p0 + DOWN * 0.9, CYAN, 6, 30, 0.22))
        v_f = halo(arrow(p0, p0 + UP * 1.5, FC, 8, 30, 0.28))
        v_n = halo(arrow(p0 + RIGHT * 0.7, p0 + RIGHT * 0.7 + UP * 0.6, WHITE, 8, 30, 0.26))
        l_e = MathTex(r"\mathbf E", font_size=34, color=CYAN).move_to(p0 + P3(-0.45, -0.5)).set_z_index(30)
        l_f = MathTex(r"\mathbf f_s", font_size=34, color=FC).move_to(p0 + P3(-0.5, 0.9)).set_z_index(30)
        l_n = MathTex(r"\mathbf f", font_size=34, color=WHITE).move_to(p0 + P3(1.2, 0.3)).set_z_index(30)
        self.play(FadeIn(v_e), FadeIn(l_e), run_time=0.8)
        self.play(FadeIn(v_f), FadeIn(l_f), run_time=0.9)
        self.play(FadeIn(v_n), FadeIn(l_n), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(VGroup(v_e, v_f, v_n, l_e, l_f, l_n)), run_time=0.6)
        self.anchor("N046")
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
        self.wait(4.0)
        for m in (cu, car, bar):
            m.clear_updaters()
        self.remove(cu)
        Ea.clear_updaters()
        Fs.clear_updaters()
        self.src_fig = VGroup(shell, cps, Ea, Ea_l, Fs, Fs_l, car, rule, bar, rule_l, n1, n2, q)
        self.play(FadeOut(self.src_fig), FadeOut(feq), FadeOut(fb_), run_time=1.0)

        # ── FEM: o marcador realmente calcula a circulação ──
        self.next_section("B10_fem")
        self.anchor("N047")
        self.set_dim(1.0, 1.0)
        u, mk, tr, bE, bF, lE, lF = self.make_circ()
        d1 = M(r"\mathcal E", "=", r"\oint", r"\mathbf f", r"\cdot d\boldsymbol\ell", size=M_L).move_to(P3(0, 0.7)).set_z_index(30)
        self.gl_fem = gloss_line([gi(r"\mathcal E", CYAN, "força eletromotriz (fem)"), gi(r"\mathbf f_s", FC, "força não eletrostática por unidade de carga")])
        un = MathTex(r"[\mathcal E]=\frac{\rm N}{\rm C}\,{\rm m}=\frac{\rm J}{\rm C}={\rm V}", font_size=36, color=CYAN).move_to(P3(0, 2.0)).set_z_index(30)
        self.play(FadeIn(self.gl_fem), Write(d1), run_time=1.6)
        self.sweep([d1[0], d1[2], d1[3], d1[4]], 0.4, CYAN, 1.25)[1]()
        self.play(FadeIn(un, shift=UP * 0.1), run_time=1.0)
        self.sweep([un, d1[0], un, d1[3]], 0.8, CYAN, 1.1)[1]()
        self.play(FadeOut(un), run_time=0.6)
        # N048: a força por carga se separa em campo + força da fonte
        self.pulse([d1[0], d1[2], d1[3], d1[4]], rt=1.2, scale=1.15)
        self.anchor("N048")
        d2 = EQ(r"\mathcal E=\oint\mathbf E\cdot d\boldsymbol\ell+\oint\mathbf f_s\cdot d\boldsymbol\ell", r"\mathcal E", r"\oint", r"\mathbf E",
                r"\mathbf f_s", r"\cdot d\boldsymbol\ell", size=M_M, width=9.0).move_to(P3(0, 0.7)).set_z_index(30)
        d2z = EQ(r"\mathcal E=0+\oint\mathbf f_s\cdot d\boldsymbol\ell", r"\mathcal E", "0", r"\oint", r"\mathbf f_s", r"\cdot d\boldsymbol\ell",
                 size=M_M, width=9.0).move_to(P3(0, 0.7)).set_z_index(30)
        d3 = EQ(r"\mathcal E=\oint\mathbf f_s\cdot d\boldsymbol\ell", r"\mathcal E", r"\oint", r"\mathbf f_s", r"\cdot d\boldsymbol\ell",
                size=M_L, width=9.0).move_to(P3(0, 0.7)).set_z_index(30)
        self.play(FadeOut(d1), FadeIn(d2), run_time=1.6)
        self.sweep([glyphs(d2, r"\mathbf E"), glyphs(d2, r"\mathbf f_s"), glyphs(d2, r"\mathcal E", 0)], 0.67, WHITE, 1.25)[1]()
        self.fill([self.pp([glyphs(d2, r"\mathbf E")], 1.4, CYAN), self.pp([glyphs(d2, r"\mathbf f_s")], 1.4, FC), self.pp([d2], 1.4, WHITE, 1.1)])
        # N049: o campo é conservativo; o marcador percorre o circuito e as barras mostram o que cada termo acumula
        self.anchor("N049")
        self.set_dim(0.6, 0.8)
        self.add(mk, tr, bE, bF)
        self.play(FadeIn(lE), FadeIn(lF), run_time=0.8)
        self.play(u.animate.set_value(1.0), run_time=12, rate_func=linear)
        for m in (mk, tr, bE, bF):
            m.clear_updaters()
        self.remove(mk, tr)
        e0 = MathTex(r"\oint\mathbf E\cdot d\boldsymbol\ell=0", font_size=30, color=CYAN).move_to(P3(-2.6, -0.55)).set_z_index(30)
        self.play(ReplacementTransform(lE, e0), run_time=1.2)
        cb = box(e0, CYAN)
        self.play(FadeIn(cb), run_time=0.6)
        self.wait(2.0)
        self.fill([self.pp([e0], 1.4, CYAN, 1.25), self.pp([lF], 1.4, FC, 1.25)])
        # N050: o termo do campo cancela; sobra só a força da fonte
        self.set_dim(1.0, 0.6)
        self.anchor("N050")
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
        self.pulse([d3, fb3, d3], rt=1.2, scale=1.08)
        self.d3, self.fb3 = d3, fb3
        self.fem_bits = VGroup(bE, bF, lF, e0, cb)

    # ═══ 9-10. ENERGIA E PAYOFF ══════════════════════════════════════════════════════════════════════════
    def energia_e_payoff(self):
        self.next_section("B11_energia")
        self.anchor("N051")
        self.play(FadeOut(self.fem_bits), self.d3.animate.scale(0.5).move_to(P3(COL + 0.8, 2.3)).set_opacity(0.6), FadeOut(self.fb3), run_time=1.0)
        self.set_dim(1.0, 0.6)
        self.play(self.mm_t[0].animate.set_value(float(self.mm_pos['res'][0])), self.mm_t[1].animate.set_value(float(self.mm_pos['res'][1])), run_time=0.8)
        self.rg = self.res_glow()
        Q0 = EQ(r"p=\mathbf J\cdot\mathbf E", "p", r"\mathbf J", r"\mathbf E", size=M_L)
        Q1 = EQ(r"P=\int p\,d\tau=\int\mathbf J\cdot\mathbf E\,d\tau", "P", "p", r"\mathbf J", r"\mathbf E", size=M_M, width=8.6)
        Q2 = EQ(r"P=JE\,AL", "P", "J", "E", "A", "L", size=M_L)
        Q3 = EQ(r"P=(JA)(EL)", "P", "J", "E", "A", "L", size=M_L)
        Q4 = EQ(r"P=VI", "P", "V", "I", size=M_L)
        Q5 = EQ(r"P=I^2R", "P", "I", size=M_L)
        for q in (Q0, Q1, Q2, Q3, Q4, Q5):
            q.scale(1.25).move_to(P3(0, 0.55)).set_z_index(30)
        pv = NT().move_to(P3(0, -0.55)).set_z_index(30)
        self.gl_en = gloss_line([gi("p", CYAN, "potência por volume"), gi("P", CYAN, "potência total"), gi("R", WHITE, "resistência total do modelo ideal")])
        self.play(FadeOut(self.gl_fem), run_time=0.4)
        self.play(Write(Q0), FadeIn(pv), FadeIn(self.gl_en), run_time=1.6)
        self.wait(1.5)
        self.fill([self.bt(glyphs(Q0, "p"), "potência por volume", CYAN, 2.6, UP), self.pp([glyphs(Q0, r"\mathbf J"), glyphs(Q0, r"\mathbf E")], 1.6, CYAN, 1.2), self.pp([Q0], 1.6, WHITE, 1.1)])
        self.anchor("N052")
        self.play(FadeOut(pv), gmap(Q0, Q1, ("p", "p"), (r"\mathbf J", r"\mathbf J"), (r"\mathbf E", r"\mathbf E")), run_time=2.4)
        self.add(Q1)
        pt = NT().move_to(P3(0, -0.55)).set_z_index(30)
        self.play(FadeIn(pt), run_time=0.6)
        self.sweep([glyphs(Q1, "P"), glyphs(Q1, "p"), glyphs(Q1, r"\mathbf J")], 0.4, CYAN, 1.2)[1]()
        self.play(FadeOut(pt), gmap(Q1, Q2, (r"\mathbf J", "J"), (r"\mathbf E", "E"), ("p", None)), run_time=2.4)
        self.add(Q2)
        un = NT().move_to(P3(0, -0.55)).set_z_index(30)
        self.play(FadeIn(un), run_time=0.6)
        self.sweep([glyphs(Q2, "J"), glyphs(Q2, "E"), glyphs(Q2, "A"), glyphs(Q2, "L")], 0.35, CYAN, 1.2)[1]()
        self.fill([self.pp([glyphs(Q2, "J"), glyphs(Q2, "E")], 1.6, CYAN, 1.2), self.bt(Q2, "soma em todo o volume", CYAN, 2.6, DOWN)])
        self.anchor("N053")
        self.play(FadeOut(un), gmap(Q2, Q3), run_time=2.0)
        self.add(Q3)
        self.wait(0.3)
        ji = rich(r"$JA=I,\qquad EL=V$", T_NOTE).move_to(P3(0, -0.85)).set_z_index(30)
        self.play(FadeIn(ji, shift=UP * 0.1), run_time=0.8)
        self.wait(0.3)
        self.play(gmap(Q3, Q4, ([("J", 0), ("A", 0)], "I"), ([("E", 0), ("L", 0)], "V")), run_time=2.6)
        self.add(Q4)
        bq = box(Q4, CYAN)
        self.play(FadeIn(bq), run_time=0.6)
        self.wait(0.6)
        self.play(FadeOut(bq), FadeOut(ji), run_time=0.5)
        vir = M("V", "=", "I", "R", size=M_M).move_to(P3(0, -0.85)).set_z_index(30)
        self.play(FadeIn(vir, shift=UP * 0.1), run_time=0.8)
        self.play(gmap(Q4, Q5, ("I", "I"), ("V", None)), run_time=2.2)
        self.add(Q5)
        bq5 = box(Q5, CYAN)
        self.play(FadeIn(bq5), run_time=0.6)
        self.wait(1.0)
        self.play(FadeOut(Q5), FadeOut(bq5), FadeOut(vir), run_time=0.8)
        self.anchor("N054")
        self.play(self.mm_t[0].animate.set_value(float(self.mm_pos['bat'][0])), self.mm_t[1].animate.set_value(float(self.mm_pos['bat'][1])), run_time=0.8)
        pf = M(r"P_{\rm fonte}", "=", r"\mathcal E", "I", size=M_L).move_to(P3(0, 0.45)).set_z_index(30)
        eir = M(r"\mathcal E", "=", "I", "R", size=M_M).move_to(P3(0, -0.4)).set_z_index(30)
        self.play(Write(pf), run_time=1.4)
        self.sweep([pf[0], pf[2], pf[3]], 0.4, CYAN, 1.2)[1]()
        self.play(FadeIn(eir, shift=UP * 0.1), run_time=1.0)
        rn = NT().move_to(P3(0, -1.0)).set_z_index(30)
        self.play(FadeIn(rn), run_time=0.8)
        self.sweep([pf[2], eir[0], eir[2], eir[3], pf[3]], 0.5, CYAN, 1.2)[1]()
        self.play(FadeOut(pf), FadeOut(eir), FadeOut(rn), run_time=0.8)
        fin = M(r"P_{\rm fonte}", "=", r"\mathcal E", "I", "=", "I^2", "R", "=", r"P_{\rm dissipada}", size=M_M, width=9.6).move_to(P3(0, 0.5)).set_z_index(30)
        self.play(Write(fin), run_time=2.4)
        fbx = box(fin, WHITE, 0.2)
        self.play(FadeIn(fbx), run_time=0.6)
        t_in = MathTex(r"P_{\rm fonte}", font_size=30, color=CYAN).set_z_index(30)
        t_out = MathTex(r"P_{\rm dissipada}", font_size=30, color=CYAN).set_z_index(30)
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
        self.pulse([g_in, g_out, fin, g_in, g_out], rt=1.1, scale=1.08)
        self.play(FadeOut(VGroup(fin, fbx, t_in, t_out, g_in, g_out, self.d3, self.gl_en)), run_time=1.0)

        # ── payoff: o próprio circuito é a síntese; holofote camada a camada ──
        self.next_section("B12_payoff")
        self.anchor("N055")
        self.rg.clear_updaters()
        self.remove(self.rg)
        self.mm[3].clear_updaters()
        self.mm_ring.clear_updaters()
        self.play(FadeOut(self.mm), FadeOut(self.mm_ring), run_time=0.5)
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
        self.pulse([self.layer, self.E_arr, self.J_arr], rt=0.4, scale=1.05)
        self.anchor("N056")
        self.play(FadeIn(fs_a, shift=UP * 0.15), FadeIn(fs_l), FadeIn(fs_ring, scale=1.3), run_time=1.6)
        self.wait(2.0)
        self.play(FadeOut(fs_ring), run_time=0.5)
        lab_q = NT().move_to(P3(-2.6, 2.3)).set_z_index(30)
        self.play(FadeIn(self.layer), FadeIn(self.sprites), FadeIn(lab_q, shift=UP * 0.1), run_time=2.0)
        self.wait(2.4)
        lab_E = MathTex(r"\mathbf E", font_size=44, color=CYAN).move_to(P3(3.9, 0.35)).set_z_index(30)
        self.play(FadeIn(self.E_arr), FadeIn(lab_E), run_time=1.4)
        self.wait(2.4)
        lab_J = MathTex(r"\mathbf J", font_size=44, color=GREEN).move_to(P3(3.9, -0.45)).set_z_index(30)
        self.play(FadeIn(self.J_arr), FadeIn(lab_J), run_time=1.4)
        self.add_shimmer(self.J_arr, j_phases())
        self.wait(2.0)
        self.anchor("N057")
        cards = []
        specs = [(txt("bateria", 26), None, MathTex(r"\mathbf J", font_size=48, color=GREEN)),
                 (MathTex(r"\nabla\cdot\mathbf J=0", font_size=44, color=GREEN), None, MathTex(r"\mathbf E", font_size=48, color=CYAN)),
                 (txt("cargas superficiais", 24), None, txt("energia", 26)),
                 (MathTex(r"\mathcal E", font_size=52, color=CYAN), None, txt("força", 26))]
        grid_ = [P3(-3.7, 0.7), P3(3.7, 0.7), P3(-3.7, -1.1), P3(3.7, -1.1)]
        for (a_, _, b_), g_ in zip(specs, grid_):
            pn_ = panel(6.9, 1.4, g_, op=0.92, z=20)
            rel_ = MathTex(r"\nRightarrow", font_size=48, color=WHITE)
            row_ = VGroup(a_, rel_, b_).arrange(RIGHT, buff=0.5).move_to(g_).set_z_index(30)
            cards.append(VGroup(pn_, row_))
        self.J_arr.clear_updaters()
        self.play(FadeOut(VGroup(self.layer, self.E_arr, self.J_arr, self.sprites, fs_a, fs_l, lab_E, lab_J)),
                  self.dim.animate.set_fill(BACKGROUND_COLOR, 1.0), run_time=0.6)
        # cada cartão entra quando a fala chega nele (sub-âncoras N057a–d); a folga de cada um vira destaques nos próprios termos
        for k_, cd_ in enumerate(cards):
            self.anchor("N057" + "abcd"[k_])
            self.play(FadeIn(cd_, shift=UP * 0.15), run_time=0.8)
            self.play(Indicate(cd_[1][1], color=WHITE, scale_factor=1.3), run_time=0.6)
            self.fill([self.pp([cd_[1][0]], 1.2, WHITE, 1.12), self.pp([cd_[1][2]], 1.2, WHITE, 1.12), self.pp([cd_[1][1]], 1.0, WHITE, 1.3)])
        self.play(FadeOut(VGroup(*cards)), run_time=0.8)
