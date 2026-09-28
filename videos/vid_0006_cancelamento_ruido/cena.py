"""Interferência de ondas e cancelamento ativo de ruído; preview sincronizado com a narração.

DA EQUAÇÃO AO FENÔMENO · EP. 02. Regime acústico linear: p_total = p₁ + p₂.
Modelo ideal: p₁ = A sin ωt, p₂ = A sin(ωt + φ), amplitude 2A|cos(φ/2)|;
φ: 0 → π leva 2A → 0 (“= 0” só neste modelo). Aplicação: p_fone = −g·p_ruído(t − τ);
com um único tom equivale a B = gA, φ = π − ωτ, e o residual nunca é zero.
No ar, as fileiras mostram deslocamento longitudinal s (não p); p(t) só nos gráficos.

Cores: ciano = p₁/ruído; magenta = p₂/fone; branco = soma/resultante;
azul = eixos/fone; violeta = processamento/atraso.
"""

from pathlib import Path
from types import SimpleNamespace

import numpy as np
from manim import (
    DEGREES, DOWN, LEFT, PI, RIGHT, UP, Arc, Circle, Create, CurvedArrow, DashedLine, DashedVMobject,
    Dot, FadeIn, FadeOut, ImageMobject, Indicate, LaggedStart, Line, MathTex, MoveAlongPath,
    Polygon, Rectangle, ReplacementTransform, RoundedRectangle, Scene, Square, SurroundingRectangle,
    TransformMatchingTex, VGroup,
    VMobject, ValueTracker, always_redraw, linear, there_and_back,
)

from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # p₁ / ruído externo
MAGENTA = "#EA63FF"       # p₂ / contribuição do fone
BLUE = "#267BFF"          # eixos, fone, ícones
VIOLET = SECONDARY_COLOR  # processamento, atraso

SAFE_BOTTOM = -4.6        # abaixo disso: faixa reservada a legendas
SAFE_X = 3.5              # |x| máximo do conteúdo
HEADLINE_TOP = 6.85

# Gráfico p(t) (C2–C6): dois períodos em x ∈ [GX0, GX1]; mesma escala nas três faixas.
GX0, GX1 = -3.2, 2.8
A_G = 0.65
Y_P1, Y_P2, Y_SUM = 4.35, 2.45, -0.35
X_PROBE = -2.45           # primeiro pico de p₁ (ωt = π/2)
Y_EQ, Y_TAG = -2.6, -3.6

# Inset p(t) em x₀ (C7)
IX0, IX1, IY, A_I = -2.5, 2.5, 4.2, 0.45

# Ar (C7–C14): camadas com deslocamento longitudinal s = s₀ sin(kx − ω_a t + φ)
LAMBDA = 3.1
K = 2 * PI / LAMBDA
S0 = 0.55 / K             # s₀k = 0,55: camadas nunca se cruzam
W_AIR = 2 * PI / 1.6
AIR_X = np.linspace(-3.1, 3.1, 26)
Y_AIR = (2.1, 0.2, -1.7)
X0_PROBE = 1.6

# Fone em corte lateral; eixo do ouvido em y = EAR_Y
EAR_Y = 2.4
DRIVER = np.array([1.45, EAR_Y, 0.0])
REGION = np.array([2.5, EAR_Y, 0.0])   # região perto do ouvido, diante do canal
REGION_R = 0.28
MIC_EXT = np.array([0.1, 3.9, 0.0])
MIC_INT = np.array([2.2, 3.1, 0.0])
CHIP = np.array([0.6, 1.2, 0.0])

# Painel “perto do ouvido”: dois períodos do fundamental
PX0, PX1, PY, A_P = -3.0, 2.9, -2.95, 0.95
PANEL_TOP = -1.15         # caixa do painel: y de −4,45 a −1,15
Y_PANEL_EQ = -0.65

AUDIO_PATH = Path(__file__).parent / "audio" / "narracao_final.wav"  # ElevenLabs, intacta

# Termos coloridos na legenda (montar_legendado.py --color-module), com o mesmo significado da cena.
SUBTITLE_TERM_COLORS = {
    "ruído": CYAN,
    "onda magenta": MAGENTA,
    "outra contribuição sonora": MAGENTA,
    "outra contribuição": MAGENTA,
    "processamento": VIOLET,
    "mesmo atraso": VIOLET,
}


# ── Modelo físico: as curvas na tela usam exatamente estas funções ──────────
def p_sum(wt, phi):
    return np.sin(wt) + np.sin(wt + phi)


def noise(wt, c):
    return np.sin(wt) + c * np.sin(3 * wt + 0.6)


def fone(wt, g, wtau, c):
    return -g * noise(wt - wtau, c)


def residual(wt, g, wtau, c):
    return noise(wt, c) + fone(wt, g, wtau, c)


def _peak(values):
    return float(np.max(np.abs(values)))


_WT = np.linspace(0, 2 * PI, 4001)
assert abs(_peak(p_sum(_WT, 0)) - 2) < 1e-6                         # construtiva: 2A
assert abs(_peak(p_sum(_WT, PI / 2)) - np.sqrt(2)) < 1e-6          # φ = π/2: √2 A (não A)
assert _peak(p_sum(_WT, PI)) < 1e-9                                 # destrutiva ideal: 0
for _phi in np.linspace(0, PI, 9):                                  # colchete: 2A|cos(φ/2)| = pico da soma
    assert abs(_peak(p_sum(_WT, _phi)) - 2 * abs(np.cos(_phi / 2))) < 1e-6
assert abs(_peak(residual(_WT, 0.90, 0.05 * PI, 0)) - 0.179) < 0.002  # B=0,9A, φ=0,95π
assert abs(_peak(residual(_WT, 0.95, 0.03 * PI, 0)) - 0.105) < 0.002  # B=0,95A, φ=0,97π


# ── Helpers visuais ─────────────────────────────────────────────────────────
def tex(content, size=40, color=WHITE):
    return MathTex(content, font_size=size, color=color)


def ctex(*parts, size=44):
    """MathTex com cor por termo: parts = (latex, cor)."""
    m = MathTex(*(p for p, _ in parts), font_size=size)
    for i, (_, color) in enumerate(parts):
        m[i].set_color(color)
    return m


def text(content, size=24, color=WHITE, opacity=1.0, **kwargs):
    return screen_text(content, size, color=color, **kwargs).set_opacity(opacity)


def display(content, size=38):
    return screen_text(content, size, oversample=2, color=WHITE)


def left_at(mob, x, y):
    return mob.move_to([x + mob.width / 2, y, 0])


def fit(mob, max_width=5.0):
    """Limita a largura: centrada em x = −0,3, termina antes da guia do painel (x = 2,5)."""
    return mob.scale_to_fit_width(min(mob.width, max_width))


def period_mark(x0, x1, y):
    return VGroup(Line([x0, y, 0], [x1, y, 0]), *(Line([x, y - 0.08, 0], [x, y + 0.08, 0]) for x in (x0, x1))
                  ).set_stroke(WHITE, 2, 0.7)


def poly(xs, ys, color, width, opacity=1.0):
    pts = np.column_stack([xs, ys, np.zeros_like(xs)])
    return VMobject().set_points_as_corners(pts).set_stroke(color, width, opacity)


def gwt(x):
    """ωt no gráfico ideal: dois períodos entre GX0 e GX1."""
    return 2 * PI * (np.asarray(x) - GX0) / 3.0


def axis(x0, x1, y):
    line = Line([x0, y, 0], [x1 + 0.1, y, 0]).set_stroke(BLUE, 2, 0.5)
    t = tex("t", 26).set_opacity(0.6).move_to([x1 + 0.22, y - 0.22, 0])
    return VGroup(line, t)


def stack(x, a, b):
    """Soma ponto a ponto na faixa soma: barra ciano 0→p₁, magenta p₁→p₁+p₂, ponto branco."""
    y1 = Y_SUM + A_G * a
    y2 = y1 + A_G * b
    return VGroup(Line([x - 0.07, Y_SUM, 0], [x - 0.07, y1 + 1e-4, 0]).set_stroke(CYAN, 6),
                  Line([x + 0.07, y1, 0], [x + 0.07, y2 + 1e-4, 0]).set_stroke(MAGENTA, 6),
                  Dot([x, y2, 0], 0.08, color=WHITE))


def bracket(h):
    x, y1 = 3.05, Y_SUM + max(h, 1e-3)
    return VGroup(Line([x, Y_SUM, 0], [x, y1, 0]), Line([x - 0.08, y1, 0], [x + 0.08, y1, 0]),
                  Line([x - 0.08, Y_SUM, 0], [x + 0.08, Y_SUM, 0])).set_stroke(WHITE, 2, 0.7)


def region_mark():
    return DashedVMobject(Circle(radius=REGION_R).move_to(REGION), num_dashes=14).set_stroke(WHITE, 2, 0.8)


def guide_line():
    return DashedLine(REGION + DOWN * (REGION_R + 0.04), [REGION[0], PANEL_TOP, 0]).set_stroke(WHITE, 2, 0.4)


def smooth(points):
    return VMobject().set_points_smoothly([[x, y, 0] for x, y in points])


def leader(start, end):
    return Line([*start, 0], [*end, 0]).set_stroke(WHITE, 1.5, 0.6)


def build_fone():
    head = VGroup(Line([2.95, 4.9, 0], [2.95, 2.62, 0]), Line([2.95, 2.18, 0], [2.95, -0.1, 0]),
                  Line([2.95, 2.62, 0], [3.3, 2.62, 0]), Line([2.95, 2.18, 0], [3.3, 2.18, 0]),
                  ).set_stroke(BLUE, 3, 0.45)
    # Orelha: aba superior e lóbulo abertos para o canal, fora do círculo da região.
    ear = VGroup(smooth([(2.95, 3.35), (2.62, 3.15), (2.52, 2.9), (2.62, 2.75)]),
                 smooth([(2.95, 1.45), (2.6, 1.65), (2.52, 1.9), (2.62, 2.05)])).set_stroke(BLUE, 3, 0.8)
    head.add(ear)
    shell = VMobject().set_points_as_corners(
        [[2.75, 4.5, 0], [0.55, 4.5, 0], [0.1, 4.05, 0], [0.1, 0.75, 0], [0.55, 0.3, 0], [2.75, 0.3, 0]]
    ).set_stroke(BLUE, 4)
    cushions = VGroup(*(RoundedRectangle(width=0.22, height=0.6, corner_radius=0.1).move_to([2.84, y, 0])
                        for y in (4.22, 0.58))).set_stroke(BLUE, 2).set_fill(BLUE, 0.25)
    paths = [VMobject().set_points_as_corners(p) for p in (
        [MIC_EXT + [0.09, 0, 0], [0.45, 3.9, 0], [0.45, 1.45, 0]],
        [MIC_INT + [0, 0.09, 0], [2.2, 3.6, 0], [0.75, 3.6, 0], [0.75, 1.45, 0]],
        [[0.85, 1.2, 0], [1.24, 1.2, 0], [1.24, 2.25, 0]],
    )]
    wires = VGroup(*paths).set_stroke(BLUE, 2, 0.45)
    driver = VGroup(Line([1.4, 1.7, 0], [1.4, 3.1, 0]).set_stroke(BLUE, 5),
                    Polygon([1.4, 2.05, 0], [1.4, 2.75, 0], [1.08, 2.6, 0], [1.08, 2.2, 0])
                    .set_stroke(BLUE, 3).set_fill(BLUE, 0.2))
    chip = Square(0.5).move_to(CHIP).set_stroke(VIOLET, 3).set_fill(VIOLET, 0.15)
    mics = VGroup(Dot(MIC_EXT, 0.09, color=BLUE), Dot(MIC_INT, 0.09, color=BLUE))
    # Identificação explícita: trecho da haste sobre a cabeça + rótulo ligado à concha.
    band = smooth([(2.3, 4.5), (2.5, 4.95), (2.95, 5.25), (3.35, 5.35)]).set_stroke(BLUE, 6)
    name = VGroup(text("fone de ouvido", 24).move_to([-1.5, 3.6, 0]), leader((-0.6, 3.6), (0.08, 3.4)))
    rest = VGroup(head, cushions, band, wires, driver, chip, mics, name)
    return SimpleNamespace(shell=shell, rest=rest, body=VGroup(shell, rest),
                           mics=mics, chip=chip, driver=driver, paths=paths)


def build_icons():
    def plane(c):
        wing = lambda s: Polygon(c + [0.1, 0.1 * s, 0], c + [-0.2, 0.5 * s, 0],
                                 c + [-0.36, 0.5 * s, 0], c + [-0.18, 0.1 * s, 0])
        return VGroup(RoundedRectangle(width=1.2, height=0.2, corner_radius=0.1).move_to(c),
                      wing(1), wing(-1),
                      Polygon(c + [-0.44, 0.1, 0], c + [-0.56, 0.36, 0], c + [-0.64, 0.36, 0], c + [-0.6, 0.1, 0]))

    def bus(c):
        return VGroup(RoundedRectangle(width=1.2, height=0.5, corner_radius=0.1).move_to(c + [0, 0.08, 0]),
                      *(Rectangle(width=0.22, height=0.16).move_to(c + [x, 0.16, 0]) for x in (-0.36, -0.06, 0.24)),
                      *(Circle(radius=0.11).move_to(c + [x, -0.2, 0]) for x in (-0.32, 0.32)))

    def ac(c):
        return VGroup(RoundedRectangle(width=1.2, height=0.5, corner_radius=0.1).move_to(c),
                      *(Line(c + [-0.4, y, 0], c + [0.4, y, 0]) for y in (-0.06, -0.15)),
                      Circle(radius=0.04).move_to(c + [0.42, 0.12, 0]))

    icons = VGroup()
    for x, draw, name in ((-2.3, plane, "AVIÃO"), (0.0, bus, "MOTOR"), (2.3, ac, "AR-CONDICIONADO")):
        c = np.array([x, 3.9, 0.0])
        icons.add(VGroup(draw(c).set_stroke(BLUE, 3).set_fill(opacity=0),
                         text(name, 18, opacity=0.8).move_to([x, 3.0, 0])))
    return icons


def wave_strip(y, cycles):
    xs = np.linspace(-3.0, 3.0, 300)
    return VGroup(axis(-3.0, 3.0, y), poly(xs, y + 0.7 * np.sin(2 * PI * cycles * (xs + 3.0) / 6.0), CYAN, 4))


class CancelamentoRuido006(Scene):
    def check_safe_area(self):
        vms = [m for m in self.mobjects if isinstance(m, VMobject) and len(m.get_all_points())]
        bottom = min(m.get_bottom()[1] for m in vms)
        assert bottom > SAFE_BOTTOM, f"conteúdo invade a faixa inferior: {bottom:.2f}"
        for m in vms:
            if m is not self.series:
                assert m.get_left()[0] > -SAFE_X and m.get_right()[0] < SAFE_X, \
                    f"conteúdo fora da margem lateral: {m.get_left()[0]:.2f}..{m.get_right()[0]:.2f}"

    def caption(self, *lines):
        """Troca a manchete do topo; devolve as animações."""
        new = VGroup(*(display(line) for line in lines)).arrange(DOWN, buff=0.14)
        if new.width > 2 * SAFE_X - 0.2:
            new.scale_to_fit_width(2 * SAFE_X - 0.2)
        new.move_to([0, HEADLINE_TOP - new.height / 2, 0])
        anims = [FadeIn(new, shift=DOWN * 0.15)]
        if self.headline is not None:
            anims.append(FadeOut(self.headline, shift=UP * 0.15))
        self.headline = new
        return anims

    def swap_eq(self, new, *extra):
        anims = [FadeIn(new, shift=UP * 0.1)]
        if self.eq is not None:
            anims.append(FadeOut(self.eq, shift=UP * 0.1))
        self.play(*anims, *extra, run_time=0.6)
        self.eq = new

    def until(self, seconds):
        """Espera até o instante `seconds` da narração (segundos do WAV; tolera ~1 frame a 15 fps)."""
        remaining = seconds - self.time
        assert remaining > -0.1, f"linha do tempo atrasada: {self.time:.2f} s > {seconds} s"
        if remaining > 1e-6:
            self.wait(remaining)

    def air_row(self, color, phases, y, xmax=None):
        """Camadas de ar; só deslocamento em x. y e xmax: número ou ValueTracker."""
        val = lambda v: v.get_value() if isinstance(v, ValueTracker) else v

        def build():
            yy, xm, t = val(y), (val(xmax) if xmax is not None else 99.0), self.air.get_value()
            s = sum(S0 * np.sin(K * AIR_X - W_AIR * t + ph) for ph in phases)
            row = VGroup()
            for x0, dx in zip(AIR_X, s):
                op = float(np.clip((xm - x0) / 0.5, 0, 1))
                if op > 0:
                    row.add(Line([x0 + dx, yy - 0.4, 0], [x0 + dx, yy + 0.4, 0]).set_stroke(color, 4, op))
            return row
        return always_redraw(build)

    def arcs(self, emit):
        def build():
            group = VGroup()
            for k in range(3):
                f = (self.clock.get_value() / 1.2 + k / 3) % 1
                group.add(Arc(radius=0.25 + 0.75 * f, start_angle=-35 * DEGREES, angle=70 * DEGREES,
                              arc_center=DRIVER).set_stroke(MAGENTA, 4, emit.get_value() * (1 - f)))
            return group
        return always_redraw(build)

    def amp_bars(self):
        """Amplitudes na mesma escala do painel: ruído (ciano) e residual (branco), picos das curvas."""
        anc, wt = self.anc, np.linspace(0, 2 * PI, 721)

        def build():
            g, wtau, c = anc.g.get_value(), anc.wtau.get_value(), anc.c.get_value()
            a_n, a_r = _peak(noise(wt, c)), max(_peak(residual(wt, g, wtau, c)), 1e-3)
            return VGroup(Line([-3.28, PY, 0], [-3.28, PY + A_P * a_n, 0]).set_stroke(CYAN, 5),
                          Line([-3.14, PY, 0], [-3.14, PY + A_P * a_r, 0]).set_stroke(WHITE, 5))
        return always_redraw(build)

    def build_panel(self):
        anc = self.anc
        box = RoundedRectangle(width=6.8, height=3.3, corner_radius=0.2).move_to([0, PANEL_TOP - 1.65, 0])
        box.set_stroke(BLUE, 2, 0.5).set_fill(BACKGROUND_COLOR, 0.9)
        title = left_at(text("PERTO DO OUVIDO", 20, opacity=0.85), -3.2, PANEL_TOP - 0.23)
        xs = np.linspace(PX0, PX1, 300)
        wt = 4 * PI * (xs - PX0) / (PX1 - PX0)
        state = lambda: (anc.g.get_value(), anc.wtau.get_value(), anc.c.get_value())
        cn = always_redraw(lambda: poly(xs, PY + A_P * noise(wt, anc.c.get_value()), CYAN, 3))
        cf = always_redraw(lambda: poly(xs, PY + A_P * fone(wt, *state()), MAGENTA, anc.w_mag.get_value()))
        cr = always_redraw(lambda: poly(xs, PY + A_P * residual(wt, *state()), WHITE, anc.w_res.get_value()))
        return VGroup(box, title, axis(PX0, PX1, PY), cn, cf, cr)

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.headline = None
        self.eq = None
        watermark = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(watermark.to_corner(UP + RIGHT, buff=0.28))
        self.series = text("DA EQUAÇÃO AO FENÔMENO · EP. 02", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4)

        # Relógios com updater dependente de dt: mantêm as esperas animadas.
        self.clock = ValueTracker(0)
        self.clock.add_updater(lambda m, dt: m.increment_value(dt))
        self.air_rate = ValueTracker(1)
        self.air = ValueTracker(0)
        self.air.add_updater(lambda m, dt: m.increment_value(dt * self.air_rate.get_value()))
        self.add(self.clock, self.air)

        anc = self.anc = SimpleNamespace(g=ValueTracker(0), wtau=ValueTracker(0.03 * PI), c=ValueTracker(0),
                                         w_mag=ValueTracker(3), w_res=ValueTracker(5))
        cy, cx = ValueTracker(EAR_Y), ValueTracker(-0.4)   # fileira ciano: altura e borda direita
        emit = ValueTracker(0)                              # intensidade dos arcos do driver

        # Tempos = segundos de audio/narracao_final.wav (pausas medidas); comentários citam a fala.
        self.add_sound(str(AUDIO_PATH))

        # ── C1. Gancho (0–5,6) ───────────────────────────────────────────────
        f1 = build_fone()
        noise_1 = self.air_row(CYAN, (0,), cy, cx)
        arcs_1 = self.arcs(emit)
        region_1, guide_1, panel_1 = region_mark(), guide_line(), self.build_panel()
        self.add(arcs_1)
        self.play(FadeIn(self.series), *self.caption("O som pode cancelar", "o próprio som?"),   # "O som pode cancelar…"
                  FadeIn(f1.body, noise_1), run_time=1.0)
        self.until(1.5)
        self.play(FadeIn(region_1, guide_1, panel_1), run_time=0.6)
        self.until(2.74)                                  # "É isso que um fone com cancelamento de ruído explora."
        self.play(anc.g.animate.set_value(0.95), emit.animate.set_value(1), run_time=2.5)
        self.check_safe_area()

        # ── C2. Volta à física (5,6–9,95) ────────────────────────────────────
        self.until(5.6)                                   # "Pra entender como, vamos voltar à física…"
        self.play(FadeOut(VGroup(f1.body, noise_1, arcs_1, region_1, guide_1, panel_1, self.headline),
                          shift=UP * 0.4, scale=0.85), run_time=0.7)
        self.headline = None
        emit.set_value(0)
        phi = ValueTracker(0)
        xs_g = np.linspace(GX0, GX1, 240)
        wt_g = gwt(xs_g)
        ax1, ax2, axs = axis(GX0, GX1, Y_P1), axis(GX0, GX1, Y_P2), axis(GX0, GX1, Y_SUM)
        c1 = poly(xs_g, Y_P1 + A_G * np.sin(wt_g), CYAN, 4)
        c2 = always_redraw(lambda: poly(xs_g, Y_P2 + A_G * np.sin(wt_g + phi.get_value()), MAGENTA, 4))
        lab1 = left_at(tex(r"p_1 = A\sin(\omega t)", 38, CYAN), GX0, Y_P1 + 0.95)
        lab2 = left_at(tex(r"p_2 = A\sin(\omega t)", 38, MAGENTA), GX0, Y_P2 + 0.95)
        self.play(FadeIn(ax1, lab1), Create(c1), run_time=0.9)
        self.play(FadeIn(ax2, lab2), Create(c2), run_time=0.9)
        self.until(8.19)                                  # "…interferência de ondas."
        self.play(*self.caption("Interferência de ondas"), run_time=0.6)

        # ── C3. Superposição (9,95–18,0) ─────────────────────────────────────
        self.until(9.95)                                  # "Este gráfico mostra a pressão num ponto…"
        nota = text("PRESSÃO EM UM PONTO · AO LONGO DO TEMPO", 24, opacity=0.75, oversample=2)
        nota = fit(nota, 6.6).move_to([0, 5.95, 0])
        self.play(*self.caption("Superposição"), FadeIn(nota), run_time=0.8)
        labs = left_at(tex(r"p_{\text{total}}", 38), GX0, Y_SUM + 1.7)
        self.until(11.3)
        self.play(FadeIn(axs, labs), run_time=0.6)
        self.until(12.2)
        self.swap_eq(ctex((r"p_{\text{total}}", WHITE), ("=", WHITE), ("p_1", CYAN), ("+", WHITE), ("p_2", MAGENTA))
                     .move_to([0, Y_EQ, 0]))

        xscan = ValueTracker(GX0 + 0.02)

        def partial_sum():
            mask = xs_g <= xscan.get_value()
            mask[:2] = True
            return poly(xs_g[mask], Y_SUM + A_G * p_sum(wt_g[mask], phi.get_value()), WHITE, 6)

        def scan_marks():
            x, ph = xscan.get_value(), phi.get_value()
            a, b = np.sin(gwt(x)), np.sin(gwt(x) + ph)
            return VGroup(DashedLine([x, Y_P1 + 0.8, 0], [x, Y_SUM - 1.4, 0]).set_stroke(BLUE, 2, 0.6),
                          Dot([x, Y_P1 + A_G * a, 0], 0.07, color=CYAN),
                          Dot([x, Y_P2 + A_G * b, 0], 0.07, color=MAGENTA),
                          stack(x, a, b))

        csum = always_redraw(partial_sum)
        scanner = always_redraw(scan_marks)
        self.until(13.21)                                 # "As duas pressões se somam, e a curva branca nasce…"
        self.add(csum)
        self.play(FadeIn(scanner), run_time=0.3)
        self.play(xscan.animate.set_value(GX1), run_time=3.2, rate_func=linear)
        self.until(16.87)                                 # "…superposição."
        self.play(FadeOut(scanner), run_time=0.5)
        self.check_safe_area()

        # ── C4. Construtiva (18,0–24,8) ──────────────────────────────────────
        self.until(18.02)                                 # "Em fase,"
        self.play(*self.caption("Em fase"), run_time=0.6)
        crest = DashedLine([X_PROBE, Y_P1 + 0.8, 0], [X_PROBE, Y_SUM - 1.4, 0]).set_stroke(WHITE, 2, 0.35)
        probe = always_redraw(lambda: stack(X_PROBE, 1.0, np.sin(PI / 2 + phi.get_value())))
        self.until(18.79)                                 # "…crista encontra crista e vale encontra vale."
        self.play(Create(crest), FadeIn(probe), run_time=0.6)
        self.until(21.56)                                 # "As ondas se reforçam:"
        self.swap_eq(ctex(("A", CYAN), ("+", WHITE), ("A", MAGENTA), ("=", WHITE), ("2A", WHITE))
                     .move_to([0, Y_EQ, 0]))
        amp = always_redraw(lambda: bracket(A_G * 2 * abs(np.cos(phi.get_value() / 2))))
        lab_2a = tex("2A", 32).move_to([2.72, Y_SUM + 2 * A_G, 0])
        self.play(FadeIn(amp, lab_2a), run_time=0.5)
        self.until(22.96)                                 # "…interferência construtiva."
        tag = text("CONSTRUTIVA", 30, opacity=0.9).move_to([0, Y_TAG, 0])
        self.play(FadeIn(tag), run_time=0.5)
        self.check_safe_area()

        # ── C5. Mudança contínua de fase: a amplitude vem da equação (24,8–35,8)
        self.until(24.82)                                 # "Agora deslocamos a fase da onda magenta."
        self.play(*self.caption("Diferença de fase"), FadeOut(tag, self.eq), run_time=0.6)
        self.eq = None
        lab2b = left_at(tex(r"p_2 = A\sin(\omega t + \phi)", 38, MAGENTA), GX0, Y_P2 + 0.95)
        self.play(ReplacementTransform(lab2, lab2b), run_time=0.4)
        full = fit(ctex((r"p_{\text{total}}", WHITE), ("=", WHITE), (r"2A\cos(\phi/2)", WHITE),
                        (r"\sin(\omega t+\phi/2)", WHITE), size=42), 6.6).move_to([0, Y_EQ, 0])
        self.play(FadeIn(full, shift=UP * 0.1), run_time=0.6)
        # Fator de amplitude destacado e ligado ao colchete, que passa a se chamar A_res.
        box = SurroundingRectangle(full[2], color=WHITE, buff=0.08, stroke_width=2)
        box_note = VGroup(text("AMPLITUDE", 20, opacity=0.85), tex(r"(0\le\phi\le\pi)", 30)).arrange(RIGHT, buff=0.12)
        box_note.next_to(box, DOWN, buff=0.14)
        link = DashedLine(box.get_corner(UP + RIGHT), [3.05, Y_SUM - 0.05, 0]).set_stroke(WHITE, 2, 0.5)
        ares_lab = always_redraw(lambda: tex(r"A_{\text{res}}", 30).move_to(
            [3.05, Y_SUM + A_G * 2 * abs(np.cos(phi.get_value() / 2)) + 0.25, 0]))
        self.until(27.38)                                 # "O fator destacado determina a amplitude da soma."
        self.play(Create(box), FadeIn(box_note), Create(link), ReplacementTransform(lab_2a, ares_lab),
                  Indicate(amp, color=WHITE, scale_factor=1.1), run_time=0.8)
        # Fica só a amplitude, com um único valor que muda nos estados 0, π/2 e π.
        ares = ctex((r"A_{\text{res}}", WHITE), ("=", WHITE), (r"2A\left|\cos(\phi/2)\right|", WHITE), ("=", WHITE),
                    size=42)
        values = [tex(v, 42) for v in ("2A", r"\sqrt{2}\,A", "0")]
        VGroup(ares, values[1].copy()).arrange(RIGHT, buff=0.15).move_to([0, Y_EQ, 0])  # centrado pelo mais largo
        for v in values:
            v.next_to(ares, RIGHT, buff=0.15)
        self.until(29.3)
        self.play(ReplacementTransform(full[2], ares[2]), FadeOut(full[0], full[1], full[3], box, box_note, link),
                  FadeIn(ares[0], ares[1], ares[3], values[0]), run_time=0.7)
        y_sl = Y_TAG
        slider = VGroup(
            Line([-2, y_sl, 0], [2, y_sl, 0]).set_stroke(BLUE, 3, 0.7),
            *(Line([x, y_sl - 0.1, 0], [x, y_sl + 0.1, 0]).set_stroke(BLUE, 3, 0.7) for x in (-2, 0, 2)),
            tex("0", 30).move_to([-2, y_sl - 0.4, 0]), tex(r"\pi/2", 30).move_to([0, y_sl - 0.4, 0]),
            tex(r"\pi", 30).move_to([2, y_sl - 0.4, 0]),
            tex(r"\phi", 40, MAGENTA).move_to([-2.45, y_sl, 0]),
            always_redraw(lambda: Dot([-2 + 4 * phi.get_value() / PI, y_sl, 0], 0.1, color=MAGENTA)))
        self.play(FadeIn(slider), run_time=0.4)
        value = values[0]
        # "Repare na curva branca: de zero a meio ciclo, sua amplitude cai até zero." (30,33–34,66)
        for target, nxt, sweep in ((PI / 2, values[1], 2.2), (PI, values[2], 1.8)):
            # Enquanto φ anda, o valor exato anterior esmaece; na chegada, vira o novo valor exato.
            self.play(phi.animate.set_value(target), value.animate.set_opacity(0.3), run_time=sweep, rate_func=linear)
            self.play(ReplacementTransform(value, nxt), run_time=0.4)
            value = nxt
            if target < PI:
                self.wait(0.5)                            # pausa em π/2: √2 A, estado intermediário
        self.check_safe_area()

        # ── C6. Cancelamento como transformação matemática (35,8–44,6) ────────
        self.until(35.8)                                  # "Com meio ciclo de diferença…" (34,80)
        self.play(*self.caption("Fases opostas"), FadeOut(slider, ares, value), run_time=0.6)
        y1, y2 = Y_EQ + 0.15, Y_EQ - 0.6                  # linha de p₂ e linha da soma
        p2_a = ctex(("p_2", MAGENTA), ("=", WHITE), (r"A\sin(\omega t+\pi)", MAGENTA)).move_to([0, y1, 0])
        p2_b = ctex(("p_2", MAGENTA), ("=", WHITE), ("-", WHITE), (r"A\sin(\omega t)", CYAN)).move_to([0, y1, 0])
        p2_c = ctex(("p_2", MAGENTA), ("=", WHITE), ("-", WHITE), ("p_1", CYAN)).move_to([0, y1, 0])
        sum_a = ctex((r"p_{\text{total}}", WHITE), ("=", WHITE), ("p_1", CYAN), ("+", WHITE), ("p_2", MAGENTA)
                     ).move_to([0, y2, 0])
        sum_b = ctex((r"p_{\text{total}}", WHITE), ("=", WHITE), ("p_1", CYAN), ("-", WHITE), ("p_1", CYAN)
                     ).move_to([0, y2, 0])
        sum_c = ctex((r"p_{\text{total}}", WHITE), ("=", WHITE), ("0", WHITE)).move_to([0, y2, 0])
        ideal = text("CASO IDEAL", 22, opacity=0.85).move_to([0, y2 - 0.5, 0])
        glow = poly(xs_g, Y_SUM + 0 * xs_g, WHITE, 14, 0.25)
        self.play(FadeIn(p2_a, shift=UP * 0.1), run_time=0.5)
        self.play(crest.animate(rate_func=there_and_back).set_stroke(opacity=0.9), run_time=0.8)  # "…crista encontra vale."
        self.until(37.74)                                 # "Se as amplitudes são iguais,"
        self.play(TransformMatchingTex(p2_a, p2_b), run_time=0.6)          # sin(ωt + π) = −sin(ωt)
        self.until(38.5)
        self.play(TransformMatchingTex(p2_b, p2_c), run_time=0.6)          # −A sin(ωt) é −p₁
        self.until(39.24)                                 # "…uma compensa a outra"
        self.play(FadeIn(sum_a, shift=UP * 0.1), run_time=0.5)
        self.until(40.5)                                  # "…e, nesse caso ideal,"
        self.play(TransformMatchingTex(sum_a, sum_b), run_time=0.6)
        self.until(41.71)                                 # "…a soma é zero:"
        self.play(TransformMatchingTex(sum_b, sum_c), FadeIn(ideal), FadeIn(glow), run_time=0.7)
        self.until(42.79)                                 # "…interferência destrutiva."
        tag = text("DESTRUTIVA", 30, opacity=0.9).move_to([0, y2 - 1.05, 0])
        self.play(FadeIn(tag), FadeOut(glow), run_time=0.5)
        self.eq = VGroup(p2_c, sum_c, ideal)
        self.check_safe_area()

        # ── C7. Significado físico (44,6–56,1) ───────────────────────────────
        xs_i = np.linspace(IX0, IX1, 200)
        wt_i = 4 * PI * (xs_i - IX0) / (IX1 - IX0)
        i1 = poly(xs_i, IY + A_I * np.sin(wt_i), CYAN, 3, 0.8)
        i2 = poly(xs_i, IY + A_I * np.sin(wt_i + PI), MAGENTA, 3, 0.8)
        isum = poly(xs_i, IY + A_I * p_sum(wt_i, PI), WHITE, 5)
        iax = VGroup(*(Line([IX0, IY, 0], [IX1 + 0.1, IY, 0]).set_stroke(BLUE, 2, 0.5) for _ in range(3)))
        ilab = left_at(VGroup(tex("p(t)", 26), text("EM", 18), tex("x_0", 26)).arrange(RIGHT, buff=0.1),
                       IX0, IY + 0.78)
        self.until(44.64)                                 # "Mas esse gráfico não é o formato do ar."
        self.play(ReplacementTransform(c1, i1), ReplacementTransform(c2, i2), ReplacementTransform(csum, isum),
                  ReplacementTransform(VGroup(ax1[0], ax2[0], axs[0]), iax),
                  FadeOut(VGroup(ax1[1], ax2[1], axs[1], lab1, lab2b, labs, nota, crest, probe, amp, ares_lab, self.eq, tag)),
                  *self.caption("O gráfico não é", "o formato do ar"), run_time=1.2)
        self.eq = None
        self.play(FadeIn(ilab), run_time=0.4)

        cy.set_value(Y_AIR[0])
        cx.set_value(99.0)
        row1 = self.air_row(CYAN, (0,), cy, cx)
        row2 = self.air_row(MAGENTA, (PI,), Y_AIR[1])
        row3 = self.air_row(WHITE, (0, PI), Y_AIR[2])     # s_total = s₁ + s₂, calculado
        rlabels = VGroup(*(left_at(text(name, 22, color=col), -3.3, y + 0.62) for name, col, y in
                           (("ONDA 1", CYAN, Y_AIR[0]), ("ONDA 2", MAGENTA, Y_AIR[1]),
                            ("RESULTANTE", WHITE, Y_AIR[2]))))
        air_note = left_at(text("DESLOCAMENTO DO AR · MESMO TRECHO", 20, opacity=0.75), -3.3, 3.25)
        j_mark = 4                                        # uma camada destacada nas três fileiras

        def layer_marks():
            t, x_eq = self.air.get_value(), AIR_X[j_mark]
            marks = VGroup()
            for col, phases, y in ((CYAN, (0,), Y_AIR[0]), (MAGENTA, (PI,), Y_AIR[1]), (WHITE, (0, PI), Y_AIR[2])):
                dx = sum(S0 * np.sin(K * x_eq - W_AIR * t + ph) for ph in phases)
                marks.add(Line([x_eq, y - 0.62, 0], [x_eq, y - 0.42, 0]).set_stroke(BLUE, 2, 0.8),
                          Dot([x_eq + dx, y - 0.52, 0], 0.07, color=col))
            return marks

        marks = always_redraw(layer_marks)
        # x₀ só no painel espacial; a chamada lateral liga o ponto ao gráfico p(t).
        x0line = DashedLine([X0_PROBE, Y_AIR[0] + 0.5, 0], [X0_PROBE, Y_AIR[2] - 0.45, 0]).set_stroke(WHITE, 2, 0.3)
        x0lab = tex("x_0", 26).set_opacity(0.8).move_to([X0_PROBE, Y_AIR[2] - 0.7, 0])

        def make_callout():
            arrow = CurvedArrow([X0_PROBE + 0.08, Y_AIR[0] + 0.55, 0], [IX1 + 0.35, IY - 0.15, 0], angle=PI / 3,
                                color=WHITE, stroke_width=2, tip_length=0.14)
            arrow.set_stroke(WHITE, 2, 0.55).set_fill(opacity=0)   # só o traço: o arco não é preenchido
            arrow.tip.set_fill(WHITE, 0.55)
            return arrow

        callout = make_callout()
        self.until(46.78)                                 # "No ar, as camadas oscilam para a frente e para trás…"
        self.play(FadeIn(row1, row2, row3, rlabels, air_note, marks, x0line, x0lab, callout), run_time=0.8)
        self.until(49.85)                                 # "…formando compressões e rarefações."
        self.play(*self.caption("No ar: compressões", "e rarefações"), run_time=0.6)
        self.play(self.air_rate.animate.set_value(0), run_time=0.3)          # congela um instante
        t0 = self.air.get_value()
        xc = ((PI + W_AIR * t0) / K + 1.2) % LAMBDA - 1.2  # kx − ω_a t₀ = π: máxima compressão, longe de “ONDA 1”
        xr = xc + LAMBDA / 2 if xc + LAMBDA / 2 < 2.6 else xc - LAMBDA / 2   # rarefação: meio λ ao lado
        lab_c = text("compressão", 20).move_to([xc, Y_AIR[0] + 0.68, 0])
        lab_r = text("rarefação", 20).move_to([xr, Y_AIR[0] - 0.68, 0])  # abaixo: não encosta
        self.play(FadeIn(lab_c, lab_r), FadeOut(callout), run_time=0.4)   # seta sai: não cruza os rótulos
        self.until(51.8)
        callout = make_callout()
        self.play(FadeOut(lab_c, lab_r), FadeIn(callout), self.air_rate.animate.set_value(1), run_time=0.4)
        msg = text("AS ONDAS NÃO SE ANIQUILAM", 24).move_to([0, -3.3, 0])
        self.play(FadeIn(msg), run_time=0.4)              # "As ondas não se aniquilam:" (52,20)
        self.until(53.75)                                 # "…o que diminui é a pressão resultante."
        msg_2 = text("A PRESSÃO RESULTANTE DIMINUI", 24).move_to([0, -3.3, 0])
        halo = RoundedRectangle(width=6.9, height=1.0, corner_radius=0.2).move_to([0, Y_AIR[2], 0])
        halo.set_stroke(width=0).set_fill(WHITE, 0.07)
        self.play(FadeOut(msg), FadeIn(msg_2, halo), run_time=0.5)
        self.check_safe_area()

        # ── C8–C9. Transição e arquitetura conceitual (56,1–64,5) ────────────
        f2 = build_fone()
        scheme = text("ESQUEMA CONCEITUAL", 18, opacity=0.6).move_to([-2.0, 0.25, 0])
        self.until(56.1)                                  # "Agora, de volta ao fone."
        self.play(FadeOut(VGroup(i1, i2, isum, iax, ilab, row2, row3, rlabels, air_note, marks,
                                 x0line, x0lab, callout, msg_2, halo)),
                  cy.animate.set_value(EAR_Y), cx.animate.set_value(-0.4),
                  *self.caption("Cancelamento ativo", "de ruído"), run_time=0.6)
        self.play(Create(f2.shell), FadeIn(f2.rest, scheme), run_time=0.9)
        # Rótulos ligados às peças por linhas curtas.
        lab_mic = VGroup(text("microfones", 24).move_to([1.15, 5.0, 0]),
                         leader((0.85, 4.84), (0.16, 3.97)), leader((1.45, 4.84), (2.17, 3.2)))
        lab_chip = VGroup(text("processamento", 24).move_to([-1.35, CHIP[1], 0]),
                          leader((-0.25, CHIP[1]), (0.33, CHIP[1])))
        lab_drv = VGroup(text("alto-falante", 24).move_to([1.4, -0.12, 0]), leader((1.4, 0.05), (1.4, 1.66)))
        self.until(57.7)                                  # "Os microfones captam o ruído,"
        self.play(*(Indicate(m, color=CYAN, scale_factor=1.8) for m in f2.mics), FadeIn(lab_mic), run_time=0.5)
        pulses = [Dot(p.get_start(), 0.08, color=CYAN) for p in f2.paths[:2]]
        self.play(*(MoveAlongPath(d, p) for d, p in zip(pulses, f2.paths[:2])), run_time=1.0, rate_func=linear)
        self.remove(*pulses)
        self.until(59.6)                                  # "…o processamento calcula uma resposta,"
        self.play(f2.chip.animate.set_fill(VIOLET, 0.6), FadeIn(lab_chip), run_time=0.4)
        self.play(f2.chip.animate.set_fill(VIOLET, 0.25), run_time=0.4)
        pulse_m = Dot(f2.paths[2].get_start(), 0.08, color=MAGENTA)
        self.until(60.6)
        self.play(MoveAlongPath(pulse_m, f2.paths[2]), run_time=0.8, rate_func=linear)
        self.remove(pulse_m)
        arcs_2 = self.arcs(emit)
        self.add(arcs_2)
        self.until(61.64)                                 # "…e o alto-falante produz outra contribuição sonora."
        self.play(emit.animate.set_value(1), FadeIn(lab_drv), Indicate(f2.driver, color=MAGENTA, scale_factor=1.15),
                  run_time=0.6)
        self.check_safe_area()

        # ── C10. Cancelamento imperfeito no ouvido (64,5–71,4) ───────────────
        labels = VGroup(lab_mic, lab_chip, lab_drv)
        region_2 = region_mark()
        self.until(64.49)                                 # "Perto do ouvido, acontece a mesma soma."
        self.play(Create(region_2), run_time=0.4)
        anc.g.set_value(0)
        anc.wtau.set_value(0.05 * PI)                     # φ = 0,95π
        panel_2, guide_2, bars_2 = self.build_panel(), guide_line(), self.amp_bars()
        self.play(Create(guide_2), FadeIn(panel_2), run_time=0.8)
        self.until(65.9)                                  # construção da soma: B 0 → 0,9A
        self.swap_eq(fit(ctex((r"p_{\text{ru\'{\i}do}}", CYAN), ("+", WHITE), (r"p_{\text{fone}}", MAGENTA),
                              ("=", WHITE), (r"p_{\text{residual}}", WHITE), size=42)).move_to([-0.3, Y_PANEL_EQ, 0]),
                     FadeIn(bars_2))
        self.play(anc.g.animate.set_value(0.9), run_time=0.6)
        self.until(69.65)                                 # "…sobra um resíduo, em branco."
        self.play(anc.w_res.animate(rate_func=there_and_back).set_value(10), run_time=0.8)
        self.check_safe_area()

        # ── C11. Melhor ajuste (71,4–76,2) ───────────────────────────────────
        self.until(71.5)                                  # "Com um ajuste melhor, o resíduo fica menor." → 0,95A, 0,97π
        self.play(anc.g.animate.set_value(0.95), anc.wtau.animate.set_value(0.03 * PI), run_time=2.0)
        self.until(73.6)                                  # compara amplitudes, não valores instantâneos
        self.swap_eq(fit(ctex((r"A_{\text{residual}}", WHITE), (r"\ll", WHITE), (r"A_{\text{ru\'{\i}do}}", CYAN),
                              size=42)).move_to([-0.3, Y_PANEL_EQ, 0]))
        self.until(74.8)                                  # "Mas, num fone real, não chega a zero."
        self.play(anc.w_res.animate(rate_func=there_and_back).set_value(10), run_time=0.8)

        # ── C12. Por que não é perfeito? (76,2–82,1) ─────────────────────────
        self.until(76.22)                                 # "O ruído real mistura várias frequências,"
        self.play(*self.caption("Por que não é perfeito?"), FadeOut(labels), run_time=0.4)  # componentes já cumpriram a função
        self.play(anc.c.animate.set_value(0.35), run_time=1.8)   # mesmo τ: erro de fase 3× maior em 3ω
        self.until(79.5)                                  # "…e o sistema ainda lida com atraso, posição e acústica."
        self.swap_eq(VGroup(text("FREQUÊNCIAS · ATRASO", 26, opacity=0.9), text("POSIÇÃO · ACÚSTICA", 26, opacity=0.9))
                     .arrange(DOWN, buff=0.1).move_to([-1.3, Y_PANEL_EQ, 0]))   # à esquerda de “alto-falante”
        self.check_safe_area()

        # ── C13. Onde costuma funcionar melhor (82,1–93,5) ───────────────────
        self.until(82.1)                                  # "Por isso, o cancelamento ativo costuma funcionar melhor…"
        self.play(FadeOut(VGroup(f2.body, row1, arcs_2, region_2, guide_2, panel_2, bars_2, scheme, self.eq)),
                  *self.caption("Onde costuma", "funcionar melhor"), run_time=0.7)
        self.eq = None
        icons = build_icons()
        self.play(LaggedStart(*(FadeIn(i) for i in icons), lag_ratio=0.3), run_time=1.2)
        strip_lo, strip_hi = wave_strip(1.3, 1), wave_strip(-1.3, 5)
        lab_lo = left_at(text("FREQUÊNCIA MAIS BAIXA", 24, opacity=0.9), -3.0, 2.3)
        lab_hi = left_at(text("FREQUÊNCIA MAIS ALTA", 24, opacity=0.9), -3.0, -0.3)
        self.until(86.6)                                  # "…ruídos contínuos e frequências mais baixas…"
        self.play(FadeIn(strip_lo[0], lab_lo), Create(strip_lo[1]), run_time=1.0)
        self.until(88.2)                                  # "…como motor e avião."
        self.play(FadeIn(strip_hi[0], lab_hi), Create(strip_hi[1]), run_time=0.9)
        # Um período de cada curva; o curto começa na borda do atraso para mostrar a fração do ciclo.
        periods = VGroup(period_mark(-3.0, 3.0, 0.4), text("1 PERÍODO", 18, opacity=0.8).move_to([2.0, 0.2, 0]),
                         period_mark(-0.7, 0.5, -2.2), text("1 PERÍODO", 18, opacity=0.8).move_to([-0.1, -2.42, 0]))
        self.until(89.26)                                 # "O período é maior,"
        self.play(FadeIn(periods), run_time=0.5)
        slabs = VGroup(*(Rectangle(width=0.4, height=1.5).move_to([-0.5, y, 0]) for y in (1.3, -1.3)))
        slabs.set_stroke(width=0).set_fill(VIOLET, 0.3)
        delay_lines = VGroup(*(VGroup(*(Line([x, y - 0.75, 0], [x, y + 0.75, 0]) for x in (-0.7, -0.3)))
                               for y in (1.3, -1.3))).set_stroke(VIOLET, 3)
        lab_delay = text("MESMO ATRASO", 26, opacity=0.9).move_to([-0.5, -3.0, 0])
        self.until(90.6)                                  # "…então o mesmo atraso…"
        self.play(FadeIn(slabs, delay_lines, lab_delay), run_time=0.5)
        self.until(91.9)                                  # "…gera uma diferença de fase menor."
        self.play(Indicate(VGroup(slabs[0], delay_lines[0]), color=VIOLET, scale_factor=1.15), run_time=1.0)
        self.check_safe_area()

        # ── C14. Fechamento (93,5–fim) ───────────────────────────────────────
        f3 = build_fone()
        anc.c.set_value(0)
        anc.g.set_value(0.95)
        anc.wtau.set_value(0.03 * PI)
        noise_3, arcs_3 = self.air_row(CYAN, (0,), cy, cx), self.arcs(emit)
        region_3, guide_3, panel_3, bars_3 = region_mark(), guide_line(), self.build_panel(), self.amp_bars()
        self.until(93.47)                                 # "O som não desaparece."
        self.play(FadeOut(VGroup(icons, strip_lo, strip_hi, lab_lo, lab_hi, periods, slabs, delay_lines, lab_delay)),
                  FadeIn(VGroup(f3.body, noise_3, arcs_3, region_3, guide_3, panel_3, bars_3)),
                  *self.caption("O som não desaparece"), run_time=0.9)
        self.until(95.4)                                  # "O fone adiciona outra contribuição…"
        self.play(anc.w_mag.animate(rate_func=there_and_back).set_value(8), run_time=1.0)
        self.until(97.6)                                  # "…e reduz a pressão resultante perto do ouvido."
        self.play(anc.w_res.animate(rate_func=there_and_back).set_value(10),
                  Indicate(region_3, color=WHITE, scale_factor=1.15), run_time=1.0)
        chain = VGroup(text("SUPERPOSIÇÃO", 22), tex(r"\rightarrow", 28), text("INTERFERÊNCIA", 22),
                       tex(r"\rightarrow", 28), text("REDUÇÃO DO RUÍDO", 22)).arrange(RIGHT, buff=0.14)
        if chain.width > 2 * SAFE_X - 0.2:
            chain.scale_to_fit_width(2 * SAFE_X - 0.2)
        chain.move_to([0, Y_PANEL_EQ, 0])
        self.until(98.7)                                  # síntese no fim de “…perto do ouvido.”
        self.play(FadeIn(chain, shift=UP * 0.1), FadeOut(guide_3), run_time=0.6)
        self.check_safe_area()
        self.until(101.12)                                # "Se curtiu, siga o Parallax Lab."
        handle = text("@labparallax", 30).move_to(chain)
        self.play(FadeOut(chain), FadeIn(handle, shift=UP * 0.1), run_time=0.6)
        self.check_safe_area()
        self.until(105.5)                                 # fala termina em 104,37 s; WAV tem 104,64 s
