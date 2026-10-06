"""Por que o eixo muda o momento de inércia: preview visual silencioso (V3).

POR TRÁS DA FÓRMULA · EP. 05.

Arco: gancho (mesma barra, eixo do centro à ponta, I: 1× → 4×) -> v = ωr_⊥ (um dm que se afasta) ->
dK = ½v²dm -> ½(ωr_⊥)²dm -> ½ω²r_⊥²dm -> 1:4:9 -> soma discreta (6, 12, 24, 48 pedaços) -> ∫ -> I = ∫r_⊥²dm
-> r_⊥ = |x| -> barra uniforme (dm = (M/L)dx, perfil x²dm) -> I_CM = ML²/12 -> eixo desliza por d (CM fixo)
-> x = x' + d -> x' = x − d -> ∫(x−d)²dm se abre em três termos -> d constante sai da integral -> I_CM e M
-> ∫x dm = M x_CM = 0 -> I' = I_CM + Md² -> eixo na ponta (1/12 + 3/12) -> I_ponta = 4 I_CM -> síntese -> CTA.

Uma única barra (L = 5,2, fina, rígida, homogênea) é o personagem contínuo. O CM fica fixo na barra (×); só o
eixo (⊙, perpendicular ao plano) se desloca. Estado de movimento em trackers:
  `th`  ângulo da barra (rotação rígida em torno do eixo);   `om`  velocidade angular (setas v = ωr leem daqui);
  `axx` posição do eixo medida a partir do CM (= d).
`ATE=k` renderiza só até o bloco k (iteração); sem a variável, roda tudo. `seg(o0, o1, n0, n1)` remapeia os
marcos de tempo escritos em um bloco; os demais blocos usam tempos absolutos.

Cores: ciano = I_CM / x² / eixo; violeta = Md² / d; magenta = termo cruzado; azul = barra; branco = texto.
"""

import os
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, ORIGIN, PI, RIGHT, UP,
    Arc, Arrow, Brace, Circle, Create, GrowFromCenter, DashedLine, Dot, FadeIn, FadeOut, Indicate, Line, MathTex, Rectangle,
    ReplacementTransform, Scene, SurroundingRectangle, Transform, TransformFromCopy, TransformMatchingTex,
    VGroup, VMobject, ValueTracker, Write, AnimationGroup, LaggedStart, ImageMobject, config, always_redraw,
    smooth, linear,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from MF_Tools import TransformByGlyphMap
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

ICON_PATH = Path(__file__).resolve().parents[2] / "assets" / "branding" / "master" / "parallax_lab_icon_transparent.png"

ATE = int(os.environ.get("ATE", "99"))

# ── Paleta ──────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR
BLUE = "#267BFF"
BLUE_L = "#7FB2FF"
VIOLET = "#9C8CFF"       # #745CFF da marca clareado para contraste das equações
MAGENTA = "#EA63FF"

# ── Geometria da barra ──────────────────────────────────────────────────────
L = 5.2
HALF = L / 2
BAR_H = 0.28
C = np.array([0.0, 4.1, 0.0])      # centro da barra / do quadro físico
KV = 0.8                           # comprimento da seta de velocidade = KV · ω · r
S1, S3 = 0.85, 2.55                # elementos r, 3r (o de 2r é o dm móvel, s = sdm)
ELEM_COL = {1: CYAN, 2: VIOLET, 3: MAGENTA}

# ── Giro: rampa, velocidade constante, desaceleração até parar na horizontal ─
RAMP, TA, TD = 1.5, 47.0, 3.5
OM = 2 * PI * 6 / (0.5 * RAMP + (TA - RAMP) + 0.5 * TD)    # th final = 6 voltas exatas
TH_F = 2 * PI * 6


def spin_state(t):
    """(theta, omega) em função do tempo desde o início do giro."""
    if t <= 0:
        return 0.0, 0.0
    if t < RAMP:
        return OM * t * t / (2 * RAMP), OM * t / RAMP
    if t < TA:
        return OM * (0.5 * RAMP + t - RAMP), OM
    if t < TA + TD:
        u = t - TA
        return OM * (0.5 * RAMP + TA - RAMP) + OM * (u - u * u / (2 * TD)), OM * (1 - u / TD)
    return TH_F, 0.0


@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def text(content, size=26, color=WHITE, opacity=1.0, t2c=None):
    with wide_pango():
        t = screen_text(content, size, **({"t2c": t2c} if t2c else {}))
    if not t2c:
        t.set_color(color)
    t.set_opacity(opacity)
    if t.width > 8.0:
        t.scale_to_fit_width(8.0)
    return t


def text2(l1, l2, size=26, color=WHITE, opacity=1.0):
    return VGroup(text(l1, size, color, opacity), text(l2, size, color, opacity)).arrange(DOWN, buff=0.14)


def mt(*parts, size=56, color=WHITE, colors=None, w=8.3):
    m = MathTex(*parts, font_size=size, color=color)
    for i, c in (colors or {}).items():
        m[i].set_color(c)
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def box(mob, color=WHITE, buff=0.18):
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.1, stroke_width=3)


def halo(m, width=7):
    return m.set_stroke(BACKGROUND_COLOR, width, background=True)


# ── Equações com índices de glifos (MF-Tools): MathTex de string única + índices por parte ──────────────
class Eq:
    def __init__(self, *parts, size=56, colors=None, w=8.3):
        multi = MathTex(*parts, font_size=size)
        self.s = np.concatenate([[0], np.cumsum([len(q) for q in multi])]).astype(int)
        self.mob = MathTex(" ".join(parts), font_size=size, color=WHITE)
        assert len(self.mob[0]) == int(self.s[-1]), parts
        if self.mob.width > w:
            self.mob.scale_to_fit_width(w)
        for i, c in (colors or {}).items():
            self.mob[0][int(self.s[i]):int(self.s[i + 1])].set_color(c)

    def p(self, *ids):
        return [k for i in ids for k in range(int(self.s[i]), int(self.s[i + 1]))]

    def g(self, *ids):
        return [self.mob[0][k] for k in self.p(*ids)]


def copy_from(src):
    """O destino nasce de uma CÓPIA dos glifos `src`, que ficam onde estão."""
    class _Copy(TransformFromCopy):
        def __init__(self, mob, **kw):
            super().__init__(VGroup(*src), mob, **kw)
    return _Copy


def M(A, pa, B, pb, **kw):
    return (A.p(*pa), B.p(*pb), kw)


def MG(ga, gb, **kw):
    return (list(ga), list(gb), kw)


def CG(src, gb, **kw):
    kw.setdefault("delay", 0.2)
    return (copy_from(src), list(gb), kw)


class MomentoInercia014(Scene):
    # ── utilidades de tempo e geometria ─────────────────────────────────────
    def seg(self, o0, o1, n0, n1):
        """Mapa linear de tempo do bloco: marcos escritos em [o0, o1] valem [n0, n1] (identidade: seg(0, 1, 0, 1))."""
        self._map = (o0, o1, n0, n1)

    def until(self, t):
        o0, o1, n0, n1 = getattr(self, "_map", (0, 1, 0, 1))
        t = n0 + (t - o0) * (n1 - n0) / (o1 - o0)
        gap = t - self.time
        if gap > 0.02:
            self.wait(gap)
        elif gap < -0.4:
            print(f"ATRASO {-gap:.2f}s antes de t={t}")

    def A(self):
        return C + RIGHT * self.axx.get_value()

    def U(self):
        a = self.th.get_value()
        return np.array([np.cos(a), np.sin(a), 0.0])

    def Tg(self):
        a = self.th.get_value()
        return np.array([-np.sin(a), np.cos(a), 0.0])

    def P(self, s):
        return self.A() + (s - self.axx.get_value()) * self.U()

    def vv(self, key):
        return self.V[key].get_value()

    def ucur(self):
        return float(np.clip(self.axx.get_value() / L, 0.0, 0.5))

    def follow(self, mob, fn, key, z=9):
        def upd(m):
            m.move_to(fn())
            m.set_opacity(self.vv(key))
        mob.add_updater(upd)
        mob.set_z_index(z)
        self.add(mob)
        return mob

    def fade_with(self, mob, key, z=9):
        def upd(m):
            m.set_opacity(self.vv(key))
        mob.add_updater(upd)
        mob.set_z_index(z)
        self.add(mob)
        return mob

    def settle(self, *parents):
        """Depois de transformar só partes (ReplacementTransform de submobjects), recoloca o pai na cena."""
        for p in parents:
            self.remove(p)
            self.add(p)

    def show(self, *keys, **kw):
        return [self.V[k].animate.set_value(1) for k in keys]

    def hide(self, *keys, **kw):
        return [self.V[k].animate.set_value(0) for k in keys]

    def swap(self, old, new, t_out=0.35, t_in=0.5, extra_out=(), extra_in=()):
        """Estado completo → estado completo (sai e depois entra): nenhum quadro com glifos sobrepostos."""
        self.play(FadeOut(old), *extra_out, run_time=t_out)
        self.play(FadeIn(new), *extra_in, run_time=t_in)

    def swap_tail(self, old, new, k, t_out=0.35, t_in=0.5):
        """Mantém as k primeiras partes (idênticas) e troca só o resto da equação."""
        new.shift(old[0].get_center() - new[0].get_center())
        self.play(*[ReplacementTransform(old[i], new[i]) for i in range(k)],
                  *[FadeOut(old[j]) for j in range(k, len(old))], run_time=t_out)
        self.play(*[FadeIn(new[j]) for j in range(k, len(new))], run_time=t_in)
        self.settle(new)

    def mm(self, old, new, *moves, y=None, rt=1.2, extra=()):
        """old (Eq) -> new (Eq) por TransformByGlyphMap; o que não for citado entra/sai por fade."""
        c = old.mob.get_center()
        new.mob.move_to([c[0], c[1] if y is None else y, 0])
        self.play(TransformByGlyphMap(old.mob, new.mob, *moves, auto_fade=True), *extra, run_time=rt)
        self.remove(old.mob)

    # ── construção do palco ─────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.build_stage()
        for k, seg in enumerate([self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8,
                                 self.b9, self.b10, self.b11, self.b12, self.b13, self.b14, self.b15], 1):
            seg()
            if k >= ATE:
                self.wait(0.5)
                return

    def build_stage(self):
        rng = np.random.default_rng(14)
        stars = VGroup(*[Dot([rng.uniform(-4.4, 4.4), rng.uniform(-4.0, 7.2), 0],
                             radius=rng.uniform(0.01, 0.025), color=WHITE,
                             fill_opacity=rng.uniform(0.08, 0.2)) for _ in range(46)])
        self.add(stars)
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(wm.to_corner(UP + RIGHT, buff=0.28))
        self.add(text("POR TRÁS DA FÓRMULA · EP. 05", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4))

        self.th, self.om, self.axx = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.xm = ValueTracker(1.8)       # coordenada x do dm marcado (blocos 6-12)
        self.dmw = ValueTracker(0.22)
        self.sdm = ValueTracker(1.0)      # posição (ao longo da barra) do dm móvel / pedaço selecionado
        self.selw = ValueTracker(0.3)     # largura do pedaço selecionado (blocos 2 e 5)
        self.pr = ValueTracker(-2.6)      # cursor do perfil x²dm
        self.pr2 = ValueTracker(-2.6)     # cursor do perfil assinado x·dm
        self.sgk = ValueTracker(1.0)      # escala do perfil assinado (1 → 0 = cancelamento)
        keys = ["axis", "ring", "cm", "lcm", "dm", "ldm", "ldx", "rd", "rdl", "rxd", "rx", "guides", "e1", "e2",
                "e3", "a1", "a2", "a3", "lva", "lv1", "lv2", "lv3", "lr1", "lr2", "lr3", "rdim", "lrr", "lri",
                "ldm2", "lsel", "sel", "lcap", "prof", "sg", "dmx", "lxp", "lxx"]
        self.V = {k: ValueTracker(0.0) for k in keys}
        self.add(self.th, self.om, self.axx, self.xm, self.dmw, self.sdm, self.selw, self.pr, self.pr2, self.sgk,
                 *self.V.values())

        # barra (corpo rígido) + níveis de discretização (blocos 5): tudo gira junto
        self.bar = Rectangle(width=L, height=BAR_H, fill_color=BLUE, fill_opacity=0.3, stroke_color=BLUE_L,
                             stroke_width=3).move_to(C).set_z_index(1)
        self.levels = {}
        for n in (6, 12, 24, 48):
            sw = L / n
            pieces = VGroup()
            for i in range(n):
                cx = -HALF + sw * (i + 0.5)
                r = abs(cx)
                pc = Rectangle(width=sw, height=BAR_H, stroke_width=1.5, stroke_color=WHITE, stroke_opacity=0.0,
                               fill_color=VIOLET, fill_opacity=0.0).move_to(C + RIGHT * cx)
                pc.op = 0.10 + 0.78 * (r / HALF) ** 2
                pieces.add(pc)
            pieces.set_z_index(2)
            self.levels[n] = pieces
        self.body = VGroup(self.bar, *self.levels.values())
        self.lvf = {n: ValueTracker(0.0) for n in self.levels}
        self.lvs = {n: ValueTracker(0.0) for n in self.levels}
        self.add(*self.lvf.values(), *self.lvs.values(), *self.levels.values())

        def mk_upd(n):
            def upd(g):
                f, st = self.lvf[n].get_value(), self.lvs[n].get_value()
                for pc in g:
                    pc.set_fill(VIOLET, pc.op * f)
                    pc.set_stroke(WHITE, 1.5, st if f > 0.001 else 0.0)
            return upd
        for n, g in self.levels.items():
            g.add_updater(mk_upd(n))

        # giro: o relógio usa Scene.time (avança só no fim de cada play) + dt acumulado dentro do play
        self.spin_t0 = None
        self._seen_time, self._acc = -1.0, 0.0

        def spin_upd(m, dt):
            if self.spin_t0 is None:
                return
            now = self.time
            if now != self._seen_time:
                self._seen_time, self._acc = now, 0.0
            self._acc += dt
            t, o = spin_state(now - self.spin_t0 + self._acc)
            d = t - m.get_value()
            m.set_value(t)
            self.om.set_value(o)
            if abs(d) > 1e-9:
                self.body.rotate(d, about_point=self.A())
        self.th.add_updater(spin_upd)

        # eixo (⊙) e seta de sentido da rotação
        def axis_mob():
            v = self.vv("axis")
            a = self.A()
            ring = Circle(radius=0.2, stroke_color=CYAN, stroke_width=4).set_fill(BACKGROUND_COLOR, 0.95)
            ring.move_to(a)
            return VGroup(ring, Dot(a, radius=0.065, color=CYAN)).set_opacity(v)
        self.add(always_redraw(axis_mob).set_z_index(7))

        def ring_mob():
            v = self.vv("ring")
            arc = Arc(radius=0.55, start_angle=0.5, angle=4.4, stroke_color=CYAN, stroke_width=3.5)
            arc.add_tip(tip_length=0.17)
            return arc.move_arc_center_to(self.A()).set_fill(opacity=0).set_stroke(opacity=v)
        self.add(always_redraw(ring_mob).set_z_index(7))
        self.lomega = self.follow(MathTex(r"\omega", font_size=40, color=CYAN),
                                  lambda: self.A() + np.array([0.72, 0.62, 0]), "ring")

        # marcador do centro de massa (fixo na barra)
        def cm_mob():
            v = self.vv("cm")
            g = VGroup(Line(C + np.array([-0.17, -0.17, 0]), C + np.array([0.17, 0.17, 0])),
                       Line(C + np.array([-0.17, 0.17, 0]), C + np.array([0.17, -0.17, 0])))
            return g.set_stroke(WHITE, 3.5).set_opacity(v)
        self.add(always_redraw(cm_mob).set_z_index(6))
        self.lcm_t = self.follow(text("CM", 24), lambda: C + np.array([-0.5, -0.62, 0]), "lcm")

        # dm / dx marcado
        def dm_mob():
            v = self.vv("dm")
            r = Rectangle(width=self.dmw.get_value(), height=BAR_H + 0.16, fill_color=WHITE,
                          fill_opacity=0.92, stroke_width=0)
            return r.move_to(C + RIGHT * self.xm.get_value()).set_opacity(v)
        self.add(always_redraw(dm_mob).set_z_index(6))
        self.l_dm = self.follow(MathTex("dm", font_size=40), lambda: C + RIGHT * self.xm.get_value() + UP * 0.62,
                                "ldm")
        self.l_dx = self.follow(MathTex("dx", font_size=40), lambda: C + RIGHT * self.xm.get_value() + UP * 0.62,
                                "ldx")
        # outros dm (todos com o mesmo d), bloco 9
        self.dmx = VGroup(*[Rectangle(width=0.3, height=BAR_H + 0.16, fill_color=WHITE, fill_opacity=0.9,
                                      stroke_width=0).move_to(C + RIGHT * x) for x in (-1.7, 0.6, 2.1)])
        self.fade_with(self.dmx, "dmx", z=6)

        # linhas de cota (d, x', x) sob a barra
        RY = {"rd": 3.15, "rxd": 2.45, "rx": 1.75}
        self.RY = RY

        def dim_row(key, getx0, getx1, color, lab, lkey=None):
            def mob():
                v = self.vv(key)
                x0, x1, y = getx0(), getx1(), RY[key]
                if abs(x1 - x0) < 0.08:
                    x1 = x0 + 0.08
                g = VGroup(Arrow([x0, y, 0], [x1, y, 0], buff=0, stroke_width=4, color=color,
                                 max_tip_length_to_length_ratio=0.3, tip_length=0.2),
                           Line([x0, y - 0.12, 0], [x0, y + 0.12, 0], stroke_width=4, color=color))
                return g.set_opacity(v)
            self.add(always_redraw(mob).set_z_index(4))
            m = self.follow(lab, lambda: [(getx0() + getx1()) / 2, RY[key] + 0.3, 0], lkey or key, z=9)
            halo(m)
            return m
        self.lab_d = dim_row("rd", lambda: C[0], lambda: C[0] + self.axx.get_value(), VIOLET,
                             MathTex("d", font_size=44, color=VIOLET), lkey="rdl")
        self.lab_d2 = self.follow(MathTex(r"d=L/2", font_size=46, color=VIOLET),
                                  lambda: [(C[0] + C[0] + self.axx.get_value()) / 2, RY["rd"] - 0.55, 0], "lcap")
        halo(self.lab_d2)
        self.lab_xp = dim_row("rxd", lambda: C[0] + self.axx.get_value(), lambda: C[0] + self.xm.get_value(),
                              WHITE, MathTex("x'", font_size=44), lkey="lxp")
        self.lab_x = dim_row("rx", lambda: C[0], lambda: C[0] + self.xm.get_value(), CYAN,
                             MathTex("x", font_size=44, color=CYAN), lkey="lxx")

        def guides_mob():
            v = self.vv("guides")
            g = VGroup(*[DashedLine([x, 3.85, 0], [x, 1.6, 0], dash_length=0.1, stroke_width=1.8,
                                    color=WHITE, stroke_opacity=0.32 * v)
                         for x in (C[0], C[0] + self.axx.get_value(), C[0] + self.xm.get_value())])
            return g
        self.add(always_redraw(guides_mob).set_z_index(0))

        # elementos de mesma massa (r, 2r, 3r): setas v = ωr
        self.make_elem(1, lambda: S1)
        self.make_elem(2, lambda: self.sdm.get_value())
        self.make_elem(3, lambda: S3)

        def rdim_mob():
            v = self.vv("rdim")
            s, a, T = self.sdm.get_value(), self.A(), self.Tg()
            p0, p1 = a - 0.5 * T, self.P(s) - 0.5 * T
            g = VGroup(Line(p0, p1, stroke_width=3, color=WHITE),
                       Line(p0 - 0.1 * T, p0 + 0.1 * T, stroke_width=3, color=WHITE),
                       Line(p1 - 0.1 * T, p1 + 0.1 * T, stroke_width=3, color=WHITE))
            return g.set_opacity(v)
        self.add(always_redraw(rdim_mob).set_z_index(4))

        def mid_r():
            return (self.A() + self.P(self.sdm.get_value())) / 2 - 0.85 * self.Tg()
        self.lrdim = halo(self.follow(MathTex("r", font_size=44), mid_r, "lrr"))
        self.lrdim_i = halo(self.follow(MathTex("r_i", font_size=44), mid_r, "lri"))
        self.lab_dm_e2 = halo(self.follow(MathTex("dm", font_size=40, color=VIOLET),
                                          lambda: self.P(self.sdm.get_value()) - 0.55 * self.Tg()
                                          + 0.62 * self.U(), "ldm2"))
        # pedaço selecionado na discretização (bloco 5)

        def sel_mob():
            v = self.vv("sel")
            r = Rectangle(width=self.selw.get_value(), height=BAR_H + 0.12, stroke_color=WHITE, stroke_width=3.5,
                          fill_opacity=0).rotate(self.th.get_value())
            return r.move_to(self.P(self.sdm.get_value())).set_stroke(opacity=v)
        self.add(always_redraw(sel_mob).set_z_index(6))
        self.lsel_m = halo(self.follow(MathTex(r"\Delta m_i", font_size=40),
                                       lambda: self.P(self.sdm.get_value()) + 0.7 * self.Tg(), "lsel"))

        # perfil x²dm acima da barra (blocos 6-7), revelado pelo cursor `pr`
        NP = 26
        wcol = L / NP
        BASEP = C[1] + 0.34

        def prof_mob():
            v = self.vv("prof")
            g = VGroup()
            for i in range(NP):
                x = -HALF + (i + 0.5) * wcol
                if x - wcol / 2 > self.pr.get_value():
                    break
                h = max(0.04, 0.2 * x * x)
                cur = abs(x - self.pr.get_value()) < wcol / 2 + 1e-6 and self.pr.get_value() < HALF - 0.01
                g.add(Rectangle(width=wcol * 0.92, height=h, stroke_width=0,
                                fill_color=WHITE if cur else CYAN, fill_opacity=(0.9 if cur else 0.6) * v
                                ).move_to([x, BASEP + h / 2 + 0.02, 0]))
            if not len(g):
                g.add(Rectangle(width=0.01, height=0.01, stroke_width=0, fill_opacity=0).move_to([-HALF, BASEP, 0]))
            return g
        self.add(always_redraw(prof_mob).set_z_index(3))

        # perfil assinado x·dm (bloco 11): + à direita, − à esquerda; sgk → 0 = cancelamento
        BASES = C[1] + 1.4
        self.BASES = BASES

        def sg_mob():
            v = self.vv("sg")
            g = VGroup()
            for i in range(NP):
                x = -HALF + (i + 0.5) * wcol
                if x - wcol / 2 > self.pr2.get_value():
                    break
                h = max(0.03, 0.34 * abs(x) * self.sgk.get_value())
                col = MAGENTA if x > 0 else BLUE_L
                g.add(Rectangle(width=wcol * 0.92, height=h, stroke_width=0, fill_color=col,
                                fill_opacity=0.65 * v).move_to([x, BASES + (h / 2 if x > 0 else -h / 2), 0]))
            if not len(g):
                g.add(Rectangle(width=0.01, height=0.01, stroke_width=0, fill_opacity=0).move_to([-HALF, BASES, 0]))
            return g
        self.add(always_redraw(sg_mob).set_z_index(3))
        self.sgbase = Line([-HALF - 0.1, BASES, 0], [HALF + 0.1, BASES, 0], stroke_width=2, color=WHITE)
        self.fade_with(self.sgbase, "sg")
        self.sgbase.add_updater(lambda m: m.set_stroke(opacity=0.6 * self.vv("sg")))
        self.sgpm = VGroup(MathTex("-", font_size=44, color=BLUE_L).move_to([-HALF - 0.45, BASES, 0]),
                           MathTex("+", font_size=44, color=MAGENTA).move_to([HALF + 0.45, BASES, 0]))
        self.fade_with(self.sgpm, "sg")


    def make_elem(self, k, sfn):
        col = ELEM_COL[k]

        def sq():
            v = self.vv(f"e{k}")
            r = Rectangle(width=0.3, height=0.3, fill_color=col, fill_opacity=0.95, stroke_color=WHITE,
                          stroke_width=2).rotate(self.th.get_value())
            return r.move_to(self.P(sfn())).set_opacity(v)

        def arr():
            v = self.vv(f"a{k}")
            ln = max(KV * self.om.get_value() * (sfn() - self.axx.get_value()), 0.12)
            p = self.P(sfn())
            return Arrow(p, p + self.Tg() * ln, buff=0, color=col, stroke_width=6, tip_length=min(0.28, ln * 0.45),
                         max_tip_length_to_length_ratio=0.5).set_opacity(v)
        self.add(always_redraw(sq).set_z_index(5), always_redraw(arr).set_z_index(5))

        def tip():
            ln = max(KV * self.om.get_value() * (sfn() - self.axx.get_value()), 0.12)
            return self.P(sfn()) + self.Tg() * (ln + 0.36)
        lab_v = {1: "v", 2: "2v", 3: "3v"}[k]
        lab_r = {1: "r", 2: "2r", 3: "3r"}[k]
        setattr(self, f"lv{k}_m", halo(self.follow(MathTex(lab_v, font_size=44, color=col), tip, f"lv{k}")))
        setattr(self, f"lr{k}_m", halo(self.follow(MathTex(lab_r, font_size=44, color=col),
                                                   lambda: self.P(sfn()) - 0.55 * self.Tg(), f"lr{k}")))
        if k == 2:
            self.lva_m = halo(self.follow(MathTex("v", font_size=44, color=col), tip, "lva"))

    # ── BLOCO 1 · 0–15 s · abertura: assunto, mesma barra, mistério e mapa do vídeo ─
    def b1(self):
        self.seg(0, 1, 0, 1)
        self.play(FadeIn(self.bar), *self.show("axis", "cm", "lcm"), run_time=0.9)
        lL = VGroup(Line([-HALF, 5.0, 0], [HALF, 5.0, 0], stroke_width=3, color=WHITE),
                    Line([-HALF, 4.88, 0], [-HALF, 5.12, 0], stroke_width=3, color=WHITE),
                    Line([HALF, 4.88, 0], [HALF, 5.12, 0], stroke_width=3, color=WHITE)).set_opacity(0.8)
        lLt = halo(MathTex("L", font_size=44).move_to([0, 5.0, 0]))
        lM = MathTex("M", font_size=48).move_to(C + np.array([-1.7, 0.62, 0]))
        eixo_cm = text("eixo pelo CM", 26, opacity=0.9).move_to([0, 2.9, 0])
        t_a = text("POR QUE O EIXO MUDA", 32, t2c={"EIXO": CYAN})
        t_b = text("O MOMENTO DE INÉRCIA?", 32)
        title = VGroup(t_a, t_b).arrange(DOWN, buff=0.16).move_to([0, 0.9, 0])
        # 0–3,6 s: o assunto, antes de qualquer fórmula (quadro parado)
        self.play(FadeIn(lL), FadeIn(lLt), FadeIn(lM), FadeIn(eixo_cm, shift=UP * 0.1),
                  FadeIn(title, shift=UP * 0.12), run_time=1.1)
        self.until(3.6)
        # 3,6–7,3 s: a mesma barra; só o eixo se move (a animação já diz "só o eixo mudou")
        cap = text("mesma barra • mesma M • mesmo L", 28).move_to([0, 2.0, 0])
        cap2 = text("centro → ponta", 32, CYAN).move_to([0, 1.1, 0])
        self.play(FadeOut(title), FadeOut(eixo_cm), FadeIn(cap, shift=UP * 0.1), FadeIn(cap2, shift=UP * 0.1),
                  run_time=0.7)
        self.until(4.3)
        self.play(self.axx.animate.set_value(HALF), run_time=3.0, rate_func=smooth)
        self.until(7.3)
        # 7,3–10,6 s: o mistério, parado para leitura
        q = mt("I_{\\rm ponta}", "=", "4", "I_{CM}", r"\;?", size=64, w=6.6, colors={3: CYAN, 4: MAGENTA}
               ).move_to([0, -1.0, 0])
        q2 = text("de onde vem esse 4?", 34).move_to([0, -2.3, 0])
        self.play(FadeIn(q, shift=UP * 0.12), FadeIn(q2, shift=UP * 0.12), run_time=0.8)
        self.until(10.6)
        self.play(FadeOut(q), FadeOut(q2), FadeOut(cap), FadeOut(cap2), FadeOut(lL),
                  FadeOut(lLt), FadeOut(lM), run_time=0.6)
        # 11,2–14 s: o mapa do vídeo entra completo
        r1 = VGroup(text("1.", 30, CYAN), text("de onde vem", 30), MathTex(r"r_\perp^2", font_size=46, color=CYAN),
                    text("?", 30)).arrange(RIGHT, buff=0.18)
        r2 = VGroup(text("2.", 30, VIOLET), text("por que mover o eixo adiciona", 30),
                    MathTex("Md^2", font_size=46, color=VIOLET), text("?", 30)).arrange(RIGHT, buff=0.18)
        road = VGroup(r1, r2).arrange(DOWN, buff=0.8, aligned_edge=LEFT).move_to([0, 0.4, 0])
        if road.width > 7.8:
            road.scale_to_fit_width(7.8)
        self.road = road
        self.play(FadeIn(road, shift=UP * 0.1), run_time=0.8)
        self.until(14.0)
        # vamos responder à primeira: o eixo volta ao CM e a barra começa a girar (bloco 2)
        self.play(r2.animate.set_opacity(0.3), Indicate(r1[2], color=CYAN, scale_factor=1.2),
                  self.axx.animate.set_value(0.0), *self.hide("cm", "lcm"), run_time=0.9, rate_func=smooth)
        self.until(15.0)

    # ── BLOCO 2 · 11–22 s · v = ωr com um dm que se afasta ──────────────────
    def b2(self):
        self.seg(11, 22, 15, 27)
        self.spin_t0 = self.time
        self.sdm.set_value(1.0)
        self.selw.set_value(0.3)
        self.play(*self.show("ring"), FadeOut(self.road), run_time=0.8)
        self.until(12.0)
        self.play(*self.show("e2", "ldm2"), run_time=0.7)
        self.until(13.0)
        cap_r = VGroup(MathTex(r"r_\perp", font_size=46), text("= distância perpendicular ao eixo", 28)
                       ).arrange(RIGHT, buff=0.2).move_to([0, 0.5, 0])
        self.play(*self.show("rdim", "lrr"), FadeIn(cap_r, shift=UP * 0.1), run_time=0.8)
        self.until(14.0)
        self.play(*self.show("a2", "lva"), run_time=0.8)
        self.until(15.0)
        self.play(FadeOut(cap_r), run_time=0.4)
        veq = self.veq = Eq("v", "=", r"\omega", r"r_\perp", size=72, colors={0: CYAN, 2: CYAN})
        veq.mob.move_to([0, -1.2, 0])
        # o dm se afasta com ω constante: r↑ ⇒ v↑ (a seta e o rótulo v acompanham)
        up = mt(r"r\uparrow", r"\Rightarrow", r"v\uparrow", size=56, colors={0: WHITE, 2: CYAN}).move_to([0, 0.4, 0])
        self.play(self.sdm.animate.set_value(2.4), FadeIn(up, shift=UP * 0.1), FadeIn(veq.mob), run_time=3.2,
                  rate_func=smooth)
        self.play(self.sdm.animate.set_value(0.9), run_time=2.2, rate_func=smooth)
        self.play(self.sdm.animate.set_value(1.7), run_time=1.2, rate_func=smooth)
        self.until(21.5)
        self.play(FadeOut(up), *self.hide("rdim", "lrr"), run_time=0.5)
        self.until(22.0)

    # ── BLOCO 3 · 22–36 s · o r² nasce: v² → (ωr)² → ω²r² ───────────────────
    def b3(self):
        self.seg(22, 36, 27, 39)
        veq = self.veq
        self.play(veq.mob.animate.scale(0.62).move_to([0, 0.75, 0]), run_time=0.9)
        P1 = Eq("dK", "=", r"\frac12", "v^2", "dm", size=66, w=6.2, colors={3: CYAN})
        P1.mob.move_to([0, -0.8, 0])
        self.play(FadeIn(P1.mob, shift=UP * 0.1), run_time=1.4)
        self.until(26.2)
        # 1) v² → (ωr)²: o termo ωr é copiado de v = ωr para dentro do quadrado
        P2 = Eq("dK", "=", r"\frac12", "(", r"\omega r_\perp", ")^2", "dm", size=66, w=6.2, colors={3: CYAN, 4: CYAN, 5: CYAN})
        wr_src = [veq.mob[0][k] for k in veq.p(2, 3)]
        self.play(*[Indicate(g, color=CYAN, scale_factor=1.35) for g in wr_src], run_time=0.8)
        self.mm(P1, P2, M(P1, [0, 1, 2], P2, [0, 1, 2]), M(P1, [4], P2, [6]),
                MG([P1.p(3)[0]], [P2.p(3)[0]]), MG([P1.p(3)[1]], [P2.p(5)[1]]),
                CG(wr_src, P2.p(4)), rt=1.8)
        self.until(30.2)
        # 2) (ωr)² → ω²r²: o expoente 2 vale para cada fator
        P3 = Eq("dK", "=", r"\frac12", r"\omega^2", r"r_\perp^2", "dm", size=66, w=6.2, colors={3: CYAN, 4: VIOLET})
        idx4 = P2.p(4)
        w_i, r_idx = idx4[0], idx4[1:]
        close_i, two_i = P2.p(5)
        self.mm(P2, P3, M(P2, [0, 1, 2], P3, [0, 1, 2]), M(P2, [6], P3, [5]),
                MG([w_i], [P3.p(3)[0]]), MG(r_idx, P3.p(4)[:2]), MG([two_i], [P3.p(3)[1]]),
                CG([P2.mob[0][two_i]], [P3.p(4)[2]]), MG([P2.p(3)[0], close_i], []), rt=1.8)
        self.P3 = P3
        self.until(33.0)
        self.boxP3 = box(P3.mob, VIOLET)
        self.play(Create(self.boxP3), Indicate(P3.mob[0][P3.p(4)[0]:P3.p(4)[-1] + 1], color=VIOLET), run_time=0.8)
        prop = mt("dK", r"\propto", r"r_\perp^2", size=52, colors={2: VIOLET}).move_to([0, -2.7, 0])
        self.play(FadeIn(prop, shift=UP * 0.1), run_time=0.8)
        self.prop = prop
        self.until(36.6)

    # ── BLOCO 4 · 37–46 s · 1 : 4 : 9 (mesmo dm, mesma ω) ───────────────────
    def b4(self):
        self.seg(0, 1, 2.4, 3.4)
        self.play(FadeOut(self.P3.mob), FadeOut(self.boxP3), FadeOut(self.veq.mob),
                  self.prop.animate.move_to([0, -3.75, 0]).scale(0.8),
                  *self.show("e1", "e3", "a1", "a3", "lr1", "lr2", "lr3", "lv1", "lv2", "lv3"),
                  *self.hide("lva", "ldm2"), run_time=1.3)
        BASE, UNIT = -0.8, 0.22
        xs = {1: -2.5, 2: 0.0, 3: 2.5}
        units = {1: 1, 2: 4, 3: 9}
        self.bars4 = VGroup()
        self.until(38.8)
        for k in (1, 2, 3):
            n = units[k]
            h = UNIT * n
            bar = Rectangle(width=0.9, height=h, fill_color=ELEM_COL[k], fill_opacity=0.65, stroke_color=ELEM_COL[k],
                            stroke_width=3).move_to([xs[k], BASE + h / 2, 0])
            ticks = VGroup(*[Line([xs[k] - 0.45, BASE + UNIT * j, 0], [xs[k] + 0.45, BASE + UNIT * j, 0],
                                  stroke_width=1.5, color=WHITE, stroke_opacity=0.5) for j in range(1, n)])
            dist = MathTex({1: "r", 2: "2r", 3: "3r"}[k], font_size=48, color=ELEM_COL[k]
                           ).move_to([xs[k], BASE - 0.45, 0])
            mult = MathTex({1: r"1\times", 2: r"4\times", 3: r"9\times"}[k], font_size=70, color=ELEM_COL[k]
                           ).move_to([xs[k], BASE - 1.2, 0])
            self.bars4.add(VGroup(bar, ticks, dist, mult))
            self.play(FadeIn(bar, shift=UP * 0.1), FadeIn(ticks), FadeIn(dist), run_time=0.7)
            self.play(FadeIn(mult), run_time=0.5)
        note = VGroup(text("mesmo dm • mesma", 28), MathTex(r"\omega", font_size=44)
                      ).arrange(RIGHT, buff=0.14).move_to([0, -2.85, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.note4 = note
        self.until(45.4)
        self.play(FadeOut(self.bars4), FadeOut(note), FadeOut(self.prop),
                  *self.hide("e1", "e2", "e3", "a1", "a2", "a3", "lr1", "lr2", "lr3", "lv1", "lv2", "lv3"),
                  run_time=0.6)
        self.until(46.0)

    # ── BLOCO 5 · 44–60 s · soma discreta → integral → I ────────────────────
    def b5(self):
        self.seg(44, 60, 48, 65.5)
        L6 = self.levels[6]

        def tint(n, stroke=0.7):
            return [self.lvf[n].animate.set_value(1.0), self.lvs[n].animate.set_value(stroke)]

        def untint(n):
            return [self.lvf[n].animate.set_value(0.0), self.lvs[n].animate.set_value(0.0)]

        def nearest(level, s0=1.5):
            ci = [-HALF + (i + 0.5) * L / len(level) for i in range(len(level))]
            return min(ci, key=lambda c: abs(c - s0))
        self.sdm.set_value(1.7)
        self.play(*tint(6), run_time=1.0)
        s6 = nearest(L6)
        self.play(self.sdm.animate.set_value(s6), self.selw.animate.set_value(L / 6), *self.show("sel", "lsel", "rdim", "lri"),
                  run_time=1.0)
        self.until(46.8)
        e2 = mt("K", "=", r"\frac12\omega^2", r"\sum_i", r"r_i^2\Delta m_i", size=54, w=6.2, colors={3: VIOLET}
                ).move_to([0, 0.2, 0])
        self.play(FadeIn(e2, shift=UP * 0.1), run_time=1.2)
        self.until(50.8)
        cnt = text("mais pedaços, cada Δm menor", 28).move_to([0, -0.8, 0])
        self.play(FadeIn(cnt, shift=UP * 0.1), run_time=0.5)
        prev = 6
        for n, t_ in ((12, 51.4), (24, 52.4), (48, 53.4)):
            lv = self.levels[n]
            s_n = nearest(lv)
            self.play(*untint(prev), *tint(n), self.sdm.animate.set_value(s_n), self.selw.animate.set_value(L / n),
                      run_time=0.8)
            prev = n
            self.until(t_ + 0.9)
        e3 = mt("K", "=", r"\frac12\omega^2", r"\int", r"r_\perp^2dm", size=54, w=6.2, colors={3: VIOLET}).move_to([0, 0.2, 0])
        e3.shift(e2[0].get_center() - e3[0].get_center())
        self.play(ReplacementTransform(e2[0], e3[0]), ReplacementTransform(e2[1], e3[1]),
                  ReplacementTransform(e2[2], e3[2]), ReplacementTransform(e2[3], e3[3]),
                  FadeOut(e2[4]), FadeOut(cnt),
                  self.lvs[48].animate.set_value(0.0), *self.hide("lsel", "lri", "rdim", "sel"),
                  run_time=0.9)
        self.play(FadeIn(e3[4]), run_time=0.6)
        self.settle(e3)
        self.until(56.0)
        eqI = mt("I", "=", r"\int", r"r_\perp^2dm", size=62, w=5.0, colors={0: CYAN}).move_to([0, -1.55, 0])
        # I é exatamente esse fator: destaque na equação de K e depois a definição completa (sem cópia sobreposta)
        hl = SurroundingRectangle(e3[3:5], color=CYAN, buff=0.1, corner_radius=0.08, stroke_width=3)
        self.play(Create(hl), run_time=0.6)
        self.play(FadeIn(eqI, shift=UP * 0.1), run_time=0.7)
        self.boxI = box(eqI, CYAN)
        self.play(Create(self.boxI), FadeOut(hl), run_time=0.5)
        eqK = mt("K", "=", r"\frac12", "I", r"\omega^2", size=48, w=4.2, colors={3: CYAN}).move_to([0, -3.5, 0])
        self.play(FadeIn(eqK, shift=UP * 0.12), run_time=0.9)
        self.eqE3, self.eqI, self.eqK, self.lastlevel = e3, eqI, eqK, prev
        self.until(60.0)

    # ── BLOCO 6 · 64–76 s · r_perp = |x|; barra uniforme: dm = (M/L)dx; perfil x²dm ──
    def b6(self):
        self.seg(0, 1, 1.5, 2.5)
        self.play(FadeOut(self.eqE3), FadeOut(self.eqK), FadeOut(self.boxI),
                  self.lvf[48].animate.set_value(0.0), *self.hide("ring"),
                  self.eqI.animate.scale(0.8).move_to([0, -2.4, 0]), run_time=1.0)
        yv = 3.5
        self.xline = VGroup(Line([-HALF - 0.4, yv, 0], [HALF + 0.5, yv, 0], stroke_width=2.5, color=WHITE),
                            *[Line([x, yv - 0.1, 0], [x, yv + 0.1, 0], stroke_width=3, color=WHITE)
                              for x in (-HALF, 0, HALF)]).set_opacity(0.8)
        self.xlabs = VGroup(MathTex("-L/2", font_size=34).move_to([-HALF, yv - 0.38, 0]),
                            MathTex("0", font_size=34).move_to([0, yv - 0.36, 0]),
                            MathTex("L/2", font_size=34).move_to([HALF, yv - 0.38, 0]),
                            MathTex("x", font_size=38, color=CYAN).move_to([HALF + 0.65, yv, 0]))
        self.xm.set_value(-HALF + 0.1)
        self.pr.set_value(-HALF - 0.2)
        self.dmw.set_value(0.2)
        self.play(Create(self.xline), FadeIn(self.xlabs), *self.show("cm"), run_time=0.8)
        # ponte: com o eixo no CM, a distância perpendicular ao eixo é |x|
        br1 = mt(r"r_\perp", "=", "|x|", size=60, colors={2: CYAN}).move_to([0, 1.7, 0])
        self.play(FadeIn(br1, shift=UP * 0.1), run_time=0.8)
        self.until(67.4)
        br2 = mt(r"r_\perp^2", "=", "x^2", size=60, colors={2: CYAN}).move_to([0, 1.7, 0])
        self.swap(br1, br2, 0.4, 0.5)
        self.until(68.8)
        lam = mt("dm", "=", r"\lambda", "dx", size=60, colors={2: CYAN}).move_to([0, 1.7, 0])
        self.play(FadeOut(br2), run_time=0.4)
        self.play(*self.show("dm", "ldx", "prof"), FadeIn(lam, shift=UP * 0.1), run_time=0.8)
        # o dm desliza e o cursor do perfil acompanha: contribuição ∝ x²
        lab = MathTex(r"x^2\,dm", font_size=44, color=CYAN).move_to([-2.0, 6.1, 0])
        self.play(self.xm.animate.set_value(HALF - 0.1), self.pr.animate.set_value(HALF + 0.2), FadeIn(lab),
                  run_time=2.6, rate_func=smooth)
        self.lab6 = lab
        self.until(72.8)
        # estado 1 completo → λ = M/L → estado 2 completo (troca da equação inteira, sem morph de glifos)
        lameq = mt(r"\lambda", "=", r"\frac ML", size=42, colors={0: CYAN}).move_to([0, 0.2, 0])
        self.play(FadeIn(lameq, shift=UP * 0.1), run_time=0.7)
        self.until(74.2)
        dmeq = mt("dm", "=", r"\frac ML", "dx", size=60, colors={2: CYAN}).move_to([0, 1.7, 0])
        self.swap(lam, dmeq, 0.4, 0.6, extra_out=(FadeOut(lameq),))
        self.dmeq = dmeq
        self.until(76.0)

    # ── BLOCO 7 · 76–89 s · I_CM em estados completos ───────────────────────
    def b7(self):
        self.seg(0, 1, 1.5, 2.5)
        self.play(self.dmeq.animate.scale(0.7).move_to([0, 2.3, 0]), run_time=0.7)
        S1 = mt("I_{CM}", "=", r"\int", "x^2", "dm", size=62, colors={0: CYAN}).move_to([0, 0.35, 0])
        self.swap(self.eqI, S1, 0.4, 0.6)
        self.until(78.8)
        # destaque: dm = (M/L)dx é o que entra na integral
        self.play(Indicate(self.dmeq, color=CYAN, scale_factor=1.15), run_time=0.9)
        self.until(80.0)
        S3 = mt("I_{CM}", "=", r"\frac ML", r"\int_{-L/2}^{L/2}", "x^2", "dx", size=58, w=6.2, colors={0: CYAN}
                ).move_to([0, 0.35, 0])
        self.swap(S1, S3, 0.4, 0.7)
        self.until(82.8)
        S4 = mt("I_{CM}", "=", r"\frac ML", r"\left[\frac{x^3}{3}\right]_{-L/2}^{L/2}", size=58, w=6.2, colors={0: CYAN}
                ).move_to([0, 0.35, 0])
        self.swap(S3, S4, 0.4, 0.6)
        self.until(85.2)
        S7 = mt("I_{CM}", "=", r"\frac1{12}ML^2", size=80, w=6.0, colors={0: CYAN, 2: CYAN}).move_to([0, 0.2, 0])
        self.swap(S4, S7, 0.4, 0.6, extra_out=(FadeOut(self.dmeq),))
        self.S7box = box(S7, CYAN)
        c2 = text2("massa perto do eixo contribui pouco", "massa longe contribui muito mais", 32
                   ).move_to([0, -1.5, 0])
        self.play(Create(self.S7box), FadeIn(c2, shift=UP * 0.1), run_time=0.7)
        self.S7, self.c7 = S7, c2
        self.until(89.0)

    # ── BLOCO 8 · 89–102 s · o eixo desliza por d (CM fixo); x' = x − d ─────
    def b8(self):
        self.seg(0, 1, 0, 1)
        Eref = self.Eref = VGroup(self.S7, self.S7box)
        self.play(FadeOut(self.c7), FadeOut(self.lab6), FadeOut(self.xline), FadeOut(self.xlabs),
                  *self.hide("prof", "ldx"), run_time=0.4)
        self.play(Eref.animate.scale(0.5).move_to([0, -3.4, 0]), run_time=0.6)
        self.xm.set_value(2.1)
        self.dmw.set_value(0.3)
        self.play(*self.show("dm", "ldm", "guides", "rx", "lcm", "lxx"), run_time=0.9)
        q = text2("E se o eixo mudar?", "Preciso refazer toda a integral?", 30).move_to([0, 0.5, 0])
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.7)
        self.until(92.6)
        self.d_val = 0.9
        self.play(FadeOut(q), run_time=0.4)
        self.play(*self.show("rd", "rdl"), self.axx.animate.set_value(self.d_val), run_time=2.6, rate_func=smooth)
        self.play(*self.show("rxd", "lxp"), run_time=0.8)
        self.until(96.6)
        # só a relação que será usada: x' = x − d (a geometria já mostra x = d + x')
        xe2 = mt("x'", "=", "x", "-", "d", size=66, colors={2: CYAN, 4: VIOLET}).move_to([0, 0.6, 0])
        self.play(FadeIn(xe2, shift=UP * 0.1), run_time=1.0)
        self.xe2 = xe2
        self.until(98.4)
        note = text2("x' é coordenada com sinal", "distância ao eixo = |x'|", 30).move_to([0, -0.5, 0])
        self.play(FadeIn(note, shift=UP * 0.1), self.xm.animate.set_value(-0.3), run_time=1.0, rate_func=smooth)
        self.play(self.xm.animate.set_value(2.1), run_time=0.9, rate_func=smooth)
        self.play(FadeOut(note), run_time=0.3)
        self.until(101.0)

    # ── BLOCO 9 · 102–121 s · expandir (x−d)²; d constante; I_CM e M ────────
    def b9(self):
        self.seg(0, 1, 0.5, 1.5)
        # o box de I_CM já cumpriu o papel: a próxima equação carrega I_CM
        self.play(*self.hide("rxd", "rx", "lxp", "lxx", "guides", "dm", "ldm", "lcm"), FadeOut(self.Eref),
                  self.xe2.animate.scale(0.7).move_to([0, 1.8, 0]), run_time=0.9)
        E0 = mt("I'", "=", r"\int", "(x')^2", "dm", size=58, w=5.4).move_to([0, 0.5, 0])
        self.play(FadeIn(E0, shift=UP * 0.1), run_time=0.9)
        self.until(104.6)
        E1 = mt("I'", "=", r"\int", "(x-d)^2", "dm", size=58, w=5.4).move_to([0, 0.5, 0])
        self.swap(E0, E1, 0.4, 0.5, extra_in=(Indicate(self.xe2[2:5], color=CYAN, scale_factor=1.2),))
        self.play(FadeOut(self.xe2), run_time=0.4)
        self.until(106.8)
        # (x−d)² = x² − 2dx + d²: a igualdade só entra com o lado direito completo
        binom = mt(r"(x-d)^2", "=", "x^2", "-2dx", "+d^2", size=42, w=5.0, colors={2: CYAN, 3: MAGENTA, 4: VIOLET}
                   ).move_to([0, -1.0, 0])
        self.play(FadeIn(binom, shift=UP * 0.1), run_time=1.0)
        self.until(109.0)
        E2 = mt("I'", "=", r"\int", "(", "x^2", "-", "2", "d", "x", "+", "d^2", ")", "dm", size=54, w=6.2,
                colors={4: CYAN, 5: MAGENTA, 6: MAGENTA, 7: MAGENTA, 8: MAGENTA, 9: VIOLET, 10: VIOLET}
                ).move_to([0, 0.5, 0])
        self.swap(E1, E2, 0.4, 0.6)
        self.until(110.8)
        # linearidade: a integral da soma é a soma das integrais (d ainda dentro)
        E2b = mt("I'", "=", r"\int", "x^2", r"\,dm", "-", r"\int", "2", "d", "x", r"\,dm", "+", r"\int", "d^2",
                 r"\,dm", size=48, w=6.8,
                 colors={3: CYAN, 5: MAGENTA, 7: MAGENTA, 8: MAGENTA, 9: MAGENTA, 10: MAGENTA, 11: VIOLET, 13: VIOLET}
                 ).move_to([0, 0.5, 0])
        self.swap(E2, E2b, 0.4, 0.6, extra_out=(FadeOut(binom),))
        self.until(112.8)
        # d é constante: sai das integrais
        E3 = mt("I'", "=", r"\int", "x^2", "dm", "-", "2", "d", r"\int", "x", r"\,dm", "+", "d^2", r"\int", "dm",
                size=48, w=6.8,
                colors={3: CYAN, 5: MAGENTA, 6: MAGENTA, 7: MAGENTA, 9: MAGENTA, 10: MAGENTA, 11: VIOLET,
                        12: VIOLET}).move_to([0, 0.5, 0])
        cons = text("d é constante", 32, color=VIOLET).move_to([0, -1.4, 0])
        self.swap(E2b, E3, 0.4, 0.6, extra_in=(FadeIn(cons, shift=UP * 0.1),))
        self.until(115.0)
        # primeiro e terceiro termos já são conhecidos: chaves em vez de igualdades
        br1 = Brace(VGroup(E3[2], E3[3], E3[4]), DOWN, color=CYAN, buff=0.12)
        br2 = Brace(VGroup(E3[13], E3[14]), DOWN, color=VIOLET, buff=0.12)
        t1 = MathTex("I_{CM}", font_size=38, color=CYAN).next_to(br1, DOWN, buff=0.1)
        t2 = MathTex("M", font_size=38, color=VIOLET).next_to(br2, DOWN, buff=0.1)
        self.play(FadeOut(cons), GrowFromCenter(br1), GrowFromCenter(br2), FadeIn(t1), FadeIn(t2), run_time=1.2)
        self.until(117.0)
        E5 = mt("I'", "=", "I_{CM}", "-", "2", "d", r"\int", "x", r"\,dm", "+", "Md^2", size=52, w=6.6,
                colors={2: CYAN, 3: MAGENTA, 4: MAGENTA, 5: MAGENTA, 7: MAGENTA, 8: MAGENTA, 10: VIOLET}
                ).move_to([0, 0.5, 0])
        self.swap(VGroup(E3, br1, br2, t1, t2), E5, 0.4, 0.6)
        self.E5 = E5
        self.rb2 = box(E5[3:9], MAGENTA, buff=0.11)
        q = text("e o termo do meio?", 28, MAGENTA).move_to([0, -1.1, 0])
        self.play(Create(self.rb2), FadeIn(q, shift=UP * 0.1), run_time=0.7)
        self.q9 = q
        self.until(121.0)

    # ── BLOCO 10 · 121–135 s · o termo que zera: ∫x dm = M x_CM = 0 ─────────
    def b10(self):
        self.seg(0, 1, 0.5, 1.5)
        self.play(FadeOut(self.q9), *self.show("sg", "lcm", "cm"), run_time=0.5)
        self.xm.set_value(-HALF + 0.1)
        self.dmw.set_value(0.2)
        self.pr2.set_value(-HALF - 0.2)
        self.play(*self.show("dm", "ldx"), run_time=0.3)
        # o dm varre a barra e o perfil assinado x·dm cresce com ele
        self.play(self.xm.animate.set_value(HALF - 0.1), self.pr2.animate.set_value(HALF + 0.2), run_time=3.0,
                  rate_func=smooth)
        self.play(*self.hide("dm", "ldx"), run_time=0.3)
        self.until(125.6)
        eq = mt(r"\int x\,dm", "=", "Mx_{CM}", "=", "0", size=56, w=6.0, colors={0: MAGENTA, 4: CYAN}
                ).move_to([0, -1.7, 0])
        self.play(FadeIn(eq[0], shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(eq[1:3], shift=UP * 0.1), Indicate(self.lcm_t, color=WHITE, scale_factor=1.3), run_time=1.0)
        self.until(128.4)
        self.play(FadeIn(eq[3:5], shift=UP * 0.1), self.sgk.animate.set_value(0.0), run_time=1.2)
        why = text("origem escolhida no CM", 30, CYAN).move_to([0, -2.7, 0])
        self.play(FadeIn(why, shift=UP * 0.1), run_time=0.6)
        self.until(131.0)
        # só agora o termo cruzado vira zero; a identidade e o gráfico saem logo em seguida
        E6 = mt("I'", "=", "I_{CM}", "-", "2", "d", r"\cdot", "0", "+", "Md^2", size=52, w=6.6,
                colors={2: CYAN, 3: MAGENTA, 4: MAGENTA, 5: MAGENTA, 7: CYAN, 9: VIOLET}).move_to([0, 0.5, 0])
        self.swap(self.E5, E6, 0.4, 0.6, extra_out=(FadeOut(self.rb2),))
        self.E6 = E6
        self.until(132.8)
        self.play(FadeOut(eq), FadeOut(why), *self.hide("sg"), run_time=0.7)
        self.until(135.0)

    # ── BLOCO 11 · 135–142,5 s · Teorema dos Eixos Paralelos ────────────────
    def b11(self):
        self.seg(0, 1, 0.5, 1.5)
        F = mt("I'", "=", "I_{CM}", "+", "Md^2", size=76, w=6.4, colors={2: CYAN, 4: VIOLET}).move_to([0, 0.4, 0])
        self.swap(self.E6, F, 0.4, 0.6)
        self.F = F
        self.Fbox = box(F, WHITE)
        c1 = text("Teorema dos Eixos Paralelos", 34, CYAN).move_to([0, -1.0, 0])
        c2 = text2("eixos paralelos", "um passa pelo CM • distância d", 30).move_to([0, -2.2, 0])
        self.play(Create(self.Fbox), FadeIn(c1, shift=UP * 0.1), FadeIn(c2, shift=UP * 0.1), run_time=0.9)
        self.c11 = VGroup(c1, c2)
        self.until(142.0)

    # ── BLOCO 12 · 142,5–154 s · o eixo vai à ponta: d = L/2 ────────────────
    def b12(self):
        self.seg(0, 1, 0.5, 1.5)
        self.play(FadeOut(self.c11), FadeOut(self.Fbox), run_time=0.5)
        H1 = mt("I_{\\rm ponta}", "=", "I_{CM}", "+", r"M\left(\frac L2\right)^2", size=52, w=6.0,
                colors={2: CYAN, 4: VIOLET}).move_to([0, 0.6, 0])
        self.play(FadeOut(self.F), run_time=0.4)
        self.play(self.axx.animate.set_value(HALF), *self.hide("rdl"), *self.show("lcap"),
                  FadeIn(H1), run_time=2.4, rate_func=smooth)
        self.until(146.4)
        H2 = mt("I_{\\rm ponta}", "=", r"\frac1{12}ML^2", "+", r"\frac14ML^2", size=52, w=6.2,
                colors={2: CYAN, 4: VIOLET}).move_to([0, 0.6, 0])
        self.swap(H1, H2, 0.4, 0.6)
        self.until(148.4)
        # só a fração muda: 1/4 → 3/12
        H3 = mt("I_{\\rm ponta}", "=", r"\frac1{12}ML^2", "+", r"\frac3{12}ML^2", size=52, w=6.2,
                colors={2: CYAN, 4: VIOLET}).align_to(H2, LEFT).align_to(H2, UP)
        self.swap_tail(H2, H3, 4, 0.4, 0.6)
        self.until(150.4)
        H5 = mt("I_{\\rm ponta}", "=", r"\frac4{12}ML^2", "=", r"\frac13ML^2", size=60, w=6.6, colors={4: CYAN}
                ).move_to([0, 0.6, 0])
        self.swap(H3, H5, 0.4, 0.6)
        self.H5 = H5
        self.until(153.8)

    # ── BLOCO 13 · 154–161 s · fechamento: 1 bloco × 4 blocos ───────────────
    def b13(self):
        self.seg(0, 1, 0.5, 1.5)
        self.play(FadeOut(self.H5), *self.hide("rd", "lcap"), run_time=0.5)
        u, X0 = 0.95, -1.9
        # 1) define a unidade
        unit_blk = Rectangle(width=0.55, height=0.4, fill_color=CYAN, fill_opacity=0.85, stroke_width=0)
        unit = VGroup(text("cada bloco", 30), unit_blk, MathTex("=", font_size=46),
                      MathTex(r"\frac1{12}ML^2", font_size=52)).arrange(RIGHT, buff=0.25).move_to([0, 1.2, 0])
        self.play(FadeIn(unit, shift=DOWN * 0.1), run_time=0.7)
        self.until(156.4)
        self.play(FadeOut(unit), run_time=0.4)
        # 2) uma linha por momento de inércia: rótulo + valor pequeno, blocos abaixo
        labA = mt("I_{CM}", "=", r"\frac1{12}ML^2", size=44, w=4.6, colors={0: CYAN, 2: CYAN}).move_to([0, 1.5, 0])
        barA = Rectangle(width=u, height=0.55, fill_color=CYAN, fill_opacity=0.85, stroke_width=0
                         ).move_to([X0 + u / 2, 0.7, 0])
        labB = mt("I_{\\rm ponta}", "=", r"\frac4{12}ML^2", size=44, w=4.6, colors={0: WHITE, 2: CYAN}
                  ).move_to([0, -0.4, 0])
        segsB = VGroup(Rectangle(width=u, height=0.55, fill_color=CYAN, fill_opacity=0.85, stroke_width=0),
                       *[Rectangle(width=u, height=0.55, fill_color=VIOLET, fill_opacity=0.85, stroke_width=0)
                         for _ in range(3)])
        for i, sg in enumerate(segsB):
            sg.move_to([X0 + u / 2 + i * u, -1.2, 0])
        divs = VGroup(*[Line([X0 + i * u, -1.2 - 0.275, 0], [X0 + i * u, -1.2 + 0.275, 0], stroke_width=2,
                             color=BACKGROUND_COLOR) for i in range(1, 4)])
        self.play(FadeIn(labA, shift=DOWN * 0.1), FadeIn(barA), run_time=0.7)
        self.until(157.6)
        self.play(FadeIn(labB, shift=DOWN * 0.1),
                  LaggedStart(*[FadeIn(sg, shift=RIGHT * 0.15) for sg in segsB], lag_ratio=0.25), FadeIn(divs),
                  run_time=1.2)
        self.until(159.0)
        # 3) conclusão
        fin = mt("I_{\\rm ponta}", "=", "4", "I_{CM}", size=68, w=6.4, colors={3: CYAN}).move_to([0, -2.9, 0])
        self.finbox = box(fin, CYAN)
        self.play(FadeIn(VGroup(fin, self.finbox), shift=UP * 0.1), run_time=0.8)
        self.fin13 = VGroup(labA, barA, labB, segsB, divs, fin, self.finbox)
        self.until(161.2)

    # ── BLOCO 14 · síntese (sem barra) ──────────────────────────────────────
    def b14(self):
        self.seg(0, 1, 0.5, 1.5)
        self.play(FadeOut(self.fin13), FadeOut(self.bar),
                  *self.hide("axis", "cm", "lcm", "rd", "rdl", "lcap", "guides", "ring"), run_time=0.8)
        s1 = VGroup(MathTex(r"r_\perp^2", font_size=64, color=CYAN),
                    text2("a contribuição cresce com", "a distância ao quadrado", 30)).arrange(DOWN, buff=0.3
                                                                                                 ).move_to([0, 2.2, 0])
        s2 = VGroup(MathTex("Md^2", font_size=64, color=VIOLET),
                    text2("deslocar o eixo adiciona", "exatamente Md²", 30)).arrange(DOWN, buff=0.3
                                                                                      ).move_to([0, -0.9, 0])
        self.play(FadeIn(s1, shift=UP * 0.1), run_time=0.7)
        self.until(163.2)
        self.play(FadeIn(s2, shift=UP * 0.1), run_time=0.8)
        self.s14 = VGroup(s1, s2)
        self.until(166.0)

    # ── BLOCO 15 · CTA: só o símbolo e @labparallax ─────────────────────────
    def b15(self):
        self.seg(0, 1, 0.5, 1.5)
        icon = ImageMobject(str(ICON_PATH)).set_width(2.1).move_to([0, 0.4, 0])
        handle = text("@labparallax", 36, CYAN).move_to([0, -1.5, 0])
        self.play(FadeOut(self.s14), FadeIn(icon, scale=0.95), FadeIn(handle, shift=UP * 0.1), run_time=0.6)
        self.wait(1.4)
        self.play(FadeOut(icon), FadeOut(handle), run_time=0.4)
