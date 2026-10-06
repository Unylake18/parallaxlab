"""Potencial de poço duplo a partir da força F(x) = F0 [x/ℓ − (x/ℓ)³]: preview silencioso (V4).

DA EQUAÇÃO AO FENÔMENO · EP. 04.
Pergunta (referência de narração): "Conhecendo a força que atua numa partícula, o que podemos descobrir sobre seu
movimento?" Complemento: "Vamos construir a energia potencial e descobrir onde essa partícula pode ir — sem resolver x(t)."
Encerramento: "Da força, encontramos o potencial. Com a energia, descobrimos onde a partícula pode ir — sem resolver x(t)."

Percurso: força dada -> potencial construído -> gráfico justificado -> movimento previsto pela energia.

  S1  esquema 1D (eixo x, partícula, posição x, seta de força); F(x) dado; zeros; posições de teste estáticas
      (a força volta para ±ℓ e afasta de 0); F(ℓ/2) = 3F0/8 levado ao gráfico; F(−x) = −F(x); curva traçada por um cursor
  S2  DA FORÇA AO POTENCIAL: F = −U′ -> U = −∫F dx -> ... -> U = −F0x²/(2ℓ) + F0x⁴/(4ℓ³) + C (cada passo em uma linha completa)
  S3  ONDE COLOCAMOS O ZERO DE ENERGIA?: U(±ℓ) = 0 -> substituir x = ℓ -> C = F0ℓ/4
  S4  C substituído -> trinômio -> quadrado perfeito; conferência −U′ = F
  S5  DOIS MÍNIMOS E UMA BARREIRA: pontos calculados, U′ = −F (tangentes), U(ℓ/2), U(−x) = U(x), U ~ x⁴, curva por cursor
  S6  ONDE A PARTÍCULA PODE IR?: E = K + U -> K = E − U ≥ 0 -> U ≤ E; cursor de leitura de K; regiões permitidas
  S7  regimes (cada E é uma nova condição inicial), destaques ligados ao tempo físico da trajetória
  S8  resumo: os três comportamentos, FORÇA → POTENCIAL → POSIÇÕES PERMITIDAS, @labparallax

Gráfico de energia adimensional: x em unidades de ℓ, U em unidades de U_b = F0ℓ/4: u(x) = (x² − 1)².
O esquema (eixo x) fica sempre abaixo dos gráficos e com a mesma escala horizontal.
Dinâmica: ẍ = −κ u′(x) (m = 1), κ = 0,2, RK4 nos regimes limitados; a separatriz usa a solução exata √2 sech(a t),
a = 2√κ·s com s = 0,7 (fator de exibição); nenhuma x(t) aparece no vídeo.

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
    Indicate, Line, MathTex, Rotate, Scene, SurroundingRectangle, VGroup, VMobject, ValueTracker, always_redraw,
    config, linear, smooth,
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
S_SEP = 0.7               # fator de exibição da separatriz (reparametrização da apresentação)
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
_TS_SUP, _XS_SUP, _VS_SUP = _rk4(-allowed(E_SUP)[0][1], 0.0, 20.0)


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
    # zeros: F(x) = 0 <=> (x/ℓ)[1 − (x/ℓ)²] = 0 <=> x = −ℓ, 0, ℓ ; F é ímpar; valores de teste
    assert np.allclose(f_force(xs), xs * (1 - xs ** 2))
    assert f_force(0.0) == 0 and f_force(1.0) == 0 and f_force(-1.0) == 0
    assert np.allclose(f_force(-xs), -f_force(xs))
    assert np.isclose(f_force(0.5), 3 / 8) and np.isclose(0.5 - 0.5 ** 3, 0.5 - 1 / 8)
    assert np.isclose(f_force(1.5), -15 / 8) and np.isclose(f_force(0.25), 15 / 64)
    # a força aponta de volta para ±ℓ dos dois lados de ℓ e afasta de 0
    assert f_force(0.5) > 0 and f_force(1.5) < 0 and f_force(0.25) > 0 and f_force(-0.25) < 0
    # inclinações de U (U′ = −F): decrescente em (0, ℓ), crescente em (−ℓ, 0)
    assert du(0.5) < 0 and du(-0.5) > 0 and du(1.35) > 0 and du(-1.35) < 0
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
    # posições escolhidas para a leitura de K: permitida (K > 0), no limite (K = 0) e inacessível (U > E)
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
    # separatriz: √2 sech(a t) (a = 2√κ·s, s = fator de exibição) conserva E = U_b na escala s, é monótona e
    # decresce para 0 sem nunca chegar nem cruzar
    s = A_SEP / (2 * np.sqrt(KAPPA))
    assert np.isclose(s, S_SEP)
    t = np.linspace(0, 9, 4501)
    xs_ = np.array([traj_sep(v) for v in t])
    vs_ = np.gradient(xs_, t)
    assert np.max(np.abs(0.5 * vs_[5:-5] ** 2 + KAPPA * s ** 2 * u(xs_[5:-5]) - KAPPA * s ** 2 * E_SEP)) < 1e-4
    assert np.all(np.diff(xs_) < 0) and xs_.min() > 0
    assert np.isclose(traj_sep(0.0), np.sqrt(2)) and np.isclose(u(np.sqrt(2)), E_SEP)
    assert traj_sep(5.6) > 0.07                                  # ainda longe de x = 0 no fim da exibição


_qa()

# ── Geometria da tela (frame 9 × 16) ────────────────────────────────────────
# Todos os gráficos usam x em unidades de ℓ com a mesma escala horizontal do esquema (eixo x) que fica abaixo deles.
GSX, GX0 = 1.9, 0.0       # tela por ℓ
GY0, GSY = -0.35, 1.6     # gráfico de energia: U = 0 e tela por U_b
AXL, AXR = -3.4, 3.4      # eixo vertical e extensão horizontal
XR = 1.6                  # domínio do gráfico de U: |x| ≤ 1,6 ℓ
PY = -2.7                 # esquema (eixo espacial da partícula) abaixo dos gráficos
AY = 0.9                  # altura do esquema na abertura (desce até PY quando o gráfico de F nasce)
FY0, FSY, FXR = 0.95, 1.25, 1.45      # gráfico de F: eixo x, tela por F0 e domínio
FAX = -3.45               # eixo vertical F
TITLE_Y, APOIO_Y = 6.35, 5.4


def gx(x):
    return GX0 + GSX * x


def gy(uu):
    return GY0 + GSY * uu


def gpt(x):
    return np.array([gx(x), gy(u(x)), 0.0])


def fpt(x):
    return np.array([gx(x), FY0 + FSY * f_force(x), 0.0])


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
    return VGroup(*(display(s, size) for s in strs)).arrange(DOWN, buff=0.12)


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
    """Barra K = E − U(x) em x: sólida se U ≤ E; tracejada magenta (posição inacessível) se U > E."""
    g = VGroup()
    if u(x) <= E + 1e-9:
        if gy(E) - gy(u(x)) > 0.03:
            g.add(seg((gx(x), gy(u(x))), (gx(x), gy(E)), stroke_width=6, color=KCOL).set_opacity(alpha).set_z_index(4))
    else:
        g.add(DashedLine([gx(x), gy(E), 0], [gx(x), gy(u(x)), 0], color=MAGENTA, stroke_width=4, dash_length=0.08)
              .set_opacity(0.8 * alpha))
    return g


def pdot(x, y=PY, vp=1.0):
    """Partícula branca (com halo discreto) na posição x (em ℓ), à altura y."""
    return VGroup(Dot([gx(x), y, 0], radius=0.19, color=WHITE).set_opacity(0.18 * vp),
                  Dot([gx(x), y, 0], radius=0.09, color=WHITE).set_opacity(vp)).set_z_index(5)


def farrow(x, direc, y, length=0.75):
    """Seta de força ligada à partícula em x: do raio da partícula até `length` na direção `direc`."""
    return Arrow([gx(x) + 0.2 * direc, y, 0], [gx(x) + (0.2 + length) * direc, y, 0], buff=0, color=CYAN,
                 stroke_width=6, max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=10).set_z_index(4)


class PotencialPocoDuplo013(Scene):

    def mark(self, name):
        print(f"[MARCA] {self.renderer.time:7.2f} s  {name}")

    def xp(self):
        return float(self.traj(self.T.TT.get_value()))

    # ── Utilidades de cena ──────────────────────────────────────────────────
    def titulo(self, linhas, apoio=None, size=34):
        """Troca título e apoio (poucos títulos, uma instrução curta por vez)."""
        if isinstance(linhas, str):
            linhas = (linhas,)
        new_t = lines(*linhas, size=size).move_to([0, TITLE_Y, 0])
        new_a = text(apoio, 26, opacity=0.95).move_to([0, APOIO_Y, 0]) if apoio else None
        outs, ins = [], [FadeIn(new_t, shift=UP * 0.1)]
        if getattr(self, "_title", None) is not None:
            outs.append(FadeOut(self._title))
        if getattr(self, "_apoio", None) is not None:
            outs.append(FadeOut(self._apoio))
        if new_a is not None:
            ins.append(FadeIn(new_a, shift=UP * 0.1))
        if outs:
            self.play(*outs, run_time=0.3)
        self.play(*ins, run_time=0.5)
        self._title, self._apoio = new_t, new_a

    def apoio_swap(self, apoio, run_time=0.6):
        new_a = text(apoio, 26, opacity=0.95).move_to([0, APOIO_Y, 0])
        if getattr(self, "_apoio", None) is not None:
            self.play(soft_swap(self._apoio, new_a), run_time=run_time)
        else:
            self.play(FadeIn(new_a, shift=UP * 0.1), run_time=run_time)
        self._apoio = new_a

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
            FB=ValueTracker(0),          # trecho central inacessível (0 < E < U_b)
            CV=ValueTracker(0),          # cursor de leitura de K (S6)
            CS=ValueTracker(1.15),       # posição do cursor
            TT=ValueTracker(0),          # tempo da trajetória
            FX=ValueTracker(0),          # cursor de F(x) (S1)
            FV=ValueTracker(0),
            UX=ValueTracker(0),          # cursor de U(x) (S5)
            UV=ValueTracker(0),
        )
        self._timed = []
        self._title = self._apoio = None
        self.traj = traj_rest

        # Cursor que traça a curva de F: posição no esquema (anel), projeção até o gráfico e ponto (x, F(x))
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
            g.add(DashedLine([p[0], PY + 0.14, 0], p, color=WHITE, stroke_width=1.6, dash_length=0.08).set_opacity(0.45 * fv))
            g.add(DashedLine([FAX, p[1], 0], p, color=CYAN, stroke_width=1.6, dash_length=0.08).set_opacity(0.5 * fv))
            g.add(Circle(radius=0.1, color=KCOL, stroke_width=3.5).move_to([p[0], PY, 0]).set_stroke(opacity=fv))
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
            g.add(DashedLine([p[0], PY + 0.14, 0], p, color=WHITE, stroke_width=1.6, dash_length=0.08).set_opacity(0.45 * uv))
            g.add(DashedLine([AXL, p[1], 0], p, color=VIOLET, stroke_width=1.6, dash_length=0.08).set_opacity(0.5 * uv))
            g.add(Circle(radius=0.1, color=KCOL, stroke_width=3.5).move_to([p[0], PY, 0]).set_stroke(opacity=uv))
            g.add(Dot(p, radius=0.09, color=WHITE).set_opacity(uv).set_z_index(5))
            return g

        self.u_trace = always_redraw(u_trace)

        # Gráfico de energia
        self.u_curve = VMobject(color=VIOLET, stroke_width=5).set_points_smoothly(
            [gpt(x) for x in np.linspace(-XR, XR, 161)])
        self.u_axis = Arrow([AXL, GY0 - 0.2, 0], [AXL, 3.75, 0], buff=0, stroke_width=2.5, tip_length=0.16,
                            color=WHITE).set_opacity(0.6)
        self.u_label = tex("U", 34, VIOLET).move_to([AXL - 0.32, 3.65, 0])
        self.base = Line([AXL, GY0, 0], [AXR, GY0, 0], stroke_width=2, color=WHITE).set_opacity(0.4)
        self.ub_level = DashedLine([AXL, gy(1), 0], [gx(0), gy(1), 0], color=MAGENTA, stroke_width=2.5,
                                   dash_length=0.12).set_opacity(0.85)
        self.ub_dot = Dot([gx(0), gy(1), 0], radius=0.1, color=MAGENTA).set_z_index(3)
        self.ub_tick = tex(r"U_b", 30, MAGENTA).move_to([AXL - 0.42, gy(1), 0])
        self.well_dots = VGroup(*(Dot([gx(s), GY0, 0], radius=0.09, color=VIOLET).set_z_index(3) for s in (-1, 1)))

        # Esquema (eixo espacial): aparece na abertura e depois fica abaixo dos gráficos
        self.p_axis = Arrow([AXL, PY, 0], [AXR, PY, 0], buff=0, stroke_width=2.5, tip_length=0.16,
                            color=WHITE).set_opacity(0.65)
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
        self.p_base = VGroup(self.p_axis, self.p_x)
        self.p_marks = VGroup(self.p_ticks, self.p_labels)

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
            return 1 - 0.65 * T.DL.get_value() if x0 < 0 else 1.0

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
            return pdot(self.xp(), PY, vp)

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
        self.wait(0.5)

    # ── S1 Esquema, força dada, zeros, posições de teste, ponto, simetria e curva ──
    def s1(self):
        T = self.T
        self.add(self.f_trace)
        sh = AY - PY
        self.p_base.shift(UP * sh)
        self.p_marks.shift(UP * sh)
        # abertura: esquema de movimento em uma dimensão (eixo de posição, partícula, posição x, seta de força)
        self.titulo(("O QUE A FORÇA REVELA", "SOBRE O MOVIMENTO?"), "Esquema de movimento em uma dimensão.")
        part = pdot(0.5, AY)
        xl = VGroup(seg((gx(0.5), AY - 0.1), (gx(0.5), AY - 0.28), stroke_width=3, color=KCOL),
                    tex("x", 32, KCOL).move_to([gx(0.5), AY - 0.55, 0]))
        arr0 = farrow(0.5, 1, AY)
        lab0 = text("força", 26, CYAN).move_to([gx(0.5) + 0.65, AY + 0.5, 0])
        self.play(FadeIn(self.p_base), FadeIn(part, scale=0.5), run_time=0.8)
        self.play(FadeIn(xl, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(arr0, shift=RIGHT * 0.2), FadeIn(lab0), run_time=0.7)
        self.wait(0.6)
        # a força é dada
        self.titulo(("A FORÇA DEPENDE", "DA POSIÇÃO"), "Cada posição determina um valor de força.")
        f_top = mt("F(x)", "=", "F_0", r"\left[\frac{x}{\ell}-\left(\frac{x}{\ell}\right)^3\right]", r",\quad F_0>0,\ \ell>0",
                   size=38, colors={0: CYAN}, maxw=7.6).move_to([0, 4.35, 0])
        self.play(FadeIn(f_top, shift=UP * 0.1), FadeOut(arr0), FadeOut(lab0), run_time=0.9)
        # zeros
        z1 = mt("F(x)", r"=0\;\Rightarrow\;", r"\frac{x}{\ell}\left[1-\left(\frac{x}{\ell}\right)^2\right]", "=0",
                size=34, colors={0: CYAN}).move_to([0, 3.4, 0])
        z2 = mt("x", "=", r"-\ell,\;0,\;+\ell", size=42).move_to([0, 2.6, 0])
        self.play(FadeIn(z1, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(z2, shift=UP * 0.1), FadeIn(self.p_marks), run_time=0.9)
        zeros = VGroup(*(Dot([gx(z), AY, 0], radius=0.09, color=WHITE).set_z_index(3) for z in (-1, 0, 1)))
        self.play(AnimationGroup(*(FadeIn(d, scale=0.4) for d in zeros), lag_ratio=0.25), FadeOut(z1), run_time=0.8)
        self.mark("zeros")
        # posição de teste 1: F(ℓ/2) = 3F0/8 > 0 -> força para a direita
        cal1 = mt(r"F\!\left(\frac{\ell}{2}\right)", "=", "F_0", r"\left(\frac12-\frac18\right)", "=", r"\frac{3F_0}{8}",
                  r">0", size=36, colors={0: CYAN}, maxw=7.4).move_to([0, -0.55, 0])
        a1 = farrow(0.5, 1, AY, 0.6)
        l1 = VGroup(text("Força para", 22, CYAN), text("a direita", 22, CYAN)).arrange(DOWN, buff=0.05)
        l1.move_to([gx(0.5) + 0.1, AY + 0.85, 0])
        self.play(FadeIn(cal1, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(a1, shift=RIGHT * 0.2), FadeIn(l1), run_time=0.7)
        self.wait(0.5)
        # posição de teste 2, do outro lado de ℓ: a força aponta de volta
        part2 = pdot(1.5, AY)
        cal2 = mt(r"F\!\left(\frac{3\ell}{2}\right)", "=", r"-\frac{15F_0}{8}", r"<0", size=36, colors={0: CYAN},
                  maxw=7.4).move_to([0, -1.5, 0])
        a2 = farrow(1.5, -1, AY, 0.6)
        l2 = VGroup(text("Força para", 22, CYAN), text("a esquerda", 22, CYAN)).arrange(DOWN, buff=0.05)
        l2.move_to([gx(1.5) - 0.05, AY + 0.85, 0])
        self.apoio_swap("Dos dois lados de x = ℓ, a força aponta de volta.")
        self.play(FadeIn(part2, scale=0.5), FadeIn(cal2, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(a2, shift=LEFT * 0.2), FadeIn(l2), run_time=0.7)
        self.wait(1.0)
        # perto do centro: pequena perturbação, a força afasta
        part3 = VGroup(pdot(0.3, AY), pdot(-0.3, AY))
        cal3 = mt(r"F(\pm\ell/4)", "=", r"\pm\frac{15F_0}{64}", size=36, colors={0: CYAN}).move_to([0, -0.55, 0])
        a3 = VGroup(farrow(0.3, 1, AY, 0.55), farrow(-0.3, -1, AY, 0.55))
        l3 = text("afasta do centro", 24, CYAN).move_to([0, AY + 0.65, 0])
        self.apoio_swap("Perto de x = 0, a força afasta.")
        self.play(FadeOut(VGroup(part, part2, a1, a2, l1, l2, cal1, cal2, xl)), run_time=0.5)
        self.play(FadeIn(part3, scale=0.5), FadeIn(cal3, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(a3), FadeIn(l3), run_time=0.6)
        self.wait(1.0)
        self.mark("posicoes de teste")
        # o esquema desce; nasce o gráfico de F; o ponto calculado (ℓ/2, 3F0/8) é levado ao gráfico
        vaxis = Arrow([FAX, FY0 - 2.2, 0], [FAX, FY0 + 2.25, 0], buff=0, stroke_width=2.5, tip_length=0.16,
                      color=WHITE).set_opacity(0.6)
        vlab = tex("F", 34, CYAN).move_to([FAX + 0.32, FY0 + 2.3, 0])
        haxis = Line([AXL, FY0, 0], [AXR, FY0, 0], stroke_width=2, color=WHITE).set_opacity(0.5)
        hx = tex("x", 30).move_to([AXR - 0.05, FY0 - 0.32, 0])
        stay = VGroup(self.p_base, self.p_marks, zeros)
        self.apoio_swap("Cada posição determina um valor de força.")
        self.play(FadeOut(VGroup(part3, a3, l3, cal3, z2)), stay.animate.shift(DOWN * sh), run_time=0.9)
        self.play(FadeIn(vaxis), FadeIn(vlab), FadeIn(haxis), FadeIn(hx), run_time=0.7)
        part = pdot(0.5, PY)
        pt = fpt(0.5)
        vline = DashedLine([pt[0], PY + 0.16, 0], pt, color=WHITE, stroke_width=1.8, dash_length=0.08).set_opacity(0.7)
        hline = DashedLine(pt, [FAX, pt[1], 0], color=CYAN, stroke_width=1.8, dash_length=0.08).set_opacity(0.7)
        pdt = Dot(pt, radius=0.09, color=WHITE).set_z_index(5)
        plab = tex(r"\frac{3F_0}{8}", 30, CYAN).move_to([FAX - 0.6, pt[1], 0])
        self.play(FadeIn(part, scale=0.5), run_time=0.4)
        self.play(Create(vline), run_time=0.7)
        self.play(FadeIn(pdt, scale=0.5), Create(hline), FadeIn(plab, shift=RIGHT * 0.1), run_time=0.7)
        # F é ímpar
        odd = mt("F(-x)", "=", "-", "F(x)", size=42, colors={0: CYAN, 3: CYAN}).move_to([0, 3.5, 0])
        self.play(FadeIn(odd, shift=UP * 0.1), run_time=0.6)
        grp = VGroup(vline, pdt).copy()
        self.add(grp)
        pt2 = np.array([-pt[0], 2 * FY0 - pt[1], 0])
        hline2 = DashedLine(pt2, [FAX, pt2[1], 0], color=CYAN, stroke_width=1.8, dash_length=0.08).set_opacity(0.7)
        plab2 = tex(r"-\frac{3F_0}{8}", 30, CYAN).move_to([FAX - 0.7, pt2[1], 0])
        self.play(Rotate(grp, PI, about_point=np.array([0, FY0, 0])), run_time=1.1)
        self.play(Create(hline2), FadeIn(plab2, shift=RIGHT * 0.1), run_time=0.6)
        # a curva é traçada por um cursor (x, F(x)): lado direito calculado, lado esquerdo pela simetria
        self.play(FadeOut(VGroup(vline, hline, pdt, plab, grp, hline2, plab2, part)), run_time=0.5)
        T.FX.set_value(0)
        self.play(T.FV.animate.set_value(1), run_time=0.4)
        self.play(T.FX.animate.set_value(FXR), run_time=3.0, rate_func=smooth)
        right = VMobject(color=CYAN, stroke_width=5).set_points_smoothly([fpt(v) for v in np.linspace(0, FXR, 90)])
        self.add(right)
        T.FV.set_value(0)
        left = right.copy()
        self.add(left)
        self.play(Rotate(left, PI, about_point=np.array([0, FY0, 0])), run_time=1.3)
        self.mark("curva F")
        self.wait(0.4)
        self.s1_all = VGroup(vaxis, vlab, haxis, hx, right, left, f_top, odd, self.p_base, self.p_marks, zeros)

    # ── S2 DA FORÇA AO POTENCIAL ────────────────────────────────────────────
    def passo(self, old, new, y_new, y_old=3.9, hold=0.8):
        """Nova linha (completa) entra abaixo da anterior; depois a anterior sai e a nova sobe para o seu lugar."""
        new.move_to([0, y_new, 0])
        self.play(FadeIn(new, shift=UP * 0.1), run_time=0.7)
        self.wait(hold)
        if old is not None:
            self.play(FadeOut(old), new.animate.move_to([0, y_old, 0]), run_time=0.6)
        return new

    def s2(self):
        self.play(FadeOut(self.s1_all), run_time=0.8)
        self.titulo("DA FORÇA AO POTENCIAL", "Integramos com o sinal trocado.")
        SZ = 48
        b1 = mt("F(x)", "=", "-", "U'(x)", size=SZ + 8, colors={0: CYAN, 3: VIOLET}).move_to([0, 3.9, 0])
        self.play(FadeIn(b1, shift=UP * 0.1), run_time=0.9)
        self.wait(0.4)
        b2 = mt("U(x)", "=", "-", r"\int", "F(x)", r"\,dx", size=SZ, colors={0: VIOLET, 4: CYAN})
        self.play(b1.animate.set_opacity(0.7), run_time=0.3)
        b2 = self.passo(None, b2, 2.5)
        b3 = mt("U(x)", "=", "-", "F_0", r"\int", r"\Big(\frac{x}{\ell}-\frac{x^3}{\ell^3}\Big)", r"\,dx", size=SZ,
                colors={0: VIOLET, 3: CYAN, 5: CYAN})
        self.play(FadeOut(b1), b2.animate.move_to([0, 3.9, 0]), run_time=0.6)
        b3 = self.passo(b2, b3, 2.5, hold=0.9)
        # a integral é aplicada a cada termo e 1/ℓ, 1/ℓ³ saem da integral (duas linhas, bloco único)
        r1 = mt("U(x)", "=", "-", "F_0", r"\Big[", r"\frac{1}{\ell}", r"\int x\,dx", size=SZ,
                colors={0: VIOLET, 3: CYAN, 5: BLUE_L}, maxw=None)
        r2 = mt("-", r"\frac{1}{\ell^3}", r"\int x^3\,dx", r"\Big]", "+C", size=SZ, colors={1: BLUE_L}, maxw=None)
        r2.align_to(r1[4], LEFT)
        b4 = VGroup(r1, r2.next_to(r1, DOWN, buff=0.25, aligned_edge=LEFT)).move_to([0, 2.0, 0])
        r2.align_to(r1[4], LEFT)
        b4 = self.passo(b3, b4, 1.5, y_old=3.4, hold=1.1)
        self.play(Indicate(b4[0][5], color=BLUE_L), Indicate(b4[1][1], color=BLUE_L), run_time=0.8)
        self.mark("integral separada")
        # primitivas: ∫x dx → x²/2 e ∫x³ dx → x⁴/4
        b5 = mt("U(x)", "=", "-", "F_0", r"\Big[", r"\frac{x^2}{2\ell}", "-", r"\frac{x^4}{4\ell^3}", r"\Big]", "+C",
                size=SZ, colors={0: VIOLET, 3: CYAN})
        prim = mt(r"\int x\,dx\to\frac{x^2}{2}", r"\qquad", r"\int x^3\,dx\to\frac{x^4}{4}", size=36, maxw=7.4)
        prim.move_to([0, 0.0, 0])
        self.play(FadeIn(prim, shift=UP * 0.1), Indicate(b4[0][6], color=BLUE_L), Indicate(b4[1][2], color=BLUE_L),
                  run_time=0.9)
        b5.move_to([0, 0.0 - 1.4, 0])
        b5 = self.passo(None, b5, -1.5, hold=1.0)
        self.play(FadeOut(prim), FadeOut(b4), b5.animate.move_to([0, 3.4, 0]), run_time=0.7)
        mult = mixed(tex("-F_0", 34), text("multiplica cada termo", 24, opacity=0.95)).move_to([0, 1.0, 0])
        b6 = mt("U(x)", "=", r"-\frac{F_0x^2}{2\ell}", r"+\frac{F_0x^4}{4\ell^3}", "+C", size=SZ, colors={0: VIOLET})
        self.play(FadeIn(mult, shift=UP * 0.1), run_time=0.5)
        b6 = self.passo(b5, b6, 2.1, y_old=3.9, hold=1.0)
        self.play(FadeOut(mult), run_time=0.3)
        self.b6 = b6

    # ── S3 ONDE COLOCAMOS O ZERO DE ENERGIA? ────────────────────────────────
    def s3(self):
        b6 = self.b6
        self.titulo(("ONDE COLOCAMOS O", "ZERO DE ENERGIA?"), "Escolhemos energia zero em x = ±ℓ.")
        self.play(b6.animate.move_to([0, 4.4, 0]), run_time=0.6)
        c1 = mt("U(", r"\pm\ell", ")", "=", "0", size=54, colors={0: VIOLET, 2: VIOLET}).move_to([0, 3.3, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.8)
        t2 = mixed(text("pela simetria, substituímos", 24, opacity=0.95), tex(r"x=\ell", 32)).move_to([0, 2.55, 0])
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.6)
        # cadeia alinhada: cada linha completa permanece à vista
        ph = r"\phantom{0=U(\ell)}"
        ra = mt("0", "=", r"U(\ell)", "=", r"-\frac{F_0\ell^2}{2\ell}", r"+\frac{F_0\ell^4}{4\ell^3}", "+C", size=44,
                colors={2: VIOLET}, maxw=None)
        rb = mt(ph, "=", r"-\frac{F_0\ell}{2}", r"+\frac{F_0\ell}{4}", "+C", size=44, maxw=None)
        rc = mt(ph, "=", r"-\frac{F_0\ell}{4}", "+C", size=44, maxw=None)
        chain = VGroup(ra, rb, rc).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([0, 0.15, 0])
        self.play(FadeIn(ra, shift=UP * 0.1), run_time=0.9)
        self.wait(0.5)
        self.play(FadeIn(rb, shift=UP * 0.1), run_time=0.8)
        self.wait(0.4)
        self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.8)
        self.wait(0.4)
        box = mt("C", "=", r"\frac{F_0\ell}{4}", size=62, colors={0: MAGENTA, 2: MAGENTA}).move_to([0, -2.8, 0])
        bx = SurroundingRectangle(box, color=MAGENTA, buff=0.2, corner_radius=0.1, stroke_width=3)
        self.play(FadeIn(box, shift=UP * 0.1), Create(bx), run_time=0.9)
        self.mark("C")
        note = text("A referência muda; a força permanece.", 26, opacity=0.95).move_to([0, -4.15, 0])
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.wait(1.0)
        self.s3_all = VGroup(c1, t2, chain, note)
        self.box, self.bx = box, bx

    # ── S4 Substituição de C e fatoração ────────────────────────────────────
    def s4(self):
        b6, box, bx = self.b6, self.box, self.bx
        self.play(FadeOut(self.s3_all), FadeOut(bx), FadeOut(box), run_time=0.6)
        self.apoio_swap("Substituímos C e fatoramos.")
        r1 = mt("U(x)", "=", r"-\frac{F_0x^2}{2\ell}", r"+\frac{F_0x^4}{4\ell^3}", r"+\frac{F_0\ell}{4}", size=48,
                colors={0: VIOLET, 4: MAGENTA}).move_to([0, 4.4, 0])
        self.play(FadeOut(b6), FadeIn(r1, shift=UP * 0.1), run_time=0.9)
        r2 = mt("U(x)", "=", r"\frac{F_0\ell}{4}", r"\Big[\Big(\frac{x}{\ell}\Big)^4-2\Big(\frac{x}{\ell}\Big)^2+1\Big]",
                size=48, colors={0: VIOLET, 2: MAGENTA}).move_to([0, 2.9, 0])
        self.play(FadeIn(r2, shift=UP * 0.1), Indicate(r1[4], color=MAGENTA, scale_factor=1.2), run_time=1.0)
        self.wait(0.6)
        ident = mt(r"a=\Big(\frac{x}{\ell}\Big)^2", r"\;:\quad", r"a^2-2a+1", "=", r"(a-1)^2", size=42,
                   colors={2: BLUE_L, 4: BLUE_L}).move_to([0, 1.4, 0])
        self.play(FadeIn(ident, shift=UP * 0.1), run_time=0.9)
        self.wait(0.8)
        res = mt("U(x)", "=", r"\frac{F_0\ell}{4}", r"\Big[\Big(\frac{x}{\ell}\Big)^2-1\Big]^2", size=56,
                 colors={0: VIOLET, 2: MAGENTA}).move_to([0, -0.4, 0])
        rb = SurroundingRectangle(res, color=VIOLET, buff=0.2, corner_radius=0.1, stroke_width=3)
        self.play(FadeIn(res, shift=UP * 0.1), Create(rb), run_time=0.9)
        chk = mixed(text("confere:", 26, opacity=0.95), mt("-", "U'(x)", "=", "F(x)", size=44, colors={1: VIOLET, 3: CYAN}))
        chk.move_to([0, -2.0, 0])
        self.play(FadeIn(chk, shift=UP * 0.1), run_time=0.7)
        self.wait(0.9)
        self.s4_rest = VGroup(r1, r2, ident, chk)
        self.res, self.rb = res, rb

    # ── S5 DOIS MÍNIMOS E UMA BARREIRA ──────────────────────────────────────
    def s5(self):
        T = self.T
        self.play(FadeOut(self.s4_rest), FadeOut(self.rb), run_time=0.5)
        res_g = VGroup(self.res)
        self.titulo(("DOIS MÍNIMOS", "E UMA BARREIRA"), None)
        note_e = text("O eixo vertical representa energia.", 26, opacity=0.95).move_to([0, -4.15, 0])
        self.play(res_g.animate.scale(0.6).move_to([0, 5.4, 0]), FadeIn(self.u_axis), FadeIn(self.u_label),
                  FadeIn(self.base), FadeIn(self.p_base), FadeIn(self.p_marks), FadeIn(note_e), run_time=1.0)
        # pontos calculados: mínimos U(±ℓ) = 0 e barreira U(0) = U_b
        l_w = VGroup(tex(r"U(-\ell)=0", 30, VIOLET).move_to([gx(-1), GY0 - 0.85, 0]),
                     tex(r"U(\ell)=0", 30, VIOLET).move_to([gx(1), GY0 - 0.85, 0]))
        l_b = tex(r"U(0)=\frac{F_0\ell}{4}=U_b", 30, MAGENTA).move_to([0, gy(1) + 0.6, 0])
        self.play(FadeIn(self.well_dots, scale=0.4), FadeIn(l_w, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(self.ub_level), FadeIn(self.ub_dot, scale=0.4), FadeIn(self.ub_tick),
                  FadeIn(l_b, shift=DOWN * 0.1), run_time=0.8)
        self.wait(0.3)
        # um ponto intermediário: U(ℓ/2) = (9/16) U_b, levado do esquema ao gráfico
        calc = mt(r"U\!\left(\frac{\ell}{2}\right)", "=", "U_b", r"\left(\frac14-1\right)^2", "=", r"\frac{9}{16}U_b",
                  size=38, colors={0: VIOLET, 2: MAGENTA, 5: MAGENTA}).move_to([0, 4.4, 0])
        p = gpt(0.5)
        part = pdot(0.5, PY)
        vl = DashedLine([p[0], PY + 0.16, 0], p, color=WHITE, stroke_width=1.8, dash_length=0.08).set_opacity(0.7)
        hl = DashedLine(p, [AXL, p[1], 0], color=VIOLET, stroke_width=1.8, dash_length=0.08).set_opacity(0.7)
        pd = Dot(p, radius=0.09, color=WHITE).set_z_index(5)
        pl = tex(r"\frac{9}{16}U_b", 26, VIOLET).move_to([AXL + 0.62, p[1] + 0.3, 0])
        self.play(FadeIn(calc, shift=UP * 0.1), FadeIn(part, scale=0.5), run_time=0.8)
        self.play(Create(vl), run_time=0.6)
        self.play(FadeIn(pd, scale=0.5), Create(hl), FadeIn(pl), run_time=0.6)
        sym = mt("U(-x)", "=", "U(x)", size=42, colors={0: VIOLET, 2: VIOLET}).move_to([0, 4.4, 0])
        self.play(soft_swap(calc, sym), run_time=0.7)
        pd2 = VGroup(vl, pd).copy()
        self.add(pd2)
        self.play(Rotate(pd2, PI, axis=UP, about_point=np.array([0, 0, 0])), run_time=1.1)
        self.wait(0.3)
        # U′ = −F: inclinações (tangentes) nos pontos conhecidos
        slope = mt("U'(x)", "=", "-", "F(x)", size=42, colors={0: VIOLET, 3: CYAN}).move_to([0, 4.6, 0])
        self.play(soft_swap(sym, slope), FadeOut(VGroup(vl, hl, pd, pl, pd2, part, l_b)), run_time=0.7)

        def tangent(x0, col=VIOLET):
            k = du(x0) * GSY / GSX
            n = np.sqrt(1 + k * k)
            d = 0.52 / n
            c = gpt(x0) if abs(x0) < 1.01 else np.array([gx(x0), GY0, 0.0])
            return seg((c[0] - d, c[1] - k * d), (c[0] + d, c[1] + k * d), stroke_width=6, color=col).set_z_index(4)

        # F>0 em (0, ℓ): U decresce; F<0 em (−ℓ, 0): U cresce; F = 0 em −ℓ, 0, ℓ: tangente horizontal
        tg_pts = [(-1.0, "mínimo"), (-0.5, ""), (0.0, "barreira"), (0.5, ""), (1.0, "")]
        tangs = VGroup(*[tangent(x0) for x0, _ in tg_pts])
        txt1 = mixed(tex(r"F>0", 32, CYAN), tex(r"\Rightarrow", 32), tex(r"U'<0", 32, VIOLET),
                     text("U decresce", 24, opacity=0.95)).move_to([0, 3.85, 0])
        txt2 = mixed(tex(r"F<0", 32, CYAN), tex(r"\Rightarrow", 32), tex(r"U'>0", 32, VIOLET),
                     text("U cresce", 24, opacity=0.95)).move_to([0, 3.85, 0])
        txt3 = mixed(tex(r"F=0", 32, CYAN), tex(r"\Rightarrow", 32), tex(r"U'=0", 32, VIOLET),
                     text("tangente horizontal", 24, opacity=0.95)).move_to([0, 3.85, 0])
        self.play(FadeIn(txt1, shift=UP * 0.1), FadeIn(tangs[3]), run_time=0.8)
        self.wait(0.5)
        self.play(soft_swap(txt1, txt2), FadeIn(tangs[1]), run_time=0.8)
        self.wait(0.5)
        self.play(soft_swap(txt2, txt3), FadeIn(tangs[0]), FadeIn(tangs[2]), FadeIn(tangs[4]), run_time=0.8)
        self.wait(0.6)
        self.mark("tangentes")
        # a curva é traçada por um cursor (x, U(x)) a partir de x = 0; o outro lado vem da simetria
        tr = text("cada posição x determina um valor de U", 24, opacity=0.95).move_to([0, 3.85, 0])
        self.add(self.u_trace)
        T.UX.set_value(0)
        self.play(soft_swap(txt3, tr), T.UV.animate.set_value(1), FadeOut(l_w), run_time=0.6)
        self.play(T.UX.animate.set_value(1.0), run_time=2.0, rate_func=smooth)
        ext = mt(r"|x|\ \text{grande}:\ U\approx\frac{F_0x^4}{4\ell^3}\ \Rightarrow\ U\to+\infty", size=34, maxw=7.4)
        ext.move_to([0, 3.85, 0])
        self.play(soft_swap(tr, ext), T.UX.animate.set_value(XR), run_time=1.5, rate_func=smooth)
        right = VMobject(color=VIOLET, stroke_width=5).set_points_smoothly([gpt(v) for v in np.linspace(0, XR, 120)])
        self.add(right)
        T.UV.set_value(0)
        left = right.copy()
        self.add(left)
        self.play(Rotate(left, PI, axis=UP, about_point=np.array([0, 0, 0])), FadeOut(tangs), run_time=1.2)
        self.remove(right, left)
        self.add(self.u_curve)
        self.mark("curva U")
        self.play(FadeOut(ext), FadeOut(slope), run_time=0.5)
        # classificação, como confirmação breve
        a0 = tex(r"U''(0)=-\frac{F_0}{\ell}<0", 32, MAGENTA).move_to([0, gy(1) + 0.7, 0])
        st0 = text("instável", 26, MAGENTA).move_to([0, gy(1) + 1.35, 0])
        aw = tex(r"U''(\pm\ell)=\frac{2F_0}{\ell}>0", 32, VIOLET).move_to([0, GY0 - 0.85, 0])
        stw = VGroup(text("estável", 26, VIOLET).move_to([gx(-1), GY0 - 1.45, 0]),
                     text("estável", 26, VIOLET).move_to([gx(1), GY0 - 1.45, 0]))
        self.play(FadeIn(a0, shift=UP * 0.1), FadeIn(st0, shift=UP * 0.1), run_time=0.7)
        self.wait(0.7)
        self.play(FadeOut(VGroup(a0, st0)), FadeIn(aw, shift=UP * 0.1), FadeIn(stw, shift=UP * 0.1), run_time=0.7)
        self.wait(0.8)
        self.play(FadeOut(VGroup(aw, stw, self.well_dots, res_g, note_e)), run_time=0.6)

    # ── S6 ONDE A PARTÍCULA PODE IR? ────────────────────────────────────────
    def s6(self):
        T = self.T
        self.titulo(("ONDE A PARTÍCULA", "PODE IR?"), "Sem dissipação, a energia total é constante.")
        c1 = mt("E", "=", "K", "+", "U", size=44, colors={0: BLUE_L, 4: VIOLET}).move_to([0, 4.7, 0])
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.8)
        self.wait(0.4)
        c2 = mt("K", "=", "E", "-", "U", r"\ge 0", size=44, colors={2: BLUE_L, 4: VIOLET}).move_to([0, 3.95, 0])
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.8)
        self.wait(0.4)
        c3 = mt("U(x)", r"\le", "E", size=50, colors={0: VIOLET, 2: BLUE_L}).move_to([0, 3.25, 0])
        box = SurroundingRectangle(c3, color=BLUE_L, buff=0.18, corner_radius=0.08, stroke_width=2.5)
        self.play(FadeIn(c3, shift=UP * 0.1), Create(box), run_time=0.9)
        self.wait(0.5)
        # a linha E nasce da desigualdade: o "E" da caixa viaja até o fim da linha (valor fixo de energia)
        cp = c3[2].copy()
        T.E.set_value(E_SUB)
        self.add(self.eline, self.e_lab)
        self.play(cp.animate.scale(0.7).move_to([AXR + 0.2, gy(E_SUB) + 0.3, 0]), T.LA.animate.set_value(1),
                  FadeOut(VGroup(c1, c2)), run_time=1.8, rate_func=smooth)
        self.remove(cp)
        self.add(self.region_axis, self.projections, self.turning, self.particle, self.kbar, self.cursor, self.k_lab)
        self.mark("linha E")
        # leitura de K na mesma posição x: ponto na curva, nível E, segmento vertical e projeção no eixo espacial
        T.CS.set_value(1.15)
        self.play(FadeOut(VGroup(c3, box)), T.CV.animate.set_value(1), T.KL.animate.set_value(1), run_time=0.8)
        n0 = mixed(text("segmento: de", 24, opacity=0.95), tex("U(x)", 28, VIOLET), text("(curva) até", 24, opacity=0.95),
                   tex("E", 28, BLUE_L), text("(nível)", 24, opacity=0.95)).move_to([0, -4.3, 0])
        self.play(FadeIn(n0, shift=UP * 0.1), run_time=0.6)
        self.wait(0.9)
        n1 = mixed(tex(r"U<E", 32, BLUE_L), text("→", 26), tex(r"K>0", 32, KCOL),
                   text("posição permitida", 26, opacity=0.95)).move_to([0, -4.3, 0])
        self.play(soft_swap(n0, n1), run_time=0.6)
        self.wait(0.7)
        b = float(allowed(E_SUB)[1][1])
        self.play(T.CS.animate.set_value(b), run_time=1.8, rate_func=smooth)
        n2 = mixed(tex(r"U=E", 32, BLUE_L), text("→", 26), tex(r"K=0", 32, KCOL),
                   text("limite da região permitida", 26, opacity=0.95)).move_to([0, -4.3, 0])
        self.play(soft_swap(n1, n2), run_time=0.6)
        self.wait(0.9)
        self.play(T.CV.animate.set_value(0), run_time=0.3)
        T.CS.set_value(0.3)
        n3 = mixed(tex(r"U>E", 32, BLUE_L), text("→ posição inacessível", 26, opacity=0.95)).move_to([0, -4.3, 0])
        self.play(T.CV.animate.set_value(1), soft_swap(n2, n3), run_time=0.6)
        self.wait(1.3)
        self.play(T.CV.animate.set_value(0), FadeOut(n3), run_time=0.4)
        # conjunto permitido projetado no eixo espacial
        n4 = text("As posições com K ≥ 0 formam o conjunto permitido.", 24, opacity=0.95).move_to([0, -4.3, 0])
        self.play(T.RG.animate.set_value(1), FadeIn(n4, shift=UP * 0.1), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(n4), run_time=0.4)

    # ── S7 Regimes ──────────────────────────────────────────────────────────
    def regime_in(self, E, traj, dl, lab, cap=None):
        """Nova condição inicial: retira a partícula e o nível anteriores, muda E, mostra o novo nível e a partícula."""
        T = self.T
        self.play(T.RG.animate.set_value(0), T.LA.animate.set_value(0), T.FB.animate.set_value(0), run_time=0.4)
        T.E.set_value(E)
        T.DL.set_value(dl)
        self.traj = traj
        T.TT.set_value(0)
        ins = [T.LA.animate.set_value(1), T.RG.animate.set_value(1), FadeIn(lab, shift=UP * 0.1)]
        if cap is not None:
            ins.append(FadeIn(cap, shift=UP * 0.1))
        self.play(*ins, run_time=0.6)
        self.play(T.VP.animate.set_value(1), T.KB.animate.set_value(1), run_time=0.5)

    def go(self, t, *anims):
        """Avança o tempo da trajetória até t (linear, sem pausa); `anims` correm junto, com a mesma duração."""
        cur = self.T.TT.get_value()
        self.play(self.T.TT.animate.set_value(t), *anims, run_time=t - cur, rate_func=linear)

    def reg_title(self, linhas, mathlab):
        """Título curto do regime (uma linha) e rótulo matemático."""
        t = display(linhas, 30).move_to([0, 6.35, 0])
        return t, mathlab

    def s7(self):
        T = self.T
        slot = [0, -4.3, 0]
        APO = 4.5
        # E = 0 ---------------------------------------------------------------------------------------------
        t0 = display("NO MÍNIMO, EM REPOUSO", 30).move_to([0, 6.35, 0])
        m0 = mt("E", "=", "0", size=52, colors={0: BLUE_L}).move_to([0, 5.5, 0])
        a0 = text("Permanece em um dos mínimos.", 26, opacity=0.95).move_to([0, APO, 0])
        self.play(FadeOut(self._title), FadeOut(self._apoio), FadeIn(t0, shift=UP * 0.1), run_time=0.6)
        self.regime_in(0.0, traj_rest, 0.0, m0, a0)
        self.wait(1.6)
        # 0 < E < U_b -----------------------------------------------------------------------------------------
        t1 = display("ENERGIA ABAIXO DA BARREIRA", 30).move_to([0, 6.35, 0])
        m1 = mt("0", "<", "E", "<", "U_b", size=52, colors={2: BLUE_L, 4: MAGENTA}).move_to([0, 5.5, 0])
        a1 = text("Oscila deste lado, sem atravessar o centro.", 26, opacity=0.95).move_to([0, APO, 0])
        self.play(FadeOut(VGroup(t0, m0, a0)), T.VP.animate.set_value(0), T.KB.animate.set_value(0), FadeIn(t1), run_time=0.5)
        self.regime_in(E_SUB, traj_sub, 1.0, m1, a1)
        self.mark("sub-barreira")
        tm1, tp1, tm2, tp2 = SUB_MIN[0], SUB_TP[0], SUB_MIN[1], SUB_TP[1]
        nA = text("retorno: K = 0", 26, opacity=0.95).move_to(slot)
        nB = text("no mínimo, K é máximo: maior rapidez", 24, opacity=0.95).move_to(slot)
        nC = text("retorno: K = 0, e a partícula volta", 24, opacity=0.95).move_to(slot)
        nD = text("retorno: K = 0", 26, opacity=0.95).move_to(slot)
        self.timed(nA, 0.0, 1.0)
        self.timed(nB, tm1 - 0.1, tm1 + 1.0)
        self.timed(nC, tp1 - 0.2, tp1 + 0.9)
        self.timed(nD, tp2 - 0.2, tp2 + 0.9)
        forb = text("inacessível: U > E", 22, MAGENTA).move_to([0, PY + 0.5, 0])
        self.add(forb)
        T.FB.set_value(1)
        self.go(tp2 + 1.0)
        self.clear_timed()
        self.go(tp2 + 1.4, FadeOut(forb), T.VP.animate.set_value(0), T.KB.animate.set_value(0))
        # E = U_b -----------------------------------------------------------------------------------------------
        t2 = display("ENERGIA NO LIMIAR", 30).move_to([0, 6.35, 0])
        m2 = mt("E", "=", "U_b", size=52, colors={0: BLUE_L, 2: MAGENTA}).move_to([0, 5.5, 0])
        a2 = text("Aproxima-se do centro cada vez mais devagar.", 26, opacity=0.95).move_to([0, APO, 0])
        a2b = mt(r"x\to0\ \ \text{quando}\ \ t\to\infty", size=36).move_to([0, APO, 0])
        self.play(FadeOut(VGroup(t1, m1, a1)), FadeIn(t2), T.FB.animate.set_value(0), run_time=0.5)
        self.regime_in(E_SEP, traj_sep, 1.0, m2)
        self.mark("separatriz")
        ex = text("repouso exato em x = 0 é outro caso", 22, opacity=0.95).move_to(slot)
        self.timed(a2, 0.0, 3.5)
        self.timed(a2b, 3.7, 99.0)
        self.timed(ex, 3.9, 99.0)
        self.go(5.2)
        self.clear_timed()
        self.add(a2b, ex)
        self.go(5.6, FadeOut(a2b), FadeOut(ex), T.VP.animate.set_value(0), T.KB.animate.set_value(0))
        # E > U_b -----------------------------------------------------------------------------------------------
        t3 = display("ENERGIA ACIMA DA BARREIRA", 30).move_to([0, 6.35, 0])
        m3 = mt("E", ">", "U_b", size=52, colors={0: BLUE_L, 2: MAGENTA}).move_to([0, 5.5, 0])
        a3 = text("Atravessa, mas permanece limitada.", 26, opacity=0.95).move_to([0, APO, 0])
        self.play(FadeOut(VGroup(t2, m2)), FadeIn(t3), run_time=0.5)
        self.regime_in(E_SUP, traj_sup, 0.0, m3)
        self.mark("travessia")
        tc1, tp_a = SUP_CEN[0], SUP_TP[0]
        n_a = text("retorno externo: K = 0", 26, opacity=0.95).move_to(slot)
        n_b = text("K > 0 no centro: atravessa", 26, opacity=0.95).move_to(slot)
        n_c = text("retorno externo: K = 0, o sentido muda", 24, opacity=0.95).move_to(slot)
        self.timed(n_a, 0.0, 1.0)
        self.timed(n_b, tc1 - 0.5, tc1 + 0.9)
        self.timed(n_c, tp_a - 0.3, tp_a + 1.0)
        self.timed(a3, tp_a + 1.0, tp_a + 4.2)
        self.go(tp_a + 4.2)
        self.clear_timed()
        self.s7_cleanup = VGroup(t3, m3)
        self.mark("retorno externo")

    # ── S8 Resumo e perfil ──────────────────────────────────────────────────
    def s8(self):
        T = self.T
        self.play(FadeOut(self.s7_cleanup), T.VP.animate.set_value(0), T.KB.animate.set_value(0), run_time=0.5)
        resumo = lines("FORÇA → POTENCIAL →", "POSIÇÕES PERMITIDAS", size=32).move_to([0, 6.3, 0])
        self.play(FadeIn(resumo, shift=UP * 0.1), run_time=0.7)
        slot = [0, 4.7, 0]
        # os três comportamentos, cada frase com o movimento correspondente
        specs = [
            (E_SUB, traj_sub, 1.0, mt("0", "<", "E", "<", "U_b", size=40, colors={2: BLUE_L, 4: MAGENTA}),
             "oscila de um lado", 5.7),
            (E_SEP, traj_sep, 1.0, mt("E", "=", "U_b", size=40, colors={0: BLUE_L, 2: MAGENTA}),
             "aproxima-se do centro", 3.8),
            (E_SUP, traj_sup, 0.0, mt("E", ">", "U_b", size=40, colors={0: BLUE_L, 2: MAGENTA}),
             "atravessa e retorna nos extremos", 6.0),
        ]
        cur = None
        for E, tr, dl, lab, frase, dur in specs:
            ph = mixed(lab, text(frase, 26)).move_to(slot)
            if ph.width > 7.8:
                ph.scale_to_fit_width(7.8)
            self.play(T.VP.animate.set_value(0), T.KB.animate.set_value(0), T.RG.animate.set_value(0),
                      T.LA.animate.set_value(0), *( [FadeOut(cur)] if cur is not None else [] ), run_time=0.4)
            T.E.set_value(E)
            T.DL.set_value(dl)
            self.traj = tr
            T.TT.set_value(0)
            self.play(T.LA.animate.set_value(1), T.RG.animate.set_value(1), FadeIn(ph, shift=UP * 0.1),
                      T.VP.animate.set_value(1), T.KB.animate.set_value(1), run_time=0.5)
            self.go(dur)
            cur = ph
        self.go(T.TT.get_value() + 0.3, FadeOut(cur), T.VP.animate.set_value(0), T.KB.animate.set_value(0))
        # cartão final: série e perfil
        keep = VGroup(resumo)
        self.play(T.RG.animate.set_value(0), T.LA.animate.set_value(0), T.KL.animate.set_value(0), FadeOut(keep),
                  FadeOut(self.u_curve), FadeOut(self.u_axis), FadeOut(self.u_label), FadeOut(self.base),
                  FadeOut(self.ub_level), FadeOut(self.ub_dot), FadeOut(self.ub_tick), FadeOut(self.p_base),
                  FadeOut(self.p_marks), FadeOut(self.series), FadeOut(self.wm), run_time=0.8)
        h1 = display("DA EQUAÇÃO AO FENÔMENO · EP. 04", 26).set_color(WHITE).move_to([0, 1.2, 0])
        h2 = display("@labparallax", 56).set_color_by_gradient(CYAN, BLUE_L).move_to([0, 0.0, 0])
        self.play(FadeIn(h1, shift=UP * 0.1), FadeIn(h2, shift=UP * 0.1), run_time=0.8)
        self.wait(2.2)
