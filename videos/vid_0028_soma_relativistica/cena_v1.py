"""vid_0028 — Soma relativística de velocidades (preview visual silencioso).

Curto vertical, Manim 2D. Física, arquitetura e hook congelados (handoff vid_0028, 2026-10-26).
Zonas fixas: cenário (foguetes, Terra) no terço superior, régua 0 → c → 2c no meio (marca de c sempre em
x = 0), equação embaixo, faixa inferior (y < -5,3) livre para a legenda. O movimento do cenário é integrado
quadro a quadro com as velocidades do referencial atual (self.vt); mudar de referencial só troca essas
velocidades, nunca a posição de nada.

Preview 540×960 / 15 fps:
    uv run --no-sync python -m manim -ql -r 540,960 --fps 15 videos/vid_0028_soma_relativistica/cena.py SomaRelativistica028
"""
from pathlib import Path
import json
import os
import sys
import numpy as np
from manim import *
from MF_Tools import TransformByGlyphMap

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

UNIT = Path(__file__).absolute().parent
config.media_dir = os.environ.get('MEDIA_DIR', str(UNIT / 'media'))
config.background_color = BACKGROUND_COLOR

# ── paleta (handoff §4) ─────────────────────────────────────────────────────────────────────────────────────
VEL = '#9C8CFF'     # só velocidade: setas, v_A, v_B, v_B', valores
GEO = '#B8C4DA'     # régua, marcas, colchete, chão
STEEL = '#7A8696'   # foguetes, carros, estação
DIM = '#8FA3C4'     # texto secundário, chips
ICE = TEXT_COLOR    # c (letra e marca da régua)
PANEL = '#0E1A33'
CYAN, PINK = PRIMARY_COLOR, '#EA63FF'   # só no degradê do cartão final (como no vid_0024/0027)

# ── layout (y) ──────────────────────────────────────────────────────────────────────────────────────────────
Y_TAG, Y_VLAB, Y_VARR, Y_ROCK = 6.5, 5.62, 5.12, 4.55
Y_GROUND, Y_TERRA, Y_EARR = 3.32, 3.06, 2.7
RUL_Y, RX0, RU = .75, -3.6, 3.6          # régua: x(v) = RX0 + RU·v/c  → c em x = 0
Y_EQ, Y_N1, Y_N2 = -1.75, -3.45, -4.45
Y_C4 = -1.0                              # equação principal da C04   # equação, notas; nada abaixo de -5,3
K, ALEN = .45, 1.25                      # deslocamento (unid./s por c) e comprimento da seta (unid. por c)
NOSE = .8


def RX(v):
    return RX0 + RU * v


FORMULAS = {  # tex, nº de glifos, {cor: índices}; o resto em branco (inclui todo c)
    'dx': (r"dx'=\gamma(dx-v_A\,dt)", 14, {VEL: [9, 10]}),
    'dt': (r"dt'=\gamma\left(dt-\frac{v_A\,dx}{c^2}\right)", 17, {VEL: [9, 10]}),
    'v0': (r"v_B'=\frac{dx'}{dt'}", 11, {VEL: [0, 1, 2]}),
    'v1': (r"v_B'=\frac{\gamma(dx-v_A\,dt)}{\gamma\left(dt-\frac{v_A\,dx}{c^2}\right)}", 28,
           {VEL: [0, 1, 2, 9, 10, 20, 21]}),
    'v2': (r"v_B'=\frac{dx-v_A\,dt}{dt-\frac{v_A\,dx}{c^2}}", 22, {VEL: [0, 1, 2, 7, 8, 15, 16]}),
    'v2b': (r"v_B'=\frac{(dx-v_A\,dt)/dt}{\left(dt-\frac{v_A\,dx}{c^2}\right)/dt}", 32,
            {VEL: [0, 1, 2, 8, 9, 21, 22]}),
    'v3': (r"v_B'=\frac{\frac{dx}{dt}-v_A}{1-\frac{v_A}{c^2}\frac{dx}{dt}}", 25, {VEL: [0, 1, 2, 10, 11, 15, 16]}),
    'v4': (r"v_B'=\frac{v_B-v_A}{1-\frac{v_Av_B}{c^2}}", 19, {VEL: [0, 1, 2, 4, 5, 7, 8, 12, 13, 14, 15]}),
    'vB': (r"v_B=\frac{dx}{dt}", 8, {VEL: [0, 1]}),
    'S1': (r"v_B'=\frac{(-0{,}8c)-(+0{,}8c)}{1-\frac{(+0{,}8c)(-0{,}8c)}{c^2}}", 39,
           {VEL: [0, 1, 2, 5, 6, 7, 8, 13, 14, 15, 16, 23, 24, 25, 26, 30, 31, 32, 33]}),
    'S2': (r"v_B'=\frac{-1{,}6c}{1-\frac{(+0{,}8c)(-0{,}8c)}{c^2}}", 29,
           {VEL: [0, 1, 2, 4, 5, 6, 7, 13, 14, 15, 16, 20, 21, 22, 23]}),
    'S2b': (r"v_B'=\frac{-1{,}6c}{1-\frac{-0{,}64\,c^2}{c^2}}", 22, {VEL: [0, 1, 2, 4, 5, 6, 7]}),
    'S3': (r"v_B'=\frac{-1{,}6c}{1-(-0{,}64)}", 19, {VEL: [0, 1, 2, 4, 5, 6, 7]}),
    'S4': (r"v_B'=\frac{-1{,}6c}{1+0{,}64}", 16, {VEL: [0, 1, 2, 4, 5, 6, 7]}),
    'S5': (r"v_B'=\frac{-1{,}6c}{1{,}64}", 14, {VEL: [0, 1, 2, 4, 5, 6, 7]}),
    'S6': (r"v_B'=-\frac{1{,}6}{1{,}64}\,c", 14, {VEL: [0, 1, 2, 4, 5, 6, 7, 9, 10, 11, 12]}),
    'S7': (r"v_B'=-\frac{40}{41}\,c\approx-0{,}976\,c", 19, {VEL: [0, 1, 2, 4, 5, 6, 8, 9, 12, 13, 14, 15, 16, 17]}),
    'S8': (r"|v_B'|\approx0{,}976\,c", 12, {VEL: [1, 2, 3, 6, 7, 8, 9, 10]}),
    'G1': (r"\frac{|v_Av_B|}{c^2}\sim10^{-14}", 15, {VEL: [1, 2, 3, 4]}),
    'G2': (r"1-\frac{v_Av_B}{c^2}\approx1", 11, {VEL: [2, 3, 4, 5]}),
    'G3': (r"v_B'\approx v_B-v_A", 9, {VEL: [0, 1, 2, 4, 5, 7, 8]}),
    'H1': (r"|v_B'|=\frac{0{,}5c+0{,}5c}{1+0{,}25}=0{,}8\,c", 27, {VEL: [1, 2, 3, 6, 7, 8, 11, 12, 13, 23, 24, 25]}),
    'H2': (r"|v_B'|=\frac{0{,}99c+0{,}99c}{1+0{,}9801}\approx0{,}99995\,c", 35,
           {VEL: [1, 2, 3, 6, 7, 8, 9, 12, 13, 14, 15, 27, 28, 29, 30, 31, 32, 33]}),
    'hook': (r"0{,}8c+0{,}8c=\,?", 11, {VEL: [0, 1, 2, 5, 6, 7]}),
    'naive': (r"0{,}8c+0{,}8c=1{,}6c\,?", 15, {VEL: [0, 1, 2, 5, 6, 7, 10, 11, 12]}),
}


def words(content, y=0, size=28, color=TEXT_COLOR, x=0):
    pw, ph = config.pixel_width, config.pixel_height
    try:
        config.pixel_width = config.pixel_height = 4000
        mob = screen_text(content, size, color=color, oversample=2)
    finally:
        config.pixel_width, config.pixel_height = pw, ph
    if mob.width > 7.8:
        mob.scale_to_fit_width(7.8)
    return mob.move_to([x, y, 0]).set_z_index(40)


def tex(key, y=0, size=46, x=0):
    s, count, colors = FORMULAS[key]
    mob = MathTex(s, font_size=size, color=TEXT_COLOR)
    assert len(mob[0]) == count, (key, len(mob[0]), count)
    for ink, idx in colors.items():
        for i in idx:
            mob[0][i].set_color(ink)
    if mob.width > 7.6:
        mob.scale_to_fit_width(7.6)
    return mob.move_to([x, y, 0]).set_z_index(40)


def vtex(s, size=32):
    """Rótulo de velocidade: tudo violeta, exceto a letra c (sempre branca, último glifo)."""
    mob = MathTex(s, font_size=size, color=VEL)
    if s.endswith('c'):
        mob[0][-1].set_color(ICE)
    return mob.set_z_index(42)


def glyphs(eq, idx):
    return VGroup(*[eq[0][i] for i in idx])


def strikes(*groups, color=TEXT_COLOR):
    return VGroup(*[Line(g.get_corner(DL) + DL * .05, g.get_corner(UR) + UR * .05, color=color, stroke_width=2.6)
                    for g in groups]).set_z_index(45)


def chip(content, pad=(.2, .11), stroke=DIM):
    box = RoundedRectangle(corner_radius=.12, width=content.width + 2 * pad[0], height=content.height + 2 * pad[1],
                           stroke_color=stroke, stroke_width=1.3, stroke_opacity=.75,
                           fill_color=PANEL, fill_opacity=.8).move_to(content).set_z_index(content.z_index - 1)
    return VGroup(box, content)


def tag(name):
    return chip(words('REFERENCIAL: ' + name, 0, 20, DIM)).move_to([0, Y_TAG, 0])


def rocket(letter, facing):
    st = dict(fill_color=STEEL, fill_opacity=1, stroke_color=GEO, stroke_width=1.3)
    body = RoundedRectangle(corner_radius=.16, width=1.15, height=.42, **st)
    nose = Polygon([.5, .21, 0], [.8, 0, 0], [.5, -.21, 0], **st)
    fin1 = Polygon([-.36, .2, 0], [-.58, .2, 0], [-.72, .44, 0], [-.6, .44, 0], **st)
    fin2 = fin1.copy().flip(RIGHT, about_point=ORIGIN)
    nozzle = Polygon([-.57, .12, 0], [-.7, .17, 0], [-.7, -.17, 0], [-.57, -.12, 0], **st)
    shape = VGroup(fin1, fin2, nozzle, body, nose)
    if facing < 0:
        shape.flip(UP, about_point=ORIGIN)
    badge = chip(words(letter, 0, 19, TEXT_COLOR), pad=(.09, .05)).move_to(ORIGIN)
    return VGroup(shape, badge).set_z_index(20)


def car(letter, facing):
    st = dict(fill_color=STEEL, fill_opacity=1, stroke_color=GEO, stroke_width=1.3)
    body = RoundedRectangle(corner_radius=.1, width=1.3, height=.34, **st).shift(UP * .02)
    cabin = Polygon([-.38, .19, 0], [-.22, .44, 0], [.2, .44, 0], [.38, .19, 0], **st)
    wheels = VGroup(*[Circle(radius=.13, fill_color=PANEL, fill_opacity=1, stroke_color=GEO, stroke_width=1.3)
                      .move_to([x, -.17, 0]) for x in (-.4, .4)])
    shape = VGroup(cabin, body, wheels)
    if facing < 0:
        shape.flip(UP, about_point=ORIGIN)
    badge = chip(words(letter, 0, 17, TEXT_COLOR), pad=(.08, .04)).move_to([0, .03, 0])
    return VGroup(shape, badge).set_z_index(20)


class SomaRelativistica028(Scene):
    # ── tempo ────────────────────────────────────────────────────────────────────────────────────────────────
    def mark(self, name):
        self.events.append({'estado': name, 'segundos': round(self.time, 3)})
        print(f'ESTADO {name}: {self.time:.3f}s')

    def beat(self, name):
        if self.beats:
            self.beats[-1][2] = self.time
        self.beats.append([name, self.time, None])
        self.mark(name)

    # ── álgebra ──────────────────────────────────────────────────────────────────────────────────────────────
    def morph(self, source, target, *links, rt=1.6, extras=(), name=None):
        anim = TransformByGlyphMap(source, target, *links, auto_fade=True, auto_morph=False, printing=False)
        assert not anim.show_indices
        if name:
            self.mark(name + '_inicio')
        self.play(anim, *extras, run_time=rt, rate_func=smooth)
        self.remove(*source.get_family())
        self.remove(*target.get_family())
        self.add(target)
        if name:
            self.mark(name + '_fim')
        return target

    def assemble(self, target, pairs, fade=(), rt=1.6, extras=(), rings=()):
        """Glifos de outras expressões (ou da cena) navegam até target; o restante de target aparece."""
        if rings:
            marks = [SurroundingRectangle(r, buff=.06, corner_radius=.06, stroke_width=1.6,
                                          color=r.get_color()).set_z_index(44) for r in rings]
            self.play(*[Create(m) for m in marks], run_time=.35)
            extras = (*extras, *[FadeOut(m) for m in marks])
        movers, anims, used = [], [], set()
        for src, idx, *kw in pairs:
            c = src.copy()
            movers.append(c)
            anims.append(Transform(c, glyphs(target, idx).copy(), **(kw[0] if kw else {})))
            used |= set(idx)
        rest = VGroup(*[g for i, g in enumerate(target[0]) if i not in used])
        self.play(*anims, FadeIn(rest), *[FadeOut(m) for m in fade], *extras, run_time=rt, rate_func=smooth)
        self.remove(*movers, rest, *fade)
        self.add(target)
        return target

    # ── cenário dinâmico ─────────────────────────────────────────────────────────────────────────────────────
    def label_pos(self, key, mob):
        if key == 'E':
            v = self.vt['E'].get_value()
            side = -np.sign(v) if abs(v) > .01 else 1
            return np.array([self.x['E'].get_value() + side * (.42 + mob.width / 2), Y_EARR, 0])
        v = self.vt[key].get_value()
        return np.array([self.x[key].get_value() + .28 * np.sign(v), Y_VLAB, 0])

    def label(self, key, s):
        m = VGroup(vtex(s))
        m.add_updater(lambda g: g.move_to(self.label_pos(key, g)))
        m.update(0)
        return m

    def relabel(self, key, s, rt=.7, extras=()):
        new = self.label(key, s)
        old = self.labs.get(key)
        anims = [FadeIn(new, shift=UP * .05)]
        if old is not None:
            anims.append(FadeOut(old, shift=UP * .05))
        self.play(*anims, *extras, run_time=rt)
        self.labs[key] = new
        return new

    def arrow_of(self, key, v=None):
        v = self.vt[key].get_value() if v is None else v
        x = self.x[key].get_value()
        y = Y_EARR if key == 'E' else Y_VARR
        if abs(v) < .02:  # corpo parado: seta mínima invisível (sempre com pontos, para os fades)
            return Arrow([x, y, 0], [x + .01, y, 0], buff=0, color=VEL).set_opacity(0).set_z_index(22)
        return Arrow([x, y, 0], [x + ALEN * v, y, 0], buff=0, color=VEL, stroke_width=5.5,
                     max_tip_length_to_length_ratio=.3, max_stroke_width_to_length_ratio=12).set_z_index(22)

    def moving_arrow(self, key):
        return always_redraw(lambda: self.arrow_of(key))

    def transfer(self, src, dst, v_dst, s_dst, path_arc=-PI / 2, rt=1.8, extras=()):
        """A seta do corpo que passa a ficar parado muda de dono: o movimento passa para outro objeto."""
        ghost = self.arrow_of(src).copy()
        self.vt[src].set_value(0)
        self.add(ghost)
        target = self.arrow_of(dst, v_dst)
        keep = self.vt[dst].get_value()
        self.vt[dst].set_value(v_dst)
        new = self.label(dst, s_dst)
        self.vt[dst].set_value(keep)
        new.suspend_updating()
        olds = [m for m in (self.labs.pop(src, None), self.labs.pop(dst, None)) if m is not None]
        self.play(Transform(ghost, target, path_arc=path_arc), FadeIn(new), *[FadeOut(m) for m in olds], *extras,
                  run_time=rt)
        self.vt[dst].set_value(v_dst)
        self.remove(ghost)
        new.resume_updating()
        self.labs[dst] = new

    def show(self, *mobs, rt=.6, extras=()):
        """FadeIn em grupo; depois cada objeto volta a ser raiz própria (updaters rodam uma vez por quadro)."""
        for m in mobs:
            m.update(0)
        group = VGroup(*mobs)
        self.play(FadeIn(group), *extras, run_time=rt)
        self.remove(group)
        self.add(*mobs)

    def actors(self, a=rocket, letters=('A', 'B')):
        rA, rB = self.body('A', a(letters[0], 1)), self.body('B', a(letters[1], -1))
        return rA, rB, self.moving_arrow('A'), self.moving_arrow('B')

    def integrate(self, m, dt):
        if self.moving:
            for k in 'ABE':
                self.x[k].increment_value(self.vt[k].get_value() * K * dt)

    def build_world(self):
        rng = np.random.default_rng(28)
        star_base = np.c_[rng.uniform(-4.8, 4.8, 30), rng.uniform(3.6, 6.15, 30)]
        stars = VGroup(*[Dot(radius=rng.uniform(.018, .032), color=GEO, fill_opacity=rng.uniform(.25, .55))
                         for _ in range(30)]).set_z_index(-5)

        def place_stars(g):
            off = self.x['E'].get_value()
            for d, (x, y) in zip(g, star_base):
                d.move_to([(x + off + 4.8) % 9.6 - 4.8, y, 0])
        stars.add_updater(place_stars)
        place_stars(stars)
        ground = Line([-4.6, Y_GROUND, 0], [4.6, Y_GROUND, 0], color=GEO, stroke_width=1.8, stroke_opacity=.7)
        ticks = VGroup(*[Line(ORIGIN, DOWN * .13, color=GEO, stroke_width=1.5, stroke_opacity=.55) for _ in range(13)])

        def place_ticks(g):
            off = self.x['E'].get_value()
            for i, t in enumerate(g):
                t.move_to([(i * .75 + off + 4.875) % 9.75 - 4.875, Y_GROUND - .065, 0])
        ticks.add_updater(place_ticks)
        place_ticks(ticks)
        st = dict(fill_color=STEEL, fill_opacity=1, stroke_color=GEO, stroke_width=1.3)
        dome = AnnularSector(inner_radius=0, outer_radius=.32, angle=PI, **st)
        mast = Line([0, .3, 0], [0, .62, 0], color=GEO, stroke_width=2)
        dish = Arc(radius=.14, start_angle=-PI / 4, angle=-PI / 2, color=GEO, stroke_width=2).move_to([.06, .64, 0])
        station = VGroup(dome, mast, dish)
        name = words('TERRA', 0, 15, DIM)
        earth = VGroup(station, name)

        def place_earth(g):
            x = self.x['E'].get_value()
            g[0].move_to([x, Y_GROUND, 0], aligned_edge=DOWN)
            g[1].move_to([x, Y_TERRA, 0])
        earth.add_updater(place_earth)
        place_earth(earth)
        return stars, VGroup(ground, ticks), earth

    def body(self, key, mob):
        mob.add_updater(lambda m: m.move_to([self.x[key].get_value(), Y_ROCK, 0]))
        mob.update(0)
        return mob

    def bracket(self):
        def build():
            a = self.x['A'].get_value() + NOSE + .08
            b = self.x['B'].get_value() - NOSE - .08
            if b - a < .05:
                return VMobject()
            return VGroup(Line([a, Y_ROCK, 0], [b, Y_ROCK, 0], color=GEO, stroke_width=2.2),
                          Line([a, Y_ROCK - .16, 0], [a, Y_ROCK + .16, 0], color=GEO, stroke_width=2.2),
                          Line([b, Y_ROCK - .16, 0], [b, Y_ROCK + .16, 0], color=GEO, stroke_width=2.2)).set_z_index(18)
        return always_redraw(build)

    def place(self, xa, xb, xe=0.):
        self.x['A'].set_value(xa)
        self.x['B'].set_value(xb)
        self.x['E'].set_value(xe)

    # ── régua ────────────────────────────────────────────────────────────────────────────────────────────────
    def build_ruler(self):
        base = Line([RX(0) - .12, RUL_Y, 0], [RX(2) + .35, RUL_Y, 0], color=GEO, stroke_width=2.2)
        ticks = VGroup()
        for i in range(21):
            h = .16 if i % 5 == 0 else .08
            if i == 10:
                continue
            ticks.add(Line([RX(i / 10), RUL_Y, 0], [RX(i / 10), RUL_Y + h, 0], color=GEO, stroke_width=1.6,
                           stroke_opacity=.9 if i % 5 == 0 else .5))
        cmark = Line([RX(1), RUL_Y - .14, 0], [RX(1), RUL_Y + .42, 0], color=ICE, stroke_width=3.6)
        nums = VGroup(MathTex('0', font_size=30, color=GEO).move_to([RX(0), RUL_Y - .36, 0]),
                      MathTex('c', font_size=36, color=ICE).move_to([RX(1), RUL_Y - .38, 0]),
                      MathTex('2', 'c', font_size=30, color=GEO).move_to([RX(2), RUL_Y - .36, 0]))
        nums[2][1].set_color(ICE)
        unit = MathTex('|v|', font_size=28, color=DIM).move_to([RX(0) - .55, RUL_Y + .05, 0])
        ruler = VGroup(base, ticks, cmark, nums, unit).set_z_index(10)
        ruler.cmark = cmark
        return ruler

    def pointer(self, kind):
        tr = self.pr if kind == 'rel' else self.pc
        y = RUL_Y + (.3 if kind == 'rel' else 1.0)

        def build():
            v = tr.get_value()
            if v < .02:
                return VMobject()
            a, b = np.array([RX(0), y, 0]), np.array([RX(v), y, 0])
            if kind == 'rel':
                return Arrow(a, b, buff=0, color=VEL, stroke_width=7, max_tip_length_to_length_ratio=.25,
                             max_stroke_width_to_length_ratio=20).set_z_index(15)
            tip = Triangle(fill_color=VEL, fill_opacity=.55, stroke_width=0).scale(.12).rotate(-PI / 2).move_to(b + LEFT * .1)
            line = DashedLine(a, b + LEFT * .18, color=VEL, stroke_width=4, dash_length=.13, dashed_ratio=.55)
            return VGroup(line.set_stroke(opacity=.55), tip).set_z_index(14)
        return always_redraw(build)

    def ptr_label(self, kind, s, dim=False):
        tr = self.pr if kind == 'rel' else self.pc
        y = RUL_Y + (.68 if kind == 'rel' else 1.38)
        m = VGroup(vtex(s, 30))
        if dim:
            m.set_opacity(.6)
        m.add_updater(lambda g: g.move_to([min(RX(tr.get_value()), 4.35 - g.width / 2), y, 0]))
        m.update(0)
        return m

    def zoom_inset(self, v, lo=.94, hi=1.01):
        """Lupa sobre a marca de c: a seta para antes de c (sem parede, só a marca)."""
        cx, cy, w, h = 2.35, RUL_Y + 1.42, 3.3, 1.05
        box = RoundedRectangle(corner_radius=.12, width=w, height=h, stroke_color=GEO, stroke_width=1.2,
                               stroke_opacity=.6, fill_color=PANEL, fill_opacity=.95).move_to([cx, cy, 0])

        def X(u):
            return cx - w / 2 + .18 + (u - lo) / (hi - lo) * (w - .36)
        yb = cy - .2
        base = Line([X(lo), yb, 0], [X(hi), yb, 0], color=GEO, stroke_width=1.8)
        cm = Line([X(1), yb - .1, 0], [X(1), yb + .42, 0], color=ICE, stroke_width=3.2)
        clab = MathTex('c', font_size=34, color=ICE).next_to(cm, RIGHT, buff=.08).shift(UP * .12)
        arr = Arrow([X(lo) - .05, yb + .14, 0], [X(v), yb + .14, 0], buff=0, color=VEL, stroke_width=6,
                    max_tip_length_to_length_ratio=.22)
        ring = Circle(radius=.2, color=GEO, stroke_width=1.4, stroke_opacity=.7).move_to([RX(1) - .03, RUL_Y + .22, 0])
        link = DashedLine(ring.get_top() + RIGHT * .1, box.get_corner(DL) + RIGHT * .25, color=GEO, stroke_width=1.2,
                          dash_length=.07).set_stroke(opacity=.6)
        return VGroup(ring, link, box, base, cm, clab, arr).set_z_index(16)

    def ghost_tick(self, v):
        return Line([RX(v), RUL_Y - .02, 0], [RX(v), RUL_Y + .2, 0], color=VEL, stroke_width=3,
                    stroke_opacity=.55).set_z_index(12)

    def drop(self, *mobs, rt=.6, extras=()):
        mobs = [m for m in mobs if m is not None]
        for m in mobs:
            m.clear_updaters()
        empty = [m for m in mobs if not any(s.has_points() for s in m.get_family())]
        self.remove(*empty)
        mobs = [m for m in mobs if m not in empty]
        self.play(*[FadeOut(m) for m in mobs], *extras, run_time=rt)

    def swap_tag(self, tg, name, rt=1.0):
        new = tag(name)
        self.play(Transform(tg[0], new[0]), TransformMatchingShapes(tg[1], new[1]), run_time=rt)
        self.remove(tg, tg[0], tg[1], new[0], new[1])
        self.add(new)
        return new

    # ── cena ─────────────────────────────────────────────────────────────────────────────────────────────────
    def construct(self):
        self.events, self.beats = [], []
        self.x = {k: ValueTracker(0) for k in 'ABE'}
        self.vt = {k: ValueTracker(0) for k in 'ABE'}
        self.pr, self.pc = ValueTracker(0), ValueTracker(0)
        self.labs = {}
        self.moving = False
        mover = Mobject()
        mover.add_updater(self.integrate)
        self.add(mover)

        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.4).to_corner(UR, buff=.28).set_z_index(60)
        brand = words('DA EQUAÇÃO AO FENÔMENO · EP. 08', 0, 20, DIM).set_opacity(.75).to_corner(UL, buff=.4)
        self.add(wm, brand)
        stars, ground, earth = self.build_world()

        # C01 — hook: os dois em movimento uniforme; as setas quase se encontram; a soma não aparece.
        self.beat('C01_hook')
        self.place(-5.05, 5.05)
        self.vt['A'].set_value(.8)
        self.vt['B'].set_value(-.8)
        rA, rB, arA, arB = self.actors()
        self.labs['A'] = self.label('A', r'+0{,}8c')
        self.labs['B'] = self.label('B', r'-0{,}8c')
        self.add(stars, rA, rB, arA, arB, self.labs['A'], self.labs['B'])
        self.moving = True
        self.wait(1.6)
        hook = tex('hook', .9, 74)
        self.play(Write(hook), run_time=1.2)
        q = words('QUANTO A MEDE DE B?', -.55, 36)
        self.play(FadeIn(q, shift=UP * .1), run_time=.7)
        self.mark('C01_pergunta')
        self.wait(10 - self.time)
        self.moving = False
        self.mark('C01_fim')

        # C02 — mudança de referencial: A não freia; o mundo passa a se mover em relação a A.
        self.beat('C02_referencial')
        self.drop(hook, q, rA, rB, arA, arB, self.labs.pop('A'), self.labs.pop('B'), rt=.6)
        self.place(-3.3, 3.3)
        rA, rB, arA, arB = self.actors()
        arE = self.moving_arrow('E')
        self.labs['A'] = self.label('A', r'v_A=+0{,}8c')
        self.labs['B'] = self.label('B', r'v_B=-0{,}8c')
        tg = tag('TERRA')
        self.show(ground, earth, rA, rB, arA, arB, arE, self.labs['A'], self.labs['B'], tg, rt=.8)
        self.wait(.5)
        self.moving = True
        self.mark('C02_terra_movimento')
        self.wait(2.4)
        self.moving = False
        self.mark('C02_congela')
        self.wait(.9)
        tg = self.swap_tag(tg, 'FOGUETE A', rt=1.1)
        self.mark('C02_tag_foguete_A')
        self.transfer('A', 'E', -.8, r'-0{,}8c', path_arc=-PI * .55, rt=1.9)
        self.vt['B'].set_value(-40 / 41)
        self.relabel('B', r'v_B=\,?', rt=.8)
        self.mark('C02_mundo_ganha_seta')
        note = words('A EM REPOUSO · A TERRA SE MOVE PARA TRÁS', -.55, 24, DIM)
        self.play(FadeIn(note), run_time=.5)
        self.moving = True
        self.mark('C02_A_movimento')
        self.wait(3.0)
        self.moving = False
        q2 = words('B, MEDIDO POR A = ?', -.55, 36)
        self.play(FadeOut(note), FadeIn(q2, shift=UP * .08), run_time=.7)
        self.mark('C02_pergunta')
        self.wait(2.6)

        # C03 — onde o 1,6c está certo: a régua entra; o palpite é riscado; a taxa de fechamento fica na Terra.
        self.beat('C03_1_6c')
        ruler = self.build_ruler()
        self.play(FadeIn(ruler), q2.animate.scale(.8).move_to([0, Y_EQ + .95, 0]), run_time=.8)
        naive = tex('naive', Y_EQ, 52)
        glyphs(naive, [10, 11, 12, 13, 14]).set_opacity(.6)
        self.play(Write(naive), run_time=1.1)
        pc, pcl = self.pointer('cls'), self.ptr_label('cls', r'1{,}6c\,?', dim=True)
        self.add(pc)
        self.play(self.pc.animate.set_value(1.6), run_time=1.8, rate_func=linear)
        self.play(FadeIn(pcl), run_time=.4)
        self.mark('C03_palpite_passa_c')
        self.wait(1.0)
        cross = strikes(glyphs(naive, [10, 11, 12, 13, 14]))
        self.play(Create(cross), run_time=.5)
        self.wait(.5)
        self.drop(naive, cross, q2, pc, pcl, rt=.6)
        self.pc.set_value(0)
        self.mark('C03_palpite_riscado')
        tg = self.swap_tag(tg, 'TERRA')
        self.transfer('E', 'A', .8, r'v_A=+0{,}8c', path_arc=PI * .55, rt=1.6)
        self.vt['B'].set_value(-.8)
        self.relabel('B', r'v_B=-0{,}8c', rt=.6)
        br = self.bracket()
        close = VGroup(chip(words('NA TERRA', 0, 20, GEO), stroke=GEO), words('A SEPARAÇÃO FECHA A 1,6c', 0, 28))
        close.arrange(RIGHT, buff=.22).move_to([0, Y_EQ + .6, 0])
        self.show(br, close)
        self.moving = True
        self.mark('C03_fechamento_terra')
        self.wait(1.3)
        self.moving = False
        self.wait(1.0)
        but = words('MAS ISSO NÃO É O QUE A MEDE DE B', Y_EQ - .55, 28)
        self.play(FadeIn(but, shift=UP * .08), run_time=.6)
        self.mark('C03_nao_e_medida')
        self.wait(1.7)

        # C04 — origem da fórmula: ao mudar de referencial, espaço e tempo mudam juntos.
        self.beat('C04_derivacao')
        self.drop(rA, rB, arA, arB, arE, br, stars, ground, earth, *self.labs.values(), ruler, close, but, tg, rt=.8)
        self.labs = {}
        head = words('MUDAR O REFERENCIAL\nMUDA ESPAÇO E TEMPO', 5.75, 32)
        self.play(FadeIn(head, shift=DOWN * .08), run_time=.7)
        e1 = tex('dx', 3.9, 54, x=.55)
        e2 = tex('dt', 2.4, 54, x=.55)
        e2.align_to(e1, LEFT)
        l1 = words('ESPAÇO', 0, 18, DIM).next_to(e1, LEFT, buff=.35)
        l2 = words('TEMPO', 0, 18, DIM).next_to(e2, LEFT, buff=.35).align_to(l1, RIGHT)
        self.play(Write(e1), FadeIn(l1), run_time=1.4)
        self.wait(.3)
        self.play(Write(e2), FadeIn(l2), run_time=1.5)
        self.mark('C04_dx_dt_juntos')
        mix = VGroup(words('cada uma mistura', 0, 22, DIM), MathTex('dx', font_size=34), words('e', 0, 22, DIM),
                     MathTex('dt', font_size=34)).arrange(RIGHT, buff=.14).move_to([0, 1.25, 0])
        self.play(FadeIn(mix), Indicate(glyphs(e1, [6, 7, 11, 12]), color=GEO, scale_factor=1.12),
                  Indicate(glyphs(e2, [6, 7, 11, 12]), color=GEO, scale_factor=1.12), run_time=1.2)
        self.wait(1.1)
        eq = tex('v0', Y_C4, 66)
        self.play(FadeOut(mix), FadeIn(eq, shift=UP * .08), run_time=.7)
        self.mark('C04_razao')
        self.wait(.6)
        eq = self.assemble(tex('v1', Y_C4, 62),
                           [(glyphs(eq, [0, 1, 2, 3]), [0, 1, 2, 3]), (glyphs(eq, [7]), [14]),
                            (glyphs(e1, list(range(4, 14))), list(range(4, 14)), {'path_arc': -.4}),
                            (glyphs(e2, list(range(4, 17))), list(range(15, 28)), {'path_arc': .4})],
                           fade=[eq], rt=1.9, extras=(VGroup(e1, e2, l1, l2).animate.set_opacity(.35),))
        self.mark('C04_montada')
        self.wait(.8)
        g = glyphs(eq, [4, 15])
        rings = VGroup(*[Circle(radius=.27, color=GEO, stroke_width=2.4).move_to(m) for m in g]).set_z_index(45)
        self.play(g.animate.set_color(GEO), Create(rings), run_time=.7)
        self.wait(.3)
        sk = strikes(glyphs(eq, [4]), glyphs(eq, [15]))
        self.play(Create(sk), run_time=.4)
        self.mark('C04_gama_destacado')
        self.wait(.3)
        eq = self.morph(eq, tex('v2', Y_C4, 64),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([4, 5, 13], []), (list(range(6, 13)), list(range(4, 11))),
                        ([14], [11]), ([15, 16, 27], []), (list(range(17, 27)), list(range(12, 22))),
                        rt=1.6, extras=(FadeOut(rings), FadeOut(sk)), name='C04_gama_cancela')
        self.wait(.6)
        hint = VGroup(words('dividir em cima e embaixo por', 0, 22, DIM), MathTex('dt', font_size=34))
        hint.arrange(RIGHT, buff=.14).move_to([0, Y_C4 - 2.1, 0])
        self.play(FadeIn(hint), run_time=.5)
        eq = self.morph(eq, tex('v2b', Y_C4, 60),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([], [4]), (list(range(4, 11)), list(range(5, 12))),
                        ([], [12, 13, 14, 15]), ([11], [16]), ([], [17]), (list(range(12, 22)), list(range(18, 28))),
                        ([], [28, 29, 30, 31]), rt=1.4, name='C04_divide_dt')
        self.wait(.9)
        eq = self.morph(eq, tex('v3', Y_C4, 64),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([4, 12], []), ([5, 6], [4, 5]), ([13], [6]), ([14, 15], [7, 8]),
                        ([7], [9]), ([8, 9], [10, 11]), ([10, 11], []), ([16], [12]), ([17, 28], []),
                        ([18, 19], [13]), ([20], [14]), ([21, 22], [15, 16]), ([23, 24], [20, 21]), ([25], [17]),
                        ([26, 27], [18, 19]), ([29, 30, 31], [22, 23, 24]), rt=1.8, name='C04_distribui')
        self.wait(.5)
        vb = tex('vB', Y_C4 - 2.4, 48)
        vbox = SurroundingRectangle(vb, buff=.16, corner_radius=.1, color=VEL, stroke_width=1.6)
        self.play(FadeOut(hint), FadeIn(vb), Create(vbox),
                  glyphs(eq, [4, 5, 6, 7, 8, 20, 21, 22, 23, 24]).animate.set_color(VEL), run_time=.8)
        self.mark('C04_vB_dxdt')
        self.wait(.8)
        eq = self.morph(eq, tex('v4', Y_C4, 68),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([4, 5, 6, 7, 8], [4, 5]), ([9], [6]), ([10, 11], [7, 8]),
                        ([12], [9]), ([13], [10]), ([14], [11]), ([15, 16], [12, 13]), ([17], [16]), ([18, 19], [17, 18]),
                        ([20, 21, 22, 23, 24], [14, 15], {'path_arc': -.5}), rt=1.8, name='C04_resultado')
        box = SurroundingRectangle(eq, buff=.24, corner_radius=.12, color=TEXT_COLOR, stroke_width=1.8)
        self.play(Create(box), FadeOut(vb), FadeOut(vbox), run_time=.6)
        self.mark('C04_caixa')
        self.wait(1.6)

        # C05 — substituição: os valores viajam dos foguetes para a equação; a régua mostra o resultado.
        self.beat('C05_substituicao')
        self.place(-3.0, 3.0)
        self.vt['A'].set_value(.8)
        self.vt['B'].set_value(-.8)
        self.vt['E'].set_value(0)
        stars, ground, earth = self.build_world()
        rA, rB, arA, arB = self.actors()
        arE = self.moving_arrow('E')
        self.labs['A'] = self.label('A', r'v_A=+0{,}8c')
        self.labs['B'] = self.label('B', r'v_B=-0{,}8c')
        tg = tag('TERRA')
        ruler = self.build_ruler()
        eq_low = eq.copy().scale(.92).move_to([0, Y_EQ, 0])
        self.show(stars, ground, earth, rA, rB, arA, arB, arE, self.labs['A'], self.labs['B'], tg, ruler, rt=1.0,
                  extras=(FadeOut(head), FadeOut(VGroup(e1, e2, l1, l2)), FadeOut(box), Transform(eq, eq_low)))
        self.remove(eq)
        eq = eq_low
        self.add(eq)
        pc, pcl = self.pointer('cls'), self.ptr_label('cls', r'1{,}6c\,?', dim=True)
        self.pc.set_value(1.6)
        self.show(pc, pcl)
        self.wait(.4)
        la, lb = self.labs['A'][0], self.labs['B'][0]
        eq = self.assemble(tex('S1', Y_EQ, 58),
                           [(glyphs(eq, [0, 1, 2, 3]), [0, 1, 2, 3]), (glyphs(eq, [6]), [11]), (glyphs(eq, [9]), [19]),
                            (glyphs(eq, [10, 11]), [20, 21]), (glyphs(eq, [16, 17, 18]), [36, 37, 38]),
                            (lb[0][3:8], [5, 6, 7, 8, 9], {'path_arc': .5}),
                            (la[0][3:8], [13, 14, 15, 16, 17], {'path_arc': -.5}),
                            (la[0][3:8], [23, 24, 25, 26, 27], {'path_arc': -.5}),
                            (lb[0][3:8], [30, 31, 32, 33, 34], {'path_arc': .5})],
                           fade=[eq], rt=1.7, rings=(la[0][3:8], lb[0][3:8]))
        self.mark('C05_valores_viajam')
        self.wait(.8)
        eq = self.morph(eq, tex('S2', Y_EQ, 58),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([5, 11], [4]), ([6, 7, 8, 14, 15, 16], [5, 6, 7]), ([9, 17], [8]),
                        ([4, 10, 12, 13, 18], []), (list(range(19, 39)), list(range(9, 29))), rt=1.0,
                        name='C05_numerador')
        self.wait(.6)
        sign_note = MathTex(r'(+)\cdot(-)=(-)', font_size=38, color=TEXT_COLOR).move_to([0, Y_N1, 0])
        self.play(Indicate(glyphs(eq, [13, 20]), color=TEXT_COLOR, scale_factor=1.6), FadeIn(sign_note), run_time=1.0)
        self.wait(.4)
        eq = self.morph(eq, tex('S2b', Y_EQ, 58),
                        (list(range(12)), list(range(12))), ([13, 20], [12]), ([14, 15, 16, 21, 22, 23], [13, 14, 15, 16]),
                        ([17, 24], [17, 18]), ([12, 18, 19, 25], []), ([26], [19]), ([27], [20]), ([28], [21]),
                        rt=1.0, name='C05_produto_negativo')
        self.wait(.4)
        cc = strikes(glyphs(eq, [17, 18]), glyphs(eq, [20, 21]))
        self.play(Create(cc), run_time=.4)
        eq = self.morph(eq, tex('S3', Y_EQ, 60),
                        (list(range(12)), list(range(12))), ([], [12]), ([12], [13]), ([13, 14, 15, 16], [14, 15, 16, 17]),
                        ([17, 18, 19, 20, 21], []), ([], [18]), rt=1.0, extras=(FadeOut(cc),), name='C05_c2_cancela')
        self.wait(.3)
        sign_note2 = MathTex(r'-(-0{,}64)=+0{,}64', font_size=38, color=TEXT_COLOR).move_to([0, Y_N1, 0])
        self.play(FadeTransform(sign_note, sign_note2), Indicate(glyphs(eq, [11, 13]), color=TEXT_COLOR, scale_factor=1.5),
                  run_time=.9)
        sign_note = sign_note2
        eq = self.morph(eq, tex('S4', Y_EQ, 60),
                        (list(range(11)), list(range(11))), ([11, 13], [11]), ([12, 18], []),
                        ([14, 15, 16, 17], [12, 13, 14, 15]), rt=1.0, name='C05_1_mais_064')
        self.wait(.7)
        eq = self.morph(eq, tex('S5', Y_EQ, 60),
                        (list(range(11)), list(range(11))), ([11, 12], []), ([13], [11]), ([14], [12]), ([15], [13]),
                        rt=1.0, extras=(FadeOut(sign_note),), name='C05_164')
        self.wait(.4)
        eq = self.morph(eq, tex('S6', Y_EQ, 60),
                        ([0, 1, 2, 3], [0, 1, 2, 3]), ([4], [4]), ([5, 6, 7], [5, 6, 7]), ([8], [13], {'path_arc': -.6}),
                        ([9], [8]), ([10, 11, 12, 13], [9, 10, 11, 12]), rt=1.0)
        self.wait(.3)
        eq = self.morph(eq, tex('S7', Y_EQ, 58),
                        ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]), ([5, 6, 7], [5, 6]), ([8], [7]), ([9, 10, 11, 12], [8, 9]),
                        ([13], [10]), ([], list(range(11, 19)), {'delay': .5}), rt=1.3, name='C05_40_41')
        self.mark('C05_resultado_com_sinal')
        self.wait(.8)
        sense = VGroup(words('o sinal só indica o sentido', 0, 22, DIM),
                       Arrow(RIGHT * .35, LEFT * .35, buff=0, color=DIM, stroke_width=4, max_tip_length_to_length_ratio=.35))
        sense.arrange(RIGHT, buff=.2).move_to([0, Y_EQ - 1.1, 0])
        self.play(glyphs(eq, [4, 12]).animate.set_color(DIM).set_opacity(.45), FadeIn(sense), run_time=.8)
        mod = tex('S8', Y_N1 - .45, 62)
        mbox = SurroundingRectangle(mod, buff=.2, corner_radius=.12, color=VEL, stroke_width=2)
        self.play(FadeIn(mod, shift=UP * .1), Create(mbox), run_time=.9)
        self.mark('C05_modulo')
        self.wait(.3)
        pcl.clear_updaters()
        self.play(self.pc.animate.set_value(40 / 41), FadeOut(pcl), run_time=1.6, rate_func=smooth)
        pr, prl = self.pointer('rel'), self.ptr_label('rel', r'0{,}976c')
        self.pr.set_value(40 / 41)
        pr.update(0)
        prl.update(0)
        self.play(FadeOut(pc), FadeIn(pr), FadeIn(prl), run_time=.7)
        self.pc.set_value(0)
        lupa = self.zoom_inset(40 / 41)
        self.play(FadeIn(lupa), run_time=.6)
        self.mark('C05_regua_0976')
        self.wait(2.0)

        # C07 — limite clássico: carros a 30 m/s (a antiga C06 está incorporada na C05).
        self.beat('C07_limite_classico')
        self.drop(eq, sense, mod, mbox, pr, prl, lupa, ruler, rA, rB, arA, arB, self.labs.pop('A'), self.labs.pop('B'), rt=.7)
        self.pr.set_value(0)
        cA = car('A', 1).move_to([-2.4, Y_GROUND + .32, 0])
        cB = car('B', -1).move_to([2.4, Y_GROUND + .32, 0])
        kA = Arrow([-2.4, 4.3, 0], [-1.4, 4.3, 0], buff=0, color=VEL, stroke_width=5.5, max_tip_length_to_length_ratio=.3)
        kB = Arrow([2.4, 4.3, 0], [1.4, 4.3, 0], buff=0, color=VEL, stroke_width=5.5, max_tip_length_to_length_ratio=.3)
        tA = vtex(r'v_A=+30\ \mathrm{m/s}', 30).move_to([-2.1, 4.8, 0])
        tB = vtex(r'v_B=-30\ \mathrm{m/s}', 30).move_to([2.1, 4.8, 0])
        self.play(FadeIn(VGroup(cA, cB)), GrowArrow(kA), GrowArrow(kB), FadeIn(tA), FadeIn(tB), run_time=.9)
        self.wait(.6)
        g1 = tex('G1', .9, 56)
        self.play(FadeIn(g1, shift=UP * .08), run_time=.8)
        self.mark('C07_1e-14')
        self.wait(1.2)
        g2 = tex('G2', -.7, 52)
        self.play(FadeIn(g2, shift=UP * .08), run_time=.8)
        self.wait(1.4)
        g3 = tex('G3', -2.3, 58)
        g3box = SurroundingRectangle(g3, buff=.2, corner_radius=.12, color=TEXT_COLOR, stroke_width=1.8)
        self.play(FadeIn(g3, shift=UP * .08), Create(g3box), run_time=.9)
        self.mark('C07_galileu_formula')
        gal = words('GALILEU = LIMITE DE BAIXAS VELOCIDADES', -3.75, 27)
        self.play(FadeIn(gal), run_time=.6)
        self.wait(2.0)

        # C08 — aproximação de c: a mesma régua; passos cada vez menores, sem parede.
        self.beat('C08_aproximacao')
        self.drop(cA, cB, kA, kB, tA, tB, g1, g2, g3, g3box, gal, rt=.7)
        self.place(-3.0, 3.0)
        self.vt['A'].set_value(.5)
        self.vt['B'].set_value(-.5)
        rA, rB, arA, arB = self.actors()
        self.labs['A'] = self.label('A', r'v_A=+0{,}5c')
        self.labs['B'] = self.label('B', r'v_B=-0{,}5c')
        ruler = self.build_ruler()
        self.show(rA, rB, arA, arB, self.labs['A'], self.labs['B'], ruler, rt=.8)
        key_c = VGroup(DashedLine(LEFT * .35, RIGHT * .35, color=VEL, stroke_width=4, dash_length=.12).set_stroke(opacity=.55),
                       words('SOMA SIMPLES', 0, 20, DIM)).arrange(RIGHT, buff=.18)
        key_r = VGroup(Line(LEFT * .35, RIGHT * .35, color=VEL, stroke_width=6),
                       words('MEDIDO POR A', 0, 20, DIM)).arrange(RIGHT, buff=.18)
        keys = VGroup(key_c, key_r).arrange(RIGHT, buff=.6).move_to([0, -.75, 0])
        pc, pr = self.pointer('cls'), self.pointer('rel')
        self.add(pc, pr)
        self.play(FadeIn(keys), self.pc.animate.set_value(1.0), run_time=1.1)
        pcl = self.ptr_label('cls', r'1c\,?', dim=True)
        self.play(FadeIn(pcl), self.pr.animate.set_value(.8), run_time=1.1)
        prl = self.ptr_label('rel', r'0{,}8c')
        h1 = tex('H1', Y_EQ - .35, 52)
        self.play(FadeIn(prl), FadeIn(h1, shift=UP * .08), run_time=.7)
        self.mark('C08_estado1')
        self.wait(1.4)
        ticks = VGroup(self.ghost_tick(.8), self.ghost_tick(40 / 41))
        self.play(FadeIn(ticks), run_time=.4)
        self.relabel('A', r'v_A=+0{,}99c', rt=.6, extras=(self.vt['A'].animate.set_value(.99),))
        self.relabel('B', r'v_B=-0{,}99c', rt=.6, extras=(self.vt['B'].animate.set_value(-.99),))
        pcl.clear_updaters()
        self.play(FadeOut(pcl), self.pc.animate.set_value(1.98), FadeOut(h1), run_time=1.0)
        pcl = self.ptr_label('cls', r'1{,}98c\,?', dim=True)
        self.play(FadeIn(pcl), run_time=.3)
        prl.clear_updaters()
        self.play(FadeOut(prl), self.pr.animate.set_value(40 / 41), run_time=.9, rate_func=linear)
        self.play(self.pr.animate.set_value(.99995), run_time=1.3, rate_func=rate_functions.ease_out_cubic)
        prl = self.ptr_label('rel', r'0{,}99995c')
        h2 = tex('H2', Y_EQ - .35, 52)
        self.play(FadeIn(prl), FadeIn(h2, shift=UP * .08), run_time=.7)
        below = MathTex(r'0{,}99995\,c<c', font_size=40, color=TEXT_COLOR)
        below[0][:7].set_color(VEL)
        below.move_to([0, Y_N1 - .35, 0])
        self.play(FadeIn(below), run_time=.5)
        self.mark('C08_estado2')
        self.wait(1.8)

        # C09 — síntese em estados sequenciais: Terra → A → B (os chips trocam de papel).
        self.beat('C09_sintese')
        self.vt['A'].set_value(.8)
        self.vt['B'].set_value(-.8)
        self.drop(pc, pcl, keys, h2, below, ticks, prl, self.labs.pop('A'), self.labs.pop('B'), rt=.6,
                  extras=(self.pr.animate.set_value(.8),))
        self.pc.set_value(0)
        self.labs['A'] = self.label('A', r'+0{,}8c')
        self.labs['B'] = self.label('B', r'-0{,}8c')
        prl = self.ptr_label('rel', r'0{,}8c')
        br = self.bracket()
        close = VGroup(chip(words('NA TERRA', 0, 20, GEO), stroke=GEO), words('SEPARAÇÃO FECHA A 1,6c', 0, 28))
        close.arrange(RIGHT, buff=.22).move_to([0, -.75, 0])
        self.show(self.labs['A'], self.labs['B'], br, prl, close, rt=.7)
        self.moving = True
        self.mark('C09_estado_terra')
        self.wait(1.6)
        self.moving = False
        self.wait(.3)
        self.drop(br, close, rt=.4)
        tg = self.swap_tag(tg, 'FOGUETE A', rt=.7)
        self.transfer('A', 'E', -.8, r'-0{,}8c', path_arc=-PI * .55, rt=1.2)
        self.vt['B'].set_value(-40 / 41)
        prl.clear_updaters()
        self.relabel('B', r'0{,}976c', rt=.8, extras=(self.pr.animate.set_value(40 / 41), FadeOut(prl)))
        prl = self.ptr_label('rel', r'0{,}976c')
        self.show(prl, rt=.3)
        self.moving = True
        self.mark('C09_estado_A')
        self.wait(1.3)
        self.moving = False
        self.wait(.3)
        tg = self.swap_tag(tg, 'FOGUETE B', rt=.7)
        old_e = self.labs.pop('E')
        old_e.clear_updaters()
        self.transfer('B', 'A', 40 / 41, r'0{,}976c', path_arc=PI * .45, rt=1.2,
                      extras=(self.vt['E'].animate.set_value(.8), FadeOut(old_e)))
        self.labs['E'] = self.label('E', r'+0{,}8c')
        each = words('CADA UM MEDE O OUTRO A 0,976c', -.75, 30)
        self.show(self.labs['E'], each)
        self.moving = True
        self.mark('C09_estado_B')
        self.wait(1.3)
        self.moving = False
        self.wait(.8)
        f1 = VGroup(words('CORPOS COM MASSA:', 0, 32), MathTex('v<c', font_size=52, color=TEXT_COLOR)).arrange(RIGHT, buff=.25)
        f1[1][0][0].set_color(VEL)
        f1.move_to([0, Y_EQ - .5, 0])
        f2 = words('PERTO DE c, VELOCIDADES NÃO SE SOMAM.\nELAS SE ACUMULAM SEM CHEGAR A c.', Y_N1 - .4, 30)
        self.play(FadeOut(each), FadeIn(f1, shift=UP * .08), run_time=.8)
        self.wait(.8)
        self.play(FadeIn(f2, shift=UP * .08), run_time=.8)
        self.mark('C09_fecho')
        self.wait(2.6)

        # C10 — cartão final, separado do fecho físico: somente o handle.
        self.beat('C10_fechamento')
        self.moving = False
        for m in list(self.mobjects):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m is not mover], run_time=.6)
        self.clear()
        self.wait(.3)
        handle = words('@labparallax', 0, 48).set_color_by_gradient(CYAN, VEL, PINK)
        self.play(FadeIn(handle, scale=.96), run_time=.7)
        self.mark('C10_handle')
        self.wait(1.5)
        self.play(FadeOut(handle), run_time=.5)
        self.wait(.4)
        self.beats[-1][2] = self.time
        self.mark('fim')
        for name, a, b in self.beats:
            print(f'[tempo] {name}: {a:6.1f} s -> {b:6.1f} s ({b - a:5.1f} s)')
        out = Path(config.media_dir) / 'estados_vid0028.json'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({'eventos': self.events, 'beats': [{'beat': n, 'inicio': round(a, 2), 'fim': round(b, 2)}
                                                                     for n, a, b in self.beats],
                                   'duracao': round(self.time, 2)}, ensure_ascii=False, indent=1), encoding='utf-8')
