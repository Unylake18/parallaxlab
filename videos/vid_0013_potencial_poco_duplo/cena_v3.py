"""Potencial de poço duplo a partir da força F(x) = F0 [x/ℓ − (x/ℓ)³]: preview silencioso (V3).

DA EQUAÇÃO AO FENÔMENO · EP. 04. Pergunta: "PRESA DE UM LADO OU ATRAVESSA?" (sem resolver x(t)).

Cadeia: força dada -> construção do gráfico de F -> integração -> referência de energia (C) -> potencial
-> forma de U demonstrada -> posições permitidas (K = E − U ≥ 0) -> regimes -> coda (analogia).

  S1  força dada, zeros, sinais por região (um marcador de análise), F(ℓ/2) = 3F0/8, F(−x) = −F(x),
      curva traçada por um cursor (x, F(x)) e completada pela simetria
  S2  F = −U′ -> U = −∫F dx -> integral aplicada a cada termo -> 1/ℓ e 1/ℓ³ fora -> primitivas -> frações -> sinal
  S3  U(±ℓ) = 0 -> substituir x = ℓ -> simplificar -> C = F0ℓ/4
  S4  substituir C -> reordenar -> retirar F0ℓ/4 por termos -> a² − 2a + 1 = (a − 1)²
  S5  forma de U: U′ = −F (inclinações), zeros de F = tangentes horizontais, pontos U(±ℓ), U(0), U(ℓ/2) = 9U_b/16,
      U(−x) = U(x), cursor (x, U(x)), crescimento externo; classificação por U″
  S6  E = K + U -> K = E − U ≥ 0 -> U ≤ E; linha E; cursor de leitura de K
  S7  regimes (cada E é uma nova condição inicial) com destaques sincronizados ao tempo da trajetória
  S8  coda: paisagem de energia (analogia) e recapitulação dos regimes

Gráfico de energia adimensional: x em unidades de ℓ, U em unidades de U_b = F0ℓ/4: u(x) = (x² − 1)².
Dinâmica: ẍ = −κ u′(x) (m = 1), κ = 0,2, RK4 nos regimes limitados; a separatriz usa a solução exata
√2 sech(a t), com a = 2√κ·s (s = fator de apresentação em câmera lenta); nenhuma x(t) aparece no vídeo.
Equações: linhas alinhadas à esquerda, uma operação por vez; termos mantidos só deslizam (ReplacementTransform),
termos dispensados saem antes de os novos entrarem (FadeOut/FadeIn), sem `transform_mismatches`.

`ATE=k` (1–8) renderiza só até o segmento k.
"""

import os
import sys
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from manim import (
    DOWN, LEFT, PI, RIGHT, UP, AnimationGroup, Arrow, Circle, Create, DashedLine, Dot, FadeIn, FadeOut, ImageMobject,
    Indicate, Line, MathTex, ReplacementTransform, Rotate, Scene, SurroundingRectangle, TransformFromCopy, VGroup,
    VMobject, ValueTracker, always_redraw, config, linear, smooth,
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
S_SEP = 0.6               # a separatriz é exibida a 0,6× (reparametrização da apresentação)
A_SEP = 2 * np.sqrt(KAPPA) * S_SEP
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
_TS_SUP, _XS_SUP, _VS_SUP = _rk4(-allowed(E_SUP)[0][1], 0.0, 26.0)


def traj_rest(t):
    return 1.0


def traj_sub(t):
    return float(np.interp(t, _TS_SUB, _XS_SUB))


def traj_sep(t):
    return float(np.sqrt(2.0) / np.cosh(A_SEP * t))


def traj_sup(t):
    return float(np.interp(t, _TS_SUP, _XS_SUP))


def _cross(ts, arr, level=0.0):
    """Instantes (t > 0) em que arr cruza `level`."""
    d = arr - level
    idx = np.where(d[:-1] * d[1:] < 0)[0]
    return ts[idx + 1]


# eventos físicos das trajetórias (para sincronizar destaques): retornos (v = 0) e passagens por x = 1 / x = 0
SUB_TP = _cross(_TS_SUB, _VS_SUB)             # retornos do poço ocupado
SUB_MIN = _cross(_TS_SUB, _XS_SUB, 1.0)       # passagens pelo mínimo (x = ℓ)
SUP_TP = _cross(_TS_SUP, _VS_SUP)             # retornos externos
SUP_CEN = _cross(_TS_SUP, _XS_SUP, 0.0)       # travessias do centro


def _qa():
    """Verificações numéricas independentes do modelo (roda ao importar)."""
    xs = np.linspace(-1.6, 1.6, 321)
    h = 1e-6
    # F = −U′: F = F0[x/ℓ − (x/ℓ)³] e U = (F0ℓ/4)[(x/ℓ)² − 1]²  (em unidades F0 e ℓ: U/(F0 ℓ) = u/4)
    assert np.allclose(f_force(xs), -(u(xs + h) - u(xs - h)) / (2 * h) / 4, atol=1e-7)
    assert np.allclose(du(xs), (u(xs + h) - u(xs - h)) / (2 * h), atol=1e-6)
    assert np.allclose(d2u(xs), (du(xs + h) - du(xs - h)) / (2 * h), atol=1e-5)
    # zeros: F(x) = 0 <=> (x/ℓ)[1 − (x/ℓ)²] = 0 <=> x = −ℓ, 0, ℓ ; F é ímpar; F(ℓ/2) = 3F0/8
    assert np.allclose(f_force(xs), xs * (1 - xs ** 2))
    assert f_force(0.0) == 0 and f_force(1.0) == 0 and f_force(-1.0) == 0
    assert np.allclose(f_force(-xs), -f_force(xs)) and np.isclose(f_force(0.5), 3 / 8)
    assert np.isclose(0.5 - 0.5 ** 3, 0.5 - 1 / 8) and np.isclose(0.5 - 1 / 8, 3 / 8)
    # sinais pelos fatores: x/ℓ e 1 − (x/ℓ)²
    for xr, sx, sb, sf in ((-1.35, -1, -1, 1), (-0.5, -1, 1, -1), (0.5, 1, 1, 1), (1.35, 1, -1, -1)):
        assert np.sign(xr) == sx and np.sign(1 - xr ** 2) == sb and np.sign(f_force(xr)) == sf == sx * sb
    # inclinações de U (U′ = −F): decrescente, crescente, decrescente, crescente
    for xr, sl in ((-1.35, -1), (-0.5, 1), (0.5, -1), (1.35, 1)):
        assert np.sign(du(xr)) == sl
    # U é par; U(ℓ/2) = U_b (1/4 − 1)² = (9/16) U_b; U ~ x⁴ para |x| grande
    assert np.allclose(u(-xs), u(xs)) and np.isclose(u(0.5), 0.5625) and np.isclose((0.25 - 1) ** 2, 9 / 16)
    assert np.isclose(u(50.0) / 50.0 ** 4, 1.0, atol=1e-3)
    # integração passo a passo, com F0 e ℓ arbitrários
    for F0, ell in ((2.3, 0.37), (1.0, 1.0), (5.5, 2.2)):
        x = xs * ell
        m4 = -F0 * (x ** 2 / (2 * ell) - x ** 4 / (4 * ell ** 3))                 # −F0[x²/2ℓ − x⁴/4ℓ³] (+ C)
        m5 = -F0 * x ** 2 / (2 * ell) + F0 * x ** 4 / (4 * ell ** 3)              # sinal distribuído
        assert np.allclose(m4, m5)
        assert np.allclose(F0 * (x / ell - x ** 3 / ell ** 3), F0 * x / ell - F0 * x ** 3 / ell ** 3)
        # condição de referência: U(ℓ) = 0 => C = F0ℓ/4
        c = F0 * ell / 4
        assert np.isclose(-F0 * ell ** 2 / (2 * ell) + F0 * ell ** 4 / (4 * ell ** 3) + c, 0.0, atol=1e-12)
        assert np.isclose(-F0 * ell / 2 + F0 * ell / 4, -F0 * ell / 4)
        u_sum = m5 + c
        u_tri = c * ((x / ell) ** 4 - 2 * (x / ell) ** 2 + 1)                     # trinômio
        u_sq = c * ((x / ell) ** 2 - 1) ** 2                                      # quadrado perfeito
        assert np.allclose(u_sum, u_tri) and np.allclose(u_tri, u_sq)
        a = (x / ell) ** 2
        assert np.allclose(a ** 2 - 2 * a + 1, (a - 1) ** 2)
        assert np.isclose(c * ((0.0 / ell) ** 2 - 1) ** 2, F0 * ell / 4)          # U(0) = U_b = F0ℓ/4
        assert np.isclose(c * ((0.5) ** 2 - 1) ** 2, 9 / 16 * F0 * ell / 4)       # U(ℓ/2) = 9/16 U_b
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
    # eventos usados na sincronização dos destaques
    assert len(SUB_TP) >= 2 and len(SUB_MIN) >= 2 and SUB_MIN[0] < SUB_TP[0] < SUB_MIN[1] < SUB_TP[1]
    assert len(SUP_TP) >= 2 and len(SUP_CEN) >= 2 and SUP_CEN[0] < SUP_TP[0] < SUP_CEN[1]
    # separatriz: √2 sech(a t) (a = 2√κ·s, s = escala de tempo da apresentação) conserva E = U_b na escala s,
    # é monótona e decresce para 0 sem nunca chegar nem cruzar
    s = A_SEP / (2 * np.sqrt(KAPPA))
    assert np.isclose(s, S_SEP)
    t = np.linspace(0, 9, 4501)
    xs_ = np.array([traj_sep(v) for v in t])
    vs_ = np.gradient(xs_, t)
    assert np.max(np.abs(0.5 * vs_[5:-5] ** 2 + KAPPA * s ** 2 * u(xs_[5:-5]) - KAPPA * s ** 2 * E_SEP)) < 1e-4
    assert np.all(np.diff(xs_) < 0) and xs_.min() > 0
    assert np.isclose(traj_sep(0.0), np.sqrt(2)) and np.isclose(u(np.sqrt(2)), E_SEP)
    assert traj_sep(7.0) > 0.05                                  # ainda longe de x = 0 no fim da exibição


_qa()

# ── Geometria da tela (frame 9 × 16) ────────────────────────────────────────
# Gráfico de energia: x em unidades de ℓ, U em unidades de U_b.
GSX, GX0 = 1.9, 0.0       # tela por ℓ
GY0, GSY = -0.35, 1.6     # U = 0 e tela por U_b
AXL, AXR = -3.4, 3.4      # eixo vertical e extensão horizontal
XR = 1.6                  # domínio do gráfico: |x| ≤ 1,6 ℓ
PY = -2.7                 # eixo espacial da partícula (faixa inferior do gráfico)
# Gráfico da força (S1)
FSX, FY0, FSY, FXR = 2.1, 0.1, 1.2, 1.45
FAX = -3.45               # eixo vertical F
LX = -3.45                # borda esquerda das linhas de derivação


def gx(x):
    return GX0 + GSX * x


def gy(uu):
    return GY0 + GSY * uu


def gpt(x):
    return np.array([gx(x), gy(u(x)), 0.0])


def fpt(x):
    return np.array([FSX * x, FY0 + FSY * f_force(x), 0.0])


# ── Texto e utilidades ──────────────────────────────────────────────────────
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
    """MathTex em partes (cor por índice de parte)."""
    m = MathTex(*parts, font_size=size, color=WHITE)
    for i, c in (colors or {}).items():
        m[i].set_color(c)
    if maxw and m.width > maxw:
        m.scale_to_fit_width(maxw)
    return m


def eqrow(parts, size=50, colors=None, y=0.0, left=LX):
    """Linha de derivação alinhada à esquerda (termos comuns ficam no mesmo lugar de um passo para outro)."""
    m = MathTex(*parts, font_size=size, color=WHITE)
    for i, c in (colors or {}).items():
        m[i].set_color(c)
    m.shift(RIGHT * (left - m.get_left()[0]) + UP * (y - m[0].get_center()[1]))
    return m


def mixed(*items, buff=0.16):
    return VGroup(*items).arrange(RIGHT, buff=buff)


def soft_swap(old, new, shift=UP * 0.12, lag=0.55):
    return AnimationGroup(FadeOut(old, shift=shift), FadeIn(new, shift=shift), lag_ratio=lag)


def seg(p, q, **kw):
    return Line(np.array([p[0], p[1], 0.0]), np.array([q[0], q[1], 0.0]), **kw)


def win(t, t0, t1, fade=0.3):
    """Janela temporal trapezoidal (0 → 1 → 0) para destaques ligados ao tempo da trajetória."""
    return float(np.clip((t - t0) / fade, 0, 1) * np.clip((t1 - t) / fade, 0, 1))


def kseg(x, E, alpha):
    """Barra K = E − U(x) em x: sólida se U ≤ E; tracejada magenta (posição proibida) se U > E."""
    g = VGroup()
    if u(x) <= E + 1e-9:
        if gy(E) - gy(u(x)) > 0.03:
            g.add(seg((gx(x), gy(u(x))), (gx(x), gy(E)), stroke_width=6, color=KCOL).set_opacity(alpha).set_z_index(4))
    else:
        g.add(DashedLine([gx(x), gy(E), 0], [gx(x), gy(u(x)), 0], color=MAGENTA, stroke_width=4, dash_length=0.08)
              .set_opacity(0.8 * alpha))
    return g


class PotencialPocoDuplo013(Scene):

    def mark(self, name):
        print(f"[MARCA] {self.renderer.time:7.2f} s  {name}")

    def xp(self):
        return float(self.traj(self.T.TT.get_value()))

    # ── Utilidades de cena ──────────────────────────────────────────────────
    def solid(self, m):
        """Depois de um FadeIn do grupo, deixa as partes como objetos independentes da cena."""
        self.remove(m)
        self.add(*m.submobjects)

    def show(self, m, run_time=1.0, shift=UP * 0.1):
        self.play(FadeIn(m, shift=shift), run_time=run_time)
        self.solid(m)

    def dim(self, m, op=0.5, run_time=0.5):
        self.play(*[p.animate.set_opacity(op) for p in m], run_time=run_time)

    def timed(self, mob, t0, t1, fade=0.3):
        """Texto cuja opacidade segue o tempo da trajetória (aparece em t0, some em t1)."""
        mob.set_opacity(0)
        mob.add_updater(lambda m: m.set_opacity(win(self.T.TT.get_value(), t0, t1, fade)))
        self.add(mob)
        self._timed.append(mob)

    def clear_timed(self):
        for m in self._timed:
            m.clear_updaters()
            self.remove(m)
        self._timed = []

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
            FX=ValueTracker(0),          # cursor de F(x) (S1)
            FV=ValueTracker(0),
            UX=ValueTracker(0),          # cursor de U(x) (S5)
            UV=ValueTracker(0),
        )
        self._timed = []
        self.traj = traj_rest

        # Cursor que traça a curva de F: ponto (x, F(x)), projeções e trecho já percorrido
        def f_trace():
            fv = T.FV.get_value()
            if fv <= 0.001:
                return VGroup()
            x = T.FX.get_value()
            p = fpt(x)
            g = VGroup()
            if x > 0.02:
                xs = np.linspace(0, x, max(4, int(70 * x / FXR)))
                g.add(VMobject(color=CYAN, stroke_width=5).set_points_smoothly([fpt(v) for v in xs]).set_stroke(opacity=fv))
            g.add(DashedLine([p[0], FY0, 0], p, color=WHITE, stroke_width=1.6, dash_length=0.08).set_opacity(0.5 * fv))
            g.add(DashedLine([FAX, p[1], 0], p, color=CYAN, stroke_width=1.6, dash_length=0.08).set_opacity(0.5 * fv))
            g.add(Dot(p, radius=0.09, color=WHITE).set_opacity(fv).set_z_index(5))
            return g

        self.f_trace = always_redraw(f_trace)

        # Cursor que traça a curva de U a partir de x = 0 (lado direito); o esquerdo vem da simetria
        def u_trace():
            uv = T.UV.get_value()
            if uv <= 0.001:
                return VGroup()
            x = T.UX.get_value()
            p = gpt(x)
            g = VGroup()
            if x > 0.02:
                xs = np.linspace(0, x, max(4, int(90 * x / XR)))
                g.add(VMobject(color=VIOLET, stroke_width=5).set_points_smoothly([gpt(v) for v in xs]).set_stroke(opacity=uv))
            g.add(DashedLine([p[0], GY0, 0], p, color=WHITE, stroke_width=1.6, dash_length=0.08).set_opacity(0.5 * uv))
            g.add(DashedLine([AXL, p[1], 0], p, color=VIOLET, stroke_width=1.6, dash_length=0.08).set_opacity(0.5 * uv))
            g.add(Dot(p, radius=0.09, color=WHITE).set_opacity(uv).set_z_index(5))
            return g

        self.u_trace = always_redraw(u_trace)

        # Gráfico de energia (S5 em diante)
        self.u_curve = VMobject(color=VIOLET, stroke_width=5).set_points_smoothly(
            [gpt(x) for x in np.linspace(-XR, XR, 161)])
        self.u_axis = Arrow([AXL, GY0 - 0.2, 0], [AXL, 3.75, 0], buff=0, stroke_width=2.5, tip_length=0.16,
                            color=WHITE).set_opacity(0.55)
        self.u_label = tex("U", 34, VIOLET).move_to([AXL + 0.32, 3.65, 0])
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
                Dot([gx(x), gy(u(x)), 0], radius=0.075, color=VIOLET).set_opacity(cv).set_z_index(4),
                Dot([gx(x), gy(E), 0], radius=0.075, color=BLUE_L).set_opacity(cv).set_z_index(4),
                kseg(x, E, cv))

        self.particle = always_redraw(particle)
        self.kbar = always_redraw(kbar)
        self.cursor = always_redraw(cursor)
        self.k_lab = mt("K", "=", "E", "-", "U(x)", size=34, colors={0: KCOL, 2: BLUE_L, 4: VIOLET}, maxw=3.0)
        self.k_lab.move_to([0, -3.65, 0])
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

    # ── S1 Força dada, zeros, sinais, ponto de teste, simetria e curva ──────
    def s1(self):
        T = self.T
        self.add(self.f_trace)
        # eixo espacial simples, centro identificado e uma partícula
        hd = lines("PRESA DE UM LADO", "OU ATRAVESSA?", size=38).move_to([0, 6.35, 0])
        sub = mixed(text("Sem resolver", 28), tex(r"x(t)?", 34)).move_to([0, 5.2, 0])
        ax = Line([-3.4, FY0, 0], [3.4, FY0, 0], stroke_width=2.5, color=WHITE).set_opacity(0.55)
        xl = tex("x", 30).move_to([3.3, FY0 - 0.35, 0])
        centro = VGroup(seg((0, FY0 - 0.1), (0, FY0 + 0.1), stroke_width=3, color=WHITE),
                        tex("0", 30).move_to([0, FY0 - 0.5, 0]),
                        text("centro", 22, opacity=0.8).move_to([0, FY0 - 1.0, 0]))
        part = VGroup(Dot([FSX * 0.5, FY0, 0], radius=0.19, color=WHITE).set_opacity(0.18),
                      Dot([FSX * 0.5, FY0, 0], radius=0.09, color=WHITE)).set_z_index(5)
        self.play(FadeIn(hd, shift=DOWN * 0.15), FadeIn(ax), FadeIn(xl), FadeIn(centro), FadeIn(part, scale=0.5),
                  run_time=1.0)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.8)
        self.wait(0.6)
        # a força é dada
        cap = text("a força é um dado do problema", 26, opacity=0.85).move_to([0, 5.2, 0])
        f_top = mt("F(x)", "=", "F_0", r"\left[\frac{x}{\ell}-\left(\frac{x}{\ell}\right)^3\right]", r",\quad F_0>0,\ \ell>0",
                   size=40, colors={0: CYAN}, maxw=7.6).move_to([0, 4.4, 0])
        self.play(soft_swap(sub, cap), FadeIn(f_top, shift=UP * 0.1), run_time=1.2)
        self.mark("forca dada")
        self.wait(0.8)
        # zeros
        vaxis = Arrow([FAX, FY0 - 2.1, 0], [FAX, FY0 + 2.3, 0], buff=0, stroke_width=2.5, tip_length=0.16,
                      color=WHITE).set_opacity(0.55)
        vlab = tex("F", 34, CYAN).move_to([FAX + 0.32, FY0 + 2.35, 0])
        self.play(FadeOut(hd), FadeOut(cap), FadeIn(vaxis), FadeIn(vlab), run_time=0.8)
        z1 = mt("F(x)", r"=0\;\Rightarrow\;", r"\frac{x}{\ell}\left[1-\left(\frac{x}{\ell}\right)^2\right]", "=0",
                size=36, colors={0: CYAN}).move_to([0, 3.3, 0])
        z2 = mt("x", "=", r"-\ell,\;0,\;+\ell", size=44).move_to([0, 2.45, 0])
        self.play(FadeIn(z1, shift=UP * 0.1), run_time=1.4)
        self.wait(0.4)
        self.play(FadeIn(z2, shift=UP * 0.1), run_time=1.0)
        zeros = VGroup(*(Dot([FSX * z, FY0, 0], radius=0.09, color=WHITE).set_z_index(3) for z in (-1, 0, 1)))
        tk = VGroup(tex(r"-\ell", 30).move_to([-FSX, FY0 - 0.5, 0]), tex(r"+\ell", 30).move_to([FSX, FY0 - 0.5, 0]))
        self.play(AnimationGroup(*(FadeIn(d, scale=0.4) for d in zeros), lag_ratio=0.25), FadeIn(tk),
                  FadeOut(centro[2]), z1.animate.set_opacity(0.4), run_time=1.3)
        self.mark("zeros")

        # sinais, região por região, com um único marcador de análise (não é uma trajetória)
        xc = [-1.35, -0.5, 0.5, 1.35]
        reasons = [
            (r"\frac{x}{\ell}<0,\quad 1-\left(\frac{x}{\ell}\right)^2<0\;\Rightarrow\;F>0", +1),
            (r"\frac{x}{\ell}<0,\quad 1-\left(\frac{x}{\ell}\right)^2>0\;\Rightarrow\;F<0", -1),
            (r"\frac{x}{\ell}>0,\quad 1-\left(\frac{x}{\ell}\right)^2>0\;\Rightarrow\;F>0", +1),
            (r"\frac{x}{\ell}>0,\quad 1-\left(\frac{x}{\ell}\right)^2<0\;\Rightarrow\;F<0", -1),
        ]
        note = text("marcador de análise (não é a trajetória)", 22, opacity=0.8).move_to([0, -3.95, 0])
        marker, rtex = None, None
        marks, arrows, labels = [], [], []
        for k, (x0, (rs, sg)) in enumerate(zip(xc, reasons)):
            cx = FSX * x0
            direc = sg
            new_m = Circle(radius=0.14, color=WHITE, stroke_width=3.5).move_to([cx, FY0, 0]).set_z_index(5)
            arr = Arrow([cx + 0.2 * direc, FY0, 0], [cx + 0.7 * direc, FY0, 0], buff=0, color=CYAN, stroke_width=6,
                        max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=10).set_z_index(4)
            lab = tex(rf"F{'>' if sg > 0 else '<'}0", 32, CYAN).move_to(
                [cx + 0.1 * direc, FY0 + (-1.05 if sg > 0 else 0.9), 0])
            new_r = tex(rs, 34).move_to([0, -3.1, 0])
            if new_r.width > 7.6:
                new_r.scale_to_fit_width(7.6)
            outs, ins = [], [FadeIn(new_m, scale=0.6), FadeIn(new_r, shift=UP * 0.1)]
            if marker is not None:
                outs += [FadeOut(marker), FadeOut(rtex)]
            if k == 0:
                outs.append(FadeOut(part))
                ins.append(FadeIn(note))
            self.play(*outs, *ins, run_time=0.8)
            self.play(FadeIn(arr, shift=RIGHT * 0.2 * direc), FadeIn(lab, shift=UP * 0.1), run_time=0.8)
            self.wait(0.7)
            marker, rtex = new_m, new_r
            marks.append(new_m)
            arrows.append(arr)
            labels.append(lab)
        self.mark("sinais")
        # ponto de teste fora dos zeros: F(ℓ/2) = 3F0/8, levado ao gráfico por projeções
        calc = mt(r"F\!\left(\frac{\ell}{2}\right)", "=", "F_0", r"\left(\frac12-\frac18\right)", "=", r"\frac{3F_0}{8}",
                  size=40, colors={0: CYAN}).move_to([0, -3.1, 0])
        m3 = Circle(radius=0.14, color=WHITE, stroke_width=3.5).move_to([FSX * 0.5, FY0, 0]).set_z_index(5)
        self.play(FadeOut(rtex), FadeOut(note), FadeOut(marker), FadeOut(z1), FadeIn(m3, scale=0.6),
                  FadeIn(calc, shift=UP * 0.1), run_time=1.2)
        pt = fpt(0.5)
        vline = DashedLine([pt[0], FY0 + 0.16, 0], pt, color=WHITE, stroke_width=1.8, dash_length=0.08).set_opacity(0.7)
        hline = DashedLine(pt, [FAX, pt[1], 0], color=CYAN, stroke_width=1.8, dash_length=0.08).set_opacity(0.7)
        pdot = Dot(pt, radius=0.09, color=WHITE).set_z_index(5)
        plab = tex(r"\frac{3F_0}{8}", 30, CYAN).move_to([FAX - 0.62, pt[1], 0])
        self.play(Create(vline), run_time=0.8)
        self.play(FadeIn(pdot, scale=0.5), Create(hline), run_time=0.8)
        self.play(FadeIn(plab, shift=RIGHT * 0.1), run_time=0.6)
        self.wait(0.5)
        # F é ímpar: F(−x) = −F(x)
        odd = mt("F(-x)", "=", "-", "F(x)", size=44, colors={0: CYAN, 3: CYAN}).move_to([0, -3.1, 0])
        self.play(soft_swap(calc, odd), run_time=0.9)
        grp = VGroup(vline, pdot).copy()
        self.add(grp)
        pt2 = np.array([-pt[0], 2 * FY0 - pt[1], 0])
        hline2 = DashedLine(pt2, [FAX, pt2[1], 0], color=CYAN, stroke_width=1.8, dash_length=0.08).set_opacity(0.7)
        plab2 = tex(r"-\frac{3F_0}{8}", 30, CYAN).move_to([FAX - 0.7, pt2[1], 0])
        self.play(Rotate(grp, PI, about_point=np.array([0, FY0, 0])), run_time=1.5)
        self.play(Create(hline2), FadeIn(plab2, shift=RIGHT * 0.1), run_time=0.8)
        self.wait(0.4)
        # a curva é traçada por um cursor (x, F(x)): lado direito calculado, lado esquerdo pela simetria
        self.play(FadeOut(VGroup(vline, hline, pdot, plab, grp, hline2, plab2, m3)), FadeOut(odd), run_time=0.6)
        tr = text("cada ponto da curva: x escolhido, F(x) calculada", 24, opacity=0.9).move_to([0, -3.1, 0])
        T.FX.set_value(0)
        self.play(T.FV.animate.set_value(1), FadeIn(tr), run_time=0.5)
        self.play(T.FX.animate.set_value(FXR), run_time=4.0, rate_func=smooth)
        right = VMobject(color=CYAN, stroke_width=5).set_points_smoothly([fpt(v) for v in np.linspace(0, FXR, 90)])
        self.add(right)
        T.FV.set_value(0)
        left = right.copy()
        self.add(left)
        odd2 = mt("F(-x)", "=", "-", "F(x)", size=40, colors={0: CYAN, 3: CYAN}).move_to([0, -3.1, 0])
        self.play(soft_swap(tr, odd2), run_time=0.7)
        self.play(Rotate(left, PI, about_point=np.array([0, FY0, 0])), run_time=1.8)
        self.mark("curva F")
        # síntese: convergência para ±ℓ e afastamento de 0; ponte para o potencial
        conv = mixed(text("a força converge para", 24, opacity=0.9), tex(r"\pm\ell", 30),
                     text("e afasta de", 24, opacity=0.9), tex("0", 30)).move_to([0, -3.1, 0])
        self.play(soft_swap(odd2, conv), *[Indicate(zz, color=CYAN, scale_factor=1.6) for zz in (zeros[0], zeros[2])], run_time=1.2)
        self.wait(1.0)
        bridge = text("Qual potencial corresponde a essa força?", 28).move_to([0, -3.1, 0])
        self.play(soft_swap(conv, bridge), run_time=1.0)
        self.wait(1.0)
        self.s1_all = VGroup(ax, xl, centro[0], centro[1], vaxis, vlab, right, left, zeros, tk, f_top, z2, bridge,
                             *marks, *arrows, *labels)

    # ── S2 Integração acompanhável ──────────────────────────────────────────
    def s2(self):
        self.play(FadeOut(self.s1_all), run_time=1.0)
        SZ = 50
        # F = −U′ (linha auxiliar) e U = −∫F dx (linha principal)
        l1 = mt("F(x)", "=", "-", "U'(x)", size=46, colors={0: CYAN, 3: VIOLET}).move_to([0, 4.9, 0])
        self.show(l1, 1.0)
        P2 = ["U(x)", "=", "-", r"\int", "F(x)", r"\,dx"]
        l2 = eqrow(P2, SZ, {0: VIOLET, 4: CYAN}, y=3.6)
        self.show(l2, 1.0)
        self.dim(l1, 0.45)
        self.wait(0.5)
        # F(x) vira F0 (x/ℓ − x³/ℓ³) dentro da integral
        P3 = ["U(x)", "=", "-", "F_0", r"\int", r"\Big(", r"\frac{x}{\ell}", "-", r"\frac{x^3}{\ell^3}", r"\Big)", r"\,dx"]
        l3 = eqrow(P3, SZ, {0: VIOLET, 3: CYAN, 6: CYAN, 7: CYAN, 8: CYAN}, y=3.6)
        self.play(FadeOut(l2[4]), run_time=0.4)
        self.play(*[ReplacementTransform(l2[i], l3[j]) for i, j in ((0, 0), (1, 1), (2, 2), (3, 4), (5, 10))],
                  run_time=0.9)
        self.play(FadeIn(l3[3]), *[FadeIn(l3[j]) for j in (5, 6, 7, 8, 9)], run_time=0.8)
        self.wait(0.6)
        # 1) separação dos dois termos: a integral é aplicada a cada termo
        A1 = ["U(x)", "=", "-", "F_0", r"\Big[", r"\int", r"\frac{x}{\ell}", r"\,dx"]
        A2 = ["-", r"\int", r"\frac{x^3}{\ell^3}", r"\,dx", r"\Big]", "+C"]
        r1 = eqrow(A1, SZ, {0: VIOLET, 3: CYAN, 6: CYAN}, y=3.6)
        r2 = eqrow(A2, SZ, {2: CYAN}, y=2.35, left=r1[4].get_left()[0])
        self.play(FadeOut(l3[5]), FadeOut(l3[9]), run_time=0.4)
        self.play(*[ReplacementTransform(l3[i], r1[i]) for i in (0, 1, 2, 3)],
                  ReplacementTransform(l3[7], r2[0]), ReplacementTransform(l3[8], r2[2]), run_time=0.9)
        self.play(ReplacementTransform(l3[4], r1[5]), ReplacementTransform(l3[6], r1[6]),
                  ReplacementTransform(l3[10], r1[7]), run_time=0.8)
        self.play(FadeIn(r1[4]), FadeIn(r2[1]), FadeIn(r2[3]), FadeIn(r2[4]), FadeIn(r2[5]), run_time=0.8)
        self.mark("integral separada")
        self.wait(0.5)
        # 2) 1/ℓ e 1/ℓ³ saem da integral e permanecem multiplicando
        B1 = ["U(x)", "=", "-", "F_0", r"\Big[", r"\frac{1}{\ell}", r"\int x\,dx"]
        B2 = ["-", r"\frac{1}{\ell^3}", r"\int x^3\,dx", r"\Big]", "+C"]
        s1_ = eqrow(B1, SZ, {0: VIOLET, 3: CYAN, 5: BLUE_L}, y=3.6)
        s2_ = eqrow(B2, SZ, {1: BLUE_L}, y=2.35, left=s1_[4].get_left()[0])
        self.play(FadeOut(r1[5]), FadeOut(r1[6]), FadeOut(r1[7]), FadeOut(r2[1]), FadeOut(r2[2]), FadeOut(r2[3]),
                  run_time=0.5)
        self.play(*[ReplacementTransform(r1[i], s1_[i]) for i in range(5)], ReplacementTransform(r2[0], s2_[0]),
                  ReplacementTransform(r2[4], s2_[3]), ReplacementTransform(r2[5], s2_[4]), run_time=0.7)
        self.play(FadeIn(s1_[5]), FadeIn(s1_[6]), FadeIn(s2_[1]), FadeIn(s2_[2]), run_time=0.8)
        self.play(Indicate(s1_[5], color=BLUE_L), Indicate(s2_[1], color=BLUE_L), run_time=0.9)
        self.wait(0.3)
        # 3) primitivas: uma de x e uma de x³
        h1 = mixed(text("uma primitiva de", 26, opacity=0.9), tex("x", 36), text(":", 26, opacity=0.9),
                   tex(r"\frac{x^2}{2}", 40)).move_to([0, 1.1, 0])
        self.play(FadeIn(h1, shift=UP * 0.1), run_time=0.7)
        C1 = ["U(x)", "=", "-", "F_0", r"\Big[", r"\frac{1}{\ell}", r"\frac{x^2}{2}"]
        t1 = eqrow(C1, SZ, {0: VIOLET, 3: CYAN, 5: BLUE_L}, y=3.6)
        self.play(FadeOut(s1_[6]), run_time=0.4)
        self.play(*[ReplacementTransform(s1_[i], t1[i]) for i in range(6)], run_time=0.3)
        self.play(FadeIn(t1[6]), run_time=0.6)
        h2 = mixed(text("uma primitiva de", 26, opacity=0.9), tex(r"x^3", 36), text(":", 26, opacity=0.9),
                   tex(r"\frac{x^4}{4}", 40)).move_to([0, 1.1, 0])
        self.play(soft_swap(h1, h2), run_time=0.7)
        C2 = ["-", r"\frac{1}{\ell^3}", r"\frac{x^4}{4}", r"\Big]", "+C"]
        t2 = eqrow(C2, SZ, {1: BLUE_L}, y=2.35, left=t1[4].get_left()[0])
        self.play(FadeOut(s2_[2]), run_time=0.4)
        self.play(*[ReplacementTransform(s2_[i], t2[j]) for i, j in ((0, 0), (1, 1), (3, 3), (4, 4))], run_time=0.5)
        self.play(FadeIn(t2[2]), run_time=0.6)
        self.wait(0.4)
        # 4) formação das frações
        h3 = text("juntar cada produto em uma fração", 24, opacity=0.9).move_to([0, 1.1, 0])
        D = ["U(x)", "=", "-", "F_0", r"\Big[", r"\frac{x^2}{2\ell}", "-", r"\frac{x^4}{4\ell^3}", r"\Big]", "+C"]
        d = eqrow(D, SZ, {0: VIOLET, 3: CYAN}, y=3.6)
        self.play(soft_swap(h2, h3), run_time=0.6)
        self.play(FadeOut(t1[5]), FadeOut(t1[6]), FadeOut(t2[1]), FadeOut(t2[2]), run_time=0.5)
        self.play(*[ReplacementTransform(t1[i], d[i]) for i in range(5)], ReplacementTransform(t2[0], d[6]),
                  ReplacementTransform(t2[3], d[8]), ReplacementTransform(t2[4], d[9]), run_time=0.9)
        self.play(FadeIn(d[5]), FadeIn(d[7]), run_time=0.7)
        self.mark("integrado")
        self.wait(0.5)
        # 5) distribuição do sinal negativo (−F0 multiplica cada termo)
        h4 = mixed(tex("-F_0", 34), text("multiplica cada termo", 24, opacity=0.9)).move_to([0, 1.1, 0])
        E = ["U(x)", "=", "-", r"\frac{F_0x^2}{2\ell}", "+", r"\frac{F_0x^4}{4\ell^3}", "+C"]
        e = eqrow(E, SZ, {0: VIOLET}, y=3.6)
        self.play(soft_swap(h3, h4), Indicate(d[2], color=WHITE, scale_factor=1.5), Indicate(d[3], color=CYAN,
                                                                                            scale_factor=1.3), run_time=1.0)
        self.play(FadeOut(d[4]), FadeOut(d[8]), FadeOut(d[3]), FadeOut(d[5]), FadeOut(d[6]), FadeOut(d[7]), run_time=0.5)
        self.play(*[ReplacementTransform(d[i], e[j]) for i, j in ((0, 0), (1, 1), (2, 2), (9, 6))], run_time=0.8)
        self.play(FadeIn(e[3]), FadeIn(e[4]), FadeIn(e[5]), run_time=0.7)
        self.play(FadeOut(h4), run_time=0.4)
        self.wait(0.6)
        self.s2_l1, self.m5 = l1, e

    # ── S3 Escolha de C ─────────────────────────────────────────────────────
    def s3(self):
        e = self.m5
        self.play(FadeOut(self.s2_l1), *[p.animate.shift(DOWN * 0.4) for p in e], run_time=0.8)     # y = 3.2
        t1 = VGroup(text("Escolhemos energia zero", 28), text("nos equilíbrios estáveis.", 28)).arrange(DOWN, buff=0.12)
        t1.move_to([0, 5.7, 0])
        c1 = mt("U(", r"\pm\ell", ")", "=", "0", size=56, colors={0: VIOLET, 2: VIOLET}).move_to([0, 4.5, 0])
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=1.0)
        self.wait(0.5)
        t2 = mixed(text("pela simetria, basta substituir", 24, opacity=0.9), tex(r"x=\ell", 32)).move_to([0, 2.2, 0])
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.7)
        PA = ["0", "=", r"U(\ell)", "=", "-", r"\frac{F_0\ell^2}{2\ell}", "+", r"\frac{F_0\ell^4}{4\ell^3}", "+C"]
        la = eqrow(PA, 46, {2: VIOLET}, y=1.2)
        self.play(FadeIn(la[0]), FadeIn(la[1]), FadeIn(la[2]), FadeIn(la[3]), run_time=0.8)
        for i, j in ((2, 4), (3, 5), (4, 6), (5, 7), (6, 8)):
            self.play(Indicate(e[i], color=BLUE_L, scale_factor=1.12), FadeIn(la[j], shift=DOWN * 0.2), run_time=0.55)
        self.wait(0.8)
        # simplificação das potências, termo a termo
        PB = ["0", "=", "-", r"\frac{F_0\ell}{2}", "+", r"\frac{F_0\ell}{4}", "+C"]
        lb = eqrow(PB, 46, y=1.2)
        self.play(FadeOut(la[2]), FadeOut(la[3]), run_time=0.4)
        self.play(ReplacementTransform(la[0], lb[0]), ReplacementTransform(la[1], lb[1]),
                  ReplacementTransform(la[4], lb[2]), ReplacementTransform(la[5], lb[3]),
                  ReplacementTransform(la[6], lb[4]), ReplacementTransform(la[7], lb[5]),
                  ReplacementTransform(la[8], lb[6]), run_time=0.9)
        self.wait(0.8)
        # reunião das frações
        PC = ["0", "=", "-", r"\frac{F_0\ell}{4}", "+C"]
        lc = eqrow(PC, 46, y=1.2)
        self.play(FadeOut(lb[3]), FadeOut(lb[4]), FadeOut(lb[5]), run_time=0.5)
        self.play(*[ReplacementTransform(lb[i], lc[j]) for i, j in ((0, 0), (1, 1), (2, 2), (6, 4))], run_time=0.7)
        self.play(FadeIn(lc[3]), run_time=0.6)
        self.wait(0.8)
        # isolamento de C
        box = mt("C", "=", r"\frac{F_0\ell}{4}", size=62, colors={0: MAGENTA, 2: MAGENTA}).move_to([0, -0.7, 0])
        bx = SurroundingRectangle(box, color=MAGENTA, buff=0.2, corner_radius=0.1, stroke_width=3)
        self.play(FadeIn(box, shift=UP * 0.1), Create(bx), run_time=1.2)
        self.mark("C")
        note = VGroup(text("C só define a referência de energia;", 24, opacity=0.9),
                      text("a força não muda.", 24, opacity=0.9)).arrange(DOWN, buff=0.1).move_to([0, -2.2, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.8)
        self.wait(1.2)
        self.s3_all = VGroup(t1, c1, t2, note, *lc)
        self.box, self.bx = box, bx

    # ── S4 Substituição de C e fatoração ────────────────────────────────────
    def s4(self):
        e, box, bx = self.m5, self.box, self.bx
        self.play(FadeOut(self.s3_all), run_time=0.8)
        # C -> F0ℓ/4 e deslocamento da linha para o topo
        Y0 = 4.9
        self.play(*[p.animate.shift(UP * (Y0 - 3.2)) for p in e], run_time=0.8)
        P6 = ["U(x)", "=", "-", r"\frac{F_0x^2}{2\ell}", "+", r"\frac{F_0x^4}{4\ell^3}", "+", r"\frac{F_0\ell}{4}"]
        m6 = eqrow(P6, 46, {0: VIOLET, 7: MAGENTA}, y=Y0)
        self.play(FadeOut(e[6]), run_time=0.4)
        self.play(*[ReplacementTransform(e[i], m6[i]) for i in range(6)], FadeIn(m6[6]), run_time=0.6)
        self.play(TransformFromCopy(box[2], m6[7]), FadeOut(bx), FadeOut(box), run_time=1.4)
        self.wait(0.5)
        # reordenar: x⁴ primeiro (os dois termos trocam de lugar por arcos opostos)
        P6b = ["U(x)", "=", r"\frac{F_0x^4}{4\ell^3}", "-", r"\frac{F_0x^2}{2\ell}", "+", r"\frac{F_0\ell}{4}"]
        m6b = eqrow(P6b, 46, {0: VIOLET, 6: MAGENTA}, y=Y0)
        self.play(FadeOut(m6[4]), run_time=0.4)
        self.play(ReplacementTransform(m6[0], m6b[0]), ReplacementTransform(m6[1], m6b[1]),
                  ReplacementTransform(m6[5], m6b[2], path_arc=PI), ReplacementTransform(m6[2], m6b[3], path_arc=PI),
                  ReplacementTransform(m6[3], m6b[4], path_arc=PI), ReplacementTransform(m6[6], m6b[5]),
                  ReplacementTransform(m6[7], m6b[6]), run_time=1.6)
        self.wait(0.5)
        # retirar F0ℓ/4 por termos: o fator comum sai do último termo e cada termo é dividido por ele
        Y1 = 3.3
        PB1 = ["U(x)", "=", r"\frac{F_0\ell}{4}", r"\Big[", r"\Big(\frac{x}{\ell}\Big)^4", "-",
               r"2\Big(\frac{x}{\ell}\Big)^2", "+", "1", r"\Big]"]
        b1 = eqrow(PB1, 46, {0: VIOLET, 2: MAGENTA}, y=Y1)
        hint = mixed(text("fator comum", 24, opacity=0.9), tex(r"\frac{F_0\ell}{4}", 34, MAGENTA), text(": dividir cada termo", 24, opacity=0.9)).move_to([0, 2.2, 0])
        self.play(FadeIn(b1[0]), FadeIn(b1[1]), FadeIn(b1[3]), FadeIn(hint), run_time=0.8)
        self.play(Indicate(m6b[6], color=MAGENTA, scale_factor=1.15), FadeIn(b1[2], shift=DOWN * 0.2), run_time=0.8)
        for i, j in ((2, 4), (3, 5), (4, 6), (5, 7), (6, 8)):
            self.play(Indicate(m6b[i], color=BLUE_L, scale_factor=1.1), FadeIn(b1[j], shift=DOWN * 0.2), run_time=0.55)
        self.play(FadeIn(b1[9]), run_time=0.4)
        self.mark("fatorado")
        self.wait(0.4)
        # a² − 2a + 1 = (a − 1)², a = (x/ℓ)²: estrutura destacada na própria expressão
        lab = VGroup(tex(r"a^2", 34, BLUE_L).next_to(b1[4], DOWN, buff=0.45),
                     tex(r"2a", 34, BLUE_L).next_to(b1[6], DOWN, buff=0.45),
                     tex(r"1", 34, BLUE_L).next_to(b1[8], DOWN, buff=0.45))
        ident = mt(r"a=\Big(\frac{x}{\ell}\Big)^2", r"\;:\quad", r"a^2-2a+1", "=", r"(a-1)^2", size=40,
                   colors={2: BLUE_L, 4: BLUE_L}).move_to([0, 0.5, 0])
        self.play(FadeOut(hint), FadeIn(lab, shift=UP * 0.1), run_time=0.9)
        self.play(FadeIn(ident, shift=UP * 0.1), run_time=1.0)
        self.wait(0.8)
        # resultado
        PR = ["U(x)", "=", r"\frac{F_0\ell}{4}", r"\Big[", r"\Big(\frac{x}{\ell}\Big)^2", "-1", r"\Big]^2"]
        res = eqrow(PR, 52, {0: VIOLET, 2: MAGENTA}, y=-1.2)
        self.play(*[FadeIn(res[k], shift=DOWN * 0.2) for k in range(4)], run_time=0.8)
        self.play(FadeIn(res[4]), FadeIn(res[5]), FadeIn(res[6]), run_time=0.9)
        rb = SurroundingRectangle(res, color=VIOLET, buff=0.2, corner_radius=0.1, stroke_width=3)
        self.play(Create(rb), FadeOut(lab), FadeOut(ident), run_time=0.8)
        chk = mixed(text("confere:", 26, opacity=0.9), mt("-", "U'(x)", "=", "F(x)", size=44, colors={1: VIOLET, 3: CYAN}))
        chk.move_to([0, -2.9, 0])
        self.play(FadeIn(chk, shift=UP * 0.1), run_time=0.9)
        self.wait(0.9)
        self.s4_rest = VGroup(*m6b, *b1, chk)
        self.res, self.rb = res, rb
        self.res_group = VGroup(res, rb)

    # ── S5 Forma do potencial e classificação ───────────────────────────────
    def s5(self):
        T = self.T
        # limpa a derivação e deixa o resultado como referência no topo
        res_g = VGroup(*self.res, self.rb)
        self.play(FadeOut(self.s4_rest), run_time=0.7)
        self.play(res_g.animate.scale(0.8).move_to([0, 6.2, 0]), run_time=0.9)
        # troca do eixo vertical: de força para energia
        hint = mixed(text("novo gráfico: o eixo vertical é", 24, opacity=0.9), text("energia", 24, VIOLET)).move_to([0, 5.25, 0])
        self.play(FadeIn(self.u_axis), FadeIn(self.u_label), FadeIn(self.base), FadeIn(self.base_x),
                  FadeIn(self.base_ticks), FadeIn(hint, shift=UP * 0.1), run_time=1.2)
        self.wait(0.4)
        # inclinações: U′ = −F
        slope = mt("U'(x)", "=", "-", "F(x)", size=44, colors={0: VIOLET, 3: CYAN}).move_to([0, 5.25, 0])
        self.play(soft_swap(hint, slope), run_time=0.8)
        ROWY = 2.5
        regs = [(-1.35, r"x<-\ell:\ \ F>0\ \Rightarrow\ U'<0", -1, "decrescente"),
                (-0.5, r"-\ell<x<0:\ \ F<0\ \Rightarrow\ U'>0", 1, "crescente"),
                (0.5, r"0<x<\ell:\ \ F>0\ \Rightarrow\ U'<0", -1, "decrescente"),
                (1.35, r"x>\ell:\ \ F<0\ \Rightarrow\ U'>0", 1, "crescente")]
        picto, cur = [], None
        for x0, rs, sl, nm in regs:
            cx = gx(x0)
            arr = Arrow([cx - 0.42, ROWY - 0.28 * sl, 0], [cx + 0.42, ROWY + 0.28 * sl, 0], buff=0, color=VIOLET,
                        stroke_width=5, max_tip_length_to_length_ratio=0.4).set_z_index(4)
            ln = mt(rs, size=36, maxw=7.4).move_to([0, 4.4, 0])
            if cur is None:
                self.play(FadeIn(ln, shift=UP * 0.1), FadeIn(arr), run_time=0.8)
            else:
                self.play(soft_swap(cur, ln), FadeIn(arr), run_time=0.8)
            self.wait(0.5)
            cur = ln
            picto.append(arr)
        zl = mt(r"F=0\ \Rightarrow\ U'=0:\ \text{tangente horizontal}", size=36, maxw=7.4).move_to([0, 4.4, 0])
        ticks0 = VGroup(*(seg((gx(z) - 0.3, ROWY), (gx(z) + 0.3, ROWY), stroke_width=5, color=VIOLET) for z in (-1, 0, 1)))
        self.play(soft_swap(cur, zl), FadeIn(ticks0), run_time=0.9)
        self.mark("inclinacoes")
        self.wait(0.7)
        # pontos calculados: U(±ℓ) = 0 e U(0) = U_b
        l_w = VGroup(tex(r"U(-\ell)=0", 30, VIOLET).move_to([gx(-1), GY0 - 1.05, 0]),
                     tex(r"U(\ell)=0", 30, VIOLET).move_to([gx(1), GY0 - 1.05, 0]))
        l_b = tex(r"U(0)=\frac{F_0\ell}{4}=U_b", 30, MAGENTA).move_to([0, gy(1) + 0.55, 0])
        self.play(FadeOut(zl), FadeOut(slope), FadeIn(self.well_dots, scale=0.4), FadeIn(l_w, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(self.ub_level), FadeIn(self.ub_dot, scale=0.4), FadeIn(self.ub_tick),
                  FadeIn(l_b, shift=DOWN * 0.1), run_time=1.0)
        self.wait(0.4)
        # um ponto intermediário: U(ℓ/2) = (9/16) U_b
        calc = mt(r"U\!\left(\frac{\ell}{2}\right)", "=", "U_b", r"\left(\frac14-1\right)^2", "=", r"\frac{9}{16}U_b",
                  size=40, colors={0: VIOLET, 2: MAGENTA, 5: MAGENTA}).move_to([0, 4.4, 0])
        self.play(FadeIn(calc, shift=UP * 0.1), run_time=1.0)
        p = gpt(0.5)
        vl = DashedLine([p[0], GY0, 0], p, color=WHITE, stroke_width=1.8, dash_length=0.08).set_opacity(0.7)
        hl = DashedLine(p, [AXL, p[1], 0], color=VIOLET, stroke_width=1.8, dash_length=0.08).set_opacity(0.7)
        pd = Dot(p, radius=0.09, color=WHITE).set_z_index(5)
        pl = tex(r"\frac{9}{16}U_b", 26, VIOLET).move_to([AXL + 0.62, p[1] + 0.3, 0])
        self.play(Create(vl), run_time=0.7)
        self.play(FadeIn(pd, scale=0.5), Create(hl), FadeIn(pl), run_time=0.8)
        self.wait(0.4)
        # U é par: U(−x) = U(x)
        sym = mt("U(-x)", "=", "U(x)", size=44, colors={0: VIOLET, 2: VIOLET}).move_to([0, 4.4, 0])
        self.play(soft_swap(calc, sym), run_time=0.8)
        pd2 = VGroup(vl, pd).copy()
        self.add(pd2)
        self.play(Rotate(pd2, PI, axis=UP, about_point=np.array([0, 0, 0])), run_time=1.3)
        self.wait(0.4)
        self.play(FadeOut(VGroup(vl, hl, pd, pl, pd2)), FadeOut(sym), FadeOut(picto[0]), FadeOut(picto[1]),
                  FadeOut(picto[2]), FadeOut(picto[3]), FadeOut(ticks0), run_time=0.7)
        # curva traçada por um cursor (x, U(x)) a partir de x = 0; o outro lado vem da simetria
        tr = text("cada ponto: x escolhido, U(x) calculada", 24, opacity=0.9).move_to([0, 4.4, 0])
        self.add(self.u_trace)
        T.UX.set_value(0)
        self.play(T.UV.animate.set_value(1), FadeIn(tr), FadeOut(l_b), run_time=0.5)
        self.play(T.UX.animate.set_value(1.0), run_time=2.6, rate_func=smooth)
        ext = mt(r"|x|\ \text{grande}:\ U\approx\frac{F_0x^4}{4\ell^3}\ \Rightarrow\ U\to+\infty", size=38, maxw=7.4).move_to([0, 4.4, 0])
        self.play(soft_swap(tr, ext), T.UX.animate.set_value(XR), run_time=1.6, rate_func=smooth)
        right = VMobject(color=VIOLET, stroke_width=5).set_points_smoothly([gpt(v) for v in np.linspace(0, XR, 120)])
        self.add(right)
        T.UV.set_value(0)
        left = right.copy()
        self.add(left)
        self.play(Rotate(left, PI, axis=UP, about_point=np.array([0, 0, 0])), run_time=1.4)
        self.remove(right, left)
        self.add(self.u_curve)
        self.mark("curva U")
        self.play(FadeOut(ext), FadeOut(l_w), run_time=0.6)
        self.wait(0.3)

        # classificação: confirma pela segunda derivada e pela direção da força
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
        self.play(FadeIn(arc0), FadeIn(fa0), FadeIn(a0, shift=UP * 0.1), FadeIn(st0, shift=UP * 0.1), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(VGroup(arc0, fa0, a0, st0)), run_time=0.5)
        aw = tex(r"U''(\pm\ell)=\frac{2F_0}{\ell}>0", 32, VIOLET).move_to([0, GY0 - 1.15, 0])
        stw = VGroup(text("estável", 26, VIOLET).move_to([gx(-1), GY0 - 1.8, 0]),
                     text("estável", 26, VIOLET).move_to([gx(1), GY0 - 1.8, 0]))
        arcw = VGroup(arc(-1, WHITE), arc(1, WHITE))
        faw = VGroup(farrow(-1.35, 1), farrow(-0.7, -1), farrow(0.7, 1), farrow(1.35, -1))   # convergem para ±ℓ
        self.play(FadeIn(arcw), FadeIn(faw), FadeIn(aw, shift=UP * 0.1), FadeIn(stw, shift=UP * 0.1), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(VGroup(aw, stw, arcw, faw)), FadeOut(self.base_ticks), FadeOut(self.well_dots),
                  FadeOut(self.base_x), FadeOut(res_g), run_time=0.8)

    # ── S6 Energia e leitura de K ───────────────────────────────────────────
    def s6(self):
        T = self.T
        c1 = mt("E", "=", "K", "+", "U", size=44, colors={0: BLUE_L, 4: VIOLET}).move_to([0, 5.9, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=1.0)
        self.wait(0.6)
        c2 = mt("K", "=", "E", "-", "U", r"\ge 0", size=44, colors={2: BLUE_L, 4: VIOLET}).move_to([0, 5.15, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=1.0)
        self.wait(0.6)
        c3 = mt("U(x)", r"\le", "E", size=50, colors={0: VIOLET, 2: BLUE_L}).move_to([0, 4.35, 0])
        box = SurroundingRectangle(c3, color=BLUE_L, buff=0.18, corner_radius=0.08, stroke_width=2.5)
        self.play(FadeIn(c3, shift=UP * 0.1), Create(box), c1.animate.set_opacity(0.5), c2.animate.set_opacity(0.5),
                  run_time=1.2)
        self.wait(0.6)
        # a linha E nasce da desigualdade: o "E" da caixa viaja até o fim da linha
        cp = c3[2].copy()
        T.E.set_value(E_SUB)
        self.add(self.eline, self.e_lab)
        self.play(cp.animate.scale(0.7).move_to([AXR + 0.2, gy(E_SUB) + 0.3, 0]), T.LA.animate.set_value(1),
                  run_time=2.0, rate_func=smooth)
        self.remove(cp)
        self.add(self.region_axis, self.projections, self.turning, self.particle, self.kbar, self.cursor, self.k_lab,
                 self.ball, self.link)
        self.mark("linha E")
        # a relação já cumpriu sua função: sai para ampliar o gráfico; o cursor lê K em uma posição
        T.CS.set_value(1.15)
        self.play(FadeOut(VGroup(c1, c2, c3, box)), FadeIn(self.p_group), run_time=0.8)
        self.play(T.CV.animate.set_value(1), T.KL.animate.set_value(1), run_time=0.8)
        n0 = mixed(text("segmento: de", 24, opacity=0.9), tex("U(x)", 28, VIOLET), text("(curva) até", 24, opacity=0.9),
                   tex("E", 28, BLUE_L), text("(linha)", 24, opacity=0.9)).move_to([0, -4.3, 0])
        self.play(FadeIn(n0, shift=UP * 0.1), run_time=0.7)
        self.wait(1.2)
        n1 = mixed(tex(r"U<E", 32, BLUE_L), text("→", 26), tex(r"K>0", 32, KCOL),
                   text("posição permitida", 26, opacity=0.9)).move_to([0, -4.3, 0])
        self.play(soft_swap(n0, n1), run_time=0.7)
        self.wait(1.0)
        b = float(allowed(E_SUB)[1][1])
        self.play(T.CS.animate.set_value(b), run_time=2.2, rate_func=smooth)
        n2 = mixed(tex(r"U=E", 32, BLUE_L), text("→", 26), tex(r"K=0", 32, KCOL),
                   text("ponto de retorno", 26, opacity=0.9)).move_to([0, -4.3, 0])
        self.play(soft_swap(n1, n2), run_time=0.7)
        self.wait(1.3)
        self.play(T.CV.animate.set_value(0), run_time=0.4)
        T.CS.set_value(0.3)
        n3 = mixed(tex(r"U>E", 32, BLUE_L), text("→ posição proibida", 26, opacity=0.9)).move_to([0, -4.3, 0])
        self.play(T.CV.animate.set_value(1), soft_swap(n2, n3), run_time=0.8)
        self.wait(1.8)
        self.play(T.CV.animate.set_value(0), FadeOut(n3), run_time=0.5)
        # conjunto permitido no eixo espacial
        n4 = text("as posições com K ≥ 0 formam o conjunto permitido", 24, opacity=0.9).move_to([0, -4.3, 0])
        self.play(T.RG.animate.set_value(1), FadeIn(n4, shift=UP * 0.1), run_time=1.2)
        self.wait(1.4)
        self.play(FadeOut(n4), run_time=0.4)

    # ── S7 Regimes ──────────────────────────────────────────────────────────
    def regime_in(self, E, traj, dl, lab, cap):
        """Nova condição inicial: retira a partícula e o nível anteriores, muda E, mostra o novo nível e a partícula."""
        T = self.T
        self.play(T.RG.animate.set_value(0), T.LA.animate.set_value(0), T.FB.animate.set_value(0), run_time=0.5)
        T.E.set_value(E)
        T.DL.set_value(dl)
        self.traj = traj
        T.TT.set_value(0)
        self.play(T.LA.animate.set_value(1), T.RG.animate.set_value(1), FadeIn(lab, shift=UP * 0.1),
                  FadeIn(cap, shift=UP * 0.1), run_time=0.7)
        self.play(T.VP.animate.set_value(1), T.KB.animate.set_value(1), run_time=0.6)

    def go(self, t, *anims):
        """Avança o tempo da trajetória até t (linear, sem pausa); `anims` correm junto, com a mesma duração."""
        cur = self.T.TT.get_value()
        self.play(self.T.TT.animate.set_value(t), *anims, run_time=t - cur, rate_func=linear)

    def s7(self):
        T = self.T
        # E = 0 ---------------------------------------------------------------------------------------------
        lab0 = mt("E", "=", "0", size=58, colors={0: BLUE_L}).move_to([0, 5.3, 0])
        cap0 = text("repouso em um dos mínimos", 26, opacity=0.9).move_to([0, 4.45, 0])
        self.play(T.RG.animate.set_value(0), run_time=0.4)
        self.regime_in(0.0, traj_rest, 0.0, lab0, cap0)
        self.wait(2.2)
        # 0 < E < U_b -----------------------------------------------------------------------------------------
        lab1 = mt("0", "<", "E", "<", "U_b", size=58, colors={2: BLUE_L, 4: MAGENTA}).move_to([0, 5.3, 0])
        cap1 = text("movimento confinado a um único poço", 26, opacity=0.9).move_to([0, 4.45, 0])
        self.play(FadeOut(VGroup(lab0, cap0)), T.VP.animate.set_value(0), T.KB.animate.set_value(0), run_time=0.4)
        self.regime_in(E_SUB, traj_sub, 1.0, lab1, cap1)
        self.mark("sub-barreira")
        tm1, tp1, tm2, tp2 = SUB_MIN[0], SUB_TP[0], SUB_MIN[1], SUB_TP[1]
        slot = [0, -4.3, 0]
        nA = text("retorno: K = 0", 26, opacity=0.95).move_to(slot)
        nB = text("no mínimo, K é máximo: maior rapidez", 24, opacity=0.95).move_to(slot)
        nC = text("retorno: K = 0 (a partícula volta)", 26, opacity=0.95).move_to(slot)
        nD = text("retorno: K = 0", 26, opacity=0.95).move_to(slot)
        self.timed(nA, 0.0, 1.0)
        self.timed(nB, tm1 - 0.1, tm1 + 1.0)
        self.timed(nC, tp1 - 0.2, tp1 + 0.9)
        self.timed(nD, tp2 - 0.2, tp2 + 0.9)
        forb = text("proibido: U > E", 22, MAGENTA).move_to([0, PY + 0.5, 0])
        self.add(forb)
        T.FB.set_value(1)
        self.go(tp2 + 1.0)
        self.clear_timed()
        self.go(tp2 + 1.4, FadeOut(forb), T.VP.animate.set_value(0), T.KB.animate.set_value(0))
        # E = U_b -----------------------------------------------------------------------------------------------
        lab2 = mt("E", "=", "U_b", size=58, colors={0: BLUE_L, 2: MAGENTA}).move_to([0, 5.3, 0])
        cap2 = mixed(text("aproxima-se de", 26, opacity=0.9), tex("x=0", 32), text("sem chegar", 26, opacity=0.9)
                     ).move_to([0, 4.45, 0])
        self.play(FadeOut(VGroup(lab1, cap1)), T.FB.animate.set_value(0), run_time=0.4)
        self.regime_in(E_SEP, traj_sep, 1.0, lab2, cap2)
        self.mark("separatriz")
        lim = mt(r"x\to0", r",\quad", r"K\to0", r",\quad", r"t\to\infty", size=38).move_to(slot)
        ex = VGroup(text("repouso exato em x = 0 é outro caso:", 22, opacity=0.9),
                    text("equilíbrio instável", 22, opacity=0.9)).arrange(DOWN, buff=0.08).move_to([0, -4.4, 0])
        self.timed(lim, 1.2, 3.4)
        self.timed(ex, 3.7, 99.0)
        self.go(6.2)
        self.clear_timed()
        self.add(ex)
        self.go(6.6, FadeOut(ex), T.VP.animate.set_value(0), T.KB.animate.set_value(0))
        # E > U_b -----------------------------------------------------------------------------------------------
        lab3 = mt("E", ">", "U_b", size=58, colors={0: BLUE_L, 2: MAGENTA}).move_to([0, 5.3, 0])
        cap3 = mixed(text("atravessa", 26, opacity=0.9), tex("x=0", 32), text("e volta nos extremos", 26, opacity=0.9)
                     ).move_to([0, 4.45, 0])
        self.play(FadeOut(VGroup(lab2, cap2)), run_time=0.4)
        self.regime_in(E_SUP, traj_sup, 0.0, lab3, cap3)
        self.mark("travessia")
        tc1, tp_a, tp_b = SUP_CEN[0], SUP_TP[0], SUP_TP[1]
        n_a = text("retorno externo: K = 0", 26, opacity=0.95).move_to(slot)
        n_b = text("no centro, K > 0: atravessa a barreira", 24, opacity=0.95).move_to(slot)
        n_c = text("retorno externo: K = 0, o sentido muda", 24, opacity=0.95).move_to(slot)
        n_d = text("U cresce nos extremos: o movimento é limitado", 24, opacity=0.95).move_to(slot)
        self.timed(n_a, 0.0, 1.0)
        self.timed(n_b, tc1 - 0.5, tc1 + 0.9)
        self.timed(n_c, tp_a - 0.3, tp_a + 1.0)
        self.timed(n_d, tp_a + 1.2, tp_a + 2.8)
        self.go(tp_a + 2.8)
        self.clear_timed()
        self.s7_cleanup = VGroup(lab3, cap3)
        self.mark("retorno externo")

    # ── S8 Coda ─────────────────────────────────────────────────────────────
    def s8(self):
        T = self.T
        title = display("PAISAGEM DE ENERGIA", 36).move_to([0, 5.6, 0])
        chip_t = text("ANALOGIA", 22, MAGENTA)
        chip = SurroundingRectangle(chip_t, color=MAGENTA, buff=0.16, corner_radius=0.12, stroke_width=2.5)
        chip_g = VGroup(chip, chip_t).move_to([0, 4.9, 0])
        t0 = T.TT.get_value()
        # a trajetória continua (sem reiniciar): linha E e barra K saem, a partícula real permanece no eixo x
        # e o marcador da analogia nasce na vertical da partícula, sobre a curva
        self.go(t0 + 1.4, soft_swap(self.s7_cleanup, VGroup(title, chip_g)),
                T.LA.animate.set_value(0), T.RG.animate.set_value(0), T.KB.animate.set_value(0),
                T.KL.animate.set_value(0), T.VP.animate.set_value(0.6), FadeIn(self.land))
        note = text("O eixo vertical representa energia.", 26, opacity=0.9).move_to([0, -3.65, 0])
        self.go(T.TT.get_value() + 1.2, T.BALL.animate.set_value(1), FadeIn(note, shift=UP * 0.1))
        self.go(T.TT.get_value() + 1.3)
        # recapitulação, um regime por vez
        recap = [
            mixed(tex(r"0\le E<U_b", 40, BLUE_L), text("permanece de um lado", 26)),
            mixed(tex(r"E=U_b", 40, BLUE_L), text("separatriz: x → 0 sem chegar", 26)),
            mixed(tex(r"E>U_b", 40, BLUE_L), text("atravessa, com retornos externos", 26)),
        ]
        cur = None
        for r in recap:
            r.move_to([0, 4.4, 0])
            if r.width > 7.8:
                r.scale_to_fit_width(7.8)
            t = T.TT.get_value()
            if cur is None:
                self.go(t + 2.2, FadeIn(r, shift=UP * 0.1))
            else:
                self.go(t + 2.2, soft_swap(cur, r))
            cur = r
        self.go(T.TT.get_value() + 1.0)
