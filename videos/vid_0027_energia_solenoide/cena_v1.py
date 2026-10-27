"""vid_0027 — Onde fica a energia de um indutor? (preview visual silencioso).

Curto vertical, Manim 2D. Solenoide longo em corte longitudinal (meia seção de trás): ⊙ na parede superior,
⊗ na inferior, corrente subindo pela meia volta de trás em traços verdes. Ampère → B; disco de fluxo → Φ;
o disco se replica ao longo de h → NΦ; L = NΦ/I; energia pelo circuito (fixada no topo) e pelo campo
(volume aceso), que se reencontram. Cartão final com @labparallax.

Preview 540×960 / 15 fps:
    uv run --no-sync python -m manim -ql -r 540,960 --fps 15 videos/vid_0027_energia_solenoide/cena.py EnergiaSolenoide027
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
CUR = '#3FE08B'     # corrente I
FLD = '#EA63FF'     # B, Φ, NΦ, U_B, u_B
GEO = '#B8C4DA'     # a, h, A, V, n, laço amperiano
STEEL = '#7A8696'   # espiras
DIM = '#8FA3C4'     # texto secundário, chips
WHITE_ = TEXT_COLOR
CYAN, VIOLET, PINK = PRIMARY_COLOR, '#9C8CFF', '#EA63FF'   # só no degradê do cartão final (como no vid_0024)

# ── palco: corte longitudinal, eixo horizontal ──────────────────────────────────────────────────────────────
YC, A_R, P = 2.9, 1.15, .52                 # eixo, raio desenhado, passo entre espiras
BOTTOMS = -4.03 + P * np.arange(16)         # ⊗ (parede inferior)
TOPS = BOTTOMS + P / 2                      # ⊙ (parede superior): meia volta depois
H0, H1 = -2.34, 2.34                        # trecho h
DISKS = np.linspace(H0, H1, 7)              # cópias do disco (estilizado: N não é o n real)
COLS = H0 + 1.4 * np.arange(-1, 5)          # colunas das setas de B (uma atravessa o disco em H0)
SPC, DASH, VFLOW = .55, .11, .5             # traços da corrente: espaçamento, meio-comprimento, velocidade
LAYOUT = {'title': 6.1, 'pin': 6.15, 'pin_label': 6.75, 'eq': -1.9, 'row2': -2.95, 'row3': -3.85}

FORMULAS = {  # tex, nº de glifos, {cor: índices}
    'amp': (r'B\ell=\mu_0(n\ell)I', 10, {FLD: [0], GEO: [1, 6, 7], CUR: [9]}),
    'B': (r'B=\mu_0nI', 6, {FLD: [0], GEO: [4], CUR: [5]}),
    'phiBA': (r'\Phi=BA', 4, {FLD: [0, 2], GEO: [3]}),
    'phi': (r'\Phi=\mu_0nI\pi a^2', 9, {FLD: [0], GEO: [4, 7, 8], CUR: [5]}),
    'A': (r'A=\pi a^2', 5, {GEO: [0, 3, 4]}),
    'N': (r'N=nh', 4, {GEO: [2, 3]}),
    'nphi1': (r'N\Phi=(nh)(\mu_0nI\pi a^2)', 16, {FLD: [0, 1], GEO: [4, 5, 10, 13, 14], CUR: [11]}),
    'nphi': (r'N\Phi=\mu_0n^2I\pi a^2h', 12, {FLD: [0, 1], GEO: [5, 6, 9, 10, 11], CUR: [7]}),
    'L0': (r'L=\frac{N\Phi}{I}', 6, {FLD: [2, 3], CUR: [5]}),
    'L1': (r'L=\frac{\mu_0n^2I\pi a^2h}{I}', 13, {GEO: [4, 5, 8, 9, 10], CUR: [6, 12]}),
    'L': (r'L=\mu_0n^2\pi a^2h', 10, {GEO: [4, 5, 7, 8, 9]}),
    'U0': (r'U_B=\frac{1}{2}LI^2', 9, {FLD: [0, 1], CUR: [7, 8]}),
    'U1': (r'U_B=\frac{1}{2}\mu_0n^2\pi a^2hI^2', 16, {FLD: [0, 1], GEO: [8, 9, 11, 12, 13], CUR: [14, 15]}),
    'u': (r'u_B=\frac{B^2}{2\mu_0}', 9, {FLD: [0, 1, 3, 4]}),
    'V': (r'V=\pi a^2h', 6, {GEO: [0, 3, 4, 5]}),
    'E1': (r'U_B=u_BV', 6, {FLD: [0, 1, 3, 4], GEO: [5]}),
    'E2': (r'U_B=\frac{B^2}{2\mu_0}\pi a^2h', 13, {FLD: [0, 1, 3, 4], GEO: [10, 11, 12]}),
    'E3': (r'U_B=\frac{(\mu_0nI)^2}{2\mu_0}\pi a^2h', 18, {FLD: [0, 1], GEO: [6, 15, 16, 17], CUR: [7]}),
    'E4': (r'U_B=\frac{\mu_0\mu_0n^2I^2}{2\mu_0}\pi a^2h', 19, {FLD: [0, 1], GEO: [7, 8, 16, 17, 18], CUR: [9, 10]}),
    'E5': (r'U_B=\frac{\mu_0n^2I^2}{2}\pi a^2h', 15, {FLD: [0, 1], GEO: [5, 6, 12, 13, 14], CUR: [7, 8]}),
}


def edge(x):
    """Opacidade nas pontas do desenho: o solenoide continua além do quadro (muito longo)."""
    return float(np.clip((4.25 - abs(x)) / 1.1, 0, 1))


def words(content, y, size=28, color=WHITE_, x=0):
    pw, ph = config.pixel_width, config.pixel_height
    try:
        config.pixel_width = config.pixel_height = 4000
        mob = screen_text(content, size, color=color, oversample=2)
    finally:
        config.pixel_width, config.pixel_height = pw, ph
    if mob.width > 7.6:
        mob.scale_to_fit_width(7.6)
    return mob.move_to([x, y, 0]).set_z_index(40)


def tex(key, y=LAYOUT['eq'], size=50, x=0):
    s, count, colors = FORMULAS[key]
    mob = MathTex(s, font_size=size, color=WHITE_)
    assert len(mob[0]) == count, (key, len(mob[0]), count)
    for ink, idx in colors.items():
        for i in idx:
            mob[0][i].set_color(ink)
    if mob.width > 7.6:
        mob.scale_to_fit_width(7.6)
    return mob.move_to([x, y, 0]).set_z_index(40)


def sym(s, color, size=38):
    return MathTex(s, font_size=size, color=color).set_z_index(40)


def chip(content, pad=(.22, .13)):
    box = RoundedRectangle(corner_radius=.12, width=content.width + 2 * pad[0], height=content.height + 2 * pad[1],
                           stroke_color=DIM, stroke_width=1.3, stroke_opacity=.6,
                           fill_color=BACKGROUND_COLOR, fill_opacity=.85).move_to(content).set_z_index(39)
    return VGroup(box, content)


def glyphs(eq, idx):
    return VGroup(*[eq[0][i] for i in idx])


def strikes(*groups):
    return VGroup(*[Line(g.get_corner(DL) + DL * .05, g.get_corner(UR) + UR * .05, color=WHITE_, stroke_width=2.6)
                    for g in groups]).set_z_index(45)


class EnergiaSolenoide027(Scene):
    # ── tempo ────────────────────────────────────────────────────────────────────────────────────────────────
    def mark(self, name):
        self.events.append({'estado': name, 'segundos': round(self.time, 3)})
        print(f'ESTADO {name}: {self.time:.3f}s')

    def beat(self, name):
        if self.beats:
            self.beats[-1][2] = self.time
        self.beats.append([name, self.time, None])
        self.mark(name)

    def pad(self, until):
        """Respiro até o fim-alvo do beat (tempo absoluto); a voz ajusta depois."""
        if until - self.time > .02:
            self.wait(until - self.time)

    # ── álgebra ──────────────────────────────────────────────────────────────────────────────────────────────
    def morph(self, target, *links, rt=1.4, extras=(), name=None):
        source = self.eq
        anim = TransformByGlyphMap(source, target, *links, auto_fade=True, auto_morph=False, printing=False)
        assert not anim.show_indices
        if name:
            self.mark(name + '_inicio')
        self.play(anim, *extras, run_time=rt)
        self.remove(*source.get_family())
        self.remove(*target.get_family())
        self.add(target)
        self.eq = target
        if name:
            self.mark(name + '_fim')

    def fly(self, eq, pairs, rt=1.3, extras=()):
        """Variáveis navegam da cena (ou de outra equação) para os glifos de eq; o resto entra por fade."""
        movers, anims, used = [], [], set()
        for src, idx in pairs:
            c = src.copy()
            movers.append(c)
            anims.append(Transform(c, glyphs(eq, idx).copy()))
            used |= set(idx)
        rest = VGroup(*[g for i, g in enumerate(eq[0]) if i not in used])
        self.play(*anims, FadeIn(rest), *extras, run_time=rt)
        self.remove(*movers, rest)
        self.add(eq)
        return eq

    # ── palco ────────────────────────────────────────────────────────────────────────────────────────────────
    def build_solenoid(self):
        back = VGroup()
        for xb, xt in zip(BOTTOMS, TOPS):
            back.add(Line([xb, YC - A_R + .13, 0], [xt, YC + A_R - .13, 0], color=STEEL,
                          stroke_width=1.6, stroke_opacity=.42 * edge((xb + xt) / 2)))
        tops, bots = VGroup(), VGroup()
        for xt in TOPS:
            o = edge(xt)
            ring = Circle(radius=.13, color=STEEL, stroke_width=2.6, stroke_opacity=o,
                          fill_color=BACKGROUND_COLOR, fill_opacity=1).move_to([xt, YC + A_R, 0])
            dot = Dot([xt, YC + A_R, 0], radius=.042, color=CUR, fill_opacity=o)
            tops.add(VGroup(ring, dot))
        for xb in BOTTOMS:
            o = edge(xb)
            c = np.array([xb, YC - A_R, 0])
            ring = Circle(radius=.13, color=STEEL, stroke_width=2.6, stroke_opacity=o,
                          fill_color=BACKGROUND_COLOR, fill_opacity=1).move_to(c)
            cross = VGroup(Line(c + [-.065, -.065, 0], c + [.065, .065, 0]),
                           Line(c + [-.065, .065, 0], c + [.065, -.065, 0])).set_stroke(CUR, 2.2, o)
            bots.add(VGroup(ring, cross))
        back.set_z_index(-2)
        tops.set_z_index(6)
        bots.set_z_index(6)
        self.back, self.tops, self.bots = back, tops, bots
        return VGroup(back, tops, bots)

    def build_flow(self):
        """Corrente: traços verdes subindo pela meia volta de trás (⊗ embaixo → ⊙ em cima), velocidade ∝ I."""
        g = VGroup().set_z_index(3)
        g.ph = 0.0
        segs = [(np.array([xb, YC - A_R + .15, 0]), np.array([xt, YC + A_R - .15, 0])) for xb, xt in zip(BOTTOMS, TOPS)]

        def upd(m, dt):
            m.ph = (m.ph + dt * VFLOW * self.current.get_value()) % SPC
            o = self.flow_op.get_value()
            marks = []
            if o > .01:
                for a, b in segs:
                    L = np.linalg.norm(b - a)
                    u = (b - a) / L
                    oe = o * edge((a[0] + b[0]) / 2)
                    if oe < .02:
                        continue
                    for s in np.arange(m.ph, L, SPC):
                        s0, s1 = max(0, s - DASH), min(L, s + DASH)
                        if s1 - s0 < .03:
                            continue
                        mid = a + u * s
                        tail = Line(a + u * s0, mid).set_stroke(CUR, 4.2, .45 * oe)
                        head = Line(mid, a + u * s1).set_stroke(CUR, 4.2, oe)
                        marks.append(VGroup(tail, head))
            m.submobjects = marks
        g.add_updater(upd)
        return g

    def build_field(self):
        arrows = VGroup()
        for y in (YC - .5, YC, YC + .5):
            for c in COLS:
                o = edge(c)
                if o < .05:
                    continue
                arrows.add(Arrow([c - .45, y, 0], [c + .45, y, 0], buff=0, color=FLD, stroke_width=3.4,
                                 max_tip_length_to_length_ratio=.24, max_stroke_width_to_length_ratio=8)
                           .set_opacity(.9 * o))
        return arrows.set_z_index(8)

    def disk(self, x, width=.62):
        return Ellipse(width=width, height=2 * A_R - .14, stroke_color=GEO, stroke_width=2,
                       fill_color=GEO, fill_opacity=.17).move_to([x, YC, 0]).set_z_index(7)

    def glow(self):
        strips = VGroup()
        xs = np.linspace(-4.5, 4.5, 91)
        for a, b in zip(xs[:-1], xs[1:]):
            o = edge((a + b) / 2)
            strips.add(Rectangle(width=b - a + .005, height=2 * A_R - .26, stroke_width=0, fill_color=FLD,
                                 fill_opacity=.24 * o).move_to([(a + b) / 2, YC, 0]))
        return strips.set_z_index(1)

    # ── cena ─────────────────────────────────────────────────────────────────────────────────────────────────
    def construct(self):
        self.events, self.beats = [], []
        self.eq = VGroup()
        self.current = ValueTracker(1)
        self.flow_op = ValueTracker(0)
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.4).to_corner(UR, buff=.28).set_z_index(60)
        tag = words('EXERCÍCIO RESOLVIDO · EP. 10', 0, 20, DIM).set_opacity(.75).to_corner(UL, buff=.4)
        self.add(wm, tag)

        solenoid = self.build_solenoid()
        flow = self.build_flow()
        field = self.build_field()
        I_lab = sym('I', CUR, 36).move_to([TOPS[1], YC + A_R + .48, 0])
        B_lab = sym('B', FLD, 36).move_to([COLS[-1] + .05, YC + .78, 0])

        # C01 — hook: duas apostas, sem resposta.
        self.beat('C01_hook')
        title = words('ONDE FICA A ENERGIA\nDE UM INDUTOR?', LAYOUT['title'], 34)
        self.play(FadeIn(title, shift=UP * .08), LaggedStart(Create(self.back), FadeIn(self.bots), FadeIn(self.tops),
                                                             lag_ratio=.25), run_time=1.6)
        self.add(flow)
        self.play(self.flow_op.animate.set_value(1), run_time=.8)
        gap = (BOTTOMS[11] + BOTTOMS[12]) / 2
        bet_wire = VGroup(words('NO FIO?', .55, 24, x=BOTTOMS[3]),
                          Arrow([BOTTOMS[3], .8, 0], [BOTTOMS[3], YC - A_R - .2, 0], buff=0, color=DIM, stroke_width=2.4,
                                max_tip_length_to_length_ratio=.2))
        bet_space = VGroup(words('NO ESPAÇO?', .55, 24, x=gap),
                           Arrow([gap, .8, 0], [gap, YC - .25, 0], buff=0, color=DIM, stroke_width=2.4,
                                 max_tip_length_to_length_ratio=.12))
        self.play(FadeIn(bet_wire[0]), GrowArrow(bet_wire[1]), run_time=.7)
        self.wait(.6)
        self.play(FadeIn(bet_space[0]), GrowArrow(bet_space[1]), run_time=.7)
        self.mark('C01_apostas')
        self.pad(7.0)
        self.play(FadeOut(bet_wire), FadeOut(bet_space), run_time=.6)
        self.pad(8.0)

        # C02 — situação: I, a, n, h; três chips.
        self.beat('C02_situacao')
        self.play(FadeOut(title), FadeIn(I_lab, shift=DOWN * .05), run_time=.8)
        self.wait(.5)
        axis = DashedLine([-4.2, YC, 0], [4.2, YC, 0], color=GEO, stroke_width=1.4, dash_length=.1).set_opacity(.45)
        radius = Arrow([3.0, YC, 0], [3.0, YC + A_R - .16, 0], buff=0, color=GEO, stroke_width=2.6,
                       max_tip_length_to_length_ratio=.16)
        a_lab = sym('a', GEO).move_to([3.28, YC + .5, 0])
        self.play(Create(axis), GrowArrow(radius), FadeIn(a_lab), run_time=1.0)
        self.wait(.6)
        ticks = VGroup(*[Line([x, YC - .08, 0], [x, YC + .08, 0], color=GEO, stroke_width=2,
                              stroke_opacity=.8 * edge(x)) for x in BOTTOMS])
        n_lab = VGroup(sym('n', GEO), words('ESPIRAS POR METRO', 0, 18, DIM)).arrange(RIGHT, buff=.15)
        n_lab.move_to([-1.3, YC + .42, 0])
        self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=.05), FadeIn(n_lab), run_time=1.2)
        self.wait(.6)
        brace = BraceBetweenPoints([H0, YC - A_R - .3, 0], [H1, YC - A_R - .3, 0], DOWN, color=GEO).set_opacity(.85)
        h_lab = sym('h', GEO).next_to(brace, DOWN, buff=.1)
        self.play(FadeIn(brace), FadeIn(h_lab), run_time=.8)
        self.wait(.6)
        c1 = chip(words('SOLENOIDE LONGO', 0, 22, DIM))
        c2 = chip(words('ENROLAMENTO UNIFORME', 0, 22, DIM))
        c3 = chip(VGroup(words('TRECHO', 0, 22, DIM), sym('h', GEO, 30), words('LONGE DAS PONTAS', 0, 22, DIM))
                  .arrange(RIGHT, buff=.14))
        for c, y in zip((c1, c2, c3), (LAYOUT['eq'], LAYOUT['row2'], LAYOUT['row3'])):
            c.move_to([0, y, 0])
            self.play(FadeIn(c, shift=UP * .06), run_time=.6)
            self.wait(.7)
        self.mark('C02_chips')
        self.pad(20.0)

        # C03 — Ampère: laço, setas de B, ℓ cancela.
        self.beat('C03_ampere')
        self.play(FadeOut(VGroup(c1, c2, c3)), FadeOut(axis), FadeOut(ticks), FadeOut(n_lab), FadeOut(radius),
                  FadeOut(a_lab), FadeOut(brace), FadeOut(h_lab), run_time=.7)
        xm = TOPS[np.argmin(abs(TOPS))]
        xl, xr = xm - 1.5 * P, xm + 1.5 * P
        yi, yo = YC + A_R - .38, YC + A_R + .55
        corners = [np.array(p) for p in ([xl, yi, 0], [xr, yi, 0], [xr, yo, 0], [xl, yo, 0])]
        loop = Polygon(*corners, color=GEO, stroke_width=2.6).set_z_index(9)
        tips = VGroup()
        for a, b in zip(corners, corners[1:] + corners[:1]):
            mid, d = (a + b) / 2, (b - a) / np.linalg.norm(b - a)
            tips.add(Arrow(mid - d * .16, mid + d * .16, buff=0, color=GEO, stroke_width=0,
                           max_tip_length_to_length_ratio=.6, tip_length=.2))
        tips.set_z_index(10)
        ell = sym(r'\ell', GEO).move_to([xm, yo + .32, 0])
        self.play(Create(loop), run_time=1.0)
        self.play(FadeIn(tips), FadeIn(ell), run_time=.5)
        ghost = VGroup(*[Arrow([c - .45, YC - A_R - .65, 0], [c + .45, YC - A_R - .65, 0], buff=0, color=FLD,
                               stroke_width=3, max_tip_length_to_length_ratio=.24).set_opacity(.28 * edge(c))
                         for c in COLS]).set_z_index(8)
        self.play(LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=.03), FadeIn(ghost), FadeIn(B_lab), run_time=1.4)
        self.mark('C03_laco_e_campo')
        self.wait(.4)
        eq = tex('amp')
        self.fly(eq, [(B_lab, [0]), (ell, [1]), (ell, [7]), (I_lab, [9])], rt=1.3)
        self.eq = eq
        enclosed = VGroup(*[self.tops[k] for k, x in enumerate(TOPS) if xl < x < xr])
        self.play(Indicate(enclosed, color=CUR, scale_factor=1.25), Indicate(glyphs(eq, [5, 6, 7, 8]), color=GEO),
                  run_time=1.0)
        self.wait(.5)
        cut = strikes(eq[0][1], eq[0][7])
        self.play(Create(cut), run_time=.5)
        self.wait(.4)
        self.morph(tex('B'), ([0], [0]), ([2], [1]), ([3, 4], [2, 3]), ([6], [4]), ([9], [5]),
                   ([1, 5, 7, 8], []), rt=1.4, extras=(FadeOut(cut),), name='C03_cancela_ell')
        box = SurroundingRectangle(self.eq, buff=.2, color=FLD, stroke_width=1.6, corner_radius=.1).set_stroke(opacity=.75)
        seal = chip(VGroup(words('B FORA', 0, 20, DIM), sym(r'\approx 0', DIM, 28)).arrange(RIGHT, buff=.1))
        seal.move_to([2.6, YC - A_R - 1.15, 0])
        self.play(Create(box), FadeIn(seal), ghost.animate.set_opacity(0), run_time=.8)
        self.mark('C03_resultado')
        self.pad(34.0)

        # C04 — fluxo por espira: o corte inclina, o disco A aparece.
        self.beat('C04_fluxo')
        B_ref = self.eq
        self.play(FadeOut(loop), FadeOut(tips), FadeOut(ell), FadeOut(seal), FadeOut(box), FadeOut(ghost),
                  B_ref.animate.scale(.72).move_to([0, LAYOUT['row3'], 0]), run_time=.8)
        self.eq = VGroup()
        d0 = self.disk(H0, .04)
        self.play(FadeIn(d0), run_time=.3)
        d_full = self.disk(H0)
        self.play(Transform(d0, d_full), run_time=1.0)
        A_lab = sym('A', GEO).move_to([H0 - .55, YC - A_R - .5, 0])
        A_lead = Line(A_lab.get_corner(UR) + [.04, .02, 0], [H0 - .1, YC - A_R + .25, 0], color=GEO, stroke_width=1.4)
        self.play(FadeIn(A_lab), Create(A_lead), Indicate(VGroup(*[a for a in field if abs(a.get_center()[0] - H0) < .1]),
                                                           color=FLD, scale_factor=1.1), run_time=.9)
        self.mark('C04_disco')
        eq = tex('phiBA')
        self.fly(eq, [(B_ref[0][0], [2]), (A_lab, [3])], rt=1.1)
        self.eq = eq
        A_ref = tex('A', y=LAYOUT['row2'], size=38)
        self.play(FadeIn(A_ref), run_time=.5)
        self.wait(.6)
        self.morph(tex('phi'), ([0, 1], [0, 1]), ([2], [2, 3, 4, 5]), ([3], [6, 7, 8]), rt=1.3, name='C04_substitui')
        phi_lab = sym(r'\Phi', FLD, 28).move_to([H0, YC + A_R + .5, 0])
        self.play(TransformFromCopy(self.eq[0][0], phi_lab), run_time=.8)
        self.mark('C04_resultado')
        self.pad(44.0)

        # C05 — o mesmo fluxo, N vezes (beat central).
        self.beat('C05_N_phi')
        phi_ref = self.eq
        self.play(FadeOut(A_ref), FadeOut(B_ref), FadeOut(A_lead), FadeOut(A_lab),
                  phi_ref.animate.scale(.72).move_to([0, LAYOUT['row3'], 0]), FadeIn(brace), FadeIn(h_lab), run_time=.8)
        self.eq = VGroup()
        unit = VGroup(d0, phi_lab)
        copies = [unit.copy() for _ in DISKS[1:]]
        self.add(*copies)
        self.play(LaggedStart(*[c.animate.shift(RIGHT * (x - H0)) for c, x in zip(copies, DISKS[1:])], lag_ratio=.18),
                  run_time=2.6)
        units = [unit] + copies
        self.mark('C05_copias')
        self.wait(.5)
        N_ref = tex('N', y=LAYOUT['row2'], size=36)
        self.play(LaggedStart(*[Indicate(u[0], color=GEO, scale_factor=1.12) for u in units], lag_ratio=.25),
                  run_time=1.8)
        self.fly(N_ref, [(h_lab, [3])], rt=.8)
        self.wait(.6)
        eq = tex('nphi1')
        self.fly(eq, [(u[1], [1]) for u in units] + [(N_ref[0][0], [0]), (N_ref[0][2:4], [4, 5]),
                                                       (phi_ref[0][2:9], [8, 9, 10, 11, 12, 13, 14])], rt=1.8)
        self.eq = eq
        self.mark('C05_soma')
        self.wait(1.0)
        self.morph(tex('nphi'), ([0, 1, 2], [0, 1, 2]), ([8, 9], [3, 4]), ([4, 10], [5]), ([], [6], {'delay': .5}),
                   ([11], [7]), ([12, 13, 14], [8, 9, 10]), ([5], [11], {'path_arc': -.9}), ([3, 6, 7, 15], []),
                   rt=1.6, name='C05_simplifica')
        concat = words('FLUXO CONCATENADO', 0, 19, DIM).next_to(glyphs(self.eq, [0, 1]), DOWN, buff=.22)
        self.play(FadeOut(N_ref), FadeOut(phi_ref), FadeIn(concat), run_time=.6)
        self.mark('C05_resultado')
        self.pad(58.0)

        # C06 — indutância; os dois n; proporcionalidades.
        self.beat('C06_indutancia')
        nphi_ref = self.eq
        self.play(FadeOut(concat), nphi_ref.animate.scale(.72).move_to([0, LAYOUT['row3'], 0]),
                  *[u[0].animate.set_stroke(opacity=.35).set_fill(opacity=.07) for u in units],
                  *[u[1].animate.set_opacity(.35) for u in units], run_time=.8)
        eq = tex('L0')
        self.fly(eq, [(glyphs(nphi_ref, [0, 1]), [2, 3]), (I_lab, [5])], rt=1.1)
        self.eq = eq
        self.wait(.6)
        self.morph(tex('L1'), ([0, 1], [0, 1]), ([2, 3], [2, 3, 4, 5, 6, 7, 8, 9, 10]), ([4], [11]), ([5], [12]),
                   rt=1.3, name='C06_substitui')
        self.wait(.4)
        cut = strikes(self.eq[0][6], self.eq[0][12])
        self.play(Create(cut), run_time=.5)
        self.wait(.3)
        self.morph(tex('L'), ([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]), ([7, 8, 9, 10], [6, 7, 8, 9]),
                   ([6, 11, 12], []), rt=1.4, extras=(FadeOut(cut),), name='C06_cancela_I')
        Lbox = SurroundingRectangle(self.eq, buff=.2, color=WHITE_, stroke_width=1.4, corner_radius=.1).set_stroke(opacity=.6)
        self.play(Create(Lbox), FadeOut(nphi_ref), run_time=.6)
        self.mark('C06_resultado')
        # os dois n: um vem de B, o outro de N
        nB = tex('B', y=LAYOUT['row2'] - .1, size=38, x=-2.0)
        nN = tex('N', y=LAYOUT['row2'] - .1, size=38, x=2.0)
        self.play(FadeIn(nB), FadeIn(nN), run_time=.6)
        n2 = glyphs(self.eq, [4, 5])
        rings = VGroup(Circle(radius=.22, color=GEO, stroke_width=2).move_to(nB[0][4]),
                       Circle(radius=.22, color=GEO, stroke_width=2).move_to(nN[0][2]))
        links = VGroup(CurvedArrow(rings[0].get_top() + UP * .02, n2.get_bottom() + DOWN * .08 + LEFT * .06, angle=-PI / 4,
                                   color=GEO, stroke_width=2, tip_length=.14),
                       CurvedArrow(rings[1].get_top() + UP * .02, n2.get_bottom() + DOWN * .08 + RIGHT * .06, angle=PI / 4,
                                   color=GEO, stroke_width=2, tip_length=.14)).set_z_index(41)
        self.play(Create(rings[0]), Create(links[0]), Indicate(field, color=FLD, scale_factor=1.05), run_time=1.0)
        self.wait(.4)
        self.play(Create(rings[1]), Create(links[1]),
                  LaggedStart(*[Indicate(u[0], color=GEO, scale_factor=1.1) for u in units], lag_ratio=.1), run_time=1.2)
        self.mark('C06_dois_n')
        self.wait(1.0)
        self.play(FadeOut(VGroup(nB, nN, rings, links)), run_time=.5)
        props = [chip(sym(s, WHITE_, 32)) for s in (r'L\propto n^2', r'L\propto a^2', r'L\propto h')]
        VGroup(*props).arrange(RIGHT, buff=.35).move_to([0, LAYOUT['row2'], 0])
        for p in props:
            for g in p[1][0][2:]:
                g.set_color(GEO)
        self.play(FadeIn(props[0], shift=UP * .05), run_time=.5)
        self.wait(.4)
        self.play(FadeIn(props[1], shift=UP * .05), Indicate(units[0][0], color=GEO, scale_factor=1.15), run_time=.7)
        self.wait(.3)
        self.play(FadeIn(props[2], shift=UP * .05), Indicate(VGroup(brace, h_lab), color=GEO, scale_factor=1.08), run_time=.7)
        self.mark('C06_proporcionalidades')
        self.pad(74.0)

        # C07 — energia pela rota do circuito; resultado fixado no topo.
        self.beat('C07_circuito')
        L_ref = self.eq
        self.play(FadeOut(VGroup(*props)), FadeOut(Lbox), L_ref.animate.scale(.72).move_to([0, LAYOUT['row3'], 0]),
                  *[FadeOut(u) for u in units[1:]], run_time=.7)
        eq = tex('U0')
        self.fly(eq, [(L_ref[0][0], [6]), (I_lab, [7])], rt=1.0)
        self.eq = eq
        self.wait(.5)
        self.morph(tex('U1'), ([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]), ([6], [6, 7, 8, 9, 10, 11, 12, 13]),
                   ([7, 8], [14, 15]), rt=1.3, name='C07_substitui')
        self.wait(.5)
        pin = self.eq
        pin_label = words('ROTA DO CIRCUITO', LAYOUT['pin_label'], 19, DIM)
        self.play(FadeOut(L_ref), pin.animate.scale(.8).move_to([0, LAYOUT['pin'], 0]), FadeIn(pin_label), run_time=1.0)
        self.eq = VGroup()
        self.mark('C07_fixado')
        self.pad(83.0)

        # C08 — energia pela rota do campo (protagonista): volume aceso, μ₀ cancela.
        self.beat('C08_campo')
        lit = self.glow()
        self.play(FadeOut(unit[1]), FadeOut(unit[0]), FadeIn(lit), run_time=1.4)
        self.mark('C08_volume_aceso')
        eq = tex('u')
        self.fly(eq, [(B_lab, [3])], rt=1.0)
        self.eq = eq
        note = words('ENERGIA POR UNIDADE DE VOLUME', LAYOUT['row2'], 20, DIM)
        self.play(FadeIn(note), run_time=.5)
        self.wait(.8)
        sx = ValueTracker(H0 + .001)
        volume = always_redraw(lambda: VGroup(
            Rectangle(width=sx.get_value() - H0, height=2 * A_R - .14, stroke_width=0, fill_color=GEO,
                      fill_opacity=.13).move_to([(H0 + sx.get_value()) / 2, YC, 0]),
            Line([H0, YC + A_R - .07, 0], [sx.get_value(), YC + A_R - .07, 0], color=GEO, stroke_width=1.6),
            Line([H0, YC - A_R + .07, 0], [sx.get_value(), YC - A_R + .07, 0], color=GEO, stroke_width=1.6),
            self.disk(H0).set_fill(opacity=.08).set_stroke(opacity=.6),
            self.disk(sx.get_value())).set_z_index(7))
        self.play(FadeIn(volume), run_time=.4)
        self.play(sx.animate.set_value(H1), run_time=2.4, rate_func=smooth)
        self.mark('C08_volume_varrido')
        V_ref = tex('V', y=LAYOUT['row3'], size=38, x=1.9)
        u_ref = self.eq
        self.play(FadeOut(note), u_ref.animate.scale(.72).move_to([-1.9, LAYOUT['row3'], 0]), run_time=.7)
        self.fly(V_ref, [(h_lab, [5])], rt=.8)
        self.wait(.4)
        eq = tex('E1')
        self.fly(eq, [(glyphs(u_ref, [0, 1]), [3, 4]), (V_ref[0][0], [5])], rt=1.1)
        self.eq = eq
        self.wait(.5)
        self.morph(tex('E2'), ([0, 1, 2], [0, 1, 2]), ([3, 4], [3, 4, 5, 6, 7, 8]), ([5], [9, 10, 11, 12]),
                   rt=1.3, name='C08_u_e_V')
        B_ref = tex('B', y=LAYOUT['row3'], size=38)
        self.play(FadeOut(u_ref), FadeOut(V_ref), FadeIn(B_ref), run_time=.7)
        self.wait(.3)
        self.morph(tex('E3'), ([0, 1, 2], [0, 1, 2]), ([3], [3, 4, 5, 6, 7, 8]), ([4], [9]),
                   ([5, 6, 7, 8, 9, 10, 11, 12], [10, 11, 12, 13, 14, 15, 16, 17]), rt=1.3, name='C08_substitui_B')
        self.wait(.5)
        self.morph(tex('E4'), ([0, 1, 2], [0, 1, 2]), ([4, 5], [3, 4, 5, 6]), ([6], [7]), ([9], [8, 10]), ([7], [9]),
                   ([3, 8], []), ([10, 11, 12, 13, 14, 15, 16, 17], [11, 12, 13, 14, 15, 16, 17, 18]),
                   rt=1.3, name='C08_expande')
        self.wait(.5)
        cut = strikes(glyphs(self.eq, [5, 6]), glyphs(self.eq, [13, 14]))
        self.play(Create(cut), run_time=.5)
        self.wait(.4)
        self.morph(tex('E5'), ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]), ([7, 8, 9, 10, 11, 12], [5, 6, 7, 8, 9, 10]),
                   ([15, 16, 17, 18], [11, 12, 13, 14]), ([5, 6, 13, 14], []), rt=1.5, extras=(FadeOut(cut),),
                   name='C08_cancela_mu0')
        self.mark('C08_resultado')
        self.pad(105.0)

        # C09 — conferência: a de baixo vira a de cima; o fio apaga, o volume fica.
        self.beat('C09_convergencia')
        self.morph(tex('U1'), ([0, 1, 2], [0, 1, 2]), ([], [3], {'delay': .4}), ([9], [4]), ([10], [5]), ([3, 4], [6, 7]),
                   ([5, 6], [8, 9]), ([11, 12, 13, 14], [10, 11, 12, 13]), ([7, 8], [14, 15], {'path_arc': -1.0}),
                   rt=1.6, name='C09_reorganiza')
        self.wait(.4)
        field_eq = self.eq
        check = MathTex('=', font_size=44, color=WHITE_).rotate(PI / 2).move_to([pin.get_center()[0], LAYOUT['pin'] - .55, 0])
        self.play(FadeOut(B_ref), FadeOut(volume),
                  field_eq.animate.scale(.8).move_to([pin.get_center()[0], LAYOUT['pin'] - 1.1, 0]), run_time=1.2)
        field_label = words('ROTA DO CAMPO', LAYOUT['pin'] - 1.62, 19, DIM)
        self.play(FadeIn(check, shift=DOWN * .12), FadeIn(field_label), run_time=.5)
        self.mark('C09_conferencia')
        self.wait(1.0)
        self.play(self.flow_op.animate.set_value(.12), self.back.animate.set_stroke(opacity=.08),
                  self.tops.animate.set_opacity(.22), self.bots.animate.set_opacity(.22),
                  I_lab.animate.set_opacity(.25), FadeOut(brace), FadeOut(h_lab), run_time=1.4)
        u_near = tex('u', y=YC - A_R - .75, size=38)
        self.play(FadeIn(u_near, shift=UP * .06), run_time=.8)
        self.mark('C09_fio_apagado')
        self.wait(.8)
        seal = words('A ENERGIA ESTÁ NO CAMPO', LAYOUT['eq'], 30)
        self.play(FadeIn(seal, shift=UP * .06), run_time=.8)
        self.mark('C09_selo')
        self.pad(118.0)

        # C10 — fechamento: somente o handle.
        self.beat('C10_fechamento')
        for m in list(self.mobjects):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.6)
        self.clear()
        self.wait(.3)
        handle = words('@labparallax', 0, 48).set_color_by_gradient(CYAN, VIOLET, PINK)
        self.play(FadeIn(handle, scale=.96), run_time=.7)
        self.mark('C10_handle')
        self.wait(1.5)
        self.play(FadeOut(handle), run_time=.5)
        self.pad(126.0)
        self.beats[-1][2] = self.time
        self.mark('fim')
        for name, a, b in self.beats:
            print(f'[tempo] {name}: {a:6.1f} s -> {b:6.1f} s ({b - a:5.1f} s)')
        out = Path(config.media_dir) / 'estados_vid0027.json'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({'eventos': self.events, 'beats': [{'beat': n, 'inicio': round(a, 2), 'fim': round(b, 2)}
                                                                     for n, a, b in self.beats],
                                   'duracao': round(self.time, 2)}, ensure_ascii=False, indent=1), encoding='utf-8')
