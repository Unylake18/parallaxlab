"""yt_0016 — kit comum: paleta, texto, setas, corpos 2D, fronteira, cavalo, pedra, pessoa de perfil, cabeçalho e relógio por quadro.

Copiado/adaptado do kit do yt_0015 (não importa entre unidades). Preview silencioso: o tempo de cada âncora vem de ancoras.json
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
LUZ = "#FFD25A"              # v4: cor nova, só para luz (coda, corpúsculos do E9, fótons da vela)
LUZ_B = "#FFE9A8"            # brilho da luz


def ponto_luz(c, r=0.07, op=1.0):
    """Corpúsculo/fóton: ponto amarelo com brilho (camadas do mais largo e transparente ao mais fino e opaco)."""
    return VGroup(Dot(c, radius=r * 2.4, color=LUZ).set_opacity(0.12 * op), Dot(c, radius=r * 1.6, color=LUZ).set_opacity(0.25 * op),
                  Dot(c, radius=r, color=LUZ_B).set_opacity(op))


def mix(c, w):
    return interpolate_color(ManimColor(c), ManimColor(WHITE_), w).to_hex()


def escuro(c, w):
    return interpolate_color(ManimColor(c), ManimColor(BACKGROUND_COLOR), w).to_hex()


T_HL, T_MAIN, T_LAB, T_SMALL = 44, 34, 26, 22
M_MAIN, M_MID, M_REF, M_LAB = 68, 56, 46, 40
FPS = int(round(config.frame_rate))   # 15 no preview, 30 no render final (o relógio da cena é por quadro)
FRAC = 0.02 / FPS            # folga p/ np.arange não criar um quadro extra

AUDITORIA = os.environ.get("AUDITORIA") == "1"
STILL = float(os.environ["STILL"]) if os.environ.get("STILL") else None   # still num instante (use com -s)

ANC = json.loads((AQUI / "ancoras.json").read_text(encoding="utf-8"))["ancoras"]   # v5: tempos da voz real (gerar_ancoras.py)


def dur(aid):
    return ANC[aid]["dur"]


def _norm(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c) and c.isalnum())


# ── texto e matemática ───────────────────────────────────────────────────────────────────────────────────
def txt(s, size=T_MAIN, color=WHITE_, op=1.0, bold=False):
    """Texto editorial: Space Grotesk em CAIXA ALTA (símbolos matemáticos vão em MathTex, nunca aqui)."""
    s = s.upper()
    if bold:
        return official_text(s, DISPLAY_FONT, BOLD, size, oversample=2, color=color).set_opacity(op)
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(op)


_MEMO = {}


def memo(chave, fazer):
    """Cópia de um mobject criado uma vez só (textos dentro de always_redraw: criar Text a cada quadro é caro)."""
    if chave not in _MEMO:
        _MEMO[chave] = fazer()
    return _MEMO[chave].copy()


def mtxt(s, size=T_MAIN, color=WHITE_, op=1.0, bold=False):
    return memo(("txt", s, size, color, bold), lambda: txt(s, size, color, 1.0, bold)).set_opacity(op)


def mtex(s, cor=WHITE_, size=M_MID):
    return memo(("tex", s, cor, size), lambda: MathTex(s, font_size=size, color=cor))


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
    return m


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


def barra2(w, h, cor, op=0.85):
    """v7 (2D+): barra com cantos arredondados, degradê vertical e brilho no topo (o centro é o do retângulo, como Rectangle)."""
    h = max(h, 0.03)
    r = RoundedRectangle(width=w, height=h, corner_radius=min(0.06, h / 2.2)).set_stroke(mix(cor, 0.3), 1.5)
    r.set_fill(color=[escuro(cor, 0.55), cor], opacity=op).set_sheen_direction(UP)
    g = VGroup(r)
    if h > 0.1:
        g.add(Line(P3(-w / 2 + 0.08, h / 2 - 0.035), P3(w / 2 - 0.08, h / 2 - 0.035)).set_stroke(mix(cor, 0.6), 3, 0.85))
    return g


def placa(w, h, centro, op=0.05, borda=0.24):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h).set_stroke(WHITE_, 1.4, opacity=borda) \
        .set_fill(WHITE_, op).move_to(centro).set_z_index(-2)


def risco(m, cor=APAGADO, w=4):
    """Traço diagonal sobre um mobject (item riscado)."""
    return Line(m.get_corner(DL) + 0.04 * UR, m.get_corner(UR) - 0.04 * UR).set_stroke(cor, w).set_z_index(30)


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


def dica(*linhas, size=22):
    """Cartão PANEL com borda BLUE_L no canto inferior direito: 'DICA' em ciano e a frase em maiúsculas. Cada linha é uma str
    ou uma lista de str/mobjects (símbolos matemáticos entram como MathTex, nunca dentro de txt())."""
    corpo = VGroup()
    for l in linhas:
        corpo.add(txt(l, size) if isinstance(l, str) else linha(*l, buff=0.1, size=size))
    corpo.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    rot = txt("DICA", 17, color=CYAN, bold=True)
    g = VGroup(rot, corpo).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    caixa = RoundedRectangle(corner_radius=0.12, width=g.width + 0.6, height=g.height + 0.44).set_stroke(BLUE_L, 2) \
        .set_fill(PANEL, 0.97).move_to(g)
    return VGroup(caixa, g).set_z_index(35).to_corner(DR, buff=0.32)


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


def fundo_lab_arq(w, h):
    """v7: o fundo espacial (fundo_lab.py) na resolução do render (redução BOX a partir do 1920×1080)."""
    arq = AQUI / "assets_unidade" / f"fundo_lab_{w}x{h}.png"
    if not arq.exists():
        from PIL import Image
        Image.open(AQUI / "assets_unidade" / "fundo_lab.png").convert("RGB").resize((w, h), Image.BOX).save(arq)
    return arq


def fundo_lab(w, h):
    from PIL import Image
    return Image.open(fundo_lab_arq(w, h))


class Fundo3D(Group):
    """Fundo 3D do quadro inteiro. `estado(t)` devolve o dict de estado da cena 3D no tempo t da cena Manim.
    `self.op` (ValueTracker) é a opacidade (recuo do PALCO). `self.e` guarda o estado do quadro corrente."""

    def __init__(self, cena_m, cena3d, estado, op=1.0, faixa=True, inst=None):
        """`inst`: segunda instância da mesma cena 3D (chave "cena@inst", outra pasta de quadros), para crossfade entre tomadas."""
        super().__init__()
        if inst:
            cena3d = f"{cena3d}@{inst}"
        self.cm, self.cena, self.fn = cena_m, cena3d, estado
        self.op = ValueTracker(op)
        self.w, self.h = config.pixel_width, config.pixel_height
        self.dir = DIR3D / "q3d" / f"{cena_m.lote}_{self.w}x{self.h}" / cena3d
        vazio = np.zeros((self.h, self.w, 4), dtype=np.uint8)
        vazio[..., :3] = (5, 8, 22)
        self.img = ImageMobject(vazio).set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
        self.img.set_width(16).move_to(ORIGIN)
        self.add(self.img)
        # v7 (§1.3): o 3D ocupa a largura toda; por cima vai o MESMO céu (fundo_lab) com alfa por coluna (CONTA, `self.conta` 0–1,
        # degradê de x = −0,6 a 2,4, no máximo 0,9: o chão some no céu, sem aresta nem faixa escura) e por linha (header, 0,55)
        self.faixa = faixa
        self.conta = ValueTracker(0.0)
        ceu = np.array(fundo_lab(self.w, self.h).convert("RGBA"))
        self.ov = ImageMobject(ceu).set_resampling_algorithm(RESAMPLING_ALGORITHMS["linear"])
        self.ov.set_width(16).move_to(ORIGIN)
        xm = (np.arange(self.w) + 0.5) / self.w * 16 - 8
        u = np.clip((xm + 0.6) / 3.0, 0, 1)
        self._rx = (0.9 * u * u * (3 - 2 * u))[None, :]
        ym = 4.5 - (np.arange(self.h) + 0.5) / self.h * 9
        v = np.clip((ym - 2.75) / 0.45, 0, 1)
        self._ry = (0.55 * v * v * (3 - 2 * v))[:, None] if faixa else np.zeros((self.h, 1))
        self.add(self.ov)
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
        self.f = f
        o = self.op.get_value() * (self.mult(f / FPS) if self.mult else 1.0)
        o = max(0.0, min(1.0, o))
        self.img.pixel_array[..., 3] = int(255 * o)
        c = self.conta.get_value()              # o véu acompanha a opacidade (duas instâncias em crossfade não escurecem)
        self.ov.pixel_array[..., 3] = (255 * o * np.maximum(self._rx * c, self._ry)).astype(np.uint8)
        return self

    def real(self, chave):
        """Ponto `chave` como o Three.js o projetou neste quadro (pontos.json do r3d.js), em coordenadas do Manim; None se não houver
        (passagem seca ou quadro ausente). Usado onde o mapa analítico erra mais de 2 px (cano do rifle inclinado)."""
        if PEDIDOS3D:
            return None
        if not hasattr(self, "_pts"):
            arq = self.dir / "pontos.json"
            import json
            self._pts = json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else {}
        p = self._pts.get(str(self.f), {}).get(chave)
        return None if p is None else manim_de_px(p[0], p[1], self.w, self.h)

    def caixas(self):
        """Caixas (x0, y0, x1, y1) no Manim dos objetos 3D do quadro corrente, a partir dos pontos projetados (auditoria 3D × texto)."""
        if self.real("__") is None and not hasattr(self, "_pts"):
            return []
        q = self._pts.get(str(self.f), {})
        P = lambda k: manim_de_px(*q[k], self.w, self.h) if k in q else None
        cx = []
        base = self.cena.split("@")[0]
        if base == "cavalo" and P("cav_tras") is not None:
            a, b, c, d = P("cav_tras"), P("cav_frente"), P("cascos"), P("topo")
            cx.append((a[0], c[1], b[0] + 0.35, d[1]))
            pt, pb_, ptp = P("pedra_tras"), P("pedra_base"), P("pedra_topo")
            cx.append((pt[0], pb_[1], 2 * pb_[0] - pt[0], ptp[1]))
        elif base == "manequim":
            ps = [P(k) for k in ("cab", "pe0", "pe1", "mao0", "mao1", "peito") if k in q]
            if self.e.get("rifle", {}).get("on") and "pb" in q:
                ps.append(P("pb"))
            if ps:
                xs, ys = [p[0] for p in ps], [p[1] for p in ps]
                cx.append((min(xs) - 0.2, min(ys) - 0.15, max(xs) + 0.2, max(ys) + 0.3))
        elif base == "vela" and P("vela") is not None:
            v = P("vela")
            cx.append((v[0] - 1.6, v[1] - 1.6, v[0] + 1.6, v[1] + 1.6))
        elif base == "esferas" and "esf" in q:
            for p in q["esf"]:
                m = manim_de_px(*p[:2], self.w, self.h)
                cx.append((m[0] - 0.7, m[1] - 0.7, m[0] + 0.7, m[1] + 0.7))
        return cx


def chip_lento(op=0.85, y=2.78, x=PALCO_X[0] + 0.25, s="CÂMERA LENTA"):
    """Chip CÂMERA LENTA (v4: canto superior esquerdo do PALCO, longe dos eixos), enquanto a cena estiver em câmera lenta."""
    return mtxt(s, 15, color=DIM, op=op).move_to(P3(x, y), aligned_edge=LEFT).set_z_index(36)


def chip_replay(op=0.85, **kw):
    """Chip REPLAY (regra 1.2): o evento roda de novo, para a frente, uma vez só."""
    return chip_lento(op, s="REPLAY", **kw)


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


def proj3d(c, p):
    """v7: projeção exata da câmera do b3d.js (posicionaCamera + setViewOffset) → ponto do Manim. Vale para 'frente', 'topo' e 'obl'
    (3/4, com az/el/alvo); as setas e rótulos das cenas 3D novas usam isto (o pontos.json do r3d.js serve de conferência)."""
    K, fov = c.get("K", 1.0), c.get("fov", 14)
    alt = 9 / K
    modo = c.get("modo", "frente")
    if modo == "topo":
        az, el, alvo = -90.0, 89.999, (c.get("camx", 0), c.get("camy", 0), 0.0)
    elif modo == "obl":
        az, el, alvo = c["az"], c["el"], tuple(c["alvo"])
    else:
        az, el, alvo = -90.0, c.get("el", 0), (c.get("camx", 0), 0.0, c.get("camz", 0))
    a, e = math.radians(az), math.radians(el)
    D = (alt / 2) / math.tan(math.radians(fov) / 2)
    al = np.array(alvo, dtype=float)
    pos = al + D * np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    up = np.array([-math.sin(e) * math.cos(a), -math.sin(e) * math.sin(a), math.cos(e)])
    zc = (pos - al) / np.linalg.norm(pos - al)
    xc = np.cross(up, zc)
    xc /= np.linalg.norm(xc)
    yc = np.cross(zc, xc)
    q = np.asarray(p, dtype=float) - pos
    X, Y, Z = q @ xc, q @ yc, q @ zc
    f = 1 / math.tan(math.radians(fov) / 2)
    return P3(8 * (f / (16 / 9)) * X / -Z + c.get("xc", 0), 4.5 * f * Y / -Z + c.get("yc", 0))


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
    TITULO = "MECÂNICA · MOMENTO EM SISTEMAS"

    def setup_base(self, cap=None, selo=None):
        self.camera.background_color = BACKGROUND_COLOR
        self.camera.background_image = str(fundo_lab_arq(config.pixel_width, config.pixel_height))    # v7: céu da unidade
        self.camera.init_background()
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
        self._off, self.atrasos, self._pal, self._cur = None, [], [], 0
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
        rf = kw.pop("rate_func", None)      # v4: o rate_func vale só para as animações, nunca para o relógio (there_and_back
        if rf is not None:                  # fazia o tempo do 3D ir e voltar: o "quadro repetido a cada ~1,1 s" do hook)
            for a in anims:
                a.rate_func = rf
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
        self._anota(anims)

    def _anota(self, anims):
        """Guarda o último termo que entrou na tela (texto/MathTex estático, fora do header), para o realce das esperas longas."""
        for a in anims:
            if isinstance(a, (FadeIn, Write, TransformFromCopy, ReplacementTransform, GrowFromCenter)):
                m = getattr(a, "target_mobject", None) if isinstance(a, (TransformFromCopy, ReplacementTransform)) else a.mobject
                if m is None or m.get_updaters() or isinstance(m, (Fundo3D, ImageMobject)) or m in self.fixos():
                    continue
                if getattr(m, "sem_realce", False) or any(isinstance(x, RoundedRectangle) and x.get_fill_opacity() > 0.5
                                                           for x in m.get_family()):
                    continue                            # v5 (V5): painel cheio (DICA, barras) nunca leva o Indicate branco
                if any(isinstance(x, (Text, SingleStringMathTex)) for x in m.get_family()):
                    self._realce = m

    def _realce_ok(self):
        m = getattr(self, "_realce", None)
        if m is None or m in self.fixos():
            return None
        if not any(m is x or m in x.get_family() for x in self.mobjects):
            return None
        try:
            if max(x.get_fill_opacity() for x in m.family_members_with_points()) < 0.5:
                return None
        except ValueError:
            return None
        return m

    def _still(self):
        if STILL is not None and self.nq / FPS >= STILL:
            from manim.utils.exceptions import EndSceneEarlyException
            self.update_mobjects(0)            # o relógio já está no instante: atualiza os fundos 3D (opacidade das duas instâncias)
            self.update_mobjects(0)
            raise EndSceneEarlyException()

    def wait(self, duration=1.0, *a, **kw):
        """v4: espera longa (≥ 3,4 s) vira espera + realce do último termo da conta a cada ~2,3 s (o estado final fica, mas a tela
        nunca para ≥ 4 s; a duração total não muda)."""
        n = max(1, round(duration * FPS))
        # final: limiares em segundos (eram quadros de 15 fps; a 30 fps cada realce somava 0,5 s e o lote saía mais longo que a voz)
        if n >= round(3.4 * FPS) and STILL is None:      # ≥ 3,4 s
            alvo = self._realce_ok()
            if alvo is not None:
                n1 = round(2.3 * FPS)                    # 2,3 s parado, 1,0 s de realce, e o resto
                self._espera(n1)
                if self._realce_ok() is alvo:
                    self.play(Indicate(alvo, color=WHITE_, scale_factor=1.03), run_time=1.0)
                    self.wait((n - n1 - FPS) / FPS)
                else:
                    self.wait((n - n1) / FPS)
                return
        self._espera(n)

    def _espera(self, n):
        self._still()
        if AUDITORIA:
            self._auditar()
        if STILL is not None and self.nq < STILL * FPS < self.nq + n:      # still: a espera para no instante pedido
            n = max(1, int(math.ceil(STILL * FPS - self.nq)))
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

    def sobra(self, s):
        """v5: espera até faltarem `s` segundos para o fim da âncora (as saídas do fim do lote cabem na fala)."""
        q = self.alvo - round(s * FPS)
        if q - self.nq >= 1:
            self.wait((q - self.nq) / FPS)

    def resta(self):
        """Segundos que faltam para o fim da âncora corrente."""
        return max(0.0, (self.alvo - self.nq) / FPS)

    def an(self, aid):
        """Fecha a âncora anterior (espera o resto da fala) e abre `aid`. v5: tempo absoluto da voz — o lote guarda o deslocamento
        no primeiro an(); cada âncora termina no quadro do começo da seguinte (sem erro acumulado de arredondamento)."""
        self._fecha()
        a = ANC[aid]
        if getattr(self, "_off", None) is None:
            self._off = round(a["t0"] * FPS) - self.nq
        q_ini = round(a["t0"] * FPS) - self._off
        if self.nq > q_ini:
            self.atrasos.append((aid, (self.nq - q_ini) / FPS))
        self._aid, self._q0 = aid, self.nq
        self._pal, self._cur = a.get("palavras", []), 0
        self.alvo = round((a["t0"] + a["dur"]) * FPS) - self._off

    def _acha(self, trecho):
        """Instante (s, no vídeo) da primeira palavra de `trecho` na fala da âncora corrente, a partir do cursor."""
        alvo = [_norm(w) for w in trecho.split() if _norm(w)]
        ws = [w for w, _ in self._pal]
        for i in range(self._cur, len(ws) - len(alvo) + 1):
            if ws[i:i + len(alvo)] == alvo:
                self._cur = i + 1
                return self._pal[i][1]
        raise KeyError(f"[diz] {self._aid}: '{trecho}' não está na fala (depois do cursor)")

    def diz(self, trecho, antes=0.15):
        """v5 (sincronia fina): espera até `antes` s antes de a voz dizer `trecho` nesta âncora. Se a cena já passou do ponto,
        não espera e registra o atraso."""
        q = round((self._acha(trecho) - antes) * FPS) - self._off
        if q - self.nq >= 1:
            self.wait((q - self.nq) / FPS)
        elif self.nq - q > 0.3 * FPS:
            self.atrasos.append((f"{self._aid} «{trecho}»", (self.nq - q) / FPS))

    def clk_de(self, aid, trecho, antes=0.0):
        """Relógio do lote (s) em que a voz diz `trecho` na âncora `aid` (qualquer âncora do lote; não mexe no cursor)."""
        alvo = [_norm(w) for w in trecho.split() if _norm(w)]
        pal = ANC[aid]["palavras"]
        ws = [w for w, _ in pal]
        for i in range(len(ws) - len(alvo) + 1):
            if ws[i:i + len(alvo)] == alvo:
                return (round((pal[i][1] - antes) * FPS) - self._off) / FPS
        raise KeyError(f"[clk_de] {aid}: '{trecho}'")

    def ate_dizer(self, trecho, antes=0.15, mover=True):
        """Segundos que faltam até a voz dizer `trecho` (não espera; avança o cursor, a não ser com mover=False)."""
        c = self._cur
        t = self._acha(trecho)
        if not mover:
            self._cur = c
        return max(0.0, (round((t - antes) * FPS) - self._off - self.nq) / FPS)

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
        return {self.wm, self.h1, *([self.h2] if self.h2 else []), *([self._sl] if getattr(self, '_sl', None) else [])}

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

    def virada(self, *saem, cab=None, selo=None, rt=0.3, tudo=False):
        """v4 (regra 1.3): virada de cena em sequência. Sai tudo o que é da cena anterior (e o header da linha 2, se `cab` vier) em
        `rt` s; o novo header fica pendente e entra junto com a primeira animação da cena nova. `tudo=True`: sai tudo menos os fixos."""
        mobs = list(saem)
        if tudo:
            mobs = [m for m in self.mobjects if m not in self.fixos() and m is not self.clk]
        velhos = [m for m in (self.h2, getattr(self, "_sl", None)) if m is not None] if cab is not None else []
        anims = [m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in mobs] + [FadeOut(m) for m in velhos]
        if anims:
            self.play(*anims, run_time=rt)
        for m in mobs:
            if not isinstance(m, Fundo3D):      # o fundo 3D pode voltar depois (mesma tomada contínua)
                m.clear_updaters()
        self.remove(*mobs, *velhos)
        self.dica_atual = None
        if cab is not None:
            self.h2 = self._sl = None
            if cab:
                novo = txt(cab, 30, op=0.95).next_to(self.h1, DOWN, buff=0.14, aligned_edge=LEFT).set_z_index(40)
                self.h2 = novo
                self._pend.append(FadeIn(novo, run_time=0.25))
                if selo:
                    self._sl = txt(selo, 20, color=DIM, op=0.85).next_to(novo, DOWN, buff=0.12, aligned_edge=LEFT).set_z_index(40)
                    self._pend.append(FadeIn(self._sl, run_time=0.25))

    def clear(self, *keep, rt=0.6, junto=False):
        """junto=True: não apaga agora; o que sai some junto com a primeira animação da cena seguinte (sem tela vazia)."""
        keep = self.fixos() | set(keep)
        mobs = [m for m in self.mobjects if m not in keep and m is not self.clk]
        if junto and not any(isinstance(m, Fundo3D) for m in mobs):
            for m in mobs:
                m.clear_updaters()
            self._pend.extend(FadeOut(m) for m in mobs)
            self.dica_atual = None
            return
        if mobs:
            self.play(*[m.op.animate.set_value(0.0) if isinstance(m, Fundo3D) else FadeOut(m) for m in mobs], run_time=rt)
        for m in mobs:
            m.clear_updaters()
        self.remove(*mobs)
        self.dica_atual = None

    def logo(self, largura):
        img = ImageMobject(str(ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"))
        arr = img.get_pixel_array()
        ys, xs = np.nonzero(arr[:, :, 3] > 8)
        return ImageMobject(arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).set_width(largura)

    def hl(self, s, y=3.0, size=T_HL, color=WHITE_, x=0.0, bold=True):
        return txt(s, size, color=color, bold=bold).move_to(P3(x, y))

    def dica_entra(self, d):
        self.dica_atual = d
        self.play(FadeIn(d, shift=0.15 * UP), run_time=0.6)

    def dica_sai(self):
        if self.dica_atual is not None:
            self.play(FadeOut(self.dica_atual), run_time=0.4)
            self.remove(self.dica_atual)
            self.dica_atual = None

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

        def walk(m):
            if isinstance(m, ImageMobject):
                return
            if isinstance(m, (Text, SingleStringMathTex)):
                if op(m) > 0.08 and m.width > 0.01:
                    itens.append(m)
                return
            for s in m.submobjects:
                walk(s)

        for top in self.mobjects:
            walk(top)

        def bb(m):
            (x0, y0, _), (x1, y1, _) = m.get_critical_point(DL), m.get_critical_point(UR)
            return x0 + 0.03, y0 + 0.03, x1 - 0.03, y1 - 0.03

        def nome(m):
            return f"'{m.text[:30]}'" if isinstance(m, Text) else f"'{m.get_tex_string()[:30]}'"

        t = self.nq / FPS
        if os.environ.get("CONTRASTE") == "1" and t - getattr(self, "_ult_ctr", -9.0) >= 0.5:     # v7: caixas e cores dos textos (QA de contraste)
            self._ult_ctr = t
            for m in itens:
                x0, y0, x1, y1 = bb(m)
                print(f"[contraste] {self.lote} {t:.3f} {x0:.3f} {y0:.3f} {x1:.3f} {y1:.3f} {ManimColor(m.get_color()).to_hex()} {op(m):.2f} {nome(m)}")
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
        if graf[0] == 0:
            print(f"[audit] {t:7.1f}s SEM PALCO")
        # v3: rótulo × objeto 3D (caixas projetadas pelo Three.js) e desenho fora do quadro / cruzando a divisa PALCO–CONTA
        caixas = []
        for top in self.mobjects:
            if isinstance(top, Fundo3D):
                o = top.op.get_value() * (top.mult(self.nq / FPS) if top.mult else 1.0)
                if o > 0.3:
                    caixas += [(top.cena, c) for c in top.caixas()]
        fixos_t = set()
        for m in fixos:
            fixos_t |= set(m.get_family())
        for a in itens:
            if a in fixos_t:
                continue
            x0, y0, x1, y1 = bb(a)
            for nm, (cx0, cy0, cx1, cy1) in caixas:
                w, h = min(x1, cx1) - max(x0, cx0), min(y1, cy1) - max(y0, cy0)
                if w > 0.05 and h > 0.05:
                    print(f"[audit] {t:7.1f}s 3D×TEXTO {nm} x {nome(a)} ({w:.2f}x{h:.2f})")

        def desenhos(m, out):
            if isinstance(m, (Fundo3D, ImageMobject, Text, SingleStringMathTex)) or m in fixos:
                return
            if isinstance(m, VMobject) and not m.submobjects and m.points.size and op(m) > 0.15:
                out.append(m)
                return
            for s in m.submobjects:
                desenhos(s, out)
        ds = []
        for top in self.mobjects:
            if top is not self.clk:
                desenhos(top, ds)
        for d in ds:
            (x0, y0, _), (x1, y1, _) = d.get_critical_point(DL), d.get_critical_point(UR)
            if x0 < -8.02 or x1 > 8.02 or y0 < -4.52 or y1 > 4.52:
                print(f"[audit] {t:7.1f}s DESENHO FORA DO QUADRO {type(d).__name__} ({x0:.1f},{y0:.1f})–({x1:.1f},{y1:.1f})")
            elif x1 - x0 < 7.5 and x0 < PALCO_X[1] - 0.05 and x1 > CONTA_X[0] + 0.05:
                print(f"[audit] {t:7.1f}s CRUZA PALCO/CONTA {type(d).__name__} ({x0:.1f}–{x1:.1f}, y {y0:.1f}–{y1:.1f})")
        for i, a in enumerate(itens):
            x0, y0, x1, y1 = bb(a)
            if x0 < -7.9 or x1 > 7.9 or y0 < -4.4 or y1 > 4.4:
                print(f"[audit] {t:7.1f}s FORA DO QUADRO {nome(a)}")
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
        for nm, d in self.atrasos:
            print(f"[atraso] {nm}: {d:.2f} s depois da voz")
        print(f"[tempo] total {self.nq / FPS:.1f} s ({self.nq} quadros)")
        if PEDIDOS3D and self._ped:
            (DIR3D / "pedidos3d").mkdir(parents=True, exist_ok=True)
            out = {"cenas": {c: [[f, r4(e)] for f, e in sorted(d.items())] for c, d in self._ped.items()}}
            (DIR3D / "pedidos3d" / f"{self.lote}.json").write_text(json.dumps(out), encoding="utf-8")
            print(f"[3d] pedidos: " + ", ".join(f"{c} {len(d)}" for c, d in self._ped.items()))
