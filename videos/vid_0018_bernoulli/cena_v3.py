"""V3 silenciosa de Bernoulli: derivar, guardar, reutilizar.

uv run python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0018_bernoulli/media_v3 -o preview_silencioso_v3 videos/vid_0018_bernoulli/cena.py BernoulliV3

Cabeçalho literal do vid_0014, trocando apenas EP. 05 → 06.
Glyph maps sobre MathTex de string única, sem índices/debug no vídeo.
"""
import json
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import *
from manim.mobject.text.tex_mobject import MathTexPart
from MF_Tools import TransformByGlyphMap

ROOT = Path(__file__).resolve().parents[2]
UNIT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from template.config import BACKGROUND_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

INK, PRESSURE = TEXT_COLOR, "#35D9FF"
BLUE, KINETIC, GRAVITY = "#267BFF", "#745CFF", "#EA63FF"
PALETTE = [BACKGROUND_COLOR, INK, PRESSURE, BLUE, KINETIC, GRAVITY]
_COUNTS = {}


@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width = config.pixel_height = 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def text(content, size=26, color=INK, opacity=1.0, t2c=None):
    # Mesmo helper tipográfico do vid_0014.
    with wide_pango():
        t = screen_text(content, size, **({"t2c": t2c} if t2c else {}))
    if not t2c:
        t.set_color(color)
    t.set_opacity(opacity)
    if t.width > 8.0:
        t.scale_to_fit_width(8.0)
    return t


def note(lines, size=27, color=INK, y=-3.15):
    return VGroup(*(text(s, size, color) for s in lines.split("\n"))).arrange(DOWN, buff=.13).move_to([0, y, 0])


class Formula(MathTex):
    """String única; parcelas nomeadas têm índices validados por contagem.

    Os glifos permanecem em self[0], conforme TransformByGlyphMap.
    MatchingTex recebe uma vista de cópias agrupadas desses mesmos glifos.
    """
    def __init__(self, *parts, size=54, width=8.0, x=0, y=-1.15, color=INK):
        self.parts_spec, self.spans = list(parts), {}
        raw = " ".join(p[1] for p in parts)
        super().__init__(raw, font_size=size, color=color)
        cursor = 0
        for key, tex in parts:
            assert key not in self.spans, key
            if tex not in _COUNTS:
                _COUNTS[tex] = len(MathTex(tex)[0])
            count = _COUNTS[tex]
            self.spans[key] = list(range(cursor, cursor + count))
            cursor += count
        assert cursor == len(self[0]), (raw, cursor, len(self[0]))
        for key, tex in parts:
            c = color
            if tex in ("=", "+", "-", "(", ")") or key.startswith("DV"):
                c = INK
            elif key.startswith(("W", "P", "F")):
                c = PRESSURE
            elif key.startswith(("K", "v", "k")):
                c = KINETIC
            elif key.startswith(("U", "h", "g")):
                c = GRAVITY
            self.term(key).set_color(c)
        if width and self.width > width:
            self.scale_to_fit_width(width)
        self.move_to([x, y, 0])

    def indices(self, keys):
        if keys is None:
            return []
        keys = [keys] if isinstance(keys, str) else keys
        return [i for key in keys for i in self.spans[key]]

    def term(self, keys):
        return VGroup(*(self[0][i] for i in self.indices(keys)))

    def rows(self, rows):
        for keys, x, y, width in rows:
            g = self.term(keys)
            if g.width > width:
                g.scale_to_fit_width(width)
            g.move_to([x, y, 0])
        return self

    def matching_view(self):
        root = VMobject()
        root.tex_string = self.tex_string
        for key, raw in self.parts_spec:
            part = MathTexPart()
            part.tex_string = raw
            part.add(*(g.copy() for g in self.term(key)))
            root.add(part)
        return root


def f(*parts, **kwargs):
    return Formula(*parts, **kwargs)


def label(tex, x, y, size=37, color=INK):
    return MathTex(tex, font_size=size, color=color).move_to([x, y, 0])


class FlowDiagram(VGroup):
    """Vista longitudinal. A=πr²; a silhueta 2D não é volume.

    O pacote conserva a integral de A(x) dx, inclusive na curva.
    Marcadores com fase uniforme nessa integral têm v proporcional a 1/A.
    """
    LEFT_X, RIGHT_X, R1, L1 = -3.15, 3.15, .72, .72

    def __init__(self):
        super().__init__()
        self.r2, self.lift = ValueTracker(.50), ValueTracker(1.0)
        self.walls = VGroup(VMobject(), VMobject())
        self.sections = VGroup(Ellipse(), Ellipse())
        self.forces = VGroup(Arrow(LEFT, RIGHT), Arrow(RIGHT, LEFT))
        self.velocities = VGroup(Arrow(LEFT, RIGHT), Arrow(LEFT, RIGHT))
        self.datum = DashedLine(LEFT, RIGHT)
        self.height_lines = VGroup(DashedLine(DOWN, UP), DashedLine(DOWN, UP))
        self.badges = VGroup(text("1", 28), text("2", 28))
        self.areas = VGroup(label(r"A_1", 0, 0), label(r"A_2", 0, 0))
        self.pressures = VGroup(label(r"P_1", 0, 0, color=PRESSURE), label(r"P_2", 0, 0, color=PRESSURE))
        self.vlabels = VGroup(label(r"v_1", 0, 0, color=KINETIC), label(r"v_2", 0, 0, color=KINETIC))
        self.hlabels = VGroup(label(r"h_1", 0, 0, color=GRAVITY), label(r"h_2", 0, 0, color=GRAVITY))
        self.add(self.walls, self.datum, self.height_lines, self.sections, self.badges,
                 self.areas, self.pressures, self.forces, self.velocities, self.vlabels, self.hlabels)
        self._shape = None
        self.refresh()
        self.add_updater(lambda m: m.refresh())

    @staticmethod
    def blend(x):
        q = np.clip((x + 1.4) / 2.8, 0, 1)
        return q * q * (3 - 2 * q)

    def cy(self, x):
        lift = self.lift.get_value()
        return 3.28 + .915 * (1 - lift) + 1.83 * lift * self.blend(x)

    def radius(self, x):
        return self.R1 + (self.r2.get_value() - self.R1) * self.blend(x)

    def point(self, x):
        return np.array([x, self.cy(x), 0.0])

    def refresh(self):
        shape = (self.r2.get_value(), self.lift.get_value())
        if shape == self._shape:
            return
        self._shape = shape
        xs = np.linspace(self.LEFT_X, self.RIGHT_X, 80)
        for wall, sign in zip(self.walls, (1, -1)):
            wall.become(VMobject(color=BLUE, stroke_width=3.2, stroke_opacity=.85).set_points_smoothly(
                [[x, self.cy(x) + sign * self.radius(x), 0] for x in xs]))
        self.datum.become(DashedLine([-3.62, 1.8, 0], [3.62, 1.8, 0], color=BLUE, stroke_width=1.2, stroke_opacity=.45))
        for i, x in enumerate((self.LEFT_X, self.RIGHT_X)):
            yy, rr = self.cy(x), self.radius(x)
            self.sections[i].become(Ellipse(width=.23, height=2 * rr, color=INK, stroke_width=2).move_to(self.point(x)))
            self.areas[i].move_to([x, yy + rr + .28, 0])
            self.badges[i].move_to([x, yy + rr + .78, 0])
            self.pressures[i].move_to([(-3.83 if i == 0 else 3.83), yy + .57, 0])
            outer, inner = (-4.14, -3.29) if i == 0 else (4.14, 3.29)
            self.forces[i].become(Arrow([outer, yy, 0], [inner, yy, 0], color=PRESSURE, buff=0,
                                        stroke_width=5.5, max_tip_length_to_length_ratio=.22))
            vx = -2.62 if i == 0 else 2.92 - .68 * (self.R1 / rr) ** 2
            vl = .68 if i == 0 else .68 * (self.R1 / rr) ** 2
            self.velocities[i].become(Arrow([vx, yy, 0], [vx + vl, yy, 0], color=KINETIC,
                                            buff=0, stroke_width=5, max_tip_length_to_length_ratio=.23))
            self.vlabels[i].move_to([vx + vl / 2, yy - rr - .35, 0])
            hx = -3.61 if i == 0 else 3.61
            self.height_lines[i].become(DashedLine([hx, 1.8, 0], [hx, yy, 0], color=GRAVITY,
                                                   stroke_width=1.8, stroke_opacity=.8))
            self.hlabels[i].move_to([(-3.96 if i == 0 else 3.96), (1.8 + yy) / 2, 0])
        self.xgrid = np.linspace(self.LEFT_X, self.RIGHT_X, 401)
        areas = np.pi * np.array([self.radius(x) ** 2 for x in self.xgrid])
        self.cumulative = np.r_[0, np.cumsum((areas[1:] + areas[:-1]) * .5 * np.diff(self.xgrid))]
        self.cdf = self.cumulative / self.cumulative[-1]

    def packet_x(self, progress):
        volume = np.pi * self.R1**2 * self.L1
        middle = volume / 2 + progress * (self.cumulative[-1] - volume)
        return float(np.interp(middle, self.cumulative, self.xgrid))

    def parcel(self, progress, fraction=1):
        volume = np.pi * self.R1**2 * self.L1
        middle = volume / 2 + progress * (self.cumulative[-1] - volume)
        start = np.interp(middle - volume / 2, self.cumulative, self.xgrid)
        end = np.interp(middle + volume / 2, self.cumulative, self.xgrid)
        return self.slab(start, start + (end - start) * max(.01, fraction))

    def slab(self, start, end):
        xs = np.linspace(start, end, 12)
        top = [[x, self.cy(x) + .90 * self.radius(x), 0] for x in xs]
        bottom = [[x, self.cy(x) - .90 * self.radius(x), 0] for x in xs[::-1]]
        body = Polygon(*top, *bottom, color=INK, stroke_width=1.5, fill_color=BLUE, fill_opacity=.30)
        caps = VGroup(*(Ellipse(width=.21, height=1.80 * self.radius(x), color=INK,
                               stroke_width=2, fill_color=BLUE, fill_opacity=.18).move_to(self.point(x))
                        for x in (start, end)))
        return VGroup(body, caps)

    def displacement(self, section):
        length = self.L1 if section == 1 else self.L1 * (self.R1 / self.r2.get_value()) ** 2
        start = self.LEFT_X if section == 1 else self.RIGHT_X - length
        yy = self.cy(start + length / 2) - self.radius(start + length / 2) - .28
        arrow = Arrow([start, yy, 0], [start + length, yy, 0], color=INK, buff=0,
                      stroke_width=2.5, max_tip_length_to_length_ratio=.2)
        lab = label(fr"\Delta x_{section}", 0, 0, size=34).next_to(arrow, DOWN, buff=.12)
        return VGroup(arrow, lab)


class BernoulliV3(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        config.tex_dir = UNIT / "media_preview/Tex"
        config.max_files_cached = 400
        self.marks, self.qa, self.glyph_steps, self.reuses = {}, [], [], []
        self.current, self.saved = None, {}
        # Cabeçalho literal do build_stage do vid_0014; somente EP alterado.
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(wm.to_corner(UP + RIGHT, buff=0.28))
        self.add(text("POR TRÁS DA FÓRMULA · EP. 06", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4))
        self.heading = text("BERNOULLI", 30).move_to([0, 6.85, 0])
        self.add(self.heading)
        self.diagram = FlowDiagram()
        self.progress, self.fill = ValueTracker(0), ValueTracker(1)
        self.packet = self.diagram.parcel(0)
        self.packet.add_updater(lambda m: m.become(self.diagram.parcel(self.progress.get_value(), self.fill.get_value())))
        self.dv_label = label(r"\Delta V", -.15, 5.85, size=43)
        self.dv_link = Line([-.15, 5.55, 0], self.packet.get_top(), color=INK, stroke_width=1.3, stroke_opacity=.45)
        self.dv_link.add_updater(lambda m: m.put_start_and_end_on([-.15, 5.55, 0], self.packet.get_top()))
        self.flowdots = VGroup(*(Dot(radius=.037, color=INK, fill_opacity=.42) for _ in range(9)))
        def flow(m, dt):
            for i, dot in enumerate(m):
                xx = np.interp((self.time / 7 + i / 9) % 1, self.diagram.cdf, self.diagram.xgrid)
                dot.move_to(self.diagram.point(xx))
        self.flowdots.add_updater(flow)

        self.play(Create(self.diagram.walls), FadeIn(VGroup(*list(self.diagram)[1:])), run_time=1.4)
        self.drop(self.diagram.walls, *list(self.diagram)[1:])
        self.add(self.diagram, self.flowdots, self.packet, self.dv_label, self.dv_link)
        self.current = self.general()
        question = note("Por que pressão, velocidade\ne altura aparecem juntas?", 31)
        self.play(Write(self.current), FadeIn(question), run_time=1.1)
        for keys, physical, color in [("P", self.diagram.forces, PRESSURE), ("k", self.diagram.velocities, KINETIC), ("g", self.diagram.height_lines, GRAVITY)]:
            self.play(Indicate(self.current.term(keys), color=color), Indicate(physical, color=color), run_time=.7)
        self.record("hook_2d", hold=1.2)
        self.play(FadeOut(question), run_time=.35)

        self.phase("Um mesmo volume de fluido")
        dx1, dx2 = self.diagram.displacement(1), self.diagram.displacement(2)
        self.play(Create(dx1), Create(dx2), run_time=.9)
        relation = f(("DV", r"\Delta V"), ("eq", "="), ("A1", r"A_1"), ("dx1", r"\Delta x_1"),
                     ("eq2", "="), ("A2", r"A_2"), ("dx2", r"\Delta x_2"), size=52)
        self.match(relation, hidden=("DV", "A1", "dx1", "A2", "dx2"))
        self.fly(self.dv_label, relation.term("DV"))
        self.fly(self.diagram.areas[0], relation.term("A1"), dx1[1], relation.term("dx1"))
        self.fly(self.diagram.areas[1], relation.term("A2"), dx2[1], relation.term("dx2"))
        self.play(Indicate(self.packet, color=INK), Indicate(VGroup(dx1, dx2), color=INK), run_time=.8)
        self.record("mesmo_volume", hold=1.6)

        self.phase("A pressão empurra o fluido")
        self.play(FadeOut(dx2), run_time=.3)
        force = f(("F1", r"F_1"), ("eq", "="), ("P1", r"P_1"), ("A1", r"A_1"), size=62)
        self.match(force, hidden=("P1", "A1"))
        pressure_arrows = VGroup(*(Arrow([-4.10, self.diagram.cy(-3.15) + d, 0], [-3.30, self.diagram.cy(-3.15) + d, 0],
                                        color=PRESSURE, buff=0, stroke_width=2.4, max_tip_length_to_length_ratio=.2) for d in (-.40, 0, .40)))
        self.play(FadeIn(pressure_arrows), Indicate(self.diagram.sections[0], color=PRESSURE), run_time=.7)
        self.fly(self.diagram.pressures[0], force.term("P1"), self.diagram.areas[0], force.term("A1"))
        self.play(Transform(pressure_arrows, self.diagram.forces[0].copy()), run_time=.75)
        self.drop(pressure_arrows)
        self.record("forca_entrada", hold=1.4)
        self.fill.set_value(.01)
        self.marks["face_varrendo_entrada"] = round(self.time + .9, 3)
        self.play(self.fill.animate(rate_func=linear).set_value(1), Indicate(dx1[0], color=INK), run_time=3.0)
        work = f(("W1", r"W_1"), ("eq", "="), ("F1", r"F_1"), ("dx1", r"\Delta x_1"), size=59)
        self.match(work, hidden=("dx1",))
        self.fly(dx1[1], work.term("dx1"))
        self.play(Indicate(self.diagram.forces[0], color=PRESSURE), Indicate(dx1[0], color=INK), run_time=.7)
        self.record("avanco_entrada", hold=1.0)
        work = f(("W1", r"W_1"), ("eq", "="), ("P1", r"P_1"), ("A1", r"A_1"), ("dx1", r"\Delta x_1"), size=57)
        self.glyph(work, [("F1", ["P1", "A1"])], "F1 para P1 A1", duration=1.2)
        geom = f(("A1", r"A_1"), ("dx1", r"\Delta x_1"), ("eq", "="), ("DV", r"\Delta V"), size=40, y=-3.05)
        for key in ("A1", "dx1", "DV"):
            geom.term(key).set_opacity(0)
        self.add(geom)
        self.play(Write(geom.term("eq")), run_time=.35)
        self.fly(self.diagram.areas[0], geom.term("A1"), dx1[1], geom.term("dx1"))
        self.fly(self.dv_label, geom.term("DV"))
        self.record("volume_varrido", hold=1.1)
        work = f(("W1", r"W_1"), ("eq", "="), ("P1", r"P_1"), ("DV", r"\Delta V"), size=63)
        self.glyph(work, [(["A1", "dx1"], "DV")], "A1 dx1 para volume", duration=1.3)
        self.play(FadeOut(geom), run_time=.3)
        self.record("trabalho_entrada", hold=1.4)
        self.store("W1", [-2.18, 1.08, 0], 3.9, PRESSURE)
        self.record("trabalho_entrada_guardado", hold=.8)

        # Um único pacote atravessa uma única vez; v e h mudam simultaneamente.
        self.phase("O trabalho muda velocidade e altura")
        self.play(FadeOut(dx1), run_time=.25)
        moving_v = self.diagram.velocities[0].copy()
        self.add(moving_v)
        def moving_arrow(m):
            xx = self.diagram.packet_x(self.progress.get_value())
            rr = self.diagram.radius(xx)
            length = .68 * (self.diagram.R1 / rr) ** 2
            m.become(Arrow(self.diagram.point(xx) + LEFT * length / 2, self.diagram.point(xx) + RIGHT * length / 2,
                           color=KINETIC, buff=0, stroke_width=5, max_tip_length_to_length_ratio=.22))
        moving_v.add_updater(moving_arrow)
        self.marks["pacote_em_transito"] = round(self.time + 2.0, 3)
        self.play(self.progress.animate(rate_func=linear).set_value(1), Indicate(self.diagram.height_lines, color=GRAVITY), run_time=4.0)
        moving_v.clear_updaters()
        self.drop(moving_v)
        self.record("pacote_mudou_velocidade_altura", hold=.8)
        self.phase("Na saída, a pressão resiste")
        self.play(Create(dx2), Indicate(self.diagram.forces[1], color=PRESSURE), run_time=.7)
        out = f(("W2", r"W_2"), ("eq", "="), ("minus", "-"), ("F2", r"F_2"), ("dx2", r"\Delta x_2"), size=58)
        self.match(out, hidden=("F2", "dx2"))
        self.fly(self.diagram.forces[1], out.term("F2"), dx2[1], out.term("dx2"))
        self.record("saida_sinal_negativo", hold=.9)
        out = f(("W2", r"W_2"), ("eq", "="), ("minus", "-"), ("P2", r"P_2"), ("A2", r"A_2"), ("dx2", r"\Delta x_2"), size=55)
        self.glyph(out, [("F2", ["P2", "A2"])], "F2 para P2 A2", duration=.9)
        out = f(("W2", r"W_2"), ("eq", "="), ("minus", "-"), ("P2", r"P_2"), ("DV", r"\Delta V"), size=61)
        self.glyph(out, [(["A2", "dx2"], "DV")], "A2 dx2 para volume", duration=1.0)
        self.record("trabalho_saida", hold=.9)
        self.store("W2", [2.18, 1.08, 0], 3.9, PRESSURE)
        self.play(FadeOut(dx2), run_time=.3)
        self.record("dois_trabalhos_guardados", hold=.8)

        self.phase("As duas pressões fazem trabalho")
        net = f(("WP", r"W_P"), ("eq", "="), ("W1", r"W_1"), ("plus", "+"), ("W2", r"W_2"), size=58)
        self.match(net, hidden=("W1", "W2"))
        self.reuse("W1", "W1", net.term("W1"))
        self.reuse("W2", "W2", net.term("W2"))
        net = f(("WP", r"W_P"), ("eq", "="), ("P1", r"P_1"), ("DV1", r"\Delta V"),
                ("minus", "-"), ("P2", r"P_2"), ("DV2", r"\Delta V"), size=55)
        self.match(net, hidden=("P1", "DV1", "minus", "P2", "DV2"))
        self.reuse("W1", ["P1", "DV"], net.term(["P1", "DV1"]))
        self.reuse("W2", ["minus", "P2", "DV"], net.term(["minus", "P2", "DV2"]))
        net = f(("WP", r"W_P"), ("eq", "="), ("lp", "("), ("P1", r"P_1"), ("minus", "-"),
                ("P2", r"P_2"), ("rp", ")"), ("DV", r"\Delta V"), size=57)
        self.glyph(net, [(["DV1", "DV2"], "DV")], "Fatorar mesmo volume nos trabalhos", duration=1.3)
        self.retire("W1", "W2")
        self.record("trabalho_liquido", hold=1.2)
        self.store("WP", [0, 1.02, 0], 7.1, PRESSURE)

        self.phase("O trabalho muda velocidade e altura")
        self.match(f(("rho", r"\rho"), ("eq", "="), ("ratio", r"\frac mV"), size=57))
        mass = f(("m", "m"), ("eq", "="), ("rho", r"\rho"), ("DV", r"\Delta V"), size=60)
        self.glyph(mass, [("ratio", ["m", "DV"])], "Densidade para massa do pacote", duration=1.1)
        self.play(Indicate(self.packet, color=INK), Indicate(mass.term("DV"), color=INK), run_time=.7)
        self.record("massa_volume", hold=1.0)
        self.store("m", [2.55, -3.60, 0], 2.9, INK, scale=.60)

        kin_states = f(("K1", r"K_1"), ("eq1", "="), ("kc1", r"\frac12m"), ("v1", r"v_1^2"),
                       ("K2", r"K_2"), ("eq2", "="), ("kc2", r"\frac12m"), ("v2", r"v_2^2"), width=None, size=48)
        kin_states.rows([(["K1", "eq1", "kc1", "v1"], -2.05, -1.2, 3.8),
                         (["K2", "eq2", "kc2", "v2"], 2.05, -1.2, 3.8)])
        self.match(kin_states, hidden=("v1", "v2"))
        self.fly(self.diagram.vlabels[0], kin_states.term("v1"), self.diagram.vlabels[1], kin_states.term("v2"))
        self.record("energias_dos_estados", hold=1.6)
        self.match(f(("K", r"\Delta K"), ("eq", "="), ("K2", r"K_2"), ("minus", "-"), ("K1", r"K_1"), size=58))
        kin = f(("K", r"\Delta K"), ("eq", "="), ("kc", r"\frac12"), ("m", "m"), ("lp", "("),
                ("v2", r"v_2^2"), ("minus", "-"), ("v1", r"v_1^2"), ("rp", ")"), size=55)
        self.match(kin, hidden=("v1", "v2"))
        self.fly(self.diagram.vlabels[0], kin.term("v1"), self.diagram.vlabels[1], kin.term("v2"))
        kin = self.kinetic()
        self.glyph(kin, [("m", ["rho", "DV"])], "m para rho volume em Delta K", duration=1.3)
        self.reuse("m", ["rho", "DV"], kin.term(["rho", "DV"]))
        self.record("variacao_cinetica", hold=1.6)
        self.store("K", [0, .14, 0], 7.5, KINETIC, scale=.68)

        potential = f(("U", r"\Delta U_g"), ("eq", "="), ("m", "m"), ("gc", "g"), ("lp", "("),
                      ("h2", r"h_2"), ("minus", "-"), ("h1", r"h_1"), ("rp", ")"), size=57, color=GRAVITY, y=-1.6)
        self.match(potential, hidden=("h1", "h2"))
        self.fly(self.diagram.hlabels[0], potential.term("h1"), self.diagram.hlabels[1], potential.term("h2"))
        self.play(Indicate(self.diagram.height_lines, color=GRAVITY), run_time=.7)
        potential = self.potential()
        self.glyph(potential, [("m", ["rho", "DV"])], "m para rho volume em Delta Ug", duration=1.3)
        self.reuse("m", ["rho", "DV"], potential.term(["rho", "DV"]))
        self.retire("m")
        self.record("variacao_gravitacional", hold=1.6)
        self.store("U", [0, -.74, 0], 7.5, GRAVITY, scale=.68)
        self.record("tres_resultados_guardados", hold=1.5)

        self.phase("Um balanço de energia")
        balance = f(("WP", r"W_P"), ("eq", "="), ("K", r"\Delta K"), ("plus", "+"), ("U", r"\Delta U_g"), size=55, y=-2.2)
        self.match(balance, hidden=("WP", "K", "U"))
        self.reuse("WP", "WP", balance.term("WP"))
        self.reuse("K", "K", balance.term("K"))
        self.reuse("U", "U", balance.term("U"))
        self.record("balanco_simbolico", hold=1.4)
        full = self.balance(True)
        travelers, destinations = [], []
        for name, source_keys, target_keys in [
            ("WP", ["lp", "P1", "minus", "P2", "rp", "DV"], ["lp", "P1", "pm", "P2", "rp", "DVp"]),
            ("K", ["kc", "rho", "DV", "lp", "v2", "minus", "v1", "rp"], ["kc", "DVk", "kl", "v2", "km", "v1", "kr"]),
            ("U", ["rho", "gc", "DV", "lp", "h2", "minus", "h1", "rp"], ["gc", "DVu", "gl", "h2", "gm", "h1", "gr"]),
        ]:
            source = self.saved.pop(name)
            travelers.append(source.term(source_keys).copy())
            destinations.append(full.term(target_keys).copy())
            full.term(target_keys).set_opacity(0)
            self.drop(source)
        # As três cópias descem juntas, preservando sua ordem vertical.
        # Os originais já consumidos não ficam sobrepostos aos objetos em voo.
        symbols = balance.copy()
        signs = full.term(["eq", "plus"]).copy()
        self.drop(balance)
        self.add(symbols, *travelers)
        self.marks["balanco_em_montagem"] = round(self.time + 2.0, 3)
        self.play(AnimationGroup(
            FadeOut(symbols, run_time=.6),
            # Mover = pela diagonal cruzaria a expressão cinética. Os dois
            # operadores conhecidos reaparecem no encaixe ao fim das cópias.
            Succession(Wait(3.4), FadeIn(signs, run_time=.6)),
            *(Transform(source, dest, run_time=4.0) for source, dest in zip(travelers, destinations)),
            lag_ratio=0), run_time=4.0)
        self.drop(symbols, signs, *travelers, full)
        full.set_opacity(1)
        self.add(full)
        self.current = full
        self.reuses.extend({"resultado": name, "destino": "balanco_expandido", "tempo": round(self.time, 3)} for name in ("WP", "K", "U"))
        self.record("balanco_completo", hold=2.6)

        self.phase("Um balanço por unidade de volume")
        dvs = [full.term(key) for key in ("DVp", "DVk", "DVu")]
        boxes = VGroup(*(SurroundingRectangle(t, color=INK, buff=.06, stroke_width=1.7) for t in dvs))
        self.play(Create(boxes), Indicate(self.packet, color=INK), Indicate(self.dv_label, color=INK), run_time=.9)
        for target in dvs:
            self.fly(self.dv_label, target, duration=.45)
        division = label(r"\div\,\Delta V\quad(\Delta V>0)", 0, -3.62, size=33)
        slashes = VGroup(*(Line(b.get_corner(DL), b.get_corner(UR), color=INK, stroke_width=2.4) for b in boxes))
        self.play(Write(division), Create(slashes), run_time=.8)
        self.record("cancelamento_volume", hold=1.2)
        self.play(FadeOut(boxes), FadeOut(slashes), FadeOut(division), run_time=.3)
        self.glyph(self.balance(False), [("DVp", None), ("DVk", None), ("DVu", None)], "Cancelar os tres volumes", duration=1.4)
        self.play(Indicate(self.dv_label, color=INK), run_time=.7)
        self.record("balanco_por_volume", hold=1.3)

        self.glyph(self.expanded(), [(["kc", "v2"], "k2"), (["kc", "v1"], "k1"),
                                    (["gc", "h2"], "g2"), (["gc", "h1"], "g1")], "Abrir diferencas copiando coeficientes", duration=1.7)
        self.record("diferencas_abertas", hold=1.7)
        links = VGroup(Line([-3.15, 2.54, 0], [-2.12, 1.28, 0], color=BLUE, stroke_width=1.4),
                       Line([3.15, 4.57, 0], [2.12, 1.28, 0], color=BLUE, stroke_width=1.4))
        states_text = VGroup(text("ESTADO 1", 24).move_to([-2.12, 1.24, 0]), text("ESTADO 2", 24).move_to([2.12, 1.24, 0]))
        self.play(Create(links), FadeIn(states_text), run_time=.6)
        # Primeiro abre espaço no lado direito e leva P2 para lá.
        # Assim os termos positivos não se cruzam com os negativos em trânsito.
        self.glyph(self.spread_states(), [("P2", "P2", {"path_arc": PI / 7}),
                                         ("k2", "k2", {"path_arc": -PI / 5}),
                                         ("pm", None), (None, "rpk")],
                   "P2 cruza a igualdade e separa os blocos", duration=1.8)
        self.marks["agrupamento_em_movimento"] = round(self.time + 1.1, 3)
        self.glyph(self.states(), [
            (["km", "k1"], ["lpk", "k1"], {"path_arc": -PI / 5}),
            (["gm", "g1"], ["lpg", "g1"], {"path_arc": -PI / 5, "delay": .9}),
            ("plus", "rpg"),
        ], "Reorganizar estados com sinais rastreaveis", duration=4.0)
        self.play(Indicate(self.diagram.sections[0], color=INK), Indicate(self.current.term(["P1", "k1", "g1"]), color=INK), run_time=.85)
        self.play(Indicate(self.diagram.sections[1], color=INK), Indicate(self.current.term(["P2", "k2", "g2"]), color=INK), run_time=.85)
        self.record("agrupamento_por_estado", hold=2.0)

        self.phase("A mesma combinação ao longo do escoamento")
        self.play(FadeOut(links), FadeOut(states_text), run_time=.4)
        self.glyph(self.general(), [("P1", "P"), ("k1", "k"), ("g1", "g"), ("lpk", "pk"), ("lpg", "pg")],
                   "Remover indices na generalizacao", duration=1.6)
        line_note = note("A mesma combinação em qualquer ponto\nda mesma linha de corrente.", 27, y=-3.05)
        self.play(FadeIn(line_note), Circumscribe(self.current, color=INK), run_time=.8)
        self.record("bernoulli", hold=1.5)
        self.play(FadeOut(line_note), run_time=.3)

        self.phase("Três termos, uma unidade")
        for key, physical, color, words, mark in [
            ("P", self.diagram.forces, PRESSURE, "Trabalho das forças de pressão\npor unidade de volume", "significado_pressao"),
            ("k", self.diagram.velocities, KINETIC, "Energia cinética\npor unidade de volume", "significado_cinetica"),
            ("g", self.diagram.height_lines, GRAVITY, "Energia potencial gravitacional\npor unidade de volume", "significado_gravitacional"),
        ]:
            caption = note(words, 27, color, y=-2.9)
            self.play(Indicate(self.current.term(key), color=color), Indicate(physical, color=color), FadeIn(caption), run_time=.7)
            self.record(mark, hold=.85)
            self.play(FadeOut(caption), run_time=.2)
        units = label(r"\frac{\mathrm N}{\mathrm m^2}=\frac{\mathrm J}{\mathrm m^3}", 0, -3.15, size=40)
        self.play(Write(units), run_time=.6)
        self.record("unidades", hold=.8)

        self.phase("Duas leis no estreitamento")
        self.play(FadeOut(units), self.diagram.lift.animate.set_value(0), self.diagram.r2.animate.set_value(.40), run_time=2.2)
        continuity = f(("A1", r"A_1"), ("v1", r"v_1"), ("eq", "="), ("A2", r"A_2"), ("v2", r"v_2"), size=58)
        self.match(continuity, hidden=("A1", "v1", "A2", "v2"))
        self.fly(self.diagram.areas[0], continuity.term("A1"), self.diagram.vlabels[0], continuity.term("v1"))
        self.fly(self.diagram.areas[1], continuity.term("A2"), self.diagram.vlabels[1], continuity.term("v2"))
        continuity_title = text("CONTINUIDADE", 26).move_to([0, .25, 0])
        narrow = label(r"A_2<A_1\;\Rightarrow\;v_2>v_1", 0, -2.65, size=43, color=KINETIC)
        self.play(FadeIn(continuity_title), Write(narrow), Indicate(self.diagram.velocities[1], color=KINETIC), run_time=.8)
        continuity_note = note("Continuidade explica o aumento da velocidade.", 25, y=-3.65)
        self.play(FadeIn(continuity_note), run_time=.3)
        self.record("continuidade_2d", hold=1.3)
        self.play(FadeOut(continuity_title), FadeOut(narrow), FadeOut(continuity_note), run_time=.25)
        same_height = label(r"h_1\simeq h_2", 0, .25, size=38, color=GRAVITY)
        self.play(Write(same_height), Indicate(self.diagram.height_lines, color=GRAVITY), run_time=.6)
        horizontal = f(("P1", r"P_1"), ("pk1", "+"), ("k1", r"\frac12\rho v_1^2"), ("eq", "="),
                       ("P2", r"P_2"), ("pk2", "+"), ("k2", r"\frac12\rho v_2^2"), size=51)
        self.match(horizontal)
        bernoulli_title = text("BERNOULLI · caso ideal à mesma altura", 24).move_to([0, -.15, 0])
        conclusion = label(r"v_2>v_1\;\Rightarrow\;P_2<P_1", 0, -2.65, size=45, color=PRESSURE)
        self.play(FadeIn(bernoulli_title), Write(conclusion), Indicate(self.diagram.pressures[1], color=PRESSURE), run_time=.9)
        case_note = note("Neste caso ideal: velocidade maior, pressão menor.", 25, y=-3.65)
        self.play(FadeIn(case_note), run_time=.3)
        self.record("bernoulli_estreitamento", hold=1.5)

        self.phase("Quando Bernoulli vale?")
        self.play(FadeOut(bernoulli_title), FadeOut(conclusion), FadeOut(same_height), FadeOut(case_note), run_time=.35)
        self.match(self.general(), duration=1.0)
        hypotheses = note("Incompressível · sem viscosidade\nEstacionário · mesma linha de corrente", 28, y=-3.0)
        self.play(FadeIn(hypotheses), run_time=.6)
        self.record("hipoteses_finais", hold=1.7)
        assert self.time < 180, self.time
        (UNIT / "tempos_preview_v3.json").write_text(json.dumps({
            "duracao_cena_s": round(self.time, 3), "estados": self.marks,
            "layout": self.qa, "glyph_maps": self.glyph_steps, "reutilizacoes": self.reuses,
            "paleta": PALETTE, "solido_3d": "nenhum", "faixa_inferior_livre_ate_y": -4.25,
            "cabecalho": "vid_0014.build_stage; somente EP alterado",
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    def drop(self, *mobs):
        # Inclui filhos promovidos por AnimationGroup / MatchingTex.
        self.remove(*(member for mob in mobs for member in mob.get_family()))

    def phase(self, content):
        self.play(Transform(self.heading, text(content, 28).move_to([0, 6.85, 0])), run_time=.35)

    def match(self, new, duration=.9, hidden=()):
        self.check_math(new)
        for key in hidden:
            new.term(key).set_opacity(0)
        if self.current is None:
            self.play(Write(new), run_time=duration)
        else:
            old = self.current
            a, b = old.matching_view(), new.matching_view()
            self.drop(old)
            self.add(a)
            self.play(TransformMatchingTex(a, b), run_time=duration)
            self.drop(a, b)
            self.add(new)
        self.current = new

    def glyph(self, new, maps, reason, duration=1.2):
        self.check_math(new)
        old, entries, used_a, used_b = self.current, [], set(), set()
        for mapping in maps:
            a, b = mapping[:2]
            opts = mapping[2] if len(mapping) == 3 else {}
            ai, bi = old.indices(a), new.indices(b)
            entries.append((ai, bi, dict(opts)))
            used_a.update(ai)
            used_b.update(bi)
        raw_new = dict(new.parts_spec)
        for key, raw in old.parts_spec:
            if key in raw_new and raw_new[key] == raw:
                ai, bi = old.indices(key), new.indices(key)
                if not used_a.intersection(ai) and not used_b.intersection(bi):
                    entries.append((ai, bi))
                    used_a.update(ai)
                    used_b.update(bi)
        animation = TransformByGlyphMap(old, new, *entries, auto_fade=True, printing=False)
        assert not animation.show_indices
        self.play(animation, run_time=duration)
        self.drop(old, new)
        self.add(new)
        self.current = new
        self.glyph_steps.append({"transformacao": reason, "tempo": round(self.time, 3)})

    def fly(self, source, target, source2=None, target2=None, duration=1.0):
        pairs = [(source, target)] + ([(source2, target2)] if source2 is not None else [])
        travelers, destinations = [], []
        for origin, dest in pairs:
            destinations.append(dest.copy().set_opacity(1))
            dest.set_opacity(0)
            existing = {id(g) for root in self.mobjects for g in root.get_family()}
            if not any(id(g) in existing for g in dest.family_members_with_points()):
                self.add(dest)
            travelers.append(origin.copy().clear_updaters())
        self.add(*travelers)
        self.play(*(Transform(a, b, path_arc=PI / 10) for a, b in zip(travelers, destinations)), run_time=duration)
        for _, dest in pairs:
            dest.set_opacity(1)
        self.drop(*travelers)

    def store(self, name, position, width, color, scale=.65):
        mob = self.current
        self.play(Circumscribe(mob, color=color, stroke_width=1.8), run_time=.7)
        target = mob.copy().scale(scale)
        if target.width > width:
            target.scale_to_fit_width(width)
        target.move_to(position)
        self.play(Transform(mob, target), run_time=1.0)
        self.saved[name], self.current = mob, None
        self.check_math(mob)

    def reuse(self, name, keys, target):
        self.fly(self.saved[name].term(keys), target, duration=1.0)
        self.reuses.append({"resultado": name, "destino": "equacao_atual", "tempo": round(self.time, 3)})

    def retire(self, *names):
        mobs = [self.saved.pop(name) for name in names]
        self.play(*(FadeOut(mob, shift=UP * .10) for mob in mobs), run_time=.35)
        self.drop(*mobs)

    def record(self, name, hold=1.0):
        self.marks[name] = round(self.time + .35, 3)
        if self.current is not None:
            self.check_math(self.current)
        self.wait(hold)

    def check_math(self, mob):
        bounds = [float(mob.get_left()[0]), float(mob.get_right()[0]), float(mob.get_bottom()[1]), float(mob.get_top()[1])]
        assert bounds[0] >= -4.18 and bounds[1] <= 4.18 and bounds[2] >= -4.25 and bounds[3] <= 1.65, bounds
        self.qa.append([round(x, 3) for x in bounds])

    def kinetic(self):
        return f(("K", r"\Delta K"), ("eq", "="), ("kc", r"\frac12"), ("rho", r"\rho"), ("DV", r"\Delta V"),
                 ("lp", "("), ("v2", r"v_2^2"), ("minus", "-"), ("v1", r"v_1^2"), ("rp", ")"), size=54, color=KINETIC, y=-1.6)

    def potential(self):
        return f(("U", r"\Delta U_g"), ("eq", "="), ("rho", r"\rho"), ("gc", "g"), ("DV", r"\Delta V"),
                 ("lp", "("), ("h2", r"h_2"), ("minus", "-"), ("h1", r"h_1"), ("rp", ")"), size=55, color=GRAVITY, y=-1.6)

    def balance(self, volume):
        pv = [("DVp", r"\Delta V")] if volume else []
        kv = [("DVk", r"\Delta V")] if volume else []
        gv = [("DVu", r"\Delta V")] if volume else []
        p = ["lp", "P1", "pm", "P2", "rp"] + (["DVp"] if volume else []) + ["eq"]
        k = ["kc"] + (["DVk"] if volume else []) + ["kl", "v2", "km", "v1", "kr"]
        g = ["plus", "gc"] + (["DVu"] if volume else []) + ["gl", "h2", "gm", "h1", "gr"]
        result = f(("lp", "("), ("P1", r"P_1"), ("pm", "-"), ("P2", r"P_2"), ("rp", ")"), *pv, ("eq", "="),
                   ("kc", r"\frac12\rho"), *kv, ("kl", "("), ("v2", r"v_2^2"), ("km", "-"), ("v1", r"v_1^2"), ("kr", ")"),
                   ("plus", "+"), ("gc", r"\rho g"), *gv, ("gl", "("), ("h2", r"h_2"), ("gm", "-"), ("h1", r"h_1"), ("gr", ")"),
                   size=51, width=None)
        return result.rows([(p, 0, .55, 7.9), (k, 0, -.85, 7.9), (g, 0, -2.25, 7.9)])

    def expanded(self):
        result = f(("P1", r"P_1"), ("pm", "-"), ("P2", r"P_2"), ("eq", "="),
                   ("k2", r"\frac12\rho v_2^2"), ("km", "-"), ("k1", r"\frac12\rho v_1^2"),
                   ("plus", "+"), ("g2", r"\rho gh_2"), ("gm", "-"), ("g1", r"\rho gh_1"), size=51, width=None)
        return result.rows([(["P1", "pm", "P2", "eq"], 0, .55, 7.9),
                            (["k2", "km", "k1"], 0, -.85, 7.9),
                            (["plus", "g2", "gm", "g1"], 0, -2.25, 7.9)])

    def states(self):
        result = f(("P1", r"P_1"), ("lpk", "+"), ("k1", r"\frac12\rho v_1^2"), ("lpg", "+"), ("g1", r"\rho gh_1"),
                   ("eq", "="), ("P2", r"P_2"), ("rpk", "+"), ("k2", r"\frac12\rho v_2^2"), ("rpg", "+"), ("g2", r"\rho gh_2"), size=52, width=None)
        return result.rows([(["P1"], -2.12, .55, 3.65), (["lpk", "k1"], -2.12, -.85, 3.65), (["lpg", "g1"], -2.12, -2.25, 3.65),
                            (["eq"], 0, -.85, 1), (["P2"], 2.12, .55, 3.65), (["rpk", "k2"], 2.12, -.85, 3.65), (["rpg", "g2"], 2.12, -2.25, 3.65)])

    def spread_states(self):
        result = f(("P1", r"P_1"), ("eq", "="), ("P2", r"P_2"),
                   ("rpk", "+"), ("k2", r"\frac12\rho v_2^2"), ("km", "-"), ("k1", r"\frac12\rho v_1^2"),
                   ("plus", "+"), ("g2", r"\rho gh_2"), ("gm", "-"), ("g1", r"\rho gh_1"), size=48, width=None)
        return result.rows([(["P1"], -2.12, .55, 3.65), (["eq"], 0, -.85, 1), (["P2"], 2.12, .55, 3.65),
                            (["rpk", "k2"], 2.12, -.55, 3.65), (["km", "k1"], 2.12, -1.62, 3.65),
                            (["plus", "g2"], 2.12, -2.60, 3.65), (["gm", "g1"], 2.12, -3.55, 3.65)])

    def general(self):
        return f(("P", "P"), ("pk", "+"), ("k", r"\frac12\rho v^2"), ("pg", "+"), ("g", r"\rho gh"),
                 ("eq", "="), ("constant", r"\text{constante}"), size=55)
