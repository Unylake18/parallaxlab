"""yt_0005 — M1 Magnetostática. Bloco B01 · Do fenômeno à geometria da força de Lorentz (abertura + M1-01 a M1-06), preview sem voz.

Escopo: abertura · M1-01 dois fios (neutros, com corrente: atração/repulsão) · M1-02 da interação para uma carga,
F = q(E + v×B) → F_B = q v×B · M1-03 ângulo θ e |F_B| = |q|vB sinθ · M1-04 paralelo → oblíquo → perpendicular ·
M1-05 q → −q (dois estados discretos) · M1-06 v = v∥ + v⊥ e F_B = q v⊥×B. Para no M1-06; sem curvatura de trajetória.

Princípio: estado físico → grandezas derivadas → geometria. Estados: θ (th), sinal de q (qs, só ±1) e deformação dos fios (t).
v e B ficam no plano da tela (B ao longo de x); F_B = q v×B sai de np.cross e é desenhada com a simbologia padrão do plano:
⊗ (entra na tela) e ⊙ (sai da tela), com raio ∝ |F_B|. Com B = x̂ e v no plano, v×B aponta para dentro da tela quando q > 0.

Gramática: B magenta · E ciano · v branco · v∥ violeta · F_B azul claro · carga + azul / − violeta (sinal na partícula).

Preview:  uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_0005_magnetostatica_forca_lorentz/cena.py YT0005MagnetostaticaM1
GUIAS=1 mostra a safe area. SEG=K (aprofundamento analítico: Lorentz+Newton → EDO → ω_c → v(t) → x(t) → hélice), A (dedução de R, ω_c e T), C (duas partículas), B (hélice), D (B01→B02), E (B04), F (B05) ou G (B06) renderiza só esse trecho.
"""

import math
import os
import sys
from pathlib import Path

import numpy as np
from manim import (
    BOLD, DL, DOWN, LEFT, Indicate, RIGHT, UL, UR, UP, Arc, Arrow, Circle, Cross, Create, DashedLine, DecimalNumber, Dot, FadeIn, FadeOut,
    Flash, ImageMobject, Line, MathTex, VMobject, ParametricFunction, ReplacementTransform, Rotate, Scene, SurroundingRectangle,
    Transform, ValueTracker, VGroup, always_redraw, linear, smooth,
)
from manim import DashedVMobject, TransformMatchingTex, ManimColor, TransformFromCopy, interpolate_color
from manim import AnimationGroup, Axes, Ellipse, LaggedStart, Polygon, Rectangle, RoundedRectangle

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import DISPLAY_FONT, official_text, screen_text  # noqa: E402
from template.layout_horizontal import GUIAS, safe_guides  # noqa: E402

SEG = os.environ.get("SEG", "")
LOGO_PATH = Path(__file__).resolve().parents[2] / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR        # campo elétrico E
MAG = "#EA63FF"             # campo magnético B
BLUE = "#267BFF"            # carga positiva
BLUE_L = "#7FB2FF"          # fios
VIOLET = "#9C8CFF"          # v∥ · carga negativa
FC = "#5AA2FF"              # força magnética F_B
GREEN = "#3FE08B"           # CORRENTE (I, K, J): o mesmo verde do vid_0009; carga continua azul
PANEL = "#0E2A52"           # painel discreto azul-escuro (cards): mesmo espírito dos preenchimentos translúcidos do Gauss
HEADER = "ELETROMAGNETISMO · MAGNETOSTÁTICA"
WM_W, WM_OP = 1.92, 0.45
T_BODY, T_NOTE = 28, 24
M_L, M_M, M_S = 46, 38, 30
LW_VEC, LW_B, LW_WIRE = 5, 3, 6

VMAX = 2.2                  # |v| em unidades do diagrama (escala gs aplicada na tela)
Z_LINES = (-1.0, 1.0, 2.0, 3.0)   # poucas linhas de B (unidades do diagrama); z = 0 é a linha auxiliar de θ
FLUXO_B = 0.0               # B é uniforme e estacionário: as marcas ficam estáticas (sem escoamento)
FLUXO_I = 0.75              # velocidade dos portadores nos fios (unidades/s)
CX = 4.6                    # centro da coluna de análise (direita)


def txt(s, size=T_BODY, color=WHITE, opacity=1.0):
    return screen_text(s, size, color=color).set_opacity(opacity)


def fs(size):
    """Fonte de equação mais contida: acima de 32 pt a redução é progressiva (equações grandes pesavam e se sobrepunham)."""
    return size if size <= 32 else 32 + (size - 32) * 0.55


MAXW = 5.7          # largura máxima de uma equação (coluna direita ≈ 6 unidades)


def eq(*parts, size=M_M, colors=None):
    m = MathTex(*parts, font_size=fs(size), color=WHITE)
    for i, c in (colors or {}).items():
        m[i].set_color(c)
    if m.width > MAXW:
        m.scale(MAXW / m.width)
    return m


def halo(m):
    """Contorno na cor do fundo: o rótulo continua legível quando cruza uma linha de campo."""
    return m.set_stroke(BACKGROUND_COLOR, width=7, background=True)


def arrow(a, b, color, width=LW_VEC, z=3, tip=0.26):
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.35,
                 max_stroke_width_to_length_ratio=50).set_z_index(z)


def vec(a, b, color, width=5, z=4, tip=0.24):
    """Vetor cuja ponta termina EXATAMENTE em b (haste + triângulo próprio): usado onde a ponta precisa tocar um ponto."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    L = float(np.linalg.norm(b - a))
    if L < 1e-6:
        return VGroup()
    u = (b - a) / L
    tl = min(tip, 0.45 * L)
    n = np.array([-u[1], u[0], 0.0])
    head = Polygon(b, b - u * tl + n * tl * 0.42, b - u * tl - n * tl * 0.42, color=color, stroke_width=1).set_fill(color, 1)
    return VGroup(Line(a, b - u * tl * 0.8, color=color, stroke_width=width), head).set_z_index(z)


def panel(m, pad=0.28, op=0.55, color=PANEL, stroke=BLUE_L):
    """Card azul-escuro discreto atrás de um grupo (hierarquia visual do Gauss; sem caixa branca)."""
    r = RoundedRectangle(corner_radius=0.16, width=m.width + 2 * pad, height=m.height + 2 * pad, stroke_width=1.5)
    r.set_fill(color, op).set_stroke(stroke, 1.5, 0.55).move_to(m.get_center()).set_z_index(-1)
    return r


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


def RT(a, b, **kw):
    """Troca limpa entre duas representações: equações compatíveis preservam os termos iguais (TransformMatchingTex);
    o resto sai e entra por fade, sem deformar glifos diferentes em um amontoado ilegível."""
    if kw.pop("match", False) and isinstance(a, MathTex) and isinstance(b, MathTex):
        return TransformMatchingTex(a, b, **kw)
    return AnimationGroup(FadeOut(a), FadeIn(b))


def nome(*linhas, pos=(0.0, 0.0, 0.0)):
    """Título curto de um resultado consolidado. Cada linha é uma str ou uma lista de str/("m", tex); a 1ª linha é a principal."""
    g = VGroup()
    for k, ln in enumerate(linhas):
        itens = [ln] if isinstance(ln, (str, tuple)) else ln
        size, op = (22, 1.0) if k == 0 else (18, 0.8)
        row = VGroup(*[(eq(it[1], size=size + 2) if isinstance(it, tuple) else txt(it, size, opacity=op)) for it in itens]).arrange(RIGHT, buff=0.1)
        g.add(row)
    return g.arrange(DOWN, buff=0.06).move_to(list(pos))


def box(m, color=WHITE, pad=0.16):
    """Destaque em painel azul-escuro com contorno azul-claro (no lugar da caixa branca sobre o preto)."""
    r = RoundedRectangle(corner_radius=0.1, width=m.width + 2 * pad, height=m.height + 2 * pad)
    return r.move_to(m.get_center()).set_fill(PANEL, 0.6).set_stroke(BLUE_L if color == WHITE else color, 3).set_z_index(-1)


# ── B02/B03: parâmetros físicos (unidades do diagrama) e órbita ─────────────────────────────────────────────
MASS, ABSQ, BM = 1.0, 1.0, 2 * math.pi / 5.0   # m, |q|, B: ω = 2π/5 → T = 5,0 s = 150 quadros a 30 fps (voltas e gatilhos exatos)
OMEGA = ABSQ * BM / MASS                 # ω_c = |q|B/m
T_PER = 2 * math.pi / OMEGA              # T = 2πm/(|q|B)
VP1 = VMAX * math.sin(math.radians(60.0))        # |v⊥| herdado do fim do B01
VPAR_B01 = VMAX * math.cos(math.radians(60.0))   # v∥ do B01 (some quando olhamos ao longo de B)
E7, B7, DMAX, R8 = 1.2, 1.0, 0.55, 1.0           # B07/B08: E, B, deflexão máxima (qualitativa), raio na região só com B
VPAR = 0.5                               # v∥ da hélice (B03): p/(2R) ≈ 0,8
BX = (-1.2, 0.0, 1.2, 2.4, 3.6)                  # B02: colunas (profundidade no B01, onde coincidem)
BY = (-2.0, -1.0, 0.0, 1.0, 2.0, 3.0)            # B02: linhas
BX3, BY3 = (-1.3, 3.9), (-1.0, 1.0)              # B03: duas linhas paralelas ao eixo da hélice
TEXS = {"q": r"|q|", "vp": r"v_\perp", "vp2": r"v_\perp^2", "B": "B", "m": "m", "R": "R", "=": "=", "w": r"\omega_c", "T": "T",
        "2pi": r"2\pi", "p": "p", "vpar": r"|v_\parallel|", "1": "1"}
TEXS.update({
    "PB": "P_B", "FB": r"\mathbf F_B", "v": r"\mathbf v", "dot": r"\cdot", "qs": "q", "(": "(", ")": ")", "times": r"\times",
    "Bv": r"\mathbf B", "0": "0", "WB": "W_B", "int": r"\int", "dtt": r"\,dt", "dK": r"\Delta E_c", "dq": "dq", "lam": r"\lambda",
    "dl": r"d\ell", "dlv": r"d\boldsymbol\ell", "vs": "v", "vv": r"\mathbf v", "dt": "dt", "I": "I", "dF": r"d\mathbf F",
    "F": r"\mathbf F", "Kv": r"\mathbf K", "Jv": r"\mathbf J", "da": r"d\mathbf a", "dtau": r"d\tau", "Qi": r"Q_{\mathrm{int}}",
    "intV": r"\int_V", "rho": r"\rho", "ddt": r"\frac{d}{dt}", "neg": "-", "oint": r"\oint_{\partial V}", "div": r"\nabla\cdot\mathbf J",
    "drho": r"\frac{\partial\rho}{\partial t}", "plus": "+", "dA": "dA", "dQdt": r"\frac{dQ_{\mathrm{int}}}{dt}",
    "Ient": r"I_{\mathrm{ent}}", "Isai": r"I_{\mathrm{sai}}", "minus": "-", "FE": r"\mathbf F_E", "Ev": r"\mathbf E", "Es": "E",
    "Bs": "B", "yh": r"\hat{\mathbf y}", "Fy": "F_y", "Fyq": r"F_y/q", "B2": "B^2"})
# Cor por grandeza (paleta aprovada): B magenta · força azul claro · velocidade/tempo violeta · carga azul · corrente, E e energia ciano
BASECOL = {"B": MAG, "Bv": MAG, "FB": FC, "dF": FC, "F": FC,
           "vp": VIOLET, "vp2": VIOLET, "vpar": VIOLET, "v": VIOLET, "vv": VIOLET, "vs": VIOLET, "w": VIOLET, "T": VIOLET,
           "dt": VIOLET, "dtt": VIOLET,
           "q": BLUE_L, "qs": BLUE_L, "dq": BLUE_L, "lam": BLUE_L, "Qi": BLUE_L, "rho": BLUE_L, "drho": BLUE_L, "dQdt": BLUE_L,
           "FE": FC, "Ev": CYAN, "Es": CYAN, "Bs": MAG, "Fy": FC, "Fyq": FC, "B2": MAG, "I": GREEN, "Kv": GREEN, "Jv": GREEN, "div": GREEN, "PB": CYAN, "WB": CYAN, "Ient": GREEN, "Isai": GREEN}


class Orbit:
    """Movimento de uma carga em B = B ẑ: todas as grandezas vêm de (m, |q|, B, v⊥, v∥, sinal de q) e de um relógio.

    R = m v⊥/(|q|B) · ω = |q|B/m · T = 2π/ω · passo p = |v∥| T. Órbitas que compartilham o relógio têm a mesma ω:
    completam as voltas juntas sem sincronização manual. A força é F = q v×B, calculada com np.cross."""

    def __init__(self, vp, vpar, s, clock, t0, color):
        self.vp, self.vpar, self.s, self.clock, self.t0, self.color = vp, vpar, s, clock, t0, color
        self.R = MASS * vp / (ABSQ * BM)
        self.a0 = math.pi if s > 0 else 0.0              # começa na origem; o centro fica do lado de F = q v×B
        self.C = -self.R * np.array([math.cos(self.a0), math.sin(self.a0), 0.0])
        self.u_max = 1e9

    def u(self):
        return min(max(0.0, self.clock.get_value() - self.t0), self.u_max)

    def pos(self, u=None):
        u = self.u() if u is None else u
        a = self.a0 - self.s * OMEGA * u
        # v∥ é uma condição inicial constante: z = v∥ t desde t = 0 (sem rampa; B não acelera a componente paralela)
        return np.array([self.C[0] + self.R * math.cos(a), self.C[1] + self.R * math.sin(a), self.vpar * u])

    def vel(self, u=None):
        u = self.u() if u is None else u
        a = self.a0 - self.s * OMEGA * u
        return np.array([self.s * OMEGA * self.R * math.sin(a), -self.s * OMEGA * self.R * math.cos(a), self.vpar])

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

    def seg(self, name):
        """SEG=A|B renderiza só um trecho (os demais rodam sem gerar quadros): A = dedução do B02 · B = hélice do B03."""
        if SEG in ("R1", "R2", "R3", "R4"):
            self.next_section(name, skip_animations=(self.cur_r != SEG))
            return
        ativo = (not SEG) or SEG == name or (SEG == "F" and name == "F2") or (SEG == "KA" and name in ("K", "Kend", "rest0", "A")) or (SEG == "B03" and name in ("B", "Bx"))
        self.next_section(name, skip_animations=not ativo)

    def rsec(self, r):
        """Fronteira dos previews de redesign (SEG=R1..R4): só o grupo escolhido gera quadros; os outros rodam sem render."""
        self.cur_r = r
        if SEG in ("R1", "R2", "R3", "R4"):
            self.next_section(r, skip_animations=(SEG != r))

    def hold(self, d):
        """Pausa que não congela o quadro: o wait() padrão do Manim vira imagem estática quando os updaters não usam dt
        (always_redraw), o que parava o fluxo de B, os portadores e os vetores a cada pausa."""
        self.wait(d, frozen_frame=False)

    def construct(self):
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(WM_W).set_opacity(WM_OP).to_corner(UR, buff=0.3)
        self.tag = txt(HEADER, 18, opacity=0.6).to_corner(UL, buff=0.38)
        if GUIAS:
            self.add(safe_guides())
        self.cores_novas = True          # cor semântica por grandeza em todo o vídeo (corrente verde, carga azul, B magenta...)
        self.cur_r = "R1"
        self.seg("pre")
        self.rsec("R1")
        self.abertura()
        self.bloco_01_lorentz()
        self.bloco_02_ciclotron()
        self.bloco_03_helice()
        self.rsec("R2")
        self.bloco_04_trabalho()
        self.bloco_05_correntes()
        self.rsec("R3")
        self.bloco_06_continuidade()
        self.rsec("R4")
        self.bloco_07_thomson()
        self.bloco_08_qm()
        self.bloco_09_fechamento()

    # ── abertura ───────────────────────────────────────────────────────────────────────────────────────────────
    def abertura(self):
        brand = txt("PARALLAX LAB", 22, opacity=0.8).move_to([0, 2.05, 0])
        title = official_text("MAGNETOSTÁTICA", DISPLAY_FONT, BOLD, 58).move_to([0, 1.2, 0])
        ask = txt("O que um campo magnético realmente faz?", 30, opacity=0.9).move_to([0, 0.25, 0])
        self.play(FadeIn(brand, shift=0.1 * DOWN), FadeIn(title, shift=0.15 * DOWN), FadeIn(self.wm), run_time=1.2)
        self.play(FadeIn(ask), run_time=0.9)
        self.hold(2.4)
        # o título vira o cabeçalho de série; a pergunta cede ao primeiro fenômeno
        self.play(FadeOut(brand), FadeOut(ask), FadeOut(title), run_time=0.8)
        self.play(FadeIn(self.tag), run_time=0.5)

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
                    g.add(Line([wx(sign, y), y, 0], [wx(sign, y2), y2, 0], color=GREEN, stroke_width=5).set_opacity(0.95 * op))
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
        cur_l = arrow([-2.75, 0.6, 0], [-2.75, 1.7, 0], GREEN, 6)
        cur_r = arrow([2.75, 0.6, 0], [2.75, 1.7, 0], GREEN, 6)
        i_l = eq("I_1", size=M_S, colors={0: GREEN}).next_to(cur_l, LEFT, buff=0.15)
        i_r = eq("I_2", size=M_S, colors={0: GREEN}).next_to(cur_r, RIGHT, buff=0.15)

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
        self.play(RT(cap2, cap3), run_time=0.8)
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
        X0, X1 = -2.0, 3.8

        def b_lines():
            """Poucas linhas de B: contínuas, estáticas, finas, com a ponta que indica o sentido."""
            g = VGroup()
            for z in Z_LINES:
                if not -3.05 < self.P(0, z)[1] < 3.05:
                    continue
                g.add(Line(self.P(X0, z), self.P(X1 - 0.3, z), color=MAG, stroke_width=2.2).set_opacity(0.5))
                g.add(arrow(self.P(X1 - 0.3, z), self.P(X1, z), MAG, 2.2, 1, tip=0.18).set_opacity(0.5))
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
        self.nome_F = nome("Força magnética", "parcela magnética da força de Lorentz", pos=(CX, 3.0, 0))
        # E sai e o termo magnético se fecha numa só passagem contínua; a caixa nasce já no destino
        self.play(AnimationGroup(AnimationGroup(*[FadeOut(full[i]) for i in (3, 4, 5, 9)]),
                                 AnimationGroup(*[Transform(full[a], short[b]) for a, b in pairs]),
                                 FadeIn(self.lor_box), FadeIn(self.nome_F), lag_ratio=0.35), run_time=2.0, rate_func=smooth)
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
        self.play(th.animate.set_value(45.0), RT(cap_par, cap_obl), run_time=2.0, rate_func=smooth)
        self.hold(1.2)
        self.play(th.animate.set_value(90.0), RT(cap_obl, cap_per), run_time=2.0, rate_func=smooth)
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
        self.play(Flash(self.O(), color=VIOLET, flash_radius=0.7, line_length=0.18), RT(e_pos, e_neg),
                  FadeIn(note), run_time=0.8)
        self.hold(2.0)
        qs.set_value(1.0)
        self.play(Flash(self.O(), color=BLUE, flash_radius=0.7, line_length=0.18), FadeOut(e_neg), FadeOut(note), run_time=0.8)
        self.hold(0.6)

    # ── M1-06 · decomposição da velocidade ────────────────────────────────────────────────────────────────
    def m1_06_decomposicao(self):
        th = self.th
        # FOCUS: o diagrama ganha espaço; a fórmula magnética desce para virar a conclusão
        self.play(FadeOut(self.mag), FadeOut(self.nome_F), FadeOut(self.readout), run_time=0.6)
        self.play(th.animate.set_value(60.0), self.ox.animate.set_value(-3.7),
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
        self.seg("D")                              # SEG=D: começa aqui (fim do M1-06) e vai até o início da curvatura no B02
        # conclusão: F_B = q v⊥ × B (a mesma força: a geometria de F_B não muda)
        final = eq(r"\mathbf F_B", "=", "q", r"\mathbf v_\perp", r"\times", r"\mathbf B", size=M_L,
                   colors={0: FC, 5: MAG}).move_to([CX, -0.45, 0])
        self.play(*[Transform(self.lor[i], final[i]) for i in range(6)], Transform(self.lor_box, box(final)),
                  run_time=1.4, rate_func=smooth)
        self.hold(1.2)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # Infraestrutura 3D → tela: câmera com guinada β (90°: B horizontal, como no B01 · 0°: olhando ao longo de B) e
    # inclinação τ (0°: plano da órbita de frente · >0°: vista mais lateral). Mundo: B ao longo de z.
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def W(self, p):
        b, t = math.radians(self.beta.get_value()), math.radians(self.tau.get_value())
        x, y, z = float(p[0]), float(p[1]), float(p[2])
        xp = x * math.cos(b) + z * math.sin(b)
        zp = -x * math.sin(b) + z * math.cos(b)
        return self.O() + self.S() * np.array([xp, y * math.cos(t) + zp * math.sin(t), 0.0])

    def Wv(self, v):
        return self.W(np.asarray(v, dtype=float)) - self.W(np.zeros(3))

    def depth(self, p):
        """Profundidade (maior = mais perto do observador) de um ponto do mundo."""
        b, t = math.radians(self.beta.get_value()), math.radians(self.tau.get_value())
        x, y, z = float(p[0]), float(p[1]), float(p[2])
        zp = -x * math.sin(b) + z * math.cos(b)
        return zp * math.cos(t) - y * math.sin(t)

    def mk_bgrid(self):
        """Campo B uniforme e ESTÁTICO. Poucas linhas contínuas e finas (com a ponta do sentido); ao olhar ao longo de B,
        as mesmas linhas viram poucos símbolos ⊙."""
        cache = {}
        SETS = {"b01": (BX, BY, 0.14, -2.0), "b02": (BX, BY, 0.14, -2.0), "b03": (BX3, BY3, 0.5, -0.3)}

        def f():
            key = (round(self.beta.get_value(), 2), round(self.tau.get_value(), 2), round(self.ox.get_value(), 3),
                   round(self.oy.get_value(), 3), round(self.gs.get_value(), 3), self.bmode, round(self.bop.get_value(), 3),
                   round(self.bz1.get_value(), 2))
            if cache.get("k") == key:
                return cache["g"]
            g = VGroup()
            xs, ys, base, z0 = SETS[self.bmode]
            z1 = self.bz1.get_value()
            for y in ys:
                row = 1.0 if y != 0.0 else min(1.0, max(0.0, (90.0 - self.beta.get_value()) / 30.0))   # z = 0: auxiliar de θ no B01
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
                        pe = p1 - (p1 - p0) / L * 0.3
                        g.add(Line(p0, pe, color=MAG, stroke_width=2.2).set_opacity(op * base * lf))
                        g.add(arrow(pe, p1, MAG, 2.2, 1, tip=0.16).set_opacity(op * base * lf))
                    if lf < 0.99:
                        s = 0.075 * self.S() / 1.15
                        oc = 0.4 * op * (1 - lf)
                        g.add(Circle(radius=s, color=MAG, stroke_width=2).set_opacity(oc).move_to(p1))
                        g.add(Dot(p1, radius=0.025, color=MAG).set_opacity(oc))
            cache["k"], cache["g"] = key, g
            return g

        return always_redraw(f)

    def mk_charge(self, orb):
        return always_redraw(lambda: charge_c(self.W(orb.pos()), orb.s, max(0.8, self.S() / 1.15)))

    def mk_trail(self, orb, width=3.5, op=0.9, optr=None):
        """Trilha da órbita. Com a câmera inclinada, trechos mais próximos ficam mais claros e grossos e são desenhados
        por cima dos mais distantes (leitura de profundidade)."""
        def f():
            u = orb.u()
            if u < 0.03:
                return VGroup()
            o = optr.get_value() if optr is not None else op
            us = np.linspace(0.0, u, int(min(480, max(8, u / 0.06))))
            P3 = [orb.pos(x) for x in us]
            pts = [self.W(p) for p in P3]
            if self.tau.get_value() < 8:
                m = VMobject(color=orb.color, stroke_width=width).set_stroke(opacity=o)
                m.set_points_as_corners(pts)
                return m.set_z_index(3)
            sb, st = math.sin(math.radians(self.beta.get_value())), math.sin(math.radians(self.tau.get_value()))
            cb = math.cos(math.radians(self.beta.get_value()))
            R = max(orb.R, 1e-6)
            chunks = []
            for i in range(0, len(pts) - 1, 5):
                j = min(i + 6, len(pts))
                mid = P3[(i + j) // 2]
                lx, ly = mid[0] - orb.C[0], mid[1] - orb.C[1]
                near = min(1.0, max(0.0, 0.5 + (-ly * st + (-lx * sb) * cb * st * 0.0 + (-lx * sb) * 0.5) / (2.0 * R)))
                m = VMobject(color=orb.color, stroke_width=width * (0.55 + 0.75 * near)).set_stroke(opacity=o * (0.3 + 0.7 * near))
                m.set_points_as_corners(pts[i:j])
                chunks.append((near, m))
            chunks.sort(key=lambda c: c[0])
            return VGroup(*[m for _, m in chunks]).set_z_index(3)
        return always_redraw(f)

    def mk_vec(self, orb, kind, color, width=5.0, z=4, vis=None, op=None, sc=1.0):
        """Seta ancorada na partícula: 'v' (v⊥, sem a componente z) · 'vpar' (comprimento em vis) · 'F' (F = q v×B)."""
        def f():
            p = orb.pos()
            if kind == "v":
                vec = orb.vel() * np.array([1.0, 1.0, 0.0])
            elif kind == "vpar":
                vec = np.array([0.0, 0.0, vis.get_value()])
            else:
                vec = orb.force() * (0.5 / (ABSQ * BM))
            a, b = self.W(p), self.W(p + vec * sc)
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

    def mk_p_marker(self, orb, optr=None):
        """Passo p = |v∥|T: cota entre dois pontos CONSECUTIVOS de mesma fase (α = π), ao lado da hélice."""
        P = abs(orb.vpar) * T_PER
        x0 = orb.C[0] - orb.R                     # ponto de fase α = π (o mais à esquerda)
        off = x0 - 0.5

        def f():
            a0, a1 = self.W([off, 0.0, 0.0]), self.W([off, 0.0, P])
            g = VGroup(DashedLine(a0, a1, dash_length=0.12, color=WHITE, stroke_width=2.5),
                       DashedLine(self.W([x0, 0, 0]), a0, dash_length=0.08, color=WHITE, stroke_width=1.5).set_opacity(0.6),
                       DashedLine(self.W([x0, 0, P]), a1, dash_length=0.08, color=WHITE, stroke_width=1.5).set_opacity(0.6))
            g.add(Line(a0 + [-0.1, 0, 0], a0 + [0.1, 0, 0], color=WHITE, stroke_width=3),
                  Line(a1 + [-0.1, 0, 0], a1 + [0.1, 0, 0], color=WHITE, stroke_width=3))
            g.add(halo(eqc("p", size=M_M).move_to((a0 + a1) / 2 + np.array([-0.4, 0.0, 0.0]))))
            g.set_z_index(2)
            return g.set_opacity(optr.get_value()) if optr is not None else g
        return always_redraw(f)

    # ── álgebra em frações verticais reais ───────────────────────────────────────────────────────────────────
    def build(self, spec, size):
        """spec: lista de tokens; ("f", numerador, denominador, nome_da_barra) é uma fração vertical (pode aninhar).
        Devolve (grupo, {nome: mobject}); o sufixo @x distingue ocorrências do mesmo símbolo."""
        pieces = {}

        def mk(tok):
            if isinstance(tok, tuple):
                _, num, den, bname = tok
                ng = VGroup(*[mk(t) for t in num]).arrange(RIGHT, buff=0.14)
                dg = VGroup(*[mk(t) for t in den]).arrange(RIGHT, buff=0.14)
                w = max(ng.width, dg.width) + 0.3
                bar = Line(LEFT * w / 2, RIGHT * w / 2, color=WHITE, stroke_width=3)
                pieces[bname] = bar
                return VGroup(ng, bar, dg).arrange(DOWN, buff=0.14)
            base = tok.split("@")[0]
            m = MathTex(TEXS[base], font_size=fs(size), color=(BASECOL.get(base, WHITE) if getattr(self, "cores_novas", False)
                                                        else (MAG if base in ("B", "Bv") else (FC if base in ("FB", "dF", "F") else WHITE))))
            pieces[tok] = m
            return m

        root = VGroup(*[mk(t) for t in spec]).arrange(RIGHT, buff=0.22)
        if root.width > MAXW:
            root.scale(MAXW / root.width)
        return root, pieces

    def morph(self, spec, size, at, alias=None, run=1.3, first=False):
        root, new = self.build(spec, size)
        root.move_to(at)
        old = {} if first else self.cur
        alias = alias or {}
        anims = []
        for k, m in old.items():
            if k in alias and alias[k]:
                anims.append(FadeOut(m))
                anims.extend(FadeIn(new[t]) for t in alias[k])
            elif k in new:
                anims.append(ReplacementTransform(m, new[k]))
            else:
                anims.append(FadeOut(m))
        aliased = {t for v in alias.values() for t in v}
        for k, m in new.items():
            if k not in old and k not in aliased:
                anims.append(FadeIn(m))
        self.play(*anims, run_time=run, rate_func=smooth)
        self.cur = new
        return new

    def strike(self, a, b):
        """Cancelamento limpo: destaca os dois fatores e risca cada um com um traço diagonal fino."""
        for m in (a, b):
            m.set_color(VIOLET)
        lines = VGroup(*[Line(m.get_corner(DL) + 0.04 * LEFT, m.get_corner(UR) + 0.04 * RIGHT, color=VIOLET, stroke_width=2.5)
                         for m in (a, b)])
        self.play(Indicate(a, color=VIOLET, scale_factor=1.15), Indicate(b, color=VIOLET, scale_factor=1.15), run_time=0.8)
        self.play(Create(lines), run_time=0.6)
        return lines

    def clear_alg(self, extra=()):
        mobs = list(self.cur.values()) + list(extra)
        self.play(*[FadeOut(m) for m in mobs], run_time=0.6)
        self.cur = {}

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B02 · movimento circular e ciclotron (nasce do estado final do B01: F_B = q v⊥ × B)
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def bloco_02_ciclotron(self):
        self.b02_transicao()
        self.b02_analitico()
        self.seg("Kend")
        self.b02_circulo()
        self.seg("A")
        self.b02_algebra()
        self.seg("C")
        self.b02_duas()

    def b02_transicao(self):
        self.beta, self.tau = ValueTracker(90.0), ValueTracker(0.0)
        self.tt, self.tg, self.tv = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)     # relógios independentes
        self.run = {"tt": False, "tg": False, "tv": False}
        for name in ("tt", "tg", "tv"):
            getattr(self, name).add_updater(lambda m, dt, n=name: m.increment_value(dt) if self.run[n] else None)
        self.add(self.tt, self.tg, self.tv)
        self.bop, self.bz1, self.bmode = ValueTracker(1.0), ValueTracker(3.8), "b01"
        self.o1 = Orbit(VP1, 0.0, 1, self.tt, 0.0, BLUE_L)
        self.vparB, self.vpar_op = ValueTracker(VPAR_B01), ValueTracker(0.5)

        # 1) sai o que era só da leitura angular do B01; a fórmula de F_B sobe para o topo
        self.play(*[FadeOut(m) for m in (self.arc, self.helper, self.th_lab, self.v_lab, self.v_arr, self.guides, self.lab_par_m,
                                         self.lab_perp_m, self.zero, self.notes, self.b_lab, self.dec)],
                  VGroup(self.lor, self.lor_box).animate.scale(0.8).move_to([CX, 2.55, 0]), run_time=1.0)
        # 2) o mesmo desenho do B01, agora gerado pela câmera 3D (visualmente idêntico)
        self.b3 = self.mk_bgrid()
        self.q3 = self.mk_charge(self.o1)
        self.vp3 = self.mk_vec(self.o1, "v", WHITE, 6, 5)
        self.vl3 = self.mk_vec(self.o1, "vpar", VIOLET, 6, 4, vis=self.vparB, op=self.vpar_op)
        self.fm3 = self.mk_force_marks(self.o1)
        self.remove(self.b_mob, self.q_mob, self.v_par, self.v_perp, self.f_sym)
        self.add(self.b3, self.q3, self.vp3, self.vl3, *self.fm3)
        self.hold(0.4)
        gen = eq(r"\mathbf v", "=", r"\mathbf v_\parallel", "+", r"\mathbf v_\perp", size=M_L, colors={2: VIOLET}).move_to([CX, 1.2, 0])
        self.play(FadeIn(gen, shift=0.1 * DOWN), run_time=0.8)           # caso geral, já sem encostar na caixa de F_B
        self.hold(0.6)
        # 3) HIPÓTESE: para estudar o movimento circular escolhemos o caso especial v∥ = 0 (v = v⊥). Não é a câmera que
        #    remove v∥: é uma escolha de condição inicial.
        case = eq(r"\mathbf v", "=", r"\mathbf v_\perp", size=M_L).move_to([CX, 1.2, 0])
        hyp = VGroup(txt("agora vamos escolher o caso", T_BODY, opacity=0.95),
                     eq(r"v_\parallel=0", size=M_L, colors={0: VIOLET})).arrange(DOWN, buff=0.3).move_to([CX, -0.8, 0])
        hb = box(hyp[1])
        self.play(RT(gen, case), FadeIn(hyp[0]), FadeIn(hyp[1]), FadeIn(hb), run_time=1.2)
        self.hold(0.6)
        self.play(self.vparB.animate.set_value(0.0), run_time=1.4, rate_func=smooth)
        self.vl3.clear_updaters()                       # encerra o v∥ do B01: B03 constrói o seu próprio, com sua condição inicial
        self.remove(self.vl3)
        self.hold(0.4)
        # 4) só agora muda a representação: olhar ao longo de B (as linhas viram ⊙; F_B sai da profundidade)
        look = txt("a perspectiva muda; a física não", T_BODY, opacity=0.95).move_to([CX, -2.2, 0])
        self.bmode = "b02"
        self.play(FadeIn(look), run_time=0.6)
        self.play(self.beta.animate.set_value(0.0), self.ox.animate.set_value(-4.2), self.oy.animate.set_value(-0.1),
                  run_time=3.6, rate_func=smooth)
        self.hold(0.6)
        bleg = VGroup(eq(r"\mathbf B", r"\odot", size=M_M, colors={0: MAG, 1: MAG}),
                      txt("sai da tela", T_NOTE, opacity=0.85)).arrange(RIGHT, buff=0.25).move_to([CX, 1.6, 0])
        self.play(FadeOut(look), FadeOut(hyp), FadeOut(hb), FadeOut(case), FadeIn(bleg), run_time=0.8)
        self.bleg = bleg

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B02 · aprofundamento analítico (SEG=K): Lorentz + Newton → equações por componentes → EDO harmônica → ω_c
    #       → v_y(t), v_z(t) senoidais → integração → círculo e R → v_x constante → hélice
    # Convenção: B = B x̂; na vista ao longo de B (⊙) a tela mostra y para a direita e z para cima (x̂ sai da tela).
    # Condição inicial escolhida para coincidir com a órbita já desenhada: v_y(0) = 0, v_z(0) = v⊥ (a carga sobe e gira
    # no sentido horário): v_y = v⊥ sen ωt, v_z = v⊥ cos ωt; y = R(1 − cos ωt), z = R sen ωt (origem na posição inicial).
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def b02_analitico(self):
        """Aprofundamento analítico. A física fica viva à esquerda (a órbita continua girando) e cada passo de álgebra nasce no
        lado direito como transformação do que está na tela: produto vetorial por componentes → Newton → equações por componente
        → EDO harmônica → solução (sin/cos, condições iniciais) → integração → circunferência → v_x constante → hélice.
        Convenção: B = B x̂; na vista ao longo de B (⊙) a tela mostra y para a direita e z para cima (x̂ sai da tela).
        Condição inicial: v_y(0) = 0, v_z(0) = v⊥ (a carga sobe e gira no sentido horário); y = R(1 − cos ωt), z = R sen ωt."""
        self.seg("K")
        o1, fm, TP = self.o1, self.fm3, T_PER
        kop, kop2, kc, kf = ValueTracker(1.0), ValueTracker(1.0), ValueTracker(0.0), ValueTracker(0.0)
        ktr, qsK = ValueTracker(0.9), ValueTracker(1.0)
        vyg, vzg, fyg, fzg = ValueTracker(1.0), ValueTracker(1.0), ValueTracker(0.0), ValueTracker(0.0)   # destaque por componente
        RX = 3.9
        BOXB = 0.12

        def bx(m, b=0.2):
            return box(m, pad=b)

        def tc(color, s):
            return s          # o template do Manim não carrega xcolor: sem \textcolor; a cor por grandeza vale nos tokens separados

        QB = rf"\frac{{{tc(BLUE_L, 'q')}{tc(MAG, 'B')}}}{{m}}"

        def G(fn, trk=None):
            """always_redraw com porta de opacidade que escala traço e preenchimento existentes (sem preencher curvas)."""
            trk = kop if trk is None else trk

            def g():
                m, k = fn(), trk.get_value()
                for sm in m.family_members_with_points():
                    sm.set_stroke(opacity=sm.get_stroke_opacity() * k)
                    sm.set_fill(opacity=sm.get_fill_opacity() * k)
                return m
            return always_redraw(g)

        def u_now():
            return self.tt.get_value() - o1.t0

        def finish_turn():
            """roda o relógio até completar a volta (a carga volta exatamente à origem)"""
            u = max(u_now(), 0.0) % TP
            rem = (TP - u) if u > 0.02 else 0.0
            if rem > 0.0:
                self.run["tt"] = True
                self.hold(rem)
                self.run["tt"] = False

        def comp_overlay(vecfn, scale, color, names, trk, gh, gv):
            """componentes (horizontal = y, vertical = z) do vetor, finas e atrás do vetor principal; cada uma com seu destaque"""
            def g():
                P = self.W(o1.pos())
                v = vecfn()
                grp = VGroup()
                for k, d in enumerate((self.Wv(np.array([v[0] * scale, 0.0, 0.0])), self.Wv(np.array([0.0, v[1] * scale, 0.0])))):
                    L = float(np.linalg.norm(d))
                    gate = (gh if k == 0 else gv).get_value()
                    if L > 0.15 and gate > 0.01:
                        grp.add(arrow(P, P + d, color, 2.5 + 2.0 * (gate > 0.9), 2, tip=0.13).set_opacity(0.95 * gate))
                        nm = names[0] if abs(d[0]) > abs(d[1]) else names[1]
                        grp.add(eqc(nm, size=30, colors={0: color}).move_to(P + d + d / L * 0.34).set_z_index(7).set_opacity(gate))
                return grp
            return G(g, trk)

        # ── 0 · composição: desenho à esquerda, equação à direita ──
        o1.t0 = self.tt.get_value()
        tri = VGroup(arrow([-6.6, -2.9, 0], [-5.9, -2.9, 0], WHITE, 3, 2, tip=0.14), arrow([-6.6, -2.9, 0], [-6.6, -2.2, 0], WHITE, 3, 2, tip=0.14),
                     Circle(radius=0.09, color=MAG, stroke_width=2.5).move_to([-6.6, -2.9, 0]), Dot([-6.6, -2.9, 0], radius=0.03, color=MAG),
                     eq("y", size=28).move_to([-5.7, -2.9, 0]), eq("z", size=28).move_to([-6.6, -2.0, 0]),
                     eq(r"\hat{\mathbf x}\ (\mathbf B)", size=24, colors={0: MAG}).move_to([-6.1, -3.3, 0]))
        vcomp = comp_overlay(lambda: o1.vel(), 1.0, VIOLET, ("v_y", "v_z"), kc, vyg, vzg)
        fcomp = comp_overlay(lambda: o1.force(), 0.5 / (ABSQ * BM), FC, ("F_y", "F_z"), kf, fyg, fzg)
        self.add(vcomp, fcomp)

        # ── 1 · eixos e componentes ──
        cap1 = txt("escolha de eixos: B ao longo de x", T_NOTE, opacity=0.95).move_to([RX, 2.9, 0])
        l1 = eq(r"\mathbf B", "=", "B", r"\hat{\mathbf x}", size=M_L, colors={0: MAG, 2: MAG, 3: MAG}).move_to([RX, 1.6, 0])
        self.play(FadeOut(self.lor), FadeOut(self.lor_box), FadeOut(self.bleg), FadeOut(fm[2]), FadeIn(tri), FadeIn(cap1), FadeIn(l1, shift=0.1 * UP), run_time=1.2)
        self.play(self.tt.animate.set_value(o1.t0 + TP / 8), run_time=1.6)           # a carga avança 1/8 de volta: v tem duas componentes
        l2 = eq(r"\mathbf v", "=", r"(v_x,\,v_y,\,v_z)", size=M_L, colors={0: VIOLET, 2: VIOLET}).move_to([RX, 0.1, 0])
        self.play(FadeIn(l2, shift=0.1 * UP), kc.animate.set_value(1.0), run_time=1.0)
        nvx = eq(r"v_x\ \text{ao longo de}\ \mathbf B\ (\odot)", size=28, colors={}).move_to([RX, -1.2, 0])
        self.play(FadeIn(nvx), run_time=0.7)
        self.hold(2.4)

        # ── 2 · produto vetorial: o determinante é construído por componentes (i, j, k) ──
        ref1 = eq(r"\mathbf B=B\,\hat{\mathbf x},\quad \mathbf v=(v_x,\,v_y,\,v_z)", size=26).move_to([RX, 3.2, 0])
        SZc = 36
        colx = [RX - 0.35 + 1.15 * j for j in range(3)]
        rowy = [2.3 - 0.62 * i for i in range(3)]
        labs = [[r"\hat{\mathbf x}", r"\hat{\mathbf y}", r"\hat{\mathbf z}"], ["v_x", "v_y", "v_z"], ["B", "0", "0"]]
        cc = [[WHITE] * 3, [VIOLET] * 3, [MAG, WHITE, WHITE]]
        cell = [[MathTex(labs[i][j], font_size=SZc, color=cc[i][j]).move_to([colx[j], rowy[i], 0]) for j in range(3)] for i in range(3)]
        bars = VGroup(*[Line([colx[0] - 0.62 + dx, rowy[0] + 0.36, 0], [colx[0] - 0.62 + dx, rowy[2] - 0.36, 0], color=WHITE, stroke_width=2.5)
                        for dx in (0.0, colx[2] - colx[0] + 1.24)])
        dlab = eq(r"\mathbf v\times\mathbf B", "=", size=36, colors={0: VIOLET}).next_to(bars[0], LEFT, buff=0.22)
        mat = VGroup(bars, dlab, *[c for r in cell for c in r])

        def hl(cs):
            return VGroup(*[SurroundingRectangle(c, color=(WHITE if k == 0 else VIOLET), buff=0.1, stroke_width=2.5, corner_radius=0.06)
                            for k, c in enumerate(cs)])

        ZD = r"\cdot 0"
        t_i = eq(r"\hat{\mathbf x}", "(", "v_y", ZD + "-", "v_z", ZD, ")", "=", "0", size=36, colors={2: VIOLET, 4: VIOLET, 8: FC}).move_to([RX, 0.15, 0])
        t_j = eq(r"-\hat{\mathbf y}", "(", "v_x", ZD + "-", "v_z", "B", ")", "=", "+", "B", "v_z", r"\hat{\mathbf y}", size=36,
                 colors={2: VIOLET, 4: VIOLET, 5: MAG, 9: MAG, 10: VIOLET}).move_to([RX, -0.6, 0])
        t_k = eq(r"+\hat{\mathbf z}", "(", "v_x", ZD + "-", "v_y", "B", ")", "=", "-", "B", "v_y", r"\hat{\mathbf z}", size=36,
                 colors={2: VIOLET, 4: VIOLET, 5: MAG, 9: MAG, 10: VIOLET}).move_to([RX, -1.35, 0])
        self.play(FadeOut(l1), FadeOut(l2), FadeOut(cap1), FadeOut(nvx), FadeIn(ref1), FadeIn(mat), run_time=1.1)
        self.hold(1.4)
        fxn = eq(r"F_x=0", size=28, colors={0: FC}).move_to([-4.3, -3.05, 0])
        # i: o menor de x̂ não tem força na direção de B
        h = hl([cell[0][0], cell[1][1], cell[1][2], cell[2][1], cell[2][2]])
        self.play(FadeIn(h), run_time=0.6)
        self.play(FadeIn(t_i[:7]), run_time=0.9)
        self.play(FadeIn(t_i[7:]), FadeIn(fxn), run_time=0.7)
        self.hold(1.2)
        # j: o menor de ŷ dá a componente horizontal da força
        h2 = hl([cell[0][1], cell[1][0], cell[1][2], cell[2][0], cell[2][2]])
        self.play(ReplacementTransform(h, h2), run_time=0.7)
        self.play(FadeIn(t_j[:8]), run_time=0.9)
        self.play(FadeIn(t_j[8:]), kf.animate.set_value(1.0), fyg.animate.set_value(1.0), run_time=0.9)
        self.hold(1.2)
        # k: o menor de ẑ dá a componente vertical
        h3 = hl([cell[0][2], cell[1][0], cell[1][1], cell[2][0], cell[2][1]])
        self.play(ReplacementTransform(h2, h3), run_time=0.7)
        self.play(FadeIn(t_k[:8]), run_time=0.9)
        self.play(FadeIn(t_k[8:]), fzg.animate.set_value(1.0), run_time=0.9)
        self.hold(1.2)
        # coletar: os mesmos termos sobrevivem e se somam
        col = eq(r"\mathbf v\times\mathbf B", "=", "B", "v_z", r"\hat{\mathbf y}", "-", "B", "v_y", r"\hat{\mathbf z}", size=36,
                 colors={0: VIOLET, 2: MAG, 3: VIOLET, 6: MAG, 7: VIOLET}).move_to([RX, -2.2, 0])
        self.play(FadeOut(h3), FadeIn(col, shift=0.1 * UP), run_time=1.0)
        self.hold(1.2)
        res = eq(r"\mathbf v\times\mathbf B", "=", r"(0,\;Bv_z,\;-Bv_y)", size=36, colors={0: VIOLET}).move_to([RX, -3.0, 0])
        self.play(FadeIn(res, shift=0.1 * UP), run_time=1.0)
        self.hold(1.6)

        # ── 3 · Newton + Lorentz: o v×B calculado entra na equação de movimento ──
        cap3 = txt("Newton + Lorentz", T_NOTE, opacity=0.95).move_to([RX, 3.0, 0])
        newton = eq("m", r"\frac{d\mathbf v}{dt}", "=", "q", r"\mathbf v", r"\times", r"\mathbf B", size=44,
                    colors={1: VIOLET, 3: BLUE_L, 4: VIOLET, 6: MAG}).move_to([RX, 1.5, 0])
        newton2 = eq("m", r"\frac{d\mathbf v}{dt}", "=", "q", r"(0,\;Bv_z,\;-Bv_y)", size=44,
                     colors={1: VIOLET, 3: BLUE_L}).move_to([RX, 1.5, 0])
        self.play(FadeOut(mat), FadeOut(ref1), FadeOut(t_i), FadeOut(t_j), FadeOut(t_k), FadeOut(col), FadeOut(fxn),
                  res.animate.move_to([RX, -0.2, 0]), kc.animate.set_value(0.4), run_time=0.9)
        self.play(FadeIn(cap3), FadeIn(newton, shift=0.1 * DOWN), run_time=0.8)
        self.hold(1.4)
        self.play(ReplacementTransform(newton[:4], newton2[:4]), FadeOut(newton[4:]), TransformFromCopy(res[2], newton2[4]),
                  FadeOut(res), run_time=1.4)
        self.hold(1.8)

        # ── 4 · uma equação por componente; a componente correspondente se acende no desenho ──
        self.play(FadeOut(cap3), newton2.animate.scale(0.7).move_to([RX, 3.05, 0]), run_time=1.0)
        cx_ = eq(r"\frac{dv_x}{dt}", "=", "0", size=40, colors={0: VIOLET}).move_to([RX - 0.6, 1.85, 0])
        cy_ = eq(r"\frac{dv_y}{dt}", "=", QB, "v_z", size=40, colors={0: VIOLET, 3: VIOLET}).move_to([RX, 0.35, 0])
        cz_ = eq(r"\frac{dv_z}{dt}", "=", "-" + QB, "v_y", size=40, colors={0: VIOLET, 3: VIOLET}).move_to([RX, -1.35, 0])
        bcx, bcy, bcz = bx(cx_, BOXB), bx(cy_, BOXB), bx(cz_, BOXB)
        nx = eq(r"\Rightarrow\ v_x\ \text{constante}", size=28, colors={}).move_to([RX, 1.0, 0])
        fxn2 = eq(r"F_x=0", size=28, colors={0: FC}).move_to([-4.3, -3.05, 0])
        self.play(FadeIn(cx_, shift=0.1 * UP), FadeIn(bcx), FadeIn(fxn2), fyg.animate.set_value(0.25), fzg.animate.set_value(0.25), run_time=0.9)
        self.play(FadeIn(nx), run_time=0.7)
        self.hold(1.6)
        self.play(FadeIn(cy_, shift=0.1 * UP), FadeIn(bcy), fyg.animate.set_value(1.0), vzg.animate.set_value(1.0),
                  vyg.animate.set_value(0.3), kc.animate.set_value(1.0), run_time=1.1)
        self.hold(1.8)
        self.play(FadeIn(cz_, shift=0.1 * UP), FadeIn(bcz), fyg.animate.set_value(0.25), fzg.animate.set_value(1.0), vyg.animate.set_value(1.0),
                  vzg.animate.set_value(0.3), run_time=1.1)
        self.hold(1.8)
        self.play(fyg.animate.set_value(1.0), vzg.animate.set_value(1.0), run_time=0.6)
        self.hold(1.0)

        # ── 5 · DEDUÇÃO CENTRAL: a álgebra ocupa o lado direito; a órbita continua girando à esquerda ──
        self.run["tt"] = True
        gy, gz, gx = VGroup(cy_, bcy), VGroup(cz_, bcz), VGroup(cx_, bcx)
        self.play(FadeOut(newton2), FadeOut(gx), FadeOut(nx), FadeOut(fxn2), kf.animate.set_value(0.0), kc.animate.set_value(0.0),
                  gy.animate.scale(0.72).move_to([RX - 1.7, 3.0, 0]), gz.animate.scale(0.72).move_to([RX + 1.8, 3.0, 0]),
                  self.bop.animate.set_value(0.25), run_time=1.4, rate_func=smooth)
        capa = VGroup(txt("derivando a equação de", T_BODY, opacity=0.95), eq(r"v_y", size=40, colors={0: VIOLET}),
                      txt("em t", T_BODY, opacity=0.95)).arrange(RIGHT, buff=0.2).move_to([RX, 2.0, 0])
        e1 = eq(r"\frac{d^2v_y}{dt^2}", "=", QB, r"\frac{dv_z}{dt}", size=50, colors={0: VIOLET, 3: VIOLET}).move_to([RX, 0.7, 0])
        self.play(FadeIn(capa), FadeIn(e1, shift=0.1 * UP), run_time=1.0)
        self.hold(2.4)
        capb = VGroup(txt("trocando", T_BODY, opacity=0.95), eq(r"\frac{dv_z}{dt}", size=40, colors={0: VIOLET}),
                      txt("pela 3ª equação", T_BODY, opacity=0.95)).arrange(RIGHT, buff=0.2).move_to([RX, 2.0, 0])
        e2 = eq(r"\frac{d^2v_y}{dt^2}", "=", QB, rf"\left(-{QB}\,v_y\right)", size=46, colors={0: VIOLET}).move_to([RX, 0.7, 0])
        self.play(RT(capa, capb), RT(e1, e2), run_time=1.3)
        self.hold(2.4)
        e3 = eq(r"\frac{d^2v_y}{dt^2}", "=", rf"-\left({QB}\right)^2", "v_y", size=50, colors={0: VIOLET, 3: VIOLET}).move_to([RX, 0.7, 0])
        self.play(RT(e2, e3), FadeOut(capb), run_time=1.3)
        self.hold(2.0)
        e4 = eq(r"\frac{d^2v_y}{dt^2}", "+", rf"\left({QB}\right)^2", "v_y", "=", "0", size=46,
                colors={0: VIOLET, 2: VIOLET, 3: VIOLET}).move_to([RX, 0.7, 0])
        b4 = bx(e4)
        self.play(RT(e3, e4), FadeOut(gy), FadeOut(gz), run_time=1.3)
        nm_edo = nome(["Equação do oscilador harmônico para ", ("m", r"v_y")], pos=(RX, 1.7, 0))
        self.play(FadeIn(b4), FadeIn(nm_edo), run_time=0.6)
        self.hold(2.0)
        g4 = VGroup(e4, b4)
        gen = eq(r"\frac{d^2f}{dt^2}", "+", r"\omega^2", "f", "=", "0", size=46, colors={2: VIOLET}).move_to([RX, -0.55, 0])
        cap_same = txt("mesma estrutura de", T_BODY, opacity=0.9).move_to([RX, 0.45, 0])
        self.play(g4.animate.scale(0.85).move_to([RX, 2.4, 0]), FadeOut(nm_edo), run_time=0.9)
        self.play(FadeIn(cap_same), FadeIn(gen, shift=0.1 * UP), run_time=0.9)
        self.hold(2.0)
        idA = eq(r"\omega^2", "=", rf"\left({QB}\right)^2", size=46, colors={0: VIOLET}).move_to([RX, -1.85, 0])
        self.play(FadeIn(idA, shift=0.1 * UP), run_time=0.9)
        self.hold(2.0)
        idB = eq(r"\omega", "=", rf"\left|{QB}\right|", size=46, colors={0: VIOLET}).move_to([RX, -1.85, 0])
        self.play(RT(idA, idB), run_time=0.9)
        self.hold(1.4)
        self.play(*[FadeOut(m) for m in (g4, gen, cap_same, idB)], run_time=0.8)
        idC = eq(r"\omega_c", "=", rf"\frac{{|{tc(BLUE_L, 'q')}|{tc(MAG, 'B')}}}{{m}}", size=64, colors={0: VIOLET}).move_to([RX, 1.0, 0])
        self.play(FadeIn(idC, shift=0.1 * UP), run_time=0.8)
        bid = bx(idC, 0.3)
        born = nome("Frequência angular ciclotrônica", pos=(RX, 2.25, 0))
        self.play(FadeIn(bid), FadeIn(born), run_time=0.8)
        self.hold(2.0)
        sgn_a = eq(r"|q|", r"\Rightarrow\ \text{frequ\^encia}", size=34, colors={0: BLUE_L}).move_to([RX, -1.7, 0])
        sgn_b = eq(r"\text{sinal de}\ q", r"\Rightarrow\ \text{sentido de rota\c{c}\~ao}", size=34, colors={0: BLUE_L}).move_to([RX, -2.4, 0])
        self.play(FadeIn(sgn_a, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(sgn_b, shift=0.1 * UP), run_time=0.8)
        self.play(FadeOut(idC), FadeOut(bid), FadeOut(born), FadeOut(sgn_a), FadeOut(sgn_b), run_time=0.8)

        # ── 5b · que função resolve? (verificação por derivação) → solução geral → condições iniciais → C1, C2 ──
        ed = eq(r"\frac{d^2v_y}{dt^2}", "+", r"\omega_c^2", "v_y", "=", "0", size=46, colors={0: VIOLET, 2: VIOLET, 3: VIOLET}).move_to([RX, 2.5, 0])
        ask = txt("derivar 2× troca o sinal: qual função?", 22, opacity=0.9).move_to([RX, 1.65, 0])
        self.play(FadeIn(ed, shift=0.1 * DOWN), FadeIn(ask), run_time=1.0)
        tS = eq(r"\frac{d^2}{dt^2}\sin(\omega_c t)", "=", r"-\omega_c^2", r"\sin(\omega_c t)", size=38, colors={2: VIOLET}).move_to([RX, 0.6, 0])
        tC = eq(r"\frac{d^2}{dt^2}\cos(\omega_c t)", "=", r"-\omega_c^2", r"\cos(\omega_c t)", size=38, colors={2: VIOLET}).move_to([RX, -0.5, 0])
        self.play(FadeIn(tS, shift=0.1 * UP), run_time=1.0)
        self.hold(1.6)
        self.play(FadeIn(tC, shift=0.1 * UP), run_time=1.0)
        self.hold(1.4)
        sol = eq(r"v_y(t)", "=", "C_1", r"\cos(\omega_c t)", "+", "C_2", r"\sin(\omega_c t)", size=40, colors={0: VIOLET}).move_to([RX, -1.7, 0])
        bsol = bx(sol)
        self.play(FadeOut(ask), FadeIn(sol, shift=0.1 * UP), FadeIn(bsol), run_time=1.5)
        self.hold(2.0)
        finish_turn()
        self.run["tt"] = True
        self.play(*[FadeOut(m) for m in (tS, tC, ed)], VGroup(sol, bsol).animate.move_to([RX, 2.4, 0]), run_time=0.9)
        # condições iniciais: a carga está na origem, com v para cima (v_y = 0, v_z = v⊥)
        o1.t0 = self.tt.get_value()
        ic = eq(r"q>0:\ \ v_y(0)=0,\ \ v_z(0)=v_\perp", size=34, colors={}).move_to([RX, 1.5, 0])
        self.play(FadeIn(ic), run_time=0.7)
        s1 = eq(r"v_y(0)", "=", "C_1", "=", "0", size=40, colors={0: VIOLET}).move_to([RX, 0.4, 0])
        self.play(FadeIn(s1, shift=0.1 * UP), run_time=0.9)
        self.hold(1.2)
        sol2 = eq(r"v_y(t)", "=", "C_2", r"\sin(\omega_c t)", size=40, colors={0: VIOLET}).move_to([RX, 2.4, 0])
        self.play(RT(sol, sol2), FadeOut(bsol), run_time=1.1)
        self.hold(0.8)
        # C2 vem da equação acoplada em t = 0
        s2 = eq(r"\frac{dv_y}{dt}", "=", r"\omega_c", "v_z", size=40, colors={0: VIOLET, 3: VIOLET}).move_to([RX, -0.55, 0])
        self.play(FadeOut(s1), FadeIn(s2, shift=0.1 * UP), run_time=0.9)
        self.hold(1.2)
        s3 = eq(r"\omega_c", "C_2", "=", r"\omega_c", r"v_\perp", size=40, colors={0: VIOLET, 3: VIOLET, 4: VIOLET}).move_to([RX, -1.6, 0])
        t0n = txt("em t = 0", 22, opacity=0.9).move_to([RX, -2.25, 0])
        self.play(FadeIn(s3, shift=0.1 * UP), FadeIn(t0n), run_time=1.0)
        self.hold(1.4)
        s4 = eq("C_2", "=", r"v_\perp", size=44, colors={2: VIOLET}).move_to([RX, -1.6, 0])
        self.play(RT(s3, s4), FadeOut(t0n), run_time=1.0)
        self.hold(1.0)
        vy_f = eq(r"v_y(t)", "=", r"v_\perp", r"\sin(\omega_c t)", size=44, colors={0: VIOLET, 2: VIOLET}).move_to([RX, 2.4, 0])
        self.play(RT(sol2, vy_f), FadeOut(s4), FadeOut(ic), run_time=1.1)
        self.hold(1.0)
        # v_z nasce da MESMA equação acoplada: v_z = (1/ω_c) dv_y/dt
        z1 = eq(r"v_z", "=", r"\frac{1}{\omega_c}", r"\frac{dv_y}{dt}", size=44, colors={0: VIOLET, 3: VIOLET}).move_to([RX, 0.9, 0])
        self.play(FadeIn(z1, shift=0.1 * UP), FadeOut(s2), run_time=1.0)
        self.hold(1.4)
        z2 = eq(r"v_z", "=", r"\frac{1}{\omega_c}", r"\frac{d}{dt}\left[v_\perp\sin(\omega_c t)\right]", size=40, colors={0: VIOLET}).move_to([RX, 0.9, 0])
        self.play(RT(z1, z2), run_time=1.1)
        self.hold(1.2)
        z3 = eq(r"v_z", "=", r"\frac{1}{\omega_c}", r"\omega_c", r"v_\perp\cos(\omega_c t)", size=44, colors={0: VIOLET}).move_to([RX, -0.3, 0])
        self.play(FadeIn(z3, shift=0.1 * UP), run_time=1.0)
        self.hold(1.0)
        vz_f = eq(r"v_z(t)", "=", r"v_\perp", r"\cos(\omega_c t)", size=44, colors={0: VIOLET, 2: VIOLET}).move_to([RX, -1.6, 0])
        self.play(RT(z3, vz_f), FadeOut(z2), run_time=1.1)
        self.hold(1.4)
        finish_turn()
        self.run["tt"] = True

        # ── 6 · soluções: trajetória REAL (esquerda-alto) · ESPAÇO DAS VELOCIDADES (esquerda-baixo) · gráficos (direita) ──
        o1.t0 = self.tt.get_value()
        VC, RV = np.array([-3.4, -1.25, 0.0]), 1.25
        self.play(self.ox.animate.set_value(-6.2), self.oy.animate.set_value(2.2), self.gs.animate.set_value(0.5),
                  self.bop.animate.set_value(0.0), FadeOut(vy_f), FadeOut(vz_f), FadeOut(tri), run_time=1.4, rate_func=smooth)

        def mk_ax(cy):
            return Axes(x_range=[0, TP, TP / 4], y_range=[-1.3, 1.3, 1.3], x_length=4.0, y_length=1.2, tips=False,
                        axis_config={"color": WHITE, "stroke_width": 2, "include_ticks": False}).move_to([RX + 0.2, cy, 0])

        axy, axz = mk_ax(1.75), mk_ax(-0.35)
        fy, fz = (lambda t: qsK.get_value() * math.sin(OMEGA * t)), (lambda t: math.cos(OMEGA * t))
        form_y = eq(r"v_y(t)", "=", r"v_\perp\sin(\omega_c t)", size=34, colors={0: VIOLET, 2: VIOLET}).move_to([RX, 2.95, 0])
        form_z = eq(r"v_z(t)", "=", r"v_\perp\cos(\omega_c t)", size=34, colors={0: VIOLET, 2: VIOLET}).move_to([RX, 0.85, 0])
        ylab_y = eq("v_y", size=26, colors={0: VIOLET}).next_to(axy.y_axis.get_end(), UP, buff=0.05)
        ylab_z = eq("v_z", size=26, colors={0: VIOLET}).next_to(axz.y_axis.get_end(), UP, buff=0.05)
        tl = eq("t", size=26, colors={0: VIOLET}).next_to(axz.x_axis.get_end(), DOWN, buff=0.1)
        tT = eq("T", size=24, colors={0: VIOLET}).move_to(axz.c2p(TP, 0) + np.array([0.0, -0.28, 0.0]))
        ticks = VGroup(*[eq(s, size=22).next_to(a.c2p(0, v), LEFT, buff=0.1) for a in (axy, axz)
                         for s, v in ((r"v_\perp", 1), (r"-v_\perp", -1))])
        ini = eq(r"q>0:\ \ v_y(0)=0,\ \ v_z(0)=v_\perp", size=32, colors={}).move_to([RX, -1.75, 0])
        vtag = VGroup(txt("espaço das velocidades", 20, opacity=0.95), eq(r"(v_y,\,v_z)", size=24, colors={0: VIOLET})).arrange(RIGHT, buff=0.15).move_to([VC[0], 0.55, 0])
        rtag = VGroup(txt("trajetória real", 20, opacity=0.95), eq(r"(y,\,z)", size=24)).arrange(DOWN, buff=0.1).move_to([-2.9, 2.2, 0])
        vpan = panel(VGroup(vtag, Circle(radius=RV).move_to(VC)).move_to(VC + np.array([0, 0.2, 0])), pad=0.25, op=0.35)
        rpan = panel(Rectangle(width=5.0, height=2.15).move_to([-4.15, 2.2, 0]), pad=0.1, op=0.35)
        vcirc = VGroup(Circle(radius=RV, color=WHITE, stroke_width=2).set_stroke(opacity=0.55).move_to(VC),
                       Line(VC + np.array([-RV - 0.25, 0, 0]), VC + np.array([RV + 0.25, 0, 0]), color=WHITE, stroke_width=1.5).set_stroke(opacity=0.55),
                       Line(VC + np.array([0, -RV - 0.25, 0]), VC + np.array([0, RV + 0.25, 0]), color=WHITE, stroke_width=1.5).set_stroke(opacity=0.55),
                       eq("v_y", size=28, colors={0: VIOLET}).move_to(VC + np.array([RV + 0.5, 0.0, 0])),
                       eq("v_z", size=28, colors={0: VIOLET}).move_to(VC + np.array([0.0, RV + 0.42, 0])), vtag, rtag)

        def curve(ax, f):
            def g():
                u = min(max(u_now(), 0.0), TP)
                if u < 0.02:
                    return VGroup()
                pts = [ax.c2p(t, f(t)) for t in np.linspace(0.0, u, int(60 * u / TP) + 3)]
                m = VMobject(color=VIOLET, stroke_width=4)
                m.set_points_as_corners(pts)
                return m
            return G(g)

        def cursor(ax, f):
            def g():
                u = max(u_now(), 0.0) % TP
                p, b = ax.c2p(u, f(u)), ax.c2p(u, 0)
                d = Dot(p, radius=0.08, color=VIOLET).set_stroke(WHITE, 2)
                if float(np.linalg.norm(p - b)) < 0.04:
                    return VGroup(d)
                return VGroup(DashedLine(b, p, dash_length=0.07, color=WHITE, stroke_width=1.5).set_opacity(0.7), d)
            return G(g)

        def vvec():
            ph = OMEGA * max(u_now(), 0.0)
            tip = VC + RV * np.array([qsK.get_value() * math.sin(ph), math.cos(ph), 0.0])
            g = VGroup(vec(VC, tip, VIOLET, 5, 5))               # a ponta termina EXATAMENTE no ponto da circunferência
            for a, b in ((tip, np.array([tip[0], VC[1], 0.0])), (tip, np.array([VC[0], tip[1], 0.0]))):
                if float(np.linalg.norm(a - b)) > 0.05:
                    g.add(DashedLine(a, b, dash_length=0.07, color=WHITE, stroke_width=1.5).set_opacity(0.6))
            g.add(Dot(tip, radius=0.07, color=WHITE).set_z_index(6), Dot(np.array([tip[0], VC[1], 0.0]), radius=0.05, color=VIOLET),
                  Dot(np.array([VC[0], tip[1], 0.0]), radius=0.05, color=VIOLET))
            return g

        def vlab_f():
            ph = OMEGA * max(u_now(), 0.0)
            s_ = qsK.get_value()
            return eqc(r"\mathbf v_\perp", size=30, colors={0: VIOLET}).move_to(
                VC + 0.55 * RV * np.array([s_ * math.sin(ph), math.cos(ph), 0.0]) + 0.42 * np.array([math.cos(ph), -s_ * math.sin(ph), 0.0]))

        cy_m, cz_m, kc_y, kc_z = curve(axy, fy), curve(axz, fz), cursor(axy, fy), cursor(axz, fz)
        gvec, vlab = G(vvec), G(vlab_f)
        self.trK = self.mk_trail(o1, 3.0, optr=ktr)
        self.add(cy_m, cz_m, kc_y, kc_z, gvec, vlab, self.trK)
        statics = VGroup(axy, axz, ylab_y, ylab_z, tl, tT, ticks, vcirc, vpan, rpan)
        self.play(FadeIn(statics), FadeIn(form_y, shift=0.1 * UP), FadeIn(form_z, shift=0.1 * UP), FadeIn(ini), run_time=1.4)
        cap6 = VGroup(VGroup(txt("a ponta de", 22, opacity=0.95), eq(r"\mathbf v_\perp", size=28, colors={0: VIOLET})).arrange(RIGHT, buff=0.14),
                      txt("percorre um círculo", 22, opacity=0.95)).arrange(DOWN, buff=0.08).move_to([-3.4, -3.3, 0])
        self.play(FadeIn(cap6), run_time=0.5)
        self.run["tt"] = True
        self.hold(TP)                                      # uma volta: gráficos e vetor nascem juntos
        self.run["tt"] = False
        cap6b = VGroup(txt("componentes senoidais,", 22, opacity=0.95), txt("defasadas de 90°", 22, opacity=0.95)).arrange(DOWN, buff=0.08).move_to([-3.4, -3.3, 0])
        self.play(RT(cap6, cap6b), run_time=0.5)
        self.hold(2.4)

        # ── 7 · o módulo de v⊥ não muda ──
        mag1 = eq(r"v_y^2+v_z^2=v_\perp^2\left(\sin^2\omega_c t+\cos^2\omega_c t\right)", size=26, colors={}).move_to([RX, -2.55, 0])
        mag2 = eq(r"v_y^2+v_z^2", "=", r"v_\perp^2", size=40, colors={0: VIOLET, 2: VIOLET}).move_to([RX, -3.25, 0])
        self.run["tt"] = True
        self.play(FadeOut(ini), FadeIn(mag1, shift=0.1 * UP), run_time=1.0)
        self.hold(1.6)
        self.play(FadeIn(mag2, shift=0.1 * UP), run_time=0.8)
        self.hold(TP - 3.4)
        self.run["tt"] = False
        msg7 = VGroup(VGroup(txt("a força magnética faz", 22, opacity=0.95), eq(r"\mathbf v_\perp", size=28, colors={0: VIOLET}),
                             txt("girar;", 22, opacity=0.95)).arrange(RIGHT, buff=0.12),
                      txt("seu módulo permanece constante", 22, opacity=0.95)).arrange(DOWN, buff=0.08).move_to([-3.4, -3.3, 0])
        self.play(RT(cap6b, msg7), run_time=0.7)
        self.hold(2.6)
        # q < 0 é OUTRO caso físico (mesmos |q|, m, B e mesmas condições iniciais): troca discreta de todo o conjunto
        # (carga, trajetória, v, F, hodógrafo, gráfico e fórmula). Nada interpola o sinal e a rapidez fica constante.
        self.play(FadeOut(mag1), FadeOut(mag2), FadeOut(msg7), run_time=0.7)
        o1n = Orbit(VP1, 0.0, -1, self.tt, 0.0, VIOLET)
        pos_set = (self.q3, self.vp3, self.fm3[1], self.trK)
        neg_set = (self.mk_charge(o1n), self.mk_vec(o1n, "v", WHITE, 6, 5), self.mk_vec(o1n, "F", FC, 6, 4), self.mk_trail(o1n, 3.0, optr=ktr))

        def troca(para_neg):
            o1.t0 = o1n.t0 = self.tt.get_value()          # outro caso: relógio e condição inicial reiniciados
            qsK.set_value(-1.0 if para_neg else 1.0)
            self.remove(*(pos_set if para_neg else neg_set))
            self.add(*(neg_set if para_neg else pos_set))
            self.ox.set_value(-4.9 if para_neg else -6.2)   # o centro da órbita fica no mesmo lugar (o círculo é espelhado)

        row_p = VGroup(eq(r"q>0:", size=34, colors={0: BLUE_L}), txt("gira no sentido horário", 22, opacity=0.95)).arrange(RIGHT, buff=0.25).move_to([RX, -2.15, 0])
        row_n = VGroup(eq(r"q<0:", size=34, colors={0: BLUE_L}), txt("gira no sentido anti-horário", 22, opacity=0.95)).arrange(RIGHT, buff=0.25).move_to([RX, -2.15, 0])
        form_yn = eq(r"v_y(t)", "=", r"-v_\perp\sin(\omega_c t)", size=34, colors={0: VIOLET, 2: VIOLET}).move_to([RX, 2.95, 0])
        sg_w = eq(r"\omega_c=\frac{|q|B}{m}", r"\ \text{(mesmo m\'odulo)}", size=30, colors={0: VIOLET}).move_to([RX, -3.2, 0])
        self.run["tt"] = True
        self.play(FadeIn(row_p), run_time=0.8)
        self.hold(TP - 0.8)                                # uma volta completa do caso q > 0
        troca(True)
        self.play(Flash(self.O(), color=VIOLET, flash_radius=0.4, line_length=0.1), RT(form_y, form_yn),
                  RT(row_p, row_n), FadeIn(sg_w), run_time=1.0)
        self.hold(TP - 1.0)                                # uma volta completa do caso q < 0
        form_y = eq(r"v_y(t)", "=", r"v_\perp\sin(\omega_c t)", size=34, colors={0: VIOLET, 2: VIOLET}).move_to([RX, 2.95, 0])
        troca(False)
        self.play(Flash(self.O(), color=BLUE_L, flash_radius=0.4, line_length=0.1), RT(form_yn, form_y),
                  FadeOut(row_n), FadeOut(sg_w), run_time=1.0)
        self.run["tt"] = False
        finish_turn()

        # ── 8 · da velocidade à posição: integração com limites; o desenho volta ao tamanho do B02 e traça a trajetória ──
        self.play(kop.animate.set_value(0.0), FadeOut(statics), FadeOut(form_y), FadeOut(form_z), run_time=1.0)
        self.remove(cy_m, cz_m, kc_y, kc_z, gvec, vlab)
        o1.t0 = self.tt.get_value()                         # volta inteira: a carga está na origem; o traço recomeça
        self.play(self.ox.animate.set_value(-5.3), self.oy.animate.set_value(0.0), self.gs.animate.set_value(0.85),
                  self.bop.animate.set_value(0.3), FadeIn(tri), run_time=1.6, rate_func=smooth)
        self.run["tt"] = True
        cap8 = eq(r"v_y=\frac{dy}{dt},\quad v_z=\frac{dz}{dt}", size=28, colors={}).move_to([RX, 3.15, 0])
        XEQ = 2.5                                           # todas as igualdades da integração ficam alinhadas neste x

        def al(m, idx, y):
            m.move_to([RX, y, 0])
            m.shift(RIGHT * (XEQ - m[idx].get_center()[0]))
            return m

        a1 = al(eq(r"\frac{dy}{dt}", "=", r"v_\perp", r"\sin(\omega_c t)", r"\,", size=42, colors={2: VIOLET}), 1, 2.2)
        self.play(FadeIn(cap8), FadeIn(a1, shift=0.1 * UP), run_time=0.9)
        self.hold(1.2)
        a2 = al(eq("dy", "=", r"v_\perp", r"\sin(\omega_c t)", r"\,dt", size=42, colors={2: VIOLET}), 1, 2.2)
        self.play(RT(a1, a2), run_time=1.0)
        self.hold(0.8)
        a3 = al(eq(r"\int_{y_0}^{y(t)}", "dy", "=", r"\int_0^{t}", r"v_\perp", r"\sin(\omega_c t')", r"\,dt'", size=40, colors={4: VIOLET}), 2, 1.1)
        lim = txt("de t' = 0 até t", 22, opacity=0.85).move_to([RX, 0.2, 0])
        self.play(FadeIn(a3, shift=0.1 * UP), FadeIn(lim), run_time=1.2)
        self.hold(1.2)
        prim = al(eq(r"\int\sin(\omega_c t')\,dt'", "=", r"-\frac{\cos(\omega_c t')}{\omega_c}+C", size=34, colors={}), 1, -0.3)
        self.play(FadeOut(lim), FadeIn(prim, shift=0.1 * UP), run_time=1.0)
        self.hold(1.4)
        a4 = al(eq("y(t)-y_0", "=", r"v_\perp", r"\left[-\frac{\cos(\omega_c t')}{\omega_c}\right]_0^{t}", size=38, colors={2: VIOLET}), 1, -1.5)
        self.play(FadeIn(a4, shift=0.1 * UP), run_time=1.1)
        cnote = txt("C se cancela nos limites", 20, opacity=0.8).move_to([RX, -2.2, 0])
        self.play(FadeIn(cnote), run_time=0.5)
        self.hold(1.2)
        a5 = al(eq("y(t)-y_0", "=", r"\frac{v_\perp}{\omega_c}", r"\left[1-\cos(\omega_c t)\right]", size=38, colors={2: VIOLET}), 1, -1.5)
        self.play(RT(a4, a5), FadeOut(prim), FadeOut(cnote), run_time=1.2)
        self.hold(1.0)
        self.play(*[FadeOut(m) for m in (a2, a3)], a5.animate.shift(UP * 3.7), run_time=0.9)
        # z: mesmo caminho, a primitiva de cos é sen
        b1 = al(eq(r"\int_{z_0}^{z(t)}", "dz", "=", r"\int_0^{t}", r"v_\perp", r"\cos(\omega_c t')", r"\,dt'", size=40, colors={4: VIOLET}), 2, 0.9)
        self.play(FadeIn(b1, shift=0.1 * UP), run_time=1.0)
        self.hold(1.0)
        b2 = al(eq("z(t)-z_0", "=", r"v_\perp", r"\left[\frac{\sin(\omega_c t')}{\omega_c}\right]_0^{t}", size=38, colors={2: VIOLET}), 1, -0.4)
        self.play(FadeIn(b2, shift=0.1 * UP), run_time=1.0)
        self.hold(1.0)
        b3 = al(eq("z(t)-z_0", "=", r"\frac{v_\perp}{\omega_c}", r"\sin(\omega_c t)", size=38, colors={2: VIOLET}), 1, 0.9)
        self.play(RT(b2, b3), FadeOut(b1), run_time=1.2)
        self.hold(1.0)
        self.play(b3.animate.shift(UP * 0.1), run_time=0.5)
        R1, R2 = a5, b3

        # ── 9 · por que é uma circunferência: elimina t somando os quadrados; o desenho revela o círculo ──
        nameR = VGroup(txt("defina", 22, opacity=0.95), eq(r"R\equiv\frac{v_\perp}{\omega_c}", size=34, colors={0: WHITE})).arrange(RIGHT, buff=0.2).move_to([RX, 3.15, 0])
        c2a = eq("y-y_0", "=", "R", r"\left[1-\cos(\omega_c t)\right]", size=40).move_to([RX, 2.15, 0])
        c2b = eq("z-z_0", "=", "R", r"\sin(\omega_c t)", size=40).move_to([RX, 1.0, 0])
        self.play(RT(R1, c2a), RT(R2, c2b), FadeOut(cap8), FadeIn(nameR), run_time=1.5)
        self.hold(2.0)
        c2a2 = eq("y-y_0-R", "=", "-R", r"\cos(\omega_c t)", size=40).move_to([RX, 2.15, 0])
        self.play(RT(c2a, c2a2), run_time=1.2)
        self.hold(1.4)
        sq1 = eq(r"(y-y_0-R)^2", "=", r"R^2", r"\cos^2(\omega_c t)", size=38).move_to([RX, 2.15, 0])
        sq2 = eq(r"(z-z_0)^2", "=", r"R^2", r"\sin^2(\omega_c t)", size=38).move_to([RX, 1.0, 0])
        self.play(RT(c2a2, sq1), RT(c2b, sq2), run_time=1.3)
        self.hold(1.6)
        sm = eq(r"(y-y_0-R)^2+(z-z_0)^2", "=", r"R^2", r"\left[\cos^2+\sin^2\right]", size=36).move_to([RX, -0.35, 0])
        self.play(FadeIn(sm, shift=0.1 * UP), run_time=1.1)
        self.hold(1.6)
        sm2 = eq(r"(y-y_0-R)^2+(z-z_0)^2", "=", r"R^2", size=40).move_to([RX, -0.35, 0])
        self.play(RT(sm, sm2), run_time=1.2)
        bsm = bx(sm2)
        self.play(FadeIn(bsm), run_time=0.5)
        # só agora: o desenho revela a circunferência, com centro e raio que saem da álgebra
        cline, clab = self.mk_center(o1, "R")
        ctag = eq(r"C=(y_0+R,\;z_0)", size=34).move_to([RX, -1.5, 0])
        circ_msg = txt("circunferência", T_BODY, opacity=0.95).move_to([RX, -2.3, 0])
        self.add(cline, clab)
        self.play(FadeIn(cline), FadeIn(clab), FadeIn(ctag), FadeIn(circ_msg), run_time=1.0)
        self.hold(2.4)
        Rfin = eq("R", "=", r"\frac{v_\perp}{\omega_c}", "=", rf"\frac{{m\,v_\perp}}{{|{tc(BLUE_L, 'q')}|{tc(MAG, 'B')}}}", size=44, colors={2: VIOLET}).move_to([RX, 1.2, 0])
        bR = bx(Rfin)
        nm_R = nome("Raio da órbita magnética", pos=(RX, 2.2, 0))
        self.play(*[FadeOut(m) for m in (sq1, sq2, sm2, bsm, ctag, circ_msg, nameR)], run_time=0.8)
        self.play(FadeIn(Rfin, shift=0.1 * UP), run_time=0.9)
        self.play(FadeIn(bR), FadeIn(nm_R), run_time=0.5)
        self.hold(2.4)
        self.run["tt"] = False

        # ── 10 · v_x constante; a hélice vem de uma NOVA condição inicial (v∥ definido antes da evolução; nada o "cria") ──
        hp, vh = ValueTracker(0.0), ValueTracker(0.0)
        R0 = VP1 / OMEGA
        HC, HS = np.array([-3.4, -0.55, 0.0]), 0.7

        def hpt(t_):
            yr, zr, xr = R0 * (1 - math.cos(OMEGA * t_)) - R0, R0 * math.sin(OMEGA * t_), vh.get_value() * (t_ - TP)
            return HC + HS * np.array([xr + 0.5 * yr, zr, 0.0])

        def helix():
            te = hp.get_value() * 2 * TP
            if te < 0.03:
                return VGroup()
            m = VMobject(color=BLUE_L, stroke_width=4)
            m.set_points_as_corners([hpt(t) for t in np.linspace(0.0, te, int(70 * te / TP) + 3)])
            return VGroup(m, charge_c(hpt(te), 1, 0.8))

        gh = G(helix, kop2)
        self.add(gh)
        baxis = VGroup(arrow(np.array([-6.4, -2.5, 0.0]), np.array([-0.6, -2.5, 0.0]), MAG, 3, 2, tip=0.18),
                       eq(r"\mathbf B", size=32, colors={0: MAG}).move_to([-0.8, -2.15, 0]))
        # a representação anterior (carga, vetores e trilha) sai POR INTEIRO: nada fica estacionado no canto
        ghost = VGroup(self.q3.copy(), self.vp3.copy(), self.fm3[1].copy())
        self.remove(self.q3, self.vp3, self.fm3[0], self.fm3[1], self.trK)
        self.add(ghost)
        self.play(*[FadeOut(m) for m in (Rfin, bR, nm_R, cline, clab, tri, ghost)], FadeIn(baxis), self.bop.animate.set_value(0.0),
                  run_time=1.2, rate_func=smooth)
        hx1 = eq(r"\frac{dv_x}{dt}", "=", "0", size=M_L, colors={0: VIOLET}).move_to([RX, 1.9, 0])
        hx2 = eq(r"v_x", "=", r"v_\parallel", size=M_L, colors={0: VIOLET, 2: VIOLET}).move_to([RX, 1.9, 0])
        hx3 = eq(r"x(t)", "=", r"x_0+v_\parallel t", size=42, colors={2: VIOLET}).move_to([RX, 0.5, 0])
        self.play(FadeIn(hx1, shift=0.1 * UP), run_time=0.8)
        self.hold(0.8)
        self.play(RT(hx1, hx2), run_time=1.0)
        self.hold(0.6)
        self.play(FadeIn(hx3, shift=0.1 * UP), run_time=0.8)
        # nova condição inicial: v∥ já no valor final antes de qualquer evolução; a hélice é desenhada uma só vez
        hp.set_value(0.0)
        vh.set_value(VPAR)
        nc = VGroup(txt("nova condição inicial:", T_NOTE, opacity=0.95),
                    eq(r"v_\parallel\neq0\ \ \text{j\'a em}\ t=0", size=34, colors={0: VIOLET})).arrange(DOWN, buff=0.12).move_to([RX, -0.9, 0])
        self.play(FadeIn(nc), run_time=0.7)
        self.play(hp.animate.set_value(1.0), run_time=TP, rate_func=linear)
        self.play(FadeOut(nc), run_time=0.4)
        d1 = VGroup(VGroup(txt("a Lorentz não cria", 24, opacity=0.95), eq(r"v_\parallel", size=36, colors={0: VIOLET}), txt(";", 24)).arrange(RIGHT, buff=0.12),
                    txt("ela preserva essa componente", 24, opacity=0.95)).arrange(DOWN, buff=0.1)
        gdn = VGroup(d1, bx(d1)).move_to([RX, -1.1, 0])
        self.play(FadeIn(gdn, shift=0.1 * UP), run_time=0.8)
        self.hold(2.0)

        # ── fim: devolve o desenho ao estado que o B02 (verificações, período, duas partículas) espera ──
        self.play(kop2.animate.set_value(0.0), *[FadeOut(m) for m in (hx2, hx3, gdn, baxis)], run_time=0.9)
        self.remove(gh, vcomp, fcomp)
        o1.t0 = self.tt.get_value()
        self.add(self.q3, self.vp3, self.fm3[0], self.fm3[1])          # o círculo volta a participar: a carga e seus vetores voltam
        self.play(self.ox.animate.set_value(-4.2), self.oy.animate.set_value(-0.1), self.gs.animate.set_value(1.15),
                  self.bop.animate.set_value(1.0), FadeIn(self.lor), FadeIn(self.lor_box), FadeIn(self.bleg), FadeIn(fm[2]),
                  run_time=1.6, rate_func=smooth)
        self.hold(0.6)

    def b02_circulo(self):
        o1 = self.o1
        o1.t0 = self.tt.get_value()
        self.run["tt"] = True
        self.trail1 = self.mk_trail(o1, 3.5)
        self.ra1 = self.mk_rightangle(o1)
        self.add(self.trail1, self.ra1)
        note = VGroup(eq(r"\mathbf F_B\perp\mathbf v", size=M_M, colors={0: FC}),
                      txt("só muda a direção de v", T_NOTE, opacity=0.9)).arrange(DOWN, buff=0.22).move_to([CX, 0.15, 0])
        self.play(FadeIn(note), run_time=0.8)
        self.hold(T_PER * 0.45)               # primeiro trecho de curvatura (fim do Preview D)
        self.seg("rest0")
        self.hold(T_PER * 0.3)                # só um trecho de órbita: F_B ⊥ v (o círculo e R já vieram do aprofundamento K)
        self.note_perp = note

    def b02_algebra(self):
        """Verificação + período, COM a órbita viva: a partícula continua girando, v tangente e F_B radial acompanham, R liga o
        centro à partícula; a equação fica à direita e cada grandeza dela é localizável no desenho."""
        o1 = self.o1
        RX = 3.9
        self.run["tt"] = True
        self.cline, self.clab = self.mk_center(o1, "R")
        self.add(self.cline, self.clab)
        self.fm3[2].clear_updaters()
        self.remove(self.fm3[2], self.ra1)

        def unit(v):
            return v / (np.linalg.norm(v) + 1e-9)

        def flab():
            F = o1.force() * (0.5 / (ABSQ * BM))
            d = self.W(o1.pos()) - self.W(np.array([o1.C[0], o1.C[1], o1.pos()[2]]))
            nn = unit(np.array([-d[1], d[0], 0.0]))
            return halo(eqc(r"\mathbf F_B", size=M_M, colors={0: FC}).move_to(self.W(o1.pos() + 0.5 * F) - 0.5 * nn))

        def vlab():
            v = o1.vel() * np.array([1.0, 1.0, 0.0])
            u = unit(self.Wv(v))
            return halo(eqc(r"\mathbf v_\perp", size=M_M, colors={0: VIOLET}).move_to(self.W(o1.pos() + v) + 0.5 * u))

        self.fl, self.vl = always_redraw(flab), always_redraw(vlab)
        self.add(self.fl, self.vl)
        AT, SZ = [RX, 0.3, 0], 52
        cap = txt("a força magnética é a força centrípeta", T_NOTE, opacity=0.95).move_to([RX + 0.5, 3.2, 0])
        self.play(FadeOut(self.note_perp), FadeOut(self.bleg), FadeOut(self.lor), FadeOut(self.lor_box), run_time=0.7)
        self.play(FadeIn(cap), self.bop.animate.set_value(0.3), FadeIn(self.fl), FadeIn(self.vl), run_time=0.9, rate_func=smooth)
        # ── raio por um segundo caminho ──
        self.morph(["q", "vp@L", "B", "=", ("f", ["m", "vp2"], ["R"], "b1")], SZ, AT, first=True)
        self.hold(1.4)
        self.morph(["q", "vp@L", "B", "=", ("f", ["m", "vp@a", "vp@b"], ["R"], "b1")], SZ, AT, alias={"vp2": ["vp@a", "vp@b"]}, run=1.0)
        self.hold(0.6)
        lines = self.strike(self.cur["vp@L"], self.cur["vp@a"])
        self.hold(0.6)
        c = self.cur
        self.play(FadeOut(c["vp@L"]), FadeOut(c["vp@a"]), FadeOut(lines), run_time=0.8)
        del c["vp@L"], c["vp@a"]
        self.morph(["q", "B", "=", ("f", ["m", "vp@b"], ["R"], "b1")], SZ, AT, run=1.0)
        self.hold(0.6)
        old_ = list(self.cur.values())
        self.play(*[FadeOut(m) for m in old_], run_time=0.5)
        root_, new_ = self.build(["R@L", "=", ("f", ["m", "vp@b"], ["q@d", "B@d"], "b1")], SZ)
        root_.move_to(AT)
        self.play(FadeIn(root_, shift=0.1 * UP), run_time=0.8)
        self.cur = new_
        bx = box(VGroup(*self.cur.values()))
        same = txt("o mesmo raio, por outro caminho", 22, opacity=0.85).move_to([RX, -1.5, 0])
        self.play(FadeIn(bx), FadeIn(same), run_time=0.8)
        self.hold(2.2)

        # ── período: uma volta completa, com o comprimento 2πR e a rapidez v⊥ ──
        ref = VGroup(*self.build(["R", "=", ("f", ["m", "vp"], ["q", "B"], "b1")], 30)[0]).move_to([RX, 2.2, 0])
        self.play(*[FadeOut(m) for m in self.cur.values()], FadeOut(bx), FadeOut(cap), FadeOut(same), FadeIn(ref), run_time=0.7)
        self.cur = {}
        o1.t0 = self.tt.get_value()                      # a trilha recomeça: a volta se desenha enquanto o cronômetro corre
        BW, BY = 3.6, 3.05
        bar_bg = Rectangle(width=BW, height=0.2, color=WHITE, stroke_width=2).set_stroke(opacity=0.6).move_to([RX, BY, 0])
        bar = always_redraw(lambda: Rectangle(width=max(0.02, BW * min(1.0, max(0.0, (self.tt.get_value() - o1.t0) / T_PER))), height=0.2, stroke_width=0,
                                              fill_color=VIOLET, fill_opacity=0.95).move_to([RX - BW / 2, BY, 0], aligned_edge=LEFT))
        t0l = eq("0", size=24).move_to([RX - BW / 2, BY - 0.32, 0])
        tTl = eq("T", size=28, colors={0: VIOLET}).move_to([RX + BW / 2, BY - 0.32, 0])
        tcl = eq("t", size=28, colors={0: VIOLET}).move_to([RX - BW / 2 - 0.35, BY, 0])
        len_l = VGroup(eq(r"2\pi R", size=34), txt("uma volta", 20, opacity=0.9)).arrange(RIGHT, buff=0.18).move_to([RX, -3.2, 0])
        self.play(FadeIn(bar_bg), FadeIn(bar), FadeIn(t0l), FadeIn(tTl), FadeIn(tcl), FadeIn(len_l), run_time=0.8)
        self.morph(["T", "=", ("f", ["2pi", "R"], ["vp@d"], "b1")], SZ, AT, first=True)
        self.hold(T_PER - 2.0)                           # a volta termina com o cronômetro em T
        self.morph(["T", "=", ("f", ["2pi", ("f", ["m", "vp@n"], ["q", "B"], "b2")], ["vp@d"], "b1")], SZ, AT,
                   alias={"R": ["m", "vp@n", "q", "B", "b2"]}, run=1.4)
        self.hold(1.0)
        lines = self.strike(self.cur["vp@n"], self.cur["vp@d"])
        self.hold(1.0)
        c = self.cur
        self.play(FadeOut(c["vp@n"]), FadeOut(c["vp@d"]), FadeOut(lines), run_time=0.8)
        del c["vp@n"], c["vp@d"]
        self.morph(["T", "=", ("f", ["2pi", "m"], ["q", "B"], "b1")], SZ, AT, run=1.6)
        bx = box(VGroup(*self.cur.values()))
        nm_T = nome("Período ciclotrônico", pos=(RX, 1.35, 0))
        msg = VGroup(txt("raios diferentes.", T_BODY, opacity=0.95), txt("mesmo período.", T_BODY, opacity=0.95)).arrange(DOWN, buff=0.1).move_to([RX, -1.7, 0])
        self.play(FadeIn(bx), FadeIn(msg), FadeIn(nm_T), run_time=0.8)
        self.hold(2.6)
        self.play(*[FadeOut(m) for m in self.cur.values()], FadeOut(bx), FadeOut(nm_T), FadeOut(ref), FadeOut(msg), FadeOut(bar_bg), FadeOut(bar), FadeOut(t0l),
                  FadeOut(tTl), FadeOut(tcl), FadeOut(len_l), FadeOut(self.fl), FadeOut(self.vl), run_time=0.8)
        self.remove(self.fl, self.vl, bar)
        self.run["tt"] = False
        self.cur = {}
        self.res_fade = (self.cline, self.clab)

    def b02_duas(self):
        """Duas partículas: mesmos m, q, B; só v⊥ muda. Mesma ω (mesmo relógio) → raios diferentes, mesmo período."""
        # limpa a órbita única e reabre a composição: as trajetórias dominam
        self.remove(*self.res_fade)
        self.play(FadeOut(self.trail1), FadeOut(self.q3), FadeOut(self.vp3), FadeOut(self.fm3[0]), FadeOut(self.fm3[1]),
                  self.ox.animate.set_value(-3.5), self.oy.animate.set_value(-0.5), self.gs.animate.set_value(1.4),
                  self.bop.animate.set_value(0.6), run_time=1.6, rate_func=smooth)
        self.tg.set_value(0.0)
        self.tfull = ValueTracker(T_PER)
        c1 = Orbit(VP1, 0.0, 1, self.tg, 0.0, BLUE_L)
        c2 = Orbit(VP1 * 0.5, 0.0, 1, self.tg, 0.0, WHITE)
        s1, s2 = Orbit(VP1, 0.0, 1, self.tfull, 0.0, BLUE_L), Orbit(VP1 * 0.5, 0.0, 1, self.tfull, 0.0, WHITE)
        self.stat_op = ValueTracker(0.9)
        st1, st2 = self.mk_trail(s1, 3.5, optr=self.stat_op), self.mk_trail(s2, 3.5, optr=self.stat_op)
        hyp = VGroup(eq(r"m_1=m_2,\;q_1=q_2,\;B_1=B_2", size=30), eq(r"v_{\perp 1}\neq v_{\perp 2}", size=30)
                     ).arrange(RIGHT, buff=0.7).move_to([0.9, 3.15, 0])
        self.play(FadeIn(st1), FadeIn(st2), FadeIn(hyp), run_time=1.6)

        def ray(orb, ang, name, side):
            def lines():
                c = self.W(np.array([orb.C[0], orb.C[1], 0.0]))
                a = math.radians(ang)
                tip = c + orb.R * self.S() * np.array([math.cos(a), math.sin(a), 0.0])
                return VGroup(Line(c, tip, color=WHITE, stroke_width=2.5), Dot(c, radius=0.05, color=WHITE))

            def lab():
                c = self.W(np.array([orb.C[0], orb.C[1], 0.0]))
                a = math.radians(ang)
                return halo(eqc(name, size=M_M).move_to(c + 0.55 * orb.R * self.S() * np.array([math.cos(a), math.sin(a), 0.0])
                                                        + np.array([0.0, 0.3, 0.0])))
            return always_redraw(lines), always_redraw(lab)

        r1, l1 = ray(s1, 40, "R_1", 1)
        r2, l2 = ray(s2, 140, "R_2", -1)
        self.add(r1, l1, r2, l2)
        concl_r = eq(r"R_1\neq R_2", size=42)
        gR = VGroup(concl_r, box(concl_r)).move_to([4.7, 0.9, 0])
        self.play(FadeIn(r1), FadeIn(l1), FadeIn(r2), FadeIn(l2), FadeIn(gR, shift=0.1 * DOWN), run_time=1.2)
        self.hold(2.0)
        # as duas partem do mesmo ponto e da mesma fase: marca de fase comum (relógio ωt) e passagens juntas
        dc = np.array([4.7, -0.9, 0.0])
        dial = always_redraw(lambda: VGroup(
            Circle(radius=0.55, color=WHITE, stroke_width=2).move_to(dc),
            Line(dc, dc + 0.55 * np.array([-math.cos(OMEGA * self.tg.get_value()), math.sin(OMEGA * self.tg.get_value()), 0.0]),
                 color=WHITE, stroke_width=4),
            Dot(dc + 0.55 * np.array([-1.0, 0.0, 0.0]), radius=0.05, color=VIOLET)))
        dlab = eq(r"\omega t", size=M_M).move_to(dc + np.array([0.0, -0.95, 0.0]))
        tr1, tr2 = self.mk_trail(c1, 4.5), self.mk_trail(c2, 4.5)
        q1, q2 = self.mk_charge(c1), self.mk_charge(c2)
        self.add(tr1, tr2, q1, q2, dial)
        self.play(FadeOut(r1), FadeOut(l1), FadeOut(r2), FadeOut(l2), FadeOut(gR), self.stat_op.animate.set_value(0.3),
                  FadeIn(dlab), run_time=1.0)
        self.run["tg"] = True
        # o gatilho do flash é a passagem física: t = nT (as duas partículas na origem comum); o flash COMEÇA aí
        self.hold(T_PER)
        concl_t = eq("T_1", "=", "T_2", size=42)
        gT = VGroup(concl_t, box(concl_t)).move_to([4.7, 0.9, 0])
        self.play(Flash(self.W(np.zeros(3)), color=VIOLET, flash_radius=0.5, line_length=0.14), FadeIn(gT, shift=0.1 * DOWN),
                  run_time=1.0)
        self.hold(T_PER - 1.0)                # t = 2T
        self.play(Flash(self.W(np.zeros(3)), color=VIOLET, flash_radius=0.5, line_length=0.14), run_time=1.0)
        self.hold(0.8)
        self.run["tg"] = False
        self.cmp = VGroup(tr1, tr2, q1, q2, dial, dlab, hyp, gT, st1, st2)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B03 · hélice: nova condição inicial (v∥ ≠ 0 desde o instante inicial), círculo + translação, passo, variações
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def bloco_03_helice(self):
        self.seg("B")
        self.b03_circulo_e_condicao()
        self.seg("Bx")
        self.b03_helice()
        self.b03_passo()
        self.b03_variacoes()

    def b03_circulo_e_condicao(self):
        # limpa a comparação e volta ao caso circular, só como ponto de partida
        self.play(FadeOut(self.cmp), self.gs.animate.set_value(1.3), self.ox.animate.set_value(-4.2),
                  self.oy.animate.set_value(-0.1), run_time=1.2, rate_func=smooth)
        self.tg.set_value(0.0)
        self.hc = Orbit(VP1, 0.0, 1, self.tg, 0.0, BLUE_L)
        trc, qc, vc = self.mk_trail(self.hc, 3.5), self.mk_charge(self.hc), self.mk_vec(self.hc, "v", WHITE, 6, 5)
        self.add(trc, qc, vc)
        dec = eq(r"\mathbf v", "=", r"\mathbf v_\perp", size=M_L).move_to([CX, 2.2, 0])
        row1 = VGroup(eq(r"\mathbf v_\perp", size=30), txt("→ movimento circular", T_BODY)).arrange(RIGHT, buff=0.3).move_to([CX, 0.9, 0])
        self.play(FadeIn(dec), FadeIn(row1), run_time=0.8)
        self.run["tg"] = True
        self.hold(T_PER * 0.4)
        self.run["tg"] = False
        # NOVA CONDIÇÃO INICIAL: pausa, reconfigura e só então começa uma nova evolução
        newc = VGroup(txt("nova condição inicial", T_BODY), eq(r"x(t)=x_0+v_\parallel t", size=34, colors={0: VIOLET})).arrange(DOWN, buff=0.2).move_to([CX, 0.9, 0])
        dec3 = eq(r"\mathbf v", "=", r"\mathbf v_\parallel", "+", r"\mathbf v_\perp", size=M_L, colors={2: VIOLET}).move_to([CX, 2.2, 0])
        self.play(FadeOut(trc), FadeOut(qc), FadeOut(vc), RT(row1, newc), RT(dec, dec3),
                  self.bop.animate.set_value(0.0), run_time=1.0)
        self.dec3 = dec3
        self.bmode = "b03"
        self.bz1.set_value(7.4)
        self.play(self.bop.animate.set_value(0.8), self.tau.animate.set_value(58.0), self.beta.animate.set_value(15.0),
                  self.gs.animate.set_value(0.85), self.ox.animate.set_value(-4.2), self.oy.animate.set_value(-2.2),
                  run_time=3.2, rate_func=smooth)
        self.newc = newc

    def b03_helice(self):
        # nova trajetória: v∥ constante desde o primeiro instante (sem rampa): z = v∥ t
        self.tg.set_value(0.0)
        self.hn = Orbit(VP1, VPAR, 1, self.tg, 0.0, BLUE_L)
        self.hn.u_max = 1.9 * T_PER
        self.vparB.set_value(VPAR)
        self.vpar_op.set_value(0.0)
        self.trn, self.qn = self.mk_trail(self.hn, 3.6), self.mk_charge(self.hn)
        self.vn = self.mk_vec(self.hn, "v", WHITE, 6, 5)
        self.vln = self.mk_vec(self.hn, "vpar", VIOLET, 6, 4, vis=self.vparB, op=self.vpar_op)
        vlab = always_redraw(lambda: halo(eqc(r"\mathbf v_\parallel", size=M_M, colors={0: VIOLET}).move_to(
            self.W(self.hn.pos() + np.array([0.0, 0.0, VPAR])) + np.array([0.55, 0.0, 0.0]))).set_opacity(self.vpar_op.get_value()))
        vplab = always_redraw(lambda: halo(eqc(r"\mathbf v_\perp", size=M_M).move_to(
            self.W(self.hn.pos() + self.hn.vel() * np.array([1.0, 1.0, 0.0]))
            + 0.45 * (self.Wv(self.hn.vel() * np.array([1.0, 1.0, 0.0])) / (np.linalg.norm(self.Wv(self.hn.vel() * np.array([1.0, 1.0, 0.0]))) + 1e-9)))))
        self.add(self.qn, self.vn, self.vln, vlab, vplab)
        row2 = VGroup(eq(r"\mathbf v_\parallel", size=30, colors={0: VIOLET}), txt("= constante (já definida)", T_BODY)
                      ).arrange(RIGHT, buff=0.3).move_to([CX, -0.4, 0])
        # v∥ aparece JÁ com seu valor (sem crescer), como parte da nova condição inicial
        self.play(self.vpar_op.animate.set_value(1.0), FadeIn(row2), run_time=1.2)
        self.hold(0.8)
        self.add(self.trn)
        self.run["tg"] = True
        self.hold(T_PER * 1.0)
        row3 = txt("círculo + translação = hélice", T_BODY)
        g3 = VGroup(row3, box(row3)).move_to([CX, -1.8, 0])
        self.play(FadeIn(g3, shift=0.1 * DOWN), run_time=1.0)
        self.hold(T_PER * 0.9 + 0.2)
        self.run["tg"] = False
        self.rows3 = VGroup(row2, g3, self.newc, self.dec3)
        self.labs3 = VGroup(vlab, vplab)

    def b03_passo(self):
        hn = self.hn
        self.pm = self.mk_p_marker(hn)
        self.add(self.pm)
        cl, clab = self.mk_center(hn, "R")
        self.add(cl, clab)
        self.cl3 = (cl, clab)
        AT = [CX, -0.3, 0]
        self.play(FadeOut(self.rows3), FadeOut(self.labs3), FadeIn(self.pm), FadeIn(cl), FadeIn(clab), run_time=1.2)
        self.morph(["p", "=", "vpar", "T"], 44, AT, first=True)
        self.hold(1.0)
        self.morph(["p", "=", ("f", ["2pi", "m", "vpar"], ["q", "B"], "b1")], 44, AT, run=1.4)
        bx = box(VGroup(*self.cur.values()))
        self.nome_p = nome("Passo da hélice", pos=(CX, 0.65, 0))
        self.play(FadeIn(bx), FadeIn(self.nome_p), run_time=0.5)
        self.pbox = bx
        self.hold(0.8)
        a = VGroup(eq(r"\mathbf v_\perp", r"\to", "R", size=32), eq(r"\mathbf v_\parallel", r"\to", "p", size=32, colors={0: VIOLET})
                   ).arrange(DOWN, buff=0.3).move_to([CX, -2.1, 0])
        self.play(FadeIn(a), run_time=0.8)
        self.arr_rows = a
        self.hold(1.0)

    def ghost(self, vp, vpar, s, turns, color=WHITE):
        self.run["tv"] = False
        self.tv.set_value(0.0)
        g = Orbit(vp, vpar, s, self.tv, 0.0, color)
        g.u_max = turns * T_PER
        tr, q = self.mk_trail(g, 3.8), self.mk_charge(g)
        self.add(tr, q)
        return g, VGroup(tr, q)

    def b03_variacoes(self):
        n = [CX, 1.4, 0]
        self.main_op = ValueTracker(0.9)
        # a hélice de referência fica discreta; só a trajetória em teste ganha destaque
        self.trn.clear_updaters()
        self.remove(self.trn)
        self.trn = self.mk_trail(self.hn, 3.6, optr=self.main_op)
        self.add(self.trn)
        # da referência fica SÓ a trilha, em baixa opacidade: sem partícula, vetores, cotas, rótulos nem fórmula
        self.play(self.main_op.animate.set_value(0.25), FadeOut(self.arr_rows), FadeOut(self.qn), FadeOut(self.vn),
                  FadeOut(self.vln), FadeOut(self.pm), FadeOut(self.cl3[0]), FadeOut(self.cl3[1]), FadeOut(self.pbox), FadeOut(self.nome_p),
                  *[FadeOut(m) for m in self.cur.values()], run_time=0.9)
        self.cur = {}
        # (a) v⊥ menor: só o raio muda
        na = VGroup(eq(r"v_\perp\downarrow", size=34), eq(r"R\downarrow", r",\ ", r"p\ \text{igual}", size=34)).arrange(DOWN, buff=0.25).move_to(n)
        ga, gga = self.ghost(VP1 * 0.55, VPAR, 1, 1.4)
        cla, clb = self.mk_center(ga, "R")
        self.play(FadeIn(na), run_time=0.7)
        self.add(cla, clb)
        self.run["tv"] = True
        self.hold(1.4 * T_PER + 0.3)
        self.run["tv"] = False
        self.play(FadeOut(gga), FadeOut(cla), FadeOut(clb), run_time=0.6)
        # (b) v∥ maior: só o passo muda (a cota acompanha a trajetória em teste)
        nb = VGroup(eq(r"v_\parallel\uparrow", size=34, colors={0: VIOLET}), eq(r"p\uparrow", r",\ ", r"R\ \text{igual}", size=34)
                    ).arrange(DOWN, buff=0.25).move_to(n)
        gb, ggb = self.ghost(VP1, VPAR * 1.6, 1, 1.0)
        pmb = self.mk_p_marker(gb)
        self.play(RT(na, nb), run_time=0.7)
        self.add(pmb)
        self.run["tv"] = True
        self.hold(1.0 * T_PER + 0.3)
        self.run["tv"] = False
        self.play(FadeOut(ggb), FadeOut(pmb), run_time=0.6)
        # (c) q → −q: gira ao contrário; R, T e p iguais; avança no mesmo sentido ao longo de B
        nc = VGroup(eq(r"q\to-q", size=34), eq(r"\text{gira ao contr\'ario}", size=30), eq(r"\text{avan\c{c}a igual}", size=30)
                    ).arrange(DOWN, buff=0.2).move_to(n)
        gc, ggc = self.ghost(VP1, VPAR, -1, 1.4, VIOLET)
        self.play(RT(nb, nc), run_time=0.7)
        self.run["tv"] = True
        self.hold(1.4 * T_PER + 0.3)
        self.run["tv"] = False
        self.hold(2.0)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # Utilidades B04–B06
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def limpa(self, run=0.9, keep_extra=()):
        """Fecha o bloco anterior: tudo sai, menos marca, cabeçalho e o que for pedido (os relógios/trackers ficam)."""
        keep = (self.wm, self.tag) + tuple(keep_extra)
        mobs = [m for m in self.mobjects if m not in keep and not isinstance(m, ValueTracker)]
        dyn = [m for m in mobs if getattr(m, "dyn", False)]      # estrutura variável: não aceita FadeOut (sai direto)
        self.remove(*dyn)
        mobs = [m for m in mobs if m not in dyn]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run)
        self.cur = {}

    def setcap(self, new, run=0.7):
        """Legenda única: a nova substitui a anterior (ou entra, se ainda não houver)."""
        old = getattr(self, "capb", None)
        if old is not None:
            self.play(RT(old, new), run_time=run)
        else:
            self.play(FadeIn(new), run_time=run)
        self.capb = new

    def delcap(self, run=0.4):
        if getattr(self, "capb", None) is not None:
            self.play(FadeOut(self.capb), run_time=run)
            self.capb = None

    def lab(self, sym, words, size=30, tsize=22, color=WHITE):
        """Símbolo + nome curto, para nascer junto do objeto que representa."""
        return VGroup(eq(sym, size=size, colors={0: color}), txt(words, tsize, opacity=0.95)).arrange(RIGHT, buff=0.15)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B04 · trabalho, rapidez e energia
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def bloco_04_trabalho(self):
        self.b04_rapidez()
        self.b04_potencia()
        self.b04_sistema()

    def b04_rapidez(self):
        self.seg("E")
        # a hélice do B03 se achata no círculo: olhando ao longo de B, a mesma trilha helicoidal projeta-se na órbita circular
        self.capb = None
        self.limpa(0.8, keep_extra=(self.trn,))
        self.tw = self.clock("tw")
        hb = Orbit(VP1, 0.0, 1, self.tw, 0.0, BLUE_L)
        self.hb = hb
        ret = VGroup(txt("retomando o caso", T_BODY, opacity=0.95), eq(r"v_\parallel=0", size=40, colors={0: VIOLET})).arrange(RIGHT, buff=0.3).move_to([0, 2.75, 0])
        retb = box(ret[1])
        self.play(FadeIn(ret), FadeIn(retb), run_time=0.8)
        self.hold(1.6)
        self.play(self.main_op.animate.set_value(0.9), self.tau.animate.set_value(0.0), self.beta.animate.set_value(0.0),
                  self.gs.animate.set_value(1.3), self.ox.animate.set_value(-4.4), self.oy.animate.set_value(-0.5),
                  run_time=3.0, rate_func=smooth)
        self.bop.set_value(0.0)
        self.play(FadeOut(ret), FadeOut(retb), run_time=0.5)
        ques = VGroup(txt("A partícula está acelerando.", 30), txt("Então por que ela não fica mais rápida?", 30)
                      ).arrange(DOWN, buff=0.2).move_to([0, 2.75, 0])
        self.play(FadeIn(ques, shift=0.1 * UP), run_time=1.0)
        self.ques = ques
        self.hold(1.6)
        self.q4, self.tr4 = self.mk_charge(hb), self.mk_trail(hb, 3.5)
        self.vv4, self.ff4 = self.mk_vec(hb, "v", VIOLET, 6, 5, sc=0.65), self.mk_vec(hb, "F", FC, 6, 4)
        self.add(self.tr4, self.q4, self.vv4, self.ff4)
        self.play(FadeOut(self.trn), run_time=0.6)                 # a órbita refeita substitui o resto da hélice achatada
        self.run["tw"] = True
        # painel: o vetor v gira (hodógrafo) e o módulo |v| fica parado num indicador de rapidez
        HC, HS = np.array([4.6, 0.3, 0.0]), 0.6
        hodo = always_redraw(lambda: VGroup(
            Circle(radius=hb.vp * HS, color=WHITE, stroke_width=1.5).set_stroke(opacity=0.35).move_to(HC),
            arrow(HC, HC + HS * np.array([hb.vel()[0], hb.vel()[1], 0.0]), VIOLET, 5, 4),
            Dot(HC, radius=0.04, color=WHITE)))
        t_v = VGroup(eq(r"\mathbf v", size=M_M, colors={0: VIOLET}), txt("muda de direção", T_NOTE, opacity=0.9)).arrange(RIGHT, buff=0.25).move_to([4.6, 1.65, 0])
        GC = np.array([4.6, -1.6, 0.0])
        gauge = always_redraw(lambda: VGroup(
            Rectangle(width=3.2, height=0.24, color=WHITE, stroke_width=2).move_to(GC),
            Rectangle(width=max(0.02, 3.2 * float(np.linalg.norm(hb.vel())) / (1.25 * hb.vp)), height=0.24, stroke_width=0,
                      fill_color=VIOLET, fill_opacity=0.95).move_to(GC + np.array([-1.6, 0.0, 0.0]), aligned_edge=LEFT)))
        lab_n = eq(r"|\mathbf v|", r"\,=", size=M_M, colors={0: VIOLET}).move_to([3.7, -1.15, 0])
        num = DecimalNumber(VP1, num_decimal_places=2, font_size=M_M, color=VIOLET)
        num.add_updater(lambda m: m.set_value(float(np.linalg.norm(hb.vel()))).next_to(lab_n, RIGHT, buff=0.2))
        t_n = txt("constante", T_BODY, opacity=0.95).move_to([4.6, -2.25, 0])
        acc = eq(r"\mathbf a", "=", r"\mathbf F_B", r"/m", r"\neq 0", size=34, colors={0: VIOLET, 2: FC}).move_to([4.6, -2.95, 0])
        self.panel4 = VGroup(hodo, t_v, gauge, lab_n, num, t_n, acc)
        self.play(FadeIn(hodo), FadeIn(t_v), FadeIn(gauge), FadeIn(lab_n), FadeIn(num), run_time=1.0)
        self.hold(1.5)
        self.play(FadeIn(t_n), FadeIn(acc), run_time=0.8)
        self.hold(T_PER * 1.3)

    def b04_potencia(self):
        hb = self.hb
        RX = 3.9
        # espera a partícula chegar ao topo da órbita (v horizontal, F vertical): geometria limpa para nomear os vetores
        u = hb.u()
        w = (0.25 * T_PER - (u % T_PER)) % T_PER
        if w > 0.05:
            self.hold(w)
        self.run["tw"] = False
        self.play(FadeOut(self.panel4), FadeOut(self.ques), run_time=0.8)
        ra = self.mk_rightangle(hb)
        self.add(ra)
        pos = hb.pos()
        p0 = self.W(pos)
        tv = self.W(pos + hb.vel() * np.array([1, 1, 0]) * 0.65)
        tf = self.W(pos + hb.force() * (0.5 / (ABSQ * BM)))
        lv = halo(self.lab(r"\mathbf v", "velocidade", color=VIOLET).move_to(tv + np.array([1.4, 0.35, 0.0])))
        lf = halo(self.lab(r"\mathbf F_B", "força magnética", color=FC).move_to(tf + np.array([1.9, -0.45, 0.0])))
        l90 = eq(r"90^\circ", size=42).move_to(p0 + np.array([0.62, -0.42, 0.0]))
        self.play(FadeIn(lv, shift=0.1 * RIGHT), run_time=0.8)
        self.hold(0.8)
        self.play(FadeIn(lf, shift=0.1 * RIGHT), FadeIn(l90), run_time=0.8)
        self.hold(1.8)
        self.play(FadeOut(lv), FadeOut(lf), FadeOut(l90), run_time=0.5)
        # a órbita volta a girar e fica viva durante toda a dedução: dr é o pequeno deslocamento ao longo da trajetória
        self.run["tw"] = True

        def unit(v):
            return v / (np.linalg.norm(v) + 1e-9)

        def dr_mob():
            v = hb.vel() * np.array([1.0, 1.0, 0.0])
            p = hb.pos()
            tdir = unit(self.Wv(v))
            nout = unit(self.W(p) - self.W(np.array([hb.C[0], hb.C[1], p[2]])))
            a = self.W(p) + 0.22 * nout
            b = a + 0.5 * tdir
            return VGroup(arrow(a, b, WHITE, 7, 7, tip=0.2),
                          halo(eqc(r"d\mathbf r", size=M_M).move_to(b + 0.35 * unit(0.6 * tdir + 0.8 * nout))))

        drm = always_redraw(dr_mob)
        AT, SZ = [RX, 0.2, 0], 54
        cap = txt("trabalho em um deslocamento", T_NOTE, opacity=0.95).move_to([RX, 2.4, 0])
        wd = eq("dW", "=", r"\mathbf F", r"\cdot", r"d\mathbf r", size=SZ, colors={0: CYAN, 2: FC}).move_to(AT)
        self.add(drm)
        self.play(FadeIn(cap), FadeIn(drm), FadeIn(wd, shift=0.1 * UP), run_time=1.2)
        self.hold(2.2)
        perp = eq(r"\mathbf F_B\perp d\mathbf r", r"\Rightarrow\ dW_B=0", size=36, colors={0: FC, 1: CYAN}).move_to([RX, -1.5, 0])
        self.play(FadeIn(perp, shift=0.1 * UP), run_time=0.9)
        self.hold(2.0)
        # potência: dW por unidade de tempo → F · dr/dt → F · v
        self.play(FadeOut(perp), FadeOut(cap), run_time=0.5)
        cap2 = txt("potência: trabalho por tempo", T_NOTE, opacity=0.95).move_to([RX, 2.4, 0])
        p1 = eq("P", "=", r"\frac{dW}{dt}", size=SZ, colors={0: CYAN, 2: CYAN}).move_to(AT)
        self.play(RT(wd, p1), FadeIn(cap2), run_time=1.2)
        self.hold(1.4)
        p2 = eq("P", "=", r"\frac{\mathbf F\cdot d\mathbf r}{dt}", size=SZ, colors={0: CYAN}).move_to(AT)
        self.play(RT(p1, p2), run_time=1.3)
        self.hold(1.2)
        p3 = eq("P", "=", r"\mathbf F\cdot", r"\frac{d\mathbf r}{dt}", size=SZ, colors={0: CYAN, 1: FC}).move_to(AT)
        self.play(RT(p2, p3), run_time=1.3)
        self.hold(1.0)
        rv = eq(r"\frac{d\mathbf r}{dt}", "=", r"\mathbf v", size=40, colors={2: VIOLET}).move_to([RX, -1.5, 0])
        self.play(FadeIn(rv, shift=0.1 * UP), run_time=0.9)
        self.hold(1.4)
        p4 = eq("P", "=", r"\mathbf F", r"\cdot", r"\mathbf v", size=60, colors={0: CYAN, 2: FC, 4: VIOLET}).move_to(AT)
        self.play(RT(p3, p4), FadeOut(rv), run_time=1.3)
        b4 = box(p4)
        self.play(FadeIn(b4), run_time=0.5)
        self.hold(2.0)
        # aplicada à força magnética
        self.play(FadeOut(p4), FadeOut(b4), FadeOut(cap2), FadeOut(drm), run_time=0.7)
        self.remove(drm)
        cap = txt("a potência da força magnética", T_BODY, opacity=0.95).move_to([RX, 2.4, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.morph(["PB", "=", "FB@a", "dot", "v@a"], SZ, AT, first=True, run=1.2)
        self.hold(1.2)
        self.morph(["PB", "=", "qs", "(", "v@b", "times", "Bv", ")", "dot", "v@a"], SZ, AT, alias={"FB@a": ["qs", "(", "v@b", "times", "Bv", ")"]}, run=1.4)
        self.hold(0.8)
        note = eq(r"\mathbf v", r"\times", r"\mathbf B", r"\ \perp\ ", r"\mathbf v", size=36, colors={0: VIOLET, 2: MAG, 4: VIOLET}).move_to([RX, -1.7, 0])
        self.play(FadeIn(note, shift=0.1 * UP), run_time=0.8)
        self.hold(1.2)
        self.morph(["PB", "=", "0"], SZ, AT, run=1.2)
        bx = box(VGroup(*self.cur.values()))
        self.play(FadeIn(bx), run_time=0.5)
        self.hold(1.4)
        self.play(FadeOut(bx), FadeOut(note), FadeOut(cap), run_time=0.5)
        # trabalho
        cap = VGroup(eq("W_B", size=34, colors={0: CYAN}), txt("trabalho da força magnética", T_BODY, opacity=0.95)).arrange(RIGHT, buff=0.2).move_to([RX, 2.4, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.morph(["WB", "=", "int", "PB", "dtt", "=@2", "0"], SZ, AT, run=1.4)
        bx = box(VGroup(*[m for k, m in self.cur.items()]))
        self.play(FadeIn(bx), run_time=0.5)
        self.hold(1.4)
        self.play(FadeOut(bx), FadeOut(cap), *[FadeOut(m) for m in self.cur.values()], run_time=0.6)
        self.cur = {}
        # energia cinética: K identificada e hipótese explícita antes de concluir ΔK = 0
        kdef = eq(r"E_c", "=", r"\frac12 m", r"|\mathbf v|^2", size=SZ, colors={3: VIOLET}).move_to(AT)
        kcap = VGroup(eq(r"E_c", size=34), txt("energia cinética", T_BODY, opacity=0.95)).arrange(RIGHT, buff=0.2).move_to([RX, 2.4, 0])
        self.play(FadeIn(kdef), FadeIn(kcap), run_time=0.9)
        self.hold(1.6)
        hyp = txt("só a força magnética atua", T_BODY, opacity=0.95).move_to([RX, 2.4, 0])
        self.play(FadeOut(kdef), RT(kcap, hyp), run_time=0.7)
        self.morph(["dK", "=", "WB", "=@2", "0"], SZ, AT, first=True, run=1.2)
        bx = box(VGroup(*self.cur.values()))
        nm_W = nome("Teorema trabalho–energia", pos=(RX, 1.15, 0))
        msg = eq(r"E_c", r"\ \text{constante}\ \Rightarrow\ ", r"|\mathbf v|", r"\ \text{constante}", size=38, colors={2: VIOLET}).move_to([RX, -1.5, 0])
        note2 = VGroup(eq(r"E_c", size=28), txt("pode mudar se outra força realizar trabalho", 20, opacity=0.8)).arrange(RIGHT, buff=0.15).move_to([RX, -2.5, 0])
        self.play(FadeIn(bx), FadeIn(msg), FadeIn(nm_W), run_time=0.8)
        self.hold(1.2)
        self.play(FadeIn(note2), run_time=0.7)
        self.hold(2.4)
        self.play(*[FadeOut(m) for m in self.cur.values()], FadeOut(bx), FadeOut(msg), FadeOut(note2), FadeOut(hyp), FadeOut(nm_W), run_time=0.8)
        self.cur = {}
        self.run["tw"] = False

    def b04_sistema(self):
        """M1-18, curto: o termo magnético não trabalha sobre a carga, mas o sistema completo pode transferir energia."""
        self.limpa(0.6)
        labels = ["fonte\nelétrica", "corrente", "interação\nmagnética", "movimento\nmecânico"]
        cols = [CYAN, GREEN, MAG, VIOLET]
        xs = [-5.2, -1.75, 1.75, 5.2]
        cards = VGroup()
        for lb, x, c in zip(labels, xs, cols):
            r = RoundedRectangle(corner_radius=0.18, width=2.7, height=1.3).set_fill(PANEL, 0.75).set_stroke(c, 3, 0.9)
            cards.add(VGroup(r, txt(lb, 24)).move_to([x, 0.9, 0]).set_z_index(2))      # o texto do card fica SEMPRE acima do pulso
        arrs = VGroup(*[arrow([xs[i] + 1.5, 0.9, 0], [xs[i + 1] - 1.5, 0.9, 0], cols[i + 1], 5, 2) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(n) for n in cards], lag_ratio=0.25), FadeIn(arrs), run_time=1.8)
        prog = ValueTracker(0.0)

        def pulse_f():
            x = xs[0] + prog.get_value() * (xs[3] - xs[0])
            k = min(2.999, max(0.0, (x - xs[0]) / (xs[1] - xs[0])))
            i = int(k)
            col = interpolate_color(ManimColor(cols[i]), ManimColor(cols[i + 1]), k - i)
            return VGroup(Circle(radius=0.3, stroke_width=0).set_fill(col, 0.22), Dot([0, 0, 0], radius=0.13, color=col)
                          .set_stroke(WHITE, 2)).move_to([x, 0.9, 0]).set_z_index(1)

        def glow_f(c, x):
            px = xs[0] + prog.get_value() * (xs[3] - xs[0])
            w = 2.0 + 6.0 * max(0.0, 1 - abs(px - x) / 1.6)           # o card se acende quando o pulso passa
            return RoundedRectangle(corner_radius=0.18, width=2.7, height=1.3).move_to([x, 0.9, 0]).set_fill(c, 0.0).set_stroke(c, w, 1.0).set_z_index(3)

        glows = [always_redraw(lambda c=c, x=x: glow_f(c, x)) for c, x in zip(cols, xs)]
        pulse = always_redraw(pulse_f)
        self.add(pulse, *glows)
        self.play(prog.animate.set_value(1.0), run_time=3.6, rate_func=linear)
        self.remove(pulse, *glows)
        self.play(Indicate(cards[2], color=MAG, scale_factor=1.06), run_time=0.8)
        m1 = VGroup(eq("W_B", "=0", size=M_M, colors={0: CYAN}), txt("a carga não recebe trabalho do termo magnético", T_NOTE, opacity=0.95)
                    ).arrange(RIGHT, buff=0.35).move_to([0, -0.9, 0])
        m2 = txt("mas o sistema pode transferir energia", T_NOTE, opacity=0.95).move_to([0, -1.7, 0])
        self.play(FadeIn(m1, shift=0.1 * UP), run_time=0.9)
        self.hold(1.2)
        self.play(FadeIn(m2, shift=0.1 * UP), run_time=0.9)
        self.hold(2.2)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B05 · da carga individual para I, K e J
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def b05_elemento_de_fio(self):
        WY = self.WY
        AT, SZ = [0.5, -1.7, 0], 50
        xa, xb = -3.0, -1.6
        xm = (xa + xb) / 2
        elem = VGroup(DashedLine([xa, WY + 0.5, 0], [xb, WY + 0.5, 0], dash_length=0.1, color=WHITE, stroke_width=2.5),
                      DashedLine([xa, WY - 0.5, 0], [xb, WY - 0.5, 0], dash_length=0.1, color=WHITE, stroke_width=2.5),
                      Line([xa, WY - 0.5, 0], [xa, WY + 0.5, 0], color=WHITE, stroke_width=2.5),
                      Line([xb, WY - 0.5, 0], [xb, WY + 0.5, 0], color=WHITE, stroke_width=2.5))
        dlab = eq(r"d\ell", size=M_M).move_to([xm, WY + 0.95, 0])
        # 1) um pequeno trecho do fio: comprimento dℓ e a carga dq que ele contém
        self.capb = self.cap2
        self.setcap(txt("trecho do fio: comprimento dℓ", T_NOTE, opacity=0.95).move_to([0, -0.6, 0]))
        self.play(FadeIn(elem), FadeIn(dlab), run_time=1.0)
        self.hold(1.4)
        dqlab = eq("dq", size=M_M, colors={0: BLUE_L}).move_to([xm, WY - 1.15, 0])
        self.setcap(txt("carga contida no trecho", T_NOTE, opacity=0.95).move_to([0, -0.6, 0]))
        self.play(FadeIn(dqlab), run_time=0.7)
        self.hold(1.4)
        # 2) λ: carga por comprimento
        self.setcap(VGroup(eq(r"\lambda\!:", size=32, colors={0: BLUE_L}), txt("carga / comprimento", T_NOTE, opacity=0.95)
                           ).arrange(RIGHT, buff=0.1).move_to([0, -0.6, 0]))
        self.morph(["lam", "=", ("f", ["dq"], ["dl"], "b1")], SZ, AT, first=True, run=1.2)
        self.hold(1.8)
        self.morph(["dq", "=", "lam", "dl"], SZ, AT, run=1.3)
        self.hold(1.4)
        self.play(FadeOut(elem), FadeOut(dlab), FadeOut(dqlab), *[FadeOut(m) for m in self.cur.values()], run_time=0.7)
        self.cur = {}
        # 3) corrente: carga que atravessa uma seção durante dt
        xs_ = 0.4
        plane = Line([xs_, WY - 0.55, 0], [xs_, WY + 0.55, 0], color=WHITE, stroke_width=3.5)
        bnd = VGroup(DashedLine([xs_ - 1.1, WY + 0.5, 0], [xs_, WY + 0.5, 0], dash_length=0.1, color=WHITE, stroke_width=2.5),
                     DashedLine([xs_ - 1.1, WY - 0.5, 0], [xs_, WY - 0.5, 0], dash_length=0.1, color=WHITE, stroke_width=2.5),
                     Line([xs_ - 1.1, WY - 0.5, 0], [xs_ - 1.1, WY + 0.5, 0], color=WHITE, stroke_width=2.5))
        vdt = eq(r"v\,dt", size=M_M, colors={0: VIOLET}).move_to([xs_ - 0.55, WY + 0.95, 0])
        sec = txt("seção", 22, opacity=0.9).move_to([xs_ + 0.55, WY + 0.85, 0])
        self.setcap(VGroup(eq("dt", size=32, colors={0: VIOLET}), txt("dq cruza a seção", T_NOTE, opacity=0.95)
                           ).arrange(RIGHT, buff=0.15).move_to([0, -0.6, 0]))
        self.play(FadeIn(plane), FadeIn(bnd), FadeIn(vdt), FadeIn(sec), run_time=0.9)
        self.hold(1.6)
        self.setcap(VGroup(eq("I", size=32, colors={0: GREEN}), txt("carga / tempo", T_NOTE, opacity=0.95)
                           ).arrange(RIGHT, buff=0.15).move_to([0, -0.6, 0]))
        self.morph(["I", "=", ("f", ["dq"], ["dt@d"], "b1")], SZ, AT, first=True, run=1.2)
        self.hold(1.4)
        # nos portadores do modelo: durante dt percorrem v dt, então dq = λ v dt
        self.setcap(txt("em dt, cada portador percorre v dt", T_NOTE, opacity=0.95).move_to([0, -0.6, 0]))
        dq3 = eq("dq", "=", r"\lambda", "v", "dt", size=40, colors={0: BLUE_L, 2: BLUE_L, 3: VIOLET, 4: VIOLET}).move_to([0.5, -2.75, 0])
        self.play(FadeIn(dq3, shift=0.1 * UP), run_time=0.8)
        self.hold(1.4)
        self.morph(["I", "=", ("f", ["lam", "vs", "dt@n"], ["dt@d"], "b1")], SZ, AT, alias={"dq": ["lam", "vs", "dt@n"]}, run=1.4)
        self.play(FadeOut(dq3), run_time=0.4)
        self.hold(0.6)
        lines = self.strike(self.cur["dt@n"], self.cur["dt@d"])
        c = self.cur
        self.play(FadeOut(c["dt@n"]), FadeOut(c["dt@d"]), FadeOut(lines), run_time=0.7)
        del c["dt@n"], c["dt@d"]
        self.morph(["I", "=", "lam", "vs"], SZ, AT, run=1.2)
        bx = box(VGroup(*self.cur.values()))
        self.play(FadeIn(bx), run_time=0.5)
        self.hold(1.4)
        # 4) força no elemento: Lorentz aplicada à carga dq já conhecida
        self.delcap()
        dlv = arrow([xa, WY + 0.0, 0], [xb, WY + 0.0, 0], WHITE, 6, 6)
        dlv_l = eq(r"d\boldsymbol\ell", size=M_M).move_to([xm, WY + 0.55, 0])
        dF = arrow([xm, WY - 0.3, 0], [xm, WY - 1.0, 0], FC, 7, 6)
        dF_l = eq(r"d\mathbf F", size=M_M, colors={0: FC}).move_to([xm + 0.55, WY - 0.85, 0])
        self.play(FadeOut(bx), FadeOut(plane), FadeOut(bnd), FadeOut(vdt), FadeOut(sec), *[FadeOut(m) for m in self.cur.values()], run_time=0.7)
        self.cur = {}
        self.play(FadeIn(dlv), FadeIn(dlv_l), run_time=0.7)
        self.morph(["dF", "=", "dq", "vv@a", "times", "Bv"], SZ, AT, first=True)
        self.play(FadeIn(dF), FadeIn(dF_l), run_time=0.7)
        self.hold(1.4)
        self.morph(["dF", "=", "lam", "dl", "vv@a", "times", "Bv"], SZ, AT, alias={"dq": ["lam", "dl"]}, run=1.2)
        self.hold(0.8)
        note2 = txt("v e dℓ: mesmo sentido", T_NOTE, opacity=0.9).move_to([0.5, -2.6, 0])
        self.play(FadeIn(note2), run_time=0.6)
        self.morph(["dF", "=", "lam", "dlv", "vs", "times", "Bv"], SZ, AT, alias={"dl": ["dlv"], "vv@a": ["vs"]}, run=1.3)
        self.hold(1.0)
        self.play(FadeOut(note2), run_time=0.4)
        note3 = eq(r"\lambda", r"\,v", "=", "I", size=40, colors={0: BLUE_L, 1: VIOLET, 3: GREEN}).move_to([0.5, -2.6, 0])
        self.play(FadeIn(note3), run_time=0.6)
        self.morph(["dF", "=", "I", "dlv", "times", "Bv"], SZ, AT, alias={"lam": ["I"]}, run=1.4)
        bx = box(VGroup(*self.cur.values()))
        self.play(FadeIn(bx), run_time=0.5)
        self.hold(1.6)
        self.play(FadeOut(bx), FadeOut(note3), run_time=0.5)
        self.morph(["F", "=", "int", "I", "dlv", "times", "Bv"], SZ, AT, run=1.4)
        bx = box(VGroup(*self.cur.values()))
        n4 = txt("dℓ segue a corrente convencional", T_NOTE, opacity=0.9).move_to([0.5, -2.7, 0])
        nm_fio = nome("Força magnética sobre um fio com corrente", pos=(0.5, -0.8, 0))
        self.play(FadeIn(bx), FadeIn(n4), FadeIn(nm_fio), run_time=0.8)
        self.hold(2.0)
        self.play(FadeOut(bx), FadeOut(n4), FadeOut(nm_fio), *[FadeOut(m) for m in (dlv, dlv_l, dF, dF_l)], run_time=0.7)
        self.fint = dict(self.cur)

    def b05_linha_superficie_volume(self):
        """Linha → superfície → volume como UMA transformação; cada densidade nasce de um elemento marcado no desenho."""
        self.seg("F2")                               # SEG=F2: só linha → superfície → volume
        self.play(self.g5.animate.set_value(0.0), FadeOut(self.wire5), *[FadeOut(m) for m in self.cur.values()], run_time=0.7)
        self.remove(self.car5)
        self.cur = {}
        self.pw, self.pt, self.pph = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.hl, self.hq = ValueTracker(0.0), ValueTracker(0.0)      # hl: seção transversal ao fluxo · hq: elemento que contém carga
        self.psc, self.pbx, self.pby = ValueTracker(1.0), ValueTracker(-5.4), ValueTracker(-1.0)
        self.pph.add_updater(lambda m, dt: m.increment_value(0.9 * dt))
        self.add(self.pph)
        EXp, EYp, EZp = np.array([1.0, 0.0, 0.0]), np.array([0.5, 0.34, 0.0]), np.array([0.0, 1.0, 0.0])
        L = 5.2

        def P3(x, y, z):
            s = self.psc.get_value()
            return np.array([self.pbx.get_value(), self.pby.get_value(), 0.0]) + s * (x * EXp + y * EYp + z * EZp)

        def prism():
            w, t, hl, hq = self.pw.get_value(), self.pt.get_value(), self.hl.get_value(), self.hq.get_value()
            s = self.psc.get_value()
            g = VGroup()
            if w < 0.03 and t < 0.03:
                g.add(Line(P3(0, 0, 0), P3(L, 0, 0), color=BLUE_L, stroke_width=6))
            else:
                top = Polygon(P3(0, 0, t), P3(L, 0, t), P3(L, w, t), P3(0, w, t), color=BLUE_L, stroke_width=2.5,
                              fill_color=BLUE, fill_opacity=0.16)
                if t > 0.03:
                    front = Polygon(P3(0, 0, 0), P3(L, 0, 0), P3(L, 0, t), P3(0, 0, t), color=BLUE_L, stroke_width=2.5,
                                    fill_color=BLUE, fill_opacity=0.10)
                    end = Polygon(P3(L, 0, 0), P3(L, w, 0), P3(L, w, t), P3(L, 0, t), color=BLUE_L, stroke_width=2.5,
                                  fill_color=BLUE, fill_opacity=0.22)
                    g.add(front, end)
                g.add(top)
            ny = 1 if w < 0.05 else int(round(w / 0.8)) + 1
            nz = 1 if t < 0.05 else int(round(t / 0.5)) + 1
            ph = self.pph.get_value()
            for j in range(ny):
                yy = 0.0 if ny == 1 else w * j / (ny - 1)
                for k in range(nz):
                    zz = 0.0 if nz == 1 else t * k / (nz - 1)
                    zz = zz if t > 0.05 else 0.0
                    for i in range(4):
                        x = (ph + i * L / 4) % L
                        op = min(1.0, max(0.0, min(x, L - x) / 0.4))
                        g.add(arrow(P3(x, yy, zz), P3(x + 0.4, yy, zz), GREEN, 3.5, 4, tip=0.14 * max(s, 0.6)).set_opacity(0.85 * op))
            if hl > 0.02:                      # seção transversal ao fluxo: faixa dw (superfície) ou área dA_perp (volume)
                y0 = 0.35 * w
                if t < 0.05:
                    g.add(Line(P3(L, y0, 0), P3(L, y0 + 0.5, 0), color=GREEN, stroke_width=8).set_opacity(hl))
                else:
                    g.add(Polygon(P3(L, y0, 0.2 * t), P3(L, y0 + 0.5, 0.2 * t), P3(L, y0 + 0.5, 0.6 * t), P3(L, y0, 0.6 * t),
                                  color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5 * hl))
            if hq > 0.02:                      # elemento que contém carga: dA_sup (superfície) ou dτ (volume)
                if t < 0.05:
                    g.add(Polygon(P3(2.2, 1.2, 0), P3(3.0, 1.2, 0), P3(3.0, 1.9, 0), P3(2.2, 1.9, 0), color=BLUE_L, stroke_width=3,
                                  fill_color=BLUE_L, fill_opacity=0.35 * hq))
                    cen = P3(2.6, 1.55, 0)
                else:
                    a0, a1, b0, b1, c0_, c1_ = 2.1, 2.9, 0.8, 1.6, 0.25, 0.8
                    g.add(Polygon(P3(a0, b0, c0_), P3(a1, b0, c0_), P3(a1, b0, c1_), P3(a0, b0, c1_), color=BLUE_L, stroke_width=2.5,
                                  fill_color=BLUE_L, fill_opacity=0.25 * hq),
                          Polygon(P3(a1, b0, c0_), P3(a1, b1, c0_), P3(a1, b1, c1_), P3(a1, b0, c1_), color=BLUE_L, stroke_width=2.5,
                                  fill_color=BLUE_L, fill_opacity=0.4 * hq),
                          Polygon(P3(a0, b0, c1_), P3(a1, b0, c1_), P3(a1, b1, c1_), P3(a0, b1, c1_), color=BLUE_L, stroke_width=2.5,
                                  fill_color=BLUE_L, fill_opacity=0.3 * hq))
                    cen = P3((a0 + a1) / 2, (b0 + b1) / 2, (c0_ + c1_) / 2)
                g.add(charge_c(cen, 1, 0.3).set_opacity(hq))
            return g

        self.prism = always_redraw(prism)
        right = np.array([4.4, 0.0, 0.0])

        def panel(*mobs):
            return VGroup(*mobs).arrange(DOWN, buff=0.26).move_to(right)

        def named(sym, words, color):
            return VGroup(eq(sym, size=60, colors={0: color}), txt(words, 20, opacity=0.9)).arrange(RIGHT, buff=0.3)

        self.prism.dyn = True
        self.add(self.prism)
        c0 = panel(txt("corrente numa linha", 22, opacity=0.9), eq("I", size=60, colors={0: GREEN}))
        self.play(FadeIn(c0), run_time=1.0)
        self.hold(2.2)
        # ── linha → superfície ────────────────────────────────────────────────────────────────────────────
        c1 = panel(txt("a linha ganha largura", 22, opacity=0.9))
        self.play(self.pw.animate.set_value(2.6), RT(c0, c1), run_time=2.0, rate_func=smooth)
        self.hold(0.8)
        # faixa de largura dw (marcada no desenho) → K, dI = K dw
        lab_dw = eq("dw", size=M_M, colors={0: GREEN}).move_to(P3(L, 0.35 * 2.6 + 0.25, 0) + np.array([0.65, -0.3, 0.0]))
        c2 = panel(named(r"\mathbf K", "corrente / largura", GREEN),
                   eq("dI", "=", r"|\mathbf K|", "dw", size=44, colors={0: GREEN, 2: GREEN}),
                   eq(r"[\mathbf K]", "=", r"\mathrm{A/m}", size=34, colors={0: GREEN}))
        self.play(self.hl.animate.set_value(1.0), FadeIn(lab_dw), RT(c1, c2), run_time=1.2)
        self.hold(3.0)
        # elemento da superfície carregada dA_sup que contém dq → σ, dq = σ dA_sup
        _la = eq(r"dA_{\mathrm{sup}}", size=M_M).move_to(P3(2.6, 1.55, 0) + np.array([-1.2, 1.0, 0.0]))
        _ll = Line(_la.get_right() + np.array([0.05, -0.05, 0.0]), P3(2.55, 1.6, 0) + np.array([-0.1, 0.0, 0.0]), color=WHITE, stroke_width=1.6).set_opacity(0.85)
        lab_as = VGroup(_la, _ll)
        lab_dq = eq("dq", size=42, colors={0: BLUE_L}).move_to(P3(2.6, 1.55, 0) + np.array([0.95, -0.6, 0.0]))
        c3 = panel(named(r"\sigma", "carga / área", BLUE_L),
                   eq("dq", "=", r"\sigma", r"dA_{\mathrm{sup}}", size=44, colors={0: BLUE_L, 2: BLUE_L}),
                   eq(r"[\sigma]", "=", r"\mathrm{C/m^2}", size=34, colors={0: BLUE_L}))
        self.play(self.hl.animate.set_value(0.0), FadeOut(lab_dw), self.hq.animate.set_value(1.0), FadeIn(lab_as), FadeIn(lab_dq),
                  RT(c2, c3), run_time=1.2)
        self.hold(3.2)
        c3b = panel(txt("espécie com velocidade v", 20, opacity=0.9), eq(r"\mathbf K", "=", r"\sigma", r"\mathbf v", size=54, colors={0: GREEN, 2: BLUE_L, 3: VIOLET}))
        self.play(RT(c3, c3b), run_time=1.0)
        self.hold(2.4)
        # ── superfície → volume ───────────────────────────────────────────────────────────────────────────
        c4 = panel(txt("a superfície ganha espessura", 22, opacity=0.9))
        self.play(self.pt.animate.set_value(1.1), self.hq.animate.set_value(0.0), FadeOut(lab_as), FadeOut(lab_dq),
                  RT(c3b, c4), run_time=2.0, rate_func=smooth)
        self.hold(0.8)
        lab_ap = eq(r"dA_\perp", size=M_M, colors={0: GREEN}).move_to(P3(L, 0.35 * 2.6 + 0.25, 0.44) + np.array([0.8, 0.05, 0.0]))
        c5 = panel(named(r"\mathbf J", "corrente / área", GREEN),
                   eq("dI", "=", r"|\mathbf J|", r"dA_\perp", size=44, colors={0: GREEN, 2: GREEN}),
                   eq(r"[\mathbf J]", "=", r"\mathrm{A/m^2}", size=34, colors={0: GREEN}))
        self.play(self.hl.animate.set_value(1.0), FadeIn(lab_ap), RT(c4, c5), run_time=1.2)
        self.hold(3.0)
        lab_dt = eq(r"d\tau", size=M_M).move_to(P3(2.5, 1.2, 0.55) + np.array([0.0, 0.7, 0.0]))
        lab_dq2 = eq("dq", size=42, colors={0: BLUE_L}).move_to(P3(2.5, 1.2, 0.55) + np.array([1.05, -0.5, 0.0]))
        c6 = panel(named(r"\rho", "carga / volume", BLUE_L),
                   eq("dq", "=", r"\rho", r"d\tau", size=44, colors={0: BLUE_L, 2: BLUE_L}),
                   eq(r"[\rho]", "=", r"\mathrm{C/m^3}", size=34, colors={0: BLUE_L}))
        self.play(self.hl.animate.set_value(0.0), FadeOut(lab_ap), self.hq.animate.set_value(1.0), FadeIn(lab_dt), FadeIn(lab_dq2),
                  RT(c5, c6), run_time=1.2)
        self.hold(3.2)
        c6b = panel(txt("espécie com velocidade v", 20, opacity=0.9), eq(r"\mathbf J", "=", r"\rho", r"\mathbf v", size=54, colors={0: GREEN, 2: BLUE_L, 3: VIOLET}))
        self.play(RT(c6, c6b), run_time=1.0)
        self.hold(2.4)
        # ── várias espécies: ρ_i inclui o sinal da carga ─────────────────────────────────────────────────
        sp = ValueTracker(0.0)

        def species():
            g = VGroup()
            ph = self.pph.get_value()
            for i in range(5):
                x = (ph * 1.2 + i * L / 5) % L
                g.add(charge_c(P3(x, 0.4 + 0.3 * (i % 3), 0.35 + 0.25 * (i % 2)), 1, 0.3))
                x2 = (L - (ph * 0.8 + i * L / 5) % L)
                g.add(charge_c(P3(x2, 1.4 + 0.3 * (i % 3), 0.5 + 0.25 * (i % 2)), -1, 0.3))
            return g.set_z_index(6).set_opacity(sp.get_value())

        self.spec = always_redraw(species)
        self.spec.dyn = True
        self.add(self.spec)
        c7 = panel(txt("duas espécies de portador", 22, opacity=0.9),
                   VGroup(eq(r"\rho_1", ">0", size=34, colors={0: BLUE_L}), eq(r"\rho_2", "<0", size=34, colors={0: BLUE_L})).arrange(RIGHT, buff=0.5),
                   VGroup(eq(r"\rho_i", size=30, colors={0: BLUE_L}), txt("com sinal", 20, opacity=0.9)).arrange(RIGHT, buff=0.12),
                   eq(r"\mathbf J", "=", r"\rho_1", r"\mathbf v_1", "+", r"\rho_2", r"\mathbf v_2", size=38, colors={0: GREEN, 2: BLUE_L, 3: VIOLET, 5: BLUE_L, 6: VIOLET}),
                   txt("− para a esquerda = J para a direita", 20, opacity=0.8))
        self.play(sp.animate.set_value(1.0), FadeOut(lab_dt), FadeOut(lab_dq2), self.hq.animate.set_value(0.0),
                  RT(c6b, c7), run_time=1.4)
        self.hold(3.0)
        c8 = panel(VGroup(txt("uma espécie:", 24), eq(r"\mathbf J", "=", r"\rho", r"\mathbf v", size=34, colors={0: GREEN, 2: BLUE_L, 3: VIOLET})).arrange(RIGHT, buff=0.2),
                   txt("somamos as contribuições", 20, opacity=0.9),
                   eq(r"\mathbf J", "=", r"\sum_i", r"\rho_i", r"\mathbf v_i", size=50, colors={0: GREEN, 3: BLUE_L, 4: VIOLET}),
                   eq(r"\rho_{\mathrm{liq}}", r"=0\ \not\Rightarrow\ ", r"\mathbf J", "=0", size=34, colors={0: BLUE_L, 2: GREEN}))
        c8.arrange(DOWN, buff=0.45).move_to(right)
        self.play(RT(c7, c8), run_time=1.0)
        bxs = box(c8[2])
        self.play(FadeIn(bxs), run_time=0.5)
        self.hold(3.0)
        # ── a mesma interação em linha, superfície e volume (o objeto físico vira só uma referência discreta) ──
        self.play(FadeOut(c8), FadeOut(bxs), FadeOut(self.spec), self.psc.animate.set_value(0.4),
                  self.pbx.animate.set_value(-6.6), self.pby.animate.set_value(1.7), run_time=1.0)
        AT, SZ = [0.8, -0.1, 0], 52
        self.play(self.pt.animate.set_value(0.0), self.pw.animate.set_value(0.0), run_time=0.8)
        self.morph(["F", "=", "int", "I", "dlv", "times", "Bv"], SZ, AT, first=True)
        self.hold(1.4)
        self.play(self.pw.animate.set_value(2.6), run_time=0.8)
        self.morph(["F", "=", "int", "Kv", "times", "Bv", "dA"], SZ, AT, alias={"I": ["Kv"], "dlv": ["dA"]}, run=1.4)
        self.hold(1.4)
        self.play(self.pt.animate.set_value(1.1), run_time=0.8)
        self.morph(["F", "=", "int", "Jv", "times", "Bv", "dtau"], SZ, AT, alias={"Kv": ["Jv"], "dA": ["dtau"]}, run=1.4)
        fin = txt("a mesma interação: linha, superfície, volume", T_NOTE, opacity=0.95).move_to([0.8, -2.3, 0])
        self.play(FadeIn(fin), run_time=0.8)
        self.hold(3.0)

    def clock(self, name):
        """Relógio próprio (ValueTracker avançado por dt enquanto self.run[name] for verdadeiro)."""
        tr = ValueTracker(0.0)
        self.run[name] = False
        tr.add_updater(lambda m, dt, n=name: m.increment_value(dt) if self.run[n] else None)
        self.add(tr)
        return tr

    def band(self, pts, color=VIOLET, op=0.9, w=2.5, dash=False):
        ln = DashedLine(pts[0], pts[1], dash_length=0.1, color=color, stroke_width=w) if dash else Line(pts[0], pts[1], color=color, stroke_width=w)
        return ln.set_opacity(op)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B04 · trabalho, rapidez e energia
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def bloco_04_trabalho(self):
        self.b04_rapidez()
        self.b04_potencia()
        self.b04_sistema()

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B05 · da carga individual para I, K e J
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def bloco_05_correntes(self):
        self.b05_muitas_cargas()
        self.b05_elemento_de_fio()
        self.b05_linha_superficie_volume()

    def b05_muitas_cargas(self):
        self.seg("F")
        self.limpa()
        WY = 1.5
        self.WY = WY
        wire = Line([-6.2, WY, 0], [3.9, WY, 0], color=BLUE_L, stroke_width=7).set_opacity(0.45)
        bdots = VGroup()
        for yy in (0.45, 2.55):
            for xx in np.arange(-6.0, 4.0, 1.25):
                bdots.add(Circle(radius=0.075, color=MAG, stroke_width=2).set_opacity(0.4).move_to([xx, yy, 0]),
                          Dot([xx, yy, 0], radius=0.025, color=MAG).set_opacity(0.4))
        blab = eq(r"\mathbf B", r"\odot", size=M_M, colors={0: MAG, 1: MAG}).move_to([5.6, 2.3, 0])
        self.ph5, self.m5, self.g5 = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.ph5.add_updater(lambda m, dt: m.increment_value(1.1 * dt))
        self.add(self.ph5)
        N, SP, X0, LEN = 8, 1.3, -6.0, 10.4

        def carriers():
            g = VGroup()
            for k in range(N):
                x = X0 + ((k * SP + self.ph5.get_value()) % LEN)
                op = (1.0 if k == 0 else self.m5.get_value()) * self.g5.get_value()
                op *= min(1.0, max(0.0, (3.9 - x) / 0.5)) * min(1.0, max(0.0, (x - X0) / 0.5))
                if op < 0.02:
                    continue
                g.add(charge_c([x, WY, 0], 1, 0.55).set_opacity(op))
                if k % 2 == 0:
                    g.add(arrow([x, WY - 0.26, 0], [x, WY - 0.85, 0], FC, 4, 4).set_opacity(op))
                if k == 0 and self.m5.get_value() < 0.3:
                    g.add(arrow([x + 0.27, WY, 0], [x + 1.05, WY, 0], VIOLET, 4, 4).set_opacity(op))
            return g.set_z_index(5)

        self.car5 = always_redraw(carriers)
        self.car5.dyn = True
        self.add(self.car5)
        cur5 = VGroup(arrow([-5.9, WY + 0.8, 0], [-3.7, WY + 0.8, 0], GREEN, 6, 4), eq("I", size=M_M, colors={0: GREEN}).move_to([-4.8, WY + 1.2, 0]))
        self.wire5 = VGroup(wire, bdots, blab, cur5)
        self.play(FadeIn(self.wire5), self.g5.animate.set_value(1.0), run_time=1.2)
        cap1 = VGroup(txt("uma carga em movimento:", T_BODY), eq(r"\mathbf F", "=", "q", r"\mathbf v", r"\times", r"\mathbf B", size=34, colors={0: FC, 2: BLUE_L, 3: VIOLET, 5: MAG})
                      ).arrange(RIGHT, buff=0.3).move_to([0, -0.55, 0])
        self.play(FadeIn(cap1), run_time=0.7)
        self.hold(4.2)
        cap2 = VGroup(txt("muitas cargas: portadores positivos efetivos", T_NOTE, opacity=0.95),
                      txt("representação conveniente, não um metal real", 20, opacity=0.75)
                      ).arrange(DOWN, buff=0.15).move_to([0, -0.6, 0])
        self.play(self.m5.animate.set_value(1.0), RT(cap1, cap2), run_time=2.0, rate_func=smooth)
        self.cap2 = cap2
        self.hold(2.4)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B06 · continuidade
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def bloco_06_continuidade(self):
        self.b06_fluxo()
        self.b06_volume()
        self.b06_algebra()
        self.b06_estacionario()

    def b06_fluxo(self):
        """Redesign 2.5D (Manim): volume de controle em perspectiva oblíqua, J como fluxo verde contínuo e regular."""
        self.seg("G")
        self.limpa()

        def S_(fn):
            return fn()
        self.S_ = S_
        self.pf = self.clock("pf")
        self.run["pf"] = True
        self.gj, self.gbox, self.gq = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        S_PHYS = 0.11                        # segundos físicos por segundo de tela: a lei física dQ/dt = I_ent − I_sai é mantida internamente
        self.Iin, self.Iout, self.Q = ValueTracker(1.0), ValueTracker(1.0), ValueTracker(1.0)
        self.Q.add_updater(lambda m, dt: m.set_value(min(1.9, max(0.15, m.get_value() + (self.Iin.get_value() - self.Iout.get_value()) * S_PHYS * dt))))
        self.add(self.Q)
        W_, H_, D_ = 4.0, 2.6, 1.8
        self.BW = (W_, H_, D_)
        self.vsc, self.vcx, self.vcy = ValueTracker(1.0), ValueTracker(-5.6), ValueTracker(-1.2)
        EZ = np.array([0.42, 0.28, 0.0])

        def pm(x, y, z=0.0):
            s = self.vsc.get_value()
            return np.array([self.vcx.get_value() + s * (x + EZ[0] * z), self.vcy.get_value() + s * (y + EZ[1] * z), 0.0])

        self.pm = pm
        ROWS = [(0.45, 0.4), (1.3, 0.4), (2.15, 0.4), (0.45, 1.4), (1.3, 1.4), (2.15, 1.4)]
        XA, XB, GAP = -1.3, W_ + 1.3, 1.0

        def flow():
            g = VGroup()
            gj = self.gj.get_value()
            if gj < 0.02:
                return g
            ph = self.pf.get_value() * 0.9
            n = int((XB - XA) / GAP)
            L = n * GAP
            for (y, z) in ROWS:
                for k in range(n):
                    x = XA + (ph + k * GAP) % L
                    op = min(1.0, (x - XA) / 0.5, (XB - x) / 0.5)
                    if x < 0.0:
                        w = 2.0 + 4.0 * self.Iin.get_value()
                    elif x > W_:
                        w = 2.0 + 4.0 * self.Iout.get_value()
                    else:
                        t = x / W_
                        w = 2.0 + 4.0 * ((1 - t) * self.Iin.get_value() + t * self.Iout.get_value())
                    g.add(arrow(pm(x, y, z), pm(x + 0.55, y, z), GREEN, w, 5, tip=0.16).set_opacity(0.95 * op * gj))
            return g

        self.jf = always_redraw(flow)
        self.jf.dyn = True
        EDGE = BLUE_L

        def faces():
            gb = self.gbox.get_value()
            g = VGroup()
            if gb < 0.02:
                return g
            fo = 0.05 + 0.13 * self.Q.get_value() / 1.9
            g.add(Polygon(pm(0, 0, 0), pm(W_, 0, 0), pm(W_, H_, 0), pm(0, H_, 0), stroke_width=2.5, color=EDGE).set_fill(BLUE, fo).set_stroke(EDGE, 2.5, 0.85 * gb).set_fill(BLUE, fo * gb))
            g.add(Polygon(pm(0, H_, 0), pm(W_, H_, 0), pm(W_, H_, D_), pm(0, H_, D_)).set_fill(BLUE, 0.8 * fo * gb).set_stroke(EDGE, 2.5, 0.85 * gb))
            g.add(Polygon(pm(W_, 0, 0), pm(W_, 0, D_), pm(W_, H_, D_), pm(W_, H_, 0)).set_fill(BLUE, 1.2 * fo * gb).set_stroke(EDGE, 2.5, 0.85 * gb))
            for a, b in (((0, 0, 0), (0, 0, D_)), ((0, 0, D_), (W_, 0, D_)), ((0, 0, D_), (0, H_, D_))):
                g.add(DashedLine(pm(*a), pm(*b), dash_length=0.1, color=EDGE, stroke_width=1.6).set_opacity(0.45 * gb))
            return g.set_z_index(2)

        self.vol = always_redraw(faces)
        self.vol.dyn = True
        rng = np.random.RandomState(11)
        NX, NY, NZ = 7, 4, 3
        pts = [(0.4 + (W_ - 0.8) * (i + 0.5 * rng.rand()) / NX * (NX / (NX - 0.5)), 0.35 + (H_ - 0.7) * (j + 0.4 * rng.rand()) / (NY - 0.6),
                0.3 + (D_ - 0.6) * (k + 0.3 * rng.rand()) / (NZ - 0.7)) for i in range(NX) for j in range(NY) for k in range(NZ)]
        order = rng.permutation(len(pts))

        def dots():
            g = VGroup()
            gq = self.gq.get_value()
            if gq < 0.02:
                return g
            n = len(pts) * self.Q.get_value() / 1.9
            s = self.vsc.get_value()
            for rank, idx in enumerate(order):
                op = min(1.0, max(0.0, n - rank)) * gq
                if op > 0.02:
                    x, y, z = pts[idx]
                    g.add(Dot(pm(x, y, z), radius=0.07 * s, color=BLUE_L).set_opacity(op * (1.0 - 0.35 * z / D_)))
            return g.set_z_index(3)

        self.qd = always_redraw(dots)
        self.qd.dyn = True
        self.add(self.jf)
        jl = eq(r"\mathbf J", size=M_L, colors={0: GREEN}).move_to([-6.2, 2.5, 0])
        self.play(self.gj.animate.set_value(1.0), FadeIn(jl), run_time=1.4)
        self.hold(1.6)
        # superfície S (plano em perspectiva), normal da e a "fatia" v dt que atravessa em dt
        xs = 2.0
        surf = S_(lambda: Polygon(pm(xs, 0.15, 0), pm(xs, 2.45, 0), pm(xs, 2.45, 1.75), pm(xs, 0.15, 1.75))
                             .set_fill(BLUE_L, 0.16).set_stroke(WHITE, 2.5, 0.9).set_z_index(4))
        da = S_(lambda: arrow(pm(xs, 1.3, 0.87), pm(xs + 0.95, 1.3, 0.87), WHITE, 6, 6))
        sl = S_(lambda: eqc("S", size=M_M).move_to(pm(xs - 0.35, 2.85, 0.5)))
        dal = S_(lambda: eqc(r"d\mathbf a", size=M_M).move_to(pm(xs + 1.25, 1.65, 0.87)))
        slab = S_(lambda: VGroup(Polygon(pm(xs - 0.9, 0.15, 0), pm(xs, 0.15, 0), pm(xs, 2.45, 0), pm(xs - 0.9, 2.45, 0)).set_fill(GREEN, 0.10).set_stroke(GREEN, 1.8, 0.7),
                                            Polygon(pm(xs - 0.9, 2.45, 0), pm(xs, 2.45, 0), pm(xs, 2.45, 1.75), pm(xs - 0.9, 2.45, 1.75)).set_fill(GREEN, 0.07).set_stroke(GREEN, 1.8, 0.5)).set_z_index(3))
        vdt = S_(lambda: eqc(r"v\,dt", size=M_M, colors={0: VIOLET}).move_to(pm(xs - 0.45, -0.45, 0)))
        self.add(surf, da, sl, dal)
        self.play(FadeIn(surf), FadeIn(da), FadeIn(sl), FadeIn(dal), run_time=1.0)
        self.add(slab, vdt)
        self.play(FadeIn(slab), FadeIn(vdt), run_time=0.8)
        e = eq(r"I", "=", r"\int_S", r"\mathbf J", r"\cdot", r"d\mathbf a", size=48, colors={0: GREEN, 3: GREEN}).move_to([4.2, 0.9, 0])
        t = txt("corrente = fluxo de J", T_BODY, opacity=0.95).move_to([4.2, -0.3, 0])
        pn = panel(VGroup(e, t), pad=0.3, op=0.45)
        self.play(FadeIn(pn), FadeIn(e, shift=0.1 * DOWN), FadeIn(t), run_time=1.0)
        self.hold(3.4)
        self.fl = (surf, da, sl, dal, slab, vdt, e, t, jl, pn)

    def b06_volume(self):
        W_, H_, D_ = self.BW
        pm = self.pm
        S_ = self.S_
        # a superfície S vira a fronteira de um volume: as caixas se cruzam sem tela vazia; o fluxo segue vivo
        self.add(self.vol, self.qd)
        self.play(*[FadeOut(m) for m in self.fl], self.gbox.animate.set_value(1.0), self.gq.animate.set_value(1.0), run_time=1.8)
        l_v = S_(lambda: halo(self.lab(r"V", "volume de controle").move_to(pm(0.6, H_ + 0.55, D_) + np.array([0.6, 0.0, 0.0]))))
        l_dv = S_(lambda: halo(self.lab(r"\partial V", "fronteira").move_to(pm(W_ - 0.4, H_ + 0.55, D_) + np.array([0.3, 0.0, 0.0]))))
        l_q = S_(lambda: halo(self.lab(r"Q_{\mathrm{int}}", "carga contida", color=BLUE_L).move_to(pm(W_ / 2, -0.55, 0))))
        l_ji = S_(lambda: halo(self.lab(r"\mathbf J", "entra", color=GREEN).move_to(pm(-0.95, 2.95, 0))))
        l_jo = S_(lambda: halo(self.lab(r"\mathbf J", "sai", color=GREEN).move_to(pm(W_ + 1.0, 2.95, 0))))
        for m in (l_v, l_dv, l_q, l_ji, l_jo):
            m.dyn = True
        self.add(l_v)
        self.play(FadeIn(l_v), run_time=0.8)
        self.add(l_dv)
        self.play(Indicate(self.vol, color=BLUE_L, scale_factor=1.02), FadeIn(l_dv), run_time=1.0)
        self.hold(0.6)
        self.add(l_q)
        self.play(FadeIn(l_q), run_time=0.8)
        self.hold(0.8)
        self.add(l_ji, l_jo)
        self.play(FadeIn(l_ji), FadeIn(l_jo), run_time=0.8)
        self.hold(1.0)
        # balanço: frase curta → símbolos
        ST, SZs = [0.0, -3.0, 0], 40
        words = txt("variação = entra − sai", T_BODY, opacity=0.95).move_to(ST)
        self.play(FadeIn(words, shift=0.1 * UP), run_time=0.8)
        self.hold(1.4)
        root_, new_ = self.build(["dQdt", "=", "Ient", "minus", "Isai"], SZs)
        root_.move_to(ST)
        self.play(RT(words, VGroup(*new_.values())), run_time=1.4)      # a frase vira a equação
        self.cur = new_

        def readout(sym, tr, y, unit_tex, col=WHITE):
            l = eq(sym, size=M_M, colors={0: col}).move_to([4.1, y, 0])
            n = DecimalNumber(1.0, num_decimal_places=2, font_size=M_M, color=col)
            n.add_updater(lambda m: m.set_value(tr.get_value()).next_to(l, RIGHT, buff=0.2))
            u = eq(unit_tex, size=M_M)
            n.next_to(l, RIGHT, buff=0.2)
            u.next_to(n, RIGHT, buff=0.12)
            u.add_updater(lambda m: m.next_to(n, RIGHT, buff=0.12))
            return VGroup(l, n, u)

        rate = ValueTracker(0.0)
        rate.add_updater(lambda m: m.set_value(self.Iin.get_value() - self.Iout.get_value()))
        self.add(rate)
        self.reads = VGroup(readout(r"I_{\mathrm{ent}}=", self.Iin, 2.2, r"\mathrm{A}", GREEN), readout(r"I_{\mathrm{sai}}=", self.Iout, 1.5, r"\mathrm{A}", GREEN),
                            readout(r"\frac{dQ_{\mathrm{int}}}{dt}=", rate, 0.5, r"\mathrm{A}", BLUE_L),
                            readout(r"Q_{\mathrm{int}}=", self.Q, -0.5, r"\mathrm{C}", BLUE_L))
        rp = panel(self.reads, pad=0.45, op=0.4)
        self.reads_p = rp
        self.play(FadeIn(rp), FadeIn(self.reads), run_time=0.8)
        self.hold(1.6)
        cap = eq(r"I_{\mathrm{sai}}>I_{\mathrm{ent}}", r"\Rightarrow", r"Q_{\mathrm{int}}\downarrow", size=34, colors={0: GREEN, 2: BLUE_L}).move_to([-1.4, -2.2, 0])
        self.play(self.Iout.animate.set_value(2.0), FadeIn(cap), run_time=1.5)
        self.hold(5.2)
        self.play(self.Iout.animate.set_value(1.0), FadeOut(cap), run_time=1.2)
        self.hold(0.8)
        cap2 = eq(r"I_{\mathrm{ent}}>I_{\mathrm{sai}}", r"\Rightarrow", r"Q_{\mathrm{int}}\uparrow", size=34, colors={0: GREEN, 2: BLUE_L}).move_to([-1.4, -2.2, 0])
        self.play(self.Iin.animate.set_value(2.0), FadeIn(cap2), run_time=1.5)
        self.hold(5.2)
        self.play(self.Iin.animate.set_value(1.0), FadeOut(cap2), run_time=1.2)
        self.hold(0.6)
        # o sinal negativo nasce das normais externas
        self.play(FadeOut(self.reads), FadeOut(rp), run_time=0.6)
        nL = S_(lambda: arrow(pm(0, 1.3, 0.87), pm(0, 1.3, 0.87) + np.array([-0.8, 0.0, 0.0]), WHITE, 5, 6))
        nR = S_(lambda: arrow(pm(W_, 1.3, 0.87), pm(W_, 1.3, 0.87) + np.array([0.8, 0.0, 0.0]), WHITE, 5, 6))
        nl = S_(lambda: halo(eqc(r"\hat{\mathbf n}", size=M_M).move_to(pm(0, 1.3, 0.87) + np.array([-0.4, 0.45, 0.0]))))
        nr = S_(lambda: halo(eqc(r"\hat{\mathbf n}", size=M_M).move_to(pm(W_, 1.3, 0.87) + np.array([0.4, 0.45, 0.0]))))
        capn = VGroup(eq(r"\hat{\mathbf n}", size=32), txt("para fora de V", T_NOTE, opacity=0.95)).arrange(RIGHT, buff=0.15).move_to([-1.4, -2.2, 0])
        sL = S_(lambda: eqc(r"\mathbf J\cdot\hat{\mathbf n}<0", size=30, colors={0: GREEN}).move_to(pm(-0.2, -0.05, 0) + np.array([-0.5, -0.1, 0.0])))
        sR = S_(lambda: eqc(r"\mathbf J\cdot\hat{\mathbf n}>0", size=30, colors={0: GREEN}).move_to(pm(W_ + 0.2, -0.05, 0) + np.array([1.0, -0.1, 0.0])))
        for m in (nL, nR, nl, nr, sL, sR):
            m.dyn = True
        self.add(nL, nR, nl, nr)
        self.play(FadeIn(nL), FadeIn(nR), FadeIn(nl), FadeIn(nr), FadeIn(capn), run_time=1.0)
        self.hold(1.2)
        self.add(sL)
        self.play(FadeIn(sL), run_time=0.7)
        self.hold(1.0)
        self.add(sR)
        self.play(FadeIn(sR), run_time=0.7)
        self.hold(1.4)
        self.play(FadeOut(capn), run_time=0.3)
        capf = txt("fluxo líquido para fora:", T_NOTE, opacity=0.95).move_to([-1.4, -2.2, 0])
        self.play(FadeIn(capf), run_time=0.5)
        self.morph(["oint", "Jv", "dot", "da", "=", "Isai", "minus", "Ient"], SZs, ST, run=1.4)
        self.hold(2.0)
        self.play(FadeOut(capf), run_time=0.3)
        self.morph(["dQdt", "=", "neg", "oint", "Jv", "dot", "da"], SZs, ST, run=1.6)
        bx = box(VGroup(*self.cur.values()))
        self.play(FadeIn(bx), run_time=0.5)
        self.hold(2.6)
        self.play(FadeOut(bx), *[FadeOut(m) for m in self.cur.values()], run_time=0.6)
        self.cur = {}
        self.vlabs = [l_v, l_dv, l_q, l_ji, l_jo, nL, nR, nl, nr, sL, sR]

    def b06_algebra(self):
        """Álgebra da continuidade com o volume VIVO à esquerda (J verde fluindo, carga interna visível) e as equações à direita."""
        RX = 3.95
        AT, SZ = [RX, -0.1, 0], 38
        W_, H_, D_ = self.BW
        pm = self.pm
        S_ = self.S_
        self.Iin.set_value(1.0)
        self.Iout.set_value(1.0)
        # só ficam o volume, o fluxo e a carga interna; rótulos e normais saem
        self.play(*[FadeOut(m) for m in self.vlabs], run_time=0.8)
        self.remove(*self.vlabs)
        cap = VGroup(eq(r"\rho", size=34, colors={0: BLUE_L}), txt("carga / volume", T_NOTE, opacity=0.95)).arrange(RIGHT, buff=0.2).move_to([RX, 2.4, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.morph(["Qi", "=", "intV", "rho", "dtau"], SZ + 6, AT, first=True)
        n1 = txt("soma da carga em todo o volume", T_NOTE, opacity=0.9).move_to([RX, -1.6, 0])
        self.play(FadeIn(n1), run_time=0.6)
        self.hold(2.0)
        self.play(FadeOut(cap), FadeOut(n1), run_time=0.4)
        cap = VGroup(txt("V fixo: só", T_NOTE, opacity=0.95), eq(r"\rho", size=30, colors={0: BLUE_L}), txt("varia com t", T_NOTE, opacity=0.95)).arrange(RIGHT, buff=0.14).move_to([RX, 2.4, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.hold(1.2)
        self.play(FadeOut(cap), run_time=0.3)
        cap = txt("forma integral", T_BODY, opacity=0.95).move_to([RX, 2.4, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.morph(["ddt", "intV", "rho", "dtau", "=", "neg", "oint", "Jv", "dot", "da"], SZ, AT, alias={"Qi": ["ddt"]}, run=1.6)
        # as duas metades acendem no desenho: o que está dentro e o que atravessa a fronteira
        hi_in = S_(lambda: Polygon(pm(0, 0, 0), pm(W_, 0, 0), pm(W_, H_, 0), pm(0, H_, 0)).set_fill(BLUE_L, 0.0).set_stroke(BLUE_L, 5, 0.9).set_z_index(6))
        hi_l = S_(lambda: Polygon(pm(0, 0, 0), pm(0, 0, D_), pm(0, H_, D_), pm(0, H_, 0)).set_fill(GREEN, 0.28).set_stroke(GREEN, 3, 0.9).set_z_index(6))
        hi_r = S_(lambda: Polygon(pm(W_, 0, 0), pm(W_, 0, D_), pm(W_, H_, D_), pm(W_, H_, 0)).set_fill(GREEN, 0.28).set_stroke(GREEN, 3, 0.9).set_z_index(6))
        for m in (hi_in, hi_l, hi_r):
            m.dyn = True
        nn = VGroup(txt("dentro de V", 20, opacity=0.9), VGroup(txt("pela fronteira", 20, opacity=0.9), eq(r"\partial V", size=26)).arrange(RIGHT, buff=0.12)
                    ).arrange(RIGHT, buff=1.4).move_to([RX, -1.6, 0])
        self.add(hi_l, hi_r)
        self.play(FadeIn(hi_l), FadeIn(hi_r), FadeIn(nn), run_time=0.8)
        bx = box(VGroup(*self.cur.values()))
        self.play(FadeIn(bx), run_time=0.5)
        self.hold(2.0)
        self.play(FadeOut(bx), FadeOut(cap), FadeOut(nn), run_time=0.4)
        cap = txt("teorema da divergência", T_BODY, opacity=0.95).move_to([RX, 2.4, 0])
        self.play(FadeIn(cap), run_time=0.5)
        # o que atravessa a fronteira vira o que acontece localmente: células com setas saindo, no interior
        cells = VGroup()
        for (cx, cy, cz) in ((1.2, 0.9, 0.9), (2.0, 1.6, 0.9), (2.8, 0.9, 0.9)):
            c0 = pm(cx, cy, cz)
            # célula com o MESMO fluxo entrando e saindo (divergência nula: coerente com o fluxo uniforme mostrado)
            cells.add(Polygon(c0 + np.array([-0.2, -0.2, 0.0]), c0 + np.array([0.2, -0.2, 0.0]), c0 + np.array([0.2, 0.2, 0.0]),
                              c0 + np.array([-0.2, 0.2, 0.0]), color=GREEN, stroke_width=2).set_fill(GREEN, 0.12).set_z_index(7))
            cells.add(arrow(c0 + np.array([-0.62, 0.0, 0.0]), c0 + np.array([-0.24, 0.0, 0.0]), GREEN, 3, 7, tip=0.1),
                      arrow(c0 + np.array([0.24, 0.0, 0.0]), c0 + np.array([0.62, 0.0, 0.0]), GREEN, 3, 7, tip=0.1))
        dvl = halo(eq(r"\nabla\cdot\mathbf J", size=M_M, colors={0: GREEN}).move_to(pm(2.0, 2.2, 0.9) + np.array([0.0, 0.5, 0.0])).set_z_index(8))
        self.morph(["ddt", "intV", "rho", "dtau", "=", "neg", "intV@d", "div", "dtau@d"], SZ, AT,
                   alias={"oint": ["intV@d"], "Jv": ["div"], "da": ["dtau@d"]}, run=1.7)
        self.play(FadeOut(hi_l), FadeOut(hi_r), FadeIn(cells), FadeIn(dvl), run_time=1.2)
        self.hold(1.6)
        self.morph(["intV", "drho", "dtau", "=", "neg", "intV@d", "div", "dtau@d"], SZ, AT, alias={"rho": ["drho"]}, run=1.5)
        self.hold(1.4)
        self.play(FadeOut(cap), run_time=0.3)
        cap = txt("V é qualquer", T_BODY, opacity=0.95).move_to([RX, 2.4, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.morph(["intV", "(", "drho", "plus", "div", ")", "dtau", "=", "0"], SZ, AT, run=1.6)
        self.hold(2.0)
        self.play(FadeOut(cap), run_time=0.3)
        self.morph(["div", "=", "neg", "drho"], 52, AT, run=1.6)
        bx = box(VGroup(*self.cur.values()))
        nm_c = nome("Equação da continuidade", "conservação da carga", pos=(RX, 1.1, 0))
        self.play(FadeIn(bx), FadeIn(nm_c), run_time=0.5)
        self.hold(2.6)
        self.play(FadeOut(bx), FadeOut(nm_c), run_time=0.4)
        cap = txt("magnetostática", T_BODY, opacity=0.95).move_to([RX, 2.4, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.morph(["drho", "=", "0"], 52, AT, run=1.2)
        self.hold(1.4)
        self.morph(["div", "=", "0"], 58, AT, alias={"drho": ["div"]}, run=1.4)
        bx = box(VGroup(*self.cur.values()))
        self.play(FadeIn(bx), run_time=0.6)
        self.hold(2.0)
        self.play(FadeOut(cap), FadeOut(bx), FadeOut(cells), FadeOut(dvl), *[FadeOut(m) for m in self.cur.values()], run_time=0.7)
        self.remove(hi_in, hi_l, hi_r)
        self.cur = {}

    def b06_estacionario(self):
        """Corrente estacionária não é corrente nula: entra e sai à mesma taxa, e nenhuma carga se acumula."""
        RX = 4.2
        e1 = VGroup(eq(r"\mathbf J", r"\neq 0", size=56, colors={0: GREEN}), txt("a corrente existe", T_BODY, opacity=0.95)).arrange(DOWN, buff=0.25).move_to([RX, 1.5, 0])
        e2 = VGroup(eq(r"\nabla\cdot\mathbf J", "=0", size=56, colors={0: GREEN}), txt("nenhuma carga se acumula", T_BODY, opacity=0.95)).arrange(DOWN, buff=0.35).move_to([RX, -1.0, 0])
        p1, p2 = panel(e1, pad=0.3, op=0.45), panel(e2, pad=0.3, op=0.45)
        self.play(FadeIn(p1), FadeIn(e1, shift=0.1 * DOWN), run_time=1.0)
        self.hold(1.6)
        self.play(FadeIn(p2), FadeIn(e2, shift=0.1 * DOWN), run_time=1.0)
        self.hold(4.0)
        msg = txt("corrente estacionária: não é nula", T_BODY, opacity=0.95).move_to([-1.4, -2.9, 0])
        self.play(FadeIn(msg), run_time=0.8)
        self.hold(3.0)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B07 · Thomson: seletor de velocidades (aplicação direta de Lorentz)
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def ap(self, x, y):
        """Coordenada local do aparato → tela (o aparato pode mudar de escala/posição ao abrir o SPLIT)."""
        s = self.asc.get_value()
        return np.array([self.aox.get_value() + s * x, self.aoy.get_value() + s * y, 0.0])

    def beam_y(self, x):
        """Deflexão QUALITATIVA do feixe na região de campos cruzados (mesma fonte de estado: v, sinal de q)."""
        v, qs = self.vth.get_value(), self.qs7.get_value()
        d = qs * DMAX * math.tanh(0.8 * (E7 - v * B7) / max(v, 0.25) ** 2)       # d = 0 exatamente em v = E/B
        if x <= -1.5:
            return 0.0
        if x <= 1.5:
            u = (x + 1.5) / 3.0
            return d * u * u
        return d + (2 * d / 3.0) * (x - 1.5)

    def beam_len(self):
        return 7.8 if self.mode7 == "cross" else 2.5 + math.pi * R8          # reta + SEMIcircunferência (sai pela borda de entrada)

    def beam_pos(self, s_):
        if self.mode7 == "cross":
            x = -4.0 + s_
            return np.array([x, self.beam_y(x)])
        if s_ <= 2.5:                                        # reta até a região só com B
            return np.array([-4.0 + s_, 0.0])
        th = (s_ - 2.5) / R8                                 # arco circular: raio R8, centro do lado da força (F_B = q v×B)
        sg = self.qs7.get_value()
        return np.array([-1.5 + R8 * math.sin(th), -sg * R8 * (1 - math.cos(th))])

    def mk_beam(self):
        def trail():
            S = self.beam_len()
            pts = [self.ap(*self.beam_pos(S * i / 110.0)) for i in range(111)]
            m = VMobject(color=BLUE_L, stroke_width=3.5).set_stroke(opacity=0.9)
            m.set_points_as_corners(pts)
            return m.set_z_index(3)

        def particle():
            S = self.beam_len()
            sp = (self.ph7.get_value() * 1.7) % S
            op = min(1.0, max(0.0, min(sp, S - sp) / 0.4))
            return charge_c(self.ap(*self.beam_pos(sp)), self.qs7.get_value(), 0.55 * max(0.8, self.asc.get_value())).set_opacity(op)

        return always_redraw(trail), always_redraw(particle)

    def b07_montar_aparato(self):
        E7_, B7_ = E7, B7
        apx = self.ap

        def plates():
            g = VGroup()
            for y, sg in ((1.2, "−"), (-1.2, "+")):
                g.add(Polygon(apx(-1.5, y), apx(1.5, y), apx(1.5, y + (0.12 if y > 0 else -0.12)), apx(-1.5, y + (0.12 if y > 0 else -0.12)),
                              color=WHITE, stroke_width=2, fill_color=WHITE, fill_opacity=0.12))
            for x in (-1.0, 0.0, 1.0):
                g.add(eqc("-", size=26, colors={0: CYAN}).move_to(apx(x, 1.45)), eqc("+", size=26, colors={0: CYAN}).move_to(apx(x, -1.45)))
            return g.set_opacity(self.pop.get_value())

        def efield():
            g = VGroup()
            for x in (-1.0, 0.0, 1.0):
                g.add(arrow(apx(x, -0.85), apx(x, 0.85), CYAN, 3, 2, tip=0.18).set_opacity(0.8 * self.eop.get_value()))
            return g

        def bfield():
            g = VGroup()
            x0, x1 = (-1.3, 1.3) if self.mode7 == "cross" else (-1.2, 0.4)     # B08: símbolos só DENTRO da região magnética
            for x in np.arange(x0, x1 + 0.01, 0.65 if self.mode7 == "cross" else 0.6):
                for y in ((-0.6, 0.6) if self.mode7 == "cross" else tuple(np.linspace(-2.3, 2.3, 7))):
                    c = apx(x, y)
                    g.add(Circle(radius=0.075 * self.asc.get_value(), color=MAG, stroke_width=2).set_opacity(0.45).move_to(c),
                          Dot(c, radius=0.025, color=MAG).set_opacity(0.45))
            return g

        def detector():
            return DashedLine(apx(3.8, -1.7), apx(3.8, 1.7), dash_length=0.1, color=WHITE, stroke_width=2).set_opacity(0.6 * self.pop.get_value())

        self.plates, self.efield, self.bfield, self.detec = (always_redraw(plates), always_redraw(efield),
                                                              always_redraw(bfield), always_redraw(detector))
        self.beam_t, self.beam_p = self.mk_beam()
        self.ap_mobs = [self.plates, self.efield, self.bfield, self.detec, self.beam_t, self.beam_p]

    def bloco_07_thomson(self):
        self.seg("H")
        self.cores_novas = True
        self.limpa(0.8)
        # estado do aparato: UMA variável física v controla gráfico, valor de F_y/q e deflexão do feixe
        self.vth, self.qs7 = ValueTracker(0.6), ValueTracker(1.0)
        self.asc, self.aox, self.aoy = ValueTracker(1.0), ValueTracker(-3.0), ValueTracker(0.35)   # aparato ~58% esquerdo, fixo em todo o B07/B08
        self.pop, self.eop = ValueTracker(0.0), ValueTracker(0.0)          # opacidade das placas / das setas de E
        self.mode7 = "cross"
        self.ph7 = ValueTracker(0.0)
        self.ph7.add_updater(lambda m, dt: m.increment_value(dt * self.vth.get_value() / (E7 / B7)))     # avanço do pulso ∝ v (mesma variável do gráfico)
        self.add(self.ph7)
        self.b07_montar_aparato()
        self.b07_aparato()
        self.b07_forcas()
        self.b07_grafico()
        self.b07_regimes()
        self.b07_sinal()

    def b07_aparato(self):
        """O aparato nasce antes de qualquer equação: feixe, v, região de E, região de B, eixos."""
        self.add(*self.ap_mobs)
        self.play(FadeIn(self.beam_t), FadeIn(self.beam_p), FadeIn(self.detec), run_time=1.2)
        # eixos e v
        triad = VGroup(arrow(self.ap(-3.9, 1.3), self.ap(-3.3, 1.3), WHITE, 3, 2, tip=0.14), arrow(self.ap(-3.9, 1.3), self.ap(-3.9, 1.9), WHITE, 3, 2, tip=0.14),
                       Circle(radius=0.07, color=MAG, stroke_width=2).move_to(self.ap(-3.9, 1.3)),
                       eq("x", size=28).move_to(self.ap(-3.15, 1.3)), eq("y", size=28).move_to(self.ap(-3.9, 2.05)),
                       eq("z", size=28).move_to(self.ap(-4.2, 1.3)))
        vlab = eq(r"\mathbf v", "=", "v", r"\hat{\mathbf x}", size=36, colors={0: VIOLET, 2: VIOLET}).move_to(self.ap(-3.0, -0.55))
        varr = arrow(self.ap(-3.5, 0.0), self.ap(-2.6, 0.0), VIOLET, 5, 5)
        self.play(FadeIn(triad), FadeIn(varr), FadeIn(vlab), run_time=1.0)
        self.hold(1.2)
        # região de E (placas) e região de B (⊙)
        elab = eq(r"\mathbf E", "=", "E", r"\hat{\mathbf y}", size=36, colors={0: CYAN, 2: CYAN}).move_to(self.ap(0.0, 1.75))
        self.play(self.pop.animate.set_value(1.0), self.eop.animate.set_value(1.0), FadeIn(elab), run_time=1.2)
        self.hold(1.0)
        blab = eq(r"\mathbf B", "=", "B", r"\hat{\mathbf z}", size=36, colors={0: MAG, 2: MAG}).move_to(self.ap(0.0, -1.75))
        self.play(FadeIn(blab), run_time=0.8)
        self.hold(1.4)
        self.leg7 = VGroup(triad, vlab, varr, elab, blab)

    def b07_forcas(self):
        """Forças em sequência, cada uma com seu rótulo e líder: F_E = qE (+y), depois F_B = q v×B (−y), depois a resultante F_y."""
        RX = 4.3

        def probe():
            return self.ap(0.0, self.beam_y(0.0))

        def lead(p, q_, color):
            return Line(p, q_, color=color, stroke_width=1.6).set_opacity(0.8)

        def fE():
            q = self.qs7.get_value()
            p = probe()
            tip = p + np.array([0.0, 0.75 * E7 * q * self.asc.get_value(), 0.0])
            lab = p + np.array([2.0 * self.asc.get_value(), 0.75 * E7 * q * self.asc.get_value(), 0.0])
            return VGroup(arrow(p, tip, FC, 5, 6), lead(tip + np.array([0.08, 0.0, 0.0]), lab + np.array([-0.45, 0.0, 0.0]), FC),
                          halo(eqc(r"\mathbf F_E", size=M_M, colors={0: FC}).move_to(lab))).set_opacity(self.foE.get_value())

        def fB():
            q = self.qs7.get_value()
            p = probe()
            L_ = -0.75 * self.vth.get_value() * B7 * q * self.asc.get_value()
            tip = p + np.array([0.0, L_, 0.0])
            lab = p + np.array([2.0 * self.asc.get_value(), L_ - 0.25 * np.sign(L_ if abs(L_) > 1e-3 else 1.0), 0.0])
            return VGroup(arrow(p, tip, FC, 5, 6), lead(tip + np.array([0.08, 0.0, 0.0]), lab + np.array([-0.45, 0.0, 0.0]), FC),
                          halo(eqc(r"\mathbf F_B", size=M_M, colors={0: FC}).move_to(lab))).set_opacity(self.foB.get_value())

        def fN():
            q = self.qs7.get_value()
            p = self.ap(-1.95, 0.0)                    # resultante fora das placas (à esquerda), sem cruzar as setas de E
            L_ = 0.75 * q * (E7 - self.vth.get_value() * B7) * self.asc.get_value()
            if abs(L_) < 0.08:
                return VGroup()
            tip = p + np.array([0.0, L_, 0.0])
            return VGroup(arrow(p, tip, WHITE, 8, 7),
                          halo(eqc(r"F_y", size=M_M, colors={0: FC}).move_to(tip + np.array([-0.5, 0.0, 0.0])))).set_opacity(self.foN.get_value())

        self.fop = ValueTracker(0.0)
        self.foE, self.foB, self.foN = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.fE_m, self.fB_m, self.fN_m = always_redraw(fE), always_redraw(fB), always_redraw(fN)
        self.add(self.fE_m, self.fB_m, self.fN_m)
        ST, SZ = [RX, 1.5, 0], 40
        # 1) F_E
        self.play(self.foE.animate.set_value(1.0), run_time=0.8)
        self.morph(["FE", "=", "qs", "Ev"], SZ, ST, first=True, run=1.0)
        self.hold(1.6)
        # 2) F_B
        self.play(self.foB.animate.set_value(1.0), run_time=0.8)
        self.morph(["FB", "=", "qs", "vv", "times", "Bv"], SZ, ST, run=1.2)
        self.hold(1.2)
        # produto vetorial em um cartão limpo (região livre, abaixo da equação), item a item
        rows = [eq(r"\mathbf v", r"\to", r"+\hat{\mathbf x}", size=32, colors={0: VIOLET}), eq(r"\mathbf B", r"\to", r"+\hat{\mathbf z}", size=32, colors={0: MAG}),
                eq(r"\mathbf v\times\mathbf B", r"\to", r"-\hat{\mathbf y}", size=32, colors={0: VIOLET, 2: FC})]
        card = VGroup(*rows).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([RX, -1.4, 0])
        cp = panel(card, pad=0.32, op=0.55)
        self.play(FadeIn(cp), FadeIn(rows[0]), run_time=0.7)
        self.play(FadeIn(rows[1]), run_time=0.7)
        self.play(FadeIn(rows[2]), run_time=0.7)
        self.hold(1.4)
        self.morph(["FB", "=", "minus", "qs", "vs", "Bs", "yh"], SZ, ST, run=1.3)
        self.hold(1.4)
        self.play(FadeOut(card), FadeOut(cp), run_time=0.5)
        # 3) resultante
        self.play(self.foN.animate.set_value(1.0), run_time=0.8)
        self.morph(["Fy", "=", "qs", "(", "Es", "minus", "vs", "Bs", ")"], SZ, ST, run=1.5)
        self.hold(1.6)
        self.morph(["Fyq", "=", "Es", "minus", "vs", "Bs"], SZ, ST, run=1.3)
        bx = box(VGroup(*self.cur.values()))
        self.play(FadeIn(bx), run_time=0.5)
        self.hold(1.6)
        self.play(FadeOut(bx), *[FadeOut(m) for m in self.cur.values()], run_time=0.7)
        self.cur = {}
        self.fop_keep = True

    def b07_grafico(self):
        """Aparato à esquerda (58%), gráfico de F_y/q = E − vB à direita (42%); mesma variável v."""
        self.play(FadeOut(self.leg7), FadeOut(self.fE_m), FadeOut(self.fB_m), FadeOut(self.fN_m), run_time=1.0)
        self.remove(self.fE_m, self.fB_m, self.fN_m)
        axes = Axes(x_range=[0, 2.4, 0.4], y_range=[-1.2, 1.2, 0.6], x_length=5.2, y_length=3.2, tips=False,
                    axis_config={"color": WHITE, "stroke_width": 2, "include_ticks": False}).move_to([4.3, 0.0, 0])
        xl = eq("v", size=34, colors={0: VIOLET}).next_to(axes.x_axis.get_end(), DOWN, buff=0.15)
        yl = eq(r"F_y/q", size=34, colors={0: FC}).next_to(axes.y_axis.get_end(), UP, buff=0.12)
        line = axes.plot(lambda v: E7 - B7 * v, x_range=[0, 2.4], color=FC, stroke_width=4)
        self.axes7 = axes

        def gdot():
            v = self.vth.get_value()
            p = axes.c2p(v, E7 - B7 * v)
            return VGroup(DashedLine(axes.c2p(v, 0), p, dash_length=0.08, color=WHITE, stroke_width=1.5).set_opacity(0.7),
                          Dot(p, radius=0.11, color=FC).set_stroke(WHITE, 2), Dot(axes.c2p(v, 0), radius=0.05, color=VIOLET))

        self.gdot = always_redraw(gdot)
        self.graf = VGroup(axes, xl, yl, line)
        self.play(FadeIn(self.graf), FadeIn(self.gdot), run_time=1.2)
        eqg = eq(r"F_y/q", "=", "E", "-", "vB", size=40, colors={0: FC, 2: CYAN, 4: VIOLET}).move_to([4.3, -2.35, 0])
        self.esq7 = txt("trajetórias esquemáticas", 20, opacity=0.5).move_to([-3.0, -3.25, 0])
        self.play(FadeIn(eqg), FadeIn(self.esq7), run_time=0.7)
        self.eqg = eqg
        self.hold(1.0)

    def b07_regimes(self):
        """Mesma variável v: v < v_sel, v > v_sel, v = v_sel. A legenda de equilíbrio só existe quando v = v_sel."""
        vsel = E7 / B7
        cap = None
        RX = 4.3

        def show(rows):
            nonlocal cap
            new = VGroup(*[VGroup(*r).arrange(RIGHT, buff=0.18) for r in rows]).arrange(DOWN, buff=0.1).move_to([RX, 2.85, 0])
            self.play(FadeIn(new), run_time=0.6)
            cap = new

        def clear():
            nonlocal cap
            if cap is not None:
                self.play(FadeOut(cap), run_time=0.3)
                cap = None

        VS = r"v_{\mathrm{sel}}"
        self.play(self.vth.animate.set_value(0.5), run_time=1.2)
        show([[eq(r"v\ \text{(atual)}", "<", VS, size=30, colors={}), eq(r"\Rightarrow\ F_y/q>0", size=30, colors={})],
              [txt("força líquida para +y (q > 0)", 20, opacity=0.9)]])
        self.hold(3.0)
        clear()
        self.play(self.vth.animate.set_value(1.9), run_time=3.0, rate_func=smooth)
        show([[eq(r"v\ \text{(atual)}", ">", VS, size=30, colors={}), eq(r"\Rightarrow\ F_y/q<0", size=30, colors={})],
              [txt("força líquida para −y (q > 0)", 20, opacity=0.9)]])
        self.hold(3.0)
        clear()
        self.play(self.vth.animate.set_value(vsel), run_time=2.6, rate_func=smooth)
        show([[eq("v", "=", VS, size=30, colors={}), eq(r"\Rightarrow\ F_y/q=0", size=30, colors={})],
              [txt("feixe reto: velocidade selecionada", 20, opacity=0.9)]])
        pr = self.axes7.c2p(vsel, 0)
        root = Dot(pr, radius=0.08, color=CYAN).set_z_index(5)
        rl = eq(VS, "=", r"\frac EB", size=34, colors={0: VIOLET, 2: CYAN}).move_to([6.05, 1.15, 0])     # callout externo ao contorno do gráfico
        ldr = Line(rl.get_bottom() + np.array([-0.3, -0.12, 0.0]), pr + np.array([0.1, 0.08, 0.0]), color=CYAN, stroke_width=1.8).set_opacity(0.9)
        self.play(FadeIn(root), FadeIn(rl), FadeIn(ldr), Flash(pr, color=CYAN, flash_radius=0.4, line_length=0.12), run_time=1.0)
        self.hold(1.4)
        res = txt("Condição de seleção de velocidades", 22, opacity=1.0).move_to([RX, -3.0, 0])
        bx = box(rl)
        self.play(FadeIn(bx), FadeIn(res), run_time=0.8)
        self.hold(2.4)
        self.cap7, self.root7 = cap, VGroup(root, rl, bx, res, ldr)

    def b07_sinal(self):
        """q → −q com a MESMA velocidade (v < v_sel): a força física inverte; a raiz de E − vB = 0 não muda."""
        vsel = E7 / B7
        VS = r"v_{\mathrm{sel}}"
        RX = 4.3
        self.play(FadeOut(self.cap7), self.vth.animate.set_value(0.6), run_time=1.6, rate_func=smooth)

        def topcap(sinal):
            return VGroup(VGroup(eq(r"\text{mesma } v", "<", VS, size=28, colors={}),
                                 eq(r"\Rightarrow\ F_y/q>0", size=28, colors={})).arrange(RIGHT, buff=0.18),
                          txt("força líquida para %s" % sinal, 20, opacity=0.9)).arrange(DOWN, buff=0.1).move_to([RX, 2.85, 0])

        c1 = topcap("+y (q > 0)")
        self.play(FadeIn(c1), run_time=0.6)
        self.hold(1.6)
        capq = VGroup(eq(r"q", r"\to", "-q", size=34, colors={0: BLUE_L, 2: BLUE_L}), txt("a força inverte", 22)).arrange(RIGHT, buff=0.3).move_to([RX, -3.0, 0])
        self.play(FadeOut(self.root7[3]), run_time=0.4)
        self.qs7.set_value(-1.0)
        c2 = topcap("−y (q < 0)")
        self.play(Flash(self.ap(-1.5, 0.0), color=BLUE_L, flash_radius=0.5, line_length=0.14), FadeIn(capq), RT(c1, c2), run_time=0.9)
        self.hold(3.0)
        n2 = VGroup(eq(r"F_y/q", size=28, colors={0: FC}), txt("não depende do sinal de q", 20, opacity=0.9)).arrange(RIGHT, buff=0.15).move_to([RX, -2.35, 0])
        self.play(RT(self.eqg, n2), run_time=0.8)
        self.hold(2.0)
        self.play(FadeOut(c2), run_time=0.3)
        self.play(self.vth.animate.set_value(vsel), run_time=2.0, rate_func=smooth)
        n3 = VGroup(VGroup(eq("v", "=", VS, size=28, colors={}), eq(r"\Rightarrow\ F_y/q=0", size=28, colors={})).arrange(RIGHT, buff=0.18),
                    txt("reto para qualquer sinal de q", 20, opacity=0.9)).arrange(DOWN, buff=0.1).move_to([RX, 2.85, 0])
        self.play(FadeIn(n3), run_time=0.8)
        self.hold(1.2)
        self.qs7.set_value(1.0)                                # no v = v_sel os dois sinais passam retos
        self.hold(1.4)
        self.play(FadeOut(capq), FadeOut(n2), FadeOut(self.root7[0]), FadeOut(self.root7[1]), FadeOut(self.root7[2]), FadeOut(self.root7[4]), run_time=0.6)
        self.sel7 = (n3,)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B08 · curvatura e |q|/m
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def bloco_08_qm(self):
        self.seg("I")
        # o MESMO feixe selecionado (v = E/B): só E é desligado; a região passa a conter apenas B
        self.play(FadeOut(self.graf), FadeOut(self.gdot), FadeOut(self.sel7[0]), FadeOut(self.esq7), run_time=0.8)
        vsel_lab = eq(r"v", "=", r"\frac EB", size=40, colors={0: VIOLET, 2: CYAN}).move_to([4.3, 2.75, 0])
        self.play(FadeIn(vsel_lab), run_time=0.7)
        desl = VGroup(eq("E", "=", "0", size=34, colors={0: CYAN}), txt("só B, mesmo v", T_NOTE, opacity=0.95)).arrange(RIGHT, buff=0.3).move_to([4.3, 1.55, 0])
        breg = Polygon(self.ap(-1.5, -2.6), self.ap(0.6, -2.6), self.ap(0.6, 2.6), self.ap(-1.5, 2.6)).set_fill(MAG, 0.06).set_stroke(MAG, 1.8, 0.6)
        self.add(breg)
        self.play(self.eop.animate.set_value(0.0), self.pop.animate.set_value(0.0), FadeIn(desl), FadeIn(breg), run_time=1.2)
        self.mode7 = "arc"                           # só B: o feixe passa a descrever um arco circular
        self.hold(0.4)
        self.hold(3.4)

        # medir R no desenho antes da fórmula: centro, linha de raio e rótulo R formam UM estado derivado do sinal de q
        def rline():
            sg = self.qs7.get_value()
            c = self.ap(-1.5, -sg * R8)
            return VGroup(DashedLine(c, self.ap(-1.5 + R8, -sg * R8), dash_length=0.1, color=WHITE, stroke_width=2.2),
                          Dot(c, radius=0.06, color=WHITE))

        rl = always_redraw(rline)
        rlab = eq("R", size=M_M)
        rlab.add_updater(lambda m: m.move_to(self.ap(-1.5 + 0.5 * R8, -self.qs7.get_value() * R8 + 0.35)))
        rlab.move_to(self.ap(-1.5 + 0.5 * R8, -R8 + 0.35))
        self.play(FadeOut(desl), FadeIn(rl), FadeIn(rlab), run_time=1.0)
        self.hold(2.0)
        self.rlab8 = VGroup(rl, rlab, vsel_lab)
        self.b08_resultado()
        self.b08_leituras()

    def b08_resultado(self):
        AT, SZ = [4.3, -0.7, 0], 44
        cap = txt("na região só com B:", T_NOTE, opacity=0.95).move_to([4.3, 0.9, 0])
        self.play(FadeIn(cap), run_time=0.5)
        self.morph(["q", "vs@L", "B", "=", ("f", ["m", "vs@a", "vs@b"], ["R"], "b1")], SZ, AT, first=True, run=1.2)
        self.hold(1.4)
        lines = self.strike(self.cur["vs@L"], self.cur["vs@a"])
        c = self.cur
        self.play(FadeOut(c["vs@L"]), FadeOut(c["vs@a"]), FadeOut(lines), run_time=0.7)
        del c["vs@L"], c["vs@a"]
        self.morph(["q", "B", "=", ("f", ["m", "vs@b"], ["R"], "b1")], SZ, AT, run=1.0)
        self.hold(0.8)
        # |q|/m: o rearranjo é rastreável (os fatores que continuam são os mesmos objetos que se movem)
        self.morph([("f", ["q", "B"], ["m"], "b2"), "=", ("f", ["vs@b"], ["R"], "b1")], SZ, AT, run=1.4)          # m desce para a esquerda
        self.hold(1.0)
        self.morph([("f", ["q"], ["m"], "b2"), "=", ("f", ["vs@b"], ["B", "R"], "b1")], SZ, AT, run=1.4)          # B atravessa a igualdade
        bx = box(VGroup(*self.cur.values()))
        self.play(FadeIn(bx), run_time=0.5)
        self.hold(1.4)
        self.play(FadeOut(bx), FadeOut(cap), run_time=0.4)
        # v = E/B (do seletor) alimenta a substituição
        cap2 = VGroup(txt("usando a velocidade selecionada", T_NOTE, opacity=0.95),
                      txt("(mesmo módulo B nas duas etapas)", 20, opacity=0.8)).arrange(DOWN, buff=0.1).move_to([4.3, 0.95, 0])
        self.play(FadeIn(cap2), Indicate(self.rlab8[2], color=CYAN, scale_factor=1.15), run_time=0.8)
        self.morph([("f", ["q"], ["m"], "b2"), "=", ("f", [("f", ["Es"], ["Bs"], "b4")], ["B", "R"], "b1")], SZ, AT,
                   alias={"vs@b": ["Es", "b4", "Bs"]}, run=1.8)
        self.hold(1.4)
        self.morph([("f", ["q"], ["m"], "b2"), "=", ("f", ["Es"], ["B2", "R"], "b1")], SZ + 4, AT, alias={"Bs": ["B2"]}, run=1.6)
        bx = box(VGroup(*self.cur.values()))
        nm_qm = nome("Razão carga–massa em módulo", pos=(4.3, 0.15, 0))
        self.play(FadeIn(bx), FadeOut(cap2), FadeIn(nm_qm), run_time=0.6)
        self.hold(2.8)
        self.fin8 = bx
        self.nome_qm = nm_qm

    def b08_leituras(self):
        """Cada medida aponta para a parte do experimento que a fornece."""
        L1 = txt("↑ vem do seletor", 22, opacity=0.95).move_to([4.3, 2.0, 0])
        L2 = VGroup(txt("com E e B conhecidos, medir R fornece", 22, opacity=0.95),
                    eq(r"|q|/m", size=32, colors={0: BLUE_L})).arrange(RIGHT, buff=0.2).move_to([-3.0, -3.2, 0])
        self.play(FadeIn(L1), run_time=0.8)
        self.hold(1.0)
        self.play(FadeIn(L2), run_time=0.8)
        self.hold(1.4)
        # sentido da curvatura ↔ sinal de q (R em módulo)
        sg_lab = VGroup(eq(r"q>0", size=30, colors={0: BLUE_L}), txt("curva para baixo", 22, opacity=0.9)).arrange(RIGHT, buff=0.2).move_to([4.3, 0.95, 0])
        self.play(FadeIn(sg_lab), run_time=0.7)
        self.hold(2.4)
        self.qs7.set_value(-1.0)
        sg_lab2 = VGroup(eq(r"q<0", size=30, colors={0: BLUE_L}), txt("curva para cima (mesmo R)", 22, opacity=0.9)).arrange(RIGHT, buff=0.2).move_to([4.3, 0.95, 0])
        self.play(RT(sg_lab, sg_lab2), run_time=0.8)
        self.hold(3.0)
        self.qs7.set_value(1.0)
        sg3 = VGroup(txt("o sentido da curva dá o sinal de", 22, opacity=0.9), eq("q", size=30, colors={0: BLUE_L})).arrange(RIGHT, buff=0.15).move_to([4.3, 0.95, 0])
        self.play(RT(sg_lab2, sg3), run_time=0.8)
        # callback: trabalho magnético
        cb = VGroup(eq(r"|\mathbf v|", r"\ \text{constante}\ \Rightarrow\ ", "W_B", "=0", size=30, colors={0: VIOLET, 2: CYAN})).move_to([4.3, 1.6, 0])
        self.play(FadeIn(cb), run_time=0.8)
        self.hold(2.0)
        un = VGroup(eq(r"\left[\frac EB\right]", "=", r"\mathrm{m/s}", size=30), eq(r"\left[\frac{E}{B^2R}\right]", "=", r"\mathrm{C/kg}", size=28)).arrange(RIGHT, buff=0.5).move_to([3.9, -3.2, 0])
        self.play(FadeIn(un, shift=0.1 * UP), run_time=0.8)
        self.hold(3.0)
        self.keep8 = VGroup(L1, L2, sg3, cb, un)

    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    # B09 · síntese e ponte para Biot–Savart
    # ═════════════════════════════════════════════════════════════════════════════════════════════════════════
    def bloco_09_fechamento(self):
        self.seg("J")
        self.limpa(0.8)
        # uma única forma central se transforma, passo a passo, nas imagens que já vimos
        cx = np.array([0.0, 0.3, 0.0])

        def tag(t_):
            if isinstance(t_, VGroup):
                return t_.move_to([0.0, -2.4, 0])
            return txt(t_, T_BODY, opacity=0.95).move_to([0.0, -2.4, 0])

        f0 = eq(r"\mathbf F_B", "=", "q", r"\mathbf v", r"\times", r"\mathbf B", size=64, colors={0: FC, 2: BLUE_L, 3: VIOLET, 5: MAG}).move_to(cx)
        t0 = tag("força magnética: a lei que sustenta tudo")
        self.play(FadeIn(f0, shift=0.1 * DOWN), FadeIn(t0), run_time=1.2)
        self.hold(2.0)
        # → círculo
        circ = Circle(radius=1.3, color=BLUE_L, stroke_width=3.5).move_to(cx)
        dotc = charge_c(cx + np.array([-1.3, 0.0, 0.0]), 1, 0.9)
        va = arrow(cx + np.array([-1.3, 0.0, 0.0]), cx + np.array([-1.3, 0.9, 0.0]), VIOLET, 5, 5)
        t1 = tag(VGroup(eq(r"\mathbf v_\parallel", "=", "0", size=40, colors={0: VIOLET}), txt(": círculo,", T_BODY, opacity=0.95),
                        eq(r"\omega", "=", r"\frac{|q|B}{m}", size=34, colors={0: VIOLET})).arrange(RIGHT, buff=0.25))
        self.play(FadeOut(f0), FadeOut(t0), run_time=0.5)
        self.play(FadeIn(VGroup(circ, dotc, va)), FadeIn(t1), run_time=0.9)
        self.hold(1.6)
        # → hélice
        hel = ParametricFunction(lambda t: cx + np.array([1.3 * math.cos(t) - 0.0, 0.45 * math.sin(t) + 0.16 * t - 1.2, 0.0]), t_range=[0, 6 * math.pi],
                                 color=BLUE_L, stroke_width=3.5)
        t2 = tag(VGroup(eq(r"\mathbf v_\parallel\neq 0", size=60, colors={0: VIOLET}), txt(": hélice", T_BODY, opacity=0.95)).arrange(RIGHT, buff=0.2))
        self.play(ReplacementTransform(circ, hel), FadeOut(dotc), FadeOut(va), FadeOut(t1), run_time=1.0)       # círculo → hélice: correspondência geométrica
        self.play(FadeIn(t2), run_time=0.6)
        self.hold(1.6)
        # → muitas cargas → corrente (portadores azuis; corrente convencional em verde)
        wire = Line([-3.0, 0.3, 0], [3.0, 0.3, 0], color=BLUE_L, stroke_width=6).set_opacity(0.45)
        cars = VGroup(*[charge_c([x, 0.3, 0], 1, 0.5) for x in np.linspace(-2.6, 2.6, 7)])
        arr = arrow([2.0, 0.85, 0], [3.2, 0.85, 0], GREEN, 6, 4)
        il = eq("I", size=M_M, colors={0: GREEN}).move_to([2.6, 1.3, 0])
        t3 = tag("muitas cargas: corrente")
        self.play(FadeOut(hel), FadeOut(t2), run_time=0.5)
        self.play(FadeIn(VGroup(wire, cars, arr, il)), FadeIn(t3), run_time=0.9)
        self.hold(1.6)
        # → densidade J: fluxo verde contínuo, paralelo e regularmente espaçado (J ≠ 0 e ∇·J = 0)
        p9 = self.clock("p9")
        self.run["p9"] = True
        g9 = ValueTracker(0.0)
        ROWS9 = (-0.6, 0.0, 0.6, 1.2)

        def flow9():
            g = VGroup()
            if g9.get_value() < 0.02:
                return g
            gap, x0, x1 = 1.2, -3.4, 3.4
            n = int((x1 - x0) / gap)
            L = n * gap
            for yy in ROWS9:
                for k in range(n):
                    x = x0 + (p9.get_value() * 0.9 + k * gap) % L
                    op = min(1.0, (x - x0) / 0.5, (x1 - x) / 0.5)
                    g.add(arrow([x, yy + 0.1, 0], [x + 0.6, yy + 0.1, 0], GREEN, 5, 2, tip=0.17).set_opacity(0.95 * op * g9.get_value()))
            return g

        flow = always_redraw(flow9)
        flow.dyn = True
        self.add(flow)
        jl = eq(r"\mathbf J", size=52, colors={0: GREEN}).move_to([-3.7, 1.7, 0])
        t4 = VGroup(eq(r"\mathbf J\neq 0", ",", r"\ \nabla\cdot\mathbf J=0", size=44, colors={0: GREEN, 2: GREEN}),
                    txt("regime estacionário", 22, opacity=0.9)).arrange(DOWN, buff=0.2).move_to([0.0, -2.35, 0])
        self.play(FadeOut(VGroup(wire, cars, arr, il)), g9.animate.set_value(1.0), FadeIn(jl), FadeOut(t3), FadeIn(t4), run_time=1.4)
        self.hold(3.2)
        # → Thomson
        pl = VGroup(Rectangle(width=2.6, height=0.12, color=WHITE, stroke_width=2).move_to([0.0, 1.2, 0]), Rectangle(width=2.6, height=0.12, color=WHITE, stroke_width=2).move_to([0.0, -0.6, 0]))
        bm = Line([-3.2, 0.3, 0], [3.2, 0.3, 0], color=BLUE_L, stroke_width=3.5)
        t5 = VGroup(eq("v", "=", r"\frac EB", size=34, colors={0: VIOLET, 2: CYAN}), eq(r"\frac{|q|}{m}", "=", r"\frac{E}{B^2R}", size=34, colors={0: BLUE_L, 2: CYAN})).arrange(RIGHT, buff=0.6).move_to([0.0, -2.4, 0])
        self.play(g9.animate.set_value(0.0), FadeOut(jl), FadeIn(VGroup(pl, bm)), FadeOut(t4), FadeIn(t5), run_time=1.4)
        self.remove(flow)
        self.hold(2.2)
        self.play(FadeOut(pl), FadeOut(bm), FadeOut(t5), run_time=0.8)
        self.b09_fios()
        self.b09_cta()

    def b09_fios(self):
        """Volta aos dois fios do começo, agora com a corrente (verde) EM MOVIMENTO e o B orientado em torno de cada fio."""
        WX = 1.9
        ph = self.clock("p9b")
        self.run["p9b"] = True
        self.g9b = ValueTracker(1.0)
        wl = Line([-WX, -2.0, 0], [-WX, 1.9, 0], color=BLUE_L, stroke_width=6)
        wr = Line([WX, -2.0, 0], [WX, 1.9, 0], color=BLUE_L, stroke_width=6)
        cl = arrow([-2.75, 0.6, 0], [-2.75, 1.7, 0], GREEN, 6)
        cr = arrow([2.75, 0.6, 0], [2.75, 1.7, 0], GREEN, 6)
        il, ir = eq("I_1", size=M_S, colors={0: GREEN}).next_to(cl, LEFT, buff=0.15), eq("I_2", size=M_S, colors={0: GREEN}).next_to(cr, RIGHT, buff=0.15)
        YMIN, SPAN, STEP = -1.9, 3.7, 0.3

        def pulses(x):
            def f():
                g = VGroup()
                period = 0.7
                for k in range(int((SPAN + STEP) / period) + 1):
                    y = YMIN + ((k * period + ph.get_value() * 0.75) % (SPAN + STEP))
                    op = min(1.0, max(0.0, min(y + 1.95, 1.95 - y) / 0.4))
                    y2 = min(y + 0.32, 1.9)
                    g.add(Line([x, y, 0], [x, y2, 0], color=GREEN, stroke_width=5).set_opacity(0.95 * op * self.g9b.get_value()))
                return g.set_z_index(2)
            return always_redraw(f)

        pl_, pr_ = pulses(-WX), pulses(WX)
        pl_.dyn = True
        pr_.dyn = True
        self.add(pl_, pr_)
        self.play(FadeIn(wl), FadeIn(wr), FadeIn(cl), FadeIn(cr), FadeIn(il), FadeIn(ir), run_time=1.4)
        self.hold(1.0)
        # B ao redor de cada corrente: anéis em perspectiva com portadores de sentido (regra da mão direita: anti-horário visto de cima)
        RW, RH = 0.75, 0.25
        levels = (-1.2, -0.1, 1.0)
        rings = VGroup()
        for x in (-WX, WX):
            for y in levels:
                rings.add(Ellipse(width=2 * RW, height=2 * RH, color=MAG, stroke_width=2.5).move_to([x, y, 0]).set_stroke(opacity=0.8))

        marks = VGroup()
        for x in (-WX, WX):
            for y in levels:
                for th, op in ((-math.pi / 2, 1.0), (math.pi / 2, 0.45), (0.0, 0.8), (math.pi, 0.8)):
                    p = np.array([x + RW * math.cos(th), y + RH * math.sin(th), 0.0])
                    tv = np.array([-RW * math.sin(th), RH * math.cos(th), 0.0])
                    tv /= np.linalg.norm(tv)
                    marks.add(arrow(p - 0.22 * tv, p + 0.22 * tv, MAG, 5, 6, tip=0.2).set_opacity(op))   # tangentes fixas: sentido de B
        md = marks
        blab = eq(r"\mathbf B", size=44, colors={0: MAG}).move_to([0.0, 1.5, 0])
        self.play(FadeIn(rings), FadeIn(md), FadeIn(blab), run_time=1.4)
        self.hold(2.0)
        att = VGroup(arrow([-WX + 0.2, -0.6, 0], [-WX + 1.0, -0.6, 0], FC, 5, 4), arrow([WX - 0.2, -0.6, 0], [WX - 1.0, -0.6, 0], FC, 5, 4))
        self.play(FadeIn(att), run_time=0.8)
        self.hold(1.2)
        q_ = VGroup(txt("Como uma corrente cria", 34), eq(r"\mathbf B", size=46, colors={0: MAG}), txt("?", 34)).arrange(RIGHT, buff=0.18).move_to([0.0, -2.75, 0])
        bq = box(q_)
        self.play(FadeIn(q_, shift=0.1 * UP), FadeIn(bq), run_time=1.2)
        self.hold(4.0)                               # a cena segue viva: corrente fluindo, B girando
        self.fios9 = VGroup(wl, wr, cl, cr, il, ir, rings, md, blab, att, q_, bq)

    def b09_cta(self):
        """End card no padrão dos longos (Gauss): marca Parallax Lab, anéis tracejados, chamada curta e tease do próximo assunto."""
        oc = np.array([0.0, 0.5, 0.0])
        rings = VGroup(*[DashedVMobject(Circle(radius=r, arc_center=oc), num_dashes=max(12, int(14 * r)), dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.16)
                         for r in (2.0, 3.0, 4.0)])
        for i, r_ in enumerate(rings):
            r_.add_updater(lambda m, dt, s=(1 if i % 2 == 0 else -1) * (0.06 - 0.01 * i): m.rotate(s * dt, about_point=oc))
        logo = ImageMobject(str(LOGO_PATH)).set_width(6.0).move_to(oc + np.array([0.0, 0.5, 0.0]))
        msg = txt("Inscreva-se para acompanhar os próximos vídeos", 28, opacity=0.9).move_to(oc + np.array([0.0, -0.9, 0.0]))
        nxt = VGroup(txt("Próximo:", 24, opacity=0.8), txt("como uma corrente gera campo magnético", 24, opacity=0.95)).arrange(RIGHT, buff=0.2).move_to(oc + np.array([0.0, -1.75, 0.0]))

        def ripple():
            w = DashedVMobject(Circle(radius=1.6, arc_center=oc), num_dashes=24, dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.35)
            self.play(w.animate.scale(2.6, about_point=oc).set_stroke(opacity=0.0), run_time=2.6)
            self.remove(w)

        self.play(FadeOut(self.fios9), self.g9b.animate.set_value(0.0), FadeOut(self.wm), FadeOut(self.tag), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(r_, scale=0.85) for r_ in rings], lag_ratio=0.3), FadeIn(logo, scale=0.92), run_time=1.8)
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=1.0)
        self.hold(0.8)
        self.play(FadeIn(nxt, shift=0.1 * UP), run_time=1.0)
        ripple()
        ripple()
        self.hold(1.2)
