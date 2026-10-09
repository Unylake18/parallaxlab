"""V2 silenciosa: o tubo é a referência persistente da derivação.

uv run python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0018_bernoulli/media_v2 -o preview_silencioso_v2 videos/vid_0018_bernoulli/cena.py BernoulliV2

Cache 3D local preparado com ponte.py: 540x960, 30 quadros, período 2 s.
MF-Tools considerado; TransformMatchingTex preserva parcelas sem glyph maps.
V1 preservada em cena_v1.py. Nenhum arquivo global é alterado.
"""
import json
from contextlib import contextmanager
from pathlib import Path
import sys

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parents[2]
UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from template.config import BACKGROUND_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

sys.path.insert(0, str(ROOT / "experimentos/blender/arsenal"))
from manim_solido3d import Solido3D
import ponte
ponte.CACHE = UNIT / "cache3d"

INK, PRESSURE, KINETIC, GRAVITY = TEXT_COLOR, "#35D9FF", "#AB99FF", "#FFD479"
VOLUME, WALL, MUTED = "#78E8B2", "#607595", "#ABB8D0"


@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width = config.pixel_height = 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def text(s, size=28, color=INK, width=7.6):
    with wide_pango():
        lines = [screen_text(line, size, color=color) for line in s.split("\n")]
    m = VGroup(*lines).arrange(DOWN, buff=.13)
    if m.width > width:
        m.scale_to_fit_width(width)
    return m


def eq(*parts, y=-.6, x=0, size=48, width=7.6, color=INK):
    m = MathTex(*parts, font_size=size, color=color)
    if m.width > width:
        m.scale_to_fit_width(width)
    for p in m:
        t = p.tex_string
        if t == r"\Delta V":
            p.set_color(VOLUME)
        elif any(q in t for q in ("P_", "F_", "W_")) or t == "P":
            p.set_color(PRESSURE)
        elif any(q in t for q in ("v_", "v^", "K_", r"\Delta K")):
            p.set_color(KINETIC)
        elif any(q in t for q in ("h_", "gh", "U_g", r"\rho g")):
            p.set_color(GRAVITY)
        elif t in ("=", "+", "-", "(", ")"):
            p.set_color(INK)
    return m.move_to([x, y, 0])


class FlowDiagram(VGroup):
    """Vista longitudinal; as faces indicam áreas transversais circulares.

    Comprimento do pacote proporcional a 1/r²: A Δx é constante. A área
    da silhueta 2D não representa volume, pois a profundidade não está desenhada.
    """
    LEFT_X, RIGHT_X = -3.05, 3.05
    R1, R2, L1 = .54, .40, .60
    L2 = L1 * (R1 / R2) ** 2
    INLET = LEFT_X + L1 / 2
    OUTLET = RIGHT_X - L2 / 2

    @staticmethod
    def blend(x):
        q = np.clip((x + 1.4) / 2.8, 0, 1)
        return q * q * (3 - 2 * q)

    @classmethod
    def cy(cls, x):
        return 3.10 + 1.25 * cls.blend(x)

    @classmethod
    def radius(cls, x):
        return cls.R1 + (cls.R2 - cls.R1) * cls.blend(x)

    @classmethod
    def point(cls, x):
        return np.array([x, cls.cy(x), 0.0])

    @classmethod
    def parcel(cls, center, opacity=.22):
        # As duas faces delimitam o mesmo volume integrado mesmo na curva.
        volume = np.pi * cls.R1**2 * cls.L1
        middle = np.interp(center, cls._volume_x, cls._volume_curve)
        start = np.interp(middle - volume / 2, cls._volume_curve, cls._volume_x)
        end = np.interp(middle + volume / 2, cls._volume_curve, cls._volume_x)
        return cls.slab(start, end, opacity)

    @classmethod
    def slab(cls, start, end, opacity=.22):
        end = max(start + .008, end)
        xs = np.linspace(start, end, 9)
        top = [[x, cls.cy(x) + .88 * cls.radius(x), 0] for x in xs]
        bottom = [[x, cls.cy(x) - .88 * cls.radius(x), 0] for x in xs[::-1]]
        body = Polygon(*top, *bottom, stroke_width=1.3, color=VOLUME,
                       fill_color=VOLUME, fill_opacity=opacity)
        caps = VGroup(*(Ellipse(width=.16, height=1.76 * cls.radius(x), color=VOLUME,
                               stroke_width=2, fill_opacity=opacity).move_to(cls.point(x))
                        for x in (start, end)))
        return VGroup(body, caps)

    def __init__(self):
        super().__init__()
        xs = np.linspace(self.LEFT_X, self.RIGHT_X, 80)
        upper = [[x, self.cy(x) + self.radius(x), 0] for x in xs]
        lower = [[x, self.cy(x) - self.radius(x), 0] for x in xs]
        self.walls = VGroup(*(VMobject(color=WALL, stroke_width=3).set_points_smoothly(p) for p in (upper, lower)))
        self.sections = VGroup(*(Ellipse(width=.18, height=2 * self.radius(x), color=INK,
                                        stroke_width=1.7, fill_opacity=.08).move_to(self.point(x))
                                 for x in (self.LEFT_X, self.RIGHT_X)))
        self.badges = VGroup(text("1", 24).move_to([-3, 4.65, 0]), text("2", 24).move_to([3, 5.58, 0]))
        self.areas = VGroup(eq(r"A_1", x=-2.95, y=4.02, size=33), eq(r"A_2", x=2.95, y=5.03, size=33))
        self.pressures = VGroup(eq(r"P_1", x=-3.65, y=3.75, size=32), eq(r"P_2", x=3.65, y=4.91, size=32))
        self.forces = VGroup(
            Arrow([-4, 3.1, 0], [-3.14, 3.1, 0], color=PRESSURE, buff=0, stroke_width=5, max_tip_length_to_length_ratio=.2),
            Arrow([4, 4.35, 0], [3.14, 4.35, 0], color=PRESSURE, buff=0, stroke_width=5, max_tip_length_to_length_ratio=.2),
        )
        self.velocities = VGroup(
            Arrow([-2.2, 3.1, 0], [-1.25, 3.1, 0], color=KINETIC, buff=0, stroke_width=4),
            Arrow([1.45, 4.35, 0], [2.85, 4.35, 0], color=KINETIC, buff=0, stroke_width=4),
        )
        self.vlabels = VGroup(eq(r"v_1", x=-1.55, y=2.28, size=33), eq(r"v_2", x=1.55, y=3.72, size=33))
        self.datum = DashedLine([-3.45, 1.65, 0], [3.45, 1.65, 0], color=WALL, stroke_width=1)
        self.height_lines = VGroup(*(DashedLine([x, 1.65, 0], [x, self.cy(s), 0], color=GRAVITY, stroke_width=1.5)
                                    for x, s in ((-3.43, self.LEFT_X), (3.43, self.RIGHT_X))))
        self.hlabels = VGroup(eq(r"h_1", x=-3.76, y=2.28, size=32), eq(r"h_2", x=3.76, y=2.93, size=32))
        self.add(self.walls, self.datum, self.height_lines, self.sections, self.badges,
                 self.areas, self.pressures, self.forces, self.velocities, self.vlabels, self.hlabels)
        self.xgrid = np.linspace(self.LEFT_X, self.RIGHT_X, 401)
        areas = np.pi * np.array([self.radius(x) ** 2 for x in self.xgrid])
        cumulative = np.concatenate(([0], np.cumsum((areas[1:] + areas[:-1]) * .5 * np.diff(self.xgrid))))
        type(self)._volume_x, type(self)._volume_curve = self.xgrid, cumulative
        self.cdf = cumulative / cumulative[-1]
        assert abs(np.pi * self.R1**2 * self.L1 - np.pi * self.R2**2 * self.L2) < 1e-10

    def travel_rate(self, u):
        a = np.interp(self.INLET, self.xgrid, self.cdf)
        b = np.interp(self.OUTLET, self.xgrid, self.cdf)
        xx = np.interp(a + u * (b - a), self.cdf, self.xgrid)
        return float((xx - self.INLET) / (self.OUTLET - self.INLET))

    def displacement(self, section):
        start, length = (self.LEFT_X, self.L1) if section == 1 else (self.RIGHT_X - self.L2, self.L2)
        yy = self.cy(start + length / 2) - self.radius(start + length / 2) - .23
        arrow = Arrow([start, yy, 0], [start + length, yy, 0], color=INK, buff=0,
                      stroke_width=2, max_tip_length_to_length_ratio=.18)
        label = eq(fr"\Delta x_{section}", size=30).next_to(arrow, DOWN, buff=.1)
        return VGroup(arrow, label)


class BernoulliV2(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        config.tex_dir = UNIT / "media_preview/Tex"
        config.max_files_cached = 300
        self.marks, self.qa = {}, []
        self.current = None
        tag = text("POR TRÁS DA FÓRMULA · EP. 06", 21, PRESSURE).move_to([0, 6.85, 0])
        rule = Line([-3.8, 6.48, 0], [3.8, 6.48, 0], color=PRESSURE, stroke_width=1.2)
        brand = ImageMobject(str(WATERMARK_PATH)).set_width(1.65).move_to([0, -6.9, 0])
        self.add(tag, rule, brand)
        self.heading = text("BERNOULLI", 30).move_to([0, 5.97, 0])
        self.add(self.heading)
        self.diagram = FlowDiagram()
        self.tracker = ValueTracker(self.diagram.INLET)
        self.packet = self.diagram.parcel(self.tracker.get_value())
        self.packet.add_updater(lambda m: m.become(self.diagram.parcel(self.tracker.get_value())))
        self.dv_label = eq(r"\Delta V", x=0, y=5.32, size=38)
        self.dv_link = Line([0, 5.05, 0], self.packet.get_top(), color=VOLUME, stroke_width=1.2, stroke_opacity=.45)
        self.dv_link.add_updater(lambda m: m.put_start_and_end_on([0, 5.05, 0], self.packet.get_top()))
        self.flowdots = VGroup(*(Dot(radius=.035, color=MUTED, fill_opacity=.45) for _ in range(7)))

        def flow(m, dt):
            for i, dot in enumerate(m):
                xx = np.interp((self.time / 7 + i / 7) % 1, self.diagram.cdf, self.diagram.xgrid)
                dot.move_to(self.diagram.point(xx))
        self.flowdots.add_updater(flow)
        solid = Solido3D("tubo_escoamento", frames=30, render="nunca")
        tube3d = solid.mobject(cena=self, largura=7, centro=UP * 2.9, periodo=2)

        # 0–10: hook visual e transição sobreposta para o esquema.
        self.play(FadeIn(tube3d), run_time=.7)
        hook = eq("P", "+", r"\frac12\rho v^2", "+", r"\rho gh", y=-.6, size=56)
        question = text("Por que pressão, velocidade\ne altura aparecem juntas?", 30).move_to([0, -2.25, 0])
        self.play(Write(hook), FadeIn(question), run_time=1.2)
        self.current = hook
        self.record("hook_3d")
        self.until(8)
        tube3d.pausar()
        self.play(FadeOut(tube3d), Create(self.diagram.walls), FadeOut(question), run_time=1.3)
        self.add(self.flowdots)
        self.play(FadeIn(VGroup(*list(self.diagram)[1:])), run_time=.7)
        self.remove(self.diagram.walls, *list(self.diagram)[1:])
        self.add(self.diagram)

        # 10–23: duas representações do mesmo volume, no mesmo sistema.
        self.phase("O mesmo volume, de 1 para 2")
        self.play(FadeIn(self.packet), FadeIn(self.dv_label), Create(self.dv_link), run_time=.6)
        dx1, dx2 = self.diagram.displacement(1), self.diagram.displacement(2)
        ghost = self.diagram.parcel(self.diagram.OUTLET, opacity=.10)
        self.play(TransformFromCopy(self.packet, ghost), Create(dx1), Create(dx2), run_time=1.2)
        conservation = eq(r"\Delta V", "=", r"A_1", r"\Delta x_1", "=", r"A_2", r"\Delta x_2", y=-.5, size=46)
        self.change(conservation, hidden=(0, 2, 3, 5, 6))
        self.feed(self.dv_label, conservation[0])
        self.feed(self.diagram.areas[0], conservation[2], dx1[1], conservation[3])
        self.feed(self.diagram.areas[1], conservation[5], dx2[1], conservation[6])
        self.play(Indicate(self.packet, color=VOLUME), Indicate(ghost, color=VOLUME), run_time=1)
        self.record("duas_secoes_mesmo_volume")
        self.until(23)

        # 23–46: a face varre o cilindro que vira ΔV na equação.
        self.phase("A pressão empurra o fluido")
        self.play(FadeOut(ghost), FadeOut(dx2), self.diagram.forces[1].animate.set_opacity(.2),
                  self.diagram.pressures[1].animate.set_opacity(.3), run_time=.5)
        self.change(eq("P", "=", r"\frac{F}{A}", size=55))
        self.play(Indicate(self.diagram.sections[0], color=PRESSURE), Indicate(self.diagram.forces[0]), run_time=.8)
        force = eq(r"F_1", "=", r"P_1", r"A_1", size=59)
        self.change(force, hidden=(2, 3))
        self.feed(self.diagram.pressures[0], force[2], self.diagram.areas[0], force[3])
        self.record("forca_entrada")
        self.until(29)
        self.sweep(1, dx1)
        work = eq(r"W_1", "=", r"F_1", r"\Delta x_1", size=55)
        self.change(work, hidden=(3,))
        self.feed(dx1[1], work[3])
        self.record("avanco_entrada")
        work = eq(r"W_1", "=", r"P_1", r"A_1", r"\Delta x_1", size=53)
        self.change(work, hidden=(3, 4))
        self.feed(self.diagram.areas[0], work[3], dx1[1], work[4])
        geom = eq(r"A_1", r"\Delta x_1", "=", r"\Delta V", y=-2.45, size=42)
        self.play(Write(geom), Indicate(self.packet, color=VOLUME), run_time=.8)
        self.feed(self.dv_label, geom[3])
        self.record("volume_varrido")
        self.until(39)
        result = eq(r"W_1", "=", r"P_1", r"\Delta V", size=61)
        self.change(result, hidden=(3,))
        self.feed(self.dv_label, result[3])
        self.play(Circumscribe(result, color=PRESSURE), FadeOut(geom), run_time=.8)
        self.record("trabalho_entrada")
        self.until(46)

        # 46–60: o destaque percorre o tubo, sem mudar a composição.
        self.phase("Na saída, a pressão resiste")
        self.play(FadeOut(dx1), self.diagram.forces[0].animate.set_opacity(.25),
                  self.diagram.forces[1].animate.set_opacity(1), self.diagram.pressures[1].animate.set_opacity(1),
                  self.tracker.animate.set_value(self.diagram.OUTLET), run_time=2.1,
                  rate_func=self.diagram.travel_rate)
        f2 = eq(r"F_2", "=", r"P_2", r"A_2", size=57)
        self.change(f2, hidden=(2, 3))
        self.feed(self.diagram.pressures[1], f2[2], self.diagram.areas[1], f2[3])
        self.sweep(2, dx2)
        w2 = eq(r"W_2", "=", "-", r"F_2", r"\Delta x_2", size=52)
        self.change(w2, hidden=(4,))
        self.feed(dx2[1], w2[4])
        self.play(Indicate(self.diagram.forces[1], color=PRESSURE), Indicate(dx2[0]), run_time=.7)
        self.record("saida_sinal_negativo")
        self.change(eq(r"W_2", "=", "-", r"P_2", r"A_2", r"\Delta x_2", size=50), hidden=(4, 5))
        self.feed(self.diagram.areas[1], self.current[4], dx2[1], self.current[5])
        self.change(eq(r"W_2", "=", "-", r"P_2", r"\Delta V", size=59), hidden=(4,))
        self.feed(self.dv_label, self.current[4])
        self.record("trabalho_saida")
        self.until(60)

        # 60–69: as contribuições descem das duas seções para a soma.
        self.phase("O trabalho líquido das duas pressões")
        self.play(FadeOut(dx2), self.diagram.forces[0].animate.set_opacity(1),
                  self.diagram.pressures[0].animate.set_opacity(1), run_time=.4)
        inlet_work = eq("+", r"P_1", r"\Delta V", x=-2.25, y=1.02, size=34)
        outlet_work = eq("-", r"P_2", r"\Delta V", x=2.25, y=1.02, size=34)
        self.play(TransformFromCopy(self.diagram.pressures[0], inlet_work),
                  TransformFromCopy(self.diagram.pressures[1], outlet_work), run_time=.8)
        self.change(eq(r"W_P", "=", r"W_1", "+", r"W_2", size=54))
        net = eq(r"W_P", "=", r"P_1", r"\Delta V", "-", r"P_2", r"\Delta V", size=49)
        self.change(net, hidden=(2, 3, 4, 5, 6))
        self.feed(VGroup(*inlet_work[1:]), VGroup(net[2], net[3]), outlet_work, VGroup(net[4], net[5], net[6]))
        self.change(eq(r"W_P", "=", "(", r"P_1", "-", r"P_2", ")", r"\Delta V", size=53))
        self.record("trabalho_liquido")
        self.until(69)

        # 69–89: massa, velocidade e altura do mesmo personagem físico.
        self.phase("O trabalho muda velocidade e altura")
        self.play(FadeOut(inlet_work), FadeOut(outlet_work), run_time=.4)
        self.change(eq(r"W_P", "=", r"\Delta K", "+", r"\Delta U_g", size=54))
        self.play(Indicate(self.diagram.velocities, color=KINETIC), Indicate(self.diagram.height_lines, color=GRAVITY), run_time=.8)
        self.change(eq(r"\rho", "=", r"\frac{m}{V}", size=52))
        mass = eq("m", "=", r"\rho", r"\Delta V", size=56)
        self.change(mass, hidden=(3,))
        self.feed(self.dv_label, mass[3])
        mass_tag = eq("m", "=", r"\rho", r"\Delta V", y=-3.55, size=32)
        self.play(TransformFromCopy(mass, mass_tag), run_time=.5)
        self.packet.suspend_updating()
        self.play(FadeOut(self.packet), run_time=.2)
        self.tracker.set_value(self.diagram.INLET)
        self.packet.become(self.diagram.parcel(self.diagram.INLET))
        self.play(FadeIn(self.packet), run_time=.2)
        self.packet.resume_updating()
        k1 = eq(r"K_1", "=", r"\frac12m", r"v_1^2", x=-2.0, y=-.6, size=41, width=3.7)
        k2 = eq(r"K_2", "=", r"\frac12m", r"v_2^2", x=2.0, y=-.6, size=41, width=3.7)
        k1[3].set_opacity(0)
        k2[3].set_opacity(0)
        self.change(VGroup(k1, k2))
        self.feed(self.diagram.vlabels[0], k1[3], self.diagram.vlabels[1], k2[3])
        self.marks["pacote_em_transito"] = round(self.time + 1.05, 3)
        self.play(self.tracker.animate(rate_func=self.diagram.travel_rate).set_value(self.diagram.OUTLET),
                  Indicate(self.diagram.velocities, color=KINETIC), Indicate(self.diagram.height_lines, color=GRAVITY),
                  run_time=2.1)
        self.record("pacote_velocidade_altura")
        self.change(eq(r"\Delta K", "=", r"K_2", "-", r"K_1", size=51))
        self.change(eq(r"\Delta K", "=", r"\frac12m", "(", r"v_2^2", "-", r"v_1^2", ")", size=48))
        kinetic = eq(r"\Delta K", "=", r"\frac12\rho", r"\Delta V", "(", r"v_2^2", "-", r"v_1^2", ")", size=47, color=KINETIC)
        self.change(kinetic, hidden=(3,))
        self.feed(mass_tag[3], kinetic[3])
        self.record("variacao_cinetica")
        potential = eq(r"\Delta U_g", "=", "mg", "(", r"h_2", "-", r"h_1", ")", size=50, color=GRAVITY)
        self.change(potential, hidden=(4, 6))
        self.feed(self.diagram.hlabels[1], potential[4], self.diagram.hlabels[0], potential[6])
        potential = eq(r"\Delta U_g", "=", r"\rho g", r"\Delta V", "(", r"h_2", "-", r"h_1", ")", size=48, color=GRAVITY)
        self.change(potential, hidden=(3,))
        self.feed(mass_tag[3], potential[3])
        self.record("variacao_gravitacional")
        self.until(89)

        # 89–102: montar o balanço por origem, sem esconder o sistema.
        self.play(FadeOut(mass_tag), run_time=.3)
        self.change(eq(r"W_P", "=", r"\Delta K", "+", r"\Delta U_g", size=54))
        self.play(FadeOut(self.current), run_time=.3)
        full = self.balance(volume=True)
        self.current = full
        for row, source_pairs, physical in [
            (full[0], [(self.diagram.pressures[0], 1), (self.diagram.pressures[1], 3), (self.dv_label, 5)], self.diagram.forces),
            (full[1], [(self.diagram.vlabels[1], 3), (self.diagram.vlabels[0], 5)], self.diagram.velocities),
            (full[2], [(self.diagram.hlabels[1], 4), (self.diagram.hlabels[0], 6)], self.diagram.height_lines),
        ]:
            fed_indices = {index for _, index in source_pairs}
            for index in fed_indices:
                row[index].set_opacity(0)
            self.add(row)
            self.play(Indicate(physical), *(Write(row[i]) for i in range(len(row)) if i not in fed_indices), run_time=.8)
            for source, index in source_pairs:
                self.feed(source, row[index], duration=.55)
        self.remove(*full)
        self.add(full)
        self.record("balanco_completo")
        self.until(102)

        # 102–112: o pacote se liga aos três fatores que cancelam.
        self.phase("Um balanço por unidade de volume")
        volumes = VGroup(*(p for row in full for p in row if p.tex_string == r"\Delta V"))
        assert len(volumes) == 3
        boxes = VGroup(*(SurroundingRectangle(p, color=VOLUME, buff=.07, stroke_width=1.7) for p in volumes))
        self.play(Create(boxes), Indicate(self.packet, color=VOLUME), Indicate(self.dv_label), run_time=.9)
        division = eq(r"\div\,\Delta V\quad(\Delta V>0)", y=-3.65, size=31, color=VOLUME)
        self.play(Write(division), run_time=.6)
        slashes = VGroup(*(Line(b.get_corner(DL), b.get_corner(UR), color=VOLUME, stroke_width=2.5) for b in boxes))
        self.play(Create(slashes), run_time=.8)
        self.record("cancelamento_volume")
        self.until(106)
        self.play(FadeOut(boxes), FadeOut(slashes), FadeOut(division), run_time=.4)
        self.change(self.balance(volume=False))
        self.play(Indicate(self.dv_label, scale_factor=1.15), run_time=.7)
        self.record("balanco_por_volume")
        self.until(112)

        # 112–128: índices 1 ficam sob a seção 1; índices 2, sob a 2.
        expanded = self.expanded()
        self.change(expanded, duration=1.1)
        self.record("diferencas_abertas")
        self.until(116)
        grouped = self.states()
        links = VGroup(Line([-3.05, 2.44, 0], [-2.12, .88, 0], color=WALL, stroke_width=1.2),
                       Line([3.05, 3.85, 0], [2.12, .88, 0], color=WALL, stroke_width=1.2))
        state_labels = VGroup(text("ESTADO 1", 21).move_to([-2.12, .98, 0]), text("ESTADO 2", 21).move_to([2.12, .98, 0]))
        self.play(Create(links), FadeIn(state_labels), run_time=.7)
        # Termos completos preservam a leitura durante a troca de lado.
        # O sinal muda junto com a parcela que cruza a igualdade.
        transfers = [
            (expanded[0][0], grouped[0][0]),
            (expanded[0][2], grouped[4][0]),
            (expanded[0][3], grouped[3][0]),
            (expanded[1][2], grouped[1][1]),
            (expanded[1][1], grouped[1][0]),
            (expanded[1][0], grouped[5][1]),
            (expanded[2][3], grouped[2][1]),
            (expanded[2][2], grouped[2][0]),
            (expanded[2][1], grouped[6][1]),
            (expanded[2][0], grouped[6][0]),
        ]
        self.play(*(Transform(source, target, path_arc=PI / 8) for source, target in transfers),
                  FadeOut(expanded[0][1]), FadeIn(grouped[5][0]), run_time=3.2)
        # Transform de filhos promove esses objetos na árvore da Scene.
        # Removê-los explicitamente evita cópias órfãs nas próximas fórmulas.
        self.remove(*(source for source, _ in transfers), expanded[0][1],
                    *expanded, expanded, grouped[5][0])
        self.add(grouped)
        self.current = grouped
        self.play(Indicate(self.diagram.sections[0]), Indicate(VGroup(*grouped[:3])), run_time=1.1)
        self.play(Indicate(self.diagram.sections[1]), Indicate(VGroup(*grouped[4:])), run_time=1.1)
        self.record("agrupamento_por_estado")
        self.until(128)

        # 128–137: generalizar com o fluido ainda visível.
        self.phase("A mesma combinação na linha de corrente")
        self.play(FadeOut(links), FadeOut(state_labels), run_time=.5)
        self.change(self.bernoulli(), duration=1.5)
        short = text("Em qualquer ponto da mesma linha de corrente", 25).move_to([0, -2.7, 0])
        self.play(FadeIn(short), Circumscribe(self.current, color=INK), run_time=.8)
        self.record("bernoulli")
        self.until(137)

        # 137–148: cada parcela acende a grandeza correspondente no tubo.
        self.phase("Três termos, uma unidade")
        self.play(FadeOut(short), run_time=.3)
        captions = [
            (0, self.diagram.forces, PRESSURE, "Trabalho das forças de pressão\npor unidade de volume"),
            (2, self.diagram.velocities, KINETIC, "Energia cinética\npor unidade de volume"),
            (4, self.diagram.height_lines, GRAVITY, "Energia potencial gravitacional\npor unidade de volume"),
        ]
        for index, physical, color, caption in captions:
            label = text(caption, 26, color).move_to([0, -2.35, 0])
            self.play(Indicate(physical, color=color), Indicate(self.current[index], color=color), FadeIn(label), run_time=.7)
            self.record(["significado_pressao", "significado_cinetica", "significado_altura"][index // 2])
            self.wait(.4)
            self.play(FadeOut(label), run_time=.25)
        units = eq(r"[P]=\frac{\mathrm N}{\mathrm m^2}=\frac{\mathrm J}{\mathrm m^3}", y=-3.15, size=36)
        self.play(Write(units), run_time=.7)
        self.record("unidades")
        self.until(148)

        # 148–162: segundo uso principal do 3D; duas leis distintas.
        self.phase("Estreitamento: duas leis")
        tube3d = solid.mobject(cena=self, largura=7, centro=UP * 2.9, periodo=2)
        self.packet.suspend_updating()
        self.dv_link.suspend_updating()
        self.flowdots.suspend_updating()
        self.play(FadeOut(self.diagram), FadeOut(self.packet), FadeOut(self.dv_label), FadeOut(self.dv_link),
                  FadeOut(self.flowdots), FadeOut(units), FadeIn(tube3d), run_time=.9)
        labels3d = VGroup(text("1 · larga", 22).move_to([-2.8, 1.8, 0]), text("2 · gargalo", 22).move_to([1, 5.03, 0]),
                          Line([-2.8, 2.1, 0], [-1.9, 4.1, 0], color=WALL, stroke_width=1.2),
                          Line([.8, 4.7, 0], [-.5, 3.75, 0], color=WALL, stroke_width=1.2))
        v3d = VGroup(Arrow([-2.2, 4.05, 0], [-1.65, 3.82, 0], color=KINETIC, buff=0, stroke_width=4),
                     Arrow([-.95, 3.7, 0], [.40, 3.12, 0], color=KINETIC, buff=0, stroke_width=4))
        self.play(FadeIn(labels3d), GrowArrow(v3d[0]), GrowArrow(v3d[1]), run_time=.6)
        self.change(eq(r"A_1", r"v_1", "=", r"A_2", r"v_2", y=-.7, size=51))
        continuity = text("CONTINUIDADE", 24).move_to([0, .3, 0])
        narrow = eq(r"A_2<A_1", r"\Rightarrow", r"v_2>v_1", y=-2.25, size=45)
        self.play(FadeIn(continuity), Write(narrow), Indicate(v3d[1], color=KINETIC), run_time=.8)
        self.record("continuidade_3d")
        self.until(155)
        self.play(FadeOut(continuity), FadeOut(narrow), run_time=.3)
        bernoulli_label = text("BERNOULLI · caso ideal à mesma altura", 23).move_to([0, .3, 0])
        height = eq(r"h_1\approx h_2", y=-2.1, size=37)
        self.play(FadeIn(bernoulli_label), Write(height), run_time=.6)
        self.change(eq(r"P_1", "+", r"\frac12\rho v_1^2", "=", r"P_2", "+", r"\frac12\rho v_2^2", y=-.7, size=43))
        conclusion = eq(r"v_2>v_1", r"\Rightarrow", r"P_2<P_1", y=-3.35, size=44)
        self.play(Write(conclusion), Circumscribe(conclusion[2], color=PRESSURE), run_time=.8)
        self.record("bernoulli_estreitamento")
        self.until(162)

        # 162–168: hipóteses compactas e faixa inferior livre.
        tube3d.pausar()
        self.phase("Validade do modelo ideal")
        self.play(FadeOut(tube3d), FadeOut(labels3d), FadeOut(v3d), FadeOut(height),
                  FadeOut(conclusion), FadeOut(bernoulli_label), FadeIn(self.diagram), run_time=.7)
        self.flowdots.resume_updating()
        self.add(self.flowdots)
        self.change(self.bernoulli(), duration=.8)
        conditions = text("Incompressível · sem viscosidade\nEstacionário · mesma linha de corrente", 25).move_to([0, -2.65, 0])
        self.play(FadeIn(conditions), run_time=.6)
        self.record("hipoteses_finais")
        self.until(168)
        (UNIT / "tempos_preview_v2.json").write_text(json.dumps({
            "duracao_cena_s": round(self.time, 3), "estados": self.marks,
            "layout": self.qa, "geometria_persistente_s": [10, 148],
            "faixa_inferior_livre_ate_y": -4.25,
            "cores": {"pressao": PRESSURE, "cinetica": KINETIC, "gravitacional": GRAVITY, "volume": VOLUME},
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    def phase(self, s):
        new = text(s, 28).move_to([0, 5.97, 0])
        self.play(ReplacementTransform(self.heading, new), run_time=.3)
        self.heading = new

    def change(self, new, duration=.7, hidden=(), **kwargs):
        self.check_math(new)
        for index in hidden:
            new[index].set_opacity(0)
        if self.current is None:
            self.play(Write(new), run_time=duration)
        else:
            self.play(TransformMatchingTex(self.current, new, **kwargs), run_time=duration)
        self.current = new

    def feed(self, source, dest, source2=None, dest2=None, duration=.65):
        """Uma cópia vem da grandeza física e ocupa a parcela antes oculta."""
        pairs = [(source, dest)] + ([(source2, dest2)] if source2 is not None else [])
        travelers, targets = [], []
        for origin, target in pairs:
            wanted = target.copy().set_opacity(1)
            target.set_opacity(0)
            moving = origin.copy().clear_updaters()
            travelers.append(moving)
            targets.append(wanted)
        self.add(*travelers)
        self.play(*(Transform(m, t, path_arc=PI / 10) for m, t in zip(travelers, targets)), run_time=duration)
        for _, target in pairs:
            target.set_opacity(1)
        self.remove(*travelers)

    def sweep(self, section, displacement):
        """A frente móvel e o preenchimento varrem o volume geométrico."""
        start, length = (self.diagram.LEFT_X, self.diagram.L1) if section == 1 else (self.diagram.RIGHT_X - self.diagram.L2, self.diagram.L2)
        amount = ValueTracker(.01)
        self.packet.clear_updaters()
        self.packet.become(self.diagram.slab(start, start + .01))
        self.packet.add_updater(lambda m: m.become(self.diagram.slab(start, start + amount.get_value())))
        self.add(displacement)
        self.play(amount.animate.set_value(length), GrowArrow(displacement[0]), FadeIn(displacement[1]), run_time=1.9, rate_func=linear)
        self.packet.clear_updaters()
        self.tracker.set_value(self.diagram.INLET if section == 1 else self.diagram.OUTLET)
        self.packet.become(self.diagram.parcel(self.tracker.get_value()))
        self.packet.add_updater(lambda m: m.become(self.diagram.parcel(self.tracker.get_value())))

    def balance(self, volume):
        dv = [r"\Delta V"] if volume else []
        p = eq("(", r"P_1", "-", r"P_2", ")", *dv, "=", y=.25, size=48)
        k = eq(r"\frac12\rho", *dv, "(", r"v_2^2", "-", r"v_1^2", ")", y=-1.2, size=48, color=KINETIC)
        u = eq("+", r"\rho g", *dv, "(", r"h_2", "-", r"h_1", ")", y=-2.65, size=48, color=GRAVITY)
        return VGroup(p, k, u)

    def expanded(self):
        return VGroup(
            eq(r"P_1", "-", r"P_2", "=", y=.25, size=48),
            eq(r"\frac12\rho v_2^2", "-", r"\frac12\rho v_1^2", y=-1.2, size=48),
            eq("+", r"\rho gh_2", "-", r"\rho gh_1", y=-2.65, size=48),
        )

    def states(self):
        return VGroup(
            eq(r"P_1", x=-2.12, y=.15, size=48, width=3.4),
            eq("+", r"\frac12\rho v_1^2", x=-2.12, y=-1.2, size=47, width=3.4),
            eq("+", r"\rho gh_1", x=-2.12, y=-2.65, size=48, width=3.4),
            eq("=", x=0, y=-1.2, size=50),
            eq(r"P_2", x=2.12, y=.15, size=48, width=3.4),
            eq("+", r"\frac12\rho v_2^2", x=2.12, y=-1.2, size=47, width=3.4),
            eq("+", r"\rho gh_2", x=2.12, y=-2.65, size=48, width=3.4),
        )

    def bernoulli(self):
        return eq("P", "+", r"\frac12\rho v^2", "+", r"\rho gh", "=", r"\text{constante}", y=-.65, size=48)

    def until(self, t):
        if self.time > t + .15:
            raise ValueError(f"Bloco excedeu o tempo: {self.time:.3f} > {t}")
        if t > self.time:
            self.wait(t - self.time)

    def check_math(self, m):
        bounds = [float(m.get_left()[0]), float(m.get_right()[0]), float(m.get_bottom()[1]), float(m.get_top()[1])]
        assert bounds[0] >= -4.1 and bounds[1] <= 4.1 and bounds[2] >= -4.25 and bounds[3] <= 1.25, bounds
        self.qa.append([round(x, 3) for x in bounds])

    def record(self, name):
        self.marks[name] = round(self.time + .6, 3)
        if self.current is not None:
            self.check_math(self.current)
        self.wait(.95)
