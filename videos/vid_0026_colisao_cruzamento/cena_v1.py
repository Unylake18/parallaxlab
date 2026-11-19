"""vid_0026 — O que uma marca no asfalto consegue contar sobre uma batida? (preview silencioso v1).

Curto vertical, Manim 2D. Cruzamento visto de cima: veículo 1 (2000 kg) vem do oeste, veículo 2 (1000 kg) vem do sul,
ficam unidos e deslizam 8 m para leste e 6 m para norte. De trás para frente: trabalho–energia no deslizamento,
momento no impacto; depois a conferência de ida e volta e a energia.
Gramática visual dos longos de colisões (yt_0013/yt_0014): velocidade violeta · momento magenta · energia convertida laranja ·
corpos em aço chato · ângulos em arco branco fino · régua de fases.

Preview 540×960 / 15 fps:
    uv run python -m manim -r 540,960 --fps 15 videos/vid_0026_colisao_cruzamento/cena.py ColisaoCruzamento026
Só alguns blocos: SECOES=c03,c04 (os outros rodam sem animar, para manter o estado). Ritmo por bloco: ESTICA.
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

# ── paleta (yt_0014 + handoff) ──────────────────────────────────────────────────────────────────────────────
WHITE_ = TEXT_COLOR
CYAN = PRIMARY_COLOR          # só na insinuação do círculo (C07)
VEL = "#9C8CFF"               # velocidade
MAG = "#EA63FF"               # momento
HEAT = "#FF7A3D"              # energia convertida (único tom quente)
STEEL = "#7A8696"             # corpo 2
GEO = "#B8C4DA"               # aço claro: corpo 1
DIM = "#8FA3C4"               # convenções, texto secundário
MARK = "#D9DEE8"              # marca no asfalto (distância)
C1F, C2F = GEO, STEEL


def mix(c, w):
    return interpolate_color(ManimColor(c), ManimColor(WHITE_), w).to_hex()


def _fundo(w):
    return interpolate_color(ManimColor(BACKGROUND_COLOR), ManimColor(WHITE_), w)


VEL_L, MAG_L = mix(VEL, 0.3), mix(MAG, 0.3)
JUNTOS = interpolate_color(ManimColor(GEO), ManimColor(STEEL), 0.5).to_hex()   # o conjunto (K_depois)

SECOES = [s.strip() for s in os.environ.get("SECOES", "").split(",") if s.strip()]
# ritmo de cada bloco (multiplica todas as durações do bloco; a voz ajusta depois)
ESTICA = {"c01": 1.0, "c02": 1.0, "c03": 1.0, "c04": 1.0, "c05": 1.0, "c06": 1.0, "c07": 1.0}

# ── física (congelada) ──────────────────────────────────────────────────────────────────────────────────────
M1, M2, MU, G = 2000.0, 1000.0, 0.5, 10.0
DX, DY = 8.0, 6.0
D = float(np.hypot(DX, DY))
VF = float(np.sqrt(2 * MU * G * D))
VFX, VFY = VF * DX / D, VF * DY / D
V1I, V2I = (M1 + M2) * VFX / M1, (M1 + M2) * VFY / M2
P1I, P2I = M1 * V1I, M2 * V2I
KA = 0.5 * M1 * V1I ** 2 + 0.5 * M2 * V2I ** 2
KD = 0.5 * (M1 + M2) * VF ** 2
TH = float(np.degrees(np.arctan2(DY, DX)))
assert abs(D - 10) < 1e-12 and abs(VF - 10) < 1e-12 and abs(VFX - 8) < 1e-12 and abs(VFY - 6) < 1e-12
assert abs(V1I - 12) < 1e-9 and abs(V2I - 18) < 1e-9 and abs(P1I - 24000) < 1e-6 and abs(P2I - 18000) < 1e-6
assert abs(np.hypot(P1I, P2I) - 30000) < 1e-6 and abs(KA - 306000) < 1e-6 and abs(KD - 150000) < 1e-6
assert abs(V1I * 3.6 - 43.2) < 1e-9 and abs(V2I * 3.6 - 64.8) < 1e-9 and abs((KA - KD) / KA - 0.5098) < 1e-3

# ── mapa (vista superior) ───────────────────────────────────────────────────────────────────────────────────
KM = 0.36                                   # tela por metro
P0 = np.array([-1.7, 1.7, 0.0])              # ponto do impacto (início da marca)
UD = np.array([DX / D, DY / D, 0.0])         # direção da marca = direção de v⃗_f
E = P0 + UD * D * KM                         # fim da marca
W1, H1, W2, H2 = 1.15, 0.62, 0.52, 0.95       # veículo 1 (deitado, vai para leste) e 2 (em pé, vai para norte)
C1 = P0 + np.array([0, H1 / 2, 0])           # centros no instante do contato
C2 = P0 + np.array([0, -H2 / 2, 0])
T0 = -0.18                                   # s antes do impacto em que a cena começa
A_ = MU * G                                  # desaceleração no deslizamento (5 m/s²)
TSTOP = VF / A_                              # 2 s
AK = 0.07                                    # tela por (m/s) nas setas de velocidade


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


def pos1(t):
    return C1 + (P3(V1I * KM * t, 0) if t <= 0 else UD * s_desl(t) * KM)


def pos2(t):
    return C2 + (P3(0, V2I * KM * t) if t <= 0 else UD * s_desl(t) * KM)


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


COR = {r"\vec v_{1i}": VEL, r"\vec v_{2i}": VEL, r"\vec v_f": VEL, "v_{1i}": VEL, "v_{2i}": VEL, "v_f": VEL,
       "v_f^2": VEL, "v_{fx}": VEL, "v_{fy}": VEL, r"\vec P_i": MAG, r"\vec P_f": MAG, "p_{1i}": MAG, "p_{2i}": MAG,
       r"\vec P": MAG, "P": MAG}


def T(*parts, size=44, w=8.2, color=WHITE_):
    """MathTex em partes; cada parte que está em COR recebe a cor da grandeza (o resto fica branco)."""
    m = MathTex(*parts, font_size=size, color=color)
    for sub, p in zip(m, parts):
        if p in COR:
            sub.set_color(COR[p])
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def arrow(a, b, color=WHITE_, width=5, z=8, tip=0.2):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if np.linalg.norm(b - a) < 0.03:
        return VMobject()
    return Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.45,
                 max_stroke_width_to_length_ratio=50).set_z_index(z)


def lab_at(m, a, b, lado=1, gap=0.14):
    """Rótulo ao lado do segmento a→b (lado=+1: à esquerda de a→b), com contorno escuro."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = unit(b - a)
    nrm = np.array([-d[1], d[0], 0.0]) * lado
    meia = 0.5 * (abs(nrm[0]) * m.width + abs(nrm[1]) * m.height)
    m.move_to((a + b) / 2 + nrm * (gap + meia))
    return m.set_stroke(BACKGROUND_COLOR, 6, background=True).set_z_index(14)


def arco(c, r, a0, a1, w=1.8, op=0.95):
    return Arc(radius=r, start_angle=np.radians(a0), angle=np.radians(a1 - a0), arc_center=np.asarray(c, float)) \
        .set_stroke(WHITE_, w, opacity=op).set_z_index(9)


def caixa(m, color=WHITE_, buff=0.16, width=2.0, op=1.0):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=width, corner_radius=0.1).set_stroke(opacity=op)


class Corpo(VGroup):
    """Veículo visto de cima, aço chato (como no yt_0014), com o nome da massa dentro."""

    def __init__(self, cor, w, h, nome=None, size=26):
        super().__init__()
        f = RoundedRectangle(corner_radius=0.06, width=w, height=h).set_stroke(mix(cor, 0.5), 2).set_fill(cor, 1.0)
        ins = min(0.07, 0.12 * min(w, h))
        filete = RoundedRectangle(corner_radius=0.03, width=w - 2 * ins, height=h - 2 * ins) \
            .set_stroke(WHITE_, 1, opacity=0.35).set_fill(opacity=0).move_to(f)
        self.front = f
        self.add(f, filete)
        if nome:
            self.add(MathTex(nome, font_size=size, color=BACKGROUND_COLOR if cor == GEO else WHITE_).move_to(f))
        self.set_z_index(10)


def cota(a, b, rotulo, lado, size=30):
    """Linha de cota a→b com traços nas pontas e rótulo ao lado."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = unit(b - a)
    n = np.array([-d[1], d[0], 0.0]) * 0.1
    linha = VGroup(Line(a, b), Line(a - n, a + n), Line(b - n, b + n)).set_stroke(MARK, 2, opacity=0.85)
    lab = lab_at(MathTex(rotulo, font_size=size, color=WHITE_), a, b, lado=lado, gap=0.12)
    return VGroup(linha, lab)


def triangulo(O, s, cor, cor_l, nomes, size=28, wl=4, wh=6):
    """Triângulo 3–4–5 de vetores: perna x (O → O+8s), perna y (vertical) e hipotenusa (O → O+(8s, 6s)); arco em O."""
    O = np.asarray(O, float)
    X, Q = O + P3(8 * s, 0), O + P3(8 * s, 6 * s)
    hx = arrow(O, X, cor_l, wl, tip=0.16)
    hy = arrow(X, Q, cor_l, wl, tip=0.16)
    hh = arrow(O, Q, cor, wh, tip=0.2, z=9)
    lx = lab_at(nomes[0], O, X, lado=-1)
    ly = lab_at(nomes[1], X, Q, lado=-1)
    lh = lab_at(nomes[2], O, Q, lado=1)
    ang = arco(O, 0.55, 0, TH)
    return dict(hx=hx, hy=hy, hh=hh, lx=lx, ly=ly, lh=lh, ang=ang, O=O, X=X, Q=Q,
                g=VGroup(hx, hy, hh, lx, ly, lh, ang))


class Linha(VGroup):
    """Régua física ANTES → IMPACTO → DESLIZAMENTO → PAROU; um ponto marca o instante investigado."""
    XS = (-3.25, -1.2, 1.25, 3.4)

    def __init__(self, y=5.0):
        super().__init__()
        self.y = y
        self.rot = [txt(s, 21) for s in ("ANTES", "IMPACTO", "DESLIZAMENTO", "PAROU")]
        for r, x in zip(self.rot, self.XS):
            r.move_to(P3(x, y + 0.33))
        trilho = Line(P3(-3.95, y), P3(3.95, y)).set_stroke(DIM, 2, opacity=0.5)
        ticks = VGroup(*[Line(P3(x, y - 0.07), P3(x, y + 0.07)).set_stroke(DIM, 2, opacity=0.8) for x in self.XS])
        self.dot = Dot(P3(self.XS[3], y), radius=0.085, color=WHITE_).set_z_index(30)
        self.add(trilho, ticks, *self.rot, self.dot)
        self.k = 3
        self._acende(3)

    def _acende(self, k):
        for i, r in enumerate(self.rot):
            r.set_opacity(1.0 if i == k else 0.38)

    def ir(self, k):
        """Animações para levar o ponto ao estado k (o ponto percorre a régua no sentido que for preciso)."""
        self.k = k
        return [self.dot.animate.move_to(P3(self.XS[k], self.y))] + \
            [r.animate.set_opacity(1.0 if i == k else 0.38) for i, r in enumerate(self.rot)]


class ColisaoCruzamento026(Scene):
    # ------------------------------------------------------------------ utilidades
    def p(self, *anims, rt=1.0, **kw):
        self.play(*anims, run_time=rt * self.K, **kw)

    def w(self, t):
        self.wait(t * self.K)

    def cab(self, s, size=32):
        """Cabeçalho do bloco (y = 6.3): o anterior sai e o novo entra na mesma animação."""
        anims = []
        if self.head is not None:
            anims.append(FadeOut(self.head))
        self.head = txt(s, size, width=8.0).move_to(P3(0, 6.3)).set_z_index(20) if s else None
        if self.head is not None:
            anims.append(FadeIn(self.head, shift=0.1 * DOWN))
        return anims

    def frase(self, s, size=24, y=-7.05, color=WHITE_):
        """Frase de tela na faixa inferior (uma por vez)."""
        anims = []
        if self._frase is not None:
            anims.append(FadeOut(self._frase))
        self._frase = txt(s, size, color=color).move_to(P3(0, y)).set_z_index(20) if s else None
        if self._frase is not None:
            anims.append(FadeIn(self._frase, shift=0.1 * UP))
        return anims

    def flash(self):
        return Flash(P0, color=WHITE_, line_length=0.22, flash_radius=0.12, num_lines=10)

    def setas_antes(self, rot1, rot2):
        """Setas violeta de v⃗₁ᵢ e v⃗₂ᵢ na posição de partida (t = T0), com rótulos."""
        a1 = pos1(T0) + P3(W1 / 2 + 0.06, 0)
        a2 = pos2(T0) + P3(0, H2 / 2 + 0.06)
        s1 = arrow(a1, a1 + P3(V1I * AK, 0), VEL, 5, tip=0.18)
        s2 = arrow(a2, a2 + P3(0, V2I * AK), VEL, 5, tip=0.18)
        l1 = T(*rot1, size=28).next_to(pos1(T0) + P3(0, H1 / 2), UP, buff=0.14).set_stroke(BACKGROUND_COLOR, 6, background=True)
        l1.shift(RIGHT * max(0, -4.1 - l1.get_left()[0]))
        l2 = T(*rot2, size=28).next_to(s2, RIGHT, buff=0.14).set_stroke(BACKGROUND_COLOR, 6, background=True)
        return VGroup(s1, s2), VGroup(l1, l2)

    # ------------------------------------------------------------------ cena
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.8).set_opacity(0.35).to_corner(UR, buff=0.28).set_z_index(40)
        tag = txt("EXERCÍCIO RESOLVIDO · EP. 9", 20, op=0.65).to_corner(UL, buff=0.4).set_z_index(40)
        self.add(wm, tag)
        self.fixos = {wm, tag}
        self.head, self._frase = None, None
        self.montar_mapa()
        marcas = []
        for nome in ("c01", "c02", "c03", "c04", "c05", "c06", "c07"):
            self.K = ESTICA[nome]
            self.next_section(nome, skip_animations=bool(SECOES) and nome not in SECOES)
            t0 = self.renderer.time
            getattr(self, nome)()
            marcas.append((nome, t0, self.renderer.time))
        for nome, a, b in marcas:
            print(f"[tempo] {nome}: {a:6.1f} s -> {b:6.1f} s ({b - a:5.1f} s)")

    def montar_mapa(self):
        # vias: faixa leste–oeste (veículo 1) e norte–sul (veículo 2)
        yv = C1[1] - 0.15
        h = Rectangle(width=9.4, height=1.5).move_to(P3(0, yv))
        v = Rectangle(width=1.5, height=5.0).move_to(P3(P0[0], 2.05))
        try:
            via = Union(h, v)
        except Exception:
            via = VGroup(h, v)
        via.set_fill([_fundo(0.11), _fundo(0.05)], opacity=1.0).set_stroke(DIM, 1.4, opacity=0.45).set_z_index(-3)
        faixas = VGroup(DashedLine(P3(-4.6, yv), P3(P0[0] - 0.85, yv), dash_length=0.2),
                        DashedLine(P3(P0[0] + 0.85, yv), P3(4.6, yv), dash_length=0.2),
                        DashedLine(P3(P0[0], -0.4), P3(P0[0], yv - 0.85), dash_length=0.2),
                        DashedLine(P3(P0[0], yv + 0.85), P3(P0[0], 4.5), dash_length=0.2)) \
            .set_stroke(WHITE_, 1.2, opacity=0.22).set_z_index(-2)
        o = P3(3.55, 0.05)
        bus = VGroup(arrow(o, o + P3(0, 0.6), DIM, 2.5, tip=0.13), arrow(o, o + P3(0.6, 0), DIM, 2.5, tip=0.13),
                     txt("N", 18, color=DIM).move_to(o + P3(0, 0.85)), txt("L", 18, color=DIM).move_to(o + P3(0.85, 0)))
        self.via = VGroup(via, faixas, bus)
        # veículos e relógio físico
        self.tt = ValueTracker(TSTOP)
        self.v1 = Corpo(C1F, W1, H1, "m_1", 26)
        self.v2 = Corpo(C2F, W2, H2, "m_2", 22)
        self.v1.add_updater(lambda m: m.move_to(pos1(self.tt.get_value())))
        self.v2.add_updater(lambda m: m.move_to(pos2(self.tt.get_value())))
        self.v1.move_to(pos1(TSTOP))
        self.v2.move_to(pos2(TSTOP))
        self.marca = always_redraw(lambda: self._marca(s_desl(self.tt.get_value())))
        # cotas da marca (fora dos corpos) e ângulo
        self.c8 = cota(P0 + P3(0, -0.62), P3(E[0], P0[1] - 0.62), r"8\ \mathrm{m}", -1)
        self.c6 = cota(P3(E[0] + 0.85, P0[1]), P3(E[0] + 0.85, E[1]), r"6\ \mathrm{m}", -1)
        self.c10 = lab_at(MathTex(r"10\ \mathrm{m}", font_size=30, color=WHITE_), P0, E, lado=1, gap=0.3)
        self.ref = DashedLine(P0, P0 + P3(0.95, 0), dash_length=0.1).set_stroke(DIM, 1.6, opacity=0.8).set_z_index(9)
        self.ang = arco(P0, 0.62, 0, TH)
        self.lth = MathTex(r"\theta", font_size=28, color=WHITE_).move_to(P0 + pol(0.88, TH / 2)) \
            .set_stroke(BACKGROUND_COLOR, 5, background=True).set_z_index(14)
        self.cotas = VGroup(self.c8, self.c6, self.c10)
        self.angulo = VGroup(self.ref, self.ang, self.lth)

    def _marca(self, s, cor=MARK, w=3.0, op=0.85):
        """Marca de deslizamento: dois traços paralelos do impacto até onde o conjunto chegou."""
        if s < 1e-3:
            return VGroup()
        n = np.array([-UD[1], UD[0], 0.0]) * 0.07
        b = P0 + UD * s * KM
        return VGroup(Line(P0 + n, b + n), Line(P0 - n, b - n)).set_stroke(cor, w, opacity=op).set_z_index(1)

    def limpa(self, *keep, rt=0.7):
        keep = self.fixos | {self.linha} | set(keep)
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.p(*[FadeOut(m) for m in mobs], rt=rt)
        self.remove(*mobs)

    # ================================================================ C01 · mistério
    def c01(self):
        self.linha = Linha()
        self.p(FadeIn(self.via), *self.cab("O QUE UMA MARCA NO ASFALTO\nCONSEGUE CONTAR SOBRE UMA BATIDA?", 30), rt=1.2)
        self.p(FadeIn(self.v1), FadeIn(self.v2), FadeIn(self.marca), FadeIn(self.linha), rt=1.0)
        self.w(1.0)
        # de onde vinham (sem valores): 1 do oeste, 2 do sul
        g1 = DashedLine(P3(-4.3, C1[1]), P3(-3.2, C1[1]), dash_length=0.12).set_stroke(DIM, 2, opacity=0.7)
        g2 = DashedLine(P3(P0[0], -0.35), P3(P0[0], 0.45), dash_length=0.12).set_stroke(DIM, 2, opacity=0.7)
        t1 = arrow(P3(-3.4, C1[1]), P3(-3.1, C1[1]), DIM, 2, tip=0.14)
        t2 = arrow(P3(P0[0], 0.3), P3(P0[0], 0.6), DIM, 2, tip=0.14)
        n1 = MathTex("1", font_size=28, color=DIM).next_to(g1, UP, buff=0.1)
        n2 = MathTex("2", font_size=28, color=DIM).next_to(g2, LEFT, buff=0.12)
        self.fantasmas = VGroup(g1, g2, t1, t2, n1, n2)
        self.p(FadeIn(self.fantasmas), rt=0.8)
        self.w(0.8)
        self.p(FadeIn(self.c8), rt=1.0)
        self.p(FadeIn(self.c6), rt=1.0)
        self.p(FadeIn(self.c10), FadeIn(self.angulo), rt=1.0)
        self.w(1.0)
        # os dados não são só a marca
        self.dados = VGroup(
            T(r"m_1=2000\ \mathrm{kg}", r"\qquad", r"m_2=1000\ \mathrm{kg}", size=40),
            T(r"\mu_k=0{,}50", r"\qquad", r"g=10\ \mathrm{m/s^2}", size=40)).arrange(DOWN, buff=0.3).move_to(P3(0, -1.9))
        self.p(FadeIn(self.dados, shift=0.1 * UP), rt=1.0)
        self.w(1.5)
        self.pergunta = T("v_{1i}", r"=\ ?", r"\qquad", "v_{2i}", r"=\ ?", size=56).move_to(P3(0, -3.9))
        self.p(FadeIn(self.pergunta, shift=0.1 * UP), rt=0.9)
        self.w(1.2)
        self.hip = VGroup(txt("IMPACTO CURTO · MESMO ATRITO · MARCA EM LINHA RETA", 19, color=DIM),
                          txt("MODELO IDEALIZADO, NÃO PERÍCIA", 18, color=DIM, op=0.6)).arrange(DOWN, buff=0.2) \
            .move_to(P3(0, -5.6))
        self.p(FadeIn(self.hip), rt=0.8)
        self.w(2.0)

    # ================================================================ C02 · começar pelo fim
    def c02(self):
        tira = VGroup(
            T(r"m_1=2000\ \mathrm{kg}", r"\quad", r"m_2=1000\ \mathrm{kg}", size=30),
            T(r"\mu_k=0{,}50", r"\quad", r"g=10\ \mathrm{m/s^2}", size=30)).arrange(DOWN, buff=0.16).move_to(P3(0, -1.1))
        tira.set_opacity(0.8)
        self.p(*self.linha.ir(2), *self.cab("COMEÇAR PELO FIM"), FadeOut(self.pergunta), FadeOut(self.hip),
               FadeOut(self.fantasmas), FadeOut(self.cotas), FadeOut(self.angulo), Transform(self.dados, tira), rt=1.5)
        # replay curto do deslizamento: volta ao impacto e desenha a marca de novo
        self.p(self.tt.animate.set_value(0.0), rt=1.4, rate_func=linear)
        self.w(0.3)
        self.p(self.flash(), rt=0.4)
        self.p(self.tt.animate.set_value(TSTOP), rt=3.0, rate_func=linear)
        self.marca.clear_updaters()                          # a marca fica como evidência
        self.w(0.5)
        # trabalho–energia no deslizamento
        Y1, Y2 = -2.75, -3.85
        eqA = T("0", "-", r"\tfrac12", "M", "v_f^2", "=", "-", r"\mu_k", "M", "g", "d", size=50).move_to(P3(0, Y1))
        mdef = T("M", "=", "m_1+m_2", size=34, color=DIM).move_to(P3(0, Y2))
        self.p(FadeIn(eqA, shift=0.1 * UP), FadeIn(mdef), rt=1.2)
        self.w(1.5)
        eqB = T(r"\tfrac12", "M", "v_f^2", "=", r"\mu_k", "M", "g", "d", size=54).move_to(P3(0, Y1))
        self.p(TransformMatchingTex(eqA, eqB), rt=1.5)
        self.w(0.8)
        riscos = VGroup(*[Line(eqB[i].get_corner(DL) + P3(-0.05, -0.05), eqB[i].get_corner(UR) + P3(0.05, 0.05))
                          .set_stroke(WHITE_, 4) for i in (1, 5)])
        self.p(Create(riscos), *self.frase("A MASSA TOTAL CANCELA"), rt=1.0)
        self.w(1.5)
        eqC = T("v_f^2", "=", "2", r"\mu_k", "g", "d", size=54).move_to(P3(0, Y1))
        self.p(ReplacementTransform(eqB[2], eqC[0]), ReplacementTransform(eqB[3], eqC[1]),
               ReplacementTransform(eqB[0], eqC[2]), ReplacementTransform(eqB[4], eqC[3]),
               ReplacementTransform(eqB[6], eqC[4]), ReplacementTransform(eqB[7], eqC[5]),
               FadeOut(eqB[1]), FadeOut(eqB[5]), FadeOut(riscos), FadeOut(mdef), rt=1.6)
        self.w(0.8)
        eqD = T("v_f", "=", r"\sqrt{2\mu_k g d}", size=54).move_to(P3(0, Y1))
        self.p(FadeOut(eqC, shift=0.1 * UP), FadeIn(eqD, shift=0.1 * UP), rt=1.0)
        self.w(0.6)
        eqE = T("v_f", "=", r"\sqrt{2\cdot 0{,}5\cdot 10\cdot 10}", "=", r"10\ \mathrm{m/s}", size=46).move_to(P3(0, Y2))
        self.p(FadeIn(eqE, shift=0.1 * UP), rt=1.2)
        bx = caixa(eqE[4], WHITE_, 0.12)
        self.p(Create(bx), rt=0.6)
        self.w(1.0)
        # o triângulo da marca vira o triângulo de velocidade (mesma direção)
        vec = T(r"\vec v_f", "=", r"(8;\ 6)\ \mathrm{m/s}", size=48).move_to(P3(0, Y1))
        self.p(FadeOut(eqD), FadeOut(eqE), FadeOut(bx), *self.frase(""), rt=0.7)
        self.p(FadeIn(self.cotas), FadeIn(self.angulo), rt=0.6)
        nomes = [T(r"8\ \mathrm{m/s}", size=30), T(r"6\ \mathrm{m/s}", size=30), T(r"10\ \mathrm{m/s}", size=30)]
        tv = triangulo(P3(-2.7, -6.35), 0.42, VEL, VEL_L, nomes, wl=5, wh=7)
        hip = Line(P0, E).set_stroke(MARK, 3)
        self.p(TransformFromCopy(self.c8[0], tv["hx"]), TransformFromCopy(self.c6[0], tv["hy"]),
               TransformFromCopy(hip, tv["hh"]), TransformFromCopy(self.c8[1], tv["lx"]),
               TransformFromCopy(self.c6[1], tv["ly"]), TransformFromCopy(self.c10, tv["lh"]),
               TransformFromCopy(self.ang, tv["ang"]), FadeIn(vec, shift=0.1 * UP), rt=2.2)
        self.w(1.0)
        self.tri_v = tv
        self.vec = vec
        self.w(1.2)

    # ================================================================ C03 · voltar ao impacto
    def c03(self):
        self.p(*self.linha.ir(1), *self.cab("VOLTAR AO IMPACTO"), FadeOut(self.tri_v["g"]), FadeOut(self.vec),
               FadeOut(self.cotas), FadeOut(self.angulo), rt=1.3)
        # os veículos voltam para antes do choque (a marca fica)
        self.p(self.tt.animate.set_value(T0), rt=2.0, rate_func=linear)
        self.setas, self.rot_setas = self.setas_antes((r"\vec v_{1i}", r"=\ ?"), (r"\vec v_{2i}", r"=\ ?"))
        self.p(FadeIn(self.setas), FadeIn(self.rot_setas), rt=0.9)
        self.w(0.6)
        fase1 = txt("DESLIZAMENTO: TRABALHO–ENERGIA", 24, color=DIM).move_to(P3(0, -2.2))
        fase2 = VGroup(txt("IMPACTO:", 24), txt("MOMENTO", 24, color=MAG)).arrange(RIGHT, buff=0.18).move_to(P3(0, -2.2))
        self.p(FadeIn(fase1), rt=0.8)
        self.w(0.6)
        self.p(FadeOut(fase1, shift=0.1 * UP), FadeIn(fase2, shift=0.1 * UP), rt=0.9)
        # por que o momento vale só no impacto
        s1 = txt("IMPACTO CURTÍSSIMO:\nIMPULSO EXTERNO DESPREZÍVEL", 18)
        s2 = txt("VÁRIOS METROS DESLIZANDO:\nATRITO NÃO DESPREZÍVEL", 18, color=DIM)
        s1.move_to(P3(-2.2, -3.6))
        s2.move_to(P3(2.2, -3.6))
        b1, b2 = caixa(s1, WHITE_, 0.18, 2.0), caixa(s2, DIM, 0.18, 1.6, 0.7)
        vs = MathTex(r"\times", font_size=36, color=DIM).move_to(P3(0, -3.6))
        self.p(FadeIn(VGroup(s1, b1)), rt=0.8)
        self.w(1.2)
        self.p(FadeIn(VGroup(s2, b2)), FadeIn(vs), rt=0.8)
        self.w(1.6)
        self.p(FadeOut(VGroup(s1, b1, s2, b2, vs)), rt=0.6)
        # conservação vetorial → componentes
        YP, YX, YY, YC = -3.3, -4.45, -5.55, -6.6
        chip = T(r"\vec v_f", "=", r"(8;\ 6)\ \mathrm{m/s}", size=36).move_to(P3(0, YC)).set_opacity(0.85)
        eqP = T(r"\vec P_i", "=", r"\vec P_f", size=56).move_to(P3(0, YP))
        self.p(FadeIn(eqP, shift=0.1 * UP), FadeIn(chip), rt=1.0)
        self.w(1.0)
        tx = MathTex("x:", font_size=32, color=DIM)
        ty = MathTex("y:", font_size=32, color=DIM)
        X1 = T("m_1", "v_{1i}", "=", r"(m_1+m_2)", "v_{fx}", size=44).move_to(P3(0.35, YX))
        Y1 = T("m_2", "v_{2i}", "=", r"(m_1+m_2)", "v_{fy}", size=44).move_to(P3(0.35, YY))
        tx.next_to(X1, LEFT, buff=0.3)
        ty.next_to(Y1, LEFT, buff=0.3)
        self.p(TransformFromCopy(eqP, X1), TransformFromCopy(eqP, Y1), FadeIn(tx), FadeIn(ty), rt=1.4)
        self.w(1.5)
        X2 = T("2000", "v_{1i}", "=", "3000", r"\cdot", "8", size=46).move_to(P3(0.35, YX))
        Y2 = T("1000", "v_{2i}", "=", "3000", r"\cdot", "6", size=46).move_to(P3(0.35, YY))
        self.p(Indicate(chip, color=WHITE_, scale_factor=1.06), rt=0.8)
        self.p(TransformMatchingTex(X1, X2), TransformMatchingTex(Y1, Y2), rt=1.6)
        self.w(1.2)
        X3 = T("v_{1i}", "=", r"12\ \mathrm{m/s}", size=48).move_to(P3(0.35, YX))
        Y3 = T("v_{2i}", "=", r"18\ \mathrm{m/s}", size=48).move_to(P3(0.35, YY))
        self.p(TransformMatchingTex(X2, X3), TransformMatchingTex(Y2, Y3), rt=1.4)
        self.w(0.8)
        _, rot = self.setas_antes((r"\vec v_{1i}", r"=12\ \mathrm{m/s}"), (r"\vec v_{2i}", r"=18\ \mathrm{m/s}"))
        self.p(Transform(self.rot_setas, rot), rt=1.0)
        self.w(0.8)
        X4 = T("v_{1i}", "=", r"12\ \mathrm{m/s}", "=", r"43{,}2\ \mathrm{km/h}", size=44).move_to(P3(0, YX))
        Y4 = T("v_{2i}", "=", r"18\ \mathrm{m/s}", "=", r"64{,}8\ \mathrm{km/h}", size=44).move_to(P3(0, YY))
        self.p(TransformMatchingTex(X3, X4), TransformMatchingTex(Y3, Y4), FadeOut(tx), FadeOut(ty), rt=1.2)
        self.w(2.0)
        self.c03_fora = VGroup(fase2, chip, eqP, X4, Y4)

    # ================================================================ C04 · o triângulo e a pegadinha
    def c04(self):
        self.p(*self.cab("O TRIÂNGULO E A PEGADINHA"), FadeOut(self.c03_fora), FadeOut(self.setas),
               FadeOut(self.rot_setas), rt=1.0)
        self.p(self.tt.animate.set_value(TSTOP), rt=1.4, rate_func=linear)
        tm = txt("MARCA", 22, color=MARK).move_to(P3(3.3, 0.85))
        self.p(FadeIn(self.cotas), FadeIn(self.angulo), FadeIn(tm), rt=1.0)
        # velocidade e momento: mesmo triângulo, outra escala
        nv = [T(r"8\ \mathrm{m/s}", size=26), T(r"6\ \mathrm{m/s}", size=26), T(r"10\ \mathrm{m/s}", size=26)]
        tv = triangulo(P3(-4.05, -5.05), 0.27, VEL, VEL_L, nv, size=26, wl=4, wh=6)
        lp2 = VGroup(T("p_{2i}", size=26), T(r"18\,000", size=26)).arrange(DOWN, buff=0.08)
        nm = [T("p_{1i}", r"=24\,000", size=26), lp2, T("P", r"=30\,000", size=26)]
        tp = triangulo(P3(-0.25, -5.05), 0.33, MAG, MAG_L, nm, size=26, wl=4, wh=6)
        ttv = txt("VELOCIDADE", 22, color=VEL).move_to(P3(-2.95, -2.55))
        ttp = VGroup(txt("MOMENTO", 22, color=MAG), MathTex(r"(\mathrm{kg\cdot m/s})", font_size=24, color=DIM)) \
            .arrange(RIGHT, buff=0.14).move_to(P3(1.15, -2.55))
        xm = MathTex(r"\xrightarrow{\ \times M\ }", font_size=34, color=WHITE_).move_to(P3(-0.95, -3.6))
        self.p(FadeIn(tv["g"]), FadeIn(ttv), rt=1.2)
        self.w(0.8)
        self.p(TransformFromCopy(tv["g"], tp["g"]), FadeIn(ttp), FadeIn(xm), rt=1.8)
        self.w(1.2)
        self.p(*[Indicate(a, color=WHITE_, scale_factor=1.25) for a in (self.ang, tv["ang"], tp["ang"])],
               *self.frase("A MESMA DIREÇÃO ATRAVESSA AS ETAPAS", 22), rt=1.2)
        self.w(1.2)
        tg = T(r"\tan\theta", "=", r"\dfrac{p_{2i}}{p_{1i}}", "=", r"\dfrac{18\,000}{24\,000}", "=", r"\dfrac34", size=40) \
            .move_to(P3(0, -6.2))
        tg[2].set_color(MAG)
        self.p(FadeIn(tg, shift=0.1 * UP), *self.frase(""), rt=1.2)
        self.w(2.0)
        self.p(FadeOut(tv["g"]), FadeOut(tp["g"]), FadeOut(ttv), FadeOut(ttp), FadeOut(xm), FadeOut(tg), rt=0.7)
        # contraste: quem é mais rápido × quem tem mais momento
        YB = -5.55
        hv = txt("VELOCIDADE", 22, color=VEL).move_to(P3(-2.25, -2.45))
        hp = VGroup(txt("MOMENTO", 22, color=MAG), MathTex(r"(\mathrm{kg\cdot m/s})", font_size=24, color=DIM)) \
            .arrange(RIGHT, buff=0.14).move_to(P3(2.25, -2.45))
        base = VGroup(Line(P3(-3.9, YB), P3(-0.6, YB)), Line(P3(0.6, YB), P3(3.9, YB))).set_stroke(DIM, 2, opacity=0.6)

        def barra(x, alt, cor, val):
            r = Rectangle(width=0.8, height=alt).set_stroke(width=0).set_fill(cor, 0.9)
            r.move_to(P3(x, YB + alt / 2))
            return r, MathTex(val, font_size=28, color=WHITE_).next_to(r, UP, buff=0.12)
        bv1, lv1 = barra(-3.0, V1I * 0.13, VEL, r"12\ \mathrm{m/s}")
        bv2, lv2 = barra(-1.5, V2I * 0.13, VEL, r"18\ \mathrm{m/s}")
        bp1, lp1 = barra(1.5, P1I / 1e4, MAG, r"24\,000")
        bp2, lp2_ = barra(3.0, P2I / 1e4, MAG, r"18\,000")
        nb = VGroup(*[MathTex(s, font_size=28, color=DIM).move_to(P3(x, YB - 0.3))
                      for s, x in (("1", -3.0), ("2", -1.5), ("1", 1.5), ("2", 3.0))])
        self.p(FadeIn(hv), FadeIn(hp), Create(base), FadeIn(nb), rt=0.8)
        self.p(GrowFromEdge(bv1, DOWN), GrowFromEdge(bv2, DOWN), FadeIn(lv1), FadeIn(lv2), rt=1.2)
        self.w(0.8)
        self.p(GrowFromEdge(bp1, DOWN), GrowFromEdge(bp2, DOWN), FadeIn(lp1), FadeIn(lp2_), rt=1.2)
        self.w(0.8)
        cv = txt("VEÍCULO 2: MAIS RÁPIDO", 18, color=VEL).move_to(P3(-2.25, -6.3))
        cp = txt("VEÍCULO 1: MAIS MOMENTO", 18, color=MAG).move_to(P3(2.25, -6.3))
        self.p(Create(caixa(VGroup(bv2, lv2), VEL, 0.1, 2.0)), FadeIn(cv), rt=0.9)
        self.w(0.8)
        self.p(Create(caixa(VGroup(bp1, lp1), MAG, 0.1, 2.0)), FadeIn(cp), rt=0.9)
        self.w(1.0)
        self.p(*self.frase("A DIREÇÃO DOS DESTROÇOS DÁ A RAZÃO\nDOS MOMENTOS, NÃO DAS VELOCIDADES", 24), rt=1.0)
        self.w(2.5)
        self.marca_t = tm

    # ================================================================ C05 · conferência de ida e volta
    def c05(self):
        fora = [m for m in self.mobjects if m not in self.fixos | {self.linha, self.via, self.v1, self.v2, self.marca,
                                                                 self.dados, self.head}]
        self.p(*self.linha.ir(0), *self.cab("CONFERÊNCIA DE IDA E VOLTA"), *[FadeOut(m) for m in fora], rt=1.0)
        self.remove(*fora)
        self._frase = None
        self.p(FadeOut(self.v1), FadeOut(self.v2), rt=0.4)
        self.tt.set_value(T0)
        setas, rot = self.setas_antes((r"\vec v_{1i}", r"=12\ \mathrm{m/s}"), (r"\vec v_{2i}", r"=18\ \mathrm{m/s}"))
        self.p(FadeIn(self.v1), FadeIn(self.v2), FadeIn(setas), FadeIn(rot), rt=0.6)
        ys = (-2.6, -3.55, -4.5, -5.6)
        l1 = T("v_{1i}", r"=12,\quad", "v_{2i}", r"=18\ \ (\mathrm{m/s})", size=40).move_to(P3(0, ys[0]))
        l2 = T(r"\vec P_i", r"=(24\,000;\ 18\,000)\ \mathrm{kg\cdot m/s}", size=36).move_to(P3(0, ys[1]))
        l3 = T(r"\vec v_f", r"=\dfrac{\vec P_i}{m_1+m_2}=(8;\ 6)\ \mathrm{m/s}", size=36).move_to(P3(0, ys[2]))
        l4 = T("d", r"=\dfrac{v_f^2}{2\mu_k g}=10\ \mathrm{m}", size=40).move_to(P3(0, ys[3]))
        self.p(FadeIn(l1, shift=0.1 * UP), rt=0.6)
        self.p(FadeOut(setas), FadeOut(rot), self.tt.animate.set_value(0.0), *self.linha.ir(1), rt=1.6, rate_func=linear)
        self.p(self.flash(), rt=0.4)
        self.p(FadeIn(l2, shift=0.1 * UP), FadeIn(l3, shift=0.1 * UP), rt=0.8)
        rastro = always_redraw(lambda: self._marca(s_desl(self.tt.get_value()), VEL, 2.2, 1.0).set_z_index(2))
        self.add(rastro)
        self.p(self.tt.animate.set_value(TSTOP), *self.linha.ir(2), rt=3.0, rate_func=linear)
        rastro.clear_updaters()
        anel = Circle(radius=0.3).set_stroke(WHITE_, 3).move_to(E).set_z_index(16)
        ok = MathTex(r"\checkmark", font_size=44, color=WHITE_).move_to(E + P3(0.0, -0.75)).set_z_index(16) \
            .set_stroke(BACKGROUND_COLOR, 6, background=True)
        ok.move_to(P3(E[0] + 0.85, E[1] - 0.25))
        self.p(*self.linha.ir(3), Create(anel), FadeIn(ok), FadeIn(l4, shift=0.1 * UP), rt=1.0)
        self.w(1.6)
        self.c05_fora = VGroup(l1, l2, l3, l4, anel, ok, rastro)

    # ================================================================ C06 · e a energia?
    def c06(self):
        self.p(*self.cab("E A ENERGIA?"), FadeOut(self.c05_fora), rt=1.0)
        q = txt("O MOMENTO SE CONSERVOU.\nE A ENERGIA?", 26).move_to(P3(0, -2.3))
        self.p(FadeIn(q, shift=0.1 * UP), rt=0.9)
        self.w(1.2)
        KS, X0 = 0.022, -3.6                                   # tela por kJ, borda esquerda das barras
        YA, YD = -3.95, -5.4

        def seg(k0, k1, y, cor, op=0.92):
            r = Rectangle(width=(k1 - k0) * KS, height=0.42).set_stroke(width=0).set_fill(cor, op)
            return r.move_to(P3(X0 + (k0 + k1) / 2 * KS, y))
        a1, a2 = seg(0, 144, YA, C1F), seg(144, 306, YA, C2F)
        ta1 = MathTex("144", font_size=28, color=BACKGROUND_COLOR).move_to(a1)
        ta2 = MathTex("162", font_size=28, color=WHITE_).move_to(a2)
        la = T(r"K_{\mathrm{antes}}", r"=306\ \mathrm{kJ}", size=36).move_to(P3(X0, YA + 0.6), aligned_edge=LEFT)
        self.p(GrowFromEdge(a1, LEFT), GrowFromEdge(a2, LEFT), FadeIn(la), rt=1.4)
        self.p(FadeIn(ta1), FadeIn(ta2), rt=0.5)
        self.w(1.0)
        d1 = seg(0, 150, YD, JUNTOS)
        td = MathTex("150", font_size=28, color=BACKGROUND_COLOR).move_to(d1)
        ld = T(r"K_{\mathrm{depois}}", r"=150\ \mathrm{kJ}", size=36).move_to(P3(X0, YD + 0.6), aligned_edge=LEFT)
        self.p(GrowFromEdge(d1, LEFT), FadeIn(ld), FadeIn(td), rt=1.2)
        self.w(0.8)
        # o que falta: 156 kJ, convertidos (laranja)
        fal = seg(150, 306, YA, HEAT, 0.0).set_stroke(HEAT, 2.5)
        self.p(Create(fal), rt=0.6)
        laranja = seg(150, 306, YD, HEAT, 0.9)
        self.p(ReplacementTransform(fal, laranja), rt=1.2)
        tl = MathTex(r"156\ \mathrm{kJ}\approx 51\,\%", font_size=32, color=HEAT).next_to(laranja, DOWN, buff=0.18) \
            .align_to(laranja, RIGHT)
        self.p(FadeIn(tl), rt=0.6)
        destinos = txt("DEFORMAÇÃO · CALOR · SOM · VIBRAÇÃO", 20, color=HEAT).move_to(P3(0, -6.45))
        gotas = VGroup(*[Dot(laranja.get_center() + P3(dx, 0), radius=0.045, color=HEAT) for dx in (-1.2, -0.4, 0.4, 1.2)])
        self.p(*[d.animate.move_to(P3(-2.9 + 1.93 * i, -6.15)).set_opacity(0) for i, d in enumerate(gotas)],
               FadeIn(destinos, shift=0.1 * DOWN), rt=1.2)
        self.remove(gotas)
        self.w(1.2)
        self.p(*self.frase("MOMENTO SE CONSERVA.\nENERGIA CINÉTICA, NÃO.", 26, y=-7.3), rt=1.0)
        self.w(2.5)

    # ================================================================ C07 · cada intervalo, sua lei
    def c07(self):
        self.marca.clear_updaters()
        for m in (self.v1, self.v2):
            m.clear_updaters()
        keep = {self.head}
        mobs = [m for m in self.mobjects if m not in self.fixos | {self.linha} | keep]
        self._frase = None
        L = self.linha
        self.p(*[FadeOut(m) for m in mobs], *self.cab("CADA INTERVALO, SUA LEI"), FadeOut(L.dot),
               *[r.animate.set_opacity(1.0 if i in (1, 2) else 0.38) for i, r in enumerate(L.rot)], rt=1.0)
        self.remove(*mobs)
        bm = txt("MOMENTO", 24, color=MAG)
        be = txt("TRABALHO–ENERGIA", 22)
        bm.move_to(P3(-1.75, 3.85))
        be.move_to(P3(1.85, 3.85))
        cm, ce = caixa(bm, MAG, 0.2, 2.2), caixa(be, WHITE_, 0.2, 2.2)
        lm = Line(P3(L.XS[1], L.y - 0.1), cm.get_top()).set_stroke(MAG, 2, opacity=0.8)
        le = Line(P3(L.XS[2], L.y - 0.1), ce.get_top()).set_stroke(WHITE_, 2, opacity=0.8)
        self.p(Create(lm), Create(le), FadeIn(VGroup(bm, cm)), FadeIn(VGroup(be, ce)), rt=1.2)
        self.w(1.5)
        aqui = txt("AQUI OS DOIS FICARAM JUNTOS.", 26).move_to(P3(0, 2.3))
        self.p(FadeIn(aqui, shift=0.1 * UP), rt=0.9)
        self.w(1.0)
        # ponte: colisão elástica (só insinuação: vetores de momento e um traço de círculo)
        O, Tp = P3(-2.6, -1.9), P3(2.6, -1.9)
        Q = O + pol(5.2 * np.cos(np.radians(32)), 32)
        pi_ = arrow(O, Tp, MAG, 7, tip=0.24)
        p1 = arrow(O, Q, MAG, 5, tip=0.2)
        p2 = arrow(Q, Tp, MAG_L, 5, tip=0.2)
        circ = DashedVMobject(Arc(radius=2.6, start_angle=np.radians(8), angle=np.radians(160), arc_center=P3(0, -1.9)),
                              num_dashes=34).set_stroke(CYAN, 2.2, opacity=0.4).set_z_index(1)
        self.p(GrowArrow(pi_), rt=0.8)
        self.p(GrowArrow(p1), GrowArrow(p2), rt=1.0)
        self.p(Create(circ), rt=1.2)
        el = VGroup(txt("COLISÃO ELÁSTICA:", 24),
                    VGroup(txt("ENERGIA CINÉTICA TAMBÉM SE CONSERVA", 22))).arrange(DOWN, buff=0.18).move_to(P3(0, -3.9))
        self.p(FadeIn(el, shift=0.1 * UP), rt=1.0)
        self.w(0.8)
        self.p(*self.frase("QUAIS ÂNGULOS SÃO POSSÍVEIS?", 26, y=-5.6), rt=1.0)
        self.w(2.0)
