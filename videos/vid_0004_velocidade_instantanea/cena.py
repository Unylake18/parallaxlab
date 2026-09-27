"""Derivada como velocidade instantânea; preview visual silencioso.

Modelo: x(t) = ½at², a = 2 m/s², x(0) = 0, v(0) = 0; instante t0 = 2 s.
Com os eixos já em segundos e metros, a curva é calculada como x = t².
A velocidade média em [t0, t0 + Δt] vale at0 + ½aΔt = 4 + Δt; Δt nunca
chega a zero no quociente: para em DT_MIN e a secante vira a tangente exata.

Cores: ciano = taxa instantânea (tangente, seta, v); azul = taxa média
(secante, Q, v̄); magenta = Δx; violeta = Δt e halos de apoio.
"""

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, Axes, Circle, Create, Dot, FadeIn, FadeOut,
    ImageMobject, Indicate, Line, MathTex, Polygon, ReplacementTransform, Scene,
    TransformMatchingShapes, TransformMatchingTex, VGroup, VMobject, ValueTracker,
    Text, Write, always_redraw, linear, smooth,
)

from pathlib import Path

from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH

AUDIO_PATH = Path(__file__).parent / "audio" / "narracao_montagem.wav"  # preparar_audio.py
ACCEL = 2.0          # m/s²
T0 = 2.0             # s
DT_START = 2.0       # s
DT_MIN = 0.02        # s; menor Δt usado no quociente
TANGENT = PRIMARY_COLOR   # ciano: taxa instantânea
SECANT = "#267BFF"        # azul elétrico: taxa média
DX_COLOR = "#EA63FF"      # magenta: Δx
DT_COLOR = "#745CFF"      # violeta: Δt
AXIS_COLOR = "#9AA1C7"
# Lido por videos/montar_legendado.py --color-module: mesma lógica de cor da cena.
SUBTITLE_TERM_COLORS = {
    "velocidade média": SECANT,
    "taxa média": SECANT,
    "reta secante": SECANT,
    "secante": SECANT,
    "velocidade instantânea": TANGENT,
    "taxa instantânea": TANGENT,
    "tangente": TANGENT,
    "derivada": TANGENT,
    "4 m/s": TANGENT,
    "variação da posição": DX_COLOR,
    "variação de posição": DX_COLOR,
    "incremento de tempo": DT_COLOR,
    "intervalo de tempo": DT_COLOR,
}
MUTED = "#8C93B8"
TRACK_Y = 5.7
TRACK_X = (-3.7, 3.7)     # 0 m → 18 m
SAFE_BOTTOM = -4.6        # abaixo disso: faixa reservada a legendas
LINE_1, LINE_2, LINE_3 = -2.62, -3.45, -4.18   # linhas da faixa de fórmulas


def position(t):
    return 0.5 * ACCEL * t ** 2


def mean_velocity(dt):
    assert dt > 0, "Δt não pode ser zero no quociente"
    return (position(T0 + dt) - position(T0)) / dt


def br(value, digits=2):
    return f"{value:.{digits}f}".replace(".", "{,}")


def tex(*parts, size=40, y=None):
    mob = MathTex(*parts, font_size=size, color=TEXT_COLOR)
    return mob if y is None else mob.move_to([0, y, 0])


def glow(mob, color, width=14, opacity=0.2):
    """Traço com halo: cópia larga e translúcida por baixo do traço principal."""
    halo = mob.copy().set_stroke(color=color, width=width, opacity=opacity)
    return VGroup(halo, mob)


def halo_dot(point, core, ring, radius=0.09):
    return VGroup(
        Dot(point, radius=radius * 3.2, color=ring, fill_opacity=0.12),
        Dot(point, radius=radius * 2.0, color=ring, fill_opacity=0.25),
        Dot(point, radius=radius, color=core),
    )


def orb():
    """Partícula: núcleo branco, halo ciano e aura violeta."""
    return VGroup(
        Dot(radius=0.46, color=DT_COLOR, fill_opacity=0.10),
        Dot(radius=0.34, color=TANGENT, fill_opacity=0.18),
        Dot(radius=0.25, color=TANGENT, fill_opacity=0.35),
        Dot(radius=0.17, color=TEXT_COLOR),
    )


class VelocidadeInstantanea004(Scene):
    def until(self, seconds):
        remaining = seconds - self.time
        if remaining > 1e-6:
            self.wait(remaining)

    def track_point(self, x):
        return [np.interp(x, [0, 18], TRACK_X), TRACK_Y, 0]

    def check_safe_area(self):
        bottom = min(m.get_bottom()[1] for m in self.mobjects
                     if isinstance(m, VMobject) and len(m.get_all_points()))
        assert bottom > SAFE_BOTTOM, f"conteúdo invade a faixa inferior: {bottom:.2f}"

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        watermark = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(watermark.to_corner(UP + RIGHT, buff=0.28))

        # Topo limpo: só o modelo, discreto.
        model = tex(r"x(t)=\tfrac12 a t^2", r",\quad", r"a=2\,\mathrm{m/s^2}", size=36, y=7.05)

        # Fenômeno: pista luminosa com poucas marcas.
        track_line = Line(self.track_point(0), self.track_point(18), stroke_width=6)
        track_line.set_color([TANGENT, DT_COLOR])
        track = glow(track_line, DT_COLOR, width=22, opacity=0.14)
        ticks = VGroup(*(Line(UP * 0.12, DOWN * 0.12, color=AXIS_COLOR, stroke_width=3)
                         .move_to(self.track_point(x)) for x in (0, 4, 8, 12, 16)))
        tick_labels = VGroup(*(tex(label, size=30).set_color(AXIS_COLOR)
                               .next_to(self.track_point(x), DOWN, buff=0.28)
                               for x, label in ((0, "0"), (4, r"4\,\mathrm{m}"))))
        physical = VGroup(track, ticks, tick_labels)

        # Gráfico posição × tempo.
        axes = Axes(x_range=[0, 4.2, 1], y_range=[0, 18, 4], x_length=7.0, y_length=6.0,
                    tips=True, axis_config={"color": AXIS_COLOR, "stroke_width": 2,
                                            "include_numbers": True, "font_size": 28},
                    ).move_to([0.25, 1.45, 0])
        t_label = tex(r"t\,(\mathrm{s})", size=30).next_to(axes.x_axis.get_end(), DOWN, buff=0.25)
        x_label = tex(r"x\,(\mathrm{m})", size=30).next_to(axes.y_axis.get_end(), RIGHT, buff=0.15)

        def curve(t_start, t_end, core=TEXT_COLOR, width=4, opacity=1.0):
            main = axes.plot(position, x_range=[t_start, max(t_end, t_start + 1e-3)],
                             stroke_width=width).set_stroke(color=core, opacity=opacity)
            halo = main.copy().set_stroke(width=16, opacity=0.2 * opacity)
            halo.set_color([TANGENT, DT_COLOR])
            return VGroup(halo, main)

        # Tempos da cena seguem a narração (segundos do WAV); comentários citam a fala.
        self.add_sound(str(AUDIO_PATH))
        self.play(FadeIn(physical, axes, t_label, x_label), run_time=1)
        self.until(1.2)

        # Gancho: um único parâmetro de tempo move a partícula e o ponto do gráfico.
        clock = ValueTracker(0)
        particle = orb().add_updater(
            lambda m: m.move_to(self.track_point(position(clock.get_value()))))
        trail = always_redraw(lambda: Line(
            self.track_point(0), self.track_point(max(position(clock.get_value()), 1e-3)),
            color=TANGENT, stroke_width=10, stroke_opacity=0.45))
        graph_dot = always_redraw(lambda: halo_dot(
            axes.c2p(clock.get_value(), position(clock.get_value())), TEXT_COLOR, TANGENT))
        traced = always_redraw(lambda: curve(0, clock.get_value()))
        clock_label = always_redraw(lambda: tex(
            rf"t={br(clock.get_value(), 1)}\,\mathrm{{s}}", size=32).move_to([2.9, 5.2, 0]))
        self.add(trail, traced, particle, graph_dot, clock_label)
        # O relógio avança em ritmo real: t = 0 → 2 s entre 1,2 s e 12,6 s da cena.
        run_clock = lambda t_end, value, *extra: self.play(
            clock.animate.set_value(value), *extra, run_time=t_end - self.time, rate_func=linear)
        run_clock(4.4, T0 * (4.4 - 1.2) / 11.4)
        run_clock(5.6, T0 * (5.6 - 1.2) / 11.4, Write(model))   # "Neste movimento…"
        run_clock(12.6, T0)                                      # "…instante de dois segundos"
        for mob in (particle, graph_dot, traced, clock_label, trail):
            mob.clear_updaters()

        P = axes.c2p(T0, position(T0))
        p_label = tex(r"P=(2\,\mathrm{s},\ 4\,\mathrm{m})", size=30).next_to(
            P, LEFT, buff=0.2).shift(UP * 0.45)
        rest = curve(T0, 4.2, core=MUTED, width=3, opacity=0.8)
        t0_mark = tex(r"t_0", size=30).next_to(particle, UP, buff=0.1)
        self.until(13.5)                                         # "…a quatro metros da origem"
        self.play(FadeIn(p_label, t0_mark), Create(rest), FadeOut(clock_label),
                  Indicate(graph_dot, color=TEXT_COLOR), run_time=1.2)
        self.bring_to_front(graph_dot)
        self.until(16.6)

        # Um único Δt controla Q, a secante, Δt/Δx (gráfico e pista), leituras e amostra.
        dt = ValueTracker(DT_START)

        def q_point():
            t = T0 + dt.get_value()
            return axes.c2p(t, position(t))

        def corner():
            return axes.c2p(T0 + dt.get_value(), position(T0))

        def fade_small(mob, gone=0.0, full=0.35):
            """Some com o rótulo antes que Q e P, ou as duas amostras, se sobreponham."""
            return mob.set_opacity(np.clip((dt.get_value() - gone) / (full - gone), 0, 1))

        def line_with_slope(slope, color, width, halo=14):
            t_min = max(0, T0 - position(T0) / slope)
            t_max = min(4.2, T0 + (18 - position(T0)) / slope)
            line = lambda t: axes.c2p(t, position(T0) + slope * (t - T0))
            return glow(Line(line(t_min), line(t_max), color=color, stroke_width=width),
                        color, width=halo, opacity=0.22)

        triangle = always_redraw(lambda: Polygon(P, corner(), q_point(), stroke_width=0,
                                                 fill_color=SECANT, fill_opacity=0.13))
        secant = always_redraw(lambda: line_with_slope(
            mean_velocity(dt.get_value()), SECANT, 4))
        dt_line = always_redraw(lambda: Line(P, corner(), color=DT_COLOR, stroke_width=5))
        dx_line = always_redraw(lambda: Line(corner(), q_point(), color=DX_COLOR, stroke_width=5))
        dt_tag = always_redraw(lambda: fade_small(tex(r"\Delta t", size=32).set_color(DT_COLOR)
                                                  .next_to(dt_line, DOWN, buff=0.12)))
        dx_tag = always_redraw(lambda: fade_small(tex(r"\Delta x", size=32).set_color(DX_COLOR)
                                                  .next_to(dx_line, RIGHT, buff=0.12)))
        q_dot = always_redraw(lambda: VGroup(
            Circle(radius=0.2, color=SECANT, stroke_width=3).move_to(q_point()),
            Dot(q_point(), radius=0.085, color=SECANT)))
        q_label = always_redraw(lambda: fade_small(
            tex("Q", size=32).set_color(SECANT).next_to(q_point(), RIGHT, buff=0.24)))
        # Na pista: o mesmo Δx é a distância entre as duas amostras do intervalo.
        ghost_x = lambda: self.track_point(position(T0 + dt.get_value()))
        track_dx = always_redraw(lambda: Line(particle.get_center(), ghost_x(),
                                              color=DX_COLOR, stroke_width=9, stroke_opacity=0.8))
        ghost = always_redraw(lambda: VGroup(
            Dot(ghost_x(), radius=0.3, color=SECANT, fill_opacity=0.15),
            Circle(radius=0.18, color=SECANT, stroke_width=4).move_to(ghost_x())))
        ghost_tag = always_redraw(lambda: fade_small(
            tex(r"t_0+\Delta t", size=28).set_color(SECANT).next_to(ghost, UP, buff=0.02),
            gone=0.3, full=0.7))
        track_dx_tag = always_redraw(lambda: fade_small(
            tex(r"\Delta x", size=28).set_color(DX_COLOR).next_to(track_dx, UP, buff=0.22),
            gone=0.5, full=1.0))

        vbar = tex(r"\bar v", "=", r"\frac{", r"\Delta x", "}{", r"\Delta t", "}", y=LINE_1)
        vbar[0].set_color(SECANT)
        vbar[3].set_color(DX_COLOR)
        vbar[5].set_color(DT_COLOR)
        # "Agora comparamos essa posição com outra, um pequeno incremento de tempo depois."
        self.play(FadeIn(q_dot, q_label, ghost, ghost_tag), run_time=1)
        self.until(19.4)
        self.add(dt_line)
        self.bring_to_front(graph_dot, particle, q_dot)
        self.play(FadeIn(dt_line, dt_tag), run_time=0.8)
        self.until(22.2)                                         # "…temos a velocidade média:"
        self.add(dx_line, track_dx)
        self.bring_to_front(graph_dot, particle, q_dot, ghost)
        self.play(FadeIn(dx_line, dx_tag, track_dx, track_dx_tag), run_time=0.8)
        self.until(25.9)                                         # "a variação da posição dividida…"
        self.play(Write(vbar), run_time=1)
        self.until(29.9)                                         # "…a inclinação da reta secante."
        self.add(triangle, secant)
        self.bring_to_front(dt_line, dx_line, graph_dot, q_dot)
        self.play(FadeIn(triangle, secant), run_time=1)
        self.until(33.9)

        # Derivação passo a passo, com Q parado em Δt = 2 s.
        dx_def = tex(r"\Delta x", "=", r"x(t_0+\Delta t)", "-", r"x(t_0)", y=LINE_2)
        dx_def[0].set_color(DX_COLOR)
        # "Então, para encontrar essa variação de posição, fazemos a posição final menos…"
        self.play(Indicate(dx_line, color=DX_COLOR), Indicate(track_dx, color=DX_COLOR),
                  Indicate(vbar[3], color=DX_COLOR), run_time=1.2)
        self.until(37.2)
        self.play(Write(dx_def), run_time=1.2)
        self.until(40.6)

        # A lei do movimento desce do topo como fonte da substituição.
        source = model[0].copy()
        self.play(source.animate.scale(1.05).move_to([0, LINE_3, 0]).set_color(DT_COLOR),
                  Indicate(model[0], color=DT_COLOR), run_time=0.9)
        self.until(41.5)                                         # "Substituímos a função…"

        dx_sub = tex(r"\Delta x", "=", r"\tfrac12 a(t_0+\Delta t)^2", "-", r"\tfrac12 a t_0^2",
                     y=LINE_2)
        dx_sub[0].set_color(DX_COLOR)
        self.play(TransformMatchingShapes(dx_def, dx_sub), run_time=1.2)
        self.until(44.0)                                         # "…desenvolvemos o quadrado…"

        dx_open = tex(r"\Delta x", "=", r"\tfrac12 a\left[(t_0+\Delta t)^2-t_0^2\right]",
                      y=LINE_2)
        dx_open[0].set_color(DX_COLOR)
        self.play(TransformMatchingShapes(dx_sub, dx_open), FadeOut(source), run_time=1.2)
        self.until(46.0)                                         # "…e simplificamos."

        dx_expanded = tex(r"\Delta x", "=", r"a t_0\,\Delta t", "+", r"\tfrac12 a(\Delta t)^2",
                          y=LINE_2)
        dx_expanded[0].set_color(DX_COLOR)
        self.play(TransformMatchingShapes(dx_open, dx_expanded), run_time=1.3)
        self.until(47.5)                                         # "Depois, dividimos pelo intervalo…"

        vbar_general = tex(r"\bar v", "=", r"a t_0", "+", r"\tfrac12 a\,\Delta t", y=LINE_1)
        vbar_numeric = tex(r"\bar v", "=", r"4\,\mathrm{m/s}", "+",
                           r"(1\,\mathrm{m/s^2})\,\Delta t", y=LINE_1)
        for mob in (vbar_general, vbar_numeric):
            mob[0].set_color(SECANT)
        self.play(TransformMatchingTex(vbar, vbar_general), run_time=1.2)
        self.until(50.5)                                         # "…expressão da velocidade média."
        self.play(TransformMatchingTex(vbar_general, vbar_numeric), run_time=1.2)
        self.check_safe_area()
        self.until(52.7)

        # Momento central: Δt diminui; o mesmo Q e a mesma secante giram, e v̄ → 4 m/s.
        def live_tex():
            mob = tex(rf"\Delta t={br(dt.get_value())}\,\mathrm{{s}}", r"\qquad",
                      rf"\bar v={br(mean_velocity(dt.get_value()))}\,\mathrm{{m/s}}",
                      size=34, y=LINE_2)
            mob[0].set_color(DT_COLOR)
            return mob

        live = always_redraw(live_tex)
        # O termo em Δt perde destaque à medida que Δt encolhe.
        vbar_numeric.add_updater(lambda m: VGroup(m[3], m[4]).set_opacity(
            np.clip(dt.get_value() / 1.2, 0.18, 1)))

        def chain_tex(values):
            return tex(r"\bar v:\ ", r"\;\to\;".join(values[-3:]), r"\,\mathrm{m/s}",
                       size=34, y=LINE_3)

        samples = ["6"]
        chain = chain_tex(samples)
        self.play(FadeOut(dx_expanded), FadeIn(live, chain), run_time=0.6)
        for target, label, run, hold in ((1.0, "5", 2.4, 0.6), (0.5, r"4{,}5", 2.2, 0.5),
                                         (0.2, r"4{,}2", 2.2, 0.5),
                                         (DT_MIN, r"4{,}02", 1.8, 0.0)):
            self.play(dt.animate.set_value(target), run_time=run, rate_func=smooth)
            samples.append(label)
            # Troca por fade: evita algarismos deslizando entre valores.
            new_chain = chain_tex(samples)
            self.play(FadeOut(chain), run_time=0.2)
            self.play(FadeIn(new_chain), run_time=0.3)
            chain = new_chain
            if hold:
                self.wait(hold)
        self.check_safe_area()
        self.until(65.6)                                         # "No limite, quando… tende a zero"

        # Secante quase tangente → tangente exata (inclinação 4 m/s).
        for mob in (triangle, secant, q_dot, q_label, dt_line, dx_line, dt_tag, dx_tag, ghost,
                    ghost_tag, track_dx, track_dx_tag, live, vbar_numeric):
            mob.clear_updaters()
        tangent = line_with_slope(ACCEL * T0, TANGENT, 6, halo=20)
        vbar_limit = tex(r"\Delta t\to0", r"\;\Rightarrow\;", r"\bar v", r"\to",
                         r"4\,\mathrm{m/s}", y=LINE_1)
        vbar_limit[0].set_color(DT_COLOR)
        vbar_limit[2].set_color(SECANT)
        vbar_limit[4].set_color(TANGENT)
        samples.append(r"\mathbf{4}")
        final_chain = chain_tex(samples)
        final_chain[1][-1].set_color(TANGENT)
        # Os números saem primeiro; a geometria faz a passagem sozinha; o estado final entra.
        self.play(FadeOut(vbar_numeric, chain, live, q_label, dt_line, dx_line, dt_tag, dx_tag,
                          ghost, ghost_tag, track_dx, track_dx_tag, triangle), run_time=0.4)
        self.play(ReplacementTransform(secant, tangent), FadeOut(q_dot), run_time=1.4)
        self.bring_to_front(graph_dot)
        self.play(FadeIn(vbar_limit, final_chain), run_time=0.5)
        chain = final_chain
        self.until(68.5)                                         # "…a taxa média tende à instantânea"

        # O limite em Δt (não em t): t0 fica fixo, só o intervalo encolhe.
        MAIN_Y, VALUE_Y = -2.85, -3.95
        lim_parts = (r"\lim_{\Delta t\to 0}", r"\frac{\Delta x}{\Delta t}", "=", r"\frac{dx}{dt}")
        limit = tex(*lim_parts, size=42, y=MAIN_Y)
        limit_v = tex(*lim_parts, "=", r"v(t)", size=42, y=MAIN_Y)
        for mob in (limit, limit_v):
            mob[0].set_color(DT_COLOR)
            mob[1].set_color(SECANT)
            mob[3].set_color(TANGENT)
        limit_v[5].set_color(TANGENT)
        self.play(FadeOut(chain), ReplacementTransform(vbar_limit, limit), run_time=1.2)
        self.until(71.2)                                         # "a derivada da posição…"
        self.play(Indicate(limit[3], color=TANGENT), run_time=1)
        self.until(74.4)                                         # "…é justamente a velocidade…"
        self.play(TransformMatchingTex(limit, limit_v), run_time=1)
        self.until(78.4)                                         # "Derivando a função da posição,"

        # Aplicação: v(t) = d/dt(½at²) → at → v(2 s) = 4 m/s.
        applied = tex(r"v(t)", "=", r"\frac{d}{dt}", r"\left(\tfrac12 a t^2\right)", size=42,
                      y=VALUE_Y)
        result = tex(r"v(t)", "=", r"a t", size=42, y=VALUE_Y)
        at_t0 = tex(r"v(2\,\mathrm{s})", "=", r"4\,\mathrm{m/s}", size=44, y=VALUE_Y)
        for mob in (applied, result, at_t0):
            mob[0].set_color(TANGENT)
        applied[3].set_color(DT_COLOR)
        at_t0[2].set_color(TANGENT)
        self.play(Write(applied), run_time=1.1)
        self.until(80.5)                                         # "…aceleração vezes tempo."
        self.play(TransformMatchingTex(applied, result), run_time=1.2)
        self.until(83.0)                                         # "Portanto, em dois segundos…"

        arrow_core = Arrow(particle.get_center(), particle.get_center() + RIGHT * 2.3,
                           buff=0.26, color=TANGENT, stroke_width=10,
                           max_tip_length_to_length_ratio=0.28)
        arrow = VGroup(arrow_core.copy().set_stroke(width=24, opacity=0.2)
                       .set_fill(opacity=0.2), arrow_core)
        # Abaixo da seta: sobre a pista, ciano sobre ciano ficaria ilegível.
        arrow_tag = tex(r"v=4\,\mathrm{m/s}", size=30).set_color(TANGENT).next_to(
            arrow_core, DOWN, buff=0.18).shift(RIGHT * 0.35)
        self.play(ReplacementTransform(result, at_t0), run_time=0.8)
        self.play(Create(arrow), FadeIn(arrow_tag), FadeOut(t0_mark),
                  Indicate(tangent, color=TANGENT), run_time=1.2)
        self.check_safe_area()
        self.until(88.3)                                         # "Ou seja, a velocidade do objeto"

        # Síntese: a seta do movimento e a inclinação da tangente são a mesma derivada.
        self.play(Indicate(VGroup(arrow, arrow_tag), color=TANGENT), run_time=1.2)
        self.until(90.8)                                         # "…e a inclinação da tangente"
        self.play(Indicate(tangent, color=TANGENT), run_time=1.2)
        self.until(93.5)                                         # "…a mesma taxa instantânea…"
        self.play(Indicate(at_t0, color=TANGENT), run_time=1.2)
        # Momento 1: a conclusão respira, completa, antes do CTA.
        self.until(97.9)

        # Momento 2: sai a matemática; pista, seta e gráfico ficam como fundo do CTA.
        # CTA no estilo do vid_0003: Text com a fonte padrão do Manim.
        self.play(FadeOut(limit_v, at_t0, arrow_tag), run_time=0.5)
        cta = VGroup(
            Text("Segue o Parallax Lab", font_size=30, color=TEXT_COLOR),
            Text("@labparallax", font_size=34, color=TANGENT),
        ).arrange(DOWN, buff=0.22).move_to([0, (MAIN_Y + VALUE_Y) / 2, 0])
        self.play(FadeIn(cta, shift=UP * 0.1), watermark.animate.set_opacity(0.75),
                  run_time=0.8)
        self.play(watermark.animate.set_opacity(0.45), run_time=0.8)
        self.check_safe_area()
        self.until(101.5)   # fala termina em "Segue o Parallax Lab" (99,93 s); @ só na tela
