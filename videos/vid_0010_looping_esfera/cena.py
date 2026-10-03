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

A derivação de I_CM é uma sub-rotina da solução principal (a energia da esfera pede I_CM).
"""

import json
import os
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import (
    ORIGIN, DOWN, LEFT, PI, RIGHT, UP, AnimationGroup, Arc, Arrow, Circle, Create, DashedLine,
    DashedVMobject, Dot, Ellipse, FadeIn, FadeOut, ImageMobject, Indicate, LaggedStart, Line,
    Polygon, Succession, TransformFromCopy, Wait,
    ManimColor, MathTex, Rectangle, Scene, SurroundingRectangle, TransformMatchingTex,
    VGroup, VMobject, ValueTracker, always_redraw, config, interpolate_color, linear,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from MF_Tools import TransformByGlyphMap
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text


PASTA = Path(__file__).resolve().parent
CAL = os.environ.get("SYNC_CAL") == "1"        # calibragem: mede o tempo NATIVO de cada âncora

# ── Paleta ──────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # velocidade e translação
BLUE = "#267BFF"          # pista, geometria e N
BLUE_L = "#7FB2FF"        # trajetória do CM (tracejada), R e x
VIOLET = SECONDARY_COLOR  # energia potencial e altura h
MAGENTA = "#EA63FF"       # rotação
SPHERE_FILL = "#1A2142"

# Cores dos termos na legenda queimada (montar_legendado.py --color-module); mesmos significados da cena
SUBTITLE_TERM_COLORS = {
    "velocidade": CYAN, "translação": CYAN,
    "rotação": MAGENTA, "momento de inércia": MAGENTA, "velocidade angular": MAGENTA,
    "altura": VIOLET, "potencial": VIOLET,
    "normal": BLUE_L,
}

SAFE_BOTTOM = -4.6        # abaixo disso: faixa reservada a legendas
SAFE_X = 3.5
HEADLINE_TOP = 6.85

BEAT, READ, READ_RES = 0.4, 1.5, 2.0
K_T = 0.85                # segundos de tela por unidade de tempo físico sqrt(R/g)
CLEAR = object()          # note(CLEAR): apaga a nota sem trocar por outra
RT_K, HOLD_K = 0.8, 0.6   # escala de tempo e de pausa das transformações de glifos (mm)

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
SM = 2.4                  # replay: o corpo sobe até aqui (~137°, antes do topo) e reinicia
RP_GAP = 0.6              # intervalo invisível entre dois ciclos do replay
S_MIN = s_start(3.0)


def _qa():
    assert SM < PI and SM < TH_FAIL                                  # o replay nunca chega ao topo
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


def roll(tr, H, b, s1, span=None, k=1.0):
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

    return tr.animate(rate_func=rate, run_time=K_T * S * k).set_value(s1)


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


# ── Equações com índices de glifos (MF-Tools) ───────────────────────────────
AUX_S, AUX_Y = 0.6, -3.95     # relação-fonte (v_top² = gR) em tamanho reduzido


class Eq:
    """MathTex de string única + índices de glifos por parte, para TransformByGlyphMap.

    As partes só servem para contar glifos (a string final é a junção delas): `p(i, j, ...)` devolve os
    índices dos glifos das partes i, j, ...; `frac(i)` separa numerador / barra / denominador de uma
    fração por geometria (numerador e denominador em ordem da esquerda para a direita)."""

    def __init__(self, *parts, size=44, colors=None):
        multi = MathTex(*parts, font_size=size)
        self.s = np.concatenate([[0], np.cumsum([len(q) for q in multi])]).astype(int)
        self.mob = MathTex(" ".join(parts), font_size=size, color=WHITE)
        assert len(self.mob[0]) == int(self.s[-1]), parts
        for i, c in (colors or {}).items():
            self.mob[0][int(self.s[i]):int(self.s[i + 1])].set_color(c)

    def p(self, *ids):
        return [k for i in ids for k in range(int(self.s[i]), int(self.s[i + 1]))]

    def g(self, *ids):
        return [self.mob[0][k] for k in self.p(*ids)]

    def px(self, i):
        return sorted(self.p(i), key=lambda k: self.mob[0][k].get_center()[0])

    def tall(self, i):
        return max(self.p(i), key=lambda k: self.mob[0][k].height)

    def frac(self, i):
        idx = self.p(i)
        c = {k: self.mob[0][k].get_center() for k in idx}
        bar = max(idx, key=lambda k: self.mob[0][k].width)
        num = sorted((k for k in idx if k != bar and c[k][1] > c[bar][1]), key=lambda k: c[k][0])
        den = sorted((k for k in idx if k != bar and c[k][1] < c[bar][1]), key=lambda k: c[k][0])
        return num, bar, den

    def center(self, k):
        return self.mob[0][k].get_center()


def copy_from(src):
    """Introdutor para TransformByGlyphMap: o destino nasce de uma CÓPIA dos glifos `src`, que ficam onde estão."""
    class _Copy(TransformFromCopy):
        def __init__(self, mob, **kw):
            super().__init__(VGroup(*src), mob, **kw)
    return _Copy


def M(A, pa, B, pb, **kw):
    """Partes pa de A viram partes pb de B."""
    return (A.p(*pa), B.p(*pb), kw)


def X(A, pa, **kw):
    """Partes pa de A saem (fade, com `shift`)."""
    return (A.p(*pa), [], kw)


def C(src, B, pb, **kw):
    """Partes pb de B nascem de uma cópia dos glifos `src` (um pouco depois da saída do termo antigo)."""
    kw.setdefault("delay", 0.2)
    return (copy_from(src), B.p(*pb), kw)


FS = 0.4                  # comprimento da seta por mg (sem zoom)
VS = 0.55                 # comprimento da seta de v por sqrt(gR) (sem zoom)
BAR_X0, BAR_W, BAR_H, BAR_Y, H_REF = -2.7, 5.4, 0.30, -0.5, 2.7
GX0, GY0, GW, GH = -2.5, -3.3, 5.6, 1.65     # gráfico cartesiano de energia (origem e tamanho)


class LoopingEsfera010(Scene):
    op_y = -2.50
    note_y = -3.75

    # ── Infraestrutura de quadro ────────────────────────────────────────────
    def mark(self, name):
        pass

    # ── Sincronia com a narração ────────────────────────────────────────────
    # Cada self.ancora("x") casa um ponto do código com um instante da fala (sync.json). Entre duas
    # âncoras, play/wait são escalados para o trecho durar o que a fala dura; se a cena acabar antes, a
    # âncora seguinte segura o último quadro. native.json guarda o tempo NATIVO de cada âncora
    # (SYNC_CAL=1 regenera; sem os dois arquivos a cena roda em tempo nativo).
    def sync_init(self):
        self.tscale, self.nativos = 1.0, {}
        arq = PASTA / "sync.json"
        dados = json.load(open(arq)) if arq.exists() else {}
        self.anc, self.extras = dados.get("anchors", []), dados.get("extras", {})
        nat = PASTA / "native.json"
        self.nat = json.load(open(nat)) if nat.exists() and not CAL else {}

    def _quadro(self, t):
        """Duração em quadros inteiros (o Manim arredonda para cima)."""
        fps = config.frame_rate
        return max(1, round(t * fps)) / fps

    def play(self, *args, **kwargs):
        if abs(self.tscale - 1.0) > 1e-6 and args and not getattr(self, "_cru", False):
            anims = self.compile_animations(*args, **kwargs)
            for a in anims:
                a.run_time = self._quadro(a.run_time * self.tscale)
            return super().play(*anims)
        return super().play(*args, **kwargs)

    def esperar_cru(self, duracao):
        """Espera SEM escala: Scene.wait chama self.play, que escalaria de novo."""
        self._cru = True
        try:
            Scene.wait(self, duracao)
        finally:
            self._cru = False

    def wait(self, duration=1.0, *a, **k):
        self.esperar_cru(self._quadro(duration * self.tscale))

    def ancora(self, nome):
        agora = self.renderer.time
        if CAL:
            self.nativos[nome] = round(agora, 3)
            if nome == "fim":
                json.dump(self.nativos, open(PASTA / "native.json", "w"), indent=1)
            return
        if not self.anc or nome not in self.nat:
            return
        nomes = [n for n, _ in self.anc]
        i = nomes.index(nome)
        t_a = self.anc[i][1]
        if agora < t_a:
            self.esperar_cru(t_a - agora)
            agora = t_a
        elif agora - t_a > 0.25:
            print("SYNC atraso %.2f s em %s" % (agora - t_a, nome))
        if i + 1 < len(self.anc):
            prox, t_prox = self.anc[i + 1]
            gap_nat = max(0.2, self.nat[prox] - self.nat[nome])
            self.tscale = float(np.clip((t_prox - agora) / gap_nat * 0.985, 0.45, 2.0))
        else:
            self.tscale = 1.0

    def _a(self, anc, chave):
        if anc and anc.get(chave):
            self.ancora(anc[chave])

    def caption(self, *lines):
        new = VGroup(*(line if isinstance(line, VMobject) else display(line) for line in lines)).arrange(DOWN, buff=0.14)
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
        self.wait(hold + 0.2)

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

    def mm(self, old, new, *moves, y, sc=1.0, box=False, cur=True, extra=(), note=None, run_time=1.1, hold=0.35):
        """Transforma a expressão `old` (Eq) em `new` (Eq) com TransformByGlyphMap.

        `moves` vêm de M/X/C (ou tuplas (idx_A, idx_B, kw)); o que não for citado sai/entra por fade.
        old=None: `new` entra por FadeIn. box: a moldura só entra DEPOIS da transformação."""
        run_time, hold = run_time * RT_K, hold * HOLD_K          # ritmo das transformações (ajuste global)
        new.mob.scale(sc)
        fit(new.mob).move_to([0, y, 0])
        anims = [*extra, *(self.note_anims(note) if note is not None else [])]
        if old is None:
            self.play(FadeIn(new.mob, shift=UP * 0.1), *anims, run_time=run_time)
        else:
            self.play(TransformByGlyphMap(old.mob, new.mob, *moves, auto_fade=True), *anims, run_time=run_time)
            self.remove(old.mob)
        out = new.mob
        if box:
            out = boxed(new.mob)
            self.play(FadeIn(out[1]), run_time=0.3)
            self.add(out)
        if cur:
            self.expr = out
        if hold:
            self.wait(hold)
        return new

    def hchain(self, coef, mid, res, final, note_end, anc=None):
        """mgh = mg(2R) + K_topo  ->  h_min: v_top² vira gR (cópia da relação-fonte), mg cancela, os termos em R
        se juntam e os coeficientes somam (mid = 2 escrito como fração de mesmo denominador)."""
        y = self.op_y
        gR = self.vt.g(2, 3)
        kw = dict(size=42)
        A0 = Eq("m", "g", "h", "=", "m", "g", "(", "2", "R", ")", "+", coef, "m", r"v_{\rm top}^2",
                colors={13: CYAN}, **kw)
        self._a(anc, "A0")
        self.mm(None, A0, y=y, note=tex("y=2R", 32), hold=0.3)
        self._a(anc, "ind")
        self.play(Indicate(VGroup(*A0.g(13)), color=CYAN, scale_factor=1.25), run_time=0.7)
        A1 = Eq("m", "g", "h", "=", "m", "g", "(", "2", "R", ")", "+", coef, "m", "g", "R",
                colors={13: CYAN, 14: CYAN}, **kw)
        self._a(anc, "A1")
        self.mm(A0, A1, M(A0, range(13), A1, range(13)), X(A0, [13], shift=DOWN * 0.3),
                C(gR, A1, [13, 14], path_arc=-PI / 3), y=y, run_time=1.3)
        A2 = Eq("m", "g", "h", "=", "2", "m", "g", "R", "+", coef, "m", "g", "R", colors={11: CYAN, 12: CYAN}, **kw)
        self.mm(A1, A2, M(A1, [0, 1, 2, 3], A2, [0, 1, 2, 3]), M(A1, [7], A2, [4], path_arc=-PI / 2),
                M(A1, [4, 5], A2, [5, 6]), M(A1, [8], A2, [7]), X(A1, [6, 9]),
                M(A1, [10, 11, 12, 13, 14], A2, [8, 9, 10, 11, 12]), y=y, run_time=1.1, hold=0.1)
        self._a(anc, "A2")
        self.play(*(Indicate(VGroup(*A2.g(*ids)), color=WHITE, scale_factor=1.2) for ids in ([0, 1], [5, 6], [10, 11])),
                  *self.note_anims(tex(r"\div\, mg", 34)), run_time=0.8)
        A3 = Eq("h", "=", "2", "R", "+", coef, "R", colors={6: CYAN}, **kw)
        self.mm(A2, A3, M(A2, [2], A3, [0]), M(A2, [3], A3, [1]), M(A2, [4], A3, [2]), M(A2, [7], A3, [3]),
                M(A2, [8], A3, [4]), M(A2, [9], A3, [5]), M(A2, [12], A3, [6]),
                X(A2, [0, 1], shift=UP * 0.4), X(A2, [5, 6], shift=DOWN * 0.4), X(A2, [10, 11], shift=UP * 0.4),
                y=y, run_time=1.3)
        A4 = Eq("h", "=", "(", "2", "+", coef, ")", "R", **kw)
        self._a(anc, "A4")
        self.mm(A3, A4, M(A3, [0], A4, [0]), M(A3, [1], A4, [1]), M(A3, [2], A4, [3]), M(A3, [4], A4, [4]),
                M(A3, [5], A4, [5]), M(A3, [3], A4, [7], path_arc=-PI / 2), X(A3, [6], shift=LEFT * 0.2),
                y=y, run_time=1.2)
        A5 = Eq("h", "=", "(", mid, "+", coef, ")", "R", **kw)
        n5, b5, d5 = A5.frac(3)
        self.mm(A4, A5, M(A4, [0, 1, 2, 4, 5, 6, 7], A5, [0, 1, 2, 4, 5, 6, 7]), (A4.p(3), [n5[0]], {}),
                ([], [b5, *d5, *n5[1:]], {"delay": 0.3}), y=y, run_time=1.1, note=tex(rf"2={mid}", 34))
        A6 = Eq("h", "=", res, "R", **kw)
        n6, b6, d6 = A6.frac(2)
        nm, bm, dmm = A5.frac(3)
        nc, bc, dc = A5.frac(5)
        moves = [M(A5, [0, 1], A6, [0, 1]), M(A5, [7], A6, [3]), (dmm, d6, {}), ([bm], [b6], {}),
                 ([bc], [], {"shift": DOWN * 0.3}), (dc, [], {"shift": DOWN * 0.3}), X(A5, [2, 4, 6])]
        if len(nm) == 1:                     # 4/2 + 1/2 = 5/2
            moves += [([nm[0]], [n6[0]], {}), (nc, [], {"shift": UP * 0.4})]
        else:                                # 20/10 + 7/10 = 27/10
            moves += [([nm[0]], [n6[0]], {}), ([nm[1]], [], {"shift": UP * 0.4}),
                      ([nc[0]], [n6[1]], {"path_arc": -PI / 3})]
        self._a(anc, "A6")
        self.mm(A5, A6, *moves, y=y, run_time=1.4, note=tex(rf"{mid}+{coef}={res}", 32))
        A7 = Eq(r"h_{\min}", "=", res, "R", "=", final, **kw)
        self._a(anc, "A7")
        self.mm(A6, A7, (A6.p(0), [A7.p(0)[0]], {}), M(A6, [1], A7, [1]), M(A6, [2], A7, [2]), M(A6, [3], A7, [3]),
                y=y, box=True, run_time=1.0, note=note_end, hold=1.0)
        return A7

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

    def go(self, s1, span=None, k=1.0):
        """Solta o corpo do início e anima s até s1."""
        if self.rest.get_value() > 0.5:
            self.S.set_value(s_start(self.H.get_value()))
            self.rest.set_value(0.0)
        return roll(self.S, self.H.get_value(), self.b.get_value(), s1, span, k)

    # ── Replay: o corpo repete a descida e a subida enquanto a conta está aberta ───────────────
    def drive(self, m, dt):
        """Primeiro updater da cena: zoom global + passo do replay (posição e giro saem do MESMO s)."""
        ZS.update(z=self.zm.get_value())
        if self.rep.get_value() < 0.5 or self.rp is None:
            return
        self.rt += dt
        t, g, T = self.rp["t"], self.rp["g"], self.rp["T"]
        u = self.rt % (T + RP_GAP)
        if u < T:
            s = float(np.interp(u, t, g))
            op = min(1.0, u / 0.3, (T - u) / 0.45)       # entra e sai por fade: o reset não parece colisão
        else:
            s, op = float(g[0]), 0.0
        self.rest.set_value(0.0)
        self.S.set_value(s)
        self.rpo.set_value(op * 0.85 * self.rpk.get_value())

    def replay_on(self, H, b, fresh=False):
        """Liga o replay (sem reversão física: desce, sobe até SM, some, reaparece na rampa)."""
        self.put(H=H, b=b)
        s0 = s_start(H)
        g = np.linspace(s0, SM, 1500)
        mid = (g[1:] + g[:-1]) / 2
        v = np.sqrt(np.maximum(v2(ys(mid), H, b), 1e-6))
        t = np.concatenate([[0.0], np.cumsum(np.diff(g) / v)]) * K_T
        self.rp = {"t": t, "g": g, "T": float(t[-1])}
        self.rt = 0.0 if fresh else 0.3                  # com o corpo já visível, começa no ponto de plena opacidade
        self.rpk.set_value(1.0)
        self.rep.set_value(1.0)
        self.bo.set_value(1.0)
        if self.bod not in self.mobjects:
            self.add(self.bod)

    def replay_off(self, *extra, run_time=0.4):
        """Desliga o replay: fade do corpo e, depois, estado limpo (o chamador reposiciona com put)."""
        self.play(self.rpk.animate.set_value(0.0), *extra, run_time=run_time)
        self.rep.set_value(0.0)
        self.rpo.set_value(1.0)
        self.rpk.set_value(1.0)
        self.bo.set_value(0.0)

    def build(self):
        self.S, self.H, self.b, self.av, self.fl, self.rest, self.bo, self.zm, self.tk = (
            ValueTracker(v) for v in (0.0, H_PART, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0))
        self.spin = ValueTracker(0.0)      # giro contínuo do disco extraído (bloco de I_CM)
        self.spin.add_updater(lambda m, dt: m.increment_value(2.4 * dt))
        # o zoom global é atualizado antes de todo always_redraw (este objeto é o primeiro da cena)
        self.rep, self.rpo, self.rpk = ValueTracker(0.0), ValueTracker(1.0), ValueTracker(1.0)
        self.rp, self.rt = None, 0.0
        self.zdrv = VMobject()
        self.zdrv.add_updater(self.drive)
        self.add(self.zdrv)
        st = lambda: (self.cs(), self.H.get_value(), self.b.get_value(), self.av.get_value())
        vz = lambda: 1 + zf()

        self.trk = always_redraw(lambda: track_mob(max(self.av.get_value(), R_PART), self.tk.get_value()))
        self.cmp = always_redraw(lambda: DashedVMobject(Circle(kk()).move_to(scr(0, 1)), num_dashes=72)
                                 .set_stroke(BLUE_L, 2, 0.5))
        self.bod = always_redraw(lambda: body(self.cs(), self.av.get_value(), self.bo.get_value() * self.rpo.get_value(),
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
            if self.rep.get_value() > 0.5:                     # no replay não há diagrama de forças
                return g
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
        self.legend = legend
        self.bartitle = tag("ENERGIA", 18, opacity=0.75).move_to([0, BAR_Y + 0.42, 0])
        self.bargroup = VGroup(legend, self.bartitle)
        self.vt = Eq(r"v_{\rm top}^2", "=", "g", "R", size=54)      # relação-fonte do topo (partícula e esfera)
        self.vbox = boxed(self.vt.mob)

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
        self.sync_init()

        self.c1_pergunta()
        self.c1b_caso()
        self.c2_topo()
        self.c3_particula()
        self.c4_esfera()
        self.c4b_energia()
        self.c5_inercia()
        self.c6_energia()
        self.c7_barras()
        self.c8_limite()
        self.c9_payoff()
        self.c10_sintese()
        self.ancora("fim")

    # A — a pergunta: altura mínima para a ESFERA completar o loop (h desconhecida)
    def c1_pergunta(self):
        self.put(H=H_PART, b=BETA, av=A_R)
        self.add(self.bod)                              # invisível (bo = 0) até entrar
        self.ancora("a00")
        self.play(FadeIn(self.series), *self.caption("QUAL A ALTURA MÍNIMA PARA", "A ESFERA COMPLETAR O LOOP?"),
                  run_time=0.8)
        self.show(self.trk, self.hmk, self.cmp)
        self.play(*self.set_hval(r"h=\,?"), self.bo.animate.set_value(1), run_time=0.6)
        self.check_safe()
        self.wait(READ + 0.3)

    # B — o caso-base: a partícula no lugar da esfera, na mesma pista
    def c1b_caso(self):
        self.ancora("a01")
        self.play(*self.caption("PRIMEIRO: O CASO CLÁSSICO"), self.av.animate.set_value(0),
                  self.b.animate.set_value(0), run_time=1.2)
        self.replay_on(H_PART, 0.0)
        self.wait(READ + 0.5)

    # C2 — condição de contato no topo (partícula), com zoom no loop
    def c2_topo(self):
        self.mark("C2")
        self.ancora("a02")
        self.replay_off(FadeOut(self.hmk), *self.set_hval(None))
        self.put(H=2.9, b=0.0, av=0.0, s=PI)
        self.play(*self.caption("O QUE PRECISA ACONTECER NO TOPO?"), self.bo.animate.set_value(1), run_time=0.6)
        self.play(self.zoom(Z_MAX, 1.3), run_time=1.3)
        self.show(self.rline, self.rlab, self.forc, self.varr)
        self.ancora("a03")
        self.show_expr(mtex("mg", "+", "N", "=", r"\frac{mv^2}{R}"))
        self.expr[2].set_color(BLUE)
        self.ancora("a04")
        self.note(tex(r"N\geq0", 40, BLUE))
        self.wait(BEAT + 0.5)
        self.note(CLEAR, FadeOut(self.rline), FadeOut(self.rlab))
        self.play(self.H.animate.set_value(H_PART), run_time=1.8)
        self.ancora("a05")
        self.show_expr(mtex("mg", "+", "0", "=", r"\frac{mv^2}{R}"))
        self.note(tex("N=0", 40, BLUE))
        self.wait(0.3)
        self.ancora("a06")
        self.show_expr(self.vbox)
        self.check_safe()
        self.wait(READ_RES)

    # C3 — resultado clássico 2,5R
    def c3_particula(self):
        self.mark("C3")
        self.ancora("a07")
        self.note_y = -3.2
        top = YB + 2 * RS
        self.cota2R = VGroup(span_mark([2.55, YB, 0], [2.55, top, 0], VIOLET),
                             tex("2R", 32, VIOLET).move_to([2.82, YB + RS, 0]))
        vb = self.vbox
        self.expr = None
        # v_top² = gR (do bloco anterior) vira a relação-fonte, menor, e fica embaixo
        self.clear_text(*self.caption("ALTURA MÍNIMA DA PARTÍCULA"), self.zoom(1, 1.1),
                        FadeOut(self.forc), FadeOut(self.varr), self.bo.animate.set_value(0),
                        vb.animate.scale(AUX_S).move_to([0, AUX_Y, 0]), run_time=1.1)
        self.hmk.update()
        self.play(FadeIn(self.hmk), FadeIn(self.cota2R), *self.set_hval(r"h=\,?"), run_time=0.6)
        self.put(H=H_PART, b=0.0, av=0.0)
        self.replay_on(H_PART, 0.0, fresh=True)
        self.hchain(r"\tfrac12", r"\tfrac42", r"\tfrac52", "2{,}5R", tag("PARTÍCULA"),
                    anc=dict(A0="a08", ind="a09", A1="a10", A2="a10b", A4="a11", A7="a12"))
        self.ancora("a12b")
        self.replay_off(*self.set_hval(r"h=2{,}5R"))
        self.put(H=H_PART, b=0.0, av=0.0)                 # corrida conclusiva: parte da altura obtida
        self.play(self.bo.animate.set_value(1), run_time=0.3)
        self.play(self.go(S_END, k=0.62))
        self.check_safe()
        self.wait(0.2)

    # C4 — a partícula vira esfera; a condição no topo não muda (zoom)
    def c4_esfera(self):
        self.mark("C4")
        self.ancora("a14")
        self.clear_text(*self.caption("AGORA, A ESFERA"), FadeOut(self.hmk), *self.set_hval(None), FadeOut(self.cota2R),
                        self.bo.animate.set_value(0))
        self.put(H=H_PART, b=0.0, av=0.0, s=PI)
        # v_topo² = 2(H - 2)/(1 + beta): H e beta lineares juntos mantêm v_topo² = gR durante a troca
        self.play(self.zoom(Z_MAX, 1.2), self.bo.animate.set_value(1), self.av.animate.set_value(A_R),
                  self.b.animate.set_value(BETA), self.H.animate.set_value(H_IDEAL), run_time=1.2)
        self.show(self.varr, self.forc, *self.esf)
        self.ancora("a15")
        self.note(tag("A CONDIÇÃO NO TOPO MUDA?"))
        self.wait(READ)
        self.ancora("a16")
        self.show_expr(mtex("mg", "+", "N", "=", r"\frac{mv^2}{R}"))
        self.expr[2].set_color(BLUE)
        self.wait(BEAT)
        vb = self.vbox
        self.play(FadeOut(self.expr), vb.animate.scale(1 / AUX_S).move_to([0, self.op_y, 0]),
                  *self.note_anims(tag("MESMA CONDIÇÃO NO TOPO")), run_time=1.1)
        self.expr = vb
        self.check_safe()
        self.wait(READ_RES)

    # F — a energia da esfera pede uma peça nova: I_CM (a equação fica em aberto)
    def c4b_energia(self):
        self.mark("C4b")
        self.ancora("a17")
        self.note_y = -3.2
        y = self.op_y
        self.clear_text(*self.caption("O QUE MUDA NA ENERGIA?"), self.zoom(1, 1.0),
                        FadeOut(self.forc), FadeOut(self.varr), *(FadeOut(m) for m in self.esf),
                        self.bo.animate.set_value(0), run_time=1.0)
        self.replay_on(H_PART, BETA, fresh=True)
        cy, mg_ = CYAN, MAGENTA
        Ka = Eq("K", "=", r"K_{\rm trans}", "+", r"K_{\rm rot}", colors={2: cy, 4: mg_})
        E0 = Eq("K", "=", r"\tfrac12", "m", "v^2", "+", r"\tfrac12", "I_{CM}", r"\omega^2",
                colors={2: cy, 3: cy, 4: cy, 6: mg_, 7: mg_, 8: mg_})
        self.mm(None, Ka, y=y, hold=0.5)
        self.ancora("a18")
        self.mm(Ka, E0, M(Ka, [0, 1], E0, [0, 1]), (Ka.p(2), E0.p(2, 3, 4), {}), M(Ka, [3], E0, [5]),
                (Ka.p(4), E0.p(6, 7, 8), {}), y=y, run_time=1.3, hold=0.4)
        self.ancora("a19")
        self.play(Indicate(VGroup(*E0.g(7)), color=MAGENTA, scale_factor=1.35),
                  *self.note_anims(tex(r"I_{CM}=\,?", 44, MAGENTA)), run_time=0.8)
        self.pend = E0                                   # a MESMA equação volta no fim do bloco de I_CM
        self.check_safe()
        self.wait(0.3)

    # C5 — I_CM por discos finos (bloco experimental, local e removível)
    def c5_inercia(self):
        self.mark("C5")
        self.ancora("a20")
        MAIN_Y, SRC_Y, AUX2_Y = -1.9, -0.95, -3.0
        self.op_y, self.note_y = MAIN_Y, -3.95
        self.replay_off()
        out = [self.trk, self.cmp, self.bod]
        pend = self.pend
        self.expr = None                                  # a equação pendente NÃO some: sobe, menor e mais fraca
        self.clear_text(*self.caption(row(display("QUAL É", 38), tex(r"I_{CM}", 44), display("DA ESFERA?", 38),
                                          buff=0.3)),
                        *(FadeOut(m) for m in out), pend.mob.animate.scale(0.7).move_to([0, 4.55, 0]).set_opacity(0.65),
                        run_time=0.9)

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
        # o MESMO disco, ampliado e visto de frente, girando em torno do próprio eixo
        phi = lambda: -self.spin.get_value()
        face = Circle(r0).move_to(Cd).set_stroke(MAGENTA, 3).set_fill(MAGENTA, 0.3)
        mag = VGroup(DashedLine(Cs + [x0, r0, 0], Cd + [0, r0, 0], dash_length=0.1),
                     DashedLine(Cs + [x0, -r0, 0], Cd + [0, -r0, 0], dash_length=0.1)).set_stroke(MAGENTA, 2, 0.5)
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
        self.play(*self.note_anims(row(text("DENSIDADE", 20), tex(r"\rho", 30))),
                  LaggedStart(*(FadeIn(d) for d in discs), lag_ratio=0.05), run_time=1.2)
        dim = [d.animate.set_stroke(BLUE_L, 2, 0.3) for i, d in enumerate(discs) if i != I0]
        self.ancora("a21")
        self.play(hl.animate.set_stroke(MAGENTA, 3, 1).set_fill(MAGENTA, 0.55), *dim, FadeIn(poly),
                  Create(x_leg), Create(r_leg), FadeIn(sq), FadeIn(x_lab), FadeIn(r_lab),
                  Create(dx_span), FadeIn(dx_lab),
                  run_time=1.3)
        self.play(TransformFromCopy(hl, face), Create(mag), FadeIn(spoke), FadeIn(rl), Create(warc_d),
                  FadeIn(dm_lab),
                  run_time=1.3)
        self.add(face)

        # triângulo a, x, r  ->  r² = a² - x²
        self.ancora("a22")
        p1 = mtex("a^2=x^2+r^2")                    # string única: o p1 -> p2 usa mapa de glifos
        p1[0][3:5].set_color(BLUE_L), p1[0][6:8].set_color(MAGENTA)
        self.step(p1, None, match=False, hold=0.8, rt=1.0,
                  extra=(Indicate(a_line, color=WHITE), Indicate(x_leg, color=BLUE_L),
                         Indicate(r_leg, color=MAGENTA)))
        p2 = mtex("r^2=a^2-x^2")
        p2[0][0:2].set_color(MAGENTA), p2[0][6:8].set_color(BLUE_L)
        # a² e x² passam por cima, r² por baixo (em linha reta se cruzariam sobre o =); o + sai e o − entra
        self.gmap(p2, ([0, 1], [3, 4], {"path_arc": -PI}), ([2], [2]),
                  ([3, 4], [6, 7], {"path_arc": -PI}), ([6, 7], [0, 1], {"path_arc": -PI * 0.75}),
                  ([5], []), ([], [5], {"delay": 0.7}), run_time=1.5)
        self.wait(0.4)
        # r² = a² − x² vira relação-fonte, menor, embaixo
        rel_r = p2
        self.expr = None
        self.play(rel_r.animate.scale(0.62).move_to([0, AUX2_Y, 0]).set_opacity(0.7), *self.note_anims(CLEAR), run_time=0.6)
        rr = [rel_r[0][k] for k in range(3, 8)]          # a² − x²

        # ── massa da fatia: dV, dm = ρ dV ──
        sdV = Eq("dV", "=", r"\pi", "r^2", "dx", size=42, colors={3: MAGENTA})
        sdV.mob.set_opacity(0.7)
        m1 = Eq("dm", "=", r"\rho", "dV", size=42)
        self.ancora("a23")
        self.mm(None, m1, y=MAIN_Y, hold=0.3)
        self.mm(None, sdV, y=SRC_Y, sc=0.85, cur=False, hold=0.2)
        self.ancora("a23b")
        m2 = Eq("dm", "=", r"\rho", "(", r"\pi", "r^2", "dx", ")", size=42, colors={5: MAGENTA})
        self.mm(m1, m2, M(m1, [0, 1, 2], m2, [0, 1, 2]), X(m1, [3], shift=UP * 0.3),
                C(sdV.g(2, 3, 4), m2, [4, 5, 6], path_arc=-PI / 4), y=MAIN_Y, run_time=1.0, hold=0.1)
        m3 = Eq("dm", "=", r"\rho", r"\pi", "r^2", "dx", size=42, colors={4: MAGENTA})
        self.mm(m2, m3, M(m2, [0, 1, 2, 4, 5, 6], m3, [0, 1, 2, 3, 4, 5]), X(m2, [3, 7]), y=MAIN_Y,
                run_time=0.8, hold=0.1)
        m4 = Eq("dm", "=", r"\rho", r"\pi", "(", "a^2", "-", "x^2", ")", "dx", size=42)
        self.mm(m3, m4, M(m3, [0, 1, 2, 3, 5], m4, [0, 1, 2, 3, 9]), X(m3, [4], shift=DOWN * 0.3),
                (copy_from(rr), m4.p(5, 6, 7), {"path_arc": -PI / 4}), y=MAIN_Y, run_time=1.1, hold=0.1)
        # a fatia (massa) vira a nova relação-fonte; a de volume sai
        self.play(m4.mob.animate.scale(0.85).move_to([0, SRC_Y, 0]).set_opacity(0.7), FadeOut(sdV.mob), *self.note_anims(CLEAR),
                  run_time=0.5)
        self.expr = None
        sdm = m4

        # ── momento da fatia: dI = ½ r² dm ──
        self.ancora("a24")
        d0 = Eq("dI", "=", r"\tfrac12", "r^2", "dm", size=42, colors={3: MAGENTA})
        self.mm(None, d0, y=MAIN_Y, hold=0.4)
        d1 = Eq("dI", "=", r"\tfrac12", "(", "a^2", "-", "x^2", ")", "dm", size=42)
        self.mm(d0, d1, M(d0, [0, 1, 2, 4], d1, [0, 1, 2, 8]), X(d0, [3], shift=UP * 0.3),
                (copy_from(rr), d1.p(4, 5, 6), {"path_arc": -PI / 4}), y=MAIN_Y, run_time=1.3, hold=0.2)
        d2 = Eq("dI", "=", r"\tfrac12", "(", "a^2", "-", "x^2", ")", r"\rho", r"\pi", "(", "a^2", "-", "x^2", ")", "dx",
                size=40)
        self.mm(d1, d2, M(d1, range(8), d2, range(8)), X(d1, [8], shift=UP * 0.3),
                C(sdm.g(2, 3, 4, 5, 6, 7, 8, 9), d2, range(8, 16), path_arc=-PI / 4),
                y=MAIN_Y, run_time=1.5, hold=0.3)
        # os dois fatores iguais se juntam: (a²−x²)(a²−x²) = (a²−x²)²
        self.ancora("a25")
        d3 = Eq("dI", "=", r"\frac{\rho\pi}{2}", "(a^2-x^2)^2", "dx", size=44)
        hn, hb, hd = d2.frac(2)
        n3, b3, dd3 = d3.frac(2)
        e3 = d3.p(3)
        self.mm(d2, d3, M(d2, [0, 1], d3, [0, 1]), (hd, dd3, {}), ([hb], [b3], {}),
                (hn, [], {"shift": UP * 0.4}), (d2.p(8), [n3[0]], {"path_arc": -PI / 3}),
                (d2.p(9), [n3[1]], {"path_arc": -PI / 3}),
                (d2.p(3, 4, 5, 6, 7), e3[:7], {}), (d2.p(10, 11, 12, 13, 14), [e3[7]], {"path_arc": -PI / 2}),
                M(d2, [15], d3, [4]), y=MAIN_Y, run_time=1.7, hold=0.4)
        # dI vira a nova relação-fonte
        self.play(d3.mob.animate.scale(0.85).move_to([0, SRC_Y, 0]).set_opacity(0.7), FadeOut(sdm.mob), FadeOut(rel_r),
                  run_time=0.7)
        self.expr = None
        sdI = d3

        # ── soma dos discos: I = ∫ dI ──
        self.ancora("a26")
        light = LaggedStart(*(d.animate.set_stroke(MAGENTA, 3, 1).set_fill(MAGENTA, 0.4) for d in discs),
                            lag_ratio=0.06)
        i1 = Eq("I", "=", r"\int", "dI", size=44)
        self.mm(None, i1, y=MAIN_Y, extra=[light], run_time=1.3, hold=0.3)
        self.ancora("a27")
        i2 = Eq("I", "=", r"\int_{-a}^{a}", r"\frac{\rho\pi}{2}", "(a^2-x^2)^2", "dx", size=42)
        self.mm(i1, i2, M(i1, [0, 1], i2, [0, 1]), ([i1.tall(2)], [i2.tall(2)], {}), X(i1, [3], shift=UP * 0.3),
                C(sdI.g(2, 3, 4), i2, [3, 4, 5], path_arc=-PI / 4), y=MAIN_Y, run_time=1.5, hold=0.3)
        # a constante sai de dentro da integral
        i3 = Eq("I", "=", r"\frac{\rho\pi}{2}", r"\int_{-a}^{a}", "(a^2-x^2)^2", "dx", size=42)
        self.mm(i2, i3, M(i2, [0, 1], i3, [0, 1]), M(i2, [3], i3, [2], path_arc=PI * 0.6), M(i2, [2], i3, [3]),
                M(i2, [4, 5], i3, [4, 5]), y=MAIN_Y, run_time=1.4, hold=0.3)
        # expansão do quadrado, numa linha à parte
        x0e = Eq("(a^2-x^2)^2", size=38)
        x0e.mob.move_to([0, AUX2_Y, 0])
        self.play(TransformFromCopy(VGroup(*i3.g(4)), x0e.mob), *self.note_anims(CLEAR), run_time=0.9)
        x1e = Eq("a^4", "-", "2a^2x^2", "+", "x^4", size=38)
        ox = x0e.px(0)                                     # ( a 2 − x 2 ) 2   em ordem de leitura
        self.mm(x0e, x1e, ([ox[0]], [], {}), ([ox[1]], [x1e.p(0)[0]], {}), ([ox[2]], [x1e.p(0)[1]], {}),
                ([ox[3]], x1e.p(1), {}), ([ox[4]], x1e.p(4)[:1], {}), ([ox[5]], x1e.p(4)[1:], {}),
                ([ox[6]], [], {}), ([ox[7]], [x1e.p(2)[0]], {"path_arc": -PI / 3}), y=AUX2_Y, cur=False,
                run_time=1.3, hold=0.4)
        i4 = Eq("I", "=", r"\frac{\rho\pi}{2}", r"\int_{-a}^{a}", "(", "a^4", "-", "2a^2x^2", "+", "x^4", ")", "dx",
                size=40)
        self.mm(i3, i4, M(i3, [0, 1, 2, 3], i4, [0, 1, 2, 3]), X(i3, [4], shift=DOWN * 0.3), M(i3, [5], i4, [11]),
                C(x1e.g(0, 1, 2, 3, 4), i4, [5, 6, 7, 8, 9], path_arc=PI / 4), extra=[FadeOut(x1e.mob)],
                y=MAIN_Y, run_time=1.4, hold=0.3)
        # a integral é avaliada: ∫(...)dx = 16a⁵/15
        i5 = Eq("I", "=", r"\frac{\rho\pi}{2}", r"\cdot", r"\frac{16a^5}{15}", size=42)
        self.mm(i4, i5, M(i4, [0, 1, 2], i5, [0, 1, 2]), (i4.p(3, 4, 5, 6, 7, 8, 9, 10, 11), i5.p(4), {}),
                y=MAIN_Y, run_time=1.4, hold=0.3)
        # 2 de baixo cancela com o 16: 16/2 = 8; ρ e π sobem
        i6 = Eq("I", "=", r"\frac{8\pi\rho a^5}{15}", size=44)
        ra, rb, rc = i5.frac(2)
        fa, fb, fc = i5.frac(4)
        sn, sb, sd = i6.frac(2)
        self.mm(i5, i6, M(i5, [0, 1], i6, [0, 1]), ([ra[0]], [sn[2]], {"path_arc": -PI / 3}),
                ([ra[1]], [sn[1]], {"path_arc": -PI / 3}), (rc, [], {"shift": UP * 0.4}), ([rb], [], {}),
                ([fa[0]], [], {"shift": UP * 0.4}), ([fa[1]], [sn[0]], {}), ([fa[2]], [sn[3]], {}),
                ([fa[3]], [sn[4]], {}), ([fb], [sb], {}), (fc, sd, {}), X(i5, [3]),
                y=MAIN_Y, run_time=1.5, hold=0.3, note=tex(r"\tfrac{16}{2}=8", 32))

        # ── massa da esfera: m = (4/3)πρa³  ->  ρ = 3m/(4πa³) ──
        self.ancora("a28")
        self.play(FadeOut(sdI.mob), *self.note_anims(CLEAR), run_time=0.4)
        Mm = Eq("m", "=", r"\tfrac43", r"\pi", r"\rho", "a^3", size=40)
        self.mm(None, Mm, y=AUX2_Y, cur=False, hold=0.4)
        Rho = Eq(r"\rho", "=", r"\frac{3m}{4\pi a^3}", size=40)
        fn, fbb, fd = Mm.frac(2)
        rn, rbb, rd = Rho.frac(2)
        self.mm(Mm, Rho, (Mm.p(4), Rho.p(0), {"path_arc": PI * 0.7}), M(Mm, [1], Rho, [1]),
                ([fd[0]], [rn[0]], {"path_arc": -PI / 3}), (Mm.p(0), [rn[1]], {"path_arc": -PI / 3}),
                ([fn[0]], [rd[0]], {"path_arc": -PI / 3}), (Mm.p(3), [rd[1]], {}), (Mm.p(5), rd[2:], {}),
                ([fbb], [rbb], {}), y=AUX2_Y, cur=False, run_time=1.5, hold=0.4)
        # a densidade entra, por cópia, na fórmula de I
        i7 = Eq("I", "=", r"\frac{8\pi a^5}{15}", r"\cdot", r"\frac{3m}{4\pi a^3}", size=42)
        on, ob, od = i6.frac(2)
        qn, qb, qd = i7.frac(2)
        self.mm(i6, i7, M(i6, [0, 1], i7, [0, 1]), ([on[0]], [qn[0]], {}), ([on[1]], [qn[1]], {}),
                ([on[2]], [], {"shift": UP * 0.4}), ([on[3]], [qn[2]], {}), ([on[4]], [qn[3]], {}),
                ([ob], [qb], {}), (od, qd, {}), C(Rho.g(2), i7, [4], path_arc=-PI / 4), extra=[FadeOut(Rho.mob)],
                y=MAIN_Y, run_time=1.5, hold=0.3)
        # reagrupa: números juntos, πa⁵ sobre πa³, m para fora
        self.ancora("a29")
        i8 = Eq("I", "=", r"\frac{8\cdot3}{15\cdot4}", r"\frac{\pi a^5}{\pi a^3}", "m", size=42)
        pn, pb, pd = i7.frac(2)
        sn2, sb2, sd2 = i7.frac(4)
        an, ab, ad = i8.frac(2)
        bn, bb, bd = i8.frac(3)
        self.mm(i7, i8, M(i7, [0, 1], i8, [0, 1]), ([pn[0]], [an[0]], {}), ([sn2[0]], [an[2]], {"path_arc": -PI / 3}),
                (pd, [ad[0], ad[1]], {}), ([sd2[0]], [ad[3]], {"path_arc": -PI / 3}), ([pb], [ab], {}),
                (pn[1:], bn, {"path_arc": PI / 3}), ([sd2[1]], [bd[0]], {}), (sd2[2:], bd[1:], {}),
                ([sn2[1]], [i8.p(4)[0]], {"path_arc": PI / 3}), ([sb2], [bb], {}), X(i7, [3]),
                y=MAIN_Y, run_time=1.6, hold=0.3)
        # cancelamentos: π com π, a⁵/a³ = a²
        i9 = Eq("I", "=", r"\frac{8\cdot3}{15\cdot4}", "m", "a^2", size=42)
        bn9, bb9, bd9 = i8.frac(3)
        self.mm(i8, i9, M(i8, [0, 1, 2], i9, [0, 1, 2]), M(i8, [4], i9, [3]), ([bn9[0]], [], {"shift": UP * 0.4}),
                ([bd9[0]], [], {"shift": DOWN * 0.4}), ([bb9], [], {}), ([bn9[1]], [i9.p(4)[0]], {}),
                ([bn9[2]], [i9.p(4)[1]], {}), (bd9[1:], [], {"shift": DOWN * 0.4}),
                y=MAIN_Y, run_time=1.5, hold=0.3, note=tex(r"\tfrac{\pi}{\pi}=1\qquad\tfrac{a^5}{a^3}=a^2", 32))
        # 8·3 / (15·4) simplifica: 8/4 = 2 e 3/15 = 1/5
        self.ancora("a30")
        res = Eq(r"I_{CM}", "=", r"\tfrac25", "m", "a^2", size=56, colors={2: MAGENTA})
        cn, cb, cd = i9.frac(2)
        tn, tb, td = res.frac(2)
        self.mm(i9, res, (i9.p(0), [res.p(0)[0]], {}), M(i9, [1], res, [1]), ([cn[0]], [tn[0]], {}),
                ([cn[1]], [], {"shift": UP * 0.4}), ([cn[2]], [], {"shift": UP * 0.4}), ([cb], [tb], {}),
                ([cd[0]], [], {"shift": DOWN * 0.4}), ([cd[1]], [td[0]], {}), ([cd[2]], [], {"shift": DOWN * 0.4}),
                ([cd[3]], [], {"shift": DOWN * 0.4}), M(i9, [3], res, [3]), M(i9, [4], res, [4]),
                y=MAIN_Y, box=True, run_time=1.6, hold=0.2, note=tex(r"\tfrac84=2\qquad\tfrac3{15}=\tfrac15", 32))
        bx = self.expr
        self.play(bx.animate.scale(1.18), *self.note_anims(CLEAR), run_time=0.6)
        self.play(bx[1].animate.set_stroke(MAGENTA, 4), Indicate(bx[0][0][4:7], color=MAGENTA, scale_factor=1.5),
                  Indicate(sph, color=MAGENTA, scale_factor=1.03), run_time=1.0)
        self.check_safe()
        self.wait(READ)

        # o resultado fica (caixa I_CM = 2/5 ma²); o resto da derivação é recolhido em c6_energia
        self.i_gone = VGroup(sph, axis, cmd, discs, a_line, a_lab, x_leg, x_lab, r_leg, r_lab, sq, poly, dx_span,
                             dx_lab, face, mag, spoke, rl, warc_d, dm_lab)
        self.i_res, self.i_resEq = bx, res

    # C6 — energia da esfera: K = 7/10 m v², com I_CM e ω entrando por cópia
    def c6_energia(self):
        self.mark("C6")
        self.ancora("a31")
        self.op_y, self.note_y = -2.50, -3.15
        y, cy, mg_ = self.op_y, CYAN, MAGENTA
        trans = {2: cy, 3: cy, 4: cy}
        E0, bx, aux_I = self.pend, self.i_res, self.i_resEq
        aux_w = Eq(r"\omega", "=", r"\frac{v}{a}", size=36, colors={0: mg_, 2: mg_})
        aux_w.mob.move_to([1.7, -3.85, 0])
        self.expr = None
        self.put(H=H_PART)
        self.bo.set_value(1.0)
        self.replay_on(H_PART, BETA, fresh=True)
        for m in (self.trk, self.cmp):
            m.update()
        # a derivação sai; a equação pendente volta ao tamanho cheio; a caixa de I_CM desce como relação-fonte
        self.clear_text(*self.caption("DE VOLTA À ENERGIA"), FadeOut(self.i_gone), FadeIn(self.trk), FadeIn(self.cmp),
                        bx.animate.scale(0.5).move_to([-1.0, -3.85, 0]),
                        E0.mob.animate.scale(1 / 0.7).move_to([0, y, 0]).set_opacity(1.0), run_time=1.2)
        self.remove(self.spin)
        self.expr = E0.mob
        self.play(FadeIn(aux_w.mob, shift=UP * 0.1), run_time=0.5)
        self.wait(0.3)
        # I_CM entra por cópia de 2/5 ma²
        self.ancora("a32")
        E1 = Eq("K", "=", r"\tfrac12", "m", "v^2", "+", r"\tfrac12", "(", r"\tfrac25", "m", "a^2", ")", r"\omega^2",
                colors={**trans, **{k: mg_ for k in range(6, 13)}})
        self.mm(E0, E1, M(E0, range(7), E1, range(7)), X(E0, [7], shift=UP * 0.3), M(E0, [8], E1, [12]),
                C(aux_I.g(2, 3, 4), E1, [8, 9, 10], path_arc=-PI / 4), y=y, run_time=1.3, hold=0.2)
        # ω entra por cópia de v/a (o expoente do ω² fica)
        self.ancora("a32b")
        E2 = Eq("K", "=", r"\tfrac12", "m", "v^2", "+", r"\tfrac12", "(", r"\tfrac25", "m", "a^2", ")", "(",
                r"\frac{v}{a}", ")^2", colors={**trans, **{k: mg_ for k in range(6, 15)}})
        om = E1.p(12)
        ex = E2.px(14)
        self.mm(E1, E2, M(E1, range(12), E2, range(12)), ([om[0]], [], {"shift": UP * 0.3}),
                ([om[1]], [ex[1]], {}), C(aux_w.g(2), E2, [13], path_arc=-PI / 4), y=y, run_time=1.3, hold=0.2)
        # (v/a)² = v²/a²: o expoente vai para cima e para baixo
        E3 = Eq("K", "=", r"\tfrac12", "m", "v^2", "+", r"\tfrac12", "(", r"\tfrac25", "m", "a^2", ")",
                r"\frac{v^2}{a^2}", colors={**trans, **{k: mg_ for k in range(6, 13)}})
        nv, bv, dv = E2.frac(13)
        nn, bn, dn = E3.frac(12)
        self.mm(E2, E3, M(E2, range(12), E3, range(12)), ([nv[0]], [nn[0]], {}), ([dv[0]], [dn[0]], {}),
                ([bv], [bn], {}), ([ex[1]], [nn[1]], {"path_arc": -PI / 3}), ([ex[1]], [dn[1]], {"path_arc": PI / 3}),
                X(E2, [12]), ([ex[0]], [], {}), y=y, run_time=1.2, hold=0.3,
                note=tex(r"\left(\tfrac{v}{a}\right)^2=\tfrac{v^2}{a^2}", 32))
        # a² do I_CM cancela com a² do denominador; ½·⅖ = ⅕
        self.ancora("a33")
        E4 = Eq("K", "=", r"\tfrac12", "m", "v^2", "+", r"\tfrac15", "m", "v^2",
                colors={**trans, 6: mg_, 7: mg_, 8: mg_})
        n6, b6, d6 = E3.frac(6)
        n8, b8, d8 = E3.frac(8)
        nB, bB, dB = E3.frac(12)
        n4, b4, d4 = E4.frac(6)
        self.mm(E3, E4, M(E3, range(6), E4, range(6)), ([n6[0]], [n4[0]], {}), ([b6], [b4], {}),
                ([d8[0]], [d4[0]], {}), (d6, [], {"shift": DOWN * 0.4}), (n8, [], {"shift": UP * 0.4}),
                ([b8], [], {}), X(E3, [7, 11]), M(E3, [9], E4, [7]), X(E3, [10], shift=UP * 0.4),
                (nB, E4.p(8), {}), (dB, [], {"shift": DOWN * 0.4}), ([bB], [], {}),
                y=y, run_time=1.6, hold=0.3, note=tex(r"\tfrac{a^2}{a^2}=1\qquad\tfrac12\cdot\tfrac25=\tfrac15", 30))
        # os dois coeficientes se juntam
        self.ancora("a34")
        E5 = Eq("K", "=", "(", r"\tfrac12", "+", r"\tfrac15", ")", "m", "v^2", colors={3: cy, 5: mg_})
        self.mm(E4, E5, M(E4, [0, 1], E5, [0, 1]), M(E4, [2], E5, [3]), M(E4, [5], E5, [4]), M(E4, [6], E5, [5]),
                M(E4, [3], E5, [7]), M(E4, [4], E5, [8]), X(E4, [7], shift=UP * 0.3), X(E4, [8], shift=UP * 0.3),
                y=y, run_time=1.3, hold=0.2)
        E6 = Eq("K", "=", "(", r"\tfrac{5}{10}", "+", r"\tfrac{2}{10}", ")", "m", "v^2", colors={3: cy, 5: mg_})
        a1, ab1, ad1 = E5.frac(3)
        a2, ab2, ad2 = E5.frac(5)
        b1n, bb1, bd1 = E6.frac(3)
        b2n, bb2, bd2 = E6.frac(5)
        self.mm(E5, E6, M(E5, [0, 1, 2, 4, 6, 7, 8], E6, [0, 1, 2, 4, 6, 7, 8]),
                ([a1[0]], [b1n[0]], {}), ([ab1], [bb1], {}), (ad1, bd1, {}),
                ([a2[0]], [b2n[0]], {}), ([ab2], [bb2], {}), (ad2, bd2, {}),
                y=y, run_time=1.2, hold=0.2, note=tex(r"\tfrac12=\tfrac5{10}\qquad\tfrac15=\tfrac2{10}", 32))
        E7 = Eq("K", "=", r"\tfrac{7}{10}", "m", "v^2")
        c1n, cb1, cd1 = E6.frac(3)
        c2n, cb2, cd2 = E6.frac(5)
        f7n, f7b, f7d = E7.frac(2)
        slide = E6.center(c1n[0]) - E6.center(c2n[0])
        self.mm(E6, E7, M(E6, [0, 1], E7, [0, 1]), M(E6, [7], E7, [3]), M(E6, [8], E7, [4]),
                ([c1n[0]], [f7n[0]], {}), (c2n, [], {"shift": slide}), ([cb1], [f7b], {}), (cd1, f7d, {}),
                ([cb2], [], {}), (cd2, [], {"shift": DOWN * 0.3}), X(E6, [2, 4, 6]),
                y=y, box=True, run_time=1.4, note=tex(r"\tfrac5{10}+\tfrac2{10}=\tfrac7{10}", 32))
        self.check_safe()
        self.wait(READ_RES)
        self.replay_off(FadeOut(bx), FadeOut(aux_w.mob))
        self.put(H=H_PART)

    def energy_graph(self, H, b, s0, s1):
        """Gráfico de energia ao longo do trajeto, normalizado por E_total = mgh, e seu cursor.

        As curvas e o cursor saem do MESMO s da esfera (e de H, beta): U = y(s)/H, K = 1 - U,
        K_trans = K/(1+beta), K_rot = K beta/(1+beta). O cursor lê self.cs(), como a barra de energia."""
        gx0, gy0, gw, gh, vmax = -2.75, -3.2, 4.4, 1.95, 1.12
        gp = lambda p, v: np.array([gx0 + gw * p, gy0 + gh * v / vmax, 0.0])
        ss = np.linspace(s0, s1, 400)
        pp = (ss - s0) / (s1 - s0)
        U = ys(ss) / H
        K = 1 - U
        Kt, Kr = K / (1 + b), K * b / (1 + b)
        assert np.allclose(U + Kt + Kr, 1.0) and np.allclose(Kt[K > 1e-6] / Kr[K > 1e-6], (1 / b))   # 5 : 2

        def curve(vals, col):
            return VMobject().set_points_as_corners([gp(p, v) for p, v in zip(pp, vals)]).set_stroke(col, 4.5)

        def mark(s, label):
            p = (s - s0) / (s1 - s0)
            return VGroup(DashedLine(gp(p, 0), gp(p, 1.0), dash_length=0.08).set_stroke(WHITE, 1.5, 0.3),
                          tag(label, 15, opacity=0.8).move_to(gp(p, 0) + [0, -0.2, 0]))

        legend = VGroup(*(row(Line(ORIGIN, RIGHT * 0.38).set_stroke(col, 5), tex(lab, 28), buff=0.14)
                          for lab, col in ((r"K_{\rm trans}", CYAN), (r"K_{\rm rot}", MAGENTA), ("U", VIOLET))))
        legend.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        legend.move_to(gp(1, 0.44) + [0.45 + legend.width / 2, 0, 0])      # coluna vertical à direita do gráfico
        assert legend.get_right()[0] < SAFE_X and legend.get_bottom()[1] > SAFE_BOTTOM + 0.3
        marks = VGroup(mark(s0 + 0.05, "PARTIDA"), mark(0.0, "FUNDO"), mark(PI, "TOPO"))
        marks[0][1].shift(RIGHT * 0.25)
        static = VGroup(
            VGroup(Line(gp(0, 0), gp(1.02, 0)), Line(gp(0, 0), gp(0, vmax))).set_stroke(WHITE, 2.5, 0.85),
            DashedLine(gp(0, 1), gp(1, 1), dash_length=0.12).set_stroke(WHITE, 2.5, 0.9),
            marks,
            curve(U, VIOLET), curve(Kt, CYAN), curve(Kr, MAGENTA),
            tex(r"E/E_{\rm total}", 22).move_to(gp(0, vmax) + [0.6, 0.12, 0]),
            tex(r"E_{\rm total}", 26).next_to(gp(1, 1), RIGHT, 0.12),
            legend,
            tag("PROGRESSO NO TRAJETO", 14, opacity=0.7).move_to(gp(0.5, 0) + [0, -0.5, 0]))

        def cursor():
            s = self.cs()
            p = float(np.clip((s - s0) / (s1 - s0), 0, 1))
            u = float(ys(s)[0]) / self.H.get_value()
            k = max(1 - u, 0.0)
            bb = self.b.get_value()
            return VGroup(Line(gp(p, 0), gp(p, vmax)).set_stroke(WHITE, 2, 0.55),
                          Dot(gp(p, u), 0.085, color=VIOLET), Dot(gp(p, k / (1 + bb)), 0.085, color=CYAN),
                          Dot(gp(p, k * bb / (1 + bb)), 0.085, color=MAGENTA))

        return static, always_redraw(cursor)

    # C7 — barra de energia acompanhando a esfera (rampa -> fundo -> subida)
    def c7_barras(self):
        self.mark("C7")
        self.ancora("a35")
        self.note_y = -3.2
        self.clear_text(*self.caption("PARA ONDE VAI A ENERGIA?"), run_time=0.5)
        self.hmk.update()
        self.bar.update()
        self.play(FadeIn(self.hmk), FadeIn(self.bar), FadeIn(self.bargroup), *self.set_hval(r"h=2{,}5R"),
                  self.bo.animate.set_value(1), run_time=0.7)
        self.note(mtex(r"K_{\rm trans}", ":", r"K_{\rm rot}", "=", "5", ":", "2", size=38))
        self.hint[0].set_color(CYAN), self.hint[2].set_color(MAGENTA)
        self.wait(BEAT)
        self.ancora("a36")
        self.play(self.go(2.1))
        self.check_safe()
        self.wait(0.6)

    # C8 — altura mínima da esfera: 2,7R; a linha, o rótulo, a esfera e a energia inicial sobem juntos
    def c8_limite(self):
        self.mark("C8")
        self.ancora("a37")
        self.note_y = -3.2
        ref25 = VGroup(DashedLine([-3.0, YB + RS * H_PART, 0], [XG, YB + RS * H_PART, 0], dash_length=0.12)
                       .set_stroke(VIOLET, 2, 0.35),
                       tex(r"2{,}5R", 26, VIOLET).set_opacity(0.5).move_to([2.2, YB + RS * H_PART - 0.25, 0]))
        x25 = BAR_X0 + BAR_W * H_PART / H_REF
        ghost = Line([x25, BAR_Y - 0.28, 0], [x25, BAR_Y + 0.28, 0]).set_stroke(WHITE, 3, 0.85)
        delta = tex(r"+0{,}2\,mgR", 26, VIOLET).move_to([2.7, BAR_Y + 0.42, 0])
        vb = self.vbox
        vb.scale(AUX_S).move_to([0, AUX_Y, 0])           # a MESMA relação do topo, de novo como fonte
        self.clear_text(self.bo.animate.set_value(0), *self.caption("ALTURA MÍNIMA DA ESFERA"),
                        *self.set_hval(r"h=\,?"), run_time=0.5)
        self.put(H=H_PART)
        self.replay_on(H_PART, BETA, fresh=True)
        self.play(FadeIn(vb), run_time=0.5)
        self.hchain(r"\tfrac{7}{10}", r"\tfrac{20}{10}", r"\tfrac{27}{10}", "2{,}7R",
                    tag("ROLAMENTO IDEAL SEM DESLIZAMENTO", 22),
                    anc=dict(A0="a38", ind="a39", A1="a40", A2="a40b", A6="a41", A7="a41b"))
        self.replay_off()
        self.put(H=H_PART)
        self.play(self.bo.animate.set_value(1), run_time=0.3)
        up = tex(r"2{,}5R\;\to\;2{,}7R", 32, VIOLET)
        up.add_updater(lambda m: m.move_to([1.3, YB + RS * self.H.get_value() + 0.3, 0]))
        up.update()
        self.play(FadeIn(ref25), FadeIn(ghost), run_time=0.4)
        self.play(FadeOut(self.hval), FadeIn(up), self.H.animate.set_value(H_IDEAL),
                  run_time=2.0)
        self.hval = None
        self.play(FadeOut(up), *self.set_hval(r"h=2{,}7R"), FadeIn(delta), run_time=0.5)
        self.check_safe()
        self.wait(0.3)
        self.ref25, self.ghost, self.delta = ref25, ghost, delta

    # C9 — payoff: a esfera parte de 2,7R e completa o loop; barra, gráfico e esfera usam o mesmo s
    def c9_payoff(self):
        self.mark("C9")
        self.ancora("a42")
        static, cur = self.energy_graph(H_IDEAL, BETA, s_start(H_IDEAL), S_END)
        self.gstatic, self.gcur = static, cur
        self.clear_text(*self.caption("AGORA, DE 2,7R"), FadeOut(self.ghost), FadeOut(self.delta), FadeOut(self.vbox),
                        FadeOut(self.legend), run_time=0.5)
        cur.update()
        self.play(FadeIn(static), FadeIn(cur), run_time=0.6)
        self.add(self.forc)
        self.play(self.go(S_END))
        done = tag("COMPLETA O LOOP", 26, CYAN).move_to([0, -4.15, 0])
        self.play(FadeIn(done), run_time=0.4)
        self.check_safe()
        self.wait(READ)
        self.play(FadeOut(done), run_time=0.3)

    # C10 — síntese sobre a pista: a esfera volta a percorrer o loop enquanto os resultados aparecem
    def c10_sintese(self):
        self.mark("C10")
        self.ancora("a44")
        Y25, Y27 = YB + RS * H_PART, YB + RS * H_IDEAL
        l25 = tag("PARTÍCULA · 2,5R", 18).move_to([1.7, Y25 - 0.25, 0])
        l27 = tag("ESFERA · 2,7R", 18, VIOLET).move_to([1.7, Y27 + 0.25, 0])

        def item(label, s, y):
            return row(label, boxed(tex(s, 44)), buff=0.45).move_to([0, y, 0])

        self.play(FadeOut(self.bar), FadeOut(self.bartitle), FadeOut(self.forc), FadeOut(self.hval),
                  FadeOut(self.gstatic), FadeOut(self.gcur),
                  FadeOut(self.ref25[1]), FadeIn(l25), FadeIn(l27), self.tk.animate.set_value(0.45),
                  self.bo.animate.set_value(0), *self.caption("POR QUE A ESFERA PRECISA", "DE MAIS ALTURA?"), run_time=0.7)
        self.put(H=H_IDEAL)
        rows = VGroup(item(tag("PARTÍCULA", 22, opacity=0.9), r"h_{\min}=2{,}5R", -0.45),
                      item(tag("ESFERA MACIÇA", 22, VIOLET), r"h_{\min}=2{,}7R", -1.45))
        ideas = VGroup(tag("MESMA VELOCIDADE MÍNIMA NO TOPO", 24),
                       tag("+ ENERGIA TAMBÉM NA ROTAÇÃO", 24, MAGENTA),
                       row(tex(r"\Rightarrow", 40, VIOLET), tag("ALTURA INICIAL MAIOR", 30, VIOLET), buff=0.25)
                       ).arrange(DOWN, buff=0.35).move_to([0, -3.1, 0])
        # as linhas entram nos instantes da fala (sem escala: tscale = 1 neste play)
        ex = self.extras
        agora = self.renderer.time
        quando = [(rows[0], agora + 0.1), (rows[1], agora + 1.4),
                  (ideas[0], ex.get("a45", agora + 3.0)), (ideas[1], ex.get("a45b", agora + 4.5)),
                  (ideas[2], ex.get("a46", agora + 6.0))]
        texts, fim_t = [], agora
        for mob, t in quando:
            texts += [Wait(max(0.04, t - fim_t)), FadeIn(mob, shift=UP * 0.1, run_time=0.5)]
            fim_t = max(t, fim_t) + 0.5
        self.tscale = 1.0
        run = Succession(self.bo.animate(run_time=0.3).set_value(1).build(), self.go(S_END).build())
        self.play(AnimationGroup(run, Succession(*texts)))
        self.check_safe()
