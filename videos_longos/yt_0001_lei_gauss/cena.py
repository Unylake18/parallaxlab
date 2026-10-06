"""yt_0001 — Lei de Gauss: o segredo não é a integral — é a simetria. Vídeo horizontal (revisão 2.1, sincronizado à voz).

Fonte de verdade: ficha.md desta pasta (narração, storyboard e equações). Revisão 2: construção da normal e do
vetor área, retomada das coordenadas esféricas, uma operação por transformação, domínios das fórmulas, regiões
que contribuem nas simetrias clássicas, carga envolvida (Q_env), caminhos alternativos e tela final.
Revisão 2.1: header ELETROMAGNETISMO · LEI DE GAUSS, watermark maior, ângulo sólido (dθ = ds/r → dΩ = dA⊥/r²,
dΩ × dΩ_or), forma geral Q_env(r), continuidade em R, idealizações infinitas, checklist progressivo e outro.

Uma única cena contínua (`LeiGauss`), dividida em seções (blocos):
  01 cold open · 02 intro · 03 normal, vetor área e fluxo · 04 Coulomb + cancelamento 1/r² × r²
  05 ângulo sólido, interna × externa, Q_env · 06 superfície ruim (carga deslocada) · 07 simetria da fonte
  08 esfera uniforme (interior, coordenadas esféricas, dV, exterior) · 09 gráfico sincronizado
  10 três simetrias · 11 casos ruins, caminhos adequados e método · 12 retorno, payoff, pausa e outro

Ritmo pela voz: gerar_sync.py alinha texto_narracao.txt às 3 partes do ElevenLabs e grava em sync.json o instante
de cada marco c[i] de cada bloco. Onde a animação não cabe até o marco seguinte, a cena pede uma espera à voz
(pads.json); `gerar_sync.py montar` insere essas esperas em pausas reais da fala (audio/narracao_montagem.wav) e
gera a legenda com a grafia normal. As durações são contadas em quadros inteiros, então vídeo e voz não derivam.

Gramática visual (ficha, seção 14): ciano = E⃗ e E nas equações · âmbar = θ, ϑ, φ, dθ, dΩ e arcos · azul
(contorno contínuo + preenchimento) = distribuição física, R, Q · violeta tracejado = superfície gaussiana e r
(traço contínuo = região que contribui) · violeta translúcido = volume envolvido · azul elétrico = n̂ ·
violeta #745CFF = d⃗A e o pedaço dA · branco = dA⊥ e matemática neutra · magenta = passo inválido ou componente hipotética. Ângulos: θ (E⃗, n̂) no fluxo;
ϑ polar nas coordenadas.

Final:    CRF=14 uv run --no-sync python -m manim -r 1920,1080 --fps 30 --disable_caching videos_longos/yt_0001_lei_gauss/cena.py LeiGauss
Passada a seco (só pads.json): SO=99 ... --fps 30 (o fps precisa ser o do final: ele define a contagem de quadros).
AJUSTAR=1 SO=99 ... recalcula ritmo.json (compressão dos trechos que não cabem na fala); depois, outra passada a seco.
SO=6 (ou SO=6,8) renderiza só esses blocos (os outros rodam sem gerar quadros). GUIAS=1 mostra a safe area.
CRF troca o crf fixo (23) do encoder do Manim no render final; VEL escala a duração das animações (padrão 1).
"""

import json
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
    SurroundingRectangle, Transform, TransformFromCopy, TransformMatchingTex, ValueTracker, VGroup, VMobject, Wait, Write,
    always_redraw, config, linear,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import DISPLAY_FONT, official_text, screen_text  # noqa: E402
from template.layout_horizontal import GUIAS, safe_guides, split  # noqa: E402

PASTA = Path(__file__).resolve().parent
SO = {int(s) for s in os.environ.get("SO", "").split(",") if s.strip()}


def _qualidade_final(crf):
    """Render final: o Manim grava os trechos com crf 23 fixo; aqui só o crf muda (codec, pix_fmt e fps iguais)."""
    import av as _av
    import manim.scene.scene_file_writer as _sfw

    class _Saida:
        def __init__(self, c):
            self._c = c

        def add_stream(self, codec, *a, options=None, **k):
            if options and "crf" in options:
                options = {**options, "crf": crf}
            return self._c.add_stream(codec, *a, options=options, **k)

        def __getattr__(self, n):
            return getattr(self._c, n)

        def __enter__(self):
            return self

        def __exit__(self, *e):
            return self._c.__exit__(*e)

    class _AV:
        def __getattr__(self, n):
            return getattr(_av, n)

        def open(self, *a, **k):
            c = _av.open(*a, **k)
            return _Saida(c) if k.get("mode", a[1] if len(a) > 1 else "r") == "w" else c

    _sfw.av = _AV()


if os.environ.get("CRF"):
    _qualidade_final(os.environ["CRF"])
LOGO_PATH = Path(__file__).resolve().parents[2] / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"

# ── Paleta (identidade vigente; mesmos tons do vid_0012) ─────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # campo elétrico e E
BLUE = "#267BFF"          # distribuição física (preenchimento)
BLUE_L = "#7FB2FF"        # contorno da distribuição física, R, Q
VIOLET = "#9C8CFF"        # superfície gaussiana, r, volume envolvido
MAGENTA = "#EA63FF"       # passo inválido / componente hipotética
NHAT = "#267BFF"          # normal unitária n̂ (azul elétrico; ficha, seção 14)
DAVEC = "#745CFF"         # vetor área d⃗A e o pedaço dA (violeta)
ANG = "#FFC24D"           # grandezas angulares: θ, ϑ, φ, dθ, dΩ, arcos e marca de 90° (âmbar; não é campo)
AUX_OP = 0.7              # comentários auxiliares e rótulos de caso: abaixo do resultado na hierarquia
HEADER = "ELETROMAGNETISMO · LEI DE GAUSS"
WM_W, WM_OP = 1.92, 0.45  # watermark: V2 tinha 1.6 / 0.35 (+20% de escala)

# ── Composição (frame 16 × 9; template/layout_horizontal.py) ────────────────
_L, _R = split(0.5)
LX, RX, MY = _L.x, _R.x, _L.y      # ≈ −3.75, 3.75, −0.2

# ── Ritmo: a voz manda ──────────────────────────────────────────────────────
# sync.json (gerar_sync.py alinhar): instante, no áudio, de cada marco c[i] de cada bloco e do fim da fala do bloco.
# Quando uma animação não cabe até o marco seguinte, a cena registra a espera que a voz precisa ganhar (pads.json);
# gerar_sync.py montar insere essas esperas em pausas reais da fala (narracao_montagem.wav). A fala não muda.
SYNC = json.loads((PASTA / "sync.json").read_text(encoding="utf-8"))
VEL = float(os.environ.get("VEL", "1.0"))     # fator global de duração das animações (1 = como desenhadas)
TOL = 0.1                                       # atraso tolerado num marco antes de pedir espera à voz
RESPIRO = {2: 0.5, 7: 0.5, 8: 0.4}              # respiro extra antes do bloco (depois de payoffs)
# Ritmo por trecho (entre dois marcos): onde a animação desenhada não cabe na fala, o trecho é comprimido antes de
# pedir espera à voz: primeiro as esperas explícitas (até P_ESPERA), depois as animações (até P_ANIM da duração).
# AJUSTAR=1 numa passada a seco recalcula ritmo.json a partir das durações desenhadas.
RITMO_ARQ = PASTA / "ritmo.json"
AJUSTAR = os.environ.get("AJUSTAR") == "1"
RITMO = {} if AJUSTAR or not RITMO_ARQ.exists() else json.loads(RITMO_ARQ.read_text(encoding="utf-8"))
P_ESPERA, P_ANIM, FOLGA = 0.4, 0.62, 0.04


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


def box(m, color=WHITE, buff=0.26):
    return SurroundingRectangle(m, color=color, buff=buff, corner_radius=0.1, stroke_width=2.0)


def strike(m, color=WHITE, w=4):
    return Line(m.get_corner(DL) + 0.06 * DL, m.get_corner(UR) + 0.06 * UR).set_stroke(color, w)


def frac_parts(part):
    """(numerador, barra, denominador) de uma fração MathTex, por geometria (esquerda → direita)."""
    gl = list(part)
    bar = max(gl, key=lambda g: g.width)
    num = sorted((g for g in gl if g is not bar and g.get_y() > bar.get_y()), key=lambda g: g.get_x())
    den = sorted((g for g in gl if g is not bar and g.get_y() < bar.get_y()), key=lambda g: g.get_x())
    return num, bar, den


def morph_frac(src, dst, keep):
    """Fração → fração: os `keep` primeiros glifos do numerador e o denominador conservam a identidade;
    o restante do numerador de src vira o restante do numerador de dst (ex.: dA⊥ → dA cosθ)."""
    sn, sb, sd = frac_parts(src)
    dn, db, dd = frac_parts(dst)
    anims = [ReplacementTransform(a, b) for a, b in zip(sn[:keep], dn[:keep])]
    anims += [ReplacementTransform(VGroup(*sn[keep:]), VGroup(*dn[keep:])), ReplacementTransform(sb, db),
              ReplacementTransform(VGroup(*sd), VGroup(*dd))]
    return anims


def hchain(*items, buff=0.18):
    return VGroup(*items).arrange(RIGHT, buff=buff)


def left_at(m, x, y):
    return m.move_to(P(0, y)).align_to(P(x, 0), LEFT)


def domain_tag(nome, dom, size=26):
    """Rótulo de caso (interior/exterior): secundário, menor e menos intenso que o resultado."""
    return hchain(text(nome, 20, opacity=AUX_OP), eq(dom, size=size).set_opacity(AUX_OP + 0.05), buff=0.12)


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
                vec(1.05 * U(22.5), 1.68 * U(22.5), CYAN, 4.5, z=6), vec(1.05 * U(22.5), 1.45 * U(22.5), DAVEC, 4, z=7))
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
                    vec(P(0.85, -0.5), P(1.5, -0.5), CYAN, 4.5, z=6), vec(P(0.85, -0.36), P(1.32, -0.36), DAVEC, 4, z=7))
    el_cap = VGroup(Ellipse(width=0.36, height=0.1).move_to(P(0.38, top)).set_stroke(WHITE, 4),
                    vec(P(0.38, top), P(0.38, top + 0.5), DAVEC, 4, z=7), vec(P(0.38, top), P(1.0, top), CYAN, 4.5, z=6))
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
    el_caps = VGroup(vec(P(-0.12, pt), P(-0.12, pt + 0.45), DAVEC, 4, z=7), vec(P(0.12, pt), P(0.12, pt + 0.62), CYAN, 4.5, z=6),
                     vec(P(-0.12, pb), P(-0.12, pb - 0.45), DAVEC, 4, z=7), vec(P(0.12, pb), P(0.12, pb - 0.62), CYAN, 4.5, z=6))
    el_lat = VGroup(Line(P(0.45, -0.62), P(0.45, -0.32)).set_stroke(WHITE, 8),
                    vec(P(0.45, -0.47), P(0.92, -0.47), DAVEC, 4, z=7), vec(P(0.6, -0.4), P(0.6, -0.95), CYAN, 4.5, z=6))
    return SimpleNamespace(src=src, fld=fld, contrib=caps, zero=lateral, el_c=el_caps, el_z=el_lat,
                           all=VGroup(src, fld, caps, lateral, el_caps, el_lat))


# ── Cena ────────────────────────────────────────────────────────────────────
class LeiGauss(Scene):

    # relógio: T = tempo do vídeo (em quadros exatos); b0 = início do bloco no vídeo; shift = esperas já pedidas à voz
    def setup(self):
        self.T, self.b0, self.b0a, self.shift, self.pads, self.wm, self.tag = 0.0, 0.0, 0.0, 0.0, [], None, None
        # trecho corrente: chave "bloco.i", início no vídeo e durações desenhadas (sem compressão)
        self.k, self.si, self.seg, self.s0, self.base_a, self.base_w, self.na_at, self.ritmo = 0, 0, "0.0", 0.0, 0.0, 0.0, False, {}
        self.camera.background_color = BACKGROUND_COLOR

    def play(self, *args, **kwargs):
        """Duração em quadros inteiros, igual nos dois caminhos do Manim (Wait congelado: int; animação: arange)."""
        anims = self.compile_animations(*args, **kwargs)
        fps = config.frame_rate
        static = False
        if len(anims) == 1 and isinstance(anims[0], Wait):
            self.animations = anims                     # should_update_mobjects() lê a animação corrente
            static = not self.should_update_mobjects()
        espera = isinstance(anims[0], Wait)
        fa, fw = RITMO.get(self.seg, (1.0, 1.0))
        rt0 = max(a.run_time for a in anims) * (1.0 if espera else VEL)
        if not self.na_at:
            if espera:
                self.base_w += rt0
            else:
                self.base_a += rt0
        rt = rt0 if self.na_at else rt0 * (fw if espera else fa)
        n = max(1, int(round(rt * fps)))
        real = (n + 0.25) / fps if static else (n - 0.5) / fps
        m = max(a.run_time for a in anims)
        for a in anims:
            a.run_time = real * a.run_time / m
        self.T += n / fps
        return super().play(*anims)

    def marcos(self, k):
        """c[i] (relativos ao início do bloco) a partir da voz; o último é o fim da fala do bloco."""
        b = SYNC["blocks"][str(k)]
        return [t - b["cues"][0] for t in b["cues"]] + [b["end"] - b["cues"][0]]

    def ext(self, nome):
        return SYNC["extras"][nome] - self.b0a

    def _espera(self, ta, d):
        self.pads.append([round(ta, 3), round(d, 3)])
        self.shift += d
        self.b0 += d

    def at(self, t):
        self._ajusta(self.b0 + t - self.s0)
        d = self.b0 + t - self.T
        if d > 0.5 / config.frame_rate:
            # Scene.wait congela o quadro quando não há updater dependente do tempo: aplica os updaters antes
            self.update_mobjects(0)
            self.na_at = True
            self.wait(d)
            self.na_at = False
        elif d < -TOL:
            self._espera(self.b0a + t, -d)               # a voz espera a animação neste ponto
        self.si += 1
        self.seg, self.s0, self.base_a, self.base_w = f"{self.k}.{self.si}", self.T, 0.0, 0.0

    def _ajusta(self, livre):
        """Fatores (animação, espera) para que o trecho desenhado caiba em `livre` segundos de fala."""
        a, w = self.base_a, self.base_w
        sobra = a + w - (livre - FOLGA)
        if sobra <= 0 or a + w == 0:
            return
        fw = max(P_ESPERA, 1 - sobra / w) if w else 1.0
        sobra -= w * (1 - fw)
        fa = max(P_ANIM, 1 - sobra / a) if a and sobra > 0 else 1.0
        self.ritmo[self.seg] = [round(fa, 3), round(fw, 3)]

    def respiro(self, t, d):
        """Pausa deliberada na voz antes do instante t do bloco (sem atraso de animação)."""
        self._espera(self.b0a + t, d)

    def begin(self, k, name):
        print(f"  (relógio antes do bloco {k:02d}: {self.T:.4f}s = {self.T * config.frame_rate:.2f} quadros)")
        self.next_section(f"{k:02d}_{name}", skip_animations=bool(SO) and k not in SO)
        self.k, self.si = k, 0
        self.b0a = SYNC["blocks"][str(k)]["cues"][0]
        self.b0 = self.b0a + self.shift
        if k in RESPIRO:
            self.respiro(0.0, RESPIRO[k])
        self.at(0.0)
        print(f"bloco {k:02d} {name}: início {self.T:6.1f}s (voz {self.b0a:6.1f}s + esperas {self.shift:5.1f}s)")

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
        if AJUSTAR:
            RITMO_ARQ.write_text(json.dumps(self.ritmo, indent=0), encoding="utf-8")
            print(f"ritmo.json: {len(self.ritmo)} trechos comprimidos")
        (PASTA / "pads.json").write_text(json.dumps({"vel": VEL, "fps": config.frame_rate, "pads": self.pads}, indent=0),
                                         encoding="utf-8")
        print(f"duração total: {self.T:.2f}s · esperas pedidas à voz: {len(self.pads)} (+{self.shift:.2f}s)")

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
        c = self.marcos(1)
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
        c = self.marcos(2)
        g = self.g1
        for m in (g.q, g.ar):
            m.clear_updaters()
        ctx = VGroup(g.gl, g.gr, g.ball, g.al, g.q, g.ar, g.el, g.er, g.ask)
        orig = ctx.copy()
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(WM_W).set_opacity(WM_OP).to_corner(UR, buff=0.3)
        self.tag = text(HEADER, 18, opacity=0.6).to_corner(UL, buff=0.38)
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
        c = self.marcos(3)
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
        plate = always_redraw(lambda: Polygon(*corners()).set_stroke(DAVEC, 3).set_fill(DAVEC, 0.35).set_z_index(2))
        # n̂: direção unitária, curta, num ponto do pedaço (a normal é a mesma em todo o pedaço plano);
        # d⃗A = n̂ dA: vetor área, grosso, no centro, com comprimento que acompanha a área
        def side():
            """Lado do pedaço onde n̂ se apoia: fora da cunha de θ até ~95°; depois gira suave para longe da seta de E⃗."""
            th = TH.get_value()
            w = float(np.clip((th - 95.0) / 40.0, 0.0, 1.0))
            return U(th + 90 - 180 * w * w * (3 - 2 * w))
        nb = lambda: pc + 0.42 * SZ.get_value() * side()
        nhat = always_redraw(lambda: vec(nb(), nb() + 0.75 * U(TH.get_value()), NHAT, 4, NA.get_value(), z=10))
        dAv = always_redraw(lambda: vec(pc, pc + 1.5 * SZ.get_value() ** 2 * U(TH.get_value()), DAVEC, 9,
                                        0.75 * DAO.get_value(), z=7))
        rmark = always_redraw(lambda: right_angle(nb(), U(TH.get_value()), side(), 0.18, ANG,
                                                  0.8 * RAO.get_value()))
        lab_dA = eq("dA", size=32)
        lab_dA.add_updater(lambda m: m.move_to(pc - 0.5 * SZ.get_value() * side()
                                               + 0.25 * SZ.get_value() * DEP.get_value() * DV - 0.18 * U(TH.get_value()))
                           .set_opacity(DLO.get_value()))
        lab_n = eq(r"\hat n", size=34, color=NHAT)
        lab_n.add_updater(lambda m: m.move_to(nb() + 1.0 * U(TH.get_value()) + 0.2 * side())
                          .set_opacity(NA.get_value()))
        lab_dAv = eq(r"d\vec A", size=34, color=DAVEC)
        lab_dAv.add_updater(lambda m: m.move_to(pc + (1.5 * SZ.get_value() ** 2 + 0.4) * U(TH.get_value()))
                            .set_opacity(DAO.get_value()))
        lab_tp = text("plano tangente", 22, opacity=0.8)
        lab_tp.add_updater(lambda m: m.move_to(max(corners(2.2), key=lambda p: p[1]) + P(0.2, 0.25))
                           .set_opacity(0.8 * TPO.get_value()))
        lab_90 = eq(r"90^\circ", size=22, color=ANG)
        lab_90.add_updater(lambda m: m.move_to(nb() + 0.32 * (U(TH.get_value()) + side())).set_opacity(0.8 * NLO.get_value()))
        self.add(tplane, plate, dAv, nhat, rmark, lab_dA, lab_n, lab_dAv, lab_tp, lab_90)

        # dA: um número. Ampliar o elemento.
        L1 = left_at(hchain(eq("dA", size=40), text("área do elemento (um número)", 24, opacity=0.85)), 0.8, 1.6)
        L2 = left_at(hchain(eq(r"\hat n", size=40, color=NHAT), text("normal unitária", 24, opacity=0.85),
                            eq(r"|\hat n|=1", size=34)), 0.8, 0.7)
        L3 = left_at(hchain(eq(r"d\vec A", "=", r"\hat n", r"\,dA", size=44, colors={0: DAVEC, 2: NHAT}),
                            text("vetor área", 24, opacity=0.85)), 0.8, -0.3)
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
        outs = VGroup(*[vec(SC + 1.6 * U(a), SC + 2.08 * U(a), NHAT, 3.5) for a in range(0, 360, 45)])
        inward = DashedLine(SC + 1.6 * U(180), SC + 1.12 * U(180), dash_length=0.06).set_stroke(NHAT, 2.5, 0.6)
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
        arc = always_redraw(lambda: Arc(radius=0.62, start_angle=0, angle=np.radians(TH.get_value()), arc_center=pc)
                            .set_stroke(ANG, 4.5, AO.get_value()).set_z_index(9) if TH.get_value() > 3 else VMobject())
        thl = eq(r"\theta", size=38, color=ANG)
        thl.add_updater(lambda m: m.move_to(pc + 0.95 * U(TH.get_value() / 2))
                        .set_opacity(AO.get_value() if TH.get_value() > 12 else 0))
        self.add(e_here, ref, arc, thl)
        eqA = eq(r"d\vec A", "=", r"\hat n", r"\,dA", size=40, colors={0: DAVEC, 2: NHAT}).move_to(P(RX, 2.15))
        self.flatten(L3)
        self.play(LaggedStart(*[FadeIn(a) for a in field], lag_ratio=0.02), DEP.animate.set_value(0.35),
                  EO.animate.set_value(1.0), FadeOut(VGroup(L1, L2, L3[1])), ReplacementTransform(L3[0], eqA), run_time=2.0)
        self.play(TH.animate.set_value(35), run_time=1.2)
        self.at(c[7])
        # dois beats, dois ângulos: 1) n̂ ⊥ pedaço (90°, secundário); 2) θ entre E⃗ e d⃗A (protagonista)
        self.play(NLO.animate.set_value(1.0), RAO.animate.set_value(1.0), Indicate(lab_90, color=ANG, scale_factor=1.3),
                  run_time=1.0)
        self.wait(0.6)
        self.play(AO.animate.set_value(1.0), NLO.animate.set_value(0.45), RAO.animate.set_value(0.5), run_time=1.0)
        self.play(Indicate(thl, color=ANG, scale_factor=1.35), run_time=0.8)
        eqF = eq(r"d\Phi_E", "=", r"\vec E", r"\cdot d\vec A", size=46, colors={2: CYAN}).move_to(P(RX, 1.05))
        eqF2 = eq(r"d\Phi_E", "=", "E", r"\,dA", r"\cos", r"\theta", size=46, colors={2: CYAN, 5: ANG}).move_to(P(RX, 1.05))
        self.play(Write(eqF), run_time=1.2)
        self.play(TransformMatchingTex(eqF, eqF2), run_time=1.2)
        eqF = eqF2

        # leituras sincronizadas: θ, cos θ, barra de dΦ e sinal; sombra = projeção da placa
        cos = lambda: float(np.cos(np.radians(TH.get_value())))
        thv = DecimalNumber(0, num_decimal_places=0, unit=r"^\circ", font_size=38, color=ANG)
        cv = DecimalNumber(1, num_decimal_places=2, include_sign=True, font_size=38)
        th_lab, c_lab = eq(r"\theta=", size=38, color=ANG), eq(r"\cos\theta=", size=38)
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
        closed = always_redraw(lambda: gauss_circle(pc - 1.5 * U(TH.get_value()), 1.5, op=0.5 * CO.get_value(), w=2.5))
        self.add(closed)
        self.play(CO.animate.set_value(1.0), SHO.animate.set_value(0.0), RAO.animate.set_value(0.0), NLO.animate.set_value(0.0),
                  run_time=1.0)                                                # o beat do 90° já passou: menos densidade
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
        normals = VGroup(*[vec(p, p + 0.42 * U(a), NHAT, 3.5) for a, p in zip(range(0, 360, 30), ring(cS, 1.6, 12))])
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
        c = self.marcos(4)
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
            vec(p, p + 0.34 * U(a), NHAT, 3.5, NO.get_value(), z=4)
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
        self.play(RR.animate.set_value(2.2), Indicate(mlabs[0], color=CYAN), run_time=2.8)
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
        c = self.marcos(5)
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
        # LO: pedaço · FO: normal, θ e dA⊥ · LBO: rótulos r, n̂, θ, dA⊥ · DOO: rótulo dΩ (só nasce com o nome)
        PH, CO, LO, FO, LBO, DOO, SW, SWO = (ValueTracker(v) for v in (300.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        DL_ = 10.0
        refc = DashedVMobject(Circle(radius=0.62, arc_center=cq), num_dashes=22).set_stroke(WHITE, 1.5, 0.45)
        self.at(c[1])

        def cone():
            o, a = CO.get_value(), PH.get_value()
            if o < 0.01:
                return VGroup()
            pts = [cq] + [cq + (rb(t) + 0.45) * U(t) for t in np.linspace(a - DL_, a + DL_, 9)]
            arc_ = Arc(radius=0.62, start_angle=np.radians(a - DL_), angle=np.radians(2 * DL_), arc_center=cq)
            return VGroup(Polygon(*pts).set_stroke(WHITE, 1.5, 0.7 * o).set_fill(WHITE, 0.14 * o),
                          arc_.set_stroke(ANG, 6, o))

        def geom(a):
            p = cq + rb(a) * U(a)
            n = blob_normal(BS, a)
            d = (ang(n) - a + 180) % 360 - 180
            chord = np.linalg.norm(rb(a + DL_) * U(a + DL_) - rb(a - DL_) * U(a - DL_))
            return p, n, d, chord

        def piece(a, o, f=1.0):
            """Pedaço dA (violeta) e distância r; com f > 0: normal n̂, ângulo θ (ciano) e área projetada dA⊥."""
            out = VGroup()
            if o < 0.01:
                return out
            p, n, d, chord = geom(a)
            arcp = [cq + rb(t) * U(t) for t in np.linspace(a - DL_, a + DL_, 12)]
            out.add(VMobject().set_points_as_corners(arcp).set_stroke(DAVEC, 9, o))
            out.add(DashedLine(cq, p, dash_length=0.08).set_stroke(WHITE, 2, 0.7 * o))
            f *= o
            if f > 0.01:
                out.add(vec(p, p + 0.72 * n, NHAT, 3.5, f, z=7))
                out.add(DashedLine(p, p + 0.72 * U(a), dash_length=0.06).set_stroke(CYAN, 2, 0.7 * f))
                if abs(d) > 4:
                    out.add(Arc(radius=0.45, start_angle=np.radians(a), angle=np.radians(d), arc_center=p).set_stroke(ANG, 4, f))
                hp = 0.5 * chord * abs(np.cos(np.radians(d)))
                out.add(Line(p - hp * U(a + 90), p + hp * U(a + 90)).set_stroke(WHITE, 5, 0.9 * f).set_z_index(6))
            return out
        cone_m = always_redraw(cone)
        pc_m = always_redraw(lambda: piece(PH.get_value(), LO.get_value(), FO.get_value()))
        labs = VGroup(eq("r", size=32), eq(r"\hat n", size=32, color=NHAT), eq(r"\theta", size=34, color=ANG),
                      eq(r"dA_\perp", size=30), eq(r"d\Omega", size=30, color=ANG), eq("dA", size=30, color=DAVEC))

        def place_labs(m):
            a = PH.get_value()
            p, n, d, chord = geom(a)
            t = U(ang(n) + 90)
            t = t if np.dot(t, U(a + 90)) < 0 else -t                         # lado oposto ao rótulo de dA⊥
            m[0].move_to(cq + 0.62 * rb(a) * U(a) + 0.3 * U(a + 90))
            m[1].move_to(p + 0.95 * n + 0.3 * U(ang(n) + 90 * np.sign(d or 1)))      # longe do θ, do lado de fora
            m[2].move_to(p + 0.78 * U(a + d / 2) + 0.12 * U(a + d / 2 + 90 * np.sign(d or 1)))
            m[3].move_to(p + (0.5 * chord + 0.62) * U(a + 90) + 0.3 * U(a))
            m[4].move_to(cq + 1.0 * U(a - 30))
            m[5].move_to(p + (0.5 * chord + 0.38) * t + 0.12 * n)
            for i, sub in enumerate(m):
                sub.set_opacity({4: DOO.get_value(), 5: LO.get_value()}.get(i, LBO.get_value()))
        labs.add_updater(place_labs)
        self.add(cone_m, pc_m, labs)
        self.play(FadeIn(refc), CO.animate.set_value(1.0), run_time=1.4)
        self.at(c[2])
        self.play(LO.animate.set_value(1.0), run_time=1.2)

        # nome e símbolo entram juntos: o cone é a representação; o conceito é o ângulo sólido
        self.at(c[3])
        title = hchain(display("ÂNGULO SÓLIDO", 34, bold=True), eq(r"d\Omega", size=48, color=ANG), buff=0.35).move_to(P(RX, 2.6))
        self.play(FadeIn(title, shift=0.1 * DOWN), DOO.animate.set_value(1.0), run_time=1.1)
        self.play(Indicate(title[1], color=ANG, scale_factor=1.25), Indicate(refc, color=WHITE, scale_factor=1.15),
                  run_time=1.1)

        # ponte curta: no plano dθ = ds/r (volta: 2π rad) → no espaço dΩ = dA⊥/r² (todas as direções: 4π sr)
        X2, X3, YF = RX - 1.75, RX + 1.75, 0.35
        O2, A2, H2, R2 = P(X2 - 1.3, YF - 0.3), 15.0, 18.0, 1.75
        h2 = text("no plano", 22, opacity=0.85).move_to(P(X2, 1.85))
        rays2 = VGroup(Line(O2, O2 + 2.2 * U(A2 - H2)), Line(O2, O2 + 2.2 * U(A2 + H2))).set_stroke(WHITE, 2.5, 0.85)
        o2 = Dot(O2, radius=0.07, color=WHITE)
        ds_arc = Arc(radius=R2, start_angle=np.radians(A2 - H2), angle=np.radians(2 * H2), arc_center=O2).set_stroke(WHITE, 7)
        dt_arc = Arc(radius=0.5, start_angle=np.radians(A2 - H2), angle=np.radians(2 * H2), arc_center=O2).set_stroke(ANG, 3.5)
        l2 = VGroup(eq("ds", size=30).move_to(O2 + (R2 + 0.36) * U(A2)),
                    eq(r"d\theta", size=28, color=ANG).move_to(O2 + 0.98 * U(A2)),
                    eq("r", size=28).move_to(O2 + 1.0 * U(A2 + H2) + 0.25 * U(A2 + H2 + 90)))
        f2 = eq(r"d\theta", "=", r"\frac{ds}{r}", size=40, colors={0: ANG}).move_to(P(X2, -1.0))
        v2 = hchain(text("volta completa:", 20, opacity=AUX_OP), eq(r"2\pi\ \mathrm{rad}", size=30, color=ANG), buff=0.12).move_to(P(X2, -1.8))
        self.at(c[4])
        self.play(FadeIn(h2), FadeIn(o2), Create(rays2), run_time=0.9)
        self.play(Create(ds_arc), Create(dt_arc), FadeIn(l2), run_time=1.0)
        self.play(Write(f2), run_time=1.0)
        self.at(self.ext("v2"))
        self.play(FadeIn(v2, shift=0.1 * UP), run_time=0.7)

        O3, A3, R3, AH = P(X3 - 1.35, YF - 0.3), 15.0, 1.9, 0.5
        D3 = O3 + R3 * U(A3)
        h3 = text("no espaço", 22, opacity=0.85).move_to(P(X3, 1.85))
        cone3 = VGroup(Polygon(O3, D3 + AH * U(A3 + 90), D3 - AH * U(A3 + 90)).set_stroke(WHITE, 1.5, 0.7).set_fill(WHITE, 0.1),
                       Ellipse(width=0.12, height=2 * AH * 0.7 / R3).rotate(np.radians(A3)).move_to(O3 + 0.7 * U(A3))
                       .set_stroke(ANG, 2.5),
                       DashedLine(O3, D3, dash_length=0.07).set_stroke(WHITE, 1.5, 0.6), Dot(O3, radius=0.07, color=WHITE))
        disk = Ellipse(width=0.34, height=2 * AH).rotate(np.radians(A3)).move_to(D3).set_stroke(WHITE, 2).set_fill(WHITE, 0.45)
        disk.set_z_index(3)
        patch3 = (Ellipse(width=0.62, height=2 * AH / np.cos(np.radians(35))).rotate(np.radians(A3 + 35)).move_to(D3)
                  .set_stroke(DAVEC, 3).set_fill(DAVEC, 0.3).set_z_index(2))
        l3 = VGroup(eq(r"dA_\perp", size=28).move_to(D3 + 0.95 * U(A3 - 70)),
                    eq(r"d\Omega", size=28, color=ANG).move_to(O3 + 0.7 * U(A3) + 0.48 * U(A3 - 90)),
                    eq("r", size=28).move_to(O3 + 1.1 * U(A3) + 0.55 * U(A3 + 90)))
        l3p = eq("dA", size=28, color=DAVEC).move_to(D3 + 0.95 * U(A3 + 70))
        arr23 = eq(r"\longrightarrow", size=36).move_to(P(RX, -1.0))
        f3 = eq(r"d\Omega", "=", r"\frac{dA_\perp}{r^2}", size=40, colors={0: ANG}).move_to(P(X3, -1.0))
        v3 = hchain(text("todas as direções:", 20, opacity=AUX_OP), eq(r"4\pi\ \mathrm{sr}", size=30, color=ANG), buff=0.12).move_to(P(X3, -1.8))
        sr = text("sr = esterradiano", 18, opacity=0.6).move_to(P(X3, -2.3))
        self.at(c[5])
        self.play(FadeIn(h3), FadeIn(cone3), run_time=1.0)
        self.play(FadeIn(disk), FadeIn(l3), run_time=0.9)
        self.play(FadeIn(arr23), Write(f3), run_time=1.1)
        self.at(self.ext("v3"))
        self.play(FadeIn(v3, shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(sr), run_time=0.6)
        self.at(c[6])
        # o mesmo cone intercepta o pedaço inclinado: o tamanho aparente é o da área projetada
        msg = hchain(eq(r"d\Omega", size=32, color=ANG), text("= tamanho aparente do pedaço, visto da carga", 22, opacity=0.9), buff=0.18)
        fit(msg, 6.7).move_to(P(RX, -2.9))
        self.play(FadeIn(patch3), FadeIn(l3p), run_time=1.0)
        self.play(FadeIn(msg, shift=0.1 * UP), Indicate(disk, color=WHITE, scale_factor=1.15), run_time=1.2)
        self.play(Indicate(refc, color=WHITE, scale_factor=1.15), Indicate(labs[4], color=WHITE, scale_factor=1.3), run_time=1.2)

        # projeção e distância no pedaço da superfície arbitrária
        self.at(c[7])
        dom_lab = text("ângulo sólido", 20, opacity=AUX_OP)
        f3t = f3.copy()
        hchain(dom_lab, f3t, buff=0.55).move_to(P(RX - 0.2, 2.5))                # folga para a margem do box
        inset = VGroup(h2, rays2, o2, ds_arc, dt_arc, l2, f2, v2, h3, cone3, disk, patch3, l3, l3p, arr23, v3, sr, msg, title)
        self.play(FadeOut(inset), ReplacementTransform(f3, f3t), FadeIn(dom_lab), run_time=1.3)
        self.play(FO.animate.set_value(1.0), LBO.animate.set_value(1.0), run_time=1.2)
        dperp = eq(r"dA_\perp", "=", "dA", r"\,|\cos", r"\theta", "|", size=40, colors={2: DAVEC, 4: ANG}).move_to(P(RX, 1.35))
        self.play(FadeIn(dperp, shift=0.1 * DOWN), run_time=1.0)
        # mesmo cone, outro pedaço: mais longe e mais inclinado ⇒ área maior para o mesmo tamanho angular
        ghost = piece(300.0, 0.4, 0.0)
        self.add(ghost)
        self.play(LBO.animate.set_value(0.0), run_time=0.4)
        self.play(PH.animate.set_value(360.0), run_time=3.0)
        self.play(LBO.animate.set_value(1.0), run_time=0.6)
        self.at(c[8])
        # dA⊥ → dA cosθ dentro da fração: dA e r² mantêm a identidade
        domB = eq(r"d\Omega", "=", r"\frac{dA\,|\cos\theta|}{r^2}", size=40, colors={0: ANG}).move_to(f3t).align_to(f3t, LEFT)
        self.flatten(f3t)
        self.play(ReplacementTransform(f3t[0], domB[0]), ReplacementTransform(f3t[1], domB[1]),
                  *morph_frac(f3t[2], domB[2], keep=2), Indicate(dperp, color=WHITE, scale_factor=1.06), run_time=1.4)
        self.regroup(domB)
        dom_box = box(domB, WHITE)
        self.play(Create(dom_box), run_time=0.6)

        # dΩ é o tamanho angular (≥ 0); dΩ_or carrega também o sinal da orientação
        self.at(c[9])
        orr = eq(r"d\Omega_{\rm or}", "=", r"\frac{\hat r\cdot\hat n}{r^2}\,dA", "=", r"\frac{\cos\theta\,dA}{r^2}", size=40,
                 colors={0: ANG})
        or_lab = text("orientado", 20, opacity=AUX_OP)
        fit(hchain(or_lab, orr, buff=0.3), 6.7).move_to(P(RX, 1.3))
        pm = hchain(eq(r"d\Omega_{\rm or}=\pm\,d\Omega", size=36, color=ANG), text("+ onde o campo sai · − onde entra", 18, opacity=AUX_OP),
                    buff=0.3)
        fit(pm, 6.7).move_to(P(RX, 0.2))
        self.play(FadeOut(dperp), FadeIn(or_lab), FadeIn(orr[0:4], shift=0.1 * DOWN), TransformFromCopy(domB[2], orr[4]),
                  run_time=1.3)
        self.play(FadeIn(pm, shift=0.1 * DOWN), run_time=1.0)

        # o fluxo pelo pedaço: Coulomb, depois a mesma fração vira dΩ_or (substituição pela definição)
        self.at(c[10])
        YS = -0.95
        s1 = eq(r"d\Phi_E", "=", r"\vec E\cdot d\vec A", size=40).move_to(P(RX, YS))
        s2 = eq(r"d\Phi_E", "=", r"\frac{q}{4\pi\varepsilon_0 r^2}", r"(\hat r\cdot\hat n)\,dA", size=40).move_to(P(RX, YS))
        s3 = eq(r"d\Phi_E", "=", r"\frac{q}{4\pi\varepsilon_0}", r"\frac{\cos\theta\,dA}{r^2}", size=40).move_to(P(RX, YS))
        s4 = eq(r"d\Phi_E", "=", r"\frac{q}{4\pi\varepsilon_0}", r"\,d\Omega_{\rm or}", size=40, colors={3: ANG}).move_to(P(RX, YS))
        self.play(Write(s1), run_time=0.9)
        self.play(TransformMatchingTex(s1, s2), run_time=1.0)
        self.play(TransformMatchingTex(s2, s3), run_time=1.0)
        self.play(Indicate(s3[3], color=WHITE, scale_factor=1.12), Indicate(orr[4], color=WHITE, scale_factor=1.12), run_time=0.8)
        self.flatten(s3)
        self.play(ReplacementTransform(s3[0], s4[0]), ReplacementTransform(s3[1], s4[1]), ReplacementTransform(s3[2], s4[2]),
                  FadeOut(s3[3], shift=0.1 * UP), TransformFromCopy(orr[0], s4[3]), run_time=1.2)
        self.regroup(s4)

        # carga interna: os ângulos sólidos completam 4π
        self.at(c[11])
        a0 = PH.get_value()
        sweep = always_redraw(lambda: sector_fill(cq, rb, a0, a0 + SW.get_value(), 0.12 * SWO.get_value())
                              if SW.get_value() > 1 else VMobject())
        self.remove(ghost)
        self.add(sweep)
        PH.add_updater(lambda m: m.set_value(a0 + SW.get_value()))
        self.add(PH)
        # três níveis: equação principal (∮ dΩ_or = 4π) · comentário geométrico (4π sr) · consequência (Φ_E = q/ε0)
        tot = eq(r"\oint_S d\Omega_{\rm or}", "=", r"4\pi", size=44).move_to(P(RX, -0.95))
        defs = VGroup(dom_lab, domB, or_lab, orr)
        self.play(SWO.animate.set_value(1.0), LO.animate.set_value(0.0), FO.animate.set_value(0.0), LBO.animate.set_value(0.0),
                  FadeOut(pm), s4.animate.move_to(P(RX, 0.2)), defs.animate.set_opacity(0.45),
                  dom_box.animate.set_stroke(opacity=0.35), run_time=0.6)
        self.play(SW.animate.set_value(360.0), run_time=4.0, rate_func=linear)
        self.play(Write(tot), run_time=1.0)
        PH.clear_updaters()
        self.remove(PH)
        self.at(c[12])
        # 4π como comentário geométrico: todas as direções do espaço = área da esfera unitária
        icon = VGroup(Circle(radius=0.24).set_stroke(ANG, 1.8).set_fill(ANG, 0.12),
                      DashedVMobject(Ellipse(width=0.48, height=0.14), num_dashes=10).set_stroke(ANG, 1.2, 0.7))
        geo = hchain(icon, text("todas as direções =", 18, opacity=AUX_OP), eq(r"4\pi\ \mathrm{sr}", size=26, color=ANG),
                     text("(esfera unitária)", 18, opacity=0.55), buff=0.14)
        fit(geo, 6.6).move_to(P(RX, -1.85))
        self.play(FadeIn(geo, shift=0.08 * UP), run_time=1.0)
        self.at(c[13])
        # consequência: os fatores 4π se cancelam
        res = eq(r"\Phi_E", "=", r"\frac{q}{4\pi\varepsilon_0}\cdot 4\pi", "=", r"\frac{q}{\varepsilon_0}", size=42)
        res.move_to(P(RX, -2.85))
        # atenua o comentário geométrico sem mexer no preenchimento do ícone (set_opacity encheria o círculo)
        self.play(FadeIn(res[0:2]), TransformFromCopy(VGroup(s4[2], tot[2]), res[2]), geo[1:].animate.set_opacity(0.45),
                  icon.animate.set_stroke(opacity=0.45), run_time=1.2)
        self.play(FadeIn(res[3:], shift=0.1 * LEFT), run_time=0.8)
        self.at(c[14])

        # COMPARE: interna (4π) × externa (0); a carga externa continua produzindo campo na superfície
        for m in (cone_m, pc_m, labs, sweep):
            m.clear_updaters()
        left_grp = VGroup(surf, k4.q, refc, sweep, cone_m)
        self.play(FadeOut(VGroup(s4, dom_lab, domB, dom_box, or_lab, orr, res, pc_m, labs, geo)),
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
        self.at(c[15])
        ext_field = coulomb([bc + BS2 * blob(a) * U(a) for a in range(0, 360, 20)], [qe], 0.95, 0.12, 0.9, w=4)
        self.play(LaggedStart(*[GrowArrow(a) for a in ext_field], lag_ratio=0.05), run_time=2.2)
        self.at(c[16])
        self.play(LaggedStart(*[Indicate(a, color=CYAN, scale_factor=1.3) for a in ext_field[7:12]], lag_ratio=0.1), run_time=1.4)
        self.at(c[17])
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
                out.add(Line(*pin).set_stroke(DAVEC, 8, o), Line(*pout).set_stroke(DAVEC, 8, o))
            return out
        ecm = always_redraw(ext_cone)
        signs = VGroup(eq(r"d\Omega_{\rm or}=-d\Omega", size=24, color=ANG), eq(r"d\Omega_{\rm or}=+d\Omega", size=24, color=ANG))

        def place_signs(m):
            a = PE.get_value()
            _, pin, pout = ext_geom(a)
            o = CE.get_value() if pin is not None else 0.0
            if pin is not None:
                m[0].move_to((pin[0] + pin[1]) / 2 - (0.3 + m[0].width / 2) * U(a) + 0.36 * U(a + 90))
                m[1].move_to((pout[0] + pout[1]) / 2 + 0.78 * U(a + 90) + 0.3 * U(a))
                if m[1].get_right()[0] > 6.95:                                  # trava na borda direita do quadro
                    m[1].shift((6.95 - m[1].get_right()[0]) * RIGHT)
            m.set_opacity(o)
        signs.add_updater(place_signs)
        self.add(ecm, signs)
        self.play(CE.animate.set_value(1.0), run_time=0.8)
        self.play(PE.animate.set_value(22.0), run_time=4.2)
        self.play(PE.animate.set_value(6.0), run_time=1.6)
        self.at(c[18])
        tot_out = eq(r"\oint_S d\Omega_{\rm or}", "=", "0", size=42).scale(0.85).move_to(P(RX, -2.35))
        self.play(Write(tot_out), run_time=1.0)
        self.at(c[19])

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
        self.at(c[20])
        # contribuições fora da superfície, ligadas às cargas por guias tracejadas
        def tagged(lab, at_, q):
            lab.move_to(at_)
            start = lab.get_center() + (lab.width / 2 + 0.1) * np.sign(q[0] - at_[0]) * RIGHT
            lead = DashedLine(start, q + 0.18 * (start - q) / np.linalg.norm(start - q), dash_length=0.06).set_stroke(WHITE, 1.5, 0.6)
            return VGroup(lab, lead)
        k3 = tagged(hchain(eq("0", size=36), text("no fluxo", 20, opacity=0.85), buff=0.12), P(1.3, 1.85), qs_pos[2])
        self.play(Indicate(charges[2], color=WHITE, scale_factor=1.5), FadeIn(k3), run_time=1.2)
        self.at(c[21])
        k1 = tagged(eq(r"\frac{q_1}{\varepsilon_0}", size=36), P(0.85, 0.45), qs_pos[0])
        k2 = tagged(eq(r"\frac{q_2}{\varepsilon_0}", size=36), P(0.85, -0.75), qs_pos[1])
        self.play(FadeIn(k1), FadeIn(k2), run_time=1.0)
        self.at(c[22])
        qenv = eq(r"Q_{\mathrm{env}}", "=", "q_1", "+", "q_2", size=40, colors={0: BLUE_L}).move_to(P(4.4, -1.0))
        qenv_lab = text("soma algébrica das cargas internas", 22, opacity=0.85).move_to(P(4.4, -1.7))
        self.play(TransformFromCopy(VGroup(charges[0][2], charges[1][2]), VGroup(qenv[2], qenv[4])),
                  FadeIn(VGroup(qenv[0], qenv[1], qenv[3])), run_time=1.4)
        self.play(FadeIn(qenv_lab), run_time=0.8)
        self.at(c[23])
        law = eq(r"\oint_S", r"\vec E\cdot d\vec A", "=", r"\frac{Q_{\mathrm{env}}}{\varepsilon_0}", size=52).move_to(P(4.4, 0.65))
        self.play(Write(law), run_time=1.6)
        self.at(c[24])
        self.play(Create(box(law)), run_time=0.9)
        self.at(c[-1] + 0.6)

    # ── 06 · Superfície deliberadamente ruim (COMPARE / BUILD) ──────────────
    def b06_superficie_ruim(self):
        self.begin(6, "superficie_ruim")
        c = self.marcos(6)
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
        normals = VGroup(*[vec(p, p + 0.45 * U(a), NHAT, 3.5, z=5) for a, p in zip(range(0, 360, 30), pts)])
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
                               .set_stroke(ANG, 4.5)))
        others = [nm for j, nm in enumerate(normals) if j not in three]
        self.play(*[nm.animate.set_opacity(0.3) for nm in others],
                  LaggedStart(*[Create(a) for a in th_arcs], lag_ratio=0.4), run_time=1.8)
        thn = eq(r"\theta_i\neq0", size=38, color=ANG).move_to(P(RX, -1.95))
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
                    vec(p, p + L * e_dir, CYAN, 7, o, z=8), vec(p, p + 0.55 * U(a), NHAT, 4, o, z=9),
                    Arc(radius=0.42, start_angle=np.radians(a), angle=np.radians(dd), arc_center=p).set_stroke(ANG, 3.5, o))
            return out
        prb = always_redraw(probe)
        pe = lambda: float(KE / np.dot(cc + RG * U(PA.get_value()) - qp, cc + RG * U(PA.get_value()) - qp))
        e_lab = eq(r"|\vec E|", size=36, color=CYAN).move_to(P(RX - 2.2, -1.2))
        e_bar = always_redraw(lambda: Rectangle(width=max(1.3 * pe(), 0.02), height=0.24).set_stroke(width=0)
                              .set_fill(CYAN, 0.85 * PRO.get_value()).next_to(P(RX - 1.6, -1.2), RIGHT, buff=0))
        t_lab = eq(r"\theta=", size=36, color=ANG).move_to(P(RX - 1.9, -1.95))

        def theta_now():
            p = cc + RG * U(PA.get_value())
            e_dir = (p - qp) / np.linalg.norm(p - qp)
            return abs((ang(e_dir) - PA.get_value() + 180) % 360 - 180)
        t_val = DecimalNumber(0, num_decimal_places=0, unit=r"^\circ", font_size=36, color=ANG)
        t_val.add_updater(lambda m: m.set_value(theta_now()).next_to(t_lab, RIGHT, buff=0.12).set_opacity(PRO.get_value()))
        self.add(prb, e_bar, t_val)
        self.play(FadeOut(VGroup(ineq, thn)), PRO.animate.set_value(1.0), FadeIn(e_lab), FadeIn(t_lab),
                  *[a.animate.set_opacity(0.35) for a in arrows], run_time=0.8)
        self.play(PA.animate.set_value(360.0), run_time=6.0, rate_func=linear)
        self.at(c[14])
        pay = hchain(display("FLUXO CONHECIDO", 32), eq(r"\neq", size=48, color=MAGENTA),
                     display("CAMPO LOCAL CONHECIDO", 32), buff=0.3).move_to(P(0, -2.8))
        self.play(FadeIn(pay, shift=0.12 * UP), run_time=1.4)
        self.at(c[-1] + 1.2)

    # ── 07 · Simetria da fonte (FOCUS) ──────────────────────────────────────
    def b07_simetria(self):
        self.begin(7, "simetria")
        c = self.marcos(7)
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
        normals = VGroup(*[vec(cs + RS * U(a), cs + (RS + 0.32) * U(a), NHAT, 3.5, z=5) for a in range(int(a_p) + 15, int(a_p) + 375, 30)])
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
        c = self.marcos(8)
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
                        .set_stroke(ANG, 3.5, o))
            if PHO.get_value() > 0.01:
                o = PHO.get_value()
                v = sph(rp, tt, ff)
                foot = p3(cc, s, (v[0], v[1], 0.0))
                out.add(DashedLine(cc, p3(cc, s, (1.12, 0, 0)), dash_length=0.08).set_stroke(WHITE, 1.5, 0.5 * o),
                        DashedLine(cc, foot, dash_length=0.06).set_stroke(WHITE, 1.5, 0.6 * o),
                        DashedLine(pt3(), foot, dash_length=0.06).set_stroke(WHITE, 1.5, 0.6 * o),
                        VMobject().set_points_as_corners([p3(cc, s, sph(0.28, 90, f)) for f in np.linspace(0, ff, 16)])
                        .set_stroke(ANG, 3.5, o))
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
                    out.add(Line(C[a], C[b]).set_stroke(WHITE, 6, o * h).set_z_index(10))
            return out.set_z_index(9)
        elem = always_redraw(element)
        clabs = VGroup(eq("r'", size=32), eq(r"\vartheta", size=32, color=ANG), eq(r"\phi", size=32, color=ANG), eq("z", size=28),
                       eq("dr'", size=28), eq(r"r'\,d\vartheta", size=28), eq(r"r'\sin\vartheta\,d\phi", size=28))

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
        self.at(self.ext("rowR"))
        self.play(FadeIn(rowR, shift=0.1 * DOWN), Indicate(rlab_R, color=BLUE_L, scale_factor=1.4), run_time=1.0)
        self.at(self.ext("rowr"))
        self.play(FadeIn(rowr, shift=0.1 * DOWN), Indicate(rlab, color=VIOLET, scale_factor=1.4), run_time=1.0)
        self.at(self.ext("rowp"))
        self.play(FadeIn(rowp, shift=0.1 * DOWN), PTO.animate.set_value(1.0), run_time=1.0)
        self.at(c[9])
        self.play(RP.animate.set_value(0.15), run_time=0.8)
        self.play(RP.animate.set_value(0.72), run_time=2.2)                  # r': distância ao centro
        self.at(c[10])
        note = left_at(hchain(eq(r"\vartheta", size=36, color=ANG), text("ângulo polar", 22, opacity=0.85), eq(r"\neq", size=32),
                              eq(r"\theta", size=36, color=ANG), text("ângulo do fluxo", 22, opacity=0.85)), 0.8, -0.75)
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
        dvp = eq("dV", "=", "dr'", r"\cdot", r"r'\,d\vartheta", r"\cdot", r"r'\sin\vartheta\,d\phi", size=40).move_to(P(RX, 1.35))
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
        qi = eq(r"Q_{\mathrm{env}}(r)=", r"\int_0^r\rho(r')\,r'^2dr'", r"\int_0^\pi\sin\vartheta\,d\vartheta", r"\int_0^{2\pi}d\phi",
                size=38)
        fit(qi, _R.width - 0.3).move_to(P(RX, 0.05))
        self.play(TransformMatchingTex(q1, qi), LBO.animate.set_value(0.0), AZO.animate.set_value(0.0),
                  PHO.animate.set_value(0.0), THO.animate.set_value(0.0), *[h.animate.set_value(0.0) for h in HL.values()],
                  VEO.animate.set_value(1.0), run_time=1.3)
        self.play(RP.animate.set_value(0.1), run_time=0.8)
        self.play(RP.animate.set_value(X.get_value() - DR_ / 2 - 0.02), Indicate(qi[1], color=VIOLET), run_time=2.6, rate_func=linear)
        self.at(c[17])
        # forma geral em simetria esférica: os ângulos dão 4π para qualquer ρ(r')
        bq = VGroup()
        for i, v in zip((2, 3), (eq("2", size=36), eq(r"2\pi", size=36))):
            b = Brace(qi[i], DOWN, buff=0.08)
            v.next_to(b, DOWN, buff=0.08)
            bq.add(VGroup(b, v))
            self.play(FadeIn(b), FadeIn(v, shift=0.1 * DOWN), run_time=0.7)
        qg = eq(r"Q_{\mathrm{env}}(r)", "=", r"4\pi", r"\int_0^r\rho(r')\,r'^2dr'", size=40, colors={0: BLUE_L}).move_to(P(RX, -1.55))
        self.play(TransformFromCopy(VGroup(bq[0][1], bq[1][1]), qg[2]), TransformFromCopy(qi[1], qg[3]), FadeIn(qg[0:2]),
                  run_time=1.3)
        self.at(c[18])
        eg = eq("E(r)", "=", r"\frac{Q_{\mathrm{env}}(r)}{4\pi\varepsilon_0 r^2}", size=42, colors={0: CYAN}).move_to(P(RX, 0.5))
        lesson = VGroup(text("a simetria resolve a geometria", 22, opacity=0.9),
                        hchain(eq(r"\rho(r)", size=30, color=BLUE_L), text("só determina quanta carga há dentro de", 22, opacity=0.9),
                               eq("r", size=30, color=VIOLET), buff=0.12)).arrange(DOWN, buff=0.16)
        fit(lesson, 6.7).move_to(P(RX, -0.85))
        self.play(FadeOut(VGroup(q1, dv2, qi, bq)), qg.animate.move_to(P(RX, 1.95)), run_time=1.2)
        self.play(Write(eg), run_time=1.2)
        self.play(FadeIn(lesson, shift=0.1 * UP), run_time=1.0)
        self.at(c[19])
        # densidade constante: a única integral restante dá r³/3
        const = hchain(eq(r"\rho", size=30, color=BLUE_L), text("constante", 20, opacity=0.85), buff=0.12).move_to(P(RX, -1.2))
        qr = eq(r"Q_{\mathrm{env}}", "=", r"\frac43\pi\rho r^3", size=44, colors={0: BLUE_L}).move_to(P(RX, -2.1))
        self.play(FadeOut(lesson), FadeIn(const), run_time=0.7)
        self.play(TransformFromCopy(VGroup(qg[2], qg[3]), qr[2]), FadeIn(qr[0:2]), run_time=1.3)

        # Gauss interior: uma operação por passo (a troca de tela e a lei entram ainda na frase anterior, que tem folga)
        for m in (crd, elem, clabs):
            m.clear_updaters()
        self.play(FadeOut(VGroup(crd, elem, clabs, qg, eg, const)), qr.animate.scale(0.8).move_to(P(RX, 2.25)),
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
        self.at(c[20])
        self.play(TransformMatchingTex(h0, h1), Indicate(qr, color=WHITE), run_time=1.1)       # substituir Q_env
        st = VGroup(strike(h1[1], WHITE), strike(h1[5], WHITE))
        self.play(Create(st), run_time=0.7)                                                    # cancelar 4π
        self.play(FadeOut(st), h1[1].animate.set_opacity(0), h1[5].animate.set_opacity(0), run_time=0.5)   # some no lugar
        self.remove(h1)
        rest = [h1[i] for i in (0, 2, 3, 4, 6, 7)]
        self.add(*rest)
        self.play(*[ReplacementTransform(a, b) for a, b in zip(rest, h2)], run_time=1.0)
        self.regroup(h2)
        self.at(c[21])
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
        tag_in = domain_tag("interior", "(r<R)").next_to(b4, DOWN, buff=0.3)
        self.play(Create(b4), FadeIn(tag_in, shift=0.1 * UP), run_time=0.8)
        self.at(c[22])
        self.play(X.animate.set_value(0.9), run_time=2.2, rate_func=linear)                  # cresce linearmente
        self.play(X.animate.set_value(0.3), run_time=1.6, rate_func=linear)
        self.play(Indicate(tag_in, color=WHITE, scale_factor=1.15), run_time=1.0)
        self.at(c[23])
        e0 = eq("E(0)=0", size=36).move_to(P(RX, -1.4))
        self.play(X.animate.set_value(0.0), FadeIn(e0), run_time=1.4)
        self.at(c[24])

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
        qin = eq(r"Q_{\mathrm{env}}=\frac43\pi\rho r^3", size=30).move_to(P(RX, 0.15))
        qout = eq(r"Q_{\mathrm{env}}=Q=\frac43\pi\rho R^3", size=30).move_to(P(RX, 0.15))
        qin.add_updater(lambda m: m.set_opacity(0.8 * QM.get_value() * (1.0 if X.get_value() < 1 else 0.0)))
        qout.add_updater(lambda m: m.set_opacity(0.8 * QM.get_value() * (1.0 if X.get_value() >= 1 else 0.0)))
        self.add(qbar, qin, qout)
        self.play(QM.animate.set_value(1.0), FadeIn(qlab), FadeIn(qcap), run_time=0.8)
        self.play(X.animate.set_value(1.0), run_time=2.2, rate_func=linear)
        r_eq_R = eq("r=R", size=36).move_to(cc + P(0, -1.25 - 0.5))
        self.play(FadeIn(r_eq_R, shift=0.1 * DOWN), Flash(cc + 1.25 * U(A_P), color=WHITE, flash_radius=0.3), run_time=1.0)
        self.at(c[25])
        self.play(FadeOut(r_eq_R), X.animate.set_value(1.6), run_time=3.2, rate_func=linear)
        self.at(c[26])
        self.play(Indicate(VGroup(qbar, qcap), color=BLUE_L, scale_factor=1.05), run_time=1.2)
        self.at(c[27])
        YX = -1.3
        x0 = eq("E(r)", r"\,4\pi r^2", "=", r"\frac{Q}{\varepsilon_0}", size=44, colors={0: CYAN}).move_to(P(RX, YX))
        self.play(Write(x0), run_time=1.3)
        self.at(c[28])
        x1 = eq("E(r)", "=", r"\frac{Q}{4\pi\varepsilon_0 r^2}", size=44, colors={0: CYAN}).move_to(P(RX, YX))
        x2 = eq("E(r)", "=", r"\frac{\rho R^3}{3\varepsilon_0 r^2}", size=48, colors={0: CYAN}).move_to(P(RX, YX))
        self.play(TransformMatchingTex(x0, x1), X.animate.set_value(2.1), run_time=1.6)        # dividir por 4πr²
        self.play(TransformMatchingTex(x1, x2), Indicate(qout, color=WHITE), run_time=1.3)     # substituir Q
        b2 = box(x2)
        tag_out = domain_tag("exterior", "(r>R)").next_to(b2, DOWN, buff=0.3)
        self.play(Create(b2), FadeIn(tag_out, shift=0.1 * UP), run_time=0.8)
        self.at(c[29])
        rgt = eq("r>R", size=36).move_to(cc + 2.1 * 1.25 * U(A_P) + P(0.45, -0.5))
        pq = charge(cc, label="Q")
        self.play(SFO.animate.set_value(0.15), FadeIn(pq, scale=0.5), FadeIn(rgt), run_time=1.6)
        self.wait(2.2)
        self.play(Indicate(fld, color=CYAN, scale_factor=1.08), run_time=1.4)
        self.at(c[-1] - 2.0)
        self.play(SFO.animate.set_value(1.0), FadeOut(pq), run_time=1.4)
        self.at(c[-1] + 0.6)
        self.k8 = SimpleNamespace(c=cc, S=S, X=X, fld=fld, res_in=res_in, res_out=VGroup(x2, b2, tag_out), rgt=rgt,
                                  junk=VGroup(qbar, qin, qout, qlab, qcap))

    # ── 09 · Gráfico sincronizado (SPLIT): o mesmo X controla esfera e gráfico ──
    def b09_grafico(self):
        self.begin(9, "grafico")
        c = self.marcos(9)
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
        self.play(X.animate.set_value(2.1), run_time=3.4, rate_func=linear)
        self.play(FadeIn(f_out), Create(lead_out), run_time=0.8)
        self.at(c[5])
        cont = eq(r"E(R^-)=E(R^+)", size=32).move_to(peak + P(1.25, 0.5))
        self.play(FadeIn(cont, shift=0.1 * DOWN), Indicate(f_in[0], color=WHITE), Indicate(f_out[0], color=WHITE), run_time=1.4)
        self.at(c[6])
        # campo contínuo, inclinações diferentes de cada lado (sem esconder o bico)
        tl = DashedLine(ax.c2p(0.72, 0.72), ax.c2p(1.15, 1.15), dash_length=0.06).set_stroke(WHITE, 2.5, 0.9)
        tr = DashedLine(ax.c2p(0.9, 1.2), ax.c2p(1.2, 0.6), dash_length=0.06).set_stroke(WHITE, 2.5, 0.9)
        # comentário auxiliar, fora do vértice e das tangentes: à direita, abaixo da igualdade E(R⁻) = E(R⁺)
        slopes = text("inclinações diferentes", 18, opacity=AUX_OP).move_to(peak + P(1.75, 0.0))
        self.play(Create(tl), Create(tr), FadeIn(slopes), run_time=1.4)
        self.at(c[7])
        # continuidade em R: não há camada superficial singular de carga ali
        no_sigma = text("sem camada superficial de carga em R", 18, opacity=AUX_OP).move_to(P(peak[0] + 0.85, 1.5))
        self.play(FadeIn(no_sigma, shift=0.1 * DOWN), Flash(peak, color=WHITE, flash_radius=0.3), run_time=1.2)
        self.at(c[8])
        st["on"] = False
        q_const.clear_updaters()
        form = eq(r"\vec E(\vec r)=E(r)\hat r", size=38, color=CYAN).move_to(P(LX, 2.35))
        self.play(FadeOut(VGroup(tl, tr, slopes, q_const, no_sigma)), X.animate.set_value(1.5), run_time=1.4)
        self.at(c[9])
        self.play(FadeIn(form, shift=0.1 * DOWN), run_time=1.0)
        self.at(c[10])
        self.play(Circumscribe(form, color=WHITE, stroke_width=2), Indicate(k.fld, color=CYAN, scale_factor=1.06), run_time=1.8)
        self.at(c[-1] + 1.0)

    # ── 10 · Três simetrias clássicas: regiões que contribuem e de fluxo nulo ──
    def b10_tres_simetrias(self):
        self.begin(10, "tres_simetrias")
        c = self.marcos(10)
        self.clear(run_time=0.9)
        BIG_C, BIG_K, SMALL_K = P(-2.9, -0.25), 1.3, 0.85
        slots = (P(-4.75, -0.25), P(0.0, -0.25), P(4.75, -0.25))

        def rule(lugar, rel, res):
            return hchain(text(lugar, 24, opacity=0.9), eq(rel, size=32), eq(r"\Rightarrow", size=30), text(res, 24, opacity=0.9))

        names = ("esfera concêntrica", "cilindro coaxial", "cilindro gaussiano curto")
        notes = ("toda a superfície contribui", "lateral contribui · tampas: fluxo nulo", "tampas contribuem · lateral: fluxo nulo")
        hyps = ("distribuição esfericamente simétrica", "linha infinita, uniformemente carregada",
                "plano infinito, uniformemente carregado")
        tags = (None, "translação + rotação + reflexão", "translação + rotação no plano + reflexão")
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
            if tags[i]:
                hyp = VGroup(hyp, left_at(text(tags[i], 20, opacity=0.7), 0.6, 1.42))
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
                self.wait(1.0)
                self.play(FadeIn(pn.el_z), FadeIn(rws[1], shift=0.1 * DOWN), Indicate(pn.zero, color=WHITE, scale_factor=1.04),
                          run_time=1.3)
            self.wait(0.8)
            name = text(names[i], 24, opacity=0.9).move_to(slots[i] + P(0, -2.25))
            note = text(notes[i], 18, opacity=0.8).move_to(slots[i] + P(0, -2.62))
            fit(note, 4.5)
            self.regroup(grp)
            self.play(grp.animate.scale(SMALL_K / BIG_K).move_to(slots[i]), FadeOut(VGroup(hyp, rws)),
                      FadeIn(name), FadeIn(note), run_time=1.3)
            small.append(SimpleNamespace(grp=grp, contrib=pn.contrib, name=name, note=note))
        self.at(c[4])
        # as simetrias clássicas são exatas só nas idealizações infinitas
        ideal = VGroup(text("simetrias exatas só nas idealizações infinitas", 26, opacity=0.9),
                       text("objetos finitos: só aproximam longe das bordas", 20, opacity=0.75)).arrange(DOWN, buff=0.14)
        ideal.move_to(P(0, 2.4))
        self.play(FadeIn(ideal, shift=0.1 * DOWN), *[FadeIn(VGroup(s.grp, s.name, s.note)) for s in small[:-1]], run_time=1.4)
        self.at(c[5])
        flow = hchain(text("fonte", 26), eq(r"\rightarrow", size=34), text("simetria", 26), eq(r"\rightarrow", size=34),
                      text("forma do campo", 26), eq(r"\rightarrow", size=34), text("superfície útil", 26))
        fit(flow, 13.6).move_to(P(0, 2.4))
        self.play(FadeOut(ideal, shift=0.1 * UP), FadeIn(flow, shift=0.1 * DOWN), run_time=1.2)
        self.at(c[6])
        self.play(LaggedStart(*[Indicate(s.contrib, color=VIOLET, scale_factor=1.06) for s in small], lag_ratio=0.35), run_time=2.4)
        self.at(c[-1] + 1.0)

    # ── 11 · Quando Gauss não simplifica: casos, caminhos adequados e método ──
    def b11_casos_e_metodo(self):
        self.begin(11, "casos_caminhos_metodo")
        c = self.marcos(11)
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
        # faixa da linha ativa: cada pergunta é aplicada aos dois exemplos no momento em que aparece
        band = Rectangle(width=13.3, height=0.6).set_stroke(width=0).set_fill(WHITE, 0.07).move_to(P(0.3, ys[0]))

        def fill_row(i):
            """Pergunta i e as respostas dos dois exemplos, em sequência; as linhas anteriores recuam um pouco."""
            back = [m.animate.set_opacity(0.55) for m in (items[i - 1], ansA[i - 1], ansB[i - 1])] if i else []
            self.play(FadeIn(items[i], shift=0.12 * DOWN), band.animate.move_to(P(0.3, ys[i])), *back, run_time=0.7)
            self.play(FadeIn(ansA[i], shift=0.15 * RIGHT), run_time=0.5)
            self.play(FadeIn(ansB[i], shift=0.15 * RIGHT), run_time=0.5)
        self.at(marks[0])
        self.play(FadeIn(hA), FadeIn(hB), FadeIn(band), run_time=0.7)
        fill_row(0)
        for i in range(1, 6):
            self.at(marks[i])
            arr = Arrow(items[i - 1].get_bottom() + 0.04 * DOWN, items[i].get_top() + 0.04 * UP, buff=0.03, stroke_width=4,
                        max_tip_length_to_length_ratio=0.35, color=WHITE).set_opacity(0.8)
            self.play(GrowArrow(arr), run_time=0.4)
            fill_row(i)
        self.play(Create(box(items[5])), run_time=0.6)
        # veredito por coluna: onde as peças se encaixam (esfera) e onde não (barra)
        colA = SurroundingRectangle(VGroup(hA, *ansA), color=WHITE, buff=0.18, corner_radius=0.1, stroke_width=2.5)
        colB = SurroundingRectangle(VGroup(hB, *ansB), color=WHITE, buff=0.18, corner_radius=0.1, stroke_width=2.5)
        self.at(c[17] + 3.2)
        self.play(FadeOut(band), *[m.animate.set_opacity(0.9) for m in ansA], Create(colA), run_time=0.9)
        self.play(Indicate(ansA[5], color=WHITE, scale_factor=1.15), run_time=1.0)
        self.at(c[18])
        self.play(ReplacementTransform(colA, colB), *[m.animate.set_opacity(0.55) for m in ansA],
                  *[m.animate.set_opacity(0.9) for m in ansB], run_time=1.0)
        self.play(Indicate(ansB[5], color=WHITE, scale_factor=1.15), run_time=1.0)
        self.at(c[18] + 5.0)
        self.play(*[m.animate.set_opacity(0.9) for m in (*items, *ansA, *ansB)], colB.animate.set_stroke(opacity=0.35),
                  run_time=1.0)
        self.at(c[-1] + 0.8)

    # ── 12 · Retorno (COMPARE) · payoff (FOCUS) · pausa · outro (END SCREEN) ──
    def b12_retorno_payoff_outro(self):
        self.begin(12, "retorno_payoff_outro")
        c = self.marcos(12)
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
        self.respiro(c[5], 0.8)                                              # pausa entre payoff e CTA
        self.at(c[5] - 0.5)
        # outro: sem destinos definidos → marca centralizada e mensagem curta; anéis com movimento discreto
        oc = P(0, 0.2)
        rings = VGroup(*[gauss_circle(oc, r, op=0.16, n=int(14 * r)) for r in (2.0, 3.0, 4.0)])
        for i, r_ in enumerate(rings):
            r_.add_updater(lambda m, dt, s=(1 if i % 2 == 0 else -1) * (0.06 - 0.01 * i): m.rotate(s * dt, about_point=oc))
        logo = ImageMobject(str(LOGO_PATH)).set_width(6.0).move_to(oc + P(0, 0.4))
        msg = text("Inscreva-se para acompanhar os próximos vídeos", 28, opacity=0.9).move_to(oc + P(0, -1.2))

        def ripple():
            """Onda discreta saindo da marca (sem conteúdo novo): um anel tracejado que cresce e some."""
            w = gauss_circle(oc, 1.6, op=0.35, n=24)
            self.play(w.animate.scale(2.6, about_point=oc).set_stroke(opacity=0.0), run_time=2.6)
            self.remove(w)
        self.play(FadeOut(VGroup(p1, p2)), FadeOut(self.wm), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(r_, scale=0.85) for r_ in rings], lag_ratio=0.3), FadeIn(logo, scale=0.92), run_time=1.8)
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=1.0)
        self.at(c[6])
        ripple()
        self.at(c[7])
        ripple()
        self.at(c[-1] + 1.2 + 1.8)
