"""yt_0002 — Lei de Gauss: três simetrias, um método. Bloco N01–N29 (0:00–18:01), preview sem voz — vídeo completo.

Fonte de verdade: producao.md, narracao.md, storyboard.md e ficha.md desta pasta; continuidade visual com
videos_longos/yt_0001_lei_gauss/cena.py (b02_intro: marca, título, subtítulo, watermark, header).

Escopo desta cena: N01 cold open · N02 intro humana · N03 recapitulação e algoritmo · N04 linha infinita: reconhecer
a simetria · N05 linha: lateral e tampas · N06 carga envolvida e resultado E ∝ 1/r · N07 casca · N08 maciço · N09 gráfico ·
N10 coaxial · N11 síntese cilíndrica · N12 folha infinita · N13 placa (slab) · N14 duas folhas · N15 face de condutor e
síntese planar · N20 casca esférica (aparato) · N21 casca: regiões · N22 esfera maciça e gráfico · N23 capacitor esférico.
N24 três capacitores · N25 áreas e potências · N26 checklist aplicado · N27 payoff · N28 pausa · N29 CTA/outro. Os tempos são o orçamento editorial
(N01 0–22 · N02 22–36 · N03 36–77 · N04 77–123 · N05 123–172 · N06 172–216 · N07 216–262 · N08 262–314 ·
N09 314–341 · N10 341–382 · N11 382–392), não áudio medido.

Gramática visual: ciano = E⃗ · azul (contorno contínuo + preenchimento) = fonte física · violeta tracejado =
superfície gaussiana (construção matemática; traço contínuo = parte que contribui) · azul elétrico = n̂ ·
violeta #745CFF = d⃗A · branco = matemática neutra.

Preview:  uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_0002_lei_gauss_casos_classicos/cena.py LeiGaussCasosClassicos002
SO=4 (ou SO=4,5) renderiza só esses blocos (os outros rodam sem gerar quadros). GUIAS=1 mostra a safe area.
"""

import json
import math
import os
import sys
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from manim import (
    BOLD, DOWN, LEFT, ORIGIN, RIGHT, UL, UP, UR, Annulus, Arrow, Axes, Brace, Circle, Create, DashedLine, DashedVMobject, Ellipse,
    FadeIn, FadeOut, ImageMobject, Indicate, LaggedStart, Line, MathTex, Polygon, ReplacementTransform, Scene,
    SurroundingRectangle, Transform, TransformMatchingTex, UpdateFromAlphaFunc, ValueTracker, VGroup, VMobject, Wait,
    always_redraw, config, smooth,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import DISPLAY_FONT, official_text, screen_text  # noqa: E402
from template.layout_horizontal import GUIAS, safe_guides, split  # noqa: E402
from MF_Tools import TransformByGlyphMap  # noqa: E402

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

# ── Paleta e parâmetros de série (idênticos ao yt_0001) ─────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR      # campo elétrico e E
BLUE = "#267BFF"          # distribuição física (preenchimento)
BLUE_L = "#7FB2FF"        # contorno da distribuição física, R, Q
VIOLET = "#9C8CFF"        # superfície gaussiana, r
NHAT = "#267BFF"          # normal unitária n̂
DAVEC = "#745CFF"         # vetor área d⃗A
AUX_OP = 0.85             # rótulos e comentários auxiliares: abaixo do resultado, mas legíveis no fundo escuro
OP_PREV = 0.75            # estados anteriores de uma construção (hierarquia secundária)
HEADER = "ELETROMAGNETISMO · LEI DE GAUSS"
WM_W, WM_OP = 1.92, 0.45

_L, _R = split(0.5)
LX, RX, MY = _L.x, _R.x, _L.y      # ≈ −3.75, 3.75, −0.2
RL = 1.15                           # borda esquerda da coluna de análise (≈ 44% do quadro): texto e fórmulas alinhados a ela

# Tipografia congelada: texto (Space Grotesk) em três níveis e matemática (MathTex) em três; MathTex 30 ≈ Text 24 em corpo visual
T_TITLE, T_BODY, T_NOTE = 36, 28, 24      # headline (negrito) · texto principal · nota/rótulo
T_LABEL = T_NOTE
M_L, M_M, M_S = 50, 40, 30                # equação ativa · equação secundária · domínios, símbolos e rótulos matemáticos
M_D = 34
# Traços: fontes e contornos físicos 4 · campo E 4,5 · construção 4 · resultante 7 · normais 3,5 · guias 2 · cargas pontuais 2,5
LW_SRC, LW_VEC, LW_THICK, LW_RES, LW_N, LW_THIN, LW_DOT = 4, 4.5, 4, 7, 3.5, 2, 2.5

# Geometria da linha e do cilindro gaussiano (vista lateral): r = RV, comprimento L = YT − YB
AX = -3.3                           # x do eixo da linha: centro do diagrama (≈ 56% do quadro à esquerda)
RV, YB, YT, EL = 1.2, -1.35, 1.35, 0.3
YW0, YW1 = -2.2, 2.0                # extensão sólida da linha na tela
P_OBS = np.array([AX + RV, 0.0, 0.0])   # ponto de observação (e depois, ponto da lateral)

# Orçamento editorial (s)
T_N02, T_N03, T_N04, T_N05, T_N06, T_N07, T_N08, T_N09, T_N10, T_N11, T_N12, T_N13, T_N14, T_N15, T_N20, T_N21, T_N22, T_N23, T_N24, T_N25, T_N26, T_N27, T_N28, T_N29, T_FIM = (
    22.0, 36.0, 77.0, 123.0, 172.0, 216.0, 262.0, 314.0, 341.0, 382.0, 392.0, 504.0, 574.0, 616.0,
    681.0, 731.0, 776.0, 840.0, 886.0, 928.0, 980.0, 1038.0, 1056.0, 1058.0, 1081.0)

# ── Ritmo: a voz manda (mesmo mecanismo do yt_0001; ver gerar_sync.py) ──────
# Os marcos editoriais at(t) abaixo (segundos do orçamento de 18:01) são convertidos pelo mapa linear por partes `knots` de sync.json
# no instante da fala (áudio original) que corresponde a eles. Quando uma animação não cabe até o marco seguinte, a cena registra a
# espera que a voz precisa ganhar (pads.json); `gerar_sync.py montar` insere essas esperas em pausas reais da fala
# (audio/narracao_montagem.wav) e gera a legenda. Sem sync.json (ou com SEM_VOZ=1) a cena roda como o preview sem voz.
VOZ = (PASTA / "sync.json").exists() and os.environ.get("SEM_VOZ") != "1"
KNOTS = np.array(json.loads((PASTA / "sync.json").read_text(encoding="utf-8"))["knots"]) if VOZ else None
TOL = 0.1                                       # atraso tolerado num marco antes de pedir espera à voz
# Ritmo por trecho (entre dois marcos): onde a animação desenhada não cabe na fala, o trecho é comprimido antes de pedir espera à voz:
# primeiro as esperas explícitas (até P_ESPERA), depois as animações (até P_ANIM da duração). AJUSTAR=1 numa passada a seco recalcula ritmo.json.
RITMO_ARQ = PASTA / "ritmo.json"
AJUSTAR = os.environ.get("AJUSTAR") == "1"
RITMO = {} if (AJUSTAR or not VOZ or not RITMO_ARQ.exists()) else json.loads(RITMO_ARQ.read_text(encoding="utf-8"))
P_ESPERA, P_ANIM, FOLGA = 0.4, 0.62, 0.04


def voz(t):
    """Instante da fala (áudio original) que corresponde ao marco editorial t."""
    return float(np.interp(t, KNOTS[:, 0], KNOTS[:, 1])) if VOZ else t



# ── Texto e matemática (mesmos helpers do yt_0001) ──────────────────────────
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


def title(content, color=WHITE):
    """Ideia principal da tela: negrito, 36."""
    return display(content, T_TITLE, color, bold=True)


def body(content, color=WHITE, op=1.0):
    """Texto principal: 28."""
    return text(content, T_BODY, color, op)


def note(content, color=WHITE, op=0.92):
    """Nota curta de apoio: 24."""
    return text(content, T_NOTE, color, op)


def label(content, color=WHITE, op=AUX_OP):
    """Rótulo (mesmo corpo da nota): 24, nunca abaixo de 85% de opacidade."""
    return text(content, T_LABEL, color, op)


def col(m, y, dx=0.0):
    """Coluna de análise: centro vertical em y, borda esquerda alinhada a RL (+ dx)."""
    return m.move_to(P(0, y)).align_to(P(RL + dx, 0), LEFT)


def box(m, color=WHITE, buff=0.26):
    return SurroundingRectangle(m, color=color, buff=buff, corner_radius=0.1, stroke_width=2.0)


def hchain(*items, buff=0.18):
    return VGroup(*items).arrange(RIGHT, buff=buff)


def frac_parts(part):
    """(numerador, barra, denominador) de uma fração MathTex, por geometria (esquerda → direita)."""
    gl = list(part)
    bar = max(gl, key=lambda g: g.width)
    num = sorted((g for g in gl if g is not bar and g.get_y() > bar.get_y()), key=lambda g: g.get_x())
    den = sorted((g for g in gl if g is not bar and g.get_y() < bar.get_y()), key=lambda g: g.get_x())
    return num, bar, den


def strike(m, color=WHITE, w=4):
    return Line(m.get_corner(LEFT + DOWN) + 0.05 * (LEFT + DOWN), m.get_corner(RIGHT + UP) + 0.05 * (RIGHT + UP)).set_stroke(color, w)


# ── Geometria ───────────────────────────────────────────────────────────────
def P(x, y):
    return np.array([x, y, 0.0])


def U(deg):
    a = np.radians(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def unit(v):
    return v / np.linalg.norm(v)


def vec(p0, p1, color=CYAN, w=5, op=1.0, z=3):
    d = float(np.linalg.norm(p1 - p0))
    if d < 0.04 or op < 0.01:
        return VMobject()
    return Arrow(p0, p1, buff=0, stroke_width=w, tip_length=min(0.2, 0.42 * d), max_tip_length_to_length_ratio=0.5,
                 max_stroke_width_to_length_ratio=40, color=color).set_opacity(op).set_z_index(z)


def sign(p, minus=False, s=0.08, color=WHITE, w=2.5):
    g = VGroup(Line(p - s * RIGHT, p + s * RIGHT))
    if not minus:
        g.add(Line(p - s * UP, p + s * UP))
    return g.set_stroke(color, w).set_z_index(8)


def q_dot(p, minus=False, r=0.17):
    """Carga pontual: fonte física (azul, contorno + preenchimento) com o sinal dentro."""
    c = Circle(radius=r, arc_center=p).set_stroke(BLUE_L, 2.5).set_fill(BLUE, 0.55)
    return VGroup(c, sign(p, minus, s=0.47 * r)).set_z_index(6)


def right_angle(p, u1, u2, s=0.16, color=WHITE, w=2.5):
    return VMobject().set_points_as_corners([p + s * u1, p + s * (u1 + u2), p + s * u2]).set_stroke(color, w).set_z_index(9)


def polar_pts(c, rho, n=181):
    return np.array([c + rho(a) * U(a) for a in np.linspace(0.0, 360.0, n)])


def blob_a(a):
    t = np.radians(a)
    return 1 + 0.18 * np.sin(2 * t + 0.6) + 0.1 * np.cos(3 * t - 0.4)


def blob_b(a):
    t = np.radians(a)
    return 1 + 0.3 * np.cos(2 * t) + 0.08 * np.sin(3 * t)


def circ(a):
    return 1.0


def gauss_surface(c, scale, f, w=3.5):
    """Superfície gaussiana (construção matemática): violeta tracejado + preenchimento translúcido."""
    pts = polar_pts(c, lambda a: scale * f(a))
    fill = VMobject().set_points_as_corners(pts).set_stroke(width=0).set_fill(VIOLET, 0.07)
    ring = DashedVMobject(VMobject().set_points_as_corners(pts), num_dashes=64, dashed_ratio=0.6).set_stroke(VIOLET, w)
    return VGroup(fill, ring)


def smooth_closed(pts, stroke, fill, w=3.0, op=0.35):
    m = VMobject().set_points_smoothly(np.vstack([pts, pts[:1]]))
    return m.set_stroke(stroke, w).set_fill(fill, op)


def wire_line(x=AX, y0=YW0, y1=YW1, signs=True):
    """Linha de carga (fonte 1D): filamento fino azul luminoso com halo leve e pequenas marcas de carga."""
    g = VGroup(Line(P(x, y0), P(x, y1)).set_stroke(BLUE, 9, 0.3), Line(P(x, y0), P(x, y1)).set_stroke(BLUE_L, 3))
    if signs:
        g.add(*[sign(P(x, y0 + 0.25 + 0.5 * k), s=0.05, w=2) for k in range(int((y1 - y0) / 0.5))])
    return g.set_z_index(5)


# ── Cold open: três fontes, três perfis qualitativos ────────────────────────
def co_line(cx, cy, k=1.2):
    """Linha de carga e E⃗ cujo comprimento cai como 1/d (escada de distâncias)."""
    half = 1.5
    src = VGroup(Line(P(cx, cy - half), P(cx, cy + half)).set_stroke(BLUE, 12, 0.5), Line(P(cx, cy - half), P(cx, cy + half)).set_stroke(BLUE_L, 4),
                 *[sign(P(cx, cy - half + 0.25 + 0.5 * j), s=0.06) for j in range(6)]).set_z_index(5)
    fld = VGroup()
    for dy, d in zip((0.9, 0.3, -0.3, -0.9), (0.45, 0.8, 1.25, 1.8)):
        L = 0.3 / d
        for s in (-1, 1):
            fld.add(vec(P(cx + s * d, cy + dy), P(cx + s * (d + L), cy + dy), CYAN, 4.5))
    return SimpleNamespace(src=src.scale(k, about_point=P(cx, cy)), fld=fld.scale(k, about_point=P(cx, cy)))


def co_sphere(cx, cy, k=1.2):
    """Esfera carregada e E⃗ radial, só fora dela, com comprimento ∝ 1/d²."""
    c = P(cx, cy)
    body = VGroup(Circle(radius=0.62, arc_center=c).set_stroke(BLUE_L, LW_SRC).set_fill(BLUE, 0.4), sign(c, s=0.14)).set_z_index(5)
    fld = VGroup()
    for a, d in ((0, 0.85), (90, 0.85), (180, 0.85), (270, 0.85), (45, 1.35), (135, 1.35), (225, 1.35), (315, 1.35)):
        L = 0.7 * (0.85 / d) ** 2
        fld.add(vec(c + d * U(a), c + (d + L) * U(a), CYAN, 4.5))
    return SimpleNamespace(src=body.scale(k, about_point=c), fld=fld.scale(k, about_point=c))


def co_plates(cx, cy, k=1.2):
    """Duas placas paralelas e E⃗ uniforme no vão."""
    yt, yb, hw = cy + 0.85, cy - 0.85, 1.7
    src = VGroup()
    for y, minus in ((yt, False), (yb, True)):
        src.add(Line(P(cx - hw, y), P(cx + hw, y)).set_stroke(BLUE, 12, 0.5), Line(P(cx - hw, y), P(cx + hw, y)).set_stroke(BLUE_L, 4))
        src.add(*[sign(P(cx + x, y), minus, s=0.06) for x in np.arange(-1.5, 1.51, 0.6)])
    src.set_z_index(5)
    fld = VGroup(*[vec(P(cx + x, cy + 0.45), P(cx + x, cy - 0.45), CYAN, 4.5) for x in (-1.2, -0.6, 0.0, 0.6, 1.2)])
    c = P(cx, cy)
    return SimpleNamespace(src=src.scale(k, about_point=c), fld=fld.scale(k, about_point=c))


# ── 2.5D: perspectiva leve, fontes físicas e a gaussiana dinâmica (N04–N15) ─
# Grade da coluna de análise (SPLIT ≈ 56% diagrama / 44% matemática): a fórmula ativa fica sempre em Y_ACT;
# o domínio e a carga envolvida em Y_DOM; notas curtas em Y_NOTE; resultados já obtidos descem para Y_S1 e Y_S2.
Y_TAG, Y_DOM, Y_ACT, Y_NOTE, Y_S1, Y_S2 = 2.6, 1.7, 0.35, -0.6, -1.4, -2.4
SRC0 = -1.95                      # extremidade inferior visível das fontes (a linha das N03–N06 vai até YW0)
R_VIS, B_VIS = 0.8, 1.8           # raio da casca / do maciço / do condutor interno (R, a) e da casca externa (b)
YS_ARR = (-0.85, 0.0, 0.85)       # alturas das setas de E na lateral da gaussiana
LAV = "#D6CCFF"                   # carga envolvida realçada (violeta claro, só dentro da gaussiana)
CM = {"Q": BLUE_L, r"\vec E": CYAN, "E": CYAN, r"\hat n": NHAT, r"\lambda": BLUE_L, r"\rho": BLUE_L, r"\sigma": BLUE_L, r"\sigma_{\mathrm{face}}": BLUE_L,
      r"E_{+}": CYAN, r"E_{-}": CYAN, "|E_{+}|": CYAN, "|E_{-}|": CYAN, r"E_{\mathrm{dentro}}": CYAN, r"E_{\mathrm{fora}}": CYAN,
      r"E_{\mathrm{entre}}": CYAN}


def eqm(s, size=M_M, colors=None, color=WHITE):
    """MathTex com partes isoladas por {{ }} (cada parte vira um submobject com `tex_string`): o TransformMatchingTex move
    os termos iguais em vez de apagar e reescrever a linha. Cores por parte (chave = TeX da parte)."""
    m = MathTex(s, font_size=size, color=color)
    cm = CM if colors is None else colors
    for part in m:
        k = getattr(part, "tex_string", "").strip()
        if k in cm:
            part.set_color(cm[k])
    return m


def gx(s, n, size=M_L, cyan=(), blue=(), violet=()):
    """MathTex de string única para o TransformByGlyphMap (os glifos seguem a ordem do LaTeX). `n` = nº de glifos esperado: confere a
    estrutura real da expressão (falha alto se o LaTeX mudar). cyan/blue/violet: índices de glifos (E; fontes físicas ρ, σ, R; r da gaussiana)."""
    m = MathTex(s, font_size=size, color=WHITE)
    assert len(m[0]) == n, (s, len(m[0]))
    for idxs, c in ((cyan, CYAN), (blue, BLUE_L), (violet, VIOLET)):
        for i in idxs:
            m[0][i].set_color(c)
    return m


def gstrike(m, *idx, w=5):
    """Um risco por glifo (cancelamento mostrado antes de o fator sumir)."""
    return VGroup(*[strike(m[0][i], WHITE, w) for i in idx])


def gind(m, *idx, sf=1.3):
    """Pulso individual nos glifos `idx` de um MathTex de string única (cada um em torno do próprio centro)."""
    return [Indicate(m[0][i], color=WHITE, scale_factor=sf) for i in idx]


def mv(*pairs):
    """Entradas (glifo de A → glifo de B) do TransformByGlyphMap."""
    return [([i], [j]) for i, j in pairs]


def ef_line(r):
    """Linha: E ∝ 1/r em todo r (comprimento da seta na lateral)."""
    return 1.2 / r


def ef_casca(r):
    """Casca: nulo por dentro; 1/r por fora (contínuo com a linha em r = RV)."""
    return 1.2 / r if r > R_VIS else 0.0


def ef_solid(r):
    """Maciço uniforme: E ∝ r por dentro, ∝ 1/r por fora (E/E_R = u ou 1/u); mesma carga ⇒ mesmo exterior da casca."""
    u = r / R_VIS
    return 1.5 * (u if u <= 1 else 1 / u)


def ef_coax(r):
    """Coaxial: campo só no vão, ∝ 1/r."""
    return 1.2 / r if R_VIS < r < B_VIS else 0.0


def ef_none(r):
    return 0.0


def row(dom, expr, y, dx=1.3):
    """Linha da coluna de análise: domínio à esquerda (borda RL) e expressão alinhada a RL + dx."""
    dom.move_to(P(0, y)).align_to(P(RL, 0), LEFT)
    expr.move_to(P(0, y)).align_to(P(RL + dx, 0), LEFT)
    return dom, expr


def mix(*parts, size=T_LABEL, color=WHITE, op=AUX_OP, buff=0.14):
    """Texto misto: str vira texto (Space Grotesk); MathTex fica como está (λ, ρ… sempre em MathTex)."""
    return hchain(*[text(p, size, color, op) if isinstance(p, str) else p for p in parts], buff=buff)


def ery(rx):
    """Semi-eixo vertical das elipses de uma circunferência de raio rx, em perspectiva leve."""
    return 0.24 * rx + 0.03


def arc(cx, cy, rx, a0, a1, color, w, op=1.0, dashed=False):
    """Arco da elipse (a0 → a1, graus; 180–360 = metade da frente, 0–180 = metade de trás)."""
    pts = [P(cx + rx * math.cos(t), cy + ery(rx) * math.sin(t)) for t in np.radians(np.linspace(a0, a1, 40))]
    m = VMobject().set_points_as_corners(pts).set_stroke(color, w, op)
    return DashedVMobject(m, num_dashes=max(10, int(rx * 14)), dashed_ratio=0.6) if dashed else m


def edge(x, y0, y1, w=3.5):
    """Aresta física: núcleo claro com leve halo."""
    return VGroup(Line(P(x, y0), P(x, y1)).set_stroke(BLUE, 3 * w, 0.3), Line(P(x, y0), P(x, y1)).set_stroke(BLUE_L, w))


def sign_col(x, y0, y1, minus=False, s=0.06, color=WHITE, op=1.0, step=0.5, w=2.2):
    return VGroup(*[sign(P(x, y0 + step / 2 + step * k), minus, s=s, color=color, w=w) for k in range(int((y1 - y0) / step))]).set_opacity(op)


class Dimmer:
    """Holofote: escurece/restaura um grupo multiplicando as opacidades originais de cada parte (sem achatar as translúcidas)."""

    def __init__(self, m):
        self.m = m
        self.subs = list(m.family_members_with_points())
        self.o = [(s.get_fill_opacity(), s.get_stroke_opacity()) for s in self.subs]
        self.f = 1.0

    def to(self, f):
        f0, f1 = self.f, f
        self.f = f

        def upd(_, a):
            k = f0 + (f1 - f0) * a
            for s, (fo, so) in zip(self.subs, self.o):
                s.set_fill(opacity=fo * k, family=False)
                s.set_stroke(opacity=so * k, family=False)
        return UpdateFromAlphaFunc(self.m, upd)


def hollow(R, minus=False, metal=False, open_frac=0.8, y0=SRC0, y1=YW1, charge_inner=False):
    """Casca cilíndrica OCA (corte lateral): só a parede é material; o interior é fundo vazio (sem preenchimento), com rim de cima aberto
    e parede traseira discreta. Cargas só na parede (`charge_inner`: na superfície interna, como na casca externa do coaxial)."""
    ry = ery(R)
    wall_op, s_sz = (0.5, 0.08) if metal else (0.3, 0.07)
    g = VGroup(Ellipse(width=2 * R, height=2 * ry).move_to(P(AX, y1)).set_stroke(width=0).set_fill(BACKGROUND_COLOR, 0.95))
    g.add(arc(AX, y1, R, 0, 180, BLUE_L, 3, 0.45), arc(AX, y0, R, 0, 180, BLUE_L, 2.5, 0.2, dashed=True))
    for sg in (-1, 1):
        xi, xo = AX + sg * open_frac * R, AX + sg * R
        g.add(Polygon(P(xi, y0), P(xo, y0), P(xo, y1), P(xi, y1)).set_stroke(width=0).set_fill(BLUE_L if metal else BLUE, wall_op))
        g.add(edge(xo, y0, y1, 4 if metal else 3.5))
        if not metal:
            g.add(Line(P(xi, y0), P(xi, y1)).set_stroke(BLUE_L, 1.5, 0.5))
        g.add(sign_col(xi if charge_inner else (xi + xo) / 2, y0, y1, minus, s=s_sz, color=WHITE))
    g.add(arc(AX, y1, R, 180, 360, BLUE_L, 4, 1), arc(AX, y0, R, 180, 360, BLUE_L, 4, 1))
    return g.set_z_index(5)


def solid_body(R, metal=False, y0=SRC0, y1=YW1):
    """Cilindro cheio: faixas verticais com opacidade variável (sombreamento), face de cima clara, brilho especular.
    `metal`: condutor (mais opaco, brilho forte); sem metal: isolante translúcido (as cargas do volume vêm de lattice_dyn)."""
    ry = ery(R)
    base = BLUE_L if metal else BLUE
    ops = (0.28, 0.46, 0.58, 0.58, 0.46, 0.28) if metal else (0.14, 0.26, 0.36, 0.36, 0.26, 0.14)
    xs = np.linspace(-R, R, 7)
    g = VGroup(*[Polygon(P(AX + xs[i], y0), P(AX + xs[i + 1], y0), P(AX + xs[i + 1], y1), P(AX + xs[i], y1)).set_stroke(width=0).set_fill(base, ops[i])
                 for i in range(6)])
    g.add(Ellipse(width=2 * R, height=2 * ry).move_to(P(AX, y1)).set_stroke(BLUE_L, 3.5).set_fill(BLUE_L, 0.5 if metal else 0.3))
    g.add(arc(AX, y0, R, 180, 360, BLUE_L, 3.5, 1))
    g.add(edge(AX - R, y0, y1, 4 if metal else 3.5), edge(AX + R, y0, y1, 4 if metal else 3.5))
    g.add(Line(P(AX - 0.5 * R, y0 + 0.15), P(AX - 0.5 * R, y1 - 0.15)).set_stroke(WHITE, 3, 0.5 if metal else 0.16))
    if metal:
        g.add(Line(P(AX - 0.2 * R, y0 + 0.15), P(AX - 0.2 * R, y1 - 0.15)).set_stroke(WHITE, 2, 0.25))
    return g.set_z_index(4)


def lattice_dyn(gc, R=R_VIS):
    """Cargas do volume do isolante; as que estão dentro da gaussiana (carga envolvida) ficam violeta claro."""
    cols = (-0.5 * R, 0.0, 0.5 * R)
    rows = [SRC0 + 0.25 + 0.5 * k for k in range(int((YW1 - SRC0) / 0.5))]

    def build():
        r = gc.r()
        out = VGroup()
        for dx in cols:
            for y in rows:
                inside = abs(dx) <= r and YB <= y <= YT
                out.add(sign(P(AX + dx, y), s=0.06 if inside else 0.05, color=LAV if inside else BLUE_L, w=2.6 if inside else 2)
                        .set_opacity(1.0 if inside else 0.6))
        return out.set_z_index(5)
    return always_redraw(build)


def env_overlay(gc, R=R_VIS, top=None):
    """Região envolvida: seleção matemática (#745CFF translúcido, sem contorno) dentro da fonte."""
    def build():
        w = max(min(gc.r(), R), 0.02) if top is None else top(gc.r())
        return Polygon(P(AX - w, YB), P(AX + w, YB), P(AX + w, YT), P(AX - w, YT)).set_stroke(width=0).set_fill(DAVEC, 0.22).set_z_index(5.5)
    return always_redraw(build)


def top_dim(x_len, name, y=2.3, color=BLUE_L, drop=None, x0=None):
    """Cota de um raio físico (R, a, b) acima da fonte, ligada à parede por uma linha tracejada (`drop` = altura da borda)."""
    x0 = AX if x0 is None else x0
    g = VGroup(Line(P(x0, y), P(x0 + x_len, y)), Line(P(x0, y - 0.08), P(x0, y + 0.08)), Line(P(x0 + x_len, y - 0.08), P(x0 + x_len, y + 0.08))
               ).set_stroke(color, LW_DOT)
    if drop is not None:
        g.add(DashedLine(P(x0 + x_len, y - 0.08), P(x0 + x_len, drop), dash_length=0.08).set_stroke(color, LW_THIN, 0.6))
    return VGroup(g, eq(name, size=M_M, color=color).move_to(P(x0 + x_len / 2, y + 0.34)))


class GaussCyl:
    """Cilindro gaussiano coaxial (vista lateral, 2.5D) controlado por r: dashed violeta leve (nunca material), frente nítida e
    fundo discreto, preenchimento translúcido (lateral `lo`, tampas `co`), setas de E na lateral (comprimento = `efun`),
    cota de r e cota de L. `vis`, `dv` e `ao` controlam a visibilidade do conjunto, da cota de r e das setas."""

    def __init__(self, r0, efun):
        self.rt = ValueTracker(r0)
        self.efun = efun
        self.lo, self.co = ValueTracker(0.08), ValueTracker(0.05)
        self.vis, self.dv, self.ao = ValueTracker(1.0), ValueTracker(0.0), ValueTracker(1.0)
        self.geom = always_redraw(self._geom)
        self.arrows = always_redraw(self._arrows)
        self.dimr = always_redraw(self._dimr)
        self.lab = eq("r", size=M_M, color=VIOLET).move_to(P(AX + r0 / 2, YB - 1.4))
        self.lab.add_updater(lambda m: m.move_to(P(AX + self.r() / 2, YB - 1.4)).set_opacity(self.dv.get_value()))
        xl = -6.45
        self.diml = VGroup(Line(P(xl, YB), P(xl, YT)), Line(P(xl - 0.08, YB), P(xl + 0.08, YB)), Line(P(xl - 0.08, YT), P(xl + 0.08, YT)))
        self.diml.set_stroke(WHITE, LW_DOT)
        self.diml = VGroup(self.diml, eq("L", size=M_S).move_to(P(xl - 0.32, (YB + YT) / 2)))

    def r(self):
        return max(float(self.rt.get_value()), 0.03)

    def add_to(self, scene):
        scene.add(self.geom, self.arrows, self.dimr, self.lab)

    def _geom(self):
        r, f = self.r(), float(self.vis.get_value())
        parts = [Polygon(P(AX - r, YB), P(AX + r, YB), P(AX + r, YT), P(AX - r, YT)).set_stroke(width=0).set_fill(VIOLET, self.lo.get_value() * f)]
        for y, k in ((YT, 1.0), (YB, 0.6)):
            parts.append(Ellipse(width=2 * r, height=2 * ery(r)).move_to(P(AX, y)).set_stroke(width=0).set_fill(VIOLET, self.co.get_value() * f * k))
        for sg in (-1, 1):
            parts.append(DashedLine(P(AX + sg * r, YB), P(AX + sg * r, YT), dash_length=0.14, dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.95 * f))
        parts += [arc(AX, YT, r, 180, 360, VIOLET, 3.5, 0.95 * f, True), arc(AX, YT, r, 0, 180, VIOLET, 3, 0.4 * f, True),
                  arc(AX, YB, r, 180, 360, VIOLET, 3.5, 0.9 * f, True), arc(AX, YB, r, 0, 180, VIOLET, 3, 0.22 * f, True)]
        return VGroup(*parts).set_z_index(6)

    def _arrows(self):
        r, ln = self.r(), self.efun(self.r())
        op = float(self.vis.get_value() * self.ao.get_value())
        return VGroup(*[vec(P(AX + r, y), P(AX + r + ln, y), CYAN, LW_VEC, op=op, z=7) for y in YS_ARR])

    def _dimr(self):
        r, y = self.r(), YB - 1.1
        return VGroup(Line(P(AX, y), P(AX + r, y)), Line(P(AX, y - 0.08), P(AX, y + 0.08)),
                      Line(P(AX + r, y - 0.08), P(AX + r, y + 0.08))).set_stroke(VIOLET, LW_DOT, float(self.dv.get_value()))


# ── Simetria planar (N12–N15): fontes planas 2.5D e o pillbox ───────────────
XS = AX                           # x do plano (médio) das fontes planas
PR, CW = 0.85, 0.34               # pillbox: meia-altura das tampas e largura aparente (perspectiva)
PY0, PY1 = -2.2, 2.0              # extensão visível dos planos
SK = 0.28                         # inclinação das bordas horizontais (profundidade)
A_S = 0.9                         # meia-espessura do slab (a)
YS_P = (-0.6, 0.0, 0.6)           # alturas das setas de E nas tampas


def plane_body(x, w, minus=False, ncols=1, metal=False, hint=True):
    """Fonte plana 2.5D: paralelogramo vertical (largura 2w, borda superior/inferior inclinada = profundidade), faixas de luz,
    arestas físicas claras, cargas na superfície (ncols = 1) ou no volume (ncols > 1). `metal`: condutor, mais sólido."""
    ops = (0.28, 0.46, 0.58, 0.58, 0.46, 0.28) if metal else (0.14, 0.3, 0.3, 0.14)
    n = len(ops)
    g = VGroup()
    for i in range(n):
        f0, f1 = i / n, (i + 1) / n
        g.add(Polygon(P(x - w + 2 * w * f0, PY0 + SK * f0), P(x - w + 2 * w * f1, PY0 + SK * f1),
                      P(x - w + 2 * w * f1, PY1 - SK + SK * f1), P(x - w + 2 * w * f0, PY1 - SK + SK * f0))
              .set_stroke(width=0).set_fill(BLUE_L if metal else BLUE, ops[i]))
    g.add(edge(x - w, PY0, PY1 - SK, 3.5), edge(x + w, PY0 + SK, PY1, 3.5))
    g.add(DashedLine(P(x - w, PY1 - SK), P(x + w, PY1), dash_length=0.1).set_stroke(BLUE_L, 2.5, 0.5),
          DashedLine(P(x - w, PY0), P(x + w, PY0 + SK), dash_length=0.1).set_stroke(BLUE_L, 2.5, 0.5))
    if hint:   # continuação tracejada que se apaga: o plano não termina aqui
        for xx, yt in ((x - w, PY1 - SK), (x + w, PY1)):
            g.add(DashedLine(P(xx, yt), P(xx, yt + 0.42), dash_length=0.09).set_stroke(BLUE_L, 3, 0.3))
        for xx, yb in ((x - w, PY0), (x + w, PY0 + SK)):
            g.add(DashedLine(P(xx, yb), P(xx, yb - 0.42), dash_length=0.09).set_stroke(BLUE_L, 3, 0.3))
    if ncols > 0:
        for c in np.linspace(-0.65, 0.65, ncols) if ncols > 1 else [0.0]:
            for k in range(int((PY1 - PY0 - 0.6) / 0.5)):
                f = 0.5 + 0.5 * c
                g.add(sign(P(x + w * c, PY0 + 0.45 + 0.5 * k + SK * f), minus, s=0.06 if ncols == 1 else 0.055,
                           color=WHITE if ncols == 1 else BLUE_L, w=2.4 if ncols == 1 else 2.0))
    return g.set_z_index(5)


def patch_on(x, w, pr=PR, color=BLUE_L, op=0.55):
    """Trecho do plano (área A) que fica dentro do pillbox."""
    return Ellipse(width=2 * w + 0.06, height=2 * pr).move_to(P(x, 0.1)).set_stroke(color, 3).set_fill(color, op).set_z_index(5.5)


class Pill:
    """Pillbox gaussiano horizontal (eixo ao longo de x) controlado por d: tampas em xc ± d. Violeta leve (nunca material);
    traço contínuo = tampas que contribuem (`cs` → 1), tracejado = não contribuem. Setas de E nas tampas com comprimento ef(d)."""

    def __init__(self, d0, ef, xc=XS, pr=PR):
        self.dt = ValueTracker(d0)
        self.vis, self.cs, self.lo, self.ao = ValueTracker(1.0), ValueTracker(0.0), ValueTracker(0.09), ValueTracker(1.0)
        self.ef, self.xc, self.pr = ef, xc, pr
        self.geom = always_redraw(self._geom)
        self.arrows = always_redraw(self._arrows)

    def d(self):
        return max(abs(float(self.dt.get_value())), 0.04)

    def _geom(self):
        d, pr, xc = self.d(), self.pr, self.xc
        f, cs = float(self.vis.get_value()), float(self.cs.get_value())
        parts = [Polygon(P(xc - d, -pr), P(xc + d, -pr), P(xc + d, pr), P(xc - d, pr)).set_stroke(width=0).set_fill(VIOLET, self.lo.get_value() * f)]
        for sg in (-1, 1):
            c = P(xc + sg * d, 0)
            parts.append(Ellipse(width=CW, height=2 * pr).move_to(c).set_stroke(width=0).set_fill(VIOLET, (0.07 + 0.3 * cs) * f))
            parts.append(DashedVMobject(Ellipse(width=CW, height=2 * pr).move_to(c), num_dashes=36, dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.95 * (1 - cs) * f))
            parts.append(Ellipse(width=CW, height=2 * pr).move_to(c).set_stroke(VIOLET, 5, cs * f))
        for s2 in (-1, 1):
            parts.append(DashedLine(P(xc - d, s2 * pr), P(xc + d, s2 * pr), dash_length=0.14, dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.95 * f))
        return VGroup(*parts).set_z_index(6)

    def _arrows(self):
        d, ln, xc = self.d(), self.ef(self.d()), self.xc
        op = float(self.vis.get_value() * self.ao.get_value())
        return VGroup(*[vec(P(xc + sg * d, y), P(xc + sg * (d + ln), y), CYAN, LW_VEC, op=op, z=7) for sg in (-1, 1) for y in YS_P])

    def add_to(self, scene):
        scene.add(self.geom, self.arrows)


SW = 0.42                         # meia-espessura da folha (sem espessura física; só para ser visível)
SY0, SY1 = -1.85, 1.75            # extensão vertical da face frontal (corte transversal) da placa
SDX, SDY = 0.42, 0.24             # deslocamento da face traseira (profundidade do bloco)


def slab_box(x, a):
    """Placa volumétrica como bloco 2.5D: face frontal = corte perpendicular ao plano (faces em x = ±a), topo e lateral dão volume,
    face traseira discreta, continuação tracejada para baixo (extensão infinita). As cargas ficam em lattice_slab."""
    L, Rr = x - a, x + a
    back = Polygon(P(L + SDX, SY0 + SDY), P(Rr + SDX, SY0 + SDY), P(Rr + SDX, SY1 + SDY), P(L + SDX, SY1 + SDY)).set_stroke(BLUE_L, 1.5, 0.3).set_fill(BLUE, 0.05)
    side = Polygon(P(Rr, SY0), P(Rr + SDX, SY0 + SDY), P(Rr + SDX, SY1 + SDY), P(Rr, SY1)).set_stroke(width=0).set_fill(BLUE, 0.22)
    top = Polygon(P(L, SY1), P(Rr, SY1), P(Rr + SDX, SY1 + SDY), P(L + SDX, SY1 + SDY)).set_stroke(BLUE_L, 2, 0.6).set_fill(BLUE_L, 0.3)
    xs = np.linspace(L, Rr, 5)
    ops = (0.16, 0.3, 0.3, 0.16)
    front = VGroup(*[Polygon(P(xs[i], SY0), P(xs[i + 1], SY0), P(xs[i + 1], SY1), P(xs[i], SY1)).set_stroke(width=0).set_fill(BLUE, ops[i]) for i in range(4)])
    edges = VGroup(edge(L, SY0, SY1, 3.5), edge(Rr, SY0, SY1, 3.5), Line(P(L, SY1), P(Rr, SY1)).set_stroke(BLUE_L, 3), Line(P(L, SY0), P(Rr, SY0)).set_stroke(BLUE_L, 3),
                   Line(P(Rr, SY1), P(Rr + SDX, SY1 + SDY)).set_stroke(BLUE_L, 2, 0.6), Line(P(Rr, SY0), P(Rr + SDX, SY0 + SDY)).set_stroke(BLUE_L, 2, 0.4))
    hint = VGroup(*[DashedLine(P(xx, SY0), P(xx, SY0 - 0.32), dash_length=0.09).set_stroke(BLUE_L, 3, 0.3) for xx in (L, Rr)])
    return VGroup(back.set_z_index(4.0), side.set_z_index(4.2), top.set_z_index(4.4), front.set_z_index(4.6), edges.set_z_index(5), hint.set_z_index(5))


def lattice_slab(pill, a):
    """Cargas no volume da placa; as que estão dentro do pillbox (carga envolvida) ficam violeta claro."""
    cols_ = (-0.55 * a, 0.0, 0.55 * a)
    rows_ = [-1.5 + 0.5 * k for k in range(7)]

    def build():
        d = pill.d()
        out = VGroup()
        for cx in cols_:
            for y in rows_:
                inside = abs(cx) <= d and abs(y) <= PR
                out.add(sign(P(XS + cx, y), s=0.065 if inside else 0.055, color=LAV if inside else BLUE_L, w=2.8 if inside else 2.0).set_opacity(1.0 if inside else 0.65))
        return out.set_z_index(5.2)
    return always_redraw(build)


def env_slab(pill, a):
    """Fatia envolvida (largura exata min(|x|, a); nula no centro): seleção matemática, sem contorno."""
    def build():
        w = min(abs(float(pill.dt.get_value())), a)
        if w < 0.03:
            return VGroup()
        return Polygon(P(XS - w, -PR), P(XS + w, -PR), P(XS + w, PR), P(XS - w, PR)).set_stroke(width=0).set_fill(DAVEC, 0.26).set_z_index(5.5)
    return always_redraw(build)


def slab_cota(pill, a):
    w = min(abs(float(pill.dt.get_value())), a)
    if w < 0.03:
        return VGroup()
    y = -2.35
    return VGroup(Line(P(XS - w, y), P(XS + w, y)), Line(P(XS - w, y - 0.08), P(XS - w, y + 0.08)),
                  Line(P(XS + w, y - 0.08), P(XS + w, y + 0.08))).set_stroke(VIOLET, LW_DOT)


def slab_ruler(x, a):
    """Régua acima da placa: faces em x = −a e x = +a e o plano central x = 0."""
    y = 2.5
    g = VGroup(Line(P(x - a, y), P(x + a, y)).set_stroke(BLUE_L, LW_DOT, 0.9))
    for xx, name in ((x - a, "-a"), (x, "0"), (x + a, "a")):
        g.add(Line(P(xx, y - 0.09), P(xx, y + 0.09)).set_stroke(BLUE_L, LW_DOT, 0.9), eq(name, size=M_S, color=BLUE_L).move_to(P(xx, y + 0.38)))
    for xx in (x - a, x + a):
        g.add(DashedLine(P(xx, y - 0.1), P(xx, SY1 + SDY), dash_length=0.08).set_stroke(BLUE_L, 1.5, 0.45))
    g.add(eq("x", size=M_S).move_to(P(x + a + 0.55, y)))
    return g


def ef_slab(d):
    """Slab: ∝ |x| dentro, constante fora; nulo no centro (nada de campo não nulo desenhado em x = 0)."""
    return 0.0 if d < 0.07 else 1.4 * min(d / A_S, 1.0)


def ef_sheet(d):
    """Folha: E constante (não depende da distância)."""
    return 1.15


def pill_static(xl, xr, cs_l, cs_r, pr=PR, lo=0.09):
    """Pillbox com tampas em xl e xr (assimétrico: face de condutor); cs = 1 → tampa que contribui (traço contínuo)."""
    parts = [Polygon(P(xl, -pr), P(xr, -pr), P(xr, pr), P(xl, pr)).set_stroke(width=0).set_fill(VIOLET, lo)]
    for x, cs in ((xl, cs_l), (xr, cs_r)):
        c = P(x, 0)
        parts.append(Ellipse(width=CW, height=2 * pr).move_to(c).set_stroke(width=0).set_fill(VIOLET, 0.07 + 0.3 * cs))
        if cs < 0.5:
            parts.append(DashedVMobject(Ellipse(width=CW, height=2 * pr).move_to(c), num_dashes=36, dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.95))
        else:
            parts.append(Ellipse(width=CW, height=2 * pr).move_to(c).set_stroke(VIOLET, 5, 1))
    for s2 in (-1, 1):
        parts.append(DashedLine(P(xl, s2 * pr), P(xr, s2 * pr), dash_length=0.14, dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.95))
    return VGroup(*parts).set_z_index(6)


# ── Simetria esférica (N20–N23): fontes esféricas 2.5D e a esfera gaussiana ──
# Convenção congelada: R (ou a) = dimensão da fonte; r = raio da gaussiana (a mesma dos blocos cilíndrico e planar).
SCX, SCY = -3.3, -0.1
SC0 = P(SCX, SCY)
RS, BS = 1.2, 2.2                 # R (fonte; a no capacitor) e b (casca externa do capacitor)


def sarc(R, a0, a1, color, w, op=1.0, dashed=False):
    """Arco do 'equador' de uma esfera (perspectiva leve): 180–360 = frente, 0–180 = trás."""
    return arc(SCX, SCY, R, a0, a1, color, w, op, dashed)


def sph_hint(R, color=BLUE_L, op=0.55):
    return VGroup(sarc(R, 180, 360, color, 2.5, op), sarc(R, 0, 180, color, 2, op * 0.45, True))


def sph_shell(R=RS, minus=False, inner=False, metal=False):
    """Casca esférica fina e OCA (corte): parede estreita, interior vazio (fundo), cargas só na parede
    (`inner`: na superfície interna, como na casca externa do capacitor). `metal`: mais sólida."""
    ring = Annulus(inner_radius=0.9 * R, outer_radius=R, arc_center=SC0).set_stroke(width=0).set_fill(BLUE_L if metal else BLUE, 0.5 if metal else 0.3)
    outer = Circle(radius=R, arc_center=SC0).set_stroke(BLUE_L, 4)
    halo = Circle(radius=R, arc_center=SC0).set_stroke(BLUE, 12, 0.3)
    inn = Circle(radius=0.9 * R, arc_center=SC0).set_stroke(BLUE_L, 1.5, 0.5)
    sg = VGroup(*[sign(SC0 + (0.9 * R if inner else 0.95 * R) * U(a), minus, s=0.07 if metal else 0.06, color=WHITE) for a in range(0, 360, 30)])
    return (VGroup(halo, ring, outer, sg) if metal else VGroup(halo, ring, inn, outer, sph_hint(R), sg)).set_z_index(5)


def sph_solid(R=RS, metal=False):
    """Esfera cheia: discos concentres translúcidos (sombreamento), contorno claro, brilho especular. `metal`: condutor, mais opaco."""
    base = BLUE_L if metal else BLUE
    op = 0.2 if metal else 0.12
    disks = VGroup(*[Circle(radius=R * k, arc_center=SC0).set_stroke(width=0).set_fill(base, op) for k in (1.0, 0.78, 0.56, 0.34)])
    out = Circle(radius=R, arc_center=SC0).set_stroke(BLUE_L, 4)
    halo = Circle(radius=R, arc_center=SC0).set_stroke(BLUE, 12, 0.3)
    hl = Ellipse(width=0.5 * R, height=0.26 * R).rotate(0.6).move_to(SC0 + R * P(-0.45, 0.5)).set_stroke(width=0).set_fill(WHITE, 0.45 if metal else 0.22)
    return VGroup(halo, disks, out, hl, sph_hint(R)).set_z_index(4)


def lattice_sph(gs, R=RS):
    """Cargas no volume da esfera isolante; as que estão dentro da gaussiana (carga envolvida) ficam violeta claro."""
    pts = [P(x * R, y * R) for x in np.arange(-0.75, 0.76, 0.375) for y in np.arange(-0.75, 0.76, 0.375) if math.hypot(x, y) <= 0.8]

    def build():
        r = gs.r()
        out = VGroup()
        for p in pts:
            inside = float(np.linalg.norm(p)) <= r
            out.add(sign(SC0 + p, s=0.06 if inside else 0.05, color=LAV if inside else BLUE_L, w=2.6 if inside else 2).set_opacity(1.0 if inside else 0.6))
        return out.set_z_index(5)
    return always_redraw(build)


def env_sph(gs, R=RS, top=None):
    """Região envolvida: seleção matemática (#745CFF translúcido, sem contorno) dentro da fonte."""
    def build():
        w = max(min(gs.r(), R), 0.02) if top is None else top(gs.r())
        return Circle(radius=w, arc_center=SC0).set_stroke(width=0).set_fill(DAVEC, 0.24).set_z_index(5.5)
    return always_redraw(build)


def rad_dim(R, name, angle, color=BLUE_L, frac=0.55):
    """Cota de um raio físico (R, a, b): raio tracejado do centro à superfície, com o rótulo ao lado."""
    d = U(angle)
    perp = P(-d[1], d[0])
    return VGroup(DashedLine(SC0, SC0 + R * d, dash_length=0.08).set_stroke(color, LW_THIN + 0.5, 0.85),
                  Circle(radius=0.045, arc_center=SC0).set_stroke(color, 2).set_fill(color, 1),
                  eq(name, size=M_M, color=color).move_to(SC0 + frac * R * d + 0.3 * perp))


def ef_shell(r):
    """Casca esférica: nulo por dentro; 1/r² por fora."""
    return min(1.4 * (RS / r) ** 2, 1.3) if r > RS else 0.0


def ef_ssolid(r):
    """Esfera maciça uniforme: ∝ r por dentro, ∝ 1/r² por fora (contínuo em R)."""
    u = r / RS
    return 1.3 * (u if u <= 1 else 1 / u ** 2)


def ef_scoax(r):
    """Capacitor esférico: campo só no vão, ∝ 1/r²."""
    return min(1.4 * (RS / r) ** 2, 1.3) if RS < r < BS else 0.0


class GaussSph:
    """Esfera gaussiana concêntrica (corte 2.5D) controlada por r: tracejada violeta leve (nunca material), 'equador' em perspectiva,
    preenchimento translúcido, 8 setas radiais de E (comprimento = `efun`) e cota de r. `gv`, `ao` e `dv`: geometria, setas e cota."""

    def __init__(self, r0, efun):
        self.rt = ValueTracker(r0)
        self.efun = efun
        self.gv, self.ao, self.dv, self.lo = ValueTracker(1.0), ValueTracker(1.0), ValueTracker(0.0), ValueTracker(0.08)
        self.geom = always_redraw(self._geom)
        self.arrows = always_redraw(self._arrows)
        self.dimr = always_redraw(self._dimr)
        self.lab = eq("r", size=M_M, color=VIOLET)
        self.lab.add_updater(lambda m: m.move_to(SC0 + 0.5 * self.r() * U(-22.5) + 0.3 * U(-112.5)).set_opacity(self.dv.get_value()))

    def r(self):
        return max(float(self.rt.get_value()), 0.03)

    def add_to(self, scene):
        scene.add(self.geom, self.arrows, self.dimr, self.lab)

    def _geom(self):
        r, f = self.r(), float(self.gv.get_value())
        return VGroup(Circle(radius=r, arc_center=SC0).set_stroke(width=0).set_fill(VIOLET, self.lo.get_value() * f),
                      DashedVMobject(Circle(radius=r, arc_center=SC0), num_dashes=max(24, int(r * 30)), dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.95 * f),
                      sarc(r, 180, 360, VIOLET, 3, 0.7 * f, True), sarc(r, 0, 180, VIOLET, 2.5, 0.3 * f, True)).set_z_index(6)

    def _arrows(self):
        r, ln = self.r(), self.efun(self.r())
        op = float(self.ao.get_value())
        return VGroup(*[vec(SC0 + r * U(a), SC0 + (r + ln) * U(a), CYAN, LW_VEC, op=op, z=7) for a in range(0, 360, 45)])

    def _dimr(self):
        r = self.r()
        d = U(-22.5)
        return VGroup(DashedLine(SC0, SC0 + r * d, dash_length=0.08)).set_stroke(VIOLET, LW_DOT, float(self.dv.get_value()))


# ── Cena ────────────────────────────────────────────────────────────────────
class LeiGaussCasosClassicos002(Scene):

    def setup(self):
        self.camera.background_color = BACKGROUND_COLOR
        # relógio: T = tempo do vídeo (quadros exatos); shift = esperas já pedidas à voz; trecho corrente: chave "bloco.i", início e durações desenhadas
        self.T, self.shift, self.pads, self.blocos = 0.0, 0.0, [], {}
        self.k, self.si, self.seg, self.s0, self.base_a, self.base_w, self.na_at, self.ritmo = 0, 0, "0.0", 0.0, 0.0, 0.0, False, {}

    @staticmethod
    def _curto(m):
        return m.width > 0 and m.width <= 10.0 and m.height <= 1.35

    @staticmethod
    def _sobrepoe(a, b):
        iw = min(a.get_right()[0], b.get_right()[0]) - max(a.get_left()[0], b.get_left()[0])
        ih = min(a.get_top()[1], b.get_top()[1]) - max(a.get_bottom()[1], b.get_bottom()[1])
        if iw <= 0 or ih <= 0:
            return False
        return iw * ih > 0.2 * min(a.width * a.height, b.width * b.height)

    def _choque(self, a, b):
        """Uma linha curta de texto/fórmula que entra sobre outra (ou sobre uma linha de um grupo que sai): não podem coexistir."""
        if a is b or not self._curto(b):
            return False
        cands = [a] if self._curto(a) else [c for c in a.submobjects if self._curto(c)]
        return any(c is not b and self._sobrepoe(c, b) for c in cands)

    def play(self, *args, **kwargs):
        """Textos que se trocam no mesmo lugar: a saída vem antes da entrada (nunca duas leituras juntas)."""
        anims = self.compile_animations(*args, **kwargs)
        outs = [x for x in anims if isinstance(x, FadeOut)]
        ins = [x for x in anims if isinstance(x, FadeIn)]
        conf = [o for o in outs if any(self._choque(o.mobject, i.mobject) for i in ins)]
        if conf:
            for c in conf:
                c.run_time = 0.45
            self._tocar(conf)
            anims = [x for x in anims if all(x is not c for c in conf)]
            if not anims:
                return None
        return self._tocar(anims)

    def _tocar(self, anims):
        """Duração em quadros inteiros (mesma regra do yt_0001), para os marcos editoriais não derivarem."""
        fps = config.frame_rate
        static = False
        if len(anims) == 1 and isinstance(anims[0], Wait):
            self.animations = anims
            static = not self.should_update_mobjects()
        espera = isinstance(anims[0], Wait)
        m = max(a.run_time for a in anims)
        rt = m
        if VOZ and not self.na_at:
            fa, fw = RITMO.get(self.seg, (1.0, 1.0))
            if espera:
                self.base_w += m
            else:
                self.base_a += m
            rt = m * (fw if espera else fa)
        n = max(1, int(round(rt * fps)))
        real = (n + 0.25) / fps if static else (n - 0.5) / fps
        for a in anims:
            a.run_time = real * a.run_time / m
        self.T += n / fps
        return super().play(*anims)

    def _espera(self, tv, d):
        self.pads.append([round(tv, 3), round(d, 3)])
        self.shift += d

    def respiro(self, tv, d):
        """Pausa deliberada na voz antes do instante tv da fala (sem atraso de animação)."""
        self._espera(tv, d)

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

    def at(self, t):
        """Marco editorial t (s do orçamento de 18:01): espera, ou pede espera à voz, até o instante da fala correspondente."""
        if not VOZ:
            d = t - self.T
            if d > 0.03:
                self.wait(d)
            return
        tv = voz(t)
        alvo = tv + self.shift
        self._ajusta(alvo - self.s0)
        d = alvo - self.T
        if d > 0.5 / config.frame_rate:
            self.update_mobjects(0)                     # Scene.wait congela o quadro sem updaters dependentes do tempo
            self.na_at = True
            self.wait(d)
            self.na_at = False
        elif d < -TOL:
            self._espera(tv, -d)                        # a voz espera a animação neste ponto
        self.si += 1
        self.seg, self.s0, self.base_a, self.base_w = f"{self.k}.{self.si}", self.T, 0.0, 0.0

    def begin(self, k, name):
        self.next_section(f"{k:02d}_{name}", skip_animations=bool(SO) and k not in SO)
        self.k, self.si = k, 0
        self.seg, self.s0, self.base_a, self.base_w = f"{k}.0", self.T, 0.0, 0.0
        self.blocos[k] = round(self.T, 3)
        if VOZ:
            print(f"bloco {k:02d} {name}: início no vídeo {self.T:7.2f}s (esperas pedidas à voz até aqui: {self.shift:5.1f}s)")

    def construct(self):
        if GUIAS:
            self.add(safe_guides())
        self.n01_cold_open()
        self.n02_intro()
        self.n03_recap_algoritmo()
        self.n04_linha_simetria()
        self.n05_lateral_tampas()
        self.n06_carga_resultado()
        self.n07_casca()
        self.n08_macico()
        self.n09_grafico()
        self.n10_coaxial()
        self.n11_ponte()
        self.n12_folha()
        self.n13_slab()
        self.n14_duas()
        self.n15_condutor()
        self.n20_casca_esf()
        self.n21_regioes()
        self.n22_macico_esf()
        self.n23_capacitor_esf()
        self.n24_tres_cap()
        self.n25_areas()
        self.n26_checklist()
        self.n27_payoff_outro()
        if VOZ:
            if AJUSTAR:
                RITMO_ARQ.write_text(json.dumps(self.ritmo, indent=0), encoding="utf-8")
                print(f"ritmo.json: {len(self.ritmo)} trechos comprimidos")
            (PASTA / "pads.json").write_text(json.dumps({"fps": config.frame_rate, "pads": self.pads}, indent=0), encoding="utf-8")
            self.blocos["fim"] = round(self.T, 3)
            (PASTA / "blocos.json").write_text(json.dumps(self.blocos, indent=0), encoding="utf-8")
            print(f"duração total: {self.T:.2f}s · esperas pedidas à voz: {len(self.pads)} (+{self.shift:.2f}s)")

    # ═══ N01 · cold open (0:00–0:22) · FOCUS → COMPARE · sem marca, header nem watermark ═══
    def n01_cold_open(self):
        self.begin(1, "cold_open")
        CY = 0.85
        XL, XM, XR = -4.8, 0.0, 4.8
        line, sph, pl = co_line(XM, CY), co_sphere(XM, CY), co_plates(XR, CY)
        # FOCUS: a primeira fonte nasce no centro, grande; as outras entram e a linha abre espaço (COMPARE)
        self.play(Create(line.src), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(a, shift=0.05 * RIGHT) for a in line.fld], lag_ratio=0.1), run_time=1.0)
        self.at(2.0)
        self.play(VGroup(line.src, line.fld).animate.shift(XL * RIGHT), FadeIn(sph.src, scale=0.9), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(a) for a in sph.fld], lag_ratio=0.08), run_time=0.9)
        self.at(3.6)
        self.play(FadeIn(pl.src, shift=0.1 * UP), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(a) for a in pl.fld], lag_ratio=0.08), run_time=0.8)
        # perfis qualitativos: um de cada vez, com a fala "um cai… outro cai ainda mais rápido… outro nem diminui"
        lab_l = eq("E", r"\propto 1/r", size=M_M, colors={0: CYAN}).move_to(P(XL, -1.45))
        lab_s = eq("E", r"\propto 1/r^{2}", size=M_M, colors={0: CYAN}).move_to(P(XM, -1.45))
        lab_p = eq("E", r"=\text{constante}", size=M_M, colors={0: CYAN}).move_to(P(XR, -1.45))
        sub_l = label("ao redor da linha").move_to(P(XL, -1.98))
        sub_s = label("fora da esfera").move_to(P(XM, -1.98))
        sub_p = label("no vão entre as placas").move_to(P(XR, -1.98))
        self.at(7.4)
        self.play(FadeIn(lab_l, shift=0.1 * UP), FadeIn(sub_l), Indicate(line.fld, color=CYAN, scale_factor=1.06), run_time=1.2)
        self.at(10.2)
        self.play(FadeIn(lab_s, shift=0.1 * UP), FadeIn(sub_s), Indicate(sph.fld, color=CYAN, scale_factor=1.08), run_time=1.2)
        self.at(13.0)
        self.play(FadeIn(lab_p, shift=0.1 * UP), FadeIn(sub_p), Indicate(pl.fld, color=CYAN, scale_factor=1.06), run_time=1.2)
        # a mesma lei: um traço único liga os três casos
        self.at(14.9)
        div = VGroup(Line(P(-6.3, -2.5), P(-1.2, -2.5)), label("mesma lei", op=0.9).move_to(P(0, -2.5)),
                     Line(P(1.2, -2.5), P(6.3, -2.5))).set_stroke(WHITE, LW_THIN, 0.4)
        self.play(FadeIn(div), Indicate(VGroup(line.src, sph.src, pl.src), color=WHITE, scale_factor=1.04), run_time=1.3)
        # a pergunta (continua aberta)
        self.at(17.0)
        ask = title("O QUE MUDA?").move_to(P(0, -2.2))
        c1 = body("a fórmula")
        c2 = body("a superfície escolhida")
        c3 = body("a carga que ficou dentro dela")
        sep = [body("·", op=0.7) for _ in range(2)]
        chips = hchain(c1, sep[0], c2, sep[1], c3, buff=0.32).move_to(P(0, -2.75))
        self.play(FadeOut(div), FadeOut(VGroup(sub_l, sub_s, sub_p)), FadeIn(ask, shift=0.1 * UP), run_time=0.9)
        self.at(18.6)
        self.play(FadeIn(c1), run_time=0.7)
        self.at(19.9)
        self.play(FadeIn(sep[0]), FadeIn(c2), run_time=0.7)
        self.at(21.2)
        self.play(FadeIn(sep[1]), FadeIn(c3), run_time=0.7)
        self.ctx = VGroup(line.src, line.fld, sph.src, sph.fld, pl.src, pl.fld, lab_l, lab_s, lab_p)
        self.question = VGroup(ask, chips)
        self.src_groups = [VGroup(line.src, line.fld), VGroup(sph.src, sph.fld), VGroup(pl.src, pl.fld)]

    # ═══ N02 · intro humana (0:22–0:36) · FOCUS · mesmo sistema do yt_0001 (valores herdados, não mudam) ═══
    def n02_intro(self):
        self.begin(2, "intro")
        ctx, orig = self.ctx, self.ctx.copy()
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(WM_W).set_opacity(WM_OP).to_corner(UR, buff=0.3)
        self.tag = text(HEADER, 18, opacity=0.6).to_corner(UL, buff=0.38)
        brand = text("PARALLAX LAB", 22, opacity=0.8).move_to(P(0, 2.05))
        brand_title = display("LEI DE GAUSS", 58, bold=True).move_to(P(0, 1.25))
        sub = text("Três simetrias, um método", 26, opacity=0.85).move_to(P(0, 0.45))
        self.at(T_N02)
        # os três casos do cold open encolhem no lugar (mesmos objetos) e abrem espaço para a marca
        self.play(ctx.animate.scale(0.5, about_point=ORIGIN).move_to(P(0, -1.6)).set_opacity(0.3),
                  FadeOut(self.question), run_time=1.2)
        self.play(FadeIn(brand, shift=0.1 * DOWN), FadeIn(brand_title, shift=0.15 * DOWN), FadeIn(sub), FadeIn(self.wm),
                  run_time=1.0)
        self.at(29.5)
        self.play(FadeOut(VGroup(brand, brand_title, sub)), FadeIn(self.tag), run_time=0.7)
        self.play(Transform(ctx, orig), run_time=1.0)
        self.remove(ctx)
        self.add(*ctx)
        # "os casos clássicos": linha, esfera, placas, um de cada vez
        for t, g in zip((31.0, 32.2, 33.4), self.src_groups):
            self.at(t)
            self.play(Indicate(g, color=WHITE, scale_factor=1.05), run_time=1.0)

    # ═══ N03 · recapitulação e algoritmo (0:36–1:17) · FOCUS → BUILD ═══
    def n03_recap_algoritmo(self):
        self.begin(3, "recap_algoritmo")
        SC = P(-4.0, -0.95)
        self.at(35.3)
        self.play(FadeOut(*self.ctx, shift=0.5 * DOWN), run_time=0.7)
        self.at(T_N03)
        # Gauss vale sempre: P0 e uma superfície fechada qualquer com carga dentro
        p0 = eq(r"\oint_S", r"\vec E", r"\cdot", r"d\vec A", "=", r"\frac{Q_{\mathrm{env}}}{\varepsilon_0}", size=M_L,
                colors={1: CYAN, 3: DAVEC}).move_to(P(0, 1.9))
        p0_box = box(p0)
        surf = gauss_surface(SC, 1.2, blob_a)
        s_lab = eq("S", size=M_S, color=VIOLET).move_to(SC + P(-1.35, 1.2))
        qin = VGroup(q_dot(SC + P(-0.3, 0.15)), q_dot(SC + P(0.3, -0.2)))
        self.play(FadeIn(surf, shift=0.3 * UP), FadeIn(qin, shift=0.3 * UP), FadeIn(s_lab), run_time=0.9)
        self.at(37.7)
        self.play(FadeIn(p0, shift=0.1 * DOWN), run_time=1.2)
        self.at(39.4)
        env_lab = col(hchain(eq(r"\leftarrow", size=M_S), label("carga envolvida"), buff=0.14), 1.9, dx=2.6)
        self.play(Create(p0_box), FadeIn(env_lab), Indicate(qin, color=BLUE_L, scale_factor=1.25),
                  Indicate(p0[5], color=WHITE, scale_factor=1.1), run_time=1.3)
        # sempre vale: qualquer superfície fechada que envolva as mesmas cargas
        self.at(41.0)
        any_s = body("vale para qualquer superfície fechada", op=0.9).move_to(P(0, 0.55))
        self.play(FadeIn(any_s), Transform(surf, gauss_surface(SC, 1.2, blob_b)), run_time=1.4)

        # a carga externa fica fora de S, mas cria campo local sobre S
        self.at(42.6)
        qx = P(-1.1, -0.95)
        ext = q_dot(qx)
        ext_lab = label("carga externa").move_to(qx + P(0, -0.5))
        r_q = col(eq(r"Q_{\mathrm{env}}=0", size=M_M), 0.45)
        r_q_aux = col(mix("a carga externa não entra em ", eq(r"Q_{\mathrm{env}}", size=M_S, color=BLUE_L), size=T_NOTE, op=0.92), -0.15)
        n_cf = col(note("mas ela ainda cria campo sobre S", CYAN), -0.62)
        self.play(FadeOut(qin), FadeIn(ext), FadeIn(ext_lab), FadeOut(env_lab), FadeOut(any_s), run_time=1.0)
        self.play(FadeIn(r_q, shift=0.1 * UP), FadeIn(r_q_aux), run_time=1.0)
        self.at(44.6)
        # amostras de E⃗ sobre S (campo da carga externa): entram à direita, saem à esquerda
        samples = []
        for a in range(0, 360, 30):
            p = SC + 1.2 * blob_b(a) * U(a)
            d = p - qx
            m = np.linalg.norm(d)
            samples.append(vec(p, p + float(np.clip(1.9 / m ** 2, 0.4, 0.95)) * d / m, CYAN, LW_VEC, z=7))
        arrows = VGroup(*samples)
        lab_in = label("entra  −").move_to(SC + P(1.7, -1.5))
        lab_out = label("sai  +").move_to(SC + P(-1.9, -1.5))
        self.play(LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.1), FadeIn(n_cf, shift=0.1 * UP), run_time=1.6)
        self.play(FadeIn(lab_in), FadeIn(lab_out), run_time=0.8)
        self.at(47.0)
        r_phi = col(eq(r"\Phi_E", "=", "0", size=M_M), -1.05)
        self.play(FadeIn(r_phi, shift=0.1 * UP), run_time=1.0)
        # fluxo zero não garante campo zero: os vetores continuam lá
        self.at(48.6)
        r_phi2 = col(eq(r"\Phi_E", "=", "0", r"\;\nRightarrow\;", r"\vec E", "=", r"\vec 0", size=M_M, colors={4: CYAN}), -1.05)
        self.play(TransformMatchingTex(r_phi, r_phi2), Indicate(arrows, color=CYAN, scale_factor=1.12), run_time=1.5)

        # Gauss sempre vale; para obter E diretamente, simetria que simplifique o fluxo.
        # A superfície e a equação ficam; só a demonstração da carga externa dá lugar à conclusão.
        self.at(50.8)
        self.play(FadeOut(VGroup(ext, ext_lab, arrows, lab_in, lab_out, r_q, r_q_aux, r_phi2, n_cf)), run_time=0.8)
        st1 = col(body("a Lei de Gauss vale sempre", op=0.9), 0.55)
        st2 = col(hchain(body("para obter"), eq("E", size=M_S, color=CYAN), body("diretamente:"), buff=0.2), -0.2)
        st3 = col(title("simetria que"), -0.95)
        st4 = col(title("simplifique o fluxo"), -1.55)
        self.play(FadeIn(st1, shift=0.1 * UP), run_time=0.8)
        self.at(51.8)
        self.play(FadeIn(st2, shift=0.1 * UP), run_time=0.9)
        self.at(53.0)
        self.play(FadeIn(st3, shift=0.1 * UP), FadeIn(st4, shift=0.1 * UP), run_time=1.1)

        # a moldura transparente: a própria S vira a moldura em volta de uma fonte qualquer
        self.at(55.6)
        frame = gauss_surface(SC, 1.5, circ)
        src_pts = np.array([SC + P(-0.05, 0.05) + (0.8 + 0.2 * math.sin(2 * math.radians(a) + 0.5)
                                                    + 0.12 * math.cos(3 * math.radians(a))) * U(a) for a in np.linspace(0, 360, 12, endpoint=False)])
        source = smooth_closed(src_pts, BLUE_L, BLUE, w=LW_SRC).set_z_index(4)
        charges = VGroup(q_dot(SC + P(-0.3, 0.2)), q_dot(SC + P(0.25, -0.15)), q_dot(SC + P(-0.1, -0.35)))
        lab_src = col(VGroup(body("fonte física", BLUE_L), label("as cargas reais")).arrange(DOWN, aligned_edge=LEFT, buff=0.1), 1.0, dx=0.5)
        lab_g = col(VGroup(body("superfície gaussiana", VIOLET), label("construção matemática")).arrange(DOWN, aligned_edge=LEFT, buff=0.1), -0.1, dx=0.5)
        lead_s = Line(SC + P(0.95, 0.3), P(RL + 0.35, 1.05)).set_stroke(BLUE_L, LW_THIN, 0.5)
        lead_g = Line(SC + P(1.5, 0.0), P(RL + 0.35, -0.05)).set_stroke(VIOLET, LW_THIN, 0.5)
        self.play(FadeOut(VGroup(p0, p0_box, s_lab, st1, st2, st3, st4)), Transform(surf, frame), FadeIn(source), FadeIn(charges),
                  run_time=1.2)
        self.play(FadeIn(lab_src, shift=0.1 * UP), Create(lead_s), run_time=0.9)
        n1 = col(body("não altera as cargas"), -1.25, dx=0.5)
        n2 = col(body("não cria simetria"), -1.85, dx=0.5)
        self.at(57.6)
        self.play(FadeIn(lab_g, shift=0.1 * UP), Create(lead_g), run_time=0.9)
        self.at(58.9)
        self.play(surf.animate.scale(1.18, about_point=SC), FadeIn(n1, shift=0.1 * UP), run_time=0.8)
        self.play(surf.animate.scale(1 / 1.18, about_point=SC), run_time=0.8)
        self.at(60.8)
        self.play(FadeIn(n2, shift=0.1 * UP), run_time=0.8)

        # algoritmo: a mesma cena encolhe e vai para baixo; as etapas entram em cima, uma por vez, em duas linhas
        self.at(62.3)
        scene = VGroup(surf, source, charges)
        self.play(FadeOut(VGroup(lab_src, lab_g, n1, n2, lead_s, lead_g)),
                  scene.animate.scale(0.62, about_point=SC).move_to(P(0, -1.65)), run_time=0.8)
        s_fonte = title("fonte", BLUE_L)
        s_sim = title("simetria")
        s_dir = hchain(title("direção/dependência de", CYAN), eq("E", size=M_M, color=CYAN), buff=0.14)
        s_sup = title("superfície gaussiana", VIOLET)
        s_flx = title("fluxo")
        s_q = eq(r"Q_{\mathrm{env}}", size=M_M, color=BLUE_L)
        s_e = eq("E", size=M_M, color=CYAN)
        a1, a2, a3, a4, a5 = (eq(r"\rightarrow", size=M_S) for _ in range(5))
        line1 = [s_fonte, a1, s_sim, a2, s_dir]
        line2 = [s_sup, a3, s_flx, a4, s_q, a5, s_e]
        Y1, Y2 = 1.85, 0.75

        def centros(items, y):
            g = VGroup(*[m.copy() for m in items]).arrange(RIGHT, buff=0.3).move_to(P(0, y))
            return [m.get_center() for m in g]

        def conector():
            xa, xb = s_dir.get_right()[0], s_sup.get_left()[0]
            yb1, yt2 = s_dir.get_bottom()[1] - 0.12, s_sup.get_top()[1] + 0.08
            ymid = (yb1 + yt2) / 2
            return VGroup(Line(P(xa - 0.1, yb1), P(xa - 0.1, ymid)), Line(P(xa - 0.1, ymid), P(xb + 0.3, ymid)),
                          vec(P(xb + 0.3, ymid), P(xb + 0.3, yt2), WHITE, LW_THIN)).set_stroke(WHITE, LW_THIN, 0.7)

        def passo(linha, vis, n_novos, y):
            """Recentraliza a linha com os novos itens; os antigos deslizam e passam à hierarquia secundária."""
            alvo = centros(linha[:vis], y)
            antigos, novos = linha[:vis - n_novos], linha[vis - n_novos:vis]
            for m, c in zip(novos, alvo[len(antigos):]):
                m.move_to(c)
            return [m.animate.move_to(c).set_opacity(OP_PREV) for m, c in zip(antigos, alvo)], novos

        conn = None
        # (linha, nº de itens visíveis, nº de itens novos, y, referência na cena pequena)
        steps = [(line1, 1, 1, Y1, source), (line1, 3, 2, Y1, None), (line1, 5, 2, Y1, None), (line2, 1, 1, Y2, surf),
                 (line2, 3, 2, Y2, None), (line2, 5, 2, Y2, charges), (line2, 7, 2, Y2, None)]
        stamps = [62.9, 64.1, 65.5, 67.2, 68.8, 70.2, 71.6]
        shown = []
        for (linha, vis, n_novos, y, ref), t in zip(steps, stamps):
            self.at(t)
            moves, novos = passo(linha, vis, n_novos, y)
            fades = [m.animate.set_opacity(OP_PREV) for m in shown if m is not conn and all(m is not x for x in linha)]
            if linha is line2 and conn is None:
                conn = always_redraw(conector)
                self.add(conn)
                shown.append(conn)
            extra = [Indicate(ref, color=VIOLET if ref is surf else BLUE_L, scale_factor=1.06)] if ref is not None else []
            self.play(*[FadeIn(m, shift=0.1 * RIGHT) for m in novos], *moves, *fades, *extra, run_time=0.9)
            shown.extend(novos)
        # leitura do algoritmo completo (~3 s)
        self.at(72.6)
        self.play(*[m.animate.set_opacity(1.0) for m in shown if m is not conn], run_time=0.5)
        conn.clear_updaters()
        algo = VGroup(*shown)

        # N03 → N04: família cilíndrica; a linha nasce no lado esquerdo do SPLIT
        self.at(75.5)
        self.fam = label("SIMETRIA CILÍNDRICA").move_to(P(AX, 2.4))
        self.wire = wire_line()
        self.play(FadeOut(algo), FadeOut(scene), run_time=0.7)
        self.play(FadeIn(self.wire), FadeIn(self.fam), run_time=0.8)
        self.at(T_N04)

    # ═══ N04 · linha infinita: reconhecer a simetria (1:17–2:03) · SPLIT ═══
    def n04_linha_simetria(self):
        self.begin(4, "linha_simetria")
        self.at(T_N04)
        R4 = 1.55                             # distância de observação (demonstração ampliada)
        P4 = P(AX + R4, 0.0)
        self.p4 = P4
        C3 = P(4.4, -0.85)                    # vista de cima (seção transversal), na coluna da direita
        # a linha é um filamento 1D infinito: extensão tracejada que some nas pontas
        ext = VGroup(*[DashedLine(P(AX, a), P(AX, b), dash_length=0.1).set_stroke(BLUE_L, LW_SRC - 0.5, op)
                       for a, b, op in ((YW1, 2.4, 0.6), (2.4, 2.8, 0.3), (YW0, -2.55, 0.6), (-2.55, -2.9, 0.3))])
        inf_lab = label("linha infinita").move_to(P(AX + 1.1, 2.5))
        self.play(FadeOut(self.fam), Create(ext), FadeIn(inf_lab), run_time=1.1)
        # λ: a mesma carga por comprimento em todo lugar (a chave desliza ao longo da linha)
        self.at(79.0)
        brace = Brace(Line(P(AX, -0.5), P(AX, 0.5)), direction=LEFT, buff=0.12, color=BLUE_L)
        lam = eq(r"\lambda", size=M_M, color=BLUE_L).next_to(brace, LEFT, buff=0.12)
        bg = VGroup(brace, lam)
        lam_def = col(eq(r"\lambda", r"=\frac{\text{carga}}{\text{comprimento}}", size=M_L, colors={0: BLUE_L}), Y_ACT)
        self.play(FadeIn(bg, shift=0.1 * RIGHT), FadeIn(lam_def, shift=0.1 * DOWN), run_time=1.1)
        self.at(81.5)
        self.play(bg.animate.shift(1.3 * UP), run_time=1.3)
        self.play(bg.animate.shift(2.6 * DOWN), run_time=1.8)
        self.at(85.8)
        self.play(bg.animate.shift(1.3 * UP), run_time=1.0)

        # andar ao longo do eixo (janela deslizante na vista lateral) e, ao lado, a vista de cima
        self.at(88.0)
        pdot = Circle(radius=0.1, arc_center=P4).set_stroke(WHITE, 0).set_fill(WHITE, 1).set_z_index(8)
        rline = DashedLine(P(AX, 0.0), P4, dash_length=0.1).set_stroke(WHITE, LW_THIN + 0.5, 0.75)
        rlab = eq("r", size=M_M, color=VIOLET).move_to(P(AX + R4 / 2, 0.32))
        win = DashedVMobject(Polygon(P(AX - 0.55, -0.95), P(AX + R4 + 0.45, -0.95), P(AX + R4 + 0.45, 0.95), P(AX - 0.55, 0.95)),
                             num_dashes=52, dashed_ratio=0.55).set_stroke(WHITE, LW_THIN + 0.5, 0.6)
        win_lab = label("ao longo do eixo").move_to(P(AX + 1.55, 1.25))
        obs = VGroup(win, pdot, rline, rlab, win_lab)
        ring = DashedVMobject(Circle(radius=R4, arc_center=C3), num_dashes=44, dashed_ratio=0.5).set_stroke(WHITE, LW_THIN + 0.5, 0.65)
        core = VGroup(Circle(radius=0.28, arc_center=C3).set_stroke(width=0).set_fill(BLUE, 0.3),
                      Circle(radius=0.1, arc_center=C3).set_stroke(BLUE_L, 2.5).set_fill(BLUE_L, 1)).set_z_index(6)
        ang = ValueTracker(0.0)
        pp = always_redraw(lambda: Circle(radius=0.1, arc_center=C3 + R4 * U(ang.get_value())).set_stroke(WHITE, 0).set_fill(WHITE, 1).set_z_index(8))
        rl = always_redraw(lambda: DashedLine(C3, C3 + R4 * U(ang.get_value()), dash_length=0.1).set_stroke(WHITE, LW_THIN + 0.5, 0.75))
        top_lab = label("vista de cima").move_to(C3 + P(0, -R4 - 0.42))
        self.play(FadeOut(bg), FadeIn(obs), FadeOut(lam_def, shift=0.12 * UP), FadeIn(VGroup(ring, core, pp, rl, top_lab)), run_time=1.0)
        self.at(89.5)
        self.play(obs.animate.shift(1.3 * UP), run_time=1.2)
        self.play(obs.animate.shift(2.6 * DOWN), run_time=1.8)
        self.play(obs.animate.shift(1.3 * UP), run_time=1.0)

        # girar em torno do eixo: na vista de cima o ponto dá a volta e a fonte continua igual
        self.at(95.0)
        rot_lab = label("em torno do eixo").move_to(C3 + P(0, R4 + 0.42))
        self.play(FadeOut(VGroup(win, win_lab)), FadeIn(rot_lab), run_time=0.8)
        self.play(ang.animate.set_value(360.0), run_time=4.2, rate_func=smooth)

        # pares simétricos: as componentes axiais se anulam
        self.at(103.0)
        pr = self.pair(1.25, 1.45)
        par_lab = label("par simétrico").move_to(P(AX - 1.35, 1.25))
        n_ax = col(note("componentes axiais: se anulam"), 2.4)
        self.play(FadeOut(rot_lab), FadeIn(par_lab), FadeIn(pr.dots), Create(pr.guides), FadeOut(VGroup(pdot, rline, rlab)), run_time=1.1)
        self.at(105.0)
        self.play(FadeIn(pr.e_u), FadeIn(pr.e_d), run_time=1.0)
        self.at(106.6)
        self.play(FadeIn(pr.a_u), FadeIn(pr.a_d), FadeIn(pr.r_u), FadeIn(pr.r_d), pr.e_u.animate.set_opacity(0.3),
                  pr.e_d.animate.set_opacity(0.3), FadeIn(n_ax, shift=0.1 * UP), run_time=1.2)
        self.at(108.6)
        self.play(Indicate(VGroup(pr.a_u, pr.a_d), color=WHITE, scale_factor=1.15), run_time=1.0)
        self.play(pr.a_u.animate.scale(0.01, about_point=P4), pr.a_d.animate.scale(0.01, about_point=P4), run_time=1.2)
        self.remove(pr.a_u, pr.a_d)
        self.at(111.2)
        n_rad = col(note("componentes radiais: se somam", CYAN), 2.4)
        res = vec(P4, P4 + P(2 * pr.rad, 0), CYAN, LW_RES + 1, z=8)
        self.play(FadeOut(n_ax), FadeIn(n_rad, shift=0.1 * UP), FadeOut(VGroup(pr.e_u, pr.e_d)),
                  ReplacementTransform(VGroup(pr.r_u, pr.r_d), res), run_time=1.3)
        # os outros pares fazem o mesmo
        self.at(113.4)
        others = [self.pair(0.65, 0.7), self.pair(1.9, 0.6)]
        self.play(*[FadeIn(o.dots) for o in others], *[FadeIn(o.e_u) for o in others], *[FadeIn(o.e_d) for o in others], run_time=1.0)
        res2 = vec(P4, P4 + P(2.0, 0), CYAN, LW_RES + 1, z=8)
        self.play(*[o.e_u.animate.set_opacity(0.25) for o in others], *[o.e_d.animate.set_opacity(0.25) for o in others],
                  ReplacementTransform(res, res2), run_time=1.2)

        # estado final: radial e só depende de r
        self.at(116.5)
        clutter = VGroup(*[m for o in [pr] + others for m in (o.dots, o.guides)], *[o.e_u for o in others], *[o.e_d for o in others])
        e8 = VGroup(*[vec(C3 + R4 * U(a), C3 + (R4 + 0.4) * U(a), CYAN, LW_VEC + 0.5) for a in range(0, 360, 45)])
        e_lab = eq(r"\vec E", size=M_S, color=CYAN).move_to(P4 + P(2.0 + 0.4, 0.34))
        e_fin = col(eqm(r"{{ \vec E }} {{=}} {{ E(r) }} {{ \,\hat r }}", M_L, {r"\vec E": CYAN, "E(r)": CYAN}), Y_DOM + 0.3, dx=0.3)
        e_box = box(e_fin)
        self.play(FadeOut(VGroup(n_rad, par_lab)), FadeOut(clutter), FadeIn(e_lab), FadeIn(e_fin, shift=0.1 * DOWN),
                  LaggedStart(*[FadeIn(a) for a in e8], lag_ratio=0.08), run_time=1.8)
        self.play(Create(e_box), run_time=0.9)
        pp.clear_updaters()
        rl.clear_updaters()
        self.n04 = SimpleNamespace(junk=VGroup(ring, core, pp, rl, top_lab, e8, e_lab, pdot, rline, rlab, ext, inf_lab, e_box, e_fin), res=res2)
        self.at(T_N05)

    def pair(self, dz, ln):
        """Par de elementos de carga em ±dz ao longo do eixo: E⃗ de cada um no ponto de observação, com componentes axial e radial."""
        p4 = self.p4
        eu, ed = P(AX, dz), P(AX, -dz)
        du, dd = unit(p4 - eu), unit(p4 - ed)
        rad = ln * du[0]
        dots = VGroup(*[Circle(radius=0.14, arc_center=p).set_stroke(BLUE_L, LW_DOT + 0.5).set_fill(BLUE, 0.7).set_z_index(7) for p in (eu, ed)])
        guides = VGroup(*[DashedLine(p, p4, dash_length=0.1).set_stroke(WHITE, LW_THIN, 0.4) for p in (eu, ed)])
        return SimpleNamespace(
            dots=dots, guides=guides, rad=rad,
            e_u=vec(p4, p4 + ln * du, CYAN, LW_THICK + 1, 0.75), e_d=vec(p4, p4 + ln * dd, CYAN, LW_THICK + 1, 0.75),
            a_u=vec(p4 + P(0.2, 0), p4 + P(0.2, ln * du[1]), WHITE, LW_VEC + 1, z=8),
            a_d=vec(p4 + P(-0.2, 0), p4 + P(-0.2, ln * dd[1]), WHITE, LW_VEC + 1, z=8),
            r_u=vec(p4 + P(0, 0.14), p4 + P(rad, 0.14), CYAN, LW_VEC + 1, z=8),
            r_d=vec(p4 + P(0, -0.14), p4 + P(rad, -0.14), CYAN, LW_VEC + 1, z=8))

    # ═══ N05 · linha infinita: lateral e tampas (2:03–2:52) · SPLIT → BUILD ═══
    def n05_lateral_tampas(self):
        self.begin(5, "lateral_tampas")
        self.at(T_N05)
        n4 = self.n04
        gc = GaussCyl(RV, ef_line)
        self.gc = gc
        gc.vis.set_value(0.0)
        gc.add_to(self)
        tag = col(label("superfície gaussiana", VIOLET), Y_TAG)
        self.play(FadeOut(n4.junk), FadeOut(n4.res), gc.vis.animate.set_value(1.0), FadeIn(tag), run_time=1.6)
        # raio r e comprimento L (finito, arbitrário)
        self.at(127.5)
        self.play(gc.dv.animate.set_value(1.0), run_time=0.9)
        self.at(131.0)
        self.play(FadeIn(gc.diml, shift=0.1 * RIGHT), run_time=0.9)
        # lateral: mesma distância ao eixo, mesmo módulo, E paralelo à normal (uma relação ativa por vez)
        self.at(134.6)
        e_par = col(eqm(r"{{ \vec E }} {{ \parallel }} {{ \hat n }}", M_L), Y_ACT)
        e_flat = col(eqm(r"{{ \Phi_{\mathrm{lat}} }} {{=}} {{ E }} {{ A_{\mathrm{lat}} }}", M_L), Y_ACT)
        self.play(gc.lo.animate.set_value(0.17), FadeOut(tag), run_time=1.0)
        self.at(138.0)
        el_patch = Line(P(AX + RV, -0.2), P(AX + RV, 0.2)).set_stroke(WHITE, 8).set_z_index(9)
        n_l = vec(P(AX + RV, 0.16), P(AX + RV + 0.65, 0.16), NHAT, LW_N, z=10)
        n_l_lab = eq(r"\hat n", size=M_S, color=NHAT).move_to(P(AX + RV + 0.95, 0.46))
        e_l_lab = eq(r"\vec E", size=M_S, color=CYAN).move_to(P(AX + RV + 1.45, -0.2))
        self.play(FadeIn(VGroup(el_patch, n_l, n_l_lab, e_l_lab)), FadeIn(e_par, shift=0.1 * DOWN), run_time=1.2)
        self.at(143.0)
        self.play(FadeOut(e_par), run_time=0.5)
        self.play(FadeIn(e_flat, shift=0.1 * DOWN), run_time=0.9)

        # tampas: E continua não nulo, mas a normal é axial; a relação do fluxo lateral desce, apagada
        self.at(147.8)
        cap_p = P(AX + 0.5 * RV, YT - 0.02)
        cap_b = P(AX + 0.5 * RV, YB + 0.02)
        cap_patch = lambda p: Ellipse(width=0.55, height=0.14).move_to(p).set_stroke(WHITE, 3).set_fill(WHITE, 0.15).set_z_index(9)
        el_t = SimpleNamespace(patch=cap_patch(cap_p), n=vec(cap_p, cap_p + P(0, 0.7), NHAT, LW_N, z=10),
                               e=vec(cap_p, cap_p + P(1.0, 0), CYAN, LW_VEC, z=10), ra=right_angle(cap_p, RIGHT, UP, s=0.24, w=3))
        e_t_lab = eq(r"\vec E", size=M_S, color=CYAN).move_to(cap_p + P(1.5, 0.3))
        n_t_lab = eq(r"\hat n", size=M_S, color=NHAT).move_to(cap_p + P(0.32, 0.92))
        el_b = SimpleNamespace(n=vec(cap_b, cap_b + P(0, -0.7), NHAT, LW_N, z=10), e=vec(cap_b, cap_b + P(1.0, 0), CYAN, LW_VEC, z=10))
        e_ne = col(eqm(r"{{ \vec E }} {{ \neq }} {{ \vec 0 }}", M_L), Y_ACT)
        n_ne = col(note("o campo continua lá", CYAN), Y_NOTE)
        self.play(FadeOut(VGroup(el_patch, n_l, n_l_lab, e_l_lab)),
                  e_flat.animate.scale(0.8).move_to(P(0, Y_S2)).align_to(P(RL, 0), LEFT).set_opacity(OP_PREV),
                  gc.lo.animate.set_value(0.07), gc.co.animate.set_value(0.26), gc.ao.animate.set_value(0.45),
                  FadeIn(el_t.patch), FadeIn(el_t.e), FadeIn(e_t_lab), FadeIn(el_b.e), FadeIn(e_ne, shift=0.1 * DOWN), FadeIn(n_ne, shift=0.1 * DOWN),
                  run_time=1.4)
        self.at(150.3)
        e_perp = col(eqm(r"{{ \vec E }} {{ \perp }} {{ \hat n }}", M_L), Y_ACT)
        self.play(FadeIn(el_t.n), FadeIn(n_t_lab), FadeIn(el_b.n), Create(el_t.ra), TransformMatchingTex(e_ne, e_perp), FadeOut(n_ne), run_time=1.3)
        self.play(Indicate(el_t.e, color=WHITE, scale_factor=1.15), run_time=1.0)
        self.play(Indicate(el_t.n, color=WHITE, scale_factor=1.25), run_time=1.0)
        self.play(Indicate(VGroup(el_t.e, el_t.n, el_t.ra), color=WHITE, scale_factor=1.1), run_time=1.0)
        self.at(154.0)
        e_dot = col(eqm(r"{{ \vec E }} {{ \cdot }} {{ \hat n }} {{=}} {{ 0 }}", M_L), Y_ACT)
        self.play(TransformMatchingTex(e_perp, e_dot), Indicate(el_t.ra, color=WHITE, scale_factor=1.6), run_time=1.2)
        # o campo não some: some a contribuição ao fluxo
        self.at(158.6)
        e_ft = col(eqm(r"{{ \Phi_{\mathrm{tampas}} }} {{=}} {{ 0 }}", M_L), Y_ACT)
        self.play(TransformMatchingTex(e_dot, e_ft), Indicate(VGroup(el_t.e, el_b.e), color=CYAN, scale_factor=1.12), run_time=1.5)
        self.at(168.0)
        self.play(Indicate(el_t.ra, color=WHITE, scale_factor=1.8), run_time=1.2)
        self.n05 = SimpleNamespace(junk=VGroup(el_t.patch, el_t.n, el_t.e, el_t.ra, e_t_lab, n_t_lab, el_b.n, el_b.e, e_ft), e_flat=e_flat)
        self.at(T_N06)

    # ═══ N06 · carga envolvida e resultado (2:52–3:36) · BUILD → FOCUS ═══
    def n06_carga_resultado(self):
        self.begin(6, "carga_resultado")
        self.at(T_N06)
        gc, n5 = self.gc, self.n05
        # o fluxo lateral volta à posição ativa; a gaussiana volta a ser só lateral (as tampas não contribuem)
        a_lat = col(eq(r"A_{\mathrm{lat}}", "=", r"2\pi r", "L", size=M_M), 2.15)
        self.play(FadeOut(n5.junk), n5.e_flat.animate.scale(1.25).move_to(P(0, Y_ACT)).align_to(P(RL, 0), LEFT).set_opacity(1.0),
                  gc.lo.animate.set_value(0.17), gc.co.animate.set_value(0.05), gc.ao.animate.set_value(1.0), run_time=1.0)
        circ_lab = eq(r"2\pi r", size=M_S, color=VIOLET).move_to(P(AX - 1.1, YT + 0.62))
        self.play(FadeIn(circ_lab, shift=0.1 * DOWN), FadeIn(a_lat, shift=0.1 * DOWN), Indicate(gc.diml, color=WHITE, scale_factor=1.05),
                  run_time=1.3)
        # carga envolvida: o pedaço do filamento dentro do cilindro
        self.at(177.8)
        seg = Line(P(AX, YB), P(AX, YT)).set_stroke(BLUE_L, 7, 0.9).set_z_index(5.6)
        q_env = col(eq(r"Q_{\mathrm{env}}", "=", r"\lambda", "L", size=M_M, colors={2: BLUE_L}), 1.45)
        self.play(Create(seg), FadeIn(q_env, shift=0.1 * DOWN), FadeOut(circ_lab), run_time=1.3)
        self.play(Indicate(gc.diml, color=WHITE, scale_factor=1.05), Indicate(q_env, color=BLUE_L, scale_factor=1.04), run_time=0.9)

        # Gauss: os dois lados, depois a substituição (os termos iguais se movem; os novos entram)
        self.at(181.0)
        gauss = col(eqm(r"{{ E }} {{ A_{\mathrm{lat}} }} {{=}} \frac{ {{ Q_{\mathrm{env}} }} }{ {{ \varepsilon_0 }} }", M_L), Y_ACT)
        self.play(TransformMatchingTex(n5.e_flat, gauss), run_time=1.2)
        self.at(182.8)
        subst = col(eqm(r"{{ E }} {{(}} {{ 2\pi }} {{ r }} {{ L }} {{)}} {{=}} \frac{ {{ \lambda }} {{ L }} }{ {{ \varepsilon_0 }} }", M_L), Y_ACT)
        self.play(TransformMatchingTex(gauss, subst), a_lat.animate.set_opacity(OP_PREV), q_env.animate.set_opacity(OP_PREV), run_time=1.4)
        # o comprimento cancela: escolha nossa, nos dois lados
        self.at(185.2)
        ls = [p for p in subst if getattr(p, "tex_string", "").strip() == "L"]
        strikes = VGroup(*[strike(p, WHITE, 5) for p in ls])
        self.play(Create(strikes), Indicate(gc.diml, color=WHITE, scale_factor=1.06), run_time=1.0)
        self.at(187.4)
        after = col(eqm(r"{{ E }} {{(}} {{ 2\pi }} {{ r }} {{)}} {{=}} \frac{ {{ \lambda }} }{ {{ \varepsilon_0 }} }", M_L), Y_ACT)
        self.play(TransformMatchingTex(subst, after), FadeOut(strikes), FadeOut(VGroup(a_lat, q_env)), run_time=1.3)
        self.at(188.8)
        a_div = col(eq(r"\div\,2\pi r", size=M_M), Y_NOTE)
        fac = VGroup(*[p for p in after if getattr(p, "tex_string", "").strip() in (r"2\pi", "r")])
        self.play(FadeIn(a_div, shift=0.1 * UP), Indicate(fac, color=WHITE, scale_factor=1.2), run_time=1.0)
        self.at(190.0)
        res = col(eqm(r"{{ E }} {{=}} \frac{ {{ \lambda }} }{ {{ 2\pi }} {{ \varepsilon_0 }} {{ r }} }", M_L), Y_ACT, dx=0.3)
        self.play(TransformMatchingTex(after, res), FadeOut(a_div), run_time=1.3)
        res_box = box(res)
        self.play(Create(res_box), run_time=0.8)

        # E ∝ 1/r e o teste r → 2r (a mesma gaussiana cresce; as setas caem à metade)
        self.at(193.0)
        prop = col(eq("E", r"\propto", r"\frac{1}{r}", size=M_M, colors={0: CYAN}), Y_S1, dx=0.3)
        self.play(FadeIn(prop, shift=0.1 * DOWN), run_time=1.0)
        self.at(195.6)
        test = col(eq(r"r\to 2r", r"\Rightarrow", r"E\to\frac{E}{2}", size=M_M, colors={2: CYAN}), Y_S2, dx=0.3)
        self.play(gc.rt.animate.set_value(2 * RV), FadeIn(test, shift=0.1 * DOWN), run_time=3.2, rate_func=smooth)
        self.at(199.8)
        why = col(VGroup(note("área lateral: o dobro", VIOLET), note("carga envolvida: a mesma", BLUE_L)).arrange(DOWN, aligned_edge=LEFT, buff=0.2), 1.9, dx=0.3)
        self.play(FadeIn(why, shift=0.1 * UP), run_time=1.0)
        self.at(204.4)
        self.play(gc.rt.animate.set_value(RV), FadeOut(VGroup(test, why)), run_time=1.6, rate_func=smooth)
        # primeira ferramenta: o cilindro fica, muda a distribuição da carga
        self.at(207.0)
        k1 = col(VGroup(title("a mesma escolha de", VIOLET), title("superfície gaussiana", VIOLET)).arrange(DOWN, aligned_edge=LEFT, buff=0.1), Y_S1 - 0.1, dx=0.3)
        k2 = col(note("agora, a carga está na casca", BLUE_L), Y_S2 - 0.2, dx=0.3)
        self.play(FadeIn(k1, shift=0.1 * UP), FadeIn(k2, shift=0.1 * UP), FadeOut(prop), run_time=1.1)
        self.n06 = SimpleNamespace(res=res, res_box=res_box, k1=k1, k2=k2, seg=seg)
        self.at(T_N07)

    # ═══ N07 · casca cilíndrica OCA (3:36–4:22) · SPLIT → COMPARE (dentro × fora) ═══
    def n07_casca(self):
        self.begin(7, "casca")
        self.at(T_N07)
        gc, wire, n6 = self.gc, self.wire, self.n06
        R = R_VIS
        gc.efun = ef_casca
        tag = col(label("CASCA UNIFORME · modelo infinito"), Y_TAG)
        shell = hollow(R)
        shell.stretch(0.04, 0, about_point=P(AX, 0))
        self.add(shell)
        # o filamento vira parede: a casca se abre em torno do eixo; a gaussiana não muda
        self.play(FadeOut(VGroup(n6.res, n6.res_box, n6.k1, n6.k2, n6.seg)), FadeOut(wire), FadeIn(tag),
                  shell.animate.stretch(1 / 0.04, 0, about_point=P(AX, 0)), run_time=1.8)
        self.at(218.6)
        dim_R = top_dim(R, "R", drop=YW1 + 0.03)
        self.play(FadeIn(dim_R, shift=0.1 * DOWN), run_time=1.0)
        self.at(221.0)
        lam = col(hchain(eq(r"\lambda", size=M_M, color=BLUE_L), note("carga total por comprimento"), buff=0.25), Y_DOM)
        self.play(FadeIn(lam, shift=0.1 * UP), run_time=1.0)

        # por dentro: nada envolvido; Gauss + simetria cilíndrica ⇒ E = 0 (Q_env = 0 sozinho não bastaria)
        self.at(227.6)
        d1, q1 = row(eq(r"r<R", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=0", size=M_M), Y_DOM)
        self.play(gc.rt.animate.set_value(0.45), FadeOut(lam), FadeIn(d1, shift=0.1 * UP), FadeIn(q1, shift=0.1 * UP), run_time=2.6, rate_func=smooth)
        self.at(231.4)
        e1 = col(eq("E", "=0", size=M_L, colors={0: CYAN}), Y_ACT)
        n1 = col(note("por Gauss + simetria cilíndrica"), Y_NOTE)
        self.play(FadeIn(e1, shift=0.1 * UP), FadeIn(n1, shift=0.1 * UP), run_time=1.0)

        # por fora: toda a carga daquele comprimento; o resultado é o da linha
        self.at(239.6)
        seg = VGroup(*[edge(AX + sg * R, YB, YT, 6) for sg in (-1, 1)]).set_z_index(5.6)
        d2, q2 = row(eq(r"r>R", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=\lambda L", size=M_M), Y_DOM)
        s1d, s1e = row(eq(r"r<R", size=M_D, color=VIOLET), eq("E", "=0", size=M_M, colors={0: CYAN}), Y_S1)
        s1 = VGroup(s1d, s1e)
        self.play(gc.rt.animate.set_value(1.8), FadeIn(seg), FadeOut(VGroup(e1, n1)), FadeIn(s1),
                  ReplacementTransform(d1, d2), TransformMatchingTex(q1, q2), run_time=2.8, rate_func=smooth)
        self.at(243.0)
        e2 = col(eq("E", "=", r"\frac{\lambda}{2\pi\varepsilon_0 r}", size=M_L, colors={0: CYAN}), Y_ACT)
        self.play(FadeIn(e2, shift=0.1 * UP), run_time=1.0)

        # a camada carregada: o campo salta de zero para um valor não nulo
        self.at(246.8)
        s2d, s2e = row(eq(r"r>R", size=M_D, color=VIOLET), eq("E", "=", r"\frac{\lambda}{2\pi\varepsilon_0 r}", size=M_M, colors={0: CYAN}), Y_S2)
        s2 = VGroup(s2d, s2e)
        jump = col(eq(r"E(R^-)=0", r"\neq", r"E(R^+)", size=M_L, colors={0: CYAN, 2: CYAN}), Y_ACT)
        n_j = col(note("salto na camada carregada"), Y_NOTE)
        self.play(FadeOut(seg), FadeOut(e2), FadeIn(s2), FadeIn(jump, shift=0.1 * UP), FadeIn(n_j, shift=0.1 * UP),
                  gc.rt.animate.set_value(R - 0.12), run_time=1.4)
        self.play(Indicate(VGroup(*shell.submobjects[1:]), color=BLUE_L, scale_factor=1.02), gc.rt.animate.set_value(R + 0.12), run_time=1.4)
        self.at(251.0)
        self.play(gc.rt.animate.set_value(R - 0.12), run_time=1.0)
        self.play(gc.rt.animate.set_value(R + 0.12), run_time=1.0)
        self.at(256.0)
        self.play(gc.rt.animate.set_value(1.8), run_time=1.2)
        self.n07 = SimpleNamespace(junk=VGroup(tag, d2, q2, s1, s2, jump, n_j), shell=shell, dim_R=dim_R)
        self.at(T_N08)

    # ═══ N08 · cilindro maciço: duas regiões (4:22–5:14) · SPLIT → BUILD ═══
    def n08_macico(self):
        self.begin(8, "macico")
        self.at(T_N08)
        gc, n7 = self.gc, self.n07
        R = R_VIS
        corpo = solid_body(R)
        lat = lattice_dyn(gc)
        env = env_overlay(gc)
        tag = col(mix("ISOLANTE · ", eq(r"\rho", size=M_S, color=BLUE_L), " constante"), Y_TAG)
        rho = col(eq(r"\rho", r"=\frac{\text{carga}}{\text{volume}}", size=M_L, colors={0: BLUE_L}), Y_ACT)
        gc.efun = ef_solid
        # a casca ganha volume: a parede vira corpo; as cargas passam a estar no volume
        self.add(lat)
        self.play(FadeOut(n7.junk), FadeOut(n7.shell), FadeIn(corpo), FadeIn(tag), FadeIn(rho, shift=0.1 * DOWN), run_time=1.6)
        # gaussiana menor que o corpo: só a parte da fonte que ficou dentro dela (R = fonte, r = gaussiana)
        self.at(271.6)
        h_in, q_in = row(eq(r"r<R", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=\rho\pi r^{2}L", size=M_M), Y_DOM)
        self.add(env)
        self.play(gc.rt.animate.set_value(0.5), FadeOut(rho), FadeIn(h_in, shift=0.1 * UP), FadeIn(q_in, shift=0.1 * UP), run_time=3.0, rate_func=smooth)
        self.play(Indicate(gc.lab, color=VIOLET, scale_factor=1.3), run_time=1.0)
        # carga cresce com r², área com r: o campo cresce linearmente. Cada fator some por uma operação mostrada (πL, depois 2r) e
        # r²/r = r tem destino visual: os r que se cancelam são riscados antes de sumir
        self.at(279.5)
        s1 = col(gx(r"E(2\pi r L)=\frac{\rho\pi r^{2}L}{\varepsilon_0}", 16, cyan=(0,), blue=(8,), violet=(4, 10)), Y_ACT)
        self.play(FadeIn(s1, shift=0.1 * UP), run_time=1.0)
        self.at(281.4)
        a1 = col(eq(r"\div\,\pi L", size=M_M), Y_NOTE)
        self.play(FadeIn(a1, shift=0.1 * UP), *gind(s1, 3, 5, 9, 12), run_time=1.0)
        stk1 = gstrike(s1, 3, 5, 9, 12)
        self.at(283.0)
        self.play(Create(stk1), run_time=0.7)
        self.at(284.0)
        s2 = col(gx(r"E(2r)=\frac{\rho r^{2}}{\varepsilon_0}", 12, cyan=(0,), blue=(6,), violet=(3, 7)), Y_ACT)
        self.play(TransformByGlyphMap(s1, s2, *mv((0, 0), (1, 1), (2, 2), (4, 3), (6, 4), (7, 5), (8, 6), (10, 7), (11, 8), (13, 9), (14, 10), (15, 11)),
                                      ([3, 5, 9, 12], [])), FadeOut(stk1), FadeOut(a1), run_time=1.3)
        self.remove(s1)
        self.at(286.0)
        a2 = col(hchain(eq(r"\div\,2r", size=M_M), eq(r"(r>0)", size=M_S), buff=0.3), Y_NOTE)
        self.play(FadeIn(a2, shift=0.1 * UP), Indicate(VGroup(s2[0][2], s2[0][3]), color=WHITE, scale_factor=1.3), run_time=1.0)
        self.at(287.4)
        sm = col(gx(r"E=\frac{\rho r^{2}}{2\varepsilon_0 r}", 10, cyan=(0,), blue=(2,), violet=(3, 9)), Y_ACT)
        self.play(TransformByGlyphMap(s2, sm, *mv((0, 0), (2, 6), (3, 9), (5, 1), (6, 2), (7, 3), (8, 4), (9, 5), (10, 7), (11, 8)), ([1, 4], [])), run_time=1.4)
        self.remove(s2)
        self.at(289.4)
        sx = col(gx(r"E=\frac{\rho\,r\,r}{2\varepsilon_0\,r}", 10, cyan=(0,), blue=(2,), violet=(3, 4, 9)), Y_ACT)
        self.play(FadeOut(a2), TransformByGlyphMap(sm, sx, *mv(*[(i, i) for i in range(10)])), run_time=1.0)
        self.remove(sm)
        self.at(291.0)
        a3 = col(eq(r"r^{2}\div r=r", size=M_M), Y_NOTE)
        stk2 = gstrike(sx, 4, 9)
        self.play(FadeIn(a3, shift=0.1 * UP), Create(stk2), run_time=0.8)
        self.at(292.0)
        s3 = col(gx(r"E=\frac{\rho r}{2\varepsilon_0}", 8, cyan=(0,), blue=(2,), violet=(3,)), Y_ACT)
        self.play(TransformByGlyphMap(sx, s3, *mv((0, 0), (1, 1), (2, 2), (3, 3), (5, 4), (6, 5), (7, 6), (8, 7)), ([4, 9], [])), FadeOut(stk2), FadeOut(a3), run_time=1.3)
        self.remove(sx)
        self.at(293.6)
        self.play(Indicate(s3, color=CYAN, scale_factor=1.05), run_time=0.9)

        # gaussiana maior que o corpo: a carga envolvida congela em R²; r continua na área
        self.at(294.4)
        res_in = VGroup(eq(r"r<R", size=M_D, color=VIOLET).move_to(P(0, Y_S1)).align_to(P(RL, 0), LEFT), s3)
        h_out, q_out = row(eq(r"r>R", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=\rho\pi R^{2}L", size=M_M), Y_DOM)
        self.play(s3.animate.scale(0.8).move_to(P(0, Y_S1)).align_to(P(RL + 1.3, 0), LEFT).set_opacity(OP_PREV), FadeIn(res_in[0]),
                  ReplacementTransform(h_in, h_out), TransformMatchingTex(q_in, q_out), gc.rt.animate.set_value(1.5),
                  run_time=3.0, rate_func=smooth)
        self.at(298.0)
        t1 = col(gx(r"E(2\pi r L)=\frac{\rho\pi R^{2}L}{\varepsilon_0}", 16, cyan=(0,), blue=(8, 10), violet=(4,)), Y_ACT)
        self.play(FadeIn(t1, shift=0.1 * UP), run_time=1.0)
        self.at(299.4)
        b1 = col(eq(r"\div\,\pi L", size=M_M), Y_NOTE)
        self.play(FadeIn(b1, shift=0.1 * UP), *gind(t1, 3, 5, 9, 12), run_time=1.0)
        stk3 = gstrike(t1, 3, 5, 9, 12)
        self.at(300.8)
        self.play(Create(stk3), run_time=0.7)
        self.at(301.8)
        t2 = col(gx(r"E(2r)=\frac{\rho R^{2}}{\varepsilon_0}", 12, cyan=(0,), blue=(6, 7), violet=(3,)), Y_ACT)
        self.play(TransformByGlyphMap(t1, t2, *mv((0, 0), (1, 1), (2, 2), (4, 3), (6, 4), (7, 5), (8, 6), (10, 7), (11, 8), (13, 9), (14, 10), (15, 11)),
                                      ([3, 5, 9, 12], [])), FadeOut(stk3), FadeOut(b1), run_time=1.3)
        self.remove(t1)
        self.at(303.4)
        b2 = col(hchain(eq(r"\div\,2r", size=M_M), eq(r"(r>0)", size=M_S), buff=0.3), Y_NOTE)
        self.play(FadeIn(b2, shift=0.1 * UP), Indicate(VGroup(t2[0][2], t2[0][3]), color=WHITE, scale_factor=1.3), run_time=1.0)
        self.at(304.6)
        t3 = col(gx(r"E=\frac{\rho R^{2}}{2\varepsilon_0 r}", 10, cyan=(0,), blue=(2, 3), violet=(9,)), Y_ACT)
        self.play(TransformByGlyphMap(t2, t3, *mv((0, 0), (2, 6), (3, 9), (5, 1), (6, 2), (7, 3), (8, 4), (9, 5), (10, 7), (11, 8)), ([1, 4], [])), FadeOut(b2), run_time=1.4)
        self.remove(t2)
        # R (fonte, fixo) e r (gaussiana, variável): duas medidas distintas; R não se cancela com r
        self.at(306.2)
        rr = col(VGroup(mix(eq("R", size=M_S, color=BLUE_L), " raio fixo da fonte"), mix(eq("r", size=M_S, color=VIOLET), " raio da gaussiana")).arrange(DOWN, aligned_edge=LEFT, buff=0.12), Y_S2 - 0.12)
        self.play(FadeIn(rr, shift=0.1 * UP), Indicate(n7.dim_R, color=BLUE_L, scale_factor=1.15), run_time=1.2)
        self.play(Indicate(gc.lab, color=VIOLET, scale_factor=1.3), run_time=1.0)
        self.play(Indicate(gc.lab, color=VIOLET, scale_factor=1.3), Indicate(n7.dim_R, color=BLUE_L, scale_factor=1.15), run_time=1.2)
        self.n08 = SimpleNamespace(junk=VGroup(tag, h_out, q_out, res_in, rr), res_out=t3, corpo=corpo, lat=lat, env=env)
        self.at(T_N09)

    # ═══ N09 · gráfico do cilindro maciço (5:14–5:41) · SPLIT: gráfico e geometria num só sistema ═══
    def n09_grafico(self):
        self.begin(9, "grafico")
        self.at(T_N09)
        gc, n8 = self.gc, self.n08
        R = R_VIS
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 1.2, 1], x_length=5.0, y_length=3.0, tips=False,
                  axis_config={"color": WHITE, "stroke_width": 2, "include_ticks": False, "stroke_opacity": 0.8})
        ax.shift(P(1.7, -2.15) - ax.c2p(0, 0))
        fu = lambda u: u if u <= 1 else 1 / u
        ux = lambda: min(gc.r() / R, 3.0)

        def curva():
            us = np.linspace(0.0, max(ux(), 1e-3), 90)
            return VMobject().set_points_as_corners([ax.c2p(x, fu(x)) for x in us]).set_stroke(CYAN, 5).set_z_index(4)

        def marcador():
            u = ux()
            return VGroup(DashedLine(ax.c2p(u, 0), ax.c2p(u, fu(u)), dash_length=0.1).set_stroke(VIOLET, LW_THIN + 0.5, 0.9),
                          Circle(radius=0.09, arc_center=ax.c2p(u, fu(u))).set_stroke(WHITE, 2).set_fill(CYAN, 1).set_z_index(6))

        lab_x = eq(r"r/R", size=M_M).move_to(ax.c2p(2.85, 0) + P(0.1, -0.4))
        lab_y = eq(r"E/E_R", size=M_M).move_to(ax.c2p(0, 1.18) + P(0.25, 0.25)).align_to(P(RL + 0.1, 0), LEFT)
        lab_norm = eq(r"E_R=E(R)", size=34).move_to(P(6.15, 1.25))
        tick1 = VGroup(DashedLine(ax.c2p(1, 0), ax.c2p(1, 1), dash_length=0.1).set_stroke(WHITE, LW_THIN, 0.4),
                       eq("1", size=34).move_to(ax.c2p(1, 0) + P(0, -0.32)), eq("1", size=34).move_to(ax.c2p(0, 1) + P(-0.28, 0)))
        # leitura ao vivo: Q_env e E mudam de lei exatamente em r = R
        live = []
        for expr, cx, dentro in ((r"Q_{\mathrm{env}}\propto r^{2}", RL, True), (r"Q_{\mathrm{env}}=\text{constante}", RL, False),
                                 (r"E\propto r", RL + 3.7, True), (r"E\propto\frac{1}{r}", RL + 3.7, False)):
            m = eq(expr, size=34).move_to(P(0, 2.75)).align_to(P(cx, 0), LEFT)
            if expr.startswith("E"):
                m.set_color(CYAN)
            m.add_updater(lambda mm, d=dentro: mm.set_opacity(1.0 if (gc.r() < R - 1e-3) == d else 0.0))
            live.append(m)
        gc.efun = ef_solid
        lab_lin = eq("E", "=", r"\frac{\rho r}{2\varepsilon_0}", size=34, colors={0: CYAN}).move_to(ax.c2p(0.5, 1.12) + P(1.0, 0.1))
        lab_out = eq("E", "=", r"\frac{\rho R^{2}}{2\varepsilon_0 r}", size=34, colors={0: CYAN}).move_to(ax.c2p(2.05, 0.9) + P(0.2, 0.35))
        self.play(FadeOut(n8.junk), FadeOut(n8.res_out), gc.rt.animate.set_value(0.04), Create(ax), FadeIn(VGroup(lab_x, lab_y, lab_norm, tick1)),
                  run_time=1.6, rate_func=smooth)
        curve, mark = always_redraw(curva), always_redraw(marcador)
        for m in live:
            m.update()
        self.add(curve, mark, *live)
        self.at(316.4)
        # começa em zero, sobe em linha reta até a borda
        self.play(gc.rt.animate.set_value(R), run_time=3.4, rate_func=smooth)
        # em r = R: pausa; os dois ramos se encontram (ρr/2ε₀ → ρR/2ε₀ = ρR²/(2ε₀R) → ρR²/(2ε₀r) para r > R)
        self.at(320.0)
        ch1 = eqm(r"{{ E }} {{(}} {{ R }} {{)}} {{=}} \frac{ {{ \rho }} {{ R }} }{ {{ 2 }} {{ \varepsilon_0 }} }", M_M).move_to(P(0, 2.05)).align_to(P(RL, 0), LEFT)
        self.play(Indicate(mark, color=WHITE, scale_factor=1.5), FadeIn(lab_lin, shift=0.1 * UP), FadeIn(ch1, shift=0.1 * DOWN), run_time=1.3)
        self.at(321.8)
        ch2 = eqm(r"{{ E }} {{(}} {{ R }} {{)}} {{=}} \frac{ {{ \rho }} {{ R }}^{2} }{ {{ 2 }} {{ \varepsilon_0 }} {{ R }} }", M_M).move_to(P(0, 2.05)).align_to(P(RL, 0), LEFT)
        self.play(TransformMatchingTex(ch1, ch2), run_time=1.3)
        self.wait(1.0)
        self.at(324.4)
        ch3 = eqm(r"{{ E }} {{(}} {{ r }} {{)}} {{=}} \frac{ {{ \rho }} {{ R }}^{2} }{ {{ 2 }} {{ \varepsilon_0 }} {{ r }} }", M_M).move_to(P(0, 2.05)).align_to(P(RL, 0), LEFT)
        self.play(TransformMatchingTex(ch2, ch3), gc.rt.animate.set_value(2.6 * R), run_time=3.6, rate_func=smooth)
        self.play(FadeIn(lab_out, shift=0.1 * UP), FadeOut(ch3), run_time=1.0)
        self.at(329.6)
        # o campo não salta: não há camada de carga na borda (a casca salta, o maciço não)
        jump_dots = VGroup(Line(ax.c2p(0, 0), ax.c2p(1, 0)).set_stroke(VIOLET, 6, 0.9),
                           DashedLine(ax.c2p(1, 0.08), ax.c2p(1, 0.92), dash_length=0.08).set_stroke(VIOLET, LW_VEC, 0.9),
                           Circle(radius=0.09, arc_center=ax.c2p(1, 0)).set_stroke(VIOLET, 3).set_fill(BACKGROUND_COLOR, 1),
                           Circle(radius=0.09, arc_center=ax.c2p(1, 1)).set_stroke(VIOLET, 3).set_fill(VIOLET, 1)).set_z_index(7)
        lab_c = label("casca: salta em R", VIOLET).move_to(P(0, 2.05)).align_to(P(RL, 0), LEFT)
        lab_m = label("maciço: contínuo em R", CYAN).move_to(P(0, 2.12)).align_to(P(RL, 0), LEFT)
        eq_c = eq(r"E(R^{-})", "=", r"E(R^{+})", size=M_M, colors={0: CYAN, 2: CYAN}).move_to(P(0, 1.62)).align_to(P(RL, 0), LEFT)
        # primeiro o maciço (curva ciano, sem salto): a gaussiana atravessa a borda e a lei, a carga envolvida e o marcador mudam juntos
        self.play(gc.rt.animate.set_value(R + 0.14), FadeIn(lab_m, shift=0.1 * UP), run_time=1.4, rate_func=smooth)
        self.play(gc.rt.animate.set_value(R - 0.14), FadeIn(eq_c, shift=0.1 * UP), run_time=1.2, rate_func=smooth)
        self.play(gc.rt.animate.set_value(R + 0.14), run_time=1.2, rate_func=smooth)
        self.play(gc.rt.animate.set_value(R), Indicate(mark, color=WHITE, scale_factor=1.3), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(lab_m), FadeOut(eq_c), run_time=0.45)
        # só depois o ghost da casca, em violeta, para comparar
        self.play(FadeIn(jump_dots), FadeIn(lab_c, shift=0.1 * UP), run_time=1.2)
        self.wait(1.5)
        self.at(339.0)
        self.play(FadeOut(jump_dots), FadeOut(lab_c), gc.rt.animate.set_value(1.5), run_time=1.4, rate_func=smooth)
        curve.clear_updaters()
        mark.clear_updaters()
        for m in live:
            m.clear_updaters()
        self.n09 = SimpleNamespace(junk=VGroup(ax, curve, mark, lab_x, lab_y, lab_norm, tick1, lab_lin, lab_out, *live))
        self.at(T_N10)

    # ═══ N10 · capacitor coaxial (5:41–6:22) · COMPARE → BUILD, com holofote por região ═══
    def n10_coaxial(self):
        self.begin(10, "coaxial")
        self.at(T_N10)
        gc, n7, n8, n9 = self.gc, self.n07, self.n08, self.n09
        a, b = R_VIS, B_VIS
        inner = solid_body(a, metal=True)
        inner_s = VGroup(*[sign_col(AX + sg * a, SRC0, YW1, False, s=0.09, color=WHITE, w=3) for sg in (-1, 1)]).set_z_index(5)
        outer = hollow(b, minus=True, metal=True, open_frac=0.82, charge_inner=True)
        dm_in, dm_out = Dimmer(VGroup(inner, inner_s)), Dimmer(outer)
        dim_a = top_dim(a, "a", drop=YW1 + 0.03)
        dim_b = top_dim(b, "b", y=2.75, drop=YW1 + 0.03)
        gap_e = VGroup(*[vec(P(AX + sg * r_, y_), P(AX + sg * (r_ + 0.36 / r_), y_), CYAN, LW_VEC, z=7) for sg in (-1, 1)
                         for r_, y_ in ((0.95, 0.75), (1.2, 0.0), (1.45, -0.75))])
        tag = col(mix("CONDUTORES · ", eq(r"+\lambda", size=M_S, color=BLUE_L), " e ", eq(r"-\lambda", size=M_S, color=BLUE_L)), Y_TAG)
        gc.efun = ef_none
        # o isolante vira condutor maciço (carga só na superfície): material diferente, mais sólido e com brilho
        self.play(FadeOut(n9.junk), FadeOut(n8.corpo), FadeOut(n8.lat), FadeOut(n8.env), FadeIn(inner), FadeIn(inner_s), FadeIn(tag),
                  ReplacementTransform(n7.dim_R, dim_a), run_time=1.8)
        k1 = col(hchain(eq(r"+\lambda", size=M_M, color=BLUE_L), note("núcleo condutor maciço"), buff=0.3), Y_DOM)
        self.play(FadeIn(k1, shift=0.1 * UP), run_time=0.9)
        # a casca externa (carga oposta, na sua superfície interna): condutora, delgada, oca
        self.at(346.0)
        k2 = col(hchain(eq(r"-\lambda", size=M_M, color=BLUE_L), note("casca condutora delgada"), buff=0.3), Y_DOM - 0.9)
        self.play(FadeIn(outer, shift=0.1 * RIGHT), FadeIn(dim_b, shift=0.1 * DOWN), FadeIn(k2, shift=0.1 * UP), run_time=1.8)

        # r < a: dentro do metal, nada envolvido e E = 0 (holofote no núcleo)
        self.at(355.4)
        env = env_overlay(gc, top=lambda r: r if r <= a else (a if r <= b else 0.02))
        d1, q1 = row(eq(r"r<a", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=0", size=M_M), Y_DOM, 1.5)
        self.add(env)
        self.play(gc.rt.animate.set_value(0.45), FadeOut(VGroup(k1, k2)), dm_out.to(0.3), FadeIn(d1, shift=0.1 * UP), FadeIn(q1, shift=0.1 * UP),
                  run_time=2.4, rate_func=smooth)
        e1 = col(eq("E", "=0", size=M_L, colors={0: CYAN}), Y_ACT)
        n1 = col(note("dentro do metal"), Y_NOTE)
        self.play(FadeIn(e1, shift=0.1 * UP), FadeIn(n1, shift=0.1 * UP), run_time=0.9)
        # a < r < b: a gaussiana envolve a carga positiva do interno; o campo aparece no vão (holofote no vão)
        self.at(359.8)
        d2, q2 = row(eq(r"a<r<b", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=\lambda L", size=M_M), Y_DOM, 1.9)
        r1d, r1e = row(eq(r"r<a", size=M_D, color=VIOLET), eq("E", "=0", size=M_M, colors={0: CYAN}), Y_S2, 1.5)
        r1 = VGroup(r1d, r1e)
        gc.efun = ef_none
        self.play(gc.rt.animate.set_value(1.25), dm_in.to(0.55), dm_out.to(0.55), FadeOut(VGroup(e1, n1)), FadeIn(r1),
                  ReplacementTransform(d1, d2), TransformMatchingTex(q1, q2), FadeIn(gap_e, shift=0.05 * RIGHT), run_time=2.4, rate_func=smooth)
        e2 = col(eq("E", "=", r"\frac{\lambda}{2\pi\varepsilon_0 r}", size=M_L, colors={0: CYAN}), Y_ACT)
        self.play(FadeIn(e2, shift=0.1 * UP), run_time=1.0)
        # r > b: as cargas envolvidas se cancelam; campo externo nulo; confinado ao vão
        self.at(365.4)
        d3, q3 = row(eq(r"r>b", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=(\lambda-\lambda)L=0", size=M_M), Y_DOM, 1.2)
        r2d, r2e = row(eq(r"a<r<b", size=M_D, color=VIOLET), eq("E", "=", r"\frac{\lambda}{2\pi\varepsilon_0 r}", size=M_M, colors={0: CYAN}), Y_S1, 1.9)
        r2 = VGroup(r2d, r2e)
        gc.efun = ef_none
        self.play(gc.rt.animate.set_value(2.3), dm_in.to(0.5), dm_out.to(0.85), FadeOut(e2), FadeIn(r2), ReplacementTransform(d2, d3),
                  TransformMatchingTex(q2, q3), run_time=2.4, rate_func=smooth)
        e3 = col(eq("E", "=0", size=M_L, colors={0: CYAN}), Y_ACT)
        n3 = col(note("campo confinado ao vão", CYAN), Y_NOTE)
        self.play(FadeIn(e3, shift=0.1 * UP), FadeIn(n3, shift=0.1 * UP), run_time=0.9)
        self.at(371.5)
        self.play(dm_in.to(1.0), dm_out.to(1.0), Indicate(gap_e, color=CYAN, scale_factor=1.15), run_time=1.2)
        self.play(Indicate(gap_e, color=CYAN, scale_factor=1.15), run_time=1.2)
        self.n10 = SimpleNamespace(junk=VGroup(tag, d3, q3, e3, n3, r1, r2), inner=inner, inner_s=inner_s, outer=outer, dims=VGroup(dim_a, dim_b),
                                   gap_e=gap_e, env=env)
        self.at(T_N11)

    # ═══ N11 · síntese cilíndrica e ponte para o plano (6:22–6:32) · FOCUS ═══
    def n11_ponte(self):
        self.begin(11, "ponte")
        self.at(T_N11)
        gc, n10 = self.gc, self.n10
        # transição limpa: o coaxial grande sai por inteiro antes das quatro miniaturas
        left = VGroup(n10.junk, n10.inner, n10.inner_s, n10.outer, n10.dims, n10.gap_e, gc.diml)
        self.play(FadeOut(left), gc.vis.animate.set_value(0.0), gc.dv.animate.set_value(0.0), run_time=0.9)
        self.remove(n10.env, gc.geom, gc.arrows, gc.dimr, gc.lab)
        # quatro cortes transversais, a MESMA gaussiana violeta: a geometria gaussiana continua; muda Q_env(r)
        xs, y0, Rg, k = (-5.25, -1.75, 1.75, 5.25), 0.15, 1.38, 1.2
        icones = []
        for nome, x in zip(("linha", "casca", "maciço", "coaxial"), xs):
            ctr = P(x, y0)
            ring_g = DashedVMobject(Circle(radius=Rg, arc_center=ctr), num_dashes=48, dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.95)
            fill_g = Circle(radius=Rg, arc_center=ctr).set_stroke(width=0).set_fill(VIOLET, 0.07)
            if nome == "linha":
                src = VGroup(Circle(radius=0.36, arc_center=ctr).set_stroke(width=0).set_fill(BLUE, 0.25),
                             Circle(radius=0.14, arc_center=ctr).set_stroke(BLUE_L, 2.5).set_fill(BLUE_L, 1))
            elif nome == "casca":
                src = VGroup(Circle(radius=0.62 * k, arc_center=ctr).set_stroke(BLUE, 12, 0.3), Circle(radius=0.62 * k, arc_center=ctr).set_stroke(BLUE_L, 4),
                             *[sign(ctr + 0.62 * k * U(a), s=0.07) for a in range(0, 360, 45)])
            elif nome == "maciço":
                src = VGroup(*[Circle(radius=0.62 * k * q, arc_center=ctr).set_stroke(width=0).set_fill(BLUE, 0.14) for q in (1.0, 0.75, 0.5, 0.25)],
                             Circle(radius=0.62 * k, arc_center=ctr).set_stroke(BLUE_L, 4),
                             *[sign(ctr + d * k, s=0.06, color=BLUE_L, w=2.2) for d in (P(-0.25, 0.2), P(0.2, 0.25), P(0.0, -0.1), P(-0.2, -0.3), P(0.3, -0.2))])
            else:
                src = VGroup(*[Circle(radius=0.3 * k * q, arc_center=ctr).set_stroke(width=0).set_fill(BLUE_L, 0.18) for q in (1.0, 0.65)],
                             Circle(radius=0.3 * k, arc_center=ctr).set_stroke(BLUE_L, 4), sign(ctr, s=0.09, w=3),
                             Circle(radius=0.62 * k, arc_center=ctr).set_stroke(BLUE, 12, 0.3), Circle(radius=0.62 * k, arc_center=ctr).set_stroke(BLUE_L, 4),
                             *[sign(ctr + 0.62 * k * U(a) * 0.93, True, s=0.07) for a in range(0, 360, 60)])
            nm = body(nome).move_to(ctr + P(0, -Rg - 0.42))
            icones.append(VGroup(fill_g, ring_g, src, nm))
        hdr = hchain(title("o que muda:"), eq(r"Q_{\mathrm{env}}(r)", size=M_L), buff=0.35).move_to(P(0, 2.5))
        gaus_lab = note("a mesma gaussiana em todos", VIOLET).move_to(P(0, -2.8))
        self.play(FadeIn(hdr, shift=0.1 * UP), LaggedStart(*[FadeIn(i, scale=0.94) for i in icones], lag_ratio=0.3), run_time=2.6)
        self.play(FadeIn(gaus_lab, shift=0.1 * UP), run_time=0.7)
        self.at(388.2)
        # a tela limpa e abre o capítulo planar
        pergunta = title("E para uma folha uniforme e infinita?").move_to(P(0, -0.1))
        self.play(FadeOut(VGroup(*icones, hdr, gaus_lab)), run_time=0.8)
        self.play(FadeIn(pergunta, shift=0.1 * UP), run_time=1.0)
        self.n11 = SimpleNamespace(pergunta=pergunta)
        self.at(T_N12)

    # ═══ N12 · folha infinita não condutora (6:32–8:43) · SPLIT: simetria, pillbox e E = σ/(2ε₀) ═══
    def n12_folha(self):
        self.begin(12, "folha")
        self.at(T_N12)
        gc = self.gc
        self.remove(gc.geom, gc.arrows, gc.dimr, gc.lab)
        sh = plane_body(XS, SW)
        self.sh = sh
        tag = col(label("FOLHA INFINITA · modelo infinito"), Y_TAG)
        sig = col(eq(r"\sigma", r"=\frac{\text{carga}}{\text{área}}", size=M_L, colors={0: BLUE_L}), Y_ACT)
        self.play(FadeOut(self.n11.pergunta), run_time=0.6)
        self.play(FadeIn(sh), FadeIn(tag), run_time=1.4)
        # σ: a mesma carga por área em todo o plano; o trecho de área desliza pela folha
        self.at(T_N12 + 3.0)
        unit_patch = patch_on(XS, SW, pr=0.42)
        sig_lab = eq(r"\sigma", size=M_M, color=BLUE_L).move_to(P(XS - 0.85, 0.1))
        bg = VGroup(unit_patch, sig_lab)
        self.play(FadeIn(bg), FadeIn(sig, shift=0.1 * DOWN), run_time=1.1)
        self.at(T_N12 + 7.0)
        self.p4 = P(XS + 1.5, 0.0)
        p4 = self.p4
        pdot = Circle(radius=0.1, arc_center=p4).set_stroke(WHITE, 0).set_fill(WHITE, 1).set_z_index(8)
        xline = DashedLine(P(XS, 0.0), p4, dash_length=0.1).set_stroke(WHITE, LW_THIN + 0.5, 0.75)
        xlab = eq("x", size=M_M).move_to(P(XS + 0.75, 0.34))
        obs = VGroup(pdot, xline, xlab)
        n_slide = col(VGroup(note("deslocar no plano"), note("preserva a distribuição")).arrange(DOWN, aligned_edge=LEFT, buff=0.1), Y_DOM)
        # o ponto de observação anda paralelo à folha, à mesma distância x: a distribuição vista dele é sempre a mesma
        self.play(FadeOut(bg), FadeIn(obs), FadeIn(n_slide, shift=0.1 * UP), run_time=1.1)
        self.play(obs.animate.shift(1.3 * UP), run_time=1.3)
        self.play(obs.animate.shift(2.6 * DOWN), run_time=1.8)
        self.play(obs.animate.shift(1.3 * UP), run_time=1.0)

        # um ponto qualquer: as componentes paralelas ao plano se anulam por pares simétricos
        self.at(T_N12 + 16.0)
        self.play(FadeOut(VGroup(sig, n_slide)), run_time=0.8)
        self.at(T_N12 + 20.0)
        pr = self.pair(1.1, 1.1)
        n_par = col(note("componentes paralelas: se anulam"), Y_DOM)
        self.play(FadeIn(pr.dots), Create(pr.guides), FadeIn(pr.e_u), FadeIn(pr.e_d), run_time=1.2)
        self.at(T_N12 + 23.4)
        self.play(FadeIn(pr.a_u), FadeIn(pr.a_d), FadeIn(pr.r_u), FadeIn(pr.r_d), pr.e_u.animate.set_opacity(0.3), pr.e_d.animate.set_opacity(0.3),
                  FadeIn(n_par, shift=0.1 * UP), run_time=1.2)
        self.at(T_N12 + 26.4)
        self.play(Indicate(VGroup(pr.a_u, pr.a_d), color=WHITE, scale_factor=1.15), run_time=1.0)
        self.play(pr.a_u.animate.scale(0.01, about_point=p4), pr.a_d.animate.scale(0.01, about_point=p4), run_time=1.2)
        self.remove(pr.a_u, pr.a_d)
        self.at(T_N12 + 30.0)
        n_nor = col(note("só sobra a componente normal", CYAN), Y_DOM)
        res_r = vec(p4, p4 + P(1.5, 0), CYAN, LW_RES + 1, z=8)
        self.play(FadeOut(n_par), FadeIn(n_nor, shift=0.1 * UP), FadeOut(VGroup(pr.e_u, pr.e_d)), ReplacementTransform(VGroup(pr.r_u, pr.r_d), res_r),
                  run_time=1.3)
        self.play(FadeOut(VGroup(pr.dots, pr.guides)), run_time=0.7)
        # os dois lados são equivalentes: mesmo módulo, sentidos opostos
        self.at(T_N12 + 35.0)
        pm = P(XS - 1.5, 0.0)
        res_l = vec(pm, pm + P(-1.5, 0), CYAN, LW_RES + 1, z=8)
        pdot_l = Circle(radius=0.1, arc_center=pm).set_stroke(WHITE, 0).set_fill(WHITE, 1).set_z_index(8)
        n_eq = col(note("os dois lados são equivalentes"), Y_DOM)
        mod = col(eq(r"|\vec E(-x)|", "=", r"|\vec E(x)|", size=M_L, colors={0: CYAN, 2: CYAN}), Y_ACT)
        self.play(FadeOut(n_nor), FadeOut(tag), FadeIn(n_eq, shift=0.1 * UP), FadeIn(pdot_l), FadeIn(res_l), FadeIn(mod, shift=0.1 * DOWN), run_time=1.4)
        self.at(T_N12 + 42.0)
        self.play(Indicate(VGroup(res_l, res_r), color=WHITE, scale_factor=1.06), run_time=1.2)
        self.n12a = SimpleNamespace(junk=VGroup(pdot, xline, xlab, pdot_l, res_l, res_r, n_eq, mod))

        # o pillbox: a mesma ideia do cilindro gaussiano, agora atravessando a folha
        self.at(T_N12 + 47.0)
        pill = Pill(0.05, ef_sheet)
        self.pill = pill
        pill.ao.set_value(0.0)
        pill.cs.set_value(0.0)
        pill.add_to(self)
        inside = patch_on(XS, SW)
        lab_g = col(label("superfície gaussiana", VIOLET), Y_TAG)
        self.play(FadeOut(self.n12a.junk), pill.dt.animate.set_value(1.1), FadeIn(inside), FadeIn(lab_g), run_time=2.0, rate_func=smooth)
        a_lab = eq("A", size=M_S, color=VIOLET).move_to(P(XS + 1.1 + 0.45, PR + 0.3))
        self.play(pill.ao.animate.set_value(1.0), FadeIn(a_lab), run_time=1.0)
        # tampas: E paralelo a n̂, contribuem; lateral: E ⟂ n̂, fluxo nulo
        self.at(T_N12 + 51.4)
        cc = P(XS + 1.1, 0.0)
        n_c = vec(cc + P(0, 0.3), cc + P(0.65, 0.3), NHAT, LW_N, z=10)
        n_c_lab = eq(r"\hat n", size=M_S, color=NHAT).move_to(cc + P(0.95, 0.3))
        e_c_lab = eq(r"\vec E", size=M_S, color=CYAN).move_to(cc + P(1.45, -0.38))
        ccl = P(XS - 1.1, 0.0)
        n_cl = vec(ccl + P(0, 0.3), ccl + P(-0.65, 0.3), NHAT, LW_N, z=10)
        n_cl_lab = eq(r"\hat n", size=M_S, color=NHAT).move_to(ccl + P(-0.95, 0.3))
        e_cl_lab = eq(r"\vec E", size=M_S, color=CYAN).move_to(ccl + P(-1.45, -0.38))
        e1 = col(eqm(r"{{ \vec E }} {{ \parallel }} {{ \hat n }}", M_L), Y_ACT)
        t1 = col(note("nas duas tampas"), Y_NOTE)
        self.play(pill.cs.animate.set_value(1.0), FadeIn(VGroup(n_c, n_c_lab, e_c_lab, n_cl, n_cl_lab, e_cl_lab)), FadeIn(e1, shift=0.1 * DOWN), FadeIn(t1, shift=0.1 * UP), run_time=1.4)
        self.at(T_N12 + 58.0)
        lp = P(XS + 0.4, PR)
        n_l = vec(lp, lp + P(0, 0.6), NHAT, LW_N, z=10)
        e_l = vec(lp, lp + P(0.7, 0), CYAN, LW_VEC, z=10)
        ra = right_angle(lp, RIGHT, UP, s=0.22, w=3)
        n_l_lab = eq(r"\hat n", size=M_S, color=NHAT).move_to(lp + P(0.3, 0.5))
        e2 = col(eqm(r"{{ \vec E }} {{ \perp }} {{ \hat n }}", M_L), Y_ACT)
        t2 = col(note("na lateral"), Y_NOTE)
        self.play(FadeIn(VGroup(n_l, e_l, ra, n_l_lab)), TransformMatchingTex(e1, e2), FadeOut(t1), FadeIn(t2, shift=0.1 * UP), run_time=1.3)
        self.at(T_N12 + 62.0)
        e3 = col(eqm(r"{{ \Phi_{\mathrm{lat}} }} {{=}} {{ 0 }}", M_L), Y_ACT)
        self.play(TransformMatchingTex(e2, e3), Indicate(ra, color=WHITE, scale_factor=1.6), run_time=1.2)
        self.at(T_N12 + 66.0)
        # Φ nas duas tampas: o primeiro EA é a tampa da direita, o segundo a da esquerda (E e n̂ no mesmo sentido, nas duas); EA + EA = 2EA
        f1 = col(gx(r"\Phi=EA+EA", 7, cyan=(2, 5)), Y_ACT)
        t3 = col(VGroup(note("cada tampa contribui com +EA:"), mix("E e ", eq(r"\hat n", size=M_S, color=NHAT), " no mesmo sentido")).arrange(DOWN, aligned_edge=LEFT, buff=0.1), Y_NOTE - 0.1)
        cap_r = Ellipse(width=CW + 0.16, height=2 * PR + 0.16).move_to(P(XS + 1.1, 0.0)).set_stroke(WHITE, 6).set_z_index(9)
        cap_l = Ellipse(width=CW + 0.16, height=2 * PR + 0.16).move_to(P(XS - 1.1, 0.0)).set_stroke(WHITE, 6).set_z_index(9)
        self.play(FadeOut(t2), FadeOut(e3), run_time=0.5)
        self.play(FadeIn(f1, shift=0.1 * DOWN), FadeIn(t3, shift=0.1 * UP), Indicate(pill.geom, color=VIOLET, scale_factor=1.02), run_time=1.1)
        self.at(T_N12 + 68.0)
        self.play(FadeIn(cap_r), Indicate(VGroup(f1[0][2], f1[0][3]), color=WHITE, scale_factor=1.3), run_time=0.9)
        self.play(FadeOut(cap_r), FadeIn(cap_l), Indicate(VGroup(f1[0][5], f1[0][6]), color=WHITE, scale_factor=1.3), run_time=0.9)
        self.play(FadeOut(cap_l), run_time=0.4)
        self.at(T_N12 + 72.0)
        f2 = col(gx(r"\Phi=2EA", 5, cyan=(3,)), Y_ACT)
        self.play(TransformByGlyphMap(f1, f2, *mv((0, 0), (1, 1), (2, 3), (3, 4), (4, 2), (5, 3), (6, 4))), FadeOut(t3), run_time=1.3)
        self.remove(f1)
        # carga envolvida: o pedaço da folha dentro do pillbox
        self.at(T_N12 + 76.0)
        q = col(eqm(r"{{ Q_{\mathrm{env}} }} {{=}} {{ \sigma }} {{ A }}", M_M), Y_DOM)
        self.play(FadeIn(q, shift=0.1 * UP), Indicate(inside, color=WHITE, scale_factor=1.05), run_time=1.3)
        self.at(T_N12 + 82.0)

        # Gauss: 2EA = σA/ε₀; o A cancela nos dois lados; depois o 2 passa para o denominador: E = σ/(2ε₀)
        g1 = col(gx(r"2EA=\frac{\sigma A}{\varepsilon_0}", 9, cyan=(1,), blue=(4,)), Y_ACT)
        self.play(TransformByGlyphMap(f2, g1, *mv((2, 0), (3, 1), (4, 2), (1, 3)), ([0], []), ([], [4, 5, 6, 7, 8])), FadeOut(q), run_time=1.5)
        self.remove(f2)
        self.at(T_N12 + 88.0)
        stk = gstrike(g1, 2, 5)
        self.play(Create(stk), Indicate(a_lab, color=WHITE, scale_factor=1.3), run_time=1.0)
        self.at(T_N12 + 90.2)
        g2 = col(gx(r"2E=\frac{\sigma}{\varepsilon_0}", 7, cyan=(1,), blue=(3,)), Y_ACT)
        self.play(TransformByGlyphMap(g1, g2, *mv((0, 0), (1, 1), (3, 2), (4, 3), (6, 4), (7, 5), (8, 6)), ([2, 5], [])), FadeOut(stk), run_time=1.3)
        self.remove(g1)
        self.at(T_N12 + 92.6)
        g3 = col(gx(r"E=\frac{\sigma}{2\varepsilon_0}", 7, cyan=(0,), blue=(2,)), Y_ACT, dx=0.3)
        self.play(TransformByGlyphMap(g2, g3, *mv((0, 4), (1, 0), (2, 1), (3, 2), (4, 3), (5, 5), (6, 6))), run_time=1.3)
        self.remove(g2)
        g3_box = box(g3)
        self.play(Create(g3_box), run_time=0.8)
        # payoff: a distância não aparece (as tampas se afastam, A e Q_env não mudam)
        self.at(T_N12 + 97.0)
        n_d = col(mix(eq("E", size=M_S, color=CYAN), " não depende da distância", color=CYAN, size=T_NOTE, op=0.92), Y_NOTE - 0.4)
        self.play(pill.dt.animate.set_value(2.6), FadeIn(n_d, shift=0.1 * UP), run_time=3.0, rate_func=smooth)
        self.play(pill.dt.animate.set_value(1.1), run_time=2.0, rate_func=smooth)
        self.at(T_N12 + 108.0)
        n_i = col(note("modelo infinito: sem efeitos de borda"), Y_NOTE - 1.1)
        self.play(FadeIn(n_i, shift=0.1 * UP), run_time=1.0)
        self.n12 = SimpleNamespace(junk=VGroup(g3, g3_box, n_d, n_i, a_lab, n_c, n_c_lab, e_c_lab, n_cl, n_cl_lab, e_cl_lab, n_l, e_l, ra, n_l_lab, inside, lab_g))
        self.at(T_N13)

    # ═══ N13 · placa (slab) infinita com espessura (8:43–10:11) · SPLIT: pillbox, E_x(x) e gráfico sincronizado ═══
    def n13_slab(self):
        self.begin(13, "slab")
        self.at(T_N13)
        pill, sh, n12 = self.pill, self.sh, self.n12
        a = A_S
        Yd, Ya, Yn = 1.5, 0.62, -0.15
        slab = slab_box(XS, a)
        lat = lattice_slab(pill, a)
        env = env_slab(pill, a)
        tag = col(mix("PLACA COM ESPESSURA · ", eq(r"\rho", size=M_S, color=BLUE_L), " constante"), 2.8)
        inf_n = col(label("infinita nas direções paralelas às faces"), 2.17)
        ruler = slab_ruler(XS, a)
        xline = DashedLine(P(XS, SY0 + 0.1), P(XS, SY1 - 0.1), dash_length=0.12).set_stroke(WHITE, 2, 0.5).set_z_index(5.2)
        pill.ef = ef_slab
        # a folha ganha espessura: o material passa a ocupar um volume (corte transversal com faces em x = ±a); o pillbox é o mesmo
        self.add(lat)
        self.play(FadeOut(n12.junk), Transform(sh, slab), FadeIn(tag), FadeIn(lat), pill.dt.animate.set_value(0.5), run_time=2.4, rate_func=smooth)
        self.at(T_N13 + 3.0)
        rho = col(eq(r"\rho", r"=\frac{\text{carga}}{\text{volume}}", size=M_L, colors={0: BLUE_L}), Ya)
        self.play(FadeIn(ruler), FadeIn(xline), FadeIn(inf_n, shift=0.1 * UP), FadeIn(rho, shift=0.1 * DOWN), run_time=1.2)

        # lado direito, 0 < x < a: x é uma distância positiva e E é o módulo; só a fatia de espessura 2x está envolvida
        self.at(T_N13 + 8.0)
        cota_m = always_redraw(lambda: slab_cota(pill, a))
        l2x = eq(r"2x", size=M_S, color=VIOLET).move_to(P(XS, -2.75))
        obs = always_redraw(lambda: Circle(radius=0.1, arc_center=P(XS + float(pill.dt.get_value()), 0.0)).set_stroke(WHITE, 2.5).set_fill(WHITE, 1).set_z_index(8))
        d1, q1 = row(eq(r"0<x<a", size=M_D, color=VIOLET), eqm(r"{{ Q_{\mathrm{env}} }} {{=}} {{ 2 }} {{ \rho }} {{ x }} {{ A }}", M_M), Yd, 1.9)
        self.add(env, cota_m, l2x, obs)
        self.play(FadeOut(rho), FadeIn(d1, shift=0.1 * UP), FadeIn(q1, shift=0.1 * UP), run_time=1.2)
        self.at(T_N13 + 13.0)
        s1 = col(gx(r"2EA=\frac{2\rho xA}{\varepsilon_0}", 11, cyan=(1,), blue=(5,)), Ya)
        self.play(FadeIn(s1, shift=0.1 * UP), run_time=1.0)
        # o fator 2 e a área A aparecem nos dois lados: riscados antes de sumir
        self.at(T_N13 + 15.0)
        self.play(*gind(s1, 0, 2, 4, 7), run_time=0.8)
        stk = gstrike(s1, 0, 2, 4, 7)
        self.play(Create(stk), run_time=0.6)
        self.at(T_N13 + 16.8)
        s2 = col(gx(r"E=\frac{\rho x}{\varepsilon_0}", 7, cyan=(0,), blue=(2,)), Ya)
        self.play(TransformByGlyphMap(s1, s2, *mv((1, 0), (3, 1), (5, 2), (6, 3), (8, 4), (9, 5), (10, 6)), ([0, 2, 4, 7], [])), FadeOut(stk), run_time=1.4)
        self.remove(s1)

        # o gráfico com os dois lados: agora a leitura é a componente E_x(x), com sinal; x também pode ser negativo
        self.at(T_N13 + 21.0)
        ax = Axes(x_range=[-3, 3, 1], y_range=[-1.2, 1.2, 1], x_length=5.4, y_length=2.0, tips=False,
                  axis_config={"color": WHITE, "stroke_width": 2, "include_ticks": False, "stroke_opacity": 0.8})
        ax.shift(P(4.0, -2.0) - ax.c2p(0, 0))
        fE = lambda u: u if abs(u) <= 1 else (1.0 if u > 0 else -1.0)
        hi, lo = [0.0], [0.0]
        xt = lambda: float(pill.dt.get_value()) / a

        def cur_r():
            hi[0] = max(hi[0], xt())
            us = np.linspace(0.0, max(hi[0], 1e-3), 80)
            return VMobject().set_points_as_corners([ax.c2p(u, fE(u)) for u in us]).set_stroke(CYAN, 5).set_z_index(4)

        def cur_l():
            lo[0] = min(lo[0], xt())
            us = np.linspace(min(lo[0], -1e-3), 0.0, 80)
            return VMobject().set_points_as_corners([ax.c2p(u, fE(u)) for u in us]).set_stroke(CYAN, 5).set_z_index(4)

        def marcador():
            u = xt()
            return VGroup(DashedLine(ax.c2p(u, 0), ax.c2p(u, fE(u)), dash_length=0.1).set_stroke(VIOLET, LW_THIN + 0.5, 0.9),
                          Circle(radius=0.11, arc_center=ax.c2p(u, fE(u))).set_stroke(WHITE, 2.5).set_fill(CYAN, 1).set_z_index(8))
        lab_x = eq(r"x/a", size=M_M).move_to(ax.c2p(2.85, 0) + P(0.1, 0.35))
        lab_y = eq(r"E_x/E_a", size=M_M).move_to(ax.c2p(0, 1.2) + P(0.85, 0.22))
        lab_norm = eq(r"E_a=E_x(a)", size=M_S).move_to(ax.c2p(-2.95, 1.0)).align_to(ax.c2p(-2.95, 0), LEFT)
        t1 = VGroup(DashedLine(ax.c2p(1, 0), ax.c2p(1, 1), dash_length=0.1).set_stroke(WHITE, LW_THIN, 0.4),
                    DashedLine(ax.c2p(-1, 0), ax.c2p(-1, -1), dash_length=0.1).set_stroke(WHITE, LW_THIN, 0.4),
                    eq("1", size=34).move_to(ax.c2p(1, 0) + P(0, -0.34)), eq("-1", size=34).move_to(ax.c2p(-1, 0) + P(0, 0.34)))
        s2x = col(gx(r"E_x(x)=\frac{\rho x}{\varepsilon_0}", 11, cyan=(0, 1), blue=(6,)), Ya)
        d1b, q1b = row(eq(r"|x|\le a", size=M_D, color=VIOLET), eqm(r"{{ Q_{\mathrm{env}} }} {{=}} {{ 2 }} {{ \rho }} {{ |x| }} {{ A }}", M_M), Yd, 1.9)
        l2xb = eq(r"2|x|", size=M_S, color=VIOLET).move_to(P(XS, -2.75))
        self.play(Create(ax), FadeIn(VGroup(lab_x, lab_y, lab_norm, t1)), TransformByGlyphMap(s2, s2x, *mv((0, 0), (1, 5), (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)), ([], [1, 2, 3, 4])), FadeOut(d1, shift=0.1 * UP),
                  TransformMatchingTex(q1, q1b), run_time=1.6)
        self.remove(s2)
        self.add(d1b)
        cr, cl, mk = always_redraw(cur_r), always_redraw(cur_l), always_redraw(marcador)
        for m in (cr, cl, mk):
            m.update()
        self.add(cr, cl, mk)
        self.remove(l2x)

        # variantes por estado: o ponto de observação decide qual domínio, carga e fórmula valem agora
        LA = ValueTracker(1.0)
        dtv = lambda: float(pill.dt.get_value())
        dom_pos = eq(r"x>a", size=M_D, color=VIOLET)
        dom_neg = eq(r"x<-a", size=M_D, color=VIOLET)
        q_out = eqm(r"{{ Q_{\mathrm{env}} }} {{=}} {{ 2 }} {{ \rho }} {{ a }} {{ A }}", M_M)
        res_pos = eqm(r"{{ E_x }} {{=}} \frac{ {{ \rho }} {{ a }} }{ {{ \varepsilon_0 }} }", M_L)
        res_neg = eqm(r"{{ E_x }} {{=}} -\frac{ {{ \rho }} {{ a }} }{ {{ \varepsilon_0 }} }", M_L)
        l2a = eq(r"2a", size=M_S, color=VIOLET).move_to(P(XS, -2.75))
        for m in (dom_pos, dom_neg):
            m.move_to(P(0, Yd)).align_to(P(RL, 0), LEFT)
        q_out.move_to(P(0, Yd)).align_to(P(RL + 1.9, 0), LEFT)
        col(res_pos, Ya)
        col(res_neg, Ya)
        n_neg = col(note("à esquerda, o campo aponta para −x"), Yn)
        n_zero = col(eq(r"E_x(0)=0", size=M_M, colors={0: CYAN}), Yn)
        n_fp = col(eq(r"E_x(+a)=\rho a/\varepsilon_0", size=M_M, colors={0: CYAN}), Yn)
        n_fm = col(eq(r"E_x(-a)=-\rho a/\varepsilon_0", size=M_M, colors={0: CYAN}), Yn)
        estados = [(d1b, lambda x: abs(x) <= a + 1e-6), (q1b, lambda x: abs(x) <= a + 1e-6), (s2x, lambda x: abs(x) <= a + 1e-6),
                   (l2xb, lambda x: abs(x) <= a + 1e-6),
                   (dom_pos, lambda x: x > a + 1e-6), (dom_neg, lambda x: x < -a - 1e-6), (q_out, lambda x: abs(x) > a + 1e-6),
                   (res_pos, lambda x: x > a + 1e-6), (res_neg, lambda x: x < -a - 1e-6), (l2a, lambda x: abs(x) > a + 1e-6),
                   (n_neg, lambda x: x < -0.03 and abs(x + a) >= 0.03), (n_zero, lambda x: abs(x) < 0.03),
                   (n_fp, lambda x: abs(x - a) < 0.03), (n_fm, lambda x: abs(x + a) < 0.03)]
        for m, pr in estados:
            m.add_updater(lambda mm, pr=pr: mm.set_opacity(float(LA.get_value()) if pr(dtv()) else 0.0))
            m.update()
            self.add(m)
        self.remove(l2x)
        self.wait(0.4)

        def ref_dot(u):
            return Circle(radius=0.075, arc_center=ax.c2p(u, fE(u))).set_stroke(WHITE, 1.5).set_fill(VIOLET, 1).set_z_index(7)

        # x = +a: a espessura envolvida chega ao máximo; os dois ramos coincidem
        self.at(T_N13 + 24.0)
        self.play(pill.dt.animate.set_value(a), run_time=3.0, rate_func=smooth)
        dot_p = ref_dot(1)
        self.play(Indicate(mk, color=WHITE, scale_factor=1.5), FadeIn(dot_p), run_time=1.2)
        self.wait(1.0)
        # x > a: toda a espessura está envolvida; o campo fica constante
        self.at(T_N13 + 30.0)
        self.play(pill.dt.animate.set_value(2.5 * a), run_time=4.5, rate_func=smooth)
        self.wait(1.2)
        # de volta ao centro: E_x(0) = 0
        self.at(T_N13 + 37.0)
        self.play(pill.dt.animate.set_value(0.0), run_time=4.0, rate_func=smooth)
        self.wait(2.0)
        # x = −a: o ramo interno e o externo coincidem também aqui
        self.at(T_N13 + 46.0)
        self.play(pill.dt.animate.set_value(-a), run_time=2.5, rate_func=smooth)
        dot_m = ref_dot(-1)
        self.play(Indicate(mk, color=WHITE, scale_factor=1.5), FadeIn(dot_m), run_time=1.2)
        self.wait(1.0)
        # x < −a: campo constante, agora no sentido −x
        self.at(T_N13 + 52.0)
        self.play(pill.dt.animate.set_value(-2.5 * a), run_time=3.5, rate_func=smooth)
        self.wait(1.5)
        # fecho: contínuo nas duas faces; o ponto volta ao lado direito, exterior
        self.at(T_N13 + 58.0)
        self.play(pill.dt.animate.set_value(2.0 * a), run_time=6.0, rate_func=smooth)
        n_c = col(note("contínuo em ±a: sem camada de carga", CYAN), Yn)
        self.play(FadeIn(n_c, shift=0.1 * UP), run_time=1.0)
        self.wait(1.0)
        for m, _ in estados:
            m.clear_updaters()
        for m in (cr, cl, mk, env, cota_m, obs, lat):
            m.clear_updaters()
        self.n13 = SimpleNamespace(junk=VGroup(tag, inf_n, ruler, xline, ax, cr, cl, mk, lab_x, lab_y, lab_norm, t1, dot_p, dot_m, env, cota_m, obs, lat, n_c,
                                               *[m for m, _ in estados]))
        self.at(T_N14)

    # ═══ N14 · duas folhas opostas / capacitor plano ideal (10:11–10:58) · COMPARE → BUILD: superposição ═══
    def n14_duas(self):
        self.begin(14, "duas_folhas")
        self.at(T_N14)
        pill, sh, n13 = self.pill, self.sh, self.n13
        w = SW
        x1, x2 = XS - 1.1, XS + 1.1
        s1, s2 = plane_body(x1, w), plane_body(x2, w, minus=True)
        tag = col(mix("DUAS FOLHAS · ", eq(r"+\sigma", size=M_S, color=BLUE_L), " e ", eq(r"-\sigma", size=M_S, color=BLUE_L)), Y_TAG)
        pill.vis.set_value(0.0)
        # troca de modelo (não há conservação de carga entre as duas configurações): a placa sai e as duas folhas entram
        n_mod = col(note("nova distribuição: duas folhas"), Y_DOM)
        self.play(FadeOut(n13.junk), FadeOut(sh), FadeIn(s1), FadeIn(s2), FadeIn(tag), FadeIn(n_mod, shift=0.1 * UP), run_time=2.0, rate_func=smooth)
        self.remove(pill.geom, pill.arrows)
        self.at(T_N14 + 3.5)
        # cada folha sozinha: |E| = σ/(2ε₀), saindo da positiva e entrando na negativa; três posições
        cols = (XS - 2.55, XS, XS + 2.55)
        L0 = 0.95

        def aux(cx, y, d):
            return vec(P(cx - d * L0 / 2, y), P(cx + d * L0 / 2, y), CYAN, LW_THIN + 1, 0.65, z=7)
        dirs_p = (-1, 1, 1)       # E₊ (afasta-se da folha +)
        dirs_m = (1, 1, -1)       # E₋ (aproxima-se da folha −)
        ap = [aux(cx, 0.6, d) for cx, d in zip(cols, dirs_p)]
        am = [aux(cx, -0.6, d) for cx, d in zip(cols, dirs_m)]
        lab_p = eq(r"E_{+}", size=M_S, color=CYAN).move_to(P(cols[0], 1.15))
        lab_m = eq(r"E_{-}", size=M_S, color=CYAN).move_to(P(cols[0], -1.15))
        m1 = col(eqm(r"{{ |E_{+}| }} {{=}} \frac{ {{ \sigma }} }{ {{ 2 }} {{ \varepsilon_0 }} }", M_L), Y_ACT)
        self.play(LaggedStart(*[FadeIn(x) for x in ap], lag_ratio=0.2), FadeIn(lab_p), FadeIn(m1, shift=0.1 * DOWN), run_time=1.6)
        self.at(T_N14 + 8.5)
        m2 = col(eqm(r"{{ |E_{+}| }} {{=}} {{ |E_{-}| }} {{=}} \frac{ {{ \sigma }} }{ {{ 2 }} {{ \varepsilon_0 }} }", M_M), Y_ACT)
        self.play(LaggedStart(*[FadeIn(x) for x in am], lag_ratio=0.2), FadeIn(lab_m), TransformMatchingTex(m1, m2), FadeOut(n_mod), run_time=1.6)
        # fora: sentidos opostos e módulos iguais ⇒ os dois vetores de cada lado se encontram e se anulam
        self.at(T_N14 + 14.0)
        zl = [eq("E=0", size=M_S, colors={0: CYAN}).move_to(P(cx, 0.0)) for cx in (cols[0], cols[2])]
        outs = VGroup(ap[0], am[0], ap[2], am[2])
        n_out = col(note("fora: mesmo módulo, sentidos opostos"), Y_DOM)
        self.play(*[Indicate(m, color=WHITE, scale_factor=1.1) for m in outs], FadeIn(n_out, shift=0.1 * UP), run_time=1.2)
        self.play(*[m.animate.move_to(P(cx, 0.07 * sg_)) for cx, pair in ((cols[0], (ap[0], am[0])), (cols[2], (ap[2], am[2]))) for m, sg_ in zip(pair, (1, -1))], run_time=0.9)
        self.play(FadeOut(outs), FadeOut(VGroup(lab_p, lab_m)), FadeIn(VGroup(*zl)), run_time=1.4)
        # entre as folhas: mesmo sentido ⇒ soma; cada parcela corresponde ao vetor da sua folha e a resultante é a soma dos dois
        self.at(T_N14 + 20.5)
        res_m = vec(P(cols[1] - L0, 0.0), P(cols[1] + L0, 0.0), CYAN, LW_RES + 1, z=8)
        n_in = col(note("entre as folhas: mesmo sentido, soma"), Y_DOM)
        f_out = col(eqm(r"{{ E_{\mathrm{fora}} }} {{=}} {{ 0 }}", M_M), Y_S1)
        f1 = col(gx(r"E_{\mathrm{entre}}=\frac{\sigma}{2\varepsilon_0}+\frac{\sigma}{2\varepsilon_0}", 18, size=M_M, cyan=(0, 1, 2, 3, 4, 5), blue=(7, 13)), Y_ACT)
        lab_p1 = eq(r"E_{+}", size=M_S, color=CYAN).move_to(P(cols[1], 1.15))
        lab_m1 = eq(r"E_{-}", size=M_S, color=CYAN).move_to(P(cols[1], -1.15))
        self.play(FadeOut(n_out), FadeIn(n_in, shift=0.1 * UP), FadeIn(f_out, shift=0.1 * UP), FadeOut(m2), FadeIn(f1, shift=0.1 * DOWN), FadeIn(VGroup(lab_p1, lab_m1)), run_time=1.4)
        self.at(T_N14 + 22.4)
        self.play(Indicate(VGroup(*[f1[0][i] for i in (7, 8, 9, 10, 11)]), color=WHITE, scale_factor=1.15), Indicate(ap[1], color=WHITE, scale_factor=1.15), run_time=1.0)
        self.play(Indicate(VGroup(*[f1[0][i] for i in (13, 14, 15, 16, 17)]), color=WHITE, scale_factor=1.15), Indicate(am[1], color=WHITE, scale_factor=1.15), run_time=1.0)
        self.at(T_N14 + 25.0)
        self.play(ap[1].animate.move_to(P(cols[1] - L0 / 2, 0.0)), am[1].animate.move_to(P(cols[1] + L0 / 2, 0.0)), run_time=1.0)
        self.play(ReplacementTransform(VGroup(ap[1], am[1]), res_m), FadeOut(VGroup(lab_p1, lab_m1)), run_time=0.8)
        self.at(T_N14 + 27.6)
        f2 = col(gx(r"E_{\mathrm{entre}}=\frac{\sigma}{\varepsilon_0}", 11, cyan=(0, 1, 2, 3, 4, 5), blue=(7,)), Y_ACT, dx=0.3)
        self.play(TransformByGlyphMap(f1, f2, *mv(*[(i, i) for i in range(9)]), *mv((10, 9), (11, 10)), ([9], []),
                                      ([12, 13, 14, 15, 16, 17], [], {"shift": P(-1.2, 0.0)})), run_time=1.4)
        self.remove(f1)
        f2_box = box(f2)
        self.play(Create(f2_box), run_time=0.8)
        # estado final: campo uniforme só no vão, do + para o −
        self.at(T_N14 + 32.5)
        gap = VGroup(*[vec(P(x1 + 0.45, y), P(x2 - 0.45, y), CYAN, LW_VEC, z=7) for y in (-1.3, -0.65, 0.0, 0.65, 1.3)])
        n_f = col(note("do + para o −: capacitor plano ideal"), Y_NOTE - 0.4)
        self.play(FadeOut(VGroup(*zl)), FadeOut(n_in), FadeOut(f_out), ReplacementTransform(res_m, gap), FadeIn(n_f, shift=0.1 * UP), run_time=1.6)
        self.at(T_N14 + 37.4)
        n_g = col(note("placas infinitas: sem efeitos de borda"), Y_NOTE - 1.1)
        self.play(FadeIn(n_g, shift=0.1 * UP), Indicate(gap, color=CYAN, scale_factor=1.1), run_time=1.4)
        self.n14 = SimpleNamespace(junk=VGroup(tag, f2, f2_box, n_f, n_g, gap), s1=s1, s2=s2)
        self.at(T_N15)

    # ═══ N15 · face de um condutor em equilíbrio e síntese planar (10:58–12:03) · SPLIT → FOCUS ═══
    def n15_condutor(self):
        self.begin(15, "condutor")
        self.at(T_N15)
        n14 = self.n14
        Yd, Ya, Yn = 2.0, 0.85, 0.05
        xc, wm = XS - 1.5, 1.5
        metal = plane_body(xc, wm, ncols=0, metal=True)
        surf_q = sign_col(XS, PY0 + SK + 0.1, PY1 - 0.2, False, s=0.09, color=WHITE, step=0.5, w=3).set_z_index(6)
        out_e = VGroup(*[vec(P(XS + 0.14, y), P(XS + 2.1, y), CYAN, LW_VEC, z=7) for y in (-1.5, 1.5)])
        pst = pill_static(XS - 0.6, XS + 0.6, 0.0, 1.0)
        cap_in_e = VGroup(*[vec(P(XS + 0.6, y), P(XS + 2.1, y), CYAN, LW_VEC, z=7) for y in YS_P])
        patch = patch_on(XS, 0.0, pr=PR)
        e_in = eq("E=0", size=M_L, colors={0: CYAN}).move_to(P(xc, 0.1))
        s_lab = eq(r"\sigma_{\mathrm{face}}", size=M_M, color=BLUE_L).move_to(P(XS + 0.95, 2.35))
        s_lead = Line(P(XS + 0.35, 2.15), P(XS + 0.05, 1.85)).set_stroke(BLUE_L, LW_THIN, 0.6)
        tag = col(label("FACE DE CONDUTOR · equilíbrio"), Y_TAG)
        # o plano vira a face de um condutor: metal à esquerda, vácuo à direita
        self.play(FadeOut(n14.junk), FadeOut(n14.s1), FadeOut(n14.s2), FadeIn(metal), FadeIn(surf_q), FadeIn(tag), run_time=2.0)
        self.at(T_N15 + 3.0)
        t_in = col(eqm(r"{{ E_{\mathrm{dentro}} }} {{=}} {{ 0 }}", M_L), Ya)
        n_in = col(note("dentro do metal em equilíbrio"), Yn)
        self.play(FadeIn(e_in), FadeIn(t_in, shift=0.1 * DOWN), FadeIn(n_in, shift=0.1 * UP), FadeIn(s_lab), Create(s_lead), run_time=1.4)
        self.at(T_N15 + 8.5)
        self.play(FadeIn(out_e, shift=0.05 * RIGHT), run_time=1.0)
        # pillbox curto atravessando a superfície: a tampa de dentro não contribui; só a de fora
        self.at(T_N15 + 12.0)
        a_lab = eq("A", size=M_S, color=VIOLET).move_to(P(XS + 0.6 + 0.45, PR + 0.3))
        self.play(FadeIn(pst), FadeIn(patch), FadeIn(a_lab), FadeOut(n_in), run_time=1.4)
        n_c = col(note("só a tampa de fora contribui"), Yn)
        self.play(FadeIn(cap_in_e), FadeOut(out_e), FadeIn(n_c, shift=0.1 * UP), run_time=1.2)
        self.at(T_N15 + 18.0)
        q = col(eqm(r"{{ Q_{\mathrm{env}} }} {{=}} {{ \sigma_{\mathrm{face}} }} {{ A }}", M_M), Yd)
        self.play(FadeIn(q, shift=0.1 * UP), Indicate(patch, color=WHITE, scale_factor=1.05), run_time=1.3)
        self.at(T_N15 + 22.0)
        g1 = col(eqm(r"{{ E }} {{ A }} {{=}} \frac{ {{ \sigma_{\mathrm{face}} }} {{ A }} }{ {{ \varepsilon_0 }} }", M_L), Ya)
        self.play(FadeOut(t_in), FadeIn(g1, shift=0.1 * DOWN), run_time=1.4)
        self.at(T_N15 + 27.0)
        As = [p for p in g1 if getattr(p, "tex_string", "").strip() == "A"]
        strikes = VGroup(*[strike(p, WHITE, 5) for p in As])
        self.play(Create(strikes), run_time=1.0)
        g2 = col(eqm(r"{{ E_{\mathrm{fora}} }} {{=}} \frac{ {{ \sigma_{\mathrm{face}} }} }{ {{ \varepsilon_0 }} }", M_L), Ya, dx=0.3)
        self.play(TransformMatchingTex(g1, g2), FadeOut(strikes), FadeOut(n_c), run_time=1.4)
        g2_box = box(g2)
        n_sup = col(VGroup(note("campo imediatamente", CYAN), note("fora da superfície", CYAN)).arrange(DOWN, aligned_edge=LEFT, buff=0.08), -0.55)
        self.play(Create(g2_box), FadeIn(n_sup, shift=0.1 * UP), run_time=0.8)
        # o fator 2: a folha isolante tem as duas tampas ativas; aqui só uma (σ_face é a densidade local desta face)
        self.at(T_N15 + 35.0)
        c1 = col(VGroup(note("folha isolante · duas tampas"), eq(r"E=\frac{\sigma}{2\varepsilon_0}", size=M_M, colors={0: CYAN})).arrange(DOWN, aligned_edge=LEFT, buff=0.2), 1.3)
        c2 = col(VGroup(note("face de condutor · uma tampa"), eq(r"E_{\mathrm{fora}}=\frac{\sigma_{\mathrm{face}}}{\varepsilon_0}", size=M_M, colors={0: CYAN})).arrange(DOWN, aligned_edge=LEFT, buff=0.2), -0.75)
        self.play(FadeOut(VGroup(q, g2_box, g2, n_sup)), run_time=0.8)
        self.play(FadeIn(c1, shift=0.1 * UP), run_time=1.1)
        self.at(T_N15 + 39.0)
        self.play(FadeIn(c2, shift=0.1 * UP), run_time=1.1)
        self.at(T_N15 + 41.5)
        n_f = col(note("mesma Lei de Gauss, outras hipóteses", CYAN), -2.1)
        self.play(FadeIn(n_f, shift=0.1 * UP), Indicate(c2, color=WHITE, scale_factor=1.03), run_time=1.2)

        # síntese planar: o mesmo pillbox em quatro fontes; muda Q_env e a região
        self.at(T_N15 + 48.0)
        left = VGroup(metal, surf_q, pst, patch, a_lab, cap_in_e, e_in, s_lab, s_lead, tag, c1, c2, n_f)
        self.play(FadeOut(left), run_time=1.0)
        icones = []
        xs, y0 = (-5.25, -1.75, 1.75, 5.25), 0.15
        for nome, x in zip(("folha", "placa", "duas folhas", "condutor"), xs):
            if nome == "folha":
                g = VGroup(plane_body(XS, SW, hint=False), pill_static(XS - 1.1, XS + 1.1, 1.0, 1.0))
            elif nome == "placa":
                g = VGroup(plane_body(XS, A_S, ncols=3, hint=False), pill_static(XS - 1.5, XS + 1.5, 1.0, 1.0))
            elif nome == "duas folhas":
                g = VGroup(plane_body(XS - 0.8, SW, hint=False), plane_body(XS + 0.8, SW, minus=True, hint=False), pill_static(XS - 1.7, XS - 0.1, 1.0, 1.0))
            else:
                g = VGroup(plane_body(XS - 1.0, 1.0, ncols=0, metal=True, hint=False), pill_static(XS - 0.55, XS + 0.55, 0.0, 1.0))
            g.scale(0.62).move_to(P(x, y0))
            nm = body(nome).move_to(P(x, y0 - 1.75))
            icones.append(VGroup(g, nm))
        hdr = hchain(title("o mesmo pillbox:"), eq(r"Q_{\mathrm{env}}", size=M_L), body("e a região mudam"), buff=0.35).move_to(P(0, 2.5))
        self.play(FadeIn(hdr, shift=0.1 * UP), LaggedStart(*[FadeIn(i, scale=0.94) for i in icones], lag_ratio=0.3), run_time=2.6)
        self.at(T_N15 + 56.5)
        # ponte para o capítulo esférico (não implementado nesta rodada)
        pergunta = VGroup(title("E quando a distribuição"), title("tem simetria esférica?")).arrange(DOWN, buff=0.25).move_to(P(0, -0.1))
        self.play(FadeOut(VGroup(*icones, hdr)), run_time=0.8)
        self.play(FadeIn(pergunta, shift=0.1 * UP), run_time=1.0)
        self.n15 = SimpleNamespace(pergunta=pergunta)
        self.at(T_N20)

    # ═══ N20 · casca esférica: o aparato (12:03–12:50) · SPLIT: simetria, esfera gaussiana e Φ = E·4πr² ═══
    def n20_casca_esf(self):
        self.begin(20, "casca_esferica")
        t0 = T_N20
        self.at(t0)
        R = RS
        shell = sph_shell(R)
        gs = GaussSph(2.0, ef_shell)
        self.gs = gs
        gs.gv.set_value(0.0)
        gs.ao.set_value(0.0)
        gs.add_to(self)
        tag = col(label("CASCA ESFÉRICA UNIFORME"), Y_TAG)
        q_lab = col(hchain(eq("Q", size=M_M, color=BLUE_L), note("carga total, uniforme na casca"), buff=0.3), Y_DOM)
        dim_R = rad_dim(R, "R", 67.5)
        self.play(FadeOut(self.n15.pergunta), run_time=0.6)
        self.play(FadeIn(shell), FadeIn(tag), FadeIn(dim_R), run_time=1.4)
        self.at(t0 + 3.5)
        self.play(FadeIn(q_lab, shift=0.1 * UP), run_time=1.0)
        # girar em torno do centro: toda rotação deixa a fonte igual
        self.at(t0 + 7.0)
        R1 = 2.0
        ang = ValueTracker(0.0)
        pp = always_redraw(lambda: Circle(radius=0.1, arc_center=SC0 + R1 * U(ang.get_value())).set_stroke(WHITE, 0).set_fill(WHITE, 1).set_z_index(8))
        rl = always_redraw(lambda: DashedLine(SC0, SC0 + R1 * U(ang.get_value()), dash_length=0.1).set_stroke(WHITE, LW_THIN + 0.5, 0.75))
        n_rot = col(note("girar: a fonte é a mesma"), Y_DOM)
        self.play(FadeOut(q_lab), FadeIn(n_rot, shift=0.1 * UP), FadeIn(VGroup(pp, rl)), run_time=1.0)
        self.play(ang.animate.set_value(360.0), run_time=5.0, rate_func=smooth)
        # só sobra o campo radial, que depende apenas da distância ao centro
        self.at(t0 + 14.5)
        pp.clear_updaters()
        rl.clear_updaters()
        e_rad = col(eqm(r"{{ \vec E }} {{=}} {{ E(r) }} {{ \,\hat r }}", M_L, {r"\vec E": CYAN, "E(r)": CYAN}), Y_ACT)
        n_rad = col(note("radial, só depende de r"), Y_NOTE)
        self.play(FadeOut(VGroup(pp, rl, n_rot)), gs.ao.animate.set_value(1.0), FadeIn(e_rad, shift=0.1 * DOWN), FadeIn(n_rad, shift=0.1 * UP), run_time=1.6)
        # só agora a esfera gaussiana concêntrica: matemática, não material
        self.at(t0 + 21.0)
        lab_g = col(label("superfície gaussiana", VIOLET), Y_TAG)
        self.play(FadeOut(tag), FadeOut(n_rad), gs.gv.animate.set_value(1.0), gs.dv.animate.set_value(1.0), run_time=1.6)
        self.play(FadeIn(lab_g, shift=0.1 * UP), run_time=0.6)
        # em todos os pontos: mesmo módulo e E paralelo à normal exterior
        self.at(t0 + 26.0)
        pt = SC0 + 2.0 * U(0)
        n_v = vec(pt + P(0, 0.2), pt + P(0.6, 0.2), NHAT, LW_N, z=10)
        n_lab = eq(r"\hat n", size=M_S, color=NHAT).move_to(pt + P(0.9, 0.42))
        e_par = col(eqm(r"{{ \vec E }} {{ \parallel }} {{ \hat n }}", M_L), Y_ACT)
        self.play(FadeOut(e_rad), FadeIn(VGroup(n_v, n_lab)), FadeIn(e_par, shift=0.1 * DOWN), run_time=1.3)
        self.at(t0 + 31.0)
        n_all = col(note("toda a superfície contribui"), Y_NOTE)
        phi = col(eqm(r"{{ \Phi }} {{=}} {{ E }} {{ 4\pi }} {{ r^{2} }}", M_L), Y_ACT)
        self.play(FadeOut(e_par), run_time=0.5)
        self.play(FadeIn(phi, shift=0.1 * DOWN), FadeIn(n_all, shift=0.1 * UP), Indicate(gs.geom, color=VIOLET, scale_factor=1.02), run_time=1.3)
        # a pergunta que decide os ramos: a gaussiana envolve a casca ou ainda está dentro dela?
        self.at(t0 + 37.0)
        n_q = col(note("a gaussiana envolve a casca?", VIOLET), Y_NOTE)
        self.play(FadeOut(n_all), FadeIn(n_q, shift=0.1 * UP), gs.rt.animate.set_value(0.66), run_time=2.4, rate_func=smooth)
        self.play(gs.rt.animate.set_value(2.0), run_time=2.4, rate_func=smooth)
        self.n20 = SimpleNamespace(junk=VGroup(lab_g, phi, n_q, n_v, n_lab), shell=shell, dim_R=dim_R)
        self.at(T_N21)

    # ═══ N21 · casca esférica: as regiões (12:50–13:31) · COMPARE: dentro × fora ═══
    def n21_regioes(self):
        self.begin(21, "regioes")
        t0 = T_N21
        self.at(t0)
        gs, n20 = self.gs, self.n20
        R = RS
        gs.efun = ef_shell
        self.play(FadeOut(n20.junk), run_time=0.8)
        tag = col(label("CASCA ESFÉRICA · duas regiões"), Y_TAG)
        # por dentro: nada envolvido; Gauss + simetria esférica ⇒ E = 0 (não vale para qualquer superfície vazia)
        d1, q1 = row(eq(r"r<R", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=0", size=M_M), Y_DOM)
        self.play(gs.rt.animate.set_value(0.6), FadeIn(tag), FadeIn(d1, shift=0.1 * UP), FadeIn(q1, shift=0.1 * UP), run_time=2.4, rate_func=smooth)
        self.at(t0 + 4.0)
        e1 = col(eq("E", "=0", size=M_L, colors={0: CYAN}), Y_ACT)
        n1 = col(note("por Gauss + simetria esférica"), Y_NOTE)
        self.play(FadeIn(e1, shift=0.1 * UP), FadeIn(n1, shift=0.1 * UP), run_time=1.0)
        # por fora: toda a carga da casca; a esfera cresce e a carga envolvida passa a ser Q
        self.at(t0 + 9.0)
        d2, q2 = row(eq(r"r>R", size=M_D, color=VIOLET), eqm(r"{{ Q_{\mathrm{env}} }} {{=}} {{ Q }}", M_M), Y_DOM)
        s1d, s1e = row(eq(r"r<R", size=M_D, color=VIOLET), eq("E", "=0", size=M_M, colors={0: CYAN}), Y_S1)
        s1 = VGroup(s1d, s1e)
        seg = Circle(radius=R, arc_center=SC0).set_stroke(BLUE_L, 8, 0.9).set_z_index(5.6)
        self.play(gs.rt.animate.set_value(2.1), FadeIn(seg), FadeOut(VGroup(e1, n1)), FadeIn(s1), ReplacementTransform(d1, d2),
                  TransformMatchingTex(q1, q2), run_time=2.8, rate_func=smooth)
        self.at(t0 + 13.0)
        f1 = col(eqm(r"{{ E }} {{ 4\pi }} {{ r^{2} }} {{=}} \frac{ {{ Q }} }{ {{ \varepsilon_0 }} }", M_L), Y_ACT)
        self.play(FadeIn(f1, shift=0.1 * UP), run_time=1.0)
        self.at(t0 + 16.5)
        f2 = col(eqm(r"{{ E }} {{=}} \frac{ {{ Q }} }{ {{ 4\pi }} {{ \varepsilon_0 }} {{ r^{2} }} }", M_L), Y_ACT, dx=0.3)
        self.play(TransformMatchingTex(f1, f2), run_time=1.3)
        f2_box = box(f2)
        self.play(Create(f2_box), FadeOut(seg), run_time=0.8)
        # fora, a casca equivale a uma carga pontual no centro (só para pontos externos)
        self.at(t0 + 21.0)
        pt_q = VGroup(Circle(radius=0.3, arc_center=SC0).set_stroke(width=0).set_fill(BLUE, 0.3), q_dot(SC0, r=0.2)).set_z_index(5)
        ghost = DashedVMobject(Circle(radius=R, arc_center=SC0), num_dashes=40, dashed_ratio=0.55).set_stroke(BLUE_L, 3, 0.5).set_z_index(5)
        q_lab = eq("Q", size=M_S, color=BLUE_L).move_to(SC0 + P(0.62, -0.42))
        n_eq = col(mix("mesmo campo para ", eq(r"r>R", size=M_S, color=VIOLET), size=T_NOTE, op=0.95, color=CYAN), Y_NOTE - 0.25)
        self.play(FadeOut(n20.shell), FadeIn(ghost), FadeIn(pt_q, scale=0.5), FadeIn(q_lab), FadeIn(n_eq, shift=0.1 * UP), run_time=1.6)
        self.at(t0 + 26.0)
        self.play(FadeOut(pt_q), FadeOut(q_lab), FadeOut(ghost), FadeIn(n20.shell), FadeOut(n_eq), run_time=1.4)
        # a camada carregada: o campo salta de zero para um valor não nulo
        self.at(t0 + 29.5)
        s2d, s2e = row(eq(r"r>R", size=M_D, color=VIOLET), eq("E", "=", r"\frac{Q}{4\pi\varepsilon_0 r^{2}}", size=M_M, colors={0: CYAN}), Y_S2)
        s2 = VGroup(s2d, s2e)
        jump = col(eq(r"E(R^-)=0", r"\neq", r"E(R^+)", size=M_L, colors={0: CYAN, 2: CYAN}), Y_ACT)
        n_j = col(note("salto na camada carregada"), Y_NOTE)
        self.play(FadeOut(VGroup(f2, f2_box)), FadeIn(s2), gs.rt.animate.set_value(R - 0.12), run_time=1.2)
        self.play(FadeIn(jump, shift=0.1 * UP), FadeIn(n_j, shift=0.1 * UP), run_time=0.9)
        self.play(Indicate(n20.shell, color=BLUE_L, scale_factor=1.02), gs.rt.animate.set_value(R + 0.12), run_time=1.4)
        self.at(t0 + 35.0)
        self.play(gs.rt.animate.set_value(R - 0.12), run_time=1.0)
        self.play(gs.rt.animate.set_value(R + 0.12), run_time=1.0)
        self.at(t0 + 39.5)
        self.play(gs.rt.animate.set_value(2.1), run_time=1.2)
        self.n21 = SimpleNamespace(junk=VGroup(tag, d2, q2, s1, s2, jump, n_j))
        self.at(T_N22)

    # ═══ N22 · esfera maciça: revisão e comparação (13:31–14:37) · SPLIT: gráfico sincronizado ═══
    def n22_macico_esf(self):
        self.begin(22, "macico_esf")
        t0 = T_N22
        self.at(t0)
        gs, n20, n21 = self.gs, self.n20, self.n21
        R = RS
        solid = sph_solid(R)
        lat = lattice_sph(gs)
        env = env_sph(gs)
        tag = col(mix("ISOLANTE · ", eq(r"\rho", size=34, color=BLUE_L), " constante"), Y_TAG)
        gs.efun = ef_ssolid
        # a casca ganha volume: já vimos este caso no primeiro vídeo; recuperar o raciocínio sem refazer dV
        self.add(lat)
        self.play(FadeOut(n21.junk), FadeOut(n20.shell), FadeOut(n20.dim_R), FadeIn(solid), FadeIn(tag), run_time=1.8)
        self.at(t0 + 3.0)
        h_in, q_in = row(eq(r"r<R", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=\frac{4}{3}\pi\rho r^{3}", size=M_M), Y_DOM)
        self.add(env)
        self.play(gs.rt.animate.set_value(0.72), FadeIn(h_in, shift=0.1 * UP), FadeIn(q_in, shift=0.1 * UP), run_time=2.6, rate_func=smooth)
        self.play(Indicate(gs.lab, color=VIOLET, scale_factor=1.3), run_time=0.8)
        # carga ∝ r³, área ∝ r²: o campo cresce linearmente. O 4π cancela (dos dois lados); depois a divisão por r² (r³/r² = r)
        self.at(t0 + 8.0)
        s1 = col(gx(r"E4\pi r^{2}=\frac{4\pi\rho r^{3}}{3\varepsilon_0}", 15, cyan=(0,), blue=(8,), violet=(3, 9)), Y_ACT)
        self.play(FadeIn(s1, shift=0.1 * UP), run_time=1.0)
        self.at(t0 + 9.3)
        a1 = col(eq(r"\div\,4\pi", size=M_M), Y_NOTE)
        self.play(FadeIn(a1, shift=0.1 * UP), *gind(s1, 1, 2, 6, 7), run_time=0.9)
        stk1 = gstrike(s1, 1, 2, 6, 7)
        self.at(t0 + 10.4)
        self.play(Create(stk1), run_time=0.6)
        self.at(t0 + 11.3)
        sa = col(gx(r"Er^{2}=\frac{\rho r^{3}}{3\varepsilon_0}", 11, cyan=(0,), blue=(4,), violet=(1, 5)), Y_ACT)
        self.play(TransformByGlyphMap(s1, sa, *mv((0, 0), (3, 1), (4, 2), (5, 3), (8, 4), (9, 5), (10, 6), (11, 7), (12, 8), (13, 9), (14, 10)),
                                      ([1, 2, 6, 7], [])), FadeOut(stk1), FadeOut(a1), run_time=1.3)
        self.remove(s1)
        self.at(t0 + 12.9)
        a2 = col(hchain(eq(r"\div\,r^{2}", size=M_M), eq(r"(r>0)", size=M_S), buff=0.3), Y_NOTE)
        self.play(FadeIn(a2, shift=0.1 * UP), Indicate(VGroup(sa[0][1], sa[0][2]), color=WHITE, scale_factor=1.3), run_time=0.9)
        self.at(t0 + 14.1)
        sm = col(gx(r"E=\frac{\rho r^{3}}{3\varepsilon_0 r^{2}}", 11, cyan=(0,), blue=(2,), violet=(3, 9)), Y_ACT)
        self.play(TransformByGlyphMap(sa, sm, *mv((0, 0), (1, 9), (2, 10), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5), (8, 6), (9, 7), (10, 8))), FadeOut(a2), run_time=1.2)
        self.remove(sa)
        self.at(t0 + 15.6)
        a3 = col(eq(r"r^{3}\div r^{2}=r", size=M_M), Y_NOTE)
        stk2 = gstrike(sm, 4, 9, 10)
        self.play(FadeIn(a3, shift=0.1 * UP), Create(stk2), run_time=0.8)
        self.at(t0 + 16.6)
        s2 = col(gx(r"E=\frac{\rho r}{3\varepsilon_0}", 8, cyan=(0,), blue=(2,), violet=(3,)), Y_ACT)
        self.play(TransformByGlyphMap(sm, s2, *mv((0, 0), (1, 1), (2, 2), (3, 3), (5, 4), (6, 5), (7, 6), (8, 7)), ([4, 9, 10], [])), FadeOut(stk2), FadeOut(a3), run_time=1.3)
        self.remove(sm)
        self.play(Indicate(s2, color=CYAN, scale_factor=1.05), run_time=0.8)
        # fora: a carga envolvida para de crescer; a área continua crescendo; R³ é fixo e r² vai para o denominador
        self.at(t0 + 19.5)
        res_in = VGroup(eq(r"r<R", size=M_D, color=VIOLET).move_to(P(0, Y_S1)).align_to(P(RL, 0), LEFT), s2)
        h_out, q_out = row(eq(r"r>R", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=\frac{4}{3}\pi\rho R^{3}", size=M_M), Y_DOM)
        self.play(s2.animate.scale(0.8).move_to(P(0, Y_S1)).align_to(P(RL + 1.3, 0), LEFT).set_opacity(OP_PREV), FadeIn(res_in[0]),
                  ReplacementTransform(h_in, h_out), TransformMatchingTex(q_in, q_out), gs.rt.animate.set_value(2.0), run_time=3.0, rate_func=smooth)
        self.at(t0 + 23.5)
        t1 = col(gx(r"E4\pi r^{2}=\frac{4\pi\rho R^{3}}{3\varepsilon_0}", 15, cyan=(0,), blue=(8, 9), violet=(3,)), Y_ACT)
        self.play(FadeIn(t1, shift=0.1 * UP), run_time=1.0)
        self.at(t0 + 24.8)
        b1 = col(eq(r"\div\,4\pi", size=M_M), Y_NOTE)
        self.play(FadeIn(b1, shift=0.1 * UP), *gind(t1, 1, 2, 6, 7), run_time=0.9)
        stk3 = gstrike(t1, 1, 2, 6, 7)
        self.play(Create(stk3), run_time=0.6)
        self.at(t0 + 26.8)
        ta = col(gx(r"Er^{2}=\frac{\rho R^{3}}{3\varepsilon_0}", 11, cyan=(0,), blue=(4, 5), violet=(1,)), Y_ACT)
        self.play(TransformByGlyphMap(t1, ta, *mv((0, 0), (3, 1), (4, 2), (5, 3), (8, 4), (9, 5), (10, 6), (11, 7), (12, 8), (13, 9), (14, 10)),
                                      ([1, 2, 6, 7], [])), FadeOut(stk3), FadeOut(b1), run_time=1.3)
        self.remove(t1)
        self.at(t0 + 28.4)
        b2 = col(hchain(eq(r"\div\,r^{2}", size=M_M), eq(r"(r>0)", size=M_S), buff=0.3), Y_NOTE)
        self.play(FadeIn(b2, shift=0.1 * UP), Indicate(VGroup(ta[0][1], ta[0][2]), color=WHITE, scale_factor=1.3), run_time=0.9)
        self.at(t0 + 29.6)
        t3 = col(gx(r"E=\frac{\rho R^{3}}{3\varepsilon_0 r^{2}}", 11, cyan=(0,), blue=(2, 3), violet=(9,)), Y_ACT)
        self.play(TransformByGlyphMap(ta, t3, *mv((0, 0), (1, 9), (2, 10), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5), (8, 6), (9, 7), (10, 8))), FadeOut(b2), run_time=1.4)
        self.remove(ta)

        # gráfico sincronizado: E/E_R × r/R; marcador, esfera gaussiana, região envolvida e leis mudam juntos em r = R
        self.at(t0 + 32.5)
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 1.2, 1], x_length=5.0, y_length=3.0, tips=False,
                  axis_config={"color": WHITE, "stroke_width": 2, "include_ticks": False, "stroke_opacity": 0.8})
        ax.shift(P(1.7, -2.15) - ax.c2p(0, 0))
        fu = lambda u: u if u <= 1 else 1 / u ** 2
        ux = lambda: min(gs.r() / R, 3.0)

        def curva():
            us = np.linspace(0.0, max(ux(), 1e-3), 100)
            return VMobject().set_points_as_corners([ax.c2p(x, fu(x)) for x in us]).set_stroke(CYAN, 5).set_z_index(4)

        def marcador():
            u = ux()
            return VGroup(DashedLine(ax.c2p(u, 0), ax.c2p(u, fu(u)), dash_length=0.1).set_stroke(VIOLET, LW_THIN + 0.5, 0.9),
                          Circle(radius=0.09, arc_center=ax.c2p(u, fu(u))).set_stroke(WHITE, 2).set_fill(CYAN, 1).set_z_index(6))
        lab_x = eq(r"r/R", size=M_M).move_to(ax.c2p(2.85, 0) + P(0.1, -0.4))
        lab_y = eq(r"E/E_R", size=M_M).move_to(ax.c2p(0, 1.18) + P(0.25, 0.25)).align_to(P(RL + 0.1, 0), LEFT)
        lab_norm = eq(r"E_R=E(R)", size=34).move_to(P(6.15, 1.25))
        tick1 = VGroup(DashedLine(ax.c2p(1, 0), ax.c2p(1, 1), dash_length=0.1).set_stroke(WHITE, LW_THIN, 0.4),
                       eq("1", size=34).move_to(ax.c2p(1, 0) + P(0, -0.32)), eq("1", size=34).move_to(ax.c2p(0, 1) + P(-0.28, 0)))
        live = []
        for expr, cx, dentro in ((r"Q_{\mathrm{env}}\propto r^{3}", RL, True), (r"Q_{\mathrm{env}}=\text{constante}", RL, False),
                                 (r"E\propto r", RL + 3.7, True), (r"E\propto\frac{1}{r^{2}}", RL + 3.7, False)):
            m = eq(expr, size=34).move_to(P(0, 2.75)).align_to(P(cx, 0), LEFT)
            if expr.startswith("E"):
                m.set_color(CYAN)
            m.add_updater(lambda mm, d=dentro: mm.set_opacity(1.0 if (gs.r() < R - 1e-3) == d else 0.0))
            live.append(m)
        lab_lin = eq("E", "=", r"\frac{\rho r}{3\varepsilon_0}", size=34, colors={0: CYAN}).move_to(ax.c2p(0.5, 1.12) + P(1.0, 0.1))
        n_0 = note("no centro, E = 0 por simetria", CYAN).move_to(P(0, 2.05)).align_to(P(RL, 0), LEFT)
        self.play(FadeOut(VGroup(h_out, q_out, res_in, t3, tag)), gs.rt.animate.set_value(0.04), Create(ax), FadeIn(VGroup(lab_x, lab_y, lab_norm, tick1)),
                  FadeIn(n_0, shift=0.1 * UP), run_time=1.8, rate_func=smooth)
        curve, mark = always_redraw(curva), always_redraw(marcador)
        for m in live:
            m.update()
        self.add(curve, mark, *live)
        self.at(t0 + 35.0)
        self.play(FadeOut(n_0), run_time=0.5)
        self.at(t0 + 36.0)
        self.play(gs.rt.animate.set_value(R), run_time=3.4, rate_func=smooth)
        # em r = R: pausa; os dois ramos se encontram (não há camada de carga na borda)
        n_c = note("contínuo em R: sem camada de carga", CYAN).move_to(P(0, 2.12)).align_to(P(RL, 0), LEFT)
        eq_c = eq(r"E(R^{-})", "=", r"E(R^{+})", size=M_M, colors={0: CYAN, 2: CYAN}).move_to(P(0, 1.62)).align_to(P(RL, 0), LEFT)
        self.play(Indicate(mark, color=WHITE, scale_factor=1.6), FadeIn(lab_lin, shift=0.1 * UP), FadeIn(n_c, shift=0.1 * UP), run_time=1.4)
        # atravessar r = R: a gaussiana, o marcador, as leis, a carga envolvida e as setas mudam juntos e E não salta
        self.play(gs.rt.animate.set_value(R - 0.14), FadeIn(eq_c, shift=0.1 * UP), run_time=1.0, rate_func=smooth)
        self.play(gs.rt.animate.set_value(R + 0.14), run_time=1.2, rate_func=smooth)
        self.at(t0 + 43.0)
        self.play(gs.rt.animate.set_value(2.2 * R), run_time=4.0, rate_func=smooth)
        self.wait(0.8)
        # comparação com o cilindro maciço (normalizado em R): mesmas variáveis, caudas diferentes
        self.at(t0 + 49.0)
        cyl_c = VMobject().set_points_as_corners([ax.c2p(u, 1 / u) for u in np.linspace(1, 2.2, 60)]).set_stroke(WHITE, 4, 0.9).set_z_index(3)
        lab_cyl = eq(r"1/r", size=34).move_to(ax.c2p(2.2, 1 / 2.2) + P(0.5, 0.2))
        lab_sph = eq(r"1/r^{2}", size=34, color=CYAN).move_to(ax.c2p(2.2, 1 / 4.84) + P(0.55, 0.1))
        n_cyl = label("cilindro", WHITE, op=1.0).move_to(ax.c2p(1.75, 1 / 1.75) + P(0.1, 0.55))
        n_sph = label("esfera", CYAN, op=1.0).move_to(ax.c2p(1.85, 1 / 1.85 ** 2) + P(-0.1, -0.42))
        n_n = mix("cada curva usa seu próprio ", eq("E(R)", size=M_S), size=T_NOTE, op=0.92).move_to(P(0, 2.05)).align_to(P(RL, 0), LEFT)
        self.play(FadeOut(n_c), FadeOut(eq_c), run_time=0.45)
        self.play(FadeIn(cyl_c), FadeIn(lab_cyl), FadeIn(lab_sph), FadeIn(n_cyl), FadeIn(n_sph), FadeIn(n_n, shift=0.1 * UP), run_time=1.6)
        self.at(t0 + 55.0)
        self.play(gs.rt.animate.set_value(R), run_time=1.4, rate_func=smooth)
        self.play(gs.rt.animate.set_value(1.8), run_time=1.4, rate_func=smooth)
        curve.clear_updaters()
        mark.clear_updaters()
        for m in live:
            m.clear_updaters()
        self.n22 = SimpleNamespace(junk=VGroup(ax, curve, mark, lab_x, lab_y, lab_norm, tick1, lab_lin, cyl_c, lab_cyl, lab_sph, n_n, n_cyl, n_sph, *live),
                                   solid=solid, lat=lat, env=env)
        self.at(T_N23)

    # ═══ N23 · capacitor esférico (14:37–15:27) · COMPARE → BUILD, com holofote por região ═══
    def n23_capacitor_esf(self):
        self.begin(23, "capacitor_esf")
        t0 = T_N23
        self.at(t0)
        gs, n22 = self.gs, self.n22
        a, b = RS, BS
        core = sph_solid(a, metal=True)
        core_s = VGroup(*[sign(SC0 + a * U(an), s=0.09, color=WHITE, w=3) for an in range(0, 360, 30)]).set_z_index(5)
        outer = sph_shell(b, minus=True, inner=True, metal=True)
        dm_in, dm_out = Dimmer(VGroup(core, core_s)), Dimmer(outer)
        dim_a, dim_b = rad_dim(a, "a", 67.5), rad_dim(b, "b", 112.5, frac=0.9)
        gap_e = VGroup(*[vec(SC0 + r_ * U(an), SC0 + (r_ + 0.9 / r_ ** 2) * U(an), CYAN, LW_VEC, z=7)
                         for an, r_ in ((0, 1.35), (90, 1.35), (180, 1.35), (270, 1.35), (45, 1.75), (135, 1.75), (225, 1.75), (315, 1.75))])
        tag = col(mix("CONDUTORES · ", eq(r"+Q", size=M_S, color=BLUE_L), " e ", eq(r"-Q", size=M_S, color=BLUE_L)), Y_TAG)
        gs.efun = ef_none
        # troca de modelo, dita: o isolante vira condutor maciço (a carga vai para a superfície); entra a casca externa, de carga oposta
        self.play(FadeOut(n22.junk), FadeOut(n22.solid), FadeOut(n22.lat), FadeOut(n22.env), FadeIn(core), FadeIn(core_s), FadeIn(tag), FadeIn(dim_a), run_time=1.8)
        k1 = col(hchain(eq(r"+Q", size=M_M, color=BLUE_L), note("núcleo condutor maciço"), buff=0.3), Y_DOM)
        self.play(FadeIn(k1, shift=0.1 * UP), run_time=0.9)
        self.at(t0 + 5.0)
        k2 = col(hchain(eq(r"-Q", size=M_M, color=BLUE_L), note("casca condutora delgada"), buff=0.3), Y_DOM - 0.9)
        self.play(FadeIn(outer), FadeIn(dim_b), FadeIn(k2, shift=0.1 * UP), run_time=1.8)
        # r < a: dentro do metal, nada envolvido e E = 0
        self.at(t0 + 10.0)
        env = env_sph(gs, top=lambda r: r if r <= a else (a if r <= b else 0.02))
        d1, q1 = row(eq(r"r<a", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=0", size=M_M), Y_DOM, 1.5)
        self.add(env)
        self.play(gs.rt.animate.set_value(0.6), FadeOut(VGroup(k1, k2)), dm_out.to(0.3), FadeIn(d1, shift=0.1 * UP), FadeIn(q1, shift=0.1 * UP),
                  run_time=2.4, rate_func=smooth)
        e1 = col(eq("E", "=0", size=M_L, colors={0: CYAN}), Y_ACT)
        n1 = col(note("dentro do metal"), Y_NOTE)
        self.play(FadeIn(e1, shift=0.1 * UP), FadeIn(n1, shift=0.1 * UP), run_time=0.9)
        # a < r < b: a esfera gaussiana envolve +Q; o campo aparece no vão
        self.at(t0 + 16.0)
        d2, q2 = row(eq(r"a<r<b", size=M_D, color=VIOLET), eqm(r"{{ Q_{\mathrm{env}} }} {{=}} {{ Q }}", M_M), Y_DOM, 1.9)
        r1d, r1e = row(eq(r"r<a", size=M_D, color=VIOLET), eq("E", "=0", size=M_M, colors={0: CYAN}), Y_S2, 1.5)
        r1 = VGroup(r1d, r1e)
        gs.efun = ef_none
        self.play(gs.rt.animate.set_value(1.7), dm_in.to(0.55), dm_out.to(0.55), FadeOut(VGroup(e1, n1)), FadeIn(r1), ReplacementTransform(d1, d2),
                  TransformMatchingTex(q1, q2), FadeIn(gap_e, shift=0.05 * RIGHT), run_time=2.4, rate_func=smooth)
        e2 = col(eq("E", "=", r"\frac{Q}{4\pi\varepsilon_0 r^{2}}", size=M_L, colors={0: CYAN}), Y_ACT)
        self.play(FadeIn(e2, shift=0.1 * UP), run_time=1.0)
        # r > b: as cargas envolvidas se cancelam; campo externo nulo; confinado ao vão
        self.at(t0 + 24.5)
        d3, q3 = row(eq(r"r>b", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=Q-Q=0", size=M_M), Y_DOM, 1.2)
        r2d, r2e = row(eq(r"a<r<b", size=M_D, color=VIOLET), eq("E", "=", r"\frac{Q}{4\pi\varepsilon_0 r^{2}}", size=M_M, colors={0: CYAN}), Y_S1, 1.9)
        r2 = VGroup(r2d, r2e)
        gs.efun = ef_none
        self.play(gs.rt.animate.set_value(2.65), dm_in.to(0.5), dm_out.to(0.85), FadeOut(e2), FadeIn(r2), ReplacementTransform(d2, d3),
                  TransformMatchingTex(q2, q3), run_time=2.4, rate_func=smooth)
        e3 = col(eq("E", "=0", size=M_L, colors={0: CYAN}), Y_ACT)
        n3 = col(note("campo confinado ao vão", CYAN), Y_NOTE)
        self.play(FadeIn(e3, shift=0.1 * UP), FadeIn(n3, shift=0.1 * UP), run_time=0.9)
        self.at(t0 + 33.0)
        self.play(dm_in.to(1.0), dm_out.to(1.0), Indicate(gap_e, color=CYAN, scale_factor=1.15), run_time=1.2)
        self.play(Indicate(gap_e, color=CYAN, scale_factor=1.15), run_time=1.2)
        self.at(t0 + 38.0)
        self.n23 = SimpleNamespace(junk=VGroup(tag, d3, q3, e3, n3, r1, r2), all=VGroup(core, core_s, outer, dim_a, dim_b, gap_e), env=env)
        self.at(T_N24)

    # ═══ N24 · três capacitores (15:27–16:09) · COMPARE em sequência → FOCUS ═══
    def n24_tres_cap(self):
        self.begin(24, "tres_capacitores")
        t0 = T_N24
        self.at(t0)
        gs, n23 = self.gs, self.n23
        # o capacitor esférico grande sai por inteiro; a gaussiana também (não há mais superfície em jogo)
        self.play(FadeOut(n23.junk), FadeOut(n23.all), gs.gv.animate.set_value(0.0), gs.dv.animate.set_value(0.0), gs.ao.animate.set_value(0.0), run_time=1.0)
        self.remove(n23.env, gs.geom, gs.arrows, gs.dimr, gs.lab)
        XL, XM, XR = -4.8, 0.0, 4.8
        CY = 0.95
        pl = co_plates(XL, CY, k=1.0)
        cx_ = self.cap_round(XM, CY, expo=1, metal_core=True, equator=False)
        sp = self.cap_round(XR, CY, expo=2, metal_core=True, equator=True)
        names = [label("placas paralelas").move_to(P(x, -1.9)) for x in (XL,)] + [label("cabo coaxial (corte)").move_to(P(XM, -1.9)), label("capacitor esférico").move_to(P(XR, -1.9))]
        laws = [eq("E", r"=\text{constante}", size=M_M, colors={0: CYAN}).move_to(P(XL, -1.25)),
                eq("E", r"\propto \frac{1}{r}", size=M_M, colors={0: CYAN}).move_to(P(XM, -1.1)),
                eq("E", r"\propto \frac{1}{r^{2}}", size=M_M, colors={0: CYAN}).move_to(P(XR, -1.1))]
        gap_tag = label("no vão entre os condutores", CYAN).move_to(P(0, 2.55))
        # um caso por vez: a lei, no vão
        self.play(FadeIn(pl.src, shift=0.1 * UP), FadeIn(gap_tag, shift=0.1 * UP), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(a) for a in pl.fld], lag_ratio=0.1), FadeIn(laws[0], shift=0.1 * UP), FadeIn(names[0]), run_time=1.4)
        self.at(t0 + 8.0)
        self.play(FadeIn(cx_.src), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(a) for a in cx_.fld], lag_ratio=0.08), FadeIn(laws[1], shift=0.1 * UP), FadeIn(names[1]), run_time=1.4)
        self.at(t0 + 16.0)
        self.play(FadeIn(sp.src), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(a) for a in sp.fld], lag_ratio=0.08), FadeIn(laws[2], shift=0.1 * UP), FadeIn(names[2]), run_time=1.4)
        # fora dos três, no modelo escolhido: cargas iguais e opostas, sem fonte externa
        self.at(t0 + 24.0)
        out_n = note("fora dos três, no modelo escolhido: E = 0").move_to(P(0, -2.6))
        self.play(FadeIn(out_n, shift=0.1 * UP), run_time=1.0)
        # não são três leis: são três formas de simplificar a mesma Lei de Gauss
        self.at(t0 + 31.0)
        un = title("três geometrias, a mesma Lei de Gauss").move_to(P(0, 2.55))
        tri = VGroup(pl.src, pl.fld, cx_.src, cx_.fld, sp.src, sp.fld)
        self.play(FadeOut(gap_tag), FadeOut(out_n), run_time=0.5)
        self.play(tri.animate.shift(0.3 * DOWN), VGroup(*laws, *names).animate.shift(0.3 * DOWN), FadeIn(un, shift=0.1 * UP), run_time=1.4)
        self.n24 = SimpleNamespace(junk=VGroup(tri, *laws, *names, un))
        self.at(T_N25)

    def cap_round(self, cx, cy, expo, metal_core=True, equator=False):
        """Capacitor em corte transversal: núcleo condutor (+), casca externa (−) e E⃗ radial só no vão, com comprimento ∝ 1/r^expo."""
        c = P(cx, cy)
        a, b = 0.48, 1.32
        core = VGroup(Circle(radius=a, arc_center=c).set_stroke(width=0).set_fill(BLUE_L, 0.28), Circle(radius=a, arc_center=c).set_stroke(BLUE, 10, 0.3),
                      Circle(radius=a, arc_center=c).set_stroke(BLUE_L, 4), *[sign(c + a * U(an), s=0.07, w=2.6) for an in range(0, 360, 45)])
        shell = VGroup(Circle(radius=b, arc_center=c).set_stroke(BLUE, 12, 0.3), Circle(radius=b, arc_center=c).set_stroke(BLUE_L, 4),
                       *[sign(c + (b - 0.09) * U(an), True, s=0.07, w=2.6) for an in range(0, 360, 30)])
        src = VGroup(core, shell)
        if equator:
            src.add(arc(cx, cy, a, 180, 360, BLUE_L, 2.5, 0.6), arc(cx, cy, b, 180, 360, BLUE_L, 2.5, 0.5),
                    Ellipse(width=0.3, height=0.16).rotate(0.6).move_to(c + a * P(-0.45, 0.5)).set_stroke(width=0).set_fill(WHITE, 0.3))
        src.set_z_index(5)
        fld = VGroup()
        for an, r0 in ((0, 0.6), (90, 0.6), (180, 0.6), (270, 0.6), (45, 0.86), (135, 0.86), (225, 0.86), (315, 0.86)):
            ln = 0.5 * (0.6 / r0) ** expo
            fld.add(vec(c + r0 * U(an), c + (r0 + ln) * U(an), CYAN, LW_VEC, z=7))
        return SimpleNamespace(src=src, fld=fld)

    # ═══ N25 · área, carga fixa e potências (16:09–17:01) · BUILD → FOCUS ═══
    def n25_areas(self):
        self.begin(25, "areas")
        t0 = T_N25
        self.at(t0)
        n24 = self.n24
        R1, R2, R3 = 1.55, 0.35, -0.85
        tag = col(note("área que contribui para o fluxo"), Y_TAG)
        tag2 = col(mix("com ", eq(r"Q_{\mathrm{env}}", size=M_S, color=BLUE_L), " fixo", size=T_LABEL, op=0.9), 2.15)
        # esfera: a área cresce com r²; com a carga envolvida fixa, o campo cai na mesma proporção
        shell = sph_shell(RS)
        gs2 = GaussSph(1.55, ef_shell)
        gs2.dv.set_value(1.0)
        gs2.add_to(self)
        gs2.gv.set_value(0.0)
        gs2.ao.set_value(0.0)
        t_a1 = col(eq(r"4\pi r^{2}", size=M_M, color=VIOLET), R1)
        t_r1 = eq(r"\rightarrow\ E\propto\frac{1}{r^{2}}", size=M_M, colors={0: WHITE}).move_to(P(0, R1)).next_to(t_a1, RIGHT, buff=0.3)
        self.play(FadeOut(n24.junk), FadeIn(shell), gs2.gv.animate.set_value(1.0), gs2.ao.animate.set_value(1.0), FadeIn(tag), FadeIn(tag2), FadeIn(t_a1, shift=0.1 * UP), run_time=1.8)
        self.at(t0 + 4.0)
        self.play(gs2.rt.animate.set_value(2.65), run_time=4.5, rate_func=smooth)
        self.play(FadeIn(t_r1, shift=0.1 * LEFT), run_time=0.9)
        self.play(gs2.rt.animate.set_value(1.55), run_time=1.6, rate_func=smooth)
        # cilindro: a área lateral cresce com r (L escolhido); a carga envolvida naquele trecho é fixa
        self.at(t0 + 15.0)
        wire = wire_line()
        gc2 = GaussCyl(0.9, ef_line)
        gc2.dv.set_value(1.0)
        gc2.diml.set_opacity(0.0)
        t_a2 = col(eq(r"2\pi rL", size=M_M, color=VIOLET), R2)
        t_r2 = eq(r"\rightarrow\ E\propto\frac{1}{r}", size=M_M).next_to(t_a2, RIGHT, buff=0.3)
        gcg = VGroup(gc2.geom, gc2.arrows, gc2.dimr, gc2.lab)
        gc2.vis.set_value(0.0)
        gc2.add_to(self)
        self.play(FadeOut(shell), FadeOut(gs2.geom), FadeOut(gs2.arrows), FadeOut(gs2.dimr), FadeOut(gs2.lab), FadeIn(wire), gc2.vis.animate.set_value(1.0),
                  FadeIn(t_a2, shift=0.1 * UP), run_time=1.8)
        self.remove(gs2.geom, gs2.arrows, gs2.dimr, gs2.lab)
        self.at(t0 + 18.0)
        self.play(gc2.rt.animate.set_value(2.1), run_time=4.0, rate_func=smooth)
        self.play(FadeIn(t_r2, shift=0.1 * LEFT), run_time=0.9)
        self.play(gc2.rt.animate.set_value(0.9), run_time=1.4, rate_func=smooth)
        # plano: afastar as tampas não aumenta a área delas (nem a carga envolvida)
        self.at(t0 + 29.0)
        sheet = plane_body(XS, SW)
        pill = Pill(0.6, ef_sheet)
        pill.vis.set_value(0.0)
        pill.cs.set_value(1.0)
        pill.add_to(self)
        inside = patch_on(XS, SW)
        t_a3 = col(eq("2A", size=M_M, color=VIOLET), R3)
        t_r3 = eq(r"\rightarrow\ E=\text{constante}", size=M_M).next_to(t_a3, RIGHT, buff=0.3)
        self.play(FadeOut(wire), FadeOut(VGroup(gc2.geom, gc2.arrows, gc2.dimr, gc2.lab)), FadeIn(sheet), FadeIn(inside), pill.vis.animate.set_value(1.0),
                  FadeIn(t_a3, shift=0.1 * UP), run_time=1.8)
        self.remove(gc2.geom, gc2.arrows, gc2.dimr, gc2.lab)
        self.at(t0 + 32.0)
        self.play(pill.dt.animate.set_value(2.6), run_time=4.0, rate_func=smooth)
        self.play(FadeIn(t_r3, shift=0.1 * LEFT), run_time=0.9)
        self.play(pill.dt.animate.set_value(0.6), run_time=1.6, rate_func=smooth)
        # só vale com simetria e carga envolvida fixa; por dentro dos maciços a carga envolvida também cresce
        self.at(t0 + 41.0)
        stamp = col(note("só com simetria e carga envolvida fixa", CYAN), -1.9)
        caut = col(VGroup(note("dentro dos maciços,"), mix(eq(r"Q_{\mathrm{env}}", size=M_S, color=BLUE_L), " cresce com o raio", size=T_NOTE, op=0.92)).arrange(DOWN, aligned_edge=LEFT, buff=0.1), -2.65)
        self.play(FadeIn(stamp, shift=0.1 * UP), run_time=1.0)
        self.at(t0 + 45.0)
        self.play(FadeIn(caut, shift=0.1 * UP), run_time=1.0)
        self.n25 = SimpleNamespace(junk=VGroup(tag, tag2, t_a1, t_r1, t_a2, t_r2, t_a3, t_r3, stamp, caut, sheet, inside, pill.geom, pill.arrows))
        self.at(T_N26)

    # ═══ N26 · checklist aplicado (17:01–17:59) · FOCUS → BUILD: seis perguntas aplicadas ao cilindro maciço ═══
    def n26_checklist(self):
        self.begin(26, "checklist")
        t0 = T_N26
        self.at(t0)
        n25 = self.n25
        R = R_VIS
        corpo = solid_body(R)
        g3 = GaussCyl(R + 0.6, ef_solid)
        g3.vis.set_value(0.0)
        lat = lattice_dyn(g3)
        env = env_overlay(g3)
        tag = col(label("antes da integral: seis perguntas"), 2.9)
        qs = [mix("1   qual a simetria da fonte?", size=T_BODY, op=1.0),
              mix("2   direção possível de ", eq(r"\vec E", size=M_S, color=CYAN), "?", size=T_BODY, op=1.0),
              mix("3   de que depende ", eq(r"|\vec E|", size=M_S, color=CYAN), "?", size=T_BODY, op=1.0),
              mix("4   qual superfície fechada serve?", size=T_BODY, op=1.0),
              mix("5   quanto vale ", eq(r"Q_{\mathrm{env}}", size=M_S, color=BLUE_L), " ?", size=T_BODY, op=1.0),
              mix("6   preciso dividir em regiões?", size=T_BODY, op=1.0)]
        ys = [2.3, 1.7, 1.1, 0.5, -0.1, -0.7]
        for q, y in zip(qs, ys):
            col(q, y)
        self.add(g3.geom, g3.arrows, g3.dimr, g3.lab)
        # 1 · a fonte (cilindro maciço isolante, ρ constante): simetria cilíndrica
        self.play(FadeOut(n25.junk), FadeIn(corpo), FadeIn(lat), FadeIn(tag), FadeIn(qs[0], shift=0.1 * UP), run_time=1.8)
        # 2 · direção de E: radial
        self.at(t0 + 9.0)
        e_src = VGroup(*[vec(P(AX + sg * R, y), P(AX + sg * (R + 0.8), y), CYAN, LW_VEC, z=7) for sg in (-1, 1) for y in YS_ARR])
        self.play(FadeIn(qs[1], shift=0.1 * UP), FadeIn(e_src), qs[0].animate.set_opacity(OP_PREV), run_time=1.3)
        # 3 · dependência: só de r
        self.at(t0 + 17.0)
        rl = DashedLine(P(AX, -1.7), P(AX + 1.5, -1.7), dash_length=0.1).set_stroke(WHITE, LW_THIN + 0.5, 0.75)
        rlab = eq("r", size=M_S, color=VIOLET).move_to(P(AX + 0.75, -2.0))
        self.play(FadeIn(qs[2], shift=0.1 * UP), FadeIn(VGroup(rl, rlab)), qs[1].animate.set_opacity(OP_PREV), run_time=1.3)
        # 4 · superfície: o cilindro coaxial; E constante na lateral, tangente nas tampas
        self.at(t0 + 25.0)
        self.play(FadeOut(VGroup(rl, rlab)), FadeOut(e_src), FadeIn(qs[3], shift=0.1 * UP), qs[2].animate.set_opacity(OP_PREV), g3.vis.animate.set_value(1.0),
                  g3.dv.animate.set_value(1.0), run_time=1.6)
        # 5 · carga envolvida: a parte da fonte dentro da gaussiana
        self.at(t0 + 33.0)
        self.add(env)
        self.play(FadeIn(qs[4], shift=0.1 * UP), qs[3].animate.set_opacity(OP_PREV), g3.rt.animate.set_value(0.5), run_time=2.2, rate_func=smooth)
        # 6 · regiões: por dentro usa r (volume envolvido); por fora usa R (a fonte inteira)
        self.at(t0 + 40.0)
        d1, q1 = row(eq(r"r<R", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=\rho\pi r^{2}L", size=M_M), -1.55, 1.3)
        self.play(FadeIn(qs[5], shift=0.1 * UP), qs[4].animate.set_opacity(OP_PREV), FadeIn(d1, shift=0.1 * UP), FadeIn(q1, shift=0.1 * UP), run_time=1.2)
        self.at(t0 + 46.0)
        d2, q2 = row(eq(r"r>R", size=M_D, color=VIOLET), eq(r"Q_{\mathrm{env}}=\rho\pi R^{2}L", size=M_M), -2.35, 1.3)
        self.play(g3.rt.animate.set_value(1.6), FadeIn(d2, shift=0.1 * UP), FadeIn(q2, shift=0.1 * UP), run_time=3.0, rate_func=smooth)
        # a superfície foi reaproveitada; a carga mudou
        self.at(t0 + 53.0)
        n_r = col(note("mesma superfície; a carga mudou", CYAN), 2.9)
        self.play(FadeOut(tag), FadeIn(n_r, shift=0.1 * UP), qs[5].animate.set_opacity(1.0), run_time=1.0)
        self.n26 = SimpleNamespace(junk=VGroup(n_r, *qs, d1, q1, d2, q2, corpo, lat, env, g3.geom, g3.arrows, g3.dimr, g3.lab))
        self.at(T_N27)

    # ═══ N27–N29 · payoff, pausa e CTA / outro (17:59–…) · FOCUS / END SCREEN (mesmo sistema do yt_0001) ═══
    def n27_payoff_outro(self):
        self.begin(27, "payoff_outro")
        t0 = T_N27
        self.at(t0)
        n26 = self.n26
        # payoff: tela limpa, sem header; o watermark fica discreto
        p1 = display("IDENTIFIQUE A SIMETRIA DA FONTE", 40).move_to(P(0, 0.55))
        p2 = display("SUPERFÍCIE ÚTIL → CARGA ENVOLVIDA → CAMPO", 36)
        p2.scale_to_fit_width(min(p2.width, 13.6)).move_to(P(0, -0.4))
        self.play(FadeOut(n26.junk), FadeOut(self.tag), run_time=1.2)
        self.play(FadeIn(p1, shift=0.12 * UP), run_time=1.2)
        self.at(t0 + 5.0)
        self.play(FadeIn(p2, shift=0.12 * UP), run_time=1.4)
        self.at(T_N28)
        # pausa de 2 s sem conteúdo novo: com voz, o áudio ganha 2 s de silêncio antes do CTA (pads.json); sem voz, a cena espera
        if VOZ:
            self.respiro(voz(T_N29), 2.0)
        else:
            self.wait(2.0)
        # outro: logo horizontal oficial centralizado, mensagem curta e anéis tracejados com movimento discreto
        self.at(T_N29)
        oc = P(0, 0.2)
        rings = VGroup(*[DashedVMobject(Circle(radius=r_, arc_center=oc), num_dashes=int(14 * r_), dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.16) for r_ in (2.0, 3.0, 4.0)])
        for i, r_ in enumerate(rings):
            r_.add_updater(lambda m, dt, s_=(1 if i % 2 == 0 else -1) * (0.06 - 0.01 * i): m.rotate(s_ * dt, about_point=oc))
        logo = ImageMobject(str(LOGO_PATH)).set_width(6.0).move_to(P(0, 0.6))
        msg = text("Inscreva-se para acompanhar os próximos vídeos", 28, opacity=0.9).move_to(P(0, -1.0))
        self.play(FadeOut(VGroup(p1, p2)), FadeOut(self.wm), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(r_, scale=0.85) for r_ in rings], lag_ratio=0.3), FadeIn(logo, scale=0.92), run_time=1.8)
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=1.0)

        def ripple():
            w = DashedVMobject(Circle(radius=1.6, arc_center=oc), num_dashes=24, dashed_ratio=0.6).set_stroke(VIOLET, 3.5, 0.35)
            self.play(w.animate.scale(2.6, about_point=oc).set_stroke(opacity=0.0), run_time=2.6)
            self.remove(w)
        self.at(T_N29 + 8.0)
        ripple()
        self.at(T_N29 + 14.0)
        ripple()
        self.at(T_FIM)
