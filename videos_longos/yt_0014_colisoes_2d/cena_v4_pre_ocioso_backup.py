"""yt_0014 — COLISÕES EM 2D: o momento sempre foi um vetor (Física I · Mecânica · Colisões) — preview silencioso v1.

Cena completa SILENCIOSA em Manim 2D (sem Blender). Complemento direto de yt_0013 (colisões em 1D): mesma gramática visual.
Preview 960×540 / 15 fps:
    uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_0014_colisoes_2d/cena.py Colisoes2DYT014
Trecho isolado (desenvolvimento): SECOES=hook,c07,c09 · auditoria de sobreposições: AUDITORIA=1 (com --dry_run)
· still num instante: STILL=12.5 (com -s).

Semântica de cor: velocidade violeta · MOMENTO magenta · força azul-claro · ENERGIA CINÉTICA e CÍRCULO DE ESTADOS ciano ·
energia interna/dissipada laranja (único tom quente) · ângulos: arcos brancos finos · corpos em aço chato (m1 claro, m2 escuro).
Dois planos que nunca se confundem: ESPAÇO FÍSICO (corpos, trajetórias) e PLANO DE p₁f (círculo de estados).
Notação (igual ao yt_0013): v₁ᵢ v₂ᵢ (antes), v₁f v₂f (depois), v_f (comum), λ = m₂/m₁ entra em C06.
"""
import os
import sys
from pathlib import Path

import numpy as np
from manim import *  # noqa: F401,F403

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import DISPLAY_FONT, official_text, screen_text  # noqa: E402
from MF_Tools import TransformByGlyphMap  # noqa: E402

# ── paleta (docs/padrao_video_longo.md §4 + decisões do yt_0013) ──────────────────────────────────────────────
WHITE_ = TEXT_COLOR          # #F5F7FF — massa, números, operadores, texto, ângulos
CYAN = PRIMARY_COLOR         # #35D9FF — energia cinética K e círculo de estados
MAG = "#EA63FF"              # momento linear p, P
VEL = "#9C8CFF"              # velocidade v (o violeta é só da velocidade)
FC = "#5AA2FF"               # força F
HEAT = "#FF7A3D"            # energia interna / dissipada (único tom quente)
STEEL = "#7A8696"            # matéria: corpo 2
GEO = "#B8C4DA"              # geometria (régua, raio, centro); tom claro de aço: corpo 1
DIM = "#8FA3C4"              # eixos, convenções, texto secundário
C1F, C2F = GEO, STEEL        # corpos em aço chato: m1 aço claro, m2 aço (distintos por tom e índice)


def mix(c, w):
    """Mistura de uma cor oficial com o branco oficial (contraste sem cor nova)."""
    return interpolate_color(ManimColor(c), ManimColor(WHITE_), w).to_hex()


MAG_L = mix(MAG, 0.35)       # segundo p⃗ quando coexistem dois momentos (mesma cor, mais claro)
KN = mix(CYAN, 0.45)         # parcela da energia cinética que passa ao alvo (família ciano)

SECOES = [s.strip() for s in os.environ.get("SECOES", "").split(",") if s.strip()]
AUDITORIA = os.environ.get("AUDITORIA") == "1"
STILL = float(os.environ["STILL"]) if os.environ.get("STILL") else None
LENTO = 1.3                  # desaceleração uniforme dos movimentos físicos

# ── voz: tempos por palavra (alinhamento forçado ElevenLabs), um bloco por âncora ### de narracao_sugestao.md ──
import json  # noqa: E402
import re  # noqa: E402

AQUI = Path(__file__).resolve().parent


def _n(w):
    return re.sub(r"[^\w]", "", w.lower())


VOZ = {c["chave"]: [(_n(p[0]), p[1], p[2]) for p in c["palavras"]]
       for c in json.loads((AQUI / "audio" / "alinhamento_forcado.json").read_text(encoding="utf-8"))["celulas"]}
VOZ_FIM = max(w[2] for ws in VOZ.values() for w in ws)
LEAD = 0.12                                          # a imagem entra ~0,12 s antes da palavra (atraso máximo pedido: 0,2 s)
GRAVAR = os.environ.get("GRAVAR") == "1"             # passe a seco que mede o conteúdo de cada trecho entre âncoras
_RIT = AQUI / "ritmo.json"
RITMO = json.loads(_RIT.read_text(encoding="utf-8")) if _RIT.exists() and not GRAVAR else None

T_HL, T_MAIN, T_LAB, T_SMALL = 44, 34, 26, 22
# v2: margens seguras de 0,6 u; tamanhos mínimos (unidades de font_size do Manim, como no yt_0013)
MARG = 0.6
X_MIN, X_MAX = -8 + MARG, 8 - MARG
Y_MIN = -4.5 + MARG
Y_TOPO = 3.1                  # limite superior do conteúdo (o header ocupa o canto superior esquerdo acima disso)
FAIXA_Y = -3.45               # faixa inferior de frases (uma por vez)
T_MIN, M_MIN = 22, 26         # nada de texto menor que isso (exceto a tag fixa da linha 1 do header)
M_EQ, M_SEC = 52, 40          # equação principal (≥ 48) e secundária (≥ 36)
T_FRASE = 30                  # frase de ideia (≥ 30)
T_TITULO = 24                # título da cena (linha 2 do header): o yt_0013 usa 30; reduzido a pedido do usuário (25/10)
M_MAIN, M_MID, M_REF, M_LAB = 68, 56, 46, 40

# cor por token de MathTex (substring; o mais longo vence). Operadores, números, massas, λ e ângulos ficam brancos.
TOK = {}
for _s in (r"\vec v_{1i}", r"\vec v_{2i}", r"\vec v_{1f}", r"\vec v_{2f}", r"\vec v_f", "v_{1i}^2", "v_{1f}^2",
           "v_{2f}^2", "v_f^2", "v_{1i}", "v_{2i}", "v_{1f}", "v_{2f}", "v_f", "v_{fx}", "v_{fy}"):
    TOK[_s] = VEL
for _s in (r"\vec p_{1i}", r"\vec p_{1f}", r"\vec p_{2f}", r"\vec P_i", r"\vec P_f", r"\vec p_1", r"\vec p_2",
           r"\vec p_3", r"\vec p_k", "p_{1i}^2", "p_{1f}^2", "p_{2f}^2", "p_{1i}", "p_{1f}", "p_{2f}", "p_{1f,x}",
           "p_{1f,y}"):
    TOK[_s] = MAG
for _s in ("K_i", "K_f", "K_{1i}", "K_{1f}", r"K_{\alpha,i}", "K_{n,f}", "K"):
    TOK[_s] = CYAN


# ── geometria do exemplo genérico (C02, C03, C06): p₁ᵢ = 4, θ₁ = 25°, colisão elástica com λ = 1/2 ───────────
def _d_mais(lam, th_deg, p=1.0):
    """Maior distância (módulo de p₁f) em que a semirreta de ângulo θ corta o círculo de estados."""
    C, R = p / (1 + lam), lam * p / (1 + lam)
    s = R * R - (C * np.sin(np.radians(th_deg))) ** 2
    return C * np.cos(np.radians(th_deg)) + np.sqrt(s)


def pol(r, graus):
    a = np.radians(graus)
    return np.array([r * np.cos(a), r * np.sin(a), 0.0])


def P3(x, y):
    return np.array([x, y, 0.0])


def unit(v):
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    return v / n if n > 1e-9 else v


GP1I, GTH1 = 4.0, 25.0
GP1F = _d_mais(0.5, GTH1, GP1I)
GV1F = pol(GP1F, GTH1)
GV2F = P3(GP1I, 0) - GV1F
GTH2 = float(np.degrees(np.arctan2(-GV2F[1], GV2F[0])))
GP2F = float(np.linalg.norm(GV2F))
assert abs(GP2F ** 2 - 0.5 * (GP1I ** 2 - GP1F ** 2)) < 1e-9          # elástica λ=1/2: p₂f² = λ(p₁ᵢ² − p₁f²)

# hook: disco pesado (m₁ = 4 m₂) bate em disco leve parado; linha dos centros a 60° abaixo do eixo
HK_M1, HK_M2, HK_V, HK_PHI = 4.0, 1.0, 3.0, 60.0
_n = pol(1.0, -HK_PHI)
_vn = HK_V * _n[0]
HK_V2F = 2 * HK_M1 / (HK_M1 + HK_M2) * _vn * _n
HK_V1F = P3(HK_V, 0) - 2 * HK_M2 / (HK_M1 + HK_M2) * _vn * _n
HK_TH1 = float(np.degrees(np.arctan2(HK_V1F[1], HK_V1F[0])))
HK_TH2 = float(np.degrees(np.arctan2(-HK_V2F[1], HK_V2F[0])))
LAM_EX = 0.25                                                          # exemplo da dupla alfa–nêutron (C07, C08, C10)
THMAX_EX = float(np.degrees(np.arcsin(LAM_EX)))
HOOK_CAND = (25.0, 40.0)                                               # direções candidatas; 40° será revelada impossível
assert 0 < HK_TH1 < THMAX_EX and abs(HK_TH1 - 10.9) < 0.1 and abs(HK_TH2 - 60) < 1e-6   # desfecho real cabe no círculo
assert HOOK_CAND[0] > THMAX_EX and HOOK_CAND[1] > THMAX_EX
assert abs(np.linalg.norm(HK_M1 * HK_V1F + HK_M2 * HK_V2F - P3(HK_M1 * HK_V, 0))) < 1e-9


# ── texto, matemática e formas ───────────────────────────────────────────────────────────────────────────────
def txt(s, size=T_MAIN, color=WHITE_, op=1.0, bold=False, fixo=False):
    """Texto editorial: Space Grotesk em CAIXA ALTA (sem símbolos matemáticos: esses vão em MathTex). Mínimo T_MIN."""
    if not fixo:
        size = max(size, T_MIN)
    s = s.upper()
    if bold:
        return official_text(s, DISPLAY_FONT, BOLD, size, oversample=2, color=color).set_opacity(op)
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(op)


def gloss(s, size=T_SMALL, op=0.7):
    """Glossário de variável (única exceção à caixa alta)."""
    return screen_text(s, size, color=WHITE_, oversample=4).set_opacity(op)


def M(*parts, size=M_MAIN, color=WHITE_, w=None):
    size = max(size, M_MIN)
    m = MathTex(*parts, font_size=size, color=color, tex_to_color_map=TOK)
    if w and m.width > w:
        m.scale_to_fit_width(w)
    return m


def arrow(a, b, color=WHITE_, width=5, z=8, tip=0.2, op=1.0):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    L = np.linalg.norm(b - a)
    if L < 0.03:
        return VMobject()
    if L < 3 * tip:                         # ponta sempre visível: vetor curto vira qualitativo (comprimento mínimo)
        b = a + (b - a) / L * 3 * tip
    m = Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.45,
              max_stroke_width_to_length_ratio=50)
    return m.set_opacity(op).set_z_index(z)


def box(m, color=WHITE_, buff=0.12, width=2.5):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=width, corner_radius=0.08)


def _fundo(w):
    """Cor do fundo misturada com `w` de branco (gradientes sutis dos painéis)."""
    return interpolate_color(ManimColor(BACKGROUND_COLOR), ManimColor(WHITE_), w)


def placa(w, h, centro, op=0.05):
    """Painel: retângulo arredondado com leve gradiente vertical, borda 1,3 px e um filete interno de 1 px."""
    frente = RoundedRectangle(corner_radius=0.14, width=w, height=h).set_stroke(WHITE_, 1.3, opacity=0.26) \
        .set_fill([_fundo(0.09), _fundo(0.035)], opacity=1.0)
    frente.set_sheen_direction(DOWN)
    filete = RoundedRectangle(corner_radius=0.1, width=w - 0.14, height=h - 0.14).set_stroke(WHITE_, 1.0, opacity=0.09) \
        .set_fill(opacity=0)
    return VGroup(frente, filete).move_to(centro).set_z_index(-2)


def vinheta(c, r, cor, soma=0.11, n=4):
    """Foco de luz muito sutil atrás do visual principal: círculos concêntricos de baixa opacidade."""
    g = VGroup(*[Circle(radius=r * (1 - 0.23 * k)).set_stroke(width=0).set_fill(cor, soma / n) for k in range(n)])
    return g.move_to(np.asarray(c, float)).set_z_index(-4)


def halo_circ(c, rad, cor=CYAN):
    """Dois traços largos e muito transparentes atrás de um círculo (presença sem virar mancha)."""
    return VGroup(Circle(radius=rad).set_stroke(cor, 20, 0.05), Circle(radius=rad).set_stroke(cor, 10, 0.10)) \
        .move_to(np.asarray(c, float)).set_z_index(2)


def dupla_caixa(m, cor=WHITE_, buff=0.16):
    """Caixa de payoff: borda fina dupla (a externa mais apagada). Uma por cena."""
    a = SurroundingRectangle(m, color=cor, buff=buff, stroke_width=2.6, corner_radius=0.1)
    b = SurroundingRectangle(m, color=cor, buff=buff + 0.11, stroke_width=1.0, corner_radius=0.17).set_stroke(opacity=0.35)
    return VGroup(a, b)


def lab_at(m, a, b, lado=1, gap=0.14):
    """Rótulo ao lado de um segmento a→b (lado=+1: esquerda de a→b; −1: direita), sem encostar nele."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = unit(b - a)
    nrm = np.array([-d[1], d[0], 0.0]) * lado
    meia = 0.5 * (abs(nrm[0]) * m.width + abs(nrm[1]) * m.height)
    m.move_to((a + b) / 2 + nrm * (gap + meia))
    return m.set_stroke(BACKGROUND_COLOR, 6, background=True)        # contorno escuro: o rótulo nunca briga com a linha


def arco(c, r, a0, a1, w=1.8, op=0.95):
    """Arco branco fino de a0 a a1 (graus), centrado em c."""
    return Arc(radius=r, start_angle=np.radians(a0), angle=np.radians(a1 - a0), arc_center=np.asarray(c, float)) \
        .set_stroke(WHITE_, w, opacity=op)


def reto(v, d1, d2, s=0.2):
    """Marca de ângulo reto no vértice v, entre as direções d1 e d2."""
    v, d1, d2 = np.asarray(v, float), unit(d1), unit(d2)
    return VMobject().set_points_as_corners([v + d1 * s, v + (d1 + d2) * s, v + d2 * s]).set_stroke(WHITE_, 1.8)


def ponto(p, cor=WHITE_, r=0.07, z=12):
    return Dot(np.asarray(p, float), radius=r, color=cor).set_z_index(z)


class Disco(VGroup):
    """Corpo 2D chato: aro de aço mais escuro, face de aço e contorno claro fino, com o rótulo da massa dentro
    (m₁ escuro sobre o aço claro, m₂ branco sobre o aço). Sem brilho, sombra nem plano deslocado."""

    def __init__(self, cor, r, nome=None, size=None):
        super().__init__()
        self.r = r
        rim = interpolate_color(ManimColor(cor), ManimColor(BACKGROUND_COLOR), 0.35)      # tom mais escuro da mesma cor
        aro = Circle(radius=r).set_stroke(mix(cor, 0.55), 2.2).set_fill(rim, 1.0)
        face = Circle(radius=r * 0.78).set_stroke(width=0).set_fill(cor, 1.0)
        self.front = aro
        self.add(aro, face)
        if nome:
            esc = cor == GEO
            self.add(MathTex(nome, font_size=size or max(20, int(r * 95)),
                             color=BACKGROUND_COLOR if esc else WHITE_).move_to(aro))
        else:
            self.add(Dot(aro.get_center(), radius=0.035, color=BACKGROUND_COLOR if cor == GEO else WHITE_)
                     .set_opacity(0.55))

    @property
    def c(self):
        return self.front.get_center()


class Corpo(VGroup):
    """Corpo retangular 2D chato (veículos vistos de cima): mesmo acabamento do Disco."""

    def __init__(self, cor, w, h, nome=None, size=30):
        super().__init__()
        f = RoundedRectangle(corner_radius=0.05, width=w, height=h).set_stroke(mix(cor, 0.5), 2).set_fill(cor, 1.0)
        ins = min(0.07, 0.12 * min(w, h))
        filete = RoundedRectangle(corner_radius=0.03, width=max(w - 2 * ins, 0.02), height=max(h - 2 * ins, 0.02)) \
            .set_stroke(WHITE_, 1, opacity=0.35).set_fill(opacity=0).move_to(f)
        self.front = f
        self.add(f, filete)
        if nome:
            esc = cor == GEO
            self.add(MathTex(nome, font_size=size, color=BACKGROUND_COLOR if esc else WHITE_).move_to(f))

    @property
    def c(self):
        return self.front.get_center()


# C11 (acidente): veículos vistos de cima, desenho do vid_0026 mas em AÇO (claro e escuro), como os demais corpos do vídeo:
# azul-claro é da força e violeta é da velocidade, então as cores ficam só para os vetores.
CAR1, CAR1_L = C1F, "#E3EAF6"          # caminhão: aço claro
CAR2, CAR2_L = C2F, "#B8C4DA"          # carro: aço escuro


class Carro(VGroup):
    """Veículo visto de cima (copiado do vid_0026): rodas, teto, para-brisa, faróis e lanternas, em vidro. Construído apontando
    para +x (comprimento L, largura W); `ang` gira o corpo, o rótulo da massa fica sempre de pé. Medidas finas ∝ largura."""

    def __init__(self, L, W, cor, borda, nome, ang=0.0, fs=40):
        super().__init__()
        k = W / 1.85
        rodas = VGroup(*[RoundedRectangle(corner_radius=0.08 * k, width=0.75 * k, height=0.32 * k)
                         .set_fill("#060A16", 1).set_stroke(borda, 1, opacity=0.5).move_to(P3(sx * L * 0.3, sy * (W / 2 - 0.02 * k)))
                         for sx in (-1, 1) for sy in (-1, 1)])
        halo = RoundedRectangle(corner_radius=W * 0.32, width=L + 0.25 * k, height=W + 0.25 * k) \
            .set_fill(opacity=0).set_stroke(borda, 7, opacity=0.18)
        corpo = RoundedRectangle(corner_radius=W * 0.3, width=L, height=W).set_fill(cor, 0.62).set_stroke(borda, 2.4)
        brilho = Line(P3(-L * 0.36, W * 0.36), P3(L * 0.3, W * 0.36)).set_stroke(WHITE_, 1.5, opacity=0.35)
        teto = RoundedRectangle(corner_radius=W * 0.2, width=L * 0.46, height=W * 0.7).move_to(P3(-L * 0.06, 0)) \
            .set_fill(interpolate_color(ManimColor(cor), ManimColor(BACKGROUND_COLOR), 0.55), 0.95).set_stroke(borda, 1.2, opacity=0.7)
        xf = L * 0.17
        para = Polygon(P3(xf, W * 0.33), P3(xf + L * 0.13, W * 0.4), P3(xf + L * 0.13, -W * 0.4), P3(xf, -W * 0.33)) \
            .set_fill("#081022", 0.95).set_stroke(borda, 1.2, opacity=0.8)
        tras = Polygon(P3(-L * 0.29, W * 0.32), P3(-L * 0.36, W * 0.37), P3(-L * 0.36, -W * 0.37), P3(-L * 0.29, -W * 0.32)) \
            .set_fill("#081022", 0.9).set_stroke(borda, 1, opacity=0.6)
        far = VGroup(*[Ellipse(width=0.22 * k, height=0.34 * k).set_fill("#F2F8FF", 1).set_stroke(width=0)
                       .move_to(P3(L / 2 - 0.12 * k, s * W * 0.32)) for s in (-1, 1)])
        lan = VGroup(*[RoundedRectangle(corner_radius=0.04 * k, width=0.12 * k, height=0.36 * k).set_fill(DIM, 0.9).set_stroke(width=0)
                       .move_to(P3(-L / 2 + 0.08 * k, s * W * 0.32)) for s in (-1, 1)])
        self.front = corpo
        self.corpo = VGroup(rodas, halo, corpo, brilho, teto, para, tras, far, lan)
        self.corpo.rotate(ang, about_point=ORIGIN)
        self.rot = MathTex(nome, font_size=fs, color=WHITE_).move_to(ORIGIN)
        self.add(self.corpo, self.rot)

    @property
    def c(self):
        return self.front.get_center()


def lam_cr(lam):
    """Centro e raio do círculo de estados de p⃗₁f, em unidades de p₁ᵢ: C = 1/(1+λ), R = λ/(1+λ)."""
    return 1 / (1 + lam), lam / (1 + lam)


_PH0 = pol(_d_mais(LAM_EX, HK_TH1), HK_TH1)[:2]      # desfecho real do hook, como ponto do círculo (unidades de p₁ᵢ)
# o círculo passa por p₁ᵢ e por (1−λ)/(1+λ) p₁ᵢ sobre o eixo; a tangência cai em sen θ = λ (conferido em desenvolvimento)
_C, _R = lam_cr(LAM_EX)
assert abs((_C + _R) - 1.0) < 1e-12 and abs((_C - _R) - (1 - LAM_EX) / (1 + LAM_EX)) < 1e-12
assert abs(_R * _R - (_C * np.sin(np.radians(THMAX_EX))) ** 2) < 1e-12
assert abs(_d_mais(LAM_EX, HK_TH1) ** 2 - ((_PH0[0]) ** 2 + (_PH0[1]) ** 2)) < 1e-12
assert abs((_PH0[0] - _C) ** 2 + _PH0[1] ** 2 - _R ** 2) < 1e-12                  # o desfecho do hook está no círculo


class DecimalPT(DecimalNumber):
    """DecimalNumber com vírgula decimal (pt-BR)."""

    def _get_num_string(self, number):
        return super()._get_num_string(number).replace(".", ",")


class Plano:
    """Plano das componentes de p⃗₁f (eixo x ao longo de p⃗₁ᵢ): origem O na tela e u = comprimento de tela de p₁ᵢ.
    É um plano de ESTADOS, nunca um espaço físico: fundo, grade e aviso próprios."""

    def __init__(self, O, u):
        self.O, self.u = np.asarray(O, float), float(u)

    def pt(self, x, y=0.0):
        return self.O + P3(x * self.u, y * self.u)

    def base(self, x0, x1, y0, y1, gs=0.25, ly_lado=RIGHT):
        pan = RoundedRectangle(corner_radius=0.14, width=(x1 - x0) * self.u, height=(y1 - y0) * self.u) \
            .set_stroke(DIM, 1.4, opacity=0.45).set_fill([_fundo(0.12), _fundo(0.05)], opacity=1.0) \
            .move_to(self.pt((x0 + x1) / 2, (y0 + y1) / 2)).set_z_index(-3)
        pan.set_sheen_direction(DOWN)
        fil = RoundedRectangle(corner_radius=0.1, width=(x1 - x0) * self.u - 0.14, height=(y1 - y0) * self.u - 0.14) \
            .set_stroke(DIM, 1.0, opacity=0.14).set_fill(opacity=0).move_to(pan).set_z_index(-3)
        grade = VGroup()
        for gx in np.arange(np.ceil(x0 / gs) * gs, x1, gs):
            if x0 + 1e-6 < gx < x1 - 1e-6:
                grade.add(Line(self.pt(gx, y0), self.pt(gx, y1)).set_stroke(DIM, 1, opacity=0.11))
        for gy in np.arange(np.ceil(y0 / gs) * gs, y1, gs):
            if y0 + 1e-6 < gy < y1 - 1e-6:
                grade.add(Line(self.pt(x0, gy), self.pt(x1, gy)).set_stroke(DIM, 1, opacity=0.11))
        grade.set_z_index(-2)
        ex = arrow(self.pt(x0 + 0.03, 0), self.pt(x1 - 0.03, 0), color=DIM, width=2.5, tip=0.16, z=-1)
        ey = arrow(self.pt(0, y0 + 0.03), self.pt(0, y1 - 0.03), color=DIM, width=2.5, tip=0.16, z=-1)
        lx = M("p_{1f,x}", size=26).next_to(ex.get_end(), DOWN, buff=0.1).shift(RIGHT * 0.1)
        ly = M("p_{1f,y}", size=28).next_to(ey.get_end(), ly_lado, buff=0.12)
        return VGroup(pan, fil, grade, ex, ey, lx, ly)


class Eq:
    """Equação em partes semânticas, com os glifos achatados na ordem da compilação.
    `.mt` = MathTex em várias partes (para TransformMatchingTex); `.m` = VGroup(VGroup(glifos)) (para TransformByGlyphMap);
    `.idx[nome]` = índices de glifo da parte. Cor por parte: None (branco), uma cor, 'num' (numerador do que é fração, magenta)
    ou 'num1' (idem, pulando o primeiro glifo da esquerda, ex.: λ)."""

    def __init__(self, partes, size=M_EQ, w=None, pos=None):
        size = max(size, M_MIN)
        self.mt = MathTex(*[p[1] for p in partes], font_size=size)
        if w and self.mt.width > w:
            self.mt.scale_to_fit_width(w)
        if pos is not None:
            self.mt.move_to(pos)
        self.mt.set_color(WHITE_)
        self.idx, self.gl, i = {}, [], 0
        for p, sub in zip(partes, self.mt.submobjects):
            g = list(sub.family_members_with_points())
            self.idx[p[0]] = list(range(i, i + len(g)))
            if p[1].startswith(r"\vec") and len(g) > 1:         # vetor: a seta (acento, a mais alta) e a base (letra + índices)
                k = max(range(len(g)), key=lambda j: g[j].get_center()[1])
                self.idx[p[0] + "@s"] = [i + k]
                self.idx[p[0] + "@b"] = [i + j for j in range(len(g)) if j != k]
            self.gl += g
            i += len(g)
        self.m = VGroup(VGroup(*self.gl))
        self.forma = "mt"
        for p in partes:
            if len(p) > 2 and p[2] is not None:
                self.cor(p[0], p[2])

    def parte(self, n):
        return VGroup(*[self.gl[i] for i in _spec(self, n)])

    def _fr(self, n):
        """Fração de uma parte: (barra, numerador, denominador) como listas de índices de glifo (numerador/denominador da esquerda para a direita)."""
        ix = self.idx[n]
        gs = [self.gl[i] for i in ix]
        k = max(range(len(gs)), key=lambda j: gs[j].width)
        bx0, bx1, by = gs[k].get_left()[0], gs[k].get_right()[0], gs[k].get_center()[1]
        dentro = [j for j in range(len(gs)) if j != k and bx0 - 0.05 <= gs[j].get_center()[0] <= bx1 + 0.05]
        num = [j for j in dentro if gs[j].get_center()[1] > by]          # na ordem do TeX (numerador antes do denominador)
        den = [j for j in dentro if gs[j].get_center()[1] < by]
        return [ix[k]], [ix[j] for j in num], [ix[j] for j in den]

    def num(self, n):
        return self._fr(n)[1]

    def den(self, n):
        return self._fr(n)[2]

    def barra(self, n):
        return self._fr(n)[0]

    def para(self, B, *pares, auto=True):
        """Mapa de glifos de `self` para `B` (MF-Tools). Cada par é (de, para[, kwargs]); `de`/`para` = nome da parte, (nome, i|fatia),
        índices crus ou lista desses; lista vazia = o glifo some (de) ou nasce (para). Partes de mesmo nome e mesmo número de glifos
        que não foram citadas seguem juntas (identidade); o resto entra e sai por fade (auto_fade)."""
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

    def cor(self, n, c):
        gs = [self.gl[i] for i in self.idx[n]]
        if c in ("num", "num1"):
            barra = max(gs, key=lambda g: g.width)
            bx0, bx1, by = barra.get_left()[0], barra.get_right()[0], barra.get_center()[1]
            num = sorted([g for g in gs if g is not barra and g.get_center()[1] > by and bx0 - 0.05 <= g.get_center()[0] <= bx1 + 0.05],
                         key=lambda g: g.get_center()[0])
            for g in (num[1:] if c == "num1" else num):
                g.set_color(MAG)
        else:
            for g in gs:
                g.set_color(c)
        return self


def _spec(E, s):
    """Índices de glifo de uma especificação: 'nome' | ('nome', i|fatia) | inteiro | lista dessas coisas."""
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


class EqJ:
    """Várias equações (linhas) tratadas como uma só nos mapas de glifos: as partes viram 'linha.parte'."""

    def __init__(self, **linhas):
        self.linhas, self.off, self.idx, self.gl, i = linhas, {}, {}, [], 0
        for k, e in linhas.items():
            self.off[k] = i
            for n, ix in e.idx.items():
                self.idx[f"{k}.{n}"] = [j + i for j in ix]
            self.gl += e.gl
            i += len(e.gl)
        self.m = VGroup(VGroup(*self.gl))
        self.mt = VGroup(*[e.mt for e in linhas.values()])
        self.forma = "mt"

    def parte(self, n):
        return VGroup(*[self.gl[i] for i in _spec(self, n)])

    def num(self, n):
        k, p = n.split(".", 1)
        return [j + self.off[k] for j in self.linhas[k].num(p)]

    def den(self, n):
        k, p = n.split(".", 1)
        return [j + self.off[k] for j in self.linhas[k].den(p)]

    def barra(self, n):
        k, p = n.split(".", 1)
        return [j + self.off[k] for j in self.linhas[k].barra(p)]

    para = Eq.para


class Pilha:
    """Equações em passos: a atual em destaque; as anteriores recuam para cima (menores e apagadas) e saem aos poucos."""

    def __init__(self, cena, x, ys, esc=0.74, ops=(0.45, 0.28, 0.16)):
        self.cena, self.x, self.ys, self.esc, self.ops = cena, x, ys, esc, ops
        self.fantasmas = []
        self.por = {}

    def copia(self, E, spec):
        """Glifos (do fantasma recuado de `E`) de uma parte: fonte de um TransformFromCopy."""
        g = self.por[id(E)]
        return VGroup(*[g[0][i] for i in _spec(E, spec)])

    def recua(self, fantasma, de=None):
        """Registra `fantasma` (cópia da equação atual) como o passo mais recente e devolve as animações do recuo."""
        if de is not None:
            self.por[id(de)] = fantasma
        self.cena.add(fantasma)
        anims = [fantasma.animate.scale(self.esc).move_to(P3(self.x, self.ys[0])).set_opacity(self.ops[0])]
        self.fantasmas.insert(0, fantasma)
        for i, f in enumerate(self.fantasmas[1:], start=1):
            if i < len(self.ys):
                anims.append(f.animate.move_to(P3(self.x, self.ys[i])).set_opacity(self.ops[min(i, len(self.ops) - 1)]))
            else:
                anims.append(FadeOut(f))
        self.fantasmas = self.fantasmas[:len(self.ys)]
        return anims

    def limpa(self):
        anims = [FadeOut(f) for f in self.fantasmas]
        self.fantasmas = []
        return anims


class Choque:
    """Dois discos que se chocam em t = 0 (relógio físico). Antes: v1i, v2i constantes; depois: v1f, v2f.
    c1c, c2c = centros no instante do contato. Setas de velocidade (violeta, finas) saem da borda do disco."""

    def __init__(self, c1c, c2c, v1i, v2i, v1f, v2f, r1, r2, t0=-1.3, ka=0.5, setas=True, wseta=4.0, n1=None, n2=None):
        self.c1c, self.c2c = np.asarray(c1c, float), np.asarray(c2c, float)
        self.v1i, self.v2i, self.v1f, self.v2f = [np.asarray(x, float) for x in (v1i, v2i, v1f, v2f)]
        self.r1, self.r2, self.ka, self.wseta = r1, r2, ka, wseta
        self.t = ValueTracker(t0)
        self.d1, self.d2 = Disco(C1F, r1, n1), Disco(C2F, r2, n2)
        self.d1.move_to(self.pos(1))
        self.d2.move_to(self.pos(2))
        self.d1.add_updater(lambda m: m.move_to(self.pos(1)))
        self.d2.add_updater(lambda m: m.move_to(self.pos(2)))
        self.setas = always_redraw(self._setas) if setas else VGroup()

    def vel(self, k):
        depois = self.t.get_value() > 1e-6
        return (self.v1f, self.v2f)[k - 1] if depois else (self.v1i, self.v2i)[k - 1]

    def pos(self, k):
        return (self.c1c, self.c2c)[k - 1] + self.vel(k) * self.t.get_value()

    def contato_pt(self):
        return self.c1c + unit(self.c2c - self.c1c) * self.r1

    def _setas(self):
        g = VGroup()
        for k, r in ((1, self.r1), (2, self.r2)):
            v = self.vel(k)
            if np.linalg.norm(v) < 0.05:
                continue
            a = self.pos(k) + unit(v) * (r + 0.06)
            g.add(arrow(a, a + v * self.ka, color=VEL, width=self.wseta, tip=0.17))
        return g

    def group(self):
        return VGroup(self.d1, self.d2, self.setas)

    def solta(self):
        for m in (self.d1, self.d2, self.setas):
            m.clear_updaters()

    def flash(self):
        return Flash(self.contato_pt(), color=WHITE_, line_length=0.2, flash_radius=0.1, num_lines=10, run_time=0.35)


class Colisoes2DYT014(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3)
        self.wm.set_z_index(40)
        self.h1 = txt("MECÂNICA · COLISÕES EM 2D", 17, color=DIM, op=0.5, fixo=True).to_corner(UL, buff=0.32).set_z_index(40)
        self.h2 = None
        self._pend = []
        self.add(self.wm, self.h1)
        # sincronia: trecho k = conteúdo da cena entre a âncora k−1 e a âncora k; FP/FW = fatores de play/espera do trecho
        self.k, self.rec, self.atrasos = 0, [], []
        self._ini_trecho()
        marcas = []
        for nome in ("hook", "abertura", "c01", "c02", "c03", "c04", "c05", "c06", "c07", "c08", "c09", "c10", "c11",
                     "c12", "c13", "c14", "cta"):
            self.next_section(nome, skip_animations=bool(SECOES) and nome not in SECOES)
            t0 = self.renderer.time
            getattr(self, nome)()
            marcas.append((nome, t0, self.renderer.time))
        self.an("FIM")
        for nome, a, b in marcas:
            print(f"[tempo] {nome}: {a:7.1f} s -> {b:7.1f} s ({b - a:5.1f} s)")
        if GRAVAR:
            (AQUI / "ritmo_bruto.json").write_text(json.dumps(self.rec, ensure_ascii=False, indent=0), encoding="utf-8")
            print(f"[sync] {len(self.rec)} trechos gravados em ritmo_bruto.json")
        elif RITMO:
            print(f"[sync] {len(self.rec)} âncoras; {len(self.atrasos)} atrasos > 1 quadro; cena {self.renderer.time:.2f} s")
            for a in self.atrasos:
                print(f"[sync] ATRASO {a[0]} {a[1]!r}: alvo {a[2]:.2f} s, real {a[3]:.2f} s")

    # ── sincronia com a voz ──────────────────────────────────────────────────────────────────────────────────
    def _ini_trecho(self):
        self.t_ini, self.sP, self.sW = float(self.renderer.time), 0.0, 0.0
        if RITMO and self.k < len(RITMO["trechos"]):
            r = RITMO["trechos"][self.k]
            self.FP, self.FW = r["fp"], r["fw"]
        else:
            self.FP, self.FW = 1.0, 1.0

    def an(self, aid, frase=None):
        """Âncora: o próximo evento visual começa LEAD s antes da fala `frase` da âncora `aid` (voz com pausas de ritmo)."""
        agora = float(self.renderer.time)
        if GRAVAR or not RITMO:
            self.rec.append({"id": aid, "frase": frase or "", "P": round(self.sP, 4), "W": round(self.sW, 4),
                             "D": round(agora - self.t_ini, 4)})
        else:
            r = RITMO["trechos"][self.k]
            assert (r["id"], r["frase"]) == (aid, frase or ""), f"âncora fora de ordem: {aid} {frase!r} x {r['id']} {r['frase']!r}"
            alvo = r["alvo"]
            if alvo - agora > 1e-3:
                Scene.wait(self, alvo - agora)
            elif agora - alvo > 1.5 / config.frame_rate:
                self.atrasos.append((aid, frase, alvo, agora))
            self.rec.append((aid, frase, alvo, float(self.renderer.time)))
        self.k += 1
        self._ini_trecho()

    # ── auditoria de sobreposições (desenvolvimento: AUDITORIA=1) ─────────────────────────────────────────────
    def wait(self, duration=1.0, *a, **kw):
        if AUDITORIA:
            self._auditar()
        if STILL is not None and self.renderer.time >= STILL:     # still: com -s, salva este quadro
            from manim.utils.exceptions import EndSceneEarlyException
            raise EndSceneEarlyException()
        self.sW += duration
        return super().wait(duration * self.FW, *a, **kw)

    def _auditar(self):
        self.update_mobjects(0)
        itens, linhas = [], []

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
                    itens.append(("txt", m))
                return
            if isinstance(m, Arrow):
                if op(m) > 0.08:
                    linhas.append(m)                      # seta = linha: só conta se atravessar um texto
                return
            if isinstance(m, (Disco, Corpo, Carro)):
                itens.append(("corpo", m.front))
                return
            if isinstance(m, (Line, DashedVMobject)) and not isinstance(m, Arrow):
                if op(m) > 0.3:
                    linhas.append(m)
                return
            for s in m.submobjects:
                walk(s)

        for top in self.mobjects:
            walk(top)

        def bb(m):
            (x0, y0, _), (x1, y1, _) = m.get_critical_point(DL), m.get_critical_point(UR)
            return x0 + 0.02, y0 + 0.02, x1 - 0.02, y1 - 0.02

        def nome(k, m):
            if k == "corpo":
                cc = m.get_center()
                return f"corpo@({cc[0]:.1f},{cc[1]:.1f})r{m.width / 2:.2f}"
            cc = m.get_center()
            if isinstance(m, Text):
                return f"{k}:'{m.text[:30]}'@({cc[0]:.1f},{cc[1]:.1f})"
            if isinstance(m, SingleStringMathTex):
                return f"{k}:'{m.get_tex_string()[:30]}'@({cc[0]:.1f},{cc[1]:.1f})"
            return k

        t = self.renderer.time
        for i, (ka, a) in enumerate(itens):
            if ka == "txt":
                x0, y0, x1, y1 = bb(a)
                if x0 < -7.7 or x1 > 7.7 or y0 < -4.35 or y1 > 4.35:
                    print(f"[audit] {t:7.1f}s FORA DO QUADRO {nome(ka, a)}")
            for kb, b in itens[i + 1:]:
                if "txt" not in (ka, kb):
                    continue
                if a in b.get_family() or b in a.get_family():
                    continue
                ax0, ay0, ax1, ay1 = bb(a)
                bx0, by0, bx1, by1 = bb(b)
                w, h = min(ax1, bx1) - max(ax0, bx0), min(ay1, by1) - max(ay0, by0)
                if w > 0.03 and h > 0.03:
                    print(f"[audit] {t:7.1f}s SOBREPOSICAO {nome(ka, a)}  x  {nome(kb, b)}  ({w:.2f}x{h:.2f})")
        for ka, a in itens:
            if ka != "txt":
                continue
            x0, y0, x1, y1 = bb(a)
            for ln in linhas:
                if ln in a.get_family():
                    continue
                pts = np.vstack([np.array([x.point_from_proportion(q) for q in np.linspace(0, 1, 24)])
                                 for x in ln.family_members_with_points()])
                dentro = (pts[:, 0] > x0) & (pts[:, 0] < x1) & (pts[:, 1] > y0) & (pts[:, 1] < y1)
                if dentro.any():
                    print(f"[audit] {t:7.1f}s LINHA SOBRE TEXTO {nome(ka, a)}")
                    break

    # ── utilidades ───────────────────────────────────────────────────────────────────────────────────────────
    def fixos(self):
        return {self.wm, self.h1, *([self.h2] if self.h2 else [])}

    def clear(self, *keep, rt=0.7):
        keep = self.fixos() | set(keep)
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=rt)
        for m in mobs:
            m.clear_updaters()
        self.remove(*mobs)
        self._frase = None

    def frase(self, s, cor=WHITE_, size=T_FRASE, y=FAIXA_Y, x=0.0, bold=True):
        """Frase de ideia num ponto fixo (faixa inferior), uma por vez: a anterior sai antes da próxima entrar."""
        if getattr(self, "_frase", None) is not None:
            self.play(FadeOut(self._frase), run_time=0.3)
            self.remove(self._frase)
            self._frase = None
        if s:
            self._frase = txt(s, size, color=cor, bold=bold).move_to(P3(x, y))
            self.play(FadeIn(self._frase, shift=0.12 * UP), run_time=0.5)
        return self._frase

    def pulso(self, m, cor=WHITE_, k=1.08, rt=0.7):
        self.play(Indicate(m, color=cor, scale_factor=k), run_time=rt)

    def passo(self, pil, A, B, extra=(), rt=0.9):
        """Afirmação NOVA (sem termos a levar de A para B): A recua (fantasma) e sai do slot; só depois B entra por fade."""
        old = A.m if A.forma == "m" else A.mt
        self.play(*pil.recua(A.m.copy(), de=A), FadeOut(old), run_time=0.6)
        self.play(FadeIn(B.mt, shift=0.15 * UP), *extra, run_time=rt)
        A.forma, B.forma = None, "mt"

    def recua_sai(self, pil, A, rt=0.6):
        """A equação A recua como fantasma e sai do slot (sem entrar nada ainda): usado quando a seguinte nasce de cópias."""
        old = A.m if A.forma == "m" else A.mt
        self.play(*pil.recua(A.m.copy(), de=A), FadeOut(old), run_time=rt)
        A.forma = None

    def avanca(self, A, B, *pares, rt=1.8, pil=None, extra=(), auto=True, **kw):
        """A → B por MF-Tools: os termos de A NAVEGAM até o lugar que ocupam em B (mapa por partes nomeadas, `Eq.para`).
        Com `pil`, uma cópia de A recua como fantasma enquanto a equação avança. Depois, B é quem está na cena (forma .m)."""
        ents = A.para(B, *pares, auto=auto)
        anims = list(pil.recua(A.m.copy(), de=A)) if pil is not None else []
        anims.append(TransformByGlyphMap(A.m, B.m, *ents, auto_fade=True, run_time=rt, **kw))
        self.play(*anims, *extra)
        A.forma, B.forma = None, "m"
        return B

    def nasce(self, E, fontes=(), fade=(), rt=1.4, extra=()):
        """E nasce de termos que já estão na tela: `fontes` = [(origem, parte-de-E)] viajam por TransformFromCopy; o resto de E entra
        por fade. Depois E fica na cena em forma .m (pronto para avançar)."""
        usados = set()
        anims = []
        for orig, spec in fontes:
            ix = _spec(E, spec)
            usados.update(ix)
            anims.append(TransformFromCopy(orig, VGroup(*[E.gl[i] for i in ix])))
        resto = [E.gl[i] for i in range(len(E.gl)) if i not in usados]
        if resto:
            anims.append(FadeIn(VGroup(*resto), shift=0.1 * UP))
        self.play(*anims, *fade, *extra, run_time=rt)
        self.add(E.m)
        E.forma = "m"
        return E

    def secao(self, s):
        """Título da cena (linha 2 do header): o antigo sai antes de o novo entrar."""
        novo = txt(s, T_TITULO, op=0.95).next_to(self.h1, DOWN, buff=0.14, aligned_edge=LEFT).set_z_index(40) if s else None
        if self.h2 is not None:
            velho, self.h2 = self.h2, None
            Scene.play(self, FadeOut(velho), run_time=0.25)
        if novo is not None:
            self._pend.append(FadeIn(novo))
        self.h2 = novo

    def play(self, *anims, **kw):
        if anims and all(isinstance(a, Wait) for a in anims):     # Scene.wait passa por aqui: já escalado em wait()
            return super().play(*anims, **kw)
        if self._pend:
            anims, self._pend = (*anims, *self._pend), []
        rt = kw.get("run_time")
        if rt is None:
            rt = max([getattr(a, "run_time", 1.0) for a in anims] or [1.0])
        self.sP += rt
        kw["run_time"] = rt * self.FP
        return super().play(*anims, **kw)

    def hl(self, s, y=3.0, size=T_HL, color=WHITE_, x=0.0):
        return txt(s, size, color=color, bold=True).move_to(P3(x, y))

    def swap(self, old, new, rt=1.1, **kw):
        self.play(TransformMatchingTex(old, new, **kw), run_time=rt)
        return new

    def tag_plano(self, fisico=True):
        """Aviso curto de em qual dos dois planos estamos (nunca confundir o círculo com uma trajetória).
        Texto sem caixa, com filete embaixo, como o indicador ANTES → CONTATO → DEPOIS do yt_0013."""
        if fisico:
            t = txt("ESPAÇO FÍSICO", 18, color=DIM, op=0.75)
            sub = Line(t.get_corner(DL) + DOWN * 0.07, t.get_corner(DR) + DOWN * 0.07).set_stroke(DIM, 1.6, opacity=0.6)
        else:
            t = VGroup(txt("PLANO DE", 20, color=WHITE_, op=0.95), M(r"\vec p_{1f}", size=30)).arrange(RIGHT, buff=0.14)
            sub = Line(t.get_corner(DL) + DOWN * 0.07, t.get_corner(DR) + DOWN * 0.07).set_stroke(WHITE_, 2, opacity=0.8)
        return VGroup(t, sub)

    def settle(self, new):
        """Depois de um TransformMatchingTex: tira da cena as peças soltas e deixa só `new`."""
        fam = {id(x) for x in new.get_family()}
        self.remove(*[m for m in self.mobjects if m is not new and (id(m) in fam or
                      (m.submobjects and all(id(x) in fam for x in m.get_family()[1:])))])
        self.add(new)
        return new

    def logo(self, largura):
        img = ImageMobject(str(ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"))
        arr = img.get_pixel_array()
        ys, xs = np.nonzero(arr[:, :, 3] > 8)
        return ImageMobject(arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).set_width(largura)

    def triangulo(self, O, K, labels=True, size=36, wi=8, wc=6):
        """Triângulo de momentos do exemplo genérico: p₁ᵢ (base), p₁f (de O) e p₂f (ponta com cauda) fechando."""
        O = np.asarray(O, float)
        T, Q = O + P3(GP1I * K, 0), O + GV1F * K
        d = dict(pi=arrow(O, T, color=MAG, width=wi, tip=0.24), p1=arrow(O, Q, color=MAG, width=wc, tip=0.2),
                 p2=arrow(Q, T, color=MAG_L, width=wc, tip=0.2), O=O, Q=Q, T=T)
        if labels:
            d["li"] = lab_at(M(r"\vec p_{1i}", size=size), O, T, lado=-1)
            d["l1"] = lab_at(M(r"\vec p_{1f}", size=size), O, Q, lado=1)
            d["l2"] = lab_at(M(r"\vec p_{2f}", size=size), Q, T, lado=1)
        return d

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # HOOK — uma colisão que começa sobre o eixo e termina fora dele: para onde pode sair?
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # HOOK (L-CENA) — uma colisão que começa sobre o eixo e termina fora dele: para onde pode sair?
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def hook(self):
        r1, r2 = 0.78, 0.4                          # corpo pesado e corpo leve
        n = pol(1.0, -HK_PHI)
        T2 = P3(-0.6, -0.5)                         # alvo parado
        Tc = T2 - n * (r1 + r2)                     # disco 1 no instante do contato
        ya = Tc[1]
        eixo = DashedLine(P3(-7.0, ya), P3(0.0, ya), dash_length=0.14).set_stroke(DIM, 1.8, opacity=0.5).set_z_index(-1)
        vig = vinheta(P3(-0.8, 0.2), 4.2, VEL, 0.10)
        ch = Choque(Tc, T2, P3(HK_V, 0), P3(0, 0), HK_V1F, HK_V2F, r1, r2, t0=-1.7, ka=0.55, wseta=5.5)
        self.an("H1")
        self.play(FadeIn(vig), Create(eixo), FadeIn(ch.group()), run_time=0.9)
        self.an("H1", "um disco pesado vem")
        self.play(ch.t.animate.set_value(0.0), rate_func=rush_into, run_time=1.7 * LENTO)
        self.an("H1", "e bate num disco leve")
        self.play(ch.flash(), Flash(ch.contato_pt(), color=WHITE_, line_length=0.35, flash_radius=0.2, num_lines=14, run_time=0.45))
        ch.t.set_value(1e-5)
        self.an("H1", "repara")
        self.play(ch.t.animate.set_value(0.9), rate_func=rate_functions.ease_out_cubic, run_time=1.6 * LENTO)
        ch.solta()
        # a trajetória real e as direções candidatas para o disco incidente (a de 40° será revelada impossível)
        real = Line(Tc, ch.pos(1)).set_stroke(GEO, 2.4, opacity=0.55)
        cands = VGroup()
        for a in HOOK_CAND:
            L_ = min(4.4, (3.0 - Tc[1]) / np.sin(np.radians(a)))
            cands.add(DashedLine(Tc, Tc + pol(L_, a), dash_length=0.16).set_stroke(VEL, 3.4, opacity=0.85))
        fim40 = Tc + pol(min(4.4, (3.0 - Tc[1]) / np.sin(np.radians(HOOK_CAND[1]))), HOOK_CAND[1])
        fim25 = Tc + pol(min(4.4, (3.0 - Tc[1]) / np.sin(np.radians(HOOK_CAND[0]))), HOOK_CAND[0])

        def xis_em(p, s=0.16):
            return VGroup(Line(p + P3(-s, -s), p + P3(s, s)), Line(p + P3(-s, s), p + P3(s, -s))).set_stroke(WHITE_, 2.2, opacity=0.95)
        xis = VGroup(xis_em(fim25), xis_em(fim40))                       # as duas direções são proibidas (> 14,5°)
        self.an("H1", "o pesado desvia")
        self.play(Create(real), run_time=0.5)
        self.an("H2")
        self.wait(0.2)
        self.an("H2", "vinte e cinco graus")
        self.play(Create(cands[0]), run_time=0.8)
        self.an("H2", "quarenta graus")
        self.play(Create(cands[1]), run_time=0.8)
        self.an("H3", "ele não deixa passar")
        self.play(FadeIn(xis, scale=0.6), run_time=0.4)
        q = VGroup(txt("PARA ONDE", 44, color=CYAN, bold=True), txt("ELA PODE SAIR?", 44, color=CYAN, bold=True)).arrange(DOWN, buff=0.15) \
            .move_to(P3(5.2, 0.3))
        self.an("H3", "por quê")
        self.play(FadeIn(q, shift=0.12 * UP), Indicate(xis, color=WHITE_, scale_factor=1.15), run_time=0.8)
        self.wait(2.0)
        self.clear(rt=0.6)

    def abertura(self):
        """Bem-vindos (logo) → título com NESTE VÍDEO (~3 s)."""
        logo = self.logo(4.6).move_to(P3(0, 0.6))
        wel = txt("BEM-VINDOS AO PARALLAX LAB", 34).move_to(P3(0, -1.3))
        tit = txt("COLISÕES EM 2D", 52, color=CYAN, bold=True).move_to(P3(0, 0.45))
        sub = txt("NESTE VÍDEO: PARA ONDE OS CORPOS PODEM SAIR", 28, op=0.85).move_to(P3(0, -0.5))
        self.an("A1")
        self.play(FadeIn(logo, scale=0.94), FadeIn(wel, shift=0.1 * UP), run_time=1.0)
        self.an("A2")
        self.play(FadeOut(logo), FadeOut(wel), FadeIn(tit, shift=0.1 * UP), run_time=0.8)
        self.an("A2", "a ideia é você sair")
        self.play(FadeIn(sub, shift=0.1 * UP), run_time=0.8)
        self.an("A2", "sem bola de cristal")
        self.play(Indicate(tit, color=CYAN, scale_factor=1.05), run_time=1.0)
        self.an("C01-1")
        self.play(FadeOut(tit), FadeOut(sub), run_time=0.6)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C01 (L-CENA) — retomada: a colisão em 1D era um caso especial (sem recap quantitativo)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c01(self):
        self.secao("DO 1D PARA O 2D")
        ty = 0.5
        trilho = Line(P3(-7.2, ty), P3(7.2, ty)).set_stroke(WHITE_, 2.8, opacity=0.45)
        r1, r2 = 0.55, 0.42
        ch = Choque(P3(-0.97, ty), P3(0.0, ty), P3(2.8, 0), P3(0, 0), P3(0.7, 0), P3(3.5, 0), r1, r2, t0=-1.6, ka=0.55, wseta=5.0)
        self.play(Create(trilho), FadeIn(ch.group()), run_time=0.9)
        self.an("C01-1", "lá tudo acontecia")
        self.play(ch.t.animate.set_value(0.0), rate_func=linear, run_time=1.6 * LENTO)
        self.an("C01-1", "e a gente viu")
        self.play(ch.flash())
        ch.t.set_value(1e-5)
        self.play(ch.t.animate.set_value(1.5), rate_func=rate_functions.ease_out_sine, run_time=1.6 * LENTO)
        ch.solta()
        # a linha era só um eixo: o plano em volta aparece e as outras direções ficam disponíveis
        grade = VGroup(*[Line(P3(x, -3.0), P3(x, 3.05)).set_stroke(DIM, 1, opacity=0.12) for x in np.arange(-7.0, 7.1, 1.0)],
                       *[Line(P3(-7.2, y), P3(7.2, y)).set_stroke(DIM, 1, opacity=0.12) for y in np.arange(-3.0, 3.1, 1.0)])
        o = P3(-0.5, ty)
        raios = VGroup(*[DashedLine(o, o + pol(2.5, a), dash_length=0.16).set_stroke(VEL, 3, opacity=0.65)
                         for a in (-70, -45, -22, 22, 45, 70)])
        self.an("C01-1", "só que a vida real")
        self.play(FadeIn(grade), run_time=0.9)
        self.an("C01-1", "pensa numa sinuca")
        self.play(trilho.animate.set_stroke(WHITE_, 5, opacity=0.95), Create(raios[0]), Create(raios[3]), run_time=1.0)
        self.an("C01-1", "ou em dois carros")
        self.play(Create(raios[1]), Create(raios[4]), run_time=1.0)
        self.an("C01-1", "cada corpo pode sair")
        self.play(Create(raios[2]), Create(raios[5]), run_time=1.0)
        k = self.hl("1D = CASO ESPECIAL", y=-3.5, size=54)
        self.an("C01-2")
        self.play(FadeIn(k, shift=0.1 * UP), run_time=0.7)
        self.an("C01-2", "a física é a mesma")
        self.play(Indicate(trilho, color=WHITE_, scale_factor=1.02), run_time=0.9)
        self.an("C01-2", "o que muda")
        self.play(Indicate(raios, color=VEL, scale_factor=1.04), run_time=0.9)
        self.wait(1.0)
        self.clear(rt=0.6)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C02 (L-CENA) — o momento sempre foi um vetor: triângulo de momentos no espaço físico
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c02(self):
        self.secao("MOMENTO É UM VETOR")
        KP = 0.5
        yA = 1.3
        # ANTES: partícula 1 chega ao longo de x; 2 parada
        da1, da2 = Disco(C1F, 0.36, "m_1").move_to(P3(-6.8, yA)), Disco(C2F, 0.3, "m_2").move_to(P3(-4.2, yA))
        pia = arrow(P3(-6.8 + 0.46, yA), P3(-6.8 + 0.46 + GP1I * KP, yA), color=MAG, width=6.5, tip=0.22)
        lia = lab_at(M(r"\vec p_{1i}", size=34), pia.get_start(), pia.get_end(), lado=1)
        t_a = txt("ANTES", T_SMALL, op=0.85).move_to(P3(-5.5, 2.6))
        antes = VGroup(da1, da2, pia, lia, t_a)
        # DEPOIS: saem em direções diferentes
        oc = P3(-2.2, yA)
        dd1, dd2 = Disco(C1F, 0.36, "m_1").move_to(oc + pol(0.85, GTH1)), Disco(C2F, 0.3, "m_2").move_to(oc + pol(0.7, -GTH2))
        a1 = arrow(dd1.c + unit(GV1F) * 0.46, dd1.c + unit(GV1F) * 0.46 + GV1F * KP, color=MAG, width=6.5, tip=0.22)
        a2 = arrow(dd2.c + unit(GV2F) * 0.4, dd2.c + unit(GV2F) * 0.4 + GV2F * KP, color=MAG_L, width=6.5, tip=0.22)
        l1 = lab_at(M(r"\vec p_{1f}", size=34), a1.get_start(), a1.get_end(), lado=1)
        l2 = lab_at(M(r"\vec p_{2f}", size=34), a2.get_start(), a2.get_end(), lado=-1)
        t_d = txt("DEPOIS", T_SMALL, op=0.85).move_to(P3(-3.6, 2.6))
        depois = VGroup(dd1, dd2, a1, a2, l1, l2, t_d)
        self.an("C02-1")
        self.play(FadeIn(antes, shift=0.12 * UP), run_time=1.0)
        self.an("C02-1", "o corpo dois está parado")
        self.play(Indicate(da2, color=WHITE_, scale_factor=1.15), run_time=0.8)
        self.an("C02-1", "depois os dois saem")
        self.play(FadeIn(depois, shift=0.12 * UP), run_time=1.0)
        # P_i = p_1i ; P_f = p_1f + p_2f ; logo p_1i = p_1f + p_2f (uma de cada vez, sem sobrepor)
        XE = 4.6
        L1 = Eq([("a", r"\vec P_i", MAG), ("b", "="), ("c", r"\vec p_{1i}", MAG)], 46, pos=P3(XE, 2.45))
        L2 = Eq([("a", r"\vec P_f", MAG), ("b", "="), ("c", r"\vec p_{1f}", MAG), ("d", "+"), ("e", r"\vec p_{2f}", MAG_L)], 46, pos=P3(XE, 1.35))
        L3 = Eq([("a", r"\vec p_{1i}", MAG), ("b", "="), ("c", r"\vec p_{1f}", MAG), ("d", "+"), ("e", r"\vec p_{2f}", MAG_L)], M_EQ, pos=P3(XE, 0.0))
        L3a = Eq([("a", r"\vec P_i", MAG), ("b", "="), ("c", r"\vec P_f", MAG)], M_EQ, pos=P3(XE, 0.0))
        # os termos das equações saem dos rótulos dos vetores (copiados), não aparecem do nada
        self.an("C02-2")
        self.nasce(L1, [(lia[0], "c")], rt=1.2)
        self.an("C02-2", "depois é a soma")
        self.nasce(L2, [(l1[0], "c"), (l2[0], "e")], rt=1.4)
        self.an("C02-2", "mas atenção")
        self.play(Indicate(L2.parte("d"), color=WHITE_, scale_factor=1.5), run_time=0.8)
        self.an("C02-2", "não dá para somar")
        self.play(Indicate(VGroup(a1, a2), color=MAG, scale_factor=1.06), run_time=1.0)
        # conservação: P⃗ᵢ = P⃗f; depois cada P⃗ vira o que ele é (os símbolos se desmancham em p⃗₁ᵢ e p⃗₁f + p⃗₂f)
        self.an("C02-3")
        self.play(Indicate(VGroup(t_a, t_d), color=WHITE_, scale_factor=1.12), run_time=0.9)
        self.an("C02-3", "e o momento total se conserva")
        self.nasce(L3a, [(L1.parte("a"), "a"), (L2.parte("a"), "c")], rt=1.3)
        self.an("C02-3", "essa é a equação-mãe")
        self.avanca(L3a, L3, (("a@b", 0), ("a@b", 0)), (("a@b", 1), ("a@b", 2)), (("c@b", 0), ("c@b", 0)), (("c@b", 1), ("c@b", 2)),
                    rt=1.8)
        bx = dupla_caixa(L3.m, buff=0.18)
        self.an("C02-3", "pode tatuar")
        self.play(Create(bx), run_time=0.5)
        # triângulo de momentos: p₁f e p₂f ponta com cauda até fechar em p₁ᵢ (num espaço próprio, abaixo dos corpos)
        tr = self.triangulo(P3(-4.8, -3.0), 1.15, size=34)
        tt = txt("TRIÂNGULO DE MOMENTOS NO ESPAÇO FÍSICO", 22, op=0.9).move_to(P3(-2.5, -0.85))
        self.an("C02-4")
        self.play(FadeIn(tt, shift=0.1 * UP), run_time=0.6)
        self.an("C02-4", "o momento inicial na base")
        self.play(ReplacementTransform(pia.copy(), tr["pi"]), FadeIn(tr["li"]), run_time=1.1)
        self.an("C02-4", "o final do corpo um")
        self.play(ReplacementTransform(a1.copy(), tr["p1"]), FadeIn(tr["l1"]), run_time=1.1)
        self.an("C02-4", "e o do corpo dois")
        self.play(ReplacementTransform(a2.copy(), tr["p2"]), FadeIn(tr["l2"]), run_time=1.5)
        n1 = txt("NO 1D: VETORES COLINEARES", 26, op=0.9).move_to(P3(XE, -1.4))
        n2 = txt("NO 2D: A GEOMETRIA APARECE", 26, color=WHITE_).move_to(P3(XE, -2.2))
        self.an("C02-4", "em uma dimensão era uma reta")
        self.play(FadeIn(n1, shift=0.1 * UP), run_time=0.6)
        self.an("C02-4", "em duas ele se abre")
        self.play(FadeIn(n2, shift=0.1 * UP), run_time=0.6)
        self.an("C02-4", "e a geometria aparece")
        self.play(Indicate(VGroup(tr["pi"], tr["p1"], tr["p2"]), color=MAG, scale_factor=1.04), run_time=1.1)
        self.wait(1.0)
        self.clear(rt=0.7)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C03 — uma conservação vetorial = duas equações escalares; ainda falta uma condição física
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c03(self):
        self.secao("DUAS EQUAÇÕES E UMA CONDIÇÃO")
        K = 1.3
        O = P3(-6.9, -2.0)
        tr = self.triangulo(O, K, labels=False)
        Q, T = tr["Q"], tr["T"]
        ex = arrow(O + P3(-0.3, 0), O + P3(6.0, 0), color=DIM, width=2.8, tip=0.18, z=2)
        ey = arrow(O + P3(0, -0.3), O + P3(0, 3.0), color=DIM, width=2.8, tip=0.18, z=2)
        lx, ly = MathTex("x", font_size=34, color=DIM).next_to(ex, RIGHT, buff=0.08), \
            MathTex("y", font_size=34, color=DIM).next_to(ey, UP, buff=0.08)
        self.an("C03-1")
        self.play(Create(ex), Create(ey), FadeIn(lx), FadeIn(ly), run_time=0.9)
        self.an("C03-1", "o horizontal na direção")
        self.play(GrowArrow(tr["pi"]), GrowArrow(tr["p1"]), GrowArrow(tr["p2"]), run_time=1.3)
        # ângulos: θ₁ acima do eixo, θ₂ abaixo do prolongamento horizontal de p₁f
        a1 = arco(O, 1.0, 0, GTH1, w=2.0)
        t1 = M(r"\theta_1", size=34).move_to(O + pol(1.45, GTH1 / 2)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        prol = DashedLine(Q, P3(T[0] + 0.55, Q[1]), dash_length=0.1).set_stroke(DIM, 1.6, opacity=0.8)
        a2 = arco(Q, 0.85, -GTH2, 0, w=2.0)
        t2 = M(r"\theta_2", size=34).move_to(Q + pol(1.25, -GTH2 / 2)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        self.an("C03-1", "o ângulo de saída do corpo um")
        self.play(Create(a1), FadeIn(t1), run_time=0.9)
        self.an("C03-1", "o do corpo dois")
        self.play(Create(prol), Create(a2), FadeIn(t2), run_time=1.1)
        nota = VGroup(MathTex(r"\theta_2", font_size=30), txt("MEDIDO ABAIXO DO EIXO", 22, op=0.85)).arrange(RIGHT, buff=0.14) \
            .move_to(P3(-3.4, -3.5))
        self.an("C03-1", "combinado")
        self.play(FadeIn(nota), run_time=0.5)
        self.wait(0.8)
        # componentes: x em duas chaves sob o eixo; y numa chave à direita
        F1 = P3(Q[0], O[1])
        vert = DashedLine(Q, F1, dash_length=0.1).set_stroke(DIM, 1.6, opacity=0.8)
        bx1 = Brace(Line(O, F1), direction=DOWN, color=DIM, buff=0.08)
        bx2 = Brace(Line(F1, T), direction=DOWN, color=DIM, buff=0.08)
        cx1 = M(r"p_{1f}\cos\theta_1", size=30).next_to(bx1, DOWN, buff=0.06)
        cx2 = M(r"p_{2f}\cos\theta_2", size=30).next_to(bx2, DOWN, buff=0.06)
        bry = Brace(Line(P3(T[0] + 0.55, O[1]), P3(T[0] + 0.55, Q[1])), direction=RIGHT, color=DIM, buff=0.05)
        cy = M(r"p_{1f}\sin\theta_1", "=", r"p_{2f}\sin\theta_2", size=28).next_to(bry, RIGHT, buff=0.08)
        # equações (coluna direita), uma de cada vez
        # a equação vetorial fica no topo; dela saem, por MF-Tools, as duas equações escalares (as cópias V2 e V3 saem de V)
        def eqv():
            return Eq([("a", r"\vec p_{1i}", MAG), ("b", "="), ("c", r"\vec p_{1f}", MAG), ("d", "+"), ("e", r"\vec p_{2f}", MAG_L)],
                      46, pos=P3(4.6, 2.85))
        V, V2, V3 = eqv(), eqv(), eqv()
        tx = txt("EIXO X", 24, color=DIM).move_to(P3(3.3, 2.2))
        ty_ = txt("EIXO Y", 24, color=DIM).move_to(P3(3.3, 1.0))
        X = Eq([("a", "p_{1i}", MAG), ("b", "="), ("c", "p_{1f}", MAG), ("cc", r"\cos\theta_1"), ("d", "+"), ("e", "p_{2f}", MAG_L),
                ("ec", r"\cos\theta_2")], 46, w=5.6, pos=P3(4.6, 1.65))
        Y = Eq([("a", "0"), ("b", "="), ("c", "p_{1f}", MAG), ("cc", r"\sin\theta_1"), ("d", "-"), ("e", "p_{2f}", MAG_L),
                ("ec", r"\sin\theta_2")], 46, w=5.6, pos=P3(4.6, 0.45))
        self.an("C03-2")
        self.play(FadeIn(V.mt, shift=0.12 * UP), run_time=1.0)
        self.wait(0.6)
        self.an("C03-2", "o momento inicial é a soma")
        self.play(Create(vert), GrowFromCenter(bx1), GrowFromCenter(bx2), FadeIn(cx1), FadeIn(cx2), run_time=1.1)
        sai = {"shift": 0.3 * UP, "scale": 0.4}
        self.an("C03-2", "cada uma com o cosseno")
        self.add(V2.m)                                        # cópia exatamente sobre V: é ela que se desfaz na equação do eixo x
        self.play(FadeIn(tx), run_time=0.4)
        self.avanca(V2, X, ("a@b", "a"), ("a@s", [], sai), ("c@b", "c"), ("c@s", [], sai), ("e@b", "e"), ("e@s", [], sai),
                    ([], "cc", {"delay": 0.8}), ([], "ec", {"delay": 0.8}), rt=2.0)
        self.wait(0.6)
        self.an("C03-2", "projeta no vertical")
        self.play(GrowFromCenter(bry), FadeIn(cy), run_time=0.8)
        self.an("C03-2", "o que sobe")
        self.add(V3.m)
        self.play(FadeIn(ty_), run_time=0.4)
        self.avanca(V3, Y, ("a", "a"), ("c@b", "c"), ("c@s", [], sai), ("e@b", "e"), ("e@s", [], sai),
                    ([], "cc", {"delay": 0.8}), ([], "ec", {"delay": 0.8}), rt=2.0)
        self.wait(1.0)
        self.an("C03-2", "uma conservação vetorial")
        h = VGroup(txt("UMA CONSERVAÇÃO VETORIAL", 26), M(r"\Downarrow", size=44), txt("DUAS EQUAÇÕES ESCALARES", 26)) \
            .arrange(DOWN, buff=0.1).move_to(P3(4.6, -1.7))
        self.play(FadeIn(h, shift=0.1 * UP), run_time=0.9)
        self.wait(0.6)
        self.an("C03-3")
        self.clear(rt=0.7)
        # ainda falta uma condição física: três cartões grandes que acendem quando citados
        falta = self.hl("MAS AINDA FALTA UMA CONDIÇÃO FÍSICA", y=2.55, size=42)
        self.play(FadeIn(falta, shift=0.1 * UP), run_time=0.8)
        cards = []
        conteudo = (("ELÁSTICA", M("K_i", "=", "K_f", size=56)),
                    ("COMPLETAMENTE INELÁSTICA", M(r"\vec v_{1f}", "=", r"\vec v_{2f}", size=56)),
                    ("OUTRO CASO", txt("CONDIÇÃO DADA PELO PROBLEMA", 28)))
        for i, (tt_, eq) in enumerate(conteudo):
            x = (-5.0, 0.0, 5.0)[i]
            p = placa(4.7, 3.0, P3(x, 0.2))
            ti = txt(tt_, 26, op=1.0).scale_to_fit_width(min(4.2, txt(tt_, 26).width)).move_to(P3(x, 1.2))
            eq.scale_to_fit_width(min(eq.width, 4.2)).move_to(P3(x, -0.2))
            VGroup(ti, eq).set_opacity(0.3)
            g = VGroup(p, ti, eq)
            cards.append(g)
        self.an("C03-3", "falta uma condição física")
        self.play(Indicate(falta, color=WHITE_, scale_factor=1.04), run_time=0.9)
        self.an("C03-3", "e ela vem do tipo de colisão")
        self.play(*[FadeIn(c) for c in cards], run_time=0.9)
        for c, fr_ in zip(cards, ("elástica a energia", "completamente inelástica os dois", "ou o problema entrega")):
            self.an("C03-3", fr_)
            self.play(VGroup(c[1], c[2]).animate.set_opacity(1.0), c[0][0].animate.set_stroke(CYAN, 2.4, opacity=0.9), run_time=0.7)
            self.play(Indicate(c[2], color=CYAN, scale_factor=1.06), run_time=0.6)
        sint = self.hl("MOMENTO + CONDIÇÃO FÍSICA", y=-2.3, size=54, color=CYAN)
        self.an("C03-3", "moral da história")
        self.play(FadeIn(sint, shift=0.1 * UP), run_time=0.8)
        self.wait(1.0)
        self.clear(rt=0.7)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c04(self):
        self.secao("MASSAS IGUAIS: O ÂNGULO RETO")
        # aparato-âncora na coluna esquerda: ANTES, DEPOIS e o triângulo de velocidades
        r, KV = 0.3, 0.4
        v1i = 3.1                                         # |v₁ᵢ| (setas = KV por unidade)
        a1 = P3(-6.9, 1.55)
        da1, da2 = Disco(C1F, r, "m_1").move_to(a1), Disco(C2F, r, "m_2").move_to(P3(-4.9, 1.55))
        sa = arrow(a1 + RIGHT * (r + 0.06), a1 + RIGHT * (r + 0.06 + v1i * KV), color=VEL, width=4.5, tip=0.2)
        la = lab_at(M(r"\vec v_{1i}", size=30), sa.get_start(), sa.get_end(), lado=1)
        t_a = txt("ANTES", T_SMALL, op=0.85).move_to(P3(-6.2, 2.4))
        antes = VGroup(da1, da2, sa, la, t_a)
        oc = P3(-5.8, -0.1)
        e1, e2 = pol(1.0, 30), pol(1.0, -60)
        dd1, dd2 = Disco(C1F, r, "m_1").move_to(oc + e1 * 0.8), Disco(C2F, r, "m_2").move_to(oc + e2 * 0.8)
        v1f_, v2f_ = v1i * np.cos(np.radians(30)), v1i * np.sin(np.radians(30))
        s1 = arrow(dd1.c + e1 * (r + 0.06), dd1.c + e1 * (r + 0.06 + v1f_ * KV), color=VEL, width=4.5, tip=0.2)
        s2 = arrow(dd2.c + e2 * (r + 0.06), dd2.c + e2 * (r + 0.06 + v2f_ * KV), color=VEL, width=4.5, tip=0.2)
        l1 = lab_at(M(r"\vec v_{1f}", size=30), s1.get_start(), s1.get_end(), lado=1)
        l2 = lab_at(M(r"\vec v_{2f}", size=30), s2.get_start(), s2.get_end(), lado=-1)
        t_d = txt("DEPOIS", T_SMALL, op=0.85).move_to(P3(-6.2, 0.95))
        depois = VGroup(dd1, dd2, s1, s2, l1, l2, t_d)
        hip = M(r"m_1=m_2=m,\ v_{2i}=0", size=38).move_to(P3(2.4, -3.4))
        self.an("C04-1")
        self.play(FadeIn(antes, shift=0.12 * UP), FadeIn(hip, shift=0.12 * UP), run_time=0.9)
        self.an("C04-1", "a bola branca bate")
        self.play(FadeIn(depois, shift=0.12 * UP), run_time=0.9)
        # (1) momento: as massas cortam
        X0, Y0 = 2.4, -0.3
        pil = Pilha(self, X0, (2.8, 1.9, 1.0), esc=0.66)
        E1 = Eq([("m1", "m"), ("a", r"\vec v_{1i}", VEL), ("eq", "="), ("m2", "m"), ("b", r"\vec v_{1f}", VEL), ("pl", "+"),
                 ("m3", "m"), ("c", r"\vec v_{2f}", VEL)], 52, w=9.4, pos=P3(X0, Y0))
        E1b = Eq([("a", r"\vec v_{1i}", VEL), ("eq", "="), ("b", r"\vec v_{1f}", VEL), ("pl", "+"), ("c", r"\vec v_{2f}", VEL)],
                 56, pos=P3(X0, Y0))
        sai = {"shift": 0.55 * UP, "scale": 0.45}                  # o termo que cancela encolhe e sai pra cima
        # os termos nascem dos rótulos de velocidade da figura (cópias que viajam até a equação)
        self.an("C04-2")
        self.nasce(E1, [(la[0], "a"), (l1[0], "b"), (l2[0], "c")], rt=1.6)
        n1 = txt("AS MASSAS SE CANCELAM", 24, color=DIM).move_to(P3(X0, Y0 - 0.95))
        self.an("C04-2", "então cancela")
        self.avanca(E1, E1b, ("m1", [], sai), ("m2", [], sai), ("m3", [], sai), rt=1.6, extra=(FadeIn(n1, shift=0.1 * UP),))
        # triângulo de velocidades (ponta com cauda); Q desliza até o ângulo reto mais adiante
        O, L = P3(-7.0, -3.3), 3.7
        d = ValueTracker(2.35)
        Q = lambda: O + pol(d.get_value(), 30)       # noqa: E731
        T = O + P3(L, 0)
        ti = arrow(O, T, color=VEL, width=6.5, tip=0.24)
        t1 = always_redraw(lambda: arrow(O, Q(), color=VEL, width=5, tip=0.22))
        t2 = always_redraw(lambda: arrow(Q(), T, color=mix(VEL, 0.3), width=5, tip=0.22))
        li = lab_at(M(r"\vec v_{1i}", size=30), O, T, lado=-1)
        lt1 = M(r"\vec v_{1f}", size=30).add_updater(lambda m: lab_at(m, O, Q(), lado=1))
        lt2 = M(r"\vec v_{2f}", size=30).add_updater(lambda m: lab_at(m, Q(), T, lado=1))

        def arco_q():
            q = Q()
            a0 = np.degrees(np.arctan2(*(T - q)[1::-1]))
            a1_ = np.degrees(np.arctan2(*(O - q)[1::-1]))
            return arco(q, 0.36, a1_, a0 if a0 > a1_ else a0 + 360)
        aq = always_redraw(arco_q)
        self.an("C04-2", "sobra a velocidade inicial")
        self.play(GrowArrow(ti), FadeIn(li), run_time=0.8)
        self.an("C04-2", "igual à soma vetorial")
        self.play(GrowArrow(t1), FadeIn(lt1), run_time=0.8)
        self.an("C04-2", "das duas velocidades finais")
        self.play(GrowArrow(t2), FadeIn(lt2), run_time=0.8)
        self.an("C04-2", "por enquanto")
        self.play(d.animate.set_value(1.9), run_time=0.9)
        self.play(d.animate.set_value(2.7), run_time=1.2)
        self.play(d.animate.set_value(2.35), run_time=0.9)
        # (2) energia: K_i = K_f → v₁ᵢ² = v₁f² + v₂f²
        K0 = Eq([("a", "K_i", CYAN), ("eq", "="), ("b", "K_f", CYAN)], 56, pos=P3(X0, Y0))
        En1 = Eq([("h1", r"\tfrac12 m"), ("a", "v_{1i}^2", VEL), ("eq", "="), ("h2", r"\tfrac12 m"), ("b", "v_{1f}^2", VEL), ("pl", "+"),
                  ("h3", r"\tfrac12 m"), ("c", "v_{2f}^2", VEL)], 48, w=9.6, pos=P3(X0, Y0))
        En2 = Eq([("a", "v_{1i}^2", VEL), ("eq", "="), ("b", "v_{1f}^2", VEL), ("pl", "+"), ("c", "v_{2f}^2", VEL)], 56, pos=P3(X0, Y0))
        n2 = VGroup(txt("ELÁSTICA:", 24, color=DIM), M(r"K_i=K_f", size=30)).arrange(RIGHT, buff=0.2).move_to(P3(X0, Y0 - 0.95))
        self.an("C04-3")
        self.play(FadeOut(n1), run_time=0.3)
        self.passo(pil, E1b, K0, extra=(FadeIn(n2),))
        # K = ½mv²: o K_i vira ½ m v₁ᵢ² (o K some no v, o índice i continua i); K_f vira a soma dos dois corpos (o f continua f)
        Ki, Kf = K0.idx["a"], K0.idx["b"]
        a_, b_, c_ = En1.idx["a"], En1.idx["b"], En1.idx["c"]
        self.an("C04-3", "o meio e a massa")
        self.avanca(K0, En1, (Ki[0], a_[0]), (Ki[1], a_[3]), (Kf[0], b_[0]), (Kf[1], b_[3]), (Kf[0], c_[0]), (Kf[1], c_[3]),
                    ([], "h1", {"delay": 0.7}), ([], "h2", {"delay": 0.7}), ([], "h3", {"delay": 0.7}), ([], "pl", {"delay": 0.7}),
                    ([], [a_[1], a_[2], b_[1], b_[2], c_[1], c_[2]], {"delay": 0.5}), rt=1.4, extra=(FadeOut(n2),))
        self.an("C04-3", "cancelam também")
        self.avanca(En1, En2, ("h1", [], sai), ("h2", [], sai), ("h3", [], sai), rt=1.1)
        self.an("C04-3", "guarda essa")
        self.play(Indicate(En2.m, color=VEL, scale_factor=1.05), run_time=1.0)
        # (3) o quadrado da relação vetorial: nasce do fantasma da relação vetorial; cada parcela do quadrado se abre no resultado
        n3 = txt("ELEVE AO QUADRADO A RELAÇÃO VETORIAL", 24, color=DIM).move_to(P3(X0, Y0 - 0.95))
        Sq = Eq([("p1", "("), ("a", r"\vec v_{1i}", VEL), ("p2", ")^2"), ("eq", "="), ("p3", "("), ("b", r"\vec v_{1f}", VEL), ("pl", "+"),
                 ("c", r"\vec v_{2f}", VEL), ("p4", ")^2")], 52, pos=P3(X0, Y0))
        Ex = Eq([("a", "v_{1i}^2", VEL), ("eq", "="), ("b", "v_{1f}^2", VEL), ("pl", "+"), ("c", "v_{2f}^2", VEL), ("pl2", "+"),
                 ("two", "2"), ("d", r"\vec v_{1f}", VEL), ("dot", r"\cdot"), ("e", r"\vec v_{2f}", VEL)], 52, w=9.8, pos=P3(X0, Y0))
        self.an("C04-4")
        self.recua_sai(pil, En2)
        self.nasce(Sq, [(pil.copia(E1b, nm), nm) for nm in ("a", "eq", "b", "pl", "c")], rt=1.5, extra=(FadeIn(n3, shift=0.1 * UP),))
        n3b = txt("O TERMO CRUZADO APARECE", 24, color=DIM).move_to(P3(X0, Y0 - 0.95))
        self.an("C04-4", "aparece um termo cruzado")
        self.play(FadeOut(n3), run_time=0.3)
        ea, eb, ec = Ex.idx["a"], Ex.idx["b"], Ex.idx["c"]
        sq2 = Sq.idx["p2"][1]                                       # o expoente 2 dos parênteses
        sq4 = Sq.idx["p4"][1]
        self.avanca(Sq, Ex,
                    ("a@b", [ea[0], ea[2], ea[3]]), ("a@s", [], sai), ("p1", [], sai), (Sq.idx["p2"][0], [], sai), (sq2, ea[1]),
                    ("b@b", [eb[0], eb[2], eb[3]]), ("b@b", "d@b"), ("b@s", "d@s"),
                    ("c@b", [ec[0], ec[2], ec[3]]), ("c@b", "e@b"), ("c@s", "e@s"),
                    ("p3", [], sai), (Sq.idx["p4"][0], [], sai), (sq4, [eb[1], ec[1]] + Ex.idx["two"]),
                    ([], "pl2", {"delay": 0.9}), ([], "dot", {"delay": 0.9}), rt=2.6, extra=(FadeIn(n3b, shift=0.1 * UP),), pil=pil)
        self.an("C04-4", "o produto escalar")
        self.play(Indicate(VGroup(Ex.parte("d"), Ex.parte("dot"), Ex.parte("e")), color=WHITE_, scale_factor=1.12), run_time=1.0)
        # (4) comparar com a energia: o que é igual se cancela; sobra 2 v⃗₁f·v⃗₂f = 0 (MF-Tools)
        self.an("C04-5")
        comum = VGroup(Ex.parte("a"), Ex.parte("eq"), Ex.parte("b"), Ex.parte("pl"), Ex.parte("c"))
        bx = SurroundingRectangle(VGroup(Ex.parte("a")), color=CYAN, buff=0.1, stroke_width=2.2, corner_radius=0.08)
        bx2 = SurroundingRectangle(VGroup(Ex.parte("b"), Ex.parte("pl"), Ex.parte("c")), color=CYAN, buff=0.1, stroke_width=2.2,
                                   corner_radius=0.08)
        gh_en = pil.fantasmas[1]
        self.play(Create(bx), Create(bx2), Indicate(gh_en, color=CYAN, scale_factor=1.05), run_time=1.4)
        self.an("C04-5", "então o termo cruzado")
        Z = Eq([("two", "2"), ("d", r"\vec v_{1f}", VEL), ("dot", r"\cdot"), ("e", r"\vec v_{2f}", VEL), ("eq", "="), ("z", "0")],
               56, pos=P3(X0, Y0))
        iE = Ex.idx
        sai_b = {"shift": 0.5 * DOWN, "scale": 0.5}
        self.avanca(Ex, Z, (iE["a"] + iE["pl"] + iE["b"] + iE["c"] + iE["pl2"], [], sai_b), ([], "z", {"delay": 0.8}), rt=2.2, pil=pil,
                    extra=(FadeOut(bx), FadeOut(bx2), FadeOut(n3b)))
        Pp = Eq([("d", r"\vec v_{1f}", VEL), ("perp", r"\perp"), ("e", r"\vec v_{2f}", VEL)], 60, pos=P3(X0, Y0))
        self.an("C04-6")
        self.play(Indicate(Z.m, color=WHITE_, scale_factor=1.06), run_time=0.9)
        # o ângulo no triângulo vira reto; os dois vetores da colisão ficam perpendiculares
        self.an("C04-6", "só acontece em noventa graus")
        self.add(aq)
        self.play(FadeIn(aq), run_time=0.3)
        self.play(d.animate.set_value(L * np.cos(np.radians(30))), run_time=2.0)
        rq = reto(Q(), O - Q(), T - Q(), s=0.3)
        self.remove(aq)
        aq.clear_updaters()
        self.add(rq)
        self.an("C04-6", "as duas velocidades finais são perpendiculares")
        self.avanca(Z, Pp, ("dot", "perp"), ("two", [], sai_b), ("eq", [], sai_b), ("z", [], sai_b), rt=1.8)
        cxp = dupla_caixa(Pp.m, buff=0.2)
        self.play(Create(cxp), run_time=0.7)
        raios = VGroup(DashedLine(oc, oc + e1 * 1.6, dash_length=0.1).set_stroke(DIM, 1.6, opacity=0.8),
                       DashedLine(oc, oc + e2 * 1.6, dash_length=0.1).set_stroke(DIM, 1.6, opacity=0.8),
                       reto(oc, e1, e2, s=0.3))
        self.an("C04-6", "é o famoso ângulo reto")
        self.play(Create(raios), run_time=0.9)
        # ressalva (frontal) e condições simultâneas
        res = VGroup(txt("NO CASO FRONTAL, UM DOS VETORES É NULO.", 24, op=0.9),
                     txt("NO DESVIO OBLÍQUO, NENHUM MÓDULO É NULO.", 24, color=CYAN)).arrange(DOWN, buff=0.12).move_to(P3(X0, -2.0))
        self.an("C04-7")
        self.play(FadeIn(res[0], shift=0.1 * UP), run_time=0.8)
        self.an("C04-7", "no desvio oblíquo")
        self.play(FadeIn(res[1], shift=0.1 * UP), Indicate(raios, color=WHITE_, scale_factor=1.05), run_time=0.8)
        chips = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.18, width=w_, height=0.55).set_stroke(CYAN, 1.6, 0.75)
                                .set_fill(WHITE_, 0.05), txt(s_, 24)) for s_, w_ in
                         (("ELÁSTICA", 2.2), ("MASSAS IGUAIS", 3.2), ("ALVO PARADO", 3.0))])
        for c_ in chips:
            c_[1].move_to(c_[0])
        chips.arrange(RIGHT, buff=0.22).move_to(P3(X0, -3.4))
        self.an("C04-8")
        self.play(FadeOut(hip), run_time=0.4)
        for c_, fr_ in zip(chips, ("elástica massas", "massas iguais", "alvo parado")):
            self.an("C04-8", fr_)
            self.play(FadeIn(c_, shift=0.1 * UP), run_time=0.45)
        self.an("C04-8", "faltou uma")
        self.play(Indicate(chips, color=CYAN, scale_factor=1.05), run_time=0.9)
        self.wait(0.5)
        for m_ in (t1, t2, lt1, lt2):
            m_.clear_updaters()
        self.clear(rt=0.7)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C05 — bilhar: aplicação do ângulo reto (L-CENA)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c05(self):
        self.secao("BILHAR")
        assert abs(10 * np.cos(np.radians(30)) - 5 * np.sqrt(3)) < 1e-12 and abs(10 * np.sin(np.radians(30)) - 5) < 1e-12
        mesa = placa(9.0, 5.0, P3(-2.9, -0.25))
        borda = RoundedRectangle(corner_radius=0.22, width=9.0, height=5.0).move_to(P3(-2.9, -0.25)).set_stroke(DIM, 2.8, opacity=0.8) \
            .set_fill(opacity=0).set_z_index(-1)
        r = 0.42
        n = pol(1.0, -60)
        C1c = P3(-4.9, 0.35)
        C2c = C1c + n * (2 * r)
        vi = 2.7
        v2f = vi * 0.5 * n
        v1f = P3(vi, 0) - v2f
        ch = Choque(C1c, C2c, P3(vi, 0), P3(0, 0), v1f, v2f, r, r, t0=-1.0, ka=0.5, wseta=5.0)
        eixo = DashedLine(P3(-7.2, C1c[1]), C1c, dash_length=0.14).set_stroke(DIM, 1.6, opacity=0.6).set_z_index(-1)
        # dados (coluna direita, em cima)
        card = VGroup(M(r"v_{1i}=10\ \mathrm{m/s}", size=44), txt("ELÁSTICA", 24, op=0.9)).arrange(RIGHT, buff=0.45).move_to(P3(4.6, 2.75))
        card2 = M(r"m_1=m_2,\ v_{2i}=0,\ \theta_1=30^\circ", size=38, w=5.6).move_to(P3(4.6, 1.95))
        ref = txt("EXERCÍCIO DE REFERÊNCIA", 22, color=DIM).move_to(P3(4.6, 3.3))
        self.an("C05-1")
        self.play(FadeIn(mesa), FadeIn(borda), Create(eixo), FadeIn(ch.group()), FadeIn(ref), run_time=1.0)
        self.an("C05-1", "uma bola a dez metros")
        self.play(FadeIn(card, shift=0.1 * UP), ch.t.animate.set_value(0.0), rate_func=linear, run_time=1.3)
        self.an("C05-1", "bate numa parada")
        self.play(ch.flash())
        ch.t.set_value(1e-5)
        self.an("C05-1", "de mesma massa")
        self.play(FadeIn(card2, shift=0.1 * UP), run_time=0.6)
        self.an("C05-1", "e desvia trinta graus")
        self.play(ch.t.animate.set_value(1.0), rate_func=rate_functions.ease_out_sine, run_time=1.5 * LENTO)
        ch.solta()
        # ângulos medidos a partir do eixo de incidência
        p1, p2 = ch.pos(1), ch.pos(2)
        tr1 = Line(C1c, p1).set_stroke(GEO, 2.0, opacity=0.5).set_z_index(-1)
        tr2 = Line(C2c, p2).set_stroke(GEO, 2.0, opacity=0.5).set_z_index(-1)
        ref1 = DashedLine(C1c, C1c + P3(2.6, 0), dash_length=0.12).set_stroke(DIM, 1.5, opacity=0.7).set_z_index(-1)
        ref2 = DashedLine(C2c, C2c + P3(2.0, 0), dash_length=0.12).set_stroke(DIM, 1.5, opacity=0.7).set_z_index(-1)
        a1 = arco(C1c, 1.3, 0, 30, w=2.0)
        a2 = arco(C2c, 0.95, -60, 0, w=2.0)
        t1 = M(r"\theta_1", size=34).move_to(C1c + pol(1.7, 15)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        t2 = M(r"\theta_2", size=34).move_to(C2c + pol(1.3, -30)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        self.play(Create(tr1), Create(tr2), Create(ref1), Create(ref2), run_time=0.7)
        self.an("C05-1", "para onde vai a segunda")
        self.play(Create(a1), FadeIn(t1), Create(a2), FadeIn(t2), run_time=0.9)
        # triângulo retângulo com hipotenusa v₁ᵢ = 10, grande, na coluna da direita
        K = 0.48
        O = P3(2.0, -2.55)
        Tt = O + P3(10 * K, 0)
        Qq = O + pol(5 * np.sqrt(3) * K, 30)
        hi = arrow(O, Tt, color=VEL, width=7, tip=0.26)
        h1 = arrow(O, Qq, color=VEL, width=5.5, tip=0.24)
        h2 = arrow(Qq, Tt, color=mix(VEL, 0.3), width=5.5, tip=0.24)
        li = lab_at(M(r"v_{1i}=10", size=34), O, Tt, lado=-1)
        l1 = lab_at(M(r"v_{1f}=5\sqrt3", size=34), O, Qq, lado=1)
        l2 = lab_at(M(r"v_{2f}=5", size=34), Qq, Tt, lado=1)
        rq = reto(Qq, O - Qq, Tt - Qq, s=0.3)
        ta = arco(O, 0.9, 0, 30, w=2.0)
        tb = arco(Tt, 0.8, 180 - 60, 180, w=2.0)
        tha = M(r"30^\circ", size=28).move_to(O + pol(1.5, 15)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        thb = M(r"60^\circ", size=28).move_to(Tt + pol(1.35, 180 - 30)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        self.an("C05-2")
        self.play(GrowArrow(h1), GrowArrow(h2), run_time=1.0)
        self.an("C05-2", "então o triângulo é retângulo")
        self.play(Create(rq), run_time=0.6)
        self.an("C05-2", "com a hipotenusa")
        self.play(GrowArrow(hi), FadeIn(li), run_time=0.8)
        # solução: uma linha de cada vez (faixa inferior sob a mesa)
        s1 = M(r"\theta_1+\theta_2=90^\circ\;\Rightarrow\;\theta_2=60^\circ", size=46, w=8.0).move_to(P3(-2.9, -3.45))
        s2 = Eq([("a", "v_{1f}", VEL), ("e1", "="), ("b", "v_{1i}", VEL), ("c", r"\cos30^\circ"), ("e2", "="), ("d", r"5\sqrt3"),
                 ("u", r"\ \mathrm{m/s}")], 46, w=8.0, pos=P3(-2.9, -3.45))
        s3 = Eq([("a", "v_{2f}", VEL), ("e1", "="), ("b", "v_{1i}", VEL), ("c", r"\sin30^\circ"), ("e2", "="), ("d", "5"),
                 ("u", r"\ \mathrm{m/s}")], 46, pos=P3(-2.9, -3.45))
        self.an("C05-2", "trinta e sessenta dão noventa")
        self.play(Create(ta), FadeIn(tha), Create(tb), FadeIn(thb), FadeIn(s1, shift=0.12 * UP), run_time=1.2)
        self.an("C05-2", "a segunda sai a sessenta")
        self.play(Indicate(VGroup(tb, thb), color=WHITE_, scale_factor=1.15), Indicate(t2, color=WHITE_, scale_factor=1.2), run_time=1.0)
        self.an("C05-3")
        self.play(FadeOut(s1), FadeIn(s2.mt, shift=0.12 * UP), FadeIn(l1), run_time=0.9)
        self.pulso(l1, WHITE_)
        # v₂f é o mesmo cálculo com o seno: o v₁f vira v₂f, o cos vira sin e o 5√3 perde a raiz e vira 5
        self.an("C05-3", "a segunda é o outro cateto")
        self.avanca(s2, s3, (("d", 0), ("d", 0)), (("d", slice(1, None)), [], {"shift": 0.4 * DOWN, "scale": 0.4}), rt=1.8, extra=(FadeIn(l2),))
        self.pulso(l2, WHITE_)
        self.an("C05-3", "pitágoras confere")
        self.play(Indicate(VGroup(hi, h1, h2), color=VEL, scale_factor=1.04), run_time=1.0)
        self.an("C05-3", "olha só")
        self.play(Indicate(VGroup(ch.d1, ch.d2), color=WHITE_, scale_factor=1.15), run_time=1.0)
        self.wait(0.5)
        self.clear(rt=0.7)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C06 — massas diferentes (L-EQUAÇÃO): a perpendicularidade não vale; sai a quadrática em p₁f, com λ = m₂/m₁
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c06(self):
        self.secao("MASSAS DIFERENTES")
        # aparato-âncora (coluna esquerda, ~25 %): o triângulo de momentos e a razão das massas
        chip = VGroup(Disco(C1F, 0.3, "m_1"), Disco(C2F, 0.22, "m_2"), M(r"m_1\neq m_2", size=40)).arrange(RIGHT, buff=0.3) \
            .move_to(P3(-5.2, 2.15))
        nao = VGroup(txt("A PERPENDICULARIDADE", 24, op=0.9), txt("NÃO VALE", 24, op=0.9)).arrange(DOWN, buff=0.1).move_to(P3(-5.2, 1.25))
        K = 0.9
        O = P3(-7.0, -0.55)
        tr = self.triangulo(O, K, size=34)
        th = arco(O, 0.8, 0, GTH1)
        tht = M(r"\theta_1", size=30).move_to(O + pol(1.2, GTH1 / 2 + 2)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        lam = VGroup(M(r"\lambda=\frac{m_2}{m_1}", size=48), txt("RAZÃO DAS MASSAS", 22, color=DIM)).arrange(DOWN, buff=0.15) \
            .move_to(P3(-5.2, -2.55))
        self.an("C06-1")
        self.play(FadeIn(chip, shift=0.15 * UP), FadeIn(nao, shift=0.15 * UP), run_time=0.9)
        self.an("C06-1", "mas o triângulo de momentos")
        self.play(GrowArrow(tr["pi"]), GrowArrow(tr["p1"]), GrowArrow(tr["p2"]), FadeIn(tr["li"]), FadeIn(tr["l1"]),
                  FadeIn(tr["l2"]), Create(th), FadeIn(tht), run_time=1.6)
        # coluna de equações: a atual em destaque, as anteriores recuam
        X0 = 2.5
        pil = Pilha(self, X0, (2.8, 1.9, 1.0), esc=0.66)
        self.pil06 = pil
        Y0 = -0.35
        r1 = Eq([("a", r"\vec p_{2f}", MAG), ("b", "="), ("c", r"\vec p_{1i}", MAG), ("d", "-"), ("e", r"\vec p_{1f}", MAG)],
                M_EQ, pos=P3(X0, Y0))
        r2 = Eq([("a", "p_{2f}^2", MAG), ("b", "="), ("c", "p_{1i}^2", MAG), ("d", "+"), ("e", "p_{1f}^2", MAG), ("f1", "-"), ("f2", "2"),
                 ("g", "p_{1i}", MAG), ("h", "p_{1f}", MAG), ("i", r"\cos\theta_1")], 46, w=9.2, pos=P3(X0, Y0))
        sai = {"shift": 0.5 * UP, "scale": 0.45}
        # r1 nasce dos rótulos do triângulo (cópias que viajam); r1 → r2: cada vetor vira o seu quadrado e o termo cruzado aparece
        self.an("C06-1", "dele sai que o momento final")
        self.nasce(r1, [(tr["l2"][0], "a"), (tr["li"][0], "c"), (tr["l1"][0], "e")], rt=1.6)
        n_lei = txt("LEI DOS COSSENOS NO TRIÂNGULO", 22, color=DIM).move_to(P3(X0, Y0 - 0.95))
        self.an("C06-2")
        self.play(Indicate(VGroup(tr["pi"], tr["p1"], tr["p2"]), color=MAG, scale_factor=1.04), run_time=1.0)
        ra, rc, re_ = r2.idx["a"], r2.idx["c"], r2.idx["e"]
        self.an("C06-2", "é um pitágoras com um ajuste")
        self.avanca(r1, r2, ("a@b", [ra[0], ra[2], ra[3]]), ("a@s", [], sai),
                    ("c@b", [rc[0], rc[2], rc[3]]), ("c@b", "g"), ("c@s", [], sai),
                    ("e@b", [re_[0], re_[2], re_[3]]), ("e@b", "h"), ("e@s", [], sai),
                    ("d", "f1"), ([], "d", {"delay": 0.9}), ([], "f2", {"delay": 0.9}), ([], "i", {"delay": 0.9}),
                    ([], [ra[1], rc[1], re_[1]], {"delay": 0.9}), rt=2.4, pil=pil, extra=(FadeIn(n_lei),))
        self.an("C06-2", "se o ângulo for reto")
        self.play(Indicate(VGroup(th, tht), color=WHITE_, scale_factor=1.15), run_time=1.0)
        # energia: elástica (K em ciano); os numeradores vêm dos termos recuados da lei dos cossenos
        r3 = Eq([("a", r"\frac{p_{1i}^2}{2m_1}", CYAN), ("b", "=", CYAN), ("c", r"\frac{p_{1f}^2}{2m_1}", CYAN), ("d", "+", CYAN),
                 ("e", r"\frac{p_{2f}^2}{2m_2}", CYAN)], 46, w=9.0, pos=P3(X0, Y0))
        n_el = VGroup(txt("ELÁSTICA:", 24, color=DIM), M("K_i", "=", "K_f", size=32)).arrange(RIGHT, buff=0.2).move_to(P3(X0, Y0 - 1.1))
        self.an("C06-3")
        self.play(FadeOut(n_lei), run_time=0.3)
        self.recua_sai(pil, r2)
        self.nasce(r3, [(pil.copia(r2, "c"), r3.num("a")), (pil.copia(r2, "e"), r3.num("c")), (pil.copia(r2, "a"), r3.num("e"))],
                   rt=1.7, extra=(FadeIn(n_el),))
        self.an("C06-3", "para não carregar duas massas")
        self.play(FadeIn(lam, shift=0.15 * UP), run_time=0.9)
        self.an("C06-3", "que na tela aparece como lambda")
        self.pulso(lam[0], WHITE_)
        r4 = Eq([("a", "p_{2f}^2", MAG), ("b", "="), ("c", r"\lambda"), ("d", "("), ("e", "p_{1i}^2", MAG), ("f", "-"),
                 ("g", "p_{1f}^2", MAG), ("h", ")")], M_EQ, pos=P3(X0, Y0))
        self.an("C06-3", "daqui para frente")
        self.play(FadeOut(n_el), run_time=0.3)
        # multiplica por 2m₂: o p₂f² isola, os p² trocam de lado e a razão das massas vira λ
        self.avanca(r3, r4, (r3.num("e"), "a"), (r3.num("a"), "e"), (r3.num("c"), "g"), ("b", "b"), ("d", "f"), (r3.den("e"), "c"),
                    rt=2.4, pil=pil)
        # igualar os dois p₂f²: os termos vêm das cópias recuadas (a lei dos cossenos e a energia)
        r5 = Eq([("a", "p_{1i}^2", MAG), ("b", "+"), ("c", "p_{1f}^2", MAG), ("d1", "-"), ("d2", "2"), ("e", "p_{1i}", MAG),
                 ("f", "p_{1f}", MAG), ("g", r"\cos\theta_1"), ("h", "="), ("i", r"\lambda"), ("j", "("), ("k", "p_{1i}^2", MAG),
                 ("l", "-"), ("m", "p_{1f}^2", MAG), ("n", ")")], 44, w=9.6, pos=P3(X0, Y0))
        self.an("C06-4")
        self.recua_sai(pil, r4)
        fts = [(pil.copia(r2, "c"), "a"), (pil.copia(r2, "d"), "b"), (pil.copia(r2, "e"), "c"), (pil.copia(r2, "f1"), "d1"),
               (pil.copia(r2, "f2"), "d2"), (pil.copia(r2, "g"), "e"), (pil.copia(r2, "h"), "f"), (pil.copia(r2, "i"), "g"),
               (pil.copia(r4, "c"), "i"), (pil.copia(r4, "d"), "j"), (pil.copia(r4, "e"), "k"), (pil.copia(r4, "f"), "l"),
               (pil.copia(r4, "g"), "m"), (pil.copia(r4, "h"), "n")]
        self.nasce(r5, fts, rt=2.0)
        self.an("C06-4", "sai uma equação do segundo grau")
        # a quadrática: tudo para a esquerda; o λ se reparte em (1+λ) e (1−λ); 1ª aparição de (1+λ)
        S0 = Eq([("lam1", r"(1+\lambda)"), ("pf2", "p_{1f}^2", MAG), ("m", "-"), ("dois", "2"), ("pi", "p_{1i}", MAG),
                 ("cos", r"\cos\theta_1"), ("pf", "p_{1f}", MAG), ("mais", "+"), ("lam2", r"(1-\lambda)"), ("pi2", "p_{1i}^2", MAG),
                 ("ig", "="), ("z", "0")], 50, w=9.6, pos=P3(X0, Y0 - 0.1))
        self.avanca(r5, S0, ("c", "pf2"), ("m", "pf2"), ("a", "pi2"), ("k", "pi2"), ("i", ("lam1", 3)), ("i", ("lam2", 3)),
                    ("d1", "m"), ("d2", "dois"), ("e", "pi"), ("g", "cos"), ("f", "pf"), ("b", "mais"), ("h", "ig"),
                    (["j", "l", "n"], [], sai), ([], "z", {"delay": 1.0}), rt=2.6, pil=pil)
        cx = dupla_caixa(S0.m)
        self.an("C06-4", "a gente não vai resolver")
        self.play(Create(cx), run_time=0.6)
        q = VGroup(txt("O QUE ESSA EQUAÇÃO DIZ, GEOMETRICAMENTE, SOBRE", 26), txt("TODOS OS MOMENTOS FINAIS POSSÍVEIS?", 26, color=CYAN)) \
            .arrange(DOWN, buff=0.1)
        q.scale_to_fit_width(min(q.width, 9.4)).move_to(P3(X0, -3.4))
        self.an("C06-4", "a gente vai perguntar")
        self.play(FadeIn(q, shift=0.12 * UP), run_time=0.8)
        self.wait(1.0)
        # fica para C07: a quadrática, sua caixa e a pergunta
        self.q06 = (S0, cx)
        self.pq = q
        self.clear(S0.m, cx, q, *pil.fantasmas, rt=0.7)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C07 — a quadrática é um círculo: álgebra em passos (L-EQUAÇÃO, MF-Tools) e troca de plano (L-PALCO)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c07(self):
        self.secao("A QUADRÁTICA É UM CÍRCULO")
        S0, cx = self.q06
        lam = LAM_EX
        C, R = lam_cr(lam)
        # conferência numérica da álgebra (desenvolvimento): o quadrado perfeito fecha em (λ p₁ᵢ/(1+λ))²
        for lm in (0.25, 0.5, 2.0):
            assert abs(1 / (1 + lm) ** 2 - (1 - lm) / (1 + lm) - lm ** 2 / (1 + lm) ** 2) < 1e-12
        X0, Y0 = 0.0, -0.5
        pil = Pilha(self, X0, (2.85, 1.75, 0.65), esc=0.6)
        self.pil07 = pil
        Wd = 13.6

        def nota(*partes, y=Y0 - 1.15):
            g = VGroup(*partes).arrange(RIGHT, buff=0.18) if len(partes) > 1 else partes[0]
            return g.move_to(P3(X0, y))

        # S1: forma vetorial (o produto escalar aparece)
        S1 = Eq([("lam1", r"(1+\lambda)"), ("pf2", "p_{1f}^2", MAG), ("m", "-"), ("dois", "2"), ("d", r"\vec p_{1i}", MAG),
                 ("e", r"\cdot"), ("f", r"\vec p_{1f}", MAG), ("mais", "+"), ("lam2", r"(1-\lambda)"), ("i", "p_{1i}^2", MAG),
                 ("ig", "="), ("z", "0")], 52, w=Wd, pos=P3(X0, Y0))
        S2 = Eq([("pf2", "p_{1f}^2", MAG), ("m", "-"), ("c", r"\frac{2}{1+\lambda}"), ("d", r"\vec p_{1i}", MAG), ("e", r"\cdot"),
                 ("f", r"\vec p_{1f}", MAG), ("mais", "+"), ("h", r"\frac{1-\lambda}{1+\lambda}"), ("i", "p_{1i}^2", MAG),
                 ("ig", "="), ("z", "0")], 52, w=Wd, pos=P3(X0, Y0))
        SQ = r"\left(\frac{p_{1i}}{1+\lambda}\right)^2"
        S3 = Eq([("pf2", "p_{1f}^2", MAG), ("m", "-"), ("c", r"\frac{2}{1+\lambda}"), ("d", r"\vec p_{1i}", MAG), ("e", r"\cdot"),
                 ("f", r"\vec p_{1f}", MAG), ("mais", "+"), ("sqL", SQ, "num"), ("ig", "="), ("sqR", SQ, "num"), ("m2", "-"),
                 ("h", r"\frac{1-\lambda}{1+\lambda}"), ("i", "p_{1i}^2", MAG)], 52, w=Wd, pos=P3(X0, Y0))
        S4 = Eq([("n1", r"\left|"), ("pf", r"\vec p_{1f}", MAG), ("m", "-"), ("fr", r"\frac{\vec p_{1i}}{1+\lambda}", "num"),
                 ("n2", r"\right|^2"), ("ig", "="), ("sqR", SQ, "num"), ("m2", "-"), ("h", r"\frac{1-\lambda}{1+\lambda}"),
                 ("i", "p_{1i}^2", MAG)], 52, w=Wd, pos=P3(X0, Y0))
        S5 = Eq([("n1", r"\left|"), ("pf", r"\vec p_{1f}", MAG), ("m", "-"), ("fr", r"\frac{\vec p_{1i}}{1+\lambda}", "num"),
                 ("n2", r"\right|^2"), ("ig", "="), ("sq5", r"\left(\frac{\lambda\,p_{1i}}{1+\lambda}\right)^2", "num1")], 56, pos=P3(X0, Y0))
        # passo 1: do quadrático com cosseno ao produto escalar (a quadrática de C06 cresce e ocupa o centro; p₁ᵢ p₁f cosθ₁ vira p⃗₁ᵢ·p⃗₁f)
        sai = {"shift": 0.5 * UP, "scale": 0.45}
        self.an("C07-1")
        self.play(FadeOut(cx), *self.pil06.limpa(), self.pq.animate.move_to(P3(0, -3.4)), run_time=0.8)
        n1 = nota(txt("O PRODUTO ESCALAR APARECE", 24, color=DIM))
        self.an("C07-1", "o produto dos tamanhos")
        self.avanca(S0, S1, ("pi", "d@b"), ("pf", "f@b"), ("cos", "e"), ("pi2", "i"), rt=2.4, extra=(FadeIn(n1, shift=0.1 * UP),))
        self.an("C07-1", "a gente reescreve na forma vetorial")
        self.play(Indicate(VGroup(S1.parte("d"), S1.parte("e"), S1.parte("f")), color=WHITE_, scale_factor=1.1), run_time=1.0)
        # passo 2: dividir por (1+λ) — o (1+λ) vai para baixo de cada termo (os parênteses ficam para trás)
        n2 = nota(txt("DIVIDA TUDO POR", 24, color=DIM), M(r"(1+\lambda)", size=30))
        self.an("C07-1", "depois divide tudo")
        self.play(FadeOut(n1), run_time=0.3)
        l1_, l2_ = S1.idx["lam1"], S1.idx["lam2"]
        self.avanca(S1, S2, ("dois", S2.num("c")), (l1_[1:4], S2.den("c")), (l1_[1:4], S2.den("h")), (l1_[0], [], sai),
                    (l1_[4], [], sai), (l2_[1:4], S2.num("h")), (l2_[0], [], sai), (l2_[4], [], sai),
                    rt=2.6, pil=pil, extra=(FadeIn(n2, shift=0.1 * UP),))
        # passo 3: completar o quadrado — o termo (p₁ᵢ/(1+λ))² nasce do termo central, é somado nos dois lados e (1−λ)/(1+λ) p₁ᵢ² atravessa a igualdade
        n3 = nota(txt("COMPLETE O QUADRADO: SOME O MESMO TERMO DOS DOIS LADOS", 24, color=DIM))
        self.an("C07-2")
        self.play(FadeOut(n2), FadeIn(n3, shift=0.1 * UP), run_time=0.5)
        self.an("C07-2", "um quadrado perfeito tem")
        self.play(Indicate(S2.parte("pf2"), color=WHITE_, scale_factor=1.15), run_time=0.9)
        self.an("C07-2", "menos duas vezes o primeiro")
        self.play(Indicate(VGroup(S2.parte("m"), S2.parte("c"), S2.parte("d"), S2.parte("e"), S2.parte("f")), color=WHITE_,
                           scale_factor=1.06), run_time=1.2)
        self.an("C07-2", "aqui o termo do meio")
        self.play(Indicate(VGroup(S2.parte("c"), S2.parte("d")), color=CYAN, scale_factor=1.12), run_time=1.0)
        self.an("C07-2", "falta só o quadrado dele")
        self.avanca(S2, S3, ("c", "c"), ("d", "d"), (["h", "i"], ["h", "i"], {"path_arc": -2.6, "run_time": 2.0}), ("z", []),
                    (["c", "d"], "sqL", {"run_time": 1.8}), (["c", "d"], "sqR", {"run_time": 1.8, "delay": 0.4}),
                    ([], "m2", {"delay": 1.0}), rt=3.0, pil=pil)
        # passo 4: agrupar o quadrado perfeito — o p⃗₁f e o p⃗₁ᵢ/(1+λ) do termo cruzado entram nas barras; o expoente 2 do p₁f² vira o expoente da barra
        n4 = nota(txt("AGRUPE O QUADRADO PERFEITO", 24, color=DIM))
        self.an("C07-3")
        self.play(FadeOut(n3), run_time=0.3)
        self.avanca(S3, S4, ("f", "pf"), (("pf2", 1), (("n2", 2))), ("d", S4.num("fr")), (S3.den("c"), S4.den("fr")),
                    (S3.barra("c"), S4.barra("fr")), ("sqL", S4.idx["n2"][:2]), ([], "n1", {"delay": 0.8}),
                    rt=2.8, pil=pil, extra=(FadeIn(n4, shift=0.1 * UP),))
        # passo 5: o lado direito se simplifica; conferência em tamanho menor
        conf = M(r"\frac{1}{(1+\lambda)^2}-\frac{1-\lambda}{1+\lambda}=\frac{\lambda^2}{(1+\lambda)^2}", size=30, w=9.0) \
            .move_to(P3(X0, Y0 - 1.8))
        n5 = nota(txt("CONFERÊNCIA DO LADO DIREITO", 22, color=DIM), y=Y0 - 1.1)
        self.an("C07-3", "e o lado direito")
        self.play(FadeOut(n4), run_time=0.3)
        self.avanca(S4, S5, (["sqR", "m2", "h", "i"], "sq5", {"run_time": 2.0}), rt=2.4, pil=pil,
                    extra=(FadeIn(n5, shift=0.1 * UP), FadeIn(conf, shift=0.1 * UP)))
        self.an("C07-3", "fica o quadrado")
        bx5 = dupla_caixa(S5.m, buff=0.2)
        self.play(Create(bx5), run_time=0.7)
        # ── troca de plano: a álgebra sai do centro e vira |p⃗₁f − C⃗| = R (os termos viajam para a coluna da direita);
        #    o plano de p₁f entra (L-PALCO) ───────────────────────────────────────────────────────────────────────
        pl = Plano(P3(-6.9, -0.6), 9.2)
        self.pl07 = pl
        painel = pl.base(-0.05, 1.06, -0.36, 0.38)
        tagp = self.tag_plano(False).move_to(pl.pt(0.2, -0.36) + P3(0, 0.38))
        T = pl.pt(1, 0)
        p1i = arrow(pl.O, T, color=MAG, width=8, tip=0.26, z=6)
        lpi = lab_at(M(r"\vec p_{1i}", size=34), pl.O, T, lado=-1)
        ctr = pl.pt(C, 0)
        circ = Circle(radius=R * pl.u).move_to(ctr).set_stroke(CYAN, 3.8).set_fill(CYAN, 0.12).set_z_index(3)
        halo = halo_circ(ctr, R * pl.u)
        vig = vinheta(ctr, 2.8, CYAN)
        dc = ponto(ctr, GEO, 0.09, z=8)
        lc = M(r"C", size=32, color=GEO).next_to(dc, DOWN, buff=0.14).set_stroke(BACKGROUND_COLOR, 5, background=True)
        rad = Line(ctr, ctr + P3(0, R * pl.u)).set_stroke(GEO, 2.4).set_z_index(4)
        lr = M(r"R", size=32, color=GEO).next_to(rad, LEFT, buff=0.1).set_stroke(BACKGROUND_COLOR, 5, background=True)
        XR = 5.25
        eqc_ = Eq([("n1", r"\left|"), ("pf", r"\vec p_{1f}", MAG), ("m", "-"), ("c", r"\vec C", GEO), ("n2", r"\right|"), ("e", "="),
                   ("r", "R", GEO)], 48, w=4.2, pos=P3(XR, 2.0))
        eqC_ = Eq([("c", r"\vec C", GEO), ("e", "="), ("f", r"\frac{\vec p_{1i}}{1+\lambda}", "num")], 44, w=4.0)
        eqR_ = Eq([("r", "R", GEO), ("e", "="), ("f", r"\frac{\lambda\,p_{1i}}{1+\lambda}", "num1")], 44, w=4.0)
        VGroup(eqC_.mt, eqR_.mt).arrange(DOWN, buff=0.45).move_to(P3(XR, 0.2))
        EJ = EqJ(c=eqc_, C=eqC_, R=eqR_)
        s5n2, s5q = S5.idx["n2"], S5.idx["sq5"]
        assert len(s5q) == 11, len(s5q)
        self.an("C07-4")
        self.play(*self.pil07.limpa(), FadeOut(bx5), FadeOut(conf), FadeOut(n5), FadeOut(self.pq), run_time=0.8)
        self.avanca(S5, EJ, ("n1", "c.n1"), ("pf", "c.pf"), ("m", "c.m"), ("fr", "C.f"), (s5n2[:-1], "c.n2"),
                    (s5n2[-1], [], {"shift": 0.4 * DOWN, "scale": 0.4}), ("ig", "c.e"), (s5q[1:9], "R.f"),
                    ([s5q[0], s5q[9], s5q[10]], [], {"shift": 0.4 * DOWN, "scale": 0.4}),
                    ([], "c.c", {"delay": 1.2}), ([], "c.r", {"delay": 1.2}), ([], "C.c", {"delay": 1.2}), ([], "C.e", {"delay": 1.2}),
                    ([], "R.r", {"delay": 1.2}), ([], "R.e", {"delay": 1.2}), rt=2.6)
        self.an("C07-4", "uma distância constante")
        self.play(Indicate(EJ.parte("c.e"), color=WHITE_, scale_factor=1.3), Indicate(EJ.parte("C.f"), color=WHITE_, scale_factor=1.06), run_time=1.0)
        self.an("C07-4", "o vetor fixo é o centro")
        self.play(Indicate(VGroup(EJ.parte("C.c"), EJ.parte("C.e"), EJ.parte("C.f")), color=GEO, scale_factor=1.08), run_time=0.9)
        self.an("C07-4", "e o número fixo é o raio")
        self.play(Indicate(VGroup(EJ.parte("R.r"), EJ.parte("R.e"), EJ.parte("R.f")), color=GEO, scale_factor=1.08), run_time=0.9)
        self.an("C07-5")
        self.play(FadeIn(painel, scale=0.97), FadeIn(tagp), run_time=1.0)
        self.an("C07-5", "o eixo horizontal é a parte")
        self.play(GrowArrow(p1i), FadeIn(lpi), Indicate(painel[3], color=WHITE_, scale_factor=1.02), run_time=1.0)
        self.an("C07-5", "o vertical a perpendicular")
        self.play(Indicate(painel[4], color=WHITE_, scale_factor=1.05), run_time=0.8)
        self.an("C07-5", "o centro fica")
        self.play(FadeIn(dc), FadeIn(lc), run_time=0.8)
        self.an("C07-5", "o raio")
        self.play(FadeIn(vig), Create(circ), FadeIn(halo), Create(rad), FadeIn(lr), run_time=1.8)
        # cada ponto do círculo é um p₁f possível; p₂f fecha o triângulo (o desfecho do hook é um desses pontos)
        ph = ValueTracker(float(np.degrees(np.arctan2(_PH0[1], _PH0[0] - C))))
        ph0 = ph.get_value()

        def vet():
            a = np.radians(ph.get_value())
            P = pl.pt(C + R * np.cos(a), R * np.sin(a))
            return VGroup(arrow(pl.O, P, color=MAG, width=6, tip=0.22, z=7), arrow(P, T, color=MAG_L, width=6, tip=0.22, z=7),
                          ponto(P, WHITE_, 0.1, z=9))

        def pos_a(m, k):
            a = np.radians(ph.get_value())
            P = pl.pt(C + R * np.cos(a), R * np.sin(a))
            lab_at(m, pl.O, P, lado=1) if k == 1 else lab_at(m, P, T, lado=1)
        v = always_redraw(vet)
        l1 = M(r"\vec p_{1f}", size=32).add_updater(lambda m: pos_a(m, 1))
        l2 = M(r"\vec p_{2f}", size=32).add_updater(lambda m: pos_a(m, 2))
        t1 = VGroup(txt("CADA PONTO É UM", 24), M(r"\vec p_{1f}", size=34), txt("POSSÍVEL", 24)).arrange(RIGHT, buff=0.14)
        t1.scale_to_fit_width(min(t1.width, 4.4)).move_to(P3(XR, -2.1))
        self.an("C07-6")
        self.play(FadeIn(v), FadeIn(l1), FadeIn(l2), FadeIn(t1, shift=0.1 * UP), run_time=1.0)
        self.play(ph.animate.set_value(ph0 + 55), run_time=2.4)
        t2 = VGroup(txt("UM PONTO DÁ", 24), M(r"\vec p_{1f}", size=34), txt("E", 24), M(r"\vec p_{2f}", size=34)).arrange(RIGHT, buff=0.14)
        t2.scale_to_fit_width(min(t2.width, 4.4)).move_to(P3(XR, -3.0))
        self.an("C07-6", "e para cada ponto")
        self.play(FadeIn(t2, shift=0.1 * UP), ph.animate.set_value(ph0 - 70), run_time=3.0)
        self.an("C07-6", "um ponto só entrega")
        self.play(ph.animate.set_value(ph0), run_time=2.0)
        self.wait(0.5)
        for m_ in (l1, l2):
            m_.clear_updaters()
        v.clear_updaters()
        self.dir07 = VGroup(EJ.m, t1, t2)
        self.vec07 = VGroup(v, l1, l2)
        self.base07 = VGroup(painel, tagp, p1i, lpi, circ, dc, lc, rad, lr, halo, vig)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C08 — o círculo une 1D, 2D e o ângulo máximo; fecha o hook (L-PALCO)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c08(self):
        self.secao("DIREÇÕES POSSÍVEIS")
        pl, lam = self.pl07, LAM_EX
        C, R = lam_cr(lam)
        XR = 5.2
        self.an("C08-1")
        # ── (a) 1D, sem recap: o eixo corta o círculo em A e B ─────────────────────────────────────────────────
        A, B = pl.pt(1, 0), pl.pt((1 - lam) / (1 + lam), 0)
        dA, dB = ponto(A, WHITE_, 0.11, z=9), ponto(B, WHITE_, 0.11, z=9)
        lA = M("A", size=36).move_to(A + P3(0.05, 0.42)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        lB = M("B", size=36).move_to(B + P3(-0.38, 0.38)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        gA = VGroup(VGroup(M("A", size=40), M(r"p_{1f}=p_{1i}", size=44)).arrange(RIGHT, buff=0.35),
                    txt("NADA MUDOU", 24, op=0.9)).arrange(DOWN, buff=0.15).move_to(P3(XR, 1.7))
        gB = VGroup(VGroup(M("B", size=40), M(r"p_{1f}=\frac{m_1-m_2}{m_1+m_2}\,p_{1i}", size=40, w=3.5)).arrange(RIGHT, buff=0.3),
                    txt("COLISÃO FRONTAL EM 1D", 24, op=0.9)).arrange(DOWN, buff=0.18).move_to(P3(XR, -0.3))
        eixo = Line(pl.pt(0, 0), A).set_stroke(WHITE_, 3.5, opacity=0.9).set_z_index(5)
        self.play(FadeOut(self.dir07), FadeOut(self.vec07), Create(eixo), run_time=0.9)
        self.remove(self.dir07, self.vec07)
        self.an("C08-1", "no primeiro")
        self.play(FadeIn(dA), FadeIn(lA), FadeIn(gA, shift=0.15 * UP),
                  Flash(A, color=WHITE_, line_length=0.22, flash_radius=0.18, num_lines=8, run_time=0.6), run_time=0.9)
        self.an("C08-1", "no segundo")
        self.play(FadeIn(dB), FadeIn(lB), FadeIn(gB, shift=0.15 * UP),
                  Flash(B, color=WHITE_, line_length=0.22, flash_radius=0.18, num_lines=8, run_time=0.6), run_time=0.9)
        self.an("C08-1", "o caso de uma dimensão")
        self.play(Indicate(VGroup(dA, dB), color=WHITE_, scale_factor=1.6), run_time=1.0)
        self.an("C08-2")
        self.play(*[FadeOut(m) for m in (gA, gB, eixo, dA, dB, lA, lB)], run_time=0.7)
        # ── (b) direções oblíquas: semirreta saindo da origem ───────────────────────────────────────────────────
        th = ValueTracker(5.0)
        thm = float(np.degrees(np.arcsin(lam)))

        def raio_len(t):
            sn = np.sin(np.radians(t))
            return min(8.6, (2.55 - pl.O[1]) / sn) if sn > 1e-6 else 8.6

        def geo():
            t = th.get_value()
            a = np.radians(t)
            g = VGroup(DashedLine(pl.O, pl.O + pol(raio_len(t), t), dash_length=0.16).set_stroke(GEO, 2.4, opacity=0.85).set_z_index(5),
                       arco(pl.O, 1.5, 0, t, w=2.0).set_z_index(5))
            s_ = R * R - (C * np.sin(a)) ** 2
            if s_ > -1e-9:
                q = np.sqrt(max(s_, 0.0))
                dp, dm = C * np.cos(a) + q, C * np.cos(a) - q
                Pp, Pm = pl.O + pol(dp * pl.u, t), pl.O + pol(dm * pl.u, t)
                if q > 2e-3:
                    g.add(arrow(pl.O, Pp, color=MAG_L, width=4.5, tip=0.2, z=7), arrow(pl.O, Pm, color=MAG, width=7, tip=0.22, z=8),
                          ponto(Pp, WHITE_, 0.11, z=9), ponto(Pm, WHITE_, 0.11, z=9))
                else:
                    g.add(arrow(pl.O, Pp, color=MAG, width=7, tip=0.22, z=8), ponto(Pp, WHITE_, 0.13, z=9),
                          Circle(radius=0.26).move_to(Pp).set_stroke(CYAN, 2.5, 0.9).set_z_index(9))
            return g
        gg = always_redraw(geo)
        lth = M(r"\theta_1", size=32).add_updater(lambda m: m.move_to(pl.O + pol(2.0, th.get_value() + 7))
                                                  .set_stroke(BACKGROUND_COLOR, 5, background=True))
        rd = VGroup(M(r"\theta_1=", size=44), DecimalPT(5.0, num_decimal_places=1, unit=r"^\circ", font_size=44)).arrange(RIGHT, buff=0.15) \
            .move_to(P3(XR, 2.55))
        rd[1].add_updater(lambda m: m.set_value(th.get_value()))
        rd[1].add_updater(lambda m: m.next_to(rd[0], RIGHT, buff=0.15))

        def reg(s1, s2, cor=WHITE_):
            g = VGroup(txt(s1, 26, color=cor), txt(s2, 26, color=cor)).arrange(DOWN, buff=0.12)
            return g.scale_to_fit_width(min(g.width, 4.3)).move_to(P3(XR, 0.9))
        r2 = reg("DOIS JEITOS DE BATER,", "O MESMO DESVIO")
        r1 = reg("TANGÊNCIA: AS DUAS", "SOLUÇÕES SE FUNDEM", CYAN)
        r0 = reg("SEM INTERSEÇÃO:", "SEM SOLUÇÃO FÍSICA")
        r2.add_updater(lambda m: m.set_opacity(1.0 if th.get_value() < thm - 0.05 else 0.0))
        r1.add_updater(lambda m: m.set_opacity(1.0 if abs(th.get_value() - thm) <= 0.05 else 0.0))
        r0.add_updater(lambda m: m.set_opacity(1.0 if th.get_value() > thm + 0.05 else 0.0))
        self.add(r2, r1, r0)
        self.play(FadeIn(gg), FadeIn(lth), FadeIn(rd), run_time=1.0)
        self.an("C08-2", "onde ela corta o círculo")
        self.play(th.animate.set_value(10.0), run_time=2.2)
        self.an("C08-2", "dois jeitos de bater")
        self.play(th.animate.set_value(7.0), run_time=1.5)
        self.an("C08-2", "um tira bastante momento")
        self.play(th.animate.set_value(10.0), run_time=1.2)
        self.an("C08-2", "o outro é de raspão")
        self.play(Indicate(gg, color=WHITE_, scale_factor=1.02), run_time=0.9)
        self.an("C08-3")
        self.play(th.animate.set_value(thm - 0.6), run_time=3.0)
        self.an("C08-3", "até virar um só")
        self.play(th.animate.set_value(thm), run_time=1.4)
        self.an("C08-3", "a tangência")
        self.play(Indicate(gg, color=WHITE_, scale_factor=1.03), run_time=0.9)
        self.an("C08-3", "passou disso")
        self.play(th.animate.set_value(20.0), run_time=2.0)
        self.an("C08-3", "a natureza fechou a porta")
        self.play(Indicate(gg, color=WHITE_, scale_factor=1.0), run_time=0.6)
        for m_ in (gg, lth, rd[1], r2, r1, r0):
            m_.clear_updaters()
        self.play(*[FadeOut(m) for m in (gg, lth, rd, r2, r1, r0)], run_time=0.7)
        self.remove(gg, lth, rd, r2, r1, r0)
        # ── (c) fecha o hook: a direção de 40° não toca o círculo ───────────────────────────────────────────────
        Lt = np.sqrt(C * C - R * R) * pl.u
        Lw = (C + R) * pl.u
        cone = Sector(radius=Lw, angle=np.radians(2 * thm), start_angle=-np.radians(thm), arc_center=pl.O) \
            .set_fill(CYAN, 0.10).set_stroke(width=0).set_z_index(1)
        tang = VGroup(Line(pl.O, pl.O + pol(Lw, thm)).set_stroke(WHITE_, 2, opacity=0.85),
                      Line(pl.O, pl.O + pol(Lw, -thm)).set_stroke(WHITE_, 1.5, opacity=0.5)).set_z_index(5)
        angs = (HK_TH1,) + HOOK_CAND
        fan = VGroup()
        for k, a in enumerate(angs):
            L_ = raio_len(a) * 0.97
            ln = Line(pl.O, pl.O + pol(L_, a)) if k == 0 else DashedLine(pl.O, pl.O + pol(L_, a), dash_length=0.18)
            fan.add(ln.set_stroke(GEO, 2.6, opacity=0.95).set_z_index(6))
        dreal = ponto(pl.O + pol(_d_mais(lam, HK_TH1) * pl.u, HK_TH1), WHITE_, 0.12, z=9)

        def xis(p, s=0.16):
            return VGroup(Line(p + P3(-s, -s), p + P3(s, s)), Line(p + P3(-s, s), p + P3(s, -s))).set_stroke(WHITE_, 2.2, opacity=0.95).set_z_index(9)
        fim40 = pl.O + pol(raio_len(40) * 0.97, 40)
        x40 = xis(fim40)
        x25 = xis(pl.O + pol(raio_len(25) * 0.97, 25))
        l25 = M(r"25^\circ", size=30).move_to(pl.O + pol(raio_len(25) * 0.97 + 0.5, 25)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        l40 = M(r"40^\circ", size=30).move_to(fim40 + P3(0.1, 0.5)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        # a mesma situação do hook, no espaço físico (≥ 25 % da altura)
        mini0 = P3(4.0, -1.55)
        mini = VGroup(Line(mini0, mini0 + pol(3.0, HK_TH1)).set_stroke(GEO, 2.6, opacity=0.95),
                      *[DashedLine(mini0, mini0 + pol(3.0, a), dash_length=0.16).set_stroke(VEL, 3.2, opacity=0.9) for a in HOOK_CAND],
                      xis(mini0 + pol(3.0, 40)), xis(mini0 + pol(3.0, 25)), arrow(mini0 + P3(-0.9, 0), mini0 + P3(-0.1, 0), color=VEL, width=4.5, tip=0.2),
                      ponto(mini0, WHITE_, 0.09))
        tmini = txt("ESPAÇO FÍSICO", 24, color=DIM, op=0.9).move_to(P3(XR, 1.15))
        self.an("C08-4")
        self.play(FadeIn(tmini), FadeIn(mini), run_time=0.9)
        self.an("C08-4", "as duas tangentes formam")
        self.play(FadeIn(cone), Create(tang), self.base07[1].animate.move_to(P3(1.7, 2.55)), run_time=1.2)
        self.an("C08-4", "a colisão real")
        self.play(Create(fan[0]), FadeIn(dreal), run_time=0.9)
        self.an("C08-4", "vinte e cinco graus")
        self.play(Create(fan[1]), FadeIn(l25), FadeIn(x25), run_time=0.9)
        self.an("C08-4", "e quarenta graus")
        self.play(Create(fan[2]), FadeIn(l40), FadeIn(x40), run_time=0.9)
        self.an("C08-4", "o segurança da porta")
        self.play(Indicate(VGroup(x25, x40), color=WHITE_, scale_factor=1.35), run_time=0.9)
        fim = txt("AGORA SABEMOS POR QUÊ.", 32, color=CYAN, bold=True).move_to(pl.pt(0.5, -0.31))
        self.an("C08-5")
        self.play(FadeIn(fim, shift=0.1 * UP), run_time=0.8)
        self.play(Indicate(fan[2], color=WHITE_, scale_factor=1.0), Indicate(l40, color=WHITE_), run_time=1.2)
        self.wait(0.8)
        self.clear(rt=0.8)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C09 — a tangência dá o ângulo máximo; tracker em λ (λ<1, λ=1, λ>1) (L-PALCO)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c09(self):
        self.secao("O ÂNGULO MÁXIMO")
        lam = ValueTracker(0.5)
        ph = ValueTracker(110.0)                    # posição de P sobre o círculo (graus, a partir do centro)
        pv = ValueTracker(0.0)                      # visibilidade de P e dos vetores p₁f, p₂f
        pl = Plano(P3(-4.5, -0.4), 4.8)
        base = pl.base(-0.48, 1.18, -0.69, 0.62, ly_lado=LEFT)
        T = pl.pt(1, 0)
        p1i = arrow(pl.O, T, color=MAG, width=7, tip=0.24, z=6)
        lpi = M(r"\vec p_{1i}", size=32).move_to(pl.pt(0.84, 0) + P3(0, -0.45)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        tagp = self.tag_plano(False).move_to(pl.pt(-0.48, -0.69) + P3(1.25, 0.3))

        def dyn():
            l_ = lam.get_value()
            C, R = lam_cr(l_)
            ctr = pl.pt(C, 0)
            g = VGroup(Circle(radius=R * pl.u).move_to(ctr).set_stroke(CYAN, 3.8).set_fill(CYAN, 0.12).set_z_index(3),
                       halo_circ(ctr, R * pl.u), ponto(ctr, GEO, 0.09, z=8))
            if l_ < 0.985:                                          # origem fora do círculo: tangentes e setor permitido
                thm = np.arcsin(l_)
                tp = pl.O + pol(np.sqrt(C * C - R * R) * pl.u, np.degrees(thm))
                Lw = min((C + R) * pl.u, 3.0 / max(np.sin(thm), 1e-6))          # não sai do painel
                g.add(Sector(radius=Lw, angle=2 * thm, start_angle=-thm, arc_center=pl.O)
                      .set_fill(CYAN, 0.10).set_stroke(width=0).set_z_index(1),
                      Line(pl.O, pl.O + pol(Lw, np.degrees(thm))).set_stroke(WHITE_, 2.2, opacity=0.9).set_z_index(5),
                      Line(pl.O, pl.O + pol(Lw, -np.degrees(thm))).set_stroke(WHITE_, 1.5, opacity=0.5).set_z_index(5),
                      Line(ctr, tp).set_stroke(GEO, 2.4).set_z_index(5),
                      reto(tp, pl.O - tp, ctr - tp, s=0.2).set_z_index(6),
                      arco(pl.O, 0.9, 0, np.degrees(thm), w=2.0).set_z_index(6),
                      M(r"R", size=30, color=GEO).move_to((ctr + tp) / 2 + P3(0.3, 0.1)).set_stroke(BACKGROUND_COLOR, 5, background=True),
                      M(r"C", size=30, color=GEO).move_to(pl.pt(C / 2, 0) + P3(0, -0.34)).set_stroke(BACKGROUND_COLOR, 5, background=True))
                if l_ < 0.9:
                    g.add(M(r"\theta_{\max}", size=30).move_to(pl.O + pol(1.55, np.degrees(thm) + 9))
                          .set_stroke(BACKGROUND_COLOR, 5, background=True))
            v_ = pv.get_value()
            if v_ > 0.01:
                a = np.radians(ph.get_value())
                P = pl.pt(C + R * np.cos(a), R * np.sin(a))
                vs = VGroup(arrow(pl.O, P, color=MAG, width=6, tip=0.22, z=7), arrow(P, T, color=MAG_L, width=6, tip=0.22, z=7),
                            ponto(P, WHITE_, 0.11, z=9))
                if abs(l_ - 1.0) < 0.012:
                    vs.add(reto(P, pl.O - P, T - P, s=0.24).set_z_index(9))
                g.add(vs.set_opacity(v_))
            return g
        din = always_redraw(dyn)

        def pos_l(m, k):
            l_ = lam.get_value()
            C, R = lam_cr(l_)
            a = np.radians(ph.get_value())
            P = pl.pt(C + R * np.cos(a), R * np.sin(a))
            lab_at(m, pl.O, P, lado=1) if k == 1 else lab_at(m, P, T, lado=1)
            curto = k == 1 and np.linalg.norm(P - pl.O) < 0.45          # p₁f = 0: sem vetor, sem rótulo
            m.set_opacity(0.0 if curto else pv.get_value())
        l1 = M(r"\vec p_{1f}", size=32).add_updater(lambda m: pos_l(m, 1))
        l2 = M(r"\vec p_{2f}", size=32).add_updater(lambda m: pos_l(m, 2))
        # deslizador de λ e leituras (coluna direita)
        XR0, XR1 = 2.6, 7.0
        fx = lambda lv: XR0 + (lv - 0.25) / 1.75 * (XR1 - XR0)          # noqa: E731
        trilho = Line(P3(XR0, 2.5), P3(XR1, 2.5)).set_stroke(DIM, 3, opacity=0.7)
        enche = always_redraw(lambda: Line(P3(XR0, 2.5), P3(fx(lam.get_value()), 2.5)).set_stroke(CYAN, 4.5))
        marcas = VGroup(*[VGroup(Line(P3(fx(v_), 2.38), P3(fx(v_), 2.62)).set_stroke(DIM, 2.4),
                                 M(t_, size=28).move_to(P3(fx(v_), 2.05))) for v_, t_ in ((0.25, r"\tfrac14"), (1.0, "1"), (2.0, "2"))])
        botao = always_redraw(lambda: VGroup(Circle(radius=0.2).move_to(P3(fx(lam.get_value()), 2.5)).set_stroke(WHITE_, 2.5)
                                             .set_fill(BACKGROUND_COLOR, 1.0),
                                             Dot(P3(fx(lam.get_value()), 2.5), radius=0.08, color=CYAN)).set_z_index(10))
        lbl_l = M(r"\lambda", size=40).move_to(P3(XR0 - 0.55, 2.5))

        def linha(rot, f, n=2, un=None):
            d = DecimalPT(f(), num_decimal_places=n, font_size=44, **({"unit": un} if un else {}))
            d.add_updater(lambda m: m.set_value(f()))
            d.add_updater(lambda m: m.next_to(rot, RIGHT, buff=0.2))
            return VGroup(rot, d)
        thf = lambda: float(np.degrees(np.arcsin(min(lam.get_value(), 1.0))) if lam.get_value() <= 1.0 else 180.0)   # noqa: E731
        rl = linha(M(r"\lambda=", size=44), lambda: lam.get_value())
        rt = linha(M(r"\theta_{\max}=", size=44), thf, 1, r"^\circ")
        leitura = VGroup(rl, rt).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(P3(4.2, 1.1))
        for g_ in leitura:
            g_[1].next_to(g_[0], RIGHT, buff=0.2)
        self.an("C09-1")
        self.play(FadeIn(base), FadeIn(tagp), GrowArrow(p1i), FadeIn(lpi), run_time=1.4)
        self.add(l1, l2)
        self.an("C09-1", "qual é o maior desvio")
        self.play(Create(trilho), FadeIn(enche), FadeIn(marcas), FadeIn(botao), FadeIn(lbl_l), FadeIn(leitura, shift=0.1 * UP), run_time=1.0)
        self.an("C09-1", "olha a tangente")
        self.play(FadeIn(din), run_time=1.2)
        # destaques da geometria do triângulo retângulo da tangente (λ = 0,5): raio, hipotenusa e ângulo máximo
        C0_, R0_ = lam_cr(0.5)
        ctr0 = pl.pt(C0_, 0)
        tp0 = pl.O + pol(np.sqrt(C0_ ** 2 - R0_ ** 2) * pl.u, 30.0)
        rad_hl = Line(ctr0, tp0).set_stroke(WHITE_, 8).set_z_index(12)
        hyp_hl = Line(pl.O, ctr0).set_stroke(WHITE_, 8).set_z_index(12)
        arc_hl = arco(pl.O, 0.9, 0, 30, w=8).set_z_index(12)
        self.an("C09-1", "o raio até o ponto")
        self.play(ShowPassingFlash(rad_hl, time_width=0.9), run_time=1.2)
        self.an("C09-1", "a hipotenusa vai")
        self.play(ShowPassingFlash(hyp_hl, time_width=0.9), run_time=1.2)
        self.an("C09-1", "o cateto oposto é o raio")
        self.play(ShowPassingFlash(rad_hl, time_width=0.9), run_time=1.2)
        self.an("C09-1", "o ângulo na origem")
        self.play(ShowPassingFlash(arc_hl, time_width=0.9), run_time=1.2)
        XC = 4.7
        # ── λ < 1: a origem fica fora do círculo; a tangente fixa o ângulo máximo ───────────────────────────────
        A1 = Eq([("s", r"\sin"), ("t", r"\theta_{\max}"), ("e1", "="), ("rc", r"\frac{R}{C}"), ("e2", "="), ("lam", r"\lambda")],
                44, w=5.2, pos=P3(XC, -0.45))
        A2 = Eq([("t", r"\theta_{\max}"), ("e", "="), ("s", r"\arcsin"), ("fr", r"\frac{m_2}{m_1}")], 50, w=5.0, pos=P3(XC, -1.7))
        ba2 = dupla_caixa(A2.mt)
        a3 = VGroup(txt("TRADUÇÃO ALGÉBRICA", 22, color=DIM),
                    M(r"\Delta\ge0\;\Leftrightarrow\;\cos^2\theta\ge1-\lambda^2", size=32, w=5.2),
                    M(r"\Leftrightarrow\;\sin\theta\le\lambda", size=32)).arrange(DOWN, buff=0.12).move_to(P3(XC, -3.3))
        self.an("C09-2")
        self.play(FadeIn(A1.mt, shift=0.15 * UP), run_time=1.2)
        self.an("C09-2", "o raio sobre a distância")
        self.play(Indicate(A1.parte("rc"), color=WHITE_, scale_factor=1.2), run_time=1.0)
        self.an("C09-2", "substituindo")
        self.play(Indicate(A1.parte("lam"), color=CYAN, scale_factor=1.3), run_time=1.0)
        # o θ_max e o λ de cima viajam (cópias) até a nova linha; o λ se desdobra em m₂/m₁
        self.an("C09-2", "então o ângulo máximo é o arco seno")
        self.nasce(A2, [(A1.parte("t"), "t"), (A1.parte("lam"), "fr")], rt=1.7, extra=(Create(ba2),))
        self.an("C09-2", "que coisa linda")
        self.play(Indicate(ba2, color=WHITE_, scale_factor=1.04), run_time=0.9)
        self.an("C09-3")
        self.play(FadeIn(a3, shift=0.15 * UP), run_time=0.8)
        self.an("C09-3", "e isso dá exatamente")
        self.play(Indicate(a3[2], color=WHITE_, scale_factor=1.06), run_time=1.0)
        self.an("C09-3", "dois caminhos independentes")
        self.play(Indicate(VGroup(ba2, a3), color=WHITE_, scale_factor=1.03), run_time=1.0)
        self.an("C09-4")
        self.play(lam.animate.set_value(0.25), run_time=2.5)
        self.an("C09-4", "alvo mais pesado")
        self.play(lam.animate.set_value(0.85), run_time=3.0)
        # ── λ = 1: o círculo tem diâmetro de 0 a p₁ᵢ; Thales ───────────────────────────────────────────────────
        gA = VGroup(A1.mt, A2.m, ba2, a3)
        self.an("C09-5")
        self.play(lam.animate.set_value(1.0), FadeOut(gA), run_time=2.4)
        b1 = txt("TEOREMA DE THALES", 30).move_to(P3(XC, -0.7))
        b2 = M(r"\vec p_{1f}\perp\vec p_{2f}", size=56, w=4.8).move_to(P3(XC, -1.85))
        bb2 = dupla_caixa(b2)
        b3 = M(r"\theta_{\max}=90^\circ", size=44).move_to(P3(XC, -3.0))
        b4 = VGroup(M(r"p_{1f}=0", size=32), txt("RECUO FRONTAL", 24, op=0.9)).arrange(RIGHT, buff=0.25).move_to(P3(XC, -3.6))
        self.an("C09-5", "e o momento inicial vira")
        self.play(ShowPassingFlash(Line(pl.O, T).set_stroke(WHITE_, 9).set_z_index(12), time_width=0.9),
                  Indicate(p1i, color=WHITE_, scale_factor=1.04), run_time=1.2)
        self.an("C09-5", "o teorema de tales")
        self.play(FadeIn(b1, shift=0.1 * UP), run_time=0.8)
        self.an("C09-5", "liga às duas pontas")
        self.play(pv.animate.set_value(1.0), run_time=1.0)
        self.an("C09-5", "e o ângulo é sempre reto")
        self.play(ph.animate.set_value(60.0), run_time=2.4)
        self.an("C09-6")
        self.play(ph.animate.set_value(150.0), run_time=3.0)
        self.an("C09-6", "os dois lados que chegam nele")
        self.play(FadeIn(b2, shift=0.1 * UP), Create(bb2), run_time=1.2)
        self.an("C09-6", "só que agora a gente sabe")
        self.play(FadeIn(b3, shift=0.1 * UP), run_time=0.7)
        self.an("C09-6", "e quando o ponto chega na origem")
        self.play(ph.animate.set_value(180.0), run_time=1.6)
        self.play(FadeIn(b4, shift=0.1 * UP), run_time=0.7)
        self.an("C09-7")
        self.play(ph.animate.set_value(110.0), run_time=1.6)
        # ── λ > 1: a origem fica dentro; qualquer direção até 180° tem solução ─────────────────────────────────
        gB = VGroup(b1, b2, bb2, b3, b4)
        self.an("C09-7", "a razão passa de um")
        self.play(lam.animate.set_value(2.0), FadeOut(gB), run_time=3.0)
        c1 = txt("A ORIGEM FICA DENTRO DO CÍRCULO", 26).scale_to_fit_width(5.2).move_to(P3(XC, -0.7))
        c2 = VGroup(txt("QUALQUER DIREÇÃO ATÉ", 26), M(r"180^\circ", size=44)).arrange(RIGHT, buff=0.2).move_to(P3(XC, -1.6))
        c3 = txt("A INCIDENTE PODE VOLTAR", 28, color=CYAN, bold=True).scale_to_fit_width(5.0).move_to(P3(XC, -2.55))
        c4 = VGroup(txt("NÃO EXISTE ÂNGULO MÁXIMO", 24, op=0.9), VGroup(txt("MENOR QUE", 24, op=0.9), M(r"180^\circ", size=36))
                    .arrange(RIGHT, buff=0.15)).arrange(DOWN, buff=0.1).move_to(P3(XC, -3.4))
        self.an("C09-7", "e o círculo engole")
        self.play(FadeIn(c1, shift=0.1 * UP), run_time=0.8)
        self.an("C09-7", "toda semirreta corta")
        self.play(ph.animate.set_value(150.0), run_time=2.0)
        self.an("C09-7", "em qualquer direção")
        self.play(FadeIn(c2, shift=0.1 * UP), run_time=0.7)
        self.an("C09-7", "o corpo incidente pode voltar")
        self.play(ph.animate.set_value(145.0), FadeIn(c3, shift=0.1 * UP), run_time=1.4)
        self.an("C09-7", "é a bolinha")
        self.play(FadeIn(c4, shift=0.1 * UP), run_time=0.7)
        self.wait(1.0)
        din.clear_updaters()
        for m_ in (l1, l2, enche, botao):
            m_.clear_updaters()
        self.clear(rt=0.8)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C10 — alfa contra nêutron (λ = 1/4): o estado do ângulo limite (L-PALCO)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c10(self):
        self.secao("ALFA CONTRA NÊUTRON")
        lam = LAM_EX
        C, R = lam_cr(lam)
        thm = THMAX_EX
        p1f_n = np.sqrt(C * C - R * R)                                  # |p₁f|/p₁ᵢ no ponto de tangência = √15/5
        th2 = float(np.degrees(np.arctan2(p1f_n * np.sin(np.radians(thm)), 1 - p1f_n * np.cos(np.radians(thm)))))
        assert abs(thm - 14.4775) < 1e-3 and abs(p1f_n - np.sqrt(15) / 5) < 1e-12 and abs(th2 - 37.76) < 0.01
        assert abs(p1f_n ** 2 - 0.60) < 1e-12 and abs(4 * lam / (1 + lam) ** 2 - 16 / 25) < 1e-12
        pl = Plano(P3(-6.9, -0.6), 9.2)
        base = pl.base(-0.05, 1.06, -0.36, 0.38)
        tagp = self.tag_plano(False).move_to(pl.pt(0.2, -0.36) + P3(0, 0.38))
        T = pl.pt(1, 0)
        p1i = arrow(pl.O, T, color=MAG, width=7, tip=0.24, z=6)
        ctr = pl.pt(C, 0)
        circ = Circle(radius=R * pl.u).move_to(ctr).set_stroke(CYAN, 3.8).set_fill(CYAN, 0.12).set_z_index(3)
        halo = halo_circ(ctr, R * pl.u)
        vig = vinheta(ctr, 2.8, CYAN)
        Tp = pl.O + pol(p1f_n * pl.u, thm)
        Lw = (C + R) * pl.u
        cone = Sector(radius=Lw, angle=np.radians(2 * thm), start_angle=-np.radians(thm), arc_center=pl.O) \
            .set_fill(CYAN, 0.10).set_stroke(width=0).set_z_index(1)
        tang = VGroup(Line(pl.O, pl.O + pol(Lw, thm)).set_stroke(WHITE_, 2, opacity=0.85),
                      Line(pl.O, pl.O + pol(Lw, -thm)).set_stroke(WHITE_, 1.5, opacity=0.5)).set_z_index(5)
        v1 = arrow(pl.O, Tp, color=MAG, width=6.5, tip=0.22, z=7)
        v2 = arrow(Tp, T, color=MAG_L, width=6.5, tip=0.22, z=7)
        pt = ponto(Tp, WHITE_, 0.12, z=9)
        l1 = lab_at(M(r"\vec p_{1f}", size=34), pl.O, Tp, lado=1)
        l2 = lab_at(M(r"\vec p_{2f}", size=34), Tp, T, lado=-1)
        prol = DashedLine(Tp, Tp + P3(1.9, 0), dash_length=0.14).set_stroke(DIM, 1.6, opacity=0.8).set_z_index(5)
        ta = arco(pl.O, 1.6, 0, thm, w=2.0).set_z_index(6)
        tb = arco(Tp, 1.0, -th2, 0, w=2.0).set_z_index(6)
        lta = M(r"\theta_{\max}", size=30).move_to(pl.O + pol(2.35, thm / 2 + 2)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        ltb = M(r"\theta_2", size=30).move_to(Tp + pol(1.45, -th2 / 2)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        self.an("C10-1")
        self.play(FadeIn(base), FadeIn(tagp), GrowArrow(p1i), FadeIn(vig), Create(circ), FadeIn(halo), run_time=1.6)
        XR = 5.2
        dg = VGroup(Disco(C1F, 0.28, r"\alpha"), M(r"m_1=4m", size=32), Disco(C2F, 0.2, "n"), M(r"m_2=m", size=32)) \
            .arrange(RIGHT, buff=0.2).move_to(P3(XR, 3.05))
        dl = M(r"\Rightarrow\;\lambda=\tfrac14", size=40).move_to(P3(XR, 2.35))
        self.an("C10-1", "uma partícula alfa")
        self.play(FadeIn(dg, shift=0.1 * UP), run_time=0.9)
        self.an("C10-1", "a razão das massas é um quarto")
        self.play(FadeIn(dl, shift=0.1 * UP), run_time=0.8)
        slot = P3(XR, 0.7)
        E1 = Eq([("t", r"\theta_{\max}"), ("e", "="), ("arc", r"\arcsin\tfrac14"), ("ap", r"\approx14{,}5^\circ")], 44, w=4.4, pos=slot)

        def duas(p1, s1, p2, s2, w2=None):
            """Duas linhas de equação (uma EqJ) empilhadas no slot da coluna direita."""
            a, b = Eq(p1, s1, w=4.4), Eq(p2, s2, w=w2 or 4.4)
            VGroup(a.mt, b.mt).arrange(DOWN, buff=0.25).move_to(slot + P3(0, 0.1))
            return EqJ(l1=a, l2=b)
        E2 = duas([("lhs", r"\frac{p_{1f}}{p_{1i}}"), ("e", "="), ("rhs", r"\frac{\cos\theta_{\max}}{1+\lambda}")], 42,
                  [("e", "="), ("v", r"\frac{\sqrt{15}}{5}"), ("ap", r"\approx0{,}775")], 42, 3.6)
        E3 = duas([("lhs", r"\frac{K_{1f}}{K_{1i}}"), ("e", "="), ("rhs", r"\left(\frac{p_{1f}}{p_{1i}}\right)^2")], 42,
                  [("e", "="), ("v", r"60\%")], 48)
        E4 = duas([("lhs", r"K_{n,f}"), ("e", "="), ("v", r"0{,}40\,K_{\alpha,i}")], 44, [("th", r"\theta_2"), ("ap", r"\approx37{,}8^\circ")], 44)
        self.an("C10-1", "e o ângulo máximo é o arco seno")
        self.play(FadeIn(cone), Create(tang), FadeIn(E1.mt, shift=0.12 * UP), run_time=1.5)
        self.an("C10-1", "uns catorze vírgula cinco graus")
        self.play(Create(ta), FadeIn(lta), run_time=0.8)
        self.an("C10-1", "é um caminhão contra")
        self.play(Indicate(dg, color=WHITE_, scale_factor=1.06), run_time=1.0)
        self.an("C10-2")
        self.play(FadeIn(pt), GrowArrow(v1), FadeIn(l1), run_time=1.0)
        # o θ_max desce para dentro do cos θ_max e o ¼ vira o λ do denominador; o resto da linha de cima se desfaz
        rn = E2.num("l1.rhs")
        self.an("C10-2", "o momento da alfa")
        self.avanca(E1, E2, ("t", rn[-4:]), (E1.idx["arc"][-3:], E2.den("l1.rhs")[-1:]), ("e", "l1.e"), rt=2.0)
        self.an("C10-2", "uns zero vírgula setenta e sete")
        self.play(GrowArrow(v2), FadeIn(l2), run_time=0.8)
        # o p₁f/p₁ᵢ de cima entra no parêntese de K₁f/K₁ᵢ = (p₁f/p₁ᵢ)²; o resultado vira 60 %
        fr_l = sorted(E2.num("l1.lhs") + E2.barra("l1.lhs") + E2.den("l1.lhs"))
        fr_r = sorted(E3.num("l1.rhs") + E3.barra("l1.rhs") + E3.den("l1.rhs"))
        self.an("C10-2", "como a energia vai")
        self.avanca(E2, E3, (fr_l, fr_r), ("l1.e", "l1.e"), ("l2.e", "l2.e"), (E2.idx["l2.v"] + E2.idx["l2.ap"], "l2.v"), rt=2.0)
        # K: 60 % fica com a alfa, 40 % vai para o nêutron (no estado do ângulo limite); barra no topo do painel
        x0, wb, yb = -5.5, 7.0, 2.15
        capt = M(r"K_{\alpha,i}", size=32).move_to(P3(x0 + 0.55, yb + 0.55))
        barA = Rectangle(width=wb * 0.6, height=0.5, stroke_width=0, fill_color=CYAN, fill_opacity=0.9).move_to(P3(x0 + wb * 0.3, yb))
        barN = Rectangle(width=wb * 0.4, height=0.5, stroke_width=0, fill_color=KN, fill_opacity=0.9).move_to(P3(x0 + wb * 0.8, yb))
        lA_ = MathTex(r"\alpha", font_size=34, color=BACKGROUND_COLOR).move_to(barA)
        lN_ = MathTex("n", font_size=34, color=BACKGROUND_COLOR).move_to(barN)
        self.an("C10-2", "a alfa fica com sessenta")
        self.play(FadeIn(capt), GrowFromEdge(barA, LEFT), FadeIn(lA_), run_time=0.8)
        self.an("C10-3")
        self.play(GrowFromEdge(barN, LEFT), FadeIn(lN_), run_time=0.8)
        # os 60 % viram os 0,40 que foram para o nêutron
        self.an("C10-3", "que sai a uns trinta e sete")
        self.avanca(E3, E4, ("l1.e", "l1.e"), (E3.idx["l2.v"], E4.idx["l1.v"][:4]), rt=2.0, extra=(Create(prol), Create(tb), FadeIn(ltb)))
        self.an("C10-3", "mas atenção")
        self.play(Indicate(pt, color=WHITE_, scale_factor=2.0), run_time=1.0)
        fr = VGroup(txt("NA COLISÃO FRONTAL:", 24, op=0.9), M(r"\frac{4\lambda}{(1+\lambda)^2}=\frac{16}{25}=64\%", size=34, w=4.4)) \
            .arrange(DOWN, buff=0.15).move_to(P3(XR, -2.6))
        self.an("C10-3", "essa acontece de frente")
        self.play(FadeIn(fr, shift=0.1 * UP), run_time=0.8)
        self.wait(1.0)
        self.clear(rt=0.8)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C11 — acidente 2D completamente inelástico (enunciado próprio) + deslizamento (L-CENA)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c11(self):
        self.secao("ACIDENTE EM 2D")
        # dados e verificações numéricas (desenvolvimento; não vão para o vídeo)
        Mt, mc, vT, vC = 3000.0, 1000.0, 60 / 3.6, 90 / 3.6
        vfx, vfy = mc * vC / (Mt + mc), Mt * vT / (Mt + mc)
        vf = float(np.hypot(vfx, vfy))
        th = float(np.degrees(np.arctan2(vfy, vfx)))
        mu, g_ = 0.5, 10.0
        dsl = vf ** 2 / (2 * mu * g_)
        assert abs(vfx - 6.25) < 1e-9 and abs(vfy - 12.5) < 1e-9 and abs(th - 63.4349) < 1e-3 and abs(vf - 13.9754) < 1e-3
        assert abs(dsl - 19.53) < 0.01 and abs(vf ** 2 - 195.3125) < 1e-6
        VS, AK = 0.08, 0.07                                          # tela por (m/s): posições e setas de velocidade
        a_ = mu * g_
        Tstop = vf / a_
        dirv = np.array([vfx, vfy, 0.0]) / vf
        cr = P3(-3.2, -0.4)                                          # centro do cruzamento
        ct, cc = cr.copy(), cr + P3(-1.3, 0)                         # caminhão e carro no instante do contato
        W = 2.4
        h = Rectangle(width=8.4, height=W).move_to(P3(-3.2, -0.4))
        v = Rectangle(width=W, height=6.9).move_to(P3(-3.2, -0.45))
        try:
            via = Union(h, v).set_fill([_fundo(0.13), _fundo(0.06)], opacity=1.0).set_stroke(DIM, 1.6, opacity=0.55)
        except Exception:
            via = VGroup(h, v).set_fill(_fundo(0.1), opacity=1.0).set_stroke(DIM, 1.6, opacity=0.55)
        via.set_z_index(-3)
        eixo_c = VGroup(DashedLine(P3(-7.4, -0.4), P3(-4.4, -0.4), dash_length=0.2), DashedLine(P3(-2.0, -0.4), P3(1.0, -0.4), dash_length=0.2),
                        DashedLine(P3(-3.2, -3.9), P3(-3.2, -1.6), dash_length=0.2), DashedLine(P3(-3.2, 0.8), P3(-3.2, 3.0), dash_length=0.2)) \
            .set_stroke(WHITE_, 1.3, opacity=0.28).set_z_index(-2)
        bus = VGroup(arrow(P3(-0.3, 1.35), P3(-0.3, 2.15), color=DIM, width=3, tip=0.15), arrow(P3(-0.3, 1.35), P3(0.5, 1.35), color=DIM, width=3, tip=0.15),
                     txt("NORTE", 22, color=DIM).move_to(P3(-0.3, 2.45)), txt("LESTE", 22, color=DIM).move_to(P3(0.2, 1.05)))
        truck = Carro(2.3, 1.0, CAR1, CAR1_L, "M", ang=PI / 2, fs=46)
        car = Carro(1.6, 0.84, CAR2, CAR2_L, "m", fs=38)
        t = ValueTracker(-1.0)

        def disp(tt):
            if tt <= 0:
                return np.zeros(3)
            s = vf * tt - 0.5 * a_ * tt * tt if tt <= Tstop else dsl
            return dirv * s * VS

        def pos_t():
            tt = t.get_value()
            return (ct + P3(0, vT * VS * tt)) if tt <= 0 else (ct + disp(tt))

        def pos_c():
            tt = t.get_value()
            return (cc + P3(vC * VS * tt, 0)) if tt <= 0 else (cc + disp(tt))
        truck.add_updater(lambda m: m.move_to(pos_t()))
        car.add_updater(lambda m: m.move_to(pos_c()))
        truck.move_to(pos_t())
        car.move_to(pos_c())

        def setas():
            tt = t.get_value()
            if tt <= 0:
                a = pos_t() + P3(0, 1.15 + 0.06)
                b = pos_c() + P3(0.8 + 0.06, 0)
                g = VGroup(arrow(a, a + P3(0, vT * AK), color=VEL, width=5.5, tip=0.22))
                folga = pos_t()[0] - 0.5 - b[0] - 0.1                    # a seta do carro não entra no caminhão
                if folga >= 0.7:
                    g.add(arrow(b, b + P3(min(vC * AK, folga), 0), color=VEL, width=5.5, tip=0.22))
                return g
            sp = max(vf - a_ * tt, 0.0) if tt <= Tstop else 0.0
            if sp < 0.6:
                return VGroup()
            a = pos_t() + P3(0, 1.2)
            return VGroup(arrow(a, a + dirv * sp * AK * 1.4, color=VEL, width=5.5, tip=0.22))
        sv = always_redraw(setas)
        dT = VGroup(M(r"M=3000\ \mathrm{kg}", size=32), M(r"60\ \mathrm{km/h}", size=32, color=VEL)).arrange(DOWN, buff=0.1) \
            .move_to(P3(-0.35, -2.7))
        dC = VGroup(M(r"m=1000\ \mathrm{kg}", size=32), M(r"90\ \mathrm{km/h}", size=32, color=VEL)).arrange(DOWN, buff=0.1) \
            .move_to(P3(-5.9, 1.55))
        # enunciado próprio (construído para o vídeo; os dados de massa e velocidade ficam nos rótulos dos veículos)
        enun = VGroup(txt("O PROBLEMA", 22, color=DIM),
                      txt("UM CAMINHÃO E UM CARRO", 24), txt("COLIDEM NUM CRUZAMENTO", 24), txt("E FICAM PRESOS.", 24),
                      txt("DEPOIS, DERRAPAM NO ASFALTO", 24), txt("COM ATRITO CINÉTICO 0,5.", 24),
                      txt("QUAL A VELOCIDADE LOGO APÓS", 24, color=CYAN), txt("O CHOQUE? E QUANTO DERRAPAM?", 24, color=CYAN)) \
            .arrange(DOWN, buff=0.16).move_to(P3(4.5, 1.1))
        self.an("C11-1")
        self.play(FadeIn(via), FadeIn(eixo_c), FadeIn(bus), FadeIn(truck), FadeIn(car), FadeIn(sv), FadeIn(enun, shift=0.1 * UP), run_time=1.4)
        self.an("C11-1", "um caminhão de três mil")
        self.play(FadeIn(dT, shift=0.1 * UP), t.animate.set_value(-0.8), rate_func=linear, run_time=3.0)
        self.an("C11-1", "bate num carro")
        self.play(FadeIn(dC, shift=0.1 * UP), t.animate.set_value(-0.55), rate_func=linear, run_time=3.0)
        self.an("C11-1", "eles ficam presos")
        self.play(t.animate.set_value(-0.35), rate_func=linear, run_time=3.0)
        self.an("C11-2")
        self.play(t.animate.set_value(0.0), rate_func=linear, run_time=0.9)
        self.play(Flash(cr + P3(-0.5, 0), color=WHITE_, line_length=0.3, flash_radius=0.2, num_lines=10, run_time=0.4))
        t.set_value(1e-5)
        self.play(FadeOut(dT), FadeOut(dC), t.animate.set_value(0.45), rate_func=rate_functions.ease_out_sine, run_time=1.4)
        vfl = M(r"\vec v_f", size=34).move_to(pos_t() + P3(0, 1.2) + dirv * 1.15 + P3(0.5, 0.2)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        self.play(FadeIn(vfl), FadeOut(enun), run_time=0.6)
        # o momento vetorial vale; os passos recuam na coluna fina da direita
        X1 = 4.5
        pil = Pilha(self, X1, (2.55, 1.75, 0.95), esc=0.66)
        YC, YX, YY = -0.45, 0.15, -1.0

        def lin(partes, s, y):
            return Eq(partes, s, w=5.6, pos=P3(X1, y))
        s_p = Eq([("a", r"\vec P_i", MAG), ("eq", "="), ("b", r"\vec P_f", MAG)], 52, pos=P3(X1, YC))
        c1 = EqJ(x=lin([("a", r"m\cdot25"), ("eq", "="), ("b", r"(M+m)\,"), ("c", "v_{fx}", VEL)], 46, YX),
                 y=lin([("a", r"M\cdot\tfrac{50}{3}"), ("eq", "="), ("b", r"(M+m)\,"), ("c", "v_{fy}", VEL)], 46, YY))
        c2 = EqJ(x=lin([("c", "v_{fx}", VEL), ("eq", "="), ("n", r"6{,}25\ \mathrm{m/s}")], 50, YX),
                 y=lin([("c", "v_{fy}", VEL), ("eq", "="), ("n", r"12{,}5\ \mathrm{m/s}")], 50, YY))
        s_t = Eq([("a", r"\tan\theta"), ("eq", "="), ("b", r"\frac{v_{fy}}{v_{fx}}", None), ("eq2", "="), ("n", "2")], 48, w=5.6,
                 pos=P3(X1, YC))
        s_t.cor("b", "num1")
        s_t2 = Eq([("a", r"\theta\approx63{,}4^\circ")], 54, pos=P3(X1, YC))
        s_v = Eq([("a", r"|\vec v_f|\approx13{,}98\ \mathrm{m/s}")], 48, w=5.6, pos=P3(X1, YC))
        self.an("C11-2", "o momento que é vetorial")
        self.play(FadeIn(s_p.mt, shift=0.15 * UP), run_time=1.0)
        self.an("C11-2", "escreve o momento em duas componentes")
        # o vetor se abre nas duas componentes: cada termo vai para as duas linhas (x e y)
        self.avanca(s_p, c1, ("a", "x.a"), ("a", "y.a"), ("eq", "x.eq"), ("eq", "y.eq"), ("b", ["x.b", "x.c"]), ("b", ["y.b", "y.c"]),
                    rt=2.4, pil=pil)
        self.an("C11-2", "para o leste só o carro")
        self.play(Indicate(c1.parte("x.a"), color=WHITE_, scale_factor=1.12), run_time=0.9)
        self.an("C11-2", "para o norte só o caminhão")
        self.play(Indicate(c1.parte("y.a"), color=WHITE_, scale_factor=1.12), run_time=0.9)
        self.an("C11-2", "cada uma é igual")
        self.play(Indicate(VGroup(c1.parte("x.b"), c1.parte("x.c"), c1.parte("y.b"), c1.parte("y.c")), color=VEL, scale_factor=1.08), run_time=1.0)
        # isola cada componente: o v_f vai para a esquerda da igualdade e a conta vira número
        self.an("C11-3")
        self.avanca(c1, c2, ("x.c", "x.c"), ("y.c", "y.c"), ("x.eq", "x.eq"), ("y.eq", "y.eq"), (["x.a", "x.b"], "x.n"),
                    (["y.a", "y.b"], "y.n"), rt=2.4)
        # tg θ = v_fy / v_fx: as duas componentes entram na fração
        self.an("C11-3", "a tangente do ângulo é dois")
        self.avanca(c2, s_t, ("y.c", s_t.num("b")), ("x.c", s_t.den("b")), ("x.eq", "eq"), ("y.eq", "eq2"), (["x.n", "y.n"], "n"),
                    rt=2.4)
        # θ sai do tg θ; o 2 vira 63,4°
        self.an("C11-3", "sessenta e três vírgula quatro graus")
        self.avanca(s_t, s_t2, (("a", 3), ("a", 0)), ("n", s_t2.idx["a"][1:]), rt=1.8, pil=pil)
        # direção do movimento conjunto: arco branco a partir do leste
        pa = pos_t() + P3(0, 1.2)                                   # início da seta v_f: o transferidor fica nela
        ang = arco(pa, 0.95, 0, th, w=2.2)
        tha = M(r"\theta", size=34).move_to(pa + pol(1.3, 22)).set_stroke(BACKGROUND_COLOR, 5, background=True)
        ref_l = DashedLine(pa, pa + P3(1.7, 0), dash_length=0.12).set_stroke(DIM, 1.6, opacity=0.8)
        self.an("C11-3", "a partir do leste")
        self.play(Create(ref_l), Create(ang), FadeIn(tha), run_time=1.2)
        self.an("C11-3", "o módulo é quase")
        self.passo(pil, s_t2, s_v)
        self.an("C11-3", "o vetor aponta mais para o norte")
        self.play(Indicate(vfl, color=WHITE_, scale_factor=1.5), run_time=1.0)
        # K não se conserva: o que não ficou como cinética foi dissipado (laranja)
        Ki = 0.5 * Mt * vT ** 2 + 0.5 * mc * vC ** 2
        Kf = 0.5 * (Mt + mc) * vf ** 2
        wk = 5.2
        msg = VGroup(txt("O MOMENTO VALE SEM CONSERVAR", 24), M("K", size=32)).arrange(RIGHT, buff=0.15).move_to(P3(X1, -2.75))
        bK = Rectangle(width=wk * Kf / Ki, height=0.3, stroke_width=0, fill_color=CYAN, fill_opacity=0.9)
        bH = Rectangle(width=wk * (1 - Kf / Ki), height=0.3, stroke_width=0, fill_color=HEAT, fill_opacity=0.85)
        VGroup(bK, bH).arrange(RIGHT, buff=0).move_to(P3(X1, -3.4))
        self.an("C11-4")
        self.play(*pil.limpa(), FadeOut(s_v.mt), FadeIn(msg, shift=0.1 * UP), run_time=0.9)
        self.play(GrowFromEdge(bK, LEFT), GrowFromEdge(bH, LEFT), run_time=1.0)
        res_card = VGroup(M(r"\vec v_f=(6{,}25;\ 12{,}5)\ \mathrm{m/s}", size=40, w=5.6), M(r"\theta\approx63{,}4^\circ", size=48),
                          M(r"|\vec v_f|\approx13{,}98\ \mathrm{m/s}", size=40, w=5.6)).arrange(DOWN, buff=0.3).move_to(P3(X1, 0.55))
        self.an("C11-4", "virou lataria")
        self.play(FadeIn(res_card, shift=0.12 * UP), Indicate(bH, color=HEAT, scale_factor=1.2), run_time=1.0)
        self.wait(0.8)
        # ── a colisão acabou: outro processo, outro princípio ──────────────────────────────────────────────────
        self.an("C11-5")
        self.play(FadeOut(res_card), FadeOut(msg), FadeOut(bK), FadeOut(bH), FadeOut(vfl), FadeOut(ang), FadeOut(tha), FadeOut(ref_l), run_time=0.8)
        ch = VGroup(txt("IMPACTO: MOMENTO", 26), txt("DEPOIS: TRABALHO–ENERGIA", 26, color=CYAN)).arrange(DOWN, buff=0.15).move_to(P3(X1, 2.45))
        w0 = M(r"\mu_k=0{,}5,\ \ g\approx10\ \mathrm{m/s^2}", size=36, w=5.6).move_to(P3(X1, 1.4))
        W1 = Eq([("h", r"\tfrac12"), ("M1", r"(M+m)\,"), ("vf2", "v_f^2", VEL), ("eq", "="), ("mu", r"\mu_k\,"), ("M2", r"(M+m)\,"),
                 ("g", r"g\,"), ("d", "d")], 44, w=5.7, pos=P3(X1, 0.35))
        W2 = Eq([("d", "d"), ("eq", "="), ("fr", r"\frac{v_f^2}{2\mu_k g}"), ("eq2", "="),
                 ("val", r"\frac{195{,}3}{10}\approx19{,}5\ \mathrm{m}")], 44, w=5.7, pos=P3(X1, -1.3))
        for i_ in W2.num("fr"):
            W2.gl[i_].set_color(VEL)
        w3 = txt("A MASSA CANCELA", 24, op=0.9).move_to(P3(X1, -2.4))
        w4 = txt("COMO NO PÊNDULO: SEPARE OS PROCESSOS", 24, op=0.9).scale_to_fit_width(5.8).move_to(P3(X1, -3.3))
        nn_ = np.array([dirv[1], -dirv[0], 0.0])                   # perpendicular, à direita do deslizamento
        q0_, q1_ = ct + nn_ * 1.6, ct + dirv * dsl * VS + nn_ * 1.6
        trilha = VGroup(Line(q0_, q1_), Line(q0_ - nn_ * 0.16, q0_ + nn_ * 0.16), Line(q1_ - nn_ * 0.16, q1_ + nn_ * 0.16)) \
            .set_stroke(GEO, 2.8, opacity=0.95).set_z_index(1)
        dl = M("d", size=36, color=GEO).move_to((q0_ + q1_) / 2 + nn_ * 0.5).set_stroke(BACKGROUND_COLOR, 5, background=True)
        self.an("C11-5", "e começou outro processo")
        self.play(t.animate.set_value(Tstop * 0.35), rate_func=linear, run_time=Tstop * 0.5)
        self.an("C11-5", "mudou o processo muda o princípio")
        self.play(t.animate.set_value(Tstop * 0.7), FadeIn(ch, shift=0.1 * UP), rate_func=linear, run_time=Tstop * 0.5)
        self.an("C11-5", "depois trabalho e energia")
        self.play(t.animate.set_value(Tstop), FadeIn(w0, shift=0.1 * UP), rate_func=linear, run_time=Tstop * 0.5)
        self.an("C11-5", "a energia cinética que sobrou")
        self.play(FadeIn(W1.mt, shift=0.1 * UP), run_time=1.2)
        # a massa cancela: o ½ vira o 2 do denominador, μ_k e g descem, os dois (M+m) se anulam; a cópia de w1 fica como referência
        W1c = W1.m.copy()
        self.add(W1c)
        dn = W2.den("fr")
        self.an("C11-5", "e a massa total cancela")
        self.avanca(W1, W2, ("d", "d"), ("eq", "eq"), ("vf2", W2.num("fr")), (("h", slice(2, 3)), dn[:1]), ("mu", dn[1:3]), ("g", dn[3:4]),
                    ("M1", [], {"shift": 0.5 * DOWN, "scale": 0.4}), ("M2", [], {"shift": 0.5 * DOWN, "scale": 0.4}),
                    rt=2.6, extra=(FadeIn(w3, shift=0.1 * UP),))
        self.an("C11-5", "a distância é a velocidade")
        self.play(Create(trilha), FadeIn(dl), run_time=0.8)
        self.an("C11-5", "uns dezenove vírgula cinco metros")
        self.play(Indicate(W2.parte("val"), color=WHITE_, scale_factor=1.1), run_time=1.0)
        self.an("C11-5", "como no pêndulo")
        self.play(FadeIn(w4, shift=0.1 * UP), run_time=0.6)
        self.wait(1.0)
        for m_ in (truck, car, sv):
            m_.clear_updaters()
        self.clear(rt=0.8)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C12 — explosão: mesmo momento, outra história energética (L-CENA)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c12(self):
        self.secao("EXPLOSÕES")
        p1, p2 = pol(2.0, 80.0), pol(1.5, 205.0)
        p3 = -(p1 + p2)
        assert np.linalg.norm(p1 + p2 + p3) < 1e-12
        rs = (0.55, 0.45, 0.38)
        ps = (p1, p2, p3)
        vel = [np.linalg.norm(ps[k]) / rs[k] ** 2 for k in range(3)]
        dist = [3.0 * v / max(vel) for v in vel]
        c0 = P3(-3.4, 0.1)
        corpo = Disco(STEEL, 0.85).move_to(c0)
        z = M(r"\vec P_i=\vec 0", size=44).move_to(P3(-3.4, -1.55))
        vig = vinheta(c0, 3.6, VEL, 0.10)
        s = ValueTracker(0.0)                                       # 0 = parado; 1 = fragmentos afastados
        frag = [Disco(C1F if k != 1 else C2F, rs[k], ["m_1", "m_2", "m_3"][k]) for k in range(3)]

        def pos_f(k):
            return c0 + unit(ps[k]) * (dist[k] * s.get_value())
        for k, f in enumerate(frag):
            f.add_updater(lambda m, k=k: m.move_to(pos_f(k)))
            f.move_to(pos_f(k))

        def rastros():
            g = VGroup()
            for k in range(3):
                if s.get_value() > 0.02:
                    g.add(Line(c0, pos_f(k)).set_stroke(GEO, 2.2, opacity=0.35))
            return g

        def setas_p():
            if s.get_value() < 0.05:
                return VGroup()
            g = VGroup()
            for k in range(3):
                a = pos_f(k) + unit(ps[k]) * (rs[k] + 0.06)
                g.add(arrow(a, a + ps[k] * 0.45, color=MAG if k != 1 else MAG_L, width=6.5, tip=0.22))
            return g.set_opacity(min(1.0, s.get_value() * 2))
        rs_ = always_redraw(rastros)
        sp = always_redraw(setas_p)
        self.an("C12-1")
        self.play(FadeIn(vig), FadeIn(corpo), FadeIn(z, shift=0.12 * UP), run_time=1.0)
        self.an("C12-1", "o corpo estava parado")
        self.play(Indicate(z, color=WHITE_, scale_factor=1.1), run_time=1.0)
        self.an("C12-1", "os três pedaços saem")
        self.remove(corpo)
        self.add(rs_, *frag)
        onda = Circle(radius=0.9).move_to(c0).set_stroke(WHITE_, 3, opacity=0.8)
        self.play(Flash(c0, color=WHITE_, line_length=0.4, flash_radius=0.55, num_lines=16, run_time=0.5),
                  onda.animate.scale(3.0).set_stroke(opacity=0.0), FadeOut(z), run_time=0.7)
        self.remove(onda)
        self.add(sp)
        self.play(s.animate.set_value(1.0), rate_func=rate_functions.ease_out_cubic, run_time=2.4)
        # Σ p = 0 : os três momentos fecham um triângulo
        E1 = Eq([("sg", r"\sum_k"), ("p", r"\vec p_k", MAG), ("e", "="), ("z", r"\vec 0")], 56, pos=P3(4.7, 2.5))
        E1b = Eq([("p1", r"\vec p_1", MAG), ("m1", "+"), ("p2", r"\vec p_2", MAG_L), ("m2", "+"), ("p3", r"\vec p_3", MAG), ("e", "="),
                  ("z", r"\vec 0")], 50, w=5.8, pos=P3(4.7, 2.5))
        nota = txt("SE PARTIU DO REPOUSO", 22, color=DIM).move_to(P3(4.7, 3.3))
        self.an("C12-1", "com momentos que somam zero")
        self.play(FadeIn(nota), FadeIn(E1.mt, shift=0.12 * UP), run_time=1.2)
        O = P3(3.3, -0.35)
        k_ = 0.95
        a1 = arrow(O, O + p1 * k_, color=MAG, width=6.5, tip=0.22)
        a2 = arrow(O + p1 * k_, O + (p1 + p2) * k_, color=MAG_L, width=6.5, tip=0.22)
        a3 = arrow(O + (p1 + p2) * k_, O, color=MAG, width=6.5, tip=0.22)
        t1 = lab_at(M(r"\vec p_1", size=32), O, O + p1 * k_, lado=-1)
        t2 = lab_at(M(r"\vec p_2", size=32), O + p1 * k_, O + (p1 + p2) * k_, lado=-1)
        t3 = lab_at(M(r"\vec p_3", size=32), O + (p1 + p2) * k_, O, lado=-1)
        self.an("C12-1", "formando um triângulo fechado")
        self.play(GrowArrow(a1), FadeIn(t1), run_time=0.8)
        self.play(GrowArrow(a2), FadeIn(t2), run_time=0.8)
        self.play(GrowArrow(a3), FadeIn(t3), run_time=0.8)
        # a soma sobre k se desdobra nos três momentos do triângulo (o p⃗ₖ se copia em p⃗₁, p⃗₂ e p⃗₃)
        self.avanca(E1, E1b, ("p", "p1"), ("p", "p2"), ("p", "p3"), rt=2.0)
        # energia: a interna alimenta a cinética; o total não muda
        wtot = 5.2
        u = ValueTracker(0.0)
        fi = lambda: max(wtot * (1 - 0.55 * u.get_value()), 1e-3)           # noqa: E731
        fc = lambda: max(wtot * 0.55 * u.get_value(), 1e-3)                 # noqa: E731
        bI = always_redraw(lambda: Rectangle(width=fi(), height=0.3, stroke_width=0, fill_color=HEAT, fill_opacity=0.85)
                           .move_to(P3(1.8 + fi() / 2, -1.8)))
        bC = always_redraw(lambda: Rectangle(width=fc(), height=0.3, stroke_width=0, fill_color=CYAN, fill_opacity=0.9)
                           .move_to(P3(1.8 + fc() / 2, -2.65)))
        bT = Rectangle(width=wtot, height=0.09, stroke_width=0, fill_color=WHITE_, fill_opacity=0.6).move_to(P3(1.8 + wtot / 2, -3.2))
        lI = txt("ENERGIA INTERNA", 24, color=HEAT).move_to(P3(1.8, -1.45), aligned_edge=LEFT)
        lC = VGroup(txt("ENERGIA CINÉTICA", 24, color=CYAN), M("K", size=30)).arrange(RIGHT, buff=0.12).move_to(P3(1.8, -2.3), aligned_edge=LEFT)
        lT = txt("TOTAL: CONSTANTE", 22, op=0.85).move_to(P3(1.8, -3.55), aligned_edge=LEFT)
        cmp_ = M(r"K_i=0\;\to\;K_f>0", size=40).move_to(P3(4.7, -0.85))
        self.an("C12-1", "a energia cinética vai de zero")
        self.play(FadeIn(lI), FadeIn(lC), FadeIn(bI), FadeIn(bC), FadeIn(bT), FadeIn(lT), run_time=0.9)
        self.an("C12-1", "a energia interna vira cinética")
        self.play(u.animate.set_value(1.0), run_time=2.2)
        self.an("C12-1", "sem criar energia nenhuma")
        self.play(FadeIn(cmp_, shift=0.1 * UP), run_time=0.9)
        self.wait(1.0)
        for m_ in (*frag, sp, rs_, bI, bC):
            m_.clear_updaters()
        self.clear(rt=0.8)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C13 — método geral e síntese (L-CENA): fluxo vertical grande com um corpo-exemplo percorrendo os cartões
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c13(self):
        self.secao("MÉTODO E SÍNTESE")
        titulos = ("SISTEMA?", "IMPULSO EXTERNO DESPREZÍVEL?", "QUANTAS DIMENSÕES?", "TIPO DE EVENTO?", "NOVA ETAPA DEPOIS?")
        alt = (1.2, 1.2, 1.2, 1.9, 1.2)
        tops, y_ = [], 3.2
        for a_ in alt:
            tops.append(y_)
            y_ -= a_ + 0.1
        cy = [t_ - a_ / 2 for t_, a_ in zip(tops, alt)]
        cards, tits, nums = VGroup(), [], []
        for i, (s_, a_, c_) in enumerate(zip(titulos, alt, cy)):
            r_ = RoundedRectangle(corner_radius=0.2, width=14.0, height=a_).set_stroke(WHITE_, 1.6, opacity=0.35) \
                .set_fill([_fundo(0.08), _fundo(0.035)], opacity=1.0).move_to(P3(0, c_))
            r_.set_sheen_direction(DOWN)
            n_ = M(str(i + 1), size=44, color=DIM).move_to(P3(-6.35, c_))
            t_ = txt(s_, 28).move_to(P3(-5.8, c_), aligned_edge=LEFT)
            tits.append(t_)
            nums.append(n_)
            cards.add(VGroup(r_, n_, t_))
        mk = Disco(C1F, 0.26, "m").set_z_index(20)

        def foco(i):
            return [c_[0].animate.set_stroke(CYAN if k == i else WHITE_, 2.4 if k == i else 1.6, opacity=0.95 if k == i else 0.35)
                    for k, c_ in enumerate(cards)]
        self.an("C13-1")
        self.play(LaggedStart(*[FadeIn(c_, shift=0.12 * RIGHT) for c_ in cards], lag_ratio=0.15), run_time=1.8)
        mk.move_to(P3(-7.0, cy[0]))
        self.play(FadeIn(mk, scale=0.6), *foco(0), run_time=0.7)
        # 1 sistema
        d1, d2 = Disco(C1F, 0.3, "m_1"), Disco(C2F, 0.26, "m_2")
        sis = VGroup(d1, d2).arrange(RIGHT, buff=0.35)
        cont = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=sis.width + 0.6, height=sis.height + 0.4).move_to(sis)
                              .set_stroke(WHITE_, 2, opacity=0.65), num_dashes=40)
        c1 = VGroup(VGroup(sis, cont), txt("O QUE ENTRA NO SISTEMA", 24, op=0.9)).arrange(RIGHT, buff=0.5).move_to(P3(3.3, cy[0]))
        self.an("C13-1", "um qual é o sistema")
        self.play(FadeIn(c1, shift=0.1 * UP), run_time=0.8)
        # 2 impulso externo
        c2 = M(r"J_{\mathrm{ext}}\approx0\;\Rightarrow\;\vec P_i=\vec P_f", size=40, w=5.8).move_to(P3(3.3, cy[1]))
        self.an("C13-1", "dois o impulso externo")
        self.play(mk.animate.move_to(P3(-7.0, cy[1])), *foco(1), FadeIn(c2, shift=0.1 * UP), run_time=0.9)
        # 3 dimensões
        c3 = VGroup(txt("1D: UMA COMPONENTE", 24), txt("2D: DUAS + GEOMETRIA VETORIAL", 24, color=CYAN)).arrange(DOWN, buff=0.15, aligned_edge=LEFT) \
            .move_to(P3(3.3, cy[2]))
        self.an("C13-1", "três quantas dimensões")
        self.play(mk.animate.move_to(P3(-7.0, cy[2])), *foco(2), FadeIn(c3, shift=0.1 * UP), run_time=0.9)
        # 4 tipo de evento

        def lin(a, b):
            return VGroup(txt(a, 22), M(r"\rightarrow", size=28), b).arrange(RIGHT, buff=0.15)
        c4 = VGroup(lin("ELÁSTICA", M("K_i=K_f", size=30)),
                    lin("COMPLETAMENTE INELÁSTICA", M(r"\vec v_{1f}=\vec v_{2f}", size=30)),
                    lin("EXPLOSÃO", txt("ENERGIA INTERNA ALIMENTA K", 22)),
                    lin("OUTRO CASO", txt("CONDIÇÃO DADA", 22))).arrange(DOWN, buff=0.13, aligned_edge=LEFT).move_to(P3(2.6, cy[3]))
        self.an("C13-1", "quatro qual é o tipo")
        self.play(mk.animate.move_to(P3(-7.0, cy[3])), *foco(3), run_time=0.7)
        for l_, fr_ in zip(c4, ("elástica", "grudou", "explosão", "ou outro")):
            self.an("C13-1", fr_)
            self.play(FadeIn(l_, shift=0.1 * RIGHT), run_time=0.5)
        # 5 nova etapa
        c5 = VGroup(txt("SEPARE OS PROCESSOS", 30, color=CYAN, bold=True),
                    VGroup(txt("IMPACTO", 22), M(r"\rightarrow", size=28), txt("DESLIZAMENTO", 22)).arrange(RIGHT, buff=0.2)) \
            .arrange(DOWN, buff=0.12).move_to(P3(3.3, cy[4]))
        self.an("C13-1", "cinco começou outro processo")
        self.play(mk.animate.move_to(P3(-7.0, cy[4])), *foco(4), FadeIn(c5, shift=0.1 * UP), run_time=0.9)
        self.wait(1.0)
        self.an("C13-2")
        self.clear(rt=0.8)
        # ── resposta ao hook ────────────────────────────────────────────────────────────────────────────────────
        q = self.hl("O QUE MUDOU DO 1D PARA O 2D?", y=2.6, size=46, color=CYAN)
        l1 = txt("A CONSERVAÇÃO DO MOMENTO NÃO MUDOU", 30).move_to(P3(0, 1.3))
        l2 = txt("O MOMENTO SEMPRE FOI UM VETOR", 30).move_to(P3(0, 0.4))
        l3 = txt("NO 1D, A GEOMETRIA FICAVA ESCONDIDA NA LINHA", 30, op=0.92).move_to(P3(0, -0.5))
        l4 = txt("NO 2D, ELA APARECE: DIREÇÕES, ÂNGULOS E ESTADOS POSSÍVEIS", 30).scale_to_fit_width(14.0).move_to(P3(0, -1.4))
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.9)
        for l_, fr_ in zip((l1, l2, l3, l4), ("a conservação do momento", "ele sempre foi um vetor", "em uma dimensão a geometria", "em duas ela aparece")):
            self.an("C13-2", fr_)
            self.play(FadeIn(l_, shift=0.1 * UP), run_time=0.7)
        self.an("C13-2", "momento mais tipo de colisão virou")
        self.play(FadeOut(VGroup(q, l1, l2, l3, l4)), run_time=0.7)
        self.remove(q, l1, l2, l3, l4)
        seta = lambda: M(r"\rightarrow", size=30)                                    # noqa: E731
        faixa = VGroup(txt("SISTEMA", 24), seta(), M(r"\vec P", size=40), seta(), txt("GEOMETRIA", 24), seta(),
                       txt("TIPO DE COLISÃO", 24), seta(), txt("NOVA ETAPA, SE HOUVER", 24)).arrange(RIGHT, buff=0.14)
        faixa.scale_to_fit_width(min(faixa.width, 14.2)).move_to(P3(0, 0.9))
        par1 = VGroup(txt("1D", 40, bold=True), M("=", size=44), txt("MOMENTO + TIPO", 36)).arrange(RIGHT, buff=0.25).move_to(P3(0, -0.8))
        par2 = VGroup(txt("2D", 40, bold=True, color=CYAN), M("=", size=44), txt("MOMENTO + GEOMETRIA + TIPO", 36, color=CYAN)) \
            .arrange(RIGHT, buff=0.25).move_to(P3(0, -1.95))
        self.play(LaggedStart(*[FadeIn(m_, shift=0.1 * UP) for m_ in faixa], lag_ratio=0.12), run_time=2.4)
        self.an("C13-2", "virou momento")
        self.play(FadeIn(par1, shift=0.1 * UP), run_time=0.8)
        self.an("C13-2", "mais geometria")
        self.play(FadeIn(par2, shift=0.1 * UP), run_time=0.8)
        self.an("C14-1")
        self.clear(rt=0.8)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C14 (L-CENA) — gancho para o próximo vídeo: o mesmo impulso, no centro e fora do centro (translação × giro)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c14(self):
        self.secao("O PRÓXIMO PASSO")
        R_D, r_p, cy, c0x = 1.5, 0.32, 0.1, -3.4
        DX, OFF2, GIRO = 2.6, 0.95, -300.0              # translação do centro (igual nos dois casos), deslocamento do impacto, giro (horário)
        pp = ValueTracker(0.0)                          # 0 → 1: projétil indo ao contato
        u = ValueTracker(0.0)                           # 0 → 1: depois do impacto (translação e giro)
        cs = {"off": 0.0, "giro": 0.0}
        x_sup = lambda: c0x - np.sqrt(R_D ** 2 - cs["off"] ** 2)                    # noqa: E731  ponto da superfície onde bate
        cen = lambda: P3(c0x + DX * u.get_value(), cy)                              # noqa: E731
        disco = Disco(C2F, R_D).move_to(cen())
        disco.add_updater(lambda m: m.move_to(cen()))

        def marcador():
            c = cen()
            a = 60.0 + cs["giro"] * u.get_value()
            pe = c + pol(R_D * 0.8, a)
            return VGroup(Line(c, pe).set_stroke(WHITE_, 4.5, opacity=0.9), Dot(pe, radius=0.11, color=WHITE_)).set_z_index(6)
        marc = always_redraw(marcador)
        proj = Disco(C1F, r_p)
        proj.add_updater(lambda m: m.move_to(P3(-7.0 + (x_sup() - r_p + 7.0) * pp.get_value(), cy + cs["off"])))

        def vcentro():
            if u.get_value() < 0.02:
                return VGroup()
            c = cen()
            a = c + P3(-0.7, R_D + 0.5)
            return VGroup(arrow(a, a + P3(1.4, 0), color=VEL, width=6, tip=0.24))
        vc = always_redraw(vcentro)

        def giro_arc():
            if abs(cs["giro"]) < 1 or u.get_value() < 0.05:
                return VGroup()
            arc = Arc(radius=R_D + 0.4, start_angle=np.radians(125), angle=-np.radians(150), arc_center=cen()).set_stroke(WHITE_, 3.2, opacity=0.95)
            arc.add_tip(tip_length=0.26)
            return VGroup(arc)
        garc = always_redraw(giro_arc)
        JC_ = mix(FC, 0.4)                               # impulso: azul da força clareado

        def seta_J():
            y = cy + cs["off"]
            return VGroup(arrow(P3(x_sup() - 1.5, y), P3(x_sup() - 0.04, y), color=JC_, width=8, tip=0.28, z=10),
                          M(r"\vec J", size=36, color=JC_).move_to(P3(x_sup() - 0.8, y + 0.5)).set_stroke(BACKGROUND_COLOR, 5, background=True))

        def rodada(off, giro, aid, fr):
            cs["off"], cs["giro"] = off, giro
            self.an(aid, fr[0])
            self.play(pp.animate.set_value(1.0), rate_func=rush_into, run_time=1.5 * LENTO)
            J = seta_J()
            self.an(aid, fr[1])
            self.play(Flash(P3(x_sup(), cy + off), color=WHITE_, line_length=0.3, flash_radius=0.18, num_lines=12, run_time=0.45),
                      FadeOut(proj, run_time=0.3), FadeIn(J, shift=0.15 * RIGHT))
            self.an(aid, fr[2])
            self.play(u.animate.set_value(1.0), rate_func=rate_functions.ease_out_cubic, run_time=2.4)
            return J

        vig = vinheta(P3(-1.0, 0.1), 4.6, VEL, 0.08)
        self.an("C14-1")
        self.play(FadeIn(vig), FadeIn(disco), FadeIn(marc), FadeIn(proj), run_time=1.0)
        self.an("C14-1", "isso significa que")
        self.play(Indicate(proj, color=WHITE_, scale_factor=1.3), run_time=1.0)
        self.an("C14-1", "mas corpos reais têm tamanho")
        self.play(Indicate(disco, color=WHITE_, scale_factor=1.08), run_time=1.0)
        # 1) impacto exatamente na direção do centro: o disco só translada
        self.an("C14-2")
        self.play(Indicate(proj, color=WHITE_, scale_factor=1.3), run_time=0.9)
        J1 = rodada(0.0, 0.0, "C14-2", ("na primeira", "bem no centro", "nesse caso"))
        # reset
        self.an("C14-3")
        self.play(FadeOut(J1), u.animate.set_value(0.0), rate_func=smooth, run_time=1.0)
        pp.set_value(0.0)
        cs["off"], cs["giro"] = OFF2, GIRO
        self.add(proj)
        self.play(FadeIn(proj), run_time=0.6)
        # 2) o mesmo impulso, deslocado do centro: translada (igual) e gira
        J2 = rodada(OFF2, GIRO, "C14-3", ("deslocado", "para um dos lados", "aí além de se mover"))
        self.add(garc)
        # congela e destaca a distância entre o centro e a linha de ação
        yl = cy + OFF2
        linha = DashedLine(P3(-7.0, yl), P3(x_sup(), yl), dash_length=0.2).set_stroke(GEO, 2.6, opacity=0.9)
        linha2 = DashedLine(P3(x_sup(), yl), P3(cen()[0] + 0.2, yl), dash_length=0.2).set_stroke(GEO, 2.0, opacity=0.4)
        cc_ = DashedLine(P3(-7.0, cy), P3(c0x - R_D - 0.5, cy), dash_length=0.2).set_stroke(GEO, 2.0, opacity=0.55)   # altura do centro
        ch_ = Line(P3(-6.4, cy), P3(-6.4, yl)).set_stroke(GEO, 3.2)
        brace = Brace(ch_, direction=LEFT, color=GEO, buff=0.06)
        dl = M("d", size=44, color=GEO).next_to(brace, LEFT, buff=0.12).set_stroke(BACKGROUND_COLOR, 5, background=True)
        self.an("C14-4")
        self.play(Create(linha), Create(linha2), Create(cc_), run_time=0.9)
        q = VGroup(txt("POR QUE O PONTO", 34, bold=True), txt("ONDE A FORÇA AGE", 34, bold=True), txt("IMPORTA?", 34, bold=True, color=CYAN)) \
            .arrange(DOWN, buff=0.15).move_to(P3(4.9, 0.4))
        self.an("C14-4", "por que a mesma força")
        self.play(FadeIn(q, shift=0.12 * UP), run_time=0.9)
        self.an("C14-4", "dependendo de onde")
        self.play(Create(ch_), GrowFromCenter(brace), FadeIn(dl), run_time=0.9)
        # cartão: o aparato fica alguns segundos e o assunto do próximo vídeo entra em ciano
        self.an("C14-5")
        self.play(FadeOut(q), Indicate(garc, color=WHITE_, scale_factor=1.03), run_time=0.9)
        k1 = txt("PRÓXIMO VÍDEO", 28, color=DIM).move_to(P3(4.9, 1.7))
        k2 = VGroup(txt("POR QUE UMA FORÇA", 32, bold=True), txt("FAZ UM CORPO GIRAR?", 32, bold=True)).arrange(DOWN, buff=0.12).move_to(P3(4.9, 0.55))
        k3 = VGroup(txt("TORQUE E DINÂMICA", 30, color=CYAN, bold=True), txt("DE ROTAÇÃO", 30, color=CYAN, bold=True)).arrange(DOWN, buff=0.12) \
            .move_to(P3(4.9, -1.0))
        self.an("C14-5", "no próximo vídeo")
        self.play(FadeIn(k1, shift=0.1 * UP), run_time=0.6)
        self.an("C14-5", "a gente vai entender por que uma força")
        self.play(FadeIn(k2, shift=0.1 * UP), run_time=0.8)
        self.an("C14-5", "e como o ponto de aplicação")
        self.play(FadeIn(k3, shift=0.1 * UP), run_time=0.8)
        self.wait(1.0)
        self.an("E1")
        for m_ in (disco, marc, vc, garc, proj):
            m_.clear_updaters()
        self.clear(rt=0.8)

    def cta(self):
        """Padrão do longo: tudo sai (inclusive tag e marca d'água), logo com anéis, inscrição, gancho, próximo vídeo."""
        self._pend = []
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        for m in self.mobjects:
            m.clear_updaters()
        Scene.clear(self)                  # nada fica atrás da logo
        oc = P3(0, 0.9)
        rings = VGroup(*[DashedVMobject(Circle(radius=r, arc_center=oc), num_dashes=max(12, int(14 * r)),
                                        dashed_ratio=0.6).set_stroke(VEL, 3.5, 0.16) for r in (2.0, 3.0, 4.0)])
        for i, r_ in enumerate(rings):
            r_.add_updater(lambda m, dt, sg=(1 if i % 2 == 0 else -1) * (0.06 - 0.01 * i): m.rotate(sg * dt, about_point=oc))
        logo = self.logo(6.0).move_to(oc + P3(0, 0.4))
        msg = txt("INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS", 28, op=0.9).move_to(oc + P3(0, -1.0))
        gancho = txt("POR QUE UMA FORÇA FAZ UM CORPO GIRAR?", 30).move_to(oc + P3(0, -1.9))
        nx1 = txt("PRÓXIMO VÍDEO:", 26, op=0.9).move_to(oc + P3(0, -1.9))
        nx2 = txt("TORQUE E DINÂMICA DE ROTAÇÃO", 32, color=CYAN, bold=True).move_to(oc + P3(0.6, -2.6))
        # o aparato do gancho: um disco com marca que gira devagar
        ic = Disco(C2F, 0.42).move_to(P3(nx2.get_left()[0] - 0.75, oc[1] - 2.6))
        ang = ValueTracker(0.0)
        marca = always_redraw(lambda: VGroup(Line(ic.c, ic.c + pol(0.34, 60 - 100 * ang.get_value())).set_stroke(WHITE_, 4, opacity=0.9),
                                             Dot(ic.c + pol(0.34, 60 - 100 * ang.get_value()), radius=0.08, color=WHITE_)).set_z_index(6))
        self.play(LaggedStart(*[FadeIn(r_, scale=0.85) for r_ in rings], lag_ratio=0.3), FadeIn(logo, scale=0.92), run_time=1.8)
        self.an("E1", "se isso ajudou você")
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=0.9)
        self.an("E2")
        self.play(FadeIn(gancho, shift=0.1 * UP), run_time=0.9)
        self.an("E2", "me conta nos comentários")
        self.play(FadeOut(gancho), FadeIn(nx1, shift=0.1 * UP), run_time=0.8)
        self.an("E2", "o que mais te surpreendeu")
        self.play(FadeIn(nx2, shift=0.1 * UP), FadeIn(ic), FadeIn(marca), ang.animate.set_value(1.0), run_time=1.4)
        self.an("E2", "valeu demais")
        w = DashedVMobject(Circle(radius=1.6, arc_center=oc), num_dashes=24, dashed_ratio=0.6).set_stroke(VEL, 3.5, 0.35)
        self.play(w.animate.scale(2.6, about_point=oc).set_stroke(opacity=0.0), ang.animate.set_value(3.0), run_time=2.4)
        self.remove(w)
        w2 = DashedVMobject(Circle(radius=1.6, arc_center=oc), num_dashes=24, dashed_ratio=0.6).set_stroke(VEL, 3.5, 0.35)
        self.play(w2.animate.scale(2.6, about_point=oc).set_stroke(opacity=0.0), ang.animate.set_value(5.0), run_time=2.4)
        self.remove(w2)
        self.wait(0.6)
