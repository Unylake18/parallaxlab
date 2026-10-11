"""VID21 — primeiro preview silencioso, inteiramente em 2D.

Preview: uv run python -m manim -r 540,960 --fps 15 \
    videos/vid_0021_ciclo_termodinamico/cena.py CicloTermodinamico021
Q_CA = -30 P0 V0 é apenas referência documental de QA, não etapa da cena.
"""

from pathlib import Path
import sys

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config import (
    BACKGROUND_COLOR, TEXT_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, WATERMARK_PATH,
)
from template.fonts import screen_text

UNIT = Path(__file__).resolve().parent
config.media_dir = str(UNIT / "media")
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

    def compact_piston(self, volume, temperature):
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
            fill_color=BLUE, fill_opacity=0.18,
        ).move_to([x,bottom+0.23*volume.get_value(),0]))
        piston = always_redraw(lambda: VGroup(
            Rectangle(width=width+0.12,height=0.13,stroke_width=0,
                      fill_color=BLUE,fill_opacity=1).move_to([x,top(),0]),
            Line([x,top()+0.06,0],[x,top()+0.57,0],color=BLUE,stroke_width=4),
        ))
        outline = RoundedRectangle(width=1.7,height=0.25,corner_radius=0.08,
                                   color=VIOLET,stroke_width=1.4).move_to([x,0.65,0])
        thermal = always_redraw(lambda: Rectangle(
            width=0.18+1.4*np.log(temperature.get_value())/np.log(16),height=0.14,
            stroke_width=0,fill_color=VIOLET,fill_opacity=0.85,
        ).align_to(outline,LEFT).shift(0.06*RIGHT).set_y(0.65))
        t_label = self.math(r"T\propto PV",0.1,26,width=1.95).set_x(x)
        self.small_piston, self.thermal = piston, thermal
        return VGroup(walls,gas,piston,outline,thermal,t_label)

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
        brand = self.words("EXERCÍCIO RESOLVIDO  •  21", 7.3, 18, MUTED)
        watermark = ImageMobject(str(WATERMARK_PATH)).set_opacity(0.32)
        watermark.scale_to_fit_width(1.55).move_to([3.1, -7.3, 0])
        self.add(brand, watermark)
        self.title = self.words("Qual é o calor total\nabsorvido pelo gás\ndurante o ciclo?", 5.85, 32)
        self.subtitle = None
        self.play(FadeIn(self.title), run_time=0.8)
        self.wait(2.2)
        self.heading("Um ciclo, três processos", "Gás ideal monoatômico")
        self.graph()
        self.play(Create(self.axes), FadeIn(self.grid[1:]), run_time=1.2)

        # Pistão 2D: área transversal constante e altura proporcional a V.
        volume = ValueTracker(1)
        temperature = ValueTracker(1)
        bottom, chamber_x, chamber_w = -4.6, -1.45, 1.65
        piston_y = lambda: bottom + 0.5 * volume.get_value()
        walls = VGroup(
            Line([chamber_x-chamber_w/2, bottom, 0], [chamber_x-chamber_w/2, -2.35, 0]),
            Line([chamber_x+chamber_w/2, bottom, 0], [chamber_x+chamber_w/2, -2.35, 0]),
            Line([chamber_x-chamber_w/2, bottom, 0], [chamber_x+chamber_w/2, bottom, 0]),
        ).set_stroke(BLUE, 3)
        gas = always_redraw(lambda: Rectangle(
            width=chamber_w-0.08, height=0.5*volume.get_value(),
            stroke_width=0, fill_color=BLUE, fill_opacity=0.15,
        ).move_to([chamber_x, bottom+0.25*volume.get_value(), 0]))
        piston = always_redraw(lambda: VGroup(
            Rectangle(width=chamber_w+0.12, height=0.15, color=BLUE,
                      fill_color=BLUE, fill_opacity=1).move_to([chamber_x, piston_y(), 0]),
            Line([chamber_x, piston_y()+0.08, 0], [chamber_x, piston_y()+0.65, 0],
                 color=BLUE, stroke_width=5),
        ))
        gas_label = self.words("gás", -5.05, 22, MUTED).set_x(chamber_x)
        # Indicador qualitativo; não representa velocidade molecular.
        temp_label = self.words("temperatura", -3.0, 23, MUTED).set_x(1.65)
        temp_outline = RoundedRectangle(width=2.1, height=0.3, corner_radius=0.1,
                                        color=VIOLET, stroke_width=1.5).move_to([1.65, -3.6, 0])
        temp_fill = always_redraw(lambda: Rectangle(
            width=0.25+1.7*np.log(temperature.get_value())/np.log(16), height=0.18,
            stroke_width=0, fill_color=VIOLET, fill_opacity=0.9,
        ).align_to(temp_outline, LEFT).shift(0.06*RIGHT).set_y(-3.6))
        temp_note = self.math(r"T\propto PV", -4.25, 30).set_x(1.65)
        physical = Group(walls, gas, piston, gas_label, temp_label, temp_outline, temp_fill, temp_note)
        self.play(FadeIn(physical), FadeIn(self.dots[0]), Write(self.labels[0]), FadeIn(self.marker), run_time=0.7)
        caption = self.math(r"A=(V_0,P_0)", -1.0, 34)
        self.play(Write(caption), run_time=0.6)
        self.wait(0.8)
        next_caption = self.words("A → B  •  expansão isobárica", -1.0, 27)
        self.play(FadeOut(caption), FadeIn(next_caption), run_time=0.4)
        self.play(Create(self.ab), self.marker.animate.move_to(self.b), volume.animate.set_value(4),
                  temperature.animate.set_value(4), run_time=3.1, rate_func=linear)
        self.play(FadeIn(self.dots[1]), Write(self.labels[1]), FadeIn(self.arrows[0]), run_time=0.5)
        state_b = self.math(r"B=(4V_0,P_0)", -1.7, 31)
        self.play(FadeIn(state_b), run_time=0.4)
        self.wait(0.8)
        caption_c = self.words("B → C  •  volume constante", -1.0, 27)
        self.play(FadeOut(next_caption), FadeOut(state_b), FadeIn(caption_c), run_time=0.4)
        self.play(Create(self.bc), self.marker.animate.move_to(self.c), temperature.animate.set_value(16),
                  run_time=2.8, rate_func=linear)
        self.play(FadeIn(self.dots[2]), Write(self.labels[2]), FadeIn(self.arrows[1]), run_time=0.5)
        state_c = self.math(r"C=(4V_0,4P_0)", -1.7, 31)
        self.play(FadeIn(state_c), run_time=0.4)
        self.wait(0.8)
        caption_a = self.words("C → A  •  compressão em reta", -1.0, 27)
        self.play(FadeOut(caption_c), FadeOut(state_c), FadeIn(caption_a), run_time=0.4)
        # Na reta P/P0 = V/V0, T/TA = (V/V0)^2.
        temperature.add_updater(lambda t: t.set_value(volume.get_value()**2))
        self.play(Create(self.ca), self.marker.animate.move_to(self.a), volume.animate.set_value(1),
                  run_time=2.8, rate_func=linear)
        temperature.clear_updaters()
        self.play(FadeIn(self.arrows[2]), run_time=0.3)
        self.finish_block(25)

        # 25–40 s: as três ferramentas, apresentadas uma de cada vez.
        gas.clear_updaters(); piston.clear_updaters(); temp_fill.clear_updaters()
        graph_all = VGroup(self.grid, self.paths, self.dots, self.labels, self.arrows, self.marker)
        self.play(FadeOut(physical), FadeOut(caption_a),
                  graph_all.animate.scale(0.82).move_to([0,2.7,0]), run_time=0.6)
        self.sync_points()
        self.heading("As ferramentas", "Para este gás ideal monoatômico")
        u = self.math(r"U=\frac{3}{2}nRT", -0.65, 46)
        ideal = self.math(r"PV=nRT", -1.9, 34)
        self.play(Write(u), run_time=0.8)
        self.play(Write(ideal), run_time=0.7)
        self.wait(1.0)
        u = self.equation_change(u, r"U=\frac{3}{2}PV", size=46)
        self.play(FadeOut(ideal), run_time=0.4)
        law = self.math(r"Q=\Delta U+W", -2.8, 47)
        self.play(Write(law), run_time=1.0)
        sign = self.words("W > 0: trabalho realizado pelo gás", -3.95, 23, MUTED)
        self.play(FadeIn(sign), run_time=0.5)
        work = self.math(r"W=\int P\,dV", -5.05, 46)
        self.play(Write(work), run_time=1.0)
        self.finish_block(40)

        # 40–75 s: trabalho, energia interna e calor de A → B.
        self.play(FadeOut(VGroup(u, law, sign, work)),
                  graph_all.animate.scale(0.76/0.82).move_to([-1.25,2.7,0]),run_time=0.6)
        self.sync_points()
        compact = self.compact_piston(volume,temperature)
        work_physical = self.piston_work(expansion=True)
        self.heading("A → B: expansão isobárica", "O gás se expande e realiza trabalho")
        self.play(FadeIn(compact),FadeIn(work_physical),run_time=0.6)
        self.focus(self.ab, self.a)
        integral = self.math(r"W=\int P\,dV", -1.0, 37, CYAN)
        self.play(Write(integral), run_time=0.8)
        area_ab = Polygon(self.pt(1,0), self.pt(4,0), self.b, self.a,
                          stroke_width=0, fill_color=CYAN, fill_opacity=0.23).set_z_index(-1)
        self.play(GrowFromEdge(area_ab, LEFT), self.marker.animate.move_to(self.b),
                  volume.animate.set_value(4),temperature.animate.set_value(4),
                  run_time=2.4, rate_func=linear)
        w_ab = self.math(r"W_{AB}=P_0(4V_0-V_0)", -2.25)
        self.play(Write(w_ab), run_time=1.2)
        self.wait(1.5)
        w_ab = self.equation_change(w_ab, r"W_{AB}=3P_0V_0", color=CYAN)
        self.play(area_ab.animate.set_fill(opacity=0.42),rate_func=there_and_back,run_time=0.7)
        self.wait(1.3)
        self.play(FadeOut(integral), w_ab.animate.move_to([0,-1.05,0]), run_time=0.7)
        du_ab = self.math(r"\Delta U_{AB}=\frac32(P_BV_B-P_AV_A)", -2.65, 39)
        du_badge = self.math(r"\Delta U>0",-0.5,28,width=2.0).set_x(2.55)
        self.play(Indicate(self.dots[0],color=VIOLET), Indicate(self.dots[1],color=VIOLET),
                  Indicate(self.thermal,color=VIOLET),FadeIn(du_badge),Write(du_ab),run_time=1.4)
        self.wait(2.0)
        du_ab = self.equation_change(du_ab, r"\Delta U_{AB}=\frac32(4-1)P_0V_0", size=40)
        self.wait(1.4)
        du_ab = self.equation_change(du_ab, r"\Delta U_{AB}=\frac92P_0V_0")
        self.wait(2.0)
        q_ab = self.math(r"Q_{AB}=\Delta U_{AB}+W_{AB}", -4.35, 41)
        heat_in = self.heat_transfer(volume,entering=True)
        self.play(Write(q_ab),GrowArrow(heat_in[0]),FadeIn(heat_in[1]),run_time=1.2)
        self.wait(1.4)
        q_ab = self.equation_change(q_ab, r"Q_{AB}=\frac{15}{2}P_0V_0>0", color=CYAN)
        heat_note = self.words("calor entra no gás", -5.3, 24, MAGENTA)
        self.play(Indicate(heat_in[0],color=MAGENTA), FadeIn(heat_note), run_time=0.8)
        self.finish_block(75)

        # 75–100 s: volume fixo; nenhum deslocamento na direção V.
        self.play(FadeOut(VGroup(w_ab,du_ab,q_ab,heat_in,heat_note,du_badge,work_physical,area_ab)),run_time=0.5)
        self.heading("B → C: processo isocórico", "O volume permanece constante")
        self.focus(self.bc, self.b)
        fixed = DashedLine(self.pt(4,0), self.c, color=CYAN, stroke_width=2)
        zero_work = self.math(r"\Delta V=0",4.5,29,width=2.0).set_x(2.55)
        self.play(Create(fixed),self.marker.animate.move_to(self.c),temperature.animate.set_value(16),
                  FadeIn(zero_work),run_time=2.3,rate_func=linear)
        dv = self.math(r"dV=0", -1.1, 46)
        self.play(Write(dv),Indicate(self.small_piston,color=CYAN,scale_factor=1),run_time=0.8)
        self.wait(1.0)
        dv = self.equation_change(dv, r"W_{BC}=\int P\,dV=0", color=CYAN)
        zero_status = self.math("W=0",4.5,29,width=2.0).set_x(2.55)
        self.play(TransformMatchingTex(zero_work,zero_status),run_time=0.5)
        self.wait(1.3)
        du_bc = self.math(r"\Delta U_{BC}=\frac32(16P_0V_0-4P_0V_0)", -2.85, 37)
        du_badge = self.math(r"\Delta U>0",-0.5,28,width=2.0).set_x(2.55)
        self.play(Write(du_bc),Indicate(self.thermal,color=VIOLET),FadeIn(du_badge),run_time=1.3)
        self.wait(2.0)
        du_bc = self.equation_change(du_bc, r"\Delta U_{BC}=18P_0V_0")
        self.wait(1.5)
        q_bc = self.math(r"Q_{BC}=\Delta U_{BC}+0", -4.45, 42)
        heat_in = self.heat_transfer(volume,entering=True)
        self.play(Write(q_bc),GrowArrow(heat_in[0]),FadeIn(heat_in[1]),run_time=1.0)
        self.wait(1.0)
        q_bc = self.equation_change(q_bc, r"Q_{BC}=18P_0V_0>0", color=CYAN)
        bc_note = self.words("calor entra no gás", -5.5, 24, MAGENTA)
        self.play(FadeIn(bc_note), run_time=0.5)
        self.finish_block(100)

        # 100–120 s: apenas sinais, sem desenvolver Q_CA numericamente.
        self.play(FadeOut(VGroup(dv,du_bc,q_bc,bc_note,fixed,heat_in,du_badge,zero_status)),run_time=0.5)
        self.heading("C → A: compressão", "Trabalho sobre o gás  •  volume diminui")
        self.focus(self.ca, self.c)
        work_physical = self.piston_work(expansion=False)
        temperature.add_updater(lambda t: t.set_value(volume.get_value()**2))
        self.play(self.marker.animate.move_to(self.a),volume.animate.set_value(1),FadeIn(work_physical),
                  run_time=2.5,rate_func=linear)
        temperature.clear_updaters()
        pv = self.math(r"PV:\ 16P_0V_0\longrightarrow P_0V_0", -1.0, 39)
        self.play(Write(pv), run_time=1.0)
        self.wait(0.7)
        pv = self.equation_change(pv, r"PV\downarrow\quad\Rightarrow\quad\Delta U_{CA}<0")
        du_badge = self.math(r"\Delta U<0",-0.5,28,width=2.0).set_x(2.55)
        self.play(FadeIn(du_badge),Indicate(self.thermal,color=VIOLET),run_time=0.5)
        v = self.math(r"V:\ 4V_0\longrightarrow V_0", -2.55, 40)
        self.play(Write(v), run_time=0.8)
        self.wait(0.7)
        v = self.equation_change(v, r"V\downarrow\quad\Rightarrow\quad W_{CA}<0")
        q_ca = self.math(r"Q_{CA}=\underbrace{\Delta U_{CA}}_{<0}+\underbrace{W_{CA}}_{<0}", -4.05, 41)
        self.play(Write(q_ca), run_time=0.9)
        self.wait(0.8)
        q_ca = self.equation_change(q_ca, r"Q_{CA}<0", size=49)
        heat_out = self.heat_transfer(volume,entering=False)
        out_note = self.words("calor sai  •  não entra em Q absorvido", -5.4, 23, MAGENTA)
        self.play(FadeIn(out_note),GrowArrow(heat_out[0]),FadeIn(heat_out[1]),run_time=0.6)
        self.finish_block(120)

        # 120–135 s: resposta à pergunta original.
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
        self.wait(1.2)
        total = self.equation_change(total, r"Q_{\mathrm{abs}}=\frac{15}{2}P_0V_0+18P_0V_0", size=43)
        self.wait(1.0)
        total = self.equation_change(total, r"Q_{\mathrm{abs}}=\frac{51}{2}P_0V_0", y=-3.5, size=58)
        answer_box = SurroundingRectangle(total, buff=0.3, color=MAGENTA, corner_radius=0.14, stroke_width=2)
        self.play(Create(answer_box), FadeOut(positives), run_time=0.8)
        self.finish_block(135)

        # 135–153 s: área interna dá o módulo; percurso determina o sinal.
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
        self.play(GrowFromCenter(base),GrowFromCenter(height),Write(base_text),Write(height_text),run_time=0.8)
        area = self.math(r"A_{\triangle}=\frac12(3V_0)(3P_0)", -1.65, 43)
        self.play(Write(area),run_time=1.0)
        self.wait(1.0)
        area = self.equation_change(area,r"A_{\triangle}=\frac92P_0V_0")
        self.wait(0.7)
        trace = VMobject().set_points_as_corners([self.a,self.b,self.c,self.a])
        self.marker.move_to(self.a)
        self.add(self.marker)
        self.play(MoveAlongPath(self.marker,trace),run_time=3.3,rate_func=linear)
        sense = self.words("Anti-horário: o sentido dá o sinal negativo", -3.1, 25)
        self.play(FadeIn(sense),run_time=0.6)
        net_w = self.math(r"W_{\mathrm{ciclo}}=-\frac92P_0V_0",-4.55,49,CYAN)
        self.play(Write(net_w),run_time=1.0)
        integral_note = self.math(r"W_{\mathrm{ciclo}}=\oint P\,dV", -5.65, 31, MUTED)
        self.play(FadeIn(integral_note),run_time=0.5)
        self.finish_block(153)

        # 153–165 s: fechamento conceitual e CTA, com pausas de leitura próprias.
        self.play(FadeOut(VGroup(area,sense,net_w,integral_note,base,height,base_text,height_text)),run_time=0.5)
        self.heading("De volta ao estado A", "Estado final = estado inicial")
        self.play(Indicate(self.dots[0],color=CYAN),run_time=0.6)
        zero_u = self.math(r"\Delta U_{\mathrm{ciclo}}=0", -1.05, 44)
        self.play(Write(zero_u),run_time=0.6)
        net_q = self.math(r"Q_{\mathrm{l\acute iquido}}=W_{\mathrm{ciclo}}",-2.6,43)
        self.play(Write(net_q),run_time=0.6)
        net_q = self.equation_change(net_q,r"Q_{\mathrm{l\acute iquido}}=W_{\mathrm{ciclo}}=-\frac92P_0V_0",size=42,color=CYAN)
        closing = self.words("No ciclo, o gás cede mais calor\ndo que absorve.",-4.4,27)
        self.play(FadeIn(closing),run_time=0.6)
        closing2 = self.words("A diferença é o trabalho líquido.",-5.5,23,MUTED)
        self.play(FadeIn(closing2),run_time=0.4)
        self.wait(3.0)
        # CTA discreto após o resultado; preserva o gráfico como continuidade.
        self.play(FadeOut(closing),FadeOut(closing2),run_time=0.5)
        cta = self.words("PARALLAX LAB",-4.45,28)
        handle = self.words("@labparallax",-5.3,31)
        self.play(FadeIn(cta),FadeIn(handle),run_time=0.6)
        self.finish_block(165)
