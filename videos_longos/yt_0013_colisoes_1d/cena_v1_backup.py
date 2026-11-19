"""yt_0013 — Colisões em 1D: como saber o que acontece depois? (Física I · Mecânica · Colisões).

Cena completa SILENCIOSA C01–C12 (briefing congelado; ver ficha.md). Preview 960×540 / 15 fps:
    uv run python -m manim -r 960,540 --fps 15 videos_longos/yt_0013_colisoes_1d/cena.py Colisoes1DYT013

3D: só o sólido `colisao_1d` do arsenal, só em C01 e C03 (sequências preparadas com ponte.py, render="nunca").
Antes de renderizar em outra resolução, preparar as três variantes (restituicao = 1.0, 0.5, 0.0):
    python experimentos/blender/arsenal/ponte.py colisao_1d --res LxA --frames 60 --set m1=2.0 --set m2=1.0 \
        --set v1=2.0 --set v2=-2.0 --set instante=0.65 --set mostrar_cm=0 --set restituicao=E

Cores: corpo 1 azul · corpo 2 violeta · vetores físicos branco · resultado/payoff ciano · energia cinética ciano ·
energia interna laranja (único tom quente). Notação: u_i iniciais, v_i finais, v_f comum; pêndulo: u, V, m, M, h.
"""
import os
import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UL, UP, UR, ORIGIN, PI, Arrow, Create, DashedLine, Dot, FadeIn, FadeOut, GrowArrow,
    ImageMobject, Indicate, Line, MathTex, Rectangle, ReplacementTransform, RoundedRectangle, Scene,
    SurroundingRectangle, Transform, TransformFromCopy, TransformMatchingTex, ValueTracker, VGroup, VMobject,
    Write, always_redraw, linear, smooth, Brace, LaggedStart, rate_functions,
)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experimentos" / "blender" / "arsenal"))
from template.config_horizontal import BACKGROUND_COLOR, PRIMARY_COLOR, TEXT_COLOR, WATERMARK_PATH  # noqa: E402
from template.fonts import screen_text  # noqa: E402
from manim_solido3d import Solido3D  # noqa: E402

# ── paleta ───────────────────────────────────────────────────────────────────────────────────────────────────
WHITE = TEXT_COLOR
CYAN = PRIMARY_COLOR        # resultado / payoff · energia cinética
C1 = "#4D93FF"              # corpo 1 (azul; o bloco 1 do 3D é #267BFF)
C1F = "#267BFF"
C2 = "#9C8CFF"              # corpo 2 (violeta)
HEAT = "#FF7A3D"            # energia interna
STEEL = "#7A8696"
DIM = "#8FA3C4"
GREY = "#B8C4DA"

SECOES = [s.strip() for s in os.environ.get("SECOES", "").split(",") if s.strip()]

T_HEAD, T_BODY, T_NOTE, T_CAP = 40, 34, 28, 24
M_XL, M_L, M_M, M_S = 72, 58, 48, 40

TOK = {}
for _s in ("m_1", "u_1", "v_1", "u_1^2", "v_1^2"):
    TOK[_s] = C1
for _s in ("m_2", "u_2", "v_2", "u_2^2", "v_2^2"):
    TOK[_s] = C2

# ── colisao_1d (Blender): parâmetros documentados da ficha; mesma configuração inicial nas três variantes ───────
SOL_BASE = {"m1": 2.0, "m2": 1.0, "v1": 2.0, "v2": -2.0, "instante": 0.65, "mostrar_cm": 0}
VARIANTES = (1.0, 0.5, 0.0)            # restituição: rebatem · se separam · ficam juntos
SOL_U = (2.0, -2.0)
SOL_V = {e: ((2.0 * 2 - e * 2 + (1 + e) * 1 * (-2)) / 3.0, (1.0 * -2 - e * 2 * -2 + (1 + e) * 2 * 2) / 3.0)
         for e in VARIANTES}         # = velocidades_apos() de experimentos/blender/colisoes.py (m1=2, m2=1)
# pontos dos blocos na imagem (px de 960×540): topo e face frontal, no quadro inicial e no final de cada variante
TOP0 = ((250, 118), (705, 212))
FRONT0 = ((222, 206), (690, 302))
TOP_END = {1.0: ((378, 130), (683, 206)), 0.5: ((406, 132), (618, 200)), 0.0: ((434, 134), (554, 194))}
DIR3D = np.array([1.0, -0.11, 0.0]) / np.hypot(1.0, 0.11)   # direção do trilho na tela


def txt(s, size=T_BODY, color=WHITE, opacity=1.0, upper=True):
    if upper:
        s = s.upper()
    return screen_text(s, size, color=color, oversample=4 if len(s) < 34 else 2).set_opacity(opacity)


def M(*parts, size=M_L, color=WHITE, w=None):
    """MathTex por partes (TransformMatchingTex casa partes); m_1/u_1/v_1 azuis e m_2/u_2/v_2 violeta."""
    m = MathTex(*parts, font_size=size, color=color, tex_to_color_map=TOK)
    if w and m.width > w:
        m.scale_to_fit_width(w)
    return m


def arrow(a, b, color=WHITE, width=5, z=8, tip=0.2, op=1.0):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if np.linalg.norm(b - a) < 0.03:
        return VMobject()
    m = Arrow(a, b, buff=0, color=color, stroke_width=width, tip_length=tip, max_tip_length_to_length_ratio=0.45,
              max_stroke_width_to_length_ratio=50)
    return m.set_opacity(op).set_z_index(z)


def box(m, color=CYAN, buff=0.12, width=3):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=width, corner_radius=0.08)


def P3(x, y):
    return np.array([x, y, 0.0])


def corpo(nome, cor, lado, size=42):
    sq = RoundedRectangle(corner_radius=0.08, width=lado, height=lado, stroke_color=cor, stroke_width=3,
                          fill_color=cor, fill_opacity=0.30)
    lab = MathTex(nome, font_size=size, color=WHITE).move_to(sq)
    return VGroup(sq, lab)


def elastica(m1, m2, u1, u2):
    s = m1 + m2
    return (m1 - m2) / s * u1 + 2 * m2 / s * u2, 2 * m1 / s * u1 + (m2 - m1) / s * u2


class Col:
    """Colisão 1D em Manim: contato em xc no instante t = 0 (contato instantâneo; t é o tempo da simulação)."""

    def __init__(self, m1, m2, u1, u2, v1, v2, w1=1.0, w2=1.0, xc=0.0, ty=-1.6, kx=1.0, ka=0.5, t0=-1.5,
                 n1="m_1", n2="m_2", pre=("u_1", "u_2"), post=("v_1", "v_2"), junto=None, lab=42):
        self.m1, self.m2, self.u1, self.u2, self.v1, self.v2 = m1, m2, u1, u2, v1, v2
        self.w1, self.w2, self.xc, self.ty, self.kx, self.ka = w1, w2, xc, ty, kx, ka
        self.pre, self.post, self.junto = pre, post, junto
        self.t, self.ao = ValueTracker(t0), ValueTracker(1.0)
        self.b1, self.b2 = corpo(n1, C1, w1), corpo(n2, C2, w2)
        self.b1.add_updater(lambda m: m.move_to(P3(self.x1(), ty + w1 / 2)))
        self.b2.add_updater(lambda m: m.move_to(P3(self.x2(), ty + w2 / 2)))
        self.track = Line(P3(-7.4, ty), P3(7.4, ty), color=STEEL, stroke_width=3)
        names = [n for n in (*pre, *post, junto) if n]
        self.L = {n: M(n, size=lab) for n in names}
        self.arrows = always_redraw(self._arrows)

    def x1(self):
        t = self.t.get_value()
        return self.xc - self.w1 / 2 + (self.u1 if t < 0 else self.v1) * t * self.kx

    def x2(self):
        t = self.t.get_value()
        return self.xc + self.w2 / 2 + (self.u2 if t < 0 else self.v2) * t * self.kx

    def _vec(self, base, vel, name):
        if not name:
            return VGroup()
        lab = self.L[name]
        L = vel * self.ka
        if abs(L) < 0.06:
            return VGroup(lab.move_to(base + UP * 0.2))
        a = arrow(base, base + RIGHT * L, width=6, tip=0.22)
        lab.next_to(a, UP, buff=0.08)
        return VGroup(a, lab)

    def _arrows(self):
        op = self.ao.get_value()
        if op <= 0.01:
            return VGroup()
        t = self.t.get_value()
        y = self.ty + 0.32
        if t >= 0 and self.junto:
            top = max(self.w1, self.w2)
            xm = (self.x1() + self.x2()) / 2
            g = VGroup(self._vec(P3(xm, y + top), self.v1, self.junto))
        else:
            n1, n2 = self.post if t >= 0 else self.pre
            v1, v2 = (self.v1, self.v2) if t >= 0 else (self.u1, self.u2)
            g = VGroup(self._vec(P3(self.x1(), y + self.w1), v1, n1), self._vec(P3(self.x2(), y + self.w2), v2, n2))
        return g.set_opacity(op)

    def group(self, arrows=True):
        return VGroup(self.track, self.b1, self.b2, *([self.arrows] if arrows else []))


class Colisoes1DYT013(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND_COLOR
        self.tag = txt("MECÂNICA · COLISÕES EM 1D", 22, opacity=0.75).to_corner(UL, buff=0.32).set_z_index(40)
        self.wm = ImageMobject(str(WATERMARK_PATH)).set_width(1.92).set_opacity(0.45).to_corner(UR, buff=0.3)
        self.wm.set_z_index(40)
        self.add(self.tag, self.wm)
        self.sols = {e: Solido3D("colisao_1d", params={**SOL_BASE, "restituicao": e}, frames=60, render="nunca")
                     for e in VARIANTES}
        marcas = []
        for nome in ("c01_tres_finais", "c02_impulso_externo", "c03_classificacao", "c04_completamente_inelastica",
                     "c05_energia_cinetica", "c06_elastica_relativa", "c07_velocidades_gerais", "c08_casos_limite",
                     "c09_pendulo_setup", "c10_pendulo_impacto", "c11_pendulo_subida", "c12_metodo_e_ponte_2d"):
            if SECOES and nome[:3] not in SECOES:      # desenvolvimento: SECOES=c06,c07 renderiza só essas
                continue
            t0 = self.renderer.time
            getattr(self, nome)()
            marcas.append((nome, t0, self.renderer.time))
        for nome, a, b in marcas:
            print(f"[tempo] {nome}: {a:7.1f} s -> {b:7.1f} s ({b - a:5.1f} s)")

    # ── utilidades ───────────────────────────────────────────────────────────────────────────────────────────
    def clear(self, *keep, rt=0.8):
        keep = {self.tag, self.wm, *keep}
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=rt)
        for m in mobs:
            m.clear_updaters()
        self.remove(*mobs)

    def head(self, s, color=WHITE, size=T_HEAD, y=3.15):
        return txt(s, size, color=color).move_to(P3(0, y))

    def swap(self, old, new, rt=1.1, **kw):
        self.play(TransformMatchingTex(old, new, **kw), run_time=rt)
        return new

    def remap(self, old, new, pairs, rt=1.2, extra=()):
        """Transformação explícita por partes: pairs = [(índices antigos, índices novos)]; o resto entra/sai em fade."""
        anims, uo, un = [], set(), set()
        for o, n in pairs:
            o = o if isinstance(o, (list, tuple)) else [o]
            n = n if isinstance(n, (list, tuple)) else [n]
            uo.update(o)
            un.update(n)
            anims.append(ReplacementTransform(VGroup(*[old[i].copy() for i in o]), VGroup(*[new[j] for j in n])))
        anims += [FadeOut(old[i]) for i in range(len(old)) if i not in uo]
        anims += [FadeIn(new[j]) for j in range(len(new)) if j not in un]
        for i in uo:
            old[i].set_opacity(0)
        antes = {id(m) for m in self.mobjects}
        self.play(*anims, *extra, run_time=rt)
        self.drop(old)
        self.remove(*[m for m in self.mobjects if id(m) not in antes])
        self.add(new)
        return new

    def drop(self, *mobs):
        """Remove os mobjects e qualquer pedaço deles que tenha ficado solto no topo da cena (TransformFromCopy etc.)."""
        fam = {id(x) for mob in mobs for x in mob.get_family()}
        self.remove(*[m for m in self.mobjects if id(m) in fam or
                      (m.submobjects and all(id(x) in fam for x in m.get_family()[1:]))])

    def settle(self, new):
        """Depois de montar `new` por pedaços: tira os pedaços soltos e deixa só `new` na cena."""
        fam = {id(x) for x in new.get_family()}
        self.remove(*[m for m in self.mobjects if m is not new and (id(m) in fam or
                      (m.submobjects and all(id(x) in fam for x in m.get_family()[1:])))])
        self.add(new)
        return new

    # ── 3D: pontos da imagem do Blender em coordenadas da cena ───────────────────────────────────────────────
    @staticmethod
    def px(img, p):
        x, y = p
        return img.get_center() + np.array([(x / 960 - 0.5) * img.width, (0.5 - y / 540) * img.height, 0.0])

    def solido(self, e, largura, centro):
        img = self.sols[e].mobject(cena=self, largura=largura, centro=centro, periodo=4.2, autoplay=False)
        img.set_z_index(1)
        return img

    def setas3d(self, img, tops, vels, names, k=0.75):
        g = VGroup()
        for p, v, n in zip(tops, vels, names):
            base = self.px(img, p) + UP * 0.32
            lab = M(n, size=46)
            if abs(v) < 0.05:
                g.add(lab.move_to(base + UP * 0.18))
                continue
            a = arrow(base, base + DIR3D * v * k * img.width / 14, width=6, tip=0.24)
            g.add(a, lab.next_to(a, UP, buff=0.1))
        return g.set_z_index(10)

    def rotulos3d(self, img, shift=(ORIGIN, ORIGIN)):
        g = VGroup()
        for p, n, d in zip(FRONT0, ("m_1", "m_2"), shift):
            g.add(MathTex(n, font_size=46 * img.width / 14, color=WHITE).move_to(self.px(img, p) + d))
        return g.set_z_index(10)

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C01 — O mesmo começo, três finais
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c01_tres_finais(self):
        LARG, CEN = 14.0, P3(0.3, -0.75)
        titulos = {1.0: "REBATEM", 0.5: "SE SEPARAM", 0.0: "FICAM JUNTOS"}
        cont = None
        for k, e in enumerate(VARIANTES):
            img = self.solido(e, LARG, CEN)
            labs = self.rotulos3d(img)
            u = self.setas3d(img, TOP0, SOL_U, ("u_1", "u_2"))
            novo = txt(f"EXPERIMENTO {k + 1}", T_NOTE, color=DIM).move_to(P3(0, 3.15))
            if k == 0:
                self.play(FadeIn(img), run_time=1.2)
                self.play(FadeIn(labs), run_time=0.7)
                self.play(*[GrowArrow(a) if isinstance(a, Arrow) else FadeIn(a) for a in u], run_time=1.0)
                self.play(FadeIn(novo), run_time=0.5)
                self.wait(3.0)
            else:
                self.play(FadeIn(img), FadeIn(labs), FadeIn(u), Transform(cont, novo), run_time=0.9)
                novo = cont
                self.wait(1.6)
            cont = novo
            self.play(FadeOut(u), FadeOut(labs), run_time=0.5)
            img.retomar()
            self.wait(4.4)
            end = TOP_END[e]
            v1, v2 = SOL_V[e]
            if e == 0.0:
                base = (self.px(img, end[0]) + self.px(img, end[1])) / 2 + UP * 0.5
                a = arrow(base, base + DIR3D * v1 * 0.75, width=6, tip=0.24)
                vs = VGroup(a, M("v_1", "=", "v_2", size=46).next_to(a, UP, buff=0.1)).set_z_index(10)
            else:
                vs = self.setas3d(img, end, (v1, v2), ("v_1" if abs(v1) > 0.05 else "v_1=0", "v_2"))
            res = txt(titulos[e], 46, color=WHITE).move_to(P3(0, 2.45)).set_z_index(12)
            self.play(FadeIn(vs), FadeIn(res, shift=0.15 * UP), run_time=0.9)
            self.wait(3.2 if k < 2 else 3.6)
            self.play(FadeOut(img), FadeOut(vs), FadeOut(res), run_time=0.7)
            img.clear_updaters()
        self.play(FadeOut(cont), run_time=0.4)

        # Payoff: P_i = P_f, uma equação e duas incógnitas
        q = self.head("O MESMO ESTADO INICIAL, TRÊS FINAIS DIFERENTES.", size=T_BODY, color=DIM)
        self.play(FadeIn(q), run_time=0.7)
        e1 = M("P_i", "=", "P_f", size=M_XL).move_to(P3(0, 0.7))
        self.play(Write(e1), run_time=1.0)
        self.wait(1.8)
        e2 = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2v_2", size=M_XL).move_to(P3(0, 0.7))
        self.play(FadeOut(e1, shift=0.3 * UP), FadeIn(e2, shift=0.3 * UP), run_time=1.1)
        self.wait(1.4)
        vv = VGroup(*[e2.get_part_by_tex(n) for n in ("v_1", "v_2")])
        bx = VGroup(*[box(m, buff=0.08) for m in vv])
        self.play(Create(bx), vv.animate.set_color(CYAN), run_time=0.9)
        n = txt("1 EQUAÇÃO · 2 INCÓGNITAS", 44, color=CYAN).move_to(P3(0, -0.9))
        self.play(FadeIn(n, shift=0.2 * UP), run_time=0.8)
        self.wait(2.2)
        fal = txt("O QUE FALTA?", 54).move_to(P3(0, -2.3))
        self.play(FadeIn(fal, scale=0.9), run_time=0.9)
        self.wait(2.8)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C02 — O detalhe do impacto pode ser complicado. O resultado, não.
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c02_impulso_externo(self):
        hq = self.head("O QUE TODAS TÊM EM COMUM?")
        self.play(FadeIn(hq), run_time=0.8)
        self.wait(1.6)
        m1, m2, u1, u2 = 2.0, 1.0, 2.0, -2.0
        v1, v2 = elastica(m1, m2, u1, u2)
        c = Col(m1, m2, u1, u2, v1, v2, w1=1.15, w2=0.9, xc=-2.6, ty=-2.4, kx=0.9, ka=0.45, t0=-1.6)
        self.play(FadeOut(hq), FadeIn(c.group()), run_time=1.0)
        self.play(c.t.animate.set_value(0), rate_func=linear, run_time=1.8)

        # Contato em câmera lenta: forças internas grandes, opostas e complicadas no tempo
        s = ValueTracker(0.0)
        KP, X0, YP = 0.62, -4.6, 1.15
        p1i, p2i, p1f, p2f = m1 * u1, m2 * u2, m1 * v1, m2 * v2

        def g(x):
            return x * x * (3 - 2 * x)

        def forcas():
            sv = s.get_value()
            f = np.sin(PI * sv) * (1 + 0.38 * np.sin(31 * sv) + 0.2 * np.sin(13 * sv + 1))
            if f < 0.03:
                return VGroup()
            y = c.ty + 0.45
            xc = c.xc
            a1 = arrow(P3(xc - 0.05, y), P3(xc - 0.05 - 1.6 * f, y), color=WHITE, width=7, tip=0.26)
            a2 = arrow(P3(xc + 0.05, y), P3(xc + 0.05 + 1.6 * f, y), color=WHITE, width=7, tip=0.26)
            return VGroup(a1, a2).set_z_index(12)

        def momentos():
            sv = g(s.get_value())
            p1 = p1i + (p1f - p1i) * sv
            p2 = p2i + (p2f - p2i) * sv
            P = p1 + p2
            a1 = arrow(P3(X0, YP + 0.9), P3(X0 + KP * p1, YP + 0.9), color=C1, width=6)
            a2 = arrow(P3(X0 + KP * p1, YP + 0.35), P3(X0 + KP * P, YP + 0.35), color=C2, width=6)
            aT = arrow(P3(X0, YP - 0.45), P3(X0 + KP * P, YP - 0.45), color=WHITE, width=9, tip=0.26)
            l1 = M("p_1", size=M_S, color=C1).next_to(a1, UP, buff=0.06)
            l2 = M("p_2", size=M_S, color=C2).next_to(a2, UP, buff=0.06)
            lT = M(r"P_{\rm sist}", size=M_S).next_to(aT, DOWN, buff=0.1)
            guia = DashedLine(P3(X0, YP + 1.35), P3(X0, YP - 0.75), color=DIM, stroke_width=2)
            return VGroup(guia, a1, a2, aT, l1, l2, lT)

        fz = always_redraw(forcas)
        mom = always_redraw(momentos)
        ltit = txt("MOMENTO", T_CAP, color=DIM).move_to(P3(X0 + 1.2, YP + 1.85))
        self.play(FadeOut(c.arrows), FadeIn(mom), FadeIn(ltit), run_time=0.9)
        self.add(fz)
        fint = txt("FORÇAS INTERNAS: GRANDES E COMPLICADAS", T_NOTE).move_to(P3(c.xc, c.ty - 0.55))
        self.play(FadeIn(fint), run_time=0.6)
        self.play(s.animate.set_value(1.0), rate_func=linear, run_time=5.0)
        self.remove(fz)
        self.wait(0.6)
        nota = VGroup(txt("cada momento muda", T_NOTE, color=GREY, upper=False),
                      txt("o total não muda", T_NOTE, color=WHITE, upper=False)) \
            .arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        nota.move_to(P3(X0 + 2.3 + nota.width / 2, YP - 0.9))
        self.play(FadeIn(nota), run_time=0.7)
        self.wait(1.4)
        self.play(s.animate.set_value(0.0), run_time=2.0, rate_func=smooth)
        self.play(s.animate.set_value(1.0), run_time=2.0, rate_func=smooth)
        self.wait(0.6)
        self.play(FadeOut(fint), run_time=0.4)
        c.ao.set_value(0)
        self.add(c.arrows)
        c.t.set_value(0.0001)
        self.play(c.t.animate.set_value(1.0), c.ao.animate.set_value(1), rate_func=linear, run_time=1.4)

        # Matemática: ΔP_sist = J_ext → J_ext ≈ 0 → P_i = P_f
        XE = 3.7
        e1 = M(r"\Delta P_{\rm sist}", "=", r"J_{\rm ext}", size=M_L).move_to(P3(XE, 1.7))
        self.play(Write(e1), run_time=1.0)
        self.wait(1.2)
        nj = txt("IMPULSO EXTERNO PEQUENO NO CURTO INTERVALO", T_CAP, color=DIM).move_to(P3(XE, 0.85))
        e2 = M(r"J_{\rm ext}", r"\approx", "0", size=M_L).move_to(P3(XE, 0.2))
        self.play(FadeIn(nj), TransformFromCopy(e1[2], e2[0]), FadeIn(e2[1:]), run_time=1.0)
        self.wait(1.6)
        e3 = M(r"\Delta P_{\rm sist}", r"\approx", "0", size=M_L).move_to(P3(XE, -0.9))
        self.play(TransformFromCopy(e1[0], e3[0]), TransformFromCopy(e2[1:], e3[1:]), run_time=1.0)
        self.wait(1.0)
        e4 = M("P_i", "=", "P_f", size=M_XL, color=CYAN).move_to(P3(XE, -0.9))
        self.play(ReplacementTransform(e3, e4), run_time=0.9)
        self.play(Create(box(e4)), run_time=0.6)
        self.wait(2.2)

        self.clear()
        f1 = txt("Não precisamos modelar a força de impacto.", 40, upper=False).move_to(P3(0, 0.6))
        self.play(FadeIn(f1), run_time=0.8)
        self.wait(2.2)
        f2 = txt("Mas ainda falta uma segunda informação.", 40, color=CYAN, upper=False).move_to(P3(0, -0.5))
        self.play(FadeIn(f2, shift=0.15 * UP), run_time=0.8)
        self.wait(2.4)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C03 — O que diferencia as colisões (nomes formais entram aqui)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c03_classificacao(self):
        LARG, CEN, XR = 10.6, P3(-2.6, -0.55), 4.55
        kq = txt("O QUE ACONTECE COM A ENERGIA CINÉTICA?", T_BODY, color=DIM).move_to(P3(0, 3.15))
        self.play(FadeIn(kq), run_time=0.7)
        nomes = {1.0: "ELÁSTICA", 0.5: "INELÁSTICA", 0.0: "COMPLETAMENTE INELÁSTICA"}
        lembra = {1.0: "rebatem", 0.5: "se separam", 0.0: "ficam juntos"}
        for e in VARIANTES:
            img = self.solido(e, LARG, CEN)
            labs = self.rotulos3d(img)
            lem = txt(lembra[e], T_NOTE, color=DIM).move_to(P3(XR, 2.25))
            self.play(FadeIn(img), FadeIn(labs), FadeIn(lem), run_time=0.8)
            self.play(FadeOut(labs), run_time=0.3)
            img.retomar()
            self.wait(4.4)
            nm = (txt(nomes[e], 40, color=CYAN) if e > 0 else VGroup(txt("COMPLETAMENTE", 36, color=CYAN),
                  txt("INELÁSTICA", 36, color=CYAN)).arrange(DOWN, buff=0.12)).move_to(P3(XR, 1.45))
            self.play(FadeIn(nm, shift=0.15 * UP), run_time=0.8)
            extra = VGroup()
            if e == 1.0:
                eqs = VGroup(M("P_i", "=", "P_f", size=M_M), M("K_i", "=", "K_f", size=M_M)) \
                    .arrange(DOWN, buff=0.4).move_to(P3(XR, 0.0))
                self.play(FadeIn(eqs[0]), run_time=0.7)
                self.wait(0.6)
                self.play(FadeIn(eqs[1]), run_time=0.7)
                self.wait(2.6)
            elif e == 0.5:
                eqs = VGroup(M("P_i", "=", "P_f", size=M_M), M("K_f", "<", "K_i", size=M_M)) \
                    .arrange(DOWN, buff=0.4).move_to(P3(XR, 0.25))
                self.play(FadeIn(eqs[0]), run_time=0.7)
                self.wait(0.5)
                self.play(FadeIn(eqs[1]), run_time=0.7)
                # K_i = 6 → K_f = 2 nas massas e velocidades da animação; 4 vão para energia interna
                L0, y0, x0 = 3.6, -1.55, XR - 1.8
                kb = Rectangle(width=L0, height=0.32, stroke_width=0, fill_color=CYAN, fill_opacity=0.85)
                kb.move_to(P3(x0 + L0 / 2, y0))
                ib = Rectangle(width=L0 * 4 / 6, height=0.32, stroke_width=0, fill_color=HEAT, fill_opacity=0.85)
                ib.move_to(P3(x0 + L0 * 4 / 6 / 2, y0 - 0.75))
                lk = M("K", size=M_S, color=CYAN).next_to(kb, LEFT, buff=0.15)
                li = txt("energia interna · deformação", T_CAP, color=HEAT).next_to(ib, DOWN, buff=0.15, aligned_edge=LEFT)
                self.play(FadeIn(kb), FadeIn(lk), run_time=0.6)
                kb_f = Rectangle(width=L0 * 2 / 6, height=0.32, stroke_width=0, fill_color=CYAN, fill_opacity=0.85)
                kb_f.move_to(P3(x0 + L0 / 6, y0))
                pedaco = kb.copy().stretch_to_fit_width(L0 * 4 / 6).move_to(P3(x0 + L0 * 2 / 6 + L0 * 2 / 6, y0))
                self.add(pedaco)
                self.play(Transform(kb, kb_f), Transform(pedaco, ib), FadeIn(li), run_time=1.6)
                extra = VGroup(kb, pedaco, lk, li)
                self.wait(2.6)
            else:
                eqs = VGroup(M("v_1", "=", "v_2", "=", "v_f", size=M_M)).move_to(P3(XR, 0.2))
                self.play(FadeIn(eqs), run_time=0.8)
                self.wait(2.8)
            self.play(FadeOut(img), FadeOut(nm), FadeOut(eqs), FadeOut(extra), FadeOut(lem), run_time=0.7)
            img.clear_updaters()
        self.play(FadeOut(kq), run_time=0.4)

        # Síntese: momento (restrição comum) + tipo de colisão (informação adicional)
        r1 = VGroup(txt("MOMENTO", 40), M(r"\rightarrow", size=M_L), txt("restrição comum", T_BODY, color=GREY, upper=False)) \
            .arrange(RIGHT, buff=0.4).move_to(P3(0, 1.2))
        r2 = VGroup(txt("TIPO DE COLISÃO", 40), M(r"\rightarrow", size=M_L),
                    txt("informação adicional", T_BODY, color=GREY, upper=False)).arrange(RIGHT, buff=0.4).move_to(P3(0, 0.0))
        self.play(FadeIn(r1), run_time=0.8)
        self.wait(1.6)
        self.play(FadeIn(r2), run_time=0.8)
        self.wait(1.8)
        fim = txt("momento + tipo de colisão", 48, color=CYAN, upper=False).move_to(P3(0, -1.6))
        self.play(FadeIn(fim, scale=0.95), run_time=0.9)
        self.play(Create(box(fim, buff=0.22)), run_time=0.7)
        self.wait(3.0)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C04 — Quando os corpos ficam juntos
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c04_completamente_inelastica(self):
        h = self.head("COMECEMOS PELO CASO MAIS SIMPLES.", size=T_BODY, color=DIM)
        self.play(FadeIn(h), run_time=0.7)
        m1, m2, u1, u2 = 2.0, 1.0, 2.0, -1.0
        vf = (m1 * u1 + m2 * u2) / (m1 + m2)
        c = Col(m1, m2, u1, u2, vf, vf, w1=1.1, w2=0.85, xc=-0.6, ty=-3.0, kx=1.0, ka=0.55, t0=-2.2, junto="v_f")
        self.play(FadeIn(c.group()), run_time=0.9)
        self.wait(1.4)
        self.play(c.t.animate.set_value(-0.0001), rate_func=linear, run_time=2.2)
        c.ao.set_value(0)
        self.play(c.t.animate.set_value(1.6), c.ao.animate.set_value(1), rate_func=linear, run_time=1.8)
        self.play(FadeOut(h), run_time=0.4)
        cond = M("v_1", "=", "v_2", "=", "v_f", size=M_L).move_to(P3(0, 2.75))
        self.play(FadeIn(cond, shift=0.2 * UP), run_time=0.9)
        self.wait(2.0)

        # Derivação: P_i = m1u1 + m2u2 ; P_f = (m1+m2) v_f
        pi = M("P_i", "=", "m_1u_1", "+", "m_2u_2", size=M_L).move_to(P3(-3.5, 1.45))
        pf = M("P_f", "=", "(m_1+m_2)", "v_f", size=M_L).move_to(P3(3.5, 1.45))
        self.play(FadeIn(pi), run_time=0.9)
        self.wait(1.2)
        self.play(FadeIn(pf), run_time=0.9)
        self.wait(1.4)
        eq = M("m_1u_1", "+", "m_2u_2", "=", "(m_1+m_2)", "v_f", size=M_L).move_to(P3(0, 0.3))
        self.play(TransformFromCopy(pi[2:], eq[:3]), FadeIn(eq[3]), TransformFromCopy(pf[2:], eq[4:]), run_time=1.3)
        self.settle(eq)
        self.wait(1.6)
        res = M("v_f", "=", r"\frac{m_1u_1+m_2u_2}{m_1+m_2}", size=M_XL).move_to(P3(0, 0.6))
        self.play(FadeOut(pi), FadeOut(pf), run_time=0.5)
        self.remap(eq, res, [([0, 1, 2, 4], 2), (5, 0), (3, 1)], rt=1.4)
        bx = box(res)
        self.play(Create(bx), run_time=0.6)
        self.wait(2.4)

        # Média ponderada numa reta de velocidades
        self.play(FadeOut(c.group()), FadeOut(cond), VGroup(res, bx).animate.scale(0.8).move_to(P3(0, 2.3)), run_time=1.0)
        r = ValueTracker(m1 / (m1 + m2))
        K, X0, Y = 2.2, -1.1, -1.4

        def X(v):
            return X0 + K * v

        reta = Line(P3(X(-1.8), Y), P3(X(2.8), Y), color=STEEL, stroke_width=3)
        lv = M("v", size=M_S, color=DIM).next_to(reta, RIGHT, buff=0.15)
        t1 = VGroup(Line(P3(X(u1), Y - 0.15), P3(X(u1), Y + 0.15), color=C1, stroke_width=5),
                    M("u_1", size=M_M).move_to(P3(X(u1), Y - 0.55)))
        t2 = VGroup(Line(P3(X(u2), Y - 0.15), P3(X(u2), Y + 0.15), color=C2, stroke_width=5),
                    M("u_2", size=M_M).move_to(P3(X(u2), Y - 0.55)))
        self.play(Create(reta), FadeIn(lv), FadeIn(t1), FadeIn(t2), run_time=1.0)

        def marcador():
            w = r.get_value()
            v = w * u1 + (1 - w) * u2
            d = Dot(P3(X(v), Y), radius=0.11, color=CYAN).set_z_index(5)
            lab = M("v_f", size=M_M, color=CYAN).move_to(P3(X(v), Y + 0.5))
            s1 = 0.45 + 0.75 * np.sqrt(w)
            s2 = 0.45 + 0.75 * np.sqrt(1 - w)
            b1 = corpo("m_1", C1, s1, size=30).move_to(P3(-5.6, -0.2 + s1 / 2 - 0.6))
            b2 = corpo("m_2", C2, s2, size=30).next_to(b1, RIGHT, buff=0.25, aligned_edge=DOWN)
            return VGroup(d, lab, b1, b2)

        mk = always_redraw(marcador)
        self.play(FadeIn(mk), run_time=0.8)
        nt = VGroup(M("v_f", size=M_S, color=GREY), txt("fica entre as velocidades iniciais", T_NOTE, color=GREY,
                    upper=False)).arrange(RIGHT, buff=0.2).move_to(P3(0, -2.75))
        self.play(FadeIn(nt), run_time=0.6)
        self.wait(1.8)
        self.play(r.animate.set_value(0.92), run_time=2.6)
        self.wait(0.8)
        self.play(r.animate.set_value(0.10), run_time=3.2)
        self.wait(0.8)
        self.play(r.animate.set_value(m1 / (m1 + m2)), run_time=1.8)
        n2 = txt("a massa maior pesa mais na velocidade final", T_BODY, color=CYAN, upper=False).move_to(P3(0, -2.75))
        self.play(ReplacementTransform(nt, n2), run_time=0.8)
        self.wait(2.6)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C05 — Momento conservado não significa energia cinética conservada
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c05_energia_cinetica(self):
        u = 2.0
        c = Col(1, 1, u, 0.0, u / 2, u / 2, w1=0.95, w2=0.95, xc=-3.2, ty=0.55, kx=0.95, ka=0.7, t0=-1.7,
                n1="m", n2="m", pre=("u", None), junto="v_f")
        cap = txt("massas iguais · alvo parado · ficam juntos", T_NOTE, color=DIM, upper=False).move_to(P3(-3.6, 2.9))
        self.play(FadeIn(c.group()), FadeIn(cap), run_time=1.0)
        self.wait(1.2)
        self.play(c.t.animate.set_value(-0.0001), rate_func=linear, run_time=1.7)
        c.ao.set_value(0)
        self.play(c.t.animate.set_value(1.2), c.ao.animate.set_value(1), rate_func=linear, run_time=1.6)

        XE = 3.9
        e = M("m", "u", "=", "(2m)", "v_f", size=M_L).move_to(P3(XE, 2.2))
        self.play(FadeIn(e), run_time=0.9)
        self.wait(1.2)
        e2 = M("v_f", "=", r"\frac{u}{2}", size=M_L).move_to(P3(XE, 2.2))
        self.remap(e, e2, [(4, 0), (2, 1), ([1, 3], 2)], rt=1.2)
        self.play(Create(box(e2)), run_time=0.5)
        self.wait(1.4)

        # Energia cinética: barras (K_f = metade exata de K_i)
        L0, XB, YB = 5.4, -6.4, -1.2
        ki = Rectangle(width=L0, height=0.42, stroke_width=0, fill_color=CYAN, fill_opacity=0.85)
        ki.move_to(P3(XB + L0 / 2, YB))
        lki = M("K_i", size=M_M, color=CYAN).next_to(ki, UP, buff=0.12, aligned_edge=LEFT)
        k1 = M("K_i", "=", r"\tfrac{1}{2}", "m", "u^2", size=M_L).move_to(P3(XE, 0.8))
        self.play(FadeIn(k1), FadeIn(ki), FadeIn(lki), run_time=1.0)
        self.wait(1.6)
        k2 = M("K_f", "=", r"\tfrac{1}{2}", "(2m)", r"\left(\tfrac{u}{2}\right)^2", size=M_L).move_to(P3(XE, -0.4))
        self.play(FadeIn(k2), run_time=1.0)
        self.wait(1.6)
        k3 = M("K_f", "=", r"\tfrac{1}{4}", "m", "u^2", size=M_L).move_to(P3(XE, -0.4))
        self.remap(k2, k3, [(0, 0), (1, 1), ([2, 4], 2), (3, 3), (4, 4)], rt=1.1)
        self.wait(1.2)
        k4 = M("K_f", "=", r"\tfrac{1}{2}", "K_i", size=M_L).move_to(P3(XE, -0.4))
        self.remap(k3, k4, [(0, 0), (1, 1), (2, 2), ([3, 4], 3)], rt=1.1)
        self.play(Create(box(k4)), run_time=0.5)

        kf = Rectangle(width=L0 / 2, height=0.42, stroke_width=0, fill_color=CYAN, fill_opacity=0.85)
        kf.move_to(P3(XB + L0 / 4, YB))
        resto = ki.copy().stretch_to_fit_width(L0 / 2).move_to(P3(XB + 3 * L0 / 4, YB))
        alvo = Rectangle(width=L0 / 2, height=0.42, stroke_width=0, fill_color=HEAT, fill_opacity=0.85)
        alvo.move_to(P3(XB + L0 / 4, YB - 1.25))
        lkf = M("K_f", size=M_M, color=CYAN).next_to(kf, UP, buff=0.12, aligned_edge=LEFT)
        guia = DashedLine(P3(XB + L0 / 2, YB + 0.45), P3(XB + L0 / 2, YB - 0.45), color=WHITE, stroke_width=2)
        lint = txt("deformação · aquecimento · vibração · energia interna", T_CAP, color=HEAT, upper=False) \
            .next_to(alvo, DOWN, buff=0.15, aligned_edge=LEFT)
        self.add(resto)
        self.play(Transform(ki, kf), ReplacementTransform(lki, lkf), Create(guia), run_time=1.2)
        self.play(Transform(resto, alvo), FadeIn(lint), run_time=1.4)
        self.wait(3.0)

        self.clear()
        p1 = txt("MOMENTO CONSERVADO", 48).move_to(P3(0, 1.3))
        p2 = txt("não implica", T_BODY, color=DIM, upper=False).move_to(P3(0, 0.3))
        p3 = txt("ENERGIA CINÉTICA CONSERVADA", 48, color=CYAN).move_to(P3(0, -0.7))
        self.play(FadeIn(p1), run_time=0.8)
        self.play(FadeIn(p2), run_time=0.6)
        self.play(FadeIn(p3), run_time=0.8)
        mt = M(r"P\ \text{conservado}", r"\;\not\Rightarrow\;", r"K\ \text{conservada}", size=M_M, color=GREY) \
            .move_to(P3(0, -2.1))
        self.play(FadeIn(mt), run_time=0.7)
        self.wait(3.4)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C06 — A colisão elástica tem uma segunda equação (núcleo)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c06_elastica_relativa(self):
        h = self.head("AGORA, A COLISÃO ELÁSTICA.", size=T_BODY, color=DIM)
        m1, m2, u1, u2 = 1.0, 2.0, 3.0, -1.5
        v1, v2 = elastica(m1, m2, u1, u2)     # (-3, 1.5)
        c = Col(m1, m2, u1, u2, v1, v2, w1=0.85, w2=1.1, xc=0.0, ty=-1.7, kx=0.9, ka=0.48, t0=-1.6)
        self.play(FadeIn(h), FadeIn(c.group()), run_time=1.0)
        self.wait(1.0)
        self.play(c.t.animate.set_value(-0.0001), rate_func=linear, run_time=1.6)
        c.ao.set_value(0)
        self.play(c.t.animate.set_value(1.3), c.ao.animate.set_value(1), rate_func=linear, run_time=1.6)
        self.wait(1.0)
        self.play(FadeOut(c.group()), FadeOut(h), run_time=0.8)

        # A — duas conservações
        P = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2v_2", size=M_L).move_to(P3(0.6, 1.1))
        E = M(r"\tfrac{1}{2}m_1u_1^2", "+", r"\tfrac{1}{2}m_2u_2^2", "=", r"\tfrac{1}{2}m_1v_1^2", "+",
              r"\tfrac{1}{2}m_2v_2^2", size=M_L).move_to(P3(0.6, -0.6))
        lp = txt("MOMENTO", T_CAP, color=DIM).next_to(P, LEFT, buff=0.5)
        le = txt("ENERGIA CINÉTICA", T_CAP, color=DIM).next_to(E, LEFT, buff=0.4)
        VGroup(lp, P).move_to(P3(0, 1.1))
        VGroup(le, E).move_to(P3(0, -0.6))
        self.play(FadeIn(lp), Write(P), run_time=1.4)
        self.wait(1.4)
        self.play(FadeIn(le), Write(E), run_time=1.6)
        self.wait(2.4)

        # B — reorganizar o momento
        self.play(E.animate.set_opacity(0.25), le.animate.set_opacity(0.25), run_time=0.6)
        P2 = M("m_1u_1", "-", "m_1v_1", "=", "m_2v_2", "-", "m_2u_2", size=M_L).move_to(P)
        P = self.swap(P, P2, rt=1.3)
        self.wait(1.0)
        P3_ = M("m_1", "(u_1-v_1)", "=", "m_2", "(v_2-u_2)", size=M_L).move_to(P)
        self.remap(P, P3_, [([0, 2], [0, 1]), (3, 2), ([4, 6], [3, 4])], rt=1.3)
        P = P3_
        f1, f2 = box(P[1], buff=0.08), box(P[4], buff=0.08)
        self.play(Create(f1), Create(f2), run_time=0.7)
        self.wait(2.2)
        n1 = M(r"(1)", size=M_S, color=DIM)
        self.play(FadeOut(f1), FadeOut(f2), FadeOut(lp), run_time=0.4)
        self.play(P.animate.scale(0.82).move_to(P3(0, 2.55)), run_time=0.9)
        n1.next_to(P, RIGHT, buff=0.5)
        self.play(FadeIn(n1), E.animate.set_opacity(1).move_to(P3(0, 0.6)), FadeOut(le), run_time=0.9)

        # C — energia como diferença de quadrados
        E2 = M("m_1u_1^2", "+", "m_2u_2^2", "=", "m_1v_1^2", "+", "m_2v_2^2", size=M_L).move_to(P3(0, 0.6))
        x2 = txt("× 2", T_NOTE, color=DIM).next_to(E, RIGHT, buff=0.4)
        self.play(FadeIn(x2), run_time=0.4)
        self.remap(E, E2, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], rt=1.1, extra=[FadeOut(x2)])
        E = E2
        self.wait(1.0)
        E3 = M("m_1u_1^2", "-", "m_1v_1^2", "=", "m_2v_2^2", "-", "m_2u_2^2", size=M_L).move_to(E)
        E = self.swap(E, E3, rt=1.3)
        self.wait(0.8)
        E4 = M("m_1", r"(u_1^2-v_1^2)", "=", "m_2", r"(v_2^2-u_2^2)", size=M_L).move_to(E)
        self.remap(E, E4, [([0, 2], [0, 1]), (3, 2), ([4, 6], [3, 4])], rt=1.3)
        E = E4
        self.wait(0.8)
        regra = M("a^2-b^2", "=", "(a-b)(a+b)", size=M_M, color=CYAN).move_to(P3(0, -1.0))
        b1, b2 = box(E[1], buff=0.08), box(E[4], buff=0.08)
        self.play(FadeIn(regra), Create(b1), Create(b2), run_time=0.9)
        self.wait(1.8)
        E5 = M("m_1", "(u_1-v_1)", "(u_1+v_1)", "=", "m_2", "(v_2-u_2)", "(v_2+u_2)", size=M_L).move_to(E)
        self.play(FadeOut(b1), FadeOut(b2), run_time=0.3)
        self.remap(E, E5, [(0, 0), (2, 3), (3, 4)], rt=1.6)
        E = E5
        self.play(FadeOut(regra), run_time=0.5)
        n2 = M(r"(2)", size=M_S, color=DIM).next_to(E, RIGHT, buff=0.5)
        self.play(FadeIn(n2), run_time=0.4)
        self.wait(1.8)

        # D — não dividir cegamente: usar (1) em (2)
        nd = txt("Não vamos simplesmente dividir.", T_BODY, color=GREY, upper=False).move_to(P3(0, -0.8))
        self.play(FadeIn(nd), run_time=0.7)
        self.wait(1.8)
        us = txt("Usamos (1) dentro de (2).", T_BODY, color=GREY, upper=False).move_to(P3(0, -0.8))
        self.play(ReplacementTransform(nd, us), run_time=0.7)
        bA, bB = box(VGroup(E[4], E[5]), buff=0.08), box(VGroup(P[3], P[4]), buff=0.08)
        self.play(Create(bA), Create(bB), run_time=0.7)
        self.wait(1.0)
        bC = box(VGroup(P[0], P[1]), buff=0.08)
        self.play(ReplacementTransform(bB, bC), run_time=0.7)
        E6 = M("m_1", "(u_1-v_1)", "(u_1+v_1)", "=", "m_1", "(u_1-v_1)", "(v_2+u_2)", size=M_L).move_to(E)
        self.play(FadeOut(bA), FadeOut(E[4]), FadeOut(E[5]), ReplacementTransform(VGroup(*E[:4], E[6]).copy(),
                  VGroup(*E6[:4], E6[6])), TransformFromCopy(P[0], E6[4]), TransformFromCopy(P[1], E6[5]), run_time=1.3)
        self.drop(E)
        self.settle(E6)
        E = E6
        self.play(FadeOut(bC), FadeOut(us), run_time=0.4)
        self.wait(1.2)
        E7 = M("m_1", "(u_1-v_1)", "(u_1+v_1)", "-", "m_1", "(u_1-v_1)", "(v_2+u_2)", "=", "0", size=M_L).move_to(E)
        self.remap(E, E7, [(0, 0), (1, 1), (2, 2), (3, 7), (4, 4), (5, 5), (6, 6)], rt=1.2, extra=[FadeOut(n2)])
        E = E7
        self.wait(1.2)
        E8 = M("m_1", "(u_1-v_1)", r"\big[", "(u_1+v_1)", "-", "(v_2+u_2)", r"\big]", "=", "0", size=M_L).move_to(E)
        self.remap(E, E8, [([0, 4], 0), ([1, 5], 1), (2, 3), (3, 4), (6, 5), (7, 7), (8, 8)], rt=1.5)
        E = E8
        bxE = box(E, color=WHITE, buff=0.16)
        self.play(Create(bxE), run_time=0.7)
        self.wait(2.2)

        # E — os dois ramos
        self.play(*[FadeOut(m) for m in (P, n1, bxE)], run_time=0.6)
        self.play(E.animate.scale(0.9).move_to(P3(0, 2.55)), run_time=0.9)
        XL_, XR_ = -3.9, 3.5
        sep = DashedLine(P3(-0.3, 1.8), P3(-0.3, -3.0), color=DIM, stroke_width=2)
        a1 = arrow(E[1].get_bottom() + DOWN * 0.1, P3(XL_, 1.55), color=DIM, width=3, tip=0.14)
        a2 = arrow(E[2:7].get_bottom() + DOWN * 0.1, P3(XR_, 1.55), color=DIM, width=3, tip=0.14)
        self.play(Create(sep), GrowArrow(a1), GrowArrow(a2), run_time=0.8)
        L1 = M("u_1-v_1", "=", "0", size=M_M).move_to(P3(XL_, 1.05))
        self.play(FadeIn(L1), run_time=0.7)
        self.wait(0.8)
        L2 = M("u_1", "=", "v_1", size=M_M).move_to(P3(XL_, 1.05))
        self.remap(L1, L2, [], rt=0.9)
        L3 = M(r"\Rightarrow", "u_2", "=", "v_2", size=M_M).move_to(P3(XL_, 0.15))
        lm = txt("(momento)", T_CAP, color=DIM, upper=False).next_to(L3, RIGHT, buff=0.25)
        self.play(FadeIn(L3), FadeIn(lm), run_time=0.8)
        tri = txt("RAMO TRIVIAL", T_NOTE, color=DIM).move_to(P3(XL_, -0.65))
        self.play(FadeIn(tri), run_time=0.6)
        # mini-diagrama: nada muda (as velocidades depois são as de antes)
        mini = VGroup()
        for k, (lb, yy) in enumerate((("antes", -1.4), ("depois", -2.2))):
            t = txt(lb, T_CAP, color=DIM, upper=False).move_to(P3(XL_ - 2.4, yy))
            r1 = arrow(P3(XL_ - 1.5, yy), P3(XL_ - 1.5 + 1.2, yy), color=C1, width=5, tip=0.16)
            r2 = arrow(P3(XL_ + 0.9, yy), P3(XL_ + 0.9 - 0.6, yy), color=C2, width=5, tip=0.16)
            mini.add(t, r1, r2)
        sm = txt("sem mudança: não houve colisão", T_CAP, color=DIM, upper=False).move_to(P3(XL_, -2.85))
        self.play(FadeIn(mini), FadeIn(sm), run_time=0.9)
        self.wait(1.6)
        R1 = M("(u_1+v_1)", "-", "(v_2+u_2)", "=", "0", size=M_M).move_to(P3(XR_, 1.05))
        self.play(FadeIn(R1), run_time=0.8)
        self.wait(0.8)
        R2 = M("u_1", "+", "v_1", "=", "v_2", "+", "u_2", size=M_M).move_to(P3(XR_, -0.05))
        self.play(FadeIn(R2, shift=0.2 * DOWN), run_time=1.0)
        self.wait(0.8)
        R3 = M("u_1", "-", "u_2", "=", "-", "(v_1-v_2)", size=M_L, color=WHITE).move_to(P3(XR_, -1.45))
        self.play(FadeIn(R3, shift=0.2 * DOWN), run_time=1.1)
        br = box(R3, buff=0.18)
        self.play(Create(br), VGroup(L2, L3, lm, tri, mini, sm, a1).animate.set_opacity(0.35), run_time=0.8)
        self.wait(2.6)

        # F — interpretação física: a colisão elástica inverte a velocidade relativa
        keep = R3
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.tag, self.wm, keep)], run_time=0.7)
        self.play(keep.animate.scale(0.9).move_to(P3(0, 2.6)), run_time=0.8)
        c = Col(m1, m2, u1, u2, v1, v2, w1=0.85, w2=1.1, xc=0.0, ty=-2.5, kx=0.9, ka=0.42, t0=-1.5)
        self.play(FadeIn(c.group()), run_time=0.8)
        KR, YR = 0.6, 0.55
        rel_i = arrow(P3(-KR * (u1 - u2) / 2, YR), P3(KR * (u1 - u2) / 2, YR), color=CYAN, width=7, tip=0.26)
        li = M("u_1-u_2", size=M_M).next_to(rel_i, UP, buff=0.1)
        ti = txt("aproximação", T_NOTE, color=DIM, upper=False).next_to(rel_i, DOWN, buff=0.15)
        self.play(GrowArrow(rel_i), FadeIn(li), FadeIn(ti), run_time=0.9)
        self.wait(1.6)
        self.play(c.t.animate.set_value(-0.0001), rate_func=linear, run_time=1.5)
        c.ao.set_value(0)
        self.play(c.t.animate.set_value(1.3), c.ao.animate.set_value(1), rate_func=linear, run_time=1.5)
        YR2 = -0.65
        rel_f = arrow(P3(KR * (v2 - v1) / 2, YR2), P3(-KR * (v2 - v1) / 2, YR2), color=CYAN, width=7, tip=0.26)
        lf = M("v_1-v_2", size=M_M).next_to(rel_f, DOWN, buff=0.1)
        tf = txt("afastamento", T_NOTE, color=DIM, upper=False).next_to(lf, DOWN, buff=0.1)
        self.play(TransformFromCopy(rel_i, rel_f), FadeIn(lf), FadeIn(tf), run_time=1.3)
        gl = VGroup(*[DashedLine(P3(x, YR + 0.2), P3(x, YR2 - 0.2), color=DIM, stroke_width=2)
                      for x in (-KR * 2.25, KR * 2.25)])
        self.play(Create(gl), run_time=0.7)
        mesmo = VGroup(txt("mesmo módulo", T_NOTE, color=GREY, upper=False),
                       txt("sentido invertido", T_NOTE, color=GREY, upper=False)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        mesmo.move_to(P3(KR * 2.25 + 0.5 + mesmo.width / 2, (YR + YR2) / 2))
        self.play(FadeIn(mesmo), run_time=0.7)
        self.wait(2.0)
        pay = txt("A colisão elástica inverte a velocidade relativa.", 38, color=CYAN, upper=False).move_to(P3(0, 1.6))
        self.play(FadeIn(pay, shift=0.15 * UP), run_time=0.9)
        self.play(Create(box(keep, buff=0.16)), run_time=0.6)
        self.wait(3.4)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C07 — As fórmulas gerais são consequência, não método
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c07_velocidades_gerais(self):
        A = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2v_2", size=M_M).move_to(P3(-3.6, 2.5))
        B = M("u_1", "-", "u_2", "=", "-", "(v_1-v_2)", size=M_M).move_to(P3(3.9, 2.5))
        la = txt("momento", T_CAP, color=DIM, upper=False).next_to(A, DOWN, buff=0.15)
        lb = txt("condição elástica", T_CAP, color=DIM, upper=False).next_to(B, DOWN, buff=0.15)
        self.play(FadeIn(A), FadeIn(la), run_time=0.8)
        self.play(FadeIn(B), FadeIn(lb), run_time=0.8)
        self.wait(2.0)
        s1 = M("v_2", "=", "u_1-u_2", "+", "v_1", size=M_L).move_to(P3(0, 0.9))
        self.play(TransformFromCopy(B, s1), run_time=1.2)
        self.wait(1.6)
        self.play(s1.animate.scale(0.75).move_to(P3(3.9, 1.2)), run_time=0.8)
        s2 = M("m_1u_1", "+", "m_2u_2", "=", "m_1v_1", "+", "m_2", "(u_1-u_2+v_1)", size=M_L).move_to(P3(0, 0.0))
        self.play(TransformFromCopy(A[:6], s2[:6]), TransformFromCopy(s1[2:], s2[7]), FadeIn(s2[6]), run_time=1.4)
        self.settle(s2)
        self.wait(3.0)
        s3 = M("(m_1-m_2)u_1", "+", "2m_2u_2", "=", "(m_1+m_2)v_1", size=M_L).move_to(P3(0, 0.0))
        self.play(FadeOut(s2, shift=0.2 * UP), FadeIn(s3, shift=0.2 * UP), run_time=1.2)
        nt = M(r"\text{agrupar termos em }", "u_1", r",\ ", "u_2", r"\text{ e }", "v_1", size=34, color=DIM) \
            .next_to(s3, DOWN, buff=0.3)
        self.play(FadeIn(nt), run_time=0.5)
        self.wait(3.0)
        s4 = M("v_1", "=", r"{m_1-m_2 \over m_1+m_2}", "u_1", "+", r"{2m_2 \over m_1+m_2}", "u_2", size=M_L) \
            .move_to(P3(0, 0.0))
        self.play(FadeOut(nt), FadeOut(s3, shift=0.2 * UP), FadeIn(s4, shift=0.2 * UP), run_time=1.3)
        b4 = box(s4)
        self.play(Create(b4), run_time=0.6)
        self.wait(3.2)
        s5 = M("v_2", "=", r"{2m_1 \over m_1+m_2}", "u_1", "+", r"{m_2-m_1 \over m_1+m_2}", "u_2", size=M_L) \
            .move_to(P3(0, -1.7))
        n5 = M(r"\text{com }", "v_2", "=", "u_1-u_2", "+", "v_1", size=34, color=DIM).next_to(s5, DOWN, buff=0.25)
        self.play(Indicate(s1, color=CYAN), run_time=0.8)
        self.play(FadeIn(s5, shift=0.2 * UP), FadeIn(n5), run_time=1.2)
        b5 = box(s5)
        self.play(Create(b5), run_time=0.6)
        self.wait(3.4)

        # Fechamento: resultado pequeno; método no centro
        self.play(*[FadeOut(m) for m in (A, B, la, lb, s1, n5)], run_time=0.6)
        res = VGroup(s4, b4, s5, b5)
        self.play(res.animate.scale(0.55).move_to(P3(0, 2.25)), run_time=1.0)
        self.play(VGroup(s4, s5).animate.set_opacity(0.55), VGroup(b4, b5).animate.set_stroke(opacity=0.45), run_time=0.5)
        lr = txt("RESULTADO", T_CAP, color=DIM).next_to(res, LEFT, buff=0.4)
        self.play(FadeIn(lr), run_time=0.5)
        met = txt("MÉTODO", 46, color=CYAN).move_to(P3(0, 0.55))
        i1 = txt("1. conservação do momento", T_BODY, upper=False)
        i2 = txt("2. condição física da colisão", T_BODY, upper=False)
        itens = VGroup(i1, i2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(P3(0, -0.75))
        self.play(FadeIn(met, scale=0.95), run_time=0.8)
        self.play(FadeIn(i1), run_time=0.6)
        self.wait(0.6)
        self.play(FadeIn(i2), run_time=0.6)
        self.wait(1.4)
        fim = txt("As fórmulas são consequência.", 36, color=CYAN, upper=False).move_to(P3(0, -2.3))
        self.play(FadeIn(fim), run_time=0.8)
        self.wait(2.6)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C08 — Três casos-limite (massas finitas na animação; resultados assintóticos com ≈)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c08_casos_limite(self):
        h = self.head("EM VEZ DE DECORAR, VAMOS TESTAR.", size=T_BODY, color=DIM)
        self.play(FadeIn(h), run_time=0.7)
        self.wait(1.4)
        u1 = 2.4
        casos = [
            (1.0, 1.0, 0.95, 0.95, (M("m_1", "=", "m_2", size=M_L), M("u_2", "=", "0", size=M_M)),
             (M("v_1", "=", "0", size=M_L), M("v_2", "=", "u_1", size=M_L)), None),
            (1.0, 30.0, 0.75, 1.25, (M("m_1", r"\ll", "m_2", size=M_L), M("u_2", "=", "0", size=M_M)),
             (M("v_1", r"\approx", "-u_1", size=M_L), M("v_2", r"\approx", "0", size=M_L)), "m_2 = 30\\,m_1"),
            (30.0, 1.0, 1.25, 0.75, (M("m_1", r"\gg", "m_2", size=M_L), M("u_2", "=", "0", size=M_M)),
             (M("v_1", r"\approx", "u_1", size=M_L), M("v_2", r"\approx", "2u_1", size=M_L)), "m_1 = 30\\,m_2"),
        ]
        first = True
        for m1, m2, w1, w2, hip, res, nota in casos:
            v1, v2 = elastica(m1, m2, u1, 0.0)
            c = Col(m1, m2, u1, 0.0, v1, v2, w1=w1, w2=w2, xc=-1.6, ty=-2.3, kx=1.0, ka=0.42, t0=-1.4,
                    post=("v_1" if abs(v1) > 0.05 else "v_1=0", "v_2"), pre=("u_1", "u_2=0"))
            hp = VGroup(*hip).arrange(DOWN, buff=0.25).move_to(P3(-4.6, 1.3))
            ex = VGroup()
            if nota:
                ex = M(r"\text{animação: } " + nota, size=26, color=DIM).next_to(hp, DOWN, buff=0.3)
            if first:
                self.play(FadeOut(h), run_time=0.4)
                first = False
            self.play(FadeIn(c.group()), FadeIn(hp), FadeIn(ex), run_time=0.9)
            self.wait(1.6)
            self.play(c.t.animate.set_value(-0.0001), rate_func=linear, run_time=1.4)
            c.ao.set_value(0)
            self.play(c.t.animate.set_value(1.25), c.ao.animate.set_value(1), rate_func=linear, run_time=1.8)
            rs = VGroup(*res).arrange(DOWN, buff=0.3).move_to(P3(3.6, 1.3))
            self.play(FadeIn(rs, shift=0.15 * UP), run_time=0.8)
            self.play(Create(box(rs, buff=0.2)), run_time=0.5)
            self.wait(3.2)
            self.clear(rt=0.6)
        s = txt("CASOS-LIMITE = TESTES DE PLAUSIBILIDADE", 44, color=CYAN).move_to(P3(0, 0.3))
        self.play(FadeIn(s, scale=0.95), run_time=0.9)
        self.wait(3.0)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C09–C11 — Pêndulo balístico (notação local: u bala, m bala, M bloco, V, h)
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def _pendulo(self, PV=P3(-3.0, 2.55), L=3.4):
        self.PV, self.LP = PV, L
        self.th = ValueTracker(0.0)
        self.bx = ValueTracker(-7.6)        # x do centro da bala (antes do impacto)
        self.dentro = False
        BW, BH = 1.35, 0.95
        self.BW, self.BH = BW, BH

        def centro():
            th = self.th.get_value()
            return PV + L * np.array([np.sin(th), -np.cos(th), 0.0])

        self.centro = centro
        teto = VGroup(Line(PV + LEFT * 0.9, PV + RIGHT * 0.9, color=STEEL, stroke_width=4),
                      *[Line(PV + RIGHT * (x - 0.1) + UP * 0.2, PV + RIGHT * (x + 0.1), color=STEEL, stroke_width=2)
                        for x in np.linspace(-0.8, 0.8, 8)])
        piv = Dot(PV, radius=0.07, color=GREY)

        def desenho():
            th = self.th.get_value()
            cc = centro()
            blk = RoundedRectangle(corner_radius=0.06, width=BW, height=BH, stroke_color=C2, stroke_width=3,
                                   fill_color=C2, fill_opacity=0.30).move_to(cc).rotate(th)
            fio = Line(PV, cc + np.array([-np.sin(th), np.cos(th), 0]) * BH / 2, color=GREY, stroke_width=2.5)
            lab = MathTex("M", font_size=34, color=WHITE).move_to(cc)
            g = VGroup(fio, blk, lab)
            if self.dentro:
                bal = RoundedRectangle(corner_radius=0.05, width=0.34, height=0.14, stroke_width=0, fill_color=C1,
                                       fill_opacity=1).move_to(cc + np.array([-0.38 * np.cos(th), -0.38 * np.sin(th), 0]))
                g.add(bal.rotate(th))
            return g

        def bala():
            if self.dentro:
                return VGroup()
            cc = centro()
            b = RoundedRectangle(corner_radius=0.05, width=0.34, height=0.14, stroke_width=0, fill_color=C1,
                                 fill_opacity=1).move_to(P3(self.bx.get_value(), cc[1]))
            lab = MathTex("m", font_size=30, color=WHITE).next_to(b, DOWN, buff=0.12)
            return VGroup(b, lab)

        self.pend = always_redraw(desenho)
        self.bal = always_redraw(bala)
        return VGroup(teto, piv), self.pend, self.bal

    def c09_pendulo_setup(self):
        h = self.head("AGORA UM PROBLEMA REAL MISTURA ETAPAS.", size=T_BODY, color=DIM)
        self.play(FadeIn(h), run_time=0.7)
        estat, pend, bal = self._pendulo()
        self.estat = estat
        self.play(FadeIn(estat), FadeIn(pend), FadeIn(bal), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(h), run_time=0.4)
        def seta_u():
            if self.dentro:
                return VGroup()
            x, y = self.bx.get_value(), self.centro()[1] + 0.35
            a = arrow(P3(x + 0.25, y), P3(x + 1.05, y), width=4, tip=0.15)
            return VGroup(a, MathTex("u", font_size=30, color=WHITE).next_to(a, UP, buff=0.06))

        lu = always_redraw(seta_u)
        self.add(lu)
        xin = self.centro()[0] - self.BW / 2 + 0.3
        self.play(self.bx.animate.set_value(xin), rate_func=linear, run_time=1.6)
        self.dentro = True
        self.remove(lu)
        TH = np.radians(38)
        self.TH = TH
        self.play(self.th.animate.set_value(TH), rate_func=rate_functions.ease_out_sine, run_time=2.2)
        self.wait(0.6)
        self.hmark = self._marca_h()
        self.play(FadeIn(self.hmark), run_time=0.8)
        self.wait(1.4)
        # duas etapas, lado a lado na linha do tempo
        tl = Line(P3(-6.8, -2.3), P3(6.8, -2.3), color=STEEL, stroke_width=3)
        cut = Line(P3(-1.6, -2.6), P3(-1.6, -2.0), color=WHITE, stroke_width=4)
        e1 = txt("ETAPA 1 — IMPACTO", T_NOTE, color=C1).move_to(P3(-4.2, -2.8))
        e2 = txt("ETAPA 2 — SUBIDA", T_NOTE, color=C2).move_to(P3(2.6, -2.8))
        z1 = Line(P3(-6.8, -2.3), P3(-1.6, -2.3), color=C1, stroke_width=6)
        z2 = Line(P3(-1.6, -2.3), P3(6.8, -2.3), color=C2, stroke_width=6)
        self.play(Create(tl), run_time=0.6)
        self.play(Create(cut), Create(z1), FadeIn(e1), run_time=0.7)
        self.play(Create(z2), FadeIn(e2), run_time=0.7)
        self.wait(1.4)
        pay = txt("Uma única conservação não resolve o processo inteiro.", 34, color=CYAN, upper=False) \
            .move_to(P3(3.2, 0.9))
        if pay.width > 7.4:
            pay = VGroup(txt("Uma única conservação", 34, color=CYAN, upper=False),
                         txt("não resolve o processo inteiro.", 34, color=CYAN, upper=False)) \
                .arrange(DOWN, buff=0.15).move_to(P3(3.6, 0.9))
        self.play(FadeIn(pay), run_time=0.8)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in (tl, cut, z1, z2, e1, e2, pay, self.hmark)], run_time=0.7)

    def _marca_h(self):
        y0 = (self.PV + self.LP * DOWN)[1]
        y1 = self.centro()[1]
        x1 = self.centro()[0]
        l0 = DashedLine(P3(self.PV[0] - 1.0, y0), P3(x1 + 1.3, y0), color=DIM, stroke_width=2)
        l1 = DashedLine(P3(self.PV[0] - 1.0, y1), P3(x1 + 1.3, y1), color=DIM, stroke_width=2)
        br = Brace(Line(P3(x1 + 1.3, y0), P3(x1 + 1.3, y1)), RIGHT, buff=0.08, color=WHITE)
        lh = MathTex("h", font_size=36, color=WHITE).next_to(br, RIGHT, buff=0.1)
        return VGroup(l0, l1, br, lh)

    def c10_pendulo_impacto(self):
        # volta ao instante do impacto
        self.dentro = False
        self.play(self.th.animate.set_value(0.0), self.bx.animate.set_value(-6.6), run_time=1.0)
        tt = txt("ETAPA 1 — IMPACTO", T_NOTE, color=C1).move_to(P3(-3.0, 3.25))
        self.play(FadeIn(tt), run_time=0.5)
        cc = self.centro()
        eixo = VGroup(arrow(P3(-6.8, cc[1] - 1.05), P3(-0.6, cc[1] - 1.05), color=DIM, width=3, tip=0.16),
                      MathTex("x", font_size=32, color=DIM).move_to(P3(-0.4, cc[1] - 0.8)))
        peso = VGroup(arrow(cc, cc + DOWN * 0.95, color=GREY, width=3.5, tip=0.15),
                      txt("peso", T_CAP, color=GREY, upper=False).move_to(cc + DOWN * 0.75 + LEFT * 0.55))
        tens = VGroup(arrow(cc + UP * self.BH / 2, cc + UP * (self.BH / 2 + 0.85), color=GREY, width=3.5, tip=0.15),
                      txt("tensão", T_CAP, color=GREY, upper=False).move_to(cc + UP * 1.05 + LEFT * 0.6))
        self.play(FadeIn(eixo), run_time=0.6)
        self.play(FadeIn(peso), FadeIn(tens), run_time=0.8)
        nj = txt("verticais", T_CAP, color=GREY, upper=False).move_to(cc + RIGHT * 1.35 + UP * 0.2)
        self.play(FadeIn(nj), run_time=0.5)
        im = txt("impulso externo horizontal ≈ 0", T_NOTE, color=WHITE, upper=False).move_to(P3(-3.4, -2.55))
        self.play(FadeIn(im), run_time=0.7)
        self.wait(1.6)

        XE = 3.9
        ant = VGroup(txt("ANTES", T_CAP, color=DIM), M("P_x", "=", "m", "u", size=M_L)).arrange(RIGHT, buff=0.4) \
            .move_to(P3(XE, 2.0))
        ant[1][0].set_color(CYAN)
        self.play(FadeIn(ant), run_time=0.7)
        lu = VGroup(a := arrow(P3(-6.2, cc[1] + 0.35), P3(-5.4, cc[1] + 0.35), width=4, tip=0.15),
                    MathTex("u", font_size=30).next_to(a, UP, buff=0.06))
        self.play(FadeIn(lu), run_time=0.4)
        # K antes / depois (barra reduz no impacto)
        L0 = 2.6
        kb = Rectangle(width=L0, height=0.3, stroke_width=0, fill_color=CYAN, fill_opacity=0.85)
        kb.move_to(P3(XE - 1.3 + L0 / 2, -2.25))
        lk = M("K", size=M_S, color=CYAN).next_to(kb, LEFT, buff=0.15)
        self.play(FadeIn(kb), FadeIn(lk), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(lu), self.bx.animate.set_value(cc[0] - self.BW / 2 + 0.3), rate_func=linear, run_time=1.2)
        self.dentro = True
        kf = Rectangle(width=L0 * 0.2, height=0.3, stroke_width=0, fill_color=CYAN, fill_opacity=0.85)
        kf.move_to(P3(XE - 1.3 + L0 * 0.1, -2.25))
        lV = VGroup(a2 := arrow(P3(cc[0] + 0.85, cc[1]), P3(cc[0] + 1.85, cc[1]), width=5, tip=0.18),
                    MathTex("V", font_size=40).next_to(a2, UP, buff=0.06))
        nk = txt("K não se conserva", T_CAP, color=GREY, upper=False).next_to(kb, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(Transform(kb, kf), FadeIn(nk), FadeOut(tens), FadeOut(nj), FadeIn(lV), run_time=1.0)
        dep = VGroup(txt("DEPOIS", T_CAP, color=DIM), M("P_x", "=", "(m+M)", "V", size=M_L)).arrange(RIGHT, buff=0.4) \
            .move_to(P3(XE, 0.95))
        dep[1][0].set_color(CYAN)
        self.play(FadeIn(dep), run_time=0.7)
        self.wait(1.6)
        eq = M("m", "u", "=", "(m+M)", "V", size=M_XL).move_to(P3(XE, -0.4))
        self.play(TransformFromCopy(ant[1][2:], eq[:2]), FadeIn(eq[2]), TransformFromCopy(dep[1][2:], eq[3:]),
                  run_time=1.3)
        self.settle(eq)
        tipo = txt("COLISÃO COMPLETAMENTE INELÁSTICA", T_CAP, color=CYAN).next_to(eq, DOWN, buff=0.3)
        self.play(FadeIn(tipo), run_time=0.6)
        self.wait(3.4)
        # V permanece: é o elo com a etapa seguinte
        self.play(*[FadeOut(m) for m in (ant, dep, kb, lk, nk, tipo, eixo, peso, im, tt)], run_time=0.7)
        self.play(eq.animate.scale(0.7).move_to(P3(3.9, 2.3)), run_time=0.9)
        self.eq_imp = eq
        self.lV = lV
        self.play(Indicate(eq[4], color=CYAN), Indicate(lV[1], color=CYAN), run_time=1.0)
        self.wait(1.2)

    def c11_pendulo_subida(self):
        tt = txt("ETAPA 2 — SUBIDA", T_NOTE, color=C2).move_to(P3(-3.0, 3.25))
        hip = txt("sem resistência do ar · sem dissipação no pivô", T_CAP, color=DIM, upper=False).move_to(P3(-3.0, -2.75))
        self.play(FadeIn(tt), FadeIn(hip), run_time=0.7)
        self.wait(0.8)
        # barras K → U_g sincronizadas com a altura
        XB, YK, L0 = 1.9, -1.75, 2.8
        TH = self.TH

        def barras():
            f = (1 - np.cos(self.th.get_value())) / (1 - np.cos(TH))
            k = Rectangle(width=max(L0 * (1 - f), 0.001), height=0.3, stroke_width=0, fill_color=CYAN, fill_opacity=0.85)
            k.move_to(P3(XB + L0 * (1 - f) / 2, YK))
            u = Rectangle(width=max(L0 * f, 0.001), height=0.3, stroke_width=0, fill_color=C2, fill_opacity=0.85)
            u.move_to(P3(XB + L0 * f / 2, YK - 0.6))
            return VGroup(k, u)

        bars = always_redraw(barras)
        lb = VGroup(M("K", size=M_S, color=CYAN).move_to(P3(XB - 0.45, YK)),
                    M("U_g", size=M_S, color=C2).move_to(P3(XB - 0.5, YK - 0.6)))
        self.play(FadeIn(bars), FadeIn(lb), FadeOut(self.lV), run_time=0.6)
        self.play(self.th.animate.set_value(TH), rate_func=rate_functions.ease_out_sine, run_time=2.6)
        hm = self._marca_h()
        self.play(FadeIn(hm), run_time=0.7)
        self.wait(1.2)

        XE = 3.9
        e1 = M(r"\tfrac{1}{2}", "(m+M)", "V^2", "=", "(m+M)", "g", "h", size=M_L, w=6.4).move_to(P3(XE, 1.0))
        self.play(FadeIn(e1), run_time=1.0)
        self.wait(2.6)
        e2 = M("V^2", "=", "2", "g", "h", size=M_L).move_to(P3(XE, 1.0))
        self.remap(e1, e2, [(2, 0), (3, 1), (0, 2), (5, 3), (6, 4)], rt=1.3)
        self.wait(0.8)
        e3 = M("V", "=", r"\sqrt{2gh}", size=M_L).move_to(P3(XE, 1.0))
        self.remap(e2, e3, [(0, 0), (1, 1), ([2, 3, 4], 2)], rt=1.1)
        self.play(Create(box(e3)), run_time=0.5)
        self.wait(1.6)
        # volta à etapa 1
        eqi = self.eq_imp
        self.play(eqi.animate.scale(1 / 0.7).move_to(P3(XE, -0.4)), run_time=0.9)
        e4 = M("u", "=", r"{m+M \over m}", "V", size=M_L).move_to(P3(XE, -0.4))
        self.remap(eqi, e4, [(1, 0), (2, 1), ([0, 3], 2), (4, 3)], rt=1.3)
        self.wait(1.0)
        e5 = M("u", "=", r"{m+M \over m}", r"\sqrt{2gh}", size=M_L).move_to(P3(XE, -0.6))
        self.play(FadeOut(e4[3]), TransformFromCopy(e3[2], e5[3]), ReplacementTransform(e4[:3], e5[:3]), run_time=1.3)
        self.drop(e4)
        self.settle(e5)
        self.wait(3.0)

        # Payoff: cada intervalo físico pode exigir uma lei diferente
        outs = [m for m in self.mobjects if m not in (self.tag, self.wm, e5)]
        self.play(*[FadeOut(m) for m in outs], e5.animate.scale(0.6).move_to(P3(0, 2.55)).set_opacity(0.6),
                  run_time=0.9)
        for m in outs:
            m.clear_updaters()
        self.remove(*outs)
        r1 = VGroup(txt("IMPACTO", 40, color=C1), M(r"\rightarrow", size=M_L),
                    txt("momento horizontal", T_BODY, upper=False)).arrange(RIGHT, buff=0.4).move_to(P3(0, 1.1))
        r2 = VGroup(txt("SUBIDA", 40, color=C2), M(r"\rightarrow", size=M_L),
                    txt("energia mecânica", T_BODY, upper=False)).arrange(RIGHT, buff=0.4)
        r2.move_to(P3(0, 0.0)).align_to(r1, LEFT)
        self.play(FadeIn(r1), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(r2), run_time=0.8)
        self.wait(1.2)
        pay = txt("Cada intervalo físico pode exigir uma lei diferente.", 38, color=CYAN, upper=False) \
            .move_to(P3(0, -1.5))
        self.play(FadeIn(pay, shift=0.15 * UP), run_time=0.9)
        self.wait(3.2)
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    # C12 — O método que funciona em prova + ponte para 2D
    # ══════════════════════════════════════════════════════════════════════════════════════════════════════════
    def c12_metodo_e_ponte_2d(self):
        h = self.head("ISSO SUGERE UM MÉTODO GERAL.", size=T_BODY, color=DIM)
        self.play(FadeIn(h), run_time=0.7)
        self.wait(1.0)
        self.play(FadeOut(h), run_time=0.4)
        XQ, XA = -6.6, 1.2
        ys = [2.55, 1.45, 0.35, -0.75, -2.15]
        perg = ["1. Qual é o sistema?", "2. O impulso externo na colisão é desprezível?", "3. Quantas incógnitas existem?",
                "4. O que o enunciado diz sobre a colisão?", "5. Existe uma nova etapa depois da colisão?"]
        nos = []
        for k, (p, y) in enumerate(zip(perg, ys)):
            q = txt(p, 28, upper=False)
            q.move_to(P3(XQ + q.width / 2, y))
            nos.append(q)

        def destaque(k):
            return [nos[j].animate.set_opacity(0.4) for j in range(k)]

        self.play(FadeIn(nos[0]), run_time=0.6)
        self.wait(1.4)
        self.play(*destaque(1), FadeIn(nos[1]), run_time=0.6)
        r2 = VGroup(txt("sim", T_NOTE, color=DIM, upper=False), M(r"\rightarrow", size=M_M), M("P_i", "=", "P_f", size=M_M)) \
            .arrange(RIGHT, buff=0.25)
        r2.move_to(P3(nos[1].get_right()[0] + 0.5 + r2.width / 2, ys[1]))
        self.play(FadeIn(r2), run_time=0.6)
        self.wait(1.4)
        self.play(*destaque(2), r2.animate.set_opacity(0.4), FadeIn(nos[2]), run_time=0.6)
        self.wait(1.4)
        self.play(*destaque(3), FadeIn(nos[3]), run_time=0.6)
        ramos = VGroup(
            VGroup(txt("ELÁSTICA", T_CAP, color=CYAN), M("K_i", "=", "K_f", size=M_S)).arrange(DOWN, buff=0.12),
            VGroup(txt("COMPLETAMENTE INELÁSTICA", T_CAP, color=CYAN), M("v_1", "=", "v_2", size=M_S)).arrange(DOWN, buff=0.12),
            VGroup(txt("OUTRA CONDIÇÃO", T_CAP, color=CYAN), txt("usar a condição dada", T_CAP, color=WHITE, upper=False))
            .arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=0.55).move_to(P3(1.6, ys[3] - 0.65))
        ramos.next_to(nos[3], DOWN, buff=0.18).align_to(nos[3], LEFT).shift(RIGHT * 0.6)
        self.play(LaggedStart(*[FadeIn(r) for r in ramos], lag_ratio=0.35), run_time=1.4)
        self.wait(1.8)
        self.play(*destaque(4), ramos.animate.set_opacity(0.4), FadeIn(nos[4]), run_time=0.6)
        r5 = VGroup(txt("sim", T_NOTE, color=DIM, upper=False), M(r"\rightarrow", size=M_M),
                    txt("SEPARE OS PROCESSOS", T_NOTE, color=CYAN)).arrange(RIGHT, buff=0.25)
        r5.next_to(nos[4], DOWN, buff=0.2).align_to(nos[4], LEFT).shift(RIGHT * 0.6)
        self.play(FadeIn(r5), run_time=0.6)
        self.wait(2.0)
        self.clear(rt=0.6)
        sint = txt("momento + tipo de colisão", 48, color=CYAN, upper=False).move_to(P3(0, 0.2))
        self.play(FadeIn(sint, scale=0.95), Create(box(sint, buff=0.22)), run_time=0.9)
        self.wait(2.2)
        self.clear(rt=0.6)

        # Ponte final: o momento é vetorial
        m1, m2, u1, u2 = 1.0, 1.0, 2.2, 0.0
        c = Col(m1, m2, u1, u2, 0.0, u1, w1=0.95, w2=0.95, xc=-0.8, ty=-1.6, kx=0.9, ka=0.55, t0=-1.5,
                pre=("u_1", None), post=(None, None))
        self.play(FadeIn(c.group()), run_time=0.8)
        lin = txt("até aqui: todas as velocidades sobre uma linha", T_NOTE, color=DIM, upper=False).move_to(P3(0, -2.6))
        self.play(FadeIn(lin), run_time=0.6)
        e = M("P_i", "=", "P_f", size=M_XL).move_to(P3(0, 2.2))
        self.play(FadeIn(e), run_time=0.8)
        self.wait(1.2)
        ev = M(r"\vec P_i", "=", r"\vec P_f", size=M_XL, color=CYAN).move_to(P3(0, 2.2))
        self.play(ReplacementTransform(e, ev), run_time=1.0)
        self.wait(0.8)
        # depois do contato: pela primeira vez, velocidades finais fora do eixo
        b1c, b2c = c.b1.get_center(), c.b2.get_center()
        ang = np.radians(32)
        s1 = arrow(b1c + UP * 0.8, b1c + UP * 0.8 + 1.15 * np.array([np.cos(-ang * 0.9), np.sin(-ang * 0.9), 0]),
                   width=5, tip=0.18)
        s2 = arrow(b2c + UP * 0.8, b2c + UP * 0.8 + 1.55 * np.array([np.cos(ang), np.sin(ang), 0]), width=5, tip=0.18)
        ax = DashedLine(P3(-7.0, b1c[1] + 0.8), P3(7.0, b1c[1] + 0.8), color=DIM, stroke_width=1.5)
        self.play(FadeOut(lin), FadeOut(c.arrows), Create(ax), run_time=0.6)
        self.play(GrowArrow(s2), run_time=0.9)
        self.play(GrowArrow(s1), run_time=0.7)
        self.wait(1.6)
        prox = txt("PRÓXIMO: COLISÕES EM DUAS DIMENSÕES", 40, color=WHITE).move_to(P3(0, -2.7))
        self.play(FadeIn(prox, shift=0.15 * UP), run_time=0.9)
        self.wait(3.2)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.wm,)], run_time=1.2)
        self.wait(0.6)
