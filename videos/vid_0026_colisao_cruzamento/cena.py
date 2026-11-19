"""vid_0026 — O que uma marca no asfalto consegue contar sobre uma batida? (preview silencioso v4).

Curto vertical, Manim 2D. Cruzamento visto de cima: carro 1 (azul, 2000 kg) vem do oeste, carro 2 (violeta, 1000 kg) vem do sul,
ficam unidos e deslizam 8 m para leste e 6 m para norte. De trás para frente: trabalho–energia no deslizamento,
momento no impacto; depois a conferência de ida e volta, a energia, a ponte e o cartão final.
v3: variáveis navegam da cena para as equações (cópias; TransformByGlyphMap do MF-Tools nos passos algébricos), carros
azul/violeta em vidro, paleta do canal nas variáveis. v4 (handoff v4): hook do acidente, cena sempre à esquerda de uma coluna
fixa de parâmetros, margens de 0,45 u (auditoria com AUDITORIA=1), trocas em fases (a cópia pousa, depois o resto entra),
cortes para ~146 s e cartão final com @labparallax. v1–v3 em cena_v1.py … cena_v3.py.

Preview 540×960 / 15 fps:
    uv run python -m manim -r 540,960 --fps 15 videos/vid_0026_colisao_cruzamento/cena.py ColisaoCruzamento026
Só alguns blocos: SECOES=c02,c03 (os outros rodam sem animar, para manter o estado). Ritmo por bloco: ESTICA.
"""
import json
import os
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import *  # noqa: F401,F403

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from template.config import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import screen_text  # noqa: E402
from MF_Tools import TransformByGlyphMap  # noqa: E402

# ── paleta (handoff v3 §3; esquema dos longos de colisões) ─────────────────────────────────────────────────
WHITE_ = TEXT_COLOR           # massas, μ_k, g, números, operadores
CYAN = PRIMARY_COLOR          # energia cinética K
VEL = "#9C8CFF"               # velocidade
MAG = "#EA63FF"               # momento
HEAT = "#FF7A3D"              # energia convertida / trabalho do atrito
FC = "#5AA2FF"                # força
GEO = "#B8C4DA"               # geometria (d, Δx, Δy, cotas)
DIM = "#8FA3C4"               # texto secundário
ICE = "#EAF2FF"               # marca no asfalto
CAR1, CAR1_L = "#267BFF", "#7FB2FF"     # carro 1 (identidade, não grandeza)
CAR2, CAR2_L = "#745CFF", "#A99BFF"     # carro 2 (violeta da marca, mais escuro que o da velocidade)
PANEL, PANEL_L = "#0E2A52", "#7FB2FF"
ROAD = "#0B1530"


def mix(c, w, com=WHITE_):
    return interpolate_color(ManimColor(c), ManimColor(com), w).to_hex()


VEL_L, MAG_L = mix(VEL, 0.3), mix(MAG, 0.3)

SECOES = [s.strip() for s in os.environ.get("SECOES", "").split(",") if s.strip()]
AUDITORIA = os.environ.get("AUDITORIA") == "1"
# sincronização com a voz: MEDIR=1 grava o instante natural de cada âncora (nat.json); SYNC=sync.json faz cada âncora esperar
# o instante da sua frase e ajusta o ritmo do trecho seguinte (fator calculado por plan_sync.py)
MEDIR = os.environ.get("MEDIR") == "1"
SYNC = os.environ.get("SYNC")
# ritmo de cada bloco (multiplica todas as durações do bloco; a voz ajusta depois). 'cta' = cartão final.
ESTICA = {"c01": 1.0, "c02": 1.0, "c03": 1.0, "c04": 1.15, "c05": 1.1, "c06": 1.0, "c07": 1.0, "cta": 1.0}

# ── física (congelada) ──────────────────────────────────────────────────────────────────────────────────────
M1, M2, MU, G = 2000.0, 1000.0, 0.5, 10.0
DX, DY = 8.0, 6.0
D = float(np.hypot(DX, DY))
VF = float(np.sqrt(2 * MU * G * D))
VFX, VFY = VF * DX / D, VF * DY / D
V1I, V2I = (M1 + M2) * VFX / M1, (M1 + M2) * VFY / M2
P1I, P2I = M1 * V1I, M2 * V2I
KA1, KA2 = 0.5 * M1 * V1I ** 2, 0.5 * M2 * V2I ** 2
KA, KD = KA1 + KA2, 0.5 * (M1 + M2) * VF ** 2
TH = float(np.degrees(np.arctan2(DY, DX)))
assert abs(D - 10) < 1e-12 and abs(VF - 10) < 1e-12 and abs(VFX - 8) < 1e-12 and abs(VFY - 6) < 1e-12
assert abs(V1I - 12) < 1e-9 and abs(V2I - 18) < 1e-9 and abs(P1I - 24000) < 1e-6 and abs(P2I - 18000) < 1e-6
assert abs(np.hypot(P1I, P2I) - 30000) < 1e-6 and abs(KA1 - 144000) < 1e-6 and abs(KA2 - 162000) < 1e-6
assert abs(KA - 306000) < 1e-6 and abs(KD - 150000) < 1e-6
assert abs(V1I * 3.6 - 43.2) < 1e-9 and abs(V2I * 3.6 - 64.8) < 1e-9 and abs((KA - KD) / KA - 0.5098) < 1e-3

# ── mundo (metros; origem no ponto do impacto) e enquadramento ──────────────────────────────────────────────
UD = np.array([DX / D, DY / D, 0.0])        # direção da marca = direção de v⃗_f
L1, W1 = 4.8, 2.0                           # carro 1 (SUV, deitado: vai para leste)
L2, W2 = 3.4, 1.7                           # carro 2 (compacto, em pé: vai para norte)
C1 = np.array([0.0, W1 / 2, 0.0])           # centros no instante do contato
C2 = np.array([0.0, -L2 / 2, 0.0])
T0 = -0.25                                  # s antes do impacto (quadro "antes")
A_ = MU * G                                 # desaceleração no deslizamento (5 m/s²)
TSTOP = VF / A_                             # 2 s
AKW = 0.18                                  # m de mundo por (m/s) nas setas de velocidade
S_CENA, O_CENA = 0.31, (-2.31, 2.07)        # vista única: o cruzamento inteiro cabe à esquerda da coluna
MARG = 0.45                                 # margem de segurança do quadro 9×16
XL, XR, YB, YT = -4.5 + MARG, 4.5 - MARG, -8 + MARG, 8 - MARG
COL_X0, COL_X1, COL_Y0, COL_Y1 = 1.55, XR, -0.4, 4.55     # coluna lateral de parâmetros (~28 % da largura)
XCENA = 1.35                                # a cena fica à esquerda daqui


def P3(x, y):
    return np.array([x, y, 0.0])


def pol(r, graus):
    a = np.radians(graus)
    return np.array([r * np.cos(a), r * np.sin(a), 0.0])


def unit(v):
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    return v / n if n > 1e-9 else v


def s_desl(t):
    """Distância deslizada (m) no instante físico t (s) depois do impacto."""
    t = min(max(t, 0.0), TSTOP)
    return VF * t - 0.5 * A_ * t * t


def vel_desl(t):
    return max(VF - A_ * max(t, 0.0), 0.0) if t > 0 else VF


def pos1(t):
    return C1 + (P3(V1I * t, 0) if t <= 0 else UD * s_desl(t))


def pos2(t):
    return C2 + (P3(0, V2I * t) if t <= 0 else UD * s_desl(t))


def w2s(p):
    return P3(*O_CENA) + S_CENA * np.asarray(p, float)


# o mundo inteiro (carros na partida e no fim, cotas) cabe à esquerda da coluna e dentro das margens
assert w2s(pos1(T0) - P3(L1 / 2, 0))[0] > XL and w2s(pos1(TSTOP) + P3(L1 / 2, 0))[0] < XCENA
assert w2s(pos1(TSTOP) + P3(0, W1 / 2))[1] < COL_Y1 + 0.01 and w2s(pos2(T0) - P3(0, L2 / 2))[1] > COL_Y0 - 0.05


# ── texto, matemática e formas ──────────────────────────────────────────────────────────────────────────────
@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def txt(s, size=26, color=WHITE_, op=1.0, width=8.0):
    """Texto de tela: Space Grotesk em maiúsculas; '\\n' quebra linha."""
    lines = []
    for line in s.upper().split("\n"):
        with wide_pango():
            t = screen_text(line, size, oversample=2 if size >= 30 else 4)
        lines.append(t.set_color(color).set_opacity(op))
    g = VGroup(*lines).arrange(DOWN, buff=0.14)
    if g.width > width:
        g.scale_to_fit_width(width)
    return g


def contorno(m, w=6):
    return m.set_stroke(BACKGROUND_COLOR, w, background=True)


def arrow(a, b, color=WHITE_, width=5, z=8, tip=0.2, op=1.0):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if np.linalg.norm(b - a) < 0.03:
        return VMobject()
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.45,
                 max_stroke_width_to_length_ratio=50).set_opacity(op).set_z_index(z)


def seta_halo(a, b, color=VEL, width=6, tip=0.22, z=12):
    """Seta de velocidade com halo claro (fica legível sobre o asfalto e ao lado do carro violeta)."""
    h = arrow(a, b, WHITE_, width + 6, z=z - 1, tip=tip + 0.04, op=0.18)
    return VGroup(h, arrow(a, b, color, width, z=z, tip=tip))


def lab_at(m, a, b, lado=1, gap=0.14):
    """Rótulo ao lado do segmento a→b (lado=+1: à esquerda de a→b), com contorno escuro."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = unit(b - a)
    nrm = np.array([-d[1], d[0], 0.0]) * lado
    meia = 0.5 * (abs(nrm[0]) * m.width + abs(nrm[1]) * m.height)
    m.move_to((a + b) / 2 + nrm * (gap + meia))
    return contorno(m).set_z_index(14)


def arco(c, r, a0, a1, w=2.0, op=0.95):
    return Arc(radius=r, start_angle=np.radians(a0), angle=np.radians(a1 - a0), arc_center=np.asarray(c, float)) \
        .set_stroke(WHITE_, w, opacity=op).set_z_index(9)


def caixa(m, color=WHITE_, buff=0.16, width=2.0, op=1.0):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=width, corner_radius=0.1).set_stroke(opacity=op)


def cartao(m=None, buff=0.2, cor=PANEL_L, w=None, h=None, centro=None):
    """Cartão de painel: azul profundo translúcido com borda clara fina (equações-chave e dados)."""
    r = RoundedRectangle(corner_radius=0.14, width=w or m.width + 2 * buff, height=h or m.height + 2 * buff)
    r.set_fill(PANEL, 0.55).set_stroke(cor, 1.5, opacity=0.6).move_to(centro if centro is not None else m).set_z_index(-1)
    return r


def ficha(n, cor, r=0.15):
    """Fichinha de identidade do carro ('1' azul, '2' violeta)."""
    c = Circle(radius=r).set_fill(cor, 1).set_stroke(mix(cor, 0.4), 1.5)
    return VGroup(c, MathTex(str(n), font_size=int(r * 150), color=WHITE_).move_to(c))


def marca_mob(a, b, w=4.0, sep=0.1, cor=ICE, op=0.9):
    """Marca de deslizamento a→b: dois traços paralelos com brilho suave."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if np.linalg.norm(b - a) < 1e-3:
        return VGroup()
    d = unit(b - a)
    n = np.array([-d[1], d[0], 0.0]) * sep
    tr = VGroup(Line(a + n, b + n), Line(a - n, b - n))
    brilho = tr.copy().set_stroke(cor, w * 3, opacity=0.12)
    return VGroup(brilho, tr.set_stroke(cor, w, opacity=op)).set_z_index(1)


class Carro(VGroup):
    """Carro visto de cima (em metros de mundo), corpo em vidro: rodas, teto, para-brisa, faróis e lanternas.
    Construído apontando para +x; `ang` gira o corpo (o rótulo da massa fica sempre de pé)."""

    def __init__(self, L, W, cor, borda, nome, ang=0.0):
        super().__init__()
        rodas = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.75, height=0.32)
                         .set_fill("#060A16", 1).set_stroke(borda, 1, opacity=0.5).move_to(P3(sx * L * 0.3, sy * (W / 2 - 0.02)))
                         for sx in (-1, 1) for sy in (-1, 1)])
        halo = RoundedRectangle(corner_radius=W * 0.32, width=L + 0.25, height=W + 0.25) \
            .set_fill(opacity=0).set_stroke(borda, 9, opacity=0.18)
        corpo = RoundedRectangle(corner_radius=W * 0.3, width=L, height=W).set_fill(cor, 0.62).set_stroke(borda, 2.6)
        brilho = Line(P3(-L * 0.36, W * 0.36), P3(L * 0.3, W * 0.36)).set_stroke(WHITE_, 1.6, opacity=0.35)
        teto = RoundedRectangle(corner_radius=W * 0.2, width=L * 0.46, height=W * 0.7).move_to(P3(-L * 0.06, 0)) \
            .set_fill(mix(cor, 0.55, BACKGROUND_COLOR), 0.95).set_stroke(borda, 1.2, opacity=0.7)
        xf = L * 0.17
        para = Polygon(P3(xf, W * 0.33), P3(xf + L * 0.13, W * 0.4), P3(xf + L * 0.13, -W * 0.4), P3(xf, -W * 0.33)) \
            .set_fill("#081022", 0.95).set_stroke(borda, 1.2, opacity=0.8)
        tras = Polygon(P3(-L * 0.29, W * 0.32), P3(-L * 0.36, W * 0.37), P3(-L * 0.36, -W * 0.37), P3(-L * 0.29, -W * 0.32)) \
            .set_fill("#081022", 0.9).set_stroke(borda, 1, opacity=0.6)
        far = VGroup(*[Ellipse(width=0.22, height=0.34).set_fill("#F2F8FF", 1).set_stroke(width=0)
                       .move_to(P3(L / 2 - 0.12, s * W * 0.32)) for s in (-1, 1)])
        lan = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.12, height=0.36).set_fill(MAG, 0.9).set_stroke(width=0)
                       .move_to(P3(-L / 2 + 0.08, s * W * 0.32)) for s in (-1, 1)])
        self.corpo = VGroup(rodas, halo, corpo, brilho, teto, para, tras, far, lan)
        self.corpo.rotate(ang, about_point=ORIGIN)
        self.rot = MathTex(nome, font_size=int(min(W, L) * 52), color=WHITE_).move_to(ORIGIN)
        self.add(self.corpo, self.rot)
        self.set_z_index(10)


class Eq:
    """Equação em partes nomeadas, com os glifos achatados na ordem da compilação (como no yt_0014).
    `.mt` = MathTex em partes; `.m` = VGroup(VGroup(glifos)) para o TransformByGlyphMap; `.idx[nome]` = índices.
    Cor por parte: None (branco), uma cor, ou ('fr', cor) (fração: tudo menos a barra)."""

    def __init__(self, partes, size=44, pos=None, w=None):
        self.mt = MathTex(*[p[1] for p in partes], font_size=size, color=WHITE_)
        if w and self.mt.width > w:
            self.mt.scale_to_fit_width(w)
        if pos is not None:
            self.mt.move_to(pos)
        self.idx, self.gl, i = {}, [], 0
        for p, sub in zip(partes, self.mt.submobjects):
            g = list(sub.family_members_with_points())
            self.idx[p[0]] = list(range(i, i + len(g)))
            self.gl += g
            i += len(g)
        self.m = VGroup(VGroup(*self.gl))
        for p in partes:
            if len(p) > 2 and p[2] is not None:
                if isinstance(p[2], tuple):
                    b, nu, de = self._fr(p[0])
                    for j in nu + de:
                        self.gl[j].set_color(p[2][1])
                else:
                    self.parte(p[0]).set_color(p[2])

    def parte(self, n):
        return VGroup(*[self.gl[i] for i in _spec(self, n)])

    def _fr(self, n):
        """(barra, numerador, denominador) de uma parte-fração, em índices de glifo (da esquerda para a direita)."""
        ix = self.idx[n]
        gs = [self.gl[i] for i in ix]
        k = max(range(len(gs)), key=lambda j: gs[j].width)
        bx0, bx1, by = gs[k].get_left()[0], gs[k].get_right()[0], gs[k].get_center()[1]
        dentro = [j for j in range(len(gs)) if j != k and bx0 - 0.05 <= gs[j].get_center()[0] <= bx1 + 0.05]
        num = sorted([j for j in dentro if gs[j].get_center()[1] > by], key=lambda j: gs[j].get_center()[0])
        den = sorted([j for j in dentro if gs[j].get_center()[1] < by], key=lambda j: gs[j].get_center()[0])
        return [ix[k]], [ix[j] for j in num], [ix[j] for j in den]

    def num(self, n):
        return self._fr(n)[1]

    def den(self, n):
        return self._fr(n)[2]

    def barra(self, n):
        return self._fr(n)[0]

    def para(self, B, *pares, auto=True):
        """Mapa de glifos de `self` para `B`. Cada par é (de, para[, kwargs]); lista vazia = some (de) ou nasce (para).
        Partes de mesmo nome e mesmo número de glifos não citadas seguem juntas; o resto entra e sai por fade."""
        usA, usB, ents = set(), set(), []
        for p in pares:
            a, b = _spec(self, p[0]), _spec(B, p[1])
            ents.append((a, b, p[2]) if len(p) > 2 else (a, b))
            usA.update(a)
            usB.update(b)
        if auto:
            for n, ia in self.idx.items():
                ib = B.idx.get(n)
                if ib is not None and len(ia) == len(ib) and not usA.intersection(ia) and not usB.intersection(ib):
                    ents.append((ia, ib))
                    usA.update(ia)
                    usB.update(ib)
        return ents


def _spec(E, s):
    """Índices de glifo: 'nome' | ('nome', i|fatia) | inteiro | lista dessas coisas."""
    if isinstance(s, str):
        return list(E.idx[s])
    if isinstance(s, int):
        return [s]
    if isinstance(s, tuple) and len(s) == 2 and isinstance(s[0], str) and not isinstance(s[1], str):
        v = E.idx[s[0]][s[1]]
        return list(v) if isinstance(v, list) else [v]
    out = []
    for x in s:
        out += _spec(E, x)
    return out


def radicando(E, n):
    """Glifos do radicando de uma parte √(...), da esquerda para a direita (sem o radical nem o traço de cima)."""
    ix = sorted(E.idx[n], key=lambda i: E.gl[i].get_left()[0])
    return [i for i in ix[1:] if E.gl[i].width < 4 * max(E.gl[i].height, 1e-3)]


def rotulo_v(nome, val=r"?", size=32):
    """Rótulo de seta de velocidade: v⃗ = ? (violeta), que depois recebe o valor."""
    return Eq([("v", nome, VEL), ("eq", "="), ("n", val)], size)


def cota_eq(sim, n, size, mostrar_sim=True):
    """Rótulo de cota (geometria): 'Δx = 8 m' ou só '8 m'."""
    partes = ([("s", sim, GEO), ("eq", "=")] if mostrar_sim else []) + [("n", n, GEO), ("u", r"\,\mathrm{m}", GEO)]
    return Eq(partes, size)


class Linha(VGroup):
    """Régua física ANTES → IMPACTO → DESLIZAMENTO → PAROU; o estado ativo ganha a cor da lei (impacto: momento,
    magenta; deslizamento: trabalho–energia, ciano)."""
    XS = (-3.25, -1.2, 1.25, 3.4)
    CORES = (WHITE_, MAG, CYAN, WHITE_)

    def __init__(self, y=5.0, k=0):
        super().__init__()
        self.y = y
        self.rot = [txt(s, 21) for s in ("ANTES", "IMPACTO", "DESLIZAMENTO", "PAROU")]
        for r, x in zip(self.rot, self.XS):
            r.move_to(P3(x, y + 0.33))
        trilho = Line(P3(-3.95, y), P3(3.95, y)).set_stroke(DIM, 2, opacity=0.5)
        ticks = VGroup(*[Line(P3(x, y - 0.07), P3(x, y + 0.07)).set_stroke(DIM, 2, opacity=0.8) for x in self.XS])
        self.dot = Dot(P3(self.XS[k], y), radius=0.09, color=self.CORES[k]).set_z_index(30)
        self.add(trilho, ticks, *self.rot, self.dot)
        for i, r in enumerate(self.rot):
            r.set_color(self.CORES[i] if i == k else WHITE_).set_opacity(1.0 if i == k else 0.38)

    def ir(self, k):
        return [self.dot.animate.move_to(P3(self.XS[k], self.y)).set_color(self.CORES[k])] + \
            [r.animate.set_color(self.CORES[i] if i == k else WHITE_).set_opacity(1.0 if i == k else 0.38)
             for i, r in enumerate(self.rot)]


class ColisaoCruzamento026(Scene):
    # ------------------------------------------------------------------ utilidades de tempo e texto
    def p(self, *anims, rt=1.0, **kw):
        self.play(*anims, run_time=rt * self.K, **kw)

    def w(self, t):
        self.wait(t * self.K)

    def ancora(self, nome):
        """Ponto da cena que começa junto com uma frase da voz (ver plan_sync.py)."""
        t = self.renderer.time
        if MEDIR:
            self.nat[nome] = round(t, 4)
        elif self.sync:
            a = self.sync["ancoras"][nome]
            falta = a["T"] - t
            if falta > 0.5 / config.frame_rate:
                self.wait(falta)
            elif falta < -0.1:
                print(f"[sync] {nome}: cena atrasada {-falta:.2f} s")
            self.K = a["f"]

    def sai(self, *mobs, rt=0.35):
        """Saída antes da entrada seguinte (nunca texto sobre texto). Aceita Eq."""
        ms = []
        for m in mobs:
            if m is None:
                continue
            ms.append(m.m if isinstance(m, Eq) else m)
        if ms:
            self.p(*[FadeOut(m) for m in ms], rt=rt)
            self.remove(*ms)
            for m in mobs:
                if isinstance(m, Eq):
                    self.remove(m.mt, *m.gl)

    def cab(self, s, size=32):
        """Cabeçalho do bloco (y = 6.3, branco com traço ciano): o anterior sai primeiro; devolve a entrada do novo."""
        self.sai(self.head, rt=0.3)
        if not s:
            self.head = None
            return []
        t = txt(s, size, width=XR - XL).move_to(P3(0, 6.3))
        tr = Line(t.get_corner(DL) + DOWN * 0.13, t.get_corner(DR) + DOWN * 0.13).set_stroke(CYAN, 1.6, opacity=0.7)
        self.head = VGroup(t, tr).set_z_index(20)
        return [FadeIn(self.head, shift=0.1 * DOWN)]

    def frase(self, s, size=24, y=-6.6, color=WHITE_, x=0.0, width=XR - XL):
        self.sai(self._frase, rt=0.3)
        self._frase = txt(s, size, color=color, width=width).move_to(P3(x, y)).set_z_index(20) if s else None
        return [FadeIn(self._frase, shift=0.1 * UP)] if self._frase is not None else []

    def troca(self, old, new, rt=0.6, shift=0.1 * UP):
        self.sai(old)
        self.p(FadeIn(new, shift=shift), rt=rt)
        return new

    # ------------------------------------------------------------------ equações que navegam
    def assenta(self, E):
        """Deixa na cena só E.m (sem glifos soltos de transformações anteriores)."""
        fam = {id(g) for g in E.gl}
        soltos = [m for m in self.mobjects if m is not E.m and (id(m) in fam or (
            m.submobjects and all(id(x) in fam for x in m.family_members_with_points())))]
        self.remove(*soltos, E.mt)
        self.add(E.m)
        return E

    def nasce(self, E, fontes=(), rt=1.0, extra=(), depois=()):
        """E nasce de termos que já estão na cena, em fases: (1) as cópias das `fontes` viajam até o lugar;
        (2) entra o resto da equação; (3) entram as partes `depois` (o resultado). Nada pousa em cima de outra coisa."""
        usados = set()
        copias = []
        for orig, spec in fontes:
            ix = _spec(E, spec)
            usados.update(ix)
            copias.append(TransformFromCopy(orig, VGroup(*[E.gl[i] for i in ix])))
        tarde = set(_spec(E, list(depois))) if depois else set()
        resto = [E.gl[i] for i in range(len(E.gl)) if i not in usados and i not in tarde]
        if copias:
            self.p(*copias, *extra, rt=rt)
            extra = ()
        if resto or extra:
            self.p(*([FadeIn(VGroup(*resto), shift=0.06 * UP)] if resto else []), *extra, rt=0.4)
        if tarde:
            self.p(FadeIn(VGroup(*[E.gl[i] for i in sorted(tarde)]), shift=0.06 * LEFT), rt=0.5)
        return self.assenta(E)

    def _passo(self, A, B, *pares, **kw):
        self.assenta(A)
        ents = A.para(B, *pares)
        anim = TransformByGlyphMap(A.m, B.m, *ents, auto_fade=True, **kw)

        def fim():
            self.remove(A.m, *A.gl)
            self.assenta(B)
        return anim, fim

    def passo(self, A, B, *pares, rt=1.3, extra=(), **kw):
        """Passo algébrico com MF-Tools: os glifos de A navegam até o lugar que ocupam em B (TransformByGlyphMap)."""
        return self.passos([(A, B, pares, kw)], rt=rt, extra=extra)[0]

    def passos(self, lista, rt=1.3, extra=()):
        """Vários passos com MF-Tools tocados juntos (ex.: isolar v₁ᵢ e v₂ᵢ em paralelo)."""
        anims, fins = [], []
        for A, B, pares, kw in lista:
            a, f = self._passo(A, B, *pares, **kw)
            anims.append(a)
            fins.append(f)
        self.p(*anims, *extra, rt=rt)
        for f in fins:
            f()
        return [x[1] for x in lista]

    def substitui(self, A, B, pares=(), copias=(), rt=1.2, manter=False):
        """Substituição com cópia deliberada, em fases: (1) sai o que de A não continua; (2) os pares A→B se transformam
        e as `copias` = [(origem na cena, parte de B)] viajam e pousam em lugares vazios; (3) entra o resto de B.
        `manter=True`: A fica na cena (a nova linha nasce de cópias de A)."""
        self.assenta(A)
        trans, usA, usB = [], set(), set()
        nomes_copia = [c[1] for c in copias if isinstance(c[1], str)]
        for a, b in pares:
            ia, ib = _spec(A, a), _spec(B, b)
            usA.update(ia)
            usB.update(ib)
            trans.append((ia, ib))
        for n, ia in A.idx.items():
            ib = B.idx.get(n)
            if ib is not None and len(ia) == len(ib) and not usA.intersection(ia) and not usB.intersection(ib) \
                    and n not in nomes_copia:
                usA.update(ia)
                usB.update(ib)
                trans.append((ia, ib))
        cp = []
        for orig, b in copias:
            ib = _spec(B, b)
            usB.update(ib)
            cp.append(TransformFromCopy(orig, VGroup(*[B.gl[i] for i in ib])))
        sobraA = [A.gl[i] for i in range(len(A.gl)) if i not in usA]
        sobraB = [B.gl[i] for i in range(len(B.gl)) if i not in usB]
        if sobraA and not manter:
            self.p(FadeOut(VGroup(*sobraA), shift=0.08 * DOWN), rt=0.3)
            self.remove(*sobraA)
        if manter:
            an = [TransformFromCopy(VGroup(*[A.gl[i] for i in ia]), VGroup(*[B.gl[i] for i in ib])) for ia, ib in trans]
        else:
            self.remove(A.m)
            an = [ReplacementTransform(VGroup(*[A.gl[i] for i in ia]), VGroup(*[B.gl[i] for i in ib])) for ia, ib in trans]
        self.p(*an, *cp, rt=rt)
        if sobraB:
            self.p(FadeIn(VGroup(*sobraB), shift=0.06 * UP), rt=0.4)
        if not manter:
            self.remove(*A.gl)
        return self.assenta(B)

    def riscar(self, *partes):
        return VGroup(*[Line(p.get_corner(DL) + P3(-0.05, -0.05), p.get_corner(UR) + P3(0.05, 0.05)).set_stroke(WHITE_, 4)
                        for p in partes])

    # ------------------------------------------------------------------ auditoria de margens (desenvolvimento)
    def auditar(self, nome):
        if not AUDITORIA:
            return
        ignora = {id(m) for m in (self.atmos, self.wm, self.tag, self.via)}
        for m in self.mobjects:
            if id(m) in ignora or not m.family_members_with_points():
                continue
            l, r = m.get_left()[0], m.get_right()[0]
            b, t = m.get_bottom()[1], m.get_top()[1]
            if l < XL - 1e-3 or r > XR + 1e-3 or b < YB - 1e-3 or t > YT + 1e-3:
                print(f"[margem] {nome}: {type(m).__name__} x[{l:.2f},{r:.2f}] y[{b:.2f},{t:.2f}]")

    # ------------------------------------------------------------------ cena
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.fundo()
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.4).to_corner(UR, buff=0.28).set_z_index(40)
        self.tag = txt("EXERCÍCIO RESOLVIDO · EP. 9", 20, op=0.7).to_corner(UL, buff=0.4).set_z_index(40)
        self.add(self.wm, self.tag)
        self.fixos = {self.wm, self.tag, self.atmos}
        self.head, self._frase = None, None
        self.montar_mundo()
        self.nat = {}
        self.sync = json.loads(Path(SYNC).read_text(encoding="utf-8")) if SYNC else None
        marcas = []
        for nome in ("c01", "c02", "c03", "c04", "c05", "c06", "c07", "cta"):
            self.K = 1.0 if (MEDIR or self.sync) else ESTICA[nome]
            self.next_section(nome, skip_animations=bool(SECOES) and nome not in SECOES)
            t0 = self.renderer.time
            getattr(self, nome)()
            self.auditar(nome)
            marcas.append((nome, t0, self.renderer.time))
        for nome, a, b in marcas:
            print(f"[tempo] {nome}: {a:6.1f} s -> {b:6.1f} s ({b - a:5.1f} s)")
        if MEDIR:
            self.nat["_fim"] = round(self.renderer.time, 4)
            Path(__file__).absolute().with_name("nat.json").write_text(json.dumps(self.nat, indent=1), encoding="utf-8")

    def fundo(self):
        """Atmosfera cósmica muito sutil: poucas estrelas e brilhos radiais de baixíssima opacidade."""
        rng = np.random.default_rng(26)
        est = VGroup(*[Dot(P3(rng.uniform(-4.4, 4.4), rng.uniform(-7.8, 7.8)), radius=rng.uniform(0.008, 0.022),
                           color=WHITE_).set_opacity(rng.uniform(0.12, 0.38)) for _ in range(46)])
        brilhos = VGroup()
        for c, cor, r in ((P3(-1.5, 2.2), CYAN, 4.2), (P3(2.6, 0.2), CAR2, 3.6), (P3(-2.2, -5.4), MAG, 3.4)):
            for k in range(5):
                brilhos.add(Circle(radius=r * (1 - 0.18 * k)).set_stroke(width=0).set_fill(cor, 0.012).move_to(c))
        self.atmos = VGroup(brilhos, est).set_z_index(-10)
        self.add(self.atmos)

    def montar_mundo(self):
        # vias (em metros): leste–oeste x∈[−5.8, 10.8], y∈[−1.5, 3.5]; norte–sul x∈[−2.5, 2.5], y∈[−8.2, 8]
        h = Rectangle(width=16.6, height=5).move_to(P3(2.5, 1))
        v = Rectangle(width=5, height=16.2).move_to(P3(0, -0.1))
        try:
            via = Union(h, v)
        except Exception:
            via = VGroup(h, v)
        via.set_fill(ROAD, 0.88).set_stroke(CYAN, 1.5, opacity=0.35).set_z_index(-3)
        faixas = VGroup(DashedLine(P3(-5.6, 1), P3(-2.9, 1), dash_length=0.9), DashedLine(P3(2.9, 1), P3(10.6, 1), dash_length=0.9),
                        DashedLine(P3(0, -8.0), P3(0, -1.9), dash_length=0.9), DashedLine(P3(0, 3.9), P3(0, 7.8), dash_length=0.9)) \
            .set_stroke(GEO, 1.5, opacity=0.4).set_z_index(-2)
        self.via = VGroup(via, faixas)
        self.via.scale(S_CENA, about_point=ORIGIN).shift(P3(*O_CENA))
        self.tt = ValueTracker(T0)
        self.v1 = Carro(L1, W1, CAR1, CAR1_L, "m_1").scale(S_CENA, about_point=ORIGIN)
        self.v2 = Carro(L2, W2, CAR2, CAR2_L, "m_2", ang=PI / 2).scale(S_CENA, about_point=ORIGIN)
        self.ligar_carros()
        self.segue = True
        self.marca = always_redraw(lambda: marca_mob(w2s(ORIGIN), w2s(UD * (s_desl(self.tt.get_value()) if self.segue else D)),
                                                     w=3.0, sep=0.05))

    def ligar_carros(self):
        for car, fn in ((self.v1, pos1), (self.v2, pos2)):
            car.clear_updaters()
            car.add_updater(lambda m, fn=fn: m.move_to(w2s(fn(self.tt.get_value()))))
            car.move_to(w2s(fn(self.tt.get_value())))

    def bussola(self, o, size=20):
        return VGroup(arrow(o, o + P3(0, 0.5), DIM, 2.5, tip=0.12), arrow(o, o + P3(0.5, 0), DIM, 2.5, tip=0.12),
                      txt("N", size, color=DIM).move_to(o + P3(0, 0.74)), txt("L", size, color=DIM).move_to(o + P3(0.74, 0)))

    def flash(self, cor=WHITE_):
        return Flash(w2s(ORIGIN), color=cor, line_length=0.25, flash_radius=0.15, num_lines=12)

    def anel_impacto(self, cor=HEAT):
        c = Circle(radius=0.1).move_to(w2s(ORIGIN)).set_stroke(cor, 3.5).set_z_index(15)
        return c, c.animate.scale(4.5).set_stroke(opacity=0)

    def setas_antes(self, val1="?", val2="?", size=32):
        """Setas violeta de v⃗₁ᵢ e v⃗₂ᵢ à frente de cada carro (fora do corpo), no quadro t = T0.
        Rótulo de v⃗₁ᵢ acima do carro 1 (o momento, quando houver, fica abaixo); o de v⃗₂ᵢ à direita da seta."""
        a1 = w2s(pos1(T0) + P3(L1 / 2 + 0.35, 0))
        a2 = w2s(pos2(T0) + P3(0, L2 / 2 + 0.35))
        s1 = seta_halo(a1, a1 + P3(V1I * AKW * S_CENA, 0), width=5, tip=0.18)
        s2 = seta_halo(a2, a2 + P3(0, V2I * AKW * S_CENA), width=5, tip=0.18)
        r1 = rotulo_v(r"\vec v_{1i}", val1, size)
        r2 = rotulo_v(r"\vec v_{2i}", val2, size)
        contorno(r1.mt.next_to(w2s(pos1(T0) + P3(0, W1 / 2)), UP, buff=0.12)).set_z_index(14)
        r1.mt.align_to(P3(XL + 0.02, 0), LEFT)
        contorno(r2.mt.next_to(s2, RIGHT, buff=0.12)).set_z_index(14)
        return VGroup(s1, s2), r1, r2

    def cotas(self, sim=True, size=30):
        """Cotas da marca (geometria): catetos tracejados e rótulos do lado de fora, longe dos carros; d dentro do
        triângulo, longe da marca e dos carros; ângulo."""
        O, X, Q = w2s(ORIGIN), w2s(P3(DX, 0)), w2s(P3(DX, DY))
        legs = VGroup(DashedLine(O, X, dash_length=0.08), DashedLine(X, Q, dash_length=0.08)).set_stroke(GEO, 2, opacity=0.75)
        legs.set_z_index(2)
        lx = cota_eq(r"\Delta x", "8", size, sim)
        lab_at(lx.mt, O, X, lado=-1, gap=0.1)
        ly1 = Eq([("s", r"\Delta y", GEO)], size) if sim else None
        ly2 = Eq(([("eq", "=")] if sim else []) + [("n", "6", GEO), ("u", r"\,\mathrm{m}", GEO)], size)
        bloco = VGroup(*([ly1.mt] if sim else []), ly2.mt).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        bloco.next_to(w2s(P3(DX + W2 / 2 + 0.2, 1.4)), RIGHT, buff=0.04)
        for m in bloco:
            contorno(m).set_z_index(14)
        ld = cota_eq("d", "10", size, sim)
        ld.mt.move_to(w2s(P3(5.3, 2.0)))
        contorno(ld.mt).set_z_index(14)
        ang = VGroup(DashedLine(O, O + P3(0.75, 0), dash_length=0.07).set_stroke(DIM, 1.8, opacity=0.8),
                     arco(O, 0.5, 0, TH),
                     contorno(MathTex(r"\theta", font_size=size - 2, color=WHITE_).move_to(O + pol(0.74, TH / 2))))
        ang.set_z_index(9)
        return dict(legs=legs, lx=lx, ly1=ly1, ly2=ly2, ld=ld, ang=ang,
                    g=VGroup(legs, lx.mt, *([ly1.mt] if sim else []), ly2.mt, ld.mt, ang))

    # ------------------------------------------------------------------ coluna lateral de parâmetros
    def coluna(self):
        """Coluna fixa à direita: m₁, m₂, μ_k, g (depois M, v_fx, v_fy, v₁ᵢ, v₂ᵢ)."""
        self.col = cartao(w=COL_X1 - COL_X0, h=COL_Y1 - COL_Y0, centro=P3((COL_X0 + COL_X1) / 2, (COL_Y0 + COL_Y1) / 2))
        self.f1, self.f2 = ficha(1, CAR1, 0.14), ficha(2, CAR2, 0.14)
        self.d_m1 = Eq([("s", "m_1"), ("eq", "="), ("v", "2000"), ("u", r"\,\mathrm{kg}")], 30)
        self.d_m2 = Eq([("s", "m_2"), ("eq", "="), ("v", "1000"), ("u", r"\,\mathrm{kg}")], 30)
        self.d_mu = Eq([("s", r"\mu_k"), ("eq", "="), ("v", r"0{,}50")], 30)
        self.d_g = Eq([("s", "g"), ("eq", "="), ("v", "10"), ("u", r"\,\mathrm{m/s^2}")], 30)
        for e, y, ch in ((self.d_m1, 4.2, self.f1), (self.d_m2, 3.74, self.f2), (self.d_mu, 3.28, None), (self.d_g, 2.82, None)):
            self.na_coluna(e, y, ch)
        return VGroup(self.col, self.f1, self.f2, self.d_m1.mt, self.d_m2.mt, self.d_mu.mt, self.d_g.mt)

    def na_coluna(self, e, y, ch=None):
        x0 = COL_X0 + 0.16
        if ch is not None:
            ch.move_to(P3(x0 + 0.14, y))
            x0 += 0.36
        if e.mt.width > COL_X1 - 0.12 - x0:
            e.mt.scale_to_fit_width(COL_X1 - 0.12 - x0)
        e.mt.move_to(P3(x0, y), aligned_edge=LEFT)
        return e

    # ================================================================ C01 · hook: o acidente e a volta no tempo
    def c01(self):
        self.linha = Linha(k=0)
        self.bus = self.bussola(P3(0.55, -0.15))
        q1 = MathTex("?", font_size=40, color=WHITE_).set_z_index(15)
        q2 = MathTex("?", font_size=40, color=WHITE_).set_z_index(15)
        q1.add_updater(lambda m: m.next_to(self.v1, UP, buff=0.08))
        q2.add_updater(lambda m: m.next_to(self.v2, RIGHT, buff=0.1))
        selo = txt("ACIDENTE NO CRUZAMENTO", 24, color=WHITE_)
        selo = VGroup(cartao(selo, 0.16, cor=HEAT), selo).move_to(P3(0, 6.3))
        # 0–4 s · o acidente numa tomada rápida (carros entram, batem, ficam unidos e deslizam desenhando a marca)
        self.ancora("acidente")
        self.p(FadeIn(self.via), FadeIn(self.v1), FadeIn(self.v2), FadeIn(q1), FadeIn(q2), FadeIn(self.linha),
               FadeIn(self.bus), FadeIn(selo), FadeIn(self.marca), rt=0.4)
        self.p(self.tt.animate.set_value(0.0), *self.linha.ir(1), rt=1.1, rate_func=linear)
        c, an = self.anel_impacto()
        self.add(c)
        self.p(an, FadeOut(q1), FadeOut(q2), rt=0.4)
        self.remove(c, q1, q2)
        self.p(self.tt.animate.set_value(TSTOP), *self.linha.ir(2), rt=2.0, rate_func=linear)
        self.segue = False
        # 4–8 s · chegamos depois: a cena escurece um pouco, só resta a marca
        veu = Rectangle(width=XCENA - XL + 0.4, height=COL_Y1 - COL_Y0 + 0.4).move_to(P3((XL + XCENA) / 2, (COL_Y0 + COL_Y1) / 2)) \
            .set_fill(BACKGROUND_COLOR, 0.32).set_stroke(width=0).set_z_index(5)
        t1 = txt("DEPOIS DA BATIDA, SÓ RESTOU\nA MARCA NO ASFALTO.", 30).move_to(P3(0, -3.0))
        self.ancora("depois")
        self.p(FadeIn(veu), *self.linha.ir(3), FadeIn(t1, shift=0.1 * UP), rt=0.8)
        ct = self.cotas(sim=False)
        self.ancora("cotas")
        self.p(Create(ct["legs"]), FadeIn(ct["lx"].mt), FadeIn(ct["ly2"].mt), rt=0.9)
        self.p(FadeIn(ct["ld"].mt), FadeIn(ct["ang"]), FadeOut(veu), rt=0.7)
        self.ct = ct
        self.w(0.4)
        # 8–12 s · a pergunta do hook; depois, voltar no tempo (seta curva de PAROU para ANTES)
        self.ancora("pergunta")
        self.sai(t1, selo, rt=0.3)
        self.p(*self.cab("O QUE UMA MARCA NO ASFALTO\nCONSEGUE CONTAR SOBRE UMA BATIDA?", 30), rt=0.7)
        L = self.linha
        volta = CurvedArrow(P3(L.XS[3], L.y + 0.62), P3(L.XS[0], L.y + 0.62), angle=PI / 6, color=CYAN, stroke_width=3.5,
                            tip_length=0.2).set_z_index(25)
        t2 = txt("VAMOS VOLTAR NO TEMPO", 32, color=CYAN).move_to(P3(0, -3.0))
        self.ancora("volta")
        self.p(Create(volta), FadeIn(t2, shift=0.1 * UP), rt=1.0)
        self.w(0.3)
        self.p(FadeOut(volta), rt=0.3)
        # 12–18 s · o que se sabe: coluna de parâmetros, setas fantasma de onde vieram, hipóteses numa legenda
        colg = self.coluna()
        self.ancora("dados")
        self.sai(t2, rt=0.3)
        self.p(FadeIn(colg, shift=0.1 * LEFT), rt=0.8)
        for e in (self.d_m1, self.d_m2, self.d_mu, self.d_g):
            self.assenta(e)
        y1 = w2s(C1)[1]
        g1 = VGroup(DashedLine(w2s(P3(-5.5, C1[1])), w2s(P3(-2.6, C1[1])), dash_length=0.12).set_stroke(VEL, 3, opacity=0.8),
                    arrow(w2s(P3(-3.4, C1[1])), w2s(P3(-2.4, C1[1])), VEL, 3, tip=0.16))
        g2 = VGroup(DashedLine(w2s(P3(0, -7.9)), w2s(P3(0, -2.4)), dash_length=0.12).set_stroke(VEL, 3, opacity=0.8),
                    arrow(w2s(P3(0, -3.3)), w2s(P3(0, -2.3)), VEL, 3, tip=0.16))
        q1 = rotulo_v(r"\vec v_{1i}", "?", 32)
        q2 = rotulo_v(r"\vec v_{2i}", "?", 32)
        contorno(q1.mt.move_to(P3(XL, y1 + 0.42), aligned_edge=LEFT))
        contorno(q2.mt.next_to(w2s(P3(0, -5.6)), RIGHT, buff=0.2))
        self.p(Create(g1[0]), FadeIn(g1[1]), FadeIn(q1.mt), Create(g2[0]), FadeIn(g2[1]), FadeIn(q2.mt), rt=1.0)
        self.fantasmas = VGroup(g1, g2, q1.mt, q2.mt)
        self.hip = VGroup(txt("IMPACTO CURTO · MESMO ATRITO · MARCA RETA, A PARTIR DO IMPACTO", 18, color=WHITE_, op=0.85),
                          txt("MODELO IDEALIZADO, NÃO PERÍCIA", 18, color=DIM)).arrange(DOWN, buff=0.14).move_to(P3(0, -1.6))
        self.ancora("hipoteses")
        self.p(FadeIn(self.hip, shift=0.08 * UP), rt=0.6)
        self.w(1.0)

    # ================================================================ C02 · começar pelo fim
    def c02(self):
        self.ancora("fim")
        self.sai(self.fantasmas, self.hip, self.ct["g"], self.bus, rt=0.4)
        self.p(*self.cab("COMEÇAR PELO FIM"), *self.linha.ir(2), rt=0.6)
        self.ancora("conjunto")
        # o conjunto: M = m₁ + m₂ (as cópias de m₁ e m₂ viajam na coluna para formar M)
        self.eM = self.na_coluna(Eq([("M", "M"), ("eq", "="), ("a", "m_1"), ("p", "+"), ("b", "m_2")], 30), 2.3)
        self.eM2 = self.na_coluna(Eq([("eq", "="), ("v", "3000"), ("u", r"\,\mathrm{kg}")], 30), 1.88)
        self.eM2.mt.shift(RIGHT * 0.38)
        self.nasce(self.eM, [(self.d_m1.parte("s"), "a"), (self.d_m2.parte("s"), "b")], rt=0.8)
        self.nasce(self.eM2, [(VGroup(self.d_m1.parte("v"), self.d_m2.parte("v")), "v")], rt=0.7)
        # replay do deslizamento: o conjunto parte do impacto com v⃗_f (fantasma à frente) e para no fim da marca
        self.segue = True
        self.p(self.tt.animate.set_value(0.0), rt=0.8, rate_func=linear)
        c, an = self.anel_impacto(WHITE_)
        self.add(c)
        self.p(an, rt=0.3)
        self.remove(c)
        vfant = always_redraw(lambda: arrow(w2s(pos1(self.tt.get_value()) + UD * 3.0),
                                            w2s(pos1(self.tt.get_value()) + UD * (3.0 + 0.32 * vel_desl(self.tt.get_value()))),
                                            VEL, 4, tip=0.15, op=0.8, z=12))
        self.add(vfant)
        self.p(self.tt.animate.set_value(TSTOP), rt=2.0, rate_func=linear)
        vfant.clear_updaters()
        self.remove(vfant)
        self.segue = False
        # v⃗_f fica como fantasma no início do deslizamento, do lado de fora do triângulo da marca
        O = w2s(ORIGIN)
        nrm = P3(-UD[1], UD[0]) * 0.28
        self.vf_seta = seta_halo(O + nrm, O + nrm + UD * 1.15, VEL, 4, tip=0.15)
        self.vf_rot = rotulo_v(r"\vec v_f", "?", 30)
        self.vf_ponta = O + nrm + UD * 1.15
        contorno(self.vf_rot.mt.next_to(self.vf_ponta, UP + LEFT, buff=0.04)).set_z_index(14)
        self.ct = self.cotas(sim=True)
        self.p(GrowArrow(self.vf_seta[1]), FadeIn(self.vf_seta[0]), FadeIn(self.vf_rot.mt), FadeIn(self.ct["g"]), rt=0.7)
        self.assenta(self.vf_rot)
        # forças no deslizamento (vista lateral): peso, normal e atrito contra o movimento (cada uma uma vez)
        gy = -3.15
        chao = Line(P3(-4.0, gy), P3(-0.6, gy)).set_stroke(GEO, 2, opacity=0.7)
        bl = VGroup(Rectangle(width=0.75, height=0.7).set_fill(CAR1, 0.6).set_stroke(CAR1_L, 2),
                    Rectangle(width=0.55, height=0.7).set_fill(CAR2, 0.6).set_stroke(CAR2_L, 2)).arrange(RIGHT, buff=0)
        bl.move_to(P3(-2.3, gy + 0.35))
        rotM = MathTex("M", font_size=32, color=WHITE_).move_to(bl)
        fN = arrow(bl.get_top(), bl.get_top() + P3(0, 0.85), FC, 6, tip=0.18)
        fP = arrow(bl.get_center(), bl.get_center() + P3(0, -1.15), FC, 6, tip=0.18, z=11)
        fA = arrow(bl.get_corner(DL) + P3(0, 0.15), bl.get_corner(DL) + P3(-1.05, 0.15), FC, 6, tip=0.18)
        vv = arrow(bl.get_right() + P3(0.1, 0.12), bl.get_right() + P3(0.95, 0.12), VEL, 4, tip=0.15, op=0.75)
        lN = Eq([("N", "N", FC)], 32)
        contorno(lN.mt.next_to(fN.get_end(), LEFT, buff=0.12))
        lP = Eq([("P", "M g", FC)], 32)
        contorno(lP.mt.next_to(fP.get_end(), RIGHT, buff=0.12))
        lA = Eq([("f", "f_k", FC)], 32)
        contorno(lA.mt.next_to(fA, DOWN, buff=0.1))
        lv = contorno(MathTex(r"\vec v_f", font_size=28, color=VEL)).next_to(vv, DOWN, buff=0.12)
        tvl = txt("VISTA LATERAL", 16, color=DIM).move_to(P3(XL + 0.7, -1.2))
        diag = VGroup(chao, bl, rotM, fN, fP, fA, vv, lN.mt, lP.mt, lA.mt, lv, tvl)
        self.ancora("forcas")
        self.p(FadeIn(VGroup(chao, bl, rotM, tvl, vv, lv)), GrowArrow(fP), FadeIn(lP.mt), GrowArrow(fN), FadeIn(lN.mt), rt=0.9)
        eN = Eq([("N", "N", FC), ("eq", "="), ("M", "M"), ("g", "g")], 38, pos=P3(1.9, -1.55))
        self.nasce(eN, [(lN.parte("N"), "N"), (lP.parte("P"), ["M", "g"])], rt=0.8)
        self.ancora("atrito")
        self.p(GrowArrow(fA), FadeIn(lA.mt), rt=0.6)
        eF = Eq([("f", "f_k", FC), ("eq", "="), ("mu", r"\mu_k"), ("N", "N", FC)], 38, pos=P3(1.9, -2.4))
        self.nasce(eF, [(lA.parte("f"), "f"), (self.d_mu.parte("s"), "mu"), (eN.parte("N"), "N")], rt=0.9)
        eF2 = Eq([("f", "f_k", FC), ("eq", "="), ("mu", r"\mu_k"), ("M", "M"), ("g", "g")], 38, pos=P3(1.9, -2.4))
        self.substitui(eF, eF2, copias=[(VGroup(eN.parte("M"), eN.parte("g")), ["M", "g"])], rt=0.8)
        # trabalho do atrito (laranja): W = −f_k d → −μ_k M g d ; d é a cota da marca
        eW = Eq([("W", r"W_{\mathrm{at}}", HEAT), ("eq", "="), ("s", "-"), ("f", "f_k", FC), ("d", r"\,d", GEO)], 40,
                pos=P3(0, -4.45))
        self.ancora("trabalho")
        self.nasce(eW,[(eF2.parte("f"), "f"), (self.ct["ld"].parte("s"), "d")], rt=0.9)
        eW2 = Eq([("W", r"W_{\mathrm{at}}", HEAT), ("eq", "="), ("s", "-"), ("mu", r"\mu_k"), ("M", "M"), ("g", "g"),
                  ("d", r"\,d", GEO)], 40, pos=P3(0, -4.45))
        self.substitui(eW, eW2, copias=[(VGroup(eF2.parte("mu"), eF2.parte("M"), eF2.parte("g")), ["mu", "M", "g"])], rt=0.8)
        nota = txt("ENERGIA QUE O ATRITO TRANSFORMA EM CALOR", 17, color=HEAT, op=0.85).move_to(P3(0, -5.0))
        self.p(FadeIn(nota), rt=0.4)
        # ΔK = W: a variação da energia cinética é o trabalho do atrito (M da coluna, v_f da seta, W da linha acima)
        lei = txt("VARIAÇÃO DA ENERGIA CINÉTICA = TRABALHO DO ATRITO", 17, color=CYAN, op=0.9).move_to(P3(0, -5.85))
        e0 = Eq([("z", "0"), ("s1", "-"), ("h", r"\tfrac12"), ("M1", "M"), ("v", "v_f^2", VEL), ("eq", "="), ("s2", "-"),
                 ("mu", r"\mu_k"), ("M2", "M"), ("g", "g"), ("d", "d", GEO)], 48, pos=P3(0, -6.65))
        e0.parte(["z", "s1", "h", "M1", "v"]).set_color(CYAN)
        e0.parte("v").set_color(VEL)
        self.ancora("teorema")
        self.p(FadeIn(lei), rt=0.4)
        self.nasce(e0, [(self.eM.parte("M"), "M1"), (self.vf_rot.parte("v"), "v"),
                        (VGroup(eW2.parte("s"), eW2.parte("mu"), eW2.parte("M"), eW2.parte("g"), eW2.parte("d")),
                         ["s2", "mu", "M2", "g", "d"])], rt=1.1)
        self.w(0.6)
        # a álgebra sobe para o espaço livre (o diagrama e as linhas de apoio saem)
        self.sai(diag, eN, eF2, eW2, nota, lei, rt=0.5)
        Y = -1.75
        self.cardE = cartao(w=7.4, h=1.0, centro=P3(0, Y))
        self.p(e0.m.animate.move_to(P3(0, Y)), FadeIn(self.cardE), rt=0.7)
        # passo 1 (MF-Tools): os sinais de menos cancelam e o zero sai
        e1 = Eq([("h", r"\tfrac12"), ("M1", "M"), ("v", "v_f^2", VEL), ("eq", "="), ("mu", r"\mu_k"), ("M2", "M"), ("g", "g"),
                 ("d", "d", GEO)], 52, pos=P3(0, Y))
        self.ancora("sinais")
        self.passo(e0, e1, rt=1.1)
        # passo 2: M dos dois lados se corta e voa para fora
        rs = self.riscar(e1.parte("M1"), e1.parte("M2"))
        self.ancora("corta")
        self.p(Create(rs), *self.frase("A MASSA TOTAL CANCELA", 24, y=-2.75), rt=0.7)
        self.w(0.5)
        e2 = Eq([("h", r"\tfrac12"), ("v", "v_f^2", VEL), ("eq", "="), ("mu", r"\mu_k"), ("g", "g"), ("d", "d", GEO)], 52, pos=P3(0, Y))
        self.remove(rs)
        self.passo(e1, e2, ("M1", [], {"shift": UP * 0.7}), ("M2", [], {"shift": UP * 0.7}), rt=1.1,
                   extra=[FadeOut(rs, shift=UP * 0.7)])
        # passo 3: o ½ atravessa a igualdade e vira 2
        e3 = Eq([("v", "v_f^2", VEL), ("eq", "="), ("dois", "2"), ("mu", r"\mu_k"), ("g", "g"), ("d", "d", GEO)], 52, pos=P3(0, Y))
        self.ancora("meio")
        self.passo(e2, e3,("h", "dois", {"path_arc": -2.2}), rt=1.2)
        # passo 4: raiz dos dois lados
        e4 = Eq([("v", "v_f", VEL), ("eq", "="), ("r", r"\sqrt{2\mu_k g\, d}")], 52, pos=P3(0, Y))
        e4.gl[radicando(e4, "r")[-1]].set_color(GEO)
        self.ancora("raiz")
        self.passo(e3, e4,(("v", slice(0, 2)), "v"), (("v", 2), []), (["dois", "mu", "g", "d"], "r"), rt=1.1)
        self.sai(self._frase, rt=0.25)
        self._frase = None
        # substituição em fases: o esqueleto copia de e4; depois 0,50 e 10 da coluna e o 10 da cota pousam nos lugares vazios
        Y2 = -3.05
        e5 = Eq([("v", "v_f", VEL), ("eq", "="), ("r", r"\sqrt{2\cdot 0{,}50\cdot 10\cdot 10}"), ("eq2", "="),
                 ("res", r"10\,\mathrm{m/s}")], 46, pos=P3(0, Y2))
        cont5 = radicando(e5, "r")
        i_mu, i_g, i_d = cont5[2:6], cont5[7:9], cont5[10:12]
        for i in i_d:
            e5.gl[i].set_color(GEO)
        cont4 = radicando(e4, "r")
        esq4 = [i for i in e4.idx["r"] if i not in cont4] + [cont4[0]]
        esq5 = [i for i in e5.idx["r"] if i not in cont5] + [cont5[0]]
        self.ancora("numeros")
        self.substitui(e4, e5,pares=[(esq4, esq5)],
                       copias=[(self.d_mu.parte("v"), i_mu), (self.d_g.parte("v"), i_g), (self.ct["ld"].parte("n"), i_d)],
                       rt=1.2, manter=True)
        bx = caixa(e5.parte("res"), WHITE_, 0.1)
        self.p(Create(bx), rt=0.4)
        # o 10 m/s volta para a seta de v⃗_f
        nr = rotulo_v(r"\vec v_f", r"10\,\mathrm{m/s}", 30)
        contorno(nr.mt.next_to(self.vf_ponta, UP + LEFT, buff=0.04)).set_z_index(14)
        self.substitui(self.vf_rot, nr, copias=[(e5.parte("res"), "n")], rt=0.9)
        self.vf_rot = nr
        self.w(0.3)
        # componentes (só números): v_fx = 10·8/10 e v_fy = 10·6/10 (o 10 da seta, 8/6/10 das cotas)
        self.ancora("direcao")
        self.sai(e4, e5, bx, self.cardE, rt=0.4)
        ex = Eq([("vx", "v_{fx}", VEL), ("eq", "="), ("a", "10"), ("dot", r"\cdot"), ("fr", r"\dfrac{8}{10}", ("fr", GEO)),
                 ("eq2", "="), ("res", r"8\,\mathrm{m/s}")], 44, pos=P3(0, -1.85))
        ey = Eq([("vy", "v_{fy}", VEL), ("eq", "="), ("a", "10"), ("dot", r"\cdot"), ("fr", r"\dfrac{6}{10}", ("fr", GEO)),
                 ("eq2", "="), ("res", r"6\,\mathrm{m/s}")], 44, pos=P3(0, -3.35))
        self.nasce(ex, [(self.vf_rot.parte("n")[0:2], "a"), (self.ct["lx"].parte("n"), ex.num("fr")),
                        (self.ct["ld"].parte("n"), ex.den("fr"))], rt=0.9, depois=["eq2", "res"])
        self.nasce(ey, [(self.vf_rot.parte("n")[0:2], "a"), (self.ct["ly2"].parte("n"), ey.num("fr")),
                        (self.ct["ld"].parte("n"), ey.den("fr"))], rt=0.9, depois=["eq2", "res"])
        # os resultados entram na coluna (para o impacto)
        self.d_vx = self.na_coluna(Eq([("s", "v_{fx}", VEL), ("eq", "="), ("v", "8"), ("u", r"\,\mathrm{m/s}")], 30), 1.32)
        self.d_vy = self.na_coluna(Eq([("s", "v_{fy}", VEL), ("eq", "="), ("v", "6"), ("u", r"\,\mathrm{m/s}")], 30), 0.88)
        self.nasce(self.d_vx, [(ex.parte("vx"), "s"), (ex.parte("res"), ["v", "u"])], rt=0.8)
        self.nasce(self.d_vy, [(ey.parte("vy"), "s"), (ey.parte("res"), ["v", "u"])], rt=0.8)
        self.w(0.8)
        self.c02_fora = [ex, ey]

    # ================================================================ C03 · voltar ao impacto
    def c03(self):
        self.ancora("impacto")
        self.sai(*self.c02_fora, self.vf_seta, self.vf_rot, self.ct["g"], rt=0.4)
        self.p(*self.cab("VOLTAR AO IMPACTO"), *self.linha.ir(1), rt=0.5)
        # congelar o instante antes do choque
        self.p(self.tt.animate.set_value(T0), rt=1.4, rate_func=linear)
        setas, r1, r2 = self.setas_antes()
        self.p(*[GrowArrow(s[1]) for s in setas], *[FadeIn(s[0]) for s in setas], FadeIn(r1.mt), FadeIn(r2.mt), rt=0.6)
        self.assenta(r1), self.assenta(r2)
        self.setas, self.r1, self.r2 = setas, r1, r2
        # a lei do impacto e por que ela vale só no impacto
        fase = VGroup(txt("IMPACTO:", 24), txt("MOMENTO", 24, color=MAG)).arrange(RIGHT, buff=0.18).move_to(P3(0, -1.1))
        s1 = txt("IMPACTO CURTÍSSIMO:\nIMPULSO EXTERNO DESPREZÍVEL", 18)
        s2 = txt("VÁRIOS METROS DESLIZANDO:\nATRITO NÃO DESPREZÍVEL", 18, color=DIM)
        s1.move_to(P3(-2.05, -2.0))
        s2.move_to(P3(2.05, -2.0))
        b1, b2 = caixa(s1, MAG, 0.12, 2.0), caixa(s2, DIM, 0.12, 1.6, 0.7)
        vs = MathTex(r"\times", font_size=34, color=DIM).move_to(P3(0, -2.0))
        self.ancora("conserva")
        self.p(FadeIn(fase), FadeIn(VGroup(s1, b1)), rt=0.6)
        self.p(FadeIn(VGroup(s2, b2)), FadeIn(vs), rt=0.6)
        self.w(0.8)
        self.ancora("momento")
        self.sai(VGroup(s1, b1, s2, b2, vs), rt=0.4)
        # momentos: p⃗ = m v⃗ (m do carro, v⃗ da seta); no mapa, p⃗₁ᵢ abaixo do carro 1 e p⃗₂ᵢ à esquerda do carro 2
        ep1 = Eq([("p", r"\vec p_{1i}", MAG), ("eq", "="), ("m", "m_1"), ("v", r"\vec v_{1i}", VEL)], 40, pos=P3(-2.05, -2.0))
        ep2 = Eq([("p", r"\vec p_{2i}", MAG), ("eq", "="), ("m", "m_2"), ("v", r"\vec v_{2i}", VEL)], 40, pos=P3(2.05, -2.0))
        a1 = w2s(pos1(T0) + P3(-L1 / 2 + 0.3, -W1 / 2 - 0.9))
        a2 = w2s(pos2(T0) + P3(-W2 / 2 - 0.9, -L2 / 2 + 0.3))
        pq1 = arrow(a1, a1 + P3(1.1, 0), MAG, 5, tip=0.16, op=0.6)
        pq2 = arrow(a2, a2 + P3(0, 1.1), MAG, 5, tip=0.16, op=0.6)
        self.nasce(ep1, [(self.v1.rot, "m"), (r1.parte("v"), "v")], rt=0.9, extra=[GrowArrow(pq1)])
        self.nasce(ep2, [(self.v2.rot, "m"), (r2.parte("v"), "v")], rt=0.9, extra=[GrowArrow(pq2)])
        # P⃗ᵢ = p⃗₁ᵢ + p⃗₂ᵢ ; depois do choque, P⃗_f = M v⃗_f ao longo da marca ; P⃗ᵢ = P⃗_f — numa só passada
        ePi = Eq([("P", r"\vec P_i", MAG), ("eq", "="), ("a", r"\vec p_{1i}", MAG), ("pl", "+"), ("b", r"\vec p_{2i}", MAG)], 40,
                 pos=P3(-2.05, -2.85))
        ePf = Eq([("P", r"\vec P_f", MAG), ("eq", "="), ("M", "M"), ("v", r"\vec v_f", VEL)], 40, pos=P3(2.05, -2.85))
        O, X_, Q_ = w2s(ORIGIN), w2s(P3(DX, 0)), w2s(P3(DX, DY))
        Pf = seta_halo(O, Q_, MAG, 6, tip=0.2, z=13)
        lPf = contorno(MathTex(r"\vec P_f", font_size=32, color=MAG)).move_to(w2s(P3(3.0, 3.6))).set_z_index(14)
        self.ancora("total")
        self.nasce(ePi, [(ep1.parte("p"), "a"), (ep2.parte("p"), "b")], rt=0.9)
        self.nasce(ePf, [(self.eM.parte("M"), "M")], rt=0.8, extra=[GrowArrow(Pf[1]), FadeIn(Pf[0]), FadeIn(lPf)])
        eIg = Eq([("a", r"\vec P_i", MAG), ("eq", "="), ("b", r"\vec P_f", MAG)], 46, pos=P3(0, -3.7))
        self.nasce(eIg, [(ePi.parte("P"), "a"), (ePf.parte("P"), "b")], rt=0.8)
        # componentes: projeções de P⃗ nos eixos dão p₁ᵢ (x) e p₂ᵢ (y)
        pr = DashedLine(Q_, X_, dash_length=0.07).set_stroke(MAG, 2, opacity=0.7)
        px = arrow(O, X_, MAG_L, 5, tip=0.16, z=12)
        py = arrow(X_, Q_, MAG_L, 5, tip=0.16, z=12)
        lpx = contorno(MathTex(r"p_{1i}", font_size=32, color=MAG)).next_to(px, DOWN, buff=0.06).set_z_index(14)
        lpy = contorno(MathTex(r"p_{2i}", font_size=32, color=MAG)).next_to(w2s(P3(DX + W2 / 2 + 0.2, 1.8)), RIGHT, buff=0.04)
        lpy.set_z_index(14)
        self.ancora("direcoes")
        self.p(Create(pr), GrowArrow(px), GrowArrow(py), FadeIn(lpx), FadeIn(lpy), FadeOut(pq1), FadeOut(pq2), rt=0.9)
        # as linhas de apoio saem; P⃗ᵢ = P⃗_f sobe e deixa o caminho livre para as componentes
        self.sai(ep1, ep2, ePi, ePf, rt=0.35)
        self.p(eIg.m.animate.move_to(P3(0, -1.95)), rt=0.5)
        YX, YY = -4.75, -6.45
        tx = MathTex("x:", font_size=30, color=DIM).move_to(P3(XL + 0.15, YX))
        ty = MathTex("y:", font_size=30, color=DIM).move_to(P3(XL + 0.15, YY))
        X1 = Eq([("m1", "m_1"), ("v", "v_{1i}", VEL), ("eq", "="), ("M", "M"), ("vx", "v_{fx}", VEL)], 46, pos=P3(0.2, YX))
        Y1 = Eq([("m1", "m_2"), ("v", "v_{2i}", VEL), ("eq", "="), ("M", "M"), ("vx", "v_{fy}", VEL)], 46, pos=P3(0.2, YY))
        self.p(FadeIn(tx), FadeIn(ty), rt=0.3)
        copX = [TransformFromCopy(lpx, X1.parte(["m1", "v"])), TransformFromCopy(self.eM.parte("M"), X1.parte("M")),
                TransformFromCopy(self.d_vx.parte("s"), X1.parte("vx")), TransformFromCopy(lpy, Y1.parte(["m1", "v"])),
                TransformFromCopy(self.eM.parte("M"), Y1.parte("M")), TransformFromCopy(self.d_vy.parte("s"), Y1.parte("vx"))]
        self.p(*copX, rt=1.0)
        self.p(FadeIn(X1.parte("eq")), FadeIn(Y1.parte("eq")), rt=0.3)
        self.assenta(X1), self.assenta(Y1)
        self.w(0.6)
        # isolar v₁ᵢ e v₂ᵢ em paralelo (MF-Tools): m₁ (m₂) atravessa a igualdade e vira denominador
        X2 = Eq([("v", "v_{1i}", VEL), ("eq", "="), ("fr", r"\dfrac{M}{m_1}"), ("vx", "v_{fx}", VEL)], 46, pos=P3(0.2, YX))
        Y2 = Eq([("v", "v_{2i}", VEL), ("eq", "="), ("fr", r"\dfrac{M}{m_2}"), ("vx", "v_{fy}", VEL)], 46, pos=P3(0.2, YY))
        self.ancora("isolar")
        self.passos([(X1, X2, (("m1", X2.den("fr"), {"path_arc": 1.6}), ("M", X2.num("fr"))), {}),
                     (Y1, Y2, (("m1", Y2.den("fr"), {"path_arc": 1.6}), ("M", Y2.num("fr"))), {})], rt=1.3)
        self.w(0.4)
        # números da coluna pousam nos lugares (M = 3000; m₁ = 2000; m₂ = 1000; v_fx = 8; v_fy = 6)
        X3 = Eq([("v", "v_{1i}", VEL), ("eq", "="), ("fr", r"\dfrac{3000}{2000}"), ("dot", r"\cdot"), ("n", "8")], 46, pos=P3(0.2, YX))
        Y3 = Eq([("v", "v_{2i}", VEL), ("eq", "="), ("fr", r"\dfrac{3000}{1000}"), ("dot", r"\cdot"), ("n", "6")], 46, pos=P3(0.2, YY))
        self.p(*[Indicate(m, color=WHITE_, scale_factor=1.12) for m in (self.eM2.parte("v"), self.d_m1.parte("v"),
                                                                        self.d_m2.parte("v"))], rt=0.5)
        X4 = Eq([("v", "v_{1i}", VEL), ("eq", "="), ("res", r"12\,\mathrm{m/s}")], 50, pos=P3(0.2, YX))
        Y4 = Eq([("v", "v_{2i}", VEL), ("eq", "="), ("res", r"18\,\mathrm{m/s}")], 50, pos=P3(0.2, YY))
        # carro azul: os números pousam e a conta vira número (a fração sai, o resultado entra)
        self.ancora("azul")
        self.p(Y2.m.animate.set_opacity(0.3), rt=0.2)
        self.substitui(X2, X3, pares=[(X2.barra("fr"), X3.barra("fr"))],
                       copias=[(self.eM2.parte("v"), X3.num("fr")), (self.d_m1.parte("v"), X3.den("fr")), (self.d_vx.parte("v"), "n")],
                       rt=1.1)
        self.w(0.4)
        self.substitui(X3, X4, rt=0.5)
        # carro violeta (a linha de x esmaece enquanto os números atravessam)
        self.ancora("violeta")
        self.p(X4.m.animate.set_opacity(0.25), Y2.m.animate.set_opacity(1.0), rt=0.2)
        self.substitui(Y2, Y3, pares=[(Y2.barra("fr"), Y3.barra("fr"))],
                       copias=[(self.eM2.parte("v"), Y3.num("fr")), (self.d_m2.parte("v"), Y3.den("fr")), (self.d_vy.parte("v"), "n")],
                       rt=1.0)
        self.w(0.4)
        self.substitui(Y3, Y4, rt=0.5)
        self.p(X4.m.animate.set_opacity(1.0), rt=0.2)
        # fechar o laço: os resultados voltam para as setas e entram na coluna
        n1 = rotulo_v(r"\vec v_{1i}", r"12\,\mathrm{m/s}", 32)
        n2 = rotulo_v(r"\vec v_{2i}", r"18\,\mathrm{m/s}", 32)
        contorno(n1.mt.move_to(r1.mt, aligned_edge=LEFT)).set_z_index(14)
        contorno(n2.mt.move_to(r2.mt, aligned_edge=LEFT)).set_z_index(14)
        self.substitui(r1, n1, copias=[(X4.parte("res"), "n")], rt=0.7)
        self.p(X4.m.animate.set_opacity(0.25), rt=0.2)
        self.substitui(r2, n2, copias=[(Y4.parte("res"), "n")], rt=0.7)
        self.r1, self.r2 = n1, n2
        self.d_v1 = self.na_coluna(Eq([("s", "v_{1i}", VEL), ("eq", "="), ("v", "12"), ("u", r"\,\mathrm{m/s}")], 30), 0.4)
        self.d_v2 = self.na_coluna(Eq([("s", "v_{2i}", VEL), ("eq", "="), ("v", "18"), ("u", r"\,\mathrm{m/s}")], 30), -0.04)
        self.p(X4.m.animate.set_opacity(1.0), rt=0.2)
        self.nasce(self.d_v1, [(X4.parte("v"), "s"), (X4.parte("res"), ["v", "u"])], rt=0.7)
        self.p(X4.m.animate.set_opacity(0.25), rt=0.2)
        self.nasce(self.d_v2, [(Y4.parte("v"), "s"), (Y4.parte("res"), ["v", "u"])], rt=0.7)
        self.p(X4.m.animate.set_opacity(1.0), rt=0.2)
        X5 = Eq([("v", "v_{1i}", VEL), ("eq", "="), ("res", r"12\,\mathrm{m/s}"), ("eq2", "="), ("k", r"43{,}2\,\mathrm{km/h}")],
                44, pos=P3(0.15, YX))
        Y5 = Eq([("v", "v_{2i}", VEL), ("eq", "="), ("res", r"18\,\mathrm{m/s}"), ("eq2", "="), ("k", r"64{,}8\,\mathrm{km/h}")],
                44, pos=P3(0.15, YY))
        self.sai(tx, ty, rt=0.25)
        self.passos([(X4, X5, (), {}), (Y4, Y5, (), {})], rt=0.8)
        self.w(1.0)
        self.c03_fora = [fase, eIg, X5, Y5, Pf, lPf, pr, px, py, lpx, lpy]

    # ================================================================ C04 · o triângulo e a pegadinha
    def c04(self):
        self.ancora("pegadinha")
        mk = marca_mob(w2s(ORIGIN), w2s(UD * D), w=3.0, sep=0.05)
        self.add(mk)
        self.remove(self.marca)
        for m in (self.v1, self.v2):
            m.clear_updaters()
        mchip = self.eM2.parte("v").copy()
        self.add(mchip)
        self.sai(*self.c03_fora, self.setas, self.r1, self.r2, rt=0.4)
        # cena e coluna recolhem; a marca vira o 1º dos três triângulos
        Om, sm = P3(-3.85, 2.35), 0.27
        Xm, Qm = Om + P3(8 * sm, 0), Om + P3(8 * sm, 6 * sm)
        hm = marca_mob(Om, Qm, w=3.5, sep=0.06)
        lgm = VGroup(DashedLine(Om, Xm, dash_length=0.08), DashedLine(Xm, Qm, dash_length=0.08)).set_stroke(GEO, 2, opacity=0.8)
        lm = [lab_at(MathTex(r"8\,\mathrm{m}", font_size=32, color=GEO), Om, Xm, lado=-1),
              lab_at(MathTex(r"6\,\mathrm{m}", font_size=32, color=GEO), Xm, Qm, lado=-1),
              lab_at(MathTex(r"10\,\mathrm{m}", font_size=32, color=GEO), Om, Qm, lado=1, gap=0.18)]
        am = arco(Om, 0.45, 0, TH, w=2.2)
        tmar = txt("MARCA", 24, color=GEO).move_to(P3(2.75, 3.75))
        tri_m = VGroup(hm, lgm, *lm, am)
        fora = [self.via, self.v1, self.v2, self.col, self.f1, self.f2, *[e.m for e in (self.d_m1, self.d_m2, self.d_mu, self.d_g,
                self.eM, self.d_vx, self.d_vy, self.d_v1, self.d_v2)]]
        self.p(*self.cab("O TRIÂNGULO E A PEGADINHA"), rt=0.4)
        self.p(*[FadeOut(m) for m in fora], FadeOut(self.eM2.m), ReplacementTransform(mk, hm), FadeIn(lgm),
               *[FadeIn(x) for x in lm], FadeIn(am), FadeIn(tmar), mchip.animate.move_to(P3(3.45, -0.75)), rt=1.1)
        self.remove(*fora, self.eM2.m)
        # velocidade (violeta) e momento (magenta): mesmo triângulo, outra escala
        nv = [MathTex(r"8\,\mathrm{m/s}", font_size=38), MathTex(r"6\,\mathrm{m/s}", font_size=38),
              MathTex(r"10\,\mathrm{m/s}", font_size=38)]
        tv = self.tri(P3(-3.95, -1.75), 0.56, VEL, VEL_L, nv, 0.8)
        tvel = txt("VELOCIDADE", 24, color=VEL).move_to(P3(2.75, 1.3))
        self.p(TransformFromCopy(VGroup(Line(Om, Xm), Line(Xm, Qm), Line(Om, Qm)), VGroup(tv["hx"], tv["hy"], tv["hh"])),
               TransformFromCopy(VGroup(*lm), VGroup(tv["lx"], tv["ly"], tv["lh"])), TransformFromCopy(am, tv["ang"]),
               FadeIn(tvel), rt=1.0)
        seta_m = arrow(P3(2.75, 0.85), P3(2.75, -2.35), DIM, 2.5, tip=0.16)
        xM = MathTex(r"\times", font_size=34, color=WHITE_).next_to(mchip, LEFT, buff=0.08)
        nm = [Eq([("p", "p_{1i}", MAG), ("eq", "="), ("n", r"24\,000")], 38),
              Eq([("p", "p_{2i}", MAG), ("eq", "="), ("n", r"18\,000")], 38),
              Eq([("p", "P", MAG), ("eq", "="), ("n", r"30\,000")], 38)]
        tp = self.tri(P3(-3.95, -6.25), 0.6, MAG, MAG_L, [e.mt for e in nm], 0.85)
        tmom = VGroup(txt("MOMENTO", 24, color=MAG), MathTex(r"(\mathrm{kg\cdot m/s})", font_size=28, color=DIM)) \
            .arrange(DOWN, buff=0.1).move_to(P3(2.75, -2.95))
        self.p(GrowArrow(seta_m), FadeIn(xM), rt=0.5)
        self.p(GrowArrow(tp["hx"]), GrowArrow(tp["hy"]), GrowArrow(tp["hh"]), Create(tp["ang"]), FadeIn(tmom), rt=0.9)
        self.p(*[FadeIn(e.mt, shift=0.08 * UP) for e in nm], rt=0.6)
        for e in nm:
            self.assenta(e)
        self.p(*[Indicate(a, color=WHITE_, scale_factor=1.3) for a in (am, tv["ang"], tp["ang"])],
               *self.frase("A MESMA DIREÇÃO\nATRAVESSA AS ETAPAS", 20, y=2.6, x=2.75, width=2.5), rt=0.9)
        self.w(0.8)
        self.ancora("tangente")
        # tan θ: os catetos do triângulo de momento voam para a fração (a linha da velocidade cede o lugar)
        self.sai(tv["g"], tvel, seta_m, xM, mchip, rt=0.4)
        tg = Eq([("t", r"\tan\theta"), ("eq", "="), ("fr", r"\dfrac{p_{2i}}{p_{1i}}", ("fr", MAG)), ("eq2", "="),
                 ("fr2", r"\dfrac{18\,000}{24\,000}"), ("eq3", "="), ("fr3", r"\dfrac34")], 46, pos=P3(0, -0.45))
        self.nasce(tg, [(nm[1].parte("p"), tg.num("fr")), (nm[0].parte("p"), tg.den("fr")),
                        (nm[1].parte("n"), tg.num("fr2")), (nm[0].parte("n"), tg.den("fr2"))], rt=1.0,
                   extra=[FadeIn(cartao(w=8.0, h=1.3, centro=P3(0, -0.45)))], depois=["eq3", "fr3"])
        self.w(1.2)
        cards = [m for m in self.mobjects if isinstance(m, RoundedRectangle)]
        self.sai(tri_m, tmar, tp["g"], *nm, tmom, tg, self._frase, *cards, rt=0.4)
        self._frase = None
        self.ancora("barras")
        # contraste: quem é mais rápido × quem tem mais momento
        YB_ = -3.8
        hv = txt("VELOCIDADE", 26, color=VEL).move_to(P3(-2.25, 2.65))
        hp = VGroup(txt("MOMENTO", 26, color=MAG), MathTex(r"(\mathrm{kg\cdot m/s})", font_size=28, color=DIM)) \
            .arrange(RIGHT, buff=0.12).move_to(P3(2.25, 2.65))
        base = VGroup(Line(P3(-3.95, YB_), P3(-0.5, YB_)), Line(P3(0.5, YB_), P3(3.95, YB_))).set_stroke(DIM, 2, opacity=0.6)

        def barra(x, alt, cor, val):
            r = Rectangle(width=1.15, height=alt).set_stroke(mix(cor, 0.4), 1.5).set_fill(cor, 0.85)
            r.move_to(P3(x, YB_ + alt / 2))
            return r, MathTex(val, font_size=38, color=WHITE_).next_to(r, UP, buff=0.14)
        kv, kp = 5.0 / 18, 5.0 / 24000
        bv1, lv1 = barra(-3.0, V1I * kv, VEL, r"12\,\mathrm{m/s}")
        bv2, lv2 = barra(-1.5, V2I * kv, VEL, r"18\,\mathrm{m/s}")
        bp1, lp1 = barra(1.5, P1I * kp, MAG, r"24\,000")
        bp2, lp2 = barra(3.0, P2I * kp, MAG, r"18\,000")
        nb = VGroup(*[ficha(n, c, 0.2).move_to(P3(x, YB_ - 0.42)) for n, c, x in
                      ((1, CAR1, -3.0), (2, CAR2, -1.5), (1, CAR1, 1.5), (2, CAR2, 3.0))])
        self.p(FadeIn(hv), FadeIn(hp), Create(base), FadeIn(nb), rt=0.5)
        self.p(GrowFromEdge(bv1, DOWN), GrowFromEdge(bv2, DOWN), FadeIn(lv1), FadeIn(lv2), rt=0.8)
        self.p(GrowFromEdge(bp1, DOWN), GrowFromEdge(bp2, DOWN), FadeIn(lp1), FadeIn(lp2), rt=0.8)
        cv = txt("CARRO 2:\nMAIS RÁPIDO", 21, color=VEL).move_to(P3(-2.25, -5.05))
        cp = txt("CARRO 1:\nMAIS MOMENTO", 21, color=MAG).move_to(P3(2.25, -5.05))
        self.p(Create(caixa(VGroup(bv2, lv2), VEL, 0.1, 2.2)), FadeIn(cv), rt=0.6)
        self.p(Create(caixa(VGroup(bp1, lp1), MAG, 0.1, 2.2)), FadeIn(cp), rt=0.6)
        self.p(*self.frase("A DIREÇÃO DOS DESTROÇOS DÁ A RAZÃO\nDOS MOMENTOS, NÃO DAS VELOCIDADES", 25, y=-6.3), rt=0.7)
        self.w(1.6)

    def tri(self, O, s, cor, cor_l, nomes, r_arc):
        """Triângulo 3–4–5 de vetores: perna x, perna y e hipotenusa; arco em O."""
        O = np.asarray(O, float)
        X, Q = O + P3(8 * s, 0), O + P3(8 * s, 6 * s)
        hx = arrow(O, X, cor_l, 5, tip=0.19)
        hy = arrow(X, Q, cor_l, 5, tip=0.19)
        hh = arrow(O, Q, cor, 7, tip=0.22, z=9)
        lx = lab_at(nomes[0], O, X, lado=-1)
        ly = lab_at(nomes[1], X, Q, lado=-1)
        lh = lab_at(nomes[2], O, Q, lado=1, gap=0.2)
        ang = arco(O, r_arc, 0, TH, w=2.2)
        return dict(hx=hx, hy=hy, hh=hh, lx=lx, ly=ly, lh=lh, ang=ang, O=O, X=X, Q=Q, g=VGroup(hx, hy, hh, lx, ly, lh, ang))

    def coluna_de_volta(self):
        """A coluna lateral volta (C05–C06) com o que já se sabe."""
        eqs = (self.d_m1, self.d_m2, self.d_mu, self.d_g, self.eM, self.eM2, self.d_vx, self.d_vy, self.d_v1, self.d_v2)
        return [FadeIn(self.col), FadeIn(self.f1), FadeIn(self.f2)] + [FadeIn(e.m) for e in eqs]

    # ================================================================ C05 · conferência de ida e volta
    def c05(self):
        self.ancora("ida")
        fora = [m for m in self.mobjects if m not in self.fixos | {self.linha, self.head}]
        self.sai(*fora, rt=0.4)
        self._frase = None
        self.tt.set_value(T0)
        self.segue = False
        self.ligar_carros()
        setas, r1, r2 = self.setas_antes(r"12\,\mathrm{m/s}", r"18\,\mathrm{m/s}")
        self.ct = self.cotas(sim=True)
        self.p(*self.linha.ir(0), *self.cab("CONFERÊNCIA DE IDA E VOLTA"), FadeIn(self.via), FadeIn(self.marca), FadeIn(self.v1), FadeIn(self.v2),
               FadeIn(setas), FadeIn(r1.mt), FadeIn(r2.mt), *self.coluna_de_volta(), rt=0.7)
        self.assenta(r1), self.assenta(r2)
        ys = (-1.3, -2.0, -2.7)
        l1 = Eq([("a", r"\vec v_{1i}", VEL), ("b", r"=12,\ "), ("c", r"\vec v_{2i}", VEL), ("d", r"=18\ (\mathrm{m/s})")], 34,
                pos=P3(0, ys[0]))
        l2 = Eq([("a", r"\vec P_i", MAG), ("b", r"=(24\,000;\ 18\,000)\ \mathrm{kg\cdot m/s}")], 34, pos=P3(0, ys[1]))
        l3 = Eq([("a", r"\vec v_f", VEL), ("b", "="), ("c", r"\vec P_i", MAG), ("d", r"/M=(8;\ 6)\ \mathrm{m/s}")], 34, pos=P3(0, ys[2]))
        l4 = Eq([("d", "d", GEO), ("b", "="), ("c", r"v_f^2", VEL), ("e", r"/(2\mu_k g)="), ("n", r"10", GEO), ("u", r"\,\mathrm{m}", GEO)],
                48, pos=P3(0, -3.85))
        self.p(FadeIn(l1.mt, shift=0.08 * UP), rt=0.4)
        self.assenta(l1)
        self.p(FadeOut(setas), FadeOut(r1.m), FadeOut(r2.m), self.tt.animate.set_value(0.0), *self.linha.ir(1),
               rt=0.9, rate_func=linear)
        c, an = self.anel_impacto()
        self.add(c)
        self.p(an, l1.m.animate.set_opacity(0.4), FadeIn(l2.mt, shift=0.08 * UP), rt=0.5)
        self.remove(c)
        self.assenta(l2)
        self.p(l2.m.animate.set_opacity(0.4), FadeIn(l3.mt, shift=0.08 * UP), rt=0.5)
        self.assenta(l3)
        rastro = always_redraw(lambda: marca_mob(w2s(ORIGIN), w2s(UD * s_desl(self.tt.get_value())), w=2.2, sep=0.05,
                                                 cor=VEL, op=1.0).set_z_index(2))
        self.add(rastro)
        self.p(self.tt.animate.set_value(TSTOP), *self.linha.ir(2), l3.m.animate.set_opacity(0.4), rt=1.8, rate_func=linear)
        rastro.clear_updaters()
        cardl4 = cartao(l4.mt, 0.18)
        self.p(*self.linha.ir(3), FadeIn(l4.mt, shift=0.08 * UP), FadeIn(cardl4), rt=0.6)
        self.assenta(l4)
        # as linhas de apoio saem; o d calculado voa para a cota da marca, que pisca com ✓
        self.sai(l1, l2, l3, rt=0.3)
        alvo = self.ct["ld"]
        ok = contorno(MathTex(r"\checkmark", font_size=48, color=WHITE_)).next_to(alvo.mt, LEFT, buff=0.12).set_z_index(16)
        self.p(TransformFromCopy(VGroup(l4.parte("d"), l4.parte("n"), l4.parte("u")), alvo.mt), rt=0.8)
        self.assenta(alvo)
        self.p(Indicate(alvo.m, color=WHITE_, scale_factor=1.25), FadeIn(ok), rt=0.6)
        self.w(0.9)
        self.rastro = rastro

    # ================================================================ C06 · e a energia?
    def c06(self):
        self.ancora("energia")
        mk = marca_mob(w2s(ORIGIN), w2s(UD * D), w=3.0, sep=0.05)
        self.add(mk)
        self.remove(self.marca)
        for m in (self.v1, self.v2):
            m.clear_updaters()
        manter = {self.linha, self.head, self.via, mk, self.v1, self.v2, self.col, self.f1, self.f2,
                  *[e.m for e in (self.d_m1, self.d_m2, self.d_mu, self.d_g, self.eM, self.eM2, self.d_vx, self.d_vy,
                                  self.d_v1, self.d_v2)]}
        fora = [m for m in self.mobjects if m not in self.fixos | manter]
        self.sai(*fora, rt=0.4)
        q = txt("O MOMENTO SE CONSERVOU. E A ENERGIA?", 24).move_to(P3(0, -1.05))
        self.p(*self.cab("E A ENERGIA?"), FadeIn(q, shift=0.08 * UP), rt=0.6)
        self.ancora("kantes")
        # K_antes: m e v viajam da coluna
        YA = -1.9
        eA = Eq([("K", r"K_{\mathrm{antes}}", CYAN), ("eq", "="), ("h1", r"\tfrac12"), ("m1", "m_1"), ("v1", "v_{1i}^2", VEL),
                 ("pl", "+"), ("h2", r"\tfrac12"), ("m2", "m_2"), ("v2", "v_{2i}^2", VEL)], 42, pos=P3(0, YA))
        self.nasce(eA, [(self.d_m1.parte("s"), "m1"), (self.d_v1.parte("s"), ("v1", slice(0, 3))), (self.d_m2.parte("s"), "m2"),
                        (self.d_v2.parte("s"), ("v2", slice(0, 3)))], rt=0.9)
        eA2 = Eq([("K", r"K_{\mathrm{antes}}", CYAN), ("eq", "="), ("h1", r"\tfrac12"), ("m1", r"\cdot 2000\cdot"), ("v1", "12^2"),
                  ("pl", "+"), ("h2", r"\tfrac12"), ("m2", r"\cdot 1000\cdot"), ("v2", "18^2")], 40, pos=P3(0, YA))
        self.substitui(eA, eA2, pares=[(("v1", 3), ("v1", 2)), (("v2", 3), ("v2", 2))],
                       copias=[(self.d_m1.parte("v"), ("m1", slice(1, 5))), (self.d_v1.parte("v"), ("v1", slice(0, 2))),
                               (self.d_m2.parte("v"), ("m2", slice(1, 5))), (self.d_v2.parte("v"), ("v2", slice(0, 2)))], rt=1.0)
        eA3 = Eq([("K", r"K_{\mathrm{antes}}", CYAN), ("eq", "="), ("a", r"144", CAR1_L), ("pl", "+"), ("b", "162", CAR2_L),
                  ("eq2", "="), ("t", r"306\,\mathrm{kJ}", CYAN)], 44, pos=P3(0, YA))
        self.passo(eA2, eA3, (["h1", "m1", "v1"], "a"), (["h2", "m2", "v2"], "b"), rt=1.0)
        # barras (mesma escala): as parcelas viajam para a barra
        KS, X0 = 0.025, -3.8
        YBa, YBd = -2.95, -4.7

        def seg(k0, k1, y, cor, op=0.85):
            r = Rectangle(width=(k1 - k0) * KS, height=0.55).set_stroke(mix(cor, 0.4), 1.5).set_fill(cor, op)
            return r.move_to(P3(X0 + (k0 + k1) / 2 * KS, y))
        a1, a2 = seg(0, 144, YBa, CAR1), seg(144, 306, YBa, CAR2)
        ta1 = MathTex("144", font_size=32, color=WHITE_).move_to(a1)
        ta2 = MathTex("162", font_size=32, color=WHITE_).move_to(a2)
        self.p(GrowFromEdge(a1, LEFT), GrowFromEdge(a2, LEFT), rt=0.7)
        self.p(TransformFromCopy(eA3.parte("a"), ta1), TransformFromCopy(eA3.parte("b"), ta2), rt=0.7)
        self.ancora("kdepois")
        # K_depois: M e v_f viajam da coluna (v_f = 10 m/s)
        YD = -3.85
        eD = Eq([("K", r"K_{\mathrm{depois}}", CYAN), ("eq", "="), ("h", r"\tfrac12"), ("M", "M"), ("v", "v_f^2", VEL), ("eq2", "="),
                 ("h2", r"\tfrac12\cdot 3000\cdot 10^2"), ("eq3", "="), ("t", r"150\,\mathrm{kJ}", CYAN)], 40, pos=P3(0, YD))
        hh2 = sorted(eD.idx["h2"], key=lambda i: eD.gl[i].get_left()[0])
        self.nasce(eD, [(self.eM.parte("M"), "M"), (self.eM2.parte("v"), hh2[4:8])], rt=0.9, depois=["eq3", "t"])
        d1 = seg(0, 150, YBd, CYAN, 0.75)
        td = MathTex("150", font_size=32, color=BACKGROUND_COLOR).move_to(d1)
        self.p(GrowFromEdge(d1, LEFT), rt=0.6)
        self.p(FadeIn(td), rt=0.3)
        self.ancora("metade")
        # o que falta: 156 kJ convertidos (laranja)
        fal = seg(150, 306, YBa, HEAT, 0.0).set_stroke(HEAT, 3)
        self.p(Create(fal), rt=0.4)
        laranja = seg(150, 306, YBd, HEAT, 0.88)
        self.p(ReplacementTransform(fal, laranja), rt=0.8)
        eDK = Eq([("dk", r"\Delta K", HEAT), ("eq", "="), ("a", r"K_{\mathrm{antes}}", CYAN), ("m", "-"), ("b", r"K_{\mathrm{depois}}", CYAN),
                  ("eq2", "="), ("t", r"156\,\mathrm{kJ}\approx 51\,\%", HEAT)], 40, pos=P3(0, -5.65))
        self.p(Indicate(eA3.parte("K"), color=CYAN, scale_factor=1.12), Indicate(eD.parte("K"), color=CYAN, scale_factor=1.12),
               rt=0.5)
        self.nasce(eDK, rt=0.6, extra=[FadeIn(cartao(w=8.1, h=0.85, centro=P3(0, -5.65), cor=HEAT))], depois=["eq2", "t"])
        destinos = txt("DEFORMAÇÃO · CALOR · SOM · VIBRAÇÃO", 22, color=HEAT).move_to(P3(0, -6.4))
        self.p(FadeIn(destinos, shift=0.08 * DOWN), rt=0.6)
        self.ancora("frase")
        self.p(*self.frase("MOMENTO SE CONSERVA. ENERGIA CINÉTICA, NÃO.", 24, y=-7.1), rt=0.6)
        self.w(1.6)

    # ================================================================ C07 · cada intervalo, sua lei
    def c07(self):
        self.ancora("licao")
        mobs = [m for m in self.mobjects if m not in self.fixos | {self.linha, self.head}]
        self._frase = None
        L = self.linha
        self.sai(*mobs, rt=0.5)
        bm = txt("MOMENTO", 26, color=MAG)
        be = txt("TRABALHO–ENERGIA", 24, color=CYAN)
        bm.move_to(P3(-1.75, 3.9))
        be.move_to(P3(1.85, 3.9))
        cm, ce = cartao(bm, 0.2, cor=MAG), cartao(be, 0.2, cor=HEAT)
        lm = Line(P3(L.XS[1], L.y - 0.1), cm.get_top()).set_stroke(MAG, 2, opacity=0.8)
        le = Line(P3(L.XS[2], L.y - 0.1), ce.get_top()).set_stroke(CYAN, 2, opacity=0.8)
        self.p(*self.cab("CADA INTERVALO, SUA LEI"), FadeOut(L.dot),
               *[r.animate.set_color(L.CORES[i] if i in (1, 2) else WHITE_).set_opacity(1.0 if i in (1, 2) else 0.38)
                 for i, r in enumerate(L.rot)],
               Create(lm), Create(le), FadeIn(VGroup(cm, bm)), FadeIn(VGroup(ce, be)), rt=1.0)
        self.w(1.2)
        # ponte: colisão elástica (insinuação neutra: momentos com ângulo ≠ 90° e um círculo completo esmaecido)
        pp, lam, th1 = 7.0, 0.5, 28.0
        O = P3(-3.5, -0.9)
        cx, R = pp / (1 + lam), lam * pp / (1 + lam)
        dmax = cx * np.cos(np.radians(th1)) + np.sqrt(R * R - (cx * np.sin(np.radians(th1))) ** 2)
        Q, Tp = O + pol(dmax, th1), O + P3(pp, 0)
        ang12 = np.degrees(np.arccos(np.dot(unit(Q - O), unit(Tp - Q))))
        assert abs(np.linalg.norm(Q - (O + P3(cx, 0))) - R) < 1e-9 and abs(ang12 - 90) > 15
        self.ancora("ponte")
        aqui = txt("AQUI OS DOIS FICARAM JUNTOS.", 28).move_to(P3(0, 2.55))
        pi_ = arrow(O, Tp, MAG, 8, tip=0.28)
        p1 = arrow(O, Q, MAG, 6, tip=0.24)
        p2 = arrow(Q, Tp, MAG_L, 6, tip=0.24)
        circ = Circle(radius=R).move_to(O + P3(cx, 0)).set_stroke(CYAN, 2.4, opacity=0.35).set_z_index(1)
        self.p(FadeIn(aqui, shift=0.1 * UP), GrowArrow(pi_), rt=1.0)
        self.p(GrowArrow(p1), GrowArrow(p2), rt=1.0)
        self.p(Create(circ), rt=1.2)
        el = VGroup(txt("COLISÃO ELÁSTICA:", 26),
                    txt("ENERGIA CINÉTICA TAMBÉM SE CONSERVA", 24, color=CYAN)).arrange(DOWN, buff=0.18).move_to(P3(0, -3.9))
        self.p(FadeIn(el, shift=0.1 * UP), rt=1.0)
        self.w(0.8)
        self.p(*self.frase("QUAIS ÂNGULOS SÃO POSSÍVEIS?", 28, y=-5.3), rt=1.0)
        self.w(2.0)

    # ================================================================ cartão final: só @labparallax em degradê
    def cta(self):
        self.ancora("cta")
        for m in list(self.mobjects):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
        self.clear()
        with wide_pango():
            handle = screen_text("@labparallax", 48, oversample=2)
        handle.set_color_by_gradient(CYAN, VEL, MAG).move_to(ORIGIN)
        self.play(FadeIn(handle, scale=0.96), run_time=0.5)
        self.w(4.0)
        self.play(FadeOut(handle), run_time=0.4)
        self.wait(0.15)
