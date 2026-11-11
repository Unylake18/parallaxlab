"""yt_0026 — kit da unidade: paleta da Matemática (handoff v2 §2.1), texto, caneta, setas de campo, base de cena (relógio por quadro, âncoras,
canto) e fundo 3D por estado (Three.js).

O relógio, as âncoras (an/gat/ate) e o Fundo3D vêm do kit do yt_0022 (copiados, sem a medição de sincronia da voz, que não existe no preview).
O fundo é o milimetrado parado da série de Cálculo (assets/calculo/papel.py): imagem da câmera, nada se mexe atrás.
Auditorias desta rodada (logs no render): [flash] (glifo de caneta visível antes da vez), [algebra] (glifos e fração colorida por MathTex),
[campo] (fator de escala de cada campo e maior seta ÷ espaçamento), [ancora] (início de cada âncora no lote).
"""
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from manim import *  # noqa: F401,F403

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[1]
sys.path.insert(0, str(ROOT))
from template.config_horizontal import TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import DISPLAY_FONT, official_text, screen_text  # noqa: E402
from assets.calculo.papel import _arq, eixos_no_papel, janela, usar_papel  # noqa: E402,F401

config.media_dir = os.environ.get("MEDIA_DIR", str(AQUI / "media"))
Circle.set_default(color=WHITE)

# ── paleta da Matemática (handoff v2 §2.1): a cor é o PAPEL do símbolo na fórmula ─────────────────────────
WHITE_ = TEXT_COLOR      # neutros: f, φ, ∂, ∫, ⊂, →, ℝ, versores, t, números
GEO = "#B8C4DA"          # domínio, regiões, conjunto de entrada (preenchimento ~18%)
E1 = "#FFC24D"           # 1ª entrada (θ, u, x de entrada) e a família em que ela fica fixa
E2 = "#EA63FF"           # 2ª entrada (ρ, v, y de entrada) e a sua família
SAI = "#7FB2FF"          # saída: imagem, ponto de saída, x y z de saída, gráfico, colunas (preenchimento ~20%)
CAMPO = "#2EE6A0"        # campo vetorial: setas, F⃗ e componentes
POS = "#D2823A"          # vetor posição e curva γ(t): X, γ(t), r⃗
VEL = "#9C8CFF"          # velocidade γ′(t) (só ela)
NORM = "#267BFF"         # normal n̂
# sistema visual v3 (handoff v4 §2.1): nenhuma curva, região ou ponto do desenho é branco
ESC = "#050B18"          # contorno escuro por baixo de todo traço de desenho
SAI_F = "#A9CCFF"        # azul-claro forte: borda de imagem e dobra
FORTE = SAI_F
DEST = "#FF7A8A"         # coral: objeto de teste (bandeira, barquinho), lado que esmaga ou cola (B2-6), "×" de ninguém chega
CH_DOM, CH_IMG = "#1A2C52", "#1C3A70"            # chapas opacas: domínio (85%, borda GEO 2,5) e imagem (80%, borda SAI_F 4)
CAMPO_FRACO, CAMPO_FORTE = "#2EE6A0", "#8CFFD2"  # seta de campo 2D: cor pela intensidade ‖F‖/‖F‖máx da cena
W_EIXO, W_FAM, W_FAM_B, W_CURVA, W_IMG, W_CAMPO, W_VEL, W_GUIA = 2.0, 3.0, 4.0, 4.5, 5.0, 4.5, 7.0, 2.2
DIM = "#8FA3C4"
W_GAMA = 5.5
BG = "#091226"

T_HL, T_MAIN, T_LAB, T_SMALL = 40, 30, 26, 20
M_XL, M_L, M_M, M_S = 54, 48, 40, 32

FPS = int(os.environ.get("FPS_RENDER", "15"))
FRAC = 0.02 / FPS
STILL = float(os.environ["STILL"]) if os.environ.get("STILL") else None
PEDIDOS3D = os.environ.get("PEDIDOS3D") == "1"
DIR3D = AQUI / "threejs"
ANC = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]
LEAD = 0.09       # a imagem começa ~0,1 s antes da palavra


def P3(x, y, z=0.0):
    return np.array([x, y, z], dtype=float)


def suave(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


# ── texto ────────────────────────────────────────────────────────────────────────────────────────────
def txt(s, size=T_MAIN, color=WHITE_, op=1.0, bold=False):
    """Texto de tela: Space Grotesk em CAIXA ALTA (símbolo matemático nunca aqui)."""
    s = s.upper()
    if bold:
        m = official_text(s, DISPLAY_FONT, BOLD, size, oversample=2, color=color)
    else:
        m = screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2)
    return m.set_opacity(op)


# ── matemática colorida ──────────────────────────────────────────────────────────────────────────────
def F(*pares, size=M_L, caneta=True):
    """MathTex em partes coloridas: cada par é (tex, cor) ou tex (branco). Traço na mesma cor do preenchimento.
    `caneta=True` marca a fórmula para o portão FLASH (não pode aparecer antes de ser escrita pela caneta)."""
    partes = [p[0] if isinstance(p, tuple) else p for p in pares]
    cores = [p[1] if isinstance(p, tuple) else WHITE_ for p in pares]
    m = MathTex(*partes, font_size=size)
    for sub, c in zip(m.submobjects, cores):
        sub.set_fill(c, 1).set_stroke(c, 0)
    m._tex = "".join(partes)
    m._caneta, m._esc, m._em_caneta = caneta, not caneta, False
    return m


def Fs(tex, cores=None, size=M_L, caneta=True):
    """MathTex de string única (para TransformByGlyphMap), colorida por índice de glifo: cores = {cor: [índices]}."""
    m = MathTex(tex, font_size=size)
    m[0].set_fill(WHITE_, 1).set_stroke(WHITE_, 0)
    for c, idx in (cores or {}).items():
        for i in idx:
            m[0][i].set_fill(c, 1).set_stroke(c, 0)
    m._tex = tex
    m._caneta, m._esc, m._em_caneta = caneta, not caneta, False
    return m


def glifos(m):
    return [g for g in m.family_members_with_points() if isinstance(g, VMobject)]


def frac_cor(m):
    gs = glifos(m)
    if not gs:
        return 0.0
    branco = ManimColor(WHITE_).to_hex().upper()
    return sum(1 for g in gs if ManimColor(g.get_fill_color()).to_hex().upper() != branco) / len(gs)


CANETA_W = 1.5         # contorno fino (handoff: ~0,7; 1,5 para ainda aparecer no preview 540p: ~0,9 px)
PASSO, DG = 0.30, 0.6  # passo entre glifos e duração de cada glifo


class _Caneta(Animation):
    """Modo caneta: contorno fino glifo a glifo (esquerda → direita), depois o preenchimento na cor do papel. Nada aparece antes da vez."""

    def __init__(self, m, ordem=None, atraso=0.0, ritmo=1.0, **kw):
        self.atraso = atraso
        self.passo, self.dg = PASSO * ritmo, DG * ritmo
        gs = glifos(m)
        gs = sorted(gs, key=lambda g: (round(g.get_left()[0], 2), -g.get_center()[1]))
        if ordem:
            gs = ordem(gs)
        self.gl = gs
        self.orig = [g.copy() for g in gs]
        self.n = len(gs)
        self.tot = atraso + self.passo * max(0, self.n - 1) + self.dg
        self.ponta = None
        m._em_caneta = True
        super().__init__(m, rate_func=linear, introducer=True, run_time=self.tot, **kw)

    def interpolate_mobject(self, alpha):
        t = alpha * self.tot - self.atraso
        topo = None
        for i, (g, o) in enumerate(zip(self.gl, self.orig)):
            u = (t - self.passo * i) / self.dg
            if u <= 0:
                g.set_fill(opacity=0).set_stroke(width=0, opacity=0)
                continue
            if u >= 1:
                g.become(o)
                continue
            p1, p2 = min(1.0, u / 0.6), max(0.0, (u - 0.45) / 0.55)
            g.pointwise_become_partial(o, 0, p1)
            c = o.get_fill_color()
            g.set_stroke(c, CANETA_W, 1).set_fill(c, p2)
            if p1 < 1:
                topo = g
        if self.ponta is not None:
            if topo is not None and len(topo.points):
                self.ponta.move_to(topo.points[-1]).set_opacity(1)
            else:
                self.ponta.set_opacity(0)

    def finish(self):
        super().finish()
        for g, o in zip(self.gl, self.orig):
            g.become(o)
        self.mobject._em_caneta, self.mobject._esc = False, True


def caneta(m, ordem=None, atraso=0.0, ritmo=1.0):
    """Animação da caneta. A ponta branca (~3 px) é posta e tirada pelo Base.play. `atraso`: segundos de espera antes do primeiro glifo."""
    return _Caneta(m, ordem=ordem, atraso=atraso, ritmo=ritmo)


def ja_escrita(m):
    """Fórmula que entra por transformação (TransformByGlyphMap / TransformFromCopy): libera do portão FLASH."""
    m._esc = True
    return m


# ── estilo v3: contorno escuro, chapas, pontos, placas (handoff v4 §2.2) ──────────────────────────────
# O contorno é o traço de FUNDO do próprio VMobject (ESC, largura = traço + 4, opacidade 0,88 × a do traço): nasce, some e se transforma junto
# com o traço em qualquer animação, e não muda a estrutura dos grupos. set_stroke/set_fill mantêm o contorno em dia (largura e opacidade).
_set_stroke0, _set_fill0 = VMobject.set_stroke, VMobject.set_fill
OP_CTN = 0.88


def _set_stroke(self, color=None, width=None, opacity=None, background=False, family=True):
    _set_stroke0(self, color, width, opacity, background, family)
    if not background and (width is not None or opacity is not None):
        for m in (self.get_family() if family else [self]):
            e = getattr(m, "_ctn", None)
            if e:
                _set_stroke0(m, None, m.get_stroke_width() + e if width is not None else None, OP_CTN * opacity if opacity is not None else None, True, False)
    return self


def _set_fill(self, color=None, opacity=None, family=True):
    _set_fill0(self, color, opacity, family)
    if opacity is not None:
        for m in (self.get_family() if family else [self]):
            if getattr(m, "_ctn", None) and m.get_stroke_width() == 0:          # só preenchimento (ponto, região): o contorno segue o preenchimento
                _set_stroke0(m, None, None, OP_CTN * opacity, True, False)
    return self


VMobject.set_stroke, VMobject.set_fill = _set_stroke, _set_fill


def desenhos(m):
    """VMobjects de DESENHO da família (com pontos): fora texto, MathTex, eixos e o que estiver marcado `_sem_contorno`."""
    if isinstance(m, (SVGMobject, VMobjectFromSVGPath, Axes)) or getattr(m, "_sem_contorno", False):          # glifo solto também é texto
        return
    if isinstance(m, VMobject) and len(m.points):
        yield m
    for sub_ in m.submobjects:
        yield from desenhos(sub_)


def contorno(m, extra=4.0):
    """Contorno escuro por baixo de cada traço (pontas de seta e tracejados inclusive). Devolve o próprio `m`."""
    for d in desenhos(m):
        if not getattr(d, "_ctn", None):
            d._ctn = extra
            base = d.get_stroke_opacity() if d.get_stroke_width() > 0 else d.get_fill_opacity()
            _set_stroke0(d, ESC, d.get_stroke_width() + extra, OP_CTN * base, True, False)
    return m


def chapa(m, tipo="dom"):
    """Região = chapa opaca (a grade do fundo não atravessa): domínio ou imagem."""
    if tipo == "dom":
        m.set_fill(CH_DOM, 0.55).set_stroke(GEO, 2.5, 1)
    else:
        m.set_fill(CH_IMG, 0.55).set_stroke(SAI_F, 4, 1)
    return contorno(m)


def ponto(p, cor, r=0.07, z=6):
    """Ponto preenchido na cor do papel, com anel escuro 3,5 para fora."""
    d = Dot(p, radius=r, color=cor).set_z_index(z)
    return contorno(d, extra=7.0)


def base_de(m):
    """Linha de base do texto: mediana do fundo dos glifos (acento e cedilha não contam)."""
    b = [g.get_bottom()[1] for g in m.submobjects if len(g.points)]
    return float(np.median(b)) if b else m.get_bottom()[1]


def linha_texto(*partes, buff=0.25):
    """Textos lado a lado alinhados pela LINHA DE BASE (arrange(RIGHT) alinha pelo centro da caixa e o acento/cedilha desalinha)."""
    g = VGroup(*partes).arrange(RIGHT, buff=buff)
    b0 = base_de(partes[0])
    for p in partes[1:]:
        p.shift(UP * (b0 - base_de(p)))
    return g


def placa(c, cor=SAI_F, size=20):
    """Rótulo preso a desenho: placa ESC a 85%, cantos 0,06, borda 2 na cor do rótulo. `c` é o texto (Space Grotesk) ou um mobject pronto."""
    t = txt(c, size, bold=True, color=cor) if isinstance(c, str) else c
    r = RoundedRectangle(width=t.width + 0.26, height=t.height + 0.2, corner_radius=0.06).set_fill(ESC, 0.85).set_stroke(cor, 2).move_to(t)
    r._sem_contorno = True
    return VGroup(r, t).set_z_index(9)


def voo(a, b, angle=-0.75, w=2.5, tip=0.13):
    """Seta de voo (arco entrada → saída): o único desenho branco, sempre com contorno."""
    s = CurvedArrow(np.asarray(a, float), np.asarray(b, float), angle=angle, tip_length=tip).set_stroke(WHITE_, w)
    s.tip.set_fill(WHITE_, 1)
    for m in s.get_family():
        m._voo = True
    return s


def guia(a, b, cor, w=W_GUIA, op=0.9):
    """Guia tracejada (dash 0,10, razão 0,55), com o contorno também tracejado."""
    return contorno(DashedLine(np.asarray(a, float), np.asarray(b, float), dash_length=0.10, dashed_ratio=0.55).set_stroke(cor, w, op))


def tracejado(m, cor, w=W_GUIA, op=0.9, dash=0.10):
    """Curva tracejada com dash ~0,10 u e razão 0,55 (contorno tracejado junto)."""
    n = max(8, int(round(m.get_arc_length() / (dash / 0.55))))
    return contorno(DashedVMobject(m, num_dashes=n, dashed_ratio=0.55).set_stroke(cor, w, op))


def pulso(m, s=1.05, w=1.7, **kw):
    """Destaque sem branco (no lugar do Indicate): escala `s` e traço `w` vezes mais grosso, ida e volta."""
    alvo = m.copy().scale(s)
    for d in desenhos(alvo):
        if d.get_stroke_width() > 0:
            d.set_stroke(width=w * d.get_stroke_width(), family=False)
    return Transform(m, alvo, rate_func=there_and_back, **kw)


def eixos(origem, x_range, y_range, unidade=1.0, unidade_y=None):
    """Eixos presos à grade: GEO a 75%, traço 2, sem contorno (ficam atrás)."""
    return eixos_no_papel(origem, x_range, y_range, unidade, unidade_y).set_stroke(GEO, W_EIXO, 0.75)


def eixo_seta(a, b, tip=0.12):
    s = seta(a, b, GEO, W_EIXO, tip=tip, op=0.75)
    for m in s.get_family():
        m._sem_contorno = True
        m._ctn = None
        _set_stroke0(m, None, 0, 0, True, False)
    return s


# ── setas e campos ───────────────────────────────────────────────────────────────────────────────────
class SetaG(VGroup):
    """Seta = haste + ponta cheia, SEM contorno e sem efeito algum (handoff v7 §2.4). Faz as vezes do Arrow nos GrowArrow/become.
    Opacidade parcial não existe: set_opacity(o) com 0 < o < 1 mistura a cor com o fundo (seta continua opaca)."""

    def get_start(self):
        return self.haste.get_start()

    def get_end(self):
        return self.ponta.points[0]

    def scale(self, factor, scale_tips=False, **kw):      # GrowArrow chama scale(0, scale_tips=True)
        return super().scale(factor, **kw)

    def set_opacity(self, opacity, family=True):
        c = getattr(self, "_cor", None)
        for m in (self.haste, self.ponta):
            if opacity <= 0 or c is None:
                m.set_fill(opacity=0).set_stroke(opacity=0)
                continue
            cc = interpolate_color(ManimColor(BG), ManimColor(c), min(1.0, opacity)) if opacity < 1 else ManimColor(c)
            if m is self.haste:
                m.set_stroke(cc, m.get_stroke_width() or self._w, 1)
            else:
                m.set_fill(cc, 1).set_stroke(cc, 1.5, 1)
        return self


def seta(a, b, cor=CAMPO, w=W_CAMPO, tip=0.20, op=1.0):
    """Seta com o pé exatamente em `a` e a ponta em `b` (sem buff): haste + ponta cheia (largura 0,7 × comprimento), sem contorno e sem brilho."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = float(np.linalg.norm(b - a))
    if L < 1e-3:
        return VMobject()
    d = (b - a) / L
    n = np.array([-d[1], d[0], 0.0])
    tl = min(tip, 0.45 * L)
    base = b - tl * d
    haste = Line(a, base + 0.3 * tl * d).set_stroke(cor, w, 1)
    ponta = Polygon(b, base + 0.5 * tl * n, base - 0.5 * tl * n).set_fill(cor, 1).set_stroke(cor, 1.5, 1)
    for m in (haste, ponta):
        m._sem_contorno = True
    s = SetaG(haste, ponta)
    s.haste, s.ponta, s._cor, s._w = haste, ponta, cor, w
    return s.set_opacity(op) if op != 1.0 else s


def cor_campo(f):
    """Cor da seta de campo pela intensidade f = ‖F‖/‖F‖máx da cena (fraca → forte)."""
    return interpolate_color(ManimColor(CAMPO_FRACO), ManimColor(CAMPO_FORTE), min(1.0, max(0.0, f)))


def grade_pts(r=3.0, passo=1.0, disco=True, sem_origem=True):
    xs = np.arange(-r, r + 1e-6, passo)
    return [(x, y) for x in xs for y in xs if (not disco or math.hypot(x, y) <= r + 1e-6) and (not sem_origem or math.hypot(x, y) > 1e-6)]


def malha(ax, x0, x1, y0, y1, passo, w=2.2, n=40):
    """Malha-OBJETO (folha, domínio): chapa de domínio + linhas GEO finas a cada `passo`, por cima do papel.
    Linhas com muitos pontos, para poderem dobrar numa transformação."""
    ret = chapa(Polygon(*[ax.c2p(*p) for p in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]))
    ret.insert_n_curves(4 * n)
    ls = VGroup()
    for x in np.arange(x0 + passo, x1 - 1e-6, passo):
        ls.add(Line(ax.c2p(x, y0), ax.c2p(x, y1)).insert_n_curves(n).set_stroke(GEO, w, 0.7))
    for y in np.arange(y0 + passo, y1 - 1e-6, passo):
        ls.add(Line(ax.c2p(x0, y), ax.c2p(x1, y)).insert_n_curves(n).set_stroke(GEO, w, 0.7))
    for l in ls:
        l._sem_contorno = True               # linhas internas da chapa: finas, sem contorno (a chapa já é escura)
    return VGroup(ret, ls)


def bandeira(ax, s=1.0, cor=DEST, silhueta=False):
    """Bandeira assimétrica (objeto de teste, coral): mastro de (1, 0) a (1, 1,6) e triângulo apontando para a direita no topo (pé em (1, 0)).
    `silhueta`: só o contorno tracejado (com contorno escuro tracejado)."""
    p = lambda x, y: ax.c2p(1 + s * (x - 1), s * y)
    if silhueta:
        mastro = guia(p(1, 0), p(1, 1.6), cor, 2.6, 1.0)
        pano = tracejado(Polygon(p(1, 1.6), p(2.0, 1.32), p(1, 1.04)), cor, 2.6, 1.0)
        pe = Dot(p(1, 0), radius=0.05, color=cor)
    else:
        mastro = Line(p(1, 0), p(1, 1.6)).set_stroke(cor, 5)
        pano = Polygon(p(1, 1.6), p(2.0, 1.32), p(1, 1.04)).set_stroke(cor, 2).set_fill(cor, 1)
        pe = Dot(p(1, 0), radius=0.07, color=cor)
    return contorno(VGroup(mastro, pano, pe))


# ── 3D por estado (Three.js): passagem seca grava pedidos, r3d.js renderiza, a passagem final cola o PNG ───────
class Fundo3D(Group):
    """(kit do yt_0022) Fundo 3D do quadro inteiro. `estado(t)` devolve o estado da cena 3D no tempo t do lote."""

    def __init__(self, cena_m, cena3d, estado, op=1.0):
        super().__init__()
        self.cm, self.cena, self.fn = cena_m, cena3d, estado
        self.op = ValueTracker(op)
        self.w, self.h = config.pixel_width, config.pixel_height
        self.dir = DIR3D / "q3d" / f"{cena_m.lote}_{self.w}x{self.h}" / cena3d
        vazio = np.zeros((self.h, self.w, 4), dtype=np.uint8)
        self.alfa = vazio[..., 3].copy()
        self.img = ImageMobject(vazio).set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
        self.img.set_width(16).move_to(ORIGIN)
        self.add(self.img)
        self.set_z_index(-20)
        self.f = -1
        self.e = estado(0.0)
        cena_m._ped.setdefault(cena3d, {})
        self.add_updater(lambda m: m._quadro())
        self._quadro()

    def __deepcopy__(self, memo):
        g = Group(ImageMobject(self.img.pixel_array.copy()).set_width(16).move_to(ORIGIN))
        return g.set_z_index(-20)

    def _quadro(self):
        f = int(round(self.cm.clk.get_value() * FPS))
        e = self.fn(f / FPS)
        self.e = e
        if PEDIDOS3D:
            self.cm._ped[self.cena][f] = r4(e)
        elif f != self.f:
            arq = self.dir / f"f{f:05d}.png"
            if arq.exists():
                from PIL import Image
                a = np.array(Image.open(arq).convert("RGBA"))
                if a.shape[0] != self.h:
                    a = np.array(Image.open(arq).convert("RGBA").resize((self.w, self.h)))
                self.img.pixel_array = a
                self.alfa = a[..., 3].copy()
        self.f = f
        o = self.op.get_value()
        self.img.pixel_array[..., 3] = (self.alfa * max(0.0, min(1.0, o)) + 0.5).astype(np.uint8)
        return self


def r4(d):
    if isinstance(d, dict):
        return {k: r4(v) for k, v in d.items()}
    if isinstance(d, (list, tuple)):
        return [r4(v) for v in d]
    if isinstance(d, float):
        return round(d, 4)
    return d


def cam_topo(K=1.0, xc=0.0, yc=0.0, camx=0.0, camy=0.0, fov=16):
    return {"modo": "topo", "K": K, "xc": xc, "yc": yc, "camx": camx, "camy": camy, "fov": fov}


def cam_obl(az, el, alvo, K=1.0, xc=0.0, yc=0.0, fov=16):
    return {"modo": "obl", "az": az, "el": el, "alvo": list(alvo), "K": K, "xc": xc, "yc": yc, "fov": fov}


_BASES = {}


def _base_cam(cam):
    """(kit do yt_0022) a mesma câmera do b3d.js (posicionaCamera + setViewOffset)."""
    k = tuple((a, tuple(b) if isinstance(b, list) else b) for a, b in sorted(cam.items()))
    if k in _BASES:
        return _BASES[k]
    K, fov = cam.get("K", 1.0), cam.get("fov", 14)
    if cam.get("modo") == "topo":
        az, el, alvo = -90.0, 89.999, (cam.get("camx", 0.0), cam.get("camy", 0.0), 0.0)
    elif cam.get("modo") == "obl":
        az, el, alvo = cam["az"], cam["el"], cam["alvo"]
    else:
        az, el, alvo = -90.0, cam.get("el", 0.0), (cam.get("camx", 0.0), 0.0, cam.get("camz", 0.0))
    a, e, th = math.radians(az), math.radians(el), math.tan(math.radians(fov) / 2)
    D = (9 / K / 2) / th
    alvo = np.array(alvo, dtype=float)
    pos = alvo + D * np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    up = np.array([-math.sin(e) * math.cos(a), -math.sin(e) * math.sin(a), math.cos(e)])
    f = (alvo - pos) / np.linalg.norm(alvo - pos)
    r = np.cross(f, up)
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    if len(_BASES) > 4000:
        _BASES.clear()
    _BASES[k] = b = (pos, np.stack([r, u, f]), 8 / (th * 16 / 9), 4.5 / th, cam.get("xc", 0.0), cam.get("yc", 0.0))
    return b


def projeta3d(cam, p):
    """Ponto 3D → Manim pela mesma câmera do b3d.js. Perspectiva exata."""
    pos, B, sx, sy, xc, yc = _base_cam(cam)
    x, y, z = B @ (np.asarray(p, dtype=float) - pos)
    return np.array([xc + sx * x / z, yc + sy * y / z, 0.0])


# ── cena-base ──────────────────────────────────────────────────────────────────────────────────────────
TITULO = "CÁLCULO III · FUNÇÕES A VALORES VETORIAIS E CAMPOS VETORIAIS"


def _placa_img(x0, y0, rects, w, h, feather=12):
    """Placa ESC (#091226, 100 %) com borda esfumada (24 px): ImageMobject RGBA de w × h px (a partir de (x0, y0) do quadro), só nos retângulos dados."""
    from PIL import Image as _I, ImageFilter as _F
    m = _I.new("L", (w, h), 0)
    from PIL import ImageDraw as _D
    d = _D.Draw(m)
    for (a, b, c, e) in rects:
        d.rectangle([a - x0, b - y0, c - x0, e - y0], fill=255)
    m = np.asarray(m.filter(_F.GaussianBlur(feather)), np.uint8)
    arr = np.zeros((h, w, 4), np.uint8)
    arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3] = 0x09, 0x12, 0x26, m
    im = ImageMobject(arr)
    im.set_width(w / 120)
    return im


class Base(Scene):
    """(kit do yt_0022) Todo `play` é quantizado em quadros inteiros e arrasta o relógio `self.clk` (segundos do lote)."""
    CANTO = True          # linha 1 do canto presente desde o início do lote (o T não tem canto; o A o faz entrar)

    def construct(self):
        self.setup_base()
        self.corpo()
        self.fim()

    def setup_base(self):
        usar_papel(self)
        self.liso = False
        if os.environ.get("SO_AUDITORIA") == "1":
            self.renderer.render = lambda *a, **k: None
        self.clk = ValueTracker(0.0)
        self.nq = 0
        self.lote = type(self).__name__
        self._ped = {}
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.9).set_opacity(0.45).move_to(P3(6.9, 4.5 - 65 / 120)).set_z_index(40)   # centro y=65 px
        self.h1 = self._canto(txt(TITULO, 13.2, color="#C8D6F0", op=0.6), 73)       # v8: centro dos caracteres em y = 65 px (baseline 73), como o logo
        self.pl_logo = _placa_img(1600, 0, [(1656, 34, 1920 + 80, 96)], 1920 - 1600, 130)
        self.pl_logo.move_to(P3(-8 + (1600 + 160) / 120 - 0.0, 4.5 - 65 / 120)).set_z_index(-45)
        self.pl_canto = _placa_img(0, 0, self._rects_canto(0), 1000, 170).set_z_index(-45)
        self.pl_canto.move_to(P3(-8 + 500 / 120, 4.5 - 85 / 120))
        self.add(self.pl_logo)
        if self.CANTO:
            self.add(self.pl_canto)
        print(f"[placa] linha 1 = {self.h1.width * 120:.0f} px → placa = {self.h1.width * 120 + 24 + 36:.0f} px (texto + 24 px + margem x = 36)")
        self.h2 = None
        self._pend = []
        self.add(self.wm)
        if self.CANTO:
            self.add(self.h1)
        self._aid, self._q0, self._off, self.alvo = None, 0, None, 0
        self.flash = 0
        self._auto, self._sem_ctn, self._brancos, self._voos = set(), {}, {}, set()
        self.cores = {}         # âncora → [(fração colorida, nº de glifos)]

    @property
    def t(self):
        return self.nq / FPS

    # tempo ---------------------------------------------------------------------------------------------
    def play(self, *anims, run_time=None, **kw):
        if self._pend:
            anims, self._pend = (*anims, *self._pend), []
        anims = tuple(self._vivo(a) for a in anims)
        self._estilo(anims)
        self._still()
        rt = run_time if run_time is not None else max([getattr(a, "run_time", 1.0) for a in anims] or [1.0])
        pontas = []
        for a in anims:
            pontas += self._log_caneta(a)
        if pontas:
            self.add(*pontas)
        n = max(1, round(rt * FPS))
        rtq = n / FPS - FRAC
        t0 = self.nq / FPS
        clk = UpdateFromAlphaFunc(self.clk, lambda m, a: m.set_value(t0 + a * n / FPS), rate_func=linear, run_time=rtq)
        self._em_play = True
        super().play(*anims, clk, run_time=rtq, **kw)
        self._em_play = False
        self.nq += n
        if pontas:
            self.remove(*pontas)

    def _estilo(self, anims=()):
        """Rede de segurança do estilo v3: todo desenho que entra em cena ganha contorno; e a auditoria anota quem ficou sem e quem é branco."""
        def de_anim(a):
            if a.__class__.__name__ == "_AnimationBuilder":
                yield a.mobject
                yield a.mobject.target
                return
            for k in ("mobject", "target_mobject", "target_copy"):
                if getattr(a, k, None) is not None:
                    yield getattr(a, k)
            for b in getattr(a, "animations", None) or []:
                yield from de_anim(b)
        fix = self.fixos()
        for m in [x for x in self.mobjects if x not in fix] + [x for a in anims for x in de_anim(a)]:
            for d in desenhos(m):
                if getattr(d, "_ctn", None) is None:
                    self._auto.add(id(d))
                    contorno(d)
        branco = (ManimColor(WHITE_).to_hex().upper(), "#FFFFFF")
        geo = ManimColor(GEO).to_hex().upper()
        for m in [x for x in self.mobjects if x not in fix]:
            for d in desenhos(m):
                so, fo, w = d.get_stroke_opacity(), d.get_fill_opacity(), d.get_stroke_width()
                if (w > 0 and so > 0.05 or fo > 0.05) and d.get_stroke_width(background=True) <= w:
                    self._sem_ctn.setdefault(id(d), (self._aid, type(d).__name__))
                cs = ManimColor(d.get_stroke_color()).to_hex().upper() if w > 0 and so > 0.05 else None
                cf = ManimColor(d.get_fill_color()).to_hex().upper() if fo > 0.3 else None
                if getattr(d, "_voo", False):
                    self._voos.add(id(d))
                elif cs in branco or cf in branco or (cs == geo and so >= 0.95 and w >= 3):
                    self._brancos.setdefault(id(d), (self._aid, type(d).__name__, "GEO" if cs == geo else "branco"))

    def _vivo(self, a):
        if isinstance(a, (FadeIn, FadeOut)) and isinstance(a.mobject, Fundo3D):
            return a.mobject.op.animate(run_time=a.run_time).set_value(1.0 if isinstance(a, FadeIn) else 0.0).build()
        return a

    def _log_caneta(self, a):
        out = []
        if isinstance(a, _Caneta):
            m = a.mobject
            fc = frac_cor(m)
            self.cores.setdefault(self._aid, []).append((fc, a.n))
            print(f"[algebra] {self._aid} {self.t:7.2f}s glifos={a.n} cor={fc:.0%} rt={a.tot:.1f}s {m._tex!r}")
            a.ponta = Dot(radius=0.028, color=WHITE).set_opacity(0).set_z_index(50)
            a.ponta._sem_contorno = True
            out.append(a.ponta)
        for b in getattr(a, "animations", []) or []:
            out += self._log_caneta(b)
        return out

    def update_to_time(self, t):
        super().update_to_time(t)
        if getattr(self, "_em_play", False):
            self._porta_flash()

    def _porta_flash(self):
        """Portão FLASH POR QUADRO: fórmula de caneta visível antes de ser escrita."""
        for mob in self.mobjects:
            for x in mob.get_family():
                if getattr(x, "_caneta", False) and not x._esc and not x._em_caneta:
                    if any(g.get_fill_opacity() > 0.02 for g in glifos(x)):
                        self.flash += 1
                        print(f"[flash] {self._aid} {self.t:7.2f}s {x._tex!r}")

    def _still(self):
        if STILL is not None and self.nq / FPS >= STILL:
            from manim.utils.exceptions import EndSceneEarlyException
            raise EndSceneEarlyException()

    def wait(self, duration=1.0, *a, **kw):
        self._estilo()
        self._still()
        n = max(1, round(duration * FPS))
        rtq = n / FPS - FRAC
        t0 = self.nq / FPS
        super().play(UpdateFromAlphaFunc(self.clk, lambda m, a_: m.set_value(t0 + a_ * n / FPS), rate_func=linear, run_time=rtq), run_time=rtq)
        self.nq += n

    # âncoras -------------------------------------------------------------------------------------------
    def _k_frase(self, aid, frase):
        import re as _r
        fala = ANC.get(aid, {}).get("fala", "").split()
        alvo = _r.findall(r"\w+", frase.lower())
        return next((i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo), None)

    def gat(self, frase):
        """Espera até LEAD s antes da palavra `frase` da âncora corrente (estimativa a 2,7 palavras/s)."""
        k = self._k_frase(self._aid, frase)
        if k is None:
            print(f"[gatilho-sem-frase] {self._aid}: {frase!r}")
            return
        alvo = self._q0 + max(0.0, ANC[self._aid]["t"][k] - LEAD) * FPS
        if alvo - self.nq >= 1:
            self.wait((alvo - self.nq) / FPS)
        atraso = (self.nq - alvo) / FPS
        print(f"[gatilho] {self._aid} {(self.nq - self._q0) / FPS:6.2f}s (alvo {(alvo - self._q0) / FPS:6.2f}s, atraso {atraso:+.2f}s) {frase}")

    def ate(self, frac):
        alvo = self._q0 + frac * ANC[self._aid]["dur"] * FPS
        if alvo - self.nq >= 1:
            self.wait((alvo - self.nq) / FPS)

    def resta(self):
        return max(0.0, (self.alvo - self.nq) / FPS)

    def an(self, aid):
        """Fecha a âncora anterior (espera o resto da fala) e abre `aid`. O relógio do lote acompanha o da voz estimada."""
        self._fecha()
        a = ANC[aid]
        ini_q = round(a["ini"] * FPS)
        if self._off is None:
            self._off = ini_q - self.nq
        self._aid = aid
        self._q0 = ini_q - self._off
        if self.nq > self._q0:
            print(f"[estouro] {aid} começou {(self.nq - self._q0) / FPS:.2f}s depois do previsto (a cena se esticou)")
            self._off -= self.nq - self._q0           # a cena se estica: as âncoras seguintes andam junto
            self._q0 = self.nq
        self.alvo = round(a["fim"] * FPS) - self._off
        print(f"[ancora] {aid} {self.nq / FPS:.3f}")

    def _fecha(self, antes=0.0):
        """Espera o resto da âncora; `antes` (s): para `antes` segundos antes do fim (v9: a saída de seção cabe dentro da fala, sem deriva)."""
        if self._aid is not None:
            alvo = self.alvo - round(antes * FPS)
            if alvo - self.nq >= 1:
                self.wait((alvo - self.nq) / FPS)
        self._aid = None

    def fim(self):
        fim_alvo = self.alvo
        self._fecha()
        print(f"[deriva] {self.lote} {(self.nq - fim_alvo) / FPS:+.2f}s além do fim da última âncora")
        if PEDIDOS3D and self._ped:
            DIR3D.joinpath("pedidos3d").mkdir(exist_ok=True)
            ped = {"cenas": {c: sorted(d.items()) for c, d in self._ped.items()}}
            (DIR3D / "pedidos3d" / f"{self.lote}.json").write_text(json.dumps(ped, separators=(",", ":")), encoding="utf-8")
            print(f"[3d] pedidos: {', '.join(f'{c}={len(d)}' for c, d in self._ped.items())}")
        fr = [(f, n) for v in self.cores.values() for f, n in v]
        bloco = sum(f * n for f, n in fr) / max(1, sum(n for _, n in fr))
        print(f"[cor-bloco] {self.lote} fração colorida (glifos de caneta) = {bloco:.0%} em {len(fr)} MathTex")
        print(f"[flash-total] {self.lote} {self.flash}")
        from collections import Counter
        print(f"[estilo] {self.lote} traços sem contorno = {len(self._sem_ctn)} {dict(Counter(v[:2] for v in self._sem_ctn.values())) if self._sem_ctn else ''}"
              f" (contorno posto pela varredura: {len(self._auto)})")
        print(f"[estilo] {self.lote} brancos = {len(self._brancos)} {dict(Counter(self._brancos.values())) if self._brancos else ''}"
              f" (setas de voo, permitidas: {len(self._voos)} traços)")
        print(f"[tempo] total {self.nq / FPS:.2f}s ({self.nq} quadros)")

    # cena ----------------------------------------------------------------------------------------------
    @staticmethod
    def _canto(m, base_px, topo_min=None):
        """Linha do canto (handoff v6 §3): x = 36 px, baseline em base_px (1080p; 120 px = 1 u). A baseline é a MEDIANA do fundo dos glifos (acento e cedilha
        não puxam o texto); `topo_min` (px): se a caixa subir acima disso (acento), a linha desce o que faltar."""
        m.move_to(ORIGIN).align_to(P3(-8 + 36 / 120, 0), LEFT)
        bases = [g.get_bottom()[1] for g in m.submobjects if len(g.points)] or [m.get_bottom()[1]]
        m.shift(UP * ((4.5 - base_px / 120) - float(np.median(bases))))
        if topo_min is not None and (4.5 - m.get_top()[1]) * 120 < topo_min:
            m.shift(DOWN * (topo_min - (4.5 - m.get_top()[1]) * 120) / 120)
        return m.set_z_index(40)

    def _rects_canto(self, w2):
        """Retângulos da placa do canto em px (x0, y0, x1, y1): a linha 1 (texto + 24 px) e a linha 2 (a sua largura + 24 px); só atrás do texto."""
        r = [(-80, 30, 36 + self.h1.width * 120 + 24, 90)]
        if w2:
            r.append((-80, 84, 36 + w2 + 24, 132))
        return r

    def _y1_fim_px(self):
        return (4.5 - self.h1.get_bottom()[1]) * 120

    def fixos(self):
        return {self.wm, self.h1, *([self.h2] if self.h2 else [])}

    def secao(self, s):
        """Linha 2 do canto: a antiga sai (0,25 s) antes de a nova entrar (junto do próximo play)."""
        if self.h2 is not None:
            self.play(FadeOut(self.h2), run_time=0.25)
            self.h2 = None
        if s:
            self.h2 = self._canto(txt(s, 21.6, color="#F5F7FF", bold=True), 118, topo_min=self._y1_fim_px() + 10)
            self._pend.append(FadeIn(self.h2))
            self.pl_canto.pixel_array = _placa_img(0, 0, self._rects_canto(self.h2.width * 120), 1000, 170).pixel_array
            print(f"[placa] {s}: linha 2 = {self.h2.width * 120:.0f} px → placa = {self.h2.width * 120 + 24 + 36:.0f} px")

    def snap(self):
        keep = self.fixos()
        return [m for m in self.mobjects if m not in keep and m is not self.clk and not isinstance(m, ValueTracker)]

    def limpa(self, *keep, rt=0.4):
        """Tudo (fora o canto e o que for mantido) sai em `rt` e é removido da cena."""
        sai = [m for m in self.snap() if m not in keep]
        if sai:
            self.play(*[m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in sai], run_time=rt)
        for m in sai:
            m.clear_updaters()
        self.remove(*sai)
        for m in [m for m in self.mobjects if isinstance(m, ValueTracker) and m is not self.clk]:
            self.remove(m)

    def papel(self, liso, rt=0.0):
        """Troca o fundo da câmera entre o milimetrado e o liso (3D). Com rt > 0, a grade some/volta num fade (uma imagem por cima, removida no fim)."""
        if liso == self.liso:
            return
        mm = str(_arq("fundo_calculo_milimetrado"))
        if rt <= 0:
            usar_papel(self, _arq("fundo_calculo_liso") if liso else None)
        else:
            img = ImageMobject(mm).set_width(16).move_to(ORIGIN).set_z_index(-50)
            if liso:
                usar_papel(self, _arq("fundo_calculo_liso"))
                self.add(img)
                self.play(FadeOut(img), run_time=rt)
            else:
                img.set_opacity(0)
                self.add(img)
                self.play(img.animate.set_opacity(1), run_time=rt)
                usar_papel(self)
            self.remove(img)
        self.liso = liso

    def logo(self, largura):
        img = ImageMobject(str(ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"))
        arr = img.get_pixel_array()
        ys, xs = np.nonzero(arr[:, :, 3] > 8)
        return ImageMobject(arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).set_width(largura)

    def hl(self, s, y=3.15, size=T_MAIN, color=WHITE_, x=0.0, bold=True):
        return txt(s, size, color=color, bold=bold).move_to(P3(x, y))

    def sai_fim(self, rt=0.35):
        """Fim do lote: o conteúdo sai até o papel (o próximo lote começa do papel vazio, com a linha 1 do canto)."""
        if self._aid is not None:
            self._fecha(antes=rt + (0.2 if self.h2 is not None else 0.0))
        self.limpa(rt=rt)
        if self.h2 is not None:
            self.play(FadeOut(self.h2), run_time=0.2)
            self.h2 = None


class Plano:
    """Sistema de coordenadas simples (sem eixos desenhados): origem `o` e unidades ux, uy. Mesma interface c2p/p2c dos Axes."""

    def __init__(self, o=(0, 0), ux=1.0, uy=None):
        self.o, self.ux, self.uy = np.array([*o, 0.0][:3], float), ux, uy or ux

    def c2p(self, x, y):
        return self.o + np.array([self.ux * x, self.uy * y, 0.0])

    def p2c(self, p):
        return ((p[0] - self.o[0]) / self.ux, (p[1] - self.o[1]) / self.uy)


def janela_local(cena, ax, folga=0.35, op=0.9, nome=None):
    """Cópia de assets/calculo/papel.py:janela que grava o PNG na própria unidade (renders/janela/), para não escrever em assets/.
    Apaga a grade atrás dos eixos que não encaixam no papel (exceção registrada: painel θρ do B2)."""
    from PIL import Image, ImageDraw, ImageFilter
    w, h = config.pixel_width, config.pixel_height
    k = w / config.frame_width
    x0, y0 = ax.c2p(ax.x_range[0], ax.y_range[0])[:2]
    x1, y1 = ax.c2p(ax.x_range[1], ax.y_range[1])[:2]
    caixa = [(x0 - folga + config.frame_width / 2) * k, (config.frame_height / 2 - y1 - folga) * k,
             (x1 + folga + config.frame_width / 2) * k, (config.frame_height / 2 - y0 + folga) * k]
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle(caixa, radius=40 * k / 120, fill=255)
    m = np.array(m.filter(ImageFilter.GaussianBlur(28 * k / 120)), float)[..., None] / 255 * op
    a = np.array(Image.open(_arq("fundo_calculo_milimetrado")).convert("RGB"), float)
    b = np.array(Image.open(_arq("fundo_calculo_liso")).convert("RGB"), float)
    d = AQUI / "renders" / "janela"
    d.mkdir(parents=True, exist_ok=True)
    saida = d / f"janela_{nome or type(cena).__name__}_{w}x{h}.png"
    Image.fromarray((a * (1 - m) + b * m).astype(np.uint8)).save(saida)
    usar_papel(cena, saida)
    return saida


def _falta(self, frase):
    """Segundos de agora até o gatilho de `frase` (LEAD antes da palavra) na âncora corrente: agenda um evento DENTRO de um play
    (ex.: Succession(Wait(falta), Indicate)) sem segurar a animação que já está rodando."""
    k = self._k_frase(self._aid, frase)
    if k is None:
        print(f"[gatilho-sem-frase] {self._aid}: {frase!r}")
        return 0.0
    alvo = self._q0 + max(0.0, ANC[self._aid]["t"][k] - LEAD) * FPS
    return max(0.0, (alvo - self.nq) / FPS)


Base.falta = _falta


def _caneta_ate(self, m, frase, ritmo=1.0, folga=0.05):
    """v9: caneta que termina até o gatilho de `frase` (o ritmo encolhe se a voz real for mais rápida que a escrita)."""
    c = caneta(m, ritmo=ritmo)
    lim = self.falta(frase) - folga
    if lim > 0.3 and c.tot > lim:
        c = caneta(m, ritmo=ritmo * lim / c.tot)
    return c


Base.caneta_ate = _caneta_ate


# ── polares: "virar e enrolar" (handoff v3 §3.1) ───────────────────────────────────────────────────────
class Polar:
    """Homotopia do retângulo (θ, ρ) ∈ [0, 2π] × [0, ρmax] do painel de entrada até o disco φ(θ, ρ) = ρ(cos θ, sen θ) do painel de saída.
    φ inverte a orientação (jacobiano −ρ na ordem (θ, ρ)): nenhuma deformação contínua sem virar a folha chega ao disco certo.
    1) virar (f de 0 a 1): escala vertical +1 → −1 em torno da linha do meio (ρ = 0 vai para cima);
    2) enrolar (k de 0 a 1): P_k = T_k + Rot(−kπ/2)[(0, D_k) + (S_k ρ + D_k)(sen ψ, −cos ψ)], ψ = k(θ − π), D_k = a_θ(1 − k)/k,
       S_k = (1 − k)a_ρ + k·u_s; T_k vai linearmente do topo-centro da folha virada até a origem da saída. Em k = 1: u_s ρ (cos θ, sen θ)."""

    def __init__(self, ent, sai, rho_max):
        self.ent, self.sai, self.rmax = ent, sai, rho_max
        o = np.array(ent.c2p(0, 0))
        self.a_th = float(ent.c2p(1, 0)[0] - o[0])
        self.a_rho = float(ent.c2p(0, 1)[1] - o[1])
        self.u_s = float(sai.c2p(1, 0)[0] - sai.c2p(0, 0)[0])
        self.T0 = np.array(ent.c2p(PI, rho_max), float)
        self.T1 = np.array(sai.c2p(0, 0), float)
        self.ymeio = float(ent.c2p(0, rho_max / 2)[1])

    def virar(self, th, rho, f):
        p = np.array(self.ent.c2p(th, rho), float)
        p[1] = self.ymeio + (p[1] - self.ymeio) * math.cos(PI * f)
        return p

    def enrolar(self, th, rho, k):
        if k < 1e-3:
            return self.virar(th, rho, 1.0)
        D = self.a_th * (1 - k) / k
        S = (1 - k) * self.a_rho + k * self.u_s
        ps = k * (th - PI)
        lx, ly = (S * rho + D) * math.sin(ps), D - (S * rho + D) * math.cos(ps)
        a = -k * PI / 2
        T = (1 - k) * self.T0 + k * self.T1
        return T + np.array([lx * math.cos(a) - ly * math.sin(a), lx * math.sin(a) + ly * math.cos(a), 0.0])

    def erro_k1(self):
        """Maior distância (px) entre P_1(θ, ρ) e φ(θ, ρ) na saída."""
        pior = 0.0
        for th in np.linspace(0, 2 * PI, 25):
            for rho in np.linspace(0, self.rmax, 9):
                q = np.array(self.sai.c2p(rho * math.cos(th), rho * math.sin(th)), float)
                pior = max(pior, float(np.linalg.norm(self.enrolar(th, rho, 1.0) - q)))
        return pior * config.pixel_width / 16

    @staticmethod
    def curva(amostras, fechada=False):
        """VMobject vazio que guarda as amostras (θ, ρ) que o define."""
        m = VMobject()
        m._amostras, m._fechada = list(amostras), fechada
        return m

    def poe(self, m, fn):
        pts = [fn(th, rho) for th, rho in m._amostras]
        if m._fechada:
            pts.append(pts[0])
        m.set_points_as_corners(pts)
        return m

    def anim_virar(self, grupo, rt=1.0):
        folhas = [m for m in grupo.family_members_with_points() if hasattr(m, "_amostras")] or \
                 [m for m in grupo.get_family() if hasattr(m, "_amostras")]
        base = {id(m): (m.get_fill_opacity(), m.get_stroke_opacity()) for m in folhas}

        def upd(g, a):
            esc = 0.55 + 0.45 * abs(math.cos(PI * a))                      # escurece no meio, como folha virando
            for m in folhas:
                self.poe(m, lambda th, rho: self.virar(th, rho, a))
                fo, so = base[id(m)]
                m.set_fill(opacity=fo * esc).set_stroke(opacity=so * esc)
        return UpdateFromAlphaFunc(grupo, upd, run_time=rt)

    def anim_enrolar(self, grupo, rt=3.0, log=None):
        folhas = [m for m in grupo.get_family() if hasattr(m, "_amostras")]

        def upd(g, a):
            k = smooth(a)
            for m in folhas:
                self.poe(m, lambda th, rho: self.enrolar(th, rho, k))
        return UpdateFromAlphaFunc(grupo, upd, run_time=rt)


def alfa_de_k(k):
    """α tal que smooth(α) = k (bisseção): para achar o quadro de cada k na folha de contato."""
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if smooth(mid) < k else (lo, mid)
    return (lo + hi) / 2


def retangulo_polar(pol, rho_max, d_rho=0.5, d_th=PI / 4, n=48):
    """Retângulo B (chapa de domínio), famílias ρ fixo (magenta) e θ fixo (âmbar), traço 3 (a da borda, 4), como curvas amostradas para o Polar."""
    ths = np.linspace(0, 2 * PI, 4 * n)
    rhs = np.linspace(0, rho_max, n // 2)
    borda = [(t, 0.0) for t in ths] + [(2 * PI, r) for r in rhs] + [(t, rho_max) for t in ths[::-1]] + [(0.0, r) for r in rhs[::-1]]
    fundo = Polar.curva(borda, fechada=True)
    fr = VGroup(*[Polar.curva([(t, r) for t in ths]).set_stroke(E2, W_FAM_B if abs(r - rho_max) < 1e-6 else W_FAM)
                  for r in np.arange(d_rho, rho_max + 1e-6, d_rho)])
    nt = int(round(2 * PI / d_th))
    ft = VGroup(*[Polar.curva([(k * d_th, r) for r in rhs]).set_stroke(E1, W_FAM_B if k in (0, nt) else W_FAM) for k in range(nt + 1)])
    g = VGroup(fundo, fr, ft)
    for m in g.get_family():
        if hasattr(m, "_amostras"):
            pol.poe(m, lambda th, rho: pol.ent.c2p(th, rho))
    chapa(fundo)
    return contorno(g)
