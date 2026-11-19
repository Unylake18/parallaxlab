"""yt_0012 — Por que a corrente resiste a mudar? (indutância e energia magnética). V2 visual/didática.

Preview visual silencioso, 960×540 / 15 fps. Storyboard C01–C20 (ver ficha.md). V1 em cena_v1_backup.py.

Um aparato só (bateria + chave + solenoide + resistor), desenhado a cada quadro a partir de trackers:
  tc = t/τ da carga     → I = 1 − e^{−tc}, dI/dt = e^{−tc}, B = I, ℰ_L = −e^{−tc}, U_B = I², P_J = I², P_L = I·dI/dt
  td = t/τ da descarga  → I = e^{−td}, dI/dt = −e^{−td}, ℰ_L = +e^{−td}, U_B = P_R = e^{−2td}, Q_R = 1 − e^{−2td}
  sp (só C06)           → corrente imposta (sobe, constante, desce) e sua derivada analítica
(unidades: I_∞ ou I₀ = 1, I_∞/τ = 1, ℰ₀ = 1). Gráficos, campo, cargas, fem, medidores e brilho leem o mesmo estado.

Solenoide, bobina secundária, capacitor e superfícies de Ampère são objetos 3D projetados (2.5D): a vista gira em torno
do eixo vertical (tracker `ang`), o que permite passar da vista lateral ao corte axial (C10) com o mesmo objeto.
Cores: corrente verde (#3FE08B, como vid_0009/yt_0010) · E induzido / ℰ_L ciano · B, Λ, U_B magenta · τ, t violeta ·
calor laranja · resto branco. Corrente horária; B dentro do solenoide = +x (na vista axial, saindo da tela).
Equações: `Eq` de string única + TransformByGlyphMap (MF-Tools), como no vid_0010/vid_0011.
`SO=3,5-7` renderiza só essas cenas (as outras são puladas, o estado é construído).
"""
import json
import math
import os
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import (
    AnimationGroup, Arrow, Axes, Brace, Circle, Create, DashedLine, DashedVMobject, Dot, FadeIn, FadeOut,
    ImageMobject, LaggedStart, Line, ManimColor, MathTex, Mobject, Polygon, Rectangle, ReplacementTransform,
    RoundedRectangle, Scene, Square, SurroundingRectangle, TransformFromCopy, TransformMatchingTex, VGroup, VMobject,
    ValueTracker, always_redraw, config, interpolate_color, linear, smooth, DOWN, LEFT, RIGHT, UP, UL, UR, DL, PI,
)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from MF_Tools import TransformByGlyphMap  # noqa: E402
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import screen_text  # noqa: E402

PASTA = Path(__file__).resolve().parent

# ── paleta ───────────────────────────────────────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR        # campo elétrico induzido, ℰ_L, ℰ₂, E_φ
GREEN = "#3FE08B"           # corrente: cargas, setas, I (padrão do vid_0009 / yt_0010)
MAGENTA = "#EA63FF"         # B, Λ, U_B, u_B
VIOLET = "#9C8CFF"          # tempo, τ (violeta clareado, como no vid_0011)
HEAT = "#FF7A3D"            # calor: P_R, P_Joule, E_calor, Q_R (único tom quente, como no yt_0010)
STEEL = "#7A8696"           # fios
COIL = "#C3CDE0"            # espiras da frente
COIL_B = "#56607A"          # espiras de trás
GEO = "#7FB2FF"             # geometria: A, ℓ, V, n, N₂, r, a (azul = geometria, como vid_0010/vid_0011)
DIM = "#8FA3C4"

T_HEAD, T_TAG, T_DESC = 30, 20, 24
M_XL, M_L, M_M, M_S = 54, 46, 38, 30

# ── tempos provisórios (a voz será escrita depois sobre estes tempos; retimar aqui) ───────────────────────────
T_FADE = 0.8     # entrada/saída de texto
T_MOVE = 1.8     # mudança de composição
T_EQ = 1.3       # entrada de equação
T_MORPH = 2.0    # transformação de equação (mapa de glifos)
T_BEAT = 1.2     # respiro curto
T_READ = 3.5     # pausa de leitura
T_HOLD = 5.5     # pausa longa (payoff)
T_RUN = 10.0     # transitório completo (0 → 5τ)
T_SW = 0.9       # movimento da chave

TOK = {   # partes que levam a cor da grandeza inteira (rótulo + índice)
    r"\mathcal E_L": CYAN, r"\mathcal E_2": CYAN, r"\mathcal E_1": CYAN, r"\mathcal E_0": CYAN, r"E_\phi": CYAN,
    "U_B": MAGENTA, "U_B(t)": MAGENTA, "U_{B,0}": MAGENTA, "u_B": MAGENTA, "dU_B": MAGENTA,
    "P_R": HEAT, "P_R(t)": HEAT, r"P_{\rm Joule}": HEAT, r"E_{\rm calor}": HEAT, "Q_R(t)": HEAT,
}

# Cor por variável, reconhecida pela forma do glifo (vale dentro de frações, expoentes e índices).
# Sequências (variável + índice) primeiro; depois símbolos isolados, em tamanho normal, de índice e de índice de índice.
VAR_SEQ = [(r"\mathcal E_0", CYAN), (r"\mathcal E_L", CYAN), (r"\mathcal E_1", CYAN), (r"\mathcal E_2", CYAN),
           ("I_0", GREEN), (r"I_\infty", GREEN), ("I_1", GREEN), ("I_2", GREEN), (r"\Lambda_2", MAGENTA),
           (r"\Lambda_1", MAGENTA), ("U_{B,0}", MAGENTA), ("U_B", MAGENTA), ("u_B", MAGENTA), ("N_2", GEO),
           ("P_R", HEAT), ("Q_R", HEAT), ("M_{12}", WHITE), ("M_{21}", WHITE)]
VAR_ONE = [(r"\mathcal E", CYAN), ("E", CYAN), ("I", GREEN), ("R", HEAT), (r"\tau", VIOLET), ("t", VIOLET),
           ("B", MAGENTA), (r"\mathbf B", MAGENTA), (r"\Lambda", MAGENTA), (r"\Phi", MAGENTA), ("Q", HEAT),
           ("A", GEO), (r"\ell", GEO), ("V", GEO), ("n", GEO), ("N", GEO), ("r", GEO), ("a", GEO)]
_REF = {}


def _norm(gl):
    p = gl.points[:, :2]
    c = np.array([(gl.get_left()[0] + gl.get_right()[0]) / 2, (gl.get_top()[1] + gl.get_bottom()[1]) / 2])
    return (p - c) / max(gl.height, 1e-6)


def _glyphs(m):
    return [g for g in m.family_members_with_points()]


def _refs():
    if _REF:
        return _REF
    seqs = []
    for t, c in VAR_SEQ:
        seqs.append(([_norm(g) for g in _glyphs(MathTex(t, font_size=48))], c))
    seqs.sort(key=lambda x: -len(x[0]))
    ones = []
    for t, c in VAR_ONE:
        for w in (t, "x_{" + t + "}", "x_{x_{" + t + "}}"):
            ones.append((_norm(_glyphs(MathTex(w, font_size=48))[-1]), c))
    _REF["seq"], _REF["one"] = seqs, ones
    return _REF


def _same(a, b):
    return a.shape == b.shape and np.allclose(a, b, atol=0.03)


def paint(m):
    """Pinta cada variável da expressão com a cor da grandeza (convenção dos vídeos longos)."""
    ref = _refs()
    gl = _glyphs(m)
    nm = [_norm(g) for g in gl]
    done = [False] * len(gl)
    for seq, c in ref["seq"]:
        k = len(seq)
        for i in range(len(gl) - k + 1):
            if not any(done[i:i + k]) and all(_same(nm[i + j], seq[j]) for j in range(k)):
                for j in range(k):
                    gl[i + j].set_color(c)
                    done[i + j] = True
    for i, g in enumerate(gl):
        if done[i]:
            continue
        for r, c in ref["one"]:
            if _same(nm[i], r):
                g.set_color(c)
                break
    return m

# ── geometria local do aparato (tela = C + s·(p − F)); profundidade z para fora da tela ─────────────────────────
XL, XA, XB = -4.2, -3.4, -2.6        # bateria, contato a, pivô da chave / ramo de desvio
XS0, XS1, XR = -1.3, 1.9, 3.6        # solenoide (início, fim), resistor
YT, YB = 1.3, -1.3                   # fio de cima (eixo do solenoide), fio de baixo
A_R, NT = 0.5, 9                     # raio do solenoide, espiras desenhadas
XC = 0.5 * (XS0 + XS1)
ANG0 = -0.42                         # vista lateral: giro em torno do eixo vertical (rad); −π/2 = vista axial (B ⊙)
ELEV = 0.17                          # leve elevação da câmera (cisalhamento vertical ∝ profundidade)
LBL = 0.8                            # comprimento da lâmina da chave
SW_OPEN, SW_A, SW_B = 145.0, 180.0, 270.0
XM0, XM1, A2, NT2 = -0.15, 0.75, 0.82, 3            # bobina secundária coaxial
YMET, MR = YT + 1.8, 0.3             # medidor / fonte da secundária
XP0, XP1, PH = XC - 0.24, XC + 0.24, 0.55           # capacitor (C20): placas quadradas de meia-aresta PH
XAMP, RAMP = -0.75, 0.78             # anel amperiano (C20)
XIA = 0.9                            # centro da seta de corrente no fio de baixo
SPD = 0.55                           # espaçamento das cargas no percurso

LAYOUTS = {                          # (s, cx, cy, fx, fy)
    "full": (1.1, 0.0, -0.4, -0.3, 0.1),
    "left": (0.9, -3.75, -0.45, -0.3, 0.1),
    "mut": (0.85, -3.55, -1.05, -0.3, 0.1),
    "solo": (1.6, -3.0, 0.0, XC, YT),
    "soloc": (1.9, 0.0, 0.45, XC, YT),
    "cells": (1.2, -2.7, -0.1, XC, YT),
    "axial": (2.0, -3.6, -0.35, XC, YT),
}
EQX = 3.95                           # centro da coluna da direita
GC = (3.95, -0.7)                    # centro do gráfico padrão


def _sel(s):
    out = set()
    for p in s.split(","):
        p = p.strip()
        if "-" in p:
            a, b = p.split("-")
            out.update(range(int(a), int(b) + 1))
        elif p:
            out.add(int(p))
    return out


SEL = _sel(os.environ.get("SO", ""))


def P3(x, y):
    return np.array([x, y, 0.0])


# ── texto (Space Grotesk via screen_text, como no vid_0010) ──────────────────────────────────────────────────
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
        t = screen_text(content, size, oversample=2)
    return t.set_color(color).set_opacity(opacity)


def tag(content, size=T_TAG, color=WHITE, opacity=0.85):
    """Rótulo curto em CAIXA ALTA (componentes, manchetes de painel)."""
    return text(content.upper(), size, color, opacity)


def desc(content, size=T_DESC, color=DIM, opacity=1.0):
    """Descrição curta em minúsculas (definições de variáveis, passos), como no vid_0011."""
    return text(content, size, color, opacity)


def tex(s, size=M_M, color=None):
    if color is not None:
        return MathTex(s, font_size=size, color=color)
    return paint(MathTex(s, font_size=size, color=TOK.get(s, WHITE)))


def row(*ms, buff=0.16):
    return VGroup(*ms).arrange(RIGHT, buff=buff)


def fitw(m, w=6.6):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def boxed(m, color=WHITE, buff=0.18, width=2.5):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=width, corner_radius=0.08)


def soft_swap(old, new, shift=UP * 0.12):
    """A velha sai, depois a nova entra (nunca se cruzam)."""
    return AnimationGroup(FadeOut(old, shift=shift), FadeIn(new, shift=shift), lag_ratio=1.0)


def arrow(a, b, color=WHITE, width=5, z=8, tip=0.2, op=1.0):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if np.linalg.norm(b - a) < 0.03:
        return VMobject()
    m = Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.45,
              max_stroke_width_to_length_ratio=50)
    return m.set_opacity(op).set_z_index(z)


def redraw(func):
    """Como always_redraw, mas troca os submobjetos a cada quadro em vez de `become()`: o desenho muda de estrutura
    o tempo todo e o alinhamento de famílias do `become()` faria o objeto engordar quadro a quadro."""
    m = VGroup()

    def upd(x):
        x.submobjects = [func()]
    m.add_updater(upd)
    upd(m)
    return m


def multi(paths):
    """Um VMobject com vários subcaminhos poligonais (pontos já em coordenadas de tela)."""
    m = VMobject()
    for p in paths:
        if len(p) < 2:
            continue
        m.start_new_path(p[0])
        m.add_points_as_corners(p[1:])
    return m


def hull(pts):
    """Fecho convexo (cadeia monótona) de pontos 2D."""
    p = sorted(set(map(tuple, np.round(np.asarray(pts)[:, :2], 5))))
    if len(p) < 3:
        return np.array(p)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for q in p:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(p):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    return np.array(lo[:-1] + up[:-1])


def probe(s):
    """C06: corrente imposta (sobe, constante, desce). Retorna (I, dI/dt normalizado, máx. 1)."""
    if s <= 0:
        return 0.0, 0.0
    if s < 1:
        return 0.5 * (1 - math.cos(PI * s)), math.sin(PI * s)
    if s < 2:
        return 1.0, 0.0
    if s < 3:
        return 0.5 * (1 + math.cos(PI * (s - 2))), -math.sin(PI * (s - 2))
    return 0.0, 0.0


# ── equações com índices de glifos (MF-Tools), como no vid_0010 ──────────────────────────────────────────────
class Eq:
    """MathTex de string única + índices de glifos por parte, para TransformByGlyphMap. Cores por parte (TOK)."""

    def __init__(self, *parts, size=M_L, colors=None):
        multi_ = MathTex(*parts, font_size=size)
        self.s = np.concatenate([[0], np.cumsum([len(q) for q in multi_])]).astype(int)
        self.mob = paint(MathTex(" ".join(parts), font_size=size, color=WHITE))
        assert len(self.mob[0]) == int(self.s[-1]), parts
        cols = {i: TOK[p] for i, p in enumerate(parts) if p in TOK}
        cols.update(colors or {})
        for i, c in cols.items():
            self.mob[0][int(self.s[i]):int(self.s[i + 1])].set_color(c)

    def p(self, *ids):
        return [k for i in ids for k in range(int(self.s[i]), int(self.s[i + 1]))]

    def g(self, *ids):
        return [self.mob[0][k] for k in self.p(*ids)]

    def px(self, i):
        return sorted(self.p(i), key=lambda k: self.mob[0][k].get_center()[0])

    def frac(self, i):
        """Numerador / barra / denominador de uma fração da parte i (só glifos sob a barra contam)."""
        idx, gl = self.p(i), self.mob[0]
        bar = max(idx, key=lambda k: gl[k].width)
        x0, x1, yb = gl[bar].get_left()[0] - 0.02, gl[bar].get_right()[0] + 0.02, gl[bar].get_center()[1]
        ins = [k for k in idx if k != bar and x0 <= gl[k].get_center()[0] <= x1]
        num = sorted((k for k in ins if gl[k].get_center()[1] > yb), key=lambda k: gl[k].get_center()[0])
        den = sorted((k for k in ins if gl[k].get_center()[1] < yb), key=lambda k: gl[k].get_center()[0])
        return num, bar, den

    def at(self, x, y):
        self.mob.move_to(P3(x, y))
        return self


def _first_half(t):
    return smooth(min(1.0, 2 * t))


def _second_half(t):
    return smooth(max(0.0, 2 * t - 1))


def copy_from(src):
    """Introdutor: o destino nasce de uma CÓPIA dos glifos `src`, que ficam onde estão."""
    class _Copy(TransformFromCopy):
        def __init__(self, mob, **kw):
            super().__init__(VGroup(*src), mob, **kw)
    return _Copy


def MP(A, pa, B, pb, **kw):
    """Partes pa de A viram partes pb de B."""
    return (A.p(*pa), B.p(*pb), kw)


def MG(ga, gb, **kw):
    return (list(ga), list(gb), kw)


def CP(src, B, pb, **kw):
    kw.setdefault("rate_func", _second_half)          # a cópia só parte depois que o termo antigo saiu
    return (copy_from(src), B.p(*pb), kw)


def CG(src, gb, **kw):
    kw.setdefault("rate_func", _second_half)
    return (copy_from(src), list(gb), kw)


class Trilha:
    """Percurso das cargas: pontos locais (x, y, z, h). h = 1 na hélice (projetada a cada quadro), 0 nos fios."""

    def __init__(self, pts):
        self.p = np.asarray(pts, float)
        d2 = np.linalg.norm(np.diff(self.p[:, :2], axis=0), axis=1)
        d3 = np.linalg.norm(np.diff(self.p[:, :3], axis=0), axis=1)
        hel = (self.p[1:, 3] > 0.5) & (self.p[:-1, 3] > 0.5)
        self.c = np.concatenate([[0.0], np.cumsum(np.where(hel, d3, d2))])
        self.L = self.c[-1]

    def at(self, s):
        return [np.interp(s, self.c, self.p[:, k]) for k in range(4)]


def helix3(x0, x1, yc, r, nt, th0=-PI / 2, n_per=40):
    """Hélice 3D: corrente avançando em θ; na frente (z > 0) desce ⇒ B em +x."""
    th = np.linspace(th0, th0 + 2 * PI * nt, nt * n_per + 1)
    x = x0 + (x1 - x0) * (th - th[0]) / (th[-1] - th[0])
    return np.stack([x, yc + r * np.cos(th), r * np.sin(th)], 1)


def trilha(*parts):
    """Junta trechos: tuplas (x, y) são cantos de fio; arrays N×3 são hélices."""
    pts = []
    for p in parts:
        if isinstance(p, np.ndarray):
            pts += [[x, y, z, 1.0] for x, y, z in p]
        else:
            pts.append([p[0], p[1], 0.0, 0.0])
    return Trilha(pts)


class Ap:
    """Estado do aparato (trackers visuais e físicos) e o desenho de cada quadro."""
    OPS0 = ("oAll", "oDots", "oEL", "oEB", "oIA", "oSec", "oSrc", "oByp", "oVol", "oAe", "oCap", "oIS", "oHL",
            "oAmp", "oS1", "oS2", "oFlux", "oGauge", "oGb", "oGr", "oGs", "oEr", "oSweep")
    OPS1 = ("oCirc", "oSol", "oBat", "oB", "oHeat", "oLat")

    def __init__(self):
        T = ValueTracker
        s, cx, cy, fx, fy = LAYOUTS["full"]
        self.s, self.cx, self.cy, self.fx, self.fy = T(s), T(cx), T(cy), T(fx), T(fy)
        for n in self.OPS0:
            setattr(self, n, T(0.0))
        for n in self.OPS1:
            setattr(self, n, T(1.0))
        self.ang = T(ANG0)
        self.sw = T(SW_OPEN)
        self.tc, self.td, self.sp = T(0.0), T(0.0), T(0.0)
        self.mode, self.role, self.ph, self.auto_tc = "charge", 1, 0.0, 0.0
        self.H1 = helix3(XS0, XS1, YT, A_R, NT)
        self.H2 = helix3(XM0, XM1, YT, A2, NT2, th0=0.0)
        a0 = self.proj(*self.H1[0], ang=ANG0)
        a1 = self.proj(*self.H1[-1], ang=ANG0)
        self.HA, self.HB = (a0[0], a0[1]), (a1[0], a1[1])          # pontas da hélice na vista lateral
        H, S = self.H1, self.H2
        self.paths = {   # todos começam no pivô e seguem igual até (XB, YB): a comutação não "pula" as cargas
            "charge": trilha((XB, YT), self.HA, H, self.HB, (XR, YT), (XR, YB), (XB, YB), (XL, YB), (XL, YT), (XA, YT),
                             (XB, YT)),
            "discharge": trilha((XB, YT), self.HA, H, self.HB, (XR, YT), (XR, YB), (XB, YB), (XB, YT - LBL), (XB, YT)),
            "cap": trilha((XB, YT), self.HA, self.HB, (XR, YT), (XR, YB), (XB, YB), (XL, YB), (XL, YT), (XA, YT),
                          (XB, YT)),
            "probe": trilha(H),
            "sec": trilha(S, (XM1, YT + A2), (XM1, YMET), (XC + MR, YMET), (XC - MR, YMET), (XM0, YMET), (XM0, YT + A2)),
        }

    # ── projeção 2.5D: giro em torno do eixo vertical que passa pelo centro do solenoide ──────────────────────
    def proj(self, x, y, z, ang=None):
        a = self.ang.get_value() if ang is None else ang
        ca, sa = math.cos(a), math.sin(a)
        return (XC + (x - XC) * ca + z * sa, y + ELEV * z * ca, -(x - XC) * sa + z * ca)

    def projv(self, P, ang=None):
        a = self.ang.get_value() if ang is None else ang
        ca, sa = math.cos(a), math.sin(a)
        X = XC + (P[:, 0] - XC) * ca + P[:, 2] * sa
        Y = P[:, 1] + ELEV * P[:, 2] * ca
        D = -(P[:, 0] - XC) * sa + P[:, 2] * ca
        return X, Y, D

    # ── estado físico: tudo sai daqui ─────────────────────────────────────────────────────────────────────────
    def st(self):
        m = self.mode
        if m == "charge":
            e = math.exp(-self.tc.get_value())
            I, dI, q = 1 - e, e, 0.0
            if self.role == 1 and self.tc.get_value() < 1e-6 and abs(self.sw.get_value() - SW_A) > 2:
                dI = 0.0                                 # chave aberta: nada muda ainda
        elif m == "discharge":
            e = math.exp(-self.td.get_value())
            I, dI, q = e, -e, 0.0
        elif m == "probe":
            (I, dI), q = probe(self.sp.get_value()), 0.0
        else:                                            # "cap": carga RC do capacitor (C20)
            e = math.exp(-self.tc.get_value())
            I, dI, q = e, -e, 1 - e
        return {"I": I, "dI": dI, "B": I, "EL": -dI, "UB": I * I, "PR": I * I, "PL": I * dI, "q": q,
                "QR": 1 - math.exp(-2 * self.td.get_value())}

    def path_key(self):
        return "sec" if self.role == 2 else self.mode

    # ── transformação local → tela ──────────────────────────────────────────────────────────────────────────
    def W(self, x, y=0.0):
        s = self.s.get_value()
        return P3(self.cx.get_value() + s * (x - self.fx.get_value()), self.cy.get_value() + s * (y - self.fy.get_value()))

    def Wv(self, a):
        a = np.asarray(a, float)
        s = self.s.get_value()
        out = np.zeros((len(a), 3))
        out[:, 0] = self.cx.get_value() + s * (a[:, 0] - self.fx.get_value())
        out[:, 1] = self.cy.get_value() + s * (a[:, 1] - self.fy.get_value())
        return out

    def W3(self, x, y, z, ang=None):
        X, Y, _ = self.proj(x, y, z, ang)
        return self.W(X, Y)

    @staticmethod
    def ring3(x, r, n=48, yc=YT):
        th = np.linspace(0, 2 * PI, n + 1)
        return np.stack([np.full_like(th, x), yc + r * np.cos(th), r * np.sin(th)], 1)

    def flat(self, P, ang=None):
        X, Y, _ = self.projv(P, ang)
        return self.Wv(np.stack([X, Y], 1))

    # ── relógio ───────────────────────────────────────────────────────────────────────────────────────────
    def tick(self, dt):
        if self.auto_tc > 0:
            self.tc.increment_value(self.auto_tc * dt)
        self.ph = (self.ph + dt * 0.9 * abs(self.st()["I"])) % SPD     # velocidade das cargas ∝ I

    # ── desenho ─────────────────────────────────────────────────────────────────────────────────────────────
    def strands(self, P, wf, wb, cf, cb, of, ob, zf, zb, glow=True):
        """Hélice projetada: trechos de trás finos e escuros, da frente claros (com brilho discreto)."""
        X, Y, D = self.projv(P)
        S = self.Wv(np.stack([X, Y], 1))
        front, back, cur, sg = [], [], [S[0]], D[0] >= 0
        for k in range(1, len(S)):
            cur.append(S[k])
            if (D[k] >= 0) != sg:
                (front if sg else back).append(np.array(cur))
                cur, sg = [S[k]], D[k] >= 0
        (front if sg else back).append(np.array(cur))
        g = VGroup()
        if ob > 0.01 and back:
            g.add(multi(back).set_stroke(cb, wb, ob).set_z_index(zb))
        if of > 0.01 and front:
            if glow:
                g.add(multi(front).set_stroke(cf, wf * 2.6, 0.10 * of).set_z_index(zf))
            g.add(multi(front).set_stroke(cf, wf, of).set_z_index(zf))
        return g

    def body(self, x0, x1, r, n=40):
        """Silhueta (fecho convexo) do cilindro x ∈ [x0, x1], raio r, na projeção atual — em coordenadas de tela."""
        P = np.vstack([self.ring3(x0, r, n), self.ring3(x1, r, n)])
        X, Y, _ = self.projv(P)
        return self.Wv(hull(np.stack([X, Y], 1)))

    def build(self):
        g = VGroup()
        A = self.oAll.get_value()
        if A < 0.01:
            return g.add(Dot(radius=0.001).set_opacity(0))
        S = self.st()
        s, W, Wv = self.s.get_value(), self.W, self.Wv
        lw = 2.2 + 1.5 * min(s, 1.7)
        cap = self.oCap.get_value()
        oc = A * self.oCirc.get_value()
        osl = A * self.oSol.get_value() * (1 - cap)
        ocap = A * cap
        role2 = self.role == 2
        Bv = S["B"]
        a = self.ang.get_value()
        ca = abs(math.cos(a))
        lat = self.oLat.get_value()                        # 1 na vista lateral, 0 fora dela (fios ligam à hélice)
        oc2 = oc * lat
        obt = oc2 * self.oBat.get_value()

        # corpo de vidro do solenoide e volume de campo (magenta, ∝ B)
        if osl > 0.01:
            hb = self.body(XS0, XS1, A_R)
            g.add(Polygon(*hb).set_fill("#1B2440", 0.35 * osl).set_stroke(COIL_B, 1.2, 0.5 * osl).set_z_index(1))
            ob = osl * self.oB.get_value()
            if ob > 0.01 and Bv > 0.01:
                g.add(Polygon(*hb).set_fill(MAGENTA, ob * (0.06 + 0.24 * min(Bv, 1.3))).set_stroke(width=0).set_z_index(2))
                core = self.body(XS0 + 0.05, XS1 - 0.05, 0.45 * A_R)
                g.add(Polygon(*core).set_fill(MAGENTA, ob * 0.12 * min(Bv, 1.3)).set_stroke(width=0).set_z_index(2))
                if ca > 0.3:                              # linhas de B ao longo do eixo (somem na vista axial)
                    for yy, zz in ((0.55 * A_R, 0.0), (0.0, 0.0), (-0.55 * A_R, 0.0), (0.0, 0.5 * A_R)):
                        p0, p1 = self.W3(XS0 + 0.15, YT + yy, zz), self.W3(XS1 - 0.3, YT + yy, zz)
                        g.add(arrow(p0, p1, MAGENTA, 3.2, 3, 0.15 * min(s, 1.5),
                                    ob * min(1.0, Bv) * 0.85 * min(1, (ca - 0.3) / 0.4)))
            # seção A (tampa da frente = ponta direita na vista lateral) e volume varrido (C14)
            oae = osl * self.oAe.get_value()
            if oae > 0.01:
                g.add(Polygon(*self.flat(self.ring3(XS1, A_R))).set_fill(MAGENTA, 0.5 * oae).set_stroke(MAGENTA, 3, oae)
                      .set_z_index(6))
            sw_ = self.oSweep.get_value()
            if sw_ > 0.01:
                xr = XS1 - (XS1 - XS0) * min(1.0, sw_)
                g.add(Polygon(*self.body(xr, XS1, A_R)).set_fill(MAGENTA, 0.42 * osl).set_stroke(MAGENTA, 2.5, osl)
                      .set_z_index(3))
            ov = osl * self.oVol.get_value()
            if ov > 0.01:                                 # cota de ℓ
                y0 = YT - A_R - 0.42
                p0, p1 = self.W3(XS0, y0, 0), self.W3(XS1, y0, 0)
                g.add(Line(p0, p1).set_stroke(GEO, 3, ov).set_z_index(9))
                for p in (p0, p1):
                    g.add(Line(p + P3(0, -0.1), p + P3(0, 0.1)).set_stroke(GEO, 3, ov).set_z_index(9))
            # fluxo concatenado: a seção de cada espira acesa (C05)
            ohl = osl * self.oHL.get_value() * min(1.0, Bv * 1.5)
            if ohl > 0.01:
                for k in range(NT):
                    xk = XS0 + (k + 0.5) * (XS1 - XS0) / NT
                    g.add(Polygon(*self.flat(self.ring3(xk, A_R, 36))).set_fill(MAGENTA, 0.16 * ohl)
                          .set_stroke(MAGENTA, 1.6, 0.8 * ohl).set_z_index(4))
            # B na vista axial: ⊙ (saindo da tela)
            obd = osl * self.oB.get_value() * max(0.0, 1 - ca / 0.35) * min(1.0, Bv)
            if obd > 0.01:
                c0 = np.array(self.proj(XC, YT, 0)[:2])
                for i in range(-3, 4):
                    for j in range(-3, 4):
                        p = c0 + np.array([0.15 * i + 0.075 * (j % 2), 0.14 * j])
                        if np.linalg.norm(p - c0) < 0.82 * A_R:
                            q = W(*p)
                            g.add(Circle(radius=0.035 * s).move_to(q).set_stroke(MAGENTA, 2, obd).set_z_index(7))
                            g.add(Dot(q, radius=0.012 * s).set_fill(MAGENTA, obd).set_z_index(7))
            # E_φ induzido em anéis (vista axial): |E| ∝ r dentro, ∝ a²/r fora; dI/dt > 0 ⇒ horário (Lenz)
            oer = osl * self.oEr.get_value()
            if oer > 0.01:
                c0 = W(*self.proj(XC, YT, 0)[:2])
                dI = S["dI"]
                for rr in (0.35, 0.7, 1.3, 1.8):
                    e = (rr if rr < 1 else 1 / rr) * dI
                    m = abs(e)
                    if m < 0.03:
                        continue
                    r = rr * A_R * s
                    g.add(DashedVMobject(Circle(radius=r, arc_center=c0), num_dashes=int(14 + 8 * r), dashed_ratio=0.55)
                          .set_stroke(CYAN, 2.5, oer * min(1.0, 0.2 + m)).set_z_index(8))
                    for k in range(4):
                        th = PI / 4 + k * PI / 2 + 0.3 * rr
                        p = c0 + r * P3(math.cos(th), math.sin(th))
                        t = P3(math.sin(th), -math.cos(th)) * (1 if dI > 0 else -1)
                        Lr = (0.12 + 0.28 * m) * s / 1.5
                        g.add(arrow(p - t * Lr / 2, p + t * Lr / 2, CYAN, 4, 8, 0.12 * s / 1.5, oer * min(1.0, 0.3 + m)))

        # secundária e o fluxo que ela concatena
        osc = A * self.oSec.get_value()
        if osc > 0.01:
            g.add(self.strands(self.H2, lw * 0.95, lw * 0.6, "#E4EAF6", COIL_B, osc, 0.55 * osc, 6, 0))
            ofl = osc * self.oFlux.get_value() * min(1.0, Bv * 1.5)
            if ofl > 0.01:
                xm = 0.5 * (XM0 + XM1)
                g.add(DashedVMobject(Polygon(*self.flat(self.ring3(xm, A2))), num_dashes=30)
                      .set_stroke(WHITE, 2, 0.8 * ofl).set_z_index(6))
                g.add(Polygon(*self.flat(self.ring3(xm, A_R))).set_fill(MAGENTA, 0.55 * ofl)
                      .set_stroke(MAGENTA, 2.5, ofl).set_z_index(6))
        if osl > 0.01:
            col = interpolate_color(ManimColor(COIL), ManimColor("#F3B6FF"), 0.5 * self.oHL.get_value())
            g.add(self.strands(self.H1, lw * 0.9, lw * 0.6, col, COIL_B, osl, 0.7 * osl, 5, 1))

        # fios (ligados às pontas da hélice só na vista lateral)
        bat = [[(XL, YB), (XL, -0.1)], [(XL, 0.1), (XL, YT), (XA, YT)], [(XL, YB), (XB, YB)]]
        main = [[(XB, YT), (self.HA[0], YT), self.HA], [self.HB, (self.HB[0], YT), (XR, YT), (XR, 0.65)],
                [(XR, -0.65), (XR, YB), (XB, YB)]]
        if obt > 0.01:
            g.add(multi([Wv(p) for p in bat]).set_stroke(STEEL, lw, obt).set_z_index(3))
        if oc2 > 0.01:
            g.add(multi([Wv(p) for p in main]).set_stroke(STEEL, lw, oc2).set_z_index(3))
        oby = oc2 * self.oByp.get_value()
        if oby > 0.01:
            g.add(Line(W(XB, YT - LBL), W(XB, YB)).set_stroke(STEEL, lw, oby).set_z_index(3))
            g.add(Dot(W(XB, YB), radius=0.05 * s).set_fill(STEEL, oby).set_z_index(4))
            g.add(Circle(radius=0.06 * s).move_to(W(XB, YT - LBL)).set_fill(BACKGROUND_COLOR, oby)
                  .set_stroke(WHITE, 2, oby).set_z_index(5))
        # bateria (placa longa = +)
        if obt > 0.01:
            g.add(Line(W(XL - 0.38, 0.1), W(XL + 0.38, 0.1)).set_stroke(WHITE, lw * 1.1, obt).set_z_index(4))
            g.add(Line(W(XL - 0.2, -0.1), W(XL + 0.2, -0.1)).set_stroke(WHITE, lw * 2.6, obt).set_z_index(4))
            pc, aa = W(XL + 0.52, 0.34), 0.07 * s
            g.add(multi([[pc + P3(-aa, 0), pc + P3(aa, 0)], [pc + P3(0, -aa), pc + P3(0, aa)]])
                  .set_stroke(WHITE, 2.5, obt).set_z_index(4))
        # medidores de potência (mesma escala ℰ₀ I_∞): fonte = resistor + campo
        og = oc2 * self.oGauge.get_value()
        if og > 0.01 and self.mode == "charge":
            Hg, wg = 1.5, 0.22
            PJ, PL = S["PR"], max(0.0, S["PL"])

            def gauge(x, y0, parts, o):
                gg = VGroup(Rectangle(width=wg * s, height=Hg * s).move_to(W(x, y0 + Hg / 2)).set_fill(opacity=0)
                            .set_stroke(DIM, 1.5, o))
                acc = 0.0
                for v, colr in parts:
                    if v > 0.004:
                        gg.add(Rectangle(width=wg * s, height=Hg * v * s).move_to(W(x, y0 + Hg * (acc + v / 2)))
                               .set_fill(colr, 0.9 * o).set_stroke(width=0))
                    acc += v
                return gg.set_z_index(9)
            if self.oGb.get_value() > 0.01:
                g.add(gauge(XL + 0.8, -0.75, [(PJ, HEAT), (PL, MAGENTA)], og * self.oGb.get_value()))
            if self.oGr.get_value() > 0.01:
                g.add(gauge(XR + 0.75, -0.75, [(PJ, HEAT)], og * self.oGr.get_value()))
            if self.oGs.get_value() > 0.01:
                g.add(gauge(XS1 + 0.55, YT + 0.1, [(PL, MAGENTA)], og * self.oGs.get_value()))
        # resistor (cor e brilho ∝ P_R) e chave
        if oc2 > 0.01:
            h = min(1.0, S["PR"]) * self.oHeat.get_value() * (0 if role2 or self.mode in ("probe", "cap") else 1)
            if h > 0.03:
                for sc, op in ((2.6, 0.10), (1.9, 0.16), (1.35, 0.26)):
                    g.add(RoundedRectangle(corner_radius=0.12 * s, width=0.45 * s * sc, height=1.3 * s * (0.6 + 0.4 * sc))
                          .set_fill(HEAT, op * h * oc2).set_stroke(width=0).move_to(W(XR, 0)).set_z_index(2))
            zz = [(XR, 0.65)] + [(XR + (0.2 if i % 2 == 0 else -0.2), 0.65 - 1.3 * (i + 0.5) / 7) for i in range(7)] + \
                 [(XR, -0.65)]
            col = interpolate_color(ManimColor(STEEL), ManimColor(HEAT), h)
            g.add(VMobject().set_points_as_corners(Wv(zz)).set_stroke(col, lw * 1.05, oc2).set_z_index(4))
            ang = math.radians(self.sw.get_value())
            pv = W(XB, YT)
            g.add(Circle(radius=0.06 * s).move_to(W(XA, YT)).set_fill(BACKGROUND_COLOR, obt)
                  .set_stroke(WHITE, 2, obt).set_z_index(5))
            g.add(Line(pv, W(XB + LBL * math.cos(ang), YT + LBL * math.sin(ang)))
                  .set_stroke("#DCE4F2", lw * 1.15, oc2).set_z_index(6))
            g.add(Dot(pv, radius=0.07 * s).set_fill("#DCE4F2", oc2).set_z_index(6))

        # terminais e medidor/fonte da secundária
        if osc > 0.01:
            g.add(multi([Wv([(XM0, YT + A2), (XM0, YMET), (XC - MR, YMET)]),
                         Wv([(XM1, YT + A2), (XM1, YMET), (XC + MR, YMET)])]).set_stroke(STEEL, lw, osc).set_z_index(5))
            mc = W(XC, YMET)
            g.add(Circle(radius=MR * s).move_to(mc).set_fill(BACKGROUND_COLOR, osc).set_stroke(WHITE, 2.5, osc)
                  .set_z_index(6))
            osr = self.oSrc.get_value()
            if osr < 0.99:
                e2 = 0.0 if role2 else max(-1.0, min(1.0, -S["dI"]))
                ph = math.radians(65 * e2)
                p0 = mc + P3(0, -0.14 * s)
                g.add(Line(p0, p0 + 0.36 * s * P3(math.sin(ph), math.cos(ph))).set_stroke(CYAN, 3, osc * (1 - osr))
                      .set_z_index(7))
            if osr > 0.01:
                xs = np.linspace(-0.18, 0.18, 30)
                g.add(VMobject().set_points_smoothly([mc + s * P3(x, 0.08 * math.sin(x / 0.18 * PI * 2)) for x in xs])
                      .set_stroke(WHITE, 3, osc * osr).set_z_index(7))

        # capacitor 2.5D (C20): placas quadradas no plano y–z
        if ocap > 0.01:
            g.add(multi([Wv([self.HA, (XP0, YT)]), Wv([(XP1, YT), self.HB])]).set_stroke(STEEL, lw, oc * cap)
                  .set_z_index(3))
            for xp in (XP0, XP1):
                q = [self.proj(xp, YT + u * PH, v * PH, ang=ANG0)[:2] for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
                g.add(Polygon(*Wv(q)).set_fill("#B8C8E8", 0.18 * ocap).set_stroke("#DCE4F2", 2.2, ocap).set_z_index(5))
            nq = int(round(9 * S["q"]))
            aa = 0.055 * s
            for i in range(nq):
                u, v = -0.6 + 0.6 * (i % 3), -0.6 + 0.6 * (i // 3)
                c1 = W(*self.proj(XP0 + 0.03, YT + u * PH, v * PH, ang=ANG0)[:2])
                c2 = W(*self.proj(XP1 - 0.03, YT + u * PH, v * PH, ang=ANG0)[:2])
                g.add(multi([[c1 + P3(-aa, 0), c1 + P3(aa, 0)], [c1 + P3(0, -aa), c1 + P3(0, aa)],
                             [c2 + P3(-aa, 0), c2 + P3(aa, 0)]]).set_stroke(GREEN, 2.5, ocap).set_z_index(6))

        # anel amperiano e superfícies S1 (disco) e S2 (saco que passa entre as placas)
        oam = A * self.oAmp.get_value()
        if oam > 0.01:
            ring = self.flat(self.ring3(XAMP, RAMP, 60), ANG0)
            o1, o2 = self.oS1.get_value() * oam, self.oS2.get_value() * oam
            if o1 > 0.01:
                g.add(Polygon(*ring).set_fill(GEO, 0.22 * o1).set_stroke(width=0).set_z_index(4))
            if o2 > 0.01:
                xg = 0.5 * (XP0 + XP1)
                P = np.vstack([self.ring3(XAMP, RAMP, 40), self.ring3(xg, RAMP, 40)])
                X, Y, _ = self.projv(P, ANG0)
                g.add(Polygon(*Wv(hull(np.stack([X, Y], 1)))).set_fill(VIOLET, 0.12 * o2).set_stroke(VIOLET, 2, 0.8 * o2)
                      .set_z_index(4))
                g.add(DashedVMobject(Polygon(*self.flat(self.ring3(xg, RAMP, 48), ANG0)), num_dashes=26)
                      .set_stroke(VIOLET, 2.5, o2).set_z_index(7))
            g.add(VMobject().set_points_as_corners(ring).set_stroke(WHITE, 3, oam).set_z_index(7))
            ib = min(1.0, abs(S["I"]) * 2.5)
            if ib > 0.02:                                  # B em volta do fio: ⊙ em cima, ⊗ embaixo
                for k in (-1.35, -0.35):
                    pu, pd, r = W(k, YT + 0.45), W(k, YT - 0.45), 0.09 * s
                    g.add(Circle(radius=r).move_to(pu).set_stroke(MAGENTA, 2.5, oam * ib).set_z_index(6))
                    g.add(Dot(pu, radius=0.03 * s).set_fill(MAGENTA, oam * ib).set_z_index(6))
                    g.add(Circle(radius=r).move_to(pd).set_stroke(MAGENTA, 2.5, oam * ib).set_z_index(6))
                    g.add(multi([[pd + P3(-0.6 * r, -0.6 * r), pd + P3(0.6 * r, 0.6 * r)],
                                 [pd + P3(-0.6 * r, 0.6 * r), pd + P3(0.6 * r, -0.6 * r)]])
                          .set_stroke(MAGENTA, 2.5, oam * ib).set_z_index(6))

        # cargas em movimento (corrente convencional): espaçamento fixo, fase comum a todos os percursos
        od = A * self.oDots.get_value()
        I = S["I"]
        if od > 0.01:
            k = self.paths[self.path_key()]
            ss = np.arange(self.ph, k.L, SPD)
            xs, ys, zs, hs = k.at(ss)
            base = od * (0.3 + 0.7 * min(1.0, abs(I)))
            for x, y, z, hh in zip(xs, ys, zs, hs):
                if hh > 0.5:
                    X, Y, D = self.proj(x, y, z)
                    f, front = (osc if role2 else osl), D >= 0
                else:
                    X, Y, front = x, y, True
                    if self.mode == "cap" and XP0 - 0.03 < x < XP1 + 0.03 and abs(y - YT) < 0.1:
                        continue
                    f = osc if role2 else (osl if self.mode == "probe" else oc2)
                op = base * f / max(A, 1e-6) * (1.0 if front else 0.35)
                if op > 0.01:
                    g.add(Dot(W(X, Y), radius=(0.06 if front else 0.045) * min(s, 1.15)).set_fill(GREEN, op)
                          .set_stroke(BACKGROUND_COLOR, 1, op).set_z_index(7 if front else 2))

        # fem autoinduzida ℰ_L (seta = sentido em que empurra a corrente; + na ponta)
        oe = osl * self.oEL.get_value() * lat
        el = S["EL"]
        if oe > 0.01 and abs(el) > 0.02:
            y = YT + A_R + 0.5
            g.add(arrow(W(XC - 0.8 * el, y), W(XC + 0.8 * el, y), CYAN, 6, 9, 0.22 * min(s, 1.4), oe))
            sg, aa, opm = (1 if el > 0 else -1), 0.08 * s, oe * min(1.0, 3 * abs(el))
            pp, pm = W(XC + sg * 1.85, y), W(XC - sg * 1.85, y)
            g.add(multi([[pp + P3(-aa, 0), pp + P3(aa, 0)], [pp + P3(0, -aa), pp + P3(0, aa)],
                         [pm + P3(-aa, 0), pm + P3(aa, 0)]]).set_stroke(CYAN, 3, opm).set_z_index(9))
        oeb = obt * self.oEB.get_value()
        if oeb > 0.01:
            g.add(arrow(W(XL + 0.62, -0.8), W(XL + 0.62, 0.8), CYAN, 6, 9, 0.22 * min(s, 1.4), oeb))
        oia = oc2 * self.oIA.get_value() * (0 if role2 else 1)
        if oia > 0.01 and abs(I) > 0.02:
            y = YB - 0.3
            g.add(arrow(W(XIA + 0.75 * I, y), W(XIA - 0.75 * I, y), GREEN, 6, 9, 0.2 * min(s, 1.4), oia))
        ois = osl * self.oIS.get_value()
        if ois > 0.01 and abs(I) > 0.02:
            y = YT - A_R - 0.62
            g.add(arrow(W(XC - 0.7 * I, y), W(XC + 0.7 * I, y), GREEN, 6, 9, 0.2 * min(s, 1.4), ois))
        return g


class Graf:
    """Eixos t × grandeza; curvas, área e marcador lidos de um tracker (unidades de τ)."""

    def __init__(self, sc, center=GC, w=5.5, h=2.8, xmax=5.0, ymax=1.15, one=None, ylab=None, ycol=WHITE,
                 ticks=True, tlab=True):
        self.sc, self.op, self.xmax, self.dyn = sc, ValueTracker(0.0), xmax, []
        ax = Axes(x_range=[0, xmax, 1], y_range=[0, ymax, 0.5], x_length=w, y_length=h, tips=False,
                  axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False}).move_to(P3(*center))
        self.ax = ax
        deco = VGroup()
        if ticks:
            for k in range(1, int(xmax) + 1):
                deco.add(Line(ax.c2p(k, 0), ax.c2p(k, 0.06), color=DIM, stroke_width=2))
                if tlab:
                    deco.add(MathTex(r"\tau" if k == 1 else rf"{k}\tau", font_size=24, color=DIM)
                             .move_to(ax.c2p(k, 0) + P3(0, -0.27)))
        deco.add(MathTex("0", font_size=24, color=DIM).move_to(ax.c2p(0, 0) + P3(-0.22, -0.18)))
        if one:
            deco.add(Line(ax.c2p(0, 1), ax.c2p(0.1 * xmax / 5, 1), color=DIM, stroke_width=2))
            deco.add(MathTex(one, font_size=26, color=DIM).next_to(ax.c2p(0, 1), LEFT, buff=0.12))
        if tlab:
            deco.add(MathTex("t", font_size=28, color=VIOLET).move_to(ax.c2p(xmax, 0) + P3(0.28, 0.0)))
        if ylab:
            deco.add(MathTex(ylab, font_size=28, color=ycol).next_to(ax.c2p(0, ymax), UP, buff=0.06))
        self.static = VGroup(ax, deco).set_z_index(4)

    def c2p(self, x, y):
        return self.ax.c2p(x, y)

    def curve(self, fn, tr, color, width=5, z=6):
        ax, op = self.ax, self.op

        def mk():
            x1 = min(tr.get_value(), self.xmax)
            o = op.get_value()
            if x1 < 0.02 or o < 0.01:
                return VMobject()
            return ax.plot(fn, x_range=[0, x1, max(0.02, x1 / 120)], color=color, stroke_width=width,
                           use_smoothing=False).set_stroke(opacity=o).set_z_index(z)
        return self._keep(redraw(mk))

    def area(self, fn, tr, color, op_=0.35):
        ax, op = self.ax, self.op

        def mk():
            x1 = min(tr.get_value(), self.xmax)
            o = op.get_value()
            if x1 < 0.02 or o < 0.01:
                return VMobject()
            xs = np.linspace(0, x1, 80)
            pts = [ax.c2p(0, 0)] + [ax.c2p(x, fn(x)) for x in xs] + [ax.c2p(x1, 0)]
            return Polygon(*pts).set_fill(color, op_ * o).set_stroke(width=0).set_z_index(5)
        return self._keep(redraw(mk))

    def marker(self, fn, tr, color=WHITE, slope=None):
        ax, op = self.ax, self.op

        def mk():
            x = min(tr.get_value(), self.xmax)
            o = op.get_value()
            if o < 0.01:
                return VMobject()
            y = fn(x)
            g = VGroup(DashedLine(ax.c2p(x, 0), ax.c2p(x, y), dash_length=0.07, color=WHITE, stroke_width=2)
                       .set_opacity(0.45 * o),
                       Dot(ax.c2p(x, y), radius=0.08).set_fill(color, o).set_stroke(WHITE, 1.5, o))
            if slope is not None:                          # reta tangente: sinal de dI/dt à vista
                d = slope(x)
                hw = 0.4 / max(1.0, abs(d) * 1.6)
                g.add(Line(ax.c2p(x - hw, y - hw * d), ax.c2p(x + hw, y + hw * d)).set_stroke(CYAN, 3, o))
            return g.set_z_index(9)
        return self._keep(redraw(mk))

    def _keep(self, m):
        self.sc.add(m)
        self.dyn.append(m)
        return m

    def show(self):
        return [FadeIn(self.static), self.op.animate.set_value(1)]

    def hide(self):
        return [FadeOut(self.static), self.op.animate.set_value(0)]

    def drop(self):
        self.sc.remove(*self.dyn)
        self.dyn = []


class IndutanciaYT012(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        ap = self.ap = Ap()
        tickm = Mobject()
        tickm.add_updater(lambda m, dt: ap.tick(dt))
        latm = Mobject()                                   # fios/rótulos do circuito só na vista lateral
        latm.add_updater(lambda m: ap.oLat.set_value(max(0.0, 1 - abs(ap.ang.get_value() - ANG0) / 0.3)))
        self.add(tickm, latm)
        self.tag = text("ELETROMAGNETISMO · INDUTÂNCIA E ENERGIA MAGNÉTICA", 20, opacity=0.58) \
            .to_corner(UL, buff=0.32).set_z_index(40)
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3)
        self.wm.set_z_index(40)
        self.add(self.tag, self.wm)
        self.body = redraw(ap.build)
        self.add(self.body)
        self.hd, self.E, self.marks, self.evts, self.cur = None, VGroup(), [], [], 0
        self.mk_labels()
        for k in range(1, 21):
            getattr(self, f"c{k:02d}")()
        out = {"cenas": self.marks, "transformacoes": self.evts, "total": round(self.renderer.time, 2)}
        json.dump(out, open(PASTA / ("tempos.json" if not SEL else f"tempos_SO_{os.environ['SO']}.json"), "w", encoding="utf-8"),
                  indent=1, ensure_ascii=False)

    # ── utilidades ──────────────────────────────────────────────────────────────────────────────────────────
    def purge(self):
        """Tira da cena o que ficou totalmente invisível e sem updater (evita acúmulo quadro a quadro)."""
        keep = {self.body, self.tag, self.wm}
        for m in list(self.mobjects):
            if m in keep or m.get_updaters() or not isinstance(m, VMobject):
                continue
            fam = m.family_members_with_points()
            if fam and all(max(f.get_fill_opacity(), f.get_stroke_opacity()) < 0.01 for f in fam):
                self.remove(m)

    def sec(self, k, nome):
        self.purge()
        self.cur = k
        self.marks.append({"cena": f"C{k:02d}", "nome": nome, "t": round(self.renderer.time, 2)})
        if SEL:
            self.next_section(f"C{k:02d}", skip_animations=k not in SEL)

    def H(self, s):
        """Manchete em CAIXA ALTA; troca sequencial (a velha sai antes de a nova entrar: nunca se cruzam)."""
        new = fitw(text(s.upper(), T_HEAD, opacity=0.92), 11.5).move_to(P3(0, 3.42)).set_z_index(30)
        old, self.hd = self.hd, new
        return [soft_swap(old, new)] if old is not None else [FadeIn(new, shift=0.1 * DOWN)]

    def lay(self, name):
        ap = self.ap
        return [tr.animate.set_value(v) for tr, v in zip((ap.s, ap.cx, ap.cy, ap.fx, ap.fy), LAYOUTS[name])]

    def setlay(self, name):
        for tr, v in zip((self.ap.s, self.ap.cx, self.ap.cy, self.ap.fx, self.ap.fy), LAYOUTS[name]):
            tr.set_value(v)

    def Wl(self, name, x, y):
        s, cx, cy, fx, fy = LAYOUTS[name]
        return P3(cx + s * (x - fx), cy + s * (y - fy))

    def lab(self, mob, anchor, off=(0, 0), color=WHITE, size=M_S, dep=None):
        """Rótulo preso ao aparato; dep = trackers extras de opacidade."""
        ap = self.ap
        m = MathTex(mob, font_size=size, color=color) if isinstance(mob, str) else mob
        m.v = ValueTracker(0)
        deps = [getattr(ap, d) for d in (dep or [])]

        def upd(x):
            o = off() if callable(off) else off
            x.move_to(ap.W(*anchor()) + P3(*o) * ap.s.get_value())
            ov = m.v.get_value() * ap.oAll.get_value()
            for d in deps:
                ov *= d.get_value()
            x.set_opacity(ov)
            if isinstance(x, MathTex):
                x.set_stroke(BACKGROUND_COLOR, 8, ov, background=True)
        m.add_updater(upd)
        upd(m)
        m.set_z_index(20)
        self.add(m)
        return m

    def mk_labels(self):
        L = self.L = {}
        L["E0"] = self.lab(r"\mathcal E_0", lambda: (XL, 0), (-0.55, 0), CYAN, dep=["oCirc", "oBat", "oLat"])
        L["R"] = self.lab("R", lambda: (XR, 0), (0.55, 0), HEAT, dep=["oCirc", "oLat"])
        L["sol"] = self.lab(tag("solenoide", 18, DIM, 1), lambda: (XC, YT - A_R), (0, -0.42), dep=["oSol", "oLat"])
        L["L"] = self.lab("L", lambda: (XC, YT - A_R), (0, -0.44), dep=["oSol", "oLat"])
        L["B"] = self.lab(r"\mathbf B", lambda: (XS0 + 0.2, YT - A_R), (0, -0.44), MAGENTA, dep=["oSol", "oB", "oLat"])
        L["I"] = self.lab("I", lambda: (XIA, YB - 0.3), (0, -0.34), GREEN, dep=["oCirc", "oIA", "oLat"])
        L["I1"] = self.lab("I_1", lambda: (XIA, YB - 0.3), (0, -0.34), GREEN, dep=["oCirc", "oIA", "oLat"])
        L["EL"] = self.lab(r"\mathcal E_L", lambda: (XC, YT + A_R + 0.5), (0, 0.38), CYAN, dep=["oSol", "oEL", "oLat"])
        L["E1"] = self.lab(r"\mathcal E_1", lambda: (XC, YT + A_R + 0.5), (-1.3, 0.3), CYAN, dep=["oSol", "oEL", "oLat"])
        L["E2"] = self.lab(r"\mathcal E_2", lambda: (XC + MR, YMET), (0.42, 0.05), CYAN, dep=["oSec"])
        L["N2"] = self.lab("N_2", lambda: (XM1, YT + A2), (0.5, 0.15), GEO, dep=["oSec"])
        L["I2"] = self.lab("I_2", lambda: (XM1, 0.5 * (YT + A2 + YMET)), (0.36, 0), GREEN, dep=["oSec"])
        L["med"] = self.lab(tag("medidor", 18, DIM, 1), lambda: (XC, YMET), (0, 0.6), dep=["oSec"])
        L["fonte"] = self.lab(tag("fonte", 18, DIM, 1), lambda: (XC, YMET), (0, 0.6), dep=["oSec"])
        L["A"] = self.lab("A", lambda: (XS1, YT), (0.62, 0.1), GEO, dep=["oSol"])
        L["ell"] = self.lab(r"\ell", lambda: (XC, YT - A_R - 0.42), (0, -0.3), GEO, dep=["oSol"])
        L["a"] = self.lab("a", lambda: (XC, YT), (0.25, 0.12), GEO, size=26, dep=["oSol"])
        L["C"] = self.lab("C", lambda: (XC, YT - PH), (0, -0.5), dep=["oCap"])
        L["S1"] = self.lab("S_1", lambda: (XAMP, YT - RAMP), (-0.2, -0.3), GEO, size=26, dep=["oAmp", "oS1"])
        L["S2"] = self.lab("S_2", lambda: (XC, YT + RAMP), (0.3, 0.32), VIOLET, size=26, dep=["oAmp", "oS2"])
        L["gap"] = self.lab(r"I=0", lambda: (XC, YT + PH), (0.0, 0.35), GREEN, size=24, dep=["oCap"])
        L["Gb"] = self.lab(r"P_{\rm fonte}", lambda: (XL + 0.8, -0.75), (0, -0.3), size=24, dep=["oGauge", "oGb"])
        L["Gr"] = self.lab(r"P_{\rm Joule}", lambda: (XR + 0.75, -0.75), (0, -0.3), HEAT, size=24,
                           dep=["oGauge", "oGr"])
        L["Gs"] = self.lab(r"\frac{dU_B}{dt}", lambda: (XS1 + 0.55, YT + 1.6), (0, 0.32), MAGENTA, size=24,
                           dep=["oGauge", "oGs"])

    def show(self, *labs):
        return [m.v.animate.set_value(1) for m in labs]

    def hide(self, *labs):
        return [m.v.animate.set_value(0) for m in labs]

    def clrE(self):
        old, self.E = self.E, VGroup()
        return [FadeOut(old)] if len(old) else []

    def gm(self, old, new, *moves, rt=T_MORPH, extra=(), pos=None, name="", copy=False):
        """old (Eq) → new (Eq) por TransformByGlyphMap; o que não for citado entra/sai por fade."""
        new.mob.move_to(pos if pos is not None else old.mob.get_center())
        t0 = self.renderer.time
        # o que some termina na 1ª metade e o que nasce só começa na 2ª: nada coexiste no mesmo lugar
        self.play(TransformByGlyphMap(old.mob, new.mob, *moves, auto_fade=True, from_copy=copy,
                                      default_remover_kwargs={"rate_func": _first_half},
                                      default_introducer_kwargs={"rate_func": _second_half}), *extra, run_time=rt)
        if not copy:
            self.remove(old.mob, *old.mob[0].submobjects)
        self.remove(*new.mob[0].submobjects)            # o MF-Tools deixa os glifos soltos na cena: reagrupa sob a equação
        self.add(new.mob)
        self.evts.append({"cena": f"C{self.cur:02d}", "nome": name, "t0": round(t0, 2), "dur": rt})
        return new

    def strike(self, *glyphs, color=HEAT):
        return VGroup(*[Line(gl.get_corner(DL) + P3(-0.04, -0.04), gl.get_corner(UR) + P3(0.04, 0.04), color=color,
                             stroke_width=5) for gl in glyphs]).set_z_index(30)

    def rewind(self, tr, gx=None):
        """Recomeça o mesmo processo em t = 0: atenua, zera o tracker, volta (marca violeta t = 0 no gráfico)."""
        ap = self.ap
        self.play(ap.oAll.animate.set_value(0.35), ap.oDots.animate.set_value(0), run_time=0.5)
        tr.set_value(0.0)
        mk = None
        if gx is not None:
            mk = MathTex("t=0", font_size=28, color=VIOLET).next_to(gx.c2p(0, 0), DOWN, buff=0.38).set_z_index(30)
        self.play(ap.oAll.animate.set_value(1), ap.oDots.animate.set_value(1), *([FadeIn(mk)] if mk else []),
                  run_time=0.6)
        if mk:
            self.play(FadeOut(mk), run_time=0.6)

    def ring(self, p, w=1.0, h=1.0, color=WHITE):
        r = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(color, 4).move_to(p).set_z_index(25)
        self.play(Create(r), run_time=0.6)
        self.play(r.animate.set_stroke(opacity=0), run_time=0.6)
        self.remove(r)

    def run(self, tr, v, t, *extra):
        self.play(tr.animate.set_value(v), *extra, run_time=t, rate_func=linear)

    # ═══ C01 — a previsão que falha ═══════════════════════════════════════════════════════════════════════
    def c01(self):
        ap, L = self.ap, self.L
        self.sec(1, "previsao_que_falha")
        self.setlay("left")
        self.play(ap.oAll.animate.set_value(1), *self.H("Bateria, chave, solenoide e resistor"),
                  *self.show(L["E0"], L["R"], L["sol"]), run_time=T_MOVE)
        self.wait(T_READ)
        g = self.g = Graf(self, one=r"I_\infty", ylab="I", ycol=GREEN)
        i0 = MathTex("I", "=", "0", font_size=M_L)
        i0[0].set_color(GREEN)
        i0.move_to(P3(EQX, 2.05))
        ca = desc("chave aberta: nenhuma corrente").next_to(i0, DOWN, buff=0.22)
        self.play(*g.show(), FadeIn(i0), FadeIn(ca), run_time=T_EQ)
        self.wait(T_READ)
        pred = MathTex("I", "=", r"\frac{\mathcal E_0}{R}", font_size=M_L)
        pred[0].set_color(GREEN)
        pred.move_to(P3(EQX, 2.05))
        pn = desc("hipótese ingênua: a corrente salta").next_to(pred, DOWN, buff=0.2)
        jump = DashedVMobject(VMobject().set_points_as_corners([g.c2p(0, 0), g.c2p(0, 1), g.c2p(5, 1)]),
                              num_dashes=48, dashed_ratio=0.55).set_stroke(WHITE, 3, 0.85).set_z_index(5)
        self.play(*self.H("O que esperamos ao fechar a chave?"), FadeOut(ca), run_time=T_FADE)
        self.play(ReplacementTransform(i0[0], pred[0]), ReplacementTransform(i0[1], pred[1]),
                  soft_swap(i0[2], pred[2]), run_time=T_EQ)
        self.remove(i0, *pred.submobjects)
        self.add(pred)
        self.play(FadeIn(pn), Create(jump), run_time=1.8)
        self.wait(T_READ)
        self.play(*self.H("Fechamos a chave"), FadeOut(pn), run_time=T_FADE)
        self.play(ap.sw.animate.set_value(SW_A), run_time=T_SW)
        g.curve(lambda x: 1 - math.exp(-x), ap.tc, GREEN, 5)
        g.marker(lambda x: 1 - math.exp(-x), ap.tc, GREEN)
        self.play(ap.oDots.animate.set_value(1), ap.oIA.animate.set_value(1), *self.show(L["I"], L["B"]),
                  run_time=0.6)
        self.run(ap.tc, 1.2, 0.3 * T_RUN, jump.animate.set_stroke(opacity=0))   # a curva real substitui o salto
        self.remove(jump)
        real = MathTex("I(t)", "=", r"I_\infty", r"\left(1-e^{-t/\tau}\right)", font_size=M_L)
        real[0].set_color(GREEN)
        real[2].set_color(GREEN)
        real.move_to(P3(EQX, 2.05))
        self.play(FadeOut(pred, shift=0.1 * UP), ap.tc.animate.set_value(1.5), run_time=0.8, rate_func=linear)
        self.run(ap.tc, 5.0, 0.6 * T_RUN, FadeIn(real))
        self.play(*self.H("A corrente deveria saltar"), run_time=T_FADE)
        self.wait(T_READ)
        self.play(*self.H("Mas não salta"), run_time=T_FADE)
        self.ring(self.Wl("left", XC, YT), 3.2, 1.25, MAGENTA)
        nb = desc("e o campo magnético cresce junto com ela", color=MAGENTA).move_to(P3(EQX, 1.25))
        self.play(FadeIn(nb), run_time=T_FADE)
        self.E = VGroup(real, nb)
        self.wait(T_HOLD)

    # ═══ C02 — promessa ═════════════════════════════════════════════════════════════════════════════════════
    def c02(self):
        ap, L, g = self.ap, self.L, self.g
        self.sec(2, "promessa")
        t1 = fitw(text("POR QUE A CORRENTE RESISTE A MUDAR?", 44, CYAN), 13.0).move_to(P3(0, 0.35))
        t2 = text("Indutância e energia magnética", 30, WHITE, 0.85).move_to(P3(0, -0.6))
        self.play(FadeOut(self.hd), *self.clrE(), *g.hide(), ap.oAll.animate.set_value(0.16), run_time=T_MOVE)
        self.hd = None
        g.drop()
        ap.tc.set_value(0)
        ap.sw.set_value(SW_OPEN)
        ap.oDots.set_value(0)
        ap.oIA.set_value(0)
        self.play(FadeIn(t1, shift=0.1 * DOWN), *self.hide(L["I"], L["B"]), run_time=1.2)
        self.play(FadeIn(t2, shift=0.1 * DOWN), run_time=T_FADE)
        self.wait(T_HOLD)
        self.play(FadeOut(t1, shift=0.1 * UP), FadeOut(t2, shift=0.1 * UP), ap.oAll.animate.set_value(1),
                  run_time=T_MOVE)

    # ═══ C03 — indução mútua ════════════════════════════════════════════════════════════════════════════════
    def c03(self):
        ap, L = self.ap, self.L
        self.sec(3, "inducao_mutua")
        self.play(*self.H("Uma segunda bobina, em volta do solenoide"), *self.lay("mut"),
                  ap.oSec.animate.set_value(1), *self.show(L["N2"], L["E2"], L["med"]), *self.hide(L["sol"]),
                  run_time=T_MOVE)
        self.wait(T_READ)
        self.play(ap.sw.animate.set_value(SW_A), run_time=T_SW)
        # a física primeiro: corrente → campo → fluxo na bobina 2 → medidor. Cada elo nasce com o fenômeno.
        ch = MathTex(r"I_1", r"\ \longrightarrow\ ", r"\mathbf B_1", r"\ \longrightarrow\ ", r"\Lambda_2",
                     r"\ \longrightarrow\ ", r"\mathcal E_2", font_size=M_L).move_to(P3(EQX, 2.05))
        for i, c in ((0, GREEN), (2, MAGENTA), (4, MAGENTA), (6, CYAN)):
            ch[i].set_color(c)
        cps = [desc(t, 22) for t in ("corrente", "campo", "fluxo na bobina 2", "fem")]
        for c, i in zip(cps, (0, 2, 4, 6)):
            c.next_to(ch[i], DOWN, buff=0.18)
        cps[2].shift(0.32 * DOWN)
        self.play(*self.H("A corrente começa a mudar"), ap.oDots.animate.set_value(1), ap.oIA.animate.set_value(1),
                  *self.show(L["I1"]), FadeIn(ch[0]), FadeIn(cps[0]), ap.tc.animate.set_value(0.25), run_time=2.6,
                  rate_func=linear)
        self.play(*self.H("Cria um campo dentro do solenoide"), FadeIn(ch[1]), FadeIn(ch[2]), FadeIn(cps[1]),
                  *self.show(L["B"]), ap.tc.animate.set_value(0.5), run_time=2.6, rate_func=linear)
        self.play(*self.H("Esse fluxo atravessa a bobina 2"), FadeIn(ch[3]), FadeIn(ch[4]), FadeIn(cps[2]),
                  ap.oFlux.animate.set_value(1), ap.tc.animate.set_value(0.75), run_time=2.6, rate_func=linear)
        self.play(*self.H("E o medidor responde"), FadeIn(ch[5]), FadeIn(ch[6]), FadeIn(cps[3]),
                  ap.tc.animate.set_value(1.0), run_time=2.6, rate_func=linear)
        self.run(ap.tc, 5.0, T_RUN, *self.H("Só há fem enquanto a corrente muda"))
        self.wait(T_READ)
        # só agora a formalização
        e1 = Eq(r"\Lambda_2", "=", "M", "I_1").at(EQX - 1.6, 0.55)
        e2 = Eq(r"\mathcal E_2", "=", "-M", r"\frac{dI_1}{dt}").at(EQX + 1.5, 0.55)
        self.play(*self.H("Formalizando"), FadeOut(VGroup(*cps)), FadeIn(e1.mob), run_time=T_EQ)
        self.play(FadeIn(e2.mob), run_time=T_EQ)
        self.wait(T_READ)
        # geometria: M = μ0 n N2 A
        self.play(*self.H("O coeficiente M vem da geometria"), run_time=T_FADE)
        br = Brace(VGroup(Dot(self.Wl("mut", XS0 + 0.1, YT - A_R - 0.12)), Dot(self.Wl("mut", XS0 + 1.1, YT - A_R - 0.12))),
                   DOWN, buff=0.04, color=GEO)
        bn = row(tex("n", 28, GEO), desc("espiras por metro", 20, GEO), buff=0.1).next_to(br, DOWN, buff=0.06)
        g1 = Eq(r"\Lambda_2", "=", "N_2", r"\mathbf B_1", "A", size=M_M).at(EQX, -0.6)
        g2 = Eq(r"\Lambda_2", "=", "N_2", r"(\mu_0 n I_1)", "A", size=M_M)
        g3 = Eq("M", "=", r"\mu_0", "n", "N_2", "A")
        nA = desc("A: seção do solenoide (fora dele, o campo é quase nulo)", 22)
        fitw(nA, 6.6).move_to(P3(EQX, -2.9))
        self.play(FadeIn(g1.mob), ap.oAe.animate.set_value(1), *self.show(L["A"]), FadeIn(nA), run_time=T_EQ)
        self.wait(T_READ)
        self.play(FadeIn(br), FadeIn(bn), run_time=T_FADE)
        self.gm(g1, g2, MP(g1, [0, 1, 2, 4], g2, [0, 1, 2, 4]), name="B1 -> mu0 n I1")
        self.wait(T_BEAT)
        q = g2.p(3)                                        # ( μ 0 n I 1 )
        self.gm(g2, g3, MG(q[1:3], g3.p(2)), MG([q[3]], g3.p(3)), MP(g2, [2], g3, [4]), MP(g2, [4], g3, [5]),
                MP(g2, [1], g3, [1]), pos=P3(EQX, -1.8), copy=True, name="M = mu0 n N2 A")
        b3 = boxed(g3.mob)
        self.play(Create(b3), run_time=T_FADE)
        self.E = VGroup(ch, e1.mob, e2.mob, g2.mob, nA, br, bn)
        self.g3 = VGroup(g3.mob, b3)
        self.wait(T_HOLD)

    # ═══ C04 — reciprocidade ════════════════════════════════════════════════════════════════════════════════
    def c04(self):
        ap, L = self.ap, self.L
        self.sec(4, "reciprocidade")
        self.play(*self.H("Trocando os papéis"), *self.clrE(), self.g3.animate.scale(0.85).move_to(P3(EQX, 2.1)),
                  ap.oAe.animate.set_value(0), *self.hide(L["A"]), ap.oDots.animate.set_value(0),
                  ap.oIA.animate.set_value(0), ap.sw.animate.set_value(SW_OPEN), ap.oBat.animate.set_value(0.3),
                  ap.oFlux.animate.set_value(0), run_time=T_MOVE)
        ap.tc.set_value(0)
        ap.role = 2
        self.play(*self.hide(L["med"], L["E2"], L["I1"]), *self.show(L["fonte"], L["I2"]), ap.oSrc.animate.set_value(1),
                  run_time=T_EQ)
        self.wait(T_BEAT)
        self.play(*self.H("Agora a bobina 2 é a fonte"), *self.show(L["E1"]), ap.oEL.animate.set_value(1),
                  ap.oDots.animate.set_value(1), ap.tc.animate.set_value(0.5), run_time=2.6, rate_func=linear)
        self.run(ap.tc, 1.5, 3.0, *self.H("E a fem aparece no solenoide"))
        self.run(ap.tc, 4.0, 4.0)
        r = Eq("M_{12}", "=", "M_{21}", size=M_XL).at(EQX, 0.4)
        rb = boxed(r.mob)
        rc = desc("mesma geometria, mesmo coeficiente").next_to(rb, DOWN, buff=0.22)
        self.play(FadeIn(r.mob), Create(rb), FadeIn(rc), run_time=T_EQ)
        self.wait(T_HOLD)
        q = fitw(text("E SE O SEGUNDO CIRCUITO DESAPARECER?", 32, CYAN), 6.8).move_to(P3(EQX, -1.6))
        self.play(*self.H("E se o segundo circuito desaparecer?"), FadeIn(q, shift=0.1 * UP), run_time=T_EQ)
        self.E = VGroup(self.g3, r.mob, rb, rc, q)
        self.wait(T_READ)

    # ═══ C05 — mútua vira autoindução ═══════════════════════════════════════════════════════════════════════
    def c05(self):
        ap, L = self.ap, self.L
        self.sec(5, "mutua_vira_autoinducao")
        e1 = Eq(r"\Lambda_2", "=", "M", "I_1", size=M_XL).at(EQX, 1.5)
        e2 = Eq(r"\mathcal E_2", "=", "-", "M", r"\frac{dI_1}{dt}", size=M_XL).at(EQX, 0.0)
        self.play(*self.clrE(), *self.hide(L["E1"], L["I2"], L["fonte"]), ap.oEL.animate.set_value(0),
                  ap.oDots.animate.set_value(0), ap.oBat.animate.set_value(1), run_time=T_MOVE)
        ap.role = 1
        ap.tc.set_value(0)
        ap.oSrc.set_value(0)
        self.play(*self.H("De volta: o solenoide alimenta a bobina 2"), FadeIn(e1.mob), FadeIn(e2.mob),
                  *self.lay("left"), ap.sw.animate.set_value(SW_A), *self.show(L["med"], L["E2"]), run_time=T_MOVE)
        self.play(ap.oDots.animate.set_value(1), ap.oIA.animate.set_value(1), *self.show(L["I1"]),
                  ap.oFlux.animate.set_value(1), ap.tc.animate.set_value(0.3), run_time=2.0, rate_func=linear)
        self.play(*self.H("A bobina 2 sai; o campo fica"), ap.oSec.animate.set_value(0),
                  *self.hide(L["N2"], L["med"], L["E2"]), ap.tc.animate.set_value(0.6), run_time=2.6, rate_func=linear)
        ap.oFlux.set_value(0)
        self.play(*self.H("O campo atravessa as próprias espiras"), ap.oHL.animate.set_value(1),
                  ap.tc.animate.set_value(0.9), run_time=2.6, rate_func=linear)
        self.run(ap.tc, 1.15, 1.6)
        n1 = Eq(r"\Lambda", "=", "L", "I", size=M_XL)
        self.gm(e1, n1, MG([e1.p(0)[0]], n1.p(0)), MP(e1, [1], n1, [1]), MG([e1.p(3)[0]], n1.p(3)), extra=[ap.tc.animate.set_value(1.4), *self.hide(L["I1"]), *self.show(L["I"])],
                name="Lambda2=MI1 -> Lambda=LI")
        nc = desc("L: autoindutância, só depende da geometria", 22).next_to(n1.mob, DOWN, buff=0.22)
        self.play(FadeIn(nc), *self.hide(L["sol"]), *self.show(L["L"]), ap.tc.animate.set_value(1.6), run_time=T_FADE,
                  rate_func=linear)
        self.run(ap.tc, 1.9, T_BEAT)
        n2 = Eq(r"\mathcal E_L", "=", "-", "L", r"\frac{dI}{dt}", size=M_XL)
        an, ab, ad = e2.frac(4)
        bn_, bb, bd = n2.frac(4)
        self.gm(e2, n2, MG([e2.p(0)[0]], [n2.p(0)[0]]), MP(e2, [1, 2], n2, [1, 2]),
                MG(an[:2], bn_), MG([ab], [bb]), MG(ad, bd), extra=[ap.tc.animate.set_value(2.2)],
                name="E2=-M dI1/dt -> EL=-L dI/dt")
        b2 = boxed(n2.mob, buff=0.2)
        un = MathTex(r"[L]=\mathrm{H}=\frac{\mathrm{V\,s}}{\mathrm{A}}", font_size=30, color=DIM).move_to(P3(EQX, -1.5))
        self.play(Create(b2), *self.show(L["EL"]), ap.oEL.animate.set_value(1), ap.oHL.animate.set_value(0),
                  ap.tc.animate.set_value(2.5), run_time=T_EQ, rate_func=linear)
        self.play(FadeIn(un), ap.tc.animate.set_value(3.0), run_time=T_EQ, rate_func=linear)
        self.E = VGroup(n1.mob, nc, n2.mob, b2, un)
        self.run(ap.tc, 4.0, T_READ)

    # ═══ C06 — o que o indutor combate ══════════════════════════════════════════════════════════════════════
    def c06(self):
        ap, L = self.ap, self.L
        self.sec(6, "o_que_o_indutor_combate")
        self.play(*self.H("O que o indutor realmente combate"), *self.clrE(), *self.lay("solo"),
                  ap.oCirc.animate.set_value(0), ap.oDots.animate.set_value(0), *self.hide(L["I"]), run_time=T_MOVE)
        ap.mode = "probe"
        ap.sp.set_value(0)
        gp = self.gp = Graf(self, center=(EQX, -1.55), w=5.4, h=1.9, xmax=3.2, ticks=False, ylab="I", ycol=GREEN)
        gp.curve(lambda x: probe(x)[0], ap.sp, GREEN, 5)
        gp.marker(lambda x: probe(x)[0], ap.sp, GREEN, slope=lambda x: probe(x)[1] * PI / 2)
        nt = desc("corrente imposta por uma fonte ajustável", 22).move_to(P3(EQX, 2.3))
        self.play(*gp.show(), FadeIn(nt), ap.oIS.animate.set_value(1), ap.oDots.animate.set_value(1), run_time=T_EQ)
        self.run(ap.sp, 0.5, 3.0)
        k1 = row(tex(r"\frac{dI}{dt}>0", M_M), tex(r"\Rightarrow", M_M), tex(r"\mathcal E_L", M_M),
                 desc("contra a corrente", 26, WHITE)).move_to(P3(EQX, 1.35))
        self.play(FadeIn(k1), run_time=T_EQ)
        self.wait(T_READ)
        self.run(ap.sp, 2.5, 7.0)
        k2 = row(tex(r"\frac{dI}{dt}<0", M_M), tex(r"\Rightarrow", M_M), tex(r"\mathcal E_L", M_M),
                 desc("a favor da corrente", 26, WHITE)).move_to(P3(EQX, 0.35))
        self.play(FadeIn(k2), run_time=T_EQ)
        self.wait(T_READ)
        self.run(ap.sp, 3.0, 1.8)
        # payoff tipográfico
        p1 = fitw(text("O INDUTOR NÃO SE OPÕE À CORRENTE", 40, WHITE), 12.5).move_to(P3(0, 0.0))
        p2 = row(text("ELE SE OPÕE À", 40, WHITE), text("MUDANÇA", 46, CYAN), text("DA CORRENTE", 40, WHITE),
                 buff=0.28)
        fitw(p2, 12.8).move_to(P3(0, 0.0))
        dim = Rectangle(width=16, height=6.2).set_fill(BACKGROUND_COLOR, 0.88).set_stroke(width=0) \
            .move_to(P3(0, -0.4)).set_z_index(25)
        p1.set_z_index(26)
        p2.set_z_index(26)
        self.play(FadeIn(dim), FadeIn(p1, shift=0.1 * UP), run_time=T_EQ)
        self.wait(T_READ)
        self.play(soft_swap(p1, p2), run_time=1.6)
        self.play(p2[1].animate.scale(1.12), run_time=0.5)
        self.play(p2[1].animate.scale(1 / 1.12), run_time=0.5)
        self.wait(T_HOLD)
        self.play(FadeOut(p2), FadeOut(dim), FadeOut(k1), FadeOut(k2), ap.oDots.animate.set_value(0), run_time=T_FADE)
        ap.sp.set_value(0)
        self.play(*self.H("E com corrente constante?"), ap.oDots.animate.set_value(1), run_time=T_FADE)
        self.run(ap.sp, 1.5, 4.5)
        z = VGroup(tex(r"I\neq0"), tex(r"B\neq0"), tex(r"\frac{dI}{dt}=0"), tex(r"\mathcal E_L=0")) \
            .arrange_in_grid(2, 2, buff=(1.3, 0.4)).move_to(P3(EQX, 0.95))
        self.play(LaggedStart(*[FadeIn(m) for m in z], lag_ratio=0.5), run_time=2.6)
        self.ring(z[3].get_center(), z[3].width + 0.4, z[3].height + 0.3, CYAN)
        self.E = VGroup(nt, z)
        self.wait(T_HOLD)

    # ═══ C07 — equação RL ═══════════════════════════════════════════════════════════════════════════════════
    def c07(self):
        ap, L, gp = self.ap, self.L, self.gp
        self.sec(7, "equacao_rl")
        self.play(*self.H("De volta ao circuito: a lei das malhas"), *self.clrE(), *gp.hide(), *self.lay("left"),
                  ap.oCirc.animate.set_value(1), ap.oIS.animate.set_value(0), ap.oDots.animate.set_value(0),
                  run_time=T_MOVE)
        gp.drop()
        ap.mode = "charge"
        ap.tc.set_value(0.9)
        self.play(ap.oDots.animate.set_value(1), ap.oIA.animate.set_value(1), *self.show(L["I"]), run_time=T_FADE)
        eq = Eq(r"\mathcal E_0", "-", "L", r"\frac{dI}{dt}", "=", "R", "I", size=M_XL) \
            .at(EQX, 1.0)
        tE = paint(MathTex(r"+\mathcal E_0", font_size=34)).move_to(self.Wl("left", XL, 0) + P3(-0.45, 0.95))
        tL = paint(MathTex(r"-L\frac{dI}{dt}", font_size=34)).move_to(self.Wl("left", XC, YT) + P3(1.85, 0.8))
        tR = paint(MathTex(r"-RI", font_size=34)).move_to(self.Wl("left", XR, 0) + P3(0.05, 0.95))
        for t in (tE, tL, tR):
            t.set_stroke(BACKGROUND_COLOR, 8, background=True).set_z_index(22)
        self.play(*self.H("A fonte empurra"), run_time=T_FADE)
        self.ring(self.Wl("left", XL, 0), 1.0, 1.0, CYAN)
        self.play(FadeIn(tE, shift=0.1 * UP), run_time=T_FADE)
        self.play(TransformFromCopy(VGroup(*tE[0][1:]), VGroup(*eq.g(0))), run_time=T_EQ)
        self.wait(T_BEAT)
        self.play(*self.H("O indutor reage"), run_time=T_FADE)
        self.ring(self.Wl("left", XC, YT), 3.0, 1.2, CYAN)
        self.play(FadeIn(tL, shift=0.1 * UP), run_time=T_FADE)
        self.play(TransformFromCopy(VGroup(*tL[0]), VGroup(*eq.g(1, 2, 3))), run_time=T_EQ)
        self.wait(T_BEAT)
        self.play(*self.H("O resistor consome"), run_time=T_FADE)
        self.ring(self.Wl("left", XR, 0), 0.9, 1.4, HEAT)
        self.play(FadeIn(tR, shift=0.1 * UP), run_time=T_FADE)
        self.play(FadeIn(VGroup(*eq.g(4))), TransformFromCopy(VGroup(*tR[0][1:]), VGroup(*eq.g(5, 6))), run_time=T_EQ)
        self.remove(*eq.g(0, 1, 2, 3, 4, 5, 6))
        self.add(eq.mob)
        cs = desc("ao dar a volta na malha, as tensões somam zero", 22).move_to(P3(EQX, 0.0))
        self.play(FadeIn(cs), run_time=T_FADE)
        self.wait(T_READ)
        eq2 = Eq("L", r"\frac{dI}{dt}", "+", "R", "I", "=", r"\mathcal E_0", size=M_XL)
        self.play(*self.H("Organizando"), FadeOut(cs), run_time=T_FADE)
        self.gm(eq, eq2, MP(eq, [2, 3], eq2, [0, 1], path_arc=-PI / 3), MP(eq, [5, 6], eq2, [3, 4], path_arc=-PI / 2),
                MP(eq, [4], eq2, [5]), MP(eq, [0], eq2, [6], path_arc=-0.9 * PI), name="malha reorganizada")
        self.E = VGroup(eq2.mob, tE, tL, tR)
        self.eq2 = eq2
        self.wait(T_HOLD)

    # ═══ C08 — resolver a dinâmica ══════════════════════════════════════════════════════════════════════════
    def step(self, s):
        new = desc(s, 24).move_to(P3(EQX, -1.5))
        old, self.stp = self.stp, new
        return [soft_swap(old, new)] if old is not None else [FadeIn(new)]

    def c08(self):
        self.sec(8, "resolver_dinamica")
        e1 = self.eq2
        tE, tL, tR = self.E[1:]
        y = 0.25
        self.stp = None
        self.play(*self.H("Resolvendo a dinâmica"), FadeOut(VGroup(tE, tL, tR)), e1.mob.animate.move_to(P3(EQX, y)),
                  run_time=T_MOVE)
        self.E = VGroup()
        self.wait(T_BEAT)
        # 1) dividir por L
        e2 = Eq(r"\frac{dI}{dt}", "=", r"\frac{\mathcal E_0-RI}{L}", size=M_XL)
        n2, b2, d2 = e2.frac(2)
        self.play(*self.step("dividimos tudo por L"), run_time=T_FADE)
        self.gm(e1, e2, MP(e1, [1], e2, [0]), MP(e1, [5], e2, [1]), MG(e1.p(6), n2[:2], path_arc=PI / 2),
                MG(e1.p(3), [n2[3]]), MG(e1.p(4), [n2[4]]), MG(e1.p(0), d2, path_arc=-PI / 3), name="dividir por L")
        self.wait(T_READ)
        # 2) colocar R/L em evidência
        e3 = Eq(r"\frac{dI}{dt}", "=", r"\frac{R}{L}", r"\Big(", r"\frac{\mathcal E_0}{R}", "-", "I", r"\Big)", size=M_XL)
        rn, rb, rd = e3.frac(2)
        en, eb, ed = e3.frac(4)
        self.play(*self.step("colocamos R/L em evidência"), run_time=T_FADE)
        self.gm(e2, e3, MP(e2, [0, 1], e3, [0, 1]), MG([n2[3]], rn, path_arc=PI / 2), MG(d2, rd), MG(n2[:2], en, path_arc=PI / 2), MG([n2[2]], e3.p(5)),
                MG([n2[4]], e3.p(6)), MG([b2], [rb]), name="R/L em evidencia")
        self.wait(T_READ)
        # 3) definições
        d1 = Eq(r"I_\infty", "=", r"\frac{\mathcal E_0}{R}", size=M_M).at(EQX - 1.7, 2.1)
        dd = Eq(r"\tau", "=", r"\frac{L}{R}", size=M_M).at(EQX + 1.7, 2.1)
        c1 = desc("corrente final", 22).next_to(d1.mob, DOWN, buff=0.12)
        c2 = desc("constante de tempo", 22).next_to(dd.mob, DOWN, buff=0.12)
        self.play(*self.step("damos nome às duas combinações"), run_time=T_FADE)
        self.play(TransformFromCopy(VGroup(*e3.g(4)), VGroup(*d1.g(2))), FadeIn(VGroup(*d1.g(0, 1))), FadeIn(c1),
                  run_time=T_EQ)
        self.remove(*d1.g(0, 1, 2))
        self.add(d1.mob)
        self.play(TransformFromCopy(VGroup(*e3.g(2)), VGroup(*dd.g(2))), FadeIn(VGroup(*dd.g(0, 1))), FadeIn(c2),
                  run_time=T_EQ)
        self.remove(*dd.g(0, 1, 2))
        self.add(dd.mob)
        self.wait(T_READ)
        e4 = Eq(r"\frac{dI}{dt}", "=", r"\frac{I_\infty-I}{\tau}", size=M_XL)
        n4, b4, d4 = e4.frac(2)
        self.play(*self.step("substituímos"), run_time=T_FADE)
        self.gm(e3, e4, MP(e3, [0, 1], e4, [0, 1]), CG(d1.g(0), n4[:2]), MG(e3.p(5), [n4[2]]), MG(e3.p(6), [n4[3]]),
                CG(dd.g(0), d4), MG([rb], [b4]), name="substituir I_inf e tau")
        self.wait(T_BEAT)
        self.play(*self.step("longe do valor final, a corrente muda depressa"), run_time=T_FADE)
        self.wait(T_READ)
        # 4) separar variáveis
        e5 = Eq(r"\frac{dI}{I_\infty-I}", "=", r"\frac{dt}{\tau}", size=M_XL)
        a5, ab5, ad5 = e5.frac(0)
        c5, cb5, cd5 = e5.frac(2)
        a4, ab4, ad4 = e4.frac(0)
        self.play(*self.step("separamos as variáveis"), run_time=T_FADE)
        self.gm(e4, e5, MG(a4, a5), MG([ab4], [ab5]), MG(ad4, c5, path_arc=-0.7 * PI), MG(n4, ad5, path_arc=-0.7 * PI),
                MG([b4], [cb5]), MG(d4, cd5), MP(e4, [1], e5, [1]), name="separar variaveis")
        self.wait(T_READ)
        # 5) integrar com I(0) = 0
        e6 = Eq(r"\int_0^{I}", r"\frac{dI}{I_\infty-I}", "=", r"\int_0^{t}", r"\frac{dt}{\tau}", size=M_XL)
        self.play(*self.step("integramos desde t = 0, quando I = 0"), run_time=T_FADE)
        self.gm(e5, e6, MP(e5, [0], e6, [1]), MP(e5, [1], e6, [2]), MP(e5, [2], e6, [4]), name="integrar")
        self.wait(T_READ)
        e7 = Eq(r"-\ln\frac{I_\infty-I}{I_\infty}", "=", r"\frac{t}{\tau}", size=M_XL)
        f6n, f6b, f6d = e6.frac(1)
        t6n, t6b, t6d = e6.frac(4)
        n7, b7, d7 = e7.frac(0)
        t7n, t7b, t7d = e7.frac(2)
        self.play(*self.step("resolvemos as duas integrais"), run_time=T_FADE)
        self.gm(e6, e7, MG(f6d, n7), MP(e6, [2], e7, [1]), MG([t6n[1]], t7n), MG([t6b], [t7b]), MG(t6d, t7d),
                name="resolver integrais")
        self.wait(T_READ)
        # 6) exponenciar e isolar
        e8 = Eq(r"\frac{I_\infty-I}{I_\infty}", "=", r"e^{-t/\tau}", size=M_XL)
        n8, b8, d8 = e8.frac(0)
        ex = e8.p(2)
        self.play(*self.step("exponenciamos"), run_time=T_FADE)
        self.gm(e7, e8, MG(n7, n8), MG([b7], [b8]), MG(d7, d8), MP(e7, [1], e8, [1]), MG([e7.p(0)[0]], [ex[1]]),
                MG(t7n, [ex[2]]), MG([t7b], [ex[3]]), MG(t7d, [ex[4]]), name="exponenciar")
        self.wait(T_READ)
        e9 = Eq("I(t)", "=", r"I_\infty", r"\left(1-e^{-t/\tau}\right)", size=M_XL)
        self.play(*self.step("isolamos a corrente"), run_time=T_FADE)
        p9 = e9.p(3)
        self.gm(e8, e9, MG(d8, e9.p(2)), MP(e8, [1], e9, [1]), MG(ex, p9[3:8]), MG([n8[3]], e9.p(0)[:1]),
                name="isolar I")
        b9 = boxed(e9.mob, buff=0.2)
        ck = row(tex(r"I(0)=0", M_S), tex(r"I(\infty)=I_\infty", M_S), buff=0.8).move_to(P3(EQX, -0.75))
        self.play(Create(b9), FadeIn(ck), *self.step("e conferimos os dois limites"), run_time=T_EQ)
        self.E = VGroup(d1.mob, dd.mob, c1, c2, e9.mob, b9, ck, self.stp)
        self.wait(T_HOLD)

    # ═══ C09 — uma escala controla tudo ═════════════════════════════════════════════════════════════════════
    def c09(self):
        ap, L = self.ap, self.L
        self.sec(9, "escala_tau")
        d1, dd, c1, c2, e9m, b9, ck, stp = self.E
        top = VGroup(e9m, b9)
        g = self.g = Graf(self, one=r"I_\infty", ylab="I", ycol=GREEN)
        self.play(*self.H("Uma única escala de tempo controla tudo"), FadeOut(VGroup(d1, dd, c1, c2, ck, stp)),
                  top.animate.scale(0.7).move_to(P3(EQX, 2.2)), *g.show(), ap.oEB.animate.set_value(1),
                  ap.oEL.animate.set_value(1), *self.show(L["EL"]), run_time=T_MOVE)
        g.curve(lambda x: 1 - math.exp(-x), ap.tc, GREEN, 5)
        g.marker(lambda x: 1 - math.exp(-x), ap.tc, GREEN)
        self.rewind(ap.tc, g)
        tg = DashedLine(g.c2p(0, 0), g.c2p(1, 1), dash_length=0.08, color=VIOLET, stroke_width=3).set_z_index(5)
        tl = row(desc("inclinação", 22, VIOLET), tex(r"\frac{\mathcal E_0}{L}", 30), buff=0.1) \
            .next_to(g.c2p(1, 1), RIGHT, buff=0.15).shift(0.15 * DOWN)
        p0 = row(tex(r"t=0:", M_S), tex(r"I=0", M_S), tex(r"\frac{dI}{dt}=\frac{\mathcal E_0}{L}", M_S),
                 tex(r"|\mathcal E_L|=\mathcal E_0", M_S), buff=0.45).move_to(P3(EQX, 1.35))
        fl = desc("a seta da fem tem o tamanho da seta da bateria", 22).move_to(P3(EQX, 0.95))
        self.play(FadeIn(p0), run_time=T_EQ)
        self.play(Create(tg), FadeIn(tl), FadeIn(fl), run_time=T_EQ)
        self.wait(T_READ)
        self.play(FadeOut(fl), run_time=0.5)
        self.run(ap.tc, 1.0, 4.5)
        # t = τ: evento visual forte
        y1 = 1 - math.exp(-1)
        vl = Line(g.c2p(1, 0), g.c2p(1, 1.1)).set_stroke(VIOLET, 4).set_z_index(8)
        mk = VGroup(DashedLine(g.c2p(0, y1), g.c2p(1, y1), dash_length=0.06, color=WHITE, stroke_width=2.5),
                    MathTex(r"I(\tau)\approx0{,}632\,I_\infty", font_size=30, color=GREEN)
                    .next_to(g.c2p(1, y1), RIGHT, buff=0.22).shift(0.28 * DOWN)).set_z_index(8)
        tt = MathTex(r"t=\tau", font_size=40, color=VIOLET).next_to(g.c2p(1, 1.1), UP, buff=0.05).set_z_index(8)
        self.play(Create(vl), FadeIn(tt, scale=1.3), run_time=0.8)
        self.play(FadeIn(mk), FadeOut(tl), run_time=T_EQ)
        self.wait(T_READ)
        self.play(vl.animate.set_stroke(opacity=0.35), run_time=0.5)
        self.run(ap.tc, 5.0, 7.0)
        p1 = row(tex(r"t\gg\tau:", M_S), tex(r"I\to I_\infty", M_S), tex(r"\frac{dI}{dt}\to0", M_S),
                 tex(r"\mathcal E_L\to0", M_S), buff=0.45).move_to(P3(EQX, 1.35))
        self.play(soft_swap(p0, p1), run_time=1.4)
        self.E = VGroup(top, tg, mk, vl, tt, p1)
        self.wait(T_HOLD)

    # ═══ C10 — B cresce, E induzido some (vista lateral → axial do mesmo solenoide) ═════════════════════════
    def c10(self):
        ap, L = self.ap, self.L
        self.sec(10, "b_cresce_e_some")
        g = self.g
        self.play(*self.H("Olhando o solenoide de frente"), *self.clrE(), *g.hide(), ap.oEB.animate.set_value(0),
                  ap.oEL.animate.set_value(0), *self.hide(L["E0"], L["R"], L["I"], L["L"], L["B"], L["EL"]),
                  run_time=T_MOVE)
        g.drop()
        self.play(*self.lay("axial"), ap.ang.animate.set_value(-PI / 2), run_time=3.2, rate_func=smooth)
        bl = row(tex(r"\mathbf B", 34, MAGENTA), desc("saindo da tela", 22, MAGENTA), buff=0.12) \
            .move_to(self.Wl("axial", XC, YT) + P3(0, -2.45))
        self.play(FadeIn(bl), *self.show(L["a"]), run_time=T_FADE)
        b1 = Eq("B(t)", "=", r"\mu_0 n", "I(t)", size=M_L).at(2.9, 2.1)
        self.play(FadeIn(b1.mob), run_time=T_EQ)
        self.wait(T_BEAT)
        self.rewind(ap.tc)
        self.play(*self.H("A corrente muda: surge um campo elétrico em anéis"), ap.oEr.animate.set_value(1),
                  ap.tc.animate.set_value(0.08), run_time=1.6, rate_func=linear)
        b2 = Eq(r"\frac{dB}{dt}", "=", r"\mu_0 n", r"\frac{dI}{dt}", size=M_L).at(2.9, 0.95)
        self.play(FadeIn(b2.mob), ap.tc.animate.set_value(0.16), run_time=T_EQ, rate_func=linear)
        r1 = Eq(r"E_\phi", "=", r"-\frac{\mu_0 n r}{2}", r"\frac{dI}{dt}", size=M_L).at(3.3, -0.4)
        l1 = tex(r"r<a", 34).next_to(r1.mob, LEFT, buff=0.35)
        self.play(FadeIn(r1.mob), FadeIn(l1), ap.tc.animate.set_value(0.25), run_time=T_EQ, rate_func=linear)
        self.run(ap.tc, 0.35, 2.0)
        r2 = Eq(r"E_\phi", "=", r"-\frac{\mu_0 n a^2}{2r}", r"\frac{dI}{dt}", size=M_L)
        l2 = tex(r"r>a", 34)
        r2.mob.move_to(r1.mob)
        l2.next_to(r2.mob, LEFT, buff=0.35)
        self.gm(r1, r2, MP(r1, [0, 1, 3], r2, [0, 1, 3]), extra=[soft_swap(l1, l2), ap.tc.animate.set_value(0.45)],
                rt=1.6, name="E_phi dentro -> fora")
        nb = desc("máximo na parede; fora, cai com 1/r", 22).move_to(P3(3.3, -1.45))
        self.play(FadeIn(nb), ap.tc.animate.set_value(0.6), run_time=T_FADE, rate_func=linear)
        self.run(ap.tc, 5.0, T_RUN, *self.H("B cresce enquanto o campo elétrico induzido some"))
        pf = row(text("REGIME:", 28, WHITE), tex(r"B\neq0", M_L), tex(",", M_L), tex(r"E_{\rm ind}=0", M_L), buff=0.25) \
            .move_to(P3(2.9, -2.65))
        pb = boxed(pf, buff=0.2)
        self.play(FadeIn(pf), Create(pb), run_time=T_EQ)
        self.E = VGroup(b1.mob, b2.mob, r2.mob, l2, nb, pf, pb, bl)
        self.wait(T_HOLD)

    # ═══ C11 — construir o campo custa energia ══════════════════════════════════════════════════════════════
    def c11(self):
        ap, L = self.ap, self.L
        self.sec(11, "custo_energia")
        self.play(*self.clrE(), ap.oEr.animate.set_value(0), *self.hide(L["a"]), run_time=T_FADE)
        self.play(*self.H("Construir o campo custa energia"), *self.lay("left"), ap.ang.animate.set_value(ANG0),
                  run_time=3.0, rate_func=smooth)
        self.play(*self.show(L["E0"], L["R"], L["I"], L["L"], L["B"]), run_time=T_FADE)
        self.rewind(ap.tc)
        self.play(ap.oGauge.animate.set_value(1), ap.oGb.animate.set_value(1), *self.show(L["Gb"]),
                  ap.tc.animate.set_value(0.3), run_time=2.0, rate_func=linear)
        nb = desc("a bateria entrega potência", 24).move_to(P3(EQX, 2.1))
        self.play(FadeIn(nb), ap.tc.animate.set_value(0.6), run_time=T_EQ, rate_func=linear)
        self.play(ap.oGr.animate.set_value(1), *self.show(L["Gr"]), ap.tc.animate.set_value(0.9), run_time=2.0,
                  rate_func=linear)
        nr = desc("parte esquenta o resistor…", 24, HEAT).move_to(P3(EQX, 1.55))
        self.play(FadeIn(nr), ap.tc.animate.set_value(1.2), run_time=T_EQ, rate_func=linear)
        self.play(ap.oGs.animate.set_value(1), *self.show(L["Gs"]), ap.tc.animate.set_value(1.5), run_time=2.0,
                  rate_func=linear)
        ns = desc("…e parte vai para o campo", 24, MAGENTA).move_to(P3(EQX, 1.0))
        self.play(FadeIn(ns), ap.tc.animate.set_value(1.8), run_time=T_EQ, rate_func=linear)
        self.run(ap.tc, 4.5, 6.0)
        # a mesma ideia na equação: multiplicar a malha por I
        self.play(FadeOut(VGroup(nb, nr, ns)), run_time=T_FADE)
        self.rewind(ap.tc)
        self.run(ap.tc, 0.6, 1.5)
        eq = Eq(r"\mathcal E_0", "-", "L", r"\frac{dI}{dt}", "=", "R", "I", size=M_XL) \
            .at(EQX, 1.2)
        self.play(FadeIn(eq.mob), ap.tc.animate.set_value(0.8), run_time=T_EQ, rate_func=linear)
        xI = MathTex(r"\times", "I", font_size=M_XL).next_to(eq.mob, RIGHT, buff=0.35)
        xI[1].set_color(GREEN)
        self.play(FadeIn(xI, shift=0.2 * LEFT), ap.tc.animate.set_value(1.0), run_time=T_EQ, rate_func=linear)
        eqI = Eq(r"\mathcal E_0", "I", "-", "L", "I", r"\frac{dI}{dt}", "=", "R", "I^2", size=M_XL,
                 ).at(EQX, 1.2)
        self.gm(eq, eqI, MP(eq, [0], eqI, [0]), MP(eq, [1], eqI, [2]), MP(eq, [2], eqI, [3]), MP(eq, [3], eqI, [5]),
                MP(eq, [4], eqI, [6]), MP(eq, [5], eqI, [7]), MG(eq.p(6), [eqI.p(8)[0]]),
                CG(list(xI[1]), eqI.p(1)), CG(list(xI[1]), eqI.p(4)), pos=P3(EQX, 1.2),
                extra=[FadeOut(xI, rate_func=_first_half), ap.tc.animate.set_value(1.3)], name="multiplicar por I")
        bs = [Brace(VGroup(*eqI.g(0, 1)), DOWN, buff=0.12, color=DIM),
              Brace(VGroup(*eqI.g(3, 4, 5)), DOWN, buff=0.12, color=MAGENTA),
              Brace(VGroup(*eqI.g(7, 8)), DOWN, buff=0.12, color=HEAT)]
        ls = [desc("fonte", 22, WHITE), desc("?", 26, MAGENTA), desc("resistor", 22, HEAT)]
        for b, l in zip(bs, ls):
            l.next_to(b, DOWN, buff=0.1)
        self.play(FadeIn(bs[0]), FadeIn(ls[0]), FadeIn(bs[2]), FadeIn(ls[2]), ap.tc.animate.set_value(1.7),
                  run_time=T_EQ, rate_func=linear)
        self.play(FadeIn(bs[1]), FadeIn(ls[1]), ap.tc.animate.set_value(2.1), run_time=T_EQ, rate_func=linear)
        self.E = VGroup(*bs, *ls)
        self.eqI = eqI
        self.run(ap.tc, 2.7, T_READ)

    # ═══ C12 — a potência se divide ═════════════════════════════════════════════════════════════════════════
    def c12(self):
        ap = self.ap
        self.sec(12, "potencia_se_divide")
        eqI = self.eqI
        self.play(*self.H("A potência se divide"), *self.clrE(), run_time=T_FADE)
        e1 = Eq(r"\mathcal E_0", "I", "=", "I^2", "R", "+", "L", "I", r"\frac{dI}{dt}", size=M_XL,
)
        self.gm(eqI, e1, MP(eqI, [0, 1], e1, [0, 1]), MP(eqI, [6], e1, [2]), MP(eqI, [8], e1, [3], path_arc=0.8 * PI),
                MP(eqI, [7], e1, [4], path_arc=0.8 * PI), MP(eqI, [3, 4, 5], e1, [6, 7, 8], path_arc=0.8 * PI),
                name="rearranjar balanco")
        self.wait(T_READ)
        side = Eq("L", "I", r"\frac{dI}{dt}", "=", r"\frac{d}{dt}", r"\Big(", r"\tfrac12", "L", "I^2", r"\Big)",
                  size=M_L).at(EQX, -0.4)
        sc = row(desc("regra da cadeia:", 22), tex(r"\frac{d(I^2)}{dt}=2I\frac{dI}{dt}", 30), buff=0.12) \
            .next_to(side.mob, DOWN, buff=0.25)
        self.play(TransformFromCopy(VGroup(*e1.g(6, 7, 8)), VGroup(*side.g(0, 1, 2))),
                  FadeIn(VGroup(*side.g(3, 4, 5, 6, 7, 8, 9))), FadeIn(sc), run_time=T_EQ)
        self.remove(*side.g(0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
        self.add(side.mob)
        self.wait(T_READ)
        e2 = Eq(r"\mathcal E_0", "I", "=", "I^2", "R", "+", r"\frac{d}{dt}", r"\Big(", r"\tfrac12", "L", "I^2", r"\Big)",
                size=M_XL)
        fitw(e2.mob, 7.0)
        self.gm(e1, e2, MP(e1, [0, 1, 2, 3, 4, 5], e2, [0, 1, 2, 3, 4, 5]), CP(side.g(4, 5, 6, 7, 8, 9), e2,
                                                                              [6, 7, 8, 9, 10, 11]),
                extra=[FadeOut(sc)], name="substituir L I dI/dt")
        self.play(FadeOut(side.mob), run_time=T_FADE)
        self.wait(T_BEAT)
        # nomes: cada termo é uma potência
        names = [MathTex(r"P_{\rm fonte}", font_size=36), MathTex(r"P_{\rm Joule}", font_size=36, color=HEAT),
                 MathTex(r"\frac{dU_B}{dt}", font_size=36, color=MAGENTA)]
        grp = [e2.g(0, 1), e2.g(3, 4), e2.g(6, 7, 8, 9, 10, 11)]
        brs = [Brace(VGroup(*gg), DOWN, buff=0.12, color=c) for gg, c in zip(grp, (WHITE, HEAT, MAGENTA))]
        for n, b in zip(names, brs):
            n.next_to(b, DOWN, buff=0.1)
        self.play(*self.H("Cada termo é uma potência"), LaggedStart(*[AnimationGroup(FadeIn(b), FadeIn(n))
                                                                      for b, n in zip(brs, names)], lag_ratio=0.6),
                  run_time=2.4)
        self.wait(T_READ)
        f = Eq(r"P_{\rm fonte}", "=", r"P_{\rm Joule}", "+", r"\frac{dU_B}{dt}", size=64).at(EQX, 1.25)
        self.play(*self.H("O balanço de potência"), FadeOut(e2.mob, rate_func=_first_half),
                  FadeOut(VGroup(*brs), rate_func=_first_half),
                  *[ReplacementTransform(n, VGroup(*f.g(i))) for n, i in zip(names, (0, 2, 4))],
                  FadeIn(VGroup(*f.g(1, 3)), rate_func=_second_half), run_time=T_MORPH)
        self.remove(*f.g(0, 1, 2, 3, 4))
        self.add(f.mob)
        fb = boxed(f.mob, buff=0.22)
        self.play(Create(fb), run_time=T_FADE)
        self.wait(T_READ)
        u = Eq("U_B", "=", r"\tfrac12", "L", "I^2", size=M_XL).at(EQX, -0.35)
        un = desc("energia guardada no campo", 22, MAGENTA).next_to(u.mob, DOWN, buff=0.25)
        self.play(FadeIn(u.mob), run_time=T_EQ)
        ub = boxed(u.mob, color=MAGENTA, buff=0.2)
        self.play(Create(ub), FadeIn(un), run_time=T_FADE)
        self.wait(T_HOLD)
        # o mesmo transitório, agora lido pelos medidores
        self.play(VGroup(f.mob, fb).animate.scale(0.75).move_to(P3(EQX, 2.15)),
                  VGroup(u.mob, ub, un).animate.scale(0.85).move_to(P3(EQX, 0.95)), run_time=T_MOVE)
        self.rewind(ap.tc)
        lg = VGroup(desc("início: quase tudo vai para o campo", 22, MAGENTA),
                    desc("regime: tudo vira calor no resistor", 22, HEAT)).arrange(DOWN, buff=0.18).move_to(P3(EQX, -0.75))
        self.play(FadeIn(lg[0]), ap.tc.animate.set_value(0.6), run_time=2.5, rate_func=linear)
        self.run(ap.tc, 2.5, 0.5 * T_RUN)
        self.run(ap.tc, 5.0, 0.7 * T_RUN, FadeIn(lg[1]))
        self.E = VGroup(f.mob, fb, un, lg)
        self.U = VGroup(u.mob, ub)
        self.wait(T_HOLD)

    # ═══ C13 — onde está a energia? ═════════════════════════════════════════════════════════════════════════
    def c13(self):
        ap, L = self.ap, self.L
        self.sec(13, "onde_esta_energia")
        self.play(*self.H("Onde está essa energia?"), *self.clrE(), ap.oGauge.animate.set_value(0),
                  *self.hide(L["Gb"], L["Gr"], L["Gs"]), ap.tc.animate.set_value(6.0), run_time=T_FADE)
        self.play(*self.lay("soloc"), ap.oCirc.animate.set_value(0), *self.hide(L["L"], L["B"], L["E0"], L["R"], L["I"]),
                  self.U.animate.move_to(P3(0, -1.55)), run_time=3.0)
        self.play(ap.oB.animate.set_value(1.35), run_time=1.5)
        self.wait(T_READ)
        q = text("ONDE ESTÁ ESSA ENERGIA?", 44, CYAN).move_to(P3(0, -2.75))
        self.play(FadeIn(q, shift=0.1 * UP), run_time=T_EQ)
        hint = desc("no fio? na bateria? ou no próprio campo?", 26).move_to(P3(0, 2.45))
        self.play(FadeIn(hint), run_time=T_FADE)
        self.wait(T_HOLD)
        self.E = VGroup(q, hint)

    # ═══ C14 — densidade de energia ═════════════════════════════════════════════════════════════════════════
    def c14(self):
        ap, L = self.ap, self.L
        self.sec(14, "densidade_energia")
        self.play(*self.H("O volume dentro do solenoide"), *self.clrE(), FadeOut(self.U), *self.lay("solo"),
                  ap.oB.animate.set_value(0.6), run_time=T_MOVE)
        # geometria primeiro: seção A, comprimento ℓ, volume varrido
        self.play(ap.oAe.animate.set_value(1), *self.show(L["A"]), run_time=T_EQ)
        ta = desc("A: área da seção", 24, GEO).move_to(P3(EQX, 2.1))
        self.play(FadeIn(ta), run_time=T_FADE)
        self.wait(T_BEAT)
        self.play(ap.oVol.animate.set_value(1), *self.show(L["ell"]), run_time=T_EQ)
        tl = desc("ℓ: comprimento", 24, GEO).move_to(P3(EQX, 1.6))
        self.play(FadeIn(tl), run_time=T_FADE)
        self.wait(T_BEAT)
        self.play(*self.H("A seção, arrastada ao longo de ℓ, varre o volume"), ap.oSweep.animate.set_value(1),
                  run_time=3.5, rate_func=linear)
        vv = Eq("V", "=", r"A\ell", size=M_L).at(EQX, 0.7)
        self.play(FadeIn(vv.mob), run_time=T_EQ)
        self.wait(T_READ)
        self.play(ap.oSweep.animate.set_value(0), ap.oB.animate.set_value(1.0), FadeOut(VGroup(ta, tl)),
                  vv.mob.animate.scale(0.8).move_to(P3(EQX + 2.15, 2.1)), run_time=T_MOVE)
        # agora a álgebra
        g1 = Eq(r"\mathbf B", "=", r"\mu_0 n", "I", size=M_M).at(EQX - 2.1, 2.1)
        g2 = Eq("L", "=", r"\mu_0 n^2", r"A\ell", size=M_M).at(EQX, 2.1)
        self.play(*self.H("Agora a álgebra"), FadeIn(g1.mob), FadeIn(g2.mob), run_time=T_EQ)
        s0 = Eq("U_B", "=", r"\tfrac12", "L", "I^2", size=M_XL).at(EQX, 0.55)
        self.play(FadeIn(s0.mob), run_time=T_EQ)
        self.wait(T_BEAT)
        s1 = Eq("U_B", "=", r"\tfrac12", r"\mu_0 n^2", r"A\ell", "I^2", size=M_XL)
        self.gm(s0, s1, MP(s0, [0, 1, 2], s1, [0, 1, 2]), MP(s0, [4], s1, [5]), CP(g2.g(2), s1, [3]),
                CP(g2.g(3), s1, [4]), name="L -> mu0 n2 A l")
        self.wait(T_READ)
        s2 = Eq("U_B", "=", r"\frac{1}{2\mu_0}", r"(\mu_0 n I)^2", r"A\ell", size=M_XL)
        hn, hb, hd = s1.frac(2)
        fn, fb_, fd = s2.frac(2)
        mu = s1.px(3)                                     # μ 0 n 2
        pp = s2.px(3)                                     # ( μ 0 n I ) 2
        ii = s1.p(5)                                      # I 2
        self.gm(s1, s2, MP(s1, [0, 1], s2, [0, 1]), MG(hn, fn), MG([hb], [fb_]), MG(hd, [fd[0]]),
                MG(mu[:3], pp[1:4]), MG([mu[3]], [pp[6]]), MG([ii[0]], [pp[4]], path_arc=PI / 2), MP(s1, [4], s2, [4], path_arc=PI / 2),
                name="reagrupar (mu0 n I)^2 / 2mu0")
        self.wait(T_READ)
        s3 = Eq("U_B", "=", r"\frac{B^2}{2\mu_0}", r"A\ell", size=M_XL)
        qn, qb, qd = s3.frac(2)
        self.gm(s2, s3, MP(s2, [0, 1, 4], s3, [0, 1, 3]), MG([pp[6]], [qn[1]]), MG([fb_], [qb]),
                MG(fd, qd), name="mu0 n I -> B")
        self.wait(T_READ)
        # Aℓ é o volume: a geometria volta
        self.play(*self.H("Aℓ é o volume que o campo ocupa"), ap.oSweep.animate.set_value(1),
                  VGroup(*s3.g(3)).animate.set_color(MAGENTA).scale(1.15), run_time=2.0)
        self.play(VGroup(*s3.g(3)).animate.scale(1 / 1.15), run_time=0.5)
        s4 = Eq("U_B", "=", r"\frac{B^2}{2\mu_0}", "V", size=M_XL)
        self.gm(s3, s4, MP(s3, [0, 1, 2], s4, [0, 1, 2]), CP(vv.g(0), s4, [3]), name="A l -> V")
        br = Brace(VGroup(*s4.g(2)), DOWN, buff=0.12, color=MAGENTA)
        bu = row(tex("u_B", 34, MAGENTA), desc("energia por volume", 22, MAGENTA), buff=0.12).next_to(br, DOWN, buff=0.1)
        self.play(FadeIn(br), FadeIn(bu), run_time=T_EQ)
        self.wait(T_READ)
        s5 = Eq("U_B", "=", "u_B", "V", size=M_XL)
        self.gm(s4, s5, MP(s4, [0, 1, 3], s5, [0, 1, 3]), extra=[FadeOut(br, rate_func=_first_half), FadeOut(bu, rate_func=_first_half)],
                name="U_B = u_B V")
        self.wait(T_READ)
        fin = Eq("u_B", "=", r"\frac{B^2}{2\mu_0}", size=64).at(EQX, -1.25)
        self.play(*self.H("A energia mora no campo"), FadeIn(fin.mob, shift=0.1 * UP), run_time=T_EQ)
        fb = boxed(fin.mob, color=MAGENTA, buff=0.22)
        un = MathTex(r"\left[\frac{B^2}{2\mu_0}\right]=\frac{\mathrm T^2}{\mathrm{T\,m/A}}=\frac{\mathrm J}{\mathrm m^3}",
                     font_size=30, color=DIM).move_to(P3(EQX, -2.7))
        self.play(Create(fb), FadeIn(un), run_time=T_EQ)
        self.E = VGroup(g1.mob, g2.mob, vv.mob, s5.mob, un)
        self.fin = VGroup(fin.mob, fb)
        self.finq = fin
        self.wait(T_HOLD)

    # ═══ C15 — generalização ════════════════════════════════════════════════════════════════════════════════
    def cells(self):
        """|B|² de um solenoide finito (cilindro uniformemente magnetizado: cargas ±σ nas tampas), em células."""
        xs = np.arange(XS0 - 1.6, XS1 + 1.61, 0.3)
        ys = np.arange(YT - 1.5, YT + 1.51, 0.3)
        rr, pp = np.meshgrid(np.linspace(0.04, A_R, 9), np.linspace(0, 2 * PI, 28, endpoint=False))
        dA = (A_R / 9) * (2 * PI / 28) * rr.ravel()
        qy, qz = (rr * np.cos(pp)).ravel(), (rr * np.sin(pp)).ravel()

        def Hfield(x, y):
            h = np.zeros(2)
            for xe, sg in ((XS1, 1.0), (XS0, -1.0)):
                d = np.stack([x - xe + 0 * qy, (y - YT) - qy, -qz], 1)
                r3 = np.linalg.norm(d, axis=1) ** 3 + 1e-9
                h += sg * np.sum((d[:, :2].T * dA / r3), axis=1) / (4 * PI)
            return h
        b0 = Hfield(XC, YT) + np.array([1.0, 0.0])
        g = VGroup()
        s = LAYOUTS["cells"][0]
        for x in xs:
            for y in ys:
                h = Hfield(x, y)
                inside = XS0 < x < XS1 and abs(y - YT) < A_R
                b = h + (np.array([1.0, 0.0]) if inside else 0)
                v = float(np.dot(b, b) / np.dot(b0, b0))
                if v < 0.004:
                    continue
                X, Y, _ = self.ap.proj(x, y, 0.0, ang=ANG0)
                g.add(Square(0.27 * s).move_to(self.Wl("cells", X, Y)).set_fill(MAGENTA, min(0.75, 0.75 * v ** 0.75))
                      .set_stroke(width=0))
        return g.set_z_index(0)

    def c15(self):
        ap, L = self.ap, self.L
        self.sec(15, "generalizacao")
        self.play(*self.H("Vale para qualquer campo"), *self.clrE(), *self.lay("cells"),
                  ap.oVol.animate.set_value(0), ap.oAe.animate.set_value(0), ap.oSweep.animate.set_value(0),
                  *self.hide(L["A"], L["ell"]), self.fin.animate.move_to(P3(EQX, 1.9)), run_time=T_MOVE)
        cg = self.cells()
        self.play(LaggedStart(*[FadeIn(c) for c in cg], lag_ratio=0.004), ap.oB.animate.set_value(0.4), run_time=2.5)
        cn = desc("campo real: não uniforme, vaza pelas pontas", 22).move_to(self.Wl("cells", XC, YT - 1.9))
        self.play(FadeIn(cn), run_time=T_FADE)
        self.wait(T_READ)
        pk = self.Wl("cells", XS1 + 0.6, YT + 0.6)
        dt_ = Square(0.27 * LAYOUTS["cells"][0]).move_to(pk).set_stroke(WHITE, 3).set_fill(opacity=0).set_z_index(8)
        dl = MathTex(r"d\tau", font_size=30).next_to(dt_, UR, buff=0.06).set_z_index(8)
        self.play(Create(dt_), FadeIn(dl), run_time=T_EQ)
        d1 = Eq("dU_B", "=", r"\frac{B^2}{2\mu_0}", r"d\tau", size=M_L).at(EQX, 0.1)
        self.play(TransformFromCopy(VGroup(*self.finq.g(2)), VGroup(*d1.g(2))), FadeIn(VGroup(*d1.g(0, 1, 3))),
                  run_time=T_EQ)
        self.remove(*d1.g(0, 1, 2, 3))
        self.add(d1.mob)
        self.wait(T_READ)
        self.play(*self.H("Somando a energia de cada pedaço"), LaggedStart(*[c.animate.set_stroke(WHITE, 1.2, 0.6)
                                                                             for c in cg], lag_ratio=0.003), run_time=2.4)
        d2 = Eq("U_B", "=", r"\frac{1}{2\mu_0}", r"\int", "B^2", r"d\tau", size=60)
        fn_, fbb, fd_ = d1.frac(2)
        gn, gb, gd = d2.frac(2)
        self.gm(d1, d2, MG(d1.p(0)[1:], d2.p(0)), MP(d1, [1], d2, [1]), MG(fn_, d2.p(4)), MG([fbb], [gb]), MG(fd_, gd),
                MP(d1, [3], d2, [5]), pos=P3(EQX, -1.55), name="somar: integral")
        b2 = boxed(d2.mob, color=MAGENTA, buff=0.22)
        self.play(Create(b2), cg.animate.set_stroke(width=0), run_time=T_EQ)
        self.E = VGroup(self.fin, d2.mob, b2, cn, dt_, dl, cg)
        self.wait(T_HOLD)

    # ═══ C16 — comutação para descarga ══════════════════════════════════════════════════════════════════════
    def c16(self):
        ap, L = self.ap, self.L
        self.sec(16, "comutacao_descarga")
        self.play(*self.H("Agora: tirar a bateria sem abrir o circuito"), *self.clrE(), *self.lay("left"),
                  ap.oCirc.animate.set_value(1), ap.oB.animate.set_value(1),
                  *self.show(L["L"], L["B"], L["I"], L["E0"], L["R"]), run_time=T_MOVE)
        i0 = Eq("I(0)", "=", "I_0", size=M_L).at(EQX, 2.05)
        u0 = Eq("U_{B,0}", "=", r"\tfrac12", "L", "I_0^2", size=M_L).at(EQX, 0.95)
        ub = boxed(u0.mob, color=MAGENTA)
        self.play(FadeIn(i0.mob), run_time=T_EQ)
        self.play(FadeIn(u0.mob), Create(ub), run_time=T_EQ)
        self.wait(T_READ)
        n1 = desc("abrir a chave exigiria I → 0 de repente", 22).move_to(P3(EQX, -0.3))
        n2 = desc("então criamos um caminho só com o resistor", 22, WHITE).move_to(P3(EQX, -0.8))
        self.play(FadeIn(n1), run_time=T_FADE)
        self.wait(T_READ)
        self.play(FadeIn(n2), ap.oByp.animate.set_value(1), run_time=T_EQ)
        self.ring(self.Wl("left", XB, 0), 0.7, 2.6, WHITE)
        self.wait(T_BEAT)
        # comutação a → b: o percurso comum não muda; a corrente é contínua (td = 0 ⇔ I = I₀)
        self.play(*self.H("A chave passa de a para b"), ap.sw.animate.set_value(SW_B), run_time=1.4)
        ap.mode = "discharge"
        ap.td.set_value(0)
        self.play(ap.oBat.animate.set_value(0.18), *self.hide(L["E0"]), run_time=T_EQ)
        n3 = desc("o caminho continua fechado pelo resistor", 22, GREEN).move_to(P3(EQX, -1.45))
        self.play(FadeIn(n3), run_time=T_FADE)
        self.E = VGroup(i0.mob, n1, n2, n3)
        self.U0 = VGroup(u0.mob, ub)
        self.wait(T_READ)

    # ═══ C17 — o indutor sustenta a corrente ════════════════════════════════════════════════════════════════
    def c17(self):
        ap, L = self.ap, self.L
        self.sec(17, "indutor_sustenta")
        self.play(*self.H("O indutor sustenta a corrente"), *self.clrE(),
                  self.U0.animate.scale(0.75).move_to(P3(EQX + 1.9, 2.35)), run_time=T_MOVE)
        e1 = Eq("L", r"\frac{dI}{dt}", "+", "R", "I", "=", "0", size=M_L).at(EQX - 1.0, 1.35)
        nb = desc("a mesma malha, sem a bateria", 22).next_to(e1.mob, DOWN, buff=0.2)
        self.play(FadeIn(e1.mob), FadeIn(nb), run_time=T_EQ)
        self.wait(T_READ)
        e2 = Eq("I(t)", "=", "I_0", r"e^{-t/\tau}", size=M_L)
        self.gm(e1, e2, MP(e1, [5], e2, [1]), name="solucao da descarga")
        b2 = boxed(e2.mob)
        self.play(Create(b2), FadeOut(nb), run_time=T_FADE)
        g = self.g = Graf(self, center=(EQX, -1.55), h=2.0, one="I_0", ylab="I", ycol=GREEN)
        self.play(*g.show(), ap.oEL.animate.set_value(1), *self.show(L["EL"]), run_time=T_EQ)
        g.curve(lambda x: math.exp(-x), ap.td, GREEN, 5)
        g.marker(lambda x: math.exp(-x), ap.td, GREEN)
        k2 = row(tex(r"\frac{dI}{dt}<0", 30), tex(r"\Rightarrow", 30), tex(r"\mathcal E_L", 30),
                 desc("a favor da corrente", 22, WHITE)).move_to(P3(EQX, 0.6))
        self.play(FadeIn(k2), ap.td.animate.set_value(0.4), run_time=2.0, rate_func=linear)
        nn = desc("como vimos antes: a fem agora sustenta a corrente", 22, CYAN).move_to(P3(EQX, 0.1))
        self.play(FadeIn(nn), ap.td.animate.set_value(0.7), run_time=T_EQ, rate_func=linear)
        self.run(ap.td, 5.0, T_RUN)
        self.E = VGroup(self.U0, e2.mob, b2, k2, nn)
        self.wait(T_HOLD)

    # ═══ C18 — campo vira calor ═════════════════════════════════════════════════════════════════════════════
    def c18(self):
        ap = self.ap
        self.sec(18, "campo_vira_calor")
        g = self.g
        self.play(*self.H("O campo vira calor"), *self.clrE(), *g.hide(), run_time=T_FADE)
        g.drop()
        gU = Graf(self, center=(EQX, 0.7), h=1.2, one="U_{B,0}", tlab=False)
        gP = Graf(self, center=(EQX, -1.7), h=1.2, one=r"RI_0^2")
        eU = Eq("U_B(t)", "=", r"\tfrac12 L I_0^2", r"e^{-2t/\tau}", size=M_M).at(EQX, 1.7)
        eP = Eq("P_R(t)", "=", r"R I_0^2", r"e^{-2t/\tau}", size=M_M).at(EQX, -0.55)
        self.play(*gU.show(), *gP.show(), FadeIn(eU.mob), FadeIn(eP.mob), run_time=T_EQ)
        gU.curve(lambda x: math.exp(-2 * x), ap.td, MAGENTA, 5)
        gU.marker(lambda x: math.exp(-2 * x), ap.td, MAGENTA)
        gP.curve(lambda x: math.exp(-2 * x), ap.td, HEAT, 5)
        gP.marker(lambda x: math.exp(-2 * x), ap.td, HEAT)
        self.rewind(ap.td, gP)
        self.run(ap.td, 0.4, 2.0)
        n1 = desc("potência: o ritmo em que o resistor recebe energia", 22, HEAT).move_to(P3(EQX, -3.2))
        self.play(FadeIn(n1), ap.td.animate.set_value(0.6), run_time=T_EQ, rate_func=linear)
        self.run(ap.td, 5.0, T_RUN)
        ck = Eq("P_R", "=", r"-\frac{dU_B}{dt}", size=M_M).at(1.05, 2.2)
        self.play(FadeIn(ck.mob), run_time=T_EQ)
        self.wait(T_READ)
        # a área sob P_R acumula o calor: Q_R
        self.play(*self.H("A área sob a potência é o calor acumulado"), FadeOut(n1), run_time=T_FADE)
        gP.area(lambda x: math.exp(-2 * x), ap.td, HEAT, 0.45)
        self.rewind(ap.td, gP)
        qq = Eq("Q_R(t)", "=", r"\int_0^t", "P_R", r"\,dt'", size=M_M).at(EQX, -3.25)
        self.play(FadeIn(qq.mob), ap.td.animate.set_value(0.3), run_time=T_EQ, rate_func=linear)
        self.run(ap.td, 5.0, T_RUN)
        self.gU, self.gP, self.E = gU, gP, VGroup(eU.mob, eP.mob, ck.mob, qq.mob)
        self.wait(T_HOLD)

    # ═══ C19 — a conservação fecha ══════════════════════════════════════════════════════════════════════════
    def c19(self):
        ap = self.ap
        self.sec(19, "conservacao_fecha")
        gU, gP = self.gU, self.gP
        self.play(*self.H("Quanto calor no total?"), *self.clrE(), *gU.hide(), *gP.hide(), run_time=T_FADE)
        gU.drop()
        gP.drop()
        y0 = 0.6
        e1 = Eq(r"E_{\rm calor}", "=", r"\int_0^\infty", "I^2", "R", r"\,dt", size=M_XL).at(EQX, y0)
        self.play(FadeIn(e1.mob), run_time=T_EQ)
        self.wait(T_READ)
        sub = Eq("I", "=", "I_0", r"e^{-t/\tau}", size=M_M).at(EQX, 2.1)
        self.play(FadeIn(sub.mob), run_time=T_EQ)
        e2 = Eq(r"E_{\rm calor}", "=", r"\int_0^\infty", "R", "I_0^2", r"e^{-2t/\tau}", r"\,dt", size=M_XL)
        i2 = e1.p(3)
        j2 = e2.p(4)                                      # I 0 2
        self.gm(e1, e2, MP(e1, [0, 1, 2, 5], e2, [0, 1, 2, 6]), MP(e1, [4], e2, [3], path_arc=PI / 2),
                MG([i2[0]], [j2[0]]), MG([i2[1]], [j2[2]]), CG(sub.g(2)[1:], [j2[1]]), CG(sub.g(3), e2.p(5)),
                name="I^2 = I0^2 e^-2t/tau")
        self.wait(T_READ)
        e3 = Eq(r"E_{\rm calor}", "=", "R", "I_0^2", r"\frac{\tau}{2}", size=M_XL)
        xe = e2.p(5)                                      # e − 2 t / τ
        tn, tb, td_ = e3.frac(4)
        self.gm(e2, e3, MP(e2, [0, 1, 3, 4], e3, [0, 1, 2, 3]), MG([xe[5]], tn), MG([xe[2]], td_), name="integral")
        rd = desc("a integral de 0 a ∞ vale τ/2", 22).move_to(P3(EQX, -0.6))
        self.play(FadeIn(rd), run_time=T_FADE)
        self.wait(T_READ)
        tl = Eq(r"\tau", "=", r"\frac{L}{R}", size=M_M).at(EQX, 2.1)
        self.play(soft_swap(sub.mob, tl.mob), FadeOut(rd), run_time=1.4)
        e4 = Eq(r"E_{\rm calor}", "=", "R", "I_0^2", r"\frac{L}{2R}", size=M_XL)
        ln, lb, ld = e4.frac(4)
        tln, tlb, tld = tl.frac(2)
        self.gm(e3, e4, MP(e3, [0, 1, 2, 3], e4, [0, 1, 2, 3]), MG([tb], [lb]), MG(td_, [ld[0]]),
                CG([tl.mob[0][k] for k in tln], [ln[0]]), CG([tl.mob[0][k] for k in tld], [ld[1]]), name="tau = L/R")
        self.wait(T_BEAT)
        s1 = self.strike(*e4.g(2))
        s2 = self.strike(e4.mob[0][ld[1]])
        self.play(*self.H("O R se cancela"), Create(s1), Create(s2), run_time=T_EQ)
        self.wait(T_READ)
        self.play(FadeOut(s1), FadeOut(s2), *[gl.animate.set_opacity(0) for gl in (*e4.g(2), e4.mob[0][ld[1]])],
                  run_time=0.8)
        e5 = Eq(r"E_{\rm calor}", "=", r"\frac{1}{2}", "L", "I_0^2", size=M_XL)
        hn, hb, hd = e5.frac(2)
        self.gm(e4, e5, MP(e4, [0, 1], e5, [0, 1]), MG([lb], [hb]), MG([ld[0]], hd), MG(ln, e5.p(3)),
                MP(e4, [3], e5, [4]), name="cancelar R")
        e6 = Eq(r"E_{\rm calor}", "=", r"\frac{1}{2}", "L", "I_0^2", "=", "U_{B,0}", size=M_XL)
        self.gm(e5, e6, MP(e5, [0, 1, 2, 3, 4], e6, [0, 1, 2, 3, 4]), name="= U_B0")
        b6 = boxed(e6.mob, buff=0.22)
        self.play(*self.H("Todo o campo vira calor"), Create(b6), run_time=T_EQ)
        cR = desc("R some do resultado: a resistência só decide o ritmo", 22).move_to(P3(EQX, -0.6))
        self.play(FadeIn(cR), run_time=T_FADE)
        self.wait(T_HOLD)
        # U_B(t) e Q_R(t): uma cai, a outra sobe, a soma fica
        self.play(*self.H("A conservação fecha"), FadeOut(tl.mob), FadeOut(cR),
                  VGroup(e6.mob, b6).animate.scale(0.72).move_to(P3(EQX, 2.15)), run_time=T_MOVE)
        q1 = Eq("Q_R(t)", "=", "U_{B,0}", r"\left(1-e^{-2t/\tau}\right)", size=M_M).at(EQX, 1.2)
        q2 = Eq("U_B(t)", "+", "Q_R(t)", "=", "U_{B,0}", size=M_L).at(EQX, 0.35)
        g = self.g = Graf(self, center=(EQX, -1.75), h=2.0, one="U_{B,0}")
        self.play(FadeIn(q1.mob), *g.show(), run_time=T_EQ)
        g.curve(lambda x: math.exp(-2 * x), ap.td, MAGENTA, 5)
        g.curve(lambda x: 1 - math.exp(-2 * x), ap.td, HEAT, 5)
        g.curve(lambda x: 1.0, ap.td, WHITE, 3)
        g.marker(lambda x: math.exp(-2 * x), ap.td, MAGENTA)
        g.marker(lambda x: 1 - math.exp(-2 * x), ap.td, HEAT)
        self.rewind(ap.td, g)
        self.play(FadeIn(q2.mob), ap.td.animate.set_value(0.3), run_time=T_EQ, rate_func=linear)
        self.run(ap.td, 5.0, T_RUN * 1.2)
        b2 = boxed(q2.mob)
        self.play(Create(b2), run_time=T_EQ)
        self.E = VGroup(e6.mob, b6, q1.mob, q2.mob, b2)
        self.wait(T_HOLD)

    # ═══ C20 — síntese e Maxwell ════════════════════════════════════════════════════════════════════════════
    def c20(self):
        ap, L = self.ap, self.L
        self.sec(20, "sintese_maxwell")
        g = self.g
        self.play(*self.H("Síntese"), *self.clrE(), *g.hide(), run_time=T_MOVE)
        g.drop()
        # cada payoff volta junto do seu fenômeno, no mesmo aparato
        self.play(ap.oDots.animate.set_value(0), run_time=0.4)
        ap.mode = "charge"
        ap.tc.set_value(0)
        self.play(ap.sw.animate.set_value(SW_A), ap.oBat.animate.set_value(1), ap.oByp.animate.set_value(0),
                  *self.show(L["E0"]), run_time=T_SW)
        self.play(ap.oDots.animate.set_value(1), run_time=0.4)
        p1 = Eq(r"\mathcal E_L", "=", "-L", r"\frac{dI}{dt}", size=M_L).at(EQX, 2.0)
        self.play(FadeIn(p1.mob), ap.tc.animate.set_value(0.6), run_time=2.0, rate_func=linear)
        self.ring(self.Wl("left", XC, YT + A_R + 0.5), 3.4, 0.8, CYAN)
        p2 = Eq("U_B", "=", r"\tfrac12", "L", "I^2", size=M_L).at(EQX, 0.95)
        self.play(FadeIn(p2.mob), ap.tc.animate.set_value(2.0), run_time=2.5, rate_func=linear)
        self.play(ap.oB.animate.set_value(1.35), run_time=0.8)
        p3 = Eq("u_B", "=", r"\frac{B^2}{2\mu_0}", size=M_L).at(EQX, -0.15)
        self.play(FadeIn(p3.mob), ap.oSweep.animate.set_value(1), ap.tc.animate.set_value(4.0), run_time=2.5,
                  rate_func=linear)
        self.play(ap.oSweep.animate.set_value(0), ap.oB.animate.set_value(1), run_time=0.8)
        self.play(ap.oByp.animate.set_value(1), run_time=0.5)
        self.play(ap.sw.animate.set_value(SW_B), run_time=T_SW)
        ap.mode = "discharge"
        ap.td.set_value(0)
        p4 = Eq(r"E_{\rm calor}", "=", "U_{B,0}", size=M_L).at(EQX, -1.25)
        self.play(FadeIn(p4.mob), ap.oBat.animate.set_value(0.18), ap.td.animate.set_value(1.5), run_time=3.0,
                  rate_func=linear)
        self.run(ap.td, 5.0, 4.0)
        cols = (CYAN, MAGENTA, MAGENTA, HEAT)
        boxes = [boxed(p.mob, c) for p, c in zip((p1, p2, p3, p4), cols)]
        self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.3), run_time=2.0)
        self.wait(T_READ)
        # condensar num mapa pequeno
        mp = VGroup(*[VGroup(p.mob, b) for p, b in zip((p1, p2, p3, p4), boxes)])
        cap = VGroup(desc("o indutor reage à mudança", 22, CYAN), desc("a energia fica no campo", 22, MAGENTA),
                     desc("e volta inteira como calor", 22, HEAT))
        self.play(mp.animate.scale(0.62).arrange_in_grid(2, 2, buff=(0.4, 0.3)).move_to(P3(EQX, 1.3)), run_time=T_MOVE)
        cap.arrange(DOWN, buff=0.14).next_to(mp, DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(c) for c in cap], lag_ratio=0.5), run_time=2.0)
        self.wait(T_HOLD)
        # o mesmo circuito, com um capacitor no lugar do solenoide
        self.play(*self.H("E se, no lugar do solenoide, houver um capacitor?"), FadeOut(mp), FadeOut(cap),
                  ap.oDots.animate.set_value(0), run_time=T_MOVE)
        self.play(ap.oCap.animate.set_value(1), ap.oByp.animate.set_value(0), ap.oBat.animate.set_value(1),
                  ap.oEL.animate.set_value(0), ap.sw.animate.set_value(SW_OPEN), *self.show(L["E0"]),
                  *self.hide(L["L"], L["B"], L["EL"]), *self.show(L["C"]), run_time=T_MOVE)
        ap.mode = "cap"
        ap.tc.set_value(0)
        self.play(ap.sw.animate.set_value(SW_A), run_time=T_SW)
        self.play(ap.oDots.animate.set_value(1), ap.tc.animate.set_value(0.5), run_time=2.8, rate_func=linear)
        ap.auto_tc = 0.04                                    # a carga continua devagar até o fim (tempo não congela)
        n1 = desc("a corrente chega às placas…", 24, GREEN).move_to(P3(EQX, 2.1))
        n2 = desc("…mas não atravessa o espaço entre elas", 24, WHITE).move_to(P3(EQX, 1.6))
        self.play(FadeIn(n1), run_time=T_FADE)
        self.wait(T_BEAT)
        self.play(FadeIn(n2), *self.show(L["gap"]), run_time=T_FADE)
        self.wait(T_READ)
        self.play(*self.H("A lei de Ampère em volta do fio"), FadeOut(n1), FadeOut(n2), *self.hide(L["gap"]),
                  ap.oAmp.animate.set_value(1), run_time=T_EQ)
        a1 = Eq(r"\oint", r"\mathbf B\cdot d\boldsymbol\ell", "=", r"\mu_0", r"I_{\rm enc}", size=M_L).at(EQX, 2.0)
        self.play(FadeIn(a1.mob), run_time=T_EQ)
        self.wait(T_READ)
        s1 = row(tex("S_1:", M_M, GEO), tex(r"I_{\rm enc}=I", M_M)).move_to(P3(EQX - 1.85, 0.9))
        s2 = row(tex("S_2:", M_M, VIOLET), tex(r"I_{\rm enc}=0", M_M)).move_to(P3(EQX + 1.85, 0.9))
        self.play(ap.oS1.animate.set_value(1), *self.show(L["S1"]), FadeIn(s1), run_time=T_EQ)
        d1 = desc("o fio fura o disco", 20).next_to(s1, DOWN, buff=0.15)
        self.play(FadeIn(d1), run_time=T_FADE)
        self.wait(T_BEAT)
        self.play(ap.oS2.animate.set_value(1), *self.show(L["S2"]), FadeIn(s2), run_time=T_EQ)
        d2 = desc("passa entre as placas", 20).next_to(s2, DOWN, buff=0.15)
        self.play(FadeIn(d2), run_time=T_FADE)
        self.wait(T_BEAT)
        qm = MathTex("?", font_size=90, color=CYAN).move_to(P3(EQX, 0.9))
        self.play(FadeIn(qm, scale=0.6), run_time=T_EQ)
        self.wait(T_READ)
        q = VGroup(text("COMO O CAMPO MAGNÉTICO SABE", 32, WHITE), text("QUE O CIRCUITO CONTINUA?", 32, WHITE)) \
            .arrange(DOWN, buff=0.16)
        fitw(q, 6.6).move_to(P3(EQX, -1.05))
        self.play(*self.H("Uma pergunta para o próximo vídeo"), FadeIn(q, shift=0.1 * UP), run_time=T_EQ)
        self.wait(T_HOLD)
        nx = text("PRÓXIMO: MAXWELL", 38, CYAN).move_to(P3(EQX, -2.25))
        self.play(FadeIn(nx, shift=0.1 * UP), run_time=T_EQ)
        cta = tag("inscreva-se para acompanhar a série", 18, DIM, 0.75).move_to(P3(0, -3.55))
        self.play(FadeIn(cta), run_time=T_FADE)
        self.wait(T_HOLD * 1.3)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.body], ap.oAll.animate.set_value(0),
                  run_time=T_MOVE)
        ap.auto_tc = 0.0
        self.wait(0.5)
