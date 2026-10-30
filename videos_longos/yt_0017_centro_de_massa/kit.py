"""yt_0017 — kit comum: paleta, marcador do centro de massa, texto, setas, corpos 2D, fronteira, cavalo, pedra, pessoa de perfil,
cabeçalho e relógio por quadro.

Copiado do kit do yt_0016 (que veio do yt_0015; não importa entre unidades). Preview silencioso: o tempo de cada âncora vem de ancoras.json
(palavras da narração congelada ÷ 2,7 palavras/s); a cena se estica para a voz depois. Pessoas e cavalo são silhuetas 2D preenchidas
(cápsulas), nunca linhas.
"""
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from manim import *  # noqa: F401,F403

Circle.set_default(color=WHITE)   # fill padrão RED aparecia ao esmaecer com set_opacity

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parents[1]
sys.path.insert(0, str(ROOT))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import DISPLAY_FONT, official_text, screen_text  # noqa: E402

# a álgebra (LaTeX, traço fino) ganha um contorno leve da própria cor: no 540p o glifo fino ficava acinzentado ao lado do título
TRACO_TEX = 0.8
_mathtex_init = MathTex.__init__


def _mathtex_com_traco(self, *a, **k):
    _mathtex_init(self, *a, **k)
    self.set_stroke(width=TRACO_TEX, family=True)


MathTex.__init__ = _mathtex_com_traco
OP_FUNDO = 0.6                # equação "de fundo" (já usada, ou sob a DICA): 0,6 mantém contraste ≥ 4,5:1 no céu

config.media_dir = os.environ.get("MEDIA_DIR", str(AQUI / "media"))

# ── paleta (padrão de Mecânica, docs/padrao_video_longo.md §4 + handoff §4) ─────────────────────────────────
WHITE_ = TEXT_COLOR          # #F5F7FF
CYAN = PRIMARY_COLOR         # #35D9FF (energia cinética e assunto do próximo vídeo)
KC = CYAN                    # energia cinética
HEAT = "#FF7A3D"             # calor / energia dissipada
MAG = "#EA63FF"              # momento p, P, Δp
VEL = "#9C8CFF"              # velocidade
FC = "#5AA2FF"               # força externa (e força em geral)
INT = "#7D8798"              # força interna / tensão (cinza apagado)
JC = "#9CC7FF"               # impulso
STEEL = "#7A8696"
GEO = "#B8C4DA"
DIM = "#8FA3C4"
PANEL = "#0E2A52"
BLUE_L = "#7FB2FF"
TERRA = "#4A5262"            # Terra / chão como corpo: aço mais escuro
APAGADO = "#6B7788"          # conta errada riscada
GELO = "#7FB2FF"
CM_COL = WHITE_              # cruz do ⊕ (branca, fina)
CM_A, CM_B = "#35D9FF", "#EA63FF"   # v3: o ⊕ é o degradê ciano → magenta da marca (exclusivo: nenhuma grandeza usa degradê, G15)
CMC = "#8BE9FF"              # posição do ⊕ nas contas (R⃗_cm, X, Y, X_cm, R⃗₀): ciano-claro
RAST = "#9FB4D6"             # rastros finos dos corpos (aço-azulado)
VREL = "#C4BAFF"             # velocidade relativa ao CM (violeta clareado ~35%)


def mix(c, w):
    return interpolate_color(ManimColor(c), ManimColor(WHITE_), w).to_hex()


def escuro(c, w):
    return interpolate_color(ManimColor(c), ManimColor(BACKGROUND_COLOR), w).to_hex()


T_HL, T_MAIN, T_LAB, T_SMALL = 44, 34, 26, 22
M_MAIN, M_MID, M_REF, M_LAB = 68, 56, 46, 40
FPS = 15
FRAC = 0.02 / FPS            # folga p/ np.arange não criar um quadro extra

AUDITORIA = os.environ.get("AUDITORIA") == "1"
STILL = float(os.environ["STILL"]) if os.environ.get("STILL") else None   # still num instante (use com -s)

ANC = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]


def dur(aid):
    return ANC[aid]["dur"]


# ── texto e matemática ───────────────────────────────────────────────────────────────────────────────────
def txt(s, size=T_MAIN, color=WHITE_, op=1.0, bold=False):
    """Texto editorial: Space Grotesk em CAIXA ALTA (símbolos matemáticos vão em MathTex, nunca aqui)."""
    s = s.upper()
    if bold:
        m = official_text(s, DISPLAY_FONT, BOLD, size, oversample=2, color=color).set_opacity(op)
    else:
        m = screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(op)
    m._tam = size
    return m


def rot(s, size=30, color=WHITE_, op=1.0):
    """Rótulo de massa/número no texto do canal (Space Grotesk), sem caixa alta: `1 kg`, `60 kg`, `2`."""
    m = screen_text(s, size, color=color, oversample=4).set_opacity(op)
    m._tam = size
    return m


_MEMO = {}


def memo(chave, fazer):
    """Cópia de um mobject criado uma vez só (textos dentro de always_redraw: criar Text a cada quadro é caro)."""
    if chave not in _MEMO:
        _MEMO[chave] = fazer()
    return _MEMO[chave].copy()


def mtxt(s, size=T_MAIN, color=WHITE_, op=1.0, bold=False):
    return memo(("txt", s, size, color, bold), lambda: txt(s, size, color, 1.0, bold)).set_opacity(op)


def mrot(s, size=30, color=WHITE_, op=1.0):
    """rot() guardado (rótulos e números dentro de camadas vivas: unidade do SI em minúscula, G9)."""
    m = memo(("rot", s, size, color), lambda: rot(s, size, color))
    m._tam = size
    return m.set_opacity(op)


def mtex(s, cor=WHITE_, size=M_MID):
    m = memo(("tex", s, cor, size), lambda: MathTex(s, font_size=size, color=cor))
    m._partes = [(s, cor)]
    return m


def tex(s, cor=WHITE_, size=M_MID):
    return MathTex(s, font_size=size, color=cor)


def Mc(*pares, size=M_MID, w=None):
    """MathTex em partes coloridas: cada par é (tex, cor|None). Cada parte precisa ser um TeX completo."""
    partes = [p[0] if isinstance(p, tuple) else p for p in pares]
    cores = [p[1] if isinstance(p, tuple) else None for p in pares]
    m = MathTex(*partes, font_size=size, color=WHITE_)
    for sub, c in zip(m.submobjects, cores):
        if c:
            sub.set_color(c)
    if w and m.width > w:
        m.scale_to_fit_width(w)
    m._partes = [(t, c or WHITE_) for t, c in zip(partes, cores)]
    return m


_NG = {}


def ng(tex_):
    """Quantos glifos um pedaço de TeX gera (sozinho)."""
    if tex_ not in _NG:
        _NG[tex_] = len(MathTex(tex_)[0]) if tex_.strip() else 0
    return _NG[tex_]


def eqp(*partes, size=M_MID, cores=None):
    """MathTex de string única montado por partes, com o índice de glifos de cada parte (para TransformByGlyphMap sem contar à mão).
    Retorna (MathTex, lista de listas de índices). `cores`: {índice da parte: cor} (G12: cor por grandeza)."""
    m = MathTex("".join(partes), font_size=size, color=WHITE_)
    idx, k = [], 0
    for t in partes:
        n = ng(t)
        idx.append(list(range(k, k + n)))
        k += n
    assert k == len(m[0]), f"glifos {k} != {len(m[0])} em {''.join(partes)}"
    for i, c in (cores or {}).items():
        for j in idx[i]:
            m[0][j].set_color(c)
    m._partes = [(t, (cores or {}).get(i, WHITE_)) for i, t in enumerate(partes)]
    return m, idx


# ── cor por token (G12, handoff v3 §1.1): a cor esperada de cada grandeza (None = parte composta, não conferida) ───────────────
import re as _re
_REGRAS = [
    (CMC, (r"\\vec R_\{cm\}(\(t\))?", r"X", r"Y", r"X_\{cm\}", r"\\vec R_0")),
    (GEO, (r"\\vec r_[i123]", r"x_[12i]", r"y_i", r"d_[12]", r"\\vec R_\{\\rm (I|II)\}", r"\\vec r_1=\\vec 0")),
    (VEL, (r"\\vec v(_[i12])?", r"\\vec V_\{cm\}", r"\\vec V_0(\\,t)?", r"\\Delta\\vec V_\{cm\}")),
    (MAG, (r"\\vec P", r"\\vec p(_[i12])?", r"m_i\\vec v_i", r"\\frac\{d\\vec P\}\{dt\}")),
    (FC, (r"\\vec F.*", r"M\\vec g", r"\\vec g")),
    (JC, (r"\\vec J",)),
    (WHITE_, (r"[0-9,.;\\ {}]+", r"[=+\-()]", r"M", r"m_[i12]", r"\\sum_i", r"\\cdot", r"\\,\(", r"\)", r"\\vec 0", r"M_\{\\rm (I|II)\}")),
]


def cor_esperada(t):
    t = t.strip()
    for cor, pads in _REGRAS:
        if any(_re.fullmatch(p, t) for p in pads):
            return cor
    return None


def caixa(m, cor=BLUE_L, buff=0.18):
    """Caixa de resultado (G11): PANEL a 85% com borda na cor da grandeza (BLUE_L se não houver uma). Nunca branca."""
    r = RoundedRectangle(corner_radius=0.1, width=m.width + 2 * buff, height=m.height + 2 * buff).move_to(m) \
        .set_fill(PANEL, 0.85).set_stroke(cor, 2.5)
    r._fundo = r._caixa = True
    return r.set_z_index(m.z_index - 1 if m.z_index else -1)


def cartao(*linhas, size=28, cor=BLUE_L):
    """Frase explicativa em cartão PANEL com texto branco (no lugar de texto DIM solto)."""
    t = VGroup(*[txt(l, size) for l in linhas]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    r = RoundedRectangle(corner_radius=0.1, width=t.width + 0.44, height=t.height + 0.32).move_to(t).set_fill(PANEL, 0.9).set_stroke(cor, 2)
    r._fundo = True
    return VGroup(r, t).set_z_index(20)


def linha(*itens, buff=0.2, size=T_MAIN, color=WHITE_):
    """Linha mista: str vira txt(); mobjects entram como estão (alinhados pela base visual)."""
    return VGroup(*[txt(i, size, color) if isinstance(i, str) else i for i in itens]).arrange(RIGHT, buff=buff)


def P3(x, y):
    return np.array([x, y, 0.0])


def arrow(a, b, color=WHITE_, width=5, z=8, tip=0.2, op=1.0):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    L = np.linalg.norm(b - a)
    if L < 0.03:
        return VMobject()
    if L < 3 * tip:                     # ponta sempre visível
        b = a + (b - a) / L * 3 * tip
    m = Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.45,
              max_stroke_width_to_length_ratio=50)
    return m.set_opacity(op).set_z_index(z)


def placa(w, h, centro, op=0.05, borda=0.24):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h).set_stroke(WHITE_, 1.4, opacity=borda) \
        .set_fill(WHITE_, op).move_to(centro).set_z_index(-2)


def risco(m, cor=APAGADO, w=4):
    """Traço diagonal sobre um mobject (item riscado)."""
    r_ = Line(m.get_corner(DL) + 0.04 * UR, m.get_corner(UR) - 0.04 * UR).set_stroke(cor, w).set_z_index(30)
    r_._risco = True                                                    # o risco é sobre o texto de propósito (fora da auditoria)
    return r_


class Corpo(VGroup):
    """Bloco 2D chato: aço, contorno claro e filete interno (sem 3D falso)."""

    def __init__(self, nome, cor, lado, alt=None, size=36):
        super().__init__()
        alt = alt or lado
        self.lado, self.alt = lado, alt
        f = RoundedRectangle(corner_radius=0.04, width=lado, height=alt).set_stroke(mix(cor, 0.5), 2).set_fill(cor, 1.0)
        ins = min(0.07, 0.12 * min(lado, alt))
        filete = RoundedRectangle(corner_radius=0.03, width=max(lado - 2 * ins, 0.02), height=max(alt - 2 * ins, 0.02)) \
            .set_stroke(WHITE_, 1, opacity=0.35).set_fill(cor, 0).move_to(f)
        self.front = f
        self.add(f, filete)
        if nome:
            esc = cor == GEO
            self.lab = MathTex(nome, font_size=size, color=BACKGROUND_COLOR if esc else WHITE_).move_to(f)
            self.add(self.lab)

    def at(self, x, yb):
        self.shift(P3(x, yb + self.alt / 2) - self.front.get_center())
        return self


def bola(r=0.28, cor=STEEL):
    c = Circle(radius=r).set_stroke(mix(cor, 0.5), 2).set_fill(cor, 1.0)
    return VGroup(c, Circle(radius=r * 0.78).set_stroke(WHITE_, 1, opacity=0.3).set_fill(cor, 0)).set_z_index(5)


def dica(*linhas, size=28):
    """Cartão PANEL com borda BLUE_L no canto inferior direito: 'DICA' em ciano e a frase em maiúsculas. Cada linha é uma str
    ou uma lista de str/mobjects (símbolos matemáticos entram como MathTex, nunca dentro de txt())."""
    corpo = VGroup()
    for l in linhas:
        corpo.add(txt(l, size) if isinstance(l, str) else linha(*l, buff=0.1, size=size))
    corpo.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    tag = txt("DICA", 24, color=CYAN, bold=True)
    g = VGroup(tag, corpo).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    cx_ = RoundedRectangle(corner_radius=0.12, width=g.width + 0.6, height=g.height + 0.44).set_stroke(BLUE_L, 2) \
        .set_fill(PANEL, 0.97).move_to(g)
    cx_._fundo = True
    return VGroup(cx_, g).set_z_index(35).to_corner(DR, buff=0.5)


def fronteira(w, h, centro, rotulo="SISTEMA", lado=UL, size=20, op=0.62):
    """Fronteira tracejada do sistema (retângulo arredondado) com o rótulo pequeno no canto de fora."""
    r = RoundedRectangle(corner_radius=0.3, width=w, height=h).move_to(centro).set_stroke(WHITE_, 2.2, opacity=op)
    d = DashedVMobject(r, num_dashes=max(24, int((w + h) * 5)), dashed_ratio=0.55).set_z_index(1)
    g = VGroup(d)
    if rotulo:
        lab = (txt(rotulo, size, color=WHITE_, op=0.8) if isinstance(rotulo, str) else
               linha(*rotulo, size=size, buff=0.1).set_opacity(0.8)).next_to(r.get_corner(lado), UP, buff=0.1)
        lab.align_to(r, LEFT if lado[0] <= 0 else RIGHT).shift((0.25 if lado[0] <= 0 else -0.25) * RIGHT)
        g.add(lab)
    return g


def mais(size=28, s="+"):
    """Conectivo matemático (+, =) para textos de tela montados com linha()."""
    return MathTex(s, font_size=size, color=WHITE_)


def chao(x0, x1, y, cor=GEO, op=0.5, seed=3, dens=2.2):
    """Chão com textura: linha + riscos curtos e pedrinhas abaixo (fixos)."""
    rng = np.random.default_rng(seed)
    g = VGroup(Line(P3(x0, y), P3(x1, y)).set_stroke(cor, 2.5, opacity=op))
    n = int((x1 - x0) * dens)
    for _ in range(n):
        x = rng.uniform(x0 + 0.1, x1 - 0.2)
        dy = rng.uniform(0.08, 0.3)
        L = rng.uniform(0.08, 0.22)
        g.add(Line(P3(x, y - dy), P3(x + L, y - dy)).set_stroke(cor, 1.5, opacity=op * 0.45))
    for _ in range(n // 2):
        g.add(Dot(P3(rng.uniform(x0 + 0.1, x1 - 0.1), y - rng.uniform(0.06, 0.32)), radius=0.022, color=cor).set_opacity(op * 0.5))
    return g.set_z_index(0)


def gelo(x0, x1, y, h=0.26, seed=5):
    """Faixa de gelo azulada (lago congelado / chão de gelo) com reflexos finos."""
    rng = np.random.default_rng(seed)
    g = VGroup(Rectangle(width=x1 - x0, height=h).move_to(P3((x0 + x1) / 2, y - h / 2)).set_stroke(width=0).set_fill(GELO, 0.16),
               Line(P3(x0, y), P3(x1, y)).set_stroke(mix(GELO, 0.4), 2.5, opacity=0.8))
    for _ in range(int((x1 - x0) * 1.6)):
        x = rng.uniform(x0 + 0.1, x1 - 0.5)
        g.add(Line(P3(x, y - rng.uniform(0.05, h - 0.04)), P3(x + rng.uniform(0.2, 0.5), y - rng.uniform(0.05, h - 0.04)))
              .set_stroke(mix(GELO, 0.5), 1.4, opacity=0.45))
    return g.set_z_index(0)


# ── silhueta humana de perfil (cápsulas preenchidas; nunca linhas) ─────────────────────────────────────────
def capsula2d(a, b, r, cor=STEEL, borda=None):
    a, b = np.asarray(a, float), np.asarray(b, float)
    L = max(np.linalg.norm(b - a), 1e-3)
    c = RoundedRectangle(corner_radius=r * 0.999, width=L + 2 * r, height=2 * r).set_stroke(borda or mix(cor, 0.45), 1.5) \
        .set_fill(cor, 1.0)
    c.rotate(math.atan2(*(b - a)[[1, 0]])).move_to((a + b) / 2)
    return c


POSES = {
    # ângulos a partir da vertical para baixo; positivo = para a frente (rad). tr: inclinação do tronco para a frente.
    "pe": dict(cf=0.04, jf=0.0, ct=-0.04, jt=0.0, bf=0.12, af=0.22, bt=-0.08, at=0.05, tr=0.0),
    "agarra": dict(cf=0.06, jf=0.0, ct=-0.12, jt=-0.12, bf=1.15, af=1.45, bt=0.9, at=1.35, tr=0.08),
    "mira": dict(cf=0.18, jf=0.05, ct=-0.2, jt=-0.2, bf=1.25, af=1.6, bt=0.75, at=1.55, tr=0.05),
    "sentado": dict(cf=1.45, jf=0.15, ct=1.5, jt=0.25, bf=2.6, af=2.95, bt=0.55, at=1.05, tr=-0.05),
    "joga": dict(cf=1.45, jf=0.15, ct=1.5, jt=0.25, bf=2.9, af=3.05, bt=0.45, at=0.9, tr=-0.1),
}


class PessoaPerfil(VGroup):
    """Pessoa de perfil olhando para `sen` (+1 direita). Pés (ou o quadril, se `quadril` for dado) apoiados em y.
    self.pts guarda pontos úteis: mao_f, mao_t, pe_f, pe_t, peito, cabeca, quadril, ombro."""

    def __init__(self, x=0.0, y=0.0, alt=1.9, sen=1, pose="pe", cor=STEEL, quadril=None, extra=None):
        super().__init__()
        k = alt / 1.76
        p = dict(POSES[pose] if isinstance(pose, str) else pose)
        if extra:
            p.update(extra)
        s = sen
        d = lambda a, L: L * k * np.array([math.sin(a) * s, -math.cos(a), 0.0])
        hip = np.array([0.0, 0.95 * k, 0.0])
        ombro = hip + 0.52 * k * np.array([math.sin(p["tr"]) * s, math.cos(p["tr"]), 0.0])
        joelho_f, joelho_t = hip + d(p["cf"], 0.45), hip + d(p["ct"], 0.45)
        tor_f, tor_t = joelho_f + d(p["jf"], 0.44), joelho_t + d(p["jt"], 0.44)
        cot_f, cot_t = ombro + d(p["bf"], 0.29), ombro + d(p["bt"], 0.29)
        mao_f, mao_t = cot_f + d(p["af"], 0.26), cot_t + d(p["at"], 0.26)
        pesc = ombro + 0.07 * k * np.array([math.sin(p["tr"]) * s, 1.0, 0.0])
        cab = ombro + k * np.array([(0.04 + 0.17 * math.sin(p["tr"])) * s, 0.2, 0.0])
        if quadril is None:
            base = min(tor_f[1], tor_t[1]) - 0.045 * k
            off = np.array([x, y - base, 0.0])
        else:
            off = np.array([x, quadril - hip[1], 0.0])
        fundo = escuro(cor, 0.38)

        def perna(j, t, c):
            pe = RoundedRectangle(corner_radius=0.035 * k, width=0.25 * k, height=0.075 * k).set_stroke(mix(c, 0.4), 1.5) \
                .set_fill(c, 1).move_to(t + np.array([0.08 * k * s, -0.01 * k, 0]))
            return VGroup(capsula2d(hip, j, 0.088 * k, c), capsula2d(j, t, 0.062 * k, c), pe)

        def braco(cv, m, c):
            return VGroup(capsula2d(ombro, cv, 0.056 * k, c), capsula2d(cv, m, 0.045 * k, c),
                          Ellipse(width=0.075 * k, height=0.1 * k).set_stroke(mix(c, 0.4), 1.5).set_fill(c, 1).move_to(m))

        self.add(braco(cot_t, mao_t, fundo), perna(joelho_t, tor_t, fundo))
        tronco = VGroup(capsula2d(hip + 0.04 * k * UP, ombro - 0.03 * k * np.array([math.sin(p["tr"]) * s, 1, 0]), 0.155 * k, cor),
                        capsula2d(ombro - 0.02 * k * UP, pesc, 0.045 * k, cor))
        cabeca = Ellipse(width=0.2 * k, height=0.25 * k).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1).move_to(cab)
        nariz = Ellipse(width=0.05 * k, height=0.04 * k).set_stroke(width=0).set_fill(cor, 1).move_to(cab + np.array([0.1 * k * s, -0.01 * k, 0]))
        self.add(perna(joelho_f, tor_f, cor), tronco, nariz, cabeca, braco(cot_f, mao_f, cor))
        for q in (hip, joelho_f, ombro, cot_f):
            self.add(Dot(q, radius=0.03 * k, color=GEO).set_z_index(1))
        self.shift(off)
        self.pts = {n: v + off for n, v in dict(mao_f=mao_f, mao_t=mao_t, pe_f=tor_f, pe_t=tor_t, peito=ombro + d(1.6, 0.12) - 0.15 * k * UP,
                                                cabeca=cab, quadril=hip, ombro=ombro).items()}
        self.k = k


def silhueta(p_, cor=STEEL):
    """G18: a pessoa (PessoaPerfil) vira uma silhueta só de corpo inteiro (união das partes, sem juntas nem pontos), em aço com
    sombreado (claro em cima, escuro embaixo) e o recorte BLUE_L na borda. Guarda .pts do original."""
    partes = [m for m in p_.submobjects if not isinstance(m, Dot)]
    folhas = [x for m in partes for x in m.family_members_with_points() if isinstance(x, VMobject) and not isinstance(x, Dot)]
    try:
        s = Union(*folhas)
    except Exception:                                   # a união falha em algumas poses: as partes, todas no mesmo aço (sem juntas nem pontos)
        s = VGroup(*[f.copy() for f in folhas])
    s.set_fill(["#9AA6B8", "#7A8696", "#3A4252"], 1.0).set_sheen_direction(UP).set_stroke("#7FB2FF", 2.4, opacity=0.8)   # luz B
    s._degrade = "aco"
    s.pts, s.k = dict(p_.pts), p_.k
    return s


def andar(fase, amp=0.42):
    """Pose de caminhada (perfil) na fase `fase` (rad): pernas e braços alternados, joelho dobrando no balanço."""
    a = amp * math.sin(fase)
    dob = lambda u: -0.6 * max(0.0, math.sin(u + 0.6))
    return dict(cf=a, jf=a + dob(fase), ct=-a, jt=-a + dob(fase + PI), bf=-0.6 * a, af=-0.6 * a + 0.35, bt=0.6 * a, at=0.6 * a + 0.35,
                tr=0.06)


# ── cavalo de perfil, patas articuladas (dois segmentos), preenchido em aço ─────────────────────────────────
CAV_PERNAS = ((-0.95, 1.5, 0.0, True), (0.72, 1.52, 0.5 * PI, True), (-0.7, 1.5, PI, False), (0.95, 1.52, 1.5 * PI, False))


def cavalo(fase=0.0, passo=0.0, cor=STEEL):
    """Cavalo virado para a direita, cascos em y≈0. `fase` (rad) do ciclo de passo; `passo` = 0 parado … 1 passo cheio.
    Retorna (VGroup, pontos) com 'peito' (peitoral), 'traseira', 'cascos' (lista dos 4 cascos), 'dorso'."""
    borda = mix(cor, 0.45)
    longe = escuro(cor, 0.35)
    g_tras, g_frente = VGroup(), VGroup()
    cascos = []
    L1, L2 = 0.74, 0.72
    for x, y, ph, perto in CAV_PERNAS:
        u = fase + ph
        a1 = passo * 0.3 * math.sin(u)
        dobra = passo * 0.75 * max(0.0, math.sin(u + 1.2))
        dianteira = x > 0
        a2 = a1 - dobra if dianteira else a1 + 0.45 * dobra
        top = P3(x, y)
        jo = top + L1 * P3(math.sin(a1), -math.cos(a1))
        pe = jo + L2 * P3(math.sin(a2), -math.cos(a2))
        c = cor if perto else longe
        casco = RoundedRectangle(corner_radius=0.04, width=0.25, height=0.13).set_stroke(width=0).set_fill(GEO if perto else escuro(GEO, 0.3), 1) \
            .move_to(pe + P3(0.02, -0.02))
        perna = VGroup(capsula2d(top, jo, 0.13, c, borda), capsula2d(jo, pe, 0.08, c, borda), casco)
        (g_frente if perto else g_tras).add(perna)
        cascos.append(pe + P3(0.02, -0.085))
    base = min(p[1] for p in cascos)
    corpo = Ellipse(width=2.55, height=1.08).set_stroke(borda, 2).set_fill(cor, 1).move_to(P3(0, 1.78))
    anca = Ellipse(width=1.0, height=1.0).set_stroke(width=0).set_fill(cor, 1).move_to(P3(-0.85, 1.86))
    pesc = Polygon(P3(0.7, 1.98), P3(1.05, 2.4), P3(1.5, 3.05), P3(1.85, 2.85), P3(1.45, 2.05), P3(1.15, 1.58)) \
        .set_stroke(borda, 2).set_fill(cor, 1)
    cab = Polygon(P3(1.5, 3.05), P3(1.75, 3.25), P3(2.42, 2.78), P3(2.52, 2.56), P3(2.32, 2.44), P3(1.75, 2.68)) \
        .set_stroke(borda, 2).set_fill(cor, 1)
    orelha = Polygon(P3(1.62, 3.1), P3(1.7, 3.45), P3(1.82, 3.15)).set_stroke(borda, 2).set_fill(cor, 1)
    crina = Polygon(P3(0.82, 2.12), P3(1.5, 3.14), P3(1.42, 2.76), P3(1.0, 2.05)).set_stroke(width=0).set_fill(GEO, 0.85)
    cauda = Polygon(P3(-1.2, 2.05), P3(-1.55, 1.88), P3(-1.78, 1.1), P3(-1.56, 1.14), P3(-1.36, 1.66)).set_stroke(width=0).set_fill(GEO, 0.85)
    olho = Dot(P3(2.03, 2.86), radius=0.04, color=BACKGROUND_COLOR)
    peitoral = RoundedRectangle(corner_radius=0.06, width=0.16, height=0.72).set_stroke(width=0).set_fill(GEO, 1).rotate(-0.35) \
        .move_to(P3(1.12, 1.7))
    tirante = Line(P3(1.05, 1.62), P3(-1.25, 1.62)).set_stroke(GEO, 3.5)
    g = VGroup(cauda, g_tras, anca, corpo, pesc, crina, cab, orelha, olho, g_frente, tirante, peitoral).shift(P3(0, -base))
    pts = dict(peito=P3(1.12, 1.62 - base), traseira=P3(-1.25, 1.62 - base), dorso=P3(0.0, 2.4 - base),
               cascos=[c + P3(0, -base) for c in cascos], cabeca=P3(1.9, 3.3 - base))
    return g, pts


def pedra(cor=TERRA):
    """Pedra grande facetada; base em y = 0, frente (onde amarra a corda) em x≈1,0."""
    contorno = [P3(-1.05, 0.0), P3(-1.18, 0.55), P3(-0.85, 1.12), P3(-0.1, 1.32), P3(0.62, 1.12), P3(1.05, 0.62), P3(1.0, 0.0)]
    base = Polygon(*contorno).set_stroke(mix(cor, 0.4), 2).set_fill(cor, 1)
    f1 = Polygon(P3(-0.85, 1.12), P3(-0.1, 1.32), P3(0.15, 0.8), P3(-0.55, 0.62)).set_stroke(mix(cor, 0.25), 1.2).set_fill(mix(cor, 0.12), 1)
    f2 = Polygon(P3(0.15, 0.8), P3(-0.1, 1.32), P3(0.62, 1.12), P3(1.05, 0.62), P3(0.55, 0.42)).set_stroke(mix(cor, 0.25), 1.2) \
        .set_fill(mix(cor, 0.06), 1)
    f3 = Polygon(P3(-1.18, 0.55), P3(-0.55, 0.62), P3(-0.3, 0.0), P3(-1.05, 0.0)).set_stroke(mix(cor, 0.2), 1.2).set_fill(escuro(cor, 0.15), 1)
    gancho = Circle(radius=0.08).set_stroke(GEO, 3).set_fill(cor, 0).move_to(P3(1.06, 0.55))
    return VGroup(base, f3, f1, f2, gancho)


# ── objetos pequenos ─────────────────────────────────────────────────────────────────────────────────────
def rifle(ang=0.0, comp=1.5, cor=STEEL):
    """Rifle preenchido (coronha, ação, cano), apontando no ângulo `ang`; origem na coronha (ombro). Retorna (VGroup, boca)."""
    g = VGroup(
        Polygon(P3(0, -0.06), P3(0.32, -0.04), P3(0.42, 0.05), P3(0.0, 0.1), P3(-0.04, -0.02)).set_stroke(mix(cor, 0.45), 1.5).set_fill(escuro(cor, 0.15), 1),
        RoundedRectangle(corner_radius=0.03, width=0.4, height=0.12).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1).move_to(P3(0.58, 0.04)),
        RoundedRectangle(corner_radius=0.02, width=comp - 0.7, height=0.055).set_stroke(mix(cor, 0.45), 1.2).set_fill(mix(cor, 0.2), 1)
        .move_to(P3(0.78 + (comp - 0.7) / 2, 0.06)),
        Polygon(P3(0.5, -0.02), P3(0.55, -0.14), P3(0.62, -0.14), P3(0.62, -0.02)).set_stroke(width=0).set_fill(cor, 1))
    g.rotate(ang, about_point=ORIGIN)
    boca = P3((comp + 0.08) * math.cos(ang) - 0.06 * math.sin(ang), (comp + 0.08) * math.sin(ang) + 0.06 * math.cos(ang))
    return g.set_z_index(6), boca


def bala_mob(ang=0.0, cor=GEO):
    return RoundedRectangle(corner_radius=0.035, width=0.2, height=0.07).set_stroke(width=0).set_fill(cor, 1).rotate(ang).set_z_index(7)


def ima(cor=STEEL):
    """Ímã em U preenchido (pontas claras)."""
    arco = AnnularSector(inner_radius=0.12, outer_radius=0.26, angle=PI, start_angle=PI).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1)
    perna_e = Rectangle(width=0.14, height=0.22).set_stroke(mix(cor, 0.45), 1.5).set_fill(cor, 1).move_to(P3(-0.19, 0.11))
    perna_d = perna_e.copy().move_to(P3(0.19, 0.11))
    ponta_e = Rectangle(width=0.14, height=0.08).set_stroke(width=0).set_fill(GEO, 1).move_to(P3(-0.19, 0.26))
    ponta_d = ponta_e.copy().move_to(P3(0.19, 0.26))
    return VGroup(arco, perna_e, perna_d, ponta_e, ponta_d).set_z_index(6)


def mola(a, b, n=9, amp=0.14, cor=GEO, w=3):
    """Mola em zigue-zague entre a e b (horizontal)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    pts = [a]
    for i in range(1, 2 * n):
        u = i / (2 * n)
        pts.append(a + (b - a) * u + P3(0, amp * (1 if i % 2 else -1)))
    pts.append(b)
    return VMobject().set_points_as_corners(pts).set_stroke(cor, w).set_z_index(4)


def flash(centro, r=0.12, cor=WHITE_):
    g = VGroup(Circle(radius=r).set_stroke(cor, 3).move_to(centro))
    for k in range(8):
        a = k * PI / 4
        g.add(Line(centro + (r + 0.04) * P3(math.cos(a), math.sin(a)), centro + (r + 0.22) * P3(math.cos(a), math.sin(a))).set_stroke(cor, 3))
    return g


_CM_MOLDE = {}


def marcador_cm(centro=ORIGIN, r=0.215, z=30, op=1.0, leve=False):
    """⊕ do centro de massa (cópia de um molde: barato dentro de always_redraw). `leve`: só anel e cruz (fotos fantasma)."""
    if (r, leve) not in _CM_MOLDE:
        m0 = _marcador_cm(ORIGIN, r, z)
        if leve:
            m0.remove(*m0.submobjects[:3])
        _CM_MOLDE[(r, leve)] = m0
    m = _CM_MOLDE[(r, leve)].copy().shift(np.asarray(centro, dtype=float))
    if op < 0.999:
        escala_op(m, op)
    return m


def vivo(func):
    """Como always_redraw, mas troca os submobjects a cada quadro em vez de `become` (que alinha pontos e custava ~0,4 s por quadro
    nas camadas sobre o 3D)."""
    g = VGroup()

    def upd(m):
        novo = func()
        # o Cairo guarda, no início de cada play, a lista dos membros que se movem: a camada antiga continuaria sendo
        # desenhada até o fim do play (rastro duplicado). Por isso ela fica invisível antes de sair.
        for velho in m.submobjects:
            for x in velho.family_members_with_points():
                if isinstance(x, VMobject):
                    x.set_stroke(opacity=0, family=False)
                    x.set_fill(opacity=0, family=False)
        m.submobjects = [novo]
        m.z_index = novo.z_index
    g.add_updater(upd)
    upd(g)
    return g


def seta(a, b, color=WHITE_, width=5, tip=0.2, op=1.0, z=8):
    """Seta leve (linha + ponta triangular) para camadas redesenhadas a cada quadro; a `arrow()` do kit custa ~15 ms."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    L = np.linalg.norm(b - a)
    if L < 0.03:
        return VMobject()
    u = (b - a) / L
    n = np.array([-u[1], u[0], 0.0])
    tl = min(tip, 0.45 * L)
    base = b - u * tl * 0.92
    corpo = VMobject().set_points_as_corners([a, base]).set_stroke(color, width, opacity=op)
    ponta = VMobject().set_points_as_corners([b, b - u * tl + n * tl * 0.55, b - u * tl - n * tl * 0.55, b])         .set_stroke(color, 1, opacity=op).set_fill(color, op)
    return VGroup(corpo, ponta).set_z_index(z)


def grad_cm(u):
    """Cor do degradê do ⊕ em u (0 = ciano, 1 = magenta)."""
    return interpolate_color(ManimColor(CM_A), ManimColor(CM_B), min(1.0, max(0.0, u)))


def _marcador_cm(centro=ORIGIN, r=0.215, z=30, op=1.0):
    """⊕ do centro de massa (v3): glow suave e halo em degradê ciano → magenta (~35%), anel em degradê angular (36 arcos, ciano em cima à
    esquerda, magenta embaixo à direita), cruz branca fina; contorno escuro fino sob o anel e a cruz para ler sobre qualquer fundo.
    Exclusivo do CM (G15)."""
    c = np.asarray(centro, dtype=float)
    esc = BACKGROUND_COLOR
    g = VGroup()
    for rr, o in ((r * 2.25, 0.07), (r * 1.75, 0.13)):                             # glow
        g.add(Circle(radius=rr).set_stroke(width=0).set_fill([CM_A, CM_B], o * op).move_to(c))
    g.add(Circle(radius=r * 1.32).set_stroke(width=0).set_fill([CM_A, CM_B], 0.35 * op).move_to(c))      # halo
    g.add(Circle(radius=r).set_stroke(esc, 6.5, opacity=0.6 * op).move_to(c))
    n, a0 = 36, 0.75 * PI
    for i in range(n):
        th = 2 * PI * i / n
        g.add(Arc(radius=r, start_angle=th, angle=2 * PI / n + 0.02, arc_center=c).set_stroke(grad_cm((1 - math.cos(th - a0)) / 2), 3.4, opacity=op))
    k = 1.22
    cruz = lambda: VGroup(Line(c + r * k * LEFT, c + r * k * RIGHT), Line(c + r * k * DOWN, c + r * k * UP))
    g.add(cruz().set_stroke(esc, 5.0, opacity=0.6 * op), cruz().set_stroke(CM_COL, 2.0, opacity=op))
    g._degrade = "cm"
    return g.set_z_index(z)


def rastro_cm(pts, w=5, op=1.0, n=18):
    """Rastro do ⊕ (v3): degradê ao longo do comprimento (ciano no começo → magenta na ponta), espessura `w`, com glow."""
    pts = np.asarray(pts, dtype=float)
    if len(pts) < 2 or op < 0.01:
        return VGroup()
    L, glow, nucleo = len(pts), VGroup(), VGroup()
    n = max(1, min(n, L - 1))
    for i in range(n):
        a, b = int(i * (L - 1) / n), int((i + 1) * (L - 1) / n)
        seg = pts[a:b + 1]
        if len(seg) < 2:
            continue
        cor = grad_cm(i / max(1, n - 1))
        glow.add(VMobject().set_points_as_corners(seg).set_stroke(cor, w * 2.8, opacity=0.16 * op))
        nucleo.add(VMobject().set_points_as_corners(seg).set_stroke(cor, w, opacity=op))
    g = VGroup(glow, nucleo)
    g._degrade = "rastro"
    return g


def esfera_aco(r=0.3, z=5):
    """Esfera 2D de aço com a luz B (v4 §3.2): gradiente radial #9AA6B8 → #7A8696 → #3A4252 (centro claro deslocado para o alto à
    esquerda), especular branco a 70% no alto à esquerda, recorte #7FB2FF a 35% na borda de baixo à esquerda e toque #EA63FF a 12% na
    borda de cima à direita. Uma função só para todos os corpos 2D (haltere, molas, massas do plano, blocos)."""
    g = VGroup()
    c0, c1, c2 = ManimColor("#3A4252"), ManimColor("#7A8696"), ManimColor("#9AA6B8")
    n = 16
    for k in range(n):
        u = k / (n - 1)
        cc = interpolate_color(c0, c1, u / 0.5) if u < 0.5 else interpolate_color(c1, c2, (u - 0.5) / 0.5)
        g.add(Circle(radius=r * (1 - 0.8 * u)).set_stroke(width=0).set_fill(cc, 1).move_to(P3(-0.3 * r * u, 0.32 * r * u)))
    wr = max(2.0, 13 * r)
    g.add(Arc(radius=r * (1 - 0.006 * wr), start_angle=1.05 * PI, angle=0.62 * PI).set_stroke("#7FB2FF", wr, opacity=0.35))   # recorte
    g.add(Arc(radius=r * (1 - 0.005 * wr), start_angle=0.08 * PI, angle=0.36 * PI).set_stroke(MAG, wr * 0.8, opacity=0.12))   # toque
    g.add(Ellipse(width=0.46 * r, height=0.3 * r).set_stroke(width=0).set_fill(WHITE_, 0.7).rotate(0.6).move_to(P3(-0.4 * r, 0.44 * r)))
    g.add(Circle(radius=r).set_stroke("#5A6476", 1.4, opacity=0.9))
    for m in g:
        m._degrade = "aco"
    return g.set_z_index(z)


def bloco_aco(w, h, z=5):
    """Bloco 2D de aço com a luz B (mesma lógica da esfera_aco): gradiente vertical claro em cima → escuro embaixo, recorte #7FB2FF na
    borda de baixo à esquerda, toque #EA63FF na de cima à direita, filete interno."""
    f = RoundedRectangle(corner_radius=0.05, width=w, height=h).set_fill(["#9AA6B8", "#7A8696", "#3A4252"], 1).set_sheen_direction(UP) \
        .set_stroke("#5A6476", 1.4)
    f._degrade = "aco"
    rec = VMobject().set_points_as_corners([P3(-w / 2 + 0.04, h / 2 - 0.1), P3(-w / 2 + 0.04, -h / 2 + 0.04), P3(w / 2 - 0.12, -h / 2 + 0.04)]) \
        .set_stroke("#7FB2FF", 3.2, opacity=0.5)
    toq = VMobject().set_points_as_corners([P3(-w / 2 + 0.12, h / 2 - 0.04), P3(w / 2 - 0.04, h / 2 - 0.04), P3(w / 2 - 0.04, -h / 2 + 0.12)]) \
        .set_stroke(MAG, 2.6, opacity=0.18)
    fil = RoundedRectangle(corner_radius=0.04, width=max(w - 0.14, 0.05), height=max(h - 0.14, 0.05)).set_stroke(WHITE_, 1, opacity=0.25)
    g = VGroup(f, rec, toq, fil).set_z_index(z)
    g.front = f
    return g


def cadeado(aberto=False, s=1.0, cor=STEEL):
    """Cadeado de aço (corpo + alça); aberto: a alça sobe e gira."""
    corpo = bloco_aco(0.5 * s, 0.42 * s)
    alca = Arc(radius=0.16 * s, start_angle=0, angle=PI).set_stroke("#9AA6B8", 5 * s).move_to(corpo.get_top() + 0.14 * s * UP)
    if aberto:
        alca.rotate(0.6, about_point=alca.get_left() + 0.0 * UP).shift(0.12 * s * UP)
    furo = Dot(corpo.get_center() + 0.02 * s * UP, radius=0.045 * s, color="#2A303A")
    return VGroup(alca, corpo, furo).set_z_index(9)


def esfera2d(r=0.3, cor=STEEL, z=5):
    """Compatibilidade: toda bola 2D é a esfera de aço com a luz B."""
    return esfera_aco(r, z)


def da_borda(c, d, r):
    """Ponto na borda de um círculo de centro c e raio r (Manim) na direção d: as setas saem da borda, nunca do centro."""
    c, d = np.asarray(c, float), np.asarray(d, float)
    n = np.linalg.norm(d)
    return c if n < 1e-9 else c + d / n * r


def lugar_livre(mob, cands, circ=(), pts=(), mem=None, chave=None, folga=0.3):
    """Centro, entre os candidatos (em ordem de preferência), em que a caixa de mob fica a pelo menos `folga` dos círculos (centro, raio),
    dos pontos e da margem; com `mem`, mantém o candidato anterior enquanto ele seguir livre (o rótulo não pula de quadro em quadro)."""
    w, h = mob.width / 2, mob.height / 2
    P_ = np.asarray(pts, float).reshape(-1, 3)

    def livre(c):
        f = min(7.55 - abs(c[0]) - w, 4.05 + c[1] - h, 3.3 - c[1] - h)                 # em cima, abaixo do título do canto
        for o, r in circ:
            f = min(f, np.hypot(max(abs(o[0] - c[0]) - w, 0), max(abs(o[1] - c[1]) - h, 0)) - r)
        if len(P_):
            f = min(f, np.hypot(np.maximum(np.abs(P_[:, 0] - c[0]) - w, 0), np.maximum(np.abs(P_[:, 1] - c[1]) - h, 0)).min())
        return f
    fs = [livre(c) for c in cands]
    i = mem.get(chave) if mem is not None else None
    if i is not None and fs[i] >= folga:
        melhor = [k for k in range(i) if fs[k] >= folga + 0.25]           # volta a um lugar preferido quando ele fica bem livre
        i = melhor[0] if melhor else i
    else:
        ok = [k for k, f in enumerate(fs) if f >= folga]
        i = ok[0] if ok else int(np.argmax(fs))
    if mem is not None:
        mem[chave] = i
    return cands[i]


def onda(c, r=0.24):
    """Pulso em anel saindo de um ponto (o ⊕): mostra o lugar sem mexer na física."""
    return FadeOut(Circle(radius=r).move_to(c).set_stroke(WHITE_, 3), scale=2.4)


def amostra(a, b, n=12):
    return [a + (b - a) * u for u in np.linspace(0, 1, n)]


def suave(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


# ── gráficos ─────────────────────────────────────────────────────────────────────────────────────────────
class Graf:
    """Eixos com mapeamento (t, y) → tela; o eixo t passa por y = 0, que fica em `y0`. ymin < 0 permitido."""

    def __init__(self, x0, y0, w, tmax, ymin, ymax, hpu, rot_y=None, rot_x=r"t", z=2, cor=DIM):
        self.x0, self.y0, self.w, self.tmax, self.hpu = x0, y0, w, tmax, hpu
        eixo_x = Arrow(P3(x0 - 0.1, y0), P3(x0 + w + 0.25, y0), buff=0, color=cor, stroke_width=3, tip_length=0.15)
        eixo_y = Line(P3(x0, y0 + ymin * hpu - 0.1), P3(x0, y0 + ymax * hpu + 0.12)).set_stroke(cor, 3)
        self.ey = rot_y.next_to(P3(x0, y0 + ymax * hpu + 0.12), UP, buff=0.06) if rot_y is not None else VGroup()
        self.ex = MathTex(rot_x, font_size=30, color=cor).next_to(P3(x0 + w + 0.28, y0), RIGHT, buff=0.06)
        self.eixos = VGroup(eixo_x, eixo_y, self.ex, self.ey).set_z_index(z)

    def pt(self, t, y):
        return P3(self.x0 + self.w * t / self.tmax, self.y0 + self.hpu * y)

    def curva(self, fun, t0=0.0, t1=None, n=200, cor=MAG, w=5):
        t1 = self.tmax if t1 is None else t1
        if t1 - t0 < 1e-4:
            return VMobject()
        ts = np.linspace(t0, t1, n)
        return VMobject().set_points_as_corners([self.pt(t, fun(t)) for t in ts]).set_stroke(cor, w).set_z_index(6)


# ── grade de layout (handoff v2 §2, em unidades do quadro 16 × 9) ─────────────────────────────────────────
PALCO_X, PALCO_Y = (-7.4, 0.7), (-3.4, 2.8)
CONTA_X, CONTA_Y = (1.1, 7.4), (-3.4, 2.8)
PALCO_C = P3(-3.35, -0.3)
CONTA_C = P3(4.25, -0.3)
XC0 = 1.35                    # borda esquerda da CONTA (alinhamento à esquerda)
Y_LEG = -3.82                 # LEGENDA


def na_conta(m, y, x0=XC0):
    """Alinha à esquerda na CONTA, na altura y."""
    return m.move_to(P3(x0 + m.width / 2, y))


# ── 3D por estado (Three.js): a passagem seca grava pedidos, o r3d.js renderiza, a passagem final cola o PNG ───────
PEDIDOS3D = os.environ.get("PEDIDOS3D") == "1"
DIR3D = AQUI / "threejs"


def manim_de_px(px, py, w, h):
    return P3(px / w * 16 - 8, 4.5 - py / h * 9)


class Fundo3D(Group):
    """Fundo 3D do quadro inteiro. `estado(t)` devolve o dict de estado da cena 3D no tempo t da cena Manim.
    `self.op` (ValueTracker) é a opacidade (recuo do PALCO). `self.e` guarda o estado do quadro corrente."""

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
        self.mult = None             # multiplicador de opacidade em função do tempo (ex.: troca de tomada)
        self.e = estado(0.0)
        cena_m._ped.setdefault(cena3d, {})
        self.add_updater(lambda m: m._quadro())
        self._quadro()

    def __deepcopy__(self, memo):
        """Cópia estática (o fundo guarda a cena; Transform/FadeOut precisam copiar)."""
        g = Group(ImageMobject(self.img.pixel_array.copy()).set_width(16).move_to(ORIGIN))
        for m in self.submobjects[1:]:
            g.add(m.copy())
        return g.set_z_index(-20)

    def _quadro(self):
        f = int(round(self.cm.clk.get_value() * FPS))
        e = self.fn(f / FPS)
        self.e = e
        if PEDIDOS3D:
            self.cm._ped[self.cena][f] = e
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
        o = self.op.get_value() * (self.mult(f / FPS) if self.mult else 1.0)
        self.img.pixel_array[..., 3] = (self.alfa * max(0.0, min(1.0, o)) + 0.5).astype(np.uint8)
        return self


def r4(d):
    """Arredonda floats de um estado (dedupe de quadros iguais no r3d.js)."""
    if isinstance(d, dict):
        return {k: r4(v) for k, v in d.items()}
    if isinstance(d, (list, tuple)):
        return [r4(v) for v in d]
    if isinstance(d, float):
        return round(d, 4)
    return d


def cam_frente(K=1.0, xc=0.0, yc=-2.0, camx=0.0, fov=16, el=3):
    return {"modo": "frente", "K": K, "xc": xc, "yc": yc, "camx": camx, "fov": fov, "el": el}


def mapa_frente(cam, x, z, y=0.0):
    """Ponto 3D (x, y, z) → Manim na vista 'frente' (perspectiva aproximada pela profundidade y)."""
    K = cam["K"]
    D = (9 / K / 2) / math.tan(math.radians(cam["fov"]) / 2)
    s = D / (D + y)
    return P3(cam["xc"] + K * s * (x - cam["camx"]), cam["yc"] + K * s * z)


def cam_topo(K=1.0, xc=0.0, yc=0.0, camx=0.0, camy=0.0, fov=16):
    return {"modo": "topo", "K": K, "xc": xc, "yc": yc, "camx": camx, "camy": camy, "fov": fov}


def cam_obl(az, el, alvo, K=1.0, xc=0.0, yc=0.0, fov=16):
    return {"modo": "obl", "az": az, "el": el, "alvo": list(alvo), "K": K, "xc": xc, "yc": yc, "fov": fov}


_BASES = {}


def _base_cam(cam):
    """Base da câmera (posição, eixos, escalas) do b3d.js, em cache por câmera: a projeção vira só produtos escalares."""
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
    """Ponto 3D → Manim pela mesma câmera do b3d.js (posicionaCamera + setViewOffset), em qualquer modo. Perspectiva exata."""
    pos, B, sx, sy, xc, yc = _base_cam(cam)
    x, y, z = B @ (np.asarray(p, dtype=float) - pos)
    return np.array([xc + sx * x / z, yc + sy * y / z, 0.0])


def projeta3d_n(cam, pts):
    """Vários pontos 3D (N×3) → Manim (N×3) de uma vez."""
    pos, B, sx, sy, xc, yc = _base_cam(cam)
    q = (np.asarray(pts, dtype=float) - pos) @ B.T
    out = np.zeros((len(q), 3))
    out[:, 0] = xc + sx * q[:, 0] / q[:, 2]
    out[:, 1] = yc + sy * q[:, 1] / q[:, 2]
    return out


def escala_op(m, o):
    """Multiplica as opacidades de fill e stroke de toda a família (preserva traços sem preenchimento)."""
    for x in m.family_members_with_points():
        if isinstance(x, VMobject):
            x.set_fill(opacity=x.get_fill_opacity() * o, family=False)
            x.set_stroke(opacity=x.get_stroke_opacity() * o, family=False)
    return m


class OpVivo(Animation):
    """Fade de um mobject vivo (always_redraw): ele continua se redesenhando e só a opacidade anima."""

    def __init__(self, m, entra=True, **kw):
        super().__init__(m, suspend_mobject_updating=False, remover=not entra, introducer=entra, **kw)
        self.entra = entra

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        self.mobject.update(0)
        o = a if self.entra else 1 - a
        if o < 0.999:
            escala_op(self.mobject, o)


def _vivo(a):
    if isinstance(a, (FadeIn, FadeOut)) and isinstance(a.mobject, Fundo3D):
        return a.mobject.op.animate(run_time=a.run_time).set_value(1.0 if isinstance(a, FadeIn) else 0.0).build()             if hasattr(a.mobject.op.animate, "build") else a
    if isinstance(a, (FadeIn, FadeOut)) and a.mobject.get_updaters():
        return OpVivo(a.mobject, entra=isinstance(a, FadeIn), run_time=a.run_time)
    return a


# ── cena-base: relógio por quadro, âncoras, cabeçalho ──────────────────────────────────────────────────────
class Base(Scene):
    """Todo `play` é quantizado em quadros inteiros e arrasta o relógio `self.clk` (segundos da cena), de modo que
    updaters baseados em `self.clk` ficam exatos quadro a quadro e o número de quadros é determinístico."""
    TITULO = "MECÂNICA · CENTRO DE MASSA"
    FUNDO = "fundo_lab.png"           # v4 §2: o céu do laboratório em toda cena (fundo.py); exercícios: fundo_lab_ex.png

    def setup_base(self, cap=None, selo=None):
        self.camera.background_color = "#08122B"
        self.fundo = ImageMobject(str(AQUI / self.FUNDO)).set_width(16).move_to(ORIGIN).set_z_index(-100)
        self.add(self.fundo)
        self.clk = ValueTracker(0.0)
        self.nq = 0
        self.lote = type(self).__name__
        self._ped = {}
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3).set_z_index(40)
        self.h1 = txt(self.TITULO, 17, color=DIM, op=0.5).to_corner(UL, buff=0.32).set_z_index(40)
        self.h2 = self._sl = None
        self._pend = []
        self.add(self.wm, self.h1)
        self.alvo = 0.0
        self.log = []
        self.dica_atual = None
        self._aid, self._q0 = None, 0
        if cap:
            self.h2 = txt(cap, 30, op=0.95).next_to(self.h1, DOWN, buff=0.14, aligned_edge=LEFT).set_z_index(40)
            self.add(self.h2)
            if selo:   # selo de ligação com a teoria (v2: sem referência de livro na tela)
                self._sl = txt(selo, 20, color=DIM, op=0.85).next_to(self.h2, DOWN, buff=0.12, aligned_edge=LEFT).set_z_index(40)
                self.add(self._sl)

    # tempo ---------------------------------------------------------------------------------------------------
    @property
    def t(self):
        return self.nq / FPS

    def play(self, *anims, run_time=None, **kw):
        if self._pend:
            anims, self._pend = (*anims, *self._pend), []
        anims = tuple(_vivo(a) for a in anims)
        self._still()
        rt = run_time
        if rt is None:
            rt = max([getattr(a, "run_time", 1.0) for a in anims] or [1.0])
        n = max(1, round(rt * FPS))
        rtq = n / FPS - FRAC
        t0 = self.nq / FPS
        clk = UpdateFromAlphaFunc(self.clk, lambda m, a: m.set_value(t0 + a * n / FPS), rate_func=linear, run_time=rtq)
        if AUDITORIA:
            self._auditar()
        super().play(*anims, clk, run_time=rtq, **kw)
        self.nq += n

    def _still(self):
        if STILL is not None and self.nq / FPS >= STILL:
            from manim.utils.exceptions import EndSceneEarlyException
            raise EndSceneEarlyException()

    def wait(self, duration=1.0, *a, **kw):
        self._still()
        if AUDITORIA:
            self._auditar()
        n = max(1, round(duration * FPS))
        rtq = n / FPS - FRAC
        t0 = self.nq / FPS
        super().play(UpdateFromAlphaFunc(self.clk, lambda m, a_: m.set_value(t0 + a_ * n / FPS), rate_func=linear,
                                         run_time=rtq), run_time=rtq)
        self.nq += n

    def ate(self, frac):
        """Espera até a fração `frac` (0–1) da âncora corrente."""
        alvo = self._q0 + frac * (self.alvo - self._q0)
        if alvo - self.nq >= 1:
            self.wait((alvo - self.nq) / FPS)

    def resta(self):
        """Segundos que faltam para o fim da âncora corrente."""
        return max(0.0, (self.alvo - self.nq) / FPS)

    def an(self, aid):
        """Fecha a âncora anterior (espera o resto da fala) e abre `aid`."""
        self._fecha()
        self._aid, self._q0 = aid, self.nq
        self.alvo = self.nq + dur(aid) * FPS

    def _fecha(self):
        if self._aid is not None:
            if self.alvo - self.nq >= 1:
                self.wait((self.alvo - self.nq) / FPS)
            self.log.append((self._aid, self._q0 / FPS, dur(self._aid), (self.nq - self._q0) / FPS))
            self._aid = None

    def fim(self):
        self._fecha()
        self.log.append(("FIM", self.nq / FPS, 0, 0))

    # cabeçalho -------------------------------------------------------------------------------------------------
    def fixos(self):
        return {self.fundo, self.wm, self.h1, *([self.h2] if self.h2 else []), *([self._sl] if getattr(self, '_sl', None) else [])}

    def secao(self, s, selo=None):
        """Linha 2 do header (e selo da fonte, linha 3): o antigo sai (0,25 s) antes de o novo entrar."""
        velhos = [m for m in (self.h2, getattr(self, "_sl", None)) if m is not None]
        if velhos:
            self.play(*[FadeOut(m) for m in velhos], run_time=0.25)
        self.h2 = self._sl = None
        if not s:
            return
        novo = txt(s, 30, op=0.95).next_to(self.h1, DOWN, buff=0.14, aligned_edge=LEFT).set_z_index(40)
        self.h2 = novo
        self._pend.append(FadeIn(novo))
        if selo:
            self._sl = txt(selo, 20, color=DIM, op=0.85).next_to(novo, DOWN, buff=0.12, aligned_edge=LEFT).set_z_index(40)
            self._pend.append(FadeIn(self._sl))

    def clear(self, *keep, rt=0.6):
        keep = self.fixos() | set(keep)
        mobs = [m for m in self.mobjects if m not in keep and m is not self.clk]
        vis = [m for m in mobs if not isinstance(m, ValueTracker)]          # trackers (estado 3D) só saem, sem animar
        if vis:
            self.play(*[m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in vis], run_time=rt)
        for m in mobs:
            m.clear_updaters()
        self.remove(*mobs)
        self.dica_atual = None

    def snap(self):
        """O que está em cena agora (fora o cabeçalho): use antes de montar a cena nova, e passe para troca()."""
        keep = self.fixos()
        return [m for m in self.mobjects if m not in keep and m is not self.clk]

    def troca(self, velhos, *entram, rt=0.5, seq=False):
        """Troca de cena. Crossfade (G5) entre cenas leves; com `seq` (G13, entre duas cenas cheias) a velha sai em 0,35 s e só então a
        nova entra em 0,35 s, sem as duas a meia opacidade uma sobre a outra."""
        vis = [m for m in velhos if not isinstance(m, ValueTracker)]
        sai = [m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in vis]
        if seq:
            self.play(*sai, run_time=0.35)
            for m in velhos:
                m.clear_updaters()
            self.remove(*velhos)
            self._em_troca = True
            self.play(*entram, run_time=0.35)
            self._em_troca = False
            return
        self.play(*sai, *entram, run_time=rt)
        for m in velhos:
            m.clear_updaters()
        self.remove(*velhos)
        if self.dica_atual in velhos:
            self.dica_atual = None

    def logo(self, largura):
        img = ImageMobject(str(ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"))
        arr = img.get_pixel_array()
        ys, xs = np.nonzero(arr[:, :, 3] > 8)
        return ImageMobject(arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).set_width(largura)

    def hl(self, s, y=3.0, size=T_HL, color=WHITE_, x=0.0, bold=True):
        return txt(s, size, color=color, bold=bold).move_to(P3(x, y))

    def dica_entra(self, d, apagar=True):
        """DICA entra; as equações soltas em cena vão a 60% (G7: uma frase na tela por vez)."""
        self.dica_atual = d
        (a0, b0), (a1, b1) = d.get_corner(DL)[:2] - 0.1, d.get_corner(UR)[:2] + 0.1
        cobre = lambda m: m.get_left()[0] < a1 and m.get_right()[0] > a0 and m.get_bottom()[1] < b1 and m.get_top()[1] > b0
        self._cobertos = [m for m in self.mobjects if m not in self.fixos() and (hasattr(m, "_tam") or isinstance(m, MathTex)) and cobre(m)]   # a DICA nunca cobre texto
        self._apagadas = [m for m in self.mobjects if isinstance(m, MathTex) and m not in self.fixos() and m not in self._cobertos] if apagar else []
        self.play(FadeIn(d, shift=0.15 * UP), *[m.animate.set_opacity(OP_FUNDO) for m in self._apagadas], *[FadeOut(m) for m in self._cobertos], run_time=0.6)

    def dica_sai(self):
        if self.dica_atual is not None:
            self.play(FadeOut(self.dica_atual), *[m.animate.set_opacity(1.0) for m in getattr(self, "_apagadas", []) if m in self.mobjects],
                      *[FadeIn(m) for m in getattr(self, "_cobertos", [])], run_time=0.4)
            self.remove(self.dica_atual)
            self.dica_atual = None
            self._apagadas = []

    # auditoria de sobreposições (AUDITORIA=1) ---------------------------------------------------------------
    def _auditar(self):
        self.update_mobjects(0)
        itens = []

        def op(m):
            vals = []
            for x in m.family_members_with_points():
                try:
                    vals.append(max(x.get_fill_opacity(), x.get_stroke_opacity()))
                except Exception:
                    vals.append(1.0)
            return max(vals) if vals else 0.0

        tams = {}

        def walk(m, tam=None, fixo=False):
            if isinstance(m, ImageMobject):
                return
            tam = getattr(m, "_tam", tam)
            if isinstance(m, (Text, SingleStringMathTex)):
                if op(m) > 0.08 and m.width > 0.01:
                    itens.append(m)
                    tams[id(m)] = (tam, fixo)
                return
            for s in m.submobjects:
                walk(s, tam, fixo)

        fx = self.fixos()
        for top in self.mobjects:
            walk(top, fixo=top in fx)

        def bb(m):
            (x0, y0, _), (x1, y1, _) = m.get_critical_point(DL), m.get_critical_point(UR)
            return x0 + 0.03, y0 + 0.03, x1 - 0.03, y1 - 0.03

        def nome(m):
            return f"'{m.text[:30]}'" if isinstance(m, Text) else f"'{m.get_tex_string()[:30]}'"

        t = self.nq / FPS
        # PALCO: algum desenho (não texto) visível fora do cabeçalho/DICA, ou um fundo 3D com opacidade
        fixos = self.fixos() | ({self.dica_atual} if self.dica_atual is not None else set())
        graf = [0]

        def tem_desenho(m):
            if isinstance(m, Fundo3D):
                if m.op.get_value() > 0.15:
                    graf[0] += 1
                return
            if isinstance(m, (Text, SingleStringMathTex, MathTex)) or isinstance(m, ImageMobject):
                return
            if m.points.size and op(m) > 0.15 and m.width + m.height > 0.4:
                graf[0] += 1
                return
            for s in m.submobjects:
                tem_desenho(s)

        for top in self.mobjects:
            if top not in fixos and top is not self.clk:
                tem_desenho(top)
        if graf[0] == 0 and not getattr(self, "_em_troca", False):
            print(f"[audit] {t:7.1f}s SEM PALCO")
        # G15: degradê só no ⊕ (e no rastro dele, e no sombreado de aço dos corpos); qualquer outro gradiente é erro
        tags = getattr(self, "_tags_degrade", None)
        if tags is None:
            tags = self._tags_degrade = {}

        def degr(m, tag=None):
            tag = getattr(m, "_degrade", tag)
            if isinstance(m, VMobject) and m.points.size and op(m) > 0.05:
                multi = any(len(np.unique(np.round(c_, 3), axis=0)) > 1 for c_ in (m.get_fill_rgbas(), m.get_stroke_rgbas()))   # cores distintas
                if tag:
                    tags[tag] = tags.get(tag, 0) + 1
                elif multi:
                    print(f"[audit] {t:7.1f}s DEGRADÊ FORA DO ⊕ {type(m).__name__} em ({m.get_x():.1f}; {m.get_y():.1f})")
            if tag and tag != "cm" and tag != "rastro" and tag != "aco":
                print(f"[audit] {t:7.1f}s DEGRADÊ FORA DO ⊕ marcado '{tag}'")
            for s_ in m.submobjects:
                degr(s_, tag)
        for top in self.mobjects:
            if top not in self.fixos() and top is not self.clk and not isinstance(top, Fundo3D):
                degr(top)
        # G12: cor por token, uma vez por MathTex
        vistos = getattr(self, "_cor_vistos", None)
        if vistos is None:
            vistos = self._cor_vistos = {}
            self._cor_n = [0, 0]

        def cores_tex(m):
            if isinstance(m, MathTex) and hasattr(m, "_partes") and id(m) not in vistos and op(m) > 0.3:
                vistos[id(m)] = True
                for tx, c in m._partes:
                    e_ = cor_esperada(tx)
                    if e_ is None:
                        continue
                    self._cor_n[0] += 1
                    if ManimColor(c).to_hex().upper() != ManimColor(e_).to_hex().upper():
                        self._cor_n[1] += 1
                        print(f"[audit] {t:7.1f}s COR POR TOKEN '{tx}' em {ManimColor(c).to_hex()} (esperado {ManimColor(e_).to_hex()})")
            elif isinstance(m, MathTex) and not hasattr(m, "_partes") and id(m) not in vistos and op(m) > 0.3:
                vistos[id(m)] = True
                print(f"[cor] {t:7.1f}s sem partes registradas: '{m.get_tex_string()[:40]}'")
            for s_ in m.submobjects:
                cores_tex(s_)
        for top in self.mobjects:
            if top not in self.fixos():
                cores_tex(top)
        # objetos (setas, bolas, corpos, molas, trajetórias): pontos de cada folha VMobject com desenho, fora do cabeçalho/DICA/caixas
        objs = []

        def folhas(m):
            if isinstance(m, (Text, SingleStringMathTex, ImageMobject, Fundo3D)) or getattr(m, "_fundo", False) or getattr(m, "_risco", False):
                return
            if isinstance(m, VMobject) and m.points.size and not m.submobjects:
                if op(m) > 0.15:
                    objs.append(m)
                return
            for s_ in m.submobjects:
                folhas(s_)
        for top in self.mobjects:
            if top not in fixos and top is not self.clk:
                folhas(top)
        cache_d = {}

        def densos(o):                                       # retas longas: pontos a cada ~0,08 ao longo das cordas (só as âncoras deixam a reta passar pelo texto)
            if id(o) not in cache_d:
                p_ = o.points
                a0, a1 = p_[0::4], p_[3::4]
                k_ = min(len(a0), len(a1))
                a0, a1 = a0[:k_], a1[:k_]
                L = np.linalg.norm(a1 - a0, axis=1)
                n_ = int(min(40, max(2, np.ceil(L.max() / 0.08)))) if k_ else 2
                u_ = np.linspace(0, 1, n_)[None, :, None]
                cache_d[id(o)] = np.vstack([p_, (a0[:, None] + (a1 - a0)[:, None] * u_).reshape(-1, 3)]) if k_ else p_
            return cache_d[id(o)]
        for o in objs:
            pts = o.points
            if (np.abs(pts[:, 0]) > 7.55).any() or (np.abs(pts[:, 1]) > 4.05).any():
                print(f"[audit] {t:7.1f}s OBJETO FORA DA MARGEM {type(o).__name__} em ({o.get_x():.1f}; {o.get_y():.1f})")
        circ = []
        for fn in getattr(self, "_corpos3d", []):
            try:
                circ += list(fn())
            except Exception:
                pass
        circ = [(q[0], q[1], len(q) > 2 and q[2]) for q in circ]           # (centro, raio, futuro?)
        for c_, r_, fut in circ:
            if not fut and (abs(c_[0]) + r_ > 7.55 or abs(c_[1]) + r_ > 4.05):
                print(f"[audit] {t:7.1f}s OBJETO FORA DA MARGEM corpo 3D em ({c_[0]:.1f}; {c_[1]:.1f})")
        for a in itens:
            tam, fixo = tams.get(id(a), (None, False))
            if fixo or (self.dica_atual is not None and a in self.dica_atual.get_family()):
                continue
            x0, y0, x1, y1 = bb(a)
            x0, y0, x1, y1 = x0 - 0.05, y0 - 0.05, x1 + 0.05, y1 + 0.05
            fam = set(id(q) for q in a.get_family())
            for o in objs:
                if id(o) in fam:
                    continue
                pts = densos(o)
                dentro = (pts[:, 0] > x0) & (pts[:, 0] < x1) & (pts[:, 1] > y0) & (pts[:, 1] < y1)
                if dentro.any():
                    print(f"[audit] {t:7.1f}s TEXTO SOBRE OBJETO {nome(a)} x {type(o).__name__} em ({o.get_x():.1f}; {o.get_y():.1f})")
                    break
            for c_, r_, _ in circ:
                dx = max(x0 - c_[0], 0, c_[0] - x1)
                dy = max(y0 - c_[1], 0, c_[1] - y1)
                if math.hypot(dx, dy) < r_ + 0.03:
                    print(f"[audit] {t:7.1f}s TEXTO SOBRE OBJETO {nome(a)} x corpo 3D em ({c_[0]:.1f}; {c_[1]:.1f})")
                    break
        caixas = [m for top in self.mobjects for m in top.get_family() if getattr(m, "_caixa", False) and op(m) > 0.3]
        for c_ in caixas:                                    # caixa (isenta como fundo) cortando texto que não está dentro dela
            cx0, cy0, cx1, cy1 = bb(c_)
            for a in itens:                                  # glifo a glifo: parte da equação pode estar na caixa, o vizinho não pode encostar
                for gl in a.family_members_with_points():
                    (x0, y0, _), (x1, y1, _) = gl.get_critical_point(DL), gl.get_critical_point(UR)    # contorno real, sem o recuo de bb()
                    cruza = min(x1, cx1 + 0.07) - max(x0, cx0 - 0.07) > 0 and min(y1, cy1 + 0.07) - max(y0, cy0 - 0.07) > 0   # folga mínima 0,04
                    dentro = x0 >= cx0 - 0.01 and x1 <= cx1 + 0.01 and y0 >= cy0 - 0.01 and y1 <= cy1 + 0.01
                    if cruza and not dentro:
                        print(f"[audit] {t:7.1f}s TEXTO SOBRE CAIXA {nome(a)}")
                        break
        for i, a in enumerate(itens):
            x0, y0, x1, y1 = bb(a)
            tam, fixo = tams.get(id(a), (None, False))
            if not fixo:
                if x0 < -7.55 or x1 > 7.55 or y0 < -4.05 or y1 > 4.05:
                    print(f"[audit] {t:7.1f}s FORA DA MARGEM {nome(a)}")
                if isinstance(a, Text):
                    if tam is not None and tam < 24:
                        print(f"[audit] {t:7.1f}s TEXTO PEQUENO {nome(a)} ({tam})")
                else:
                    fs = a.font_size
                    na_conta = (x0 + x1) / 2 > 1.1
                    eq = "=" in a.get_tex_string()
                    minimo = (46 if eq else 34) if na_conta else 36
                    if fs < minimo - 0.5:
                        print(f"[audit] {t:7.1f}s TEXTO PEQUENO {nome(a)} ({fs:.0f} < {minimo})")
            for b in itens[i + 1:]:
                if a in b.get_family() or b in a.get_family():
                    continue
                bx0, by0, bx1, by1 = bb(b)
                w, h = min(x1, bx1) - max(x0, bx0), min(y1, by1) - max(y0, by0)
                if w > 0.03 and h > 0.03:
                    print(f"[audit] {t:7.1f}s SOBREPOSICAO {nome(a)} x {nome(b)} ({w:.2f}x{h:.2f})")

    def relatorio(self):
        for aid, t0, prev, real in self.log:
            if aid != "FIM" and real > prev + 0.2:
                print(f"[tempo] {aid}: previsto {prev:.1f} s, real {real:.1f} s (cena mais longa que a fala)")
        for aid, t0, prev, real in self.log:
            print(f"[ancora] {aid} {t0:.2f}")
        if AUDITORIA:
            print(f"[degrade] objetos com degradê por marca: {getattr(self, '_tags_degrade', {})}")
            n_ = getattr(self, "_cor_n", [0, 0])
            print(f"[cor] tokens conferidos: {n_[0]}; fora da tabela: {n_[1]}")
        print(f"[tempo] total {self.nq / FPS:.1f} s ({self.nq} quadros)")
        if PEDIDOS3D and self._ped:
            (DIR3D / "pedidos3d").mkdir(parents=True, exist_ok=True)
            out = {"cenas": {c: [[f, r4(e)] for f, e in sorted(d.items())] for c, d in self._ped.items()}}
            (DIR3D / "pedidos3d" / f"{self.lote}.json").write_text(json.dumps(out), encoding="utf-8")
            print(f"[3d] pedidos: " + ", ".join(f"{c} {len(d)}" for c, d in self._ped.items()))
