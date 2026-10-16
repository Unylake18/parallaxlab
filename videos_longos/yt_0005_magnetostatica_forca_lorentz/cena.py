"""yt_0005 — M1 Magnetostática. Bloco B01 · Do fenômeno à geometria da força de Lorentz (abertura + M1-01 a M1-06), preview sem voz.

Escopo: abertura · M1-01 dois fios (neutros, com corrente: atração/repulsão) · M1-02 da interação para uma carga,
F = q(E + v×B) → F_B = q v×B · M1-03 ângulo θ e |F_B| = |q|vB sinθ · M1-04 paralelo → oblíquo → perpendicular ·
M1-05 q → −q (dois estados discretos) · M1-06 v = v∥ + v⊥ e F_B = q v⊥×B. Para no M1-06; sem curvatura de trajetória.

Princípio: estado físico → grandezas derivadas → geometria. Estados: θ (th), sinal de q (qs, só ±1) e deformação dos fios (t).
v e B ficam no plano da tela (B ao longo de x); F_B = q v×B sai de np.cross e é desenhada com a simbologia padrão do plano:
⊗ (entra na tela) e ⊙ (sai da tela), com raio ∝ |F_B|. Com B = x̂ e v no plano, v×B aponta para dentro da tela quando q > 0.

Gramática: B magenta · E ciano · v branco · v∥ violeta · F_B azul claro · carga + azul / − violeta (sinal na partícula).

Preview:  uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_0005_magnetostatica_forca_lorentz/cena.py YT0005MagnetostaticaM1
GUIAS=1 mostra a safe area.
"""

import math
import sys
from pathlib import Path

import numpy as np
from manim import (
    BOLD, DOWN, LEFT, RIGHT, UL, UR, UP, Arc, Arrow, Circle, Cross, Create, DashedLine, DecimalNumber, Dot, FadeIn, FadeOut,
    Flash, ImageMobject, Line, MathTex, VMobject, ParametricFunction, ReplacementTransform, Rotate, Scene, SurroundingRectangle,
    Transform, ValueTracker, VGroup, always_redraw, linear, smooth,
)
from manim import AnimationGroup

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import DISPLAY_FONT, official_text, screen_text  # noqa: E402
from template.layout_horizontal import GUIAS, safe_guides  # noqa: E402

WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR        # campo elétrico E
MAG = "#EA63FF"             # campo magnético B
BLUE = "#267BFF"            # carga positiva
BLUE_L = "#7FB2FF"          # fios
VIOLET = "#9C8CFF"          # v∥ · carga negativa
FC = "#5AA2FF"              # força magnética F_B
HEADER = "ELETROMAGNETISMO · MAGNETOSTÁTICA"
WM_W, WM_OP = 1.92, 0.45
T_BODY, T_NOTE = 28, 24
M_L, M_M, M_S = 46, 38, 30
LW_VEC, LW_B, LW_WIRE = 5, 3, 6

VMAX = 2.2                  # |v| em unidades do diagrama (escala gs aplicada na tela)
Z_LINES = tuple(0.55 * k for k in (-3, -2, -1, 1, 2, 3, 4, 5))   # linhas de B (unidades do diagrama); z = 0 é a linha auxiliar de θ
FLUXO_B = 0.0               # B é uniforme e estacionário: as marcas ficam estáticas (sem escoamento)
FLUXO_I = 0.75              # velocidade dos portadores nos fios (unidades/s)
CX = 4.6                    # centro da coluna de análise (direita)


def txt(s, size=T_BODY, color=WHITE, opacity=1.0):
    return screen_text(s, size, color=color).set_opacity(opacity)


def eq(*parts, size=M_M, colors=None):
    m = MathTex(*parts, font_size=size, color=WHITE)
    for i, c in (colors or {}).items():
        m[i].set_color(c)
    return m


def halo(m):
    """Contorno na cor do fundo: o rótulo continua legível quando cruza uma linha de campo."""
    return m.set_stroke(BACKGROUND_COLOR, width=7, background=True)


def arrow(a, b, color, width=LW_VEC, z=3, tip=0.26):
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.35,
                 max_stroke_width_to_length_ratio=50).set_z_index(z)


def charge(pos, s, k=1.0):
    c = Circle(radius=0.25 * k, color=WHITE, stroke_width=3).set_fill(BLUE if s >= 0 else VIOLET, 1).move_to(pos)
    sg = MathTex("+" if s >= 0 else "-", font_size=44 * k, color=WHITE).move_to(pos)
    return VGroup(c, sg).set_z_index(6)


_CH, _EQC = {}, {}


def charge_c(pos, s, k=1.0):
    """charge() com a geometria em cache (a cena redesenha a carga a cada quadro)."""
    key = s >= 0
    if key not in _CH:
        _CH[key] = charge(np.zeros(3), s, 1.0)
    return _CH[key].copy().scale(k).move_to(pos)


def eqc(*parts, size=M_M, colors=None):
    """eq() com o MathTex em cache, para rótulos redesenhados a cada quadro."""
    key = (parts, size, tuple(sorted((colors or {}).items())))
    if key not in _EQC:
        _EQC[key] = eq(*parts, size=size, colors=colors)
    return _EQC[key].copy()


def box(m, color=WHITE):
    return SurroundingRectangle(m, color=color, buff=0.22, stroke_width=3, corner_radius=0.1)


# ── B02/B03: parâmetros físicos (unidades do diagrama) e órbita ─────────────────────────────────────────────
MASS, ABSQ, BM = 1.0, 1.0, 1.25          # m, |q|, B
OMEGA = ABSQ * BM / MASS                 # ω_c = |q|B/m
T_PER = 2 * math.pi / OMEGA              # T = 2πm/(|q|B)
VP1 = VMAX * math.sin(math.radians(60.0))        # |v⊥| herdado do fim do B01
VPAR_B01 = VMAX * math.cos(math.radians(60.0))   # v∥ do B01 (some quando olhamos ao longo de B)
VPAR = 0.8                               # v∥ da hélice (B03)
BX = tuple(0.55 * k for k in range(-3, 8))       # grade de B: colunas (profundidade no B01)
BY = tuple(sorted(Z_LINES + (0.0,)))             # grade de B: linhas
BXS, BYS = BX[::2], (-1.1, 0.0, 1.1, 2.2)        # grade esparsa (B03)


class Orbit:
    """Movimento de uma carga em B = B ẑ: todas as grandezas vêm de (m, |q|, B, v⊥, v∥, sinal de q) e de um relógio.

    R = m v⊥/(|q|B) · ω = |q|B/m · T = 2π/ω · passo p = |v∥| T. Órbitas que compartilham o relógio têm a mesma ω:
    completam as voltas juntas sem sincronização manual. A força é F = q v×B, calculada com np.cross."""

    def __init__(self, vp, vpar, s, clock, t0, color):
        self.vp, self.vpar, self.s, self.clock, self.t0, self.color = vp, vpar, s, clock, t0, color
        self.R = MASS * vp / (ABSQ * BM)
        self.a0 = math.pi if s > 0 else 0.0              # começa na origem; o centro fica do lado de F = q v×B
        self.C = -self.R * np.array([math.cos(self.a0), math.sin(self.a0), 0.0])
        self.u_on, self.ramp, self.u_max = 1e9, 0.15, 1e9

    def u(self):
        return min(max(0.0, self.clock.get_value() - self.t0), self.u_max)

    def _g(self, x):
        d = self.ramp
        return 0.0 if x <= 0 else (x * x / (2 * d) if x < d else x - d / 2)

    def _gd(self, x):
        return 0.0 if x <= 0 else (x / self.ramp if x < self.ramp else 1.0)

    def pos(self, u=None):
        u = self.u() if u is None else u
        a = self.a0 - self.s * OMEGA * u
        return np.array([self.C[0] + self.R * math.cos(a), self.C[1] + self.R * math.sin(a), self.vpar * self._g(u - self.u_on)])

    def vel(self, u=None):
        u = self.u() if u is None else u
        a = self.a0 - self.s * OMEGA * u
        return np.array([self.s * OMEGA * self.R * math.sin(a), -self.s * OMEGA * self.R * math.cos(a),
                         self.vpar * self._gd(u - self.u_on)])

    def force(self, u=None):
        return self.s * ABSQ * np.cross(self.vel(u), np.array([0.0, 0.0, BM]))   # F = q v×B


class YT0005MagnetostaticaM1(Scene):

    def setup(self):
        self.camera.background_color = BACKGROUND_COLOR
        # geometria 2D do diagrama (origem da carga e escala): trackers para poder abrir espaço (FOCUS) no M1-06
        self.ox, self.oy, self.gs = ValueTracker(-4.3), ValueTracker(-1.0), ValueTracker(1.15)

    # ── geometria ────────────────────────────────────────────────────────────────────────────────────────────
    def O(self):
        return np.array([self.ox.get_value(), self.oy.get_value(), 0.0])

    def S(self):
        return self.gs.get_value()

    def P(self, x, z):
        """Ponto do diagrama (x ao longo de B, z para cima) → tela."""
        return self.O() + self.S() * np.array([x, z, 0.0])

    def hold(self, d):
        """Pausa que não congela o quadro: o wait() padrão do Manim vira imagem estática quando os updaters não usam dt
        (always_redraw), o que parava o fluxo de B, os portadores e os vetores a cada pausa."""
        self.wait(d, frozen_frame=False)

    def construct(self):
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(WM_W).set_opacity(WM_OP).to_corner(UR, buff=0.3)
        self.tag = txt(HEADER, 18, opacity=0.6).to_corner(UL, buff=0.38)
        if GUIAS:
            self.add(safe_guides())
        self.abertura()
        self.bloco_01_lorentz()
        self.bloco_02_ciclotron()
        self.bloco_03_helice()

    # ── abertura ───────────────────────────────────────────────────────────────────────────────────────────────
    def abertura(self):
        brand = txt("PARALLAX LAB", 22, opacity=0.8).move_to([0, 2.05, 0])
        title = official_text("MAGNETOSTÁTICA", DISPLAY_FONT, BOLD, 58).move_to([0, 1.2, 0])
        ask = txt("O que um campo magnético realmente faz?", 30, opacity=0.9).move_to([0, 0.25, 0])
        self.play(FadeIn(brand, shift=0.1 * DOWN), FadeIn(title, shift=0.15 * DOWN), FadeIn(self.wm), run_time=1.2)
        self.play(FadeIn(ask), run_time=0.9)
        self.hold(2.4)
        # o título vira o cabeçalho de série; a pergunta cede ao primeiro fenômeno
        self.play(FadeOut(brand), FadeOut(ask), ReplacementTransform(title, self.tag), run_time=1.2)

    def bloco_01_lorentz(self):
        self.m1_01_fios()
        self.m1_02_carga()
        self.m1_03_angulo()
        self.m1_04_paralelo_perp()
        self.m1_05_sinal()
        self.m1_06_decomposicao()

    # ── M1-01 · dois fios ─────────────────────────────────────────────────────────────────────────────────────
    def m1_01_fios(self):
        t = ValueTracker(0.0)                       # >0 atração · <0 repulsão (deformação das duas barras)
        self.t_fios = t
        XW = 1.9
        self.ph_l = ValueTracker(0.0)               # deslocamento dos portadores (+) da barra da esquerda
        YMIN, SPAN, STEP = -1.9, 3.6, 0.3

        def wx(sign, y):
            prof = max(0.0, 1 - ((y + 0.1) / 2.1) ** 2)
            return sign * (XW - 0.5 * t.get_value() * prof)

        def wire(sign):
            return always_redraw(lambda: ParametricFunction(lambda y: np.array([wx(sign, y), y, 0]), t_range=[-2.1, 1.9],
                                                           color=BLUE_L, stroke_width=LW_WIRE))

        def dots(sign, ph):
            """Corrente como fluxo: pulsos claros que correm ao longo do fio (sem modelo microscópico de portadores)."""
            def f():
                g = VGroup()
                period = 0.7
                for k in range(int((SPAN + STEP) / period) + 1):
                    y = YMIN + ((k * period + ph.get_value()) % (SPAN + STEP))
                    op = min(1.0, max(0.0, min(y + 1.95, 1.95 - y) / 0.4))   # entram e saem sem "pop"
                    y2 = min(y + 0.32, 1.9)
                    g.add(Line([wx(sign, y), y, 0], [wx(sign, y2), y2, 0], color=WHITE, stroke_width=4.5).set_opacity(0.9 * op))
                return g.set_z_index(2)
            return always_redraw(f)

        self.ph_r = ValueTracker(0.0)
        self.dir_r = 1.0                            # sentido da corrente da direita (+1 sobe, −1 desce)
        # corrente como fluxo contínuo: os portadores (+) correm o tempo todo
        self.ph_l.add_updater(lambda m, dt: m.increment_value(FLUXO_I * dt))
        self.ph_r.add_updater(lambda m, dt: m.increment_value(FLUXO_I * dt * self.dir_r))
        self.add(self.ph_l, self.ph_r)
        wl, wr = wire(-1), wire(+1)
        dl, dr = dots(-1, self.ph_l), dots(+1, self.ph_r)
        cur_l = arrow([-2.75, 0.6, 0], [-2.75, 1.7, 0], WHITE, 6)
        cur_r = arrow([2.75, 0.6, 0], [2.75, 1.7, 0], WHITE, 6)
        i_l = eq("I_1", size=M_S).next_to(cur_l, LEFT, buff=0.15)
        i_r = eq("I_2", size=M_S).next_to(cur_r, RIGHT, buff=0.15)

        def force_pair():
            tv = t.get_value()
            if abs(tv) < 0.4:
                return VGroup()
            d = 1 if tv > 0 else -1
            ln = 0.95 * min(1.0, abs(tv))
            y = -0.1
            xl, xr = wx(-1, y), wx(1, y)
            a_l = arrow([xl, y, 0], [xl + d * ln, y, 0], FC, 6)
            a_r = arrow([xr, y, 0], [xr - d * ln, y, 0], FC, 6)
            lab_l = eq(r"\mathbf F", size=M_S, colors={0: FC}).next_to(a_l.get_end(), DOWN, buff=0.12)
            lab_r = eq(r"\mathbf F", size=M_S, colors={0: FC}).next_to(a_r.get_end(), DOWN, buff=0.12)
            return VGroup(a_l, a_r, lab_l, lab_r)

        forces = always_redraw(force_pair)
        neutro = txt("fios eletricamente neutros, percorridos por corrente", T_NOTE, opacity=0.9).move_to([0, 2.3, 0])
        cap1 = txt("correntes no mesmo sentido: os fios se atraem", T_BODY).move_to([0, -2.75, 0])
        cap2 = txt("sentidos opostos: os fios se repelem", T_BODY).move_to([0, -2.75, 0])
        cap3 = txt("neutros, e ainda assim interagem", T_BODY).move_to([0, -2.75, 0])

        self.wires = VGroup(wl, wr, dl, dr, cur_l, cur_r, i_l, i_r, forces)
        self.add(forces)
        self.play(AnimationGroup(AnimationGroup(FadeIn(wl), FadeIn(wr), FadeIn(dl), FadeIn(dr), FadeIn(neutro)),
                                 AnimationGroup(FadeIn(cur_l), FadeIn(cur_r), FadeIn(i_l), FadeIn(i_r)), lag_ratio=0.5),
                  run_time=1.6)
        self.hold(0.5)
        self.play(FadeIn(cap1), t.animate.set_value(1.0), run_time=1.6, rate_func=smooth)
        self.hold(1.0)
        # zera o estado (atração) antes de inverter a corrente: as barras relaxam enquanto a corrente da direita gira
        self.play(FadeOut(cap1), t.animate.set_value(0.0), run_time=0.9, rate_func=smooth)
        self.dir_r = -1.0
        self.play(Rotate(cur_r, math.pi, about_point=cur_r.get_center()), run_time=0.8)
        self.play(FadeIn(cap2), t.animate.set_value(-1.0), run_time=1.6, rate_func=smooth)
        self.hold(1.2)
        self.play(ReplacementTransform(cap2, cap3), run_time=0.8)
        self.hold(0.6)
        self.neutro, self.cur_r_ref, self.cap3 = neutro, cur_r, cap3

    # ── M1-02 · da interação para uma carga ────────────────────────────────────────────────────────────────
    def m1_02_carga(self):
        t, ph = self.t_fios, self.ph_l
        # volta à geometria reta; só a corrente da esquerda interessa agora
        self.play(t.animate.set_value(0.0), FadeOut(self.cur_r_ref), FadeOut(self.neutro), FadeOut(self.cap3), run_time=1.0)
        cap = txt("olhando para uma carga em movimento", T_BODY).move_to([0, -2.75, 0])
        lens = Circle(radius=1.0, color=WHITE, stroke_width=3).move_to([-1.9, 0.0, 0])
        self.play(FadeIn(lens), FadeIn(cap), run_time=0.8)
        self.hold(1.6)                                 # a corrente continua fluindo dentro da lente
        carrier = charge([-1.9, 0.0, 0], 1, 0.36)       # uma carga em movimento, vista de perto
        self.th, self.qs, self.vs, self.fs = ValueTracker(60.0), ValueTracker(1.0), ValueTracker(0.0), ValueTracker(0.0)
        self.play(FadeIn(carrier, scale=0.5), run_time=0.6)
        self.play(AnimationGroup(AnimationGroup(FadeOut(self.wires), FadeOut(lens), FadeOut(cap)),
                                 carrier.animate.scale(1 / 0.36).move_to(self.O()), lag_ratio=0.25),
                  run_time=1.8, rate_func=smooth)
        ph.clear_updaters()
        self.ph_r.clear_updaters()
        self.remove(carrier, ph, self.ph_r)
        self.q_mob = always_redraw(lambda: charge_c(self.O(), self.qs.get_value(), self.S() / 1.15))
        self.add(self.q_mob)

        # campo B: três linhas magenta paralelas ao eixo x do diagrama
        X0, X1, PER, DASH = -2.0, 3.8, 0.9, 0.58

        def b_lines():
            """Linhas de B densas e discretas: traços que derivam devagar para a direita (fluxo sutil) + ponta fixa."""
            g = VGroup()
            off = (self.time * FLUXO_B) % PER
            for z in Z_LINES:
                if self.P(0, z)[1] < -3.05:
                    continue
                a = X0 - PER + off
                while a < X1 - 0.3:
                    s, e = max(a, X0), min(a + DASH, X1 - 0.3)
                    if e > s:
                        g.add(Line(self.P(s, z), self.P(e, z), color=MAG, stroke_width=2.4).set_opacity(0.45))
                    a += PER
                g.add(arrow(self.P(X1 - 0.3, z), self.P(X1, z), MAG, 2.4, 1, tip=0.2).set_opacity(0.45))
            return g

        self.b_mob = always_redraw(b_lines)
        self.b_lab = always_redraw(lambda: halo(eqc(r"\mathbf B", size=M_M, colors={0: MAG}).move_to(
            self.P(X1, Z_LINES[-1]) + np.array([-0.05, 0.38, 0]))))

        # velocidade (derivada de th) e rótulo ao lado do vetor
        def v2():
            a = math.radians(self.th.get_value())
            return VMAX * self.vs.get_value() * np.array([math.cos(a), math.sin(a)])

        self.v2 = v2
        self.v_dim = ValueTracker(1.0)
        self.v_arr = always_redraw(lambda: arrow(self.O(), self.O() + self.S() * np.array([*v2(), 0]), WHITE, LW_VEC, 4)
                                   .set_opacity(self.v_dim.get_value()) if self.vs.get_value() > 0.02 else VGroup())

        def v_label():
            v = np.array([*v2(), 0.0])
            if np.linalg.norm(v) < 0.3:
                return VGroup()
            u = v / np.linalg.norm(v)
            n = np.array([-u[1], u[0], 0.0])                           # normal à esquerda de v
            lift = 0.4 * max(0.0, (40.0 - self.th.get_value()) / 40.0)  # θ pequeno: o "v" sai de cima da linha auxiliar
            return halo(eqc(r"\mathbf v", size=M_M).move_to(self.O() + self.S() * (v + 0.42 * u + lift * n))
                        .set_opacity(self.v_dim.get_value()))

        self.v_lab = always_redraw(v_label)
        self.add(self.v_arr, self.v_lab)
        # o campo aparece em volta da carga e, logo em seguida, a velocidade cresce (uma só entrada contínua)
        self.play(AnimationGroup(AnimationGroup(FadeIn(self.b_mob, shift=0.2 * RIGHT), FadeIn(self.b_lab)),
                                 self.vs.animate.set_value(1.0), lag_ratio=0.45), run_time=1.8, rate_func=smooth)

        # lei completa → termo magnético (com lado esquerdo)
        full = eq(r"\mathbf F", "=", "q", "(", r"\mathbf E", "+", r"\mathbf v", r"\times", r"\mathbf B", ")", size=M_L,
                  colors={4: CYAN, 8: MAG}).move_to([CX, 1.9, 0])
        short = eq(r"\mathbf F_B", "=", "q", r"\mathbf v", r"\times", r"\mathbf B", size=M_L,
                   colors={0: FC, 5: MAG}).move_to([CX, 1.9, 0])
        self.play(FadeIn(full, shift=0.1 * DOWN), run_time=1.2)
        self.hold(1.2)
        pairs = ((0, 0), (1, 1), (2, 2), (6, 3), (7, 4), (8, 5))
        self.lor = VGroup(*[full[a] for a, _ in pairs])
        self.lor_box = box(short)
        # E sai e o termo magnético se fecha numa só passagem contínua; a caixa nasce já no destino
        self.play(AnimationGroup(AnimationGroup(*[FadeOut(full[i]) for i in (3, 4, 5, 9)]),
                                 AnimationGroup(*[Transform(full[a], short[b]) for a, b in pairs]),
                                 FadeIn(self.lor_box), lag_ratio=0.35), run_time=2.0, rate_func=smooth)
        self.hold(0.5)

    # ── M1-03 · geometria do produto vetorial ──────────────────────────────────────────────────────────────
    def m1_03_angulo(self):
        th, qs, fs = self.th, self.qs, self.fs

        def f3():
            """F = q v×B calculado em 3D (v no plano da tela, B = x̂); f3()[2] > 0: sai da tela."""
            a = math.radians(th.get_value())
            v = VMAX * np.array([math.cos(a), math.sin(a), 0.0])
            return qs.get_value() * fs.get_value() * np.cross(v, np.array([1.0, 0.0, 0.0]))

        self.f3 = f3

        def f_symbol():
            F = f3()
            m = abs(F[2]) / VMAX                      # |F_B| / (|q| v B) = sinθ
            if m < 0.03:
                return VGroup()
            S = self.S()
            pos = self.P(-1.25, 0.0)
            r = 0.32 * S                              # o símbolo indica a DIREÇÃO (tamanho fixo)
            op = min(1.0, m / 0.12)                   # aparece/some sem "pop" perto de F = 0
            ring = Circle(radius=r, color=FC, stroke_width=4).set_fill(BACKGROUND_COLOR, 1).move_to(pos)
            if F[2] < 0:                              # entra na tela: ⊗
                c = 0.62 * r
                mark = VGroup(Line(pos + [-c, -c, 0], pos + [c, c, 0], color=FC, stroke_width=4),
                              Line(pos + [-c, c, 0], pos + [c, -c, 0], color=FC, stroke_width=4))
            else:                                     # sai da tela: ⊙
                mark = Circle(radius=0.3 * r, color=FC, stroke_width=0).set_fill(FC, 1).move_to(pos)
            # a MAGNITUDE (qualitativa) vai num halo separado: brilho e espessura crescem com |F_B|
            glow = Circle(radius=r + 0.1 * S, color=FC, stroke_width=2 + 8 * m).set_stroke(opacity=0.12 + 0.5 * m).move_to(pos)
            lab = halo(eqc(r"\mathbf F_B", size=M_M, colors={0: FC}).move_to(pos + np.array([0, -(r + 0.42), 0])))
            link = Line(pos + [r, 0, 0], self.O() + [-0.3 * S, 0, 0], color=FC, stroke_width=2).set_opacity(0.55)
            return VGroup(link, glow, ring, mark, lab).set_z_index(4).set_opacity(op)

        self.f_sym = always_redraw(f_symbol)

        # linha auxiliar paralela a B por O, arco e rótulo de θ ancorado ao arco (posição calculada, nunca fixa)
        helper = always_redraw(lambda: DashedLine(self.O(), self.P(3.2, 0.0), color=WHITE, stroke_width=2, dash_length=0.12)
                               .set_opacity(0.65).set_z_index(2))
        arc = always_redraw(lambda: Arc(radius=0.95 * self.S(), start_angle=0, angle=math.radians(th.get_value()),
                                        arc_center=self.O(), color=WHITE, stroke_width=3).set_z_index(5)
                            if th.get_value() > 2 else VGroup())

        def th_label():
            tv = th.get_value()
            if tv < 6:
                return VGroup()
            a = math.radians(tv)
            # um único rótulo, sempre entre B (linha auxiliar) e v, ou logo abaixo da linha auxiliar quando θ é pequeno:
            # o ângulo polar vai de θ/2 (θ ≥ 40°) a −24° (θ → 0), de forma contínua e sem cruzar v
            lead = max(0.0, (40.0 - tv) / 40.0)
            phi = a / 2 - math.radians(24) * lead
            r = 1.3 + 0.1 * lead
            return halo(eqc(r"\theta", size=M_M).move_to(self.O() + self.S() * np.array([r * math.cos(phi), r * math.sin(phi), 0.0])))

        th_lab = always_redraw(th_label)
        self.helper, self.arc, self.th_lab = helper, arc, th_lab
        self.play(FadeIn(helper), FadeIn(arc), FadeIn(th_lab), run_time=1.0)
        self.add(self.f_sym)
        note = eq(r"\otimes", r"\;\text{entra na tela}", size=M_S).move_to([CX, -2.0, 0])
        self.play(fs.animate.set_value(1.0), FadeIn(note), run_time=1.4, rate_func=smooth)
        self.hold(0.6)

        # |F_B| = |q| v B sinθ
        mag = eq(r"|\mathbf F_B|", "=", "|q|", "v", "B", r"\sin\theta", size=M_M, colors={0: FC, 4: MAG}).move_to([CX, 0.7, 0])
        self.play(FadeIn(mag, shift=0.1 * DOWN), FadeOut(note), run_time=1.2)
        lab_t, lab_s = eq(r"\theta", "=", size=M_S), eq(r"\sin\theta", "=", size=M_S)
        num_t = DecimalNumber(60, num_decimal_places=0, unit=r"^\circ", font_size=M_S)
        num_s = DecimalNumber(0.87, num_decimal_places=2, font_size=M_S)
        lab_t.move_to([CX - 0.9, -0.4, 0])
        lab_s.move_to([CX - 0.9, -1.05, 0]).align_to(lab_t, LEFT)
        num_t.add_updater(lambda m: m.set_value(th.get_value()).next_to(lab_t, RIGHT, buff=0.15))
        num_s.add_updater(lambda m: m.set_value(math.sin(math.radians(th.get_value()))).next_to(lab_s, RIGHT, buff=0.15))
        self.readout = VGroup(lab_t, num_t, lab_s, num_s)
        self.mag = mag
        self.play(FadeIn(self.readout), run_time=0.8)
        self.play(th.animate.set_value(85.0), run_time=1.8, rate_func=smooth)
        self.play(th.animate.set_value(40.0), run_time=1.8, rate_func=smooth)
        self.hold(0.6)

    # ── M1-04 · paralelo → oblíquo → perpendicular ─────────────────────────────────────────────────────────
    def m1_04_paralelo_perp(self):
        th = self.th
        slot = [CX, -2.1, 0]
        cap_par = eq(r"\mathbf v\parallel\mathbf B", r"\Rightarrow", r"|\mathbf F_B|=0", size=34, colors={2: FC}).move_to(slot)
        cap_obl = eq(r"0<|\mathbf F_B|<|q|vB", size=34, colors={0: WHITE}).move_to(slot)
        cap_per = eq(r"\mathbf v\perp\mathbf B", r"\Rightarrow", r"|\mathbf F_B|=|q|vB", size=34, colors={2: FC}).move_to(slot)
        self.play(th.animate.set_value(0.0), run_time=2.6, rate_func=smooth)
        self.play(FadeIn(cap_par), run_time=0.6)
        self.hold(1.6)
        self.play(th.animate.set_value(45.0), ReplacementTransform(cap_par, cap_obl), run_time=2.0, rate_func=smooth)
        self.hold(1.2)
        self.play(th.animate.set_value(90.0), ReplacementTransform(cap_obl, cap_per), run_time=2.0, rate_func=smooth)
        self.hold(1.8)
        self.cap_per = cap_per

    # ── M1-05 · sinal da carga: dois estados discretos ────────────────────────────────────────────────────
    def m1_05_sinal(self):
        qs = self.qs
        slot = [CX, -0.5, 0]
        e_pos = eq("q>0", r"\Rightarrow", r"\otimes", size=M_M).move_to(slot)
        e_neg = eq("q<0", r"\Rightarrow", r"\odot", size=M_M).move_to(slot)
        note = txt("mesmo módulo, sentido oposto", T_NOTE, opacity=0.9).move_to([CX, -1.3, 0])
        self.play(FadeOut(self.readout), FadeOut(self.cap_per), run_time=0.5)
        self.play(FadeIn(e_pos, shift=0.1 * DOWN), run_time=0.6)
        self.hold(1.0)
        # troca discreta: o módulo de F_B não passa por zero
        qs.set_value(-1.0)
        self.play(Flash(self.O(), color=VIOLET, flash_radius=0.7, line_length=0.18), ReplacementTransform(e_pos, e_neg),
                  FadeIn(note), run_time=0.8)
        self.hold(2.0)
        qs.set_value(1.0)
        self.play(Flash(self.O(), color=BLUE, flash_radius=0.7, line_length=0.18), FadeOut(e_neg), FadeOut(note), run_time=0.8)
        self.hold(0.6)

    # ── M1-06 · decomposição da velocidade ────────────────────────────────────────────────────────────────
    def m1_06_decomposicao(self):
        th = self.th
        # FOCUS: o diagrama ganha espaço; a fórmula magnética desce para virar a conclusão
        self.play(FadeOut(self.mag), th.animate.set_value(60.0), self.ox.animate.set_value(-3.7),
                  self.oy.animate.set_value(-1.1), self.gs.animate.set_value(1.3),
                  VGroup(self.lor, self.lor_box).animate.move_to([CX, -0.45, 0]), run_time=1.8, rate_func=smooth)
        self.p_vis, self.par_dim, self.perp_dim = ValueTracker(0.0), ValueTracker(1.0), ValueTracker(1.0)

        def par2():
            return self.p_vis.get_value() * np.array([self.v2()[0], 0.0, 0.0])

        def perp2():
            return self.p_vis.get_value() * np.array([0.0, self.v2()[1], 0.0])

        def at(p):
            return self.O() + self.S() * p

        self.v_par = always_redraw(lambda: arrow(self.O(), at(par2()), VIOLET, 6, 4).set_opacity(self.par_dim.get_value())
                                   if self.p_vis.get_value() > 0.02 else VGroup())
        self.v_perp = always_redraw(lambda: arrow(self.O(), at(perp2()), WHITE, 6, 5)
                                    if self.p_vis.get_value() > 0.02 else VGroup())

        def guides():
            if self.p_vis.get_value() < 0.02:
                return VGroup()
            tip = at(np.array([*self.v2(), 0.0]))
            return VGroup(DashedLine(tip, at(par2()), color=WHITE, stroke_width=2, dash_length=0.1).set_opacity(0.45),
                          DashedLine(tip, at(perp2()), color=WHITE, stroke_width=2, dash_length=0.1).set_opacity(0.45))

        def lab_par():
            if self.p_vis.get_value() < 0.5:
                return VGroup()
            return halo(eqc(r"\mathbf v_\parallel", size=M_M, colors={0: VIOLET}).move_to(at(par2()) + np.array([0.0, -0.5, 0.0]))
                        .set_opacity(self.par_dim.get_value()))

        def lab_perp():
            if self.p_vis.get_value() < 0.5:
                return VGroup()
            return halo(eqc(r"\mathbf v_\perp", size=M_M).move_to(at(perp2()) + np.array([-0.55, 0.0, 0.0])))

        self.guides = always_redraw(guides)
        self.lab_par_m, self.lab_perp_m = always_redraw(lab_par), always_redraw(lab_perp)
        self.add(self.guides, self.v_par, self.v_perp, self.lab_par_m, self.lab_perp_m)
        self.play(self.p_vis.animate.set_value(1.0), run_time=1.6, rate_func=smooth)

        # v = v∥ + v⊥
        dec = eq(r"\mathbf v", "=", r"\mathbf v_\parallel", "+", r"\mathbf v_\perp", size=M_M, colors={2: VIOLET}).move_to([CX, 2.0, 0])
        self.play(FadeIn(dec, shift=0.1 * DOWN), run_time=1.0)
        self.hold(0.8)
        # v∥ ∥ B → v∥ × B = 0
        zero = eq(r"\mathbf v_\parallel", r"\times", r"\mathbf B", "=", r"\mathbf 0", size=M_M,
                  colors={0: VIOLET, 2: MAG}).move_to([CX, 0.95, 0])
        self.play(FadeIn(zero, shift=0.1 * DOWN), run_time=1.0)
        self.hold(1.0)
        # v∥ perde destaque (continua identificável); v⊥ fica ativa e ligada à força
        self.play(self.par_dim.animate.set_value(0.5), self.v_dim.animate.set_value(0.4), zero.animate.set_opacity(0.7),
                  run_time=1.2)
        note_p = VGroup(eq(r"\mathbf v_\parallel", size=30, colors={0: VIOLET}), txt("→ não contribui", T_NOTE, opacity=0.9)
                        ).arrange(RIGHT, buff=0.25)
        note_q = VGroup(eq(r"\mathbf v_\perp", size=30), txt("→ produz a força magnética", T_NOTE)).arrange(RIGHT, buff=0.25)
        notes = VGroup(note_p, note_q).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([CX, -2.2, 0])
        self.dec, self.zero, self.notes = dec, zero, notes
        self.play(FadeIn(note_p), run_time=0.8)
        self.play(FadeIn(note_q), run_time=0.8)
        # conclusão: F_B = q v⊥ × B (a mesma força: a geometria de F_B não muda)
        final = eq(r"\mathbf F_B", "=", "q", r"\mathbf v_\perp", r"\times", r"\mathbf B", size=M_L,
                   colors={0: FC, 5: MAG}).move_to([CX, -0.45, 0])
        self.play(*[Transform(self.lor[i], final[i]) for i in range(6)], Transform(self.lor_box, box(final)),
                  run_time=1.4, rate_func=smooth)
        self.hold(1.2)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # Infraestrutura 3D → tela: câmera com guinada β (90°: B horizontal, como no B01 · 0°: olhando ao longo de B) e
    # inclinação τ (0°: plano da órbita de frente · >0°: perspectiva da hélice). Mundo: B ao longo de z.
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def W(self, p):
        b, t = math.radians(self.beta.get_value()), math.radians(self.tau.get_value())
        x, y, z = float(p[0]), float(p[1]), float(p[2])
        xp = x * math.cos(b) + z * math.sin(b)
        zp = -x * math.sin(b) + z * math.cos(b)
        return self.O() + self.S() * np.array([xp, y * math.cos(t) + zp * math.sin(t), 0.0])

    def Wv(self, v):
        return self.W(np.asarray(v, dtype=float)) - self.W(np.zeros(3))

    def mk_bgrid(self):
        """Campo B uniforme e ESTÁTICO: a mesma grade de segmentos ao longo de z vira pontos ⊙ quando olhamos ao longo de B."""
        cache = {}

        def f():
            key = (round(self.beta.get_value(), 2), round(self.tau.get_value(), 2), round(self.ox.get_value(), 3),
                   round(self.oy.get_value(), 3), round(self.gs.get_value(), 3), self.bsparse, round(self.bop.get_value(), 3),
                   round(self.bz1.get_value(), 2))
            if cache.get("k") == key:
                return cache["g"]
            b = math.radians(self.beta.get_value())
            g = VGroup()
            xs, ys = (BXS, BYS) if self.bsparse else (BX, BY)
            z0, z1 = -2.0, self.bz1.get_value()
            for y in ys:
                row = 1.0 if y != 0.0 else min(1.0, max(0.0, (90.0 - self.beta.get_value()) / 30.0))   # a linha z = 0 do B01 era a auxiliar de θ
                for x in xs:
                    p0, p1 = self.W([x, y, z0]), self.W([x, y, z1])
                    if p0[1] < -3.1 or p0[1] > 3.1:
                        continue
                    if p1[1] > 3.2:
                        p1 = p0 + (p1 - p0) * ((3.2 - p0[1]) / (p1[1] - p0[1]))
                    L = float(np.linalg.norm(p1 - p0))
                    lf = min(1.0, max(0.0, (L - 0.2) / 0.6))
                    op = self.bop.get_value() * row
                    if lf > 0.01 and L > 0.5:
                        pe = p1 - (p1 - p0) / L * 0.4
                        opl = op * (0.07 + 0.38 * (1 - math.sin(b))) * lf
                        g.add(DashedLine(p0, pe, dash_length=0.2, dashed_ratio=0.55, color=MAG, stroke_width=2.4).set_opacity(opl))
                        g.add(arrow(pe, p1, MAG, 2.4, 1, tip=0.18).set_opacity(opl))
                    if lf < 0.99:
                        s = 0.07 * self.S() / 1.15
                        oc = 0.3 * op * (1 - lf)
                        g.add(Circle(radius=s, color=MAG, stroke_width=2).set_opacity(oc).move_to(p1))
                        g.add(Dot(p1, radius=0.025, color=MAG).set_opacity(oc))
            cache["k"], cache["g"] = key, g
            return g

        return always_redraw(f)

    def mk_charge(self, orb):
        return always_redraw(lambda: charge_c(self.W(orb.pos()), orb.s, max(0.8, self.S() / 1.15)))

    def mk_trail(self, orb, width=3.5, op=0.9):
        def f():
            u = orb.u()
            if u < 0.03:
                return VGroup()
            us = np.linspace(0.0, u, int(min(520, max(8, u / 0.06))))
            m = VMobject(color=orb.color, stroke_width=width).set_stroke(opacity=op)
            m.set_points_as_corners([self.W(orb.pos(x)) for x in us])
            return m.set_z_index(3)
        return always_redraw(f)

    def mk_vec(self, orb, kind, color, width=5.0, z=4, vis=None, op=None):
        """Seta ancorada na partícula: 'v' (v⊥, sem a componente z) · 'vpar' (comprimento em vis) · 'F' (F = q v×B)."""
        def f():
            p = orb.pos()
            if kind == "v":
                vec = orb.vel() * np.array([1.0, 1.0, 0.0])
            elif kind == "vpar":
                vec = np.array([0.0, 0.0, vis.get_value()])
            else:
                vec = orb.force() * (0.5 / (ABSQ * BM))
            a, b = self.W(p), self.W(p + vec)
            if np.linalg.norm(b - a) < 0.14:
                return VGroup()
            m = arrow(a, b, color, width, z)
            return m.set_opacity(op.get_value()) if op is not None else m
        return always_redraw(f)

    def mk_force_marks(self, orb):
        """F_B como seta no plano da tela, ou como ⊗/⊙ (tamanho fixo) quando aponta para dentro/fora dela."""
        def ring():
            F = orb.force()
            nf = float(np.linalg.norm(F)) + 1e-9
            b = math.radians(self.beta.get_value())
            zp = -F[0] * math.sin(b) + F[2] * math.cos(b)
            ro = min(1.0, max(0.0, (abs(zp) / nf - 0.25) / 0.6))
            if ro < 0.03:
                return VGroup()
            S, pos = self.S(), self.W(orb.pos() + np.array([0.0, 0.0, -1.25]))
            r = 0.32 * S
            rg = Circle(radius=r, color=FC, stroke_width=4).set_fill(BACKGROUND_COLOR, 1).move_to(pos)
            if zp < 0:
                c = 0.62 * r
                mark = VGroup(Line(pos + [-c, -c, 0], pos + [c, c, 0], color=FC, stroke_width=4),
                              Line(pos + [-c, c, 0], pos + [c, -c, 0], color=FC, stroke_width=4))
            else:
                mark = Circle(radius=0.3 * r, color=FC, stroke_width=0).set_fill(FC, 1).move_to(pos)
            lab = halo(eqc(r"\mathbf F_B", size=M_M, colors={0: FC}).move_to(pos + np.array([0, -(r + 0.42), 0])))
            link = Line(pos + [r, 0, 0], self.W(orb.pos()) + [-0.3 * S, 0, 0], color=FC, stroke_width=2).set_opacity(0.55)
            return VGroup(link, rg, mark, lab).set_z_index(4).set_opacity(ro)

        def lab_arrow():
            F = orb.force() * (0.5 / (ABSQ * BM))
            a, b = self.W(orb.pos()), self.W(orb.pos() + F)
            L = float(np.linalg.norm(b - a))
            if L < 0.5:
                return VGroup()
            u = (b - a) / L
            n = np.array([-u[1], u[0], 0.0])
            return halo(eqc(r"\mathbf F_B", size=M_M, colors={0: FC}).move_to((a + b) / 2 - 0.42 * n)).set_opacity(min(1.0, (L - 0.5) / 0.4))

        return [always_redraw(ring), self.mk_vec(orb, "F", FC, 6, 4), always_redraw(lab_arrow)]

    def mk_center(self, orb, name):
        """Raio R como linha de cota (deslocada, para não coincidir com a seta de F_B), centro e rótulo."""
        def geom():
            c = self.W(np.array([orb.C[0], orb.C[1], orb.pos()[2]]))
            p = self.W(orb.pos())
            d = p - c
            n = np.array([-d[1], d[0], 0.0])
            n = n / (np.linalg.norm(n) + 1e-9)
            return c, p, n

        def line():
            c, p, n = geom()
            off = 0.2 * self.S() / 1.3
            a, b = c + n * off, p + n * off
            return VGroup(DashedLine(a, b, dash_length=0.12, color=WHITE, stroke_width=2).set_opacity(0.85),
                          Line(a - n * 0.08, a + n * 0.08, color=WHITE, stroke_width=2),
                          Line(b - n * 0.08, b + n * 0.08, color=WHITE, stroke_width=2),
                          Dot(c, radius=0.05, color=WHITE)).set_z_index(2)

        def lab():
            c, p, n = geom()
            return halo(eqc(name, size=M_M).move_to((c + p) / 2 + n * (0.2 * self.S() / 1.3 + 0.3)))

        return always_redraw(line), always_redraw(lab)

    def mk_tag(self, orb, text):
        return always_redraw(lambda: halo(eqc(text, size=M_S).move_to(self.W(orb.pos()) + np.array([0.42, 0.42, 0.0]))))

    def mk_rightangle(self, orb):
        def f():
            if self.tau.get_value() > 5:
                return VGroup()
            v, F = orb.vel(), orb.force()
            a, b = self.Wv(v / (np.linalg.norm(v) + 1e-9)), self.Wv(F / (np.linalg.norm(F) + 1e-9))
            a, b = a / (np.linalg.norm(a) + 1e-9), b / (np.linalg.norm(b) + 1e-9)
            p, d = self.W(orb.pos()), 0.24 * self.S() / 1.3
            m = VMobject(color=WHITE, stroke_width=2).set_stroke(opacity=0.9)
            m.set_points_as_corners([p + d * a, p + d * (a + b), p + d * b])
            return m.set_z_index(6)
        return always_redraw(f)

    def mk_p_marker(self, orb):
        """Passo p = |v∥|T medido ao longo de B, ao lado da hélice."""
        P = abs(orb.vpar) * T_PER
        off = -0.5

        def f():
            a0, a1 = self.W([off, 0.0, 0.0]), self.W([off, 0.0, P])
            g = VGroup(DashedLine(a0, a1, dash_length=0.12, color=WHITE, stroke_width=2.5),
                       DashedLine(self.W([0, 0, 0]), a0, dash_length=0.08, color=WHITE, stroke_width=1.5).set_opacity(0.6),
                       DashedLine(self.W([0, 0, P]), a1, dash_length=0.08, color=WHITE, stroke_width=1.5).set_opacity(0.6))
            g.add(Line(a0 + [-0.1, 0, 0], a0 + [0.1, 0, 0], color=WHITE, stroke_width=3),
                  Line(a1 + [-0.1, 0, 0], a1 + [0.1, 0, 0], color=WHITE, stroke_width=3))
            g.add(halo(eqc("p", size=M_M).move_to((a0 + a1) / 2 + np.array([-0.4, 0.0, 0.0]))))
            return g.set_z_index(2)
        return always_redraw(f)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B02 · movimento circular e ciclotron (nasce do estado final do B01: F_B = q v⊥ × B)
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def bloco_02_ciclotron(self):
        self.b02_transicao()
        self.b02_circulo()
        self.b02_raio()
        self.b02_omega()
        self.b02_duas()

    def b02_transicao(self):
        self.beta, self.tau = ValueTracker(90.0), ValueTracker(0.0)
        self.tt, self.tg = ValueTracker(0.0), ValueTracker(0.0)          # relógios: principal e das demonstrações
        self.tt_run = self.tg_run = False
        self.tt.add_updater(lambda m, dt: m.increment_value(dt) if self.tt_run else None)
        self.tg.add_updater(lambda m, dt: m.increment_value(dt) if self.tg_run else None)
        self.add(self.tt, self.tg)
        self.bop, self.bz1, self.bsparse = ValueTracker(1.0), ValueTracker(3.8), False
        self.o1 = Orbit(VP1, 0.0, 1, self.tt, 0.0, BLUE_L)
        self.vparB, self.vpar_op = ValueTracker(VPAR_B01), ValueTracker(0.5)

        # 1) sai o que era só da leitura angular do B01; a fórmula de F_B sobe para o topo
        self.play(*[FadeOut(m) for m in (self.arc, self.helper, self.th_lab, self.v_lab, self.v_arr, self.guides, self.lab_par_m,
                                         self.lab_perp_m, self.dec, self.zero, self.notes, self.b_lab)],
                  VGroup(self.lor, self.lor_box).animate.scale(0.8).move_to([CX, 2.55, 0]), run_time=1.0)
        # 2) o mesmo desenho do B01, agora gerado pela câmera 3D (visualmente idêntico): campo, carga, v⊥, v∥ e F_B
        self.b3 = self.mk_bgrid()
        self.q3 = self.mk_charge(self.o1)
        self.vp3 = self.mk_vec(self.o1, "v", WHITE, 6, 5)
        self.vl3 = self.mk_vec(self.o1, "vpar", VIOLET, 6, 4, vis=self.vparB, op=self.vpar_op)
        self.fm3 = self.mk_force_marks(self.o1)
        self.remove(self.b_mob, self.q_mob, self.v_par, self.v_perp, self.f_sym)
        self.add(self.b3, self.q3, self.vp3, self.vl3, *self.fm3)
        self.hold(0.4)
        # 3) mudança de perspectiva: a câmera gira até olharmos AO LONGO de B — as linhas de B viram pontos ⊙, v∥ aponta
        #    para o observador (some) e F_B sai da profundidade (⊗) e vira uma seta no plano da órbita
        look = txt("olhando ao longo de B", T_NOTE, opacity=0.9).move_to([CX, 0.9, 0])
        self.play(self.beta.animate.set_value(0.0), self.ox.animate.set_value(-4.2), self.oy.animate.set_value(-0.1),
                  FadeIn(look), run_time=3.6, rate_func=smooth)
        self.vparB.set_value(0.0)
        bleg = VGroup(eq(r"\mathbf B", r"\odot", size=M_M, colors={0: MAG, 1: MAG}),
                      txt("sai da tela", T_NOTE, opacity=0.85)).arrange(RIGHT, buff=0.25).move_to([CX, 1.6, 0])
        self.play(FadeOut(look), FadeIn(bleg), run_time=0.8)
        self.bleg = bleg

    def b02_circulo(self):
        o1 = self.o1
        o1.t0 = self.tt.get_value()
        self.tt_run = True
        self.trail1 = self.mk_trail(o1, 3.5)
        self.ra1 = self.mk_rightangle(o1)
        self.add(self.trail1, self.ra1)
        note = VGroup(eq(r"\mathbf F_B\perp\mathbf v", size=M_M, colors={0: FC}),
                      txt("só muda a direção de v", T_NOTE, opacity=0.9)).arrange(DOWN, buff=0.22).move_to([CX, 0.15, 0])
        self.play(FadeIn(note), run_time=0.8)
        self.hold(T_PER * 1.1)               # uma volta completa: o círculo nasce da força transversal
        self.note_perp = note

    def b02_raio(self):
        o1 = self.o1
        W1 = [CX, 1.45, 0]
        self.cline, self.clab = self.mk_center(o1, "R")
        self.add(self.cline, self.clab)
        self.play(FadeOut(self.note_perp), FadeOut(self.bleg), run_time=0.6)
        e1 = eq("|q|", r"v_\perp", "B", "=", "m", r"v_\perp", r"v_\perp", "/", "R", size=M_M).move_to(W1)
        self.play(FadeIn(e1, shift=0.1 * DOWN), run_time=1.0)
        self.hold(1.2)
        cr = VGroup(Cross(e1[1], stroke_color=WHITE, stroke_width=4), Cross(e1[5], stroke_color=WHITE, stroke_width=4))
        self.play(Create(cr), run_time=0.8)             # v⊥ cancela nos dois lados
        self.hold(0.5)
        e2 = eq("|q|", "B", "=", "m", r"v_\perp", "/", "R", size=M_M).move_to(W1)
        self.play(FadeOut(e1[1]), FadeOut(e1[5]), FadeOut(cr),
                  *[Transform(e1[i], e2[j]) for i, j in ((0, 0), (2, 1), (3, 2), (4, 3), (6, 4), (7, 5), (8, 6))],
                  run_time=1.4, rate_func=smooth)
        g2 = VGroup(*[e1[i] for i in (0, 2, 3, 4, 6, 7, 8)])      # g2[k] ↔ e2[k]
        self.hold(0.6)
        e3 = eq("R", "=", "m", r"v_\perp", "/", "(", "|q|", "B", ")", size=40).move_to(W1)
        self.play(*[Transform(g2[k], e3[j]) for k, j in ((6, 0), (2, 1), (3, 2), (4, 3), (5, 4), (0, 6), (1, 7))],
                  FadeIn(e3[5]), FadeIn(e3[8]), run_time=1.4, rate_func=smooth)
        boxR = box(e3)
        self.play(FadeIn(boxR), run_time=0.5)
        self.Rgrp = VGroup(g2[6], g2[2], g2[3], g2[4], g2[5], e3[5], g2[0], g2[1], e3[8], boxR)
        self.hold(0.6)

    def b02_omega(self):
        o1 = self.o1
        W2 = [CX, 0.4, 0]
        e4 = eq(r"\omega_c", "=", r"v_\perp", "/", "R", size=M_M).move_to(W2)
        self.play(FadeIn(e4, shift=0.1 * DOWN), run_time=1.0)
        self.hold(1.0)
        e5 = eq(r"\omega_c", "=", r"v_\perp", r"\cdot", "|q|B", "/", "(", "m", r"v_\perp", ")", size=34).move_to(W2)
        self.play(ReplacementTransform(e4, e5), run_time=1.2)
        self.hold(0.8)
        cr = VGroup(Cross(e5[2], stroke_color=WHITE, stroke_width=4), Cross(e5[8], stroke_color=WHITE, stroke_width=4))
        self.play(Create(cr), run_time=0.8)             # v⊥ cancela de novo
        self.hold(0.5)
        e6 = eq(r"\omega_c", "=", "|q|B", "/", "m", size=40).move_to(W2)
        self.play(*[FadeOut(e5[i]) for i in (2, 3, 6, 8, 9)], FadeOut(cr),
                  *[Transform(e5[i], e6[j]) for i, j in ((0, 0), (1, 1), (4, 2), (5, 3), (7, 4))],
                  run_time=1.4, rate_func=smooth)
        b6 = box(e6)
        self.play(FadeIn(b6), run_time=0.5)
        self.Wgrp = VGroup(*[e5[i] for i in (0, 1, 4, 5, 7)], b6)
        W3 = [CX, -0.65, 0]
        e7 = eq("T", "=", r"2\pi", "/", r"\omega_c", size=M_M).move_to(W3)
        self.play(FadeIn(e7, shift=0.1 * DOWN), run_time=0.9)
        self.hold(0.8)
        e8 = eq("T", "=", r"2\pi m", "/", "(", "|q|B", ")", size=40).move_to(W3)
        self.play(ReplacementTransform(e7, e8), run_time=1.2)
        b8 = box(e8)
        self.play(FadeIn(b8), run_time=0.5)
        self.Tgrp = VGroup(e8, b8)
        self.hold(1.0)

    def b02_duas(self):
        o1 = self.o1
        # espera a partícula 1 voltar à origem: a partícula 2 nasce no mesmo ponto, com o mesmo relógio
        w = (-o1.u()) % T_PER
        if w > 0.05:
            self.hold(w)
        o2 = Orbit(VP1 * 0.5, 0.0, 1, self.tt, self.tt.get_value(), WHITE)     # mesmos m, q, B; só v⊥ cai à metade
        self.o2 = o2
        tr2, q2 = self.mk_trail(o2, 3.5, 0.9), self.mk_charge(o2)
        c1l, c1t = self.mk_center(o1, "R_1")
        c2l, c2t = self.mk_center(o2, "R_2")
        t1, t2 = self.mk_tag(o1, "1"), self.mk_tag(o2, "2")
        self.remove(self.cline, self.clab)
        self.cline, self.clab = c1l, c1t
        self.add(tr2, q2, c1l, c1t, c2l, c2t, t1, t2)
        hyp1 = eq(r"m_1=m_2,\;q_1=q_2,\;B_1=B_2", size=28).move_to([CX, 0.45, 0])
        hyp2 = eq(r"v_{\perp 1}\neq v_{\perp 2}", size=34).move_to([CX, -0.2, 0])
        self.play(FadeOut(VGroup(self.lor, self.lor_box)), FadeOut(self.Wgrp), self.Rgrp.animate.move_to([CX, 2.3, 0]),
                  self.Tgrp.animate.move_to([CX, 1.3, 0]), FadeIn(hyp1), FadeIn(hyp2), run_time=1.4, rate_func=smooth)
        self.hold(T_PER * 1.0)
        ccl_r = eq(r"R_1\neq R_2", size=40, colors={})
        bR = box(ccl_r)
        gR = VGroup(ccl_r, bR).move_to([CX, -1.2, 0])
        self.play(FadeIn(gR, shift=0.1 * DOWN), run_time=0.8)
        self.hold(T_PER * 0.8)
        ccl_t = eq("T_1", "=", "T_2", size=40)
        gT = VGroup(ccl_t, box(ccl_t)).move_to([CX, -2.1, 0])
        self.play(FadeIn(gT, shift=0.1 * DOWN), run_time=0.8)
        self.hold(T_PER * 1.1)               # as duas completam a volta juntas
        self.demo2 = VGroup(tr2, q2, c2l, c2t, t1, t2, hyp1, hyp2, gR, gT)
        self.c1 = (c1l, c1t)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B03 · hélice (a mesma decomposição v = v∥ + v⊥ do B01, agora reconstruindo a trajetória espacial)
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def bloco_03_helice(self):
        self.b03_decomposicao()
        self.b03_perspectiva()
        self.b03_translacao()
        self.b03_passo()
        self.b03_variacoes()

    def b03_decomposicao(self):
        o1 = self.o1
        # sai a demonstração das duas partículas; fica a partícula 1 (o círculo), R e T
        self.remove(*self.c1)
        c1l, c1t = self.mk_center(o1, "R")
        self.cline, self.clab = c1l, c1t
        self.add(c1l, c1t)
        self.play(FadeOut(self.demo2), self.Rgrp.animate.move_to([CX, 1.5, 0]), self.Tgrp.animate.move_to([CX, 0.6, 0]),
                  run_time=1.2, rate_func=smooth)
        dec = eq(r"\mathbf v", "=", r"\mathbf v_\parallel", "+", r"\mathbf v_\perp", size=M_M, colors={2: VIOLET}).move_to([CX, 2.55, 0])
        row1 = VGroup(eq(r"\mathbf v_\perp", size=30), txt("→ círculo", T_BODY)).arrange(RIGHT, buff=0.3).move_to([CX, -0.6, 0])
        self.dec, self.row1 = dec, row1
        self.play(FadeIn(dec, shift=0.1 * DOWN), FadeIn(row1), run_time=1.2)
        self.hold(T_PER * 0.6)

    def b03_perspectiva(self):
        # a grade de B fica esparsa (senão vira floresta vertical) e a câmera inclina: o círculo vira elipse (ainda plano)
        self.play(self.bop.animate.set_value(0.0), run_time=0.5)
        self.bsparse = True
        self.bz1.set_value(7.6)
        self.play(self.bop.animate.set_value(0.55), self.tau.animate.set_value(45.0), self.gs.animate.set_value(0.8),
                  self.ox.animate.set_value(-4.0), self.oy.animate.set_value(-2.0), run_time=3.4, rate_func=smooth)
        self.hold(T_PER * 0.4)

    def b03_translacao(self):
        o1 = self.o1
        # v∥ entra: a seta cresce ao longo de B (colada à partícula) e o rótulo acompanha
        vlab = always_redraw(lambda: halo(eqc(r"\mathbf v_\parallel", size=M_M, colors={0: VIOLET}).move_to(
            self.W(o1.pos() + np.array([0.0, 0.0, self.vparB.get_value()])) + np.array([0.5, 0.1, 0.0])))
            .set_opacity(min(1.0, self.vparB.get_value() / 0.4)))
        self.add(vlab)
        row2 = VGroup(eq(r"\mathbf v_\parallel", size=30, colors={0: VIOLET}), txt("→ translação uniforme", T_BODY)
                      ).arrange(RIGHT, buff=0.3).move_to([CX, -1.4, 0])
        self.play(self.vparB.animate.set_value(VPAR), self.vpar_op.animate.set_value(1.0), FadeIn(row2), run_time=1.4,
                  rate_func=smooth)
        self.hold(0.6)
        # a translação começa quando a partícula volta à origem; a hélice cresce volta por volta
        w = (-o1.u()) % T_PER
        if w > 0.05:
            self.hold(w)
        o1.vpar = VPAR
        o1.u_on = o1.u()
        o1.u_max = o1.u_on + 1.6 * T_PER
        self.hold(T_PER * 1.0)
        row3 = txt("círculo + translação = hélice", T_BODY)
        b3 = box(row3)
        g3 = VGroup(row3, b3).move_to([CX, -2.3, 0])
        self.play(FadeIn(g3, shift=0.1 * DOWN), run_time=1.0)
        self.hold(T_PER * 0.6 + 0.2)
        self.tt_run = False                       # a hélice chegou ao fim (u_max); as demonstrações usam o relógio tg
        self.rows = VGroup(self.row1, row2, g3)
        self.vlab = vlab

    def b03_passo(self):
        o1 = self.o1
        self.pm = self.mk_p_marker(o1)
        self.add(self.pm)
        peq1 = eq("p", "=", r"|\mathbf v_\parallel|", "T", size=M_M, colors={2: VIOLET}).move_to([CX, -0.7, 0])
        self.play(FadeOut(self.rows), FadeIn(self.pm), FadeIn(peq1, shift=0.1 * DOWN), run_time=1.2)
        self.hold(1.0)
        peq2 = eq("p", "=", r"2\pi m|\mathbf v_\parallel|", "/", "(", "|q|B", ")", size=40, colors={2: VIOLET}).move_to([CX, -0.7, 0])
        self.play(ReplacementTransform(peq1, peq2), run_time=1.2)
        bp = box(peq2)
        self.play(FadeIn(bp), run_time=0.5)
        self.pgrp = VGroup(peq2, bp)
        self.hold(0.8)
        a = VGroup(eq(r"\mathbf v_\perp", r"\to", "R", size=32, colors={}), eq(r"\mathbf v_\parallel", r"\to", "p", size=32,
                                                                                 colors={0: VIOLET})).arrange(DOWN, buff=0.3).move_to([CX, -1.85, 0])
        self.play(FadeIn(a), run_time=0.8)
        self.arr_rows = a
        self.hold(1.0)

    def ghost(self, vp, vpar, s, color, turns):
        self.tg_run = False
        self.tg.set_value(0.0)
        g = Orbit(vp, vpar, s, self.tg, 0.0, color)
        g.u_on, g.u_max = 0.0, turns * T_PER
        tr, q = self.mk_trail(g, 3.5, 0.95), self.mk_charge(g)
        self.add(tr, q)
        self.tg_run = True
        return VGroup(tr, q)

    def b03_variacoes(self):
        n = [CX, -2.7, 0]
        # (a) v⊥ menor: o raio diminui, o passo não muda por esse motivo
        na = eq(r"v_\perp\downarrow\;\Rightarrow\;R\downarrow,\;p\ \text{igual}", size=30).move_to(n)
        ga = self.ghost(VP1 * 0.55, VPAR, 1, WHITE, 1.5)
        self.play(FadeIn(na), run_time=0.6)
        self.hold(1.5 * T_PER + 0.4)
        self.tg_run = False
        # (b) v∥ maior: o passo aumenta, o raio não muda
        nb = eq(r"v_\parallel\uparrow\;\Rightarrow\;p\uparrow,\;R\ \text{igual}", size=30).move_to(n)
        self.play(FadeOut(ga), ReplacementTransform(na, nb), run_time=0.8)
        gb = self.ghost(VP1, VPAR * 1.6, 1, WHITE, 1.0)
        self.hold(1.0 * T_PER + 0.4)
        self.tg_run = False
        # (c) q → −q: gira ao contrário, mas avança no mesmo sentido ao longo de B; R, T e p não mudam
        nc = eq(r"q\to-q:\ \text{gira ao contr\'ario},\ \text{avan\c{c}a igual}", size=28).move_to(n)
        self.play(FadeOut(gb), ReplacementTransform(nb, nc), run_time=0.8)
        gc = self.ghost(VP1, VPAR, -1, WHITE, 1.5)
        self.hold(1.5 * T_PER + 0.4)
        self.tg_run = False
        self.hold(2.0)
