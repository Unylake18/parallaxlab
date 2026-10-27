"""vid_0027 — Onde fica a energia de um indutor? (v3 sincronizada com a voz v4).

Curto vertical, Manim 2D. v3: volta ao solenoide deitado da v1 (eixo horizontal, B → +x; corte com a parede de cima
em ⊙ e a de baixo em ⊗; corrente subindo pela meia volta de trás), agora maior e com 9 espiras. Da v2 fica a regra
das três etapas (forma geral com chip e definição → passagem ao solenoide → resultado em painel), com tela limpa:
no máximo duas equações (forma geral em cima, passo atual embaixo) e uma linha de nota, que também traz o resultado
anterior quando ele é substituído. Texto de tela em MAIÚSCULAS (Space Grotesk); definição de variável em MathTex
minúsculo (padrão dos longos). v1 em cena_v1.py, v2 (solenoide em pé) em cena_v2.py.

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
config.media_dir = os.environ.get('MEDIA_DIR', str(UNIT / 'media_v3'))
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

# ── palco: corte longitudinal, eixo horizontal ──────────────────────────────────────────────────────────────
YC, A_R = 3.75, 1.55                        # eixo, raio desenhado (corte ~480 × 190 px no preview)
BOTTOMS = -3.825 + .9 * np.arange(9)        # ⊗ (parede de baixo)
TOPS = BOTTOMS + .45                        # ⊙ (parede de cima): meia volta depois
H0, H1 = -2.7, 2.7                          # trecho h
DISKS = np.linspace(H0, H1, 7)              # cópias do disco (estilizado: N não é o n real)
COLS, ROWS = (-2.7, -.9, .9, 2.7), (YC - .75, YC, YC + .75)   # setas de B
SPC, DASH, VFLOW = .6, .12, .55             # traços da corrente: espaçamento, meio-comprimento, velocidade
# zonas (y): tag · faixa fixada (C07–C09) · palco · chip · forma geral G · passo M · notas · ~25% inferior livre
Y = {'pin': 6.62, 'chip': .5, 'G': -.42, 'M': -1.8, 'n1': -3.15, 'n2': -3.72}
# sincronia com a voz (narracao_tags_v4 → audio/narracao_v4.wav): MEDIR=1 grava o instante natural de cada âncora (nat.json);
# SYNC=sync.json faz cada âncora começar LEAD s antes da frase e ajusta o ritmo do trecho seguinte (plan_sync.py).
MEDIR = os.environ.get('MEDIR') == '1'
SYNC = os.environ.get('SYNC')

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


def edge(x):
    """Opacidade nas pontas do desenho: o solenoide continua além do quadro (muito longo)."""
    return float(np.clip((4.4 - abs(x)) / 1.0, 0, 1))


def words(content, y=0, size=28, color=WHITE_, x=0, upper=True):
    """Texto de tela: Space Grotesk em MAIÚSCULAS (padrão dos longos); o handle do canal fica como é."""
    pw, ph = config.pixel_width, config.pixel_height
    try:
        config.pixel_width = config.pixel_height = 4000
        mob = screen_text(content.upper() if upper else content, size, color=color, oversample=2)
    finally:
        config.pixel_width, config.pixel_height = pw, ph
    if mob.width > 7.8:
        mob.scale_to_fit_width(7.8)
    return mob.move_to([x, y, 0]).set_z_index(40)


def tex(key, y=0, size=48, x=0):
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


def defn(symbol, text, color=WHITE_, y=Y['n1'], size=36):
    """Definição de variável em MathTex minúsculo: símbolo na cor da grandeza, texto apagado."""
    if symbol in FORMULAS:
        s, count, colors = FORMULAS[symbol]
    else:
        s, count, colors = symbol, None, {color: None}
    mob = MathTex(s, r':\ \text{' + text + '}', font_size=size, color=DIM)
    if count is not None:
        assert len(mob[0]) == count, (symbol, len(mob[0]))
        mob[0].set_color(WHITE_)
        for ink, idx in colors.items():
            for i in idx:
                mob[0][i].set_color(ink)
    else:
        mob[0].set_color(color)
    if mob.width > 8.2:
        mob.scale_to_fit_width(8.2)
    return mob.move_to([0, y, 0]).set_z_index(40)


def line(*parts, y=Y['n1'], size=20):
    """Linha de justificativa: texto em MAIÚSCULAS apagado; símbolos na cor da grandeza."""
    ms = [words(p, 0, size, DIM) if isinstance(p, str) else sym(p[0], p[1], 32) for p in parts]
    g = VGroup(*ms).arrange(RIGHT, buff=.13)
    if g.width > 8.2:
        g.scale_to_fit_width(8.2)
    return g.move_to([0, y, 0])


def chip(content, pad=(.2, .12), stroke=DIM):
    box = RoundedRectangle(corner_radius=.12, width=content.width + 2 * pad[0], height=content.height + 2 * pad[1],
                           stroke_color=stroke, stroke_width=1.3, stroke_opacity=.7,
                           fill_color=PANEL, fill_opacity=.75).move_to(content).set_z_index(39)
    return VGroup(box, content)


def tag(text, y=Y['chip'], x=0, size=18):
    return chip(words(text, 0, size, DIM)).move_to([x, y, 0])


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
    def morph(self, source, target, *links, rt=1.5, extras=(), keep=False, name=None):
        """Glyph map de source para target; keep=True deixa a forma anterior no lugar (passagem para a linha de baixo)."""
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
        """Variáveis navegam da cena (ou da nota) para os glifos de eq; o resto entra por fade."""
        movers, anims, used = [], [], set()
        for src, idx in pairs:
            c = src.copy()
            movers.append(c)
            anims.append(Transform(c, glyphs(eq, idx).copy()))
            used |= set(idx)
        rest = VGroup(*[g for i, g in enumerate(eq[0]) if i not in used])
        self.play(*anims, FadeIn(rest), *extras, run_time=rt, rate_func=smooth)
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

    def result(self, eq, rt=.6):
        box = glass(eq)
        self.play(FadeIn(box), run_time=rt)
        return box

    def to_note(self, eq, box=None, slot='n1', x=0, extras=(), rt=.8):
        """O resultado anterior encolhe para a linha de nota e fica como referência da substituição."""
        old = self.notes.get(slot)
        anims = [eq.animate.scale(.68).move_to([x, Y[slot], 0]), *extras]
        if box is not None:
            anims.append(FadeOut(box))
        if old is not None:
            anims.append(FadeOut(old))
        self.play(*anims, run_time=rt)
        self.notes[slot] = eq

    # ── fundo e palco ────────────────────────────────────────────────────────────────────────────────────────
    def backdrop(self):
        grad = Rectangle(width=9.2, height=16.2, stroke_width=0).set_fill(['#0B1736', BACKGROUND_COLOR], opacity=1)
        grad.set_sheen_direction(DOWN)
        halo = VGroup(*[Ellipse(width=w, height=w * .6).set_stroke(width=0).set_fill(BLUE_L, .016).move_to([0, YC, 0])
                        for w in (9.5, 8.0, 6.6, 5.2)])
        vignette = VGroup(*[Rectangle(width=9.2 - k * .5, height=16.2 - k * .5).set_stroke(BACKGROUND_COLOR, 18, .10)
                            for k in range(4)])
        rng = np.random.default_rng(27)
        stars = VGroup(*[Dot([rng.uniform(-4.3, 4.3), rng.uniform(-7.8, 7.8), 0], radius=rng.uniform(.008, .02),
                             color=WHITE_).set_opacity(rng.uniform(.1, .28)) for _ in range(30)])
        return VGroup(grad, halo, stars, vignette).set_z_index(-20)

    def build_solenoid(self):
        back = VGroup()
        for xb, xt in zip(BOTTOMS, TOPS):
            back.add(Line([xb, YC - A_R + .16, 0], [xt, YC + A_R - .16, 0], color=STEEL, stroke_width=1.6,
                          stroke_opacity=.38 * edge((xb + xt) / 2)))
        tops, bots = VGroup(), VGroup()
        for xt in TOPS:
            o = edge(xt)
            ring = Circle(radius=.17, color=STEEL, stroke_width=2.8, stroke_opacity=o,
                          fill_color=BACKGROUND_COLOR, fill_opacity=1).move_to([xt, YC + A_R, 0])
            tops.add(VGroup(ring, Dot([xt, YC + A_R, 0], radius=.052, color=CUR, fill_opacity=o)))
        for xb in BOTTOMS:
            o = edge(xb)
            c = np.array([xb, YC - A_R, 0])
            ring = Circle(radius=.17, color=STEEL, stroke_width=2.8, stroke_opacity=o,
                          fill_color=BACKGROUND_COLOR, fill_opacity=1).move_to(c)
            cross = VGroup(Line(c + [-.08, -.08, 0], c + [.08, .08, 0]),
                           Line(c + [-.08, .08, 0], c + [.08, -.08, 0])).set_stroke(CUR, 2.4, o)
            bots.add(VGroup(ring, cross))
        back.set_z_index(-2)
        tops.set_z_index(6)
        bots.set_z_index(6)
        self.back, self.tops, self.bots = back, tops, bots

    def build_flow(self):
        """Corrente: traços verdes subindo pela meia volta de trás (⊗ embaixo → ⊙ em cima); velocidade ∝ I."""
        g = VGroup().set_z_index(3)
        g.ph = 0.0
        segs = [(np.array([xb, YC - A_R + .19, 0]), np.array([xt, YC + A_R - .19, 0])) for xb, xt in zip(BOTTOMS, TOPS)]

        def upd(m, dt):
            I = self.current.get_value()
            m.ph = (m.ph + dt * VFLOW * I) % SPC
            o = self.flow_op.get_value() * min(1.0, 4 * I)
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
                        marks.append(VGroup(Line(a + u * s0, mid).set_stroke(CUR, 4.4, .45 * oe),
                                            Line(mid, a + u * s1).set_stroke(CUR, 4.4, oe)))
            m.submobjects = marks
        g.add_updater(upd)
        return g

    def build_field(self):
        arrows, glows = VGroup(), VGroup()
        for y in ROWS:
            for x in COLS:
                o = edge(x)
                a = Arrow([x - .5, y, 0], [x + .5, y, 0], buff=0, color=FLD, stroke_width=3.8,
                          max_tip_length_to_length_ratio=.24, max_stroke_width_to_length_ratio=8).set_opacity(.92 * o)
                a.base = .92 * o
                arrows.add(a)
                gl = Line([x - .5, y, 0], [x + .4, y, 0], color=FLD, stroke_width=12).set_stroke(opacity=.11 * o)
                gl.base = .11 * o
                glows.add(gl)
        return arrows.set_z_index(8), glows.set_z_index(7)

    def disk(self, x, width=.62):
        return Ellipse(width=width, height=2 * A_R - .18, stroke_color=GEO, stroke_width=2,
                       fill_color=GEO, fill_opacity=.16).move_to([x, YC, 0]).set_z_index(9)

    def glow(self):
        strips = VGroup()
        xs = np.linspace(-4.6, 4.6, 93)
        for a, b in zip(xs[:-1], xs[1:]):
            o = edge((a + b) / 2)
            strips.add(Rectangle(width=b - a + .005, height=2 * A_R - .38, stroke_width=0, fill_color=FLD,
                                 fill_opacity=.24 * o).move_to([(a + b) / 2, YC, 0]))
        soft = VGroup(*[Rectangle(width=8.4, height=2 * A_R - .38 + k * .1, stroke_width=0, fill_color=FLD,
                                  fill_opacity=.025).move_to([0, YC, 0]) for k in range(3)])
        return VGroup(soft, strips).set_z_index(1)

    def leader(self, a, b, color=GEO):
        return Line(a, b, color=color, stroke_width=1.3, stroke_opacity=.75).set_z_index(5)

    # ── sincronia com a voz ──────────────────────────────────────────────────────────────────────────────────
    def play(self, *anims, run_time=None, **kw):
        """Todo play do roteiro é escalado pelo ritmo do trecho atual (K); os de infraestrutura (_raw) não."""
        if not self._raw:
            run_time = (1.0 if run_time is None else run_time) * self.K
        if run_time is not None:
            kw['run_time'] = run_time
        return super().play(*anims, **kw)

    def wait(self, duration=1.0, **kw):
        self.idle(duration * self.K)

    def idle(self, d):
        """Espera sem tela parada: o último elemento em foco "respira" (pulso sutil); a corrente segue correndo no palco."""
        if d < .02:
            return
        self._raw = True
        try:
            f = self.focus
            if f is not None and f in self.mobjects and d >= .45:
                n = max(1, int(round(d / 2.0)))
                for _ in range(n):
                    self.play(f.animate(rate_func=there_and_back).scale(1.035), run_time=d / n)
            else:
                Scene.wait(self, d)
        finally:
            self._raw = False

    def an(self, nome):
        """Âncora: o passo seguinte começa LEAD s antes da frase de mesmo nome na voz (SYNC) ou só mede (MEDIR)."""
        t = self.time
        if MEDIR:
            self.nat[nome] = round(t, 4)
        elif self.sync:
            a = self.sync['ancoras'][nome]
            if a['T'] - t > .02:
                self.idle(a['T'] - t)
            self.atrasos[nome] = round(self.time - a['T'], 3)
            self.K = a['f']
        self.mark('an_' + nome)

    def focar(self, mob):
        self.focus = mob
        return mob

    # ── cena ─────────────────────────────────────────────────────────────────────────────────────────────────
    def construct(self):
        self.events, self.beats, self.notes = [], [], {}
        self.K, self._raw, self.focus = 1.0, False, None
        self.nat, self.atrasos = {}, {}
        self.sync = json.loads(Path(SYNC).read_text(encoding='utf-8')) if SYNC else None
        self.current = ValueTracker(1)
        self.flow_op = ValueTracker(0)
        self.add(self.backdrop())
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(.4).to_corner(UR, buff=.28).set_z_index(60)
        brand = words('EXERCÍCIO RESOLVIDO · EP. 10', 0, 20, DIM).set_opacity(.75).to_corner(UL, buff=.4)
        self.add(wm, brand)

        self.build_solenoid()
        flow = self.build_flow()
        field, field_glow = self.build_field()
        I_lab = sym('I', CUR).move_to([TOPS[1], YC + A_R + .56, 0])
        B_lab = sym('B', FLD).move_to([3.72, YC + .38, 0])

        # C01 — hook: duas apostas, sem resposta.
        self.beat('C01_hook')
        self.an('hook')
        title = words('ONDE FICA A ENERGIA\nDE UM INDUTOR?', -1.0, 38)
        self.play(FadeIn(title, shift=UP * .08), LaggedStart(Create(self.back), FadeIn(self.bots), FadeIn(self.tops),
                                                             lag_ratio=.25), run_time=1.8)
        self.add(flow)
        self.play(self.flow_op.animate.set_value(1), run_time=.8)
        self.focar(title)
        self.wait(.4)
        gap = (BOTTOMS[6] + BOTTOMS[7]) / 2
        bet_wire = VGroup(words('NO FIO?', 1.05, 24, x=BOTTOMS[2]),
                          Arrow([BOTTOMS[2], 1.32, 0], [BOTTOMS[2], YC - A_R - .24, 0], buff=0, color=DIM,
                                stroke_width=2.4, max_tip_length_to_length_ratio=.25))
        bet_space = VGroup(words('NO ESPAÇO?', 1.05, 24, x=gap),
                           Arrow([gap, 1.32, 0], [gap, YC - .3, 0], buff=0, color=DIM, stroke_width=2.4,
                                 max_tip_length_to_length_ratio=.12))
        self.an('fio')
        self.play(FadeIn(bet_wire[0]), GrowArrow(bet_wire[1]), Indicate(self.tops[2], color=CUR, scale_factor=1.2),
                  run_time=.7)
        self.an('espaco')
        self.play(FadeIn(bet_space[0]), GrowArrow(bet_space[1]), run_time=.7)
        self.an('palpite')
        self.play(Indicate(VGroup(bet_wire[0], bet_space[0]), color=WHITE_, scale_factor=1.08), run_time=.8)

        # C02 — situação: cada variável entra com a sua definição (uma de cada vez).
        self.beat('C02_situacao')
        self.an('cenario')
        self.play(FadeOut(title), FadeOut(bet_wire), FadeOut(bet_space), run_time=.6)
        self.note('n2', tag('SOLENOIDE LONGO · ENROLAMENTO UNIFORME · NÚCLEO DE AR', Y['n2'], size=16))
        self.focar(self.notes['n2'])
        self.wait(.6)
        self.an('sentidos')
        self.play(Indicate(self.tops, color=CUR, scale_factor=1.18), FadeIn(I_lab, shift=DOWN * .05), run_time=.9)
        self.note('n1', defn('I', 'corrente elétrica nas espiras', CUR))
        self.play(Indicate(self.bots, color=CUR, scale_factor=1.18), run_time=.9)
        self.focar(I_lab)
        radius = Arrow([1.8, YC, 0], [1.8, YC + A_R - .2, 0], buff=0, color=GEO, stroke_width=2.8,
                       max_tip_length_to_length_ratio=.14)
        axis = DashedLine([-4.3, YC, 0], [4.3, YC, 0], color=GEO, stroke_width=1.4, dash_length=.1).set_opacity(.4)
        a_lab = sym('a', GEO, 34).move_to([2.08, YC + .78, 0])
        self.an('raio')
        self.play(Create(axis), GrowArrow(radius), FadeIn(a_lab), run_time=.8)
        self.note('n1', defn('a', 'raio do solenoide', GEO), rt=.4)
        self.focar(a_lab)
        n_brace = BraceBetweenPoints([TOPS[6], YC + A_R + .26, 0], [TOPS[8], YC + A_R + .26, 0], UP, color=GEO)
        n_lab = sym('n', GEO).next_to(n_brace, UP, buff=.08)
        self.an('espiras')
        self.play(FadeIn(n_brace), FadeIn(n_lab), Indicate(VGroup(*self.tops[6:9]), color=GEO, scale_factor=1.2),
                  run_time=.8)
        self.note('n1', defn('n', 'espiras por metro', GEO), rt=.4)
        self.focar(n_lab)
        brace = BraceBetweenPoints([H0, YC - A_R - .32, 0], [H1, YC - A_R - .32, 0], DOWN, color=GEO)
        h_lab = sym('h', GEO).next_to(brace, DOWN, buff=.08)
        self.an('trecho')
        self.play(FadeIn(brace), FadeIn(h_lab), run_time=.8)
        self.note('n1', defn('h', 'trecho longe das pontas', GEO), rt=.4)
        self.focar(h_lab)
        self.wait(.6)

        # C03 — Ampère: lei → Bℓ → B.
        self.beat('C03_ampere')
        self.an('campo_q')
        self.play(FadeOut(axis), FadeOut(radius), FadeOut(a_lab), FadeOut(n_brace), FadeOut(n_lab), run_time=.5)
        self.clear_notes(.3)
        self.play(LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=.05), FadeIn(field_glow), FadeIn(B_lab),
                  run_time=1.6)
        self.focar(B_lab)
        chip_t = tag('LEI DE AMPÈRE')
        G = tex('amp0', Y['G'], 44)
        self.an('ampere')
        self.play(FadeIn(chip_t), FadeIn(G, shift=UP * .05), run_time=.8)
        self.focar(G)
        self.wait(.8)
        self.an('mi0')
        self.play(Indicate(glyphs(G, [8, 9]), color=WHITE_, scale_factor=1.3), run_time=.9)
        self.an('iint')
        self.play(Indicate(glyphs(G, [10, 11, 12, 13]), color=CUR, scale_factor=1.2), run_time=.8)
        self.note('n1', defn(r'I_{\text{int}}', 'corrente elétrica total (líquida) que atravessa', CUR))
        self.note('n2', MathTex(r'\text{a área delimitada pelo caminho}', font_size=36, color=DIM)
                  .move_to([0, Y['n2'], 0]).set_z_index(40), rt=.4)
        xm = (TOPS[3] + TOPS[4]) / 2
        xl, xr = xm - .9, xm + .9
        yi, yo = YC + A_R - .45, YC + A_R + .62
        corners = [np.array(p) for p in ([xl, yi, 0], [xr, yi, 0], [xr, yo, 0], [xl, yo, 0])]
        sides = VGroup(*[Line(a, b, color=GEO, stroke_width=2.6) for a, b in zip(corners, corners[1:] + corners[:1])])
        sides.set_z_index(10)
        tips = VGroup()
        for a, b in zip(corners, corners[1:] + corners[:1]):
            mid, d = (a + b) / 2, (b - a) / np.linalg.norm(b - a)
            tips.add(Arrow(mid - d * .17, mid + d * .17, buff=0, color=GEO, stroke_width=0,
                           max_tip_length_to_length_ratio=.6, tip_length=.2))
        tips.set_z_index(11)
        ell = sym(r'\ell', GEO).move_to([xm, yo + .3, 0])
        self.an('retangulo')
        self.clear_notes(.3)
        self.play(Create(sides), run_time=.9)
        self.an('dentro')
        self.play(FadeIn(tips), FadeIn(ell), run_time=.5)
        self.note('n1', line('SÓ O LADO INTERNO CONTA:', (r'\vec B\parallel d\vec\ell', FLD)), rt=.4)
        self.play(Indicate(sides[0], color=FLD, scale_factor=1.0), run_time=1.2)
        self.play(Indicate(VGroup(*[a for a in field if abs(a.get_center()[1] - ROWS[2]) < .1]), color=FLD,
                           scale_factor=1.06), run_time=1.0)
        self.an('verticais')
        self.note('n2', line('NOS LADOS VERTICAIS:', (r'\vec B\perp d\vec\ell', FLD), y=Y['n2']), rt=.4)
        self.play(Indicate(VGroup(sides[1], sides[3]), color=WHITE_, scale_factor=1.0), run_time=1.0)
        self.an('fora')
        self.note('n2', line('FORA:', (r'B\approx0', FLD), y=Y['n2']), rt=.4)
        self.play(Indicate(sides[2], color=WHITE_, scale_factor=1.0), run_time=.9)
        self.an('bl')
        M = self.morph(G, tex('amp1', Y['M']), ([2], [0]), ([6], [1]), ([7], [2]), ([8, 9], [3, 4]),
                       ([10, 11, 12, 13], [5, 6, 7, 8]), ([0, 1, 3, 4, 5], []), keep=True, name='C03_integral_vira_Bl')
        self.focar(M)
        self.wait(.6)
        inside = VGroup(*[w for w, x in zip(self.tops, TOPS) if xl < x < xr])
        self.an('corrente_q')
        self.clear_notes(.3)
        self.note('n1', VGroup(tex('Iint', size=34), words('ESPIRAS DENTRO DO LAÇO × CORRENTE', 0, 18, DIM))
                  .arrange(RIGHT, buff=.25).move_to([0, Y['n1'], 0]), rt=.4)
        self.an('cada_espira')
        self.play(Indicate(inside, color=CUR, scale_factor=1.3), run_time=.9)
        M = self.morph(M, tex('amp', Y['M']), ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]), ([5, 6, 7, 8], [5, 6, 7, 8, 9]),
                       rt=1.2, name='C03_substitui_Iint')
        self.focar(M)
        self.an('comprimento')
        self.play(Indicate(glyphs(M, [1, 7]), color=GEO, scale_factor=1.3), run_time=.9)
        cut = strikes(M[0][1], M[0][7])
        self.an('corta')
        self.play(Create(cut), run_time=.5)
        self.an('campo_res')
        R = self.morph(M, tex('B', Y['M'], 52), ([0], [0]), ([2], [1]), ([3, 4], [2, 3]), ([6], [4]), ([9], [5]),
                       ([1, 5, 7, 8], []), extras=(FadeOut(cut), FadeOut(G)), rt=1.3, name='C03_cancela_ell')
        box = self.result(R)
        self.focar(R)
        self.note('n1', line('CAMPO UNIFORME DENTRO; FORA,', (r'B\approx0', FLD)))
        self.wait(1.0)

        # C04 — fluxo: ∫B·dA → BA.
        self.beat('C04_fluxo')
        self.an('fluxo')
        self.play(FadeOut(chip_t), FadeOut(sides), FadeOut(tips), FadeOut(ell), run_time=.5)
        self.to_note(R, box, rt=.6)
        B_ref = R
        d0 = self.disk(DISKS[0], .03)
        self.play(FadeIn(d0), run_time=.2)
        self.play(Transform(d0, self.disk(DISKS[0])), run_time=.9)
        A_lab = sym('A', GEO).move_to([H0 - .85, YC - A_R - .62, 0])
        A_lead = self.leader(A_lab.get_corner(UR) + [.05, .02, 0], [H0 - .08, YC - A_R + .25, 0])
        self.play(FadeIn(A_lab), Create(A_lead), run_time=.5)
        self.focar(d0)
        chip_t = tag('FLUXO MAGNÉTICO')
        G = tex('phi0', Y['G'], 44)
        self.an('soma_disco')
        self.play(FadeIn(chip_t), FadeIn(G, shift=UP * .05), run_time=.8)
        self.note('n2', defn(r'\Phi', 'quanto campo atravessa uma superfície', FLD, y=Y['n2']), rt=.4)
        self.focar(G)
        self.an('uniforme')
        self.note('n2', line((r'\vec B', FLD), 'UNIFORME E PERPENDICULAR AO DISCO', y=Y['n2']), rt=.4)
        self.play(Indicate(VGroup(*[a for a in field if abs(a.get_center()[0] - H0) < .1]), color=FLD,
                           scale_factor=1.1), run_time=.9)
        self.an('sai_integral')
        M = self.morph(G, tex('phi1', Y['M']), ([0, 1], [0, 1]), ([4], [2], {'path_arc': -.8}), ([2], [3]), ([6], [4]),
                       ([8], [5]), ([3, 5, 7], []), keep=True, rt=1.3, name='C04_B_sai_da_integral')
        self.focar(M)
        self.an('sobra_area')
        self.note('n2', VGroup(tex('dA', size=34), words('ÁREA DO DISCO', 0, 18, DIM)).arrange(RIGHT, buff=.25)
                  .move_to([0, Y['n2'], 0]), rt=.3)
        M = self.morph(M, tex('phiBA', Y['M']), ([0, 1, 2], [0, 1, 2]), ([5], [3]), ([3, 4], []), rt=1.0,
                       extras=(Indicate(d0, color=GEO, scale_factor=1.06),), name='C04_BA')
        self.focar(M)
        self.an('fluxo_ba')
        self.play(FadeOut(G), run_time=.3)
        R = self.morph(M, tex('phi', Y['M'], 52), ([0, 1], [0, 1]), ([2], [2, 3, 4, 5]), ([3], [6, 7, 8]),
                       extras=(Indicate(B_ref, color=FLD, scale_factor=1.1),), rt=1.3, name='C04_substitui')
        box = self.result(R, rt=.4)
        phi_lab = sym(r'\Phi', FLD, 28).move_to([H0, YC + .38, 0])
        self.play(TransformFromCopy(R[0][0], phi_lab), FadeOut(self.notes.pop('n2')), run_time=.7)
        self.focar(R)

        # C05 — fluxo concatenado: o mesmo Φ, N vezes (beat central).
        self.beat('C05_concatenado')
        self.an('muitas')
        self.play(FadeOut(chip_t), FadeOut(A_lab), FadeOut(A_lead), run_time=.4)
        self.to_note(R, box, rt=.6)
        phi_ref = R
        unit = VGroup(d0, phi_lab)
        copies = [unit.copy().set_opacity(0) for _ in DISKS[1:]]
        self.add(*copies)
        self.play(LaggedStart(*[c.animate.move_to(unit.get_center() + RIGHT * (x - H0)).set_opacity(1)
                                for c, x in zip(copies, DISKS[1:])], lag_ratio=.18), run_time=2.2)
        for c in copies:
            c[0].set_fill(opacity=.16)
        units = [unit] + copies
        self.focar(phi_ref)
        chip_t = tag('FLUXO CONCATENADO')
        G = tex('lam', Y['G'], 44)
        self.an('concat')
        self.play(FadeIn(chip_t), FadeIn(G, shift=UP * .05), run_time=.8)
        self.note('n2', line('CADA ESPIRA DO TRECHO ENXERGA O MESMO', (r'\Phi', FLD), y=Y['n2']), rt=.4)
        self.play(Indicate(G[0][0], color=FLD, scale_factor=1.3), run_time=.8)
        self.focar(G)
        self.an('nphi')
        M = self.morph(G, tex('lam1', Y['M']), ([0, 1], [0, 1]), ([2, 5, 12], [3]), ([13], [2]),
                       ([3, 4, 6, 7, 8, 9, 10, 11], []), keep=True, rt=1.4,
                       extras=(LaggedStart(*[Indicate(u[1], color=FLD) for u in units], lag_ratio=.1),),
                       name='C05_todos_iguais')
        self.focar(M)
        self.an('numero')
        N_note = defn('N', 'espiras no trecho', y=Y['n2'])
        self.note('n2', N_note, rt=.4)
        self.play(LaggedStart(*[Indicate(u[0], color=GEO, scale_factor=1.1) for u in units], lag_ratio=.15),
                  Indicate(VGroup(brace, h_lab), color=GEO, scale_factor=1.05), run_time=1.3)
        new = tex('nphi1', Y['M'])
        self.play(FadeOut(G), run_time=.3)
        self.fly(new, [(glyphs(M, [2, 3]), [0, 1]), (M[0][1], [2]), (N_note[0][2:4], [4, 5]),
                       (phi_ref[0][2:9], [8, 9, 10, 11, 12, 13, 14])], rt=1.1, extras=(FadeOut(M),))
        M = new
        self.mark('C05_substitui')
        R = self.morph(M, tex('nphi', Y['M'], 52), ([0, 1, 2], [0, 1, 2]), ([8, 9], [3, 4]), ([4, 10], [5]),
                       ([], [6], {'delay': .5}), ([11], [7]), ([12, 13, 14], [8, 9, 10]), ([5], [11], {'path_arc': -.9}),
                       ([3, 6, 7, 15], []), rt=1.3, name='C05_simplifica')
        box = self.result(R, rt=.4)
        self.focar(R)

        # C06 — indutância; os dois n.
        self.beat('C06_indutancia')
        self.an('indutancia')
        self.clear_notes(.3)
        self.play(FadeOut(chip_t), *[u[0].animate.set_stroke(opacity=.3).set_fill(opacity=.05) for u in units],
                  *[u[1].animate.set_opacity(.3) for u in units], run_time=.5)
        self.to_note(R, box, rt=.6)
        nphi_ref = R
        chip_t = tag('INDUTÂNCIA')
        G = tex('L0', Y['G'], 44)
        self.play(FadeIn(chip_t), run_time=.3)
        self.fly(G, [(glyphs(nphi_ref, [0, 1]), [2, 3]), (I_lab, [5])], rt=1.1)
        self.note('n2', defn('{L}', 'fluxo concatenado por unidade de corrente (henry)', y=Y['n2']), rt=.4)
        self.focar(G)
        self.an('cancela')
        M = self.morph(G, tex('L1', Y['M']), ([0, 1], [0, 1]), ([2, 3], [2, 3, 4, 5, 6, 7, 8, 9, 10]), ([4], [11]),
                       ([5], [12]), keep=True, extras=(Indicate(nphi_ref, color=FLD, scale_factor=1.08),), rt=1.0,
                       name='C06_substitui')
        cut = strikes(M[0][6], M[0][12])
        self.play(Create(cut), run_time=.4)
        self.focar(M)
        self.an('geometria')
        R = self.morph(M, tex('L', Y['M'], 52), ([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]), ([7, 8, 9, 10], [6, 7, 8, 9]),
                       ([6, 11, 12], []), extras=(FadeOut(cut), FadeOut(G)), rt=1.1, name='C06_cancela_I')
        box = self.result(R, rt=.4)
        self.note('n1', line('L SÓ DEPENDE DA GEOMETRIA'), rt=.3)
        self.focar(R)
        nB = tex('B', Y['n1'] - .1, 38, x=-2.3)
        nN = tex('N', Y['n1'] - .1, 38, x=2.3)
        self.an('repara')
        self.play(FadeOut(chip_t), FadeOut(self.notes.pop('n1')), FadeOut(self.notes.pop('n2')), FadeIn(nB), FadeIn(nN),
                  Indicate(glyphs(R, [4, 5]), color=GEO, scale_factor=1.3), run_time=.8)
        n2 = R[0][4]
        rings = VGroup(Circle(radius=.22, color=GEO, stroke_width=2).move_to(nB[0][4]),
                       Circle(radius=.22, color=GEO, stroke_width=2).move_to(nN[0][2])).set_z_index(41)
        tip_y = box.get_bottom()[1] - .06
        links = VGroup(Arrow(rings[0].get_top(), [n2.get_x() - .1, tip_y, 0], buff=.05, color=GEO, stroke_width=2,
                             max_tip_length_to_length_ratio=.1),
                       Arrow(rings[1].get_top(), [n2.get_x() + .1, tip_y, 0], buff=.05, color=GEO, stroke_width=2,
                             max_tip_length_to_length_ratio=.1)).set_z_index(41)
        self.an('fator_campo')
        self.play(Create(rings[0]), GrowArrow(links[0]), Indicate(field, color=FLD, scale_factor=1.04), run_time=1.0)
        self.an('fator_contagem')
        self.play(Create(rings[1]), GrowArrow(links[1]),
                  LaggedStart(*[Indicate(u[0], color=GEO, scale_factor=1.1) for u in units], lag_ratio=.1), run_time=1.1)
        self.wait(.4)

        # C07 — rota do circuito: de onde vem ½LI².
        self.beat('C07_circuito')
        self.an('energia')
        self.play(FadeOut(VGroup(nB, nN, rings, links)), *[FadeOut(u) for u in units], run_time=.5)
        self.to_note(R, box, rt=.6)
        L_ref = R
        chip_t = tag('ENERGIA NO INDUTOR')
        # a corrente volta a zero; depois sobe até I enquanto a energia entra
        self.play(FadeIn(chip_t), self.current.animate.set_value(0), *[a.animate.set_opacity(0) for a in field],
                  *[g.animate.set_stroke(opacity=0) for g in field_glow], run_time=.9)
        self.focar(chip_t)

        def ramp(m, dt):
            self.current.set_value(min(1.0, self.current.get_value() + dt / 8))
            k = self.current.get_value()
            for a in field:
                a.set_opacity(a.base * k)
            for gl in field_glow:
                gl.set_stroke(opacity=gl.base * k)
        driver = Mobject()
        G = tex('emf', Y['G'], 44)
        self.an('fem')
        driver.add_updater(ramp)
        self.add(driver)
        self.play(FadeIn(G, shift=UP * .05), run_time=.8)
        self.note('n2', defn(r'\mathcal{E}_L', 'fem do indutor, contra a variação de I', EMF, y=Y['n2']), rt=.4)
        self.focar(G)
        M = tex('P', Y['M'])
        self.an('potencia')
        self.fly(M, [(glyphs(G, [0, 1]), [3, 4]), (G[0][4], [8]), (glyphs(G, [5, 6, 7, 8, 9]), [10, 11, 12, 13, 14])],
                 rt=1.2)
        self.note('n2', defn('{P}', 'potência que a fonte entrega para vencer a fem', EMF, y=Y['n2']), rt=.4)
        self.focar(M)
        new = tex('dU', Y['M'])
        self.an('du')
        self.fly(new, [(M[0][0], [4]), (glyphs(M, [8, 9]), [8, 9]), (glyphs(M, [10, 11]), [10, 11])],
                 extras=(FadeOut(M), FadeOut(G)), rt=1.2)
        M = new
        self.note('n2', line('EM CADA', (r'dt', WHITE_), ', A ENERGIA GUARDADA CRESCE', (r'P\,dt', EMF), y=Y['n2']), rt=.4)
        self.focar(M)
        self.wait(.6)
        self.play(Indicate(glyphs(M, [8, 9, 10, 11]), color=WHITE_, scale_factor=1.15), run_time=.9)
        self.an('somando')
        self.play(M.animate.move_to([0, Y['G'], 0]).scale(44 / 48), run_time=.6)
        G = M
        M = tex('Uint', Y['M'])
        self.fly(M, [(G[0][8], [6]), (G[0][9], [7]), (glyphs(G, [10, 11]), [9, 10])], rt=1.1)
        self.focar(M)
        R = tex('U0', Y['M'], 52)
        self.an('meio')
        self.play(Indicate(glyphs(M, [13, 14, 15, 16, 17, 18]), color=WHITE_, scale_factor=1.15), run_time=.7)
        self.fly(R, [(glyphs(M, [0, 1, 2]), [0, 1, 2]), (glyphs(M, [13, 14, 15, 16, 17, 18]), [3, 4, 5, 6, 7, 8])],
                 extras=(FadeOut(M), FadeOut(G)), rt=1.1)
        box = self.result(R, rt=.4)
        self.focar(R)
        self.an('guardada')
        self.note('n2', tag('A ENERGIA ENTRA ENQUANTO I SOBE DE 0 A I', Y['n2'], size=17))
        self.play(Indicate(R, color=FLD, scale_factor=1.06), run_time=.9)
        target = tex('U1', Y['M'], 52)
        self.an('com_L')
        R = self.morph(R, target, ([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]), ([6], [6, 7, 8, 9, 10, 11, 12, 13]),
                       ([7, 8], [14, 15]), extras=(Indicate(L_ref, color=WHITE_, scale_factor=1.1),
                                                   box.animate.become(glass(target))), rt=1.3, name='C07_substitui_L')
        self.focar(R)
        pin_chip = tag('ROTA DO CIRCUITO')
        pin = R
        row = VGroup(pin_chip.copy(), pin.copy().scale(.72)).arrange(RIGHT, buff=.3).move_to([0, Y['pin'], 0])
        pin_chip.move_to(row[0])
        self.an('topo')
        self.clear_notes(.3)
        self.play(FadeOut(chip_t), FadeOut(box), pin.animate.scale(.72).move_to(row[1]), FadeIn(pin_chip), run_time=1.0)
        driver.clear_updaters()
        self.remove(driver)
        self.current.set_value(1)
        for a in field:
            a.set_opacity(a.base)
        for gl in field_glow:
            gl.set_stroke(opacity=gl.base)
        self.focar(pin)

        # C08 — rota do campo: u_B (resultado geral), ∫ → u V, μ₀ cancela.
        self.beat('C08_campo')
        chip_t = tag('DENSIDADE DE ENERGIA')
        self.an('segundo')
        self.play(FadeIn(chip_t, shift=UP * .05), Indicate(field, color=FLD, scale_factor=1.04), run_time=.9)
        self.focar(chip_t)
        G = tex('udef', Y['G'], 44)
        self.an('densidade')
        self.play(FadeIn(G, shift=UP * .05), run_time=.8)
        self.note('n2', defn('u_B', 'energia do campo por unidade de volume', FLD, y=Y['n2']), rt=.4)
        self.focar(G)
        gen = tag('RESULTADO GERAL', Y['M'], x=-2.7, size=16)
        M = tex('u', Y['M'], x=1.0)
        self.an('geral')
        self.play(FadeIn(gen), run_time=.5)
        self.fly(M, [(B_lab, [3])], rt=1.1)
        self.note('n2', line('VALE PARA QUALQUER CAMPO MAGNÉTICO NO VÁCUO', y=Y['n2']), rt=.4)
        self.focar(M)
        lit = self.glow()
        self.an('brilho')
        self.play(FadeIn(lit), run_time=1.3)
        self.focar(M)
        G2 = tex('Uint2', Y['G'], 44)
        self.an('somando_vol')
        self.play(FadeOut(G), run_time=.3)
        self.fly(G2, [(glyphs(M, [0, 1]), [4, 5])], rt=1.0)
        G = G2
        self.focar(G)
        self.an('uv')
        self.note('n2', line((r'u_B', FLD), 'UNIFORME DENTRO E ZERO FORA', y=Y['n2']), rt=.4)
        G = self.morph(G, tex('E1', Y['G'], 44), ([0, 1, 2], [0, 1, 2]), ([4, 5], [3, 4]), ([7], [5]), ([3, 6], []),
                       rt=1.1, name='C08_integral_vira_uV')
        self.focar(G)
        sx = ValueTracker(H0 + .001)
        volume = always_redraw(lambda: VGroup(
            Rectangle(width=sx.get_value() - H0, height=2 * A_R - .18, stroke_width=0, fill_color=GEO,
                      fill_opacity=.12).move_to([(H0 + sx.get_value()) / 2, YC, 0]),
            Line([H0, YC + A_R - .09, 0], [sx.get_value(), YC + A_R - .09, 0], color=GEO, stroke_width=1.6),
            Line([H0, YC - A_R + .09, 0], [sx.get_value(), YC - A_R + .09, 0], color=GEO, stroke_width=1.6),
            self.disk(H0).set_fill(opacity=.06).set_stroke(opacity=.6),
            self.disk(sx.get_value())).set_z_index(9))
        self.an('arrastada')
        self.add(volume)
        self.note('n2', defn('V', 'seção A varrida ao longo de h', y=Y['n2']), rt=.3)
        self.play(sx.animate.set_value(H1), run_time=2.0, rate_func=smooth)
        self.an('trocando')
        self.play(FadeOut(gen), run_time=.3)
        M_src = M
        G = self.morph(G, tex('E2', Y['M']), ([0, 1, 2], [0, 1, 2]), ([3, 4], [3, 4, 5, 6, 7, 8]), ([5], [9, 10, 11, 12]),
                       extras=(FadeOut(M_src),), rt=1.1, name='C08_u_e_V')
        self.clear_notes(.3)
        B_ref = tex('B', Y['n1'], 34)
        self.play(FadeIn(B_ref), run_time=.3)
        self.notes['n1'] = B_ref
        self.focar(G)
        self.an('elevando')
        G = self.morph(G, tex('E3', Y['M']), ([0, 1, 2], [0, 1, 2]), ([3], [3, 4, 5, 6, 7, 8]), ([4], [9]),
                       ([5, 6, 7, 8, 9, 10, 11, 12], [10, 11, 12, 13, 14, 15, 16, 17]),
                       extras=(Indicate(B_ref, color=FLD, scale_factor=1.1),), rt=1.1, name='C08_substitui_B')
        G = self.morph(G, tex('E4', Y['M']), ([0, 1, 2], [0, 1, 2]), ([4, 5], [3, 4, 5, 6]), ([6], [7]), ([9], [8, 10]),
                       ([7], [9]), ([3, 8], []), ([10, 11, 12, 13, 14, 15, 16, 17], [11, 12, 13, 14, 15, 16, 17, 18]),
                       rt=1.1, name='C08_expande')
        self.focar(G)
        cut = strikes(glyphs(G, [5, 6]), glyphs(G, [13, 14]))
        self.an('cancela_mu')
        self.note('n2', line('UM', (r'\mu_0', WHITE_), 'DE CIMA CANCELA O', (r'\mu_0', WHITE_), 'DE BAIXO', y=Y['n2']), rt=.3)
        self.play(Create(cut), run_time=.5)
        self.wait(.3)
        R = self.morph(G, tex('E5', Y['M'], 52), ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]),
                       ([7, 8, 9, 10, 11, 12], [5, 6, 7, 8, 9, 10]), ([15, 16, 17, 18], [11, 12, 13, 14]),
                       ([5, 6, 13, 14], []), extras=(FadeOut(cut),), rt=1.2, name='C08_cancela_mu0')
        box = self.result(R, rt=.4)
        self.focar(R)

        # C09 — conferência das duas rotas; o fio apaga, o volume fica aceso.
        self.beat('C09_convergencia')
        self.an('mesma')
        self.clear_notes(.3)
        self.play(FadeOut(chip_t), FadeOut(volume), FadeOut(box), run_time=.4)
        R = self.morph(R, tex('U1', Y['M'], 52), ([0, 1, 2], [0, 1, 2]), ([], [3], {'delay': .4}), ([9], [4]), ([10], [5]),
                       ([3, 4], [6, 7]), ([5, 6], [8, 9]), ([11, 12, 13, 14], [10, 11, 12, 13]),
                       ([7, 8], [14, 15], {'path_arc': -1.0}), rt=1.3, name='C09_mesma_forma')
        top_t = VGroup(pin_chip.copy(), pin.copy().scale(.85 / .72)).arrange(RIGHT, buff=.3).move_to([0, Y['G'], 0])
        camp_chip = tag('ROTA DO CAMPO').move_to([0, Y['M'], 0]).align_to(top_t[0], RIGHT)
        mid_eq = R.copy().scale(.85).move_to([0, Y['M'], 0]).align_to(top_t[1], LEFT)
        self.play(pin_chip.animate.move_to(top_t[0]), pin.animate.become(top_t[1]), R.animate.become(mid_eq),
                  FadeIn(camp_chip), run_time=1.0)
        self.focar(R)
        conf = tex('conf', Y['n1'] - .1, 52)
        lhs, eqs, rhs = glyphs(conf, [0, 1, 2, 3, 4, 5]), conf[0][6], glyphs(conf, [7, 8, 9])
        self.an('conferem')
        self.play(FadeIn(lhs, shift=RIGHT * .1), FadeIn(rhs, shift=LEFT * .1), run_time=.6)
        self.play(FadeIn(eqs, shift=DOWN * .15), run_time=.4)
        self.remove(lhs, eqs, rhs)
        self.add(conf)
        box = self.result(conf, rt=.4)
        self.focar(conf)
        self.an('dois_jeitos')
        self.play(Indicate(pin, color=WHITE_, scale_factor=1.06), run_time=.8)
        self.play(Indicate(R, color=WHITE_, scale_factor=1.06), run_time=.8)
        self.an('pergunta')
        self.play(FadeOut(pin_chip), FadeOut(pin), FadeOut(camp_chip), FadeOut(R),
                  VGroup(conf, box).animate.move_to([0, Y['M'], 0]), run_time=.7)
        self.an('fio_conduz')
        self.play(self.flow_op.animate.set_value(.1), self.back.animate.set_stroke(opacity=.06),
                  self.tops.animate.set_opacity(.2), self.bots.animate.set_opacity(.2), I_lab.animate.set_opacity(.25),
                  FadeOut(brace), FadeOut(h_lab), run_time=1.2)
        u_near = tex('u', YC - A_R - .85, 36)
        self.an('campo_final')
        self.play(FadeIn(u_near, shift=UP * .06), Indicate(lit, color=FLD, scale_factor=1.0), run_time=.8)
        self.note('n1', words('A ENERGIA ESTÁ NO CAMPO', Y['n1'], 30))
        self.focar(self.notes['n1'])
        self.mark('C09_selo')
        self.an('chutou')
        self.play(Indicate(self.notes['n1'], color=FLD, scale_factor=1.06), run_time=.9)

        # C10 — fechamento: somente o handle.
        self.beat('C10_fechamento')
        self.an('cta')
        for m in list(self.mobjects):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.6)
        self.clear()
        self.focus = None
        self.wait(.2)
        handle = words('@labparallax', 0, 48, upper=False).set_color_by_gradient(CYAN, VIOLET, PINK)
        self.play(FadeIn(handle, scale=.96), run_time=.7)
        self.focar(handle)
        self.mark('C10_handle')
        self.wait(1.5)
        self.play(FadeOut(handle), run_time=.5)
        self.wait(.3)
        self.beats[-1][2] = self.time
        self.mark('fim')
        for name, a, b in self.beats:
            print(f'[tempo] {name}: {a:6.1f} s -> {b:6.1f} s ({b - a:5.1f} s)')
        if MEDIR:
            self.nat['_fim'] = round(self.time, 4)
            (UNIT / 'nat.json').write_text(json.dumps(self.nat, indent=1), encoding='utf-8')
        if self.sync:
            pior = max(self.atrasos.values())
            print(f'[sync] atraso máximo da imagem: {pior:+.3f} s ({max(self.atrasos, key=self.atrasos.get)})')
            (Path(config.media_dir) / 'atrasos.json').write_text(json.dumps(self.atrasos, indent=1), encoding='utf-8')
        out = Path(config.media_dir) / 'estados_vid0027.json'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({'eventos': self.events, 'beats': [{'beat': n, 'inicio': round(a, 2), 'fim': round(b, 2)}
                                                                     for n, a, b in self.beats],
                                   'duracao': round(self.time, 2)}, ensure_ascii=False, indent=1), encoding='utf-8')
