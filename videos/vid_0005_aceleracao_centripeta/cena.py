"""Origem geométrica de a_c = v²/R; preview visual silencioso (2ª rodada).

POR TRÁS DA FÓRMULA · EP. 02. Movimento circular uniforme: |v| constante,
direção de v variando. Dois instantes simétricos t± = t ± Δt/2 (ângulos
θ ± Δθ/2 em torno de THETA_C) dão r± de módulo R e v± de módulo v, ambos
separados por Δθ. Δv = v₊ − v₋ é construído na origem comum (translação
pura) e, pela simetria, aponta exatamente para −r̂(t). Triângulos isósceles
de mesmo Δθ ⇒ |Δv|/v = |Δr|/R; com |Δr|/Δt → v e |Δv|/Δt → a_c, a_c = v²/R.
Sem aproximação de arco: Δr é a corda.

Terminologia: "módulo da velocidade" para |v| = v; "vetor velocidade" para a seta.
Cores: azul discreto = trajetória; branco = r e matemática; azul = Δr;
ciano = v; magenta = Δv; violeta = a_c.
"""

import numpy as np
from manim import (
    DOWN, LEFT, PI, RIGHT, UP, Arc, Arrow, Circle, Create,
    DashedLine, Dot, FadeIn, FadeOut, GrowArrow, ImageMobject, Indicate, MathTex,
    ReplacementTransform, RoundedRectangle, Scene, SurroundingRectangle,
    TransformFromCopy, TransformMatchingShapes, VGroup, VMobject, ValueTracker,
    Write, always_redraw, linear,
)

from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # v
BLUE = "#267BFF"          # trajetória (discreta) e Δr
VIOLET = SECONDARY_COLOR  # a_c
MAGENTA = "#EA63FF"       # Δv

R_VIS = 2.2               # raio na tela
L_V = 1.5                 # |v| na tela, fixo em toda a cena
L_A = 1.1                 # |a_c| na tela (fechamento)
THETA_C = 0.0             # direção de r no instante central t
DTH_START = 50 * PI / 180 # Δθ da construção
DTH_MIN = 16 * PI / 180   # Δθ ao fim do limite: v₋ e v₊ ainda distinguíveis
SAFE_BOTTOM = -4.6        # abaixo disso: faixa reservada a legendas
HEADLINE_TOP = 6.85

O_A = np.array([-0.7, 2.2, 0])   # círculo das partes A–C
Q_C = np.array([0.0, -3.75, 0])  # origem comum das velocidades (C)
O_D = np.array([-3.6, 1.8, 0])   # triângulo das posições (D)
Q_D = np.array([2.2, 0.85, 0])   # triângulo das velocidades (D)
O_E = np.array([-1.2, 1.3, 0])   # círculo do limite (E)
Q_E = np.array([3.0, -0.05, 0])  # triângulo das velocidades do limite (E)
O_F = np.array([0.0, 2.2, 0])    # círculo do fechamento (F)


def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0.0])


def tangent(angle):
    """Direção de v no ponto de ângulo `angle` (movimento anti-horário)."""
    return unit(angle + PI / 2)


def tex(content, size=40, color=WHITE):
    return MathTex(content, font_size=size, color=color)


def text(content, size=24, color=WHITE, opacity=1.0):
    return screen_text(content, size, color=color).set_opacity(opacity)


def display(content, size=38):
    return screen_text(content, size, oversample=2, color=WHITE)


def baseline_glyph(mob):
    """Glifo mais baixo de um MathTex sem descendentes (ex.: o v de \\vec v)."""
    return min(mob[0], key=lambda g: g.get_bottom()[1])


def inline(parts, gap):
    """Texto e MathTex numa linha; parts = (mobject, glifo que repousa na linha de base)."""
    x = 0.0
    for mob, glyph in parts:
        mob.shift(-glyph.get_bottom()[1] * UP)
        mob.shift((x - mob.get_left()[0]) * RIGHT)
        x = mob.get_right()[0] + gap
    return VGroup(*(mob for mob, _ in parts))


def vec(start, end, color, width=6):
    return Arrow(start, end, buff=0, color=color, stroke_width=width, tip_length=0.24,
                 max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=30)


def right_angle(P, d1, d2, size=0.18):
    return VMobject().set_points_as_corners(
        [P + size * d1, P + size * (d1 + d2), P + size * d2]).set_stroke(WHITE, 2, 0.55)


def orb(point):
    return VGroup(Dot(point, radius=0.2, color=CYAN, fill_opacity=0.18),
                  Dot(point, radius=0.1, color=WHITE))


def color_slices(mob, *pairs):
    """pairs: (índice do termo, fatia de glifos ou None, cor)."""
    for term, glyphs, color in pairs:
        (mob[term] if glyphs is None else mob[term][glyphs]).set_color(color)
    return mob


def side_labels(Q, dth, label_m, label_p, size, theta=THETA_C):
    """Rótulos de v₋ e v₊ na origem comum Q, cada um do lado de fora do triângulo."""
    a_m, a_p = theta - dth / 2, theta + dth / 2
    return VGroup(
        tex(label_m, size, CYAN).move_to(Q + 0.55 * L_V * tangent(a_m) + 0.34 * unit(a_m)),
        tex(label_p, size, CYAN).move_to(Q + 0.55 * L_V * tangent(a_p) + 0.34 * unit(a_p + PI)))


NUM = slice(0, 5)  # glifos de |Δx⃗| no numerador de \frac{|\Delta\vec x|}{...}


class Construction:
    """P±, r±, Δr, v± e Δθ em um círculo de centro O, para instantes t ± Δt/2."""

    def __init__(self, O, dth, theta=THETA_C):
        self.a_m, self.a_p = theta - dth / 2, theta + dth / 2
        self.O = O
        self.P_m, self.P_p = O + R_VIS * unit(self.a_m), O + R_VIS * unit(self.a_p)
        self.r_m, self.r_p = vec(O, self.P_m, WHITE, 4), vec(O, self.P_p, WHITE, 4)
        self.dr = vec(self.P_m, self.P_p, BLUE, 5)
        self.v_m = vec(self.P_m, self.P_m + L_V * tangent(self.a_m), CYAN)
        self.v_p = vec(self.P_p, self.P_p + L_V * tangent(self.a_p), CYAN)
        self.arc = Arc(radius=0.55, start_angle=self.a_m, angle=dth, arc_center=O,
                       color=WHITE, stroke_width=3)
        self.dots = VGroup(Dot(self.P_m, 0.07, color=WHITE), Dot(self.P_p, 0.07, color=WHITE))


class VelocityTriangle:
    """v± transladados para a origem comum Q e Δv = v₊ − v₋ de ponta a ponta."""

    def __init__(self, Q, dth, theta=THETA_C):
        a_m, a_p = theta - dth / 2, theta + dth / 2
        self.tip_m, self.tip_p = Q + L_V * tangent(a_m), Q + L_V * tangent(a_p)
        self.v_m, self.v_p = vec(Q, self.tip_m, CYAN), vec(Q, self.tip_p, CYAN)
        self.dv = vec(self.tip_m, self.tip_p, MAGENTA, 5)
        self.arc = Arc(radius=0.45, start_angle=a_m + PI / 2, angle=dth, arc_center=Q,
                       color=WHITE, stroke_width=3)


class AceleracaoCentripeta005(Scene):
    def check_safe_area(self):
        bottom = min(m.get_bottom()[1] for m in self.mobjects
                     if isinstance(m, VMobject) and len(m.get_all_points()))
        assert bottom > SAFE_BOTTOM, f"conteúdo invade a faixa inferior: {bottom:.2f}"

    def caption(self, *lines):
        """Troca a manchete do topo (linhas: str ou mobject pronto); devolve as animações."""
        new = VGroup(*(display(line) if isinstance(line, str) else line for line in lines))
        new.arrange(DOWN, buff=0.14)
        new.move_to([0, HEADLINE_TOP - new.height / 2, 0])
        anims = [FadeIn(new, shift=DOWN * 0.15)]
        if self.headline is not None:
            anims.append(FadeOut(self.headline, shift=UP * 0.15))
        self.headline = new
        return anims

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.headline = None
        watermark = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(watermark.to_corner(UP + RIGHT, buff=0.28))
        series = text("POR TRÁS DA FÓRMULA · EP. 02", 20, opacity=0.65)
        series.to_corner(UP + LEFT, buff=0.4)

        # ── A. Movimento circular: |v| constante, direção de v muda ─────────────
        circle = Circle(radius=R_VIS, arc_center=O_A).set_stroke(BLUE, 3, 0.55)
        center = Dot(O_A, 0.06, color=WHITE)
        o_label = tex("O", 32).set_opacity(0.8).next_to(center, DOWN + LEFT, buff=0.08)
        theta = ValueTracker(100 * PI / 180)

        def particle_point():
            return O_A + R_VIS * unit(theta.get_value())

        particle = always_redraw(lambda: orb(particle_point()))
        v_live = always_redraw(lambda: vec(
            particle_point(), particle_point() + L_V * tangent(theta.get_value()), CYAN))
        v_label = always_redraw(lambda: tex(r"\vec v", 36, CYAN).move_to(
            particle_point() + (L_V + 0.32) * tangent(theta.get_value())
            + 0.12 * unit(theta.get_value())))

        self.play(FadeIn(series),
                  *self.caption("Se o módulo da velocidade", "não muda, por que", "existe aceleração?"),
                  run_time=1.2)
        self.play(Create(circle), FadeIn(center, o_label), run_time=1.0)
        self.play(FadeIn(particle), GrowArrow(v_live), FadeIn(v_label), run_time=0.8)

        speed_line = tex(r"|\vec v|=\text{constante}", 42).move_to([0, -0.9, 0])
        speed_line[0][1].set_color(CYAN)
        speed_line[0][2].set_color(CYAN)
        dir_words = text("a direção de", 28), text("muda", 28)
        dir_vec = tex(r"\vec v", 34, CYAN)
        direction_line = inline([(dir_words[0], dir_words[0][-1]), (dir_vec, baseline_glyph(dir_vec)),
                                 (dir_words[1], dir_words[1][-1])], gap=0.14).move_to([0, -1.75, 0])

        omega = 2 * PI / 8.0  # rad/s na tela: uma volta em 8 s, sempre uniforme

        def orbit_to(degrees, *extra):
            target = degrees * PI / 180
            self.play(theta.animate.set_value(target), *extra,
                      run_time=(target - theta.get_value()) / omega, rate_func=linear)

        orbit_to(220, Write(speed_line))
        orbit_to(340, FadeIn(direction_line))
        orbit_to(460)

        # Microexplicação: três posições próximas, três cópias do mesmo vetor.
        copies, guides = VGroup(), VGroup()
        for degrees in (480, 520, 560):
            orbit_to(degrees)
            a, P = theta.get_value(), particle_point()
            copies.add(vec(P, P + L_V * tangent(a), CYAN).set_opacity(0.4))
            guides.add(DashedLine(P - 0.45 * tangent(a), P + (L_V + 0.4) * tangent(a),
                                  dash_length=0.08).set_stroke(WHITE, 1.5, 0.35))
            self.add(copies[-1])
        tag_same = text("MESMO MÓDULO", 20, opacity=0.85)
        tag_dir = text("· DIREÇÃO DIFERENTE", 20, color=CYAN)
        VGroup(tag_same, tag_dir).arrange(RIGHT, buff=0.16).move_to([0, -2.6, 0])
        self.play(FadeIn(tag_same), Indicate(copies, color=WHITE, scale_factor=1.05), run_time=1.0)
        self.play(FadeIn(tag_dir), Create(guides), run_time=1.0)
        self.play(*self.caption("O vetor velocidade muda"), run_time=0.8)
        self.wait(1.0)
        self.check_safe_area()

        # ── B. Dois instantes simétricos em torno de t ────────────────────────
        b = Construction(O_A, DTH_START)
        p_m_label = tex("P_-", 34).next_to(b.P_m, DOWN + RIGHT, buff=0.08)
        p_p_label = tex("P_+", 34).next_to(b.P_p, RIGHT, buff=0.16).shift(UP * 0.1)
        r_m_label = tex(r"\vec r_-", 34).move_to(O_A + 1.15 * unit(b.a_m) + 0.36 * unit(b.a_m - PI / 2))
        r_p_label = tex(r"\vec r_+", 34).move_to(O_A + 1.15 * unit(b.a_p) + 0.36 * unit(b.a_p + PI / 2))
        v_m_label = tex(r"\vec v_-", 34, CYAN).move_to(b.P_m + 0.62 * L_V * tangent(b.a_m) + 0.42 * unit(b.a_m))
        v_p_label = tex(r"\vec v_+", 34, CYAN).move_to(b.P_p + 0.62 * L_V * tangent(b.a_p) + 0.42 * unit(b.a_p + 0.35))
        dth_label = tex(r"\Delta\theta", 32).move_to(O_A + 0.8 * unit(THETA_C))
        right_marks = VGroup(right_angle(b.P_m, -unit(b.a_m), tangent(b.a_m)),
                             right_angle(b.P_p, -unit(b.a_p), tangent(b.a_p)))
        t_line = tex(r"t_\pm=t\pm\tfrac{\Delta t}{2}", 40).move_to([0, -0.9, 0])

        self.play(FadeOut(copies, guides, speed_line, direction_line, tag_same, tag_dir),
                  *self.caption("Dois instantes próximos"), run_time=0.8)
        # A partícula passa por P₋ e P₊: cada passagem congela posição e velocidade.
        v_m_frozen, v_p_frozen = b.v_m.copy(), b.v_p.copy()
        orbit_to(720 + b.a_m * 180 / PI)
        self.add(b.dots[0], v_m_frozen)
        self.play(FadeIn(p_m_label), FadeIn(t_line), run_time=0.5)
        orbit_to(720 + b.a_p * 180 / PI)
        self.add(b.dots[1], v_p_frozen)
        self.play(FadeIn(p_p_label), FadeOut(particle, v_live, v_label), run_time=0.6)
        self.play(FadeIn(v_m_label, v_p_label), run_time=0.6)
        self.wait(0.4)

        self.play(GrowArrow(b.r_m), GrowArrow(b.r_p), FadeIn(r_m_label, r_p_label), run_time=1.0)
        self.play(Create(b.arc), FadeIn(dth_label), run_time=0.8)
        perp_line = tex(r"\vec v_\pm\perp\vec r_\pm", 40).move_to([0, -1.8, 0])
        perp_line[0][0:2].set_color(CYAN)
        self.play(Create(right_marks), FadeIn(perp_line), run_time=0.9)
        self.wait(0.9)

        # Δr = r₊ − r₋: da ponta de r₋ à ponta de r₊ (corda, sem aproximação de arco).
        dr_label = tex(r"\Delta\vec r", 34, BLUE).next_to(b.dr, LEFT, buff=0.08).shift(DOWN * 0.3)
        dr_line = tex(r"\Delta\vec r=\vec r_+-\vec r_-", 40).move_to([0, -2.7, 0])
        dr_line[0][0:3].set_color(BLUE)
        self.play(GrowArrow(b.dr), run_time=1.0)
        self.play(FadeIn(dr_label), Write(dr_line), run_time=0.9)
        self.wait(1.0)
        self.check_safe_area()

        # ── C. Δv construído na origem comum ─────────────────────────────────
        c = VelocityTriangle(Q_C, DTH_START)
        panel_c = RoundedRectangle(width=4.4, height=3.6, corner_radius=0.2).move_to([0, -2.65, 0])
        panel_c.set_stroke(WHITE, 1.5, 0.2)
        panel_c_title = text("VELOCIDADES · ORIGEM COMUM", 18, opacity=0.6)
        panel_c_title.move_to([0, -1.1, 0])
        self.play(FadeOut(t_line, perp_line, dr_line), *self.caption("Variação do vetor velocidade"),
                  run_time=0.8)
        self.play(Create(panel_c), FadeIn(panel_c_title), run_time=0.8)

        # Translação pura: só shift; módulo e orientação não mudam.
        moving_m, moving_p = b.v_m.copy(), b.v_p.copy()
        self.play(moving_m.animate.shift(Q_C - b.P_m), run_time=1.6)
        self.play(moving_p.animate.shift(Q_C - b.P_p), run_time=1.6)
        c_labels = side_labels(Q_C, DTH_START, r"\vec v_-", r"\vec v_+", 32)
        self.play(FadeIn(c_labels), run_time=0.5)
        dth_c_label = tex(r"\Delta\theta", 30).move_to(Q_C + 0.8 * UP)
        self.play(Create(c.arc), FadeIn(dth_c_label), run_time=0.8)
        self.play(Indicate(VGroup(b.arc, dth_label), color=WHITE),
                  Indicate(VGroup(c.arc, dth_c_label), color=WHITE), run_time=1.2)
        self.wait(0.4)

        tips = VGroup(Dot(c.tip_m, 0.07, color=MAGENTA), Dot(c.tip_p, 0.07, color=MAGENTA))
        self.play(FadeIn(tips, scale=1.6), run_time=0.6)
        self.play(GrowArrow(c.dv), run_time=1.4)  # da ponta de v₋ até a ponta de v₊
        dv_label = tex(r"\Delta\vec v=\vec v_+-\vec v_-", 40).next_to(c.dv, UP, buff=0.18)
        dv_label[0][0:3].set_color(MAGENTA)
        dv_label[0][4:7].set_color(CYAN)
        dv_label[0][8:].set_color(CYAN)
        self.play(Write(dv_label), FadeOut(tips), run_time=1.0)
        self.wait(1.2)

        # Simetria: Δv tem a direção de P (instante central) para O.
        P_c = O_A + R_VIS * unit(THETA_C)
        radius_c = DashedLine(P_c, O_A, dash_length=0.1).set_stroke(WHITE, 2, 0.45)
        center_ring = Circle(radius=0.1, arc_center=P_c).set_stroke(WHITE, 2, 0.7)
        dv_radial = c.dv.copy()
        self.play(Create(radius_c), FadeIn(center_ring), FadeOut(dr_label),
                  dth_label.animate.set_opacity(0.15), run_time=0.8)
        head_dv = tex(r"\Delta\vec v", 44, MAGENTA)
        head_words = display("aponta para o centro")
        head_line = inline([(head_dv, baseline_glyph(head_dv)), (head_words, head_words[-1])], gap=0.2)
        self.play(dv_radial.animate.shift(P_c - c.tip_m),
                  *self.caption("Com instantes simétricos,", head_line), run_time=1.6)
        self.wait(1.6)
        self.check_safe_area()

        # ── D. Triângulos semelhantes: comparação, não o mesmo espaço ─────────
        tri_r = VGroup(b.r_m, b.r_p, b.dr, b.arc, dth_label)
        tri_v = VGroup(moving_m, moving_p, c.dv, c.arc, dth_c_label)
        self.play(
            FadeOut(circle, center, o_label, b.dots, p_m_label, p_p_label, v_m_frozen, v_p_frozen,
                    v_m_label, v_p_label, r_m_label, r_p_label, right_marks, radius_c,
                    center_ring, dv_radial, panel_c, panel_c_title, c_labels, dv_label),
            dth_label.animate.set_opacity(1),
            *self.caption("Triângulos semelhantes"), run_time=1.0)
        self.play(tri_r.animate.shift(O_D - O_A), tri_v.animate.shift(Q_D - Q_C), run_time=1.4)

        panels = VGroup(*(RoundedRectangle(width=4.1, height=3.8, corner_radius=0.2)
                          .set_stroke(WHITE, 1.5, 0.2).move_to([x, 2.0, 0]) for x in (-2.2, 2.2)))
        panel_titles = VGroup(text("POSIÇÃO", 18, opacity=0.6).move_to([-2.2, 3.55, 0]),
                              text("VELOCIDADE", 18, opacity=0.6).move_to([2.2, 3.55, 0]))
        same_shape = text("MESMA FORMA · ESCALAS DIFERENTES", 20, opacity=0.75)
        same_shape.move_to([0, 4.4, 0])
        self.play(Create(panels), FadeIn(panel_titles, same_shape), run_time=1.0)

        d_r = Construction(O_D, DTH_START)
        d_v = VelocityTriangle(Q_D, DTH_START)
        R_labels = VGroup(*(tex("R", 36).move_to(O_D + 1.1 * unit(a) + 0.3 * unit(a + s * PI / 2))
                            for a, s in ((d_r.a_m, -1), (d_r.a_p, 1))))
        dr_mag = tex(r"|\Delta\vec r|", 36, BLUE).next_to(d_r.dr, RIGHT, buff=0.12)
        v_labels = side_labels(Q_D, DTH_START, "v", "v", 36)
        dv_mag = tex(r"|\Delta\vec v|", 36, MAGENTA).next_to(d_v.dv, UP, buff=0.14)

        # 1) mesmo Δθ; 2) R ↔ v; 3) |Δr| ↔ |Δv|; 4) a razão, termo a termo.
        self.play(Indicate(VGroup(tri_r[3], tri_r[4]), color=WHITE),
                  Indicate(VGroup(tri_v[3], tri_v[4]), color=WHITE), run_time=1.2)
        pair_1 = tex(r"R\ \leftrightarrow\ v", 44).move_to([0, -0.45, 0])
        pair_1[0][-1].set_color(CYAN)
        pair_2 = tex(r"|\Delta\vec r|\ \leftrightarrow\ |\Delta\vec v|", 44).move_to([0, -1.35, 0])
        pair_2[0][0:5].set_color(BLUE)
        pair_2[0][6:].set_color(MAGENTA)
        self.play(FadeIn(R_labels, v_labels), run_time=0.6)
        self.play(FadeIn(pair_1), Indicate(VGroup(tri_r[0], tri_r[1], R_labels), color=WHITE),
                  Indicate(VGroup(tri_v[0], tri_v[1], v_labels), color=CYAN), run_time=1.3)
        self.play(FadeIn(dr_mag, dv_mag), run_time=0.6)
        self.play(FadeIn(pair_2), Indicate(VGroup(tri_r[2], dr_mag), color=BLUE),
                  Indicate(VGroup(tri_v[2], dv_mag), color=MAGENTA), run_time=1.3)
        self.wait(0.5)

        ratio = MathTex(r"\frac{|\Delta\vec v|}{v}", "=", r"\frac{|\Delta\vec r|}{R}",
                        font_size=62, color=WHITE).move_to([0, -2.95, 0])
        color_slices(ratio, (0, NUM, MAGENTA), (0, slice(6, 7), CYAN), (2, NUM, BLUE))
        self.play(TransformFromCopy(dv_mag, ratio[0][NUM]), run_time=1.0)
        self.play(FadeIn(ratio[0][5]), TransformFromCopy(v_labels[0], ratio[0][6]), run_time=0.9)
        self.play(FadeIn(ratio[1]), TransformFromCopy(dr_mag, ratio[2][NUM]), run_time=1.0)
        self.play(FadeIn(ratio[2][5]), TransformFromCopy(R_labels[0], ratio[2][6]), run_time=0.9)
        self.remove(*ratio.get_family())
        self.add(ratio)
        self.wait(1.2)

        # Sem tela separada: a razão vira taxa ali mesmo, com os triângulos à vista.
        step_2 = MathTex(r"\frac{|\Delta\vec v|}{\Delta t}", "=", r"\frac{v}{R}",
                         r"\frac{|\Delta\vec r|}{\Delta t}", font_size=56, color=WHITE).move_to(ratio)
        color_slices(step_2, (0, NUM, MAGENTA), (2, slice(0, 1), CYAN), (3, NUM, BLUE))
        self.play(FadeOut(pair_1, pair_2), TransformMatchingShapes(ratio, step_2), run_time=1.6)
        self.wait(1.2)
        self.check_safe_area()

        # ── E. Limite Δt → 0: primeiro a posição, depois a velocidade ─────────
        dth_r, dth_v = ValueTracker(DTH_START), ValueTracker(DTH_START)
        pos_opacity = ValueTracker(1.0)
        e_circle = Circle(radius=R_VIS, arc_center=O_E).set_stroke(BLUE, 3, 0.55)
        e_center = Dot(O_E, 0.06, color=WHITE)
        P_e = O_E + R_VIS * unit(THETA_C)
        e_ring = Circle(radius=0.1, arc_center=P_e).set_stroke(WHITE, 2, 0.7)

        def e_geometry():
            g = Construction(O_E, dth_r.get_value())
            fade = np.clip((dth_r.get_value() - 24 * PI / 180) / (8 * PI / 180), 0, 1)
            labels = VGroup(tex("P_-", 32).next_to(g.P_m, DOWN + RIGHT, buff=0.06),
                            tex("P_+", 32).next_to(g.P_p, RIGHT, buff=0.12).shift(UP * 0.1))
            main = VGroup(g.r_m, g.r_p, g.arc, g.dr, g.dots).set_opacity(pos_opacity.get_value())
            return VGroup(main, labels.set_opacity(fade * pos_opacity.get_value()))

        def e_triangle():
            t = VelocityTriangle(Q_E, dth_v.get_value())
            label = tex(r"|\Delta\vec v|", 30, MAGENTA).move_to(
                Q_E + (L_V * np.cos(dth_v.get_value() / 2) + 0.42) * UP)
            return VGroup(t.v_m, t.v_p, t.arc, t.dv, label)

        e_geo = always_redraw(e_geometry)
        e_dr_label = always_redraw(lambda: tex(r"|\Delta\vec r|", 30, BLUE).set_opacity(
            pos_opacity.get_value()).move_to(P_e + 0.55 * RIGHT + 0.3 * DOWN))
        e_tri = always_redraw(e_triangle)
        e_panel = RoundedRectangle(width=1.95, height=3.0, corner_radius=0.18).move_to([Q_E[0], 1.1, 0])
        e_panel.set_stroke(WHITE, 1.5, 0.2)
        e_panel_title = text("VELOCIDADE", 16, opacity=0.6).move_to([Q_E[0], 2.36, 0])
        dt_label = tex(r"\Delta t\to 0", 40).move_to([O_E[0], -1.35, 0])

        self.play(FadeOut(tri_r, tri_v, panels, panel_titles, same_shape, R_labels, dr_mag,
                          v_labels, dv_mag),
                  step_2.animate.scale(50 / 56).move_to([0, 4.85, 0]),
                  *self.caption("Instantes cada vez", "mais próximos"), run_time=1.2)
        self.play(Create(e_circle), FadeIn(e_center, e_ring, e_geo, e_dr_label), run_time=1.0)

        # Posição: P₋ e P₊ se aproximam; Δr fica alinhado com o vetor velocidade em P.
        self.play(FadeIn(dt_label), dth_r.animate.set_value(DTH_MIN), run_time=3.5)
        v_c = vec(P_e, P_e + L_V * tangent(THETA_C), CYAN)
        v_c_label = tex(r"\vec v", 36, CYAN).next_to(v_c.get_end(), RIGHT, buff=0.12)
        lim_1 = MathTex(r"\frac{|\Delta\vec r|}{\Delta t}", r"\to", r"|\vec v|", "=", "v",
                        font_size=44, color=WHITE).move_to([O_E[0], -2.4, 0])
        color_slices(lim_1, (0, NUM, BLUE), (2, None, CYAN), (4, None, CYAN))
        self.play(GrowArrow(v_c), FadeIn(v_c_label), run_time=0.8)
        self.play(Write(lim_1), Indicate(step_2[3], color=BLUE), run_time=1.2)
        self.wait(1.4)

        # Velocidade: v₋ e v₊ na origem comum; Δv encolhe junto, sempre para o centro.
        lim_2 = MathTex(r"\frac{|\Delta\vec v|}{\Delta t}", r"\to", "a_c", font_size=44,
                        color=WHITE).move_to([Q_E[0], -2.4, 0])
        color_slices(lim_2, (0, NUM, MAGENTA), (2, None, VIOLET))
        self.play(pos_opacity.animate.set_value(0.35), Create(e_panel), FadeIn(e_panel_title, e_tri),
                  run_time=0.9)
        self.play(dth_v.animate.set_value(DTH_MIN), run_time=2.8)
        self.play(Write(lim_2), Indicate(step_2[0], color=MAGENTA), run_time=1.2)
        self.wait(0.8)
        self.check_safe_area()

        # Ponte: duas taxas, duas perguntas.
        note_1 = VGroup(text("posição muda", 22, opacity=0.85),
                        text("→ velocidade", 22, color=CYAN)).arrange(DOWN, buff=0.1)
        note_2 = VGroup(text("velocidade muda", 22, opacity=0.85),
                        text("→ aceleração", 22, color=VIOLET)).arrange(DOWN, buff=0.1)
        note_1.move_to([O_E[0], -3.45, 0])
        note_2.move_to([Q_E[0], -3.45, 0])
        self.play(FadeIn(note_1, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(note_2, shift=UP * 0.1), run_time=0.7)
        self.wait(1.4)
        self.check_safe_area()

        eq_lim = MathTex("a_c", "=", r"\frac{v}{R}", "v", font_size=50, color=WHITE).move_to(step_2)
        color_slices(eq_lim, (0, None, VIOLET), (2, slice(0, 1), CYAN), (3, None, CYAN))
        self.play(FadeOut(step_2[0]), TransformFromCopy(lim_2[2], eq_lim[0]),
                  ReplacementTransform(step_2[1], eq_lim[1]), ReplacementTransform(step_2[2], eq_lim[2]),
                  FadeOut(step_2[3]), TransformFromCopy(lim_1[4], eq_lim[3]), run_time=1.6)
        self.wait(0.5)
        eq_final = MathTex("a_c", "=", r"\frac{v}{R}", "v", "=", r"\frac{v^2}{R}",
                           font_size=50, color=WHITE).move_to(eq_lim)
        color_slices(eq_final, (0, None, VIOLET), (2, slice(0, 1), CYAN), (3, None, CYAN),
                     (5, slice(0, 2), CYAN))
        box = SurroundingRectangle(eq_final[5], buff=0.14, corner_radius=0.08).set_stroke(VIOLET, 3)
        self.play(*(ReplacementTransform(eq_lim[i], eq_final[i]) for i in range(4)), run_time=0.9)
        self.play(Write(eq_final[4:]), run_time=1.0)
        self.play(Create(box), run_time=0.8)
        self.wait(1.2)
        self.check_safe_area()

        # ── F. De volta ao círculo: v tangente, a_c para o centro ─────────────
        final = MathTex("a_c", "=", r"\frac{v^2}{R}", font_size=64, color=WHITE).move_to([0, -2.75, 0])
        color_slices(final, (0, None, VIOLET), (2, slice(0, 2), CYAN))
        final_box = SurroundingRectangle(final, buff=0.24, corner_radius=0.1).set_stroke(VIOLET, 3)
        self.play(FadeOut(e_circle, e_center, e_ring, e_geo, e_dr_label, e_panel, e_panel_title, e_tri,
                          dt_label, v_c, v_c_label, lim_1, lim_2, note_1, note_2, eq_final[1:5]),
                  ReplacementTransform(eq_final[0], final[0]), ReplacementTransform(eq_final[5], final[2]),
                  FadeIn(final[1]), ReplacementTransform(box, final_box),
                  *self.caption("Aceleração centrípeta"), run_time=1.4)

        phi = ValueTracker(20 * PI / 180)

        def f_point():
            return O_F + R_VIS * unit(phi.get_value())

        def f_vectors():
            a, P = phi.get_value(), f_point()
            return VGroup(
                vec(P, P - L_A * unit(a), VIOLET),
                vec(P, P + L_V * tangent(a), CYAN),
                right_angle(P, -unit(a), tangent(a), 0.2),
                tex(r"\vec a_c", 36, VIOLET).move_to(P - 0.62 * L_A * unit(a) - 0.36 * tangent(a)),
                tex(r"\vec v", 36, CYAN).move_to(P + (L_V + 0.3) * tangent(a) + 0.12 * unit(a)),
                orb(P),
            )

        f_circle = Circle(radius=R_VIS, arc_center=O_F).set_stroke(BLUE, 3, 0.55)
        f_center = Dot(O_F, 0.07, color=WHITE)
        f_o_label = tex("O", 32).set_opacity(0.8).next_to(f_center, DOWN + LEFT, buff=0.08)
        f_vecs = always_redraw(f_vectors)
        perp = tex(r"\vec v\perp\vec a_c", 46).move_to([0, -0.95, 0])
        perp[0][0:2].set_color(CYAN)
        perp[0][3:].set_color(VIOLET)
        self.play(Create(f_circle), FadeIn(f_center, f_o_label, f_vecs), run_time=1.2)
        self.play(FadeIn(perp), run_time=0.8)
        self.play(phi.animate.set_value(20 * PI / 180 + 2 * PI), run_time=6.0, rate_func=linear)
        self.play(Indicate(perp), Indicate(final[0], color=VIOLET), run_time=1.2)
        # Volta à pergunta inicial.
        self.play(phi.animate(rate_func=linear).set_value(20 * PI / 180 + 2 * PI + 70 * PI / 180),
                  *self.caption("O módulo não muda;", "o vetor muda."), run_time=1.2 * 70 / 60)
        self.check_safe_area()
        self.wait(2.2)
