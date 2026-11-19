"""vid_0026 — O que uma marca no asfalto consegue contar sobre uma batida? (preview silencioso v3).

Curto vertical, Manim 2D. Cruzamento visto de cima: carro 1 (azul, 2000 kg) vem do oeste, carro 2 (violeta, 1000 kg) vem do sul,
ficam unidos e deslizam 8 m para leste e 6 m para norte. De trás para frente: trabalho–energia no deslizamento,
momento no impacto; depois a conferência de ida e volta e a energia.
v3 (handoff v3): as variáveis navegam da cena para as equações (cópias viajando; TransformByGlyphMap do MF-Tools nos passos
algébricos), cada termo explicado (forças, trabalho, isolamento), carros azul/violeta em vidro, paleta do canal nas variáveis
(velocidade violeta · momento magenta · K ciano · energia convertida laranja · força azul-claro · geometria cinza-claro),
asfalto azul-marinho e atmosfera cósmica sutil. v1 e v2 em cena_v1.py / cena_v2.py.

Preview 540×960 / 15 fps:
    uv run python -m manim -r 540,960 --fps 15 videos/vid_0026_colisao_cruzamento/cena.py ColisaoCruzamento026
Só alguns blocos: SECOES=c02,c03 (os outros rodam sem animar, para manter o estado). Ritmo por bloco: ESTICA.
"""
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
# ritmo de cada bloco (multiplica todas as durações do bloco; a voz ajusta depois)
ESTICA = {"c01": 1.0, "c02": 0.82, "c03": 0.95, "c04": 1.0, "c05": 1.0, "c06": 0.9, "c07": 1.0}

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

# ── mundo (metros; origem no ponto do impacto) e vistas ─────────────────────────────────────────────────────
UD = np.array([DX / D, DY / D, 0.0])        # direção da marca = direção de v⃗_f
L1, W1 = 4.8, 2.0                           # carro 1 (SUV, deitado: vai para leste)
L2, W2 = 3.4, 1.7                           # carro 2 (compacto, em pé: vai para norte)
C1 = np.array([0.0, W1 / 2, 0.0])           # centros no instante do contato
C2 = np.array([0.0, -L2 / 2, 0.0])
T0 = -0.25                                  # s antes do impacto (quadro "antes")
A_ = MU * G                                 # desaceleração no deslizamento (5 m/s²)
TSTOP = VF / A_                             # 2 s
AKW = 0.18                                  # m de mundo por (m/s) nas setas de velocidade
VISTAS = {"BIG": (0.62, (-2.15, -0.41)),    # C01: ~55 % da altura
          "LADO": (0.34, (-2.56, 1.75)),    # C02/C03: mapa à esquerda, cartão à direita, contas embaixo
          "MEIO": (0.45, (-1.6, 0.9))}      # C05


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


# ── texto, matemática e formas ──────────────────────────────────────────────────────────────────────────────
@contextmanager
def wide_pango():
    pw, ph = config.pixel_width, config.pixel_height
    config.pixel_width, config.pixel_height = 4000, 4000
    try:
        yield
    finally:
        config.pixel_width, config.pixel_height = pw, ph


def txt(s, size=26, color=WHITE_, op=1.0, width=8.2):
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


def cartao(m, buff=0.2, cor=PANEL_L, w=None, h=None):
    """Cartão de painel: azul profundo translúcido com borda clara fina (equações-chave e dados)."""
    r = RoundedRectangle(corner_radius=0.14, width=w or m.width + 2 * buff, height=h or m.height + 2 * buff)
    r.set_fill(PANEL, 0.55).set_stroke(cor, 1.5, opacity=0.6).move_to(m).set_z_index(-1)
    return r


def ficha(n, cor, r=0.17):
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
        self.rot = MathTex(nome, font_size=int(min(W, L) * 50), color=WHITE_).move_to(ORIGIN)
        self.add(self.corpo, self.rot)
        self.s_atual = 1.0
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


def rotulo_v(nome, val=r"?", size=40):
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

    def __init__(self, y=5.0):
        super().__init__()
        self.y = y
        self.rot = [txt(s, 21) for s in ("ANTES", "IMPACTO", "DESLIZAMENTO", "PAROU")]
        for r, x in zip(self.rot, self.XS):
            r.move_to(P3(x, y + 0.33))
        trilho = Line(P3(-3.95, y), P3(3.95, y)).set_stroke(DIM, 2, opacity=0.5)
        ticks = VGroup(*[Line(P3(x, y - 0.07), P3(x, y + 0.07)).set_stroke(DIM, 2, opacity=0.8) for x in self.XS])
        self.dot = Dot(P3(self.XS[3], y), radius=0.09, color=WHITE_).set_z_index(30)
        self.add(trilho, ticks, *self.rot, self.dot)
        for i, r in enumerate(self.rot):
            r.set_color(WHITE_).set_opacity(1.0 if i == 3 else 0.38)

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

    def sai(self, *mobs, rt=0.35):
        """Saída antes da entrada seguinte (nunca texto sobre texto). Aceita Eq."""
        ms = []
        for m in mobs:
            if m is None:
                continue
            ms.append(self.vivo(m) if isinstance(m, Eq) else m)
        if ms:
            self.p(*[FadeOut(m) for m in ms], rt=rt)
            self.remove(*ms)
            for m in mobs:
                if isinstance(m, Eq):
                    self.remove(m.mt, *m.gl)

    def vivo(self, E):
        return E.m

    def cab(self, s, size=32):
        """Cabeçalho do bloco (y = 6.3, branco com traço ciano): o anterior sai primeiro; devolve a entrada do novo."""
        self.sai(self.head, rt=0.3)
        if not s:
            self.head = None
            return []
        t = txt(s, size, width=8.0).move_to(P3(0, 6.3))
        tr = Line(t.get_corner(DL) + DOWN * 0.13, t.get_corner(DR) + DOWN * 0.13).set_stroke(CYAN, 1.6, opacity=0.7)
        self.head = VGroup(t, tr).set_z_index(20)
        return [FadeIn(self.head, shift=0.1 * DOWN)]

    def frase(self, s, size=24, y=-6.6, color=WHITE_, x=0.0):
        self.sai(self._frase, rt=0.3)
        self._frase = txt(s, size, color=color).move_to(P3(x, y)).set_z_index(20) if s else None
        return [FadeIn(self._frase, shift=0.1 * UP)] if self._frase is not None else []

    def troca(self, old, new, rt=0.8, shift=0.1 * UP):
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

    def nasce(self, E, fontes=(), rt=1.4, extra=()):
        """E nasce de termos que já estão na cena: `fontes` = [(origem, parte-de-E)] viajam (cópias); o resto entra por fade."""
        usados, anims = set(), []
        for orig, spec in fontes:
            ix = _spec(E, spec)
            usados.update(ix)
            anims.append(TransformFromCopy(orig, VGroup(*[E.gl[i] for i in ix]), path_arc=-0.3))
        resto = [E.gl[i] for i in range(len(E.gl)) if i not in usados]
        if resto:
            anims.append(FadeIn(VGroup(*resto), shift=0.08 * UP))
        self.p(*anims, *extra, rt=rt)
        return self.assenta(E)

    def passo(self, A, B, *pares, rt=1.6, extra=(), **kw):
        """Passo algébrico com MF-Tools: os glifos de A navegam até o lugar que ocupam em B (TransformByGlyphMap)."""
        self.assenta(A)
        ents = A.para(B, *pares)
        self.p(TransformByGlyphMap(A.m, B.m, *ents, auto_fade=True, **kw), *extra, rt=rt)
        self.remove(A.m, *A.gl)
        return self.assenta(B)

    def substitui(self, A, B, pares=(), copias=(), rt=1.6, extra=()):
        """Substituição com cópia deliberada: pares de A→B se transformam; `copias` = [(origem na cena, parte de B)]
        viajam da cena para B; o que sobra de A sai e o que sobra de B entra (sem estado intermediário ilegível)."""
        self.assenta(A)
        anims, usA, usB = [], set(), set()
        for a, b in pares:
            ia, ib = _spec(A, a), _spec(B, b)
            usA.update(ia)
            usB.update(ib)
            anims.append(ReplacementTransform(VGroup(*[A.gl[i] for i in ia]), VGroup(*[B.gl[i] for i in ib])))
        for n, ia in A.idx.items():
            ib = B.idx.get(n)
            if ib is not None and len(ia) == len(ib) and not usA.intersection(ia) and not usB.intersection(ib) \
                    and n not in [c[1] for c in copias if isinstance(c[1], str)]:
                usA.update(ia)
                usB.update(ib)
                anims.append(ReplacementTransform(VGroup(*[A.gl[i] for i in ia]), VGroup(*[B.gl[i] for i in ib])))
        for orig, b in copias:
            ib = _spec(B, b)
            usB.update(ib)
            anims.append(TransformFromCopy(orig, VGroup(*[B.gl[i] for i in ib]), path_arc=-0.35))
        sobraA = [A.gl[i] for i in range(len(A.gl)) if i not in usA]
        sobraB = [B.gl[i] for i in range(len(B.gl)) if i not in usB]
        self.remove(A.m)
        if sobraA:
            anims.append(FadeOut(VGroup(*sobraA), shift=0.1 * DOWN))
        if sobraB:
            anims.append(FadeIn(VGroup(*sobraB), shift=0.1 * UP))
        self.p(*anims, *extra, rt=rt)
        self.remove(*A.gl)
        return self.assenta(B)

    def riscar(self, *partes):
        return VGroup(*[Line(p.get_corner(DL) + P3(-0.05, -0.05), p.get_corner(UR) + P3(0.05, 0.05)).set_stroke(WHITE_, 4)
                        for p in partes])

    # ------------------------------------------------------------------ mundo → tela
    def S(self):
        return self.Sv.get_value()

    def O(self):
        return P3(self.Ox.get_value(), self.Oy.get_value())

    def w2s(self, p):
        return self.O() + self.S() * np.asarray(p, float)

    def zoom(self, vista, rt=1.4, extra=()):
        """Muda a vista do mundo: via (estática) e rastreadores de escala/origem animam juntos (mesma interpolação)."""
        S1, (x1, y1) = VISTAS[vista]
        O1 = P3(x1, y1)
        f = S1 / self.S()
        Oa = self.O()
        self.p(self.Sv.animate.set_value(S1), self.Ox.animate.set_value(x1), self.Oy.animate.set_value(y1),
               self.via.animate.scale(f, about_point=Oa).shift(O1 - Oa), *extra, rt=rt)
        self.vista = vista

    def por_vista(self, vista):
        """Põe o mundo direto numa vista (sem animação)."""
        S1, (x1, y1) = VISTAS[vista]
        f = S1 / self.S()
        Oa = self.O()
        self.via.scale(f, about_point=Oa).shift(P3(x1, y1) - Oa)
        self.Sv.set_value(S1)
        self.Ox.set_value(x1)
        self.Oy.set_value(y1)
        self.vista = vista

    def flash(self):
        return Flash(self.w2s(ORIGIN), color=WHITE_, line_length=0.3, flash_radius=0.18, num_lines=12)

    def anel_impacto(self):
        c = Circle(radius=0.12).move_to(self.w2s(ORIGIN)).set_stroke(WHITE_, 3).set_z_index(15)
        return c, c.animate.scale(4).set_stroke(opacity=0)

    def setas_antes(self, val1="?", val2="?", size=None):
        """Setas violeta de v⃗₁ᵢ e v⃗₂ᵢ à frente de cada carro (fora do corpo), no quadro t = T0, com rótulos Eq."""
        size = size or {"BIG": 40, "LADO": 36, "MEIO": 34}[self.vista]
        a1 = self.w2s(pos1(T0) + P3(L1 / 2 + 0.35, 0))
        a2 = self.w2s(pos2(T0) + P3(0, L2 / 2 + 0.35))
        s1 = seta_halo(a1, a1 + P3(V1I * AKW * self.S(), 0))
        s2 = seta_halo(a2, a2 + P3(0, V2I * AKW * self.S()))
        r1 = rotulo_v(r"\vec v_{1i}", val1, size)
        r2 = rotulo_v(r"\vec v_{2i}", val2, size)
        contorno(r1.mt.next_to(self.w2s(pos1(T0) + P3(0, W1 / 2)), UP, buff=0.14)).set_z_index(14)
        r1.mt.align_to(self.w2s(pos1(T0) + P3(-L1 / 2, 0)), LEFT)
        r1.mt.shift(RIGHT * max(0, -4.25 - r1.mt.get_left()[0]))
        contorno(r2.mt.next_to(s2, RIGHT, buff=0.14)).set_z_index(14)
        return VGroup(s1, s2), r1, r2

    def cotas(self, sim=True):
        """Cotas da marca na vista atual (geometria): catetos tracejados, rótulos fora dos carros, ângulo."""
        size = {"BIG": 40, "LADO": 32, "MEIO": 32}[self.vista]
        O, X, Q = self.w2s(ORIGIN), self.w2s(P3(DX, 0)), self.w2s(P3(DX, DY))
        legs = VGroup(DashedLine(O, X, dash_length=0.1), DashedLine(X, Q, dash_length=0.1)).set_stroke(GEO, 2, opacity=0.75)
        legs.set_z_index(2)
        lx = cota_eq(r"\Delta x", "8", size, sim)
        lab_at(lx.mt, O, X, lado=-1, gap=0.1)
        ly1 = Eq([("s", r"\Delta y", GEO)], size) if sim else None
        ly2 = Eq(([("eq", "=")] if sim else []) + [("n", "6", GEO), ("u", r"\,\mathrm{m}", GEO)], size)
        bloco = VGroup(*([ly1.mt] if sim else []), ly2.mt).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        bloco.next_to(self.w2s(P3(DX + W2 / 2 + 0.15, DY / 2)), RIGHT, buff=0.06)
        for m in bloco:
            contorno(m).set_z_index(14)
        ld = cota_eq("d", "10", size, sim)
        lab_at(ld.mt, O, Q, lado=1, gap=0.22)
        r = {"BIG": 0.95, "LADO": 0.6, "MEIO": 0.7}[self.vista]
        ang = VGroup(DashedLine(O, O + P3(r * 1.45, 0), dash_length=0.08).set_stroke(DIM, 1.8, opacity=0.8),
                     arco(O, r, 0, TH),
                     contorno(MathTex(r"\theta", font_size=size, color=WHITE_).move_to(O + pol(r * 1.38, TH / 2))))
        ang.set_z_index(9)
        return dict(legs=legs, lx=lx, ly1=ly1, ly2=ly2, ld=ld, ang=ang,
                    g=VGroup(legs, lx.mt, *([ly1.mt] if sim else []), ly2.mt, ld.mt, ang))

    # ------------------------------------------------------------------ cena
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.fundo()
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.4).to_corner(UR, buff=0.28).set_z_index(40)
        tag = txt("EXERCÍCIO RESOLVIDO · EP. 9", 20, op=0.7).to_corner(UL, buff=0.4).set_z_index(40)
        self.add(wm, tag)
        self.fixos = {wm, tag, self.atmos}
        self.head, self._frase = None, None
        self.montar_mundo()
        marcas = []
        for nome in ("c01", "c02", "c03", "c04", "c05", "c06", "c07"):
            self.K = ESTICA[nome]
            self.next_section(nome, skip_animations=bool(SECOES) and nome not in SECOES)
            t0 = self.renderer.time
            getattr(self, nome)()
            marcas.append((nome, t0, self.renderer.time))
        for nome, a, b in marcas:
            print(f"[tempo] {nome}: {a:6.1f} s -> {b:6.1f} s ({b - a:5.1f} s)")

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
        S0, (x0, y0) = VISTAS["BIG"]
        self.Sv, self.Ox, self.Oy = ValueTracker(S0), ValueTracker(x0), ValueTracker(y0)
        self.vista = "BIG"
        # vias (em metros): leste–oeste x∈[−9, 11], y∈[−1.5, 3.5]; norte–sul x∈[−2.5, 2.5], y∈[−8.5, 8]
        h = Rectangle(width=20, height=5).move_to(P3(1, 1))
        v = Rectangle(width=5, height=16.5).move_to(P3(0, -0.25))
        try:
            via = Union(h, v)
        except Exception:
            via = VGroup(h, v)
        via.set_fill(ROAD, 0.88).set_stroke(CYAN, 1.5, opacity=0.35).set_z_index(-3)
        faixas = VGroup(DashedLine(P3(-9, 1), P3(-2.9, 1), dash_length=0.9), DashedLine(P3(2.9, 1), P3(11, 1), dash_length=0.9),
                        DashedLine(P3(0, -8.5), P3(0, -1.9), dash_length=0.9), DashedLine(P3(0, 3.9), P3(0, 8), dash_length=0.9)) \
            .set_stroke(GEO, 1.5, opacity=0.4).set_z_index(-2)
        self.via = VGroup(via, faixas)
        self.via.scale(S0, about_point=ORIGIN).shift(P3(x0, y0))
        # carros e relógio físico (atualizados pela vista e pelo relógio)
        self.tt = ValueTracker(TSTOP)
        self.v1 = Carro(L1, W1, CAR1, CAR1_L, "m_1")
        self.v2 = Carro(L2, W2, CAR2, CAR2_L, "m_2", ang=PI / 2)
        self.ligar_carros()
        self.segue = False
        self.marca = always_redraw(lambda: marca_mob(self.w2s(ORIGIN),
                                                     self.w2s(UD * (s_desl(self.tt.get_value()) if self.segue else D)),
                                                     w=4.0 * self.S() / 0.62 + 1.0, sep=0.16 * self.S()))

    def ligar_carros(self):
        for car, fn in ((self.v1, pos1), (self.v2, pos2)):
            def upd(m, fn=fn):
                s = self.S()
                if abs(s - m.s_atual) > 1e-9:
                    m.scale(s / m.s_atual)
                    m.s_atual = s
                m.move_to(self.w2s(fn(self.tt.get_value())))
            car.clear_updaters()
            car.add_updater(upd)
            upd(car)

    def bussola(self, o, size=22):
        return VGroup(arrow(o, o + P3(0, 0.55), DIM, 2.5, tip=0.13), arrow(o, o + P3(0.55, 0), DIM, 2.5, tip=0.13),
                      txt("N", size, color=DIM).move_to(o + P3(0, 0.82)), txt("L", size, color=DIM).move_to(o + P3(0.82, 0)))

    # ================================================================ C01 · mistério
    def c01(self):
        self.linha = Linha()
        self.bus = self.bussola(P3(3.6, -3.4))
        # cartão de dados (fichas de identidade: 1 azul, 2 violeta)
        self.d_m1 = Eq([("s", "m_1"), ("eq", "="), ("v", "2000"), ("u", r"\,\mathrm{kg}")], 38)
        self.d_m2 = Eq([("s", "m_2"), ("eq", "="), ("v", "1000"), ("u", r"\,\mathrm{kg}")], 38)
        self.d_mu = Eq([("s", r"\mu_k"), ("eq", "="), ("v", r"0{,}50")], 38)
        self.d_g = Eq([("s", "g"), ("eq", "="), ("v", "10"), ("u", r"\,\mathrm{m/s^2}")], 38)
        self.f1, self.f2 = ficha(1, CAR1), ficha(2, CAR2)
        lin1 = VGroup(VGroup(self.f1, self.d_m1.mt).arrange(RIGHT, buff=0.16), VGroup(self.f2, self.d_m2.mt).arrange(RIGHT, buff=0.16)) \
            .arrange(RIGHT, buff=0.9)
        lin2 = VGroup(self.d_mu.mt, self.d_g.mt).arrange(RIGHT, buff=1.3)
        corpo = VGroup(lin1, lin2).arrange(DOWN, buff=0.3).move_to(P3(0, -4.95))
        self.card = cartao(corpo, 0.24, w=8.3)
        # tudo entra junto: cruzamento, carros unidos no fim da marca, régua e dados (sem tela vazia)
        self.p(FadeIn(self.via), FadeIn(self.v1), FadeIn(self.v2), FadeIn(self.marca), FadeIn(self.linha), FadeIn(self.bus),
               FadeIn(self.card), FadeIn(corpo), *self.cab("O QUE UMA MARCA NO ASFALTO\nCONSEGUE CONTAR SOBRE UMA BATIDA?", 30),
               rt=0.5)
        for e in (self.d_m1, self.d_m2, self.d_mu, self.d_g):
            self.assenta(e)
        self.remove(corpo)
        self.add(self.f1, self.f2)
        self.w(1.4)
        # cotas da marca (geometria)
        ct = self.cotas(sim=False)
        self.p(Create(ct["legs"][0]), FadeIn(ct["lx"].mt), rt=1.0)
        self.p(Create(ct["legs"][1]), FadeIn(ct["ly2"].mt), rt=1.0)
        self.p(FadeIn(ct["ld"].mt), FadeIn(ct["ang"]), rt=1.0)
        self.ct = ct
        self.w(1.0)
        # de onde vieram: setas fantasma tracejadas com v⃗ = ?
        y1 = self.w2s(C1)[1]
        g1 = VGroup(DashedLine(P3(-4.4, y1), self.w2s(P3(-2.2, C1[1])), dash_length=0.15).set_stroke(VEL, 3, opacity=0.8),
                    arrow(self.w2s(P3(-3.0, C1[1])), self.w2s(P3(-2.1, C1[1])), VEL, 3, tip=0.2))
        g2 = VGroup(DashedLine(self.w2s(P3(0, -8.4)), self.w2s(P3(0, -2.4)), dash_length=0.15).set_stroke(VEL, 3, opacity=0.8),
                    arrow(self.w2s(P3(0, -3.2)), self.w2s(P3(0, -2.3)), VEL, 3, tip=0.2))
        q1 = rotulo_v(r"\vec v_{1i}", "?", 40)
        q2 = rotulo_v(r"\vec v_{2i}", "?", 40)
        contorno(q1.mt.next_to(g1, UP, buff=0.14).align_to(P3(-4.2, 0), LEFT))
        contorno(q2.mt.next_to(self.w2s(P3(0, -5.4)), RIGHT, buff=0.3))
        self.p(Create(g1[0]), FadeIn(g1[1]), FadeIn(q1.mt), rt=1.0)
        self.p(Create(g2[0]), FadeIn(g2[1]), FadeIn(q2.mt), rt=1.0)
        self.fantasmas = VGroup(g1, g2, q1.mt, q2.mt)
        self.w(1.6)
        # hipóteses: uma ficha de cada vez
        hips = ["IMPACTO CURTO", "MESMO ATRITO EM TODO O DESLIZAMENTO", "MARCA EM LINHA RETA"]
        atual = None
        for h in hips:
            t = txt(h, 21, color=WHITE_)
            ch = VGroup(cartao(t, 0.14, cor=DIM), t).move_to(P3(0, -6.55))
            if atual is not None:
                self.sai(atual, rt=0.3)
            self.p(FadeIn(ch, shift=0.08 * UP), rt=0.6)
            self.w(1.1)
            atual = ch
        self.sai(atual, rt=0.3)
        self.hip = txt("MODELO IDEALIZADO, NÃO PERÍCIA", 19, color=DIM).move_to(P3(0, -6.55))
        self.p(FadeIn(self.hip), rt=0.6)
        self.w(1.8)

    # ================================================================ C02 · começar pelo fim
    def c02(self):
        self.sai(self.fantasmas, self.hip, self.ct["g"], self.bus, rt=0.5)
        # o cartão vira coluna à direita; o mundo vai para a vista lateral
        X = 1.35
        anims = []
        for e, ch, y in ((self.d_m1, self.f1, 4.25), (self.d_m2, self.f2, 3.78), (self.d_mu, None, 3.31), (self.d_g, None, 2.84)):
            anims.append(e.m.animate.scale(34 / 38).move_to(P3(X + 0.32, y), aligned_edge=LEFT))
            if ch is not None:
                anims.append(ch.animate.scale(0.8).move_to(P3(X + 0.08, y)))
        self.card2 = cartao(VGroup(Rectangle(width=3.0, height=4.0)), 0, w=3.2, h=4.15).move_to(P3(2.85, 2.55))
        cab = self.cab("COMEÇAR PELO FIM")
        self.zoom("LADO", rt=1.6, extra=[*cab, *self.linha.ir(2), *anims, ReplacementTransform(self.card, self.card2)])
        # o conjunto: M = m₁ + m₂ (as cópias de m₁ e m₂ viajam para formar M)
        self.eM = Eq([("M", "M"), ("eq", "="), ("a", "m_1"), ("p", "+"), ("b", "m_2")], 34)
        self.eM.mt.move_to(P3(X + 0.05, 2.18), aligned_edge=LEFT)
        self.nasce(self.eM, [(self.d_m1.parte("s"), "a"), (self.d_m2.parte("s"), "b")], rt=1.3)
        self.eM2 = Eq([("eq", "="), ("v", "3000"), ("u", r"\,\mathrm{kg}")], 34)
        self.eM2.mt.next_to(self.eM.mt, DOWN, buff=0.16).align_to(self.eM.mt[1], LEFT)
        self.nasce(self.eM2, [(VGroup(self.d_m1.parte("v"), self.d_m2.parte("v")), "v")], rt=1.2)
        self.w(0.6)
        # replay do deslizamento: o conjunto parte do impacto com v⃗_f (fantasma à frente) e para no fim da marca
        self.segue = True
        self.p(self.tt.animate.set_value(0.0), rt=1.2, rate_func=linear)
        c, an = self.anel_impacto()
        self.add(c)
        self.p(an, rt=0.5)
        self.remove(c)
        vfant = always_redraw(lambda: arrow(self.w2s(pos1(self.tt.get_value()) + UD * 3.0),
                                            self.w2s(pos1(self.tt.get_value()) + UD * (3.0 + 0.32 * vel_desl(self.tt.get_value()))),
                                            VEL, 5, tip=0.18, op=0.75, z=12))
        self.add(vfant)
        self.p(self.tt.animate.set_value(TSTOP), rt=3.0, rate_func=linear)
        vfant.clear_updaters()
        self.remove(vfant)
        self.segue = False
        # v⃗_f fica como fantasma no início do deslizamento (o valor é o que se procura)
        O = self.w2s(ORIGIN)
        nrm = P3(UD[1], -UD[0]) * 0.32
        self.vf_seta = seta_halo(O + nrm, O + nrm + UD * 1.45, VEL, 5, tip=0.18)
        self.vf_rot = rotulo_v(r"\vec v_f", "?", 36)
        contorno(self.vf_rot.mt.next_to(self.vf_seta[1].get_end(), RIGHT, buff=0.1))
        self.p(GrowArrow(self.vf_seta[1]), FadeIn(self.vf_seta[0]), FadeIn(self.vf_rot.mt), rt=0.8)
        self.assenta(self.vf_rot)
        self.ct = self.cotas(sim=True)
        self.p(FadeIn(self.ct["g"]), rt=0.7)
        self.w(0.6)
        # forças no deslizamento (vista lateral): peso, normal e atrito contra o movimento
        gy = -3.05
        chao = Line(P3(-4.3, gy), P3(-0.5, gy)).set_stroke(GEO, 2, opacity=0.7)
        bl = VGroup(Rectangle(width=0.8, height=0.75).set_fill(CAR1, 0.6).set_stroke(CAR1_L, 2),
                    Rectangle(width=0.6, height=0.75).set_fill(CAR2, 0.6).set_stroke(CAR2_L, 2)).arrange(RIGHT, buff=0)
        bl.move_to(P3(-2.4, gy + 0.375))
        rotM = MathTex("M", font_size=34, color=WHITE_).move_to(bl)
        fN = arrow(bl.get_top(), bl.get_top() + P3(0, 0.95), FC, 6, tip=0.2)
        fP = arrow(bl.get_center(), bl.get_center() + P3(0, -1.25), FC, 6, tip=0.2, z=11)
        fA = arrow(bl.get_corner(DL) + P3(0, 0.15), bl.get_corner(DL) + P3(-1.25, 0.15), FC, 6, tip=0.2)
        vv = arrow(bl.get_right() + P3(0.1, 0.1), bl.get_right() + P3(1.05, 0.1), VEL, 4, tip=0.16, op=0.7)
        lN = Eq([("N", "N", FC)], 34)
        contorno(lN.mt.next_to(fN, LEFT, buff=0.1))
        lP = Eq([("P", "M g", FC)], 34)
        contorno(lP.mt.next_to(fP.get_end(), RIGHT, buff=0.1))
        lA = Eq([("f", "f_k", FC)], 34)
        contorno(lA.mt.next_to(fA, UP, buff=0.08))
        lv = MathTex(r"\vec v_f", font_size=30, color=VEL).next_to(vv, UP, buff=0.06)
        tvl = txt("VISTA LATERAL", 16, color=DIM).move_to(P3(-3.75, -1.4))
        diag = VGroup(chao, bl, rotM, fN, fP, fA, vv, lN.mt, lP.mt, lA.mt, lv, tvl)
        self.p(FadeIn(VGroup(chao, bl, rotM, tvl, vv, lv)), rt=0.7)
        self.p(GrowArrow(fP), FadeIn(lP.mt), GrowArrow(fN), FadeIn(lN.mt), rt=0.9)
        pass
        eN = Eq([("N", "N", FC), ("eq", "="), ("M", "M"), ("g", "g")], 38, pos=P3(1.7, -1.75))
        self.nasce(eN, [(lN.parte("N"), "N"), (lP.parte("P"), ["M", "g"])], rt=1.2)
        self.p(GrowArrow(fA), FadeIn(lA.mt), rt=0.8)
        pass
        eF = Eq([("f", "f_k", FC), ("eq", "="), ("mu", r"\mu_k"), ("N", "N", FC)], 38, pos=P3(1.7, -2.6))
        self.nasce(eF, [(lA.parte("f"), "f"), (self.d_mu.parte("s"), "mu"), (eN.parte("N"), "N")], rt=1.3)
        self.w(0.5)
        eF2 = Eq([("f", "f_k", FC), ("eq", "="), ("mu", r"\mu_k"), ("M", "M"), ("g", "g")], 38, pos=P3(1.7, -2.6))
        self.substitui(eF, eF2, copias=[(VGroup(eN.parte("M"), eN.parte("g")), ["M", "g"])], rt=1.3)
        self.w(0.8)
        # trabalho do atrito (laranja): W = −f_k d; d é a cota da marca
        eW = Eq([("W", r"W_{\mathrm{at}}", HEAT), ("eq", "="), ("s", "-"), ("f", "f_k", FC), ("d", r"\,d", GEO)], 40,
                pos=P3(0, -4.05))
        self.nasce(eW, [(eF2.parte("f"), "f"), (self.ct["ld"].parte("s"), "d")], rt=1.4)
        eW2 = Eq([("W", r"W_{\mathrm{at}}", HEAT), ("eq", "="), ("s", "-"), ("mu", r"\mu_k"), ("M", "M"), ("g", "g"),
                  ("d", r"\,d", GEO)], 40, pos=P3(0, -4.05))
        self.substitui(eW, eW2, copias=[(VGroup(eF2.parte("mu"), eF2.parte("M"), eF2.parte("g")), ["mu", "M", "g"])], rt=1.3)
        nota = txt("ENERGIA QUE O ATRITO TRANSFORMA EM CALOR", 17, color=HEAT, op=0.85).move_to(P3(0, -4.62))
        self.p(FadeIn(nota), rt=0.6)
        self.w(0.8)
        # energia cinética no início do deslizamento → 0 ao parar
        eK = Eq([("K", "K", CYAN), ("c", ":"), ("h", r"\tfrac12"), ("M", "M"), ("v", "v_f^2", VEL), ("ar", r"\ \longrightarrow\ "),
                 ("z", "0")], 40, pos=P3(0, -5.3))
        self.nasce(eK, [(self.eM.parte("M"), "M"), (self.vf_rot.parte("v"), "v")], rt=1.4)
        self.w(0.8)
        # variação da energia cinética = trabalho do atrito
        e0 = Eq([("z", "0"), ("s1", "-"), ("h", r"\tfrac12"), ("M1", "M"), ("v", "v_f^2", VEL), ("eq", "="), ("s2", "-"),
                 ("mu", r"\mu_k"), ("M2", "M"), ("g", "g"), ("d", "d", GEO)], 50, pos=P3(0, -6.4))
        self.nasce(e0, [(eK.parte("z"), "z"), (VGroup(eK.parte("h"), eK.parte("M"), eK.parte("v")), ["h", "M1", "v"]),
                        (VGroup(eW2.parte("s"), eW2.parte("mu"), eW2.parte("M"), eW2.parte("g"), eW2.parte("d")),
                         ["s2", "mu", "M2", "g", "d"])],
                   rt=1.8, extra=[FadeIn(cartao(VGroup(Rectangle(width=6.6, height=0.8)), 0).move_to(P3(0, -6.4)))])
        self.w(1.0)
        # a álgebra sobe para o espaço livre (o diagrama e as linhas de apoio saem)
        fundoE = [m for m in self.mobjects if isinstance(m, RoundedRectangle) and abs(m.get_center()[1] + 6.4) < 0.05]
        self.sai(diag, eN, eF2, eW2, nota, eK, *fundoE, rt=0.6)
        Y = -2.55
        self.p(e0.m.animate.move_to(P3(0, Y)), rt=0.8)
        self.cardE = cartao(VGroup(Rectangle(width=7.4, height=1.0)), 0).move_to(P3(0, Y))
        self.p(FadeIn(self.cardE), rt=0.3)
        # passo 1 (MF-Tools): os sinais de menos cancelam e o zero sai
        e1 = Eq([("h", r"\tfrac12"), ("M1", "M"), ("v", "v_f^2", VEL), ("eq", "="), ("mu", r"\mu_k"), ("M2", "M"), ("g", "g"),
                 ("d", "d", GEO)], 52, pos=P3(0, Y))
        self.passo(e0, e1, rt=1.5)
        self.w(0.6)
        # passo 2: M dos dois lados se corta e voa para fora
        rs = self.riscar(e1.parte("M1"), e1.parte("M2"))
        self.p(Create(rs), *self.frase("A MASSA TOTAL CANCELA", 24, y=-3.65), rt=0.9)
        self.w(0.9)
        e2 = Eq([("h", r"\tfrac12"), ("v", "v_f^2", VEL), ("eq", "="), ("mu", r"\mu_k"), ("g", "g"), ("d", "d", GEO)], 52, pos=P3(0, Y))
        self.remove(rs)
        self.passo(e1, e2, ("M1", [], {"shift": UP * 0.7}), ("M2", [], {"shift": UP * 0.7}), rt=1.5,
                   extra=[FadeOut(rs, shift=UP * 0.7)])
        self.w(0.6)
        # passo 3: o ½ atravessa a igualdade e vira 2
        e3 = Eq([("v", "v_f^2", VEL), ("eq", "="), ("dois", "2"), ("mu", r"\mu_k"), ("g", "g"), ("d", "d", GEO)], 52, pos=P3(0, Y))
        self.passo(e2, e3, ("h", "dois", {"path_arc": -2.2}), rt=1.6)
        self.w(0.6)
        # passo 4: raiz dos dois lados
        e4 = Eq([("v", "v_f", VEL), ("eq", "="), ("r", r"\sqrt{2\mu_k g\, d}")], 52, pos=P3(0, Y))
        e4.gl[radicando(e4, "r")[-1]].set_color(GEO)
        self.passo(e3, e4, (("v", slice(0, 2)), "v"), (("v", 2), []), (["dois", "mu", "g", "d"], "r"), rt=1.5)
        self.sai(self._frase)
        self._frase = None
        self.w(0.6)
        # substituição com cópia: μ_k e g do cartão, d da cota da marca
        Y2 = -3.9
        e5 =Eq([("v", "v_f", VEL), ("eq", "="), ("r", r"\sqrt{2\cdot 0{,}50\cdot 10\cdot 10}"), ("eq2", "="),
                 ("res", r"10\,\mathrm{m/s}")], 46, pos=P3(0, Y2))
        conteudo = radicando(e5, "r")
        i_mu, i_g, i_d = conteudo[2:6], conteudo[7:9], conteudo[10:12]
        for i in i_d:
            e5.gl[i].set_color(GEO)
        rad_rest = [i for i in e5.idx["r"] if i not in i_mu + i_g + i_d]
        self.p(*[Indicate(m, color=WHITE_, scale_factor=1.15) for m in (self.d_mu.parte("v"), self.d_g.parte("v"),
                                                                        self.ct["ld"].parte("n"))], rt=0.8)
        anims = [TransformFromCopy(e4.parte("v"), e5.parte("v")), TransformFromCopy(e4.parte("eq"), e5.parte("eq")),
                 TransformFromCopy(e4.parte("r"), VGroup(*[e5.gl[i] for i in rad_rest])),
                 TransformFromCopy(self.d_mu.parte("v"), VGroup(*[e5.gl[i] for i in i_mu]), path_arc=-0.4),
                 TransformFromCopy(self.d_g.parte("v"), VGroup(*[e5.gl[i] for i in i_g]), path_arc=-0.4),
                 TransformFromCopy(self.ct["ld"].parte("n"), VGroup(*[e5.gl[i] for i in i_d]), path_arc=0.4)]
        self.p(*anims, rt=1.8)
        self.p(FadeIn(VGroup(e5.parte("eq2"), e5.parte("res")), shift=0.1 * LEFT), rt=0.8)
        self.assenta(e5)
        bx = caixa(e5.parte("res"), WHITE_, 0.1)
        self.p(Create(bx), rt=0.5)
        # o 10 m/s volta para a seta de v⃗_f
        nr = rotulo_v(r"\vec v_f", r"10\,\mathrm{m/s}", 36)
        contorno(nr.mt.move_to(self.vf_rot.mt, aligned_edge=LEFT))
        self.substitui(self.vf_rot, nr, copias=[(e5.parte("res"), "n")], rt=1.3)
        self.vf_rot = nr
        self.w(1.0)
        # direção e componentes: v_fx = v_f · Δx/d e v_fy = v_f · Δy/d (cópias da seta e das cotas)
        self.sai(e4, e5, bx, self.cardE, rt=0.6)
        ex = Eq([("vx", "v_{fx}", VEL), ("eq", "="), ("vf", "v_f", VEL), ("fr", r"\dfrac{\Delta x}{d}", ("fr", GEO))], 42,
                pos=P3(-1.6, -2.1))
        ey = Eq([("vy", "v_{fy}", VEL), ("eq", "="), ("vf", "v_f", VEL), ("fr", r"\dfrac{\Delta y}{d}", ("fr", GEO))], 42,
                pos=P3(-1.6, -3.55))
        self.nasce(ex, [(self.vf_rot.parte("v"), "vf"), (self.ct["lx"].parte("s"), ex.num("fr")),
                        (self.ct["ld"].parte("s"), ex.den("fr"))], rt=1.4)
        self.nasce(ey, [(self.vf_rot.parte("v"), "vf"), (self.ct["ly1"].parte("s"), ey.num("fr")),
                        (self.ct["ld"].parte("s"), ey.den("fr"))], rt=1.4)
        self.w(0.6)
        ex2 = Eq([("vx", "v_{fx}", VEL), ("eq", "="), ("vf", "10"), ("dot", r"\cdot"), ("fr", r"\dfrac{8}{10}", ("fr", GEO)),
                  ("eq2", "="), ("res", r"8\,\mathrm{m/s}")], 42)
        ex2.mt.move_to(ex.mt, aligned_edge=LEFT)
        ey2 = Eq([("vy", "v_{fy}", VEL), ("eq", "="), ("vf", "10"), ("dot", r"\cdot"), ("fr", r"\dfrac{6}{10}", ("fr", GEO)),
                  ("eq2", "="), ("res", r"6\,\mathrm{m/s}")], 42)
        ey2.mt.move_to(ey.mt, aligned_edge=LEFT)
        self.substitui(ex, ex2, pares=[("fr", "fr")], copias=[(self.vf_rot.parte("n")[0:2], "vf")], rt=1.4)
        self.substitui(ey, ey2, pares=[("fr", "fr")], copias=[(self.vf_rot.parte("n")[0:2], "vf")], rt=1.2)
        self.w(0.8)
        # o triângulo da marca vira o de velocidade (catetos copiados, geometria → violeta)
        O2, s = P3(-3.8, -6.75), 0.33
        Xv, Qv = O2 + P3(8 * s, 0), O2 + P3(8 * s, 6 * s)
        hx = arrow(O2, Xv, VEL_L, 6, tip=0.2)
        hy = arrow(Xv, Qv, VEL_L, 6, tip=0.2)
        hh = arrow(O2, Qv, VEL, 8, tip=0.24, z=9)
        lx = Eq([("n", r"8\,\mathrm{m/s}")], 34)
        lab_at(lx.mt, O2, Xv, lado=-1, gap=0.08)
        ly = Eq([("n", r"6\,\mathrm{m/s}")], 34)
        lab_at(ly.mt, Xv, Qv, lado=-1)
        lh = Eq([("n", r"10\,\mathrm{m/s}")], 34)
        lab_at(lh.mt, O2, Qv, lado=1, gap=0.18)
        av = arco(O2, 0.55, 0, TH)
        Om_, Xm_, Qm_ = self.w2s(ORIGIN), self.w2s(P3(DX, 0)), self.w2s(P3(DX, DY))
        self.p(TransformFromCopy(Line(Om_, Xm_), hx), TransformFromCopy(Line(Xm_, Qm_), hy),
               TransformFromCopy(Line(Om_, Qm_), hh), TransformFromCopy(self.ct["ang"][1], av), rt=1.6)
        self.p(TransformFromCopy(ex2.parte("res"), lx.parte("n")), TransformFromCopy(ey2.parte("res"), ly.parte("n")),
               TransformFromCopy(self.vf_rot.parte("n"), lh.parte("n")), rt=1.2)
        self.assenta(lx), self.assenta(ly), self.assenta(lh)
        res = Eq([("v", r"\vec v_f", VEL), ("eq", "="), ("x", r"(8;\ 6)\,\mathrm{m/s}")], 44, pos=P3(1.95, -5.35))
        self.p(FadeIn(res.mt, shift=0.1 * UP), FadeIn(cartao(res.mt, 0.18)), rt=0.9)
        self.assenta(res)
        self.w(1.0)
        # os resultados entram no cartão (para o impacto)
        self.d_vx = Eq([("s", "v_{fx}", VEL), ("eq", "="), ("v", "8"), ("u", r"\,\mathrm{m/s}")], 34)
        self.d_vy = Eq([("s", "v_{fy}", VEL), ("eq", "="), ("v", "6"), ("u", r"\,\mathrm{m/s}")], 34)
        self.d_vx.mt.move_to(P3(X + 0.32, 1.12), aligned_edge=LEFT)
        self.d_vy.mt.move_to(P3(X + 0.32, 0.67), aligned_edge=LEFT)
        self.nasce(self.d_vx, [(ex2.parte("vx"), "s"), (ex2.parte("res"), ["v", "u"])], rt=1.1)
        self.nasce(self.d_vy, [(ey2.parte("vy"), "s"), (ey2.parte("res"), ["v", "u"])], rt=1.0)
        self.w(1.2)
        self.c02_fora = [ex2, ey2, hx, hy, hh, lx, ly, lh, av, res]

    # ================================================================ C03 · voltar ao impacto
    def c03(self):
        resto = [m for m in self.mobjects if isinstance(m, RoundedRectangle) and m.get_center()[1] < -4.5]
        self.sai(*self.c02_fora, *resto, self.vf_seta, self.vf_rot, self.ct["g"], rt=0.6)
        self.p(*self.cab("VOLTAR AO IMPACTO"), *self.linha.ir(1), rt=0.6)
        # congelar o instante antes do choque
        self.p(self.tt.animate.set_value(T0), rt=2.0, rate_func=linear)
        setas, r1, r2 = self.setas_antes()
        self.p(*[GrowArrow(s[1]) for s in setas], *[FadeIn(s[0]) for s in setas], FadeIn(r1.mt), FadeIn(r2.mt), rt=0.9)
        self.assenta(r1), self.assenta(r2)
        self.setas, self.r1, self.r2 = setas, r1, r2
        # a lei do impacto
        YF = -1.55
        fase = VGroup(txt("IMPACTO:", 24), txt("MOMENTO", 24, color=MAG)).arrange(RIGHT, buff=0.18).move_to(P3(0, YF))
        self.p(FadeIn(fase), rt=0.7)
        s1 = txt("IMPACTO CURTÍSSIMO:\nIMPULSO EXTERNO DESPREZÍVEL", 19)
        s2 = txt("VÁRIOS METROS DESLIZANDO:\nATRITO NÃO DESPREZÍVEL", 19, color=DIM)
        s1.move_to(P3(-2.2, -2.55))
        s2.move_to(P3(2.2, -2.55))
        b1, b2 = caixa(s1, MAG, 0.14, 2.0), caixa(s2, DIM, 0.14, 1.6, 0.7)
        vs = MathTex(r"\times", font_size=36, color=DIM).move_to(P3(0, -2.55))
        self.p(FadeIn(VGroup(s1, b1)), rt=0.7)
        self.w(1.0)
        self.p(FadeIn(VGroup(s2, b2)), FadeIn(vs), rt=0.7)
        self.w(1.4)
        self.sai(VGroup(s1, b1, s2, b2, vs), rt=0.5)
        # momentos: p⃗ = m v⃗ (m₁ do carro, v⃗₁ᵢ da seta)
        ep1 = Eq([("p", r"\vec p_{1i}", MAG), ("eq", "="), ("m", "m_1"), ("v", r"\vec v_{1i}", VEL)], 42, pos=P3(-2.15, -2.45))
        ep2 = Eq([("p", r"\vec p_{2i}", MAG), ("eq", "="), ("m", "m_2"), ("v", r"\vec v_{2i}", VEL)], 42, pos=P3(2.15, -2.45))
        self.nasce(ep1, [(self.v1.rot, "m"), (r1.parte("v"), "v")], rt=1.3)
        self.nasce(ep2, [(self.v2.rot, "m"), (r2.parte("v"), "v")], rt=1.3)
        # no mapa: p⃗₁ᵢ ao longo de x e p⃗₂ᵢ ao longo de y (tamanhos ainda desconhecidos: tracejados)
        a1 = self.w2s(pos1(T0) + P3(-L1 / 2, W1 / 2 + 0.55))
        a2 = self.w2s(pos2(T0) + P3(-W2 / 2 - 0.55, -L2 / 2))
        pq1 = arrow(a1, a1 + P3(1.4, 0), MAG, 5, tip=0.18, op=0.55)
        pq2 = arrow(a2, a2 + P3(0, 1.4), MAG, 5, tip=0.18, op=0.55)
        self.p(Create(pq1), Create(pq2), rt=0.8)
        self.w(0.6)
        # P⃗ᵢ = p⃗₁ᵢ + p⃗₂ᵢ ; depois do choque, P⃗_f = M v⃗_f ao longo da marca
        ePi = Eq([("P", r"\vec P_i", MAG), ("eq", "="), ("a", r"\vec p_{1i}", MAG), ("pl", "+"), ("b", r"\vec p_{2i}", MAG)], 38,
                  pos=P3(-2.0, -3.35))
        self.nasce(ePi, [(ep1.parte("p"), "a"), (ep2.parte("p"), "b")], rt=1.2)
        ePf = Eq([("P", r"\vec P_f", MAG), ("eq", "="), ("M", "M"), ("v", r"\vec v_f", VEL)], 42, pos=P3(2.2, -3.35))
        self.nasce(ePf, [(self.eM.parte("M"), "M")], rt=1.1)
        O, X_, Q_ = self.w2s(ORIGIN), self.w2s(P3(DX, 0)), self.w2s(P3(DX, DY))
        Pf = seta_halo(O, Q_, MAG, 7, tip=0.24, z=13)
        lPf = contorno(MathTex(r"\vec P_f", font_size=36, color=MAG)).move_to(O + (Q_ - O) * 0.55 + P3(-0.35, 0.35)).set_z_index(14)
        self.p(GrowArrow(Pf[1]), FadeIn(Pf[0]), TransformFromCopy(ePf.parte("P"), lPf), rt=1.2)
        self.w(0.6)
        eIg = Eq([("a", r"\vec P_i", MAG), ("eq", "="), ("b", r"\vec P_f", MAG)], 48, pos=P3(0, -4.4))
        self.nasce(eIg, [(ePi.parte("P"), "a"), (ePf.parte("P"), "b")], rt=1.2,
                   extra=[FadeIn(cartao(VGroup(Rectangle(width=2.6, height=0.7)), 0).move_to(P3(0, -4.4)))])
        self.w(0.8)
        # componentes: projeções tracejadas de P⃗ nos eixos dão p₁ᵢ (x) e p₂ᵢ (y)
        pr = VGroup(DashedLine(Q_, X_, dash_length=0.08), ).set_stroke(MAG, 2, opacity=0.7)
        px = arrow(O, X_, MAG_L, 5, tip=0.18, z=12)
        py = arrow(X_, Q_, MAG_L, 5, tip=0.18, z=12)
        lpx = contorno(MathTex(r"p_{1i}", font_size=34, color=MAG)).next_to(px, DOWN, buff=0.06).set_z_index(14)
        lpy = contorno(MathTex(r"p_{2i}", font_size=34, color=MAG)).next_to(py, RIGHT, buff=0.06).set_z_index(14)
        self.p(Create(pr), GrowArrow(px), GrowArrow(py), FadeIn(lpx), FadeIn(lpy), FadeOut(pq1), FadeOut(pq2), rt=1.2)
        self.w(0.6)
        fundoP = [m for m in self.mobjects if isinstance(m, RoundedRectangle) and abs(m.get_center()[1] + 4.4) < 0.05]
        self.sai(ep1, ep2, ePi, ePf, eIg, *fundoP, rt=0.5)
        YX, YY = -2.65, -5.0
        tx = MathTex("x:", font_size=30, color=DIM).move_to(P3(-3.95, YX))
        ty = MathTex("y:", font_size=30, color=DIM).move_to(P3(-3.95, YY))
        X1 = Eq([("m1", "m_1"), ("v", "v_{1i}", VEL), ("eq", "="), ("M", "M"), ("vx", "v_{fx}", VEL)], 46, pos=P3(0.2, YX))
        Y1 = Eq([("m1", "m_2"), ("v", "v_{2i}", VEL), ("eq", "="), ("M", "M"), ("vx", "v_{fy}", VEL)], 46, pos=P3(0.2, YY))
        self.p(FadeIn(tx), FadeIn(ty), rt=0.4)
        self.nasce(X1, [(lpx, ["m1", "v"]), (self.eM.parte("M"), "M"), (self.d_vx.parte("s"), "vx")], rt=1.4)
        self.nasce(Y1, [(lpy, ["m1", "v"]), (self.eM.parte("M"), "M"), (self.d_vy.parte("s"), "vx")], rt=1.3)
        self.w(1.0)
        # isolar v₁ᵢ (MF-Tools): m₁ atravessa a igualdade e vira denominador
        X2 = Eq([("v", "v_{1i}", VEL), ("eq", "="), ("fr", r"\dfrac{M}{m_1}"), ("vx", "v_{fx}", VEL)], 46, pos=P3(0.2, YX))
        self.passo(X1, X2, ("m1", X2.den("fr"), {"path_arc": 1.6}), ("M", X2.num("fr")), rt=1.6)
        self.w(0.6)
        X3 = Eq([("v", "v_{1i}", VEL), ("eq", "="), ("fr", r"\dfrac{m_1+m_2}{m_1}"), ("vx", "v_{fx}", VEL)], 46, pos=P3(0.2, YX))
        self.passo(X2, X3, (X2.num("fr"), X3.num("fr")), (X2.barra("fr"), X3.barra("fr")), (X2.den("fr"), X3.den("fr")), rt=1.3)
        self.w(0.6)
        X4 = Eq([("v", "v_{1i}", VEL), ("eq", "="), ("fr", r"\dfrac{2000+1000}{2000}"), ("dot", r"\cdot"), ("n", "8")], 46,
                pos=P3(0.2, YX))
        nu, de = X4.num("fr"), X4.den("fr")
        self.p(*[Indicate(m, color=WHITE_, scale_factor=1.15) for m in (self.d_m1.parte("v"), self.d_m2.parte("v"),
                                                                        self.d_vx.parte("v"))], rt=0.7)
        self.substitui(X3, X4, pares=[(X3.barra("fr"), X4.barra("fr")), (X3.num("fr")[2:3], nu[4:5])],
                       copias=[(self.d_m1.parte("v"), nu[0:4]), (self.d_m2.parte("v"), nu[5:9]), (self.d_m1.parte("v"), de),
                               (self.d_vx.parte("v"), "n")], rt=1.7)
        self.w(0.6)
        X5 = Eq([("v", "v_{1i}", VEL), ("eq", "="), ("res", r"12\,\mathrm{m/s}")], 50, pos=P3(0.2, YX))
        self.passo(X4, X5, (["fr", "dot", "n"], "res"), rt=1.3)
        self.w(0.6)
        # isolar v₂ᵢ (mesmo caminho, mais rápido)
        Y2 = Eq([("v", "v_{2i}", VEL), ("eq", "="), ("fr", r"\dfrac{M}{m_2}"), ("vx", "v_{fy}", VEL)], 46, pos=P3(0.2, YY))
        self.passo(Y1, Y2, ("m1", Y2.den("fr"), {"path_arc": 1.6}), ("M", Y2.num("fr")), rt=1.4)
        Y3 = Eq([("v", "v_{2i}", VEL), ("eq", "="), ("fr", r"\dfrac{3000}{1000}"), ("dot", r"\cdot"), ("n", "6")], 46,
                pos=P3(0.2, YY))
        self.substitui(Y2, Y3, pares=[(Y2.barra("fr"), Y3.barra("fr"))],
                       copias=[(self.eM2.parte("v"), Y3.num("fr")), (self.d_m2.parte("v"), Y3.den("fr")),
                               (self.d_vy.parte("v"), "n")], rt=1.5)
        self.w(0.5)
        Y4 = Eq([("v", "v_{2i}", VEL), ("eq", "="), ("res", r"18\,\mathrm{m/s}")], 50, pos=P3(0.2, YY))
        self.passo(Y3, Y4, (["fr", "dot", "n"], "res"), rt=1.2)
        self.w(0.6)
        # fechar o laço: os resultados voltam para as setas
        n1 = rotulo_v(r"\vec v_{1i}", r"12\,\mathrm{m/s}", 36)
        n2 = rotulo_v(r"\vec v_{2i}", r"18\,\mathrm{m/s}", 36)
        contorno(n1.mt.move_to(r1.mt, aligned_edge=LEFT)).set_z_index(14)
        contorno(n2.mt.move_to(r2.mt, aligned_edge=LEFT)).set_z_index(14)
        self.substitui(r1, n1, copias=[(X5.parte("res"), "n")], rt=1.1)
        self.substitui(r2, n2, copias=[(Y4.parte("res"), "n")], rt=1.1)
        self.r1, self.r2 = n1, n2
        self.w(0.6)
        X6 = Eq([("v", "v_{1i}", VEL), ("eq", "="), ("res", r"12\,\mathrm{m/s}"), ("eq2", "="), ("k", r"43{,}2\,\mathrm{km/h}")],
                44, pos=P3(0, YX))
        Y6 = Eq([("v", "v_{2i}", VEL), ("eq", "="), ("res", r"18\,\mathrm{m/s}"), ("eq2", "="), ("k", r"64{,}8\,\mathrm{km/h}")],
                44, pos=P3(0, YY))
        self.sai(tx, ty, rt=0.3)
        self.passo(X5, X6, rt=1.0)
        self.passo(Y4, Y6, rt=1.0)
        self.w(2.0)
        self.c03_fora = [fase, X6, Y6, Pf, lPf, pr, px, py, lpx, lpy]

    # ================================================================ C04 · o triângulo e a pegadinha
    def c04(self):
        mk = marca_mob(self.w2s(ORIGIN), self.w2s(UD * D), w=4.0 * self.S() / 0.62 + 1.0, sep=0.16 * self.S())
        self.add(mk)
        self.remove(self.marca)
        for m in (self.v1, self.v2):
            m.clear_updaters()
        mchip = self.eM2.parte("v").copy()
        self.add(mchip)
        cards = [m for m in self.mobjects if isinstance(m, RoundedRectangle)]
        self.sai(*self.c03_fora, self.setas, self.r1, self.r2, rt=0.6)
        self.p(*self.cab("O TRIÂNGULO E A PEGADINHA"), rt=0.6)
        # o cruzamento sai; a marca vira o 1º dos três triângulos
        Om, sm = P3(-4.0, 2.45), 0.27
        Xm, Qm = Om + P3(8 * sm, 0), Om + P3(8 * sm, 6 * sm)
        hm = marca_mob(Om, Qm, w=3.5, sep=0.06)
        lgm = VGroup(DashedLine(Om, Xm, dash_length=0.08), DashedLine(Xm, Qm, dash_length=0.08)).set_stroke(GEO, 2, opacity=0.8)
        lm = [lab_at(MathTex(r"8\,\mathrm{m}", font_size=32, color=GEO), Om, Xm, lado=-1),
              lab_at(MathTex(r"6\,\mathrm{m}", font_size=32, color=GEO), Xm, Qm, lado=-1),
              lab_at(MathTex(r"10\,\mathrm{m}", font_size=32, color=GEO), Om, Qm, lado=1, gap=0.18)]
        am = arco(Om, 0.45, 0, TH, w=2.2)
        tmar = txt("MARCA", 24, color=GEO).move_to(P3(2.9, 3.75))
        tri_m = VGroup(hm, lgm, *lm, am)
        fora = [self.via, self.v1, self.v2, self.d_m1.m, self.d_m2.m, self.d_mu.m, self.d_g.m, self.f1, self.f2, self.eM.m,
                self.d_vx.m, self.d_vy.m, *cards]
        self.p(*[FadeOut(m) for m in fora], FadeOut(self.eM2.m), ReplacementTransform(mk, hm), FadeIn(lgm),
               *[FadeIn(x) for x in lm], FadeIn(am), FadeIn(tmar), mchip.animate.move_to(P3(3.75, -0.75)), rt=1.6)
        self.remove(*fora, self.eM2.m)
        self.w(0.5)
        # velocidade (violeta) e momento (magenta): mesmo triângulo, outra escala
        nv = [MathTex(r"8\,\mathrm{m/s}", font_size=40), MathTex(r"6\,\mathrm{m/s}", font_size=40),
              MathTex(r"10\,\mathrm{m/s}", font_size=40)]
        tv = self.tri(P3(-4.1, -1.75), 0.58, VEL, VEL_L, nv, 0.8)
        tvel = txt("VELOCIDADE", 24, color=VEL).move_to(P3(2.9, 1.3))
        self.p(TransformFromCopy(VGroup(Line(Om, Xm), Line(Xm, Qm), Line(Om, Qm)), VGroup(tv["hx"], tv["hy"], tv["hh"])),
               TransformFromCopy(VGroup(*lm), VGroup(tv["lx"], tv["ly"], tv["lh"])), TransformFromCopy(am, tv["ang"]),
               FadeIn(tvel), rt=1.4)
        self.w(0.6)
        seta_m = arrow(P3(2.9, 0.85), P3(2.9, -2.35), DIM, 2.5, tip=0.16)
        lm_ = MathTex(r"\times", font_size=36, color=WHITE_).next_to(mchip, LEFT, buff=0.08)
        self.p(GrowArrow(seta_m), FadeIn(lm_), rt=0.7)
        # cada cateto multiplicado por M = 3000 kg
        tp_n0 = [MathTex(r"3000\cdot 8", font_size=40), MathTex(r"3000\cdot 6", font_size=40), MathTex(r"3000\cdot 10", font_size=40)]
        tp = self.tri(P3(-4.1, -6.3), 0.64, MAG, MAG_L, tp_n0, 0.85)
        tmom = VGroup(txt("MOMENTO", 24, color=MAG), MathTex(r"(\mathrm{kg\cdot m/s})", font_size=30, color=DIM)) \
            .arrange(DOWN, buff=0.12).move_to(P3(2.9, -2.95))
        self.p(TransformFromCopy(VGroup(tv["hx"], tv["hy"], tv["hh"], tv["ang"]), VGroup(tp["hx"], tp["hy"], tp["hh"], tp["ang"])),
               *[TransformFromCopy(VGroup(mchip.copy(), src), dst) for src, dst in
                 ((tv["lx"], tp["lx"]), (tv["ly"], tp["ly"]), (tv["lh"], tp["lh"]))],
               FadeIn(tmom), rt=1.8)
        self.w(0.6)
        nm = [Eq([("p", "p_{1i}", MAG), ("eq", "="), ("n", r"24\,000")], 40),
              Eq([("p", "p_{2i}", MAG), ("eq", "="), ("n", r"18\,000")], 40),
              Eq([("p", "P", MAG), ("eq", "="), ("n", r"30\,000")], 40)]
        lab_at(nm[0].mt, tp["O"], tp["X"], lado=-1)
        lab_at(nm[1].mt, tp["X"], tp["Q"], lado=-1)
        lab_at(nm[2].mt, tp["O"], tp["Q"], lado=1, gap=0.2)
        self.p(*[ReplacementTransform(a, e.mt) for a, e in zip((tp["lx"], tp["ly"], tp["lh"]), nm)], rt=1.3)
        for e in nm:
            self.assenta(e)
        self.w(0.8)
        self.p(*[Indicate(a, color=WHITE_, scale_factor=1.3) for a in (am, tv["ang"], tp["ang"])],
               *self.frase("A MESMA DIREÇÃO\nATRAVESSA AS ETAPAS", 22, y=2.55, x=2.9), rt=1.2)
        self.w(1.2)
        # tan θ: os catetos do triângulo de momento voam para a fração
        self.sai(tv["g"], tvel, seta_m, lm_, mchip, rt=0.5)
        tg = Eq([("t", r"\tan\theta"), ("eq", "="), ("fr", r"\dfrac{p_{2i}}{p_{1i}}", ("fr", MAG)), ("eq2", "="),
                 ("fr2", r"\dfrac{18\,000}{24\,000}"), ("eq3", "="), ("fr3", r"\dfrac34")], 46, pos=P3(0, -0.45))
        self.nasce(tg, [(tp["ang"], "t"), (nm[1].parte("p"), tg.num("fr")), (nm[0].parte("p"), tg.den("fr")),
                        (nm[1].parte("n"), tg.num("fr2")), (nm[0].parte("n"), tg.den("fr2"))], rt=1.6,
                   extra=[FadeIn(cartao(VGroup(Rectangle(width=8.0, height=1.3)), 0).move_to(P3(0, -0.45)))])
        self.w(2.2)
        cards = [m for m in self.mobjects if isinstance(m, RoundedRectangle)]
        self.sai(tri_m, tmar, tp["g"], *nm, tmom, tg, self._frase, *cards, rt=0.6)
        self._frase = None
        # contraste: quem é mais rápido × quem tem mais momento
        YB = -3.8
        hv = txt("VELOCIDADE", 26, color=VEL).move_to(P3(-2.25, 2.65))
        hp = VGroup(txt("MOMENTO", 26, color=MAG), MathTex(r"(\mathrm{kg\cdot m/s})", font_size=30, color=DIM)) \
            .arrange(RIGHT, buff=0.14).move_to(P3(2.25, 2.65))
        base = VGroup(Line(P3(-4.0, YB), P3(-0.5, YB)), Line(P3(0.5, YB), P3(4.0, YB))).set_stroke(DIM, 2, opacity=0.6)

        def barra(x, alt, cor, val):
            r = Rectangle(width=1.15, height=alt).set_stroke(mix(cor, 0.4), 1.5).set_fill(cor, 0.85)
            r.move_to(P3(x, YB + alt / 2))
            return r, MathTex(val, font_size=38, color=WHITE_).next_to(r, UP, buff=0.14)
        kv, kp = 5.0 / 18, 5.0 / 24000
        bv1, lv1 = barra(-3.0, V1I * kv, VEL, r"12\,\mathrm{m/s}")
        bv2, lv2 = barra(-1.5, V2I * kv, VEL, r"18\,\mathrm{m/s}")
        bp1, lp1 = barra(1.5, P1I * kp, MAG, r"24\,000")
        bp2, lp2 = barra(3.0, P2I * kp, MAG, r"18\,000")
        nb = VGroup(*[ficha(n, c, 0.2).move_to(P3(x, YB - 0.42)) for n, c, x in
                      ((1, CAR1, -3.0), (2, CAR2, -1.5), (1, CAR1, 1.5), (2, CAR2, 3.0))])
        self.p(FadeIn(hv), FadeIn(hp), Create(base), FadeIn(nb), rt=0.8)
        self.p(GrowFromEdge(bv1, DOWN), GrowFromEdge(bv2, DOWN), FadeIn(lv1), FadeIn(lv2), rt=1.2)
        self.w(0.8)
        self.p(GrowFromEdge(bp1, DOWN), GrowFromEdge(bp2, DOWN), FadeIn(lp1), FadeIn(lp2), rt=1.2)
        self.w(0.8)
        cv = txt("CARRO 2:\nMAIS RÁPIDO", 21, color=VEL).move_to(P3(-2.25, -5.05))
        cp = txt("CARRO 1:\nMAIS MOMENTO", 21, color=MAG).move_to(P3(2.25, -5.05))
        self.p(Create(caixa(VGroup(bv2, lv2), VEL, 0.1, 2.2)), FadeIn(cv), rt=0.9)
        self.w(0.8)
        self.p(Create(caixa(VGroup(bp1, lp1), MAG, 0.1, 2.2)), FadeIn(cp), rt=0.9)
        self.w(1.0)
        self.p(*self.frase("A DIREÇÃO DOS DESTROÇOS DÁ A RAZÃO\nDOS MOMENTOS, NÃO DAS VELOCIDADES", 25, y=-6.3), rt=1.0)
        self.w(2.5)

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

    # ================================================================ C05 · conferência de ida e volta
    def c05(self):
        fora = [m for m in self.mobjects if m not in self.fixos | {self.linha, self.head}]
        self.sai(*fora, rt=0.6)
        self._frase = None
        self.por_vista("MEIO")
        self.tt.set_value(T0)
        self.ligar_carros()
        setas, r1, r2 = self.setas_antes(r"12\,\mathrm{m/s}", r"18\,\mathrm{m/s}")
        self.ct = self.cotas(sim=True)
        self.p(*self.linha.ir(0), *self.cab("CONFERÊNCIA DE IDA E VOLTA"), FadeIn(self.via), FadeIn(self.marca),
               FadeIn(self.v1), FadeIn(self.v2), FadeIn(setas), FadeIn(r1.mt), FadeIn(r2.mt), FadeIn(self.ct["ld"].mt), rt=1.0)
        self.assenta(r1), self.assenta(r2), self.assenta(self.ct["ld"])
        ys = (-3.45, -4.15, -4.85)
        l1 = Eq([("a", r"\vec v_{1i}", VEL), ("b", r"=12,\ "), ("c", r"\vec v_{2i}", VEL), ("d", r"=18\ (\mathrm{m/s})")], 34,
                pos=P3(0, ys[0]))
        l2 = Eq([("a", r"\vec P_i", MAG), ("b", r"=(24\,000;\ 18\,000)\ \mathrm{kg\cdot m/s}")], 34, pos=P3(0, ys[1]))
        l3 = Eq([("a", r"\vec v_f", VEL), ("b", "="), ("c", r"\vec P_i", MAG), ("d", r"/M=(8;\ 6)\ \mathrm{m/s}")], 34, pos=P3(0, ys[2]))
        l4 = Eq([("d", "d", GEO), ("b", "="), ("c", r"v_f^2", VEL), ("e", r"/(2\mu_k g)="), ("n", r"10", GEO), ("u", r"\,\mathrm{m}", GEO)],
                48, pos=P3(0, -5.85))
        self.nasce(l1, [(r1.parte("v"), "a"), (r2.parte("v"), "c")], rt=0.8)
        self.p(FadeOut(setas), FadeOut(r1.m), FadeOut(r2.m), self.tt.animate.set_value(0.0), *self.linha.ir(1),
               rt=1.6, rate_func=linear)
        c, an = self.anel_impacto()
        self.add(c)
        self.p(an, self.flash(), l1.m.animate.set_opacity(0.4), FadeIn(l2.mt, shift=0.1 * UP), rt=0.7)
        self.remove(c)
        self.assenta(l2)
        self.p(l2.m.animate.set_opacity(0.4), FadeIn(l3.mt, shift=0.1 * UP), rt=0.7)
        self.assenta(l3)
        rastro = always_redraw(lambda: marca_mob(self.w2s(ORIGIN), self.w2s(UD * s_desl(self.tt.get_value())), w=2.4,
                                                 sep=0.16 * self.S(), cor=VEL, op=1.0).set_z_index(2))
        self.add(rastro)
        self.p(self.tt.animate.set_value(TSTOP), *self.linha.ir(2), l3.m.animate.set_opacity(0.4), rt=3.0, rate_func=linear)
        rastro.clear_updaters()
        self.p(*self.linha.ir(3), FadeIn(l4.mt, shift=0.1 * UP), FadeIn(cartao(l4.mt, 0.18)), rt=0.9)
        self.assenta(l4)
        # o d calculado volta para a cota da marca, que pisca com ✓
        alvo = self.ct["ld"]
        ok = contorno(MathTex(r"\checkmark", font_size=56, color=WHITE_)).next_to(alvo.mt, LEFT, buff=0.15).set_z_index(16)
        self.p(TransformFromCopy(VGroup(l4.parte("d"), l4.parte("n"), l4.parte("u")), alvo.mt.copy().set_opacity(0)),
               Indicate(alvo.mt, color=WHITE_, scale_factor=1.25), FadeIn(ok), rt=1.1)
        self.w(1.4)

    # ================================================================ C06 · e a energia?
    def c06(self):
        mk = marca_mob(self.w2s(ORIGIN), self.w2s(UD * D), w=4.0 * self.S() / 0.62 + 1.0, sep=0.16 * self.S())
        self.add(mk)
        self.remove(self.marca)
        for m in (self.v1, self.v2):
            m.clear_updaters()
        mapa = Group(self.via, mk, self.v1, self.v2)
        fora = [m for m in self.mobjects if m not in self.fixos | {self.linha, self.head, self.via, mk, self.v1, self.v2}]
        self.sai(*fora, rt=0.6)
        self.p(*self.cab("E A ENERGIA?"), mapa.animate.scale(0.3).move_to(P3(0, 3.55)), rt=1.2)
        q = txt("O MOMENTO SE CONSERVOU. E A ENERGIA?", 24).move_to(P3(0, 2.4))
        self.p(FadeIn(q, shift=0.1 * UP), rt=0.8)
        # fichas com o que já se sabe (as variáveis vão viajar delas)
        fm1 = Eq([("m", "m_1"), ("eq", "="), ("v", "2000")], 34)
        fv1 = Eq([("v", "v_{1i}", VEL), ("eq", "="), ("n", "12")], 34)
        fm2 = Eq([("m", "m_2"), ("eq", "="), ("v", "1000")], 34)
        fv2 = Eq([("v", "v_{2i}", VEL), ("eq", "="), ("n", "18")], 34)
        fM = Eq([("m", "M"), ("eq", "="), ("v", "3000")], 34)
        fvf = Eq([("v", "v_f", VEL), ("eq", "="), ("n", "10")], 34)
        g1 = VGroup(ficha(1, CAR1, 0.15), fm1.mt, fv1.mt).arrange(RIGHT, buff=0.18)
        g2 = VGroup(ficha(2, CAR2, 0.15), fm2.mt, fv2.mt).arrange(RIGHT, buff=0.18)
        g3 = VGroup(fM.mt, fvf.mt).arrange(RIGHT, buff=0.3)
        fil = VGroup(VGroup(g1, g2).arrange(RIGHT, buff=0.5), g3).arrange(DOWN, buff=0.18)
        if fil.width > 8.3:
            fil.scale_to_fit_width(8.3)
        fil.move_to(P3(0, 1.5))
        self.p(FadeIn(fil), rt=0.8)
        for e in (fm1, fv1, fm2, fv2, fM, fvf):
            self.assenta(e)
        # K_antes: m e v viajam das fichas
        YA = 0.3
        eA = Eq([("K", r"K_{\mathrm{antes}}", CYAN), ("eq", "="), ("h1", r"\tfrac12"), ("m1", "m_1"), ("v1", "v_{1i}^2", VEL),
                 ("pl", "+"), ("h2", r"\tfrac12"), ("m2", "m_2"), ("v2", "v_{2i}^2", VEL)], 42, pos=P3(0, YA))
        self.nasce(eA, [(fm1.parte("m"), "m1"), (fv1.parte("v"), ("v1", slice(0, 3))), (fm2.parte("m"), "m2"),
                        (fv2.parte("v"), ("v2", slice(0, 3)))], rt=1.4)
        self.w(0.6)
        eA2 = Eq([("K", r"K_{\mathrm{antes}}", CYAN), ("eq", "="), ("h1", r"\tfrac12"), ("m1", r"\cdot 2000\cdot"), ("v1", "12^2"),
                  ("pl", "+"), ("h2", r"\tfrac12"), ("m2", r"\cdot 1000\cdot"), ("v2", "18^2")], 40, pos=P3(0, YA))
        self.substitui(eA, eA2, pares=[(("v1", 3), ("v1", 2)), (("v2", 3), ("v2", 2))],
                       copias=[(fm1.parte("v"), ("m1", slice(1, 5))), (fv1.parte("n"), ("v1", slice(0, 2))),
                               (fm2.parte("v"), ("m2", slice(1, 5))), (fv2.parte("n"), ("v2", slice(0, 2)))], rt=1.6)
        self.w(0.6)
        eA3 = Eq([("K", r"K_{\mathrm{antes}}", CYAN), ("eq", "="), ("a", r"144", CAR1_L), ("pl", "+"), ("b", "162", CAR2_L),
                  ("eq2", "="), ("t", r"306\,\mathrm{kJ}", CYAN)], 44, pos=P3(0, YA))
        self.passo(eA2, eA3, (["h1", "m1", "v1"], "a"), (["h2", "m2", "v2"], "b"), rt=1.5)
        self.w(0.5)
        # barras (mesma escala): as parcelas voam para a barra
        KS, X0 = 0.025, -3.8
        YBa, YBd = -0.85, -2.45

        def seg(k0, k1, y, cor, op=0.85):
            r = Rectangle(width=(k1 - k0) * KS, height=0.6).set_stroke(mix(cor, 0.4), 1.5).set_fill(cor, op)
            return r.move_to(P3(X0 + (k0 + k1) / 2 * KS, y))
        a1, a2 = seg(0, 144, YBa, CAR1), seg(144, 306, YBa, CAR2)
        ta1 = MathTex("144", font_size=34, color=WHITE_).move_to(a1)
        ta2 = MathTex("162", font_size=34, color=WHITE_).move_to(a2)
        self.p(GrowFromEdge(a1, LEFT), GrowFromEdge(a2, LEFT), TransformFromCopy(eA3.parte("a"), ta1),
               TransformFromCopy(eA3.parte("b"), ta2), rt=1.3)
        self.w(0.5)
        # K_depois: M e v_f viajam das fichas
        YD = -1.65
        eD = Eq([("K", r"K_{\mathrm{depois}}", CYAN), ("eq", "="), ("h", r"\tfrac12"), ("M", "M"), ("v", "v_f^2", VEL), ("eq2", "="),
                 ("h2", r"\tfrac12\cdot 3000\cdot 10^2"), ("eq3", "="), ("t", r"150\,\mathrm{kJ}", CYAN)], 40, pos=P3(0, YD))
        hh2 = sorted(eD.idx["h2"], key=lambda i: eD.gl[i].get_left()[0])
        self.nasce(eD, [(fM.parte("m"), "M"), (fvf.parte("v"), ("v", slice(0, 2))), (fM.parte("v"), hh2[4:8]),
                        (fvf.parte("n"), hh2[9:11])], rt=1.6)
        self.w(0.6)
        d1 = seg(0, 150, YBd, CYAN, 0.75)
        td = MathTex("150", font_size=34, color=BACKGROUND_COLOR).move_to(d1)
        self.p(GrowFromEdge(d1, LEFT), TransformFromCopy(eD.parte("t")[0:3], td), rt=1.1)
        self.w(0.6)
        # o que falta: 156 kJ convertidos (laranja)
        fal = seg(150, 306, YBa, HEAT, 0.0).set_stroke(HEAT, 3)
        self.p(Create(fal), rt=0.5)
        laranja = seg(150, 306, YBd, HEAT, 0.88)
        self.p(ReplacementTransform(fal, laranja), rt=1.1)
        eDK = Eq([("dk", r"\Delta K", HEAT), ("eq", "="), ("a", r"K_{\mathrm{antes}}", CYAN), ("m", "-"), ("b", r"K_{\mathrm{depois}}", CYAN),
                  ("eq2", "="), ("t", r"156\,\mathrm{kJ}\approx 51\,\%", HEAT)], 40, pos=P3(0, -3.35))
        self.nasce(eDK, [(eA3.parte("K"), "a"), (eD.parte("K"), "b")], rt=1.4,
                   extra=[FadeIn(cartao(VGroup(Rectangle(width=8.1, height=0.85)), 0, cor=HEAT).move_to(P3(0, -3.35)))])
        destinos = txt("DEFORMAÇÃO · CALOR · SOM · VIBRAÇÃO", 23, color=HEAT).move_to(P3(0, -4.3))
        gotas = VGroup(*[Dot(laranja.get_center() + P3(dx, 0), radius=0.06, color=HEAT) for dx in (-1.2, -0.4, 0.4, 1.2)])
        self.p(*[d.animate.move_to(P3(-2.9 + 1.93 * i, -4.0)).set_opacity(0) for i, d in enumerate(gotas)],
               FadeIn(destinos, shift=0.1 * DOWN), rt=1.1)
        self.remove(gotas)
        self.w(1.0)
        self.p(*self.frase("MOMENTO SE CONSERVA.\nENERGIA CINÉTICA, NÃO.", 30, y=-5.5), rt=1.0)
        self.w(2.5)

    # ================================================================ C07 · cada intervalo, sua lei
    def c07(self):
        mobs = [m for m in self.mobjects if m not in self.fixos | {self.linha, self.head}]
        self._frase = None
        L = self.linha
        self.sai(*mobs, rt=0.6)
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
               Create(lm), Create(le), FadeIn(VGroup(cm, bm)), FadeIn(VGroup(ce, be)), rt=1.2)
        self.w(1.2)
        # ponte: colisão elástica (insinuação neutra: momentos com ângulo ≠ 90° e um círculo completo esmaecido)
        pp, lam, th1 = 7.0, 0.5, 28.0
        O = P3(-3.5, -0.9)
        cx, R = pp / (1 + lam), lam * pp / (1 + lam)
        dmax = cx * np.cos(np.radians(th1)) + np.sqrt(R * R - (cx * np.sin(np.radians(th1))) ** 2)
        Q, Tp = O + pol(dmax, th1), O + P3(pp, 0)
        ang12 = np.degrees(np.arccos(np.dot(unit(Q - O), unit(Tp - Q))))
        assert abs(np.linalg.norm(Q - (O + P3(cx, 0))) - R) < 1e-9 and abs(ang12 - 90) > 15
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
        self.w(2.4)
