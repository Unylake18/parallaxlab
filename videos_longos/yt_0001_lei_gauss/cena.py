"""yt_0001 — Lei de Gauss: o segredo não é a integral — é a simetria. Preview horizontal, revisão 2 (sem voz).

Fonte de verdade: ficha.md desta pasta (narração, storyboard e equações). Revisão 2: construção da normal e do
vetor área, retomada das coordenadas esféricas, uma operação por transformação, domínios das fórmulas, regiões
que contribuem nas simetrias clássicas, carga envolvida (Q_env), caminhos alternativos e tela final.

Uma única cena contínua (`LeiGauss`), dividida em seções (blocos):
  01 cold open · 02 intro · 03 normal, vetor área e fluxo · 04 Coulomb + cancelamento 1/r² × r²
  05 ângulo sólido, interna × externa, Q_env · 06 superfície ruim (carga deslocada) · 07 simetria da fonte
  08 esfera uniforme (interior, coordenadas esféricas, dV, exterior) · 09 gráfico sincronizado
  10 três simetrias · 11 casos ruins, caminhos adequados e método · 12 retorno, payoff, pausa e outro

Ritmo sem voz: cada bloco declara as falas da ficha que cobre (`cues`); o instante de cada fala sai da contagem
de palavras (RATE palavras/s + GAP entre falas). Ao importar, a cena verifica que toda fala existe literalmente
na seção 12 da ficha — narração e animação não divergem. A voz real definirá a sincronia final.

Gramática visual (ficha, seção 14): ciano = E⃗, θ e E nas equações · azul (contorno contínuo + preenchimento) =
distribuição física, R, Q · violeta tracejado = superfície gaussiana e r (traço contínuo = região que contribui) ·
violeta translúcido = volume envolvido · branco = n̂ (fino) e d⃗A (grosso, translúcido) e matemática neutra ·
magenta = passo inválido ou componente hipotética. Ângulos: θ (E⃗, n̂) no fluxo; ϑ polar nas coordenadas.

Preview:  uv run --no-sync python -m manim -r 960,540 --fps 15 --disable_caching videos_longos/yt_0001_lei_gauss/cena.py LeiGauss
SO=6 (ou SO=6,8) renderiza só esses blocos (os outros rodam sem gerar quadros). GUIAS=1 mostra a safe area.
"""

import os
import sys
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from manim import (
    BOLD, DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, UL, UP, UR, Arc, Arrow, Axes, Brace, Circle, Circumscribe, Create,
    DashedLine, DashedVMobject, DecimalNumber, Dot, Ellipse, FadeIn, FadeOut, Flash, GrowArrow, ImageMobject,
    Indicate, LaggedStart, Line, MathTex, Polygon, Rectangle, ReplacementTransform, Rotate, Scene,
    SurroundingRectangle, Transform, TransformFromCopy, TransformMatchingTex, ValueTracker, VGroup, VMobject, Write,
    always_redraw, config, linear,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import DISPLAY_FONT, official_text, screen_text  # noqa: E402
from template.layout_horizontal import GUIAS, safe_guides, split  # noqa: E402

PASTA = Path(__file__).resolve().parent
SO = {int(s) for s in os.environ.get("SO", "").split(",") if s.strip()}
LOGO_PATH = Path(__file__).resolve().parents[2] / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"

# ── Paleta (identidade vigente; mesmos tons do vid_0012) ─────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # campo elétrico, θ, E
BLUE = "#267BFF"          # distribuição física (preenchimento)
BLUE_L = "#7FB2FF"        # contorno da distribuição física, R, Q
VIOLET = "#9C8CFF"        # superfície gaussiana, r, volume envolvido
MAGENTA = "#EA63FF"       # passo inválido / componente hipotética
NCOL = WHITE              # n̂ e d⃗A (ficha, seção 14)

# ── Composição (frame 16 × 9; template/layout_horizontal.py) ────────────────
_L, _R = split(0.5)
LX, RX, MY = _L.x, _R.x, _L.y      # ≈ −3.75, 3.75, −0.2

# ── Ritmo: falas da ficha → instantes ───────────────────────────────────────
RATE, GAP = 2.45, 0.15             # palavras por segundo; respiro entre falas
_NARR = " ".join((PASTA / "ficha.md").read_text(encoding="utf-8")
                 .split("## 12. NARRAÇÃO FINAL")[1].split("## 13.")[0].split())


def cues(*falas):
    """Instantes (s, relativos ao bloco) de início de cada fala; o último é o fim da última fala."""
    t, out = 0.0, []
    for f in falas:
        f = " ".join(f.split())
        assert f in _NARR, "fala ausente da ficha: " + f[:70]
        out.append(round(t, 2))
        t += len(f.split()) / RATE + GAP
    out.append(round(t, 2))
    return out


# ── Física: verificações independentes do que a tela afirma ─────────────────
def f_graph(x):
    """E(r)/E(R) com x = r/R: linear dentro, 1/x² fora."""
    return x if x <= 1 else 1 / (x * x)


def _qa():
    rho, R, eps = 3.1e-6, 0.42, 8.854e-12
    e_in = lambda r: rho * r / (3 * eps)
    e_out = lambda r: rho * R ** 3 / (3 * eps * r * r)
    Q = 4 / 3 * np.pi * R ** 3 * rho
    # Q_env = ρ ∫r'² dr' ∫ sinϑ dϑ ∫ dφ = ρ · r³/3 · 2 · 2π = 4/3 π ρ r³ (somas de Riemann independentes)
    for r in (0.2 * R, 0.7 * R, R):
        n = 200000
        rp = (np.arange(n) + 0.5) * r / n
        th = (np.arange(n) + 0.5) * np.pi / n
        i_r, i_t, i_f = np.sum(rp ** 2) * r / n, np.sum(np.sin(th)) * np.pi / n, 2 * np.pi
        assert np.isclose(i_r, r ** 3 / 3) and np.isclose(i_t, 2.0)
        q = rho * i_r * i_t * i_f
        assert np.isclose(q, 4 / 3 * np.pi * rho * r ** 3, rtol=1e-6)
        # passos da tela: E 4πr² = (1/3ε0) 4π ρ r³ → E r² = ρ r³ / 3ε0 → E = ρ r / 3ε0
        assert np.isclose(q / eps, 4 * np.pi * rho * r ** 3 / (3 * eps))
        assert np.isclose(q / (eps * 4 * np.pi * r * r), e_in(r), rtol=1e-6)
    for r in (1.0 * R, 1.8 * R, 30 * R):
        assert np.isclose(e_out(r), Q / (4 * np.pi * eps * r * r), rtol=1e-12)        # = carga pontual Q
    assert np.isclose(e_in(R), e_out(R)) and np.isclose(e_in(R), rho * R / (3 * eps))  # E(R⁻) = E(R⁺)
    assert e_in(0) == 0 and e_out(1e6 * R) < 1e-10 * e_in(R)                          # limites
    assert np.isclose(f_graph(1), 1) and (f_graph(1.001) - 1) / 0.001 < -1.9 and (1 - f_graph(0.999)) / 0.001 > 0.9
    assert np.cos(0) == 1 and abs(np.cos(np.pi / 2)) < 1e-12 and np.cos(np.radians(150)) < 0
    # elemento de volume: |∂/∂r'| |∂/∂ϑ| |∂/∂φ| = 1 · r' · r' sinϑ (arestas ortogonais)
    rp_, t_, f_ = 0.62, np.radians(50), np.radians(-50)
    pos = lambda a, b, c: np.array([a * np.sin(b) * np.cos(c), a * np.sin(b) * np.sin(c), a * np.cos(b)])
    h = 1e-6
    dr = (pos(rp_ + h, t_, f_) - pos(rp_ - h, t_, f_)) / (2 * h)
    dt = (pos(rp_, t_ + h, f_) - pos(rp_, t_ - h, f_)) / (2 * h)
    dp = (pos(rp_, t_, f_ + h) - pos(rp_, t_, f_ - h)) / (2 * h)
    assert np.isclose(np.linalg.norm(dr), 1) and np.isclose(np.linalg.norm(dt), rp_)
    assert np.isclose(np.linalg.norm(dp), rp_ * np.sin(t_)) and abs(dr @ dt) < 1e-6 and abs(dt @ dp) < 1e-6
    # ∮ dΩ_or = ∮ cosθ dA / r²: 4π com a carga dentro (mesmo deslocada), 0 fora (esfera unitária, quadratura)
    nt, nf = 600, 1200
    th = (np.arange(nt) + 0.5) * np.pi / nt
    ph = (np.arange(nf) + 0.5) * 2 * np.pi / nf
    T, F = np.meshgrid(th, ph, indexing="ij")
    nrm = np.stack([np.sin(T) * np.cos(F), np.sin(T) * np.sin(F), np.cos(T)], -1)
    dA = np.sin(T) * (np.pi / nt) * (2 * np.pi / nf)
    for qpos, alvo in (((0.5, 0.25, 0.1), 4 * np.pi), ((1.8, 0.3, 0.0), 0.0)):
        d = nrm - np.array(qpos)
        dist = np.linalg.norm(d, axis=-1)
        omega = np.sum(np.sum(d * nrm, -1) / dist ** 3 * dA)
        assert abs(omega - alvo) < 2e-3, (qpos, omega)


_qa()


# ── Texto (mesmo idioma do vid_0012) ────────────────────────────────────────
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


def display(content, size=36, color=WHITE, bold=False):
    with wide_pango():
        if bold:
            t = official_text(content, DISPLAY_FONT, BOLD, size, oversample=2)
        else:
            t = screen_text(content, size, oversample=2)
    return t.set_color(color)


def eq(*parts, size=44, color=WHITE, colors=None):
    m = MathTex(*parts, font_size=size, color=color)
    for i, col in (colors or {}).items():
        m[i].set_color(col)
    return m


def fit(m, w):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def box(m, color=WHITE, buff=0.16):
    return SurroundingRectangle(m, color=color, buff=buff, corner_radius=0.08, stroke_width=2.5)


def strike(m, color=WHITE, w=4):
    return Line(m.get_corner(DL) + 0.06 * DL, m.get_corner(UR) + 0.06 * UR).set_stroke(color, w)


def frac_parts(part):
    """(numerador, barra, denominador) de uma fração MathTex, por geometria (esquerda → direita)."""
    gl = list(part)
    bar = max(gl, key=lambda g: g.width)
    num = sorted((g for g in gl if g is not bar and g.get_y() > bar.get_y()), key=lambda g: g.get_x())
    den = sorted((g for g in gl if g is not bar and g.get_y() < bar.get_y()), key=lambda g: g.get_x())
    return num, bar, den


def hchain(*items, buff=0.18):
    return VGroup(*items).arrange(RIGHT, buff=buff)


def left_at(m, x, y):
    return m.move_to(P(0, y)).align_to(P(x, 0), LEFT)


def domain_tag(nome, dom, size=30):
    return hchain(text(nome, 22, opacity=0.85), eq(dom, size=size), buff=0.15)


# ── Geometria ───────────────────────────────────────────────────────────────
def P(x, y):
    return np.array([x, y, 0.0])


def U(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def ang(v):
    return np.degrees(np.arctan2(v[1], v[0]))


def vec(p0, p1, color=CYAN, w=5, op=1.0, z=3):
    d = float(np.linalg.norm(p1 - p0))
    if d < 0.04 or op < 0.01:
        return VMobject()
    return Arrow(p0, p1, buff=0, stroke_width=w, tip_length=min(0.2, 0.42 * d), max_tip_length_to_length_ratio=0.5,
                 max_stroke_width_to_length_ratio=40, color=color).set_opacity(op).set_z_index(z)


def right_angle(p, u1, u2, s=0.2, color=WHITE, op=1.0):
    if op < 0.01:
        return VMobject()
    return VMobject().set_points_as_corners([p + s * u1, p + s * (u1 + u2), p + s * u2]).set_stroke(color, 2.5, op)


def ring(c, r, n, a0=0.0):
    return [c + r * U(a0 + 360.0 * k / n) for k in range(n)]


def e_point(p, charges, qs=None):
    E = np.zeros(3)
    for q, s in zip(charges, qs or [1.0] * len(charges)):
        d = p - q
        E += s * d / np.linalg.norm(d) ** 3
    return E


def coulomb(points, charges, k, lmin, lmax, qs=None, w=4.5, op=1.0):
    """E⃗ (superposição de cargas pontuais) desenhado em cada ponto; comprimento = clip(k |E|)."""
    out = VGroup()
    if op < 0.01:
        return out
    for p in points:
        E = e_point(p, charges, qs)
        m = np.linalg.norm(E)
        if m > 1e-9:
            out.add(vec(p, p + float(np.clip(k * m, lmin, lmax)) * E / m, CYAN, w, op))
    return out


def arrows_norm(points, evecs, med=0.3, lmin=0.08, lmax=0.8, w=4):
    """Setas com comprimento ∝ |E| (normalizado pela mediana do painel), recortado em [lmin, lmax]."""
    ms = [float(np.linalg.norm(e)) for e in evecs]
    k = med / float(np.median(ms))
    return VGroup(*[vec(p, p + float(np.clip(k * m, lmin, lmax)) * e / m, CYAN, w) for p, e, m in zip(points, evecs, ms)])


def gauss_circle(c, r, op=1.0, n=None, w=3.5):
    r = max(r, 1e-3)
    return DashedVMobject(Circle(radius=r, arc_center=c), num_dashes=n or max(12, int(16 * r)),
                          dashed_ratio=0.6).set_stroke(VIOLET, w, op)


def dashed_curve(pts, op=1.0, n=56, color=VIOLET, w=3.5):
    return DashedVMobject(VMobject().set_points_as_corners(pts), num_dashes=n, dashed_ratio=0.6).set_stroke(color, w, op)


def polar_pts(c, rho, a0=0.0, a1=360.0, n=181):
    return np.array([c + rho(a) * U(a) for a in np.linspace(a0, a1, n)])


def charge(p, op=1.0, label=None):
    g = VGroup(Dot(p, radius=0.19, color=WHITE).set_opacity(0.18 * op), Dot(p, radius=0.09, color=WHITE).set_opacity(op))
    if label:
        g.add(eq(label, size=30).set_opacity(op).next_to(g[1], DR, buff=0.02))
    return g.set_z_index(6)


def blob(a):
    """Forma da superfície arbitrária (a em graus); estrelada em relação ao centro."""
    t = np.radians(a)
    return 1 + 0.2 * np.sin(2 * t + 0.6) + 0.1 * np.cos(3 * t - 0.4)


def blob_normal(scale, a):
    """Normal exterior da curva polar ρ(a) = scale·blob(a): n ∝ ρ û − ρ' û⊥."""
    t = np.radians(a)
    rho = scale * blob(a)
    drho = scale * (0.4 * np.cos(2 * t + 0.6) - 0.3 * np.sin(3 * t - 0.4))
    n = rho * U(a) - drho * np.array([-np.sin(t), np.cos(t), 0.0])
    return n / np.linalg.norm(n)


def ray_hits(q, a, bc, scale, tmax=7.0, n=1400):
    """Distâncias ao longo do raio (de q, ângulo a) em que ele cruza a curva polar centrada em bc."""
    t = np.linspace(0.02, tmax, n)
    pts = q[None, :] + t[:, None] * U(a)[None, :]
    rel = pts - bc
    inside = np.linalg.norm(rel, axis=1) < scale * blob(np.degrees(np.arctan2(rel[:, 1], rel[:, 0])))
    idx = np.nonzero(inside[1:] != inside[:-1])[0]
    return [float(t[i]) for i in idx]


def sector_fill(c, rho, a0, a1, op):
    pts = [c] + [c + rho(a) * U(a) for a in np.linspace(a0, a1, max(3, int(abs(a1 - a0) / 3) + 2))]
    return Polygon(*pts).set_stroke(width=0).set_fill(WHITE, op)


# projeção ortográfica levemente de cima: x → tela x; z (eixo polar) → tela y; y (profundidade) sobe pouco
EL_C, EL_S = 0.95, 0.31


def p3(c, s, v):
    return c + s * np.array([v[0], v[2] * EL_C + v[1] * EL_S, 0.0])


def sph(rp, th, ph):
    t, f = np.radians(th), np.radians(ph)
    return np.array([rp * np.sin(t) * np.cos(f), rp * np.sin(t) * np.sin(f), rp * np.cos(t)])


# ── Painéis das simetrias clássicas (coordenadas locais, centro na origem) ──
def sym_sphere():
    src = Circle(radius=0.55).set_stroke(BLUE_L, 3).set_fill(BLUE, 0.3)
    fld = VGroup(*[vec(1.05 * U(a), 1.6 * U(a), CYAN, 4.5) for a in range(0, 360, 45)])
    srf = Circle(radius=1.05).set_stroke(VIOLET, 5).set_fill(VIOLET, 0.08)
    el = VGroup(Arc(radius=1.05, start_angle=np.radians(12), angle=np.radians(21)).set_stroke(WHITE, 8),
                vec(1.05 * U(22.5), 1.68 * U(22.5), CYAN, 4.5, z=6), vec(1.05 * U(22.5), 1.45 * U(22.5), WHITE, 3.5, z=7))
    return SimpleNamespace(src=src, fld=fld, contrib=srf, zero=VGroup(), el_c=el, el_z=VGroup(),
                           all=VGroup(src, fld, srf, el))


def sym_line():
    src = VGroup(Line(P(0, -1.75), P(0, 1.75)).set_stroke(BLUE_L, 5),
                 DashedLine(P(0, 1.75), P(0, 2.15), dash_length=0.08).set_stroke(BLUE_L, 3, 0.5),
                 DashedLine(P(0, -1.75), P(0, -2.15), dash_length=0.08).set_stroke(BLUE_L, 3, 0.5))
    fld = VGroup(*[vec(P(sg * 0.22, y), P(sg * 1.45, y), CYAN, 4.5) for y in (-0.8, 0.05, 0.8) for sg in (-1, 1)])
    top, bot = 1.1, -1.1
    lateral = VGroup(Polygon(P(-0.85, bot), P(0.85, bot), P(0.85, top), P(-0.85, top)).set_stroke(width=0)
                     .set_fill(VIOLET, 0.1),
                     Line(P(-0.85, bot), P(-0.85, top)).set_stroke(VIOLET, 5), Line(P(0.85, bot), P(0.85, top)).set_stroke(VIOLET, 5))
    caps = VGroup(DashedVMobject(Ellipse(width=1.7, height=0.42).move_to(P(0, top)), num_dashes=16),
                  DashedVMobject(Ellipse(width=1.7, height=0.42).move_to(P(0, bot)), num_dashes=16)).set_stroke(VIOLET, 2.5)
    el_lat = VGroup(Line(P(0.85, -0.62), P(0.85, -0.22)).set_stroke(WHITE, 8),
                    vec(P(0.85, -0.5), P(1.5, -0.5), CYAN, 4.5, z=6), vec(P(0.85, -0.36), P(1.32, -0.36), WHITE, 3.5, z=7))
    el_cap = VGroup(Ellipse(width=0.36, height=0.1).move_to(P(0.38, top)).set_stroke(WHITE, 4),
                    vec(P(0.38, top), P(0.38, top + 0.5), WHITE, 3.5, z=7), vec(P(0.38, top), P(1.0, top), CYAN, 4.5, z=6))
    return SimpleNamespace(src=src, fld=fld, contrib=lateral, zero=caps, el_c=el_lat, el_z=el_cap,
                           all=VGroup(src, fld, lateral, caps, el_lat, el_cap))


def sym_plane():
    src = Polygon(P(-1.95, -0.35), P(1.25, -0.35), P(1.95, 0.25), P(-1.25, 0.25)).set_stroke(BLUE_L, 3).set_fill(BLUE, 0.3)
    fld = VGroup(*[vec(P(a, 0.05), P(a, 0.95), CYAN, 4.5) for a in (-1.2, 1.2)] +
                 [vec(P(a, -0.15), P(a, -1.05), CYAN, 4.5) for a in (-1.2, 1.2)])
    pt, pb = 0.75, -0.85
    caps = VGroup(Ellipse(width=0.9, height=0.24).move_to(P(0, pt)).set_stroke(VIOLET, 5).set_fill(VIOLET, 0.15),
                  Ellipse(width=0.9, height=0.24).move_to(P(0, pb)).set_stroke(VIOLET, 5).set_fill(VIOLET, 0.15))
    lateral = VGroup(DashedLine(P(-0.45, pb), P(-0.45, pt), dash_length=0.08),
                     DashedLine(P(0.45, pb), P(0.45, pt), dash_length=0.08)).set_stroke(VIOLET, 2.5)
    el_caps = VGroup(vec(P(-0.12, pt), P(-0.12, pt + 0.45), WHITE, 3.5, z=7), vec(P(0.12, pt), P(0.12, pt + 0.62), CYAN, 4.5, z=6),
                     vec(P(-0.12, pb), P(-0.12, pb - 0.45), WHITE, 3.5, z=7), vec(P(0.12, pb), P(0.12, pb - 0.62), CYAN, 4.5, z=6))
    el_lat = VGroup(Line(P(0.45, -0.62), P(0.45, -0.32)).set_stroke(WHITE, 8),
                    vec(P(0.45, -0.47), P(0.92, -0.47), WHITE, 3.5, z=7), vec(P(0.6, -0.4), P(0.6, -0.95), CYAN, 4.5, z=6))
    return SimpleNamespace(src=src, fld=fld, contrib=caps, zero=lateral, el_c=el_caps, el_z=el_lat,
                           all=VGroup(src, fld, caps, lateral, el_caps, el_lat))


# ── Cena ────────────────────────────────────────────────────────────────────
class LeiGauss(Scene):

    # relógio nominal: soma dos run_time; at(t) completa o bloco até o instante t (relativo)
    def setup(self):
        self.T, self.b0, self.wm, self.tag = 0.0, 0.0, None, None
        self.camera.background_color = BACKGROUND_COLOR

    def play(self, *args, **kwargs):
        anims = self.compile_animations(*args, **kwargs)
        self.T += max(a.run_time for a in anims)
        return super().play(*anims)

    def at(self, t):
        d = self.b0 + t - self.T
        if d > 0.04:
            # Scene.wait congela o quadro quando não há updater dependente do tempo: aplica os updaters antes
            self.update_mobjects(0)
            self.wait(d)
        elif d < -0.4:
            print(f"ATRASO {-d:.1f}s no bloco que começou em {self.b0:.0f}s (marca {t})")

    def begin(self, k, name):
        self.next_section(f"{k:02d}_{name}", skip_animations=bool(SO) and k not in SO)
        self.b0 = self.T
        print(f"bloco {k:02d} {name}: início nominal {self.T:6.1f}s")

    def clear(self, *keep, run_time=0.8, extra=()):
        keep = {id(m) for m in (*keep, self.wm, self.tag) if m is not None}
        ms = [m for m in self.mobjects if id(m) not in keep]
        for m in ms:
            m.clear_updaters()
            for s in m.get_family():
                s.clear_updaters()
        if ms or extra:
            self.play(*[FadeOut(m) for m in ms], *extra, run_time=run_time)

    def flatten(self, g):
        """Partes de g viram objetos de topo da cena (para animá-las separadamente)."""
        self.remove(g)
        self.add(*g)

    def regroup(self, g):
        """Reúne em g partes soltas na cena (inverso de flatten)."""
        self.remove(*g)
        self.add(g)

    def construct(self):
        if GUIAS:
            self.add(safe_guides())
        self.b01_cold_open()
        self.b02_intro()
        self.b03_normal_fluxo()
        self.b04_coulomb()
        self.b05_angulo_solido()
        self.b06_superficie_ruim()
        self.b07_simetria()
        self.b08_esfera_uniforme()
        self.b09_grafico()
        self.b10_tres_simetrias()
        self.b11_casos_e_metodo()
        self.b12_retorno_payoff_outro()
        print(f"duração nominal total: {self.T:.1f}s")

    # ── 01 · Cold open: dois problemas (COMPARE) ────────────────────────────
    GAUSS = (r"\oint", r"\vec E\cdot d\vec A", "=", r"\frac{Q_{\mathrm{env}}}{\varepsilon_0}")
    RG1 = 1.3
    QOFF1 = np.array([0.55, 0.3, 0.0])

    def problems(self, off, aro):
        """Os dois casos (reusados no retorno). off: carga da direita, 0 = centro → 1 = deslocada."""
        g = SimpleNamespace(cl=P(LX, 0.35), cr=P(RX, 0.35))
        g.ball = Circle(radius=0.72, arc_center=g.cl).set_stroke(BLUE_L, 3).set_fill(BLUE, 0.32)
        g.gl, g.gr = gauss_circle(g.cl, self.RG1), gauss_circle(g.cr, self.RG1)
        g.al = VGroup(*[vec(g.cl + self.RG1 * U(a), g.cl + (self.RG1 + 0.55) * U(a)) for a in range(18, 360, 36)])
        g.qpos = lambda: g.cr + off.get_value() * self.QOFF1
        g.q = always_redraw(lambda: charge(g.qpos()))
        g.ar = always_redraw(lambda: coulomb(ring(g.cr, self.RG1, 12, 15), [g.qpos()], 0.93, 0.12, 0.85,
                                             op=aro.get_value()))
        g.el = eq(*self.GAUSS, size=36).move_to(P(LX, -2.5))
        g.er = eq(*self.GAUSS, size=36).move_to(P(RX, -2.5))
        return g

    def b01_cold_open(self):
        self.begin(1, "cold_open")
        c = cues("Olha esses dois problemas.",
                 "Nos dois, eu consigo desenhar uma superfície fechada e escrever exatamente a mesma Lei de Gauss.",
                 "No primeiro, a distribuição de carga é perfeitamente simétrica. Em poucos passos, o campo elétrico aparece.",
                 "No segundo, eu coloco uma carga fora do centro de uma esfera.",
                 "A Lei de Gauss continua verdadeira.",
                 "O fluxo continua perfeitamente determinado.",
                 "E mesmo assim eu não consigo simplesmente descobrir o campo sobre a esfera.",
                 "Então o que mudou?")
        off, aro = ValueTracker(0.0), ValueTracker(0.0)
        g = self.problems(off, aro)
        self.play(Create(g.gl), Create(g.gr), FadeIn(g.ball), run_time=1.6)
        self.at(c[1])
        self.play(Write(g.el), Write(g.er), run_time=2.2)
        self.at(c[2])
        self.play(LaggedStart(*[GrowArrow(a) for a in g.al], lag_ratio=0.08), run_time=1.6)
        s2 = eq("E", r"\,4\pi r^2", "=", r"\frac{Q_{\mathrm{env}}}{\varepsilon_0}", size=36, colors={0: CYAN}).move_to(g.el)
        s3 = eq("E", "=", r"\frac{Q_{\mathrm{env}}}{4\pi\varepsilon_0 r^2}", size=36, colors={0: CYAN}).move_to(g.el)
        self.play(TransformMatchingTex(g.el, s2), run_time=1.1)
        self.wait(0.5)
        self.play(TransformMatchingTex(s2, s3), run_time=1.1)
        g.el = s3
        self.at(c[3])
        self.add(g.ar)
        self.play(FadeIn(g.q, scale=0.5), aro.animate.set_value(1.0), run_time=0.9)
        self.play(off.animate.set_value(1.0), run_time=2.6)
        self.at(c[4])
        self.play(Indicate(g.er, color=WHITE, scale_factor=1.08), run_time=1.0)
        self.at(c[5])
        self.play(Circumscribe(g.er, color=WHITE, stroke_width=2), run_time=1.2)
        self.at(c[6])
        g.ask = eq(r"\vec E=\,?", size=38, colors={0: CYAN}).move_to(g.cr + P(2.05, 1.35))
        self.play(FadeIn(g.ask, shift=0.15 * LEFT), run_time=0.8)
        self.at(c[7])
        g.question = display("Então o que mudou?", 38).move_to(P(0, 3.1))
        self.play(FadeIn(g.question, shift=0.15 * DOWN), run_time=0.9)
        self.at(c[-1] + 0.8)
        self.g1 = g

    # ── 02 · Intro humana curta (FOCUS com contexto residual) ───────────────
    def b02_intro(self):
        self.begin(2, "intro")
        c = cues("Fala, pessoal. Bem-vindos ao Parallax Lab.",
                 "Hoje a gente vai entender por que a Lei de Gauss resolve alguns problemas quase instantaneamente e, em outros, parece não ajudar.",
                 "E a chave para entender isso é a simetria.",
                 "E é justamente essa diferença que faz muita gente aprender a usar esferas e cilindros gaussianos sem realmente entender por quê.")
        g = self.g1
        for m in (g.q, g.ar):
            m.clear_updaters()
        ctx = VGroup(g.gl, g.gr, g.ball, g.al, g.q, g.ar, g.el, g.er, g.ask)
        orig = ctx.copy()
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.6).set_opacity(0.35).to_corner(UR, buff=0.3)
        self.tag = text("LEI DE GAUSS", 18, opacity=0.6).to_corner(UL, buff=0.38)
        brand = text("PARALLAX LAB", 22, opacity=0.8).move_to(P(0, 2.05))
        title = display("LEI DE GAUSS", 58, bold=True).move_to(P(0, 1.25))
        sub = text("Quando ela realmente encontra o campo?", 26, opacity=0.85).move_to(P(0, 0.45))
        self.play(ctx.animate.scale(0.55, about_point=ORIGIN).move_to(P(0, -1.65)).set_opacity(0.3),
                  FadeOut(g.question), run_time=1.2)
        self.play(FadeIn(brand, shift=0.1 * DOWN), FadeIn(title, shift=0.15 * DOWN), FadeIn(sub), FadeIn(self.wm),
                  run_time=1.0)
        self.at(c[1] + 3.0)
        self.play(FadeOut(VGroup(brand, title, sub)), FadeIn(self.tag), Transform(ctx, orig), run_time=1.2)
        self.remove(ctx)
        self.add(*ctx)
        self.at(c[1] + 5.0)
        self.play(Indicate(VGroup(g.ball, g.al, g.el), color=CYAN, scale_factor=1.04), run_time=1.2)
        self.at(c[1] + 7.2)
        self.play(Indicate(VGroup(g.ar, g.ask), color=WHITE, scale_factor=1.04), run_time=1.2)
        # a promessa: fonte → campo → superfície (a ordem que o vídeo vai defender)
        self.at(c[2])
        words = [text("fonte", 26, BLUE_L), eq(r"\rightarrow", size=32), text("campo", 26, CYAN), eq(r"\rightarrow", size=32),
                 text("superfície", 26, VIOLET)]
        chain = hchain(*words, buff=0.2).move_to(P(LX, 2.45))
        self.play(FadeIn(words[0], shift=0.1 * DOWN), Indicate(g.ball, color=BLUE_L, scale_factor=1.12), run_time=1.1)
        self.play(FadeIn(words[1]), FadeIn(words[2], shift=0.1 * DOWN),
                  LaggedStart(*[Indicate(a, color=CYAN, scale_factor=1.2) for a in g.al], lag_ratio=0.05), run_time=1.4)
        self.play(FadeIn(words[3]), FadeIn(words[4], shift=0.1 * DOWN), Indicate(g.gl, color=VIOLET, scale_factor=1.06),
                  run_time=1.2)
        self.at(c[3] + 2.0)
        self.play(Circumscribe(chain, color=WHITE, stroke_width=2), run_time=1.6)
        # a superfície gaussiana da esquerda vira a superfície fechada do próximo bloco
        self.at(c[-1] - 1.3)
        self.surf0 = gauss_circle(P(-4.6, -0.2), 1.6)
        others = [m for m in ctx if m is not g.gl] + [chain]
        self.play(FadeOut(VGroup(*others)), ReplacementTransform(g.gl, self.surf0), run_time=1.3)
        self.at(c[-1] + 0.2)

    # ── 03 · Normal, vetor área (FOCUS) e produto escalar (BUILD) ───────────
    def b03_normal_fluxo(self):
        self.begin(3, "normal_vetor_area_fluxo")
        c = cues("Antes de responder, precisamos entender o que a Lei de Gauss está medindo.",
                 "Pegue um pedacinho muito pequeno de uma superfície. Sua área é um número: d A.",
                 "De tão pequeno, esse pedacinho praticamente coincide com um plano: o plano tangente naquele ponto.",
                 "A normal, n chapéu, é um vetor de comprimento um, perpendicular a esse plano.",
                 "Multiplicando a normal pela área, obtemos o vetor área. Ele aponta na direção da normal, e seu tamanho representa a área do pedacinho.",
                 "Numa superfície fechada, cada ponto tem a sua própria normal. E, por convenção, escolhemos sempre a normal que aponta para fora.",
                 "Agora coloque esse elemento num campo elétrico.",
                 "O ângulo que importa aqui não é o de noventa graus entre a normal e a superfície. É o ângulo teta entre o campo e a normal.",
                 "Se o campo atravessa a superfície de frente, a contribuição para o fluxo é máxima.",
                 "Se inclinarmos o elemento, a normal e o vetor área inclinam junto com ele.",
                 "Se o campo passa tangente à superfície, não atravessa aquele elemento. A contribuição é zero.",
                 "E se o campo aponta para dentro de uma superfície fechada, enquanto a normal aponta para fora, a contribuição é negativa.",
                 "É isso que o produto escalar está fazendo.",
                 "A integral fechada apenas repete essa soma por toda a superfície.",
                 "Ela não está contando literalmente linhas de campo. As linhas são uma representação. O fluxo é essa soma matemática de quanto do campo atravessa cada elemento de área.")
        SC, pc = P(-4.6, -0.2), P(-3.0, -0.2)
        surf0 = getattr(self, "surf0", None) or gauss_circle(SC, 1.6)
        self.clear(surf0, run_time=0.6)
        self.add(surf0)
        TH, DEP, SZ = ValueTracker(0.0), ValueTracker(1.0), ValueTracker(0.3)
        NA, DAO, TPO, RAO, DLO, NLO, EO, AO, SHO, CO, RO = (ValueTracker(0.0) for _ in range(11))
        DV = np.array([-0.62, 0.5, 0.0])                    # profundidade (projeção oblíqua) da placa

        def corners(k=1.0):
            s, t = SZ.get_value() * k, U(TH.get_value() + 90)
            hl, hd = 0.8 * s * t, 0.55 * DEP.get_value() * s * DV
            return [pc - hl - hd, pc + hl - hd, pc + hl + hd, pc - hl + hd]

        def tangent_plane():
            o = TPO.get_value()
            if o < 0.01:
                return VGroup()
            cs = corners(2.2)
            return VGroup(Polygon(*cs).set_stroke(width=0).set_fill(WHITE, 0.05 * o),
                          DashedVMobject(Polygon(*cs), num_dashes=36).set_stroke(WHITE, 1.5, 0.6 * o)).set_z_index(1)
        tplane = always_redraw(tangent_plane)
        plate = always_redraw(lambda: Polygon(*corners()).set_stroke(VIOLET, 3).set_fill(VIOLET, 0.38).set_z_index(2))
        nhat = always_redraw(lambda: vec(pc, pc + 1.0 * U(TH.get_value()), NCOL, 3.5, NA.get_value(), z=8))
        dAv = always_redraw(lambda: vec(pc, pc + 1.5 * SZ.get_value() ** 2 * U(TH.get_value()), NCOL, 10,
                                        0.38 * DAO.get_value(), z=7))
        rmark = always_redraw(lambda: right_angle(pc, U(TH.get_value()), U(TH.get_value() + 90), 0.22, WHITE, RAO.get_value()))
        lab_dA = eq("dA", size=32)
        lab_dA.add_updater(lambda m: m.move_to(pc + 0.45 * SZ.get_value() * U(TH.get_value() + 90)
                                               + 0.25 * SZ.get_value() * DEP.get_value() * DV - 0.18 * U(TH.get_value()))
                           .set_opacity(DLO.get_value()))
        lab_n = eq(r"\hat n", size=34)
        lab_n.add_updater(lambda m: m.move_to(pc + 0.6 * U(TH.get_value()) + 0.3 * U(TH.get_value() - 90))
                          .set_opacity(NA.get_value()))
        lab_dAv = eq(r"d\vec A", size=34)
        lab_dAv.add_updater(lambda m: m.move_to(pc + (1.5 * SZ.get_value() ** 2 + 0.4) * U(TH.get_value()))
                            .set_opacity(DAO.get_value()))
        lab_tp = text("plano tangente", 22, opacity=0.8)
        lab_tp.add_updater(lambda m: m.move_to(max(corners(2.2), key=lambda p: p[1]) + P(0.2, 0.25))
                           .set_opacity(0.8 * TPO.get_value()))
        lab_90 = eq(r"90^\circ", size=26)
        lab_90.add_updater(lambda m: m.move_to(pc + 0.5 * U(TH.get_value() + 45)).set_opacity(NLO.get_value()))
        self.add(tplane, plate, dAv, nhat, rmark, lab_dA, lab_n, lab_dAv, lab_tp, lab_90)

        # dA: um número. Ampliar o elemento.
        L1 = left_at(hchain(eq("dA", size=40), text("área do elemento (um número)", 24, opacity=0.85)), 0.8, 1.6)
        L2 = left_at(hchain(eq(r"\hat n", size=40), text("normal unitária", 24, opacity=0.85), eq(r"|\hat n|=1", size=34)), 0.8, 0.7)
        L3 = left_at(hchain(eq(r"d\vec A", "=", r"\hat n", r"\,dA", size=44), text("vetor área", 24, opacity=0.85)), 0.8, -0.3)
        self.at(c[1])
        self.play(SZ.animate.set_value(0.3), DLO.animate.set_value(1.0), FadeIn(L1, shift=0.1 * DOWN), run_time=1.0)
        self.play(FadeOut(surf0), SZ.animate.set_value(1.0), run_time=1.5)
        self.at(c[2])
        self.play(TPO.animate.set_value(1.0), run_time=1.4)
        self.at(c[3])
        self.play(NA.animate.set_value(1.0), run_time=1.2)
        self.play(RAO.animate.set_value(1.0), FadeIn(L2, shift=0.1 * DOWN), run_time=1.0)
        self.at(c[4])
        self.play(DAO.animate.set_value(1.0), FadeIn(L3, shift=0.1 * DOWN), run_time=1.2)
        # o vetor área acompanha a área; a normal unitária não muda
        self.play(SZ.animate.set_value(0.68), run_time=1.6)
        self.play(SZ.animate.set_value(1.0), run_time=1.4)
        self.at(c[5])
        # superfície fechada: uma normal por ponto, sempre a exterior
        self.play(TPO.animate.set_value(0.0), SZ.animate.set_value(0.3), DAO.animate.set_value(0.0), RAO.animate.set_value(0.0),
                  DLO.animate.set_value(0.0), NA.animate.set_value(0.0), FadeIn(surf0), run_time=1.2)
        outs = VGroup(*[vec(SC + 1.6 * U(a), SC + 2.08 * U(a), NCOL, 3.5) for a in range(0, 360, 45)])
        inward = DashedLine(SC + 1.6 * U(180), SC + 1.12 * U(180), dash_length=0.06).set_stroke(WHITE, 2.5, 0.6)
        inward.add_tip(tip_length=0.14)
        ext_lab = text("normal exterior", 22, opacity=0.85).move_to(SC + P(-0.2, -2.2))
        self.play(LaggedStart(*[GrowArrow(a) for a in outs], lag_ratio=0.1), run_time=1.6)
        self.play(Create(inward), run_time=0.6)
        self.play(FadeOut(inward), Indicate(outs[4], color=WHITE, scale_factor=1.4), FadeIn(ext_lab), run_time=1.2)
        self.play(FadeOut(VGroup(outs, ext_lab, surf0)), SZ.animate.set_value(1.0), NA.animate.set_value(1.0),
                  DAO.animate.set_value(1.0), RAO.animate.set_value(1.0), run_time=1.4)
        self.at(c[6])

        # campo uniforme (para +x); vista quase lateral
        rows = (-2.05, -1.25, -0.45, 0.45, 1.25, 2.05)
        field = VGroup(*[vec(P(x0, pc[1] + dy), P(x0 + 1.0, pc[1] + dy), CYAN, 4, 0.55, z=1)
                         for dy in rows for x0 in (-6.9, -5.6, -4.3, -3.0)])
        e_here = always_redraw(lambda: vec(pc - 1.25 * U(0), pc - 0.04 * U(0), CYAN, 5, EO.get_value(), z=4))
        ref = always_redraw(lambda: DashedLine(pc, pc + 0.75 * U(0)).set_stroke(CYAN, 2, 0.6 * AO.get_value()))
        arc = always_redraw(lambda: Arc(radius=0.55, start_angle=0, angle=np.radians(TH.get_value()), arc_center=pc)
                            .set_stroke(CYAN, 3, AO.get_value()) if TH.get_value() > 3 else VMobject())
        thl = eq(r"\theta", size=32, color=CYAN)
        thl.add_updater(lambda m: m.move_to(pc + 0.85 * U(TH.get_value() / 2))
                        .set_opacity(AO.get_value() if TH.get_value() > 12 else 0))
        self.add(e_here, ref, arc, thl)
        eqA = eq(r"d\vec A", "=", r"\hat n", r"\,dA", size=40).move_to(P(RX, 2.15))
        self.flatten(L3)
        self.play(LaggedStart(*[FadeIn(a) for a in field], lag_ratio=0.02), DEP.animate.set_value(0.35),
                  EO.animate.set_value(1.0), FadeOut(VGroup(L1, L2, L3[1])), ReplacementTransform(L3[0], eqA), run_time=2.0)
        self.play(TH.animate.set_value(35), run_time=1.2)
        self.at(c[7])
        # dois ângulos diferentes: 90° (n̂ × plano) e θ (E⃗ × n̂)
        self.play(NLO.animate.set_value(1.0), Indicate(rmark, color=WHITE, scale_factor=1.3), run_time=1.0)
        self.play(AO.animate.set_value(1.0), run_time=1.0)
        eqF = eq(r"d\Phi_E", "=", r"\vec E", r"\cdot d\vec A", size=46, colors={2: CYAN}).move_to(P(RX, 1.05))
        eqF2 = eq(r"d\Phi_E", "=", "E", r"\,dA", r"\cos", r"\theta", size=46, colors={2: CYAN, 5: CYAN}).move_to(P(RX, 1.05))
        self.play(Write(eqF), run_time=1.2)
        self.play(TransformMatchingTex(eqF, eqF2), run_time=1.2)
        eqF = eqF2

        # leituras sincronizadas: θ, cos θ, barra de dΦ e sinal; sombra = projeção da placa
        cos = lambda: float(np.cos(np.radians(TH.get_value())))
        thv = DecimalNumber(0, num_decimal_places=0, unit=r"^\circ", font_size=38, color=CYAN)
        cv = DecimalNumber(1, num_decimal_places=2, include_sign=True, font_size=38)
        th_lab, c_lab = eq(r"\theta=", size=38, color=CYAN), eq(r"\cos\theta=", size=38)
        row = VGroup(th_lab, thv, c_lab, cv)
        th_lab.move_to(P(RX - 1.9, -0.2))
        c_lab.move_to(P(RX + 0.75, -0.2))
        thv.add_updater(lambda m: m.set_value(TH.get_value()).next_to(th_lab, RIGHT, buff=0.12)
                        .set_opacity(RO.get_value()))
        cv.add_updater(lambda m: m.set_value(cos()).next_to(c_lab, RIGHT, buff=0.12).set_opacity(RO.get_value()))
        for m in (th_lab, c_lab):
            m.add_updater(lambda m: m.set_opacity(RO.get_value()))
        my, half = -1.35, 2.2
        meter = VGroup(Line(P(RX - half, my), P(RX + half, my)).set_stroke(WHITE, 2, 0.45),
                       Line(P(RX, my - 0.2), P(RX, my + 0.2)).set_stroke(WHITE, 2, 0.8))
        bar = always_redraw(lambda: Rectangle(width=max(abs(cos()) * half, 1e-3), height=0.26).set_stroke(width=0)
                            .set_fill(CYAN, 0.85 * RO.get_value()).move_to(P(RX + cos() * half / 2, my)))
        signs = VGroup(eq(r"d\Phi_E>0", size=36), eq(r"d\Phi_E=0", size=36), eq(r"d\Phi_E<0", size=36))
        for i, s in enumerate(signs):
            s.move_to(P(RX, -2.1))
            s.add_updater(lambda m, i=i: m.set_opacity(
                RO.get_value() * (1.0 if (cos() > 0.04, abs(cos()) <= 0.04, cos() < -0.04)[i] else 0.0)))
        SXP = -0.55

        def shadow():
            o = SHO.get_value()
            s, th = SZ.get_value(), TH.get_value()
            h = 0.8 * s * abs(np.cos(np.radians(th)))
            out = VGroup()
            if o < 0.01:
                return out
            if h > 0.03:
                out.add(Line(P(SXP, pc[1] - h), P(SXP, pc[1] + h)).set_stroke(WHITE, 6, 0.85 * o))
            t = U(th + 90)
            for e in (pc + 0.8 * s * t, pc - 0.8 * s * t):
                if abs(SXP - e[0]) > 0.08:
                    out.add(DashedLine(e, P(SXP, e[1]), dash_length=0.06).set_stroke(WHITE, 1.5, 0.45 * o))
            return out
        shad = always_redraw(shadow)
        self.add(row, bar, signs, shad)
        self.at(c[8])
        self.play(FadeIn(meter), RO.animate.set_value(1.0), SHO.animate.set_value(1.0), run_time=1.0)
        self.play(TH.animate.set_value(0), run_time=1.8)                       # de frente: máximo
        self.at(c[9])
        self.play(TH.animate.set_value(40), run_time=2.4)                      # n̂ e d⃗A acompanham o elemento
        self.at(c[10])
        self.play(TH.animate.set_value(90), run_time=2.6)                      # tangente: zero
        self.at(c[11])
        closed = always_redraw(lambda: gauss_circle(pc - 1.5 * U(TH.get_value()), 1.5, op=CO.get_value()))
        self.add(closed)
        self.play(CO.animate.set_value(1.0), SHO.animate.set_value(0.0), run_time=1.0)
        self.play(TH.animate.set_value(150), run_time=2.8)                     # entrando: negativo
        self.at(c[12])
        self.play(Indicate(eqF, color=WHITE, scale_factor=1.1), run_time=1.2)
        self.at(c[13])

        # a integral fechada repete essa soma em toda a superfície
        movers = (closed, plate, tplane, nhat, dAv, rmark, lab_dA, lab_n, lab_dAv, lab_tp, lab_90, e_here, ref, arc, thl,
                  row, bar, signs, shad, thv, cv, th_lab, c_lab)
        for m in movers:
            m.clear_updaters()
        cS = P(-3.4, -0.2)
        surfS = gauss_circle(cS, 1.6)
        normals = VGroup(*[vec(p, p + 0.42 * U(a), NCOL, 3.5) for a, p in zip(range(0, 360, 30), ring(cS, 1.6, 12))])
        eqI = eq(r"\Phi_E", "=", r"\oint_S", r"\vec E", r"\cdot d\vec A", size=50, colors={3: CYAN}).move_to(P(RX, 0.6))
        self.play(FadeOut(VGroup(*[m for m in movers if m is not closed]), meter, eqA), ReplacementTransform(closed, surfS),
                  run_time=1.2)
        self.play(LaggedStart(*[GrowArrow(n) for n in normals], lag_ratio=0.06), ReplacementTransform(eqF, eqI), run_time=1.6)
        self.at(c[14])
        lines = VGroup(*[Line(P(-6.9, pc[1] + dy), P(-0.4, pc[1] + dy)).set_stroke(CYAN, 2.5, 0.7) for dy in rows])
        self.regroup(field)
        self.play(ReplacementTransform(field, lines), run_time=1.5)
        self.at(c[14] + 3.8)
        self.play(lines.animate.set_stroke(opacity=0.18), run_time=1.2)
        self.at(c[14] + 6.8)
        self.play(LaggedStart(*[Indicate(n, color=WHITE, scale_factor=1.4) for n in normals], lag_ratio=0.08),
                  Create(box(eqI)), run_time=2.4)
        self.at(c[-1] + 0.4)

    # ── 04 · Coulomb + esfera (SPLIT) e cancelamento 1/r² × r² ──────────────
    def b04_coulomb(self):
        self.begin(4, "coulomb_esfera")
        c = cues("Agora coloque uma carga pontual no centro de uma esfera.",
                 "Pela Lei de Coulomb, o campo aponta radialmente e seu módulo diminui com o quadrado da distância.",
                 "Na superfície da esfera, campo e vetor área apontam na mesma direção.",
                 "Além disso, todos os pontos estão à mesma distância da carga. Então o módulo do campo é igual em toda a esfera.",
                 "Nesse caso, podemos tirar E da integral.",
                 "O fluxo vira o campo multiplicado pela área da esfera.",
                 "E aqui acontece algo importante.",
                 "Quando aumentamos o raio, o campo cai como um sobre o raio ao quadrado.",
                 "Mas a área da esfera cresce como o raio ao quadrado.",
                 "Uma coisa compensa exatamente a outra.",
                 "Por isso, não importa qual esfera centrada na carga escolhamos: o fluxo total é sempre q dividido por épsilon zero.",
                 "Isso já sugere que o fluxo está capturando alguma coisa mais profunda do que o valor local do campo.")
        self.clear(run_time=0.9)
        cc = P(LX, -0.2)
        RR, AO, NO, RLO, RA, MO, PO = (ValueTracker(v) for v in (1.4, 0.0, 0.0, 0.0, 210.0, 0.0, 0.0))
        K4 = 0.85 * 1.4 ** 2
        sph_ = always_redraw(lambda: VGroup(
            Circle(radius=RR.get_value(), arc_center=cc).set_stroke(width=0).set_fill(VIOLET, 0.06),
            gauss_circle(cc, RR.get_value()),
            DashedVMobject(Ellipse(width=2 * RR.get_value(), height=0.52 * RR.get_value()).move_to(cc),
                           num_dashes=26).set_stroke(VIOLET, 2, 0.4)))
        q = charge(cc, label="q")
        arrows = always_redraw(lambda: coulomb(ring(cc, RR.get_value(), 12, 15), [cc], K4, 0.05, 2.5, op=AO.get_value()))
        normals = always_redraw(lambda: VGroup(*[
            vec(p, p + 0.34 * U(a), NCOL, 3.5, NO.get_value(), z=4)
            for a, p in zip(range(0, 360, 30), ring(cc, RR.get_value(), 12))]))
        rline = always_redraw(lambda: Line(cc, cc + RR.get_value() * U(RA.get_value())).set_stroke(WHITE, 2.5, RLO.get_value()))
        rlab = eq("r", size=34, color=VIOLET)
        rlab.add_updater(lambda m: m.move_to(cc + 0.55 * RR.get_value() * U(RA.get_value())
                                             + 0.24 * U(RA.get_value() + 90)).set_opacity(RLO.get_value()))
        self.add(arrows, normals)
        self.play(FadeIn(sph_), FadeIn(q, scale=0.5), run_time=1.4)
        self.at(c[1])
        coul = eq(r"\vec E", r"=\frac{q}{4\pi\varepsilon_0 r^2}\hat r", size=42, colors={0: CYAN}).move_to(P(RX, 1.75))
        self.play(Write(coul), run_time=1.5)
        self.play(AO.animate.set_value(1.0), run_time=1.2)
        self.at(c[2])
        # passo 1 — campo e normal se alinham: o produto escalar vira produto de módulos
        b1 = eq(r"\Phi_E", "=", r"\oint_S", r"\vec E\cdot d\vec A", size=46).move_to(P(RX, 0.45))
        b2 = eq(r"\Phi_E", "=", r"\oint_S", "E", r"\,dA", size=46, colors={3: CYAN}).move_to(P(RX, 0.45))
        b3 = eq(r"\Phi_E", "=", "E", r"\oint_S", r"\,dA", size=46, colors={2: CYAN}).move_to(P(RX, 0.45))
        b4 = eq(r"\Phi_E", "=", "E", r"\,4\pi r^2", size=46, colors={2: CYAN}).move_to(P(RX, 0.45))
        par = eq(r"\vec E\parallel d\vec A", size=34).move_to(P(LX, 2.35))
        self.play(NO.animate.set_value(1.0), Write(b1), run_time=1.4)
        self.play(FadeIn(par, shift=0.1 * DOWN), run_time=0.8)
        self.play(TransformMatchingTex(b1, b2), run_time=1.2)
        self.at(c[3])
        # passo 2 — mesmo módulo em todos os pontos (mesma distância)
        self.add(rline, rlab)
        self.play(RLO.animate.set_value(1.0), run_time=0.6)
        self.play(RA.animate.set_value(210 + 360), run_time=3.0)
        tips = [cc + (1.4 + K4 / 1.4 ** 2 + 0.25) * U(a) for a in (15, 135, 255)]
        e_labs = VGroup(*[eq("E", size=30, color=CYAN).move_to(p) for p in tips])
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in e_labs], lag_ratio=0.3), run_time=1.2)
        self.at(c[4])
        self.play(TransformMatchingTex(b2, b3), FadeOut(e_labs), run_time=1.3)          # E sai da integral
        self.at(c[5])
        # passo 3 — a soma dos elementos de área é a área da esfera
        segs = VGroup(*[Arc(radius=1.4, start_angle=np.radians(a + 2), angle=np.radians(26), arc_center=cc)
                        .set_stroke(VIOLET, 7) for a in range(0, 360, 30)])
        self.play(LaggedStart(*[Create(s) for s in segs], lag_ratio=0.12), run_time=1.6)
        self.flatten(b3)
        self.play(ReplacementTransform(b3[0], b4[0]), ReplacementTransform(b3[1], b4[1]), ReplacementTransform(b3[2], b4[2]),
                  ReplacementTransform(VGroup(b3[3], b3[4]), b4[3]), FadeOut(segs), run_time=1.3)
        self.regroup(b4)
        self.at(c[6])

        # 1/r² × r²: o mesmo r controla vetores, área e as três barras
        rows = ((r"E\propto 1/r^2", CYAN, lambda R: (1.4 / R) ** 2),
                (r"A=4\pi r^2", VIOLET, lambda R: (R / 1.4) ** 2),
                (r"\Phi_E", WHITE, lambda R: 1.0))
        mlabs, mbars = VGroup(), VGroup()
        for i, (lab, col, f) in enumerate(rows):
            y = -1.1 - 0.68 * i
            mlabs.add(eq(lab, size=32, color=col).next_to(P(RX - 0.95, y), LEFT, buff=0))
            mbars.add(always_redraw(lambda f=f, col=col, y=y: Rectangle(width=max(1.3 * f(RR.get_value()), 0.01),
                                                                         height=0.24).set_stroke(width=0)
                                    .set_fill(col, 0.85 * MO.get_value()).next_to(P(RX - 0.75, y), RIGHT, buff=0)))
        self.add(mbars)
        self.play(MO.animate.set_value(1.0), FadeIn(mlabs), FadeOut(par), run_time=1.0)
        self.at(c[7])
        self.play(RR.animate.set_value(2.2), Indicate(mlabs[0], color=CYAN), run_time=3.6)
        self.at(c[8])
        c1 = eq(r"\Phi_E=", r"\frac{q}{4\pi\varepsilon_0 r^2}", r"\cdot", r"4\pi r^2", size=46,
                colors={1: CYAN, 3: VIOLET}).move_to(P(RX, 0.45))
        self.play(ReplacementTransform(b4, c1), Indicate(mlabs[1], color=VIOLET), run_time=1.4)
        self.at(c[9])
        _, _, den = frac_parts(c1[1])
        area = sorted(c1[3], key=lambda g: g.get_x())
        st_r = VGroup(strike(VGroup(*den[-2:]), WHITE), strike(VGroup(*area[2:4]), WHITE))
        st_4 = VGroup(strike(VGroup(*den[0:2]), WHITE), strike(VGroup(*area[0:2]), WHITE))
        self.play(Create(st_r), run_time=0.9)
        self.play(Create(st_4), run_time=0.7)
        self.at(c[10])
        c2 = eq(r"\Phi_E=", r"\frac{q}{\varepsilon_0}", size=54).move_to(P(RX, 0.45))
        bx = box(c2)
        self.play(FadeOut(VGroup(st_r, st_4)), ReplacementTransform(c1, c2), run_time=1.2)
        self.play(Create(bx), run_time=0.6)
        self.play(RR.animate.set_value(1.0), run_time=2.6)
        self.at(c[11])
        # última variação de raio com fluxo constante; a esfera fica no raio da deformação seguinte
        self.play(RR.animate.set_value(2.05), run_time=3.2)
        self.play(RR.animate.set_value(1.7), run_time=2.4)
        self.at(c[-1] + 0.3)
        self.k4 = SimpleNamespace(c=cc, sph=sph_, q=q)

    # ── 05 · Ângulo sólido (BUILD), interna × externa (COMPARE), Q_env ──────
    def b05_angulo_solido(self):
        self.begin(5, "angulo_solido")
        c = cues("Mas a superfície precisa mesmo ser uma esfera?",
                 "Imagine agora um pequeno cone de direções partindo da carga.",
                 "Esse cone intercepta um pedaço de uma superfície arbitrária.",
                 "Se o pedaço está inclinado, entra um fator de projeção. Se está mais distante, sua área precisa crescer proporcionalmente ao quadrado da distância para ocupar o mesmo tamanho angular visto pela carga.",
                 "A combinação entre área, inclinação e distância define um pequeno ângulo sólido.",
                 "E o fluxo produzido pela carga através daquele pedaço depende exatamente desse ângulo sólido orientado.",
                 "Se a superfície fechada envolve a carga, todos esses pequenos ângulos sólidos completam quatro pi.",
                 "Quatro pi é o ângulo sólido de todas as direções do espaço: a área de uma esfera de raio um, e não a volta de um círculo.",
                 "O resultado continua sendo q dividido por épsilon zero, independentemente da forma da superfície.",
                 "Agora coloque a carga fora.",
                 "O campo sobre a superfície não desaparece.",
                 "Pode até ser muito intenso em alguns lugares.",
                 "Mas cada feixe que entra numa região da superfície volta a sair por outra. Com a orientação correta, as contribuições se cancelam no fluxo líquido.",
                 "Por isso uma carga externa contribui zero para o fluxo total fechado.",
                 "E como campos elétricos obedecem ao princípio de superposição, podemos repetir o argumento para várias cargas.",
                 "As cargas externas cancelam no fluxo líquido.",
                 "As internas contribuem com suas cargas divididas por épsilon zero.",
                 "Somadas, elas formam a carga envolvida: a soma algébrica das cargas que estão dentro da superfície.",
                 "E chegamos à Lei de Gauss.",
                 "O fluxo do campo elétrico por qualquer superfície fechada é igual à carga total envolvida dividida por épsilon zero.")
        k4 = self.k4
        c4, c5, R4, BS = k4.c, P(-3.35, -0.25), 1.7, 1.95
        MO = ValueTracker(0.0)
        center = lambda: c4 + (c5 - c4) * MO.get_value()
        surf = always_redraw(lambda: dashed_curve(polar_pts(center(), lambda a: R4 * (1 - MO.get_value())
                                                            + BS * blob(a) * MO.get_value()), n=66))
        self.add(surf)
        self.remove(k4.sph)
        self.clear(k4.q, surf, run_time=0.8)
        self.play(MO.animate.set_value(1.0), k4.q.animate.shift(c5 - c4), run_time=2.4)   # esfera → superfície arbitrária
        surf.clear_updaters()
        cq = c5
        rb = lambda a: BS * blob(a)
        PH, CO, LO, LBO, SW, SWO = (ValueTracker(v) for v in (300.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        DL_ = 10.0
        refc =DashedVMobject(Circle(radius=0.62, arc_center=cq), num_dashes=22).set_stroke(WHITE, 1.5, 0.45)
        self.at(c[1])

        def cone():
            o, a = CO.get_value(), PH.get_value()
            if o < 0.01:
                return VGroup()
            pts = [cq] + [cq + (rb(t) + 0.45) * U(t) for t in np.linspace(a - DL_, a + DL_, 9)]
            arc_ = Arc(radius=0.62, start_angle=np.radians(a - DL_), angle=np.radians(2 * DL_), arc_center=cq)
            return VGroup(Polygon(*pts).set_stroke(WHITE, 1.5, 0.7 * o).set_fill(WHITE, 0.14 * o),
                          arc_.set_stroke(CYAN, 5, o))

        def geom(a):
            p = cq + rb(a) * U(a)
            n = blob_normal(BS, a)
            d = (ang(n) - a + 180) % 360 - 180
            chord = np.linalg.norm(rb(a + DL_) * U(a + DL_) - rb(a - DL_) * U(a - DL_))
            return p, n, d, chord

        def piece(a, o, full=True):
            """Elemento dA, normal n̂ (branca), distância r, ângulo θ (ciano) e área projetada dA cosθ."""
            out = VGroup()
            if o < 0.01:
                return out
            p, n, d, chord = geom(a)
            arcp = [cq + rb(t) * U(t) for t in np.linspace(a - DL_, a + DL_, 12)]
            out.add(VMobject().set_points_as_corners(arcp).set_stroke(VIOLET, 9, o))
            out.add(DashedLine(cq, p, dash_length=0.08).set_stroke(WHITE, 2, 0.7 * o))
            if full:
                out.add(vec(p, p + 0.72 * n, NCOL, 3.5, o, z=7))
                out.add(DashedLine(p, p + 0.72 * U(a), dash_length=0.06).set_stroke(CYAN, 2, 0.7 * o))
                if abs(d) > 4:
                    out.add(Arc(radius=0.45, start_angle=np.radians(a), angle=np.radians(d), arc_center=p).set_stroke(CYAN, 3, o))
                hp = 0.5 * chord * abs(np.cos(np.radians(d)))
                out.add(Line(p - hp * U(a + 90), p + hp * U(a + 90)).set_stroke(WHITE, 5, 0.9 * o).set_z_index(6))
            return out
        cone_m = always_redraw(cone)
        pc_m = always_redraw(lambda: piece(PH.get_value(), LO.get_value()))
        labs = VGroup(eq("r", size=32), eq(r"\hat n", size=32), eq(r"\theta", size=32, color=CYAN),
                      eq(r"dA\cos\theta", size=30), eq(r"d\Omega", size=30, color=CYAN))

        def place_labs(m):
            a = PH.get_value()
            p, n, d, chord = geom(a)
            o = LBO.get_value()
            m[0].move_to(cq + 0.62 * rb(a) * U(a) + 0.3 * U(a + 90))
            m[1].move_to(p + 1.0 * n + 0.12 * U(ang(n) - 90))
            m[2].move_to(p + 0.78 * U(a + d / 2) + 0.12 * U(a + d / 2 + 90 * np.sign(d or 1)))
            m[3].move_to(p + (0.5 * chord + 0.62) * U(a + 90) + 0.3 * U(a))
            m[4].move_to(cq + 1.0 * U(a - 30))
            for i, sub in enumerate(m):
                sub.set_opacity(o if i < 4 else CO.get_value())
        labs.add_updater(place_labs)
        self.add(cone_m, pc_m, labs)
        self.play(FadeIn(refc), CO.animate.set_value(1.0), run_time=1.4)
        self.at(c[2])
        self.play(LO.animate.set_value(1.0), run_time=1.2)
        self.at(c[3])
        s1 = eq(r"d\Phi_E", "=", r"\vec E\cdot d\vec A", size=42).move_to(P(RX, 1.85))
        s2 = eq(r"d\Phi_E", "=", r"\frac{q}{4\pi\varepsilon_0 r^2}", r"(\hat r\cdot\hat n)\,dA", size=42).move_to(P(RX, 1.85))
        s3 = eq(r"d\Phi_E", "=", r"\frac{q}{4\pi\varepsilon_0}", r"\frac{\cos\theta\,dA}{r^2}", size=42).move_to(P(RX, 1.85))
        self.play(LBO.animate.set_value(1.0), Write(s1), run_time=1.2)
        self.play(TransformMatchingTex(s1, s2), run_time=1.3)
        self.play(TransformMatchingTex(s2, s3), run_time=1.3)
        # mesmo cone, outro pedaço: mais longe e mais inclinado ⇒ área maior para o mesmo tamanho angular
        ghost = piece(300.0, 0.4, full=False)
        self.add(ghost)
        self.play(LBO.animate.set_value(0.0), run_time=0.4)
        self.play(PH.animate.set_value(360.0), run_time=3.0)
        self.play(LBO.animate.set_value(1.0), run_time=0.6)
        self.at(c[4])
        dom = eq(r"d\Omega_{\rm or}", "=", r"\frac{\cos\theta\,dA}{r^2}", size=42).move_to(P(RX, 0.7))
        self.play(TransformFromCopy(s3[3], dom[2]), FadeIn(dom[0:2]), run_time=1.4)
        dom_box = box(dom, CYAN)
        self.play(Create(dom_box), run_time=0.6)
        self.at(c[5])
        s4 = eq(r"d\Phi_E", "=", r"\frac{q}{4\pi\varepsilon_0}", r"\,d\Omega_{\rm or}", size=42).move_to(P(RX, 1.85))
        self.play(TransformMatchingTex(s3, s4), run_time=1.3)
        self.at(c[6])

        # carga interna: os ângulos sólidos completam 4π
        a0 = PH.get_value()
        sweep = always_redraw(lambda: sector_fill(cq, rb, a0, a0 + SW.get_value(), 0.12 * SWO.get_value())
                              if SW.get_value() > 1 else VMobject())
        self.remove(ghost)
        self.add(sweep)
        PH.add_updater(lambda m: m.set_value(a0 + SW.get_value()))
        self.add(PH)
        tot = eq(r"\oint_S d\Omega_{\rm or}", "=", r"4\pi", size=42).move_to(P(RX - 0.9, -0.5))
        self.play(SWO.animate.set_value(1.0), LO.animate.set_value(0.0), LBO.animate.set_value(0.0), run_time=0.3)
        self.play(SW.animate.set_value(360.0), run_time=4.0, rate_func=linear)
        self.play(Write(tot), run_time=1.0)
        PH.clear_updaters()
        self.remove(PH)
        self.at(c[7])
        # 4π em 3D: todas as direções do espaço = área da esfera de raio 1
        ic = P(RX + 2.35, -0.5)
        icon = VGroup(Circle(radius=0.5, arc_center=ic).set_stroke(WHITE, 2).set_fill(CYAN, 0.12),
                      DashedVMobject(Ellipse(width=1.0, height=0.3).move_to(ic), num_dashes=14).set_stroke(WHITE, 1.5, 0.6),
                      eq(r"4\pi", size=28).move_to(ic))
        icon_lab = text("esfera de raio 1", 20, opacity=0.85).move_to(ic + P(0, -0.8))
        self.play(FadeIn(icon, scale=0.7), FadeIn(icon_lab), run_time=1.0)
        self.at(c[8])
        res = eq(r"\Phi_E", "=", r"\frac{q}{4\pi\varepsilon_0}\cdot 4\pi", "=", r"\frac{q}{\varepsilon_0}", size=42)
        res.move_to(P(RX, -2.2))
        self.play(Write(res), run_time=1.4)
        self.at(c[9])

        # COMPARE: interna (4π) × externa (0); a carga externa continua produzindo campo na superfície
        for m in (cone_m, pc_m, labs, sweep):
            m.clear_updaters()
        left_grp = VGroup(surf, k4.q, refc, sweep, cone_m)
        self.play(FadeOut(VGroup(s4, dom, dom_box, res, pc_m, labs, icon, icon_lab)),
                  left_grp.animate.scale(0.62, about_point=cq).move_to(P(LX, 0.3)),
                  tot.animate.scale(0.85).move_to(P(LX, -2.35)), run_time=1.6)
        bc = P(RX + 0.25, 0.3)
        BS2 = BS * 0.62
        qe = P(RX - 2.35, 0.45)
        surf_r = dashed_curve(polar_pts(bc, lambda a: BS2 * blob(a)), n=48)
        qext = charge(qe, label="q")
        lab_in = text("carga interna", 24, opacity=0.8).move_to(P(LX, 2.3))
        lab_out = text("carga externa", 24, opacity=0.8).move_to(P(RX, 2.3))
        self.play(FadeIn(surf_r), FadeIn(qext, scale=0.5), FadeIn(lab_in), FadeIn(lab_out), run_time=1.0)
        self.at(c[10])
        ext_field = coulomb([bc + BS2 * blob(a) * U(a) for a in range(0, 360, 20)], [qe], 0.95, 0.12, 0.9, w=4)
        self.play(LaggedStart(*[GrowArrow(a) for a in ext_field], lag_ratio=0.05), run_time=2.2)
        self.at(c[11])
        self.play(LaggedStart(*[Indicate(a, color=CYAN, scale_factor=1.3) for a in ext_field[7:12]], lag_ratio=0.1), run_time=1.4)
        self.at(c[12])
        PE, CE = ValueTracker(-22.0), ValueTracker(0.0)
        DLe = 4.0

        def ext_geom(a):
            h1, h2 = ray_hits(qe, a - DLe, bc, BS2), ray_hits(qe, a + DLe, bc, BS2)
            far = max(h1[-1] if h1 else 3.5, h2[-1] if h2 else 3.5) + 0.45
            if len(h1) >= 2 and len(h2) >= 2:
                pin = (qe + h1[0] * U(a - DLe), qe + h2[0] * U(a + DLe))
                pout = (qe + h1[1] * U(a - DLe), qe + h2[1] * U(a + DLe))
                return far, pin, pout
            return far, None, None

        def ext_cone():
            o, a = CE.get_value(), PE.get_value()
            out = VGroup()
            if o < 0.01:
                return out
            far, pin, pout = ext_geom(a)
            out.add(Polygon(qe, qe + far * U(a - DLe), qe + far * U(a + DLe)).set_stroke(WHITE, 1.5, 0.6 * o)
                    .set_fill(WHITE, 0.12 * o))
            if pin is not None:
                out.add(Line(*pin).set_stroke(VIOLET, 8, o), Line(*pout).set_stroke(VIOLET, 8, o))
            return out
        ecm = always_redraw(ext_cone)
        signs = VGroup(eq(r"-d\Omega", size=32), eq(r"+d\Omega", size=32))

        def place_signs(m):
            a = PE.get_value()
            _, pin, pout = ext_geom(a)
            o = CE.get_value() if pin is not None else 0.0
            if pin is not None:
                m[0].move_to((pin[0] + pin[1]) / 2 - 0.5 * U(a) + 0.32 * U(a + 90))
                m[1].move_to((pout[0] + pout[1]) / 2 + 0.55 * U(a) + 0.1 * U(a + 90))
            m.set_opacity(o)
        signs.add_updater(place_signs)
        self.add(ecm, signs)
        self.play(CE.animate.set_value(1.0), run_time=0.8)
        self.play(PE.animate.set_value(22.0), run_time=4.2)
        self.play(PE.animate.set_value(6.0), run_time=1.6)
        self.at(c[13])
        tot_out = eq(r"\oint_S d\Omega_{\rm or}", "=", "0", size=42).scale(0.85).move_to(P(RX, -2.35))
        self.play(Write(tot_out), run_time=1.0)
        self.at(c[14])

        # superposição: cada carga recebe a sua contribuição para o fluxo → Q_env
        ecm.clear_updaters()
        signs.clear_updaters()
        self.clear(run_time=0.9)
        cF = P(-3.1, -0.2)
        rbF = lambda a: 1.55 * blob(a)
        qs_pos = [cF + P(-0.55, 0.35), cF + P(0.45, -0.5), cF + P(2.75, 1.55)]
        surfF = dashed_curve(polar_pts(cF, rbF), n=60)
        charges = VGroup(*[charge(p, label=lab) for p, lab in zip(qs_pos, ("q_1", "q_2", "q_3"))])
        fieldF = coulomb([cF + rbF(a) * U(a) for a in range(0, 360, 18)], qs_pos, 0.55, 0.12, 0.8, w=4)
        self.play(FadeIn(surfF), FadeIn(charges, scale=0.6), run_time=1.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in fieldF], lag_ratio=0.04), run_time=1.8)
        self.at(c[15])
        # contribuições fora da superfície, ligadas às cargas por guias tracejadas
        def tagged(lab, at_, q):
            lab.move_to(at_)
            start = lab.get_center() + (lab.width / 2 + 0.1) * np.sign(q[0] - at_[0]) * RIGHT
            lead = DashedLine(start, q + 0.18 * (start - q) / np.linalg.norm(start - q), dash_length=0.06).set_stroke(WHITE, 1.5, 0.6)
            return VGroup(lab, lead)
        k3 = tagged(hchain(eq("0", size=36), text("no fluxo", 20, opacity=0.85), buff=0.12), P(1.3, 1.85), qs_pos[2])
        self.play(Indicate(charges[2], color=WHITE, scale_factor=1.5), FadeIn(k3), run_time=1.2)
        self.at(c[16])
        k1 = tagged(eq(r"\frac{q_1}{\varepsilon_0}", size=36), P(0.85, 0.45), qs_pos[0])
        k2 = tagged(eq(r"\frac{q_2}{\varepsilon_0}", size=36), P(0.85, -0.75), qs_pos[1])
        self.play(FadeIn(k1), FadeIn(k2), run_time=1.0)
        self.at(c[17])
        qenv = eq(r"Q_{\mathrm{env}}", "=", "q_1", "+", "q_2", size=40, colors={0: BLUE_L}).move_to(P(4.4, -1.0))
        qenv_lab = text("soma algébrica das cargas internas", 22, opacity=0.85).move_to(P(4.4, -1.7))
        self.play(TransformFromCopy(VGroup(charges[0][2], charges[1][2]), VGroup(qenv[2], qenv[4])),
                  FadeIn(VGroup(qenv[0], qenv[1], qenv[3])), run_time=1.4)
        self.play(FadeIn(qenv_lab), run_time=0.8)
        self.at(c[18])
        law = eq(r"\oint_S", r"\vec E\cdot d\vec A", "=", r"\frac{Q_{\mathrm{env}}}{\varepsilon_0}", size=52).move_to(P(4.4, 0.65))
        self.play(Write(law), run_time=1.6)
        self.at(c[19])
        self.play(Create(box(law)), run_time=0.9)
        self.at(c[-1] + 0.6)

    # ── 06 · Superfície deliberadamente ruim (COMPARE / BUILD) ──────────────
    def b06_superficie_ruim(self):
        self.begin(6, "superficie_ruim")
        c = cues("Agora vem a parte mais importante do vídeo.",
                 "Se essa lei vale para qualquer superfície fechada, por que não desenhar qualquer uma e calcular o campo?",
                 "Coloque uma carga pontual deslocada do centro desta esfera.",
                 "A carga continua dentro.",
                 "Portanto o fluxo continua sendo q dividido por épsilon zero.",
                 "Isso é exato.",
                 "Mas olhe o campo sobre a superfície.",
                 "Os pontos da esfera não estão todos à mesma distância da carga.",
                 "Então o módulo de E varia de ponto para ponto.",
                 "E, na maior parte da esfera, o campo também não aponta na direção da normal.",
                 "Portanto este passo é inválido.",
                 "Eu não posso transformar a integral em E vezes a área da esfera.",
                 "A Lei de Gauss me deu um número: o fluxo total.",
                 "Mas o campo sobre a superfície é uma função que muda de ponto para ponto.",
                 "Saber o fluxo total não significa conhecer o campo em cada ponto.")
        self.clear(run_time=0.9)
        cc, RG = P(LX, 0.05), 1.9
        QO = ValueTracker(0.0)
        QV = np.array([0.95, 0.45, 0.0])
        qpos = lambda: cc + QO.get_value() * QV
        KE = 0.7 * RG ** 2
        sph_ = gauss_circle(cc, RG, n=34)
        center = VGroup(Line(cc + 0.1 * UL, cc + 0.1 * DR), Line(cc + 0.1 * UR, cc + 0.1 * DL)).set_stroke(WHITE, 2, 0.6)
        q = always_redraw(lambda: charge(qpos(), label="q"))
        pts = ring(cc, RG, 12, 0)
        arrows = always_redraw(lambda: coulomb(pts, [qpos()], KE, 0.12, 1.15))
        normals = VGroup(*[vec(p, p + 0.45 * U(a), NCOL, 3.5, z=5) for a, p in zip(range(0, 360, 30), pts)])
        self.play(Create(sph_), FadeIn(center), FadeIn(q), run_time=1.4)
        self.add(arrows)
        self.play(FadeIn(arrows), LaggedStart(*[GrowArrow(n) for n in normals], lag_ratio=0.05), run_time=1.6)
        self.at(c[1])
        fl = eq(r"\oint\vec E\cdot d\vec A", "=", r"\frac{q}{\varepsilon_0}", size=46).move_to(P(RX, 1.55))
        self.play(Write(fl), run_time=1.4)
        self.at(c[2])
        self.play(QO.animate.set_value(1.0), run_time=3.0)                    # deslocada, mas dentro
        self.at(c[3])
        self.play(Flash(qpos(), color=WHITE, line_length=0.18, flash_radius=0.3), run_time=0.9)
        self.at(c[4])
        self.play(Circumscribe(fl, color=WHITE, stroke_width=2), run_time=1.4)
        self.at(c[6])
        arrows.clear_updaters()
        q.clear_updaters()
        qp = qpos()
        dists = [np.linalg.norm(p - qp) for p in pts]
        i_near, i_far = int(np.argmin(dists)), int(np.argmax(dists))
        i_side = (i_near + 3) % 12
        three = (i_near, i_side, i_far)
        self.play(Indicate(sph_, color=VIOLET, scale_factor=1.02), run_time=1.0)
        # três pontos, um de cada vez: distância → módulo → ângulo
        self.at(c[7])
        dls = VGroup(*[DashedLine(qp, pts[i], dash_length=0.08).set_stroke(WHITE, 2, 0.75) for i in three])
        for d in dls:
            self.play(Create(d), run_time=0.8)
        self.at(c[8])
        dim = [a for j, a in enumerate(arrows) if j not in three]
        e_labs = VGroup()
        for k, i in enumerate(three):
            tip = arrows[i].get_end()
            e_labs.add(eq(f"E_{k + 1}", size=30, color=CYAN).move_to(tip + 0.3 * U(i * 30)))
        self.play(*[a.animate.set_opacity(0.3) for a in dim], LaggedStart(*[FadeIn(m, scale=0.6) for m in e_labs], lag_ratio=0.3),
                  run_time=1.4)
        ineq = eq("E_1", r"\neq", "E_2", r"\neq", "E_3", size=40, colors={0: CYAN, 2: CYAN, 4: CYAN}).move_to(P(RX, -1.2))
        self.play(FadeIn(ineq, shift=0.1 * UP), run_time=0.8)
        self.at(c[9])
        th_arcs = VGroup()
        for i in three:
            p = pts[i]
            e_dir = (p - qp) / np.linalg.norm(p - qp)
            d = (ang(e_dir) - i * 30 + 180) % 360 - 180
            th_arcs.add(VGroup(DashedLine(p, p + 1.0 * U(i * 30), dash_length=0.06).set_stroke(WHITE, 2, 0.9),
                               Arc(radius=0.65, start_angle=np.radians(i * 30), angle=np.radians(d), arc_center=p)
                               .set_stroke(CYAN, 4.5)))
        others = [nm for j, nm in enumerate(normals) if j not in three]
        self.play(*[nm.animate.set_opacity(0.3) for nm in others],
                  LaggedStart(*[Create(a) for a in th_arcs], lag_ratio=0.4), run_time=1.8)
        thn = eq(r"\theta_i\neq0", size=38, color=CYAN).move_to(P(RX, -1.95))
        self.play(FadeIn(thn, shift=0.1 * UP), run_time=0.7)
        self.at(c[10])
        tr = eq(r"\oint\vec E\cdot d\vec A", r"\overset{?}{=}", r"E\oint dA", size=46).move_to(P(RX, 0.15))
        self.play(Write(tr), run_time=1.3)
        self.at(c[11])
        bad = eq(r"\oint\vec E\cdot d\vec A", r"\neq", r"E\oint dA", size=46, colors={1: MAGENTA}).move_to(tr)
        cut = strike(bad[2], MAGENTA, 4)
        self.play(TransformMatchingTex(tr, bad), run_time=0.9)
        self.play(Create(cut), bad[2].animate.set_opacity(0.55), run_time=0.7)
        self.at(c[12])
        self.play(Indicate(fl[2], color=WHITE, scale_factor=1.3), FadeOut(VGroup(dls, e_labs, th_arcs)),
                  *[a.animate.set_opacity(1.0) for a in dim], *[nm.animate.set_opacity(1.0) for nm in others], run_time=1.2)
        self.at(c[13])
        # uma sonda percorre a esfera: distância, |E| e θ mudam continuamente
        PA, PRO = ValueTracker(0.0), ValueTracker(0.0)

        def probe():
            o = PRO.get_value()
            out = VGroup()
            if o < 0.01:
                return out
            a = PA.get_value()
            p = cc + RG * U(a)
            d = p - qp
            L = float(np.clip(KE / np.dot(d, d), 0.12, 1.3))
            e_dir = d / np.linalg.norm(d)
            dd = (ang(e_dir) - a + 180) % 360 - 180
            out.add(DashedLine(qp, p, dash_length=0.08).set_stroke(WHITE, 2, 0.7 * o),
                    Dot(p, radius=0.08, color=WHITE).set_opacity(o).set_z_index(9),
                    vec(p, p + L * e_dir, CYAN, 7, o, z=8), vec(p, p + 0.55 * U(a), NCOL, 4, o, z=9),
                    Arc(radius=0.42, start_angle=np.radians(a), angle=np.radians(dd), arc_center=p).set_stroke(CYAN, 3, o))
            return out
        prb = always_redraw(probe)
        pe = lambda: float(KE / np.dot(cc + RG * U(PA.get_value()) - qp, cc + RG * U(PA.get_value()) - qp))
        e_lab = eq(r"|\vec E|", size=36, color=CYAN).move_to(P(RX - 2.2, -1.2))
        e_bar = always_redraw(lambda: Rectangle(width=max(1.3 * pe(), 0.02), height=0.24).set_stroke(width=0)
                              .set_fill(CYAN, 0.85 * PRO.get_value()).next_to(P(RX - 1.6, -1.2), RIGHT, buff=0))
        t_lab = eq(r"\theta=", size=36, color=CYAN).move_to(P(RX - 1.9, -1.95))

        def theta_now():
            p = cc + RG * U(PA.get_value())
            e_dir = (p - qp) / np.linalg.norm(p - qp)
            return abs((ang(e_dir) - PA.get_value() + 180) % 360 - 180)
        t_val = DecimalNumber(0, num_decimal_places=0, unit=r"^\circ", font_size=36, color=CYAN)
        t_val.add_updater(lambda m: m.set_value(theta_now()).next_to(t_lab, RIGHT, buff=0.12).set_opacity(PRO.get_value()))
        self.add(prb, e_bar, t_val)
        self.play(FadeOut(VGroup(ineq, thn)), PRO.animate.set_value(1.0), FadeIn(e_lab), FadeIn(t_lab),
                  *[a.animate.set_opacity(0.35) for a in arrows], run_time=0.8)
        self.play(PA.animate.set_value(360.0), run_time=7.5, rate_func=linear)
        self.at(c[14])
        pay = hchain(display("FLUXO CONHECIDO", 32), eq(r"\neq", size=48, color=MAGENTA),
                     display("CAMPO LOCAL CONHECIDO", 32), buff=0.3).move_to(P(0, -2.8))
        self.play(FadeIn(pay, shift=0.12 * UP), run_time=1.4)
        self.at(c[-1] + 1.2)

    # ── 07 · Simetria da fonte (FOCUS) ──────────────────────────────────────
    def b07_simetria(self):
        self.begin(7, "simetria")
        c = cues("É aqui que entra a simetria.",
                 "E a ordem do raciocínio importa.",
                 "Você não começa escolhendo uma esfera porque quer que o problema fique esférico.",
                 "Você começa olhando para a distribuição de carga.",
                 "E forma esférica não basta. Uma bola com mais carga de um lado tem forma de esfera, mas, se eu girá-la, a fonte muda.",
                 "Pergunte: quais transformações deixam essa fonte fisicamente igual?",
                 "Considere uma distribuição esfericamente simétrica.",
                 "Se eu girá-la em torno do centro, nada muda.",
                 "Não existe nenhuma direção tangencial privilegiada.",
                 "O campo produzido por essa distribuição precisa apontar radialmente, e seu módulo só pode depender da distância ao centro.",
                 "Se eu me mover mantendo a mesma distância ao centro, a direção do campo muda, mas o módulo é sempre o mesmo.",
                 "Só depois de descobrir isso escolhemos uma esfera concêntrica.",
                 "Nessa esfera, o campo é paralelo ao vetor área.",
                 "E como todos os pontos têm o mesmo raio, o módulo do campo é constante.",
                 "Agora, e somente agora, podemos tirar E da integral.",
                 "A esfera gaussiana não criou a simetria.",
                 "Ela apenas explorou uma simetria que a distribuição de carga já possuía.")
        self.at(c[2] - 0.8)
        self.clear(run_time=0.8)
        cs = P(-2.4, 0.0)
        RS = 1.75
        pre = gauss_circle(cs, RS, n=30)
        self.play(Create(pre), run_time=1.2)
        cut = strike(pre, MAGENTA, 4)
        self.play(Create(cut), run_time=0.7)
        self.play(FadeOut(VGroup(pre, cut)), run_time=0.8)
        self.at(c[3])
        src = VGroup(*[Circle(radius=r, arc_center=cs).set_stroke(width=0).set_fill(BLUE, 0.17) for r in (1.15, 0.8, 0.45)])
        src[0].set_stroke(BLUE_L, 3)
        guides = VGroup(DashedVMobject(Ellipse(width=2.3, height=0.6).move_to(cs), num_dashes=22),
                        DashedVMobject(Ellipse(width=0.6, height=2.3).move_to(cs), num_dashes=22)).set_stroke(BLUE_L, 1.5, 0.55)
        source = VGroup(src, guides)
        lab_sym = text("simetria esférica", 22, opacity=0.85).move_to(cs + P(0, -2.05))
        self.play(FadeIn(source), FadeIn(lab_sym), run_time=1.2)
        self.at(c[4])
        # forma esférica ≠ simetria esférica: carga concentrada de um lado muda ao girar
        ca = P(2.9, 0.0)
        asym = VGroup(Circle(radius=1.15, arc_center=ca).set_stroke(BLUE_L, 3).set_fill(BLUE, 0.12),
                      Circle(radius=0.55, arc_center=ca + 0.45 * U(130)).set_stroke(width=0).set_fill(BLUE, 0.5),
                      DashedVMobject(Ellipse(width=2.3, height=0.6).move_to(ca), num_dashes=22).set_stroke(BLUE_L, 1.5, 0.55))
        lab_asym = text("forma esférica, carga não simétrica", 22, opacity=0.85).move_to(ca + P(0, -2.05))
        self.play(FadeIn(asym), FadeIn(lab_asym), run_time=1.2)
        self.play(Rotate(asym, -PI / 2, about_point=ca), run_time=2.0)
        self.at(c[5])
        rot = VGroup(Arc(radius=1.55, start_angle=np.radians(20), angle=np.radians(110), arc_center=cs),
                     Arc(radius=1.55, start_angle=np.radians(200), angle=np.radians(110), arc_center=cs)).set_stroke(WHITE, 2.5, 0.75)
        for a in rot:
            a.add_tip(tip_length=0.18)
        self.play(FadeIn(rot), run_time=0.6)
        self.play(Rotate(source, 2 * PI / 3, about_point=cs), Rotate(rot, 2 * PI / 3, about_point=cs),
                  Rotate(asym, 2 * PI / 3, about_point=ca), run_time=2.4)
        self.at(c[6])
        self.play(FadeOut(VGroup(asym, lab_asym)), Indicate(src, color=BLUE_L, scale_factor=1.04), run_time=1.0)
        self.at(c[7])
        self.play(Rotate(source, -PI / 2, about_point=cs), Rotate(rot, -PI / 2, about_point=cs), run_time=2.0)
        self.play(FadeOut(rot), FadeOut(lab_sym), run_time=0.5)
        self.at(c[8])
        # componente tangencial hipotética: girar 180° em torno do eixo OP leva a fonte nela mesma e a inverte
        a_p = 20.0
        p = cs + RS * U(a_p)
        axis = DashedLine(cs, cs + (RS + 1.0) * U(a_p), dash_length=0.08).set_stroke(WHITE, 2, 0.6)
        hyp = vec(p, p + 1.05 * U(a_p + 50), MAGENTA, 6)
        hyp_lab = text("componente tangencial hipotética", 20, MAGENTA).move_to(p + P(0.6, 1.25))
        self.play(Create(axis), GrowArrow(hyp), FadeIn(hyp_lab), run_time=1.0)
        ghost = hyp.copy().set_opacity(0.35)
        self.add(ghost)
        self.play(Rotate(hyp, PI, axis=U(a_p), about_point=p), run_time=1.8)
        self.wait(0.4)
        radial = vec(p, p + 0.62 * U(a_p), CYAN, 5)
        self.play(ReplacementTransform(VGroup(hyp, ghost), radial), FadeOut(hyp_lab), run_time=1.0)
        self.at(c[9])
        arrows = VGroup(*[vec(cs + RS * U(a), cs + (RS + 0.55) * U(a), CYAN, 5) for a in range(int(a_p) + 30, int(a_p) + 360, 30)])
        self.play(FadeOut(axis), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.06), run_time=2.0)
        form = eq(r"\vec E(\vec r)", "=", "E(r)", r"\hat r", size=54, colors={0: CYAN, 2: CYAN}).move_to(P(3.5, 1.15))
        self.play(Write(form), run_time=1.4)
        self.at(c[10])
        # sonda à mesma distância do centro: direção muda, módulo não
        PA, PRO = ValueTracker(a_p), ValueTracker(0.0)
        path = DashedVMobject(Circle(radius=RS + 0.8, arc_center=cs), num_dashes=40).set_stroke(WHITE, 1.5, 0.45)
        prb = always_redraw(lambda: VGroup(
            Dot(cs + (RS + 0.8) * U(PA.get_value()), radius=0.08, color=WHITE).set_opacity(PRO.get_value()).set_z_index(9),
            vec(cs + (RS + 0.8) * U(PA.get_value()), cs + (RS + 1.45) * U(PA.get_value()), CYAN, 7, PRO.get_value(), z=8)))
        e_lab = eq(r"|\vec E|", size=36, color=CYAN).move_to(P(1.6, -0.35))
        e_bar = Rectangle(width=2.2, height=0.24).set_stroke(width=0).set_fill(CYAN, 0.85).next_to(P(2.15, -0.35), RIGHT, buff=0)
        e_txt = text("o mesmo em todo o percurso", 20, opacity=0.85).next_to(e_bar, DOWN, buff=0.15)
        self.add(prb)
        self.play(Create(path), PRO.animate.set_value(1.0), FadeIn(e_lab), FadeIn(e_bar), FadeIn(e_txt),
                  arrows.animate.set_opacity(0.35), radial.animate.set_opacity(0.35), run_time=0.9)
        self.play(PA.animate.set_value(a_p + 360), run_time=4.8, rate_func=linear)
        self.at(c[11])
        prb.clear_updaters()
        gs = gauss_circle(cs, RS, n=30)
        self.play(FadeOut(VGroup(path, prb, e_lab, e_bar, e_txt)), arrows.animate.set_opacity(1.0),
                  radial.animate.set_opacity(1.0), run_time=0.8)
        self.play(Create(gs), run_time=1.4)
        self.at(c[12])
        normals = VGroup(*[vec(cs + RS * U(a), cs + (RS + 0.32) * U(a), NCOL, 3.5, z=5) for a in range(int(a_p) + 15, int(a_p) + 375, 30)])
        self.play(LaggedStart(*[GrowArrow(n) for n in normals], lag_ratio=0.05), run_time=1.4)
        self.at(c[13])
        self.play(Indicate(VGroup(arrows, radial), color=CYAN, scale_factor=1.06), run_time=1.4)
        self.at(c[14])
        g1 = eq(r"\oint\vec E\cdot d\vec A", "=", "E(r)", r"\oint dA", size=42, colors={2: CYAN}).move_to(P(3.5, -0.3))
        g2 = eq(r"\oint\vec E\cdot d\vec A", "=", "E(r)", r"\,4\pi r^2", size=42, colors={2: CYAN}).move_to(P(3.5, -0.3))
        self.play(Write(g1), run_time=1.3)
        self.play(TransformMatchingTex(g1, g2), run_time=1.1)
        self.at(c[15])
        m1 = display("A SUPERFÍCIE EXPLORA A SIMETRIA.", 30)
        m2 = display("ELA NÃO A CRIA.", 30)
        hchain(m1, m2, buff=0.4).move_to(P(0, -2.65))
        self.play(FadeIn(m1, shift=0.1 * UP), Indicate(gs, color=VIOLET, scale_factor=1.03), run_time=1.2)
        self.at(c[16])
        self.play(FadeIn(m2, shift=0.1 * UP), Indicate(src, color=BLUE_L, scale_factor=1.05), run_time=1.2)
        self.at(c[-1] + 1.0)

    # ── 08 · Esfera uniforme: interior, coordenadas esféricas, exterior (SPLIT / BUILD) ──
    def b08_esfera_uniforme(self):
        self.begin(8, "esfera_uniforme")
        c = cues("Vamos usar isso numa esfera isolante com densidade volumétrica uniforme.",                    # 0
                 "Primeiro queremos o campo num ponto dentro da esfera.",
                 "Pela simetria, sabemos antes de fazer qualquer conta que o campo é radial e depende apenas da distância ao centro.",
                 "Escolhemos então uma superfície gaussiana esférica de raio menor que o raio da esfera física.",
                 "O lado do fluxo fica simples: campo vezes a área da superfície gaussiana.",
                 "Agora precisamos da carga realmente envolvida por ela.",                                       # 5
                 "Como a densidade é uniforme, poderíamos simplesmente multiplicar densidade por volume.",
                 "Mas vale a pena enxergar a versão que também funcionará quando a densidade deixar de ser constante.",
                 "Para isso, vale relembrar as coordenadas esféricas. E repare em três letras parecidas: R maiúsculo é o raio fixo da esfera física; r é o raio da superfície gaussiana, onde medimos o campo; e r linha é a variável que percorre o volume durante a integração.",
                 "Um ponto do volume fica determinado por três números. Primeiro, a distância r linha até o centro.",
                 "Depois, o ângulo polar, medido a partir do eixo z. Vamos escrevê-lo com outra grafia de teta, para não confundir com o ângulo do fluxo.",  # 10
                 "Por fim, o ângulo azimutal, fi, que dá a volta em torno do eixo z.",
                 "Variando cada coordenada um pouquinho, formamos um pequeno bloco. Na direção radial, sua espessura é d r linha.",
                 "Na direção polar, o arco tem comprimento r linha vezes d teta.",
                 "Na direção azimutal, o ponto gira num círculo de raio r linha seno de teta, um círculo que encolhe perto dos polos. Por isso esse arco mede r linha seno de teta d fi.",
                 "Multiplicando as três dimensões, temos o elemento de volume.",                                 # 15
                 "Integramos a densidade com r linha indo de zero até r, porque só conta a carga que está dentro da superfície gaussiana.",
                 "Para densidade constante, o resultado é exatamente a densidade vezes quatro terços de pi vezes o raio ao cubo.",
                 "Substituindo na Lei de Gauss, primeiro cancelamos quatro pi dos dois lados.",
                 "Depois, o raio ao cubo da carga dividido pelo raio ao quadrado da área deixa um único fator de raio.",
                 "Por isso, dentro da esfera uniforme, o campo cresce linearmente com a distância ao centro. Esse resultado vale só para r menor que R.",  # 20
                 "No centro ele vale zero.",
                 "Agora mova a superfície gaussiana para fora da esfera física.",
                 "A partir daqui, aumentar o raio da superfície não envolve mais carga.",
                 "Toda a carga da esfera já está dentro.",
                 "Então a carga envolvida fica constante, enquanto a área gaussiana continua crescendo como o raio ao quadrado.",  # 25
                 "O campo passa a cair como um sobre o raio ao quadrado. Agora o resultado vale para r maior que R.",
                 "E, para pontos externos a toda a região ocupada por essa distribuição esfericamente simétrica, o resultado é exatamente o mesmo campo que seria produzido por uma carga pontual com a carga total da esfera colocada no centro.")
        self.clear(run_time=0.9)
        cc = P(LX, -0.15)
        S, X = ValueTracker(2.0), ValueTracker(0.55)                          # S: unidades de tela por R; X = r/R
        PO, GO, AO, EQO, SFO, VEO = (ValueTracker(v) for v in (0.0, 0.0, 0.0, 0.0, 1.0, 0.0))
        A_R, A_P = 145.0, -20.0
        EL = 1.15

        def body():
            s, sf = S.get_value(), SFO.get_value()
            return VGroup(Circle(radius=s, arc_center=cc).set_stroke(BLUE_L, 3.5).set_fill(BLUE, 0.2 * sf),
                          DashedVMobject(Ellipse(width=2 * s, height=2 * EL_S * s).move_to(cc), num_dashes=28)
                          .set_stroke(BLUE_L, 1.5, 0.4),
                          Line(cc, cc + s * U(A_R)).set_stroke(BLUE_L, 3))
        sphere = always_redraw(body)
        envol = always_redraw(lambda: Circle(radius=max(min(X.get_value(), 1.0) * S.get_value(), 1e-3), arc_center=cc)
                              .set_stroke(width=0).set_fill(VIOLET, 0.2 * EQO.get_value()).set_z_index(1)
                              if EQO.get_value() > 0.01 else VMobject())
        rlab_R = eq("R", size=36, color=BLUE_L)
        rlab_R.add_updater(lambda m: m.move_to(cc + 0.55 * S.get_value() * U(A_R) + 0.26 * U(A_R + 90)))

        def gauss():
            o, r = GO.get_value(), X.get_value() * S.get_value()
            if o < 0.01 or r < 0.02:
                return VGroup()
            return VGroup(gauss_circle(cc, r, op=o), Line(cc, cc + r * U(A_P)).set_stroke(VIOLET, 3, o)).set_z_index(2)
        gs = always_redraw(gauss)
        rlab = eq("r", size=36, color=VIOLET)
        rlab.add_updater(lambda m: m.move_to(cc + 0.5 * X.get_value() * S.get_value() * U(A_P) + 0.26 * U(A_P - 90))
                         .set_opacity(GO.get_value() if X.get_value() * S.get_value() > 0.5 else 0))
        lab_env = text("volume envolvido", 20, VIOLET)
        lab_env.add_updater(lambda m: m.move_to(cc + 0.4 * min(X.get_value(), 1.0) * S.get_value() * UP)
                            .set_opacity(EQO.get_value() * VEO.get_value()))

        def field():
            x, s = X.get_value(), S.get_value()
            out = VGroup()
            L = EL * f_graph(x)
            p = cc + x * s * U(A_P)
            if PO.get_value() > 0.01:
                out.add(Dot(p, radius=0.07, color=WHITE).set_opacity(PO.get_value()).set_z_index(6))
                out.add(vec(p, p + L * U(A_P), CYAN, 5, PO.get_value()))
            if AO.get_value() > 0.01:
                for a in range(int(A_P) + 45, int(A_P) + 360, 45):
                    q = cc + x * s * U(a)
                    out.add(vec(q, q + L * U(a), CYAN, 4, 0.8 * AO.get_value()))
            return out
        fld = always_redraw(field)
        self.add(sphere, envol, gs, fld, lab_env)
        self.play(FadeIn(sphere), FadeIn(rlab_R), run_time=1.4)
        rho = eq(r"\rho", size=40, color=BLUE_L).move_to(cc + 1.6 * U(112))
        self.play(FadeIn(rho), run_time=0.6)
        self.at(c[1])
        self.play(PO.animate.set_value(1.0), run_time=0.8)
        self.at(c[2])
        self.play(AO.animate.set_value(1.0), run_time=1.2)
        self.at(c[3])
        self.add(rlab)
        rr = eq("r<R", size=36).move_to(P(LX + 2.4, 2.25))
        self.play(GO.animate.set_value(1.0), FadeIn(rr), run_time=1.4)
        self.at(c[4])
        g1 = eq("E(r)", r"\,4\pi r^2", "=", r"\frac{Q_{\mathrm{env}}}{\varepsilon_0}", size=44, colors={0: CYAN}).move_to(P(RX, 1.9))
        self.play(Write(g1), run_time=1.4)
        self.play(Indicate(g1[0:2], color=WHITE), run_time=1.0)
        self.at(c[5])
        self.play(EQO.animate.set_value(1.0), VEO.animate.set_value(1.0), Indicate(g1[3], color=WHITE), run_time=1.2)
        self.at(c[6])
        q0 = eq(r"Q_{\mathrm{env}}", "=", r"\rho\,V_{\mathrm{env}}", size=42).move_to(P(RX, 0.7))
        self.play(FadeIn(q0, shift=0.1 * UP), run_time=1.0)
        self.at(c[7])
        q1 = eq(r"Q_{\mathrm{env}}", "=", r"\int_V\rho\,dV", size=42).move_to(P(RX, 0.7))
        self.play(TransformMatchingTex(q0, q1), run_time=1.2)
        self.at(c[8])

        # ── parêntese: coordenadas esféricas (r', ϑ, φ) e o elemento de volume ──
        RP, TT, FF = ValueTracker(0.72), ValueTracker(50.0), ValueTracker(-50.0)
        ZO, PTO, THO, PHO, AZO, VO, LBO = (ValueTracker(0.0) for _ in range(7))
        DR_, DT_, DF_ = 0.2, 20.0, 30.0
        pt3 = lambda: p3(cc, S.get_value(), sph(RP.get_value(), TT.get_value(), FF.get_value()))

        def coords():
            s, rp, tt, ff = S.get_value(), RP.get_value(), TT.get_value(), FF.get_value()
            out = VGroup()
            if ZO.get_value() > 0.01:
                o = ZO.get_value()
                out.add(DashedLine(p3(cc, s, (0, 0, -1.1)), p3(cc, s, (0, 0, 1.18)), dash_length=0.08).set_stroke(WHITE, 2, 0.6 * o))
            if PTO.get_value() > 0.01:
                o = PTO.get_value()
                p = pt3()
                out.add(Line(cc, p).set_stroke(WHITE, 3, o), Dot(p, radius=0.07, color=WHITE).set_opacity(o).set_z_index(9))
            if THO.get_value() > 0.01:
                o = THO.get_value()
                out.add(VMobject().set_points_as_corners([p3(cc, s, sph(0.3, t, ff)) for t in np.linspace(0, tt, 16)])
                        .set_stroke(WHITE, 3, o))
            if PHO.get_value() > 0.01:
                o = PHO.get_value()
                v = sph(rp, tt, ff)
                foot = p3(cc, s, (v[0], v[1], 0.0))
                out.add(DashedLine(cc, p3(cc, s, (1.12, 0, 0)), dash_length=0.08).set_stroke(WHITE, 1.5, 0.5 * o),
                        DashedLine(cc, foot, dash_length=0.06).set_stroke(WHITE, 1.5, 0.6 * o),
                        DashedLine(pt3(), foot, dash_length=0.06).set_stroke(WHITE, 1.5, 0.6 * o),
                        VMobject().set_points_as_corners([p3(cc, s, sph(0.28, 90, f)) for f in np.linspace(0, ff, 16)])
                        .set_stroke(WHITE, 3, o))
            if AZO.get_value() > 0.01:
                o = AZO.get_value()
                v = sph(rp, tt, ff)
                axis_pt = p3(cc, s, (0, 0, v[2]))
                out.add(DashedVMobject(VMobject().set_points_as_corners([p3(cc, s, sph(rp, tt, f)) for f in np.linspace(0, 360, 73)]),
                                       num_dashes=36).set_stroke(WHITE, 2, 0.75 * o),
                        Line(axis_pt, pt3()).set_stroke(WHITE, 2.5, o))
            return out.set_z_index(8)
        crd = always_redraw(coords)
        HL = {"r": ValueTracker(0.0), "t": ValueTracker(0.0), "f": ValueTracker(0.0)}

        def corner(i, j, k):
            return p3(cc, S.get_value(), sph(RP.get_value() + (i - 0.5) * DR_, TT.get_value() + (j - 0.5) * DT_,
                                              FF.get_value() + (k - 0.5) * DF_))

        def element():
            o = VO.get_value()
            out = VGroup()
            if o < 0.01:
                return out
            C = {(i, j, k): corner(i, j, k) for i in (0, 1) for j in (0, 1) for k in (0, 1)}
            out.add(Polygon(C[1, 0, 0], C[1, 0, 1], C[1, 1, 1], C[1, 1, 0]).set_stroke(WHITE, 1.5, o).set_fill(WHITE, 0.4 * o))
            out.add(Polygon(C[0, 0, 0], C[0, 0, 1], C[0, 1, 1], C[0, 1, 0]).set_stroke(WHITE, 1.2, 0.6 * o).set_fill(WHITE, 0.1 * o))
            for j in (0, 1):
                for k in (0, 1):
                    out.add(Line(C[0, j, k], C[1, j, k]).set_stroke(WHITE, 1.2, 0.7 * o))
            # as três arestas que partem do mesmo vértice: radial, polar e azimutal
            for key, (a, b) in (("r", ((0, 0, 0), (1, 0, 0))), ("t", ((1, 0, 0), (1, 1, 0))), ("f", ((1, 0, 0), (1, 0, 1)))):
                h = HL[key].get_value()
                if h > 0.01:
                    out.add(Line(C[a], C[b]).set_stroke(CYAN if key == "f" else WHITE, 6, o * h).set_z_index(10))
            return out.set_z_index(9)
        elem = always_redraw(element)
        clabs = VGroup(eq("r'", size=32), eq(r"\vartheta", size=32), eq(r"\phi", size=32), eq("z", size=28),
                       eq("dr'", size=28), eq(r"r'\,d\vartheta", size=28), eq(r"r'\sin\vartheta\,d\phi", size=28, color=CYAN))

        def place_clabs(m):
            s, rp, tt, ff = S.get_value(), RP.get_value(), TT.get_value(), FF.get_value()
            o = LBO.get_value()
            m[0].move_to((cc + pt3()) / 2 + 0.28 * U(ang(pt3() - cc) + 90)).set_opacity(PTO.get_value() * o)
            m[1].move_to(p3(cc, s, sph(0.48, tt / 2, ff))).set_opacity(THO.get_value() * o)
            m[2].move_to(p3(cc, s, sph(0.45, 90, ff / 2)) + P(0.05, -0.12)).set_opacity(PHO.get_value() * o)
            m[3].move_to(p3(cc, s, (0, 0, 1.18)) + P(0.25, 0.05)).set_opacity(ZO.get_value() * o)
            C100, C000, C110, C101 = corner(1, 0, 0), corner(0, 0, 0), corner(1, 1, 0), corner(1, 0, 1)
            out_dir = (C100 - cc) / max(np.linalg.norm(C100 - cc), 1e-6)
            m[4].move_to((C100 + C000) / 2 + 0.32 * np.array([out_dir[1], -out_dir[0], 0]) * -1).set_opacity(HL["r"].get_value() * o)
            m[5].move_to((C100 + C110) / 2 + 0.55 * out_dir).set_opacity(HL["t"].get_value() * o)
            m[6].move_to((C100 + C101) / 2 + P(0.85, -0.25)).set_opacity(HL["f"].get_value() * o)
        clabs.add_updater(place_clabs)
        self.add(crd, elem, clabs)
        rowR = left_at(hchain(eq("R", size=36, color=BLUE_L), text("raio fixo da esfera física", 22, opacity=0.85)), 0.8, 1.15)
        rowr = left_at(hchain(eq("r", size=36, color=VIOLET), text("raio da gaussiana, onde medimos o campo", 22, opacity=0.85)), 0.8, 0.55)
        rowp = left_at(hchain(eq("r'", size=36), text("variável que percorre o volume", 22, opacity=0.85)), 0.8, -0.05)
        self.play(FadeOut(VGroup(g1, rho, rr)), q1.animate.scale(0.85).move_to(P(RX, 2.25)), AO.animate.set_value(0.0),
                  PO.animate.set_value(0.0), VEO.animate.set_value(0.0), S.animate.set_value(2.75), X.animate.set_value(0.88),
                  ZO.animate.set_value(1.0), LBO.animate.set_value(1.0), run_time=1.6)
        self.at(c[8] + 5.6)
        self.play(FadeIn(rowR, shift=0.1 * DOWN), Indicate(rlab_R, color=BLUE_L, scale_factor=1.4), run_time=1.0)
        self.at(c[8] + 8.8)
        self.play(FadeIn(rowr, shift=0.1 * DOWN), Indicate(rlab, color=VIOLET, scale_factor=1.4), run_time=1.0)
        self.at(c[8] + 12.6)
        self.play(FadeIn(rowp, shift=0.1 * DOWN), PTO.animate.set_value(1.0), run_time=1.0)
        self.at(c[9])
        self.play(RP.animate.set_value(0.15), run_time=0.8)
        self.play(RP.animate.set_value(0.72), run_time=2.2)                  # r': distância ao centro
        self.at(c[10])
        note = left_at(hchain(eq(r"\vartheta", size=36), text("ângulo polar", 22, opacity=0.85), eq(r"\neq", size=32),
                              eq(r"\theta", size=36, color=CYAN), text("ângulo do fluxo", 22, opacity=0.85)), 0.8, -0.75)
        self.play(THO.animate.set_value(1.0), FadeIn(note, shift=0.1 * DOWN), run_time=1.0)
        self.play(TT.animate.set_value(22.0), run_time=1.4)
        self.play(TT.animate.set_value(72.0), run_time=1.8)
        self.play(TT.animate.set_value(50.0), run_time=1.2)
        self.at(c[11])
        self.play(PHO.animate.set_value(1.0), run_time=0.8)
        self.play(FF.animate.set_value(310.0), run_time=4.6, rate_func=linear)   # uma volta em torno de z
        FF.set_value(-50.0)
        self.at(c[12])
        self.play(FadeOut(VGroup(rowR, rowr, rowp, note)), VO.animate.set_value(1.0), PHO.animate.set_value(0.35),
                  THO.animate.set_value(0.6), run_time=1.0)
        self.play(HL["r"].animate.set_value(1.0), run_time=0.8)
        self.at(c[13])
        self.play(HL["t"].animate.set_value(1.0), run_time=0.8)
        self.at(c[14])
        self.play(AZO.animate.set_value(1.0), run_time=0.9)
        # o raio do círculo azimutal é r' sinϑ: encolhe perto do polo
        self.play(TT.animate.set_value(16.0), run_time=2.0)
        self.play(TT.animate.set_value(50.0), run_time=1.8)
        self.play(HL["f"].animate.set_value(1.0), run_time=0.8)
        self.at(c[15])
        dvp = eq("dV", "=", "dr'", r"\cdot", r"r'\,d\vartheta", r"\cdot", r"r'\sin\vartheta\,d\phi", size=40,
                 colors={6: CYAN}).move_to(P(RX, 1.35))
        brs = VGroup(*[Brace(dvp[i], DOWN, buff=0.08) for i in (2, 4, 6)])
        blab = VGroup(*[text(t, 20, opacity=0.85).next_to(b, DOWN, buff=0.06) for t, b in zip(("radial", "polar", "azimutal"), brs)])
        self.play(Write(dvp), run_time=1.4)
        self.play(FadeIn(brs), FadeIn(blab), run_time=0.8)
        self.wait(0.8)
        dv2 = eq("dV", "=", r"r'^2\sin\vartheta\,dr'\,d\vartheta\,d\phi", size=40).move_to(P(RX, 1.35))
        self.flatten(dvp)
        self.play(FadeOut(VGroup(brs, blab)), ReplacementTransform(dvp[0], dv2[0]), ReplacementTransform(dvp[1], dv2[1]),
                  ReplacementTransform(VGroup(*dvp[2:]), dv2[2]), run_time=1.3)
        self.regroup(dv2)
        self.at(c[16])
        # só a carga dentro da gaussiana conta: r' varre de 0 até r, e o elemento fica dentro do volume envolvido
        qi = eq(r"Q_{\mathrm{env}}=\rho", r"\int_0^r r'^2dr'", r"\int_0^\pi\sin\vartheta\,d\vartheta", r"\int_0^{2\pi}d\phi", size=38)
        fit(qi, _R.width - 0.3).move_to(P(RX, 0.05))
        self.play(TransformMatchingTex(q1, qi), LBO.animate.set_value(0.0), AZO.animate.set_value(0.0),
                  PHO.animate.set_value(0.0), THO.animate.set_value(0.0), *[h.animate.set_value(0.0) for h in HL.values()],
                  VEO.animate.set_value(1.0), run_time=1.3)
        self.play(RP.animate.set_value(0.1), run_time=0.8)
        self.play(RP.animate.set_value(X.get_value() - DR_ / 2 - 0.02), Indicate(qi[1], color=VIOLET), run_time=2.6, rate_func=linear)
        self.at(c[17])
        vals = [eq(r"\frac{r^3}{3}", size=36), eq("2", size=36), eq(r"2\pi", size=36)]
        bq = VGroup()
        for i, v in zip((1, 2, 3), vals):
            b = Brace(qi[i], DOWN, buff=0.08)
            v.next_to(b, DOWN, buff=0.08)
            bq.add(b, v)
            self.play(FadeIn(b), FadeIn(v, shift=0.1 * DOWN), run_time=0.7)
        qr = eq(r"Q_{\mathrm{env}}", "=", r"\frac43\pi\rho r^3", size=44, colors={0: BLUE_L}).move_to(P(RX, -2.1))
        self.play(TransformFromCopy(VGroup(*vals), qr[2]), FadeIn(qr[0:2]), run_time=1.3)
        self.at(c[18])

        # Gauss interior: uma operação por passo
        for m in (crd, elem, clabs):
            m.clear_updaters()
        self.play(FadeOut(VGroup(crd, elem, clabs, dv2, qi, bq)), qr.animate.scale(0.8).move_to(P(RX, 2.25)),
                  S.animate.set_value(2.0), X.animate.set_value(0.55), AO.animate.set_value(1.0), PO.animate.set_value(1.0),
                  FadeIn(rho), FadeIn(rr), run_time=1.3)
        Y = 0.9
        h0 = eq("E(r)", r"\,4\pi", r"\,r^2", "=", r"\frac{Q_{\mathrm{env}}}{\varepsilon_0}", size=46,
                colors={0: CYAN, 2: VIOLET}).move_to(P(RX, Y))
        h1 = eq("E(r)", r"\,4\pi", r"\,r^2", "=", r"\frac{1}{3\varepsilon_0}", r"\,4\pi", r"\,\rho", r"\,r^3", size=46,
                colors={0: CYAN, 2: VIOLET, 7: VIOLET}).move_to(P(RX, Y))
        h2 = eq("E(r)", r"\,r^2", "=", r"\frac{1}{3\varepsilon_0}", r"\,\rho", r"\,r^3", size=46,
                colors={0: CYAN, 1: VIOLET, 5: VIOLET}).move_to(P(RX, Y))
        h3 = eq("E(r)", "=", r"\frac{1}{3\varepsilon_0}", r"\,\rho", r"\,r", size=46, colors={0: CYAN, 4: VIOLET}).move_to(P(RX, Y))
        h4 = eq("E(r)", "=", r"\frac{\rho r}{3\varepsilon_0}", size=52, colors={0: CYAN}).move_to(P(RX, Y))
        self.play(FadeIn(h0, shift=0.1 * UP), run_time=0.9)
        self.play(TransformMatchingTex(h0, h1), Indicate(qr, color=WHITE), run_time=1.3)       # substituir Q_env
        st = VGroup(strike(h1[1], WHITE), strike(h1[5], WHITE))
        self.play(Create(st), run_time=0.8)                                                    # cancelar 4π
        self.play(FadeOut(st), h1[1].animate.set_opacity(0), h1[5].animate.set_opacity(0), run_time=0.6)   # some no lugar
        self.remove(h1)
        rest = [h1[i] for i in (0, 2, 3, 4, 6, 7)]
        self.add(*rest)
        self.play(*[ReplacementTransform(a, b) for a, b in zip(rest, h2)], run_time=1.0)
        self.regroup(h2)
        self.at(c[19])
        note = eq(r"\frac{r^3}{r^2}=r", size=38, color=VIOLET).move_to(P(RX, -0.35))
        self.play(FadeIn(note, shift=0.1 * DOWN), Indicate(h2[1], color=VIOLET), Indicate(h2[5], color=VIOLET), run_time=1.2)
        # r³/r² → r: r² sai do lado esquerdo e o r³ vira r (os demais símbolos mantêm a identidade)
        self.play(h2[1].animate.set_opacity(0), run_time=0.5)
        self.remove(h2)
        rest = [h2[i] for i in (0, 2, 3, 4, 5)]
        self.add(*rest)
        self.play(*[ReplacementTransform(a, b) for a, b in zip(rest, h3)], run_time=1.0)
        self.regroup(h3)
        self.play(TransformMatchingTex(h3, h4), FadeOut(note), run_time=1.0)
        b4 = box(h4)
        tag_in = domain_tag("interior", "(r<R)").next_to(b4, DOWN, buff=0.18)
        self.play(Create(b4), FadeIn(tag_in, shift=0.1 * UP), run_time=0.8)
        self.at(c[20])
        self.play(X.animate.set_value(0.9), run_time=2.2, rate_func=linear)                  # cresce linearmente
        self.play(X.animate.set_value(0.3), run_time=1.6, rate_func=linear)
        self.play(Indicate(tag_in, color=WHITE, scale_factor=1.15), run_time=1.0)
        self.at(c[21])
        e0 = eq("E(0)=0", size=36).move_to(P(RX, -1.4))
        self.play(X.animate.set_value(0.0), FadeIn(e0), run_time=1.4)
        self.at(c[22])

        # exterior: o interior fica identificado e atenuado; Q_env congela em Q
        res_in = VGroup(h4, b4, tag_in)
        dimmed = res_in.copy().scale(0.7).move_to(P(RX - 1.75, 2.0))
        dimmed[0].set_opacity(0.55)
        dimmed[1].set_stroke(opacity=0.55)                                    # a caixa não ganha preenchimento
        dimmed[2].set_opacity(0.55)
        self.play(FadeOut(VGroup(e0, rr, rho, qr)), Transform(res_in, dimmed),
                  S.animate.set_value(1.25), VEO.animate.set_value(0.0), run_time=1.4)
        QM = ValueTracker(0.0)
        qlab = eq(r"Q_{\mathrm{env}}", size=36, color=BLUE_L).move_to(P(RX - 2.65, 0.75))
        qbar = always_redraw(lambda: Rectangle(width=max(3.6 * min(X.get_value(), 1.0) ** 3, 0.01), height=0.26)
                             .set_stroke(width=0).set_fill(BLUE_L, 0.85 * QM.get_value())
                             .next_to(P(RX - 1.95, 0.75), RIGHT, buff=0))
        qcap = Line(P(RX - 1.95 + 3.6, 0.55), P(RX - 1.95 + 3.6, 0.95)).set_stroke(WHITE, 2, 0.5)
        qin = eq(r"Q_{\mathrm{env}}=\frac43\pi\rho r^3", size=34).move_to(P(RX, 0.05))
        qout = eq(r"Q_{\mathrm{env}}=Q=\frac43\pi\rho R^3", size=34).move_to(P(RX, 0.05))
        qin.add_updater(lambda m: m.set_opacity(QM.get_value() * (1.0 if X.get_value() < 1 else 0.0)))
        qout.add_updater(lambda m: m.set_opacity(QM.get_value() * (1.0 if X.get_value() >= 1 else 0.0)))
        self.add(qbar, qin, qout)
        self.play(QM.animate.set_value(1.0), FadeIn(qlab), FadeIn(qcap), run_time=0.8)
        self.play(X.animate.set_value(1.0), run_time=2.2, rate_func=linear)
        r_eq_R = eq("r=R", size=36).move_to(cc + P(0, -1.25 - 0.5))
        self.play(FadeIn(r_eq_R, shift=0.1 * DOWN), Flash(cc + 1.25 * U(A_P), color=WHITE, flash_radius=0.3), run_time=1.0)
        self.at(c[23])
        self.play(FadeOut(r_eq_R), X.animate.set_value(1.6), run_time=3.2, rate_func=linear)
        self.at(c[24])
        self.play(Indicate(VGroup(qbar, qcap), color=BLUE_L, scale_factor=1.05), run_time=1.2)
        self.at(c[25])
        x0 = eq("E(r)", r"\,4\pi r^2", "=", r"\frac{Q}{\varepsilon_0}", size=44, colors={0: CYAN}).move_to(P(RX, -1.0))
        self.play(Write(x0), run_time=1.3)
        self.at(c[26])
        x1 = eq("E(r)", "=", r"\frac{Q}{4\pi\varepsilon_0 r^2}", size=44, colors={0: CYAN}).move_to(P(RX, -1.0))
        x2 = eq("E(r)", "=", r"\frac{\rho R^3}{3\varepsilon_0 r^2}", size=48, colors={0: CYAN}).move_to(P(RX, -1.0))
        self.play(TransformMatchingTex(x0, x1), X.animate.set_value(2.1), run_time=1.6)        # dividir por 4πr²
        self.play(TransformMatchingTex(x1, x2), Indicate(qout, color=WHITE), run_time=1.3)     # substituir Q
        b2 = box(x2)
        tag_out = domain_tag("exterior", "(r>R)").next_to(b2, DOWN, buff=0.18)
        self.play(Create(b2), FadeIn(tag_out, shift=0.1 * UP), run_time=0.8)
        self.at(c[27])
        rgt = eq("r>R", size=36).move_to(cc + 2.1 * 1.25 * U(A_P) + P(0.45, -0.5))
        pq = charge(cc, label="Q")
        self.play(SFO.animate.set_value(0.15), FadeIn(pq, scale=0.5), FadeIn(rgt), run_time=1.6)
        self.wait(5.0)
        self.play(Indicate(fld, color=CYAN, scale_factor=1.08), run_time=1.4)
        self.at(c[-1] - 2.0)
        self.play(SFO.animate.set_value(1.0), FadeOut(pq), run_time=1.4)
        self.at(c[-1] + 0.6)
        self.k8 = SimpleNamespace(c=cc, S=S, X=X, fld=fld, res_in=res_in, res_out=VGroup(x2, b2, tag_out), rgt=rgt,
                                  junk=VGroup(qbar, qin, qout, qlab, qcap))

    # ── 09 · Gráfico sincronizado (SPLIT): o mesmo X controla esfera e gráfico ──
    def b09_grafico(self):
        self.begin(9, "grafico")
        c = cues("Agora podemos enxergar todo o comportamento no gráfico.",
                 "No centro, o campo começa em zero.",
                 "Dentro da esfera, cresce em linha reta.",
                 "Atinge seu maior valor na superfície.",
                 "E, do lado de fora, passa a cair como um sobre o raio ao quadrado.",
                 "As duas expressões fornecem exatamente o mesmo valor na superfície.",
                 "O campo é contínuo ali, embora a inclinação do gráfico mude.",
                 "E repare no que realmente tornou toda essa conta simples.",
                 "Não foi a existência de uma integral.",
                 "Foi sabermos, antes de integrar, como o campo precisava se comportar por causa da simetria.")
        k = self.k8
        X, cc = k.X, k.c
        for m in k.junk:
            m.clear_updaters()
        ax = Axes(x_range=[0, 2.2, 1], y_range=[0, 1.45, 1], x_length=5.3, y_length=3.5,
                  axis_config={"color": WHITE, "stroke_opacity": 0.7, "include_tip": False, "include_ticks": False})
        ax.shift(P(1.35, -2.55) - ax.c2p(0, 0))
        xl = eq("r", size=34, color=VIOLET).next_to(ax.c2p(2.2, 0), DOWN, buff=0.15)
        yl = eq("E", size=34, color=CYAN).next_to(ax.c2p(0, 1.45), UP, buff=0.1)
        tR = VGroup(Line(ax.c2p(1, 0) + 0.08 * DOWN, ax.c2p(1, 0) + 0.08 * UP).set_stroke(WHITE, 2),
                    eq("R", size=32, color=BLUE_L).next_to(ax.c2p(1, 0), DOWN, buff=0.15))
        vR = DashedLine(ax.c2p(1, 0), ax.c2p(1, 1.45), dash_length=0.08).set_stroke(WHITE, 1.5, 0.35)
        # cada expressão ligada ao seu ramo, com o domínio
        f_in = VGroup(eq(r"E=\frac{\rho r}{3\varepsilon_0}", size=30), eq("(r<R)", size=26)).arrange(DOWN, buff=0.06)
        f_in.move_to(ax.c2p(0.36, 1.2))
        f_out = VGroup(eq(r"E=\frac{\rho R^3}{3\varepsilon_0 r^2}", size=30), eq("(r>R)", size=26)).arrange(DOWN, buff=0.06)
        f_out.move_to(ax.c2p(1.85, 0.58))
        lead_in = DashedLine(f_in.get_bottom() + 0.05 * DOWN, ax.c2p(0.55, 0.55), dash_length=0.05).set_stroke(WHITE, 1.5, 0.6)
        lead_out = DashedLine(f_out.get_bottom() + 0.05 * DOWN, ax.c2p(1.6, 1 / 1.6 ** 2), dash_length=0.05).set_stroke(WHITE, 1.5, 0.6)
        self.play(FadeOut(k.junk), FadeOut(k.rgt), Create(ax), FadeIn(VGroup(xl, yl, tR, vR)),
                  FadeOut(k.res_in), FadeOut(k.res_out), run_time=1.6)
        self.at(c[1])
        self.play(X.animate.set_value(0.0), run_time=1.6)
        st = {"rv": 0.0, "on": True}

        def curve():
            x = X.get_value()
            if st["on"]:
                st["rv"] = max(st["rv"], x)
            rv = st["rv"]
            out = VGroup()
            if rv > 0.01:
                out.add(ax.plot(lambda t: t, x_range=[0, min(rv, 1.0)], color=CYAN, stroke_width=4.5))
            if rv > 1.01:
                out.add(ax.plot(lambda t: 1 / (t * t), x_range=[1.0, rv], color=CYAN, stroke_width=4.5))
            p = ax.c2p(x, f_graph(x))
            out.add(DashedLine(ax.c2p(x, 0), p, dash_length=0.06).set_stroke(WHITE, 1.5, 0.5) if x > 0.02 else VMobject())
            out.add(Dot(p, radius=0.085, color=CYAN).set_z_index(6))
            return out
        cv = always_redraw(curve)
        self.add(cv)
        e0 = eq("E(0)=0", size=30)
        e0.move_to(ax.c2p(0, 0) + P(0.6 + e0.width / 2, 0.22))
        self.play(FadeIn(e0), Flash(ax.c2p(0, 0), color=CYAN, flash_radius=0.25), run_time=0.9)
        self.at(c[2])
        self.play(X.animate.set_value(1.0), run_time=2.8, rate_func=linear)
        self.play(FadeIn(f_in), Create(lead_in), run_time=0.8)
        self.at(c[3])
        peak = ax.c2p(1, 1)
        hR = DashedLine(ax.c2p(0, 1), peak, dash_length=0.08).set_stroke(WHITE, 1.5, 0.4)
        ylab = eq(r"\frac{\rho R}{3\varepsilon_0}", size=30).next_to(ax.c2p(0, 1), LEFT, buff=0.12)
        self.play(Flash(peak, color=CYAN, flash_radius=0.3), Create(hR), FadeIn(ylab), run_time=1.2)
        self.wait(0.8)
        self.at(c[4])
        q_const = eq(r"Q_{\mathrm{env}}=Q", size=32, color=BLUE_L).move_to(P(-6.0, 2.4))
        q_const.add_updater(lambda m: m.set_opacity(1.0 if X.get_value() > 1.0 else 0.0))
        self.add(q_const)
        self.play(X.animate.set_value(2.1), run_time=4.4, rate_func=linear)
        self.play(FadeIn(f_out), Create(lead_out), run_time=0.8)
        self.at(c[5])
        cont = eq(r"E(R^-)=E(R^+)", size=32).move_to(peak + P(1.25, 0.5))
        self.play(FadeIn(cont, shift=0.1 * DOWN), Indicate(f_in[0], color=WHITE), Indicate(f_out[0], color=WHITE), run_time=1.4)
        self.at(c[6])
        # campo contínuo, inclinações diferentes de cada lado (sem esconder o bico)
        tl = DashedLine(ax.c2p(0.72, 0.72), ax.c2p(1.15, 1.15), dash_length=0.06).set_stroke(WHITE, 2.5, 0.9)
        tr = DashedLine(ax.c2p(0.9, 1.2), ax.c2p(1.2, 0.6), dash_length=0.06).set_stroke(WHITE, 2.5, 0.9)
        slopes = text("inclinações diferentes", 20, opacity=0.85).move_to(peak + P(1.45, 0.02))
        self.play(Create(tl), Create(tr), FadeIn(slopes), run_time=1.4)
        self.at(c[7])
        st["on"] = False
        q_const.clear_updaters()
        form = eq(r"\vec E(\vec r)=E(r)\hat r", size=38, color=CYAN).move_to(P(LX, 2.35))
        self.play(FadeOut(VGroup(tl, tr, slopes, q_const)), X.animate.set_value(1.5), run_time=1.4)
        self.at(c[8])
        self.play(FadeIn(form, shift=0.1 * DOWN), run_time=1.0)
        self.at(c[9])
        self.play(Circumscribe(form, color=WHITE, stroke_width=2), Indicate(k.fld, color=CYAN, scale_factor=1.06), run_time=1.8)
        self.at(c[-1] + 1.0)

    # ── 10 · Três simetrias clássicas: regiões que contribuem e de fluxo nulo ──
    def b10_tres_simetrias(self):
        self.begin(10, "tres_simetrias")
        c = cues("É daí que surgem as três superfícies gaussianas famosas. Cada uma pressupõe uma fonte idealizada.",
                 "Se a fonte possui simetria esférica, uma esfera concêntrica acompanha essa simetria. Ali, toda a superfície contribui para o fluxo.",
                 "Se temos uma linha infinita e uniforme, o campo depende apenas da distância ao eixo. Um cilindro coaxial aproveita isso: na lateral, o campo é paralelo ao vetor área e contribui; nas tampas, ele é tangente, e o fluxo é zero.",
                 "Para um plano infinito uniformemente carregado, a simetria obriga o campo a ser perpendicular ao plano. Um cilindro gaussiano curto atravessando o plano inverte os papéis: as duas tampas contribuem, e a lateral tem fluxo zero.",
                 "Essas formas não são receitas arbitrárias.",
                 "Elas são consequências da simetria das fontes.")
        self.clear(run_time=0.9)
        BIG_C, BIG_K, SMALL_K = P(-2.9, -0.25), 1.3, 0.85
        slots = (P(-4.75, -0.25), P(0.0, -0.25), P(4.75, -0.25))

        def rule(lugar, rel, res):
            return hchain(text(lugar, 24, opacity=0.9), eq(rel, size=32), eq(r"\Rightarrow", size=30), text(res, 24, opacity=0.9))

        names = ("esfera concêntrica", "cilindro coaxial", "cilindro gaussiano curto")
        notes = ("toda a superfície contribui", "lateral contribui · tampas: fluxo nulo", "tampas contribuem · lateral: fluxo nulo")
        hyps = ("distribuição esfericamente simétrica", "linha infinita, uniformemente carregada",
                "plano infinito, uniformemente carregado")
        rules = ((("toda a superfície:", r"\vec E\parallel d\vec A", "contribui"),),
                 (("lateral:", r"\vec E\parallel d\vec A", "contribui"), ("tampas:", r"\vec E\perp d\vec A", "fluxo nulo")),
                 (("tampas:", r"\vec E\parallel d\vec A", "contribuem"), ("lateral:", r"\vec E\perp d\vec A", "fluxo nulo")))
        builders = (sym_sphere, sym_line, sym_plane)
        starts = (c[1], c[2], c[3])
        small = []
        self.at(c[0] + 1.5)
        for i in range(3):
            pn = builders[i]()
            parts = [pn.src, pn.fld, pn.contrib, pn.zero, pn.el_c, pn.el_z]
            grp = VGroup(*parts).scale(BIG_K).move_to(BIG_C)
            hyp = text(hyps[i], 26, opacity=0.9)
            left_at(hyp, 0.6, 1.9)
            rws = VGroup(*[left_at(rule(*r), 0.6, 0.8 - 1.0 * j) for j, r in enumerate(rules[i])])
            self.at(starts[i] if i else c[0] + 1.5)
            # os painéis já reduzidos saem de cena durante a construção grande e voltam juntos no quadro comparativo
            hide = [FadeOut(VGroup(s.grp, s.name, s.note)) for s in small]
            self.play(FadeIn(pn.src), FadeIn(hyp, shift=0.1 * DOWN), *hide, run_time=1.0)
            self.play(LaggedStart(*[GrowArrow(a) for a in pn.fld], lag_ratio=0.08), run_time=1.2)
            self.play(Create(pn.contrib), *([Create(pn.zero)] if len(pn.zero) else []), run_time=1.4)
            self.play(FadeIn(pn.el_c), FadeIn(rws[0], shift=0.1 * DOWN), Indicate(pn.contrib, color=VIOLET, scale_factor=1.04),
                      run_time=1.3)
            if len(rws) > 1:
                self.wait(1.6)
                self.play(FadeIn(pn.el_z), FadeIn(rws[1], shift=0.1 * DOWN), Indicate(pn.zero, color=WHITE, scale_factor=1.04),
                          run_time=1.3)
            self.wait(1.2)
            name = text(names[i], 24, opacity=0.9).move_to(slots[i] + P(0, -2.25))
            note = text(notes[i], 18, opacity=0.8).move_to(slots[i] + P(0, -2.62))
            fit(note, 4.5)
            self.regroup(grp)
            self.play(grp.animate.scale(SMALL_K / BIG_K).move_to(slots[i]), FadeOut(VGroup(hyp, rws)),
                      FadeIn(name), FadeIn(note), run_time=1.3)
            small.append(SimpleNamespace(grp=grp, contrib=pn.contrib, name=name, note=note))
        self.at(c[4])
        flow = hchain(text("fonte", 26), eq(r"\rightarrow", size=34), text("simetria", 26), eq(r"\rightarrow", size=34),
                      text("forma do campo", 26), eq(r"\rightarrow", size=34), text("superfície útil", 26))
        fit(flow, 13.6).move_to(P(0, 2.4))
        self.play(FadeIn(flow, shift=0.1 * DOWN), *[FadeIn(VGroup(s.grp, s.name, s.note)) for s in small[:-1]], run_time=1.4)
        self.at(c[5])
        self.play(LaggedStart(*[Indicate(s.contrib, color=VIOLET, scale_factor=1.06) for s in small], lag_ratio=0.35), run_time=2.4)
        self.at(c[-1] + 1.0)

    # ── 11 · Quando Gauss não simplifica: casos, caminhos adequados e método ──
    def b11_casos_e_metodo(self):
        self.begin(11, "casos_caminhos_metodo")
        c = cues("E isso também explica quando Gauss não é o método mais prático.",
                 "A carga deslocada do começo, uma barra finita, um disco observado fora do eixo ou uma distribuição irregular continuam obedecendo perfeitamente à Lei de Gauss.",
                 "Mas normalmente não existe uma superfície fechada na qual a simetria nos permita substituir toda aquela informação local do campo por um único E.",
                 "Gauss ainda fornece o fluxo total.",
                 "O que ela não fornece sozinha é a distribuição ponto a ponto do campo.",
                 "Nesses casos, outro caminho funciona melhor.",                                                         # 5
                 "Para a carga deslocada, basta Coulomb, ou uma esfera centrada nela.",
                 "Para a barra, somamos as contribuições de Coulomb ao longo do comprimento.",
                 "Para o disco, no eixo, somamos anéis.",
                 "Para uma distribuição irregular, integramos, de forma analítica ou numérica.",
                 "E, em problemas com condutores, costuma ser melhor resolver o potencial, com as condições de contorno.",  # 10
                 "Então, diante de um problema novo, não pergunte primeiro qual superfície gaussiana você decorou.",
                 "Pergunte qual é a simetria da distribuição de carga.",
                 "Essa simetria determina a direção possível do campo?",
                 "Ela diz de quais coordenadas o módulo pode depender?",
                 "Existe uma superfície fechada em que o campo tenha módulo constante nas regiões que contribuem, ou fique tangente nas regiões que não devem contribuir?",  # 15
                 "E você consegue calcular a carga envolvida?",
                 "Se essas peças se encaixam, a Lei de Gauss provavelmente transforma um problema difícil em poucas linhas.",
                 "Se não se encaixam, a lei continua verdadeira. Ela simplesmente pode não ser suficiente para determinar o campo local.")
        self.at(c[0] + 2.5)
        self.clear(run_time=0.9)
        xs, cy, RC = (-5.4, -1.8, 1.8, 5.4), 0.15, 1.0
        cs_ = [P(x, cy) for x in xs]
        pts = [ring(ci, RC, 12, 15) for ci in cs_]
        # carga deslocada
        q0 = cs_[0] + P(0.45, 0.25)
        f0 = arrows_norm(pts[0], [e_point(p, [q0]) for p in pts[0]])
        s0 = charge(q0)
        # barra finita
        rod_q = [cs_[1] + P(t, 0) for t in np.linspace(-0.85, 0.85, 15)]
        s1 = Line(cs_[1] + P(-0.85, 0), cs_[1] + P(0.85, 0)).set_stroke(BLUE_L, 7)
        f1 = arrows_norm(pts[1], [e_point(p, rod_q) for p in pts[1]])
        # disco observado fora do eixo: disco horizontal (perspectiva), campo no plano vertical que contém o eixo
        rr, tt = np.meshgrid(0.93 * np.sqrt(np.linspace(0.02, 1, 8)), np.linspace(0, 2 * PI, 24, endpoint=False))
        dpts = np.stack([rr.ravel() * np.cos(tt.ravel()), rr.ravel() * np.sin(tt.ravel())], -1)

        def disk_E(p):
            rel = p - cs_[2]
            obs = np.array([rel[0], 0.0, rel[1]])
            E = np.zeros(3)
            for dx, dy in dpts:
                d = obs - np.array([dx, dy, 0.0])
                E += d / np.linalg.norm(d) ** 3
            return np.array([E[0], E[2], 0.0])
        s2 = VGroup(Ellipse(width=1.86, height=0.5).move_to(cs_[2]).set_stroke(BLUE_L, 3).set_fill(BLUE, 0.3),
                    DashedLine(cs_[2] + 1.3 * DOWN, cs_[2] + 1.3 * UP, dash_length=0.08).set_stroke(WHITE, 1.5, 0.45))
        f2 = arrows_norm(pts[2], [disk_E(p) for p in pts[2]])
        # distribuição irregular
        off3 = P(0.2, 0.14)
        irr_pts = [cs_[3] + off3 + 0.65 * P(a, b) for a, b in ((-0.45, 0.25), (0.35, 0.4), (0.15, -0.35), (-0.2, -0.15), (0.55, -0.05))]
        irr_w = [1.0, 0.6, 1.4, 0.8, 0.5]
        s3 = Polygon(*[cs_[3] + off3 + 0.5 * (0.55 + 0.25 * np.sin(3 * t) + 0.12 * np.cos(5 * t + 1)) * U(np.degrees(t))
                       for t in np.linspace(0, 2 * PI, 40, endpoint=False)]).set_stroke(BLUE_L, 3).set_fill(BLUE, 0.3)
        f3 = arrows_norm(pts[3], [e_point(p, irr_pts, irr_w) for p in pts[3]])
        srcs = VGroup(s0, s1, s2, s3)
        trials = VGroup(*[gauss_circle(ci, RC, n=20) for ci in cs_])
        fields = VGroup(f0, f1, f2, f3)
        law = eq(r"\oint\vec E\cdot d\vec A=\frac{Q_{\mathrm{env}}}{\varepsilon_0}", size=36).move_to(P(0, -2.55))
        self.at(c[1])
        self.play(LaggedStart(*[FadeIn(s) for s in srcs], lag_ratio=0.25), run_time=1.6)
        self.play(LaggedStart(*[Create(t) for t in trials], lag_ratio=0.2), run_time=1.4)
        self.play(LaggedStart(*[LaggedStart(*[GrowArrow(a) for a in f], lag_ratio=0.04) for f in fields], lag_ratio=0.2),
                  run_time=2.0)
        self.play(Write(law), run_time=1.2)
        m1 = display("A LEI CONTINUA VÁLIDA.", 30)
        m2 = display("A SIMETRIA NÃO FECHA O PROBLEMA.", 30)
        hchain(m1, m2, buff=0.5).move_to(P(0, 2.35))
        self.play(FadeIn(m1, shift=0.1 * DOWN), run_time=1.0)
        self.at(c[2])
        self.play(LaggedStart(*[Indicate(f, color=CYAN, scale_factor=1.06) for f in fields], lag_ratio=0.3), run_time=2.4)
        self.play(FadeIn(m2, shift=0.1 * DOWN), run_time=1.0)
        self.at(c[3])
        self.play(Circumscribe(law, color=WHITE, stroke_width=2), run_time=1.4)
        self.at(c[4])
        self.play(LaggedStart(*[Indicate(a, color=CYAN, scale_factor=1.3) for f in fields for a in f], lag_ratio=0.02),
                  run_time=2.6)
        self.at(c[5])

        # caminhos adequados: uma animação curta por caso; a lei segue válida, só não simplifica
        self.play(trials.animate.set_stroke(opacity=0.25), fields.animate.set_opacity(0.25), run_time=0.8)

        def alt_label(l1, l2, x):
            return VGroup(text(l1, 20, opacity=0.9), text(l2, 20, opacity=0.9)).arrange(DOWN, buff=0.06).move_to(P(x, cy - 1.75))
        self.at(c[6])
        a0 = VGroup(gauss_circle(q0, 0.55, n=14), vec(q0 + 0.55 * U(60), q0 + 1.0 * U(60), CYAN, 4.5),
                    vec(q0 + 0.55 * U(200), q0 + 1.0 * U(200), CYAN, 4.5))
        self.play(Create(a0[0]), GrowArrow(a0[1]), GrowArrow(a0[2]), FadeIn(alt_label("Coulomb direto, ou", "esfera centrada na carga", xs[0])),
                  run_time=1.4)
        self.at(c[7])
        P1 = cs_[1] + P(0.0, 0.8)
        dqs = [cs_[1] + P(t, 0) for t in np.linspace(-0.7, 0.7, 5)]
        a1 = VGroup(*[Dot(d, radius=0.06, color=WHITE) for d in dqs])
        contrib = VGroup(*[vec(P1, P1 + 0.45 * (P1 - d) / np.linalg.norm(P1 - d), CYAN, 2.5, 0.8) for d in dqs])
        resul = vec(P1, P1 + 0.85 * UP, CYAN, 6)
        self.play(FadeIn(a1), FadeIn(Dot(P1, radius=0.06, color=WHITE)), run_time=0.6)
        self.play(LaggedStart(*[GrowArrow(v) for v in contrib], lag_ratio=0.15), run_time=1.0)
        self.play(ReplacementTransform(contrib, resul), FadeIn(alt_label("somar Coulomb", "ao longo da barra", xs[1])), run_time=1.0)
        self.at(c[8])
        P2 = cs_[2] + P(0.0, 0.85)
        rings = VGroup(*[Ellipse(width=2 * r, height=2 * r * 0.27).move_to(cs_[2]).set_stroke(WHITE, 2.5) for r in (0.3, 0.6, 0.9)])
        self.play(LaggedStart(*[Create(r_) for r_ in rings], lag_ratio=0.3), FadeIn(Dot(P2, radius=0.06, color=WHITE)), run_time=1.2)
        self.play(GrowArrow(vec(P2, P2 + 0.75 * UP, CYAN, 6)), FadeIn(alt_label("no eixo:", "somar anéis", xs[2])), run_time=0.9)
        self.at(c[9])
        cells = VGroup(*[Rectangle(width=0.26, height=0.26).move_to(cs_[3] + off3 + P(i * 0.27, j * 0.27)).set_stroke(WHITE, 1.5, 0.8)
                         for i in (-1, 0, 1) for j in (-1, 0, 1)])
        self.play(LaggedStart(*[Create(r_) for r_ in cells], lag_ratio=0.08),
                  FadeIn(alt_label("integração", "analítica ou numérica", xs[3])), run_time=1.6)
        self.at(c[10])
        pot = hchain(text("com condutores: potencial", 22, opacity=0.9), eq(r"\nabla^2V=-\rho/\varepsilon_0", size=32),
                     text("e condições de contorno", 22, opacity=0.9))
        fit(pot, 13.6).move_to(P(0, -2.55))
        self.play(FadeOut(law, shift=0.1 * DOWN), FadeIn(pot, shift=0.1 * DOWN), run_time=1.2)
        self.at(c[11])

        # método de decisão aplicado a dois exemplos
        self.clear(run_time=0.9)
        icons = VGroup(gauss_circle(P(-2.2, 0.3), 0.7, n=16),
                       VGroup(DashedVMobject(Ellipse(width=1.1, height=0.3).move_to(P(0, 0.95)), num_dashes=12),
                              DashedVMobject(Ellipse(width=1.1, height=0.3).move_to(P(0, -0.35)), num_dashes=12),
                              DashedLine(P(-0.55, -0.35), P(-0.55, 0.95)), DashedLine(P(0.55, -0.35), P(0.55, 0.95))),
                       VGroup(DashedVMobject(Ellipse(width=0.8, height=0.22).move_to(P(2.2, 0.75)), num_dashes=10),
                              DashedVMobject(Ellipse(width=0.8, height=0.22).move_to(P(2.2, -0.15)), num_dashes=10),
                              DashedLine(P(1.8, -0.15), P(1.8, 0.75)), DashedLine(P(2.6, -0.15), P(2.6, 0.75)))).set_stroke(VIOLET, 3)
        self.play(FadeIn(icons), run_time=1.0)
        self.at(c[12] - 0.9)
        self.play(FadeOut(icons, shift=0.2 * UP), run_time=0.8)
        XQ, XA, XB = -3.6, 1.55, 5.05
        ys = (1.65, 0.9, 0.15, -0.6, -1.35, -2.25)
        hA = VGroup(Circle(radius=0.2).set_stroke(BLUE_L, 2).set_fill(BLUE, 0.3), text("esfera uniforme", 22, opacity=0.9)).arrange(RIGHT, buff=0.15)
        hB = VGroup(Line(P(-0.22, 0), P(0.22, 0)).set_stroke(BLUE_L, 5), text("barra finita", 22, opacity=0.9)).arrange(RIGHT, buff=0.15)
        hA.move_to(P(XA, 2.45))
        hB.move_to(P(XB, 2.45))
        items = [text("SIMETRIA DA FONTE", 24), hchain(text("DIREÇÃO DE", 24), eq(r"\vec E", size=32, color=CYAN), buff=0.12),
                 text("DEPENDÊNCIA ESPACIAL", 24), text("SUPERFÍCIE COMPATÍVEL", 24), text("CARGA ENVOLVIDA", 24),
                 display("GAUSS É UM BOM MÉTODO?", 26)]
        ansA = [text("esférica", 20), text("radial", 20), hchain(text("só de", 20), eq("r", size=28, color=VIOLET), buff=0.1),
                text("esfera concêntrica", 20), eq(r"\tfrac43\pi\rho r^3", size=28), display("sim", 24)]
        ansB = [text("só em torno do eixo", 20), text("muda com a posição", 20), text("de duas coordenadas", 20),
                text("nenhuma", 20), text("fácil, mas não basta", 20), display("não: Coulomb", 24)]
        for m, y in zip(items, ys):
            m.move_to(P(XQ, y))
        for m, y in zip(ansA, ys):
            m.move_to(P(XA, y)).set_opacity(0.9)
        for m, y in zip(ansB, ys):
            m.move_to(P(XB, y)).set_opacity(0.9)
        marks = (c[12], c[13], c[14], c[15], c[16], c[17])
        self.at(marks[0])
        self.play(FadeIn(hA), FadeIn(hB), FadeIn(items[0], shift=0.12 * DOWN), run_time=0.9)
        self.play(FadeIn(ansA[0]), FadeIn(ansB[0]), run_time=0.7)
        for i in range(1, 6):
            self.at(marks[i])
            arr = Arrow(items[i - 1].get_bottom() + 0.04 * DOWN, items[i].get_top() + 0.04 * UP, buff=0.03, stroke_width=4,
                        max_tip_length_to_length_ratio=0.35, color=WHITE).set_opacity(0.8)
            self.play(GrowArrow(arr), run_time=0.4)
            self.play(FadeIn(items[i], shift=0.12 * DOWN), run_time=0.7)
            self.play(FadeIn(ansA[i]), FadeIn(ansB[i]), run_time=0.7)
        self.play(Create(box(items[5])), run_time=0.6)
        self.at(c[18])
        self.play(Indicate(ansB[5], color=WHITE, scale_factor=1.1), run_time=1.2)
        self.at(c[-1] + 0.8)

    # ── 12 · Retorno (COMPARE) · payoff (FOCUS) · pausa · outro (END SCREEN) ──
    def b12_retorno_payoff_outro(self):
        self.begin(12, "retorno_payoff_outro")
        c = cues("Voltando aos dois casos do começo, agora a diferença fica clara.",
                 "Nos dois, a Lei de Gauss era igualmente válida.",
                 "Mas apenas em um deles a simetria permitia transformar a integral de fluxo numa equação simples para o campo.",
                 "A Lei de Gauss fala sobre fluxo.",
                 "É a simetria da fonte que transforma fluxo em campo.",
                 "Se esse vídeo te ajudou a enxergar a Lei de Gauss de outro jeito, se inscreve no Parallax Lab, porque vem mais Física e Matemática por aqui.",
                 "E se você conhece alguém sofrendo com Física 3, compartilha esse vídeo com essa pessoa.",
                 "Deixa o like se curtiu, e a gente se vê no próximo.")
        self.clear(run_time=0.9)
        off, aro = ValueTracker(1.0), ValueTracker(1.0)
        g = self.problems(off, aro)
        for m in (g.q, g.ar):
            m.clear_updaters()
        self.play(FadeIn(VGroup(g.gl, g.gr, g.ball, g.al, g.q, g.ar)), run_time=1.4)
        self.at(c[1])
        self.play(Write(g.el), Write(g.er), run_time=1.6)
        self.at(c[2])
        l2 = eq(r"\oint", r"\vec E\cdot d\vec A", r"\;\rightarrow\;", "E", r"\,A", size=36, colors={3: CYAN}).move_to(g.el)
        r2 = eq(r"\oint", r"\vec E\cdot d\vec A", r"\neq", "E", r"\,A", size=36, colors={2: MAGENTA, 3: CYAN}).move_to(g.er)
        self.play(TransformMatchingTex(g.el, l2), Indicate(g.al, color=CYAN, scale_factor=1.05), run_time=1.6)
        self.play(TransformMatchingTex(g.er, r2), LaggedStart(*[Indicate(a, color=CYAN, scale_factor=1.25) for a in g.ar],
                                                               lag_ratio=0.05), run_time=2.0)
        self.at(c[3] - 1.4)
        self.clear(self.wm, run_time=1.2, extra=[FadeOut(self.tag)])
        self.tag = None
        p1 = display("A LEI DE GAUSS FALA SOBRE FLUXO.", 40).move_to(P(0, 0.55))
        p2 = display("É A SIMETRIA DA FONTE QUE TRANSFORMA FLUXO EM CAMPO.", 36)
        fit(p2, 13.6).move_to(P(0, -0.4))
        self.at(c[3])
        self.play(FadeIn(p1, shift=0.12 * UP), run_time=1.2)
        self.at(c[4])
        self.play(FadeIn(p2, shift=0.12 * UP), run_time=1.4)
        self.at(c[5] + 1.8)                                                   # frase + pausa curta (~2 s)
        # outro: sem destinos definidos → marca centralizada e mensagem curta; anéis com movimento discreto
        oc = P(0, 0.2)
        rings = VGroup(*[gauss_circle(oc, r, op=0.16, n=int(14 * r)) for r in (2.0, 3.0, 4.0)])
        for i, r_ in enumerate(rings):
            r_.add_updater(lambda m, dt, s=(1 if i % 2 == 0 else -1) * (0.06 - 0.01 * i): m.rotate(s * dt, about_point=oc))
        logo = ImageMobject(str(LOGO_PATH)).set_width(5.2).move_to(oc + P(0, 0.35))
        msg = text("Inscreva-se para acompanhar os próximos vídeos", 26, opacity=0.85).move_to(oc + P(0, -1.15))
        self.play(FadeOut(VGroup(p1, p2)), FadeOut(self.wm), run_time=1.0)
        self.play(FadeIn(rings), FadeIn(logo), run_time=1.6)
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=1.0)
        self.at(c[-1] + 1.2 + 1.8)
