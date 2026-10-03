"""Campo elétrico dentro e fora de uma esfera isolante com ρ(r) = ρ0 (1 − r/R): preview silencioso (V2.1).

EXERCÍCIO RESOLVIDO · EP. 05.

Uma única investigação contínua; nenhuma equação importante só "aparece".

  Gauss, por geometria: gaussiana (raio r) -> E sobre ela (mesmo módulo) -> dA⃗ (patch dA + normal n̂, d⃗A = n̂ dA)
    -> E ∥ dA ⇒ θ = 0, cos 0 = 1 -> E⃗·dA⃗ = E dA -> ∮E dA -> E ∮dA -> E 4πr² = Q_enc(r)/ε0 (linha persistente)
  Q_enc(r) (cópia de glifos) -> ∫dQ -> casca em corte (r', dr') -> casca aberta -> dV = 4πr'² dr' -> dQ = ρ(r') dV
    -> ∫ρ(r') 4πr'² dr' -> ρ(r') = ρ0(1 − r'/R) -> integrar -> volta ao Gauss -> corta 4π e r² -> E_in(r)
  gráfico (curva revelada pelo tracker) -> r = R: Q = Q_enc(R) -> E_in(r) vira E_out(r) -> função por partes
  -> dE/dr passo a passo -> tangente (> 0 … = 0) -> resolver -> r_max = 2R/3 -> interpretação por Δr -> checagens.

Estados de layout (a esfera só fica deslocada enquanto houver conteúdo que o justifique):
  SOLO_CENTER (LA, LGA, LC): esfera sozinha no centro; LGA é a esfera ampliada da cena de Gauss.
  PRIMARY_LEFT (LP): esfera à esquerda enquanto a definição de ρ e a casca aberta estão à direita (S4–S5).
  SPHERE_GRAPH (LC + gráfico centrado): esfera sobre o gráfico, os dois no eixo central do quadro.
  MATH_FOCUS (LM): esfera pequena no canto enquanto a derivação ocupa a tela (S8–S9); volta ao centro no payoff.
Todas as posições são absolutas e todas as mudanças de estado são animadas.

Tracker único: x = r/R (`T.X`): raio da gaussiana, marca radial, setas, ponto do gráfico, curva revelada
(`T.RV`: revela até o maior x já visitado). Gráfico adimensional: x = r/R, E0 = ρ0 R / ε0. e(x) = x/3 − x²/4
(x ≤ 1), e(x) = 1/(12 x²) (x ≥ 1); máximo em x = 2/3, e = 1/9; e(1) = 1/12; e_max = (4/3) e(1).

Gramática visual: contorno contínuo azul = esfera física; tracejado violeta = gaussiana; ciano = E⃗ (sobre a gaussiana);
lavanda clara = n̂, dA e d⃗A; magenta = densidade e carga (gradiente contínuo, sem pontinhos); branco = r', casca, texto.

`ATE=k` (1–12) renderiza só até o segmento k. Sem voz: os tempos (`until`) seguem o storyboard de referência.
"""

import json
import os
import sys
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from PIL import Image
from manim import (
    DOWN, LEFT, PI, RIGHT, UP, AnimationGroup, Annulus, Arrow, Brace, Circle, Create, DashedLine, Dot, FadeIn,
    FadeOut, GrowFromPoint, ImageMobject, Indicate, Line, MathTex, ManimColor, Polygon, Scene,
    SurroundingRectangle, TransformFromCopy, VGroup, VMobject, ValueTracker, always_redraw, config, linear, smooth,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from MF_Tools import TransformByGlyphMap
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR, WATERMARK_PATH
from template.fonts import screen_text

ATE = int(os.environ.get("ATE", "99"))
PASTA = Path(__file__).resolve().parent
CAL = os.environ.get("SYNC_CAL") == "1"        # calibragem: mede o tempo NATIVO de cada âncora

# ── Paleta ──────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # campo elétrico
BLUE = "#267BFF"          # geometria
BLUE_L = "#7FB2FF"        # superfície física
VIOLET = "#9C8CFF"        # gaussiana, r, r² (SECONDARY_COLOR #745CFF clareado: contraste, como no vid_0011)
MAGENTA = "#EA63FF"       # densidade e carga
NCOL = "#EDE7FF"          # n̂, dA, d⃗A (lavanda clara: distinta de E⃗ e da gaussiana)

# Cores dos termos na legenda queimada (montar_legendado.py --color-module); mesmos significados da cena
SUBTITLE_TERM_COLORS = {
    "campo": CYAN, "campo elétrico": CYAN, "campo interno": CYAN, "campo externo": CYAN,
    "densidade": MAGENTA, "carga": MAGENTA, "carga encerrada": MAGENTA,
    "gaussiana": VIOLET, "área": VIOLET, "normal": NCOL,
}

SAFE_X = 3.5
SAFE_BOTTOM = -4.6        # abaixo disso: faixa reservada a legendas

# ── Modelo (adimensional) ───────────────────────────────────────────────────
XM = 2 / 3                # posição do máximo
XMAX = 3.3                # limite horizontal do gráfico


def e_in(x):
    return x / 3 - x * x / 4


def e_out(x):
    return 1 / (12 * x * x)


def e(x):
    return e_in(x) if x <= 1 else e_out(x)


def ep(x):
    """de/dx."""
    return 1 / 3 - x / 2 if x <= 1 else -1 / (6 * x ** 3)


def rho_rel(x):
    """ρ/ρ0."""
    return max(1 - x, 0.0)


def _qa():
    """Verificações numéricas independentes (dimensionais, com ρ0, R, ε0 arbitrários)."""
    rho0, R, eps = 2.3e-6, 0.37, 8.854e-12
    e_dim_in = lambda r: rho0 / eps * (r / 3 - r * r / (4 * R))
    e_dim_out = lambda r: rho0 * R ** 3 / (12 * eps * r * r)
    # Gauss + integral numérica das cascas: Q_enc(r) = ∫ ρ(r') 4π r'² dr'
    for r in (0.1 * R, 0.5 * R, 2 * R / 3, 0.9 * R, R):
        rp = np.linspace(0, r, 400001)
        f = rho0 * (1 - rp / R) * 4 * np.pi * rp ** 2
        q = float(np.sum((f[1:] + f[:-1]) / 2 * np.diff(rp)))
        assert np.isclose(q, 4 * np.pi * rho0 * (r ** 3 / 3 - r ** 4 / (4 * R)), rtol=1e-9)
        assert np.isclose(q / (4 * np.pi * eps * r * r), e_dim_in(r), rtol=1e-9)
    assert np.isclose(4 * np.pi * rho0 * (R ** 3 / 3 - R ** 4 / (4 * R)), np.pi * rho0 * R ** 3 / 3)   # Q total
    for r in (1.0 * R, 1.7 * R, 40 * R):
        assert np.isclose(np.pi * rho0 * R ** 3 / 3 / (4 * np.pi * eps * r * r), e_dim_out(r), rtol=1e-12)
    # fluxo: E ∥ dA (θ = 0) e |E| constante => ∮E·dA = E · 4π r²; derivada termo a termo; raiz de dE/dr
    assert np.isclose(np.cos(0.0), 1.0)
    xs = np.linspace(0.05, 0.95, 19)
    assert np.allclose((e_in(xs + 1e-6) - e_in(xs - 1e-6)) / 2e-6, 1 / 3 - 2 * xs / 4, atol=1e-7)   # d/dr(r/3) − d/dr(r²/4R)
    assert np.allclose(1 / 3 - 2 * xs / 4, 1 / 3 - xs / 2)                                           # 2r/4R = r/2R
    assert np.isclose(3 * XM, 2) and np.isclose(1 / 3, XM / 2)                                       # 1/3 = r/2R ⇔ 3r = 2R
    # pontos estratégicos
    assert e_dim_in(0) == 0                                                          # E(0) = 0
    assert np.isclose(e_dim_in(2 * R / 3), rho0 * R / (9 * eps), rtol=1e-12)         # E(2R/3) = ρ0 R / 9ε0
    assert np.isclose(e_dim_in(R), rho0 * R / (12 * eps), rtol=1e-12)                # E(R) = ρ0 R / 12ε0
    assert np.isclose(e_dim_in(2 * R / 3) / e_dim_in(R), 4 / 3, rtol=1e-12)          # E_max = 4/3 E(R)
    assert np.isclose(e_dim_in(R), e_dim_out(R), rtol=1e-12)                         # contínuo em R
    h = 1e-7 * R                                                                     # derivadas laterais em R
    d_in = (e_dim_in(R) - e_dim_in(R - h)) / h
    d_out = (e_dim_out(R + h) - e_dim_out(R)) / h
    assert np.isclose(d_in, -rho0 / (6 * eps), rtol=1e-5) and np.isclose(d_out, -rho0 / (6 * eps), rtol=1e-5)
    assert np.isclose(d_in, d_out, rtol=1e-5)                                        # sem bico em R
    assert -rho0 / (2 * R * eps) < 0                                                 # E'' < 0
    assert e_dim_out(1e6 * R) < 1e-10 * e_dim_in(R)                                  # E → 0 no infinito
    assert 0 < 2 * R / 3 < R
    r = np.linspace(1e-6, 4 * R, 400001)
    emp = np.where(r <= R, e_dim_in(r), e_dim_out(np.maximum(r, 1e-12)))
    assert np.isclose(r[int(np.argmax(emp))], 2 * R / 3, rtol=1e-4)                  # máximo global em 2R/3
    # versão adimensional usada no gráfico: e(x) = E / E0, E0 = ρ0 R / ε0
    for x in (0.0, 0.2, XM, 1.0, 1.5, 3.0):
        assert np.isclose(e(x), (e_dim_in(x * R) if x <= 1 else e_dim_out(x * R)) / (rho0 * R / eps))
    assert np.isclose(e(XM), 1 / 9) and np.isclose(e(1.0), 1 / 12) and np.isclose(e(XM) / e(1.0), 4 / 3)
    assert np.isclose(ep(XM), 0) and np.isclose(ep(1 - 1e-12), ep(1 + 1e-12)) and np.isclose(ep(0), 1 / 3)
    # interpretação por Δr: em termos ABSOLUTOS a casca da borda tem mais carga (dQ ∝ x²(1−x), pico em 2/3); o que
    # decide E ∝ Q_enc/r² é o crescimento RELATIVO: Q_enc cresce mais que r² perto do centro e menos perto da borda
    q = lambda x: x ** 3 / 3 - x ** 4 / 4
    assert q(0.30) / q(0.12) > (0.30 / 0.12) ** 2 and q(0.96) / q(0.78) < (0.96 / 0.78) ** 2
    assert q(0.96) - q(0.78) > q(0.30) - q(0.12) > 0
    assert e(0.30) > e(0.12) and e(0.96) < e(0.78) and ep(0.78) < 0                 # E sobe, depois cai


_qa()

# ── Composição ──────────────────────────────────────────────────────────────
# Esfera: (CX, CY, RS). Gráfico fixo e CENTRADO no quadro: x ∈ [0, XMAX] ocupa [GX0, GX0 + GSX·XMAX] = [−3,3; 3,3].
LA = (0.0, 2.5, 1.8)      # SOLO_CENTER: abertura
LGA = (0.0, 2.7, 2.0)     # SOLO_CENTER ampliada: Lei de Gauss
LP = (-1.9, 3.9, 1.6)     # PRIMARY_LEFT: cascas (definição de ρ e casca aberta à direita)
LC = (0.0, 3.9, 1.6)      # SPHERE_GRAPH: esfera centrada sobre o gráfico
LM = (-2.9, 5.0, 0.8)     # MATH_FOCUS: esfera pequena no canto
GSX, GY0, GSY = 2.0, -3.6, 24.0
GX0 = -GSX * XMAX / 2
SLOT = 1.05               # y da equação de trabalho em SPHERE_GRAPH (entre a esfera e o gráfico)
TILT = 0.26               # achatamento do equador (sugere esfera)
DR0 = 0.09                # espessura (exagerada) da casca dr', em R
HA = np.radians(35)       # ponto destacado da gaussiana (patch dA, normal n̂)
E_ANGLES = (35, 95, 155, 215, 275, 335)
DA_ANGLES = (107, 167, 287, 347)
GTR = ValueTracker(0.0)   # deslocamento vertical do gráfico (só durante a interpretação, S11)
GSHIFT = 0.55             # quanto o gráfico desce na interpretação (mesmo x, centrado)


# ── Texto e utilidades (mesmo idioma do vid_0010/vid_0011) ──────────────────
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


def tex(content, size=40, color=WHITE):
    return MathTex(content, font_size=size, color=color)


def mixed(*items, buff=0.15):
    return VGroup(*items).arrange(RIGHT, buff=buff)


def fit(m, w=2 * SAFE_X - 0.3):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def boxed_rect(mob, color=WHITE, buff=0.15):
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08, stroke_width=2.5)


def soft_swap(old, new, shift=UP * 0.12, lag=0.55):
    return AnimationGroup(FadeOut(old, shift=shift), FadeIn(new, shift=shift), lag_ratio=lag)


def sstep(u):
    u = float(np.clip(u, 0.0, 1.0))
    return u * u * (3 - 2 * u)


def gpt(x):
    """Ponto do gráfico (tela) para x = r/R."""
    return np.array([GX0 + GSX * x, GY0 + GTR.get_value() + GSY * e(x), 0.0])


# ── Equações com índices de glifos (MF-Tools), como no vid_0010/vid_0011 ────
class Eq:
    """MathTex de string única + índices de glifos por parte, para TransformByGlyphMap."""

    def __init__(self, *parts, size=46, colors=None):
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

    def frac(self, i):
        """Numerador (da esquerda p/ a direita), barra e denominador de uma fração, por geometria."""
        idx = self.p(i)
        c = {k: self.mob[0][k].get_center() for k in idx}
        bar = max(idx, key=lambda k: self.mob[0][k].width)
        num = sorted((k for k in idx if k != bar and c[k][1] > c[bar][1]), key=lambda k: c[k][0])
        den = sorted((k for k in idx if k != bar and c[k][1] < c[bar][1]), key=lambda k: c[k][0])
        return num, bar, den


def copy_from(src):
    """Introdutor: o destino nasce de uma CÓPIA dos glifos `src`, que ficam onde estão."""
    class _Copy(TransformFromCopy):
        def __init__(self, mob, **kw):
            super().__init__(VGroup(*src), mob, **kw)
    return _Copy


def M(A, pa, B, pb, **kw):
    return (A.p(*pa), B.p(*pb), kw)


def X(A, pa, **kw):
    return (A.p(*pa), [], kw)


def CG(src, gb, **kw):
    kw.setdefault("delay", 0.2)
    return (copy_from(src), list(gb), kw)


def MG(ga, gb, **kw):
    return (list(ga), list(gb), kw)


# ── Geometria desenhada por pontos ──────────────────────────────────────────
def circ_pts(cx, cy, r, a0=0.0, a1=2 * PI, n=121):
    a = np.linspace(a0, a1, n)
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a), np.zeros_like(a)], axis=-1)


def ell_pts(cx, cy, r, a0, a1, n=61):
    a = np.linspace(a0, a1, n)
    return np.stack([cx + r * np.cos(a), cy + TILT * r * np.sin(a), np.zeros_like(a)], axis=-1)


def poly_mob(pts, color, width, op):
    m = VMobject().set_points_as_corners(pts)
    return m.set_stroke(color, width, op).set_fill(color, 0)


def dashed_ring(cx, cy, r, a0, a1, color, width, op, n=40, duty=0.58):
    out = VGroup()
    step = (a1 - a0) / n
    for k in range(n):
        out.add(poly_mob(circ_pts(cx, cy, r, a0 + k * step, a0 + (k + duty) * step, 5), color, width, op))
    return out


def sphere_image(kind, n=600):
    """Corte da esfera: gradiente radial contínuo. Densidade ∝ alfa ∝ (1 − x); 0 na superfície."""
    ax = (np.arange(n) + 0.5) / n * 2 - 1
    xx, yy = np.meshgrid(ax, -ax)
    rr = np.hypot(xx, yy)
    if kind == "uniform":
        a = np.where(rr < 1, 0.55, 0.0) * np.clip((1 - rr) * n / 2, 0, 1)
        w = np.zeros_like(rr)
    else:
        a = 0.95 * np.clip(1 - rr, 0, 1)
        w = 0.5 * np.clip(1 - rr, 0, 1) ** 2             # núcleo mais claro: o centro brilha
    base = np.array(ManimColor(MAGENTA).to_rgb()) * 255
    rgb = base[None, None, :] * (1 - w[..., None]) + 255 * w[..., None]
    return np.dstack([rgb, a * 255]).astype(np.uint8)


# ── Cena ────────────────────────────────────────────────────────────────────
class CampoEsfera012(Scene):

    # ── Quadro e sincronia com a narração ───────────────────────────────────
    # Cada self.ancora("x") casa um ponto do código com um instante da fala (sync.json). `ntime` é o relógio
    # NOMINAL da cena (soma dos run_time/waits sem escala; until(t) o preenche até t). Entre duas âncoras
    # ativas, play/wait são escalados para o trecho durar o que a fala dura; native.json guarda o tempo nominal
    # de cada âncora (SYNC_CAL=1 regenera). Âncoras que não constam em sync.json são ignoradas. Sem
    # sync.json/native.json a cena roda em tempo nominal (preview silencioso).
    def sync_init(self):
        self.tscale, self.ntime, self.nativos = 1.0, 0.0, {}
        arq = PASTA / "sync.json"
        dados = json.load(open(arq)) if arq.exists() else {}
        self.anc, self.extras = dados.get("anchors", []), dados.get("extras", {})
        nat = PASTA / "native.json"
        self.nat = json.load(open(nat)) if nat.exists() and not CAL else {}

    def _quadro(self, t):
        fps = config.frame_rate
        return max(1, round(t * fps)) / fps

    def play(self, *args, **kwargs):
        if args and not getattr(self, "_cru", False):
            anims = self.compile_animations(*args, **kwargs)
            self.ntime += max(a.run_time for a in anims)
            if abs(self.tscale - 1.0) > 1e-6:
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
        self.ntime += duration
        self.esperar_cru(self._quadro(duration * self.tscale))

    def until(self, t):
        d = t + self.toff - self.ntime
        if d > 0.02:
            self.wait(d)
        elif d < -0.25:
            print("ATRASO %.2f s antes de %.1f" % (-d, t + self.toff))

    def ancora(self, nome):
        agora = self.renderer.time
        if CAL:
            self.nativos[nome] = round(agora, 3)
            if nome == "fim":
                json.dump(self.nativos, open(PASTA / "native.json", "w"), indent=1)
            return
        nomes = [n for n, _ in self.anc]
        if not self.anc or nome not in self.nat or nome not in nomes:
            return
        i = nomes.index(nome)
        t_a = self.anc[i][1]
        if agora < t_a:
            self.esperar_cru(t_a - agora)
            agora = t_a
        elif agora - t_a > 0.25:
            print("SYNC atraso %.2f s em %s" % (agora - t_a, nome))
        self.ntime = self.nat[nome]
        if i + 1 < len(self.anc):
            prox, t_prox = self.anc[i + 1]
            gap_nat = max(0.2, self.nat[prox] - self.nat[nome])
            self.tscale = float(np.clip((t_prox - agora) / gap_nat * 0.985, 0.45, 2.0))
        else:
            self.tscale = 1.0

    def head(self, label):
        new = text(label, 24, opacity=0.75).move_to([0, 6.35, 0])
        if self.hl is None:
            self.play(FadeIn(new, shift=UP * 0.1), run_time=0.5)
        else:
            self.play(FadeOut(self.hl, shift=UP * 0.1), FadeIn(new, shift=UP * 0.1), run_time=0.5)
        self.hl = new

    def place(self, eq, x=0.0, y=0.0):
        fit(eq.mob).move_to([x, y, 0])
        return eq

    def layout(self, L):
        """Animações que levam a esfera ao estado de layout L = (CX, CY, RS)."""
        T = self.T
        return [T.CX.animate.set_value(L[0]), T.CY.animate.set_value(L[1]), T.RS.animate.set_value(L[2])]

    def gshift(self, d, e0=0.85, tk=1.0):
        """Animações que deslocam o gráfico inteiro (d > 0: para cima), sempre centrado em x = 0.
        e0 / tk: opacidade do rótulo E0 e das marcas do eixo (reduzidas nas cenas de leitura densa)."""
        return [GTR.animate.set_value(GTR.get_value() + d), self.axes.animate.shift(UP * d),
                self.ticks.animate.shift(UP * d).set_opacity(tk), self.e0lab.animate.shift(UP * d).set_opacity(e0)]

    def _finish(self, new, box, hold):
        out = new.mob
        if box:
            out = VGroup(new.mob, boxed_rect(new.mob))
            self.play(FadeIn(out[1]), run_time=0.3)
            self.add(out)
        if hold:
            self.wait(hold)
        return out

    def mm(self, old, new, *moves, y=None, x=None, rt=1.2, hold=0.3, extra=(), box=False, scale=1.0, width=None):
        """old (Eq) -> new (Eq) por TransformByGlyphMap; o que não for citado entra/sai por fade."""
        c = old.mob.get_center()
        new.mob.scale(scale)
        fit(new.mob, width or 2 * SAFE_X - 0.3).move_to([c[0] if x is None else x, c[1] if y is None else y, 0])
        self.play(TransformByGlyphMap(old.mob, new.mob, *moves, auto_fade=True), *extra, run_time=rt)
        self.remove(old.mob)
        return self._finish(new, box, hold)

    def born(self, new, *moves, x=0.0, y=0.0, rt=1.2, hold=0.2, extra=(), box=False, width=None):
        """`new` nasce de CÓPIAS de glifos já na tela (moves = CG(...)); o resto entra por fade."""
        fit(new.mob, width or 2 * SAFE_X - 0.3).move_to([x, y, 0])
        dummy = MathTex("x", font_size=20).set_opacity(0).move_to(new.mob)
        self.play(TransformByGlyphMap(dummy, new.mob, *moves, auto_fade=True), *extra, run_time=rt)
        self.remove(dummy)
        return self._finish(new, box, hold)

    def show(self, eq, x=0.0, y=0.0, run_time=0.8, extra=(), shift=UP * 0.1):
        self.place(eq, x, y)
        self.play(FadeIn(eq.mob, shift=shift), *extra, run_time=run_time)
        return eq

    # ── Estado e objetos da cena ────────────────────────────────────────────
    def build(self):
        mk = ValueTracker
        T = self.T = SimpleNamespace(
            X=mk(0.0), CX=mk(LA[0]), CY=mk(LA[1]), RS=mk(LA[2]), SV=mk(1.0),
            UOP=mk(0.0), GOP=mk(0.0), OL=mk(1.0),          # esfera uniforme / com gradiente / contorno
            MK=mk(0.0), GA=mk(0.0), GF=mk(0.0),            # marca radial / gaussiana / preenchimento
            FA=mk(0.0), FM=mk(0.0), FL=mk(1.0), FD=mk(1.0),   # setas de E: opacidade / modo / crescimento / dim dos demais
            DA=mk(0.0), PA=mk(0.0), NV=mk(0.0),            # vetores dA (amostragem) / patch dA / normal n̂
            LR=mk(0.0), LD=mk(0.0), LN1=mk(0.0), LN2=mk(0.0), LE=mk(0.0),   # rótulos: r, dA, n̂, d⃗A, E⃗
            RL=mk(0.0), SH=mk(0.0), XP=mk(0.04), DX=mk(DR0), SI=mk(0.0), DL=mk(0.0),   # r', casca
            ACC=mk(0.0), ACO=mk(0.0),                      # disco acumulado (integral): raio e opacidade
            GE=mk(0.0), RV=mk(0.0), PT=mk(0.0), TG=mk(0.0), GV=mk(1.0),   # curva, revelação, ponto, tangente, visibilidade
            HX=mk(0.0), ER=mk(0.0),                        # destaque do ramo externo / linha E(R)
        )
        self.hl = None

        def c3():
            return np.array([T.CX.get_value(), T.CY.get_value(), 0.0])

        def rs():
            return T.RS.get_value()

        def sv():
            return T.SV.get_value()

        def far(x, a, b):
            """Some suavemente quando a gaussiana passa de a para b (não sai do quadro)."""
            return float(np.clip((b - x) / (b - a), 0, 1))

        # esfera: duas imagens (uniforme e gradiente) comandadas pelos mesmos trackers
        def img(kind, trk):
            m = ImageMobject(sphere_image(kind)).set_z_index(0)

            def up(mm_):
                mm_.set_width(2 * rs()).move_to(c3()).set_opacity(float(np.clip(trk.get_value() * sv(), 0, 1)))
            m.add_updater(up)
            up(m)
            return m
        self.img_u, self.img_g = img("uniform", T.UOP), img("grad", T.GOP)

        def outline():                                       # esfera física: contorno contínuo azul + equador
            o = T.OL.get_value() * sv() * max(T.UOP.get_value(), T.GOP.get_value())
            if o < 0.01:
                return VGroup()
            c, r = c3(), rs()
            g = VGroup(poly_mob(circ_pts(c[0], c[1], r), BLUE_L, 2.8, 0.9 * o),
                       poly_mob(ell_pts(c[0], c[1], r, PI, 2 * PI), BLUE_L, 1.4, 0.45 * o),
                       poly_mob(ell_pts(c[0], c[1], r, 0, PI), BLUE_L, 1.0, 0.18 * o))
            return g.set_z_index(1)
        self.outline = always_redraw(outline)

        def acc():                                           # região já integrada
            o = T.ACO.get_value() * sv()
            r = T.ACC.get_value() * rs()
            if o < 0.01 or r < 0.02:
                return VGroup()
            c = c3()
            return VGroup(Polygon(*circ_pts(c[0], c[1], r, n=90)[:-1]).set_fill(VIOLET, 0.16 * o).set_stroke(
                VIOLET, 2, 0.7 * o)).set_z_index(1)
        self.acc = always_redraw(acc)

        def shell():
            """r' (círculo + raio) e a casca entre r' e r'+dr', em CORTE: dois círculos e a faixa fina entre eles."""
            rl, sh = T.RL.get_value() * sv(), T.SH.get_value() * sv()
            if rl < 0.01 and sh < 0.01:
                return VGroup()
            c, r = c3(), rs()
            xp, dx = T.XP.get_value(), T.DX.get_value()
            r0 = max(xp * r, 0.03)
            out = VGroup()
            if rl > 0.01:
                u = np.array([np.cos(np.radians(40)), np.sin(np.radians(40)), 0.0])
                out.add(poly_mob(circ_pts(c[0], c[1], r0), WHITE, 2.4, 0.9 * rl),
                        Line(c, c + r0 * u).set_stroke(WHITE, 3, rl),
                        Dot(c, radius=0.05, color=WHITE).set_opacity(rl),
                        Dot(c + r0 * u, radius=0.07, color=WHITE).set_opacity(rl))
            if sh > 0.01:
                r1 = r0 + dx * r
                xm = xp + dx / 2
                alpha = (0.6 if T.SI.get_value() < 0.5 else 0.08 + 0.85 * rho_rel(xm)) * sh   # SI=1: brilho ∝ ρ
                an = Annulus(inner_radius=r0, outer_radius=r1).move_to(c)
                an.set_fill(WHITE, alpha).set_stroke(WHITE, 0, 0)
                out.add(an, poly_mob(circ_pts(c[0], c[1], r1), WHITE, 2.4, 0.95 * sh))
            return out.set_z_index(3)
        self.shell = always_redraw(shell)
        self.rlab = tex(r"r'", 34, WHITE)
        self.dlab = tex(r"dr'", 30, WHITE)
        self.dlab2 = tex(r"\Delta r", 32, WHITE)

        def lab_up(m, which):
            c, r = c3(), rs()
            xp, dx = T.XP.get_value(), T.DX.get_value()
            if which == "r":                                  # r' junto do raio a 40°
                a = np.radians(40)
                m.move_to(c + (max(xp, 0.05) * r * 0.55) * np.array([np.cos(a), np.sin(a), 0]) + np.array([-0.22, 0.2, 0]))
                m.set_opacity(T.RL.get_value() * sv())
            else:                                             # dr' / Δr fora da casca, a −35°
                a = np.radians(-35)
                m.move_to(c + ((xp + dx) * r + 0.3) * np.array([np.cos(a), np.sin(a), 0]))
                dl = T.DL.get_value()
                w = (1 - dl) if which == "d" else dl
                m.set_opacity(T.SH.get_value() * w * sv())
        self.rlab.add_updater(lambda m: lab_up(m, "r"))
        self.dlab.add_updater(lambda m: lab_up(m, "d"))
        self.dlab2.add_updater(lambda m: lab_up(m, "d2"))

        def gauss():                                         # superfície gaussiana (r = x R): tracejado violeta
            x = T.X.get_value()
            o = T.GA.get_value() * sv() * far(x, 1.3, 1.65)
            if o < 0.01:
                return VGroup()
            c, r = c3(), x * rs()
            if r < 0.03:
                return VGroup()
            phi = PI - (PI / 2) * sstep((x - 1.0) / 0.45)    # x > 1: só o arco voltado ao gráfico
            out = VGroup()
            gf = T.GF.get_value() * sv() * o
            if gf > 0.01 and x <= 1.0:
                out.add(Polygon(*circ_pts(c[0], c[1], r, n=90)[:-1]).set_fill(VIOLET, gf).set_stroke(VIOLET, 0, 0))
            out.add(dashed_ring(c[0], c[1], r, -phi, phi, VIOLET, 3.6, o))
            if x <= 1.05:
                out.add(poly_mob(ell_pts(c[0], c[1], r, PI, 2 * PI), VIOLET, 1.8, 0.6 * o),
                        poly_mob(ell_pts(c[0], c[1], r, 0, PI), VIOLET, 1.2, 0.22 * o))
            return out.set_z_index(2)
        self.gauss = always_redraw(gauss)

        def mark():                                          # marca radial: o mesmo x, dentro da esfera
            x = T.X.get_value()
            o = T.MK.get_value() * sv() * far(x, 1.15, 1.45)
            if o < 0.01:
                return VGroup()
            c, r = c3(), x * rs()
            tip = c + np.array([r, 0, 0])
            return VGroup(Line(c, tip).set_stroke(WHITE, 4, o),
                          Dot(c, radius=0.06, color=WHITE).set_opacity(o),
                          Dot(tip, radius=0.1, color=WHITE).set_opacity(o)).set_z_index(4)
        self.mark = always_redraw(mark)

        def arrows():
            """E⃗ (ciano) nasce sobre a gaussiana, mesmo módulo; d⃗A (lavanda, menor) ao lado, também radial."""
            x = T.X.get_value()
            base = T.FA.get_value() * sv() * far(x, 1.3, 1.65)
            c = c3()
            r = x * rs()
            out = VGroup()
            if r < 0.03:
                return out
            mode = T.FM.get_value()
            L = 0.5 if mode < 0.5 else (0.6 * x if mode < 1.5 else 6.5 * e(x))
            L *= T.FL.get_value()
            if base > 0.01 and L >= 0.06:
                for deg in E_ANGLES:
                    o = base * (1.0 if deg == 35 else T.FD.get_value())
                    u = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])
                    p0 = c + r * u
                    if p0[0] < -3.7 or p0[0] > 3.7 or p0[1] > 6.0:
                        continue
                    out.add(Arrow(p0, p0 + L * u, buff=0, stroke_width=4.5, tip_length=min(0.2, 0.45 * L),
                                  max_tip_length_to_length_ratio=0.5, color=CYAN).set_opacity(o))
            da = T.DA.get_value() * sv() * far(x, 1.3, 1.65)
            if da > 0.01:
                for deg in DA_ANGLES:
                    u = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])
                    p0 = c + r * u
                    out.add(Arrow(p0, p0 + 0.34 * u, buff=0, stroke_width=3.5, tip_length=0.15,
                                  max_tip_length_to_length_ratio=0.5, color=NCOL).set_opacity(da))
            return out.set_z_index(3)
        self.arrows = always_redraw(arrows)

        def patch():
            """Patch dA na gaussiana e normal n̂ (radial, para fora), no ponto destacado (35°)."""
            x = T.X.get_value()
            pa, nv = T.PA.get_value() * sv(), T.NV.get_value() * sv()
            c, r = c3(), x * rs()
            if r < 0.03 or (pa < 0.01 and nv < 0.01):
                return VGroup()
            u = np.array([np.cos(HA), np.sin(HA), 0.0])
            perp = np.array([-np.sin(HA), np.cos(HA), 0.0])
            out = VGroup()
            if pa > 0.01:
                out.add(poly_mob(circ_pts(c[0], c[1], r, HA - 0.16, HA + 0.16, 9), NCOL, 9, pa))
            if nv > 0.01:
                p0 = c + r * u + perp * 0.16
                out.add(Arrow(p0, p0 + 0.62 * u, buff=0, stroke_width=5, tip_length=0.2,
                              max_tip_length_to_length_ratio=0.5, color=NCOL).set_opacity(nv))
            return out.set_z_index(4)
        self.patch = always_redraw(patch)

        # rótulos que acompanham a gaussiana (r, dA, n̂, d⃗A, E⃗)
        self.lab_r = tex(r"r", 38, VIOLET)
        self.lab_dA = tex(r"dA", 34, NCOL)
        self.lab_n = tex(r"\hat n", 40, NCOL)
        self.lab_dAv = tex(r"d\vec A", 40, NCOL)
        self.lab_E = tex(r"\vec E", 40, CYAN)

        def lab_pos(kind):
            x = T.X.get_value()
            c, r = c3(), x * rs()
            u = np.array([np.cos(HA), np.sin(HA), 0.0])
            perp = np.array([-np.sin(HA), np.cos(HA), 0.0])
            if kind == "r":
                return c + np.array([r / 2, -0.3, 0.0])
            if kind == "dA":
                return c + (r - 0.5) * u - perp * 0.18
            if kind in ("n", "dAv"):
                return c + r * u + perp * 0.16 + u * 1.0 + perp * 0.62
            return c + r * u + u * 0.82 - perp * 0.62            # "E"

        def make_lab_updater(kind, trk):
            def up(m):
                m.move_to(lab_pos(kind)).set_opacity(float(trk.get_value()) * sv())
            return up
        for kind, lab, trk in (("r", self.lab_r, T.LR), ("dA", self.lab_dA, T.LD), ("n", self.lab_n, T.LN1),
                               ("dAv", self.lab_dAv, T.LN2), ("E", self.lab_E, T.LE)):
            lab.add_updater(make_lab_updater(kind, trk))

        # gráfico E(x): curva revelada até GE (RV: acompanha o maior x visitado), ponto e tangente
        def curve():
            if T.RV.get_value() > 0.5 and T.X.get_value() > T.GE.get_value():
                T.GE.set_value(T.X.get_value())
            ge = T.GE.get_value()
            gv = T.GV.get_value()
            if ge < 0.01 or gv < 0.01:
                return VGroup()
            xs = np.linspace(0, min(ge, 1.0), 120)
            if ge > 1:
                xs = np.concatenate([xs, np.linspace(1.0, ge, int(100 * (ge - 1)) + 2)[1:]])
            pts = np.array([gpt(x) for x in xs])
            out = VGroup(poly_mob(pts, CYAN, 6, gv))
            hx = T.HX.get_value()
            if hx > 0.01 and ge > 1:
                xo = xs[xs >= 1]
                out.add(poly_mob(np.array([gpt(x) for x in xo]), WHITE, 7.5, hx))
            return out.set_z_index(3)
        self.curve = always_redraw(curve)

        def dot():
            o = T.PT.get_value() * T.GV.get_value()
            if o < 0.01:
                return VGroup()
            p = gpt(T.X.get_value())
            return VGroup(Dot(p, radius=0.22, color=CYAN).set_opacity(0.28 * o),
                          Dot(p, radius=0.11, color=WHITE).set_opacity(o)).set_z_index(6)
        self.dot = always_redraw(dot)

        def tangent():
            o = T.TG.get_value()
            if o < 0.01:
                return VGroup()
            x = T.X.get_value()
            p = gpt(x)
            m = ep(x) * GSY / GSX
            d = np.array([1.0, m, 0.0]) / np.hypot(1.0, m)
            room = max(p[1] - GY0 - GTR.get_value() - 0.03, 0.0)   # a tangente não atravessa o eixo horizontal
            lo = min(0.9, room / abs(d[1])) if d[1] > 1e-9 else 0.9
            hi = min(0.9, room / abs(d[1])) if d[1] < -1e-9 else 0.9
            return VGroup(Line(p - lo * d, p + hi * d).set_stroke(WHITE, 4, o)).set_z_index(5)
        self.tangent = always_redraw(tangent)

        def e_r():                                           # nível E(R): o pico é só ~33% maior
            o = T.ER.get_value()
            if o < 0.01:
                return VGroup()
            return VGroup(DashedLine(gpt(0) + [0, GSY * e(1.0), 0], gpt(1.0), dash_length=0.1).set_stroke(
                BLUE_L, 2, 0.6 * o), Dot(gpt(1.0), radius=0.07, color=BLUE_L).set_opacity(o)).set_z_index(3)
        self.e_r = always_redraw(e_r)

        # eixos e rótulos do gráfico (estáticos, CENTRADOS no quadro; rótulos posicionados à parte; entram em S6)
        ax_top = GY0 + GSY * 0.13
        xa = Line([GX0, GY0, 0], [GX0 + GSX * XMAX, GY0, 0]).set_stroke(WHITE, 2.5, 0.8)
        ya = Line([GX0, GY0, 0], [GX0, ax_top, 0]).set_stroke(WHITE, 2.5, 0.8)
        ticks = VGroup(*[Line([GX0 + GSX * k, GY0, 0], [GX0 + GSX * k, GY0 - 0.1, 0]).set_stroke(WHITE, 2, 0.8)
                         for k in (1, 2, 3)])
        tlabs = VGroup(*[tex(str(k), 32).move_to([GX0 + GSX * k, GY0 - 0.34, 0]) for k in (1, 2, 3)])
        xlab = tex(r"x=r/R", 36, WHITE).move_to([GX0 + GSX * XMAX - 0.5, GY0 + 0.5, 0])
        ylab = tex(r"E/E_0", 36, CYAN).move_to([GX0 + 0.5, ax_top + 0.2, 0])
        e0lab = tex(r"E_0=\rho_0R/\varepsilon_0", 30, WHITE).set_opacity(0.85).move_to(
            [GX0 + 2.55, ax_top + 0.2, 0])
        self.axes = VGroup(xa, ya, xlab, ylab)
        self.ticks = VGroup(ticks, tlabs)
        self.e0lab = e0lab

        self.add(self.img_u, self.img_g, self.outline, self.acc, self.gauss, self.shell, self.rlab, self.dlab,
                 self.dlab2, self.mark, self.arrows, self.patch, self.lab_r, self.lab_dA, self.lab_n, self.lab_dAv,
                 self.lab_E, self.curve, self.e_r, self.tangent, self.dot)

    # ── Execução ────────────────────────────────────────────────────────────
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.toff = 0.0
        self.sync_init()
        self.build()
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35)
        self.add(self.wm.to_corner(UP + RIGHT, buff=0.28))
        self.series = text("EXERCÍCIO RESOLVIDO · EP. 05", 20, opacity=0.65).to_corner(UP + LEFT, buff=0.4)
        self.add(self.series)
        for k, seg in enumerate([self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8,
                                 self.s9, self.s10, self.s11, self.s12, self.s13, self.s14], 1):
            seg()
            if k >= ATE:
                self.wait(0.5)
                return
        self.wait(0.4)

    # ── S1 Caso uniforme e pergunta ─────────────────────────────────────────
    def s1(self):
        T = self.T
        hd = lines("O CAMPO MÁXIMO ESTÁ", "NA SUPERFÍCIE?", size=38).move_to([0, 6.15, 0])
        self.hl = hd
        self.ancora("s1a")
        self.play(T.UOP.animate.set_value(1), FadeIn(hd, shift=DOWN * 0.15), run_time=1.1)
        tg = text("ESFERA UNIFORMEMENTE CARREGADA", 22, opacity=0.8).move_to([0, -0.2, 0])
        e1 = Eq(r"E_{\rm dentro}", r"\propto", "r", size=62, colors={0: CYAN})
        self.place(e1, 0, -1.3)
        self.play(FadeIn(tg), FadeIn(e1.mob, shift=UP * 0.1), run_time=0.7)
        T.FM.set_value(1)
        self.ancora("s1b")
        self.play(T.MK.animate.set_value(1), T.FA.animate.set_value(1), T.GA.animate.set_value(1), run_time=0.5)
        cres = text("o campo cresce até a superfície", 26, CYAN).move_to([0, -2.5, 0])
        self.play(T.X.animate.set_value(1.0), FadeIn(cres), run_time=3.0, rate_func=linear)
        self.until(5.8)
        self.ancora("s1c")
        q = lines("E se a densidade diminuir", "com a distância?", size=28).move_to([0, -1.3, 0])
        self.play(T.UOP.animate.set_value(0), T.GOP.animate.set_value(1), T.FA.animate.set_value(0),
                  T.MK.animate.set_value(0), T.GA.animate.set_value(0),
                  AnimationGroup(FadeOut(VGroup(tg, e1.mob, cres)), FadeIn(q, shift=UP * 0.1), lag_ratio=0.85),
                  run_time=2.0)
        self.until(8.0)
        c = np.array([LA[0] + LA[2], LA[1], 0])
        self.ancora("s1d")
        ring = Circle(radius=0.3, color=VIOLET, stroke_width=4).move_to(c)
        lab = text("borda?", 24, VIOLET).move_to([2.7, 1.55, 0])
        self.play(FadeIn(ring), FadeIn(lab), Indicate(ring, color=VIOLET, scale_factor=1.35), run_time=1.1)
        self.until(9.5)
        self.s1_items = VGroup(q, ring, lab)

    # ── S2 ρ(r) e simetria ──────────────────────────────────────────────────
    def s2(self):
        T = self.T
        self.ancora("s2a")
        self.head("Densidade não uniforme")
        R0 = Eq(r"\rho(r)", "=", r"\rho_0", r"\left(1-\frac rR\right)", size=58, colors={0: MAGENTA, 2: MAGENTA})
        self.place(R0, 0, -0.65)
        cond = tex(r"0\le r\le R", 34).set_opacity(0.85).move_to([0, -1.85, 0])
        cx, cy, r = LA
        ll = tex(r"\rho=\rho_0", 36, MAGENTA).move_to([-2.85, cy, 0])
        rl = tex(r"\rho=0", 36, MAGENTA).move_to([2.85, cy, 0])
        lead = VGroup(Line([-2.15, cy, 0], [cx, cy, 0]).set_stroke(WHITE, 1.8, 0.6),
                      Dot([cx, cy, 0], radius=0.06, color=WHITE),
                      Line([2.15, cy, 0], [cx + r, cy, 0]).set_stroke(WHITE, 1.8, 0.6),
                      Dot([cx + r, cy, 0], radius=0.06, color=WHITE))
        self.play(FadeOut(self.s1_items), FadeIn(R0.mob, shift=UP * 0.1), FadeIn(cond), run_time=1.0)
        self.until(13.0)
        self.ancora("s2b")
        self.play(FadeIn(ll), FadeIn(rl), FadeIn(lead), run_time=1.0)
        self.until(16.0)
        # simetria: ρ só depende de r  =>  E é radial e de mesmo módulo a uma mesma distância (setas nascem na gaussiana)
        self.ancora("s2c")
        Sy = Eq(r"\rho=\rho(r)", r"\Rightarrow", r"\vec E=E(r)\,\hat r", size=50, colors={0: MAGENTA, 2: CYAN})
        self.place(Sy, 0, -0.65)
        T.FM.set_value(0)
        T.X.set_value(0.85)
        T.FL.set_value(0.0)
        tg = text("mesmo módulo a uma mesma distância r", 24, opacity=0.85).move_to([0, -1.85, 0])
        self.play(FadeOut(R0.mob), FadeOut(cond), FadeOut(ll), FadeOut(rl), FadeOut(lead),
                  FadeIn(Sy.mob, shift=UP * 0.1), FadeIn(tg), T.GA.animate.set_value(1), T.FA.animate.set_value(1),
                  run_time=1.2)
        self.play(T.FL.animate.set_value(1.0), run_time=1.0)
        self.until(20.5)
        self.s2_items = VGroup(Sy.mob, tg)

    # ── S3 Lei de Gauss, por geometria ──────────────────────────────────────
    def s3(self):
        T = self.T
        self.ancora("s3a")
        self.head("Lei de Gauss")
        TAG_Y = 0.15
        tag = text("superfície gaussiana, de raio r", 24, VIOLET).move_to([0, TAG_Y, 0])
        # esfera ampliada e centrada; a gaussiana (r < R) e o raio r
        self.play(*self.layout(LGA), T.X.animate.set_value(0.65), FadeOut(self.s2_items), T.MK.animate.set_value(1),
                  T.LR.animate.set_value(1), FadeIn(tag, shift=UP * 0.1), run_time=1.4)
        self.until(22.2)
        # E⃗ sobre a gaussiana: todos radiais e do mesmo comprimento
        self.ancora("s3b")
        tag2 = mixed(tex(r"\vec E", 34, CYAN), text("sobre a gaussiana: mesmo módulo", 24)).move_to(
            [0, TAG_Y, 0])
        self.play(soft_swap(tag, tag2), T.FL.animate.set_value(0.0), run_time=0.5)
        self.play(T.FL.animate.set_value(1.0), run_time=1.0)
        self.until(24.2)
        self.ancora("s3c")
        L1 = Eq(r"\oint", r"\vec E", r"\cdot", r"d\vec A", "=", r"\frac{Q_{\rm enc}}{\varepsilon_0}", size=52,
                colors={1: CYAN, 3: NCOL})
        self.place(L1, 0, -0.9)
        self.play(FadeIn(L1.mob, shift=UP * 0.1), run_time=0.9)
        # d⃗A: vetor área, perpendicular à superfície (4 amostras)
        tag3 = mixed(tex(r"d\vec A", 34, NCOL), text("vetor área: perpendicular à superfície", 24)).move_to([0, TAG_Y, 0])
        self.play(soft_swap(tag2, tag3), T.DA.animate.set_value(1), run_time=1.0)
        self.until(27.0)
        self.ancora("s3d")
        # um ponto: patch dA, normal n̂ e d⃗A = n̂ dA
        self.play(T.FD.animate.set_value(0.25), T.DA.animate.set_value(0.25), T.PA.animate.set_value(1),
                  T.LD.animate.set_value(1), FadeOut(tag3), run_time=1.0)
        self.play(T.NV.animate.set_value(1), T.LN1.animate.set_value(1), run_time=0.8)
        self.play(T.LE.animate.set_value(1), run_time=0.6)
        self.until(30.2)
        self.ancora("s3e")
        Tn = Eq(r"d\vec A", "=", r"\hat n", "dA", size=44, colors={0: NCOL, 2: NCOL, 3: NCOL})
        self.born(Tn, CG(L1.g(3), Tn.p(0), path_arc=-PI / 4), CG(list(self.lab_n[0]), Tn.p(2), path_arc=PI / 4),
                  CG(list(self.lab_dA[0]), Tn.p(3), path_arc=PI / 4), x=0, y=TAG_Y, rt=1.3, hold=0.1,
                  extra=[T.LN1.animate.set_value(0), T.LN2.animate.set_value(1)])
        self.until(31.8)
        self.ancora("s3f")
        par = mixed(tex(r"\vec E\parallel d\vec A", 36, WHITE), tex(r"\Rightarrow\ \theta=0", 36, WHITE), buff=0.4)
        par.move_to([0, TAG_Y, 0])
        self.play(soft_swap(Tn.mob, par), run_time=0.8)
        self.until(33.0)
        self.ancora("s3g")
        # E⃗·dA⃗ = E dA cos θ  ->  θ = 0, cos 0 = 1  ->  E dA
        P1 = Eq(r"\vec E", r"\cdot", r"d\vec A", "=", "E", "dA", r"\cos\theta", size=50,
                colors={0: CYAN, 2: NCOL, 4: CYAN, 5: NCOL})
        self.born(P1, CG(L1.g(1, 2, 3), P1.p(0, 1, 2), path_arc=PI / 6), x=0, y=-2.5, rt=1.2, hold=0.2)
        P2 = Eq(r"\vec E", r"\cdot", r"d\vec A", "=", "E", "dA", r"\cos 0", size=50,
                colors={0: CYAN, 2: NCOL, 4: CYAN, 5: NCOL})
        self.mm(P1, P2, M(P1, [0, 1, 2, 3, 4, 5], P2, [0, 1, 2, 3, 4, 5]), M(P1, [6], P2, [6]), rt=1.0, hold=0.3)
        P3 = Eq(r"\vec E", r"\cdot", r"d\vec A", "=", "E", "dA", size=50, colors={0: CYAN, 2: NCOL, 4: CYAN, 5: NCOL})
        c01 = tex(r"\cos 0=1", 36, WHITE).move_to([0, -3.55, 0])
        self.mm(P2, P3, M(P2, [0, 1, 2, 3, 4, 5], P3, [0, 1, 2, 3, 4, 5]), X(P2, [6], shift=DOWN * 0.25), rt=0.9,
                hold=0.1, extra=[FadeIn(c01, shift=UP * 0.1), FadeOut(par)])
        self.until(37.0)
        self.ancora("s3h")
        # a mesma situação em TODA a gaussiana: |E| = E(r), E ∥ dA
        tag4 = mixed(text("em toda a gaussiana:", 24), tex(r"\vec E\parallel d\vec A", 32), text("e", 24),
                     tex(r"|\vec E|=E(r)", 32), buff=0.2).move_to([0, TAG_Y, 0])
        self.play(T.FD.animate.set_value(1.0), T.DA.animate.set_value(1.0), T.PA.animate.set_value(0),
                  T.NV.animate.set_value(0), T.LD.animate.set_value(0), T.LN2.animate.set_value(0),
                  T.LE.animate.set_value(0), FadeIn(tag4, shift=UP * 0.1), FadeOut(c01), run_time=1.1)
        self.until(38.6)
        self.ancora("s3i")
        # ∮E⃗·dA⃗ -> ∮E dA -> E ∮dA -> E 4πr²
        L2 = Eq(r"\oint", "E", "dA", "=", r"\frac{Q_{\rm enc}}{\varepsilon_0}", size=52, colors={1: CYAN, 2: NCOL})
        self.mm(L1, L2, M(L1, [0], L2, [0]), M(L1, [4], L2, [3]), M(L1, [5], L2, [4]),
                X(L1, [1, 2, 3], shift=UP * 0.3), CG(P3.g(4, 5), L2.p(1, 2), path_arc=-PI / 4), y=-0.9, rt=1.4,
                hold=0.2, extra=[FadeOut(P3.mob)])
        L3 = Eq("E", r"\oint", "dA", "=", r"\frac{Q_{\rm enc}}{\varepsilon_0}", size=52, colors={0: CYAN, 2: NCOL})
        self.mm(L2, L3, M(L2, [1], L3, [0], path_arc=-PI / 3), M(L2, [0], L3, [1]), M(L2, [2], L3, [2]),
                M(L2, [3, 4], L3, [3, 4]), rt=1.2, hold=0.2)
        tag5 = mixed(tex(r"\oint dA", 36, NCOL), text("= área da esfera =", 24), tex(r"4\pi r^2", 36, VIOLET)).move_to(
            [0, TAG_Y, 0])
        L4 = Eq("E", r"4\pi r^2", "=", r"\frac{Q_{\rm enc}(r)}{\varepsilon_0}", size=56, colors={0: CYAN, 1: VIOLET})
        self.mm(L3, L4, M(L3, [0], L4, [0]), M(L3, [1, 2], L4, [1]), M(L3, [3], L4, [2]), M(L3, [4], L4, [3]),
                rt=1.5, hold=0.2, extra=[soft_swap(tag4, tag5), T.GF.animate.set_value(0.4)])
        self.G = L4
        self.until(44.0)
        self.ancora("s3k")
        num = L4.frac(3)[0]
        qg = VGroup(*[L4.mob[0][k] for k in num])
        self.play(T.GF.animate.set_value(0.13), FadeOut(tag5), T.LR.animate.set_value(0),
                  Indicate(qg, color=MAGENTA, scale_factor=1.2), run_time=1.0)
        qg.set_color(MAGENTA)
        self.until(48.0)

    # ── S4 Cascas: Q_enc = ∫ dQ, casca em corte, dV, dQ ─────────────────────
    def s4(self):
        T = self.T
        self.ancora("s4a")
        self.toff = -2.0
        self.head("Densidade variável: cascas")
        G = self.G
        rd = Eq(r"\rho(r)", "=", r"\rho_0", r"\left(1-\frac rR\right)", size=36, colors={0: MAGENTA, 2: MAGENTA})
        fit(rd.mob, 3.2).move_to([1.8, 4.75, 0])
        self.rd = rd
        T.XP.set_value(0.04)
        T.X.set_value(0.7)
        # PRIMARY_LEFT: a esfera vai para a esquerda enquanto a definição de ρ e a casca aberta estão à direita
        self.play(*self.layout(LP), G.mob.animate.scale(0.8).move_to([0, 1.5, 0]), T.FA.animate.set_value(0),
                  T.DA.animate.set_value(0), T.MK.animate.set_value(0), T.GF.animate.set_value(0),
                  FadeIn(rd.mob, shift=UP * 0.1), run_time=1.3)
        # Q_enc(r) do Gauss -> Q_enc(r) = ∫ dQ
        W0 = Eq(r"Q_{\rm enc}(r)", "=", r"\int_0^r", "dQ", size=52, colors={0: MAGENTA, 3: MAGENTA})
        gn = G.frac(3)[0]
        assert len(gn) == len(W0.p(0))
        self.born(W0, CG([G.mob[0][k] for k in gn], W0.p(0), path_arc=PI / 4), x=0, y=-0.2, rt=1.4, hold=0.1)
        self.W0 = W0
        self.until(52.2)
        self.ancora("s4b")
        nr = VGroup(tex("Q_{\\rm enc}\\neq", 36, MAGENTA), tex(r"\rho\,V", 36, MAGENTA)).arrange(RIGHT, buff=0.12)
        whyt = mixed(tex(r"\rho", 34, MAGENTA), text("varia com", 24), tex("r", 34, VIOLET))
        nr_g = VGroup(nr, whyt).arrange(DOWN, buff=0.12).move_to([0, -1.3, 0])
        self.play(FadeIn(nr_g, shift=UP * 0.1), run_time=0.7)
        self.until(53.6)
        self.ancora("s4c")
        # etapa A: r' cresce e seleciona uma casca (círculos r' e r'+dr', faixa fina entre eles)
        self.play(FadeOut(nr_g), T.RL.animate.set_value(1), run_time=0.5)
        self.play(T.XP.animate.set_value(0.5), run_time=1.3, rate_func=smooth)
        self.play(T.SH.animate.set_value(1), run_time=0.7)
        self.until(56.0)
        self.ancora("s4d")
        # etapa B: a casca se abre: área da casca × espessura  =>  dV
        slab = self._slab()
        self.play(GrowFromPoint(slab, np.array([-0.7, 3.9, 0.0])), run_time=0.9)
        dV = Eq("dV", "=", r"4\pi", r"r'^2", "dr'", size=52, colors={2: VIOLET, 3: VIOLET})
        self.place(dV, 0, -1.7)
        br = Brace(VGroup(*dV.g(2, 3)), DOWN, buff=0.1, color=VIOLET)
        br2 = Brace(VGroup(*dV.g(4)), DOWN, buff=0.1, color=WHITE)
        self.play(FadeIn(dV.mob, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(br), FadeIn(br2), run_time=0.5)
        self.until(58.4)
        self.ancora("s4e")
        # etapa C: dQ = ρ(r') dV; a casca aberta e as chaves saem (já foram entendidas)
        dQ0 = Eq("dQ", "=", r"\rho(r')", "dV", size=52, colors={0: MAGENTA, 2: MAGENTA})
        self.born(dQ0, CG(self.W0.g(3), dQ0.p(0)), CG(dV.g(0), dQ0.p(3)), x=0, y=-3.1, rt=1.3, hold=0.1,
                  extra=[FadeOut(slab), FadeOut(VGroup(br, br2))])
        dQ1 = Eq("dQ", "=", r"\rho(r')", r"4\pi", r"r'^2", "dr'", size=52, colors={0: MAGENTA, 2: MAGENTA})
        self.mm(dQ0, dQ1, M(dQ0, [0, 1, 2], dQ1, [0, 1, 2]), X(dQ0, [3], shift=UP * 0.3),
                CG(dV.g(2, 3, 4), dQ1.p(3, 4, 5)), rt=1.4, hold=0.2, extra=[FadeOut(dV.mob)])
        self.dQ1 = dQ1
        self.until(61.0)

    def _slab(self):
        """Casca aberta: área 4πr'² × espessura dr' (para ver por que dV = 4πr'² dr')."""
        top = Polygon([0.35, 3.0, 0], [2.55, 3.0, 0], [3.0, 3.5, 0], [0.8, 3.5, 0])
        top.set_fill(VIOLET, 0.55).set_stroke(VIOLET, 2, 1)
        front = Polygon([0.35, 3.0, 0], [2.55, 3.0, 0], [2.55, 2.78, 0], [0.35, 2.78, 0])
        front.set_fill(WHITE, 0.85).set_stroke(WHITE, 2, 1)
        side = Polygon([2.55, 3.0, 0], [3.0, 3.5, 0], [3.0, 3.28, 0], [2.55, 2.78, 0])
        side.set_fill(WHITE, 0.6).set_stroke(WHITE, 2, 1)
        a = tex(r"4\pi r'^2", 30, WHITE).move_to([1.7, 3.25, 0])
        d = tex(r"dr'", 30, WHITE).move_to([1.45, 2.45, 0])
        cap = text("casca aberta", 20, opacity=0.8).move_to([1.7, 3.85, 0])
        return VGroup(top, front, side, a, d, cap)

    # ── S5 Somando as cascas ────────────────────────────────────────────────
    def s5(self):
        T = self.T
        y = -0.2
        self.ancora("s5a")
        self.head("Somando as cascas")
        dQ1 = self.dQ1
        W1 = Eq(r"Q_{\rm enc}(r)", "=", r"\int_0^r", r"\rho(r')", r"4\pi", r"r'^2", "dr'", size=48,
                colors={0: MAGENTA, 3: MAGENTA})
        T.ACO.set_value(1)
        self.mm(self.W0, W1, M(self.W0, [0, 1, 2], W1, [0, 1, 2]), X(self.W0, [3], shift=UP * 0.3),
                CG(dQ1.g(2, 3, 4, 5), W1.p(3, 4, 5, 6)), y=y, rt=1.4, hold=0.0,
                extra=[FadeOut(dQ1.mob), T.XP.animate.set_value(0.04), T.ACC.animate.set_value(0.04 + DR0 / 2)])
        # integrar de 0 até r: a casca varre do centro até a gaussiana; a região já somada cresce
        W2 = Eq(r"Q_{\rm enc}(r)", "=", r"4\pi", r"\int_0^r", r"\rho(r')", r"r'^2", "dr'", size=48,
                colors={0: MAGENTA, 4: MAGENTA})
        self.mm(W1, W2, M(W1, [0, 1], W2, [0, 1]), M(W1, [4], W2, [2], path_arc=-PI / 3), M(W1, [2], W2, [3]),
                M(W1, [3], W2, [4]), M(W1, [5], W2, [5]), M(W1, [6], W2, [6]), rt=2.6, hold=0.0,
                extra=[T.XP.animate.set_value(0.58), T.ACC.animate.set_value(0.7)])
        self.until(64.2)
        self.ancora("s5b")
        # ρ(r') = ρ0 (1 − r'/R): vem da definição, que está ao lado da esfera
        W3 = Eq(r"Q_{\rm enc}(r)", "=", r"4\pi", r"\rho_0", r"\int_0^r", r"\left(1-\frac{r'}{R}\right)", r"r'^2", "dr'",
                size=48, colors={0: MAGENTA, 3: MAGENTA})
        rd = self.rd
        self.mm(W2, W3, M(W2, [0, 1, 2, 3], W3, [0, 1, 2, 4]), M(W2, [5], W3, [6]), M(W2, [6], W3, [7]),
                X(W2, [4], shift=UP * 0.3), CG(rd.g(2), W3.p(3), path_arc=PI / 4),
                CG(rd.g(3), W3.p(5), path_arc=PI / 4), rt=1.5, hold=0.15, extra=[FadeOut(rd.mob)])
        W4 = Eq(r"Q_{\rm enc}(r)", "=", r"4\pi", r"\rho_0", r"\int_0^r", r"\left(r'^2-\frac{r'^3}{R}\right)", "dr'",
                size=48, colors={0: MAGENTA, 3: MAGENTA})
        self.mm(W3, W4, M(W3, [0, 1, 2, 3, 4], W4, [0, 1, 2, 3, 4]), M(W3, [7], W4, [6]),
                M(W3, [5, 6], W4, [5]), rt=1.2, hold=0.1)
        self.ancora("s5c")
        W4b = Eq(r"Q_{\rm enc}(r)", "=", r"4\pi", r"\rho_0", r"\left[\frac{r'^3}{3}-\frac{r'^4}{4R}\right]_0^r",
                 size=48, colors={0: MAGENTA, 3: MAGENTA})
        self.mm(W4, W4b, M(W4, [0, 1, 2, 3], W4b, [0, 1, 2, 3]), M(W4, [5], W4b, [4]), X(W4, [4, 6], shift=DOWN * 0.2),
                rt=1.2, hold=0.1)
        W5 = Eq(r"Q_{\rm enc}(r)", "=", r"4\pi", r"\rho_0", r"\left(\frac{r^3}{3}-\frac{r^4}{4R}\right)", size=50,
                colors={0: MAGENTA, 3: MAGENTA})
        self.W5box = self.mm(W4b, W5, M(W4b, [0, 1, 2, 3], W5, [0, 1, 2, 3]), M(W4b, [4], W5, [4]), rt=1.2, hold=0.2,
                             box=True, extra=[T.ACO.animate.set_value(0.0), T.RL.animate.set_value(0),
                                              T.SH.animate.set_value(0)])
        self.W5 = W5
        self.until(69.0)

    # ── S6 Campo interno e nascimento do gráfico ───────────────────────────
    def s6(self):
        T = self.T
        self.ancora("s6a")
        self.head("Campo interno")
        G, W5 = self.G, self.W5
        A = Eq("E", r"4\pi r^2", "=", r"\frac{4\pi\rho_0}{\varepsilon_0}", r"\left(\frac{r^3}{3}-\frac{r^4}{4R}\right)",
               size=44, colors={0: CYAN})
        # o resultado volta ao Gauss: 4πρ0 e o parêntese saem de Q_enc(r) e substituem Q_enc(r) no numerador
        gn, gb, gd = G.frac(3)
        an, ab, ad = A.frac(3)
        self.mm(G, A, M(G, [0, 1, 2], A, [0, 1, 2]), MG([gb], [ab]), MG(gd, ad), MG(gn, [], shift=UP * 0.3),
                CG(W5.g(2, 3), an, path_arc=-PI / 5), CG(W5.g(4), A.p(4), path_arc=-PI / 5),
                y=1.5, rt=1.8, hold=0.2, extra=[FadeOut(self.W5box), T.GF.animate.set_value(0.13)])

        self.ancora("s6b")
        # cancelamento visível: 4π de ambos os lados e a divisão por r²
        def strike(*glyphs):
            grp = VGroup(*glyphs)
            return Line(grp.get_corner(DOWN + LEFT), grp.get_corner(UP + RIGHT), color=MAGENTA, stroke_width=5)
        s1 = strike(A.mob[0][1], A.mob[0][2])                                   # 4π (lado esquerdo)
        s2 = strike(A.mob[0][6], A.mob[0][7])                                   # 4π (numerador)
        dv = tex(r"\div\,4\pi r^2", 36, MAGENTA).move_to([0, 0.5, 0])
        self.play(Create(s1), Create(s2), FadeIn(dv, shift=UP * 0.1), run_time=0.8)
        self.wait(0.4)
        B = Eq(r"E_{\rm in}(r)", "=", r"\frac{\rho_0}{\varepsilon_0}", r"\left(\frac{r}{3}-\frac{r^2}{4R}\right)",
               size=48, colors={0: CYAN})
        # A: 0 E | 1-4 4πr² | 5 = | 6 '4' 7 π 8 ρ 9 0 10 barra 11 ε 12 0 | 13 ( 14 r 15 3(exp) 16 barra 17 3 18 − 19 r
        #    20 4(exp) 21 barra 22 4 23 R 24 )
        # B: 0 E 1 i 2 n 3 ( 4 r 5 ) | 6 = | 7 ρ 8 0 9 barra 10 ε 11 0 | 12 ( 13 r 14 barra 15 3 16 − 17 r 18 2(exp)
        #    19 barra 20 4 21 R 22 )
        moves = [MG([0], [0]), MG([5], [6]),
                 MG([8, 9, 10, 11, 12], [7, 8, 9, 10, 11]),
                 MG([13, 14, 16, 17, 18, 19, 21, 22, 23, 24], [12, 13, 14, 15, 16, 17, 19, 20, 21, 22]),
                 MG([20], [18]), MG([1, 2, 3, 4], [], shift=LEFT * 0.4), MG([6, 7], [], shift=UP * 0.3),
                 MG([15], [], shift=UP * 0.3)]
        # SPHERE_GRAPH: sem conteúdo lateral, a esfera volta ao centro; o gráfico (centrado) entra
        self.Bbox = self.mm(A, B, *moves, y=SLOT, rt=2.0, hold=0.3, box=True,
                            extra=[FadeOut(s1), FadeOut(s2), FadeOut(dv), *self.layout(LC)])
        self.B = B
        self.until(73.5)
        self.ancora("s6c")
        # gráfico: a curva nasce enquanto o mesmo x percorre a esfera
        T.X.set_value(0.0)
        T.RV.set_value(1.0)
        self.play(FadeIn(self.axes), FadeIn(self.ticks), FadeIn(self.e0lab), run_time=0.7)
        T.PT.set_value(1.0)
        T.GA.set_value(1.0)
        T.MK.set_value(1.0)
        T.FM.set_value(2)
        self.play(T.X.animate.set_value(1.0), run_time=4.0, rate_func=linear)
        self.until(81.0)

    # ── S7 r = R, carga total e campo externo ───────────────────────────────
    def s7(self):
        T = self.T
        self.ancora("s7a")
        self.head("r = R: toda a carga está dentro")
        Bg, B = self.Bbox, self.B
        rect = Bg[1]
        self.remove(Bg)
        self.add(B.mob, rect)
        ring = Circle(radius=0.24, color=WHITE, stroke_width=4).move_to(gpt(1.0))
        # E_in vira um rótulo do ramo interno; a gaussiana coincide com a superfície; o ponto chega à fronteira
        self.play(FadeOut(rect), B.mob.animate.set_width(3.3).move_to([1.35, -0.95, 0]),
                  FadeIn(ring), T.GF.animate.set_value(0.35), run_time=1.0)
        self.play(Indicate(ring, color=WHITE, scale_factor=1.4), T.GF.animate.set_value(0.13), run_time=0.8)
        self.ancora("s7b")
        Q0 = Eq("Q", "=", r"Q_{\rm enc}(R)", "=", r"\frac{\pi\rho_0R^3}{3}", size=50, colors={0: MAGENTA, 2: MAGENTA})
        self.show(Q0, 0, SLOT, run_time=0.9)
        self.until(86.2)
        self.ancora("s7d")
        Q1 = Eq("Q", "=", r"\frac{\pi\rho_0R^3}{3}", size=54, colors={0: MAGENTA})
        self.mm(Q0, Q1, M(Q0, [0, 1], Q1, [0, 1]), M(Q0, [4], Q1, [2]), X(Q0, [2, 3], shift=UP * 0.2),
                rt=1.1, hold=0.3, extra=[FadeOut(ring)])
        self.head("Fora da esfera")
        # E_in(r) vira E_out(r): o mesmo campo, outro regime; Q vem de πρ0R³/3
        Eo = Eq(r"E_{\rm out}(r)", "=", r"\frac{Q}{4\pi\varepsilon_0 r^2}", size=52, colors={0: CYAN})
        self.born(Eo, CG(B.g(0), Eo.p(0), path_arc=-PI / 4), x=0, y=SLOT, rt=1.3, hold=0.1,
                  extra=[FadeOut(Q1.mob), T.X.animate.set_value(1.25)])
        Eo2 = Eq(r"E_{\rm out}(r)", "=", r"\frac{\rho_0R^3}{12\varepsilon_0 r^2}", size=52, colors={0: CYAN})
        self.mm(Eo, Eo2, M(Eo, [0, 1], Eo2, [0, 1]), rt=1.1, hold=0.15)
        self.Eo2 = Eo2
        self.until(89.8)
        self.ancora("s7c")
        # o ponto continua pelo ramo externo (sem salto); E_out vira rótulo do ramo externo
        self.play(T.X.animate.set_value(XMAX), run_time=3.2, rate_func=smooth)
        self.play(Eo2.mob.animate.set_width(3.0).move_to([1.35, -1.95, 0]), run_time=0.8)
        self.until(94.5)

    # ── S8 Virada: função por partes ────────────────────────────────────────
    def s8(self):
        T = self.T
        self.ancora("s8a")
        self.head("O campo em todo o espaço")
        B, Eo2 = self.B, self.Eo2
        row1, row2 = B.mob, Eo2.mob
        pre = tex("E(r)=", 36, WHITE)
        cond1 = tex(r"0\le r\le R", 26, WHITE).move_to([2.7, 3.55, 0])
        cond2 = tex(r"r\ge R", 26, WHITE).move_to([2.7, 2.45, 0])
        # MATH_FOCUS: as duas expressões já existentes viajam e formam a função por partes; a esfera encolhe
        self.play(*self.layout(LM), row1.animate.set_width(3.8).move_to([-2.2 + 1.9, 3.55, 0]),
                  row2.animate.set_width(3.0).move_to([-2.2 + 1.5, 2.45, 0]), run_time=1.4)
        brc = Brace(VGroup(row1, row2), LEFT, buff=0.1, color=WHITE)
        pre.next_to(brc, LEFT, buff=0.1)
        self.play(FadeIn(brc), FadeIn(pre), FadeIn(cond1), FadeIn(cond2), run_time=0.8)
        self.pw = VGroup(brc, pre, cond1, cond2)
        self.until(98.0)
        m1 = display("Encontramos o campo.", 28).move_to([0, 1.3, 0])
        m2 = display("Mas o exercício ainda não acabou.", 28).set_color(CYAN).move_to([0, 0.6, 0])
        self.play(FadeIn(m1, shift=UP * 0.1), run_time=0.7)
        self.until(100.0)
        self.ancora("s8b")
        self.play(FadeIn(m2, shift=UP * 0.1), run_time=0.8)
        self.until(103.0)
        self.s8_items = VGroup(m1, m2)

    # ── S9 Derivada passo a passo, tangente e resolução ────────────────────
    def s9(self):
        T = self.T
        self.ancora("s9a")
        self.head("Onde o campo é máximo?")
        B, Eo2 = self.B, self.Eo2
        row1 = B.mob
        # fora: só diminui; dentro: o ponto volta pelo ramo interno
        out = mixed(tex(r"E_{\rm out}\propto\frac{1}{r^2}", 34, WHITE), text("só diminui", 24)).move_to([0, 1.2, 0])
        self.play(FadeOut(self.s8_items), FadeIn(out, shift=UP * 0.1), T.HX.animate.set_value(1),
                  *self.gshift(-0.5, e0=0.0), run_time=0.9)
        self.until(105.5)
        self.ancora("s9b")
        self.play(FadeOut(self.pw), FadeOut(Eo2.mob), FadeOut(out), T.HX.animate.set_value(0),
                  row1.animate.set_width(4.4).move_to([0.6, 5.3, 0]), T.X.animate.set_value(0.12),
                  T.TG.animate.set_value(1), run_time=1.8)
        self.ancora("s9c")
        # dE/dr termo a termo; o prefator ρ0/ε0 vem de E_in
        DY = 3.55
        D0 = Eq(r"\frac{dE}{dr}", "=", r"\frac{\rho_0}{\varepsilon_0}", r"\Bigl[", r"\frac{d}{dr}\frac r3", "-",
                r"\frac{d}{dr}\frac{r^2}{4R}", r"\Bigr]", size=42, colors={0: CYAN})
        self.born(D0, CG(B.g(2), D0.p(2), path_arc=-PI / 4), x=0, y=DY, rt=1.2, hold=0.35)
        self.ancora("s9d")
        D1 = Eq(r"\frac{dE}{dr}", "=", r"\frac{\rho_0}{\varepsilon_0}", r"\Bigl[", r"\frac13", "-", r"\frac{2r}{4R}",
                r"\Bigr]", size=42, colors={0: CYAN})
        self.mm(D0, D1, M(D0, [0, 1, 2, 3, 5, 7], D1, [0, 1, 2, 3, 5, 7]), M(D0, [4], D1, [4]), M(D0, [6], D1, [6]),
                rt=1.2, hold=0.35)
        self.ancora("s9e")
        D2 = Eq(r"\frac{dE}{dr}", "=", r"\frac{\rho_0}{\varepsilon_0}", r"\Bigl(", r"\frac13", "-", r"\frac{r}{2R}",
                r"\Bigr)", size=42, colors={0: CYAN})
        self.mm(D1, D2, M(D1, [0, 1, 2, 4, 5], D2, [0, 1, 2, 4, 5]), M(D1, [3], D2, [3]), M(D1, [7], D2, [7]),
                M(D1, [6], D2, [6]), rt=1.1, hold=0.2)
        self.until(111.5)
        self.ancora("s9f")
        # tangente dinâmica: inclinação positiva, diminuindo, até o pico
        Z0 = Eq(r"\frac{dE}{dr}", ">", "0", size=44, colors={0: CYAN})
        self.place(Z0, 0.4, 2.3)
        self.play(FadeIn(Z0.mob, shift=UP * 0.1), run_time=0.6)
        self.play(T.X.animate.set_value(XM), run_time=4.0, rate_func=smooth)
        self.ancora("s9g")
        Z1 = Eq(r"\frac{dE}{dr}", "=", "0", size=44, colors={0: CYAN})
        self.Z = self.mm(Z0, Z1, M(Z0, [0, 2], Z1, [0, 2]), M(Z0, [1], Z1, [1]), rt=0.8, hold=0.1, box=True)
        self.until(117.2)
        self.ancora("s9h")
        # resolver: ρ0/ε0 > 0, logo só resta a condição sobre o parêntese
        S1 = Eq(r"\frac{\rho_0}{\varepsilon_0}", r"\Bigl(", r"\frac13", "-", r"\frac{r}{2R}", r"\Bigr)", "=", "0",
                size=44)
        self.born(S1, CG(D2.g(2, 3, 4, 5, 6, 7), S1.p(0, 1, 2, 3, 4, 5)), x=0.4, y=0.5, rt=1.0, hold=0.3)
        note = tex(r"\frac{\rho_0}{\varepsilon_0}>0", 28, WHITE).move_to([0.4, -0.38, 0])
        S2 = Eq(r"\frac13", "-", r"\frac{r}{2R}", "=", "0", size=46)
        self.mm(S1, S2, M(S1, [2, 3, 4], S2, [0, 1, 2]), M(S1, [6, 7], S2, [3, 4]), X(S1, [0, 1, 5], shift=UP * 0.3),
                rt=1.1, hold=0.2, extra=[FadeIn(note, shift=UP * 0.1)])
        self.ancora("s9i")
        S3 = Eq(r"\frac13", "=", r"\frac{r}{2R}", size=48)
        self.mm(S2, S3, M(S2, [0], S3, [0]), M(S2, [1], S3, [1]), M(S2, [2], S3, [2]), X(S2, [3, 4]), rt=1.0, hold=0.2,
                extra=[FadeOut(note)])
        S4 = Eq("3r", "=", "2R", size=50)
        # S3: 0 '1' 1 barra 2 '3' 3 '=' 4 r 5 barra 6 '2' 7 R | S4: 0 '3' 1 r 2 '=' 3 '2' 4 R
        self.mm(S3, S4, MG([2], [0]), MG([4], [1]), MG([3], [2]), MG([6, 7], [3, 4]), MG([0, 1, 5], [], shift=UP * 0.3),
                rt=1.0, hold=0.2)
        self.ancora("s9j")
        R2 = Eq("r", "=", r"\frac{2R}{3}", size=50, colors={0: VIOLET})
        # R2: 0 r 1 '=' 2 '2' 3 R 4 barra 5 '3'
        self.mm(S4, R2, MG([1], [0]), MG([2], [1]), MG([3, 4], [2, 3]), MG([0], [5]), rt=1.2, hold=0.2)
        self.R2 = R2
        self.until(123.0)
        self.s9_items = VGroup(row1, D2.mob, self.Z)

    # ── S10 Payoff: r_max = 2R/3 ────────────────────────────────────────────
    def s10(self):
        T = self.T
        self.ancora("s10a")
        self.head("Máximo do campo")
        T.FM.set_value(2)
        T.FL.set_value(0.0)
        pbox = Eq(r"r_{\max}", "=", r"\frac{2R}{3}", size=70, colors={0: VIOLET})
        # SPHERE_GRAPH: a esfera volta ao centro; gaussiana, marca radial e ponto já estão juntos em x = 2/3
        self.play(FadeOut(self.s9_items), *self.layout(LC), T.GA.animate.set_value(1), T.MK.animate.set_value(1),
                  T.FA.animate.set_value(1), T.GF.animate.set_value(0.1), *self.gshift(0.5, e0=0.85), run_time=1.3)
        self.play(T.FL.animate.set_value(1.0), run_time=0.7)
        assert abs(T.X.get_value() - XM) < 1e-9
        self.ancora("s10b")
        pk = gpt(XM)
        ring = Circle(radius=0.3, color=WHITE, stroke_width=4).move_to(pk)
        drop = DashedLine(pk, [pk[0], GY0, 0], dash_length=0.1).set_stroke(WHITE, 2.5, 0.8)
        tl = tex(r"\tfrac{2}{3}", 38, WHITE).move_to([pk[0], GY0 - 0.38, 0])
        self.pb = self.mm(self.R2, pbox, M(self.R2, [0], pbox, [0]), M(self.R2, [1], pbox, [1]),
                          M(self.R2, [2], pbox, [2]), x=0, y=SLOT, rt=1.3, hold=0.0, box=True,
                          extra=[T.ER.animate.set_value(1), FadeIn(ring), Create(drop), FadeIn(tl)])
        self.play(Indicate(ring, color=WHITE, scale_factor=1.35), run_time=0.9)
        self.until(132.0)
        self.wait(1.5)                    # o payoff respira, sem animação concorrente
        self.s10_items = VGroup(ring, drop, tl)

    # ── S11 Interpretação: o mesmo Δr perto do centro e perto da borda ─────
    def s11(self):
        T = self.T
        self.ancora("s11a")
        self.toff = -0.5                  # +1,5 s de respiro depois do payoff (as marcas de S11 acompanham)
        self.head("Por que o máximo fica dentro?")
        eqI = Eq("E", "=", r"\frac{Q_{\rm enc}(r)}{4\pi\varepsilon_0\,r^2}", size=50, colors={0: CYAN})
        self.place(eqI, 0, 1.4)
        T.XP.set_value(0.12)
        T.DX.set_value(0.18)
        T.SI.set_value(1.0)
        T.DL.set_value(1.0)
        T.GF.set_value(0.13)
        YA, YB = 0.52, -0.05               # duas linhas com espaçamento confortável, acima do gráfico deslocado

        def pair(a, b):
            return VGroup(a.move_to([0, YA, 0]), b.move_to([0, YB, 0]))
        a1 = mixed(text("Perto do centro:", 22, MAGENTA), tex(r"\rho", 27, MAGENTA), text("é grande", 22, MAGENTA))
        b1 = mixed(tex(r"Q_{\rm enc}", 27, MAGENTA), text("cresce rápido o suficiente →", 20), tex("E", 29, CYAN),
                   text("aumenta", 20, CYAN), buff=0.12)
        st1 = pair(a1, b1)
        self.ancora("s11b")
        # o gráfico desce (só horizontalmente centrado), abrindo espaço para as frases
        self.play(FadeOut(self.pb), FadeIn(eqI.mob, shift=UP * 0.1), FadeOut(self.s10_items),
                  T.ER.animate.set_value(0), T.TG.animate.set_value(0), T.X.animate.set_value(0.12),
                  T.FL.animate.set_value(0.55), *self.gshift(-0.75, e0=0.85, tk=0.0), run_time=1.3)
        self.until(136.0)
        self.ancora("s11c")
        # mesmo Δr perto do centro: a casca nova é brilhante (ρ alta); a gaussiana cresce; o ponto sobe
        self.play(T.SH.animate.set_value(1), FadeIn(st1, shift=UP * 0.1), run_time=0.7)
        self.play(T.X.animate.set_value(0.30), run_time=2.4, rate_func=smooth)
        self.until(142.0)
        self.ancora("s11d")
        a2 = mixed(text("Perto da borda:", 22, MAGENTA), tex(r"\rho", 27, MAGENTA), text("já é pequena", 22, MAGENTA))
        b2 = mixed(tex(r"Q_{\rm enc}", 27, MAGENTA), text("cresce devagar demais →", 20), tex("E", 29, CYAN),
                   text("diminui", 20, CYAN), buff=0.12)
        st2 = pair(a2, b2)
        self.play(T.SH.animate.set_value(0), FadeOut(st1, shift=UP * 0.1), run_time=0.5)
        T.XP.set_value(0.78)
        self.play(T.X.animate.set_value(0.78), run_time=1.0)
        self.ancora("s11e")
        # mesmo Δr perto da borda: ρ ≈ 0, casca nova fraca; a gaussiana segue crescendo; o ponto desce
        self.play(T.SH.animate.set_value(1), FadeIn(st2, shift=UP * 0.1), run_time=0.6)
        self.play(T.X.animate.set_value(0.96), run_time=2.4, rate_func=smooth)
        self.until(149.0)
        self.ancora("s11f")
        num, bar, den = eqI.frac(2)
        qn = VGroup(*[eqI.mob[0][k] for k in num])
        r2 = VGroup(*[eqI.mob[0][k] for k in den])
        self.play(Indicate(qn, color=MAGENTA, scale_factor=1.15), Indicate(r2, color=VIOLET, scale_factor=1.15),
                  run_time=1.2)
        self.until(152.0)
        self.s11_items = VGroup(eqI.mob, st2)

    # ── S12 Checagens, no mesmo gráfico ─────────────────────────────────────
    def s12(self):
        T = self.T
        self.ancora("s12a")
        self.head("Checagens")
        # o gráfico volta à posição de repouso; sai o texto da interpretação
        self.play(FadeOut(self.s11_items), T.SH.animate.set_value(0), T.FL.animate.set_value(1.0),
                  *self.gshift(0.75, e0=0.85, tk=1.0), run_time=0.7)
        CY_ = SLOT
        r0 = Circle(radius=0.22, color=WHITE, stroke_width=4).move_to(gpt(0.0))
        c1 = tex(r"E(0)=0", 40, WHITE).move_to([0, CY_, 0])
        self.ancora("s12b")
        self.play(T.X.animate.set_value(0.0), FadeIn(r0), FadeIn(c1, shift=UP * 0.1), run_time=1.2)
        self.wait(0.4)
        self.ancora("s12c")
        r1 = Circle(radius=0.24, color=WHITE, stroke_width=4).move_to(gpt(1.0))
        c2 = tex(r"E(R^-)=E(R^+)", 40, WHITE).move_to([0, CY_, 0])
        self.play(FadeOut(r0), T.X.animate.set_value(1.0), FadeIn(r1), soft_swap(c1, c2), run_time=1.3)
        self.wait(0.4)
        self.ancora("s12d")
        c3 = tex(r"E(r)\to0", 40, WHITE).move_to([0, CY_, 0])
        self.play(FadeOut(r1), T.X.animate.set_value(XMAX), soft_swap(c2, c3), run_time=1.4)
        self.wait(0.5)
        self.c3 = c3

    # ── S13 Resumo: a lógica da resolução ───────────────────────────────────
    def s13(self):
        T = self.T
        self.ancora("s13a")
        self.head("A lógica da resolução")

        def node(mob, color=WHITE, buff=0.22):
            return VGroup(mob, boxed_rect(mob, color, buff))
        g1 = node(text("GAUSS", 38, WHITE))
        g2 = node(tex(r"Q_{\rm enc}(r)", 46, MAGENTA), MAGENTA)
        g3 = node(tex(r"E(r)", 58, CYAN), CYAN)
        ar1, ar2 = tex(r"\rightarrow", 44, WHITE), tex(r"\rightarrow", 44, WHITE)
        row1 = VGroup(g1, ar1, g2, ar2, g3).arrange(RIGHT, buff=0.14)
        fit(row1, 6.6).move_to([0, 3.55, 0])
        g4 = node(tex(r"\frac{dE}{dr}=0", 60, CYAN), CYAN, 0.25).move_to([0, 1.45, 0])
        m5 = tex(r"r_{\max}=\frac{2R}{3}", 72, VIOLET)
        g5 = node(m5, WHITE, 0.3).move_to([0, -1.0, 0])
        glow = SurroundingRectangle(m5, color=CYAN, buff=0.42, corner_radius=0.16, stroke_width=9).set_stroke(
            CYAN, 9, 0.28).move_to(g5)
        a34 = Arrow(g3.get_bottom() + DOWN * 0.05, g4.get_top() + RIGHT * 0.5 + UP * 0.05, buff=0.05, stroke_width=4,
                    color=WHITE, tip_length=0.2, max_tip_length_to_length_ratio=0.5)
        a45 = Arrow(g4.get_bottom() + DOWN * 0.05, g5.get_top() + UP * 0.05, buff=0.05, stroke_width=4, color=WHITE,
                    tip_length=0.2, max_tip_length_to_length_ratio=0.5)
        # a esfera, o gráfico e a conta saem; o caminho é recapitulado passo a passo
        self.play(FadeOut(self.axes), FadeOut(self.ticks), FadeOut(self.e0lab), T.GV.animate.set_value(0), T.SV.animate.set_value(0), FadeOut(self.c3),
                  run_time=0.7)
        self.play(FadeIn(g1, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(ar1), FadeIn(g2, shift=RIGHT * 0.1), run_time=0.5)
        self.ancora("s13b")
        self.play(FadeIn(ar2), FadeIn(g3, shift=RIGHT * 0.1), run_time=0.5)
        self.ancora("s13c")
        self.play(Create(a34), FadeIn(g4, shift=UP * 0.1), run_time=0.6)
        self.play(Create(a45), FadeIn(g5, shift=UP * 0.1), FadeIn(glow), run_time=0.7)
        self.play(Indicate(g5, color=CYAN, scale_factor=1.05), run_time=0.7)
        self.wait(0.4)
        self.ancora("s13d")
        f1 = display("A distribuição de carga muda", 32).move_to([0, -3.25, 0])
        f2 = display("onde o campo é mais intenso.", 32).set_color(CYAN).move_to([0, -3.9, 0])
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(f2, shift=UP * 0.1), run_time=0.7)
        self.wait(2.0)
        self.s13_items = VGroup(g1, ar1, g2, ar2, g3, g4, g5, glow, a34, a45, f1, f2)

    # ── S14 CTA ─────────────────────────────────────────────────────────────
    def s14(self):
        self.ancora("s14a")
        im = Image.open(WATERMARK_PATH.parent / "parallax_lab_logo_horizontal.png").convert("RGBA")
        arr = np.array(im)
        ys, xs = np.where(arr[..., 3] > 40)
        logo = ImageMobject(arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).set_width(5.2).move_to([0, 2.6, 0])
        t1 = display("Se curtiu,", 44).move_to([0, 0.35, 0])
        h1 = display("segue", 42)
        h2 = display("@labparallax", 56).set_color_by_gradient(CYAN, BLUE_L)
        line2 = VGroup(h1, h2).arrange(RIGHT, buff=0.3).move_to([0, -0.7, 0])
        # transição curta: a matemática sai, o branding entra
        self.play(FadeOut(self.s13_items), FadeOut(self.hl), FadeOut(self.series), FadeOut(self.wm),
                  FadeIn(logo), run_time=0.8)
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(line2, shift=UP * 0.1), run_time=0.6)
        self.wait(2.0)
        self.ancora("fim")
        self.esperar_cru(0.6)             # o handle fica visível um instante depois da fala
