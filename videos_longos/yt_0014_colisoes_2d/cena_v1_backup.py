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

T_HL, T_MAIN, T_LAB, T_SMALL = 44, 34, 26, 22
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
def txt(s, size=T_MAIN, color=WHITE_, op=1.0, bold=False):
    """Texto editorial: Space Grotesk em CAIXA ALTA (sem símbolos matemáticos: esses vão em MathTex)."""
    s = s.upper()
    if bold:
        return official_text(s, DISPLAY_FONT, BOLD, size, oversample=2, color=color).set_opacity(op)
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(op)


def gloss(s, size=T_SMALL, op=0.7):
    """Glossário de variável (única exceção à caixa alta)."""
    return screen_text(s, size, color=WHITE_, oversample=4).set_opacity(op)


def M(*parts, size=M_MAIN, color=WHITE_, w=None):
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


def placa(w, h, centro, op=0.05):
    """Painel chato: retângulo arredondado, fundo ~5 %, borda 1,4 px."""
    frente = RoundedRectangle(corner_radius=0.12, width=w, height=h).set_stroke(WHITE_, 1.4, opacity=0.24) \
        .set_fill(WHITE_, op).move_to(centro)
    return VGroup(frente).set_z_index(-2)


def lab_at(m, a, b, lado=1, gap=0.14):
    """Rótulo ao lado de um segmento a→b (lado=+1: esquerda de a→b; −1: direita), sem encostar nele."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    d = unit(b - a)
    nrm = np.array([-d[1], d[0], 0.0]) * lado
    meia = 0.5 * (abs(nrm[0]) * m.width + abs(nrm[1]) * m.height)
    return m.move_to((a + b) / 2 + nrm * (gap + meia))


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

    def base(self, x0, x1, y0, y1, gs=0.25):
        pan = RoundedRectangle(corner_radius=0.12, width=(x1 - x0) * self.u, height=(y1 - y0) * self.u) \
            .set_stroke(DIM, 1.4, opacity=0.45).set_fill(DIM, 0.07).move_to(self.pt((x0 + x1) / 2, (y0 + y1) / 2)).set_z_index(-3)
        grade = VGroup()
        for gx in np.arange(np.ceil(x0 / gs) * gs, x1, gs):
            if x0 + 1e-6 < gx < x1 - 1e-6:
                grade.add(Line(self.pt(gx, y0), self.pt(gx, y1)).set_stroke(DIM, 1, opacity=0.13))
        for gy in np.arange(np.ceil(y0 / gs) * gs, y1, gs):
            if y0 + 1e-6 < gy < y1 - 1e-6:
                grade.add(Line(self.pt(x0, gy), self.pt(x1, gy)).set_stroke(DIM, 1, opacity=0.13))
        grade.set_z_index(-2)
        ex = arrow(self.pt(x0 + 0.03, 0), self.pt(x1 - 0.03, 0), color=DIM, width=2.5, tip=0.16, z=-1)
        ey = arrow(self.pt(0, y0 + 0.03), self.pt(0, y1 - 0.03), color=DIM, width=2.5, tip=0.16, z=-1)
        lx = M("p_{1f,x}", size=26).next_to(ex.get_end(), UP, buff=0.08)
        ly = M("p_{1f,y}", size=28).next_to(ey.get_end(), RIGHT, buff=0.12)
        return VGroup(pan, grade, ex, ey, lx, ly)


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
        self.h1 = txt("MECÂNICA · COLISÕES EM 2D", 17, color=DIM, op=0.5).to_corner(UL, buff=0.32).set_z_index(40)
        self.h2 = None
        self._pend = []
        self.add(self.wm, self.h1)
        marcas = []
        for nome in ("hook", "abertura", "c01", "c02", "c03", "c04", "c05", "c06", "c07", "c08", "c09", "c10", "c11",
                     "c12", "c13", "cta"):
            self.next_section(nome, skip_animations=bool(SECOES) and nome not in SECOES)
            t0 = self.renderer.time
            getattr(self, nome)()
            marcas.append((nome, t0, self.renderer.time))
        for nome, a, b in marcas:
            print(f"[tempo] {nome}: {a:7.1f} s -> {b:7.1f} s ({b - a:5.1f} s)")

    # ── auditoria de sobreposições (desenvolvimento: AUDITORIA=1) ─────────────────────────────────────────────
    def wait(self, duration=1.0, *a, **kw):
        if AUDITORIA:
            self._auditar()
        if STILL is not None and self.renderer.time >= STILL:     # still: com -s, salva este quadro
            from manim.utils.exceptions import EndSceneEarlyException
            raise EndSceneEarlyException()
        return super().wait(duration, *a, **kw)

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
            if isinstance(m, (Disco, Corpo)):
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
            if isinstance(m, Text):
                return f"{k}:'{m.text[:34]}'"
            if isinstance(m, SingleStringMathTex):
                return f"{k}:'{m.get_tex_string()[:34]}'"
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
        if anims and all(isinstance(a, Wait) for a in anims):
            return super().play(*anims, **kw)
        if self._pend:
            anims, self._pend = (*anims, *self._pend), []
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
    def hook(self):
        r1, r2 = 0.58, 0.3                          # corpo pesado e corpo leve
        n = pol(1.0, -HK_PHI)
        T2 = P3(0.2, 0.25)                          # alvo parado
        Tc = T2 - n * (r1 + r2)                     # disco 1 no instante do contato
        ya = Tc[1]
        eixo = DashedLine(P3(-7.0, ya), P3(0.6, ya), dash_length=0.12).set_stroke(DIM, 1.6, opacity=0.5).set_z_index(-1)
        ch = Choque(Tc, T2, P3(HK_V, 0), P3(0, 0), HK_V1F, HK_V2F, r1, r2, t0=-1.5, ka=0.5)
        self.play(Create(eixo), FadeIn(ch.group()), run_time=0.9)
        self.wait(0.8)
        self.play(ch.t.animate.set_value(0.0), rate_func=linear, run_time=1.5 * LENTO)
        self.play(ch.flash())
        ch.t.set_value(1e-5)
        self.play(ch.t.animate.set_value(0.8), rate_func=linear, run_time=1.2 * LENTO)
        self.wait(0.6)
        ch.solta()
        # a trajetória real e as direções candidatas para o disco incidente
        real = Line(Tc, ch.pos(1)).set_stroke(GEO, 2, opacity=0.55)
        cands = VGroup(*[DashedLine(Tc, Tc + pol(3.6, a), dash_length=0.14).set_stroke(VEL, 3, opacity=0.8)
                         for a in HOOK_CAND])
        self.play(Create(real), run_time=0.5)
        for c in cands:
            self.play(Create(c), run_time=0.8)
        q = self.hl("PARA ONDE ELA PODE SAIR?", y=-3.55, size=46, color=CYAN)
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.7)
        self.wait(2.0)
        self.clear(rt=0.6)

    def abertura(self):
        """Bem-vindos (logo) → título com NESTE VÍDEO (~3 s)."""
        logo = self.logo(4.6).move_to(P3(0, 0.6))
        wel = txt("BEM-VINDOS AO PARALLAX LAB", 34).move_to(P3(0, -1.3))
        self.play(FadeIn(logo, scale=0.94), FadeIn(wel, shift=0.1 * UP), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(logo), FadeOut(wel), run_time=0.5)
        tit = txt("COLISÕES EM 2D", 52, color=CYAN, bold=True).move_to(P3(0, 0.45))
        sub = txt("NESTE VÍDEO: PARA ONDE OS CORPOS PODEM SAIR", 28, op=0.85).move_to(P3(0, -0.5))
        self.play(FadeIn(tit, shift=0.1 * UP), run_time=1.0)
        self.play(FadeIn(sub, shift=0.1 * UP), run_time=0.8)
        self.wait(1.6)
        self.play(FadeOut(tit), FadeOut(sub), run_time=0.6)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C01 — retomada: a colisão em 1D era um caso especial (sem recap quantitativo)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c01(self):
        self.secao("DO 1D PARA O 2D")
        ty = 0.4
        trilho = Line(P3(-6.6, ty), P3(6.6, ty)).set_stroke(WHITE_, 2.5, opacity=0.4)
        r1, r2 = 0.36, 0.28
        ch = Choque(P3(-0.64, ty), P3(0.0, ty), P3(2.6, 0), P3(0, 0), P3(0.6, 0), P3(3.2, 0), r1, r2, t0=-1.6, ka=0.5)
        self.play(Create(trilho), FadeIn(ch.group()), run_time=0.9)
        self.play(ch.t.animate.set_value(0.0), rate_func=linear, run_time=1.6 * LENTO)
        self.play(ch.flash())
        ch.t.set_value(1e-5)
        self.play(ch.t.animate.set_value(1.6), rate_func=linear, run_time=1.6 * LENTO)
        ch.solta()
        # a linha era só um eixo: o plano em volta aparece e as outras direções ficam disponíveis
        grade = VGroup(*[Line(P3(x, -3.4), P3(x, 3.0)).set_stroke(DIM, 1, opacity=0.14) for x in np.arange(-6.5, 6.6, 1.0)],
                       *[Line(P3(-6.6, y), P3(6.6, y)).set_stroke(DIM, 1, opacity=0.14) for y in np.arange(-3.0, 3.1, 1.0)])
        o = P3(-0.3, ty)
        raios = VGroup(*[DashedLine(o, o + pol(2.3, a), dash_length=0.14).set_stroke(VEL, 2.5, opacity=0.6)
                         for a in (-70, -45, -22, 22, 45, 70)])
        self.play(FadeIn(grade), run_time=0.9)
        self.play(trilho.animate.set_stroke(WHITE_, 4, opacity=0.9), LaggedStart(*[Create(r) for r in raios], lag_ratio=0.15),
                  run_time=1.6)
        k = self.hl("1D = CASO ESPECIAL", y=-3.5, size=52)
        self.play(FadeIn(k, shift=0.1 * UP), run_time=0.7)
        self.wait(2.4)
        self.clear(rt=0.6)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C02 — o momento sempre foi um vetor: triângulo de momentos no espaço físico
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c02(self):
        self.secao("MOMENTO É UM VETOR")
        KP = 0.5
        yA = 0.85
        # ANTES: partícula 1 chega ao longo de x; 2 parada
        da1, da2 = Disco(C1F, 0.34, "m_1").move_to(P3(-6.9, yA)), Disco(C2F, 0.28, "m_2").move_to(P3(-4.2, yA))
        pia = arrow(P3(-6.9 + 0.4, yA), P3(-6.9 + 0.4 + GP1I * KP, yA), color=MAG, width=6, tip=0.2)
        lia = M(r"\vec p_{1i}", size=34).move_to(P3(-5.9, yA + 0.5))
        t_a = txt("ANTES", T_SMALL, op=0.8).move_to(P3(-5.6, 2.2))
        antes = VGroup(da1, da2, pia, lia, t_a)
        # DEPOIS: saem em direções diferentes
        oc = P3(-2.9, yA)
        dd1, dd2 = Disco(C1F, 0.34, "m_1").move_to(oc + pol(0.8, GTH1)), Disco(C2F, 0.28, "m_2").move_to(oc + pol(0.65, -GTH2))
        a1 = arrow(dd1.c + unit(GV1F) * 0.4, dd1.c + unit(GV1F) * 0.4 + GV1F * KP, color=MAG, width=6, tip=0.2)
        a2 = arrow(dd2.c + unit(GV2F) * 0.34, dd2.c + unit(GV2F) * 0.34 + GV2F * KP, color=MAG_L, width=6, tip=0.2)
        l1 = lab_at(M(r"\vec p_{1f}", size=34), a1.get_start(), a1.get_end(), lado=1)
        l2 = lab_at(M(r"\vec p_{2f}", size=34), a2.get_start(), a2.get_end(), lado=-1)
        t_d = txt("DEPOIS", T_SMALL, op=0.8).move_to(P3(-3.3, 2.2))
        depois = VGroup(dd1, dd2, a1, a2, l1, l2, t_d)
        self.play(FadeIn(antes), run_time=1.0)
        self.wait(1.0)
        self.play(FadeIn(depois), run_time=1.0)
        self.wait(1.0)
        # P_i = p_1i ; P_f = p_1f + p_2f ; logo p_1i = p_1f + p_2f
        L1 = M(r"\vec P_i", "=", r"\vec p_{1i}", size=M_REF).move_to(P3(4.3, 2.4))
        L2 = M(r"\vec P_f", "=", r"\vec p_{1f}", "+", r"\vec p_{2f}", size=M_REF).move_to(P3(4.3, 1.4))
        L3 = M(r"\vec p_{1i}", "=", r"\vec p_{1f}", "+", r"\vec p_{2f}", size=M_MID).move_to(P3(4.3, 0.0))
        self.play(Write(L1), run_time=0.9)
        self.wait(0.5)
        self.play(Write(L2), run_time=1.1)
        self.wait(0.6)
        self.play(TransformFromCopy(L1[2], L3[0]), TransformFromCopy(L2[2:], L3[2:]), FadeIn(L3[1]), run_time=1.3)
        bx = box(L3, buff=0.14)
        self.play(Create(bx), run_time=0.5)
        self.wait(1.0)
        # triângulo de momentos: p₁f e p₂f ponta com cauda até fechar em p₁ᵢ
        tr = self.triangulo(P3(-7.0, -2.35), 1.0)
        tt = txt("TRIÂNGULO DE MOMENTOS NO ESPAÇO FÍSICO", 20, op=0.85).move_to(P3(-4.1, -3.55))
        self.play(ReplacementTransform(pia.copy(), tr["pi"]), FadeIn(tr["li"]), run_time=1.0)
        self.play(ReplacementTransform(a1.copy(), tr["p1"]), FadeIn(tr["l1"]), run_time=1.0)
        self.play(ReplacementTransform(a2.copy(), tr["p2"]), FadeIn(tr["l2"]), FadeIn(tt), run_time=1.4)
        self.wait(1.2)
        n1 = VGroup(txt("NO 1D: VETORES COLINEARES", 24, op=0.85)).move_to(P3(4.3, -1.5))
        n2 = txt("NO 2D: A GEOMETRIA APARECE", 24, color=WHITE_).move_to(P3(4.3, -2.3))
        self.play(FadeIn(n1, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(n2, shift=0.1 * UP), run_time=0.6)
        self.play(Indicate(VGroup(tr["pi"], tr["p1"], tr["p2"]), color=MAG, scale_factor=1.04), run_time=1.1)
        self.wait(2.0)
        self.clear(rt=0.7)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C03 — uma conservação vetorial = duas equações escalares; ainda falta uma condição física
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c03(self):
        self.secao("DUAS EQUAÇÕES E UMA CONDIÇÃO")
        K = 1.0
        O = P3(-6.9, -1.7)
        tr = self.triangulo(O, K, labels=False)
        Q, T = tr["Q"], tr["T"]
        ex = arrow(O + P3(-0.3, 0), O + P3(5.2, 0), color=DIM, width=2.5, tip=0.16, z=2)
        ey = arrow(O + P3(0, -0.3), O + P3(0, 3.1), color=DIM, width=2.5, tip=0.16, z=2)
        lx, ly = MathTex("x", font_size=30, color=DIM).next_to(ex, RIGHT, buff=0.08), \
            MathTex("y", font_size=30, color=DIM).next_to(ey, UP, buff=0.08)
        self.play(Create(ex), Create(ey), FadeIn(lx), FadeIn(ly), run_time=0.9)
        self.play(GrowArrow(tr["pi"]), GrowArrow(tr["p1"]), GrowArrow(tr["p2"]), run_time=1.3)
        # ângulos: θ₁ acima do eixo, θ₂ abaixo do prolongamento horizontal de p₁f
        a1 = arco(O, 0.95, 0, GTH1)
        t1 = MathTex(r"\theta_1", font_size=32).move_to(O + pol(1.3, GTH1 / 2))
        prol = DashedLine(Q, P3(T[0] + 0.55, Q[1]), dash_length=0.1).set_stroke(DIM, 1.5, opacity=0.7)
        a2 = arco(Q, 0.8, -GTH2, 0)
        t2 = MathTex(r"\theta_2", font_size=32).move_to(Q + pol(1.15, -GTH2 / 2))
        self.play(Create(a1), FadeIn(t1), Create(prol), Create(a2), FadeIn(t2), run_time=1.1)
        nota = VGroup(MathTex(r"\theta_2", font_size=26), txt("MEDIDO ABAIXO DO EIXO", 18, op=0.8)).arrange(RIGHT, buff=0.12) \
            .move_to(P3(-3.3, -3.45))
        self.play(FadeIn(nota), run_time=0.5)
        self.wait(0.8)
        # componentes: x em duas chaves sob o eixo; y na vertical tracejada
        F1 = P3(Q[0], O[1])
        vert = DashedLine(Q, F1, dash_length=0.1).set_stroke(DIM, 1.5, opacity=0.8)
        bx1 = Brace(Line(O, F1), direction=DOWN, color=DIM, buff=0.08)
        bx2 = Brace(Line(F1, T), direction=DOWN, color=DIM, buff=0.08)
        cx1 = M(r"p_{1f}\cos\theta_1", size=30).next_to(bx1, DOWN, buff=0.06)
        cx2 = M(r"p_{2f}\cos\theta_2", size=30).next_to(bx2, DOWN, buff=0.06)
        bry = Brace(Line(P3(T[0] + 0.55, O[1]), P3(T[0] + 0.55, Q[1])), direction=RIGHT, color=DIM, buff=0.05)
        cy = M(r"p_{1f}\sin\theta_1", "=", r"p_{2f}\sin\theta_2", size=28).next_to(bry, RIGHT, buff=0.08)
        # equações
        tx = txt("EIXO X", 20, color=DIM).move_to(P3(1.6, 2.75))
        ex_ = M(r"p_{1i}", "=", r"p_{1f}\cos\theta_1", "+", r"p_{2f}\cos\theta_2", size=M_REF, w=6.2).move_to(P3(4.5, 2.1))
        ty_ = txt("EIXO Y", 20, color=DIM).move_to(P3(1.6, 1.0))
        ey2 = M("0", "=", r"p_{1f}\sin\theta_1", "-", r"p_{2f}\sin\theta_2", size=M_REF, w=6.2).move_to(P3(4.5, 0.35))
        self.play(Create(vert), GrowFromCenter(bx1), GrowFromCenter(bx2), FadeIn(cx1), FadeIn(cx2), run_time=1.1)
        self.play(FadeIn(tx), Write(ex_), run_time=1.2)
        self.wait(0.6)
        self.play(GrowFromCenter(bry), FadeIn(cy), run_time=0.8)
        self.play(FadeIn(ty_), Write(ey2), run_time=1.2)
        self.wait(1.0)
        h = VGroup(txt("UMA CONSERVAÇÃO VETORIAL", 26), M(r"\Downarrow", size=40), txt("DUAS EQUAÇÕES ESCALARES", 26)) \
            .arrange(DOWN, buff=0.1).move_to(P3(4.5, -1.7))
        self.play(FadeIn(h, shift=0.1 * UP), run_time=0.9)
        self.wait(2.0)
        self.clear(rt=0.7)
        # ainda falta uma condição física
        falta = self.hl("MAS AINDA FALTA UMA CONDIÇÃO FÍSICA", y=2.55, size=40)
        self.play(FadeIn(falta, shift=0.1 * UP), run_time=0.8)
        cards = []
        conteudo = ((r"ELÁSTICA", M("K_i", "=", "K_f", size=M_REF)),
                    ("COMPLETAMENTE INELÁSTICA", M(r"\vec v_{1f}", "=", r"\vec v_{2f}", size=M_REF)),
                    ("OUTRO CASO", txt("CONDIÇÃO DADA", 22)))
        for i, (tt_, eq) in enumerate(conteudo):
            x = (-5.1, 0.0, 5.1)[i]
            p = placa(4.6, 2.3, P3(x, 0.4))
            ti = txt(tt_, 20, op=0.9).move_to(P3(x, 1.15))
            eq.move_to(P3(x, -0.1))
            cards.append(VGroup(p, ti, eq))
        for c in cards:
            self.play(FadeIn(c, shift=0.1 * UP), run_time=0.7)
            self.wait(0.8)
        sint = self.hl("MOMENTO + CONDIÇÃO FÍSICA", y=-2.2, size=52, color=CYAN)
        self.play(FadeIn(sint, shift=0.1 * UP), run_time=0.8)
        self.wait(2.2)
        self.clear(rt=0.7)

    # ── SEÇÕES SEGUINTES ────────────────────────────────────────────────────────────────────────────────────
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C04 — massas iguais, alvo parado, elástica: por que surgem 90°?
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c04(self):
        self.secao("MASSAS IGUAIS: O ÂNGULO RETO")
        hip = VGroup(M(r"m_1=m_2=m,\ v_{2i}=0", size=32), txt("ELÁSTICA", 20, op=0.9)).arrange(RIGHT, buff=0.5) \
            .move_to(P3(4.4, 3.2))
        r, KV, yA = 0.32, 0.45, 1.3
        v1i = 3.1                                         # |v₁ᵢ| em unidades de velocidade (setas = KV por unidade)
        a1 = P3(-6.9, yA)
        da1, da2 = Disco(C1F, r, "m_1").move_to(a1), Disco(C2F, r, "m_2").move_to(P3(-4.6, yA))
        sa = arrow(a1 + RIGHT * (r + 0.06), a1 + RIGHT * (r + 0.06 + v1i * KV), color=VEL, width=4, tip=0.17)
        la = lab_at(M(r"\vec v_{1i}", size=32), sa.get_start(), sa.get_end(), lado=1)
        antes = VGroup(da1, da2, sa, la, txt("ANTES", T_SMALL, op=0.8).move_to(P3(-5.8, 2.3)))
        oc = P3(-2.6, yA)
        e1, e2 = pol(1.0, 30), pol(1.0, -60)
        dd1, dd2 = Disco(C1F, r, "m_1").move_to(oc + e1 * 0.85), Disco(C2F, r, "m_2").move_to(oc + e2 * 0.85)
        v1f_, v2f_ = v1i * np.cos(np.radians(30)), v1i * np.sin(np.radians(30))
        s1 = arrow(dd1.c + e1 * (r + 0.06), dd1.c + e1 * (r + 0.06 + v1f_ * KV), color=VEL, width=4, tip=0.17)
        s2 = arrow(dd2.c + e2 * (r + 0.06), dd2.c + e2 * (r + 0.06 + v2f_ * KV), color=VEL, width=4, tip=0.17)
        l1 = lab_at(M(r"\vec v_{1f}", size=32), s1.get_start(), s1.get_end(), lado=1)
        l2 = lab_at(M(r"\vec v_{2f}", size=32), s2.get_start(), s2.get_end(), lado=-1)
        depois = VGroup(dd1, dd2, s1, s2, l1, l2, txt("DEPOIS", T_SMALL, op=0.8).move_to(P3(-3.3, 2.3)))
        self.play(FadeIn(hip, shift=0.1 * UP), run_time=0.9)
        self.play(FadeIn(antes), run_time=0.8)
        self.play(FadeIn(depois), run_time=0.8)
        self.wait(1.0)
        # (1) momento: as massas cortam
        E1 = M("m", r"\vec v_{1i}", "=", "m", r"\vec v_{1f}", "+", "m", r"\vec v_{2f}", size=M_REF, w=6.4).move_to(P3(4.4, 2.55))
        E1b = M(r"\vec v_{1i}", "=", r"\vec v_{1f}", "+", r"\vec v_{2f}", size=M_REF).move_to(P3(4.4, 2.55))
        self.play(Write(E1), run_time=1.2)
        self.wait(0.6)
        self.play(TransformMatchingTex(E1, E1b), run_time=1.1)
        self.settle(E1b)
        self.wait(0.5)
        # triângulo de velocidades (ponta com cauda); Q desliza até o ângulo reto mais adiante
        O, L = P3(-6.9, -3.35), 4.6
        d = ValueTracker(2.9)
        Q = lambda: O + pol(d.get_value(), 30)       # noqa: E731
        T = O + P3(L, 0)
        ti = arrow(O, T, color=VEL, width=6, tip=0.22)
        t1 = always_redraw(lambda: arrow(O, Q(), color=VEL, width=4.5, tip=0.2))
        t2 = always_redraw(lambda: arrow(Q(), T, color=mix(VEL, 0.3), width=4.5, tip=0.2))
        li = lab_at(M(r"\vec v_{1i}", size=32), O, T, lado=-1)
        lt1 = M(r"\vec v_{1f}", size=32).add_updater(lambda m: lab_at(m, O, Q(), lado=1))
        lt2 = M(r"\vec v_{2f}", size=32).add_updater(lambda m: lab_at(m, Q(), T, lado=1))

        def arco_q():
            q = Q()
            a0 = np.degrees(np.arctan2(*(T - q)[1::-1]))
            a1_ = np.degrees(np.arctan2(*(O - q)[1::-1]))
            return arco(q, 0.38, a1_, a0 if a0 > a1_ else a0 + 360)
        aq = always_redraw(arco_q)
        self.play(GrowArrow(ti), FadeIn(li), run_time=0.8)
        self.play(GrowArrow(t1), FadeIn(lt1), run_time=0.8)
        self.play(GrowArrow(t2), FadeIn(lt2), run_time=0.8)
        self.wait(0.8)
        # (2) energia
        ea = M("K_i", "=", "K_f", size=M_REF).move_to(P3(4.4, 1.55))
        tg = txt("ELÁSTICA", 18, color=DIM).move_to(P3(1.5, 2.0))
        eb = M(r"\tfrac12 m", "v_{1i}^2", "=", r"\tfrac12 m", "v_{1f}^2", "+", r"\tfrac12 m", "v_{2f}^2", size=M_REF, w=6.4) \
            .move_to(P3(4.4, 1.55))
        ec = M("v_{1i}^2", "=", "v_{1f}^2", "+", "v_{2f}^2", size=M_REF).move_to(P3(4.4, 1.55))
        self.play(FadeIn(tg), Write(ea), run_time=0.9)
        self.wait(0.5)
        self.play(TransformMatchingTex(ea, eb), run_time=1.1)
        self.settle(eb)
        self.wait(0.4)
        self.play(TransformMatchingTex(eb, ec), run_time=1.1)
        self.settle(ec)
        self.wait(0.6)
        # (3) a relação vetorial ao quadrado
        sq = txt("ELEVE AO QUADRADO", 18, color=DIM).move_to(P3(1.7, 0.95))
        e3a = M("(", r"\vec v_{1i}", ")^2", "=", "(", r"\vec v_{1f}", "+", r"\vec v_{2f}", ")^2", size=M_REF).move_to(P3(4.4, 0.45))
        e3b = M("v_{1i}^2", "=", "v_{1f}^2", "+", "v_{2f}^2", "+", "2", r"\vec v_{1f}", r"\cdot", r"\vec v_{2f}", size=M_REF, w=6.4) \
            .move_to(P3(4.4, 0.45))
        self.play(FadeIn(sq), Write(e3a), run_time=1.0)
        self.wait(0.5)
        self.play(TransformMatchingTex(e3a, e3b), run_time=1.3)
        self.settle(e3b)
        self.wait(0.6)
        # (4) comparar: sobra o termo cruzado, que precisa ser zero
        extra = VGroup(*e3b[5:])
        bx = box(extra, color=WHITE_, buff=0.08)
        e4 = M("2", r"\vec v_{1f}", r"\cdot", r"\vec v_{2f}", "=", "0", size=M_REF).move_to(P3(4.4, -0.6))
        self.play(Create(bx), run_time=0.5)
        self.play(TransformFromCopy(e3b[6:], e4[:4]), FadeIn(e4[4:]), run_time=1.2)
        self.wait(0.6)
        e5 = M(r"\vec v_{1f}", r"\perp", r"\vec v_{2f}", size=M_MID).move_to(P3(4.4, -1.7))
        b5 = box(e5, buff=0.14)
        self.play(Write(e5), Create(b5), run_time=1.0)
        # o ângulo no triângulo vira reto; os dois vetores da colisão ficam perpendiculares
        self.add(aq)
        self.play(FadeIn(aq), run_time=0.3)
        self.play(d.animate.set_value(L * np.cos(np.radians(30))), run_time=2.0)
        rq = reto(Q(), O - Q(), T - Q(), s=0.28)
        self.remove(aq)
        aq.clear_updaters()
        self.add(rq)
        raios = VGroup(DashedLine(oc, oc + e1 * 1.7, dash_length=0.1).set_stroke(DIM, 1.5, opacity=0.7),
                       DashedLine(oc, oc + e2 * 1.7, dash_length=0.1).set_stroke(DIM, 1.5, opacity=0.7),
                       reto(oc, e1, e2, s=0.3))
        self.play(Create(raios), run_time=0.9)
        self.wait(0.8)
        # ressalva e condições simultâneas
        res = VGroup(M(r"\vec v_{1f}=\vec 0", size=28), txt("(FRONTAL) TAMBÉM ZERA O PRODUTO", 18, op=0.85)) \
            .arrange(RIGHT, buff=0.2).move_to(P3(4.4, -2.55))
        res2 = txt("NO DESVIO OBLÍQUO, NENHUM MÓDULO É NULO", 18, op=0.85).move_to(P3(4.4, -2.95))
        self.play(FadeIn(res, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(res2, shift=0.1 * UP), run_time=0.6)
        chips = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.16, width=w_, height=0.45).set_stroke(CYAN, 1.4, 0.7)
                                .set_fill(WHITE_, 0.04), txt(s_, 18)) for s_, w_ in
                         (("ELÁSTICA", 1.7), ("MASSAS IGUAIS", 2.2), ("ALVO PARADO", 2.0))])
        for c_ in chips:
            c_[1].move_to(c_[0])
        chips.arrange(RIGHT, buff=0.18).move_to(P3(4.4, -3.65))
        for c_ in chips:
            self.play(FadeIn(c_, shift=0.1 * UP), run_time=0.45)
        self.wait(2.2)
        for m_ in (t1, t2, lt1, lt2):
            m_.clear_updaters()
        self.clear(rt=0.7)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C05 — bilhar: aplicação do ângulo reto
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c05(self):
        self.secao("BILHAR")
        mesa = RoundedRectangle(corner_radius=0.2, width=7.8, height=4.3).set_stroke(DIM, 2.5, opacity=0.8) \
            .set_fill(WHITE_, 0.03).move_to(P3(-3.8, -0.35)).set_z_index(-2)
        assert abs(10 * np.cos(np.radians(30)) - 5 * np.sqrt(3)) < 1e-12 and abs(10 * np.sin(np.radians(30)) - 5) < 1e-12
        r = 0.32
        n = pol(1.0, -60)
        C1c = P3(-4.7, -0.05)
        C2c = C1c + n * (2 * r)
        vi = 2.6
        v2f = vi * 0.5 * n
        v1f = P3(vi, 0) - v2f
        ch = Choque(C1c, C2c, P3(vi, 0), P3(0, 0), v1f, v2f, r, r, t0=-1.0, ka=0.5)
        eixo = DashedLine(P3(-7.4, C1c[1]), C1c, dash_length=0.12).set_stroke(DIM, 1.5, opacity=0.6).set_z_index(-1)
        card = VGroup(M(r"v_{1i}=10\ \mathrm{m/s}", size=40), txt("ELÁSTICA", 20, op=0.9)).arrange(RIGHT, buff=0.5).move_to(P3(4.3, 2.55))
        card2 = M(r"m_1=m_2,\ v_{2i}=0,\ \theta_1=30^\circ", size=38, w=6.4).move_to(P3(4.3, 1.65))
        ref = txt("EXERCÍCIO DE REFERÊNCIA", 18, color=DIM).move_to(P3(4.3, 3.2))
        self.play(FadeIn(mesa), Create(eixo), FadeIn(ch.group()), FadeIn(ref), run_time=1.0)
        self.play(FadeIn(card, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(card2, shift=0.1 * UP), run_time=0.6)
        self.wait(0.6)
        self.play(ch.t.animate.set_value(0.0), rate_func=linear, run_time=1.0 * LENTO)
        self.play(ch.flash())
        ch.t.set_value(1e-5)
        self.play(ch.t.animate.set_value(1.0), rate_func=linear, run_time=1.0 * LENTO)
        ch.solta()
        # ângulos medidos a partir do eixo de incidência
        p1, p2 = ch.pos(1), ch.pos(2)
        tr1 = Line(C1c, p1).set_stroke(GEO, 1.8, opacity=0.5).set_z_index(-1)
        tr2 = Line(C2c, p2).set_stroke(GEO, 1.8, opacity=0.5).set_z_index(-1)
        ref1 = DashedLine(C1c, C1c + P3(2.3, 0), dash_length=0.1).set_stroke(DIM, 1.4, opacity=0.6).set_z_index(-1)
        ref2 = DashedLine(C2c, C2c + P3(1.8, 0), dash_length=0.1).set_stroke(DIM, 1.4, opacity=0.6).set_z_index(-1)
        a1 = arco(C1c, 1.0, 0, 30)
        a2 = arco(C2c, 0.75, -60, 0)
        t1 = MathTex(r"\theta_1", font_size=30).move_to(C1c + pol(1.35, 15))
        t2 = MathTex(r"\theta_2", font_size=30).move_to(C2c + pol(1.05, -30))
        self.play(Create(tr1), Create(tr2), Create(ref1), Create(ref2), run_time=0.7)
        self.play(Create(a1), FadeIn(t1), Create(a2), FadeIn(t2), run_time=0.9)
        self.wait(0.6)
        # solução
        s1 = M(r"\theta_1+\theta_2=90^\circ", r"\;\Rightarrow\;", r"\theta_2=60^\circ", size=M_REF, w=6.4).move_to(P3(4.3, 0.45))
        s2 = M(r"v_{1f}", "=", r"v_{1i}\cos30^\circ", "=", r"5\sqrt3\ \mathrm{m/s}", size=M_REF, w=6.4).move_to(P3(4.3, -0.65))
        s3 = M(r"v_{2f}", "=", r"v_{1i}\sin30^\circ", "=", r"5\ \mathrm{m/s}", size=M_REF, w=6.4).move_to(P3(4.3, -1.75))
        self.play(Write(s1), run_time=1.4)
        self.wait(0.8)
        # triângulo retângulo com hipotenusa v₁ᵢ
        grp = VGroup(mesa, ch.d1, ch.d2, ch.setas, eixo, tr1, tr2, ref1, ref2, a1, a2, t1, t2)
        self.play(FadeOut(grp), run_time=0.6)
        for m_ in grp:
            m_.clear_updaters()
        self.remove(*grp)
        K = 0.6
        O = P3(-7.0, -2.3)
        T = O + P3(10 * K, 0)
        Q = O + pol(5 * np.sqrt(3) * K, 30)
        hi = arrow(O, T, color=VEL, width=6, tip=0.22)
        h1 = arrow(O, Q, color=VEL, width=4.5, tip=0.2)
        h2 = arrow(Q, T, color=mix(VEL, 0.3), width=4.5, tip=0.2)
        li = lab_at(M(r"v_{1i}=10", size=30), O, T, lado=-1)
        l1 = lab_at(M(r"v_{1f}=5\sqrt3", size=30), O, Q, lado=1)
        l2 = lab_at(M(r"v_{2f}=5", size=30), Q, T, lado=1)
        rq = reto(Q, O - Q, T - Q, s=0.28)
        ta = arco(O, 0.9, 0, 30)
        tb = arco(T, 0.8, 180 - 60, 180)
        tha = MathTex(r"30^\circ", font_size=26).move_to(O + pol(1.35, 15))
        thb = MathTex(r"60^\circ", font_size=26).move_to(T + pol(1.2, 180 - 30))
        self.play(GrowArrow(hi), FadeIn(li), run_time=0.8)
        self.play(GrowArrow(h1), FadeIn(l1), Create(ta), FadeIn(tha), run_time=0.9)
        self.play(GrowArrow(h2), FadeIn(l2), Create(tb), FadeIn(thb), Create(rq), run_time=1.0)
        self.play(Write(s2), run_time=1.3)
        self.wait(0.5)
        self.play(Write(s3), run_time=1.3)
        self.wait(2.2)
        self.clear(rt=0.7)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C06 — massas diferentes: a perpendicularidade não vale; sai a quadrática em p₁f (com λ = m₂/m₁)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c06(self):
        self.secao("MASSAS DIFERENTES")
        chip = VGroup(Disco(C1F, 0.28, "m_1"), Disco(C2F, 0.2, "m_2"), M(r"m_1\neq m_2", size=34),
                      txt("A PERPENDICULARIDADE NÃO VALE", 20, op=0.9)).arrange(RIGHT, buff=0.3).move_to(P3(-3.8, 2.4))
        K = 1.3
        O = P3(-7.0, -0.6)
        tr = self.triangulo(O, K, size=34)
        th = arco(O, 0.95, 0, GTH1)
        tht = MathTex(r"\theta_1", font_size=32).move_to(O + pol(1.35, GTH1 / 2))
        self.play(FadeIn(chip, shift=0.1 * UP), run_time=0.9)
        self.play(GrowArrow(tr["pi"]), GrowArrow(tr["p1"]), GrowArrow(tr["p2"]), FadeIn(tr["li"]), FadeIn(tr["l1"]),
                  FadeIn(tr["l2"]), Create(th), FadeIn(tht), run_time=1.6)
        self.wait(0.7)
        # lei dos cossenos
        r1 = M(r"\vec p_{2f}", "=", r"\vec p_{1i}", "-", r"\vec p_{1f}", size=40).move_to(P3(4.3, 3.05))
        r2 = M(r"p_{2f}^2", "=", r"p_{1i}^2", "+", r"p_{1f}^2", "-2", "p_{1i}", "p_{1f}", r"\cos\theta_1", size=40, w=6.4) \
            .move_to(P3(4.3, 2.1))
        self.play(Write(r1), run_time=1.0)
        self.wait(0.4)
        self.play(Write(r2), run_time=1.4)
        self.wait(0.8)
        # energia: elástica
        tg = txt("ELÁSTICA", 18, color=DIM).move_to(P3(1.4, 1.5))
        r3 = M(r"\frac{p_{1i}^2}{2m_1}=\frac{p_{1f}^2}{2m_1}+\frac{p_{2f}^2}{2m_2}", size=40, w=6.4).move_to(P3(4.3, 0.85))
        r3.set_color(CYAN)
        r4 = M(r"p_{2f}^2", "=", r"\lambda", "(", r"p_{1i}^2", "-", r"p_{1f}^2", ")", size=40).move_to(P3(4.3, 0.85))
        lam = VGroup(M(r"\lambda=\frac{m_2}{m_1}", size=40), txt("RAZÃO DAS MASSAS", 18, color=DIM)).arrange(DOWN, buff=0.15) \
            .move_to(P3(-4.1, -2.35))
        self.play(FadeIn(tg), Write(r3), run_time=1.4)
        self.wait(0.8)
        self.play(FadeIn(lam, shift=0.1 * UP), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(r3), FadeIn(r4), run_time=1.0)
        self.wait(0.6)
        # igualar os dois p₂f²
        self.play(FadeOut(r1), FadeOut(tg), run_time=0.4)
        r5 = M(r"p_{1i}^2", "+", r"p_{1f}^2", "-2", "p_{1i}", "p_{1f}", r"\cos\theta_1", "=", r"\lambda", "(", r"p_{1i}^2", "-",
               r"p_{1f}^2", ")", size=40, w=6.6).move_to(P3(4.3, -0.4))
        self.play(TransformFromCopy(r2[2:], r5[:7]), TransformFromCopy(r4[2:], r5[8:]), FadeIn(r5[7]), run_time=1.5)
        self.wait(0.8)
        r6 = M(r"(1+\lambda)", r"p_{1f}^2", "-2", "p_{1i}", r"\cos\theta_1", "p_{1f}", r"+(1-\lambda)", r"p_{1i}^2", "=0",
               size=M_REF, w=6.6).move_to(P3(4.3, -1.8))
        self.play(TransformMatchingTex(r5.copy(), r6), run_time=1.6)
        self.settle(r6)
        b6 = box(r6, buff=0.14)
        self.play(Create(b6), run_time=0.5)
        self.wait(0.8)
        q1 = txt("O QUE ESSA EQUAÇÃO DIZ, GEOMETRICAMENTE, SOBRE", 24).move_to(P3(0, -3.35))
        q2 = txt("TODOS OS MOMENTOS FINAIS POSSÍVEIS?", 24, color=CYAN).move_to(P3(0, -3.78))
        self.play(FadeIn(VGroup(q1, q2), shift=0.1 * UP), run_time=0.8)
        self.wait(1.8)
        # a quadrática e a pergunta ficam para C07
        self.q06 = VGroup(r6, b6)
        self.pq = VGroup(q1, q2)
        self.clear(r6, b6, self.pq, rt=0.7)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C07 — a quadrática é um círculo (troca explícita de plano: espaço físico → plano de p₁f)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c07(self):
        self.secao("A QUADRÁTICA É UM CÍRCULO")
        r6, b6 = self.q06
        lam = LAM_EX
        C, R = lam_cr(lam)
        # ── fase A: álgebra, largura total; a pergunta de C06 fica até o círculo nascer ─────────────────────────
        def nota(*partes):
            g = VGroup(*partes).arrange(RIGHT, buff=0.15)
            return g.move_to(P3(0, 2.5))

        E1 = M(r"(1+\lambda)", "p_{1f}^2", "-2", r"\vec p_{1i}", r"\cdot", r"\vec p_{1f}", r"+(1-\lambda)", "p_{1i}^2", "=0",
               size=M_REF).move_to(P3(0, 1.3))
        E2 = M("p_{1f}^2", r"-\frac{2}{1+\lambda}", r"\vec p_{1i}", r"\cdot", r"\vec p_{1f}", r"+\frac{1-\lambda}{1+\lambda}",
               "p_{1i}^2", "=0", size=M_REF).move_to(P3(0, 1.3))
        E3 = M(r"\Bigl|", r"\vec p_{1f}", r"-\frac{\vec p_{1i}}{1+\lambda}", r"\Bigr|^2", "=",
               r"\Bigl(\frac{\lambda\,p_{1i}}{1+\lambda}\Bigr)^2", size=M_REF).move_to(P3(0, 1.3))
        n1 = nota(txt("O PRODUTO ESCALAR APARECE", 20, color=DIM))
        self.play(FadeOut(b6), r6.animate.scale(1.25).move_to(P3(0, 1.3)), run_time=1.0)
        self.wait(0.6)
        E1.move_to(r6)
        self.play(TransformMatchingTex(r6, E1), FadeIn(n1, shift=0.1 * UP), run_time=1.4)
        self.settle(E1)
        self.wait(1.2)
        n2 = nota(txt("DIVIDA POR", 20, color=DIM), M(r"(1+\lambda)", size=26))
        self.play(TransformMatchingTex(E1, E2), FadeOut(n1), FadeIn(n2, shift=0.1 * UP), run_time=1.5)
        self.settle(E2)
        self.wait(1.2)
        n3 = nota(txt("COMPLETE O QUADRADO", 20, color=DIM))
        self.play(TransformMatchingTex(E2, E3), FadeOut(n2), FadeIn(n3, shift=0.1 * UP), run_time=1.8)
        self.settle(E3)
        b3 = box(E3, buff=0.15)
        self.play(Create(b3), run_time=0.5)
        self.wait(1.8)
        # ── fase B: troca de plano ──────────────────────────────────────────────────────────────────────────────
        pl = Plano(P3(-7.3, -0.7), 7.6)
        self.pl07 = pl
        painel = pl.base(-0.07, 1.09, -0.36, 0.4)
        tagp = self.tag_plano(False).move_to(pl.pt(0.62, 0.4) + P3(0, -0.35))
        T = pl.pt(1, 0)
        p1i = arrow(pl.O, T, color=MAG, width=8, tip=0.24)
        lpi = lab_at(M(r"\vec p_{1i}", size=34), pl.O, T, lado=-1)
        ctr = pl.pt(C, 0)
        circ = Circle(radius=R * pl.u).move_to(ctr).set_stroke(CYAN, 3.5).set_fill(CYAN, 0.07).set_z_index(3)
        dc = ponto(ctr, GEO, 0.08)
        lc = M(r"C", size=32, color=GEO).next_to(dc, DOWN, buff=0.12)
        rad = Line(ctr, ctr + P3(0, R * pl.u)).set_stroke(GEO, 2.2).set_z_index(4)
        lr = M(r"R", size=32, color=GEO).next_to(rad, LEFT, buff=0.1)
        E3.generate_target()
        E3.target.scale_to_fit_width(6.0).move_to(P3(4.5, 2.55))
        b3.generate_target()
        b3.target = box(E3.target, buff=0.12)
        self.play(FadeOut(self.pq), FadeOut(n3), MoveToTarget(E3), MoveToTarget(b3), run_time=1.2)
        self.play(FadeIn(painel, scale=0.97), FadeIn(tagp), run_time=1.0)
        self.wait(0.5)
        self.play(GrowArrow(p1i), FadeIn(lpi), run_time=1.0)
        self.wait(0.4)
        self.play(Create(circ), run_time=1.6)
        self.play(FadeIn(dc), FadeIn(lc), Create(rad), FadeIn(lr), run_time=0.9)
        eC = M(r"\vec C", "=", r"\frac{\vec p_{1i}}{1+\lambda}", size=M_REF).move_to(P3(4.5, 1.2))
        eC[0].set_color(GEO)
        eR = M("R", "=", r"\frac{\lambda\,p_{1i}}{1+\lambda}", size=M_REF).move_to(P3(4.5, -0.2))
        eR[0].set_color(GEO)
        self.play(Write(eC), run_time=1.1)
        self.play(Write(eR), run_time=1.1)
        self.wait(0.8)
        # cada ponto do círculo é um p₁f possível, e p₂f fecha o triângulo: um ponto determina os dois
        a0 = lambda: np.degrees(np.arctan2(*(P3(_PH0[0] - C, _PH0[1]))[1::-1]))     # noqa: E731
        ph = ValueTracker(float(a0()))
        T_ = T

        def vet():
            a = np.radians(ph.get_value())
            P = pl.pt(C + R * np.cos(a), R * np.sin(a))
            return VGroup(arrow(pl.O, P, color=MAG, width=6, tip=0.2, z=7),
                          arrow(P, T_, color=MAG_L, width=6, tip=0.2, z=7), ponto(P, WHITE_, 0.09, z=9))

        def pos_a(m, k):
            a = np.radians(ph.get_value())
            P = pl.pt(C + R * np.cos(a), R * np.sin(a))
            return lab_at(m, pl.O, P, lado=1) if k == 1 else lab_at(m, P, T_, lado=1)
        v = always_redraw(vet)
        l1 = M(r"\vec p_{1f}", size=32).add_updater(lambda m: pos_a(m, 1))
        l2 = M(r"\vec p_{2f}", size=32).add_updater(lambda m: pos_a(m, 2))
        t1 = VGroup(txt("CADA PONTO DO CÍRCULO", 22), VGroup(txt("É UM", 22), M(r"\vec p_{1f}", size=32), txt("POSSÍVEL", 22))
                    .arrange(RIGHT, buff=0.16)).arrange(DOWN, buff=0.14).move_to(P3(4.5, -1.55))
        t2 = VGroup(txt("UM PONTO DETERMINA", 22), VGroup(txt("OS DOIS", 22), M(r"\vec p_{1f}", size=32), txt("E", 22),
                                                          M(r"\vec p_{2f}", size=32)).arrange(RIGHT, buff=0.16)) \
            .arrange(DOWN, buff=0.14).move_to(P3(4.5, -2.85))
        self.play(FadeIn(v), FadeIn(l1), FadeIn(l2), FadeIn(t1, shift=0.1 * UP), run_time=1.0)
        self.wait(0.8)
        self.play(ph.animate.set_value(float(a0()) + 55), run_time=2.4)
        self.play(FadeIn(t2, shift=0.1 * UP), run_time=0.7)
        self.play(ph.animate.set_value(float(a0()) - 70), run_time=3.0)
        self.play(ph.animate.set_value(float(a0())), run_time=2.0)
        self.wait(1.2)
        # estado entregue ao C08
        for m_ in (l1, l2):
            m_.clear_updaters()
        v.clear_updaters()
        self.dir07 = VGroup(E3, b3, eC, eR, t1, t2)
        self.vec07 = VGroup(v, l1, l2)
        self.base07 = VGroup(painel, tagp, p1i, lpi, circ, dc, lc, rad, lr)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C08 — o círculo une 1D, 2D e o ângulo máximo; fecha o hook
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c08(self):
        self.secao("DIREÇÕES POSSÍVEIS")
        pl, lam = self.pl07, LAM_EX
        C, R = lam_cr(lam)
        self.play(FadeOut(self.dir07), FadeOut(self.vec07), run_time=0.8)
        self.remove(self.dir07, self.vec07)
        # ── (a) 1D, sem recap: o eixo corta o círculo em dois pontos ───────────────────────────────────────────
        A, B = pl.pt(1, 0), pl.pt((1 - lam) / (1 + lam), 0)
        dA, dB = ponto(A, WHITE_, 0.1, z=9), ponto(B, WHITE_, 0.1, z=9)
        lA = M("A", size=34).next_to(A, DOWN, buff=0.22)
        lB = M("B", size=34).next_to(B, DOWN, buff=0.22)
        rowA = VGroup(M("A", size=36), M(r"p_{1f}=p_{1i}", size=40)).arrange(RIGHT, buff=0.4)
        subA = txt("NADA MUDOU", 20, op=0.85)
        gA = VGroup(rowA, subA).arrange(DOWN, buff=0.15).move_to(P3(4.5, 2.4))
        rowB = VGroup(M("B", size=36), M(r"p_{1f}=\frac{m_1-m_2}{m_1+m_2}\,p_{1i}", size=40)).arrange(RIGHT, buff=0.4)
        subB = txt("COLISÃO FRONTAL EM 1D", 20, op=0.85)
        gB = VGroup(rowB, subB).arrange(DOWN, buff=0.15).move_to(P3(4.5, 0.6))
        eixo = Line(pl.pt(0, 0), A).set_stroke(WHITE_, 3, opacity=0.9).set_z_index(5)
        self.play(Create(eixo), run_time=0.8)
        self.play(FadeIn(dA), FadeIn(lA), FadeIn(gA, shift=0.1 * UP), Flash(A, color=WHITE_, line_length=0.2, flash_radius=0.15,
                                                                           num_lines=8, run_time=0.5), run_time=0.9)
        self.wait(1.2)
        self.play(FadeIn(dB), FadeIn(lB), FadeIn(gB, shift=0.1 * UP), Flash(B, color=WHITE_, line_length=0.2, flash_radius=0.15,
                                                                           num_lines=8, run_time=0.5), run_time=0.9)
        self.wait(1.8)
        self.play(FadeOut(gA), FadeOut(gB), FadeOut(eixo), FadeOut(dA), FadeOut(dB), FadeOut(lA), FadeOut(lB), run_time=0.7)
        # ── (b) direções oblíquas: semirreta saindo da origem ───────────────────────────────────────────────────
        th = ValueTracker(5.0)
        thm = float(np.degrees(np.arcsin(lam)))

        def raio_len(t):
            sn = np.sin(np.radians(t))
            return min(7.9, (2.2 - pl.O[1]) / sn) if sn > 1e-6 else 7.9

        def geo():
            t = th.get_value()
            a = np.radians(t)
            g = VGroup(DashedLine(pl.O, pl.O + pol(raio_len(t), t), dash_length=0.14).set_stroke(GEO, 2.2, opacity=0.8).set_z_index(5),
                       arco(pl.O, 1.3, 0, t, w=1.8).set_z_index(5))
            s_ = R * R - (C * np.sin(a)) ** 2
            if s_ > -1e-9:
                q = np.sqrt(max(s_, 0.0))
                dp, dm = C * np.cos(a) + q, C * np.cos(a) - q
                Pp, Pm = pl.O + pol(dp * pl.u, t), pl.O + pol(dm * pl.u, t)
                if q > 2e-3:
                    g.add(arrow(pl.O, Pp, color=MAG_L, width=4.5, tip=0.18, z=7), arrow(pl.O, Pm, color=MAG, width=7, tip=0.2, z=8),
                          ponto(Pp, WHITE_, 0.09, z=9), ponto(Pm, WHITE_, 0.09, z=9))
                else:
                    g.add(arrow(pl.O, Pp, color=MAG, width=7, tip=0.2, z=8), ponto(Pp, WHITE_, 0.11, z=9))
            return g
        gg = always_redraw(geo)
        lth = M(r"\theta_1", size=30).add_updater(lambda m: m.move_to(pl.O + pol(1.9, th.get_value() + 8)))
        rd = VGroup(M(r"\theta_1=", size=40), DecimalPT(5.0, num_decimal_places=1, unit=r"^\circ", font_size=40)).arrange(RIGHT, buff=0.15) \
            .move_to(P3(4.5, 2.7))
        rd[1].add_updater(lambda m: m.set_value(th.get_value()))
        rd[1].add_updater(lambda m: m.next_to(rd[0], RIGHT, buff=0.15))
        r2 = VGroup(txt("DOIS JEITOS DE BATER,", 24), txt("O MESMO DESVIO", 24)).arrange(DOWN, buff=0.12).move_to(P3(4.5, 1.1))
        r1 = VGroup(txt("TANGÊNCIA: AS DUAS", 24, color=CYAN), txt("SOLUÇÕES SE FUNDEM", 24, color=CYAN)).arrange(DOWN, buff=0.12) \
            .move_to(P3(4.5, 1.1))
        r0 = VGroup(txt("SEM INTERSEÇÃO:", 24), txt("SEM SOLUÇÃO FÍSICA", 24)).arrange(DOWN, buff=0.12).move_to(P3(4.5, 1.1))
        r2.add_updater(lambda m: m.set_opacity(1.0 if th.get_value() < thm - 0.05 else 0.0))
        r1.add_updater(lambda m: m.set_opacity(1.0 if abs(th.get_value() - thm) <= 0.05 else 0.0))
        r0.add_updater(lambda m: m.set_opacity(1.0 if th.get_value() > thm + 0.05 else 0.0))
        self.add(r2, r1, r0)
        self.play(FadeIn(gg), FadeIn(lth), FadeIn(rd), run_time=1.0)
        self.wait(1.4)
        self.play(th.animate.set_value(10.0), run_time=2.2)
        self.wait(1.0)
        self.play(th.animate.set_value(thm - 0.6), run_time=3.0)
        self.wait(1.2)
        self.play(th.animate.set_value(thm), run_time=1.4)
        self.wait(1.8)
        self.play(th.animate.set_value(20.0), run_time=2.0)
        self.wait(1.6)
        for m_ in (gg, lth, rd[1], r2, r1, r0):
            m_.clear_updaters()
        self.play(FadeOut(gg), FadeOut(lth), FadeOut(rd), FadeOut(r2), FadeOut(r1), FadeOut(r0), run_time=0.7)
        self.remove(gg, lth, rd, r2, r1, r0)
        # ── (c) fecha o hook: a direção de 40° não toca o círculo ───────────────────────────────────────────────
        Lt = np.sqrt(C * C - R * R) * pl.u
        tp, tm_ = pl.O + pol(Lt, thm), pl.O + pol(Lt, -thm)
        cone = Sector(radius=(C + R) * pl.u, angle=np.radians(2 * thm), start_angle=-np.radians(thm), arc_center=pl.O) \
            .set_fill(CYAN, 0.09).set_stroke(width=0).set_z_index(1)
        tang = VGroup(Line(pl.O, pl.O + pol((C + R) * pl.u, thm)).set_stroke(WHITE_, 1.8, opacity=0.8),
                      Line(pl.O, pl.O + pol((C + R) * pl.u, -thm)).set_stroke(WHITE_, 1.8, opacity=0.8)).set_z_index(5)
        angs = (HK_TH1,) + HOOK_CAND
        cores = (GEO, GEO, GEO)
        fan = VGroup()
        for k, a in enumerate(angs):
            ln = (Line(pl.O, pl.O + pol(raio_len(a) * 0.98, a)) if k == 0 else DashedLine(pl.O, pl.O + pol(raio_len(a) * 0.98, a), dash_length=0.16)) \
                .set_stroke(cores[k], 2.4, opacity=0.9).set_z_index(6)
            fan.add(ln)
        dreal = ponto(pl.O + pol(_d_mais(lam, HK_TH1) * pl.u, HK_TH1), WHITE_, 0.1, z=9)
        l25 = M(r"25^\circ", size=28).move_to(pl.O + pol(raio_len(25) * 0.98 + 0.4, 25))
        l40 = M(r"40^\circ", size=28).move_to(pl.O + pol(raio_len(40) * 0.98 + 0.4, 40))
        # a mesma situação do hook, no espaço físico
        mini0 = P3(2.4, -1.1)
        mini = VGroup(Line(mini0, mini0 + pol(3.4, HK_TH1)).set_stroke(GEO, 2.4, opacity=0.9),
                      *[DashedLine(mini0, mini0 + pol(3.4, a), dash_length=0.14).set_stroke(VEL, 3, opacity=0.8) for a in HOOK_CAND],
                      ponto(mini0, WHITE_, 0.08))
        tmini = self.tag_plano(True).move_to(P3(4.6, 2.4))
        # o rótulo do plano sai do alto do painel (onde passam os raios) e vai para o pé dele

        self.play(FadeIn(cone), Create(tang), self.base07[1].animate.move_to(pl.pt(0.62, -0.36) + P3(0, 0.35)), run_time=1.2)
        self.play(FadeIn(tmini), FadeIn(mini), run_time=0.9)
        self.wait(0.8)
        self.play(Create(fan[0]), FadeIn(dreal), run_time=0.9)
        self.wait(0.6)
        self.play(Create(fan[1]), FadeIn(l25), run_time=0.9)
        self.play(Create(fan[2]), FadeIn(l40), run_time=0.9)
        self.wait(0.8)
        fim = self.hl("AGORA SABEMOS POR QUÊ.", y=-3.85, size=40, color=CYAN)
        self.play(FadeIn(fim, shift=0.1 * UP), run_time=0.8)
        self.play(Indicate(fan[2], color=WHITE_, scale_factor=1.0), Indicate(l40, color=WHITE_), run_time=1.2)
        self.wait(2.2)
        self.clear(rt=0.8)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C09 — a tangência dá o ângulo máximo; tracker em λ (λ<1, λ=1, λ>1)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c09(self):
        self.secao("O ÂNGULO MÁXIMO")
        lam = ValueTracker(0.5)
        ph = ValueTracker(110.0)                    # posição de P sobre o círculo (graus, a partir do centro)
        pv = ValueTracker(0.0)                      # visibilidade de P e dos vetores p₁f, p₂f
        pl = Plano(P3(-4.7, -0.7), 4.1)
        base = pl.base(-0.5, 1.2, -0.74, 0.74)
        tagp = self.tag_plano(False).move_to(pl.pt(-0.5, -0.74) + P3(0.8, 0.3))
        T = pl.pt(1, 0)
        p1i = arrow(pl.O, T, color=MAG, width=7, tip=0.22, z=6)
        lpi = lab_at(M(r"\vec p_{1i}", size=32), pl.O, T, lado=-1)

        def dyn():
            l_ = lam.get_value()
            C, R = lam_cr(l_)
            ctr = pl.pt(C, 0)
            g = VGroup(Circle(radius=R * pl.u).move_to(ctr).set_stroke(CYAN, 3.5).set_fill(CYAN, 0.07).set_z_index(3),
                       ponto(ctr, GEO, 0.07, z=8))
            if l_ < 0.985:                                          # origem fora do círculo: tangentes e setor permitido
                thm = np.arcsin(l_)
                tp = pl.O + pol(np.sqrt(C * C - R * R) * pl.u, np.degrees(thm))
                Lw = min((C + R) * pl.u, 2.9 / max(np.sin(thm), 1e-6))          # não sai do painel
                g.add(Sector(radius=Lw, angle=2 * thm, start_angle=-thm, arc_center=pl.O)
                      .set_fill(CYAN, 0.09).set_stroke(width=0).set_z_index(1),
                      Line(pl.O, pl.O + pol(Lw, np.degrees(thm))).set_stroke(WHITE_, 2, opacity=0.85).set_z_index(5),
                      Line(pl.O, pl.O + pol(Lw, -np.degrees(thm))).set_stroke(WHITE_, 1.4, opacity=0.5).set_z_index(5),
                      Line(ctr, tp).set_stroke(GEO, 2.2).set_z_index(5),
                      reto(tp, pl.O - tp, ctr - tp, s=0.18).set_z_index(6),
                      arco(pl.O, 0.75, 0, np.degrees(thm)).set_z_index(6),
                      M(r"R", size=26, color=GEO).move_to((ctr + tp) / 2 + unit(tp - ctr) * 0.0 + P3(0.22, 0.12)),
                      M(r"C", size=26, color=GEO).move_to(pl.pt(C / 2, 0) + P3(0, -0.28)))
                if l_ < 0.9:
                    g.add(M(r"\theta_{\max}", size=26).move_to(pl.O + pol(1.25, np.degrees(thm) / 2 + 3)))
            v_ = pv.get_value()
            if v_ > 0.01:
                a = np.radians(ph.get_value())
                P = pl.pt(C + R * np.cos(a), R * np.sin(a))
                vs = VGroup(arrow(pl.O, P, color=MAG, width=6, tip=0.2, z=7), arrow(P, T, color=MAG_L, width=6, tip=0.2, z=7),
                            ponto(P, WHITE_, 0.09, z=9))
                if abs(l_ - 1.0) < 0.012:
                    vs.add(reto(P, pl.O - P, T - P, s=0.22).set_z_index(9))
                g.add(vs.set_opacity(v_))
            return g
        din = always_redraw(dyn)

        def pos_l(m, k):
            l_ = lam.get_value()
            C, R = lam_cr(l_)
            a = np.radians(ph.get_value())
            P = pl.pt(C + R * np.cos(a), R * np.sin(a))
            lab_at(m, pl.O, P, lado=1) if k == 1 else lab_at(m, P, T, lado=1)
            curto = k == 1 and np.linalg.norm(P - pl.O) < 0.3          # p₁f = 0: sem vetor, sem rótulo
            m.set_opacity(0.0 if curto else pv.get_value())
        l1 = M(r"\vec p_{1f}", size=30).add_updater(lambda m: pos_l(m, 1))
        l2 = M(r"\vec p_{2f}", size=30).add_updater(lambda m: pos_l(m, 2))

        def linha(rot, f, n=2, un=None):
            d = DecimalPT(f(), num_decimal_places=n, font_size=38, **({"unit": un} if un else {}))
            g = VGroup(rot, d)
            d.add_updater(lambda m: m.set_value(f()))
            d.add_updater(lambda m: m.next_to(rot, RIGHT, buff=0.18))
            return g

        thf = lambda: float(np.degrees(np.arcsin(min(lam.get_value(), 1.0))) if lam.get_value() <= 1.0 else 180.0)   # noqa: E731
        rl = linha(M(r"\lambda=", size=44), lambda: lam.get_value())
        rc = linha(M(r"C/p_{1i}=", size=36), lambda: lam_cr(lam.get_value())[0])
        rr = linha(M(r"R/p_{1i}=", size=36), lambda: lam_cr(lam.get_value())[1])
        rt = linha(M(r"\theta_{\max}=", size=36), thf, 1, r"^\circ")
        leitura = VGroup(rl, rc, rr, rt).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(P3(3.2, 1.9))
        for g_ in leitura:                                          # DecimalNumber acompanha o rótulo depois do arrange
            g_[1].next_to(g_[0], RIGHT, buff=0.18)
        self.play(FadeIn(base), FadeIn(tagp), run_time=0.9)
        self.play(GrowArrow(p1i), FadeIn(lpi), FadeIn(din), run_time=1.0)
        self.add(l1, l2)
        self.play(FadeIn(leitura, shift=0.1 * UP), run_time=0.8)
        self.wait(1.2)
        # ── λ < 1: a origem fica fora do círculo; a tangente fixa o ângulo máximo ───────────────────────────────
        a1 = M(r"\sin\theta_{\max}=\frac{R}{C}=\lambda", size=44, w=6.4).move_to(P3(4.4, -0.55))
        a2 = M(r"\theta_{\max}=\arcsin\frac{m_2}{m_1}", size=48).move_to(P3(4.4, -1.95))
        ba2 = box(a2, buff=0.14)
        a3 = VGroup(txt("TRADUÇÃO ALGÉBRICA", 16, color=DIM),
                    M(r"\Delta\ge0\;\Leftrightarrow\;\cos^2\theta\ge1-\lambda^2\;\Leftrightarrow\;\sin\theta\le\lambda", size=32, w=6.4)) \
            .arrange(DOWN, buff=0.12).move_to(P3(4.4, -3.3))
        self.play(Write(a1), run_time=1.4)
        self.wait(1.6)
        self.play(Write(a2), Create(ba2), run_time=1.4)
        self.wait(1.4)
        self.play(FadeIn(a3, shift=0.1 * UP), run_time=0.8)
        self.wait(1.6)
        self.play(lam.animate.set_value(0.25), run_time=2.5)
        self.wait(1.0)
        self.play(lam.animate.set_value(0.85), run_time=3.0)
        self.wait(1.6)
        # ── λ = 1: o círculo tem diâmetro de 0 a p₁ᵢ; Thales ───────────────────────────────────────────────────
        gA = VGroup(a1, a2, ba2, a3)
        self.play(lam.animate.set_value(1.0), FadeOut(gA), run_time=2.4)
        b1 = txt("TEOREMA DE THALES", 26).move_to(P3(4.4, -0.7))
        b2 = M(r"\vec p_{1f}\perp\vec p_{2f}", size=52).move_to(P3(4.4, -1.8))
        bb2 = box(b2, buff=0.14)
        b3 = M(r"\theta_{\max}=90^\circ", size=40).move_to(P3(4.4, -2.9))
        b4 = VGroup(M(r"p_{1f}=0", size=30), txt("RECUO FRONTAL DO ALVO", 20, op=0.85)).arrange(RIGHT, buff=0.25).move_to(P3(4.4, -3.6))
        self.play(pv.animate.set_value(1.0), FadeIn(b1, shift=0.1 * UP), run_time=1.0)
        self.play(Write(b2), Create(bb2), run_time=1.2)
        self.play(ph.animate.set_value(60.0), run_time=2.4)
        self.play(ph.animate.set_value(150.0), run_time=3.0)
        self.play(FadeIn(b3, shift=0.1 * UP), run_time=0.7)
        self.play(ph.animate.set_value(180.0), run_time=1.6)
        self.play(FadeIn(b4, shift=0.1 * UP), run_time=0.7)
        self.wait(1.6)
        self.play(ph.animate.set_value(110.0), run_time=1.6)
        # ── λ > 1: a origem fica dentro; qualquer direção até 180° tem solução ─────────────────────────────────
        gB = VGroup(b1, b2, bb2, b3, b4)
        self.play(lam.animate.set_value(2.0), FadeOut(gB), run_time=3.0)
        c1 = txt("A ORIGEM FICA DENTRO DO CÍRCULO", 24).move_to(P3(4.4, -0.7))
        c2 = VGroup(txt("QUALQUER DIREÇÃO ATÉ", 24), M(r"180^\circ", size=40)).arrange(RIGHT, buff=0.2).move_to(P3(4.4, -1.6))
        c3 = txt("TEM SOLUÇÃO: A INCIDENTE PODE VOLTAR", 24, color=CYAN).move_to(P3(4.4, -2.5))
        c4 = VGroup(txt("NÃO EXISTE ÂNGULO MÁXIMO MENOR QUE", 20, op=0.85), M(r"180^\circ", size=30)).arrange(RIGHT, buff=0.15) \
            .move_to(P3(4.4, -3.4))
        self.play(FadeIn(c1, shift=0.1 * UP), run_time=0.8)
        self.play(ph.animate.set_value(150.0), run_time=2.0)
        self.play(FadeIn(c2, shift=0.1 * UP), run_time=0.7)
        self.play(ph.animate.set_value(125.0), run_time=1.4)
        self.play(FadeIn(c3, shift=0.1 * UP), run_time=0.7)
        self.play(FadeIn(c4, shift=0.1 * UP), run_time=0.7)
        self.wait(2.4)
        din.clear_updaters()
        for m_ in (l1, l2):
            m_.clear_updaters()
        self.clear(rt=0.8)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C10 — alfa contra nêutron (λ = 1/4): o estado do ângulo limite
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
        pl = Plano(P3(-7.3, -0.7), 7.6)
        base = pl.base(-0.07, 1.09, -0.36, 0.4)
        tagp = self.tag_plano(False).move_to(pl.pt(0.62, -0.36) + P3(0, 0.35))
        T = pl.pt(1, 0)
        p1i = arrow(pl.O, T, color=MAG, width=7, tip=0.22, z=6)
        ctr = pl.pt(C, 0)
        circ = Circle(radius=R * pl.u).move_to(ctr).set_stroke(CYAN, 3.5).set_fill(CYAN, 0.07).set_z_index(3)
        Tp = pl.O + pol(p1f_n * pl.u, thm)
        cone = Sector(radius=(C + R) * pl.u, angle=np.radians(2 * thm), start_angle=-np.radians(thm), arc_center=pl.O) \
            .set_fill(CYAN, 0.09).set_stroke(width=0).set_z_index(1)
        tang = VGroup(Line(pl.O, pl.O + pol((C + R) * pl.u, thm)).set_stroke(WHITE_, 1.8, opacity=0.85),
                      Line(pl.O, pl.O + pol((C + R) * pl.u, -thm)).set_stroke(WHITE_, 1.4, opacity=0.5)).set_z_index(5)
        v1 = arrow(pl.O, Tp, color=MAG, width=6, tip=0.2, z=7)
        v2 = arrow(Tp, T, color=MAG_L, width=6, tip=0.2, z=7)
        pt = ponto(Tp, WHITE_, 0.1, z=9)
        l1 = lab_at(M(r"\vec p_{1f}", size=32), pl.O, Tp, lado=1)
        l2 = lab_at(M(r"\vec p_{2f}", size=32), Tp, T, lado=-1)
        prol = DashedLine(Tp, Tp + P3(1.7, 0), dash_length=0.12).set_stroke(DIM, 1.5, opacity=0.8).set_z_index(5)
        ta = arco(pl.O, 1.5, 0, thm).set_z_index(6)
        tb = arco(Tp, 0.9, -th2, 0).set_z_index(6)
        lta = M(r"\theta_{\max}", size=28).move_to(pl.O + pol(2.15, thm / 2 + 2))
        ltb = M(r"\theta_2", size=28).move_to(Tp + pol(1.3, -th2 / 2))
        self.play(FadeIn(base), FadeIn(tagp), GrowArrow(p1i), Create(circ), run_time=1.4)
        # dados (coluna da direita)
        dg = VGroup(Disco(C1F, 0.3, r"\alpha"), M(r"m_1=4m", size=34), Disco(C2F, 0.2, "n"), M(r"m_2=m", size=34),
                    M(r"\Rightarrow\lambda=\tfrac14", size=34)).arrange(RIGHT, buff=0.22).move_to(P3(4.5, 3.0))
        e1 = M(r"\theta_{\max}=\arcsin\tfrac14\approx14{,}5^\circ", size=44, w=6.4).move_to(P3(4.5, 2.1))
        e2 = M(r"\frac{p_{1f}}{p_{1i}}=\frac{\cos\theta_{\max}}{1+\lambda}=\frac{\sqrt{15}}{5}\approx0{,}775", size=40, w=6.4) \
            .move_to(P3(4.5, 0.95))
        e3 = M(r"\frac{K_{1f}}{K_{1i}}=\left(\frac{p_{1f}}{p_{1i}}\right)^2=60\%", size=40, w=6.4).move_to(P3(4.5, -0.25))
        e4a = M(r"K_{n,f}=0{,}40\,K_{\alpha,i}", size=40)
        e4b = M(r"\theta_2\approx37{,}8^\circ", size=40)
        e4 = VGroup(e4a, e4b).arrange(RIGHT, buff=0.55).move_to(P3(4.5, -1.3))
        e4a[0].set_color(CYAN)
        self.play(FadeIn(dg, shift=0.1 * UP), run_time=0.9)
        self.wait(0.8)
        self.play(FadeIn(cone), Create(tang), Write(e1), run_time=1.6)
        self.play(Create(ta), FadeIn(lta), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(pt), GrowArrow(v1), FadeIn(l1), run_time=1.0)
        self.play(GrowArrow(v2), FadeIn(l2), run_time=0.8)
        self.play(Write(e2), run_time=1.6)
        self.wait(1.4)
        self.play(Write(e3), run_time=1.5)
        self.wait(1.0)
        # K: 60 % fica com a alfa, 40 % vai para o nêutron (no estado do ângulo limite)
        x0, wb, yb = 1.7, 5.0, -2.5
        capt = M(r"K_{\alpha,i}", size=28).move_to(P3(x0 + 0.5, -2.05))
        barA = Rectangle(width=wb * 0.6, height=0.34, stroke_width=0, fill_color=CYAN, fill_opacity=0.9).move_to(P3(x0 + wb * 0.3, yb))
        barN = Rectangle(width=wb * 0.4, height=0.34, stroke_width=0, fill_color=KN, fill_opacity=0.9).move_to(P3(x0 + wb * 0.8, yb))
        lA_ = MathTex(r"\alpha", font_size=26, color=BACKGROUND_COLOR).move_to(barA)
        lN_ = MathTex("n", font_size=26, color=BACKGROUND_COLOR).move_to(barN)
        self.play(FadeIn(capt), GrowFromEdge(barA, LEFT), run_time=0.8)
        self.play(GrowFromEdge(barN, LEFT), FadeIn(lA_), FadeIn(lN_), run_time=0.8)
        self.play(Write(e4a), run_time=1.2)
        self.play(Write(e4b), Create(prol), Create(tb), FadeIn(ltb), run_time=1.4)
        self.wait(1.4)
        fr = VGroup(txt("NA COLISÃO FRONTAL: ", 20, op=0.85), M(r"\frac{4\lambda}{(1+\lambda)^2}=\frac{16}{25}=64\%", size=32)) \
            .arrange(RIGHT, buff=0.2).move_to(P3(4.5, -3.45))
        self.play(FadeIn(fr, shift=0.1 * UP), run_time=0.8)
        self.wait(2.6)
        self.clear(rt=0.8)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C11 — acidente 2D completamente inelástico (inspirado no exercício 119) + deslizamento
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
        VS = 0.1                                                     # tela por (m/s) nas posições
        AK = 0.07                                                    # tela por (m/s) nas setas de velocidade
        a_ = mu * g_                                                 # desaceleração (m/s²)
        Tstop = vf / a_
        dirv = np.array([vfx, vfy, 0.0]) / vf
        ct, cc = P3(-3.6, -0.6), P3(-4.25, -0.6)                     # centros de caminhão e carro no contato
        # via vista de cima (cruz)
        W = 1.4
        h = Rectangle(width=8.0, height=W).move_to(P3(-3.6, -0.6))
        v = Rectangle(width=W, height=6.6).move_to(P3(-3.6, -0.6))
        try:
            via = Union(h, v).set_fill(DIM, 0.12).set_stroke(DIM, 1.5, opacity=0.5)
        except Exception:
            via = VGroup(h, v).set_fill(DIM, 0.1).set_stroke(DIM, 1.5, opacity=0.5)
        via.set_z_index(-3)
        eixo_c = VGroup(DashedLine(P3(-7.6, -0.6), P3(-4.3, -0.6), dash_length=0.18).set_stroke(WHITE_, 1.2, opacity=0.25),
                        DashedLine(P3(-2.9, -0.6), P3(0.4, -0.6), dash_length=0.18).set_stroke(WHITE_, 1.2, opacity=0.25),
                        DashedLine(P3(-3.6, -3.9), P3(-3.6, -1.3), dash_length=0.18).set_stroke(WHITE_, 1.2, opacity=0.25),
                        DashedLine(P3(-3.6, 0.1), P3(-3.6, 2.7), dash_length=0.18).set_stroke(WHITE_, 1.2, opacity=0.25)).set_z_index(-2)
        bus = VGroup(arrow(P3(-1.0, 1.55), P3(-1.0, 2.3), color=DIM, width=2.5, tip=0.13),
                     arrow(P3(-1.0, 1.55), P3(-0.3, 1.55), color=DIM, width=2.5, tip=0.13),
                     txt("NORTE", 14, color=DIM).move_to(P3(-1.0, 2.5)), txt("LESTE", 14, color=DIM).move_to(P3(-0.5, 1.3)))
        truck = Corpo(C1F, 0.5, 1.15, "M", 30)
        car = Corpo(C2F, 0.8, 0.42, "m", 26)
        t = ValueTracker(-1.1)

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
                a = pos_t() + P3(0, 0.575 + 0.06)
                b = pos_c() + P3(0.4 + 0.06, 0)
                return VGroup(arrow(a, a + P3(0, vT * AK), color=VEL, width=4.5, tip=0.18),
                              arrow(b, b + P3(vC * AK, 0), color=VEL, width=4.5, tip=0.18))
            sp = max(vf - a_ * tt, 0.0) if tt <= Tstop else 0.0
            if sp < 0.6:
                return VGroup()
            a = pos_t() + P3(0, 0.6)
            return VGroup(arrow(a, a + dirv * sp * AK, color=VEL, width=4.5, tip=0.18))
        sv = always_redraw(setas)
        dT = VGroup(M(r"M=3000\ \mathrm{kg}", size=30), M(r"60\ \mathrm{km/h}", size=30, color=VEL)).arrange(DOWN, buff=0.08) \
            .move_to(P3(-1.6, -2.5))
        dC = VGroup(M(r"m=1000\ \mathrm{kg}", size=30), M(r"90\ \mathrm{km/h}", size=30, color=VEL)).arrange(DOWN, buff=0.08) \
            .move_to(P3(-6.3, 0.35))
        ref = txt("INSPIRADO NO EXERCÍCIO 119", 18, color=DIM).move_to(P3(4.4, 3.3))
        self.play(FadeIn(via), FadeIn(eixo_c), FadeIn(bus), FadeIn(truck), FadeIn(car), FadeIn(sv), FadeIn(ref),
                  run_time=1.2)
        self.play(FadeIn(dT, shift=0.1 * UP), FadeIn(dC, shift=0.1 * UP), run_time=0.8)
        self.wait(1.0)
        self.play(t.animate.set_value(0.0), rate_func=linear, run_time=1.1 * 2.0)
        self.play(Flash(P3(-3.9, -0.6), color=WHITE_, line_length=0.25, flash_radius=0.15, num_lines=10, run_time=0.4))
        t.set_value(1e-5)
        self.play(FadeOut(dT), FadeOut(dC), t.animate.set_value(0.45), rate_func=linear, run_time=1.3)
        vfl = M(r"\vec v_f", size=32).next_to(sv, RIGHT, buff=0.12)
        self.play(FadeIn(vfl), run_time=0.5)
        # a colisão: o momento vetorial vale; K não
        e0 = M(r"\vec P_i", "=", r"\vec P_f", size=44).move_to(P3(4.4, 2.6))
        ex1 = M(r"m\cdot25=(M+m)\,v_{fx}", size=38, w=6.2).move_to(P3(4.4, 1.6))
        ex2 = M(r"v_{fx}=6{,}25\ \mathrm{m/s}", size=38).move_to(P3(4.4, 0.85))
        ey1 = M(r"M\cdot\tfrac{50}{3}=(M+m)\,v_{fy}", size=38, w=6.2).move_to(P3(4.4, -0.0))
        ey2 = M(r"v_{fy}=12{,}5\ \mathrm{m/s}", size=38).move_to(P3(4.4, -0.75))
        eth = M(r"\tan\theta=\frac{v_{fy}}{v_{fx}}=2\;\Rightarrow\;\theta\approx63{,}4^\circ", size=38, w=6.2).move_to(P3(4.4, -1.8))
        evf = M(r"|\vec v_f|\approx13{,}98\ \mathrm{m/s}", size=38).move_to(P3(4.4, -2.7))
        self.play(Write(e0), run_time=1.0)
        self.wait(0.6)
        self.play(Write(ex1), run_time=1.1)
        self.play(Write(ex2), run_time=0.9)
        self.wait(0.5)
        self.play(Write(ey1), run_time=1.1)
        self.play(Write(ey2), run_time=0.9)
        self.wait(0.6)
        # direção do movimento conjunto: arco branco a partir do leste
        o_ = pos_t() + P3(0, 0)
        ang = arco(P3(-3.6, -0.6), 0.8, 0, th)
        tha = MathTex(r"\theta", font_size=28).move_to(P3(-3.6, -0.6) + pol(1.15, th / 2))
        ref_l = DashedLine(P3(-3.6, -0.6), P3(-2.5, -0.6), dash_length=0.1).set_stroke(DIM, 1.5, opacity=0.7)
        self.play(Write(eth), Create(ref_l), Create(ang), FadeIn(tha), run_time=1.6)
        self.play(Write(evf), run_time=1.0)
        self.wait(0.8)
        # K não se conserva: o que não ficou como cinética foi dissipado (laranja)
        Ki = 0.5 * Mt * vT ** 2 + 0.5 * mc * vC ** 2
        Kf = 0.5 * (Mt + mc) * vf ** 2
        wk = 4.2
        msg = VGroup(txt("MOMENTO VETORIAL VALE SEM CONSERVAR", 18), M("K", size=28)).arrange(RIGHT, buff=0.12) \
            .move_to(P3(4.4, -3.35))
        bK = Rectangle(width=wk * Kf / Ki, height=0.2, stroke_width=0, fill_color=CYAN, fill_opacity=0.9)
        bH = Rectangle(width=wk * (1 - Kf / Ki), height=0.2, stroke_width=0, fill_color=HEAT, fill_opacity=0.85)
        VGroup(bK, bH).arrange(RIGHT, buff=0).move_to(P3(4.4, -3.8))
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=0.8)
        self.play(GrowFromEdge(bK, LEFT), GrowFromEdge(bH, LEFT), run_time=1.0)
        self.wait(1.8)
        # ── a colisão acabou: outro processo, outro princípio ──────────────────────────────────────────────────
        eqs = VGroup(e0, ex1, ex2, ey1, ey2, eth, evf, msg, bK, bH, ang, tha, ref_l)
        self.play(FadeOut(eqs), FadeOut(vfl), run_time=0.8)
        ch = VGroup(txt("IMPACTO: MOMENTO", 24), txt("DEPOIS: TRABALHO–ENERGIA", 24, color=CYAN)).arrange(DOWN, buff=0.15) \
            .move_to(P3(4.4, 2.5))
        w0 = M(r"\mu_k=0{,}5,\ \ g\approx10\ \mathrm{m/s^2}", size=34).move_to(P3(4.4, 1.35))
        w1 = M(r"\tfrac12(M+m)\,v_f^2=\mu_k\,(M+m)\,g\,d", size=40, w=6.2).move_to(P3(4.4, 0.35))
        w2 = M(r"d=\frac{v_f^2}{2\mu_k g}=\frac{195{,}3}{10}\approx19{,}5\ \mathrm{m}", size=40, w=6.2).move_to(P3(4.4, -1.1))
        w3 = txt("A MASSA CANCELA", 20, op=0.85).move_to(P3(4.4, -2.3))
        w4 = txt("COMO NO PÊNDULO: SEPARE OS PROCESSOS", 20, op=0.85).move_to(P3(4.4, -3.2))
        self.play(FadeIn(ch, shift=0.1 * UP), run_time=0.9)
        self.play(Write(w0), run_time=0.9)
        self.play(Write(w1), run_time=1.4)
        self.wait(0.8)
        trilha = Line(ct + dirv * 0.0, ct + dirv * dsl * VS).set_stroke(GEO, 2.2, opacity=0.8).set_z_index(-1)
        self.play(t.animate.set_value(Tstop), rate_func=linear, run_time=Tstop * 1.5)
        self.play(Create(trilha), run_time=0.6)
        dl = M("d", size=30, color=GEO).move_to(ct + dirv * dsl * VS * 0.5 + P3(-0.35, 0.0))
        self.play(FadeIn(dl), Write(w2), run_time=1.4)
        self.play(FadeIn(w3, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(w4, shift=0.1 * UP), run_time=0.6)
        self.wait(2.4)
        for m_ in (truck, car, sv):
            m_.clear_updaters()
        self.clear(rt=0.8)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C12 — explosão: mesmo momento, outra história energética
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c12(self):
        self.secao("EXPLOSÕES")
        p1, p2 = pol(2.0, 80.0), pol(1.5, 205.0)
        p3 = -(p1 + p2)
        assert np.linalg.norm(p1 + p2 + p3) < 1e-12
        rs = (0.36, 0.3, 0.26)
        ps = (p1, p2, p3)
        c0 = P3(-3.6, -0.3)
        corpo = Disco(STEEL, 0.62).move_to(c0)
        z = M(r"\vec P_i=\vec 0", size=36).move_to(P3(-3.6, -1.3))
        s = ValueTracker(0.0)                                       # 0 = parado; 1 = fragmentos afastados
        frag = [Disco(C1F if k != 1 else C2F, rs[k], ["m_1", "m_2", "m_3"][k]) for k in range(3)]

        def pos_f(k):
            return c0 + unit(ps[k]) * (0.0 + 1.7 * s.get_value() * (np.linalg.norm(ps[k]) / rs[k] ** 2) / 14.0)
        for k, f in enumerate(frag):
            f.add_updater(lambda m, k=k: m.move_to(pos_f(k)))
            f.move_to(pos_f(k))

        def setas_p():
            if s.get_value() < 0.05:
                return VGroup()
            g = VGroup()
            for k in range(3):
                a = pos_f(k) + unit(ps[k]) * (rs[k] + 0.05)
                g.add(arrow(a, a + ps[k] * 0.42, color=MAG if k != 1 else MAG_L, width=6, tip=0.2))
            return g.set_opacity(min(1.0, s.get_value() * 2))
        sp = always_redraw(setas_p)
        self.play(FadeIn(corpo), FadeIn(z, shift=0.1 * UP), run_time=1.0)
        self.wait(1.0)
        self.remove(corpo)
        self.add(*frag)
        self.play(Flash(c0, color=WHITE_, line_length=0.3, flash_radius=0.35, num_lines=14, run_time=0.5), FadeOut(z), run_time=0.5)
        self.add(sp)
        self.play(s.animate.set_value(1.0), rate_func=rate_functions.ease_out_cubic, run_time=2.2)
        self.wait(0.8)
        # Σ p = 0 : os três momentos fecham um triângulo
        e1 = M(r"\sum_k", r"\vec p_k", "=", r"\vec 0", size=52).move_to(P3(4.4, 2.5))
        nota = txt("SE PARTIU DO REPOUSO", 18, color=DIM).move_to(P3(4.4, 3.2))
        self.play(FadeIn(nota), Write(e1), run_time=1.4)
        O = P3(3.0, 0.45)
        a1 = arrow(O, O + p1 * 0.62, color=MAG, width=6, tip=0.2)
        a2 = arrow(O + p1 * 0.62, O + (p1 + p2) * 0.62, color=MAG_L, width=6, tip=0.2)
        a3 = arrow(O + (p1 + p2) * 0.62, O, color=MAG, width=6, tip=0.2)
        t1 = lab_at(M(r"\vec p_1", size=30), O, O + p1 * 0.62, lado=-1)
        t2 = lab_at(M(r"\vec p_2", size=30), O + p1 * 0.62, O + (p1 + p2) * 0.62, lado=-1)
        t3 = lab_at(M(r"\vec p_3", size=30), O + (p1 + p2) * 0.62, O, lado=-1)
        self.play(GrowArrow(a1), FadeIn(t1), run_time=0.8)
        self.play(GrowArrow(a2), FadeIn(t2), run_time=0.8)
        self.play(GrowArrow(a3), FadeIn(t3), run_time=0.8)
        self.wait(1.0)
        # energia: a interna alimenta a cinética; o total não muda
        wtot = 3.6
        u = ValueTracker(0.0)
        bI = always_redraw(lambda: Rectangle(width=max(wtot * (1 - 0.55 * u.get_value()), 1e-3), height=0.28, stroke_width=0,
                                             fill_color=HEAT, fill_opacity=0.85)
                           .move_to(P3(3.6 + max(wtot * (1 - 0.55 * u.get_value()), 1e-3) / 2, -1.55)))
        bC = always_redraw(lambda: Rectangle(width=max(wtot * 0.55 * u.get_value(), 1e-3), height=0.28, stroke_width=0,
                                             fill_color=CYAN, fill_opacity=0.9)
                           .move_to(P3(3.6 + max(wtot * 0.55 * u.get_value(), 1e-3) / 2, -2.15)))
        lI = txt("ENERGIA INTERNA", 16, color=HEAT)
        lI.move_to(P3(3.45 - lI.width / 2, -1.55))
        lC = VGroup(txt("ENERGIA CINÉTICA", 16, color=CYAN), M("K", size=24)).arrange(RIGHT, buff=0.1)
        lC.move_to(P3(3.45 - lC.width / 2, -2.15))
        cmp_ = M(r"K_i=0\;\to\;K_f>0", size=34).move_to(P3(4.4, -3.1))
        tot = txt("ENERGIA TOTAL: CONSTANTE", 18, op=0.85).move_to(P3(4.4, -3.75))
        self.play(FadeIn(lI), FadeIn(lC), FadeIn(bI), FadeIn(bC), run_time=0.8)
        self.play(u.animate.set_value(1.0), run_time=2.0)
        self.play(Write(cmp_), run_time=1.0)
        self.play(FadeIn(tot, shift=0.1 * UP), run_time=0.7)
        self.wait(2.2)
        for m_ in (*frag, sp, bI, bC):
            m_.clear_updaters()
        self.clear(rt=0.8)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C13 — método geral e síntese
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c13(self):
        self.secao("MÉTODO E SÍNTESE")
        textos = ("SISTEMA?", "IMPULSO EXTERNO DESPREZÍVEL?", "QUANTAS DIMENSÕES?", "TIPO DE EVENTO?", "NOVA ETAPA DEPOIS?")
        ys = (2.35, 1.2, 0.05, -1.1, -2.25)
        chips = VGroup()
        for i, (s_, y_) in enumerate(zip(textos, ys)):
            r_ = RoundedRectangle(corner_radius=0.18, width=5.7, height=0.78).set_stroke(WHITE_, 1.6, opacity=0.4).set_fill(WHITE_, 0.04)
            n_ = MathTex(str(i + 1), font_size=34, color=DIM)
            t_ = txt(s_, 20)
            g_ = VGroup(r_, n_, t_)
            n_.move_to(r_.get_left() + RIGHT * 0.42)
            t_.move_to(r_.get_center() + RIGHT * 0.3)
            g_.move_to(P3(-4.5, y_))
            chips.add(g_)
        mk = Circle(radius=0.15).set_stroke(CYAN, 2.5).set_fill(CYAN, 0.35).set_z_index(20)

        def foco(i):
            return [c_[0].animate.set_stroke(CYAN if k == i else WHITE_, 2.2 if k == i else 1.6, opacity=0.95 if k == i else 0.4)
                    for k, c_ in enumerate(chips)]
        pos = lambda i: chips[i][0].get_right() + LEFT * 0.0 + RIGHT * 0.25        # noqa: E731
        self.play(LaggedStart(*[FadeIn(c_, shift=0.1 * RIGHT) for c_ in chips], lag_ratio=0.15), run_time=1.6)
        mk.move_to(pos(0))
        self.play(FadeIn(mk, scale=0.6), *foco(0), run_time=0.7)
        # 1 sistema
        d1, d2 = Disco(C1F, 0.28, "m_1"), Disco(C2F, 0.24, "m_2")
        sis = VGroup(d1, d2).arrange(RIGHT, buff=0.35).move_to(P3(3.2, 2.35))
        cont = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=sis.width + 0.6, height=sis.height + 0.55).move_to(sis)
                              .set_stroke(WHITE_, 2, opacity=0.6), num_dashes=40)
        d1_ = VGroup(sis, cont)
        self.play(FadeIn(d1_), run_time=0.8)
        self.wait(1.2)
        # 2 impulso externo
        d2_ = VGroup(M(r"\vec P_i=\vec P_f", size=44), txt("SE O IMPULSO EXTERNO FOR DESPREZÍVEL", 18, op=0.85)) \
            .arrange(DOWN, buff=0.2).move_to(P3(3.2, 1.2))
        self.play(mk.animate.move_to(pos(1)), *foco(1), FadeIn(d2_, shift=0.1 * UP), run_time=0.9)
        self.wait(1.4)
        # 3 dimensões
        d3_ = VGroup(VGroup(M(r"1\mathrm{D}:", size=34), txt("UMA COMPONENTE", 20)).arrange(RIGHT, buff=0.2),
                     VGroup(M(r"2\mathrm{D}:", size=34), txt("DUAS COMPONENTES + GEOMETRIA", 20)).arrange(RIGHT, buff=0.2)) \
            .arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(P3(3.6, 0.0))
        self.play(mk.animate.move_to(pos(2)), *foco(2), FadeIn(d3_, shift=0.1 * UP), run_time=0.9)
        self.wait(1.4)
        # 4 tipo de evento
        def lin(a, b):
            return VGroup(txt(a, 17), M(r"\rightarrow", size=26), b).arrange(RIGHT, buff=0.15)
        d4_ = VGroup(lin("ELÁSTICA", M("K_i=K_f", size=28)),
                     lin("COMPLETAMENTE INELÁSTICA", M(r"\vec v_{1f}=\vec v_{2f}", size=28)),
                     lin("EXPLOSÃO", txt("ENERGIA INTERNA ALIMENTA K", 17)),
                     lin("OUTRO CASO", txt("CONDIÇÃO DADA", 17))).arrange(DOWN, buff=0.17, aligned_edge=LEFT).move_to(P3(3.6, -1.35))
        self.play(mk.animate.move_to(pos(3)), *foco(3), run_time=0.7)
        for l_ in d4_:
            self.play(FadeIn(l_, shift=0.1 * RIGHT), run_time=0.5)
        self.wait(1.2)
        # 5 nova etapa
        d5_ = VGroup(txt("SEPARE OS PROCESSOS", 28, color=CYAN, bold=True),
                     VGroup(txt("IMPACTO", 20), M(r"\rightarrow", size=28), txt("DESLIZAMENTO", 20)).arrange(RIGHT, buff=0.2)) \
            .arrange(DOWN, buff=0.2).move_to(P3(3.6, -3.3))
        self.play(mk.animate.move_to(pos(4)), *foco(4), FadeIn(d5_, shift=0.1 * UP), run_time=0.9)
        self.wait(2.2)
        self.clear(rt=0.8)
        # ── resposta ao hook ────────────────────────────────────────────────────────────────────────────────────
        q = self.hl("O QUE MUDOU DO 1D PARA O 2D?", y=2.55, size=44, color=CYAN)
        l1 = txt("A CONSERVAÇÃO DO MOMENTO NÃO MUDOU", 28).move_to(P3(0, 1.3))
        l2 = txt("O MOMENTO SEMPRE FOI UM VETOR", 28).move_to(P3(0, 0.4))
        l3 = txt("NO 1D, A GEOMETRIA FICAVA ESCONDIDA NA LINHA", 28, op=0.9).move_to(P3(0, -0.5))
        l4 = txt("NO 2D, ELA APARECE: DIREÇÕES, ÂNGULOS E ESTADOS POSSÍVEIS", 28).move_to(P3(0, -1.4))
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.9)
        for l_ in (l1, l2, l3, l4):
            self.wait(0.9)
            self.play(FadeIn(l_, shift=0.1 * UP), run_time=0.7)
        self.wait(2.2)
        self.play(FadeOut(VGroup(q, l1, l2, l3, l4)), run_time=0.7)
        self.remove(q, l1, l2, l3, l4)
        seta = lambda: M(r"\rightarrow", size=30)                                    # noqa: E731
        faixa = VGroup(txt("SISTEMA", 20), seta(), M(r"\vec P", size=34), seta(), txt("GEOMETRIA", 20), seta(),
                       txt("TIPO DE COLISÃO", 20), seta(), txt("NOVA ETAPA, SE HOUVER", 20)).arrange(RIGHT, buff=0.16).move_to(P3(0, 0.9))
        par1 = VGroup(txt("1D", 36, bold=True), M("=", size=40), txt("MOMENTO + TIPO", 32)).arrange(RIGHT, buff=0.25).move_to(P3(0, -0.8))
        par2 = VGroup(txt("2D", 36, bold=True, color=CYAN), M("=", size=40), txt("MOMENTO + GEOMETRIA + TIPO", 32, color=CYAN)) \
            .arrange(RIGHT, buff=0.25).move_to(P3(0, -1.9))
        self.play(LaggedStart(*[FadeIn(m_, shift=0.1 * UP) for m_ in faixa], lag_ratio=0.12), run_time=2.4)
        self.wait(1.6)
        self.play(FadeIn(par1, shift=0.1 * UP), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(par2, shift=0.1 * UP), run_time=0.8)
        self.wait(2.6)

    def cta(self):
        """Padrão do longo: tudo sai (inclusive tag e marca d'água), logo com anéis, inscrição, gancho, próximo vídeo.
        O assunto do próximo vídeo ainda não foi decidido: marcador visível PRÓXIMO: A DEFINIR."""
        self._pend = []
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        for m in self.mobjects:
            m.clear_updaters()
        Scene.clear(self)                  # nada fica atrás da logo
        oc = P3(0, 0.7)
        rings = VGroup(*[DashedVMobject(Circle(radius=r, arc_center=oc), num_dashes=max(12, int(14 * r)),
                                        dashed_ratio=0.6).set_stroke(VEL, 3.5, 0.16) for r in (2.0, 3.0, 4.0)])
        for i, r_ in enumerate(rings):
            r_.add_updater(lambda m, dt, sg=(1 if i % 2 == 0 else -1) * (0.06 - 0.01 * i): m.rotate(sg * dt, about_point=oc))
        logo = self.logo(6.0).move_to(oc + P3(0, 0.4))
        msg = txt("INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS", 28, op=0.9).move_to(oc + P3(0, -1.0))
        gancho = txt("PERGUNTA-GANCHO DO PRÓXIMO VÍDEO: A DEFINIR", 24, op=0.7).move_to(oc + P3(0, -1.85))
        nx1 = txt("PRÓXIMO VÍDEO:", 26, op=0.9).move_to(oc + P3(0, -1.85))
        pill = RoundedRectangle(corner_radius=0.2, width=4.6, height=0.7)
        pill = DashedVMobject(pill.set_stroke(CYAN, 2.5, opacity=0.9), num_dashes=40).move_to(oc + P3(0, -2.5))
        nx2 = txt("PRÓXIMO: A DEFINIR", 28, color=CYAN, bold=True).move_to(oc + P3(0, -2.5))
        self.play(LaggedStart(*[FadeIn(r_, scale=0.85) for r_ in rings], lag_ratio=0.3), FadeIn(logo, scale=0.92), run_time=1.8)
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=0.9)
        self.play(FadeIn(gancho, shift=0.1 * UP), run_time=0.9)
        self.wait(1.4)
        self.play(FadeOut(gancho), run_time=0.5)
        self.play(FadeIn(nx1, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(pill), FadeIn(nx2, shift=0.1 * UP), run_time=0.6)
        w = DashedVMobject(Circle(radius=1.6, arc_center=oc), num_dashes=24, dashed_ratio=0.6).set_stroke(VEL, 3.5, 0.35)
        self.play(w.animate.scale(2.6, about_point=oc).set_stroke(opacity=0.0), run_time=2.4)
        self.remove(w)
        w2 = DashedVMobject(Circle(radius=1.6, arc_center=oc), num_dashes=24, dashed_ratio=0.6).set_stroke(VEL, 3.5, 0.35)
        self.play(w2.animate.scale(2.6, about_point=oc).set_stroke(opacity=0.0), run_time=2.4)
        self.remove(w2)
        self.wait(0.6)

