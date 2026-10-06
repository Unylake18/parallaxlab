"""Potencial de poço duplo a partir da força F(x) = F0 [x/ℓ − (x/ℓ)³]: preview silencioso (V2).

DA EQUAÇÃO AO FENÔMENO · EP. 04. Pergunta: "PRESA DE UM LADO OU ATRAVESSA?" (sem resolver x(t)).

Segmentos (tempos ditados pelo conteúdo; `self.mark(...)` registra marcas no console):
  S1  força dada -> zeros F(x)=0 -> curva -> sinal de F e setas sobre o eixo x -> ponte para o potencial
  S2  F = −U′ -> U = −∫F dx -> integração termo a termo (x -> x²/2, x³ -> x⁴/4, fatores 1/ℓ, 1/ℓ³, sinal)
  S3  zero de energia nos mínimos: U(±ℓ) = 0 -> substituir x = ℓ -> C = F0ℓ/4
  S4  substituir C -> trinômio -> quadrado perfeito; conferência −U′ = F
  S5  gráfico de U (eixo vertical = energia) a partir dos pontos calculados; classificação por U″ e pela força
  S6  E = K + U -> K = E − U ≥ 0 -> U ≤ E; a linha E nasce da desigualdade; leitura de K com um cursor
  S7  regimes (cada E é uma nova condição inicial): E = 0, 0 < E < U_b, E = U_b, E > U_b
  S8  coda: paisagem de energia (analogia), sem reiniciar a trajetória

Gráfico de energia adimensional: x em unidades de ℓ, U em unidades de U_b = F0ℓ/4: u(x) = (x² − 1)².
Durante os regimes a partícula só se move no eixo espacial x, separado do eixo de energia. Posição da
partícula, linha E, retornos, região permitida e barra K = E − U leem os mesmos trackers (E, TT).
Dinâmica: ẍ = −κ u′(x) (m = 1), κ = 0,2, RK4 nos regimes limitados; a separatriz usa a solução exata
√2 sech(a t) só para posicionar o ponto (nenhuma x(t) aparece no vídeo).

`ATE=k` (1–8) renderiza só até o segmento k.
"""

import os
import sys
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, AnimationGroup, Arrow, Circle, Create, DashedLine, Dot, FadeIn, FadeOut, ImageMobject,
    Indicate, Line, MathTex, Scene, SurroundingRectangle, TransformFromCopy, TransformMatchingTex, VGroup, VMobject,
    ValueTracker, always_redraw, config, linear, smooth,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

ATE = int(os.environ.get("ATE", "99"))

# ── Paleta ──────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # força F(x)
VIOLET = "#9C8CFF"        # potencial U(x) (SECONDARY #745CFF clareado para contraste, como no vid_0012)
BLUE = "#267BFF"          # linha e região de energia
BLUE_L = "#7FB2FF"        # rótulos de energia, pontos de retorno
MAGENTA = "#EA63FF"       # barreira U_b e constante C
KCOL = "#DDEBFF"          # barra K = E − U

SAFE_BOTTOM = -4.6        # abaixo disso: faixa reservada a legendas

# ── Modelo ──────────────────────────────────────────────────────────────────
KAPPA = 0.2               # ẍ = −κ u′(x); só escolhe a escala de tempo da animação
A_SEP = 2 * np.sqrt(KAPPA) * 0.75   # separatriz a 0,75× (câmera lenta) para a aproximação ser acompanhável
E_SUB, E_SEP, E_SUP = 0.5, 1.0, 1.5     # energias dos regimes, em unidades de U_b


def f_force(x):
    """F/F0 como função de x/ℓ."""
    return x - x ** 3


def u(x):
    """U/U_b como função de x/ℓ."""
    return (x * x - 1.0) ** 2


def du(x):
    return 4.0 * x * (x * x - 1.0)


def d2u(x):
    return 12.0 * x * x - 4.0


def allowed(E):
    """Intervalos de x (em ℓ) onde u(x) ≤ E."""
    if E <= 1e-9:
        return [(-1.0, -1.0), (1.0, 1.0)]
    if E < 1.0 - 1e-9:
        a, b = np.sqrt(1 - np.sqrt(E)), np.sqrt(1 + np.sqrt(E))
        return [(-b, -a), (a, b)]
    b = np.sqrt(1 + np.sqrt(E))
    return [(-b, b)]


def turning_points(E):
    return sorted({round(float(v), 9) for iv in allowed(E) for v in iv})


def _rk4(x0, v0, T, dt=0.002):
    n = int(T / dt) + 1
    ts, xs, vs = np.arange(n) * dt, np.empty(n), np.empty(n)
    x, v = x0, v0
    f = lambda y: -KAPPA * du(y)
    for i in range(n):
        xs[i], vs[i] = x, v
        k1x, k1v = v, f(x)
        k2x, k2v = v + .5 * dt * k1v, f(x + .5 * dt * k1x)
        k3x, k3v = v + .5 * dt * k2v, f(x + .5 * dt * k2x)
        k4x, k4v = v + dt * k3v, f(x + dt * k3x)
        x += dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        v += dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
    return ts, xs, vs


_TS_SUB, _XS_SUB, _VS_SUB = _rk4(allowed(E_SUB)[1][1], 0.0, 20.0)
_TS_SUP, _XS_SUP, _VS_SUP = _rk4(-allowed(E_SUP)[0][1], 0.0, 14.0)


def traj_rest(t):
    return 1.0


def traj_sub(t):
    return float(np.interp(t, _TS_SUB, _XS_SUB))


def traj_sep(t):
    return float(np.sqrt(2.0) / np.cosh(A_SEP * t))


def traj_sup(t):
    return float(np.interp(t, _TS_SUP, _XS_SUP))


def _qa():
    """Verificações numéricas independentes do modelo (roda ao importar)."""
    xs = np.linspace(-1.6, 1.6, 321)
    h = 1e-6
    # F = −U′: F = F0[x/ℓ − (x/ℓ)³] e U = (F0ℓ/4)[(x/ℓ)² − 1]²  (em unidades F0 e ℓ: U/(F0 ℓ) = u/4)
    assert np.allclose(f_force(xs), -(u(xs + h) - u(xs - h)) / (2 * h) / 4, atol=1e-7)
    assert np.allclose(du(xs), (u(xs + h) - u(xs - h)) / (2 * h), atol=1e-6)
    assert np.allclose(d2u(xs), (du(xs + h) - du(xs - h)) / (2 * h), atol=1e-5)
    # zeros: F(x) = 0 <=> (x/ℓ)[1 − (x/ℓ)²] = 0 <=> x = −ℓ, 0, ℓ
    assert np.allclose(f_force(xs), xs * (1 - xs ** 2))
    assert f_force(0.0) == 0 and f_force(1.0) == 0 and f_force(-1.0) == 0
    # integração passo a passo, com F0 e ℓ arbitrários
    for F0, ell in ((2.3, 0.37), (1.0, 1.0), (5.5, 2.2)):
        x = xs * ell
        m4 = -F0 * (x ** 2 / (2 * ell) - x ** 4 / (4 * ell ** 3))                 # −F0[x²/2ℓ − x⁴/4ℓ³] (+ C)
        m5 = -F0 * x ** 2 / (2 * ell) + F0 * x ** 4 / (4 * ell ** 3)              # sinal distribuído
        assert np.allclose(m4, m5)
        # condição de referência: U(ℓ) = 0 => C = F0ℓ/4
        c = F0 * ell / 4
        assert np.isclose(-F0 * ell ** 2 / (2 * ell) + F0 * ell ** 4 / (4 * ell ** 3) + c, 0.0, atol=1e-12)
        assert np.isclose(-F0 * ell / 2 + F0 * ell / 4, -F0 * ell / 4)
        u_sum = m5 + c
        u_tri = c * ((x / ell) ** 4 - 2 * (x / ell) ** 2 + 1)                     # trinômio
        u_sq = c * ((x / ell) ** 2 - 1) ** 2                                      # quadrado perfeito
        assert np.allclose(u_sum, u_tri) and np.allclose(u_tri, u_sq)
        assert np.isclose(c * ((0.0 / ell) ** 2 - 1) ** 2, F0 * ell / 4)          # U(0) = U_b = F0ℓ/4
        # −U′ = F
        dx = 1e-6 * ell
        assert np.allclose(-(c * (((x + dx) / ell) ** 2 - 1) ** 2 - c * (((x - dx) / ell) ** 2 - 1) ** 2) / (2 * dx),
                           F0 * (x / ell - (x / ell) ** 3), atol=1e-6 * F0)
        # U″ = −F′: F′ = F0 (1/ℓ − 3x²/ℓ³)  =>  U″(0) = −F0/ℓ  e  U″(±ℓ) = 2F0/ℓ
        assert np.isclose(-F0 * (1 / ell - 0.0), -F0 / ell)
        assert np.isclose(-F0 * (1 / ell - 3 * ell ** 2 / ell ** 3), 2 * F0 / ell)
    assert np.allclose(u(xs) / 4, xs ** 4 / 4 - xs ** 2 / 2 + 0.25)               # coeficientes em unidades F0, ℓ
    # equilíbrios e classificação
    assert u(1.0) == 0 and u(-1.0) == 0 and u(0.0) == 1.0                         # U(±ℓ) = 0, U(0) = U_b
    assert d2u(0.0) < 0 and d2u(1.0) > 0 and d2u(-1.0) > 0
    # sinais da força nas quatro regiões (setas)
    assert f_force(-1.35) > 0 and f_force(-0.5) < 0 and f_force(0.5) > 0 and f_force(1.35) < 0
    # pontos de retorno: u(x_r) = E
    for E in (E_SUB, E_SEP, E_SUP, 0.2, 0.9):
        for iv in allowed(E):
            for x in iv:
                assert np.isclose(u(x), E, atol=1e-12)
    # quatro interseções só para 0 < E < U_b; duas para E ≥ U_b
    assert len(turning_points(E_SUB)) == 4 and len(turning_points(E_SUP)) == 2
    assert np.isclose(allowed(E_SEP)[0][1], np.sqrt(2)) and len(allowed(E_SEP)) == 1
    # posições escolhidas para a leitura de K: permitida (K > 0), no retorno (K = 0) e proibida (U > E, K < 0)
    assert E_SUB - u(1.15) > 0 and np.isclose(E_SUB - u(allowed(E_SUB)[1][1]), 0, atol=1e-12) and u(0.3) > E_SUB
    # conservação de energia: ½v² + κu = κE
    for ts, xs_, vs_, E in ((_TS_SUB, _XS_SUB, _VS_SUB, E_SUB), (_TS_SUP, _XS_SUP, _VS_SUP, E_SUP)):
        assert np.max(np.abs(0.5 * vs_ ** 2 + KAPPA * u(xs_) - KAPPA * E)) < 1e-7
    # 0 < E < U_b: confinado a uma componente permitida; trajetória nunca sai de [a, b]
    a, b = allowed(E_SUB)[1]
    assert _XS_SUB.min() >= a - 1e-6 and _XS_SUB.max() <= b + 1e-6
    # E > U_b: atravessa x = 0 e fica entre os dois retornos externos
    b = allowed(E_SUP)[0][1]
    assert _XS_SUP.min() >= -b - 1e-6 and _XS_SUP.max() <= b + 1e-6
    assert np.any(np.diff(np.sign(_XS_SUP)) != 0)
    # separatriz: √2 sech(a t) (a = 2√κ·s, s = escala de tempo da apresentação) conserva E = U_b na escala s,
    # é monótona e decresce para 0 sem nunca chegar nem cruzar
    s = A_SEP / (2 * np.sqrt(KAPPA))
    t = np.linspace(0, 9, 4501)
    xs_ = np.array([traj_sep(v) for v in t])
    vs_ = np.gradient(xs_, t)
    assert np.max(np.abs(0.5 * vs_[5:-5] ** 2 + KAPPA * s ** 2 * u(xs_[5:-5]) - KAPPA * s ** 2 * E_SEP)) < 1e-4
    assert np.all(np.diff(xs_) < 0) and xs_.min() > 0
    assert np.isclose(traj_sep(0.0), np.sqrt(2)) and np.isclose(u(np.sqrt(2)), E_SEP)


_qa()

# ── Geometria da tela (frame 9 × 16) ────────────────────────────────────────
# Gráfico de energia: x em unidades de ℓ, U em unidades de U_b.
GSX, GX0 = 1.9, 0.0       # tela por ℓ
GY0, GSY = -0.15, 1.35    # U = 0 e tela por U_b
AXL, AXR = -3.4, 3.4      # eixo vertical e extensão horizontal
XR = 1.6                  # domínio do gráfico: |x| ≤ 1,6 ℓ
PY = -2.45                # eixo espacial da partícula (faixa inferior do gráfico)
# Gráfico da força (S1)
FSX, FY0, FSY, FXR = 2.1, -0.2, 1.3, 1.45
FAX = -3.45               # eixo vertical F


def gx(x):
    return GX0 + GSX * x


def gy(uu):
    return GY0 + GSY * uu


def gpt(x):
    return np.array([gx(x), gy(u(x)), 0.0])


def fpt(x):
    return np.array([FSX * x, FY0 + FSY * f_force(x), 0.0])


# ── Texto e utilidades (mesmo idioma dos vídeos anteriores) ─────────────────
@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def text(content, size=24, color=WHITE, opacity=1.0):
    with wide_pango():
        t = screen_text(content, size)
    return t.set_color(color).set_opacity(opacity)


def display(content, size=38):
    with wide_pango():
        t = screen_text(content, size, oversample=2)
    return t.set_color(WHITE)


def lines(*strs, size=38):
    return VGroup(*(display(s, size) for s in strs)).arrange(DOWN, buff=0.14)


def tex(content, size=36, color=WHITE):
    return MathTex(content, font_size=size, color=color)


def mt(*parts, size=40, colors=None, maxw=7.6):
    """MathTex em partes (para TransformMatchingTex), com cor por índice de parte."""
    m = MathTex(*parts, font_size=size, color=WHITE)
    for i, c in (colors or {}).items():
        m[i].set_color(c)
    if maxw and m.width > maxw:
        m.scale_to_fit_width(maxw)
    return m


def mixed(*items, buff=0.16):
    return VGroup(*items).arrange(RIGHT, buff=buff)


def soft_swap(old, new, shift=UP * 0.12, lag=0.55):
    return AnimationGroup(FadeOut(old, shift=shift), FadeIn(new, shift=shift), lag_ratio=lag)


def seg(p, q, **kw):
    return Line(np.array([p[0], p[1], 0.0]), np.array([q[0], q[1], 0.0]), **kw)


def kseg(x, E, alpha):
    """Barra K = E − U(x) em x: sólida se U ≤ E; tracejada magenta (posição proibida) se U > E."""
    g = VGroup()
    if u(x) <= E + 1e-9:
        if gy(E) - gy(u(x)) > 0.03:
            g.add(seg((gx(x), gy(u(x))), (gx(x), gy(E)), stroke_width=6, color=KCOL).set_opacity(alpha).set_z_index(4))
    else:
        g.add(DashedLine([gx(x), gy(E), 0], [gx(x), gy(u(x)), 0], color=MAGENTA, stroke_width=2.5, dash_length=0.1)
              .set_opacity(0.8 * alpha))
    return g


class PotencialPocoDuplo013(Scene):

    def mark(self, name):
        print(f"[MARCA] {self.renderer.time:7.2f} s  {name}")

    def xp(self):
        return float(self.traj(self.T.TT.get_value()))

    # ── Construção dos objetos dirigidos por trackers e dos objetos estáticos ──
    def build(self):
        T = self.T = SimpleNamespace(
            E=ValueTracker(E_SUB),       # energia (u.a. de U_b)
            LA=ValueTracker(0),          # opacidade da linha E e do rótulo E
            RG=ValueTracker(0),          # eixo espacial: regiões permitidas, retornos e projeções
            VP=ValueTracker(0),          # partícula
            KB=ValueTracker(0),          # barra K = E − U na posição da partícula e guia
            KL=ValueTracker(0),          # rótulo fixo K = E − U(x)
            DL=ValueTracker(0),          # atenua a componente da esquerda (não ocupada)
            FB=ValueTracker(0),          # trecho central proibido (0 < E < U_b)
            CV=ValueTracker(0),          # cursor de leitura de K (S6)
            CS=ValueTracker(1.15),       # posição do cursor
            TT=ValueTracker(0),          # tempo da trajetória
            BALL=ValueTracker(0),        # marcador da analogia (coda)
        )
        self.traj = traj_rest

        # Gráfico de força (S1): eixos x e F
        self.f_axis = Arrow([-3.4, FY0, 0], [3.4, FY0, 0], buff=0, stroke_width=2.5, tip_length=0.16,
                            color=WHITE).set_opacity(0.55)
        self.f_x = tex("x", 30).move_to([3.3, FY0 - 0.35, 0])
        self.f_vaxis = Arrow([FAX, FY0 - 2.3, 0], [FAX, FY0 + 2.5, 0], buff=0, stroke_width=2.5, tip_length=0.16,
                             color=WHITE).set_opacity(0.55)
        self.f_vlab = tex("F", 34, CYAN).move_to([FAX + 0.32, FY0 + 2.55, 0])
        self.f_curve = VMobject(color=CYAN, stroke_width=5).set_points_smoothly(
            [fpt(x) for x in np.linspace(-FXR, FXR, 121)])
        self.f_zeros = VGroup(*(Dot(fpt(z), radius=0.09, color=WHITE).set_z_index(3) for z in (-1, 0, 1)))
        self.f_ticks = VGroup(
            tex(r"-\ell", 30).move_to([-FSX, FY0 - 0.55, 0]),
            tex("0", 30).move_to([0, FY0 - 0.55, 0]),
            tex(r"+\ell", 30).move_to([FSX, FY0 - 0.55, 0]),
        )
        # Partículas sobre o eixo com a força: (x/ℓ, sentido, lado do rótulo, sinal)
        self.f_states = []
        for x0, direc, side, sign in ((-1.35, 1, -1, ">"), (-0.5, -1, 1, "<"), (0.5, 1, -1, ">"),
                                      (1.35, -1, 1, "<")):
            cx = FSX * x0
            dot = VGroup(Dot([cx, FY0, 0], radius=0.19, color=WHITE).set_opacity(0.18),
                         Dot([cx, FY0, 0], radius=0.09, color=WHITE)).set_z_index(5)
            arr = Arrow([cx + 0.16 * direc, FY0, 0], [cx + 0.58 * direc, FY0, 0], buff=0, color=CYAN, stroke_width=6,
                        max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=10).set_z_index(4)
            lab = tex(rf"F{sign}0", 32, CYAN).move_to([cx + 0.1 * direc, FY0 + (0.55 if side > 0 else -1.05), 0])
            self.f_states.append(VGroup(dot, arr, lab))

        # Gráfico de energia (S5 em diante)
        self.u_curve = VMobject(color=VIOLET, stroke_width=5).set_points_smoothly(
            [gpt(x) for x in np.linspace(-XR, XR, 161)])
        self.u_axis = Arrow([AXL, GY0 - 0.2, 0], [AXL, 3.4, 0], buff=0, stroke_width=2.5, tip_length=0.16,
                            color=WHITE).set_opacity(0.55)
        self.u_label = tex("U", 34, VIOLET).move_to([AXL + 0.32, 3.3, 0])
        self.base = Line([AXL, GY0, 0], [AXR, GY0, 0], stroke_width=2, color=WHITE).set_opacity(0.35)
        self.base_x = tex("x", 30).move_to([AXR - 0.05, GY0 - 0.32, 0])
        self.base_ticks = VGroup(
            tex(r"-\ell", 28).move_to([gx(-1), GY0 - 0.42, 0]),
            tex("0", 28).move_to([gx(0), GY0 - 0.42, 0]),
            tex(r"\ell", 28).move_to([gx(1), GY0 - 0.42, 0]),
        )
        self.ub_level = DashedLine([AXL, gy(1), 0], [gx(0), gy(1), 0], color=MAGENTA, stroke_width=2.5,
                                   dash_length=0.12).set_opacity(0.85)
        self.ub_dot = Dot([gx(0), gy(1), 0], radius=0.1, color=MAGENTA).set_z_index(3)
        self.ub_tick = tex(r"U_b", 30, MAGENTA).move_to([AXL - 0.42, gy(1), 0])
        self.u_name = tex(r"U(x)", 30, VIOLET).move_to([2.45, 2.95, 0])
        self.well_dots = VGroup(*(Dot([gx(s), GY0, 0], radius=0.09, color=VIOLET).set_z_index(3) for s in (-1, 1)))

        # Eixo espacial (faixa inferior)
        self.p_axis = Arrow([AXL, PY, 0], [AXR, PY, 0], buff=0, stroke_width=2.5, tip_length=0.16,
                            color=WHITE).set_opacity(0.6)
        self.p_x = tex("x", 30).move_to([AXR - 0.05, PY + 0.32, 0])
        self.p_ticks = VGroup(
            seg((gx(-1), PY - 0.09), (gx(-1), PY + 0.09), stroke_width=3, color=VIOLET),
            seg((gx(0), PY - 0.09), (gx(0), PY + 0.09), stroke_width=3, color=MAGENTA),
            seg((gx(1), PY - 0.09), (gx(1), PY + 0.09), stroke_width=3, color=VIOLET),
        )
        self.p_labels = VGroup(
            tex(r"-\ell", 28).move_to([gx(-1), PY - 0.42, 0]),
            tex("0", 28).move_to([gx(0), PY - 0.42, 0]),
            tex(r"\ell", 28).move_to([gx(1), PY - 0.42, 0]),
        )
        self.p_group = VGroup(self.p_axis, self.p_x, self.p_ticks, self.p_labels)

        # Linha de energia (E) e rótulo
        def eline():
            la = T.LA.get_value()
            if la <= 0.001:
                return VGroup()
            y = gy(T.E.get_value())
            return Line([AXL, y, 0], [AXR, y, 0], color=BLUE, stroke_width=4).set_opacity(la).set_z_index(2)

        self.eline = always_redraw(eline)
        self.e_lab = tex("E", 34, BLUE_L)
        self.e_lab.add_updater(lambda m: m.move_to([AXR + 0.2, gy(T.E.get_value()) + 0.3, 0])
                               .set_opacity(T.LA.get_value()))

        # Regiões permitidas (eixo espacial), retornos (na linha E) e projeções (pontilhadas, discretas)
        def dimf(x0):
            return 1 - 0.72 * T.DL.get_value() if x0 < 0 else 1.0

        def ivs(E):
            if abs(E - 1.0) < 1e-9:        # separatriz: o lado percorrido e o outro lado do conjunto U ≤ E
                b = allowed(E)[0][1]
                return [(-b, 0.0), (0.0, b)]
            return allowed(E)

        def region_axis():
            rg = T.RG.get_value()
            if rg <= 0.001:
                return VGroup()
            g = VGroup()
            for iv in ivs(T.E.get_value()):
                op = rg * dimf(iv[0])
                if iv[1] - iv[0] > 0.03:
                    g.add(seg((gx(iv[0]), PY), (gx(iv[1]), PY), stroke_width=9, color=BLUE).set_opacity(op))
                else:
                    g.add(Circle(radius=0.16, color=BLUE, stroke_width=4).move_to([gx(iv[0]), PY, 0])
                          .set_stroke(opacity=op))
            fb = T.FB.get_value()
            if fb > 0.001 and T.E.get_value() < 1 - 1e-9:
                a = allowed(T.E.get_value())[1][0]
                g.add(DashedLine([gx(-a), PY, 0], [gx(a), PY, 0], color=MAGENTA, stroke_width=4, dash_length=0.12)
                      .set_opacity(0.85 * fb * rg))
            return g

        def projections():
            rg = T.RG.get_value()
            if rg <= 0.001:
                return VGroup()
            E = T.E.get_value()
            g = VGroup()
            for xe in turning_points(E):
                if E >= 1 - 1e-9 and abs(xe) < 1e-6:
                    continue
                g.add(DashedLine([gx(xe), gy(E) - 0.1, 0], [gx(xe), PY + 0.1, 0], color=BLUE_L, stroke_width=1.5,
                                 dash_length=0.05).set_opacity(0.3 * rg * dimf(xe)))
            return g

        def turning():
            rg = T.RG.get_value()
            if rg <= 0.001:
                return VGroup()
            E = T.E.get_value()
            xp = self.xp() if T.VP.get_value() > 0.01 else 99.0
            g = VGroup()
            for xr in turning_points(E):
                if E >= 1 - 1e-9 and abs(xr) < 1e-6:
                    continue
                near = max(0.0, 1 - abs(xp - xr) / 0.1)
                g.add(Dot([gx(xr), gy(E), 0], radius=0.09 + 0.05 * near, color=BLUE_L).set_opacity(rg * dimf(xr))
                      .set_z_index(3))
            return g

        self.region_axis = always_redraw(region_axis)
        self.projections = always_redraw(projections)
        self.turning = always_redraw(turning)

        # Partícula (só no eixo espacial), barra K = E − U na posição atual e rótulo fixo
        def particle():
            vp = T.VP.get_value()
            if vp <= 0.001:
                return VGroup()
            x = self.xp()
            return VGroup(Dot([gx(x), PY, 0], radius=0.19, color=WHITE).set_opacity(0.18 * vp),
                          Dot([gx(x), PY, 0], radius=0.09, color=WHITE).set_opacity(vp)).set_z_index(5)

        def kbar():
            kb = T.KB.get_value()
            if kb <= 0.001 or T.VP.get_value() <= 0.01:
                return VGroup()
            x, E = self.xp(), T.E.get_value()
            g = VGroup(DashedLine([gx(x), PY + 0.14, 0], [gx(x), gy(E), 0], color=WHITE, stroke_width=1.6,
                                  dash_length=0.1).set_opacity(0.45 * kb))
            g.add(kseg(x, E, kb))
            return g

        def cursor():
            cv = T.CV.get_value()
            if cv <= 0.001:
                return VGroup()
            x, E = T.CS.get_value(), T.E.get_value()
            return VGroup(
                DashedLine([gx(x), PY + 0.12, 0], [gx(x), gy(u(x)), 0], color=KCOL, stroke_width=1.6,
                           dash_length=0.1).set_opacity(0.4 * cv),
                Circle(radius=0.1, color=KCOL, stroke_width=3.5).move_to([gx(x), PY, 0]).set_stroke(opacity=cv),
                Dot([gx(x), gy(u(x)), 0], radius=0.07, color=KCOL).set_opacity(cv).set_z_index(4),
                kseg(x, E, cv))

        self.particle = always_redraw(particle)
        self.kbar = always_redraw(kbar)
        self.cursor = always_redraw(cursor)
        self.k_lab = mt("K", "=", "E", "-", "U(x)", size=34, colors={0: KCOL, 2: BLUE_L, 4: VIOLET}, maxw=3.0)
        self.k_lab.move_to([0, -3.5, 0])
        self.k_lab.add_updater(lambda m: m.set_opacity(T.KL.get_value()))

        # Coda: paisagem de energia (analogia)
        pts = [gpt(x) for x in np.linspace(-XR, XR, 161)]
        self.land = VMobject(stroke_width=0, fill_color=VIOLET, fill_opacity=0.2)
        self.land.set_points_as_corners(pts + [np.array([gx(XR), GY0, 0]), np.array([gx(-XR), GY0, 0]), pts[0]])
        self.ball = always_redraw(lambda: Circle(radius=0.15, color=VIOLET, stroke_width=4)
                                  .move_to(gpt(self.xp()) + UP * 0.15).set_stroke(opacity=T.BALL.get_value())
                                  if T.BALL.get_value() > 0.001 else VGroup())
        self.link = always_redraw(lambda: DashedLine([gx(self.xp()), PY + 0.14, 0], [gx(self.xp()), gpt(self.xp())[1], 0],
                                                     color=VIOLET, stroke_width=1.6, dash_length=0.1)
                                  .set_opacity(0.4 * T.BALL.get_value()) if T.BALL.get_value() > 0.001 else VGroup())

    # ── Execução ────────────────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.build()
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(self.wm.to_corner(UP + RIGHT, buff=0.28))
        self.series = text("DA EQUAÇÃO AO FENÔMENO · EP. 04", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4)
        self.add(self.series)
        for k, fn in enumerate([self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8], 1):
            fn()
            self.mark(f"fim S{k}")
            if k >= ATE:
                self.wait(0.5)
                return
        self.wait(1.0)

    # ── S1 Força dada, zeros, curva, sinais ─────────────────────────────────
    def s1(self):
        hd = lines("PRESA DE UM LADO", "OU ATRAVESSA?", size=38).move_to([0, 6.2, 0])
        sub = mixed(text("Sem resolver", 28), tex(r"x(t)?", 34)).move_to([0, 5.1, 0])
        self.hd = hd
        # partícula e eixo espacial simples (ela já fica na região 0 < x < ℓ, onde a força será lida)
        d0 = self.f_states[2][0]
        ax0 = Line([-3.4, FY0, 0], [3.4, FY0, 0], stroke_width=2.5, color=WHITE).set_opacity(0.55)
        xl0 = tex("x", 30).move_to([3.3, FY0 - 0.35, 0])
        self.play(FadeIn(hd, shift=DOWN * 0.15), run_time=1.0)
        self.play(FadeIn(ax0), FadeIn(xl0), FadeIn(d0, scale=0.5), run_time=1.0)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=1.0)
        self.wait(1.0)
        cap = text("a força é um dado do problema", 26, opacity=0.85).move_to([0, 5.1, 0])
        f_top = mt("F(x)", "=", "F_0", r"\left[\frac{x}{\ell}-\left(\frac{x}{\ell}\right)^3\right]", size=44,
                   colors={0: CYAN}, maxw=7.2).move_to([0, 4.15, 0])
        self.play(soft_swap(sub, cap), FadeIn(f_top, shift=UP * 0.1), run_time=1.4)
        self.mark("forca dada")
        self.wait(1.0)
        # zeros
        self.play(FadeOut(cap), FadeOut(ax0), FadeOut(xl0), FadeIn(self.f_axis), FadeIn(self.f_x),
                  FadeIn(self.f_vaxis), FadeIn(self.f_vlab), run_time=1.0)
        z1 = mt("F(x)", r"=0\;\Rightarrow\;", r"\frac{x}{\ell}\left[1-\left(\frac{x}{\ell}\right)^2\right]", "=0",
                size=34, colors={0: CYAN}).move_to([0, 3.2, 0])
        z2 = mt("x", "=", r"-\ell,\;0,\;+\ell", size=42).move_to([0, 2.35, 0])
        self.play(FadeIn(z1, shift=UP * 0.1), run_time=1.8)
        self.wait(0.6)
        self.play(FadeIn(z2, shift=UP * 0.1), run_time=1.2)
        self.play(AnimationGroup(*(FadeIn(d, scale=0.4) for d in self.f_zeros), lag_ratio=0.3),
                  FadeIn(self.f_ticks), z1.animate.set_opacity(0.45), run_time=1.5)
        self.mark("zeros")
        # curva
        self.play(Create(self.f_curve), FadeOut(f_top), run_time=3.0, rate_func=smooth)
        self.play(FadeOut(z1), FadeOut(z2), run_time=0.5)
        # sinal da força e setas: a partícula em cada região, com a força sobre ela
        for k, st in enumerate(self.f_states):
            anims = [FadeIn(st[1], shift=st[1].get_vector() * 0.25), FadeIn(st[2])]
            if k != 2:
                anims.append(FadeIn(st[0], scale=0.5))
            self.play(*anims, run_time=0.8)
            self.wait(0.5)
        self.mark("setas")
        conv = mixed(text("a força converge para", 24, opacity=0.9), tex(r"\pm\ell", 30),
                     text("e afasta de", 24, opacity=0.9), tex("0", 30)).move_to([0, -3.3, 0])
        self.play(FadeIn(conv, shift=UP * 0.1), run_time=1.0)
        self.wait(1.2)
        bridge = text("Que energia produz essa força?", 28).move_to([0, -3.3, 0])
        self.play(soft_swap(conv, bridge), run_time=1.2)
        self.wait(1.5)
        self.s1_all = VGroup(self.f_axis, self.f_x, self.f_vaxis, self.f_vlab, self.f_curve, self.f_zeros,
                             self.f_ticks, *self.f_states, bridge)

    # ── S2 Integração acompanhável ──────────────────────────────────────────
    def s2(self):
        ref = mt("F(x)", "=", "F_0", r"\left[\frac{x}{\ell}-\left(\frac{x}{\ell}\right)^3\right]", size=44,
                 colors={0: CYAN}, maxw=7.2).move_to([0, 4.15, 0])
        self.play(FadeOut(self.s1_all), FadeOut(self.hd), FadeIn(ref), run_time=1.2)
        self.play(ref.animate.scale(0.72).move_to([0, 5.4, 0]), run_time=0.8)
        Y = 2.5
        sz = 52
        m1 = mt("F(x)", "=", "-", "U'(x)", size=64, colors={0: CYAN, 3: VIOLET}).move_to([0, Y, 0])
        self.play(FadeIn(m1, shift=UP * 0.1), run_time=1.4)
        self.wait(0.6)
        m2 = mt("U(x)", "=", "-", r"\int", "F(x)", r"\,dx", size=sz, colors={0: VIOLET, 4: CYAN}).move_to([0, Y, 0])
        self.play(TransformMatchingTex(m1, m2, transform_mismatches=True), run_time=1.8)
        self.wait(0.6)
        m2b = mt("U(x)", "=", "-", "F_0", r"\int", r"\Big[\frac{x}{\ell}-\frac{x^3}{\ell^3}\Big]", r"\,dx", size=sz,
                 colors={0: VIOLET, 5: CYAN}).move_to([0, Y, 0])
        self.play(Indicate(ref, color=CYAN, scale_factor=1.04),
                  TransformMatchingTex(m2, m2b, transform_mismatches=True), run_time=2.2)
        self.wait(0.5)
        P3 = ["U(x)", "=", "-", "F_0", r"\Big[", r"\frac{1}{\ell}", r"\int x\,dx", "-", r"\frac{1}{\ell^3}",
              r"\int x^3\,dx", r"\Big]", "+C"]
        m3 = mt(*P3, size=sz, colors={0: VIOLET}).move_to([0, Y, 0])
        self.play(TransformMatchingTex(m2b, m3, transform_mismatches=True), run_time=2.4)
        self.mark("integral separada")
        self.play(Indicate(m3[5], color=BLUE_L), Indicate(m3[8], color=BLUE_L), run_time=1.0)
        # x -> x²/2 e x³ -> x⁴/4, um de cada vez; os fatores 1/ℓ e 1/ℓ³ permanecem
        h1 = tex(r"\int x\,dx=\frac{x^2}{2}", 40).move_to([0, 0.2, 0])
        self.play(FadeIn(h1, shift=UP * 0.1), run_time=0.7)
        P3b = list(P3)
        P3b[6] = r"\frac{x^2}{2}"
        m3b = mt(*P3b, size=sz, colors={0: VIOLET}).move_to([0, Y, 0])
        self.play(TransformMatchingTex(m3, m3b, transform_mismatches=True), run_time=1.6)
        self.wait(0.4)
        h2 = tex(r"\int x^3\,dx=\frac{x^4}{4}", 40).move_to([0, 0.2, 0])
        self.play(soft_swap(h1, h2), run_time=0.9)
        P3c = list(P3b)
        P3c[9] = r"\frac{x^4}{4}"
        m3c = mt(*P3c, size=sz, colors={0: VIOLET}).move_to([0, Y, 0])
        self.play(TransformMatchingTex(m3b, m3c, transform_mismatches=True), run_time=1.6)
        self.wait(0.4)
        self.play(FadeOut(h2), run_time=0.5)
        m4 = mt("U(x)", "=", "-", "F_0", r"\Big[", r"\frac{x^2}{2\ell}", "-", r"\frac{x^4}{4\ell^3}", r"\Big]", "+C",
                size=sz, colors={0: VIOLET}).move_to([0, Y, 0])
        self.play(TransformMatchingTex(m3c, m4, transform_mismatches=True), run_time=2.0)
        self.mark("integrado")
        self.wait(0.5)
        h3 = text("o sinal negativo distribui pelos dois termos", 24, opacity=0.9).move_to([0, 0.4, 0])
        m4b = mt("U(x)", "=", r"-F_0\frac{x^2}{2\ell}", r"+F_0\frac{x^4}{4\ell^3}", "+C", size=sz,
                 colors={0: VIOLET}).move_to([0, Y, 0])
        self.play(FadeIn(h3, shift=UP * 0.1), TransformMatchingTex(m4, m4b, transform_mismatches=True), run_time=2.4)
        self.wait(0.4)
        m5 = mt("U(x)", "=", "-", r"\frac{F_0x^2}{2\ell}", "+", r"\frac{F_0x^4}{4\ell^3}", "+", "C", size=sz,
                colors={0: VIOLET}).move_to([0, Y, 0])
        self.play(FadeOut(h3), TransformMatchingTex(m4b, m5, transform_mismatches=True), run_time=1.6)
        self.wait(0.6)
        self.ref, self.m5 = ref, m5

    # ── S3 Escolha de C ─────────────────────────────────────────────────────
    def s3(self):
        m5, ref = self.m5, self.ref
        self.play(FadeOut(ref), m5.animate.scale(0.82).move_to([0, 5.0, 0]), run_time=1.0)
        t1 = VGroup(text("Escolhemos o zero de energia", 28), text("nos mínimos.", 28)).arrange(DOWN, buff=0.12)
        t1.move_to([0, 3.65, 0])
        c1 = mt("U(", r"\pm\ell", ")", "=", "0", size=54, colors={0: VIOLET, 2: VIOLET}).move_to([0, 2.3, 0])
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=1.2)
        self.wait(0.5)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=1.2)
        self.wait(0.8)
        t2 = mixed(text("pela simetria, basta substituir", 24, opacity=0.9), tex(r"x=\ell", 32)).move_to([0, 1.35, 0])
        self.play(FadeIn(t2, shift=UP * 0.1), Indicate(m5, color=WHITE, scale_factor=1.03), run_time=1.2)
        la = mt("0", "=", r"U(\ell)", "=", r"-\frac{F_0\ell^2}{2\ell}", r"+\frac{F_0\ell^4}{4\ell^3}", "+C", size=44,
                colors={2: VIOLET}).move_to([0, 0.15, 0])
        self.play(FadeIn(la, shift=UP * 0.1), run_time=1.6)
        self.wait(0.6)
        lb = mt("0", "=", r"-\frac{F_0\ell}{2}", r"+\frac{F_0\ell}{4}", "+C", size=48).move_to([0, 0.15, 0])
        self.play(TransformMatchingTex(la, lb, transform_mismatches=True), run_time=1.8)
        self.wait(0.6)
        lc = mt("0", "=", r"-\frac{F_0\ell}{4}", "+C", size=52).move_to([0, 0.15, 0])
        self.play(TransformMatchingTex(lb, lc, transform_mismatches=True), run_time=1.8)
        self.wait(0.4)
        box = mt("C", "=", r"\frac{F_0\ell}{4}", size=60, colors={0: MAGENTA, 2: MAGENTA}).move_to([0, -1.6, 0])
        bx = SurroundingRectangle(box, color=MAGENTA, buff=0.2, corner_radius=0.1, stroke_width=3)
        self.play(TransformMatchingTex(lc.copy(), box, transform_mismatches=True), Create(bx), run_time=1.8)
        self.mark("C")
        note = VGroup(text("C só define a referência de energia;", 24, opacity=0.9),
                      text("a força não muda.", 24, opacity=0.9)).arrange(DOWN, buff=0.1).move_to([0, -3.1, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=1.0)
        self.wait(1.4)
        self.s3_all = VGroup(t1, c1, t2, lc, note)
        self.box, self.bx = box, bx

    # ── S4 Fatoração e conferência ──────────────────────────────────────────
    def s4(self):
        m5, box, bx = self.m5, self.box, self.bx
        self.play(FadeOut(self.s3_all), run_time=0.8)
        Y = 2.9
        m5b = mt("U(x)", "=", "-", r"\frac{F_0x^2}{2\ell}", "+", r"\frac{F_0x^4}{4\ell^3}", "+", r"\frac{F_0\ell}{4}",
                 size=43, colors={0: VIOLET, 7: MAGENTA}).move_to(m5)
        self.play(TransformMatchingTex(m5, m5b, transform_mismatches=True), FadeOut(bx), FadeOut(box), run_time=2.0)
        self.wait(0.4)
        m6 = mt("U(x)", "=", r"\frac{F_0x^4}{4\ell^3}", "-", r"\frac{F_0x^2}{2\ell}", "+", r"\frac{F_0\ell}{4}", size=52,
                colors={0: VIOLET, 6: MAGENTA}).move_to([0, Y, 0])
        self.play(TransformMatchingTex(m5b, m6, transform_mismatches=True), run_time=2.0)
        self.wait(0.5)
        m7 = mt("U(x)", "=", r"\frac{F_0\ell}{4}", r"\left[\left(\frac{x}{\ell}\right)^4-2\left(\frac{x}{\ell}\right)^2+1\right]",
                size=52, colors={0: VIOLET, 2: MAGENTA}).move_to([0, Y, 0])
        self.play(TransformMatchingTex(m6, m7, transform_mismatches=True), run_time=2.4)
        self.wait(0.7)
        m8 = mt("U(x)", "=", r"\frac{F_0\ell}{4}", r"\left[\left(\frac{x}{\ell}\right)^2-1\right]^2", size=56,
                colors={0: VIOLET, 2: MAGENTA}).move_to([0, Y, 0])
        self.play(TransformMatchingTex(m7, m8, transform_mismatches=True), run_time=2.2)
        chk = mixed(text("confere:", 26, opacity=0.9), mt("-", "U'(x)", "=", "F(x)", size=44, colors={1: VIOLET, 3: CYAN}))
        chk.move_to([0, 0.8, 0])
        self.play(FadeIn(chk, shift=UP * 0.1), run_time=1.2)
        self.wait(1.2)
        self.play(FadeOut(chk), m8.animate.scale(0.7).move_to([0, 5.2, 0]), run_time=1.0)
        self.m8 = m8

    # ── S5 Gráfico do potencial e classificação ─────────────────────────────
    def s5(self):
        # a troca do eixo vertical: de força (F) para energia (U)
        hint = mixed(text("novo gráfico: o eixo vertical é", 24, opacity=0.9), text("energia", 24, VIOLET)).move_to([0, 4.2, 0])
        self.play(FadeIn(self.u_axis), FadeIn(self.u_label), FadeIn(self.base), FadeIn(self.base_x),
                  FadeIn(self.base_ticks), FadeIn(hint, shift=UP * 0.1), run_time=1.4)
        self.wait(0.5)
        # pontos calculados: mínimos em ±ℓ (U = 0) e centro em U_b
        l_w = VGroup(tex(r"U(-\ell)=0", 30, VIOLET).move_to([gx(-1), GY0 - 1.0, 0]),
                     tex(r"U(\ell)=0", 30, VIOLET).move_to([gx(1), GY0 - 1.0, 0]))
        l_b = tex(r"U(0)=\frac{F_0\ell}{4}=U_b", 32, MAGENTA).move_to([0, gy(1) + 0.85, 0])
        self.play(FadeIn(self.well_dots, scale=0.4), FadeIn(l_w, shift=UP * 0.1), run_time=1.2)
        self.play(FadeIn(self.ub_level), FadeIn(self.ub_dot, scale=0.4), FadeIn(self.ub_tick),
                  FadeIn(l_b, shift=DOWN * 0.1), run_time=1.3)
        self.mark("pontos U")

        def piece(a, b, n=40):
            return VMobject(color=VIOLET, stroke_width=5).set_points_smoothly(
                [gpt(x) for x in np.linspace(a, b, n)])

        # a curva cresce dos mínimos: poços, barreira central e extremidades que sobem
        p_w = VGroup(piece(-1.3, -0.7), piece(0.7, 1.3))
        p_b = piece(-0.7, 0.7, 60)
        p_e = VGroup(piece(-XR, -1.3), piece(1.3, XR))
        self.play(Create(p_w), run_time=1.2)
        self.play(Create(p_b), run_time=1.2)
        self.play(Create(p_e), FadeIn(self.u_name), FadeOut(hint), run_time=1.2)
        self.remove(p_w, p_b, p_e)
        self.add(self.u_curve)
        self.mark("curva U")
        self.wait(0.4)

        # classificação: centro (instável) e mínimos (estáveis), com as setas de força já vistas
        def arc(x0, col):
            d2 = d2u(x0)
            return VMobject(color=col, stroke_width=3.5).set_points_smoothly(
                [np.array([gx(x0 + dx), gy(u(x0) + 0.5 * d2 * dx * dx), 0]) for dx in np.linspace(-0.28, 0.28, 25)])

        def farrow(x0, direc):
            cx = gx(x0)
            return Arrow([cx - 0.3 * direc, GY0, 0], [cx + 0.3 * direc, GY0, 0], buff=0, color=CYAN, stroke_width=5,
                         max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=10).set_z_index(4)

        a0 = tex(r"U''(0)=-\frac{F_0}{\ell}<0", 32, MAGENTA).move_to([0, gy(1) + 0.85, 0])
        st0 = text("instável", 26, MAGENTA).move_to([0, gy(1) + 1.5, 0])
        arc0 = arc(0, MAGENTA)
        fa0 = VGroup(farrow(-0.3, -1), farrow(0.3, 1))
        self.play(FadeOut(l_b), FadeIn(arc0), FadeIn(fa0), FadeIn(a0, shift=UP * 0.1), FadeIn(st0, shift=UP * 0.1),
                  run_time=1.4)
        self.wait(1.2)
        aw = tex(r"U''(\pm\ell)=\frac{2F_0}{\ell}>0", 32, VIOLET).move_to([0, GY0 - 1.15, 0])
        stw = VGroup(text("estável", 26, VIOLET).move_to([gx(-1), GY0 - 1.8, 0]),
                     text("estável", 26, VIOLET).move_to([gx(1), GY0 - 1.8, 0]))
        arcw = VGroup(arc(-1, WHITE), arc(1, WHITE))
        faw = VGroup(farrow(-1.35, 1), farrow(-0.7, -1), farrow(0.7, 1), farrow(1.35, -1))   # convergem para ±ℓ
        self.play(FadeOut(l_w), FadeIn(arcw), FadeIn(faw), FadeIn(aw, shift=UP * 0.1), FadeIn(stw, shift=UP * 0.1),
                  run_time=1.4)
        self.wait(1.4)
        self.play(FadeOut(VGroup(arc0, fa0, a0, st0, aw, stw, arcw, faw)), FadeOut(self.base_ticks),
                  FadeOut(self.well_dots), FadeOut(self.base_x), FadeOut(self.m8), run_time=1.0)

    # ── S6 Energia e leitura de K ───────────────────────────────────────────
    def s6(self):
        T = self.T
        c1 = mt("E", "=", "K", "+", "U", size=46, colors={0: BLUE_L, 4: VIOLET}).move_to([0, 5.6, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=1.2)
        self.wait(0.8)
        c2 = mt("K", "=", "E", "-", "U", r"\ge 0", size=46, colors={2: BLUE_L, 4: VIOLET}).move_to([0, 4.8, 0])
        self.play(TransformMatchingTex(c1.copy(), c2), run_time=1.6)
        self.wait(0.8)
        c3 = mt("U(x)", r"\le", "E", size=52, colors={0: VIOLET, 2: BLUE_L}).move_to([0, 4.0, 0])
        box = SurroundingRectangle(c3, color=BLUE_L, buff=0.2, corner_radius=0.08, stroke_width=2.5)
        self.play(FadeIn(c3, shift=UP * 0.1), Create(box), c1.animate.set_opacity(0.5), c2.animate.set_opacity(0.5),
                  run_time=1.6)
        self.c_chain, self.c_box = VGroup(c1, c2, c3), box
        self.wait(0.8)
        # a linha E nasce da desigualdade: o "E" da caixa viaja até o fim da linha
        cp = c3[2].copy()
        T.E.set_value(E_SUB)
        self.add(self.eline, self.e_lab)
        self.play(cp.animate.scale(0.65).move_to([AXR + 0.2, gy(E_SUB) + 0.3, 0]), T.LA.animate.set_value(1),
                  run_time=2.2, rate_func=smooth)
        self.remove(cp)
        self.add(self.region_axis, self.projections, self.turning, self.particle, self.kbar, self.cursor, self.k_lab,
                 self.ball, self.link)
        self.mark("linha E")
        # leitura de K com um cursor sobre o eixo espacial (não é a partícula)
        T.CS.set_value(1.15)
        self.play(FadeOut(self.u_name), FadeIn(self.p_group), run_time=0.8)
        self.play(T.CV.animate.set_value(1), T.KL.animate.set_value(1), run_time=1.0)
        n1 = mixed(tex(r"U<E", 32, BLUE_L), text("→", 26), tex(r"K>0", 32, KCOL),
                   text("posição permitida", 26, opacity=0.9)).move_to([0, -4.15, 0])
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.8)
        self.wait(1.2)
        b = float(allowed(E_SUB)[1][1])
        self.play(T.CS.animate.set_value(b), run_time=2.4, rate_func=smooth)
        n2 = mixed(tex(r"U=E", 32, BLUE_L), text("→", 26), tex(r"K=0", 32, KCOL),
                   text("ponto de retorno", 26, opacity=0.9)).move_to([0, -4.15, 0])
        self.play(soft_swap(n1, n2), run_time=0.9)
        self.wait(1.6)
        self.play(T.CV.animate.set_value(0), run_time=0.5)
        T.CS.set_value(0.3)
        n3 = mixed(tex(r"U>E", 32, BLUE_L), text("→ posição proibida", 26, opacity=0.9)).move_to([0, -4.15, 0])
        self.play(T.CV.animate.set_value(1), soft_swap(n2, n3), run_time=1.0)
        self.wait(2.0)
        self.play(T.CV.animate.set_value(0), FadeOut(n3), run_time=0.6)
        # conjunto permitido no eixo espacial
        n4 = text("as posições com K ≥ 0 formam o conjunto permitido", 24, opacity=0.9).move_to([0, -4.15, 0])
        self.play(T.RG.animate.set_value(1), FadeIn(n4, shift=UP * 0.1), run_time=1.4)
        self.wait(1.8)
        self.play(FadeOut(n4), run_time=0.5)

    # ── S7 Regimes ──────────────────────────────────────────────────────────
    def regime_in(self, E, traj, dl, lab, cap):
        """Nova condição inicial: retira a partícula e o nível anteriores, muda E, mostra o novo nível e a partícula."""
        T = self.T
        self.play(T.VP.animate.set_value(0), T.KB.animate.set_value(0), T.RG.animate.set_value(0),
                  T.LA.animate.set_value(0), T.FB.animate.set_value(0), run_time=0.6)
        T.E.set_value(E)
        T.DL.set_value(dl)
        self.traj = traj
        T.TT.set_value(0)
        self.play(T.LA.animate.set_value(1), T.RG.animate.set_value(1), FadeIn(lab, shift=UP * 0.1),
                  FadeIn(cap, shift=UP * 0.1), run_time=0.8)
        self.play(T.VP.animate.set_value(1), T.KB.animate.set_value(1), run_time=0.7)

    def s7(self):
        T = self.T
        # E = 0 ---------------------------------------------------------------------------------------------
        lab0 = mt("E", "=", "0", size=58, colors={0: BLUE_L}).move_to([0, 5.3, 0])
        cap0 = text("repouso em um dos mínimos", 26, opacity=0.9).move_to([0, 4.45, 0])
        self.play(FadeOut(self.c_chain), FadeOut(self.c_box), T.RG.animate.set_value(0), run_time=0.8)
        self.regime_in(0.0, traj_rest, 0.0, lab0, cap0)
        self.wait(2.5)
        # 0 < E < U_b -----------------------------------------------------------------------------------------
        lab1 = mt("0", "<", "E", "<", "U_b", size=58, colors={2: BLUE_L, 4: MAGENTA}).move_to([0, 5.3, 0])
        cap1 = text("movimento confinado a um único poço", 26, opacity=0.9).move_to([0, 4.45, 0])
        self.play(FadeOut(VGroup(lab0, cap0)), run_time=0.4)
        self.regime_in(E_SUB, traj_sub, 1.0, lab1, cap1)
        self.mark("sub-barreira")
        note = text("nos retornos, K = 0", 24, opacity=0.9).move_to([0, -4.15, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.5)
        self.play(T.TT.animate.set_value(1.1), run_time=1.1, rate_func=linear)
        n_b = text("no mínimo, K é máximo: maior rapidez", 24, opacity=0.9).move_to([0, -4.15, 0])
        self.play(soft_swap(note, n_b), run_time=0.5)
        self.play(T.TT.animate.set_value(2.8), run_time=1.7, rate_func=linear)
        n_c = text("o centro é proibido: U > E", 24, opacity=0.9).move_to([0, -4.15, 0])
        self.play(soft_swap(n_b, n_c), T.FB.animate.set_value(1), run_time=0.5)
        self.play(T.TT.animate.set_value(5.6), run_time=2.8, rate_func=linear)
        self.play(T.TT.animate.set_value(6.5), FadeOut(n_c), run_time=0.9, rate_func=linear)
        # E = U_b -----------------------------------------------------------------------------------------------
        lab2 = mt("E", "=", "U_b", size=58, colors={0: BLUE_L, 2: MAGENTA}).move_to([0, 5.3, 0])
        cap2 = mixed(text("aproxima-se de", 26, opacity=0.9), tex("x=0", 32), text("sem chegar", 26, opacity=0.9)
                     ).move_to([0, 4.45, 0])
        self.play(FadeOut(VGroup(lab1, cap1)), T.FB.animate.set_value(0), run_time=0.4)
        self.regime_in(E_SEP, traj_sep, 1.0, lab2, cap2)
        self.mark("separatriz")
        self.play(T.TT.animate.set_value(3.0), run_time=3.0, rate_func=linear)
        lim = mt(r"x\to0", r",\quad", r"K\to0", r",\quad", r"t\to\infty", size=38).move_to([0, -4.15, 0])
        self.play(FadeIn(lim, shift=UP * 0.1), T.TT.animate.set_value(4.6), run_time=1.6, rate_func=linear)
        self.play(T.TT.animate.set_value(5.2), run_time=0.6, rate_func=linear)
        self.mark("separatriz fim")
        # E > U_b -----------------------------------------------------------------------------------------------
        lab3 = mt("E", ">", "U_b", size=58, colors={0: BLUE_L, 2: MAGENTA}).move_to([0, 5.3, 0])
        cap3 = mixed(text("atravessa", 26, opacity=0.9), tex("x=0", 32), text("e volta nos extremos", 26, opacity=0.9)
                     ).move_to([0, 4.45, 0])
        self.play(FadeOut(VGroup(lab2, cap2)), FadeOut(lim), run_time=0.4)
        self.regime_in(E_SUP, traj_sup, 0.0, lab3, cap3)
        self.mark("travessia")
        self.play(T.TT.animate.set_value(2.6), run_time=2.6, rate_func=linear)
        n_d = text("K > 0 em x = 0: atravessa a barreira", 24, opacity=0.9).move_to([0, -4.15, 0])
        self.play(FadeIn(n_d, shift=UP * 0.1), T.TT.animate.set_value(3.6), run_time=1.0, rate_func=linear)
        self.play(T.TT.animate.set_value(5.3), run_time=1.7, rate_func=linear)
        n_e = text("U cresce nos extremos: o movimento é limitado", 24, opacity=0.9).move_to([0, -4.15, 0])
        self.play(soft_swap(n_d, n_e), T.TT.animate.set_value(5.7), run_time=0.8, rate_func=linear)
        self.mark("retorno externo")
        self.s7_cleanup = VGroup(lab3, cap3, n_e)

    # ── S8 Coda ─────────────────────────────────────────────────────────────
    def s8(self):
        T = self.T
        title = display("PAISAGEM DE ENERGIA", 36).move_to([0, 5.5, 0])
        chip_t = text("ANALOGIA", 22, MAGENTA)
        chip = SurroundingRectangle(chip_t, color=MAGENTA, buff=0.16, corner_radius=0.12, stroke_width=2.5)
        chip_g = VGroup(chip, chip_t).move_to([0, 4.8, 0])
        # a trajetória continua (sem reiniciar): a linha E e a barra K saem, a partícula real permanece
        # no eixo x e o marcador da analogia nasce na vertical da partícula, sobre a curva
        self.play(soft_swap(self.s7_cleanup, VGroup(title, chip_g)),
                  T.LA.animate.set_value(0), T.RG.animate.set_value(0), T.KB.animate.set_value(0),
                  T.KL.animate.set_value(0), T.VP.animate.set_value(0.6), FadeIn(self.land),
                  T.TT.animate.set_value(6.7), run_time=1.6, rate_func=linear)
        self.play(T.BALL.animate.set_value(1), T.TT.animate.set_value(7.4), run_time=0.7, rate_func=linear)
        note = text("O eixo vertical representa energia.", 26, opacity=0.9).move_to([0, -3.5, 0])
        self.play(FadeIn(note, shift=UP * 0.1), T.TT.animate.set_value(9.2), run_time=1.8, rate_func=linear)
        ans = VGroup(mixed(text("presa de um lado se", 26), tex(r"E<U_b", 32, BLUE_L)),
                     mixed(text("atravessa se", 26), tex(r"E>U_b", 32, BLUE_L))).arrange(DOWN, buff=0.2).move_to([0, 4.0, 0])
        self.play(FadeOut(chip_g), FadeIn(ans, shift=UP * 0.1), T.TT.animate.set_value(11.0), run_time=1.8,
                  rate_func=linear)
        self.wait(1.2)
