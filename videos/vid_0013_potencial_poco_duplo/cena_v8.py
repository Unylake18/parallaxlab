"""Potencial de poço duplo a partir da força F(x) = F0 [x/ℓ − (x/ℓ)³]: preview silencioso (V8).

DA EQUAÇÃO AO FENÔMENO · EP. 04.
Gancho (referência de narração): "Essa partícula fica presa de um lado ou consegue atravessar para o outro?"
"Dá para descobrir sem resolver x(t)." Encerramento: "Um gráfico de potencial permite classificar o movimento sem
resolver x(t)."

Percurso: força dada -> potencial construído -> gráfico justificado -> movimento previsto pela energia.

  S1  pergunta (presa ou atravessa?) no esquema 1D; F(x) dado (F0: escala de força; ℓ: escala de comprimento); zeros por fatoração (x/ℓ em evidência);
      x = ℓ/2 copiado para os dois lugares de x -> F(ℓ/2) = 3F0/8 -> seta e ponto do gráfico; F(−x) = −F(x);
      curva traçada por um cursor (x, F(x)); leitura dos sinais na curva com posições de teste estáticas.
      Partícula: ponto branco com halo; posição escolhida: anel no eixo; ponto do gráfico: anel colorido
  S2  DA FORÇA AO POTENCIAL: F = −U′ -> U′ = −F -> U = −∫F dx -> F0 sai -> integral em cada termo -> primitivas
      (uma de cada vez) -> frações -> distribuição de −F0 (os dois sinais negativos viram +)
  S3  ONDE COLOCAMOS O ZERO DE ENERGIA?: d/dx(U + C) = U′ (a força não fixa C) -> escolha U(±ℓ) = 0 -> x = ℓ -> potências de ℓ canceladas -> −F0ℓ/4 + C -> somamos F0ℓ/4 aos dois lados -> C = F0ℓ/4
  S4  C substituído -> reordenação -> F0ℓ/4 em evidência -> quadrado perfeito; conferência −U′ = F
  S5  DOIS MÍNIMOS E UMA BARREIRA: pontos calculados U(±ℓ) = 0 e U(0) = U_b, cursor (x, U(x)) com tangente (U′ = −F),
      crescimento x⁴, simetria U(−x) = U(x); confirmação por U″ (máximo instável / mínimos estáveis)
  S6  ONDE A PARTÍCULA PODE IR?: E = K + U -> K = E − U ; K = ½mv² ≥ 0 -> E − U ≥ 0 -> U ≤ E; linha E nasce do E;
      leitura de K; a energia total vem da condição inicial
  S7  regimes (cada E é uma nova condição inicial), destaques ligados ao tempo físico da trajetória; separatriz longa
  S8  último quadro: os três níveis identificados sobre U(x), "A ENERGIA DECIDE A TRAVESSIA", @labparallax

Equações: classe `Eq` (MathTex de string única por linha + índices de glifos por parte) e TransformByGlyphMap
(MF-Tools): termos mantidos ficam como âncoras ("=" em posição fixa), termos ativos se transformam; glifos
dispensados saem antes de os novos entrarem; destaques temporários em azul-claro acompanham o termo ativo.
Escalas: MAIN (contas), REF (referências), LAB (rótulos de gráfico); expressões longas quebram em linhas alinhadas.

Gráfico de energia adimensional: x em unidades de ℓ, U em unidades de U_b = F0ℓ/4: u(x) = (x² − 1)².
O esquema (eixo x) fica sempre abaixo dos gráficos e com a mesma escala horizontal.
Dinâmica: ẍ = −κ u′(x) (m = 1), κ = 0,2, RK4 nos regimes limitados; a separatriz usa a solução exata √2 sech(a t),
a = 2√κ·s com s = 0,4 (fator de exibição; ~9,5 s sem chegar a x = 0); nenhuma x(t) aparece no vídeo.

`ATE=k` (1–8) renderiza só até o segmento k.
"""

import os
import sys
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from manim import (
    DOWN, LEFT, PI, RIGHT, UP, AnimationGroup, Arrow, Circle, Create, CurvedArrow, DashedLine, DecimalNumber, Dot, FadeIn, FadeOut,
    ImageMobject, Indicate, LaggedStart, Line, MathTex, MoveAlongPath, ReplacementTransform, Rotate, Scene, SurroundingRectangle, TransformFromCopy,
    VGroup, VMobject, ValueTracker, always_redraw, config, linear, smooth, there_and_back,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text
from MF_Tools import TransformByGlyphMap

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
S_SEP = 0.4               # fator de exibição da separatriz (reparametrização da apresentação)
SEP_T = 9.5               # duração do movimento exibido na separatriz
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
    # leitura dos sinais na curva (posições de teste do S1): volta para ±ℓ dos dois lados, afasta de 0
    assert f_force(0.5) > 0 and f_force(1.4) < 0 and f_force(-0.5) < 0 and f_force(-1.4) > 0
    assert f_force(0.25) > 0 and f_force(-0.25) < 0
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
    assert traj_sep(SEP_T) > 0.09                                # ainda longe de x = 0 no fim da exibição


_qa()

# ── Geometria da tela (frame 9 × 16) ────────────────────────────────────────
# Todos os gráficos usam x em unidades de ℓ com a mesma escala horizontal do esquema (eixo x) que fica abaixo deles.
GSX, GX0 = 1.9, 0.0       # tela por ℓ
GY0, GSY = -0.35, 1.6     # gráfico de energia: U = 0 e tela por U_b
AXL, AXR = -3.4, 3.4      # eixo vertical e extensão horizontal
XR = 1.6                  # domínio do gráfico de U: |x| ≤ 1,6 ℓ
PY = -2.7                 # esquema (eixo espacial da partícula) abaixo dos gráficos
AY = 0.3                  # altura do esquema na abertura (desce até PY quando o gráfico de F nasce)
FY0, FSY, FXR = 0.95, 1.25, 1.45      # gráfico de F: eixo x, tela por F0 e domínio
FAX = -3.45               # eixo vertical F
TITLE_Y, APOIO_Y = 6.35, 5.4
WAIT_K = 0.4             # escala das pausas de leitura
RT_K = 1.0                # escala das transformações de equações (mm/born): sem aceleração global
SZ2, EQ2, Y2, HY2 = 50, -1.55, 1.9, -0.9    # integração: tamanho, "=" fixo, linha principal, linha de apoio
EQD = EQ2 - 0.8                             # "=" da distribuição de −F0 (linha única mais larga)
SZ3, EQ3, YA, YB = 48, -1.6, 2.15, 0.25       # escolha de C: tamanho, "=" fixo, linhas A e B


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


def gmark(p, color=CYAN, r=0.1):
    """Marcador de ponto do GRÁFICO (anel colorido com centro escuro): distinto da partícula física (pdot)."""
    return VGroup(Circle(radius=r, color=color, stroke_width=3.5).set_fill(BACKGROUND_COLOR, 1).move_to(p),
                  Dot(p, radius=0.035, color=color)).set_z_index(5)


def pmark(x, y=PY, color=KCOL):
    """Posição escolhida no eixo x (anel), distinta da partícula."""
    return Circle(radius=0.11, color=color, stroke_width=3.5).move_to([gx(x), y, 0]).set_z_index(5)


def farrow(x, direc, y, length=0.75):
    """Seta de força ligada à partícula em x: do raio da partícula até `length` na direção `direc`."""
    return Arrow([gx(x) + 0.2 * direc, y, 0], [gx(x) + (0.2 + length) * direc, y, 0], buff=0, color=CYAN,
                 stroke_width=6, max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=10).set_z_index(4)


# ── Equações com índices de glifos (MF-Tools), no idioma do vid_0012 ────────
MAIN, REF, LAB = 44, 34, 28      # escala principal das contas, fórmulas de referência e rótulos de gráfico
EQX = -1.9                       # posição horizontal do "=" nas contas (âncora fixa da região da álgebra)


class Eq:
    """MathTex de string única por linha + índices de glifos por parte, para TransformByGlyphMap.

    `br`: índice da parte que começa a segunda linha; `under`: parte da 1ª linha sob cuja borda
    esquerda a 2ª linha começa (linhas alinhadas, sem reduzir a fonte)."""

    default_size = MAIN

    def __init__(self, *parts, size=None, colors=None, br=None, under=None):
        size = size or Eq.default_size
        rows = [list(parts)] if br is None else [list(parts[:br]), list(parts[br:])]
        spans, lns = [0], []
        for r in rows:
            multi = MathTex(*r, font_size=size)
            single = MathTex(" ".join(r), font_size=size, color=WHITE)
            assert len(single[0]) == sum(len(q) for q in multi), r
            for q in multi:
                spans.append(spans[-1] + len(q))
            lns.append(single)
        self.s = np.array(spans, dtype=int)
        if br is not None:
            l0, l1 = lns
            l1.next_to(l0, DOWN, buff=0.32)
            ref = VGroup(*[l0[0][k] for k in range(int(self.s[under]), int(self.s[under + 1]))])
            l1.shift(RIGHT * (ref.get_left()[0] - l1.get_left()[0]))
        self.mob = VGroup(VGroup(*[g for ln in lns for g in ln[0]]))
        for i, c in (colors or {}).items():
            self.g(i).set_color(c)

    def p(self, *ids):
        return [k for i in ids for k in range(int(self.s[i]), int(self.s[i + 1]))]

    def g(self, *ids):
        return VGroup(*[self.mob[0][k] for k in self.p(*ids)])

    def gl(self, idx):
        return VGroup(*[self.mob[0][k] for k in idx])

    def at(self, part, x, y):
        c = self.g(part).get_center()
        self.mob.shift([x - c[0], y - c[1], 0])
        return self

    def center_at(self, y, x=0.0):
        self.mob.move_to([x, y, 0])
        return self

    def geo(self, i):
        """Índices da parte i em ordem geométrica: colunas da esquerda para a direita, de cima para baixo."""
        ks = sorted(self.p(i), key=lambda k: self.mob[0][k].get_center()[0])
        cols = []
        for k in ks:
            cx = self.mob[0][k].get_center()[0]
            if cols and abs(cx - cols[-1][0]) < 0.07:
                cols[-1][1].append(k)
            else:
                cols.append([cx, [k]])
        out = []
        for _, c in cols:
            out += sorted(c, key=lambda k: -self.mob[0][k].get_center()[1])
        return out

    def frac(self, i):
        """Numerador (esquerda → direita), barra e denominador de uma fração, por geometria."""
        idx = self.p(i)
        c = {k: self.mob[0][k].get_center() for k in idx}
        bar = max(idx, key=lambda k: self.mob[0][k].width)
        num = sorted((k for k in idx if k != bar and c[k][1] > c[bar][1]), key=lambda k: c[k][0])
        den = sorted((k for k in idx if k != bar and c[k][1] < c[bar][1]), key=lambda k: c[k][0])
        return num, [bar], den


def copy_from(src):
    """Introdutor: o destino nasce de uma CÓPIA dos glifos `src`, que ficam onde estão."""
    class _Copy(TransformFromCopy):
        def __init__(self, mob, **kw):
            super().__init__(VGroup(*src), mob, **kw)
    return _Copy


def M(A, pa, B, pb, **kw):
    """Partes de A viram partes de B (os mesmos termos, deslocados ou transformados)."""
    return (A.p(*pa), B.p(*pb), kw)


def MG(ia, ib, **kw):
    """Glifos de A viram glifos de B (índices explícitos)."""
    return (list(ia), list(ib), kw)


def X(ia, **kw):
    """Glifos dispensados saem cedo, antes de os novos entrarem."""
    kw.setdefault("run_time", 0.45)
    return (list(ia), [], kw)


def N(ib, **kw):
    """Glifos novos entram depois que os termos mantidos se acomodam."""
    kw.setdefault("delay", 0.65)
    kw.setdefault("run_time", 0.45)
    return ([], list(ib), kw)


def CG(src, ib, **kw):
    """Glifos de B nascem de cópias de glifos já na tela."""
    return (copy_from(list(src)), list(ib), kw)


def strike(mob, color=None):
    """Traço de cancelamento sobre um glifo (ou grupo)."""
    return Line(mob.get_corner(DOWN + LEFT) + np.array([-0.04, -0.03, 0]),
                mob.get_corner(UP + RIGHT) + np.array([0.04, 0.03, 0]),
                color=color or BLUE_L, stroke_width=3.5).set_z_index(6)


class PotencialPocoDuplo013(Scene):

    def wait(self, duration=1.0, *a, **k):
        """Pausas de leitura do preview: WAIT_K × o valor escrito (recupera tempo sem acelerar as transformações)."""
        return super().wait(duration * WAIT_K, *a, **k)

    def hold(self, duration):
        """Pausa de leitura REAL (sem WAIT_K): espaço para a futura narração depois de uma ideia-chave."""
        return Scene.wait(self, duration)

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

    def apoio_swap(self, apoio, run_time=0.4, extra=()):
        new_a = text(apoio, 26, opacity=0.95).move_to([0, APOIO_Y, 0])
        if getattr(self, "_apoio", None) is not None:
            self.play(soft_swap(self._apoio, new_a), *extra, run_time=run_time)
        else:
            self.play(FadeIn(new_a, shift=UP * 0.1), *extra, run_time=run_time)
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
            FM=ValueTracker(0),          # metade esquerda de F por correspondência (x, F) ↔ (−x, −F)
            FMV=ValueTracker(0),
            UM=ValueTracker(0),          # metade esquerda de U por correspondência (x, U) ↔ (−x, U)
            UMV=ValueTracker(0),
            LL=ValueTracker(1),          # rótulo E da linha (separado da linha)
            TS=ValueTracker(0),          # tempo do resumo (S8)
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
            g.add(gmark(p, CYAN).set_opacity(fv))
            return g

        self.f_trace = always_redraw(f_trace)

        def f_mirror():
            fv = T.FMV.get_value()
            if fv <= 0.001:
                return VGroup()
            x = T.FM.get_value()
            g = VGroup()
            if x > 0.02:
                xs = np.linspace(0, x, max(4, int(70 * x / FXR)))
                g.add(VMobject(color=CYAN, stroke_width=5).set_points_smoothly([fpt(-v) for v in xs])
                      .set_stroke(opacity=fv))
                g.add(DashedLine(fpt(x), fpt(-x), color=WHITE, stroke_width=1.5, dash_length=0.07).set_opacity(0.4 * fv))
            g.add(gmark(fpt(x), CYAN, 0.085).set_opacity(fv), gmark(fpt(-x), CYAN, 0.085).set_opacity(fv))
            return g

        self.f_mirror = always_redraw(f_mirror)

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
            k = du(x) * GSY / GSX                       # tangente no cursor: inclinação U′ = −F
            d = 0.55 / np.sqrt(1 + k * k)
            g.add(seg((p[0] - d, p[1] - k * d), (p[0] + d, p[1] + k * d), stroke_width=4, color=KCOL)
                  .set_opacity(0.9 * uv).set_z_index(4))
            g.add(gmark(p, VIOLET).set_opacity(uv))
            return g

        self.u_trace = always_redraw(u_trace)

        def u_mirror():
            uv = T.UMV.get_value()
            if uv <= 0.001:
                return VGroup()
            x = T.UM.get_value()
            g = VGroup()
            if x > 0.02:
                xs = np.linspace(0, x, max(4, int(90 * x / XR)))
                g.add(VMobject(color=VIOLET, stroke_width=5).set_points_smoothly([gpt(-v) for v in xs])
                      .set_stroke(opacity=uv))
                g.add(DashedLine(gpt(x), gpt(-x), color=WHITE, stroke_width=1.5, dash_length=0.07).set_opacity(0.4 * uv))
            g.add(gmark(gpt(x), VIOLET, 0.085).set_opacity(uv), gmark(gpt(-x), VIOLET, 0.085).set_opacity(uv))
            return g

        self.u_mirror = always_redraw(u_mirror)

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
                               .set_opacity(T.LA.get_value() * T.LL.get_value()))

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

    # ── Transformações de equações ──────────────────────────────────────────
    def mm(self, A, B, *moves, rt=1.3, extra=()):
        """A (Eq) -> B (Eq) por TransformByGlyphMap; o que não for citado entra/sai por fade."""
        self.play(TransformByGlyphMap(A.mob, B.mob, *moves, auto_fade=True), *extra, run_time=rt * RT_K)
        self.remove(A.mob)
        self.add(B.mob)
        return B

    def born(self, B, *moves, rt=1.2, extra=()):
        """B nasce de cópias de glifos já na tela (CG); o que não for citado entra por fade."""
        dummy = MathTex("x", font_size=20).set_opacity(0).move_to(B.mob)
        self.play(TransformByGlyphMap(dummy, B.mob, *moves, auto_fade=True), *extra, run_time=rt * RT_K)
        self.remove(dummy)
        self.add(B.mob)
        return B

    def recolor(self, pairs, rt=0.4):
        """Restaura/aplica cores: pairs = [(VGroup, cor), ...]."""
        self.play(*[m.animate.set_color(c) for m, c in pairs], run_time=rt)

    def timed_on(self, mob, tracker, t0, t1, fade=0.3):
        """Texto cuja opacidade segue um tracker (aparece em t0, some em t1)."""
        mob.set_opacity(0)
        mob.add_updater(lambda m: m.set_opacity(win(tracker.get_value(), t0, t1, fade)))
        self.add(mob)
        self._timed.append(mob)

    # ── S1 Esquema, força dada, zeros, um valor calculado, curva e leitura dos sinais ──
    def s1(self):
        T = self.T
        self.add(self.f_trace)
        sh = AY - PY
        self.p_base.shift(UP * sh)
        self.p_marks.shift(UP * sh)
        # A. pergunta física: a partícula fica presa deste lado ou atravessa para o outro? (sem resolver x(t))
        self.titulo(("FICA PRESA DE UM LADO", "OU ATRAVESSA?"))
        part = pdot(0.5, AY)
        xt = seg((gx(0.5), AY - 0.1), (gx(0.5), AY - 0.26), stroke_width=3, color=KCOL)
        xl = tex("x", 32, KCOL).move_to([gx(0.5), AY - 0.5, 0])
        arr0 = farrow(0.5, 1, AY, 0.6)
        lab0 = text("força", 24, CYAN).next_to(arr0, UP, buff=0.12)
        self.play(FadeIn(self.p_base), FadeIn(part, scale=0.5), run_time=0.8)
        self.play(part.animate.shift(LEFT * 0.5), run_time=0.9, rate_func=there_and_back)
        jump = CurvedArrow([gx(0.42), AY + 0.3, 0], [gx(-0.5), AY + 0.3, 0], angle=PI * 0.55, color=WHITE,
                           stroke_width=3, tip_length=0.2)
        jump.set_stroke(opacity=0.75)
        jump.tip.set_fill(WHITE, opacity=0.75)
        qm = display("?", 48).move_to([gx(-0.04), AY + 1.2, 0])
        self.play(Create(jump), FadeIn(qm, shift=UP * 0.1), run_time=0.9)
        self.apoio_swap("Dá para descobrir sem resolver x(t).")
        self.hold(1.1)
        self.play(FadeIn(VGroup(xt, xl), shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(arr0, shift=RIGHT * 0.2), FadeIn(lab0), run_time=0.6)
        nota = text("A seta indica a força, não a velocidade.", 24, opacity=0.9).move_to([0, AY - 1.3, 0])
        self.play(FadeIn(nota, shift=UP * 0.1), run_time=0.5)
        self.hold(0.9)
        # B. a força é um dado do problema
        self.titulo(("A FORÇA DEPENDE", "DA POSIÇÃO"), "A força é um dado do problema.")
        FA = Eq("F(x)", "=", "F_0", r"\Big[", r"\frac{x}{\ell}", "-", r"\Big(\frac{x}{\ell}\Big)^3", r"\Big]",
                colors={0: CYAN}).center_at(4.45)
        self.FA = FA
        nf = VGroup(mixed(tex(r"F_0>0", 30), text("escala de força", 22, opacity=0.9), buff=0.14),
                    mixed(tex(r"\ell>0", 30), text("escala de comprimento", 22, opacity=0.9), buff=0.14)
                    ).arrange(RIGHT, buff=0.45).move_to([0, 3.55, 0])
        self.play(FadeOut(VGroup(arr0, lab0, nota, jump, qm)), FadeIn(FA.mob, shift=UP * 0.1), run_time=0.9)
        self.play(FadeIn(nf, shift=UP * 0.1), run_time=0.6)
        self.wait(1.2)
        # C. zeros: F = 0 e x/ℓ em evidência
        self.apoio_swap("Onde a força se anula?")
        FAP = ("F(x)", "=", "F_0", r"\Big[", r"\frac{x}{\ell}", "-", r"\Big(\frac{x}{\ell}\Big)^3", r"\Big]")
        zx = FA.g(1).get_center()[0]
        Zc = Eq(*FAP, colors={0: CYAN}).at(1, zx, 2.65)
        self.play(FadeOut(nf), run_time=0.4)
        self.play(TransformFromCopy(FA.mob, Zc.mob), run_time=0.8)
        Z0 = Eq("0", "=", *FAP[2:]).at(1, zx, 2.65)
        self.mm(Zc, Z0, M(Zc, [0], Z0, [0]), M(Zc, [1, 2, 3, 4, 5, 6, 7], Z0, [1, 2, 3, 4, 5, 6, 7]), rt=0.9)
        self.apoio_swap("Colocamos x/ℓ em evidência.")
        self.recolor([(Z0.g(4), BLUE_L), (Z0.gl(Z0.geo(6)[1:4]), BLUE_L)], rt=0.5)
        Z1 = Eq("0", "=", "F_0", r"\frac{x}{\ell}", r"\Big[", "1", "-", r"\Big(\frac{x}{\ell}\Big)^2", r"\Big]",
                colors={3: BLUE_L}).at(1, zx, 2.65)
        a6, b7 = Z0.geo(6), Z1.geo(7)
        self.mm(Z0, Z1, M(Z0, [0, 1, 2], Z1, [0, 1, 2]), M(Z0, [4], Z1, [3], path_arc=PI * 0.8), M(Z0, [3], Z1, [4]),
                N(Z1.p(5)), M(Z0, [5], Z1, [6]), MG(a6[:5], b7[:5]), MG(a6[5:], b7[5:]), M(Z0, [7], Z1, [8]), rt=1.6)
        self.wait(0.5)
        # cada fator anula em seus pontos: x/ℓ = 0 → x = 0 ; 1 − (x/ℓ)² = 0 → x = ±ℓ
        self.apoio_swap("Como F₀ ≠ 0, um dos fatores se anula.")
        R0 = tex("x=0", 36, BLUE_L).next_to(Z1.g(3), DOWN, buff=0.32)
        R1 = tex(r"x=\pm\ell", 36, KCOL).next_to(Z1.g(4, 5, 6, 7, 8), DOWN, buff=0.32)
        zeros = VGroup(*(Dot([gx(z), AY, 0], radius=0.09, color=c).set_z_index(3)
                         for z, c in ((-1, KCOL), (0, BLUE_L), (1, KCOL))))
        self.play(Indicate(Z1.g(3), color=BLUE_L), FadeIn(R0, shift=DOWN * 0.1), run_time=0.8)
        self.play(Z1.g(4, 5, 6, 7, 8).animate.set_color(KCOL), FadeIn(R1, shift=DOWN * 0.1), run_time=0.8)
        R = VGroup(R0, R1)
        self.play(FadeIn(self.p_marks), FadeIn(zeros[1], scale=0.4), FadeIn(VGroup(zeros[0], zeros[2]), scale=0.4),
                  Indicate(R, scale_factor=1.06), run_time=1.0)
        self.mark("zeros")
        self.wait(0.6)
        # D. um valor calculado: x = ℓ/2 copiado para os dois lugares de x
        self.apoio_swap("Escolhemos uma posição e calculamos a força.")
        xv = Eq("x", "=", r"\ell/2", size=30, colors={0: KCOL, 2: BLUE_L}).center_at(AY - 0.85, gx(0.5) + 0.3)
        posm = pmark(0.5, AY)
        self.play(FadeOut(VGroup(Z1.mob, R)), ReplacementTransform(xl, xv.g(0)), FadeIn(xv.g(1, 2)),
                  FadeOut(part), FadeIn(posm, scale=0.6), run_time=0.8)
        self.add(xv.mob)
        P1 = Eq("F", r"(\ell/2)", "=", "F_0", r"\Big[", r"\frac{\ell/2}{\ell}", "-", r"\Big(",
                r"\frac{\ell/2}{\ell}", r"\Big)^3", r"\Big]", colors={0: CYAN, 1: CYAN}).center_at(2.2)
        eqx_p = P1.g(2).get_center()[0]
        f5, f8 = P1.frac(5), P1.frac(8)
        for idx in (f5[0], f8[0], P1.geo(1)[1:4]):
            P1.gl(idx).set_color(BLUE_L)
        Pc = Eq(*FAP, colors={0: CYAN}).at(1, zx, 2.2)
        self.play(TransformFromCopy(FA.mob, Pc.mob), run_time=0.8)
        fa0, fx, fx3 = Pc.geo(0), Pc.frac(4), Pc.geo(6)      # F ( x ) ; x/ℓ ; ( x bar ℓ ) 3
        g1 = P1.geo(1)                                       # ( ℓ / 2 )
        lv = xv.p(2)
        self.mm(Pc, P1, MG(fa0[:1], P1.p(0)), MG([fa0[1], fa0[3]], [g1[0], g1[4]]), X(fa0[2:3], run_time=1.0),
                CG(xv.gl(lv), g1[1:4]), M(Pc, [1, 2, 3], P1, [2, 3, 4]),
                MG(fx[1] + fx[2], f5[1] + f5[2]), X(fx[0], run_time=1.0), CG(xv.gl(lv), f5[0]),
                M(Pc, [5], P1, [6]), MG(fx3[:1], P1.p(7)), MG(fx3[2:4], f8[1] + f8[2]), X(fx3[1:2], run_time=1.0),
                CG(xv.gl(lv), f8[0]), MG(fx3[4:], P1.p(9)), M(Pc, [7], P1, [10]), rt=1.8)
        # razões e cubo numa só transformação: (ℓ/2)/ℓ = 1/2 e ((ℓ/2)/ℓ)³ = 1/8
        P3 = Eq("F", r"(\ell/2)", "=", "F_0", r"\Big(", r"\frac{1}{2}", "-", r"\frac{1}{8}", r"\Big)",
                colors={0: CYAN, 1: CYAN, 5: BLUE_L, 7: BLUE_L}).at(2, eqx_p, 2.2)
        P1.gl(P1.geo(1)[1:4]).set_color(CYAN)
        n5, b5_, d5 = P1.frac(5)          # n5 = ℓ / 2
        m5, c5_, e5_ = P3.frac(5)         # m5 = 1, e5_ = 2
        self.mm(P1, P3, M(P1, [0, 1, 2, 3, 4, 6], P3, [0, 1, 2, 3, 4, 6]), MG([n5[0], d5[0]], m5),
                MG([n5[1]] + b5_, c5_), MG([n5[2]], e5_), M(P1, [7, 8, 9], P3, [7]), M(P1, [10], P3, [8]), rt=1.6)
        self.wait(0.4)
        # resultado: F0(4/8 − 1/8) = 3F0/8 > 0
        P4 = Eq("F", r"(\ell/2)", "=", r"\frac{3F_0}{8}", ">", "0", colors={0: CYAN, 1: CYAN, 3: CYAN}
                ).at(2, eqx_p, 2.2)
        r3 = P4.frac(3)
        self.mm(P3, P4, M(P3, [0, 1, 2], P4, [0, 1, 2]), MG(P3.p(3), r3[0][1:]),
                MG(P3.p(5, 6, 7), r3[0][:1] + r3[1] + r3[2]), X(P3.p(4, 8)), N(P4.p(4, 5)), rt=1.4)
        # E. o mesmo resultado dá o sentido da força (seta) e, adiante, a altura do ponto no gráfico
        a1 = farrow(0.5, 1, AY, 0.6)
        l1 = text("Força para a direita", 22, CYAN).next_to(a1, UP, buff=0.14)
        self.play(FadeIn(a1, shift=RIGHT * 0.2), FadeIn(l1), Indicate(P4.g(4, 5), color=CYAN), run_time=0.8)
        self.mark("F(l/2)")
        self.wait(1.0)
        # o esquema desce; os eixos x e F aparecem; o valor calculado vira um ponto do gráfico
        self.apoio_swap("Posição escolhida → força nessa posição.")
        vaxis = Arrow([FAX, FY0 - 2.2, 0], [FAX, FY0 + 2.25, 0], buff=0, stroke_width=2.5, tip_length=0.16,
                      color=WHITE).set_opacity(0.6)
        vlab = tex("F", 34, CYAN).move_to([FAX + 0.32, FY0 + 2.3, 0])
        haxis = Line([AXL, FY0, 0], [AXR, FY0, 0], stroke_width=2, color=WHITE).set_opacity(0.5)
        hx = tex("x", 30).move_to([AXR - 0.05, FY0 - 0.32, 0])
        stay = VGroup(self.p_base, self.p_marks, zeros, posm, xt, xv.mob)
        self.play(P4.mob.animate.move_to([0, 3.45, 0]), stay.animate.shift(DOWN * sh), FadeOut(VGroup(a1, l1)),
                  FadeIn(vaxis), FadeIn(vlab), FadeIn(haxis), FadeIn(hx), run_time=1.1)
        pt = fpt(0.5)
        vline = DashedLine([pt[0], PY + 0.16, 0], pt, color=WHITE, stroke_width=1.8, dash_length=0.08).set_opacity(0.7)
        hline = DashedLine(pt, [FAX, pt[1], 0], color=CYAN, stroke_width=1.8, dash_length=0.08).set_opacity(0.7)
        pdt = gmark(pt, CYAN)
        plab = MathTex(r"\frac{3F_0}{8}", font_size=LAB, color=CYAN).move_to([FAX + 0.42, pt[1] + 0.32, 0])
        # o ponto reúne a posição escolhida (abscissa) e a força calculada nela (ordenada)
        coord = VGroup(tex(r"\Big(", LAB + 12), tex(r"\frac{\ell}{2}", LAB + 10, KCOL), tex(",", LAB + 10),
                       tex(r"\frac{3F_0}{8}", LAB + 10, CYAN), tex(r"\Big)", LAB + 12)).arrange(RIGHT, buff=0.1)
        coord.move_to(pt + np.array([1.45, 0.5, 0]))
        self.play(Create(vline), run_time=0.6)
        self.play(FadeIn(pdt, scale=0.5), Create(hline), TransformFromCopy(P4.g(3), plab),
                  FadeIn(coord, shift=UP * 0.1), run_time=0.9)
        self.hold(1.0)
        # F é ímpar: F(−x) = −F(x) (mostrada junto com o traçado espelhado da curva)
        odd = Eq("F(-x)", "=", "-", "F(x)", colors={0: CYAN, 3: CYAN}).center_at(3.45)
        # F. a curva: cursor x -> F(x) avaliada -> ponto que deixa o traço (lado direito)
        self.play(FadeOut(VGroup(vline, hline, pdt, plab, coord, P4.mob, posm, xt, xv.mob)),
                  run_time=0.5)
        xr = DecimalNumber(0, num_decimal_places=2, font_size=30)
        fr = DecimalNumber(0, num_decimal_places=2, font_size=30, color=CYAN)
        ro = VGroup(tex(r"x/\ell=", 30), xr, tex(r"F/F_0=", 30, CYAN), fr).arrange(RIGHT, buff=0.14)
        ro[2].shift(RIGHT * 0.35)
        fr.shift(RIGHT * 0.35)
        ro.move_to([0, -3.75, 0])
        xr.add_updater(lambda m: m.set_value(T.FX.get_value()))
        fr.add_updater(lambda m: m.set_value(f_force(T.FX.get_value())))
        T.FX.set_value(0)
        self.play(T.FV.animate.set_value(1), FadeIn(ro), run_time=0.4)
        self.play(T.FX.animate.set_value(FXR), run_time=2.5, rate_func=linear)
        right = VMobject(color=CYAN, stroke_width=5).set_points_smoothly([fpt(v) for v in np.linspace(0, FXR, 90)])
        self.add(right)
        T.FV.set_value(0)
        xr.clear_updaters()
        fr.clear_updaters()
        # a outra metade nasce da correspondência (x, F(x)) ↔ (−x, −F(x))
        self.add(self.f_mirror)
        T.FM.set_value(0)
        self.play(T.FMV.animate.set_value(1), FadeOut(ro), FadeIn(odd.mob, shift=UP * 0.1), run_time=0.4)
        self.play(T.FM.animate.set_value(FXR), run_time=1.0, rate_func=linear)
        left = VMobject(color=CYAN, stroke_width=5).set_points_smoothly([fpt(-v) for v in np.linspace(0, FXR, 90)])
        self.add(left)
        self.play(T.FMV.animate.set_value(0), run_time=0.3)
        self.remove(self.f_mirror)
        self.add(left)
        self.mark("curva F")

        # G. leitura dos sinais: uma posição de teste por vez (marcador no eixo, seta horizontal, ponto no gráfico)
        def probe(x0, length=0.38):
            sg = 1 if f_force(x0) > 0 else -1
            a = Arrow([gx(x0) + 0.17 * sg, PY, 0], [gx(x0) + (0.17 + length) * sg, PY, 0], buff=0, color=CYAN,
                      stroke_width=6, max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)
            return VGroup(
                DashedLine([gx(x0), PY + 0.14, 0], fpt(x0), color=WHITE, stroke_width=1.5, dash_length=0.08)
                .set_opacity(0.45),
                gmark(fpt(x0), CYAN, 0.085),
                Circle(radius=0.12, color=KCOL, stroke_width=3.5).move_to([gx(x0), PY, 0]).set_z_index(5),
                a.set_z_index(4),
                text("força", 22, CYAN).next_to(a, UP, buff=0.1))

        def show_probe(*xs, hold=1.0):
            pr = VGroup(*(probe(x0) for x0 in xs))
            self.play(FadeIn(pr), run_time=0.5)
            self.wait(hold)
            self.play(FadeOut(pr), run_time=0.35)

        self.apoio_swap("Perto de +ℓ, a força aponta de volta.")
        show_probe(0.5, 1.4, hold=1.6)
        self.apoio_swap("Perto de 0, a força aponta para longe.")
        show_probe(0.25, -0.25, hold=1.4)
        self.mark("sinais")
        self.apoio_swap("Qual potencial corresponde a essa força?")
        self.wait(1.0)
        self.s1_all = VGroup(vaxis, vlab, haxis, hx, right, left, odd.mob, self.p_base, self.p_marks, zeros)
        self.zeros_f = zeros

    # ── S2 DA FORÇA AO POTENCIAL ────────────────────────────────────────────
    def s2(self):
        FA = self.FA
        Y = Y2
        Eq.default_size = SZ2
        self.play(FadeOut(self.s1_all), FA.mob.animate.scale(0.8).move_to([0, 4.45, 0]), run_time=0.9)
        self.titulo("DA FORÇA AO POTENCIAL", "Integramos com o sinal trocado.")
        # F = −U′  ->  U′ = −F  ->  U = −∫F dx
        I0 = Eq("F(x)", "=", "-", "U'(x)", colors={0: CYAN, 3: VIOLET}).at(1, EQ2 + 0.6, Y)
        self.born(I0, CG(FA.g(0), I0.p(0)), rt=0.9)
        self.wait(0.4)
        I0b = Eq("U'(x)", "=", "-", "F(x)", colors={0: VIOLET, 3: CYAN}).at(1, EQ2 + 0.6, Y)
        self.mm(I0, I0b, M(I0, [0], I0b, [3], path_arc=PI * 0.45), M(I0, [3], I0b, [0], path_arc=PI * 0.45),
                M(I0, [1, 2], I0b, [1, 2]), rt=1.2)
        self.apoio_swap("Integrar desfaz a derivada.")
        I1 = Eq("U(x)", "=", "-", r"\int", "F(x)", r"\,dx", colors={0: VIOLET, 4: CYAN}).at(1, EQ2, Y)
        u0, u1 = I0b.geo(0), I1.geo(0)             # U ′ ( x )  ->  U ( x )
        self.mm(I0b, I1, MG(u0[:1], u1[:1]), MG(u0[2:], u1[1:]), X(u0[1:2]), M(I0b, [1, 2], I1, [1, 2]),
                M(I0b, [3], I1, [4]), N(I1.p(3, 5)), rt=1.3)
        self.wait(0.6)
        # F(x) é substituída pela expressão dada; depois F0, constante, sai da integral
        self.apoio_swap("Substituímos a força dada.")
        I2a = Eq("U(x)", "=", "-", r"\int", "F_0", r"\Big(", r"\frac{x}{\ell}", "-", r"\frac{x^3}{\ell^3}", r"\Big)",
                 r"\,dx", colors={0: VIOLET, 4: CYAN, 5: CYAN, 6: CYAN, 7: CYAN, 8: CYAN, 9: CYAN}).at(1, EQ2, Y)
        self.mm(I1, I2a, M(I1, [0, 1, 2, 3], I2a, [0, 1, 2, 3]), X(I1.p(4)), M(I1, [5], I2a, [10]),
                CG(FA.g(2), I2a.p(4)), CG(FA.g(3), I2a.p(5)), CG(FA.g(4), I2a.p(6)), CG(FA.g(5), I2a.p(7)),
                CG(FA.g(6), I2a.p(8)), CG(FA.g(7), I2a.p(9)), rt=1.5)
        self.apoio_swap("F₀ é constante: sai da integral.")
        I2b = Eq("U(x)", "=", "-", "F_0", r"\int", r"\Big(", r"\frac{x}{\ell}", "-", r"\frac{x^3}{\ell^3}", r"\Big)",
                 r"\,dx", colors={0: VIOLET, 3: CYAN, 5: CYAN, 6: CYAN, 7: CYAN, 8: CYAN, 9: CYAN}).at(1, EQ2, Y)
        # F0 passa por cima da integral (arco), a integral desliza para a direita
        self.mm(I2a, I2b, M(I2a, [0, 1, 2], I2b, [0, 1, 2]), M(I2a, [4], I2b, [3], path_arc=PI * 0.9),
                M(I2a, [3], I2b, [4]), M(I2a, [5, 6, 7, 8, 9, 10], I2b, [5, 6, 7, 8, 9, 10]), rt=1.1)
        self.wait(0.4)
        # a integral é aplicada a cada termo; 1/ℓ e 1/ℓ³ saem das integrais (duas linhas alinhadas)
        self.apoio_swap("Integramos cada termo.")
        I3a = Eq("U(x)", "=", "-", "F_0", r"\Big[", r"\int", r"\frac{x}{\ell}", r"\,dx",
                 "-", r"\int", r"\frac{x^3}{\ell^3}", r"\,dx", r"\Big]", "+C",
                 colors={0: VIOLET, 3: CYAN}, br=8, under=5).at(1, EQ2, Y)
        self.mm(I2b, I3a, M(I2b, [0, 1, 2, 3], I3a, [0, 1, 2, 3]), M(I2b, [5], I3a, [4]), M(I2b, [4], I3a, [5]),
                M(I2b, [4], I3a, [9], delay=0.45), M(I2b, [6], I3a, [6]), M(I2b, [7], I3a, [8], delay=0.45),
                M(I2b, [8], I3a, [10], delay=0.45), M(I2b, [9], I3a, [12], delay=0.45), M(I2b, [10], I3a, [7]),
                M(I2b, [10], I3a, [11], delay=0.45), N(I3a.p(13), delay=1.0), rt=1.8)
        self.wait(0.4)
        self.apoio_swap("Os fatores constantes ficam fora.", extra=(I3a.g(6, 10).animate.set_color(BLUE_L),))
        I3 = Eq("U(x)", "=", "-", "F_0", r"\Big[", r"\frac{1}{\ell}", r"\int", "x", r"\,dx",
                "-", r"\frac{1}{\ell^3}", r"\int", "x^3", r"\,dx", r"\Big]", "+C",
                colors={0: VIOLET, 3: CYAN, 5: BLUE_L, 10: BLUE_L}, br=9, under=5).at(1, EQ2, Y)
        fa_, fb_ = I3a.frac(6), I3a.frac(10)
        g5, g10 = I3.frac(5), I3.frac(10)
        self.mm(I3a, I3, M(I3a, [0, 1, 2, 3, 4], I3, [0, 1, 2, 3, 4]), M(I3a, [5], I3, [6]),
                MG(fa_[0], I3.p(7)), MG(fa_[1], g5[1], path_arc=PI * 0.9), MG(fa_[2], g5[2], path_arc=PI * 0.9),
                N(g5[0]), M(I3a, [7], I3, [8]), M(I3a, [8], I3, [9]), M(I3a, [9], I3, [11]),
                MG(fb_[0], I3.geo(12)), MG(fb_[1], g10[1], path_arc=PI * 0.9), MG(fb_[2], g10[2], path_arc=PI * 0.9),
                N(g10[0]), M(I3a, [11, 12, 13], I3, [13, 14, 15]), rt=1.5)
        self.mark("integral separada")
        # primitivas, uma de cada vez
        hp = mixed(text("uma primitiva de", 24, opacity=0.95), tex("x", 34, BLUE_L), text(":", 24),
                   tex(r"\frac{x^2}{2}", 36, BLUE_L)).move_to([0, HY2, 0])
        self.apoio_swap("Calculamos uma primitiva de cada termo.", run_time=0.5,
                        extra=(I3.g(5, 10).animate.set_color(WHITE), I3.g(7).animate.set_color(BLUE_L),
                               FadeIn(hp, shift=UP * 0.1)))
        I4 = Eq("U(x)", "=", "-", "F_0", r"\Big[", r"\frac{1}{\ell}", r"\frac{x^2}{2}",
                "-", r"\frac{1}{\ell^3}", r"\int", "x^3", r"\,dx", r"\Big]", "+C",
                colors={0: VIOLET, 3: CYAN, 6: BLUE_L}, br=7, under=5).at(1, EQ2, Y)
        n6 = I4.frac(6)
        self.mm(I3, I4, M(I3, [0, 1, 2, 3, 4, 5], I4, [0, 1, 2, 3, 4, 5]), X(I3.p(6, 8)),
                MG(I3.p(7), n6[0][:1]), N(n6[0][1:] + n6[1] + n6[2]),
                M(I3, [9, 10, 11, 12, 13, 14, 15], I4, [7, 8, 9, 10, 11, 12, 13]), rt=1.3)
        self.wait(0.3)
        hp2 = mixed(text("uma primitiva de", 24, opacity=0.95), tex("x^3", 34, BLUE_L), text(":", 24),
                    tex(r"\frac{x^4}{4}", 36, BLUE_L)).move_to([0, HY2, 0])
        self.play(soft_swap(hp, hp2), I4.g(6).animate.set_color(WHITE), I4.g(10).animate.set_color(BLUE_L),
                  run_time=0.6)
        I5 = Eq("U(x)", "=", "-", "F_0", r"\Big[", r"\frac{1}{\ell}", r"\frac{x^2}{2}",
                "-", r"\frac{1}{\ell^3}", r"\frac{x^4}{4}", r"\Big]", "+C",
                colors={0: VIOLET, 3: CYAN, 9: BLUE_L}, br=7, under=5).at(1, EQ2, Y)
        n9 = I5.frac(9)
        x3 = I4.geo(10)                              # x, 3
        self.mm(I4, I5, M(I4, [0, 1, 2, 3, 4, 5, 6, 7, 8], I5, [0, 1, 2, 3, 4, 5, 6, 7, 8]), X(I4.p(9, 11)),
                MG(x3, n9[0]), N(n9[1] + n9[2]), M(I4, [12, 13], I5, [10, 11]), rt=1.3)
        self.wait(0.3)
        # cada produto vira uma fração; o termo de baixo volta para a linha principal
        self.apoio_swap("Cada produto vira uma só fração.", extra=(FadeOut(hp2), I5.g(9).animate.set_color(WHITE)))
        I5b = Eq("U(x)", "=", "-", "F_0", r"\Big[", r"\frac{x^2}{2\ell}", "-", r"\frac{x^4}{4\ell^3}", r"\Big]", "+C",
                 colors={0: VIOLET, 3: CYAN}).at(1, EQD, Y)
        A5, A6, A8, A9 = I5.frac(5), I5.frac(6), I5.frac(8), I5.frac(9)
        B5, B7 = I5b.frac(5), I5b.frac(7)
        self.mm(I5, I5b, M(I5, [0, 1, 2, 3, 4], I5b, [0, 1, 2, 3, 4]),
                MG(A6[0], B5[0]), MG(A6[2], B5[2][:1]), MG(A5[2], B5[2][1:]), MG(A5[1] + A6[1], B5[1]), X(A5[0]),
                M(I5, [7], I5b, [6]), MG(A9[0], B7[0]), MG(A9[2], B7[2][:1]), MG(A8[2], B7[2][1:]),
                MG(A8[1] + A9[1], B7[1]), X(A8[0]), M(I5, [10, 11], I5b, [8, 9]), rt=1.6)
        I6 = I5b
        self.mark("integrado")
        # distribuição de −F0, numa linha só: −F0[a − b] = −F0·a − F0·(−b); o "−" e o F0 vão a cada termo
        self.apoio_swap("Distribuímos o fator negativo.", extra=(I6.g(2, 3).animate.set_color(BLUE_L),))
        I6a = Eq("U(x)", "=", "-", r"\frac{F_0x^2}{2\ell}", "-", "F_0", r"\Big(", "-", r"\frac{x^4}{4\ell^3}", r"\Big)",
                 "+C", colors={0: VIOLET, 2: BLUE_L, 4: BLUE_L, 5: BLUE_L}).at(1, EQD, Y)
        C5 = I6.frac(5)
        A3, A8 = I6a.frac(3), I6a.frac(8)
        I6a.gl(A3[0][:2]).set_color(BLUE_L)
        # a cópia de −F0 sobe para a faixa livre, atravessa por cima enquanto os termos se acomodam e só então
        # desce no lugar já livre (o destino fica invisível até a cópia chegar)
        cpF = I6.g(2, 3).copy()
        lift = UP * 1.0
        dest = I6a.g(4, 5).get_center()
        I6a.g(4, 5).set_opacity(0)
        self.play(cpF.animate.shift(lift), run_time=0.35)
        self.mm(I6, I6a, M(I6, [0, 1, 2], I6a, [0, 1, 2]), MG(I6.p(3), A3[0][:2]), MG(C5[0], A3[0][2:]),
                MG(C5[1], A3[1]), MG(C5[2], A3[2]), M(I6, [6], I6a, [7]), M(I6, [7], I6a, [8]), X(I6.p(4, 8)),
                N(I6a.p(6, 9), delay=0.8), M(I6, [9], I6a, [10]), rt=1.7,
                extra=(cpF.animate.move_to(dest + lift),))
        self.play(cpF.animate.move_to(dest), run_time=0.45)
        I6a.g(4, 5).set_opacity(1)
        self.remove(cpF)
        # (−)·(−) = +: os dois sinais negativos do termo em x⁴ se fundem em um "+"
        hd2 = mixed(tex(r"(-)\cdot(-)=+", 38, MAGENTA), text("o termo em x⁴ fica positivo.", 26, opacity=0.95),
                    buff=0.2).move_to([0, HY2, 0])
        self.play(FadeIn(hd2, shift=UP * 0.1), I6a.g(4, 7).animate.set_color(MAGENTA), I6a.g(5).animate.set_color(WHITE),
                  I6a.g(2).animate.set_color(WHITE), I6a.gl(A3[0][:2]).animate.set_color(WHITE), run_time=0.6)
        self.play(Indicate(I6a.g(4), color=MAGENTA, scale_factor=1.5), Indicate(I6a.g(7), color=MAGENTA, scale_factor=1.5),
                  run_time=0.7)
        I7 = Eq("U(x)", "=", "-", r"\frac{F_0x^2}{2\ell}", "+", r"\frac{F_0x^4}{4\ell^3}", "+C",
                colors={0: VIOLET, 4: MAGENTA}).at(1, EQD, Y)
        D5 = I7.frac(5)
        self.mm(I6a, I7, M(I6a, [0, 1, 2, 3], I7, [0, 1, 2, 3]), MG(I6a.p(4, 7), I7.p(4)),
                MG(I6a.p(5), D5[0][:2]), MG(A8[0], D5[0][2:]), MG(A8[1], D5[1]), MG(A8[2], D5[2]),
                X(I6a.p(6, 9)), M(I6a, [10], I7, [6]), rt=1.6)
        bx4 = SurroundingRectangle(I7.g(4, 5), color=MAGENTA, buff=0.1, corner_radius=0.08, stroke_width=2.5)
        self.play(Create(bx4), run_time=0.5)
        self.hold(1.0)
        self.play(FadeOut(VGroup(hd2, bx4)), I7.g(4).animate.set_color(WHITE), run_time=0.5)
        Eq.default_size = MAIN
        self.Ueq = I7

    # ── S3 ONDE COLOCAMOS O ZERO DE ENERGIA? ────────────────────────────────
    def s3(self):
        Ue = self.Ueq
        self.titulo(("ONDE COLOCAMOS O", "ZERO DE ENERGIA?"), "Somar uma constante não muda a inclinação.")
        cg0 = Ue.geo(6)[1:]                             # C
        self.play(FadeOut(self.FA.mob), Ue.mob.animate.scale(0.7).move_to([0, 4.45, 0]), run_time=0.8)
        # a força só fixa diferenças de U: a derivada de U + C é U′, qualquer que seja C
        dC = mixed(mt(r"\frac{d}{dx}", r"\big(U+C\big)", "=", "U'", size=REF + 2, colors={3: VIOLET}),
                   text("→ mesma força", 24, CYAN), buff=0.25)
        dC[0][1][3].set_color(MAGENTA)
        dC.move_to([0, 3.45, 0])
        self.play(FadeIn(dC, shift=UP * 0.1), Ue.gl(cg0).animate.set_color(MAGENTA), run_time=0.7)
        self.hold(1.2)
        # escolha explícita da referência (C ainda não está determinado: será fixado por essa escolha)
        c1 = Eq("U(", r"\pm\ell", ")", "=", "0", size=REF + 4, colors={0: VIOLET, 2: VIOLET}).center_at(3.45)
        tag = text("escolha", 22, KCOL).next_to(c1.mob, RIGHT, buff=0.35)
        self.apoio_swap("Escolhemos a referência U(±ℓ) = 0.", run_time=0.6,
                        extra=(FadeOut(dC, shift=UP * 0.1), FadeIn(c1.mob, shift=UP * 0.1), FadeIn(tag, shift=LEFT * 0.1),
                               Ue.gl(cg0).animate.set_color(WHITE)))
        self.hold(0.6)
        self.apoio_swap("Pela simetria, basta usar x = ℓ.")
        Eq.default_size = SZ3
        # A. cópia completa da expressão, transportada como um bloco para a linha A
        Lx = Eq("U(x)", "=", "-", r"\frac{F_0x^2}{2\ell}", "+", r"\frac{F_0x^4}{4\ell^3}", "+C",
                colors={0: VIOLET}).at(1, EQ3, YA)
        self.play(TransformFromCopy(Ue.mob, Lx.mob), run_time=0.8)
        self.add(Lx.mob)
        # B. só os x viram ℓ
        La = Eq(r"U(\ell)", "=", "-", r"\frac{F_0\ell^2}{2\ell}", "+", r"\frac{F_0\ell^4}{4\ell^3}", "+C",
                colors={0: VIOLET}).at(1, EQ3, YA)
        xs = [Lx.geo(0)[2], Lx.frac(3)[0][2], Lx.frac(5)[0][2]]
        La.gl(xs).set_color(BLUE_L)
        keep = [k for k in range(len(Lx.mob[0])) if k not in xs]
        self.mm(Lx, La, MG(keep, keep), X(xs, run_time=0.5), N(xs, delay=0.5, run_time=0.5), rt=1.2)
        self.wait(0.4)
        # C. potências de ℓ: ℓ²/ℓ = ℓ e ℓ⁴/ℓ³ = ℓ
        self.apoio_swap("Simplificamos as potências de ℓ.")
        self.play(La.gl(xs).animate.set_color(WHITE), run_time=0.3)
        # a simplificação acontece na própria linha A
        LaC = La
        b3, b5 = LaC.frac(3), LaC.frac(5)
        cuts = VGroup(strike(LaC.gl(b3[0][3:])), strike(LaC.gl(b3[2][1:])),
                      strike(LaC.gl(b5[0][3:])), strike(LaC.gl(b5[2][1:])))
        self.play(Create(cuts), run_time=0.6)
        Lb = Eq("0", "=", "-", r"\frac{F_0\ell}{2}", "+", r"\frac{F_0\ell}{4}", "+C").at(1, EQ3, YA)
        c3, c5 = Lb.frac(3), Lb.frac(5)
        self.mm(LaC, Lb, X(LaC.p(0)), N(Lb.p(0), delay=0.35), M(LaC, [1, 2], Lb, [1, 2]),
                MG(b3[0][:3], c3[0]), X(b3[0][3:]), MG(b3[1], c3[1]), MG(b3[2][:1], c3[2]), X(b3[2][1:]),
                M(LaC, [4], Lb, [4]), MG(b5[0][:3], c5[0]), X(b5[0][3:]), MG(b5[1], c5[1]), MG(b5[2][:1], c5[2]),
                X(b5[2][1:]), M(LaC, [6], Lb, [6]), extra=(FadeOut(cuts), Indicate(c1.g(4), color=VIOLET)), rt=1.3)
        self.wait(0.4)
        # D. combinação dos termos (na mesma linha)
        self.apoio_swap("Juntamos os dois termos.")
        hc = MathTex(r"-\frac12+\frac14=-\frac14", font_size=REF + 4, color=BLUE_L).move_to([0, HY2, 0])
        self.play(Indicate(Lb.g(2, 3, 4, 5), color=BLUE_L, scale_factor=1.06), FadeIn(hc, shift=UP * 0.1),
                  run_time=0.6)
        LbC = Lb
        Lc = Eq("0", "=", "-", r"\frac{F_0\ell}{4}", "+C").at(1, EQ3, YA)
        d3, e3 = LbC.frac(3), Lc.frac(3)
        self.mm(LbC, Lc, M(LbC, [0, 1, 2], Lc, [0, 1, 2]), MG(d3[0] + d3[1], e3[0] + e3[1]), X(d3[2]),
                N(e3[2], delay=0.3), X(LbC.p(4, 5)), M(LbC, [6], Lc, [4], delay=0.4), rt=1.3)
        self.wait(0.4)
        self.play(FadeOut(hc), run_time=0.3)
        # E. isolamento de C: somamos F0ℓ/4 aos dois lados. À direita, −F0ℓ/4 + F0ℓ/4 = 0; à esquerda, 0 + F0ℓ/4.
        cg = Lc.geo(4)                                  # +, C
        addL = tex(r"+\frac{F_0\ell}{4}", SZ3 - 6, MAGENTA).next_to(Lc.g(0), DOWN, buff=0.35)
        addR = tex(r"+\frac{F_0\ell}{4}", SZ3 - 6, MAGENTA).next_to(Lc.g(2, 3), DOWN, buff=0.35)
        self.apoio_swap("Somamos F₀ℓ/4 aos dois lados.", run_time=0.6,
                        extra=(Lc.gl(cg[1:]).animate.set_color(MAGENTA), FadeIn(addL, shift=DOWN * 0.15),
                               FadeIn(addR, shift=DOWN * 0.15)))
        canc = VGroup(strike(Lc.g(2, 3), MAGENTA), strike(addR, MAGENTA))
        self.play(Create(canc), run_time=0.5)
        Ld = Eq("C", "=", r"\frac{F_0\ell}{4}", colors={0: MAGENTA, 2: MAGENTA}).at(1, EQ3, YB)
        # primeiro o lado esquerdo (0 + F0ℓ/4) desce para o destino; depois C e "=" descem pela região já livre
        self.play(FadeOut(VGroup(addR, canc)), ReplacementTransform(addL[0][1:], Ld.g(2), path_arc=-0.6),
                  FadeOut(addL[0][0]), run_time=0.7)
        # C desce pela faixa livre entre as duas linhas (longe dos denominadores) até a esquerda do "="
        cpC = Lc.gl(cg[1:]).copy()
        p0, p1 = cpC.get_center(), Ld.g(0).get_center()
        lane = VMobject().set_points_smoothly([p0, [p0[0] - 0.3, 1.2, 0], [-1.0, 1.15, 0], [p1[0] + 0.1, 0.95, 0], p1])
        self.play(MoveAlongPath(cpC, lane), FadeIn(Ld.g(1)), run_time=0.9)
        self.remove(cpC)
        self.add(Ld.mob)
        bx = SurroundingRectangle(Ld.mob, color=MAGENTA, buff=0.18, corner_radius=0.1, stroke_width=3)
        note = text("C vem da referência escolhida, não da força.", 26, opacity=0.95).move_to([0, HY2, 0])
        self.play(Create(bx), FadeIn(note, shift=UP * 0.1), run_time=0.6)
        self.mark("C")
        self.hold(2.0)
        Eq.default_size = MAIN
        self.s3_rest = VGroup(c1.mob, tag, Lc.mob, note)
        self.Ld, self.bx = Ld, bx

    # ── S4 Substituição de C e fatoração ────────────────────────────────────
    def s4(self):
        Ue0, Ld, bx = self.Ueq, self.Ld, self.bx
        self.titulo(("DO POTENCIAL À", "FORMA FINAL"), "Substituímos C pelo valor encontrado.")
        Y1 = 3.45
        Ue = Eq("U(x)", "=", "-", r"\frac{F_0x^2}{2\ell}", "+", r"\frac{F_0x^4}{4\ell^3}", "+C",
                colors={0: VIOLET}).at(1, EQX, Y1)
        Ue.gl(Ue.geo(6)[1:]).set_color(MAGENTA)          # C fica magenta durante o próprio deslocamento
        self.play(FadeOut(self.s3_rest), VGroup(Ld.mob, bx).animate.move_to([0, 1.9, 0]),
                  ReplacementTransform(Ue0.mob, Ue.mob), run_time=0.9)
        G1 = Eq("U(x)", "=", "-", r"\frac{F_0x^2}{2\ell}", "+", r"\frac{F_0x^4}{4\ell^3}", "+", r"\frac{F_0\ell}{4}",
                colors={0: VIOLET, 7: MAGENTA}).at(1, EQX, Y1)
        cg = Ue.geo(6)
        self.mm(Ue, G1, M(Ue, [0, 1, 2, 3, 4, 5], G1, [0, 1, 2, 3, 4, 5]), MG(cg[:1], G1.p(6)), X(cg[1:]),
                CG(Ld.g(2), G1.p(7)), extra=(FadeOut(VGroup(Ld.mob, bx), rate_func=lambda t: max(0, 2 * t - 1)),),
                rt=1.4)
        self.wait(0.3)
        # reorganizar: termo em x⁴ primeiro (trocam de lugar por arcos opostos)
        self.apoio_swap("Ordenamos pelas potências de x.")
        G2 = Eq("U(x)", "=", r"\frac{F_0x^4}{4\ell^3}", "-", r"\frac{F_0x^2}{2\ell}", "+", r"\frac{F_0\ell}{4}",
                colors={0: VIOLET, 6: MAGENTA}).at(1, EQX, Y1)
        self.mm(G1, G2, M(G1, [0, 1], G2, [0, 1]), M(G1, [5], G2, [2], path_arc=PI * 0.6),
                M(G1, [3], G2, [4], path_arc=PI * 0.6), M(G1, [2], G2, [3]), X(G1.p(4)),
                M(G1, [6, 7], G2, [5, 6]), rt=1.4)
        self.wait(0.3)
        # fator comum F0ℓ/4: cada termo, dividido por ele, desce para dentro dos colchetes
        self.apoio_swap("Pomos F₀ℓ/4 em evidência.")
        G3 = Eq("U(x)", "=", r"\frac{F_0\ell}{4}", r"\Big[", r"\Big(\frac{x}{\ell}\Big)^4", "-",
                r"2\Big(\frac{x}{\ell}\Big)^2", "+", "1", r"\Big]", colors={0: VIOLET, 2: MAGENTA}).at(1, EQX, 2.0)
        self.play(TransformFromCopy(G2.g(0, 1), G3.g(0, 1)), TransformFromCopy(G2.g(6), G3.g(2)),
                  FadeIn(G3.g(3, 9)), run_time=0.9)
        for src, dst in ((2, (4,)), (3, (5,)), (4, (6,)), (5, (7,)), (6, (8,))):
            self.play(Indicate(G2.g(src), color=BLUE_L, scale_factor=1.12),
                      TransformFromCopy(G2.g(src), G3.g(*dst)), run_time=0.4)
        self.add(G3.mob)
        self.mark("fatorado")
        self.wait(0.4)
        # quadrado perfeito: a² − 2a + 1 = (a − 1)², a = (x/ℓ)²
        self.apoio_swap("Reconhecemos um quadrado perfeito.")
        labs = VGroup(tex(r"a^2", 30, BLUE_L).next_to(G3.g(4), DOWN, buff=0.3),
                      tex(r"2a", 30, BLUE_L).next_to(G3.g(6), DOWN, buff=0.3),
                      tex(r"1", 30, BLUE_L).next_to(G3.g(8), DOWN, buff=0.3))
        ident = mixed(tex(r"a=\Big(\frac{x}{\ell}\Big)^2", REF, BLUE_L), tex(r"a^2-2a+1=(a-1)^2", REF, BLUE_L),
                      buff=0.5).move_to([0, 0.15, 0])
        self.play(FadeIn(labs, shift=UP * 0.1), G3.g(4, 6, 8).animate.set_color(BLUE_L), FadeIn(ident, shift=UP * 0.1),
                  run_time=0.7)
        self.hold(0.6)
        G4 = Eq("U(x)", "=", r"\frac{F_0\ell}{4}", r"\Big[", r"\Big(\frac{x}{\ell}\Big)^2", "-", "1", r"\Big]^2",
                colors={0: VIOLET, 2: MAGENTA, 4: BLUE_L, 6: BLUE_L}).at(1, EQX, 2.0)
        q4, r4 = G3.geo(4), G4.geo(4)
        sq = G4.geo(7)
        self.mm(G3, G4, M(G3, [0, 1, 2, 3], G4, [0, 1, 2, 3]), MG(q4[:5], r4[:5]), MG(q4[5:], r4[5:]),
                M(G3, [5], G4, [5]), X(G3.p(6, 7)), M(G3, [8], G4, [6]), MG(G3.p(9), sq[:1]), N(sq[1:]),
                extra=(FadeOut(labs),), rt=1.4)
        rb = SurroundingRectangle(G4.mob, color=VIOLET, buff=0.2, corner_radius=0.1, stroke_width=3)
        chk = mixed(text("confere:", 26, opacity=0.95), mt("-", "U'(x)", "=", "F(x)", size=REF + 4,
                                                           colors={1: VIOLET, 3: CYAN}))
        chk.move_to([0, 0.15, 0])
        self.play(Create(rb), soft_swap(ident, chk), G4.g(4, 6).animate.set_color(WHITE), run_time=0.8)
        self.hold(1.6)
        self.s4_rest = VGroup(G2.mob, chk)
        self.res = VGroup(G4.mob, rb)

    # ── S5 DOIS MÍNIMOS E UMA BARREIRA ──────────────────────────────────────
    def s5(self):
        T = self.T
        res = self.res
        self.titulo(("DOIS MÍNIMOS", "E UMA BARREIRA"), "Esta forma revela os dois mínimos do potencial.")
        note_e = text("O eixo vertical representa energia.", 26, opacity=0.95).move_to([0, -4.15, 0])
        self.play(FadeOut(self.s4_rest), FadeOut(res[1]), run_time=0.5)
        self.play(res[0].animate.scale(0.6).move_to([0, 4.6, 0]), run_time=0.7)
        self.play(FadeIn(self.u_axis), FadeIn(self.u_label), FadeIn(self.base), FadeIn(self.p_base),
                  FadeIn(self.p_marks), FadeIn(note_e), run_time=0.9)
        # pontos calculados: mínimos U(±ℓ) = 0 e barreira U(0) = U_b
        l_w = VGroup(tex(r"U(-\ell)=0", LAB + 2, VIOLET).move_to([gx(-1), GY0 - 0.85, 0]),
                     tex(r"U(\ell)=0", LAB + 2, VIOLET).move_to([gx(1), GY0 - 0.85, 0]))
        l_b = tex(r"U(0)=\frac{F_0\ell}{4}=U_b", LAB + 2, MAGENTA).move_to([0, gy(1) + 0.6, 0])
        self.play(FadeIn(self.well_dots, scale=0.4), FadeIn(l_w, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(self.ub_level), FadeIn(self.ub_dot, scale=0.4), FadeIn(self.ub_tick),
                  FadeIn(l_b, shift=DOWN * 0.1), run_time=0.8)
        # a curva é traçada por um cursor (x, U(x)); a tangente acompanha o cursor: U′ = −F
        slope = mt("U'(x)", "=", "-", "F(x)", size=REF + 2, colors={0: VIOLET, 3: CYAN}).move_to([0, 3.8, 0])
        self.play(FadeIn(slope, shift=UP * 0.1), FadeOut(l_b), run_time=0.6)
        self.add(self.u_trace)
        T.UX.set_value(0)
        y_t = 3.15

        def txt(f, up, w):
            return mixed(tex(f, 30, CYAN), tex(r"\Rightarrow", 30), tex(up, 30, VIOLET), text(w, 22, opacity=0.95),
                         buff=0.14).move_to([0, y_t, 0])

        items = [(txt(r"F=0", r"U'=0", "topo da barreira"), -1.0, 0.07),
                 (txt(r"F>0", r"U'<0", "U decresce"), 0.07, 0.93),
                 (txt(r"F=0", r"U'=0", "mínimo"), 0.93, 1.07),
                 (txt(r"F<0", r"U'>0", "U cresce"), 1.07, 1.38),
                 (mt(r"|x|\ \text{grande}:\ U\approx\frac{F_0x^4}{4\ell^3}\to+\infty", size=30).move_to([0, y_t, 0]),
                  1.38, 9.0)]
        for m, a, b in items:
            self.timed_on(m, T.UX, a, b, fade=0.03)
        self.play(T.UV.animate.set_value(1), run_time=0.4)
        self.wait(0.7)
        self.play(T.UX.animate.set_value(0.5), run_time=1.2, rate_func=linear)
        self.play(T.UX.animate.set_value(1.0), run_time=1.1, rate_func=linear)
        self.wait(0.7)
        self.play(T.UX.animate.set_value(1.38), run_time=0.9, rate_func=linear)
        self.play(T.UX.animate.set_value(XR), run_time=0.6, rate_func=linear)
        self.wait(0.8)
        self.mark("metade direita")
        right = VMobject(color=VIOLET, stroke_width=5).set_points_smoothly([gpt(v) for v in np.linspace(0, XR, 120)])
        self.add(right)
        T.UV.set_value(0)
        self.clear_timed()
        # simetria U(−x) = U(x): a metade esquerda nasce da correspondência (x, U) ↔ (−x, U), sem rotação
        sym = mt("U(-x)", "=", "U(x)", size=REF + 2, colors={0: VIOLET, 2: VIOLET}).move_to([0, 3.8, 0])
        self.play(soft_swap(slope, sym), run_time=0.6)
        self.add(self.u_mirror)
        T.UM.set_value(0)
        self.play(T.UMV.animate.set_value(1), run_time=0.3)
        self.play(T.UM.animate.set_value(XR), run_time=0.9, rate_func=linear)
        self.remove(right)
        self.add(self.u_curve)
        self.play(T.UMV.animate.set_value(0), FadeOut(l_w), run_time=0.4)
        self.remove(self.u_mirror)
        self.mark("curva U")
        # confirmação curta pelo Cálculo: sinal de U″ junto de cada equilíbrio
        a0 = tex(r"U''(0)=-\frac{F_0}{\ell}<0", 32, MAGENTA).move_to([0, gy(1) + 0.7, 0])
        st0 = text("máximo: equilíbrio instável", 24, MAGENTA).move_to([0, gy(1) + 1.3, 0])
        aw = tex(r"U''(\pm\ell)=\frac{2F_0}{\ell}>0", 32, VIOLET).move_to([0, GY0 - 0.85, 0])
        stw = text("mínimos: equilíbrios estáveis", 24, VIOLET).move_to([0, GY0 - 1.42, 0])
        self.play(FadeOut(sym), FadeIn(VGroup(a0, st0), shift=UP * 0.1),
                  Indicate(self.ub_dot, color=MAGENTA, scale_factor=1.6), run_time=0.7)
        self.play(FadeIn(VGroup(aw, stw), shift=UP * 0.1),
                  *(Indicate(d, color=VIOLET, scale_factor=1.6) for d in self.well_dots), run_time=0.7)
        self.hold(2.3)
        self.play(FadeOut(VGroup(a0, st0, aw, stw, self.well_dots, res[0], note_e)), run_time=0.5)

    # ── S6 ONDE A PARTÍCULA PODE IR? ────────────────────────────────────────
    def s6(self):
        T = self.T
        self.titulo(("ONDE A PARTÍCULA", "PODE IR?"), "Movimento em uma dimensão, sem dissipação.")
        YE, XE = 4.45, -0.35
        cE = {"E": BLUE_L, "K": KCOL, "U(x)": VIOLET}

        def eq(*parts):
            return Eq(*parts, colors={i: cE[q] for i, q in enumerate(parts) if q in cE})

        e1 = eq("E", "=", "K", "+", "U(x)").at(1, XE, YE)
        self.play(FadeIn(e1.mob, shift=UP * 0.1), run_time=0.8)
        self.wait(0.6)
        self.apoio_swap("A diferença entre E e U é a energia cinética.")
        e2 = eq("K", "=", "E", "-", "U(x)").at(1, XE, YE)
        self.mm(e1, e2, M(e1, [0], e2, [2], path_arc=-PI * 0.5), M(e1, [2], e2, [0], path_arc=-PI * 0.5),
                M(e1, [1], e2, [1]), M(e1, [3], e2, [3]), M(e1, [4], e2, [4]), rt=1.3)
        self.wait(0.5)
        # K = ½mv² ≥ 0: m > 0 e v² ≥ 0
        self.apoio_swap("A energia cinética nunca é negativa.")
        k2 = Eq("K", "=", r"\frac{1}{2}", "m", "v^2", r"\ge", "0", colors={0: KCOL}).at(1, XE, YE - 1.05)
        self.born(k2, CG(e2.g(0), k2.p(0)), CG(e2.g(1), k2.p(1)), rt=1.0)
        why = mixed(tex("m>0", 30), text("e", 22, opacity=0.9), tex(r"v^2\ge0", 30), buff=0.18).move_to([0, YE - 1.95, 0])
        self.play(FadeIn(why, shift=UP * 0.1), Indicate(k2.g(3, 4), color=BLUE_L), run_time=0.7)
        self.hold(1.4)
        # K = E − U e K ≥ 0  =>  E − U(x) ≥ 0
        self.apoio_swap("Juntando as duas: E − U(x) ≥ 0.")
        e4 = eq("E", "-", "U(x)", r"\ge", "0").center_at(YE)
        self.mm(e2, e4, X(e2.p(0, 1)), M(e2, [2, 3, 4], e4, [0, 1, 2]), CG(k2.g(5), e4.p(3)), CG(k2.g(6), e4.p(4)),
                extra=(FadeOut(VGroup(k2.mob, why), run_time=0.9),), rt=1.3)
        self.wait(0.6)
        self.apoio_swap("Só são permitidas posições com U(x) ≤ E.")
        e5 = eq("U(x)", r"\le", "E").center_at(YE)
        self.mm(e4, e5, M(e4, [2], e5, [0], path_arc=-PI * 0.7), M(e4, [0], e5, [2], path_arc=-PI * 0.7),
                M(e4, [3], e5, [1]), X(e4.p(1, 4)), rt=1.3)
        box = SurroundingRectangle(e5.mob, color=BLUE_L, buff=0.18, corner_radius=0.08, stroke_width=2.5)
        self.play(Create(box), run_time=0.5)
        self.hold(2.0)
        # a linha E nasce da desigualdade: o "E" da caixa viaja até o fim da linha (valor fixo de energia)
        cp = e5.g(2).copy()
        T.E.set_value(E_SUB)
        T.LL.set_value(0)                     # o rótulo definitivo só aparece quando a cópia chega
        self.add(self.eline, self.e_lab)
        self.e_lab.update()
        self.play(cp.animate.scale(self.e_lab.height / cp.height).move_to(self.e_lab.get_center()),
                  T.LA.animate.set_value(1), run_time=1.3, rate_func=smooth)
        T.LL.set_value(1)
        self.e_lab.update()
        self.remove(cp)
        self.add(self.region_axis, self.projections, self.turning, self.particle, self.kbar, self.cursor, self.k_lab)
        self.mark("linha E")
        # leitura de K na mesma posição x: ponto na curva, nível E, segmento vertical e projeção no eixo espacial
        T.CS.set_value(1.15)
        self.apoio_swap("Vamos comparar a energia nesta posição.")
        self.play(FadeOut(VGroup(e5.mob, box)), T.CV.animate.set_value(1), T.KL.animate.set_value(1), run_time=0.8)
        n1 = mixed(tex(r"U<E", 32, BLUE_L), text("→", 26), tex(r"K>0", 32, KCOL),
                   text("posição permitida", 26, opacity=0.95)).move_to([0, -4.3, 0])
        self.play(FadeIn(n1, shift=UP * 0.1), run_time=0.5)
        self.wait(1.4)
        self.play(T.CV.animate.set_value(0), FadeOut(n1), run_time=0.4)
        n4 = text("As posições com K ≥ 0 formam o conjunto permitido.", 24, opacity=0.95).move_to([0, -4.3, 0])
        self.play(T.RG.animate.set_value(1), FadeIn(n4, shift=UP * 0.1), run_time=1.0)
        self.wait(1.1)
        # energia inicial e conservação numa só mensagem: os regimes a seguir são movimentos DIFERENTES
        n5 = VGroup(text("Cada condição inicial fixa uma energia E,", 24, opacity=0.95),
                    text("que se conserva durante o movimento.", 24, BLUE_L)).arrange(DOWN, buff=0.1)
        n5.move_to([0, -4.25, 0])
        self.play(soft_swap(n4, n5), run_time=0.6)
        self.hold(2.0)
        self.play(FadeOut(n5), run_time=0.4)

    # ── S7 Regimes ──────────────────────────────────────────────────────────
    def regime_in(self, E, traj, dl, lab, cap=None):
        """Nova condição inicial: retira a partícula e o nível anteriores, muda E, mostra o novo nível e a partícula."""
        T = self.T
        self.play(T.RG.animate.set_value(0), T.LA.animate.set_value(0), T.FB.animate.set_value(0), run_time=0.3)
        T.E.set_value(E)
        T.DL.set_value(dl)
        self.traj = traj
        T.TT.set_value(0)
        ins = [T.LA.animate.set_value(1), T.RG.animate.set_value(1), FadeIn(lab, shift=UP * 0.1)]
        if cap is not None:
            ins.append(FadeIn(cap, shift=UP * 0.1))
        self.play(*ins, run_time=0.5)
        self.play(T.VP.animate.set_value(1), T.KB.animate.set_value(1), run_time=0.4)

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
        a0 = text("Repouso em um dos mínimos.", 26, opacity=0.95).move_to([0, APO, 0])
        refn = mixed(text("com a referência escolhida:", 22, opacity=0.9), tex(r"U(\pm\ell)=0", 28, VIOLET)).move_to(slot)
        self.play(FadeOut(self._title), FadeOut(self._apoio), FadeIn(t0, shift=UP * 0.1), run_time=0.6)
        self.regime_in(0.0, traj_rest, 0.0, m0, VGroup(a0, refn))
        self.hold(1.8)
        # 0 < E < U_b -----------------------------------------------------------------------------------------
        t1 = display("ENERGIA ABAIXO DA BARREIRA", 30).move_to([0, 6.35, 0])
        m1 = mt("0", "<", "E", "<", "U_b", size=52, colors={2: BLUE_L, 4: MAGENTA}).move_to([0, 5.5, 0])
        a1 = text("Oscila deste lado, sem atravessar o centro.", 26, opacity=0.95).move_to([0, APO, 0])
        self.play(FadeOut(VGroup(t0, m0, a0, refn)), T.VP.animate.set_value(0), T.KB.animate.set_value(0), FadeIn(t1), run_time=0.4)
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
        self.timed(nD, tp2 - 0.2, tp2 + 0.75)
        forb = text("inacessível: U > E", 22, MAGENTA).move_to([0, PY + 0.5, 0])
        # a outra componente permitida existe matematicamente, mas não pertence a esta trajetória
        oth = VGroup(text("permitida, mas", 20, BLUE_L), text("outra trajetória", 20, BLUE_L)
                     ).arrange(DOWN, buff=0.06).move_to([-2.65, -3.8, 0])
        self.add(forb)
        self.timed(oth, 0.8, tp2 + 1.2)
        T.FB.set_value(1)
        self.go(tp2 + 0.5)
        self.clear_timed()
        self.add(oth.set_opacity(1))
        self.go(tp2 + 0.75, FadeOut(forb), FadeOut(oth), T.VP.animate.set_value(0), T.KB.animate.set_value(0))
        # E = U_b -----------------------------------------------------------------------------------------------
        t2 = display("ENERGIA NO LIMIAR", 30).move_to([0, 6.35, 0])
        m2 = mt("E", "=", "U_b", size=52, colors={0: BLUE_L, 2: MAGENTA}).move_to([0, 5.5, 0])
        a2 = text("Aproxima-se do centro cada vez mais devagar.", 26, opacity=0.95).move_to([0, APO, 0])
        a2b = mt(r"x\to0\ \ \text{quando}\ \ t\to\infty", size=36).move_to([0, APO, 0])
        self.play(FadeOut(VGroup(t1, m1, a1)), FadeIn(t2), T.FB.animate.set_value(0), run_time=0.4)
        sepl = text("SEPARATRIZ", 20, opacity=0.7).move_to([2.55, 5.5, 0])
        self.regime_in(E_SEP, traj_sep, 1.0, m2, sepl)
        self.mark("separatriz")
        ex = text("repouso exato em x = 0 é outro caso", 22, opacity=0.95).move_to(slot)
        self.timed(a2, 0.0, 5.0)
        self.timed(a2b, 5.2, 99.0)
        self.timed(ex, 6.6, 99.0)
        self.go(SEP_T - 0.4)
        self.clear_timed()
        self.add(a2b, ex)
        self.go(SEP_T, FadeOut(a2b), FadeOut(ex), T.VP.animate.set_value(0), T.KB.animate.set_value(0))
        # E > U_b -----------------------------------------------------------------------------------------------
        t3 = display("ENERGIA ACIMA DA BARREIRA", 30).move_to([0, 6.35, 0])
        m3 = mt("E", ">", "U_b", size=52, colors={0: BLUE_L, 2: MAGENTA}).move_to([0, 5.5, 0])
        a3 = text("Atravessa, mas permanece limitada.", 26, opacity=0.95).move_to([0, APO, 0])
        self.play(FadeOut(VGroup(t2, m2, sepl)), FadeIn(t3), run_time=0.4)
        self.regime_in(E_SUP, traj_sup, 0.0, m3)
        self.mark("travessia")
        tc1, tp_a = SUP_CEN[0], SUP_TP[0]
        n_a = text("retorno externo: K = 0", 26, opacity=0.95).move_to(slot)
        n_b = text("K > 0 no centro: atravessa", 26, opacity=0.95).move_to(slot)
        n_c = text("retorno externo: K = 0, o sentido muda", 24, opacity=0.95).move_to(slot)
        self.timed(n_a, 0.0, 1.0)
        self.timed(n_b, tc1 - 0.5, tc1 + 0.9)
        self.timed(n_c, tp_a - 0.3, tp_a + 1.0)
        n_d = mt(r"U(x)\to+\infty\ \ \text{quando}\ \ |x|\to\infty", size=32).move_to(slot)
        self.timed(a3, tp_a + 0.9, tp_a + 2.3)
        self.timed(n_d, tp_a + 1.0, tp_a + 2.3)
        self.go(tp_a + 2.3)
        self.clear_timed()
        self.s7_cleanup = VGroup(t3, m3)
        self.mark("retorno externo")

    # ── S8 Último quadro: o mesmo U(x), os três níveis identificados, título e @labparallax ─
    def s8(self):
        T = self.T
        self.play(FadeOut(self.s7_cleanup), T.VP.animate.set_value(0), T.KB.animate.set_value(0),
                  T.RG.animate.set_value(0), T.LA.animate.set_value(0), T.KL.animate.set_value(0),
                  FadeOut(VGroup(self.p_base, self.p_marks)), run_time=0.5)
        levels = ((E_SUB, r"E<U_b", "Oscila de um lado."), (E_SEP, r"E=U_b", "Aproxima-se do centro."),
                  (E_SUP, r"E>U_b", "Atravessa e retorna."))
        lv = VGroup(*(Line([AXL, gy(E), 0], [AXR, gy(E), 0], color=BLUE, stroke_width=3).set_opacity(0.7)
                      for E, _, _ in levels))
        tags = VGroup(*(tex(m, 31, BLUE_L).move_to([AXR + 0.15, gy(E) + 0.26, 0]) for E, m, _ in levels))
        rows = VGroup(*(mixed(tex(m, 33, BLUE_L), text(f, 25, opacity=0.95), buff=0.3) for _, m, f in levels))
        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([0, -1.75, 0])
        for r in rows:                       # rótulos matemáticos alinhados em coluna
            r[1].align_to(rows[0][1], LEFT)
        fim = lines("A ENERGIA DECIDE", "A TRAVESSIA", size=34).move_to([0, 6.05, 0])
        handle = display("@labparallax", 50).set_color_by_gradient(CYAN, BLUE_L).move_to([0, -3.45, 0])
        self.play(LaggedStart(*(Create(v) for v in lv), lag_ratio=0.4), LaggedStart(*(FadeIn(t) for t in tags), lag_ratio=0.4),
                  FadeIn(fim, shift=UP * 0.1), run_time=1.0)
        self.play(LaggedStart(*(FadeIn(r, shift=UP * 0.08) for r in rows), lag_ratio=0.35), run_time=0.9)
        self.play(FadeIn(handle, shift=UP * 0.1), run_time=0.5)
        self.mark("último quadro")
        self.hold(2.8)
