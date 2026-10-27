"""VID21 — cena sincronizada à narração fornecida, inteiramente em 2D.

Preview: uv run python -m manim -r 540,960 --fps 15 \
    videos/vid_0021_ciclo_termodinamico/cena.py CicloTermodinamico021
Q_CA = -30 P0 V0 é apenas referência documental de QA, não etapa da cena.
"""

from pathlib import Path
import sys
import json

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config import (
    BACKGROUND_COLOR, TEXT_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, WATERMARK_PATH,
)
from template.fonts import screen_text

UNIT = Path(__file__).resolve().parent
config.media_dir = str(UNIT / ("media_particulas_final" if config.pixel_height >= 1920 else "media_particulas_preview"))
config.max_files_cached = 400
config.background_color = BACKGROUND_COLOR

CYAN = PRIMARY_COLOR
VIOLET = SECONDARY_COLOR
BLUE = "#267BFF"
MAGENTA = "#EA63FF"
MUTED = "#8492AE"


class CicloTermodinamico021(Scene):
    """Gráfico, pistão e álgebra compartilham a mesma gramática de grandezas."""

    def words(self, content, y, size=28, color=TEXT_COLOR, width=7.7):
        obj = screen_text(content, font_size=size, color=color,
                          oversample=2 if size >= 25 else 4)
        if obj.width > width:
            obj.scale_to_fit_width(width)
        return obj.move_to([0, y, 0])

    def math(self, tex, y=-1.5, size=43, color=TEXT_COLOR, width=7.6):
        # Isolar símbolos preserva operadores e números neutros. A Primeira Lei
        # combina três grandezas distintas mesmo quando os termos se movem.
        neutral = MUTED if color == MUTED else TEXT_COLOR
        obj = MathTex(tex, font_size=size, color=neutral,
                      substrings_to_isolate=[r"\Delta U", "Q", "W", "U", "T", r"A_{\triangle}"])
        for token, ink in [(r"\Delta U", VIOLET), ("U", VIOLET), ("T", VIOLET),
                           ("W", CYAN), ("Q", MAGENTA), (r"A_{\triangle}", CYAN)]:
            obj.set_color_by_tex(token, ink, substring=False)
        if obj.width > width:
            obj.scale_to_fit_width(width)
        return obj.move_to([0, y, 0])

    def equation_change(self, old, tex, y=None, size=43, color=TEXT_COLOR):
        new = self.math(tex, old.get_y() if y is None else y, size, color)
        # Strings estabilizadas; matching só para correspondências reais.
        self.play(TransformMatchingTex(old, new), run_time=1.3)
        return new

    def finish_block(self, until):
        remaining = until - self.time
        if remaining < -0.1:
            raise RuntimeError(f"Bloco excedeu o marco {until}s: {self.time:.2f}s")
        if remaining > 0:
            self.wait(remaining)

    def cue(self, name, lead=0):
        target = self.cues[name] - lead
        lag = self.time - target
        if lag > 0.55:
            raise RuntimeError(f"Âncora {name} atrasada {lag:.3f}s (tempo {self.time:.3f})")
        if lag < 0:
            self.wait(-lag)
        self.events.append(dict(cue=name, target=target, actual=self.time,
                                lag=round(self.time-target, 4)))

    def heading(self, title, subtitle=None):
        new = self.words(title, 6.35, 34)
        animations = [FadeOut(self.title), FadeIn(new)]
        if self.subtitle is not None:
            animations.append(FadeOut(self.subtitle))
        new_sub = self.words(subtitle, 5.55, 23, MUTED) if subtitle else None
        if new_sub is not None:
            animations.append(FadeIn(new_sub))
        self.play(*animations, run_time=0.7)
        self.title, self.subtitle = new, new_sub

    def graph(self):
        self.axes = Axes(
            x_range=[0, 4.7, 1], y_range=[0, 4.7, 1],
            x_length=4.7, y_length=4.7, tips=True,
            axis_config={"color": BLUE, "stroke_width": 2, "include_ticks": False,
                         "tip_width": 0.13, "tip_height": 0.16},
        ).shift([-0.25, 2.7, 0])
        self.pt = lambda v, p: self.axes.c2p(v, p)
        self.a, self.b, self.c = self.pt(1, 1), self.pt(4, 1), self.pt(4, 4)
        symbols = VGroup(
            MathTex("V", font_size=32).next_to(self.axes.x_axis.get_end(), RIGHT, buff=0.16),
            MathTex("P", font_size=32).next_to(self.axes.y_axis.get_end(), LEFT, buff=0.16),
        )
        ticks = VGroup()
        for v, text in [(1, r"V_0"), (4, r"4V_0")]:
            ticks.add(Line(self.pt(v, 0)+0.06*UP, self.pt(v, 0)+0.06*DOWN, color=MUTED))
            ticks.add(MathTex(text, font_size=28).next_to(self.pt(v, 0), DOWN, buff=0.15))
        for p, text in [(1, r"P_0"), (4, r"4P_0")]:
            ticks.add(Line(self.pt(0, p)+0.06*LEFT, self.pt(0, p)+0.06*RIGHT, color=MUTED))
            ticks.add(MathTex(text, font_size=28).next_to(self.pt(0, p), LEFT, buff=0.16))
        self.grid = VGroup(self.axes, symbols, ticks)
        self.ab = Line(self.a, self.b, color=BLUE, stroke_width=5)
        self.bc = Line(self.b, self.c, color=BLUE, stroke_width=5)
        self.ca = Line(self.c, self.a, color=BLUE, stroke_width=5)
        self.paths = VGroup(self.ab, self.bc, self.ca)
        self.dots = VGroup(*[Dot(p, radius=0.07, color=TEXT_COLOR) for p in [self.a, self.b, self.c]])
        self.labels = VGroup(
            MathTex("A", font_size=31).next_to(self.a, UL, buff=0.12),
            MathTex("B", font_size=31).next_to(self.b, RIGHT, buff=0.14),
            MathTex("C", font_size=31).next_to(self.c, RIGHT, buff=0.14),
        )
        self.arrows = VGroup(
            self.direction(self.a, self.b), self.direction(self.b, self.c), self.direction(self.c, self.a),
        )
        self.marker = Dot(self.a, radius=0.12, color=CYAN).set_z_index(8)

    def direction(self, start, end, color=BLUE):
        middle = (start + end) / 2
        unit = (end - start) / np.linalg.norm(end-start)
        return Arrow(middle-0.25*unit, middle+0.25*unit, buff=0,
                     stroke_width=4, color=color, max_tip_length_to_length_ratio=0.4)

    def focus(self, segment, point):
        self.play(
            *[path.animate.set_color(BLUE)
              .set_opacity(1 if path is segment else 0.25) for path in self.paths],
            *[arrow.animate.set_opacity(1 if i == list(self.paths).index(segment) else 0.22)
              for i, arrow in enumerate(self.arrows)],
            self.marker.animate.move_to(point), run_time=0.8,
        )

    def sync_points(self):
        """Atualiza coordenadas após reorganizar o gráfico existente."""
        self.a, self.b, self.c = self.pt(1, 1), self.pt(4, 1), self.pt(4, 4)

    def state_readout(self, volume, pressure, temperature, center=(2.55,0.34),
                      bar_width=1.3, size=24):
        """Barras qualitativas: mesma posição e escala ao longo de cada ciclo.

        A escala visual é comprimida para manter o estado A perceptível;
        não representa velocidade molecular nem introduz uma nova relação.
        """
        x, y = center
        labels, outlines, fills = VGroup(), VGroup(), VGroup()
        for index, (symbol, tracker, maximum) in enumerate([
            (r"V_0",volume,4), (r"P_0",pressure,4), (r"T_A",temperature,16),
        ]):
            row_y = y + (1-index)*0.48
            label_x = x+0.35-bar_width/2-0.7
            labels.add(MathTex(symbol,font_size=size,color=TEXT_COLOR)
                       .move_to([label_x,row_y,0]))
            outline = RoundedRectangle(width=bar_width,height=0.18,corner_radius=0.05,
                                       color=MUTED,stroke_width=1.1).move_to([x+0.35,row_y,0])
            outlines.add(outline)
            left = outline.get_left()[0]+0.04
            fills.add(always_redraw(lambda tracker=tracker,maximum=maximum,left=left,row_y=row_y:
                Rectangle(width=0.12+(bar_width-0.22)*np.log(max(1,tracker.get_value()))/np.log(maximum),
                          height=0.1,stroke_width=0,fill_color=TEXT_COLOR,fill_opacity=0.85)
                .align_to([left,row_y,0],LEFT).set_y(row_y)))
        panel = VGroup(labels,outlines,fills)
        panel.state_labels, panel.state_fills, panel.label_size = labels, fills, size
        return panel

    def state_trend(self, panel, process):
        trends = {
            "AB": [r"V\uparrow",r"P\,\mathrm{const.}",r"T\uparrow"],
            "BC": [r"V\,\mathrm{const.}",r"P\uparrow",r"T\uparrow"],
            "CA": [r"V\downarrow",r"P\downarrow",r"T\downarrow"],
        }[process]
        animations = []
        for label,tex in zip(panel.state_labels,trends):
            ink = MUTED if "const." in tex else TEXT_COLOR
            target = MathTex(tex,font_size=panel.label_size,color=ink).move_to(label)
            animations.append(Transform(label,target))
        self.play(*animations,run_time=0.35)

    @staticmethod
    def gas_opacity(pressure, temperature):
        # Intensidade apenas qualitativa: o gás continua visível no estado A.
        return 0.16+0.10*np.log(max(1,temperature.get_value()))/np.log(16)+0.08*(pressure.get_value()-1)/3

    def gas_particles(self, gas, temperature, count=36):
        """Modelo molecular qualitativo, com N fixo e rapidez proporcional a sqrt(T).

        O domínio acompanha o volume do gás. Coordenadas refletidas mantêm
        cada centro dentro das paredes e abaixo do pistão, inclusive durante
        compressão. A mudança do domínio transporta as posições relativas;
        não é uma simulação quantitativa de colisões com parede móvel.
        Não há força intermolecular ou associação de calor a uma substância.
        """
        rng = np.random.default_rng(2107)
        phase = rng.uniform(0, 1, (count, 2))
        angles = rng.uniform(0, TAU, count)
        directions = np.column_stack((np.cos(angles), np.sin(angles)))
        dots = VGroup(*[Dot(radius=0.027, color="#B59AFF", fill_opacity=0.95,
                           stroke_width=0) for _ in range(count)])

        def advance(cloud, dt):
            margin = cloud[0].width / 2 + 0.018
            # O topo do preenchimento coincide com o centro da barra do
            # pistão. Rebatemos na face inferior, inclusive na abertura escalada.
            piston_half_height = 0.08 * cloud[0].width / 0.054
            size = np.maximum([gas.width-2*margin,
                               gas.height-2*margin-piston_half_height], 0.01)
            speed = 0.45 * np.sqrt(max(1, temperature.get_value()))
            phase[:] += directions * speed * dt / size
            # Onda triangular: reflexão especular sem atravessar os limites.
            positions = 1 - np.abs(np.mod(phase, 2) - 1)
            lower = gas.get_corner(DL)[:2] + margin
            for dot, xy in zip(cloud, lower + positions*size):
                dot.move_to([*xy, gas.get_z()])

        advance(dots, 0)
        dots.add_updater(advance)
        return dots

    def compact_piston(self, volume, pressure, temperature, with_readout=True):
        """A mesma câmara esquemática da introdução, ao lado do gráfico."""
        x, bottom, width = 2.55, 1.25, 1.25
        top = lambda: bottom + 0.46 * volume.get_value()
        walls = VGroup(
            Line([x-width/2,bottom,0],[x-width/2,3.3,0]),
            Line([x+width/2,bottom,0],[x+width/2,3.3,0]),
            Line([x-width/2,bottom,0],[x+width/2,bottom,0]),
        ).set_stroke(BLUE, 3)
        gas = always_redraw(lambda: Rectangle(
            width=width-0.08, height=0.46*volume.get_value(), stroke_width=0,
            fill_color=BLUE, fill_opacity=self.gas_opacity(pressure,temperature),
        ).move_to([x,bottom+0.23*volume.get_value(),0]))
        piston = always_redraw(lambda: VGroup(
            Rectangle(width=width+0.12,height=0.16,stroke_width=0,
                      fill_color=BLUE,fill_opacity=1).move_to([x,top(),0]),
            Line([x-width/2,top()+0.07,0],[x+width/2,top()+0.07,0],
                 color=TEXT_COLOR,stroke_width=1.6),
            Line([x,top()+0.06,0],[x,top()+0.57,0],color=BLUE,stroke_width=4),
        ))
        particles = self.gas_particles(gas, temperature)
        if not with_readout:
            vessel = VGroup(walls,gas,particles,piston)
            vessel.particles = particles
            return vessel
        readout = self.state_readout(volume,pressure,temperature)
        self.small_piston, self.thermal = piston, readout.state_fills[2]
        self.compact_state = readout
        return VGroup(walls,gas,particles,piston,readout)

    def heat_transfer(self, volume, entering=True):
        # A seta cruza a parede na altura do gás, inclusive após a compressão.
        y = 1.25 + 0.23 * volume.get_value()
        outside, inside = np.array([3.9,y,0]), np.array([2.8,y,0])
        arrow = Arrow(outside if entering else inside, inside if entering else outside,
                      color=MAGENTA,buff=0,stroke_width=4,
                      max_tip_length_to_length_ratio=0.25)
        label = self.math("Q",y+0.45,30).set_x(3.55)
        return VGroup(arrow,label)

    def piston_work(self, expansion=True):
        low, high = np.array([3.6,3.35,0]), np.array([3.6,4.1,0])
        arrow = Arrow(low if expansion else high,high if expansion else low,
                      color=CYAN,buff=0,stroke_width=3,
                      max_tip_length_to_length_ratio=0.3)
        label = self.math("W>0" if expansion else "W<0",4.5,29,width=2.0).set_x(2.65)
        return VGroup(arrow,label)

    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        timing = json.loads((UNIT / "sync.json").read_text(encoding="utf-8"))
        self.cues = {**dict(timing["anchors"]), **timing["extras"]}
        self.events = []
        # Padrão de série: episódio público à esquerda e marca oficial à direita.
        brand = screen_text("EXERCÍCIO RESOLVIDO · EP. 07", 20, oversample=2)
        brand.set_opacity(0.65).to_corner(UP + LEFT, buff=0.4).set_z_index(200)
        watermark = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        watermark.to_corner(UP + RIGHT, buff=0.28).set_z_index(200)
        self.add(brand, watermark)
        self.title = self.words("Qual é o calor total\nabsorvido pelo gás\ndurante o ciclo?", 5.85, 32)
        self.subtitle = None
        volume, pressure, temperature = ValueTracker(1), ValueTracker(1), ValueTracker(1)
        self.add(volume,pressure,temperature)
        opening_vessel = self.compact_piston(volume,pressure,temperature,with_readout=False)
        for part in opening_vessel:
            if part is not opening_vessel.particles:
                part.clear_updaters(recursive=True)
        opening_vessel.scale(1.05).move_to([0,1.3,0])
        opening_vessel.particles.update(0)
        opening_state = self.math(r"A=(V_0,P_0)",-0.55,33)
        self.play(FadeIn(self.title),FadeIn(opening_vessel),FadeIn(opening_state),run_time=0.8)
        self.cue("estado_A", lead=3.0)
        self.play(FadeOut(opening_vessel),FadeOut(opening_state),run_time=0.4)
        self.heading("Um ciclo, três processos", "Gás ideal monoatômico")
        self.graph()
        self.play(Create(self.axes), FadeIn(self.grid[1:]), run_time=1.2)

        # Pistão 2D: área transversal constante e altura proporcional a V.
        bottom, chamber_x, chamber_w = -4.6, -1.45, 1.65
        piston_y = lambda: bottom + 0.5 * volume.get_value()
        walls = VGroup(
            Line([chamber_x-chamber_w/2, bottom, 0], [chamber_x-chamber_w/2, -2.35, 0]),
            Line([chamber_x+chamber_w/2, bottom, 0], [chamber_x+chamber_w/2, -2.35, 0]),
            Line([chamber_x-chamber_w/2, bottom, 0], [chamber_x+chamber_w/2, bottom, 0]),
        ).set_stroke(BLUE, 3)
        gas = always_redraw(lambda: Rectangle(
            width=chamber_w-0.08, height=0.5*volume.get_value(),
            stroke_width=0, fill_color=BLUE, fill_opacity=self.gas_opacity(pressure,temperature),
        ).move_to([chamber_x, bottom+0.25*volume.get_value(), 0]))
        piston = always_redraw(lambda: VGroup(
            Rectangle(width=chamber_w+0.12, height=0.15, color=BLUE,
                      fill_color=BLUE, fill_opacity=1).move_to([chamber_x, piston_y(), 0]),
            Line([chamber_x-chamber_w/2,piston_y()+0.07,0],
                 [chamber_x+chamber_w/2,piston_y()+0.07,0],color=TEXT_COLOR,stroke_width=1.6),
            Line([chamber_x, piston_y()+0.08, 0], [chamber_x, piston_y()+0.65, 0],
                 color=BLUE, stroke_width=5),
        ))
        gas_label = self.words("gás", -5.05, 22, MUTED).set_x(chamber_x)
        intro_state = self.state_readout(volume,pressure,temperature,center=(1.55,-3.6),bar_width=1.7,size=28)
        particles = self.gas_particles(gas, temperature)
        physical = Group(walls,gas,particles,piston,gas_label,intro_state)
        self.play(FadeIn(physical), FadeIn(self.dots[0]), Write(self.labels[0]), FadeIn(self.marker), run_time=0.7)
        caption = self.math(r"A=(V_0,P_0)", -1.0, 34)
        self.play(Write(caption), run_time=0.6)
        self.cue("intro_AB", lead=0.75)
        next_caption = self.words("A → B  •  expansão isobárica", -1.0, 27)
        self.play(FadeOut(caption), FadeIn(next_caption), run_time=0.4)
        self.state_trend(intro_state,"AB")
        self.play(Create(self.ab), self.marker.animate.move_to(self.b), volume.animate.set_value(4),
                  temperature.animate.set_value(4), run_time=3.1, rate_func=linear)
        self.play(FadeIn(self.dots[1]), Write(self.labels[1]), FadeIn(self.arrows[0]), run_time=0.5)
        state_b = self.math(r"B=(4V_0,P_0)", -1.7, 31)
        self.play(FadeIn(state_b), run_time=0.4)
        self.cue("intro_BC", lead=0.35)
        caption_c = self.words("B → C  •  volume constante", -1.0, 27)
        self.play(FadeOut(next_caption), FadeOut(state_b), FadeIn(caption_c), run_time=0.4)
        self.state_trend(intro_state,"BC")
        self.play(Create(self.bc),self.marker.animate.move_to(self.c),pressure.animate.set_value(4),temperature.animate.set_value(16),
                  run_time=2.8, rate_func=linear)
        self.play(FadeIn(self.dots[2]), Write(self.labels[2]), FadeIn(self.arrows[1]), run_time=0.5)
        state_c = self.math(r"C=(4V_0,4P_0)", -1.7, 31)
        self.play(FadeIn(state_c), run_time=0.4)
        self.cue("intro_CA", lead=0.75)
        caption_a = self.words("C → A  •  retorno linear", -1.0, 27)
        self.play(FadeOut(caption_c), FadeOut(state_c), FadeIn(caption_a), run_time=0.4)
        self.state_trend(intro_state,"CA")
        # Na reta P/P0 = V/V0, T/TA = (V/V0)^2.
        pressure.add_updater(lambda p: p.set_value(volume.get_value()))
        temperature.add_updater(lambda t: t.set_value(volume.get_value()**2))
        self.play(Create(self.ca), self.marker.animate.move_to(self.a), volume.animate.set_value(1),
                  run_time=2.8, rate_func=linear)
        temperature.clear_updaters()
        pressure.clear_updaters()
        self.play(FadeIn(self.arrows[2]), run_time=0.3)
        self.cue("ferramentas", lead=1.3)

        # as três ferramentas, apresentadas uma de cada vez.
        physical.clear_updaters(recursive=True)
        graph_all = VGroup(self.grid, self.paths, self.dots, self.labels, self.arrows, self.marker)
        compact = self.compact_piston(volume,pressure,temperature)
        self.play(FadeOut(physical), FadeOut(caption_a),
                  graph_all.animate.scale(0.76).move_to([-1.25,2.7,0]),FadeIn(compact),run_time=0.6)
        self.sync_points()
        self.heading("As ferramentas", "Para este gás ideal monoatômico")
        u = self.math(r"U=\frac{3}{2}nRT", -0.95, 46)
        ideal = self.math(r"PV=nRT", -1.9, 34)
        self.play(Write(u), run_time=0.8)
        self.play(Write(ideal), run_time=0.7)
        self.cue("u_pv", lead=0.4)
        u = self.equation_change(u, r"U=\frac{3}{2}PV", size=46)
        self.play(FadeOut(ideal), run_time=0.4)
        sign = self.words("W > 0: trabalho realizado pelo gás", -3.95, 23, MUTED)
        self.cue("primeira_lei")
        self.play(FadeIn(sign), run_time=0.5)
        law = self.math(r"Q=\Delta U+W", -2.8, 47)
        self.cue("lei_equacao", lead=0.2)
        self.play(Write(law), run_time=1.0)
        work = self.math(r"W=\int P\,dV", -5.05, 46)
        self.cue("integral", lead=0.2)
        self.play(Write(work), run_time=1.0)
        self.cue("geometria")
        self.play(Indicate(work, color=CYAN, scale_factor=1.04), run_time=0.6)
        self.cue("AB", lead=1.3)

        # trabalho, energia interna e calor de A → B.
        self.play(FadeOut(VGroup(u, law, sign, work)),
                  run_time=0.6)
        self.sync_points()
        work_physical = self.piston_work(expansion=True)
        self.heading("A → B: expansão isobárica", "O gás se expande e realiza trabalho")
        self.play(FadeIn(work_physical),run_time=0.6)
        self.focus(self.ab, self.a)
        self.state_trend(self.compact_state,"AB")
        integral = self.math(r"W=\int P\,dV", -1.0, 37, CYAN)
        self.play(Write(integral), run_time=0.8)
        area_ab = Polygon(self.pt(1,0), self.pt(4,0), self.b, self.a,
                          stroke_width=0, fill_color=CYAN, fill_opacity=0.23).set_z_index(-1)
        self.play(GrowFromEdge(area_ab, LEFT), self.marker.animate.move_to(self.b),
                  volume.animate.set_value(4),temperature.animate.set_value(4),
                  run_time=2.4, rate_func=linear)
        w_ab = self.math(r"W_{AB}=P_0(4V_0-V_0)", -2.25)
        self.play(Write(w_ab), run_time=1.2)
        self.cue("w_ab_valor", lead=0.3)
        w_ab = self.equation_change(w_ab, r"W_{AB}=3P_0V_0", color=CYAN)
        self.play(area_ab.animate.set_fill(opacity=0.42),rate_func=there_and_back,run_time=0.7)
        self.play(FadeOut(integral), w_ab.animate.move_to([0,-1.05,0]), run_time=0.7)
        du_ab = self.math(r"\Delta U_{AB}=\frac32(P_BV_B-P_AV_A)", -2.65, 39)
        du_badge = self.math(r"\Delta U>0",3.95,26,width=1.8).set_x(2.55)
        self.cue("DU_AB", lead=0.25)
        self.play(Indicate(self.dots[0],color=VIOLET), Indicate(self.dots[1],color=VIOLET),
                  Indicate(self.thermal,color=VIOLET),FadeIn(du_badge),Write(du_ab),run_time=1.4)
        self.cue("du_ab_valor", lead=2.0)
        du_ab = self.equation_change(du_ab, r"\Delta U_{AB}=\frac32(4-1)P_0V_0", size=40)
        self.cue("du_ab_valor", lead=0.3)
        du_ab = self.equation_change(du_ab, r"\Delta U_{AB}=\frac92P_0V_0")
        self.cue("Q_AB", lead=0.3)
        q_ab = self.math(r"Q_{AB}=\Delta U_{AB}+W_{AB}", -4.35, 41)
        heat_in = self.heat_transfer(volume,entering=True)
        self.play(Write(q_ab),GrowArrow(heat_in[0]),FadeIn(heat_in[1]),run_time=1.2)
        self.cue("q_ab_valor", lead=0.3)
        q_ab = self.equation_change(q_ab, r"Q_{AB}=\frac{15}{2}P_0V_0>0", color=CYAN)
        heat_note = self.words("calor entra no gás", -5.3, 24, MAGENTA)
        self.cue("calor_entra_AB")
        self.play(Indicate(heat_in[0],color=MAGENTA), FadeIn(heat_note), run_time=0.8)
        self.cue("BC", lead=1.3)

        # volume fixo; nenhum deslocamento na direção V.
        self.play(FadeOut(VGroup(w_ab,du_ab,q_ab,heat_in,heat_note,du_badge,work_physical,area_ab)),run_time=0.5)
        self.heading("B → C: processo isocórico", "O volume permanece constante")
        self.focus(self.bc, self.b)
        self.state_trend(self.compact_state,"BC")
        fixed = DashedLine(self.pt(4,0), self.c, color=CYAN, stroke_width=2)
        zero_work = self.math(r"\Delta V=0",4.5,29,width=2.0).set_x(2.55)
        self.play(Create(fixed),self.marker.animate.move_to(self.c),pressure.animate.set_value(4),temperature.animate.set_value(16),
                  FadeIn(zero_work),run_time=2.3,rate_func=linear)
        dv = self.math(r"dV=0", -1.1, 46)
        self.cue("W_BC", lead=0.2)
        self.play(Write(dv),Indicate(self.small_piston,color=CYAN,scale_factor=1),run_time=0.8)
        dv = self.equation_change(dv, r"W_{BC}=\int P\,dV=0", color=CYAN)
        zero_status = self.math("W=0",4.5,29,width=2.0).set_x(2.55)
        self.play(TransformMatchingTex(zero_work,zero_status),run_time=0.5)
        self.cue("DU_BC", lead=0.4)
        du_bc = self.math(r"\Delta U_{BC}=\frac32(16P_0V_0-4P_0V_0)", -2.85, 37)
        du_badge = self.math(r"\Delta U>0",3.95,26,width=1.8).set_x(2.55)
        self.play(Write(du_bc),Indicate(self.thermal,color=VIOLET),FadeIn(du_badge),run_time=1.3)
        self.cue("du_bc_valor", lead=0.2)
        du_bc = self.equation_change(du_bc, r"\Delta U_{BC}=18P_0V_0")
        self.cue("Q_BC", lead=0.2)
        q_bc = self.math(r"Q_{BC}=\Delta U_{BC}+0", -4.45, 42)
        heat_in = self.heat_transfer(volume,entering=True)
        self.play(Write(q_bc),GrowArrow(heat_in[0]),FadeIn(heat_in[1]),run_time=1.0)
        self.cue("calor_entra_BC", lead=1.5)
        q_bc = self.equation_change(q_bc, r"Q_{BC}=18P_0V_0>0", color=CYAN)
        bc_note = self.words("calor entra no gás", -5.5, 24, MAGENTA)
        self.cue("calor_entra_BC")
        self.play(FadeIn(bc_note), run_time=0.5)
        self.cue("CA", lead=1.3)

        # apenas sinais, sem desenvolver Q_CA numericamente.
        self.play(FadeOut(VGroup(dv,du_bc,q_bc,bc_note,fixed,heat_in,du_badge,zero_status)),run_time=0.5)
        self.heading("C → A: retorno linear", "Compressão  •  trabalho sobre o gás")
        self.focus(self.ca, self.c)
        self.state_trend(self.compact_state,"CA")
        work_physical = self.piston_work(expansion=False)
        pressure.add_updater(lambda p: p.set_value(volume.get_value()))
        temperature.add_updater(lambda t: t.set_value(volume.get_value()**2))
        self.play(self.marker.animate.move_to(self.a),volume.animate.set_value(1),FadeIn(work_physical),
                  run_time=2.5,rate_func=linear)
        temperature.clear_updaters()
        pressure.clear_updaters()
        pv = self.math(r"PV:\ 16P_0V_0\longrightarrow P_0V_0", -1.0, 39)
        self.play(Write(pv), run_time=1.0)
        pv = self.equation_change(pv, r"PV\downarrow\quad\Rightarrow\quad\Delta U_{CA}<0")
        du_badge = self.math(r"\Delta U<0",3.95,26,width=1.8).set_x(2.55)
        self.play(FadeIn(du_badge),Indicate(self.thermal,color=VIOLET),run_time=0.5)
        v = self.math(r"V:\ 4V_0\longrightarrow V_0", -2.55, 40)
        self.play(Write(v), run_time=0.8)
        self.cue("w_ca_negativo", lead=0.3)
        v = self.equation_change(v, r"V\downarrow\quad\Rightarrow\quad W_{CA}<0")
        q_ca = self.math(r"Q_{CA}=\underbrace{\Delta U_{CA}}_{<0}+\underbrace{W_{CA}}_{<0}", -4.05, 41)
        self.cue("Q_CA", lead=0.3)
        self.play(Write(q_ca), run_time=0.9)
        self.cue("q_ca_negativo", lead=0.3)
        q_ca = self.equation_change(q_ca, r"Q_{CA}<0", size=49)
        heat_out = self.heat_transfer(volume,entering=False)
        out_note = self.words("calor sai  •  não entra em Q absorvido", -5.4, 23, MAGENTA)
        self.play(FadeIn(out_note),GrowArrow(heat_out[0]),FadeIn(heat_out[1]),run_time=0.6)
        self.cue("excluir_CA")
        self.play(Indicate(out_note, color=MAGENTA, scale_factor=1.02), run_time=0.4)
        self.cue("soma_abs", lead=1.3)

        # resposta à pergunta original.
        self.play(FadeOut(VGroup(pv,v,q_ca,out_note,heat_out,work_physical,du_badge)),
                  FadeOut(compact),graph_all.animate.scale(0.8/0.76).move_to([0,2.7,0]),run_time=0.6)
        self.sync_points()
        self.heading("Calor total absorvido", "Somamos somente os trechos com Q > 0")
        self.play(self.ab.animate.set_color(MAGENTA).set_opacity(1),
                  self.bc.animate.set_color(MAGENTA).set_opacity(1),
                  self.ca.animate.set_color(BLUE).set_opacity(0.2),
                  self.arrows[0].animate.set_color(MAGENTA).set_opacity(1),
                  self.arrows[1].animate.set_color(MAGENTA).set_opacity(1),
                  self.arrows[2].animate.set_opacity(0.2),run_time=0.6)
        positives = VGroup(
            self.math(r"Q_{AB}=\frac{15}{2}P_0V_0", -0.7, 39),
            self.math(r"Q_{BC}=18P_0V_0", -1.85, 39),
        )
        self.play(Write(positives), run_time=1.0)
        total = self.math(r"Q_{\mathrm{abs}}=Q_{AB}+Q_{BC}", -3.35, 45)
        self.play(Write(total), run_time=0.9)
        total = self.equation_change(total, r"Q_{\mathrm{abs}}=\frac{15}{2}P_0V_0+18P_0V_0", size=43)
        self.cue("abs_valor", lead=0.3)
        total = self.equation_change(total, r"Q_{\mathrm{abs}}=\frac{51}{2}P_0V_0", y=-3.5, size=58)
        answer_box = SurroundingRectangle(total, buff=0.3, color=MAGENTA, corner_radius=0.14, stroke_width=2)
        self.play(Create(answer_box), FadeOut(positives), run_time=0.8)
        self.cue("triangulo", lead=1.3)

        # área interna dá o módulo; percurso determina o sinal.
        self.play(FadeOut(VGroup(total,answer_box)),
                  graph_all.animate.scale(1/0.8).move_to([-0.25,2.7,0]),run_time=0.6)
        self.sync_points()
        self.heading("Trabalho líquido do ciclo", "O módulo vem da área interna")
        triangle = Polygon(self.a,self.b,self.c, stroke_width=0,
                           fill_color=CYAN,fill_opacity=0.22).set_z_index(-1)
        self.play(*[path.animate.set_color(CYAN).set_opacity(1) for path in self.paths],
                  self.arrows.animate.set_color(CYAN).set_opacity(1),
                  FadeIn(triangle),FadeOut(self.marker),run_time=0.8)
        base = BraceBetweenPoints(self.a+0.12*DOWN,self.b+0.12*DOWN, direction=DOWN, color=MUTED)
        height = BraceBetweenPoints(self.b+0.75*RIGHT,self.c+0.75*RIGHT, direction=RIGHT, color=MUTED)
        base_text = MathTex(r"3V_0",font_size=29,color=CYAN).next_to(base,DOWN,buff=0.08)
        height_text = MathTex(r"3P_0",font_size=29,color=CYAN).next_to(height,RIGHT,buff=0.1)
        area = self.math(r"A_{\triangle}=\frac12(\mathrm{base})(\mathrm{altura})", -1.65, 40)
        self.cue("area_triangulo")
        self.play(Write(area),run_time=1.0)
        self.cue("base_altura", lead=0.2)
        self.play(GrowFromCenter(base),GrowFromCenter(height),Write(base_text),Write(height_text),run_time=0.8)
        area = self.equation_change(area,r"A_{\triangle}=\frac12(3V_0)(3P_0)",size=43)
        self.cue("resultado_area", lead=0.3)
        area = self.equation_change(area,r"A_{\triangle}=\frac92P_0V_0")
        trace = VMobject().set_points_as_corners([self.a,self.b,self.c,self.a])
        self.marker.move_to(self.a)
        self.add(self.marker)
        self.cue("sentido", lead=2.0)
        self.play(MoveAlongPath(self.marker,trace),run_time=3.3,rate_func=linear)
        sense = self.words("Anti-horário: o sentido dá o sinal negativo", -3.1, 25)
        self.play(FadeIn(sense),run_time=0.4)
        net_w = self.math(r"W_{\mathrm{ciclo}}=-\frac92P_0V_0",-4.55,49,CYAN)
        self.cue("w_liquido_negativo")
        self.play(Write(net_w),run_time=1.0)
        integral_note = self.math(r"W_{\mathrm{ciclo}}=\oint P\,dV", -5.65, 31, MUTED)
        self.play(FadeIn(integral_note),run_time=0.5)
        self.cue("conferencia", lead=0.5)

        # fechamento conceitual e CTA, com pausas de leitura próprias.
        self.play(FadeOut(VGroup(area,sense,net_w,integral_note,base,height,base_text,height_text)),run_time=0.5)
        self.heading("De volta ao estado A", "Estado final = estado inicial")
        self.play(Indicate(self.dots[0],color=CYAN),run_time=0.6)
        zero_u = self.math(r"\Delta U_{\mathrm{ciclo}}=0", -1.05, 44)
        self.cue("zero_ciclo", lead=0.2)
        self.play(Write(zero_u),run_time=0.6)
        net_q = self.math(r"Q_{\mathrm{l\acute iquido}}=W_{\mathrm{ciclo}}",-2.6,43)
        self.cue("Q_liquido", lead=0.2)
        self.play(Write(net_q),run_time=0.6)
        self.cue("q_liquido_igual", lead=0.2)
        net_q = self.equation_change(net_q,r"Q_{\mathrm{l\acute iquido}}=W_{\mathrm{ciclo}}=-\frac92P_0V_0",size=42,color=CYAN)
        closing = self.words("No ciclo, o gás cede mais calor\ndo que absorve.",-4.4,27)
        self.cue("cedido", lead=0.2)
        self.play(FadeIn(closing),run_time=0.6)
        closing2 = self.words("A diferença é o trabalho líquido.",-5.5,23,MUTED)
        self.play(FadeIn(closing2),run_time=0.4)
        self.cue("CTA", lead=0.5)
        # CTA discreto após o resultado; preserva o gráfico como continuidade.
        self.play(FadeOut(closing),FadeOut(closing2),run_time=0.5)
        handle = self.words("@labparallax",-5.3,31).set_color_by_gradient(CYAN,VIOLET,MAGENTA)
        self.play(FadeIn(handle),run_time=0.6)
        self.finish_block(timing["audio_duration_s"])
        (UNIT / f"timing_particulas_{config.pixel_width}x{config.pixel_height}.json").write_text(
            json.dumps(dict(duration=self.time, fps=config.frame_rate, events=self.events), indent=2),
            encoding="utf-8")
