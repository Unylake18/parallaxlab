"""vid_0027 — Onde fica a energia de um indutor? (preview visual silencioso v2).

Curto vertical, Manim 2D. v2 (handoff v2): solenoide em pé (eixo vertical, B para cima), corte com a parede esquerda
em ⊙ e a direita em ⊗, corrente correndo pela meia volta de trás (da direita para a esquerda) em traços verdes.
Toda grandeza entra em três estágios: forma geral (chip + linha de definição) → passagem ao caso do solenoide
(glyph map, termos vindos da cena) → resultado em painel. Zonas fixas: palco no terço superior, equações em
três linhas (G, M, R) num painel de vidro, definições abaixo, 10% inferior livre. v1 em cena_v1.py.

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
config.media_dir = os.environ.get('MEDIA_DIR', str(UNIT / 'media_v2'))
config.background_color = BACKGROUND_COLOR

# ── paleta (handoff v1 §4 e v2 §3.2) ────────────────────────────────────────────────────────────────────────
CUR = '#3FE08B'     # corrente I
FLD = '#EA63FF'     # B, Φ, NΦ, Λ, U_B, u_B
GEO = '#B8C4DA'     # a, h, A, V, n, ℓ, dℓ, dA, laço
STEEL = '#7A8696'   # espiras
DIM = '#8FA3C4'     # texto secundário, chips, definições
EMF = PRIMARY_COLOR  # fem ε_L e potência P da fonte (ciano, como no yt_0012)
PANEL, BLUE_L = '#0E2A52', '#7FB2FF'
WHITE_ = TEXT_COLOR
CYAN, VIOLET, PINK = PRIMARY_COLOR, '#9C8CFF', '#EA63FF'   # só no degradê do cartão final (como no vid_0024)

# ── palco: solenoide em pé ──────────────────────────────────────────────────────────────────────────────────
XC, A_R, YC = 0.0, 1.5, 3.4                 # eixo x = 0, raio desenhado, centro vertical do desenho
RIGHT_W = .85 + .6 * np.arange(9)           # ⊗ (parede direita)
LEFT_W = RIGHT_W + .3                       # ⊙ (parede esquerda): meia volta depois
H0, H1 = 1.75, 5.05                         # trecho h
DISKS = np.linspace(1.95, 4.85, 6)          # cópias do disco (estilizado: N não é o n real)
COLS, ROWS = (-.7, 0., .7), (1.4, 2.75, 4.1, 5.45)   # setas de B
SPC, DASH, VFLOW = .6, .12, .55             # traços da corrente: espaçamento, meio-comprimento, velocidade
# zonas (y): tag 0–7% · faixa fixada 7–13% · palco 9–44% · equações 48–78% · definições 80–90% · 10% livre
Y = {'pin': 6.48, 'chip': .02, 'G': -.82, 'M': -2.08, 'R': -3.32, 'refs': -4.3, 'd1': -5.12, 'd2': -5.72}

FORMULAS = {  # tex, nº de glifos, {cor: índices}
    'amp0': (r'\oint\vec B\cdot d\vec\ell=\mu_0I_{\text{int}}', 14, {FLD: [1, 2], GEO: [4, 5, 6], CUR: [10, 11, 12, 13]}),
    'amp1': (r'B\ell=\mu_0I_{\text{int}}', 9, {FLD: [0], GEO: [1], CUR: [5, 6, 7, 8]}),
    'Iint': (r'I_{\text{int}}=(n\ell)I', 10, {CUR: [0, 1, 2, 3, 9], GEO: [6, 7]}),
    'amp': (r'B\ell=\mu_0(n\ell)I', 10, {FLD: [0], GEO: [1, 6, 7], CUR: [9]}),
    'B': (r'B=\mu_0nI', 6, {FLD: [0], GEO: [4], CUR: [5]}),
    'phi0': (r'\Phi=\int\vec B\cdot d\vec A', 9, {FLD: [0, 3, 4], GEO: [6, 7, 8]}),
    'phi1': (r'\Phi=B\int dA', 6, {FLD: [0, 2], GEO: [4, 5]}),
    'phiBA': (r'\Phi=BA', 4, {FLD: [0, 2], GEO: [3]}),
    'phi': (r'\Phi=\mu_0nI\pi a^2', 9, {FLD: [0], GEO: [4, 7, 8], CUR: [5]}),
    'dA': (r'\int dA=A=\pi a^2', 9, {GEO: [1, 2, 4, 7, 8]}),
    'lam': (r'\Lambda=\Phi_1+\Phi_2+\cdots+\Phi_N', 14, {FLD: [0, 2, 3, 5, 6, 12, 13]}),
    'lam1': (r'\Lambda=N\Phi', 4, {FLD: [0, 3]}),
    'N': (r'N=nh', 4, {GEO: [2, 3]}),
    'nphi1': (r'N\Phi=(nh)(\mu_0nI\pi a^2)', 16, {FLD: [1], GEO: [4, 5, 10, 13, 14], CUR: [11]}),
    'nphi': (r'N\Phi=\mu_0n^2I\pi a^2h', 12, {FLD: [1], GEO: [5, 6, 9, 10, 11], CUR: [7]}),
    'L0': (r'L=\frac{N\Phi}{I}', 6, {FLD: [3], CUR: [5]}),
    'L1': (r'L=\frac{\mu_0n^2I\pi a^2h}{I}', 13, {GEO: [4, 5, 8, 9, 10], CUR: [6, 12]}),
    'L': (r'L=\mu_0n^2\pi a^2h', 10, {GEO: [4, 5, 7, 8, 9]}),
    'emf': (r'\mathcal{E}_L=-L\frac{dI}{dt}', 10, {EMF: [0, 1], CUR: [6]}),
    'P': (r'P=|\mathcal{E}_L|\,I=LI\frac{dI}{dt}', 15, {EMF: [0, 3, 4], CUR: [6, 9, 11]}),
    'dU': (r'dU_B=P\,dt=LI\,dI', 12, {FLD: [0, 1, 2], EMF: [4], CUR: [9, 11]}),
    'Uint': (r"U_B=\int_0^{I}LI'\,dI'=\frac{1}{2}LI^2", 19, {FLD: [0, 1], CUR: [4, 7, 8, 10, 11, 17, 18]}),
    'U0': (r'U_B=\frac{1}{2}LI^2', 9, {FLD: [0, 1], CUR: [7, 8]}),
    'U1': (r'U_B=\frac{1}{2}\mu_0n^2\pi a^2hI^2', 16, {FLD: [0, 1], GEO: [8, 9, 11, 12, 13], CUR: [14, 15]}),
    'udef': (r'u_B=\frac{dU_B}{dV}', 9, {FLD: [0, 1, 3, 4, 5], GEO: [7, 8]}),
    'u': (r'u_B=\frac{B^2}{2\mu_0}', 9, {FLD: [0, 1, 3, 4]}),
    'Uint2': (r'U_B=\int u_B\,dV', 8, {FLD: [0, 1, 4, 5], GEO: [6, 7]}),
    'V': (r'V=\pi a^2h', 6, {GEO: [0, 3, 4, 5]}),
    'E1': (r'U_B=u_BV', 6, {FLD: [0, 1, 3, 4], GEO: [5]}),
    'E2': (r'U_B=\frac{B^2}{2\mu_0}\pi a^2h', 13, {FLD: [0, 1, 3, 4], GEO: [10, 11, 12]}),
    'E3': (r'U_B=\frac{(\mu_0nI)^2}{2\mu_0}\pi a^2h', 18, {FLD: [0, 1], GEO: [6, 15, 16, 17], CUR: [7]}),
    'E4': (r'U_B=\frac{\mu_0\mu_0n^2I^2}{2\mu_0}\pi a^2h', 19, {FLD: [0, 1], GEO: [7, 8, 16, 17, 18], CUR: [9, 10]}),
    'E5': (r'U_B=\frac{\mu_0n^2I^2}{2}\pi a^2h', 15, {FLD: [0, 1], GEO: [5, 6, 12, 13, 14], CUR: [7, 8]}),
    'conf': (r'\frac{1}{2}LI^2=u_BV', 10, {CUR: [4, 5], FLD: [7, 8], GEO: [9]}),
}


def edge(y):
    """Opacidade nas pontas do desenho: o solenoide continua além do quadro (muito longo)."""
    return float(np.clip((2.9 - abs(y - YC)) / .9, 0, 1))


def words(content, y=0, size=28, color=WHITE_, x=0):
    pw, ph = config.pixel_width, config.pixel_height
    try:
        config.pixel_width = config.pixel_height = 4000
        mob = screen_text(content, size, color=color, oversample=2)
    finally:
        config.pixel_width, config.pixel_height = pw, ph
    if mob.width > 7.6:
        mob.scale_to_fit_width(7.6)
    return mob.move_to([x, y, 0]).set_z_index(40)


def tex(key, y=0, size=46, x=0):
    s, count, colors = FORMULAS[key]
    mob = MathTex(s, font_size=size, color=WHITE_)
    assert len(mob[0]) == count, (key, len(mob[0]), count)
    for ink, idx in colors.items():
        for i in idx:
            mob[0][i].set_color(ink)
    if mob.width > 7.4:
        mob.scale_to_fit_width(7.4)
    return mob.move_to([x, y, 0]).set_z_index(40)


def sym(s, color, size=36):
    return MathTex(s, font_size=size, color=color).set_z_index(40)


def line(*parts, y=Y['d1'], size=21):
    """Linha curta de definição/justificativa: texto em minúsculas apagado; símbolos na cor da grandeza."""
    ms = [words(p, 0, size, DIM) if isinstance(p, str) else sym(p[0], p[1], 32) for p in parts]
    g = VGroup(*ms).arrange(RIGHT, buff=.12)
    if g.width > 8.0:
        g.scale_to_fit_width(8.0)
    return g.move_to([0, y, 0])


def chip(content, pad=(.2, .12), stroke=DIM):
    box = RoundedRectangle(corner_radius=.12, width=content.width + 2 * pad[0], height=content.height + 2 * pad[1],
                           stroke_color=stroke, stroke_width=1.3, stroke_opacity=.7,
                           fill_color=PANEL, fill_opacity=.75).move_to(content).set_z_index(39)
    return VGroup(box, content)


def tag(text, y=Y['chip'], x=0):
    return chip(words(text, 0, 18, DIM)).move_to([x, y, 0])


def glass(mob, pad=(.32, .2), op=.7):
    return RoundedRectangle(corner_radius=.16, width=mob.width + 2 * pad[0], height=mob.height + 2 * pad[1],
                            stroke_color=BLUE_L, stroke_width=1.5, stroke_opacity=.85,
                            fill_color=PANEL, fill_opacity=op).move_to(mob).set_z_index(30)


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

    # ── álgebra ──────────────────────────────────────────────────────────────────────────────────────────────
    def morph(self, source, target, *links, rt=2.0, extras=(), keep=False, name=None):
        """Glyph map de source para target; keep=True deixa a forma anterior no lugar (passagem para outra linha)."""
        src = source.copy() if keep else source
        if keep:
            self.add(src)
        anim = TransformByGlyphMap(src, target, *links, auto_fade=True, auto_morph=False, printing=False)
        assert not anim.show_indices
        if name:
            self.mark(name + '_inicio')
        self.play(anim, *extras, run_time=rt, rate_func=smooth)
        self.remove(*src.get_family())
        self.remove(*target.get_family())
        self.add(target)
        if name:
            self.mark(name + '_fim')
        return target

    def fly(self, eq, pairs, rt=1.4, extras=()):
        """Variáveis navegam da cena (ou de outra linha) para os glifos de eq e deixam uma marca de origem que se apaga."""
        movers, anims, used, marks = [], [], set(), []
        for src, idx in pairs:
            c = src.copy()
            movers.append(c)
            anims.append(Transform(c, glyphs(eq, idx).copy()))
            used |= set(idx)
            ring = SurroundingRectangle(src, buff=.06, corner_radius=.06, stroke_width=1.6,
                                        color=src.get_color()).set_z_index(44)
            marks.append(ring)
        rest = VGroup(*[g for i, g in enumerate(eq[0]) if i not in used])
        self.play(*[Create(m) for m in marks], run_time=.35)
        self.play(*anims, FadeIn(rest), *[FadeOut(m) for m in marks], *extras, run_time=rt, rate_func=smooth)
        self.remove(*movers, rest)
        self.add(eq)
        return eq

    def note(self, slot, mob, rt=.6):
        old = self.notes.get(slot)
        anims = [FadeOut(old)] if old is not None else []
        if mob is not None:
            anims.append(FadeIn(mob, shift=UP * .05))
        if anims:
            self.play(*anims, run_time=rt)
        self.notes[slot] = mob

    def clear_notes(self, rt=.5):
        olds = [m for m in self.notes.values() if m is not None]
        if olds:
            self.play(*[FadeOut(m) for m in olds], run_time=rt)
        self.notes = {}

    def result(self, eq, rt=.7):
        box = glass(eq)
        self.play(FadeIn(box), run_time=rt)
        return box

    # ── fundo e palco ────────────────────────────────────────────────────────────────────────────────────────
    def backdrop(self):
        grad = Rectangle(width=9.2, height=16.2, stroke_width=0).set_fill(['#0B1736', BACKGROUND_COLOR], opacity=1)
        grad.set_sheen_direction(DOWN)
        halo = VGroup(*[Circle(radius=r).set_stroke(width=0).set_fill(BLUE_L, .016).move_to([0, YC, 0])
                        for r in (4.4, 3.6, 2.9, 2.3)])
        vignette = VGroup(*[Rectangle(width=9.2 - k * .5, height=16.2 - k * .5).set_stroke(BACKGROUND_COLOR, 18, .10)
                            for k in range(4)])
        rng = np.random.default_rng(27)
        stars = VGroup(*[Dot([rng.uniform(-4.3, 4.3), rng.uniform(-7.8, 7.8), 0], radius=rng.uniform(.008, .02),
                             color=WHITE_).set_opacity(rng.uniform(.1, .3)) for _ in range(34)])
        return VGroup(grad, halo, stars, vignette).set_z_index(-20)

    def build_solenoid(self):
        back = VGroup()
        for yr, yl in zip(RIGHT_W, LEFT_W):
            back.add(Line([A_R - .15, yr, 0], [-A_R + .15, yl, 0], color=STEEL, stroke_width=1.6,
                          stroke_opacity=.4 * edge((yr + yl) / 2)))
        left, right = VGroup(), VGroup()
        for yl in LEFT_W:
            o = edge(yl)
            ring = Circle(radius=.15, color=STEEL, stroke_width=2.8, stroke_opacity=o,
                          fill_color=BACKGROUND_COLOR, fill_opacity=1).move_to([-A_R, yl, 0])
            left.add(VGroup(ring, Dot([-A_R, yl, 0], radius=.048, color=CUR, fill_opacity=o)))
        for yr in RIGHT_W:
            o = edge(yr)
            c = np.array([A_R, yr, 0])
            ring = Circle(radius=.15, color=STEEL, stroke_width=2.8, stroke_opacity=o,
                          fill_color=BACKGROUND_COLOR, fill_opacity=1).move_to(c)
            cross = VGroup(Line(c + [-.075, -.075, 0], c + [.075, .075, 0]),
                           Line(c + [-.075, .075, 0], c + [.075, -.075, 0])).set_stroke(CUR, 2.4, o)
            right.add(VGroup(ring, cross))
        back.set_z_index(-2)
        left.set_z_index(6)
        right.set_z_index(6)
        self.back, self.left, self.right = back, left, right

    def build_flow(self):
        """Corrente: traços verdes na meia volta de trás, da parede ⊗ (direita) para a ⊙ (esquerda); velocidade ∝ I."""
        g = VGroup().set_z_index(3)
        g.ph = 0.0
        segs = [(np.array([A_R - .17, yr, 0]), np.array([-A_R + .17, yl, 0])) for yr, yl in zip(RIGHT_W, LEFT_W)]

        def upd(m, dt):
            I = self.current.get_value()
            m.ph = (m.ph + dt * VFLOW * I) % SPC
            o = self.flow_op.get_value() * min(1.0, 4 * I)
            marks = []
            if o > .01:
                for a, b in segs:
                    L = np.linalg.norm(b - a)
                    u = (b - a) / L
                    oe = o * edge((a[1] + b[1]) / 2)
                    if oe < .02:
                        continue
                    for s in np.arange(m.ph, L, SPC):
                        s0, s1 = max(0, s - DASH), min(L, s + DASH)
                        if s1 - s0 < .03:
                            continue
                        mid = a + u * s
                        marks.append(VGroup(Line(a + u * s0, mid).set_stroke(CUR, 4.4, .45 * oe),
                                            Line(mid, a + u * s1).set_stroke(CUR, 4.4, oe)))
            m.submobjects = marks
        g.add_updater(upd)
        return g

    def build_field(self):
        arrows, glows = VGroup(), VGroup()
        for x in COLS:
            for y in ROWS:
                o = edge(y)
                a = Arrow([x, y - .45, 0], [x, y + .45, 0], buff=0, color=FLD, stroke_width=3.6,
                          max_tip_length_to_length_ratio=.24, max_stroke_width_to_length_ratio=8).set_opacity(.92 * o)
                a.base = .92 * o
                arrows.add(a)
                gl = Line([x, y - .45, 0], [x, y + .35, 0], color=FLD, stroke_width=11).set_stroke(opacity=.12 * o)
                gl.base = .12 * o
                glows.add(gl)
        return arrows.set_z_index(8), glows.set_z_index(7)

    def disk(self, y, height=.46):
        return Ellipse(width=2 * A_R - .16, height=height, stroke_color=GEO, stroke_width=2,
                       fill_color=GEO, fill_opacity=.16).move_to([XC, y, 0]).set_z_index(9)

    def glow(self):
        strips = VGroup()
        ys = np.linspace(YC - 2.9, YC + 2.9, 81)
        for a, b in zip(ys[:-1], ys[1:]):
            o = edge((a + b) / 2)
            strips.add(Rectangle(width=2 * A_R - .34, height=b - a + .005, stroke_width=0, fill_color=FLD,
                                 fill_opacity=.24 * o).move_to([XC, (a + b) / 2, 0]))
        soft = VGroup(*[Rectangle(width=2 * A_R - .34 + k * .12, height=5.2, stroke_width=0, fill_color=FLD,
                                  fill_opacity=.025).move_to([XC, YC, 0]) for k in range(3)])
        return VGroup(soft, strips).set_z_index(1)

    def leader(self, label_pos, target, color=GEO):
        return Line(label_pos, target, color=color, stroke_width=1.3, stroke_opacity=.75).set_z_index(5)

    # ── cena ─────────────────────────────────────────────────────────────────────────────────────────────────
    def construct(self):
        self.events, self.beats, self.notes = [], [], {}
        self.current = ValueTracker(1)
        self.flow_op = ValueTracker(0)
        self.add(self.backdrop())
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.4).to_corner(UR, buff=.28).set_z_index(60)
        brand = words('EXERCÍCIO RESOLVIDO · EP. 10', 0, 20, DIM).set_opacity(.75).to_corner(UL, buff=.4)
        self.add(wm, brand)

        self.build_solenoid()
        flow = self.build_flow()
        field, field_glow = self.build_field()
        eqpanel = RoundedRectangle(corner_radius=.22, width=8.4, height=4.95, stroke_color=BLUE_L, stroke_width=1.1,
                                   stroke_opacity=.25, fill_color=PANEL, fill_opacity=.28).move_to([0, -2.08, 0])
        eqpanel.set_z_index(-5)
        I_lab = sym('I', CUR).move_to([-2.5, LEFT_W[7], 0])
        I_lead = self.leader(I_lab.get_right() + RIGHT * .08, [-A_R - .17, LEFT_W[7], 0], CUR)
        yB = (RIGHT_W[7] + RIGHT_W[8]) / 2
        B_lab = sym('B', FLD).move_to([2.5, yB, 0])
        B_lead = self.leader(B_lab.get_left() + LEFT * .08, [COLS[2] + .08, yB, 0], FLD)

        # C01 — hook: duas apostas, sem resposta.
        self.beat('C01_hook')
        title = words('ONDE FICA A ENERGIA\nDE UM INDUTOR?', -1.3, 38)
        self.play(FadeIn(title, shift=UP * .08), LaggedStart(Create(self.back), FadeIn(self.right), FadeIn(self.left),
                                                             lag_ratio=.25), run_time=1.8)
        self.add(flow)
        self.play(self.flow_op.animate.set_value(1), run_time=.8)
        yw, yg = LEFT_W[6], (RIGHT_W[3] + RIGHT_W[4]) / 2
        bet_wire = VGroup(words('NO FIO?', yw, 24, x=-3.3),
                          Arrow([-2.6, yw, 0], [-A_R - .2, yw, 0], buff=0, color=DIM, stroke_width=2.4,
                                max_tip_length_to_length_ratio=.25))
        bet_space = VGroup(words('NO ESPAÇO?', yg, 24, x=3.25),
                           Arrow([2.32, yg, 0], [.35, yg, 0], buff=0, color=DIM, stroke_width=2.4,
                                 max_tip_length_to_length_ratio=.12))
        self.play(FadeIn(bet_wire[0]), GrowArrow(bet_wire[1]), run_time=.7)
        self.wait(.7)
        self.play(FadeIn(bet_space[0]), GrowArrow(bet_space[1]), run_time=.7)
        self.mark('C01_apostas')
        self.wait(2.0)
        self.play(FadeOut(bet_wire), FadeOut(bet_space), run_time=.6)
        self.wait(.5)

        # C02 — situação: índice de variáveis, cada uma definida ao entrar.
        self.beat('C02_situacao')
        self.play(FadeOut(title), FadeIn(eqpanel), run_time=.8)
        rows = [-.15, -.95, -1.75, -2.55, -3.35]

        def entry(symtex, color, text, y):
            return VGroup(sym(symtex, color, 38), words(text, 0, 22, DIM)).arrange(RIGHT, buff=.22).move_to([0, y, 0])
        index = VGroup()
        e1 = entry('I', CUR, 'corrente elétrica nas espiras', rows[0])
        self.play(FadeIn(I_lab), Create(I_lead), FadeIn(e1, shift=UP * .05), run_time=.9)
        index.add(e1)
        self.wait(1.6)
        axis = DashedLine([XC, .45, 0], [XC, 6.2, 0], color=GEO, stroke_width=1.4, dash_length=.1).set_opacity(.4)
        y_a = (LEFT_W[5] + LEFT_W[6]) / 2
        radius = Arrow([XC, y_a, 0], [A_R - .18, y_a, 0], buff=0, color=GEO, stroke_width=2.6,
                       max_tip_length_to_length_ratio=.14)
        a_lab = sym('a', GEO, 34).move_to([.68, y_a + .25, 0])
        e2 = entry('a', GEO, 'raio do solenoide', rows[1])
        self.play(Create(axis), GrowArrow(radius), FadeIn(a_lab), FadeIn(e2, shift=UP * .05), run_time=.9)
        index.add(e2)
        self.wait(1.6)
        n_brace = BraceBetweenPoints([-A_R - .32, LEFT_W[2], 0], [-A_R - .32, LEFT_W[0], 0], LEFT, color=GEO)
        n_lab = sym('n', GEO).next_to(n_brace, LEFT, buff=.12)
        e3 = entry('n', GEO, 'espiras por metro', rows[2])
        self.play(FadeIn(n_brace), FadeIn(n_lab), Indicate(VGroup(*self.left[:2]), color=GEO, scale_factor=1.2),
                  FadeIn(e3, shift=UP * .05), run_time=1.0)
        index.add(e3)
        self.wait(1.5)
        brace = BraceBetweenPoints([A_R + .32, H1, 0], [A_R + .32, H0, 0], RIGHT, color=GEO)
        h_lab = sym('h', GEO).next_to(brace, RIGHT, buff=.12)
        e4 = entry('h', GEO, 'trecho longe das pontas', rows[3])
        self.play(FadeIn(brace), FadeIn(h_lab), FadeIn(e4, shift=UP * .05), run_time=.9)
        index.add(e4)
        self.wait(1.5)
        in_h = [w for w, y in zip(self.right, RIGHT_W) if H0 < y < H1]
        e5 = VGroup(tex('N', size=38), words('espiras no trecho', 0, 22, DIM)).arrange(RIGHT, buff=.22).move_to([0, rows[4], 0])
        self.play(LaggedStart(*[Indicate(w, color=GEO, scale_factor=1.25) for w in in_h], lag_ratio=.2),
                  FadeIn(e5, shift=UP * .05), run_time=1.8)
        index.add(e5)
        self.note('d1', tag('SOLENOIDE LONGO · ENROLAMENTO UNIFORME · NÚCLEO DE AR', Y['d1']))
        self.mark('C02_indice')
        self.wait(2.6)

        # C03 — Ampère: lei → Bℓ → B.
        self.beat('C03_ampere')
        self.play(FadeOut(index), FadeOut(axis), FadeOut(radius), FadeOut(a_lab), FadeOut(n_brace), FadeOut(n_lab),
                  run_time=.7)
        self.clear_notes()
        chip_t = tag('LEI DE AMPÈRE')
        G = tex('amp0', Y['G'])
        self.play(FadeIn(chip_t), FadeIn(G, shift=UP * .05), run_time=.8)
        self.note('d1', line((r'I_{\text{int}}', CUR), ': corrente elétrica total (líquida) que atravessa', y=Y['d1']))
        self.note('d2', line('a área delimitada pelo caminho', y=Y['d2']))
        self.mark('C03_lei')
        self.wait(2.6)
        xo, xi = -A_R - .6, -A_R + .4
        yb, yt = (LEFT_W[2] + LEFT_W[3]) / 2, (LEFT_W[5] + LEFT_W[6]) / 2
        corners = [np.array(p) for p in ([xo, yb, 0], [xi, yb, 0], [xi, yt, 0], [xo, yt, 0])]
        sides = VGroup(*[Line(a, b, color=GEO, stroke_width=2.6) for a, b in zip(corners, corners[1:] + corners[:1])])
        sides.set_z_index(10)
        tips = VGroup()
        for a, b in zip(corners, corners[1:] + corners[:1]):
            mid, d = (a + b) / 2, (b - a) / np.linalg.norm(b - a)
            tips.add(Arrow(mid - d * .17, mid + d * .17, buff=0, color=GEO, stroke_width=0,
                           max_tip_length_to_length_ratio=.6, tip_length=.2))
        tips.set_z_index(11)
        ell = sym(r'\ell', GEO).move_to([-2.5, (yb + yt) / 2, 0])
        self.play(Create(sides), run_time=1.0)
        self.play(FadeIn(tips), FadeIn(ell), LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=.03),
                  FadeIn(field_glow), FadeIn(B_lab), Create(B_lead), run_time=1.4)
        self.mark('C03_laco_e_campo')
        self.clear_notes(.4)
        self.note('d1', line('lado interno:', (r'\vec B\parallel d\vec\ell', FLD), ' contribui com ', (r'B\ell', FLD)))
        self.play(Indicate(sides[1], color=FLD, scale_factor=1.0), run_time=1.0)
        self.wait(.8)
        self.note('d1', line('lados de cima e de baixo:', (r'\vec B\perp d\vec\ell', FLD), ' não contribuem'))
        self.play(Indicate(VGroup(sides[0], sides[2]), color=WHITE_, scale_factor=1.0), run_time=1.0)
        self.wait(.6)
        self.note('d1', line('lado externo:', (r'B\approx 0', FLD), ' (fora do solenoide)'))
        self.play(Indicate(sides[3], color=WHITE_, scale_factor=1.0), run_time=1.0)
        self.wait(.6)
        M = self.morph(G, tex('amp1', Y['M']), ([2], [0]), ([6], [1]), ([7], [2]), ([8, 9], [3, 4]),
                       ([10, 11, 12, 13], [5, 6, 7, 8]), ([0, 1, 3, 4, 5], []), keep=True, name='C03_integral_vira_Bl')
        self.wait(1.4)
        inside = VGroup(*[w for w, y in zip(self.left, LEFT_W) if yb < y < yt])
        self.note('d1', VGroup(tex('Iint', size=36), words('espiras dentro do laço × I', 0, 21, DIM))
                  .arrange(RIGHT, buff=.25).move_to([0, Y['d1'], 0]))
        self.play(Indicate(inside, color=CUR, scale_factor=1.3), run_time=1.2)
        self.wait(.6)
        M = self.morph(M, tex('amp', Y['M']), ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]), ([5, 6, 7, 8], [5, 6, 7, 8, 9]),
                       name='C03_substitui_Iint')
        self.wait(1.0)
        cut = strikes(M[0][1], M[0][7])
        self.play(Create(cut), run_time=.5)
        self.wait(.4)
        R = self.morph(M, tex('B', Y['R'], 50), ([0], [0]), ([2], [1]), ([3, 4], [2, 3]), ([6], [4]), ([9], [5]),
                       ([1, 5, 7, 8], []), extras=(FadeOut(cut),), name='C03_cancela_ell')
        box = self.result(R)
        self.note('d1', line('dentro: campo uniforme e paralelo ao eixo; fora:', (r'B\approx0', FLD)))
        self.mark('C03_resultado')
        self.wait(3.0)

        # C04 — fluxo: ∫B·dA → BA.
        self.beat('C04_fluxo')
        B_ref = R
        self.play(FadeOut(G), FadeOut(chip_t), FadeOut(sides), FadeOut(tips), FadeOut(ell), FadeOut(box),
                  B_ref.animate.scale(.7).move_to([-2.3, Y['refs'], 0]), run_time=.8)
        self.clear_notes(.4)
        d0 = self.disk(DISKS[0], .02)
        self.play(FadeIn(d0), run_time=.3)
        self.play(Transform(d0, self.disk(DISKS[0])), run_time=1.0)
        A_lab = sym('A', GEO).move_to([-2.5, DISKS[0], 0])
        A_lead = self.leader(A_lab.get_right() + RIGHT * .08, [-A_R + .12, DISKS[0], 0])
        self.play(FadeIn(A_lab), Create(A_lead), run_time=.6)
        chip_t = tag('FLUXO MAGNÉTICO')
        G = tex('phi0', Y['G'])
        self.play(FadeIn(chip_t), FadeIn(G, shift=UP * .05), run_time=.8)
        self.note('d1', line((r'\Phi', FLD), ': quanto campo atravessa uma superfície'))
        self.mark('C04_definicao')
        self.wait(2.8)
        self.note('d1', line((r'\vec B', FLD), ' uniforme e perpendicular ao disco:', (r'\vec B\cdot d\vec A=B\,dA', FLD)))
        self.play(Indicate(VGroup(*[a for a in field if abs(a.get_center()[1] - DISKS[0]) < .6]), color=FLD,
                           scale_factor=1.08), run_time=.9)
        M = self.morph(G, tex('phi1', Y['M']), ([0, 1], [0, 1]), ([4], [2], {'path_arc': -.8}), ([2], [3]), ([6], [4]),
                       ([8], [5]), ([3, 5, 7], []), keep=True, name='C04_B_sai_da_integral')
        self.wait(1.4)
        self.note('d1', VGroup(tex('dA', size=36), words('(área do disco)', 0, 21, DIM)).arrange(RIGHT, buff=.25)
                  .move_to([0, Y['d1'], 0]))
        self.play(Indicate(d0, color=GEO, scale_factor=1.06), run_time=.8)
        M = self.morph(M, tex('phiBA', Y['M']), ([0, 1, 2], [0, 1, 2]), ([5], [3]), ([3, 4], []), name='C04_BA')
        self.wait(1.2)
        R = self.morph(M, tex('phi', Y['R'], 50), ([0, 1], [0, 1]), ([2], [2, 3, 4, 5]), ([3], [6, 7, 8]),
                       extras=(Indicate(B_ref, color=FLD, scale_factor=1.1),), name='C04_substitui')
        box = self.result(R)
        phi_lab = sym(r'\Phi', FLD, 28).move_to([-.35, DISKS[0], 0])
        self.play(TransformFromCopy(R[0][0], phi_lab), run_time=.8)
        self.mark('C04_resultado')
        self.wait(3.0)

        # C05 — fluxo concatenado: o mesmo Φ, N vezes (beat central).
        self.beat('C05_concatenado')
        phi_ref = R
        self.play(FadeOut(G), FadeOut(chip_t), FadeOut(box), FadeOut(A_lab), FadeOut(A_lead),
                  phi_ref.animate.scale(.7).move_to([2.3, Y['refs'], 0]), run_time=.8)
        self.clear_notes(.4)
        unit = VGroup(d0, phi_lab)
        copies = [unit.copy().set_opacity(0) for _ in DISKS[1:]]
        for c in copies:
            c.move_to(unit)
        self.add(*copies)
        self.play(LaggedStart(*[c.animate.move_to([XC, y, 0]).set_opacity(1) for c, y in zip(copies, DISKS[1:])],
                              lag_ratio=.18), run_time=2.6)
        for c in copies:
            c[0].set_fill(opacity=.16)
        units = [unit] + copies
        chip_t = tag('FLUXO CONCATENADO')
        G = tex('lam', Y['G'], 44)
        self.play(FadeIn(chip_t), FadeIn(G, shift=UP * .05), run_time=.8)
        self.note('d1', line('cada espira do trecho enxerga o mesmo', (r'\Phi', FLD)))
        self.mark('C05_soma_de_espiras')
        self.wait(2.8)
        M = self.morph(G, tex('lam1', Y['M']), ([0, 1], [0, 1]), ([2, 5, 12], [3]), ([13], [2]),
                       ([3, 4, 6, 7, 8, 9, 10, 11], []), keep=True,
                       extras=(LaggedStart(*[Indicate(u[1], color=FLD) for u in units], lag_ratio=.1),),
                       name='C05_todos_iguais')
        self.wait(1.4)
        N_note = VGroup(tex('N', size=36), words('espiras no trecho', 0, 21, DIM)).arrange(RIGHT, buff=.25)
        N_note.move_to([0, Y['d1'], 0])
        self.note('d1', N_note)
        self.play(LaggedStart(*[Indicate(u[0], color=GEO, scale_factor=1.1) for u in units], lag_ratio=.2), run_time=1.6)
        new = tex('nphi1', Y['M'])
        self.fly(new, [(glyphs(M, [2, 3]), [0, 1]), (M[0][1], [2]), (N_note[0][0][2:4], [4, 5]),
                       (phi_ref[0][2:9], [8, 9, 10, 11, 12, 13, 14])], extras=(FadeOut(M),))
        M = new
        self.mark('C05_substitui')
        self.wait(1.4)
        R = self.morph(M, tex('nphi', Y['R'], 50), ([0, 1, 2], [0, 1, 2]), ([8, 9], [3, 4]), ([4, 10], [5]),
                       ([], [6], {'delay': .6}), ([11], [7]), ([12, 13, 14], [8, 9, 10]), ([5], [11], {'path_arc': -.9}),
                       ([3, 6, 7, 15], []), name='C05_simplifica')
        box = self.result(R)
        self.note('d1', line('fluxo concatenado: o mesmo', (r'\Phi', FLD), ', N vezes'))
        self.mark('C05_resultado')
        self.wait(3.0)

        # C06 — indutância; os dois n; proporcionalidades.
        self.beat('C06_indutancia')
        nphi_ref = R
        self.play(FadeOut(G), FadeOut(chip_t), FadeOut(box), FadeOut(phi_ref),
                  nphi_ref.animate.scale(.7).move_to([2.2, Y['refs'], 0]),
                  *[u[0].animate.set_stroke(opacity=.3).set_fill(opacity=.05) for u in units],
                  *[u[1].animate.set_opacity(.3) for u in units], run_time=.8)
        self.clear_notes(.4)
        chip_t = tag('INDUTÂNCIA')
        G = tex('L0', Y['G'])
        self.play(FadeIn(chip_t), run_time=.4)
        self.fly(G, [(glyphs(nphi_ref, [0, 1]), [2, 3]), (I_lab, [5])], rt=1.2)
        self.note('d1', line('fluxo concatenado por unidade de corrente'))
        self.note('d2', line('unidade: henry (H)', y=Y['d2']))
        self.mark('C06_definicao')
        self.wait(2.8)
        M = self.morph(G, tex('L1', Y['M']), ([0, 1], [0, 1]), ([2, 3], [2, 3, 4, 5, 6, 7, 8, 9, 10]), ([4], [11]),
                       ([5], [12]), keep=True, extras=(Indicate(nphi_ref, color=FLD, scale_factor=1.08),),
                       name='C06_substitui')
        self.wait(1.2)
        self.clear_notes(.4)
        cut = strikes(M[0][6], M[0][12])
        self.note('d1', line('a corrente se cancela: L só depende da geometria'))
        self.play(Create(cut), run_time=.5)
        self.wait(.6)
        R = self.morph(M, tex('L', Y['R'], 50), ([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]), ([7, 8, 9, 10], [6, 7, 8, 9]),
                       ([6, 11, 12], []), extras=(FadeOut(cut), FadeOut(nphi_ref)), name='C06_cancela_I')
        box = self.result(R)
        self.mark('C06_resultado')
        self.wait(1.6)
        self.play(FadeOut(G), FadeOut(chip_t), run_time=.4)
        nB = tex('B', Y['M'], 40, x=-2.4)
        nN = tex('N', Y['M'], 40, x=2.4)
        self.note('d1', line('um n vem do campo, o outro do número de espiras'))
        self.play(FadeIn(nB), FadeIn(nN), FadeOut(B_ref), run_time=.6)
        n2 = R[0][4]
        rings = VGroup(Circle(radius=.24, color=GEO, stroke_width=2).move_to(nB[0][4]),
                       Circle(radius=.24, color=GEO, stroke_width=2).move_to(nN[0][2])).set_z_index(41)
        links = VGroup(Arrow(rings[0].get_bottom(), n2.get_top() + LEFT * .08 + UP * .04, buff=.06, color=GEO,
                             stroke_width=2, max_tip_length_to_length_ratio=.08),
                       Arrow(rings[1].get_bottom(), n2.get_top() + RIGHT * .08 + UP * .04, buff=.06, color=GEO,
                             stroke_width=2, max_tip_length_to_length_ratio=.08)).set_z_index(41)
        self.play(Create(rings[0]), GrowArrow(links[0]), Indicate(field, color=FLD, scale_factor=1.04), run_time=1.1)
        self.wait(.6)
        self.play(Create(rings[1]), GrowArrow(links[1]),
                  LaggedStart(*[Indicate(u[0], color=GEO, scale_factor=1.1) for u in units], lag_ratio=.1), run_time=1.2)
        self.mark('C06_dois_n')
        self.wait(2.0)
        self.play(FadeOut(VGroup(nB, nN, rings, links)), run_time=.5)
        props = [chip(sym(s, WHITE_, 32)) for s in (r'L\propto n^2', r'L\propto a^2', r'L\propto h')]
        for p in props:
            for g in p[1][0][2:]:
                g.set_color(GEO)
        VGroup(*props).arrange(RIGHT, buff=.35).move_to([0, Y['M'], 0])
        self.clear_notes(.3)
        self.play(FadeIn(props[0], shift=UP * .05), run_time=.5)
        self.wait(.4)
        self.play(FadeIn(props[1], shift=UP * .05), Indicate(units[0][0], color=GEO, scale_factor=1.12), run_time=.7)
        self.wait(.4)
        self.play(FadeIn(props[2], shift=UP * .05), Indicate(VGroup(brace, h_lab), color=GEO, scale_factor=1.08),
                  run_time=.7)
        self.mark('C06_proporcionalidades')
        self.wait(2.0)

        # C07 — rota do circuito: de onde vem ½LI².
        self.beat('C07_circuito')
        L_ref = R
        self.play(FadeOut(VGroup(*props)), FadeOut(box), *[FadeOut(u) for u in units],
                  L_ref.animate.scale(.7).move_to([0, Y['refs'], 0]), run_time=.8)
        # a corrente começa em zero e sobe até I enquanto a energia entra
        self.current.set_value(0)
        for a in field:
            a.set_opacity(0)
        for gl in field_glow:
            gl.set_stroke(opacity=0)

        def ramp(m, dt):
            self.current.set_value(min(1.0, self.current.get_value() + dt / 9))
            k = self.current.get_value()
            for a in field:
                a.set_opacity(a.base * k)
            for gl in field_glow:
                gl.set_stroke(opacity=gl.base * k)
        driver = Mobject()
        driver.add_updater(ramp)
        self.add(driver)
        chip_t = tag('ENERGIA NO INDUTOR')
        G = tex('emf', Y['G'])
        self.play(FadeIn(chip_t), FadeIn(G, shift=UP * .05), run_time=.8)
        self.note('d1', tag('A ENERGIA ENTRA ENQUANTO I SOBE DE 0 A I', Y['d1']))
        self.note('d2', line((r'\mathcal{E}_L', EMF), ': fem do indutor, contra a variação de I', y=Y['d2']))
        self.mark('C07_fem')
        self.wait(2.6)
        M = tex('P', Y['M'])
        self.fly(M, [(glyphs(G, [0, 1]), [3, 4]), (G[0][4], [8]), (glyphs(G, [5, 6, 7, 8, 9]), [10, 11, 12, 13, 14])])
        self.note('d2', line((r'P', EMF), ': potência que a fonte entrega para vencer a fem', y=Y['d2']))
        self.wait(2.2)
        R = tex('dU', Y['R'])
        self.fly(R, [(M[0][0], [4]), (glyphs(M, [8, 9]), [8, 9]), (glyphs(M, [10, 11]), [10, 11])])
        self.note('d2', line('em', (r'dt', WHITE_), ', a energia guardada cresce', (r'dU_B=P\,dt', FLD), y=Y['d2']))
        self.mark('C07_dU')
        self.wait(2.2)
        self.play(FadeOut(G), FadeOut(M), R.animate.move_to([0, Y['G'], 0]), run_time=.8)
        G = R
        M = tex('Uint', Y['M'])
        self.fly(M, [(G[0][8], [6]), (G[0][9], [7]), (glyphs(G, [10, 11]), [9, 10])])
        self.note('d2', line('somando de', (r'I=0', CUR), ' até ', (r'I', CUR), y=Y['d2']))
        self.mark('C07_integral')
        self.wait(2.6)
        R = tex('U0', Y['R'], 50)
        self.fly(R, [(glyphs(M, [0, 1, 2]), [0, 1, 2]), (glyphs(M, [13, 14, 15, 16, 17, 18]), [3, 4, 5, 6, 7, 8])])
        box = self.result(R)
        self.wait(1.6)
        R = self.morph(R, tex('U1', Y['R'], 50), ([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]),
                       ([6], [6, 7, 8, 9, 10, 11, 12, 13]), ([7, 8], [14, 15]),
                       extras=(Indicate(L_ref, color=WHITE_, scale_factor=1.1), box.animate.stretch_to_fit_width(
                           tex('U1', Y['R'], 50).width + .64)), name='C07_substitui_L')
        self.mark('C07_resultado')
        self.wait(2.4)
        pin_chip = tag('ROTA DO CIRCUITO')
        pin = R
        pin_target = pin.copy().scale(.74)
        row = VGroup(pin_chip.copy(), pin_target).arrange(RIGHT, buff=.3).move_to([0, Y['pin'], 0])
        pin_chip.move_to(row[0])
        self.clear_notes(.4)
        self.play(FadeOut(G), FadeOut(M), FadeOut(chip_t), FadeOut(box), FadeOut(L_ref),
                  pin.animate.scale(.74).move_to(row[1]), FadeIn(pin_chip), run_time=1.1)
        driver.clear_updaters()
        self.remove(driver)
        self.current.set_value(1)
        self.mark('C07_fixado')
        self.wait(1.5)

        # C08 — rota do campo: u_B (resultado geral), ∫ → u V, μ₀ cancela.
        self.beat('C08_campo')
        chip_t = tag('DENSIDADE DE ENERGIA')
        G = tex('udef', Y['G'])
        self.play(FadeIn(chip_t), FadeIn(G, shift=UP * .05), run_time=.8)
        self.note('d1', line((r'u_B', FLD), ': energia do campo por unidade de volume'))
        self.mark('C08_definicao')
        self.wait(2.6)
        lit = self.glow()
        gen = tag('RESULTADO GERAL', Y['M'], x=-2.75)
        M = tex('u', Y['M'], x=.9)
        self.play(FadeIn(lit), FadeIn(gen), run_time=1.0)
        self.fly(M, [(B_lab, [3])], rt=1.2)
        self.note('d1', line('vale para qualquer campo magnético no vácuo'))
        self.mark('C08_volume_aceso')
        self.wait(2.8)
        G2 = tex('Uint2', Y['G'])
        self.play(FadeOut(G), run_time=.4)
        self.fly(G2, [(glyphs(M, [0, 1]), [4, 5])], rt=1.1)
        G = G2
        self.note('d1', line('somando a energia de cada volume', (r'dV', GEO)))
        self.wait(2.2)
        self.note('d1', line((r'u_B', FLD), ' uniforme dentro, zero fora:', (r'\int u_B\,dV\to u_BV', FLD)))
        G = self.morph(G, tex('E1', Y['G']), ([0, 1, 2], [0, 1, 2]), ([4, 5], [3, 4]), ([7], [5]), ([3, 6], []),
                       name='C08_integral_vira_uV')
        sy = ValueTracker(H0 + .001)
        volume = always_redraw(lambda: VGroup(
            Rectangle(width=2 * A_R - .16, height=sy.get_value() - H0, stroke_width=0, fill_color=GEO,
                      fill_opacity=.12).move_to([XC, (H0 + sy.get_value()) / 2, 0]),
            Line([-A_R + .08, H0, 0], [-A_R + .08, sy.get_value(), 0], color=GEO, stroke_width=1.6),
            Line([A_R - .08, H0, 0], [A_R - .08, sy.get_value(), 0], color=GEO, stroke_width=1.6),
            self.disk(H0).set_fill(opacity=.06).set_stroke(opacity=.6),
            self.disk(sy.get_value())).set_z_index(9))
        self.add(volume)
        self.note('d1', VGroup(tex('V', size=36), words('seção A varrida ao longo de h', 0, 21, DIM))
                  .arrange(RIGHT, buff=.25).move_to([0, Y['d1'], 0]))
        self.play(sy.animate.set_value(H1), run_time=2.6, rate_func=smooth)
        self.mark('C08_volume_varrido')
        self.wait(1.0)
        G = self.morph(G, tex('E2', Y['G']), ([0, 1, 2], [0, 1, 2]), ([3, 4], [3, 4, 5, 6, 7, 8]), ([5], [9, 10, 11, 12]),
                       extras=(Indicate(glyphs(M, [2, 3, 4, 5, 6, 7, 8]), color=FLD, scale_factor=1.08),),
                       name='C08_u_e_V')
        self.wait(1.2)
        B_ref = tex('B', Y['refs'], 34)
        self.play(FadeOut(M), FadeOut(gen), FadeIn(B_ref), run_time=.7)
        self.note('d1', line('substituir', (r'B=\mu_0nI', FLD)))
        G = self.morph(G, tex('E3', Y['G']), ([0, 1, 2], [0, 1, 2]), ([3], [3, 4, 5, 6, 7, 8]), ([4], [9]),
                       ([5, 6, 7, 8, 9, 10, 11, 12], [10, 11, 12, 13, 14, 15, 16, 17]),
                       extras=(Indicate(B_ref, color=FLD, scale_factor=1.1),), name='C08_substitui_B')
        self.wait(1.2)
        M = self.morph(G, tex('E4', Y['M']), ([0, 1, 2], [0, 1, 2]), ([4, 5], [3, 4, 5, 6]), ([6], [7]), ([9], [8, 10]),
                       ([7], [9]), ([3, 8], []), ([10, 11, 12, 13, 14, 15, 16, 17], [11, 12, 13, 14, 15, 16, 17, 18]),
                       keep=True, name='C08_expande')
        self.wait(1.0)
        cut = strikes(glyphs(M, [5, 6]), glyphs(M, [13, 14]))
        self.note('d1', line('um', (r'\mu_0', WHITE_), ' de cima cancela o', (r'\mu_0', WHITE_), ' de baixo'))
        self.play(Create(cut), run_time=.5)
        self.wait(.6)
        R = self.morph(M, tex('E5', Y['R'], 50), ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]), ([7, 8, 9, 10, 11, 12], [5, 6, 7, 8, 9, 10]),
                       ([15, 16, 17, 18], [11, 12, 13, 14]), ([5, 6, 13, 14], []), extras=(FadeOut(cut),),
                       name='C08_cancela_mu0')
        box = self.result(R)
        self.mark('C08_resultado')
        self.wait(3.0)

        # C09 — conferência das duas rotas; o fio apaga, o volume fica aceso.
        self.beat('C09_convergencia')
        self.clear_notes(.4)
        self.play(FadeOut(G), FadeOut(chip_t), FadeOut(B_ref), FadeOut(volume), FadeOut(box), run_time=.6)
        R = self.morph(R, tex('U1', Y['R'], 50), ([0, 1, 2], [0, 1, 2]), ([], [3], {'delay': .5}), ([9], [4]), ([10], [5]),
                       ([3, 4], [6, 7]), ([5, 6], [8, 9]), ([11, 12, 13, 14], [10, 11, 12, 13]),
                       ([7, 8], [14, 15], {'path_arc': -1.0}), name='C09_mesma_forma')
        self.wait(1.0)
        top_row = VGroup(pin_chip, pin)
        top_t = VGroup(pin_chip.copy(), pin.copy().scale(1 / .74 * .8)).arrange(RIGHT, buff=.3).move_to([0, Y['G'], 0])
        camp_chip = tag('ROTA DO CAMPO')
        mid_t = VGroup(camp_chip, R.copy().scale(.8)).arrange(RIGHT, buff=.3).move_to([0, Y['M'], 0])
        mid_t[1].align_to(top_t[1], LEFT)
        camp_chip.align_to(top_t[0], RIGHT).set_y(Y['M'])
        self.play(top_row[0].animate.move_to(top_t[0]), top_row[1].animate.become(top_t[1]),
                  R.animate.become(mid_t[1]), FadeIn(camp_chip), run_time=1.3)
        conf = tex('conf', Y['R'], 52)
        lhs, eqs, rhs = glyphs(conf, [0, 1, 2, 3, 4, 5]), conf[0][6], glyphs(conf, [7, 8, 9])
        self.play(FadeIn(lhs, shift=RIGHT * .1), FadeIn(rhs, shift=LEFT * .1), run_time=.7)
        self.play(FadeIn(eqs, shift=DOWN * .15), run_time=.5)
        self.remove(lhs, eqs, rhs)
        self.add(conf)
        box = self.result(conf)
        self.mark('C09_conferencia')
        self.wait(2.2)
        self.play(self.flow_op.animate.set_value(.1), self.back.animate.set_stroke(opacity=.06),
                  self.left.animate.set_opacity(.2), self.right.animate.set_opacity(.2), I_lab.animate.set_opacity(.25),
                  I_lead.animate.set_stroke(opacity=.2), FadeOut(brace), FadeOut(h_lab), run_time=1.4)
        u_near = tex('u', YC, 34, x=2.95)
        self.play(FadeIn(u_near, shift=LEFT * .06), run_time=.8)
        self.mark('C09_fio_apagado')
        self.wait(.6)
        self.note('d1', words('A ENERGIA ESTÁ NO CAMPO', Y['d1'], 30))
        self.mark('C09_selo')
        self.wait(2.6)

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
        self.wait(.4)
        self.beats[-1][2] = self.time
        self.mark('fim')
        for name, a, b in self.beats:
            print(f'[tempo] {name}: {a:6.1f} s -> {b:6.1f} s ({b - a:5.1f} s)')
        out = Path(config.media_dir) / 'estados_vid0027.json'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({'eventos': self.events, 'beats': [{'beat': n, 'inicio': round(a, 2), 'fim': round(b, 2)}
                                                                     for n, a, b in self.beats],
                                   'duracao': round(self.time, 2)}, ensure_ascii=False, indent=1), encoding='utf-8')
