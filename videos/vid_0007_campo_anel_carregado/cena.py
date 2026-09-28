"""Campo elétrico no eixo de um anel carregado e posição do máximo; preview silencioso.

EXERCÍCIO RESOLVIDO · EP. 03. Anel fino de raio R, carga Q > 0 uniforme, no plano xy,
centro na origem; P = (0, 0, z), z ≥ 0 (eixo vertical na tela). Coulomb + simetria +
integração (sem Lei de Gauss): dE_z = dE cos θ = k dq/s² · z/s = kz dq/s³, com
s³ = (R² + z²)^{3/2}; E(z) = kQz/(R² + z²)^{3/2}; dE/dz = kQ(R² − 2z²)/(R² + z²)^{5/2};
máximo em z = R/√2. Interno: u = z/R, e(u) = u/(1 + u²)^{3/2}; posição de P, seta do
campo e marcador do gráfico saem todos de e(self.u) (um único ValueTracker).

Vista: pseudo-3D por projeção oblíqua — eixo z e diâmetro horizontal em verdadeira
grandeza, profundidade achatada por TILT. O corte lateral (TILT = 0) é o plano que
contém o eixo e o dq em φ = 0, com R, z, s e θ em verdadeira grandeza.

Cores: ciano = dq / 1ª contribuição / curva E(z); magenta = dq oposto e sua decomposição;
violeta = s, correspondência angular, s²·s → s³, raiz → 3/2, destaques do máximo;
branco = resultante, equações e resultados; azul = anel, eixo e geometria.
"""

from pathlib import Path
from types import SimpleNamespace

import numpy as np
from manim import (
    DOWN, LEFT, PI, RIGHT, UP, Arc, Arrow, Circle, Create, DashedLine, Dot, FadeIn, FadeOut, GrowArrow,
    ImageMobject, Indicate, LaggedStart, Line, MathTex, ReplacementTransform, Scene, SurroundingRectangle,
    TransformMatchingShapes, TransformMatchingTex, VGroup, VMobject, ValueTracker, always_redraw, linear,
)

from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # dq, 1ª contribuição, curva E(z)
MAGENTA = "#EA63FF"       # dq diametralmente oposto
BLUE = "#267BFF"          # anel, eixo, geometria
VIOLET = SECONDARY_COLOR  # s, ângulos, transformações do denominador, máximo

SAFE_BOTTOM = -4.6        # abaixo disso: faixa reservada a legendas
SAFE_X = 3.5              # |x| máximo do conteúdo
HEADLINE_TOP = 6.85

# Vista física: centro do anel (ox, oy); rs unidades de tela por R; P em O + (0, rs·u)
O_Y = -0.5
RS = 2.1                  # anel com ~47% da largura do quadro
TILT = 0.3
AXIS_TOP = 5.15
U_HOOK = 2.2              # subida do gancho (C1)
U_MODEL = 1.2             # P congelado (C2–C7)
U_FAR = 15.0              # z ≫ R (C7): mesma altura de P na tela, anel visto de longe
RS_G, O_Y_G = 1.75, -0.2  # vista acima do gráfico (C8–C11)
U_SWEEP = 2.4
OX_RESULT = -1.0          # C10–C11: anel à esquerda, resultado à direita
LMAX = 1.8                # comprimento da seta de E no máximo
LD = 1.8                  # comprimento dos dE do par (C4–C5)
X_NOTE = 2.15
Y_EQ, Y_TAG = -2.7, -3.85
Y_EQ5, Y_REM5, Y_NOTE5 = -3.0, -1.72, -4.2   # C5: equação principal / relação auxiliar / nota
EQ5 = 58                                     # corpo da equação principal em C5
Y_EQ6, Y_QINT = -2.45, -3.95                 # C6: equação principal / ∫dq = Q sob o ∫dq
Y_C9, Y_C9_NOTE = 2.3, 1.0

# Gráfico E(z) (C8–C11): u ∈ [0, U_GRAPH] em x ∈ [GX0, GX1]; pico com altura GH
GX0, GX1, GY0, GH, U_GRAPH = -3.0, 3.0, -3.85, 1.95, 3.0

AUDIO_PATH = Path(__file__).parent / "audio" / "narracao_final.wav"  # ElevenLabs, intacta

# Termos coloridos na legenda (montar_legendado.py --color-module), com o mesmo significado da cena.
SUBTITLE_TERM_COLORS = {
    "elemento de carga": CYAN,
    "outro do lado oposto": MAGENTA,
    "hipotenusa": VIOLET,
    "três meios": VIOLET,
    "R sobre raiz de dois": VIOLET,
    "0,71 R": VIOLET,
}


# ── Modelo físico: tudo que se move na tela usa exatamente estas funções ────
def e(u):
    """E(z) / (kQ/R²) com u = z/R."""
    u = np.asarray(u, dtype=float)
    return u / (1 + u * u) ** 1.5


def de(u):
    """dE/dz / (kQ/R³): sinal de R² − 2z²."""
    u = np.asarray(u, dtype=float)
    return (1 - 2 * u * u) / (1 + u * u) ** 2.5


U_STAR = 1 / np.sqrt(2)
E_MAX = 2 / (3 * np.sqrt(3))

_U = np.linspace(0, U_GRAPH, 30001)
assert e(0) == 0                                                    # centro: E = 0
assert abs(_U[np.argmax(e(_U))] - U_STAR) < 1e-3                    # máximo em u = 1/√2
assert abs(e(U_STAR) - E_MAX) < 1e-12 and abs(E_MAX - 0.3849) < 1e-4
assert abs(de(U_STAR)) < 1e-12
assert np.all(de(_U[_U < U_STAR - 1e-6]) > 0) and np.all(de(_U[_U > U_STAR + 1e-6]) < 0)  # + → 0 → −
assert np.allclose(np.gradient(e(_U), _U)[1:-1], de(_U)[1:-1], atol=1e-6)                # de = e'
assert abs(e(100.0) * 100.0 ** 2 - 1) < 1e-3                        # z ≫ R: E ≈ kQ/z²
assert np.allclose(e(-_U), -e(_U))                                  # E_z(−z) = −E_z(z)
_S = np.hypot(1.0, _U)                                              # dE_z = k dq/s² · z/s = kz dq/(R²+z²)^{3/2}
assert np.allclose((1 / _S ** 2) * (_U / _S), _U / (1 + _U ** 2) ** 1.5)


def gpt(u):
    """Ponto da curva E(z) no gráfico."""
    return np.array([GX0 + (GX1 - GX0) * u / U_GRAPH, GY0 + GH * float(e(u)) / E_MAX, 0.0])


assert max(range(len(_U)), key=lambda i: gpt(_U[i])[1]) == int(np.argmax(e(_U)))  # pico do gráfico = pico físico


def pair_vectors(u):
    """dE dos dq em φ = 0 (ciano) e φ = π (magenta) em P; ambos no plano da tela."""
    s = np.hypot(1.0, u)
    d1 = LD * np.array([-1 / s, u / s, 0.0])   # afasta-se do dq em (+R, 0)
    d2 = LD * np.array([1 / s, u / s, 0.0])    # afasta-se do dq em (−R, 0)
    assert np.isclose(d1[0], -d2[0]) and np.isclose(d1[1], d2[1]) and d1[1] > 0  # laterais opostas, axiais iguais
    return d1, d2


def slow_peak(u_end):
    """rate_func da varredura de u: mesma função física, só desacelera perto do pico."""
    us = np.linspace(0, u_end, 2001)
    speed = 1 - 0.55 * np.exp(-((us - U_STAR) / 0.3) ** 2)
    t = np.concatenate([[0], np.cumsum(np.diff(us) / ((speed[1:] + speed[:-1]) / 2))])
    t /= t[-1]
    return lambda a: float(np.interp(a, t, us / u_end))


# ── Helpers visuais ─────────────────────────────────────────────────────────
def tex(content, size=40, color=WHITE):
    return MathTex(content, font_size=size, color=color)


def mtex(*parts, size=50):
    return MathTex(*parts, font_size=size, color=WHITE)


def text(content, size=24, color=WHITE, opacity=1.0, **kwargs):
    return screen_text(content, size, color=color, **kwargs).set_opacity(opacity)


def display(content, size=38):
    return screen_text(content, size, oversample=2, color=WHITE)


def tag(content, size=28, opacity=1.0):
    """Mensagem de uma linha (oversample 2: sem quebra do Pango), limitada à margem."""
    t = screen_text(content, size, oversample=2, color=WHITE).set_opacity(opacity)
    return t.scale_to_fit_width(min(t.width, 2 * SAFE_X - 0.4))


def vec(a, b, color, width=6):
    return Arrow(a, b, buff=0, stroke_width=width, tip_length=0.24, max_tip_length_to_length_ratio=0.35,
                 max_stroke_width_to_length_ratio=30, color=color)


def boxed(mob, color=WHITE):
    return VGroup(mob, SurroundingRectangle(mob, color=color, buff=0.16, corner_radius=0.08, stroke_width=2.5))


def frac_parts(frac):
    """Separa os glifos de uma fração do MathTex: (numerador, barra, denominador)."""
    bar = max(frac, key=lambda m: m.width - 10 * m.height)
    y = bar.get_center()[1]
    num = VGroup(*(m for m in frac if m is not bar and m.get_center()[1] > y))
    den = VGroup(*(m for m in frac if m is not bar and m.get_center()[1] < y))
    return num, bar, den


def dim_mark(a, b, color, ticks=0.09):
    """Cota: segmento fino com traços nas pontas (não é vetor)."""
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0], 0.0]) * ticks
    return VGroup(Line(a, b), Line(a - n, a + n), Line(b - n, b + n)).set_stroke(color, 2.5, 0.9)


class CampoAnel007(Scene):
    def check_safe_area(self):
        vms = [m for m in self.mobjects if isinstance(m, VMobject) and len(m.get_all_points())]
        bottom = min(m.get_bottom()[1] for m in vms)
        assert bottom > SAFE_BOTTOM, f"conteúdo invade a faixa inferior: {bottom:.2f}"
        for m in vms:
            if m is not self.series:
                assert m.get_left()[0] > -SAFE_X and m.get_right()[0] < SAFE_X, \
                    f"conteúdo fora da margem lateral: {m.get_left()[0]:.2f}..{m.get_right()[0]:.2f}"

    def caption(self, *lines):
        """Troca a manchete do topo (linhas de texto ou um Mobject pronto); devolve as animações."""
        if len(lines) == 1 and isinstance(lines[0], VMobject):
            new = lines[0]
        else:
            new = VGroup(*(display(line) for line in lines)).arrange(DOWN, buff=0.14)
        if new.width > 2 * SAFE_X - 0.2:
            new.scale_to_fit_width(2 * SAFE_X - 0.2)
        new.move_to([0, HEADLINE_TOP - new.height / 2, 0])
        anims = [FadeIn(new, shift=DOWN * 0.15)]
        if self.headline is not None:
            anims.append(FadeOut(self.headline, shift=UP * 0.15))
        self.headline = new
        return anims

    def swap_eq(self, new, *extra, run_time=0.6):
        anims = [FadeIn(new, shift=UP * 0.1)] if new is not None else []
        if self.eq is not None:
            anims.append(FadeOut(self.eq, shift=UP * 0.1))
        self.play(*anims, *extra, run_time=run_time)
        self.eq = new

    def until(self, seconds):
        """Espera até o instante `seconds` da narração (segundos do WAV; tolera ~1 frame a 15 fps)."""
        remaining = seconds - self.time
        assert remaining > -0.1, f"linha do tempo atrasada: {self.time:.2f} s > {seconds} s"
        if remaining > 1e-6:
            self.wait(remaining)

    # ── Vista física (tudo derivado de u, rs, tilt, ox, oy) ─────────────────
    def o(self):
        return np.array([self.ox.get_value(), self.oy.get_value(), 0.0])

    def ring_pt(self, phi):
        rs, t = self.rs.get_value(), self.tilt.get_value()
        return self.o() + rs * np.array([np.cos(phi), t * np.sin(phi), 0.0])

    def p_pt(self):
        return self.o() + np.array([0.0, self.rs.get_value() * self.u.get_value(), 0.0])

    def e_len(self):
        return LMAX * float(e(self.u.get_value())) / E_MAX

    @staticmethod
    def depth(phi):
        """Metade de trás do anel (sin φ > 0, acima na tela) mais apagada."""
        return 0.45 if np.sin(phi) > 1e-9 else 1.0

    def ring_half(self, back):
        phis = np.linspace(0, PI, 61) + (0 if back else PI)
        op = self.ring_op.get_value() * self.view_op.get_value() * (0.45 if back else 1.0)
        return VMobject().set_points_as_corners([self.ring_pt(p) for p in phis]).set_stroke(BLUE, 7, op)

    def charges(self):
        op = self.plus_op.get_value() * self.view_op.get_value()
        g = VGroup()
        if op < 0.01:
            return g
        for phi in np.arange(12) * PI / 6 + PI / 12:
            c, a = self.ring_pt(phi), op * (0.55 if np.sin(phi) > 0 else 1.0)
            g.add(Line(c + LEFT * 0.08, c + RIGHT * 0.08).set_stroke(WHITE, 3, a),
                  Line(c + DOWN * 0.08, c + UP * 0.08).set_stroke(WHITE, 3, a))
        return g

    def e_arrow(self):
        L, op = self.e_len(), self.arrow_op.get_value() * self.view_op.get_value()
        if L < 0.02 or op < 0.01:
            return VMobject()                     # z = 0: campo nulo, nenhuma seta
        p = self.p_pt()
        return vec(p, p + UP * L, WHITE, 8).set_opacity(op)

    def place_e_label(self, m):
        L = self.e_len()
        m.next_to(self.p_pt() + UP * L * 0.6, RIGHT, 0.18)
        m.set_opacity(self.arrow_op.get_value() * self.view_op.get_value() * min(1.0, L / 0.5))

    def dq_mark(self, phi, color):
        """Elemento dq: trecho do anel + ponto; acompanha o achatamento do corte."""
        def build():
            pts = [self.ring_pt(p) for p in np.linspace(phi - 0.14, phi + 0.14, 9)]
            return VGroup(VMobject().set_points_as_corners(pts).set_stroke(color, 13),
                          Dot(self.ring_pt(phi), 0.12, color=color))
        return always_redraw(build)

    def cut_frame(self):
        """Corte lateral: diâmetro auxiliar tracejado (não é haste), seção do fio em −R, O e rótulo."""
        o, rs = self.o(), self.rs.get_value()
        return VGroup(DashedLine(o + LEFT * rs, o + RIGHT * rs, dash_length=0.12).set_stroke(BLUE, 2, 0.6),
                      Circle(0.1, color=BLUE, stroke_width=3).set_fill(BLUE, 0.5).move_to(o + LEFT * rs),
                      tex("O", 32).set_opacity(0.85).move_to(o + np.array([-0.3, -0.34, 0])),
                      text("CORTE LATERAL", 22, opacity=0.7).move_to([X_NOTE, 4.5, 0]))

    def triangle(self, op=1.0):
        """O, dq em (+R, 0), P em (0, z): R, z, s em verdadeira grandeza (s em violeta)."""
        o, dq, p = self.o(), self.ring_pt(0), self.p_pt()
        seg_r, seg_z = Line(o, dq).set_stroke(WHITE, 4, op), Line(o, p).set_stroke(WHITE, 4, op)
        seg_s = Line(dq, p).set_stroke(VIOLET, 5, op)
        mid, d = (dq + p) / 2, p - dq
        normal = np.array([d[1], -d[0], 0.0]) / np.linalg.norm(d)
        if np.dot(normal, mid - o) < 0:
            normal = -normal
        corner = VMobject().set_points_as_corners([o + RIGHT * 0.22, o + RIGHT * 0.22 + UP * 0.22, o + UP * 0.22]
                                                  ).set_stroke(WHITE, 2, 0.6 * op)
        return SimpleNamespace(seg_r=seg_r, seg_z=seg_z, seg_s=seg_s, corner=corner,
                               lab_r=tex("R", 38).next_to(seg_r, DOWN, 0.18),
                               lab_z=tex("z", 38).next_to(seg_z, LEFT, 0.22),
                               lab_s=tex("s", 38, VIOLET).move_to(mid + 0.34 * normal))

    def pair(self):
        phi = self.pair_phi.get_value()
        a, b = self.ring_pt(phi), self.ring_pt(phi + PI)
        return VGroup(DashedLine(a, b, dash_length=0.1).set_stroke(WHITE, 2, 0.45),
                      Dot(a, 0.12, color=CYAN).set_opacity(self.depth(phi)),
                      Dot(b, 0.12, color=MAGENTA).set_opacity(self.depth(phi + PI)))

    def sweep_arc(self):
        end = self.sweep.get_value()
        g = VGroup()
        if end < 1e-3:
            return g
        for a, b, op in ((0, min(end, PI), 0.55), (PI, end, 1.0)):   # trás, frente
            if b > a + 1e-3:
                pts = [self.ring_pt(p) for p in np.linspace(a, b, max(2, int(40 * (b - a))))]
                g.add(VMobject().set_points_as_corners(pts).set_stroke(CYAN, 11, op))
        return g.add(Dot(self.ring_pt(end), 0.12, color=CYAN))

    # ── Gráfico E(z) ─────────────────────────────────────────────────────────
    def trace_curve(self):
        umax = self.trace.get_value()
        if umax < 1e-3:
            return VMobject()
        us = np.linspace(0, umax, max(2, int(80 * umax)))
        return VMobject().set_points_as_corners([gpt(v) for v in us]).set_stroke(CYAN, 5)

    def drop_line(self):
        top = gpt(self.u.get_value())
        if top[1] - GY0 < 0.08:
            return VMobject()
        return DashedLine([top[0], GY0, 0], top, dash_length=0.07).set_stroke(WHITE, 2, 0.45)

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.headline = None
        self.eq = None
        watermark = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(watermark.to_corner(UP + RIGHT, buff=0.28))
        self.series = text("EXERCÍCIO RESOLVIDO · EP. 03", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4)

        self.u, self.rs, self.tilt = ValueTracker(0), ValueTracker(RS), ValueTracker(TILT)
        self.ox, self.oy = ValueTracker(0), ValueTracker(O_Y)
        self.view_op, self.ring_op, self.plus_op, self.arrow_op, self.p_op = (
            ValueTracker(v) for v in (0, 1, 1, 1, 1))
        self.pair_phi, self.sweep, self.trace = ValueTracker(0), ValueTracker(0), ValueTracker(0)
        self.add(self.u, self.rs, self.trace)

        view_op = self.view_op.get_value
        ring_back = always_redraw(lambda: self.ring_half(True))
        axis = always_redraw(lambda: Line(self.o() + DOWN * 0.35, [self.ox.get_value(), AXIS_TOP, 0])
                             .set_stroke(BLUE, 3, 0.75 * view_op()))
        ring_front = always_redraw(lambda: self.ring_half(False))
        charges = always_redraw(self.charges)
        p_dot = always_redraw(lambda: Dot(self.p_pt(), 0.1, color=WHITE).set_opacity(view_op()))
        e_vec = always_redraw(self.e_arrow)
        z_lab = tex("z", 34).add_updater(
            lambda m: m.move_to([self.ox.get_value() + 0.3, AXIS_TOP - 0.05, 0]).set_opacity(0.7 * view_op()))
        p_lab = tex("P", 38).add_updater(
            lambda m: m.next_to(self.p_pt(), LEFT, 0.2).set_opacity(view_op() * self.p_op.get_value()))
        e_lab = tex(r"\vec E", 38).add_updater(self.place_e_label)
        for m in (z_lab, p_lab, e_lab):
            m.update()
        self.add(ring_back, axis, ring_front, charges, p_dot, e_vec, z_lab, p_lab, e_lab)

        # Tempos = segundos de audio/narracao_final.wav (pausas medidas); comentários citam a fala.
        self.add_sound(str(AUDIO_PATH))

        # ── C1. Gancho (0–11,9): o campo nasce zero, cresce, passa por um pico e cai ──
        e0 = tex("E=0", 40).move_to(self.o() + RIGHT * 0.85)
        self.play(FadeIn(self.series), *self.caption("ONDE O CAMPO ELÉTRICO", "É MAIS FORTE?"),
                  self.view_op.animate.set_value(1), FadeIn(e0), run_time=0.8)
        self.check_safe_area()
        self.until(5.9)                                   # "…lá ele é zero."
        self.play(Indicate(e0, color=WHITE), run_time=0.8)
        self.until(7.1)                                   # "Ele cresce, chega a um pico e depois cai."
        self.play(FadeOut(e0), run_time=0.3)
        self.play(self.u.animate.set_value(U_HOOK), run_time=2.9, rate_func=linear)   # seta = e(u), não keyframes
        self.check_safe_area()

        # ── C2. Modelo físico (11,9–20,1): eixo, cota z e seta separados ───────
        self.until(11.94)                                  # "Temos um anel fino…"
        self.play(*self.caption("ANEL FINO · CARGA UNIFORME"), self.u.animate.set_value(U_MODEL), run_time=1.5)
        o, p = self.o(), self.p_pt()
        r_line = DashedLine(o, self.ring_pt(0), dash_length=0.12).set_stroke(WHITE, 3, 0.85)
        r_lab = tex("R", 38).move_to(o + np.array([RS / 2, 0.26, 0]))
        self.until(13.5)                                  # "…de raio R,"
        self.play(Create(r_line), FadeIn(r_lab), run_time=0.8)
        q_lab = tex("Q>0", 40).move_to(self.ring_pt(1.25 * PI) + np.array([-0.55, -0.42, 0]))
        self.until(15.2)                                  # "…com carga total positiva Q…"
        self.play(FadeIn(q_lab, shift=UP * 0.1), run_time=0.6)
        z_mark = dim_mark(o + LEFT * 0.8, p + LEFT * 0.8, WHITE)
        z_mlab = tex("z", 38).next_to(z_mark, LEFT, 0.18)
        self.until(17.1)                                  # "O ponto P está a uma distância z do centro."
        self.play(Indicate(p_lab, color=WHITE), run_time=0.8)
        self.play(Create(z_mark), FadeIn(z_mlab), run_time=0.8)
        self.check_safe_area()

        # ── C3. Um elemento dq e o corte lateral (20,1–36,8) ────────────────────
        self.until(20.1)                                  # "Pega um pedacinho do anel…"
        dq1 = self.dq_mark(0, CYAN)
        dq1_lab = tex("dq", 38, CYAN).move_to(self.ring_pt(0) + np.array([0.5, -0.36, 0]))
        self.play(*self.caption("Um elemento de carga"), FadeOut(VGroup(r_line, r_lab, q_lab, z_mark, z_mlab)),
                  self.arrow_op.animate.set_value(0), run_time=0.8)
        self.until(20.9)
        self.play(FadeIn(dq1), FadeIn(dq1_lab), run_time=0.7)
        self.until(21.65)                                  # "…um elemento de carga."
        cut = self.cut_frame()
        self.play(self.tilt.animate.set_value(0), self.ring_op.animate.set_value(0),
                  self.plus_op.animate.set_value(0), FadeIn(cut), dq1_lab.animate.move_to(self.ring_pt(0) + RIGHT * 0.45),
                  run_time=1.0)
        tri = self.triangle()
        self.until(22.75)                                 # "A distância dele até P é a hipotenusa…"
        self.play(Create(tri.seg_s), FadeIn(tri.lab_s), run_time=0.6)                       # s
        self.until(26.34)                                 # "…um cateto é o raio,"
        self.play(Create(tri.seg_r), FadeIn(tri.lab_r), Create(tri.corner), run_time=0.6)   # R
        self.until(27.64)                                 # "…o outro é a altura."
        self.play(Create(tri.seg_z), FadeIn(tri.lab_z), run_time=0.6)                       # z
        eq_s = mtex("s^2", "=", "R^2", "+", "z^2", size=56).move_to([0, Y_EQ, 0])
        eq_s[0].set_color(VIOLET)
        self.until(28.94)                                  # "Então essa distância ao quadrado é R² mais z²."
        self.swap_eq(eq_s)
        # invariância: o elemento oposto (seção em −R) está à mesma distância s de P
        s_opp = DashedLine(self.o() + LEFT * RS, self.p_pt(), dash_length=0.12).set_stroke(VIOLET, 4)
        s_opp_lab = tex("s", 38, VIOLET).move_to((self.o() + LEFT * RS + self.p_pt()) / 2 + np.array([-0.3, 0.25, 0]))
        self.until(33.37)                                  # "E todo pedacinho do anel está a essa mesma distância de P."
        self.play(Create(s_opp), FadeIn(s_opp_lab), Indicate(tri.lab_s, color=VIOLET), run_time=0.8)
        self.check_safe_area()

        # ── C4. O par oposto: laterais se cancelam, axiais se somam (36,8–52,5) ──
        self.until(36.76)                                  # "Agora vem a simetria."
        tri_all = VGroup(tri.seg_r, tri.seg_z, tri.seg_s, tri.corner, tri.lab_r, tri.lab_z, tri.lab_s)
        self.swap_eq(None, *self.caption("Simetria"), FadeOut(VGroup(tri_all, cut, s_opp, s_opp_lab)),
                     self.tilt.animate.set_value(TILT), self.ring_op.animate.set_value(1),
                     self.plus_op.animate.set_value(1), self.p_op.animate.set_value(0),
                     dq1_lab.animate.move_to(self.ring_pt(0) + np.array([0.5, -0.36, 0])), run_time=1.2)
        dq2 = self.dq_mark(PI, MAGENTA)
        dq2_lab = tex("dq", 38, MAGENTA).move_to(self.ring_pt(PI) + np.array([-0.5, -0.36, 0]))
        self.until(39.3)                                  # "Pra cada pedacinho, existe outro do lado oposto."
        self.play(FadeIn(dq2), FadeIn(dq2_lab), run_time=0.7)
        p = self.p_pt()
        d1, d2 = pair_vectors(U_MODEL)
        dE1, dE2 = vec(p, p + d1, CYAN, 7), vec(p, p + d2, MAGENTA, 7)
        dE1_lab = tex(r"d\vec E_1", 40, CYAN).next_to(p + d1, LEFT, 0.12)
        dE2_lab = tex(r"d\vec E_2", 40, MAGENTA).next_to(p + d2, RIGHT, 0.12)
        self.until(41.07)                                   # 1. "Os campos dos dois…"
        self.play(GrowArrow(dE1), GrowArrow(dE2), FadeIn(dE1_lab, dE2_lab), run_time=0.9)
        self.check_safe_area()

        # 2. decomposição ponta–cauda: lateral a partir de P, axial na ponta da lateral
        h1, v1 = vec(p, p + d1 * RIGHT, CYAN, 6), vec(p + d1 * RIGHT, p + d1, CYAN, 6)
        h2, v2 = vec(p, p + d2 * RIGHT, MAGENTA, 6), vec(p + d2 * RIGHT, p + d2, MAGENTA, 6)
        ticks = VGroup(*(VGroup(*(Line(m + np.array([dx, -0.12, 0]), m + np.array([dx, 0.12, 0]))
                                  for dx in (-0.05, 0.05)))
                         for m in (p + d1 * RIGHT / 2, p + d2 * RIGHT / 2))).set_stroke(WHITE, 3)
        self.until(42.1)                                  # 2. "…têm partes laterais…"
        self.play(dE1.animate.set_opacity(0.3), dE2.animate.set_opacity(0.3),
                  GrowArrow(h1), GrowArrow(h2), GrowArrow(v1), GrowArrow(v2), run_time=1.0)
        self.until(43.2)                                    # 3–4. "…iguais e opostas,"
        aux = tag("MESMO MÓDULO · SENTIDOS OPOSTOS", 22, 0.75).move_to([0, Y_TAG, 0])
        self.swap_eq(tag("LATERAIS SE CANCELAM").move_to([0, Y_EQ, 0]),
                     v1.animate.set_opacity(0.25), v2.animate.set_opacity(0.25), Create(ticks), FadeIn(aux),
                     run_time=0.8)
        self.until(44.52)                                   # 5. "…então elas se cancelam."
        self.play(h1.animate.scale(0.02, about_point=p).set_opacity(0),
                  h2.animate.scale(0.02, about_point=p).set_opacity(0), FadeOut(ticks), FadeOut(aux), run_time=1.0)
        self.remove(h1, h2)
        self.until(45.95)                                   # 6–7. "Já as partes ao longo do eixo apontam pro mesmo lado…"
        aux = tag("MESMO SENTIDO", 22, 0.75).move_to([0, Y_TAG, 0])
        self.swap_eq(tag("AXIAIS SE SOMAM").move_to([0, Y_EQ, 0]),
                     v1.animate.set_opacity(1), v2.animate.set_opacity(1), FadeIn(aux), run_time=0.8)
        self.until(48.2)                                    # 8. "…e se somam."
        self.play(v1.animate.shift(-d1 * RIGHT), v2.animate.shift(-d2 * RIGHT + d1 * UP), FadeOut(aux),
                  run_time=1.2)
        axial = vec(p, p + 2 * d1 * UP, WHITE, 8)
        self.until(49.45)
        self.play(ReplacementTransform(VGroup(v1, v2), axial), run_time=0.6)
        self.check_safe_area()

        # 9. generalização: cada par gira pelo anel e só a componente axial fica
        pair = always_redraw(self.pair)
        self.until(50.1)                                  # 9. "No anel inteiro, só sobra o campo no eixo."
        self.swap_eq(tag("SÓ SOBRA A COMPONENTE NO EIXO", 30).move_to([0, Y_EQ, 0]),
                     FadeOut(VGroup(dE1, dE2, dE1_lab, dE2_lab, dq1_lab, dq2_lab)),
                     FadeOut(dq1), FadeOut(dq2), FadeIn(pair), run_time=0.8)
        self.play(self.pair_phi.animate.set_value(PI), run_time=1.3)
        self.check_safe_area()

        # ── C5. Campo de um elemento (52,5–87,9): uma transformação por estado ──
        self.until(52.52)                                  # "Então vamos calcular essa parte pra um pedacinho."
        dq1 = self.dq_mark(0, CYAN)
        dq1_lab = tex("dq", 38, CYAN).move_to(self.ring_pt(0) + RIGHT * 0.45)
        self.swap_eq(None, *self.caption("Campo de um elemento"), FadeOut(pair), FadeOut(axial), FadeIn(dq1),
                     FadeIn(dq1_lab), self.tilt.animate.set_value(0), self.ring_op.animate.set_value(0),
                     self.plus_op.animate.set_value(0), self.p_op.animate.set_value(1), FadeIn(cut), run_time=1.2)
        tri = self.triangle(op=0.75)
        tri_all = VGroup(tri.seg_r, tri.seg_z, tri.seg_s, tri.corner, tri.lab_r, tri.lab_z, tri.lab_s)
        theta = np.arctan2(1.0, U_MODEL)                                  # ângulo entre dE e o eixo
        assert np.isclose(np.cos(theta), U_MODEL / np.hypot(1.0, U_MODEL))   # cos θ = z/s
        assert np.isclose(np.arctan2(d1[1], d1[0]), PI / 2 + theta)          # θ de cima: eixo → dE
        to_o, to_dq = self.o() - p, self.ring_pt(0) - p
        assert np.isclose(np.arccos(np.dot(to_o, to_dq) / np.linalg.norm(to_o) / np.linalg.norm(to_dq)), theta)
        dE = vec(p, p + d1, CYAN, 7)
        dE_lab = tex(r"d\vec E", 40, CYAN).next_to(p + d1, LEFT, 0.12)
        up_line = DashedLine(p, p + UP * 1.7, dash_length=0.09).set_stroke(WHITE, 2, 0.55)
        arc_top = Arc(radius=0.6, start_angle=PI / 2, angle=theta, arc_center=p).set_stroke(VIOLET, 4)
        th_top = tex(r"\theta", 36, VIOLET).move_to(p + 0.92 * np.array([np.cos(PI / 2 + theta / 2),
                                                                          np.sin(PI / 2 + theta / 2), 0]))
        arc_in = Arc(radius=0.6, start_angle=-PI / 2, angle=theta, arc_center=p).set_stroke(VIOLET, 4)
        th_in = tex(r"\theta", 36, VIOLET).move_to(p + 0.92 * np.array([np.cos(-PI / 2 + theta / 2),
                                                                         np.sin(-PI / 2 + theta / 2), 0]))
        self.until(53.75)
        self.play(FadeIn(tri_all), GrowArrow(dE), FadeIn(dE_lab), run_time=0.9)
        self.play(Create(up_line), Create(arc_top), FadeIn(th_top), run_time=0.6)
        self.check_safe_area()

        # Estado 1: dE = k dq/s² — dq, s e dE ligados ao desenho
        eq1 = mtex("dE", "=", "k", r"\frac{dq}{s^2}", size=EQ5).move_to([0, Y_EQ5, 0])
        num1, _, den1 = frac_parts(eq1[3])
        eq1[0].set_color(CYAN), num1.set_color(CYAN), den1.set_color(VIOLET)
        self.until(55.3)                                  # "Pela lei de Coulomb…"
        self.swap_eq(eq1)
        self.until(56.0)                                  # "…o campo que ele cria"
        self.play(Indicate(eq1[0], color=CYAN), Indicate(dE_lab, color=CYAN), run_time=0.6)
        self.until(58.0)                                  # "…é k vezes a carga dele,"
        self.play(Indicate(num1, color=CYAN), Indicate(dq1_lab, color=CYAN), run_time=0.6)
        self.until(59.6)                                  # "…dividido pela distância ao quadrado."
        self.play(Indicate(den1, color=VIOLET), Indicate(tri.lab_s, color=VIOLET), run_time=0.6)

        # Estado 2: dE_z = dE cos θ — projeção axial no desenho
        eq2 = mtex("dE_z", "=", "dE", r"\cos\theta", size=EQ5).move_to([0, Y_EQ5, 0])
        eq2[0].set_color(CYAN), eq2[2].set_color(CYAN)
        dEz = vec(p, p + d1 * UP, CYAN, 7)
        proj = DashedLine(p + d1, p + d1 * UP, dash_length=0.07).set_stroke(WHITE, 2, 0.6)
        dEz_lab = tex("dE_z", 36, CYAN).next_to(p + d1 * UP * 0.6, RIGHT, 0.15)
        self.until(61.0)                                  # "Mas só interessa a parte no eixo, e aí entra o cosseno…"
        self.play(TransformMatchingTex(eq1, eq2), FadeOut(up_line), Create(proj), GrowArrow(dEz),
                  FadeIn(dEz_lab), dE.animate.set_opacity(0.45), run_time=1.0)
        self.eq = eq2

        # Estado 3: cos θ = z/s — cateto z e hipotenusa s; o mesmo θ dentro do triângulo
        eq3 = mtex(r"\cos\theta", "=", r"\frac{z}{s}", size=EQ5).move_to([0, Y_EQ5, 0])
        frac_parts(eq3[2])[2].set_color(VIOLET)
        self.until(65.19)                                  # "No triângulo, cosseno é…"
        self.swap_eq(eq3)
        self.until(66.4)                                  # "…cateto adjacente…"
        self.play(Indicate(tri.lab_z, color=WHITE, scale_factor=1.4), tri.seg_z.animate.set_stroke(opacity=1),
                  run_time=0.6)
        self.until(67.7)                                  # "…sobre hipotenusa:"
        self.play(Indicate(tri.lab_s, color=VIOLET, scale_factor=1.4), tri.seg_s.animate.set_stroke(opacity=1),
                  run_time=0.6)
        self.until(68.9)                                  # "…a altura z dividida pela distância." (mesmo θ)
        self.play(Create(arc_in), FadeIn(th_in), Indicate(th_top, color=VIOLET), run_time=0.7)
        self.check_safe_area()

        # Estado 4: substituição explícita — os dois fatores entram em dE_z = dE cos θ e saem de cima
        rem_a = mtex("dE", "=", "k", r"\frac{dq}{s^2}", size=40).move_to([-2.0, Y_REM5, 0])
        na, _, da = frac_parts(rem_a[3])
        rem_a[0].set_color(CYAN), na.set_color(CYAN), da.set_color(VIOLET)
        rem_b = mtex(r"\cos\theta", "=", r"\frac{z}{s}", size=40).move_to([2.1, Y_REM5, 0])
        frac_parts(rem_b[2])[2].set_color(VIOLET)
        eq2b = eq2.copy().move_to([0, Y_EQ5, 0])
        self.until(71.3)                                  # "Juntando as duas coisas,"
        self.swap_eq(eq2b, FadeIn(rem_a, rem_b), run_time=0.7)
        eq4 = mtex("dE_z", "=", "k", r"\frac{dq}{s^2}", r"\cdot", r"\frac{z}{s}", size=EQ5).move_to([0, Y_EQ5, 0])
        n4, _, d4 = frac_parts(eq4[3])
        eq4[0].set_color(CYAN), n4.set_color(CYAN), d4.set_color(VIOLET)
        frac_parts(eq4[5])[2].set_color(VIOLET)
        self.until(72.05)
        self.play(ReplacementTransform(eq2b[0], eq4[0]), ReplacementTransform(eq2b[1], eq4[1]),
                  FadeOut(eq2b[2]), FadeOut(eq2b[3]), ReplacementTransform(rem_a[2:4].copy(), VGroup(eq4[2], eq4[3])),
                  ReplacementTransform(rem_b[2].copy(), eq4[5]), FadeIn(eq4[4]), run_time=1.2)
        self.play(FadeOut(rem_a), FadeOut(rem_b), run_time=0.4)
        self.eq = eq4

        # Estado 5: de onde vem s³ — a projeção trouxe mais um 1/s
        eq5 = mtex("dE_z", "=", r"\frac{kz\,dq}{s^2\cdot s}", size=EQ5).move_to([0, Y_EQ5, 0])
        n5, _, d5 = frac_parts(eq5[2])
        eq5[0].set_color(CYAN), n5[2:].set_color(CYAN), d5.set_color(VIOLET)
        self.until(73.7)                                  # "…aparece mais uma distância embaixo:"
        self.play(Indicate(eq4[5], color=VIOLET), run_time=0.5)
        self.play(TransformMatchingShapes(eq4, eq5), run_time=1.0)
        eq6 = mtex("dE_z", "=", r"\frac{kz\,dq}{s^3}", size=EQ5).move_to([0, Y_EQ5, 0])
        n6, bar6, d6 = frac_parts(eq6[2])
        eq6[0].set_color(CYAN), n6[2:].set_color(CYAN), d6.set_color(VIOLET)
        box5 = SurroundingRectangle(d5, color=VIOLET, buff=0.08, corner_radius=0.05, stroke_width=3)
        box6 = SurroundingRectangle(d6, color=VIOLET, buff=0.08, corner_radius=0.05, stroke_width=3)
        note = mtex(r"s^2\cdot s=s^3", size=42).set_color(VIOLET).move_to([0, Y_NOTE5, 0])
        self.until(75.4)                                  # "…ao quadrado vezes mais uma, dá ao cubo."
        self.play(Create(box5), run_time=0.3)                     # destaque curto só no denominador
        self.play(TransformMatchingShapes(eq5, eq6), ReplacementTransform(box5, box6),
                  FadeIn(note, shift=UP * 0.1), run_time=1.0)
        self.eq = eq6
        self.check_safe_area()

        # Estado 6: recuperar a geometria — s² = R² + z² → s = √(R² + z²); a principal fica em segundo plano
        rem5 = mtex(r"s^2=R^2+z^2", size=46).move_to([0, Y_REM5, 0])
        rem5[0][0].set_color(VIOLET)
        self.until(77.3)                                  # "E, como a distância é a raiz de R² mais z²,"
        self.play(FadeOut(note), FadeOut(box6), eq6.animate.set_opacity(0.35), FadeIn(rem5, shift=UP * 0.1),
                  Indicate(tri.lab_s, color=VIOLET), run_time=0.6)
        rem6 = mtex(r"s=\sqrt{R^2+z^2}", size=46).move_to([0, Y_REM5, 0])
        rem6[0][0].set_color(VIOLET)
        self.until(78.3)
        self.play(TransformMatchingShapes(rem5, rem6), run_time=0.9)

        # Estado 7: de onde vem 3/2 — só a raiz/potência em violeta
        rem7a = mtex(r"s^3=\left[\sqrt{R^2+z^2}\right]^3", size=46).move_to([0, Y_REM5, 0])
        assert len(rem7a[0]) == 13, len(rem7a[0])
        rem7a[0][0].set_color(VIOLET)
        VGroup(*(rem7a[0][i] for i in (3, 4, 5, 11, 12))).set_color(VIOLET)   # [ √ ‾ ] ³
        self.until(81.1)                                  # "…elevar ao cubo…"
        self.play(TransformMatchingShapes(rem6, rem7a), run_time=0.9)
        rem7 = mtex(r"s^3=(R^2+z^2)^{3/2}", size=46).move_to([0, Y_REM5, 0])
        assert len(rem7[0]) == 13, len(rem7[0])
        rem7[0][0].set_color(VIOLET), rem7[0][-3:].set_color(VIOLET)            # s … 3/2
        self.until(83.6)                                  # "…dá R² mais z², elevado a três meios."
        self.play(TransformMatchingShapes(rem7a, rem7), run_time=0.9)
        self.check_safe_area()

        # Estado 8: resultado diferencial — o denominador vem da relação de cima; nada ao redor
        final = mtex("dE_z", "=", r"\frac{kz\,dq}{(R^2+z^2)^{3/2}}", size=EQ5)
        nf, barf, denf = frac_parts(final[2])
        assert len(denf) == 10, len(denf)
        final_box = boxed(final).move_to([0, Y_EQ5, 0])
        self.until(84.9)
        self.play(ReplacementTransform(eq6[0], final[0]), ReplacementTransform(eq6[1], final[1]),
                  ReplacementTransform(n6, nf), ReplacementTransform(bar6, barf), FadeOut(d6),
                  ReplacementTransform(VGroup(*rem7[0][3:]), denf), FadeOut(VGroup(*rem7[0][:3])),
                  Create(final_box[1]), run_time=1.0)
        self.eq = final_box
        self.check_safe_area()

        # ── C6. Somar o anel (87,9–97,9): a varredura é a ∫dq ───────────────────
        self.until(87.9)                                  # dE_z fica sob "Agora é só somar o anel inteiro." e sai em "Temos que…"
        sweep = always_redraw(self.sweep_arc)
        self.swap_eq(None, *self.caption("Somar o anel"),
                     FadeOut(VGroup(tri_all, dE, dE_lab, dEz, dEz_lab, proj, arc_top, th_top, arc_in, th_in, cut)),
                     FadeOut(dq1), FadeOut(dq1_lab), self.tilt.animate.set_value(TILT),
                     self.ring_op.animate.set_value(1), self.plus_op.animate.set_value(1), run_time=1.2)
        eq_i = mtex("E(z)", "=", r"\int dE_z").move_to([0, Y_EQ6, 0])
        self.add(sweep)
        self.until(89.2)
        self.swap_eq(eq_i)
        eq_f = mtex("E(z)", "=", r"\frac{kz}{(R^2+z^2)^{3/2}}", r"\,\int dq").move_to([0, Y_EQ6, 0])
        eq_f[3].set_color(CYAN)
        self.until(90.5)                                  # "…o raio e a altura são os mesmos pra todo pedacinho,"
        self.play(TransformMatchingTex(eq_i, eq_f), run_time=1.0)
        self.eq = eq_f
        const_box = SurroundingRectangle(eq_f[2], color=VIOLET, buff=0.1, corner_radius=0.06, stroke_width=3)
        fixed = VGroup(tex("R", 36, VIOLET), text("e", 26, VIOLET), tex("z", 36, VIOLET), text("fixos", 26, VIOLET)
                       ).arrange(RIGHT, buff=0.12).next_to(const_box, DOWN, 0.2)
        self.until(91.6)                                  # "…então saem da soma."
        self.play(Create(const_box), FadeIn(fixed, shift=UP * 0.1), run_time=0.8)
        self.until(93.5)                                  # "Sobra somar as cargas,"
        self.play(Indicate(eq_f[3], color=CYAN), self.sweep.animate(rate_func=linear).set_value(2 * PI),
                  run_time=1.4)                           # o dq percorre o anel = ∫dq
        # ∫dq = Q abaixo do ∫dq (limitado à margem), fora da caixa do fator constante
        q_int = mtex(r"\int dq", "=", "Q", size=42)
        q_int.shift([min(eq_f[3].get_center()[0] - q_int[0].get_center()[0], SAFE_X - 0.2 - q_int.get_right()[0]),
                     Y_QINT - q_int.get_center()[1], 0])
        q_int[0].set_color(CYAN)
        assert q_int.get_top()[1] < eq_f.get_bottom()[1] - 0.25 and q_int.get_right()[0] < SAFE_X
        assert q_int.get_top()[1] < const_box.get_bottom()[1] - 0.2          # folga para a caixa violeta
        self.until(94.95)                                  # "…e isso dá a carga total Q."
        self.play(ReplacementTransform(eq_f[3].copy(), q_int[0]), FadeIn(q_int[1:]), FadeOut(fixed), run_time=0.8)
        res_e = boxed(mtex("E(z)", "=", r"\frac{kQz}{(R^2+z^2)^{3/2}}", size=56)).move_to([0, Y_EQ6, 0])
        self.until(95.9)                                  # "Pronto: esse é o campo no eixo."
        self.play(TransformMatchingShapes(VGroup(eq_f, q_int), res_e[0]), FadeOut(const_box), Create(res_e[1]),
                  FadeOut(sweep), self.arrow_op.animate.set_value(1), run_time=0.9)
        self.eq = res_e
        self.check_safe_area()

        # ── C7. Checagens físicas (97,9–108,6) ─────────────────────────────────
        self.until(97.88)                                 # "Dois testes rápidos:" (resultado ainda na tela)
        self.play(*self.caption("Dois testes"), run_time=0.6)
        self.until(99.2)                                  # "…no centro, z igual a zero dá campo zero."
        self.swap_eq(None, self.u.animate.set_value(0), run_time=1.2)
        self.until(100.4)
        self.swap_eq(mtex("z=0", r"\;\Rightarrow\;", "E=0").move_to([0, Y_EQ, 0]))
        self.until(101.9)                                  # "E, visto de muito longe,"
        self.swap_eq(None, self.u.animate.set_value(U_MODEL), run_time=0.8)
        self.play(self.arrow_op.animate.set_value(0), self.plus_op.animate.set_value(0), run_time=0.4)
        # z ≫ R: P fica na mesma altura da tela enquanto o anel é visto de longe (u·rs constante)
        self.u.add_updater(lambda m: m.set_value(RS * U_MODEL / self.rs.get_value()))
        far = tag("VISTO DE MUITO LONGE", 24, 0.8).move_to([0, O_Y - 0.9, 0])
        self.until(103.1)
        self.swap_eq(mtex(r"z", r"\gg", "R").move_to([0, Y_EQ, 0]), FadeIn(far),
                     self.rs.animate.set_value(RS * U_MODEL / U_FAR), run_time=2.0)
        self.u.clear_updaters()
        q_far = tex("Q", 38).move_to(self.o() + np.array([0.38, -0.28, 0]))
        self.until(105.2)                                  # "…a expressão vira kQ sobre z²: o anel parece uma carga pontual."
        self.swap_eq(mtex("E", r"\approx", r"\frac{kQ}{z^2}").move_to([0, Y_EQ, 0]), FadeIn(q_far))
        self.check_safe_area()

        # ── C8. Ver a função (108,6–115,4): P, seta e marcador pelo mesmo self.u ──
        self.until(108.57)                                  # "Agora acompanha o mesmo ponto no eixo e no gráfico:"
        self.u.add_updater(lambda m: m.set_value(RS * U_MODEL / self.rs.get_value()))
        self.swap_eq(None, *self.caption("O campo ao longo do eixo"), FadeOut(q_far), FadeOut(far),
                     self.rs.animate.set_value(RS_G), self.oy.animate.set_value(O_Y_G),
                     self.plus_op.animate.set_value(1), run_time=1.3)
        self.u.clear_updaters()
        g_axes = VGroup(Line([GX0, GY0, 0], [GX1 + 0.1, GY0, 0]), Line([GX0, GY0, 0], [GX0, GY0 + GH + 0.3, 0])
                        ).set_stroke(BLUE, 3, 0.75)
        g_labs = VGroup(tex("z", 32).move_to([GX1 + 0.25, GY0 - 0.22, 0]),
                        tex("E(z)", 32).next_to([GX0, GY0 + GH + 0.3, 0], RIGHT, 0.12))
        g_faint = VMobject().set_points_as_corners([gpt(v) for v in np.linspace(0, U_GRAPH, 241)]
                                                   ).set_stroke(CYAN, 3, 0.22)
        g_trace = always_redraw(self.trace_curve)
        g_drop = always_redraw(self.drop_line)
        g_mark = always_redraw(lambda: Dot(gpt(self.u.get_value()), 0.11, color=WHITE))
        self.until(109.9)
        self.play(self.u.animate.set_value(0), FadeIn(g_axes, g_labs, g_faint), run_time=1.0)
        self.trace.add_updater(lambda m: m.set_value(max(m.get_value(), self.u.get_value())))
        self.add(g_trace, g_drop, g_mark)
        self.play(self.arrow_op.animate.set_value(1), run_time=0.3)
        self.check_safe_area()
        self.until(111.5)                                  # "…o campo sai de zero, cresce, passa pelo pico e cai."
        self.play(self.u.animate.set_value(U_SWEEP), run_time=3.7, rate_func=slow_peak(U_SWEEP))
        self.check_safe_area()

        # ── C9. Encontrar o máximo (115,4–133,1) ───────────────────────────────
        self.until(115.38)                                  # "Pra achar esse pico, derivamos o campo em relação à altura."
        self.play(*self.caption("Encontrar o máximo"), self.view_op.animate.set_value(0), run_time=0.9)
        self.until(116.3)
        self.swap_eq(mtex("E(z)", "=", "kQz", r"\,(R^2+z^2)^{-3/2}").move_to([0, Y_C9, 0]))
        deriv = mtex(r"\frac{dE}{dz}", "=", r"kQ\,", r"\frac{R^2-2z^2}{(R^2+z^2)^{5/2}}").move_to([0, Y_C9, 0])
        num, _, den = frac_parts(deriv[3])
        assert len(num) == 6 and len(den) == 10, (len(num), len(den))
        self.until(117.6)
        self.swap_eq(deriv, run_time=0.8)
        num_box = SurroundingRectangle(num, color=VIOLET, buff=0.1, corner_radius=0.06, stroke_width=3)
        den_pos = mtex(r"(R^2+z^2)^{5/2}", ">", "0", size=40).set_opacity(0.75).move_to([0, Y_C9_NOTE, 0])
        self.until(118.6)                                 # "O denominador é sempre positivo,"
        self.play(den.animate.set_opacity(0.55), FadeIn(den_pos, shift=UP * 0.1), run_time=0.8)
        self.until(120.4)                                 # "…então o sinal depende do numerador:"
        self.play(num.animate.set_color(VIOLET), Create(num_box), run_time=0.7)
        self.check_safe_area()
        root = mtex("R^2", "-", "2z^2", "=", "0").move_to([0, Y_C9, 0])
        VGroup(*root[:3]).set_color(VIOLET)
        self.until(122.55)                                 # "R² menos dois z²": numerador zera ↔ marcador vai ao pico
        self.play(ReplacementTransform(num.copy(), VGroup(*root[:3])), FadeIn(VGroup(*root[3:])),
                  FadeOut(deriv), FadeOut(num_box), FadeOut(den_pos),
                  self.u.animate.set_value(U_STAR), run_time=1.6)
        self.eq = root
        self.until(125.25)                                  # "Ele zera quando z é R sobre raiz de dois,"
        solve = mtex("2z^2", "=", "R^2").move_to([0, Y_C9, 0])
        self.play(TransformMatchingTex(root, solve), run_time=0.9)
        self.eq = solve
        self.until(126.5)
        assert np.isclose(self.u.get_value(), U_STAR)      # R/√2 só surge com o marcador no pico
        z_star = mtex("z", "=", r"\frac{R}{\sqrt2}", size=58)
        z_box = boxed(z_star).move_to([0, Y_C9, 0])
        self.play(TransformMatchingTex(solve, z_star), Create(z_box[1]), run_time=0.9)
        self.eq = z_box
        # sinais de dE/dz sobre os trechos da curva
        signs = VGroup(tex("+", 50, VIOLET).move_to(gpt(0.36) + np.array([0.38, -0.3, 0])),
                       tex("0", 44, VIOLET).move_to(gpt(U_STAR) + UP * 0.4),
                       tex("-", 50, VIOLET).move_to(gpt(1.8) + DOWN * 0.45))
        assert signs[0].get_left()[0] > GX0 + 0.5              # + longe do eixo vertical
        self.until(128.3)                                  # "…e a derivada passa de positiva pra negativa."
        self.play(LaggedStart(*(FadeIn(s, scale=1.3) for s in signs), lag_ratio=0.35), run_time=1.0)
        self.until(131.03)                                # "Aí isso diz que ali é o máximo."
        self.play(Indicate(z_box, color=VIOLET, scale_factor=1.08), Indicate(signs[1], color=VIOLET), run_time=0.9)
        self.check_safe_area()

        # ── C10. Resultado físico (133,1–140,3): anel à esquerda, resultado à direita ──
        self.until(133.14)                                  # "Portanto, o campo é mais forte a R sobre raiz de dois,"
        self.swap_eq(None, *self.caption("Onde o campo é máximo"), FadeOut(signs),
                     self.view_op.animate.set_value(1), self.ox.animate.set_value(OX_RESULT), run_time=1.2)
        o, p = self.o(), self.p_pt()
        cota = dim_mark(o + RIGHT * 0.42, p + RIGHT * 0.42, VIOLET)
        cota_lab = tex(r"\frac{R}{\sqrt2}", 38, VIOLET).next_to(p + RIGHT * 0.42 + DOWN * 0.12, RIGHT, 0.16)
        assert cota_lab.get_bottom()[1] > o[1] + TILT * RS_G + 0.12   # acima da borda de trás do anel
        peak = gpt(U_STAR)
        g_guide = DashedLine([peak[0], GY0, 0], peak, dash_length=0.07).set_stroke(VIOLET, 2.5)
        g_star = tex(r"\frac{R}{\sqrt2}", 32, VIOLET).move_to([peak[0], GY0 - 0.4, 0])
        self.until(134.4)
        self.play(Create(cota), FadeIn(cota_lab), FadeIn(g_guide, g_star), run_time=0.8)
        res = boxed(mtex(r"z_{\max}", "=", r"\frac{R}{\sqrt2}", size=46)).move_to([X_NOTE, 2.4, 0])
        self.until(135.3)
        self.play(FadeIn(res, shift=UP * 0.1), run_time=0.7)
        approx = mtex(r"\frac{R}{\sqrt2}", r"\approx", r"0{,}71\,R", size=38).move_to([X_NOTE, 1.1, 0])
        self.until(136.5)                                  # "…cerca de zero vírgula setenta e um R acima do plano do anel."
        self.play(FadeIn(approx, shift=UP * 0.1), run_time=0.7)
        self.check_safe_area()

        # ── C11. Fechamento (140,3–148,3): síntese revelada em três passos ──────
        chain = VGroup(display("SIMETRIA", 32), tex(r"\rightarrow", 36, VIOLET), display("INTEGRAÇÃO", 32),
                       tex(r"\rightarrow", 36, VIOLET), display("MÁXIMO", 32)).arrange(RIGHT, buff=0.18)
        chain.scale_to_fit_width(min(chain.width, 2 * SAFE_X - 0.2))
        chain.move_to([0, HEADLINE_TOP - chain.height / 2, 0])
        self.until(140.26)                                  # "Simetria pra saber o que sobra,"
        self.play(FadeOut(self.headline, shift=UP * 0.15), FadeIn(chain[0], shift=DOWN * 0.15), run_time=0.6)
        self.headline = chain
        self.until(142.09)                                  # "…integração pra somar as cargas…"
        self.play(FadeIn(chain[1:3], shift=RIGHT * 0.1), run_time=0.6)
        self.until(144.2)                                  # "…e derivada pra achar o máximo."
        self.play(FadeIn(chain[3:], shift=RIGHT * 0.1), run_time=0.6)
        handle = tag("@labparallax", 22, 0.8).next_to(chain, DOWN, 0.3)
        self.until(145.91)                                  # "Se curtiu, siga o Parallax Lab."
        self.play(FadeIn(handle, shift=UP * 0.1), run_time=0.6)
        self.check_safe_area()
        self.until(148.3)                                  # WAV tem 148,0 s
