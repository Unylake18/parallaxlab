"""Esfera maciça no looping: 2,5R -> 2,7R. Preview silencioso (3ª versão: zoom nas forças, matemática aberta).

EXERCÍCIO RESOLVIDO · EP. 04.

Unidades físicas: g = R = 1. R é o raio da trajetória do CENTRO DE MASSA (a pista física do
loop tem raio R + a); a/R = 0,12. Origem em (x, y) = (0, 0): fundo da trajetória do CM, onde a
rampa encontra o loop. h = H R é a altura inicial do CM acima desse ponto.

A trajetória do CM é uma curva única, parametrizada pelo comprimento de arco s:
  s < 0            rampa  y = M (sqrt(u² + C²) - C), x = -u   (suave e tangente ao fundo)
  0 <= s <= 2 pi   loop   (x, y) = (sin s, 1 - cos s), theta = s
  s > 2 pi         saída horizontal
Corpo genérico I = beta m a², rolando sem deslizar (v = a omega):
  v²        = 2 (H - y) / (1 + beta)          (partícula 2(H-y); esfera maciça 10(H-y)/7)
  N/mg      = [2 (H - 1) + (3 + beta) cos theta] / (1 + beta)     (no loop)
  rotação   phi = phi0 - s/a                  (no loop: -R theta/a)
Posição, giro, vetores e barras de energia saem do MESMO s (e de H, beta): nenhum keyframe.
O tempo vem de dt = ds / v.

Zoom: o enquadramento é uma transformação única scr(x, y) comandada por um ValueTracker (zm);
pista, corpo, vetores e trajetória do CM são always_redraw e acompanham o zoom sozinhos.

Cores: azul pista/geometria e N; ciano velocidade/translação; magenta rotação; violeta energia
potencial e altura; branco texto, peso, equações e energia total.

INERCIA = False remove o bloco local da derivação de I_CM.
"""

import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, PI, RIGHT, UP, AnimationGroup, Arc, Arrow, Circle, Create, DashedLine,
    DashedVMobject, Dot, Ellipse, FadeIn, FadeOut, ImageMobject, Indicate, LaggedStart, Line,
    Polygon, Succession, TransformFromCopy, Wait,
    ManimColor, MathTex, Rectangle, Scene, SurroundingRectangle, TransformMatchingTex,
    VGroup, VMobject, ValueTracker, always_redraw, config, interpolate_color, linear,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from MF_Tools import TransformByGlyphMap
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

INERCIA = True            # bloco C5: derivação visual de I_CM (local e removível)

# ── Paleta ──────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # velocidade e translação
BLUE = "#267BFF"          # pista, geometria e N
BLUE_L = "#7FB2FF"        # trajetória do CM (tracejada), R e x
VIOLET = SECONDARY_COLOR  # energia potencial e altura h
MAGENTA = "#EA63FF"       # rotação
SPHERE_FILL = "#1A2142"

SAFE_BOTTOM = -4.6        # abaixo disso: faixa reservada a legendas
SAFE_X = 3.5
HEADLINE_TOP = 6.85

BEAT, READ, READ_RES = 0.4, 1.5, 2.0
K_T = 0.85                # segundos de tela por unidade de tempo físico sqrt(R/g)
CLEAR = object()          # note(CLEAR): apaga a nota sem trocar por outra

# ── Modelo físico ───────────────────────────────────────────────────────────
BETA = 2 / 5              # esfera maciça: I = (2/5) m a²
H_PART = 2.5
H_IDEAL = (5 + BETA) / 2  # 2,7
A_R = 0.12                # a / R
R_PART = 0.05             # raio desenhado da partícula (em R)
M_SL, C_SL = 1.4, 1.7     # rampa y = M (sqrt(u² + C²) - C); curvatura no fundo M/C < 1/R


def v2(y, H, b):
    return 2 * (H - y) / (1 + b)


def n_mg(th, H, b):
    return (2 * (H - 1) + (3 + b) * np.cos(th)) / (1 + b)


def f_ramp(u):
    return M_SL * (np.sqrt(u * u + C_SL ** 2) - C_SL)


def fp_ramp(u):
    return M_SL * u / np.sqrt(u * u + C_SL ** 2)


_U = np.linspace(0.0, 6.0, 12001)
_L = np.concatenate([[0.0], np.cumsum(np.hypot(1, fp_ramp((_U[1:] + _U[:-1]) / 2)) * np.diff(_U))])


def u_of_H(H):
    return float(np.sqrt((H / M_SL + C_SL) ** 2 - C_SL ** 2))


def s_start(H):
    """Posição s do CM na rampa, em repouso, à altura H."""
    return -float(np.interp(u_of_H(H), _U, _L))


def pose(s):
    """(x, y, tx, ty) do CM em s; (tx, ty) é a tangente no sentido do movimento."""
    if s < 0:
        u = float(np.interp(-s, _L, _U))
        g = float(fp_ramp(u))
        n = np.hypot(1, g)
        return -u, float(f_ramp(u)), 1 / n, -g / n
    if s <= 2 * PI:
        return np.sin(s), 1 - np.cos(s), np.cos(s), np.sin(s)
    return s - 2 * PI, 0.0, 1.0, 0.0


def ys(s):
    s = np.atleast_1d(np.asarray(s, float))
    out = np.zeros_like(s)
    m = s < 0
    out[m] = f_ramp(np.interp(-s[m], _L, _U))
    c = (s >= 0) & (s <= 2 * PI)
    out[c] = 1 - np.cos(s[c])
    return out


TH_FAIL = float(np.arccos(-2 * (H_PART - 1) / (3 + BETA)))   # esfera com 2,5R: N = 0 (só interno)
S_END = 2 * PI + 0.55
S_MIN = s_start(3.0)


def _qa():
    th = np.linspace(0.01, 2 * PI - 0.01, 4001)
    assert np.isclose(v2(2, H_PART, 0), 1) and np.isclose(v2(2, H_IDEAL, BETA), 1)    # v_topo² = gR
    assert np.isclose(n_mg(PI, H_PART, 0), 0) and np.isclose(n_mg(PI, H_IDEAL, BETA), 0)
    assert np.isclose(H_PART, 5 / 2) and np.isclose(H_IDEAL, 27 / 10)
    assert np.isclose(2 + (1 + BETA) / 2, H_IDEAL) and np.isclose((1 + BETA) / 2, 7 / 10)   # K = 7/10 m v²
    assert np.isclose(v2(0.4, 2.5, BETA), 10 / 7 * (2.5 - 0.4))
    assert np.isclose(BETA / (1 + BETA), 2 / 7) and np.isclose(1 / (1 + BETA), 5 / 7)  # K_trans:K_rot = 5:2
    assert n_mg(th, H_IDEAL, BETA).min() > -1e-9                    # N nunca negativa com 2,7R
    assert np.isclose(np.cos(TH_FAIL), -15 / 17) and n_mg(TH_FAIL, H_PART, BETA) < 1e-9
    for H in (2.5, 2.7, 3.0):                                       # início da rampa à altura H
        assert np.isclose(pose(s_start(H))[1], H)
    a, b = pose(-1e-9), pose(1e-9)                                  # rampa -> loop contínuos
    assert np.allclose(a, b, atol=1e-6)
    assert M_SL / C_SL < 1                                          # a rampa não cruza o loop
    x = (np.arange(200000) + 0.5) / 100000 - 1                      # I_CM por discos (a = 1, rho = 1)
    I = np.pi / 2 * np.sum((1 - x ** 2) ** 2) / 100000
    assert np.isclose(I, 8 * np.pi / 15, atol=1e-8) and np.isclose(I / (4 / 3 * np.pi), 2 / 5, atol=1e-8)
    assert np.isclose(8 * np.pi / 15 * 3 / (4 * np.pi), 2 / 5)      # rho = 3m/(4 pi a³) em I = 8 pi rho a⁵/15
    # a bola em voo (esfera, 2,5R) fica dentro do loop até sumir: |p - centro| < 1 para tau <= 0.9
    x0, y0, tx, ty = pose(TH_FAIL)
    v = np.sqrt(v2(y0, H_PART, BETA))
    for tau in np.linspace(0, 1.2, 25):
        assert np.hypot(x0 + v * tx * tau, y0 + v * ty * tau - tau * tau / 2 - 1) <= 1.0 + 1e-9   # centro do loop: (0, 1)


_qa()


def roll(tr, H, b, s1, span=None):
    """Leva o tracker de s até s1 no tempo físico dt = ds / v; `span` alonga (fica parado no fim)."""
    s0 = tr.get_value()
    g = np.linspace(s0, s1, 3001)
    mid = (g[1:] + g[:-1]) / 2
    v = np.sqrt(np.maximum(v2(ys(mid), H, b), 1e-6))
    t = np.concatenate([[0.0], np.cumsum(np.diff(g) / v)])
    T = float(t[-1])
    S = T if span is None else span

    def rate(x):
        return (np.interp(min(x * S, T), t, g) - s0) / (s1 - s0)

    return tr.animate(rate_func=rate, run_time=K_T * S).set_value(s1)


# ── Geometria na tela, com zoom ─────────────────────────────────────────────
RS = 1.25                 # unidades de tela por R, sem zoom
CX, YB = 0.95, 0.75       # fundo da trajetória do CM na tela, sem zoom
XG = 3.05                 # cota de h (à direita, só sem zoom)
Z_MAX = 2.4               # zoom nas forças
P0 = np.array([CX, YB + RS])      # centro do loop, sem zoom
T1 = np.array([0.0, 1.9])        # onde o centro do loop vai com zoom máximo
ZS = {"z": 1.0}           # zoom corrente (atualizado a cada quadro por zm)


def zf():
    return (ZS["z"] - 1) / (Z_MAX - 1)


def kk():
    """Unidades de tela por R com o zoom atual."""
    return RS * ZS["z"]


def scr_v(x, y):
    t = P0 + (T1 - P0) * zf()
    k = kk()
    return np.stack([t[0] + k * np.asarray(x), t[1] + k * (np.asarray(y) - 1), np.zeros_like(np.asarray(x, float))],
                    axis=-1)


def scr(x, y):
    return scr_v(np.float64(x), np.float64(y))


_SS = np.linspace(S_MIN, S_END, 900)
_PATH = np.array([pose(s) for s in _SS])
_I0 = int(np.searchsorted(_SS, 0.0))


def track_mob(rr, op):
    """Pista física: a CM-curva deslocada de rr (raio desenhado do corpo), pelo lado oposto ao do corpo.

    A rampa fica menos visível quanto maior o zoom (fica fora do assunto: forças no loop)."""
    d = rr + 0.012
    x, y, tx, ty = _PATH.T
    P = scr_v(x + d * ty, y - d * tx)
    ramp = VMobject().set_points_as_corners(P[:_I0 + 1]).set_stroke(BLUE, 5, op * (1 - zf()))
    loop = VMobject().set_points_as_corners(P[_I0:]).set_stroke(BLUE, 5, op)
    return VGroup(ramp, loop)


def body(s, av, o, fl, H, b):
    """r = raio desenhado (R_PART = partícula). Giro: phi = phi0 - s/a, do MESMO s da posição.

    fl > 0: queda livre depois de perder o contato em TH_FAIL (só no gancho)."""
    if fl > 0:
        x0, y0, tx, ty = pose(TH_FAIL)
        v = float(np.sqrt(v2(y0, H, b)))
        x, y = x0 + v * tx * fl, y0 + v * ty * fl - 0.5 * fl * fl
        phi = PI / 2 - TH_FAIL / A_R - v / A_R * fl
        o *= float(np.clip((1.2 - fl) / 0.5, 0, 1))
    else:
        x, y, _, _ = pose(s)
        phi = PI / 2 - s / A_R
    c = scr(x, y)
    rr = max(av, R_PART) * kk()
    k = min(av / A_R, 1.0)
    disk = Circle(rr).move_to(c).set_stroke(WHITE, 2.5, o).set_fill(
        interpolate_color(ManimColor(WHITE), ManimColor(SPHERE_FILL), k), o)
    u = np.array([np.cos(phi), np.sin(phi), 0.0])
    return VGroup(disk, Line(c, c + 0.95 * rr * u).set_stroke(MAGENTA, 4, o * k))


# ── Helpers visuais ─────────────────────────────────────────────────────────
def tex(content, size=40, color=WHITE):
    return MathTex(content, font_size=size, color=color)


def mtex(*parts, size=46, color=WHITE):
    return MathTex(*parts, font_size=size, color=color)


@contextmanager
def wide_pango():
    """Largura de layout fixa para o Pango: o texto não depende da resolução nem do cache."""
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


def tag(content, size=24, color=WHITE, opacity=1.0):
    """Mensagem de uma linha, limitada à margem; falha se o Pango quebrar a linha."""
    with wide_pango():
        t = screen_text(content, size, oversample=2)
    t.set_color(color).set_opacity(opacity)
    t.scale_to_fit_width(min(t.width, 2 * SAFE_X - 0.4))
    assert t.height < 0.60, f"o Pango quebrou a linha: {content!r}"
    return t


def row(*ms, buff=0.14):
    return VGroup(*ms).arrange(RIGHT, buff=buff)


def fit(m, w=2 * SAFE_X - 0.3):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def soft_swap(old, new, shift=UP * 0.12, lag=0.55):
    return AnimationGroup(FadeOut(old, shift=shift), FadeIn(new, shift=shift), lag_ratio=lag)


def vec(a, b, color, width=6):
    return Arrow(a, b, buff=0, stroke_width=width * (1 + 0.5 * zf()), tip_length=0.2 * (1 + 0.5 * zf()), max_tip_length_to_length_ratio=0.35,
                 max_stroke_width_to_length_ratio=30, color=color)


def boxed(mob, color=WHITE):
    return VGroup(mob, SurroundingRectangle(mob, color=color, buff=0.15, corner_radius=0.08, stroke_width=2.5))


def span_mark(a, b, color, ticks=0.11, width=2.5, op=0.9):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0], 0.0]) * ticks
    return VGroup(Line(a, b), Line(a - n, a + n), Line(b - n, b + n)).set_stroke(color, width, op)


FS = 0.4                  # comprimento da seta por mg (sem zoom)
VS = 0.55                 # comprimento da seta de v por sqrt(gR) (sem zoom)
BAR_X0, BAR_W, BAR_H, BAR_Y, H_REF = -2.7, 5.4, 0.30, -0.5, 2.7
GX0, GY0, GW, GH = -2.5, -3.3, 5.6, 1.65     # gráfico cartesiano de energia (origem e tamanho)


class LoopingEsfera010(Scene):
    op_y = -2.50
    note_y = -3.75

    # ── Infraestrutura de quadro ────────────────────────────────────────────
    def mark(self, name):
        print(f"[T] {name} t={self.renderer.time:.1f}s")

    def caption(self, *lines):
        new = VGroup(*(display(line) for line in lines)).arrange(DOWN, buff=0.14)
        fit(new, 2 * SAFE_X - 0.2)
        new.move_to([0, HEADLINE_TOP - new.height / 2, 0])
        anims = [soft_swap(self.headline, new, UP * 0.15)] if self.headline is not None \
            else [FadeIn(new, shift=DOWN * 0.15)]
        self.headline = new
        return anims

    def note_anims(self, new):
        """Animações da troca da nota inferior (new=None: mantém; CLEAR: apaga)."""
        if new is None:
            return []
        if new is CLEAR:
            anims = [FadeOut(self.hint, shift=UP * 0.08)] if self.hint is not None else []
            self.hint = None
            return anims
        fit(new).move_to([0, self.note_y, 0])
        anims = [soft_swap(self.hint, new, UP * 0.08)] if self.hint is not None \
            else [FadeIn(new, shift=UP * 0.08)]
        self.hint = new
        return anims

    def note(self, new, *extra, run_time=0.55):
        anims = self.note_anims(new)
        if anims or extra:
            self.play(*anims, *extra, run_time=run_time)

    def show_expr(self, new, *extra, run_time=0.8, match=False):
        fit(new).move_to([0, self.op_y, 0])
        if self.expr is None:
            anims = [FadeIn(new, shift=UP * 0.1)]
        elif match:
            anims = [TransformMatchingTex(self.expr, new)]
        else:
            anims = [soft_swap(self.expr, new)]
        self.play(*anims, *extra, run_time=run_time)
        self.expr = new

    def step(self, new, note=None, hold=0.8, match=True, rt=0.65, extra=()):
        """Nova expressão (e nota) na mesma animação; depois um respiro para ler."""
        self.show_expr(new, *self.note_anims(note), *extra, run_time=rt, match=match)
        self.wait(hold + 0.3)

    def gmap(self, new, *entries, frame=None, extra=(), run_time=1.2, **kw):
        """Como show_expr, mas com mapa explícito de glifos (MF-Tools). Só entre MathTex de string única.

        Os índices valem para as fórmulas exatamente como estão escritas: mexeu no LaTeX, refaça o mapa
        (para ver os índices: TransformByGlyphMap(a, b, show_indices=True), só em desenvolvimento).
        frame: `boxed(new)`; a moldura entra junto e o grupo vira a expressão corrente."""
        fit(frame or new).move_to([0, self.op_y, 0])
        old = self.expr
        self.play(TransformByGlyphMap(old, new, *entries, **kw), *extra, run_time=run_time)
        self.remove(old)
        if frame:
            self.play(FadeIn(frame[1]), run_time=0.3)
            self.add(frame)
        self.expr = frame or new

    def clear_text(self, *extra, run_time=0.5):
        anims = [FadeOut(m) for m in (self.expr, self.hint) if m is not None]
        self.expr = self.hint = None
        if anims or extra:
            self.play(*anims, *extra, run_time=run_time)

    def show(self, *ms, run_time=0.5):
        """FadeIn de objetos always_redraw: atualiza antes para não mostrar estado velho."""
        for m in ms:
            m.update()
        self.play(*(FadeIn(m) for m in ms), run_time=run_time)

    def zoom(self, z, run_time=1.2):
        return self.zm.animate(run_time=run_time).set_value(z)

    def check_safe(self):
        skip = set()
        for m in self.bleed:
            skip.update(id(x) for x in m.get_family())
        for m in self.mobjects:
            if not isinstance(m, VMobject) or id(m) in skip or not len(m.get_all_points()):
                continue
            who = getattr(m, "tex_string", None) or getattr(m, "text", None) or type(m).__name__
            assert m.get_bottom()[1] > SAFE_BOTTOM, f"invade a faixa inferior: {m.get_bottom()[1]:.2f} [{who}]"
            assert m.get_left()[0] > -SAFE_X and m.get_right()[0] < SAFE_X, \
                f"fora da margem lateral: {m.get_left()[0]:.2f}..{m.get_right()[0]:.2f} [{who}]"

    # ── Estado físico: um único s, mais H e beta ───────────────────────────
    def cs(self):
        return s_start(self.H.get_value()) if self.rest.get_value() > 0.5 else self.S.get_value()

    def put(self, *, H=None, b=None, av=None, s=None):
        """Reposiciona o corpo: s=None = em repouso no início da rampa à altura H."""
        for tr, v in ((self.H, H), (self.b, b), (self.av, av)):
            if v is not None:
                tr.set_value(v)
        self.fl.set_value(0.0)
        self.rest.set_value(1.0 if s is None else 0.0)
        if s is not None:
            self.S.set_value(s)

    def go(self, s1, span=None):
        """Solta o corpo do início e anima s até s1."""
        if self.rest.get_value() > 0.5:
            self.S.set_value(s_start(self.H.get_value()))
            self.rest.set_value(0.0)
        return roll(self.S, self.H.get_value(), self.b.get_value(), s1, span)

    def build(self):
        self.S, self.H, self.b, self.av, self.fl, self.rest, self.bo, self.zm, self.tk = (
            ValueTracker(v) for v in (0.0, H_PART, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0))
        self.spin = ValueTracker(0.0)      # giro contínuo do disco extraído (bloco de I_CM)
        self.spin.add_updater(lambda m, dt: m.increment_value(2.4 * dt))
        # o zoom global é atualizado antes de todo always_redraw (este objeto é o primeiro da cena)
        self.zdrv = VMobject()
        self.zdrv.add_updater(lambda m: ZS.update(z=self.zm.get_value()))
        self.add(self.zdrv)
        st = lambda: (self.cs(), self.H.get_value(), self.b.get_value(), self.av.get_value())
        vz = lambda: 1 + zf()

        self.trk = always_redraw(lambda: track_mob(max(self.av.get_value(), R_PART), self.tk.get_value()))
        self.cmp = always_redraw(lambda: DashedVMobject(Circle(kk()).move_to(scr(0, 1)), num_dashes=72)
                                 .set_stroke(BLUE_L, 2, 0.5))
        self.bod = always_redraw(lambda: body(self.cs(), self.av.get_value(), self.bo.get_value(),
                                              self.fl.get_value(), self.H.get_value(), self.b.get_value()))

        def varrow():
            s, H_, b_, _ = st()
            x, y, tx, ty = pose(s)
            c = scr(x, y)
            L = VS * vz() * np.sqrt(max(v2(y, H_, b_), 0))
            t = np.array([tx, ty, 0.0])
            return VGroup(vec(c, c + L * t, CYAN), tex("v", 32, CYAN).scale(1 + 0.5 * zf()).move_to(c + (L + 0.22 * vz()) * t + 0.05 * UP))

        def forces():
            s, H_, b_, r_ = st()
            g = VGroup()
            if not (0.02 < s < 2 * PI - 0.02 and abs(s - PI) < 1.7):   # só a metade de cima do loop
                return g
            x, y, tx, ty = pose(s)
            c, n, t = scr(x, y), np.array([np.sin(s), -np.cos(s), 0.0]), np.array([tx, ty, 0.0])
            rr = max(r_, R_PART) * kk()
            fs = FS * vz()
            g.add(vec(c - 0.1 * t, c - 0.1 * t + fs * DOWN, WHITE),
                  tex("mg", 30).scale(1 + 0.5 * zf()).move_to(c - 0.1 * t + fs * 0.55 * DOWN + 0.38 * vz() * RIGHT))
            N = n_mg(s, H_, b_)
            if N > 0.02:
                pc = c + rr * n + 0.1 * t
                g.add(vec(pc, pc - fs * N * n, BLUE),
                      tex("N", 30, BLUE).scale(1 + 0.5 * zf()).move_to(pc - fs * N * 0.5 * n + 0.32 * vz() * LEFT).set_opacity(min(1, N / 0.15)))
            return g

        def hmark():
            H_ = self.H.get_value()
            y = YB + RS * H_
            xs = CX - RS * u_of_H(H_)
            return VGroup(
                DashedLine([xs - 0.15, y, 0], [XG, y, 0], dash_length=0.12).set_stroke(VIOLET, 2.5, 0.9),
                DashedLine([CX, YB, 0], [XG, YB, 0], dash_length=0.08).set_stroke(VIOLET, 1.5, 0.4),
                span_mark([XG, YB, 0], [XG, y, 0], VIOLET),
                tex("h", 36, VIOLET).move_to([XG + 0.24, (YB + y) / 2, 0]))

        def ebar():
            s, H_, b_, _ = st()
            U = float(ys(s)[0])
            K = max(H_ - U, 0.0)
            g, x = VGroup(), BAR_X0
            for val, col in ((U, VIOLET), (K / (1 + b_), CYAN), (K * b_ / (1 + b_), MAGENTA)):
                w = BAR_W * val / H_REF
                if w > 1e-3:
                    g.add(Rectangle(width=w, height=BAR_H).set_stroke(width=0).set_fill(col, 0.9)
                          .move_to([x + w / 2, BAR_Y, 0]))
                x += w
            W = BAR_W * H_ / H_REF
            return g.add(Rectangle(width=W, height=BAR_H).move_to([BAR_X0 + W / 2, BAR_Y, 0]).set_stroke(WHITE, 2))

        self.varr = always_redraw(varrow)
        self.forc = always_redraw(forces)
        self.hmk = always_redraw(hmark)
        self.bar = always_redraw(ebar)
        self.hval = None

        # R: trajetória do CM (aparece uma vez, com zoom)
        self.rline = always_redraw(lambda: Line(scr(0, 1), scr(-1, 1)).set_stroke(BLUE_L, 2.5))
        self.rlab = row(tex("R", 30, BLUE_L), text(": TRAJETÓRIA DO CM", 15, BLUE_L), buff=0.05)
        self.rlab.add_updater(lambda m: m.move_to(scr(0, 1) + np.array([0, -0.55 * (1 + zf()), 0])))

        # ω no topo (esfera em s = pi)
        self.warc = always_redraw(lambda: Arc(radius=A_R * kk() + 0.25, start_angle=0.75 * PI, angle=-0.7 * PI,
                                              arc_center=scr(0, 2)).set_stroke(MAGENTA, 4).add_tip(tip_length=0.13))
        self.wlab = tex(r"\omega", 32, MAGENTA)
        self.wlab.add_updater(lambda m: m.move_to(scr(0, 2) + (A_R * kk() + 0.75) * np.array([np.cos(0.3), np.sin(0.3), 0])))
        self.esf = [self.warc, self.wlab]

        legend = VGroup()
        for s_, col in (("U", VIOLET), (r"K_{\rm trans}", CYAN), (r"K_{\rm rot}", MAGENTA)):
            legend.add(row(Rectangle(width=0.22, height=0.22).set_stroke(width=0).set_fill(col, 0.9),
                           tex(s_, 30), buff=0.1))
        legend.arrange(RIGHT, buff=0.55).move_to([0, BAR_Y - 0.6, 0])
        self.bargroup = VGroup(legend, tag("ENERGIA TOTAL: CONSTANTE", 18, opacity=0.75).move_to([0, BAR_Y + 0.42, 0]))

    def hval_label(self, s):
        lab = tex(s, 32, VIOLET)
        lab.add_updater(lambda m: m.move_to([1.5, YB + RS * self.H.get_value() + 0.3, 0]))
        lab.update()
        return lab

    def set_hval(self, s=None):
        new = self.hval_label(s) if s else None
        anims = ([FadeOut(self.hval)] if self.hval is not None else []) + ([FadeIn(new)] if new else [])
        self.hval = new
        return anims

    # ── Cena ────────────────────────────────────────────────────────────────
    def construct(self):
        ZS["z"] = 1.0
        self.camera.background_color = BACKGROUND_COLOR
        self.headline = self.hint = self.expr = None
        watermark = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(watermark.to_corner(UP + RIGHT, buff=0.28))
        self.series = text("EXERCÍCIO RESOLVIDO · EP. 04", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4)
        self.build()
        self.bleed = [self.series, self.trk]

        self.c1_gancho()
        self.c2_topo()
        self.c3_particula()
        self.c4_esfera()
        if INERCIA:
            self.c5_inercia()
        self.c6_energia()
        self.c7_barras()
        self.c8_limite()
        self.c9_payoff()
        self.c10_sintese()
        self.mark("fim")

    # C1 — gancho: mesma altura, resultados diferentes
    def c1_gancho(self):
        who = tag("PARTÍCULA", 24).move_to([0, -0.55, 0])
        self.put(H=H_PART, b=0.0, av=0.0)
        self.add(self.bod)                              # invisível (bo = 0) até soltar o corpo
        self.play(FadeIn(self.series), *self.caption("POR QUE 2,5R NÃO BASTA", "PARA UMA ESFERA?"), run_time=0.8)
        self.show(self.trk, self.hmk, self.cmp)
        self.play(*self.set_hval(r"h=2{,}5R"), self.bo.animate.set_value(1), FadeIn(who), run_time=0.6)
        self.wait(BEAT)
        self.play(self.go(S_END))
        done = tag("COMPLETA", 24, CYAN).move_to([0, -1.2, 0])
        self.play(FadeIn(done), run_time=0.4)
        self.wait(BEAT)
        who2 = tag("ESFERA MACIÇA", 24).move_to([0, -0.55, 0])
        self.play(self.bo.animate.set_value(0), FadeOut(who), FadeOut(done), run_time=0.4)
        self.put(b=BETA, av=A_R)
        self.play(self.bo.animate.set_value(1), FadeIn(who2), run_time=0.4)
        self.play(self.go(TH_FAIL))
        # perde o contato antes do topo e cai dentro do loop (voo curto; sem tratar o que vem depois)
        fail = tag("NÃO COMPLETA", 24, MAGENTA).move_to([0, -1.2, 0])
        self.play(self.fl.animate(rate_func=linear, run_time=1.2 * K_T).set_value(1.2), FadeIn(fail))
        self.check_safe()
        self.wait(READ_RES)
        self.play(FadeOut(fail), FadeOut(who2), FadeOut(self.hmk), *self.set_hval(None), run_time=0.5)
        self.put(av=A_R)
        self.bo.set_value(0)

    # C2 — condição de contato no topo (partícula), com zoom no loop
    def c2_topo(self):
        self.mark("C2")
        self.put(H=2.9, b=0.0, av=0.0, s=PI)
        self.play(*self.caption("O TOPO DO LOOP"), self.bo.animate.set_value(1), run_time=0.6)
        self.play(self.zoom(Z_MAX, 1.3), run_time=1.3)
        self.show(self.rline, self.rlab, self.forc, self.varr)
        self.show_expr(mtex("mg", "+", "N", "=", r"\frac{mv^2}{R}"))
        self.expr[2].set_color(BLUE)
        self.note(tag("A PISTA SÓ EMPURRA, NÃO PUXA"))
        self.wait(READ)
        self.note(tag("MENOS ALTURA: A PISTA EMPURRA MENOS"), FadeOut(self.rline), FadeOut(self.rlab))
        self.play(self.H.animate.set_value(H_PART), run_time=1.8)
        self.show_expr(mtex("mg", "+", "0", "=", r"\frac{mv^2}{R}"))
        self.note(row(text("NO LIMITE,"), tex("N=0", 36, BLUE)))
        self.wait(READ)
        self.show_expr(boxed(mtex(r"v_{\rm topo}^2", "=", "gR", size=54)))
        self.check_safe()
        self.wait(READ_RES)

    # C3 — resultado clássico 2,5R
    def c3_particula(self):
        self.mark("C3")
        top = YB + 2 * RS
        self.cota2R = VGroup(span_mark([2.55, YB, 0], [2.55, top, 0], VIOLET),
                             tex("2R", 32, VIOLET).move_to([2.82, YB + RS, 0]))
        self.clear_text(*self.caption("PARTÍCULA: ALTURA MÍNIMA"), self.zoom(1, 1.1),
                        FadeOut(self.forc), FadeOut(self.varr), run_time=1.1)
        self.hmk.update()
        self.play(FadeIn(self.hmk), FadeIn(self.cota2R), *self.set_hval(r"h=2{,}5R"), run_time=0.6)
        a = mtex("mgh", "=", "mg(2R)", "+", r"\tfrac12 mv_{\rm topo}^2", size=42)
        self.step(a, row(text("NO TOPO:", 20), tex("y=2R", 30), text("E", 20), tex("v^2=gR", 30)),
                  match=False, hold=0.7)
        c = mtex("mgh", "=", "2mgR", "+", r"\tfrac12 m(gR)", size=42)
        c[4].set_color(CYAN)
        self.step(c, hold=0.7)
        self.step(mtex("mgh", "=", "2mgR", "+", r"\tfrac12 mgR", size=42), hold=0.5)
        self.step(mtex("mgh", "=", r"\tfrac52 mgR", size=42), tex(r"2+\tfrac12=\tfrac52", 32), hold=0.5)
        self.step(mtex("h", "=", r"\tfrac52", "R"), CLEAR, hold=0.4)
        self.show_expr(boxed(mtex(r"h_{\min}", "=", r"2{,}5R", size=54)), *self.note_anims(tag("PARTÍCULA")))
        self.check_safe()
        self.wait(READ_RES)

    # C4 — a partícula vira esfera; a condição no topo não muda (zoom)
    def c4_esfera(self):
        self.mark("C4")
        self.clear_text(*self.caption("E A ESFERA?"), FadeOut(self.hmk), *self.set_hval(None), FadeOut(self.cota2R))
        self.play(self.zoom(Z_MAX, 1.2), run_time=1.2)
        # v_topo² = 2(H - 2)/(1 + beta): H e beta lineares juntos mantêm v_topo² = gR durante a troca
        self.show(self.varr, self.forc)
        self.play(self.av.animate.set_value(A_R), self.b.animate.set_value(BETA),
                  self.H.animate.set_value(H_IDEAL), run_time=1.5)
        self.show(*self.esf)
        self.note(tag("A CONDIÇÃO NO TOPO MUDOU?"))
        self.wait(READ)
        self.show_expr(mtex("mg", "+", "N", "=", r"\frac{mv^2}{R}"))
        self.expr[2].set_color(BLUE)
        self.wait(BEAT)
        self.show_expr(boxed(mtex(r"v_{\rm topo}^2", "=", "gR", size=54)))
        self.note(tag("NÃO: A VELOCIDADE MÍNIMA É A MESMA"))
        self.check_safe()
        self.wait(READ_RES)

    # C5 — I_CM por discos finos (bloco experimental, local e removível)
    def c5_inercia(self):
        self.mark("C5")
        self.op_y, self.note_y = -1.3, -2.75
        out = [self.trk, self.cmp, self.bod, self.forc, self.varr, *self.esf]
        self.clear_text(*self.caption("DE ONDE VEM O 2/5?"), *(FadeOut(m) for m in out), self.zoom(1, 0.7),
                        run_time=0.7)

        Cs, Cd = np.array([-1.35, 2.35, 0.0]), np.array([2.05, 2.35, 0.0])
        Ra, ND, I0 = 1.45, 15, 11
        xs = Ra * (-1 + (2 * np.arange(ND) + 1) / ND)
        rs = np.sqrt(Ra ** 2 - xs ** 2)
        x0, r0 = xs[I0], rs[I0]
        Pd, top = Cs + [x0, 0, 0], Cs + [x0, r0, 0]
        sph = Circle(Ra).move_to(Cs).set_stroke(WHITE, 3).set_fill(SPHERE_FILL, 1)
        axis = DashedLine(Cs + [-1.95, 0, 0], Cs + [1.75, 0, 0], dash_length=0.12).set_stroke(WHITE, 2, 0.75)
        cmd = Dot(Cs, 0.06, color=WHITE)
        discs = VGroup(*(Ellipse(width=0.15, height=2 * r).move_to(Cs + [x, 0, 0]).set_stroke(BLUE_L, 2, 0.6)
                         for x, r in zip(xs, rs)))
        hl = discs[I0]
        poly = Polygon(Cs, Pd, top).set_stroke(width=0).set_fill(BLUE_L, 0.18)
        a_line = Line(Cs, top).set_stroke(WHITE, 4)
        a_lab = tex("a", 40).move_to(Cs + [x0 / 2 - 0.28, r0 / 2 + 0.2, 0])
        x_leg = Line(Cs, Pd).set_stroke(BLUE_L, 5)
        x_lab = tex("x", 40, BLUE_L).move_to(Cs + [x0 / 2, -0.35, 0])
        r_leg = Line(Pd, top).set_stroke(MAGENTA, 5)
        r_lab = tex("r", 40, MAGENTA).move_to(Cs + [x0 + 0.33, r0 / 2, 0])
        sq = VMobject().set_points_as_corners([Pd + [-0.18, 0, 0], Pd + [-0.18, 0.18, 0], Pd + [0, 0.18, 0]]
                                              ).set_stroke(WHITE, 2, 0.9)
        dx_span = span_mark(Cs + [x0 - 0.15, -r0 - 0.13, 0], Cs + [x0 + 0.15, -r0 - 0.13, 0], VIOLET)
        dx_lab = tex("dx", 30, VIOLET).move_to(Cs + [x0, -r0 - 0.42, 0])
        # o disco extraído, visto de frente, girando em torno do próprio eixo
        phi = lambda: -self.spin.get_value()
        face = Circle(r0).move_to(Cd).set_stroke(MAGENTA, 3).set_fill(MAGENTA, 0.3)
        spoke = always_redraw(lambda: Line(Cd, Cd + r0 * np.array([np.cos(phi()), np.sin(phi()), 0.0]))
                              .set_stroke(WHITE, 4))
        rl = tex("r", 36, MAGENTA)
        rl.add_updater(lambda m: m.move_to(Cd + 0.55 * r0 * np.array([np.cos(phi()), np.sin(phi()), 0.0])
                                           + 0.28 * np.array([-np.sin(phi()), np.cos(phi()), 0.0])))
        warc_d = Arc(radius=0.4, start_angle=2.5, angle=-1.8, arc_center=Cd).set_stroke(MAGENTA, 4)
        warc_d.add_tip(tip_length=0.14)
        dm_lab = tex("dm", 34, MAGENTA).move_to(Cd + [0, -r0 - 0.38, 0])
        self.spin.set_value(0.0)
        self.add(self.spin)

        self.play(FadeIn(sph), FadeIn(axis), FadeIn(cmd), Create(a_line), FadeIn(a_lab), run_time=0.9)
        self.play(*self.note_anims(row(text("ESFERA HOMOGÊNEA, DENSIDADE", 20), tex(r"\rho", 32),
                                       text("· EIXO PELO CM", 20))),
                  LaggedStart(*(FadeIn(d) for d in discs), lag_ratio=0.05), run_time=1.2)
        dim = [d.animate.set_stroke(BLUE_L, 2, 0.3) for i, d in enumerate(discs) if i != I0]
        self.play(hl.animate.set_stroke(MAGENTA, 3, 1).set_fill(MAGENTA, 0.55), *dim, FadeIn(poly),
                  Create(x_leg), Create(r_leg), FadeIn(sq), FadeIn(x_lab), FadeIn(r_lab),
                  Create(dx_span), FadeIn(dx_lab), *self.note_anims(tag("UMA FATIA: DISCO FINO DE ESPESSURA dx", 20)),
                  run_time=1.3)
        self.play(TransformFromCopy(hl, face), FadeIn(spoke), FadeIn(rl), Create(warc_d), FadeIn(dm_lab),
                  *self.note_anims(tag("O DISCO, VISTO DE FRENTE, GIRA NO PRÓPRIO EIXO", 20)), run_time=1.3)
        self.add(face)

        # triângulo a, x, r  ->  r² = a² - x²
        p1 = mtex("a^2=x^2+r^2")                    # string única: o p1 -> p2 usa mapa de glifos
        p1[0][3:5].set_color(BLUE_L), p1[0][6:8].set_color(MAGENTA)
        self.step(p1, tag("PITÁGORAS NO TRIÂNGULO a, x, r", 20), match=False, hold=0.8, rt=1.0,
                  extra=(Indicate(a_line, color=WHITE), Indicate(x_leg, color=BLUE_L),
                         Indicate(r_leg, color=MAGENTA)))
        p2 = mtex("r^2=a^2-x^2")
        p2[0][0:2].set_color(MAGENTA), p2[0][6:8].set_color(BLUE_L)
        # a² e x² passam por cima, r² por baixo (em linha reta se cruzariam sobre o =); o + sai e o − entra
        self.gmap(p2, ([0, 1], [3, 4], {"path_arc": -PI}), ([2], [2]),
                  ([3, 4], [6, 7], {"path_arc": -PI}), ([6, 7], [0, 1], {"path_arc": -PI * 0.75}),
                  ([5], []), ([], [5], {"delay": 0.7}), run_time=1.5)
        self.wait(0.7)

        # massa da fatia
        e1 = mtex("dV", "=", r"\pi r^2", "dx")
        e1[2].set_color(MAGENTA)
        self.step(e1, tag("VOLUME: ÁREA DO DISCO × ESPESSURA", 20), match=False, hold=0.7)
        self.step(mtex("dm", "=", r"\rho", "dV"), tag("MASSA = DENSIDADE × VOLUME", 20), hold=0.6)
        self.step(mtex("dm", "=", r"\rho", r"\pi r^2", "dx"), hold=0.6)
        self.step(mtex("dm", "=", r"\rho", r"\pi (a^2-x^2)", "dx"),
                  row(text("COM", 20), tex(r"r^2=a^2-x^2", 30)), hold=0.8)

        # momento da fatia
        self.step(mtex("dI", "=", r"\tfrac12", "r^2", "dm"), tag("DISCO FINO GIRANDO EM TORNO DO EIXO", 20),
                  match=False, hold=0.8)
        self.step(mtex("dI", "=", r"\tfrac12", "(a^2-x^2)", "dm"), row(text("TROCANDO", 20), tex("r^2", 30)),
                  hold=0.5)
        self.step(mtex("dI", "=", r"\tfrac12", "(a^2-x^2)", r"\rho\pi(a^2-x^2)dx", size=42),
                  row(text("E", 20), tex("dm", 30)), hold=0.6)
        self.step(mtex("dI", "=", r"\frac{\rho\pi}{2}", "(a^2-x^2)^2", "dx"), CLEAR, hold=0.8)

        # soma de todos os discos
        light = LaggedStart(*(d.animate.set_stroke(MAGENTA, 3, 1).set_fill(MAGENTA, 0.4) for d in discs),
                            lag_ratio=0.06)
        self.show_expr(mtex("I", "=", r"\int dI"), light, *self.note_anims(tag("SOMA DE TODOS OS DISCOS", 20)),
                       run_time=1.2)
        self.wait(0.4)
        self.step(mtex("I", "=", r"\frac{\rho\pi}{2}\int_{-a}^{a}", "(a^2-x^2)^2", "dx", size=42), hold=0.6)
        self.step(mtex("I", "=", r"\frac{\rho\pi}{2}\int_{-a}^{a}", "(a^4-2a^2x^2+x^4)", "dx", size=42),
                  tex(r"(a^2-x^2)^2=a^4-2a^2x^2+x^4", 30), hold=0.6)
        self.step(mtex("I", "=", r"\frac{8\pi\rho\,a^5}{15}"), tag("AVALIANDO ENTRE OS EXTREMOS DA ESFERA", 20),
                  match=False, hold=0.8)

        # massa total e resultado
        self.step(mtex("m", "=", r"\tfrac43", r"\pi\rho a^3"), tag("MASSA TOTAL DA ESFERA", 20), match=False, hold=0.6)
        self.step(mtex(r"\rho", "=", r"\frac{3m}{4\pi a^3}"), tag("ISOLANDO A DENSIDADE", 20), match=False, hold=0.6)
        self.step(mtex("I", "=", r"\frac{8\pi a^5}{15}", r"\cdot", r"\frac{3m}{4\pi a^3}"),
                  row(text("SUBSTITUINDO", 20), tex(r"\rho", 30)), match=False, hold=0.6)
        g3 = mtex(r"I=\frac{8}{15}\cdot\frac{3}{4}\cdot\frac{\pi a^5}{\pi a^3}\cdot m", size=42)
        g3[0][11:18].set_color(MAGENTA)
        self.step(g3, row(tex(r"\pi", 30), text("E", 20), tex("a^3", 30), text("SE CANCELAM", 20)),
                  match=False, hold=0.7)
        res = mtex(r"I_{CM}=\tfrac25 ma^2", size=56)
        res[0][4:7].set_color(MAGENTA)
        bx = boxed(res)
        # π e a³ se cancelam (um sobe, o outro desce); 8/15·3/4 sai e 2/5 entra; a⁵/a³ deixa a²
        # primeiro sai o que cancela; só depois o resto se reacomoda (m passa por baixo do a)
        self.gmap(res, ([11], [], {"shift": UP * 0.35}), ([15], [], {"shift": DOWN * 0.35}),
                  ([16, 17], [], {"shift": DOWN * 0.35}), ([14, 18], []),
                  ([2, 3, 4, 5, 6, 7, 8, 9, 10], []),
                  ([0], [0], {"delay": 0.5}), ([1], [3], {"delay": 0.5}), ([12], [8], {"delay": 0.5}),
                  ([13], [9], {"delay": 0.6}), ([19], [7], {"delay": 0.8, "path_arc": -PI * 0.8}),
                  ([], [1, 2], {"delay": 0.8}), ([], [4, 5, 6], {"delay": 0.9}),
                  frame=bx, extra=self.note_anims(CLEAR), run_time=1.8)
        self.play(bx.animate.scale(1.18), run_time=0.6)
        self.play(bx[1].animate.set_stroke(MAGENTA, 4), Indicate(bx[0][0][4:7], color=MAGENTA, scale_factor=1.5),
                  Indicate(sph, color=MAGENTA, scale_factor=1.03), run_time=1.0)
        self.check_safe()
        self.wait(READ)

        gone = VGroup(sph, axis, cmd, discs, a_line, a_lab, x_leg, x_lab, r_leg, r_lab, sq, poly, dx_span, dx_lab,
                      face, spoke, rl, warc_d, dm_lab)
        self.op_y, self.note_y = -2.50, -3.75
        self.put(H=H_PART)
        self.clear_text(FadeOut(gone), run_time=0.5)
        self.remove(self.spin)
        self.show(self.trk, self.bod, self.cmp)

    # C6 — energia da esfera: K = 7/10 m v²
    def c6_energia(self):
        self.mark("C6")
        left = [m for m in (self.forc, self.varr, self.rline, self.rlab, *self.esf) if m in self.mobjects]
        extra = [self.zoom(1, 0.8)] if self.zm.get_value() > 1 else []
        self.clear_text(*self.caption("ENERGIA DA ESFERA"), self.bo.animate.set_value(0),
                        *(FadeOut(m) for m in left), *extra, run_time=0.8)
        self.put(H=H_PART)
        self.play(self.bo.animate.set_value(1), run_time=0.4)
        k1 = mtex("K", "=", r"\tfrac12 mv^2", "+", r"\tfrac12 I_{CM}\,\omega^2", size=44)
        k1[2].set_color(CYAN), k1[4].set_color(MAGENTA)
        self.show_expr(k1, *self.note_anims(tag("TRANSLAÇÃO + ROTAÇÃO")))
        self.wait(READ)
        sub = mtex(r"I_{CM}=\tfrac25 ma^2", r"\qquad", r"\omega=\frac{v}{a}", size=36)
        sub[0].set_color(MAGENTA)
        self.note(sub)
        self.wait(0.6)
        k2 = mtex("K", "=", r"\tfrac12 mv^2", "+", r"\tfrac12\left(\tfrac25 ma^2\right)\left(\frac{v}{a}\right)^2",
                  size=42)
        k2[2].set_color(CYAN), k2[4].set_color(MAGENTA)
        self.show_expr(k2, match=True, run_time=1.0)
        self.wait(READ)
        # k2 -> k3 com mapa de glifos: troca k2 (partes, para o TransformMatchingTex acima) pela mesma
        # fórmula em string única, no mesmo lugar e escala (sem salto visível)
        k2s = mtex(r"K=\tfrac12 mv^2+\tfrac12\left(\tfrac25 ma^2\right)\left(\frac{v}{a}\right)^2", size=42)
        k2s.match_width(k2).move_to(k2)
        k2s[0][2:8].set_color(CYAN), k2s[0][9:26].set_color(MAGENTA)
        self.remove(k2)
        self.add(k2s)
        self.expr = k2s
        k3 = mtex(r"K=\tfrac12 mv^2+\tfrac15 mv^2", size=44)
        k3[0][2:8].set_color(CYAN), k3[0][9:15].set_color(MAGENTA)
        # a² (em ma²) cancela com a² de (v/a)²: um sobe, o outro desce; o ½ some e ⅖ vira ⅕; v² e m ficam
        self.gmap(k3, ([0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 3, 4, 5, 6, 7, 8]),
                  ([9, 10, 11], [], {"shift": UP * 0.3}), ([13, 14, 15], [9, 10, 11], {"delay": 0.2}),
                  ([16], [12]), ([21], [13]), ([25], [14], {"path_arc": -PI / 3}),
                  ([17, 18], [], {"shift": UP * 0.4}), ([23], [], {"shift": DOWN * 0.4}),
                  ([12, 19, 20, 22, 24], []),
                  extra=self.note_anims(tex(r"\tfrac12\cdot\tfrac25=\tfrac15", 32)), run_time=1.4)
        self.wait(READ)
        self.show_expr(boxed(mtex("K", "=", r"\tfrac{7}{10}", "mv^2", size=54)),
                       *self.note_anims(tex(r"\tfrac12+\tfrac15=\tfrac{7}{10}", 32)))
        self.check_safe()
        self.wait(READ_RES)

    # C7 — barra + gráfico de energia acompanhando a esfera (rampa -> fundo -> subida)
    def c7_barras(self):
        self.mark("C7")
        self.note_y = -4.3
        s0, s1 = s_start(H_PART), 2.1
        H_, b_ = H_PART, BETA
        gp = lambda p, v: np.array([GX0 + GW * p, GY0 + GH * v / H_REF, 0.0])
        ss = np.linspace(s0, s1, 240)
        pp = (ss - s0) / (s1 - s0)
        U = ys(ss)
        K = H_ - U

        def curve(vals, col):
            return VMobject().set_points_as_corners([gp(p, v) for p, v in zip(pp, vals)]).set_stroke(col, 3.5)

        pb = (0.0 - s0) / (s1 - s0)
        graph = VGroup(
            VGroup(Line(gp(0, 0), gp(1.02, 0)), Line(gp(0, 0), gp(0, 2.78))).set_stroke(WHITE, 2, 0.8),
            DashedLine(gp(0, H_), gp(1, H_), dash_length=0.1).set_stroke(WHITE, 2, 0.85),
            DashedLine(gp(pb, 0), gp(pb, 2.7), dash_length=0.08).set_stroke(WHITE, 1.5, 0.35),
            tag("FUNDO", 14, opacity=0.7).move_to(gp(pb, 0) + [0, -0.2, 0]),
            tag("PROGRESSO NO TRAJETO", 14, opacity=0.7).move_to(gp(0.3, 0) + [0, -0.45, 0]),
            tex("E", 26).move_to(gp(0, 2.78) + [-0.25, 0.0, 0]),
            tex(r"E_{\rm total}=mgh", 24).move_to(gp(0.78, H_) + [0, 0.2, 0]),
            curve(U, VIOLET), curve(K / (1 + b_), CYAN), curve(K * b_ / (1 + b_), MAGENTA))

        def cursor():
            s = self.cs()
            p = float(np.clip((s - s0) / (s1 - s0), 0, 1))
            u = float(ys(s)[0])
            k = max(self.H.get_value() - u, 0.0)
            bb = self.b.get_value()
            return VGroup(Line(gp(p, 0), gp(p, 2.7)).set_stroke(WHITE, 2, 0.6),
                          Dot(gp(p, u), 0.07, color=VIOLET), Dot(gp(p, k / (1 + bb)), 0.07, color=CYAN),
                          Dot(gp(p, k * bb / (1 + bb)), 0.07, color=MAGENTA))

        cur = always_redraw(cursor)
        self.graph = VGroup(graph, cur)
        self.clear_text(*self.caption("PARA ONDE VAI A ENERGIA?"), run_time=0.5)
        self.hmk.update()
        self.bar.update()
        self.play(FadeIn(self.hmk), FadeIn(self.bar), FadeIn(self.bargroup), *self.set_hval(r"h=2{,}5R"),
                  FadeIn(graph), FadeIn(cur), *self.note_anims(tag("DESCE: U VIRA K. SOBE: K VIRA U")), run_time=0.8)
        self.wait(BEAT)
        self.play(self.go(s1))
        self.note(mtex(r"K_{\rm trans}", ":", r"K_{\rm rot}", "=", "5", ":", "2", size=38))
        self.hint[0].set_color(CYAN), self.hint[2].set_color(MAGENTA)
        self.check_safe()
        self.wait(READ_RES)

    # C8 — altura mínima da esfera: 2,7R; a linha, o rótulo, a esfera e a energia inicial sobem juntos
    def c8_limite(self):
        self.mark("C8")
        self.note_y = -3.75
        ref25 = VGroup(DashedLine([-3.0, YB + RS * H_PART, 0], [XG, YB + RS * H_PART, 0], dash_length=0.12)
                       .set_stroke(VIOLET, 2, 0.35),
                       tex(r"2{,}5R", 26, VIOLET).set_opacity(0.5).move_to([2.2, YB + RS * H_PART - 0.25, 0]))
        x25 = BAR_X0 + BAR_W * H_PART / H_REF
        ghost = Line([x25, BAR_Y - 0.28, 0], [x25, BAR_Y + 0.28, 0]).set_stroke(WHITE, 3, 0.85)
        delta = tex(r"+0{,}2\,mgR", 26, VIOLET).move_to([2.7, BAR_Y + 0.42, 0])
        self.clear_text(self.bo.animate.set_value(0), *self.caption("ESFERA: ALTURA MÍNIMA"), FadeOut(self.graph),
                        run_time=0.5)
        self.put(H=H_PART)
        self.play(self.bo.animate.set_value(1), run_time=0.4)
        a = mtex("mgh", "=", "mg(2R)", "+", r"\tfrac{7}{10}", r"mv_{\rm topo}^2", size=42)
        self.step(a, row(text("NO TOPO:", 20), tex("y=2R", 30), text("E", 20), tex("v^2=gR", 30)),
                  match=False, hold=0.7)
        c = mtex("mgh", "=", "2mgR", "+", r"\tfrac{7}{10}", "m(gR)", size=42)
        c[5].set_color(CYAN)
        self.step(c, hold=0.7)
        self.step(mtex("mgh", "=", "2mgR", "+", r"\tfrac{7}{10}", "mgR", size=42), hold=0.5)
        self.step(mtex("mgh", "=", r"\tfrac{27}{10}", "mgR", size=42), tex(r"2+\tfrac{7}{10}=\tfrac{27}{10}", 32),
                  hold=0.5)
        self.step(mtex("h", "=", r"\tfrac{27}{10}", "R", r"=", r"2{,}7R"), CLEAR, hold=0.4)
        self.show_expr(boxed(mtex(r"h_{\min}", "=", r"2{,}7R", size=54)),
                       *self.note_anims(tag("ROLAMENTO IDEAL SEM DESLIZAMENTO", 22)))
        self.wait(BEAT)
        up = tex(r"2{,}5R\;\to\;2{,}7R", 32, VIOLET)
        up.add_updater(lambda m: m.move_to([1.3, YB + RS * self.H.get_value() + 0.3, 0]))
        up.update()
        self.play(FadeIn(ref25), FadeIn(ghost), run_time=0.4)
        self.play(FadeOut(self.hval), FadeIn(up), self.H.animate.set_value(H_IDEAL),
                  *self.note_anims(tag("MAIS ENERGIA INICIAL: A ESFERA PARTE MAIS ALTO", 22)), run_time=2.0)
        self.hval = None
        self.play(FadeOut(up), *self.set_hval(r"h=2{,}7R"), FadeIn(delta), run_time=0.5)
        self.check_safe()
        self.wait(READ)
        self.ref25, self.ghost, self.delta = ref25, ghost, delta

    # C9 — payoff: a esfera parte de 2,7R e completa o loop
    def c9_payoff(self):
        self.mark("C9")
        self.clear_text(*self.caption("AGORA, DE 2,7R"), FadeOut(self.ghost), FadeOut(self.delta), run_time=0.5)
        self.add(self.forc)
        self.wait(BEAT)
        self.play(self.go(S_END))
        done = tag("COMPLETA O LOOP", 26, CYAN).move_to([0, -2.6, 0])
        self.play(FadeIn(done), run_time=0.4)
        self.check_safe()
        self.wait(READ)
        self.play(FadeOut(done), run_time=0.3)

    # C10 — síntese sobre a pista: a esfera volta a percorrer o loop enquanto os resultados aparecem
    def c10_sintese(self):
        self.mark("C10")
        Y25, Y27 = YB + RS * H_PART, YB + RS * H_IDEAL
        l25 = tag("PARTÍCULA · 2,5R", 18).move_to([1.7, Y25 - 0.25, 0])
        l27 = tag("ESFERA · 2,7R", 18, VIOLET).move_to([1.7, Y27 + 0.25, 0])

        def item(label, s, y):
            return row(label, boxed(tex(s, 44)), buff=0.45).move_to([0, y, 0])

        self.play(FadeOut(self.bar), FadeOut(self.bargroup), FadeOut(self.forc), FadeOut(self.hval),
                  FadeOut(self.ref25[1]), FadeIn(l25), FadeIn(l27), self.tk.animate.set_value(0.45),
                  self.bo.animate.set_value(0), *self.caption("O QUE O LOOP ENSINA"), run_time=0.7)
        self.put(H=H_IDEAL)
        rows = VGroup(item(tag("PARTÍCULA", 22, opacity=0.9), r"h_{\min}=2{,}5R", -0.45),
                      item(tag("ESFERA MACIÇA", 22, VIOLET), r"h_{\min}=2{,}7R", -1.45))
        ideas = VGroup(tag("MESMA VELOCIDADE MÍNIMA NO TOPO", 24),
                       tag("+ ENERGIA TAMBÉM NA ROTAÇÃO", 24, MAGENTA),
                       tag("MAIOR ALTURA INICIAL", 30, VIOLET)).arrange(DOWN, buff=0.35).move_to([0, -3.1, 0])
        texts = [FadeIn(rows[0], shift=UP * 0.1), Wait(0.4), FadeIn(rows[1], shift=UP * 0.1), Wait(0.5)]
        for i in ideas:
            texts += [FadeIn(i, shift=UP * 0.1), Wait(0.4)]
        run = Succession(self.bo.animate(run_time=0.3).set_value(1).build(), self.go(S_END).build())
        self.play(AnimationGroup(run, Succession(*texts)))
        self.check_safe()
        self.wait(READ)
