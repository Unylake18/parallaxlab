"""V4 silenciosa de Bernoulli: símbolos físicos e destinos algébricos estáveis.

uv run python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0018_bernoulli/media_v4 -o preview_silencioso_v4 videos/vid_0018_bernoulli/cena.py BernoulliV4

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
        if all(isinstance(key, int) for key in keys):
            return list(keys)
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


def label(tex, x, y, size=41, color=INK):
    return MathTex(tex, font_size=size, color=color).move_to([x, y, 0])


class FlowDiagram(VGroup):
    """Vista longitudinal. A=πr²; a silhueta 2D não é volume.

    O pacote conserva a integral de A(x) dx, inclusive na curva.
    Marcadores com fase uniforme nessa integral têm v proporcional a 1/A.
    """
    LEFT_X, RIGHT_X, R1, L1 = -3.35, 3.35, .80, .84

    def __init__(self):
        super().__init__()
        self.r2, self.lift = ValueTracker(.555), ValueTracker(1.0)
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
        return 3.15 + .99 * (1 - lift) + 1.98 * lift * self.blend(x)

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
        self.datum.become(DashedLine([-3.72, 1.5, 0], [3.72, 1.5, 0], color=BLUE, stroke_width=1.2, stroke_opacity=.45))
        for i, x in enumerate((self.LEFT_X, self.RIGHT_X)):
            yy, rr = self.cy(x), self.radius(x)
            self.sections[i].become(Ellipse(width=.23, height=2 * rr, color=INK, stroke_width=2).move_to(self.point(x)))
            self.areas[i].move_to([x, yy + rr + .28, 0])
            self.badges[i].move_to([x, yy + rr + .73, 0])
            self.pressures[i].move_to([(-3.94 if i == 0 else 3.94), yy + .50, 0])
            outer, inner = (-4.14, -3.45) if i == 0 else (4.14, 3.45)
            self.forces[i].become(Arrow([outer, yy, 0], [inner, yy, 0], color=PRESSURE, buff=0,
                                        stroke_width=5.5, max_tip_length_to_length_ratio=.22))
            vx = -2.22 if i == 0 else 3.05 - .68 * (self.R1 / rr) ** 2
            vl = .68 if i == 0 else .68 * (self.R1 / rr) ** 2
            self.velocities[i].become(Arrow([vx, yy, 0], [vx + vl, yy, 0], color=KINETIC,
                                            buff=0, stroke_width=5, max_tip_length_to_length_ratio=.23))
            self.vlabels[i].move_to([vx + vl / 2, yy - rr - .34, 0])
            hx = -3.72 if i == 0 else 3.72
            self.height_lines[i].become(DashedLine([hx, 1.5, 0], [hx, yy, 0], color=GRAVITY,
                                                   stroke_width=1.8, stroke_opacity=.8))
            self.hlabels[i].move_to([(-4.02 if i == 0 else 4.02), (1.5 + yy) / 2, 0])
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

    def displacement(self, section, fraction=1):
        length = self.L1 if section == 1 else self.L1 * (self.R1 / self.r2.get_value()) ** 2
        start = self.LEFT_X if section == 1 else self.RIGHT_X - length
        yy = self.cy(start + length / 2) - self.radius(start + length / 2) - (.18 if section == 1 else .70)
        end = start + max(.10, length * fraction)
        brace = BraceBetweenPoints([start, yy, 0], [end, yy, 0], direction=DOWN, color=INK, buff=0)
        lab = label(fr"\Delta x_{section}", 0, 0, size=37).next_to(brace, DOWN, buff=.09)
        return VGroup(brace, lab)


class BernoulliV4(Scene):
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
        self.dv_label = label(r"\Delta V", -.15, 5.95, size=47)
        self.dv_link = Line([-.15, 5.65, 0], self.packet.get_top(), color=INK, stroke_width=1.3, stroke_opacity=.45)
        self.dv_link.add_updater(lambda m: m.put_start_and_end_on([-.15, 5.65, 0], self.packet.get_top()))
        self.flowdots = VGroup(*(Dot(radius=.047, color=INK, fill_opacity=.55) for _ in range(9)))
        def flow(m, dt):
            for i, dot in enumerate(m):
                xx = np.interp((self.time / 7 + i / 9) % 1, self.diagram.cdf, self.diagram.xgrid)
                dot.move_to(self.diagram.point(xx))
        self.flowdots.add_updater(flow)

        self.play(Create(self.diagram.walls), FadeIn(VGroup(*list(self.diagram)[1:])), run_time=1.4)
        self.drop(self.diagram.walls, *list(self.diagram)[1:])
        self.add(self.diagram, self.flowdots, self.packet, self.dv_label, self.dv_link)
        self.current = self.general()
        question = note("Por que pressão, velocidade e altura\naparecem somadas?", 30)
        for key in ("P", "k", "g"):
            self.current.term(key).set_opacity(0)
        self.add(self.current)
        self.fly(self.diagram.pressures[0], self.current.term("P"), duration=.7)
        self.fly(self.diagram.vlabels[1], self.current.term("k"),
                 self.diagram.hlabels[1], self.current.term("g"), duration=.9)
        self.play(FadeIn(question), Indicate(self.diagram.velocities[1], color=KINETIC), run_time=.7)
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
        # Face inicial fixa; a segunda avança e o brace mede o volume varrido.
        dx1.add_updater(lambda m: m.become(self.diagram.displacement(1, self.fill.get_value())))
        initial_face = self.diagram.sections[0].copy().clear_updaters().set_opacity(.35)
        self.add(initial_face)
        self.dv_label.set_opacity(0)
        self.marks["face_varrendo_entrada"] = round(self.time + .9, 3)
        self.play(self.fill.animate(rate_func=linear).set_value(1), run_time=3.0)
        dx1.clear_updaters()
        self.dv_label.set_opacity(1)
        self.play(FadeIn(self.dv_label), run_time=.4)
        self.drop(initial_face)
        work = f(("W1", r"W_1"), ("eq", "="), ("F1", r"F_1"), ("dx1", r"\Delta x_1"), size=59)
        self.match(work, hidden=("dx1",))
        self.fly(dx1[1], work.term("dx1"))
        self.play(Indicate(self.diagram.forces[0], color=PRESSURE), Indicate(dx1[0], color=INK), run_time=.7)
        self.record("avanco_entrada", hold=1.0)
        work = f(("W1", r"W_1"), ("eq", "="), ("P1", r"P_1"), ("A1", r"A_1"), ("dx1", r"\Delta x_1"), size=57)
        self.substitute(work, "F1", [(self.diagram.pressures[0], "P1"), (self.diagram.areas[0], "A1")],
                        "F1 recebe P1 A1 da face de entrada", duration=1.45)
        geom = f(("A1", r"A_1"), ("dx1", r"\Delta x_1"), ("eq", "="), ("DV", r"\Delta V"), size=48, y=-3.05)
        for key in ("A1", "dx1", "DV"):
            geom.term(key).set_opacity(0)
        self.add(geom)
        self.play(Write(geom.term("eq")), run_time=.35)
        self.fly(self.diagram.areas[0], geom.term("A1"), dx1[1], geom.term("dx1"))
        self.play(Indicate(self.packet, color=BLUE, scale_factor=1.04), run_time=.5)
        self.fly(self.dv_label, geom.term("DV"), duration=.7)
        self.record("volume_varrido", hold=1.1)
        work = f(("W1", r"W_1"), ("eq", "="), ("P1", r"P_1"), ("DV", r"\Delta V"), size=63)
        self.substitute(work, ["A1", "dx1"], [(geom.term("DV"), "DV")],
                        "A1 dx1 recebe o volume varrido", duration=1.3)
        self.play(FadeOut(geom), run_time=.3)
        self.record("trabalho_entrada", hold=1.4)
        self.store("W1", [-2.18, 1.08, 0], 3.9, PRESSURE)
        self.record("trabalho_entrada_guardado", hold=.8)

        # Um único pacote atravessa uma única vez; v e h mudam simultaneamente.
        self.phase("O trabalho muda a energia mecânica")
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
        self.substitute(out, "F2", [(self.diagram.pressures[1], "P2"), (self.diagram.areas[1], "A2")],
                        "F2 recebe P2 A2 da face de saida", duration=1.2)
        out = f(("W2", r"W_2"), ("eq", "="), ("minus", "-"), ("P2", r"P_2"), ("DV", r"\Delta V"), size=61)
        self.substitute(out, ["A2", "dx2"], [(self.dv_label, "DV")],
                        "A2 dx2 recebe o mesmo volume", duration=1.1)
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
        self.glyph(net, [("DV1", "DV", {"path_arc": PI / 2}), ("DV2", None, {"scale": .1}),
                         (None, ["lp", "rp"], {"delay": .6})], "Fatorar volume por uma rota abaixo da expressao", duration=1.3)
        self.retire("W1", "W2")
        self.record("trabalho_liquido", hold=1.2)
        self.store("WP", [0, 1.02, 0], 7.1, PRESSURE)

        self.phase("O trabalho muda a energia mecânica")
        density = label(r"\rho", .85, 5.95, size=46)
        self.play(FadeIn(density), Indicate(self.packet, color=BLUE, scale_factor=1.04), run_time=.65)
        mass = f(("m", "m"), ("eq", "="), ("rho", r"\rho"), ("DV", r"\Delta V"), size=60)
        self.match(mass, hidden=("rho", "DV"), duration=.5)
        self.fly(density, mass.term("rho"), self.dv_label, mass.term("DV"), duration=.9)
        self.play(FadeOut(density), run_time=.2)
        self.record("massa_volume", hold=1.0)
        # A ferramenta de massa fica junto ao pacote, acima das energias.
        self.play(self.saved["WP"].animate.move_to([-1.85, 1.02, 0]), run_time=.5)
        self.store("m", [2.25, 1.02, 0], 3.4, INK)

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
        self.substitute(kin, "m", [(self.saved["m"].term(["rho", "DV"]), ["rho", "DV"])],
                        "Massa guardada substitui m em Delta K", duration=1.7, memory="m")
        self.record("variacao_cinetica", hold=1.6)
        self.store("K", [0, .14, 0], 7.5, KINETIC, scale=.68)

        potential = f(("U", r"\Delta U_g"), ("eq", "="), ("m", "m"), ("gc", "g"), ("lp", "("),
                      ("h2", r"h_2"), ("minus", "-"), ("h1", r"h_1"), ("rp", ")"), size=57, color=GRAVITY, y=-1.6)
        self.match(potential, hidden=("h1", "h2"))
        self.fly(self.diagram.hlabels[0], potential.term("h1"), self.diagram.hlabels[1], potential.term("h2"))
        self.play(Indicate(self.diagram.height_lines, color=GRAVITY), run_time=.7)
        potential = self.potential()
        self.substitute(potential, "m", [(self.saved["m"].term(["rho", "DV"]), ["rho", "DV"])],
                        "Massa guardada substitui m em Delta Ug", duration=1.7, memory="m")
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
        self.marks["balanco_em_montagem"] = round(self.time + 1.4, 3)
        self.play(AnimationGroup(
            FadeOut(symbols, run_time=.6),
            # Mover = pela diagonal cruzaria a expressão cinética. Os dois
            # operadores conhecidos reaparecem no encaixe ao fim das cópias.
            Succession(Wait(2.2), FadeIn(signs, run_time=.6)),
            *(Transform(source, dest, run_time=2.8) for source, dest in zip(travelers, destinations)),
            lag_ratio=0), run_time=2.8)
        self.drop(symbols, signs, *travelers, full)
        full.set_opacity(1)
        self.add(full)
        self.current = full
        self.reuses.extend({"resultado": name, "destino": "balanco_expandido", "tempo": round(self.time, 3)} for name in ("WP", "K", "U"))
        self.record("balanco_completo", hold=2.6)

        self.phase("Um balanço por unidade de volume")
        dvs = [full.term(key) for key in ("DVp", "DVk", "DVu")]
        common = VGroup(*(Line(a.get_bottom() + DOWN * .08, b.get_top() + UP * .08,
                              color=INK, stroke_width=1.0, stroke_opacity=.25)
                          for a, b in zip(dvs, dvs[1:])))
        division = note("Mesmo ΔV > 0: dividimos todo o balanço.", 27, y=-3.55)
        self.play(Create(common), FadeIn(division),
                  *(Indicate(t, color=INK, scale_factor=1.12) for t in dvs),
                  Indicate(self.packet, color=BLUE, scale_factor=1.04),
                  Indicate(self.dv_label, color=INK), run_time=1.0)
        self.record("cancelamento_volume", hold=.8)
        self.play(FadeOut(common), run_time=.25)
        self.marks["volumes_encolhendo"] = round(self.time + .5, 3)
        self.glyph(self.balance(False), [(key, None, {"scale": .05}) for key in ("DVp", "DVk", "DVu")],
                   "Dividir pelo mesmo volume: tres fatores encolhem juntos", duration=1.1)
        self.play(FadeOut(division), run_time=.25)
        self.record("balanco_por_volume", hold=1.3)

        expanded = self.expanded()
        expanded.term(["k2", "km", "k1"]).move_to([0, -1.35, 0])
        expanded.term(["plus", "g2", "gm", "g1"]).move_to([0, -3.05, 0])
        distribution = []
        for coefficient, left, right, left_target, right_target in (("kc", "v2", "v1", "k2", "k1"), ("gc", "h2", "h1", "g2", "g1")):
            count = len(self.current.indices(coefficient))
            left_ids, right_ids = expanded.indices(left_target), expanded.indices(right_target)
            distribution.extend([(self.current.indices(coefficient), left_ids[:count]),
                                 (self.current.indices(left), left_ids[count:]),
                                 (self.current.indices(coefficient), right_ids[:count], {"path_arc": -PI / 1.1 if coefficient == "kc" else PI / 2}),
                                 (self.current.indices(right), right_ids[count:])])
        distribution.extend((key, None, {"run_time": .25}) for key in ("lp", "rp", "kl", "kr", "gl", "gr"))
        self.glyph(expanded, distribution, "Distribuir coeficientes por rotas separadas das velocidades e alturas", duration=1.7)
        self.record("diferencas_abertas", hold=1.2)
        links = VGroup(Line([-3.35, 2.30, 0], [-2.12, 1.40, 0], color=BLUE, stroke_width=1.2, stroke_opacity=.5),
                       Line([3.35, 4.50, 0], [2.12, 1.40, 0], color=BLUE, stroke_width=1.2, stroke_opacity=.5))
        states_text = VGroup(text("ESTADO 1", 24).move_to([-2.12, 1.24, 0]), text("ESTADO 2", 24).move_to([2.12, 1.24, 0]))
        slots = VGroup(*(Line([x - 1.58, y - .39, 0], [x + 1.58, y - .39, 0],
                              color=BLUE, stroke_width=1.0, stroke_opacity=.25)
                         for x in (-2.12, 2.12) for y in (.55, -.85, -2.25)))
        self.play(Create(links), FadeIn(states_text), Create(slots), run_time=.6)
        pending = self.expanded()
        pending.term(["km", "k1"]).move_to([2.12, -1.62, 0])
        pending.term(["gm", "g1"]).move_to([2.12, -3.55, 0])
        self.glyph(pending, [(["km", "k1"], ["km", "k1"]), (["gm", "g1"], ["gm", "g1"])],
                   "Separar primeiro os termos negativos em espera", duration=.8)
        self.glyph(self.state_stage(0), [("eq", "eq"), ("k2", "k2", {"path_arc": -PI / 3}), (["plus", "g2"], ["plus", "g2"])],
                   "Preparar destinos livres por estado; igualdade fixa daqui em diante", duration=.9)
        self.marks["P2_atravessando"] = round(self.time + .65, 3)
        self.glyph(self.state_stage(1), [("P2", "P2", {"path_arc": PI / 9}),
                                        ("pm", None, {"scale": .1}),
                                        (None, "rpk", {"delay": .65})],
                   "P2 atravessa: menos P2 vira mais P2 no estado 2", duration=1.3)
        self.marks["agrupamento_em_movimento"] = round(self.time + .9, 3)
        self.glyph(self.state_stage(2), [("k1", "k1", {"path_arc": -PI / 7}),
                                        ("km", None, {"scale": .1}),
                                        (None, "lpk", {"delay": .7})],
                   "Cinetica 1 atravessa sozinha e muda de sinal", duration=1.7)
        self.marks["altura_atravessando"] = round(self.time + .9, 3)
        self.glyph(self.state_stage(3), [("g1", "g1", {"path_arc": -PI / 9}),
                                        ("gm", None, {"scale": .1}),
                                        (None, "lpg", {"delay": .7})],
                   "Gravitacional 1 atravessa sozinha e muda de sinal", duration=1.7)
        self.glyph(self.states(), [("plus", "rpg")], "Encaixar termos nos slots definitivos", duration=.65)
        self.play(Indicate(self.current.term(["P1", "k1", "g1"]), color=INK, scale_factor=1.04),
                  Indicate(self.current.term(["P2", "k2", "g2"]), color=INK, scale_factor=1.04), run_time=.7)
        self.record("agrupamento_por_estado", hold=1.8)

        self.phase("A mesma combinação ao longo do escoamento")
        self.play(FadeOut(links), FadeOut(states_text), FadeOut(slots), run_time=.3)
        columns = self.general_columns()
        maps = [("lpk", "pk"), ("lpg", "pg"),
                (["P2", "rpk", "k2", "rpg", "g2"], None, {"scale": .15}),
                (None, "constant", {"delay": .6})]
        for a, b in (("P1", "P"), ("k1", "k"), ("g1", "g")):
            old_ids = self.current.indices(a)
            assert len(old_ids) == len(columns.indices(b)) + 1
            maps.extend([(old_ids[:-1], columns.indices(b)), ([old_ids[-1]], None, {"scale": .1})])
        tracer = Dot(self.diagram.point(self.diagram.LEFT_X), radius=.08, color=INK)
        line = VMobject().set_points_smoothly([self.diagram.point(x) for x in np.linspace(-3.35, 3.35, 80)])
        self.add(tracer)
        self.glyph(columns, maps, "Indices desaparecem; a outra soma representa C", duration=1.3,
                   extra=[MoveAlongPath(tracer, line, rate_func=linear)])
        self.glyph(self.general("C"), [(["pk", "k"], ["pk", "k"], {"run_time": .55}),
                                       ("P", "P", {"delay": .4, "path_arc": PI / 4}),
                                       (["pg", "g"], ["pg", "g"], {"delay": .4, "path_arc": PI / 4})],
                   "A quantidade conservada ocupa uma unica linha sem cruzar parcelas", duration=1.2)
        self.glyph(self.general(), [("constant", None, {"scale": .1}), (None, "constant", {"delay": .35})],
                   "C recebe o nome constante", duration=.7)
        self.drop(tracer)
        line_note = note("A mesma combinação em qualquer ponto\nda mesma linha de corrente.", 27, y=-3.05)
        self.play(FadeIn(line_note), Circumscribe(self.current, color=INK), run_time=.8)
        self.record("bernoulli", hold=1.0)
        self.play(FadeOut(line_note), run_time=.3)

        self.phase("Três termos, uma unidade")
        caption = note("Trabalho das forças de pressão\npor unidade de volume", 29, PRESSURE, y=-2.8)
        self.add(caption)
        for key, physical, color, words, mark in [
            ("P", self.diagram.forces, PRESSURE, "Trabalho das forças de pressão\npor unidade de volume", "significado_pressao"),
            ("k", self.diagram.velocities, KINETIC, "Energia cinética\npor unidade de volume", "significado_cinetica"),
            ("g", self.diagram.height_lines, GRAVITY, "Energia potencial gravitacional\npor unidade de volume", "significado_gravitacional"),
        ]:
            self.play(Indicate(self.current.term(key), color=color), Indicate(physical, color=color, scale_factor=1.07),
                      Transform(caption, note(words, 29, color, y=-2.8)), run_time=.75)
            self.record(mark, hold=1.0)
        units = label(r"[P]=\frac{\mathrm N}{\mathrm m^2}=\frac{\mathrm J}{\mathrm m^3}", 0, -2.65, size=54)
        unit_note = note("Todos os termos são energia por volume.", 28, y=-3.7)
        self.play(FadeOut(caption), Write(units), FadeIn(unit_note), run_time=.7)
        self.record("unidades", hold=1.0)

        self.phase("Duas leis no estreitamento")
        self.marks["tubo_em_estreitamento"] = round(self.time + 1.2, 3)
        self.play(FadeOut(units), FadeOut(unit_note), self.diagram.lift.animate.set_value(0), self.diagram.r2.animate.set_value(.44), run_time=2.5)
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
        same_height.move_to([0, 1.12, 0])
        self.match(self.states(), duration=.65)
        self.play(Indicate(self.current.term("g1"), color=GRAVITY), Indicate(self.current.term("g2"), color=GRAVITY), run_time=.6)
        horizontal = f(("P1", r"P_1"), ("lpk", "+"), ("k1", r"\frac12\rho v_1^2"), ("eq", "="),
                       ("P2", r"P_2"), ("rpk", "+"), ("k2", r"\frac12\rho v_2^2"), size=52, width=None)
        horizontal.rows([(["P1"], -2.12, .35, 3.65), (["lpk", "k1"], -2.12, -.85, 3.65),
                         (["eq"], 0, -.85, 1), (["P2"], 2.12, .35, 3.65), (["rpk", "k2"], 2.12, -.85, 3.65)])
        self.glyph(horizontal, [(["lpg", "g1"], None, {"scale": .1}), (["rpg", "g2"], None, {"scale": .1})],
                   "Alturas iguais: parcelas gravitacionais iguais se retiram", duration=.8)
        bernoulli_title = text("BERNOULLI · caso ideal à mesma altura", 24).move_to([0, -1.75, 0])
        # Comprimento total fixo: a repartição qualitativa responde à fórmula.
        share = ValueTracker(.65)
        bars = VGroup()
        def energy_bars(m):
            groups = []
            for x, pressure_length in ((-2.12, 1.05), (2.12, share.get_value())):
                left = x - .85
                p = Rectangle(width=pressure_length, height=.13, stroke_width=0, fill_color=PRESSURE, fill_opacity=.85).move_to([left + pressure_length / 2, -2.35, 0])
                k = Rectangle(width=1.70 - pressure_length, height=.13, stroke_width=0, fill_color=KINETIC, fill_opacity=.85).move_to([left + pressure_length + (1.70 - pressure_length) / 2, -2.35, 0])
                groups.append(VGroup(p, k))
            m.become(VGroup(*groups))
        share.set_value(1.05)
        energy_bars(bars)
        bars.add_updater(energy_bars)
        self.play(FadeIn(bernoulli_title), FadeIn(bars), run_time=.4)
        self.marks["compensacao_pressao_cinetica"] = round(self.time + .8, 3)
        self.play(share.animate.set_value(.50), Indicate(horizontal.term("k2"), color=KINETIC),
                  Indicate(self.diagram.velocities[1], color=KINETIC), run_time=1.3)
        conclusion = label(r"v_2>v_1\;\Rightarrow\;P_2<P_1", 0, -3.05, size=47, color=PRESSURE)
        self.play(Write(conclusion), Indicate(horizontal.term("P2"), color=PRESSURE),
                  Indicate(self.diagram.pressures[1], color=PRESSURE), run_time=.7)
        self.record("bernoulli_estreitamento", hold=1.2)

        self.phase("Quando Bernoulli vale?")
        bars.clear_updaters()
        self.play(FadeOut(bernoulli_title), FadeOut(conclusion), FadeOut(same_height), FadeOut(bars), run_time=.35)
        self.match(self.general(), duration=1.0)
        hypotheses = note("Incompressível · sem viscosidade\nEscoamento estacionário\nAo longo de uma linha de corrente", 29, y=-2.65)
        self.play(FadeIn(hypotheses), run_time=.6)
        self.record("hipoteses_finais", hold=2.7)
        cta = text("Segue o Parallax Lab / @labparallax", 23).set_color_by_gradient(PRESSURE, KINETIC, GRAVITY).move_to([0, -3.93, 0])
        self.play(FadeIn(cta, shift=UP * .08), run_time=1.1)
        self.record("cta_final", hold=3.0)
        assert self.time < 180, self.time
        (UNIT / "tempos_preview_v4.json").write_text(json.dumps({
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

    def glyph(self, new, maps, reason, duration=1.2, hidden=(), extra=()):
        self.check_math(new)
        for key in hidden:
            new.term(key).set_opacity(0)
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
        self.marks[f"morph_{len(self.glyph_steps) + 1:02d}_meio"] = round(self.time + duration * .5, 3)
        self.play(animation, *extra, run_time=duration)
        self.drop(old, new)
        self.add(new)
        self.current = new
        self.glyph_steps.append({"transformacao": reason, "tempo": round(self.time, 3)})

    def fly(self, source, target, source2=None, target2=None, duration=1.0):
        pairs = [(source, target)] + ([(source2, target2)] if source2 is not None else [])
        travelers, destinations, motions, powers = [], [], [], []
        for origin, dest in pairs:
            destination = dest.copy().set_opacity(1)
            traveler = VGroup(*(g.copy() for g in origin[0])) if isinstance(origin, MathTex) else origin.copy().clear_updaters()
            # v_i sai da seta sem virar o expoente: o 2 entra no destino.
            if isinstance(origin, MathTex) and origin.tex_string.startswith("v_") and len(dest) == 3:
                traveler = VGroup(*(g.copy() for g in origin[0]))
                destination = VGroup(destination[0], destination[2])
                power = dest[1].copy().set_opacity(1)
                powers.append(power)
                motions.append(Succession(Wait(duration * .6), FadeIn(power, run_time=duration * .4)))
                motion = Transform(traveler, destination, path_arc=PI / 10)
            elif len(traveler.family_members_with_points()) != len(destination.family_members_with_points()) or isinstance(origin, Arrow):
                motion = FadeTransform(traveler, destination)
            else:
                motion = Transform(traveler, destination, path_arc=PI / 10)
            destinations.append(destination)
            dest.set_opacity(0)
            existing = {id(g) for root in self.mobjects for g in root.get_family()}
            if not any(id(g) in existing for g in dest.family_members_with_points()):
                self.add(dest)
            travelers.append(traveler)
            motions.append(motion)
        self.add(*travelers)
        self.play(*motions, run_time=duration)
        for _, dest in pairs:
            dest.set_opacity(1)
        self.drop(*travelers, *destinations, *powers)

    def substitute(self, new, old_keys, sources, reason, duration, memory=None):
        """A cópia já está viajando enquanto o fator antigo abre o encaixe.

        Evita transformar uma letra em várias ou deixar um slot vazio antes
        de iniciar a reutilização. As parcelas restantes mantêm glyph maps.
        """
        travelers, destinations, motions, hidden = [], [], [], []
        for index, (source, keys) in enumerate(sources):
            destination = new.term(keys).copy().set_opacity(1)
            traveler = VGroup(*(g.copy() for g in source[0])) if isinstance(source, MathTex) else source.copy().clear_updaters()
            travelers.append(traveler)
            destinations.append(destination)
            hidden.extend([keys] if isinstance(keys, str) else keys)
            if index:
                motions.append(Succession(Wait(duration * .28), Transform(traveler, destination, path_arc=PI / 12, run_time=duration * .72)))
            else:
                motions.append(Transform(traveler, destination, path_arc=PI / 12, run_time=duration))
        self.add(*travelers)
        self.glyph(new, [(old_keys, None, {"scale": .15, "delay": .25, "run_time": .55})],
                   reason, duration=duration, hidden=hidden, extra=motions)
        for _, keys in sources:
            new.term(keys).set_opacity(1)
        self.drop(*travelers, *destinations)
        if memory:
            self.reuses.append({"resultado": memory, "destino": "substituicao_simultanea", "tempo": round(self.time, 3)})

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
        return result.rows([(p, 0, .55, 7.9), (k, 0, -.85 if volume else -1.35, 7.9), (g, 0, -2.25 if volume else -3.05, 7.9)])

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

    def state_stage(self, stage):
        pressure = [("P1", r"P_1"), ("pm", "-"), ("P2", r"P_2")] if stage == 0 else [("P1", r"P_1"), ("P2", r"P_2"), ("rpk", "+")]
        kinetic_sign = ("km", "-") if stage < 2 else ("lpk", "+")
        gravity_sign = ("gm", "-") if stage < 3 else ("lpg", "+")
        result = f(*pressure, ("eq", "="), ("k2", r"\frac12\rho v_2^2"), kinetic_sign, ("k1", r"\frac12\rho v_1^2"),
                   ("plus", "+"), ("g2", r"\rho gh_2"), gravity_sign, ("g1", r"\rho gh_1"), size=48, width=None)
        rows = [(["eq"], 0, -.85, 1), (["plus", "g2"], 2.12, -2.60, 3.65)]
        if stage == 0:
            rows += [(["P1", "pm", "P2"], -2.12, .55, 3.65), (["k2"], 2.12, -.55, 3.65)]
        else:
            rows += [(["P1"], -2.12, .55, 3.65), (["P2"], 2.12, .55, 3.65), (["rpk", "k2"], 2.12, -.55, 3.65)]
        rows += [([kinetic_sign[0], "k1"], -2.12 if stage >= 2 else 2.12, -.85 if stage >= 2 else -1.62, 3.65),
                 ([gravity_sign[0], "g1"], -2.12 if stage >= 3 else 2.12, -2.25 if stage >= 3 else -3.55, 3.65)]
        return result.rows(rows)

    def general(self, constant=r"\text{constante}"):
        return f(("P", "P"), ("pk", "+"), ("k", r"\frac12\rho v^2"), ("pg", "+"), ("g", r"\rho gh"),
                 ("eq", "="), ("constant", constant), size=55)

    def general_columns(self):
        return self.general("C").rows([(["P"], -2.12, .55, 3.65), (["pk", "k"], -2.12, -.85, 3.65),
                                       (["pg", "g"], -2.12, -2.25, 3.65), (["eq"], 0, -.85, 1),
                                       (["constant"], 2.12, -.85, 3.65)])
