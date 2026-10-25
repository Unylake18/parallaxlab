"""yt_0013 — COLISÕES EM 1D: como saber o que acontece depois? (Física I · Mecânica · Colisões) — v3.

Cena completa SILENCIOSA em Manim 2D/2.5D (sem Blender). Regra-mãe: a voz explica, a tela demonstra; nenhuma equação
importante aparece desconectada do fenômeno. Preview 960×540 / 15 fps:
    uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_0013_colisoes_1d/cena.py Colisoes1DYT013
Trecho isolado (desenvolvimento): SECOES=hook,c01,c06 · auditoria de sobreposições: AUDITORIA=1 (com --dry_run).

Semântica de cor (somente a paleta oficial; tons claros = mistura com branco):
corpo 1 azul #267BFF · corpo 2 violeta #745CFF · MOMENTO magenta #EA63FF · ENERGIA CINÉTICA ciano #35D9FF ·
velocidade e texto branco · energia interna / U_g violeta translúcido. Texto editorial: Space Grotesk, caixa alta.
Um único estado físico (ValueTracker) alimenta posição, setas, vetores momento, medidores e gráficos.
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

# ── paleta v4 (docs/padrao_video_longo.md §4 + decisões do usuário em 2026-10-24) ─────────────────────────────
WHITE_ = TEXT_COLOR          # #F5F7FF — massa, números, operadores, texto
CYAN = PRIMARY_COLOR         # #35D9FF — energia cinética K
MAG = "#EA63FF"              # momento linear p, P, Δp
VEL = "#9C8CFF"              # velocidade u, v (o violeta é só da velocidade)
FC = "#5AA2FF"               # força F
HEAT = "#FF7A3D"             # energia interna / dissipada (único tom quente)
STEEL = "#7A8696"            # matéria: corpo 1
GEO = "#B8C4DA"              # geometria (d, x, régua); tom claro de aço: corpo 2
DIM = "#8FA3C4"              # eixos, convenções, texto secundário
C1F, C2F = GEO, STEEL        # corpos em aço chato: m1 aço claro, m2 aço (distintos por tom e índice)


def mix(c, w):
    """Mistura de uma cor oficial com o branco oficial (contraste sem cor nova)."""
    return interpolate_color(ManimColor(c), ManimColor(WHITE_), w).to_hex()


JC = mix(FC, 0.4)            # impulso J, ∫F dt e a área sob F(t): tom claro do azul da força
INT = HEAT                   # energia interna
UG = mix(CYAN, 0.45)         # energia potencial gravitacional (família da energia mecânica, com rótulo)

SECOES = [s.strip() for s in os.environ.get("SECOES", "").split(",") if s.strip()]
AUDITORIA = os.environ.get("AUDITORIA") == "1"
STILL = float(os.environ["STILL"]) if os.environ.get("STILL") else None   # desenvolvimento: still num instante
LENTO = 1.3                                         # desaceleração uniforme dos movimentos físicos

# ── voz: tempos por palavra (alinhamento forçado ElevenLabs), um bloco por âncora ### de narracao_sugestao.md ──
import json  # noqa: E402
import re  # noqa: E402

AQUI = Path(__file__).resolve().parent


def _n(w):
    return re.sub(r"[^\w]", "", w.lower())


VOZ = {c["chave"]: [(_n(p[0]), p[1], p[2]) for p in c["palavras"]]
       for c in json.loads((AQUI / "audio" / "alinhamento_forcado.json").read_text(encoding="utf-8"))["celulas"]}
VOZ_FIM = max(w[2] for ws in VOZ.values() for w in ws)
LEAD = 0.15                                          # a imagem entra ~0,15 s antes da palavra
GRAVAR = os.environ.get("GRAVAR") == "1"             # passe a seco que mede o conteúdo de cada trecho entre âncoras
_RIT = AQUI / "ritmo.json"
RITMO = json.loads(_RIT.read_text(encoding="utf-8")) if _RIT.exists() and not GRAVAR else None


def vt(aid, frase=None):
    """Instante (s, voz original) em que a fala `frase` começa dentro da âncora `aid` (sem frase: o início dela)."""
    ws = VOZ[aid]
    if frase is None:
        return ws[0][1]
    toks = [_n(x) for x in frase.split()]
    seq = [w[0] for w in ws]
    for i in range(len(seq) - len(toks) + 1):
        if seq[i:i + len(toks)] == toks:
            return ws[i][1]
    raise KeyError(f"frase {frase!r} não encontrada em {aid}: {' '.join(seq)}")

T_HL, T_MAIN, T_LAB, T_SMALL = 44, 34, 26, 22
M_MAIN, M_MID, M_REF, M_LAB = 68, 56, 46, 40

import re

_NOT = [(re.compile(r"v_1(?![0-9])"), "v_{1f}"), (re.compile(r"v_2(?![0-9])"), "v_{2f}"),
        (re.compile(r"u_1(?![0-9])"), "v_{1i}"), (re.compile(r"u_2(?![0-9])"), "v_{2i}"),
        (re.compile(r"(?<![A-Za-z\\])u(?![A-Za-z_])"), "v_i"), (re.compile(r"(?<![A-Za-z\\])V(?![A-Za-z_])"), "V_t")]


def notacao(t):
    """Notação do vídeo: velocidades sempre com v (i = inicial, f = final); conjunto do pêndulo V_t.
    Os textos da cena continuam escritos como u/v/V e são traduzidos aqui."""
    for rx, novo in _NOT:
        t = rx.sub(novo, t)
    return t


TOK = {}
for _s in ("v_{1i}", "v_{1f}", "v_{1i}^2", "v_{1f}^2", "v_{2i}", "v_{2f}", "v_{2i}^2", "v_{2f}^2", "v_f", r"\vec v"):
    TOK[_s] = VEL
for _s in (r"\vec J", r"J_{\mathrm{ext}}", r"J_{\mathrm{ext},x}"):
    TOK[_s] = JC
TOK[r"\vec F"] = FC
VELP = {notacao(x) for x in ("u", "v", "u^2", "V", "V^2", r"\tfrac{u}{2}", r"\frac{u}{2}", r"\left(\tfrac{u}{2}\right)^2",
                              r"\frac{u^2}{4}", "v_i", "V_t")}
for _s in ("p_1", "p_2", r"\vec p", r"\vec p_1", r"\vec p_2", r"\vec P", r"\vec P_i", r"\vec P_f", "P", "P_i", "P_f",
           r"\Delta P", r"\Delta p_1", r"\Delta p_2", r"\Delta\vec p", "P_{x,A}", "P_{x,B}"):
    TOK[_s] = MAG
for _s in ("K", "K_i", "K_f", "K_A", "K_B", "K_C"):
    TOK[_s] = CYAN

# Exemplo-base: m1 = 2 kg, m2 = 1 kg, u1 = +2 m/s, u2 = −2 m/s; P = +2 kg·m/s; K_i = 6 J
BASE = (2.0, 1.0, 2.0, -2.0)
FINAIS = (("rebatem", -2 / 3, 10 / 3), ("se separam", 0.0, 2.0), ("ficam juntos", 2 / 3, 2 / 3))

# Pêndulo balístico (modelo interno): m = 20 g, M = 980 g, L = 1,0 m, g = 9,8 m/s², h = 0,20 m
PM, PMM, PL, PG, PH = 0.020, 0.980, 1.0, 9.8, 0.20
PV = np.sqrt(2 * PG * PH)
ESC = 3.0


def _subida():
    """θ'' = −(g/L) sen θ, sem dissipação, de θ = 0 e ω = V/L até ω = 0 (RK4)."""
    dt, th, w, t = 2e-4, 0.0, PV / PL, 0.0
    T, TH, W = [0.0], [0.0], [w]

    def f(a):
        return -PG / PL * np.sin(a)
    while w > 0:
        k1t, k1w = w, f(th)
        k2t, k2w = w + dt / 2 * k1w, f(th + dt / 2 * k1t)
        k3t, k3w = w + dt / 2 * k2w, f(th + dt / 2 * k2t)
        k4t, k4w = w + dt * k3w, f(th + dt * k3t)
        th += dt / 6 * (k1t + 2 * k2t + 2 * k3t + k4t)
        w += dt / 6 * (k1w + 2 * k2w + 2 * k3w + k4w)
        t += dt
        T.append(t)
        TH.append(th)
        W.append(max(w, 0.0))
    return np.array(T), np.array(TH), np.array(W)


SUB_T, SUB_TH, SUB_W = _subida()


# ── texto, matemática e formas ───────────────────────────────────────────────────────────────────────────────
def txt(s, size=T_MAIN, color=WHITE_, op=1.0, bold=False):
    """Texto editorial: Space Grotesk em CAIXA ALTA."""
    s = s.upper()
    if bold:
        return official_text(s, DISPLAY_FONT, BOLD, size, oversample=2, color=color).set_opacity(op)
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(op)


def gloss(s, size=T_SMALL, op=0.7):
    """Glossário de variável (única exceção à caixa alta)."""
    return screen_text(s, size, color=WHITE_, oversample=4).set_opacity(op)


def M(*parts, size=M_MAIN, color=WHITE_, w=None):
    parts = [notacao(x) for x in parts]
    m = MathTex(*parts, font_size=size, color=color, tex_to_color_map=TOK)
    for part, sub in zip(parts, m.submobjects):
        if part in VELP:                      # u, v e V soltos (sem índice): velocidade
            sub.set_color(VEL)
    if w and m.width > w:
        m.scale_to_fit_width(w)
    return m


def P3(x, y):
    return np.array([x, y, 0.0])


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


def contorno(m, buff=0.3, op=0.55):
    r = RoundedRectangle(corner_radius=0.18, width=m.width + 2 * buff, height=m.height + 2 * buff).move_to(m)
    return DashedVMobject(r.set_stroke(WHITE_, 2, opacity=op), num_dashes=60)


def placa(w, h, centro, op=0.05):
    """Painel chato: retângulo arredondado, fundo ~5 %, borda 1,4 px."""
    frente = RoundedRectangle(corner_radius=0.12, width=w, height=h).set_stroke(WHITE_, 1.4, opacity=0.24) \
        .set_fill(WHITE_, op).move_to(centro)
    return VGroup(frente).set_z_index(-2)


def barra(x0, y, largura, cor, h=0.3, op=0.9):
    r = Rectangle(width=max(largura, 1e-3), height=h, stroke_width=0, fill_color=cor, fill_opacity=op)
    return r.move_to(P3(x0 + max(largura, 1e-3) / 2, y))


class Corpo(VGroup):
    """Corpo 2D chato: preenchimento sólido, contorno claro de 2 px e filete interno de 1 px (sem 3D falso)."""

    def __init__(self, nome, cor, lado, size=40, alt=None):
        super().__init__()
        alt = alt or lado
        self.lado, self.alt = lado, alt
        f = RoundedRectangle(corner_radius=0.04, width=lado, height=alt).set_stroke(mix(cor, 0.5), 2) \
            .set_fill(cor, 1.0)
        ins = min(0.07, 0.12 * min(lado, alt))
        filete = RoundedRectangle(corner_radius=0.03, width=max(lado - 2 * ins, 0.02), height=max(alt - 2 * ins, 0.02)) \
            .set_stroke(WHITE_, 1, opacity=0.35).set_fill(opacity=0).move_to(f)
        self.front = f
        self.add(f, filete)
        if nome:
            esc = cor == GEO                     # texto escuro sobre o aço claro, branco sobre o escuro
            self.lab = MathTex(nome, font_size=size, color=BACKGROUND_COLOR if esc else WHITE_).move_to(f)
            self.add(self.lab)

    def at(self, x, yb):
        self.shift(P3(x, yb + self.alt / 2) - self.front.get_center())
        return self


class Cron(VGroup):
    """Régua ANTES → CONTATO → DEPOIS; o estado atual fica aceso."""

    def __init__(self, centro):
        super().__init__()
        self.rot = [txt(s, T_SMALL) for s in ("ANTES", "CONTATO", "DEPOIS")]
        setas = [MathTex(r"\rightarrow", font_size=30, color=WHITE_).set_opacity(0.4) for _ in range(2)]
        VGroup(self.rot[0], setas[0], self.rot[1], setas[1], self.rot[2]).arrange(RIGHT, buff=0.22)
        self.sub = Line(LEFT, RIGHT).set_stroke(WHITE_, 2.5)
        self.add(self.rot[0], setas[0], self.rot[1], setas[1], self.rot[2], self.sub)
        self.move_to(centro)
        self.set(0)

    def set(self, k):
        for i, r in enumerate(self.rot):
            r.set_opacity(1.0 if i == k else 0.32)
        r = self.rot[k]
        self.sub.put_start_and_end_on(r.get_corner(DL) + DOWN * 0.08, r.get_corner(DR) + DOWN * 0.08)
        return self


class Col:
    """Colisão 1D com contato instantâneo em xc no instante t = 0 (t = relógio físico em s; kx = tela por metro).
    Velocidade: seta branca acima do corpo. Momento: seta magenta numa faixa abaixo do trilho (opcional)."""

    def __init__(self, m1, m2, u1, u2, v1, v2, w1=1.0, w2=0.8, xc=0.0, ty=-1.6, kx=0.9, ka=0.5, kp=0.32, t0=-1.5,
                 n1="m_1", n2="m_2", pre=("u_1", "u_2"), post=("v_1", "v_2"), junto=None, lab=M_LAB, nsize=40,
                 eixo=True, trilho=(-7.2, 7.2), mom=False, pnames=("p_1", "p_2")):
        self.m1, self.m2, self.u1, self.u2, self.v1, self.v2 = m1, m2, u1, u2, v1, v2
        self.w1, self.w2, self.xc, self.ty, self.kx, self.ka, self.kp = w1, w2, xc, ty, kx, ka, kp
        self.pre, self.post, self.junto, self.pnames = pre, post, junto, pnames
        self.t, self.ao, self.po = ValueTracker(t0), ValueTracker(1.0), ValueTracker(1.0 if mom else 0.0)
        self.b1, self.b2 = Corpo(n1, C1F, w1, size=nsize), Corpo(n2, C2F, w2, size=nsize)
        self.b1.add_updater(lambda m: m.at(self.x1(), ty))
        self.b2.add_updater(lambda m: m.at(self.x2(), ty))
        self.b1.at(self.x1(), ty)
        self.b2.at(self.x2(), ty)
        self.track = VGroup(Line(P3(trilho[0], ty), P3(trilho[1], ty)).set_stroke(WHITE_, 2.5, opacity=0.4))
        if eixo:
            ax = arrow(P3(trilho[1] - 1.3, ty - 0.4), P3(trilho[1] - 0.35, ty - 0.4), color=DIM, width=2.5, tip=0.14)
            self.track.add(ax, MathTex("+x", font_size=32, color=DIM).next_to(ax, LEFT, buff=0.1))
        names = [n for n in (*pre, *post, junto, *pnames) if n]
        self.L = {n: M(n, size=lab) for n in names}
        self.arrows = always_redraw(self._arrows)
        self.moms = always_redraw(self._moms)

    def vel(self):
        return (self.v1, self.v2) if self.t.get_value() > 1e-6 else (self.u1, self.u2)

    def x1(self):
        return self.xc - self.w1 / 2 + self.vel()[0] * self.t.get_value() * self.kx

    def x2(self):
        return self.xc + self.w2 / 2 + self.vel()[1] * self.t.get_value() * self.kx

    def P(self):
        v1, v2 = self.vel()
        return self.m1 * v1 + self.m2 * v2

    def K(self):
        v1, v2 = self.vel()
        return 0.5 * self.m1 * v1 ** 2 + 0.5 * self.m2 * v2 ** 2

    def _vec(self, x, y, vel, name):
        if name is False:
            return VGroup()
        L = vel * self.ka
        base = P3(x, y)
        lab = self.L.get(name) if name else None
        if abs(L) < 0.06:
            return VGroup(lab.move_to(base + UP * 0.2)) if lab else VGroup()
        a = arrow(base, base + RIGHT * L, color=VEL, width=4.5, tip=0.2)
        g = VGroup(a)
        if lab:
            g.add(lab.next_to(a, UP, buff=0.08))
        return g

    def _arrows(self):
        op = self.ao.get_value()
        if op <= 0.01:
            return VGroup()
        t = self.t.get_value()
        y0 = self.ty + 0.32
        if t > 1e-6 and self.junto is not None:
            xm = (self.x1() + self.x2()) / 2
            g = VGroup(self._vec(xm, y0 + max(self.w1, self.w2), self.v1, self.junto or None))
        else:
            n1, n2 = self.post if t > 1e-6 else self.pre
            v1, v2 = self.vel()
            g = VGroup(self._vec(self.x1(), y0 + self.w1, v1, n1), self._vec(self.x2(), y0 + self.w2, v2, n2))
        return g.set_opacity(op)

    def _moms(self):
        op = self.po.get_value()
        if op <= 0.01:
            return VGroup()
        v1, v2 = self.vel()
        y = self.ty - 0.42
        g = VGroup()
        for x, m, v, nm in ((self.x1(), self.m1, v1, self.pnames[0]), (self.x2(), self.m2, v2, self.pnames[1])):
            L = m * v * self.kp
            if abs(L) < 0.05:
                continue
            a = arrow(P3(x, y), P3(x + L, y), color=MAG, width=7, tip=0.22)
            g.add(a)
            if nm:
                g.add(self.L[nm].next_to(a, DOWN, buff=0.06))
        return g.set_opacity(op)

    def group(self, arrows=True):
        return VGroup(self.track, self.b1, self.b2, *([self.arrows, self.moms] if arrows else []))

    def contato(self):
        return Flash(P3(self.xc, self.ty + 0.5 * min(self.w1, self.w2)), color=WHITE_, line_length=0.2,
                     flash_radius=0.1, num_lines=10, run_time=0.35)

    def run(self, sc, t_end, rt1, rt2, cron=None, at=None):
        """Aproximação → contato → separação; `at` = âncora (id, frase) do instante do contato."""
        if cron:
            cron.set(0)
        sc.play(self.t.animate.set_value(0.0), rate_func=linear, run_time=rt1 * LENTO)
        if at:
            sc.an(*at)
        if cron:
            cron.set(1)
        sc.play(self.contato())
        self.t.set_value(1e-5)
        if cron:
            cron.set(2)
        sc.play(self.t.animate.set_value(t_end), rate_func=linear, run_time=rt2 * LENTO)

    def solta(self):
        for m in (self.b1, self.b2, self.arrows, self.moms):
            m.clear_updaters()


def estado(v1, v2, junto, escala=0.4, w1=1.0, w2=0.8, ka=0.5, kx=0.9, t=1.4, antes=False):
    """Miniatura estática (sem updaters) do exemplo-base: antes do contato ou depois dele."""
    if antes:
        v1, v2, t = BASE[2], BASE[3], -t
    x1 = -w1 / 2 + v1 * t * kx
    x2 = w2 / 2 + v2 * t * kx
    b1 = Corpo("", C1F, w1).at(x1, 0)
    b2 = Corpo("", C2F, w2).at(x2, 0)
    trilho = Line(P3(min(x1, -2.0) - 0.9, 0), P3(max(x2, 2.0) + 0.9, 0)).set_stroke(WHITE_, 2, opacity=0.4)
    g = VGroup(trilho, b1, b2).scale(escala, about_point=ORIGIN)
    e = escala
    if junto and not antes:
        xm = (x1 + x2) / 2 * e
        g.add(arrow(P3(xm, (w1 + 0.3) * e), P3(xm + v1 * ka * e, (w1 + 0.3) * e), color=VEL, width=2.5, tip=0.11))
    else:
        for x, w, v in ((x1, w1, v1), (x2, w2, v2)):
            if abs(v) > 0.05:
                g.add(arrow(P3(x * e, (w + 0.3) * e), P3((x + v * ka) * e, (w + 0.3) * e), color=VEL, width=2.5, tip=0.11))
            else:
                g.add(MathTex("0", font_size=26, color=VEL).move_to(P3(x * e, (w + 0.35) * e + 0.1)))
    return g


class Medidor(VGroup):
    """Placa com P TOTAL (magenta) e K TOTAL (ciano) lidos do mesmo estado da colisão; a parte de K que vira
    energia interna aparece em laranja (HEAT)."""

    def __init__(self, col, centro, w=4.7, kp=0.55, ke=0.5, K0=None, mostrar_K=True):
        super().__init__()
        self.col, self.kp, self.ke = col, kp, ke
        self.K0 = col.K() if K0 is None else K0
        h = 1.9 if mostrar_K else 1.1
        self.placa = placa(w, h, centro)
        x0, yc = centro[0] - w / 2, centro[1]
        self.zx = x0 + 1.75
        self.yP = yc + (0.38 if mostrar_K else 0.0)
        self.yK = yc - 0.42
        self.lP = txt("P TOTAL", T_SMALL, color=MAG).move_to(P3(x0 + 0.85, self.yP))
        self.lK = txt("K TOTAL", T_SMALL, color=CYAN).move_to(P3(x0 + 0.85, self.yK))
        zero = Line(P3(self.zx, self.yP - 0.25), P3(self.zx, self.yP + 0.25)).set_stroke(WHITE_, 1.5, opacity=0.5)
        self.add(self.placa, self.lP, zero)
        self.vP = always_redraw(lambda: arrow(P3(self.zx, self.yP), P3(self.zx + self.col.P() * self.kp, self.yP),
                                              color=MAG, width=9, tip=0.24))
        self.add(self.vP)
        if mostrar_K:
            self.add(self.lK)
            self.vK = always_redraw(self._k)
            self.add(self.vK)

    def _k(self):
        K = self.col.K()
        g = VGroup(barra(self.zx, self.yK, K * self.ke, CYAN, h=0.28))
        perdido = self.K0 - K
        if perdido > 0.05:
            g.add(barra(self.zx + K * self.ke, self.yK, perdido * self.ke, INT, h=0.28, op=0.8))
        return g

    def solta(self):
        for m in (self.vP, getattr(self, "vK", None)):
            if m is not None:
                m.clear_updaters()


class Colisoes1DYT013(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3)
        self.wm.set_z_index(40)
        self.h1 = txt("MECÂNICA · COLISÕES EM 1D", 17, color=DIM, op=0.5).to_corner(UL, buff=0.32).set_z_index(40)
        self.h2 = None
        self._pend = []
        self.add(self.wm, self.h1)
        # sincronia: trecho k = conteúdo entre a âncora k−1 e a âncora k; FP/FW = fatores de play/espera do trecho
        self.k, self.rec, self.atrasos = 0, [], []
        self._ini_trecho()
        marcas = []
        for nome in ("hook", "abertura", "c01_momento", "c02_impulso", "c03_tipos", "c04_juntos", "c05_energia",
                     "c06_elastica", "c06b_relativa", "c07_formulas", "c08_limites", "c09_pendulo", "c10_impacto",
                     "c11_subida", "c12_metodo", "ponte_2d", "cta"):
            self.next_section(nome, skip_animations=bool(SECOES) and nome.split("_")[0] not in SECOES)
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

    # ── auditoria de sobreposições (desenvolvimento: AUDITORIA=1) ───────────────────────────────────────────
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
                    itens.append(("seta", m))
                return
            if isinstance(m, Corpo):
                itens.append(("corpo", m.front))
                return
            if isinstance(m, (Line, DashedVMobject)) and not isinstance(m, Arrow):
                if op(m) > 0.3:
                    linhas.append(m)
                return
            if isinstance(m, Rectangle) and m.get_stroke_width() == 0 and m.get_fill_opacity() > 0.4:
                itens.append(("barra", m))
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
        novo = txt(s, 30, op=0.95).next_to(self.h1, DOWN, buff=0.14, aligned_edge=LEFT).set_z_index(40) if s else None
        if self.h2 is not None:
            velho, self.h2 = self.h2, None
            self._pend = [a for a in self._pend]
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

    def troca(self, old, new, rt=0.5):
        if old is None:
            self.play(FadeIn(new), run_time=rt)
        else:
            self.play(FadeOut(old), FadeIn(new), run_time=rt)
        return new

    def dica(self, s, pos=P3(4.9, -3.45), dur=2.0):
        """Hábito de resolução: pílula discreta que aparece e some."""
        t = txt(s, T_SMALL)
        p = RoundedRectangle(corner_radius=0.2, width=t.width + 0.5, height=t.height + 0.32) \
            .set_stroke(WHITE_, 1.4, opacity=0.5).set_fill(WHITE_, 0.04)
        g = VGroup(p, t).move_to(pos)
        t.move_to(p)
        self.play(FadeIn(g, shift=0.1 * UP), run_time=0.4)
        self.wait(dur)
        self.play(FadeOut(g), run_time=0.4)

    def swap(self, old, new, rt=1.1, **kw):
        self.play(TransformMatchingTex(old, new, **kw), run_time=rt)
        return new

    def remap(self, old, new, pairs, rt=1.2, extra=(), sem_fade=()):
        anims, uo, un = [], set(), set()
        for o, n in pairs:
            o = o if isinstance(o, (list, tuple)) else [o]
            n = n if isinstance(n, (list, tuple)) else [n]
            uo.update(o)
            un.update(n)
            so = "".join(getattr(old[i], "tex_string", "?") for i in o)
            sn = "".join(getattr(new[j], "tex_string", "!") for j in n)
            if so.replace(" ", "") == sn.replace(" ", ""):
                anims.append(ReplacementTransform(VGroup(*[old[i].copy() for i in o]), VGroup(*[new[j] for j in n])))
            else:
                anims.append(FadeOut(VGroup(*[old[i].copy() for i in o]), shift=0.12 * UP))
                anims.append(FadeIn(VGroup(*[new[j] for j in n]), shift=0.12 * UP))
        anims += [FadeOut(old[i]) for i in range(len(old)) if i not in uo]
        anims += [FadeIn(new[j]) for j in range(len(new)) if j not in un and j not in sem_fade]
        for i in uo:
            old[i].set_opacity(0)
        antes = {id(m) for m in self.mobjects}
        self.play(*anims, *extra, run_time=rt)
        self.drop(old)
        self.remove(*[m for m in self.mobjects if id(m) not in antes and m is not new])
        self.add(new)
        return new

    def drop(self, *mobs):
        fam = {id(x) for mob in mobs for x in mob.get_family()}
        self.remove(*[m for m in self.mobjects if id(m) in fam or
                      (m.submobjects and all(id(x) in fam for x in m.get_family()[1:]))])

    def settle(self, new):
        fam = {id(x) for x in new.get_family()}
        self.remove(*[m for m in self.mobjects if m is not new and (id(m) in fam or
                      (m.submobjects and all(id(x) in fam for x in m.get_family()[1:])))])
        self.add(new)
        return new

    def base_col(self, v1, v2, junto=None, **kw):
        m1, m2, u1, u2 = BASE
        args = dict(w1=1.0, w2=0.8, xc=0.3, ty=-1.4, kx=0.9, ka=0.5, t0=-1.5)
        args.update(kw)
        return Col(m1, m2, u1, u2, v1, v2, junto=junto, **args)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # HOOK — mesmo começo, três finais (sem vocabulário formal)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def hook(self):
        slots = (-4.7, 0.0, 4.7)
        res = ("REBATEM", "SE SEPARAM", "FICAM JUNTOS")
        ats = (("H1", "eles batem"), ("H2", "e dessa vez"), ("H3", "e agora eles grudam"))
        for k, (nm, v1, v2) in enumerate(FINAIS):
            c = self.base_col(v1, v2, junto="" if nm == "ficam juntos" else None, n1="", n2="",
                              pre=(None, None), post=(None, None), ty=-1.3)
            self.an(("H1", "H2", "H3")[k])
            self.play(FadeIn(c.group()), run_time=0.5 if k == 0 else 0.3)
            c.run(self, 1.3, 0.55, 0.6, at=ats[k])
            t = txt(res[k], T_HL, bold=True).move_to(P3(0.3, 0.75))
            self.play(FadeIn(t, shift=0.1 * UP), run_time=0.35)
            self.wait(0.25)
            mini = VGroup(estado(v1, v2, nm == "ficam juntos", escala=0.3), txt(res[k], T_SMALL, op=0.85))
            if k == 0:
                self.minis = []
            self.minis.append((v1, v2, nm == "ficam juntos", res[k]))
            mini[1].next_to(mini[0], DOWN, buff=0.12)
            mini.move_to(P3(slots[k], 2.3))
            c.solta()
            self.play(FadeOut(c.group()), ReplacementTransform(t, mini[1]), FadeIn(mini[0]), run_time=0.35)
        h1 = self.hl("MESMO COMEÇO.", y=0.0)
        h2 = self.hl("TRÊS FINAIS.", y=-0.85)
        h3 = self.hl("POR QUÊ?", y=-2.1, size=56, color=CYAN)
        self.an("H4")
        self.play(FadeIn(h1, shift=0.1 * UP), run_time=0.4)
        self.an("H4", "três finais")
        self.play(FadeIn(h2, shift=0.1 * UP), run_time=0.4)
        self.an("H4", "por quê")
        self.play(FadeIn(h3, scale=0.95), run_time=0.4)
        self.wait(0.9)
        self.clear(rt=0.5)

    def abertura(self):
        """Bem-vindos (logo) → título com NESTE VÍDEO (~3 s) → a tag do canto encolhe."""
        logo = self.logo(4.6).move_to(P3(0, 0.6))
        wel = txt("BEM-VINDOS AO PARALLAX LAB", 34).move_to(P3(0, -1.3))
        self.an("A1")
        self.play(FadeIn(logo, scale=0.94), FadeIn(wel, shift=0.1 * UP), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(logo), FadeOut(wel), run_time=0.5)
        tit = txt("COLISÕES EM 1D", 52, color=CYAN, bold=True).move_to(P3(0, 0.45))
        sub = txt("NESTE VÍDEO: COMO SABER O QUE ACONTECE DEPOIS", 28, op=0.85).move_to(P3(0, -0.5))
        self.an("A2", "começando por colisões")
        self.play(FadeIn(tit, shift=0.1 * UP), run_time=1.0)
        self.an("A2", "a ideia é sair")
        self.play(FadeIn(sub, shift=0.1 * UP), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(tit), FadeOut(sub), run_time=0.6)

    def logo(self, largura):
        img = ImageMobject(str(ROOT / "assets" / "branding" / "overlays" / "parallax_lab_logo_horizontal.png"))
        arr = img.get_pixel_array()
        ys, xs = np.nonzero(arr[:, :, 3] > 8)
        return ImageMobject(arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).set_width(largura)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C01 — o que a conservação do momento nos diz
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c01_momento(self):
        self.secao("MOMENTO LINEAR")
        # um corpo: p = m v (massa e velocidade controladas por trackers)
        m, v = ValueTracker(1.0), ValueTracker(1.6)
        ty = -0.8
        trilho = Line(P3(-6.6, ty), P3(1.6, ty)).set_stroke(WHITE_, 2.5, opacity=0.4)

        def um():
            lado = 0.85 + 0.22 * (m.get_value() - 1)
            b = Corpo("m", C1F, lado, size=40).at(-3.6, ty)
            yv = ty + lado + 0.32
            va = arrow(P3(-3.6, yv), P3(-3.6 + 0.9 * v.get_value(), yv), color=VEL, width=6, tip=0.22)
            pa = arrow(P3(-3.6, ty - 0.45), P3(-3.6 + 0.62 * m.get_value() * v.get_value(), ty - 0.45), color=MAG,
                       width=8, tip=0.24)
            return VGroup(b, va, M(r"\vec v", size=M_LAB).next_to(va, UP, buff=0.08),
                          pa, M(r"\vec p", size=M_LAB).next_to(pa, DOWN, buff=0.08))

        g = always_redraw(um)
        pl = placa(4.4, 1.6, P3(4.5, 0.9))
        eq = M(r"\vec p", "=", "m", r"\vec v", size=M_MAIN).move_to(P3(4.5, 0.9))
        self.an("C01-1")
        self.play(Create(trilho), FadeIn(g), run_time=0.9)
        self.an("C01-1", "é a massa vezes")
        self.play(FadeIn(pl), Write(eq), run_time=1.0)
        self.wait(0.6)
        self.an("C01-1", "por isso o momento aponta")
        self.play(Indicate(eq[0], color=MAG), Indicate(eq[3], color=VEL), run_time=1.0)
        self.wait(0.6)
        rm = txt("MAIS MASSA", T_LAB, op=0.8).move_to(P3(4.5, -0.4))
        self.an("C01-2")
        self.play(m.animate.set_value(2.0), Indicate(eq[2], color=WHITE_), FadeIn(rm), run_time=1.6)
        self.wait(0.8)
        rv = txt("MAIS VELOCIDADE", T_LAB, op=0.8).move_to(P3(4.5, -0.4))
        self.play(m.animate.set_value(1.0), FadeOut(rm), run_time=0.8)
        self.an("C01-3")
        self.play(v.animate.set_value(2.8), Indicate(eq[3], color=WHITE_), FadeIn(rv), run_time=1.6)
        self.wait(1.0)
        self.play(FadeOut(rv), v.animate.set_value(1.6), run_time=0.8)
        g.clear_updaters()
        self.an("C01-4")
        self.play(FadeOut(g), FadeOut(trilho), FadeOut(pl), eq.animate.scale(0.62).move_to(P3(-4.7, 2.75)), run_time=0.8)

        # dois corpos: p1, p2 (magenta) e o eixo com sinais
        c = self.base_col(-2 / 3, 10 / 3, ty=-0.3, xc=0.3, mom=True, w1=1.2, w2=0.95, ka=0.55)
        c.po.set_value(0.0)
        self.play(FadeIn(c.group()), run_time=0.9)
        self.an("C01-4", "cada um tem")
        self.play(c.po.animate.set_value(1.0), run_time=0.9)
        self.wait(0.6)
        s1 = M("u_1", ">", "0", size=M_LAB).move_to(P3(-3.4, 1.85))
        s2 = M("u_2", "<", "0", size=M_LAB).move_to(P3(3.9, 1.85))
        self.an("C01-5", "a gente combina")
        self.play(Indicate(c.track[1:], color=WHITE_, scale_factor=1.15), run_time=0.8)
        self.wait(0.4)
        self.an("C01-5", "então a velocidade inicial do corpo um")
        self.play(FadeIn(s1, shift=0.1 * UP), run_time=0.6)
        self.an("C01-5", "e a velocidade inicial do corpo dois")
        self.play(FadeIn(s2, shift=0.1 * UP), run_time=0.6)
        self.wait(0.4)
        self.an("C01-5", "defina o eixo")
        self.dica("DEFINA O EIXO · RESPEITE OS SINAIS")
        self.play(FadeOut(s1), FadeOut(s2), run_time=0.4)
        # P = p1 + p2: soma com sinal, ponta com cauda
        K, X0, Y = 0.6, -1.6, -2.75
        zero = VGroup(Line(P3(X0, Y - 0.2), P3(X0, Y + 1.15)).set_stroke(DIM, 1.5),
                      MathTex("0", font_size=28, color=DIM).move_to(P3(X0, Y - 0.38)))
        y1, y2 = Y + 0.95, Y + 0.45
        a1 = arrow(P3(X0, y1), P3(X0 + 4 * K, y1), color=MAG, width=7, tip=0.22)
        a2 = arrow(P3(X0, y2), P3(X0 - 2 * K, y2), color=MAG, width=7, tip=0.22, op=0.7)
        l1 = M(r"\vec p_1", size=34).next_to(P3(X0 - 2.6 * K, y1), LEFT, buff=0.1)
        l2 = M(r"\vec p_2", size=34).next_to(P3(X0 - 2.6 * K, y2), LEFT, buff=0.1)
        self.an("C01-6")
        self.play(FadeIn(zero), FadeIn(l1), GrowArrow(a1), run_time=0.8)
        self.play(FadeIn(l2), GrowArrow(a2), run_time=0.8)
        self.an("C01-6", "a seta do corpo dois")
        self.play(a2.animate.shift(RIGHT * 4 * K), run_time=1.1)            # p2 começa onde p1 termina
        aP = arrow(P3(X0, Y), P3(X0 + 2 * K, Y), color=MAG, width=11, tip=0.26).set_z_index(9)
        lP = M(r"\vec P", "=", r"\vec p_1", "+", r"\vec p_2", size=M_LAB).next_to(P3(X0 + 5.6 * K, Y + 0.45), RIGHT, buff=0.4)
        gP = DashedLine(P3(X0 + 2 * K, y2 - 0.1), P3(X0 + 2 * K, Y + 0.12)).set_stroke(DIM, 1.5)
        self.an("C01-6", "o que sobra")
        self.play(GrowArrow(aP), Create(gP), FadeIn(lP), run_time=0.9)
        self.wait(1.6)
        self.an("C01-7")
        self.play(*[FadeOut(x) for x in (zero, a1, a2, l1, l2, aP, lP, gP)], run_time=0.5)

        # ANTES | equação | DEPOIS
        c.solta()
        self.play(FadeOut(c.group()), run_time=0.5)
        antes = VGroup(estado(0, 0, False, escala=0.38, antes=True), txt("ANTES", T_SMALL, op=0.8))
        antes[1].next_to(antes[0], DOWN, buff=0.15)
        depois = estado(0, 0, False, escala=0.38)
        q1 = MathTex("?", font_size=48, color=VEL).move_to(depois[1].get_top() + UP * 0.25)
        q2 = MathTex("?", font_size=48, color=VEL).move_to(depois[2].get_top() + UP * 0.25)
        depois = VGroup(VGroup(depois[0], depois[1], depois[2], q1, q2), txt("DEPOIS", T_SMALL, op=0.8))
        depois[1].next_to(depois[0], DOWN, buff=0.15)
        antes.move_to(P3(-4.3, 1.4))
        depois.move_to(P3(4.3, 1.4))
        di = VGroup(M(r"v_{1i},\ v_{2i}", size=34), gloss(": velocidades iniciais", size=20)).arrange(RIGHT, buff=0.08)
        df = VGroup(M(r"v_{1f},\ v_{2f}", size=34), gloss(": velocidades finais", size=20)).arrange(RIGHT, buff=0.08)
        di.next_to(antes, DOWN, buff=0.18)
        df.next_to(depois, DOWN, buff=0.18)
        self.play(FadeIn(antes), FadeIn(depois), run_time=0.8)
        self.an("C01-7", "o índice i")
        self.play(FadeIn(di), run_time=0.6)
        self.an("C01-7", "o índice f")
        self.play(FadeIn(df), run_time=0.6)
        self.an("C01-7", "então temos a velocidade")
        self.play(Indicate(di[0], color=VEL), Indicate(df[0], color=VEL), run_time=1.0)
        self.wait(0.6)
        self.an("C01-8")
        self.play(Indicate(antes[0], color=WHITE_, scale_factor=1.05), Indicate(depois[0], color=WHITE_, scale_factor=1.05),
                  run_time=1.0)
        e = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2v_2", size=M_MAIN).move_to(P3(0, -0.9))
        self.an("C01-8", "o momento total antes")
        self.play(Write(e[:3]), run_time=0.9)
        la = Line(di.get_bottom() + DOWN * 0.08, e[:3].get_top() + UP * 0.1).set_stroke(WHITE_, 1.5, opacity=0.35)
        self.play(Create(la), run_time=0.4)
        self.an("C01-8", "é igual ao momento total depois")
        self.play(Write(e[3:]), run_time=0.9)
        ld = Line(df.get_bottom() + DOWN * 0.08, e[4:].get_top() + UP * 0.1).set_stroke(WHITE_, 1.5, opacity=0.35)
        self.play(Create(ld), run_time=0.4)
        self.wait(1.0)
        vv = VGroup(e.get_part_by_tex("v_{1f}"), e.get_part_by_tex("v_{2f}"))
        bxs = VGroup(*[box(x, buff=0.07) for x in vv])
        self.an("C01-9")
        self.play(Indicate(e[:3], color=WHITE_, scale_factor=1.06), run_time=1.0)
        self.an("C01-9", "as incógnitas são")
        self.play(Create(bxs), run_time=0.6)
        h = self.hl("1 EQUAÇÃO. 2 INCÓGNITAS.", y=-2.35)
        self.an("C01-9", "uma equação")
        self.play(FadeIn(h, shift=0.1 * UP), run_time=0.6)
        self.wait(1.4)
        q = self.hl("O QUE FALTA?", y=-2.35, size=52, color=CYAN)
        self.an("C01-10", "o que está faltando")
        self.play(ReplacementTransform(h, q), run_time=0.6)
        self.wait(1.8)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C02 — impulso: forças internas trocam momento; o total não muda
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c02_impulso(self):
        self.secao("MOMENTO E IMPULSO")
        rec = VGroup(M(r"\Delta\vec p", "=", r"\vec J", size=M_LAB), M(r"\vec J", "=", r"\int", r"\vec F", r"\,dt", size=M_LAB)) \
            .arrange(RIGHT, buff=0.7).move_to(P3(0.6, 3.0))
        c = self.base_col(-2 / 3, 10 / 3, ty=-0.6, xc=-3.6, trilho=(-7.2, 0.0), kx=0.7, ka=0.45, eixo=False)
        cron = Cron(P3(-3.6, -3.45))
        self.an("C02-1")
        self.play(FadeIn(c.group()), FadeIn(cron), run_time=0.8)
        self.an("C02-1", "lembrando")
        self.play(FadeIn(rec[0], shift=0.1 * DOWN), run_time=0.8)
        self.an("C02-1", "e o impulso é")
        self.play(FadeIn(rec[1], shift=0.1 * DOWN), run_time=0.8)
        self.wait(1.2)
        # gráfico F(t) e placa de momentos à direita
        pg = placa(6.0, 2.7, P3(4.0, 0.85))
        ax = Axes(x_range=[0, 1, 1], y_range=[0, 1.15, 1], x_length=4.6, y_length=1.9, tips=False,
                  axis_config={"color": WHITE_, "stroke_width": 2, "stroke_opacity": 0.55}).move_to(P3(4.1, 0.75))
        axl = VGroup(MathTex("t", font_size=32, color=DIM).next_to(ax.x_axis, RIGHT, buff=0.1),
                     MathTex("F", font_size=32, color=FC).next_to(ax.y_axis, UP, buff=0.06))
        curva = ax.plot(lambda x: np.sin(PI * x), x_range=[0, 1], color=FC, stroke_width=3)
        s = ValueTracker(0.0)
        area = always_redraw(lambda: ax.get_area(curva, x_range=[0, max(s.get_value(), 1e-3)], color=JC, opacity=0.4))
        J = 16 / 3                             # momento trocado: Δp2 = −Δp1 = 16/3 kg·m/s
        pm = placa(6.0, 2.0, P3(4.0, -2.0))
        KP, ZX, YM = 0.42, 2.6, -2.0

        def momentos():
            q = (1 - np.cos(PI * s.get_value())) / 2      # ∫ sen(πs) ds normalizada: mesma lei do gráfico
            p1, p2 = 4 - J * q, -2 + J * q
            g = VGroup(arrow(P3(ZX, YM + 0.55), P3(ZX + p1 * KP, YM + 0.55), color=MAG, width=7, tip=0.2),
                       arrow(P3(ZX, YM + 0.05), P3(ZX + p2 * KP, YM + 0.05), color=MAG, width=7, tip=0.2, op=0.7),
                       arrow(P3(ZX, YM - 0.55), P3(ZX + (p1 + p2) * KP, YM - 0.55), color=MAG, width=11, tip=0.24))
            return g

        zero = Line(P3(ZX, YM - 0.8), P3(ZX, YM + 0.8)).set_stroke(WHITE_, 1.5, opacity=0.45)
        mv = always_redraw(momentos)
        lm = VGroup(M("p_1", size=34).move_to(P3(1.45, YM + 0.55)), M("p_2", size=34).move_to(P3(1.45, YM + 0.05)),
                    txt("P TOTAL", 18, color=MAG).move_to(P3(1.6, YM - 0.55)))
        caso = txt("CASO: REBATEM", 16, op=0.6).move_to(pg.get_corner(UR) + P3(-1.0, -0.22))
        la = M(r"\text{área} = J", size=30, color=JC).move_to(ax.c2p(0.5, 0.42))
        self.an("C02-2")
        self.play(FadeIn(pg), Create(ax), FadeIn(axl), Create(curva), FadeIn(caso), run_time=1.0)
        self.an("C02-2", "embaixo")
        self.play(FadeIn(pm), FadeIn(zero), FadeIn(mv), FadeIn(lm), run_time=0.8)
        self.wait(0.8)
        self.an("C02-2", "a forma da curva")
        self.play(Indicate(curva, color=JC, scale_factor=1.04), run_time=0.9)
        cron.set(0)
        self.play(c.t.animate.set_value(0.0), rate_func=linear, run_time=1.5)
        self.an("C02-3")
        cron.set(1)

        def forcas():
            f = np.sin(PI * s.get_value())
            if f < 0.03:
                return VGroup()
            y = c.ty + max(c.w1, c.w2) + 0.3
            return VGroup(arrow(P3(c.xc - 0.03, y), P3(c.xc - 0.03 - 1.4 * f, y), color=FC, width=7, tip=0.24),
                          arrow(P3(c.xc + 0.03, y), P3(c.xc + 0.03 + 1.4 * f, y), color=FC, width=7, tip=0.24)).set_z_index(12)

        fz = always_redraw(forcas)
        c.ao.set_value(0)
        self.add(area, fz)
        self.play(s.animate.set_value(0.5), rate_func=rate_functions.ease_in_sine, run_time=2.1)
        self.an("C02-3", "enquanto a área cresce")
        self.play(s.animate.set_value(1.0), rate_func=rate_functions.ease_out_sine, run_time=2.1)
        self.remove(fz)
        self.an("C02-3", "mas olha o total")
        self.play(FadeIn(la), Indicate(lm[2], color=MAG), run_time=0.9)
        self.wait(0.6)
        dl = M(r"\Delta p_1", "=", r"-\Delta p_2", size=M_MID).move_to(P3(-3.6, 1.55))
        self.an("C02-4")
        self.play(FadeIn(dl, shift=0.1 * UP), run_time=0.7)
        self.wait(0.8)
        h1 = self.hl("AS FORÇAS INTERNAS TROCAM MOMENTO.", y=-2.5, size=26, x=-3.1)
        self.an("C02-5")
        self.play(FadeIn(h1), run_time=0.6)
        self.wait(0.6)
        h2 = self.hl("O TOTAL NÃO MUDA.", y=-2.5, size=30, x=-3.1, color=MAG)
        self.an("C02-5", "mas o total")
        self.play(ReplacementTransform(h1, h2), Indicate(lm[2], color=MAG), run_time=0.8)
        self.wait(1.0)
        c.t.set_value(1e-5)
        cron.set(2)
        # impulso externo: sistema, J_ext ≈ 0, modelo ideal
        area.clear_updaters()
        mv.clear_updaters()
        self.an("C02-6")
        self.play(c.t.animate.set_value(1.3), c.ao.animate.set_value(1),
                  *[FadeOut(x) for x in (pg, ax, axl, curva, area, h2, dl, la, caso)], rate_func=linear, run_time=1.4)
        sist = contorno(VGroup(c.b1, c.b2, c.arrows), buff=0.22)
        ls = txt("SISTEMA", T_SMALL, op=0.8).next_to(sist, UP, buff=0.1)
        self.an("C02-6", "aqui o sistema")
        self.play(Create(sist), FadeIn(ls), run_time=0.8)
        self.an("C02-6", "as forças entre eles")
        self.dica("ESCOLHA O SISTEMA", pos=P3(-3.6, -2.5))
        e1 = M(r"J_{\mathrm{ext}}", r"\approx", "0", size=M_MID).move_to(P3(4.0, 2.05))
        e2 = M(r"\Delta P", r"\approx", "0", size=M_MID).move_to(P3(4.0, 1.3))
        # forças de fora (atrito, ar): pequenas e contrárias ao movimento de cada bloco
        yb = c.ty + 0.15
        fat = VGroup(arrow(P3(c.x1() - c.w1 / 2 - 0.08, yb), P3(c.x1() - c.w1 / 2 - 0.08 + 0.45, yb), color=FC, width=3,
                           tip=0.12, op=0.75),
                     arrow(P3(c.x2() + c.w2 / 2 + 0.08, yb), P3(c.x2() + c.w2 / 2 + 0.08 - 0.45, yb), color=FC, width=3,
                           tip=0.12, op=0.75))
        lfat = txt("ATRITO, AR", 16, op=0.7).next_to(sist, DOWN, buff=0.35)
        self.an("C02-7", "atrito com o trilho")
        self.play(*[GrowArrow(a) for a in fat], FadeIn(lfat), run_time=0.7)
        self.wait(0.6)
        self.an("C02-7", "o impulso externo é")
        self.play(FadeIn(e1), FadeOut(fat), FadeOut(lfat), run_time=0.6)
        self.an("C02-7", "então a variação")
        self.play(FadeIn(e2, shift=0.1 * DOWN), run_time=0.6)
        self.wait(0.6)
        mi = txt("MODELO IDEAL", T_SMALL, op=0.75).move_to(P3(4.0, 0.7))
        e3 = M("P_i", "=", "P_f", size=M_MAIN).move_to(P3(4.0, 0.05))
        self.an("C02-8")
        self.play(FadeIn(mi), run_time=0.4)
        self.an("C02-8", "e aí sim")
        self.play(FadeIn(e3, shift=0.1 * DOWN), run_time=0.7)
        self.play(Create(box(e3, color=MAG)), Indicate(lm[2], color=MAG), run_time=0.7)
        self.wait(2.0)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C03 — tipos de colisão: P TOTAL e K TOTAL lidos do mesmo estado; nomes só depois do fenômeno
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c03_tipos(self):
        self.secao("TIPOS DE COLISÃO")
        nomes = (VGroup(txt("ELÁSTICA", 40, bold=True)), VGroup(txt("INELÁSTICA", 40, bold=True)),
                 VGroup(txt("COMPLETAMENTE", 34, bold=True), txt("INELÁSTICA", 34, bold=True)).arrange(DOWN, buff=0.08))
        eqs = (VGroup(M("P_i", "=", "P_f", size=M_REF), M("K_i", "=", "K_f", size=M_REF)),
               VGroup(M("P_i", "=", "P_f", size=M_REF), M("K_f", "<", "K_i", size=M_REF)),
               VGroup(M("P_i", "=", "P_f", size=M_REF), M("v_1", "=", "v_2", "=", "v_f", size=M_REF)))
        # (âncora de entrada, frase da colisão rodar, contato, frase do nome, frase das equações)
        roteiro = ((("C03-1",), ("C03-1", "lembrando que a energia"), None, ("C03-2", "isso tem nome"), ("C03-2", "momento conservado e")),
                   (("C03-3",), None, ("C03-3", "só que a energia"), ("C03-4",), ("C03-4", "o momento se conserva")),
                   (("C03-5",), None, None, ("C03-5", "é a colisão completamente"), ("C03-5", "e a marca dela")))
        for k, (nm, v1, v2) in enumerate(FINAIS):
            ent, rodar, toque, anome, aeqs = roteiro[k]
            c = self.base_col(v1, v2, junto="v_f" if nm == "ficam juntos" else None, ty=-1.2, xc=-2.9,
                              trilho=(-7.2, 1.1), kx=0.75, ka=0.45, eixo=False, w1=1.15, w2=0.9)
            med = Medidor(c, P3(4.55, -1.0))
            cron = Cron(P3(-2.9, -3.45))
            self.an(*ent)
            self.play(FadeIn(c.group()), FadeIn(med), FadeIn(cron), run_time=0.8)
            if k == 0:                     # K = ½ m v² (lembrete), some antes do nome
                kf = M("K", "=", r"\tfrac{1}{2}", "m", "v^2", size=M_REF).move_to(P3(4.55, 1.5))
                kf[4].set_color(VEL)
                self.an(*rodar)
                self.play(FadeIn(kf, shift=0.1 * UP), run_time=0.7)
                self.wait(0.6)
            else:
                self.wait(0.4)
            c.run(self, 1.4, 1.5, 1.6, cron=cron, at=toque)
            self.wait(1.0)
            if k == 1:
                li = txt("ENERGIA INTERNA", 18, color=HEAT).next_to(med.placa, DOWN, buff=0.12) \
                    .align_to(med.placa, RIGHT)
                self.an("C03-3", "virou energia interna")
                self.play(FadeIn(li), run_time=0.5)
                self.wait(0.8)
            nomes[k].move_to(P3(4.55, 2.45))
            eqs[k].arrange(DOWN, buff=0.22).move_to(P3(4.55, 0.85))
            self.an(*anome)
            self.play(FadeIn(nomes[k], shift=0.1 * UP), *([FadeOut(kf)] if k == 0 else []), run_time=0.7)
            self.an(*aeqs)
            self.play(FadeIn(eqs[k]), run_time=0.7)
            self.wait(2.2)
            c.solta()
            med.solta()
            self.clear(rt=0.6)
        # resumo compacto (não é a explicação principal)
        linhas = []
        for k, (nm, v1, v2) in enumerate(FINAIS):
            mini = estado(v1, v2, nm == "ficam juntos", escala=0.26)
            n = txt(("ELÁSTICA", "INELÁSTICA", "COMPLETAMENTE INELÁSTICA")[k], T_LAB)
            cond = (M("K_i", "=", "K_f", size=M_LAB), M("K_f", "<", "K_i", size=M_LAB), M("v_1", "=", "v_2", size=M_LAB))[k]
            linhas.append(VGroup(mini, n, cond))
        tab = VGroup()
        for i, (mini, n, cond) in enumerate(linhas):
            y = 1.6 - 1.15 * i
            mini.move_to(P3(-4.8, y))
            n.move_to(P3(-0.9, y))
            cond.move_to(P3(3.6, y))
            tab.add(VGroup(mini, n, cond))
        cab = VGroup(M("P_i", "=", "P_f", size=M_LAB).move_to(P3(-0.9, 2.65)), txt("NAS TRÊS", T_SMALL, op=0.7))
        cab[1].next_to(cab[0], RIGHT, buff=0.3)
        self.an("C03-6")
        self.play(LaggedStart(*[FadeIn(VGroup(r[0], r[1])) for r in tab], lag_ratio=0.3), run_time=1.4)
        self.an("C03-6", "o momento se conserva nas")
        self.play(FadeIn(cab, shift=0.1 * DOWN), run_time=0.7)
        self.an("C03-6", "na elástica")
        self.play(FadeIn(tab[0][2], shift=0.1 * LEFT), run_time=0.6)
        self.an("C03-6", "na que gruda")
        self.play(FadeIn(tab[2][2], shift=0.1 * LEFT), run_time=0.6)
        self.an("C03-6", "mas repara na inelástica")
        self.play(FadeIn(tab[1][2], shift=0.1 * LEFT), run_time=0.6)
        nf = txt("NÃO FECHA SOZINHA", 18, color=HEAT).next_to(linhas[1][2], RIGHT, buff=0.3)
        self.an("C03-6", "ela restringe")
        self.play(FadeIn(nf), run_time=0.5)
        self.wait(2.0)
        pay = self.hl("MOMENTO + TIPO DE COLISÃO", y=-2.35, size=40, color=CYAN)
        self.an("C03-7")
        self.play(LaggedStart(*[Indicate(r[0], color=WHITE_, scale_factor=1.08) for r in tab], lag_ratio=0.3), run_time=1.4)
        self.an("C03-7", "o que falta é")
        self.play(FadeIn(pay, scale=0.96), run_time=0.8)
        self.wait(1.6)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C04 — completamente inelástica: as setas finais se fundem em v_f; média ponderada
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c04_juntos(self):
        self.secao("COMPLETAMENTE INELÁSTICA")
        vf = 2 / 3
        c = self.base_col(vf, vf, junto="v_f", ty=-1.9, xc=0.0, kx=0.85, ka=0.55, t0=1.2)
        cron = Cron(P3(0, -3.45)).set(2)
        self.an("C04-1")
        self.play(FadeIn(c.group()), FadeIn(cron), run_time=0.7)
        self.wait(0.6)
        cron.set(0)
        self.play(c.t.animate.set_value(-1.5), run_time=1.0)            # volta ao ANTES
        self.wait(0.5)
        self.play(c.t.animate.set_value(0.0), rate_func=linear, run_time=1.3)
        self.an("C04-1", "no contato")
        cron.set(1)
        # as duas setas se fundem em uma só
        y0 = c.ty + 0.32
        a_1 = arrow(P3(c.x1(), y0 + c.w1), P3(c.x1() + BASE[2] * c.ka, y0 + c.w1), color=VEL, width=6, tip=0.22)
        a_2 = arrow(P3(c.x2(), y0 + c.w2), P3(c.x2() + BASE[3] * c.ka, y0 + c.w2), color=VEL, width=6, tip=0.22)
        c.t.set_value(1e-5)
        cron.set(2)
        alvo = arrow(P3((c.x1() + c.x2()) / 2, y0 + c.w1), P3((c.x1() + c.x2()) / 2 + vf * c.ka, y0 + c.w1), color=VEL, width=6,
                     tip=0.22)
        c.ao.set_value(0)
        self.add(a_1, a_2)
        self.play(c.contato(), ReplacementTransform(VGroup(a_1, a_2), alvo), run_time=0.7)
        self.remove(alvo)
        c.ao.set_value(1)
        self.play(c.t.animate.set_value(1.2), rate_func=linear, run_time=1.2)
        cond = M("v_1", "=", "v_2", "=", "v_f", size=M_MID).move_to(P3(0, -0.15))
        self.an("C04-2")
        self.play(FadeIn(cond, shift=0.1 * UP), run_time=0.7)
        self.wait(0.6)
        self.an("C04-2", "vamos chamar de")
        self.play(Indicate(cond[4], color=VEL), run_time=0.9)
        self.wait(0.4)
        # antes e depois, perto das imagens físicas
        ea = M("m_1u_1", "+", "m_2u_2", size=M_MID).move_to(P3(-4.0, 1.25))
        ed = M("(m_1+m_2)", "v_f", size=M_MID).move_to(P3(4.0, 1.25))
        ta = txt("ANTES", T_SMALL, op=0.7).next_to(ea, UP, buff=0.15)
        td = txt("DEPOIS", T_SMALL, op=0.7).next_to(ed, UP, buff=0.15)
        self.an("C04-3")
        self.play(FadeIn(ea), FadeIn(ta), run_time=0.7)
        self.wait(0.4)
        self.an("C04-3", "depois é como")
        self.play(FadeIn(ed), FadeIn(td), run_time=0.7)
        self.wait(1.0)
        eq = M("m_1u_1", "+", "m_2u_2", "=", "(m_1+m_2)", "v_f", size=M_MAIN).move_to(P3(0, 1.25))
        self.an("C04-4")
        self.play(FadeOut(ta), FadeOut(td), TransformFromCopy(ea, eq[:3]), FadeIn(eq[3]), TransformFromCopy(ed, eq[4:]),
                  FadeOut(ea), FadeOut(ed), run_time=1.2)
        self.settle(eq)
        self.wait(0.3)
        res = M("v_f", "=", r"\frac{m_1u_1+m_2u_2}{m_1+m_2}", size=M_MAIN).move_to(P3(0, 1.25))
        dv = M(r"\div\,(m_1+m_2)", size=M_LAB).set_opacity(0.75).next_to(eq, RIGHT, buff=0.3)
        self.an("C04-4", "sai a velocidade")
        self.play(FadeIn(dv), run_time=0.4)
        self.remap(eq, res, [([0, 1, 2, 4], 2), (5, 0), (3, 1)], rt=1.3, extra=[FadeOut(dv)])
        bres = box(res)
        self.an("C04-4", "o momento total dividido")
        self.play(Create(bres), run_time=0.5)
        self.wait(1.6)

        # média ponderada: eixo de velocidades; equação e ponto atualizam juntos
        c.solta()
        self.play(FadeOut(c.group()), FadeOut(cond), FadeOut(cron), FadeOut(bres), run_time=0.6)
        self.secao("MÉDIA PONDERADA")
        self.an("C04-5")
        self.play(Indicate(res, color=WHITE_, scale_factor=1.04), run_time=1.0)
        m1, m2 = ValueTracker(2.0), ValueTracker(1.0)
        u1, u2 = BASE[2], BASE[3]

        def vfv():
            return (m1.get_value() * u1 + m2.get_value() * u2) / (m1.get_value() + m2.get_value())

        wf = M("v_f", "=", r"\frac{m_1}{m_1+m_2}", "u_1", "+", r"\frac{m_2}{m_1+m_2}", "u_2", size=M_MAIN).move_to(P3(0, 1.25))
        self.an("C04-5", "separando os termos")
        self.play(FadeOut(res, shift=0.1 * UP), run_time=0.4)
        self.play(FadeIn(wf, shift=0.1 * UP), run_time=0.6)
        self.settle(wf)
        self.an("C04-5", "cada velocidade pesa")
        self.play(Indicate(wf[2], color=WHITE_), Indicate(wf[5], color=WHITE_), run_time=1.0)
        KV, X0, Y = 2.4, 0.0, -1.45

        def X(v):
            return X0 + KV * v

        reta = VGroup(arrow(P3(X(-2.6), Y), P3(X(2.7), Y), color=DIM, width=2.5, tip=0.15))
        for v in (-2, -1, 0, 1, 2):
            reta.add(Line(P3(X(v), Y - 0.09), P3(X(v), Y + 0.09)).set_stroke(WHITE_, 2.5, opacity=0.55))
            reta.add(MathTex(str(v), font_size=28, color=WHITE_).set_opacity(0.6).move_to(P3(X(v), Y - 0.36)))
        rv = MathTex(r"v\ (\mathrm{m/s})", font_size=30, color=WHITE_).set_opacity(0.6).next_to(reta[0], RIGHT, buff=0.1)
        rv.shift(DOWN * 0.3)
        mu1 = VGroup(Dot(P3(X(u1), Y), radius=0.08, color=VEL), M("u_1", size=M_LAB).move_to(P3(X(u1), Y - 0.8)))
        mu2 = VGroup(Dot(P3(X(u2), Y), radius=0.08, color=VEL), M("u_2", size=M_LAB).move_to(P3(X(u2), Y - 0.8)))
        self.an("C04-5", "esse eixo aqui")
        self.play(Create(reta), FadeIn(rv), FadeIn(mu1), FadeIn(mu2), run_time=0.9)

        def marcador():
            x = X(vfv())
            return VGroup(Dot(P3(x, Y), radius=0.12, color=VEL).set_z_index(6),
                          M("v_f", size=M_LAB).move_to(P3(x, Y + 0.45)))

        def corpinhos():
            a = 0.45 + 0.13 * m1.get_value()
            b = 0.45 + 0.13 * m2.get_value()
            return VGroup(Corpo("", C1F, a).at(X(u1), Y + 1.05), Corpo("", C2F, b).at(X(u2), Y + 1.05))

        mk = always_redraw(marcador)
        cps = always_redraw(corpinhos)
        nums = VGroup(VGroup(M("m_1", "=", size=M_LAB), DecimalNumber(2.0, num_decimal_places=1, font_size=M_LAB)),
                      VGroup(M("m_2", "=", size=M_LAB), DecimalNumber(1.0, num_decimal_places=1, font_size=M_LAB)),
                      VGroup(M("v_f", "=", size=M_LAB), DecimalNumber(vfv(), num_decimal_places=2, font_size=M_LAB,
                                                                      include_sign=True)))
        for g in nums:
            g.arrange(RIGHT, buff=0.15)
        nums.arrange(RIGHT, buff=0.7).move_to(P3(0, 0.05))
        nums[0][1].add_updater(lambda d: d.set_value(m1.get_value()))
        nums[1][1].add_updater(lambda d: d.set_value(m2.get_value()))
        nums[2][1].add_updater(lambda d: d.set_value(vfv()))
        self.an("C04-6")
        self.play(FadeIn(mk), FadeIn(cps), FadeIn(nums), run_time=0.8)
        self.wait(0.6)
        faixa = Line(P3(X(u2), Y), P3(X(u1), Y)).set_stroke(VEL, 14, opacity=0.28).set_z_index(-1)
        for a, b, ancora in ((4.0, 1.0, "quando a massa um"), (1.0, 1.0, "quando a massa dois"), (1.0, 4.0, None),
                             (2.0, 1.0, "e ele nunca sai")):
            if ancora:
                self.an("C04-6", ancora)
            if a == 2.0:
                self.play(Create(faixa), m1.animate.set_value(a), m2.animate.set_value(b), run_time=1.8)
            else:
                self.play(m1.animate.set_value(a), m2.animate.set_value(b), run_time=1.8)
            self.wait(0.6)
        h = self.hl("A MASSA MAIOR PESA MAIS NO RESULTADO.", y=-3.35, size=30)
        self.an("C04-7")
        self.play(FadeIn(h), run_time=0.6)
        self.wait(2.0)
        for x in nums:
            x[1].clear_updaters()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C05 — momento conservado não significa K conservada
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c05_energia(self):
        self.secao("ENERGIA CINÉTICA")
        q = self.hl("METADE DA VELOCIDADE = METADE DA ENERGIA?", y=2.9, size=32)
        self.an("C05-1")
        self.play(FadeIn(q), run_time=0.7)
        c = Col(1, 1, 2.0, 0.0, 1.0, 1.0, w1=0.85, w2=0.85, xc=-3.6, ty=0.45, kx=0.75, ka=0.65, t0=-1.6,
                n1="m", n2="m", pre=("u_1", False), junto="v_f", trilho=(-7.2, 0.4), eixo=False)
        cond = M("m_1", "=", "m_2", "=", "m", r",\quad", "u_2", "=", "0", size=M_LAB).move_to(P3(3.7, 2.05))
        # barras de K na mesma escala (m = 1 kg, u = 2 m/s → K_i = 2 J, K_f = 1 J), vivas durante a colisão
        KE, XB, YB = 2.1, -6.6, -1.35
        pk = placa(5.6, 1.9, P3(-3.9, -1.75))
        bi = barra(XB + 0.95, YB, 2 * KE, CYAN)
        li = M("K_i", size=M_LAB).move_to(P3(XB + 0.45, YB))
        lf = M("K", size=M_LAB).move_to(P3(XB + 0.45, YB - 0.75))
        kv = ValueTracker(0.0)

        def kbar():
            k = 2.0 - 1.0 * kv.get_value()
            g = VGroup(barra(XB + 0.95, YB - 0.75, k * KE, CYAN))
            if kv.get_value() > 0.01:
                g.add(barra(XB + 0.95 + k * KE, YB - 0.75, (2.0 - k) * KE, INT, op=0.8))
            return g

        bf = always_redraw(kbar)
        self.an("C05-1", "dois blocos de massas")
        self.play(FadeIn(c.group()), FadeIn(cond), run_time=0.8)
        self.wait(0.6)
        self.an("C05-1", "se a velocidade cair")
        self.play(Indicate(q, color=WHITE_, scale_factor=1.04), run_time=1.0)
        self.wait(0.4)
        self.an("C05-2")
        self.play(FadeIn(pk), FadeIn(bi), FadeIn(li), FadeIn(bf), FadeIn(lf), run_time=0.8)
        self.play(c.t.animate.set_value(0.0), rate_func=linear, run_time=1.5 * LENTO)
        c.t.set_value(1e-5)
        self.an("C05-2", "no contato")
        self.play(c.contato(), kv.animate.set_value(1.0), run_time=1.0)
        li2 = txt("ENERGIA INTERNA", 18, color=HEAT).move_to(P3(XB + 0.95 + 1.5 * KE, YB - 1.2))
        self.an("C05-2", "e o que sai dela")
        self.play(FadeIn(li2), run_time=0.6)
        self.an("C05-2", "pelo momento")
        self.play(c.t.animate.set_value(1.2), rate_func=linear, run_time=1.2 * LENTO)
        bf.clear_updaters()
        lf2 = M("K_f", size=M_LAB).move_to(lf)
        self.play(ReplacementTransform(lf, lf2), run_time=0.4)
        self.wait(0.8)
        # conta à direita, termo a termo
        XE = 3.7
        k1 = M("K_i", "=", r"\tfrac{1}{2}", "m", "u_1^2", size=M_MID).move_to(P3(XE, 1.3))
        self.an("C05-3", "antes a energia")
        self.play(FadeIn(k1), run_time=0.7)
        self.wait(0.8)
        k2 = M("K_f", "=", r"\tfrac{1}{2}", "(2m)", r"\left(\tfrac{u_1}{2}\right)^2", size=M_MID).move_to(P3(XE, -0.1))
        self.an("C05-4")
        self.play(FadeIn(k2), run_time=0.8)
        b1 = Brace(k2[3], DOWN, buff=0.08, color=WHITE_).set_opacity(0.6)
        n1 = txt("MASSA ×2", 20, op=0.85).next_to(b1, DOWN, buff=0.08)
        self.an("C05-4", "dobrou")
        self.play(FadeIn(b1), FadeIn(n1), run_time=0.5)
        b2 = Brace(k2[4], DOWN, buff=0.08, color=WHITE_).set_opacity(0.6)
        n2 = txt("VELOCIDADE ÷2", 20, op=0.85).next_to(b2, DOWN, buff=0.08).shift(DOWN * 0.4)
        self.an("C05-4", "e a velocidade caiu")
        self.play(FadeIn(b2), FadeIn(n2), run_time=0.5)
        self.wait(0.9)
        k3 = M("K_f", "=", r"\tfrac{1}{2}", "(2m)", r"\frac{u_1^2}{4}", size=M_MID).move_to(k2)
        n3 = txt("QUADRADO ÷4", 20, color=CYAN).next_to(k3[4], DOWN, buff=0.25)
        self.play(FadeOut(b2), FadeOut(n2), FadeOut(b1), FadeOut(n1), run_time=0.4)
        self.an("C05-5", "metade ao quadrado")
        self.remap(k2, k3, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], rt=1.0)
        self.play(FadeIn(n3), run_time=0.4)
        self.wait(0.6)
        k4 = M("K_f", "=", r"\tfrac{1}{4}", "m", "u_1^2", size=M_MID).move_to(k2)
        self.play(FadeOut(n3), run_time=0.3)
        self.an("C05-5", "dobro da massa")
        self.remap(k3, k4, [(0, 0), (1, 1), ([2, 3, 4], [2, 3, 4])], rt=1.0)
        self.wait(0.6)
        k5 = M("K_f", "=", r"\tfrac{1}{2}", "K_i", size=M_MAIN).move_to(k2)
        self.an("C05-6")
        self.remap(k4, k5, [(0, 0), (1, 1), ([2, 3, 4], [2, 3])], rt=1.0)
        self.play(Create(box(k5, color=CYAN)), Indicate(bf, color=CYAN, scale_factor=1.05), run_time=1.0)
        self.an("C05-6", "a outra metade")
        self.play(Indicate(li2, color=HEAT), run_time=0.9)
        self.wait(1.4)
        self.clear()
        p1 = self.hl("P CONSERVADO", y=1.2, size=56, color=MAG)
        p2 = txt("NÃO IMPLICA", T_MAIN, op=0.7).move_to(P3(0, 0.0))
        p3 = self.hl("K CONSERVADA", y=-1.2, size=56, color=CYAN)
        self.an("C05-7", "momento conservado")
        self.play(FadeIn(p1, shift=0.1 * UP), run_time=0.7)
        self.an("C05-7", "não implica")
        self.play(FadeIn(p2), run_time=0.5)
        self.an("C05-7", "energia cinética conservada")
        self.play(FadeIn(p3, shift=0.1 * DOWN), run_time=0.7)
        self.wait(2.4)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C06 — colisão elástica: as equações nascem dos medidores; a física fica visível como âncora
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c06_elastica(self):
        self.secao("COLISÃO ELÁSTICA")
        m1, m2, u1, u2, v1, v2 = 1.0, 2.0, 3.0, 0.0, -1.0, 2.0
        c = Col(m1, m2, u1, u2, v1, v2, w1=0.8, w2=1.0, xc=-3.4, ty=-0.6, kx=0.7, ka=0.42, t0=-1.6,
                pre=("u_1", "u_2=0"), trilho=(-7.2, 0.4), eixo=False)
        med = Medidor(c, P3(4.3, -0.3), kp=0.6, ke=0.33)
        cron = Cron(P3(-3.4, -3.45))
        self.an("C06-1")
        self.play(FadeIn(c.group()), FadeIn(med), FadeIn(cron), run_time=0.8)
        self.wait(0.8)
        self.an("C06-1", "repara nos medidores")
        c.run(self, 1.3, 1.5, 1.4, cron=cron)
        self.wait(1.2)
        # as duas equações nascem dos medidores (uma de cada vez)
        # âncora: a colisão e os medidores sobem para uma faixa superior legível
        c.solta()
        med.solta()
        fis = VGroup(c.track, c.b1, c.b2, c.arrows)
        self.play(FadeOut(cron), fis.animate.scale(0.62).move_to(P3(-4.75, 2.25)), med.animate.scale(0.62).move_to(P3(-0.55, 2.25)),
                  run_time=1.0)
        P = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2v_2", size=M_MAIN).move_to(P3(0.6, 0.6))
        self.an("C06-2")
        self.play(TransformFromCopy(med.lP, P), run_time=1.1)
        self.settle(P)
        self.wait(0.4)
        P2 = M("m_1u_1", "-", "m_1v_1", "=", "m_2v_2", "-", "m_2u_2", size=M_MAIN).move_to(P)
        self.an("C06-3")
        P = self.swap(P, P2, rt=1.3)
        self.wait(0.8)
        P3_ = M("m_1", "(u_1-v_1)", "=", "m_2", "(v_2-u_2)", size=M_MAIN).move_to(P)
        self.an("C06-3", "a massa um vezes")
        self.remap(P, P3_, [([0, 2], [0, 1]), (3, 2), ([4, 6], [3, 4])], rt=1.2)
        P = P3_
        self.play(Indicate(P[1], color=WHITE_), run_time=0.8)
        self.an("C06-3", "é igual à massa dois")
        self.play(Indicate(P[4], color=WHITE_), run_time=0.8)
        self.wait(0.4)
        n1 = M("(1)", size=M_LAB).set_opacity(0.6)
        self.an("C06-3", "essa é a equação um")
        self.play(P.animate.scale(0.62).move_to(P3(4.1, 2.55)), run_time=0.8)
        n1.next_to(P, RIGHT, buff=0.22)
        self.play(FadeIn(n1), run_time=0.3)
        # energia (nasce do medidor de K)
        E = M(r"\tfrac{1}{2}m_1u_1^2", "+", r"\tfrac{1}{2}m_2u_2^2", "=", r"\tfrac{1}{2}m_1v_1^2", "+",
              r"\tfrac{1}{2}m_2v_2^2", size=M_MAIN, w=13.2).move_to(P3(0.6, 0.4))
        self.an("C06-4")
        self.play(TransformFromCopy(med.lK, E), run_time=1.2)
        self.settle(E)
        self.wait(0.6)
        xl = M(r"\times 2", size=M_LAB, color=CYAN).next_to(E[:3], DOWN, buff=0.22)
        xr = M(r"\times 2", size=M_LAB, color=CYAN).next_to(E[4:], DOWN, buff=0.22)
        self.an("C06-4", "e aqui está a ideia")
        self.play(FadeIn(xl), FadeIn(xr), run_time=0.5)
        E2 = M("m_1u_1^2", "+", "m_2u_2^2", "=", "m_1v_1^2", "+", "m_2v_2^2", size=M_MAIN).move_to(E)
        self.remap(E, E2, [(i, i) for i in range(7)], rt=1.0, extra=[FadeOut(xl), FadeOut(xr)])
        E = E2
        self.an("C06-4", "conversar com a do momento")
        self.play(Indicate(P, color=MAG, scale_factor=1.05), run_time=0.9)
        self.wait(0.3)
        E3 = M("m_1u_1^2", "-", "m_1v_1^2", "=", "m_2v_2^2", "-", "m_2u_2^2", size=M_MAIN).move_to(E)
        self.an("C06-5")
        E = self.swap(E, E3, rt=1.2)
        self.wait(0.5)
        E4 = M("m_1", r"(u_1^2-v_1^2)", "=", "m_2", r"(v_2^2-u_2^2)", size=M_MAIN).move_to(E)
        self.an("C06-5", "até aparecerem")
        self.remap(E, E4, [([0, 2], [0, 1]), (3, 2), ([4, 6], [3, 4])], rt=1.2)
        E = E4
        self.wait(0.6)
        # diferença de quadrados: direto na expressão física, um lado de cada vez
        bL = box(E[1], color=WHITE_, buff=0.07)
        dica = M(r"a^2-b^2=(a-b)(a+b)", size=30).set_opacity(0.6).next_to(E, DOWN, buff=0.45)
        self.an("C06-6")
        self.play(Create(bL), FadeIn(dica), run_time=0.5)
        E5 = M("m_1", "(u_1-v_1)(u_1+v_1)", "=", "m_2", r"(v_2^2-u_2^2)", size=M_MAIN, w=11.4).move_to(P3(0.1, 0.4))
        self.remap(E, E5, [(0, 0), (2, 2), (3, 3), (4, 4)], rt=1.2, extra=[FadeOut(bL)])
        E = E5
        self.wait(0.3)
        bR = box(E[4], color=WHITE_, buff=0.07)
        self.an("C06-6", "surgem exatamente")
        self.play(Create(bR), run_time=0.4)
        E6 = M("m_1", "(u_1-v_1)", "(u_1+v_1)", "=", "m_2", "(v_2-u_2)", "(v_2+u_2)", size=M_MAIN, w=11.4).move_to(P3(0.1, 0.4))
        self.remap(E, E6, [(0, 0), (1, [1, 2]), (2, 3), (3, 4)], rt=1.2, extra=[FadeOut(bR), FadeOut(dica)])
        E = E6
        n2 = M("(2)", size=M_LAB).set_opacity(0.6).next_to(E, RIGHT, buff=0.3)
        self.an("C06-7")
        self.play(FadeIn(n2), run_time=0.3)
        self.an("C06-7", "e agora as duas")
        self.play(Indicate(P[1], color=WHITE_), Indicate(E[1], color=WHITE_), Indicate(P[4], color=WHITE_),
                  Indicate(E[5], color=WHITE_), run_time=1.0)
        self.wait(0.4)
        # não dividir cegamente: o fator m1(u1 − v1) pode ser zero; usar (1) dentro de (2)
        div = M(r"\frac{(2)}{(1)}", r"\,?", size=M_LAB).set_opacity(0.8).move_to(P3(0.1, -1.55))
        self.an("C06-8", "a tentação é dividir")
        self.play(FadeIn(div, shift=0.1 * UP), run_time=0.6)
        fm = box(VGroup(E[0], E[1]), color=WHITE_, buff=0.07)
        self.an("C06-8", "mas esse fator")
        self.play(Create(fm), run_time=0.5)
        corte = Line(div.get_corner(DL) + P3(-0.1, -0.05), div.get_corner(UR) + P3(0.1, 0.05)).set_stroke(HEAT, 4)
        self.an("C06-8", "e dividir por zero")
        self.play(Create(corte), run_time=0.5)
        self.wait(0.6)
        self.an("C06-8", "então a gente faz diferente")
        self.play(FadeOut(fm), FadeOut(div), FadeOut(corte), run_time=0.5)
        bA = box(VGroup(E[4], E[5]), color=MAG, buff=0.07)
        bB = box(VGroup(P[3], P[4]), color=MAG, buff=0.07)
        self.an("C06-9")
        self.play(Create(bA), Create(bB), run_time=0.7)
        bC = box(VGroup(P[0], P[1]), color=MAG, buff=0.07)
        self.an("C06-9", "então a gente usa")
        self.play(ReplacementTransform(bB, bC), run_time=0.6)
        E7 = M("m_1", "(u_1-v_1)", "(u_1+v_1)", "=", "m_1", "(u_1-v_1)", "(v_2+u_2)", size=M_MAIN, w=11.4).move_to(E)
        self.play(FadeOut(bA), FadeOut(E[4]), FadeOut(E[5]), FadeOut(n2),
                  ReplacementTransform(VGroup(*E[:4], E[6]).copy(), VGroup(*E7[:4], E7[6])),
                  FadeIn(E7[4], shift=0.1 * DOWN), FadeIn(E7[5], shift=0.1 * DOWN), run_time=1.3)
        self.drop(E)
        self.settle(E7)
        E = E7
        self.play(FadeOut(bC), run_time=0.3)
        self.wait(0.8)
        E8 = M("m_1", "(u_1-v_1)", "(u_1+v_1)", "-", "m_1", "(u_1-v_1)", "(v_2+u_2)", "=", "0", size=M_MAIN,
               w=13.6).move_to(E)
        self.an("C06-10")
        self.remap(E, E8, [(0, 0), (1, 1), (2, 2), (3, 7), (4, 4), (5, 5), (6, 6)], rt=1.1)
        E = E8
        self.wait(0.4)
        E9 = M("m_1", "(u_1-v_1)", r"\big[", "(u_1+v_1)", "-", "(v_2+u_2)", r"\big]", "=", "0", size=M_MAIN).move_to(E)
        self.an("C06-10", "aparece um produto")
        self.remap(E, E9, [([0, 4], 0), ([1, 5], 1), (2, 3), (3, 4), (6, 5), (7, 7), (8, 8)], rt=1.3)
        E = E9
        self.an("C06-10", "a massa não é zero")
        self.play(Indicate(E[0], color=WHITE_), run_time=0.8)
        # dois ramos
        XA, XB = -3.6, 3.6
        sep = DashedLine(P3(0.0, 0.3), P3(0.0, -3.3)).set_stroke(WHITE_, 1.5, opacity=0.35)
        self.an("C06-10", "então ou o primeiro")
        self.play(FadeOut(P), FadeOut(n1), E.animate.scale(0.82).move_to(P3(1.2, 1.0)), run_time=0.8)
        a1 = arrow(E[1].get_bottom() + DOWN * 0.08, P3(XA, 0.1), width=2.5, tip=0.13, op=0.5)
        a2 = arrow(E[3:6].get_bottom() + DOWN * 0.08, P3(XB, 0.1), width=2.5, tip=0.13, op=0.5)
        self.play(Create(sep), GrowArrow(a1), run_time=0.6)
        self.an("C06-10", "ou o colchete")
        self.play(GrowArrow(a2), Indicate(E[2:7], color=WHITE_, scale_factor=1.05), run_time=0.8)
        A1 = M("u_1", "=", "v_1", size=M_MID).move_to(P3(XA, -0.45))
        A2 = M("u_2", "=", "v_2", size=M_MID).move_to(P3(XA, -1.25))
        self.an("C06-11")
        self.play(FadeIn(A1), run_time=0.5)
        self.play(FadeIn(A2), run_time=0.5)
        ma = estado(0, 0, False, escala=0.26, antes=True)
        mb = estado(0, 0, False, escala=0.26, antes=True)
        mini = VGroup(VGroup(ma, txt("ANTES", 16, op=0.7)).arrange(DOWN, buff=0.08),
                      MathTex("=", font_size=40, color=WHITE_),
                      VGroup(mb, txt("DEPOIS", 16, op=0.7)).arrange(DOWN, buff=0.08)).arrange(RIGHT, buff=0.3)
        mini.move_to(P3(XA, -2.15))
        sl = txt("SEM TROCA LÍQUIDA", T_SMALL, op=0.85).move_to(P3(XA, -3.0))
        self.an("C06-11", "nada mudou")
        self.play(FadeIn(mini), FadeIn(sl), run_time=0.7)
        self.wait(1.0)
        ramoA = VGroup(A1, A2, mini, sl, a1)
        self.an("C06-11", "não é o encontro")
        self.play(ramoA.animate.set_opacity(0.25), run_time=0.6)
        B1 = M("u_1", "+", "v_1", "=", "v_2", "+", "u_2", size=M_MID).move_to(P3(XB, -0.45))
        self.an("C06-12")
        self.play(FadeIn(B1), run_time=0.6)
        self.wait(0.6)
        B2 = M("u_1", "-", "u_2", "=", "-", "(v_1-v_2)", size=M_MID).move_to(P3(XB, -1.6))
        self.an("C06-12", "rearrumando")
        self.play(TransformMatchingTex(B1.copy(), B2), run_time=1.1)
        self.settle(B2)
        self.an("C06-12", "guarda essa relação")
        self.play(Create(box(B2, color=CYAN, buff=0.15)), run_time=0.5)
        self.wait(2.0)
        self.clear()

    def c06b_relativa(self):
        self.secao("VELOCIDADE RELATIVA")
        m1, m2, u1, u2, v1, v2 = 1.0, 2.0, 3.0, 0.0, -1.0, 2.0
        c = Col(m1, m2, u1, u2, v1, v2, w1=0.8, w2=1.0, xc=-3.0, ty=-1.0, kx=0.7, ka=0.42, t0=-1.5,
                pre=("u_1", False), trilho=(-7.2, 1.0), eixo=False)

        def regua():
            x1, x2 = c.x1(), c.x2()
            y = c.ty - 0.5
            return VGroup(DoubleArrow(P3(x1, y), P3(x2, y), buff=0, color=GEO, stroke_width=3.5, tip_length=0.15,
                                      max_tip_length_to_length_ratio=0.3),
                          Line(P3(x1, c.ty + 0.35), P3(x1, y - 0.1)).set_stroke(WHITE_, 1.3, opacity=0.5),
                          Line(P3(x2, c.ty + 0.35), P3(x2, y - 0.1)).set_stroke(WHITE_, 1.3, opacity=0.5),
                          MathTex("d", font_size=M_LAB, color=GEO).move_to(P3((x1 + x2) / 2, y - 0.38)))

        rg = always_redraw(regua)
        cron = Cron(P3(-3.0, -3.45))
        self.an("C06b-1")
        self.play(FadeIn(c.group()), FadeIn(rg), FadeIn(cron), run_time=0.8)
        gl = VGroup(MathTex("d", font_size=34, color=GEO), gloss(": distância entre os centros", size=22)) \
            .arrange(RIGHT, buff=0.08).move_to(P3(-3.0, 1.9))
        self.play(FadeIn(gl), run_time=0.5)
        # gráfico d × t (unidades físicas: metros e segundos) no mesmo relógio
        dc = (c.w1 + c.w2) / 2 / c.kx
        tmin, tmax = -1.5, 1.5
        dmax = dc + (u1 - u2) * 1.5
        pg = placa(5.6, 3.0, P3(4.4, 0.5))
        ax = Axes(x_range=[tmin, tmax, 0.5], y_range=[0, dmax * 1.05, 1], x_length=4.4, y_length=2.0, tips=False,
                  axis_config={"color": WHITE_, "stroke_width": 2, "stroke_opacity": 0.55}).move_to(P3(4.5, 0.65))
        axl = VGroup(MathTex("t", font_size=32, color=DIM).next_to(ax.x_axis, RIGHT, buff=0.1),
                     MathTex("d", font_size=32, color=GEO).next_to(ax.y_axis, UP, buff=0.06))

        def dlei(t):
            return dc + ((u2 - u1) if t < 0 else (v2 - v1)) * t

        traco = always_redraw(lambda: ax.plot(dlei, x_range=[tmin, max(c.t.get_value(), tmin + 1e-3)],
                                              color=GEO, stroke_width=4))
        cur = always_redraw(lambda: Dot(ax.c2p(c.t.get_value(), dlei(c.t.get_value())), radius=0.08,
                                        color=WHITE_).set_z_index(6))
        self.an("C06b-1", "no gráfico da direita")
        self.play(FadeIn(pg), Create(ax), FadeIn(axl), run_time=0.8)
        self.add(traco, cur)
        cron.set(0)
        self.an("C06b-2")
        self.play(c.t.animate.set_value(-0.75), rate_func=linear, run_time=1.7)
        ap = txt("APROXIMAÇÃO", 18, op=0.9).move_to(ax.c2p(-0.75, 0) + DOWN * 0.4)
        sa = M(r"\frac{\Delta d}{\Delta t}", "=", "u_2-u_1", "=", r"-3\ \text{m/s}", size=34).move_to(P3(4.4, -1.55))
        self.an("C06b-2", "a inclinação dessa reta")
        self.play(c.t.animate.set_value(0.0), FadeIn(ap), rate_func=linear, run_time=1.7)
        self.an("C06b-2", "aqui a distância diminui")
        self.play(FadeIn(sa), run_time=0.6)
        self.wait(1.4)
        cron.set(1)
        self.an("C06b-3")
        self.play(c.contato())
        c.t.set_value(1e-5)
        cron.set(2)
        self.play(c.t.animate.set_value(1.5), rate_func=linear, run_time=3.4)
        af = txt("AFASTAMENTO", 18, op=0.9).move_to(ax.c2p(0.75, 0) + DOWN * 0.4)
        sb = M(r"\frac{\Delta d}{\Delta t}", "=", "v_2-v_1", "=", r"+3\ \text{m/s}", size=34).move_to(P3(4.4, -2.5))
        self.an("C06b-3", "e repara na inclinação")
        self.play(FadeIn(af), FadeIn(sb), run_time=0.6)
        self.wait(1.2)
        mod = M(r"|u_2-u_1|", "=", r"|v_2-v_1|", size=M_LAB).move_to(P3(-3.0, 1.9))
        self.an("C06b-4")
        self.play(FadeOut(gl), FadeIn(mod), run_time=0.6)
        self.wait(1.4)
        pay = self.hl("A VELOCIDADE RELATIVA INVERTE.", y=2.95, size=36, color=CYAN, x=0.6)
        rel = M("u_1", "-", "u_2", "=", "-", "(v_1-v_2)", size=M_MID).move_to(P3(-3.0, 1.9))
        self.an("C06b-5")
        self.play(ReplacementTransform(mod, rel), run_time=0.8)
        self.play(Create(box(rel, color=CYAN, buff=0.14)), run_time=0.5)
        self.an("C06b-5", "a velocidade relativa inverte")
        self.play(FadeIn(pay, shift=0.1 * UP), run_time=0.8)
        self.wait(1.0)
        self.an("C06b-5", "cada bloco não precisa")
        self.play(Indicate(VGroup(rel[0], rel[1], rel[2]), color=WHITE_), Indicate(rel[5], color=WHITE_), run_time=1.0)
        self.wait(1.6)
        traco.clear_updaters()
        cur.clear_updaters()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C07 — fórmulas gerais: poucos estados, âncora física no canto
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c07_formulas(self):
        self.secao("FÓRMULAS GERAIS")
        anc = VGroup(estado(0, 0, False, escala=0.3, antes=True), MathTex(r"\rightarrow", font_size=36, color=WHITE_),
                     estado(*FINAIS[0][1:], False, escala=0.3)).arrange(RIGHT, buff=0.25).move_to(P3(-4.6, 2.55))
        A = M("P_i", "=", "P_f", size=M_REF).move_to(P3(1.0, 2.75))
        B = M("u_1", "-", "u_2", "=", "v_2", "-", "v_1", size=M_REF).move_to(P3(4.6, 2.75))
        self.an("C07-1")
        self.play(FadeIn(anc), FadeIn(A), run_time=0.8)
        self.an("C07-1", "e a velocidade relativa")
        self.play(FadeIn(B), run_time=0.6)
        self.wait(0.8)
        s1 = M("v_2", "=", "u_1-u_2", "+", "v_1", size=M_REF).move_to(B)
        self.an("C07-2")
        self.play(TransformMatchingTex(B, s1), run_time=1.0)
        self.wait(0.6)
        e1 = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2", "(u_1-u_2+v_1)", size=M_MAIN).move_to(P3(0.4, 0.6))
        bl = box(s1[2:], color=WHITE_, buff=0.06)
        self.play(Create(bl), run_time=0.4)
        self.play(TransformFromCopy(A, e1[:7]), TransformFromCopy(s1[2:], e1[7]), FadeOut(bl), run_time=1.3)
        self.settle(e1)
        self.wait(1.4)
        op = txt("DISTRIBUTIVA + AGRUPAR", T_SMALL, op=0.7).move_to(P3(0.4, -0.6))
        e2 = M("(m_1-m_2)", "u_1", "+", "2m_2u_2", "=", "(m_1+m_2)", "v_1", size=M_MAIN).move_to(e1)
        self.play(FadeIn(op), run_time=0.4)
        self.play(FadeOut(e1, shift=0.15 * UP), FadeIn(e2, shift=0.15 * UP), run_time=1.2)
        self.wait(1.4)
        e3 = M("v_1", "=", r"\frac{m_1-m_2}{m_1+m_2}", "u_1", "+", r"\frac{2m_2}{m_1+m_2}", "u_2", size=M_MAIN).move_to(e1)
        op2 = M(r"\div\,(m_1+m_2)", size=M_LAB).set_opacity(0.75).move_to(op)
        self.play(ReplacementTransform(op, op2), run_time=0.4)
        self.remap(e2, e3, [(6, 0), (4, 1), ([0, 5], 2), (1, 3), (2, 4), (3, [5, 6])], rt=1.3)
        b3 = box(e3)
        self.an("C07-4")
        self.play(Create(b3), FadeOut(op2), run_time=0.5)
        self.wait(1.2)
        e4 = M("v_2", "=", r"\frac{2m_1}{m_1+m_2}", "u_1", "+", r"\frac{m_2-m_1}{m_1+m_2}", "u_2", size=M_MAIN) \
            .move_to(P3(0.4, -1.75))
        op3 = M(r"v_2=u_1-u_2+v_1", size=34).set_opacity(0.7).next_to(e4, DOWN, buff=0.3)
        self.an("C07-5")
        self.play(Indicate(s1, color=WHITE_), FadeIn(op3), run_time=0.8)
        self.play(FadeIn(e4, shift=0.15 * DOWN), run_time=1.0)
        b4 = box(e4)
        self.play(Create(b4), run_time=0.5)
        self.wait(1.6)
        res = VGroup(VGroup(e3, b3), VGroup(e4, b4))
        self.an("C07-6")
        self.play(FadeOut(op3), FadeOut(A), FadeOut(s1), res.animate.arrange(DOWN, buff=0.2).scale(0.5).move_to(P3(3.4, 2.4)),
                  run_time=0.9)
        h1 = self.hl("RESULTADO ≠ MÉTODO", y=0.6, size=52)
        self.an("C07-6", "essas fórmulas são")
        self.play(FadeIn(h1, scale=0.96), run_time=0.7)
        so = txt("SÓ ELÁSTICA · 1D", 18, op=0.75).next_to(res, DOWN, buff=0.15)
        self.an("C07-6", "elas valem para")
        self.play(FadeIn(so), Indicate(res, color=WHITE_, scale_factor=1.04), run_time=0.9)
        h2 = VGroup(txt("MÉTODO:", T_MAIN, op=0.7), txt("MOMENTO + CONDIÇÃO DA COLISÃO", T_MAIN, color=CYAN, bold=True)) \
            .arrange(RIGHT, buff=0.3).move_to(P3(0, -0.6))
        self.an("C07-6", "o método é sempre")
        self.play(FadeIn(h2), run_time=0.7)
        self.wait(1.8)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C08 — casos-limite: PREVISÃO → MOVIMENTO → CONFERE (massas finitas; ≈ na tela)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c08_limites(self):
        self.secao("CASOS-LIMITE")
        g1 = M("v_1", "=", r"\frac{m_1-m_2}{m_1+m_2}", "u_1", size=M_REF)
        g2 = M("v_2", "=", r"\frac{2m_1}{m_1+m_2}", "u_1", size=M_REF)
        lu = M(r"u_2=0", size=M_LAB).set_opacity(0.75)
        topo = VGroup(lu, g1, g2).arrange(RIGHT, buff=0.8).move_to(P3(0.9, 2.65))
        self.an("C08-1")
        self.play(FadeIn(topo), run_time=0.8)
        self.an("C08-1", "com o segundo bloco parado")
        self.play(Indicate(lu, color=WHITE_), run_time=0.9)
        self.wait(0.8)
        u1 = 2.4
        casos = (
            (1.0, 1.0, 0.85, 0.85, "MASSAS IGUAIS", M("m_1", "=", "m_2", size=M_MID), None,
             (M("v_1", "=", "0", size=M_MID), M("v_2", "=", "u_1", size=M_MID))),
            (1.0, 30.0, 0.7, 1.15, "LEVE CONTRA PESADO", M("m_1", r"\ll", "m_2", size=M_MID), "REBATE.",
             (M("v_1", r"\approx", "-u_1", size=M_MID), M("v_2", r"\approx", "0", size=M_MID))),
            (30.0, 1.0, 1.15, 0.7, "PESADO CONTRA LEVE", M("m_1", r"\gg", "m_2", size=M_MID),
             "O LEVE PODE SAIR MAIS RÁPIDO QUE O INCIDENTE.",
             (M("v_1", r"\approx", "u_1", size=M_MID), M("v_2", r"\approx", "2u_1", size=M_MID))),
        )
        # âncoras por caso: entrada, pergunta, contato, (frase, evento) depois do contato
        roteiro = ((("C08-2",), ("C08-2", "pensa um pouco"), ("C08-3",),
                    (("C08-3", "as fórmulas dão"), "rs"), (("C08-3", "confere"), "ok")),
                   (("C08-4",), ("C08-4", "na animação"), ("C08-5",),
                    (("C08-5", "e o pesado mal"), "rs"), (("C08-5", "repara na marquinha"), "mk"), (("C08-5", "por isso está escrito"), "ind"),
                    (("C08-5", "é como uma bolinha"), "nt"), (("C08-5", "rebate"), "ok")),
                   (("C08-6",), None, ("C08-7",),
                    (("C08-7", "e o leve sai"), "rs"), (("C08-7", "quase o dobro"), "ind"), (("C08-7", "parece estranho"), "nt"),
                    (("C08-7", "a energia que o leve"), "ok")))
        for (m1, m2, w1, w2, titulo, hip, nota, res), (ent, perg, toque, *depois) in zip(casos, roteiro):
            v1 = (m1 - m2) / (m1 + m2) * u1
            v2 = 2 * m1 / (m1 + m2) * u1
            c = Col(m1, m2, u1, 0.0, v1, v2, w1=w1, w2=w2, xc=-1.3, ty=-2.2, kx=0.85, ka=0.42, t0=-1.5,
                    pre=("u_1", "u_2=0"), post=("v_1" if abs(v1) > 0.05 else "v_1=0", "v_2"), eixo=False)
            t = txt(titulo, 38, bold=True).move_to(P3(-3.6, 1.45))
            hip.move_to(P3(-3.6, 0.6))
            self.an(*ent)
            self.play(FadeIn(c.group()), FadeIn(t), FadeIn(hip), run_time=0.8)
            pq = txt("O QUE VOCÊ ESPERA?", T_LAB, op=0.85).move_to(P3(3.4, 1.0))
            if perg:
                self.an(*perg)
            if m2 > m1:                      # a razão real das massas (o tamanho dos blocos não é escala)
                r30 = M("m_2", "=", "30", "m_1", size=34).set_opacity(0.75).next_to(hip, DOWN, buff=0.25)
                self.play(FadeIn(pq), FadeIn(r30), run_time=0.6)
            else:
                self.play(FadeIn(pq), run_time=0.5)
            self.wait(1.0)
            x2a = c.x2()
            c.run(self, 1.6, 1.2, 1.8, at=toque)
            rs = VGroup(*res).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(P3(3.4, 0.75))
            ok = VGroup(txt("CONFERE", T_LAB, color=CYAN), M(r"\checkmark", size=40, color=CYAN)).arrange(RIGHT, buff=0.15)
            ok.next_to(rs, DOWN, buff=0.3)
            for anc_, ev in depois:
                self.an(*anc_)
                if ev == "rs":
                    self.play(FadeOut(pq), FadeIn(rs, shift=0.1 * DOWN), run_time=0.7)
                elif ev == "mk":
                    x2b = c.x2()
                    y = c.ty - 0.32
                    mk = VGroup(Line(P3(x2a, y - 0.12), P3(x2a, y + 0.12)), Line(P3(x2b, y - 0.12), P3(x2b, y + 0.12)),
                                Line(P3(x2a, y), P3(x2b, y))).set_stroke(GEO, 3)
                    lm = M(r"\Delta x_2", r">0", size=34, color=GEO).next_to(mk, DOWN, buff=0.1)
                    self.play(Create(mk), FadeIn(lm), run_time=0.6)
                elif ev == "ind":
                    self.play(Indicate(rs[1], color=WHITE_), run_time=0.9)
                elif ev == "nt":
                    if len(nota) > 20:
                        nt = VGroup(txt("O LEVE PODE SAIR", 30, bold=True), txt("MAIS RÁPIDO QUE O INCIDENTE.", 30, bold=True)) \
                            .arrange(DOWN, buff=0.1)
                    else:
                        nt = txt(nota, 34, bold=True)
                    nt.move_to(t)
                    self.play(FadeOut(t), FadeOut(hip), *([FadeOut(r30)] if m2 > m1 else []), run_time=0.35)
                    self.play(FadeIn(nt), run_time=0.45)
                elif ev == "ok":
                    self.play(FadeIn(ok), run_time=0.5)
                self.wait(0.6)
            self.wait(1.2)
            c.solta()
            self.clear(topo, rt=0.5)
        self.play(FadeOut(topo), run_time=0.4)
        s = self.hl("CASOS-LIMITE = TESTES DE PLAUSIBILIDADE", y=0.5, size=36, color=CYAN)
        d = self.hl("TESTE SUA RESPOSTA.", y=-0.5, size=30)
        self.an("C08-8")
        self.play(FadeIn(s, scale=0.96), run_time=0.8)
        self.an("C08-8", "achou uma fórmula")
        self.play(FadeIn(d), run_time=0.6)
        self.wait(2.0)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C09–C11 — pêndulo balístico bifilar (bloco translada sem girar); linha do tempo A → B → C
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def _pendulo(self):
        PX, PY = -3.2, 2.45
        self.PX, self.PY = PX, PY
        self.th = ValueTracker(0.0)
        self.bx = ValueTracker(-6.7)
        self.dentro = False
        BW, BH, A = 1.6, 0.85, 0.55
        self.BW, self.BH = BW, BH
        Lsc = PL * ESC

        def centro():
            th = self.th.get_value()
            return P3(PX + Lsc * np.sin(th), PY - Lsc * np.cos(th) - BH / 2)

        self.centro = centro
        teto = VGroup(Line(P3(PX - 1.3, PY), P3(PX + 1.3, PY)).set_stroke(WHITE_, 3, opacity=0.6),
                      *[Line(P3(x - 0.1, PY + 0.18), P3(x + 0.1, PY)).set_stroke(WHITE_, 1.5, opacity=0.45)
                        for x in np.linspace(PX - 1.2, PX + 1.2, 10)])
        piv = VGroup(Dot(P3(PX - A, PY), radius=0.055, color=WHITE_), Dot(P3(PX + A, PY), radius=0.055, color=WHITE_))

        def desenho():
            cc = centro()
            blk = Corpo("M", C2F, BW, size=40, alt=BH).at(cc[0], cc[1] - BH / 2)
            top = cc[1] + BH / 2
            fios = VGroup(Line(P3(PX - A, PY), P3(cc[0] - A, top)), Line(P3(PX + A, PY), P3(cc[0] + A, top))) \
                .set_stroke(WHITE_, 2, opacity=0.7)
            g = VGroup(fios, blk)
            if self.dentro:
                g.add(RoundedRectangle(corner_radius=0.03, width=0.2, height=0.2, stroke_width=2, stroke_color=WHITE_, fill_color=C1F,
                                       fill_opacity=1).move_to(cc + LEFT * (BW / 2 - 0.22)).set_z_index(5))
            return g

        def bala():
            if self.dentro:
                return VGroup()
            y = centro()[1]
            b = RoundedRectangle(corner_radius=0.03, width=0.2, height=0.2, stroke_width=2, stroke_color=WHITE_, fill_color=C1F,
                                 fill_opacity=1).move_to(P3(self.bx.get_value(), y))
            return VGroup(b, MathTex("m", font_size=34, color=WHITE_).next_to(b, DOWN, buff=0.12))

        self.estat = VGroup(teto, piv)
        self.pend = always_redraw(desenho)
        self.bal = always_redraw(bala)
        self.xin = PX - BW / 2 + 0.22

    def _th(self, tau):
        return float(np.interp(tau, SUB_T, SUB_TH))

    def _om(self, tau):
        return float(np.interp(tau, SUB_T, SUB_W))

    def _timeline(self):
        """A — ANTES DO IMPACTO → B — LOGO DEPOIS → C — ALTURA MÁXIMA (faixa inferior)."""
        xs = (-5.4, 0.0, 5.4)
        y = -3.45
        nos = VGroup(*[Dot(P3(x, y), radius=0.07, color=WHITE_) for x in xs])
        rot = VGroup(txt("A — ANTES DO IMPACTO", 18, op=0.85), txt("B — LOGO DEPOIS", 18, op=0.85),
                     txt("C — ALTURA MÁXIMA", 18, op=0.85))
        for r, x in zip(rot, xs):
            r.move_to(P3(x, y + 0.32))
        seg = VGroup(Line(P3(xs[0] + 0.12, y), P3(xs[1] - 0.12, y)), Line(P3(xs[1] + 0.12, y), P3(xs[2] - 0.12, y))) \
            .set_stroke(WHITE_, 3, opacity=0.3)
        self.tl = VGroup(seg, nos, rot)
        self.tl_seg = seg
        return self.tl

    def _acende(self, k, cor):
        alvo = self.tl_seg[k].copy().set_stroke(cor, 6, opacity=1.0)
        return Transform(self.tl_seg[k], alvo)

    def _marca_h(self):
        yB = self.PY - PL * ESC - self.BH / 2
        yC = self.centro()[1]
        xr = self.centro()[0] + self.BW / 2 + 0.35
        l0 = DashedLine(P3(self.PX - 1.2, yB), P3(xr, yB)).set_stroke(GEO, 1.5, opacity=0.6)
        l1 = DashedLine(P3(self.PX - 1.2, yC), P3(xr, yC)).set_stroke(GEO, 1.5, opacity=0.6)
        br = Brace(Line(P3(xr, yB), P3(xr, yC)), RIGHT, buff=0.06, color=GEO)
        lh = MathTex("h", font_size=40, color=GEO).next_to(br, RIGHT, buff=0.1)
        return VGroup(l0, l1, br, lh)

    def _seta_V(self):
        cc = self.centro()
        b = arrow(P3(cc[0] + 1.0, cc[1]), P3(cc[0] + 1.9, cc[1]), color=VEL, width=6, tip=0.2)
        return VGroup(b, M("V", size=40).next_to(b, UP, buff=0.06))

    def _seta_u(self):
        cc = self.centro()
        a = arrow(P3(-6.3, cc[1] + 0.35), P3(-5.4, cc[1] + 0.35), color=VEL, width=6, tip=0.2)
        return VGroup(a, M("u", size=40).next_to(a, UP, buff=0.06))

    def c09_pendulo(self):
        self.secao("PÊNDULO BALÍSTICO")
        self._pendulo()
        tl = self._timeline()
        self.an("C09-1")
        self.play(FadeIn(self.estat), FadeIn(self.pend), FadeIn(self.bal), run_time=1.0)
        self.wait(0.6)
        lu = self._seta_u()
        gi = VGroup(M("v_i", size=34), gloss(": velocidade inicial do projétil", size=20)).arrange(RIGHT, buff=0.08)
        gt = VGroup(M("V_t", size=34), gloss(": velocidade do conjunto (projétil + bloco)", size=20)).arrange(RIGHT, buff=0.08)
        VGroup(gi, gt).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to(P3(3.6, 1.7))
        self.an("C09-1", "um projétil")
        self.play(GrowArrow(lu[0]), FadeIn(lu[1], shift=0.1 * UP), FadeIn(gi), run_time=0.6)
        self.wait(0.6)
        self.an("C09-2")
        self.play(FadeOut(lu), self.bx.animate.set_value(self.xin), rate_func=linear, run_time=0.9)
        self.dentro = True
        lV = self._seta_V()
        self.an("C09-2", "logo depois")
        self.play(GrowArrow(lV[0]), FadeIn(lV[1], shift=0.1 * UP), FadeIn(gt), run_time=0.6)
        self.wait(0.6)
        ghost = self.pend.copy().clear_updaters().set_opacity(0.2)
        self.add(ghost)
        tau = ValueTracker(0.0)
        self.th.add_updater(lambda m: m.set_value(self._th(tau.get_value())))
        self.an("C09-3")
        self.play(FadeOut(lV), tau.animate.set_value(SUB_T[-1]), rate_func=linear, run_time=3.2)
        self.th.clear_updaters()
        self.th.set_value(SUB_TH[-1])
        hm = self._marca_h()
        self.an("C09-3", "a altura é fácil")
        self.play(FadeIn(hm), run_time=0.6)
        self.wait(0.6)
        self.an("C09-3", "a pergunta é")
        self.play(Indicate(gi[0], color=VEL), Indicate(hm[3], color=GEO), run_time=1.0)
        self.wait(0.6)
        h = self.hl("UMA ÚNICA LEI NÃO VALE DO COMEÇO AO FIM.", y=-1.85, size=28, x=2.6)
        self.an("C09-4")
        self.play(FadeIn(h), run_time=0.7)
        self.wait(0.6)
        self.an("C09-4", "vamos dividir em")
        self.play(FadeIn(tl[0]), run_time=0.6)
        for k, frase in enumerate(("a antes do impacto", "b logo depois", "c na altura máxima")):
            self.an("C09-4", frase)
            self.play(FadeIn(tl[1][k], scale=0.6), FadeIn(tl[2][k], shift=0.1 * UP), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(h), FadeOut(hm), FadeOut(ghost), FadeOut(gi), FadeOut(gt), self.th.animate.set_value(0.0),
                  run_time=1.0)
        self.dentro = False
        self.bx.set_value(-6.7)

    def c10_impacto(self):
        self.secao("PÊNDULO · IMPACTO")
        if not hasattr(self, "tl"):                       # trecho isolado
            self._pendulo()
            self.add(self.estat, self.pend, self.bal, self._timeline())
        self.an("C10-1")
        self.play(self._acende(0, MAG), run_time=0.6)
        hd = txt("MOMENTO HORIZONTAL", T_LAB, color=MAG).move_to(P3(3.9, 2.3))
        self.an("C10-1", "o impacto")
        self.play(FadeIn(hd), run_time=0.6)
        cc = self.centro()
        ex = arrow(P3(-6.9, cc[1] - 1.1), P3(-5.4, cc[1] - 1.1), color=DIM, width=2.5, tip=0.14)
        eixo = VGroup(ex, MathTex("+x", font_size=32, color=DIM).next_to(ex, RIGHT, buff=0.1))
        peso = arrow(cc + DOWN * self.BH / 2, cc + DOWN * (self.BH / 2 + 0.75), color=FC, width=3.5, tip=0.15, op=0.8)
        tens = VGroup(arrow(cc + P3(-0.55, self.BH / 2), cc + P3(-0.55, self.BH / 2 + 0.7), color=FC, width=3.5, tip=0.15, op=0.8),
                      arrow(cc + P3(0.55, self.BH / 2), cc + P3(0.55, self.BH / 2 + 0.7), color=FC, width=3.5, tip=0.15, op=0.8))
        vt = VGroup(txt("FORÇAS EXTERNAS", 18, op=0.85), txt("VERTICAIS", 18, op=0.85)).arrange(DOWN, buff=0.06) \
            .move_to(P3(-0.9, cc[1] + 0.95))
        self.an("C10-2")
        self.play(FadeIn(eixo), FadeIn(peso), FadeIn(tens), FadeIn(vt), run_time=0.8)
        self.wait(0.6)
        self.an("C10-2", "na horizontal")
        self.play(Indicate(eixo, color=WHITE_), run_time=0.8)
        self.an("C10-2", "então no impacto")
        self.play(Indicate(hd, color=MAG), run_time=0.9)
        XE = 3.9
        pa = M("P_{x,A}", "=", "m", "u", size=M_MID).move_to(P3(XE, 1.15))
        lu = self._seta_u()
        self.an("C10-3")
        self.play(FadeIn(lu), run_time=0.3)
        self.an("C10-3", "momento horizontal igual")
        self.play(Indicate(lu[1], color=VEL), FadeIn(pa), run_time=0.9)
        self.wait(0.6)
        self.an("C10-4")
        self.play(FadeOut(lu), FadeOut(tens), self.bx.animate.set_value(self.xin), rate_func=linear, run_time=0.9)
        self.dentro = True
        lV = self._seta_V()
        self.play(FadeIn(lV), run_time=0.4)
        pb = M("P_{x,B}", "=", "(m+M)", "V", size=M_MID).move_to(P3(XE, 0.2))
        self.an("C10-4", "a massa total vezes")
        self.play(Indicate(lV[1], color=VEL), FadeIn(pb), run_time=0.9)
        self.wait(0.8)
        eq = M("m", "u", "=", "(m+M)", "V", size=M_MAIN).move_to(P3(XE, -1.0))
        self.an("C10-5")
        self.play(TransformFromCopy(pa[2:], eq[:2]), FadeIn(eq[2]), TransformFromCopy(pb[2:], eq[3:]), run_time=1.1)
        self.settle(eq)
        bq = box(eq, color=MAG)
        self.play(Create(bq), run_time=0.4)
        self.wait(1.0)
        # K não se conserva no impacto: K_B/K_A = m/(m+M) = 2 %
        kA = barra(1.4, -2.25, 4.4, CYAN, h=0.24)
        kB = barra(1.4, -2.65, 4.4 * PM / (PM + PMM), CYAN, h=0.24)
        lk = VGroup(M("K_A", size=32).next_to(kA, LEFT, buff=0.12), M("K_B", size=32).next_to(kB, LEFT, buff=0.12))
        rz = M(r"2\%", size=32, color=CYAN).next_to(kB, RIGHT, buff=0.2)
        self.an("C10-6")
        self.play(FadeOut(vt), FadeIn(kA), FadeIn(lk[0]), run_time=0.5)
        self.an("C10-6", "despenca")
        self.play(FadeIn(kB), FadeIn(lk[1]), run_time=0.6)
        self.an("C10-6", "sobram só")
        self.play(FadeIn(rz, scale=0.8), run_time=0.5)
        self.wait(1.6)
        self.play(*[FadeOut(m) for m in (kA, kB, lk, rz, eixo, peso, pa, pb, hd)], run_time=0.6)
        self.play(VGroup(eq, bq).animate.scale(0.75).move_to(P3(4.4, 2.65)), run_time=0.7)
        self.eq_imp, self.bq_imp, self.lV = eq, bq, lV
        self.wait(0.6)

    def c11_subida(self):
        if not hasattr(self, "eq_imp"):                   # trecho isolado: reconstrói o estado B
            self._pendulo()
            self.dentro = True
            self.lV = self._seta_V()
            self.eq_imp = M("m", "u", "=", "(m+M)", "V", size=M_MAIN).scale(0.75).move_to(P3(4.4, 2.65))
            self.bq_imp = box(self.eq_imp, color=MAG)
            tl = self._timeline()
            self.add(self.estat, self.pend, self.bal, self.lV, self.eq_imp, self.bq_imp, tl)
            self.tl_seg[0].set_stroke(MAG, 6, opacity=1.0)
        self.secao("PÊNDULO · SUBIDA")
        self.an("C11-1")
        self.play(self._acende(1, CYAN), run_time=0.6)
        hd = txt("ENERGIA MECÂNICA", T_LAB, color=CYAN).move_to(P3(3.9, 1.35))
        # tensão perpendicular ao movimento: não realiza trabalho
        cc = self.centro()
        tens = VGroup(arrow(cc + P3(-0.55, self.BH / 2), cc + P3(-0.55, self.BH / 2 + 0.7), color=FC, width=3.5, tip=0.15, op=0.8),
                      arrow(cc + P3(0.55, self.BH / 2), cc + P3(0.55, self.BH / 2 + 0.7), color=FC, width=3.5, tip=0.15, op=0.8))
        ang = VGroup(Line(cc + P3(0.55, self.BH / 2 + 0.22), cc + P3(0.77, self.BH / 2 + 0.22)),
                     Line(cc + P3(0.77, self.BH / 2 + 0.22), cc + P3(0.77, self.BH / 2))).set_stroke(WHITE_, 2, opacity=0.7)
        hip = txt("SEM AR · SEM ATRITO · FIOS IDEAIS", 17, op=0.7).move_to(P3(3.9, 1.85))
        self.an("C11-1", "desprezando o ar")
        self.play(FadeIn(hip, shift=0.1 * DOWN), run_time=0.7)
        self.an("C11-1", "a tensão é sempre")
        self.play(FadeIn(tens), Create(ang), Indicate(self.lV, color=VEL), run_time=1.0)
        self.wait(0.6)
        self.an("C11-1", "então a energia mecânica")
        self.play(FadeIn(hd), FadeOut(tens), FadeOut(ang), run_time=0.6)
        yB = self.centro()[1]
        ref = VGroup(DashedLine(P3(-6.6, yB), P3(self.centro()[0] - self.BW / 2 - 0.15, yB)).set_stroke(WHITE_, 1.5, opacity=0.45),
                     M("U_g=0", size=32, color=UG).move_to(P3(-5.8, yB + 0.28)))
        self.an("C11-1", "vamos tomar a energia")
        self.play(FadeIn(ref), run_time=0.5)
        # subida integrada; K e U_g do mesmo estado (θ, ω)
        KE = 2.6 / (0.5 * PV ** 2)
        tau = ValueTracker(0.0)

        def barras():
            tv = tau.get_value()
            th, om = self._th(tv), self._om(tv)
            k = 0.5 * (PL * om) ** 2
            u = PG * PL * (1 - np.cos(th))
            return VGroup(barra(2.55, -0.15, k * KE, CYAN, h=0.28), barra(2.55, -0.7, u * KE, UG, h=0.28, op=0.9))

        pb = placa(4.4, 1.5, P3(3.85, -0.42))
        bars = always_redraw(barras)
        lb = VGroup(M("K", size=34).move_to(P3(2.1, -0.15)), M("U_g", size=34, color=UG).move_to(P3(2.1, -0.7)))
        self.an("C11-2")
        self.play(FadeIn(pb), FadeIn(bars), FadeIn(lb), run_time=0.6)
        self.th.add_updater(lambda m: m.set_value(self._th(tau.get_value())))
        self.an("C11-2", "conforme o conjunto sobe")
        self.play(FadeOut(self.lV), tau.animate.set_value(SUB_T[-1]), rate_func=linear, run_time=3.2)
        self.th.clear_updaters()
        self.th.set_value(SUB_TH[-1])
        bars.clear_updaters()
        hm = self._marca_h()
        self.an("C11-2", "no topo")
        self.play(FadeIn(hm), Indicate(bars[1], color=UG), run_time=0.8)
        nP = txt("MOMENTO NÃO SE CONSERVA", 18, color=MAG).move_to(P3(3.9, 0.85))
        self.an("C11-2", "e repara que aqui")
        self.play(FadeIn(nP, shift=0.1 * UP), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(hd), FadeOut(pb), FadeOut(bars), FadeOut(lb), FadeOut(nP), FadeOut(hip), run_time=0.5)
        XE = 3.9
        e1 = M(r"\tfrac{1}{2}", "(m+M)", "V^2", "=", "(m+M)", "g", "h", size=M_MID).move_to(P3(XE, 1.15))
        self.an("C11-3")
        self.play(FadeIn(e1[:3]), run_time=0.7)
        self.an("C11-3", "é igual à energia potencial")
        self.play(FadeIn(e1[3:]), run_time=0.7)
        self.wait(1.0)
        cancel = VGroup(*[Line(e1[i].get_corner(DL), e1[i].get_corner(UR)).set_stroke(CYAN, 3) for i in (1, 4)])
        self.an("C11-4")
        self.play(Create(cancel), run_time=0.5)
        e2 = M(r"\tfrac{1}{2}", "V^2", "=", "g", "h", size=M_MID).move_to(e1)
        self.remap(e1, e2, [(0, 0), (2, 1), (3, 2), (5, 3), (6, 4)], rt=1.0, extra=[FadeOut(cancel)])
        e3 = M("V", "=", r"\sqrt{2gh}", size=M_MID).move_to(e1)
        self.an("C11-4", "e a velocidade do conjunto")
        self.remap(e2, e3, [(1, 0), (2, 1), ([0, 3, 4], 2)], rt=1.1)
        b3 = box(e3, color=CYAN)
        self.an("C11-4", "a raiz positiva")
        self.play(Create(b3), run_time=0.4)
        self.wait(1.0)
        # volta ao impacto (A → B): substitui V
        self.an("C11-5")
        self.play(Indicate(self.eq_imp, color=MAG), run_time=0.7)
        e4 = M("u", "=", r"\frac{m+M}{m}", "V", size=M_MID).move_to(P3(XE, -0.4))
        self.play(TransformFromCopy(self.eq_imp, e4), run_time=1.0)
        self.settle(e4)
        self.wait(0.6)
        e5 = M("u", "=", r"\frac{m+M}{m}", r"\sqrt{2gh}", size=M_MID).move_to(P3(XE, -0.4))
        self.an("C11-5", "e substitui")
        self.play(FadeOut(e4[3]), TransformFromCopy(e3[2], e5[3]), ReplacementTransform(e4[:3], e5[:3]), run_time=1.1)
        self.drop(e4)
        self.settle(e5)
        self.an("C11-5", "chegamos lá")
        self.play(Create(box(e5, color=WHITE_)), run_time=0.5)
        self.wait(1.6)
        # payoff: a linha do tempo inteira
        outs = [m for m in self.mobjects if m not in (*self.fixos(), self.tl)]
        self.an("C11-6")
        self.play(*[FadeOut(m) for m in outs], run_time=0.7)
        for m in outs:
            m.clear_updaters()
        self.remove(*outs)
        self.play(self.tl.animate.move_to(P3(0, 0.2)).scale(1.1), run_time=0.9)
        lm = txt("MOMENTO", T_LAB, color=MAG, bold=True).move_to((self.tl_seg[0].get_center() + DOWN * 0.45))
        le = txt("ENERGIA", T_LAB, color=CYAN, bold=True).move_to((self.tl_seg[1].get_center() + DOWN * 0.45))
        self.an("C11-6", "no impacto momento")
        self.play(FadeIn(lm), run_time=0.5)
        self.an("C11-6", "na subida energia")
        self.play(FadeIn(le), run_time=0.5)
        pay = self.hl("LEIS DIFERENTES PARA INTERVALOS DIFERENTES.", y=-1.6, size=32)
        self.an("C11-6", "leis diferentes")
        self.play(FadeIn(pay, shift=0.1 * UP), run_time=0.7)
        self.wait(2.4)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C12 — método como fluxo visual
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c12_metodo(self):
        self.secao("MÉTODO")

        def no(conteudo, centro, cor=WHITE_):
            t = txt(conteudo, T_SMALL, color=cor) if isinstance(conteudo, str) else conteudo
            r = RoundedRectangle(corner_radius=0.18, width=t.width + 0.5, height=max(t.height, 0.3) + 0.42) \
                .set_stroke(cor, 1.6, opacity=0.7).set_fill(WHITE_, 0.04)
            return VGroup(r, t.move_to(r)).move_to(centro)

        def liga(a, b):
            return arrow(a.get_right() + RIGHT * 0.08, b.get_left() + LEFT * 0.08, color=DIM, width=2.5, tip=0.13)

        b1 = Corpo("", C1F, 0.5).at(-6.1, 1.85)
        b2 = Corpo("", C2F, 0.42).at(-5.1, 1.85)
        sis = VGroup(Line(P3(-6.7, 1.85), P3(-4.6, 1.85)).set_stroke(WHITE_, 2, opacity=0.4), b1, b2)
        sis.add(contorno(VGroup(b1, b2), buff=0.18))
        n1 = no("SISTEMA + INTERVALO", P3(-5.4, 1.0))
        mk = VGroup(Circle(radius=0.17).set_stroke(CYAN, 2, opacity=0.5), Dot(radius=0.08, color=CYAN)).set_z_index(20)

        def em(n):
            return n.get_corner(UL) + P3(0.02, 0.02)

        mk.move_to(em(n1))
        self.an("C12-1", "primeiro qual é")
        self.play(FadeIn(sis), FadeIn(n1), FadeIn(mk, scale=0.6), run_time=0.8)
        self.wait(1.0)
        n2 = no("EIXO + SINAIS", P3(-1.6, 1.0))
        ix = arrow(P3(-2.3, 1.85), P3(-0.9, 1.85), color=DIM, width=2.5, tip=0.14)
        ixl = MathTex("+x", font_size=30, color=DIM).next_to(ix, RIGHT, buff=0.08)
        self.an("C12-2")
        self.play(Create(liga(n1, n2)), mk.animate.move_to(em(n2)), FadeIn(n2), FadeIn(ix), FadeIn(ixl), run_time=0.9)
        self.wait(0.8)
        n3 = no(M(r"J_{\mathrm{ext}}", r"\approx", "0", r"\,?", size=36), P3(2.3, 1.0))
        r3 = M("P_i", "=", "P_f", size=M_LAB).next_to(n3, UP, buff=0.3)
        self.an("C12-3")
        self.play(Create(liga(n2, n3)), mk.animate.move_to(em(n3)), FadeIn(n3), run_time=0.9)
        self.an("C12-3", "se for o momento")
        self.play(FadeIn(r3), run_time=0.5)
        self.wait(1.0)
        n4 = no("CONDIÇÃO EXTRA?", P3(-3.6, -1.15))
        l34 = CurvedArrow(n3.get_bottom() + DOWN * 0.05, n4.get_top() + UP * 0.05, angle=-0.6, color=DIM,
                          stroke_width=2.5, tip_length=0.15)
        l34.set_fill(opacity=0)
        l34.get_tip().set_fill(DIM, 1.0)
        self.an("C12-4")
        self.play(Create(l34), MoveAlongPath(mk, l34.copy()), FadeIn(n4), run_time=1.0)
        self.play(mk.animate.move_to(em(n4)), run_time=0.3)
        ramos = VGroup(VGroup(txt("ELÁSTICA", 18), M(r"\rightarrow", size=30), M("K_i", "=", "K_f", size=34)),
                       VGroup(txt("GRUDAM", 18), M(r"\rightarrow", size=30), M("v_1", "=", "v_2", size=34)),
                       VGroup(txt("OUTRA", 18), M(r"\rightarrow", size=30), txt("DADO", 18)))
        for r in ramos:
            r.arrange(RIGHT, buff=0.15)
        ramos.arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(n4, DOWN, buff=0.3)
        for r, frase in zip(ramos, ("se é elástica", "se gruda", "se for outra")):
            self.an("C12-4", frase)
            self.play(FadeIn(r, shift=0.1 * RIGHT), run_time=0.6)
        self.wait(1.2)
        n5 = no("NOVO PROCESSO?", P3(2.3, -1.15))
        r5 = txt("SEPARE", T_SMALL, color=CYAN, bold=True).next_to(n5, DOWN, buff=0.3)
        self.an("C12-5")
        self.play(Create(liga(n4, n5)), mk.animate.move_to(em(n5)), FadeIn(n5), run_time=0.9)
        self.an("C12-5", "então separe")
        self.play(FadeIn(r5), run_time=0.5)
        self.wait(1.6)
        self.clear()
        # fechamento na pergunta do hook: os três finais e a condição que decide cada um
        minis = getattr(self, "minis", [(v1, v2, nm == "ficam juntos", r) for (nm, v1, v2), r in
                                        zip(FINAIS, ("REBATEM", "SE SEPARAM", "FICAM JUNTOS"))])
        conds = (M("K_i", "=", "K_f", size=M_LAB), txt("DADO EXTRA", 22), M("v_1", "=", "v_2", size=M_LAB))
        cols = VGroup()
        for (v1, v2, jt, rot), cd in zip(minis, conds):
            cols.add(VGroup(estado(v1, v2, jt, escala=0.42), txt(rot, T_SMALL, op=0.85), cd).arrange(DOWN, buff=0.22))
        cols.arrange(RIGHT, buff=1.1).move_to(P3(0, 0.9))
        ini = txt("MESMO COMEÇO", T_SMALL, op=0.6).next_to(cols, UP, buff=0.35)
        self.an("C12-6")
        self.play(FadeIn(ini, shift=0.1 * DOWN), run_time=0.7)
        self.an("C12-6", "mesmo começo")
        self.play(LaggedStart(*[FadeIn(c_[:2]) for c_ in cols], lag_ratio=0.25), run_time=1.1)
        for c_, frase in zip(cols, ("na elástica", "quando se separam", "quando grudam")):
            self.an("C12-6", frase)
            self.play(FadeIn(c_[2], shift=0.1 * UP), run_time=0.6)
        self.an("C12-6", "o momento é o mesmo")
        self.play(Indicate(ini, color=MAG), run_time=0.8)
        self.an("C12-6", "quem decide o final")
        self.play(LaggedStart(*[Indicate(c_[2], color=CYAN) for c_ in cols], lag_ratio=0.25), run_time=1.2)
        self.wait(1.0)
        a = self.hl("MODELE O PROCESSO.", y=-1.75, size=44)
        b = self.hl("NÃO PROCURE UMA FÓRMULA.", y=-2.6, size=34, color=CYAN)
        self.an("C12-7", "modele o processo")
        self.play(FadeIn(a, shift=0.1 * UP), run_time=0.7)
        self.an("C12-7", "não procure")
        self.play(FadeIn(b, shift=0.1 * UP), run_time=0.7)
        self.wait(2.0)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # Ponte para 2D (sem resolver): as velocidades finais saem da linha; P vetorial fica fixo
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def ponte_2d(self):
        self.secao("PRÓXIMO PASSO")
        # massas iguais, P = (2, 0); depois do contato v1 = (1, −s), v2 = (1, s): P_y = 0 em todo s
        s = ValueTracker(0.0)
        c1, c2 = P3(-2.2, 0.0), P3(1.6, 0.0)
        KA = 1.0
        d1 = Circle(radius=0.42).set_stroke(mix(C1F, 0.5), 2).set_fill(C1F, 1.0).move_to(c1)
        d2 = Circle(radius=0.42).set_stroke(mix(C2F, 0.5), 2).set_fill(C2F, 1.0).move_to(c2)

        def vetores():
            sv = s.get_value()
            v1, v2 = np.array([1.0, -sv, 0]), np.array([1.0, sv, 0])
            a1 = arrow(c1 + v1 / np.linalg.norm(v1) * 0.45, c1 + v1 / np.linalg.norm(v1) * 0.45 + v1 * KA, color=VEL, width=6, tip=0.2)
            a2 = arrow(c2 + v2 / np.linalg.norm(v2) * 0.45, c2 + v2 / np.linalg.norm(v2) * 0.45 + v2 * KA, color=VEL, width=6, tip=0.2)
            o = P3(-1.4, -2.3)                 # soma ponta com cauda dos momentos, em magenta
            p1 = arrow(o, o + v1 * 1.1, color=MAG, width=6, tip=0.18, op=0.75)
            p2 = arrow(o + v1 * 1.1, o + (v1 + v2) * 1.1, color=MAG, width=6, tip=0.18, op=0.75)
            pt = arrow(o, o + (v1 + v2) * 1.1, color=MAG, width=10, tip=0.24)
            return VGroup(a1, a2, p1, p2, pt)

        vs = always_redraw(vetores)
        ev = M(r"\vec P_i", "=", r"\vec P_f", size=M_MAIN).move_to(P3(0, 2.3))
        self.an("P1")
        self.play(FadeIn(ev), run_time=0.7)
        self.an("P1", "em uma dimensão")
        self.play(FadeIn(d1), FadeIn(d2), FadeIn(vs), run_time=0.9)
        self.wait(0.6)
        self.an("P1", "mas se os corpos")
        self.play(s.animate.set_value(1.0), run_time=2.4)
        self.an("P1", "só que agora como vetor")
        self.play(Indicate(ev, color=MAG, scale_factor=1.06), run_time=1.0)
        self.wait(1.0)
        vs.clear_updaters()

    def cta(self):
        """Padrão do longo: tudo sai (inclusive tag e marca d'água), logo com anéis, inscrição, gancho, próximo vídeo."""
        self._pend = []
        self.an("E1")
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
        gancho = txt("E SE A COLISÃO NÃO ACONTECER EM UMA LINHA?", 28).move_to(oc + P3(0, -1.85))
        nx1 = txt("PRÓXIMO VÍDEO:", 26, op=0.9).move_to(oc + P3(0, -1.85))
        nx2 = txt("COLISÕES EM 2D", 30, color=CYAN, bold=True).move_to(oc + P3(0, -2.45))
        self.play(LaggedStart(*[FadeIn(r_, scale=0.85) for r_ in rings], lag_ratio=0.3), FadeIn(logo, scale=0.92),
                  run_time=1.8)
        self.an("E1", "se essas ideias")
        self.play(FadeIn(msg, shift=0.1 * UP), run_time=0.9)
        self.an("E2")
        self.play(FadeIn(gancho, shift=0.1 * UP), run_time=0.9)
        self.wait(1.2)
        self.an("E3")
        self.play(FadeOut(gancho), run_time=0.5)
        self.play(FadeIn(nx1, shift=0.1 * UP), run_time=0.6)
        self.an("E3", "colisões em duas")
        self.play(FadeIn(nx2, shift=0.1 * UP), run_time=0.6)
        w = DashedVMobject(Circle(radius=1.6, arc_center=oc), num_dashes=24, dashed_ratio=0.6).set_stroke(VEL, 3.5, 0.35)
        self.play(w.animate.scale(2.6, about_point=oc).set_stroke(opacity=0.0), run_time=2.4)
        self.remove(w)
        self.an("E3", "valeu demais")
        w2 = DashedVMobject(Circle(radius=1.6, arc_center=oc), num_dashes=24, dashed_ratio=0.6).set_stroke(VEL, 3.5, 0.35)
        self.play(w2.animate.scale(2.6, about_point=oc).set_stroke(opacity=0.0), run_time=2.4)
        self.remove(w2)
        self.wait(0.6)
